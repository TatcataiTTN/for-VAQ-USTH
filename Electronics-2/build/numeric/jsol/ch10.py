"""Jaeger 5e chapter 10 (ideal op amps, amplifier models, transfer functions).  Standard 1 % values: the E96 series (Appendix A)."""
import math, cmath
import numpy as np
from core import *
E96 = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976]
E12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
def near(x, series, base=100):
    """nearest value (log scale) of a standard series whose mantissas are listed as integers in [base, 10*base)"""
    dec = math.floor(math.log10(x)); scale = 10 ** dec / base * 1.0 if base == 10 else 10 ** (dec - 2)
    m = x / scale; cands = [v for v in series] + [10 * base]; cands = [c for c in cands]
    best = min(cands + [series[0] / 10 * 10], key=lambda c: abs(math.log(c / m)))
    return best * scale
def e96(x): return near(x, E96, 100)
def e12(x): return near(x, E12, 10)
for _x, _y in ((15e3, 15e3), (376.8e3, 374e3), (446.7e3, 442e3), (13.13e3, 13.0e3)): close(e96(_x), _y, 1e-9)       # self-test of the picker
close(e12(79.6e-12), 82e-12, 1e-9)
def db(x): return 20 * math.log10(abs(x))
def thd(amps): return math.sqrt(sum(a * a for a in amps[1:])) / amps[0]
def harmonics(f, f0=1000.0, n=5, N=4096):
    t = np.arange(N) / (N * f0) * 1.0; v = f(t); sp = np.fft.rfft(v) / N * 2; return [abs(sp[k]) for k in range(1, n + 1)], abs(np.fft.rfft(v)[0]) / N

@solve('10.33')
def _():
    a, dc = harmonics(lambda t: 2 + 4 * np.sin(1200 * np.pi * t) + 0.8 * np.sin(2400 * np.pi * t) + 0.4 * np.sin(3600 * np.pi * t), 600.0, 4)
    close(a[0], 4, 1e-6); close(a[1], 0.8, 1e-6); close(a[2], 0.4, 1e-6); t = thd(a)
    return [('Voltage gain (ac fundamental)', f'{g(4 / 0.25)} V/V ({g(db(16))} dB)'), ('Harmonics present', '2nd (1200 Hz) and 3rd (1800 Hz) harmonics; fundamental 600 Hz'), ('THD = √(V2² + V3²)/V1', f'{g(100 * thd([4, .8, .4]))} %')], 'Gain = amplitude of the 600 Hz output component / input amplitude (the dc terms are not part of the gain). THD checked with an FFT of the waveform.', []
@solve('10.34')
def _():
    a, dc = harmonics(lambda t: 5 * np.sin(2000 * np.pi * t) + .5 * np.sin(6000 * np.pi * t) + .2 * np.sin(10000 * np.pi * t), 1000.0, 5)
    close(a[0], 5, 1e-6); close(a[2], .5, 1e-6); close(a[4], .2, 1e-6)
    return [('Voltage gain', f'{g(5 / 0.004)} V/V ({g(db(1250))} dB)'), ('Harmonics present', '3rd (3 kHz) and 5th (5 kHz); only odd harmonics'), ('THD', f'{g(100 * thd([5, .5, .2]))} %')], 'Gain = 5 V/4 mV at 1 kHz; THD = √(0.5² + 0.2²)/5 checked with an FFT.', []
@solve('10.37')
def _():
    N = 8192; t = np.arange(N) / (N * 1000.0); v = 10 * np.tanh(2 * 0.75 * np.sin(2 * np.pi * 1000 * t)); sp = np.fft.rfft(v) / N * 2
    c = [abs(sp[k]) for k in range(1, 4)]
    # independent check: the same coefficients by numerical integration of the Fourier integral
    th = (np.arange(N) + .5) / N * 2 * np.pi; y = 10 * np.tanh(1.5 * np.sin(th)); b = [2 / N * np.sum(y * np.sin(k * th)) for k in range(1, 4)]
    for k in range(3): close(c[k], abs(b[k]), 1e-6, 1e-9)
    return [('Fourier amplitudes V1, V2, V3', f'{g(c[0])} V, {g(c[1] if c[1] > 1e-9 else 0)} V, {g(c[2])} V'), ('Distortion from the first three components', f'{g(100 * math.sqrt(c[1] ** 2 + c[2] ** 2) / c[0])} % (the VTC is odd, so the 2nd harmonic is zero)')], 'Fourier components of 10·tanh(1.5·sin ωt) found with an FFT and by direct integration; THD = √(V2² + V3²)/V1. The plot of part (a) is not reproduced.', []
