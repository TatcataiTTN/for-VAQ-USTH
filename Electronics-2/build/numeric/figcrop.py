"""Crop a figure of Floyd 9e (Electronic Devices, PDF in ../pdf_ocr_fixed) to OCR_output/floyd_figs/ so it can be read by eye.
Usage: python3 -I build/numeric/figcrop.py 6–16 [pdf_page_hint] [height_pt]
The caption 'FIGURE 6–16' is searched on the pages around the hint (the exercise page).  A yellow ▶ before the label means the figure stands to the right of / below the
label; a ▲ means the figure is above its caption (when it does not fit above the caption on the same page the bottom of the previous page is stacked on top).
The crops are for reading while writing solvers; they are NOT published (OCR_output/ is excluded by build/push.sh): the site describes each circuit in words and cites
the figure and page."""
import sys, os, io, fitz
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PDF = os.path.join(ROOT, '..', 'pdf_ocr_fixed', 'Floyd_Electronic_Devices_9e_fixed.pdf')
OUT = os.path.join(ROOT, 'OCR_output', 'floyd_figs'); os.makedirs(OUT, exist_ok=True)
def shot(page, y0, y1, dpi): return Image.open(io.BytesIO(page.get_pixmap(clip=fitz.Rect(0, y0, page.rect.width, y1), dpi=dpi).tobytes('png')))
def crop(label, hint=None, height=380, dpi=170, span=8):
    doc = fitz.open(PDF); lab = label.replace('-', '–')
    pages = range(max(1, (hint or 1) - span), min(len(doc), (hint or len(doc)) + span) + 1) if hint else range(1, len(doc) + 1); done = []
    for p in pages:
        page = doc[p - 1]
        for r in page.search_for('FIGURE ' + lab):                      # search_for ignores case: keep only hits that are really set in capitals (the caption label)
            if not page.get_text('text', clip=fitz.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1)).strip().startswith('FIGURE ' + lab): continue
            near = page.get_text('text', clip=fitz.Rect(r.x0 - 30, r.y0 - 3, r.x1, r.y1 + 3)); up = '▲' in near or (page.get_text('text', clip=fitz.Rect(r.x0 - 30, r.y0 - 3, r.x0, r.y1 + 3)).strip() == '' and False)
            if not up:                                                   # ▶ : figure to the right of / below the label
                img = shot(page, max(0, r.y0 - 15), min(page.rect.height, r.y0 + height), dpi)
            else:                                                        # ▲ : figure above the caption
                top = r.y0 - height
                if top >= 0: img = shot(page, top, r.y1 + 10, dpi)
                else:
                    a = shot(page, 0, r.y1 + 10, dpi)
                    if p > 1: b = shot(doc[p - 2], doc[p - 2].rect.height + top, doc[p - 2].rect.height, dpi); img = Image.new('RGB', (a.width, a.height + b.height), 'white'); img.paste(b, (0, 0)); img.paste(a, (0, b.height))
                    else: img = a
            fn = os.path.join(OUT, f'fig_{lab.replace("–", "-")}_p{p}_{len(done)}.png'); img.convert('RGB').save(fn); done.append(fn)
        if done: break
    return done
if __name__ == '__main__':
    a = sys.argv; r = crop(a[1], int(a[2]) if len(a) > 2 else None, float(a[3]) if len(a) > 3 else 380); print('\n'.join(r) or 'not found')
