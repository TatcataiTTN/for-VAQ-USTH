"""Floyd 9e calculation exercises without a printed answer (Section Checkups, Examples, Related Problems, even-numbered Problems).  Formulas are Floyd's own."""
import math, cmath
import numpy as np
from core import *
F = 'floyd'
def lag_gain(f, fc): return 1 / (1 + 1j * f / fc)                      # RC lag circuit
def aol(f, A0, fc): return A0 / math.sqrt(1 + (f / fc) ** 2)

# ------------------------------------------------------------------ Section Checkups
@solve(F, 'checkup', 7, '7–3.3')
def _():
    Pout, PD = 1.0, 0.1; eta = Pout / (Pout + PD); Pin = Pout + PD; close(Pout / Pin, eta); close(Pin - Pout, PD)
    return [('Efficiency η = Pout/(Pout + PD)', f'{g(100 * eta)} %')], 'Power taken from the supply = output power + power dissipated in the transistor; η = Pout/(Pout + PD(avg)) (Floyd §7–3).', ['The 100 mW is the average power dissipated in the transistor.']
@solve(F, 'checkup', 12, '12–5.3')
def _():
    Rf, Ri, A, Zin, Zout = 100e3, 2e3, 120000.0, 2e6, 60.0; B = Ri / (Ri + Rf); k = 1 + B * A
    zin_book, zout_book = Ri, Zout / k
    # independent route: exact nodal solution of the inverting stage (Rid from the inverting input to ground, output resistance Zout)
    M = np.array([[1 / Ri + 1 / Zin + 1 / Rf, -1 / Rf], [A, 1.0]]); v1, vo = np.linalg.solve(M, [1 / Ri, 0.0]); zin_exact = 1 / ((1 - v1) / Ri)
    # output impedance: 1 A pushed into the output through Zout, input grounded; unknowns v- and vo
    M3 = np.array([[1 / Ri + 1 / Zin + 1 / Rf, -1 / Rf], [A, 1.0]]); v1b, vob = np.linalg.solve(M3, [0.0, Zout * 1.0]); zout_exact = vob / 1.0
    close(zin_exact, zin_book, 2e-3); close(zout_exact, zout_book, 5e-2)
    return [('B = Ri/(Ri + Rf)', g(B, 4)), ('1 + B·Aol', g(k, 5)), ('Zin(I) ≈ Ri', si(zin_book, 'Ω')), ('Zout(I) = Zout/(1 + B·Aol)', si(zout_book, 'Ω', 3))], 'Inverting amplifier (Floyd §12–4): Zin ≈ Ri; Zout(I) = Zout/(1 + B·Aol) with B = Ri/(Ri + Rf).', [f'Exact nodal solution gives Zin = {si(zin_exact, "Ω")} (the approximation Zin ≈ Ri is what the book uses).']
@solve(F, 'checkup', 12, '12–7.2')
def _(): return [('Open-loop 3 dB bandwidth', '100 Hz')], 'For a single-pole response starting at 0 Hz the open-loop 3 dB bandwidth equals the upper critical frequency fc(ol).', ['The op-amp response is low-pass down to dc, so the bandwidth is fc(ol).']
@solve(F, 'checkup', 12, '12–7.4')
def _():
    tot = 20 + 30; close(db(10 ** (20 / 20) * 10 ** (30 / 20)), tot); return [('Total gain', f'{tot} dB')], 'Stage gains in dB add.', []
@solve(F, 'checkup', 12, '12–7.5')
def _(): return [('Total phase lag', f'{g(-49 + -5.2)}°')], 'Phase lags of the stages add: −49° + (−5.2°).', []
@solve(F, 'checkup', 12, '12–8.2')
def _():
    fT = 30 * 100e3; close(fT / 60, 50e3); return [('New bandwidth', '50 kHz')], 'Gain × bandwidth is constant: 30 × 100 kHz = 3 MHz, so at a gain of 60 the bandwidth is 3 MHz/60.', ['The op-amp has a single-pole response (constant gain–bandwidth product).']
