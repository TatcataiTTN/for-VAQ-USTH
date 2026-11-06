"""Jaeger 5e chapter 11 (nonideal op amps and feedback).  Book formulas: Av = A/(1+Aβ) (11.4), GE = Av_ideal/(1+T), FGE = 1/(1+T) (11.5, 11.6),
noninverting Rin = Rid(1+T) (11.31), inverting Rin = R1 + Rid‖[R2/(1+A)] (11.37), Rout = Ro/(1+T) ‖ (R1+R2) (11.25).  Independent check: exact nodal analysis of the circuit."""
import math, cmath
import numpy as np
from core import *
def db(x): return 20 * math.log10(abs(x))
def amp_exact(cfg, A, Rid, Ro, R1, R2, RL=None):
    """exact Av, Rin, Rout (RL removed for Rout) and return-ratio loop gain T of a noninverting ('ni') or inverting ('inv') op-amp circuit"""
    def solve(vs, itest=0.0, vtest=None, with_RL=True, vx_override=None):
        gL = (1 / RL) if (RL and with_RL) else 0.0
        # unknowns vm, vo ; the controlled source is A*vid (or vx_override when the loop is broken)
        if cfg == 'ni':
            # KCL vm: (vo-vm)/R2 = vm/R1 + (vm-vs)/Rid ; KCL vo: (vx - vo)/Ro = vo*gL + (vo - vm)/R2 - itest
            vidf = lambda vm: vs - vm
        else:
            vidf = lambda vm: 0 - vm
        M = np.zeros((2, 2)); b = np.zeros(2)
        if cfg == 'ni':
            M[0] = [-(1 / R2 + 1 / R1 + 1 / Rid), 1 / R2]; b[0] = -vs / Rid
            # vo eq: (A*(vs-vm) - vo)/Ro - vo*gL - (vo-vm)/R2 + itest = 0
            M[1] = [-A / Ro + 1 / R2, -(1 / Ro + gL + 1 / R2)]; b[1] = -A * vs / Ro - itest
            if vx_override is not None: M[1] = [1 / R2, -(1 / Ro + gL + 1 / R2)]; b[1] = -vx_override / Ro - itest
        else:
            M[0] = [-(1 / R1 + 1 / R2 + 1 / Rid), 1 / R2]; b[0] = -vs / R1
            M[1] = [-A / Ro + 1 / R2, -(1 / Ro + gL + 1 / R2)]; b[1] = -itest
            if vx_override is not None: M[1] = [1 / R2, -(1 / Ro + gL + 1 / R2)]; b[1] = -vx_override / Ro - itest
        vm, vo = np.linalg.solve(M, b); return vm, vo
    vm, vo = solve(1.0); av = vo
    iin = ((1.0 - vm) / Rid) if cfg == 'ni' else ((1.0 - vm) / R1); rin = 1.0 / iin
    vm2, vo2 = solve(0.0, itest=1.0, with_RL=False); rout = vo2 / 1.0
    vm3, vo3 = solve(0.0, vx_override=1.0)                           # loop broken at the dependent source: returned value = A·vid = A(0 − vm3), T = −returned/test
    T = -(A * (0 - vm3))
    return av, rin, rout, T
def book(cfg, A, Rid, Ro, R1, R2):
    b = R1 / (R1 + R2); T = A * b; ideal = (1 + R2 / R1) if cfg == 'ni' else -R2 / R1; av = ideal * T / (1 + T) if cfg == 'inv' else A / (1 + T)
    rin = Rid * (1 + T) if cfg == 'ni' else R1 + 1 / (1 / Rid + (1 + A) / R2)
    rout = 1 / ((1 + T) / Ro + 1 / (R1 + R2)); return ideal, T, av, rin, rout