@solve('10.40')
def _(): return [('Maximum output resistance', si(50 * 2 / 100, 'Ω'))], 'The same current flows in RL and Rout: P ∝ R, so Rout/RL ≤ 2 W/100 W.', []
@solve('10.41')
def _(): r = 0.99 / 0.01 * 50e3; close(1e-3 * r / (r + 50e3), 0.99e-3); return [('Minimum input resistance', si(r, 'Ω'))], 'vid = 1 mV·Rin/(Rin + 50 kΩ) ≥ 0.99 mV.', []
@solve('10.42')
def _():
    A = 10 ** 6; vid = 15 / A; return [('vid', si(vid, 'V')), ('Gain needed for vid ≤ 1 μV', f'A ≥ {g(15 / 1e-6)} ({g(db(15 / 1e-6))} dB)'), ('i+ = vid/Rid', si(vid / 1e6, 'A'))], 'vid = vo/A; A = 120 dB = 10⁶.', []
@solve('10.43')
def _(): A = 10 ** (106 / 20); return [('A', g(A)), ('vid', si(10 / A, 'V')), ('Gain needed for vid ≤ 1 μV', f'A ≥ {g(10 / 1e-6)} ({g(db(10 / 1e-6))} dB)')], 'vid = vo/A with A = 10^(106/20).', []
def design_inv(rin, gdb):
    a = 10 ** (gdb / 20); r1 = e96(rin); r2 = e96(a * r1); gain = r2 / r1; return a, r1, r2, gain
@solve('10.53')
def _():
    a, r1, r2, gn = design_inv(15e3, 28); return [('Ideal R2 for R1 = 15 kΩ', si(a * 15e3, 'Ω')), ('Standard 1 % values', f'R1 = {si(r1, "Ω")}, R2 = {si(r2, "Ω")}'), ('Resulting gain', f'{g(gn)} ({g(db(gn))} dB)')], '|Av| = R2/R1 with Rin = R1; R2 taken from the nearest value of the E96 table.', ['Appendix A 1 % table taken as the E96 series.']
@solve('10.54')
def _():
    a, r1, r2, gn = design_inv(2e3, 40); return [('Ideal R2', si(a * 2e3, 'Ω')), ('Standard 1 % values', f'R1 = {si(r1, "Ω")}, R2 = {si(r2, "Ω")}'), ('Resulting gain', f'{g(gn)} ({g(db(gn))} dB)')], 'As Problem 10.53.', ['E96 series.']
@solve('10.55')
def _():
    a, r1, r2, gn = design_inv(100e3, 13); return [('Ideal R2', si(a * 100e3, 'Ω')), ('Standard 1 % values', f'R1 = {si(r1, "Ω")}, R2 = {si(r2, "Ω")}'), ('Resulting gain', f'{g(gn)} ({g(db(gn))} dB)')], 'As Problem 10.53.', ['E96 series.']
@solve('10.59')
def _(): return [('R', si(5 / 2.5e-6, 'Ω'))], 'Transresistance amplifier (virtual ground): vO = −iS·R, so R = 5 V/2.5 μA; the 100 kΩ source resistance does not matter.', []
def design_ni(gdb, r1):
    a = 10 ** (gdb / 20); r2 = e96((a - 1) * r1); return a, r2, 1 + r2 / r1
@solve('10.65')
def _():
    a, r2, gn = design_ni(23, 10e3); return [('Ideal R2/R1', g(a - 1)), ('Choice (R1 = 10 kΩ ≥ 2 kΩ)', f'R1 = 10.0 kΩ, R2 = {si(r2, "Ω")}'), ('Resulting gain', f'{g(gn)} ({g(db(gn))} dB)')], 'Av = 1 + R2/R1; R2 from the E96 table.', ['R1 = 10 kΩ chosen; other pairs also work.']
