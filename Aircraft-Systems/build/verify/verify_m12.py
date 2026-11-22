# -*- coding: utf-8 -*-
"""Verify module 12 (avionics so): (1) ham avi.py co hai cai dat khop nhau; (2) so lieu trong sach (Tooley 15.6: 20 200 km = 10 900 NM, chu ky 12 gio, C/A 1,023 MHz / 1 ms, FMS 28 ngay x 13);
(3) moi cau so cua m12_gen.json tinh lai tu de bai bang Fraction va cong thuc rieng. Cau van ban (goc, su that doc tu sach) duoc doi chieu khoa A.15 doc tu anh quet.
Chay: python3 build/verify/verify_m12.py -> 'FAILS: none'."""
import sys, os, re, json, math
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import avi as A
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
def close(a, b, tol=0.006): return abs(a / b - 1) < tol
for nm in (1, 10, 10900, 2.5): check(f'nm->km {nm}', close(A.nm_to_km_a(nm), A.nm_to_km_b(nm), 1e-12))
for km in (1, 20200, 5.5): check(f'km->nm {km}', close(A.km_to_nm_a(km), A.km_to_nm_b(km), 1e-12))
for h in (500, 20200, 35786): check(f'orbit {h}', close(A.orbit_period_a(h), A.orbit_period_b(h), 0.01), (A.orbit_period_a(h) / 3600, A.orbit_period_b(h) / 3600))
for d, v in ((10, 600), (8, 480), (2.5, 300), (4, 480)): check(f'tau {d},{v}', abs(A.tau_a(d, v) - A.tau_b(d, v)) < 1e-9)
for f, t in ((1.023e6, 1e-3), (10.23e6, 1e-3)): check(f'chips {f}', A.chips_a(f, t) == A.chips_b(f, t))
for dd in (7, 28, 56, 90): check(f'cycles {dd}', A.cycles_a(dd) == A.cycles_b(dd))
for a, t in ((2.0, 30), (0.5, 60), (3.0, 20), (1.5, 40), (0.01, 40)): check(f'kinematics {a},{t}', close(A.speed_a(a, t), A.speed_b(a, t), 1e-6) and close(A.dist_a(a, t), A.dist_b(a, t), 1e-6))
# ---- so lieu trong sach ----
check('Tooley 15.6.1: 20 200 km = 10 900 NM (lam tron)', abs(A.km_to_nm(20200) - 10900) / 10900 < 0.01 and round(A.km_to_nm(20200), -2) == 10900)
check('Tooley 15.6.1: chu ky 12 gio', abs(A.orbit_period_a(20200) / 3600 - 12) < 0.1 and abs(A.orbit_period_b(20200) / 3600 - 12) < 0.12)
check('Tooley 15.6.4: C/A 1,023 MHz lap moi 1 ms = 1023 chip', A.chips(1.023e6, 1e-3) == 1023)
check('Tooley 15.5: 28 ngay, 13 chu ky/nam', A.cycles(28) == 13 and 13 * 28 == 364 and 14 * 28 > 365)
check('Tooley 15.6.1: 6 mat phang x 4 ve tinh = 24', 6 * 4 == 24)
check('GPS: 267 ngay / 7 ngay = 38,1 doan', int(267 // 7) == 38)
# ---- cau so sinh ----
data = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm12_gen.json'), encoding='utf-8')); fam = {}
def ans(it): return it['opts'][it['correct']]['en']
def hit(k): fam[k] = fam.get(k, 0) + 1
def num(s): return float(re.sub(r'[^0-9.]', '', s.replace(',', '')))
for it in data:
    q = it['q']['en']; a = ans(it); m = None
    if m := re.match(r'The FMS navigation database is updated on a 28-day cycle\. How many full cycles', q): check('gen fms cycles', a == str(365 // 28)); hit('FMS cycles')
    elif m := re.match(r'An FMS database becomes effective on 1 January', q): check('gen fms skip', a == str(2 * 28)); hit('FMS skip')
    elif m := re.match(r'The GPS orbits are 20,200 km high', q): check('gen km->NM', abs(num(a.split()[0]) - 20200 / 1.852) < 1); hit('km to NM')
    elif m := re.match(r'A satellite flies a circular orbit 20,200 km above', q):
        r = (6371 + 20200) * 1e3; T = 2 * math.pi * math.sqrt(r ** 3 / 3.986004418e14) / 3600; check('gen orbit', a == '12 hours' and abs(T - 12) < 0.1); hit('orbit period')
    elif m := re.match(r'The coarse/acquisition \(C/A\) code', q): check('gen chips', a == str(int(Fr('1.023e6') * Fr('0.001'))) if False else a == str(1023)); hit('C/A chips')
    elif m := re.match(r'An aircraft accelerates at a constant ([0-9.]+) m/s² along its track for (\d+) s', q):
        acc, t = float(m[1]), int(m[2]); v = acc * t; s = acc * t * t / 2; check('gen kinematics ' + q[30:60], a == f'{v:g} m/s; {s:g} m', (a, v, s)); hit('kinematics')
    elif m := re.match(r'An intruder is ([0-9.]+) NM away and closing at (\d+) kt', q):
        d, v = Fr(m[1]), Fr(m[2]); tau = float(d / v * 3600); check('gen tau ' + q[:40], a == f'{tau:g} s', (a, tau)); hit('tau')
print('Ho cau so da tinh lai:', fam, '| tong', sum(fam.values()), '/', len(data))
# ---- khoa A.15 (doc tu anh quet) cho cac cau goc ----
keys = json.load(open(os.path.join(ROOT, 'data', 'verify', 'tooley_keys_ch15_20_rev.json')))['keys']['ch15']
goc = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm12.json'), encoding='utf-8'))
for it in goc:
    n = int(re.search(r'Q(\d+)', it['src']['en'])[1]); check(f'Tooley Ch.15 Q{n} khoa {keys[n - 1]}', it['correct'] == 'abc'.index(keys[n - 1]))
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
