"""Cut the figures of Jaeger 5e (Microelectronic Circuit Design, PDF in ../pdf_ocr_fixed) that a solved exercise refers to, from the VECTOR drawing of the page
(Jaeger's figures are vector paths plus text, not pictures): the caption 'Figure 10.22' / 'Figure P10.44' stands BELOW its figure, so the figure is the group of drawings above
the caption (growing upward until a vertical gap larger than 28 pt, staying in the caption's column); the small-print labels of the figure are added.
Usage: python3 -I build/numeric/jfigexport.py [label ...]   (no argument: every label named by a 'circuit' text of data/numeric/jaeger_solved.json / calc_solved.json)
Output: assets/figs/jaeger/fNN.NN.png and data/numeric/jfigs.json  ('P10.44' -> file).  OCR_output/jaeger_figs/ keeps the contact sheets used to read the figures."""
import sys, os, re, io, json, collections
import fitz
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PDF = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'Jaeger_Microelectronic_Circuit_Design_5e_fixed.pdf'); OUTD = os.path.join(ROOT, 'assets', 'figs', 'jaeger')
SCRATCH = os.path.join(ROOT, 'OCR_output', 'jaeger_figs')
_IDX = {}
def caption_index(doc):
    """One pass over the book: {label: [(page, caption rect)]}.  Real captions only: the word 'Figure' (and its number) is set in a bold sans face (TradeGothic / HelveticaNeue,
    blue); a mention in running text is Times-Roman.  Cached in data/numeric/jcaptions.json (the PDF does not change)."""
    if _IDX: return _IDX
    cache = os.path.join(ROOT, 'data', 'numeric', 'jcaptions.json')
    if os.path.exists(cache):
        for k, v in json.load(open(cache, encoding='utf-8')).items(): _IDX[k] = [(p, fitz.Rect(*r)) for p, r in v]
        return _IDX
    sans = lambda x: 'Gothic' in x['font'] or 'Helvetica' in x['font']
    for p in range(1, len(doc) + 1):
        for b in doc[p - 1].get_text('dict')['blocks']:
            for l in b.get('lines', []):
                sp = l['spans']
                if not sp or not sans(sp[0]): continue
                head = ''.join(x['text'] for x in sp if sans(x)).strip(); m = re.fullmatch(r'Figure\s+(P?\d+\.\d+)', head)
                if m: _IDX.setdefault(m.group(1), []).append((p, fitz.Rect(sp[0]['bbox'][0], sp[0]['bbox'][1], max(x['bbox'][2] for x in sp if sans(x)), sp[0]['bbox'][3])))
    json.dump({k: [(p, list(r)) for p, r in v] for k, v in _IDX.items()}, open(cache, 'w'))
    return _IDX
def captions(doc, lab, hint=None, span=25):
    c = caption_index(doc).get(lab, [])
    return [x for x in c if abs(x[0] - hint) <= span] if hint else c