@solve('10.66')
def _():
    a, r2, gn = design_ni(6, 10e3); return [('Input resistance', 'R3 = 100 kΩ from the + input to ground'), ('Gain network', f'R1 = 10.0 kΩ, R2 = {si(r2, "Ω")}'), ('Resulting gain', f'{g(gn)} ({g(db(gn))} dB)')], 'The ideal noninverting amplifier has infinite input resistance, so the 100 kΩ is set by a resistor R3 to ground at the input; Av = 1 + R2/R1.', ['R1 = 10 kΩ chosen.']
@solve('10.67')
def _():
    a, r2, gn = design_ni(46, 1e3); return [('Ideal R2/R1', g(a - 1)), ('Choice (R1 = 1.00 kΩ)', f'R1 = 1.00 kΩ, R2 = {si(r2, "Ω")}'), ('Resulting gain', f'{g(gn)} ({g(db(gn))} dB)')], 'Av = 1 + R2/R1; R2 from the E96 table.', ['R1 = 1 kΩ chosen.']
def tf(num, den): return lambda w: np.polyval(num, 1j * w) / np.polyval(den, 1j * w)
def fz(num, den): return [r / (2 * math.pi) for r in np.roots(num)], [r / (2 * math.pi) for r in np.roots(den)]
@solve('10.75')
def _():
    num_a = [-3e9, 0, 0]; den_a = np.polymul([1, 51, 50], [1, 13000, 3e7]); num_b = [-1e5, -51e5, -50e5]; den_b = [1, 1000, 50000, 20000, 13000, 3e7]
    za, pa = np.roots(num_a), np.roots(den_a); zb, pb = np.roots(num_b), np.roots(den_b)
    # check: rebuild the denominators from the roots
    close(np.poly(pa)[2], den_a[2], 1e-6); close(abs(np.poly(pb)[5]), den_b[5], 1e-6)
    fmt = lambda r: ', '.join(g(float(np.real(x))) if abs(np.imag(x)) < 1e-6 * max(1, abs(x)) else f'{g(float(np.real(x)))} {"+" if np.imag(x) > 0 else "−"} j{g(abs(float(np.imag(x))))}' for x in sorted(r, key=lambda z: (abs(z), -z.imag)))
    return [('(a) zeros (rad/s)', 'double zero at s = 0'), ('(a) poles (rad/s)', fmt(pa)), ('(b) zeros (rad/s)', fmt(zb)), ('(b) poles (rad/s)', fmt(pb))], '(a): s² + 51s + 50 = (s + 1)(s + 50) and s² + 13000s + 3×10⁷ = (s + 3000)(s + 10000); (b): numerator (s + 1)(s + 50), denominator roots found numerically (rebuilt to check).', ['Part (b): Av(s) = −10⁵(s² + 51s + 50)/(s⁵ + 10³s⁴ + 5×10⁴s³ + 2×10⁴s² + 1.3×10⁴s + 3×10⁷), as printed; its denominator has a complex pair in the right half-plane (unstable), which is what the printed coefficients give.']

TF = {
 '10.76': ([2 * math.pi * 1e7, 0], np.polymul([1, 20 * math.pi], [1, 2 * math.pi * 1e4]), 'band-pass'),
 '10.77': ([2 * math.pi * 1e6], [1, 200 * math.pi], 'low-pass'),
 '10.78': ([1e4, 0], [1, 200 * math.pi], 'high-pass'),
 '10.79': ([-5e6, 0], [1, 1e5, 1e14], 'band-pass (second order)'),
 '10.80': ([-20, 0, -20e12], [1, 1e4, 1e12], 'band-reject (notch)'),
 '10.81': ([4 * math.pi ** 2 * 1e14, 0, 0], np.polymul(np.polymul([1, 20 * math.pi], [1, 50 * math.pi]), np.polymul([1, 2 * math.pi * 1e5], [1, 2 * math.pi * 1e6])), 'band-pass'),
}
from scipy.optimize import brentq
def cutoffs(num, den, kind, amid):
    """-3 dB frequencies: sign changes of |H| − |amid|/√2 on a log grid, each refined with brentq between the two neighbouring grid points"""
    H = tf(num, den); lim = abs(amid) / math.sqrt(2); f = np.logspace(-2, 9, 400001); d = np.abs(H(2 * np.pi * f)) - lim
    ch = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    root = lambda i: brentq(lambda x: abs(H(2 * np.pi * x)) - lim, f[i], f[i + 1], xtol=1e-12 * f[i])
    if kind == 'low-pass': return 0.0, root(ch[-1])
    if kind == 'high-pass': return root(ch[0]), float('inf')
    return root(ch[0]), root(ch[-1])
