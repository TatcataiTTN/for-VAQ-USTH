"""Jaeger 5e Chapter 10 problems that refer to a figure (Figs. 10.22–10.35, P10.27–P10.117).  Each solver reads the figure (see `circuit`), applies the book's formulas and re-checks the result with
an exact modified-nodal solution of the circuit (mna.py), a numerical experiment or the printed worked examples of the same chapter."""
import math, os, sys, json
import numpy as np
from core import *
from mna import Ckt, dc
from fighelp import cir, dbv
INV = 'inverting amplifier: vI (source with the resistor R1) → R1 → the − input, feedback resistor R2 from the output to the − input, + input grounded; the currents iI and io are marked'
def inv_amp(R1, R2, vi, Rs=0.0):
    c = Ckt(); c.V('vi', 'in', '0', vi); c.R('in', 'x', R1 + Rs); c.opamp('0', 'x', 'o'); c.R('x', 'o', R2); v, i = dc(c); return v['o'], i['vi']
def noninv(R1, R2, vi):
    c = Ckt(); c.V('vi', 'in', '0', vi); c.opamp('in', 'm', 'o'); c.R('o', 'm', R2); c.R('m', '0', R1); v, i = dc(c); return v['o'], v['m'], i['vi']
@solve('10.27')
def _():
    rng = np.random.default_rng(7); lo, hi = 1e9, -1e9
    for _ in range(300):                                                   # random resistor-diode networks fed from +15 V, −9 V and 0 V (piecewise-linear diodes, 0.6 V drop)
        n = 5; nodes = list(range(n)); R = []; D = []
        for a in range(n + 3):
            for b in range(a + 1, n + 3):
                if rng.random() < 0.5: R.append((a, b, 10 ** rng.uniform(2, 5)))
                elif rng.random() < 0.3: D.append((a, b))
        src = {n: 15.0, n + 1: -9.0, n + 2: 0.0}; v = np.zeros(n + 3); on = {d: False for d in D}
        for _it in range(40):
            Y = np.zeros((n + 3, n + 3)); 
            for a, b, r in R: Y[a, a] += 1 / r; Y[b, b] += 1 / r; Y[a, b] -= 1 / r; Y[b, a] -= 1 / r
            I = np.zeros(n + 3)
            for (a, b), s_ in on.items():
                if s_: g_ = 1 / 50.0; Y[a, a] += g_; Y[b, b] += g_; Y[a, b] -= g_; Y[b, a] -= g_; I[a] += 0.6 * g_; I[b] -= 0.6 * g_       # forward-biased diode: V_anode − V_cathode = 0.6 + 50 Ω·I
            free = list(range(n)); fx = list(src)
            for k in fx: Y[k, k] += 1e9; I[k] += 1e9 * src[k]
            try: vn = np.linalg.solve(Y, I)
            except np.linalg.LinAlgError: break
            new = {d: (vn[d[0]] - vn[d[1]] > 0.6) for d in D}
            if new == on: break
            on = new
        else: continue
        lo = min(lo, vn[:n].min()); hi = max(hi, vn[:n].max())
    assert hi <= 15.0 + 1e-6 and lo >= -9.0 - 1e-6, (lo, hi)
    return [('(a) largest possible VO', '+15 V'), ('(b) smallest possible VO', '−9 V')], 'A network of resistors and diodes contains no source: every node voltage is a weighted average of the voltages of the nodes it is connected to (a diode can only lower it), so no node can lie above the highest supply (+15 V) or below the lowest (−9 V). VO can come close to +15 V (tied to that terminal through a small resistance and a conducting diode) and to −9 V, but not to +6 V or 0 V as extremes: those are intermediate values.', \
        [f'Random resistor–diode networks fed from +15 V, −9 V and 0 V were solved (300 networks, ideal 0.6 V diodes): all node voltages stayed between {lo:.2f} V and {hi:.2f} V, inside the limits.', 'The “most nearly” answers are the limits; the exact extremes also lose a diode drop.'], cir('10.27', 'Fig. P10.27', 'a box containing only resistors and diodes with the terminals +15 V, −9 V, ground and the output vO.')
@solve('10.28')
def _():
    import fitz
    pts = [(0, 14), (0.3, 14), (0.5, 12), (0.7, 4), (0.9, 2), (1.2, 2)]                                                  # vertices of the piecewise-linear transfer curve read from the figure
    gain = (4 - 12) / (0.7 - 0.5); VB = 0.6; VM = 0.1
    f = lambda v: float(np.interp(v, [p[0] for p in pts], [p[1] for p in pts])); t = np.linspace(0, 2 * math.pi, 2001); out = np.array([f(VB + VM * np.sin(x)) for x in t])
    close(float((out.max() - out.min()) / 2), 4.0, 1e-6); close(float(out.mean()), 8.0, 1e-6)                                # independent: drive the curve with VB + VM sin and measure
    big = np.array([f(VB + 0.12 * np.sin(x)) for x in t]); assert abs(float((big.max() - big.min()) / 2) - 4.8) > 0.2                    # a larger VM leaves the straight segment (0.5–0.7 V): the output is no longer a scaled sine
    return [('(a) small-signal gain at VB = 0.6 V', f'Av = ΔvO/ΔvI = (4 V − 12 V)/(0.7 V − 0.5 V) = {g(gain, 3)} V/V'), ('(a) largest undistorted VM', '0.1 V (the segment is straight between vI = 0.5 V and 0.7 V)'), ('(b) vI(t)', 'vI(t) = 0.6 + VM sin 1000t V'), ('(b) vO(t)', f'vO(t) = 8 − 40·VM sin 1000t V (for VM = 0.1 V: 8 − 4 sin 1000t V)')], \
        'The amplifier is linear only where the transfer curve is straight: around vI = 0.6 V the curve falls from (0.5 V, 12 V) to (0.7 V, 4 V), a slope of −40; the bias point is vO = 8 V, so vO = 8 − 40(vI − 0.6).', ['The vertices (0.3, 14), (0.5, 12), (0.7, 4), (0.9, 2) were read from the figure.'], cir('10.28', 'Fig. P10.28', 'transfer characteristic vO (0 to 14 V) versus vI (0 to 1.2 V) of an amplifier: 14 V up to 0.3 V, then a straight fall through (0.5 V, 12 V) and (0.7 V, 4 V) to 2 V at 0.9 V, then flat.')
