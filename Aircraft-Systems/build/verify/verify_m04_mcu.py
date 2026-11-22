# -*- coding: utf-8 -*-
"""Verify phan mo rong module 04 (vi dieu khien, Floyd Ch.14): (1) mcu.py hai cai dat khop nhau; (2) khoa in cua 30 cau goc doc lai TU DONG tu van ban sach (PDF tr.854) khop khoa trong ngan hang tru 2 khoa in sai da ghi ro;
(3) cum tu bang chung cua tung cau goc tim lai trong van ban Floyd; (4) hai khoa in sai kiem lai bang chinh van ban (DMA co ba tin hieu BR/BG/BGACK; yeu cau bus khong cho het chu ky lenh; sach khong noi ngat 'khong the che');
(5) 24 cau bo sung tinh lai bang Fraction tu de bai va so voi lua chon dung; (6) 9 bai tu luan goc.   Chay: python3 build/verify/verify_m04_mcu.py -> 'FAILS: none'."""
import sys, os, re, json, glob
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import mcu as F
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, '|', str(info)[:200])
# ---- 1. two implementations
for n in range(1, 40): check(f'addr {n}', F.addresses_a(n) == F.addresses_b(n))
for vs, th, T in ((12, 2, 8), (5, 3, 4), (24, 1, 5), (9, 6, 10), (3.3, 1, 3)): check(f'pwm {vs},{th},{T}', abs(F.pwm_avg_a(vs, th, T) - F.pwm_avg_b(vs, th, T)) < 1e-12 and abs(F.duty_a(th, T) - F.duty_b(th, T)) < 1e-12)
for f, p, c in ((16e6, 8, 2000), (8e6, 64, 1250), (1e6, 1, 1000), (20e6, 256, 78125)): check(f'timer {f},{p},{c}', abs(F.timer_s_a(f, p, c) / F.timer_s_b(f, p, c) - 1) < 1e-12)
for b, r in ((16, 1000), (32, 1e6), (32, 1000), (16, 100)): check(f'rollover {b},{r}', abs(F.rollover_s_a(b, r) / F.rollover_s_b(b, r) - 1) < 1e-12)
for f, b, w in ((50, 3, 2), (100, 4, 1), (25, 3, 0), (40, 2, 3)): check(f'access {f},{b},{w}', abs(F.access_ns_a(f, b, w) - F.access_ns_b(f, b, w)) < 1e-9)
# ---- 2/3/4. keys and evidence from the book text
import fitz, glob
pdf = glob.glob(os.path.join(ROOT, '..', 'sources', 'textbooks', '*Floyd*.pdf'))[0]; d = fitz.open(pdf)
page = lambda p: re.sub(r'\s+', ' ', d[p - 1].get_text())
keys_txt = page(854)
tf_keys = re.search(r'True/False Quiz (.*?) Self-Test', keys_txt).group(1); st_keys = re.search(r'Self-Test (.*)$', keys_txt).group(1)
tf_k = re.findall(r'(\d+)\.\s*([TF])', tf_keys); st_k = re.findall(r'(\d+)\.\s*\(([a-d])\)', st_keys)
check('15 Dung/Sai keys parsed', len(tf_k) == 15, tf_k); check('15 Self-Test keys parsed', len(st_k) == 15, st_k)
meta = json.load(open(f'{ROOT}/data/verify/m04_mcu_meta.json'))
book = ' '.join(page(p) for p in range(800, 854)).lower()
n_ev = 0
for m in meta:
    if m['kind'] == 'tf':
        pk = dict((int(a), b) for a, b in tf_k).get(m['n']); check(f'T/F {m["n"]}: printed key in registry = key read from the book page ({pk})', m['printed'] == pk, (m['printed'], pk))
    elif m['kind'] == 'st':
        pk = dict((int(a), b) for a, b in st_k).get(m['n']); check(f'Self-Test {m["n"]}: printed key in registry = key read from the book page ({pk})', m['printed'] == pk, (m['printed'], pk))
    if m['kind'] in ('tf', 'st'):
        for ph in m['ev']: n_ev += 1; check(f'evidence {m["kind"]} {m["n"]}: {ph!r}', ph.lower() in book)
overruled = [(m['kind'], m['n']) for m in meta if m['kind'] in ('tf', 'st') and m['printed'] != m['ans']]
check('exactly two printed keys overruled (T/F 12 and Self-Test 13)', overruled == [('tf', 12), ('st', 13)], overruled)
sec = ' '.join(page(p) for p in range(824, 830)).lower()
check('book: DMA bus-request signals BR, BG, BGACK', all(x in sec for x in ('bus request (br)', 'bus grant (bg)', 'bus grant acknowledge (bgack)')))
check('book: bus requests do not complete the current instruction cycle; interrupts do', 'do not complete the current instruction cycle' in sec and 'allow the processor to complete the current instruction cycle' in sec)
check('book: the text of 14-5 never says that interrupts cannot be masked', 'mask' not in sec)
print('Floyd keys compared:', len(tf_k) + len(st_k), '| evidence phrases re-found:', n_ev)
# ---- 5. generated items recomputed from the stem
items = json.load(open(f'{ROOT}/data/qsrc/m04_mcu.json', encoding='utf-8')); gen = [i for i in items if i['origin'] == 'bo_sung']; gm = [m for m in meta if m['kind'] == 'gen']
check('24 generated items and 24 meta rows', len(gen) == len(gm) == 24, (len(gen), len(gm)))
num = lambda s: float(re.search(r'-?\d+(?:\.\d+)?', s.replace(' ', '').replace(',', '')).group(0))
UNIT = {'s': 1, 'min': 60, 'day': 86400, 'days': 86400}
n_gen = 0
for it, m in zip(gen, gm):
    cor = it['opts'][it['correct']]['en']; a = m['args']; fam = m['fam']; got = num(cor)
    if fam == 'addr': want = 1 << a[0]; ok = int(got) == want
    elif fam == 'pwm': want = float(Fr(a[0]) * Fr(a[1]) / Fr(a[2])); ok = abs(got - want) < 1e-9
    elif fam == 'duty': want = float(Fr(a[0], a[1]) * 100); ok = abs(got - want) < 1e-9
    elif fam == 'timer': want = float(Fr(a[2]) * Fr(a[1]) / Fr(int(a[0] * 1e6))) * 1000; ok = abs(got / want - 1) < 1e-9
    elif fam == 'rollover':
        unit = re.search(r'(day|min|s)s?\s*$', cor.strip()).group(1); want = float(Fr(2 ** a[0]) / Fr(a[1])); ok = abs(got * UNIT[unit] / want - 1) < 5e-3
    elif fam == 'wait': want = float((Fr(a[1]) + Fr(a[2])) * Fr(1000) / Fr(a[0])); ok = abs(got - want) < 1e-9
    else: ok = False; want = None
    check(f'generated {fam} {a}: option {cor!r} = recomputed {want}', ok); n_gen += 1
    check(f'generated {fam} {a}: options distinct', len({o["en"] for o in it['opts']}) == len(it['opts']))
print('generated items recomputed:', n_gen)
# ---- 6. essays
ess = json.load(open(f'{ROOT}/data/qsrc/m04_mcu_ess.json', encoding='utf-8'))
check('9 original essays from Floyd 14-8 / 14-9 checkups', len(ess) == 9 and all(e['origin'] == 'goc' and e['src']['en'].startswith('Floyd 14-') for e in ess))
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
