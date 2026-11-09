"""Jaeger 5e Chapter 12 problems that refer to a figure: cascaded op-amp amplifiers (Figs. P12.2–P12.23), instrumentation amplifiers (Figs. 12.4, P12.38), active filters (Figs. 12.5, 12.7, 12.9),
data converters and oscillators.  Every solver reads the figure (`circuit` string says what was read), applies the book's formulas and re-checks the result with an exact nodal (MNA) solution of
the circuit (mna.py); the cascade helpers are first tested against the book's own worked Example 12.1 (anchor, run at import time)."""
import math, itertools, random
import numpy as np
from core import *
from mna import Ckt, dc
from fighelp import cir, dbv
from scipy.optimize import brentq

# ---------------------------------------------------------------- cascades of single-op-amp stages
# a stage is ('inv', R1, R2)  (R1 in series with the − input, R2 feedback)  or ('non', R2, R1)  (R2 feedback, R1 from the − input to ground; the input drives the + input)
def _opamp(c, k, plus, minus, out, A, Rid, Ro, vos=0.0, sat=None, fT=None, Ric=None):
    p = plus
    if vos: c.V(f'vos{k}', f'p{k}', plus, vos); p = f'p{k}'                    # offset: the + terminal of the ideal amplifier is vos above the external + node
    if Rid < 1e14: c.R(p, minus, Rid)
    if Ric: c.R(p, '0', 2 * Ric); c.R(minus, '0', 2 * Ric)
    internal = f'i{k}' if Ro > 0 else out
    if sat is not None: c.V(f'sat{k}', internal, '0', sat)                    # output stuck at a supply rail: the gain element is removed
    elif fT:                                                                       # single-pole op amp  A(s) = A/(1 + s/ωb), ωb = 2π fT/A  (E → 1 Ω → C → buffer)
        c.E(f'E{k}', f'x{k}', '0', p, minus, A); c.R(f'x{k}', f'y{k}', 1.0); c.C(f'y{k}', '0', A / (2 * math.pi * fT)); c.E(f'B{k}', internal, '0', f'y{k}', '0', 1.0)
    else: c.E(f'E{k}', internal, '0', p, minus, A)
    if Ro > 0: c.R(internal, out, Ro)
def _build(stages, vin, A, Rid, Ro, shunt, vos, sat, fT, Ric, test_out):
    c = Ckt(); n = len(stages)
    if test_out is None: c.V('vs', 'in', '0', vin)
    else: c.V('vs', 'in', '0', 0.0); c.V('vt', f'o{n - 1}', '0', test_out)
    if shunt: c.R('in', '0', shunt)
    prev = 'in'
    for k, (kind, a, b) in enumerate(stages):
        o = f'o{k}'; m = f'm{k}'
        if kind == 'inv': c.R(prev, m, a); c.R(m, o, b); _opamp(c, k, '0', m, o, A, Rid, Ro, vos, sat.get(k), fT, Ric)
        else: c.R(o, m, a); c.R(m, '0', b); _opamp(c, k, prev, m, o, A, Rid, Ro, vos, sat.get(k), fT, Ric)
        prev = o
    return c
def cascade(stages, vin=1.0, A=1e12, Rid=1e15, Ro=0.0, shunt=None, Vs=None, vos=0.0, fT=None, Ric=None, test_out=None, s=0.0):
    """exact solution; with Vs the outputs are clamped at ±Vs (an op amp whose output would exceed the supply is replaced by a fixed source) -> (volts, amps, set of saturated stages)"""
    sat = {}
    for _ in range(len(stages) + 2):
        c = _build(stages, vin, A, Rid, Ro, shunt, vos, sat, fT, Ric, test_out); v, i = c.solve(s)
        if Vs is None: break
        new = {}
        for k in range(len(stages)):
            if k in sat: continue
            u = v[f'i{k}'] if Ro > 0 else v[f'o{k}']
            if abs(u.real) > Vs * (1 + 1e-12): new[k] = math.copysign(Vs, u.real)
        if not new: break
        sat.update(new)
    return v, i, set(sat)
def metrics(stages, A=1e12, Rid=1e15, Ro=0.0, shunt=None, Ric=None):
    """voltage gain, input resistance (source side) and output resistance of the whole cascade from the exact nodal solution"""
    v, i, _ = cascade(stages, 1.0, A, Rid, Ro, shunt, Ric=Ric); Av = v[f'o{len(stages) - 1}'].real; Rin = 1.0 / (-i['vs'].real) if abs(i['vs']) > 1e-18 else float('inf')
    if Ro == 0: return Av, Rin, 0.0                                                         # the output of a voltage-controlled source with Ro = 0 is stiff
    v, i, _ = cascade(stages, 0.0, A, Rid, Ro, shunt, Ric=Ric, test_out=1.0); Rout = 1.0 / (-i['vt'].real)
    return Av, Rin, Rout
def ideal_av(stages):
    p = 1.0
    for kind, a, b in stages: p *= (-b / a if kind == 'inv' else 1 + a / b)
    return p
def book_stage(st, A, Rid, Ro, Ric=None):
    """Jaeger Table 11.3: Av, Rin, Rout of one closed-loop stage with finite A, Rid, Ro"""
    kind, a, b = st
    if kind == 'non': R2, R1 = a, b; beta = R1 / (R1 + R2); T = A * beta; Rin = Rid * (1 + T); Av = A / (1 + T)
    else: R1, R2 = a, b; beta = R1 / (R1 + R2); T = A * beta; Rin = R1 + 1 / (1 / Rid + (1 + A) / R2); Av = -(R2 / R1) * T / (1 + T)
    if Ric and kind == 'non': Rin = 1 / (1 / Rin + 1 / Ric)
    return Av, Rin, Ro / (1 + T), beta
def book_cascade(stages, A, Rid, Ro, shunt=None):
    """two-port cascade, Eq. (12.1): product of the gains times the loading divider between stages; Rin = first stage, Rout = last stage"""
    s = [book_stage(x, A, Rid, Ro) for x in stages]; Av = 1.0
    for k, (a, rin, rout, _) in enumerate(s):
        Av *= a
        if k + 1 < len(s): Av *= s[k + 1][1] / (rout + s[k + 1][1])
    Rin = s[0][1] if not shunt else 1 / (1 / s[0][1] + 1 / shunt)
    return Av, Rin, s[-1][2]
def nodes7(v, stages, shunt_in=True):
    """the seven non-ground nodes of a three-stage amplifier in the order the book lists them: vI, v−A, vOA, v−B, vOB, v−C, vO"""
    out = [('vI', v['in'])]
    for k in range(len(stages)): out += [(f'v−{"ABC"[k]}' if stages[k][0] == 'inv' else f'v−{"ABC"[k]}', v[f'm{k}']), (f'vO{"ABC"[k]}' if k < len(stages) - 1 else 'vO', v[f'o{k}'])]
    return out
def vfmt(nodes, n=4, clean=False): return '; '.join(f'{nm} = {si(0.0 if clean and abs(x.real) < 1e-9 else x.real, "V", n)}' for nm, x in nodes)          # clean: an ideal op amp has exactly 0 V across its inputs (the 1e12 gain leaves femtovolts)
def ac_bw(stages, fT, A, Rid=1e15, Ro=0.0, shunt=None):
    """−3 dB frequency of the exact circuit with single-pole op amps (E, RC, buffer) by root search"""
    v0, _, _ = cascade(stages, 1.0, A, Rid, Ro, shunt, fT=fT); g0 = abs(v0[f'o{len(stages) - 1}'])
    f = lambda lf: abs(cascade(stages, 1.0, A, Rid, Ro, shunt, fT=fT, s=2j * math.pi * 10 ** lf)[0][f'o{len(stages) - 1}']) / g0 - 1 / math.sqrt(2)
    return 10 ** brentq(f, -1, 9, xtol=1e-12)
def stage_bw(st, A, fT):
    """book: f_B = β·fT (Table 11.3); exact single-pole value f_B = (fT/A)(1 + Aβ)"""
    kind, a, b = st; beta = (b / (a + b)) if kind == 'non' else (a / (a + b)); return beta * fT, fT / A * (1 + A * beta), beta
def overall_bw(fs):
    """Eq. (12.6): |Π 1/(1 + jf/f_i)| = 1/√2"""
    f = lambda lf: np.prod([1 / math.sqrt(1 + (10 ** lf / x) ** 2) for x in fs]) - 1 / math.sqrt(2)
    return 10 ** brentq(f, -3, 12, xtol=1e-13)
def worst(stages, shunt, tol, fn, rng_seed=1):
    """corners of the tolerance box of every resistor (the quantity is monotone in each) -> (min, max); a random sample inside the box must stay inside [min, max]"""
    base = [(k, j) for k, st in enumerate(stages) for j in (1, 2)]; nom = fn(stages, shunt); vals = []
    def mk(signs, sh):
        new = [list(st) for st in stages]
        for (k, j), sg in zip(base, signs): new[k][j] *= 1 + sg * tol
        return [tuple(x) for x in new], (None if shunt is None else shunt * (1 + sh * tol))
    n = len(base) + (1 if shunt else 0)
    for sg in itertools.product((-1, 1), repeat=n): st, sh = mk(sg[:len(base)], sg[-1] if shunt else 0); vals.append(fn(st, sh))
    lo, hi = min(vals), max(vals); rnd = random.Random(rng_seed)
    for _ in range(400):
        st, sh = mk([rnd.uniform(-1, 1) for _ in base], rnd.uniform(-1, 1) if shunt else 0); x = fn(st, sh); assert lo * (1 - 1e-9) - 1e-12 <= x <= hi * (1 + 1e-9) + 1e-12
    return nom, lo, hi

# ---- anchor: the book's own Example 12.1 (three-stage cascade; Av = −1320, Rin = 75 kΩ; 5 mV and 10 mV nodes; SPICE v−B with A = 120 dB) ----
EX121 = [('non', 150e3, 15e3), ('inv', 21e3, 420e3), ('non', 100e3, 20e3)]
def _anchor():
    close(ideal_av(EX121), -1320, 1e-12); Av, Rin, Rout = metrics(EX121, shunt=75e3); close(Av, -1320, 1e-6); close(Rin, 75e3, 1e-6); assert Rout < 1e-3
    v, _, sat = cascade(EX121, 5e-3, shunt=75e3, Vs=12.0); assert not sat; close(v['o0'].real, 55e-3, 1e-9); close(v['o1'].real, -1.1, 1e-9); close(v['o2'].real, -6.6, 1e-9)
    v, _, sat = cascade(EX121, 10e-3, shunt=75e3, Vs=12.0); assert sat == {2}; close(v['m2'].real, -2.0, 1e-9); close(v['o2'].real, -12.0, 1e-9); close(12 / 1320, 9.09e-3, 1e-3)    # Example 12.1 (c), (d)
    v, _, _ = cascade(EX121, 5e-3, A=1e6, shunt=75e3); close(v['m1'].real, 1.10e-6, 2e-2, 1e-12)                                                                                  # SPICE v−B = 1.100 μV
_anchor()
CASC = 'cascade of single-op-amp stages (inverting stage: R1 in series with the − input, R2 in feedback; noninverting stage: input on the + input, divider R2/R1 on the − input); each stage drives the next one directly'
STG2 = [('inv', 24e3, 360e3), ('inv', 10e3, 47e3)]                                          # Fig. P12.2
STG3 = [('inv', 3e3, 56e3)] * 3                                                           # Fig. P12.3
STG5 = [('non', 160e3, 20e3), ('inv', 20e3, 160e3)]                                       # Fig. P12.5
STG6 = [('non', 390e3, 47e3), ('non', 100e3, 18e3)]                                       # Fig. P12.6
STG9 = [('inv', 56e3, 560e3), ('inv', 18e3, 180e3), ('inv', 20e3, 270e3)]                 # Fig. P12.9
STG14 = [('non', 27e3, 2e3)] * 3; SH14 = 1e6                                              # Fig. P12.14 (1 MΩ from the first + input to ground)
STG17 = [('non', 150e3, 12e3), ('inv', 10e3, 200e3), ('non', 200e3, 20e3)]; SH17 = 120e3  # Fig. P12.17 (120 kΩ from the first + input to ground)
STG23 = [('non', 47e3, 12e3), ('inv', 2e3, 220e3), ('non', 47e3, 12e3)]                   # Fig. P12.23
def desc(stages, shunt=None):
    t = []
    for kind, a, b in stages: t.append(f'inverting {si(a, "Ω", 3)} / {si(b, "Ω", 3)}' if kind == 'inv' else f'noninverting {si(a, "Ω", 3)} / {si(b, "Ω", 3)}')
    return ' → '.join(t) + (f' (input shunted by {si(shunt, "Ω", 3)} to ground)' if shunt else '')
def swapped(stages): return list(reversed(stages))
def ideal_rows(stages, shunt=None, tag=''):
    Av, Rin, Rout = metrics(stages, shunt=shunt); close(Av, ideal_av(stages), 1e-6); Rin_ex = shunt if shunt else (stages[0][1] if stages[0][0] == 'inv' else float('inf'))
    if Rin_ex != float('inf'): close(Rin, Rin_ex, 1e-6)
    return [(f'{tag}Av (ideal)', f'{g(Av, 5)} ({g(dbv(Av), 4)} dB)'), (f'{tag}Rin', si(Rin_ex, 'Ω') if Rin_ex != float('inf') else '∞'), (f'{tag}Rout', '0')], Av
def finite_rows(stages, A, Rid, Ro, shunt=None, tag=''):
    Av, Rin, Rout = metrics(stages, A, Rid, Ro, shunt); bA, bRi, bRo = book_cascade(stages, A, Rid, Ro, shunt)
    close(Av, bA, 5e-3); close(Rin, bRi, 3e-2) if Rin != float('inf') else None; close(Rout, bRo, 0.25, 1e-9)             # the book formulas ignore the loading of Rid on the feedback divider (a few % in Rout)
    return [(f'{tag}Av (A = {g(A, 4)}, Rid = {si(Rid, "Ω", 3)}, Ro = {si(Ro, "Ω", 3)})', f'{g(Av, 5)} ({g(dbv(Av), 4)} dB)'), (f'{tag}Rin', si(Rin, 'Ω', 4)), (f'{tag}Rout', si(Rout, 'Ω', 3))], (Av, Rin, Rout), (bA, bRi, bRo)
