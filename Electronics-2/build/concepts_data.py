"""Build concepts/data.json for the Concept finder: concepts of the ten modules with their definition, formulas, steps, traps and 'how asked',
the number of bank questions and book exercises that mention each one, mined keywords, and a coverage table.   Run: python3 -I build/concepts_data.py"""
import os, sys, json, re, math, unicodedata, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, 'concepts')); sys.path.insert(0, HERE)
import lib
for i in range(1, 11): __import__(f'm{i:02d}')
import out as _out
from modules import MODS
THIN = 8

def strip(t):
    t = unicodedata.normalize('NFD', t.lower().replace('đ', 'd')); return ''.join(c for c in t if unicodedata.category(c) != 'Mn')
STOP = set('the and for with that this from are was were what which find calculate determine value values given when then than its into over under between each have has will can how does not one two three four five six seven eight nine ten has had they their there these those such also only more most both other same used use using uses must should would could may might very much many any all but how why who whom whose out off yes true false none about above below after before again further once here where while during being been because until against through down per via'.split())
def stem(w): return re.sub(r'(ies|ing|ed|es|s)$', lambda m: 'y' if m.group(0) == 'ies' else '', w) if len(w) > 4 else w
def toks(t): return [stem(w) for w in re.findall(r'[a-z][a-z0-9\-]{2,}', t.lower()) if w not in STOP]
# keywords too common in ordinary text to be evidence for a concept; dropped here so the source lists stay readable (the list is printed by the build)
GENERIC = set('and or not set rs q ia sum mean ramp lead pad mat die peak sin cos sine cosine 90 120 180 ohm ρ √6 vcc r1 r2 error phase width length core primary secondary correspondence sample đảo tổng đặt xoá khắc méo đệm cầu điốt cực bậc đồng hàn thảm pha 90° 29'.split())
def drop_generic(c):
    gone = [k for k in c['kw'] + c['kwv'] if k in GENERIC]; c['kw'] = [k for k in c['kw'] if k not in GENERIC]; c['kwv'] = [k for k in c['kwv'] if k not in GENERIC]; return gone
DROPPED = {c['id']: drop_generic(c) for c in lib.CONCEPTS}
for o in lib.OUT: drop_generic(o)
def kw_re(kws):
    parts = [r'(?<![a-z0-9])' + re.escape(strip(k)) + (r'(?![a-z0-9])' if len(strip(k)) <= 4 else '') for k in kws if len(strip(k)) >= 2]
    return re.compile('|'.join(parts)) if parts else None

banks = {m['id']: json.load(open(os.path.join(ROOT, 'data', 'qbank', m['id'] + '.json'), encoding='utf-8')) for m in MODS}
catalog = json.load(open(os.path.join(ROOT, 'data', 'numeric', 'catalog.json'), encoding='utf-8'))
def item_text(it, lang): return strip(it['q'][lang] + ' ' + it['explain'][lang]) if isinstance(it.get('explain'), dict) else strip(it['q'][lang])
ITEMS = {mid: [(it, item_text(it, 'en'), item_text(it, 'vi')) for it in b['items']] for mid, b in banks.items()}
CAT = collections.defaultdict(list)
for e in catalog:
    for m in e.get('modules') or []: CAT[m].append((e, strip(e.get('text') or e.get('title') or '')))

rows = []; matched_by_mod = collections.defaultdict(set); topic_names = {}
for mid, b in banks.items():
    for it in b['items']: topic_names[(mid, it['topic']['en'])] = it['topic']
