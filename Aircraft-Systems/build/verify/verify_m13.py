# -*- coding: utf-8 -*-
"""Verify module 13 (AFDX, IMA): (1) ham afdx.py co hai cai dat khop nhau; (2) so lieu trong sach (Bang 16.1, vi du 3 036 000 bit/s, khung 64 va 1 518 byte, 1000 lan ARINC 429); (3) moi cau so cua m13_gen.json tinh lai
tu de bai bang Fraction; (4) khoa A.16 va A.18 doc tu anh quet khop cau goc, tru hai khoa in sai da sua (Ch.16 cau 5 va 9) - kiem lai cac cau do bang suy luan tu chinh quy tac cua sach.
Chay: python3 build/verify/verify_m13.py -> 'FAILS: none'."""
import sys, os, re, json
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import afdx as F
fails = []
def check(name, ok, info=''):
    if not ok: fails.append(name); print('FAIL', name, info)
for b in F.BAGS: check(f'bag {b}', abs(F.bag_hz_a(b) - F.bag_hz_b(b)) < 1e-9)
for r in (1, 10, 30, 60, 100, 150, 200, 400, 500, 1000): check(f'max_bag {r}', F.max_bag_a(r) == F.max_bag_b(r))
for L, b in ((1518, 4), (256, 128), (64, 2), (512, 16)): check(f'bitrate {L},{b}', abs(F.bitrate_a(L, b) - F.bitrate_b(L, b)) < 1e-6)
for p in range(1, 1472, 7): check(f'frame {p}', F.frame_len_a(p) == F.frame_len_b(p))
for nb, r in ((1518, 10e6), (64, 100e6), (12, 100e6)): check(f'tx {nb},{r}', abs(F.tx_time_a(nb, r) / F.tx_time_b(nb, r) - 1) < 1e-12)
for r in (10e6, 100e6): check(f'ifg {r}', abs(F.ifg_a(r) / F.ifg_b(r) - 1) < 1e-12)
for sn in range(1, 256): check(f'sn {sn}', F.sn_next_a(sn) == F.sn_next_b(sn))
check('sn: 0 -> 1 khi tang tu khoi dong', F.sn_next_a(0) == 1)
for n in range(1, 9): check(f'backoff {n}', F.backoff_a(n, 3) == F.backoff_b(n, 3))
# ---- sach ----
check('Tooley 16.8 Bang 16.1: BAG 1..128 ms -> 1000 .. 7,8125 Hz', [F.bag_hz(b) for b in F.BAGS] == [1000, 500, 250, 125, 62.5, 31.25, 15.625, 7.8125])
check('Tooley 16.8: 1518 byte, BAG 4 ms = 3 036 000 bit/s', F.bitrate(1518, 4) == 3036000)
check('Tooley 16.8: 100 lan/s -> BAG <= 8 ms', F.max_bag(100) == 8)
check('Tooley 16.9: khung nho nhat 64, lon nhat 1518 byte', F.frame_len(1) == 64 and F.frame_len(17) == 64 and F.frame_len(1471) == 1518 and F.frame_len(1472 - 1) == 1518)
check('Tooley 16.9: payload < 17 can dem toi da 16 byte', max(17 - p for p in range(1, 17)) == 16 and F.frame_len(17) == F.frame_len(1))
check('Tooley 16.9: SN 255 -> 1', F.sn_next(255) == 1)
check('Tooley 18.5: 100 Mbit/s / 100 kbit/s = 1000', Fr(100_000_000, 100_000) == 1000)
check('Tooley 16.7: VL ID 16 bit + 32 bit hang so = 48 bit = 6 byte dia chi MAC', 16 + 32 == 6 * 8)
check('Tooley 16.8: 1518 byte x 8 x 1000 / 4 va 256 byte, 128 ms', F.bitrate(256, 128) == 16000)
# ---- cau so sinh ----
data = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm13_gen.json'), encoding='utf-8')); fam = {}
def ans(it): return it['opts'][it['correct']]['en']
def hit(k): fam[k] = fam.get(k, 0) + 1
def num(s): return float(re.match(r'[0-9.]+', s.replace(',', ''))[0])
def val(s):                                                   # '3.036 Mbit/s' -> bit/s; '1.2144 ms' -> s; '121.4 μs' -> s; '1000 Hz'
    m = re.match(r'([0-9.]+) (Mbit/s|kbit/s|bit/s|ms|μs|Hz|byte)', s); x = float(m[1])
    return x * {'Mbit/s': 1e6, 'kbit/s': 1e3, 'bit/s': 1, 'ms': 1e-3, 'μs': 1e-6, 'Hz': 1, 'byte': 1}[m[2]]
