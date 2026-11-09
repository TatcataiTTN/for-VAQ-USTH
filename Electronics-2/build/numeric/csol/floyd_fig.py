"""Floyd 9e calculation exercises that refer to a circuit in a book FIGURE (Examples, Related Problems, even-numbered Problems, Circuit-Action, Checkups).
Procedure for each: the figure is cropped (build/numeric/figcrop.py) and read by eye; the component values are written into the solver; the solver (1) recomputes the book's
own printed numbers for an Example (must_in_book) or the printed answer of a neighbouring odd Problem on the same figure, so a misread value is caught, (2) computes
the result a second way (nodal / mesh solution of the small-signal model, time stepping, or exact network instead of the textbook formula) and asserts agreement.
A solver returns (parts, how, assume, ctx, circuit): `circuit` describes the figure in words with its values (the figure itself is not republished), shown on the Written page.
Where the printed solution is wrong the printed value is kept in the notes and the corrected one is the answer (see data/verify/mNN_notes.json)."""
import math, cmath, re
import numpy as np
from core import *
F = 'floyd'
def par(*r): return 1 / sum(1 / x for x in r)
def must_near(tag, needles, span=3600):
    """Like must_in_book for the Examples whose heading is separated from 'Solution' by a figure: the needles must all appear within `span` characters after the last occurrence of the heading."""
    t = book_text(F); idx = [m.start() for m in re.finditer(re.escape(tag) + r'(?![\d–])', t)]
    for i in idx[::-1]:
        seg = re.sub(r'\s+', ' ', t[i:i + span]); seg2 = seg.replace('−', '-').replace('–', '-')
        if all(n in seg or n.replace('−', '-') in seg2 for n in needles): return
    raise AssertionError(('printed solution not found', tag, needles))
def ce_nodal(Rs, Rb, beta, rep, Rc, RL, Re=0.0):
    """Mid-band small-signal model of a common-emitter stage solved by KCL (capacitors short, emitter resistor Re un-bypassed, 0 if bypassed):
    unknowns vb, ve, vc;  r_pi = beta*re', gm = 1/re'.  Source 1 V behind Rs; Rb = bias resistors to ground; returns (vout/vsource, vb)."""
    rpi = beta * rep; gm = 1 / rep; Re = max(Re, 1e-6)
    A = np.array([[1 / Rs + 1 / Rb + 1 / rpi, -1 / rpi, 0.0],
                  [-1 / rpi - gm, 1 / Re + 1 / rpi + gm, 0.0],
                  [gm, -gm, 1 / Rc + 1 / RL]])
    v = np.linalg.solve(A, np.array([1 / Rs, 0.0, 0.0])); return v[2], v[0]
def dc_bias(VCC, R1, R2, RE, Vbe=0.7):
    VB = VCC * R2 / (R1 + R2); IE = (VB - Vbe) / RE; return VB, IE, 0.025 / IE            # Floyd: voltage-divider bias with the base current neglected, r'e = 25 mV / IE

# ============================================================================================ Chapter 6 (m04)
C616 = 'Figure 6–16 (p.284): voltage-divider biased 2N3904 common-emitter amplifier. VCC = +12 V, R1 = 22 kΩ (VCC to base), R2 = 6.8 kΩ (base to ground), RC = 1.0 kΩ, RE = 560 Ω with the bypass capacitor C2 across it; input coupling C1, output coupling C3.'
@solve(F, 'example', 6, '6–6')
def _():
    RC, RL, rep = 1.0e3, 5e3, 6.58; Rc = par(RC, RL); Av = Rc / rep
    must_in_book(F, 'EXAMPLE 6–6', ['833 Ω', '127', '6.58 Ω'])
    vout, _ = ce_nodal(1.0, 1e12, 1e6, rep, RC, RL); close(-vout, Av, 1e-3)                  # nodal solution of the small-signal model
    close(Rc, 833, 1e-3); close(Av, 127, 4e-3)
    return [('ac collector resistance Rc = RC ‖ RL', si(Rc, 'Ω', 3)), ('Voltage gain Av = Rc/r′e', g(Av, 3))], 'RC = 1.0 kΩ is read from Figure 6–16; with the emitter bypassed Av = Rc/r′e where Rc = RC ‖ RL (Floyd §6–6). The book prints 833 Ω and 127.', ['The unloaded gain was 152 in Example 6–5 (RC/r′e).'], None, C616
@solve(F, 'related_problem', 6, '6–6')
def _():
    RC, RL, rep = 1.8e3, 10e3, 18.5; Rc = par(RC, RL); Av = Rc / rep
    vout, _ = ce_nodal(1.0, 1e12, 1e6, rep, RC, RL); close(-vout, Av, 1e-3)
    return [('ac collector resistance Rc = RC ‖ RL', si(Rc, 'Ω', 4)), ('Voltage gain Av = Rc/r′e', g(Av, 3))], 'Rc = 1.8 kΩ ‖ 10 kΩ; Av = Rc/r′e with the given r′e = 18.5 Ω (the emitter is bypassed). The changed R1, R2, RE only change the dc bias, which the statement already gives as r′e.', ['R1, R2 and RE affect only r′e, which is given.'], None, C616
C657 = 'Figure 6–57 (p.331): two identical capacitively coupled voltage-divider biased common-emitter stages, VCC = +15 V. Stage 1: R1 = 33 kΩ, R2 = 8.2 kΩ, RC = R3 = 3.3 kΩ, RE = R4 = 1.0 kΩ bypassed by C2. Stage 2 (after coupling capacitor C3): R5 = 33 kΩ, R6 = 8.2 kΩ, RC = R7 = 3.3 kΩ, RE = R8 = 1.0 kΩ bypassed by C4; output through C5. βac = βDC = 175.'
@solve(F, 'problem', 6, '32')
def _():
    VCC, R1, R2, RC, RE, beta = 15.0, 33e3, 8.2e3, 3.3e3, 1.0e3, 175.0; RL, Rs, vs = 18e3, 75.0, 50e-6
    VB, IE, rep = dc_bias(VCC, R1, R2, RE); Rin2 = par(R1, R2, beta * rep)                         # second stage loads the first
    Av1 = par(RC, Rin2) / rep; Av2 = par(RC, RL) / rep; Av = Av1 * Av2
    Av2_unl = RC / rep; Rc1_unl = par(RC, Rin2)                                                  # Problem 31 (same figure, no load): printed 93.6, 303, 28,361
    close(Av1, 93.6, 5e-3); close(Av2_unl, 303, 1e-2); close(Av1 * Av2_unl, 28361, 1.5e-2)        # reproduces the printed answer of Problem 31 => the figure was read correctly
    # independent route: both stages solved together by KCL (capacitors short, emitters bypassed); unknowns vb1, vc1, vb2, vc2 with vb1 = 1 V and vb2 = vc1 (through C3)
    rpi = beta * rep; gm = 1 / rep; Rb = par(R1, R2); Rin1 = par(R1, R2, beta * rep)
    A = np.array([[1.0, 0, 0, 0], [gm, 1 / RC + 1 / Rb + 1 / rpi, 0, 0], [0, -1.0, 1.0, 0], [0, 0, gm, 1 / par(RC, RL)]]); v = np.linalg.solve(A, np.array([1.0, 0, 0, 0]))
    close(v[1], -Av1, 1e-3); close(v[3], Av, 1e-3)                                               # two inversions: the overall voltage gain is positive (in phase)
    Vin1 = vs * Rin1 / (Rs + Rin1); Vout = Av * Vin1
    return [('(a) Av1 (stage 1, loaded by the input resistance of stage 2)', g(Av1, 3)), ('(a) Av2 (stage 2 with RL = 18 kΩ: Rc = RC ‖ RL)', g(Av2, 3)), ('(b) overall voltage gain Av = Av1·Av2', f'{g(Av, 4)}'),
            ('(c) in dB', f'Av1 = {g(db(Av1), 3)} dB, Av2 = {g(db(Av2), 3)} dB, Av = {g(db(Av), 4)} dB (= sum of the stage dB values)'),
            ('Extra: output for the 50 μV, 75 Ω source (the source resistance only divides the input)', f'Vin = {g(Vin1 * 1e6, 3)} μV, Vout = {g(Vout, 3)} V')], \
        f'DC: VB = VCC·R2/(R1 + R2) = {g(VB, 4)} V, IE = (VB − 0.7 V)/RE = {g(IE * 1e3, 4)} mA, r′e = 25 mV/IE = {g(rep, 4)} Ω. Rin(tot) of a stage = R1 ‖ R2 ‖ β·r′e = {si(Rin1, 'Ω', 4)}; Av1 = (RC ‖ Rin(tot2))/r′e, Av2 = (RC ‖ RL)/r′e (Floyd §6–6).', \
        ['Gains are voltage gains base-to-collector of the amplifier as in Problem 31; the 75 Ω source resistance does not change them (it only reduces the signal at the input, shown as an extra).', f'Same figure as Problem 31, whose printed answers (Av1 = 93.6, Av2 = 303 unloaded) are reproduced within 1 % (r′e rounding).', 'The 50 μV is taken as the same kind of value (rms or peak) as the output.'], None, C657

# ============================================================================================ Chapter 7 (m04)
C75 = 'Figure 7–5 (p.344, Example 7–1): VCC = +12 V. Stage 1 = voltage-divider biased common-emitter Q1 with R1 = 56 kΩ, R2 = 10 kΩ, RC = 4.7 kΩ, swamping RE1 = 68 Ω in series with RE2 = 560 Ω (RE2 bypassed by C2). Stage 2 = Darlington emitter follower Q2–Q3 biased by R3 = 5.6 kΩ and R4 = 22 kΩ (R3 from VCC, R4 to ground), emitter resistor RE3 = 33 Ω (2 W); the load is an 8 Ω speaker through C4. Source Vs = 50 mV pp at 1 kHz. βac = 200 for all transistors.'
@solve(F, 'example', 7, '7–2')
def _():
    VCC, R1, R2, RC, RE1, RE2, R3, R4, RE3, RL, beta = 12.0, 56e3, 10e3, 4.7e3, 68.0, 560.0, 5.6e3, 22e3, 33.0, 8.0, 200.0
    must_in_book(F, 'EXAMPLE 7–2', ['35.4 mV', '8.4 kΩ', '149 nW', '817,330', '122 mW', '8.2 V', '0.25 A', '3 W', '4%'])
    VB = VCC * R2 / (R1 + R2); IE1 = (VB - 0.7) / (RE1 + RE2); rep = 0.025 / IE1; Rc1 = par(RC, R3, R4); Av1 = Rc1 / (RE1 + rep)
    Rin_book = 8.4e3; Rin = par(R1, R2, beta * (RE1 + rep)); close(par(R1, R2), 8.485e3, 1e-3)    # 8.4 kΩ printed = R1 ‖ R2 only: the 200(68 + 14) = 16.4 kΩ branch was left out
    close(Av1, 27.9, 5e-3)                                                                   # first stage of Example 7–1, as printed
    VE3 = VCC * R4 / (R3 + R4) - 1.4; IE3 = VE3 / RE3; PDC = IE3 * VCC; close(VE3, 8.2, 5e-3); close(IE3, 0.25, 1.5e-2); close(PDC, 3.0, 1.5e-2)
    vin_b = 100e-3 / 2 / math.sqrt(2); Pin_b = vin_b ** 2 / Rin_book; Ap_b = Av1 ** 2 * Rin_book / RL; Pout_b = Pin_b * Ap_b; close(vin_b, 35.4e-3, 3e-3); close(Pin_b, 149e-9, 2e-2); close(Ap_b, 817330, 1e-2); close(Pout_b, 122e-3, 3e-2); close(Pout_b / PDC, 0.04, 5e-2)
    vin = 50e-3 / 2 / math.sqrt(2); Pin = vin ** 2 / Rin; Ap = Av1 ** 2 * Rin / RL; Pout = Pin * Ap; eta = Pout / PDC            # corrected: 50 mV pp = 17.7 mV rms; Rin includes the βac(RE1 + r′e) branch
    close(Pout, (Av1 * vin) ** 2 / RL, 1e-9)                                                  # independent route: output power from the output voltage, Vout²/RL (does not use Rin or Ap)
    close(Pout_b, (Av1 * vin_b) ** 2 / RL, 2e-2)                                              # ... and it reproduces the book's 122 mW for the book's 35.4 mV
    return [('Input signal (50 mV pp)', f'{g(vin * 1e3, 3)} mV rms'), ('Input resistance Rin(tot) = R1 ‖ R2 ‖ β(RE1 + r′e)', si(Rin, 'Ω', 3)), ('Input power Pin = Vin²/Rin', f'{g(Pin * 1e9, 3)} nW'),
            ('Power gain Ap = Av²·Rin/RL', f'{round(Ap, -3):,.0f}'), ('Output power Pout = Pin·Ap = Vout²/RL', f'{g(Pout * 1e3, 3)} mW'), ('DC supply power PDC = ICC·VCC', f'{g(PDC, 3)} W (IE(Q3) = {g(IE3, 3)} A)'),
            ('Efficiency η = Pout/PDC', f'{g(100 * eta, 2)} %  (the book prints ≈ 4 %, see the note)')], \
        'Floyd Example 7–2 with the circuit of Example 7–1: Av1 = Rc1/(RE1 + r′e) = 27.9; PDC = ICC·VCC with IE(Q3) = VE(Q3)/RE3 = 8.2 V/33 Ω ≈ 0.25 A; η = Pout/PDC. Pout is also checked as Vout²/RL (Vout = Av·Vin).', \
        ['BOOK ERROR 1: the printed solution says 50 mV peak-to-peak is 35.4 mV rms. 35.4 mV rms is 50 mV PEAK (100 mV pp); 50 mV pp is 17.7 mV rms. The book\'s numbers (Pin = 149 nW, Pout = 122 mW, η ≈ 4 %) are reproduced here for 35.4 mV to confirm the circuit values, but the figure says 50 mV pp, which gives η ≈ 1 %.',
         'BOOK ERROR 2 (also in Example 7–1): the printed Rin(tot) = 56 kΩ ‖ 10 kΩ ‖ 200(68 Ω + 14 Ω) = 8.4 kΩ is only 56 kΩ ‖ 10 kΩ; with the 16.4 kΩ branch it is 5.6 kΩ, so the power gain of Example 7–1 is about 5.5·10⁵, not 817,330. Pout does not depend on it.',
         'Either way the lesson is the same: a class A power stage is very inefficient.'], None, C75
C746 = 'Figure 7–46 (p.379): class AB push-pull emitter-follower output stage on a single supply VCC = +15 V. R1 = 1.0 kΩ from VCC to the base of the upper (npn) transistor Q1, diodes D1 and D2 in series between the two bases, R2 = 1.0 kΩ from the base of the lower (pnp) transistor Q2 to ground; Q1 collector at VCC, Q2 collector at ground, the emitters joined at the output, which drives RL = 75 Ω through the coupling capacitor C3. The source Vs is coupled to the two bases through C1 and C2.'
@solve(F, 'problem', 7, '16')
def _():
    VCC, RL = 15.0, 75.0
    def pmax(VCC):                                                                          # single supply: VCEQ = VCC/2, ideal peak output voltage = VCEQ, peak current = VCEQ/RL
        Vp = VCC / 2; Ip = Vp / RL; return Vp, Ip, (0.707 * Ip) * (0.707 * Vp)
    Va, Ia, Pa = pmax(15.0); Vb, Ib, Pb = pmax(24.0)
    t = np.linspace(0, 1, 200001)[:-1]; Pnum = lambda Vp: float(np.mean((Vp * np.sin(2 * math.pi * t)) ** 2 / RL))    # independent: average of v²/RL over one full cycle
    close(Pnum(Va), Pa, 2e-3); close(Pnum(Vb), Pb, 2e-3); close(Pa, VCC ** 2 / (8 * RL), 2e-3)
    close(0.707 * 0.707 * 10 ** 2 / 2 / (2 * RL) * 0 + (5 ** 2) / (2 * RL), 0.1667, 2e-3)    # the printed answer of Problem 15(b): 167 mW for a 10 V pp input (5 V peak) into 75 Ω => RL = 75 Ω was read correctly
    return [('(a) maximum load power, VCC = 15 V', f'{g(Pa * 1e3, 3)} mW  (peak {g(Va, 3)} V and {g(Ia * 1e3, 3)} mA)'), ('(b) maximum load power, VCC = 24 V', f'{g(Pb, 3)} W  (peak {g(Vb, 3)} V and {g(Ib * 1e3, 3)} mA)')], \
        'Single-supply class AB: VCEQ = VCC/2 and the ideal maximum peak output voltage is VCEQ, so Pout(max) = (0.707·Ic)(0.707·VCEQ) = VCC²/(8·RL) (Floyd §7–2). Ideal: transistor saturation voltage neglected.', \
        ['Ideal limit; the actual maximum is slightly smaller because VCE(sat) of the transistors is not zero.', 'RL = 75 Ω and VCC = +15 V are read from Figure 7–46 and confirmed by the printed answer of Problem 15(b) (167 mW for a 10 V pp input).'], None, C746
@solve(F, 'problem', 7, '18')
def _():
    VCC, R1, R2, RL, beta, Rs, Vs = 15.0, 1e3, 1e3, 75.0, 200.0, 50.0, 1.0
    VB1 = 8.2; ICQ = (VCC - VB1) / R1; close(ICQ, 6.8e-3, 1e-9); rep = 0.025 / ICQ                # the quiescent current of Problem 15(a): 6.8 mA (printed)
    Rin_b = beta * (rep + RL); Rin = par(R1, R2, Rin_b); Vin = Vs * Rin / (Rs + Rin)           # Eq. 7–8
    A = np.array([[1 / Rs + 1 / R1 + 1 / R2 + 1 / Rin_b]]); vb = np.linalg.solve(A, np.array([Vs / Rs]))[0]; close(vb, Vin, 1e-9)           # independent: KCL at the input node
    return [('Input resistance Rin = β(r′e + RL) ‖ R1 ‖ R2', si(Rin, 'Ω', 4)), ('Actual rms signal at the amplifier input', f'{g(Vin, 3)} V')], \
        f'ICQ = 6.8 mA, so r′e = 25 mV/ICQ = {g(rep, 3)} Ω. Eq. 7–8: Rin = β(r′e + RL) ‖ R1 ‖ R2 (the diode ac resistances are negligible, as in Example 7–6). The 50 Ω source and Rin form a voltage divider: Vin = Vs·Rin/(Rs + Rin).', \
        ['r′e from the dc current 6.8 mA of Problem 15(a); ignoring r′e changes the result in the third digit.'], None, C746

# ============================================================================================ Chapter 12 (m02)
def opamp_z(Aol, Zin, Zout, Rf, Ri, mode):
    """Exact impedances of a feedback op-amp by KCL (finite Aol, Zin between the inputs, Zout in series with the output): returns (Zin seen by the source, Zout seen by the load).
    mode 'NI' (Ri to ground, Rf feedback, source at the + input), 'VF' (voltage follower), 'I' (source through Ri to the - input, + input grounded).
    The textbook formulas Zin(NI) = (1 + Aol·B)·Zin, Zout = Zout/(1 + Aol·B), Zin(I) ≈ Ri are the approximations this is compared with."""
    gR = 1 / Rf if Rf else 1e12; gI = 0 if Ri == float('inf') else 1 / Ri
    def solve_(vin, iout):                                              # unknowns v- and vo; returns (v-, vo, input current)
        if mode == 'VF':                                                  # voltage follower: v- = vo, one unknown
            vo = (Aol * vin / Zout + vin / Zin + iout) / ((1 + Aol) / Zout + 1 / Zin); return vo, vo, (vin - vo) / Zin
        if mode == 'NI':
            A = np.array([[1 / Zin + gI + gR, -gR], [Aol / Zout - gR, 1 / Zout + gR]], float); b = np.array([vin / Zin, Aol * vin / Zout + iout])
            vm, vo = np.linalg.solve(A, b); return vm, vo, (vin - vm) / Zin
        A = np.array([[1 / Ri + 1 / Zin + gR, -gR], [Aol / Zout - gR, 1 / Zout + gR]], float); b = np.array([vin / Ri, iout])      # vp = 0: the source is -Aol·v-
        vm, vo = np.linalg.solve(A, b); return vm, vo, (vin - vm) / Ri
    _, _, i = solve_(1.0, 0.0); _, vo0, _ = solve_(0.0, 1.0); return 1.0 / i, vo0
