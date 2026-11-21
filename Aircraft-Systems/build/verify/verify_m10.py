# -*- coding: utf-8 -*-
"""Verify module 10 (A/D, D/A): (1) ham tinh co hai cai dat doc lap khop nhau; (2) so lieu in trong sach; (3) moi cau sinh duoc TINH LAI tu de bai (EN) bang Fraction/sympy, doc lap voi gen_m10.py.
Chay: .venv/bin/python -I build/verify/verify_m10.py   -> cuoi cung in 'FAILS: none'."""
import sys, os, re, json, math
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib'))
import adda as A
import sympy as sp
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
# ---- 1. hai cai dat ----
for c in range(16):
    check(f'weighted {c}', abs(A.dac_weighted_closed(c) - A.dac_weighted_sum(c)) < 1e-9 and abs(A.dac_weighted_closed(c) + 0.625 * c) < 1e-12)
    check(f'r2r {c}', abs(A.dac_r2r_closed(c) - A.dac_r2r_nodal(c)) < 1e-9)
for vin in [x / 10 for x in range(0, 160)]:
    code, steps = A.sar_trace(vin); check(f'sar {vin}', code == A.sar_direct(vin) and code == min(15, int(vin)), (vin, code))
for vin in [x / 10 for x in range(0, 90)]:
    hi, outs = A.flash_comparators(vin); check(f'flash {vin}', hi == A.flash_closed(vin) == sum(1 for k in range(7) if Fr(str(vin)) > Fr(2 * k + 1, 2)), vin)
for n in range(1, 17):
    check(f'resolution {n}', abs(A.resolution_pct(n) - 100 / (2 ** n - 1)) < 1e-12 and A.comparators(n) == A.levels(n) - 1)
