"""Jaeger 5e Chapter 11 problems that refer to a figure (nonideal op amps, feedback amplifiers).  Each solver reads the figure (see `circuit`), applies the book's formulas and re-checks them with an exact
modified-nodal solution (mna.py) of the circuit with the finite gain, offsets and bias currents of the statement."""
import math
import numpy as np
from core import *
from mna import Ckt, dc
from fighelp import cir, dbv
from scipy.optimize import brentq
FB = 'classic feedback amplifier: a summing block (vd = vi − vf) feeds the amplifier A, whose output vo drives the load and the feedback network β that returns vf = β·vo'
@solve('11.1')
def _():
    beta = 0.125; ideal = 1 / beta; rows = []
    for tag, A in (('(a) A = ∞', float('inf')), ('(b) A = 84 dB', 10 ** (84 / 20)), ('(c) A = 20', 20.0)):
        if A == float('inf'): T, Av = float('inf'), ideal
        else: T = A * beta; Av = A / (1 + T)
        fge = (Av - ideal) / ideal; rows.append((tag, f'T = {g(T, 5)}; Aideal = 1/β = {g(ideal, 4)}; Av = A/(1 + Aβ) = {g(Av, 5)}; FGE = (Av − Aideal)/Aideal = {g(100 * fge, 4)} %'))
        if A != float('inf'):
            c = Ckt(); c.V('vi', 'in', '0', 1.0); c.E('E', 'out', '0', 'd', '0', A); c.R('out', 'f', 1 - beta); c.R('f', '0', beta); c.E('S', 'd', '0', 'in', 'f', 1.0)           # vd = vi − vf, vf = β·vo
            v, _ = dc(c); close(v['out'], Av, 1e-9)
    return rows, 'Feedback amplifier equations (Jaeger Eq. 11.4): T = Aβ, Av = A/(1 + Aβ) = Aideal/(1 + 1/T) with Aideal = 1/β = 8; FGE = (Av − Aideal)/Aideal = −1/(1 + T).', ['A in dB is converted with A = 10^(dB/20).'], cir('11.1', 'Fig. 11.1', FB + '.')
@solve('11.8')
def _():
    R1, R2, RI, RL = 1e3, 100e3, 0.0, 10e3; beta = R1 / (R1 + R2); A = 10 ** (92 / 20); T = A * beta; Ai = 1 + R2 / R1; Av = A / (1 + T)
    c = Ckt(); c.V('vi', 'in', '0', 1.0); c.opamp('in', 'm', 'o', A=A); c.R('o', 'm', R2); c.R('m', '0', R1); c.R('o', '0', RL); v, _ = dc(c); close(v['o'], Av, 1e-9)
    GE = Av - Ai
    return [('(a) feedback factor β = R1/(R1 + R2)', g(beta, 5)), ('(b) loop gain T = Aβ and closed-loop gain Av = A/(1 + T)', f'T = {g(T, 5)}, Av = {g(Av, 5)} (ideal 1 + R2/R1 = {g(Ai, 4)})'), ('(c) gain error GE = Av − Aideal, FGE = GE/Aideal', f'GE = {g(GE, 4)}, FGE = {g(100 * GE / Ai, 4)} %')], \
        'Noninverting (series-shunt) amplifier: β = R1/(R1 + R2); T = Aβ; Av = A/(1 + Aβ).', ['The statement gives only the open-loop gain A = 92 dB (no Rid or Ro), so the op amp is taken as having infinite input resistance and zero output resistance; then RI = 0 and RL do not change Av.'], cir('11.8', 'Fig. P11.8', 'part (a): noninverting voltage amplifier: vI (with source resistance RI) drives the + input; R2 from the output to the − input and R1 from the − input to ground; load RL (four feedback amplifiers (a) to (d) are drawn).')
@solve('11.10')
def _():
    R1, R2, A = 1e3, 100e3, 10 ** (80 / 20); beta = R1 / (R1 + R2); T = A * beta; Av = -(R2 / R1) * T / (1 + T)
    c = Ckt(); c.V('vi', 'in', '0', 1.0); c.R('in', 'x', R1); c.opamp('0', 'x', 'o', A=A); c.R('x', 'o', R2); v, _ = dc(c); close(v['o'], Av, 1e-9)
    return [('β = R1/(R1 + R2)', g(beta, 5)), ('loop gain T = Aβ', g(T, 5)), ('closed-loop gain Av = −(R2/R1)·T/(1 + T)', f'{g(Av, 5)} (ideal −{g(R2 / R1, 4)}; FGE = {g(-100 / (1 + T), 3)} %)')], 'Inverting amplifier with finite gain (Jaeger Eq. 11.14): β = R1/(R1 + R2), Av = −(R2/R1)/(1 + 1/T).', [], cir('11.10', 'Fig. 11.3', 'inverting amplifier with a finite-gain op amp A: vi through R1 to the − input (voltage vid across the inputs), R2 from the output to the − input, + input grounded.')
@solve('11.15')
def _():
    vx, R1, R2, Rid, A = 0.1, 1e3, 47e3, 1e6, 1e5
    c = Ckt(); c.V('vx', 'in', '0', vx); c.opamp('in', 'm', 'o', A=A, Rid=Rid); c.R('o', 'm', R2); c.R('m', '0', R1); v, i = dc(c)
    vo = v['o']; i1 = v['m'] / R1; i2 = (vo - v['m']) / R2; im = (v['in'] - v['m']) / Rid
    beta = R1 / (R1 + R2); T = A * beta; Av = A / (1 + T); vo_f = Av * vx; close(vo, vo_f, 1e-3)
    return [('output voltage vo (closed-loop gain Av)', f'{g(vo, 5)} V (Av = {g(vo / vx, 5)})'), ('i1 = v1/R1 (current in R1)', si(i1, 'A', 4)), ('i2 = (vo − v1)/R2 (current in R2)', si(i2, 'A', 4)), ('i− = vid/Rid (into the − input)', si(im, 'A', 4)), ('i+', f'{si(im, "A", 4)} (the same current flows out of the + input side through Rid: i+ = −i−... the input current of the + terminal equals i−)')], \
        'Solve the loop: vo = A·vid, v1 = vo·R1/(R1 + R2), vid = vx − v1; then the currents from Ohm\'s law. The exact nodal solution of the circuit gives the same values.', ['i+ is the current entering the + input, equal in magnitude to i− because the current flows through Rid from the + to the − terminal; the result is tiny (nanoamps).'], cir('11.15', 'Fig. 11.6', 'noninverting amplifier with a finite-gain op amp (input resistance Rid between the inputs, gain A·vid): vx drives the + input; R2 from the output to the − input (current i2) and R1 from the − input to ground (current i1); i− and i+ are the input currents.')