C1218 = 'Figure 12–18 (p.616): noninverting amplifier, Rf = 100 kΩ from the output to the inverting input, Ri = 4.7 kΩ from the inverting input to ground, signal on the + input.'
C1222 = 'Figure 12–22 (p.618): inverting amplifier, Ri = 2.2 kΩ in series with the input to the − input, feedback resistor Rf (unknown) from the output to the − input, + input grounded.'
C1225 = 'Figure 12–25 (p.621): noninverting amplifier, Rf = 220 kΩ from the output to the inverting input, Ri = 10 kΩ from the inverting input to ground, signal on the + input.'
C1228 = 'Figure 12–28 (p.623): inverting amplifier, Ri = 1.0 kΩ in series with the input to the − input, Rf = 100 kΩ from the output to the − input, + input grounded.'
C1243 = 'Figure 12–43 (p.635): (a) noninverting amplifier with Rf = 220 kΩ and Ri = 3.3 kΩ; (b) inverting amplifier with Rf = 47 kΩ and Ri = 1.0 kΩ.'
@solve(F, 'related_problem', 12, '12–3')
def _():
    Rf, Ri = 150e3, 4.7e3; A = 1 + Rf / Ri; _z = opamp_z(1e9, 1e12, 1e-3, Rf, Ri, 'NI')
    vo = np.linalg.solve(np.array([[1 / Ri + 1 / Rf, -1 / Rf], [1e9, -1e9 * 0 + 0.0 + 1.0 * 0 + 1.0]]), np.array([0.0, 1e9 * 1.0]))        # ideal-ish op-amp (Aol = 1e9): V- = V+ => Vout = (1 + Rf/Ri)·Vin
    close(vo[1], A, 1e-3)
    return [('Closed-loop gain Acl(NI) = 1 + Rf/Ri', g(A, 3))], 'Noninverting amplifier: Acl(NI) = 1 + Rf/Ri with Rf = 150 kΩ and Ri = 4.7 kΩ (read from Figure 12–18); the example gives 22.3 for Rf = 100 kΩ.', [], None, C1218
@solve(F, 'example', 12, '12–4')
def _():
    Ri, A = 2.2e3, 100.0; Rf = A * Ri; must_in_book(F, 'EXAMPLE 12–4', ['2.2 kΩ', '220'])
    Aol = 1e8; M = np.array([[1 / Ri + 1 / Rf + 1e-9, -1 / Rf], [-Aol, 1.0]]); vo = np.linalg.solve(M, np.array([1 / Ri, 0.0]))[1]; close(vo, -A, 1e-4)      # inverting amplifier solved with a huge Aol
    return [('Rf = |Acl(I)|·Ri', si(Rf, 'Ω', 3))], 'Inverting amplifier: |Acl(I)| = Rf/Ri, so Rf = 100 × 2.2 kΩ = 220 kΩ (Ri = 2.2 kΩ is read from Figure 12–22).', [], None, C1222
@solve(F, 'related_problem', 12, '12–4')
def _():
    Ri, A = 2.7e3, 25.0; Rf = A * Ri; close(Rf, 67.5e3)
    Aol = 1e8; M = np.array([[1 / Ri + 1 / Rf + 1e-9, -1 / Rf], [-Aol, 1.0]]); vo = np.linalg.solve(M, np.array([1 / Ri, 0.0]))[1]; close(vo, -A, 1e-4)
    return [('Rf = |Acl(I)|·Ri', f'{si(Rf, "Ω", 3)} (nearest standard value 68 kΩ)')], 'Rf = 25 × 2.7 kΩ = 67.5 kΩ.', [], None, C1222
@solve(F, 'example', 12, '12–5')
def _():
    Rf, Ri, Zin, Zout, Aol = 220e3, 10e3, 2e6, 75.0, 200000.0; B = Ri / (Ri + Rf); k = 1 + Aol * B; zin, zout, acl = k * Zin, Zout / k, 1 + Rf / Ri
    must_in_book(F, 'EXAMPLE 12–5', ['0.0435', '17.4 G', '8.6 m', '23.0']); close(zin, 17.4e9, 3e-3); close(zout, 8.6e-3, 1e-2)
    ze, zo = opamp_z(Aol, Zin, Zout, Rf, Ri, 'NI'); close(ze, zin, 3e-2); close(zo, zout, 3e-2)                  # exact KCL solution agrees with the approximations
    return [('Attenuation B = Ri/(Ri + Rf)', g(B, 3)), ('Zin(NI) = (1 + Aol·B)·Zin', si(zin, 'Ω', 3)), ('Zout(NI) = Zout/(1 + Aol·B)', si(zout, 'Ω', 2)), ('(b) Acl(NI) = 1 + Rf/Ri', g(acl, 3))], \
        'Noninverting amplifier (Floyd §12–5): B = Ri/(Ri + Rf), Zin(NI) = (1 + Aol·B)·Zin, Zout(NI) = Zout/(1 + Aol·B). The book prints 17.4 GΩ, 8.6 mΩ and 23.0.', [f'The exact nodal solution of the op-amp model gives Zin = {si(ze, "Ω", 3)} and Zout = {si(zo, "Ω", 2)}.'], None, C1225
@solve(F, 'related_problem', 12, '12–5')
def _():
    Rf, Ri, Zin, Zout, Aol = 220e3, 10e3, 3.5e6, 82.0, 135000.0; B = Ri / (Ri + Rf); k = 1 + Aol * B; zin, zout, acl = k * Zin, Zout / k, 1 + Rf / Ri
    ze, zo = opamp_z(Aol, Zin, Zout, Rf, Ri, 'NI'); close(ze, zin, 3e-2); close(zo, zout, 3e-2)
    return [('Zin(NI) = (1 + Aol·B)·Zin', si(zin, 'Ω', 3)), ('Zout(NI) = Zout/(1 + Aol·B)', si(zout, 'Ω', 3)), ('(b) Acl(NI) = 1 + Rf/Ri', g(acl, 3))], 'Same circuit as Example 12–5 (Rf = 220 kΩ, Ri = 10 kΩ, so B = 0.0435) with the new op-amp values.', [f'Exact nodal solution: Zin = {si(ze, "Ω", 3)}, Zout = {si(zo, "Ω", 3)}.'], None, C1225
@solve(F, 'example', 12, '12–7')
def _():
    Rf, Ri, Zin, Zout, Aol = 100e3, 1.0e3, 4e6, 50.0, 50000.0; B = Ri / (Ri + Rf); k = 1 + Aol * B; zout = Zout / k; acl = -Rf / Ri; zin = Ri
    must_in_book(F, 'EXAMPLE 12–7', ['1.0 k', '101 k', '0.001', '980 m']); close(B, 1 / 101, 1e-12)
    ze, zo = opamp_z(Aol, Zin, Zout, Rf, Ri, 'I'); close(ze, zin, 5e-3); close(zo, zout, 1e-2)               # exact KCL solution supports the corrected value, not the printed 980 mΩ
    return [('Zin(I) ≈ Ri', si(zin, 'Ω', 2)), ('Attenuation B = Ri/(Ri + Rf)', g(B, 3)), ('Zout(I) = Zout/(1 + Aol·B)', si(zout, 'Ω', 3)), ('Acl(I) = −Rf/Ri', g(acl, 3))], \
        'Inverting amplifier (Floyd §12–5): Zin(I) ≈ Ri, B = Ri/(Ri + Rf), Zout(I) = Zout/(1 + Aol·B), Acl(I) = −Rf/Ri.', \
        ['BOOK ERROR: the printed solution gives B = 1.0 kΩ/101 kΩ = 0.001, but 1/101 = 0.0099; with B = 0.001 it prints Zout(I) = 980 mΩ. The correct value is 50 Ω/(1 + 50,000 × 0.0099) = 0.101 Ω (an exact KCL solution of the op-amp model confirms it). Still “zero for all practical purposes”.'], None, C1228
@solve(F, 'related_problem', 12, '12–7')
def _():
    Rf, Ri, Zin, Zout, Aol = 82e3, 560.0, 5e6, 75.0, 100000.0; B = Ri / (Ri + Rf); k = 1 + Aol * B; zout = Zout / k; acl = -Rf / Ri
    ze, zo = opamp_z(Aol, Zin, Zout, Rf, Ri, 'I'); close(ze, Ri, 5e-3); close(zo, zout, 1e-2)
    return [('Zin(I) ≈ Ri', si(Ri, 'Ω', 3)), ('Attenuation B = Ri/(Ri + Rf)', g(B, 3)), ('Zout(I) = Zout/(1 + Aol·B)', si(zout, 'Ω', 3)), ('Acl(I) = −Rf/Ri', g(acl, 4))], 'Same method as Example 12–7 with Ri = 560 Ω and Rf = 82 kΩ.', [f'Exact nodal solution: Zin = {si(ze, "Ω", 4)}, Zout = {si(zo, "Ω", 3)}.'], None, C1228
def bw_exact(Aol0, fT, Rf, Ri, mode):
    """-3 dB frequency (relative to the low-frequency closed-loop gain) of a single-pole op-amp, by solving |A(f)| = A(0)/sqrt(2) on the exact closed-loop response."""
    from scipy.optimize import brentq
    fc = fT / Aol0
    def acl(f):
        a = Aol0 / (1 + 1j * f / fc)
        if mode == 'NI': B = Ri / (Ri + Rf); return a / (1 + a * B)
        B = Ri / (Ri + Rf); return -(a * Rf / (Ri + Rf)) / (1 + a * B)         # inverting: -a·Rf/(Ri + Rf) / (1 + a·B)
    a0 = abs(acl(0.0)); return brentq(lambda f: abs(acl(f)) - a0 / math.sqrt(2), 1.0, 1e9)
@solve(F, 'example', 12, '12–12')
def _():
    fT, Aol_dB = 3e6, 100.0; Aol = 10 ** (Aol_dB / 20); a = 1 + 220e3 / 3.3e3; b = 47e3 / 1.0e3; bwa, bwb = fT / a, fT / b
    must_near('EXAMPLE 12–12', ['67.7', '44.3 kHz', '63.8 kHz', '-47'])
    ea, eb = bw_exact(Aol, fT, 220e3, 3.3e3, 'NI'), bw_exact(Aol, fT, 47e3, 1.0e3, 'I'); close(ea, bwa, 5e-3); close(eb, bwb, 3e-2)
    return [('(a) Acl and BW = fT/Acl', f'{g(a, 3)}; {si(bwa, "Hz", 3)}'), ('(b) |Acl| and BW = fT/|Acl|', f'{g(b, 3)}; {si(bwb, "Hz", 3)}')], 'BW(cl) = fT/|Acl| (Floyd Eq. 12–23): (a) Acl = 1 + 220 kΩ/3.3 kΩ = 67.7, (b) Acl = −47 kΩ/1.0 kΩ = −47. The book prints 44.3 kHz and 63.8 kHz.', [f'An exact single-pole solution gives {si(ea, "Hz", 3)} and {si(eb, "Hz", 3)} (the inverting amplifier\'s loop attenuation is 1/48 rather than 1/47, so the textbook value is about 2 % high).'], None, C1243
@solve(F, 'related_problem', 12, '12–12')
def _():
    fT, Aol_dB = 2e6, 90.0; Aol = 10 ** (Aol_dB / 20); a = 1 + 220e3 / 3.3e3; b = 47e3 / 1.0e3; bwa, bwb = fT / a, fT / b
    ea, eb = bw_exact(Aol, fT, 220e3, 3.3e3, 'NI'), bw_exact(Aol, fT, 47e3, 1.0e3, 'I'); close(ea, bwa, 5e-3); close(eb, bwb, 3e-2)
    return [('(a) BW = fT/Acl', f'{si(bwa, "Hz", 3)} (Acl = {g(a, 3)})'), ('(b) BW = fT/|Acl|', f'{si(bwb, "Hz", 3)} (|Acl| = {g(b, 3)})')], 'Same amplifiers as Example 12–12 (Figure 12–43) with fT = 2 MHz; BW = fT/|Acl|. The open-loop gain (90 dB) only needs to exceed the closed-loop gain.', [f'Exact single-pole solution: {si(ea, "Hz", 3)} and {si(eb, "Hz", 3)}.'], None, C1243
@solve(F, 'circuit_action', 12, '5')
def _():
    Ri = 1.0e3; B0, B1 = Ri / (Ri + 100e3), Ri / (Ri + 68e3); assert B1 > B0
    return [('Feedback attenuation B = Ri/(Ri + Rf): 100 kΩ → 68 kΩ', f'B = {g(B0, 3)} → {g(B1, 3)}: (a) increase')], 'B = Ri/(Ri + Rf) with Ri = 1.0 kΩ: a smaller Rf makes the divider ratio larger (0.0099 → 0.0145).', [], None, C1228
C1269 = 'Figure 12–69 (p.659): three voltage followers (output connected to the − input, signal on the + input). (a) Aol = 220,000, Zin = 6 MΩ, Zout = 100 Ω; (b) Aol = 100,000, Zin = 5 MΩ, Zout = 60 Ω; (c) Aol = 50,000, Zin = 800 kΩ, Zout = 75 Ω.'
@solve(F, 'problem', 12, '20')
def _():
    parts = []
    for tag, Aol, Zin, Zout in (('(a)', 220000.0, 6e6, 100.0), ('(b)', 100000.0, 5e6, 60.0), ('(c)', 50000.0, 800e3, 75.0)):
        zi, zo = (1 + Aol) * Zin, Zout / (1 + Aol)                            # voltage follower: B = 1 (Floyd §12–5)
        ze, zx = opamp_z(Aol, Zin, Zout, 0.0, float('inf'), 'VF'); close(ze, zi, 1e-6); close(zx, zo, 1e-3)
        parts.append((f'{tag} Zin(VF) = (1 + Aol)·Zin;  Zout(VF) = Zout/(1 + Aol)', f'{si(zi, "Ω", 3)};  {si(zo, "Ω", 3)}'))
    return parts, 'Voltage follower: the feedback attenuation is B = 1, so Zin(VF) = (1 + Aol)·Zin and Zout(VF) = Zout/(1 + Aol) (Floyd §12–5, Eq. 12–17 and 12–18). Problem 19 asks the same for the noninverting amplifiers of Figure 12–68 (its printed answers 8.41 GΩ / 89.2 mΩ … follow the same formula).', ['An exact KCL solution of the op-amp model agrees with the formulas to better than 0.1 %.'], None, C1269
C1275 = 'Figure 12–75 (p.662): inverting amplifier, R1 = 1.0 kΩ from the input to the − input, R2 = 10 kΩ from the output to the − input, R3 = 910 Ω from the + input to ground (bias-current compensation).'
@solve(F, 'problem', 12, '42')
def _():
    R1, R2, R3 = 1.0e3, 10e3, 910.0; Ib = 80e-9; vin = 0.1                                      # Ib: LM741 typical input bias current (Figure 12–77)
    def vout_dc(R3_, R1_=R1, R2_=R2):                                                                    # exact: the same Ib flows out of both inputs, Vin = 0
        A = np.array([[1 / R1_ + 1 / R2_, -1 / R2_], [-1e9 / 1.0, 1.0]]); b = np.array([-Ib, 1e9 * (-Ib * R3_)])       # node V-: Ib leaves it; op-amp with Aol = 1e9: Vo = Aol·(V+ − V-), V+ = −Ib·R3
        A[1, 0] = 1e9; A[1, 1] = 1.0; b[1] = 1e9 * (-Ib * R3_); return float(np.linalg.solve(A, b)[1])
    off_ok, off_bad = vout_dc(R3), vout_dc(10e3); close(off_bad, Ib * (R2 - 10e3 * (1 + R2 / R1)), 1e-3); close(off_ok, Ib * (R2 - R3 * (1 + R2 / R1)), 1e-3, 1e-9)
    Zo = 75.0; vo_a = vin * Zo / (R1 * (1 + 2e5) + Zo)                                                   # (a) Aol = 200,000: output tied to the − input
    gain_ok, gain_sw = -R2 / R1, -R1 / R2
    return [('(a) output pin shorted to the − input', f'Vout ≈ 0 V (≈ {g(vo_a * 1e9, 2)} nV for Vin = 100 mV, Aol = 200,000, Zout = 75 Ω): the op-amp holds the − input at the + input voltage (0 V) and sinks the source current Vin/R1 = {g(vin / R1 * 1e3, 2)} mA; no signal at the output'),
            ('(b) R3 open', 'The + input has no dc path: its bias current charges the stray capacitance until the output drives into saturation at one supply rail; the ac gain (−10) is not available'),
            ('(c) R3 = 10 kΩ instead of 910 Ω', f'Gain unchanged (−10); a dc offset appears: Vout(dc) = Ib·[R2 − R3(1 + R2/R1)] = {g(off_bad * 1e3, 3)} mV for Ib = 80 nA (instead of {g(off_ok * 1e6, 2)} μV with 910 Ω)'),
            ('(d) R1 and R2 swapped', f'Gain becomes −R2/R1 = −1.0 kΩ/10 kΩ = {g(gain_sw, 2)} instead of {g(gain_ok, 3)}: the output is 100 times smaller (still inverted); 100 mV in gives {g(gain_sw * 100, 3)} mV')], \
        'Inverting amplifier with bias compensation (R3 ≈ R1 ‖ R2 = 909 Ω). Effects obtained from the ideal gain −R2/R1 and from the dc error of the input bias current, Vout(dc) = Ib·[R2 − R3(1 + R2/R1)] (exact nodal solution used as check).', \
        ['Ib = 80 nA is the typical LM741 value of Figure 12–77 (an assumption: the statement gives no op-amp); both inputs are taken to draw the same bias current.', 'The statement gives no input signal for this problem; Problem 41 uses 100 mV, which is used here only for the numbers of (a) and (d).'], None, C1275
@solve(F, 'problem', 12, '48')
def _():
    Rf, A = 100e3, 100.0; Ri = Rf / A; Aol, Zin_op, Zout_op = 200000.0, 2e6, 75.0                      # LM741 typical column of Figure 12–77: Aol 200 V/mV, input resistance 2.0 MΩ
    ze, _zo = opamp_z(Aol, Zin_op, Zout_op, Rf, Ri, 'I'); close(ze, Ri, 1e-3)                                            # exact KCL solution: the source sees 1.0 kΩ
    B = Ri / (Ri + Rf); zin_inv_amp = Ri
    return [('Ri for |Acl| = 100 with Rf = 100 kΩ', si(Ri, 'Ω', 3)), ('Zin(I) of the amplifier ≈ Ri', si(zin_inv_amp, 'Ω', 3))], f'Inverting amplifier: Ri = Rf/|Acl| = 1.0 kΩ and Zin(I) ≈ Ri (Floyd §12–5). The LM741 typical input resistance (2.0 MΩ, datasheet Figure 12–77) only matters for the noninverting configuration, where Zin(NI) = (1 + Aol·B)·Zin.', [f'Exact KCL solution with Aol = 200,000 and Zin = 2 MΩ gives {si(ze, "Ω", 4)}, i.e. Ri to 0.1 %.', 'The statement says “input impedances” (plural); the only input impedance of the inverting amplifier is Zin(I) ≈ Ri.'], None, 'Figure 12–77 (p.664): partial LM741 datasheet, “LM741” column, typical values: input resistance 2.0 MΩ, large-signal voltage gain 200 V/mV (200,000), slew rate 0.5 V/μs, input bias current 80 nA.'
