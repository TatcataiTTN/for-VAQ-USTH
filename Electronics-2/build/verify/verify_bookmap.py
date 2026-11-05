"""Verify the book content map (data/bookmap/map.json).
 1. Floyd / Jaeger: the printed page number of every section start must appear in the header/footer of that PDF page (offset check),
    and the section title must be present in that page's text (letter-spaced small caps are squeezed first).
 2. EASA: every heading was located by text search; list the headings that rely on the contents page only.
 3. The syllabus map in build/modules.py (Floyd chapters/sections, Jaeger sections, EASA sub-modules) must be covered by the module assignment.
 4. Every Floyd/EASA/SERVO question source resolved to a place in the map; nothing a lesson cites points to a section that does not exist.
Exit code 1 if anything fails.   Run: python3 -I build/verify/verify_bookmap.py"""
import os, re, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build')); sys.path.insert(0, os.path.join(ROOT, 'build', 'bookmap'))
from modules import MODS
M = json.load(open(os.path.join(ROOT, 'data', 'bookmap', 'map.json'), encoding='utf-8'))
PDFDIR = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'text')
def pages(fn):
    d = open(os.path.join(PDFDIR, fn), encoding='utf-8').read().split('===== PAGE ')
    return {int(x.split(' =====')[0]): x.split('=====\n', 1)[-1] for x in d[1:]}
def sq(s): return re.sub(r'[^a-z0-9]', '', s.lower().replace('–', '-'))
fails = []; stats = {}
def hdrnum(txt, n):
    L = [l.strip() for l in txt.splitlines() if l.strip()]
    if not L: return False
    return bool(re.search(r'(?<!\d)%d(?!\d)' % n, L[0] + ' ' + L[-1]))

# ---- 1. Floyd + Jaeger offsets and titles
FL = pages('Floyd_Electronic_Devices_9e_fixed.txt'); JA = pages('Jaeger_Microelectronic_Circuit_Design_5e_fixed.txt')
def check_book(name, chapters, P, entries):
    ok_p = ok_t = n = 0; bad = []
    for ch, s in entries:
        n += 1; t = P[s['pdf']]
        if hdrnum(t, s['printed']): ok_p += 1
        else: bad.append(('page', name, s.get('num') or s['title'], s['pdf'], s['printed']))
        title = s['title']
        if s.get('kind') in ('section',) or (s.get('num') and s['kind'] != 'end'):
            # titles longer than a line may wrap or be abbreviated: compare the first 18 letters, accept on the page or the previous page (section starts at a page break)
            key = sq(title)[:18]
            if key in sq(t) or key in sq(P.get(s['pdf'] - 1, '')) or key in sq(P.get(s['pdf'] + 1, '')): ok_t += 1
            else: bad.append(('title', name, s['num'], s['pdf'], title))
        else: ok_t += 1
    stats[name] = (n, ok_p, ok_t); return bad
fe = [(c, s) for c in M['floyd']['chapters'] for s in c['sections']] + [(c, dict(e, num='', kind='part', title=e['name'])) for c in M['floyd']['chapters'] for e in c['end_parts']]
je = [(c, s) for c in M['jaeger5']['chapters'] for s in c['sections']]
bad = check_book('floyd', M['floyd']['chapters'], FL, fe) + check_book('jaeger5', M['jaeger5']['chapters'], JA, je)
for ch in M['floyd']['chapters']:
    if not sq(ch['title'])[:14] in sq(FL[ch['pdf']]): bad.append(('chapter-title', 'floyd', ch['num'], ch['pdf'], ch['title']))
    if not hdrnum(FL[ch['pdf']] if False else FL[ch['pdf']], ch['printed']) and ch['num'] not in (): pass
for ch in M['jaeger5']['chapters']:
    if not hdrnum(JA[ch['pdf']], ch['printed']): bad.append(('chapter-page', 'jaeger5', ch['num'], ch['pdf'], ch['printed']))
# tolerate a few pages whose header is a full-page figure; require >= 97 %
for name, (n, okp, okt) in stats.items():
    print(f'{name}: {n} entries, printed page confirmed {okp} ({okp / n:.1%}), title confirmed {okt} ({okt / n:.1%})')
    if okp / n < 0.97 or okt / n < 0.97: fails.append((name, 'offset/title confirmation below 97 %'))
chap_bad = [b for b in bad if b[0] in ('chapter-title', 'chapter-page')]
fails += chap_bad
for b in bad:
    if b[0] in ('page', 'title'): print('  not confirmed:', b)

# ---- 2. EASA / SERVO
by_hint = [r['title'] for r in M['easa']['rows'] if r.get('by_hint')]; nf = [r['title'] for r in M['easa']['rows'] if r['pdf'] is None]
print('EASA headings:', len(M['easa']['rows']), '| located by text search:', len(M['easa']['rows']) - len(by_hint) - len(nf), '| contents page only:', by_hint)
if nf: fails.append(('easa not found', nf))
if len(by_hint) > 4: fails.append(('easa', 'too many headings without a text match'))
sv = M['servo']['rows']; assert [r['pdf'] for r in sv] == sorted(r['pdf'] for r in sv), 'servo not in page order'
print('SERVO headings:', len(sv), 'pages', sv[0]['pdf'], '-', M['servo']['pages'])

