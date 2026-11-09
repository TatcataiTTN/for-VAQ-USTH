"""Merge the scans of Floyd, Jaeger, EASA (and SERVO: it has no exercises) into data/numeric/catalog.json.
Each entry: id, book, kind, chapter, section, number, pdf, printed, text, answer, nq (quantities with units), numeric, figure, sim, module(s), in_site(modules), cls.
cls: in_site | ready (mapped, numeric, no figure, no simulator) | figure | simulation | conceptual | outside (belongs to no module of AE2.025).
Run: python3 -I build/numeric/scan_jaeger.py && scan_floyd.py && scan_easa.py && scan_all.py"""
import re, os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import *
M = load_map()

def load(name): return json.load(open(os.path.join(OUT, name), encoding='utf-8'))
raw = load('floyd_raw.json') + load('jaeger_raw.json') + load('easa_raw.json')
FANS = {int(c): {int(n): t for n, t in d.items()} for c, d in load('floyd_answers.json').items()}      # printed answers of the odd Floyd problems

# ---- module of each entry
FLOYD_CH = {12: 'm02', 13: 'm03', 14: 'm05', 15: 'm06', 16: 'm07', 17: 'm08'}
jsec = {s['num']: [m for m, r in s['mods'].items()] for c in M['jaeger5']['chapters'] for s in c['sections'] if s['num']}
# ---- what the banks already hold
held = collections.defaultdict(set)
KMAP = {'Self-Test': 'selftest', 'True/False Quiz': 'truefalse', 'Circuit-Action Quiz': 'circuit_action', 'Problem': 'problem'}
for mid in ['m%02d' % i for i in range(1, 11)]:
    b = json.load(open(os.path.join(ROOT, 'data', 'qbank', mid + '.json'), encoding='utf-8'))
    for it in b['items'] + b.get('essays', []):
        s = it['src']['en'] if isinstance(it['src'], dict) else it['src']
        m = re.match(r'^Floyd 9e, Ch\.(\d+), (Self-Test|True/False Quiz|Circuit-Action Quiz|Problem) (?:Q)?(\d+)\b', s)
        if m: held[('floyd', int(m[1]), KMAP[m[2]], m[3])].add(mid)
        m = re.match(r'^EASA M04 SM0?\d, Question (\d+-\d+)\b', s)
        if m: held[('easa', 0, 'question', m[1])].add(mid)

def modules_of(e):
    b, k, n, sec = e['book'], e['kind'], e['chapter'], e['section']
    if b == 'floyd':
        if n in FLOYD_CH: return [FLOYD_CH[n]]
        if n in (6, 7):
            if sec in ('6–6', '7–2', '7–3') or (n == 7 and k in ('truefalse', 'circuit_action', 'selftest', 'problem', 'related_problem') and sec in (None, '7–2', '7–3', '7–1') and False): return ['m04']
        return []
    if b == 'jaeger5':
        return jsec.get(sec, []) if sec else []
    if b == 'easa':
        if n == 1: return ['m01'] if int(e['number'].split('-')[1]) >= 23 else []
        return ['m09'] if n == 2 else ['m10']
    return []

