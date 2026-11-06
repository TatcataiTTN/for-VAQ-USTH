"""Run every numeric formula check of the Concept finder and the structural checks on build/concepts/*.py (topics exist, ids resolve, no empty fields)."""
import os, sys, json, importlib, traceback
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'concepts')); sys.path.insert(0, os.path.join(ROOT, 'build'))
import lib, checks
for i in range(1, 11): importlib.import_module(f'm{i:02d}')
bad = []; ran = {}
for name, fn in sorted(checks.CHECKS.items()):
    try: ran[name] = fn()
    except Exception as e: bad.append((name, repr(e)[:300])); traceback.print_exc()
ids = {c['id'] for c in lib.CONCEPTS}
for c in lib.CONCEPTS:
    if not c['chk'] and c['facts']: bad.append((c['id'], 'has formulas but no check'))
    if c['chk'] and c['chk'] not in checks.CHECKS: bad.append((c['id'], 'unknown check ' + c['chk']))
    for r in c['related']:
        if r not in ids: bad.append((c['id'], 'unknown related ' + r))
    bank = json.load(open(os.path.join(ROOT, 'data', 'qbank', c['mod'] + '.json'), encoding='utf-8'))
    topics = {x['topic']['en'] for x in bank['items']}
    for t in c['topics']:
        if t not in topics: bad.append((c['id'], 'topic not in bank: ' + t))
    if not c['topics']: bad.append((c['id'], 'no topics'))
    if not (c['kw'] and c['kwv']): bad.append((c['id'], 'no keywords'))
with_f = [c for c in lib.CONCEPTS if c['facts']]; checked = [c for c in with_f if c['chk']]
print(f'concepts {len(lib.CONCEPTS)} | with formulas {len(with_f)} | formulas checked by a numeric route {len(checked)} | distinct checks {len(ran)}')
for k, v in ran.items(): print(f'  ok  {k:16s} {v}')
print('FAILS:', bad if bad else 'none')
sys.exit(1 if bad else 0)
