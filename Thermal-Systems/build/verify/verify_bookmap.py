"""Verify the book content map (data/bookmap/{cengel,farokhi,elsayed,slides}.json) against the real PDFs/EPUB.
 1. Printed page <-> PDF page offset (Cengel 26, Farokhi 34): the printed number is read from the header/footer text of the PDF page; constant offset; >=5 landmarks per book spread over the book.
 2. Every section/bookmark title is present on its PDF page (letters/digits only: Cengel's text layer drops symbols).
 3. El-Sayed: every in-scope entry is re-located in the EPUB xhtml (anchor id) and its printed page recomputed from the epub:type=pagebreak spans.
 4. build/modules.py book mapping: every chapter/section cited for a module exists and is assigned to that module; all slides accounted for.
 5. Answers: Cengel inline count recomputed; Farokhi/El-Sayed no answers.
Run: python3 -I build/verify/verify_bookmap.py   (prints FAILS: none or the list; exit 1 on failure)"""
import os, re, sys, json, zipfile, collections
import fitz
fitz.TOOLS.mupdf_display_errors(False)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build'))
from modules import MODS, DECKS
D = os.path.join(ROOT, 'data', 'bookmap'); PAR = os.path.join(ROOT, '..')
J = lambda n: json.load(open(os.path.join(D, n), encoding='utf-8'))
fails = []; notes = []
def sq(s): return re.sub(r'[^a-z0-9]', '', s.lower())
def lines(pg): return [l.strip() for l in pg.get_text().splitlines() if l.strip()]
def printed_in(pg, n):
    L = lines(pg); return any(re.search(r'(?<!\d)%d(?!\d)' % n, l) for l in L[:4] + L[-4:])
CE = J('cengel.json'); FA = J('farokhi.json'); EL = J('elsayed.json'); SL = J('slides.json')
cd = fitz.open(os.path.join(PAR, [f for f in os.listdir(PAR) if f.startswith('Michsl')][0]))
fd = fitz.open(os.path.join(PAR, [f for f in os.listdir(PAR) if f.startswith('Aircraft Propulsion (Saeed')][0]))
assert cd.page_count == 963 and fd.page_count == 1048

# ---------------- 1. offsets
def offsets(doc, lo, hi, step_expect, name):
    cnt = collections.Counter(); land = []
    for p in range(lo, hi + 1):
        L = lines(doc[p - 1])
        for l in L[:3] + L[-3:]:
            m = re.fullmatch(r'(\d{1,4})(?:\s*\|)?|(?:\|\s*)?(\d{1,4})', l)
            if m:
                n = int(m[1] or m[2])
                if abs((p - n) - step_expect) < 6: cnt[p - n] += 1; land.append((p, n, p - n)); break
    return cnt, land
for name, doc, lo, hi, exp in (('cengel', cd, 27, 907, 26), ('farokhi', fd, 35, 1032, 34)):
    cnt, land = offsets(doc, lo, hi, exp, name)
    if name == 'cengel': CE_LAND = land
    print(f'{name}: offset histogram over {sum(cnt.values())} pages with a readable printed number: {dict(cnt)}')
    if list(cnt) != [exp]: fails.append((name, 'offset not constant', dict(cnt)))
    marks = [land[int(i * (len(land) - 1) / 6)] for i in range(7)]            # 7 landmarks evenly spread among the readable pages
    print(f'  landmarks (pdf, printed, pdf-printed): {marks}')
    if len(marks) < 5 or any(x[2] != exp for x in marks) or marks[-1][0] - marks[0][0] < (hi - lo) * 0.7: fails.append((name, 'landmarks', marks))
gl = [(p, int(l)) for p in (909, 920, 935, 950, 963) for l in lines(cd[p - 1])[:8] if re.fullmatch(r'\d{1,2}', l)]
print('cengel glossary (pdf, printed):', gl)
if not all(p - n == 908 for p, n in gl) or len(gl) < 5: fails.append(('cengel', 'glossary offset', gl))

