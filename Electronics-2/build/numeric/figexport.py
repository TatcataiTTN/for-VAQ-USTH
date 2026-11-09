"""Cut every Floyd 9e figure that a solved exercise refers to (data/numeric/calc_solved.json: the 'circuit' text names 'Figure N–M') out of the PDF and save it as a compact PNG in
assets/figs/floyd/, so the Written Practice page can show the circuit next to the problem.  data/numeric/figs.json maps 'N–M' -> file.
The bounding box comes from the VECTOR drawing of the page (wires, parts, curves, drawn between the caption label and the end of the figure), not from pixels: drawings wider than
the text column (example box, rules) are ignored; the text labels inside the box are included by a margin; ▶ captions have their figure to the right of / below the label, ▲ captions have it above.
Usage: python3 -I build/numeric/figexport.py [label ...]   (no argument: every label named in calc_solved.json)"""
import sys, os, re, io, json, math, collections
import fitz
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PDF = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'Floyd_Electronic_Devices_9e_fixed.pdf'); OUTD = os.path.join(ROOT, 'assets', 'figs', 'floyd'); os.makedirs(OUTD, exist_ok=True)
def caption_hits(doc, lab, hint, span=10):
    res = []
    for p in (range(max(1, hint - span), min(len(doc), hint + span) + 1) if hint else range(1, len(doc) + 1)):
        page = doc[p - 1]
        for r in page.search_for('FIGURE ' + lab):
            if page.get_text('text', clip=fitz.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1)).strip().startswith('FIGURE ' + lab):
                near = page.get_text('text', clip=fitz.Rect(r.x0 - 30, r.y0 - 3, r.x0 + 2, r.y1 + 3)); res.append((p, r, 'up' if '▲' in near else 'left' if '◀' in near else 'right'))
    return res
def other_captions(page, cap):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for sp in l['spans']:
                if 'Strayhorn' in sp['font'] and sp['text'].strip().upper().startswith('FIGURE'):
                    r = fitz.Rect(sp['bbox'])
                    if abs(r.y0 - cap.y0) > 12: out.append(r)
    return out
MANUAL = {'15–12': (793, (48.0, 61.0, 446.0, 421.0))}                                          # two sub-figures (a) and (b) one under the other: box read off the page
TABLES = {'12–77': 60.0}                                                                          # a datasheet table (ruled text, no figure drawing): from the top of the page body to the caption
def collect(page):
    out = []; ds = page.get_drawings(); cell = collections.Counter()
    for d in ds: cell[(int((d['rect'].x0 + d['rect'].x1) / 40), int((d['rect'].y0 + d['rect'].y1) / 40))] += 1
    dense = {c for c, n in cell.items() if n > 60}                                          # the Multisim badge is built of hundreds of tiny paths: not part of any figure
    badge = None
    for d in ds:
        r = d['rect']
        if (int((r.x0 + r.x1) / 40), int((r.y0 + r.y1) / 40)) in dense and r.width < 60 and r.height < 60: badge = fitz.Rect(r) if badge is None else badge | r
    if badge is not None: badge = fitz.Rect(badge.x0 - 8, badge.y0 - 8, badge.x1 + 8, badge.y1 + 8)
    for d in ds:
        r = d['rect']
        if r.width > 470 or r.height > 520 or (r.height < 1.0 and r.width > 150) or r.x1 < 0 or r.y1 < 0: continue     # page frames, example box, caption rules
        if (int((r.x0 + r.x1) / 40), int((r.y0 + r.y1) / 40)) in dense and r.width < 60 and r.height < 60: continue
        if badge is not None and r.width < 60 and r.height < 60 and badge.contains(r): continue
        if d.get('color') and tuple(round(c, 2) for c in d['color']) == (0.0, 0.4, 0.7): continue                       # caption rule
        fl = d.get('fill'); co = d.get('color')
        if (fl and fl[0] > 0.75 and fl[1] < 0.62 and fl[2] < 0.35) or (co and co[0] > 0.75 and co[1] < 0.62 and co[2] < 0.35): continue    # orange side bar and frame of the example boxes
        if d.get('fill') and tuple(round(c, 2) for c in d['fill']) not in ((1.0, 1.0, 1.0),) and r.width > 300 and r.height > 120: continue
        out.append((r, bool(d.get('fill')) and tuple(round(c, 2) for c in d['fill']) == (1.0, 1.0, 1.0) and r.width > 60 and r.height > 60))
    return out