BOOKNOTE = 'Table 11.3 / Eq. (12.1): stage gain A/(1 + Aβ) (noninverting) or −(R2/R1)·T/(1 + T) (inverting) with T = Aβ, β = R1/(R1 + R2); Rin = Rid(1 + Aβ) or R1 + Rid‖R2/(1 + A); Rout = Ro/(1 + Aβ); stages combined with the loading divider Rin2/(Rout1 + Rin2); the overall Rin is that of the first stage and the overall Rout that of the last'
def two_stage_problem(num, fig, stages, A, Rid, Ro, figtext, extra=None):
    ia, Av0 = ideal_rows(stages, tag='(a) '); fr, ex, bk = finite_rows(stages, A, Rid, Ro, tag='(b) ')
    sw = swapped(stages); ia2, Av2 = ideal_rows(sw, tag='(c, stages interchanged) (a) '); fr2, ex2, bk2 = finite_rows(sw, A, Rid, Ro, tag='(c, stages interchanged) (b) ')
    close(Av0, Av2, 1e-9)                                                                    # the ideal gain does not depend on the order
    parts = ia + fr + [('(c) new circuit', desc(sw))] + ia2 + fr2
    return parts, f'Ideal op amps: Av = product of the stage gains, Rin = Rin of the first stage, Rout = 0 (Eq. 12.2). Finite op amps: {BOOKNOTE}. All numbers were also obtained from an exact nodal solution of the complete circuit; the book formulas agree within {g(100 * max(abs(ex[0] / bk[0] - 1), abs(ex2[0] / bk2[0] - 1)), 2)} % in the gain and within {g(100 * max(abs(ex[2] / bk[2] - 1), abs(ex2[2] / bk2[2] - 1)), 2)} % in Rout (they neglect the loading of Rid on the feedback divider).', \
        ['Rin and Rout of the cascade are those of the first and last amplifier (ideal source, no load), as stated in Sec. 12.1.1.'] + (extra or []), cir(num, fig, figtext)
@solve('12.4')
def _(): return two_stage_problem('12.4', 'Fig. P12.2', STG2, 1e5, 500e3, 200.0, 'two inverting stages in cascade: vI → 24 kΩ → (− input) with 360 kΩ feedback; its output → 10 kΩ → (− input) with 47 kΩ feedback → vo1; both + inputs grounded.')
@solve('12.5')
def _(): return two_stage_problem('12.5', 'Fig. P12.5', STG5, 10 ** (86 / 20), 250e3, 100.0, 'noninverting stage (vI on the + input, feedback divider 160 kΩ from the output / 20 kΩ to ground) followed by an inverting stage (20 kΩ in, 160 kΩ feedback); the figure carries a stray label "(c)" under it.')
@solve('12.6')
def _(): return two_stage_problem('12.6', 'Fig. P12.6', STG6, 10 ** (106 / 20), 300e3, 200.0, 'two noninverting stages in cascade: vI on the + input of the first, feedback divider 390 kΩ / 47 kΩ; its output on the + input of the second, feedback divider 100 kΩ / 18 kΩ.')
def _three(num, stages, fig, A, Rid, Ro, txt, shunt=None):
    ia, Av0 = ideal_rows(stages, shunt, '(a) '); fr, ex, bk = finite_rows(stages, A, Rid, Ro, shunt, '(b) ')
    return ia + fr, f'Ideal: Av = product of the stage gains, Rin = first stage, Rout = 0 (Eq. 12.2). Finite op amps: {BOOKNOTE}. The values were also found by an exact nodal solution of the whole circuit (book formulas agree within {g(100 * abs(ex[0] / bk[0] - 1), 2)} % in gain).', ['The open-loop gain in dB is converted with A = 10^(dB/20).'], cir(num, fig, txt)
T3 = 'three identical inverting stages in cascade: each 3 kΩ in series with the − input and 56 kΩ feedback, + inputs grounded; vI drives the first stage, vO is the output of the third.'
T9 = 'three inverting stages in cascade: 56 kΩ in / 560 kΩ feedback, then 18 kΩ / 180 kΩ, then 20 kΩ / 270 kΩ; + inputs grounded; vI drives the first stage, vO is the output of the third.'
@solve('12.7')
def _(): return _three('12.7', STG3, 'Fig. P12.3', 10 ** (94 / 20), 400e3, 250.0, T3)
@solve('12.9')
def _(): return _three('12.9', STG9, 'Fig. P12.9', 10 ** (94 / 20), 400e3, 250.0, T9)
def sat_problem(num, stages, fig, txt, cases, Vs=12.0, shunt=None):
    rows = []
    for tag, vin, A in cases:
        v, i, sat = cascade(stages, vin, A or 1e12, shunt=shunt, Vs=Vs)
        Ai = ideal_av(stages) if not A else None; n = len(stages)
        if not sat and not A: close(v[f'o{n - 1}'].real, ideal_av(stages) * vin, 1e-9)                     # linear ideal case: vO = Av·vI
        if sat and not A:                                                                                  # saturated: the clamped stage output must be where the linear gain would have exceeded the supply
            lin = vin
            for kind, a, b in stages: lin *= (-b / a if kind == 'inv' else 1 + a / b)
            assert abs(lin) > Vs
        rows.append((tag, vfmt(nodes7(v, stages), 4, clean=not A) + ('; op amp ' + ', '.join('ABC'[k] for k in sorted(sat)) + f' saturated at {"+" if v[f"o{max(sat)}"].real > 0 else "−"}{Vs:g} V (output cannot reach the linear value)' if sat else '; all three op amps are in their linear range')))
    return rows, 'Ideal op amps with ±12 V supplies: node voltages from the stage gains (vO = Av·vI) while |vO| < 12 V; when a stage would exceed the supply its output is clamped at the rail, its feedback loop is broken and the − input of that stage is the divider voltage of its resistors (Example 12.1(c)). Exact nodal solution (clamped output = fixed source) gives the same voltages.', \
        [f'The statement counts 8 nodes; the figure shows seven circuit nodes (vI, the three − inputs and three outputs) besides the ground, which is listed here; the ±{Vs:g} V supply rails are 8th/9th and are not circuit nodes.' if False else 'The figure shows seven nodes besides ground (vI, the three − inputs, the three outputs); the statement says 8 nodes, probably counting the ground (0 V) as the 8th. All seven are listed.', 'The output saturates exactly at the supply voltage (as in Example 12.1).'] + (['Case (c) uses finite gain A = 80 dB = 10^4 with infinite Rid and zero Ro (nothing else is specified).'] if any(c[2] for c in cases) else []), cir(num, fig, txt)
@solve('12.8')
def _(): return sat_problem('12.8', STG3, 'Fig. P12.3', T3, [('(a) vI = 1 mV', 1e-3, None), ('(b) vI = 3 mV', 3e-3, None), ('(c) vI = 2 mV, A = 80 dB', 2e-3, 1e4)])
@solve('12.10')
def _(): return sat_problem('12.10', STG9, 'Fig. P12.9', T9, [('(a) vI = 5 mV', 5e-3, None), ('(b) vI = 10 mV', 10e-3, None), ('(c) vI = 10 mV, A = 80 dB', 10e-3, 1e4)])
@solve('12.12')
def _():
    Rf = 56e3; G = 100 ** (1 / 3); R1 = Rf / G; st = [('inv', R1, Rf)] * 3; Av, Rin, Rout = metrics(st); close(abs(Av), 100, 1e-9); close(Rin, R1, 1e-9); assert Av < 0
    return [('Gain per stage', f'{g(G, 5)} (each stage inverts)'), ('New input resistor R1 = 56 kΩ / 4.6416', si(R1, 'Ω', 4)), ('Overall gain', f'{g(Av, 5)} = {g(dbv(Av), 4)} dB (magnitude 100)'), ('New Rin', si(Rin, 'Ω', 4))], \
        '40 dB = 100 = G³ with three identical inverting stages: G = 100^(1/3) = Rf/R1; Rin = R1 of the first stage (Sec. 12.1.1).', ['The statement speaks of "the 2-kΩ resistors" but Fig. P12.3 shows 3-kΩ input resistors (and 12.11 also says 3 kΩ): the three input resistors of the figure are replaced and the 56-kΩ feedback resistors are kept. 40 dB is taken as magnitude 100 (the amplifier is inverting, so Av = −100).'], cir('12.12', 'Fig. P12.3', T3)
T14 = 'three noninverting stages in cascade (feedback divider 27 kΩ from the output / 2 kΩ to ground in each); vI drives the + input of the first stage, which is also tied to ground by 1 MΩ; the output of each stage drives the + input of the next; vO is the output of the third.'
@solve('12.14')
def _():
    rows, Av = ideal_rows(STG14, SH14); close(Av, 14.5 ** 3, 1e-8); v, i, sat = cascade(STG14, 1e-3, shunt=SH14, Vs=None); close(v['o2'].real, Av * 1e-3, 1e-9)
    return rows + [('(b) node voltages for vI = 1 mV', vfmt(nodes7(v, STG14), 5, True))], 'Three noninverting stages: Av = (1 + 27/2)³ = 14.5³; Rin = 1 MΩ (the shunt resistor; the + input is ideal); Rout = 0. Node voltages: vO1 = 14.5 vI, vO2 = 14.5² vI, vO3 = 14.5³ vI; each − input equals the + input of its stage (ideal op amp): v−A = vI, v−B = vO1, v−C = vO2. Exact nodal solution agrees.', \
        ['The statement says eight nodes; seven non-ground nodes are shown in the figure (vI, three − inputs, three outputs), the 8th is probably the ground.'], cir('12.14', 'Fig. P12.14', T14)
@solve('12.15')
def _():
    st = [('non', 27e3, 3e3)] * 3; sh = 470e3
    stages = [('non', 27e3, 3e3)] * 3; rows, Av = ideal_rows(stages, sh); close(Av, 10 ** 3, 1e-8); v, i, sat = cascade(stages, 1e-3, shunt=sh)
    return rows + [('node voltages for vI = 1 mV', vfmt(nodes7(v, stages), 5, True))], 'As Prob. 12.14 with the 2-kΩ resistors replaced by 3 kΩ: Av = (1 + 27/3)³ = 10³ = 1000; Rin = 470 kΩ; Rout = 0.', ['"All the 2-kΩ resistors" are the three divider resistors to ground; the 27-kΩ feedback resistors are kept.'], cir('12.15', 'Fig. P12.14', T14)
@solve('12.16')
def _():
    nom, lo, hi = worst(STG14, SH14, 0.02, lambda s, sh: metrics(s, shunt=sh)[0]) if False else worst(STG14, SH14, 0.02, lambda s, sh: ideal_av(s))
    r = worst(STG14, SH14, 0.02, lambda s, sh: sh); close(r[0], 1e6, 1e-12)
    return [('Voltage gain (nominal, min, max)', f'{g(nom, 5)}; {g(lo, 5)}; {g(hi, 5)}'), ('Input resistance (nominal, min, max)', f'{si(r[0], "Ω", 4)}; {si(r[1], "Ω", 4)}; {si(r[2], "Ω", 4)}'), ('Output resistance', '0 (ideal op amps)')], \
        'Av = Π(1 + R2/R1) is monotone in every resistor: the extremes occur when each feedback resistor is at +2 % and each resistor to ground at −2 % (max) or the reverse (min). Checked by evaluating all 2⁷ corners of the tolerance box and 400 random points inside it (none lies outside the range).', [], cir('12.16', 'Fig. P12.14', T14)
T17 = 'noninverting stage (vI on the + input, tied to ground by 120 kΩ; divider 150 kΩ / 12 kΩ), then an inverting stage (10 kΩ in, 200 kΩ feedback), then a noninverting stage (divider 200 kΩ / 20 kΩ); vO is the output of the third.'
@solve('12.17')
def _():
    rows, Av = ideal_rows(STG17, SH17); close(Av, 13.5 * -20 * 11, 1e-8); vin = 0.004; v, i, sat = cascade(STG17, vin, shunt=SH17, Vs=None)
    return rows + [('(b) node voltages for vI = 0.004 V', vfmt(nodes7(v, STG17), 5, True))], 'Av = (1 + 150/12)(−200/10)(1 + 200/20) = 13.5·(−20)·11; Rin = 120 kΩ (shunt resistor; the first + input is ideal); Rout = 0. vOA = 13.5 vI, vOB = −20 vOA, vO = 11 vOB; v−A = vI, v−B = 0 (virtual ground), v−C = vOB. Exact nodal solution agrees.', \
        ['No supply voltage is given, so the op amps are taken as unsaturated (|vO| = 11.88 V stays below the usual ±12 V anyway).', 'Seven non-ground nodes are listed (the statement says eight; the 8th is probably the ground).'], cir('12.17', 'Fig. P12.17', T17)
@solve('12.13')
def _():
    nom, lo, hi = worst(STG9, None, 0.05, lambda s, sh: ideal_av(s)); rin = worst([STG9[0]], None, 0.05, lambda s, sh: s[0][1])
    return [('Voltage gain (nominal, min, max)', f'{g(nom, 5)}; {g(lo, 5)}; {g(hi, 5)}'), ('Input resistance = R1 of the first stage (nominal, min, max)', f'{si(rin[0], "Ω", 4)}; {si(rin[1], "Ω", 4)}; {si(rin[2], "Ω", 4)}'), ('Output resistance', '0')], \
        'Av = Π(−R2/R1): gain magnitude is maximum with every feedback resistor +5 % and every input resistor −5 % (and minimum the reverse); the sign is negative (three inversions). Checked by all 2⁶ corners and 400 random points.', ['"Minimum" and "maximum" refer to the magnitude of the (negative) gain.'], cir('12.13', 'Fig. P12.9', T9)
@solve('12.18')
def _():
    nom, lo, hi = worst(STG17, SH17, 0.01, lambda s, sh: ideal_av(s)); r = worst(STG17, SH17, 0.01, lambda s, sh: sh)
    return [('Voltage gain (nominal, min, max)', f'{g(nom, 5)}; {g(lo, 5)}; {g(hi, 5)}'), ('Input resistance = 120 kΩ shunt (nominal, min, max)', f'{si(r[0], "Ω", 4)}; {si(r[1], "Ω", 4)}; {si(r[2], "Ω", 4)}'), ('Output resistance', '0')], \
        'Corner evaluation of the product Av = (1 + R2/R1)(−R2/R1)(1 + R2/R1) over the 2⁷ corners of the ±1 % tolerance box, checked with 400 random points.', ['"Minimum" and "maximum" refer to the magnitude of the (negative) gain.'], cir('12.18', 'Fig. P12.17', T17)
@solve('12.11')
def _():
    st = [('inv', 3.9e3, 56e3)] * 3; Av, Rin, Rout = metrics(st); close(Av, -(56 / 3.9) ** 3, 1e-9)
    return [('Av', f'{g(Av, 5)} ({g(dbv(Av), 4)} dB)'), ('Rin', si(Rin, 'Ω')), ('Rout', '0')], 'Three identical inverting stages: Av = (−56/3.9)³; Rin = 3.9 kΩ (first stage); Rout = 0.', ['Ideal op amps (the statement gives no op-amp parameters).'], cir('12.11', 'Fig. P12.3', T3)