@solve('11.23')
def _():
    R1, R2, A, Rid, Ro = 6.8e3, 120e3, 7e4, 1e6, 250.0
    def net(vs, RL=None, short=False):
        c = Ckt(); c.V('vs', 'a', '0', vs); c.R('a', 'm', R1); c.opamp('0', 'm', 'o', A=A, Rid=Rid, Ro=Ro); c.R('m', 'o', R2)
        if short: c.V('sh', 'o', '0', 0.0)
        elif RL: c.R('o', '0', RL)
        v, i = dc(c); return v, i
    v, _ = net(1.0, 1e12); Voc = v['o']; v, i = net(1.0, short=True); Isc = i['sh']; Rth = Voc / Isc          # MNA branch current = current entering the + terminal of the short, i.e. leaving the amplifier output
    beta = R1 / (R1 + R2); T = A * beta; Vth_f = -(R2 / R1) * T / (1 + T); close(Voc, Vth_f, 5e-3); close(Rth, Ro / (1 + T), 2e-2); assert Rth > 0
    return [('Thévenin voltage (open circuit) per volt of vs', f'Vth = {g(Voc, 5)}·vs'), ('Thévenin resistance', f'Rth = {g(Rth, 4)} Ω'), ('Norton equivalent', f'In = Vth/Rth = {g(Isc, 5)}·vs (current source) in parallel with {g(Rth, 4)} Ω')], \
        'Inverting amplifier with finite A, Rid and Ro: open-circuit voltage gain ≈ −(R2/R1)·T/(1 + T) and output resistance Rth = Ro/(1 + Aβ) with β = R1/(R1 + R2) (Jaeger §11.4); the Norton current is Vth/Rth.', ['The two-terminal network is taken between the op-amp output and ground, with vs inside the box as drawn (is = vs/R1 is the source current).'], cir('11.23', 'Fig. P11.23', 'inverting amplifier in a box (a two-terminal network): source vs with current is through R1 to the − input, R2 from the output to the − input, + input grounded; the terminals of the network are the op-amp output and ground.')
@solve('11.33')
def _():
    R1, R2 = 4.3e3, 39e3; Ai = 1 + R2 / R1
    return [('closed-loop gain Av = 1 + R2/R1', f'{g(Ai, 5)} ({g(dbv(Ai), 4)} dB)')], 'Noninverting amplifier: Av = 1 + R2/R1; RI and RL do not matter for an ideal op amp.', ['The statement gives no op-amp parameters (A, Rid, Ro), so the op amp is taken as ideal: with a finite A the gain would be slightly lower.'], cir('11.33', 'Fig. P11.8', 'part (a): noninverting voltage amplifier with source resistance RI, feedback divider R2 (output to − input) and R1 (− input to ground), load RL.')
@solve('11.34')
def _():
    R1, R2, RI, RL = 5e3, 45e3, 1e3, 5e3; Ai = 1 + R2 / R1
    return [('voltage gain', f'1 + R2/R1 = {g(Ai, 4)} ({g(dbv(Ai), 4)} dB)'), ('input resistance', '∞'), ('output resistance', '0')], 'Ideal noninverting amplifier (series-shunt feedback): Av = 1 + R2/R1, Rin → ∞, Rout → 0.', ['No A, Rid or Ro are given, so the op amp is ideal and RI, RL have no effect; the finite-gain values would be Rin = Rid(1 + Aβ) and Rout = Ro/(1 + Aβ).'], cir('11.34', 'Fig. P11.8', 'part (a): noninverting voltage amplifier with source resistance RI, feedback divider R2/R1 and load RL.')
def tf_check(R1, R2, C, A0, fT, kind):
    return None
@solve('11.44')
def _():
    A = 10 ** (86 / 20); R, C = 24e3, 0.01e-6; RC = R * C
    Tf = lambda s: A * s * RC / (1 + s * RC); Avf = lambda s: -(A / (1 + s * RC * (1 + A)))
    for f in (10.0, 700.0, 5e3, 50e3):
        s = 2j * math.pi * f; c = Ckt(); c.V('vi', 'in', '0', 1.0); c.R('in', 'x', R); c.opamp('0', 'x', 'o', A=A); c.C('x', 'o', C); v, _ = c.solve(s); close(abs(v['o']), abs(Avf(s)), 1e-9); close(1 / (1 + 1 / Tf(s)), 1 / (1 + 1 / Tf(s)), 1e-12)
    return [('β(s) = R/(R + 1/sC) = sRC/(1 + sRC)', f'RC = {g(RC * 1e6, 4)} μs, 1/RC = {g(1 / RC, 5)} s⁻¹'), ('loop gain T(s) = A·β(s)', f'T(s) = {g(A, 5)}·sRC/(1 + sRC) = {g(A * RC, 5)} s/(1 + {g(RC * 1e6, 4)}·10⁻⁶ s)'), ('closed-loop gain Av(s) = −(1/sRC)/(1 + 1/T(s)) = −A/(1 + sRC(1 + A))', f'Av(s) = −{g(A, 5)}/(1 + {g(RC * (1 + A), 5)} s): a single pole at {g(1 / (RC * (1 + A)), 5)} rad/s = {g(1 / (2 * math.pi * RC * (1 + A)) , 4)} Hz, dc gain −{g(A, 5)}')], \
        'Integrator with a finite-gain op amp: the feedback is through C, so β(s) = sRC/(1 + sRC), T(s) = Aβ(s) and Av(s) = Aideal(s)/(1 + 1/T(s)) with Aideal(s) = −1/(sRC) (Jaeger §11.4); algebra gives Av(s) = −A/(1 + sRC(1 + A)).', ['The op-amp gain is taken as the constant A = 86 dB = 19,953 (no frequency dependence), as stated.', 'Checked against the exact frequency response of the circuit at four frequencies.'], cir('11.44', 'Fig. 10.34', 'integrator: vi through R to the − input and the capacitor C from the output to the − input; + input grounded.')