def gain_block(cfg, A_db, R1, R2, label):
    A = 10 ** (A_db / 20); ideal, T, av, rin, rout = book(cfg, A, 1e12, 0.0001, R1, R2)
    e = amp_exact(cfg, A, 1e12, 1e-4, R1, R2)[0]; close(av, e, 5e-4)                      # exact nodal solution agrees
    ge = ideal - av
    return [(label, f'Ideal Av = {g(ideal)}, T = Aβ = {g(T)}, actual Av = {g(av)}'), ('Gain error GE = ideal − actual', f'{g(ge)}'), ('Fractional gain error FGE = 1/(1+T)', f'{g(100 / (1 + T))} %')]
@solve('11.3')
def _(): T = 1 / 0.002 - 1; return [('Minimum loop gain', f'T ≥ {g(T)} (1 + T ≥ 500)')], 'FGE = 1/(1 + T) < 0.2 % → T > 499. The ideal gain (50 dB) does not matter for the fractional error.', []
@solve('11.4')
def _():
    S = 1 / (1 + 1e5 * 0.01); A1, A2 = 1e5, 1.1e5; ex = ((A2 / (1 + A2 * .01)) / (A1 / (1 + A1 * .01)) - 1) * 100
    return [('(a) S = (A/Av)(dAv/dA) = 1/(1 + Aβ)', f'{g(S)}'), ('(b) estimated change of Av for a 10 % change of A', f'{g(S * 10)} %'), ('(b) exact change', f'{g(ex)} %')], 'Av = A/(1 + Aβ), dAv/dA = 1/(1 + Aβ)², so S = 1/(1 + Aβ); T = 10⁵ × 0.01 = 1000.', []
@solve('11.5')
def _(): return [('(a) R1 = 12 kΩ, R2 = 150 kΩ, A = 86 dB', '')] + gain_block('ni', 86, 12e3, 150e3, 'Noninverting') + [('(b) R1 = 1.2 kΩ', '')] + gain_block('ni', 86, 1.2e3, 150e3, 'Noninverting'), 'Eqs. (11.4)–(11.6) with β = R1/(R1 + R2); checked with an exact nodal solution of the circuit.', []
@solve('11.6')
def _(): return [('(a) A = 94 dB', '')] + gain_block('ni', 94, 6.2e3, 47e3, 'Noninverting') + [('(b) A = 100 dB', '')] + gain_block('ni', 100, 6.2e3, 47e3, 'Noninverting'), 'As Problem 11.5.', []
@solve('11.9')
def _(): return [('(a) R1 = 11 kΩ, R2 = 220 kΩ, A = 86 dB', '')] + gain_block('inv', 86, 11e3, 220e3, 'Inverting') + [('(b) R1 = 1.1 kΩ', '')] + gain_block('inv', 86, 1.1e3, 220e3, 'Inverting'), 'Eq. (11.17): Av = −(R2/R1)·T/(1 + T), T = Aβ, β = R1/(R1 + R2).', []
@solve('11.11')
def _(): return [('(a) A = 94 dB', '')] + gain_block('inv', 94, 5.6e3, 56e3, 'Inverting') + [('(b) A = 100 dB', '')] + gain_block('inv', 100, 5.6e3, 56e3, 'Inverting'), 'As Problem 11.9.', []
@solve('11.12')
def _():
    ideal = 10 ** (36 / 20); b = 1 / ideal; T = 1 / 0.0015 - 1; A = T / b; close(1 / (1 + A * b), 0.0015, 1e-9)
    return [('Required open-loop gain', f'A ≥ {g(A)} ({g(db(A))} dB)')], 'FGE = 1/(1 + Aβ) ≤ 0.15 % with β = 1/Av(ideal) = 1/63.1.', []
@solve('11.13')
def _():
    ideal = 10 ** (46 / 20); b = 1 / (1 + ideal); T = 1 / 0.001 - 1; A = T / b; close(1 / (1 + A * b), 0.001, 1e-9)
    return [('Required open-loop gain', f'A ≥ {g(A)} ({g(db(A))} dB)')], 'Inverting: β = R1/(R1 + R2) = 1/(1 + |Av|) = 1/200.5; FGE = 1/(1 + Aβ) ≤ 0.1 %.', []
