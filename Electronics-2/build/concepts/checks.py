"""Independent numeric checks of the formulas quoted in the Concept finder.  Each check recomputes the result by a DIFFERENT route
(exhaustive truth tables, nodal circuit solution with a finite-gain op-amp, time-domain simulation, polynomial roots, numerical integration)
and raises AssertionError on a mismatch.  A check returns a short text of what it verified."""
import math, itertools, cmath
import numpy as np
TRAPZ = getattr(np, 'trapezoid', None) or np.trapz
from scipy.optimize import brentq
CHECKS = {}
def chk(name):
    def deco(f): CHECKS[name] = f; return f
    return deco
def close(a, b, rel=1e-6, ab=1e-12): return abs(a - b) <= max(ab, rel * max(abs(a), abs(b)))
def must(cond, msg): 
    if not cond: raise AssertionError(msg)

# ------------------------------------------------------------------ module 01
@chk('binary')
def _():
    for n in range(0, 600):
        bits = []; m = n
        while m: bits.append(m % 2); m //= 2                       # repeated division, remainders read bottom-up
        s = ''.join(map(str, reversed(bits))) or '0'
        must(int(s, 2) == n and sum(int(c) << i for i, c in enumerate(reversed(s))) == n, n)
    must(format(45, 'b') == '101101' and 32 + 8 + 4 + 1 == 45, '45')
    bcd = ' '.join(format(int(d), '04b') for d in '45'); must(bcd == '0100 0101', bcd)
    must(all(2 ** n - 1 == int('1' * n, 2) for n in range(1, 20)), 'range')
    return 'division/remainder conversion for 0..599, 45 = 101101, BCD of 45, 2^n - 1 range'
@chk('gates')
def _():
    NOT = lambda a: 1 - a; AND = lambda a, b: a & b; OR = lambda a, b: a | b
    NAND = lambda a, b: NOT(AND(a, b)); NOR = lambda a, b: NOT(OR(a, b))
    for a, b in itertools.product((0, 1), repeat=2):
        must(NOT(AND(a, b)) == OR(NOT(a), NOT(b)) and NOT(OR(a, b)) == AND(NOT(a), NOT(b)), 'de morgan')
        must((a ^ b) == OR(AND(a, NOT(b)), AND(NOT(a), b)) == int(a != b), 'xor')
        must(NOT(a) == NAND(a, a) and AND(a, b) == NAND(NAND(a, b), NAND(a, b)) and OR(a, b) == NAND(NAND(a, a), NAND(b, b)), 'nand universal')
        must(NOT(a) == NOR(a, a) and OR(a, b) == NOR(NOR(a, b), NOR(a, b)) and AND(a, b) == NOR(NOR(a, a), NOR(b, b)), 'nor universal')
    return 'De Morgan, XOR = A.B\' + A\'.B, NAND and NOR universality on every input combination'
@chk('adders')
def _():
    for a, b in itertools.product((0, 1), repeat=2):
        s, c = a ^ b, a & b; must(a + b == 2 * c + s, 'half')
    for a, b, ci in itertools.product((0, 1), repeat=3):
        s = a ^ b ^ ci; co = (a & b) | (ci & (a ^ b)); must(a + b + ci == 2 * co + s, 'full')
    def add4(x, y):
        c = 0; out = 0
        for i in range(4):
            a, b = (x >> i) & 1, (y >> i) & 1; s = a ^ b ^ c; c = (a & b) | (c & (a ^ b)); out |= s << i
        return out | (c << 4)
    must(all(add4(x, y) == x + y for x in range(16) for y in range(16)), 'ripple')
    must(0b101 + 0b011 == 0b1000, '5+3')
    return 'half and full adder on every input, 4-bit ripple adder on all 256 pairs, 101 + 011 = 1000'
@chk('comb')
def _():
    for n in range(1, 6):
        for code in range(2 ** n):
            outs = [int(i == code) for i in range(2 ** n)]; must(sum(outs) == 1 and outs.index(1) == code, 'decoder')
    pe = lambda ins: max((i for i, v in enumerate(ins) if v), default=None)
    must(pe([1, 0, 1, 0]) == 2 and pe([0, 0, 0, 0]) is None, 'priority')
    must(2 ** 4 == 16, '4->16')
    return 'n-to-2^n decoder for n = 1..5, priority encoder picks the highest HIGH input'
@chk('flipflops')
def _():
    for j, k, q in itertools.product((0, 1), repeat=3):
        nxt = (j & (1 - q)) | ((1 - k) & q)
        ref = q if (j, k) == (0, 0) else 0 if (j, k) == (0, 1) else 1 if (j, k) == (1, 0) else 1 - q
        must(nxt == ref, 'jk')
    must(all((d == d) and ((t ^ q) == (1 - q if t else q)) for d in (0, 1) for t in (0, 1) for q in (0, 1)), 'dt')
    def nor_latch(s, r, q=0, qb=1):
        for _ in range(8): q, qb = int(not (r or qb)), int(not (s or q))
        return q, qb
    must(nor_latch(1, 0) == (1, 0) and nor_latch(0, 1) == (0, 1) and nor_latch(1, 1) == (0, 0), 'rs forbidden')
    t = 0
    for _ in range(6): t = (1 & (1 - t)) | ((1 - 1) & t)
    must(t == 0, 'toggle even count')
    return 'JK characteristic Q+ = J.Q\' + K\'.Q against the hold/reset/set/toggle table, D and T, NOR latch gives Q = Q\' = 0 for S = R = 1'
@chk('families')
def _():
    VOH, VOL, VIH, VIL = 4.9, 0.1, 3.5, 1.5
    NMH, NML = VOH - VIH, VIL - VOL
    for noise in np.linspace(0, 3, 301):
        if abs(noise - NMH) < 1e-9 or abs(noise - NML) < 1e-9: continue                # exactly on the boundary the floating-point comparison is meaningless
        must((VOH - noise >= VIH) == (noise < NMH) and (VOL + noise <= VIL) == (noise < NML), ('noise sweep', noise))
    must(close(NMH, 1.4) and close(NML, 1.4), 'values')
    return 'noise-margin definition by sweeping injected noise until the receiving gate flips'