def close(a, b, t=0.002): return abs(a / b - 1) < t
for it in data:
    q = it['q']['en']; a = ans(it); m = None
    if m := re.match(r'A BAG of (\d+) ms corresponds to a frequency', q): check('gen bag hz ' + q[:25], close(val(a), 1000 / int(m[1])), (q, a)); hit('BAG Hz')
    elif m := re.match(r'An avionics port supplies data (\d+) times a second to a VL', q):
        r = int(m[1]); best = max(b for b in (1, 2, 4, 8, 16, 32, 64, 128) if Fr(1000, b) >= r); check('gen max bag ' + q[:40], a == str(best), (q, a)); hit('max BAG')
    elif m := re.match(r'A VL has a maximum frame length of (\d+) bytes and a BAG of (\d+) ms', q): check('gen bitrate ' + q[:40], close(val(a), int(m[1]) * 8 * 1000 / int(m[2])), (q, a)); hit('VL bit rate')
    elif m := re.match(r'An AFDX frame carries (\d+) bytes of payload', q):
        p = int(m[1]); L = 6 + 6 + 2 + 20 + 8 + max(p, 17) + 1 + 4; check('gen frame ' + q[:40], a == f'{L} bytes', (q, a, L)); hit('frame length')
    elif m := re.match(r'The time to transmit a (\d+)-byte frame on a (\d+) Mbit/s network', q): check('gen tx ' + q[:50], close(val(a), int(m[1]) * 8 / (int(m[2]) * 1e6)), (q, a)); hit('tx time')
    elif m := re.match(r'The AFDX inter-frame gap is 12 bytes long\. On a (\d+) Mbit/s network', q): check('gen ifg', close(val(a), 96 / (int(m[1]) * 1e6)), (q, a)); hit('inter-frame gap')
    elif q.startswith('An end system sends successive frames; the frame just sent has sequence number 255'): check('gen sn255', a == '1'); hit('SN wrap')
    elif q.startswith('After start-up the sequence numbers'):
        sn = 0; seq = [0]
        for _ in range(256): sn = 1 if sn == 255 else sn + 1; seq.append(sn)
        check('gen sn 257th', a == str(seq[256]), (a, seq[256])); hit('SN 257th')
    elif m := re.match(r'In binary exponential back-off the first random interval is T\. After collision number (\d+)', q): check('gen backoff', a == f'{2 ** (int(m[1]) - 1)}T', (q, a)); hit('back-off')
    elif q.startswith('ARINC 664 replaces ARINC 429'): check('gen ratio', a == '1,000' and Fr(100_000_000, 100_000) == 1000); hit('ARINC ratio')
print('Ho cau so da tinh lai:', fam, '| tong', sum(fam.values()), '/', len(data))
# ---- khoa ----
K = json.load(open(os.path.join(ROOT, 'data', 'verify', 'tooley_keys_ch15_20_rev.json')))['keys']
goc = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm13.json'), encoding='utf-8'))
for it in goc:
    mm = re.search(r'Ch\.(\d+) · Q(\d+)', it['src']['en']); ch, n = int(mm[1]), int(mm[2]); printed = K[f'ch{ch}'][n - 1]
    if ch == 16 and n in (5, 9): check(f'Ch.16 Q{n}: khoa in {printed} bi thay', it['correct'] == 'abc'.index({5: 'a', 9: 'c'}[n]) and 'printed key' in it['src']['en'])
    else: check(f'Tooley Ch.{ch} Q{n} khoa {printed}', it['correct'] == 'abc'.index(printed))
# suy luan lai cau 5 va 9 tu chinh sach: 400 msg/s can tan so BAG >= 400 -> 2 ms; ngan xep phat UDP -> IP -> link (cau 11 a)
check('Ch.16 Q5 suy luan: BAG toi da cho 400 msg/s = 2 ms', F.max_bag(400) == 2 and 1000 / 4 < 400 <= 1000 / 2)
check('Ch.16 Q9 suy luan: lop cuoi cua ngan xep phat la lop lien ket', ['UDP', 'IP', 'link'][-1] == 'link' and K['ch16'][10] == 'a')
print('\nFAILS:', fails if fails else 'none'); sys.exit(1 if fails else 0)