# ---------------------------------------------------------------- gain and bandwidth of cascades (single-pole op amps: A(s) = Ao/(1 + s/ωb), fT = Ao·fb)
def bw_rows(stages, Ao, fT, shunt=None, tag=''):
    rows = []; fs = []; gs = []
    for k, st in enumerate(stages):
        fb, fex, beta = stage_bw(st, Ao, fT); T = Ao * beta; ideal = ideal_av([st]); a0 = ideal * T / (1 + T); close(a0, metrics([st], Ao)[0], 1e-6); close(fb, fex, 2e-2)
        rows.append((f'{tag}stage {"ABC"[k]} ({"inverting" if st[0] == "inv" else "noninverting"} {si(st[1], "Ω", 3)}/{si(st[2], "Ω", 3)})', f'Av(0) = {g(a0, 5)} (ideal {g(ideal, 4)}); f_B = β·fT = {si(fb, "Hz", 4)} (β = {g(beta, 4)})')); fs.append(fb); gs.append(a0)
    A0 = float(np.prod(gs)); fo = overall_bw(fs); fo_ac = ac_bw(stages, fT, Ao, shunt=shunt)
    close(fo, fo_ac, 2e-2)                                                                   # exact frequency response of the complete circuit with single-pole op amps
    if len(set(stages)) == 1:
        n = len(stages); close(fo, fs[0] * math.sqrt(2 ** (1 / n) - 1), 1e-9)                # Eq. (12.9) for identical stages
    rows.append((f'{tag}overall', f'Av(0) = {g(A0, 5)} ({g(dbv(A0), 4)} dB); bandwidth f_H = {si(fo, "Hz", 4)} (from |Av(jω_H)| = |Av(0)|/√2, Eq. 12.6)'))
    return rows, fo, fo_ac
BWNOTE = 'Each closed-loop stage has Av(0) = Av,ideal·T/(1 + T) with T = Ao·β, β = R1/(R1 + R2), and bandwidth f_B = β·fT (Table 11.3); the cascade is Av(s) = ΠAv_k(s) (Eq. 12.3) and its −3 dB frequency solves Eq. (12.6). Check: the full circuit with single-pole op amps (A(s) = Ao/(1 + s/ωb), ωb = 2π·fT/Ao) solved exactly at s = jω by nodal analysis gives the same −3 dB frequency within 2 %'
def bw_problem(num, fig, txt, cases, Ao, fT):
    rows = []; ref = []
    for tag, st, sh in cases:
        r, fo, fa = bw_rows(st, Ao, fT, sh, tag); rows += r; ref.append(f'{si(fa, "Hz", 4)}')
    return rows, BWNOTE + f' (exact: {"; ".join(ref)}).', ['Ao in dB is converted with A = 10^(dB/20); Rid = ∞ and Ro = 0 (the statement gives no other op-amp parameters).'], cir(num, fig, txt)
@solve('12.19')
def _(): return bw_problem('12.19', 'Figs. P12.2, P12.5 and P12.6', 'Fig. P12.2: two inverting stages 24k/360k and 10k/47k; Fig. P12.5: noninverting 160k/20k then inverting 20k/160k; Fig. P12.6: noninverting 390k/47k then noninverting 100k/18k.', [('P12.2 ', STG2, None), ('P12.5 ', STG5, None), ('P12.6 ', STG6, None)], 10 ** (86 / 20), 3e6)
@solve('12.20')
def _(): return bw_problem('12.20', 'Fig. P12.3', T3, [('P12.3 ', STG3, None)], 1e5, 3e6)
@solve('12.21')
def _(): return bw_problem('12.21', 'Fig. P12.14', T14, [('P12.14 ', STG14, SH14)], 10 ** (86 / 20), 5e6)
@solve('12.22')
def _(): return bw_problem('12.22', 'Fig. P12.17', T17, [('P12.17 ', STG17, SH17)], 10 ** (80 / 20), 5e6)
T23 = 'three stages in cascade: a noninverting amplifier (divider 47 kΩ / 12 kΩ), an inverting amplifier (2 kΩ in, 220 kΩ feedback) and a noninverting amplifier (47 kΩ / 12 kΩ); each op amp is drawn with its supply pins (+, −); vI drives the + input of the first stage, vO is the output of the third.'
A23, RID23, RO23, FT23 = 10 ** (86 / 20), 250e3, 200.0, 4e6
@solve('12.23')
def _():
    Av, Rin, Rout = metrics(STG23, A23, RID23, RO23); bA, bRi, bRo = book_cascade(STG23, A23, RID23, RO23); close(Av, bA, 5e-3); close(Rin, bRi, 0.15); close(Rout, bRo, 0.25, 1e-9)           # book formulas neglect the loading of Rid on the feedback divider
    fs = [stage_bw(st, A23, FT23)[0] for st in STG23]; fo = overall_bw(fs); fa = ac_bw(STG23, FT23, A23, RID23, RO23); close(fo, fa, 3e-2)
    v, i, sat = cascade(STG23, 0.0, A23, RID23, RO23, Vs=15.0, vos=10e-3)
    nd = nodes7(v, STG23); close(nd[0][1].real, 0, 1, 1e-9)
    lin = cascade(STG23, 0.0, A23, RID23, RO23, vos=10e-3)[0]                                  # the unclamped value shows that the last output would be beyond the rail
    assert 'o2' in v and abs(lin['o2'].real) > 15
    return [('(a) voltage gain', f'{g(Av, 5)} ({g(dbv(Av), 4)} dB)'), ('(a) input resistance', si(Rin, 'Ω', 4)), ('(a) output resistance', si(Rout, 'Ω', 3)), ('(a) bandwidth', f'{si(fo, "Hz", 4)} (exact circuit with single-pole op amps: {si(fa, "Hz", 4)})'),
            ('(b) the 10 nodes for vI = 0 (offset +10 mV at each + input, ±15 V supplies)', vfmt(nd, 3) + '; V+ = 15.0 V; V− = −15.0 V; ground = 0 V' + f'. The output of the third op amp would be {si(lin["o2"].real, "V", 3)} without the supply limit, so op amp C saturates at {si(v["o2"].real, "V", 3)}')], \
        BOOKNOTE + '. Bandwidth: ' + BWNOTE[:150] + '… Offsets: each op amp is replaced by an ideal-gain amplifier whose + input sits 10 mV above the external + node; when an output would pass ±15 V the amplifier is replaced by a fixed source at the rail (its feedback loop is open, Example 12.1(c)).', \
        ['The ten nodes are the seven circuit nodes (vI, three − inputs, three outputs) plus V+, V− and ground, as listed in Example 12.1.', 'Offsets of +10 mV at the + input of every op amp, output saturation exactly at ±15 V; three significant digits are shown.'], cir('12.23', 'Fig. P12.23', T23)
@solve('12.24')
def _():
    def fAv(s, sh): return metrics(s, A23, RID23, RO23)[0]
    def fRin(s, sh): return metrics(s, A23, RID23, RO23)[1]
    def fRout(s, sh): return metrics(s, A23, RID23, RO23)[2]
    def fBW(s, sh): return overall_bw([stage_bw(st, A23, FT23)[0] for st in s])
    r = {k: worst(STG23, None, 0.10, f) for k, f in (('Av', fAv), ('Rin', fRin), ('Rout', fRout), ('BW', fBW))}
    return [('Voltage gain (nominal, min, max)', f'{g(r["Av"][0], 5)}; {g(r["Av"][1], 5)}; {g(r["Av"][2], 5)}'), ('Input resistance (nominal, min, max)', f'{si(r["Rin"][0], "Ω", 3)}; {si(r["Rin"][1], "Ω", 3)}; {si(r["Rin"][2], "Ω", 3)}'),
            ('Output resistance (nominal, min, max)', f'{si(r["Rout"][0], "Ω", 3)}; {si(r["Rout"][1], "Ω", 3)}; {si(r["Rout"][2], "Ω", 3)}'), ('Bandwidth (nominal, min, max)', f'{si(r["BW"][0], "Hz", 4)}; {si(r["BW"][1], "Hz", 4)}; {si(r["BW"][2], "Hz", 4)}')], \
        'The quantities of Prob. 12.23 (Ao = 86 dB, Rid = 250 kΩ, Ro = 200 Ω, fT = 4 MHz) are evaluated at all 2⁶ corners of the ±10 % tolerance box of the six resistors (each quantity is monotone in every resistor, so the extremes are at corners); 400 random points inside the box are checked to lie within [min, max].', \
        ['"Min" and "max" refer to the magnitude of the gain; the sign is the same for all corners.'], cir('12.24', 'Fig. P12.23', T23)

# ---------------------------------------------------------------- instrumentation amplifiers (Fig. 12.4 and Fig. P12.38)
def inamp(v1, v2, R1, R2, R3, R4, A=1e12, Rid=1e15, Ro=0.0, Ric=None, test=None):
    """Fig. 12.4: op amps ① and ② (noninverting, R2 in each output leg, 2R1 between their − inputs) feed the difference amplifier ③ (R3 from each output, R4 feedback / to ground)"""
    c = Ckt(); c.V('s1', 'v1', '0', v1); c.V('s2', 'v2', '0', v2)
    _opamp(c, 1, 'v1', 'n1', 'a', A, Rid, Ro, Ric=Ric); _opamp(c, 2, 'v2', 'n2', 'b', A, Rid, Ro, Ric=Ric); c.R('a', 'n1', R2); c.R('n1', 'n2', 2 * R1); c.R('n2', 'b', R2)
    c.R('a', 'q', R3); c.R('q', 'o', R4); c.R('b', 'p', R3); c.R('p', '0', R4); _opamp(c, 3, 'p', 'q', 'o', A, Rid, Ro, Ric=Ric)
    if test == 'out': c.V('vt', 'o', '0', 1.0)
    return c
@solve('12.35')
def _():
    R1, R2, R3, R4 = 1.5e3, 75e3, 10e3, 10e3; G = -(R4 / R3) * (1 + R2 / R1); c = inamp(1.0, 0.0, R1, R2, R3, R4); v, _ = dc(c); close(v['o'], G, 1e-8)
    c = inamp(2.0, 2.1, R1, R2, R3, R4); v, _ = dc(c); close(v['o'], G * (2.0 - 2.1), 1e-8); vdc = v['o']; c = inamp(2.1, 2.0, R1, R2, R3, R4); vm, _ = dc(c)     # v1 = 2.1 (= 2 + 0.1) → peak of the sine
    return [('Voltage gain vo/(v1 − v2) = −(R4/R3)(1 + R2/R1)', f'{g(G, 5)}'), ('Output voltage', f'vo = {g(G * (2 - 2.1), 4)} V {g(G * 0.1, 4)}·sin(2000πt) V, i.e. vo = {g(-G * 0.1, 3)} − {g(-G * 0.1, 3)}·sin(2000πt) V (between 0 and {g(-2 * G * 0.1, 3)} V)')], \
        'Instrumentation amplifier (Eq. 12.10 and the formula printed beside Fig. 12.4): vo = −(R4/R3)(1 + R2/R1)(v1 − v2) with v1 − v2 = (2 + 0.1 sin 2000πt) − 2.1 = −0.1 + 0.1 sin 2000πt. Checked with an exact nodal solution of the three-op-amp circuit (the middle resistor is 2R1).', \
        ['Ideal op amps and no supply limits (none are given); the output swing 0 … 10.2 V therefore is not clipped.'], cir('12.35', 'Fig. 12.4', 'instrumentation amplifier: v1 and v2 drive the + inputs of op amps ① and ②; resistors R2, 2R1, R2 in series between their outputs (the − inputs are at the nodes v1 and v2 of the 2R1 resistor); op amp ③ with R3, R4 forms the difference amplifier.')
@solve('12.36')
def _():
    R1, R2, R3, R4 = 15e3, 75e3, 10e3, 20e3; G = -(R4 / R3) * (1 + R2 / R1); c = inamp(1.0, 0.0, R1, R2, R3, R4); v, _ = dc(c); close(v['o'], G, 1e-8)
    c = inamp(4.0, 3.5, R1, R2, R3, R4); v, _ = dc(c); close(v['o'], G * 0.5, 1e-8)
    return [('Voltage gain vo/(v1 − v2) = −(R4/R3)(1 + R2/R1)', g(G, 5)), ('Output voltage', f'vo = {g(G * 0.5, 4)} V + {g(-G * -0.2, 4) if False else g(G * -0.2, 4)}·sin(4000πt) V (dc {g(G * 0.5, 3)} V, amplitude {g(abs(G * 0.2), 3)} V)')], \
        'As Prob. 12.35: vo = G(v1 − v2) with v1 − v2 = (4 − 0.2 sin 4000πt) − 3.5 = 0.5 − 0.2 sin 4000πt.', ['Ideal op amps and no supply limits (none are given).'], cir('12.36', 'Fig. 12.4', 'instrumentation amplifier of Fig. 12.4 (op amps ① and ② with R2, 2R1, R2; difference amplifier ③ with R3, R4).')
@solve('12.37')
def _():
    A, Rid, Ric, Ro = 8e4, 1e6, 800e6, 100.0; R1, R2, R3, R4 = 2e3, 42e3, 10e3, 10e3
    def Rin(which):
        c = inamp(1.0 if which == 1 else 0.0, 1.0 if which == 2 else 0.0, R1, R2, R3, R4, A, Rid, Ro, Ric); v, i = dc(c); return 1.0 / (-i[f's{which}'])
    Ri1, Ri2 = Rin(1), Rin(2)
    c = inamp(0.0, 0.0, R1, R2, R3, R4, A, Rid, Ro, Ric, test='out'); v, i = dc(c); Rout = 1.0 / (-i['vt'])
    b1 = 2 * R1 / (2 * R1 + R2); T1 = A * b1; bR = 1 / (1 / (2 * Ric) + 1 / (Rid * (1 + T1))); bTab = 1 / (1 / Ric + 1 / (Rid * (1 + T1))); b3 = R3 / (R3 + R4); bRout = Ro / (1 + A * b3)
    close(Ri1, bR, 1e-2); close(Ri2, bR, 1e-2); close(Rout, bRout, 0.1)
    return [('Rin1 (input v1, v2 grounded)', si(Ri1, 'Ω', 4)), ('Rin2 (input v2, v1 grounded)', si(Ri2, 'Ω', 4)), ('Rout', si(Rout, 'Ω', 3))], \
        f'Exact nodal solution of the instrumentation amplifier with each op amp modelled by A, Rid between the inputs, 2Ric from each input to ground (Fig. 11.44) and Ro. Book estimate: op amp ① or ② is a noninverting amplifier with β = 2R1/(2R1 + R2) = {g(b1, 4)}, so the source sees 2Ric (the resistor at its own + input) in parallel with Rid(1 + Aβ): Rin = {si(bR, "Ω", 3)} (the 2Ric at the − input is fed from the op-amp output, not from the source). the simplified entry of Table 11.3, Ric ‖ Rid(1 + Aβ), would give {si(bTab, "Ω", 3)}; the exact nodal values are given. The output resistance is that of op amp ③, Rout = Ro/(1 + Aβ3) = {si(bRout, "Ω", 3)} with β3 = R3/(R3 + R4) = 0.5.', \
        ['Rin1 is measured with v2 grounded and Rin2 with v1 grounded.', 'The common-mode input resistance is modelled as in Fig. 11.44 (a resistor 2Ric from each op-amp input to ground); with the simplified Table 11.3 formula Ric ‖ Rid(1 + Aβ) the input resistances would be about 0.55 times smaller (ambiguity logged).'], cir('12.37', 'Fig. 12.4', 'instrumentation amplifier of Fig. 12.4 (op amps ① and ② with R2, 2R1, R2 between their outputs; difference amplifier ③ with R3, R4).')