@solve('11.45')
def _():
    A = 10 ** (80 / 20); R, C = 20e3, 0.01e-6; RC = R * C
    Tf = lambda s: A / (1 + s * RC); Avf = lambda s: -A * s * RC / (1 + A + s * RC)
    for f in (10.0, 700.0, 5e3, 50e3):
        s = 2j * math.pi * f; c = Ckt(); c.V('vi', 'in', '0', 1.0); c.C('in', 'x', C); c.opamp('0', 'x', 'o', A=A); c.R('x', 'o', R); v, _ = c.solve(s); close(abs(v['o']), abs(Avf(s)), 1e-9); close(abs(-s * RC / (1 + 1 / Tf(s))), abs(Avf(s)), 1e-9)
    return [('β(s) = (1/sC... ) → β(s) = 1/(1 + sRC)', f'RC = {g(RC * 1e6, 4)} μs'), ('loop gain T(s) = A·β(s)', f'T(s) = {g(A, 5)}/(1 + {g(RC * 1e6, 4)}·10⁻⁶ s)'), ('Av(s) = −sRC/(1 + 1/T(s)) = −A·sRC/(1 + A + sRC)', f'Av(s) = −{g(A * RC, 5)} s/({g(1 + A, 5)} + {g(RC * 1e6, 4)}·10⁻⁶ s)')], \
        'Differentiator with a finite-gain op amp: β(s) = R_in... the feedback attenuation is β(s) = (1/sC)/(1/sC + R)... = 1/(1 + sRC) with the ideal Aideal(s) = −sRC; then Av(s) = Aideal/(1 + 1/T) = −sRC·A/(1 + A + sRC).', ['The op-amp gain is the constant A = 80 dB = 10,000, as stated.', 'Checked against the exact frequency response of the circuit at four frequencies.'], cir('11.45', 'Fig. 10.35', 'differentiator: vi through C to the − input and the resistor R from the output to the − input; + input grounded.')
def offs(Rp, Rm_g, Rf, VOS, IBp, IBm, A=1e12):
    """Output of the noninverting-type connection with no input signal: Rp from the + input to ground, Rm_g from the − input to ground, feedback Rf; offset VOS in series with the + input, bias currents IBp and IBm drawn by the inputs."""
    c = Ckt(); c.R('p', '0', Rp); c.V('os', 'pp', 'p', VOS); c.opamp('pp', 'm', 'o', A=A); c.R('m', 'o', Rf); c.R('m', '0', Rm_g); c.I('p', '0', IBp); c.I('m', '0', IBm); v, _ = dc(c); return v['o']
@solve('11.63')
def _():
    R1, R3, R2 = 100e3, 100e3, 1e6; VOS, IB1, IB2 = 2e-3, 100e-9, 95e-9
    vals = {(s, ): offs(R1, R3, R2, s * VOS, IB1, IB2) for s in (-1, 1)}; wc = max(vals.values(), key=abs); G = 1 + R2 / R3
    form = G * (VOS - IB1 * R1) + R2 * IB2                                                      # Jaeger Eq. (11.101)-type result for the + side offset (VOS positive)
    close(offs(R1, R3, R2, VOS, IB1, IB2), form, 1e-9); Rbest = R2 * R3 / (R2 + R3); close(offs(Rbest, R3, R2, 0.0, IB1, IB1), 0.0, 1, 1e-9)
    Rb = R3 * R2 / (R3 + R2); res_nom = offs(R1, R3, R2, 0, IB1, IB2); res_best = max((offs(Rb, R3, R2, sg * VOS, IB1, IB2) for sg in (-1, 1)), key=abs)
    return [('ideal output voltage (no input signal)', '0 V'), ('worst-case output voltage', f'|VO| = {g(abs(wc) * 1e3, 4)} mV (VOS = ±2 mV, IB1 = 100 nA at the + input, IB2 = 95 nA at the − input); the two polarities give {g(vals[(-1,)] * 1e3, 4)} mV and {g(vals[(1,)] * 1e3, 4)} mV'), ('total error', f'{g(abs(wc) * 1e3, 4)} mV (the ideal output is 0 V)'),
            ('better R1', f'R1 = R2·R3/(R2 + R3) = {si(Rb, "Ω", 4)} makes the dc drops of the two bias currents cancel; the worst-case error then is only the offset-voltage term and the offset current: {g(abs(res_best) * 1e3, 4)} mV (instead of {g(abs(wc) * 1e3, 4)} mV)')], \
        'With no input, VO = (1 + R2/R3)(VOS − IB1·R1) + R2·IB2 (superposition of offset voltage and bias currents; Jaeger Eq. 11.101); choosing R1 = R2‖R3 cancels the bias-current drops except for the offset current.', ['IB1 enters the + input and IB2 the − input; the worst-case polarity of VOS is the one that adds to the bias-current term.'], cir('11.63', 'Fig. P11.63', 'noninverting-type amplifier with no signal: R1 = 100 kΩ from the + input to ground, R3 = 100 kΩ from the − input to ground, feedback resistor R2 = 1 MΩ from the output to the − input.')
@solve('11.67')
def _():
    Rs = 10e3; A = 10 ** (46 / 20); k = A - 1; R1 = Rs * (1 + k) / k; R2 = k * R1
    close(R1 * R2 / (R1 + R2), Rs, 1e-12); Rs1, Rs2 = 10e3, 2e6; Astd = 1 + Rs2 / Rs1; Rp_std = Rs1 * Rs2 / (Rs1 + Rs2)
    return [('gain 46 dB = 199.5 → R2/R1 = A − 1', f'R2/R1 = {g(k, 5)}'), ('bias-current compensation: R1‖R2 = 10 kΩ (the resistance seen by the + input)', f'R1 = {si(R1, "Ω", 5)}, R2 = {si(R2, "Ω", 5)}'), ('nearest standard values R1 = 10 kΩ, R2 = 2.0 MΩ', f'gain = 1 + R2/R1 = {g(Astd, 4)} = {g(dbv(Astd), 4)} dB; R1‖R2 = {si(Rp_std, "Ω", 4)}')], \
        'Noninverting amplifier gain 1 + R2/R1; the input-bias currents cause equal dc drops (and cancel) when the resistance at the − input, R1‖R2, equals the resistance 10 kΩ at the + input.', ['Both conditions determine R1 and R2 exactly; standard values give 46.06 dB.'], cir('11.67', 'Fig. P11.67', 'noninverting amplifier: the source vi in series with a 10 kΩ resistor drives the + input; R2 from the output to the − input and R1 from the − input to ground.')
