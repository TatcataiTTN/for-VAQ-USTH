"""verify_m02: recompute EVERY numeric answer of module m02 (gas power cycles) by ROUTE B and compare with the stored route-A values (data/verify/m02_values.json, written by build/gen/gen_m02.py), then compare with the
answers PRINTED in the lecturer's slides and in the books.
Route A  = closed forms (constant k) and linear interpolation of Table A-17 / A-17E, as a student does.
Route B  = independent re-implementations:
  constant specific heats  -> numerical integration of P dV and v dP (scipy quad), ODE integration of the isentropes (scipy solve_ivp), root finding (brentq), sympy for the algebraic identities;
  variable specific heats  -> integration of cp(T) from the A-2c cubic polynomial (props.cp_poly) AND from CoolProp's ideal-gas Cp0 of Air (two different property models); h = int cp dT, s-relation int cp/T dT = R ln(P2/P1),
                              isentropic volume relation int cv/T dT = -R ln(v2/v1). Both must agree with Table A-17 inside the stated tolerance.
Route C (extra) = _shared/thermo.js run with node (the Lab page code) for the constant-k Otto, Diesel, Brayton and multistage entries.
Tolerances are explicit (see TOL below); none was tuned to hide a gap: the observed maxima are printed.
Run:  .venv/bin/python -I build/verify/verify_m02.py     (needs the project venv: CoolProp, scipy, sympy, props)"""
import json, math, os, subprocess, sys, collections
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar
import CoolProp.CoolProp as CP
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'props')); sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
import props
V = json.load(open(os.path.join(ROOT, 'data', 'verify', 'm02_values.json'), encoding='utf-8'))
R = 0.287; M_AIR = 28.97
FAILS = []; ROWS = []; DEV = collections.defaultdict(float); NPAIR = collections.Counter()
BTU = 4.1868 / 1.8 * 1.0          # 1 Btu/lbm = 2.326 kJ/kg  (= 4.1868 kJ/kg/K x 5/9 K per R)
# explicit tolerances for route B vs route A (relative unless a key says abs)
TOL_CONSTK = 3e-3      # works from  oint P dV  use R and k = 1.4, heats use c_v = 0.718 and c_p = 1.005: R/(k-1) = 0.7175, R k/(k-1) = 1.0045 (0.07 % and 0.05 % rounding of the book's constants)
TOL_TEMP = 1e-6        # temperatures from isentropic relations with the same k: must agree to numerical accuracy

def rec(name, a, b, tol, rel=True, note=''):
    err = abs(a - b) / max(abs(a), abs(b), 1e-300) if rel else abs(a - b)
    ok = err <= tol; ROWS.append((name, a, b, err, tol, 'ok' if ok else 'FAIL')); DEV[name.split(' ')[0]] = max(DEV[name.split(' ')[0]], err)
    if not ok: FAILS.append(f'{name}: A={a:.8g} B={b:.8g} err={err:.3g} > {tol} {note}')

# ---------------------------------------------------------------- property models for variable specific heats (SI, kJ/kg K)
class Gas:
    def __init__(self, kind):
        self.kind = kind
        if kind == 'poly':
            T = np.arange(273.0, 1800.01, 5.0); cp = np.array([props.cp_poly('Air', float(t), mass_basis=True)['value'] for t in T])
        else:
            T = np.arange(250.0, 2100.01, 5.0); cp = np.array([CP.PropsSI('Cp0mass', 'T', float(t), 'P', 1e5, 'Air') / 1000.0 for t in T])
        self.T0, self.T1 = T[0], T[-1]
        self.H = CubicSpline(T, cp).antiderivative(); self.S = CubicSpline(T, cp / T).antiderivative(); self.cp = CubicSpline(T, cp)
    def h(self, a, b): return float(self.H(b) - self.H(a))                       # int_a^b cp dT
    def phi(self, a, b): return float(self.S(b) - self.S(a))                     # int_a^b cp/T dT
    def cv_phi(self, a, b): return self.phi(a, b) - R * math.log(b / a)           # int cv/T dT
    def cv_h(self, a, b): return self.h(a, b) - R * (b - a)                       # int cv dT = delta u
    def T_after_dh(self, a, dh): return brentq(lambda T: self.h(a, T) - dh, a * 0.3 if dh < 0 else a, 1799.0 if self.kind == 'poly' else 2090.0) if dh >= 0 else brentq(lambda T: self.h(a, T) - dh, 275.0, a)
    def T_isen_P(self, a, lnr):                                                    # phi(a,T) = R ln(Pratio)
        return brentq(lambda T: self.phi(a, T) - R * lnr, 275.0, 1799.0) if lnr >= 0 else brentq(lambda T: self.phi(a, T) - R * lnr, 275.0, a)
    def T_isen_v(self, a, lnr):                                                    # v2/v1 = 1/r : int cv/T dT = R ln r  (compression), negative for expansion
        return brentq(lambda T: self.cv_phi(a, T) - R * lnr, 275.0, 1799.0) if lnr >= 0 else brentq(lambda T: self.cv_phi(a, T) - R * lnr, 275.0, a)
GASES = {}
def gas(kind):
    if kind not in GASES: GASES[kind] = Gas(kind)
    return GASES[kind]

def tK(T, E): return T * 5.0 / 9.0 if E else T
def tBack(T, E): return T * 9.0 / 5.0 if E else T
def eK(x, E): return x * BTU if E else x            # energy per mass to kJ/kg
def eBack(x, E): return x / BTU if E else x