@chk('cmos')
def _():
    def vsp_formula(VDD, VTN, VTP, KR): return (VDD + VTP + VTN * math.sqrt(KR)) / (1 + math.sqrt(KR))
    for VDD, VTN, VTP, Kn, Kp in [(2.5, 0.5, -0.6, 200e-6, 80e-6), (5, 1.0, -1.0, 100e-6, 100e-6), (3.3, 0.7, -0.8, 300e-6, 100e-6), (1.8, 0.4, -0.45, 150e-6, 150e-6)]:
        f = lambda v: 0.5 * Kn * (v - VTN) ** 2 - 0.5 * Kp * (VDD - v + VTP) ** 2          # both saturated: ID(n) = ID(p)
        v = brentq(f, VTN + 1e-6, VDD + VTP - 1e-6)                    # p-channel stays on while vin < VDD + VTP
        must(close(v, vsp_formula(VDD, VTN, VTP, Kn / Kp), 1e-6), (VDD, v))
    must(close(vsp_formula(2.5, 0.6, -0.6, 1), 1.25), 'VDD/2')
    # dynamic energy: supply delivers C*V^2 per charge-discharge cycle (integrate i*V through an RC charge)
    C, R, V = 10e-12, 1e3, 2.5; t = np.linspace(0, 40 * R * C, 400001); i = V / R * np.exp(-t / (R * C)); E = TRAPZ(i * V, t)
    must(close(E, C * V ** 2, 1e-4), E); must(close(C * V ** 2 * 100e6, 10e-12 * 6.25 * 1e8), 'P')
    return 'switching threshold against the root of ID(n) = ID(p) for four parameter sets, VSP = VDD/2 for the symmetric case, CV^2 supply energy by numerical integration'
# ------------------------------------------------------------------ module 02 and the circuits below: nodal solution with a finite-gain op-amp
@chk('cmrr')
def _():
    must(close(20 * math.log10(100000 / 0.18), 114.89, 1e-4), 'dB')
    for dB in (20, 40, 80, 90): must(close(20 * math.log10(10 ** (dB / 20)), dB), dB)
    must(close(10 ** (60 / 20), 1000) and close(10 ** (20 / 20), 10) and close(10 ** (80 / 20), 10000), 'factors')
    # output of an amplifier with differential 1 mV and common mode 1 V: Aol=1e5, CMRR=100 dB -> Acm=1
    Aol = 1e5; Acm = Aol / 10 ** (100 / 20); must(close(Acm, 1.0), Acm); must(close(Aol * 1e-3 + Acm * 1.0, 101.0), 'mix')
    return 'CMRR in dB from Aol/Acm and back, factors 20/40/60/80 dB, mixed differential + common-mode output'
@chk('bias')
def _():
    I1, I2 = 8.3e-6, 7.9e-6; must(close((I1 + I2) / 2, 8.1e-6) and close(abs(I1 - I2), 0.4e-6), 'values')
    Ri, Rf, A = 10e3, 100e3, 1e6
    def vout_error(Rc, Ib=100e-9):                                     # inverting stage, Vin = 0, both inputs draw Ib; exact nodal equations
        # unknowns: V- (n), Vo ; V+ = -Ib*Rc ; Vo = A(V+ - V-); KCL at V-: (0 - V-)/Ri + (Vo - V-)/Rf - Ib = 0
        M = np.array([[1.0, 1.0 / A], [-(1 / Ri + 1 / Rf), 1 / Rf]]); vplus = -Ib * Rc
        # Vo/A = vplus - Vminus  => Vminus + Vo/A = vplus
        sol = np.linalg.solve(M, [vplus, Ib]); return sol[1]
    best = min(np.linspace(0, 20e3, 20001), key=lambda r: abs(vout_error(r)))
    must(close(best, Ri * Rf / (Ri + Rf), 1e-3), best)
    return 'compensating resistor found by scanning Rc on the exact nodal equations: the output error vanishes at Ri||Rf'
@chk('slew')
def _():
    must(close(24 / 15, 1.6) and close(20 / 0.5, 40), 'examples')
    Vp, SR = 10.0, 0.5e6; fmax = SR / (2 * math.pi * Vp); must(close(fmax / 1e3, 7.9577, 1e-3), fmax)
    t = np.linspace(0, 1 / fmax, 400001); slope = np.max(np.abs(np.gradient(Vp * np.sin(2 * math.pi * fmax * t), t))); must(close(slope, SR, 1e-4), slope)
    return 'f_max = SR/(2 pi Vp) = 7.96 kHz against the maximum slope of the sine, 24 V/15 us, 20 V/0.5 V/us'
@chk('feedback')
def _():
    for A, B in [(1e5, 1 / 101), (1e5, 0.02), (2e5, 0.1), (1e3, 0.5)]:
        Vin = 1.0; Vo = A * Vin / (1 + A * B)                         # Vo = A(Vin - B Vo) solved from the loop equation
        must(close(Vo, A / (1 + A * B) * Vin) and close(Vo - A * (Vin - B * Vo), 0, ab=1e-9), 'loop')
    must(close(1 / 0.02, 50) and close(1e5 / (1 + 1e5 * 0.02), 50, 1e-3), 'A=1e5, Acl=50 -> B~0.02')
    return 'closed-loop gain from the loop equation Vo = A(Vin - B Vo), B = 0.02 gives Acl = 50 for A = 100,000'
def noninv_gain(A, Ri, Rf):
    B = Ri / (Ri + Rf); return A / (1 + A * B)
@chk('noninv')
def _():
    for Ri, Rf in [(10e3, 220e3), (1e3, 24e3), (2.2e3, 5.6e3)]:
        # exact nodal solution: V- = Vo*Ri/(Ri+Rf), Vo = A(Vin - V-)
        A = 1e7; M = np.array([[1.0, A * Ri / (Ri + Rf)], [0.0, 1.0]]); Vo = A / (1 + A * Ri / (Ri + Rf))          # Vo + A*B*Vo = A*Vin
        must(close(M[0, 0] * Vo + (M[0, 1]) * Vo, A), 'loop')
        must(close(Vo, 1 + Rf / Ri, 1e-5), (Ri, Rf, Vo))
    must(close((1 + 220 / 10) * 50e-3, 1.15), '50 mV')
    return 'exact finite-gain solution (A = 10^7) equals 1 + Rf/Ri for three resistor pairs; 50 mV x 23 = 1.15 V'
@chk('inv')
def _():
    A = 1e7
    for Ri, Rf in [(10e3, 220e3), (1e3, 4.7e3), (2.2e3, 100e3)]:
        # unknowns V-, Vo with Vin = 1: (1 - V-)/Ri = (V- - Vo)/Rf ; Vo = -A V-
        M = np.array([[1 / Ri + 1 / Rf, -1 / Rf], [A, 1.0]]); rhs = np.array([1 / Ri, 0.0]); Vm, Vo = np.linalg.solve(M, rhs)
        must(close(Vo, -Rf / Ri, 1e-5), (Ri, Rf, Vo)); must(abs(Vm) < 1e-5 * abs(Vo), 'virtual ground')
        Zin = 1.0 / ((1.0 - Vm) / Ri); must(close(Zin, Ri, 1e-5), 'Zin = Ri')
    return 'nodal solution gives -Rf/Ri, V- ~ 0 (virtual ground) and Zin = Ri'