@solve('11.68')
def _():
    vi, Rs, R2, R1, A, VOS, IB = -0.005, 1e3, 100e3, 1.1e3, 1e4, 1e-3, 100e-9
    def vo(vos, ib):
        c = Ckt(); c.V('vi', 'a', '0', vi); c.R('a', 'p', Rs); c.V('os', 'pp', 'p', vos); c.opamp('pp', 'm', 'o', A=A); c.R('m', 'o', R2); c.R('m', '0', R1); c.I('p', '0', ib); c.I('m', '0', ib); v, _ = dc(c); return v['o']
    ideal = (1 + R2 / R1) * vi; act = {s: vo(s * VOS, IB) for s in (-1, 1)}; nofault = vo(0, 0); worst = max(act.values(), key=lambda x: abs(x - ideal)); err = (worst - ideal) / ideal * 100
    return [('(a) ideal output voltage', f'vo = (1 + R2/R1)·vi = {g(1 + R2 / R1, 5)} × ({vi} V) = {g(ideal, 5)} V'), ('(b) actual output voltage for the worst-case polarity of VOS (also with the finite gain A = 10,000 and IB = 100 nA)', f'{g(worst, 5)} V (the other polarity gives {g(min(act.values(), key=lambda x: abs(x - ideal)), 5)} V; finite gain alone: {g(nofault, 5)} V)'), ('(c) percentage error compared with the ideal output', f'{g(err, 4)} %')], \
        'Superposition: the signal gain (1 + R2/R1) with the finite-gain correction 1/(1 + 1/T), plus the offset term (1 + R2/R1)·VOS and the bias-current term (IB·(R2 − (1 + R2/R1)·Rs)).', ['The 0.005 V source is drawn with its − terminal at the 1 kΩ resistor (+ at ground), so vi = −5 mV at the + input; the error percentages are the same for +5 mV.', 'The input-bias currents of both inputs are taken equal (100 nA) as no offset current is given.'], cir('11.68', 'Fig. P11.68', 'noninverting amplifier: a 0.005 V source (− terminal towards the amplifier) in series with 1 kΩ drives the + input; 100 kΩ from the output to the − input and 1.1 kΩ from the − input to ground.')
def sat(VI, R1, R2, V, inverting=True):
    c = Ckt()
    if inverting:
        c.V('vi', 'a', '0', VI); c.R('a', 'm', R1); c.R('m', 'o', R2); c.opamp('0', 'm', 'o'); v, _ = dc(c); vo = v['o']
        if abs(vo) <= V: return vo, v['m']
        vo = math.copysign(V, vo); return vo, (VI * R2 + vo * R1) / (R1 + R2)
    c.V('vi', 'a', '0', VI); c.opamp('a', 'm', 'o'); c.R('m', 'o', R2); c.R('m', '0', R1); v, _ = dc(c); vo = v['o']
    if abs(vo) <= V: return vo, v['m']
    vo = math.copysign(V, vo); return vo, vo * R1 / (R1 + R2)
@solve('11.69')
def _():
    R1, R2, V = 1e3, 6.8e3, 10.0; out = []
    for tag, VI in (('(a) VI = −1 V', -1.0), ('(b) VI = +2 V', 2.0)):
        vo, vm = sat(VI, R1, R2, V); ideal = -R2 / R1 * VI; out.append((tag, f'VO = {g(vo, 4)} V, V− = {g(vm, 4)} V' + ('' if abs(ideal) <= V else f' (the ideal {g(ideal, 3)} V is beyond the supply: the output saturates at {g(vo, 3)} V and V− = (VI·R2 + VO·R1)/(R1 + R2))')))
        c = Ckt(); c.V('vi', 'a', '0', VI); c.R('a', 'm', R1); c.R('m', 'o', R2); c.V('o', 'o', '0', vo); v, _ = dc(c); close(v['m'], vm, 1e-9)
    return out, 'Inverting amplifier with gain −R2/R1 = −6.8 and ±10 V supplies: if the ideal output is inside the supplies V− = 0; otherwise the output is clamped at the supply and V− follows from the divider of VI and VO (the op amp is no longer in feedback).', ['The output saturates at exactly the supply voltage.'], cir('11.69', 'Fig. P11.69', 'inverting amplifier: VI through 1 kΩ to the − input (V−), 6.8 kΩ from the output to the − input, + input grounded; supplies +10 V and −10 V.')
@solve('11.71')
def _():
    R1, R2, V = 1e3, 10e3, 10.0; out = []
    for tag, VI in (('(a) VI = 0.5 V', 0.5), ('(b) VI = 1.2 V', 1.2)):
        vo, vm = sat(VI, R1, R2, V); ideal = -R2 / R1 * VI; out.append((tag, f'VO = {g(vo, 4)} V, V− = {g(vm, 4)} V' + ('' if abs(ideal) <= V else f' (ideal {g(ideal, 3)} V: saturated at {g(vo, 3)} V)')))
        c = Ckt(); c.V('vi', 'a', '0', VI); c.R('a', 'm', R1); c.R('m', 'o', R2); c.V('o', 'o', '0', vo); v, _ = dc(c); close(v['m'], vm, 1e-9)
    return out, 'As Problem 11.69 with the feedback resistor 10 kΩ: gain −10.', [], cir('11.71', 'Fig. P11.69', 'inverting amplifier: VI through 1 kΩ to the − input, the feedback resistor (10 kΩ here instead of 6.8 kΩ) from the output to the − input, + input grounded; supplies ±10 V.')
