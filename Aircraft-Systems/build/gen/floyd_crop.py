# -*- coding: utf-8 -*-
"""Cat anh de bai va anh dap an in (Phu luc 'Answers to odd-numbered problems') cua Floyd, Digital Fundamentals 11e, TU DONG tu PDF goc theo toa do chu
(thay cho cat tay theo toa do trong ocr/floyd/scripts). Dung chung cho cac bai tap Floyd moi.
  question_png(ch, n, page, out, upto=None, first=None)  de bai n (va hinh) tu khoi 'n.' den khoi so ke tiep / tieu de muc / het trang; 'first' = bat dau tu bai nho hon (de lay hinh cua bai truoc)
  answer_png(page, n, out)   dap an in cua bai n (mot cot, tu hang 'n.' den hang 'm.' ke tiep)
Tra ve (so trang PDF, toa do) de ghi lai trong nhan nguon."""
import os, re, glob, fitz
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PDF = glob.glob(os.path.join(ROOT, '..', 'sources', 'textbooks', '*Floyd*.pdf'))[0]
_doc = None
def doc():
    global _doc
    if _doc is None: _doc = fitz.open(PDF)
    return _doc
NUM = re.compile(r'^\s*(\d{1,2})\.\s')
def _blocks(pg): return sorted(pg.get_text('blocks'), key=lambda b: (round(b[1]), b[0]))
def question_png(ch, n, page, out, first=None, dpi=200):
    pg = doc()[page - 1]; r = pg.rect; start = first if first is not None else n; y0 = y1 = None
    bl = _blocks(pg)
    for b in bl:
        m = NUM.match(b[4])
        if m and int(m.group(1)) == start and b[0] < 250 and y0 is None: y0 = b[1]
    assert y0 is not None, ('khong thay bai', ch, start, page)
    y1 = r.height - 58
    for b in bl:
        t = b[4].strip()
        m = NUM.match(t)
        if b[1] <= y0 + 4: continue
        if (m and b[0] < 250 and int(m.group(1)) > n) or t.startswith('Section') or t.startswith('Basic Problems') or t.startswith('Applied Logic'):
            y1 = min(y1, b[1] - 2)
    clip = fitz.Rect(52, y0 - 3, r.width - 40, y1)
    pm = pg.get_pixmap(dpi=dpi, clip=clip); pm.save(out); return page, (round(clip.y0), round(clip.y1)), pm.width, pm.height
def answer_png(page, n, out, dpi=200):
    pg = doc()[page - 1]; r = pg.rect; words = pg.get_text('words')
    cand = [w for w in words if w[4] == f'{n}.' ]
    assert cand, ('khong thay dap an', n, page)
    w0 = min(cand, key=lambda w: w[1]); col = (30, 300) if w0[0] < 300 else (300, r.width - 20)
    rows = {}
    for w in words:
        if col[0] <= w[0] < col[1]: rows.setdefault(round(w[1] / 3), []).append(w)
    ys = sorted(rows); y_start = w0[1] - 2; y_end = None
    for k in ys:
        row = sorted(rows[k], key=lambda w: w[0]); first = row[0][4]
        if rows[k][0][1] > y_start + 6 and re.fullmatch(r'\d{1,2}\.', first) and first != f'{n}.': y_end = rows[k][0][1] - 2; break
    if y_end is None: y_end = min(r.height - 50, y_start + 60)
    clip = fitz.Rect(col[0], y_start, col[1], y_end)
    pm = pg.get_pixmap(dpi=dpi, clip=clip); pm.save(out); return page, (round(clip.y0), round(clip.y1)), pm.width, pm.height
def answer_text(page, n):
    """Van ban dap an in cua bai n (cung cach xac dinh khung nhu answer_png) de doi chieu tu dong."""
    pg = doc()[page - 1]; r = pg.rect; words = pg.get_text('words')
    cand = [w for w in words if w[4] == f'{n}.']; w0 = min(cand, key=lambda w: w[1]); col = (30, 300) if w0[0] < 300 else (300, r.width - 20)
    rows = {}
    for w in words:
        if col[0] <= w[0] < col[1]: rows.setdefault(round(w[1] / 3), []).append(w)
    out = []
    for k in sorted(rows):
        row = sorted(rows[k], key=lambda w: w[0]); y = rows[k][0][1]
        if y < w0[1] - 3: continue
        if out and re.fullmatch(r'\d{1,2}\.', row[0][4]) and row[0][4] != f'{n}.': break
        out.append(' '.join(x[4] for x in row))
        if len(out) > 8: break
    return ' '.join(out)