@solve(F, 'checkup', 13, '13–2.3')
def _():
    R = 10e3 / 2; return [('Resistor for the double-weight input', si(R, 'Ω'))], 'In a scaling adder the weight of an input is Rf/Rk, so twice the weight needs half the resistance: 10 kΩ/2.', ['The lower-weighted input has the larger resistor (10 kΩ).']
@solve(F, 'checkup', 14, '14–1.4')
def _():
    G = 1 + 50.5e3 / 10e3; close(G, 6.05); return [('Gain G = 1 + 50.5 kΩ/RG', g(G, 3))], 'AD622: G = 1 + 50.5 kΩ/RG (Floyd §14–1).', []
@solve(F, 'checkup', 16, '16–3.2')
def _():
    R, C = 1e3, 1e-7; fr = 1 / (2 * math.pi * R * C); s = 1j * 2 * math.pi * fr; Z1 = R + 1 / (s * C); Z2 = R / (1 + s * R * C); B = Z2 / (Z1 + Z2)
    close(abs(B), 1 / 3, 1e-9); out = 5 * abs(B); return [('Vout = Vin/3', f'{g(out, 4)} V rms'), ('Phase shift', '0°')], 'At the resonant frequency the lead-lag network has B = 1/3 and 0° phase shift (Floyd §16–3).', []
@solve(F, 'checkup', 17, '17–1.3')
def _():
    dvo, dvi, vo = 0.042, 3.5, 20.0; pct = dvo / dvi * 100; perV = (dvo / vo * 100) / dvi; close(perV, 0.06, 1e-9)
    return [('Line regulation = (ΔVOUT/ΔVIN)·100 % (Eq. 17–1)', f'{g(pct)} %'), ('Line regulation in %/V = (ΔVOUT/VOUT)·100 %/ΔVIN (Eq. 17–2)', f'{g(perV)} %/V')], 'Floyd Eq. 17–1 and 17–2.', []
@solve(F, 'checkup', 17, '17–1.4')
def _():
    Rout, I, Vnl = 80e-3, 1.0, 5.0; Vfl = Vnl - I * Rout; reg = (Vnl - Vfl) / Vfl * 100; close(reg, 1.626, 1e-3); per = reg / (I * 1e3)
    # independent check: Thevenin divider VFL = VNL·RL/(RL + Rout) with RL = VFL/I
    RL = Vfl / I; close(Vnl * RL / (RL + Rout), Vfl, 1e-9)
    return [('Full-load voltage', f'{g(Vfl)} V'), ('Load regulation = (VNL − VFL)/VFL·100 %', f'{g(reg, 3)} %'), ('Per mA of load current', f'{g(per, 3)} %/mA')], 'Thevenin model of the supply: VFL = VNL − IFL·ROUT; load regulation from Eq. 17–3.', ['The 5.0 V is the no-load voltage VNL and 1.0 A is the full-load current.']
@solve(F, 'checkup', 17, '17–2.2')
def _():
    return [('Vref = Vout/(closed-loop gain)', f'{g(8 / 4)} V')], 'Series regulator: VOUT = Acl·VREF with Acl = 1 + R2/R3 (Floyd §17–2), so VREF = 8 V/4.', []
# ------------------------------------------------------------------ Examples (the book prints the solution: the numbers are checked against it) and their Related Problems
@solve(F, 'example', 12, '12–8')
def _():
    r = [aol(f, 1e5, 100) for f in (0, 10, 100, 1000)]; must_in_book(F, 'EXAMPLE 12–8', ['100,000', '99,503', '70,710', '9950']); close(r[1], 99503, 1e-4); close(r[2], 70710, 1e-4); close(r[3], 9950, 1e-3)
    return [('(a) f = 0 Hz', '100,000'), ('(b) f = 10 Hz', f'{r[1]:,.0f}'), ('(c) f = 100 Hz', f'{r[2]:,.0f}'), ('(d) f = 1000 Hz', f'{r[3]:,.0f}')], 'Aol = Aol(mid)/√(1 + (f/fc(ol))²) (Floyd §12–7).', ['The book prints 99,503 for (b): it truncates 99,503.7.']
