"""Scan Farokhi 2e (Aircraft Propulsion): Examples and end-of-chapter Problems of Ch.1-4, 6, 7 and the 45 quizzes of Appendix K.
Text comes from the PDF text layer through PyMuPDF spans (the OCR md has the same characters but lost the layout). Layout facts (checked on images, see handcheck.json):
  two columns (x0 = 33/263 on even printed pages, 53/283 on odd ones); problem number = TimesLTStd-Bold 9 "2.1" at the column edge, statement text at +29 on the first row;
  continuation lines start at the column edge; "(a) ..." items are Bold at +44; figure labels are Helvetica / Italic fragments; display equations are STIX fragments in the middle.
  Display equations, tables and figure labels are NOT reconstructed: a statement whose column area holds such fragments gets text_reliable=false (reason given) and its fragments are listed in `dropped`.
  Examples: header 'E X A M P L E n . m' (AvenirLTStd-Heavy 13.9), statement = Times 9 lines under it up to 'SOLUTION' or the first sentence end not followed by an item.
Run: python3 -I build/numeric/scan_farokhi.py -> data/numeric/farokhi_raw.json"""
import re, os, sys, json, collections
import fitz
sys.path.insert(0, os.path.dirname(__file__))
from common import *
fitz.TOOLS.mupdf_display_errors(False)
OFFSET = 34
CHAPS = (1, 2, 3, 4, 6, 7)

NUMRX = re.compile(r'^(\d)\.(\d{1,2})$')
MIDX = 258.0                       # column gutter: a span right of it never joins a line that starts left of it (a problem number at the right edge)
def lines_of(page):
    """merged physical lines of a page. 1) spans of size >= 8.4 are grouped on a baseline (tol 1.5 pt, same column side); 2) small spans (sub/superscripts, size <= 7.4) that sit within 4.5 pt of
    a line and inside its x range are inserted into it in x order (T + 1 -> 'T1'); the rest stay lines of their own (figure labels)."""
    big, small = [], []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0: continue
        for l in b['lines']:
            for s in l['spans']:
                if not s['text'].strip(): continue
                d = dict(x0=s['bbox'][0], x1=s['bbox'][2], y=s['origin'][1], size=s['size'], font=s['font'], text=s['text'])
                (small if s['size'] <= 7.4 and not s['font'].startswith(('Helvetica', 'MSAM')) else big).append(d)
    big.sort(key=lambda s: (round(s['y']), s['x0']))
    out = []
    for s in big:
        for l in out:
            if abs(l['y'] - s['y']) <= (6.5 if s['font'].startswith(('STIX', 'Symbol')) and len(s['text'].strip()) <= 3 else 3.2 if s['font'].startswith(('STIX', 'Symbol')) else 1.5) and abs(s['x0'] - l['x1']) < 12 and s['x0'] >= l['x0'] - 1 and (s['x0'] < MIDX) == (l['x0'] < MIDX) and not (s['x0'] > 258 and l['x0'] < 258 and NUMRX.match(s['text'].strip())):
                l['spans'].append(s); l['x1'] = max(l['x1'], s['x1']); break
        else: out.append(dict(y=s['y'], x0=s['x0'], x1=s['x1'], spans=[s]))
    for s in small:
        for l in out:
            if abs(l['y'] - s['y']) <= 4.5 and l['x0'] - 1 <= s['x0'] <= l['x1'] + 3 and (s['x0'] < MIDX) == (l['x0'] < MIDX) and l['spans'][0]['size'] >= 8.4:
                s['sub'] = True; l['spans'].append(s); l['x1'] = max(l['x1'], s['x1']); break
        else: out.append(dict(y=s['y'], x0=s['x0'], x1=s['x1'], spans=[s]))
    for l in out:
        l['spans'].sort(key=lambda s: s['x0'])
        full = [s for s in l['spans'] if not s.get('sub')] or l['spans']
        dom = max(full, key=lambda s: (len(s['text'].strip()), s['size'])); l['font'] = dom['font']; l['size'] = dom['size']
        txt = ''; prev = None
        for s in l['spans']:
            t = s['text']
            if prev is not None and not t.startswith(' ') and not txt.endswith(' '):
                gap = s['x0'] - prev['x1']
                if not (s.get('sub') or prev.get('sub')) and gap > 0.8: txt += ' '
                elif (s.get('sub') or prev.get('sub')) and gap > 2.2: txt += ' '
            txt += t; prev = s
        l['text'] = re.sub(r'\s+', ' ', txt).strip()
        l['stix'] = any(s['font'].startswith(('STIX', 'Symbol')) for s in l['spans'])
    return out

