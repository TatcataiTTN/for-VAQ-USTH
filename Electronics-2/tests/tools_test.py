"""Exercise finder, Written Practice (study + exam + self-marking + save) and the Your-progress panel, in vi and en.
Usage: python3 tests/tools_test.py [baseURL]  (needs python3 -m http.server 8765 in the project root)"""
import sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
bad = []
with sync_playwright() as pw:
    br = pw.chromium.launch(channel='chrome')
    for lang in ('vi', 'en'):
        ctx = br.new_context(viewport={'width': 1200, 'height': 900}); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e, E=errs: E.append(str(e))); pg.on('console', lambda m, E=errs: E.append(m.text) if m.type == 'error' else None)
        # ---- exercise finder
        pg.goto(f'{BASE}{lang}/exercises/index.html', wait_until='load'); pg.wait_for_selector('#exfind .qitem', timeout=20000)
        info = pg.inner_text('#exfind .score'); n_all = int(''.join(c for c in info.split('/')[0] if c.isdigit()) or 0) if False else None
        total = pg.evaluate("() => +document.querySelector('#exfind .score').textContent.match(/(\\d[\\d,. ]*)\\s*(?:\\/|of)\\s*(\\d[\\d,. ]*)/)[2].replace(/[^0-9]/g,'')")
        pg.select_option('#exfind select >> nth=0', 'jaeger5'); c_book = pg.evaluate("() => +document.querySelector('#exfind .score').textContent.match(/(\\d[\\d,. ]*)\\s*(?:\\/|of)/)[1].replace(/[^0-9]/g,'')")
        if c_book != 2983: bad.append((lang, 'finder: select did not re-filter', c_book))
        pg.select_option('#exfind select >> nth=1', 'exercise')
        pg.check('#exfind input[type=checkbox] >> nth=0'); pg.check('#exfind input[type=checkbox] >> nth=1')
        cnt = pg.evaluate("() => +document.querySelector('#exfind .score').textContent.match(/(\\d[\\d,. ]*)\\s*(?:\\/|of)/)[1].replace(/[^0-9]/g,'')")
        if not (200 < cnt < 650): bad.append((lang, 'finder: jaeger numeric exercises with answer', cnt))
        if total != 4858: bad.append((lang, 'finder total', total))
        if not pg.evaluate("() => !!document.querySelector('#exfind details')"): bad.append((lang, 'finder: no printed answer shown'))
        pg.select_option('#exfind select >> nth=2', 'm02'); pg.fill('#exfind input[type=search]', 'op amp')
        cnt2 = pg.evaluate("() => +document.querySelector('#exfind .score').textContent.match(/(\\d[\\d,. ]*)\\s*(?:\\/|of)/)[1].replace(/[^0-9]/g,'')")
        if cnt2 < 1: bad.append((lang, 'finder: module+search found nothing', cnt2))
        # ---- written hub and paper
        pg.goto(f'{BASE}{lang}/written/index.html', wait_until='load'); pg.wait_for_selector('#written-hub .panel', timeout=15000)
        npap = pg.evaluate("() => document.querySelectorAll('#written-hub .panel').length")
        if npap != 7: bad.append((lang, 'written hub papers', npap))
        pg.goto(f'{BASE}{lang}/written/paper.html?p=jaeger-m01', wait_until='load'); pg.wait_for_selector('#written .panel', timeout=15000)
        pg.click('#written .panel >> nth=0 >> button'); shown = pg.evaluate("() => !document.querySelector('#written .callout.good').classList.contains('hide')")
        if not shown: bad.append((lang, 'study: answer not shown'))
        pg.goto(f'{BASE}{lang}/written/paper.html?p=jaeger-m01&mode=exam', wait_until='load'); pg.wait_for_selector('#written .btn', timeout=15000)
        pg.click('#written .panel >> button'); pg.wait_for_selector('#written .exambar', timeout=5000)
        pg.once('dialog', lambda d: d.accept()); pg.click('#written .exambar button'); pg.wait_for_selector('#written .bigscore', timeout=5000)
        pg.select_option('#written select >> nth=0', '1'); pg.select_option('#written select >> nth=1', '0.5')
        sc = pg.inner_text('#written .bigscore')
        pg.click('#written .panel >> button >> text=/Lưu|Save/'); saved = pg.evaluate("() => JSON.parse(localStorage.getItem('prog:written:jaeger-m01'))")
        if not saved or saved['score'] != 1.5: bad.append((lang, 'written: saved score', saved, sc))
        # ---- practice bank + progress panel on the home page
        pg.goto(f'{BASE}{lang}/practice/m02.html', wait_until='load'); pg.wait_for_selector('#bank .opt', timeout=15000); pg.click('#bank .opt >> nth=0')
        pg.goto(f'{BASE}{lang}/index.html', wait_until='load'); pg.wait_for_selector('#progress .stats', timeout=10000)
        stats = pg.inner_text('#progress'); 
        if '1' not in stats or ('M02' not in stats): bad.append((lang, 'progress panel content', stats[:120]))
        if not pg.evaluate("() => !!document.querySelector('#progress table')"): bad.append((lang, 'progress: no recent results table'))
        if errs: bad.append((lang, 'console/page errors', errs[:3]))
        print(lang, 'finder total', total, 'jaeger numeric+answer', cnt, 'module+search', cnt2, 'papers', npap, 'saved', saved and saved['score'])
        ctx.close()
    br.close()
print('FAILS:', bad or 'none'); sys.exit(1 if bad else 0)
