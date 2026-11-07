"""Browser test (Playwright, system Chrome): every page in vi/ and en/ -> HTTP errors, console errors, broken images, deck slides,
quiz click -> explanation, bank page, exam. Usage: python3 tests/site_test.py [baseURL]  (needs: python3 -m http.server 8765 in the project root)"""
import sys, os, glob
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')); BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
pages = sorted(os.path.relpath(p, ROOT) for l in ('vi', 'en') for p in glob.glob(f'{ROOT}/{l}/**/*.html', recursive=True))
fails = 0
with sync_playwright() as pw:
    br = pw.chromium.launch(channel='chrome'); ctx = br.new_context(viewport={'width': 1280, 'height': 900}); os.makedirs(f'{ROOT}/tests/shots', exist_ok=True)
    for rel in pages:
        pg = ctx.new_page(); errs = []
        pg.on('console', lambda m, e=errs: e.append('console: ' + m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda x, e=errs: e.append('pageerror: ' + str(x)))
        pg.on('response', lambda r, e=errs: e.append(f'{r.status} {r.url}') if r.status >= 400 else None)
        pg.goto(BASE + rel, wait_until='load')
        info = pg.evaluate("() => ({slides: document.querySelectorAll('.mdeck-slide').length, quiz: document.querySelectorAll('.quiz .qitem').length, bank: document.querySelectorAll('#bank .qitem').length, exam: document.querySelectorAll('#exam .qitem, #exam .panel, #exam .xq').length})")
        pg.evaluate("async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } }"); pg.wait_for_timeout(300)
        broken = pg.evaluate("() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src)")
        if info['quiz']:
            pg.evaluate("() => document.querySelector('.quiz .qitem .opt').click()")
            if not pg.evaluate("() => !!document.querySelector('.quiz .qitem .explain.show')"): errs.append('quiz explanation not shown')
        if info['bank']:
            pg.evaluate("() => document.querySelector('#bank .qitem .opt').click()")
            if not pg.evaluate("() => !!document.querySelector('#bank .qitem .explain.show')"): errs.append('bank explanation not shown')
        if '/modules/' in rel and info['slides'] < 15: errs.append(f"only {info['slides']} slides")
        if '/practice/m' in rel and info['bank'] == 0: errs.append('bank empty')
        if rel.endswith('exam/index.html') and info['exam'] < 15: errs.append('exam hub: too few cards ' + str(info['exam']))
        if rel.endswith('exam/print.html') or rel.endswith('exam/run.html'): pass         # these need ?exam=...; they are exercised in tests/exam_test.py
        errs += ['broken img ' + s for s in broken]
        if '/modules/' in rel: pg.screenshot(path=f"{ROOT}/tests/shots/{rel.replace('/', '_')}.png", full_page=False)
        fails += bool(errs); print('FAIL' if errs else 'ok  ', rel, info, errs[:4]); pg.close()
    br.close()
print('pages:', len(pages), 'failed:', fails); sys.exit(1 if fails else 0)