@solve(F, 'related_problem', 12, '12–8')
def _():
    r = [aol(f, 8e4, 200) for f in (2, 10, 2500)]
    return [('(a) f = 2 Hz', f'{r[0]:,.0f}'), ('(b) f = 10 Hz', f'{r[1]:,.0f}'), ('(c) f = 2500 Hz', f'{r[2]:,.0f}')], 'Aol = Aol(mid)/√(1 + (f/fc(ol))²).', []
@solve(F, 'example', 12, '12–9')
def _():
    ph = [-math.degrees(math.atan(f / 100)) for f in (1, 10, 100, 1000, 10000)]; must_in_book(F, 'EXAMPLE 12–9', ['−0.573°', '−5.71°', '−45°', '−84.3°', '−89.4°'])
    for f, p in zip((1, 10, 100, 1000, 10000), ph): close(math.degrees(cmath.phase(lag_gain(f, 100))), p, 1e-9)                # transfer function of the RC lag circuit
    return [(f'f = {f} Hz', f'{g(p, 3)}°') for f, p in zip((1, 10, 100, 1000, 10000), ph)], 'RC lag circuit: θ = −tan⁻¹(f/fc); plot θ against f on a log axis.', []
@solve(F, 'related_problem', 12, '12–9')
def _():
    fc = 100.0; f = fc * math.tan(math.radians(60)); close(math.degrees(cmath.phase(lag_gain(f, fc))), -60, 1e-9); return [('Frequency for a 60° phase shift', f'{g(f, 4)} Hz')], 'θ = −tan⁻¹(f/fc) = −60° ⇒ f = fc·tan 60°.', ['fc = 100 Hz, as in Example 12–9.']
@solve(F, 'example', 12, '12–10')
def _():
    A = 40 + 32 + 20; th = -math.degrees(math.atan(1)) - math.degrees(math.atan(2 / 40)) - math.degrees(math.atan(2 / 150)); must_in_book(F, 'EXAMPLE 12–10', ['92 dB', '−48.6°']); close(th, -48.6, 1e-3)
    return [('Open-loop midrange gain', f'{A} dB'), ('Total phase lag at f = fc1', f'{g(th, 3)}°')], 'Stage gains add in dB; the phase lags of the stages add: −tan⁻¹(f/fc1) − tan⁻¹(f/fc2) − tan⁻¹(f/fc3).', []
@solve(F, 'related_problem', 12, '12–10')
def _():
    th = -math.degrees(math.atan(1)) - math.degrees(math.atan(1500 / 3000)); return [('Open-loop midrange gain', '75 dB'), ('Total phase lag at f = fc1', f'{g(th, 4)}°')], '50 dB + 25 dB; −tan⁻¹(1) − tan⁻¹(1500/3000).', []
@solve(F, 'example', 12, '12–11')
def _():
    bw = 200 * (1 + 0.002 * 150000); close(bw, 60.2e3); must_in_book(F, 'EXAMPLE 12–11', ['60.2 kHz']); return [('BWcl = BWol(1 + B·Aol(mid))', si(bw, 'Hz'))], 'Closed-loop bandwidth BWcl = BWol(1 + B·Aol(mid)) (Floyd §12–8).', []
@solve(F, 'related_problem', 12, '12–2')
def _():
    sr = (7 - (-8)) / 0.75; close(sr, 20); return [('Slew rate = ΔVout/Δt', f'{g(sr)} V/μs')], 'ΔVout = +7 V − (−8 V) = 15 V in 0.75 μs.', []
@solve(F, 'example', 14, '14–1')
def _():
    Rg = 2 * 25e3 / (500 - 1); close(Rg, 100.2, 2e-3); must_in_book(F, 'EXAMPLE 14–1', ['50 kΩ', '500']); G = 1 + 2 * 25e3 / Rg; close(G, 500); return [('RG = 2R/(Acl − 1)', si(Rg, 'Ω', 4))], 'Instrumentation amplifier: Acl = 1 + 2R/RG (Floyd §14–1).', []
@solve(F, 'related_problem', 14, '14–1')
def _():
    Rg = 2 * 39e3 / (325 - 1); G = 1 + 2 * 39e3 / Rg; close(G, 325); return [('RG = 2R/(Acl − 1)', si(Rg, 'Ω', 4))], 'RG = 2R/(Acl − 1) with R = 39 kΩ.', []
