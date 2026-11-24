# -*- coding: utf-8 -*-
"""Duong kiem thu hai cho ban chep slide: OCR (tesseract) tung slide tu PDF GOC o 200 dpi, doi chieu voi text_en cua ban chep.
Do: (1) pho = ti le tu (>=4 chu cai) cua ban chep tim thay trong OCR; (2) bo sot = ti le tu OCR (>=5 chu cai, nam trong tu dien cua chinh ban chep + sach) khong co trong ban chep; (3) so trong OCR khong co trong ban chep.
In danh sach slide lech de nguoi doc xem mat. Chay: .venv/bin/python build/verify/ocr_slides.py [deck ...]   -> data/verify/ocr_slides.json"""
import os, sys, re, json, subprocess, tempfile, importlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'transcripts'))
import fitz
PDF = {'cpu': 'Basic computer structure and microprocessor PDA version 2026.pdf', 'disp': 'Electronic displays - ver 2026.pdf', 'emc': 'Cours_EMC_Aircraft_ver2026.pdf', 'icmux': 'integrated circuit and multiplexing version 2026.pdf',
       'logic': 'logic circuit_version 2026.pdf', 'num': 'Number system.pdf', 'bus': 'Data buses aircraft - ver 2026 v2.pdf', 'fib': 'Optic_Fiber_ver 2026.pdf', 'swc': 'software management control.pdf'}
CACHE = os.path.join(ROOT, 'scratch', 'ocr_cache'); os.makedirs(CACHE, exist_ok=True)
def ocr_page(deck, page):
    fn = os.path.join(CACHE, f'{deck}_{page:02d}.txt')
    if os.path.exists(fn): return open(fn, encoding='utf-8').read()
    d = fitz.open(os.path.join(ROOT, '..', 'sources', 'lectures', PDF[deck])); pg = d[page - 1]
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, 'p.png'); pg.get_pixmap(dpi=200).save(png)
        r = subprocess.run(['tesseract', png, 'stdout', '-l', 'eng', '--psm', '3'], capture_output=True, text=True)
    open(fn, 'w', encoding='utf-8').write(r.stdout); return r.stdout
W = re.compile(r'[a-z]{4,}'); N = re.compile(r'\d+(?:[.,]\d+)?')
def words(t, n=4): return set(re.findall(r'[a-z]{%d,}' % n, t.lower()))
def stem(w): return w[:5]
def main(decks):
    out = {}; allflag = []
    for deck in decks:
        m = importlib.import_module(deck); S = {s['page']: s for s in m.S}
        for page, s in sorted(S.items()):
            if s.get('basis') != 'summary' and '--all' not in sys.argv: continue
            o = ocr_page(deck, page); tx = s['text_en'] + ' ' + s['title'] + ' ' + ' '.join(s['formulas'])
            tw = {stem(w) for w in words(tx)}; ow = words(o); ow5 = {stem(w) for w in words(o, 5)}
            cov = (sum(1 for w in words(tx) if stem(w) in {stem(x) for x in ow}) / max(1, len(words(tx))))
            miss = sorted(w for w in ow5 if w not in tw)
            tn = set(N.findall(tx.replace(',', '.'))); on = {x.replace(',', '.') for x in N.findall(o)}; nmiss = sorted(x for x in on if x not in tn and len(x) <= 6)
            out[f'{deck}:{page}'] = dict(cov=round(cov, 2), omitted_words=miss[:40], n_omitted=len(miss), numbers_missing=nmiss[:20])
            flag = cov < .55 or len(miss) >= 25 or len(nmiss) >= 6
            if flag: allflag.append((deck, page, round(cov, 2), len(miss), len(nmiss)))
    json.dump(out, open(os.path.join(ROOT, 'data', 'verify', 'ocr_slides.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('slides compared:', len(out), '| flagged for visual review:', len(allflag)); [print('  ', f) for f in allflag]
if __name__ == '__main__':
    main([a for a in sys.argv[1:] if not a.startswith('--')] or ['cpu', 'disp', 'emc', 'icmux'])

def check_patch_numbers():
    """Moi so (>= 2 chu so) trong 'numbers' cua phan va (zoom_patch.PATCH) phai co trong OCR cua dung slide; so OCR khong thay duoc liet ke de doi chieu mat (da lam, xem CONTINUE.md)."""
    import zoom_patch as Z
    miss = {}
    for (deck, page), pt in sorted(Z.PATCH.items()):
        if not pt['numbers']: continue
        o = ocr_page(deck, page).replace(',', '.').lower(); compact = re.sub(r'\s+', '', o)
        for vi, en in pt['numbers']:
            for tok in set(re.findall(r'\d+(?:\.\d+)?', en.replace(',', '').replace('10⁻', ''))):
                if len(tok) >= 2 and tok not in o and tok not in compact: miss.setdefault(f'{deck}:{page}', set()).add(tok)
    print('patched-number tokens not seen by OCR (confirmed by eye on the zoomed image):', {k: sorted(v) for k, v in miss.items()})
    return miss
if __name__ == '__main__' and '--patch' in sys.argv: check_patch_numbers()