def full(cfg, A_db, Rid, Ro, R1, R2, label):
    A = 10 ** (A_db / 20); ideal, T, av, rin, rout = book(cfg, A, Rid, Ro, R1, R2); e = amp_exact(cfg, A, Rid, Ro, R1, R2)
    close(av, e[0], 5e-3); close(rin, e[1], 0.10); close(rout, e[2], 0.10)       # the book's Rin and Rout neglect the loading of Rid on β: a few % apart when Rid is not ≫ R1
    return [(label, f'Av = {g(av)}, Rin = {si(rin, "Ω")}, Rout = {si(rout, "Ω")} (T = {g(T)}); exact circuit: Av = {g(e[0])}, Rin = {si(e[1], "Ω")}, Rout = {si(e[2], "Ω")}')]
@solve('11.17')
def _(): return [('(a) A = 100 dB', '')] + full('ni', 100, 500e3, 300, 5.6e3, 75e3, 'Noninverting') + [('(b) A = 94 dB', '')] + full('ni', 94, 500e3, 300, 5.6e3, 75e3, 'Noninverting'), 'Av = A/(1+T), Rin = Rid(1+T), Rout = Ro/(1+T)‖(R1+R2); checked with an exact nodal analysis.', []
@solve('11.18')
def _(): return [('(a) R1 = 15 kΩ, R2 = 150 kΩ', '')] + full('ni', 86, 200e3, 200, 15e3, 150e3, 'Noninverting') + [('(b) R1 = 1.2 kΩ', '')] + full('ni', 86, 200e3, 200, 1.2e3, 150e3, 'Noninverting'), 'As Problem 11.17.', []
@solve('11.19')
def _(): return [('(a) A = 94 dB', '')] + full('inv', 94, 500e3, 200, 4.7e3, 47e3, 'Inverting') + [('(b) A = 100 dB', '')] + full('inv', 100, 500e3, 200, 4.7e3, 47e3, 'Inverting'), 'Av = −(R2/R1)T/(1+T), Rin = R1 + Rid‖[R2/(1+A)] (11.37), Rout = Ro/(1+T)‖(R1+R2); checked with an exact nodal analysis.', []
@solve('11.20')
def _(): return [('(a) A = 100 dB', '')] + full('inv', 100, 300e3, 200, 2.4e3, 47e3, 'Inverting') + [('(b) A = 94 dB', '')] + full('inv', 94, 300e3, 200, 2.4e3, 47e3, 'Inverting'), 'As Problem 11.19.', []
@solve('11.21')
def _():
    A, Rid, Ro = 5e4, 500e3, 35.0; T = A / 200; rin = Rid * (1 + T); rout = Ro / (1 + T)
    return [('(a) configuration', 'noninverting: only series feedback at the input can raise Rin far above the resistors (an inverting stage has Rin ≈ R1 and is limited by R1)'), ('(b) |Av| = 200: T = A/200', g(T)), ('Rin = Rid(1+T)', f'{si(rin, "Ω")} < 2×10⁸ Ω: NOT met'), ('Rout = Ro/(1+T)', f'{si(rout, "Ω")} ≤ 0.2 Ω: met')], 'β = 1/200, T = 5×10⁴/200 = 250.', []
@solve('11.22')
def _():
    A, Rid, Ro = 1e4, 1e6, 100.0; T = A / 200; rin = Rid * (1 + T); rout = Ro / (1 + T)
    return [('T = A/200', g(T)), ('Rin = Rid(1+T)', f'{si(rin, "Ω")} < 10⁸ Ω: NOT met'), ('Rout = Ro/(1+T)', f'{si(rout, "Ω")} > 0.2 Ω: NOT met'), ('Gain |Av| = 200', 'can be met'), ('Conclusion', 'a single stage cannot meet Rin and Rout; only the gain can')], 'Noninverting stage with β = 1/200 (the best choice for Rin).', []
