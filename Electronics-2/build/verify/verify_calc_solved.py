"""Verification of the solved book calculations: runs every solver of build/numeric/csol (independent checks + the book's printed solution for Examples) and confirms that
no calculation exercise of the modules is left open (data/numeric/coverage.json).   Run: python3 -I build/verify/verify_calc_solved.py"""
import os, sys, json, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'build', 'numeric', 'solve_calc.py')], capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip()[-400:])
subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'build', 'numeric', 'coverage.py')], capture_output=True, text=True)
cov = json.load(open(os.path.join(ROOT, 'data', 'numeric', 'coverage.json'), encoding='utf-8')); bad = []
if r.returncode: bad.append('solve_calc failed')
if cov['open']: bad.append(('open calculation exercises', cov['open'][:5]))
print('coverage:', cov['unique_total'], cov['unique'])
print('FAILS:', bad if bad else 'none'); sys.exit(1 if bad else 0)