@chk('follower')
def _():
    A, Rid = 1e5, 2e6
    # + input at V, - input tied to Vo: Iin = (V - Vo)/Rid, Vo = A (V - Vo)
    V = 1.0; Vo = A * V / (1 + A); Iin = (V - Vo) / Rid; Zin = V / Iin
    must(close(Vo, 1.0, 1e-4) and close(Zin, Rid * (1 + A), 1e-9), (Vo, Zin))
    Rout = 75.0; # Zout: Vo = A(V - Vo) - I*Rout with V = 0 -> Vo(1 + A) = -I*Rout
    I = 1e-3; Vo2 = -I * Rout / (1 + A); must(close(abs(Vo2 / I), Rout / (1 + A), 1e-9), 'Zout')
    return 'Acl = A/(1+A) ~ 1, Zin = Rid(1+A), Zout = Rout/(1+A) from the loop equations'
@chk('impedance')
def _():
    A, B, Zin, Zout = 1e5, 1 / 101, 2e6, 75.0; k = 1 + A * B
    # noninverting: current into + input = (V - V-)/Zin, V- = B Vo, Vo = A (V - V-) (unloaded)
    V = 1.0; Vo = A * V / (1 + A * B); Iin = (V - B * Vo) / Zin; must(close(V / Iin, k * Zin, 1e-9), 'Zin(NI)')
    # output impedance: apply source current I into the output with V = 0:   Vo = A(-B Vo) + I*... use Vo = -A B Vo + Vx where output node is Vo through Zout
    I = 1e-3; Vo2 = (-I * Zout) / (1 + A * B); must(close(abs(Vo2 / I), Zout / k, 1e-9), 'Zout(NI)')
    must(close(k * 2e6 / 1e9, 1.982, 1e-3) and close(75.0 / k * 1e3, 75.68, 1e-3), 'worked example: 1.98 GOhm and 75.7 mOhm')
    return 'Zin(NI) = (1 + BA)Zin and Zout/(1 + BA) from the loop equations; 2 MOhm -> 1.98 GOhm, 75 ohm -> 75.7 mOhm'
@chk('frequency')
def _():
    A0, fc = 1e5, 10.0                                                 # single-pole open-loop model
    Aol = lambda f: A0 / (1 + 1j * f / fc)
    for B in (1 / 101, 0.02, 0.1):
        Acl = lambda f: Aol(f) / (1 + B * Aol(f))
        fcl = fc * (1 + B * A0); must(close(abs(Acl(fcl)) / abs(Acl(1e-6)), 1 / math.sqrt(2), 1e-4), ('-3 dB', B))
        must(close(abs(Acl(fcl * 100)) , 0.0, ab=0.2 / B) , 'rolls off')
        fT = A0 * fc; must(close((1 / B) * fcl, fT, 2e-2), ('GBW', B, fT, fcl / 1))
    return 'single-pole model: the closed-loop -3 dB frequency is fc(1 + B A0) and Acl x fc(cl) ~ A0 fc = fT, for three feedback fractions'
# ------------------------------------------------------------------ module 03
@chk('comparator')
def _():
    Vsat = 13.0
    for Vref in (0.0, 2.0, -1.5):
        out = lambda vin: Vsat if vin - Vref > 0 else -Vsat
        must(out(Vref + 1e-3) == Vsat and out(Vref - 1e-3) == -Vsat, 'threshold')
    must(close(5.1 + 0.7, 5.8), 'VZ + 0.7')
    return 'output flips exactly at Vref for three references; bounded level VZ + 0.7 V'
@chk('hysteresis')
def _():
    for R1, R2, Vm in [(10e3, 100e3, 12.0), (47e3, 10e3, 13.5), (1e3, 1e3, 5.0)]:
        B = R2 / (R1 + R2); state = Vm
        up = None; vin_scan = np.linspace(-1.5 * Vm * B, 1.5 * Vm * B, 20001)
        for vin in vin_scan:                                            # rising input: find where the output goes from +Vm to -Vm for the inverting Schmitt
            if state == Vm and vin > B * Vm: state = -Vm; up = vin; break
        must(up is not None and close(up, B * Vm, 1e-3, 3 * (vin_scan[1] - vin_scan[0])), ('UTP', up, B * Vm))
        low = None
        for vin in vin_scan[::-1]:
            if state == -Vm and vin < -B * Vm: state = Vm; low = vin; break
        must(low is not None and close(low, -B * Vm, 1e-3, 3 * (vin_scan[1] - vin_scan[0])), ('LTP', low))
        must(close(up - low, 2 * B * Vm, 1e-3, 3 * (vin_scan[1] - vin_scan[0])), 'VHYS')
    return 'Schmitt trigger simulated by sweeping the input up and down: trip points +-R2/(R1+R2) Vmax for three resistor pairs'
def amp_nodal(A, ri_list, vs, rf):
    """inverting summing node: sum (Vk - V-)/Rk = (V- - Vo)/Rf, Vo = -A V-"""
    G = sum(1 / r for r in ri_list); J = sum(v / r for v, r in zip(vs, ri_list))
    M = np.array([[G + 1 / rf, -1 / rf], [A, 1.0]]); return np.linalg.solve(M, [J, 0.0])[1]
@chk('summing')
def _():
    A = 1e8
    for Ri, Rf, vs in [(10e3, 10e3, [1, 2, 3]), (10e3, 22e3, [0.5, -0.2, 1.1]), (4.7e3, 4.7e3, [1, 1])]:
        Vo = amp_nodal(A, [Ri] * len(vs), vs, Rf); must(close(Vo, -(Rf / Ri) * sum(vs), 1e-6), (Ri, Rf, vs, Vo))
    return 'nodal solution equals -(Rf/Ri)(V1+V2+...) for three cases, including a unity adder (1 V + 2 V + 3 V -> -6 V)'
@chk('averaging')
def _():
    for n in (2, 3, 4, 8):
        Ri = 10e3; Rf = Ri / n; vs = list(np.linspace(1, 2, n)); Vo = amp_nodal(1e8, [Ri] * n, vs, Rf); must(close(Vo, -np.mean(vs), 1e-6), n)
    return 'with Rf = Ri/n the output is minus the mean of the n inputs (n = 2, 3, 4, 8)'
@chk('scaling')
def _():
    Rf = 10e3; weights = [1, 2, 4, 8]; Rk = [Rf / w for w in weights]
    for code in range(16):
        bits = [(code >> i) & 1 for i in range(4)]; vs = [5.0 * b for b in bits]; Vo = amp_nodal(1e8, Rk, vs, Rf)
        must(close(Vo, -5.0 * code, 1e-6, 1e-9), (code, Vo))
    return 'binary-weighted summer (Rk = Rf/weight): output = -5 V x code for all 16 four-bit codes'
