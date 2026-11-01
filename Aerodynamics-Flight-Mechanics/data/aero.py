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

# ---------------- On dinh dong: B747 (Etkin & Reid 3rd, Bang 6.1/6.2, ma tran A pt 6.2,1, tr.165-166) ----------------
B747_A = [[-0.006868, 0.01395, 0.0, -32.2],
          [-0.09055, -0.3151, 773.98, 0.0],
          [0.0001187, -0.001026, -0.4285, 0.0],
          [0.0, 0.0, 1.0, 0.0]]      # state [du (ft/s), w (ft/s), q (rad/s), dtheta (rad)]
B747_U0_FPS = 773.98
G_FPS2 = 32.174

def modes_b747():
    """Tra ve (phugoid, short_period) moi cai = dict(lam, wn, zeta, T, t_half)."""
    import numpy as np
    ev = [e for e in np.linalg.eigvals(np.array(B747_A)) if e.imag > 0]
    out = []
    for e in sorted(ev, key=lambda z: abs(z)):
        wn = abs(e)
        out.append({"lam": e, "wn": wn, "zeta": -e.real / wn, "T": 2 * math.pi / e.imag, "t_half": math.log(2) / -e.real})
    return out  # [phugoid, short period]

def lanchester_period(u0, g=G_FPS2):
    return math.pi * math.sqrt(2) * u0 / g

# ---------------- Dong nen duoc (Anderson ch.7-9) ----------------
R_SI = 287.0
def T0_over_T(M, g=GAMMA): return 1 + (g - 1) / 2 * M * M
def p0_over_p(M, g=GAMMA): return T0_over_T(M, g) ** (g / (g - 1))
def rho0_over_rho(M, g=GAMMA): return T0_over_T(M, g) ** (1 / (g - 1))
def mach_from_p0p(r, g=GAMMA):
    lo, hi = 0.0, 20.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if p0_over_p(mid, g) < r: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def normal_shock_p0(M1, g=GAMMA):
    """p02/p01"""
    r = (g + 1) * M1 ** 2 / ((g - 1) * M1 ** 2 + 2)
    return r ** (g / (g - 1)) * ((g + 1) / (2 * g * M1 ** 2 - (g - 1))) ** (1 / (g - 1))
def mach_from_shock_entropy(ds_over_R):
    """ds/R = -ln(p02/p01) -> M1 (M1>1)"""
    lo, hi = 1.0001, 20.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if -math.log(normal_shock_p0(mid)) < ds_over_R: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def rayleigh_pitot_ratio(M1, g=GAMMA):
    """p02/p1 sau song xung kich thang"""
    return normal_shock_p0(M1, g) * p0_over_p(M1, g)
def mach_from_rayleigh(r, g=GAMMA):
    lo, hi = 1.0001, 30.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if rayleigh_pitot_ratio(mid, g) < r: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def theta_beta_m(M, beta_rad, g=GAMMA):
    return math.atan(2 / math.tan(beta_rad) * (M * M * math.sin(beta_rad) ** 2 - 1) / (M * M * (g + math.cos(2 * beta_rad)) + 2))
def beta_from_theta(M, theta_rad, strong=False, g=GAMMA):
    mu = math.asin(1 / M)
    # theta(beta) tang tu 0 (beta=mu) den cuc dai roi giam ve 0 (beta=90)
    bs = [mu + (math.pi / 2 - mu) * i / 20000 for i in range(1, 20000)]
    ths = [theta_beta_m(M, b, g) for b in bs]
    imax = max(range(len(ths)), key=lambda i: ths[i])
    if theta_rad > ths[imax]: return None
    rng = range(0, imax) if not strong else range(imax, len(bs) - 1)
    lo, hi = (bs[0], bs[imax]) if not strong else (bs[imax], bs[-1])
    for _ in range(100):
        mid = (lo + hi) / 2
        f = theta_beta_m(M, mid, g) - theta_rad
        if (not strong and f < 0) or (strong and f > 0): lo = mid
        else: hi = mid
    return (lo + hi) / 2
def oblique(M1, beta_rad, theta_rad=None, g=GAMMA):
    Mn1 = M1 * math.sin(beta_rad)
    M2n, p, rho, T = normal_shock(Mn1, g)
    th = theta_beta_m(M1, beta_rad, g) if theta_rad is None else theta_rad
    M2 = M2n / math.sin(beta_rad - th)
    return {"Mn1": Mn1, "M2": M2, "p": p, "rho": rho, "T": T, "p0": normal_shock_p0(Mn1, g), "theta": th}
def prandtl_meyer(M, g=GAMMA):
    a = math.sqrt((g + 1) / (g - 1))
    return a * math.atan(math.sqrt((M * M - 1) / a ** 2)) - math.atan(math.sqrt(M * M - 1))
def mach_from_pm(nu, g=GAMMA):
    lo, hi = 1.0, 60.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if prandtl_meyer(mid, g) < nu: lo = mid
        else: hi = mid
    return (lo + hi) / 2

# ---------------- Dong luc bay ngang B747 (Etkin & Reid 3rd, tr.187, state [v, p, r, phi]) ----------------
B747_LAT = [[-0.0558, 0.0, -774.0, 32.2], [-0.003865, -0.4342, 0.4136, 0.0], [0.001086, -0.006112, -0.1458, 0.0], [0.0, 1.0, 0.0, 0.0]]
def modes_b747_lat():
    import numpy as np
    ev = np.linalg.eigvals(np.array(B747_LAT))
    real = sorted([e.real for e in ev if abs(e.imag) < 1e-9])      # [roll convergence, spiral]
    dr = [e for e in ev if e.imag > 1e-9][0]
    return {"roll": real[0], "spiral": real[1], "dr": dr}
