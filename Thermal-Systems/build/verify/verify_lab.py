"""Gate of the Lab (build/lab_body.py, _shared/thermo.js, _shared/lab.js).
Computes the expected values of every function of thermo.js by an INDEPENDENT route (numpy / scipy / sympy: integral of P dV, entropy equation by
brentq, mass-flux maximisation, sympy linear systems, ODEs), adds the reference values of the checked sources (OCR_output/_qa/*.json) and the
worked examples shown on the Lab page, writes data/lab_expected.json and runs `node tests/lab_node_test.js` on it.
Run:  .venv/bin/python -I build/verify/verify_lab.py [--mutation]      (finishes with 'FAILS: none')
--mutation : copy thermo.js, break one coefficient on purpose, and show that the Node test catches it (the real file is never touched)."""
import json, math, os, re, subprocess, sys, tempfile, shutil
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
QA = os.path.abspath(os.path.join(ROOT, '..', 'OCR_output', '_qa'))
OUT = os.path.join(ROOT, 'data', 'lab_expected.json')
cases, refs, examples = [], [], []
R_AIR = 0.287


def tol_of(v, abs_tol=0.0, rel=1e-9):
    return max(abs_tol, rel * abs(v), 1e-12)


def case(cid, fn, args, expect, how, argv=None):
    """expect: {key: value | (value, abs_tol)}. key '' = the return value itself."""
    e = {}
    for k, v in expect.items():
        if isinstance(v, tuple):
            e[k] = [float(v[0]), float(v[1])]
        else:
            e[k] = [float(v), tol_of(v, rel=1e-8)]
    c = {'id': cid, 'fn': fn, 'expect': e, 'how': how}
    if argv is not None: c['argv'] = argv
    else: c['args'] = args
    cases.append(c)


# ============================================================ 1. Otto: integral of P dV (consistent gas: cv = R/(k-1))
def otto_indep(r, k, R, T1, P1, mode, val, V1=None):
    v1 = R * T1 / P1; v2 = v1 / r                                     # ideal gas law
    P12 = lambda v: P1 * (v1 / v) ** k                                 # polytropic law (isentropic)
    w12 = quad(P12, v1, v2, epsabs=1e-12, epsrel=1e-12)[0]             # work done ON the gas is negative here: integral of P dV from v1 to v2
    P2 = P12(v2); T2 = P2 * v2 / R
    cv = R / (k - 1)
    if mode == 'qin': T3 = T2 + val / cv
    elif mode == 'T3': T3 = val
    else:                                                               # T4 given: P4 from gas law, back along the polytropic law to state 3
        P4 = R * val / v1; P3 = P4 * (v1 / v2) ** k; T3 = P3 * v2 / R
    P3 = R * T3 / v2
    P34 = lambda v: P3 * (v2 / v) ** k
    w34 = quad(P34, v2, v1, epsabs=1e-12, epsrel=1e-12)[0]
    P4 = P34(v1); T4 = P4 * v1 / R
    wnet = w12 + w34; qin = cv * (T3 - T2)
    out = dict(T2=T2, P2=P2, T3=T3, P3=P3, T4=T4, P4=P4, qin=qin, qout=qin - wnet, wnet=wnet, eta=wnet / qin, mep=wnet / (v1 - v2), v1=v1, v2=v2)
    x = sp.symbols('x', positive=True)
    out['etaOtto'] = float((1 - x ** (1 - sp.Float(k, 30))).subs(x, sp.Float(r, 30)))      # sympy
    if V1 is not None:
        m = P1 * V1 / (R * T1)
        Wt = quad(lambda V: P1 * (V1 / V) ** k, V1, V1 / r)[0] + quad(lambda V: P3 * (V1 / r / V) ** k, V1 / r, V1)[0]   # integral of P dV on actual volumes
        out.update(m=m, Wnet=Wt, Qin=m * qin, Qout=m * qin - Wt)
    return out


for i, (r, k, R, T1, P1, mode, val, V1) in enumerate([(8, 1.4, R_AIR, 290, 100, 'qin', 800, None), (9.5, 1.4, R_AIR, 308, 100, 'T4', 800, 0.0006), (10, 1.35, R_AIR, 300, 95, 'T3', 2200, None),
                                                      (12, 1.3, 0.25, 320, 150, 'qin', 1500, 0.002), (7, 1.4, R_AIR, 300, 100, 'T3', 1800, None), (6, 1.67, 0.2081, 400, 200, 'qin', 900, None)], 1):
    e = otto_indep(r, k, R, T1, P1, mode, val, V1)
    a = dict(r=r, k=k, R=R, T1=T1, P1=P1, mode=mode); a[mode] = val
    if V1: a['V1'] = V1
    case(f'otto-{i}', 'otto', a, e, 'integral of P dV (quad) + gas law + sympy for 1-r^(1-k)')

# mixed convention: k for T and P, cv given for the heats (Tutorials I style)
for cid, (r, k, cv, R, T1, P1, q) in {'otto-mix1': (8, 1.4, 0.718, 0.287, 290, 100, 800.0)}.items():
    T3s = sp.symbols('T3'); T2 = T1 * r ** (k - 1); sol = sp.solve(sp.Eq(q, cv * (T3s - T2)), T3s)[0]; T3 = float(sol); T4 = T3 / r ** (k - 1)
    case(cid, 'otto', dict(r=r, k=k, cv=cv, R=R, T1=T1, P1=P1, mode='qin', qin=q), {'T3': T3, 'T4': T4, 'qout': cv * (T4 - T1), 'wnet': q - cv * (T4 - T1), 'eta': 1 - cv * (T4 - T1) / q,
                                                                               'mep': (q - cv * (T4 - T1)) / (R * T1 / P1 * (1 - 1 / r))}, 'sympy solve of q = cv (T3-T2), heats by cv')


# ============================================================ 2. Diesel
def diesel_indep(r, k, R, T1, P1, mode, val, V1=None):
    v1 = R * T1 / P1; v2 = v1 / r; cv = R / (k - 1); cp = k * R / (k - 1)
    P12 = lambda v: P1 * (v1 / v) ** k
    w12 = quad(P12, v1, v2, epsabs=1e-12, epsrel=1e-12)[0]; P2 = P12(v2); T2 = P2 * v2 / R
    if mode == 'rc': v3 = val * v2
    elif mode == 'T3': v3 = R * val / P2
    else: v3 = R * (T2 + val / cp) / P2
    T3 = P2 * v3 / R; w23 = P2 * (v3 - v2)
    qin = w23 + cv * (T3 - T2)                                          # first law on the isobaric heating
    P34 = lambda v: P2 * (v3 / v) ** k
    w34 = quad(P34, v3, v1, epsabs=1e-12, epsrel=1e-12)[0]; P4 = P34(v1); T4 = P4 * v1 / R
    wnet = w12 + w23 + w34
    rc = v3 / v2
    x = sp.symbols('x', positive=True)
    eta_formula = float((1 - (1 / x ** (sp.Float(k, 30) - 1)) * (sp.Float(rc, 30) ** sp.Float(k, 30) - 1) / (sp.Float(k, 30) * (sp.Float(rc, 30) - 1))).subs(x, sp.Float(r, 30)))
    out = dict(rc=rc, T2=T2, P2=P2, P3=P2, T3=T3, T4=T4, P4=P4, qin=qin, qout=qin - wnet, wnet=wnet, eta=wnet / qin, etaDiesel=eta_formula, mep=wnet / (v1 - v2), v1=v1, v2=v2, v3=v3,
               etaOtto=1 - r ** (1 - k))
    if V1 is not None:
        m = P1 * V1 / (R * T1); out.update(m=m, Qin=m * qin, Wnet=m * wnet, Qout=m * (qin - wnet))
    return out


for i, (r, k, R, T1, P1, mode, val, V1) in enumerate([(18, 1.4, R_AIR, 300, 101.353, 'rc', 2, None), (20, 1.4, R_AIR, 293, 95, 'T3', 2200, None), (16, 1.35, 0.3, 310, 100, 'qin', 1000, None),
                                                      (14, 1.3, 0.2, 350, 120, 'rc', 1.5, 0.001), (22, 1.4, R_AIR, 300, 100, 'rc', 2.5, None)], 1):
    e = diesel_indep(r, k, R, T1, P1, mode, val, V1)
    a = dict(r=r, k=k, R=R, T1=T1, P1=P1, mode=mode); a[mode] = val
    if V1: a['V1'] = V1
    case(f'diesel-{i}', 'diesel', a, e, 'integral of P dV over the 3 work-exchanging processes, first law for q_in, sympy for the eta formula')

# mixed convention (Tutorials I #2): temperatures by k, heats by cp, cv
r, rc, k, cp, cv, T1, P1 = 18, 2, 1.4, 0.24 * 4.1868, 0.171 * 4.1868, 300.0, 14.7 * 6.894757
T2 = T1 * r ** (k - 1); T3 = rc * T2; T4 = T3 * (rc / r) ** (k - 1) * 1.0; T4b = T1 * rc ** k
assert abs(T4 - T4b) < 1e-9
qin = cp * (T3 - T2); qout = cv * (T4b - T1)
case('diesel-mix1', 'diesel', dict(r=r, rc=rc, k=k, cp=cp, cv=cv, R=R_AIR, T1=T1, P1=P1, mode='rc'), {'T2': T2, 'T3': T3, 'T4': T4b, 'qin': qin, 'qout': qout, 'eta': 1 - qout / qin,
     'etaDiesel': 1 - (rc ** k - 1) / (r ** (k - 1) * k * (rc - 1))}, 'by hand with k for T and cp, cv for heats (sympy-free closed form of Tutorials I #2)')


# ============================================================ 3. Brayton: entropy equation solved by brentq, h from cp T
def isen_exit(Tin, pr, k, expand):
    cp = k * R_AIR / (k - 1)
    f = (lambda T: cp * math.log(T / Tin) + R_AIR * math.log(pr)) if expand else (lambda T: cp * math.log(T / Tin) - R_AIR * math.log(pr))
    return brentq(f, 1.0, 20000.0, xtol=1e-12, rtol=1e-14)


