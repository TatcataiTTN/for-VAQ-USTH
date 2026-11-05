"""Merge data/qsrc/mNN.json (original questions) + data/qsrc/mNN_gen.json (generated) -> data/qbank/mNN.json.
Validates every item, balances correct-answer position where allowed, runs the bias audit (data/qbank/_audit.json).
Run:  python3 build/assemble.py"""
import json, os, sys, random, collections
sys.path.insert(0, os.path.dirname(__file__))
from modules import MODS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'data', 'qsrc'); OUT = os.path.join(ROOT, 'data', 'qbank')
KINDS = {'mcq', 'tf', 'ca', 'ess'}

def bi(x, field, it):
    if not (isinstance(x, dict) and x.get('vi', '').strip() and x.get('en', '').strip()):
        raise ValueError(f'{it.get("src")}: field {field} must be {{"vi":..,"en":..}} non-empty, got {str(x)[:80]}')

def validate(it):
    k = it.get('kind')
    if k not in KINDS: raise ValueError(f'bad kind {k} in {it.get("src")}')
    bi(it['q'], 'q', it); bi(it['topic'], 'topic', it)
    if it.get('origin') not in ('goc', 'bo_sung'): raise ValueError(f'bad origin in {it.get("src")}')
    if it.get('level') not in (1, 2, 3): raise ValueError(f'bad level in {it.get("src")}')
    if not it.get('src'): raise ValueError('missing src')
    if k == 'ess':
        bi(it['sol'], 'sol', it); return
    bi(it['explain'], 'explain', it)
    o = it['opts']
    if not (2 <= len(o) <= 5): raise ValueError(f'{it["src"]}: needs 2-5 options')
    for x in o: bi(x, 'opt', it)
    for lang in ('vi', 'en'):
        if len({x[lang].strip() for x in o}) != len(o): raise ValueError(f'{it["src"]}: duplicate options ({lang})')
    if not (isinstance(it['correct'], int) and 0 <= it['correct'] < len(o)): raise ValueError(f'{it["src"]}: bad correct index')

def audit(items):
    rep = {}
    groups = collections.defaultdict(list)
    for it in items: groups[(it['kind'], len(it['opts']))].append(it)
    for (k, n), g in sorted(groups.items()):
        pos = collections.Counter(it['correct'] for it in g); exp = len(g) / n
        chi = sum((pos.get(i, 0) - exp) ** 2 / exp for i in range(n))
        multi = [it for it in g if len({len(o['en']) for o in it['opts']}) > 1]
        longest = sum(1 for it in multi if len(it['opts'][it['correct']]['en']) > max(len(o['en']) for i, o in enumerate(it['opts']) if i != it['correct']))
        rep[f'{k}/{n}opt'] = dict(n=len(g), pos=[pos.get(i, 0) for i in range(n)], chi2=round(chi, 2),
                                   correct_is_longest=round(longest / max(1, len(multi)), 3))
    return rep

def main():
    os.makedirs(OUT, exist_ok=True); full = {}
    only = set(filter(None, os.environ.get('ONLY', '').split(',')))
    prev = json.load(open(os.path.join(OUT, '_audit.json'))) if os.path.exists(os.path.join(OUT, '_audit.json')) else {}
    full.update(prev)
    for m in MODS:
        mid = m['id']; items = []
        if only and mid not in only: continue
        import glob
        for p in sorted(glob.glob(os.path.join(SRC, f'{mid}*.json'))):   # mNN.json, mNN_gen.json, mNN_easa.json ...
            items += json.load(open(p, encoding='utf-8'))
        if not items: print(mid, 'no questions yet'); continue
        for it in items: validate(it)
        mcq = [i for i in items if i['kind'] != 'ess']; ess = [i for i in items if i['kind'] == 'ess']
        rng = random.Random(int(mid[1:]) * 97 + 5)
        # balance position only where options are independent (fixed_order=True keeps book order, e.g. "answers (a) and (b)")
        bal = collections.defaultdict(list)
        for it in mcq:
            if not it.get('fixed_order') and it['kind'] == 'mcq': bal[len(it['opts'])].append(it)
        for n, g in bal.items():
            targets = [i % n for i in range(len(g))]; rng.shuffle(targets)
            for it, t in zip(g, targets):
                c = it['correct']
                if c != t: it['opts'][c], it['opts'][t] = it['opts'][t], it['opts'][c]; it['correct'] = t
        # originals first (book order), generated after
        mcq.sort(key=lambda i: 0 if i['origin'] == 'goc' else 1)
        for k, it in enumerate(mcq): it['id'] = f'{mid}-{k + 1:03d}'
        for k, it in enumerate(ess): it['id'] = f'{mid}-E{k + 1:02d}'
        tmp = os.path.join(OUT, f'{mid}.json.tmp'); json.dump(dict(module=mid, items=mcq, essays=ess), open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':')); os.replace(tmp, os.path.join(OUT, f'{mid}.json'))
        a = audit(mcq); n_goc = sum(1 for i in mcq if i['origin'] == 'goc')
        full[mid] = dict(n=len(mcq), n_goc=n_goc, n_bo_sung=len(mcq) - n_goc, essays=len(ess),
                         essays_goc=sum(1 for e in ess if e['origin'] == 'goc'), audit=a)
        print(mid, f'MCQ {len(mcq)} (orig {n_goc}) | worked {len(ess)} |', {k: (v['pos'], v['chi2'], v['correct_is_longest']) for k, v in a.items()})
    tmp = os.path.join(OUT, '_audit.json.tmp'); json.dump(full, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); os.replace(tmp, os.path.join(OUT, '_audit.json'))

if __name__ == '__main__':
    main()
