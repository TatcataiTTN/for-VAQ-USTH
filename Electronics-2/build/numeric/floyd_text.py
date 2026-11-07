"""Physical text lines of a Floyd 9e page, rebuilt from the characters.
Why: in the PDF the spans of one printed line are not stored left to right (e.g. 'for a particular JFET.' comes BEFORE 'V_GS(off) = -6 V' in the content stream), so
PyMuPDF puts them in different lines/blocks and the old scan dropped the narrow fragment: 'IDSS = 20 mA and for a particular JFET.' lost its VGS(off) = -6 V.
Here every character is placed on the line whose baseline it sits on, sorted by x; sub- and superscripts attach to the line (superscripts as ^x), and the glyphs of the
math font Optr2k (whose codes are not the printed symbols) are translated.  Lines of body fonts and of other fonts (headings, figure labels, sidebars) are built apart so a
figure label at the same height never merges into a statement.
page_lines(page) -> list of dict(y, x0, x1, size, text, kind)   kind: body | head | fig | small"""
import re, fitz
fitz.TOOLS.mupdf_display_errors(False)
BODY = re.compile(r'^(Times|MathematicalPi|MathPi|Optr2k|PBB2k|Symbol|Grk2k|Universal-GreekwithMathP|Rads2K|Courier|ZapfDingbats)')
MATH = re.compile(r'^(MathematicalPi|MathPi|Optr2k|PBB2k|Symbol|Grk2k|Universal-GreekwithMathP|Rads2K)')
# Optr2k glyph codes -> printed symbols (identified from crops of the page images)
OPTR = {'-': '−', ';': '±', '¿': '′', 'Á': '…', 'ƒ': '|', '¢': 'Δ', '7': '>', 'G': '≥', 'V': '≪', 'œ': '′'}
STRAY = {'æ': 'Ω'}                                                          # the checkup font prints the ohm sign with the code of 'æ' (the letter never occurs in the statements)
SPACE = 0.12                                                               # a gap wider than this fraction of the font size is a word space when the PDF has no space glyph
GAPCUT = 14.0                                                              # points; an ordinary word space is about 2.2 pt
BIG = 8.4                                                                  # body text is 9 pt; sub/superscripts 6-7 pt; figure labels 8 pt or less

def _chars(page):
    d = page.get_text('rawdict'); out = []
    for b in d['blocks']:
        if b.get('type') != 0: continue
        for l in b['lines']:
            for s in l['spans']:
                f = s['font']
                for c in s['chars']:
                    ch = c['c']
                    if f == 'Optr2k': ch = OPTR.get(ch, ch)
                    ch = STRAY.get(ch, ch)
                    out.append(dict(c=ch, x0=c['bbox'][0], x1=c['bbox'][2], y=c['origin'][1], size=min(s['size'], 7.0) if ch == '′' else s['size'], font=f))   # a prime is attached to the line and kept inline, never a superscript
    return out