def brayton_indep(rp, T1, T3, k, etac=1.0, etat=1.0, eps=0.0, Nc=1, Nt=1):
    cp = k * R_AIR / (k - 1)
    prc, prt = rp ** (1 / Nc), rp ** (1 / Nt)
    T2s = isen_exit(T1, prc, k, False); T2 = T1 + (T2s - T1) / etac
    T4s = isen_exit(T3, prt, k, True); T4 = T3 - etat * (T3 - T4s)
    wc = Nc * cp * (T2 - T1); wt = Nt * cp * (T3 - T4)
    T5 = T2 + eps * (T4 - T2) if eps > 0 else T2
    T6 = T4 - (T5 - T2) if eps > 0 else T4
    qin = cp * (T3 - T5) + (Nt - 1) * cp * (T3 - T4)
    qout_hx = cp * (T6 - T1) + (Nc - 1) * cp * (T2 - T1)                  # heat rejected in the final cooler and the intercoolers
    wnet = wt - wc
    assert abs(qin - qout_hx - wnet) < 1e-8 * max(abs(qin), 1.0), 'first law of the cycle'
    return dict(Tcs=T2s, Tc=T2, Tts=T4s, Tt=T4, T5=T5, T6=T6, wc=wc, wt=wt, wnet=wnet, bwr=wc / wt, qin=qin, qout=qout_hx, eta=wnet / qin, etaIdeal=1 - rp ** (-(k - 1) / k),
                P2=100 * rp)


bcases = [dict(rp=8, T1=300, T3=1300, k=1.4), dict(rp=10, T1=300, T3=1400, k=1.4, etac=0.85, etat=0.88), dict(rp=8, T1=300, T3=1200, k=1.4, eps=1.0),
          dict(rp=12, T1=290, T3=1400, k=1.4, etac=0.8, etat=0.85, eps=0.75), dict(rp=16, T1=300, T3=1300, k=1.4, Nc=2, Nt=2, eps=0.8),
          dict(rp=20, T1=300, T3=1400, k=1.35, etac=0.85, etat=0.9, eps=0.7, Nc=3, Nt=2), dict(rp=6, T1=288, T3=1100, k=1.4, Nc=2), dict(rp=2, T1=300, T3=1000, k=1.4),
          dict(rp=15, T1=300, T3=1000, k=1.4), dict(rp=8.2, T1=300, T3=1000, k=1.4)]
for i, a in enumerate(bcases, 1):
    e = brayton_indep(**a); aa = dict(a); aa['R'] = R_AIR
    case(f'brayton-{i}', 'brayton', aa, e, 'entropy equation (brentq) per stage, h = cp T, first law of the whole cycle asserted')

# optimum pressure ratio: scipy maximisation of w_net(rp), sympy for the closed form
def wnet_of(rp, T1, T3, k, etac, etat, Nc, Nt):
    return brayton_indep(rp, T1, T3, k, etac, etat, 0.0, Nc, Nt)['wnet']

x, tau, ec, et = sp.symbols('x tau eta_c eta_t', positive=True)
xs = sp.solve(sp.diff(et * tau * (1 - 1 / x) - (x - 1) / ec, x), x)
assert any(sp.simplify(s - sp.sqrt(ec * et * tau)) == 0 for s in xs), xs                  # sympy: x = sqrt(eta_c eta_t tau)
for i, (T1, T3, k, etac, etat, Nc, Nt) in enumerate([(300, 1000, 1.4, 1, 1, 1, 1), (300, 1300, 1.4, 0.85, 0.9, 1, 1), (300, 1400, 1.4, 0.85, 0.9, 2, 2), (290, 1250, 1.33, 0.8, 0.88, 3, 3), (300, 1400, 1.4, 0.85, 0.9, 1, 2), (300, 1400, 1.4, 1, 1, 2, 3)], 1):
    res = minimize_scalar(lambda lr: -wnet_of(math.exp(lr), T1, T3, k, etac, etat, Nc, Nt), bounds=(math.log(1.01), math.log(5000)), method='bounded', options={'xatol': 1e-10})
    rp_num = math.exp(res.x)
    case(f'brayton-opt-{i}', 'braytonOptRp', dict(T1=T1, T3=T3, k=k, etac=etac, etat=etat, Nc=Nc, Nt=Nt), {'rp': (rp_num, 2e-5 * rp_num)}, 'scipy bounded maximisation of w_net(rp) from the entropy-equation chain')
# regenerator crossover: solve 1 - t x = 1 - 1/x by brentq
for T1, T3 in [(300, 1200), (300, 1500), (200, 1000), (250, 750), (330, 1000)]:
    t = T1 / T3; k = 1.4
    xx = brentq(lambda x_: (1 - t * x_) - (1 - 1 / x_), 1.0001, 1e3, xtol=1e-13)    # x = rp^((k-1)/k)
    case(f'regenx-{T1}-{T3}', 'regenCrossover', dict(T1=T1, T3=T3, k=k), {'': (xx ** (k / (k - 1)), 1e-8 * xx ** (k / (k - 1)))}, 'brentq on 1 - t x = 1 - 1/x, rp = x^(k/(k-1))', )

# ============================================================ 4. Isentropic flow
def T_ind(Ma, k):
    """T/T0 from Ma by the energy balance cp T0 = cp T + V^2/2 with V = Ma sqrt(k R T): brentq on T (R = 1, T0 = 1)."""
    cp = k / (k - 1)
    return brentq(lambda T: cp * (1 - T) - 0.5 * Ma * Ma * k * T, 1e-9, 1.0, xtol=1e-14, rtol=1e-14)


def P_ind(T, k):
    """P/P0 by integrating dlnP/dlnT = cp/R (isentropic: ds = 0) from T0 = 1 down to T."""
    cp_R = k / (k - 1)
    sol = solve_ivp(lambda lt, y: [cp_R], [0, math.log(T)], [0.0], rtol=1e-13, atol=1e-14)
    return math.exp(sol.y[0][-1])


def flux(Ma, k):
    T = T_ind(Ma, k); rho = T ** (1 / (k - 1)); V = Ma * math.sqrt(k * T)
    return rho * V


def AAs_ind(Ma, k):
    fmax = minimize_scalar(lambda m: -flux(m, k), bounds=(0.2, 3), method='bounded', options={'xatol': 1e-12}).fun * -1       # throat = maximum of rho V
    return fmax / flux(Ma, k)

for k in (1.4, 1.289, 1.33, 1.667):
    for Ma in (0.3, 0.8, 1.0, 1.5, 2.5, 4.0):
        T = T_ind(Ma, k); P = P_ind(T, k); rho = T ** (1 / (k - 1))
        case(f'fromMa-{k}-{Ma}', 'fromMa', None, {'TT0': (T, 1e-9), 'PP0': (P, 1e-9), 'rr0': (rho, 1e-9), 'AAs': (AAs_ind(Ma, k), 2e-7)}, 'energy balance (brentq) + ds=0 ODE + max of rho*V', argv=[Ma, k])
    for A, br in ((1.0304, 'sub'), (1.0304, 'sup'), (2.0351, 'sub'), (2.0351, 'sup'), (1.6281, 'sub'), (5.0, 'sub'), (25.0, 'sup'), (1.0, 'sub')):
        f = (lambda m: AAs_ind(m, k) - A)
        if A == 1.0: Mx = 1.0
        elif br == 'sub': Mx = brentq(f, 1e-4, 1.0 - 1e-9, xtol=1e-13)
        else: Mx = brentq(f, 1.0 + 1e-9, 40, xtol=1e-13)
        case(f'MaFromAAstar-{k}-{A}-{br}', 'MaFromAAstar', None, {'': (Mx, 2e-6)}, 'brentq on the mass-flux ratio rho*V (independent of eq. 17)', argv=[A, k, br])
    for pr in (0.99, 0.8, 0.5283, 0.3, 0.05):
        Mx = brentq(lambda m: P_ind(T_ind(m, k), k) - pr, 1e-6, 30, xtol=1e-13)
        case(f'MaFromPratio-{k}-{pr}', 'MaFromPratio', None, {'': (Mx, 1e-7)}, 'brentq on P/P0(Ma) from the ODE', argv=[pr, k])
    for tr in (0.99, 0.8, 0.5, 0.2):
        Mx = brentq(lambda m: T_ind(m, k) - tr, 1e-6, 30, xtol=1e-13)
        case(f'MaFromTratio-{k}-{tr}', 'MaFromTratio', None, {'': (Mx, 1e-7)}, 'brentq on T/T0(Ma)', argv=[tr, k])
    kk = sp.Float(k, 30); M = sp.symbols('M')
    TsT0 = sp.simplify((1 / (1 + (kk - 1) / 2 * M ** 2)).subs(M, 1)); PsP0 = ((1 / (1 + (kk - 1) / 2 * M ** 2)) ** (kk / (kk - 1))).subs(M, 1); rs = ((1 / (1 + (kk - 1) / 2 * M ** 2)) ** (1 / (kk - 1))).subs(M, 1)
    case(f'critical-{k}', 'critical', dict(k=k), {'TsT0': float(TsT0), 'PsP0': float(PsP0), 'rsr0': float(rs)}, 'sympy: isentropic ratios at Ma = 1')

# stagnation by integrating dh = -V dV and dP/P = cp/R dT/T
for T, P, V, k, R in [(255.7, 54.05, 250, 1.4, R_AIR), (300, 100, 100, 1.4, R_AIR), (300, 100, 1000, 1.4, R_AIR), (400, 500, 180, 1.289, 0.1889), (1100, 800, 300, 1.33, 0.287), (250, 20, 0, 1.4, R_AIR)]:
    cp = k * R / (k - 1) * 1000.0                                           # J/(kg K)
    T0 = T + quad(lambda v: v / cp, 0, V)[0]
    P0 = P * math.exp(solve_ivp(lambda lt, y: [cp / (R * 1000.0)], [math.log(T), math.log(T0)], [0.0], rtol=1e-13, atol=1e-14).y[0][-1]) if T0 > T else P
    c = math.sqrt(k * R * 1000 * T)
    case(f'stag-{T}-{V}', 'stagnation', dict(T=T, P=P, V=V, k=k, R=R), {'T0': T0, 'P0': (P0, 1e-9 * P0), 'Ma': V / c, 'dT': T0 - T, 'dP': (P0 - P, 1e-9 * max(P0, 1)), 'c': c}, 'quad of V dV / cp and ODE dlnP/dlnT = cp/R')