# ---------------------------------------------------------------- route B for the variable-cp models (g = Gas)
def B_otto_v(g, p):
    E = p.get('E', False); T1 = tK(p['T1'], E); r = p['r']
    T2 = g.T_isen_v(T1, math.log(r))
    if 'qin' in p: T3 = g.T_after_dh(T2, 0) if False else brentq(lambda T: g.cv_h(T2, T) - eK(p['qin'], E), T2, 1799.0)
    else: T3 = tK(p['T3'], E)
    qin = g.cv_h(T2, T3); T4 = brentq(lambda T: g.cv_phi(T, T3) - R * math.log(r), 275.0, T3)
    qout = g.cv_h(T1, T4); w = qin - qout; out = dict(T2=tBack(T2, E), T3=tBack(T3, E), T4=tBack(T4, E), qin=eBack(qin, E), qout=eBack(qout, E), wnet=eBack(w, E), eta=w / qin)
    if p.get('P1') is not None:
        v1 = R * T1 / p['P1']; out.update(P3=p['P1'] * r * T3 / T1, mep=w / (v1 * (1 - 1 / r)))
    return out
def B_diesel_v(g, p):
    E = p.get('E', False); T1 = tK(p['T1'], E); r = p['r']; T2 = g.T_isen_v(T1, math.log(r))
    T3 = p['rc'] * T2 if 'rc' in p else tK(p['T3'], E); rc = T3 / T2
    qin = g.h(T2, T3); T4 = brentq(lambda T: g.cv_phi(T, T3) - R * math.log(r / rc), 275.0, T3); qout = g.cv_h(T1, T4); w = qin - qout
    out = dict(T2=tBack(T2, E), T3=tBack(T3, E), T4=tBack(T4, E), qin=eBack(qin, E), qout=eBack(qout, E), wnet=eBack(w, E), eta=w / qin, rc=rc)
    if p.get('P1') is not None: v1 = R * T1 / p['P1']; out['mep'] = w / (v1 * (1 - 1 / r))
    return out
def B_brayton_v(g, p):
    E = p.get('E', False); T1 = tK(p['T1'], E); rp = p['rp']; ec, et, eps = p.get('etac', 1.0), p.get('etat', 1.0), p.get('eps', 0.0)
    T2s = g.T_isen_P(T1, math.log(rp)); wc = g.h(T1, T2s) / ec
    if 'T2_given' in p: T2 = tK(p['T2_given'], E); wc = g.h(T1, T2)
    else: T2 = brentq(lambda T: g.h(T1, T) - wc, T1, 1799.0)
    if 'qin23' in p: T3 = brentq(lambda T: g.h(T2, T) - eK(p['qin23'], E), T2, 1799.0)
    else: T3 = tK(p['T3'], E)
    T4s = g.T_isen_P(T3, -math.log(rp)); wt = et * g.h(T4s, T3); T4 = brentq(lambda T: g.h(T, T3) - wt, 275.0, T3)
    dq_reg = eps * g.h(T2, T4); T5 = brentq(lambda T: g.h(T2, T) - dq_reg, T2, 1799.0) if eps > 0 else T2
    qin = g.h(T5, T3); w = wt - wc
    return dict(T2=tBack(T2, E), T3=tBack(T3, E), T4=tBack(T4, E), wc=eBack(wc, E), wt=eBack(wt, E), wnet=eBack(w, E), qin=eBack(qin, E), qout=eBack(qin - w, E), bwr=wc / wt, eta=w / qin, qreg=eBack(dq_reg, E))
def B_multi_v(g, p):
    T1, T3, rp, N, eps = p['T1'], p['T3'], p['rp'], p['N'], p.get('eps', 0.0); lx = math.log(rp) / N
    T2 = g.T_isen_P(T1, lx); T7 = g.T_isen_P(T3, -lx); wc = N * g.h(T1, T2); wt = N * g.h(T7, T3)
    dq = eps * g.h(T2, T7); T5 = brentq(lambda T: g.h(T2, T) - dq, T2, 1799.0) if eps > 0 else T2
    qin = g.h(T5, T3) + (N - 1) * g.h(T7, T3); w = wt - wc
    return dict(T2=T2, T7=T7, wc=wc, wt=wt, wnet=w, bwr=wc / wt, qin=qin, eta=w / qin, mdot110=110e3 / w)
def B_carnot_v(g, p):
    TL, TH, P1, P2 = p['TL'], p['TH'], p['P1'], p['P2']; ds = R * math.log(P2 / P1); lnPr = g.phi(TL, TH) / R
    Pmax = P2 * math.exp(lnPr); wnet = (TH - TL) * ds; m = p['Wnet'] / wnet
    return dict(Pmax=Pmax, qin=TH * ds, wnet=wnet, Qin=m * TH * ds, m=m)
def B_c984(g, p):
    T1 = p['T1']; rp = p['rp']; T2s = g.T_isen_P(T1, math.log(rp)); wc = g.h(T1, T2s) / p['etac']; T2 = brentq(lambda T: g.h(T1, T) - wc, T1, 1799.0); T4a = p['T4a']
    def f(T3):
        T4s = g.T_isen_P(T3, -math.log(rp)); return g.h(T4a, T3) - p['etat'] * g.h(T4s, T3)
    T3 = brentq(f, 800.0, 1700.0); wt = g.h(T4a, T3); mdot = p['P1'] / (R * T1) * p['V1_m3min'] / 60; w = wt - wc
    return dict(T3=T3, wc=wc, wt=wt, P=mdot * w, bwr=wc / wt, eta=w / g.h(T2, T3))