def _lines(chars, kind_of):
    big = [c for c in chars if c['size'] >= BIG and c['c'].strip() and not MATH.match(c['font'])] or [c for c in chars if c['size'] >= BIG and c['c'].strip()]      # baselines come from text fonts: a math font sits up to 2 pt off the text baseline
    big.sort(key=lambda c: c['y']); bases = []
    for c in big:
        if bases and abs(c['y'] - bases[-1][0]) <= 1.6: bases[-1][1].append(c)
        else: bases.append([c['y'], [c]])
    base_y = [sum(c['y'] for c in g) / len(g) for _, g in bases]
    spans = [[(c['x0'], c['x1']) for c in g] for _, g in bases]
    groups = [[] for _ in base_y]
    def xdist(i, c): return min((max(0.0, a0 - c['x1'], c['x0'] - a1) for a0, a1 in spans[i]), default=1e9)
    for c in chars:
        if not c['c'].strip() and c['size'] < BIG: continue
        if not base_y: break
        tol = 3.0 if MATH.match(c['font']) and c['size'] >= BIG else 1.8 if c['size'] >= BIG else 5.0
        cand = [i for i in range(len(base_y)) if abs(base_y[i] - c['y']) <= tol]
        if not cand: continue
        if len(cand) > 1: i = min(cand, key=lambda k: (xdist(k, c), abs(base_y[k] - c['y'])))          # two columns: a subscript belongs to the line whose letters it touches
        else: i = cand[0]
        groups[i].append(c)
    res = []
    segs = []                                                                   # a body line is cut where a gap far wider than a word space separates two pieces (figure labels standing on the same baseline)
    for by, g in zip(base_y, groups):
        g.sort(key=lambda c: (c['x0'], c['x1'])); cur = []; prevx = None
        for c in g:
            if c['c'].strip():
                if prevx is not None and c['x0'] - prevx > GAPCUT and cur: segs.append((by, cur)); cur = []
                prevx = c['x1']
            cur.append(c)
        if cur: segs.append((by, cur))
    for by, g in segs:
        txt = ''; prev = None; mode = 'n'
        for c in g:
            small = c['size'] < BIG; kind = 'n'
            if small and c['c'].strip() and c['c'] != '′':
                kind = 'sup' if c['y'] < by - 1.5 else ('sub' if c['y'] > by + 1.2 else 'n')
            if prev is not None and c['c'] != ' ' and c['x0'] - prev > SPACE * 9 and not txt.endswith(' '): txt += ' '
            if kind == 'sup' and mode != 'sup': txt += '^'
            if mode == 'sup' and kind != 'sup' and c['c'] != ' ': pass
            txt += c['c'] if c['c'] != ' ' or kind != 'sup' else ' '
            mode = kind; prev = c['x1']
        txt = re.sub(r'\^([^\s^]*[^\s\w.−+\-/][^\s^]*)', lambda m: '^(' + m.group(1) + ')', txt)
        txt = re.sub(r'[ \t ]+', ' ', txt).strip()
        if not txt: continue
        sizes = [c['size'] for c in g if c['c'].strip()]; mx = max(sizes) if sizes else 0
        fonts = [c['font'] for c in g if c['c'].strip() and c['size'] >= BIG]
        res.append(dict(y=by, x0=min(c['x0'] for c in g if c['c'].strip()), x1=max(c['x1'] for c in g if c['c'].strip()), size=mx, text=txt,
                        kind=kind_of(fonts, mx), bold=bool(g) and 'Bold' in g[0]['font']))
    return res

def page_lines(page):
    chars = _chars(page)
    text = [c for c in chars if not MATH.match(c['font'])]; math = [c for c in chars if MATH.match(c['font'])]
    body = [c for c in text if BODY.match(c['font'])]; other = [c for c in text if not BODY.match(c['font'])]
    for m in math:                                                                 # a symbol joins the group (body text / heading font) of the nearest text character on its baseline
        near = [c for c in text if abs(c['y'] - m['y']) <= 6 and c['c'].strip()]
        if near:
            n = min(near, key=lambda c: min(abs(c['x1'] - m['x0']), abs(c['x0'] - m['x1'])))
            (body if BODY.match(n['font']) else other).append(m)
        else: body.append(m)
    lines = _lines(body, lambda fonts, mx: 'body' if mx >= BIG else 'small')
    def kind_other(fonts, mx):
        return 'fig' if fonts and all(f.startswith(('Arial', 'Helvetica')) for f in fonts) else 'head'
    lines += _lines(other, kind_other)
    lines.sort(key=lambda l: (round(l['y'] / 3), l['x0']))
    return lines

if __name__ == '__main__':
    import sys
    doc = fitz.open('../pdf_ocr_fixed/Floyd_Electronic_Devices_9e_fixed.pdf')
    for l in page_lines(doc[int(sys.argv[1]) - 1]):
        if l['kind'] in ('body', 'head'): print(f"{l['y']:6.1f} {l['x0']:6.1f} {l['kind']:5s} {l['text'][:150]}")