# choked mass flow: maximum of rho V A over Ma (independent of the closed form)
for A, P0, T0, k, R in [(0.001, 1000, 500, 1.4, R_AIR), (0.005, 1045.603, 884.194, 1.4, R_AIR), (9.608e-4, 1400, 473, 1.289, 0.1889), (0.0123, 250, 310, 1.33, 0.287), (0.002, 3000, 2800, 1.2, 0.35)]:
    def mdot_of(Ma):
        T = T0 * T_ind(Ma, k); rho = (P0 / (R * T0)) * T_ind(Ma, k) ** (1 / (k - 1)); V = Ma * math.sqrt(k * R * 1000 * T)
        return rho * V * A
    mx = -minimize_scalar(lambda m: -mdot_of(m), bounds=(0.3, 2.5), method='bounded', options={'xatol': 1e-12}).fun
    case(f'choked-{A}-{k}', 'chokedMdot', dict(Astar=A, P0=P0, T0=T0, k=k, R=R), {'': (mx, 1e-7 * mx)}, 'maximum of rho V A over Ma (minimize_scalar)')

# fromPratio with T0, P0, mdot
for P, P0, T0, mdot, k, R in [(1200, 1400, 473, 3, 1.289, 0.1889), (100, 300, 600, 2, 1.4, R_AIR), (50, 400, 900, 5, 1.33, 0.287)]:
    Ma = brentq(lambda m: P_ind(T_ind(m, k), k) - P / P0, 1e-6, 30, xtol=1e-13); T = T0 * T_ind(Ma, k); c = math.sqrt(k * R * 1000 * T); V = Ma * c; rho = P / (R * T)
    case(f'fromPr-{P}', 'fromPratio', dict(P=P, P0=P0, T0=T0, mdot=mdot, k=k, R=R), {'Ma': (Ma, 1e-7), 'T': (T, 1e-6 * T), 'c': (c, 1e-6 * c), 'V': (V, 1e-6 * V), 'rho': (rho, 1e-6 * rho), 'A': (mdot / (rho * V), 1e-6 * mdot / (rho * V))},
         'brentq on P/P0(Ma) (ODE), ideal gas law, continuity')

# duct: integrate the Hugoniot relation d ln A / d Ma = -(1-Ma^2)/(Ma (1+(k-1)/2 Ma^2)) (independent of eq. 17)
def hug(M, k): return -(1 - M * M) / (M * (1 + (k - 1) / 2 * M * M))
for Ma1, A2A1, k, br, T1, P1 in [(0.3, 0.8, 1.4, 'sub', 400, 100), (0.5, 1.5, 1.4, 'sub', 300, 200), (2.0, 1.8, 1.4, 'sup', 300, 100), (0.2, 0.7, 1.289, 'sub', 450, 150), (1.5, 2.0, 1.33, 'sup', 350, 120)]:
    target = math.log(A2A1)
    lo, hi = (1e-6, 1 - 1e-9) if br == 'sub' else (1 + 1e-9, 30)
    Ma2 = brentq(lambda m2: quad(hug, Ma1, m2, args=(k,), epsabs=1e-13, epsrel=1e-13)[0] - target, lo, hi, xtol=1e-12)
    T1T0, T2T0 = T_ind(Ma1, k), T_ind(Ma2, k); P1P0, P2P0 = P_ind(T1T0, k), P_ind(T2T0, k)
    case(f'duct-{Ma1}-{A2A1}', 'duct', dict(Ma1=Ma1, A2A1=A2A1, k=k, branch=br, T1=T1, P1=P1), {'Ma2': (Ma2, 1e-7), 'T2': (T1 * T2T0 / T1T0, 1e-6 * T1), 'P2': (P1 * P2P0 / P1P0, 1e-6 * P1), 'A1s': (AAs_ind(Ma1, k), 2e-7), 'A2s': (AAs_ind(Ma1, k) * A2A1, 2e-7 * 10)},
         'integral of the Hugoniot ODE (quad) + brentq; T, P from the energy balance and ds = 0 ODE')

# converging nozzle: flux ρVA by independent state relations; choked case = maximum of the flux over the exit pressure
for T, P, V, Pb, Ae, k, R in [(873, 1000, 150, 700, 0.005, 1.4, R_AIR), (873, 1000, 150, 400, 0.005, 1.4, R_AIR), (500, 800, 0, 600, 0.001, 1.33, 0.287), (400, 300, 50, 100, 0.01, 1.289, 0.1889), (293, 500, 0, 250, 0.0004, 1.4, R_AIR)]:
    cp = k * R * 1000 / (k - 1); T0 = T + quad(lambda v: v / cp, 0, V)[0]
    P0 = P * math.exp((cp / (R * 1000)) * math.log(T0 / T)) if V > 0 else P
    def flux_P(Pe):
        Te = T0 * math.exp((R * 1000 / cp) * math.log(Pe / P0)); Ve = math.sqrt(2 * cp * (T0 - Te)); return Pe / (R * Te) * Ve * Ae
    crit = brentq(lambda Pe: math.sqrt(2 * cp * (T0 - T0 * math.exp((R * 1000 / cp) * math.log(Pe / P0)))) - math.sqrt(k * R * 1000 * T0 * math.exp((R * 1000 / cp) * math.log(Pe / P0))), 0.01 * P0, 0.9999 * P0, xtol=1e-12)
    best = -minimize_scalar(lambda Pe: -flux_P(Pe), bounds=(0.05 * P0, 0.999 * P0), method='bounded', options={'xatol': 1e-10}).fun
    choked = Pb < crit
    md = best if choked else flux_P(Pb)
    Pe = crit if choked else Pb; Te = T0 * math.exp((R * 1000 / cp) * math.log(Pe / P0))
    case(f'nozzle-{Pb}-{k}', 'convergingNozzle', dict(T=T, P=P, V=V, Pb=Pb, Ae=Ae, k=k, R=R), {'T0': T0, 'P0': (P0, 1e-9 * P0), 'Pcrit': (crit, 1e-8 * crit), 'mdot': (md, 1e-6 * md), 'Pe': (Pe, 1e-7 * Pe), 'Te': (Te, 1e-7 * Te), 'choked': (1.0 if choked else 0.0, 0.0)},
         'quad of V dV/cp, ds = 0, critical state by sonic condition (brentq), flux maximisation (minimize_scalar)')

# Table A-32 as printed in Appendix 1 (rows copied by the P0 agent in _qa/ch5/numeric.py, k = 1.4): Ma, Ma*, A/A*, P/P0, rho/rho0, T/T0
A32 = [(0.1, 0.1094, 5.8218, 0.9930, 0.9950, 0.9980), (0.2, 0.2182, 2.9635, 0.9725, 0.9803, 0.9921), (0.3, 0.3257, 2.0351, 0.9395, 0.9564, 0.9823), (0.4, 0.4313, 1.5901, 0.8956, 0.9243, 0.9690),
       (0.5, 0.5345, 1.3398, 0.8430, 0.8852, 0.9524), (0.6, 0.6348, 1.1882, 0.7840, 0.8405, 0.9328), (0.7, 0.7318, 1.0944, 0.7209, 0.7916, 0.9107), (0.8, 0.8251, 1.0382, 0.6560, 0.7400, 0.8865),
       (0.9, 0.9146, 1.0089, 0.5913, 0.6870, 0.8606), (1.0, 1.0000, 1.0000, 0.5283, 0.6339, 0.8333), (1.2, 1.1583, 1.0304, 0.4124, 0.5311, 0.7764), (1.4, 1.2999, 1.1149, 0.3142, 0.4374, 0.7184),
       (1.6, 1.4254, 1.2502, 0.2353, 0.3557, 0.6614), (1.8, 1.5360, 1.4390, 0.1740, 0.2868, 0.6068), (2.0, 1.6330, 1.6875, 0.1278, 0.2300, 0.5556), (2.2, 1.7179, 2.0050, 0.0935, 0.1841, 0.5081),
       (2.4, 1.7922, 2.4031, 0.0684, 0.1472, 0.4647), (2.6, 1.8571, 2.8960, 0.0501, 0.1179, 0.4252), (2.8, 1.9140, 3.5001, 0.0368, 0.0946, 0.3894), (3.0, 1.9640, 4.2346, 0.0272, 0.0760, 0.3571),
       (5.0, 2.2361, 25.000, 0.0019, 0.0113, 0.1667)]
for Ma, Mas, aa, pp, rr, tt in A32:
    exp = {'AAs': (aa, 6e-5), 'PP0': (pp, 6e-5), 'rr0': (rr, 6e-5), 'TT0': (tt, 6e-5)}
    if Ma == 3.0: exp['rr0'] = (0.0762, 6e-5)                                 # the book prints 0.0760: typo (exact 0.07623), see lab note
    refs.append({'id': f'A32-Ma{Ma}', 'fn': 'fromMa', 'argv': [Ma, 1.4], 'expect': {k_: [v[0], v[1]] for k_, v in exp.items()},
                 'src': 'Appendix 1 Table A-32 (printed, 4 decimals)' + ('; rho/rho0 at Ma 3.0: printed 0.0760 is a typo, exact 0.07623' if Ma == 3.0 else '')})