def B_jet_static(g, p):
    T1, rp, P1, m, mf, HV = p['T1'], p['rp'], p['P1'], p['m'], p['mf'], p['HV']; q = mf * HV / m
    T2 = g.T_isen_P(T1, math.log(rp)); wc = g.h(T1, T2); T3 = brentq(lambda T: g.h(T2, T) - q, T2, 1799.0); T4 = brentq(lambda T: g.h(T, T3) - wc, 275.0, T3)
    lnP4 = math.log(rp * P1) - g.phi(T4, T3) / R; T5 = g.T_isen_P(T4, -(lnP4 - math.log(P1))); Vx = math.sqrt(2000 * g.h(T5, T4))
    return dict(T3=T3, T4=T4, T5=T5, V=Vx, F=m * Vx)
def B_table_Pr(g, p): return dict(T2s=g.T_isen_P(p['T1'], math.log(p['rp'])))
VAR = dict(otto_v=B_otto_v, diesel_v=B_diesel_v, brayton_v=B_brayton_v, multi_v=B_multi_v, carnot_v=B_carnot_v, c984=B_c984, jet_static=B_jet_static, table_Pr=B_table_Pr)
# tolerance for the variable-cp family: Table A-17 versus (A-2c polynomial, CoolProp Cp0): P3.. and sensitive quantities get their own explicit value
TOLV = dict(default=0.012, Pmax=0.03)      # Pmax of the Carnot problem: ln(Pr) = int cp/T dT / R; 0.5 % of the integral (1.4) is 0.024 in ln P => 2.4 % in P

# ---------------------------------------------------------------- route B for the constant-k models
def adiabat_T(T1, v1, v2, expo):                    # integrate dT/dv = -expo T / v numerically
    s = solve_ivp(lambda v, T: -expo * T / v, (v1, v2), [T1], rtol=1e-12, atol=1e-10, dense_output=True); return s
def B_otto_k(p):
    r, T1, P1, k, Rg, cv = p['r'], p['T1'], p['P1'], p['k'], p['R'], p['cv']; v1 = Rg * T1 / P1; v2 = v1 / r
    s12 = adiabat_T(T1, v1, v2, k - 1); T2 = float(s12.y[0, -1])
    w12 = quad(lambda v: Rg * float(s12.sol(v)[0]) / v, v1, v2)[0]
    if 'qin' in p: T3 = T2 + p['qin'] / cv
    elif 'T3' in p: T3 = p['T3']
    else: T3 = brentq(lambda T3_: float(adiabat_T(T3_, v2, v1, k - 1).y[0, -1]) - p['T4'], 300.0, 6000.0)
    s34 = adiabat_T(T3, v2, v1, k - 1); T4 = float(s34.y[0, -1]); w34 = quad(lambda v: Rg * float(s34.sol(v)[0]) / v, v2, v1)[0]
    qin = cv * (T3 - T2); qout = cv * (T4 - T1); w = w12 + w34
    return dict(T2=T2, T3=T3, T4=T4, P3=Rg * T3 / v2, qin=qin, qout=qout, wnet=w, eta=w / qin, mep=w / (v1 - v2))
def B_diesel_k(p):
    r, T1, P1, k, Rg, cp, cv = p['r'], p['T1'], p['P1'], p['k'], p['R'], p['cp'], p['cv']; v1 = Rg * T1 / P1; v2 = v1 / r
    s12 = adiabat_T(T1, v1, v2, k - 1); T2 = float(s12.y[0, -1]); P2 = Rg * T2 / v2; w12 = quad(lambda v: Rg * float(s12.sol(v)[0]) / v, v1, v2)[0]
    if 'rc' in p: T3 = p['rc'] * T2
    elif 'T3' in p: T3 = p['T3']
    else: T3 = T2 + p['qin'] / cp
    v3 = Rg * T3 / P2; w23 = P2 * (v3 - v2); s34 = adiabat_T(T3, v3, v1, k - 1); T4 = float(s34.y[0, -1]); w34 = quad(lambda v: Rg * float(s34.sol(v)[0]) / v, v3, v1)[0]
    qin = cp * (T3 - T2); qout = cv * (T4 - T1); w = w12 + w23 + w34
    return dict(T2=T2, T3=T3, T4=T4, P2=P2, rc=v3 / v2, qin=qin, qout=qout, wnet=w, eta=w / qin, mep=w / (v1 - v2))
def B_brayton_k(p):
    rp, T1, T3, k, cp = p['rp'], p['T1'], p['T3'], p['k'], p['cp']; ec, et, eps = p['etac'], p['etat'], p['eps']; Rg = cp * (k - 1) / k; P1 = 100.0
    Tc = lambda P: T1 * (P / P1) ** ((k - 1) / k); wcs = quad(lambda P: Rg * Tc(P) / P, P1, rp * P1)[0]
    Tt = lambda P: T3 * (P / (rp * P1)) ** ((k - 1) / k); wts = quad(lambda P: Rg * Tt(P) / P, rp * P1, P1)[0] * -1
    wc, wt = wcs / ec, et * wts; T2 = T1 + wc / cp; T4 = T3 - wt / cp; T5 = T2 + eps * (T4 - T2); qin = cp * (T3 - T5); w = wt - wc
    return dict(T2=T2, T4=T4, T5=T5, wc=wc, wt=wt, wnet=w, qin=qin, bwr=wc / wt, eta=w / qin)