def inamp38(va, vb, sgn=1.0):
    c = Ckt(); c.V('sa', 'va', '0', va); c.V('sb', 'vb', '0', vb)
    _opamp(c, 1, 'va', 'v2', 'v1', 1e12, 1e15, 0.0); _opamp(c, 2, 'vb', 'v3', 'v4', 1e12, 1e15, 0.0)
    c.R('v1', 'v2', 4.9e3); c.R('v2', 'v3', 200.0); c.R('v3', 'v4', 4.9e3); c.R('v1', 'v5', 9.99e3); c.R('v5', 'vo', 10.01e3); c.R('v4', 'v6', 10.01e3); c.R('v6', '0', 9.99e3); _opamp(c, 3, 'v6', 'v5', 'vo', 1e12, 1e15, 0.0)
    v, _ = dc(c); i1 = (v['v1'] - v['v2']) / 4.9e3 + (v['v1'] - v['v5']) / 9.99e3; i2 = (v['v4'] - v['v3']) / 4.9e3 + (v['v4'] - v['v6']) / 10.01e3; i3 = (v['vo'] - v['v5']) / 10.01e3
    return v, i1, i2, i3
def inamp38_formula(va, vb):
    d = va - vb; v1 = va + 24.5 * d; v4 = vb - 24.5 * d; v6 = v4 * 9.99 / (10.01 + 9.99); v5 = v6; vo = v5 * (1 + 10.01 / 9.99) - (10.01 / 9.99) * v1
    return dict(v1=v1, v2=va, v3=vb, v4=v4, v5=v5, v6=v6, vo=vo)
T38 = 'instrumentation amplifier with ideal op amps: va on the + input of the upper op amp (output v1; 4.9 kΩ from v1 to its − input v2), vb on the + input of the lower op amp (output v4; 4.9 kΩ from v4 to its − input v3); 200 Ω between v2 and v3; difference amplifier: 9.99 kΩ from v1 to v5 (− input) with 10.01 kΩ feedback v5→vo, 10.01 kΩ (R3) from v4 to v6 (+ input) with 9.99 kΩ from v6 to ground; i1, i2, i3 are drawn flowing from the nodes v1, v4, vo into the op-amp outputs.'
def inamp38_rows(va, vb):
    v, i1, i2, i3 = inamp38(va, vb); f = inamp38_formula(va, vb)
    for k in f: close(v[k], f[k], 1e-8, 1e-8)
    return v, i1, i2, i3
@solve('12.38')
def _():
    v, i1, i2, i3 = inamp38_rows(5.02, 4.98)
    ad = (inamp38(0.5, -0.5)[0]['vo']); ac = inamp38(1.0, 1.0)[0]['vo']; cm = abs(ad / ac); f = inamp38_formula(0.5, -0.5); close(ad, f['vo'], 1e-8); close(ac, inamp38_formula(1.0, 1.0)['vo'], 1e-8, 1e-9)
    close(v['vo'], ad * 0.04 + ac * 5.0, 1e-8)                                              # superposition: vo = Adm·vid + Acm·vic with vid = 0.04 V, vic = 5.00 V
    return [('node voltages', f'v1 = {g(v["v1"], 6)} V, v2 = {g(v["v2"], 6)} V, v3 = {g(v["v3"], 6)} V, v4 = {g(v["v4"], 6)} V, v5 = {g(v["v5"], 6)} V, v6 = {g(v["v6"], 6)} V, vo = {g(v["vo"], 6)} V'), ('currents (into the op-amp outputs)', f'i1 = {si(i1, "A", 4)}, i2 = {si(i2, "A", 4)}, i3 = {si(i3, "A", 4)}'),
            ('differential-mode gain', f'Adm = vo/vid = {g(ad, 6)} ({g(dbv(ad), 4)} dB), vid = va − vb'), ('common-mode gain', f'Acm = vo/vic = {g(ac, 5)} ({g(dbv(ac), 4)} dB), vic = (va + vb)/2'), ('CMRR', f'|Adm/Acm| = {g(cm, 5)} = {g(dbv(cm), 4)} dB')], \
        'Ideal op amps: v2 = va, v3 = vb, so the current through 4.9k + 200 Ω + 4.9k is (va − vb)/200 and v1 = va + 24.5(va − vb), v4 = vb − 24.5(va − vb); then the difference amplifier gives v6 = v4·9.99/20, v5 = v6 and vo = v5(1 + 10.01/9.99) − (10.01/9.99)v1. Adm and Acm come from vo = Adm·vid + Acm·vic (vid = va − vb, vic = (va + vb)/2); the same values follow from the exact nodal solution of the circuit.', \
        ['Current directions follow the arrows of the figure (from the node into the op-amp output); the common-mode gain arises only from the 0.2 % mismatch of the 9.99 k / 10.01 k resistors.'], cir('12.38', 'Fig. P12.38', T38)
@solve('12.39')
def _():
    v, i1, i2, i3 = inamp38_rows(3.0, 3.0)
    return [('node voltages', f'v1 = {g(v["v1"], 6)} V, v2 = {g(v["v2"], 6)} V, v3 = {g(v["v3"], 6)} V, v4 = {g(v["v4"], 6)} V, v5 = {g(v["v5"], 6)} V, v6 = {g(v["v6"], 6)} V, vo = {g(v["vo"], 6)} V'), ('currents (into the op-amp outputs)', f'i1 = {si(i1, "A", 4)}, i2 = {si(i2, "A", 4)}, i3 = {si(i3, "A", 4)}')], \
        'Purely common-mode input (va = vb = 3 V): no current in the 4.9k–200 Ω–4.9k chain, v1 = v2 = v3 = v4 = 3 V; the difference amplifier gives v6 = v5 = 3·0.4995 = 1.4985 V and vo = v5(1 + 10.01/9.99) − (10.01/9.99)·3 = −6.006 mV. Exact nodal solution agrees.', ['Current directions follow the arrows of Fig. P12.38.'], cir('12.39', 'Fig. P12.38', T38)
# ---------------------------------------------------------------- active filters (Fig. 12.5 low-pass, Fig. 12.7 high-pass with gain, Fig. 12.9 band-pass)
def lpf_ckt(R1, R2, C1, C2):
    c = Ckt(); c.V('vi', 'i', '0', 1.0); c.R('i', 'v1', R1); c.R('v1', 'v2', R2); c.C('v1', 'o', C1); c.C('v2', '0', C2); c.opamp('v2', 'o', 'o'); return c            # voltage follower: the output node is also the − input
def hpf_ckt(R1, R2, C1, C2, K):
    c = Ckt(); c.V('vi', 'i', '0', 1.0); c.C('i', 'v1', C1); c.C('v1', 'v2', C2); c.R('v2', '0', R2); c.R('v1', 'o', R1); Rg = 10e3
    c.opamp('v2', 'm', 'o'); c.R('o', 'm', (K - 1) * Rg); c.R('m', '0', Rg); return c                                                                                    # noninverting amplifier of gain K
def bpf_ckt(R1, R2, C1, C2, R3=None):
    c = Ckt(); c.V('vi', 'i', '0', 1.0); c.R('i', 'v1', R1)
    if R3: c.R('v1', '0', R3)                                   # R3 to ground at the Thévenin node: with the source it forms vth = vI·R3/(R1 + R3), Rth = R1‖R3 (Fig. 12.9(b))
    c.C('v1', 'o', C1); c.C('v1', 'm', C2); c.R('m', 'o', R2); c.opamp('0', 'm', 'o'); return c
def gain_at(c, f, node='o'): return c.solve(2j * math.pi * f)[0][node]
def lp_fH(c):
    g0 = abs(gain_at(c, 1e-3)); return 10 ** brentq(lambda lf: abs(gain_at(c, 10 ** lf)) / g0 - 1 / math.sqrt(2), -2, 9, xtol=1e-13)
def hp_fL(c, fo):
    """lower half-power frequency: |H| = H(∞)/√2, searched between fo/100 and fo (the response rises monotonically there)"""
    gh = abs(gain_at(c, fo * 1e5)); return 10 ** brentq(lambda lf: abs(gain_at(c, 10 ** lf)) / gh - 1 / math.sqrt(2), math.log10(fo) - 2, math.log10(fo), xtol=1e-13)
def bp_peak(c, f0):
    """peak frequency (maximum of |H|), the two −3 dB frequencies relative to the peak, peak gain"""
    lf = np.linspace(math.log10(f0) - 2, math.log10(f0) + 2, 4001); m = np.array([abs(gain_at(c, 10 ** x)) for x in lf]); k = int(m.argmax())
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda x: -abs(gain_at(c, 10 ** x)), bounds=(lf[max(k - 1, 0)], lf[min(k + 1, len(lf) - 1)]), method='bounded', options={'xatol': 1e-12}); fp = 10 ** r.x; gp = abs(gain_at(c, fp))
    f = lambda x: abs(gain_at(c, 10 ** x)) / gp - 1 / math.sqrt(2); lo = 10 ** brentq(f, lf[0], r.x, xtol=1e-13); hi = 10 ** brentq(f, r.x, lf[-1], xtol=1e-13)
    return fp, lo, hi, gp
def lpf_design(fo, C2):
    """maximally flat: Q = 1/√2 with C1 = 2C2 = 2C, R1 = R2 = R = 1/(√2·ωo·C) (Example 12.6)"""
    R = 1 / (math.sqrt(2) * 2 * math.pi * fo * C2); return R, R, 2 * C2, C2
def lpf_check(R1, R2, C1, C2):
    fo = 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2)); Q = math.sqrt(C1 / C2) * math.sqrt(R1 * R2) / (R1 + R2); c = lpf_ckt(R1, R2, C1, C2); fH = lp_fH(c)
    close(abs(gain_at(c, fo)), Q, 1e-6); return fo, Q, fH                                      # the gain at ωo equals Q (Sec. 12.3.1); fH = fo for Q = 1/√2
@solve('12.40')
def _():
    C2 = 5e-9; R1, R2, C1, C2 = lpf_design(25e3, C2); fo, Q, fH = lpf_check(R1, R2, C1, C2); close(fo, 25e3, 1e-9); close(Q, 1 / math.sqrt(2), 1e-9); close(fH, 25e3, 1e-6)
    KF = 2.0; C1b, C2b = C1 / KF, C2 / KF; fo2, Q2, fH2 = lpf_check(R1, R2, C1b, C2b); close(fo2, 50e3, 1e-9); close(Q2, Q, 1e-12); close(fH2, 50e3, 1e-6)
    return [('(a) R1 = R2 = 1/(√2·ωo·C) with C = C2 = 5 nF', f'R1 = R2 = {si(R1, "Ω", 4)}, C1 = {si(C1, "F", 3)}, C2 = {si(C2, "F", 3)} (nearest standard 1 % value to be taken from Appendix A)'), ('(a) check', f'fo = {si(fo, "Hz", 5)}, Q = {g(Q, 5)}; −3 dB frequency of the exact circuit = {si(fH, "Hz", 5)}'), ('(a) filter bandwidth', f'f_H = fo = {si(fH, "Hz", 4)} (the low-pass filter extends from dc to f_H)'),
            ('(b) frequency scaling KF = 2: every capacitor divided by 2, R unchanged', f'R1 = R2 = {si(R1, "Ω", 4)}, C1 = {si(C1b, "F", 3)}, C2 = {si(C2b, "F", 3)}; fo = {si(fo2, "Hz", 5)}, Q = {g(Q2, 5)}, f_H = {si(fH2, "Hz", 5)}')], \
        'Design Example 12.6 with C1 = 2C2 = 2C and R1 = R2 = R: ωo = 1/√(R1R2C1C2) = 1/(√2·RC), Q = √(C1/C2)·√(R1R2)/(R1 + R2) = 1/√2 (Eqs. 12.19), so R = 1/(√2·ωo·C). The exact circuit (Fig. 12.5 with an ideal follower) solved at s = jω confirms |A(jωo)| = Q and that the −3 dB frequency equals fo; frequency scaling (Eq. 12.37) halves the capacitors.', \
        ['"Assume C = 0.005 μF" is read as C2 = C = 5 nF, C1 = 2C = 10 nF (as in Example 12.6).'], cir('12.40', 'Fig. 12.5', 'two-pole low-pass filter: vI → R1 → node v1 → R2 → node v2 (+ input of a voltage follower, output vo); C1 from v1 to the output; C2 from v2 to ground.')
@solve('12.47')
def _():
    C2 = 10e-9; R1, R2, C1, C2 = lpf_design(2e3, C2); fo, Q, fH = lpf_check(R1, R2, C1, C2); close(fH, 2e3, 1e-6)
    return [('Design (C2 = C = 10 nF chosen)', f'R1 = R2 = {si(R1, "Ω", 4)} (the exercise in Sec. 12.3.1 for the same case gives 5.62 kΩ), C1 = 2C = {si(C1, "F", 3)}, C2 = {si(C2, "F", 3)}'), ('Check on the exact circuit', f'fo = {si(fo, "Hz", 5)}, Q = {g(Q, 5)}, −3 dB frequency (bandwidth) = {si(fH, "Hz", 5)}')], \
        'Maximally flat means Q = 1/√2, for which f_H = fo. Use C1 = 2C2 = 2C and R1 = R2 = 1/(√2·ωo·C) (Design Example 12.6); the value of C sets the impedance level. The exact circuit confirms the −3 dB frequency.', ['The statement does not fix the capacitor: C2 = 10 nF is chosen as in Example 12.6 (any other C works with R scaled as 1/C).'], cir('12.47', 'Fig. 12.5', 'two-pole low-pass filter: vI → R1 → v1 → R2 → v2 (+ input of a voltage follower); C1 from v1 to the output; C2 from v2 to ground.')
@solve('12.48')
def _():
    Q = 1.0; K = 3 - 1 / Q; x = math.sqrt((-1 + math.sqrt(5)) / 2); fL = 24e3; fo = fL / x; C = 1e-9; R = 1 / (2 * math.pi * fo * C)
    c = hpf_ckt(R, R, C, C, K); fL_ex = hp_fL(c, fo); close(fL_ex, fL, 1e-6)
    ga = abs(gain_at(c, fo)); close(ga, K * Q, 1e-6)                                        # |A(jωo)| = K/(3 − K) = K·Q (Sec. 12.3.2)
    alt = hp_fL(hpf_ckt(1 / (2 * math.pi * fL * C), 1 / (2 * math.pi * fL * C), C, C, K), fL)
    return [('Amplifier gain K from Q = 1/(3 − K)', f'K = 3 − 1/Q = {g(K, 4)}  (noninverting amplifier: (K − 1)R′ = R′, e.g. two equal resistors)'), ('Natural frequency from the −3 dB condition', f'x = fL/fo = {g(x, 5)} (x⁴ + x² − 1 = 0), so fo = {si(fo, "Hz", 5)}'), ('R and C (C1 = C2 = 1 nF chosen)', f'R1 = R2 = 1/(2π·fo·C) = {si(R, "Ω", 4)}'), ('Check on the exact circuit', f'lower half-power frequency = {si(fL_ex, "Hz", 5)}; |A(jωo)| = {g(ga, 5)} = K·Q')], \
        'High-pass filter of Fig. 12.7 with R1 = R2 = R, C1 = C2 = C: ωo = 1/(RC), Q = 1/(3 − K) (Eq. 12.26), so Q = 1 needs K = 2. The lower half-power frequency fL satisfies |A(jω)| = K/√2: with x = ω/ωo and Q = 1 it gives x⁴ + x² − 1 = 0, x = 0.786, so fo = fL/0.786. The −3 dB condition |A| = K/√2 reads x⁴/√((1 − x²)² + x²/Q²) = 1/√2. Verified by solving the exact circuit at s = jω (root of |A| = K/√2).', \
        ['"Lower-half power frequency" is taken as the exact −3 dB frequency (fo = 30.5 kHz). If one set fo = 24 kHz instead (the book says ωo approximately equals the lower cutoff), the real half-power frequency would be ' + si(alt, 'Hz', 4) + '.', 'The capacitor value is not given: C1 = C2 = 1 nF chosen (R scales as 1/C).'], cir('12.48', 'Fig. 12.7', 'high-pass filter with gain: vI → C1 → v1 → C2 → v2 → R2 to ground; R1 from v1 to the output; the output is vo = K·v2 from a noninverting amplifier with resistors (K − 1)R and R.')