AMID = {'10.76': 1000.0, '10.77': 1e4, '10.78': 1e4, '10.79': 50.0, '10.80': 20.0, '10.81': 1000.0}      # closed-form midband (or notch-free) gains
def tf_report(num_key):
    num, den, kind = TF[num_key]; H = tf(num, den); amid = AMID[num_key]
    f = np.logspace(-2, 9, 200001); a = np.abs(H(2 * np.pi * f))
    close(float(np.max(a)) if 'pass' in kind and kind != 'low-pass' and kind != 'high-pass' else (a[0] if kind in ('low-pass', 'band-reject (notch)') else a[-1]), amid, 5e-3)   # numeric plateau/peak agrees with the closed form
    fl, fh = cutoffs(num, den, kind, amid); return kind, amid, fl, fh
@solve('10.76')
def _():
    kind, amid, fl, fh = tf_report('10.76'); close(amid, 1000, 2e-3)           # analytic: 2π·10⁷/(2π·10⁴)
    return [('Amid', f'{g(db(amid))} dB ({g(amid)})'), ('fL, fH', f'{g(fl)} Hz, {g(fh)} Hz (poles at 10 Hz and 10 kHz)'), ('BW', f'{g(fh - fl)} Hz'), ('Type', kind)], 'Midband: s ≫ 20π, s ≪ 2π×10⁴: Av = 2π×10⁷/(2π×10⁴) = 10³. The −3 dB frequencies are found by a numerical sweep and agree with the pole frequencies.', []
@solve('10.77')
def _():
    kind, amid, fl, fh = tf_report('10.77'); close(amid, 1e4, 1e-3); close(fh, 100, 2e-3)
    return [('Amid', f'{g(db(amid))} dB ({g(amid)})'), ('fH', f'{g(fh)} Hz'), ('fL', '0 (dc gain is the mid-band gain)'), ('BW', f'{g(fh)} Hz'), ('Type', kind)], 'Av(0) = 2π×10⁶/200π = 10⁴; single pole at 200π rad/s = 100 Hz.', []
@solve('10.78')
def _():
    kind, amid, fl, fh = tf_report('10.78'); close(amid, 1e4, 1e-3); close(fl, 100, 2e-3)
    return [('Amid', f'{g(db(amid))} dB ({g(amid)})'), ('fL', f'{g(fl)} Hz'), ('fH', '∞ (ideal single-pole high-pass)'), ('BW', '∞'), ('Type', kind)], 'For s ≫ 200π the gain is 10⁴; zero at the origin and pole at 200π rad/s = 100 Hz (Eq. 10.78).', []
@solve('10.79')
def _():
    kind, amid, fl, fh = tf_report('10.79'); f0 = 1e7 / (2 * math.pi); q = 1e7 / 1e5; close(amid, 50, 1e-3); close(math.sqrt(fl * fh), f0, 1e-4)
    return [('Amid (at f0)', f'{g(db(amid))} dB ({g(amid)})'), ('f0, Q', f'{si(f0, "Hz")}, {g(q)}'), ('fL, fH', f'{si(fl, "Hz")}, {si(fh, "Hz")}'), ('BW = f0/Q', si(fh - fl, 'Hz')), ('Type', kind)], 'ω0 = √10¹⁴ = 10⁷ rad/s, ω0/Q = 10⁵ rad/s so Q = 100; at ω0 |Av| = 5×10⁶/10⁵ = 50. Cutoffs by a numerical sweep; fL·fH = f0².', []
@solve('10.80')
def _():
    kind, amid, fl, fh = tf_report('10.80'); f0 = 1e6 / (2 * math.pi); close(amid, 20, 1e-3); close(math.sqrt(fl * fh), f0, 1e-4)
    return [('Amid (gain away from the notch)', f'{g(db(amid))} dB ({g(amid)})'), ('Notch frequency, Q', f'{si(f0, "Hz")} (ω0 = 10⁶ rad/s), Q = {g(1e6 / 1e4)}'), ('fL, fH (−3 dB edges of the notch)', f'{si(fl, "Hz")}, {si(fh, "Hz")}'), ('BW of the rejected band', si(fh - fl, 'Hz')), ('Type', kind)], 'Numerator zeros on the jω axis at ω = 10⁶ rad/s (gain 0); far from it Av → −20. Edges found numerically; BW = ω0/(2πQ) = 1.59 kHz.', []
