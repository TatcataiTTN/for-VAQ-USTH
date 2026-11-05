"""Block-ordered page text with superscripts kept (PyMuPDF spans): 10^(40 dB/20 dB) instead of the flattened '1040 dB/20 dB'.
page_blocks(page) -> list of blocks, each a list of line strings (reading order of the PDF's own blocks, so two-column pages stay separated)."""
import fitz, re
fitz.TOOLS.mupdf_display_errors(False)

def _line_text(spans):
    txt = [s for s in spans if s['text'].strip()] or spans; base = max(s['size'] for s in txt)                       # body size = the largest size on the line
    dom = max((s for s in txt if s['size'] >= base - 0.6), key=lambda s: len(s['text'].strip()))
    ref = dom['origin'][1]; parts = []                     # (kind, text); ref = baseline of the last full-size span (a raised numerator keeps its own baseline)
    for s in spans:
        t = s['text']
        if not t: continue
        small = s['size'] < 0.82 * dom['size']
        if not small and t.strip(): ref = s['origin'][1]
        kind = 'sup' if small and s['origin'][1] < ref - 0.16 * dom['size'] else ('sub' if small and s['origin'][1] > ref + 0.10 * dom['size'] else 'n')
        if parts and parts[-1][0] == kind: parts[-1] = (kind, parts[-1][1] + t)
        else: parts.append((kind, t))
    out = ''
    for kind, t in parts:
        if kind == 'sup':
            u = t.strip(); out += (' ' if t.startswith(' ') else '') + ('^' + u if re.fullmatch(r'[−\-+]?[\w.]+', u) else '^(' + u + ')')
        else: out += t
    return re.sub(r'[ \t]+', ' ', out).strip()

def _gap_text(page, bbox):
    rd = page.get_text('rawdict', clip=fitz.Rect(bbox)); out = ''; prev = None
    for b in rd['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                for ch in s['chars']:
                    x0, x1 = ch['bbox'][0], ch['bbox'][2]
                    if prev is not None and ch['c'] != ' ' and x0 - prev > 0.10 * s["size"] and not out.endswith(' '): out += ' '
                    out += ch['c']; prev = x1
    return re.sub(r'\s+', ' ', out).strip()

def page_blocks(page):
    d = page.get_text('dict'); res = []; glue = re.compile(r'[A-Za-z]{22,}')
    for b in d['blocks']:
        if b.get('type') != 0: continue
        lines = []
        for l in b['lines']:
            sp = [s for s in l['spans']]
            if not sp: continue
            tx = _line_text(sp)
            if glue.search(tx):                                    # the text layer has no space glyphs on this (justified) line: put spaces back from the gaps between characters
                alt = _gap_text(page, l['bbox'])
                if alt: tx = alt
            if tx: lines.append(tx)
        if lines: res.append(dict(bbox=b['bbox'], lines=lines))
    return res