def amp38(Rid, Ro, Adb, RI, RL):
    A = 10 ** (Adb / 20); c = Ckt(); c.V('vi', 'in', '0', 1.0); c.R('in', 'id', RI); c.R('id', '0', Rid); c.E('E', 'x', '0', 'id', '0', A); c.R('x', 'o', Ro); c.R('o', '0', RL); v, i = dc(c)
    return A, v['o'], v['id'], i['vi']
M38 = 'an amplifier model: signal source vi in series with RI drives the amplifier input resistance Rid (voltage vid across it); the output is a dependent source A·vid in series with Ro driving the load RL'
@solve('10.38')
def _():
    Rid, Ro, Adb, RI, RL = 1e6, 25.0, 60.0, 5e3, 600.0; A = 10 ** (Adb / 20); Av = Rid / (Rid + RI) * A * RL / (RL + Ro); ii = 1 / (RI + Rid); Ai = Av * (RI + Rid) / RL; AP = Av * Ai
    A_, vo, vid, i_ = amp38(Rid, Ro, Adb, RI, RL); close(vo, Av, 1e-9); close(-i_ * 1.0 * 0 + (1 / (RI + Rid)), -i_ if i_ < 0 else i_, 1e-9)
    VI = 10.0 / Av
    return [('(a) overall voltage gain Av = vo/vi', f'{g(Av, 4)} = {g(dbv(Av), 4)} dB'), ('(a) current gain Ai = io/ii', f'{g(Ai, 4)} = {g(dbv(Ai), 4)} dB'), ('(a) power gain AP = Av·Ai', f'{g(AP, 4)} = {g(10 * math.log10(AP), 4)} dB'), ('(b) amplitude of vi for 20 V p-p at vo', f'VI = 10 V/Av = {g(VI, 4)} V')], \
        'Voltage divider RI–Rid at the input, the gain A = 60 dB = 1000, and the divider Ro–RL at the output: Av = [Rid/(Rid + RI)]·A·[RL/(RL + Ro)]; ii = vi/(RI + Rid), io = vo/RL; AP = Po/Pi = Av·Ai.', ['AP is taken as Av·Ai (source voltage and source current), the textbook definition of power gain from vi and ii.', 'RI = 5 kΩ and RL = 600 Ω are given in the statement; Rid = 1 MΩ, Ro = 25 Ω and A = 60 dB are the parameters listed under it.'], cir('10.38', 'Fig. P10.38', M38 + ' (Rid = 1 MΩ, Ro = 25 Ω, A = 60 dB; RI = 5 kΩ, RL = 600 Ω).')
@solve('10.39')
def _():
    Rid, Ro, Adb, RI, RL = 5e3, 1e3, 30.0, 5e3, 600.0; A = 10 ** (Adb / 20); Av = Rid / (Rid + RI) * A * RL / (RL + Ro); VI = 7.5 / Av
    A_, vo, vid, i_ = amp38(Rid, Ro, Adb, RI, RL); close(vo, Av, 1e-9)
    PL = 0.5; io = math.sqrt(PL / RL); vo_ = io * RL; vid_ = vo_ * (RL + Ro) / (A * RL); P_Ro = io ** 2 * Ro; P_Rid = vid_ ** 2 / Rid; P_dep = A * vid_ * io
    close(P_dep, PL + P_Ro, 1e-9)                                                                                                                         # power balance: the dependent source delivers the load power plus the loss in Ro
    return [('(a) overall gain Av', f'{g(Av, 4)}'), ('(a) amplitude of vi for 15 V p-p at vo', f'VI = 7.5 V/Av = {g(VI, 4)} V'), ('(b) io, vo for 0.5 W in RL', f'io = {si(io, "A", 3)}, vo = {g(vo_, 4)} V (peak values)'), ('(b) power dissipated in the amplifier model', f'in Ro: {g(P_Ro, 4)} W; in Rid: {si(P_Rid, "W", 3)}; total ≈ {g(P_Ro + P_Rid, 4)} W (the dependent source delivers {g(P_dep, 4)} W)')], \
        'Av = [Rid/(Rid + RI)]·A·[RL/(RL + Ro)] with RI = 5 kΩ, RL = 600 Ω (Problem 10.38); for 0.5 W in RL the load current is √(PL/RL) and the amplifier dissipates io²·Ro in its output resistance plus vid²/Rid in its input resistance.', ['The statement says the amplifier is “designed to match” the source and load of Problem 10.38, but its listed Ro = 1 kΩ is not 600 Ω: the load RL = 600 Ω is kept.', 'Powers are for sinusoidal peak amplitudes: the 0.5 W is taken as the power in RL with io, vo as the rms-equivalent quantities (the ratios do not change).', '“Power dissipated in the amplifier” is read as the loss in the model resistances Ro and Rid; the dependent source supplies it.'], cir('10.39', 'Fig. P10.38', M38 + ' (Rid = 5 kΩ, Ro = 1 kΩ, A = 30 dB).')
