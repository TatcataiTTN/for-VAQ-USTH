# -*- coding: utf-8 -*-
"""Kiem doc lap cho 11 bai tap cuoi chuong cua Floyd (m11_fex.json, m10_fex.json).
 1. Dap an in doc TU DONG tu lop chu PDF (floyd_crop.answer_text) va so voi chuoi dap an ghi trong gen_floyd_ex.
 2. Moi dap an duoc tinh lai bang CACH KHAC voi gen (Fraction, logarit, mo phong tung flip-flop cua bo dem gon song), roi so voi dap an in va voi loi giai trong ngan hang.
 3. Hai bai co dap an in lech de (7-27, 7-31) va cac chenh lech nho (7-21, 12-19, 12-7) duoc chung minh bang so, va phai nam trong nhan nguon / loi giai.
 4. Anh de va anh dap an ton tai.   Chay: .venv/bin/python build/verify/verify_floyd_ex.py -> 'FAILS: none'"""
import os, sys, json, math, re
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'gen')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib'))
import floyd_crop as FC, seq as S
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, '|', str(info)[:220])
meta = json.load(open(f'{ROOT}/data/verify/floyd_ex_meta.json')); by = {(m['ch'], m['n']): m for m in meta}
items = {}
for mid in ('m10', 'm11'):
    for it in json.load(open(f'{ROOT}/data/qsrc/{mid}_fex.json')):
        mm = re.search(r'Ch\.(\d+) · Problem (\d+)', it['src']['en']); items[int(mm.group(1)), int(mm.group(2))] = it
sol = lambda ch, n: items[ch, n]
def has(ch, n, *tokens, lang='en'):
    t = sol(ch, n)['sol'][lang]; return all(x in t for x in tokens)
# ---- 1. printed answers read from the PDF text layer
for m in meta:
    txt = FC.answer_text(m['ans_page'], m['n']).replace('æ', 'Ω').replace('mF', 'µF') if False else FC.answer_text(m['ans_page'], m['n'])
    key = re.sub(r'\s+', '', m['printed'].replace('µ', 'm').replace('Ω', 'æ')); got = re.sub(r'\s+', '', txt)
    check(f'Ch.{m["ch"]} P{m["n"]}: printed answer {m["printed"]!r} found in the PDF text ({txt[:60]!r})', key.split('(use')[0] in got or key in got, (key, got[:80]))