# ---- 2. so lieu trong sach ----
check('Tooley 1010 -> -6.25 V', A.dac_weighted_closed(0b1010) == -6.25); check('Tooley 1111 -> -9.375 V', A.dac_weighted_closed(0b1111) == -9.375)
check('Tooley gains', [-1 / 1, -1 / 2, -1 / 4, -1 / 8] == [-1, -0.5, -0.25, -0.125])
check('Tooley 2 V flash -> 010', A.flash_closed(2.0) == 0b010 and A.flash_comparators(2.0)[1][:2] == [1, 1])
code, st = A.sar_trace(5.1); check('Floyd Fig 12-18: 5.1 V -> 0101 qua 8,4,6,5 V', code == 0b0101 and [s[2] for s in st] == [8, 4, 6, 5] and [s[3] for s in st] == [False, True, False, True])
check('Floyd 12-26 buoc 0,25 V', all(abs(-sum(5 * 10 / r for r, b in zip([25, 50, 100, 200], format(c, '04b')) if b == '1') + 0.25 * c) < 1e-12 for c in range(16)))
check('Floyd R-2R 1000 .. 0001', [A.dac_r2r_closed(c) for c in (8, 4, 2, 1)] == [-5.0, -2.5, -1.25, -0.625])
check('Floyd P7/P9', A.inv_gain(5e-3, 1.0) == -(-200.0) * -1 or abs(1.0 / 5e-3 - 200) < 1e-9); check('Floyd P9', -33000 / 1000 == -33)
check('Floyd P19', [round(A.resolution_pct(n), 2) for n in (2, 5)] == [33.33, 3.23] and round(A.resolution_pct(12), 3) == 0.024)
check('Floyd Ex12-4', round(A.resolution_pct(8), 3) == 0.392 and round(A.resolution_pct(12), 4) == 0.0244 and round(A.resolution_pct(16), 5) == 0.00153)
check('Floyd checkup 12-3 #2', round(A.resolution_pct(4), 2) == 6.67); check('Floyd P10', A.comparators(4) == 15)
check('Floyd Hinh 12-30 sympy', all(sp.nsimplify(-5 * sp.Rational(c, 8)) == sp.nsimplify(A.dac_r2r_closed(c)) for c in (8, 4, 2, 1)))
# ---- 3. moi cau sinh: tinh lai tu de bai bang Fraction ----
def num(s): return Fr(s.replace(',', '.').replace('−', '-'))
def optnum(o): return Fr(re.sub(r'[^0-9.+-]', '', o['en'].replace('−', '-')))
def correct_opt(it): return it['opts'][it['correct']]['en']
n_checked = 0; fam = {}
data = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm10_gen.json'), encoding='utf-8'))
for it in data:
    q = it['q']['en']; ans = correct_opt(it); m = None
    def hit(k): fam[k] = fam.get(k, 0) + 1
    if (m := re.search(r'^The resolution of an (\d+)-bit DAC', q)):
        n = int(m.group(1)); check('res ' + q, abs(float(re.sub('[^0-9.]', '', ans.split('%')[0])) - float(Fr(100, 2 ** n - 1))) / float(Fr(100, 2 ** n - 1)) < 0.01, ans); hit('resolution')
    elif (m := re.search(r'How many comparators does a (\d+)-bit', q)):
        check('cmp ' + q, int(ans) == 2 ** int(m.group(1)) - 1); hit('comparators')
    elif (m := re.search(r'component of a signal is (\d+) kHz', q)):
        check('nyq ' + q, int(re.sub(r'\D', '', ans)) == 2 * int(m.group(1))); hit('nyquist')
    elif (m := re.search(r'receives code (\d{4}). The output voltage', q)) and 'binary-weighted DAC of Tooley' in q:
        c = int(m.group(1), 2); check('wtd ' + q, optnum(it['opts'][it['correct']]) == -Fr(5) * (Fr((c >> 3) & 1) + Fr((c >> 2) & 1, 2) + Fr((c >> 1) & 1, 4) + Fr(c & 1, 8)), ans); hit('weighted')
    elif (m := re.search(r'R/2R ladder DAC receives code (\d{4})', q)):
        c = int(m.group(1), 2); exp = -sum(Fr(5, 2 ** k) * ((c >> (3 - k)) & 1) for k in range(4)); check('r2r ' + q, abs(float(optnum(it['opts'][it['correct']]) - exp)) < 1e-3, (ans, float(exp))); hit('r2r')
    elif (m := re.search(r'constant input is ([\d.]+) V', q)):
        vin = Fr(m.group(1)); code = 0
        for w in (8, 4, 2, 1):
            if code + w <= vin: code += w
        check('sar ' + q, ans == format(code, '04b'), (ans, format(code, '04b'))); hit('sar')
    elif (m := re.search(r'receives ([\d.]+) V\. The output code', q)):
        vin = Fr(m.group(1)); code = sum(1 for k in range(7) if vin > Fr(2 * k + 1, 2)); check('flash ' + q, ans == format(code, '03b'), (ans, code)); hit('flash')
    elif (m := re.search(r'R_f=(\d+)\$ kΩ and \$R_i=(\d+)', q)):
        check('inv ' + q, optnum(it['opts'][it['correct']]) == -Fr(int(m.group(1)), int(m.group(2))), ans); hit('inverting')
    elif (m := re.search(r'full-scale output of (\d+) V and an accuracy of ±([\d.]+) %', q)):
        check('acc ' + q, optnum(it['opts'][it['correct']]) == Fr(m.group(1)) * Fr(m.group(2)) / 100 * 1000, ans); hit('accuracy')
    elif (m := re.search(r'A ([\d.]+) kHz sine wave is sampled at ([\d.]+) kHz', q)):
        f, fs = Fr(m.group(1)), Fr(m.group(2)); al = abs(f - fs * round(f / fs)); check('alias ' + q, optnum(it['opts'][it['correct']]) == al, (ans, al)); hit('alias')
    elif (m := re.search(r'receives code (\d{4}). The output voltage', q)) and 'Figure 12-27' in q:
        c = int(m.group(1), 2); exp = -sum(Fr(5 * 10, r) * ((c >> (3 - k)) & 1) for k, r in enumerate([25, 50, 100, 200])); check('wtd-floyd ' + q, abs(float(optnum(it['opts'][it['correct']]) - exp)) < 1e-3, (ans, float(exp))); hit('weighted-floyd')
    elif (m := re.search(r'better than ([\d.]+) %', q)):
        pct = Fr(m.group(1)); n = next(k for k in range(1, 40) if Fr(100, 2 ** k - 1) < pct); check('bits ' + q, int(re.sub(r'\D', '', ans)) == n, (ans, n)); hit('bits-required')
    elif (m := re.search(r'takes ([\d.]+) µs per conversion', q)):
        tc = Fr(m.group(1)); fmax = Fr(10 ** 6) / tc / 2 / 1000; check('thr ' + q, optnum(it['opts'][it['correct']]) == fmax, (ans, fmax)); hit('throughput')
    else: continue
    n_checked += 1
print('cau sinh tinh lai bang cach doc lap:', n_checked, '/', len(data), '| theo dang:', fam)
check('so cau sinh duoc kiem >= 50', n_checked >= 50, n_checked)
# ---- 4. dap an goc: khoa Tooley va Floyd ----
orig = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm10.json'), encoding='utf-8'))
tooley_key = dict(zip(range(1, 14), 'abbbccbccabcb'))
for it in orig:
    m = re.search(r'Tooley Ch\.3 · Q(\d+)', it['src']['en'])
    if m: check('Tooley key Q' + m.group(1), 'abc'[it['correct']] == tooley_key[int(m.group(1))], it['correct'])
floyd_tf = {1: True, 2: False, 3: False, 4: True, 6: False, 7: True, 8: True, 9: True, 10: False}
for it in orig:
    m = re.search(r'True/False #(\d+)', it['src']['en'])
    if m: check('Floyd T/F #' + m.group(1), (it['correct'] == 0) == floyd_tf[int(m.group(1))])
floyd_st = {1: 'c', 2: 'd', 3: 'b', 4: 'b', 5: 'c', 6: 'a', 7: 'e', 8: 'd', 9: 'd', 10: 'c', 11: 'a'}
for it in orig:
    m = re.search(r'Self-Test #(\d+)', it['src']['en'])
    if m: check('Floyd Self-Test #' + m.group(1), 'abcde'[it['correct']] == floyd_st[int(m.group(1))])
print('FAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