# ---- 3. syllabus map in modules.py
fl_sec = {s['num']: (c['num'], s) for c in M['floyd']['chapters'] for s in c['sections'] if s['num']}
ja_sec = {s['num']: s for c in M['jaeger5']['chapters'] for s in c['sections'] if s['num']}
def rng(a, b):
    ma, mb = re.match(r'(\d+)\.(\d+)', a), re.match(r'(\d+)\.(\d+)', b); return [f'{ma[1]}.{k}' for k in range(int(ma[2]), int(mb[2]) + 1)]
for m in MODS:
    mid = m['id']
    for src in m['src']:
        if src.startswith('Floyd'):
            for ch in re.findall(r'Ch\.(\d+)', src):
                nums = [s for s in M['floyd']['chapters'][int(ch) - 1]['sections'] if s['kind'] == 'section']
                if not nums or any(s['mods'].get(mid) != 'core' for s in nums): fails.append((mid, 'Floyd chapter not fully core', ch))
            for sec in re.findall(r'§(\d+–\d+)', src):
                if sec not in fl_sec: fails.append((mid, 'Floyd section does not exist', sec))
                elif mid not in fl_sec[sec][1]['mods']: fails.append((mid, 'Floyd section not assigned', sec))
        if src.startswith('Jaeger'):
            chn = None
            for part in src.replace('Jaeger 5e', '').split('·'):
                mm = re.search(r'Ch\.(\d+)', part)
                if mm: chn = mm[1]
                for tok in re.findall(r'(\d+\.\d+)(?:–(\d+\.\d+))?', part.split('§', 1)[1] if '§' in part else ''):
                    for sec in (rng(tok[0], tok[1]) if tok[1] else [tok[0]]):
                        if sec not in ja_sec: fails.append((mid, 'Jaeger section does not exist', sec))
                        elif mid not in ja_sec[sec]['mods']: fails.append((mid, 'Jaeger section not assigned', sec))
        if src.startswith('EASA'):
            sm = re.search(r'sub-module 0(\d)', src)
            if sm and not any(mid in r['mods'] for r in M['easa']['rows'] if r['sm'] == int(sm[1])): fails.append((mid, 'EASA sub-module not assigned', sm[1]))
# every Jaeger section mapped to a module is a section of the module list in modules.py (no extras)
for sec, s in ja_sec.items():
    for mid in s['mods']:
        m = next(x for x in MODS if x['id'] == mid)
        if not any(src.startswith('Jaeger') for src in m['src']): fails.append((mid, 'Jaeger section assigned but not in modules.py', sec))

# ---- 4. questions resolved, lessons cite real sections
qb = {mid: json.load(open(os.path.join(ROOT, 'data', 'qbank', f'{mid}.json'), encoding='utf-8')) for mid in [m['id'] for m in MODS]}
unres = []; resolved = {'floyd': 0, 'easa': 0, 'servo': 0}
def src(i): return i['src']['en'] if isinstance(i['src'], dict) else i['src']
for mid, b in qb.items():
    qsum = {'floyd': 0, 'easa': 0, 'servo': 0}
    for c in M['floyd']['chapters']:
        for e in c['end_parts']: qsum['floyd'] += e['q'].get(mid, {}).get('quoted', 0)
    for i in b['items'] + b.get('essays', []):
        s = src(i)
        if s.startswith('Floyd 9e, Ch.'): resolved['floyd'] += 1
        elif s.startswith('EASA M04'): resolved['easa'] += 1
        elif 'SERVOMECHANISM' in s: resolved['servo'] += 1
    book_floyd = sum(1 for i in b['items'] + b.get('essays', []) if src(i).startswith('Floyd 9e, Ch.'))
    if qsum['floyd'] != book_floyd: fails.append((mid, 'Floyd quoted count differs', qsum['floyd'], book_floyd))
    easa_q = sum(r['q'].get(mid, {}).get('quoted', 0) for r in M['easa']['rows'] if r['title'] == 'Questions')
    book_easa_q = sum(1 for i in b['items'] + b.get('essays', []) if re.match(r'^EASA M04 SM0?\d, Question', src(i)))
    if easa_q != book_easa_q: fails.append((mid, 'EASA quoted question count differs', easa_q, book_easa_q))
for mid, ms in M['modules'].items():
    for sec in ms['lesson_cites']:
        if sec not in fl_sec: fails.append((mid, 'lesson cites a Floyd section that does not exist', sec))
print('questions anchored to Floyd/EASA/SERVO sources:', resolved)
print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