# ---- 2. independent recomputation
check('7-21: 1/(20 ns + 40 ns) = 16.667 MHz; printed 16.66 is the truncated value', abs(1 / Fr(60, 10 ** 9) / 10 ** 6 - Fr(50, 3)) == 0 and math.floor(16.666666 * 100) / 100 == 16.66 and has(7, 21, '16.67'))
check('7-23: 16 x 8 mA = 128 mA; 4 V x 128 mA = 512 mW', Fr(16 * 8) == 128 and Fr(4) * 128 == 512 and has(7, 23, '128 mA', '512 mW'))
tw = math.log(2) * 1e3 * 1e-12                                                       # 0,693 ns (cach suy ra, khong dung 0,7)
check('7-27: t_W = 0.7 R C = 0.7 ns (and ln2 R C = 0.693 ns, 1 % from 0.7)', abs(tw - 0.7e-9) / 0.7e-9 < 0.01 and has(7, 27, '0.7 ns', '0.07 µs'))
check('7-27: the printed 0.07 us (70 ns) equals 0.7 R C only for C = 100 pF, 100 times the 1 pF of the statement', abs(0.7 * 1e3 * 100e-12 - 0.07e-6) < 1e-15 and abs(0.07e-6 / 0.7e-9 - 100) < 1e-9)
import subprocess
ocr = subprocess.run(['tesseract', f'{ROOT}/assets/figures/floyd_ex_ch07_a27.png', 'stdout', '--psm', '7'], capture_output=True, text=True).stdout
check('7-27: OCR of the printed-answer image reads a micro-like glyph followed by s (tesseract reads the micro sign as p), NOT ms as the PDF text layer does; the micro sign itself was confirmed by eye on the zoomed image', re.search(r'0\.07\s*[µμup]s', ocr) is not None and 'ms' not in ocr, ocr)
R = Fr(1, 2) / (Fr(11, 10) * Fr(1, 10 ** 6)); t_exact = -math.log(1 - 2 / 3) * float(R) * 1e-6
check('7-29: R1 = 0.5 s / (1.1 x 1 uF) = 454.5 kOhm and the exact RC ln3 charge to 2/3 Vcc gives 0.4994 s', abs(float(R) - 454545.45) < 1 and abs(t_exact - 0.4994) < 5e-4 and has(7, 29, '454.5'))
check('7-29: with 430 kOhm t = 1.1 R C = 0.473 s', abs(1.1 * 430e3 * 1e-6 - 0.473) < 1e-3 and has(7, 29, '0.473'))
C = Fr(4, 10 ** 9); s = Fr(144, 100) / (10 ** 4 * C); r2 = s - Fr(4, 5) * s; r1 = Fr(4, 5) * s - r2
check('7-31: R1 + 2 R2 = 36 kOhm, R2 = 7.2 kOhm, R1 = 21.6 kOhm for 10 kHz, C = 4 nF, D = 80 %', (s, r2, r1) == (36000, 7200, 21600) and has(7, 31, '21.6', '7.2'))
fr = lambda a, b, c: Fr(144, 100) / ((a + 2 * b) * c); du = lambda a, b: (a + b) / (a + 2 * b)
check('7-31: E24 22 kOhm and 7.5 kOhm give 9.73 kHz and 79.7 %', abs(float(fr(22000, 7500, C)) - 9729.7) < 0.1 and abs(float(du(22000, 7500)) - 0.7973) < 1e-4 and has(7, 31, '9.73', '79.7'))
check('7-31: printed R1 = 9.1k, R2 = 4.3k give 20.3 kHz and 75.7 % at C = 4 nF; they give 10 kHz only for C = 8.14 nF', abs(float(fr(9100, 4300, C)) - 20339) < 1 and abs(float(du(9100, 4300)) - 0.757) < 1e-3 and abs(float(Fr(144, 100) / (Fr(17700) * 10 ** 4)) - 8.136e-9) < 1e-12 and has(7, 31, '20.3', '75.7', '0.008'))
check('8-25: a Johnson counter of n flip-flops has 2n distinct states (simulated); n = 2, 4, 6, 9 for modulus 4, 8, 12, 18',
      all(len({S.johnson_b(n, k) for k in range(4 * n)}) == 2 * n for n in (2, 4, 6, 9)) and [M // 2 for M in (4, 8, 12, 18)] == [2, 4, 6, 9])
def settle(n, tpd, before):                                                          # mo phong: tang 1, tang cao nhat bi doi * tpd
    after = (before + 1) % (1 << n); changed = [i for i in range(n) if ((before ^ after) >> i) & 1]; return (max(changed) + 1) * tpd, after
res = [(settle(3, 8, b)[0], format(settle(3, 8, b)[1], '03b'), format(b, '03b')) for b in range(8)]; worst = max(r[0] for r in res); wstates = sorted((r[2] + ' to ' + r[1]) for r in res if r[0] == worst)
check('9-5: worst-case ripple settling 3 x 8 = 24 ns for 011 to 100 and 111 to 000 (simulated over all 8 transitions)', worst == 24 and wstates == ['011 to 100', '111 to 000'] and has(9, 5, '24 ns', '011 → 100', '111 → 000'), (worst, wstates))
check('9-7: synchronous: one propagation delay, 8 ns', has(9, 7, '8 ns'))
check('12-7: 1 V / 5 mV = 200 (magnitude), -200 signed for an inverting amplifier', Fr(1) / Fr(5, 1000) == 200 and has(12, 7, '200', '−200'))
check('12-9: -Rf/Ri = -33', -Fr(33000, 1000) == -33 and has(12, 9, '−33'))
res3 = [100 / (2 ** n - 1) for n in (2, 5, 12)]
check('12-19: 33.33 %, 3.226 % (printed 3.22 truncated), 0.0244 % (printed 0.024)', abs(res3[0] - 33.3333) < 1e-3 and abs(res3[1] - 3.2258) < 1e-3 and math.floor(res3[1] * 100) / 100 == 3.22 and abs(res3[2] - 0.02442) < 1e-4 and has(12, 19, '33.33', '3.226', '0.0244'))
# ---- 3. the discrepancy is in the source label
for ch, n in ((7, 27), (7, 31)): check(f'{ch}-{n}: label says the printed answer disagrees with the statement', 'disagrees' in sol(ch, n)['src']['en'] and 'lệch' in sol(ch, n)['src']['vi'])
check('exactly two items marked as printed-answer mismatches', sorted((m['ch'], m['n']) for m in meta if m['mismatch']) == [(7, 27), (7, 31)])
# ---- 4. images
for m in meta:
    for f in (m['q_png'], m['a_png']):
        p = f'{ROOT}/assets/figures/{f}'; check(f'image {f}', os.path.exists(p) and os.path.getsize(p) > 500)
# ---- 5. out-of-scope check recorded in notes: Floyd 12-27 (not a bank item)
t = FC.answer_text(922, 27); check('12-27 printed answer read from the PDF: 18.75 million instructions/s', '18.75 million' in t, t)
import fitz
d = FC.doc(); body = ' '.join(d[p - 1].get_text() for p in range(729, 733)).replace('\n', ' ')
check('12-27: the text of 12-5 says eight 32-bit instructions per clock cycle, so 600 MHz x 8 = 4.8 x 10^9 per second (and 600 MHz / 32 = 18.75 MHz is the printed number)', 'eight 32-bit instructions to the functional units during every clock cycle' in re.sub(r'\s+', ' ', body) and 8 * 600e6 == 4.8e9 and 600e6 / 32 == 18.75e6)
print('items checked:', len(meta), '| bank files:', {k: len(json.load(open(f'{ROOT}/data/qsrc/{k}_fex.json'))) for k in ('m10', 'm11')})
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