@solve(F, 'example', 14, '14–5')
def _():
    i = 1000e-6 * 25e-3; close(i, 25e-6); must_in_book(F, 'EXAMPLE 14–5', ['25 μA']); return [('Iout = gm·Vin', si(i, 'A'))], 'OTA: Iout = gm·Vin; 1 μS × 1 mV = 1 nA.', []
@solve(F, 'example', 14, '14–9')
def _():
    VT = 0.025; v = lambda R1, Vin=3.0: -VT * math.log(Vin / (40e-9 * R1)); close(v(68e3), -0.1751, 1e-3); must_in_book(F, 'EXAMPLE 14–9', ['175.1 mV']); return [('Vout = −0.025·ln(Vin/(IEBO·R1))', f'{g(1e3 * v(68e3), 4)} mV')], 'Transistor log amplifier (Floyd §14–4): use the natural logarithm.', []
@solve(F, 'related_problem', 14, '14–9')
def _():
    v = -0.025 * math.log(3.0 / (40e-9 * 33e3)); return [('Vout with R1 = 33 kΩ', f'{g(1e3 * v, 4)} mV')], 'Vout = −0.025 ln(Vin/(IEBO·R1)).', ['Vin = 3 V and IEBO = 40 nA as in Example 14–9.']
@solve(F, 'example', 14, '14–8')
def _():
    v = -0.025 * math.log(2.0 / (50e-9 * 100e3)); return [('Vout = −0.025·ln(Vin/(IR·R1))', f'{g(1e3 * v, 4)} mV')], 'Log amplifier of Figure 14–31.', ['Values read from Figure 14–31: Vin = +2 V, R1 = 100 kΩ; IR = 50 nA given in the example.']
@solve(F, 'related_problem', 14, '14–8')
def _():
    v = -0.025 * math.log(4.0 / (50e-9 * 100e3)); return [('Vout for Vin = +4 V', f'{g(1e3 * v, 4)} mV')], 'Vout = −0.025 ln(Vin/(IR·R1)).', ['R1 = 100 kΩ and IR = 50 nA as in Example 14–8 (Figure 14–31).']
@solve(F, 'example', 15, '15–1')
def _():
    Q = 15e3 / 1e3; must_in_book(F, 'EXAMPLE 15–1', ['= 15']); return [('Q = f0/BW', g(Q)), ('Classification', 'narrow-band (Q > 10)')], 'Band-pass filter: Q = f0/BW; Q > 10 is narrow-band (Floyd §15–1).', []
@solve(F, 'related_problem', 15, '15–2')
def _():
    DF = 2 - 5.6 / 10; close(DF, 1.44); return [('DF = 2 − R1/R2', g(DF, 3))], 'Damping factor of the two-pole Sallen-Key filter: DF = 2 − R1/R2 (Floyd §15–2).', []
@solve(F, 'example', 17, '17–1')
def _():
    v = (0.25 / 15 * 100) / 5; close(v, 0.333, 2e-3); must_in_book(F, 'EXAMPLE 17–1', ['0.333%/V']); return [('Line regulation (%/V)', f'{g(v, 3)} %/V')], 'Floyd Eq. 17–2: line regulation = (ΔVOUT/VOUT)·100 %/ΔVIN.', []
@solve(F, 'related_problem', 17, '17–1')
def _():
    v = (0.42 / 20 * 100) / 3.5; return [('Regulation (%/V)', f'{g(v, 3)} %/V')], 'Eq. 17–2 with ΔVOUT = 0.42 V, VOUT = 20 V, ΔVIN = 3.5 V.', []
@solve(F, 'example', 17, '17–2')
def _():
    reg = (12 - 11.9) / 11.9 * 100; close(reg, 0.840, 1e-3); must_in_book(F, 'EXAMPLE 17–2', ['0.840%', '0.084%/mA']); return [('Load regulation', f'{g(reg, 3)} %'), ('Per mA', f'{g(reg / 10, 3)} %/mA')], 'Floyd Eq. 17–3: load regulation = (VNL − VFL)/VFL·100 %; the load current changes by 10 mA.', []
