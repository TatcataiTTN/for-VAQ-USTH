"""Jaeger 5e worked Examples (chapters 10-12) that refer to a circuit drawn in a figure.  The figure was read (build/numeric/jfigexport.py cuts it from the vector drawing of the page), the
values are the ones printed in the Example's own statement, each result is looked up in the book's printed solution (must_in_book) and recomputed with an exact nodal solution
(jsol/mna.py) of the circuit as the independent route.  A solver returns (parts, how, assume, ctx, circuit)."""
import math, os, sys, json
import numpy as np
from core import *
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.append(os.path.join(HERE, '..', 'jsol'))
from mna import Ckt, dc
J = 'jaeger'
_cat = None
def pg(num):
    global _cat
    if _cat is None: _cat = json.load(open(os.path.join(HERE, '..', '..', '..', 'data', 'numeric', 'catalog.json'), encoding='utf-8'))
    return next(e['printed'] for e in _cat if e['book'] == 'jaeger5' and e['kind'] == 'example' and e['number'] == num)
def cj(num, fig, text): return f'{fig} (p.{pg(num)}): {text}'
@solve('jaeger5', 'example', 10, '10.5')
def _():
    R1, R2, vi = 3e3, 43e3, 0.1; Av = 1 + R2 / R1; vo = Av * vi; io = vo / (R1 + R2)
    c = Ckt(); c.V('vi', 'i', '0', vi); c.opamp('i', 'm', 'o'); c.R('o', 'm', R2); c.R('m', '0', R1); v, _ = dc(c); close(v['o'], vo, 1e-8); close((v['o'] - v['m']) / R2, io, 1e-6)
    must_in_book(J, '10.5', ['+15.3', '1.53 V', '33.3'])
    return [('Voltage gain Av = 1 + R2/R1', g(Av, 4)), ('Output voltage vo = Av·vi', f'{g(vo, 4)} V'), ('Output current io = vo/(R1 + R2)', si(io, 'A', 3))], 'Ideal noninverting amplifier (Eq. 10.53): Av = 1 + R2/R1; the input current is zero, so the output current flows only through R2 + R1. The exact nodal solution gives the same vo and io.', ['Ideal op amp.'], None, \
        cj('10.5', 'Fig. 10.22', 'noninverting amplifier: vi on the + input, R2 from the output to the − input, R1 from the − input to ground; R1 = 3 kΩ, R2 = 43 kΩ, vi = +0.1 V.')
@solve('jaeger5', 'example', 10, '10.7')
def _():
    V1, V2, R1, R2 = 5.0, 3.0, 10e3, 100e3; Vp = V2 * R2 / (R1 + R2); I1 = (V1 - Vp) / R1; VO = V1 - I1 * (R1 + R2); IO = -I1
    c = Ckt(); c.V('s1', 'a', '0', V1); c.V('s2', 'b', '0', V2); c.R('a', 'm', R1); c.R('m', 'o', R2); c.R('b', 'p', R1); c.R('p', '0', R2); c.opamp('p', 'm', 'o'); v, _ = dc(c)
    close(v['o'], VO, 1e-8); close(v['p'], Vp, 1e-8); close(v['m'], Vp, 1e-8); close((v['a'] - v['m']) / R1, I1, 1e-6); close(VO, -R2 / R1 * (V1 - V2), 1e-9)
    must_in_book(J, '10.7', ['2.73 V', '227', '−20.0 V'])
    return [('V+ = V− = V2·R2/(R1 + R2)', f'{g(Vp, 3)} V'), ('I1 = I2 = (V1 − V−)/R1', si(I1, 'A', 3)), ('VO = V1 − I1(R1 + R2)', f'{g(VO, 4)} V'), ('Op-amp output current IO = −I2', si(IO, 'A', 3))], 'Ideal difference amplifier: V+ from the divider on V2, V− = V+, I1 from Ohm\'s law on R1, VO from KVL around R1 and R2; check: VO = −(R2/R1)(V1 − V2) = −20 V. Exact nodal solution agrees.', ['Ideal op amp.'], None, \
        cj('10.7', 'Fig. 10.25', 'difference amplifier: V1 through R1 to the − input with R2 feedback; V2 through R1 to the + input with R2 to ground; V1 = 5 V, V2 = 3 V, R1 = 10 kΩ, R2 = 100 kΩ.')