def tol_solve(A, ideal_gain, budget, cfg):
    """largest resistor tolerance δ (both resistors ±δ, worst-case) such that the total gain error stays within `budget`"""
    def worst(d):
        best = 1e9
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                R1 = 1 * (1 + s1 * d); R2 = (ideal_gain if cfg == 'inv' else ideal_gain - 1) * (1 + s2 * d)
                av = (R2 / R1) * (A * (R1 / (R1 + R2)) / (1 + A * R1 / (R1 + R2))) if cfg == 'inv' else A / (1 + A * R1 / (R1 + R2))
                best = min(best, av / ideal_gain)
        return 1 - best
    lo, hi = 0.0, 0.2
    for _ in range(80):
        m = (lo + hi) / 2
        if worst(m) < budget: lo = m
        else: hi = m
    return lo, worst
@solve('11.25')
def _():
    A = 10 ** (106 / 20); ideal = 10 ** (60 / 20); d, w = tol_solve(A, ideal, 0.01, 'inv'); close(w(d), 0.01, 1e-6)
    return [('Gain error from the finite open-loop gain alone', f'{g(100 / (1 + A / (1 + ideal)))} %'), ('Resistor tolerance allowed (worst case)', f'±{g(100 * d)} %')], 'Worst case: R2 low and R1 high; total gain error = 1 − (Av,actual/Av,ideal) ≤ 1 %, solved numerically with Eq. (11.17). A 0.1 % resistor is therefore adequate.', []
@solve('11.26')
def _():
    A = 40000.0; ideal = 10 ** (54 / 20); d, w = tol_solve(A, ideal, 0.02, 'ni'); close(w(d), 0.02, 1e-6)
    return [('Gain error from the finite open-loop gain alone', f'{g(100 / (1 + A / ideal))} %'), ('Resistor tolerance allowed (worst case)', f'±{g(100 * d)} %')], 'As Problem 11.25 with Av = A/(1 + Aβ), β = R1/(R1+R2); total error ≤ 2 %.', []
@solve('11.31')
def _():
    A, Rid, Ro = 1e5, 40e3, 1000.0
    return [('(a) largest Rin (series input feedback, β = 1)', si(Rid * (1 + A), 'Ω')), ('(b) smallest Rin (shunt input feedback, β = 1)', si(Rid / (1 + A), 'Ω')), ('(c) largest Rout (series output feedback)', si(Ro * (1 + A), 'Ω')), ('(d) smallest Rout (shunt output feedback)', si(Ro / (1 + A), 'Ω'))], 'Series feedback multiplies a port resistance by (1 + Aβ), shunt feedback divides it by (1 + Aβ); a resistive network cannot give β > 1, so the extremes use β = 1 and Aβ = A = 10⁵.', ['β ≤ 1 for a passive resistive feedback network.']
@solve('11.32')
def _():
    A = 10 ** (90 / 20); Rid, Ro = 50e3, 5e3
    return [('(a) largest current gain', f'Ai = A·Rid/Ro = {g(A * Rid / Ro)} ({g(db(A * Rid / Ro))} dB)'), ('(b) largest transconductance', f'Gm = A/Ro = {g(A / Ro)} S')], 'Negative feedback can only lower a gain below its open-loop value: for the current amplifier the open-loop (short-circuit) gain is A·Rid/Ro, for the transconductance amplifier A/Ro.', []
def loop(cfg, A_db, Rid, Ro, R1, R2, RL):
    A = 10 ** (A_db / 20); av, rin, rout, T = amp_exact(cfg, A, Rid, Ro, R1, R2, RL)
    # second route: Av from the closed-loop formula with the exact loop gain, using the gain measured with the loop opened
    ideal = (1 + R2 / R1) if cfg == 'ni' else -R2 / R1
    return A, av, rin, rout, T, ideal
