"""Book map page (vi/books and en/books) of AE2.013, Playwright + Chrome.
Starts its own `python3 -m http.server` in the project root (port 8794) unless a base URL is given.
Usage: python3 tests/books_test.py [baseURL]   (build first: python3 -I build/build_site.py)
Checks per language: entry counts per book equal the JSON; module / role / search filters work instantly and rows of other modules are hidden;
no-match message; filter state is kept in the URL hash and restored on reload; slide thumbnails load (scrolled into view first, naturalWidth > 0);
lightbox opens; overview anchors exist; answers table numbers = cengel.json; no horizontal overflow at 390 px; no .katex-error; no console errors;
no wrong-language UI strings; the Questions column is hidden when data/bookmap/qcount.json is absent; fetch failure shows an error with a retry button.
Screenshots (1366 and 390 px) go to scratch/shots/."""
import json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SHOTS = os.path.join(ROOT, 'scratch', 'shots'); os.makedirs(SHOTS, exist_ok=True)
def J(n):
    with open(os.path.join(ROOT, 'data', 'bookmap', n + '.json'), encoding='utf-8') as f: return json.load(f)
C, F, E, S = J('cengel'), J('farokhi'), J('elsayed'), J('slides')
EXP = {'cengel': sum(len(c['sections']) + len(c['end_parts']) + len(c.get('features', [])) for c in C['chapters']), 'farokhi': len(F['entries']), 'elsayed': len(E['entries'])}
NSL = sum(len(d['slides']) for d in S.values())
srv = None
if len(sys.argv) > 1: BASE = sys.argv[1]
else:
    PORT = 8794
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    BASE = f'http://127.0.0.1:{PORT}/'; time.sleep(1.0)

VI_CH = re.compile('[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]', re.I)
EN_UI = ['All modules', 'All roles', 'Search section', 'Clear filters', 'Printed p.', 'Role legend', 'Overview: module', 'Table of contents of each book', 'Printed answers', 'What the books do not have', 'Lecturer', 'With printed answer']
VI_UI = ['Tất cả module', 'Xoá lọc', 'Tr. in', 'Chú giải vai trò', 'Điều sách không có', 'Đáp án in và bài tập', 'Tổng quan']
bad, nchk = [], 0
def chk(cond, *msg):
    global nchk; nchk += 1
    if not cond: bad.append(msg)

def visible(pg, book=None):
    sel = f'tr[data-book="{book}"]' if book else 'tr[data-book]'
    return pg.evaluate("s => [...document.querySelectorAll(s)].filter(r => !r.classList.contains('bm-hide')).length", sel)
def total(pg, book): return pg.evaluate("s => document.querySelectorAll(s).length", f'tr[data-book="{book}"]')

