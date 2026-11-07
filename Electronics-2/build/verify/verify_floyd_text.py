"""Floyd statements: structure checks + (optional, macOS) an independent reading of sampled pages with Apple Vision OCR.
  python3 -I build/verify/verify_floyd_text.py           structure and regression checks
  python3 -I build/verify/verify_floyd_text.py --ocr     also OCR ~60 sampled pages and compare each statement with what the OCR sees
Structure: counts, no gap in the numbering of Problems / Self-Tests / True-False / Circuit-Action, every Example has its Related Problem, every section has Checkup questions,
no untranslated Optr2k glyph (¿ Á ¢ ƒ), no figure label glued to a statement, and the symbols that used to be lost are present."""
import os, sys, json, re, subprocess, random, difflib, collections, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
raw = json.load(open(os.path.join(ROOT, 'data', 'numeric', 'floyd_raw.json'), encoding='utf-8')); M = json.load(open(os.path.join(ROOT, 'data', 'bookmap', 'map.json'), encoding='utf-8'))
bad = []; by = collections.defaultdict(list)
for e in raw: by[e['kind']].append(e)
cnt = {k: len(v) for k, v in by.items()}
for kind, n in (('problem', 843), ('selftest', 356), ('truefalse', 239), ('circuit_action', 154), ('example', 209), ('related_problem', 209)):
    if cnt.get(kind) != n: bad.append(('count', kind, cnt.get(kind), n))
for kind in ('problem', 'selftest', 'truefalse', 'circuit_action'):
    for ch in range(1, 19):
        nums = sorted(int(e['number']) for e in by[kind] if e['chapter'] == ch)
        if nums and nums != list(range(1, nums[-1] + 1)): bad.append(('numbering gap', kind, ch, [x for x in range(1, nums[-1] + 1) if x not in nums]))
ex = {(e['chapter'], e['number']) for e in by['example']}; rp = {(e['chapter'], e['number']) for e in by['related_problem']}
if ex != rp: bad.append(('example/related mismatch', sorted(ex ^ rp)[:5]))
got = collections.defaultdict(collections.Counter)
for e in by['checkup']: got[e['chapter']][e['section']] += 1
for c in M['floyd']['chapters']:
    for s in c['sections']:
        if s['kind'] == 'section' and got[c['num']][s['num']] < 2: bad.append(('checkup section too thin', c['num'], s['num'], got[c['num']][s['num']]))
for e in raw:
    if re.search(r'[¿Á¢ƒ]', e['text']): bad.append(('untranslated glyph', e['chapter'], e['kind'], e['number']))
    if e['kind'] in ('problem', 'selftest', 'truefalse', 'circuit_action', 'example', 'related_problem') and len(e['text']) < 15: bad.append(('too short', e['chapter'], e['kind'], e['number'], e['text']))
def find(ch, kind, num): return next(e for e in raw if e['chapter'] == ch and e['kind'] == kind and e['number'] == num)['text']
REG = [(8, 'problem', '19', ['VGS(off) = −6 V', 'IDSS = 20 mA', '(c) If VGS is increased from −4 V to −1 V']), (5, 'problem', '13', ['If the potentiometer described in Problem 12 is set at 2 kΩ']),
       (15, 'checkup', '15–5.2', ['Q = 5', 'Q = 25']), (12, 'example', '12–8', ['(d) f = 1000 Hz']), (3, 'problem', '38', ['(e) What is the radiant intensity']), (4, 'example', '4–1', ['IC = 3.65 mA'])]
for ch, kind, num, subs in REG:
    t = find(ch, kind, num)
    for sub in subs:
        if sub not in t: bad.append(('regression', ch, kind, num, sub, t[:80]))
dp = os.path.join(ROOT, 'data', 'numeric', 'floyd_dropped.json')              # body lines no statement took: only a handful may sit right after a statement (a figure's dash, one pseudocode word)
if os.path.exists(dp):
    near = [x for x in json.load(open(dp, encoding='utf-8')) if x['gap'] is not None and 0 <= x['gap'] <= 40 and x['x0'] >= x['item_x'] - 2 and x['after']]
    if len(near) > 4 or any(len(x['text']) > 6 for x in near): bad.append(('lines left out right after a statement', [(x['chapter'], x['pdf'], x['text']) for x in near][:6]))
print('counts', cnt)
if '--ocr' in sys.argv:
    exe = os.path.expanduser('~/.claude/skills/build-complete-self-study-system/scripts/vision_ocr')
    import fitz
    doc = fitz.open(os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'Floyd_Electronic_Devices_9e_fixed.pdf')); rng = random.Random(7)
    pages = sorted({e['pdf'] for e in raw if e['kind'] in ('problem', 'selftest', 'truefalse', 'circuit_action', 'example', 'checkup')}); pick = sorted(rng.sample(pages, min(60, len(pages))))
    tmp = tempfile.mkdtemp(prefix='fl_ocr_', dir=os.environ.get('CLAUDE_JOB_DIR', None) and os.path.join(os.environ['CLAUDE_JOB_DIR'], 'tmp'))
    paths = []
    for p in pick:
        fp = os.path.join(tmp, f'p{p}.png'); doc[p - 1].get_pixmap(dpi=220).save(fp); paths.append(fp)
    out = subprocess.run([exe] + paths, capture_output=True, text=True).stdout; txt = {}; cur = None
    for ln in out.split('\n'):
        if ln.startswith('#PAGE'): cur = int(re.search(r'p(\d+)\.png', ln)[1]); txt[cur] = []
        elif cur and '\t' in ln: txt[cur].append(ln.split('\t')[-1])
    norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower().replace('−', '').replace('–', ''))
    scores = []; low = []
    for e in raw:
        if e['pdf'] in txt and e['kind'] in ('problem', 'selftest', 'truefalse', 'circuit_action', 'example', 'related_problem', 'checkup'):
            a = norm(e['text']); b = norm(' '.join(txt[e['pdf']]))
            if len(a) < 12: continue
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False); cov = sum(m.size for m in sm.get_matching_blocks() if m.size >= 4) / len(a)
            scores.append(cov)
            if cov < 0.9: low.append((round(cov, 2), e['chapter'], e['kind'], e['number'], e['pdf'], e['text'][:110]))
    print(f'OCR cross-check: {len(scores)} statements on {len(pick)} sampled pages | mean coverage {sum(scores) / len(scores):.3f} | below 0.90: {len(low)}')
    for l in sorted(low)[:25]: print('  ', l)
    if len(low) > 0.04 * len(scores): bad.append(('OCR agreement too low', len(low), len(scores)))
print('FAILS:', bad if bad else 'none'); sys.exit(1 if bad else 0)
