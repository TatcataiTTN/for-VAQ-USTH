"""Book map page: filter by module, 'assigned only', title search, anchors from the overview, no horizontal page overflow at phone width.
Usage: python3 tests/books_test.py [baseURL]   (needs python3 -m http.server 8765 in the project root)"""
import sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
bad = []
def vis(pg): return pg.evaluate("() => [...document.querySelectorAll('details.bm-ch tbody tr:not(.bm-sep)')].filter(r => r.offsetParent !== null).length")
with sync_playwright() as pw:
    br = pw.chromium.launch(channel='chrome')
    for lang in ('vi', 'en'):
        pg = br.new_page(viewport={'width': 1280, 'height': 900}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.goto(f'{BASE}{lang}/books/index.html', wait_until='load')
        total = vis(pg)
        pg.select_option('#bm-mod', 'm04'); n04 = vis(pg)
        if not (0 < n04 < total): bad.append((lang, 'module filter', n04, total))
        hidden_other = pg.evaluate("() => [...document.querySelectorAll('details.bm-ch tbody tr:not(.bm-sep)')].filter(r => r.offsetParent !== null && !(r.dataset.mods || '').split(' ').includes('m04')).length")
        if hidden_other: bad.append((lang, 'rows of other modules still visible', hidden_other))
        pg.select_option('#bm-mod', ''); pg.fill('#bm-q', 'multistage'); nq = vis(pg)
        if nq < 1: bad.append((lang, 'search found nothing for multistage', nq))
        pg.fill('#bm-q', 'zzzzqq'); pg.wait_for_timeout(100)
        if vis(pg) != 0 or pg.evaluate("() => document.getElementById('bm-none').hidden"): bad.append((lang, 'no-match message', None))
        pg.fill('#bm-q', ''); pg.check('#bm-only'); na = vis(pg)
        if not (0 < na < total): bad.append((lang, 'assigned-only filter', na, total))
        # overview links point at existing anchors
        miss = pg.evaluate("() => [...document.querySelectorAll('table.bm-ov a[href^=\"#\"]')].filter(a => !document.querySelector(a.getAttribute('href'))).map(a => a.getAttribute('href'))")
        if miss: bad.append((lang, 'dead anchors', sorted(set(miss))))
        if errs: bad.append((lang, 'console/page errors', errs[:3]))
        print(lang, 'rows', total, 'm04', n04, 'search', nq, 'assigned', na); pg.close()
        pm = br.new_page(viewport={'width': 390, 'height': 800}); pm.goto(f'{BASE}{lang}/books/index.html', wait_until='load')
        ov = pm.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        if ov > 2: bad.append((lang, 'horizontal overflow at 390px', ov))
        pm.close()
    br.close()
print('FAILS:', bad or 'none'); sys.exit(1 if bad else 0)