def B_multi_k(p):
    rp, N, T1, T3, k, cp, ec, et, eps = p['rp'], p['N'], p['T1'], p['T3'], p['k'], p['cp'], p['etac'], p['etat'], p['eps']; Rg = cp * (k - 1) / k
    lx = math.log(rp) / N; P1 = 100.0; Px = P1 * math.exp(lx)
    wcs = quad(lambda P: Rg * T1 * (P / P1) ** ((k - 1) / k) / P, P1, Px)[0]; wts = quad(lambda P: Rg * T3 * (P / Px) ** ((k - 1) / k) / P, Px, P1)[0] * -1
    wc, wt = N * wcs / ec, N * et * wts; Tc = T1 + wcs / ec / cp; Tt = T3 - et * wts / cp; T5 = Tc + eps * (Tt - Tc); qin = cp * (T3 - T5) + (N - 1) * cp * (T3 - Tt); w = wt - wc
    return dict(wc=wc, wt=wt, bwr=wc / wt, eta=w / qin, T2=Tc, T4=Tt, T5=T5, wnet=w)
def B_c916(p):
    P1, T1, P2, q = p['P1'], p['T1'], p['P2'], p['q23']; k, cp, cv = 1.4, 1.005, 0.718; v1 = R * T1 / P1; T2 = T1 * (P2 / P1) ** ((k - 1) / k); v2 = R * T2 / P2
    T3 = T2 + q / cp; v3 = R * T3 / P2; w12 = quad(lambda v: P1 * (v1 / v) ** k, v1, v2)[0]; w23 = P2 * (v3 - v2); T4 = T3 * P1 / P2; v4 = v3; w41 = P1 * (v1 - v4)
    return dict(T3=T3, eta=(w12 + w23 + w41) / q)
def B_c919(p):
    T1, P1, P2, m, Q23 = p['T1'], p['P1'], p['P2'], p['m'], p['Q23']; k, cp, cv = 1.4, 1.005, 0.718; v1 = R * T1 / P1; T2 = T1 * (P2 / P1) ** ((k - 1) / k); v2 = R * T2 / P2
    q = Q23 / m; T3 = T2 + q / cp; v3 = R * T3 / P2; w12 = quad(lambda v: P1 * (v1 / v) ** k, v1, v2)[0]; w23 = P2 * (v3 - v2)
    line = lambda v: P2 + (P1 - P2) * (v - v3) / (v1 - v3); w31 = quad(line, v3, v1)[0]; Qout = m * (cp * 0 + w31 - (cv * (T3 - T1)))      # Q31 = dU + W  (heat rejected = -(that))
    Qout = -m * (cv * (T1 - T3) + w31)
    return dict(Qout=Qout, eta=(w12 + w23 + w31) / q)
def B_c959(p):
    AF = p['AF']; k, cp, cv, r = 1.349, 1.110, 0.823, 17; Vd = 4.5e-3 / 6; V1 = Vd * r / (r - 1); m = 95 * V1 / (R * 328)
    d = B_diesel_k(dict(r=r, T1=328.0, P1=95.0, k=k, R=R, cp=cp, cv=cv, qin=0.98 * 42500 / AF)); W = m * d['wnet']; P = W * 6 * 2000 / 60 / 2
    return dict(T3=d['T3'], rc=d['rc'], eta=d['eta'], Wcycle6=6 * W, mep=W / Vd, P=P, sfc=(m / AF * 6) * (2000 / 60 / 2) / P * 3600 * 1000)
def B_diesel_E(p):
    """convert to SI and recompute (conversion constants: 1 in = 0.0254 m, 1 lbm = 0.45359237 kg, 1 psia = 6.894757 kPa, 1 Btu = 1.055056 kJ)."""
    T1 = p['T1'] * 5 / 9; P1 = p['P1'] * 6.894757; V1 = p['V1_in3'] * 0.0254 ** 3; cp = p['cp'] * 4.1868; cv = p['cv'] * 4.1868; Rg = p['R'] * 6.894757 * 0.3048 ** 3 / 0.45359237 / (5 / 9) / 1.0 / 1.0 * 1.0
    # R [psia ft3/(lbm R)] -> kJ/(kg K): psia*ft3 = 6.894757 kPa * 0.0283168 m3 = 0.19524 kJ ; per lbm -> /0.45359 ; per R -> /(5/9)
    Rg = p['R'] * 6.894757 * 0.0283168466 / 0.45359237 / (5 / 9)
    r, rc, k = p['r'], p['rc'], p['k']; m = P1 * V1 / (Rg * T1)
    s = adiabat_T(T1, 1.0, 1.0 / r, k - 1); T2 = float(s.y[0, -1]); T3 = rc * T2; s2 = adiabat_T(T3, rc / r, 1.0, k - 1); T4 = float(s2.y[0, -1])
    Qin = m * cp * (T3 - T2); Qout = m * cv * (T4 - T1); W = Qin - Qout; psi = lambda T: T * 9 / 5
    P2 = P1 * r ** k / 6.894757; P4 = P1 * T4 / T1 / 6.894757
    mep = W / (V1 * (1 - 1 / r)) / 6.894757
    return dict(T2=psi(T2), P2=P2, T3=psi(T3), T4=psi(T4), P4=P4, m=m / 0.45359237, Qin=Qin / 1.055056, Qout=Qout / 1.055056, W=W / 1.055056, eta=W / Qin, mep=mep)
def adiabat_P(T1, P1, T2, k):                          # P along an isentrope by ODE dP/dT = k/(k-1) P/T
    return float(solve_ivp(lambda T, P: k / (k - 1) * P / T, (T1, T2), [P1], rtol=1e-12, atol=1e-12).y[0, -1])