@solve(F, 'related_problem', 17, '17–2')
def _():
    reg = (18 - 17.8) / 17.8 * 100; return [('Load regulation', f'{g(reg, 3)} %'), ('Per mA', f'{g(reg / 50, 3)} %/mA')], 'Eq. 17–3 with VNL = 18 V, VFL = 17.8 V, ΔIL = 50 mA.', []
@solve(F, 'example', 17, '17–9')
def _():
    R1 = 5 / 0.5; close(R1, 10); must_in_book(F, 'EXAMPLE 17–9', ['5 V', '0.5 A']); return [('R1 = VOUT/IL', f'{g(R1)} Ω')], 'The 7805 holds 5 V between its output and ground terminals, so the current-setting resistor is R1 = 5 V/IL (neglecting IG).', ['The regulator ground-terminal current IG is neglected.']
@solve(F, 'related_problem', 17, '17–9')
def _():
    R1 = 8 / 0.5; return [('R1 = 8 V/0.5 A', f'{g(R1)} Ω')], 'A 7808 holds 8 V across R1.', ['IG neglected.']
@solve(F, 'related_problem', 17, '17–6')
def _():
    v = 1.25 * (1 + 2e3 / 220) + 50e-6 * 2e3; return [('VOUT = 1.25 V(1 + R2/R1) + IADJ·R2', f'{g(v, 4)} V')], 'LM317 output (Floyd §17–4).', ['R1 = 220 Ω (Figure 17–30), IADJ = 50 μA as in Example 17–6.']
@solve(F, 'related_problem', 17, '17–7')
def _():
    I = 0.7 / 1.5; return [('Qext turns on at IREG = 0.7 V/Rext', f'{g(1e3 * I, 3)} mA')], 'The external pass transistor turns on when the drop across Rext reaches 0.7 V.', ['VBE(on) = 0.7 V.']
@solve(F, 'related_problem', 7, '7–3')
def _():
    must_in_book(F, 'EXAMPLE 7–3', ['133 mA']); close(20 / 150 * 1e3, 133.3, 2e-3)
    return [('Maximum peak output voltage ≈ VCC', '15 V'), ('Maximum peak output current ≈ VCC/RL', f'{g(1e3 * 15 / 150)} mA')], 'Ideal limits of the push-pull stage: Vout(peak) ≈ VCC, Iout(peak) ≈ VCC/RL.', ['RL = 150 Ω from Figure 7–15 (Example 7–3).']
# ------------------------------------------------------------------ even-numbered end-of-chapter Problems
@solve(F, 'problem', 12, '22')
def _():
    Rs, I1, I2 = 75.0, 42e-6, 40e-6; Rc = Rs; err = Rs * abs(I1 - I2)            # follower: Vout = I-·Rc − I+·Rs with Rc = Rs
    return [('(a) Compensating resistor', f'{g(Rc)} Ω, in the feedback path (between the output and the inverting input)'), ('(b) Output error voltage', f'{g(1e6 * err)} μV')], 'Bias-current compensation (Floyd §12–6): the resistor equals the resistance seen by the other input; the error is IOS × R.', ['The two currents (42 μA and 40 μA) are the input currents after compensation: the error is the offset current × 75 Ω.']
@solve(F, 'problem', 12, '24')
def _(): return [('Output error voltage', '2 nV')], 'A voltage follower has unity gain, so the input offset voltage appears unchanged at the output.', []
@solve(F, 'problem', 12, '26')
def _():
    A = 120 - 50; return [('Closed-loop gain', f'{A} dB ({g(10 ** (A / 20), 4)})')], 'Gains in dB subtract: 120 dB − 50 dB.', []
@solve(F, 'problem', 12, '28')
def _():
    fc, R = 5e3, 1e3; C = 1 / (2 * math.pi * fc * R); Xc = 1 / (2 * math.pi * 3e3 * C); close(Xc, R * fc / 3e3, 1e-9); close(abs(lag_gain(3e3, fc)), Xc / math.hypot(R, Xc), 1e-9)          # |H| of the RC lag circuit = XC/√(R² + XC²)
    return [('XC at 3 kHz = R·fc/f', si(Xc, 'Ω', 4))], 'RC lag circuit: XC = R at f = fc, and XC ∝ 1/f.', []
