"""Scan the end-of-chapter Problems and the printed Examples of Cengel & Boles 5e, chapters 9, 11, 14 (catalog only), 15, 17.

TEXT comes from the repaired layer OCR_output/09b_Cengel_repaired_chapters.md (`## [Trang N]` = PDF page; printed = PDF - 26): its lines are the PDF text lines
one for one (checked on all 243 pages of the five chapters: same line count), so line k of the page in 09b = line k of PyMuPDF's text of that page.
LAYOUT (reading order, what is a number / heading / answer / figure label) comes from the PDF itself through font, size and colour, because the text layer lists the
blocks of a page out of reading order (a left-column statement can continue at the top of the right column that the stream gives first):
    problem number   Times-Bold 9.5, pink        "9-96", "9-10C", "9-17E"
    statement        Times-Roman 9.5
    printed answer   TradeGothic-Oblique 8, or inline in the last line of the statement ("Answers: (a) ..., (b) ...")
    sub-heading, part heading, figure caption   TradeGothic-Bold 10, pink  ("Otto Cycle", "Review Problems", "FIGURE P9-84")
    figure labels    any other font or size (ignored)
    Example          heading TradeGothic-BoldOblique pink "EXAMPLE 9-2" + title TradeGothic-Bold pink on the same row, statement TradeGothic 9, then the label "Solution"
Run: python3 -I build/numeric/scan_cengel.py   ->  data/numeric/cengel_raw.json"""
import re, os, sys, json, collections
import fitz
sys.path.insert(0, os.path.dirname(__file__))
from common import *
fitz.TOOLS.mupdf_display_errors(False)

CHAPTERS = (9, 11, 14, 15, 17)
OFFSET = 26
PARTS = {'PROBLEMS': 'Problems', 'PROBLEMS*': 'Problems', 'Review Problems': 'Review Problems', 'Fundamentals of Engineering (FE) Exam Problems': 'FE', 'Design and Essay Problems': 'Design and Essay'}
PART_FULL = {'Problems': 'PROBLEMS', 'Review Problems': 'Review Problems', 'FE': 'Fundamentals of Engineering (FE) Exam Problems', 'Design and Essay': 'Design and Essay Problems'}
NUMLINE = re.compile(r'^(\d{1,2})\s?[–-]\s?(\d{1,3})\s?([CE])?$')
EXLINE = re.compile(r'^EXAMPLE\s+(\d{1,2})\s?[–-]\s?(\d{1,2})$')
ANS = re.compile(r'\bAnswers?:\s*')
PINK = (0xec008c, 0xec078d)

def load_md():
    t = open(os.path.join(OCR, '09b_Cengel_repaired_chapters.md'), encoding='utf-8').read()
    pages = {}
    for m in re.finditer(r'^## \[Trang (\d+)\]\n(.*?)(?=^---\n|\Z)', t, re.S | re.M): pages[int(m[1])] = [l for l in m[2].split('\n') if l.strip()]
    return pages, t

def vocab(full):
    joined = collections.Counter(re.findall(r'(?<![\w-])[a-z]{3,}(?![\w-])', full))
    hyph = collections.Counter(re.findall(r'(?<![\w-])[a-z]{2,}-[a-z]{2,}(?![\w-])', full))
    return joined, hyph

def join(lines, joined, hyph):
    out = ''
    for l in lines:
        l = l.strip()
        if not l: continue
        if re.search(r'[a-z]-$', out) and re.match(r'^[a-z]', l):
            a = re.search(r'([a-z]+)-$', out).group(1); b = re.match(r'^([a-z]+)', l).group(1)
            out = out[:-1] + ('-' if hyph[f'{a}-{b}'] > joined[a + b] else '') + l
        elif re.search(r'[A-Za-z]-$', out) and re.match(r'^[A-Za-z]', l) and not re.search(r'\d-$', out): out += l
        else: out += (' ' if out else '') + l
    return re.sub(r'\s+', ' ', out).strip()