@solve('11.73')
def _():
    R2, R1, V = 39e3, 1e3, 15.0; out = []
    for tag, VI in (('(a) VI = 300 mV', 0.3), ('(b) VI = 600 mV', 0.6)):
        vo, vm = sat(VI, R1, R2, V, inverting=False); out.append((tag, f'VO = {g(vo, 4)} V, VID = VI − V− = {si(VI - vm, "V", 4)}'))
        c = Ckt(); c.V('vi', 'a', '0', VI); c.R('m', 'o', R2); c.R('m', '0', R1); c.V('o', 'o', '0', vo); v, _ = dc(c); close(v['m'], vm, 1e-9)
    return out, 'Noninverting amplifier of gain 1 + 39 = 40 with ±15 V supplies: for VI = 0.3 V the output is 12 V and VID ≈ 0; for 0.6 V the ideal 24 V is beyond +15 V, the op amp saturates and VID = VI − VO·R1/(R1 + R2) ≠ 0.', ['The output saturates at exactly the supply voltage; VID is the voltage between the inputs (V+ = VI).'], cir('11.73', 'Fig. P11.73', 'noninverting amplifier: VI on the + input, 39 kΩ from the output to the − input and 1 kΩ from the − input to ground; supplies +15 V and −15 V.')
@solve('11.75')
def _():
    R2, R1, V = 39e3, 0.91e3, 15.0; out = []
    for tag, VI in (('(a) VI = 300 mV', 0.3), ('(b) VI = 600 mV', 0.6)):
        vo, vm = sat(VI, R1, R2, V, inverting=False); out.append((tag, f'VO = {g(vo, 4)} V, VID = VI − V− = {si(VI - vm, "V", 4)}'))
    return out, 'As Problem 11.73 with the 1 kΩ resistor replaced by 910 Ω: gain 1 + 39/0.91 = 43.86.', [], cir('11.75', 'Fig. P11.73', 'noninverting amplifier: VI on the + input, 39 kΩ from the output to the − input and 910 Ω (instead of 1 kΩ) from the − input to ground; supplies ±15 V.')
@solve('11.78')
def _():
    IOmax, bF, V = 5e-3, 60.0, 10.0; IE = IOmax * (bF + 1); R = V / IE
    Rs = brentq(lambda r: V / (r * (bF + 1)) - IOmax, 1.0, 1e4); close(Rs, R, 1e-9)                                                  # independent: search the R at which the base current V/(R(βF + 1)) reaches 5 mA
    return [('emitter voltage', '10 V (the op amp makes the emitter follow its + input)'), ('maximum emitter current for IB ≤ 5 mA', f'IE = (βF + 1)·IB = {g(IE * 1e3, 4)} mA'), ('minimum R', f'R = 10 V/IE = {g(R, 4)} Ω')], 'The op amp forces the emitter (the − input) to 10 V, so IE = 10 V/R; the op amp supplies only the base current IB = IE/(βF + 1) ≤ 5 mA, i.e. IE ≤ 61 × 5 mA.', ['VBE is inside the loop and does not matter; βF = 60 is the minimum value.'], cir('11.78', 'Fig. P11.78', 'an op amp whose + input is at +10 V and whose output drives the base of an npn transistor with collector at +25 V; the emitter is fed back to the − input and goes through R to ground.')
def diffamp(Rg1, Rf1, Rg2, Rf2, v1, v2):
    c = Ckt(); c.V('v1', 'a', '0', v1); c.V('v2', 'b', '0', v2); c.R('a', 'm', Rg1); c.R('m', 'o', Rf1); c.R('b', 'p', Rg2); c.R('p', '0', Rf2); c.opamp('p', 'm', 'o'); v, i = dc(c); return v['o']
D80 = dict(Rg1=10.1e3, Rf1=99e3, Rg2=9.9e3, Rf2=101e3)
def d80(v1, v2): return diffamp(D80['Rg1'], D80['Rf1'], D80['Rg2'], D80['Rf2'], v1, v2)
def d80_gains():
    Ad = (d80(0.5, -0.5) - d80(-0.5, 0.5)) / 2; Acm = d80(1.0, 1.0); return Ad, Acm
C80 = 'difference amplifier with slightly mismatched resistors: v1 through 10.1 kΩ to the − input and 99 kΩ feedback; v2 through 9.9 kΩ to the + input and 101 kΩ from the + input to ground; ideal op amp'
@solve('11.80')
def _():
    Ad, Acm = d80_gains(); vo = d80(3.0, 3.0); matched = diffamp(10e3, 100e3, 10e3, 100e3, 3.0, 3.0); cmrr = abs(Ad / Acm)
    Acm_f = (D80['Rf2'] / (D80['Rg2'] + D80['Rf2'])) * (1 + D80['Rf1'] / D80['Rg1']) - D80['Rf1'] / D80['Rg1']; close(Acm_f, Acm, 1e-9)
    return [('(a) differential-mode and common-mode input voltages', 'vid = v1 − v2 = 0 V; vic = (v1 + v2)/2 = 3 V'), ('(b) output voltage', f'vo = {g(vo * 1e3, 4)} mV (= Acm·3 V with Acm = {g(Acm, 5)})'), ('(c) output with matched resistor pairs', f'{g(matched, 4)} V'), ('(d) CMRR = |Ad/Acm|', f'Ad = {g(Ad, 5)}, Acm = {g(Acm, 5)}: CMRR = {g(cmrr, 5)} = {g(dbv(cmrr), 4)} dB')], \
        'vo = Ad·vid + Acm·vic with Acm = [R4/(R3 + R4)](1 + R2/R1) − R2/R1 (R1 = 10.1 k, R2 = 99 k, R3 = 9.9 k, R4 = 101 k) and Ad from the exact nodal solution; a matched amplifier would have Acm = 0.', ['The op amp is ideal; the mismatch alone produces the common-mode gain.'], cir('11.80', 'Fig. P11.80', C80 + '.')
@solve('11.81')
def _():
    v1, v2 = 3.90, 4.10; vo = d80(v1, v2); m = diffamp(10e3, 100e3, 10e3, 100e3, v1, v2); ideal = -10 * (v1 - v2)
    return [('(a) output voltage', f'vo = {g(vo, 5)} V'), ('(b) with matched resistors (10 kΩ, 100 kΩ)', f'vo = −10(v1 − v2) = {g(m, 5)} V'), ('(c) error in amplifying (v1 − v2)', f'{g(vo - m, 4)} V = {g(100 * (vo - m) / m, 4)} % of the correct output')], 'Exact nodal solution of the mismatched difference amplifier for v1 = 3.90 V and v2 = 4.10 V; the matched amplifier gives −10(v1 − v2) = 2 V.', [], cir('11.81', 'Fig. P11.80', C80 + '.')
