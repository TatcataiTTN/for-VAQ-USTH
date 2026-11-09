"""Independent re-derivation of the level-3 'hard' questions (data/qsrc/mNN_zhard.json, written by build/gen/gen_hard.py).

The generator already re-derives each result by a second route inside the question.  This script is a THIRD, separate pass written with different methods
(nodal linear solves, time-domain simulation, root finding on the complex response, scipy.signal Butterworth poles, ideal-network balance equations ...).
It parses the numbers out of the stored correct option and compares them with the independent value (relative tolerance 0.6 %, which covers the 3-4 significant
figures shown).  It also checks the structure of every hard item and that the assembled bank (data/qbank) carries the same question with the same correct option.
Run: python3 build/verify/verify_hard.py   (exit 1 on any mismatch)"""
import os, sys, json, math, re, cmath, glob
from fractions import Fraction
import numpy as np
from scipy.optimize import brentq
from scipy import signal
from scipy.integrate import solve_ivp, quad
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
ITEMS = {}
for i in range(1, 11):
    p = os.path.join(ROOT, 'data', 'qsrc', f'm{i:02d}_zhard.json')
    ITEMS[f'm{i:02d}'] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
bad = []; done = 0
NUM = re.compile(r'(?<![A-Za-z])[-−]?\d+(?:\.\d+)?(?:e[-+]?\d+)?')
def nums(s): return [float(x.replace('−', '-')) for x in NUM.findall(s)]
def get(mod, sub):
    r = [it for it in ITEMS[mod] if sub in it['q']['en']]; assert len(r) == 1, (mod, sub, len(r)); return r[0]
def ctext(it): return it['opts'][it.get('correct', 0)]['en']
def chk(mod, sub, *want, tol=0.006):
    global done
    it = get(mod, sub); got = nums(ctext(it)); done += 1
    if len(got) != len(want) or any(abs(a - b) > tol * abs(b) + 1e-9 for a, b in zip(got, want)): bad.append((mod, sub[:50], ctext(it), want))
def eq(mod, sub, text):
    global done
    it = get(mod, sub); done += 1
    if ctext(it) != text: bad.append((mod, sub[:50], ctext(it), text))
def db(x): return 20 * math.log10(abs(x))
# ---------------------------------------------------------------- m01
chk('m01', 'decimal value of 101101', int('101101', 2) + int('11011', 2))
eq('m01', 'written in BCD', ' '.join(f'{int(d):04b}' for d in '59'))
t = 0b1011 + 0b0110; eq('m01', 'ripple-carry adder', f'S = {t & 15:04b}, carry out = {t >> 4}')
q = 0; seq = []
for j, k in ((1, 0), (1, 1), (0, 0), (1, 1)): q = (j & (1 - q)) | ((1 - k) & q); seq.append(q)       # characteristic equation Q+ = J.Q' + K'.Q
eq('m01', 'JK flip-flop starts', ', '.join(map(str, seq)))
bits = [0, 0, 0]
for _ in range(13):                                    # ripple chain: bit k toggles when bit k-1 falls 1 -> 0
    k = 0
    while k < 3:
        bits[k] ^= 1
        if bits[k] == 1: break
        k += 1