@solve('10.46')
def _():
    R1, R2, Vp, w = 750.0, 9.1e3, 0.05, 4638.0; Av = -R2 / R1; vo, ii = inv_amp(R1, R2, Vp); close(vo, Av * Vp, 1e-9); close(-ii, Vp / R1, 1e-9)
    return [('Voltage gain Av = −R2/R1', g(Av, 4)), ('Output voltage', f'vo(t) = {g(Av * Vp, 4)} sin(4638t) V'), ('Input current', f'ii(t) = vi/R1 = {g(Vp / R1 * 1e6, 4)} sin(4638t) μA')], 'Ideal inverting amplifier: v− = 0, so ii = vi/R1 and vo = −R2·ii.', [], cir('10.46', 'Fig. P10.44', INV + '.')
@solve('10.47')
def _():
    R1, R2 = 22e3, 220e3; A = -R2 / R1; out = []
    def case(vdc, vac): return A * vdc, A * vac, vdc / R1, vac / R1
    for vdc, vac in ((0, 0), (0.22, 0), (0, 0.15), (0.22, -0.15)):
        vo, _ = inv_amp(R1, R2, vdc + vac); close(vo, A * (vdc + vac), 1e-9)
    return [('(a) vI = 0', 'vO = 0'), ('(b) VI = 0.22 V', f'VO = {g(A * 0.22, 4)} V'), ('(c) vI = 0.15 sin 2500πt V', f'vO = {g(A * 0.15, 4)} sin 2500πt V'), ('(d) vI = 0.22 − 0.15 sin 2500πt V', f'vO = {g(A * 0.22, 4)} + {g(-A * 0.15, 4)} sin 2500πt V'),
            ('(e) input current iI', f'(b) {g(0.22 / R1 * 1e6, 3)} μA; (c) {g(0.15 / R1 * 1e6, 3)} sin 2500πt μA; (d) {g(0.22 / R1 * 1e6, 3)} − {g(0.15 / R1 * 1e6, 3)} sin 2500πt μA'), ('(f) op-amp output current iO = vO/R2 (into R2)', f'(b) {g(A * 0.22 / R2 * 1e6, 3)} μA; (c) {g(A * 0.15 / R2 * 1e6, 3)} sin 2500πt μA; (d) {g(A * 0.22 / R2 * 1e6, 3)} + {g(-A * 0.15 / R2 * 1e6, 3)} sin 2500πt μA'), ('(g) v− for part (d)', '0 V (virtual ground)')], \
        'Ideal inverting amplifier with gain −R2/R1 = −10: vO = −10·vI, iI = vI/R1, iO = vO/R2 (the only load of the output is R2), v− = v+ = 0.', ['No power-supply limits are given, so no clipping is applied.', 'iO is the current leaving the op-amp output towards R2 (arrow direction of the figure); iO = iI by KCL at the summing node.'], cir('10.47', 'Fig. P10.44', INV + '.')
@solve('10.48')
def _():
    R1, R2, V = 7.5e3, 150e3, 12.0; A = -R2 / R1; ok = lambda x: abs(x) <= V
    for vdc in (-0.2, 0.6):
        vo, _ = inv_amp(R1, R2, vdc); close(vo, A * vdc, 1e-9)
    Vi_a = min((V - 4.0) / 20, (V + 4.0) / 20)                                                        # vO = 4 − 20·Vi·sin: peaks 4 ± 20Vi must stay inside ±12 V
    return [('(a) vO(t)', f'vO = {g(A * -0.2, 3)} − {g(-A * 1, 3)}·Vi sin 2000πt V  (= 4 − 20·Vi sin 2000πt V)'), ('(b) largest Vi without clipping', f'{g(Vi_a, 3)} V (the positive peak 4 + 20·Vi reaches +12 V)'), ('(c) vI = 0.6 + Vi sin 2000πt', 'vO = −12 − 20·Vi sin 2000πt V: the dc output is already at the −12 V limit, so any Vi > 0 clips the negative peaks: largest undistorted Vi = 0')], \
        'Gain −R2/R1 = −20; the output may swing only between the supplies (±12 V).', ['The output is assumed to reach the supply voltages exactly.'], cir('10.48', 'Fig. P10.44', INV + '.')
@solve('10.49')
def _():
    R1, R2, Rs = 8.2e3, 160e3, 1.5e3; A1 = -R2 / R1; A2 = -R2 / (R1 + Rs); vo, _ = inv_amp(R1, R2, 1.0, Rs); close(vo, A2, 1e-9)
    return [('(a) Av = vo/vi', f'{g(A1, 4)} ({g(dbv(A1), 4)} dB)'), ('(b) with a 1.5 kΩ source resistance in series with the source', f'Av = −R2/(R1 + Rs) = {g(A2, 4)} ({g(dbv(A2), 4)} dB), i.e. {g(100 * (A2 / A1 - 1), 3)} % smaller')], 'The source resistance adds to R1 because the − input is a virtual ground: the input resistance of the stage is R1, so Av = −R2/(R1 + Rs).', ['Av = vo/vi with vi the open-circuit source voltage.'], cir('10.49', 'Fig. P10.44', INV + '.')