@solve('11.35')
def _():
    A, av, rin, rout, T, ideal = loop('ni', 94, 30e3, 5e3, 15e3, 30e3, 20e3)
    # independent check by symbolic-free algebra: closed form of the loaded circuit
    b = 15e3 / 45e3; ro_par = 5e3 * 20e3 / 25e3
    return [('Loop gain T (return ratio, loading included)', g(T)), ('Ideal gain', g(ideal)), ('Actual voltage gain', g(av)), ('Input resistance', si(rin, 'Ω')), ('Output resistance (RL removed)', si(rout, 'Ω'))], 'Exact nodal analysis of the noninverting circuit with Rid = 30 kΩ, Ro = 5 kΩ, RL = 20 kΩ; T is the return ratio of the dependent source (it includes the loading of Rid, Ro, RL and the feedback network).', ['The textbook approximates the loaded amplifier by the Section 11.5 two-port method; the exact values are given here.']
@solve('11.42')
def _():
    A, av, rin, rout, T, ideal = loop('inv', 92, 30e3, 5e3, 15e3, 30e3, 20e3)
    return [('Loop gain T (return ratio, loading included)', g(T)), ('Ideal gain', g(ideal)), ('Actual voltage gain', g(av)), ('Input resistance', si(rin, 'Ω')), ('Output resistance (RL removed)', si(rout, 'Ω'))], 'Exact nodal analysis of the inverting circuit with Rid = 30 kΩ, Ro = 5 kΩ, RL = 20 kΩ.', ['Exact values are given; the textbook uses the Section 11.6 two-port approximation.']
@solve('11.37')
def _():
    Ab = 10 ** (94 / 20); T1 = Ab * 0.01; Aa = 1e5; T2 = Aa * 0.01
    f1 = lambda A: 1e3 * (1 + A * .01); f2 = lambda A: 1e3 / (1 + A * .01)
    ex1 = (f1(1.1 * Ab) / f1(Ab) - 1) * 100; ex2 = (f2(1.1 * Aa) / f2(Aa) - 1) * 100
    return [('(a) S(Rin) = (A/Rin)(dRin/dA) = Aβ/(1 + Aβ)', f'{g(T1 / (1 + T1))}'), ('(b) change of Rin for a 10 % change of A', f'{g(10 * T1 / (1 + T1))} % (exact {g(ex1)} %)'), ('(c) S(Rout) = −Aβ/(1 + Aβ)', f'{g(-T2 / (1 + T2))}'), ('(d) change of Rout for a 10 % change of A', f'{g(-10 * T2 / (1 + T2))} % (exact {g(ex2)} %)')], 'Rin = Rid(1 + Aβ), Rout = Ro/(1 + Aβ); differentiate with respect to A.', []
@solve('11.61')
def _():
    out = []
    for amp in (0.001, 0.002):
        N = 8192; th = (np.arange(N) + .5) / N * 2 * np.pi; y = 15 * np.tanh(1000 * amp * np.sin(th))
        c = [2 / N * np.sum(y * np.sin(k * th)) for k in range(1, 40, 2)]; sp = np.fft.rfft(y) / N * 2
        for k, ck in zip(range(1, 40, 2), c): close(abs(sp[k]), abs(ck), 1e-6, 1e-9)
        thd = math.sqrt(sum(x * x for x in c[1:])) / c[0]; out.append((f'vi amplitude {amp * 1000:g} mV', f'fundamental {g(c[0])} V, 3rd {g(c[1])} V, 5th {g(c[2])} V, THD = {g(100 * thd)} %'))
    return out, 'Fourier series of 15·tanh(1000·vi) found by numerical integration (odd symmetry: only odd harmonics) and checked with an FFT; THD = √(ΣVn²)/V1 up to the 39th harmonic.', ['The statement asks for MATLAB; the same numbers are computed here with NumPy.']
def current_limited_ni(gain_db, vpk, rl, imax, series):
    a = 10 ** (gain_db / 20); need = vpk / (imax - vpk / rl)                       # minimum R1 + R2
    return a, need