try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='chrome')
        for lang in ('vi', 'en'):
            vi = lang == 'vi'; url = f'{BASE}{lang}/books/index.html'
            pg = br.new_page(viewport={'width': 1366, 'height': 900}); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            r404 = []; pg.on('response', lambda r: r404.append(r.url) if r.status >= 400 else None)
            pg.goto(url, wait_until='load'); pg.wait_for_selector('#bm-app[data-ready="1"]', timeout=15000)
            for b, n in EXP.items(): chk(total(pg, b) == n, lang, 'entries', b, total(pg, b), n)
            chk(pg.evaluate("() => !!document.querySelector('.bm-noq')") and not pg.evaluate("() => [...document.querySelectorAll('th.bm-qc')].some(e => e.offsetParent !== null)"), lang, 'questions column should be hidden without qcount.json')
            # filters
            tot = visible(pg)
            pg.select_option('#bm-mod', 'm04'); n04 = visible(pg)
            chk(0 < n04 < tot, lang, 'module filter', n04, tot)
            other = pg.evaluate("() => [...document.querySelectorAll('tr[data-book]')].filter(r => !r.classList.contains('bm-hide') && !(r.dataset.mods || '').split(' ').includes('m04')).length")
            chk(other == 0, lang, 'rows of other modules still shown', other)
            exp04 = sum(1 for c in C['chapters'] for s in c['sections'] + c['end_parts'] if 'm04' in s['mods']) + sum(1 for e in F['entries'] if 'm04' in e['mods']) + sum(1 for e in E['entries'] if 'm04' in e['mods'])
            chk(n04 == exp04, lang, 'm04 count vs JSON', n04, exp04)
            pg.select_option('#bm-role', 'core'); nc = visible(pg)
            chk(0 < nc < n04, lang, 'role filter', nc, n04)
            notcore = pg.evaluate("() => [...document.querySelectorAll('tr[data-book]')].filter(r => !r.classList.contains('bm-hide') && !(r.dataset.roles || '').split(' ').includes('core')).length")
            chk(notcore == 0, lang, 'non-core rows visible under role=core', notcore)
            h = pg.evaluate("() => location.hash"); chk('m=m04' in h and 'r=core' in h, lang, 'hash not written', h)
            pg.reload(wait_until='load'); pg.wait_for_selector('#bm-app[data-ready="1"]')
            chk(pg.input_value('#bm-mod') == 'm04' and pg.input_value('#bm-role') == 'core' and visible(pg) == nc, lang, 'hash restore', pg.input_value('#bm-mod'), visible(pg), nc)
            pg.click('#bm-reset'); chk(visible(pg) == tot, lang, 'reset')
            pg.fill('#bm-q', 'brayton'); nq = visible(pg); chk(nq >= 3, lang, 'search brayton', nq)
            pg.fill('#bm-q', 'zzzzqq'); chk(visible(pg) == 0 and not pg.evaluate("() => document.getElementById('bm-none').hidden"), lang, 'no-match message')
            pg.fill('#bm-q', ''); chk(visible(pg) == tot, lang, 'clear search')
            # chapter 9 of Cengel: module m02 core rows
            pg.select_option('#bm-mod', 'm02'); pg.select_option('#bm-role', 'core'); pg.fill('#bm-q', 'otto')
            chk(pg.evaluate("() => [...document.querySelectorAll('tr[data-book=cengel]:not(.bm-hide) td:first-child')].some(td => td.textContent.includes('Otto Cycle'))"), lang, 'Cengel 9-5 Otto not found with m02/core/otto')
            pg.click('#bm-reset')
            # slides
            pg.evaluate("() => { const d = document.getElementById('bm-book-slides'); d.open = true; }")
            pg.wait_for_selector('.bm-card', timeout=5000)
            chk(pg.evaluate("() => document.querySelectorAll('.bm-card').length") == NSL, lang, 'slide cards', pg.evaluate("() => document.querySelectorAll('.bm-card').length"), NSL)
            chk(pg.evaluate("() => document.querySelectorAll('img[loading=lazy]').length") == 0, lang, 'lazy images present')
            pg.select_option('#bm-deck', 'ch3'); ns = pg.evaluate("() => [...document.querySelectorAll('.bm-card')].filter(c => !c.classList.contains('bm-hide')).length")
            chk(ns == S['ch3']['pages'], lang, 'deck filter', ns, S['ch3']['pages'])
            pg.evaluate("() => document.getElementById('bm-grid').scrollIntoView()"); pg.wait_for_timeout(1500)
            nl = pg.evaluate("() => [...document.querySelectorAll('.bm-card:not(.bm-hide) img')].filter(i => i.complete && i.naturalWidth > 0).length")
            chk(nl == ns, lang, 'ch3 thumbnails loaded', nl, ns)
            pg.select_option('#bm-deck', ''); pg.wait_for_timeout(2500)
            nl = pg.evaluate("() => [...document.querySelectorAll('.bm-card img')].filter(i => i.complete && i.naturalWidth > 0).length")
            chk(nl == NSL, lang, 'all thumbnails loaded', nl, NSL)
            pg.click('.bm-card:not(.bm-hide) a'); chk(pg.locator('.lightbox img').count() == 1, lang, 'lightbox'); pg.keyboard.press('Escape'); chk(pg.locator('.lightbox').count() == 0, lang, 'lightbox close')
            pg.select_option('#bm-mod', 'm03'); pg.wait_for_timeout(100)
            m03 = pg.evaluate("() => [...document.querySelectorAll('.bm-card')].filter(c => !c.classList.contains('bm-hide')).length")
            chk(m03 == sum(1 for d in S.values() for x in d['slides'] if x['module'] == 'm03'), lang, 'slide module filter m03', m03)
            pg.click('#bm-reset')
            # overview anchors, answers numbers, structure
            miss = pg.evaluate("() => [...document.querySelectorAll('table.bm-ov a[href^=\"#\"]')].filter(a => !document.querySelector(a.getAttribute('href'))).map(a => a.getAttribute('href'))")
            chk(not miss, lang, 'dead anchors', miss[:5])
            chk(pg.evaluate("() => document.querySelectorAll('table.bm-ov tbody tr').length") == 5, lang, 'overview rows')
            pc = C['answers']['per_chapter']; ta = sum(v['with_answer'] for v in pc.values()); tp = sum(v['problems'] for v in pc.values())
            txt = pg.inner_text('#answers ~ ul') if False else pg.inner_text('main')
            chk(f'{ta}/{tp}' in txt, lang, 'answers total text', ta, tp)
            for ch in ('9', '11', '14', '15', '17'): chk(f'{pc[ch]["with_answer"]}/{pc[ch]["problems"]}' in txt, lang, 'chapter answers', ch)
            for idn in ('overview', 'books', 'slides', 'answers', 'gaps'): chk(pg.evaluate("i => !!document.getElementById(i)", idn), lang, 'missing section', idn)
            chk('11-8' in txt or '11–8' in txt, lang, 'gaps mention 11-8')
            chk(pg.evaluate("() => document.querySelectorAll('.katex-error').length") == 0, lang, 'katex-error')
            # language purity (UI text only: book titles and basis are English data)
            ui = pg.evaluate("() => [...document.querySelectorAll('h1,h2,h3,.lead,#bm-filters,summary,th,.callout,#answers ~ ul li,#gaps ~ ul li')].map(e => e.innerText).join(' | ')")
            if vi: chk(not [w for w in EN_UI if w in ui], lang, 'English UI in vi', [w for w in EN_UI if w in ui])
            else: chk(not VI_CH.search(re.sub(r'Çengel|Çen', '', ui)) or not [1 for m in [VI_CH.search(ui)] if m], lang, 'Vietnamese letters in en UI', VI_CH.findall(ui)[:5]) if False else None
            if not vi:
                body = pg.evaluate("() => document.querySelector('main').innerText"); chk(not [w for w in VI_UI if w in body], lang, 'Vietnamese UI in en', [w for w in VI_UI if w in body])
                vi_chars = VI_CH.findall(body); chk(not vi_chars, lang, 'Vietnamese letters on en page', vi_chars[:10])
            # the only tolerated failed request is the optional qcount.json (column hidden when absent)
            chk(all(u.endswith('qcount.json') for u in r404), lang, 'unexpected 4xx', r404)
            errs = [e for e in errs if not (e.startswith('Failed to load resource') and r404 and all(u.endswith('qcount.json') for u in r404))]
            chk(not errs, lang, 'console/page errors', errs[:3])
            pg.screenshot(path=os.path.join(SHOTS, f'books_{lang}_1366.png'), full_page=False)
            pg.evaluate("() => { document.querySelectorAll('details.bm-bk').forEach(d => d.open = true); }"); pg.wait_for_timeout(300)
            pg.close()
            # phone
            pm = br.new_page(viewport={'width': 390, 'height': 800}); pm.goto(url, wait_until='load'); pm.wait_for_selector('#bm-app[data-ready="1"]')
            pm.evaluate("() => document.querySelectorAll('details.bm-bk').forEach(d => d.open = true)"); pm.wait_for_timeout(1200)
            ov = pm.evaluate("() => document.documentElement.scrollWidth - window.innerWidth"); chk(ov <= 2, lang, 'horizontal overflow at 390px (all blocks open)', ov)
            pm.evaluate("() => window.scrollTo(0, 0)"); pm.screenshot(path=os.path.join(SHOTS, f'books_{lang}_390.png'), full_page=False)
            pm.screenshot(path=os.path.join(SHOTS, f'books_{lang}_390_full.png'), full_page=False, clip={'x': 0, 'y': 0, 'width': 390, 'height': 800})
            pm.evaluate("() => document.getElementById('overview').scrollIntoView()"); pm.screenshot(path=os.path.join(SHOTS, f'books_{lang}_390_overview.png'))
            pm.close()
            # error + retry, and qcount column
            pe = br.new_page(viewport={'width': 1000, 'height': 700}); pe.route('**/data/bookmap/slides.json', lambda r: r.abort()); pe.goto(url, wait_until='load'); pe.wait_for_selector('#bm-retry', timeout=8000)
            pe.unroute('**/data/bookmap/slides.json'); pe.click('#bm-retry'); pe.wait_for_selector('#bm-app[data-ready="1"]', timeout=8000); chk(total(pe, 'cengel') == EXP['cengel'], lang, 'retry did not recover'); pe.close()
            pq = br.new_page(viewport={'width': 1200, 'height': 700})
            qc = {'cengel': {'9–5': 7}, 'farokhi': {}, 'elsayed': {}}
            pq.route('**/data/bookmap/qcount.json', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps(qc)))
            pq.goto(url, wait_until='load'); pq.wait_for_selector('#bm-app[data-ready="1"]')
            chk(pq.evaluate("() => !document.querySelector('.bm-noq') && [...document.querySelectorAll('th.bm-qc')].every(e => e.offsetParent !== null || e.closest('details:not([open])'))"), lang, 'questions column should appear with qcount.json')
            chk(pq.evaluate("() => [...document.querySelectorAll('tr[data-book=cengel]')].some(r => r.textContent.includes('Otto Cycle') && r.querySelector('td.bm-qc').textContent.trim() === '7')"), lang, 'qcount value shown')
            pq.close()
            print(lang, 'rows', {b: n for b, n in EXP.items()}, 'tot', tot, 'm04', n04, 'core', nc, 'slides', NSL)
        br.close()
finally:
    if srv: srv.terminate()
print('checks:', nchk); print('FAILS:', bad or 'none'); sys.exit(1 if bad else 0)
