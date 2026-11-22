# -*- coding: utf-8 -*-
"""Cong cu tinh cho module 11 (mach tuan tu). MOI ham co hai cach cai dat doc lap (hau to _a va _b); build/verify/verify_m11.py doi chieu hai cach tren nhieu bo thu.
Ham khong hau to la cach duoc dung de sinh cau hoi (chinh la cach _a)."""
import math
from fractions import Fraction

# ---- chot S-R: _a mo phong cong NOR/NAND lap cho den khi on dinh; _b tra bang chan tri
def sr_nor_a(S, R, Q, Qb):
    for _ in range(10):
        q2 = int(not (R or Qb)); qb2 = int(not (S or q2))
        if (q2, qb2) == (Q, Qb): break
        Q, Qb = q2, qb2
    return Q, Qb
def sr_nor_b(S, R, Q, Qb):
    return {(0, 0): (Q, Qb), (1, 0): (1, 0), (0, 1): (0, 1), (1, 1): (0, 0)}[(S, R)]
sr_nor = sr_nor_a
def sr_nand_a(Sn, Rn, Q, Qb):
    for _ in range(10):
        q2 = int(not (Sn and Qb)); qb2 = int(not (Rn and q2))
        if (q2, qb2) == (Q, Qb): break
        Q, Qb = q2, qb2
    return Q, Qb
def sr_nand_b(Sn, Rn, Q, Qb):
    return {(1, 1): (Q, Qb), (0, 1): (1, 0), (1, 0): (0, 1), (0, 0): (1, 1)}[(Sn, Rn)]
sr_nand = sr_nand_a

# ---- flip-flop JK, D, T: _a bang dac trung, _b phuong trinh dac trung
def jk_a(J, K, Q): return {(0, 0): Q, (0, 1): 0, (1, 0): 1, (1, 1): 1 - Q}[(J, K)]
def jk_b(J, K, Q): return int((J and not Q) or ((not K) and Q))
jk = jk_a
def t_ff_a(T, Q): return 1 - Q if T else Q
def t_ff_b(T, Q): return Q ^ T
t_ff = t_ff_a

# ---- bo dem khong dong bo (ripple): _a mo phong tung FF lat o suon xuong cua Q truoc; _b so hoc modulo
def ripple_a(n, pulses, start=0):
    q = [(start >> i) & 1 for i in range(n)]
    for _ in range(pulses):
        i = 0
        while i < n:
            q[i] ^= 1
            if q[i] == 1: break          # Q vua len 1 (suon len): FF ke tiep khong lat
            i += 1                       # Q vua xuong 0 (suon xuong): FF ke tiep lat
    return sum(b << i for i, b in enumerate(q))
def ripple_b(n, pulses, start=0): return (start + pulses) % (1 << n)
ripple = ripple_a
def ripple_delay_a(n, tpd): return sum(tpd for _ in range(n))
def ripple_delay_b(n, tpd): return n * tpd
ripple_delay = ripple_delay_b
def ffs_for_mod_a(N):
    n = 0
    while (1 << n) < N: n += 1
    return n
def ffs_for_mod_b(N): return math.ceil(math.log2(N)) if N > 1 else 0
ffs_for_mod = ffs_for_mod_a

# ---- bo dem BCD/cat cut: dem len, ve 0 khi dat modulo N (Floyd: bo dem cat cut co it trang thai hon toi da)
def mod_n_a(N, pulses, start=0):
    s = start
    for _ in range(pulses): s = 0 if s == N - 1 else s + 1
    return s
def mod_n_b(N, pulses, start=0): return (start + pulses) % N
mod_n = mod_n_a
def down_a(n, pulses, start):
    s = start
    for _ in range(pulses): s = (1 << n) - 1 if s == 0 else s - 1
    return s
def down_b(n, pulses, start): return (start - pulses) % (1 << n)
down = down_a
def cascade_mod_a(ms):
    p = 1
    for m in ms: p *= m
    return p
def cascade_mod_b(ms): return math.prod(ms)
cascade_mod = cascade_mod_a
def freq_div_a(f, ms): return Fraction(f) / cascade_mod_a(ms)
def freq_div_b(f, ms): return Fraction(f) / math.prod(ms)
freq_div = freq_div_a

# ---- thanh ghi dich: _a thao tac tren list, _b thao tac tren chuoi
def shift_right_a(reg, bits, serial_first):
    """reg: chuoi bit (trai = MSB). Vao noi tiep tai dau trai, dich phai; 'serial_first' = bit nao cua `bits` vao truoc ('right' = bit ngoai cung ben phai)."""
    r = list(reg); seq = list(bits)[::-1] if serial_first == 'right' else list(bits)
    for b in seq: r = [b] + r[:-1]
    return ''.join(r)
def shift_right_b(reg, bits, serial_first):
    seq = bits[::-1] if serial_first == 'right' else bits; s = reg
    for b in seq: s = b + s[:-1]
    return s
shift_right = shift_right_a
def ring_a(n, k):
    r = [1] + [0] * (n - 1)
    for _ in range(k): r = [r[-1]] + r[:-1]
    return ''.join(map(str, r))
def ring_b(n, k): s = '1' + '0' * (n - 1); k %= n; return s[-k:] + s[:-k] if k else s
ring = ring_a
def johnson_a(n, k):
    r = [0] * n
    for _ in range(k): r = [1 - r[-1]] + r[:-1]
    return ''.join(map(str, r))
def johnson_b(n, k):
    k %= 2 * n
    return '1' * k + '0' * (n - k) if k <= n else '0' * (k - n) + '1' * (2 * n - k)
johnson = johnson_a
def serial_time_a(nbits, f): return Fraction(nbits) / Fraction(f)
def serial_time_b(nbits, f): return Fraction(nbits, 1) * (1 / Fraction(f))
serial_time = serial_time_a
def delay_clock_a(nbits, t): return Fraction(nbits) / Fraction(t)
def delay_clock_b(nbits, t): return 1 / (Fraction(t) / nbits)
delay_clock = delay_clock_a

# ---- 555 va mach mot nhip: _a dung cong thuc Floyd (7-5, 7-6); _b suy tu thoi gian nap/xa cua tu
def one_shot_a(R, C): return 0.7 * R * C                       # 74121 (Floyd 7-5): tW = 0.7 R C
def one_shot_b(R, C): return math.log(2) * R * C               # ln 2 = 0,693: cach suy ra
one_shot = one_shot_a
def t555_mono_a(R, C): return 1.1 * R * C
def t555_mono_b(R, C): return -math.log(1 - 2 / 3) * R * C     # tu nap tu 0 den 2/3 Vcc
t555_mono = t555_mono_a
def t555_astable_a(R1, R2, C):
    th = 0.7 * (R1 + R2) * C; tl = 0.7 * R2 * C; T = th + tl
    return dict(tH=th, tL=tl, T=T, f=1 / T, duty=th / T)
def t555_astable_b(R1, R2, C):
    th = math.log(2) * (R1 + R2) * C; tl = math.log(2) * R2 * C            # nap tu 1/3 den 2/3 Vcc qua R1+R2, xa qua R2
    T = th + tl
    return dict(tH=th, tL=tl, T=T, f=1.44 / ((R1 + 2 * R2) * C), duty=(R1 + R2) / (R1 + 2 * R2))
t555_astable = t555_astable_a