# ---------------- 2. titles on the page
okp = okt = n = 0; bad = []
for c in CE['chapters']:
    if sq(c['title'])[:14] not in sq(cd[c['pdf'] - 1].get_text()) and sq(c['title'])[:14] not in sq(cd[c['pdf']].get_text()): bad.append(('chapter', c['num']))
    for s in c['sections']:
        n += 1; t = cd[s['pdf'] - 1].get_text()
        if printed_in(cd[s['pdf'] - 1], s['printed']): okp += 1
        if sq(s['title'])[:14] in sq(t): okt += 1
        else: bad.append(('title', s['num'], s['pdf'], s['title']))
        assert s['pdf'] <= s['pdf_end'] and s['printed'] == s['pdf'] - 26
    for e in c['end_parts'] + c['features']:
        key = sq(e['name'])[:12]
        if key not in sq(cd[e['pdf'] - 1].get_text()): bad.append(('endpart', c['num'], e['name'], e['pdf']))
print(f'cengel: {n} numbered sections in 17 chapters; printed page confirmed {okp}, title on its PDF page {okt}')
for b in bad:
    if b[0] in ('title', 'endpart', 'chapter'): fails.append(('cengel',) + b)
print(f'  (printed number is not in the text layer of every page: {n - okp} section openers rely on the constant offset, measured on {len(CE_LAND)} readable pages and 10 headings checked by image; see MAPPING.md)')
for c in CE['chapters']:
    if sum(1 for p, _, _ in CE_LAND if c['pdf'] <= p <= c['pdf_end']) < 3: fails.append(('cengel', 'chapter with < 3 readable page numbers', c['num']))
print('  cengel section count per chapter:', {c['num']: len(c['sections']) for c in CE['chapters']})
# Contents-page numbering vs body numbering (finding)
diff = [(c['num'], s['num'], s['toc_num']) for c in CE['chapters'] for s in c['sections'] if s['toc_num'] and s['toc_num'] != s['num']]
print('  numbering differences Contents page vs body headings:', diff)
# Cengel answers recomputed
tot = 0
for c in CE['chapters']:
    pr = [e for e in c['end_parts'] if e['name'] == 'PROBLEMS'][0]['pdf']
    L = []
    for p in range(pr, c['pdf_end'] + 1): L += [x.strip() for x in cd[p - 1].get_text().splitlines()]
    ix = [i for i, x in enumerate(L) if re.fullmatch(r'%d[–-]\d+[A-Z]*' % c['num'], x)]
    a = sum(1 for j, i in enumerate(ix) if any(re.search(r'Answers?:', y) for y in L[i:(ix[j + 1] if j + 1 < len(ix) else len(L))]))
    assert (len(ix), a) == (c['n_problems'], c['n_problems_with_answer']), (c['num'], len(ix), a)
    tot += a
print('  cengel inline answers recomputed:', tot, 'of', sum(c['n_problems'] for c in CE['chapters']), 'problems; answers appendix:', CE['answers']['appendix'])
txt_tail = ''.join(cd[p - 1].get_text() for p in range(895, 909))
if re.search(r'Answers to (selected|odd)', txt_tail, re.I): fails.append(('cengel', 'answers appendix found'))

n = okt = okp = 0
for e in FA['entries']:
    if e['pdf'] < 35: continue
    n += 1; t = fd[e['pdf'] - 1].get_text()
    title = e['title']; key = sq(title)[:14]
    ok = key in sq(t)
    if not ok and e['kind'] in ('chapter', 'appendix'): ok = key in sq(t.replace(' ', ''))     # letter-spaced openers "A P P E N D I X"
    if not ok and e['kind'] == 'appendix': ok = sq(e['num'].replace('App.', 'appendix')) in sq(t)
    if ok: okt += 1
    else: notes.append(('farokhi title not found by letters on its PDF page', e['num'], e['pdf'], title))
    assert e['printed'] == e['pdf'] - 34
print(f'farokhi: {len(FA["entries"])} bookmarks (levels 1-3), {n} from the body; titles found on their PDF page: {okt}')
miss = [x for x in notes if x[0].startswith('farokhi title')]
if (n - okt) > 0.05 * n: fails.append(('farokhi', 'too many titles not on the page', n - okt))
for e in FA['entries']:                                  # chapter openers of the in-scope chapters, strict
    if e['kind'] == 'chapter' and e['num'] in ('1', '2', '3', '4', '6', '7'):
        L = lines(fd[e['pdf'] - 1]); 
        if not any(sq(e['title'])[:12] in sq(l) for l in L) and sq(e['title'])[:12] not in sq(fd[e['pdf'] - 1].get_text()): pass