SOLVED = load('jaeger_solved.json') if os.path.exists(os.path.join(OUT, 'jaeger_solved.json')) else dict(solved={}, skipped={})
CALC = load('calc_solved.json') if os.path.exists(os.path.join(OUT, 'calc_solved.json')) else dict(solved={}, skipped={})     # Floyd/Jaeger Examples, Related Problems, Checkups, even problems (build/numeric/csol)
def parts_text(parts): return ' | '.join((f'{a}: {b}' if b else a) for a, b in parts)
cat = []
for e in raw:
    e = dict(e); b = e['book']
    if b == 'floyd' and e['kind'] == 'problem' and e['number'].isdigit(): e['answer'] = FANS.get(e['chapter'], {}).get(int(e['number']))
    e['modules'] = modules_of(e)
    if b == 'jaeger5' and e['kind'] == 'problem' and e['number'] in SOLVED['solved']:
        sv = SOLVED['solved'][e['number']]; e['answer'] = parts_text(sv['parts']); e['ans_kind'] = 'computed'; e['how'] = sv['how']; e['assume'] = sv['assume']; e['parts'] = sv['parts']
        e['modules'] = sorted(set(e['modules']) | set(sv['modules']))
    elif b == 'jaeger5' and e['kind'] == 'problem' and e['number'] in SOLVED['skipped']: e['skip'] = SOLVED['skipped'][e['number']]['reason']
    elif e.get('answer'): e['ans_kind'] = 'printed'
    ck = '|'.join((b, e['kind'], str(e['chapter']), str(e['number'])))
    if ck in CALC['solved'] and e.get('ans_kind') != 'printed':
        sv = CALC['solved'][ck]; e['answer'] = parts_text(sv['parts']); e['ans_kind'] = 'computed'; e['how'] = sv['how']; e['assume'] = sv['assume']; e['parts'] = sv['parts']; e['calc'] = 1
        if sv.get('ctx'): e['ctx'] = sv['ctx']
        if sv.get('circuit'): e['circuit'] = sv['circuit']             # the circuit of a book figure, described in words with its values (the figure itself is not republished)
        e['modules'] = sorted(set(e['modules']) | set(sv['modules']))
    elif ck in CALC['skipped']: e['skip'] = CALC['skipped'][ck]['reason']
    key = (b, e['chapter'] if b == 'floyd' else 0, e['kind'], e['number'])
    e['in_site'] = sorted(held.get(key, []))
    if b == 'floyd' and e['chapter'] in (6, 7) and e['in_site']: e['modules'] = sorted(set(e['modules']) | set(e['in_site']))
    cat.append(e)

def cls(e):
    if e['in_site']: return 'in_site'
    if e.get('ans_kind') == 'computed': return 'solved'
    if not e['modules']: return 'outside'
    if e.get('sim'): return 'simulation'
    if not e['numeric']: return 'conceptual'
    if e.get('figure'): return 'figure'
    return 'ready'
for i, e in enumerate(cat):
    e['id'] = f"{e['book']}-{e['kind']}-{e['chapter']}-{e['number'] or i}-{i}"; e['cls'] = cls(e)

json.dump(cat, open(os.path.join(OUT, 'catalog.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# ---- summary
C = collections.Counter
by = collections.defaultdict(lambda: C())
for e in cat:
    k = (e['book'], e['kind']); by[k]['total'] += 1; by[k]['numeric'] += e['numeric']; by[k]['figure'] += bool(e.get('figure')); by[k]['answer'] += e.get('ans_kind') == 'printed'; by[k]['solved'] += e.get('ans_kind') == 'computed'; by[k]['skipped'] += bool(e.get('skip')); by[k]['mapped'] += bool(e['modules']); by[k]['in_site'] += bool(e['in_site']); by[k]['ready'] += e['cls'] == 'ready'
print(f"{'book / kind':28s} total numeric figure answer solved mapped in_site ready")
for k, v in sorted(by.items()): print(f"{k[0] + ' / ' + k[1]:28s} {v['total']:5d} {v['numeric']:7d} {v['figure']:6d} {v['answer']:6d} {v['solved']:6d} {v['mapped']:6d} {v['in_site']:7d} {v['ready']:5d}")
print('TOTAL entries', len(cat), '| numeric', sum(e['numeric'] for e in cat))
pm = collections.defaultdict(C)
for e in cat:
    for m in e['modules']: pm[m]['mapped'] += 1; pm[m][e['cls']] += 1; pm[m]['numeric'] += e['numeric']
print('per module:')
for m in sorted(pm): print(' ', m, dict(pm[m]))
json.dump({'by_kind': {f'{k[0]}/{k[1]}': dict(v) for k, v in by.items()}, 'per_module': {m: dict(v) for m, v in pm.items()}, 'total': len(cat)}, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
