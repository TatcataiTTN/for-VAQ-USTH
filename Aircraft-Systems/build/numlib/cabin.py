# -*- coding: utf-8 -*-
"""Cong cu tinh cho module 15 (cabin va thong tin tau bay). Moi ham co hai cai dat doc lap (_a, _b); build/verify/verify_m15.py doi chieu."""
from fractions import Fraction as Fr
def cycles_a(f_hz, t_s): return f_hz * t_s
def cycles_b(f_hz, t_s): return float(Fr(str(f_hz)) * Fr(str(t_s)))
cycles = cycles_a
def period_a(f_hz): return 1 / f_hz
def period_b(f_hz): return float(Fr(1) / Fr(str(f_hz)))
period = period_a
def load_time_a(size_gb, rate_bps): return size_gb * 8e9 / rate_bps            # giay; 1 GB = 10^9 byte (gia dinh cua site)
def load_time_b(size_gb, rate_bps): return float(Fr(str(size_gb)) * 8 * 10 ** 9 / Fr(str(rate_bps)))
load_time = load_time_a
def ratio_a(f1, f2): return f2 / f1
def ratio_b(f1, f2): return float(Fr(str(f2)) / Fr(str(f1)))
ratio = ratio_a
PA_LEVELS = ['Flight deck announcements', 'Forward attendant panel', 'Rear/other attendant panels', 'Pre-recorded announcements', 'Boarding music and IFE']    # muc 1 den 5 (Tooley 19.3.2)