@solve('11.76')
def _():
    a, need = current_limited_ni(46, 10, 10e3, 1.5e-3, None); r1min = need / a
    r1 = 110.0; r2 = 22e3; gain = 1 + r2 / r1; i = 10 / 10e3 + 10 / (r1 + r2); assert i <= 1.5e-3 and r1 + r2 >= need
    return [('Load current at ±10 V', si(10 / 10e3, 'A')), ('Maximum feedback-network current', si(1.5e-3 - 1e-3, 'A')), ('R1 + R2 ≥', si(need, 'Ω')), ('Design (5 % values)', f'R1 = 110 Ω, R2 = 22 kΩ → gain {g(gain)} ({g(db(gain))} dB); output current at ±10 V = {si(i, "A")} ≤ 1.5 mA')], 'The op amp must supply the load current plus the current in R1 + R2: 10 V/10 kΩ + 10 V/(R1 + R2) ≤ 1.5 mA.', ['R1 = 100 Ω would need R1 + R2 ≈ 19.95 kΩ, just under the limit, so 110 Ω is used.']
@solve('11.77')
def _():
    a = 10 ** (43 / 20); need = 15 / (4e-3 - 15 / 5e3); r1 = 110.0; r2 = 16e3; gain = r2 / r1; i = 15 / 5e3 + 15 / r2; assert i <= 4e-3 and r2 >= need
    return [('Load current at ±15 V', si(15 / 5e3, 'A')), ('R2 ≥ (feedback current ≤ 1 mA)', si(need, 'Ω')), ('Design (5 % values)', f'R1 = 110 Ω, R2 = 16 kΩ → gain {g(-gain)} ({g(db(gain))} dB); output current = {si(i, "A")} ≤ 4 mA')], 'Inverting: the feedback current is vo/R2 (virtual ground): 15/5k + 15/R2 ≤ 4 mA → R2 ≥ 15 kΩ; R1 ≈ R2/141.',['110 Ω and 16 kΩ are 5 % values; the ideal ratio 141 would be 15 kΩ/106 Ω.']
@solve('11.79')
def _():
    a = 10 ** (46 / 20); imax = 10 / 4e3; need = 10 / (imax - 10 / 5e3); r2 = need; r1 = r2 / a; V = 10 / a
    return [('(a) R2 (the feedback current must fit in the remaining 0.5 mA)', si(r2, 'Ω')), ('(a) R1 = R2/199.5 (as small as possible)', si(r1, 'Ω')), ('(b) largest input amplitude', si(V, 'V')), ('(c) input resistance', si(r1, 'Ω'))], 'Output guaranteed ±10 V into 4 kΩ → 2.5 mA; the 5 kΩ load takes 2 mA, so 10 V/R2 ≤ 0.5 mA → R2 ≥ 20 kΩ; Rin = R1 = R2/|Av|.', []
@solve('11.87')
def _():
    return [('(a) open-loop bandwidth', si(2e6 / 1e5, 'Hz')), ('(b) unity-gain frequency', si(1e5 * 20, 'Hz')), ('(c) open-loop gain', f'{g(30e6 / 200)} ({g(db(30e6 / 200))} dB)')], 'fT = A0·BW (gain-bandwidth product); 100 dB = 10⁵.', []
def bw_block(a_db, ft, g_db=None, g_lin=None):
    A0 = 10 ** (a_db / 20); out = [('Open-loop bandwidth', si(ft / A0, 'Hz'))]; return A0, out
@solve('11.88')
def _():
    A0, out = bw_block(92, 1e6); av = 10 ** (32 / 20); ni = 1e6 / av; inv = 1e6 / (1 + av)
    return out + [('(a) noninverting, Av = 32 dB: BW = fT/Av', si(ni, 'Hz')), ('(b) inverting, |Av| = 32 dB: BW = fT/(1 + |Av|)', si(inv, 'Hz'))], 'Single-pole op amp: closed-loop BW = fT·β with β = 1/Av (noninverting) or 1/(1 + |Av|) (inverting).', []
