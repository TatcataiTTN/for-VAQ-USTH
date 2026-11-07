"""Jaeger 5e worked Examples (chapters 10-11) recomputed; each result is also looked for in the book's own printed solution."""
import math, cmath
import numpy as np
from core import *
J = 'jaeger'
@solve('jaeger5', 'example', 10, '10.3')
def _():
    A, Rid, Ro, RI, RL = 100, 100e3, 100.0, 10e3, 1000.0
    av = A * Rid / (RI + Rid) * RL / (Ro + RL)
    # independent route: source RI -> Rid gives vid; the controlled source A·vid behind Ro drives RL (node equation at the output)
    vid = (1 / RI) / (1 / RI + 1 / Rid); vo = (A * vid / Ro) / (1 / Ro + 1 / RL); close(vo, av, 1e-9); must_in_book(J, '10.3', ['82.6', '38.3 dB'])
    return [('Av = A·Rid/(RI + Rid)·RL/(Ro + RL)', g(av, 4)), ('In decibels', f'{g(db(av), 3)} dB')], 'Voltage gain of the differential amplifier model including the source resistance RI and the load RL (Jaeger Eq. 10.33).', []
@solve('jaeger5', 'example', 10, '10.4')
def _():
    Av = 10 ** (40 / 20); R1 = 20e3; R2 = Av * R1
    A = 1e7; M = np.array([[1 / R1 + 1 / R2, -1 / R2], [A, 1.0]]); v1, vo = np.linalg.solve(M, [1 / R1, 0.0]); close(vo, -100, 1e-4); must_in_book(J, '10.4', ['2 MΩ', 'R1 = Rin = 20 kΩ'])
    return [('R1 = Rin', '20 kΩ'), ('R2 = |Av|·R1 (|Av| = 10^(40/20) = 100)', '2 MΩ'), ('Gain', '−100 (40 dB)')], 'Ideal inverting amplifier: Rin = R1, Av = −R2/R1.', ['Ideal op amp.']
@solve('jaeger5', 'example', 10, '10.10')
def _():
    num, den = [50, 0, 200], [1, 2, 2]; res = []
    for w in (0, 3):
        s = 1j * w; h = np.polyval(num, s) / np.polyval(den, s); res.append((abs(h), math.degrees(cmath.phase(h))))
    close(res[0][0], 100, 1e-9); close(res[1][0], 250 / math.sqrt(85), 1e-9); close(res[1][1], 40.6, 2e-3); must_in_book(J, '10.10', ['40.0 dB', '27.1', '28.7 dB'])
    return [('ω = 0', f'|Av| = {g(res[0][0])} ({g(db(res[0][0]), 3)} dB), phase {g(res[0][1], 3)}°'), ('ω = 3 rad/s', f'|Av| = {g(res[1][0], 3)} ({g(db(res[1][0]), 3)} dB), phase {g(res[1][1], 3)}°')], 'Substitute s = jω and take magnitude and phase of the complex number.', [], 'Transfer function of the example: Av(s) = 50(s² + 4)/(s² + 2s + 2).'
@solve('jaeger5', 'example', 10, '10.11')
def _():
    R1 = 5e3; Av = 100; R2 = Av * R1; fH = 2e3; C = 1 / (2 * math.pi * fH * R2)
    H = lambda f, R2, C: -(R2 / R1) / (1 + 1j * 2 * math.pi * f * R2 * C)
    close(abs(H(fH, R2, C)), Av / math.sqrt(2), 1e-9)                                    # −3 dB at fH, independent check on the circuit transfer function
    R2s, Cs = 510e3, 160e-12; fH2 = 1 / (2 * math.pi * R2s * Cs); close(fH2 / 1e3, 1.95, 5e-3); must_in_book(J, '10.11', ['159 pF', '5.1 kΩ', '510 kΩ', '160 pF'])
    return [('R1 = Rin', '5 kΩ'), ('R2 = |Av|·R1 (|Av| = 100 for 40 dB)', '500 kΩ'), ('C = 1/(2π·fH·R2)', f'{g(C * 1e12, 3)} pF'), ('With standard values R1 = 5.1 kΩ, R2 = 510 kΩ, C = 160 pF', f'fH = {g(fH2 / 1e3, 3)} kHz')], 'Active low-pass filter: inverting amplifier with C in parallel with R2; Rin = R1, |Av| = R2/R1, fH = 1/(2π·R2·C).', ['Standard values are the nearest of the Appendix A tables, as in the book.']
@solve('jaeger5', 'example', 11, '11.1')
def _():
    A, beta = 1e4, 1 / 200; T = A * beta; av = 200 * T / (1 + T); fge = 1 / (1 + T)
    close(A / (1 + T), av, 1e-9); must_in_book(J, '11.1', ['196', '0.02'])
    return [('Ideal gain', '200 (46 dB)'), ('T = A·β', g(T)), ('Actual gain = Aideal·T/(1 + T)', g(av, 4)), ('Fractional gain error = 1/(1 + T)', f'{g(100 * fge, 3)} % (the book rounds to 2 %)')], 'Finite open-loop gain: Av = Aideal·T/(1 + T), FGE = 1/(1 + T) (Jaeger §11.2).', ['The op amp is ideal except for its finite open-loop gain A = 10,000 (80 dB).']
