"""Re-run the solvers of the Jaeger problems without printed answers: each carries its own independent check (simulated VTC, FFT vs integral, exact nodal circuit,
numerical root finding, rebuilt polynomials...).  Prints FAILS: none when all pass.  Run: python3 -I build/verify/verify_jaeger_solved.py"""
import subprocess, sys, os
r = subprocess.run([sys.executable, '-I', os.path.join(os.path.dirname(__file__), '..', 'numeric', 'solve_all.py')], capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip()[-400:]); print('FAILS:', 'none' if r.returncode == 0 else 'see above'); sys.exit(r.returncode)