eq('m01', '3-bit binary counter', ''.join(map(str, bits[::-1])))
tt = tuple(int(not ((a and not b) or (not a and b))) for a in (0, 1) for b in (0, 1)); gates = {(1, 0, 0, 1): 'XNOR', (0, 1, 1, 0): 'XOR', (1, 1, 1, 0): 'NAND', (1, 0, 0, 0): 'NOR'}
eq('m01', 'is equivalent to which gate', gates[tt])
VDD, VTN, VTP, Kn, Kp = 3.3, 0.6, -0.8, 225e-6, 100e-6; v = np.linspace(VTN, VDD + VTP, 2000001); d = 0.5 * Kn * (v - VTN) ** 2 - 0.5 * Kp * (VDD - v + VTP) ** 2
chk('m01', 'switching threshold VSP', float(v[np.argmin(np.abs(d))]))
chk('m01', 'dynamic power P', 0.1 * 10000 * 2e-12 * 1.8 ** 2 * 200e6)
chk('m01', 'largest noise tolerated', 1.4 - 0.2, 4.8 - 3.2)
k = next(k for k in range(1, 20) if 4 * (k - 1) >= 16 and k - 1 <= 4); chk('m01', 'minimum number of 2→4 decoders', k)
# ---------------------------------------------------------------- m02
def solve(A, b): return np.linalg.solve(np.array(A, float), np.array(b, float))
Ri, Rf, A = 1e3, 49e3, 2e4                                              # noninverting, B = Ri/(Ri+Rf) = 1/50: unknowns vout, vfb
vout, vfb = solve([[1, A], [-Ri, Ri + Rf]], [A * 1.0, 0]); G = vout
chk('m02', 'gain of 50 (B = 1/50)', G, (G - 50) / 50 * 100)
vn, vo = solve([[1 / 10e3 + 1 / 100e3, -1 / 100e3], [5000, 1]], [1 / 10e3, 0]); chk('m02', 'exact closed-loop gain is', vo)
Vp = 0.2 * 20
def maxslope(f):
    t = np.linspace(0, 1 / f, 200001); y = Vp * np.sin(2 * math.pi * f * t); return float(np.max(np.abs(np.gradient(y, t))))
fs_ = brentq(lambda f: maxslope(f) - 0.8e6, 1, 1e7); chk('m02', 'highest undistorted frequency', min(fs_, 2e6 / 20) / 1e3)
Ri, Rf, Vos, Ib = 1e3, 100e3, 2e-3, 80e-9
M_ = np.array([[1.0, 0.0], [-(1 / Ri + 1 / Rf), 1 / Rf]]); b_ = np.array([Vos, Ib]); vn_, vo_ = np.linalg.solve(M_, b_); chk('m02', 'worst-case (same sign) dc output error', vo_ * 1e3)
Ad = 100; Acm = Ad / 10 ** (90 / 20); chk('m02', 'CMRR of 90 dB', (Ad * 2e-3 + Acm * 1.5) * 1e3)
Rin_, Rf_, Aol, Rout = 1e3, 49e3, 120000, 75; B = Rin_ / (Rin_ + Rf_)
def vo_for(i): return solve([[1 + Aol * B]], [-Rout * i])[0]
chk('m02', 'output impedance with feedback', abs(vo_for(1e-3) - vo_for(0)) / 1e-3 * 1e3)
bw1 = 1e6 / 20
fx = brentq(lambda f: abs(1 / (1 + 1j * f / bw1) ** 2) - 1 / math.sqrt(2), 1, 1e7); chk('m02', 'bandwidth of the pair', fx / 1e3)
Ao, fc, ACL, f = 200000, 10.0, 40, 100e3; Af = Ao / (1 + 1j * f / fc); chk('m02', 'The gain at 100 kHz', db(Af / (1 + Af / ACL)))
Ib_p, Ib_m = 105e-9, 95e-9; Ri, Rf = 10e3, 220e3; Rc = Ri * Rf / (Ri + Rf); vp = -Ib_p * Rc; vo = vp * (1 + Rf / Ri) + Rf * Ib_m; chk('m02', 'compensating resistor at the noninverting input', abs(vo) * 1e3)
ph = sum(cmath.phase(1 / (1 + 1j * 20 / fc_)) for fc_ in (1, 20, 100)); chk('m02', 'total phase lag at f = 20 kHz', math.degrees(ph))
# ---------------------------------------------------------------- m03
Vsat = 5.1 + 0.7; R1, R2 = 33e3, 6.8e3
def schmitt_up():
    vin = -3.0; out = +Vsat
    while True:
        vplus = out * R2 / (R1 + R2)
        if out > 0 and vin > vplus: return vin
        vin += 1e-5
def schmitt_dn():
    vin = 3.0; out = -Vsat
    while True:
        vplus = out * R2 / (R1 + R2)
        if out < 0 and vin < vplus: return vin
        vin -= 1e-5