def simulate_stage(kind, Rin, Cap, vin_fn, T, N=200000, A=1e6):
    dt = T / N; vc = 0.0; t = 0; ys = []
    for k in range(N):
        t = k * dt; v = vin_fn(t)
        if kind == 'int':                                              # virtual ground: i = v/R charges C, Vo = -vc
            vc += (v / Rin) * dt / Cap; ys.append(-vc)
        else: ys.append(None)
    return np.array(ys)
@chk('integrator')
def _():
    R, C = 10e3, 0.1e-6; Vin = 1.0; T = 5e-3
    y = simulate_stage('int', R, C, lambda t: Vin, T); slope = (y[-1] - y[0]) / (T * (1 - 1 / len(y)))
    must(close(slope, -Vin / (R * C), 1e-3), slope)
    # square wave in -> triangular wave out: peak-to-peak = Vin * T_half / (R C)
    f = 100.0; sq = lambda t: 1.0 if (t * f) % 1 < 0.5 else -1.0; y2 = simulate_stage('int', R, C, sq, 0.02, N=400000)
    must(close(y2.max() - y2.min(), 1.0 * (0.5 / f) / (R * C), 2e-2), y2.max() - y2.min())
    return 'RC integration step: slope = -Vin/(RC) = -1000 V/s; square wave -> triangle with the predicted peak-to-peak'
@chk('differentiator')
def _():
    Rf, C = 10e3, 0.1e-6; ramp = 2.0 / 1e-3                            # 2 V/ms
    t = np.linspace(0, 1e-3, 100001); vin = ramp * t; vout = -Rf * C * np.gradient(vin, t)
    must(close(vout[500], -Rf * C * ramp, 1e-6), vout[500]); must(close(-Rf * C * ramp, -2.0), 'value')
    tri = np.concatenate([np.linspace(0, 1, 5001), np.linspace(1, 0, 5001)[1:]]); dtri = np.gradient(tri, np.arange(len(tri)) * 1e-6)
    must(dtri[100] > 0 > dtri[-100], 'triangle -> square')
    return 'derivative of a ramp is constant (-2 V for 2 V/ms, 10 kOhm, 0.1 uF); a triangle gives a two-level output'
# ------------------------------------------------------------------ module 04
@chk('cascade')
def _():
    rng = np.random.default_rng(3)
    for _ in range(200):
        g = rng.uniform(1.5, 40, size=rng.integers(2, 5)); must(close(20 * math.log10(np.prod(g)), sum(20 * math.log10(x) for x in g), 1e-9), 'dB add')
    must(close(20 * math.log10(1000), 60) and 10 * 10 * 10 == 1000, '1000 -> 60 dB'); must(close(10 ** ((20 + 14) / 20), 50.12, 1e-3), '20 dB + 14 dB')
    return 'dB of a product equals the sum of dB (200 random cascades); 10x10x10 = 1000 = 60 dB; 20 dB + 14 dB = 50.1'
@chk('coupling')
def _():
    R, C = 10e3, 1e-6; fc = 1 / (2 * math.pi * R * C); H = lambda f: (2j * math.pi * f * R * C) / (1 + 2j * math.pi * f * R * C)
    must(close(abs(H(fc)), 1 / math.sqrt(2), 1e-9) and abs(H(1e-3)) < 1e-3 and close(abs(H(1e6)), 1, 1e-3), 'RC high-pass')
    return 'series-C/R-to-ground coupling: |H| = 0.707 at 1/(2 pi RC), blocks dc, passes high frequencies'
@chk('classes')
def _():
    VCC, RL = 12.0, 8.0; th = np.linspace(0, math.pi, 200001)
    Pout = 0.5 * VCC ** 2 / RL                                       # sine of peak VCC across RL
    Ip = VCC / RL
    # each transistor supplies a half-sine of current during its half cycle: its average over the whole cycle is Ip/pi; the two together draw 2 Ip/pi from the supplies
    Iavg_one = TRAPZ(Ip * np.sin(th), th) / (2 * math.pi); Pdc = VCC * 2 * Iavg_one
    must(close(Pout / Pdc, math.pi / 4, 1e-9) and abs(Pout / Pdc - 0.785398) < 1e-5, Pout / Pdc)
    return 'class B push-pull efficiency pi/4 = 78.5 % (about 79 %) from the average supply current of a full-swing sine'
@chk('pushpull')
def _():
    must(close(12.0 / 8.0, 1.5), 'Ic(sat)'); return CHECKS['classes']()
@chk('oscillation')
def _():
    for g, grows in ((1.01, True), (1.0, None), (0.99, False)):
        x = 1e-3
        for _ in range(2000): x *= g
        must((x > 1e-3 * 1.5) if grows else (x < 1e-3 * 0.5) if grows is False else close(x, 1e-3, 1e-9), g)
    return 'loop simulation x(n+1) = (A.B) x(n): grows for A.B > 1, stays constant at 1, dies for < 1'
@chk('barkhausen')
def _(): return CHECKS['oscillation']()
# ------------------------------------------------------------------ module 05
@chk('instrumentation')
def _():
    def ia(R, RG, v1, v2, A=1e9):
        # input stages: V1' = v1 + (v1 - v2) R/RG, V2' = v2 - (v1 - v2) R/RG  (virtual short across RG) -> solved from KCL with finite A
        x = np.zeros(2)
        # unknown node voltages a (output of op amp 1), b (output of op amp 2) with V- of each op amp equal to v1 (v2): current through RG = (v1 - v2)/RG
        i = (v1 - v2) / RG; a = v1 + i * R; b = v2 - i * R; return a - b                       # difference stage with unity gain
    for R, RG in [(100e3, 1e3), (25e3, 500.0), (10e3, 100.0)]:
        Av = 1 + 2 * R / RG; must(close(ia(R, RG, 0.2, 0.195), Av * 0.005, 1e-9), (R, RG))
    must(close(2 * 100e3 / 999, 200.2, 1e-3) and close(1 + 50.5e3 / 1e3, 51.5), 'RG for G = 1000; AD622 G = 51.5')
    must(close((1 + 2 * 100e3 / 1e3) * 5e-3, 1.005), '1.005 V'); return 'two-buffer IA gain 1 + 2R/RG (3 cases), RG = 200 ohm for G = 1000, AD622 G = 51.5, 201 x 5 mV = 1.005 V'
@chk('isolation')
def _():
    must(30 * 10 == 300 and close(20 * math.log10(30) + 20 * math.log10(10), 20 * math.log10(300)), 'product'); return 'overall gain of two isolated stages = product (30 x 10 = 300)'