# ============================================================ 5. Combustion: sympy element balances
ATOM = {'C': 12.011, 'H': 1.008, 'O': 15.999, 'N': 14.007}
fuels = [(1, 4, 0, 0, 0), (2, 6, 0, 0, 20), (8, 18, 0, 0, 60), (3, 8, 0, 0, 0), (1, 4, 1, 0, 50), (2, 6, 1, 0, 100), (0, 2, 0, 0, 0), (1, 3.8, 0, 0.1, 10), (12, 23, 0, 0, 25), (6, 6, 0, 0, 5), (2, 2, 0, 0, 0)]
for a, b, c, d, ex in fuels:
    nO2s, nCO2, nH2O, nO2, nN2 = sp.symbols('nO2s nCO2 nH2O nO2 nN2')
    def solve(x_o2):
        eqs = [sp.Eq(nCO2, a), sp.Eq(2 * nH2O, b), sp.Eq(c + 2 * x_o2, 2 * nCO2 + nH2O + 2 * nO2), sp.Eq(d + 2 * sp.Rational(376, 100) * x_o2, 2 * nN2)]
        return sp.solve(eqs, [nCO2, nH2O, nO2, nN2], dict=True)[0]
    xth = sp.symbols('xth'); st = sp.solve(sp.Eq(solve(xth)[nO2], 0), xth)[0]          # O2 supplied for nO2 = 0
    st = float(st); x_act = st * (1 + ex / 100.0); s = solve(sp.nsimplify(x_act, rational=True)) if False else solve(sp.Float(x_act, 30))
    nCO2v, nH2Ov, nO2v, nN2v = [float(s[v]) for v in (nCO2, nH2O, nO2, nN2)]
    # numpy cross-check of the same 4x4 system
    A_ = np.array([[1, 0, 0, 0], [0, 2, 0, 0], [-2, -1, -2, 0], [0, 0, 0, 2]], float); rhs = np.array([a, b, -(c + 2 * x_act), 3.76 * 2 * x_act + d], float)
    rhs[3] = 2 * 3.76 * x_act + d; sol_np = np.linalg.solve(np.array([[1, 0, 0, 0], [0, 2, 0, 0], [2, 1, 2, 0], [0, 0, 0, 2]], float), np.array([a, b, c + 2 * x_act, d + 2 * 3.76 * x_act]))
    assert np.allclose(sol_np, [nCO2v, nH2Ov, nO2v, nN2v], atol=1e-9), (sol_np, nCO2v, nH2Ov, nO2v, nN2v)
    tot = nCO2v + nH2Ov + nO2v + nN2v
    Mf = a * ATOM['C'] + b * ATOM['H'] + c * ATOM['O'] + d * ATOM['N']
    m_air = x_act * 4.76 * 28.97
    case(f'comb-{a}-{b}-{c}-{d}-{ex}', 'combustion', dict(a=a, b=b, c=c, d=d, excess=ex, Pprod=100),
         {'co2': nCO2v, 'h2o': nH2Ov, 'o2': nO2v, 'n2': nN2v, 'tot': tot, 'ath': (st, 1e-9), 'nO2': x_act, 'AFmol': x_act * 4.76, 'AFmass': (m_air / Mf, 1e-9 * m_air / Mf), 'Mf': (Mf, 1e-9 * Mf),
          'Pv': (100 * nH2Ov / tot, 1e-9 * 100), 'y.co2': nCO2v / tot, 'y.h2o': nH2Ov / tot, 'y.n2': nN2v / tot, 'y.o2': nO2v / tot},
         'sympy linear system of C, H, O, N balances (+ numpy solve), AF from masses')
    # mass conservation of the whole reaction: kg of reactants = kg of products (independent check of the coefficients and of the masses)
    m_react = Mf + x_act * (2 * ATOM['O']) + x_act * 3.76 * (2 * ATOM['N'])
    m_prod = nCO2v * (ATOM['C'] + 2 * ATOM['O']) + nH2Ov * (2 * ATOM['H'] + ATOM['O']) + nO2v * 2 * ATOM['O'] + nN2v * 2 * ATOM['N']
    assert abs(m_react - m_prod) < 1e-8 * m_react, ('mass balance', a, b, c, d, ex)
    case(f'comb-mass-{a}-{b}-{c}-{d}-{ex}', 'combustion', dict(a=a, b=b, c=c, d=d, excess=ex), {'mProducts.co2': nCO2v * (ATOM['C'] + 2 * ATOM['O']), 'mProducts.h2o': nH2Ov * (2 * ATOM['H'] + ATOM['O'])}, 'mass conservation asserted in Python (reactants = products)')

# molar masses printed in Appendix 1 (images checked: Table A-1 p.910 and Table A-27 p.951); rounding of the atomic masses < 0.0015 kg/kmol
for name, (a, b, c, d), Mp in [('CH4', (1, 4, 0, 0), 16.043), ('C2H6', (2, 6, 0, 0), 30.070), ('C3H8', (3, 8, 0, 0), 44.097), ('C8H18', (8, 18, 0, 0), 114.231), ('CH3OH', (1, 4, 1, 0), 32.042),
                               ('C2H5OH', (2, 6, 1, 0), 46.069), ('H2', (0, 2, 0, 0), 2.016), ('CO2', (1, 0, 2, 0), 44.01), ('H2O', (0, 2, 1, 0), 18.015), ('N2', (0, 0, 0, 2), 28.013), ('O2', (0, 0, 2, 0), 31.999), ('C(s)', (1, 0, 0, 0), 12.011)]:
    refs.append({'id': f'M-{name}', 'fn': 'molarMass', 'args': dict(a=a, b=b, c=c, d=d), 'argvobj': True, 'expect': {'': [Mp, 0.0015]}, 'src': 'Appendix 1 Table A-1 / A-27 (printed kg/kmol)'})

# ============================================================ references from the checked QA files
tut = json.load(open(os.path.join(QA, 'tut.json'), encoding='utf-8'))['numeric']
ch2 = json.load(open(os.path.join(QA, 'ch2.json'), encoding='utf-8'))
ch4 = json.load(open(os.path.join(QA, 'ch4.json'), encoding='utf-8'))['numeric']
ch5 = json.load(open(os.path.join(QA, 'ch5.json'), encoding='utf-8'))['numeric']


def find(rows, prob=None, item=None, page=None, startswith=False):
    out = [r for r in rows if (prob is None or r.get('problem') == prob) and (item is None or (r['item'].startswith(item) if startswith else r['item'] == item)) and (page is None or r['page'] == page)]
    assert len(out) == 1, (prob, item, page, len(out))
    return out[0]


def ref(rows, key, label_vi, label_en, unit, prob=None, item=None, page=None, startswith=False, use='recomputed', factor=1.0, tol=None, rel=1e-4, startsw=False):
    r = find(rows, prob, item, page, startswith or startsw); v = r[use] * factor
    tl = tol if tol is not None else (r['tol'] * factor if r.get('tol') else rel * abs(v))
    tl = max(tl, 1e-9)
    return {'key': key, 'vi': label_vi, 'en': label_en, 'v': v, 'tol': tl, 'unit': unit, 'slide': r.get('slide')}


def add_example(ex_id, calc, title_vi, title_en, src_vi, src_en, args, rlist, note_vi='', note_en=''):
    examples.append({'id': ex_id, 'calc': calc, 'title': {'vi': title_vi, 'en': title_en}, 'src': {'vi': src_vi, 'en': src_en}, 'args': args, 'refs': rlist, 'note': {'vi': note_vi, 'en': note_en}})


# --- Otto: Tutorials I #3 (no printed solution: values recomputed by two routes in _qa/tut.json)
add_example('otto-tut3', 'otto', 'Tutorials I bài 3: r = 9,5; 100 kPa; 35 °C; 600 cm³; T₄ = 800 K', 'Tutorials I problem 3: r = 9.5; 100 kPa; 35 °C; 600 cm³; T₄ = 800 K',
            'Tutorials I tr.14 (đề, không có lời giải in); số tính lại bằng hai đường trong _qa/tut.json', 'Tutorials I p.14 (problem only, no printed solution); values recomputed by two routes in _qa/tut.json',
            dict(r=9.5, T1=308, P1=100, mode='T4', T4=800, k=1.4, R=0.287, cv=0.718, V1=0.0006),
            [ref(tut, 'T2', '$T_2$', '$T_2$', 'K', prob='P3 Otto', item='T2 [T1=308]'),
             ref(tut, 'P2', '$P_2$', '$P_2$', 'kPa', prob='P3 Otto', item='P2 [T1=308]'), ref(tut, 'T3', '$T_3$', '$T_3$', 'K', prob='P3 Otto', item='T3 = Tmax [T1=308]'),
             ref(tut, 'P3', '$P_3$', '$P_3$', 'kPa', prob='P3 Otto', item='P3 = Pmax [T1=308]'), ref(tut, 'Qin', '$Q_{in}$', '$Q_{in}$', 'kJ', prob='P3 Otto', item='Q_in [T1=308]'),
             ref(tut, 'Wnet', '$W_{net}$', '$W_{net}$', 'kJ', prob='P3 Otto', item='W_net [T1=308]'), ref(tut, 'eta', '$\\eta_{th}$', '$\\eta_{th}$', '', prob='P3 Otto', item='eta_th [T1=308]'),
             ref(tut, 'mep', 'MEP', 'MEP', 'kPa', prob='P3 Otto', item='MEP [T1=308]')],
            'Đề không in c_v, R: dùng 0,718 và 0,287 (Appendix 1 Table A-2 (a)); 35 °C lấy 308 K (308,15 K đổi P₃ 3 kPa và MEP 0,08 %).', 'The problem prints neither c_v nor R: 0.718 and 0.287 are used (Appendix 1 Table A-2 (a)); 35 °C is taken as 308 K (308.15 K shifts P₃ by 3 kPa and MEP by 0.08 %).')
sens = find(tut, prob='P1 Otto', item='cold-air (k=1.4, cv=0.718) T2, T3, P3')
p3cold = float(re.search(r'P3=(\d+) kPa', sens['how']).group(1))
cold_eta = find(tut, prob='P1 Otto', item='eta cold-air = 1-r^(1-k)')
add_example('otto-tut1-cold', 'otto', 'Tutorials I bài 1 theo khí lạnh: r = 8; 290 K; 100 kPa; q_in = 800 kJ/kg', 'Tutorials I problem 1 as cold-air: r = 8; 290 K; 100 kPa; q_in = 800 kJ/kg',
            'Tutorials I tr.1–6: η khí lạnh 0,565 in trên slide; T₂, T₃, P₃ tính lại (_qa/tut.json)', 'Tutorials I p.1–6: cold-air η = 0.565 printed on the slide; T₂, T₃, P₃ recomputed (_qa/tut.json)',
            dict(r=8, T1=290, P1=100, mode='qin', qin=800, k=1.4, R=0.287, cv=0.718),
            [{'key': 'T2', 'vi': '$T_2$', 'en': '$T_2$', 'v': sens['recomputed'], 'tol': 0.05, 'unit': 'K'}, {'key': 'T3', 'vi': '$T_3$', 'en': '$T_3$', 'v': sens['recomputed_B'], 'tol': 0.1, 'unit': 'K'},
             {'key': 'P3', 'vi': '$P_3$', 'en': '$P_3$', 'v': p3cold, 'tol': 1.0, 'unit': 'kPa'},
             {'key': 'etaOtto', 'vi': '$\\eta_{Otto}=1-r^{1-k}$', 'en': '$\\eta_{Otto}=1-r^{1-k}$', 'v': cold_eta['slide'], 'tol': cold_eta['tol'], 'unit': ''}],
            'Slide giải bằng bảng khí (c_p biến thiên): η = 0,523, T₃ = 1575 K; khí lạnh cho 0,565 và 1780 K, lệch 13 %: hai cách KHÔNG cho cùng số.', 'The slide solves it with gas tables (variable c_p): η = 0.523, T₃ = 1575 K; cold-air gives 0.565 and 1780 K, a 13 % gap: the two methods do NOT give the same numbers.')