def bp_formulas(R1, R2, C1, C2, R3=None):
    Rth = R1 if not R3 else R1 * R3 / (R1 + R3); fo = 1 / (2 * math.pi * math.sqrt(Rth * R2 * C1 * C2)); Q = math.sqrt(R2 * C1 * C2) / (math.sqrt(Rth) * (C1 + C2)); return fo, Q, Rth
@solve('12.49')
def _():
    Rth, R2, C = 1e3, 200e3, 220e-12; fo = 1 / (2 * math.pi * C * math.sqrt(Rth * R2)); Q = 0.5 * math.sqrt(R2 / Rth); BW = 2 / (R2 * C) / (2 * math.pi); close(BW, fo / Q, 1e-9)
    c = bpf_ckt(Rth, R2, C, C); fp, lo, hi, gp = bp_peak(c, fo); close(fp, fo, 1e-6); close(hi - lo, fo / Q, 3e-3); close(gp, 0.5 * R2 / Rth, 1e-5)            # R3 = ∞ ⇒ Rth = R1; peak gain 2Q²
    KM = 3.3; R2b, Rthb, Cb = R2 * KM, Rth * KM, C / KM; fob = 1 / (2 * math.pi * Cb * math.sqrt(Rthb * R2b)); Qb = 0.5 * math.sqrt(R2b / Rthb); close(fob, fo, 1e-12); close(Qb, Q, 1e-12)
    KF = 2.0; Cc = C / KF; foc = 1 / (2 * math.pi * Cc * math.sqrt(Rth * R2)); close(foc, 2 * fo, 1e-12); BWc = 2 / (R2 * Cc) / (2 * math.pi); close(foc / Q, BWc, 1e-9)
    return [('(a) center frequency fo = 1/(2πC√(Rth·R2))', si(fo, 'Hz', 4)), ('(a) Q = ½√(R2/Rth)', g(Q, 5)), ('(a) bandwidth BW = fo/Q = 1/(π·R2·C)', si(BW, 'Hz', 4)), ('(a) check on the exact circuit', f'peak at {si(fp, "Hz", 5)}, −3 dB edges {si(lo, "Hz", 4)} and {si(hi, "Hz", 4)} (width {si(hi - lo, "Hz", 4)}), peak gain {g(gp, 4)} = 2Q²'),
            ('(b) magnitude scaling KM = 3.3 (R × KM, C ÷ KM)', f'Rth = {si(Rthb, "Ω", 3)}, R2 = {si(R2b, "Ω", 3)}, C1 = C2 = {si(Cb, "F", 4)}; fo = {si(fob, "Hz", 4)} and Q = {g(Qb, 4)} unchanged'), ('(c) frequency scaling KF = 2 (C ÷ 2, R unchanged)', f'C1 = C2 = {si(Cc, "F", 4)}; fo = {si(foc, "Hz", 4)}, Q = {g(Q, 4)}, BW = {si(BWc, "Hz", 4)}')], \
        'Band-pass filter of Fig. 12.9 with C1 = C2 = C (Eq. 12.32): ωo = 1/(C√(Rth R2)), Q = ½√(R2/Rth), BW = 2/(R2 C). Magnitude scaling (Eq. 12.35) multiplies R by KM and divides C by KM (fo, Q unchanged); frequency scaling (Eq. 12.37) divides C by KF. The exact circuit (Thévenin source) solved at s = jω gives the same fo, bandwidth and peak gain.', \
        ['Rth = R1‖R3 is the Thévenin resistance of Fig. 12.9(b); as given, R1 and R3 individually are not needed.'], cir('12.49', 'Fig. 12.9', 'band-pass filter with the inverting op-amp configuration: vI → R1 (R3 from the node to ground, giving the Thévenin source vth with Rth = R1‖R3) → node v1; C1 from v1 to the output; C2 from v1 to the − input; R2 from the − input to the output; + input grounded.')
@solve('12.50')
def _():
    fo, Q, C = 600.0, 5.0, 10e-9; wo = 2 * math.pi * fo; R1 = 1 / (2 * Q * wo * C); R2 = 4 * Q ** 2 * R1; BW = fo / Q
    c = bpf_ckt(R1, R2, C, C); fp, lo, hi, gp = bp_peak(c, fo); close(fp, fo, 1e-6); close(hi - lo, BW, 3e-3); close(gp, 2 * Q ** 2, 1e-5)
    KF = 2250.0 / 600.0; Cb = C / KF; c2 = bpf_ckt(R1, R2, Cb, Cb); fp2, lo2, hi2, gp2 = bp_peak(c2, 2250.0); close(fp2, 2250.0, 1e-6); close((hi2 - lo2), 2250.0 / Q, 3e-3)
    return [('(a) design with R3 = ∞ (Rth = R1) and C1 = C2 = C = 10 nF', f'R1 = Rth = 1/(2Q·ωo·C) = {si(R1, "Ω", 4)}, R2 = 4Q²·R1 = {si(R2, "Ω", 4)}'), ('(a) bandwidth', f'BW = fo/Q = {si(BW, "Hz", 3)}  (peak gain 2Q² = {g(2 * Q ** 2, 3)})'), ('(a) check on the exact circuit', f'peak {si(fp, "Hz", 5)}, edges {si(lo, "Hz", 4)} – {si(hi, "Hz", 4)}, gain {g(gp, 4)}'),
            ('(b) frequency scaling to 2.25 kHz: KF = 3.75, C ÷ KF', f'C1 = C2 = {si(Cb, "F", 4)}, R1 and R2 unchanged; fo = {si(fp2, "Hz", 5)}, Q = 5, BW = {si(2250.0 / Q, "Hz", 3)}')], \
        'From Eq. (12.32) with R3 = ∞: Q = ½√(R2/R1) ⇒ R2 = 4Q²R1, and ωo = 1/(C√(R1R2)) = 1/(2Q·R1·C) ⇒ R1 = 1/(2Q·ωo·C). Frequency scaling (Eq. 12.37): C′ = C/KF with KF = 2250/600. The exact circuit confirms fo, the bandwidth and the gain 2Q².', ['The capacitor is not specified: C1 = C2 = 10 nF is chosen (R1, R2 scale as 1/C).'], cir('12.50', 'Fig. 12.9', 'band-pass filter with the inverting op-amp configuration: vI → R1 → v1 (R3 omitted, R3 = ∞); C1 from v1 to the output; C2 from v1 to the − input; R2 from the − input to the output.')
@solve('12.52')
def _():
    Q, wo = 3.0, 1.0; num = (2 * Q) ** 2; a = math.sqrt(math.sqrt(2) - 1)
    def H1(w): s = 1j * w; return -2 * Q * s * wo / (s * s + s * wo / Q + wo ** 2)
    H2 = lambda w: H1(w) ** 2; wp = brentq(lambda w: (abs(H2(w * 1.0001)) - abs(H2(w / 1.0001))), 0.5, 2, xtol=1e-13); close(wp, 1.0, 1e-9); gp = abs(H2(1.0)); close(gp, (2 * Q ** 2) ** 2, 1e-12)
    f = lambda w: abs(H2(w)) / gp - 1 / math.sqrt(2); w1 = brentq(f, 0.1, 1.0); w2 = brentq(f, 1.0, 10.0); BW = w2 - w1; Qo = wp / BW; close(BW, a / Q, 1e-9); close(Qo, Q / a, 1e-9); close(w1 * w2, 1.0, 1e-9)
    return [('(a) center frequency', f'ωo = {g(wp, 5)} (unchanged; also the geometric mean of the band edges {g(w1, 5)} and {g(w2, 5)})'), ('(a) bandwidth', f'BW = ωo·√(√2 − 1)/Q = {g(BW, 5)} (a single stage has ωo/Q = {g(1 / Q, 5)})'), ('(a) Q of the overall filter', f'Q = ωo/BW = Q/√(√2 − 1) = {g(Qo, 5)}'), ('(b) transfer function', 'A(s) = [−2Q·s·ωo/(s² + sωo/Q + ωo²)]² with 2Q = 6, ωo = 1: A(s) = 36 s² / (s² + s/3 + 1)²; center gain (2Q²)² = 324')], \
        'Each stage (C1 = C2, R3 = ∞) has A(s) = −2Q·sωo/(s² + sωo/Q + ωo²) with gain 2Q² at ωo (Sec. 12.3.3). The cascade is the product (Eq. 12.3), so the center frequency stays ωo; |A|/|A(jωo)| = [1 + Q²(x − 1/x)²]⁻¹ for two stages and the −3 dB condition gives (x − 1/x)² = (√2 − 1)/Q², i.e. BW = ωo·√(√2 − 1)/Q. Confirmed by root-finding on the exact product.', ['Q of the overall filter is defined as center frequency / (−3 dB bandwidth).'], cir('12.52', 'Fig. 12.9', 'band-pass filter with the inverting op-amp configuration (R3 = ∞, C1 = C2); two identical filters in cascade.')
@solve('12.54')
def _():
    fo1, fo2, Q = 5e3, 6e3, 5.0
    H = lambda f: np.prod([abs(2 * Q * 1j * (f / fo) / (1 - (f / fo) ** 2 + 1j * (f / fo) / Q)) for fo in (fo1, fo2)])
    fs = np.linspace(3e3, 9e3, 60001); m = np.array([H(f) for f in fs]); k = int(m.argmax()); fp = float(fs[k]); gp = float(m[k])
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda f: -H(f), bounds=(fp - 1, fp + 1), method='bounded', options={'xatol': 1e-9}); fp = r.x; gp = H(fp)
    peaks = int(((m[1:-1] > m[:-2]) & (m[1:-1] > m[2:])).sum()); assert peaks == 1                                    # a single hump
    f1 = brentq(lambda f: H(f) / gp - 1 / math.sqrt(2), 3e3, fp); f2 = brentq(lambda f: H(f) / gp - 1 / math.sqrt(2), fp, 9e3); BW = f2 - f1; Qo = fp / BW; fg = math.sqrt(f1 * f2)
    # independent route: the same two filters as exact circuits (Fig. 12.9, R3 = ∞) in cascade, buffered
    def circ(fo):
        C = 10e-9; R1 = 1 / (2 * Q * 2 * math.pi * fo * C); return bpf_ckt(R1, 4 * Q ** 2 * R1, C, C)
    Hc = lambda f: abs(gain_at(circ(fo1), f) * gain_at(circ(fo2), f)); close(Hc(5.5e3), H(5.5e3), 1e-6); close(Hc(fp), gp, 1e-6)
    return [('Single stages', f'fo1 = 5 kHz, fo2 = 6 kHz, Q = 5 each (bandwidths fo/Q = 1 kHz and 1.2 kHz, peak gain 2Q² = 50 each)'), ('Center frequency (maximum of the overall response)', f'{si(fp, "Hz", 5)} (geometric mean of the −3 dB edges: {si(fg, "Hz", 5)}; geometric mean of fo1, fo2: {si(math.sqrt(fo1 * fo2), "Hz", 5)})'), ('−3 dB frequencies', f'{si(f1, "Hz", 5)} and {si(f2, "Hz", 5)}'), ('Bandwidth', si(BW, 'Hz', 4)), ('Q of the overall filter = fp/BW', g(Qo, 4)), ('Peak gain', f'{g(gp, 4)} ({g(dbv(gp), 4)} dB; the response has a single hump)')], \
        'Overall response = product of the two single-stage band-pass responses A_k(jf) = −2Q·j(f/fo_k)/(1 − (f/fo_k)² + j(f/fo_k)/Q) (Eq. 12.3 with R3 = ∞). The peak is found by a one-dimensional search, the −3 dB frequencies relative to the peak by root finding. The same numbers come from solving the two filters of Fig. 12.9 as exact circuits (op amp, R, C) and multiplying their gains (the second filter does not load the first because the first output is an op-amp output).', \
        ['"Center frequency" is taken as the frequency of maximum gain (the response is not symmetric on a log scale); the geometric mean of the band edges is also shown. Q = center frequency / bandwidth.'], cir('12.54', 'Fig. 12.9', 'band-pass filter with the inverting op-amp configuration (R3 = ∞, C1 = C2); two such filters in cascade, tuned to 5 kHz and 6 kHz, Q = 5 each.')
# ---------------------------------------------------------------- D/A converters (weighted-resistor Figs. P12.67/P12.76, R-2R ladder Fig. P12.70, resistor string Fig. 12.25)
def wr_dac(bits, Rs, Rf, VREF, RREF=0.0, Ron=0.0, vos=0.0):
    """weighted-resistor DAC of Fig. 12.22: leg k = switch (on-resistance Ron) + resistor Rs[k] from the − input to VREF (bit 1) or ground (bit 0); VREF may sit behind RREF; returns vO"""
    c = Ckt()
    if RREF: c.V('vref', 'vr0', '0', VREF); c.R('vr0', 'r', RREF)
    else: c.V('vref', 'r', '0', VREF)
    for k, (b, R) in enumerate(zip(bits, Rs)):
        far = 'r' if b else '0'
        if Ron: c.R(far, f'sw{k}', Ron); far = f'sw{k}'
        c.R(far, 'm', R)
    c.R('o', 'm', Rf); _opamp(c, 0, '0', 'm', 'o', 1e12, 1e15, 0.0, vos=vos); v, _ = dc(c); return v['o']
def codes(n): return [[(k >> (n - 1 - j)) & 1 for j in range(n)] for k in range(2 ** n)]            # b1 is the MSB
def linearity(u):
    """step size, differential and integral linearity errors in LSB; the ideal LSB is recomputed from the end points (a converter with gain error has no 0.1250 step): LSB = (u[N] − u[0])/N, INL = running sum of DNL"""
    N = len(u) - 1; lsb = (u[-1] - u[0]) / N; step = [(u[k] - u[k - 1]) / lsb for k in range(1, N + 1)]; dnl = [x - 1 for x in step]; inl = [(u[k] - u[0] - k * lsb) / lsb for k in range(N + 1)]
    cs = 0.0
    for k in range(1, N + 1): cs += dnl[k - 1]; close(inl[k], cs, 1e-9, 1e-9)
    return lsb, step, dnl, inl