@solve(F, 'problem', 12, '30')
def _():
    r = [aol(f, 8e4, 1e3) for f in (100, 1e3, 1e4, 1e6)]; return [(f'({l}) f = {n}', g(v, 4)) for l, n, v in zip('abcd', ('100 Hz', '1 kHz', '10 kHz', '1 MHz'), r)], 'Aol = Aol(mid)/√(1 + (f/fc(ol))²).', []
@solve(F, 'problem', 12, '32')
def _():
    fs = [100, 400, 850, 8500, 25000, 85000]; ph = [-math.degrees(math.atan(f / 8500)) for f in fs]
    for f, p in zip(fs, ph): close(math.degrees(cmath.phase(lag_gain(f, 8500))), p, 1e-9)
    names = ['100 Hz', '400 Hz', '850 Hz', '8.5 kHz', '25 kHz', '85 kHz']; return [(f'({l}) {n}', f'{g(p, 4)}°') for l, n, p in zip('abcdef', names, ph)], 'θ = −tan⁻¹(f/fc) with fc = 8.5 kHz; plot θ against f on a log axis.', []
@solve(F, 'problem', 12, '36')
def _():
    bw = 1500 * (1 + 0.015 * 180000); close(bw, 4.0515e6, 1e-4); return [('BWcl = BWol(1 + B·Aol(mid))', si(bw, 'Hz', 4))], 'BWcl = fc(ol)(1 + B·Aol(mid)).', []
@solve(F, 'problem', 12, '52')
def _():
    Ri, Rf = 10e3, 680e3; Rc = Ri * Rf / (Ri + Rf); A = 2e5
    M = np.array([[1 / Ri + 1 / Rf, -1 / Rf], [A, 1.0]]); v1, vo = np.linalg.solve(M, [1 / Ri, 0.0]); gain = vo
    close(gain, -68, 5e-2); assert abs(gain / -68 - 1) < 0.05
    return [('Ri', '10 kΩ (sets Zin ≈ Ri)'), ('Rf = 68·Ri', '680 kΩ'), ('Compensating resistor Rc = Ri‖Rf at the + input', f'{si(Rc, "Ω", 3)} → use 10 kΩ'), ('Resulting gain', f'{g(gain, 4)} (within ±5 % of −68)')], 'Inverting amplifier: |Av| = Rf/Ri, Zin ≈ Ri (Floyd §12–4); bias compensation Rc = Ri‖Rf (§12–6).', ['One valid design (several are possible): the book\'s even-numbered problems have no printed answer.', 'Aol of the 741 taken as 200,000 for the check.']
@solve(F, 'problem', 12, '56')
def _():
    fT = 1e6; Acl = fT / 5e3; return [('Acl(max) = fT/BW', f'{g(Acl)} ({g(db(Acl), 3)} dB)')], 'Gain × bandwidth = fT: with BW ≥ 5 kHz the closed-loop gain cannot exceed fT/5 kHz.', ['741 unity-gain bandwidth fT = 1 MHz (typical datasheet value; the book\'s datasheet figure is an image).']
@solve(F, 'problem', 14, '22')
def _():
    v = [math.log(x) for x in (0.5, 2, 50, 130)]; return [(f'({l}) ln {x}', g(y, 4)) for l, x, y in zip('abcd', ('0.5', '2', '50', '130'), v)], 'Natural logarithms.', []
@solve(F, 'problem', 17, '28')
def _():
    R1 = 1.25 / 0.5; P = 0.5 ** 2 * R1; I50 = 1.25 / R1 + 50e-6; close(I50, 0.50005, 1e-3)
    return [('R1 = 1.25 V/IL', f'{g(R1)} Ω'), ('Power in R1', f'{g(P, 3)} W (use a 1 W resistor)')], 'LM317 as a current regulator: IL = VREF/R1 (+ IADJ), with VREF = 1.25 V; the load goes where RL normally sits and R1 is the only resistor.', ['IADJ (≈ 50 μA) is neglected.']