# --- Otto: closed form η from ch2 computed_only (r = 7, 8, 10, 14)
for item in ch2['computed_only']:
    if item['item'].startswith('Otto eta r='):
        r_ = float(item['item'].split('=')[1])
        refs.append({'id': f'ch2-otto-eta-{r_}', 'fn': 'otto', 'args': dict(r=r_, T1=300, P1=100, mode='T3', T3=1800, k=1.4, R=0.287), 'expect': {'etaOtto': [item['closed_k1p4'], 6e-5], 'eta': [item['closed_k1p4'], 6e-5]},
                     'src': f'_qa/ch2.json computed_only "{item["item"]}" (closed form k = 1.4, slide Ch.2 tr.24)'})
for pg, r_ in ((25, 8), (25, 10), (25, 6), (25, 14)):
    it = find(ch2['numeric'], item=f'Otto eta (do thi p25) r={r_}, k=1.4', page=pg)
    refs.append({'id': f'ch2-otto-graph-{r_}', 'fn': 'otto', 'args': dict(r=r_, T1=300, P1=100, mode='T3', T3=1800, k=1.4, R=0.287), 'expect': {'etaOtto': [it['slide'], it['tol']]}, 'src': 'Slide Ch.2 tr.25 (curve read, tolerance of the reading)'})

# --- Diesel #2 (cp, cv constants of the slide; SI conversion psia -> kPa x 6.894757, R -> K /1.8, Btu/lbm-R -> kJ/kg-K x 4.1868)
psi, rk, BTU = 6.894757, 1 / 1.8, 4.1868
D2 = lambda item, **kw: ref(tut, prob='P2 Diesel', item=item, **kw)
k_ = 5.0 / 9.0
add_example('diesel-tut2', 'diesel', 'Tutorials I bài 2: r = 18; r_c = 2; 14,7 psia; 80 °F; 117 in³ (đã đổi SI)', 'Tutorials I problem 2: r = 18; r_c = 2; 14.7 psia; 80 °F; 117 in³ (converted to SI)',
            'Tutorials I tr.7–13 (có lời giải, đổi sang SI: 1 psia = 6,894757 kPa; K = °R/1,8; 1 Btu/lbm·R = 4,1868 kJ/kg·K)', 'Tutorials I p.7–13 (printed solution, converted to SI: 1 psia = 6.894757 kPa; K = °R/1.8; 1 Btu/lbm·R = 4.1868 kJ/kg·K)',
            dict(r=18, rc=2, mode='rc', T1=300, P1=round(14.7 * psi, 4), k=1.4, R=0.287, cp=round(0.24 * BTU, 6), cv=round(0.171 * BTU, 6), V1=round(117 * 0.0254 ** 3, 9)),
            [D2('T2', key='T2', label_vi='', label_en='', unit='K', factor=rk, tol=0.5 * rk) | {'vi': '$T_2$', 'en': '$T_2$'}, D2('T3', key='T3', label_vi='', label_en='', unit='K', factor=rk, tol=1.0 * rk) | {'vi': '$T_3$', 'en': '$T_3$'},
             D2('T4', key='T4', label_vi='', label_en='', unit='K', factor=rk, tol=0.5 * rk) | {'vi': '$T_4$', 'en': '$T_4$'}, D2('P2 = P3', key='P2', label_vi='', label_en='', unit='kPa', factor=psi, tol=0.5 * psi) | {'vi': '$P_2=P_3$', 'en': '$P_2=P_3$'},
             D2('P4', key='P4', label_vi='', label_en='', unit='kPa', factor=psi, tol=0.05 * psi) | {'vi': '$P_4$', 'en': '$P_4$'},
             D2('eta_th', key='eta', label_vi='', label_en='', unit='', tol=0.0006) | {'vi': '$\\eta_{th}$ (nhiệt cp, cv)', 'en': '$\\eta_{th}$ (heats with c_p, c_v)'},
             D2('MEP', key='mep', label_vi='', label_en='', unit='kPa', factor=psi, tol=0.6 * psi) | {'vi': 'MEP', 'en': 'MEP'}],
            'Slide dùng k = 1,4 cho nhiệt độ/áp suất nhưng c_p = 0,240, c_v = 0,171 (c_p/c_v = 1,4035) cho nhiệt lượng; công thức η(r, r_c, k) chính xác cho 0,6316, slide in 0,632. Slide ghi hằng số "ở 77 °F" nhưng dùng 80 °F.',
            'The slide uses k = 1.4 for temperatures/pressures but c_p = 0.240, c_v = 0.171 (c_p/c_v = 1.4035) for the heats; the exact formula η(r, r_c, k) gives 0.6316, the slide prints 0.632. The slide says the constants are "at 77 °F" but uses 80 °F.')
# W_net and Q_in totals of #2 in kJ (Btu x 1.055056)
BTUJ = 1.055056
refs.append({'id': 'tut2-W', 'fn': 'diesel', 'args': examples[-1]['args'], 'expect': {'Wnet': [find(tut, prob='P2 Diesel', item='W_net')['recomputed'] * BTUJ, 0.002 * BTUJ], 'Qin': [find(tut, prob='P2 Diesel', item='Q_in = m cp (T3-T2)')['recomputed'] * BTUJ, 0.002 * BTUJ]}, 'src': 'Tutorials I tr.11–13 (Btu x 1.055056 kJ/Btu)'})
D6 = lambda item, **kw: ref(tut, prob='P6 Diesel', item=item + ' [T1=293 K]', **kw)
add_example('diesel-tut6', 'diesel', 'Tutorials I bài 6: r = 20; 95 kPa; 20 °C; T_max = 2200 K', 'Tutorials I problem 6: r = 20; 95 kPa; 20 °C; T_max = 2200 K',
            'Tutorials I tr.17 (đề, không có lời giải in); số tính lại hai đường trong _qa/tut.json', 'Tutorials I p.17 (problem only); values recomputed by two routes in _qa/tut.json',
            dict(r=20, T1=293, P1=95, mode='T3', T3=2200, k=1.4, R=0.287, cp=1.005, cv=0.718),
            [D6('T2', key='T2', label_vi='', label_en='', unit='K', tol=0.05) | {'vi': '$T_2$', 'en': '$T_2$'}, D6('r_c = T3/T2', key='rc', label_vi='', label_en='', unit='', tol=0.001) | {'vi': '$r_c=T_3/T_2$', 'en': '$r_c=T_3/T_2$'},
             D6('q_in', key='qin', label_vi='', label_en='', unit='kJ/kg', tol=0.1) | {'vi': '$q_{in}$', 'en': '$q_{in}$'}, D6('(a) eta_th', key='etaDiesel', label_vi='', label_en='', unit='', tol=0.0002) | {'vi': '$\\eta_{Diesel}(r,r_c,k)$', 'en': '$\\eta_{Diesel}(r,r_c,k)$'},
             D6('(b) MEP', key='mep', label_vi='', label_en='', unit='kPa', tol=1.0) | {'vi': 'MEP', 'en': 'MEP'}],
            'Đề không in c_p, c_v, R, k: dùng Appendix 1 Table A-2 (a) (1,005; 0,718; 0,287; 1,4). Số tham chiếu ghi MEP 932,9 kPa (đường B: 932,4).', 'The problem prints no c_p, c_v, R, k: Appendix 1 Table A-2 (a) is used (1.005; 0.718; 0.287; 1.4). The reference MEP is 932.9 kPa (route B: 932.4).')
add_example('diesel-ch2-12', 'diesel', 'Slide Ch.2 tr.31: r = 12, r_c = 2, k = 1,4 (công thức η)', 'Slide Ch.2 p.31: r = 12, r_c = 2, k = 1.4 (η formula)',
            'Slide Ch.2 tr.31; η tính lại bằng công thức đóng (_qa/ch2.json, computed_only)', 'Slide Ch.2 p.31; η recomputed by the closed form (_qa/ch2.json, computed_only)',
            dict(r=12, rc=2, mode='rc', T1=300, P1=100, k=1.4, R=0.287),
            [{'key': 'etaDiesel', 'vi': '$\\eta_{Diesel}$', 'en': '$\\eta_{Diesel}$', 'v': [i for i in ch2['computed_only'] if i['item'].startswith('Diesel r=12')][0]['closed_k1p4'], 'tol': 6e-5, 'unit': ''}],
            'T₁ = 300 K và P₁ = 100 kPa là giả thiết của người kiểm tra (η không phụ thuộc chúng).', 'T₁ = 300 K and P₁ = 100 kPa are the checker\'s assumptions (η does not depend on them).')
cold5 = find(tut, prob='P5 Diesel', item='cold-air eta (k=1.4) for comparison')
add_example('diesel-tut5-cold', 'diesel', 'Tutorials I bài 5 theo khí lạnh: r = 16, r_c = 2, 95 kPa, 27 °C', 'Tutorials I problem 5 as cold-air: r = 16, r_c = 2, 95 kPa, 27 °C',
            'Tutorials I tr.16: slide giải bằng bảng khí (η = 0,563); η khí lạnh tính lại (_qa/tut.json)', 'Tutorials I p.16: the slide uses gas tables (η = 0.563); the cold-air η is recomputed (_qa/tut.json)',
            dict(r=16, rc=2, mode='rc', T1=300, P1=95, k=1.4, R=0.287),
            [{'key': 'etaDiesel', 'vi': '$\\eta_{Diesel}$ (khí lạnh)', 'en': '$\\eta_{Diesel}$ (cold-air)', 'v': cold5['recomputed'], 'tol': 6e-5, 'unit': ''}],
            'Bảng khí (c_p biến thiên) cho 0,563: KHÔNG tái tạo được bằng k hằng.', 'Gas tables (variable c_p) give 0.563: NOT reproducible with a constant k.')