@solve('10.50')
def _():
    R1, R2, V = 10e3, 100e3, 10.0; A = -R2 / R1
    return [('(a) vI = 0.5 + Vi sin 5000πt V', f'vO = {g(A * 0.5, 3)} − 10·Vi sin 5000πt V'), ('(b) largest Vi without clipping', f'{g(min(V - 5.0, V + 5.0) / 10, 3)} V (vO swings −5 V ∓ 10·Vi: the negative peak −5 − 10·Vi reaches −10 V)'), ('(c) vI = −0.25 + Vi sin 2000πt V', f'vO = {g(A * -0.25, 3)} − 10·Vi sin 2000πt V; largest Vi = {g(min(V - 2.5, V + 2.5) / 10, 3)} V (the positive peak 2.5 + 10·Vi reaches +10 V)')], 'Gain −R2/R1 = −10, outputs limited to ±10 V.', [], cir('10.50', 'Fig. P10.44', INV + '.')
NONINV = 'noninverting amplifier: vi drives the + input, R2 from the output to the − input and R1 from the − input to ground; the input current ii and the output current io are marked'
@solve('10.60')
def _():
    R1, R2 = 8.2e3, 750e3; A = 1 + R2 / R1; vo, vm, _ = noninv(R1, R2, 1.0); close(vo, A, 1e-9)
    return [('Voltage gain Av = 1 + R2/R1', f'{g(A, 4)} = {g(dbv(A), 4)} dB'), ('Input resistance', '∞ (ideal op amp: ii = 0)'), ('Output resistance', '0 (ideal op amp)')], 'Ideal noninverting amplifier (Jaeger Eq. 10.53 and the examples of §10.9).', [], cir('10.60', 'Fig. P10.60', NONINV + '.')
@solve('10.61')
def _():
    R1, R2 = 910.0, 8.2e3; A = 1 + R2 / R1; vo, _, _ = noninv(R1, R2, 0.04); close(vo, A * 0.04, 1e-9)
    return [('vo(t) = (1 + R2/R1)·vi', f'vo(t) = {g(A * 0.04, 4)} sin 9125t V (gain {g(A, 4)})')], 'Ideal noninverting amplifier.', [], cir('10.61', 'Fig. P10.60', NONINV + '.')
@solve('10.62')
def _():
    rows = []
    for tag, R1, R2 in (('(a)', 30e3, 120e3), ('(b)', 18e3, 300e3), ('(c)', 3.3e3, 390e3)):
        A = 1 + R2 / R1; vo, _, _ = noninv(R1, R2, 1.0); close(vo, A, 1e-9); rows.append((f'{tag} R1 = {si(R1, "Ω", 3)}, R2 = {si(R2, "Ω", 3)}', f'Av = {g(A, 4)} ({g(dbv(A), 4)} dB); Rin = ∞; Rout = 0'))
    return rows, 'Av = 1 + R2/R1, infinite input resistance and zero output resistance for the ideal op amp.', [], cir('10.62', 'Fig. P10.60', NONINV + '.')
@solve('10.63')
def _():
    R1, R2 = 22e3, 360e3; A = 1 + R2 / R1
    for vdc in (0.0, 0.33, 0.18, 0.33 - 0.18): vo, vm, _ = noninv(R1, R2, vdc); close(vo, A * vdc, 1e-9); close(vm, vdc, 1e-9)
    io = lambda v: v / (R1 + R2)
    return [('(a) vI = 0', 'vO = 0'), ('(b) VI = 0.33 V', f'VO = {g(A * 0.33, 4)} V'), ('(c) vi = 0.18 sin 3250πt V', f'vO = {g(A * 0.18, 4)} sin 3250πt V'), ('(d) vI = 0.33 − 0.18 sin 3250πt V', f'vO = {g(A * 0.33, 4)} − {g(A * 0.18, 4)} sin 3250πt V'),
            ('(e) input current iI', '0 for all three (ideal op amp, infinite input resistance)'), ('(f) op-amp output current iO = vO/(R1 + R2)', f'(b) {g(io(A * 0.33) * 1e6, 4)} μA; (c) {g(io(A * 0.18) * 1e6, 4)} sin 3250πt μA; (d) {g(io(A * 0.33) * 1e6, 4)} − {g(io(A * 0.18) * 1e6, 4)} sin 3250πt μA'), ('(g) v− for part (d)', 'v− = v+ = vI = 0.33 − 0.18 sin 3250πt V')], \
        'Ideal noninverting amplifier: vO = (1 + R2/R1)·vI = 17.36·vI; the only load of the output is R2 + R1 to ground.', ['No supply limits are given, so no clipping is applied.'], cir('10.63', 'Fig. P10.60', NONINV + '.')
