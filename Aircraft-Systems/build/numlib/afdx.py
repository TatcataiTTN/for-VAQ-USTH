# -*- coding: utf-8 -*-
"""Cong cu tinh cho module 13 (mang AFDX, IMA). Moi ham co hai cai dat doc lap (_a, _b); build/verify/verify_m13.py doi chieu. Cau truc khung theo Tooley 16.9 (Hinh 16.7)."""
from fractions import Fraction as Fr
BAGS = [1, 2, 4, 8, 16, 32, 64, 128]
def bag_hz_a(bag): return 1000 / bag
def bag_hz_b(bag): return float(Fr(1000, 1) / Fr(bag))
bag_hz = bag_hz_a
def max_bag_a(rate):                                       # BAG lon nhat (ms) sao cho tan so BAG >= toc do thong diep
    return max(b for b in BAGS if 1000 / b >= rate)
def max_bag_b(rate):
    for b in reversed(BAGS):
        if Fr(1000, b) >= Fr(str(rate)): return b
    raise ValueError(rate)
max_bag = max_bag_a
def bitrate_a(l_max, bag): return l_max * 8 * 1000 / bag        # bit/s (Tooley 16.8)
def bitrate_b(l_max, bag): return float(Fr(l_max * 8) / Fr(bag, 1000))
bitrate = bitrate_a
HEADER = 6 + 6 + 2 + 20 + 8                                 # dia chi MAC dich + nguon, Type, IP, UDP
def frame_len_a(payload): return HEADER + max(payload, 17) + 1 + 4         # payload + SN (1) + FCS (4); padding neu payload < 17
def frame_len_b(payload):
    pad = max(0, 17 - payload); return 6 + 6 + 2 + 20 + 8 + payload + pad + 1 + 4
frame_len = frame_len_a
def tx_time_a(nbytes, rate): return nbytes * 8 / rate
def tx_time_b(nbytes, rate): return float(Fr(nbytes * 8) / Fr(rate))
tx_time = tx_time_a
IFG_BYTES = 12
def ifg_a(rate): return IFG_BYTES * 8 / rate
def ifg_b(rate): return float(Fr(96) / Fr(rate))
ifg = ifg_a
def sn_next_a(sn): return 1 if sn == 255 else sn + 1
def sn_next_b(sn): return sn % 255 + 1 if sn >= 1 else 1
sn_next = sn_next_a
def backoff_a(n, t): return 2 ** (n - 1) * t               # khoang ngau nhien sau lan va cham thu n: gap doi moi lan
def backoff_b(n, t):
    x = t
    for _ in range(n - 1): x *= 2
    return x
backoff = backoff_a