@solve('jaeger5', 'example', 11, '11.2')
def _():
    A, R1, R2, Ro = 1e4, 1e3, 39e3, 50.0; T = A * R1 / (R1 + R2); rout = (Ro / (1 + T)) * (R1 + R2) / (Ro / (1 + T) + R1 + R2)
    close(1 + T, 251, 1e-9); close(rout, 50 / 251, 1e-3); must_in_book(J, '11.2', ['251', '0.199 Ω'])
    return [('1 + T = 1 + A·R1/(R1 + R2)', g(1 + T, 4)), ('Rout = [Ro/(1 + T)] ‖ (R1 + R2)', f'{g(rout, 3)} Ω')], 'Output resistance of the noninverting amplifier (Jaeger Eq. 11.25).', ['The op amp is ideal except for finite A and nonzero Ro.', 'The book prints 0.198 Ω after “0.199 Ω ‖ 40 kΩ”; 50/251 = 0.1992 and the 40 kΩ in parallel changes nothing visible, so 0.199 Ω is the value (the book\'s last digit is a small arithmetic slip).']
@solve('jaeger5', 'example', 11, '11.3')
def _():
    beta = 1 / 10 ** (35 / 20); A = (1 / beta) * (250 / 0.2 - 1); close(1 + A * beta, 250 / 0.2, 1e-9); must_in_book(J, '11.3', ['96.9 dB'])
    return [('β = 1/|Av| = 10^(−35/20)', g(beta, 4)), ('A ≥ (1/β)(Ro/Rout − 1)', f'{g(A, 3)} ({g(db(A), 3)} dB)')], 'Rout = Ro/(1 + Aβ) ≤ 0.2 Ω (Jaeger Eq. 11.26).', ['The book rounds A to 7.03 × 10⁴ using 56.2; the exact value is 7.02 × 10⁴.']
@solve('jaeger5', 'example', 11, '11.13')
def _():
    A, cm = 1e4, 10 ** (60 / 20); ge = 1 / A - 1 / cm
    av = A * (1 + 1 / (2 * cm)) / (1 + A * (1 - 1 / (2 * cm)))                                        # exact gain of the follower with finite A and CMRR
    # independent: solve vo = A·(vi − vo) + (A/CMRR)·(vi + vo)/2 directly
    vo = np.linalg.solve([[1 + A - A / (2 * cm)]], [A + A / (2 * cm)])[0]; close(vo, av, 1e-12); close(1 - av, ge, 5e-2); must_in_book(J, '11.13', ['0.090 percent', '1.001'])
    return [('Gain error ≈ 1/A − 1/CMRR', f'{g(ge)} = {g(100 * ge, 3)} %'), ('Av', g(av, 4))], 'Voltage-follower gain error with finite gain and finite CMRR (Jaeger Eq. 12.38).', ['CMRR = 60 dB = 1000.']
@solve('jaeger5', 'example', 11, '11.15')
def _():
    Ao, fT = 1e5, 1e7; fB = fT / Ao; beta = 1 / 1000; fH = fB * (1 + Ao * beta); close(fH, 10.1e3, 1e-9); must_in_book(J, '11.15', ['100 Hz', '10.1 kHz'])
    return [('(a) Op-amp bandwidth fB = fT/Ao', f'{g(fB)} Hz'), ('(b) fH = fB(1 + Ao·β), β = 1/1000', f'{g(fH / 1e3, 3)} kHz'), ('(c) Op-amp transfer function', 'Av(s) = 2π×10⁷/(s + 200π)'), ('(d) Noninverting amplifier', f'Av(s) = 2π×10⁷/(s + {g(2 * math.pi * fB * (1 + Ao * beta) / math.pi / 1e4, 3)}π×10⁴)')], 'Single-pole op amp: Av(s) = Ao·ωB/(s + ωB) with ωB = 2π·fT/Ao; closed loop: pole moves to ωB(1 + Ao·β).', []
@solve('jaeger5', 'example', 11, '11.16')
def _():
    Ao, fT = 2e5, 5e5; fB = fT / Ao; beta = 1 / 101; fH = fB * (1 + Ao * beta); close(fH, 4.95e3, 1e-3); must_in_book(J, '11.16', ['2.5 Hz', '4.95 kHz'])
    num = 100 * Ao * beta * 2 * math.pi * fB; pole = 2 * math.pi * fB * (1 + Ao * beta)
    return [('(a) Op-amp cutoff fB = fT/Ao', f'{g(fB)} Hz'), ('(b) fH = fB(1 + Ao·β), β = 1/(1 + |Av|) = 1/101', f'{g(fH / 1e3, 3)} kHz'), ('(c) Op-amp transfer function', 'Av(s) = 10⁶π/(s + 5π)'), ('(d) Inverting amplifier', f'Av(s) = −{g(num / math.pi / 1e5, 3)}×10⁵π/(s + {g(pole / math.pi / 1e3, 4)}π×10³)')], 'Inverting amplifier: Av(s) = −(R2/R1)·Aoβ·ωB/(s + ωB(1 + Aoβ)), with the feedback factor β = 1/(1 + |Av|).', ['Closed-loop gain 40 dB means |Av(0)| = 100.']