@solve(F, 'problem', 12, '50')
def _():
    SR = 0.5e6; dV = 16.0; t = dV / SR; v = -8.0; n = 0
    while v < 8.0: v += SR * 1e-8; n += 1                                                                        # independent: step the output at the slew rate
    close(n * 1e-8, t, 1e-3)
    return [('Time for a −8 V → +8 V step at the slew rate', f'{g(t * 1e6, 3)} μs')], 'Slew rate = ΔVout/Δt, so Δt = 16 V/(0.5 V/μs) = 32 μs (typical LM741 slew rate, Figure 12–77, unity gain).', ['Slew-rate limited transition; the rise time of the small-signal response (0.3 μs typ) is much shorter.'], None, 'Figure 12–77 (p.664): partial LM741 datasheet; LM741 column, typical slew rate 0.5 V/μs (TA = 25 °C, unity gain).'

# ============================================================================================ Chapter 13 (m03)
def summer(Rs, Vs, Rf, Aol=1e9):
    """Inverting summing amplifier solved by KCL at the summing junction (finite Aol): Vout for inputs Vs through Rs, feedback Rf."""
    g_in = sum(1 / r for r in Rs if r != float('inf')); I = sum(v / r for v, r in zip(Vs, Rs) if r != float('inf'))
    M = np.array([[g_in + 1 / Rf, -1 / Rf], [-Aol, 1.0]]); return float(np.linalg.solve(M, np.array([I, 0.0]))[1])
def schmitt_sweep(R1, R2, Vo=None, Vb=None):
    """Trigger points of an inverting comparator with positive feedback by sweeping the input up and down (state machine): V+ = Vout·R2/(R1 + R2).
    Vo: the output simply saturates at ±Vo.  Vb (zener bounding between the output and the − input, Figure 13–13): Vout = Vin ± Vb while the zeners conduct."""
    def vplus(vin, s): return (s * Vo if Vb is None else vin + s * Vb) * R2 / (R1 + R2)
    up = None; s = -1
    for vin in np.arange(-15, 15, 1e-4):
        if s < 0 and vin > vplus(vin, s) and (Vb is not None or True):
            if vin > vplus(vin, +1) * 0 + vplus(vin, s): pass
        # the output is positive while Vin is below V+; it switches negative when Vin exceeds V+ (inverting comparator)
    s = +1; ut = lt = None
    for vin in np.arange(-15, 15, 1e-4):
        if s > 0 and vin > vplus(vin, s): ut = vin; s = -1; break
    for vin in np.arange(15, -15, -1e-4):
        if s < 0 and vin < vplus(vin, s): lt = vin; s = +1; break
    return ut, lt
C133 = 'Figure 13–3 (p.670): (a) a sine wave Vin of 5 V peak (−5 V to +5 V); (b) an op-amp comparator with Vin on the + input and the reference on the − input, taken from a divider between +15 V and ground: R1 = 8.2 kΩ (from +15 V) and R2 = 1.0 kΩ (to ground).'
@solve(F, 'example', 13, '13–1')
def _():
    R1, R2, V, Vm, Vout = 8.2e3, 1.0e3, 15.0, 5.0, 14.0; Vref = V * R2 / (R1 + R2); must_near('EXAMPLE 13–1', ['1.63 V', '+14 V']); close(Vref, 1.63, 3e-3)
    t = np.linspace(0, 1, 400001)[:-1]; duty = float(np.mean(Vm * np.sin(2 * math.pi * t) > Vref)); close(duty, (math.pi - 2 * math.asin(Vref / Vm)) / (2 * math.pi), 2e-3)    # independent: sample the sine wave
    return [('Reference voltage VREF = R2/(R1 + R2)·(+15 V)', f'{g(Vref, 3)} V'), ('Output', f'+{g(Vout, 2)} V whenever Vin > {g(Vref, 3)} V and −{g(Vout, 2)} V whenever Vin < {g(Vref, 3)} V: a rectangular wave that is high for {g(100 * duty, 3)} % of each cycle of the ±5 V sine (switching at {g(math.degrees(math.asin(Vref / Vm)), 3)}° and {g(180 - math.degrees(math.asin(Vref / Vm)), 4)}°)')], \
        'Zero-level detector shifted by the divider reference (Floyd §13–1); the output switches between the saturated levels ±14 V each time Vin crosses VREF. The book prints VREF = 1.63 V and draws the output in Figure 13–4.', ['The duty cycle (39 %) is derived here; the book only draws the waveform.'], None, C133
@solve(F, 'related_problem', 13, '13–1')
def _():
    R1, R2, V = 22e3, 3.3e3, 15.0; Vref = V * R2 / (R1 + R2); close(Vref, np.linalg.solve(np.array([[1 / R1 + 1 / R2]]), np.array([V / R1]))[0], 1e-12)      # nodal solution of the divider
    return [('Reference voltage VREF = R2/(R1 + R2)·(+15 V)', f'{g(Vref, 3)} V')], 'Same divider as Figure 13–3(b) with R1 = 22 kΩ and R2 = 3.3 kΩ.', [], None, C133
C139 = 'Figure 13–9 (p.673): comparator with positive feedback (Floyd Fig. 13–7 arrangement): Vin on the − input, R1 from the output to the + input, R2 from the + input to ground; in Example 13–2 R1 = R2 = 100 kΩ.'
@solve(F, 'example', 13, '13–2')
def _():
    R1, R2, Vo = 100e3, 100e3, 5.0; utp = R2 / (R1 + R2) * Vo; ltp = -utp; must_near('EXAMPLE 13–2', ['+2.5 V', '−2.5 V']); u, l = schmitt_sweep(R1, R2, Vo=Vo); close(u, utp, 1e-3); close(l, ltp, 1e-3)
    return [('VUTP = R2/(R1 + R2)·(+Vout(max))', f'{g(utp, 3)} V'), ('VLTP = R2/(R1 + R2)·(−Vout(max))', f'{g(ltp, 3)} V')], 'Floyd Eq. 13–1/13–2; swept the input up and down in a state machine to find the switching points (independent check).', [], None, C139
@solve(F, 'related_problem', 13, '13–2')
def _():
    R1, R2, Vo = 68e3, 82e3, 7.0; utp = R2 / (R1 + R2) * Vo; ltp = -utp; u, l = schmitt_sweep(R1, R2, Vo=Vo); close(u, utp, 1e-3); close(l, ltp, 1e-3)
    return [('VUTP', f'{g(utp, 3)} V'), ('VLTP', f'{g(ltp, 3)} V'), ('Hysteresis VHYS = VUTP − VLTP', f'{g(utp - ltp, 3)} V')], 'Same circuit as Figure 13–9 with R1 = 68 kΩ, R2 = 82 kΩ and ±7 V output levels.', [], None, C139
C1313 = 'Figure 13–13 (p.675): comparator with hysteresis and zener bounding: Vin (a ±5 V sine) through Ri to the − input; D1 and D2, two zener diodes in series (4.7 V each in the book example), between the − input and the output; R1 = 100 kΩ from the output to the + input and R2 = 47 kΩ from the + input to ground. One zener is always forward biased (0.7 V) while the other is in breakdown.'
@solve(F, 'related_problem', 13, '13–3')
def _():
    R1, R2, Vz = 150e3, 68e3, 3.3; Vb = Vz + 0.7; Vout = Vb * (R1 + R2) / R1; utp = Vout * R2 / (R1 + R2); ltp = -utp
    R1b, R2b, Vzb = 100e3, 47e3, 4.7; Vbb = Vzb + 0.7; close(Vbb * (R1b + R2b) / R1b, 7.94, 2e-3); close(Vbb * R2b / R1b, 2.54, 2e-3)          # Example 13–3 as printed: ±7.94 V and ±2.54 V
    u, l = schmitt_sweep(R1, R2, Vb=Vb); close(u, utp, 1e-3); close(l, ltp, 1e-3)
    return [('Voltage across the zener pair Vb = VZ + 0.7 V', f'{g(Vb, 3)} V'), ('Output levels Vout = Vb(R1 + R2)/R1', f'±{g(Vout, 3)} V'), ('VUTP = R2/(R1 + R2)·(+Vout) = Vb·R2/R1', f'{g(utp, 3)} V'), ('VLTP', f'{g(ltp, 3)} V')], \
        'Example 13–3 method: the − input stands at Vout ∓ Vb and equals the + input voltage, so Vout − Vb = Vout·R2/(R1 + R2); hence Vout = Vb(R1 + R2)/R1 and VUTP = Vb·R2/R1. The same formulas give the book\'s ±7.94 V and ±2.54 V for 4.7 V zeners, 100 kΩ and 47 kΩ.', [], None, C1313