# --- Brayton (slide Ch.2 tr.40 and tr.45), closed form k = 1.4
cl = {i['item']: i for i in ch2['computed_only']}
b82 = cl['Brayton eta rp=8.2, T1=300,Tmax=1000']
add_example('brayton-ch2-40', 'brayton', 'Slide Ch.2 tr.40: T₁ = 300 K, T_max = 1000 K, r_p = 8,2 (cực đại w_net)', 'Slide Ch.2 p.40: T₁ = 300 K, T_max = 1000 K, r_p = 8.2 (maximum w_net)',
            'Slide Ch.2 tr.40 (r_p,opt = 8,2); số tính lại bằng công thức đóng và scipy (_qa/ch2.json)', 'Slide Ch.2 p.40 (r_p,opt = 8.2); recomputed by the closed form and scipy (_qa/ch2.json)',
            dict(rp=8.2, T1=300, T3=1000, k=1.4, R=0.287, etac=1, etat=1, eps=0, Nc=1, Nt=1),
            [{'key': 'rpOpt', 'vi': '$r_{p,opt}$', 'en': '$r_{p,opt}$', 'v': find(ch2['numeric'], item='rp (w_net max), Tmax/Tmin=1000/300, k=1.4')['recomputed'], 'tol': 0.0001, 'unit': ''},
             {'key': 'eta', 'vi': '$\\eta_{th}$ tại $r_p=8{,}2$', 'en': '$\\eta_{th}$ at $r_p=8.2$', 'v': b82['closed_k1p4'], 'tol': 6e-5, 'unit': ''}],
            'Slide ghi 8,2; công thức đóng cho 8,2231. Bảng khí (c_p biến thiên) cho 8,0 và CoolProp cho 9,1: cực đại rất phẳng (w_net tại 8,2 bằng 0,998 cực đại CoolProp). Đường cong η trên slide tr.40 cao hơn công thức k = 1,4 khi r_p ≥ 20 (0,63 so với 0,575).',
            'The slide says 8.2; the closed form gives 8.2231. Gas tables (variable c_p) give 8.0 and CoolProp 9.1: the maximum is very flat (w_net at 8.2 is 0.998 of the CoolProp maximum). The η curve on slide p.40 is above the k = 1.4 formula for r_p ≥ 20 (0.63 vs 0.575).')
r45 = cl['Regen eps=1 T1/T3=0.25, rp=8']
cross = find(ch2['numeric'], item="Regen: rp giao nhau voi 'without regen', T1/T3=0.25 (p45)")
add_example('brayton-ch2-45', 'brayton', 'Slide Ch.2 tr.45: hồi nhiệt lý tưởng ε = 1, T₁/T₃ = 0,25, r_p = 8', 'Slide Ch.2 p.45: ideal regeneration ε = 1, T₁/T₃ = 0.25, r_p = 8',
            'Slide Ch.2 tr.45 (đồ thị: giao điểm r_p ≈ 11,3); η và giao điểm tính lại bằng công thức đóng (_qa/ch2.json)', 'Slide Ch.2 p.45 (graph: crossing at r_p ≈ 11.3); η and crossing recomputed by the closed form (_qa/ch2.json)',
            dict(rp=8, T1=300, T3=1200, k=1.4, R=0.287, etac=1, etat=1, eps=1, Nc=1, Nt=1),
            [{'key': 'eta', 'vi': '$\\eta_{th}$ có hồi nhiệt', 'en': '$\\eta_{th}$ with regeneration', 'v': r45['closed_k1p4'], 'tol': 6e-5, 'unit': ''},
             {'key': 'rpCross', 'vi': '$r_p$ giao nhau', 'en': '$r_p$ crossing', 'v': cross['recomputed'], 'tol': 0.001, 'unit': ''}],
            'Giá trị slide đọc từ đồ thị (11,3), dung sai đọc 2.', 'The slide value is read from a graph (11.3), reading tolerance 2.')
for t_, it in ((0.2, 'T1/T3=0.2'), (0.25, 'T1/T3=0.25'), (0.33, 'T1/T3=0.33')):
    rc_ = find(ch2['numeric'], item=f"Regen: rp giao nhau voi 'without regen', {it} (p45)")
    refs.append({'id': f'ch2-cross-{t_}', 'fn': 'regenCrossover', 'args': dict(T1=t_, T3=1.0, k=1.4), 'argvobj': True, 'expect': {'': [rc_['recomputed'], 1e-3]}, 'src': 'slide Ch.2 tr.45, closed form in _qa/ch2.json'})
    refs.append({'id': f'ch2-cross-slide-{t_}', 'fn': 'regenCrossover', 'args': dict(T1=t_, T3=1.0, k=1.4), 'argvobj': True, 'expect': {'': [rc_['slide'], rc_['tol']]}, 'src': 'slide Ch.2 tr.45 read from the graph (tolerance of the reading)'})
for key_, rp_ in (('Brayton eta rp=2, T1=300,Tmax=1000', 2), ('Brayton eta rp=15, T1=300,Tmax=1000', 15)):
    refs.append({'id': f'ch2-brayton-{rp_}', 'fn': 'brayton', 'args': dict(rp=rp_, T1=300, T3=1000, k=1.4, R=0.287), 'expect': {'eta': [cl[key_]['closed_k1p4'], 6e-5]}, 'src': '_qa/ch2.json computed_only (closed form)'})
refs.append({'id': 'ch2-regen-0.2', 'fn': 'brayton', 'args': dict(rp=10, T1=300, T3=1500, k=1.4, R=0.287, eps=1), 'expect': {'eta': [cl['Regen eps=1 T1/T3=0.2, rp=10']['closed_k1p4'], 6e-5]}, 'src': '_qa/ch2.json computed_only (closed form)'})
refs.append({'id': 'ch2-rpopt', 'fn': 'braytonOptRp', 'args': dict(T1=300, T3=1000, k=1.4), 'argvobj': True, 'expect': {'rp': [8.2231, 0.0001]}, 'src': '_qa/ch2.json (sympy, scipy, closed form agree: 8.2231; the slide prints 8.2)'})

# --- Isentropic flow examples
add_example('flow-ma-2', 'flow_ma', 'Appendix 1 Table A-32: Ma = 2,0, k = 1,4', 'Appendix 1 Table A-32: Ma = 2.0, k = 1.4', 'Appendix 1 Table A-32 (in 4 chữ số thập phân)', 'Appendix 1 Table A-32 (printed to 4 decimals)',
            dict(k=1.4, Ma=2), [{'key': 'TT0', 'vi': '$T/T_0$', 'en': '$T/T_0$', 'v': 0.5556, 'tol': 6e-5, 'unit': ''}, {'key': 'PP0', 'vi': '$P/P_0$', 'en': '$P/P_0$', 'v': 0.1278, 'tol': 6e-5, 'unit': ''},
                                {'key': 'rr0', 'vi': '$\\rho/\\rho_0$', 'en': '$\\rho/\\rho_0$', 'v': 0.2300, 'tol': 6e-5, 'unit': ''}, {'key': 'AAs', 'vi': '$A/A^*$', 'en': '$A/A^*$', 'v': 1.6875, 'tol': 6e-5, 'unit': ''}])
add_example('flow-ma-3', 'flow_ma', 'Appendix 1 Table A-32: Ma = 3,0 (có ô in sai của sách)', 'Appendix 1 Table A-32: Ma = 3.0 (has a misprinted cell)', 'Appendix 1 Table A-32; _qa/ch5.json (ρ/ρ₀ đúng 0,0762)', 'Appendix 1 Table A-32; _qa/ch5.json (correct ρ/ρ₀ is 0.0762)',
            dict(k=1.4, Ma=3), [{'key': 'TT0', 'vi': '$T/T_0$', 'en': '$T/T_0$', 'v': 0.3571, 'tol': 6e-5, 'unit': ''}, {'key': 'PP0', 'vi': '$P/P_0$', 'en': '$P/P_0$', 'v': 0.0272, 'tol': 6e-5, 'unit': ''},
                                {'key': 'rr0', 'vi': '$\\rho/\\rho_0$ (giá trị đúng)', 'en': '$\\rho/\\rho_0$ (correct value)', 'v': 0.0762, 'tol': 6e-5, 'unit': ''}, {'key': 'AAs', 'vi': '$A/A^*$', 'en': '$A/A^*$', 'v': 4.2346, 'tol': 6e-5, 'unit': ''}],
            'Bảng A-32 in ρ/ρ₀ = 0,0760 tại Ma = 3,0; công thức cho 0,07623: ô này in sai (lệch 2,3×10⁻⁴, lớn hơn nửa đơn vị làm tròn).', 'Table A-32 prints ρ/ρ₀ = 0.0760 at Ma = 3.0; the formula gives 0.07623: that cell is misprinted (off by 2.3×10⁻⁴, more than half a rounding unit).')
duct_rows = lambda it, **kw: ref(ch5, item=it, **kw)
add_example('flow-aas-duct', 'flow_aas', 'Slide Ch.5 tr.57–59: Ma₁ = 0,3; A₂/A₁ = 0,8; T₁ = 400 K; P₁ = 100 kPa (dưới âm)', 'Slide Ch.5 p.57–59: Ma₁ = 0.3; A₂/A₁ = 0.8; T₁ = 400 K; P₁ = 100 kPa (subsonic)',
            'Slide Ch.5 tr.57–59; số đã tính lại bằng hai đường (_qa/ch5.json)', 'Slide Ch.5 p.57–59; values recomputed by two routes (_qa/ch5.json)',
            dict(k=1.4, mode='Ma1', Ma1=0.3, A2A1=0.8, branch='sub', T1=400, P1=100),
            [{'key': 'A1s', 'vi': '$A_1/A^*$', 'en': '$A_1/A^*$', 'v': 2.0351, 'tol': 6e-5, 'unit': ''}, {'key': 'T1T0', 'vi': '$T_1/T_0$', 'en': '$T_1/T_0$', 'v': 0.9823, 'tol': 6e-5, 'unit': ''},
             {'key': 'P1P0', 'vi': '$P_1/P_0$', 'en': '$P_1/P_0$', 'v': 0.9395, 'tol': 6e-5, 'unit': ''}, {'key': 'A2s', 'vi': '$A_2/A^*$', 'en': '$A_2/A^*$', 'v': 1.6281, 'tol': 2e-4, 'unit': ''},
             duct_rows('p58 Ma2 (subsonic root)', key='Ma2', label_vi='', label_en='', unit='', tol=1e-4) | {'vi': '$Ma_2$ (giá trị đã tính lại)', 'en': '$Ma_2$ (recomputed value)'},
             duct_rows('p58 T2/T0', key='T2T0', label_vi='', label_en='', unit='', tol=1e-4) | {'vi': '$T_2/T_0$', 'en': '$T_2/T_0$'}, duct_rows('p58 P2/P0', key='P2P0', label_vi='', label_en='', unit='', tol=1e-4) | {'vi': '$P_2/P_0$', 'en': '$P_2/P_0$'},
             duct_rows('p59 T2', key='T2', label_vi='', label_en='', unit='K', tol=0.05) | {'vi': '$T_2$', 'en': '$T_2$'}, duct_rows('p59 P2', key='P2', label_vi='', label_en='', unit='kPa', tol=0.02) | {'vi': '$P_2$', 'en': '$P_2$'}],
            'LỖI SLIDE: slide in Ma₂ = 0,391; T₂/T₀ = 0,9701; P₂/P₀ = 0,8993; P₂ = 95,7 kPa (nội suy tuyến tính trong bảng thô). Giá trị đúng: 0,3887; 0,9707; 0,9011; 95,91 kPa. T₁ = 400 K và P₁ = 100 kPa suy ra từ T₂ = 395 K và P₂ của slide.',
            'SLIDE ERROR: the slide prints Ma₂ = 0.391; T₂/T₀ = 0.9701; P₂/P₀ = 0.8993; P₂ = 95.7 kPa (linear interpolation in a coarse table). Correct values: 0.3887; 0.9707; 0.9011; 95.91 kPa. T₁ = 400 K and P₁ = 100 kPa are inferred from the slide\'s T₂ = 395 K and P₂.')