def page_captions(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            sp = l['spans']
            if sp and ('Gothic' in sp[0]['font'] or 'Helvetica' in sp[0]['font']) and ''.join(x['text'] for x in sp).strip().startswith('Figure'): out.append(fitz.Rect(l['bbox']))
    return out
def is_blue(c): return bool(c) and len(c) == 3 and c[2] > 0.8 and c[0] < 0.45 and c[1] > 0.35
def drawings(page):
    out = []; ds = page.get_drawings(); cell = collections.Counter()
    for d in ds: cell[(int((d['rect'].x0 + d['rect'].x1) / 40), int((d['rect'].y0 + d['rect'].y1) / 40))] += 1
    for d in ds:
        r = d['rect']
        if r.width > 480 or r.height > 400 or (r.height < 0.6 and r.width > 200): continue                 # page frames, text-block rules
        fl = d.get('fill')
        if is_blue(fl) or is_blue(d.get('color')): continue                                          # the blue hint icons (light bulb) next to some problem numbers
        if fl and r.width > 300 and r.height > 60 and not (fl[0] > 0.97 and fl[1] > 0.97): continue           # tinted boxes of the examples
        out.append(r)
    return out
TALL = {'P11.8': 600}                                                                       # figures taller than the usual 340 pt search window (four stacked sub-figures)
WIDE = {'P12.23': 40}                                                                        # figure labels whose drawing starts left of the caption (checked by eye)
def box_for(page, cap, problem, cap_label=''):
    """Problem figures (P…) are left-aligned with their caption in one of the two columns of the problem pages; figures of the text are centred over the caption line."""
    lo, hi = (cap.x0 - 22, cap.x0 + 500) if problem else (cap.x0 - 150, cap.x1 + 230)
    row = [c for c in page_captions(page) if abs(c.y0 - cap.y0) < 15 and c != cap]              # captions on the same baseline (figures side by side)
    left = [c for c in row if c.x1 < cap.x0 - 5]; right = [c for c in row if c.x0 > cap.x1 + 5]
    if not problem and left: lo = cap.x0 - 8                                                  # the figure starts at its own caption: the left neighbour is another figure
    if not problem and right: hi = min(hi, min(c.x0 for c in right) - 8)
    nxt = [c.x0 for c in page_captions(page) if c.x0 > cap.x0 + 120]                          # a caption of the other column of the page bounds the figure on the right
    if problem and nxt: hi = min(hi, min(nxt) - 6)
    if cap_label in WIDE: lo = min(lo, WIDE[cap_label])                                          # a wide problem figure whose caption is not left-aligned with it
    rects = [r for r in drawings(page) if r.y1 <= cap.y0 + 3 and r.y1 > cap.y0 - TALL.get(cap_label, 340) and r.x1 > lo and r.x0 < hi]
    cur = None
    for r in sorted(rects, key=lambda r: -r.y1):
        if cur is None:
            if cap.y0 - r.y1 < 60: cur = fitz.Rect(r); break
    if cur is None: return None
    grown = True
    while grown:                                                                               # grow to a fixpoint (the result does not depend on the order of the rectangles)
        grown = False
        for r in rects:
            if r.y1 >= cur.y0 - 28 and r.y0 <= cur.y1 + 2 and r.x1 > cur.x0 - 70 and r.x0 < cur.x1 + 70:
                before = tuple(cur); cur.include_rect(r)
                if tuple(cur) != before: grown = True                                           # (a degenerate line never counts as growth: no endless loop)
    return cur
def labels(page, box, cap):
    """Add the short labels (a whole text line of at most 14 characters: 'R2', '27 kΩ', 'vo', '(a)') that touch the box; the statements of the problems are long lines and stay out."""
    big = fitz.Rect(box.x0 - 14, box.y0 - 14, box.x1 + 14, box.y1 + 10); u = fitz.Rect(box)
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            txt = ''.join(sp['text'] for sp in l['spans']).strip(); r = fitz.Rect(l['bbox'])
            if not txt or len(txt) > 14 or txt.startswith('Figure') or r.y1 > cap.y0 + 1 or r.width > 90 or re.fullmatch(r'\d{1,2}\.\d{1,3}\.?', txt): continue            # (problem numbers such as '12.11.' of the next column stay out)
            if r.intersects(big): u.include_rect(r)
    return u
def export(doc, lab, hint=None, dpi=150):
    hs = captions(doc, lab, hint) or (captions(doc, lab) if hint else [])
    if not hs: return None, 'caption not found'
    p, cap = hs[0]; page = doc[p - 1]; box = box_for(page, cap, lab.startswith('P'), lab)
    if box is None: return None, 'no vector drawing above the caption'
    box = labels(page, box, cap); y0 = box.y0 - 8
    for c in page_captions(page):                                                              # the caption of the figure above, in the same column, stays out
        if c.y1 <= box.y0 + 3 and c.y1 > box.y0 - 14 and c.x1 > box.x0 and c.x0 < box.x1: y0 = max(y0, c.y1 + 1)
    for b in page.get_text('dict')['blocks']:                                                  # and so do the last lines of the text above it
        for l in b.get('lines', []):
            r = fitz.Rect(l['bbox']); txt = ''.join(sp['text'] for sp in l['spans']).strip()
            if len(txt) > 14 and r.y1 <= box.y0 + 1 and r.y1 > box.y0 - 14 and r.x1 > box.x0 and r.x0 < box.x1: y0 = max(y0, r.y1 + 0.5)
    x0, x1, y1 = max(0, box.x0 - 8), min(page.rect.width, box.x1 + 8), min(page.rect.height, cap.y0 - 1)
    foreign = []                                                                                 # text lines and hint icons that are not part of the figure: the margin must not reach them
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            r = fitz.Rect(l['bbox']); txt = ''.join(sp['text'] for sp in l['spans']).strip()
            if txt and (len(txt) > 14 or re.fullmatch(r'\d{1,2}\.\d{1,3}\.?', txt)): foreign.append(r)
    for d in page.get_drawings():
        if is_blue(d.get('fill')) or is_blue(d.get('color')): foreign.append(d['rect'])
    for r in foreign:
        if r.y1 > y0 and r.y0 < y1:
            if r.x0 >= box.x0 + 0.6 * (box.x1 - box.x0) and r.x0 < x1: x1 = r.x0 - 0.5                  # foreign text/icon on the right side (the other column): cut before it
            if r.x1 <= box.x0 + 0.5 and r.x1 > x0: x0 = r.x1 + 0.5
    box = fitz.Rect(x0, max(0, y0), x1, y1)
    return Image.open(io.BytesIO(page.get_pixmap(clip=box, dpi=dpi).tobytes('png'))), f'p{p} box {[round(v) for v in box]}'
def labels_from_texts():
    out = {}
    for fn, key in (('jaeger_solved.json', 'solved'), ('calc_solved.json', 'solved')):
        pth = os.path.join(ROOT, 'data', 'numeric', fn)
        if not os.path.exists(pth): continue
        for k, v in json.load(open(pth, encoding='utf-8'))[key].items():
            c = v.get('circuit')
            if not c: continue
            head = re.split(r'\(pp?\.|:', c, 1)[0]
            for lab in re.findall(r'P?\d+\.\d+', head): out.setdefault(lab, []).append(int(v['pdf']))
    return out
if __name__ == '__main__':
    args = sys.argv[1:]; scratch = '--scratch' in args; args = [a for a in args if a != '--scratch']; OUT_ = SCRATCH if scratch else OUTD; os.makedirs(OUT_, exist_ok=True)
    doc = fitz.open(PDF); want = labels_from_texts(); sel = args or sorted(want, key=lambda x: (x.startswith('P'), float(x.lstrip('P')))); res = {}; bad = []
    for lab in sel:
        img = None
        for h in (want.get(lab) or [0]) + [0]:
            img, note = export(doc, lab, h or None)
            if img is not None: break
        if img is None: bad.append((lab, note)); print('FAIL', lab, note); continue
        fn = f'f{lab}.png'; img.convert('P', palette=Image.ADAPTIVE, colors=48).save(os.path.join(OUT_, fn), optimize=True); res[lab] = 'assets/figs/jaeger/' + fn; print('ok  ', lab, img.size, note)
    if not args: json.dump(res, open(os.path.join(ROOT, 'data', 'numeric', 'jfigs.json'), 'w'), ensure_ascii=False, indent=0)
    print(len(res), 'figures;', 'problems:', bad or 'none')