@solve('jaeger5', 'example', 11, '11.4')
def _():
    Rid, A, R1, R2 = 2e6, 10 ** (90 / 20), 20e3, 510e3; beta = R1 / (R1 + R2); Rin = Rid * (1 + A * beta)
    c = Ckt(); c.V('vs', 'i', '0', 1.0); c.opamp('i', 'm', 'o', A=A, Rid=Rid); c.R('o', 'm', R2); c.R('m', '0', R1); v, i = dc(c); Rex = 1.0 / (-i['vs']); close(Rex, Rin, 2e-2)
    must_in_book(J, '11.4', ['26.5', '2.39', 'GΩ'])
    return [('β = R1/(R1 + R2)', f'{g(beta, 4)} = 1/{g(1 / beta, 3)}'), ('A = 10^(90/20)', g(A, 5)), ('Rin = Rid(1 + Aβ)', si(Rin, 'Ω', 3))], f'Eq. (11.31) for the series-shunt noninverting amplifier: Rin = Rid(1 + Aβ). The exact nodal solution of the circuit (Rid between the inputs) gives {si(Rex, "Ω", 3)}; the small difference is the loading of Rid by R1‖R2, which the formula neglects.', ['Op amp ideal except for the finite gain A = 90 dB and Rid = 2 MΩ (Ro = 0).'], None, \
        cj('11.4', 'Fig. 11.6', 'noninverting amplifier with a finite-gain op amp having input resistance Rid between the inputs: vx on the + input, R2 from the output to the − input, R1 from the − input to ground.')
@solve('jaeger5', 'example', 11, '11.10')
def _():
    VOS, R1, R2 = 3e-3, 1.2e3, 99e3; VO = (1 + R2 / R1) * VOS
    c = Ckt(); c.V('vos', 'p', '0', VOS); c.opamp('p', 'm', 'o'); c.R('o', 'm', R2); c.R('m', '0', R1); v, _ = dc(c); close(v['o'], VO, 1e-8)
    must_in_book(J, '11.10', ['0.25 V'])
    return [('|VO| ≤ (1 + R2/R1)·|VOS|', f'{g(VO, 4)} V'), ('Range (the sign of VOS is not known)', f'−{g(VO, 3)} V ≤ VO ≤ +{g(VO, 3)} V')], 'Offset of an otherwise ideal noninverting amplifier (Eq. 11.95): the offset voltage is amplified by the noninverting gain 1 + R2/R1 = 83.5. The exact nodal solution (offset source at the + input) agrees.', ['The sign of VOS is not specified (only |VOS| ≤ 3 mV), so only the range is known.'], None, \
        cj('11.10', 'Fig. 11.32', 'noninverting amplifier with the input grounded (vI = 0) and the op-amp offset voltage VOS modelled in series with the + input; R2 = 99 kΩ from the output to the − input, R1 = 1.2 kΩ from the − input to ground.')