@solve('10.69')
def _():
    R1, R2, R3 = 1e3, 2e3, 47e3; a1, a2 = 0.04, 0.01
    c = Ckt(); c.V('v1', 'a', '0', a1); c.V('v2', 'b', '0', a2); c.R('a', 'm', R1); c.R('b', 'm', R2); c.opamp('0', 'm', 'o'); c.R('m', 'o', R3); v, _ = dc(c); close(v['o'], -(R3 / R1 * a1 + R3 / R2 * a2), 1e-9); close(v['m'], 0, 1e-9, 1e-9)
    return [('Output voltage', f'vo(t) = −R3·(v1/R1 + v2/R2) = −{g(R3 / R1 * a1, 4)} sin 10000t − {g(R3 / R2 * a2, 4)} sin 3770t V'), ('Voltage at the summing junction', 'v− = 0 (virtual ground)')], 'Ideal summing amplifier: v− = 0, the currents v1/R1 and v2/R2 add and flow through R3.', [], cir('10.69', 'Fig. P10.69', 'inverting summing amplifier: v1 through R1 and v2 through R2 to the − input v−, R3 from the output to the − input, + input grounded.')
@solve('10.70')
def _():
    wts = [1 / 2, 1 / 4, 1 / 8, 1 / 16]; bits = lambda s: [int(x) for x in s]; vI = 2.0
    def gain(code):
        b = bits(code); c = Ckt(); c.V('vi', 'in', '0', 1.0); c.opamp('0', 'm', 'o'); c.R('m', 'o', 1.0)
        for k, bk in enumerate(b): c.R('in' if bk else '0', 'm', 2.0 ** (k + 1))
        v, _ = dc(c); return v['o']
    for code in ('0110', '1011', '0000', '1111'): close(gain(code), -sum(w * x for w, x in zip(wts, bits(code))), 1e-9, 1e-12)
    tab = ', '.join(f'{n:04b}: {-n / 16 * vI:+.4g}' for n in range(16))
    return [('(a) 0110, vI = 2 sin 4000πt V', f'vO = −(1/4 + 1/8)·vI = {g(-0.375 * vI, 4)} sin 4000πt V'), ('(b) 1011', f'vO = −(1/2 + 1/8 + 1/16)·vI = {g(-0.6875 * vI, 4)} sin 4000πt V'), ('(c) all 16 codes: vO amplitude (V) = −(n/16)·2 V, n = 8b1 + 4b2 + 2b3 + b4', tab)], \
        'Each switch connects its resistor to vI (bi = 1) or to 0 V (bi = 0); the summing amplifier with feedback resistor R gives vO = −(b1·R/2R + b2·R/4R + b3·R/8R + b4·R/16R)·vI = −(n/16)·vI.', ['b1 is the bit of the 2R resistor (the most significant) and b4 the bit of the 16R resistor, as drawn.'], cir('10.70', 'Fig. P10.70', 'summing amplifier with feedback resistor R and four input resistors 2R, 4R, 8R, 16R, each switched by a bit b1…b4 either to 0 V (bi = 0) or to the input vI (bi = 1).')
@solve('10.72')
def _():
    R = 10e3
    def diff(v1, v2, k=10):
        c = Ckt(); c.V('v1', 'a', '0', v1); c.V('v2', 'b', '0', v2); c.R('a', 'm', R); c.R('m', 'o', k * R); c.R('b', 'p', R); c.R('p', '0', k * R); c.opamp('p', 'm', 'o'); v, i = dc(c); return v['o'], i['v1'], i['v2']
    vo, _, _ = diff(1.0, 0.0); close(vo, -10, 1e-9); vo2, _, i2 = diff(0.0, 1.0); close(vo2, 10, 1e-9); close(1 / abs(i2), 11 * R, 1e-9)
    a = diff(3.0, 0.0)[0]
    return [('(a) gain Av = vo/(v1 − v2)', '−10'), ('(b) input resistance presented to v2', f'R + 10R = 11R = {si(11 * R, "Ω", 3)}'), ('(c) input resistance at v1', f'R = {si(R, "Ω", 3)} (for v2 = 0; in general i1 depends on v2 also)'),
            ('(d) v1 = 3 V, v2 = 1.5 cos 8300πt V', f'vO = −10(v1 − v2) = {g(-30, 3)} + 15 cos 8300πt V'), ('(e) v1 = 3 − 1.5 cos 8300πt, v2 = 1.5 sin 8300πt', 'vO = −10(3 − 1.5 cos 8300πt − 1.5 sin 8300πt) = −30 + 15 cos 8300πt + 15 sin 8300πt V = −30 + 21.2 sin(8300πt + 45°) V')], 'Difference amplifier with R1 = R3 = R and R2 = R4 = 10R: vO = −(R2/R1)(v1 − v2) = −10(v1 − v2) (Jaeger Eq. 10.64); Rin2 = R + 10R and Rin1 = R for v2 = 0.', ['Av is defined as vo/(v1 − v2), so it is negative for this connection (v1 on the inverting side).'], cir('10.72', 'Fig. P10.72', 'difference amplifier: v1 through R to the − input and 10R feedback from the output to the − input; v2 through R to the + input with 10R from the + input to ground.')