@solve('10.81')
def _():
    kind, amid, fl, fh = tf_report('10.81'); close(amid, 1000, 5e-3)
    return [('Amid', f'{g(db(amid))} dB ({g(amid)})'), ('fL, fH (−3 dB)', f'{g(fl)} Hz, {si(fh, "Hz")}'), ('BW', si(fh - fl, 'Hz')), ('Type', kind), ('Poles', '10 Hz, 25 Hz, 100 kHz, 1 MHz; double zero at 0')], 'Between 25 Hz and 100 kHz: Av ≈ 4π²×10¹⁴/(4π²×10¹¹) = 10³. The two low poles are close, so the exact lower −3 dB point (numerical) lies a little above 25 Hz.', []
def at_freq(key, vi_amp, unit, freqs):
    num, den, kind = TF[key]; H = tf(num, den); out = []
    zs, ps = np.roots(num), np.roots(den); k = num[0] / den[0]
    for f in freqs:
        w = 2 * math.pi * f; h = H(w); s = 1j * w
        h2 = k * np.prod([s - z for z in zs]) / np.prod([s - p for p in ps]) if len(zs) else k / np.prod([s - p for p in ps])
        close(abs(h), abs(h2), 1e-6); mag = abs(h); ph = math.degrees(cmath.phase(h))
        out.append((f'f = {si(f, "Hz")}', f'|Av| = {g(mag)}, phase {g(ph)}°: vo = {g(mag * vi_amp)} {unit} · sin(ωt {"+" if ph >= 0 else "−"} {g(abs(ph))}°)'))
    return out
@solve('10.85')
def _(): return at_freq('10.76', 2e-3, 'V', (5, 500, 5e4)), 'Evaluate Av(jω) of Problem 10.76 (complex arithmetic; checked against the pole-zero product form).', []
@solve('10.86')
def _(): return at_freq('10.78', 0.3, 'mV', (1, 50, 5e3)), 'Evaluate Av(jω) of Problem 10.78.', []
@solve('10.87')
def _(): return at_freq('10.77', 10, 'μV', (2, 2e3, 2e5)), 'Evaluate Av(jω) of Problem 10.77.', []
@solve('10.88')
def _(): return at_freq('10.79', 4e-3, 'V', (1.59e6, 1e6, 5e6)), 'Evaluate Av(jω) of Problem 10.79.', []
@solve('10.89')
def _(): return at_freq('10.80', 0.25, 'V', (159e3, 50e3, 200e3)), 'Evaluate Av(jω) of Problem 10.80.', []
@solve('10.90')
def _(): return at_freq('10.81', 2e-3, 'V', (5, 500, 5e4)), 'Evaluate Av(jω) of Problem 10.81.', []
@solve('10.91')
def _():
    A = 10 ** (26 / 20); wH = 2 * math.pi * 5e6; k = A * wH
    return [('(a) Av(s) = A0·ωH/(s + ωH)', f'A0 = {g(A)} (26 dB), ωH = {g(wH)} rad/s: Av(s) = {g(k)}/(s + {g(wH)})'), ('(b) with 180° at f = 0', f'Av(s) = −{g(k)}/(s + {g(wH)})')], 'Single-pole low-pass amplifier, Eq. (10.66).', []
@solve('10.92')
def _():
    A = 100; wl = 2 * math.pi * 400; wh = 2 * math.pi * 1e5; k = A * wh
    return [('(a) Av(s) = A0·ωH·s/[(s + ωL)(s + ωH)]', f'A0 = 100 (40 dB), ωL = {g(wl)}, ωH = {g(wh)} rad/s: Av(s) = {g(k)}·s/[(s + {g(wl)})(s + {g(wh)})]'), ('(b) with 180° at f = 0', 'the same with a minus sign in front')], 'Band-pass amplifier = high-pass × low-pass; midband gain A0 requires ωH ≫ ωL.', []