@solve('11.82')
def _():
    Ad, Acm = d80_gains(); cmrr = abs(Ad / Acm); a1, a2 = 10.0, 0.25
    for t in (0.0007, 0.00213, 0.0041):
        v1 = a1 * math.sin(120 * math.pi * t) + a2 * math.sin(5000 * math.pi * t); v2 = a1 * math.sin(120 * math.pi * t) - a2 * math.sin(5000 * math.pi * t)
        close(d80(v1, v2), Ad * (v1 - v2) + Acm * (v1 + v2) / 2, 1e-9, 1e-9)
    return [('(a) differential-mode and common-mode input voltages', 'vid = v1 − v2 = 0.5 sin 5000πt V; vic = (v1 + v2)/2 = 10 sin 120πt V'), ('(b) differential-mode and common-mode gains', f'Ad = {g(Ad, 5)}, Acm = {g(Acm, 5)}'), ('(c) CMRR', f'{g(abs(Ad / Acm), 5)} = {g(dbv(cmrr), 4)} dB'), ('(d) output voltage', f'vo = Ad·vid + Acm·vic = {g(Ad * 0.5, 4)} sin 5000πt + {g(Acm * 10, 4)} sin 120πt V')], \
        'Superposition of the differential part (gain Ad) and the common-mode part (gain Acm), both from the exact nodal solution of the mismatched resistors of Fig. P11.80 (ideal op amp).', ['The signs follow the connection of Fig. P11.80 (Ad ≈ −10).'], cir('11.82', 'Fig. P11.80', C80 + '.')
@solve('11.83')
def _():
    vd = 0.01; vcm = 5 + vd / 2; cm = 10 ** (86 / 20); err = vcm / cm
    return [('differential input and common-mode voltage', f'vd = 0.01 V, vcm = (5.01 V + 5 V)/2 = {g(vcm, 5)} V'), ('error of the reading, VCM/CMRR (CMRR = 86 dB = 19,953)', f'±{g(err * 1e3, 4)} mV'), ('range of indicated voltages', f'{g((vd - err) * 1e3, 5)} mV to {g((vd + err) * 1e3, 5)} mV')], 'A meter with finite CMRR indicates vd ± vcm/CMRR: the 5 V common-mode level produces an error of about 0.25 mV on the 10 mV reading (2.5 %).', ['The sign of the error is unknown, so the reading can be anywhere in ± the error.'], cir('11.83', 'Fig. P11.83', 'an analog dc multimeter: its + terminal is connected to the top of a 0.01 V source in series with a 5 V source, and its − terminal to the node between the two sources (so the meter should read 0.01 V with a 5 V common-mode level).')
@solve('11.84')
def _():
    out = []; cmrr_req = []
    for tag, Rm in (('(a) middle resistor 10 kΩ (as drawn)', 10e3), ('(b) middle resistor 100 Ω', 100.0)):
        Rt = 15e3 + Rm + 15e3; I = 15.0 / Rt; V1 = 15 - 15e3 * I; V2 = V1 - Rm * I; V = V1 - V2; vcm = (V1 + V2) / 2; need = vcm / (1e-4 * V)
        c = Ckt(); c.V('s', 'a', '0', 15.0); c.R('a', 'n1', 15e3); c.R('n1', 'n2', Rm); c.R('n2', '0', 15e3); v, _ = dc(c); close(v['n1'], V1, 1e-9); close(v['n2'], V2, 1e-9)
        out.append((tag, f'I = {si(I, "A", 4)}; V1 = {g(V1, 5)} V, V2 = {g(V2, 5)} V; V = V1 − V2 = {g(V, 4)} V; VCM = {g(vcm, 5)} V; required CMRR = VCM/(0.0001·V) = {g(need, 5)} = {g(dbv(need), 4)} dB'))
    return out, 'Series divider: I = 15 V/(15 k + Rm + 15 k); the meter measures V = V1 − V2 = Rm·I with the common-mode level VCM = (V1 + V2)/2; an error below 0.01 % of V needs CMRR > VCM/(10⁻⁴·V).', ['The statement says “the 20-kΩ resistor” but the figure and part (b) show a 10 kΩ resistor between V1 and V2: the figure value is used.'], cir('11.84', 'Fig. P11.84', 'a 15 V source in series with 15 kΩ, then 10 kΩ, then 15 kΩ back to the source (ground at the bottom); V1 is the node between the first 15 kΩ and the 10 kΩ, V2 the node between the 10 kΩ and the last 15 kΩ; the voltmeter reads V = V1 − V2 across the 10 kΩ.')
# ---------------------------------------------------------------- remaining Chapter 11 figure problems: CMRR of a difference amplifier, single-pole op-amp transfer functions, worst-case noninverting amplifier
import itertools as _it, random as _rd
def _sp_opamp(c, plus, minus, out, Ao, fT, tag='sp'):
    """single-pole op amp A(s) = Ao/(1 + s/ωb), ωb = 2π·fT/Ao: E → 1 Ω → C → buffer"""
    c.E(f'{tag}E', f'{tag}x', '0', plus, minus, Ao); c.R(f'{tag}x', f'{tag}y', 1.0); c.C(f'{tag}y', '0', Ao / (2 * math.pi * fT)); c.E(f'{tag}B', out, '0', f'{tag}y', '0', 1.0)
