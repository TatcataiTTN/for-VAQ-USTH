"""Registry for the solved Jaeger problems.  @solve('7.10') functions return (parts, how, assume):
parts = [(label, value_string)], how = the method in one or two lines, assume = list of assumptions the statement leaves open.
Every solver also runs its own independent check (an assert) before returning."""
import math
REG = {}
def solve(num):
    def deco(f): REG[num] = f; return f
    return deco
def g(x, n=4):
    if x == 0: return '0'
    a = abs(x)
    if a >= 1e5 or a < 1e-3: return f'{x:.{n-1}e}'.replace('e-0', 'e-').replace('e+0', 'e+')
    return str(float(f'{x:.{n}g}'))
def si(x, unit, n=4):
    if x == 0: return f'0 {unit}'
    a = abs(x)
    for f, p in ((1e9, 'G'), (1e6, 'M'), (1e3, 'k'), (1, ''), (1e-3, 'm'), (1e-6, 'μ'), (1e-9, 'n'), (1e-12, 'p'), (1e-15, 'f')):
        if a >= f * 0.99995: return f'{float(f"{x / f:.{n}g}")} {p}{unit}'
    return f'{x:.3e} {unit}'
def close(a, b, rel=1e-3, ab=1e-12): assert abs(a - b) <= rel * max(abs(a), abs(b)) + ab, (a, b)
