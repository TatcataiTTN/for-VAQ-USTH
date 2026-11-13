"""Playwright test of the Lab page (vi/lab and en/lab) on the local build.
Starts its own `python3 -m http.server` in the project root (port 8793) unless a base URL is given.
Usage: python3 tests/lab_test.py [baseURL]      (build first: .venv/bin/python -I build/verify/verify_lab.py && python3 build/build_site.py)
Checks, per language: every worked example is loaded and the DISPLAYED results are compared with the reference values (tolerance + display rounding);
reference panel marks are all ticks; decimal comma in VI / point in EN; steps and KaTeX rendered; no .katex-error; no console error;
no horizontal overflow at 390 px; no wrong-language strings; input validation messages; no loading="lazy" on the page."""
import json, math, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXP = json.load(open(os.path.join(ROOT, 'data', 'lab_expected.json'), encoding='utf-8'))
srv = None
if len(sys.argv) > 1:
    BASE = sys.argv[1]
else:
    PORT = 8793
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    BASE = f'http://127.0.0.1:{PORT}/'
    time.sleep(1.0)

VI_CH = re.compile('[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]', re.I)
EN_WORDS = ['Calculate', 'Quantity', 'Reference values', 'Deviation', 'Tolerance', 'Required', 'Load worked example', 'Calculation steps', 'Invalid input', 'Cannot compute', 'Compression ratio', 'Heat input', 'Choked flow', 'NOT DONE', 'Scope and assumptions', 'optional']
bad, nchk, maxdev = [], 0, (0.0, '')


def parse(s):
    s = s.replace('−', '-').replace(' ', '').replace(' ', '')
    return float(s.replace(',', '.'))


def half_ulp(v):                                           # half a unit of the 5th significant digit shown by the page (6th for the reference column)
    return 0.5 * 10 ** (math.floor(math.log10(abs(v))) - 4) if v else 0.0


def fail(*a): bad.append(a)