utp, ltp = schmitt_up(), schmitt_dn(); chk('m03', 'comparator with hysteresis', utp, utp - ltp)
R, C = 10e3, 47e-9; dt = 1e-7; t = np.arange(0, 6e-3, dt); vin = 2.0 * np.sign(np.sin(2 * math.pi * 500 * t + 1e-9)); vo = -np.cumsum(vin) * dt / (R * C); last = vo[t > 3e-3]; chk('m03', 'triangular output is about', float(last.max() - last.min()))
R, C = 100e3, 0.1e-6; v = 0.0; tt = 0.0
while v > -11: v -= 1.5 * 1e-6 / (R * C); tt += 1e-6
chk('m03', 'until the output reaches', tt * 1e3)
Rf, C = 10e3, 10e-9; t = np.linspace(0, 4e-3, 4000001); tri = 4 * np.abs(((t * 1000 + 0.25) % 1) - 0.5) - 1; vd = -Rf * C * np.gradient(tri, t); chk('m03', 'peak amplitude of the square-wave output', float(np.max(np.abs(vd))))
Vk = np.array([2.0, -1.0, 0.5]); Rk = np.array([10e3, 20e3, 5e3]); chk('m03', 'inverting summer with Rf = 20', float(-20e3 * np.sum(Vk / Rk)))
Rk = np.array([10e3, 20e3, 40e3, 80e3]); bitsx = np.array([1, 0, 1, 1]) * 5.0; chk('m03', '4-bit DAC uses an inverting summer', float(-10e3 * np.sum(bitsx / Rk)))
Vk = np.array([1.2, 2.4, 3.6, 4.8]); Rfx = brentq(lambda rf: -rf * np.sum(Vk / 10e3) + Vk.mean(), 1, 1e6); chk('m03', 'four-input averaging amplifier', Rfx / 1e3, float(-Rfx * np.sum(Vk / 10e3)))
Ri_, Rf_, C = 10e3, 1e6, 0.1e-6; H = lambda f: abs(-(Rf_ / (1 + 1j * 2 * math.pi * f * Rf_ * C)) / Ri_); H0 = H(0); fcc = brentq(lambda f: H(f) - H0 / math.sqrt(2), 1e-3, 1e5); chk('m03', 'practical integrator uses', -H0, db(H0), fcc)
Rin, Rf_, C = 1e3, 10e3, 10e-9; H = lambda f: abs(-Rf_ / (Rin + 1 / (1j * 2 * math.pi * f * C))); Hinf = H(1e12); fcc = brentq(lambda f: H(f) - Hinf / math.sqrt(2), 1, 1e8); chk('m03', 'practical differentiator', -Hinf, db(Hinf), fcc / 1e3)
# ---------------------------------------------------------------- m04
chk('m04', 'unloaded gain of 30', float(Fraction(30) * Fraction(6, 8) * 20), db(float(Fraction(30) * Fraction(6, 8) * 20)))
chk('m04', 'gains of 18 dB, 26 dB and', 10 ** ((18 + 26 - 3) / 20))
VCC, RL = 18.0, 8.0; Pd, _ = quad(lambda th: (VCC - VCC * math.sin(th)) * (VCC / RL) * math.sin(th), 0, math.pi); chk('m04', 'class B push-pull', Pd / (2 * math.pi))
VCC, Rc = 12.0, 100.0; Pout, _ = quad(lambda th: (VCC * math.sin(th)) ** 2 / Rc, 0, 2 * math.pi); Pout /= 2 * math.pi; PD = 0.05 * 0.3 * 0.5; chk('m04', 'class C amplifier', 100 * Pout / (Pout + PD))
fcut = 1 / (2 * math.pi * (4.7e3 + 3.3e3) * 2.2e-6); Hrel = abs((3.3e3 / (3.3e3 + 4.7e3 + 1 / (1j * 2 * math.pi * 5 * 2.2e-6))) / (3.3e3 / (3.3e3 + 4.7e3))); chk('m04', 'RC-coupled', db(Hrel))
acl = lambda a, b: Fraction(a) / (1 + Fraction(a) * Fraction(b)); chk('m04', 'Aol falls by 20 %', float((acl(8000, '0.01') / acl(10000, '0.01') - 1) * 100))
chk('m04', 'minimum number of cascaded stages', next(n for n in range(1, 20) if 15 ** n > 1000))
# ---------------------------------------------------------------- m05
R, RG = 25e3, 500.0; i = (3.100 - 3.085) / RG; Va = 3.100 + R * i; Vb = 3.085 - R * i; chk('m05', 'R = 25 kΩ and RG = 500', Va - Vb)
chk('m05', 'gain of 250 with R = 47', brentq(lambda rg: 1 + 2 * 47e3 / rg - 250, 1, 1e6))
gm = 16e-6 / 1e-6 * 62.5e-6; chk('m05', 'gm = K·IBIAS with K = 16', gm * 50e-3 * 5e3, gm * 5e3)
tm = np.linspace(0, 1, 100001); Ibt = 50e-6 + 20e-6 * np.sin(2 * math.pi * tm); env = 16 * Ibt * 1e6 * 1e-6 * 10e-3 * 10e3; mx, mn = env.max(), env.min(); chk('m05', 'modulated bias current', mx * 1e3, (mx - mn) / (mx + mn) * 100)
chk('m05', 'log amplifier', -0.025 * math.log(2 / (47e3 * 30e-9)) * 1e3, -0.025 * math.log(10) * 1e3)
lsb = 4.096 / 4096; code = round(2.3456 / lsb); chk('m05', '12-bit SAR ADC', lsb * 1e3, code, 12 / 2e6 * 1e6)
chk('m05', 'isolation amplifier', 12 * 8 * 0.015)
Iload = 3.3 / 1.5e3; RLmax = brentq(lambda rl: Iload * (rl + 1.5e3) - 11, 1, 1e6); chk('m05', 'V-to-I current source', Iload * 1e3, RLmax / 1e3)
# ---------------------------------------------------------------- m06
dfs = sorted(2 * math.sin((2 * k - 1) * math.pi / (2 * 4)) for k in (1, 2)); assert abs(dfs[0] - 0.765) < 1e-3 and abs(dfs[1] - 1.848) < 1e-3; chk('m06', 'DF = 0.765', 2 - dfs[0])
b3, a3 = signal.butter(3, 2 * math.pi * 1e3, analog=True); _, h = signal.freqs(b3, a3, [2 * math.pi * 8e3]); chk('m06', '3-pole Butterworth', db(h[0]))
chk('m06', 'Sallen-Key stage with RA = RB', 1 / (2 * math.pi * 2.5e3 * 10e-9) / 1e3)
f1, f2 = 300, 3400; f0 = math.sqrt(f1 * f2); Qb = f0 / (f2 - f1); eq('m06', 'band-pass filter is built from', f'{f0:.0f} Hz; Q = {Qb:.3g}; ' + ('narrow-band' if Qb > 10 else 'wide-band'))
chk('m06', 'multiple-feedback band-pass', 1 / (math.pi * (1000 / 10) * 10e-9) / 1e3)
b4, a4 = signal.butter(4, 1.0, 'high', analog=True); _, h = signal.freqs(b4, a4, [0.1]); chk('m06', '4-pole Butterworth high-pass', db(h[0]))
chk('m06', 'Bessel response has DF = 1.732', 2 - 1.732, 1 / 1.732)
fx = brentq(lambda f: abs(1 / (1 + 1j * f / 1e4)) ** 2 - 1 / math.sqrt(2), 1, 1e6); chk('m06', 'Two identical single-pole RC', fx / 1e3)
# ---------------------------------------------------------------- m07
Rw, Cw = 8.2e3, 0.022e-6
def wien(f):
    s = 1j * 2 * math.pi * f; Zs = Rw + 1 / (s * Cw); Zp = Rw / (1 + s * Rw * Cw); return Zp / (Zp + Zs)
