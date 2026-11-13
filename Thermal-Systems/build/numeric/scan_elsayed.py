"""Scan El-Sayed 2e (EPUB -> OCR_output/11_*.md): end-of-chapter Problems and worked Examples of Ch.1, 2, 3, 4, 9, 10, 11.
Text is the pandoc conversion of the EPUB xhtml (MathML -> LaTeX): characters reliable. Markdown list numbering ('1.', 'a.') is pandoc's own renumbering of the printed (a), (b)...: it is kept as written
but flagged in `list_markers`. Printed page = the last marker ⟦p.N⟧ seen before the item. Figure OCR lines '*[Hình `x.jpg` ...]*' are removed from the statement and set needs_figure; table images likewise.
Run: python3 -I build/numeric/scan_elsayed.py -> data/numeric/elsayed_raw.json"""
import re, os, sys, json, collections, glob
sys.path.insert(0, os.path.dirname(__file__))
from common import *

CHAPS = (1, 2, 3, 4, 9, 10, 11)
FIGLINE = re.compile(r'^\*\[(Hình|Bảng)\s*`([^`]+)`[^\]]*\]\*$')
PAGE = re.compile(r'⟦p\.([ivxlcdm\d]+)⟧')

def clean(t):
    t = re.sub(r'\*\*\[Bảng dạng ảnh `[^`]+`[^\]]*\]\*\*\s*```text\s*(.*?)```', lambda m: '[TABLE (image OCR): ' + re.sub(r'\s{2,}', ' | ', m[1].strip()) + ']', t, flags=re.S)
    t = re.sub(r'\[([^\]]+)\]\(#[^)]*\)(\{[^}]*\})?', r'\1', t)
    t = re.sub(r'-{4,}(?: +-{4,})*', ' ', t)
    t = PAGE.sub(' ', t)
    t = t.replace('\\hspace{0pt}', '')
    t = re.sub(r'~\*?([^~\s]{1,12})\*?~', r'_\1', t)
    t = re.sub(r'\^([^\^\s]{1,10})\^', r'^\1', t)
    t = t.replace('*', '')
    return tidy(re.sub(r'\s*\n\s*', ' ', t))

def items_of(lines, start, end):
    """-> list of (number, first_text, extra_lines, line_index_of_start) for **c.n** items between line numbers start..end (0-based, end excl.)"""
    out = []; cur = None
    for i in range(start, end):
        l = lines[i]
        m = re.match(r'^\*\*(\d{1,2})\.(\d{1,3})\*\*\s*(.*)$', l)
        if m: cur = dict(chapter=int(m[1]), n=int(m[2]), first=m[3], rest=[], i=i); out.append(cur); continue
        if cur is not None: cur['rest'].append(l)
    return out

def page_at(lines, i):
    for k in range(i, -1, -1):
        m = PAGE.findall(lines[k])
        if m: return m[-1]
    return None

def run():
    md = open(os.path.join(OCR, '11_ElSayed_Aircraft_Propulsion_and_Gas_Turbine_Engines.md'), encoding='utf-8').read().split('\n')
    em = bookmap('elsayed'); res = []
    for ch in CHAPS:
        chap = next(e for e in em['entries'] if e['kind'] == 'chapter' and e['chapter'] == ch)
        prob = next(e for e in em['entries'] if e['kind'] == 'endpart' and e['title'] == 'Problems' and e['chapter'] == ch)
        ref = next(e for e in em['entries'] if e['kind'] == 'endpart' and e['title'] == 'References' and e['chapter'] == ch)
        mods = prob.get('mods') or chap.get('mods') or {}
        mm = next(iter(mods.items())) if mods else ('out', {'role': None, 'basis': ''})
        # problems: heading line md_line is 1-based
        for it in items_of(md, prob['md_line'], ref['md_line'] - 1):
            blk = [it['first']] + it['rest']; figs = []; txt = []
            for l in blk:
                if not l.strip(): continue
                mf = FIGLINE.match(l.strip())
                if mf: figs.append(mf[2]); continue
                txt.append(l.rstrip())
            body = clean('\n'.join(txt))
            res.append(dict(source='elsayed', chapter=ch, number=f"{ch}.{it['n']}", kind='problem', part='Problems', suffix='', text=body, pdf_page=None, printed_page=page_at(md, it['i']),
                            module=mm[0], module_role=mm[1].get('role'), module_basis=f"El-Sayed Ch.{ch} Problems: {mm[1].get('basis', mm[1].get('status', ''))}" if mods else f'El-Sayed Ch.{ch} not mapped',
                            answer_printed=None, has_solution_printed=False, fig_caption=bool(figs), figure_files=figs, list_markers=bool(re.search(r'(?:^|\s)(?:\d+|[a-z])\.\s', ' '.join(txt))),
                            md_line=it['i'] + 1))
        # examples
        for ex in [e for e in em['examples'] if e['chapter'] == ch]:
            i = ex['md_line'] - 1
            assert md[i].strip().startswith('Example'), (ex, md[i])
            j = i + 1; txt = []; figs = []
            while j < len(md) and not re.match(r'^(Solution|\*\*Solution|Solution:)\b', md[j].strip()) and j < i + 60 and not md[j].startswith('## ') and not re.match(r'^Example \d', md[j].strip()):
                l = md[j].strip(); j += 1
                if not l: continue
                mf = FIGLINE.match(l)
                if mf: figs.append(mf[2]); continue
                txt.append(l.rstrip())
            has_sol = j < len(md) and md[j].strip().startswith(('Solution', '**Solution'))
            res.append(dict(source='elsayed', chapter=ch, number=ex['num'], kind='example', part='Example', suffix='', text=clean('\n'.join(txt)), pdf_page=None, printed_page=ex['printed'],
                            module=mm[0], module_role=mm[1].get('role'), module_basis=f"El-Sayed Ch.{ch}: {mm[1].get('basis', mm[1].get('status', ''))}" if mods else f'El-Sayed Ch.{ch} not mapped',
                            answer_printed=None, has_solution_printed=has_sol, fig_caption=bool(figs), figure_files=figs, list_markers=False, md_line=ex['md_line']))
    return res

if __name__ == '__main__':
    r = run()
    json.dump(r, open(os.path.join(OUT, 'elsayed_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(sorted(collections.Counter((e['chapter'], e['kind']) for e in r).items()))
    for ch in CHAPS:
        n = [int(e['number'].split('.')[1]) for e in r if e['chapter'] == ch and e['kind'] == 'problem']
        print(ch, len(n), 'max', max(n) if n else None, 'missing', [k for k in range(1, (max(n) if n else 0) + 1) if k not in n], 'dup', [k for k, c in collections.Counter(n).items() if c > 1])
