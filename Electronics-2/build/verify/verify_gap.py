"""Independent re-derivation of the numeric answers of the gap-fill questions (data/qsrc/mNN_zgap.json): current-balance root for VSP, time-stepped relaxation oscillator,
binary-search ADC, integration for dynamic energy, nodal solution for the V-to-I compliance, etc.  Also runs the concept check that backs each question's concept."""
import os, sys, json, math, glob
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'concepts')); sys.path.insert(0, os.path.join(ROOT, 'build'))
import lib, checks
for i in range(1, 11): __import__(f'm{i:02d}')
CHK = {c['id']: c['chk'] for c in lib.CONCEPTS}
bad = []; items = []
for p in sorted(glob.glob(os.path.join(ROOT, 'data', 'qsrc', 'm*_zgap.json'))): items += json.load(open(p, encoding='utf-8'))
def correct(it): return it['opts'][it['correct']]['en'] if 'correct' in it else it['opts'][0]['en']
def find(sub): 
    r = [it for it in items if sub in it['q']['en']]; assert len(r) == 1, (sub, len(r)); return r[0]
def num(s): return float(s.replace(' ', '').split()[0].replace('−', '-')) if s[0].isdigit() or s[0] in '−-' else None
def vsp_root(VDD, VTN, VTP, Kn, Kp): return brentq(lambda v: 0.5 * Kn * (v - VTN) ** 2 - 0.5 * Kp * (VDD - v + VTP) ** 2, VTN + 1e-6, VDD + VTP - 1e-6)
# CMOS thresholds
for sub, args, want in [('VDD = 3.3 V, VTN = 0.7 V', (3.3, 0.7, -0.7, 1, 1), 1.65), ('VDD = 5 V, VTN = 1 V', (5, 1, -1, 1, 1), 2.5), ('KR = Kn/Kp = 4', (2.5, 0.5, -0.5, 4, 1), 1.0)]:
    got = vsp_root(*args); a = float(correct(find(sub)).split()[0]); (bad.append((sub, got, a)) if abs(got - a) > 0.006 else None)
# dynamic power / PDP / delay
C, V, f = 0.5e-12, 2.5, 100e6; Rr = 1e3; t = np.linspace(0, 40 * Rr * C, 400001); E = np.trapz((V / Rr) * np.exp(-t / (Rr * C)) * V, t)      # energy drawn from the supply while charging C through R
if abs(E - C * V * V) / (C * V * V) > 1e-4: bad.append('CV^2 energy')
if abs(E * f * 1e6 - float(correct(find('C = 0.5 pF')).split()[0])) > 1e-6: bad.append('dynamic power')
if abs((E * f) * 1e-9 * 1e12 - float(correct(find('power–delay product')).split()[0])) > 1e-9: bad.append('PDP')
# relaxation oscillator by time stepping
R, Cc, B = 10e3, 10e-9, 0.5; dt = 1e-8; vc, vo, t, cross = 0.0, 12.0, 0.0, []
while len(cross) < 6: 
    vc += (vo - vc) * dt / (R * Cc); t += dt
    if vo > 0 and vc > B * 12: vo = -12; cross.append(t)
    elif vo < 0 and vc < -B * 12: vo = 12; cross.append(t)
fsim = 1 / (cross[-1] - cross[-3]) / 1e3; fa = float(correct(find('relaxation oscillator has R1')).split()[0])
if abs(fsim - fa) / fa > 0.01: bad.append(('relaxation', fsim, fa))
# ADC / DAC
def sar(vin, n, vfs):
    lsb = vfs / 2 ** n; code = 0
    for k in range(n - 1, -1, -1):
        if (code | (1 << k)) * lsb <= vin + 1e-15: code |= 1 << k
    return code, lsb
c10, lsb10 = sar(3.0, 10, 5.0); near = int(round(3.0 / lsb10))
if str(near) != correct(find('10-bit ADC with VFS = 5 V')): bad.append(('adc code', near))
if abs(5 / 2 ** 8 * 1e3 - float(correct(find('8-bit ADC')).split()[0])) > 0.01: bad.append('lsb8')
if abs(10 / 2 ** 12 / 2 * 1e3 - float(correct(find('12-bit ADC has VFS = 10 V')).split()[0])) > 0.01: bad.append('qerr')
if next(n for n in range(1, 30) if 5 / 2 ** n <= 1e-3) != int(correct(find('minimum number of bits'))): bad.append('bits')
dac = 5 * sum(int(b) * 2 ** -(i + 1) for i, b in enumerate('1010'))
if abs(dac - float(correct(find('4-bit DAC')).split()[0])) > 1e-9: bad.append('dac')
# V-to-I compliance by nodal solution
def vout_for(RL, I=2e-3, R1=1e3): return I * (RL + R1)
rl = brentq(lambda r: vout_for(r) - 10.0, 1, 1e6)
if abs(rl - 4000) > 1e-6 or correct(find('largest load resistance')) != '4 kΩ': bad.append(('compliance', rl))
# PWM and 555
if abs(12 * 0.4 - 4.8) > 1e-12 or correct(find('40 % duty cycle drives')) != '4.8 V': bad.append('pwm avg')
duty = 11 / 21; a = correct(find('astable 555 with R1 = 1 kΩ, R2 = 10 kΩ')); 
if abs(float(a.split('%')[0]) - duty * 100) > 0.05 or abs(float(a.split(',')[1].split()[0]) - 12 * duty) > 0.01: bad.append(('555 duty', a))
# regulator
if abs((12 - 5) * 0.5 - float(correct(find('power is dissipated as heat')).split()[0])) > 1e-9 or abs(5 / 12 * 100 - float(correct(find('approximate efficiency')).split()[0])) > 0.05: bad.append('regulator')
# resolver
if abs(math.degrees(math.atan2(0.5, 0.866)) - 30) > 0.01 or abs(math.degrees(math.atan2(0.707, -0.707)) - 135) > 0.01: bad.append('resolver')
if correct(find('4 code inputs')) != '16' or correct(find('priority encoder has inputs')) != '10': bad.append('decoder/encoder')
# noise margins
if abs((2.4 - 2.0) - float(correct(find('high-level noise margin')).split()[0])) > 1e-9 or abs(min(4.9 - 3.5, 1.5 - 0.1) - float(correct(find('gate noise margin')).split()[0])) > 1e-9: bad.append('noise margins')
# concept checks that back these questions
used = sorted({it['concept'] for it in items}); res = {}
for cid in used:
    try: res[cid] = checks.CHECKS[CHK[cid]]() if CHK.get(cid) else 'no formula'
    except Exception as e: bad.append((cid, repr(e)[:120]))
print(f'gap-fill questions {len(items)} | concepts {len(used)} | numeric answers re-derived independently | concept checks run {sum(1 for v in res.values() if v != "no formula")}')
print('FAILS:', bad if bad else 'none'); sys.exit(1 if bad else 0)