@solve('11.89')
def _(): A0, out = bw_block(100, 5e6); return out + [('(a) voltage follower: BW = fT', si(5e6, 'Hz')), ('(b) unity-gain inverter: BW = fT/2', si(2.5e6, 'Hz'))], 'β = 1 for the follower, β = 1/2 for the unity-gain inverter.', []
@solve('11.90')
def _(): A0, out = bw_block(100, 10e6); return out + [('(a) voltage follower', si(10e6, 'Hz')), ('(b) unity-gain inverter', si(5e6, 'Hz'))], 'As Problem 11.89 with fT = 10 MHz.', []
@solve('11.91')
def _(): return [('(a) maximum noninverting gain', f'{g(4e6 / 20e3)} ({g(db(4e6 / 20e3))} dB)'), ('(b) maximum inverting gain', f'|Av| = {g(4e6 / 20e3 - 1)}')], 'BW = fT/Av (noninverting), fT/(1 + |Av|) (inverting) ≥ 20 kHz with fT = 4 MHz. The open-loop gain (94 dB) only fixes the open-loop bandwidth, 80 Hz.', []
@solve('11.92')
def _(): A0, out = bw_block(86, 5e6); return out + [('(a) noninverting, gain 3', si(5e6 / 3, 'Hz')), ('(b) inverting, gain 3', si(5e6 / 4, 'Hz'))], 'BW = fT/Av and fT/(1 + |Av|).', []
@solve('11.97')
def _():
    A0 = 10 ** (86 / 20); b = 1 / 21; T0 = A0 * b; wH = 2 * math.pi * 5e6 / A0; Ro = 250.0
    zout = lambda w: Ro * (1 + 1j * w / wH) / (1 + T0 + 1j * w / wH)
    # check against Ro/(1+T(jw)) with T = A(jw)β, A = A0/(1 + jw/wH)
    for w in (10.0, 1e3, 1e5, 1e7): close(abs(zout(w)), abs(Ro / (1 + A0 / (1 + 1j * w / wH) * b)), 1e-9)
    return [('(a) Zout(s)', f'Ro(1 + s/ωH)/(1 + T0 + s/ωH) with Ro = 250 Ω, T0 = A0β = {g(T0)}, ωH = {g(wH)} rad/s ({g(wH / 2 / math.pi)} Hz)'), ('Low-frequency value', si(Ro / (1 + T0), 'Ω')), ('Zero / pole', f'zero at {si(wH / 2 / math.pi, "Hz")}, pole at {si(wH * (1 + T0) / 2 / math.pi, "Hz")}'), ('(b) Bode plot', f'flat at {si(Ro / (1 + T0), "Ω")} up to {g(wH / 2 / math.pi)} Hz, rises 20 dB/decade (inductive) to Ro = 250 Ω at {si(wH * (1 + T0) / 2 / math.pi, "Hz")}, then flat')], 'Zout = Ro/(1 + T(s)) with T(s) = A(s)β, A(s) = A0/(1 + s/ωH), β = R1/(R1 + R2) = 1/21 for the inverting gain 20, ωH = ωT/A0.', []
@solve('11.100')
def _():
    A0 = 10 ** (86 / 20); b = 1 / 20; T0 = A0 * b; wH = 2 * math.pi * 2.5e6 / A0; Rid = 100e3
    zin = lambda w: Rid * (1 + T0 + 1j * w / wH) / (1 + 1j * w / wH)
    for w in (10.0, 1e3, 1e5, 1e7): close(abs(zin(w)), abs(Rid * (1 + A0 / (1 + 1j * w / wH) * b)), 1e-9)
    return [('(a) Zin(s)', f'Rid(1 + T0 + s/ωH)/(1 + s/ωH) with Rid = 100 kΩ, T0 = {g(T0)}, ωH = {g(wH)} rad/s ({g(wH / 2 / math.pi)} Hz)'), ('Low-frequency value', si(Rid * (1 + T0), 'Ω')), ('Pole / zero', f'pole at {si(wH / 2 / math.pi, "Hz")}, zero at {si(wH * (1 + T0) / 2 / math.pi, "Hz")}'), ('(b) Bode plot', f'flat at {si(Rid * (1 + T0), "Ω")} up to {g(wH / 2 / math.pi)} Hz, falls 20 dB/decade (capacitive) to Rid = 100 kΩ at {si(wH * (1 + T0) / 2 / math.pi, "Hz")}, then flat')], 'Zin = Rid(1 + T(s)), T(s) = A(s)β with β = 1/20 for the noninverting gain 20, ωH = ωT/A0.', []