@solve('jaeger5', 'example', 11, '11.11')
def _():
    R1, R2, RL, VO, IOmax = 10e3, 100e3, 5e3, 10.0, 2.5e-3
    c = Ckt(); c.V('vi', 'i', '0', -1.0); c.R('i', 'm', R1); c.opamp('0', 'm', 'o'); c.R('o', 'm', R2); c.R('o', '0', RL); v, _ = dc(c); close(v['o'], VO, 1e-8)
    IO = v['o'] / RL + v['o'] / (R1 + R2) * 0 + (v['o'] - v['m']) / R2; close(IO, 2.09e-3, 5e-3); assert IO < IOmax
    ok = [(a, b) for a, b in ((2.2e3, 22e3), (2.7e3, 27e3), (4.7e3, 47e3), (10e3, 100e3)) if (10 / (RL * 1) + 10 / b) < IOmax and abs(b / a - 10) < 1e-9]; assert len(ok) == 4
    must_in_book(J, '11.11', ['R2 ≥ 20 kΩ', 'R1 = 10 kΩ and R2 = 100 kΩ', '2.1 mA'])
    return [('Load of the op amp for |vO| = 10 V: REQ = 10 V/2.5 mA', '4 kΩ; with RL ≥ 5 kΩ the feedback resistor must satisfy RL‖R2 ≥ 4 kΩ, i.e. R2 ≥ 20 kΩ'), ('Gain 20 dB', '|Av| = R2/R1 = 10'), ('Acceptable pairs (R1, R2)', '2.2 kΩ/22 kΩ, 2.7 kΩ/27 kΩ, 4.7 kΩ/47 kΩ, 10 kΩ/100 kΩ'), ('Chosen design', f'R1 = 10 kΩ, R2 = 100 kΩ: IO = 10 V/5 kΩ + 10 V/110 kΩ = {si(IO, "A", 3)} < 2.5 mA, Rin = 10 kΩ')], \
        'The op amp supplies the load current and the current in the feedback network: IO = vO/RL + vO/(R1 + R2). With RL = 5 kΩ the current limit forces R2 ≥ 20 kΩ; a gain of 10 sets R2 = 10·R1; R1 = 10 kΩ, R2 = 100 kΩ keeps Rin high. The exact nodal solution gives vO = 10 V and IO = 2.09 mA.', ['Design example: several resistor pairs are acceptable (the book chooses 10 kΩ and 100 kΩ).'], None, \
        cj('11.11', 'Fig. 11.39', 'inverting amplifier: input resistor R1 to the − input, feedback R2, load RL = 5 kΩ at the output, + input grounded.')
@solve('jaeger5', 'example', 11, '11.12')
def _():
    Ad, CMRR, V1, V2 = 2500.0, 10 ** (80 / 20), 5.001, 4.999; vid = V1 - V2; vic = (V1 + V2) / 2; VO = Ad * (vid + vic / CMRR)
    Acm = Ad / CMRR; close(VO, Ad * vid + Acm * vic, 1e-9)                                  # second route: separate differential and common-mode gains
    err = (VO - Ad * vid) / (Ad * vid); close(VO, 6.25, 1e-9); close(err, 0.25, 1e-9)
    must_in_book(J, '11.12', ['6.25 V', '25 percent'])
    return [('Differential and common-mode input voltages', f'VID = {g(vid, 4)} V, VIC = {g(vic, 4)} V'), ('Output vO = A(VID + VIC/CMRR), CMRR = 10⁴', f'{g(VO, 4)} V (the ideal value is {g(Ad * vid, 4)} V)'), ('Error from the common-mode input', f'{g(100 * err, 3)} % of the ideal output')], 'Eq. (11.110): vO = A_d·vid + A_cm·vic with A_cm = A_d/CMRR. The common-mode term 2500·5.000/10⁴ = 1.25 V is a 25 % error.', ['CMRR = +10⁴ (the sign of the CMRR is not specified, the book assumes +).'], None, \
        cj('11.12', 'Fig. 11.40', 'differential amplifier with inputs V1 and V2 and differential gain A = 2500 (finite common-mode rejection).')
def _inamp(v1, v2, R1, R2, R3, R4):
    c = Ckt(); c.V('s1', 'v1', '0', v1); c.V('s2', 'v2', '0', v2); c.opamp('v1', 'n1', 'a'); c.opamp('v2', 'n2', 'b'); c.R('a', 'n1', R2); c.R('n1', 'n2', 2 * R1); c.R('n2', 'b', R2)
    c.R('a', 'q', R3); c.R('q', 'o', R4); c.R('b', 'p', R3); c.R('p', '0', R4); c.opamp('p', 'q', 'o'); v, _ = dc(c); return v