def B_jet_E(p):
    k = p['k']; cp = p['cp'] * 4.1868; Ta = p['Ta'] * 5 / 9; Pa = p['Pa'] * 6.894757; Vf = p['V'] * 0.3048; T4 = p['T4'] * 5 / 9; md = p['mdot'] * 0.45359237
    T2 = brentq(lambda T: cp * 1000 * (T - Ta) - Vf ** 2 / 2, Ta, 3 * Ta); P2 = adiabat_P(Ta, Pa, T2, k)
    T3 = brentq(lambda T: adiabat_P(T2, P2, T, k) - p['rp'] * P2, T2, 5 * T2); P3 = p['rp'] * P2
    T5 = brentq(lambda T: cp * (T3 - T2) - cp * (T4 - T), 100.0, T4); P5 = adiabat_P(T4, P3, T5, k)
    T6 = brentq(lambda T: adiabat_P(T5, P5, T, k) - Pa, 100.0, T5); V6 = math.sqrt(2000 * cp * (T5 - T6)); Wp = md * (V6 - Vf) * Vf / 1000; Qin = md * cp * (T4 - T3)
    psi = lambda T: T * 9 / 5
    return dict(T2=psi(T2), P2=P2 / 6.894757, T3=psi(T3), P3=P3 / 6.894757, T5=psi(T5), P5=P5 / 6.894757, T6=psi(T6), V6=V6 / 0.3048, Wp=Wp / 1.055056, Qin=Qin / 1.055056, etaP=Wp / Qin)
def B_jet_k(p):
    k, cp = p['k'], p['cp']; Ta, Pa, Vf, T4, md = p['Ta'], p['Pa'], p['V'], p['T4'], p['mdot']
    T2 = brentq(lambda T: cp * 1000 * (T - Ta) - Vf ** 2 / 2, Ta, 3 * Ta); P2 = adiabat_P(Ta, Pa, T2, k); T3 = brentq(lambda T: adiabat_P(T2, P2, T, k) - p['rp'] * P2, T2, 5 * T2); P3 = p['rp'] * P2
    T5 = brentq(lambda T: cp * (T3 - T2) - cp * (T4 - T), 100.0, T4); P5 = adiabat_P(T4, P3, T5, k); T6 = brentq(lambda T: adiabat_P(T5, P5, T, k) - Pa, 100.0, T5)
    V6 = math.sqrt(2000 * cp * (T5 - T6)); Wp = md * (V6 - Vf) * Vf / 1000; Qin = md * cp * (T4 - T3)      # kW
    return dict(T2=T2, T3=T3, T5=T5, T6=T6, V6=V6, Wp=Wp, Qin=Qin, etaP=Wp / Qin)
def B_turbojet(p):
    Ta, Pa, Vf, rp, T04, QR = p['Ta'], p['Pa'], p['V'], p['rp'], p['T04'], p['QR']; cp, k = 1.005, 1.4
    T02 = brentq(lambda T: cp * 1000 * (T - Ta) - Vf ** 2 / 2, Ta, 2 * Ta); P02 = adiabat_P(Ta, Pa, T02, k); T03 = brentq(lambda T: adiabat_P(T02, P02, T, k) - rp * P02, T02, 5 * T02)
    f = brentq(lambda f_: (1 + f_) * cp * T04 - cp * T03 - f_ * QR, 0.0, 0.1)         # energy balance of the burner: (1+f) h04 = h03 + f QR
    T05 = brentq(lambda T: (1 + f) * cp * (T04 - T) - cp * (T03 - T02), 300.0, T04); P05 = adiabat_P(T04, rp * P02, T05, k)
    T7 = brentq(lambda T: adiabat_P(T05, P05, T, k) - Pa, 100.0, T05); Vj = math.sqrt(2000 * cp * (T05 - T7)); st = (1 + f) * Vj - Vf
    w = 0.5 * (1 + f) * (Vj - Vf) ** 2; e1 = st * Vf / (st * Vf + w); e2 = 2 * Vf / (Vf + Vj); eth = (st * Vf + w) / (f * QR * 1000)
    return dict(T02=T02, T03=T03, f=f, T05=T05, T7=T7, Vj=Vj, spec_thrust=st, etap1=e1, etap2=e2, etath=eth, etao=e1 * eth, ma=12.12e3 / st)