try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='chrome')
        for lang in ('vi', 'en'):
            ctx = br.new_context(viewport={'width': 1200, 'height': 900}); pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e, E=errs: E.append(('pageerror', str(e))))
            pg.on('console', lambda m, E=errs: E.append(('console', m.text)) if m.type == 'error' else None)
            url = f'{BASE}{lang}/lab/index.html'
            pg.goto(url, wait_until='load'); pg.wait_for_selector('.labcard [data-k]', timeout=15000) if False else pg.wait_for_selector('.labcard .labform', timeout=15000)
            html = pg.content()
            if 'loading="lazy"' in html: fail(lang, 'loading=lazy present on the Lab page')
            # ---- calculators present, NOT DONE card present
            calcs = pg.evaluate("() => [...document.querySelectorAll('[data-calc]')].map(e => e.dataset.calc)")
            for need in ('otto', 'diesel', 'brayton', 'flow_ma', 'flow_aas', 'flow_pr', 'flow_stag', 'flow_crit', 'flow_noz', 'comb'):
                if need not in calcs: fail(lang, 'calculator missing', need)
            for need in ('R-134a', 'P3'):
                if need not in pg.inner_text('#lab-todo'): fail(lang, 'NOT DONE card lacks', need)
            if not re.search('CHƯA LÀM|NOT DONE', pg.inner_text('#lab-todo')): fail(lang, 'NOT DONE card has no explicit label')
            # ---- worked examples
            for ex in EXP['examples']:
                card = pg.locator(f'[data-calc="{ex["calc"]}"]')
                titles = [x for x in EXP['examples'] if x['calc'] == ex['calc']]
                if len(titles) > 1: card.locator('select.exsel').select_option(index=titles.index(ex))
                card.locator('button.ex').click()
                try: card.locator('.refs').wait_for(timeout=5000)
                except Exception: fail(lang, ex['id'], 'no reference panel'); continue
                if card.locator('.callout.bad').count(): fail(lang, ex['id'], 'error box shown', card.locator('.callout.bad').inner_text())
                if card.locator('details.steps .step').count() < 3: fail(lang, ex['id'], 'too few steps')
                if card.locator('details.steps .step .katex').count() < 3: fail(lang, ex['id'], 'KaTeX formulas not rendered in the steps')
                for r in ex['refs']:
                    nchk += 1
                    cell = card.locator(f'table.labres tr[data-k="{r["key"]}"] td.v')
                    if cell.count() != 1: fail(lang, ex['id'], r['key'], 'result row missing'); continue
                    shown = cell.inner_text(); val = parse(shown)
                    if lang == 'vi' and re.search(r'\d\.\d', shown): fail(lang, ex['id'], r['key'], 'decimal point in VI', shown)
                    if lang == 'en' and re.search(r'\d,\d', shown): fail(lang, ex['id'], r['key'], 'decimal comma in EN', shown)
                    dev = abs(val - r['v']); tol = r['tol'] + half_ulp(r['v'])
                    if dev > tol: fail(lang, ex['id'], r['key'], 'displayed', shown, 'reference', r['v'], 'dev', dev, 'tol', tol)
                    if r['tol'] > 0 and dev / r['tol'] > maxdev[0]: maxdev = (dev / r['tol'], f'{lang}/{ex["id"]}/{r["key"]}')
                    row = card.locator(f'tr.refrow[data-key="{r["key"]}"]')
                    if row.count() != 1: fail(lang, ex['id'], r['key'], 'reference row missing'); continue
                    if 'ok' not in (row.get_attribute('class') or ''): fail(lang, ex['id'], r['key'], 'reference row not ok')
                    rv = parse(row.locator('td.rv').inner_text())
                    if abs(rv - r['v']) > 1e-5 * max(abs(r['v']), 1e-3) + 1e-9: fail(lang, ex['id'], r['key'], 'reference shown differs', rv, r['v'])
                src = card.locator('.refsrc').inner_text()
                if not src.strip(): fail(lang, ex['id'], 'no source line')
            pg.wait_for_timeout(400)
            if pg.locator('.katex-error').count(): fail(lang, 'katex-error', pg.locator('.katex-error').count())
            # ---- input handling: comma and point give the same result; errors are explicit
            otto = pg.locator('[data-calc="otto"]')
            def run_otto(rv):
                otto.locator('input[data-k="r"]').fill(rv); otto.locator('input[data-k="T1"]').fill('300'); otto.locator('input[data-k="P1"]').fill('100'); otto.locator('input[data-k="qin"]').fill('1000')
                otto.locator('button.labbtn').first.click(); c = otto.locator('tr[data-k="eta"] td.v'); return c.inner_text() if c.count() else None
            a = run_otto('8,5'); b = run_otto('8.5')
            if a is None or a != b: fail(lang, 'comma/point differ', a, b)
            run_otto('abc')
            if not otto.locator('.lferr').first.inner_text().strip(): fail(lang, 'no error message for text input')
            if otto.locator('table.labres').count(): fail(lang, 'result shown for invalid input')
            run_otto('0.5')
            if not otto.locator('.lferr').first.inner_text().strip(): fail(lang, 'no message for r <= 1')
            otto.locator('input[data-k="r"]').fill('8'); otto.locator('input[data-k="qin"]').fill('')
            otto.locator('button.labbtn').first.click()
            if not otto.locator('.lferr').nth(5).inner_text().strip() and not any(e.inner_text().strip() for e in otto.locator('.lferr').all()): fail(lang, 'no message for missing q_in')
            otto.locator('input[data-k="mode"]').count()
            otto.locator('select[data-k="mode"]').select_option('T3'); otto.locator('input[data-k="T3"]').fill('400'); otto.locator('button.labbtn').first.click()
            if not otto.locator('.callout.bad').count(): fail(lang, 'T3 below T2 gave no error box')
            # ---- language leaks inside the Lab (main, KaTeX removed)
            txt = pg.evaluate("() => { const m = document.querySelector('main').cloneNode(true); m.querySelectorAll('.katex, script, style').forEach(e => e.remove()); return m.innerText; }")
            if lang == 'en':
                m = VI_CH.findall(txt)
                if m: fail(lang, 'Vietnamese characters on the EN page', ''.join(sorted(set(m)))[:40], re.findall(r'.{0,25}' + VI_CH.pattern + r'.{0,25}', txt)[:3])
            else:
                for w in EN_WORDS:
                    if re.search(r'\b' + re.escape(w) + r'\b', txt): fail(lang, 'English string on the VI page', w)
            if errs: fail(lang, 'console/page errors', errs[:5])
            # ---- 390 px: no horizontal overflow (with the widest results shown)
            m = br.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=2); mp = m.new_page(); merrs = []
            mp.on('console', lambda x, E=merrs: E.append(x.text) if x.type == 'error' else None)
            mp.goto(url, wait_until='load'); mp.wait_for_selector('.labcard .labform')
            for ex in EXP['examples']:
                c = mp.locator(f'[data-calc="{ex["calc"]}"]'); same = [x for x in EXP['examples'] if x['calc'] == ex['calc']]
                if len(same) > 1: c.locator('select.exsel').select_option(index=same.index(ex))
                c.locator('button.ex').click()
            mp.wait_for_timeout(500)
            sw = mp.evaluate("() => [document.documentElement.scrollWidth, document.body.scrollWidth, window.innerWidth]")
            if sw[0] > 391 or sw[1] > 391: fail(lang, 'horizontal overflow at 390 px', sw)
            wide = mp.evaluate("() => [...document.querySelectorAll('#lab *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > 392 && !e.closest('.tw') && !e.closest('.sb') && !e.closest('.katex-display') && !e.closest('.sf'); }).map(e => e.tagName + '.' + e.className).slice(0, 5)")
            if wide: fail(lang, 'elements wider than the viewport outside scroll boxes', wide)
            mp.screenshot(path=os.path.join(ROOT, 'scratch', 'lab', f'lab_{lang}_390.png'), full_page=False)
            if merrs: fail(lang, 'console errors at 390 px', merrs[:3])
            m.close(); ctx.close()
        br.close()
finally:
    if srv: srv.terminate()

print(f'reference comparisons on the displayed results: {nchk}; largest deviation as a fraction of its tolerance: {maxdev[0]:.3f} at {maxdev[1]}')
if bad:
    for b in bad[:40]: print('FAIL', *b)
    print(f'FAILS: {len(bad)}'); sys.exit(1)
print('FAILS: none')