f0w = brentq(lambda f: wien(f).imag, 10, 1e5, xtol=1e-9); Gw = 1 / abs(wien(f0w)); assert abs(Gw - 3) < 1e-9; chk('m07', 'Wien-bridge oscillator', f0w, (Gw - 1) * 10e3 / 1e3)
Rl, Cl = 4.7e3, 0.01e-6
def ladder(f):
    s = 1j * 2 * math.pi * f; Y = 1 / Rl; G = s * Cl
    Mx = np.array([[G + Y + G, -G, 0], [-G, G + Y + G, -G], [0, -G, G + Y]], complex); v = np.linalg.solve(Mx, np.array([G, 0, 0], complex)); return v[2]
fl = brentq(lambda f: ladder(f).imag, 100, 1e4); gl = 1 / abs(ladder(fl)); assert ladder(fl).real < 0; chk('m07', 'three-section RC phase-shift', fl / 1e3, gl * Rl / 1e3, tol=0.007)
L, C1, C2 = 100e-6, 470e-12, 47e-12; fcol = brentq(lambda f: 2 * math.pi * f * L - 1 / (2 * math.pi * f) * (1 / C1 + 1 / C2), 1e3, 1e9); chk('m07', 'Colpitts oscillator', fcol / 1e6, C1 / C2)
fs_c = brentq(lambda f: 2 * math.pi * f * 0.1 - 1 / (2 * math.pi * f * 0.04e-12), 1e3, 1e8); chk('m07', 'crystal has Ls', fs_c / 1e6)
sol = np.linalg.solve([[1, 2], [1, 1]], [1.44 / (2000 * 10e-9), 0.65 * 1.44 / (2000 * 10e-9)]); chk('m07', 'astable 555 for f = 2 kHz', sol[0] / 1e3, sol[1] / 1e3)
chk('m07', 'monostable 555', 0.25 / (1.1 * 4.7e-6) / 1e3)
Vcc, R1, R2, Cx, Vc = 12.0, 10e3, 10e3, 10e-9, 9.0
def cross_time(y0, tau, target, level):
    ev = lambda t, y: y[0] - level; ev.terminal = True
    s_ = solve_ivp(lambda t, y: [(target - y[0]) / tau], [0, 1], [y0], events=ev, rtol=1e-10, atol=1e-12); return s_.t_events[0][0]