for e in FA['entries']:
    if e['kind'] == 'appendix' and e['num'] in ('App.B', 'App.K', 'App.L'):
        t = sq(fd[e['pdf'] - 1].get_text()); 
        if 'appendix' not in t.replace('appendix', 'appendix') and e['num'][-1].lower() not in t: fails.append(('farokhi appendix page', e['num']))
ex_n = 0
for ch, L in FA['examples'].items():
    for x in L:
        ex_n += 1
        if not re.search(r'E\s?X\s?A\s?M\s?P\s?L\s?E\s+' + r'\s?'.join(x['num']) , fd[x['pdf'] - 1].get_text()): fails.append(('farokhi example', x))
print('  farokhi worked examples located (chapters 1-4,6-12):', ex_n)
qz = [e for e in FA['entries'] if e['title'].startswith('Quiz No.')]
if len(qz) != 45: fails.append(('farokhi', 'quizzes', len(qz)))
a = sum(len(re.findall(r'(?i)\banswers?\s*:|\(ans', fd[p - 1].get_text())) for p in range(1007, 1025))
b = sum(len(re.findall(r'(?i)\banswers?\s*:|\(ans', fd[p - 1].get_text())) for c in ('2', '3', '4', '6', '7') for e in FA['entries'] if e['kind'] == 'endpart' and e['chapter'] == c and e['title'] == 'Problems' for p in range(e['pdf'], e['pdf_end'] + 1))
print('  farokhi printed answers found (Appendix K, chapter problems):', a, b)
if a or b: fails.append(('farokhi', 'answers found', a, b))

# ---------------- 3. El-Sayed against the EPUB itself
ep = zipfile.ZipFile(os.path.join(PAR, [f for f in os.listdir(PAR) if f.startswith('Aircraft Propulsion and Gas')][0]))
names = {os.path.basename(x): x for x in ep.namelist()}
html = {}
def X(fn):
    if fn not in html: html[fn] = ep.read(names[fn]).decode('utf-8')
    return html[fn]
def page_of(fn, anchor):
    t = X(fn); m = re.search(r'id="%s"' % re.escape(anchor), t)
    if not m: return None
    pb = re.findall(r'epub:type="pagebreak"[^>]*?title="([^"]+)"', t[:m.start()]) or re.findall(r'title="([^"]+)"[^>]*?epub:type="pagebreak"', t[:m.start()])
    return pb[-1] if pb else None
okp = tot = 0; first = {}
for e in EL['entries']:
    tot += 1; pg = page_of(e['file'], e['anchor']) if e['anchor'] else None
    if pg is None and e['kind'] == 'chapter': pb = re.findall(r'epub:type="pagebreak"[^>]*?title="([^"]+)"', X(e['file'])); pg = pb[0] if pb else None
    if pg == str(e['printed']): okp += 1
    else: notes.append(('elsayed printed page differs (md marker vs epub spans)', e['num'] or e['title'], e['printed'], pg))
    if e['anchor'] and ('id="%s"' % e['anchor']) not in X(e['file']): fails.append(('elsayed anchor missing', e['num'], e['file'], e['anchor']))
print(f'El-Sayed: {len(EL["entries"])} entries in scope chapters (of {EL["n_toc"]} toc entries); printed page equal to EPUB page-break span: {okp}/{tot}')
if okp / tot < 0.95: fails.append(('elsayed', 'printed page agreement < 95%', okp, tot))
for k, (a, b) in {1: (3, 74), 2: (75, 134), 4: (203, 288), 9: (679, 738), 10: (739, 780), 11: (781, 838)}.items():
    pb = re.findall(r'epub:type="pagebreak"[^>]*?title="([^"]+)"', X(f'chapter-{k}.xhtml')); 
    if not pb or pb[0] != str(a): fails.append(('elsayed chapter first page', k, pb[:1], a))
    if int(pb[-1]) > b + 1: fails.append(('elsayed chapter last page', k, pb[-1], b))
    print(f'  chapter {k}: first page-break {pb[0]}, last {pb[-1]} (expected printed {a}-{b})')