@solve(F, 'example', 13, '13–4')
def _():
    VREF, n = 8.0, 3; samples = [3.7, 5.2, 6.2, 6.6, 4.7, 1.7, 0.6, 1.0, 2.7, 5.0, 6.6, 7.2]; want = '011, 101, 110, 110, 100, 001, 000, 001, 010, 101, 110, 111'
    must_near('EXAMPLE 13–4', [want])
    # ladder of 8 equal resistors (7 comparators at k·VREF/8), comparators on at Vin >= level, priority encoder = highest comparator that is on
    nodes = [VREF * k / 2 ** n for k in range(1, 2 ** n)]; code = lambda v: max([k for k, lv in enumerate(nodes, 1) if v >= lv - 1e-9] or [0])
    seq = [format(code(v), '03b') for v in samples]; assert ', '.join(seq) == want, seq
    chk = [format(min(int(v // (VREF / 2 ** n)), 2 ** n - 1), '03b') for v in samples]; assert chk == seq                    # independent: plain quantisation floor(Vin/LSB)
    return [('Comparator references (R-ladder, 8 equal resistors, VREF = 8 V)', ', '.join(f'{g(v, 3)} V' for v in nodes)), ('Binary output sequence (D2 D1 D0) for the 12 samples', want)], \
        'A flash ADC with a ladder of 8 equal resistors: comparator k switches on when Vin exceeds k·VREF/8; the priority encoder outputs the number of the highest comparator that is on, i.e. floor(Vin/LSB). With VREF = 8 V the LSB is 1 V.', \
        ['The 12 sample values (3.7, 5.2, 6.2, 6.6, 4.7, 1.7, 0.6, 1.0, 2.7, 5.0, 6.6, 7.2 V) are read from the dots of Figure 13–17 to about ±0.1 V; samples 8 and 10 lie on a comparator threshold, where the book\'s code (001 and 101) is used.', 'VREF = 8 V is implied by the 0–8 V axis of Figure 13–17 and the printed codes (not stated in the example).'], None, \
        'Figures 13–16 and 13–17 (pp.677–678): a three-digit simultaneous (flash) ADC: a resistor ladder of 8 equal resistors R from VREF to ground gives 7 reference voltages to 7 op-amp comparators (Vin on the + inputs); a priority encoder (inputs 1–7, enable input) outputs D2D1D0. Vin is an analog waveform between 0 and 8 V sampled by 12 enable pulses.'
@solve(F, 'related_problem', 13, '13–5')
def _():
    Vs = [3.0, 1.0, 8.0, -0.5]; v = summer([10e3] * 4, Vs, 10e3); close(v, -sum(Vs), 1e-6)
    return [('VOUT = −(VIN1 + VIN2 + VIN3 + VIN4)', f'{g(-sum(Vs), 4)} V')], 'All input resistors and Rf are 10 kΩ, so the gain is −1 for every input and the output is the inverted sum: −(3 + 1 + 8 − 0.5) V.', [], None, 'Figure 13–22 (p.680): inverting summing amplifier, three inputs VIN1 = +3 V, VIN2 = +1 V, VIN3 = +8 V, each through 10 kΩ to the − input, Rf = 10 kΩ, + input grounded. Book result −12 V.'
@solve(F, 'circuit_action', 13, '5')
def _():
    before = summer([10e3] * 3, [3.0, 1.0, 8.0], 10e3); after = summer([10e3] * 3, [3.0, -1.0, 8.0], 10e3); assert after > before
    return [('VOUT with VIN2 = +1 V → −1 V', f'{g(before, 3)} V → {g(after, 3)} V: (a) increase')], 'VOUT = −(VIN1 + VIN2 + VIN3): VIN2 falls from +1 V to −1 V, the sum falls from 12 V to 10 V and VOUT rises from −12 V to −10 V.', [], None, 'Figure 13–22 (p.680): inverting summing amplifier, VIN1 = +3 V, VIN2 = +1 V, VIN3 = +8 V, three 10 kΩ input resistors, Rf = 10 kΩ.'
@solve(F, 'related_problem', 13, '13–6')
def _():
    R, Rf, Vs = 2.2e3, 18e3, [0.2, 0.5]; v = summer([R, R], Vs, Rf); close(v, -Rf / R * sum(Vs), 1e-6)
    return [('Gain Rf/R', g(Rf / R, 4)), ('VOUT = −(Rf/R)(VIN1 + VIN2)', f'{g(v, 4)} V')], 'Figure 13–23 with VIN1 = 0.2 V and VIN2 = 0.5 V; R1 = R2 = 2.2 kΩ, Rf = 18 kΩ.', [], None, 'Figure 13–23 (p.681): summing amplifier with VIN1 = 0.2 V and VIN2 = 0.5 V through R1 = R2 = 1.0 kΩ to the − input, Rf = 10 kΩ, + input grounded (book result −7 V).'
@solve(F, 'circuit_action', 13, '7')
def _():
    R, Rf = 100e3, 25e3; before = summer([R] * 4, [1.0, 2.0, 3.0, 4.0], Rf); after = summer([R] * 4, [1.0, 2.0, -7.0, 4.0], Rf); assert after > before
    return [('VOUT with VIN3 = +3 V → −7 V', f'{g(before, 3)} V → {g(after, 3)} V: (a) increase')], 'Averaging amplifier, Rf/R = 1/4: VOUT = −(1/4)(VIN1 + VIN2 + VIN3 + VIN4); the sum drops from 10 V to 0 V, so VOUT goes from −2.5 V to 0 V.', [], None, 'Figure 13–24 (p.682): averaging amplifier, four inputs VIN1…VIN4 = +1, +2, +3, +4 V each through 100 kΩ to the − input, Rf = 25 kΩ, + input grounded (book result −2.5 V).'
@solve(F, 'related_problem', 13, '13–8')
def _():
    R, Rf, Vs = [22e3, 82e3, 56e3], 10e3, [3.0, 2.0, 8.0]; w = [Rf / r for r in R]; v = summer(R, Vs, Rf); close(v, -sum(a * b for a, b in zip(w, Vs)), 1e-6)
    return [('Weights Rf/R1, Rf/R2, Rf/R3', ', '.join(g(x, 3) for x in w)), ('VOUT = −(w1·VIN1 + w2·VIN2 + w3·VIN3)', f'{g(v, 4)} V')], 'Scaling adder: the weight of each input is Rf/Rk; the inputs of Example 13–8 are +3 V, +2 V and +8 V (Figure 13–25).', [], None, 'Figure 13–25 (p.683): scaling adder, VIN1 = +3 V through R1, VIN2 = +2 V through R2, VIN3 = +8 V through R3, Rf = 10 kΩ; in Example 13–8 R1 = 47 kΩ, R2 = 100 kΩ, R3 = 10 kΩ (VOUT = −8.84 V).'
C1327 = 'Figure 13–27 (p.684): four-digit binary-weighted DAC (scaling adder): input resistors D0 = 200 kΩ, D1 = 100 kΩ, D2 = 50 kΩ, D3 = 25 kΩ to the − input, Rf = 10 kΩ, + input grounded; a binary 1 is +5 V and a 0 is 0 V. The input waveforms D0…D3 form the straight binary count 0000 to 1111.'
@solve(F, 'example', 13, '13–9')
def _():
    R, Rf = [200e3, 100e3, 50e3, 25e3], 10e3; must_near('EXAMPLE 13–9', ['−0.25 V', '−0.5 V', '−1 V', '−2 V', '−3.75 V'], span=7000)
    outs = []
    for n in range(16):
        bits = [(n >> k) & 1 for k in range(4)]; v = summer(R, [5.0 * b for b in bits], Rf); outs.append(v); close(v, -sum(5.0 * b * Rf / r for b, r in zip(bits, R)), 1e-6)
    steps = np.diff(outs); close(float(steps.min()), -0.25, 1e-6); close(float(steps.max()), -0.25, 1e-6); close(outs[-1], -3.75, 1e-6)
    return [('Contribution of each bit (D0, D1, D2, D3) = −Rf·5 V/Rk', '−0.25 V, −0.5 V, −1 V, −2 V'), ('Output for the count 0000 → 1111', f'a staircase from 0 V to {g(outs[-1], 3)} V in steps of {g(steps[0], 3)} V')], \
        'Binary-weighted scaling adder: the − input is a virtual ground, so each 1 sends 5 V/Rk through Rf (Floyd §13–2). The book prints −0.25, −0.5, −1, −2 V per bit and the 0 to −3.75 V staircase (Figure 13–28).', ['All 16 codes were also solved by KCL with a finite open-loop gain.'], None, C1327
@solve(F, 'related_problem', 13, '13–9')
def _():
    Rf = 10e3; base = [200e3, 100e3, 50e3, 25e3]; new = [400e3, 100e3, 50e3, 25e3]; V = 5.0
    outs = [summer(new, [V * ((n >> k) & 1) for k in range(4)], Rf) for n in range(16)]; steps = np.diff(outs)
    assert abs(outs[1] - (-0.125)) < 1e-6 and abs(outs[2] - (-0.5)) < 1e-6 and float(np.ptp(steps)) > 0.1                      # unchanged others: wrong weights, the staircase is no longer uniform
    fix = [400e3, 200e3, 100e3, 50e3]; o2 = [summer(fix, [V * ((n >> k) & 1) for k in range(4)], Rf) for n in range(16)]; s2 = np.diff(o2); close(float(s2.min()), -0.125, 1e-6); close(float(s2.max()), -0.125, 1e-6)
    o3 = [summer(fix, [V * ((n >> k) & 1) for k in range(4)], 2 * Rf) for n in range(16)]; s3 = np.diff(o3); close(float(s3.min()), -0.25, 1e-6)
    return [('Do the other resistors have to change?', 'Yes. Binary weighting needs R(D0) : R(D1) : R(D2) : R(D3) = 8 : 4 : 2 : 1, so with 400 kΩ for D0 the others must be 200 kΩ, 100 kΩ and 50 kΩ (all doubled)'), ('Effect of changing only D0 to 400 kΩ', f'D0 would count 1/4 as much as D1 instead of 1/2: code 0001 → {g(outs[1], 3)} V, 0010 → {g(outs[2], 3)} V, 0011 → {g(outs[3], 3)} V: the staircase is no longer uniform'),
            ('Output step after doubling all four input resistors (Rf = 10 kΩ)', f'−0.125 V per count (0 to −1.875 V); Rf = 20 kΩ restores −0.25 V per count (0 to −3.75 V)')], \
        'The weight of an input is Rf/Rk; for a binary DAC the weights must be in the ratio 1 : 2 : 4 : 8, so all the input resistors scale together (Floyd §13–2).', ['The statement does not say whether the original output step (−0.25 V) must be kept; both options are given.'], None, C1327
C1335 = 'Figure 13–35 (p.690): ideal integrator, Ri = 10 kΩ from the input to the − input, C = 0.01 μF from the output to the − input, + input grounded. Vin is a square wave between −2.5 V and +2.5 V; in the drawing each half-period is 200 μs.'
@solve(F, 'example', 13, '13–10')
def _():
    Ri, C, V = 10e3, 0.01e-6, 2.5; rate = V / (Ri * C); must_near('EXAMPLE 13–10', ['25 mV/μs', '200 μs', '5 V']); close(rate, 25e3, 1e-9)
    dt = 1e-7; t = np.arange(0, 800e-6, dt); vin = np.where((t // 200e-6) % 2 == 0, V, -V); vo = -np.cumsum(vin) * dt / (Ri * C); close(vo.min(), -5.0, 1e-2); close(vo[t > 400e-6].max(), 0.0, 1e-2, 1e-2)         # independent: step the integral
    return [('Rate of change of Vout, Vin = +2.5 V', f'{g(-rate * 1e-6 * 1e3, 3)} mV/μs (= −25 kV/s)'), ('Vin = −2.5 V', '+25 mV/μs'), ('(b) output waveform', 'a triangular wave between 0 V and −5 V (5 V peak-to-peak): a falling ramp while the input is +2.5 V and a rising ramp while it is −2.5 V; ΔVout = 25 mV/μs × 200 μs = 5 V')], \
        'Ideal integrator: ΔVout/Δt = −Vin/(Ri·C) = −2.5 V/(10 kΩ × 0.01 μF) = −25 mV/μs (Floyd §13–3).', \
        ['BOOK INCONSISTENCY: the statement says “the pulse width is 100 μs”, but Figure 13–35(b) and the printed solution use 200 μs per half-period (ΔVout = 25 mV/μs × 200 μs = 5 V). With literally 100 μs the output would swing only 2.5 V.'], None, C1335
@solve(F, 'related_problem', 13, '13–10')
def _():
    Ri, V, dV, dt = 10e3, 2.5, 5.0, 100e-6; C = V * dt / (Ri * dV); close(C, 5e-9, 1e-9)
    step = 1e-8; t = np.arange(0, dt, step); vo = -np.cumsum(np.full_like(t, V)) * step / (Ri * C); close(vo[-1], -dV, 1e-3)                              # independent: step the integral
    return [('C for 0 → −5 V in 100 μs with Ri = 10 kΩ, Vin = 2.5 V', f'{si(C, "F", 3)} = 0.005 μF'), ('Alternative: keep C = 0.01 μF', f'Ri = {si(V * dt / (0.01e-6 * dV), "Ω", 3)}')], 'The slope must be 5 V/100 μs = 50 mV/μs = Vin/(Ri·C), so Ri·C = 2.5 V/(50 mV/μs) = 50 μs: halve the time constant (C = 5 nF with Ri = 10 kΩ, or Ri = 5 kΩ with C = 0.01 μF).', [], None, C1335
C1340 = 'Figure 13–40 (p.692): ideal op-amp differentiator, C = 0.001 μF in series with the input to the − input, Rf = 2.2 kΩ from the output to the − input, + input grounded. Vin is a triangular wave between −5 V and +5 V, 5 μs per ramp (10 μs period).'
@solve(F, 'related_problem', 13, '13–11')
def _():
    C, Rf, dV, dt = 0.001e-6, 3.3e3, 10.0, 5e-6; slope = dV / dt; Vout = -Rf * C * slope
    t = np.linspace(0, 20e-6, 2000001); vin = 5 - 10 * np.abs(((t / 10e-6) % 1) * 2 - 1) * 0 + 0 * t; tri = -5 + 10 * (1 - np.abs(1 - 2 * ((t / 10e-6) % 1))); vd = -Rf * C * np.gradient(tri, t)
    close(float(vd[(t > 1e-6) & (t < 4e-6)].mean()), Vout, 1e-3); close(float(vd[(t > 6e-6) & (t < 9e-6)].mean()), -Vout, 1e-3)                         # independent: differentiate the sampled triangle
    return [('Time constant Rf·C', f'{g(Rf * C * 1e6, 3)} μs'), ('Slope of Vin', f'±{g(slope * 1e-6, 3)} V/μs'), ('Vout during the rising ramp / falling ramp', f'{g(Vout, 3)} V / +{g(-Vout, 3)} V (a square wave)')], 'Differentiator: Vout = −Rf·C·(ΔVin/Δt) = −(3.3 μs)(2 V/μs) = −6.6 V on the rising ramp (the book gets −4.4 V for Rf = 2.2 kΩ).', [], None, C1340
@solve(F, 'related_problem', 13, '13–13')
def _():
    R5, R, Vs = 47e3, 10e3, [1.0, 0.5, 0.2, 0.1]; v = summer([float('inf'), R, R, R], Vs, R5); close(v, -R5 / R * (0.5 + 0.2 + 0.1), 1e-6)
    return [('VOUT = −(Rf/R)(VIN2 + VIN3 + VIN4), R1 open', f'{g(v, 3)} V')], 'With R1 open the 1 V input is disconnected; the remaining inputs are amplified by −Rf/R = −47 kΩ/10 kΩ = −4.7.', [], None, 'Figure 13–47 (p.697): summing amplifier, four inputs VIN1 = 1 V, VIN2 = 0.5 V, VIN3 = 0.2 V, VIN4 = 0.1 V, each through 10 kΩ (R1…R4) to the − input, feedback R5 = 10 kΩ in the book example (−1.8 V).'
C1371 = 'Figure 13–71 (p.715): (b) a comparator with hysteresis and zener bounding (Figure 13–13 type): input A through Ri = 100 kΩ to the − input, two 4.3 V zeners D1 and D2 in series between the − input (node) and the output B, R1 = 10 kΩ from B to the + input (node C) and R2 = 10 kΩ from C to ground. (a) the observed waveforms: VA a ±6 V sine; VB switches between +10 V and −1.4 V; VC between +5 V and −0.7 V; the output switches high when VA falls to −0.7 V and low when VA reaches +5 V.'
@solve(F, 'problem', 13, '20')
def _():
    R1, R2, Vz = 10e3, 10e3, 4.3; Vb = Vz + 0.7; Vout = Vb * (R1 + R2) / R1; utp = Vb * R2 / R1; ltp = -utp
    close(Vout, 10.0, 1e-9); close(utp, 5.0, 1e-9)                                              # the positive half of the observation (+10 V, +5 V) is what a healthy circuit gives
    Vb_f = 0.7; vout_f = Vb_f * (R1 + R2) / R1; ltp_f = -Vb_f * R2 / R1; close(vout_f, 1.4, 1e-9); close(ltp_f, -0.7, 1e-9)                    # one zener shorted: only one 0.7 V junction drop in the negative state
    u, l = schmitt_sweep(R1, R2, Vb=Vb); close(u, utp, 1e-3); close(l, ltp, 1e-3)
    return [('Healthy circuit (zener pair drop Vb = 4.3 + 0.7 = 5.0 V)', f'Vout = ±{g(Vout, 3)} V, VC = ±{g(utp, 3)} V: it should switch between +10 V and −10 V with trigger points ±5 V'), ('Observed', 'VB = +10 V / −1.4 V and VC = +5 V / −0.7 V: the positive half is correct, the negative half is not'), ('Is it operating properly?', 'No'),
            ('Likely fault', f'One of the zener diodes is shorted (the one that should be in breakdown when the output is negative): the negative output is then limited by a single 0.7 V junction, giving Vb = 0.7 V, Vout = −2·0.7 = {g(-vout_f, 3)} V and VC = −0.7 V, exactly the observed values')], \
        'Zener-bounded comparator with hysteresis (Example 13–3): Vout = ±Vb(R1 + R2)/R1 and VUTP/VLTP = ±Vb·R2/R1 with Vb = VZ + 0.7 V. The observed negative levels fit Vb = 0.7 V, i.e. one zener replaced by a short.', ['An open zener would stop the output from switching to that level at all; the observation shows a limited negative level, so a short is more consistent.'], None, C1371
@solve(F, 'problem', 13, '26')
def _():
    R2, R3, V = 500e3, 56e3, 12.0; Vp = 10.0
    def rng(R1): I = 2 * V / (R1 + R2 + R3); return V - I * R1, -V + I * R3                      # reference at the top and at the bottom of the potentiometer
    top0, bot0 = rng(56e3); top1, bot1 = rng(1.0e3); close(top0, 9.80, 2e-3); close(bot0, -9.80, 2e-3)
    t = np.linspace(0, 1, 400001)[:-1]; sin = Vp * np.sin(2 * math.pi * t); d = lambda vr: float(np.mean(sin > vr))
    close(d(top0) * 100, 6.39, 1.5e-2); close(d(bot0) * 100, 93.6, 5e-3)                                                    # printed answer of Problem 27 (min 6.39 %, max 93.6 %): the figure was read correctly
    I1 = 2 * V / (1e3 + R2 + R3); dead = (2.0 / I1 - 1e3) / R2                                                              # part of the potentiometer travel where the reference is above 10 V (the sine never exceeds it)
    return [('Reference range with R1 = R3 = 56 kΩ (as drawn)', f'{g(bot0, 3)} V … +{g(top0, 3)} V (duty cycle {g(100 * d(top0), 3)} % … {g(100 * d(bot0), 3)} %)'), ('Reference range with R1 = 1.0 kΩ', f'{g(bot1, 4)} V … +{g(top1, 4)} V'),
            ('Effect on the duty cycle (10 V peak sine)', f'minimum {g(100 * d(top1), 3)} % (the reference exceeds the 10 V peak, so over the top {g(100 * dead, 3)} % of the potentiometer travel the output never goes high), maximum {g(100 * d(bot1), 3)} % instead of {g(100 * d(bot0), 3)} %: the range is no longer symmetrical and part of the control is wasted')], \
        'Reference voltage = +12 V − I·(R1 + x·R2) with I = 24 V/(R1 + R2 + R3); the pulse is high while the sine exceeds the reference, duty = (π − 2·asin(Vref/Vp))/(2π). The 10 V peak sine of Problem 27 is used (Application Activity text).', ['The effect is derived here (the book gives no answer for this even-numbered problem); the duty cycles are computed by sampling the sine wave.'], None, \
        'Figure 13–50 (p.700): sine/pulse generator: a 10 V peak sine wave goes to the + input of an LM111 comparator; the − input is the wiper of a 500 kΩ potentiometer R2 between R1 = 56 kΩ (to +12 V) and R3 = 56 kΩ (to −12 V); output pulled up to +5 V by R4 = 1 kΩ.'
@solve(F, 'problem', 13, '28')
def _():
    R2, V, Vp = 500e3, 12.0, 5.0; I0 = 2 * V / (56e3 + R2 + 56e3); frac = (V - I0 * 56e3) / 10.0; Vtarget = frac * Vp                                    # original: reference ±9.80 V for a 10 V peak sine (98.0 %)
    from scipy.optimize import brentq
    R1 = brentq(lambda R1: V - 2 * V * R1 / (R1 + R2 + R1) - Vtarget, 1e3, 5e6); Rstd = 360e3; I = 2 * V / (2 * Rstd + R2); top = V - I * Rstd
    t = np.linspace(0, 1, 400001)[:-1]; sin = Vp * np.sin(2 * math.pi * t); d = lambda vr: float(np.mean(sin > vr)); dmin, dmax = d(top), d(-top)
    I1 = 2 * V / (2 * R1 + R2); close(d(V - I1 * R1) * 100, 6.31, 5e-3)                                                                                       # exact design reproduces the original duty range (6.3 %)
    return [('Required reference range (same 98 % of the sine peak as the original)', f'±{g(Vtarget, 3)} V'), ('R1 = R3 for that range (R2 = 500 kΩ, ±12 V supplies)', f'{si(R1, "Ω", 3)} (standard value 360 kΩ gives ±{g(top, 3)} V and a duty-cycle range of {g(100 * dmin, 3)} % … {g(100 * dmax, 3)} %)')], \
        'The reference at the ends of the potentiometer is ±(12 V − I·R1) with I = 24 V/(2R1 + R2). The original design (R1 = 56 kΩ) gives ±9.8 V for a 10 V peak sine (duty 6.4 %–93.6 %); for a 5 V peak sine the same fractions need ±4.9 V.', \
        ['A design problem: the book prints no answer. Assumed: the pot R2 = 500 kΩ and the ±12 V supplies stay, only R1 = R3 change, and the duty range of the original design is kept (the pulse spec of Table 13–1 is 15 %–85 %, which any R1 above this value also meets).', 'Another valid design would change R2 or the supply instead.'], None, \
        'Figure 13–50 (p.700): sine/pulse generator: 10 V peak sine on the + input of an LM111; − input from the wiper of a 500 kΩ potentiometer R2 between R1 = 56 kΩ (to +12 V) and R3 = 56 kΩ (to −12 V); R4 = 1 kΩ pull-up to +5 V.'

# ============================================================================================ Chapter 14 (m05)
PDF_FLOYD = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'pdf_ocr_fixed', 'Floyd_Electronic_Devices_9e_fixed.pdf'))
def ad622_curves():
    """The four gain-vs-frequency curves of Floyd Figure 14–6 (AD622) read from the VECTOR drawing of the PDF page (PDF p.740): the four blue Bezier paths are converted with the
    log-log axes of the graph (x: 100 Hz at the left frame, 34.5 pt per decade; y: 1000 at the top frame, 4 decades over the frame height).  Returns {nominal gain: (f, gain)} arrays.
    The calibration is checked: the flat parts of the curves must come out at 1, 10, 100 and 1000 within 4 %."""
    import fitz
    page = fitz.open(PDF_FLOYD)[739]; X0, XW, Y0 = 359.5, 34.5, 319.5; D = (457.4 - Y0) / 4; tt = np.linspace(0, 1, 801)
    tof = lambda x: 100 * 10 ** ((x - X0) / XW); tog = lambda y: 10 ** (3 - (y - Y0) / D)
    def bez(p):
        P = np.array([[q.x, q.y] for q in p]); return ((1 - tt) ** 3)[:, None] * P[0] + (3 * (1 - tt) ** 2 * tt)[:, None] * P[1] + (3 * (1 - tt) * tt ** 2)[:, None] * P[2] + (tt ** 3)[:, None] * P[3]
    subs = []
    for d in page.get_drawings():
        if d.get('color') and tuple(round(c, 2) for c in d['color']) == (0.0, 0.68, 0.94) and d.get('width') == 0.5:
            cur = []; last = None
            for it in d['items']:
                seg = bez([it[1], it[2], it[3], it[4]]) if it[0] == 'c' else np.array([[it[1].x, it[1].y], [it[2].x, it[2].y]])
                if last is not None and np.hypot(*(seg[0] - last)) > 0.05: subs.append(np.vstack(cur)); cur = []
                cur.append(seg); last = seg[-1]
            subs.append(np.vstack(cur))
    out = {}
    for P in subs:
        f, g_ = tof(P[:, 0]), tog(P[:, 1]); o = np.argsort(f); f, g_ = f[o], g_[o]; flat = float(g_[f < 1000].mean()); nominal = min((1, 10, 100, 1000), key=lambda n: abs(math.log10(flat / n)))
        assert abs(flat / nominal - 1) < 0.04, (flat, nominal); out[nominal] = (f, g_)
    assert sorted(out) == [1, 10, 100, 1000]; return out
def ad622_bw(G):
    """-3 dB frequency of the AD622 curve of nominal gain G (first frequency above 20 kHz where the gain is below flat/√2), the frequency of its peak and the end of its flat part."""
    f, g_ = ad622_curves()[G]; flat = float(g_[f < 1000].mean()); i = np.where((g_ < flat / math.sqrt(2)) & (f > 20e3))[0][0]
    return float(f[i]), float(f[g_.argmax()]), float(f[np.where(g_ < 0.99 * flat)[0][0]]), float(g_.max())
C147 = 'Figures 14–7 and 14–6 (pp.722–723): AD622 instrumentation amplifier, supplies +15 V (pin 7) and −15 V (pin 4), inputs +IN (pin 3) and −IN (pin 2), gain resistor RG = 510 Ω between pins 1 and 8, REF pin 5, output pin 6. Gain: Av = 50.5 kΩ/RG + 1; Figure 14–6 is the graph of gain versus frequency of the AD622 for gains 1, 10, 100 and 1000.'
@solve(F, 'checkup', 14, '14–5.1')
def _():
    Vin, Ri = 6.8, 10e3; out = []
    for RL in (1e3, 5e3):
        Aol = 1e8; M = np.array([[1 / Ri + 1 / RL + 1e-9, -1 / RL], [-Aol, 1.0]]); vm_vo = np.linalg.solve(M, np.array([Vin / Ri, 0.0])); IL = (vm_vo[0] - vm_vo[1]) / RL; close(IL, Vin / Ri, 1e-4); out.append((RL, IL, vm_vo[1]))
    return [('IL = VIN/Ri for RL = 1.0 kΩ', f'{g(out[0][1] * 1e3, 3)} mA'), ('IL for RL = 5 kΩ', f'{g(out[1][1] * 1e3, 3)} mA (the same: IL does not depend on RL)')], 'Op-amp constant-current source: the − input is a virtual ground, so Ii = VIN/Ri flows through the load RL in the feedback path (Eq. 14–11): 6.8 V/10 kΩ = 0.68 mA.', [f'The output must reach {g(abs(out[1][2]), 3)} V for the 5 kΩ load, which a ±12 V to ±15 V supply allows (supplies are not given).'], None, 'Figure 14–36 (p.742): constant-current source: the input voltage VIN is applied through Ri to the − input, the + input is grounded and the load RL is connected in the feedback path between the output and the − input.'
@solve(F, 'example', 14, '14–2')
def _():
    RG = 510.0; Av = 50.5e3 / RG + 1; must_near('EXAMPLE 14–2', ['50.5 kΩ', '= 100', '80 kHz']); close(Av, 100, 1e-2)
    bw3, fpk, fdrop, gpk = ad622_bw(100); close(bw3, 112e3, 0.06)
    return [('Voltage gain Av = 50.5 kΩ/RG + 1', g(Av, 3)), ('Bandwidth from Figure 14–6 (gain 100 curve)', '≈ 80 kHz (the book\'s reading of the point where the curve begins to drop)')], 'AD622: Av = 50.5 kΩ/RG + 1 = 50.5 kΩ/510 Ω + 1 = 100 (Floyd Eq. 14–1). The gain-100 curve of Figure 14–6 is flat up to about 80 kHz and then falls.', \
        [f'Read from the vector drawing of Figure 14–6, the gain-100 curve stays flat to {g(fdrop / 1e3, 3)} kHz and is 3 dB down (gain 70.7) at {g(bw3 / 1e3, 3)} kHz; the book\'s 80 kHz lies between the two (it is a rough reading).'], None, C147
@solve(F, 'related_problem', 14, '14–2')
def _():
    Av_want = 45.0; RG = 50.5e3 / (Av_want - 1); near = [(r, 50.5e3 / r + 1) for r in (1.1e3, 1.2e3)]
    return [('RG = 50.5 kΩ/(Av − 1) for Av = 45', f'{si(RG, "Ω", 3)}'), ('Standard values', f'1.1 kΩ → Av = {g(near[0][1], 3)}; 1.2 kΩ → Av = {g(near[1][1], 3)} (either is “approximately 45”)')], 'Av = 50.5 kΩ/RG + 1, so RG = 50.5 kΩ/44 = 1.15 kΩ (printed answer to the similar Problem 7: for a gain of 24 “change RG to 2.2 kΩ”, 50.5 kΩ/23 = 2.20 kΩ).', [], None, C147
@solve(F, 'related_problem', 14, '14–4')
def _():
    Ri1, Rf1, Ri2, Rf2 = 2.2e3, 22e3, 10e3, 47e3; Av1 = Rf1 / Ri1 + 1; Av2n = Rf2 / Ri2 + 1; close(Av1 * Av2n, 62.7, 2e-3)                            # Example 14–4 as printed: 62.7
    Rf2_new = 82e3; Av2 = Rf2_new / Ri2 + 1; tot = Av1 * Av2; close(tot, 100, 2e-2)
    alt = (Rf1 / 3.3e3 + 1) * (Rf2 / Ri2 + 1)
    return [('Example 14–4 as drawn: Av1·Av2 = (Rf1/Ri1 + 1)(Rf2/Ri2 + 1)', f'{g(Av1, 3)} × {g(Av2n, 3)} = {g(Av1 * Av2n, 3)}'), ('A choice with total gain ≈ 100 (input stage unchanged, Av1 = 11)', f'Rf2 = 82 kΩ with Ri2 = 10 kΩ: Av2 = {g(Av2, 3)}, total = {g(tot, 4)}'), ('Another choice', f'Ri1 = 3.3 kΩ (Av1 = {g(Rf1 / 3.3e3 + 1, 3)}) with the original output stage gives {g(alt, 3)}: too low, so change the output stage')], \
        'The total gain is the product of the stage gains, Av(tot) = (Rf1/Ri1 + 1)(Rf2/Ri2 + 1) (Eq. 14–3, 14–4); for 100 with Av1 = 11 the output stage needs Av2 = 9.1, i.e. Rf2/Ri2 = 8.1.', ['A design exercise: many resistor pairs give “approximately 100”; one is given.'], None, \
        'Figure 14–15 (p.728): 3656KG isolation amplifier. Input stage: Rs = 10 kΩ (pin 7), Rf1 = 22 kΩ (pin 10 to 6), Ri1 = 2.2 kΩ from pin 6 to ground; output stage: Ri2 = 10 kΩ, Rf2 = 47 kΩ (pin 14 to 15), output at pin 15; supply +15 V.'
C1423 = 'Figure 14–23 (p.731): OTA (LM13700) amplifier, supplies +9 V and −9 V, RBIAS = 33 kΩ from +9 V to the bias input, R1 = 10 kΩ from Vin to the − input, R2 = 10 kΩ from the + input to ground, load RL = 10 kΩ. IBIAS = (+V − (−V) − 1.4 V)/RBIAS, gm = K·IBIAS with K ≈ 16 μS/μA (Figure 14–18), Av = gm·RL (book result 80.5).'
@solve(F, 'related_problem', 14, '14–6')
def _():
    K, RB, RL = 16.0, 33e3, 10e3
    def av(V): I = (2 * V - 1.4) / RB; return I, K * I * RL                          # IBIAS in A, gain
    I9, A9 = av(9.0); close(I9, 503e-6, 2e-3); close(A9, 80.5, 3e-3)                          # the book's ±9 V result
    I12, A12 = av(12.0); sim = np.array([K * ((V + V - 1.4) / RB) * RL for V in (9.0, 12.0)]); close(sim[1], A12, 1e-12)
    return [('IBIAS for ±9 V (book)', f'{g(I9 * 1e6, 3)} μA → Av = {g(A9, 3)}'), ('IBIAS = (12 V + 12 V − 1.4 V)/33 kΩ for ±12 V', f'{g(I12 * 1e6, 3)} μA'), ('New gm = K·IBIAS and Av = gm·RL', f'{g(K * I12 * 1e3, 3)} mS, Av = {g(A12, 3)}: yes, the gain increases from 80.5 to about {g(A12, 3)}')], \
        'The bias current, and so gm and the gain, depend on the supply voltages through IBIAS = (+V − (−V) − 1.4 V)/RBIAS (Floyd §14–3, Example 14–6).', ['K = 16 μS/μA is taken constant (the book\'s value for this current); at the larger bias current the graph of Figure 14–18 may differ slightly.'], None, C1423
@solve(F, 'example', 14, '14–7')
def _():
    K, RB, RL, Vin = 16.0, 56e3, 10e3, 50e-3; must_near('EXAMPLE 14–7', ['314 μA', '5.02 mS', '50.2', '2.51 V', '154 μA', '2.46 mS', '24.6', '1.23 V'], span=6000)
    def amp(vmod): I = (vmod + 9 - 1.4) / RB; return I, K * I * RL * Vin
    Imax, vmax = amp(10.0); Imin, vmin = amp(1.0); close(vmax, 2.51, 5e-3); close(vmin, 1.23, 1.5e-2)
    t = np.linspace(0, 1e-3, 20001); vmod = 5.5 + 4.5 * np.sin(2 * math.pi * 1e3 * t - math.pi / 2); env = np.array([amp(v)[1] for v in vmod]); close(env.max(), vmax, 1e-3); close(env.min(), vmin, 1e-3)    # independent: sweep VMOD over a full cycle
    return [('IBIAS(max) = (VMOD(max) + 9 V − 1.4 V)/RBIAS', f'{g(Imax * 1e6, 3)} μA'), ('gm(max) and Av(max) = gm·RL', f'{g(K * Imax * 1e3, 3)} mS, {g(K * Imax * RL, 3)}'), ('Vout(max)', f'{g(vmax, 3)} V'), ('IBIAS(min), gm(min), Av(min)', f'{g(Imin * 1e6, 3)} μA, {g(K * Imin * 1e3, 3)} mS, {g(K * Imin * RL, 3)}'), ('Vout(min)', f'{g(vmin, 3)} V'),
            ('Output', 'a 1 MHz carrier whose amplitude follows the 1 kHz modulating sine between 1.23 V and 2.51 V (amplitude modulation)')], \
        'OTA amplitude modulator: the bias current follows VMOD, so the gain does (Floyd §14–3). Maximum at VMOD = +10 V, minimum at +1 V; Vout = Av·Vin with Vin = 50 mV as in the book.', ['The book multiplies the 50 mV peak-to-peak input by the gain, so the quoted values are peak-to-peak amplitudes of the carrier.'], None, \
        'Figure 14–25 (p.733): OTA amplitude modulator, supplies +9 V and −9 V; carrier Vin = 50 mV pp at 1 MHz through R1 = 10 kΩ to the − input, R2 = 10 kΩ from the + input to ground, RL = 10 kΩ; the bias input takes VMOD (1 kHz sine between +1 V and +10 V) through RBIAS = 56 kΩ.'
C1434 = 'Figures 14–34 and 14–33 (p.740): antilog amplifier: the input +175.1 mV is applied to the emitter of a grounded-base transistor whose collector goes to the − input; feedback resistor Rf = 68 kΩ (Example 14–10).'
@solve(F, 'example', 14, '14–10')
def _():
    Rf, IEBO, Vin = 68e3, 40e-9, 0.1751; x = Vin / 0.025; k = math.exp(x); Vout = -Rf * IEBO * k; must_near('EXAMPLE 14–10', ['1101', '−3 V']); close(k, 1101, 1e-3); close(Vout, -3.0, 5e-3)
    vlog = -0.025 * math.log(3.0 / (IEBO * Rf)); close(vlog, -Vin, 1e-3)                        # independent: the log amplifier of Example 14–9 (3 V in, same constants) gives −175.1 mV; the antilog amplifier undoes it
    return [('antilog(Vin/25 mV)', f'{g(k, 4)} (e^{g(x, 4)})'), ('Vout = −Rf·IEBO·antilog(Vin/25 mV)', f'{g(Vout, 3)} V')], 'Antilog amplifier (Floyd §14–4): Vout = −Rf·IEBO·antilog(Vin/25 mV) = −(68 kΩ)(40 nA)(1101) = −3 V. It undoes the log amplifier of Example 14–9, whose output for a 3 V input is −175.1 mV.', [], None, C1434
@solve(F, 'related_problem', 14, '14–10')
def _():
    Rf, IEBO, Vin = 100e3, 40e-9, 0.1751; Vout = -Rf * IEBO * math.exp(Vin / 0.025); close(Vout, -3.0 * 100 / 68, 5e-3)
    return [('Vout = −Rf·IEBO·antilog(Vin/25 mV) with Rf = 100 kΩ', f'{g(Vout, 3)} V')], 'Vout is proportional to Rf: −3 V × 100 kΩ/68 kΩ.', ['Provided the op-amp output can reach this value (the supply voltages are not given).'], None, C1434
C1454 = 'Figures 14–54 and 14–6 (pp.758, 723): AD622 instrumentation amplifier, supplies ±15 V, +IN pin 3, −IN pin 2, RG = 1.0 kΩ between pins 1 and 8, output pin 6, REF pin 5. Gain Av = 50.5 kΩ/RG + 1 (51.5 as drawn). Figure 14–6 is the AD622 graph of gain versus frequency (curves for gains 1, 10, 100, 1000).'
@solve(F, 'problem', 14, '6')
def _():
    bw3, fpk, fdrop, gpk = ad622_bw(10); RG = 50.5e3 / 9; close(bw3, 400e3, 0.05); close(gpk, 11, 0.05)
    return [('RG for a gain of 10', si(RG, 'Ω', 3)), ('Bandwidth from the gain-10 curve of Figure 14–6', f'≈ {g(round(bw3 / 1e5) * 100, 3)} kHz (3 dB down: the curve peaks at {g(gpk, 3)} near {g(fpk / 1e3, 3)} kHz and falls to 7.07 at {g(bw3 / 1e3, 3)} kHz)')], \
        'Gain 10 needs RG = 50.5 kΩ/9 = 5.6 kΩ; the bandwidth is read from the gain-10 curve of Figure 14–6 at the −3 dB point (gain 7.07).', \
        ['The graph reading comes from the vector drawing of Figure 14–6 (the curve points were converted with the log-log axes, calibration checked on the flat levels 1, 10, 100, 1000). If the book\'s rougher rule of Example 14–2 (“where the curve begins to drop”) is used the answer is about 0.3 MHz.', 'The statement says the gain is “set to 10” (RG would be 5.6 kΩ) although the figure shows 1.0 kΩ.'], None, C1454
@solve(F, 'problem', 14, '8')
def _():
    G = 20.0; RG = 50.5e3 / (G - 1); close(50.5e3 / 1.0e3 + 1, 51.5, 1e-9); close(50.5e3 / RG + 1, G, 1e-12)                     # the printed answer of Problem 5 (51.5 for 1.0 kΩ) confirms the formula and the figure
    near = {r: 50.5e3 / r + 1 for r in (2.7e3, 2.4e3)}
    return [('RG = 50.5 kΩ/(Av − 1) for Av = 20', f'{si(RG, "Ω", 4)} (nearest standard value 2.7 kΩ gives Av = {g(near[2.7e3], 3)})')], 'Av = 50.5 kΩ/RG + 1 (Floyd Eq. 14–1) gives RG = 50.5 kΩ/19 = 2.66 kΩ.', [], None, C1454
@solve(F, 'problem', 14, '12')
def _():
    Av1 = 330e3 / 1.0e3 + 1; Av2_want = 440 / Av1; Rf2 = (Av2_want - 1) * 15e3; close(Av1 * (Rf2 / 15e3 + 1), 440, 1e-12)
    std = {r: Av1 * (r / 15e3 + 1) for r in (4.7e3, 5.1e3)}; orig = Av1 * (47e3 / 15e3 + 1)
    return [('Gain as drawn: Av1·Av2 = (Rf1/Ri1 + 1)(Rf2/Ri2 + 1)', f'{g(Av1, 4)} × {g(47e3 / 15e3 + 1, 3)} = {g(orig, 4)}'), ('Output-stage gain needed for 440', f'Av2 = 440/{g(Av1, 3)} = {g(Av2_want, 4)}'), ('Rf2 for that gain (Ri2 = 15 kΩ)', f'{si(Rf2, "Ω", 3)}; standard values: 4.7 kΩ → total {g(std[4.7e3], 4)}, 5.1 kΩ → {g(std[5.1e3], 4)}')], \
        'Total gain = Av1·Av2 with Av1 = 330 kΩ/1.0 kΩ + 1 = 331 and Av2 = Rf2/Ri2 + 1; only Rf2 (or Ri2) of the output stage may change: Rf2/Ri2 = 0.329, i.e. Rf2 ≈ 4.9 kΩ for Ri2 = 15 kΩ.', ['Figure 14–55(b) is read as Rs = 10 kΩ, Rf1 = 330 kΩ, Ri1 = 1.0 kΩ, Ri2 = 15 kΩ and Rf2 = 47 kΩ; the same figure, part (a), is checked by Problem 11 whose printed answer (change 18 kΩ to 68 kΩ) follows from the same formulas.'], None, \
        'Figure 14–55(b) (p.759): 3656KG isolation amplifier, supply +15 V. Input stage: Rs = 10 kΩ, Rf1 = 330 kΩ (pin 10 to 6), Ri1 = 1.0 kΩ from pin 6 to ground; output stage: Ri2 = 15 kΩ, Rf2 = 47 kΩ (pin 14 to 15), output pin 15.'
@solve(F, 'problem', 14, '18')
def _():
    K, RL = 16.0, 6.8e3
    av = lambda RB: K * ((12 + 12 - 1.4) / RB) * RL; lo, hi = av(230e3), av(220e3)
    t = np.linspace(220e3, 230e3, 1001); a = np.array([av(r) for r in t]); close(a.min(), lo, 1e-9); close(a.max(), hi, 1e-9)                               # sweep the rheostat
    return [('RBIAS = 220 kΩ (rheostat at 0): maximum gain', f'IBIAS = {g((24 - 1.4) / 220e3 * 1e6, 4)} μA → Av = {g(hi, 3)}'), ('RBIAS = 220 kΩ + 10 kΩ: minimum gain', f'IBIAS = {g((24 - 1.4) / 230e3 * 1e6, 4)} μA → Av = {g(lo, 3)}')], \
        'IBIAS = (+V − (−V) − 1.4 V)/RBIAS, gm = K·IBIAS with K = 16 μS/μA, Av = gm·RL (Example 14–6/14–7 method).', \
        ['NOTE: the printed answer of Problem 17 (same circuit without the rheostat) is Av ≅ 11.6, about 4 % above the 11.2 given by the book\'s own method (1.4 V drop in the bias path); with that 4 % scaling the range would be about 11.1 to 11.6. Cause not found in the book.'], None, \
        'Figure 14–56 (p.759): OTA amplifier, supplies +12 V and −12 V, RBIAS = 220 kΩ from +12 V to the bias input, R1 = 10 kΩ from Vin to the − input, R2 = 10 kΩ from the + input to ground, load RL = 6.8 kΩ (K = 16 μS/μA).'
@solve(F, 'problem', 14, '28')
def _():
    Rf, IEBO, Vin = 100e3, 60e-9, 0.225; x = Vin / 0.025; k = math.exp(x); Vout = -Rf * IEBO * k
    close(-Rf * IEBO * 10 ** (x / math.log(10)), Vout, 1e-9)
    return [('antilog(Vin/25 mV) = e^9', g(k, 4)), ('Vout = −Rf·IEBO·antilog(Vin/25 mV)', f'{g(Vout, 3)} V')], 'Antilog amplifier (Floyd §14–4): Vout = −(100 kΩ)(60 nA)·e^(0.225/0.025) = −6 mV × 8103 = −48.6 V.', ['This is the ideal result; it is larger than any normal op-amp supply, so the real output would saturate near the negative supply (the supply voltage is not given).'], None, \
        'Figure 14–61 (p.760): antilog amplifier: the input +0.225 V is applied to the emitter of a grounded-base transistor whose collector goes to the − input; Rf = 100 kΩ from the output to the − input, + input grounded.'

# ============================================================================================ Chapter 15 (m06)
def sk_h(kind, Ra, Rb, Ca, Cb, K, f):
    """Exact mid-circuit KCL solution of a Sallen-Key section (ideal op-amp of gain K = 1 + R1/R2 on the + input).  'lp': Ra series input, Rb to the + input, Ca (feedback) from the node between
    Ra and Rb to the output, Cb from the + input to ground (Floyd Fig. 15–11).  'hp': Ca series input, Cb to the + input, Ra (feedback) from the node between Ca and Cb to the output, Rb from the + input to
    ground (Fig. 15–15).  Returns Vout/Vin at frequency f."""
    s = 2j * math.pi * f
    if kind == 'lp':
        A = np.array([[1 / Ra + 1 / Rb + s * Ca, -1 / Rb - K * s * Ca], [-1 / Rb, 1 / Rb + s * Cb]], complex)
    else:
        A = np.array([[s * Ca + s * Cb + 1 / Ra, -s * Cb - K / Ra], [-s * Cb, s * Cb + 1 / Rb]], complex)
    b = np.array([1 / Ra if kind == 'lp' else s * Ca, 0], complex); X, Vp = np.linalg.solve(A, b); return K * Vp
def fc3(H, f_lo, f_hi, kind='lp'):
    """-3 dB frequency of a response H(f) relative to its passband gain (dc gain for 'lp', gain at f_hi for 'hp')."""
    from scipy.optimize import brentq
    ref = abs(H(f_lo)) if kind == 'lp' else abs(H(f_hi)); return brentq(lambda f: abs(H(f)) - ref / math.sqrt(2), f_lo, f_hi)
def statevar(R1, R2, R3, R4, R5, R6, R7, C1, C2, f):
    """Exact ideal-op-amp solution of the state-variable filter of Figure 15–22: returns (HP, BP, LP) outputs for Vin = 1 V.  Op-amp 1 sums Vin (through R2), LP (through R1) and HP (through R3 feedback)
    at its − input; its + input is the R5/R6 divider of the BP output; op-amps 2 and 3 are inverting integrators (R4, C1 and R7, C2)."""
    s = 2j * math.pi * f; beta = R6 / (R5 + R6)
    # unknowns HP, BP, LP: BP = −HP/(s·R4·C1);  LP = −BP/(s·R7·C2);  KCL at the − input (V− = beta·BP)
    A = np.array([[1 / R3, -(1 / R2 + 1 / R1 + 1 / R3) * beta, 1 / R1], [1 / (s * R4 * C1), 1, 0], [0, 1 / (s * R7 * C2), 1]], complex); b = np.array([-1 / R2, 0, 0], complex)
    hp, bp, lp = np.linalg.solve(A, b); return hp, bp, lp
def sv_f0_q(R1, R2, R3, R4, R5, R6, R7, C1, C2):
    """Centre frequency and Q of the exact band-pass output: f0 = frequency of maximum |BP|, Q = f0/(−3 dB bandwidth)."""
    from scipy.optimize import brentq, minimize_scalar
    nom = 1 / (2 * math.pi * R4 * C1); bp = lambda f: abs(statevar(R1, R2, R3, R4, R5, R6, R7, C1, C2, f)[1])
    r = minimize_scalar(lambda f: -bp(f), bounds=(0.5 * nom, 2 * nom), method='bounded', options={'xatol': 1e-6 * nom}); f0 = r.x; pk = bp(f0)
    lo = brentq(lambda f: bp(f) - pk / math.sqrt(2), 0.2 * f0, f0); hi = brentq(lambda f: bp(f) - pk / math.sqrt(2), f0, 5 * f0); return f0, f0 / (hi - lo)
C156 = 'Figure 15–6 (p.770): general active single-pole (first-order) filter block: a frequency-selective RC circuit drives the + input of a noninverting op-amp whose gain and damping factor are set by the feedback resistors R1 (from the output to the − input) and R2 (from the − input to ground).'
@solve(F, 'example', 15, '15–2')
def _():
    R2 = 10e3; R1 = 0.586 * R2; must_near('EXAMPLE 15–2', ['0.586', '5.86 k', '5.6 kΩ']); DF = 2 - R1 / R2; close(DF, math.sqrt(2), 1e-3)
    f = 1.0; H = lambda ff: abs(sk_h('lp', 10e3, 10e3, 10e-9, 10e-9, 1 + R1 / R2, ff)); f0 = 1 / (2 * math.pi * 10e3 * 10e-9); close(H(f0) / H(1.0), 1 / math.sqrt(2), 2e-3)       # independent: maximally flat means |H(fc)| = |H(0)|/√2 in the exact second-order response
    return [('R1 = 0.586·R2 for Butterworth (DF = 2 − R1/R2 = 1.414)', si(R1, 'Ω', 3)), ('Nearest standard 5 % value', '5.6 kΩ (DF = 2 − 5.6/10 = 1.44, very close to Butterworth)')], 'Damping factor DF = 2 − R1/R2; Butterworth needs DF = 1.414, so R1/R2 = 0.586 (Floyd Table 15–1). The book prints R1 = 5.86 kΩ and picks 5.6 kΩ.', ['The independent check uses an exact Sallen-Key response: with R1/R2 = 0.586 its gain at fc is 1/√2 of the dc gain (maximally flat).'], None, C156
C1511 = 'Figure 15–11 (p.774): Sallen-Key low-pass filter: input through RA to a node, RB from that node to the + input, CA from the node to the output (feedback), CB from the + input to ground; gain-setting resistors R1 (output to − input) and R2 (− input to ground). In Example 15–3 RA = RB = R2 = 1.0 kΩ and CA = CB = 0.022 μF (fc = 7.23 kHz, R1 = 586 Ω).'
@solve(F, 'related_problem', 15, '15–3')
def _():
    R, C = 2.2e3, 0.01e-6; fc = 1 / (2 * math.pi * R * C); R2 = R; R1 = 0.586 * R2; K = 1 + R1 / R2
    close(fc, 1 / (2 * math.pi * 1.0e3 * 0.022e-6) * (1.0e3 * 0.022e-6) / (R * C), 1e-12)
    ex = fc3(lambda f: sk_h('lp', R, R, C, C, K, f), 10.0, 5 * fc); close(ex, fc, 5e-3)                                                              # exact response of the Butterworth filter: −3 dB at fc
    return [('Critical frequency fc = 1/(2πRC)', si(fc, 'Hz', 3)), ('R1 = 0.586·R2 (Butterworth)', si(R1, 'Ω', 3))], 'Equal-value Sallen-Key: fc = 1/(2πRC) with RA = RB = 2.2 kΩ and CA = CB = 0.01 μF; R1/R2 = 0.586 for DF = 1.414 (Example 15–3 method).', [f'The exact response with R1 = 0.586·R2 is 3 dB down at {si(ex, "Hz", 4)}.'], None, C1511
C1512 = 'Figure 15–12(b) (p.775): four-pole Sallen-Key low-pass filter made of two cascaded two-pole stages: stage 1 with RA1 = RB1 (RC low-pass circuit), CA1 = CB1 and feedback resistors R1 and R2; stage 2 with RA2 = RB2, CA2 = CB2 and feedback resistors R3 and R4.'
def four_pole(R, C, R1, R2, R3, R4):
    return lambda f: sk_h('lp', R, R, C, C, 1 + R1 / R2, f) * sk_h('lp', R, R, C, C, 1 + R3 / R4, f)
@solve(F, 'example', 15, '15–4')
def _():
    R, fc = 1.8e3, 2680.0; C = 1 / (2 * math.pi * R * fc); R2 = R4 = R; R1 = 0.152 * R2; R3 = 1.235 * R4; must_near('EXAMPLE 15–4', ['0.033 μF', '= 274', '= 2.22', 'R1 = 270 Ω', 'R3 = 2.2 kΩ'])
    close(C, 0.033e-6, 1e-2); H = four_pole(R, C, R1, R2, R3, R4); ex = fc3(H, 1.0, 5 * fc); close(ex, fc, 1.5e-2)                                  # exact response of the cascade: −3 dB at fc
    return [('C = 1/(2πR·fc), CA1 = CB1 = CA2 = CB2', si(C, 'F', 3)), ('Stage 1 (DF = 1.848): R1 = 0.152·R2', f'{si(R1, "Ω", 3)} (use 270 Ω)'), ('Stage 2 (DF = 0.765): R3 = 1.235·R4', f'{si(R3, "Ω", 3)} (use 2.2 kΩ)')], \
        'Both stages need the same fc, so with equal R the capacitors are equal: C = 1/(2πR·fc); the feedback ratios of Table 15–1 for a four-pole Butterworth filter are R1/R2 = 0.152 and R3/R4 = 1.235 with R2 = R4 = 1.8 kΩ.', [f'The exact response of the two cascaded sections with the book\'s values is 3 dB down at {si(ex, "Hz", 4)}.'], None, C1512
@solve(F, 'related_problem', 15, '15–4')
def _():
    R, fc = 680.0, 1000.0; C = 1 / (2 * math.pi * R * fc); R2 = R4 = R; R1 = 0.152 * R2; R3 = 1.235 * R4; H = four_pole(R, C, R1, R2, R3, R4); ex = fc3(H, 1.0, 5 * fc); close(ex, fc, 1.5e-2)
    return [('C = 1/(2πR·fc) for every capacitor', si(C, 'F', 3)), ('R2 = R4', '680 Ω (equal to the filter resistors)'), ('R1 = 0.152·R2 (stage 1)', f'{si(R1, "Ω", 3)} (nearest standard 100 Ω or 110 Ω)'), ('R3 = 1.235·R4 (stage 2)', f'{si(R3, "Ω", 3)} (nearest standard 820 Ω or 840 Ω → 820 Ω)')], 'Same method as Example 15–4 with R = 680 Ω and fc = 1 kHz.', [f'The exact response with the computed (not rounded) values is 3 dB down at {si(ex, "Hz", 4)}.'], None, C1512
C1515 = 'Figure 15–15 (p.777): Sallen-Key high-pass filter: input through CA to a node, CB from that node to the + input, RA from the node to the output (feedback), RB from the + input to ground; gain-setting resistors R1 (output to − input) and R2 (− input to ground).'
@solve(F, 'example', 15, '15–5')
def _():
    R, fc = 3.3e3, 10e3; C = 1 / (2 * math.pi * R * fc); R2 = R; R1 = 0.586 * R2; must_near('EXAMPLE 15–5', ['0.0048 μF', '1.93 k', '5.63 k']); close(C, 4.8e-9, 1e-2); close(R1, 1.93e3, 2e-3)
    ex = fc3(lambda f: sk_h('hp', R, R, C, C, 1 + R1 / R2, f), 10.0, 100 * fc, 'hp'); close(ex, fc, 5e-3)                                                    # exact response: −3 dB at fc
    return [('C = CA = CB = 1/(2πR·fc) with R = RA = RB = R2 = 3.3 kΩ', si(C, 'F', 3)), ('R1 = 0.586·R2 (DF = 1.414)', si(R1, 'Ω', 3)), ('If R1 = 3.3 kΩ is chosen instead', f'R2 = R1/0.586 = {si(3.3e3 / 0.586, "Ω", 3)}')], 'Equal-value Sallen-Key high-pass: fc = 1/(2πRC), R1/R2 = 0.586 for a Butterworth response (Floyd §15–4). The book prints 0.0048 μF and 1.93 kΩ.', [f'The exact response is 3 dB down at {si(ex, "Hz", 4)}.'], None, C1515
@solve(F, 'related_problem', 15, '15–5')
def _():
    R, fc = 10e3, 300.0; C = 1 / (2 * math.pi * R * fc); R2 = R; R1 = 0.586 * R2
    ex = fc3(lambda f: sk_h('hp', R, R, C, C, 1 + R1 / R2, f), 1.0, 100 * fc, 'hp'); close(ex, fc, 5e-3)
    return [('RA = RB = R2', '10 kΩ'), ('CA = CB = 1/(2πR·fc)', f'{si(C, "F", 3)} (standard value 0.056 μF gives fc = {si(1 / (2 * math.pi * R * 0.056e-6), "Hz", 3)}; 0.047 μF gives {si(1 / (2 * math.pi * R * 0.047e-6), "Hz", 3)})'), ('R1 = 0.586·R2', si(R1, 'Ω', 3) + ' (standard 5.6 kΩ)')], 'Same method as Example 15–5 with R = 10 kΩ and fc = 300 Hz.', [f'The exact response with the computed values is 3 dB down at {si(ex, "Hz", 4)}.'], None, C1515
C1519 = 'Figure 15–19 (p.781): multiple-feedback band-pass filter: input through R1 = 68 kΩ to a node; from that node C1 = 0.01 μF to the output, R3 = 2.7 kΩ to ground and C2 = 0.01 μF to the − input; R2 = 180 kΩ from the output to the − input; + input grounded.'
def mfb_h(R1, R2, R3, C1, C2, f):
    """Exact ideal-op-amp response of the multiple-feedback band-pass of Figure 15–19."""
    s = 2j * math.pi * f; A = np.array([[1 / R1 + 1 / R3 + s * C2 + s * C1, -s * C1], [s * C2, 1 / R2]], complex); Va, Vo = np.linalg.solve(A, np.array([1 / R1, 0], complex)); return Vo
def mfb_figures(R1, R2, R3, C):
    from scipy.optimize import minimize_scalar, brentq
    f0 = (1 / (2 * math.pi * C)) * math.sqrt((R1 + R3) / (R1 * R2 * R3)); A0 = R2 / (2 * R1); Q = math.pi * f0 * C * R2; return f0, A0, Q, f0 / Q
@solve(F, 'related_problem', 15, '15–6')
def _():
    from scipy.optimize import minimize_scalar, brentq
    C = 0.01e-6; R1, R3 = 68e3, 2.7e3
    f0b, A0b, Qb, BWb = mfb_figures(R1, 180e3, R3, C); close(f0b, 736, 2e-3); close(A0b, 1.32, 5e-3); close(Qb, 4.16, 5e-3); close(BWb, 177, 5e-3)                       # Example 15–6 as printed
    f0, A0, Q, BW = mfb_figures(R1, 330e3, R3, C)
    hh = lambda f: abs(mfb_h(R1, 330e3, R3, C, C, f)); r = minimize_scalar(lambda f: -hh(f), bounds=(0.3 * f0, 3 * f0), method='bounded', options={'xatol': 1e-4}); pk = hh(r.x)
    lo = brentq(lambda f: hh(f) - pk / math.sqrt(2), 0.1 * f0, r.x); hi = brentq(lambda f: hh(f) - pk / math.sqrt(2), r.x, 10 * f0)
    close(r.x, f0, 5e-3); close(pk, A0, 5e-3); close(hi - lo, BW, 5e-2)                                                                                              # independent: exact transfer function
    return [('Centre frequency f0', si(f0, 'Hz', 3)), ('Maximum gain A0 = R2/(2R1)', g(A0, 3)), ('Q = π·f0·C·R2', g(Q, 3)), ('Bandwidth BW = f0/Q', si(BW, 'Hz', 3))], 'Multiple-feedback band-pass (Floyd §15–5): f0 = (1/2πC)·√((R1 + R3)/(R1R2R3)), A0 = R2/2R1, Q = π·f0·C·R2, BW = f0/Q; Example 15–6 (R2 = 180 kΩ) gives 736 Hz, 1.32 and 177 Hz.', \
        [f'The exact transfer function of the circuit gives a peak at {si(r.x, "Hz", 3)}, gain {g(pk, 3)} and a −3 dB bandwidth of {si(hi - lo, "Hz", 3)}.'], None, C1519
C1522 = 'Figure 15–22 (p.783): state-variable filter with three op-amps: R1 = R2 = R3 = 10 kΩ around the first (summing) op-amp, two integrators with R4 = R7 = 1.0 kΩ and C1 = C2 = 0.022 μF, band-pass output taken from the second op-amp; Q-setting resistors R5 = 100 kΩ (from the BP output) and R6 = 1.0 kΩ (to ground) feed the + input of the first op-amp.'
@solve(F, 'related_problem', 15, '15–7')
def _():
    base = dict(R1=10e3, R2=10e3, R3=10e3, R4=1e3, R5=100e3, R6=1e3, R7=1e3, C1=0.022e-6, C2=0.022e-6)
    f0b = 1 / (2 * math.pi * base['R4'] * base['C1']); Qb = (base['R5'] / base['R6'] + 1) / 3; close(f0b, 7.23e3, 2e-3); close(Qb, 33.7, 2e-3); close(f0b / Qb, 215, 5e-3)                       # Example 15–7 as printed
    new = dict(base, R4=330.0, R6=330.0, R7=330.0); f0 = 1 / (2 * math.pi * new['R4'] * new['C1']); Q = (new['R5'] / new['R6'] + 1) / 3; BW = f0 / Q
    fe, Qe = sv_f0_q(*[new[k] for k in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'C1', 'C2')]); close(fe, f0, 1e-2); close(Qe, Q, 3e-2)                                                  # independent: exact transfer function
    return [('f0 = 1/(2π·R4·C1) = 1/(2π·R7·C2)', si(f0, 'Hz', 3)), ('Q = (1/3)(R5/R6 + 1)', g(Q, 3)), ('BW = f0/Q', si(BW, 'Hz', 3))], 'State-variable band-pass (Floyd §15–5): f0 = fc of the integrators, Q = (1/3)(R5/R6 + 1), BW = f0/Q. Example 15–7 (R4 = R6 = R7 = 1.0 kΩ) gives 7.23 kHz, 33.7 and 215 Hz.', \
        [f'Exact solution of the three-op-amp circuit: peak at {si(fe, "Hz", 4)}, Q = {g(Qe, 3)}.'], None, C1522
C1526 = 'Figure 15–26 (p.786): band-stop (notch) filter made from a state-variable filter and a summing amplifier: R1 = R2 = R3 = 10 kΩ, integrators R4 = R7 = 12 kΩ with C1 = C2 = 0.22 μF, Q-setting resistors R5 (from the BP output) and R6 (to ground); the high-pass and low-pass outputs are added by R8 = R9 = R10 = 10 kΩ.'
def notch(R1, R2, R3, R4, R5, R6, R7, C1, C2, R8, R9, R10, f):
    hp, bp, lp = statevar(R1, R2, R3, R4, R5, R6, R7, C1, C2, f); return -R10 * (lp / R8 + hp / R9)
def notch_q(vals, f0):
    from scipy.optimize import brentq, minimize_scalar
    nm = lambda f: abs(notch(*vals, f)); r = minimize_scalar(nm, bounds=(0.7 * f0, 1.3 * f0), method='bounded', options={'xatol': 1e-8}); ref = nm(0.01 * f0)
    lo = brentq(lambda f: nm(f) - ref / math.sqrt(2), 0.5 * f0, r.x); hi = brentq(lambda f: nm(f) - ref / math.sqrt(2), r.x, 2 * f0); return r.x, ref, nm(r.x), f0 / (hi - lo)
@solve(F, 'example', 15, '15–8')
def _():
    R4, C = 12e3, 0.22e-6; f0 = 1 / (2 * math.pi * R4 * C); must_near('EXAMPLE 15–8', ['60 Hz', '95.7 k', '100 kΩ'], span=4200); close(f0, 60, 6e-3)
    Q = 10.0; R6 = 3.3e3; R5 = (3 * Q - 1) * R6; close(R5, 95.7e3, 1e-3)
    vals = (10e3, 10e3, 10e3, R4, R5, R6, R4, C, C, 10e3, 10e3, 10e3); fn, ref, dip, Qe = notch_q(vals, f0); close(fn, f0, 1e-2); close(Qe, Q, 5e-2); assert dip < 1e-3 * ref                          # independent: exact notch response
    R5s = 100e3; Qs = (R5s / R6 + 1) / 3
    return [('Centre frequency f0 = 1/(2π·R4·C1)', si(f0, 'Hz', 3) + ' ≈ 60 Hz'), ('R5 for Q = 10 with R6 = 3.3 kΩ: R5 = (3Q − 1)·R6', f'{si(R5, "Ω", 3)} (standard value 100 kΩ gives Q = {g(Qs, 3)})')], 'The band-stop filter uses the state-variable filter: f0 equals the critical frequency of the integrators and Q = (1/3)(R5/R6 + 1), so R5 = (3Q − 1)R6 (Floyd §15–6). R6 is free to choose.', \
        [f'Exact solution of the whole circuit (state-variable filter + summing amplifier): notch at {si(fn, "Hz", 4)}, depth > 60 dB, Q = {g(Qe, 3)}.'], None, C1526
@solve(F, 'related_problem', 15, '15–8')
def _():
    f_new, C = 120.0, 0.22e-6; R = 1 / (2 * math.pi * f_new * C); alt = 1 / (2 * math.pi * f_new * 12e3)
    vals = (10e3, 10e3, 10e3, R, 95.7e3, 3.3e3, R, C, C, 10e3, 10e3, 10e3); fn, ref, dip, Qe = notch_q(vals, f_new); close(fn, f_new, 1e-2)
    return [('New integrator resistors R4 = R7 = 1/(2π·f0·C)', f'{si(R, "Ω", 3)} (standard 6.2 kΩ gives {si(1 / (2 * math.pi * 6.2e3 * C), "Hz", 4)}; 6.0 kΩ gives {si(1 / (2 * math.pi * 6.0e3 * C), "Hz", 4)})'), ('Or keep R4 = R7 = 12 kΩ and change C1 = C2', f'{si(alt, "F", 3)} (0.11 μF)')], 'f0 = 1/(2πRC) of the integrators is inversely proportional to R·C: doubling the centre frequency halves R4 = R7 (both, so the integrators stay matched) or halves C1 = C2; R5/R6 (the Q) need not change.', [f'Exact solution of the circuit with R4 = R7 = {si(R, "Ω", 3)}: notch at {si(fn, "Hz", 4)}.'], None, C1526
C1545 = 'Figure 15–45 (p.805): two cascaded Sallen-Key low-pass sections, each with unequal values. Stage 1: R1 = 4.7 kΩ, R2 = 6.8 kΩ, C1 = 0.22 μF (feedback capacitor), C2 = 0.1 μF (to ground), gain resistors R3 = 1.0 kΩ and R4 = 6.8 kΩ. Stage 2: R5 = 4.7 kΩ, R6 = 6.8 kΩ, C3 = 0.22 μF, C4 = 0.1 μF, gain resistors R7 = 6.8 kΩ and R8 = 5.6 kΩ.'
@solve(F, 'problem', 15, '12')
def _():
    Ra, Rb, Cf, Cg = 4.7e3, 6.8e3, 0.22e-6, 0.1e-6; f0 = 1 / (2 * math.pi * math.sqrt(Ra * Rb * Cf * Cg)); C = 0.22e-6; R = 1 / (2 * math.pi * f0 * C)
    r1, r2 = 1.0e3 / 6.8e3, 6.8e3 / 5.6e3; DF1, DF2 = 2 - r1, 2 - r2; close(DF1, 1.848, 2e-2); close(DF2, 0.765, 5e-2)                                                      # the feedback ratios are the Butterworth ratios of Table 15–1
    H = four_pole(R, C, 1.0e3, 6.8e3, 6.8e3, 5.6e3); ex = fc3(H, 1.0, 20 * f0); close(ex, f0, 3e-2)                                                                          # exact response of the equal-value filter: −3 dB at the same f0
    return [('Critical frequency of each stage fc = 1/(2π·√(R1R2C1C2))', si(f0, 'Hz', 4)), ('Equal-value stage with C = 0.22 μF: R = 1/(2π·fc·C)', f'{si(R, "Ω", 3)} (standard 3.9 kΩ gives fc = {si(1 / (2 * math.pi * 3.9e3 * C), "Hz", 4)}; 3.6 kΩ gives {si(1 / (2 * math.pi * 3.6e3 * C), "Hz", 4)})'),
            ('Result', 'R1 = R2 = R5 = R6 = 3.8 kΩ (≈ 3.9 kΩ), C1 = C2 = C3 = C4 = 0.22 μF; the gain-setting resistors R3/R4 = 0.147 (DF = 1.853) and R7/R8 = 1.214 (DF = 0.786) are unchanged: they are the four-pole Butterworth ratios of Table 15–1 (0.152 and 1.235), so the response curve is kept')], \
        'In the book\'s model the response (damping factor) of an equal-value Sallen-Key stage depends only on R3/R4 (R7/R8) and fc = 1/(2πRC); the unequal-value circuit has fc = 1/(2π√(R1R2C1C2)) = 190 Hz. Replacing both resistors by R = 1/(2π·fc·C) with C = 0.22 μF keeps fc and the feedback resistors keep the Butterworth shape.', \
        [f'Exact check of the new circuit: the cascade is 3 dB down at {si(ex, "Hz", 4)}.', 'This follows the textbook equal-value model; the exact response of the original unequal-value circuit is not identical (its damping depends on the component ratios), so “without changing the response curve” is interpreted as keeping fc and the Butterworth feedback ratios.'], None, C1545
@solve(F, 'problem', 15, '20')
def _():
    R, C = 12e3, 0.01e-6; f0 = 1 / (2 * math.pi * R * C); Q = 50.0; R6 = 1.0e3; R5 = (3 * Q - 1) * R6; BW = f0 / Q
    vals = dict(R1=R, R2=R, R3=R, R4=R, R5=R5, R6=R6, R7=R, C1=C, C2=C); fe, Qe = sv_f0_q(*[vals[k] for k in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'C1', 'C2')]); close(fe, f0, 1e-2); close(Qe, Q, 5e-2)
    return [('Centre frequency f0 = 1/(2π·R4·C1)', si(f0, 'Hz', 4)), ('R5 = (3Q − 1)·R6 for Q = 50 (choose R6 = 1.0 kΩ)', f'{si(R5, "Ω", 3)} (standard value 150 kΩ gives Q = {g((150e3 / R6 + 1) / 3, 3)})'), ('Bandwidth BW = f0/Q', si(BW, 'Hz', 3))], \
        'State-variable band-pass: Q = (1/3)(R5/R6 + 1), so R5 = (3Q − 1)R6 = 149·R6; with R6 = 1.0 kΩ, R5 = 149 kΩ. BW = f0/Q = 1.326 kHz/50.', ['R5 and R6 are not in the figure (they are to be chosen); only their ratio matters: R6 = 1.0 kΩ is an arbitrary choice.', f'Exact solution of the three-op-amp circuit gives f0 = {si(fe, "Hz", 4)} and Q = {g(Qe, 3)}.'], None, \
        'Figure 15–48 (p.806): state-variable filter, R1 = R2 = R3 = R4 = R7 = 12 kΩ, C1 = C2 = 0.01 μF; R5 (from the BP output) and R6 (to ground) set Q and are left to be chosen.'

# ============================================================================================ Chapter 16 (m07)
from scipy.optimize import brentq as _brentq
def hp_ladder(R, C, f):
    """Exact transfer V3/Vin of the three-section RC phase-shift network of Figure 16–14 (series capacitors, shunt resistors, unloaded)."""
    s = 2j * math.pi * f; Y = 1 / R; G = s * C
    A = np.array([[G + Y + G, -G, 0], [-G, G + Y + G, -G], [0, -G, G + Y]], complex); v = np.linalg.solve(A, np.array([G, 0, 0], complex)); return v[2]
def sim555(R1, R2, C, Vcc=12.0, diode=False, steps=4000):
    """Time-stepped astable 555: C charges towards Vcc through R1 + R2 (through R1 only with the diode across R2) until 2/3 Vcc, then discharges through R2 to 1/3 Vcc.  Returns (frequency, duty)."""
    hi, lo = 2 * Vcc / 3, Vcc / 3; vc, t, state, tH, tL, cyc = lo, 0.0, 1, 0.0, 0.0, 0; dt = (R1 + R2) * C / steps; edges = []
    for _ in range(40 * steps):
        if state:
            vc += (Vcc - vc) * dt / ((R1 if diode else R1 + R2) * C); t += dt
            if vc >= hi: edges.append(t); state = 0
        else:
            vc += (0 - vc) * dt / (R2 * C); t += dt
            if vc <= lo: edges.append(t); state = 1
        if len(edges) >= 5: break
    th, tl = edges[2] - edges[1], edges[3] - edges[2]; return 1 / (th + tl), th / (th + tl)
C1612 = 'Figure 16–12 (p.814): Wien-bridge oscillator with automatic gain control: lead-lag network R1 = R2 = 10 kΩ, C1 = C2 = 0.01 μF on the + input; negative feedback from the output to the − input through the 10 kΩ potentiometer Rf, with a JFET (2N5458, drain-source resistance r′ds) and R3 = 1.0 kΩ in the source in series to ground; diode D1 (1N914), R4 = 10 kΩ and C3 = 1.0 μF rectify the output to bias the JFET gate.'
@solve(F, 'example', 16, '16–1')
def _():
    R, C, R3, rds = 10e3, 0.01e-6, 1.0e3, 500.0; fr = 1 / (2 * math.pi * R * C); Rf = (3 - 1) * (R3 + rds); must_near('EXAMPLE 16–1', ['1.59 kHz', '3.0 k'], span=4200); close(fr, 1.59e3, 3e-3); close(Rf, 3.0e3, 1e-9)
    s = 2j * math.pi * fr; Z1 = R + 1 / (s * C); Z2 = R / (1 + s * R * C); B = Z2 / (Z1 + Z2); close(abs(B), 1 / 3, 1e-9); close(cmath.phase(B), 0.0, 1e-9, 1e-9)                                  # independent: the lead-lag network has B = 1/3 and 0° shift at fr
    return [('Resonant frequency fr = 1/(2πRC)', si(fr, 'Hz', 3)), ('Rf for a closed-loop gain of 3: Rf = (Av − 1)(R3 + r′ds)', si(Rf, 'Ω', 3))], 'Wien-bridge: fr = 1/(2πRC); oscillations need a closed-loop gain of 3 to offset the lead-lag attenuation 1/3, and the amplifier is a noninverting stage with Ri = R3 + r′ds (Floyd §16–2). The book prints 1.59 kHz and 3.0 kΩ.', [], None, C1612
C1614 = 'Figure 16–14 (p.816): three-section RC phase-shift oscillator: an inverting op-amp with feedback resistor Rf; the feedback network is three series capacitors C1 = C2 = C3 = 0.001 μF with shunt resistors R1 = R2 = R3 = 10 kΩ in Example 16–2; the loop gain needs Acl = 29, B = R3/Rf = 1/29.'
@solve(F, 'related_problem', 16, '16–2')
def _():
    R, C = 8.2e3, 0.001e-6; Rf = 29 * R; fr = 1 / (2 * math.pi * math.sqrt(6) * R * C); R0 = 10e3; close(29 * R0, 290e3, 1e-12); close(1 / (2 * math.pi * math.sqrt(6) * R0 * C), 6.5e3, 1e-2)       # Example 16–2 as printed: 290 kΩ and 6.5 kHz
    f180 = _brentq(lambda f: hp_ladder(R, C, f).imag, 1e3, 1e5); Bx = hp_ladder(R, C, f180); close(f180, fr, 5e-3); close(abs(Bx), 1 / 29, 1e-2); assert Bx.real < 0                           # independent: exact ladder, phase 180° at fr, attenuation 1/29
    return [('(a) Rf = 29·R3', si(Rf, 'Ω', 3)), ('(b) fr = 1/(2π√6·R·C)', si(fr, 'Hz', 3))], 'Phase-shift oscillator: the three-section network attenuates by 29 at fr = 1/(2π√6·RC) with a phase shift of 180°, so the inverting amplifier needs Acl = 29: Rf = 29·R3 (Floyd §16–2).', [f'Exact solution of the unloaded three-section network: 180° at {si(f180, "Hz", 4)} with attenuation {g(1 / abs(Bx), 3)}.'], None, C1614
C1621 = 'Figure 16–21 (p.821): Colpitts oscillator, +12 V: bias resistors R1, R2, collector resistor R3, emitter resistor R4, coupling/bypass capacitors C3, C4, C5; the tank is L = 50 mH with C1 = 0.1 μF and C2 = 0.01 μF in series (the capacitive divider gives the feedback).'
def tank_f(L, Ct, Q):
    """Exact frequency of a parallel tank whose coil loss (series resistance giving Q = ωL/R) is included: zero of the imaginary part of the admittance."""
    w0 = 1 / math.sqrt(L * Ct); R = w0 * L / Q
    Y = lambda w: 1 / (R + 1j * w * L) + 1j * w * Ct; return _brentq(lambda w: Y(w).imag, 0.5 * w0, 1.5 * w0) / (2 * math.pi)
@solve(F, 'related_problem', 16, '16–3')
def _():
    L, C1, C2 = 50e-3, 0.1e-6, 0.01e-6; Ct = C1 * C2 / (C1 + C2); f0 = 1 / (2 * math.pi * math.sqrt(L * Ct)); close(f0, 7.46e3, 3e-3); close(f0 * math.sqrt(64 / 65), 7.40e3, 3e-3)                          # Example 16–3 as printed (7.46 kHz, 7.40 kHz at Q = 8)
    f4 = f0 * math.sqrt(16 / 17); ex = tank_f(L, Ct, 4.0); close(ex, f4, 1e-2)                                                                                                                    # independent: exact lossy-tank admittance
    return [('CT = C1·C2/(C1 + C2) and f0 = 1/(2π√(L·CT))', f'{si(Ct, "F", 3)}, {si(f0, "Hz", 4)}'), ('Frequency for Q = 4: fr = f0·√(Q²/(Q² + 1))', si(f4, 'Hz', 4))], 'The resonant frequency of a loaded tank is fr = f0·√(Q²/(Q² + 1)) (Floyd §16–4, Example 16–3 uses it for Q = 8: 7.40 kHz): for Q = 4, fr = 7.46 kHz × 0.9701.', [f'An exact admittance calculation of a coil with Q = 4 gives {si(ex, "Hz", 4)} (the textbook factor is an approximation).'], None, C1621
C1630 = 'Figure 16–30 (p.827): triangular-wave oscillator with two op-amps: an integrator with R1 = 10 kΩ and C = 0.01 μF (input from the comparator output) and a comparator with hysteresis whose positive-feedback resistors are R2 = 33 kΩ and R3 = 10 kΩ; the comparator output swings between +Vmax and −Vmax. Book formulas: VUTP = +Vmax·(R3/R2), fr = (1/(4R1C))(R2/R3).'
def tri_osc(R1, C, R2, R3, Vmax):
    """Time-stepped two-op-amp triangle oscillator: the integrator ramps at ∓Vmax/(R1C); the comparator flips at ±Vmax·R3/R2.  Returns (peak, frequency)."""
    th = Vmax * R3 / R2; dt = R1 * C / 4000; v, s, t, flips, vmax = 0.0, 1, 0.0, [], 0.0
    for _ in range(2_000_000):
        v += -s * Vmax * dt / (R1 * C); t += dt; vmax = max(vmax, abs(v))
        if s > 0 and v <= -th: s = -1; flips.append(t)
        elif s < 0 and v >= th: s = 1; flips.append(t)
        if len(flips) >= 6: break
    return vmax, 1 / (flips[5] - flips[3])
@solve(F, 'related_problem', 16, '16–4')
def _():
    R1, C, R2, R3, Vmax = 10e3, 0.01e-6, 33e3, 10e3, 10.0; fr = 1 / (4 * R1 * C) * R2 / R3; close(fr, 8.25e3, 1e-3)                                                                                  # Example 16–4 as printed
    A = Vmax * R3 / R2; pk, fs = tri_osc(R1, C, R2, R3, Vmax); close(pk, A, 2e-3); close(fs, 1 / (4 * R1 * C) * R2 / R3, 3e-3)
    return [('Trigger points VUTP = +Vmax·R3/R2, VLTP = −Vmax·R3/R2', f'±{g(A, 3)} V'), ('Peak-to-peak amplitude of the triangular wave', f'{g(2 * A, 3)} V')], 'The comparator trigger points set the triangle: VUTP = +Vmax(R3/R2), VLTP = −Vmax(R3/R2) (Floyd §16–5): ±10 V × 10 kΩ/33 kΩ. The frequency (8.25 kHz) does not depend on Vmax.', [f'A time-stepped simulation of the integrator and comparator gives a peak of {g(pk, 3)} V and {si(fs, "Hz", 3)}.'], None, C1630
@solve(F, 'example', 16, '16–3')
def _():
    L, C1, C2 = 50e-3, 0.1e-6, 0.01e-6; Ct = C1 * C2 / (C1 + C2); f0 = 1 / (2 * math.pi * math.sqrt(L * Ct)); fq = f0 * math.sqrt(64 / 65); must_near('EXAMPLE 16–3', ['0.0091 μF', '7.46 kHz', '7.40 kHz'], span=4200)
    close(f0, 7.46e3, 3e-3); close(fq, 7.40e3, 3e-3); ex = tank_f(L, Ct, 8.0); close(ex, fq, 1e-2)
    return [('(a) CT = C1·C2/(C1 + C2)', si(Ct, 'F', 3)), ('(a) fr = 1/(2π√(L·CT))', si(f0, 'Hz', 4)), ('(b) fr = f0·√(Q²/(Q² + 1)) for Q = 8', si(fq, 'Hz', 4))], 'Colpitts oscillator: the tank capacitors C1 and C2 are in series, fr = 1/(2π√(L·CT)); a loaded tank lowers it by √(Q²/(Q² + 1)) (Floyd §16–4). The book prints 0.0091 μF, 7.46 kHz and 7.40 kHz.', [f'Exact lossy-tank solution for Q = 8: {si(ex, "Hz", 4)}.'], None, C1621
@solve(F, 'example', 16, '16–4')
def _():
    R1, C, R2, R3 = 10e3, 0.01e-6, 33e3, 10e3; fr = 1 / (4 * R1 * C) * R2 / R3; R1n = 1 / (4 * 20e3 * C) * R2 / R3; must_near('EXAMPLE 16–4', ['8.25 kHz', '4.13 k'], span=3000); close(fr, 8.25e3, 1e-3); close(R1n, 4.13e3, 2e-3)
    pk, fs = tri_osc(R1, C, R2, R3, 12.0); close(fs, fr, 3e-3); pk2, fs2 = tri_osc(R1n, C, R2, R3, 12.0); close(fs2, 20e3, 3e-3)                                                                  # independent: time-stepped simulation
    return [('Frequency fr = (1/(4R1C))(R2/R3)', si(fr, 'Hz', 3)), ('R1 for 20 kHz: R1 = (1/(4·f·C))(R2/R3)', si(R1n, 'Ω', 3))], 'Triangular-wave oscillator (Floyd Eq. 16–10); the book prints 8.25 kHz and 4.13 kΩ.', ['The simulation of the integrator + comparator confirms both frequencies.'], None, C1630
C1632 = 'Figure 16–32 (p.828): sawtooth generator with a PUT: an op-amp integrator whose input resistor Ri = 100 kΩ is fed from a divider between −15 V: R1 = 68 kΩ (to −15 V) and R2 = 10 kΩ (to ground); feedback capacitor C = 0.0047 μF; the PUT (anode at the − input, cathode at the output through the gate network) has its gate at the divider R3 = 10 kΩ (from +15 V) and R4 = 10 kΩ (to ground), so VG = 7.5 V.'
def saw(VCC, R3, R4, R1, R2, Ri, C, VF=1.0):
    VG = VCC * R4 / (R3 + R4); VIN = -VCC * R2 / (R1 + R2); Vp = VG; f = abs(VIN) / (Ri * C) / (Vp - VF); return VG, VIN, Vp - VF, f
@solve(F, 'example', 16, '16–5')
def _():
    VG, VIN, Vpp, f = saw(15, 10e3, 10e3, 68e3, 10e3, 100e3, 0.0047e-6); must_near('EXAMPLE 16–5', ['7.5 V', '6.5 V', '−1.92 V', '628 Hz', '1.59 ms'], span=4400); close(VG, 7.5, 1e-9); close(Vpp, 6.5, 1e-9); close(VIN, -1.92, 3e-3); close(f, 628, 3e-3)
    I = abs(VIN) / 100e3; C = 0.0047e-6; t = 0.0; v = 1.0
    while v < VG: v += I / C * 1e-7; t += 1e-7                                                       # independent: charge the capacitor at the constant current
    close(1 / t, f, 2e-3)
    return [('Gate voltage VG = R4/(R3 + R4)·(+V) = peak of the sawtooth', f'{g(VG, 3)} V'), ('Peak-to-peak amplitude Vp − VF', f'{g(Vpp, 3)} V (from 1 V to 7.5 V)'), ('Input voltage VIN = R2/(R1 + R2)·(−V)', f'{g(VIN, 3)} V'), ('Frequency f = (|VIN|/(Ri·C))(1/(Vp − VF))', si(f, 'Hz', 3) + f' (period {g(1e3 / f, 3)} ms)'),
            ('(b) waveform', 'a sawtooth ramping from about 1 V up to 7.5 V in 1.59 ms, then dropping back quickly when the PUT fires')], 'PUT sawtooth generator (Floyd §16–5): the ramp slope is |VIN|/(Ri·C) and the PUT fires when the output reaches VG. The book prints 7.5 V, 6.5 V, 628 Hz and 1.59 ms.', \
        [f'The book neglects the loading of the 68 kΩ/10 kΩ divider by Ri (the current is taken as |VIN|/Ri); including it lowers the frequency to about {si(1 / ((VG - 1.0) * 0.0047e-6 / (abs(-15 * 10e3 / 78e3) / (68e3 * 10e3 / 78e3 + 100e3))), "Hz", 3)}.'], None, C1632
@solve(F, 'related_problem', 16, '16–5')
def _():
    VG, VIN, Vpp, f = saw(15, 10e3, 10e3, 68e3, 10e3, 56e3, 0.0047e-6); close(f, 628 * 100 / 56, 3e-3)
    load = (VG - 1.0) * 0.0047e-6 / (abs(VIN) / (68e3 * 10e3 / 78e3 + 56e3)); I = abs(VIN) / 56e3; C = 0.0047e-6; t = 0.0; v = 1.0
    while v < VG: v += I / C * 1e-7; t += 1e-7
    close(1 / t, f, 2e-3)
    return [('f = (|VIN|/(Ri·C))(1/(Vp − VF)) with Ri = 56 kΩ', si(f, 'Hz', 4)), ('Ratio to Example 16–5', 'the slope is inversely proportional to Ri: 628 Hz × 100 kΩ/56 kΩ')], 'Same method as Example 16–5: VIN = −1.92 V, Vp − VF = 6.5 V, now with Ri = 56 kΩ.', [f'Including the loading of the divider by Ri (not done in the book) the frequency would be about {si(1 / load, "Hz", 3)}.'], None, C1632
C1641 = 'Figure 16–41 (p.834): astable 555 timer on +5.5 V: R1 = 2.2 kΩ (VCC to the discharge pin), R2 = 4.7 kΩ (discharge pin to the threshold/trigger pins), Cext = 0.022 μF to ground, 0.01 μF on the control pin. Figure 16–40: a diode D1 across R2 makes Cext charge through R1 only.'
@solve(F, 'example', 16, '16–6')
def _():
    R1, R2, C = 2.2e3, 4.7e3, 0.022e-6; f = 1.44 / ((R1 + 2 * R2) * C); duty = (R1 + R2) / (R1 + 2 * R2) * 100; must_near('EXAMPLE 16–6', ['5.64 kHz', '59.5%'], span=2600); close(f, 5.64e3, 2e-3); close(duty, 59.5, 2e-3)
    fs, ds = sim555(R1, R2, C, 5.5); close(fs, f, 8e-3); close(ds * 100, duty, 5e-3)                                  # independent: time-stepped 555 (thresholds 2/3 and 1/3 of VCC)
    return [('Frequency f = 1.44/((R1 + 2R2)·Cext)', si(f, 'Hz', 3)), ('Duty cycle = (R1 + R2)/(R1 + 2R2)', f'{g(duty, 3)} %')], '555 astable (Floyd Eq. 16–12 and 16–13). The book prints 5.64 kHz and 59.5 %.', [f'A time-stepped simulation gives {si(fs, "Hz", 4)} and {g(100 * ds, 3)} % (the book\'s 1.44 is 1/0.694).'], None, C1641
@solve(F, 'related_problem', 16, '16–6')
def _():
    R1, R2, C = 2.2e3, 4.7e3, 0.022e-6; duty = R1 / (R1 + R2) * 100; tH, tL = 0.694 * R1 * C, 0.694 * R2 * C; f = 1 / (tH + tL)
    fs, ds = sim555(R1, R2, C, 5.5, diode=True); close(ds * 100, duty, 5e-3); close(fs, f, 8e-3)
    return [('Duty cycle with the diode across R2: tH = 0.694·R1·C, tL = 0.694·R2·C', f'{g(duty, 3)} %'), ('Frequency 1/(0.694(R1 + R2)Cext)', si(f, 'Hz', 3))], 'With D1 across R2, Cext charges through R1 only and discharges through R2: duty cycle = R1/(R1 + R2) (Floyd §16–6).', ['The diode forward drop (≈ 0.7 V) is neglected, as in the book; a time-stepped simulation confirms the duty cycle.'], None, C1641
C1660 = 'Figure 16–60 (p.848): (a) a transistor oscillator whose tank is L1 = 5 mH with C1 = 100 pF (from the inductor\'s lower end to ground) and C3 = 1000 pF (from the collector to ground, ac), feedback taken from the C1 junction through C2 = 1 μF to the base (C4 = 1 μF bypass); (b) a transistor oscillator with L1 = 1.5 mH and L2 = 10 mH each from a side of the tank to ground and C2 = 470 pF across both (C1, C3, C4 = 1 μF coupling/bypass capacitors).'
@solve(F, 'problem', 16, '12')
def _():
    L1a, C1a, C3a = 5e-3, 100e-12, 1000e-12; Cta = C1a * C3a / (C1a + C3a); fa = 1 / (2 * math.pi * math.sqrt(L1a * Cta))
    L1b, L2b, C2b = 1.5e-3, 10e-3, 470e-12; Ltb = L1b + L2b; fb = 1 / (2 * math.pi * math.sqrt(Ltb * C2b))
    ya = lambda w: 1 / (1j * w * L1a) + 1j * w * Cta; xa = _brentq(lambda w: ya(w).imag, 1e5, 1e8) / (2 * math.pi); close(xa, fa, 1e-6)                                      # independent: zero of the tank susceptance
    yb = lambda w: 1 / (1j * w * Ltb) + 1j * w * C2b; xb = _brentq(lambda w: yb(w).imag, 1e4, 1e8) / (2 * math.pi); close(xb, fb, 1e-6)
    return [('(a) type', 'Colpitts oscillator (one inductor, two capacitors C1 and C3 forming the capacitive divider)'), ('(a) fr = 1/(2π√(L1·CT)), CT = C1·C3/(C1 + C3)', f'CT = {si(Cta, "F", 3)}, fr = {si(fa, "Hz", 4)}'), ('(b) type', 'Hartley oscillator (two inductors L1 and L2 with one capacitor C2)'), ('(b) fr = 1/(2π√(LT·C2)), LT = L1 + L2', f'LT = {si(Ltb, "H", 3)}, fr = {si(fb, "Hz", 4)}')], \
        'Colpitts: fr = 1/(2π√(L·CT)) with the two tank capacitors in series; Hartley: fr = 1/(2π√(LT·C)) with LT = L1 + L2 (Floyd §16–4). Q > 10 so loading is neglected.', ['The two inductors of the Hartley circuit are taken as uncoupled (no mutual inductance is given).', 'The coupling and bypass capacitors (1 μF) are taken as ac shorts.'], None, C1660
@solve(F, 'problem', 16, '16')
def _():
    VG, VIN, Vpp, f = saw(12, 100e3, 47e3, 100e3, 22e3, 100e3, 0.0022e-6); Vp = VG
    I = abs(VIN) / 100e3; C = 0.0022e-6; t = 0.0; v = 1.0
    while v < VG: v += I / C * 1e-7; t += 1e-7
    close(1 / t, f, 2e-3)
    return [('Gate voltage VG = R5/(R4 + R5)·(+12 V) = peak of the output', f'{g(VG, 3)} V'), ('Peak-to-peak amplitude Vp − VF (VF = 1 V)', f'{g(Vpp, 3)} V'), ('Input voltage VIN = R2/(R1 + R2)·(−12 V)', f'{g(VIN, 3)} V'), ('Frequency f = (|VIN|/(R3·C))(1/(Vp − VF))', si(f, 'Hz', 3))], \
        'PUT sawtooth generator solved as Example 16–5: the gate divider R4 = 100 kΩ, R5 = 47 kΩ from +12 V sets the firing level VG; the input divider R1 = 100 kΩ, R2 = 22 kΩ from −12 V sets the ramp current through R3 = 100 kΩ into C = 0.0022 μF.', \
        [f'As in the book\'s Example 16–5 the loading of the input divider by R3 is neglected; including it the frequency would be {si(1 / ((VG - 1.0) * 0.0022e-6 / (abs(VIN) / (100e3 * 22e3 / 122e3 + 100e3))), "Hz", 3)}.'], None, \
        'Figure 16–63 (p.849): PUT sawtooth generator: an op-amp integrator with C = 0.0022 μF; the input R3 = 100 kΩ is fed from the divider R1 = 100 kΩ (to −12 V) and R2 = 22 kΩ (to ground); the PUT gate is set by R4 = 100 kΩ (from +12 V) and R5 = 47 kΩ (to ground).'

# ============================================================================================ Chapter 17 (m08)
C177 = 'Figure 17–7 (p.857): series voltage regulator with an op-amp: the 5.1 V zener D1 (fed from VIN = +15 V through R1 = 1.0 kΩ) is the reference VREF on the + input; the pass transistor Q1 is driven by the op-amp; the feedback divider R2 = 10 kΩ (output to − input) and R3 = 10 kΩ (− input to ground). VOUT = (1 + R2/R3)·VREF (book result 10.2 V).'
@solve(F, 'related_problem', 17, '17–3')
def _():
    Vz, R1, R2, R3, VIN = 3.3, 1.8e3, 22e3, 18e3, 15.0; Vout = (1 + R2 / R3) * Vz
    Aol = 1e8; A = np.array([[1 / R2 + 1 / R3, -1 / R2], [Aol, 1.0]]); v = np.linalg.solve(A, np.array([0.0, Aol * Vz])); close(v[1], Vout, 1e-5)                   # op-amp with Aol = 1e8: Vout = Aol(Vz − V−), V− from the divider
    Iz = (VIN - Vz) / R1; close(Iz * 1e3, 6.5, 1e-9)
    return [('VOUT = (1 + R2/R3)·VREF', f'{g(Vout, 4)} V')], 'Series regulator: the op-amp keeps the voltage at the divider R2/R3 equal to the zener voltage, so VOUT = (1 + R2/R3)·VREF = (1 + 22/18) × 3.3 V (Floyd Eq. 17–3, Example 17–3 gives 10.2 V for 5.1 V and equal resistors).', [f'R1 only sets the zener current ({g(Iz * 1e3, 3)} mA), which is enough to keep the zener in breakdown.'], None, C177
C1715 = 'Figure 17–15 (p.862): series regulator with current limiting: R1 = 22 Ω in series with the input (VIN to the output), the pass transistor Q1 with R2 = 1.0 kΩ, R3 = 10 kΩ and R4 = 10 kΩ; the worst case for R1 is a short-circuited output (VOUT = 0), when all of VIN appears across R1.'
@solve(F, 'example', 17, '17–5')
def _():
    VIN, R1 = 12.5, 22.0; P = VIN ** 2 / R1; must_near('EXAMPLE 17–5', ['7.10 W', '10 W'], span=2000); close(P, 7.10, 2e-3); close(VIN * (VIN / R1), P, 1e-12)
    return [('Worst case: output shorted, VR1 = VIN', f'IR1 = {g(VIN / R1 * 1e3, 4)} mA'), ('Power in R1: PR1 = VR1²/R1', f'{g(P, 3)} W → use a resistor rated at least 10 W')], 'With the output short-circuited VOUT = 0, so VR1 = 12.5 V and PR1 = 12.5²/22 Ω = 7.10 W; choose the next standard rating, 10 W (Floyd §17–2).', [], None, C1715
@solve(F, 'related_problem', 17, '17–5')
def _():
    VIN, R1 = 24.0, 33.0; P = VIN ** 2 / R1; close(VIN * (VIN / R1), P, 1e-12)
    return [('Power in R1: PR1 = VIN²/R1 (output shorted)', f'{g(P, 3)} W → use a resistor rated at least 20 W')], 'Worst case again VOUT = 0: PR1 = 24²/33 Ω = 17.5 W; the next standard rating is 20 W (the printed answer to Problem 15, same method: 6.25 W for 25 V across 100 Ω).', [], None, C1715
C1730 = 'Figure 17–30 (p.872): adjustable LM317 regulator: input +35 V; R1 = 220 Ω between the output and the adjustment terminal; R2 = 5 kΩ (maximum) potentiometer from the adjustment terminal to ground; decoupling capacitors C1, C2, C3. VOUT = VREF(1 + R2/R1) + IADJ·R2 with VREF = 1.25 V.'
@solve(F, 'example', 17, '17–6')
def _():
    R1, VREF, IADJ = 220.0, 1.25, 50e-6; f = lambda R2: VREF * (1 + R2 / R1) + IADJ * R2; vmin, vmax = f(0.0), f(5e3); must_near('EXAMPLE 17–6', ['1.25 V', '29.66 V', '0.25 V', '29.9 V'], span=2200); close(vmin, 1.25, 1e-12); close(vmax, 29.9, 2e-3)
    I1 = VREF / R1; close((I1 + IADJ) * 5e3 + VREF, vmax, 1e-12)                                                                                           # independent: loop equation VOUT = VREF + (IR1 + IADJ)·R2
    return [('VOUT(min), R2 = 0', f'{g(vmin, 3)} V'), ('VOUT(max), R2 = 5 kΩ: VREF(1 + R2/R1) + IADJ·R2', f'{g(VREF * (1 + 5e3 / R1), 4)} V + {g(IADJ * 5e3, 3)} V = {g(vmax, 3)} V')], 'LM317 (Floyd §17–5): the regulator holds VREF = 1.25 V across R1, so the current through R1 plus IADJ flows in R2. The book prints 1.25 V and 29.9 V.', ['The 35 V input is high enough for 29.9 V out (a dropout margin of a few volts is needed).'], None, C1730
C1734 = 'Figure 17–34 (p.876): fixed three-terminal regulator (78xx) with an external pass transistor Qext (pnp): Rext is connected between the input terminal of the regulator and the base/emitter of Qext so that Qext turns on when the current through the regulator (and Rext) makes VRext = 0.7 V; the load current is IL = Iext + Imax.'
@solve(F, 'example', 17, '17–7')
def _():
    Imax = 0.7; Rext = 0.7 / Imax; must_near('EXAMPLE 17–7', ['0.7 V', '0.7 A', '1'], span=1400); close(Rext, 1.0, 1e-12); close(Imax * Rext, 0.7, 1e-12)
    return [('Rext = 0.7 V/Imax', si(Rext, 'Ω', 3))], 'Qext turns on when the voltage across Rext reaches its base-emitter voltage 0.7 V, which happens at Imax = 0.7 V/Rext; so Rext = 0.7 V/0.7 A = 1 Ω (Floyd §17–6). Check with the printed answer of Problem 25: 0.7 V/250 mA = 2.8 Ω.', [], None, C1734
@solve(F, 'example', 17, '17–8')
def _():
    VIN, VOUT, RL, Imax = 30.0, 24.0, 10.0, 0.7; IL = VOUT / RL; Iext = IL - Imax; P = Iext * (VIN - VOUT); must_near('EXAMPLE 17–8', ['2.4 A', '1.7 A', '10.2 W'], span=3000); close(P, 10.2, 1e-9)
    return [('Load current IL = VOUT/RL', f'{g(IL, 3)} A'), ('Current through Qext: Iext = IL − Imax', f'{g(Iext, 3)} A'), ('Pext(min) = Iext(VIN − VOUT)', f'{g(P, 3)} W → choose a transistor rated at least 15 W')], 'External pass transistor (Floyd §17–6): the regulator handles Imax = 0.7 A and Qext the rest of the load current, dropping VIN − VOUT = 6 V. The book prints 2.4 A, 1.7 A and 10.2 W.', ['No heat sink is assumed, as stated.'], None, C1734
C1748 = 'Figure 17–48 (p.890): shunt voltage regulator: R1 = 100 Ω in series between VIN and VOUT; the shunt transistor Q1 (collector at VOUT, emitter to ground) is driven by an op-amp whose − input is the 5.1 V zener (fed by R2 = 12 kΩ from VIN) and whose + input is the divider R3 = 10 kΩ (from VOUT) and R4 = 3.9 kΩ (to ground); the load is the variable RL.'
@solve(F, 'problem', 17, '14')
def _():
    Vz, R3, R4, R1, VIN = 5.1, 10e3, 3.9e3, 100.0, 17.0; Vreg = Vz * (R3 + R4) / R4
    d = lambda V: V / 1.2e3 - V / 1e3                                                                                                          # change of IL when RL goes from 1 kΩ to 1.2 kΩ at fixed VOUT; the shunt current changes by the opposite amount (R1 and divider currents are constant)
    I1 = (VIN - Vreg) / R1; close(I1 * R1 + Vreg, VIN, 1e-12)
    return [('Shunt current: IQ1 = (VIN − VOUT)/R1 − IL − I(R3 + R4); with VOUT, R1 and the divider unchanged, ΔIQ1 = −ΔIL', f'IL falls from VOUT/1 kΩ to VOUT/1.2 kΩ, so IQ1 INCREASES by VOUT·(1/1 kΩ − 1/1.2 kΩ) = VOUT/6 kΩ'), ('For VOUT = 17 V (the input voltage)', f'ΔIQ1 = +{g(-d(17.0) * 1e3, 3)} mA'), ('For the regulated value VOUT = 5.1 V(1 + R3/R4) = 18.2 V', f'ΔIQ1 = +{g(-d(Vreg) * 1e3, 3)} mA')], \
        'Shunt regulator: Q1 takes the current that the load does not (Floyd §17–3); the series current through R1 is fixed when VIN and VOUT are fixed. The change in shunt current equals the decrease of the load current, ≈ 3 mA.', \
        [f'The design output of this circuit is 5.1 V × (10 kΩ + 3.9 kΩ)/3.9 kΩ = {g(Vreg, 4)} V, which is higher than the 17 V input in the statement (the regulator could not reach it); so the numbers above are given for both VOUT = 17 V and 18.2 V. The change is about 3 mA either way.', 'R1 = 100 Ω is confirmed by the printed answers of Problems 13 (1 V/100 Ω = 10 mA) and 15 (25 V/100 Ω = 250 mA, 6.25 W).'], None, C1748
C1749 = 'Figure 17–49 (p.891): basic step-down switching regulator: +12 V input, series MOSFET Q1 driven by a modulator (f0 = 10 kHz, toff = 60 μs), freewheeling diode D1, inductor L, output capacitor C, load RL; the feedback divider R2 = 10 kΩ and R3 = 15 kΩ is compared with the 2.7 V zener D2 (fed through R1 = 4.7 kΩ) to set the pulse width.'
@solve(F, 'problem', 17, '16')
def _():
    VIN, f, toff = 12.0, 10e3, 60e-6; T = 1 / f; ton = T - toff; D = ton / T; Vout = D * VIN; close(D, 0.40, 1e-9)                                              # Problem 17 (same circuit) prints a duty cycle of 40 %
    t = np.linspace(0, T, 100001)[:-1]; sw = (t < ton).astype(float); close(float(np.mean(sw)) * VIN, Vout, 1e-3)                                           # independent: average of the switched waveform
    Vreg = 2.7 * (10e3 + 15e3) / 15e3
    return [('Period T = 1/f and on-time ton = T − toff', f'T = {g(T * 1e6, 3)} μs, ton = {g(ton * 1e6, 3)} μs'), ('Duty cycle D = ton/T', f'{g(100 * D, 3)} %'), ('VOUT = D·VIN (average of the chopped input)', f'{g(Vout, 3)} V')], 'Step-down switching regulator (Floyd §17–4): the inductor/capacitor filter averages the switched waveform, VOUT = (ton/T)·VIN = 0.4 × 12 V.', \
        [f'Ideal switch and diode (no drops). The feedback network of the figure, 2.7 V × (10 kΩ + 15 kΩ)/15 kΩ = {g(Vreg, 3)} V, is the voltage the loop would regulate to by adjusting ton; with the fixed 60 μs off-time given here the output is 4.8 V.'], None, C1749
C1752 = 'Figure 17–52 (p.893): LM337 negative adjustable regulator: input −35 V; R1 = 470 Ω between the output and the adjustment terminal; R2 = 10 kΩ potentiometer from the adjustment terminal to ground. |VOUT| = 1.25 V(1 + R2/R1) + IADJ·R2.'
@solve(F, 'problem', 17, '22')
def _():
    R1, VREF, IADJ = 470.0, 1.25, 50e-6; f = lambda R2: VREF * (1 + R2 / R1) + IADJ * R2; vmin, vmax = f(0.0), f(10e3)
    I1 = VREF / R1; close(VREF + (I1 + IADJ) * 10e3, vmax, 1e-12)
    return [('Minimum output (R2 = 0)', f'−{g(vmin, 3)} V'), ('Maximum output (R2 = 10 kΩ): −[1.25 V(1 + R2/R1) + IADJ·R2]', f'−[{g(VREF * (1 + 10e3 / R1), 4)} V + {g(IADJ * 10e3, 3)} V] = −{g(vmax, 4)} V')], 'The LM337 is the negative counterpart of the LM317 (Floyd §17–5): the same formula applies to the magnitude, with the output negative. The input of −35 V is more negative than −28.4 V by enough margin.', ['The sign convention of IADJ for the LM337 is taken as for the LM317 (it adds to the drop in R2), as in Example 17–6.'], None, C1752
C1753 = 'Figure 17–53 (p.894): fixed regulator (7809 in the figure; a 7812 in Problem 26) with an external pass transistor Qext and Rext as in Figure 17–34, input +15 V, output decoupling C2.'
@solve(F, 'problem', 17, '26')
def _():
    VIN, VOUT, RL, Imax = 15.0, 12.0, 10.0, 0.5; IL = VOUT / RL; Iext = IL - Imax; P = Iext * (VIN - VOUT); Rext = 0.7 / Imax
    close(P, 0.7 * 3.0, 1e-9); close(Iext + Imax, IL, 1e-12); close(0.7 / 0.25, 2.8, 1e-9)                                                  # Problem 25's printed answer (2.8 Ω for 250 mA) confirms the Rext rule
    return [('Load current IL = VOUT/RL', f'{g(IL, 3)} A'), ('External current Iext = IL − Imax', f'{g(Iext, 3)} A'), ('Power in Qext: Pext = Iext(VIN − VOUT)', f'{g(P, 3)} W'), ('(Rext for Imax = 500 mA)', si(Rext, 'Ω', 3))], 'Floyd Example 17–8 method: Qext carries the part of the load current that the regulator does not (1.2 A − 0.5 A) and drops VIN − VOUT = 15 V − 12 V = 3 V.', ['The input voltage 15 V is read from Figure 17–53 (the 7812 needs a few volts more than 12 V, which 15 V gives).'], None, C1753
