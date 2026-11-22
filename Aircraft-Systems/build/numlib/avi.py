# -*- coding: utf-8 -*-
"""Cong cu tinh cho module 12 (avionics so). Moi ham co hai cach doc lap (_a, _b); build/verify/verify_m12.py doi chieu."""
import math
from fractions import Fraction as Fr
MU = 3.986004418e14; R_EARTH = 6371e3; T_MOON = 27.321661 * 86400; R_MOON = 384400e3        # hang so vat ly chuan (khong lay tu Tooley): doi chieu rieng
def nm_to_km_a(nm): return nm * 1.852
def nm_to_km_b(nm): return float(Fr(nm) * 1852 / 1000)
nm_to_km = nm_to_km_a
def km_to_nm_a(km): return km / 1.852
def km_to_nm_b(km): return float(Fr(km) * 1000 / 1852)
km_to_nm = km_to_nm_a
def orbit_period_a(alt_km):                                   # dinh luat Kepler 3 voi hang so hap dan
    r = R_EARTH + alt_km * 1e3; return 2 * math.pi * math.sqrt(r ** 3 / MU)
def orbit_period_b(alt_km):                                   # ti le theo quy dao Mat Trang (T ~ r^1,5), khong dung MU
    r = R_EARTH + alt_km * 1e3; return T_MOON * (r / R_MOON) ** 1.5
orbit_period = orbit_period_a
def tau_a(dist_nm, closure_kt): return dist_nm / closure_kt * 3600            # giay: thoi gian toi diem gan nhat = khoang cach / toc do tiep can
def tau_b(dist_nm, closure_kt): return float(Fr(dist_nm) / Fr(closure_kt) * 3600)
tau = tau_a
def chips_a(f_hz, t_s): return round(f_hz * t_s)
def chips_b(f_hz, t_s): return int(Fr(str(f_hz)) * Fr(str(t_s)))
chips = chips_a
def cycles_a(days_per_cycle, year=365): return year // days_per_cycle
def cycles_b(days_per_cycle, year=365):
    n = 0; d = 0
    while d + days_per_cycle <= year: d += days_per_cycle; n += 1
    return n
cycles = cycles_a
def speed_a(acc, t): return acc * t
def speed_b(acc, t, steps=100000):                            # tich phan so (tong hinh chu nhat)
    dt = t / steps; v = 0.0
    for _ in range(steps): v += acc * dt
    return v
speed = speed_a
def dist_a(acc, t): return 0.5 * acc * t * t
def dist_b(acc, t, steps=20000):
    dt = t / steps; v = 0.0; s = 0.0
    for _ in range(steps): s += v * dt + 0.5 * acc * dt * dt; v += acc * dt
    return s
dist = dist_a