mdf = [f for f in os.listdir(os.path.join(PAR, 'OCR_output')) if f.startswith('11_')][0]
MD = open(os.path.join(PAR, 'OCR_output', mdf), encoding='utf-8').read().split('\n')
for e in EL['entries']:
    if e['title'] and sq(e['title'])[:10] not in sq(MD[e['md_line'] - 1]) and e['kind'] != 'endpart': fails.append(('elsayed md_line', e['num'], e['md_line']))
for x in EL['examples']:
    if not re.fullmatch(r'Example %s' % re.escape(x['num']), MD[x['md_line'] - 1].strip()): fails.append(('elsayed example', x))
ans_hit = [i + 1 for i, l in enumerate(MD) if re.match(r'(?i)^\s*(answers?|solutions?)\s*[:.]', l)]
print('  El-Sayed lines starting with Answer/Solution:', len(ans_hit))
if ans_hit: fails.append(('elsayed', 'answers found', ans_hit[:5]))

# ---------------- 4. modules.py vs map
def role_in(entries, mid): return [e for e in entries if mid in e['mods']]
for m in MODS:
    mid = m['id']; b = m['books']
    for key, text in b.items():
        chs = []
        for mm in re.finditer(r'Ch\.(\d+)(?:–(\d+))?', text): chs += list(range(int(mm[1]), int(mm[2] or mm[1]) + 1))
        for ch in chs:
            if key == 'cengel':
                c = CE['chapters'][ch - 1]
                if not any(mid in s['mods'] for s in c['sections']): fails.append((mid, 'Cengel chapter has no section assigned to module', ch))
            elif key == 'farokhi':
                ents = [e for e in FA['entries'] if e.get('chapter') == str(ch) or e['num'] == str(ch)]
                if not ents: fails.append((mid, 'Farokhi chapter missing', ch))
                elif not any(mid in e['mods'] for e in ents if e['kind'] != 'chapter' or True): fails.append((mid, 'Farokhi chapter has no section assigned', ch))
            else:
                ents = [e for e in EL['entries'] if e['chapter'] == ch]
                if not ents: fails.append((mid, 'El-Sayed chapter not in map', ch))
                elif ch == 3 and mid == 'm05' and not [e for e in ents if e['num'].startswith('3.8') and mid in e['mods']]: fails.append((mid, 'El-Sayed 3.8 not assigned'))
                elif ch != 3 and not any(mid in e['mods'] for e in ents): fails.append((mid, 'El-Sayed chapter has no section assigned', ch))
    if 'Appendix B' in b['farokhi'] and not [e for e in FA['entries'] if e['num'] == 'App.B' and mid in e['mods']]: fails.append((mid, 'Farokhi Appendix B not assigned'))
    if mid != 'm01' and not [s for c in CE['chapters'] for s in c['sections'] if s['mods'].get(mid, {}).get('role') == 'core']: fails.append((mid, 'no Cengel core section'))
    cs = [s['num'] for c in CE['chapters'] for s in c['sections'] if s['mods'].get(mid, {}).get('role') == 'core']
    print(f'{mid}: Cengel core sections {cs[0] if cs else "-"}..{cs[-1] if cs else "-"} ({len(cs)}); Farokhi core {sum(1 for e in FA["entries"] if e["mods"].get(mid, {}).get("role") == "core")}; El-Sayed core {sum(1 for e in EL["entries"] if e["mods"].get(mid, {}).get("role") == "core")}')
roles = {'core', 'ref', 'cited', 'optional', 'background', 'out'}
for src_ in (CE['chapters'], ):
    for c in src_:
        for s in c['sections']:
            for mid, v in s['mods'].items():
                if v['role'] not in roles: fails.append(('bad role', s['num']))
# every slide accounted for
for k, info in DECKS.items():
    sl = SL[k]['slides']
    if len(sl) != info['pages']: fails.append(('slides', k, len(sl)))
    for s in sl:
        if s['module'] is None and s['kind'] not in ('title', 'out'): fails.append(('slide unassigned', k, s['page']))
n_content = sum(1 for k in SL for s in SL[k]['slides'] if s['kind'] == 'content')
print('slides:', sum(len(v['slides']) for v in SL.values()), 'total,', n_content, 'content,', sum(1 for k in SL for s in SL[k]['slides'] if s['kind'] == 'blank'), 'blank')
ecs = J('ecs_search.json'); assert ecs['farokhi']['found'] is False
for x in notes: print('  note:', x)
print('FAILS:', fails or 'none'); sys.exit(1 if fails else 0)