def figure_box(page, cap, dirn, gap=30.0):
    up = dirn == 'up'
    """Bounding box of the figure that belongs to the caption `cap`: the white panel of an example box if there is one next to the caption, otherwise the drawings that follow the caption (▶: from its
    top downwards, ▲: from its top upwards) until a vertical gap larger than `gap` points."""
    items = collect(page); panels = [r for r, w in items if w]; others = other_captions(page, cap)
    items = [(r, w) for r, w in items if w or not (r.width < 14 and r.height < 14 and fitz.Rect(cap.x0 - 14, cap.y0 - 14, cap.x1 + 14, cap.y1 + 14).intersects(r))]      # the ▶ ◀ ▲ arrow of the caption
    near = [r for r in panels if (r.y1 > cap.y0 - 40 and r.y1 < cap.y0 + 40) ] if up else [r for r in panels if abs(r.y0 - cap.y0) < 60 and ((r.x1 < cap.x0 + 10) if dirn == 'left' else (r.x0 > cap.x0 - 10))]
    if near: return min(near, key=lambda r: abs((r.y1 if up else r.y0) - cap.y0))
    rects = [r for r, w in items if not w]
    if up:
        prev = [o.y1 for o in others if o.y1 < cap.y0 - 15]; lo = max(prev) + 2 if prev else -1e9; rects = [r for r in rects if r.y0 >= lo]       # not above the previous caption: that is another figure
    else:
        nxt = [o.y0 for o in others if o.y0 > cap.y0 + 15]; hi = min(nxt) - 3 if nxt else 1e9; rects = [r for r in rects if r.y1 <= hi + 4]            # not reaching the next caption
    if up:
        cur = None; todo = sorted([r for r in rects if r.y1 <= cap.y0 + 3], key=lambda r: -r.y1)
        for r in todo:
            if cur is None:
                if cap.y0 - r.y1 < 45: cur = fitz.Rect(r)
            elif r.y1 >= cur.y0 - gap: cur.include_rect(r)
        return cur
    side = (lambda r: r.x1 <= cap.x0 + 6) if dirn == 'left' else (lambda r: r.x0 >= cap.x1 + 4)                                  # ▶: the figure is right of the label column; ◀: left of it
    cur = None; todo = sorted([r for r in rects if r.y1 >= cap.y0 - 15 and side(r)], key=lambda r: r.y0)
    for r in todo:
        if cur is None:
            if r.y0 - cap.y0 < 60: cur = fitz.Rect(r)
        elif r.y0 <= cur.y1 + gap: cur.include_rect(r)
    return cur
def add_labels(page, box, cap, dirn):
    up = dirn == 'up'
    """Grow the drawing box so that it contains the small-print labels of the figure (component values, (a)/(b) tags): spans of the figure font (≤ 8.6 pt) that touch the box enlarged by 26 pt;
    the caption itself and the larger text of the problem statements are not included."""
    big = fitz.Rect(box.x0 - 26, box.y0 - 16, box.x1 + 26, box.y1 + 30); u = fitz.Rect(box)
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for sp in l['spans']:
                r = fitz.Rect(sp['bbox']); t = sp['text'].strip()
                if not t or t.upper().startswith(('FIGURE', 'IGURE')) or 'Strayhorn' in sp['font'] or sp['size'] > 8.6 or sp['size'] < 5: continue          # figure labels are 6-8 pt Times; the statements are 9 pt
                if dirn == 'right' and r.x0 < cap.x1 + 4: continue
                if dirn == 'left' and r.x1 > cap.x0 + 6: continue
                if r.intersects(big) and ((r.y1 <= cap.y0 + 2) if up else (r.y0 >= cap.y0 - 12)): u.include_rect(r)
    return u
