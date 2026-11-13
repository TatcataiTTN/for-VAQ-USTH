"""Playwright + Chrome test of the property-lookup page (vi/props, en/props). Starts http.server on port 8794 unless a base URL is given.
Per language: 3 lookups (saturated water 100 C; R-134a 0,8 MPa given s; air given P_r) compared with props.py; the suspect warning for A-17 1040 K v_r;
a range error message; no horizontal overflow at 390 px; no wrong-language strings; no .katex-error; no console errors.
python3 tests/props_test.py [baseURL]   (build first: python3 build/build_site.py)"""
import json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'props'))
import props as L
srv = None
if len(sys.argv) > 1:
    BASE = sys.argv[1]
else:
    PORT = 8794
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    BASE = f'http://127.0.0.1:{PORT}/'; time.sleep(1.0)
VI_CH = re.compile('[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]', re.I)
EN_WORDS = ['Look up', 'Quantity', 'Rows used', 'Show whole table', 'Print errors', 'Substance', 'Cannot look up', 'Lookup type', 'Scope', 'NOT DONE']
VI_WORDS = ['Tra', 'Đại lượng', 'Các hàng đã dùng', 'Xem nguyên bảng', 'Lỗi in', 'Chất', 'Không tra được', 'CHƯA LÀM']
bad = []; nchk = 0
def fail(*a): bad.append(a); print('FAIL', *a)
def parse(s): return float(s.replace('−', '-').replace(' ', '').replace(' ', '').replace(',', '.'))
def ok(cond, *a):
    global nchk; nchk += 1
    if not cond: fail(*a)

def results(pg):
    """-> {quantity-symbol-text: (value-text, class)} from the first result table"""
    rows = pg.evaluate("""() => [...document.querySelectorAll('#p-out table.pres tr')].slice(1).map(tr => [...tr.children].map(td => td.innerText.trim()).concat([tr.children[1].className]))""")
    return rows

def val_of(rows, key_start):
    for r in rows:
        if r[0].startswith(key_start): return r
    raise KeyError(key_start)