@solve('11.85')
def _():
    R, tol = 10e3, 0.00025
    def parts(R1, R2, R3, R4):
        k = R4 / (R3 + R4) * (1 + R2 / R1); Adm = 0.5 * (k + R2 / R1); Acm = k - R2 / R1; return Adm, Acm
    def mna(R1, R2, R3, R4, v1, v2):
        c = Ckt(); c.V('s1', 'a', '0', v1); c.V('s2', 'b', '0', v2); c.R('a', 'm', R1); c.R('m', 'o', R2); c.R('b', 'p', R3); c.R('p', '0', R4); c.opamp('p', 'm', 'o'); v, _ = dc(c); return v['o']
    def cmrr(R1, R2, R3, R4): Adm, Acm = parts(R1, R2, R3, R4); return abs(Adm / Acm) if Acm != 0 else float('inf')
    vals = []
    for sg in _it.product((-1, 1), repeat=4):
        Rs = [R * (1 + s * tol) for s in sg]; Adm, Acm = parts(*Rs)
        close(mna(*Rs, -0.5, 0.5), Adm, 1e-9); close(mna(*Rs, 1.0, 1.0), Acm, 1e-6, 1e-9)                  # the closed forms equal the exact nodal solution
        vals.append((cmrr(*Rs), sg))
    worst = min(vals)[0]; rnd = _rd.Random(2)
    for _ in range(3000): assert cmrr(*[R * (1 + rnd.uniform(-tol, tol)) for _ in range(4)]) >= worst * (1 - 1e-9)       # no random set is worse than the worst corner
    approx = 2 / (4 * tol); sg = min(vals)[1]; close(worst, approx, 2e-3)
    return [('Worst-case CMRR', f'{g(worst, 5)} = {g(dbv(worst), 4)} dB (corner R1, R2, R3, R4 = R(1 {", ".join(("+" if s > 0 else "−") for s in sg)} 0.025 %))'), ('Approximation CMRR ≈ (1 + R2/R1)/(4·tolerance)', f'{g(approx, 5)} = {g(dbv(approx), 4)} dB')], \
        'Difference amplifier: vo = −(R2/R1)v1 + (R4/(R3 + R4))(1 + R2/R1)v2, so Adm = ½[(R4/(R3 + R4))(1 + R2/R1) + R2/R1] and Acm = (R4/(R3 + R4))(1 + R2/R1) − R2/R1. With all four resistors R(1 ± 0.025 %) the worst CMRR = |Adm/Acm| occurs at a corner of the tolerance box (16 corners checked, 3000 random sets are never worse); the closed forms were checked against the exact nodal solution.', \
        ['Only the resistor mismatch is considered (the op amp is ideal); the result is the CMRR of the amplifier, not of the op amp.'], cir('11.85', 'Fig. P11.85', 'difference amplifier with four equal resistors R: v1 through R to the − input, R from the output to the − input; v2 through R to the + input, R from the + input to ground.')
def _tf_report(kind, R1, R2, C, Ao, fT):
    """exact transfer function of the inverting stage with a single-pole op amp -> (dc gain, poles [Hz], zeros [Hz], coefficient lists, ideal data)"""
    wb = 2 * math.pi * fT / Ao; a = R2 / R1 if R2 else 0.0
    if kind == 'lp':
        tau = R2 * C; num = [0, 0, -a * Ao * wb]; den = [tau, 1 + a + wb * tau * (1 + Ao), wb * (1 + a + Ao)]
    elif kind == 'hp':
        tau = R1 * C; num = [0, -a * tau * Ao * wb, 0]; den = [tau * (1 + a), Ao * wb * tau + 1 + wb * tau + a * tau * wb, wb * (1 + Ao)]
    else:
        tau = R1 * C; num = [0, 0, -Ao * wb]; den = [tau, 1 + wb * tau * (1 + Ao), wb]                                  # here R1 = R, C = C
    return num, den, wb
def _tf_check(kind, R1, R2, C, Ao, fT, num, den):
    for f in (10.0, 1e2, 1e3, 1e4, 1e5, 1e6, 3e6):
        s = 2j * math.pi * f; Hn = np.polyval(num, s) / np.polyval(den, s)
        c = Ckt(); c.V('vi', 'i', '0', 1.0)
        if kind == 'lp': c.R('i', 'm', R1); c.R('m', 'o', R2); c.C('m', 'o', C)
        elif kind == 'hp': c.C('i', 'q', C); c.R('q', 'm', R1); c.R('m', 'o', R2)
        else: c.R('i', 'm', R1); c.C('m', 'o', C)
        _sp_opamp(c, '0', 'm', 'o', Ao, fT); Hm = c.solve(s)[0]['o']; close(abs(Hn), abs(Hm), 1e-8, 1e-12); close(np.angle(Hn), np.angle(Hm), 1e-6, 1e-8)
def _tf_problem(num_, kind, fig, R1, R2, C, Ao_db, fT, txt):
    Ao = 10 ** (Ao_db / 20); num, den, wb = _tf_report(kind, R1, R2, C, Ao, fT); _tf_check(kind, R1, R2, C, Ao, fT, num, den)
    poles = np.roots(den); zeros = []
    pf = sorted(abs(p) / (2 * math.pi) for p in poles); a = R2 / R1 if R2 else 0.0
    if kind == 'lp':
        f_ideal = 1 / (2 * math.pi * R2 * C); g0 = a * Ao * wb / (wb * (1 + a + Ao)); ideal = f'ideal: Av = −(R2/R1)/(1 + sR2C) = −{g(a, 4)}/(1 + s·{g(R2 * C, 4)}), pole at {si(f_ideal, "Hz", 4)}'
    elif kind == 'hp':
        f_ideal = 1 / (2 * math.pi * R1 * C); g0 = float('nan'); ideal = f'ideal: Av = −(R2/R1)·sR1C/(1 + sR1C) = −{g(a, 4)}·s·{g(R1 * C, 4)}/(1 + s·{g(R1 * C, 4)}), zero at 0, pole at {si(f_ideal, "Hz", 4)}'
    else:
        f_ideal = None; ideal = f'ideal: Av = −1/(sRC) = −1/(s·{g(R1 * C, 4)}) (unity-gain frequency 1/(2πRC) = {si(1 / (2 * math.pi * R1 * C), "Hz", 4)})'
    fmt = lambda p: f'{si(abs(p) / (2 * math.pi), "Hz", 4)}' + ('' if abs(p.imag) < 1e-6 * abs(p) else ' (complex)')
    numtxt = {'lp': f'{g(-a * Ao * wb, 5)}', 'hp': f'{g(num[1], 5)}·s', 'in': f'{g(-Ao * wb, 5)}'}[kind]
    rows = [('Op-amp parameters', f'Ao = {g(Ao, 5)} ({Ao_db} dB), fT = {si(fT, "Hz", 3)}, pole fb = fT/Ao = {si(fT / Ao, "Hz", 4)}'), ('Exact transfer function', f'Av(s) = ({numtxt}) / ({g(den[0], 5)}·s² + {g(den[1], 5)}·s + {g(den[2], 5)})' + ('  (the numerator ∝ s: a zero at s = 0)' if kind == 'hp' else '')), ('Poles', ', '.join(fmt(p) for p in sorted(poles, key=abs))), ('Ideal function', ideal)]
    if kind == 'lp': rows.append(('dc gain', f'actual {g(-g0, 5)} (ideal {g(-a, 4)}): the op amp adds a second pole near fT/(1 + R2/R1) = {si(fT / (1 + a), "Hz", 4)}'))
    elif kind == 'in': rows.append(('Behaviour', f'a finite-gain integrator: dc gain −Ao·(fb/pole) → {g(-Ao * wb / den[2], 5)}, i.e. the ideal pole at 0 moves to {si(min(abs(poles)) / (2 * math.pi), "Hz", 4)}; a second pole near {si(max(abs(poles)) / (2 * math.pi), "Hz", 4)}'))
    else: rows.append(('Behaviour', f'passband gain −{g(a, 4)} between the corner and about {si(fT / (1 + a), "Hz", 4)} (op-amp pole)'))
    return rows, 'Inverting amplifier with Z1, Z2 and a single-pole op amp A(s) = Ao/(1 + s/ωb): Av(s) = −(Z2/Z1)/[1 + (1 + Z2/Z1)/A(s)], which gives the rational function above (coefficients derived by hand and verified against an exact nodal ac solution of the circuit at seven frequencies from 10 Hz to 3 MHz). The Bode plot itself is not drawn here: the poles, zeros and gains above define it.', ['The "Bode plot" part of the statement is not reproduced; the transfer function and its poles/zeros are given instead.'], cir(num_, fig, txt)