def export(doc, lab, hint, dpi=150):
    hits = caption_hits(doc, lab, hint)
    if not hits: return None, 'caption not found'
    p, r, dirn = min(hits, key=lambda h: abs(h[0] - hint)); page = doc[p - 1]; up = dirn == 'up'
    box = figure_box(page, r, dirn); pg = page; cap = r
    if lab in MANUAL and MANUAL[lab][0] == p: box = fitz.Rect(*MANUAL[lab][1]); panel = False
    if lab in TABLES: box = fitz.Rect(60, TABLES[lab], page.rect.width - 40, r.y0 - 4); panel = False
    if box is None and up and p > 1:                                                      # the figure continues from the previous page
        pg = doc[p - 2]; cap = fitz.Rect(r.x0, pg.rect.height + 5, r.x1, pg.rect.height + 15); box = figure_box(pg, cap, 'up'); p -= 1
    if box is None: return None, 'no vector drawing'
    panel = any(w and abs(r2.y0 - box.y0) < 1 and abs(r2.y1 - box.y1) < 1 for r2, w in collect(pg))
    if panel: box = fitz.Rect(box.x0 - 1, box.y0 - 1, box.x1 + 1, box.y1 + 1)
    else:
        box = box if (lab in TABLES or lab in MANUAL) else add_labels(pg, box, cap, dirn); box = fitz.Rect(box.x0 - 10 if dirn != 'right' else max(box.x0 - 10, cap.x1 + 2), box.y0 - 6, box.x1 + 10 if dirn != 'left' else min(box.x1 + 10, cap.x0 - 2), box.y1 + 5)
    box = fitz.Rect(max(0, box.x0), max(0, box.y0), min(pg.rect.width, box.x1), min(pg.rect.height, box.y1))
    return Image.open(io.BytesIO(pg.get_pixmap(clip=box, dpi=dpi).tobytes('png'))), f'p{p} box {[round(v) for v in box]}' + (' panel' if panel else '')
def labels_from_calc():
    cs = json.load(open(os.path.join(ROOT, 'data', 'numeric', 'calc_solved.json'), encoding='utf-8'))['solved']; out = {}
    for k, v in cs.items():
        if v['book'] != 'floyd' or not v.get('circuit'): continue
        head = re.split(r'\(pp?\.|:', v['circuit'], 1)[0]
        for lab in re.findall(r'\d+–\d+', head): out.setdefault(lab, []).append(int(v['pdf']))
    return out
if __name__ == '__main__':
    doc = fitz.open(PDF); want = labels_from_calc(); sel = sys.argv[1:] or sorted(want, key=lambda x: [int(t) for t in x.split('–')]); res = {}; bad = []
    for lab in sel:
        img = None
        for h in (want.get(lab) or [0]) + [0]:                                              # try the page of each exercise that cites the figure, then the whole book
            img, note = export(doc, lab, h)
            if img is not None: break
        if img is None: bad.append((lab, note)); print('FAIL', lab, note); continue
        fn = f'f{lab.replace("–", "-")}.png'; img.convert('P', palette=Image.ADAPTIVE, colors=48).save(os.path.join(OUTD, fn), optimize=True); res[lab] = 'assets/figs/floyd/' + fn; print('ok  ', lab, img.size, note)
    if not sys.argv[1:]: json.dump(res, open(os.path.join(ROOT, 'data', 'numeric', 'figs.json'), 'w'), ensure_ascii=False, indent=0)
    print(len(res), 'figures;', 'problems:', bad or 'none')
