"""Site data from the catalogue:  exercises/catalog.json (compact table of every exercise, snippets only)  and  written/papers.json (Written Practice papers).
Papers = Jaeger 5e in-text EXERCISES that have a printed answer, belong to a section mapped to a module and need no simulator.
Floyd statements are only indexed (their inline mathematics is not reliably extractable); their printed answers are listed in the finder."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *
sys.path.insert(0, os.path.join(ROOT, 'build'))
from modules import MODS, BYID

cat = json.load(open(os.path.join(OUT, 'catalog.json'), encoding='utf-8'))
FIELDS = ['id', 'book', 'kind', 'chapter', 'section', 'number', 'printed', 'pdf', 'text', 'answer', 'nq', 'numeric', 'figure', 'sim', 'modules', 'in_site', 'cls']
def cut(t, n): t = t or ''; return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'
rows = []
for e in cat:
    r = [e.get(f) for f in FIELDS]
    r[FIELDS.index('text')] = cut(e.get('text') or e.get('title') or '', 190); r[FIELDS.index('answer')] = cut(e.get('answer'), 130)
    r[FIELDS.index('numeric')] = int(bool(e.get('numeric'))); r[FIELDS.index('figure')] = int(bool(e.get('figure'))); r[FIELDS.index('sim')] = int(bool(e.get('sim')))
    r[FIELDS.index('printed')] = str(e.get('printed')) if e.get('printed') is not None else ''
    rows.append(r)
os.makedirs(os.path.join(ROOT, 'exercises'), exist_ok=True)
json.dump(dict(fields=FIELDS, rows=rows), open(os.path.join(ROOT, 'exercises', 'catalog.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

papers = []
for m in MODS:
    mid = m['id']
    items = [e for e in cat if e['book'] == 'jaeger5' and e['kind'] == 'exercise' and mid in e['modules'] and e['answer'] and e['numeric'] and not e.get('sim')]
    if len(items) < 3: continue
    items.sort(key=lambda e: (e['pdf'], e['id']))
    probs = [[dict(text=e['text'], marks=1, answer=e['answer'], ref=f"Jaeger 5e §{e['section']}, p.{e['printed']} (PDF {e['pdf']})", fig=int(bool(e.get('figure'))), page=e['pdf'])] for e in items]
    papers.append(dict(id=f'jaeger-{mid}', module=mid, minutes=max(15, 6 * len(items)),
                       title={'vi': f'{mid.upper()} · {m["vi"]}: bài tập có số của Jaeger (đáp án in sẵn)', 'en': f'{mid.upper()} · {m["en"]}: Jaeger numeric exercises (printed answers)'},
                       note={'vi': 'Mỗi phần là một khung EXERCISE của Jaeger 5e kèm ANSWERS in ngay dưới. Thời gian là giả định của site (6 phút mỗi bài); mỗi bài 1 điểm. Bài có ghi “cần hình” dùng hình vẽ trong sách ở trang đã nêu.',
                             'en': 'Each part is an EXERCISE box of Jaeger 5e with its printed ANSWERS. The time limit is this site\'s assumption (6 minutes per exercise); 1 mark each. Parts marked “figure needed” refer to the figure in the book at the page given.'},
                       problems=probs))
os.makedirs(os.path.join(ROOT, 'written'), exist_ok=True)
json.dump(papers, open(os.path.join(ROOT, 'written', 'papers.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
sz = os.path.getsize(os.path.join(ROOT, 'exercises', 'catalog.json'))
print('catalog rows', len(rows), 'size', sz // 1024, 'KB | papers', [(p['id'], len(p['problems'])) for p in papers])