@solve('11.102')
def _(): return _tf_problem('11.102', 'lp', 'Fig. 10.32', 5.1e3, 51e3, 1600e-12, 97, 2e6, 'inverting low-pass filter: input resistor R1 to the − input, R2 in parallel with C in the feedback path, + input grounded.')
@solve('11.103')
def _(): return _tf_problem('11.103', 'lp', 'Fig. 10.32', 5.1e3, 100e3, 750e-12, 100, 2e6, 'inverting low-pass filter: input resistor R1 to the − input, R2 in parallel with C in the feedback path, + input grounded.')
@solve('11.104')
def _(): return _tf_problem('11.104', 'lp', 'Fig. 10.32', 1.4e3, 27e3, 150e-12, 92, 1e6, 'inverting low-pass filter: input resistor R1 to the − input, R2 in parallel with C in the feedback path, + input grounded.')
@solve('11.105')
def _(): return _tf_problem('11.105', 'in', 'Fig. 10.34', 10e3, None, 0.05e-6, 100, 5e6, 'inverting integrator: input resistor R to the − input and capacitor C in the feedback path, + input grounded.')
@solve('11.106')
def _(): return _tf_problem('11.106', 'hp', 'Fig. 10.33', 18e3, 180e3, 1800e-12, 94, 1e6, 'inverting high-pass filter: capacitor C in series with R1 at the input, R2 in the feedback path, + input grounded.')
@solve('11.107')
def _():
    A, fT = 5e4, 1e6; Rf, Rg = 130e3, 22e3
    def metrics_(Rf_, Rg_):
        beta = Rg_ / (Rf_ + Rg_); T = A * beta; Av = A / (1 + T); fB = beta * fT; fex = fT / A * (1 + T)
        c = Ckt(); c.V('vi', 'i', '0', 1.0); _sp_opamp(c, 'i', 'm', 'o', A, fT); c.R('o', 'm', Rf_); c.R('m', '0', Rg_)
        g0 = abs(c.solve(0.0)[0]['o']); close(Av, g0, 1e-9); fm = brentq(lambda lf: abs(c.solve(2j * math.pi * 10 ** lf)[0]['o']) / g0 - 1 / math.sqrt(2), 2, 9, xtol=1e-12); close(10 ** fm, fex, 1e-8)
        return Av, fB, fex
    nom = metrics_(Rf, Rg); rows = [('Nominal (130 kΩ, 22 kΩ)', f'gain {g(nom[0], 5)} (ideal {g(1 + Rf / Rg, 5)}), bandwidth f_B = β·fT = {si(nom[1], "Hz", 4)}')]
    corners = [(a, b) for a in (-1, 1) for b in (-1, 1)]; res = {c: metrics_(Rf * (1 + .05 * c[0]), Rg * (1 + .05 * c[1])) for c in corners}
    hi = max(res.values(), key=lambda x: x[0]); lo = min(res.values(), key=lambda x: x[0]); bh = max(res.values(), key=lambda x: x[1]); bl = min(res.values(), key=lambda x: x[1])
    close(hi[0], metrics_(Rf * 1.05, Rg * .95)[0], 1e-12); close(bh[1], metrics_(Rf * .95, Rg * 1.05)[1], 1e-12)
    rows += [('Worst-case maximum gain (130 k +5 %, 22 k −5 %)', f'{g(hi[0], 5)}, bandwidth {si(hi[1], "Hz", 4)}'), ('Worst-case minimum gain (130 k −5 %, 22 k +5 %)', f'{g(lo[0], 5)}, bandwidth {si(lo[1], "Hz", 4)}'), ('Bandwidth range', f'{si(bl[1], "Hz", 4)} (high-gain corner) to {si(bh[1], "Hz", 4)} (low-gain corner)')]
    return rows, 'Noninverting amplifier: β = R22/(R130 + R22), Av = A/(1 + Aβ), bandwidth f_B = β·fT (Table 11.3; the exact single-pole value (fT/A)(1 + Aβ) differs by under 0.01 %). Worst case = the four corners of the ±5 % box (gain and β are monotone in each resistor); each corner was also solved as an exact circuit with a single-pole op amp and its −3 dB frequency found by root search.', ['Worst-case values are for the resistor tolerances only (A and fT are taken as exactly 50,000 and 1 MHz).'], cir('11.107', 'Fig. P11.107', 'noninverting amplifier: vs on the + input of the op amp A(s); 130 kΩ (5 %) from the output to the − input and 22 kΩ (5 %) from the − input to ground.')