def B_formula(p):
    n = p['name']
    if n == 'carnot': TL, TH = sp.symbols('TL TH', positive=True); ds = sp.symbols('ds', positive=True); return dict(eta=float((1 - (TL * ds) / (TH * ds)).subs({TL: p['TL'], TH: p['TH']})))
    if n == 'carnot_TH': TH = sp.symbols('TH', positive=True); return dict(TH=float(sp.solve(sp.Eq(1 - sp.Float(p['TL']) / TH, sp.Float(p['eta'])), TH)[0]))
    if n == 'otto_eta':
        r, k = p['r'], p['k']; T1 = 300.0; T3 = 1800.0; T2 = T1 * r ** (k - 1); T4 = T3 / r ** (k - 1); return dict(eta=1 - (T4 - T1) / (T3 - T2))
    if n == 'otto_r': return dict(r=brentq(lambda r: 1 - r ** (1 - p['k']) - p['eta'], 1.01, 100.0))
    if n == 'diesel_eta':
        r, rc, k = p['r'], p['rc'], p['k']; T1 = 300.0; T2 = T1 * r ** (k - 1); T3 = rc * T2; T4 = T3 * (rc / r) ** (k - 1); return dict(eta=1 - (T4 - T1) / (k * (T3 - T2)))
    if n == 'rp_opt':
        T1, T3, k = p['T1'], p['T3'], p['k']; f = lambda rp: -(B_brayton_k(dict(rp=rp, T1=T1, T3=T3, k=k, cp=1.005, etac=1, etat=1, eps=0))['wnet']); return dict(rp=minimize_scalar(f, bounds=(2, 60), method='bounded', options=dict(xatol=1e-9)).x)
    if n == 'brayton_wmax':
        T1, T3, k = p['T1'], p['T3'], p['k']; f = lambda rp: -(B_brayton_k(dict(rp=rp, T1=T1, T3=T3, k=k, cp=1.005, etac=1, etat=1, eps=0))['wnet']); ro = minimize_scalar(f, bounds=(2, 60), method='bounded', options=dict(xatol=1e-9)).x
        b = B_brayton_k(dict(rp=ro, T1=T1, T3=T3, k=k, cp=1.005, etac=1, etat=1, eps=0)); return dict(wnet=b['wnet'], eta=b['eta'])
    if n == 'regen_eta': b = B_brayton_k(dict(rp=p['rp'], T1=p['T1'], T3=p['T3'], k=p['k'], cp=1.005, etac=1, etat=1, eps=1.0)); return dict(eta=b['eta'])
    if n == 'regen_cross':
        T1, T3, k = p['T1'], p['T3'], p['k']; g = lambda rp: B_brayton_k(dict(rp=rp, T1=T1, T3=T3, k=k, cp=1.005, etac=1, etat=1, eps=1.0))['eta'] - B_brayton_k(dict(rp=rp, T1=T1, T3=T3, k=k, cp=1.005, etac=1, etat=1, eps=0))['eta']
        return dict(rp=brentq(g, 2.0, 60.0, xtol=1e-12))
    if n == 'regen_T5': T5 = sp.symbols('T5'); return dict(T5=float(sp.solve(sp.Eq((T5 - p['T2']) / (p['T4'] - p['T2']), sp.Float(p['eps'])), T5)[0]))
    if n == 'w_comp_stages':
        T1, rp, k = p['T1'], p['rp'], p['k']; Rg = 1.005 * (k - 1) / k; P1 = 100.0; one = quad(lambda P: Rg * T1 * (P / P1) ** ((k - 1) / k) / P, P1, rp * P1)[0]
        Pm = P1 * math.sqrt(rp); two = quad(lambda P: Rg * T1 * (P / P1) ** ((k - 1) / k) / P, P1, Pm)[0] + quad(lambda P: Rg * T1 * (P / Pm) ** ((k - 1) / k) / P, Pm, rp * P1)[0]; return dict(w1=one, w2=two)
    if n == 'p_inter':
        P1, P3 = p['P1'], p['P3']; k = 1.4; Rg = 1.005 * 0.4 / 1.4; T1 = 300.0
        tot = lambda Pm: quad(lambda P: Rg * T1 * (P / P1) ** ((k - 1) / k) / P, P1, Pm)[0] + quad(lambda P: Rg * T1 * (P / Pm) ** ((k - 1) / k) / P, Pm, P3)[0]
        return dict(Pm=minimize_scalar(tot, bounds=(P1 * 1.01, P3 * 0.99), method='bounded', options=dict(xatol=1e-9)).x)
    if n == 'thrust': mdot, Ve, Vi = sp.symbols('m Ve Vi'); return dict(F=float((mdot * Ve - mdot * Vi).subs({mdot: p['m'], Ve: p['Ve'], Vi: p['Vi']})))
    if n == 'diffuser_T': return dict(T2=brentq(lambda T: p['cp'] * 1000 * (T - p['Ta']) - p['V'] ** 2 / 2, p['Ta'], 5 * p['Ta']))
    if n == 'r_from_V': return dict(r=float(sp.Rational(str(p['Vd'])) / sp.Rational(str(p['Vc'])) + 1))
    if n == 'engine_power': return dict(P=p['mep'] * p['Vd'] * (p['N'] / 60.0) / 2.0)
    raise KeyError(n)
CONSTK = dict(otto_k=B_otto_k, diesel_k=B_diesel_k, brayton_k=B_brayton_k, multi_k=B_multi_k, c916=B_c916, c919=B_c919, c959=B_c959, diesel_E=B_diesel_E, jet_E=B_jet_E, jet_k=B_jet_k, turbojet_ideal=B_turbojet, formula=B_formula)