def page_events(doc, pages, p):
    """reading-ordered, classified lines of PDF page p, with the repaired text"""
    md = pages[p]; ev = []; k = 0
    for b in doc[p - 1].get_text('dict')['blocks']:
        if b['type'] != 0: continue
        for l in b['lines']:
            sp = [s for s in l['spans'] if s['text'].strip()]
            raw = ''.join(s['text'] for s in l['spans'])
            if not raw.strip(): continue
            txt = md[k].strip(); k += 1
            if not sp: continue
            dom = max(sp, key=lambda s: len(s['text'].strip()))
            f, sz, col = dom['font'], dom['size'], dom['color']
            x0, y0 = l['bbox'][0], dom['origin'][1]                                    # baseline: stable on one row (bbox tops differ with the glyph mix)
            if y0 < 58: continue                                                          # running heads (chapter/page number)
            if txt == 'Solution' and f.startswith('TradeGothic-Bold') and col in PINK: kind = 'solution'
            elif f.startswith('Times-Bold') and abs(sz - 9.5) < 0.3 and col in PINK and NUMLINE.match(txt): kind = 'num'
            elif col == 0xec078d and sz < 8.6: kind = 'ans'                                  # printed answers: pink (slightly different pink), 8 pt, all spans
            elif f.startswith('TradeGothic-Bold') and not f.startswith('TradeGothic-BoldOb') and sz >= 9.9 and col in PINK: kind = 'head'
            elif f.startswith('TradeGothic-BoldOblique') and col in PINK and EXLINE.match(txt): kind = 'exhead'
            elif f.startswith('Times') and abs(sz - 9.5) < 0.3 and col not in PINK: kind = 'body'
            elif f == 'TradeGothic' and abs(sz - 9.0) < 0.3: kind = 'exbody'
            else: kind = 'other'
            ev.append(dict(kind=kind, text=txt, x0=x0, y0=y0, page=p, font=f, size=sz))
    assert k == len(md), (p, k, len(md))
    thr = 300 if p % 2 else 280                                                         # odd printed pages: columns at x = 59 / 314; even: 35 / 290
    ev.sort(key=lambda e: (0 if e['x0'] < thr else 1, e['y0'], e['x0']))
    out = []; row = []                                                                     # rows: events of one column whose baselines differ by < 1.8 pt, left to right
    for e in ev:
        if row and (row[-1]['x0'] < thr) == (e['x0'] < thr) and abs(e['y0'] - row[0]['y0']) < 1.8: row.append(e)
        else:
            out += sorted(row, key=lambda z: z['x0']); row = [e]
    out += sorted(row, key=lambda z: z['x0']); ev = out
    return ev

def parse_problems(c, doc, pages, joined, hyph):
    ch = c['num']
    p0 = next(e['pdf'] for e in c['end_parts'] if e['name'] == 'PROBLEMS'); p1 = c['pdf_end']
    items = []; cur = None; part = 'Problems'; heading = ''; pend_head = []; figs = set(); started = False
    for p in range(p0, p1 + 1):
        for e in page_events(doc, pages, p):
            k, t = e['kind'], e['text']
            if k == 'num':
                m = NUMLINE.match(t)
                if int(m[1]) != ch: continue
                if not started and int(m[2]) != 1: continue
                started = True
                heading = ' '.join(pend_head) if pend_head else heading; pend_head = []
                cur = dict(num=int(m[2]), suffix=m[3] or '', number=f'{ch}–{m[2]}{m[3] or ""}', pdf=p, part=part, section_heading=heading, _blk=[]); items.append(cur); continue
            if not started: continue
            if k == 'head':
                if t in PARTS: part = PARTS[t]; pend_head = []; heading = ''; continue
                mf = re.match(r'^FIGURE P\s?(\d+)\s?[–-]\s?(\d+)', t)
                if mf: figs.add(f'{mf[1]}–{mf[2]}'); continue
                pend_head.append(t); continue
            if k in ('body', 'ans') and cur is not None: cur['_blk'].append(t)
    for it in items:
        txt = join(it['_blk'], joined, hyph)
        m = ANS.search(txt)
        it['text'] = tidy(txt[:m.start()] if m else txt); it['answer_printed'] = tidy(txt[m.end():]) if m else None
        it['fig_caption'] = it['number'] in figs or it['number'].rstrip('CE') in {f.rstrip('CE') for f in figs}
        del it['_blk']
    return items

def parse_examples(c, doc, pages, joined, hyph):
    ch = c['num']; p0 = c['pdf']; summ = next(e['pdf'] for e in c['end_parts'] if e['name'] == 'SUMMARY')
    out = []; cur = None
    for p in range(p0, summ + 1):
        evs = page_events(doc, pages, p)
        for e in evs:
            k, t = e['kind'], e['text']
            if k == 'exhead':
                m = EXLINE.match(t)
                if int(m[1]) == ch:
                    # the title stands to the right of the label on the same row (it can lie beyond the column limit used for reading order) and may wrap to a second row
                    tl = sorted([z for z in evs if z['kind'] == 'head' and not z['text'].startswith('FIGURE') and z['x0'] >= e['x0'] - 1 and -3 <= z['y0'] - e['y0'] <= 16], key=lambda z: (z['y0'], z['x0']))
                    cur = dict(number=f'{ch}–{m[2]}', pdf=p, y=e['y0'], x0=e['x0'], title=tidy(' '.join(z['text'] for z in tl)), _blk=[], has_sol=False, closed=False); out.append(cur)
                else: cur = None
                continue
            if cur is None or cur['closed']: continue
            if k == 'solution': cur['has_sol'] = True; cur['closed'] = True; continue
            if k == 'exbody': cur['_blk'].append(t); continue
            if k == 'num': cur['closed'] = True                                                    # a problem number: the Problems section began
    res = []
    for ex in out:
        res.append(dict(number=ex['number'], title=ex['title'], text=tidy(join(ex['_blk'], joined, hyph)), pdf=ex['pdf'], has_solution_printed=ex['has_sol']))
    return res

