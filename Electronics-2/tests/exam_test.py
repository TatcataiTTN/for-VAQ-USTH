"""Mock exams in vi and en: hub, forward-only Midterm (no way back, scoring, mark out of 10, by-module bars, saved result, review, redo of the mistakes),
free-navigation Final (palette, flags, jump), Speed (random draw differs between runs), Custom (chosen modules only), reload resume, automatic submit when time is up,
A4 print view, and the Your-progress panel on the home page.
Usage: python3 tests/exam_test.py [baseURL]  (needs python3 -m http.server 8765 in the project root)"""
import sys, re, json, os
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
bad = []
def data(lang): return json.load(open(os.path.join(ROOT, lang, 'exam', 'data.json'), encoding='utf-8'))
with sync_playwright() as pw:
    br = pw.chromium.launch(channel='chrome')
    for lang in ('vi', 'en'):
        D = data(lang); BY = {q['id']: q for q in D['pool']}; P = {p['id']: p for p in D['papers'] + D['mixed']}
        ctx = br.new_context(viewport={'width': 1200, 'height': 900}); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e, E=errs: E.append(str(e))); pg.on('console', lambda m, E=errs: E.append(m.text) if m.type == 'error' else None)
        pg.on('dialog', lambda d: d.accept())
        # ---- hub
        pg.goto(f'{BASE}{lang}/exam/index.html', wait_until='load'); pg.wait_for_selector('#exam .panel', timeout=15000)
        n_cards = pg.evaluate("() => document.querySelectorAll('#exam .panel').length")
        if n_cards != 3 + 1 + 3 + 1 + 1 + 6 + 1: bad.append((lang, 'hub cards', n_cards))
        if len(pg.query_selector_all('#exam .callout')) < 1: bad.append((lang, 'hub: assumption note missing'))
        for pid in ('midterm-A', 'midterm-B', 'midterm-C', 'final-A', 'final-B', 'final-C'):
            if not pg.query_selector(f'#exam a[href="run.html?exam={pid}"]') or not pg.query_selector(f'#exam a[href="print.html?exam={pid}"]'): bad.append((lang, 'hub link missing', pid))
        # ---- structure of the fixed papers (data)
        for t, n, mins, fwd in (('midterm', 30, 40, True), ('final', 50, 60, False)):
            sets = [P[f'{t}-{c}'] for c in 'ABC']
            if any(len(p['ids']) != n or p['minutes'] != mins or p['forward'] != fwd for p in sets): bad.append((lang, 'paper definition', t))
            allids = [i for p in sets for i in p['ids']]
            if len(set(allids)) != len(allids): bad.append((lang, 'papers of one type overlap', t))
        if any(BY[i]['m'] not in ('m01', 'm02', 'm03', 'm04', 'm05') for i in P['midterm-A']['ids']): bad.append((lang, 'midterm outside modules 01-05'))
        # ---- Midterm A: forward-only
        pid = 'midterm-A'; paper = P[pid]; n = len(paper['ids'])
        pg.goto(f'{BASE}{lang}/exam/run.html?exam={pid}', wait_until='load'); pg.wait_for_selector('#exam .panel .btn', timeout=15000)
        intro = pg.inner_text('#exam .panel')
        if not re.search(r'30', intro) or not re.search(r'40', intro) or not re.search(r'KHÔNG|NO going back', intro): bad.append((lang, 'intro text', intro[:100]))
        pg.click('#exam .panel .btn'); pg.wait_for_selector('#exam .qitem .opt', timeout=5000)
        if pg.evaluate("() => document.querySelectorAll('#exam .row button').length") > 3 and pg.evaluate("() => /^1/.test((document.querySelectorAll('#exam > .row button')[0]||{}).textContent||'')"): bad.append((lang, 'forward-only shows a palette'))
        if re.search(r'Câu trước|Previous', pg.inner_text('#exam .qitem')): bad.append((lang, 'forward-only: a Previous button is offered'))
        plan = []                                                         # correct for q1..q10, wrong for q11..q15, blank for the rest
        for i in range(n):
            q = BY[paper['ids'][i]]
            if i < 10: choose = q['c']
            elif i < 15: choose = (q['c'] + 1) % len(q['o'])
            else: choose = None
            plan.append(choose)
            if choose is not None: pg.keyboard.press('abcdef'[choose])
            if i == 0:
                pg.keyboard.press('ArrowRight'); pg.keyboard.press('ArrowLeft')           # going back must be impossible
                if 'Câu 2' not in pg.inner_text('#exam .exambar') and 'Question 2' not in pg.inner_text('#exam .exambar'): bad.append((lang, 'forward-only: ArrowRight/ArrowLeft', pg.inner_text('#exam .exambar')))
                continue
            if i < n - 1: pg.keyboard.press('ArrowRight')
        # reload resumes the run
        pg.reload(wait_until='load'); pg.wait_for_selector('#exam .qitem .opt', timeout=5000)
        got_idx = pg.inner_text('#exam .exambar')
        if not re.search(r'30 / 30|30 / 30', got_idx) and f'{n} / {n}' not in got_idx: bad.append((lang, 'reload did not resume at the last question', got_idx))
        pg.keyboard.press('ArrowRight')                                    # on the last question: asks to submit (dialog accepted)
        pg.wait_for_selector('#exam .stats', timeout=5000)
        exp = sum(1 for i, c in enumerate(plan) if c is not None and c == BY[paper['ids'][i]]['c'])
        stats = pg.inner_text('#exam .stats')
        if f'{exp} / {n}' not in stats: bad.append((lang, 'midterm score', exp, stats))
        if (str(round(10 * exp / n, 1)).replace('.', ',') if lang == 'vi' else str(round(10 * exp / n, 1))) not in stats: bad.append((lang, 'mark /10', stats))
        saved = pg.evaluate("() => JSON.parse(localStorage.getItem('prog:exam:midterm-A'))")
        if not saved or saved['score'] != exp or saved['n'] != n or not saved['byMod']: bad.append((lang, 'saved result', saved))
        if sum(v[1] for v in saved['byMod'].values()) != n or sum(v[0] for v in saved['byMod'].values()) != exp: bad.append((lang, 'byMod totals', saved['byMod']))
        shown = pg.evaluate("() => document.querySelectorAll('#exam .qitem').length")
        if shown != n - exp: bad.append((lang, 'review shows wrong+blank only', shown, n - exp))
        pg.evaluate("() => { const c = document.querySelector('#exam input[type=checkbox]'); c.click(); }"); pg.wait_for_timeout(100)
        if pg.evaluate("() => document.querySelectorAll('#exam .qitem').length") != n: bad.append((lang, 'review all'))
        # redo mistakes
        pg.click('#exam .row .btn >> nth=0'); pg.wait_for_selector('#exam .qitem .opt', timeout=5000)
        pg.click('#exam .qitem .opt >> nth=0'); pg.wait_for_selector('#exam .explain.show', timeout=3000)
        # ---- Final A: free navigation, palette, flag, jump
        pid = 'final-A'; paper = P[pid]; n = len(paper['ids'])
        pg.goto(f'{BASE}{lang}/exam/run.html?exam={pid}', wait_until='load'); pg.wait_for_selector('#exam .panel .btn'); pg.click('#exam .panel .btn'); pg.wait_for_selector('#exam .qitem .opt')
        pal = pg.evaluate("() => document.querySelectorAll('#exam > .row button').length")
        if pal != n: bad.append((lang, 'final palette size', pal, n))
        pg.keyboard.press('b'); pg.keyboard.press('m'); pg.click('#exam > .row button >> nth=19'); pg.wait_for_timeout(100)
        if not re.search(r'20 / 50', pg.inner_text('#exam .exambar')): bad.append((lang, 'palette jump', pg.inner_text('#exam .exambar')))
        pg.keyboard.press('ArrowLeft'); pg.keyboard.press('ArrowLeft'); pg.click('#exam > .row button >> nth=0'); pg.wait_for_timeout(100)
        lab = pg.evaluate("() => document.querySelectorAll('#exam > .row button')[0].textContent")
        if '⚑' not in lab: bad.append((lang, 'flag not shown on palette', lab))
        if pg.evaluate("() => document.querySelectorAll('#exam .qitem .opt')[1].style.outline === ''"): bad.append((lang, 'answer b not marked after returning'))
        # ---- Speed: random draw, differs between two fresh contexts, 30 questions over several modules
        ids_runs = []
        for k in range(2):
            c2 = br.new_context(viewport={'width': 1200, 'height': 900}); p2 = c2.new_page(); p2.on('dialog', lambda d: d.accept())
            p2.goto(f'{BASE}{lang}/exam/run.html?exam=speed', wait_until='load'); p2.wait_for_selector('#exam .panel .btn'); p2.click('#exam .panel .btn'); p2.wait_for_selector('#exam .qitem')
            st = p2.evaluate("() => JSON.parse(sessionStorage.getItem('examrun:' + location.search))"); ids_runs.append(st['ids']); c2.close()
        if any(len(r) != 30 for r in ids_runs) or ids_runs[0] == ids_runs[1]: bad.append((lang, 'speed draw', [len(r) for r in ids_runs], ids_runs[0] == ids_runs[1]))
        if len({BY[i]['m'] for i in ids_runs[0]}) < 8 or len(set(ids_runs[0])) != 30: bad.append((lang, 'speed modules/unique', len({BY[i]['m'] for i in ids_runs[0]})))
        # ---- Custom: only the chosen modules, forward-only, n
        pg.goto(f'{BASE}{lang}/exam/run.html?exam=custom&mods=m02,m03&n=12&min=5&fwd=1&orig=0', wait_until='load'); pg.wait_for_selector('#exam .panel .btn'); pg.click('#exam .panel .btn'); pg.wait_for_selector('#exam .qitem')
        st = pg.evaluate("() => JSON.parse(sessionStorage.getItem('examrun:' + location.search))")
        if len(st['ids']) != 12 or {BY[i]['m'] for i in st['ids']} - {'m02', 'm03'}: bad.append((lang, 'custom', len(st['ids']), {BY[i]['m'] for i in st['ids']}))
        # ---- time up: the run started long ago is submitted automatically
        pg.evaluate("() => { const k = 'examrun:' + location.search, s = JSON.parse(sessionStorage.getItem(k)); s.t0 = Date.now() - 6 * 60 * 1000; sessionStorage.setItem(k, JSON.stringify(s)); }")
        pg.reload(wait_until='load'); pg.wait_for_selector('#exam .stats', timeout=8000)
        if not re.search(r'Hết giờ|Time is up', pg.inner_text('#exam')): bad.append((lang, 'no time-up notice'))
        # ---- print view
        pg.goto(f'{BASE}{lang}/exam/print.html?exam=midterm-B', wait_until='load'); pg.wait_for_selector('#exam .xq', timeout=8000)
        cnt = pg.evaluate("() => [document.querySelectorAll('#exam .xq').length, document.querySelectorAll('#exam table.t')[0].querySelectorAll('tr').length, document.querySelectorAll('#exam table.t')[1].querySelectorAll('tr').length]")
        if cnt != [30, 31, 31]: bad.append((lang, 'print structure', cnt))
        pdf_ok = pg.pdf(format='A4', print_background=False)
        if len(pdf_ok) < 5000: bad.append((lang, 'print pdf too small'))
        # ---- home progress panel lists the exam
        pg.goto(f'{BASE}{lang}/index.html', wait_until='load'); pg.wait_for_selector('#progress', timeout=8000); pg.wait_for_timeout(300)
        prog = pg.inner_text('#progress')
        if not re.search(r'midterm|Midterm|Giữa kỳ', prog, re.I): bad.append((lang, 'progress panel does not show the midterm', prog[:120]))
        # ---- phone width
        pg.set_viewport_size({'width': 390, 'height': 800}); pg.goto(f'{BASE}{lang}/exam/index.html', wait_until='load'); pg.wait_for_selector('#exam .panel'); pg.wait_for_timeout(100)
        if pg.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2"): bad.append((lang, 'hub overflows at 390 px'))
        if errs: bad.append((lang, 'console/page errors', errs[:3]))
        print(lang, 'ok pool', len(D['pool']), 'papers', len(D['papers']), 'mixed', len(D['mixed']))
        ctx.close()
    br.close()
print('FAILS:', bad or 'none'); sys.exit(1 if bad else 0)
