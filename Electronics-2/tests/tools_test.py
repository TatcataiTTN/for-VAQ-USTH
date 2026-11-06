"""Exercise finder, Written Practice (study + exam + self-marking + save) and the Your-progress panel, in vi and en.
Usage: python3 tests/tools_test.py [baseURL]  (needs python3 -m http.server 8765 in the project root)"""
import sys, re
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
        # ---- Jaeger problems solved by the site: own class, own label, count 122; the 21 unsolved keep their reason
        pg.goto(f'{BASE}{lang}/exercises/index.html', wait_until='load'); pg.wait_for_selector('#exfind .qitem', timeout=20000)
        pg.select_option('#exfind select >> nth=3', 'solved')
        nsol = pg.evaluate("() => +document.querySelector('#exfind .score').textContent.match(/(\\d[\\d,. ]*)\\s*(?:\\/|of)/)[1].replace(/[^0-9]/g,'')")
        if nsol != 122: bad.append((lang, 'finder: solved class count', nsol))
        lab = pg.evaluate("() => document.querySelector('#exfind details summary').textContent")
        if not re.search(r'site tính|Computed by this site', lab): bad.append((lang, 'finder: computed label', lab))
        pg.select_option('#exfind select >> nth=3', 'ready'); pg.select_option('#exfind select >> nth=0', 'jaeger5'); pg.select_option('#exfind select >> nth=1', 'problem')
        nskip = pg.evaluate("() => document.querySelectorAll('#exfind .srcnote').length")
        if nskip != 21: bad.append((lang, 'finder: no skip reasons shown'))
        # ---- written hub and paper
        pg.goto(f'{BASE}{lang}/written/index.html', wait_until='load'); pg.wait_for_selector('#written-hub .panel', timeout=15000)
        npap = pg.evaluate("() => document.querySelectorAll('#written-hub .panel').length")
        if npap != 12: bad.append((lang, 'written hub papers', npap))
        pg.goto(f'{BASE}{lang}/written/paper.html?p=jaeger-prob-m03', wait_until='load'); pg.wait_for_selector('#written .panel', timeout=15000)
        pg.click('#written .panel >> nth=0 >> button'); box = pg.inner_text('#written .callout.good')
        if not re.search(r'site tính|Computed by this site', box) or not re.search(r'Cách tính|Method', box): bad.append((lang, 'written: computed answer box', box[:120]))
        npr = pg.evaluate("() => document.querySelectorAll('#written .panel').length")
        if npr != 34: bad.append((lang, 'written: jaeger-prob-m03 problems', npr))
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
        # ---- Lab
        pg.goto(f'{BASE}{lang}/lab/index.html', wait_until='load'); pg.wait_for_selector('#lab .panel', timeout=10000)
        txt = lambda sel: pg.inner_text(sel)
        o = txt('#tool-opamp .laboutput'); t5 = txt('#tool-timer555 .laboutput'); fl = txt('#tool-filter .laboutput'); bn = txt('#tool-binary .laboutput'); rg = txt('#tool-regulator .laboutput')
        for what, hay, need in (('opamp gain', o, '-22'), ('opamp vout', o, '1.1'), ('opamp bw', o, '45.45'), ('555 f', t5, '4.031'), ('filter fc', fl, '48.2'), ('binary', bn, '1010111'), ('twos complement', bn, '11011011'), ('bcd', bn, '1000 0111'), ('lm317', rg, '14.25')):
            if need not in hay.replace(',', '.').replace('−', '-'): bad.append((lang, 'lab ' + what, need, hay[:120]))
        pg.fill('#tool-opamp input >> nth=1', '1k'); pg.fill('#tool-opamp input >> nth=1', '10k')
        # ---- Analyser
        pg.goto(f'{BASE}{lang}/analyse/index.html', wait_until='load'); pg.wait_for_selector('#analyser textarea', timeout=20000)
        pg.fill('#analyser textarea', 'An inverting amplifier has Ri = 10 kΩ and Rf = 220 kΩ. What is the voltage gain and the output for a 50 mV input?'); pg.click('#analyser .btn >> nth=0')
        pg.wait_for_selector('#analyser .qitem', timeout=5000); nsim = pg.evaluate("() => document.querySelectorAll('#analyser .qitem').length"); mods = pg.evaluate("() => [...document.querySelectorAll('#analyser a.bm-chip')].map(a => a.textContent)")
        if nsim < 5 or not mods: bad.append((lang, 'analyser matches', nsim, mods))
        pg.fill('#analyser textarea', 'recipe for chocolate cake with sugar and butter'); pg.click('#analyser .btn >> nth=0'); pg.wait_for_timeout(200)
        if not pg.evaluate("() => !!document.querySelector('#analyser .callout.warn')"): bad.append((lang, 'analyser did not flag an off-topic question'))
        pg.fill('#analyser textarea', 'Tính tần số cắt của bộ lọc thông thấp RC với R = 2,2 kΩ và C = 0,0015 μF.'); pg.click('#analyser .btn >> nth=0'); pg.wait_for_timeout(200)
        if pg.evaluate("() => document.querySelectorAll('#analyser .qitem').length") < 3: bad.append((lang, 'analyser: Vietnamese question found too little'))
        if errs: bad.append((lang, 'console/page errors', errs[:3]))
        print(lang, 'finder total', total, 'jaeger numeric+answer', cnt, 'module+search', cnt2, 'papers', npap, 'saved', saved and saved['score'])
        ctx.close()
    br.close()
print('FAILS:', bad or 'none'); sys.exit(1 if bad else 0)
