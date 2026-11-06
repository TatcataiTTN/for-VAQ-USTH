"""Concept finder in vi and en: counts, analysis of English/Vietnamese/off-topic/out-of-scope questions, taught keyword, brief, deep link, links to the bank and the exercise finder, coverage table.
Usage: python3 tests/concepts_test.py [baseURL]  (needs python3 -m http.server 8765 in the project root)"""
import sys, re, json, os
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = json.load(open(os.path.join(ROOT, 'concepts', 'data.json'), encoding='utf-8'))
NC = len(DATA['concepts']); NQ = DATA['total_items']
CASES = [  # (language of the question, text, ids that must appear among the first two results)
    ('en', 'Find the gain of an inverting amplifier with Rf = 220 kΩ and Ri = 10 kΩ; the inverting input is a virtual ground.', ['m02-inverting']),
    ('vi', 'Tính độ lợi của mạch khuếch đại đảo có Rf = 220 kΩ và Ri = 10 kΩ, đất ảo ở ngõ vào đảo.', ['m02-inverting']),
    ('en', 'What R1/R2 and damping factor does a two-pole Sallen-Key Butterworth filter need?', ['m06-sallen-key', 'm06-characteristics']),
    ('en', 'Choose R1, R2 for an astable 555 with f = 4 kHz and 60 % duty cycle.', ['m07-555-astable']),
    ('vi', 'Hunting trong servo là gì và chống bằng cách nào?', ['m10-stability']),
    ('en', 'Design an instrumentation amplifier with a gain of 1000: find RG.', ['m05-instrumentation']),
    ('en', 'An 8-bit ADC has VFS = 5 V. What is the LSB and the quantization error?', ['m05-adc-dac']),
]
bad = []
with sync_playwright() as pw:
    br = pw.chromium.launch(channel='chrome')
    for lang in ('vi', 'en'):
        ctx = br.new_context(viewport={'width': 1200, 'height': 900}); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e, E=errs: E.append(str(e))); pg.on('console', lambda m, E=errs: E.append(m.text) if m.type == 'error' else None)
        pg.goto(f'{BASE}{lang}/concepts/index.html', wait_until='load'); pg.wait_for_selector('#concepts button', timeout=15000)
        # ---- analyse
        for ql, text, want in CASES:
            pg.fill('#concepts [data-pane="0"] textarea', text); pg.click('#concepts [data-pane="0"] .btn >> text=/Tìm khái niệm|Find concepts/'); pg.wait_for_timeout(150)
            ids = pg.evaluate("() => [...document.querySelectorAll('#concepts [data-pane=\"0\"] details.qitem summary b')].map(b => b.textContent.trim())")
            ids = [next((c['id'] for c in DATA['concepts'] if c['name'][lang] == n), n) for n in ids]
            if not any(w in ids[:2] for w in want): bad.append((lang, 'analyse', text[:50], ids[:3], want))
            if not pg.evaluate("() => document.querySelector('#concepts [data-pane=\"0\"] details.qitem').open"): bad.append((lang, 'first result not open'))
        pg.fill('#concepts [data-pane="0"] textarea', 'recipe for chocolate cake with sugar and butter'); pg.click('#concepts [data-pane="0"] .btn >> text=/Tìm khái niệm|Find concepts/'); pg.wait_for_timeout(150)
        if not pg.evaluate("() => !!document.querySelector('#concepts .callout.warn') && !document.querySelector('#concepts [data-pane=\"0\"] details.qitem')"): bad.append((lang, 'off-topic question not flagged'))
        pg.fill('#concepts [data-pane="0"] textarea', 'Explain how a PLL (phase-locked loop) locks onto the frequency of the input signal in a superheterodyne radio.'); pg.click('#concepts [data-pane="0"] .btn >> text=/Tìm khái niệm|Find concepts/'); pg.wait_for_timeout(150)
        warn = pg.evaluate("() => (document.querySelector('#concepts .callout.warn')||{}).textContent || ''")
        if not re.search(r'truyền thông|Communications', warn, re.I): bad.append((lang, 'out-of-scope not named', warn[:80]))
        # ---- taught keyword
        pg.fill('#concepts [data-pane="0"] textarea', 'the zorblax of the circuit'); pg.click('#concepts [data-pane="0"] .btn >> text=/Tìm khái niệm|Find concepts/'); pg.wait_for_timeout(100)
        pg.fill('#concepts [data-pane="0"] .panel input[type=search]', 'zorblax'); pg.select_option('#concepts [data-pane="0"] .panel select', 'm08-series'); pg.click('#concepts [data-pane="0"] .panel .btn')
        pg.wait_for_timeout(200); ids = pg.evaluate("() => [...document.querySelectorAll('#concepts [data-pane=\"0\"] details.qitem summary b')].map(b => b.textContent.trim())")
        ids = [next((c['id'] for c in DATA['concepts'] if c['name'][lang] == n), n) for n in ids]
        if ids[:1] != ['m08-series']: bad.append((lang, 'taught keyword not used', ids[:3]))
        pg.evaluate("() => localStorage.removeItem('prog:customkw')")
        # ---- browse
        pg.click('#concepts .row button >> nth=1'); pg.wait_for_timeout(100)
        n = pg.evaluate("() => document.querySelectorAll('#concepts [data-pane=\"1\"] details.qitem').length")
        if n != NC: bad.append((lang, 'browse count', n, NC))
        pg.select_option('#concepts [data-pane="1"] .bm-bar select >> nth=0', 'm10'); n10 = pg.evaluate("() => document.querySelectorAll('#concepts [data-pane=\"1\"] details.qitem').length")
        if n10 != len([c for c in DATA['concepts'] if c['mod'] == 'm10']): bad.append((lang, 'module filter', n10))
        pg.select_option('#concepts [data-pane="1"] .bm-bar select >> nth=0', 'all'); pg.fill('#concepts [data-pane="1"] .bm-bar input[type=search]', 'hunting'); n2 = pg.evaluate("() => document.querySelectorAll('#concepts [data-pane=\"1\"] details.qitem').length")
        if n2 < 1: bad.append((lang, 'browse search found nothing'))
        pg.fill('#concepts [data-pane="1"] .bm-bar input[type=search]', '')
        pg.evaluate("() => { document.querySelector('#concepts [data-pane=\"1\"] details.qitem').open = true; }")
        pg.check('#concepts [data-pane="1"] details.qitem >> nth=0 >> input[type=checkbox]'); pg.wait_for_timeout(100)
        if not pg.evaluate("() => /\\(1\\)/.test((document.querySelector('#concepts > p:last-child button')||{}).textContent||'')"): bad.append((lang, 'brief button missing'))
        pg.evaluate("() => localStorage.removeItem('prog:conceptbrief')")
        # ---- links of a concept card
        href_bank = pg.evaluate("() => document.querySelector('#c-m05-adc-dac a.btn[href*=\"practice\"]').getAttribute('href')"); href_ex = pg.evaluate("() => document.querySelector('#c-m05-adc-dac a.btn[href*=\"exercises\"]').getAttribute('href')")
        if 'practice/m05.html?topic=' not in href_bank or 'exercises/index.html?mod=m05' not in href_ex: bad.append((lang, 'card links', href_bank, href_ex))
        pg.goto(f'{BASE}{lang}/concepts/' + href_bank.replace('../', '../'), wait_until='load'); pg.wait_for_selector('#bank select', timeout=10000)
        tsel = pg.evaluate("() => [...document.querySelectorAll('#bank select')].map(s => s.options[s.selectedIndex].text)")
        if not any(re.search(r'Converters|Mạch chuyển đổi', t) for t in tsel): bad.append((lang, 'bank topic not preselected', tsel))
        pg.goto(f'{BASE}{lang}/concepts/' + href_ex, wait_until='load'); pg.wait_for_selector('#exfind .qitem', timeout=20000)
        info = pg.inner_text('#exfind .score'); sel_mod = pg.evaluate("() => document.querySelectorAll('#exfind select')[2].value")
        if sel_mod != 'm05': bad.append((lang, 'exercise finder module not preselected', sel_mod))
        # ---- deep link and coverage
        pg.goto(f'{BASE}{lang}/concepts/index.html#m05-adc-dac', wait_until='load'); pg.wait_for_selector('#c-m05-adc-dac', timeout=10000)
        if not pg.evaluate("() => document.getElementById('c-m05-adc-dac').open"): bad.append((lang, 'deep link did not open the concept'))
        pg.click('#concepts .row button >> nth=3'); pg.wait_for_timeout(100)
        cells = pg.evaluate("() => [...document.querySelectorAll('#concepts table')[0].querySelectorAll('tr:last-child th')].map(t => t.textContent)")
        if cells[2] != str(NQ) or cells[4] != '0' or cells[1] != str(NC): bad.append((lang, 'coverage totals', cells, NC, NQ))
        if not pg.evaluate("() => !!document.querySelector('#concepts .callout.good')"): bad.append((lang, 'coverage: thin-concept notice missing'))
        # ---- layout at phone width
        pg.set_viewport_size({'width': 390, 'height': 800}); pg.wait_for_timeout(100)
        if pg.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2"): bad.append((lang, 'horizontal overflow at 390 px'))
        if errs: bad.append((lang, 'console/page errors', errs[:3]))
        print(lang, 'concepts', NC, 'questions', NQ, 'cases', len(CASES))
        ctx.close()
    br.close()
print('FAILS:', bad or 'none'); sys.exit(1 if bad else 0)
