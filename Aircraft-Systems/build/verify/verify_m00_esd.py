# -*- coding: utf-8 -*-
"""Verify cau so cua kiem tra dau vao (m00) va phan ESD cua Module 09: tinh lai tu de bai bang Fraction/cong thuc rieng; khoa Floyd Ch.1 (tr.64) va Tooley A.12 (tr.380).
Chay: python3 build/verify/verify_m00_esd.py -> 'FAILS: none'."""
import sys, os, re, json
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
UN = {'': 1, 'k': 1e3, 'M': 1e6, 'm': 1e-3, 'μ': 1e-6, 'n': 1e-9}
def val(s):
    m = re.match(r'([0-9.]+) ?([kMmμn]?)(Hz|s|V|mA|%)', s.replace(' ', '', 0)); return float(m[1]) * UN[m[2]] if m else None
def ans(it): return it['opts'][it['correct']]['en']
def close(a, b, t=0.002): return abs(a / b - 1) < t
fam = {}
def hit(k): fam[k] = fam.get(k, 0) + 1
for it in json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm00_gen.json'), encoding='utf-8')):
    q = it['q']['en']; a = ans(it); m = None
    if m := re.match(r'A periodic waveform has a frequency of ([0-9.]+ ?[kM]?Hz)\. Its period', q): check('m00 T ' + m[1], close(val(a), 1 / val(m[1].replace(' ', ''))), (q, a)); hit('period')
    elif m := re.match(r'A waveform has a period of ([0-9.]+ ?[mμn]?s)\. Its frequency', q): check('m00 f ' + m[1], close(val(a), 1 / val(m[1].replace(' ', ''))), (q, a)); hit('frequency')
    elif m := re.match(r'A pulse has a width of ([0-9.]+ ?[mμn]?s) and a period of ([0-9.]+ ?[mμn]?s)\. The duty cycle', q): check('m00 duty', close(float(a.split()[0]), 100 * val(m[1].replace(' ', '')) / val(m[2].replace(' ', ''))), (q, a)); hit('duty')
    elif q.startswith('A waveform has a period of 5 ms and a duty cycle of 40 %'): check('m00 tw', a == '2 ms'); hit('pulse width')
    elif m := re.match(r'How many different values can (\d+) binary bits represent', q): check('m00 2^n', a == str(2 ** int(m[1]))); hit('2^n')
    elif q.startswith('A 1 MHz clock. The number of clock pulses in 2.5 ms'): check('m00 pulses', a == '2,500' and Fr(10 ** 6) * Fr(5, 2000) == 2500); hit('clock pulses')
    else: check('m00 khong nhan dang', False, q)
print('m00 cau so da tinh lai:', fam, sum(fam.values()), '/ 15')
# khoa in Floyd Ch.1: TF dung; Self-Test 8 cau lech da sua (2,3,7,8,9,11,12,13) va 7 cau con lai khop
goc = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm00.json'), encoding='utf-8'))
printed = 'b c a b a d b a d e c a d d b'.split(); right_theory = 'b d c b a d c d c e b c a d b'.split(); changed = {2, 3, 7, 8, 9, 11, 12, 13}
for it in goc:
    mm = re.search(r'Self-Test (\d+)', it['src']['en'])
    if not mm: continue
    n = int(mm[1]); check(f'Floyd Ch.1 ST{n} dap an dung {right_theory[n - 1]}', it['correct'] == 'abcde'.index(right_theory[n - 1]))
    check(f'Floyd Ch.1 ST{n}: nhan nguon ' + ('co khoa in' if n in changed else 'khop khoa in'), (('printed key' in it['src']['en']) == (n in changed)) and (n in changed or printed[n - 1] == right_theory[n - 1]), (n, it['src']['en']))
tf_keys = 'TFTTFTTFFT'
for it in goc:
    mm = re.search(r'True/False (\d+)', it['src']['en'])
    if mm: n = int(mm[1]); check(f'Floyd Ch.1 TF{n}', it['correct'] == (0 if tf_keys[n - 1] == 'T' else 1))
# theory checks for numeric ST items
check('ST4: 1/50 Hz = 20 ms', Fr(1, 50) == Fr(20, 1000)); check('ST5: T = 4 tW -> 25 %', Fr(1, 4) == Fr(25, 100))
# ---- ESD ----
esd = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm09_esd.json'), encoding='utf-8')); K = json.load(open(os.path.join(ROOT, 'data', 'verify', 'tooley_keys_ch15_20_rev.json')))['keys']['ch12']
T121 = [(35e3, 1.5e3), (18e3, 1.2e3), (15e3, 1e3), (11e3, 350), (10e3, 250), (8e3, 150)]; nes = 0
for it in esd:
    q = it['q']['en']; a = ans(it); m = None
    if it['origin'] == 'goc': n = int(re.search(r'Q(\d+)', it['src']['en'])[1]); check(f'Tooley Ch.12 Q{n} khoa {K[n - 1]}', it['correct'] == 'abc'.index(K[n - 1])); continue
    if q.startswith('By Table 12.1, when'):
        ratio = int(a); ok = any(abs(ratio - hi / lo) <= 0.5 for hi, lo in T121); check('esd ratio ' + q[20:60], ok, (q, a)); nes += 1
    elif q.startswith('A wrist-strap lead has a 1 MΩ'):
        V = int(re.search(r'at (\d+) V', q)[1]); check('esd current', abs(float(a.split()[0]) - V / 1e6 * 1e3) < 1e-9, (q, a)); nes += 1
print('ESD cau so da tinh lai:', nes)
check('Bang 12.1: 35 kV / 1,5 kV = 23,3 lan; 1,5 kV / 100 V = 15 lan', abs(35e3 / 1.5e3 - 23.33) < 0.01 and 1500 / 100 == 15 and 35e3 / 100 == 350)
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