def dac_rows(codes_, u, scale, unit, extra=False):
    lsb, step, dnl, inl = linearity(u); rows = []
    for k, b in enumerate(codes_):
        rows.append(f'{"".join(map(str, b))}: {g(u[k] * scale, 5)} {unit}' + (f'; step {g(step[k - 1], 4)} LSB, DNL {g(dnl[k - 1], 3)}, INL {g(0.0 if abs(inl[k]) < 1e-9 else inl[k], 3)} LSB' if extra and k else (f'; INL {g(0.0 if abs(inl[k]) < 1e-9 else inl[k], 3)} LSB' if extra else '')))
    return rows, lsb, step, dnl, inl
TP67 = 'weighted-resistor DAC: switches b1…b4 (b1 = MSB) connect resistors 2R, 4R, 8R, 16R either to ground (0) or to VREF (1); the summing node is the − input of an op amp with feedback resistor R, + input grounded; the switch settings drawn are b1 b2 b3 b4 = 0 1 1 0.'
@solve('12.67')
def _():
    VREF = 2.56; Rs = [2, 4, 8, 16]; Rs = [x * 1e3 for x in Rs]; Rf = 1e3                 # R = 1 kΩ (only ratios matter)
    def vo(bits): return wr_dac(bits, Rs, Rf, VREF)
    a, b = vo([0, 1, 1, 0]), vo([1, 0, 0, 1]); close(a, -VREF * (1 / 4 + 1 / 8), 1e-8); close(b, -VREF * (1 / 2 + 1 / 16), 1e-8)
    tab = []
    for k, bits in enumerate(codes(4)): x = vo(bits); close(x, -VREF * k / 16, 1e-8, 1e-9); tab.append(f'{"".join(map(str, bits))}: {g(x, 4)} V')
    return [('(a) input 0110: vO = −VREF(b1/2 + b2/4 + b3/8 + b4/16)', f'−{g(-a, 4)} V (= −2.56·(0.25 + 0.125); magnitude {g(-a, 4)} V)'), ('(b) input 1001', f'{g(b, 4)} V (= −2.56·(0.5 + 0.0625))'), ('(c) table of all 16 codes (vO = −VREF·N/16, LSB = VREF/16 = 0.16 V)', '; '.join(tab))], \
        'The op amp with R in feedback sums the currents of the legs: vO = −R·Σ b_k·VREF/R_k = −VREF(b1/2 + b2/4 + b3/8 + b4/16) (Eq. 12.52 gives the magnitude). Exact nodal solution of the circuit for all 16 codes gives the same values.', \
        ['The circuit as drawn inverts, so vO is negative; Eq. (12.52) in the book quotes the same value without the minus sign.'], cir('12.67', 'Fig. P12.67', TP67)
@solve('12.68')
def _():
    VREF = 2.56; Rs = [x * 1e3 for x in (2, 4, 8, 16)]; R = 1e3; Rf = 1.05 * R; vos = 5e-3
    ideal = [wr_dac(b, Rs, R, VREF) for b in codes(4)]; act = [wr_dac(b, Rs, Rf, VREF, vos=vos) for b in codes(4)]
    Rp = 1 / sum(1 / x for x in Rs); offset = vos * (1 + Rf / Rp); close(act[0], offset, 1e-8)
    gain = [(act[k] - act[0]) / (ideal[k] - ideal[0]) - 1 for k in range(1, 16)]
    for x in gain: close(x, 0.05, 1e-8)                                                    # the slope is 5 % too large for every code
    lsb = VREF / 16; fsd = (act[15] - act[0]) - ideal[15]
    return [('Offset error (output for input code 0000)', f'vOS = Vos(1 + Rf/Rp) = {g(offset * 1e3, 4)} mV (Rp = 2R‖4R‖8R‖16R = {g(Rp / R, 5)}R; noise gain 1 + 1.05R/Rp = {g(1 + Rf / Rp, 5)}); = {g(offset / lsb, 3)} LSB'), ('Gain error (deviation of the slope from the ideal converter)', f'+{g(100 * gain[0], 4)} % (slope 1.05 times the ideal); at full scale (code 1111): {g(-fsd, 3)} V more negative = {g(abs(fsd) / lsb, 3)} LSB')], \
        'With feedback resistor Rf = 1.05R the transfer function is vO = −1.05·VREF·N/16 + Vos·(1 + Rf/Rp): the offset voltage is amplified by the noise gain of the summing amplifier (all legs are low-impedance to ground or VREF, so the noise gain does not depend on the code) and adds to every output; the slope is 5 % high. Exact nodal solution for all 16 codes confirms both.', \
        ['VREF = 2.56 V from Prob. 12.67 is used (it affects only the values in LSB, not the % gain error or the offset in mV).', 'Offset error = output for the all-zero code, gain error = relative deviation of the slope (Sec. 12.5.2).'], cir('12.68', 'Fig. P12.67', TP67)
TP70 = 'R-2R ladder DAC: a 2R termination to ground at the left, then three series resistors R; four legs of 2R (b4 at the left end … b1 next to the op amp) switched between ground (0) and VREF (1); the right end of the ladder is the − input (virtual ground) of an op amp with feedback R; drawn switches: b4 b3 b2 b1 = 0 1 1 0.'
@solve('12.70')
def _():
    VREF = 2.50; R = 1e3; out = []
    def ladder(b4, b3, b2, b1):
        c = Ckt(); c.V('vref', 'r', '0', VREF); legs = {'n4': b4, 'n3': b3, 'n2': b2, 'n1': b1}
        c.R('n4', '0', 2 * R); c.R('n4', 'n3', R); c.R('n3', 'n2', R); c.R('n2', 'n1', R)                      # the termination 2R, then the three series R
        for n, b in legs.items(): c.R(n, 'r' if b else '0', 2 * R)
        c.R('n1', 'm', 1e-9 * R)                                                                         # the last node is the virtual ground (wire)
        c.R('o', 'm', R); _opamp(c, 0, '0', 'm', 'o', 1e12, 1e15, 0.0); v, _ = dc(c); return v['o']
    for tag, bits, w in (('0001 (b1 only)', (0, 0, 0, 1), 1 / 2), ('0010 (b2)', (0, 0, 1, 0), 1 / 4), ('0100 (b3)', (0, 1, 0, 0), 1 / 8), ('1000 (b4)', (1, 0, 0, 0), 1 / 16)):
        x = ladder(*bits); close(x, -VREF * w, 1e-6); out.append((tag, f'vO = {g(x, 5)} V (= −VREF/{int(1 / w)})'))
    return [(f'Input {t}', v) for t, v in out], \
        'Successive Thévenin equivalents from the left: the termination 2R in parallel with a 2R leg is R, which in series with R gives 2R again, so at every node the part of the ladder to the left looks like 2R; a switched leg therefore delivers VREF/2 to the next node and each step toward the LSB halves the contribution. For the MSB leg next to the op amp, i = VREF/(2R) and vO = −R·i = −VREF/2; the others are VREF/4, VREF/8 and VREF/16. The nodal solution of the whole ladder agrees.', \
        ['The word is written b4 b3 b2 b1 as in the figure, so "0001" switches b1 (the leg next to the op amp, the MSB of the converter, weight 1/2) — the four combinations give the four binary weights.', 'The circuit as drawn inverts, so the outputs are negative (the magnitudes are VREF/2 … VREF/16).'], cir('12.70', 'Fig. P12.70', TP70)
TP72 = 'weighted-resistor DAC as in Fig. P12.67 with three bits: resistors 2R = 2.4 kΩ (b1), 4R = 4.8 kΩ (b2), 8R = 9.1 kΩ (b3) and feedback R = 1.2 kΩ.'
@solve('12.72')
def _():
    Rs = [2.4e3, 4.8e3, 9.1e3]; Rf = 1.2e3; cs = codes(3)
    u = [-wr_dac(b, Rs, Rf, 1.0) for b in cs]; rows, lsb, step, dnl, inl = dac_rows(cs, u, 1.0, '× VREF', True)
    for k, b in enumerate(cs): close(u[k], sum(x * Rf / R for x, R in zip(b, Rs)), 1e-8, 1e-12)
    import itertools as it, random as rd
    def lin(vals): Rf_, R1, R2, R3 = vals; uu = [sum(x * Rf_ / R for x, R in zip(b, (R1, R2, R3))) for b in cs]; _l, _s, d, i = linearity(uu); return max(abs(x) for x in d), max(abs(x) for x in i)
    nom = (1.2e3, 2.4e3, 4.8e3, 9.1e3); w = [0.0, 0.0]
    for sg in it.product((-1, 1), repeat=4): r = lin([x * (1 + .05 * s) for x, s in zip(nom, sg)]); w = [max(w[0], r[0]), max(w[1], r[1])]
    rnd = rd.Random(3)
    for _ in range(20000): r = lin([x * (1 + rnd.uniform(-.05, .05)) for x in nom]); assert r[0] <= w[0] * (1 + 1e-9) and r[1] <= w[1] * (1 + 1e-9)
    return [('(a) nominal outputs and errors (ideal step = (u(111) − u(000))/7 = ' + g(lsb, 5) + ' VREF)', ' | '.join(rows)), ('(a) largest errors for the nominal resistors', f'differential {g(max(abs(x) for x in dnl), 3)} LSB, integral {g(max(abs(x) for x in inl), 3)} LSB'), ('(b) worst case with 5 % resistors (R, 2R, 4R, 8R each ±5 %)', f'differential linearity error up to {g(w[0], 3)} LSB, integral linearity error up to {g(w[1], 3)} LSB')], \
        'vO/VREF = −Σ b_k R/R_k: nominal weights 0.5, 0.25 and 1.2/9.1 = 0.1319 (instead of 0.125). The gain is not the ideal one, so the ideal step is recomputed from the end points, (u111 − u000)/7 (as in Table 12.7 and Prob. 12.69); DNL = step/LSB − 1 and INL = running sum of the DNL. Worst case: the largest errors over the 16 corners of the ±5 % tolerance box of the four resistors; 20 000 random resistor sets inside the box never exceed them.', \
        ['The 8R resistor is 9.1 kΩ (a standard value), not 9.6 kΩ, so even the nominal converter has linearity errors.', 'The worst case is found at the corners of the tolerance box (checked with random sets); sign convention: the circuit inverts, the table lists the magnitudes.'], cir('12.72', 'Fig. P12.67', TP72)
TP76 = 'weighted-resistor DAC with three bits: resistors 2 kΩ (b1), 4 kΩ (b2), 8 kΩ (b3) from the − input of the op amp (feedback R, + input grounded) to switches connected to ground (0) or to VREF through the series resistor RREF (1).'
@solve('12.76')
def _():
    VREF, RREF, R = 5.0, 250.0, 1218.8; Rs = [2e3, 4e3, 8e3]; cs = codes(3)
    u = [-wr_dac(b, Rs, R, VREF, RREF) for b in cs]; rows, lsb, step, dnl, inl = dac_rows(cs, u, 1.0, 'V', True)
    for k, b in enumerate(cs):                                                                      # closed form: the reference node is VREF/(1 + RREF·Σg) with Σg the conductance of the legs connected to it
        G = sum(x / r for x, r in zip(b, Rs)); close(u[k], R * G * VREF / (1 + RREF * G), 1e-9, 1e-12)
    return [('Output magnitudes, steps, DNL, INL', ' | '.join(rows)), ('Ideal LSB (end points)', f'{g(lsb, 5)} V (VREF/8 = 0.625 V)'), ('Largest errors', f'differential {g(max(abs(x) for x in dnl), 3)} LSB, integral {g(max(abs(x) for x in inl), 3)} LSB')], \
        'With RREF the reference node moves with the data: v_ref = VREF/(1 + RREF·G) where G is the total conductance of the legs connected to it, and |vO| = R·G·v_ref. R = 1.2188 kΩ makes the full-scale code 111 equal to 7/8·VREF (zero gain error), so the ideal LSB is VREF/8; the data-dependent drop across RREF (superposition error) is what produces the linearity errors. Exact nodal solution of the circuit for all 8 codes agrees with the closed form.', \
        ['The circuit inverts; magnitudes are listed. The ideal step is taken from the end points; with R = 1.2188 kΩ this equals VREF/8 (verified).'], cir('12.76', 'Fig. P12.76', TP76)
@solve('12.77')
def _():
    VREF, Rs, Ron = 5.0, [2e3, 4e3, 8e3], 200.0; cs = codes(3); G = sum(1 / (r + Ron) for r in Rs)
    R_a = 0.875 / G; R_c0 = 0.875 * (1 + 250 * G) / G
    def table(RREF, R):
        u = [-wr_dac(b, Rs, R, VREF, RREF, Ron) for b in cs]
        for k, b in enumerate(cs):
            Gk = sum(x / (r + Ron) for x, r in zip(b, Rs)); close(u[k], R * Gk * VREF / (1 + RREF * Gk), 1e-9, 1e-12)
        return linearity(u), u
    (l1, s1, d1, i1), u1 = table(0.0, R_a); (l2, s2, d2, i2), u2 = table(250.0, R_a); (l3, s3, d3, i3), u3 = table(250.0, R_c0)
    close(u1[7], 0.875 * VREF, 1e-9); close(u3[7], 0.875 * VREF, 1e-9)
    return [('(a) R for zero gain error (code 111 → 7/8 VREF) with Ron = 200 Ω and RREF = 0', f'R = 0.875/Σ[1/(Rk + Ron)] = {si(R_a, "Ω", 5)} (Σ = {g(G * 1e3, 5)} mS); with RREF = 250 Ω the same condition gives {si(R_c0, "Ω", 5)}'), ('(b) RREF = 0, R from (a)', f'largest DNL {g(max(abs(x) for x in d1), 3)} LSB, largest INL {g(max(abs(x) for x in i1), 3)} LSB (step sizes in LSB: {", ".join(g(x, 4) for x in s1)})'),
            ('(c) RREF = 250 Ω, same R as in (a)', f'largest DNL {g(max(abs(x) for x in d2), 3)} LSB, largest INL {g(max(abs(x) for x in i2), 3)} LSB (end-point LSB {g(l2, 5)} V; steps in LSB: {", ".join(g(x, 4) for x in s2)}); gain error: full scale {g(u2[7], 5)} V instead of 4.375 V = {g(100 * (u2[7] / 4.375 - 1), 3)} % (not zero any more); with R re-trimmed to {si(R_c0, "Ω", 5)} the gain error vanishes and the linearity errors stay the same ({g(max(abs(x) for x in d3), 3)} and {g(max(abs(x) for x in i3), 3)} LSB) because they are measured against the end-point step')], \
        'Each leg is Rk + Ron (Ron = 200 Ω of its switch). |vO| = R·G·VREF/(1 + RREF·G) with G = Σ b_k/(Rk + Ron). The on-resistance is not binary-weighted, so the effective weights 1/(2.2k), 1/(4.2k), 1/(8.2k) are not in the ratio 4:2:1 and the converter is nonlinear. Zero gain error means |vO(111)| = 7/8·VREF. Errors are measured against the end-point step. Exact nodal solution of the circuit agrees with the closed form.', \
        ['Part (a) is solved with RREF = 0 (the statement does not say; the RREF = 250 Ω value is also given).', 'In (c) the resistor R is kept from (a); the end-point LSB is recomputed because a gain error now exists (the re-trimmed case is also shown).'], cir('12.77', 'Fig. P12.76', TP76)