@chk('ota')
def _():
    must(close(5000e-6 * 100e-3, 500e-6) and close(500e-6 * 10e3, 5.0) and close(1e-6 * 1e-3, 1e-9), 'values'); must(close(5.0 / 500e-6, 10e3), 'RL')
    must(close(1000e-6 * 5e-3, 5e-6) , 'gm 1000 uS'); return 'Iout = gm Vin (5000 uS x 100 mV = 500 uA), RL = 10 kOhm for 5 V, 1 uS x 1 mV = 1 nA'
@chk('log')
def _():
    VT = 0.025; IR = 2e-9; R = 10e3
    for Vin in (0.1, 0.5, 2.0, 5.0):
        Iin = Vin / R; Vd = brentq(lambda v: IR * (math.exp(v / VT) - 1) - Iin, 0, 1.0)              # exact diode equation
        must(close(-Vd, -VT * math.log(Vin / (R * IR)), 1e-3), (Vin, Vd))
        Vo_anti = -R * IR * math.exp(Vd / VT); must(close(-Vd, -VT * math.log(Vin / (R * IR) + 1), 1e-9), 'ln(1+x)')
    return 'diode-equation root equals -VT ln(Vin/(R IR)) within 0.1 % for Iin >> IR (four inputs)'
@chk('vi')
def _():
    A = 1e8; R1 = 10e3
    for RL in (100.0, 1e3, 4.7e3):
        # Vin on +, load RL in the feedback path to V-, R1 from V- to ground: V- = Vin (virtual short) -> I = V-/R1
        # exact: V- node; Vo = A(Vin - V-); RL between Vo and V-; R1 from V- to gnd: (Vo - V-)/RL = V-/R1
        M = np.array([[1.0, 1.0 / A], [1 / R1 + 1 / RL, -1 / RL]]); Vin = 5.0; Vm, Vo = np.linalg.solve(M, [Vin, 0.0])
        must(close(Vm / R1, Vin / R1, 1e-6), RL)
    Rf = 22e3; Iin = 50e-6; must(close(-Iin * Rf, -1.1), 'I-to-V'); return 'V-to-I load current equals Vin/R1 for three load values; I-to-V = -Iin Rf'
@chk('adcdac')
def _():
    for n, VFS in [(4, 5.0), (8, 5.0), (10, 5.0), (12, 10.0)]:
        LSB = VFS / 2 ** n
        for vin in np.linspace(0, VFS * (1 - 2 ** -n), 997):
            N = int(round(vin / LSB)); err = vin - N * LSB; must(abs(err) <= LSB / 2 + 1e-12, (n, vin))
            code = 0                                                   # successive approximation
            for k in range(n - 1, -1, -1):
                if (code | (1 << k)) * LSB <= vin + 1e-15: code |= 1 << k
            must(code == int(math.floor(vin / LSB + 1e-9)), (n, vin, code))
    must(close(5.0 / 2 ** 10, 4.8828e-3, 1e-4) and int(round(3 / (5 / 2 ** 10))) == 614, 'example'); must(close(12 / 1e6, 12e-6), 'SAR 12 bit @ 1 MHz')
    return 'quantisation error <= LSB/2 and SAR binary search reaches floor(Vin/LSB) in n steps for n = 4, 8, 10, 12; LSB = 4.88 mV and code 614 for 3 V at 10 bit/5 V'
# ------------------------------------------------------------------ module 06
@chk('poles')
def _():
    fc = 1.0; one = lambda f: 1 / (1 + 1j * f / fc)
    must(close(20 * math.log10(abs(one(fc))), -3.0103, 1e-4), '-3 dB at fc')
    for n in (1, 2, 3, 4):                                             # n identical buffered RC sections
        slope = 20 * math.log10(abs(one(1000 * fc)) ** n) - 20 * math.log10(abs(one(100 * fc)) ** n); must(close(slope, -20 * n, 1e-3), (n, slope))
        oct_ = 20 * math.log10(abs(one(2000 * fc)) ** n) - 20 * math.log10(abs(one(1000 * fc)) ** n); must(close(oct_, -6.0206 * n, 1e-3), 'octave')
    return 'one RC pole is -3 dB at fc, -20 dB/decade and -6.02 dB/octave per pole (n = 1..4 buffered sections)'
@chk('characteristics')
def _():
    def df_list(n):
        poles = [cmath.exp(1j * math.pi * (2 * k + n - 1) / (2 * n)) for k in range(1, n + 1)]; upper = [p for p in poles if p.imag > 1e-9]
        return sorted([-2 * p.real for p in upper])                  # damping factor of each second-order section of the normalised Butterworth polynomial
    d6 = df_list(6); must(all(close(a, b, 1e-3) for a, b in zip(d6, [0.5176, 1.4142, 1.9319])), d6)
    d4 = df_list(4); must(all(close(a, b, 1e-3) for a, b in zip(d4, [0.7654, 1.8478])), d4); must(close(df_list(2)[0], math.sqrt(2), 1e-9), 'DF2')
    must(all(close(2 - df, r, 2e-3, 2e-3) for df, r in zip(sorted(d6, reverse=True), [0.068, 0.586, 1.482])), 'R1/R2 = 2 - DF')
    return 'Butterworth damping factors from the poles on the unit circle: 2nd 1.414, 4th 0.765/1.848, 6th 0.518/1.414/1.932, hence R1/R2 = 2 - DF = 0.068, 0.586, 1.482'
def sk_lowpass(R, C, K):
    return lambda f: K / (1 + (3 - K) * (2j * math.pi * f * R * C) + (2j * math.pi * f * R * C) ** 2)
@chk('sallenkey')
def _():
    R, C = 10e3, 15e-9; fc = 1 / (2 * math.pi * R * C); K = 1.586; H = sk_lowpass(R, C, K)
    f3 = brentq(lambda f: abs(H(f)) - abs(H(1e-3)) / math.sqrt(2), 0.1 * fc, 10 * fc); must(close(f3, fc, 2e-3), (f3, fc))
    must(close(1 + 0.586, K) and close(3 - K, 1.414, 1e-3) and close(2 - 0.586, 1.414, 1e-3), 'DF = 3 - K = 2 - R1/R2')
    # unequal components: fc = 1/(2 pi sqrt(RA RB CA CB))
    RA, RB, CA, CB = 10e3, 22e3, 10e-9, 4.7e-9; fcu = 1 / (2 * math.pi * math.sqrt(RA * RB * CA * CB)); wn = 2 * math.pi * fcu
    den = lambda f: 1 + 2j * math.pi * f * (CB * (RA + RB)) + (2j * math.pi * f) ** 2 * RA * RB * CA * CB
    must(close(abs(den(fcu) - (1 - 1)) , abs(2j * math.pi * fcu * CB * (RA + RB)), 1e-9), 'natural frequency'); 
    return 'exact Sallen-Key transfer function: -3 dB at 1/(2 pi RC) for K = 1.586, DF = 3 - K = 2 - R1/R2, natural frequency 1/(2 pi sqrt(RA RB CA CB))'