sup25 = find(ch5, item='p49 chart: supersonic Ma at A/A*=25 (graph reads ~4.3-4.35)')
add_example('flow-aas-25', 'flow_aas', 'Slide Ch.5 tr.49: A/A* = 25, nhánh trên âm', 'Slide Ch.5 p.49: A/A* = 25, supersonic branch', 'Appendix 1 Table A-32 hàng Ma = 5,0 (A/A* = 25,000); _qa/ch5.json', 'Appendix 1 Table A-32 row Ma = 5.0 (A/A* = 25.000); _qa/ch5.json',
            dict(k=1.4, mode='A1s', A1s=25, branch='sup'), [{'key': 'Ma2', 'vi': '$Ma$', 'en': '$Ma$', 'v': sup25['recomputed'], 'tol': 1e-3, 'unit': ''}],
            'LỖI SLIDE: đồ thị M–A/A* trên tr.49 cho Ma ≈ 4,3 tại A/A* = 25; đúng là 5,000 (bảng A-32).', 'SLIDE ERROR: the M–A/A* chart on p.49 reads Ma ≈ 4.3 at A/A* = 25; the correct value is 5.000 (Table A-32).')
PR = lambda item, **kw: ref(ch5, item=item, **kw)
add_example('flow-pr-co2', 'flow_pr', 'Slide Ch.5 tr.22: CO₂, P₀ = 1400 kPa, T₀ = 473 K, ṁ = 3 kg/s, tại P = 1200 kPa', 'Slide Ch.5 p.22: CO₂, P₀ = 1400 kPa, T₀ = 473 K, ṁ = 3 kg/s, at P = 1200 kPa',
            'Slide Ch.5 tr.22 (k = 1,289; R = 0,1889 kJ/kg·K: Appendix 1 Table A-2 (a), A-1); số đã tính lại (_qa/ch5.json)', 'Slide Ch.5 p.22 (k = 1.289; R = 0.1889 kJ/kg·K: Appendix 1 Table A-2 (a), A-1); values recomputed (_qa/ch5.json)',
            dict(k=1.289, R=0.1889, mode='abs', P=1200, P0=1400, T0=473, mdot=3),
            [PR('p22 P=1200 kPa T', key='T', label_vi='', label_en='', unit='K', tol=0.5) | {'vi': '$T$', 'en': '$T$'}, PR('p22 P=1200 kPa rho', key='rho', label_vi='', label_en='', unit='kg/m3', tol=0.1) | {'vi': '$\\rho$', 'en': '$\\rho$'},
             PR('p22 P=1200 kPa c', key='c', label_vi='', label_en='', unit='m/s', tol=1.0) | {'vi': '$c$', 'en': '$c$'}, PR('p22 P=1200 kPa Ma', key='Ma', label_vi='', label_en='', unit='', tol=0.0015) | {'vi': 'Ma', 'en': 'Ma'},
             PR('p22 P=1200 kPa V', key='V', label_vi='', label_en='', unit='m/s', tol=0.6) | {'vi': '$V$', 'en': '$V$'}, PR('p22 P=1200 kPa A', key='A_cm2', label_vi='', label_en='', unit='cm2', tol=0.1) | {'vi': '$A$ (cm²)', 'en': '$A$ (cm²)'}],
            'Slide dùng c_p = 0,846 (bảng) nhưng kR/(k−1) = 0,8426: V lệch 0,2 %. Trong phạm vi làm tròn của slide.', 'The slide uses c_p = 0.846 (table) but kR/(k−1) = 0.8426: V differs by 0.2 %. Within the slide\'s rounding.')
add_example('flow-stag-aircraft', 'flow_stag', 'Slide Ch.5 tr.11–13: máy bay 250 m/s, T = 255,7 K, P = 54,05 kPa', 'Slide Ch.5 p.11–13: aircraft at 250 m/s, T = 255.7 K, P = 54.05 kPa', 'Slide Ch.5 tr.11–13; số đã tính lại bằng hai đường (_qa/ch5.json)', 'Slide Ch.5 p.11–13; values recomputed by two routes (_qa/ch5.json)',
            dict(k=1.4, R=0.287, T=255.7, P=54.05, V=250),
            [PR('p11 T01', key='T0', label_vi='', label_en='', unit='K', tol=0.1) | {'vi': '$T_0$', 'en': '$T_0$'}, PR('p12 P01', key='P0', label_vi='', label_en='', unit='kPa', tol=0.05) | {'vi': '$P_0$', 'en': '$P_0$'},
             PR('p12 dT = T01-T1', key='dT', label_vi='', label_en='', unit='K', tol=0.1) | {'vi': '$T_0-T$', 'en': '$T_0-T$'}, PR('p12 dP = P01-P1', key='dP', label_vi='', label_en='', unit='kPa', tol=0.05) | {'vi': '$P_0-P$', 'en': '$P_0-P$'}],
            'c_p = kR/(k−1) = 1,0045 kJ/kg·K (đường tham chiếu dùng 1,005: lệch 0,01 K).', 'c_p = kR/(k−1) = 1.0045 kJ/kg·K (the reference route uses 1.005: 0.01 K apart).')
add_example('flow-crit-co2', 'flow_crit', 'Slide Ch.5 tr.37–38: CO₂ (k = 1,289), P₀ = 1400 kPa, T₀ = 473 K, họng A* = 9,608 cm²', 'Slide Ch.5 p.37–38: CO₂ (k = 1.289), P₀ = 1400 kPa, T₀ = 473 K, throat A* = 9.608 cm²',
            'Slide Ch.5 tr.37–38 và tr.22 (ṁ = 3 kg/s đề cho; A* = 9,608 cm² tính lại ở _qa/ch5.json)', 'Slide Ch.5 p.37–38 and p.22 (ṁ = 3 kg/s given; A* = 9.608 cm² recomputed in _qa/ch5.json)',
            dict(k=1.289, R=0.1889, P0=1400, T0=473, Astar=9.608e-4),
            [PR('p37 T*/T0', key='TsT0', label_vi='', label_en='', unit='', tol=6e-5) | {'vi': '$T^*/T_0$', 'en': '$T^*/T_0$'}, PR('p37 P*/P0', key='PsP0', label_vi='', label_en='', unit='', tol=6e-5) | {'vi': '$P^*/P_0$', 'en': '$P^*/P_0$'},
             PR('p38 T*', key='Tstar', label_vi='', label_en='', unit='K', tol=0.5) | {'vi': '$T^*$', 'en': '$T^*$'}, PR('p38 P*', key='Pstar', label_vi='', label_en='', unit='kPa', tol=0.5) | {'vi': '$P^*$', 'en': '$P^*$'},
             {'key': 'mdot', 'vi': 'lưu lượng nghẹt $\\dot m$ (đề cho 3 kg/s)', 'en': 'choked flow $\\dot m$ (given 3 kg/s)', 'v': 3.0, 'tol': 0.03, 'unit': 'kg/s'}])
NZ = lambda item, **kw: ref(ch5, item=item, **kw)
add_example('flow-noz-a', 'flow_noz', 'Slide Ch.5 tr.51–54: không khí 873 K, 1 MPa, 150 m/s; A = 50 cm²; P_b = 700 kPa', 'Slide Ch.5 p.51–54: air at 873 K, 1 MPa, 150 m/s; A = 50 cm²; P_b = 700 kPa', 'Slide Ch.5 tr.51–54; số đã tính lại (_qa/ch5.json)', 'Slide Ch.5 p.51–54; values recomputed (_qa/ch5.json)',
            dict(k=1.4, R=0.287, T=873, P=1000, V=150, Pb=700, Ae=0.005),
            [NZ('p51 T0i', key='T0', label_vi='', label_en='', unit='K', tol=0.5) | {'vi': '$T_0$', 'en': '$T_0$'}, {'key': 'P0', 'vi': '$P_0$', 'en': '$P_0$', 'v': find(ch5, item='p51 P0i')['recomputed'] * 1000, 'tol': 1.0, 'unit': 'kPa'},
             NZ('p52 Pb/P0 (a)', key='PbP0', label_vi='', label_en='', unit='', tol=0.0005) | {'vi': '$P_b/P_0$', 'en': '$P_b/P_0$'},
             NZ('p53 Mat at Pt/P0=0.670', key='Ma', label_vi='', label_en='', unit='', tol=0.001) | {'vi': '$Ma_e$', 'en': '$Ma_e$'},
             NZ('p53 rho_t', key='rho', label_vi='', label_en='', unit='kg/m3', tol=0.001) | {'vi': '$\\rho_e$', 'en': '$\\rho_e$'}, NZ('p54 mdot (a) not choked', key='mdot', label_vi='', label_en='', unit='kg/s', tol=0.02) | {'vi': '$\\dot m$', 'en': '$\\dot m$'}],
            'Slide làm tròn P_b/P₀ = 0,670 (đúng 0,6695) nên T_e = 788,5 K và V_e = 437,9 m/s của slide lệch nhẹ so với tính chặt (788,4 K; 438,7 m/s): hai đại lượng này không đưa vào so sánh.',
            'The slide rounds P_b/P₀ to 0.670 (exact 0.6695), so its T_e = 788.5 K and V_e = 437.9 m/s differ slightly from the exact chain (788.4 K; 438.7 m/s): these two are not compared.')
