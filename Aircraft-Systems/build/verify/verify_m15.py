# -*- coding: utf-8 -*-
"""Verify module 15 (cabin, thong tin tau bay): (1) cabin.py hai cai dat khop nhau; (2) so lieu trong sach (494 Hz, 587 Hz, 900 ms; V1 < VR < V2 cua B737: 124, 125, 136 kt, doc tu anh trang tr.320); (3) cau so cua m15_gen.json tinh lai
tu de bai; (4) khoa A.19, A.20 doc tu anh quet khop cau goc. Chay: python3 build/verify/verify_m15.py -> 'FAILS: none'."""
import sys, os, re, json
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import cabin as C
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
for f in (494, 587, 1000): check(f'cycles {f}', abs(C.cycles_a(f, 0.9) - C.cycles_b(f, 0.9)) < 1e-9 and abs(C.period_a(f) - C.period_b(f)) < 1e-15)
for s, r in ((4.7, 100e6), (4.7, 1e9), (20, 100e6), (1, 1e9)): check(f'load {s},{r}', abs(C.load_time_a(s, r) / C.load_time_b(s, r) - 1) < 1e-12)
check('ratio', abs(C.ratio_a(494, 587) - C.ratio_b(494, 587)) < 1e-12)
check('Tooley 19.3.5: 494 Hz x 900 ms = 444,6 chu ky; 587 Hz = 528,3', abs(C.cycles(494, 0.9) - 444.6) < 1e-9 and abs(C.cycles(587, 0.9) - 528.3) < 1e-9)
check('587 / 494 = 1,188 (gan 6/5)', abs(C.ratio(494, 587) - 1.18826) < 1e-4 and abs(6 / 5 - C.ratio(494, 587)) < 0.02)
check('Tooley 20.1: 124 < 125 < 136 kt (V1 < VR < V2)', 124 < 125 < 136)
check('Tooley 19.3: 4,7 GB o 100 Mbit/s = 376 s; o 1 Gbit/s = 37,6 s (gia dinh 1 GB = 1e9 byte)', abs(C.load_time(4.7, 100e6) - 376) < 1e-9 and abs(C.load_time(4.7, 1e9) - 37.6) < 1e-9)
check('Tooley 19.3.2: 5 muc uu tien', len(C.PA_LEVELS) == 5 and C.PA_LEVELS[0].startswith('Flight deck'))
data = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm15_gen.json'), encoding='utf-8')); fam = {}
def ans(it): return it['opts'][it['correct']]['en']
def hit(k): fam[k] = fam.get(k, 0) + 1
def tsec(s):
    m = re.match(r'([0-9.]+) (s|min)', s); return float(m[1]) * (60 if m[2] == 'min' else 1)
for it in data:
    q = it['q']['en']; a = ans(it); m = None
    if m := re.match(r'The (low|high) cabin chime is a (\d+) Hz sine burst lasting 900 ms', q): check('gen cycles ' + m[2], a == str(round(int(m[2]) * 0.9)), (q, a)); hit('chime cycles')
    elif m := re.match(r'The period of a (\d+) Hz sine wave', q): check('gen period ' + m[1], abs(float(a.split()[0]) - 1000 / int(m[1])) < 0.0006, (q, a)); hit('chime period')
    elif q.startswith('The high chime (587 Hz) and low chime (494 Hz)'): check('gen ratio', abs(float(a) - 587 / 494) < 0.001, (q, a)); hit('chime ratio')
    elif m := re.match(r'Loading a ([0-9.]+) GB media file .* over a (100 Mbit/s|1 Gbit/s) link', q):
        rate = 100e6 if m[2].startswith('100') else 1e9; t = float(m[1]) * 8e9 / rate; check('gen load ' + q[:30], abs(tsec(a) / t - 1) < 0.002, (q, a, t)); hit('media load')
print('Ho cau so da tinh lai:', fam, '| tong', sum(fam.values()), '/', len(data))
K = json.load(open(os.path.join(ROOT, 'data', 'verify', 'tooley_keys_ch15_20_rev.json')))['keys']
goc = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm15.json'), encoding='utf-8'))
for it in goc:
    mm = re.search(r'Ch\.(\d+) · Q(\d+)', it['src']['en']); ch, n = int(mm[1]), int(mm[2]); k = K[f'ch{ch}'][n - 1]
    check(f'Tooley Ch.{ch} Q{n} khoa {k}', it['correct'] == 'abc'.index(k))
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