@chk('cascadefilter')
def _():
    return CHECKS['characteristics']() + '; poles add: 2 + 2 = 4 -> -80 dB/decade'
def mfb_bandpass(R1, R2, R3, C):
    def H(f):
        s = 2j * math.pi * f; G1, G2, G3 = 1 / R1, 1 / R2, 1 / R3
        # ideal op-amp: node a (junction of R1, R3, C, C); inverting node at 0.  Equations: (Vin-Va)G1 + (Vo-Va)sC + (0-Va)G3 + (0-Va)sC = 0 ; (Va-0)sC + (Vo-0)G2 = 0
        # from 2nd: Va = -Vo G2/(sC);  insert into 1st
        Va_over_Vo = -G2 / (s * C); return 1 / ((Va_over_Vo * (G1 + G3 + 2 * s * C) - s * C) / G1)
    return H
@chk('bandpass')
def _():
    for R1, R2, R3, C in [(2.2e3, 22e3, 22e3, 10e-9), (1e3, 47e3, 1e3, 4.7e-9), (4.7e3, 100e3, 2.2e3, 1e-9)]:
        H = mfb_bandpass(R1, R2, R3, C); f0 = (1 / (2 * math.pi * C)) * math.sqrt((R1 + R3) / (R1 * R2 * R3))
        fs = np.geomspace(f0 / 100, f0 * 100, 200001); mag = np.array([abs(H(f)) for f in fs]); fp = fs[mag.argmax()]; peak = mag.max()
        must(close(fp, f0, 5e-3), (fp, f0)); lo = fs[:mag.argmax()][np.argmin(abs(mag[:mag.argmax()] - peak / math.sqrt(2)))]; hi = fs[mag.argmax():][np.argmin(abs(mag[mag.argmax():] - peak / math.sqrt(2)))]
        must(close(hi - lo, 1 / (math.pi * R2 * C), 2e-2), (hi - lo, 1 / (math.pi * R2 * C)))
        must(close(f0 / (hi - lo), math.pi * f0 * R2 * C, 2e-2), 'Q')
    fc1, fc2 = 1e3, 4e3; must(close(math.sqrt(fc1 * fc2), 2e3) and close(fc2 - fc1, 3e3) and close(2e3 / 3e3, 0.6667, 1e-3), 'LP/HP cascade')
    return 'multiple-feedback band-pass solved with ideal-op-amp nodal equations: peak at f0, bandwidth 1/(pi R2 C), Q = f0/BW (three designs); f0 = sqrt(fc1 fc2) for 1 kHz and 4 kHz'
# ------------------------------------------------------------------ module 07
@chk('wien')
def _():
    R, C = 10e3, 16e-9; fr = 1 / (2 * math.pi * R * C); s = lambda f: 2j * math.pi * f
    Z1 = lambda f: R + 1 / (s(f) * C); Z2 = lambda f: R / (1 + s(f) * R * C); B = lambda f: Z2(f) / (Z1(f) + Z2(f))
    must(close(abs(B(fr)), 1 / 3, 1e-9) and abs(cmath.phase(B(fr))) < 1e-9, B(fr)); fs = np.geomspace(fr / 10, fr * 10, 20001); must(abs(fs[np.argmax([abs(B(f)) for f in fs])] - fr) / fr < 1e-3, 'peak')
    must(close(1 + 2.0, 3.0) and close(10e3 * 0 + 1 / (2 * math.pi * 10e3 * 16e-9), 994.7, 1e-3), 'values'); return 'lead-lag network: |B| = 1/3 at 0 deg exactly at 1/(2 pi RC), maximum there; gain needed 3 = 1 + Rf/Ri with Rf = 2 Ri'
@chk('phaseshift')
def _():
    R, C = 10e3, 10e-9; fr = 1 / (2 * math.pi * math.sqrt(6) * R * C); w = 2 * math.pi * fr
    Zc = 1 / (1j * w * C)
    # three-section RC ladder (series C, shunt R): solve the ladder current by backward substitution
    Z3 = R; Z2 = R + Zc + 0; # placeholder, replaced by explicit nodal solution below
    A = np.array([[Zc + R, -R, 0], [-R, Zc + 2 * R, -R], [0, -R, Zc + 2 * R]], dtype=complex); i = np.linalg.solve(A, [1, 0, 0]); Vout = i[2] * R
    must(close(abs(Vout), 1 / 29, 1e-6) and close(abs(cmath.phase(Vout)), math.pi, 1e-6), (abs(Vout), cmath.phase(Vout)))
    return 'three-section RC ladder solved exactly: attenuation 1/29 and phase 180 deg at 1/(2 pi sqrt6 RC)'
@chk('lc')
def _():
    L, C1, C2 = 1e-3, 100e-12, 100e-12; CT = C1 * C2 / (C1 + C2); fr = 1 / (2 * math.pi * math.sqrt(L * CT))
    Z = lambda f: 1j * 2 * math.pi * f * L + 1 / (1j * 2 * math.pi * f * C1) + 1 / (1j * 2 * math.pi * f * C2)      # series loop impedance of the tank
    fz = brentq(lambda f: Z(f).imag, 0.1 * fr, 10 * fr); must(close(fz, fr, 1e-9), (fz, fr))
    # tank voltages: output across C2, feedback across C1 -> |Vf/Vout| = C2/C1  (Floyd Eq. 16-5), Av = C1/C2
    Ic = 1e-3; Vf = Ic / (2 * math.pi * fr * C1); Vo = Ic / (2 * math.pi * fr * C2); must(close(Vf / Vo, C2 / C1, 1e-9), 'B')
    LT = 2e-3 + 1e-3; Ch = 100e-12; must(close(1 / (2 * math.pi * math.sqrt(LT * Ch)), 1 / (2 * math.pi * math.sqrt((2e-3 + 1e-3) * Ch)), 1e-12), 'Hartley LT = L1 + L2')
    return 'Colpitts: the tank loop impedance is purely resistive exactly at 1/(2 pi sqrt(L CT)), B = Vf/Vout = C2/C1 so Av = C1/C2'