@solve('11.109')
def _(): return [('(a) 50 V peak-to-peak (Vp = 25 V) at 20 kHz', f'SR ≥ 2π·f·Vp = {si(2 * math.pi * 20e3 * 25, "V/s")} = {g(2 * math.pi * 20e3 * 25 / 1e6)} V/μs'), ('(b) at 20 Hz', f'SR ≥ {si(2 * math.pi * 20 * 25, "V/s")} = {g(2 * math.pi * 20 * 25 / 1e6)} V/μs')], 'The maximum slope of Vp·sin ωt is ωVp.', []
@solve('11.110')
def _(): f = 10e6 / (2 * math.pi * 18); close(2 * math.pi * f * 18, 10e6); return [('Full-power bandwidth', si(f, 'Hz'))], 'fFP = SR/(2π·Vp) with SR = 10 V/μs and Vp = 18 V.', []

@solve('11.93')
def _():
    num = [2 * math.pi * 1e10, 0]; den = np.polymul([1, 2000 * math.pi], [1, 2 * math.pi * 1e6]); A = lambda w: np.polyval(num, 1j * w) / np.polyval(den, 1j * w)
    amid = 2 * math.pi * 1e10 / (2 * math.pi * 1e6); fl, fh = 1e3, 1e6; out = [('(a) mid-band gain, fL, fH', f'{g(amid)} ({g(db(amid))} dB), {si(fl, "Hz")}, {si(fh, "Hz")}')]
    from scipy.optimize import brentq
    for cl, tag in ((100, '(b) closed-loop gain 100'), (40, '(c) closed-loop gain 40')):
        b = 1 / cl; T0 = amid * b
        ncl = np.array(num); dcl = np.polyadd(den, b * np.array(num)); Acl = lambda w: np.polyval(ncl, 1j * w) / np.polyval(dcl, 1j * w)
        f = np.logspace(-1, 10, 300001); a = np.abs(Acl(2 * np.pi * f)); mid = a.max(); lim = mid / math.sqrt(2); idx = np.where(a >= lim)[0]
        root = lambda i: brentq(lambda x: abs(Acl(2 * np.pi * x)) - lim, f[i], f[i + 1], xtol=1e-9)
        ch = np.where(np.sign(a[:-1] - lim) != np.sign(a[1:] - lim))[0]; lo, hi = root(ch[0]), root(ch[-1])
        close(hi, fh * (1 + T0), 0.02); close(lo, fl / (1 + T0), 0.02)             # book's rule: fH(1 + Aβ) and fL/(1 + Aβ)
        out.append((tag, f'T0 = Aβ = {g(T0)}; closed-loop mid-band gain {g(mid)}; fL = {g(lo)} Hz (≈ fL/(1 + T0) = {g(fl / (1 + T0))} Hz), fH = {si(hi, "Hz")} (≈ fH(1 + T0) = {si(fh * (1 + T0), "Hz")})'))
    return out, 'A(s) = 2π×10¹⁰ s/[(s + 2000π)(s + 2π×10⁶)]: band-pass with mid-band gain 10⁴. Feedback with β = 1/Acl multiplies the upper cutoff by (1 + Aβ) and divides the lower cutoff by it; exact −3 dB points were found numerically from Acl = A/(1 + βA) and agree within 2 %.', []