@solve('10.94')
def _():
    k = 10 ** (10 / 20)
    return [('(a) phase shifts needed', 'linear in frequency: 10° at 500 Hz, 30° at 1500 Hz, 50° at 2500 Hz (each frequency delayed by the same time 55.6 μs)'), ('Output', f'vo(t) = {g(k)}·[sin(1000πt − 10°) + 0.333 sin(3000πt − 30°) + 0.2 sin(5000πt − 50°)] V = {g(k)}·[sin 1000π(t − 55.6 μs) + 0.333 sin 3000π(t − 55.6 μs) + 0.2 sin 5000π(t − 55.6 μs)] V')], 'No waveform distortion needs equal gain and a time delay td constant: phase = −ω·td. At 500 Hz 10° = 360°·500·td gives td = 55.6 μs.', ['The phase shifts are taken as lags (delays).']
def lp(r1, r2, c): return r2 / (r1 + r2), 1 / (2 * math.pi * (r1 * r2 / (r1 + r2)) * c)
@solve('10.95')
def _(): a, f = lp(10e3, 100e3, 0.01e-6); return [('Midband gain', f'{g(db(a))} dB ({g(a)})'), ('Upper cutoff fH', si(f, 'Hz'))], 'Ex. 10.8: Av = [R2/(R1+R2)]/(1 + s/ωH), ωH = 1/[(R1‖R2)C].', []
@solve('10.96')
def _(): a, f = lp(1e3, 1.5e3, 0.02e-6); return [('Midband gain', f'{g(db(a))} dB ({g(a)})'), ('Upper cutoff fH', si(f, 'Hz'))], 'Same formulas as Problem 10.95.', []
@solve('10.97')
def _():
    ratio = 10 ** (-0.5 / 20); r1 = 620.0; r2min = ratio * r1 / (1 - ratio); r2 = r2min; c = 1 / (2 * math.pi * (r1 * r2 / (r1 + r2)) * 20e3)
    r2s = 11e3; cs = 1 / (2 * math.pi * (r1 * r2s / (r1 + r2s)) * 20e3); a, f = lp(r1, r2s, 13e-9); close(db(r2s / (r1 + r2s)), -0.4, 0.3, 0.3)
    return [('(a) R2 for loss ≤ 0.5 dB', f'R2/(R1 + R2) ≥ {g(ratio)} → R2 ≥ {si(r2min, "Ω")}'), ('(a) C for fH = 20 kHz (R2 = that minimum)', si(c, 'F')), ('(b) standard values', f'R1 = 620 Ω, R2 = 11 kΩ → loss {g(-db(r2s / (r1 + r2s)))} dB, C = {si(cs, "F")} → 13 nF gives fH = {si(f, "Hz")}')], 'Loss at low frequency = −20·log₁₀[R2/(R1+R2)] ≤ 0.5 dB gives R2 ≥ 16.9·R1; then C = 1/[2π(R1‖R2)fH].', ['Standard values from the 5 % series (620 Ω and 11 kΩ).']
@solve('10.99')
def _():
    r1 = 10e3; r2 = r1 * 10 ** (20 / 20); c = 1 / (2 * math.pi * r2 * 20e3); cs = 82e-12; f = 1 / (2 * math.pi * 100e3 * cs)
    return [('(a) R1, R2, C', f'R1 = {si(r1, "Ω")}, R2 = {si(r2, "Ω")}, C = {si(c, "F")}'), ('(b) standard values', f'R1 = 10.0 kΩ, R2 = 100 kΩ, C = 82 pF → fH = {si(f, "Hz")}')], 'Active low-pass amplifier (inverting, C across R2): Av = −(R2/R1)/(1 + sR2C); Rin = R1, |Av| = 10, fH = 1/(2πR2C).', ['Circuit: inverting amplifier with C in parallel with R2 (Section 10.10.2/10.10.5).']