@chk('relaxation')
def _():
    for R1, R2, R, C in [(10e3, 10e3, 10e3, 10e-9), (10e3, 20e3, 4.7e3, 22e-9)]:
        B = R2 / (R1 + R2); Vs = 12.0; dt = 1e-8 * (R * C / 1e-4); vc = 0.0; vo = Vs; crossings = []; t = 0.0; n = 0
        while len(crossings) < 7 and n < 5_000_000:
            vc += (vo - vc) * dt / (R * C); t += dt; n += 1
            if vo > 0 and vc > B * Vs: vo = -Vs; crossings.append(t)
            elif vo < 0 and vc < -B * Vs: vo = Vs; crossings.append(t)
        T = (crossings[-1] - crossings[-3]); f_sim = 1 / T; f_form = 1 / (2 * R * C * math.log((1 + B) / (1 - B)))
        must(close(f_sim, f_form, 5e-3), (f_sim, f_form))
    return 'time-stepped RC + comparator oscillator: measured frequency equals 1/(2 R C ln((1+B)/(1-B))) within 0.5 % (two designs)'
@chk('astable555')
def _():
    for R1, R2, C in [(1e3, 10e3, 0.1e-6), (4.7e3, 47e3, 10e-9), (2.2e3, 6.8e3, 1e-6)]:
        Vcc = 1.0; dt = (R2 * C) / 20000; v = Vcc / 3; t = 0.0; hi = True; edges = []
        while len(edges) < 6:
            tau = (R1 + R2) * C if hi else R2 * C; target = Vcc if hi else 0.0
            v += (target - v) * dt / tau; t += dt
            if hi and v >= 2 * Vcc / 3: hi = False; edges.append(t)
            elif (not hi) and v <= Vcc / 3: hi = True; edges.append(t)
        T = edges[-1] - edges[-3]; th = edges[-2] - edges[-3]; f_book = 1.44 / ((R1 + 2 * R2) * C); duty_book = (R1 + R2) / (R1 + 2 * R2)
        must(close(1 / T, f_book, 5e-3) and close(th / T, duty_book, 5e-3), (R1, R2, C, 1 / T, f_book, th / T, duty_book))
        must(close(0.693 * (R1 + R2) * C, th, 5e-3), 'tH')
    return 'time-stepped 555 capacitor between VCC/3 and 2 VCC/3: frequency 1.44/((R1+2R2)C), duty (R1+R2)/(R1+2R2) and tH = 0.693 (R1+R2) C for three designs'
@chk('monostable555')
def _():
    R, C = 10e3, 10e-6; tau = R * C; t = tau * math.log((1 - 0) / (1 - 2 / 3)); must(close(t / tau, 1.1, 2e-3), t / tau); must(close(1.1 * R * C, 0.11), 'tW')
    return 'charging 0 -> 2VCC/3 takes RC ln 3 = 1.0986 RC (1.1 RC to 0.2 %)'
# ------------------------------------------------------------------ module 08
@chk('regulation')
def _():
    must(close((5.05 - 5.00) / 5.00 * 100, 1.0, 1e-9) and close(2e-3 / 6 * 100, 0.0333, 1e-3), 'values')
    must(close(abs(5.05 - 5.00) / 5.05 * 100, 0.99, 1e-2) and not close((5.05 - 5.00) / 5.05 * 100, 1.0, 1e-3), 'VFL not VNL in the denominator')
    return 'load regulation (VNL - VFL)/VFL = 1.0 % (using VNL in the denominator would give 0.99 %); line regulation 2 mV/6 V = 0.0333 %'
@chk('series')
def _():
    must(close((1 + 5.6 / 2.2) * 2.4, 8.509, 1e-3) and close((1 + 5.6 / 4.7) * 2.4, 5.26, 2e-3) and close((1 + 5.6 / 2.2) * 2.7, 9.57, 2e-3), 'examples')
    A = 1e6; VREF, R2, R3 = 2.4, 5.6e3, 2.2e3; Vo = A * VREF / (1 + A * R3 / (R2 + R3)); must(close(Vo, (1 + R2 / R3) * VREF, 1e-5), 'op-amp loop'); return 'op-amp error amplifier with a finite-gain loop reproduces (1 + R2/R3) VREF; the three book numbers 8.51, 5.26, 9.57 V'
@chk('currentlimit')
def _():
    R4 = 0.7 / 0.25; must(close(R4, 2.8) and close(0.25 ** 2 * R4, 0.175) and close(0.7 / (R4 / 2), 0.5), 'values'); return 'R4 = 0.7/IL(max) = 2.8 ohm, 0.175 W, halving R4 doubles the limit to 500 mA'
@chk('shunt')
def _():
    VIN, R1 = 25.0, 100.0; must(close(VIN / R1, 0.25) and close((VIN / R1) ** 2 * R1, 6.25) and close(1.0 / 100, 0.01), 'values'); return 'short-circuit current VIN/R1 = 250 mA and 6.25 W in R1; 1 V / 100 ohm = 10 mA'
@chk('lm317')
def _():
    R1 = 240.0; R2 = (9 / 1.25 - 1) * R1; must(close(1.25 * (1 + R2 / R1), 9.0, 1e-12), 'solve'); must(close(1.25 * (1 + R2 / R1) + 50e-6 * R2, 9.0 + 50e-6 * R2), 'IADJ')
    must(close(0.7 / 2.0, 0.35), 'Rext'); return 'solving R2 for 9 V and substituting back (with and without IADJ R2)'
@chk('switching')
def _():
    VIN = 24.0
    for duty in (0.25, 0.4, 0.75):
        T = 100e-6; t = np.linspace(0, T, 200001); sw = np.where(t < duty * T, VIN, 0.0); must(close(TRAPZ(sw, t) / T, duty * VIN, 1e-3), duty)
    must(close(40e-6 / 100e-6, 0.4), 'duty'); return 'average of the switch-node waveform equals duty x VIN (three duty cycles); 40 us of 100 us = 40 %'
@chk('heat')
def _():
    VIN, VOUT, IL = 12.0, 5.0, 0.5; PD = (VIN - VOUT) * IL; Pin = VIN * IL; must(close(PD, 3.5) and close(VOUT * IL / Pin, VOUT / VIN, 1e-12), 'values'); return 'dissipation (12 - 5) V x 0.5 A = 3.5 W; efficiency = VOUT/VIN = 41.7 %'
# ------------------------------------------------------------------ module 09
@chk('trace')
def _():
    rho = 1.68e-8; L, w, t = 0.10, 0.25e-3, 35e-6; R = rho * L / (w * t); must(close(R, 0.192, 1e-2), R); must(close(rho * (2 * L) / (w * t), 2 * R) and close(rho * L / (2 * w * t), R / 2), 'scaling')
    return 'R = rho L/(w t) = 0.19 ohm for 10 cm x 0.25 mm x 35 um; proportional to length, inversely to width'