def column_edges(page, lines):
    """left/right column edges: the page is one of two layouts (even printed pages 33/263, odd 53/283); choose by counting text lines that start there"""
    mid = page.rect.width / 2 - 5
    best = None
    for el, er in ((33, 263), (53, 283)):
        n = sum(1 for l in lines if l['font'].startswith('Times') and l['size'] >= 8.9 and (abs(l['x0'] - el) <= 1.8 or abs(l['x0'] - er) <= 1.8))
        if best is None or n > best[0]: best = (n, el, er)
    return mid, best[1], best[2]

def is_text_line(l, edge):
    """a statement line: Times text (body 9 pt) inside the column; short italic fragments and anything in another font are figure labels / equation pieces"""
    if not l['font'].startswith('Times') or not (8.8 <= l['size'] <= 9.6): return False
    if not (edge - 1.8 <= l['x0'] <= edge + 215): return False
    if 'Italic' in l['font']: return len(l['text']) >= 25 and len(l['text'].split()) >= 4
    return len(l['text']) >= 10 or l['text'].endswith(('.', ':', '?', ','))

def parse_problems(doc, ch, p0, p1, chap_mod):
    items = []; cur = None
    for p in range(p0, p1 + 1):
        page = doc[p - 1]; L = lines_of(page); mid, el, er = column_edges(page, L)
        hy = next((l['y'] for l in L if l['text'] == 'Problems' and 'Bold' in l['font'] and l['size'] > 13), None) if not items else None
        cols = [(el, [l for l in L if l['x0'] < mid]), (er, [l for l in L if l['x0'] >= mid])]
        for edge, col in cols:
            col.sort(key=lambda l: (l['y'], l['x0']))
            i = 0; cur = cur if (cur and cur['pdf'] != p) else None
            for l in col:
                if l['y'] < 60 or l['y'] > 640: continue
                if hy is not None and l['y'] <= hy + 1: continue
                if hy is None and not items and cur is None: continue
                m = NUMRX.match(l['text'].split(' ')[0]) if 'Bold' in l['font'] and l['size'] < 9.6 and abs(l['x0'] - edge) <= 1.8 else None
                if m and l['spans'][0]['text'].strip() == m[0] and int(m[1]) == ch and len(l['spans']) == 1:
                    cur = dict(number=f'{ch}.{m[2]}', num=int(m[2]), pdf=p, edge=edge, y=l['y'], lines=[], dropped=[], figcap=False, col=edge); items.append(cur); continue
                if cur is None: continue
                if cur['pdf'] != p and cur['col'] != edge and cur['pdf'] == p: pass
                if re.match(r'^[■▪]?\s*F\s?I\s?G\s?U\s?R\s?E', l['text']) or l['font'].startswith('MSAM'): cur['figcap'] = True; continue
                first_row = abs(l['y'] - cur['y']) <= 2.5 and edge + 20 <= l['x0'] <= edge + 36 and cur['pdf'] == p and not cur['lines']
                if l['text'].startswith('Source:') or re.match(r'^(Reproduced|Courtesy)', l['text']): continue
                if (first_row and l['font'].startswith('Times')) or is_text_line(l, edge) and not (l['text'] in ('Problems',) and l['size'] > 13): cur['lines'].append((l['y'], l['text'], l['stix']))
                elif l['size'] > 13: continue
                else: cur['dropped'].append((round(l['y']), l['text'], l['stix']))
            # the statement stays open across the column/page break
    return items

# --- examples
def parse_examples(doc, ch, p0, p1):
    out = []
    for p in range(p0, p1 + 1):
        page = doc[p - 1]; L = lines_of(page); mid, el, er = column_edges(page, L)
        for h in L:
            if not (h['font'].startswith('Avenir') and re.match(r'^E\s?X\s?A\s?M\s?P\s?L\s?E', h['text'])): continue
            raw = re.sub(r'\s+', '', re.sub(r'^E\s?X\s?A\s?M\s?P\s?L\s?E', '', h['text'].split('(')[0]))
            m = re.match(r'^(\d)\.(\d{1,2})$', raw)
            if not m or int(m[1]) != ch: continue
            tm = re.search(r'\((.*)\)', h['text'])
            out.append(dict(number=f'{ch}.{m[2]}', pdf=p, hy=h['y'], hx=h['x0'], title=tm[1].strip() if tm else '', page=page))
    res = []
    for ex in out:
        collected = []; sol = False; done = False
        seq = []
        for pp in (ex['pdf'], ex['pdf'] + 1):
            if pp > len(doc): break
            page = doc[pp - 1]; L = lines_of(page); mid, el, er = column_edges(page, L)
            cl = [l for l in L if l['x0'] < mid]; cr = [l for l in L if l['x0'] >= mid]
            for c in (cl, cr): c.sort(key=lambda l: (l['y'], l['x0']))
            if pp == ex['pdf']:
                hcol = cl if ex['hx'] < mid else cr
                after = [l for l in hcol if l['y'] > ex['hy'] + 3]
                other = cr if hcol is cl else []
                seq += [(l, pp) for l in after] + [(l, pp) for l in other]
            else: seq += [(l, pp) for l in cl + cr]
        stop = False
        for l, pp in seq:
            t = l['text']
            if re.match(r'^(SOLUTION|Solution)$', t) or (l['font'].startswith('Avenir') and 'SOLUTION' in t): sol = True; break
            if l['font'].startswith('Avenir') and re.match(r'^E\s?X\s?A\s?M', t): break
            if not l['font'].startswith('Times') or l['size'] < 8.8 or l['size'] > 9.6: continue
            if 'Bold' in l['font'] and l['size'] > 9.4: continue
            collected.append(t)
            nxt_ok = True
            if re.search(r'[.?]$', t) and not re.search(r'\b(calculate|determine|find|following|and|or)\s*[.]?$', t, re.I):
                idx = [k for k, (ll, _) in enumerate(seq) if ll is l][0]
                nl = seq[idx + 1][0]['text'] if idx + 1 < len(seq) else ''
                if not re.match(r'^\(?[a-h]\)', nl) and not re.match(r'^\(?[a-h]\)', t): break
            if len(collected) > 40: break
        res.append(dict(number=ex['number'], pdf=ex['pdf'], title=ex['title'], text=tidy(' '.join(collected)), has_solution_printed=True, sol_label=sol))
    return res

