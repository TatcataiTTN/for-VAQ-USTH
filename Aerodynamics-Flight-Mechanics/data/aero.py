# -*- coding: utf-8 -*-
"""Cac ham vat ly dung chung: khi quyen chuan ISA, dong chay khong nen, dong nen duoc.
Moi dap an hien tren trang deu chay ra tu day (khong go tay)."""
import math

G0 = 9.80665
R_AIR = 287.05287      # J/(kg K), ISA
R_ANDERSON = 287.0     # Anderson dung R = 287 J/(kg K)
GAMMA = 1.4
P0 = 101325.0
T0 = 288.15
RHO0 = 1.225

def isa(h_m):
    """ISA 0..20 km: (T K, p Pa, rho kg/m3). Tang doi luu 0-11 km (L=-6.5 K/km), dang nhiet 11-20 km."""
    if h_m <= 11000.0:
        L = -0.0065
        T = T0 + L * h_m
        p = P0 * (T / T0) ** (-G0 / (L * R_AIR))
    elif h_m <= 20000.0:
        T = 216.65
        p11 = P0 * (216.65 / T0) ** (-G0 / (-0.0065 * R_AIR))
        p = p11 * math.exp(-G0 * (h_m - 11000.0) / (R_AIR * T))
    else:
        raise ValueError("chi dung den 20 km")
    return T, p, p / (R_AIR * T)

FT = 0.3048
PSI = 6894.757
def isa_ft(h_ft):
    T, p, rho = isa(h_ft * FT)
    return T, p, rho

def speed_of_sound(T, R=R_AIR, g=GAMMA):
    return math.sqrt(g * R * T)

def pitot_ratio_subsonic(M, g=GAMMA):
    return (1 + (g - 1) / 2 * M * M) ** (g / (g - 1))

def mach_from_pitot_ratio(r, g=GAMMA):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if pitot_ratio_subsonic(mid, g) < r: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def normal_shock(M1, g=GAMMA):
    M2 = math.sqrt(((g - 1) * M1**2 + 2) / (2 * g * M1**2 - (g - 1)))
    p = 1 + 2 * g / (g + 1) * (M1**2 - 1)
    rho = (g + 1) * M1**2 / ((g - 1) * M1**2 + 2)
    T = p / rho
    return M2, p, rho, T

def cp_crit(M, g=GAMMA):
    return 2 / (g * M * M) * (((1 + (g - 1) / 2 * M * M) / ((g + 1) / 2)) ** (g / (g - 1)) - 1)

def mcr_prandtl_glauert(cp0, g=GAMMA):
    """M_cr: Cp0/sqrt(1-M^2) = Cp_crit(M)."""
    lo, hi = 0.3, 0.99
    f = lambda M: cp0 / math.sqrt(1 - M * M) - cp_crit(M, g)
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2