tH = cross_time(Vc / 2, (R1 + R2) * Cx, Vcc, Vc); tL = cross_time(Vc, R2 * Cx, 0.0, Vc / 2)
chk('m07', 'control pin (pin 5)', 1 / (tH + tL) / 1e3)
# ---------------------------------------------------------------- m08
Ir = 1.25 / 240; chk('m08', 'Design an LM317', 1.25 + (Ir + 50e-6) * 1500)
chk('m08', 'A 7805 IC takes', 40 + (12 - 5) * 0.6 * (5 + 1 + 10))
chk('m08', 'sense resistor R4', 1.2 ** 2 * (0.7 / 1.2))
R1s = brentq(lambda r: (20 - 12) / r - 0.1 - 0.010, 1, 1e4); chk('m08', 'shunt regulator', R1s, 12 * (20 - 12) / R1s)
Pin = 5 * 2 / 0.88; chk('m08', 'step-down switching regulator', Pin / 24 * 1e3, (24 - 5) * 2)
Dd = brentq(lambda d: 5 * d - (15 - 5) * (1 - d), 0, 1); chk('m08', 'step-up (boost)', Dd)
chk('m08', 'line regulation in %/V', (12.05 - 12.00) / 12.00 * 100 / (18 - 15))
chk('m08', 'series regulator with a 2.4 V reference', (1 + 27 / 10) * 2.4)
chk('m08', 'load regulation', (5.10 - (5.10 - 2 * 0.1)) / (5.10 - 2 * 0.1) * 100)
# ---------------------------------------------------------------- m09
Rt = 1.68e-8 * 0.20 / (0.5e-3 * 70e-6); chk('m09', 'copper trace', 3 * Rt * 1e3, 9 * Rt)
chk('m09', 'vias', 1 / (5 / 1.2e-3) * 1e3)
rng = {'bipolar transistors': (380, 7000), 'CMOS': (250, 3000), 'EPROM': (100, 3000)}; risk = [k for k, (lo, hi) in rng.items() if lo <= 300]
it = get('m09', 'static charge'); got = ctext(it); done += 1
if got != 'CMOS and EPROM, but not bipolar transistors' or risk != ['CMOS', 'EPROM']: bad.append(('m09', 'ESD risk', got, risk))
chk('m09', 'wrist strap', 230 / 1e6 * 1e6)
# ---------------------------------------------------------------- m10
w_, e_ = solve([[1, -20.0], [0.05, 2.0]], [0, 15.0]); chk('m10', 'velocity servo', w_, e_)
chk('m10', 'overcome static friction', 2 / 40 / 0.15)
def stator(a): return np.array([math.cos(math.radians(a + 120)), math.cos(math.radians(a)), math.cos(math.radians(a - 120))])    # S1, S2, S3 with S2 = electrical zero (SERVOMECHANISM §3.7)
def angle_of(vv): return math.degrees(math.atan2((vv[1] * math.cos(math.radians(120)) - vv[0]) / math.sin(math.radians(120)), vv[1]))
th1 = angle_of(stator(135)[::-1]); tot = th1 + 60; chk('m10', 'differential synchro TDX', tot, tot % 360)
chk('m10', 'rotor shaft 60°', 115 / 2.2 * math.cos(math.radians(60)))
chk('m10', 'reduction gear train', 3000 / 60, 60)
chk('m10', 'capacitance probe', 100 * (0.4 * 1.0 + 0.6 * 2.1))
# ---------------------------------------------------------------- structure and bank cross-check
import collections
seen = set(); total = 0
for mod, its in ITEMS.items():
    for it in its:
        total += 1; en = [o['en'] for o in it['opts']]; vi = [o['vi'] for o in it['opts']]
        if len(set(en)) != len(en) or len(set(vi)) != len(vi) or len(en) < 4: bad.append((mod, 'options', it['q']['en'][:40]))
        if it['level'] != 3 or 'hard' not in it['tags'] or it['kind'] != 'mcq': bad.append((mod, 'fields', it['q']['en'][:40]))
        if it['q']['en'] in seen: bad.append((mod, 'duplicate', it['q']['en'][:40]))
        seen.add(it['q']['en'])
        dig = lambda s: re.sub(r'[^0-9]', '', s)
        if any(dig(a) != dig(b) for a, b in zip(en, vi)): bad.append((mod, 'digits EN/VI differ in options', it['q']['en'][:40]))
        if re.search(r'\d\.\d', it['q']['vi'] + it['explain']['vi']): bad.append((mod, 'dot decimal in VI text', it['q']['en'][:40]))
        if any(re.search(r'\d\.\d', o) for o in vi): bad.append((mod, 'dot decimal in VI option', it['q']['en'][:40]))
        right = nums(ctext(it).replace('−', '-'))
        if right and not any(abs(x) > 0 and (f'{abs(x):g}'.replace('.', ',') in it['explain']['vi'] or f'{abs(x):g}' in it['explain']['en']) for x in right) and not re.fullmatch(r'[A-Za-z .,=0-9]+', ctext(it)):
            bad.append((mod, 'correct value missing from the explanation', it['q']['en'][:40], ctext(it)))
bank_ok = 0
for mod, its in ITEMS.items():
    bank = json.load(open(os.path.join(ROOT, 'data', 'qbank', f'{mod}.json'), encoding='utf-8'))['items']; byq = {b['q']['en']: b for b in bank}
    for it in its:
        b = byq.get(it['q']['en'])
        if b is None: bad.append((mod, 'not in bank', it['q']['en'][:40])); continue
        if b['opts'][b['correct']]['en'] != ctext(it) or b['opts'][b['correct']]['vi'] != it['opts'][it.get('correct', 0)]['vi'] or sorted(o['en'] for o in b['opts']) != sorted(o['en'] for o in it['opts']) or b['level'] != 3: bad.append((mod, 'bank differs', it['q']['en'][:40]))
        else: bank_ok += 1
print(f'hard items: {total}; independent numeric checks run: {done}; items matched in assembled bank: {bank_ok}')
if bad:
    print('MISMATCHES:'); [print(' ', b) for b in bad]; sys.exit(1)
if done < 70: print('WARNING: fewer independent checks than expected', done); sys.exit(1)
print('verify_hard: OK')