def join_lines(lines):
    out = ''
    for _, t, _ in lines:
        if out.endswith('-') and re.match(r'^[a-z]', t) and re.search(r'[a-z]-$', out):
            out = out[:-1] + t          # line-end hyphenation ("com-bustor"); real hyphens at the line end are rare in these statements
        else: out += (' ' if out else '') + t
    return re.sub(r'\s+', ' ', out).strip()

def parse_quizzes(doc, p0, p1):
    res = []; cur = None
    for p in range(p0, p1 + 1):
        page = doc[p - 1]; L = lines_of(page); mid = page.rect.width / 2 - 5
        for col in ([l for l in L if l['x0'] < mid], [l for l in L if l['x0'] >= mid]):
            col.sort(key=lambda l: (l['y'], l['x0']))
            for l in col:
                if l['y'] < 60 or l['y'] > 610 and l['size'] < 9: continue
                m = re.match(r'^Quiz No\.\s*(\d+)$', l['text'])
                if m and l['size'] > 13: cur = dict(number=f'K-{m[1]}', quiz=int(m[1]), pdf=p, qs=[]); res.append(cur); continue
                if cur is None or not l['font'].startswith('Times') or l['size'] > 10.4 or l['size'] < 9.6 or 'Italic' in l['font'] and l['size'] < 9: continue
                if re.match(r'^(Aircraft Propulsion|©|Companion)', l['text']): continue
                if re.match(r'^\d+\.\s', l['text']): cur['qs'].append(l['text'])
                elif cur['qs']: cur['qs'][-1] += ' ' + l['text']
    return res

def glue_flags(t):
    """signs that the layer lost the '=' / spacing of inline math (Farokhi's text layer places the right-hand side of 'T1 = 288 K' elsewhere)"""
    w = []
    if re.search(r'\b(?:if|and|with|at|is|as|by|to|of|the|for|in|on|that)[A-Z𝜂𝛾𝜌𝜋℘Δ]', t): w.append('spacing lost around inline math')
    STOP = {'at', 'is', 'of', 'to', 'by', 'as', 'in', 'on', 'for', 'from', 'than', 'about', 'over', 'under', 'and', 'with', 'or', 'per', 'rate', 'flow', 'ratio', 'pressure', 'temperature', 'speed', 'mass', 'power', 'thrust', 'velocity', 'area', 'increase', 'decrease', 'factor', 'loss', 'equal', 'between', 'near', 'nearly', 'only', 'up', 'be', 'are', 'was', 'a', 'an', 'the', 'its', 'each', 'every', 'one', 'two', 'number', 'angle', 'is,', 'when', 'above', 'below', 'around', 'after', 'before', 'least', 'most', 'than', 'let', 'use', 'take', 'consider', 'assume', 'assuming', 'having', 'has', 'have', 'got', 'mach', 'of', 'if', 'then', 'that', 'this', 'kg', 'psia', 'm', 's', 'k'}
    for m in re.finditer(r'(?<![\w.])([A-Za-z𝛾𝜂𝜌𝜋𝜃𝜔𝜏𝛼𝛽𝜁][A-Za-z]{0,5}\d?(?:,[A-Za-z.]+)?)\s+\d[\d.,]*\s*(?:K\b|kPa|MPa|Mpa|kg|m\b|J\b|W\b|N\b|s\b|°|◦|%|lbf|lbm|psia|Btu|ft|bar|atm|cm|mm|rpm|deg)', t):
        if m[1].lower() not in STOP: w.append("'=' missing between a symbol and its value (" + m[1] + ')'); break
    if re.search(r'[=≅]\s*$|\b(?:is|are|ratio|of)\s+(?:What|Calculate)\b', t): w.append('equation lost between sentences')
    if re.search(r'[𝛾𝜂𝜌𝜋℘Δ]\S*\s*[=]?\s*$', t): w.append('ends on a symbol without its value')
    return w