def section_of(c, pdf):
    best = None
    for s in c['sections']:
        if s['pdf'] <= pdf and (best is None or s['pdf'] >= best['pdf']): best = s
    return best

ORDER = {'core': 0, 'ref': 1, 'background': 2, 'optional': 3}
def mods_of(mods):
    return [dict(module=m, role=v['role']) for m, v in sorted(mods.items(), key=lambda kv: (ORDER.get(kv[1]['role'], 9), kv[0]))]

WORDS = lambda s: set(w for w in re.findall(r'[a-z]{3,}', s.lower()) if w not in ('and', 'the', 'for', 'with', 'its', 'cycle', 'cycles', 'systems'))
def section_for_heading(c, heading):
    """sub-heading above a problem -> section of the chapter when the heading names exactly one section (word overlap), else None"""
    if not heading: return None
    hw = WORDS(heading); best = None; bs = 0
    for s in c['sections']:
        sw = WORDS(s['title'])
        if not sw: continue
        sc = len(hw & sw) / len(sw)
        if sc > bs: best, bs = s, sc
    return best if bs >= 0.6 and len(hw) <= 6 else None

def run():
    doc = fitz.open(CENGEL_PDF); pages, full = load_md(); joined, hyph = vocab(full)
    cm = bookmap('cengel'); res = []
    for c in cm['chapters']:
        if c['num'] not in CHAPTERS: continue
        parts = {e['name']: e for e in c['end_parts']}
        for it in parse_problems(c, doc, pages, joined, hyph):
            pname = PART_FULL[it['part']]; pm = mods_of(parts[pname]['mods'])
            sec = section_for_heading(c, it['section_heading'])
            if sec and sec.get('mods') and it['part'] == 'Problems':
                sm = mods_of(sec['mods']); pm = sm; basis = f"Cengel Ch.{c['num']} sub-heading '{it['section_heading']}' ~ §{sec['num']} {sec['title']}: {sec['mods'][sm[0]['module']]['basis']}"
            else: basis = f"Cengel Ch.{c['num']} {pname}: {parts[pname]['mods'][pm[0]['module']]['basis']}"
            res.append(dict(source='cengel', chapter=c['num'], number=it['number'], kind='problem', part=it['part'], suffix=it['suffix'], section_heading=it['section_heading'], section=sec['num'] if sec else None,
                            text=it['text'], pdf_page=it['pdf'], printed_page=it['pdf'] - OFFSET, module=pm[0]['module'], module_role=pm[0]['role'], modules_all=pm, module_basis=basis,
                            answer_printed=it['answer_printed'], has_solution_printed=False, fig_caption=it['fig_caption']))
        for ex in parse_examples(c, doc, pages, joined, hyph):
            s = section_of(c, ex['pdf']); sm = mods_of(s['mods']) if s.get('mods') else []
            res.append(dict(source='cengel', chapter=c['num'], number=ex['number'], kind='example', part='Example', suffix='', title=ex['title'], text=ex['text'], pdf_page=ex['pdf'], printed_page=ex['pdf'] - OFFSET,
                            module=sm[0]['module'] if sm else 'out', module_role=sm[0]['role'] if sm else None, modules_all=sm,
                            module_basis=(f"section {s['num']} {s['title']}: {s['mods'][sm[0]['module']]['basis']}" if sm else f"section {s['num']} has no module"), section=s['num'],
                            answer_printed=None, has_solution_printed=ex['has_solution_printed'], fig_caption=False, section_heading=''))
    return res

if __name__ == '__main__':
    r = run()
    json.dump(r, open(os.path.join(OUT, 'cengel_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    c = collections.Counter((e['chapter'], e['kind']) for e in r); print(sorted(c.items()))
    a = collections.Counter(e['chapter'] for e in r if e['answer_printed']); print('answers', sorted(a.items()))