@solve('jaeger5', 'example', 12, '12.5')
def _():
    V1, V2, R1, R2, R3, R4 = 2.5, 2.25, 15e3, 150e3, 15e3, 30e3; VO = -(R4 / R3) * (1 + R2 / R1) * (V1 - V2); I = (V1 - V2) / (2 * R1); VA = V1 + I * R2; VB = V2 - I * R2
    v = _inamp(V1, V2, R1, R2, R3, R4); close(v['o'], VO, 1e-8); close(v['a'], VA, 1e-8); close(v['b'], VB, 1e-8); close(VO, -(R4 / R3) * (VA - VB), 1e-9)
    must_in_book(J, '12.5', ['−5.50 V', '+3.75 V', '1.00 V', '8.33'])
    return [('VO = −(R4/R3)(1 + R2/R1)(V1 − V2)', f'{g(VO, 4)} V'), ('Current in 2R1: I = (V1 − V2)/2R1', si(I, 'A', 3)), ('VA = V1 + I·R2', f'{g(VA, 4)} V'), ('VB = V2 − I·R2', f'{g(VB, 4)} V')], 'Instrumentation amplifier (Eq. 12.13): the ideal op amps ① and ② put V1 and V2 on the ends of 2R1, so I = (V1 − V2)/2R1 and VA, VB are I·R2 above and below; the difference amplifier gives VO = −(R4/R3)(VA − VB). The exact nodal solution of the three-op-amp circuit agrees.', ['Ideal op amps.'], None, \
        cj('12.5', 'Fig. 12.4', 'instrumentation amplifier: V1 and V2 on the + inputs of op amps ① and ②; R2, 2R1, R2 in series between their outputs; op amp ③ with R3, R4 forms the difference amplifier; V1 = 2.5 V, V2 = 2.25 V, R1 = 15 kΩ, R2 = 150 kΩ, R3 = 15 kΩ, R4 = 30 kΩ.')
@solve('jaeger5', 'example', 12, '12.6')
def _():
    fo, C = 5e3, 0.01e-6; R = 1 / (math.sqrt(2) * 2 * math.pi * fo * C); Rs = 2260.0; C1, C2 = 0.02e-6, 0.01e-6
    f0 = 1 / (2 * math.pi * math.sqrt(Rs * Rs * C1 * C2)); Q = math.sqrt(C1 / C2) * Rs / (2 * Rs)
    c = Ckt(); c.V('vi', 'i', '0', 1.0); c.R('i', 'v1', Rs); c.R('v1', 'v2', Rs); c.C('v1', 'o', C1); c.C('v2', '0', C2); c.opamp('v2', 'o', 'o')
    h = lambda f: abs(c.solve(2j * math.pi * f)[0]['o']); close(h(f0), Q, 1e-6)
    from scipy.optimize import brentq
    fH = 10 ** brentq(lambda lf: h(10 ** lf) - 1 / math.sqrt(2) * h(1e-3), 2, 6, xtol=1e-12); close(fH, 4980, 5e-3)
    must_in_book(J, '12.6', ['2250 Ω', '2260 Ω', '4980 Hz', '0.707'])
    return [('R = 1/(√2·ωo·C) with C2 = C = 0.01 μF', si(R, 'Ω', 4)), ('Standard 1 % value and capacitors', 'R1 = R2 = 2.26 kΩ, C1 = 0.02 μF, C2 = 0.01 μF'), ('Check', f'fo = {si(f0, "Hz", 4)}, Q = {g(Q, 4)}; −3 dB frequency of the exact circuit {si(fH, "Hz", 4)}')], 'Maximally flat second-order low-pass filter (Q = 1/√2): C1 = 2C2 = 2C, R1 = R2 = R = 1/(√2·ωo·C); then fH = fo. The exact circuit (Fig. 12.5 with an ideal follower) solved at s = jω confirms |A(jωo)| = Q and fH ≈ fo = 4.98 kHz.', ['Ideal op amp (voltage follower).'], None, \
        cj('12.6', 'Fig. 12.5', 'two-pole low-pass filter: vI → R1 → v1 → R2 → v2 (+ input of a voltage follower); C1 from v1 to the output; C2 from v2 to ground.')
