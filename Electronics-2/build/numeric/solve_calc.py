"""Run every solver of build/numeric/csol (each asserts its own independent check; Examples are also compared with the book's printed solution) and write
data/numeric/calc_solved.json.  Exit status 1 if a solver fails or a calculation exercise of the modules is neither solved nor skipped with a reason.
Candidates = numeric, mapped to a module, no figure, no simulator, not already in the question bank, no printed answer, and not a Jaeger end-of-chapter problem (those are in jsol).
Run: python3 -I build/numeric/solve_calc.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'csol')); sys.path.insert(0, HERE)
import floyd, floyd_fig, jaeger
from core import REG
from skipped import SKIP
from common import OUT
cat = json.load(open(os.path.join(OUT, 'catalog.json'), encoding='utf-8'))
def key(e): return (e['book'], e['kind'], str(e['chapter']), str(e['number']))
by = {key(e): e for e in cat if e['book'] in ('floyd', 'jaeger5')}
cands = [e for e in cat if e.get('numeric') and e['modules'] and not e.get('figure') and not e.get('sim') and not e['in_site'] and e.get('ans_kind') != 'printed'
         and not (e['book'] == 'jaeger5' and e['kind'] == 'problem') and not (e['book'] == 'easa') and e['kind'] != 'exercise']
solved = {}; fails = []
for k in sorted(REG):
    try: r = REG[k](); parts, how, assume = r[0], r[1], r[2]; ctx = r[3] if len(r) > 3 else None; circuit = r[4] if len(r) > 4 else None
    except Exception as ex: fails.append((k, type(ex).__name__, str(ex)[:160])); continue
    e = by.get(k)
    if e is None: fails.append((k, 'no such exercise in the catalog', '')); continue
    solved['|'.join(k)] = dict(book=k[0], kind=k[1], chapter=k[2], number=k[3], modules=e['modules'], pdf=e['pdf'], printed=e['printed'], parts=[[a, b] for a, b in parts], how=how, assume=assume, ctx=ctx, circuit=circuit)
miss = [key(e) for e in cands if key(e) not in REG and key(e) not in SKIP]
bad_skip = [k for k in SKIP if k not in by]
json.dump(dict(solved=solved, skipped={'|'.join(k): dict(reason=r, modules=by[k]['modules'], pdf=by[k]['pdf']) for k, r in SKIP.items() if k in by}), open(os.path.join(OUT, 'calc_solved.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('candidates', len(cands), '| solved', len(solved), '| skipped with a reason', len(SKIP), '| unaccounted', miss, '| unknown skip keys', bad_skip, '| failures', fails or 'none')
sys.exit(1 if (fails or miss or bad_skip) else 0)
