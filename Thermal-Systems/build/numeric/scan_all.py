"""Merge the four scans into data/numeric/catalog.json (+ summary.json). Run: python3 -I build/numeric/scan_{cengel,farokhi,elsayed,tut}.py && python3 -I build/numeric/scan_all.py
No problem is solved here: flags describe the printed statement only. `class` decision order is in common.classify()."""
import os, sys, json, re, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import *

def load(n): return json.load(open(os.path.join(OUT, n), encoding='utf-8'))
FORMULA = re.compile(r'[∂∫Σ√]|\bsqrt\b')

def prepare(e):
    e = dict(e)
    why = list(e.pop('unreliable_why', []) or [])
    if e['source'] == 'cengel':
        if FORMULA.search(e['text']): why.append('formula fragment (partial derivative / root / sum) in the statement: layout lost')
        if re.search(r'\b(?:rate|power)\b', e['text']) and re.search(r'\bkg/s\b|\bkW\b|\bkJ/s\b|\blbm/s\b', e['text']) and False: pass
    if e['source'] == 'elsayed' and 'TABLE (image OCR)' in e['text']: why.append('table taken from an image by OCR (less reliable): check the image')
    if e['source'] == 'elsayed' and e.get('list_markers'): pass
    e['unreliable_why'] = why
    if why: e['text_reliable'] = False
    e.setdefault('text_reliable', True)
    return e

def build():
    raw = load('cengel_raw.json') + load('farokhi_raw.json') + load('elsayed_raw.json') + load('tut_raw.json')
    cat = []
    for e in raw:
        e = finalize(prepare(e))
        cat.append(e)
    # ids must be unique and stable: collisions (identical text) get a suffix by (source, number)
    seen = collections.Counter(e['id'] for e in cat)
    for e in cat:
        if seen[e['id']] > 1: e['id'] = make_id(e['source'], e['kind'], e['chapter'], e['number'] + '#' + str(e['pdf_page']), e['text'] + e['number'])
    keep = ('id', 'source', 'chapter', 'number', 'kind', 'part', 'text', 'pdf_page', 'printed_page', 'module', 'module_role', 'module_basis', 'answer_printed', 'has_solution_printed', 'numeric', 'needs_figure', 'needs_table',
            'needs_chart', 'english_units', 'concept', 'text_reliable', 'class', 'class_reason', 'unreliable_why', 'nq', 'n_numbers', 'figure_basis', 'table_basis', 'chart_basis', 'asks_diagram', 'software', 'refers_to',
            'title', 'section', 'section_heading', 'suffix', 'solution_pages', 'same_as', 'typo_fixed', 'figure_files', 'n_questions', 'modules_all', 'md_line')
    out = [{k: e[k] for k in keep if k in e} for e in cat]
    return out

def summarize(cat):
    by = collections.defaultdict(lambda: collections.Counter())
    for e in cat:
        k = f"{e['source']}|{e['chapter']}|{e['kind']}"
        by[k]['total'] += 1; by[k][e['class']] += 1
        by[k]['answer_printed'] += bool(e['answer_printed']); by[k]['numeric'] += e['numeric']; by[k]['text_reliable_false'] += (not e['text_reliable'])
    tot_src = collections.Counter(e['source'] for e in cat)
    cls = collections.Counter(e['class'] for e in cat)
    return dict(total=len(cat), by_source=dict(tot_src), by_class=dict(cls), by_source_chapter_kind={k: dict(v) for k, v in sorted(by.items())},
                by_source_class={s: dict(collections.Counter(e['class'] for e in cat if e['source'] == s)) for s in tot_src},
                by_module={m: dict(collections.Counter(e['class'] for e in cat if e['module'] == m)) for m in sorted(set(e['module'] for e in cat))})

if __name__ == '__main__':
    cat = build()
    json.dump(cat, open(os.path.join(OUT, 'catalog.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    s = summarize(cat); json.dump(s, open(os.path.join(OUT, 'summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('total', s['total'], s['by_source']); print('by class', s['by_class'])
    for k, v in s['by_source_chapter_kind'].items(): print(k, v)