@solve('jaeger5', 'example', 12, '12.1')
def _():
    R = dict(R1=15e3, R2=150e3, R3=21e3, R4=420e3, R5=20e3, R6=100e3, R7=75e3)
    def circuit(vin, Vs=None, A=1e12):
        sat = {}
        for _ in range(4):
            c = Ckt(); c.V('vs', 'in', '0', vin); c.R('in', '0', R['R7'])
            c.R('m0', '0', R['R1']); c.R('o0', 'm0', R['R2'])
            c.R('o0', 'm1', R['R3']); c.R('o1', 'm1', R['R4'])
            c.R('m2', '0', R['R5']); c.R('o2', 'm2', R['R6'])
            for k, (plus, minus, out) in enumerate((('in', 'm0', 'o0'), ('0', 'm1', 'o1'), ('o1', 'm2', 'o2'))):
                if k in sat: c.V(f'sat{k}', out, '0', sat[k])
                else: c.E(f'E{k}', out, '0', plus, minus, A)
            v, i = c.solve(0.0); v = {a: b.real for a, b in v.items()}; i = {a: b.real for a, b in i.items()}
            new = {k: math.copysign(Vs, v[f'o{k}']) for k in range(3) if Vs and k not in sat and abs(v[f'o{k}']) > Vs}
            if not new: return v, i, set(sat)
            sat.update(new)
        return v, i, set(sat)
    v, i, _s = circuit(1.0); Av = v['o2']; Rin = 1.0 / (-i['vs']); close(Av, -1320, 1e-8); close(Rin, 75e3, 1e-8)
    Avf = (1 + R['R2'] / R['R1']) * (-R['R4'] / R['R3']) * (1 + R['R6'] / R['R5']); close(Avf, -1320, 1e-12)
    v5, _i, s5 = circuit(5e-3, 12.0); assert not s5; v10, _i, s10 = circuit(10e-3, 12.0); assert s10 == {2}
    close(v5['o0'], 55e-3, 1e-8); close(v5['o1'], -1.1, 1e-8); close(v5['o2'], -6.6, 1e-8); close(v10['m2'], -2.0, 1e-8); close(v10['o2'], -12.0, 1e-8); Vi = 12 / abs(Av); close(Vi, 9.09e-3, 1e-3)
    must_in_book(J, '12.1', ['−1320', '75 kΩ', '−6.60 V', '−2 V', '9.09 mV'], 7000)
    return [('(a) voltage gain', f'(1 + R2/R1)(−R4/R3)(1 + R6/R5) = {g(Av, 5)}'), ('(a) input resistance', f'{si(Rin, "Ω", 3)} (the 75 kΩ resistor; the + input of the first op amp is ideal)'), ('(a) output resistance', '0'),
            ('(b) vI = 5 mV', f'vOA = {si(v5["o0"], "V", 4)}, vOB = {si(v5["o1"], "V", 4)}, vO = {si(v5["o2"], "V", 4)}; v−A = 5.00 mV, v−B = 0, v−C = {si(v5["m2"], "V", 4)}'), ('(c) vI = 10 mV', f'vOA = {si(v10["o0"], "V", 4)}, vOB = {si(v10["o1"], "V", 4)}; the third output would be −13.2 V, so it saturates at {si(v10["o2"], "V", 3)} and v−C = {si(v10["m2"], "V", 3)}'), ('(d) largest linear amplitude', f'12 V/1320 = {si(Vi, "V", 3)}')], \
        'Three stages (noninverting, inverting, noninverting) with ±12-V supplies: gains multiply, Rin is the 75 kΩ shunt resistor, Rout = 0 (Eq. 12.2); nodes follow vOA = 11 vI, vOB = −20 vOA, vO = 6 vOB. When vO would exceed the rail, the output is clamped at −12 V, the loop of the third stage is open and v−C = −12·20/120 = −2 V. The exact nodal solution with the clamped output as a fixed source gives all the printed values.', ['The book counts 10 nodes (including V+, V− and ground), here the seven circuit nodes are given.', 'The output saturates at exactly the supply voltage.'], None, \
        'Three-stage amplifier of the worked example (p.%s; the figure has no number): noninverting stage (R1 = 15 kΩ to ground, R2 = 150 kΩ feedback; input tied to ground by R7 = 75 kΩ), inverting stage (R3 = 21 kΩ in, R4 = 420 kΩ feedback), noninverting stage (R5 = 20 kΩ to ground, R6 = 100 kΩ feedback); supplies ±12 V.' % pg('12.1')
