"""Run every solver of build/numeric/jsol (each one asserts its own independent check) and write data/numeric/jaeger_solved.json.
Exit status 1 if any solver fails: this is the verification of the solved Jaeger problems.   Run: python3 -I build/numeric/solve_all.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'jsol')); sys.path.insert(0, HERE)
import ch07, ch09, ch10, ch11, ch12, figs10, figs11, figs12, figs6, figs7, figs9
from core import REG
from skipped import SKIP
from common import OUT
cat = json.load(open(os.path.join(OUT, 'catalog.json'), encoding='utf-8'))
by = {e['number']: e for e in cat if e['book'] == 'jaeger5' and e['kind'] == 'problem'}
solved = {}; fails = []
for n in sorted(REG, key=lambda x: [float(p) for p in x.split('.')]):
    try: r_ = REG[n](); parts, how, assume = r_[0], r_[1], r_[2]; circuit = r_[3] if len(r_) > 3 else None
    except Exception as e: fails.append((n, type(e).__name__, str(e)[:160])); continue
    e = by[n]; solved[n] = dict(number=n, section=e['section'], modules=e['modules'], pdf=e['pdf'], printed=e['printed'], parts=[[a, b] for a, b in parts], how=how, assume=assume, circuit=circuit)
ready = json.load(open(os.path.join(OUT, 'jaeger_ready.json'), encoding='utf-8'))
miss = [e['number'] for e in ready if e['number'] not in REG and e['number'] not in SKIP]
json.dump(dict(solved=solved, skipped={n: dict(reason=r, modules=by[n]['modules'] if n in by else [], pdf=by[n]['pdf'] if n in by else None) for n, r in SKIP.items()}), open(os.path.join(OUT, 'jaeger_solved.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('solved', len(solved), '| skipped with a reason', len(SKIP), '| ready problems unaccounted', miss, '| failures', fails or 'none')
sys.exit(1 if (fails or miss) else 0)