for c in lib.CONCEPTS:
    mid = c['mod']; ren, rvi = kw_re(c['kw']), kw_re(c['kwv'])
    direct = [i for i, (it, en, vi) in enumerate(ITEMS[mid]) if (ren and ren.search(en)) or (rvi and rvi.search(vi))]
    in_topic = [i for i, (it, en, vi) in enumerate(ITEMS[mid]) if it['topic']['en'] in c['topics']]
    matched_by_mod[mid].update(direct)
    ex = [(e, t) for e, t in CAT[mid] if ren and ren.search(t)]
    orig = sum(1 for i in direct if ITEMS[mid][i][0].get('origin') == 'goc'); gap = sum(1 for i in direct if 'gap' in (ITEMS[mid][i][0].get('tags') or []))
    rows.append(dict(c=c, direct=direct, in_topic=in_topic, ex=ex, orig=orig, gap=gap))

# ---- mined keywords: stems frequent in the concept's own questions and rare in the other concepts' questions
docs = {}
for r in rows:
    tk = collections.Counter(); 
    for i in set(r['direct']) | set(r['in_topic']):
        for w in set(toks(ITEMS[r['c']['mod']][i][1])): tk[w] += 1
    docs[r['c']['id']] = tk
N = len(rows); dfc = collections.Counter(w for tk in docs.values() for w, n in tk.items() if n >= 2)
own_kw = {r['c']['id']: {stem(x) for k in r['c']['kw'] for x in re.findall(r'[a-z][a-z0-9\-]{2,}', k)} for r in rows}
concepts = []
for r in rows:
    c = r['c']; tk = docs[c['id']]
    cand = sorted(((n * math.log(N / dfc[w]), w) for w, n in tk.items() if n >= 3 and dfc[w] <= 3 and w not in own_kw[c['id']] and not w.isdigit()), reverse=True)[:10]
    concepts.append(dict(id=c['id'], mod=c['mod'], name=c['name'], defn=c['defn'], facts=c['facts'], steps=c['steps'], traps=c['traps'], angles=c['angles'],
                         topics=[topic_names[(c['mod'], t)] for t in c['topics']], kw=c['kw'], kwv=c['kwv'], ak=[w for _, w in cand], src=c['src'], related=c['related'],
                         n=len(r['direct']), n_topic=len(r['in_topic']), n_orig=r['orig'], n_gap=r['gap'],
                         n_ex=len(r['ex']), n_ex_num=sum(1 for e, _ in r['ex'] if e.get('numeric')), checked=bool(c['chk'])))
mods = []
for m in MODS:
    cs = [c for c in concepts if c['mod'] == m['id']]; nb = len(banks[m['id']]['items'])
    mods.append(dict(id=m['id'], vi=m['vi'], en=m['en'], concepts=len(cs), items=nb, matched=len(matched_by_mod[m['id']]), thin=sum(1 for c in cs if c['n'] < THIN),
                     essays=len(banks[m['id']]['essays']), gap=sum(1 for it in banks[m['id']]['items'] if 'gap' in (it.get('tags') or []))))
data = dict(version=1, thin=THIN, modules=mods, concepts=concepts, out=lib.OUT, total_items=sum(x['items'] for x in mods))
os.makedirs(os.path.join(ROOT, 'concepts'), exist_ok=True)
json.dump(data, open(os.path.join(ROOT, 'concepts', 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
if __name__ == '__main__':
    print(f'concepts {len(concepts)} | out-of-scope {len(lib.OUT)} | bank questions {data["total_items"]} | json {os.path.getsize(os.path.join(ROOT, "concepts", "data.json")) // 1024} KB')
    print('module  concepts  items  matched  thin(<%d)' % THIN)
    for m in mods: print(f'{m["id"]}  {m["concepts"]:8d} {m["items"]:6d} {m["matched"]:8d} {m["thin"]:6d}')
    print('thin concepts:')
    for c in sorted(concepts, key=lambda c: c['n']):
        if c['n'] < THIN: print(f'  {c["id"]:26s} direct {c["n"]:3d} topic {c["n_topic"]:3d} orig {c["n_orig"]:2d} ex {c["n_ex"]:3d}')
    print('generic keywords dropped:', sum(len(v) for v in DROPPED.values()))
    print('ak sample:', [(c['id'], c['ak'][:5]) for c in concepts[:4]])