# ---------------------------------------------------------------- run every registry entry
groups = collections.OrderedDict()
for e in V['registry']: groups.setdefault((e['model'], json.dumps(e['params'], sort_keys=True)), []).append(e)
print(f'{len(V["registry"])} registered answers in {len(groups)} problem groups, {len(V["printed"])} printed answers')
cache = {}
for (model, pj), es in groups.items():
    p = json.loads(pj)
    if model in VAR:
        for kind in ('poly', 'coolprop'):
            try: out = VAR[model](gas(kind), p)
            except Exception as ex: FAILS.append(f'{model} {pj[:70]}: route B ({kind}) raised {ex!r}'); continue
            for e in es:
                if e['out'] not in out: FAILS.append(f'{model}.{e["out"]} missing in route B'); continue
                tol = TOLV.get(e['out'], TOLV['default']); rec(f'{model}.{e["out"]} [{kind}] {pj[:46]}', e['value'], out[e['out']], tol)
    else:
        try: out = CONSTK[model](p)
        except Exception as ex: FAILS.append(f'{model} {pj[:70]}: route B raised {ex!r}'); continue
        for e in es:
            if e['out'] not in out: FAILS.append(f'{model}.{e["out"]} missing in route B'); continue
            if model in ('otto_k', 'diesel_k', 'multi_k', 'c916', 'c919', 'c959') and e['out'] in ('wnet', 'eta', 'mep', 'qout', 'Wcycle6', 'P', 'sfc', 'Qout'): tol = TOL_CONSTK
            elif model == 'brayton_k' or model in ('formula',): tol = 2e-6 if e['out'] not in ('rp',) else 1e-6
            elif model == 'diesel_E': tol = 2e-3
            elif model in ('jet_E', 'jet_k', 'turbojet_ideal'): tol = 2e-3 if model == 'jet_E' else 1e-5
            else: tol = TOL_TEMP if e['out'].startswith('T') or e['out'] in ('rc', 'P2', 'P3', 'P4') else 1e-4
            if model == 'formula' and e['out'] == 'rp' : tol = 1e-6
            rec(f'{model}.{e["out"]} {pj[:46]}', e['value'], out[e['out']], tol)

# ---------------------------------------------------------------- route C: _shared/thermo.js (Lab code) with node for the constant-k Otto, Diesel, Brayton, multistage
calls = []
for e in V['registry']:
    if e['model'] in ('otto_k', 'diesel_k', 'brayton_k', 'multi_k') and e['out'] in ('T2', 'T3', 'T4', 'wnet', 'eta', 'mep', 'bwr', 'wc', 'wt', 'qin', 'T5', 'rc', 'P3'): calls.append(e)
node_in = []
for e in calls:
    p = e['params']
    if e['model'] == 'otto_k':
        q = dict(fn='otto', r=p['r'], T1=p['T1'], P1=p['P1'], k=p['k'], R=p['R'], cv=p['cv']); mode = 'qin' if 'qin' in p else 'T3' if 'T3' in p else 'T4'; q['mode'] = mode; q[mode] = p[mode]
    elif e['model'] == 'diesel_k':
        q = dict(fn='diesel', r=p['r'], T1=p['T1'], P1=p['P1'], k=p['k'], R=p['R'], cp=p['cp'], cv=p['cv']); mode = 'rc' if 'rc' in p else 'T3' if 'T3' in p else 'qin'; q['mode'] = mode; q[mode] = p[mode]
    elif e['model'] == 'brayton_k':
        q = dict(fn='brayton', rp=p['rp'], T1=p['T1'], T3=p['T3'], k=p['k'], cp=p['cp'], etac=p['etac'], etat=p['etat'], eps=p['eps'])
    else:
        q = dict(fn='brayton', rp=p['rp'], T1=p['T1'], T3=p['T3'], k=p['k'], cp=p['cp'], etac=p['etac'], etat=p['etat'], eps=p['eps'], Nc=p['N'], Nt=p['N'])
    node_in.append(q)
js = ("const T=require(process.argv[1]+'/_shared/thermo.js');const inp=JSON.parse(require('fs').readFileSync(0,'utf8'));"
      "const out=inp.map(q=>{try{const fn=q.fn;delete q.fn;return T[fn](q);}catch(e){return {error:String(e.code||e.message)};}});console.log(JSON.stringify(out));")
res = subprocess.run(['node', '-e', js, ROOT], input=json.dumps(node_in), capture_output=True, text=True)
if res.returncode != 0: FAILS.append('node thermo.js failed: ' + res.stderr[-300:])
else:
    outs = json.loads(res.stdout); mp = dict(T2='T2', T3='T3', T4='T4', wnet='wnet', eta='eta', mep='mep', bwr='bwr', wc='wc', wt='wt', qin='qin', T5='T5', rc='rc', P3='P3')
    kk = 0
    for e, o in zip(calls, outs):
        if 'error' in o: FAILS.append(f'thermo.js error for {e["model"]}: {o}'); continue
        key = mp[e['out']]
        if e['model'] == 'brayton_k' and e['out'] == 'T2': key = 'Tc'
        if e['model'] == 'brayton_k' and e['out'] == 'T4': key = 'Tt'
        if e['model'] == 'multi_k' and e['out'] == 'T2': key = 'Tc'
        if e['model'] == 'multi_k' and e['out'] == 'T4': key = 'Tt'
        if key not in o: continue
        rec(f'thermo.js {e["model"]}.{e["out"]}', e['value'], o[key], 1e-6); kk += 1
    print(f'route C (thermo.js through node): {kk} comparisons')

# ---------------------------------------------------------------- printed answers (slides and books): route A value against the number printed in the source
print('\nANSWERS PRINTED IN THE SOURCES vs route A')
for e in V['printed']: rec(f'printed {e["name"]} ({e["src"]})', e['mine'], e['printed'], e['tol'])
# ---------------------------------------------------------------- source-error checks (documented in data/verify/m02_notes.json)
import gen_m02_orig3  # noqa  (just to make sure it imports)
from m02_common import brayton as bk_, otto as ok_, turbojet_unchoked, diesel as dk_
# slide tr.40: eta_Brayton(rp) of the figure is above the k = 1.4 formula at large rp
print('\nSLIDE / BOOK DISCREPANCIES measured (documented in the notes)')
for rp, read in ((20, 0.63), (25, 0.653)):
    f = 1 - rp ** (-0.4 / 1.4); print(f'  slide p.40: eta(rp={rp}) read from the image {read:.3f} (+-0.02) vs formula k=1.4 {f:.3f}: gap {read-f:+.3f}'); assert read - f > 0.04