@solve('10.73')
def _():
    R = 100e3; V1, V2 = 3.1, 3.2
    c = Ckt(); c.V('v1', 'a', '0', V1); c.V('v2', 'b', '0', V2); c.R('a', 'm', R); c.R('m', 'o', 10 * R); c.R('b', 'p', R); c.R('p', '0', 10 * R); c.opamp('p', 'm', 'o'); v, i = dc(c)
    Vp = V2 * 10 / 11; Vo = -10 * (V1 - V2); close(v['o'], Vo, 1e-9); close(v['p'], Vp, 1e-9); close(v['m'], Vp, 1e-6)
    i1, i2 = (V1 - Vp) / R, V2 / (11 * R); Io = Vo / (10 * R + 0)
    return [('(a) node voltages', f'v1 = {V1} V, v2 = {V2} V, v+ = v− = {g(Vp, 5)} V, vO = {g(Vo, 4)} V'), ('(b) output current IO (into the 10R feedback resistor, leaving the output)', f'IO = (vO − v−)/10R = {si((Vo - Vp) / (10 * R), "A", 4)}'), ('(c) currents entering from v1 and v2', f'i1 = (v1 − v−)/R = {si(i1, "A", 4)}; i2 = v2/11R = {si(i2, "A", 4)}')], \
        'Ideal op amp: v+ = v2·10R/(11R) = v−; vO = −10(V1 − V2); currents from Ohm\'s law.', ['IO is the current delivered by the op-amp output through the feedback resistor (no other load).'], cir('10.73', 'Fig. P10.72', 'difference amplifier with R = 100 kΩ: v1 through R to the − input and 10R feedback, v2 through R to the + input with 10R to ground.')
@solve('10.74')
def _():
    R = 15e3
    def diffc(v1, v2):
        c = Ckt(); c.V('v1', 'a', '0', v1); c.V('v2', 'b', '0', v2); c.R('a', 'm', R); c.R('m', 'o', 10 * R); c.R('b', 'p', R); c.R('p', '0', 10 * R); c.opamp('p', 'm', 'o'); v, i = dc(c); return v['o'], i['v1'], i['v2']
    c1, c2, c3 = 2 / 11 / R, 2 / R, 2 / (11 * R)
    for t in (0.0003, 0.0007, 0.00123):                                                  # v1 = 2 sin a + 2 sin 2a, v2 = 2 sin a with a = 1000πt
        a_ = 1000 * math.pi * t; s1, s2 = 2 * math.sin(a_), 2 * math.sin(2 * a_); o, i1, i2 = diffc(s1 + s2, s1)
        close(o, -10 * s2, 1e-9, 1e-9); close(-i1, c1 * math.sin(a_) + c2 * math.sin(2 * a_), 1e-6, 1e-12); close(-i2, c3 * math.sin(a_) * 1.0 * -1 * -1, 1e-6, 1e-12)
    return [('vO = −10(v1 − v2)', 'vO = −20 sin 2000πt V (the common-mode term 2 sin 1000πt cancels)'), ('i1 = (v1 − v−)/R with v− = (10/11)v2', f'i1 = {g(c1 * 1e6, 4)} sin 1000πt μA + {g(c2 * 1e6, 4)} sin 2000πt μA'), ('i2 = v2/(11R)', f'i2 = {g(c3 * 1e6, 4)} sin 1000πt μA')], \
        'Ideal difference amplifier with R = 15 kΩ and 10R: v1 − v2 = 2 sin 2000πt, so vO = −10(v1 − v2); v+ = v− = (10/11)v2 gives the input currents.', [], cir('10.74', 'Fig. P10.72', 'difference amplifier with R = 15 kΩ: v1 through R to the − input and 10R feedback, v2 through R to the + input with 10R to ground; i1 and i2 are the currents drawn from the sources.')
LP = 'low-pass amplifier: vi through R1 to the − input; the feedback is R2 in parallel with C from the output to the − input; + input grounded'
HP = 'high-pass amplifier: vi through C in series with R1 to the − input; feedback resistor R2 from the output to the − input; + input grounded'
@solve('10.98')
def _():
    out = []
    for tag, R1, R2, C in (('(a)', 2e3, 10e3, 0.001e-6), ('(b)', 3.3e3, 56e3, 100e-12)):
        A0 = R2 / R1; fH = 1 / (2 * math.pi * R2 * C)
        def H(f):
            c = Ckt(); c.V('vi', 'in', '0', 1.0); c.R('in', 'x', R1); c.opamp('0', 'x', 'o'); c.R('x', 'o', R2); c.C('x', 'o', C); v, _ = c.solve(2j * math.pi * f); return v['o']
        close(abs(H(fH)), A0 / math.sqrt(2), 1e-6); close(abs(H(1e-3 * fH)), A0, 1e-5)
        out.append((f'{tag} R1 = {si(R1, "Ω", 3)}, R2 = {si(R2, "Ω", 3)}, C = {si(C, "F", 3)}', f'low-frequency gain −R2/R1 = {g(-A0, 4)} ({g(dbv(A0), 4)} dB); fH = 1/(2πR2C) = {si(fH, "Hz", 4)}'))
    return out, 'Low-pass inverting amplifier (Jaeger Fig. 10.32): Av(s) = −(R2/R1)/(1 + sR2C), so the low-frequency gain is −R2/R1 and the −3 dB frequency fH = 1/(2πR2C).', ['The gain in dB is 20 log|Av|; the minus sign (inversion) is shown separately.'], cir('10.98', 'Fig. 10.32', LP + '.')