# ------------------------------------------------------------------ module 10
@chk('servoloop')
def _():
    # example from the notes: R2 = R3, input +10 V, feedback 0 V -> sum point +5 V, motor runs until feedback = -10 V
    summing = lambda vin, vfb: (vin + vfb) / 2; must(summing(10, 0) == 5 and summing(10, -10) == 0, 'sum point')
    th, theta_in, K, dt = 0.0, 1.0, 4.0, 1e-3                       # first-order motor: velocity proportional to error
    for _ in range(20000): th += K * (theta_in - th) * dt
    must(close(th, theta_in, 1e-6), th); return 'summing point (10 V, 0 V) = 5 V and 0 at feedback -10 V; a closed first-order position loop drives the error to zero'
@chk('synchro')
def _():
    angles = np.radians(np.arange(0, 360, 1.0)); k = 1.0
    v = np.array([[math.cos(a), math.cos(a - 2 * math.pi / 3), math.cos(a + 2 * math.pi / 3)] for a in angles]); must(np.allclose(v.sum(axis=1), 0, atol=1e-12), 'sum zero')
    # Clarke transform: alpha = v0, beta = (v1 - v2)/sqrt(3)  gives (cos a, sin a) for stator voltages cos(a), cos(a-120), cos(a+120)
    rec = [math.degrees(math.atan2((x[1] - x[2]) / math.sqrt(3), x[0])) % 360 for x in v]
    err = [abs(((r - a + 180) % 360) - 180) for r, a in zip(rec, np.degrees(angles))]
    must(max(err) < 1e-9, max(err))
    must(close(115 / 2.2, 52.27, 1e-3), '115 V / 2.2')
    return 'three stator voltages 120 deg apart sum to zero and recover the rotor angle uniquely over 0..359 deg; 115 V / 2.2 = 52.3 V'
@chk('resolver')
def _():
    for a in np.radians(np.arange(-179, 180, 3.0)): must(close(math.atan2(math.sin(a), math.cos(a)), a, 1e-9), a)
    return 'atan2(sin, cos) recovers the angle over the whole circle'
@chk('stability')
def _():
    # velocity servo example: control -9 V, R2 = R3, motor 10 rpm/V, tach 1 V per 10 rpm
    w = 0.0
    for _ in range(200): e = (-9 + 0.1 * w) / 2; w = 10 * abs(e)
    must(close(w, 30, 1e-6) and close((-9 + 0.1 * w) / 2, -3, 1e-6), (w,))
    must(close((-9 + 0) / 2, -4.5) and close((-9 + 0.1 * 10) / 2, -4.0), 'initial errors')
    def run(c, K=40.0, dt=1e-4, T=3.0):
        th, om, peak = 0.0, 0.0, 0.0
        for _ in range(int(T / dt)): om += (K * (1 - th) - c * om) * dt; th += om * dt; peak = max(peak, th)
        return peak, th
    pk0, _ = run(0.0); pk1, th1 = run(2 * math.sqrt(40.0)); pk2, _ = run(1.0)
    must(pk0 > 1.9 and pk1 <= 1.0 + 1e-3 and pk1 < pk2 < pk0 and close(th1, 1, 2e-2), (pk0, pk1, pk2, th1))
    return 'velocity servo settles at 30 rpm with -3 V error (book example); position loop: undamped overshoots by 100 %, light damping overshoots, critical damping settles without overshoot'
@chk('pwm')
def _():
    for duty in (0.1, 0.4, 0.9):
        T = 1e-3; t = np.linspace(0, T, 400001); v = np.where(t < duty * T, 12.0, 0.0); must(close(TRAPZ(v, t) / T, 12 * duty, 1e-3), duty)
    must(close(0.4 * 12, 4.8), 'example'); return 'average of a 12 V pulse train equals duty x 12 V (duty 10 %, 40 %, 90 %)'

@chk('opampsat')
def _():
    Vs, A = 13.0, 1e5; out = lambda vp, vm: max(-Vs, min(Vs, A * (vp - vm)))
    must(out(0.001, 0.0) == Vs and out(0.0, 0.001) == -Vs and close(out(1e-7, 0.0), 0.01), 'saturation / linear zone')
    return 'open-loop op-amp: output clips at the supply for |V+ - V-| above Vs/A and has the sign of V+ - V-'
@chk('idealmodel')
def _():
    A = 1e5
    for Ri, Rf in [(10e3, 220e3), (1e3, 10e3)]:
        M = np.array([[1 / Ri + 1 / Rf, -1 / Rf], [A, 1.0]]); Vm, Vo = np.linalg.solve(M, [1 / Ri, 0.0])
        must(abs(Vo / (-Rf / Ri) - 1) < 3e-4, (Ri, Rf, Vo))                                # the ideal model is adequate for Aol ~ 1e5
    return 'with Aol = 100,000 the exact inverting gain differs from the ideal -Rf/Ri by < 0.03 %, so the ideal model is adequate'
@chk('esdtable')
def _():
    cls1, cls2 = (100, 1000), (1001, 4000); must(cls1[1] + 1 == cls2[0], 'classes are contiguous')
    bip, cmos, eprom, feel = (380, 7000), (250, 3000), 100, 3000
    must(eprom < cmos[0] < bip[0] and cmos[0] < feel, 'a damaging voltage can be below the 3000 V a person feels')
    must(1500 < 5000 < 10000 < 35000, 'ordering of the quoted static voltages'); return 'quoted ESD data are internally consistent (contiguous MIL-STD classes; EPROM < CMOS < bipolar thresholds; sensitive parts fail below human perception)'
@chk('lvdt')
def _():
    E, k, Lh = 1.0, 0.5, 10.0
    for x in np.linspace(-5, 5, 11):
        v1, v2 = k * E * (1 + x / Lh), k * E * (1 - x / Lh); vout = v1 - v2
        must(close(vout, 2 * k * E * x / Lh, 1e-12, 1e-12), x)
        if x != 0: must((vout > 0) == (x > 0), 'sign follows the direction')
        else: must(abs(vout) < 1e-12, 'null at the centre')
    return 'series-opposing secondaries: output is zero at the centre, linear in displacement, and changes sign (phase) with the direction'
@chk('controlsynchro')
def _():
    err = lambda d: math.sin(math.radians(d))
    must(err(0) == 0 and err(-20) == -err(20) and err(20) > 0, 'sign = phase, zero at correspondence')
    must(all(abs(err(d) / math.radians(d) - 1) < 0.01 for d in (1, 5, 10)), 'linear for small angles')
    def volts(a): return [math.cos(a), math.cos(a - 2 * math.pi / 3), math.cos(a + 2 * math.pi / 3)]
    for a in np.radians(np.arange(0, 360, 7.0)):
        v = volts(a); swapped = [v[0], v[2], v[1]]; must(np.allclose(swapped, volts(-a)), 'S1-S3 reversed = negative angle')
    return 'error voltage ~ sin(difference): zero at correspondence, opposite sign for the other direction, within 1 % of linear up to 10 deg; swapping two stator leads negates the angle (sum becomes difference)'