try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='chrome')
        for lang in ('vi', 'en'):
            L.set_lang(lang)
            ctx = br.new_context(viewport={'width': 1200, 'height': 900}); pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e, E=errs: E.append(('pageerror', str(e))))
            pg.on('console', lambda m, E=errs: E.append(('console', m.text)) if m.type == 'error' else None)
            pg.goto(f'{BASE}{lang}/props/index.html', wait_until='load'); pg.wait_for_selector('#props-app[data-ready="1"]', timeout=15000)
            # ---- Example 1: water sat 100 C
            pg.click('[data-ex="0"]'); pg.wait_for_selector('#p-out table.pres')
            rows = results(pg)
            for sym, col in (('h', 'hg'), ('P', 'Psat_kPa'), ('s', 'sg'), ('v', 'vg')):
                pass
            exp = {'hg': L.sat_T('water', 100, 'hg')['value'], 'hf': L.sat_T('water', 100, 'hf')['value'], 'Psat_kPa': L.sat_T('water', 100, 'Psat_kPa')['value'], 'sg': L.sat_T('water', 100, 'sg')['value']}
            for r in rows:
                if r[1] == '' or r[1] == '—': continue
            def find(name_frag):
                for r in rows:
                    if name_frag.lower() in r[0].lower(): return r
            for frag, key in (('sat. vapour' if lang == 'en' else 'hơi bão hòa', None),):
                pass
            hg_row = [r for r in rows if r[0].startswith('h') and ('hơi bão hòa' in r[0] or 'sat. vapour' in r[0])][0]
            ok(abs(parse(hg_row[1]) - exp['hg']) < 1e-9, lang, 'water hg', hg_row, exp['hg'])
            ps_row = [r for r in rows if r[0].startswith('P')][0]; ok(abs(parse(ps_row[1]) - exp['Psat_kPa']) < 1e-4, lang, 'water Psat', ps_row)
            txt = pg.inner_text('#p-out')
            ok(('Bảng A-4' in txt or 'Table A-4' in txt) and ('916' in txt), lang, 'source table/page shown')
            ok(pg.locator('#p-out a[data-pageimg]').count() >= 1, lang, 'page image link')
            href = pg.get_attribute('#p-out a[data-pageimg]', 'href'); ok(href.endswith('assets/appendix/p08.jpg') or 'p08.jpg' in href, lang, 'page image href', href)
            if lang == 'vi': ok(',' in hg_row[1] or '.' not in hg_row[1], lang, 'decimal comma', hg_row[1])
            else: ok(',' not in hg_row[1], lang, 'decimal point', hg_row[1])
            # image exists
            ctx_req = ctx.request.get(BASE + 'assets/appendix/p08.jpg'); ok(ctx_req.status == 200, lang, 'p08.jpg served', ctx_req.status)
            # ---- Example 2: R-134a 0.8 MPa given s
            pg.click('[data-ex="1"]'); pg.wait_for_selector('#p-out table.pres')
            rows = results(pg)
            ref = L.superheated_inverse('R134a', 0.8, 's', 0.94456)
            T_row = rows[0]; ok(abs(parse(T_row[1]) - ref['value']) < 5e-6 * max(1, ref['value']), lang, 'R134a T', T_row, ref['value'])
            h_row = [r for r in rows if r[0].startswith('h')][0]; ok(abs(parse(h_row[1]) - ref['extra']['h']) < 1e-4 * 1.1 + 5e-7 * ref['extra']['h'], lang, 'R134a h2', h_row, ref['extra']['h'])
            ok(abs(parse(h_row[1]) - 275.39) < 0.02, lang, 'h2 ~ 275.39 (Tutorials I)', h_row[1])
            # ---- Example 3: air given P_r
            pg.click('[data-ex="2"]'); pg.wait_for_selector('#p-out table.pres')
            rows = results(pg); ref = L.air_inverse('Pr', 11.088)
            ok(abs(parse(rows[0][1]) - ref['value']) < 1e-4, lang, 'air T from Pr', rows[0], ref['value'])
            h_row = [r for r in rows if r[0].startswith('h')][0]; ok(abs(parse(h_row[1]) - ref['extra']['h']) < 2e-4, lang, 'air h', h_row, ref['extra']['h'])
            # ---- suspect: air T = 1040 K  (v_r)
            pg.select_option('#p-sub', 'air'); pg.fill('#pf-val', '1040'); pg.click('#p-go'); pg.wait_for_selector('#p-out table.pres')
            ok(pg.locator('#p-out td.sus').count() >= 1, lang, 'suspect cell flagged at 1040 K')
            ok(('22,39' if lang == 'vi' else '22.39') in pg.inner_text('#p-out'), lang, 'expected value in note')
            # ---- exact row not suspect
            pg.fill('#pf-val', '600'); pg.click('#p-go'); pg.wait_for_selector('#p-out table.pres')
            ok(pg.locator('#p-out td.sus').count() == 0, lang, 'no suspect at 600 K')
            # ---- range error
            pg.fill('#pf-val', '100'); pg.click('#p-go'); pg.wait_for_selector('#p-out .callout.bad')
            ok(pg.locator('#p-out .callout.bad').count() == 1, lang, 'range error shown')
            msg = pg.inner_text('#p-out .callout.bad'); ok(('ngoài phạm vi' in msg) if lang == 'vi' else ('outside the table' in msg), lang, 'range message language', msg[:100])
            # ---- bad input
            pg.fill('#pf-val', 'abc'); pg.click('#p-go'); ok(pg.inner_text('#pe-val') != '', lang, 'input validation message')
            # ---- full table button
            pg.fill('#pf-val', '300'); pg.click('#p-fullbtn'); pg.wait_for_selector('#p-tabwrap table.full')
            ok(pg.locator('#p-tabwrap table.full td.sus').count() >= 3, lang, 'full table marks suspect cells', pg.locator('#p-tabwrap table.full td.sus').count())
            ok(pg.locator('#p-tabwrap table.full tr').count() >= 120, lang, 'full table rows')
            # ---- errata list
            ok(pg.locator('#p-errata tr').count() >= 40, lang, 'errata list rows')
            # ---- language leak
            body = pg.inner_text('#props-app')
            if lang == 'vi':
                for w in EN_WORDS: ok(w not in body, lang, 'EN string leaked into VI', w)
            else:
                ok(not VI_CH.search(body.replace('Cengel', '')), lang, 'Vietnamese characters in EN page', VI_CH.findall(body)[:8])
                for w in VI_WORDS: ok(w not in body, lang, 'VI string leaked into EN', w)
            ok(pg.locator('.katex-error').count() == 0, lang, 'katex-error')
            ok(not errs, lang, 'console/page errors', errs[:3])
            ctx.close()
            # ---- 390 px, no horizontal overflow (also after a lookup and with the full table open)
            ctx = br.new_context(viewport={'width': 390, 'height': 800}); pg = ctx.new_page()
            pg.goto(f'{BASE}{lang}/props/index.html', wait_until='load'); pg.wait_for_selector('#props-app[data-ready="1"]')
            for step in ('initial', 'result', 'table', 'superheated'):
                if step == 'result': pg.click('#p-go'); pg.wait_for_selector('#p-out table.pres')
                if step == 'table': pg.click('#p-fullbtn'); pg.wait_for_selector('#p-tabwrap table.full')
                if step == 'superheated': pg.click('[data-ex="1"]'); pg.wait_for_selector('#p-out table.pres')
                ov = pg.evaluate('() => document.documentElement.scrollWidth - document.documentElement.clientWidth')
                ok(ov <= 0, lang, '390px horizontal overflow', step, ov)
            ctx.close()
        br.close()
finally:
    if srv: srv.terminate()
print(f'{nchk} checks, {len(bad)} failures')
print('FAILS: none' if not bad else f'FAILS: {len(bad)}')
sys.exit(1 if bad else 0)
