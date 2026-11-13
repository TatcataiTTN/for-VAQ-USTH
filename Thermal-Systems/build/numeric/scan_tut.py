"""Tutorials I (lecturer's problem set, 29 slide pages): 8 numbered problems + 2 worked examples without a number (Brayton p.18, R-134a p.24).
Statement text from OCR_output/07_Tutorials_I.md (page = `## [Trang N]`), item list and page numbers from OCR_output/_qa/tut.json (`problems`; checked on all 29 page images in P0, see _qa/tut/QA.md).
The text is cut before the block '**[Đọc trực tiếp từ ảnh slide ...]**' (Vietnamese description of the figure). Source typos of the slides are repaired only for word splits
(effec tive, temper ature ...) and the doubled '(b) (b)'; each repair is listed in `typo_fixed`.
Run: python3 -I build/numeric/scan_tut.py -> data/numeric/tut_raw.json"""
import re, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from common import *

FIXES = [('effec tive', 'effective'), ('effi ciency', 'efficiency'), ('temper ature', 'temperature'), ('com pression', 'compression'), ('com pressor', 'compressor'),
         ('com\npressor', 'compressor'), ('(b) (b)', '(b)'), ('(c) (c)', '(c)'), ('(d) (d)', '(d)'), ('effi ciency', 'efficiency')]
MODULE = {'P1': 'm02', 'P2': 'm02', 'P3': 'm02', 'P4': 'm02', 'P5': 'm02', 'P6': 'm02', 'B': 'm02', 'R': 'm03', 'P7': 'm02', 'P8': 'm02'}
SAME_AS = {'P1': 'Cengel Example 9-2 (same data)', 'P2': 'Cengel Example 9-3 (same data)', 'B Brayton': 'Cengel Example 9-5 (same data)', 'R R134a': 'Cengel Example 11-1 (same data)'}

def run():
    t = open(os.path.join(OCR, '07_Tutorials_I.md'), encoding='utf-8').read()
    pages = {int(m[1]): m[2] for m in re.finditer(r'^## \[Trang (\d+)\]\n(.*?)(?=^---\n|\Z)', t, re.S | re.M)}
    j = json.load(open(os.path.join(OCR, '_qa', 'tut.json'), encoding='utf-8'))
    nr = {}                                                                       # per problem: input/slide values count from tut.json numeric
    for r in j['numeric']: nr.setdefault(r['problem'], []).append(r)
    res = []
    for pr in j['problems']:
        pid = pr['id']; p = pr['page_problem']
        raw = pages[p].split('**[Đọc trực tiếp')[0]
        fixed = []
        for a, b in FIXES:
            if a in raw: raw = raw.replace(a, b); fixed.append(f'{a!r}->{b!r}')
        raw = re.sub(r'^\s*\d+\.\s+', '', raw.strip(), count=1) if re.match(r'^\s*\d+\.\s', raw.strip()) else raw
        # drop the slide title line of the unnumbered examples ('The Simple Ideal Brayton Cycle') and of numbered ones with titles
        lines = [l for l in raw.split('\n') if l.strip()]
        title = ''
        if lines and not re.search(r'[.:,)]$', lines[0]) and len(lines[0]) < 70 and len(lines) > 1: title = lines[0]; lines = lines[1:]
        body = tidy(' '.join(l.strip().lstrip('•').strip() if l.strip().startswith('•') else l.strip() for l in lines))
        body = re.sub(r'^\d+\.\s+', '', body)
        m = re.match(r'^P(\d)', pid); number = m[1] if m else ('Brayton example' if pid.startswith('B') else 'R-134a example')
        key = f'P{m[1]}' if m else pid[0]
        sol = pr['pages_solution']
        res.append(dict(source='tut', chapter='Tutorials I', number=number, kind='problem' if m else 'example', part='Tutorials I', suffix='', title=title or pr['title'], text=body,
                        pdf_page=p, printed_page=p, solution_pages=sol, module=MODULE[key], module_role='core',
                        module_basis='Tutorials I tr.%d: %s (CONTINUE.md: Tutorials I attached to m02 and m03; Brayton/Otto/Diesel -> m02, R-134a -> m03)' % (p, pr['title']),
                        answer_printed=None, has_solution_printed=bool(pr['has_solution']), fig_caption=False, typo_fixed=fixed, same_as=SAME_AS.get(key) or SAME_AS.get(pid),
                        n_slide_values=sum(1 for r in nr.get(pid, []) if r.get('kind') != 'input'), tut_id=pid, slide_figure=('Sơ đồ' in pages[p])))
    return res

if __name__ == '__main__':
    r = run()
    json.dump(r, open(os.path.join(OUT, 'tut_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    for e in r: print(e['number'], e['kind'], e['pdf_page'], e['solution_pages'], e['text'][:90], '|', e['typo_fixed'])
