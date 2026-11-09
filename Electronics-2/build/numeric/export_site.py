"""Site data from the catalogue:  exercises/catalog.json (compact table of every exercise, snippets only)  and  written/papers.json (Written Practice papers).
Papers: (1) Jaeger 5e in-text EXERCISES with a printed answer, (2) Floyd 9e end-of-chapter Problems with a printed answer (odd-numbered; statements rebuilt from the characters, see
floyd_text.py), (3) Jaeger Problems without a printed answer that this site solved and checked, (4) Floyd Examples / Related Problems / Section Checkups / even Problems and Jaeger Examples that this site solved and checked (build/numeric/csol).  Floyd problems that need a Multisim file or whose answer is a figure are left out."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *
sys.path.insert(0, os.path.join(ROOT, 'build'))
from modules import MODS, BYID

cat = json.load(open(os.path.join(OUT, 'catalog.json'), encoding='utf-8'))
FIELDS = ['id', 'book', 'kind', 'chapter', 'section', 'number', 'printed', 'pdf', 'text', 'answer', 'nq', 'numeric', 'figure', 'sim', 'modules', 'in_site', 'cls', 'ans_kind', 'skip']
def cut(t, n): t = t or ''; return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'
rows = []
for e in cat:
    r = [e.get(f) for f in FIELDS]
    r[FIELDS.index('text')] = cut(e.get('text') or e.get('title') or '', 190); r[FIELDS.index('answer')] = cut(e.get('answer'), 260 if e.get('ans_kind') == 'computed' else 130)
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
    papers.append(dict(id=f'jaeger-{mid}', module=mid, group='jaeger-box', minutes=max(15, 6 * len(items)),
                       title={'vi': f'{mid.upper()} · {m["vi"]}: bài tập có số của Jaeger (đáp án in sẵn)', 'en': f'{mid.upper()} · {m["en"]}: Jaeger numeric exercises (printed answers)'},
                       note={'vi': 'Mỗi phần là một khung EXERCISE của Jaeger 5e kèm ANSWERS in ngay dưới. Thời gian là giả định của site (6 phút mỗi bài); mỗi bài 1 điểm. Bài có ghi “cần hình” dùng hình vẽ trong sách ở trang đã nêu.',
                             'en': 'Each part is an EXERCISE box of Jaeger 5e with its printed ANSWERS. The time limit is this site\'s assumption (6 minutes per exercise); 1 mark each. Parts marked “figure needed” refer to the figure in the book at the page given.'},
                       problems=probs))
CHUNK = 12                                                          # at most 12 problems per paper
for m in MODS:                                                      # Floyd end-of-chapter problems with a printed answer
    mid = m['id']
    items = [e for e in cat if e['book'] == 'floyd' and e['kind'] == 'problem' and mid in e['modules'] and e.get('answer') and e.get('ans_kind') == 'printed'
             and not re.search(r'Open file|Multisim file|Open the Multisim', e['text']) and not re.search(r'Figure ANS|See Figure ANS', e['answer'])]
    if len(items) < 3: continue
    items.sort(key=lambda e: (e['chapter'], int(e['number'])))
    k = -(-len(items) // CHUNK); size = -(-len(items) // k)
    for j in range(k):
        part = items[j * size:(j + 1) * size]
        probs = [[dict(text=e['text'], marks=1, answer=e['answer'], ref=f"Floyd 9e Ch.{e['chapter']} Problem {e['number']}, p.{e['printed']} (PDF {e['pdf']})", fig=int(bool(e.get('figure'))), page=e['pdf'])] for e in part]
        tag_vi = f' · phần {j + 1}/{k}' if k > 1 else ''; tag_en = f' · part {j + 1} of {k}' if k > 1 else ''
        papers.append(dict(id=f'floyd-{mid}' + (f'-{j + 1}' if k > 1 else ''), module=mid, group='floyd', minutes=max(15, 6 * len(part)),
                           title={'vi': f'{mid.upper()} · {m["vi"]}: problem cuối chương của Floyd (đáp án in){tag_vi}', 'en': f'{mid.upper()} · {m["en"]}: Floyd end-of-chapter problems (printed answers){tag_en}'},
                           note={'vi': 'Problem cuối chương của Floyd 9e có đáp án in ở phụ lục (chỉ các bài số lẻ), chương ' + ', '.join(sorted({str(e['chapter']) for e in part}, key=int)) + '. Bài cần mở file Multisim hoặc có đáp án là hình vẽ đã được bỏ. Thời gian là giả định của site (6 phút mỗi bài); mỗi bài 1 điểm. Bài ghi “cần hình” dùng hình của sách ở trang đã nêu; đáp án chỉ có kết quả cuối, cách làm bạn tự viết.',
                                 'en': 'End-of-chapter problems of Floyd 9e whose answer is printed in the appendix (odd-numbered only), chapter ' + ', '.join(sorted({str(e['chapter']) for e in part}, key=int)) + '. Problems that need a Multisim file or whose answer is a figure are left out. The time limit is this site\'s assumption (6 minutes per problem); 1 mark each. Parts marked “figure needed” use the book\'s figure at the page given; the answer is the final result only, you write the working yourself.'},
                           problems=probs))
for m in MODS:                                                      # problems without a printed answer, solved and checked by this site
    mid = m['id']
    items = [e for e in cat if e['book'] == 'jaeger5' and e['kind'] == 'problem' and mid in e['modules'] and e.get('ans_kind') == 'computed']
    if len(items) < 3: continue
    items.sort(key=lambda e: (e['pdf'], [int(x) for x in e['number'].split('.')]))
    probs = [[dict(text=e['text'], marks=1, answer=e['parts'], how=e['how'], assume=e['assume'], ref=f"Jaeger 5e Problem {e['number']}, p.{e['printed']} (PDF {e['pdf']})", fig=int(bool(e.get('figure'))), page=e['pdf'], computed=1)] for e in items]
    papers.append(dict(id=f'jaeger-prob-{mid}', module=mid, group='jaeger-solved', minutes=max(20, 8 * len(items)),
                       title={'vi': f'{mid.upper()} · {m["vi"]}: problem Jaeger không có đáp án in (site tự giải và kiểm)', 'en': f'{mid.upper()} · {m["en"]}: Jaeger problems without a printed answer (solved and checked by this site)'},
                       note={'vi': 'Sách không in đáp án các problem này. Đáp án do site tính theo công thức của chính sách và kiểm lại bằng một cách độc lập (mô phỏng số, mạch chính xác, FFT, nghiệm đa thức…); phần “Giả định” ghi chỗ đề chưa nói rõ. Thời gian là giả định (8 phút mỗi bài).',
                             'en': 'The book prints no answer for these problems. The answers were computed by this site with the book\'s own formulas and re-checked by an independent route (numerical simulation, exact circuit solution, FFT, polynomial roots…); the “Assumptions” lines state what the statement leaves open. The time limit is an assumption (8 minutes per problem).'},
                       problems=probs))
KLAB = {'circuit_action': ('Circuit Action', 'Circuit Action'), 'checkup': ('Section Checkup', 'Section Checkup'), 'example': ('Example', 'Example'), 'related_problem': ('Related Problem của Example', 'Related Problem of Example'), 'problem': ('Problem', 'Problem')}
KORD = {'example': 0, 'related_problem': 1, 'checkup': 2, 'circuit_action': 3, 'problem': 4}
def sortkey(e): return (e['book'], e['chapter'] or 0, KORD.get(e['kind'], 9), [int(x) if x.isdigit() else 0 for x in re.split(r'[–.\-]', str(e['number']))])
FIGS = json.load(open(os.path.join(OUT, 'figs.json'), encoding='utf-8')) if os.path.exists(os.path.join(OUT, 'figs.json')) else {}
def figs_of(e):                                       # the book figures the circuit description names (cut out by build/numeric/figexport.py)
    if not e.get('circuit'): return []
    head = re.split(r'\(pp?\.|:', e['circuit'], 1)[0]; return [FIGS[l] for l in dict.fromkeys(re.findall(r'\d+–\d+', head)) if l in FIGS]
def ctx_of(e):                                        # a Related Problem refers to its Example: print the Example statement with it
    if e.get('ctx'): return e['ctx']
    if e['kind'] == 'related_problem':
        ex = next((x for x in cat if x['book'] == e['book'] and x['kind'] == 'example' and x['chapter'] == e['chapter'] and x['number'] == e['number']), None)
        if ex: return f"Example {e['number']}: {ex['text']}"
    return None
for m in MODS:                                                      # book calculations without a printed answer: Examples, Related Problems, Checkups, even Problems
    mid = m['id']
    items = [e for e in cat if e.get('calc') and mid in e['modules']]
    if not items: continue
    items.sort(key=sortkey)
    k = -(-len(items) // CHUNK); size = -(-len(items) // k)
    for j in range(k):
        part = items[j * size:(j + 1) * size]
        def ref(e):
            if e['book'] == 'floyd': return f"Floyd 9e Ch.{e['chapter']} {KLAB[e['kind']][1]} {e['number']}, p.{e['printed']} (PDF {e['pdf']})"
            return f"Jaeger 5e Example {e['number']}, p.{e['printed']} (PDF {e['pdf']})"
        probs = [[dict(text=e['text'], ctx=ctx_of(e), marks=1, answer=e['parts'], how=e['how'], assume=e['assume'], ref=ref(e), fig=0, page=e['pdf'], computed=1, circuit=e.get('circuit'), figs=figs_of(e))] for e in part]
        tag_vi = f' · phần {j + 1}/{k}' if k > 1 else ''; tag_en = f' · part {j + 1} of {k}' if k > 1 else ''
        papers.append(dict(id=f'calc-{mid}' + (f'-{j + 1}' if k > 1 else ''), module=mid, group='calc-solved', minutes=max(15, 6 * len(part)),
                           title={'vi': f'{mid.upper()} · {m["vi"]}: bài tính trong sách không có đáp án in (site tự giải và kiểm){tag_vi}', 'en': f'{mid.upper()} · {m["en"]}: book calculations without a printed answer (solved and checked by this site){tag_en}'},
                           note={'vi': 'Example, Related Problem, Section Checkup và problem chẵn của Floyd, Example của Jaeger: sách không in đáp án các bài này (đáp án Related Problem của Floyd nằm trên website nhà xuất bản). Đáp án do site tính theo công thức của chính sách và kiểm lại bằng một cách độc lập; với Example, kết quả còn được so với lời giải in trong sách. Related Problem được kèm đề của Example mà nó dựa vào. Thời gian là giả định (6 phút mỗi bài).',
                                 'en': 'Floyd Examples, Related Problems, Section Checkups and even-numbered Problems, and Jaeger Examples: the book prints no answer for these (Floyd\'s Related Problem answers are on the publisher\'s website). The answers were computed by this site with the book\'s own formulas and re-checked by an independent route; for the Examples the result is also compared with the worked solution printed in the book. A Related Problem is shown with the statement of the Example it builds on. The time limit is an assumption (6 minutes per exercise).'},
                           problems=probs))
os.makedirs(os.path.join(ROOT, 'written'), exist_ok=True)
json.dump(papers, open(os.path.join(ROOT, 'written', 'papers.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
sz = os.path.getsize(os.path.join(ROOT, 'exercises', 'catalog.json'))
print('catalog rows', len(rows), 'size', sz // 1024, 'KB | papers', [(p['id'], len(p['problems'])) for p in papers])