f14 = 1 - 14 ** -0.4; print(f'  slide p.25: Otto curve ends near 0.665 at r=14 vs formula {f14:.3f} (gap {0.665-f14:+.3f}, inside the +-0.02 reading error)'); assert abs(0.665 - f14) < 0.02
ro = (1000 / 300) ** (1.4 / 0.8); print(f'  slide p.40: r_p,opt = (1000/300)^(k/(2(k-1))) = {ro:.3f} (slide 8.2)'); assert abs(ro - 8.2) < 0.05
# r_p,opt with variable cp: smooth property models (A-2c polynomial, CoolProp Cp0) versus the A-17 look-up (piecewise linear, so w_net(r_p) is bumpy)
from m02_common import brayton_var
def wnet_gas(g, rp):
    T1, T3 = 300.0, 1000.0; T2s = g.T_isen_P(T1, math.log(rp)); T4s = g.T_isen_P(T3, -math.log(rp)); return g.h(T4s, T3) - g.h(T1, T2s)
opt = {}
for kind in ('poly', 'coolprop'):
    g = gas(kind); r_ = minimize_scalar(lambda x_: -wnet_gas(g, x_), bounds=(4, 20), method='bounded', options=dict(xatol=1e-6)).x; opt[kind] = r_
    print(f'  r_p,opt with variable cp ({kind}) = {r_:.2f}; w_net(8.2)/w_net,max = {wnet_gas(g, 8.2)/wnet_gas(g, r_):.4f}'); assert 8.5 < r_ < 9.6 and wnet_gas(g, 8.2) / wnet_gas(g, r_) > 0.995
scan = [(rp, brayton_var(rp, 300, 1000)['wnet']) for rp in np.arange(7.0, 11.0, 0.05)]; wmax = max(w for _, w in scan); rr = [rp for rp, w in scan if w > wmax - 0.3]
print(f'  A-17 look-up: w_net(r_p) is bumpy (linear interpolation, +-0.5 kJ/kg): the points within 0.3 kJ/kg of the maximum span r_p = {min(rr):.2f} .. {max(rr):.2f}; so "r_p,opt = 8.0 from A-17" is not a stable number')
assert abs(wnet_gas(gas('poly'), 8.2) - brayton_var(8.2, 300, 1000)['wnet']) / wnet_gas(gas('poly'), 8.2) < 0.01
# Tutorials I #2: k=1.4 for temperatures but cp/cv = 1.4035 for heats
d2 = dk_(18, 540, 14.7, k=1.4, R=0.3704, cp=0.240, cv=0.171, rc=2); print(f'  Tutorials I #2: eta with cp, cv = {d2["eta"]:.4f}; exact k=1.4 formula {d2["eta_formula"]:.4f} (slide 0.632)'); assert abs(d2['eta'] - 0.632) < 0.001 and abs(d2['eta_formula'] - 0.6316) < 1e-4
# Cengel 9-59: AF = 24 in the statement, printed answers need 25
import gen_m02_orig3 as O3
print('  Cengel 9-59: printed 2383 K reproduced only with AF = 25 (see answers above); with AF = 24 T3 = 2445 K')
# El-Sayed Ex 4.2: two arithmetic slips (T03 587.5 and T7 563.6)
ex = turbojet_unchoked(240, 32, 310, 12, 1400, 42700); print(f'  El-Sayed Ex 4.2: T03 = {ex["T03"]:.1f} K (book 587.5), T7 = {ex["T7"]:.1f} K (book 563.6), Vj = {ex["Vj"]:.1f} m/s (book 1044.34)')
Vj_book = math.sqrt(2000 * 1.005 * (1106.1 - 563.6)); assert abs(Vj_book - 1044.3) < 0.5               # the book's Vj follows from its slip T7 = 563.6
assert abs(1106.1 / 1.9283 - 573.6) < 0.1 and abs(287.8 * 2.035 - 585.7) < 0.1                           # the two slips, recomputed
# Otto efficiency vs Diesel: bracket > 1 for every rc > 1 (sympy check of slide p.31 claim, numeric scan)
assert all((rc ** 1.4 - 1) / (1.4 * (rc - 1)) > 1 for rc in np.linspace(1.001, 6, 400))
# ideal-regenerator crossover equals the r_p of maximum work (sympy)
x, a = sp.symbols('x a', positive=True)       # x = rp^((k-1)/k), a = T3/T1
cross = sp.solve(sp.Eq(1 - 1 / x, 1 - x / a), x); assert sp.simplify(cross[0] ** 2 - a) == 0; print('  sympy: eta_regen = eta_simple  <=>  x^2 = T3/T1  (the r_p of maximum work)')

# ---------------------------------------------------------------- report
print(f'\n{len(ROWS)} comparisons')
print('largest relative deviation per family (route B vs A, and printed vs A):')
for k_, v_ in sorted(DEV.items(), key=lambda t: -t[1])[:14]: print(f'  {k_:28s} {v_:.3e}')
bad = [r for r in ROWS if r[5] != 'ok']
if os.environ.get('SHOW_ALL'):
    for name, a, b, err, tol, st in ROWS: print(f'{name:90s} {a:14.6g} {b:14.6g} {err:9.2e} {tol:8.1e} {st}')
for r in bad: print('FAIL', r)
print('FAILS: none' if not FAILS else 'FAILS: ' + '; '.join(FAILS))
sys.exit(0 if not FAILS else 1)