@solve('10.104')
def _():
    out = []
    for tag, R1, R2, C in (('(a)', 4.2e3, 20e3, 560e-12), ('(b)', 2.7e3, 56e3, 0.002e-6)):
        A0 = R2 / R1; fL = 1 / (2 * math.pi * R1 * C)
        def H(f):
            c = Ckt(); c.V('vi', 'in', '0', 1.0); c.C('in', 'y', C); c.R('y', 'x', R1); c.opamp('0', 'x', 'o'); c.R('x', 'o', R2); v, _ = c.solve(2j * math.pi * f); return v['o']
        close(abs(H(fL)), A0 / math.sqrt(2), 1e-6); close(abs(H(1e3 * fL)), A0, 1e-5)
        out.append((f'{tag} R1 = {si(R1, "Ω", 3)}, R2 = {si(R2, "Ω", 3)}, C = {si(C, "F", 3)}', f'high-frequency gain −R2/R1 = {g(-A0, 4)} ({g(dbv(A0), 4)} dB); fL = 1/(2πR1C) = {si(fL, "Hz", 4)}'))
    return out, 'High-pass inverting amplifier (Jaeger Fig. 10.33): Av(s) = −(R2/R1)·sR1C/(1 + sR1C): the high-frequency gain is −R2/R1 and the −3 dB frequency fL = 1/(2πR1C).', [], cir('10.104', 'Fig. 10.33', HP + '.')
INTG = 'integrator: vi through R to the − input and the capacitor C from the output to the − input; + input grounded'
@solve('10.107')
def _():
    R, C = 12e3, 0.005e-6; w = 2000 * math.pi; k = 1 / (R * C); amp = 0.1 * k / w
    dt = 1e-8; t = np.arange(0, 2e-3, dt); vo = -np.cumsum(0.1 * np.sin(w * t)) * dt * k; ref = amp * (np.cos(w * t) - 1); close(float(np.max(np.abs(vo - ref))), 0.0, 1, 2e-3 * amp)       # independent: step the integral
    return [('vo(t) = −(1/RC)∫vi dt + vo(0)', f'vo(t) = {g(amp, 4)}·(cos 2000πt − 1) V = {g(-amp, 4)} + {g(amp, 4)} cos 2000πt V'), ('RC', f'{g(R * C * 1e6, 3)} μs; 1/RC = {g(k, 5)} s⁻¹')], 'Ideal integrator (Jaeger Fig. 10.34): vo(t) = vo(0) − (1/RC)∫ vi dτ; with vi = 0.1 sin ωt, ω = 2000π, vo = (0.1/(RCω))(cos ωt − 1).', ['The dc offset −0.265 V comes from vo(0) = 0: the output starts at 0 V and swings below it.'], cir('10.107', 'Fig. 10.34', INTG + '.')
@solve('10.108')
def _():
    R, C = 10e3, 0.1e-6; k = 1 / (R * C); T = 1e-3; res = []
    for v0 in (0.0, -2.5):
        dt = 1e-7; t = np.arange(0, 2.5e-3, dt); vi = np.where(t < T, 5.0, 0.0); vo = v0 - np.cumsum(vi) * dt * k
        close(float(vo[int(T / dt) - 1]), v0 - 5.0 * T * k, 1e-3); close(float(vo[-1]), v0 - 5.0 * T * k, 1e-3); res.append(v0 - 5 * T * k)
    return [('(a) vo(0) = 0', f'for 0 ≤ t ≤ 1 ms: vo(t) = −5 V × (t/1 ms) (a ramp falling {g(5 * k, 4)} V/s = 5 V/ms to {g(res[0], 3)} V at t = 1 ms); for t > 1 ms the input is 0, so vo stays at {g(res[0], 3)} V'), ('(b) vo(0) = −2.5 V', f'the same ramp starting from −2.5 V: vo(t) = −2.5 − 5·(t/1 ms) V down to {g(res[1], 3)} V at t = 1 ms, then constant at {g(res[1], 3)} V')], \
        'RC = 10 kΩ × 0.1 μF = 1 ms, so a 5 V pulse makes the output fall 5 V per millisecond (vo = vo(0) − (1/RC)∫vi dt); after the pulse the input is 0 and the capacitor holds its charge.', ['The op amp is ideal with no supply limit.', 'The waveform asked for is described by its segments and levels.'], cir('10.108', 'Fig. 10.34', INTG + '.')
@solve('10.111')
def _():
    R, C = 120e3, 0.02e-6; w = 3000 * math.pi; RC = R * C; amp = 3 * w * RC
    t = np.linspace(0, 2e-3, 200001); num = -RC * np.gradient(3 * np.cos(w * t), t); ref = amp * np.sin(w * t); close(float(np.max(np.abs(num[2:-2] - ref[2:-2]))), 0.0, 1, 1e-3 * amp)         # independent: differentiate numerically
    c = Ckt(); c.V('vi', 'in', '0', 1.0); c.C('in', 'x', C); c.opamp('0', 'x', 'o'); c.R('x', 'o', R); v, _ = c.solve(1j * w); close(abs(v['o']), w * RC, 1e-6)
    return [('vo(t) = −RC·dvi/dt', f'vo(t) = {g(amp, 4)} sin 3000πt V  (RC = {g(RC * 1e3, 3)} ms, ωRC = {g(w * RC, 4)})')], 'Ideal differentiator (Jaeger Fig. 10.33/10.35): vo = −RC·dvi/dt; for vi = 3 cos ωt, vo = 3ωRC sin ωt.', ['The result (67.9 V amplitude) shows that the ideal differentiator would need far larger supplies than a real op amp has: the high-pass of the practical circuit limits it.'], cir('10.111', 'Fig. 10.33', 'differentiator: vi through C to the − input, feedback resistor R from the output to the − input; + input grounded (R and C are the values of the statement).')