def hp(r1, r2, c): return r2 / (r1 + r2), 1 / (2 * math.pi * (r1 + r2) * c)
@solve('10.101')
def _(): a, f = hp(10e3, 82e3, 0.01e-6); return [('Midband gain', f'{g(db(a))} dB ({g(a)})'), ('Cutoff frequency (the high-pass has a LOWER cutoff fL; fH is infinite)', si(f, 'Hz'))], 'Ex. 10.9: Av = [R2/(R1+R2)]·s/(s + ωL), ωL = 1/[(R1 + R2)C]. (The statement says "upper" but only the lower cutoff exists.)', []
@solve('10.102')
def _(): a, f = hp(8.2e3, 20e3, 0.02e-6); return [('Midband gain', f'{g(db(a))} dB ({g(a)})'), ('Cutoff frequency (lower cutoff fL)', si(f, 'Hz'))], 'Same formulas as Problem 10.101.', []
@solve('10.103')
def _():
    ratio = 10 ** (-0.5 / 20); r1 = 390.0; r2 = ratio * r1 / (1 - ratio); c = 1 / (2 * math.pi * (r1 + r2) * 20e3); r2s = 6.8e3; cs = 1 / (2 * math.pi * (r1 + r2s) * 20e3)
    return [('(a) R2 for loss ≤ 0.5 dB at high frequency', f'R2 ≥ {si(r2, "Ω")}'), ('(a) C for fL = 20 kHz', si(c, 'F')), ('(b) standard values', f'R1 = 390 Ω, R2 = 6.8 kΩ → loss {g(-db(r2s / (r1 + r2s)))} dB, C = {si(cs, "F")} → use 1.1 nF (fL = {si(1 / (2 * math.pi * (r1 + r2s) * 1.1e-9), "Hz")})')], 'Loss = −20·log₁₀[R2/(R1+R2)] ≤ 0.5 dB gives R2 ≥ 16.9·R1; C = 1/[2π(R1 + R2)fL].', ['Standard values from the 5 % series.']
@solve('10.105')
def _():
    r1 = 20e3; r2 = 10 * r1; c = 1 / (2 * math.pi * r1 * 1e3); cs = 8.2e-9
    return [('(a) R1, R2, C', f'R1 = {si(r1, "Ω")}, R2 = {si(r2, "Ω")}, C = {si(c, "F")}'), ('(b) standard values', f'R1 = 20.0 kΩ, R2 = 200 kΩ, C = 8.2 nF → fL = {si(1 / (2 * math.pi * r1 * cs), "Hz")}')], 'Active high-pass amplifier (inverting, C in series with R1): Rin(high f) = R1, |Av| = R2/R1 = 10, fL = 1/(2πR1C) (same form as Example 10.10).', []

# ---- problems that use Figure P10.44 (ideal inverting amplifier: Av = −R2/R1, Rin = R1, Rout = 0)
def inv_set(pairs):
    out = []
    for tag, r1, r2 in pairs:
        av = -r2 / r1; out.append((tag, f'Av = {g(av)} ({g(db(av))} dB), Rin = {si(r1, "Ω")}, Rout = 0 (ideal op amp)'))
    return out
@solve('10.44')
def _(): return inv_set((('(a) R1 = 12 kΩ, R2 = 120 kΩ', 12e3, 120e3), ('(b) R1 = 160 kΩ, R2 = 330 kΩ', 160e3, 330e3), ('(c) R1 = 4.3 kΩ, R2 = 270 kΩ', 4.3e3, 270e3))), 'Figure P10.44 is the inverting amplifier: Av = −R2/R1, Rin = R1, Rout = 0 for the ideal op amp.', ['Figure P10.44 read from the book page: inverting amplifier.']
@solve('10.45')
def _(): return inv_set((('(a) R1 = 4.7 kΩ, R2 = 220 kΩ', 4.7e3, 220e3), ('(b) R1 = 47 kΩ, R2 = 2.2 MΩ', 47e3, 2.2e6))), 'As Problem 10.44: both circuits have the same gain, 10× different input resistance.', ['Figure P10.44 read from the book page: inverting amplifier.']
def tol5(r1, r2, tag):
    nom = r2 / r1; hi = r2 * 1.05 / (r1 * 0.95); lo = r2 * 0.95 / (r1 * 1.05)
    close(hi * lo, nom * nom, 1e-9)
    return [(tag, f'nominal |Av| = {g(nom)} ({g(db(nom))} dB); worst case {g(lo)} to {g(hi)} ({g(db(lo))} to {g(db(hi))} dB); Rin nominal {si(r1, "Ω")}, worst case {si(0.95 * r1, "Ω")} to {si(1.05 * r1, "Ω")}')]
@solve('10.52')
def _(): return tol5(4.7e3, 220e3, '(a) Prob. 10.45(a)') + tol5(160e3, 330e3, '(b) Prob. 10.44(b)') + tol5(4.3e3, 270e3, '(c) Prob. 10.44(c)'), '|Av| = R2/R1: the largest gain has R2 +5 % and R1 −5 %, the smallest the reverse; Rin = R1 ± 5 %.', ['Same circuit as Problem 10.44 (Figure P10.44).']