def dropped_flags(it, dropped):
    ys = [y for y, _, _ in it['lines']]
    lo, hi = (min(ys), max(ys)) if ys else (0, 0)
    why = []
    prose = [t for y, t, st in dropped if len(t) >= 25 and len(t.split()) >= 3 and not re.match(r'^[A-Za-z]{1,2}\d?\s*[=∕/]', t)]
    math = [t for y, t, st in dropped if st or re.search(r'[=∕]', t)]
    if prose: why.append('prose line(s) of the statement not captured: ' + '; '.join(prose[:2])[:120])
    if math and not it['figcap']: why.append('display formula/table fragments between statement lines not captured')
    if not it['lines']: why.append('no statement lines captured')
    why += glue_flags(join_lines(it['lines']))
    return dict(stix_in_statement=any(st for _, _, st in it['lines']), unreliable_why=why, text_reliable=not why)

def run():
    doc = fitz.open(FAROKHI_PDF); fm = bookmap('farokhi'); res = []
    ent = fm['entries']
    for ch in CHAPS:
        chap = next(e for e in ent if e['kind'] == 'chapter' and e['num'] == str(ch))
        prob = next(e for e in ent if e['kind'] == 'endpart' and e['title'] == 'Problems' and e['chapter'] == str(ch))
        pmods = prob['mods'] or chap['mods']
        for it in parse_problems(doc, ch, prob['pdf'], prob['pdf_end'], None):
            txt = join_lines(it['lines'])
            dropped = [d for d in it['dropped'] if d[1].strip()]
            mm = list(pmods.items())[0] if pmods else ('out', {'role': None, 'basis': ''})
            res.append(dict(source='farokhi', chapter=ch, number=it['number'], kind='problem', part='Problems', suffix='', text=tidy(txt), pdf_page=it['pdf'], printed_page=it['pdf'] - OFFSET,
                            module=mm[0], module_role=mm[1].get('role'), module_basis=f"Farokhi Ch.{ch} Problems: {mm[1].get('basis', '')}" if pmods else f'Farokhi Ch.{ch} has no module', answer_printed=None, has_solution_printed=False,
                            fig_caption=it['figcap'], dropped=[d[1] for d in dropped], **dropped_flags(it, dropped)))
        secs = [e for e in ent if e['kind'] == 'section' and e['chapter'] == str(ch)]
        for ex in parse_examples(doc, ch, chap['pdf'], prob['pdf'] - 1 if prob['pdf'] > chap['pdf'] else chap['pdf_end']):
            s = max([e for e in secs if e['pdf'] <= ex['pdf']], key=lambda e: e['pdf'], default=None)
            mods = (s or chap)['mods'] or chap['mods']
            mm = list(mods.items())[0] if mods else ('out', {'role': None, 'basis': ''})
            res.append(dict(source='farokhi', chapter=ch, number=ex['number'], kind='example', part='Example', suffix='', title=ex['title'], text=ex['text'], pdf_page=ex['pdf'], printed_page=ex['pdf'] - OFFSET, unreliable_why=glue_flags(ex['text']) + (['example statement taken up to its first full stop: may be cut'] if False else []), text_reliable=not glue_flags(ex['text']),
                            module=mm[0], module_role=mm[1].get('role'), module_basis=f"Farokhi §{s['num'] if s else ch} {s['title'] if s else ''}: {mm[1].get('basis', '')}", section=s['num'] if s else None,
                            answer_printed=None, has_solution_printed=True, fig_caption=False, dropped=[], stix_in_statement=False))
    k = next(e for e in ent if e.get('num') == 'App.K')
    for q in parse_quizzes(doc, k['pdf'], k['pdf_end']):
        res.append(dict(source='farokhi', chapter='App.K', number=q['number'], kind='quiz', part='10-Minute Quiz', suffix='', text=tidy(' '.join(q['qs'])), n_questions=len(q['qs']), pdf_page=q['pdf'], printed_page=q['pdf'] - OFFSET,
                        module='?', module_role=None, module_basis='Appendix K quiz: no answers printed, module not assigned in the book map (left to P3)', answer_printed=None, has_solution_printed=False, fig_caption=False, dropped=[], stix_in_statement=False))
    return res

if __name__ == '__main__':
    r = run()
    json.dump(r, open(os.path.join(OUT, 'farokhi_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(sorted(collections.Counter((e['chapter'], e['kind']) for e in r).items(), key=str))