@solve('10.114')
def _():
    VEE, R, VTN, Kn = 10.0, 20.0, 2.5, 0.25; IO = VEE / R; VGS = VTN + math.sqrt(2 * IO / Kn); VDmin = VGS - VTN + 0.0; PR = IO ** 2 * R; PFET = IO * VDmin
    c = Ckt(); c.opamp('0', 'x', 'g'); c.V('vee', 'e', '0', -VEE); c.R('x', 'e', R); v, i = dc(c); close((0 - (-VEE)) / R, IO, 1e-9)                    # the op amp holds the source node at 0 V
    return [('(a) output current IO = VEE/R (the source node is held at 0 V)', f'IO = {g(IO, 4)} A'), ('(b) VGS and minimum VDD', f'VGS = VTN + √(2·ID/Kn) = {g(VGS, 4)} V; saturation needs VDS ≥ VGS − VTN = {g(VDmin, 4)} V, so VDD(min) = {g(VDmin, 4)} V (source at 0 V)'), ('(c) power ratings', f'resistor: IO²R = {g(PR, 4)} W; FET at VDD(min): ID·VDS = {g(PFET, 3)} W (it grows as 0.5 A × VDD for a higher supply)')], \
        'The op amp (+ input grounded) forces the MOSFET source node to 0 V (virtual ground), so IO = ID = VEE/R, independent of the transistor; with ID = (Kn/2)(VGS − VTN)² the gate voltage follows.', ['The drain is assumed connected directly to VDD; Kn follows ID = (Kn/2)(VGS − VTN)² (Jaeger).'], cir('10.114', 'Fig. P10.114', 'an op amp with + input grounded and its output driving the gate of an NMOS transistor whose drain goes to VDD and whose source is fed back to the − input and connected through R to −VEE; the output current IO is the drain current.')
@solve('10.115')
def _():
    VEE, R, bF, IS, VT = 15.0, 15.0, 30.0, 1e-13, 0.025; IE = VEE / R; IC = bF / (bF + 1) * IE; IB = IE / (bF + 1); VBE = VT * math.log(IC / IS); PR = IE ** 2 * R; VCC = 15.0; PQ = IC * VCC + IB * VBE
    from scipy.optimize import brentq
    vbe2 = brentq(lambda v: IS * (math.exp(v / VT) - 1) - IC, 0.3, 1.0); close(vbe2, VBE, 5e-3)                                                    # solve the exponential characteristic numerically
    return [('(a) IO = IC = βF/(βF + 1)·VEE/R', f'IE = {g(IE, 4)} A, IO = {g(IC, 4)} A (IB = {si(IB, "A", 3)})'), ('(b) op-amp output voltage = VBE (emitter at 0 V)', f'VBE = VT·ln(IC/IS) = {g(VBE, 4)} V (VT = 25 mV)'), ('(c) minimum VCC for the forward-active region', f'VCB ≥ 0: VC ≥ VB = {g(VBE, 3)} V, so VCC(min) ≈ {g(VBE, 3)} V'), ('(d) power ratings', f'resistor: IE²R = {g(PR, 4)} W; transistor at VCC = 15 V: IC·VCE + IB·VBE = {g(PQ, 4)} W')], \
        'The op amp holds the emitter at 0 V, so IE = VEE/R = 1 A and IC = βF/(βF + 1)·IE; the base is VBE above the emitter.', ['VT = 25 mV and the collector is tied directly to VCC; VCE = VCC because the emitter is at 0 V.'], cir('10.115', 'Fig. P10.115', 'an op amp with + input grounded and its output driving the base of an npn transistor whose collector goes to VCC and whose emitter is fed back to the − input and connected through R to −VEE; the output current IO is the collector current.')
@solve('10.117')
def _():
    R1, R2, C = 10e3, 330e3, 100e-12; tR, tCp, tCm = 0.10, 0.20, 0.50
    gain = lambda r1, r2: r2 / r1; fH = lambda r2, c: 1 / (2 * math.pi * r2 * c)
    nom = (gain(R1, R2), fH(R2, C)); gmax = gain(R1 * (1 - tR), R2 * (1 + tR)); gmin = gain(R1 * (1 + tR), R2 * (1 - tR)); fmax = fH(R2 * (1 - tR), C * (1 - tCm)); fmin = fH(R2 * (1 + tR), C * (1 + tCp))
    corners = [(gain(r1, r2), fH(r2, c)) for r1 in (R1 * 0.9, R1 * 1.1) for r2 in (R2 * 0.9, R2 * 1.1) for c in (C * 0.5, C * 1.2)]; close(max(x[0] for x in corners), gmax, 1e-12); close(min(x[1] for x in corners), fmin, 1e-12); close(max(x[1] for x in corners), fmax, 1e-12)
    return [('nominal low-frequency gain and cutoff', f'|Av0| = R2/R1 = {g(nom[0], 4)} ({g(dbv(nom[0]), 4)} dB); fH = {si(nom[1], "Hz", 4)}'), ('worst-case gain', f'{g(gmin, 4)} to {g(gmax, 4)} ({g(dbv(gmin), 4)} to {g(dbv(gmax), 4)} dB)'), ('worst-case cutoff frequency', f'{si(fmin, "Hz", 4)} to {si(fmax, "Hz", 4)}')], \
        'Gain −R2/R1 and fH = 1/(2πR2C); the extremes occur at the corners of the tolerance box: gain largest for R2 high and R1 low, fH largest for R2 and C both low (R2·C smallest).', ['All 8 tolerance corners were evaluated: the extremes above are the largest and smallest values.'], cir('10.117', 'Fig. P10.117', LP + '.')