add_example('flow-noz-b', 'flow_noz', 'Slide Ch.5 tr.55: cùng vòi, P_b = 400 kPa (nghẹt)', 'Slide Ch.5 p.55: same nozzle, P_b = 400 kPa (choked)', 'Slide Ch.5 tr.54–55; giá trị đã tính lại 7,10 kg/s (KHÔNG dùng số nguyên văn 0,2246: slide thiếu hệ số √1000)', 'Slide Ch.5 p.54–55; recomputed value 7.10 kg/s (NOT the literal 0.2246: the slide omits the factor √1000)',
            dict(k=1.4, R=0.287, T=873, P=1000, V=150, Pb=400, Ae=0.005),
            [NZ('p54 Pb/P0 (b)', key='PbP0', label_vi='', label_en='', unit='', tol=0.0005) | {'vi': '$P_b/P_0$', 'en': '$P_b/P_0$'}, NZ('p55 mdot (b) choked', key='mdot', label_vi='', label_en='', unit='kg/s', tol=0.02) | {'vi': '$\\dot m$ (nghẹt)', 'en': '$\\dot m$ (choked)'},
             {'key': 'PcritP0', 'vi': '$P^*/P_0$', 'en': '$P^*/P_0$', 'v': find(ch5, item='p52 P*/P0 air k=1.4 (slide: Table 17-2)')['recomputed'], 'tol': 6e-5, 'unit': ''}],
            'LỖI SLIDE tr.55: biểu thức ṁ = A·P₀·√(k/RT₀)·(2/(k+1))^… in thiếu hệ số √1000 (kPa và kJ/kg·K): tính nguyên văn ra 0,2246; nhân đúng ra 7,10 kg/s (kết quả in 7,10 là đúng).',
            'SLIDE ERROR p.55: the expression ṁ = A·P₀·√(k/RT₀)·(2/(k+1))^… omits the factor √1000 (kPa and kJ/kg·K): evaluated literally it gives 0.2246; with the factor 7.10 kg/s (the printed result 7.10 is right).')

# --- Combustion examples
C4 = lambda item, **kw: ref(ch4, item=item, **kw)
add_example('comb-octane', 'comb', 'Slide Ch.4 tr.15–17: octan C₈H₁₈ với 60 % không khí thừa (160 % lý thuyết)', 'Slide Ch.4 p.15–17: octane C₈H₁₈ with 60 % excess air (160 % theoretical)', 'Slide Ch.4 tr.15–17; AF tính lại với M_kk = 28,97 và M = 114,231 (_qa/ch4.json)', 'Slide Ch.4 p.15–17; AF recomputed with M_air = 28.97 and M = 114.231 (_qa/ch4.json)',
            dict(a=8, b=18, c=0, d=0, excess=60, Pprod=100),
            [C4('p15 x (CO2)', key='co2', label_vi='', label_en='', unit='kmol', tol=1e-9) | {'vi': '$\\mathrm{CO_2}$', 'en': '$\\mathrm{CO_2}$'}, C4('p15 y (H2O)', key='h2o', label_vi='', label_en='', unit='kmol', tol=1e-9) | {'vi': '$\\mathrm{H_2O}$', 'en': '$\\mathrm{H_2O}$'},
             C4('p15 z (O2)', key='o2', label_vi='', label_en='', unit='kmol', tol=1e-9) | {'vi': '$\\mathrm{O_2}$', 'en': '$\\mathrm{O_2}$'}, C4('p15 w (N2)', key='n2', label_vi='', label_en='', unit='kmol', tol=1e-9) | {'vi': '$\\mathrm{N_2}$', 'en': '$\\mathrm{N_2}$'},
             C4('p16 mol khong khi', key='AFmol', label_vi='', label_en='', unit='kmol/kmol', tol=1e-9) | {'vi': '$AF$ (kmol/kmol)', 'en': '$AF$ (kmol/kmol)'},
             C4('p17 AF octane (28.97/114.231)', key='AFmass', label_vi='', label_en='', unit='kg/kg', tol=0.01) | {'vi': '$AF$ (kg/kg)', 'en': '$AF$ (kg/kg)'}],
            'Slide in AF = 24,2 (dùng M_kk = 29 và M = 114): với 28,97 và 114,231 ra 24,14; lệch 0,06 là do làm tròn khối lượng mol.', 'The slide prints AF = 24.2 (M_air = 29, M = 114): with 28.97 and 114.231 it is 24.14; the 0.06 gap is molar-mass rounding.')
add_example('comb-ethane', 'comb', 'Slide Ch.4 tr.29–31: etan C₂H₆ với 20 % không khí thừa', 'Slide Ch.4 p.29–31: ethane C₂H₆ with 20 % excess air', 'Slide Ch.4 tr.29–31; AF với M_kk = 28,97 và M = 30,070 (_qa/ch4.json)', 'Slide Ch.4 p.29–31; AF with M_air = 28.97 and M = 30.070 (_qa/ch4.json)',
            dict(a=2, b=6, c=0, d=0, excess=20, Pprod=100),
            [C4('p29 a_th', key='ath', label_vi='', label_en='', unit='kmol', tol=1e-9) | {'vi': '$a_{th}$', 'en': '$a_{th}$'}, C4('p29 N2 san pham', key='n2', label_vi='', label_en='', unit='kmol', tol=0.005) | {'vi': '$\\mathrm{N_2}$', 'en': '$\\mathrm{N_2}$'},
             C4('p29 O2 du', key='o2', label_vi='', label_en='', unit='kmol', tol=1e-9) | {'vi': '$\\mathrm{O_2}$', 'en': '$\\mathrm{O_2}$'}, C4('p31 N_prod', key='tot', label_vi='', label_en='', unit='kmol', tol=0.005) | {'vi': '$N_{prod}$', 'en': '$N_{prod}$'},
             C4('p30 AF ethane (28.97/30.070)', key='AFmass', label_vi='', label_en='', unit='kg/kg', tol=0.05) | {'vi': '$AF$ (kg/kg)', 'en': '$AF$ (kg/kg)'}, C4('p31 P_v', key='Pv', label_vi='', label_en='', unit='kPa', tol=0.01) | {'vi': '$P_v$ (hơi nước, P = 100 kPa)', 'en': '$P_v$ (water vapour, P = 100 kPa)'}],
            'Slide in AF = 19,3 (M_kk = 29); với 28,97 ra 19,26. Điểm sương T_dp = 52,3 °C của slide: CHƯA LÀM trên Lab (cần bộ tra thuộc tính P3).', 'The slide prints AF = 19.3 (M_air = 29); with 28.97 it is 19.26. The slide\'s dew point T_dp = 52.3 °C is NOT DONE in the Lab (needs the property library P3).')
add_example('comb-methane', 'comb', 'Slide Ch.4 tr.22: metan CH₄ cháy lý thuyết (không khí đủ)', 'Slide Ch.4 p.22: methane CH₄ stoichiometric combustion', 'Slide Ch.4 tr.22 (N₂ = 2 × 3,76 = 7,52 kmol); C, H cân bằng tay', 'Slide Ch.4 p.22 (N₂ = 2 × 3.76 = 7.52 kmol); C and H balanced by hand',
            dict(a=1, b=4, c=0, d=0, excess=0, Pprod=100),
            [C4('p22 N2 cua CH4 ly thuyet', key='n2', label_vi='', label_en='', unit='kmol', tol=1e-9) | {'vi': '$\\mathrm{N_2}$', 'en': '$\\mathrm{N_2}$'}, {'key': 'co2', 'vi': '$\\mathrm{CO_2}$', 'en': '$\\mathrm{CO_2}$', 'v': 1.0, 'tol': 1e-9, 'unit': 'kmol'},
             {'key': 'h2o', 'vi': '$\\mathrm{H_2O}$', 'en': '$\\mathrm{H_2O}$', 'v': 2.0, 'tol': 1e-9, 'unit': 'kmol'}])

# ---- clean example refs (labels), units
for ex in examples:
    for r_ in ex['refs']:
        r_.setdefault('vi', r_['key']); r_.setdefault('en', r_['key'])
        for kx in ('slide',): r_.pop(kx, None)

json.dump({'note': 'Generated by build/verify/verify_lab.py. cases: independent expectations (abs tolerance). refs: reference values of the checked sources. examples: worked examples shown on the Lab page (args use thermo.js keys and SI units; areas in m2).',
           'cases': cases, 'refs': refs, 'examples': examples}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'wrote {os.path.relpath(OUT, ROOT)}: {len(cases)} independent cases, {len(refs)} source refs, {len(examples)} worked examples')

# ============================================================ run the Node test
env = dict(os.environ)
node = shutil.which('node') or 'node'
if '--mutation' in sys.argv:
    src = open(os.path.join(ROOT, '_shared', 'thermo.js'), encoding='utf-8').read()
    muts = [('3.76 * nO2', '3.67 * nO2', 'N2 per O2 in air'), ('Math.pow(2 / (k + 1), (k + 1) / (2 * (k - 1)))', 'Math.pow(2 / (k + 1), (k + 1) / (2 * (k + 1)))', 'choked-flow exponent'), ('T1 * Math.pow(r, k - 1), P2', 'T1 * Math.pow(r, k), P2', 'Otto T2 exponent')]
    bad = 0
    for a, b, what in muts:
        assert src.count(a) >= 1, a
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, 'thermo.js'); open(p, 'w', encoding='utf-8').write(src.replace(a, b, 1))
            res = subprocess.run([node, os.path.join(ROOT, 'tests', 'lab_node_test.js')], env=dict(env, THERMO_PATH=p), capture_output=True, text=True)
            last = [l for l in res.stdout.strip().splitlines() if l.startswith('FAILS')][-1]
            print(f'MUTATION "{what}": exit={res.returncode}, {last[:100]}')
            if res.returncode == 0: bad += 1
    print('MUTATION TEST:', 'FAILED (a broken coefficient went unnoticed)' if bad else 'ok (every deliberate error was caught)')
    sys.exit(1 if bad else 0)
res = subprocess.run([node, os.path.join(ROOT, 'tests', 'lab_node_test.js')], env=env, capture_output=True, text=True)
print(res.stdout[-6000:] if len(res.stdout) > 6000 else res.stdout)
if res.stderr: print(res.stderr[-2000:])
print('FAILS: none' if res.returncode == 0 else 'FAILS: see above')
sys.exit(res.returncode)