@solve('12.82')
def _():
    n, R, Rs, Wmin = 10, 500.0, 50.0, 2.5e-6; N = 2 ** n; sq = R / Rs; tot = N * sq; L = tot * Wmin; inch = L / 0.0254
    close(sq, 10, 1e-12); close(N, 1024, 1e-12)
    return [('Number of resistors (Fig. 12.25 technique, 2ⁿ equal resistors)', f'{N}'), ('(a) squares per resistor = R/Rs', f'{g(sq)} squares'), ('(a) squares of the whole string', f'{N} × {g(sq)} = {int(tot)} squares'), ('(b) length of the string for W = 2.5 μm', f'{int(tot)} × 2.5 μm = {g(L * 1e3, 4)} mm = {g(inch, 4)} inches')], \
        'The resistor string of Fig. 12.25 has 2ⁿ equal resistors (1024 for 10 bits, the exercise in Sec. 12.5.3). A resistor of R ohms in a film of sheet resistance Rs has R/Rs squares; its length is squares × width.', ['One square is taken as one width of length (all resistors have the minimum width, same material).'], cir('12.82', 'Fig. 12.25', 'inherently monotonic DAC: a long string of equal resistors between VREF and ground, a switch tree that connects one tap to a voltage-follower op amp, decoded from the binary input (a 3-bit version has 8 resistors).')
# ---------------------------------------------------------------- ADC / integrator problems
@solve('12.88')
def _():
    out = []
    for tag, n in (('(a) 12-bit', 12), ('(b) 20-bit', 20)):
        lsb = 3.3 / 2 ** n; out.append((tag, f'LSB = VFS/2ⁿ = {si(lsb, "V", 5)}; offset < 0.1 LSB = {si(0.1 * lsb, "V", 4)}'))
    close(0.1 * 3.3 / 2 ** 12, 80.566e-6, 1e-4)
    return out, 'The comparator offset VOS shifts every transition of the successive-approximation converter by VOS, so it is an error of VOS/LSB least-significant bits: require VOS < 0.1·VFS/2ⁿ.', [], cir('12.88', 'Fig. 12.33', 'successive-approximation ADC: a comparator compares the input vX with the output of a DAC driven by the successive-approximation register (SAR) and the clock; the comparator decides each bit.')
@solve('12.90')
def _():
    V, Vos, VFS, T, R = 3.0, 10e-3, 5.12, 1 / 30, 50e3
    Vm, Vp = V - Vos, V + Vos; RC = V * T / VFS; C = RC / R
    # independent: integrate the ramp numerically for T and check it reaches VFS at the end
    from scipy.integrate import solve_ivp
    s = solve_ivp(lambda t, y: [V / RC], [0, T], [0.0], rtol=1e-12, atol=1e-14); close(s.y[0][-1], VFS, 1e-9)
    return [('(a) effective reference voltage (offset +10 mV at the + input)', f'V − Vos = {g(Vm, 5)} V (the ramp slope is (V − Vos)/RC); for an offset of the opposite sign V + Vos = {g(Vp, 5)} V'), ('(b) RC time constant (ramp reaches VFS in T = 1/30 s)', f'RC = V·T/VFS = {si(RC, "s", 4)}'), ('(b) C for R = 50 kΩ', si(C, 'F', 4))], \
        'Integrator (Fig. P12.90): vO = −(1/RC)∫(V − Vos)dt, so the offset appears as an error of the reference: Vref,eff = V − Vos. For a single-slope converter |vO| = V·t/RC must equal VFS at t = T: RC = V·T/VFS.', \
        ['The sign of the offset is not given: +10 mV at the + input is assumed (V − Vos); the opposite sign is also shown.', 'In (b) the reference V = 3 V of part (a) is used (nothing else is specified) and the offset is neglected.'], cir('12.90', 'Fig. P12.90', 'ramp generator of an integrating converter: source V through R to the − input of an op amp with capacitor C in feedback (a reset switch across C), + input grounded; output vO.')
@solve('12.91')
def _():
    A, V, T = 4e4, 5.0, 0.2
    def err(RC): tau = (A + 1) * RC; return V * T / RC - A * V * (1 - math.exp(-T / tau))
    RCmin = brentq(lambda x: err(x) - 1e-3, 1e-3, 100, xtol=1e-14); RCa = RCmin
    # independent route: integrate the circuit equation dvO/dt = −(V + vO/A)/(RC(1 + 1/A)) numerically
    from scipy.integrate import solve_ivp
    sol = solve_ivp(lambda t, y: [-(V + y[0] / A) / (RCa * (1 + 1 / A))], [0, T], [0.0], rtol=1e-12, atol=1e-14); close(sol.y[0][-1], -A * V * (1 - math.exp(-T / ((A + 1) * RCa))), 1e-9)
    assert abs(err(RCa) - 1e-3) < 1e-9 and err(RCa * 1.5) < 1e-3
    return [('Output (t ≥ 0)', f'vO(t) = −A·V·[1 − exp(−t/((A + 1)RC))] = −2×10⁵·[1 − e^(−t/(40001·RC))] V (the ideal ramp is −V·t/RC)'), ('Minimum RC for an error below 1 mV at t = 200 ms', f'RC ≥ {si(RCmin, "s", 4)} ({g(RCmin * 1e3, 4)} ms); error at that RC = {g(1e3 * err(RCmin), 4)} mV')], \
        'Op amp with finite gain A: vO = −A·v−, KCL at the − node gives (A + 1)RC·dvO/dt + vO = −A·V, so vO(t) = −A·V(1 − e^(−t/τ)), τ = (A + 1)RC (a first-order lag, not a perfect ramp). The error |ideal − actual| at T = 0.2 s is ≈ V·T/(A·RC) + V·T²/(2A·RC²), decreasing with RC; the minimum RC is found by root finding on the exact expression. Numerical integration of the circuit equation reproduces the output.', \
        ['The error is the difference of magnitudes of the ideal ramp −V·t/RC and the actual output at t = 200 ms; "less than 1 mV" is taken as the equality limit for the minimum RC.'], cir('12.91', 'Fig. P12.90', 'integrator: source V through R to the − input of an op amp with capacitor C in feedback (reset switch across C), + input grounded; a 5-V step is applied at t = 0.')
# ---------------------------------------------------------------- oscillators and multivibrators
def _finv(R3, R4, VD):
    g3, g4 = 1 / R3, 1 / R4
    def f(i):
        if abs(i) <= VD * g3: return i * R3
        return math.copysign((abs(i) + g4 * VD) / (g3 + g4), i)
    return f
def wien_sim(R, C, R1, R2, R3, R4, VD, cycles=300):
    """time-domain simulation of the Wien-bridge oscillator with ideal op amp and the diode network (piecewise-linear diodes with drop VD): returns steady amplitude and frequency"""
    from scipy.integrate import solve_ivp
    finv = _finv(R3, R4, VD); vO = lambda vp: vp * (1 + R2 / R1) + finv(vp / R1)
    def rhs(t, y): vcs, vp = y; i_s = (vO(vp) - vcs - vp) / R; return [i_s / C, (i_s - vp / R) / C]
    per = 2 * math.pi * R * C; s = solve_ivp(rhs, [0, cycles * per], [0.0, 1e-3], method='LSODA', rtol=1e-10, atol=1e-13, max_step=per / 200)
    vo = np.array([vO(v) for v in s.y[1]]); t = s.t; m = t > 0.8 * t[-1]; amp = (vo[m].max() - vo[m].min()) / 2
    z = np.where((vo[m][:-1] < 0) & (vo[m][1:] >= 0))[0]; return amp, 1 / np.mean(np.diff(t[m][z]))
def wien_formula(R, C, R1, R2, R3, R4, VD):
    fo = 1 / (2 * math.pi * R * C); ok = (R2 + R3) / R1 > 2 and (R2 + R3 * R4 / (R3 + R4)) / R1 < 2
    return fo, 3 * VD / ((2 - R2 / R1) * (1 + R4 / R3) - R4 / R1), ok
@solve('12.97')
def _():
    p = (5.1e3, 500e-12, 10e3, 14e3, 6.8e3, 10e3); VD = 0.6; fo, A, ok = wien_formula(*p, VD); assert ok
    b = wien_formula(10e3, 1e-9, 10e3, 10e3, 12e3, 24e3, VD); close(b[0], 15.9e3, 5e-3); close(b[1], 3.0, 1e-9)                     # anchor: the book's exercise (Fig. 12.48 values) gives 15.9 kHz and 3.0 V
    sa, sf = wien_sim(*p, VD); close(sf, fo, 5e-3)
    return [('Frequency of oscillation fo = 1/(2πRC)', si(fo, 'Hz', 4)), ('Conditions for the amplitude network, Eq. (12.82)', f'(R2 + R3)/R1 = {g((p[3] + p[4]) / p[2], 4)} > 2 and (R2 + R3‖R4)/R1 = {g((p[3] + p[4] * p[5] / (p[4] + p[5])) / p[2], 4)} < 2: both satisfied'), ('Amplitude from Eq. (12.85), VD = 0.6 V', f'vO ≈ 3VD/[(2 − R2/R1)(1 + R4/R3) − R4/R1] = {g(A, 4)} V (from KCL of Eqs. 12.83–12.84, equal to Eq. 12.85)'), ('Check: time-domain simulation of the same circuit (ideal op amp, diode drop 0.6 V)', f'frequency {si(sf, "Hz", 4)}, amplitude {g(sa, 3)} V (Eq. 12.85 is only an estimate)')], \
        'Wien bridge (Eq. 12.74–12.75): the loop gain is zero-phase at ωo = 1/RC where |T| = G/3, so oscillation needs G = 3. The diode network (Fig. 12.48) switches R4 in parallel with R3 at the peaks; the amplitude estimate of Eq. (12.85) follows from the equivalent circuit with D1 on (Fig. 12.49). Anchor: the book\'s own exercise with the Fig. 12.48 values (R = 10 kΩ, C = 1 nF, R1 = R2 = 10 kΩ, R3 = 12 kΩ, R4 = 24 kΩ, VD = 0.6 V) gives 15.9 kHz and 3.0 V, reproduced here.', \
        ['The diode on-voltage is not given: VD = 0.6 V as in the book\'s exercise is assumed (the amplitude is proportional to VD).', 'The time-domain simulation (piecewise-linear diodes) gives a larger amplitude than Eq. (12.85) because the book\'s formula is a peak-voltage estimate; the book\'s own SPICE value for its exercise is 3.33 V against 3.0 V from the formula.'], cir('12.97', 'Fig. 12.48', 'Wien-bridge oscillator: series RC from the output to the + input and parallel RC from the + input to ground; the − input network R1 (to ground), R2, then R3 in parallel with R4 + back-to-back diodes D1/D2 to the output (the figure also shows the lamp version of Fig. 12.47).')
def phase_sim(R, C, R2, R3, R4, VD, cycles=400):
    from scipy.integrate import solve_ivp
    g3, g4 = 1 / R3, 1 / R4; it = VD * g3
    def Phi(i): return -i * (R2 + R3) if abs(i) <= it else -math.copysign(abs(i) * R2 + (abs(i) + g4 * VD) / (g3 + g4), i)
    def Phi_inv(V):
        if abs(V) <= (R2 + R3) * it: return -V / (R2 + R3)
        return -math.copysign((abs(V) - VD / (R4 * (g3 + g4))) / (R2 + 1 / (g3 + g4)), V)
    def rhs(t, y): u1, u2, u3 = y; i = Phi_inv(u1 + u2 + u3); return [((u2 + u3) / R + u3 / R + i) / C, (u3 / R + i) / C, i / C]
    per = 2 * math.pi * math.sqrt(3) * R * C; s = solve_ivp(rhs, [0, cycles * per], [0, 0, 1e-3], method='LSODA', rtol=1e-10, atol=1e-13, max_step=per / 200)
    vo = np.array([Phi(Phi_inv(a + b + c)) for a, b, c in s.y.T]); t = s.t; m = t > 0.8 * t[-1]; amp = (vo[m].max() - vo[m].min()) / 2
    z = np.where((vo[m][:-1] < 0) & (vo[m][1:] >= 0))[0]; return amp, 1 / np.mean(np.diff(t[m][z]))
@solve('12.99')
def _():
    R, C, R2, R3, R4 = 5e3, 1e-9, 47e3, 15e3, 68e3; VD = 0.6; fo = 1 / (2 * math.pi * math.sqrt(3) * R * C); k = 1 / (12 * R)
    RF_off = R2 + R3; RF_on = R2 + R3 * R4 / (R3 + R4); assert RF_off > 12 * R > RF_on                                            # starts (RF > 12R), limited when a diode conducts (RF < 12R)
    Vpk = VD / ((1 - R2 * k) * (R4 / R3 + 1) - R4 * k); sa, sf = phase_sim(R, C, R2, R3, R4, VD); close(sf, fo, 5e-3); close(Vpk, sa, 0.3)
    return [('Frequency fo = 1/(2π√3·RC)', si(fo, 'Hz', 4)), ('Start-up and limiting condition (RF must pass 12R = 60 kΩ)', f'RF (diodes off) = R2 + R3 = {si(RF_off, "Ω", 3)} > 12R; RF (diode on, R4 in parallel with R3) = {si(RF_on, "Ω", 4)} < 12R'), ('Amplitude estimate (diode on, VD = 0.6 V; by the same method as Eq. 12.85)', f'Vpk ≈ VD/[(1 − R2/12R)(1 + R4/R3) − R4/12R] = {g(Vpk, 4)} V'), ('Check: time-domain simulation (ideal op amp, diode drop 0.6 V)', f'frequency {si(sf, "Hz", 4)}, amplitude {g(sa, 3)} V')], \
        'Phase-shift oscillator (Fig. 12.46, Eqs. 12.78–12.81): T(jωo) = RF/(12R) at ωo = 1/(√3RC), so RF must be 12R. With the diode network of Fig. 12.50 RF = R2 + R3 (> 12R, oscillation starts) and falls below 12R when a diode conducts, which limits the amplitude. The amplitude estimate sets the current through RF equal to the value that the RC network needs at the peak, vO/(12R), with the equivalent circuit of D1 on (R4 in series with VD, in parallel with R3), the − input being a virtual ground.', \
        ['The book gives no amplitude formula for the phase-shift oscillator: the estimate above is derived here by analogy with Eq. (12.85), and VD = 0.6 V is assumed. The time-domain simulation of the piecewise-linear circuit gives a somewhat larger amplitude (checked within 30 %).', 'No supply voltage is given; the amplitude of about 10 V assumes supplies larger than that.'], cir('12.99', 'Fig. 12.50', 'phase-shift oscillator: three series capacitors C with two resistors R to ground (after the first and second capacitor) feeding the − input of an op amp; the feedback network RF = R2 in series with R3, with R4 and the anti-parallel diodes D1, D2 in parallel with R3.')
@solve('12.101')
def _():
    R, C = 10e3, 100e-12; wo = 1 / (R * C); fo = wo / (2 * math.pi)
    T = lambda s: (-1 / (s * R * C)) ** 4
    close(T(1j * wo), 1.0, 1e-12)                                                          # |T| = 1 and phase 0° at ωo = 1/RC
    poly = np.roots([1, 0, 0, 0, -(1 / (R * C)) ** 4]); assert any(abs(r - 1j * wo) < 1e-6 * wo for r in poly) and any(abs(r + 1j * wo) < 1e-6 * wo for r in poly)    # 1 − T(s) = 0  ⇒  s⁴ = (1/RC)⁴: poles at ±jωo (and ±ωo)
    ph = [complex(1, 0)]
    for k in range(3): ph.append(ph[-1] * (-1 / (1j * wo * R * C)))
    close(ph[-1] * (-1 / (1j * wo * R * C)), ph[0], 1e-12)
    names = ['1∠0°', '1∠90°', '1∠180°', '1∠270° (= 1∠−90°)']
    return [('(a) circuit', 'four identical inverting integrators (R from the input to the − input, C in feedback, + input grounded), each output driving the next; the output of the fourth is fed back to the input of the first (Fig. 10.34 integrator ×4)'), ('(b) frequency of oscillation', f'T(s) = (−1/sRC)⁴ = 1/(sRC)⁴ has gain 1 and phase 0° at ωo = 1/RC = {si(wo, "rad/s", 4)}: fo = 1/(2πRC) = {si(fo, "Hz", 4)}'), ('(c) phasors of the four outputs for Vo1 = 1∠0°', f'Vo1 = {names[0]}, Vo2 = {names[1]}, Vo3 = {names[2]}, Vo4 = {names[3]} (each integrator gives −1/j = +90° at ωo)')], \
        'Each ideal integrator has Vo/Vi = −1/(sRC); four in a ring give T(s) = 1/(sRC)⁴, which equals +1 at s = jωo with ωo = 1/RC (the phase of each stage is +90°, 4 × 90° = 360°). The characteristic equation s⁴ = (1/RC)⁴ has the roots ±jωo (and ±ωo); checked numerically. Part (d) (amplitude-stabilisation design for about 2 V) is a design choice and is not solved here.', \
        ['Part (a) is a drawing: it is described in words.', 'Part (d) is an open design (no specific stabilisation network is prescribed) and is not answered.', 'The ideal integrator ring also has a real root +ωo (a growing mode); the oscillation criterion used is the Barkhausen condition of the book.'], cir('12.101', 'Fig. 10.34', 'inverting integrator: input resistor R to the − input of the op amp, capacitor C in feedback, + input grounded (four of them are cascaded in a ring in this problem).')
def astable_sim(R, C, beta, VCC, VEE, n=6):
    from scipy.integrate import solve_ivp
    vC = -beta * VEE; high = True; times = []
    for _ in range(2 * n):
        tgt, thr = (VCC, beta * VCC) if high else (-VEE, -beta * VEE)
        ev = lambda t, v, thr=thr: v[0] - thr; ev.terminal = True
        s = solve_ivp(lambda t, v: [(tgt - v[0]) / (R * C)], [0, 60 * R * C], [vC], events=ev, rtol=1e-12, atol=1e-14)
        times.append(s.t_events[0][0]); vC = thr; high = not high
    return times
@solve('12.117')
def _():
    f0, VCC, VEE = 1e3, 5.0, 5.0; R1 = R2 = 12e3; beta = R1 / (R1 + R2); R = 15e3
    I = (VCC + beta * VEE) / R + VCC / (R1 + R2); assert I < 1e-3
    C = 1 / (f0 * 2 * R * math.log((1 + beta) / (1 - beta)))
    t = astable_sim(R, C, beta, VCC, VEE); close(t[2] + t[3], 1e-3, 1e-6)                    # period from the numerical simulation equals 1 ms
    f = lambda R_, C_, R1_, R2_, vcc=VCC, vee=VEE: 1 / (R_ * C_ * (math.log((1 + R1_ / (R1_ + R2_) * vee / vcc) / (1 - R1_ / (R1_ + R2_))) + math.log((1 + R1_ / (R1_ + R2_) * vcc / vee) / (1 - R1_ / (R1_ + R2_)))))
    vals = [f(R * (1 + a * .05), C * (1 + b * .10), R1 * (1 + c * .05), R2 * (1 + d * .05)) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1) for d in (-1, 1)]; fmin, fmax = min(vals), max(vals)
    rnd = random.Random(5)
    for _ in range(2000): x = f(R * (1 + rnd.uniform(-.05, .05)), C * (1 + rnd.uniform(-.1, .1)), R1 * (1 + rnd.uniform(-.05, .05)), R2 * (1 + rnd.uniform(-.05, .05))); assert fmin * (1 - 1e-9) <= x <= fmax * (1 + 1e-9)
    fc = f(R, C, R1, R2, 4.75, 5.25); tc = astable_sim(R, C, beta, 4.75, 5.25); close(1 / (tc[2] + tc[3]), fc, 1e-6)
    return [('(a) design (β = R1/(R1 + R2) = 0.5, symmetric supplies)', f'R1 = R2 = {si(R1, "Ω", 3)}, R = {si(R, "Ω", 3)}, C = T/(2R·ln 3) = {si(C, "F", 4)}  (T = 2RC·ln[(1 + β)/(1 − β)] = 1 ms)'), ('(a) peak output current (when the output switches)', f'(VCC + βVEE)/R + VCC/(R1 + R2) = {si(I, "A", 3)} < 1 mA'), ('(b) worst-case frequency (R ±5 %, C ±10 %)', f'{si(fmin, "Hz", 4)} to {si(fmax, "Hz", 4)} (nominal 1 kHz)'), ('(c) supplies +4.75 V and −5.25 V, nominal components', f'T1 = RC ln[(1 + βVEE/VCC)/(1 − β)], T2 = RC ln[(1 + βVCC/VEE)/(1 − β)]: f = {si(fc, "Hz", 4)}')], \
        'Astable multivibrator (Eqs. 12.91, 12.94, 12.95): T = T1 + T2 with T1 = RC·ln[(1 + βVEE/VCC)/(1 − β)], T2 = RC·ln[(1 + βVCC/VEE)/(1 − β)]; symmetric supplies: T = 2RC·ln[(1 + β)/(1 − β)]. The current limit is met at the switching instant, when the capacitor is at −βVEE. Worst case = extreme over the 16 corners of the tolerance box (confirmed by 2000 random sets); exact event-driven numerical simulation of the capacitor reproduces the period of the design and of case (c).', \
        ['The statement leaves free β, R and C: β = 0.5 with R1 = R2 = 12 kΩ and R = 15 kΩ is chosen (any other choice meeting the 1 mA limit works; only the product RC·ln[(1+β)/(1−β)] matters for the frequency).', '"Worst-case" means the minimum and maximum frequency over the tolerance extremes of R1, R2, R (±5 %) and C (±10 %).'], cir('12.117', 'Fig. 12.60', 'astable multivibrator: comparator (op amp) with positive-feedback divider R2 (from the output) and R1 (to ground) on the + input, and R from the output to the − input with C from the − input to ground; supplies VCC and −VEE.')
def mono(R, C, beta, VCC, VEE, VD):
    T = R * C * math.log((1 + VD / VCC) / (1 - beta)); Tr = R * C * math.log((1 + beta * VCC / VEE) / (1 - VD / VEE)); return T, Tr
def mono_sim(R, C, beta, VCC, VEE, VD):
    from scipy.integrate import solve_ivp
    ev1 = lambda t, v: v[0] - beta * VCC; ev1.terminal = True
    s1 = solve_ivp(lambda t, v: [(VCC - v[0]) / (R * C)], [0, 60 * R * C], [-VD], events=ev1, rtol=1e-12, atol=1e-14)
    ev2 = lambda t, v: v[0] + VD; ev2.terminal = True; ev2.direction = -1
    s2 = solve_ivp(lambda t, v: [(-VEE - v[0]) / (R * C)], [0, 60 * R * C], [beta * VCC], events=ev2, rtol=1e-12, atol=1e-14); return s1.t_events[0][0], s2.t_events[0][0]
@solve('12.119')
def _():
    R, C, R1, R2, VCC, VEE, VD = 51e3, 0.033e-6, 15e3, 27e3, 7.5, 7.5, 0.7; beta = R1 / (R1 + R2)
    bT, bTr = mono(11e3, 0.002e-6, 22 / 40, 5.0, 5.0, 0.7); close(bT, 20.4e-6, 5e-3); close(bT + bTr, 33.4e-6, 5e-3)                            # anchor: the exercise of Fig. 12.64 (20.4 µs and 33.4 µs between triggers) fixes VD = 0.7 V
    T, Tr = mono(R, C, beta, VCC, VEE, VD); sT, sTr = mono_sim(R, C, beta, VCC, VEE, VD); close(T, sT, 1e-6); close(Tr, sTr, 1e-6)
    return [('β = R1/(R1 + R2)', g(beta, 5)), ('RC', si(R * C, 's', 4)), ('Pulse width T = RC·ln[(1 + VD/VCC)/(1 − β)]', si(T, 's', 4)), ('Recovery time Tr = RC·ln[(1 + βVCC/VEE)/(1 − VD/VEE)]', si(Tr, 's', 4)), ('Minimum interval between triggers', si(T + Tr, 's', 4))], \
        'Monostable multivibrator (Eqs. 12.100 and 12.101): the capacitor starts at −VD (clamped by D2), charges toward VCC until it reaches βVCC (pulse width T) and then discharges from βVCC toward −VEE until D2 clamps it at −VD again (recovery time Tr). Numerical event simulation of the two exponentials gives the same times. Anchor: the book\'s exercise (Fig. 12.64: VCC = VEE = 5 V, R1 = 22 kΩ, R2 = 18 kΩ, R = 11 kΩ, C = 2 nF) gives 20.4 μs and 33.4 μs between triggers, which the formulas reproduce with VD = 0.7 V.', \
        ['The diode on-voltage is not given: VD = 0.7 V is used (it reproduces the book\'s exercise 20.4 μs / 33.4 μs).', 'R1 = 15 kΩ (to ground) and R2 = 27 kΩ (feedback) read from Fig. P12.116, with R = 51 kΩ and C = 0.033 μF; the supplies are ±7.5 V.'], cir('12.119', 'Fig. P12.116', 'astable-multivibrator comparator (op amp with the output-switching symbol): + input with 15 kΩ to ground and 27 kΩ from the output; 51 kΩ from the output to the − input with 0.033 μF from the − input to ground; supply +12 V (changed to ±7.5 V in this problem) and two diodes added as in Fig. 12.62.')
@solve('12.120')
def _():
    T, Tr, VCC, VEE, VD = 20e-6, 5e-6, 5.0, 5.0, 0.7
    f = lambda b: math.log((1 + VD / VCC) / (1 - b)) / math.log((1 + b * VCC / VEE) / (1 - VD / VEE)) - T / Tr
    beta = brentq(f, 0.1, 0.99, xtol=1e-14); RC = T / math.log((1 + VD / VCC) / (1 - beta)); R2R1 = 1 / beta - 1
    C = 100e-12; R = RC / C; R1 = 19e3; R2 = R1 * R2R1
    t, tr = mono(R, C, beta, VCC, VEE, VD); close(t, T, 1e-9); close(tr, Tr, 1e-9); sT, sTr = mono_sim(R, C, beta, VCC, VEE, VD); close(sT, T, 1e-6); close(sTr, Tr, 1e-6)
    assert beta * VEE > VD                                                                    # condition (12.98) for a single stable state
    return [('β from the ratio T/Tr = 4', f'β = R1/(R1 + R2) = {g(beta, 5)}  (R2/R1 = {g(R2R1, 4)})'), ('RC from T = RC·ln[(1 + VD/VCC)/(1 − β)]', si(RC, 's', 4)), ('Example choice', f'C = 100 pF → R = {si(R, "Ω", 4)}; R1 = 19 kΩ, R2 = {si(R2, "Ω", 4)} (≈ 1 kΩ gives β = 0.95)'), ('Check (formulas and numerical simulation)', f'T = {si(t, "s", 4)}, Tr = {si(tr, "s", 4)}; stability condition βVEE = {g(beta * VEE, 3)} V > VD')], \
        'Two equations (Eqs. 12.100, 12.101) fix β and RC: the ratio T/Tr = ln[(1 + VD/VCC)/(1 − β)] / ln[(1 + βVCC/VEE)/(1 − VD/VEE)] = 4 gives β by root finding, then RC = T/ln[(1 + VD/VCC)/(1 − β)]. R, C and R1 are then free choices.', \
        ['VD = 0.7 V is used (it reproduces the book\'s exercise 20.4 μs / 33.4 μs).', 'The requirement T/Tr = 4 forces β close to 1 (about 0.95): R2 must be only about 5 % of R1, so the design is sensitive to resistor tolerance; C = 100 pF and R1 = 19 kΩ are example choices.'], cir('12.120', 'Fig. 12.62', 'monostable multivibrator: comparator with divider R2 (from the output) and R1 (to ground) on the + input, R from the output to the − input with C from the − input to ground; trigger diode D1 and clamp diode D2 on the − input.')
@solve('12.114')
def _():
    VH, VL = 1.05, 0.95; Vs = 5.0; RA = 10e3; G = Vs / (VL * RA); RF = 5 / ((VH - VL) * G); RB = 1 / (G - 1 / RA - 1 / RF)
    def thr(vo):
        c = Ckt(); c.V('vs', 'a', '0', Vs); c.R('a', 'p', RA); c.R('p', '0', RB); c.V('vo', 'o', '0', vo); c.R('o', 'p', RF); v, _ = dc(c); return v['p']
    th, tl = thr(Vs), thr(0.0); close(th, VH, 1e-9); close(tl, VL, 1e-9)
    return [('Design equations (output 0 V / 5 V; node on the + input)', 'VL = 5·RB‖RF/(RA + RB‖RF) with output low, VH = VL + 5/(RF·G) with G = 1/RA + 1/RB + 1/RF'), ('Choice RA = 10 kΩ (as in the figure)', f'RF = {si(RF, "Ω", 4)}, RB = {si(RB, "Ω", 4)} (RF = 9.5·RA, RB = 0.2405·RA)'), ('Thresholds (exact circuit)', f'upper {g(th, 5)} V, lower {g(tl, 5)} V: centre {g((th + tl) / 2, 5)} V, hysteresis ±{g((th - tl) / 2, 4)} V')], \
        'Fig. P12.111 topology: the + input is the node of RA (to the 5-V supply), RB (to ground) and RF (to the comparator output, 0 V or 5 V), the input signal is applied to the − input. With the output high the node voltage is VH, with the output low VL; centre 1 V and hysteresis ±0.05 V need VL = 0.95 V and VH = 1.05 V, which give RF = 9.5·RA and RB = RA/4.158.', ['Only two conditions (centre, hysteresis) for three resistors: RA = 10 kΩ is chosen as in Fig. P12.111; the others follow (the nearest standard values should be chosen in practice).', 'The comparator output swings 0 V to 5 V (supply pins +5 V and ground in the figure).'], cir('12.114', 'Fig. P12.111', 'Schmitt trigger: comparator (supply 5 V and ground); + input node with 10 kΩ to a 5-V source, 15 kΩ to ground and 100 kΩ to the output; the signal vS on the − input.')
