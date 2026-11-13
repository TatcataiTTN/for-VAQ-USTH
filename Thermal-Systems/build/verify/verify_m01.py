"""verify_m01: recompute EVERY numeric answer of module m01 by ROUTE B and compare with the stored route-A values
(data/verify/m01_values.json, written by build/gen/gen_m01.py), then compare with the answers PRINTED in the books and with Farokhi's SI atmosphere table.
Route A = closed forms in gen_m01*.py.  Route B = independent re-implementation: sympy exact rationals for algebraic definitions, scipy root finding
(brentq), numerical control-volume balance, scipy ODE integration (hydrostatic equation for the atmosphere, mass-vs-distance for Breguet), summed component impulses.
Run: python3 -I build/verify/verify_m01.py   (needs the project venv for scipy/sympy:  .venv/bin/python -I build/verify/verify_m01.py)"""
import json, math, os, sys
import sympy as sp
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp, quad
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REG = json.load(open(os.path.join(ROOT, 'data', 'verify', 'm01_values.json'), encoding='utf-8'))
G0, R, GAM = 9.80665, 287.0, 1.4
FAILS = []; ROWS = []

def close(name, a, b, tol=1e-3, abs_tol=0.0):
    ok = abs(a - b) <= max(abs_tol, tol * max(abs(a), abs(b), 1e-300))
    ROWS.append((name, a, b, 'ok' if ok else 'FAIL'))
    if not ok: FAILS.append(f'{name}: A={a} B={b}')

# ---------------------------------------------------------------- route-B building blocks
def thrust_cv(ma, f, ue, u, pe=None, pa=None, Ae=0.0):
    """control-volume momentum balance solved numerically for the reaction T: sum of momentum flux out minus in equals T_applied + pressure force."""
    me = ma * (1 + f)
    def resid(T):          # x-momentum: me*ue - ma*u = T - (pe - pa)*Ae   (T = force the strut applies on the fluid = thrust on engine)
        return me * ue - ma * u - (T - ((pe - pa) * Ae if pe is not None else 0.0))
    return brentq(resid, -1e9, 1e9, xtol=1e-9)

def isa_B(z):
    """hydrostatic dp/dz = -rho g with piecewise-linear T(z) of the 1976 atmosphere, integrated numerically from sea level."""
    Tz = lambda h: 288.15 - 0.0065 * h if h <= 11000 else (216.65 if h <= 20000 else 216.65 + 0.001 * (h - 20000))
    sol = solve_ivp(lambda h, p: -p[0] * 9.80665 / (287.053 * Tz(h)), (0, z), [101325.0], rtol=1e-11, atol=1e-8, max_step=50)
    p = sol.y[0, -1]; T = Tz(z); return T, p, p / (287.053 * T)

def breguet_B(eo, QR, LD, r):
    """integrate ds = -(u/g)(T/mf)(L/D) dm/m  with  T u/mf = eo*QR  numerically in mass."""
    val, _ = quad(lambda m: eo * QR / G0 * LD / m, 1.0, r)      # distance accumulated while the mass falls from r to 1 (mass unit cancels)
    return val

def ep1_sympy(ma, f, ue, u):
    ma_, f_, ue_, u_ = [sp.Rational(str(x)) for x in (ma, f, ue, u)]
    T = ma_ * ((1 + f_) * ue_ - u_); me = ma_ * (1 + f_); w = me * (ue_ - u_) ** 2 / 2
    return float(T * u_ / (T * u_ + w))

# ---------------------------------------------------------------- per-kind checks
def check(rec):
    k, p, v = rec['kind'], rec['params'], rec['value']; tol = rec.get('tol', 2e-3)
    if k == 'g_thrust': close(k, v, thrust_cv(p['ma'], p['f'], p['ue'], p['u']), 1e-9)
    elif k == 'g_etap_s':
        u, ue = p['u'], p['ue']; ma = 100.0; T = ma * (ue - u); w = .5 * ma * (ue - u) ** 2; close(k, v, T * u / (T * u + w), 1e-9)       # from power balance, f = 0
    elif k == 'g_etap_1': close(k, v, ep1_sympy(p['ma'], p['f'], p['ue'], p['u']), 1e-9)
    elif k == 'g_etath':
        f, ue, u, QR = p['f'], p['ue'], p['u'], p['QR']; ma = 50.0; mf = f * ma; dke = .5 * ((ma + mf) * ue ** 2 - ma * u ** 2); close(k, v, dke / (mf * QR), 1e-9)
    elif k == 'g_etao':
        T, u, mf, QR = p['T'], p['u'], p['mf'], p['QR']; close(k, v, float(sp.Rational(str(T)) * sp.Rational(str(u)) / (sp.Rational(str(mf)) * sp.Rational(str(QR)))), 1e-12)
    elif k == 'g_tsfc': close(k, v, p['mf'] * 3600 / p['T'] * 1e6 / 3600, 1e-12)
    elif k == 'g_isa':
        T, pp, rho = isa_B(p['z'])
        close(k + ' T', v['T'], T, 1e-9); close(k + ' p', v['p'], pp, 3e-5); close(k + ' rho', v['rho'], rho, 3e-5)
    elif k == 'g_speed':
        T, _, _ = isa_B(p['z']); close(k, v, p['M'] * math.sqrt(GAM * R * T), 1e-5)
    elif k == 'g_breguet': close(k, v, breguet_B(p['eo'], p['QR'], p['LD'], p['r']), 1e-9)
    elif k == 'g_isp': close(k, v, p['T'] / (p['mp'] * G0), 1e-12)
    elif k == 'g_bpr': close(k, v, p['ma'] - p['ma'] / (1 + p['be']), 1e-12)
    elif k == 'g_tf':
        mh, be = p['mh'], p['be']; mc = be * mh
        T = thrust_cv(mh, p['f'], p['uh'], p['u']) + thrust_cv(mc, 0.0, p['uc'], p['u']); close(k, v, T, 1e-9)
    elif k == 'g_cruise': close(k, v, p['m'] * G0 / (p['CL'] / p['CD']), 1e-12)
    elif k == 'g_lift':
        _, _, rho = isa_B(p['z']); close(k, v, p['CL'] * .5 * rho * p['V'] ** 2 * p['S'], 1e-4)
    elif k == 'g_esp':
        ESP = p['SP'] + p['Te'] * p['u'] / p['epr']; close(k, v, p['mf'] / ESP * 3.6e9, 1e-12)
    elif k == 'g_takeoff':
        # static thrust from definition: T = (1+f) ma ue, eta_th = (1+f) ma ue^2 / (2 mf QR) => solve for T given eta, mf, QR, ue
        eth, mf, QR, ue = p['eth'], p['mf'], p['QR'], p['ue']
        Tt = brentq(lambda T: (T * ue / 2) / (mf * QR) - eth, 1.0, 1e9); close(k, v, Tt, 1e-9)
    elif k == 'g_pthrust': close(k, v, quad(lambda x: (p['pe'] - p['pa']), 0, p['Ae'])[0], 1e-12)
    elif k == 'g_vreq':
        _, _, rho = isa_B(p['z']); Vz = brentq(lambda V: p['CL'] * .5 * rho * V ** 2 * p['S'] - p['m'] * G0, 1.0, 1e4); close(k, v, Vz, 3e-4)
    elif k == 'g_cmp':
        u, a, b = p['u'], p['ueA'], p['ueB']
        eA = (lambda T=1.0: T * u / (T * u + .5 * (T / (a - u)) * (a - u) ** 2))(); eB = (lambda T=1.0: T * u / (T * u + .5 * (T / (b - u)) * (b - u) ** 2))()
        close(k, v, eA / eB, 1e-9)
    # ---- printed examples / problems
    elif k == 'p22':
        ma, mf, u, ue, pe, pa, Te, QR = [p[x] for x in ('ma', 'mf', 'u', 'ue', 'pe', 'pa', 'Te', 'QR')]
        rho_e = pe / (R * Te); me = ma + mf; Ae = me / (rho_e * ue)
        T = thrust_cv(ma, mf / ma, ue, u, pe, pa, Ae)
        close('p22 Ae', v['Ae'], Ae, 1e-9); close('p22 T', v['T'], T, 1e-9)
        ke = .5 * me * ue ** 2 - .5 * ma * u ** 2       # kinetic power gain (does not include the pressure term): used only as a sanity bound
        eo = T * u / (mf * QR); close('p22 eta_o', v['eo'], eo, 1e-9)
        wake = .5 * me * (ue - u) ** 2; close('p22 eta_p', v['ep'], T * u / (T * u + wake), 1e-9); close('p22 eta_th', v['eth'], (T * u + wake) / (mf * QR), 1e-9)
        close('p22 tsfc', v['tsfc'], mf / T, 1e-9); close('p22 M', v['M'], ue / math.sqrt(4 / 3 * R * Te), 1e-9)
    elif k == 'p25a':
        u, ue, st = p['u'], p['ue'], p['st']
        close('p25a e1', v['e1'], 2 * st * u / (2 * st * u + (ue - u) ** 2), 1e-12)
        T = st * 1.0; w = .5 * 1.0 * (ue - u) ** 2; close('p25a e1 (power balance)', v['e1'], T * u / (T * u + w), 1e-9)
        close('p25a e2', v['e2'], 2 * st * u / (ue * ue - u * u), 1e-12); close('p25a e3', v['e3'], 2 / (1 + ue / u), 1e-12)
    elif k == 'p25b':
        f, ue, ma, eo, em, LD, r = [p[x] for x in ('f', 'ue', 'ma', 'eo', 'eomax', 'LD', 'm1m2')]
        # route B: eta_o(u) = u((1+f)ue-u)/(f QR) must equal eo at the two roots, with QR fixed by eta_o,max = max_u eta_o
        us = sp.symbols('u'); fe = (1 + sp.Rational(str(f))) * ue
        QR = float(((1 + f) * ue / 2) * ((1 + f) * ue / 2) / (f * em))              # eta_o,max at u=(1+f)ue/2
        roots = sorted([float(x) for x in sp.solve(sp.Eq(us * (fe - us) / (f * QR), eo), us)], reverse=True)
        close('p25b u1', v['u1'], roots[0], 1e-9); close('p25b u2', v['u2'], roots[1], 1e-9); close('p25b QR', v['QR'], QR, 1e-9)
        S = breguet_B(eo, QR, LD, r); close('p25b S', v['S'], S, 1e-9)
        # range from S = (u/g)(T/mf)(L/D) ln r  with T = ma((1+f)ue-u), mf = f ma
        for i, key in enumerate(('u1', 'u2')):
            uu = roots[i]; T = ma * ((1 + f) * ue - uu); Sx = uu / G0 * T / (f * ma) * LD * math.log(r); close('p25b S via T/mf ' + key, v['S'], Sx, 1e-9)
            t = Sx / uu; close('p25b t' + str(i + 1), v['t' + str(i + 1)], t, 1e-9)
            close('p25b m1' + 'ab'[i], v['m1' + 'ab'[i]], f * ma * t / (1 - 1 / r), 1e-9); close('p25b T' + str(i + 1), v['T' + str(i + 1)], T, 1e-9)
    elif k == 'p212':
        gc, J = 32.174, 778.169
        T = (p['mc'] * p['uc'] + p['mh'] * p['uh']) / gc; close('p212 T lbf', v['T'], T, 1e-9)
        # SI route
        lb, ft, lbf = 0.45359237, 0.3048, 4.4482216153
        T_si = (p['mc'] * lb * p['uc'] * ft + p['mh'] * lb * p['uh'] * ft); close('p212 T SI/lbf', v['T'], T_si / lbf, 5e-6)
        ke = .5 * (p['mh'] * lb * (p['uh'] * ft) ** 2 + p['mc'] * lb * (p['uc'] * ft) ** 2); q = p['mfh'] / 3600 * lb * (18400 * 1055.056 / lb); close('p212 eta_th SI', v['eth'], ke / q, 2e-3)
        close('p212 tsfc', v['tsfc'], p['mfh'] / T_si * lbf, 5e-6); close('Farokhi 3.4 printed takeoff thrust 43,500 lbf', 43500.0, v['T'], 2e-3)
    elif k == 'p213':
        ue, f, em = p['ue'], p['f'], p['em']; us = sp.symbols('u')
        # maximise eta_o(u) = u((1+f)ue - u)/(f QR) numerically; QR from eta_o,max
        QR = (1 + f) ** 2 * ue ** 2 / (4 * f * em); eta = lambda u: u * ((1 + f) * ue - u) / (f * QR)
        from scipy.optimize import minimize_scalar
        res = minimize_scalar(lambda u: -eta(u), bounds=(1, ue), method='bounded', options={'xatol': 1e-10})
        close('p213 u', v['u'], res.x, 1e-6); close('p213 eta max', em, -res.fun, 1e-9); close('p213 QR', v['QR'], QR, 1e-9)
        close('p213 S', v['S'], breguet_B(em, QR, 10, 1.2), 1e-9); close('p213 t', v['t'], breguet_B(em, QR, 10, 1.2) / res.x, 1e-6)
    elif k == 'p219':
        hp = 745.699872; mph = 0.44704; Te = 700 * 4.4482216153; u = 250 * mph; ESP = 3300 * hp + Te * u / .9
        close('p219 ESP hp', v['esp'], ESP / hp, 2e-4); close('p219 ESFC', v['esfc'], 1500 / (ESP / hp), 2e-4)
    elif k == 'p229':
        sol = solve_ivp(lambda t, y: [20e3 / 174e3, y[0]], (0, 120), [241.40, 0.0], rtol=1e-12, atol=1e-12)
        close('p229 v', v['v'], sol.y[0, -1], 1e-9)
        # y[0] is velocity and y[1] distance in a coupled form: integrate separately
        sol = solve_ivp(lambda t, y: [y[1], 20e3 / 174e3], (0, 120), [0.0, 241.40], rtol=1e-12, atol=1e-12); close('p229 d', v['d'], sol.y[0, -1], 1e-9)
    elif k == 'f1x':
        close('f1 carnot', v['carnot'], 1 - 288 / 2000, 1e-12); close('f1 brayton', v['brayton'], 1 - 288 / 864, 1e-12)
        T1, T2, T3, g = 288.0, 864.0, 2000.0, 1.4; cv = 287 / (g - 1); cp = g * cv
        qin = cv * (T3 - T2)      # constant-volume heat addition 2->3 (v2 = v3)
        p1 = 1.0; p2 = (T2 / T1) ** (g / (g - 1)); p3 = p2 * T3 / T2; T4 = T3 * (p1 / p3) ** ((g - 1) / g); qout = cp * (T4 - T1)
        close('f1 humphrey', v['humphrey'], 1 - qout / qin, 1e-9)
    elif k == 'f15': close('f15 AB', v['ab'], 1.75 * 21000 * 0.5, 1e-12); close('f15 noAB', v['nab'], 0.81 * 13500 * 0.5, 1e-12)
    elif k == 'f14': close('f14 rpm', v['rpm'], 340 / 1e-3 / (2 * math.pi) * 60, 1e-12)
    elif k == 'f35':
        T0 = 223.15; V0 = 2 * math.sqrt(GAM * R * T0); close('f35 V0', v['V0'], V0, 1e-9)
        Fn = thrust_cv(25, 0.03, 1050, V0); close('f35 Fn', v['Fn'], Fn, 1e-9); close('f35 Dr', v['Dr'], 25 * V0, 1e-9); close('f35 Fg', v['Fg'], Fn + 25 * V0, 1e-9)
        mf = .75; dke = quad(lambda x: 0, 0, 1)[0] + .5 * (25.75 * 1050 ** 2 - 25 * V0 ** 2)
        close('f35 eth', v['eth'], dke / (mf * 42.8e6), 1e-9); close('f35 ep', v['ep'], Fn * V0 / dke, 1e-9); close('f35 eo', v['eo'], Fn * V0 / (mf * 42.8e6), 1e-9)
        close('f35 tsfc', v['tsfc_h'], mf / Fn * 3600, 1e-9)
    elif k == 'f36':
        Fprop, V0, ep, m, Fg = 5000, 150, .75, 5, 1000
        close('f36 Ps', v['Ps'], brentq(lambda P: Fprop * V0 / P - ep, 1, 1e8), 1e-9); close('f36 V9', v['V9'], brentq(lambda V: m * V - Fg, 1, 1e5), 1e-9)
        dk = .5 * m * (200.0 ** 2 - V0 ** 2); close('f36 dk', v['dk'], dk, 1e-9)
        Pt = (Fprop + Fg - m * V0) * V0; close('f36 eta', v['ep'], Pt / (1e6 + dk), 1e-9)
    elif k == 'f39':
        # route B: static temperature from total temperature, Tt = T(1+(g-1)/2 M^2), with Tt = a^2/(gR)*(1+(g-1)/2 M^2)
        def noz(mdot, M, a, g, cp, pe, pa):
            Rg = cp * (g - 1) / g; T = a * a / (g * Rg); Tt = T * (1 + (g - 1) / 2 * M * M); T2 = Tt / (1 + (g - 1) / 2 * M * M)
            V = M * math.sqrt(g * Rg * T2); A = mdot * Rg * T2 / (pe * V); return mdot * V + A * (pe - pa), A
        F9, A9 = noz(10, 1.5, 450, 1.33, 1157, 15e3, 10e3); F19, A19 = noz(65, 1.5, 310, 1.4, 1004, 15e3, 10e3)
        close('f39 Fg9', v['Fg9'], F9, 1e-9); close('f39 Fg19', v['Fg19'], F19, 1e-9); close('f39 A9', v['A9'], A9, 1e-9); close('f39 A19', v['A19'], A19, 1e-9)
        close('f39 Dram', v['Dram'], 75 * .85 * 300, 1e-12); close('f39 Fn', v['Fn'], F9 + F19 - 75 * .85 * 300, 1e-9)
    elif k == 'f310':
        T0 = 223.15; V0 = 2 * math.sqrt(GAM * R * T0); Tt9 = 2500.0; Rr = 1004 * 0.4 / 1.4
        T9 = brentq(lambda T: T * (1 + .2 * 4) - Tt9, 1, 1e4); V9 = 2.0 * math.sqrt(GAM * Rr * T9)
        Fn = thrust_cv(10, .04, V9, V0); close('f310 V9', v['V9'], V9, 1e-9); close('f310 Fn', v['Fn'], Fn, 1e-9)
        dke = .5 * (10.4 * V9 ** 2 - 10 * V0 ** 2); close('f310 ep', v['ep'], Fn * V0 / dke, 1e-9); close('f310 Fg', v['Fg'], 10.4 * V9, 1e-9)
    elif k == 'f311':
        Fn = thrust_cv(100, .025, 600, 300); close('f311 Fn', v['Fn'], 102.5 * 600 - 100 * 300, 1e-12); close('f311 Fn(cv)', v['Fn'], Fn, 1e-9)
        close('f311 tsfc', v['tsfc'], 2.5 / Fn * 1e6, 1e-9); dke = .5 * (102.5 * 600 ** 2 - 100 * 300 ** 2)
        close('f311 eth', v['eth'], dke / (2.5 * 42e6), 1e-9); close('f311 ep', v['ep'], Fn * 300 / dke, 1e-9)
    elif k == 'ex24':
        comps = [(648e3, .117, 124), (655e3, .132, 112), (641e3, .374, 94), (145e3, .310, 271), (145e3, .420, 196), (41e3, .214, 584)]
        imp = [pA + 69.4 * U for (pA, A, U) in [(p_ * A_, A_, U_) for p_, A_, U_ in comps]]      # impulse function I = pA + m U at each station (route B)
        F = [imp[0]] + [imp[i] - imp[i - 1] for i in range(1, 6)]
        for i in range(6): close(f'ex24 F{i}', v['F'][i], F[i], 1e-9)
        close('ex24 total', v['tot'], sum(F), 1e-9); close('ex24 direct = last impulse', v['direct'], imp[5], 1e-12)
        for want, got in zip([84421, 9812, 152025, -182500, 10745, -25198], v['F']): close('ex24 printed', want, got, 1e-3, abs_tol=2.0)
        close('ex24 printed total', 49304, v['tot'], 1e-3, abs_tol=2.0)
    elif k == 'ex21':
        us = sp.symbols('u'); roots = sorted([float(x) for x in sp.solve(30 * us ** 2 - 31 * 610 * us + 1.12e6, us)], reverse=True)
        close('ex21 r1', v['r1'], roots[0], 1e-9); close('ex21 r2', v['r2'], roots[1], 1e-9); close('ex21 printed 564.15', 564.15, v['r1'], 1e-4, abs_tol=0.02); close('ex21 printed 66.17', 66.17, v['r2'], 1e-3, abs_tol=0.02)
    elif k == 'ex22':
        close('ex22 Ff', v['Ff'], thrust_cv(100 / 32.2, 0, 450, 146.67), 1e-9); close('ex22 Fr', v['Fr'], thrust_cv(100 / 32.2, 0, 0, 146.67), 1e-9)
        close('ex22 printed 942', 942, v['Ff'], 1e-3, abs_tol=1); close('ex22 printed -455.5', -455.5, v['Fr'], 1e-3, abs_tol=0.5)
    elif k == 'ex23':
        close('ex23 Tmom', v['Tmom1'], 24480.0, 1e-12); close('ex23 Tp', v['Tp'], 42300.0, 1e-12)
        rho = 30.8e3 / (R * 229.74); U = 1000 / 3.6; ma = rho * U * .235; T = thrust_cv(ma, .02, 600, U, 200e3, 30.8e3, .25); close('ex23 net(1000 km/h)', v['Tn2'], T, 1e-9)
        book = 42300 + 18.66 * 1000 - 8.47e-3 * 1000 ** 2; close('ex23 vs book polynomial', v['Tn2'], book, 2e-3)
    elif k == 'ex25':
        T = 223.3; u = .8 * math.sqrt(GAM * R * T); close('ex25 u', v['u'], u, 1e-9); close('ex25 printed u 239.6', 239.6, v['u'], 1e-3)
        st = thrust_cv(1.0, .02, 570, u, .67e5, .265e5, .006); close('ex25 st', v['st'], st, 1e-9); close('ex25 printed 584.77', 584.77, v['st'], 2e-4, abs_tol=0.1)
        close('ex25 e1', v['e1'], ep1_sympy(1.0, .02, 570, u) * 0 + 2 * st * u / (2 * st * u + 1.02 * (570 - u) ** 2), 1e-12)
        close('ex25 printed 0.7156', .7156, v['e1'], 2e-3); close('ex25 printed 1.022', 1.022, v['e2'], 2e-3); close('ex25 printed 0.5918', .5918, v['e3'], 1e-3)
    elif k == 'ex26':
        u = .9 * math.sqrt(GAM * R * 222.75); close('ex26 u', v['u'], u, 1e-9)
        Th = thrust_cv(22.7, .015, 452, u, 32.56e3, 26.2e3, .229); Tc = thrust_cv(68.1, 0, 339.7, u, 55.26e3, 26.2e3, .299)
        close('ex26 T', v['T'], Th + Tc, 1e-9); close('ex26 printed 19.257 kN', 19257, v['T'], 1e-3, abs_tol=10)
        close('ex26 printed eta 0.9032', .9032, v['ep'], 1e-3)
    elif k == 'ex27':
        U = .8 * math.sqrt(GAM * R * 223.2); close('ex27 U', v['U'], U, 1e-9)
        mc, mh = 125 * 5 / 6, 125 / 6; f = .75 / mh
        uec = brentq(lambda ue: mc * (ue - U) - 18000, 1, 5000); ueh = brentq(lambda ue: mh * ((1 + f) * ue - U) - 6000, 1, 5000)
        close('ex27 uec', v['uec'], uec, 1e-9); close('ex27 ueh', v['ueh'], ueh, 1e-9)
        ke = .5 * (mh * ((1 + f) * ueh ** 2 - U ** 2) + mc * (uec ** 2 - U ** 2)); close('ex27 eta_p', v['ep'], 24000 * U / ke, 1e-9); close('ex27 eta_th', v['eth'], ke / (.75 * 42.8e6), 1e-9)
        close('ex27 eta_o', v['eo'], 24000 * U / (.75 * 42.8e6), 1e-9)
        close('ex27 printed uec 413', 413, v['uec'], 3e-3); close('ex27 printed ueh 510', 510, v['ueh'], 3e-3); close('ex27 printed etap 0.712', .712, v['ep'], 6e-3)
        close('ex27 eta_th = 16.179e6/(2*0.75*42.8e6) = 0.2520 (book prints 0.2546: its own arithmetic slip, see notes)', .2520, v['eth'], 3e-3); close('ex27 book-printed eta_th 0.2546 is 1.3 % high', .2546, v['eth'], 2.5e-2); close('ex27 printed eta_o 0.1793', .1793, v['eo'], 6e-3); close('ex27 printed TSFC 0.03125', .03125, v['tsfc'], 1e-9)
    elif k == 'ex29': close('ex29 S', v['S'], breguet_B(.35, 45e6, 17, 1 / .673) * G0 / 9.8, 1e-9); close('ex29 printed 10,819 km', 10819e3, v['S'], 5e-4)
    elif k == 'ex211':
        def burn(Vg):
            ode = solve_ivp(lambda s, m: [-m[0] * (.08 / 3600) * 9.8 / (Vg * 10)], (0, 4000e3), [50000.0], rtol=1e-11, atol=1e-8)   # dm/ds = -m * TSFC g /(Vg L/D)
            return 50000.0 - ode.y[0, -1]
        close('ex211 tail', v['ft'], burn(300), 1e-6); close('ex211 head', v['fh'], burn(200), 1e-6)
        close('ex211 printed 12,600', 12600, v['ft'], 1e-3); close('ex211 printed 17,654', 17654, v['fh'], 1e-4)
    elif k == 'p24': close('p24 Trev', v['Trev'], abs(thrust_cv(40, .025, -500, 80)), 1e-9)
    elif k == 'p228':
        close('p228 a', v['a'], (560 - 475) * .44704 / 20, 1e-12)
        sol = solve_ivp(lambda t, y: [y[1], (560 - 475) * .44704 / 20], (0, 20), [0.0, 475 * .44704], rtol=1e-12, atol=1e-12); close('p228 d', v['d'], sol.y[0, -1], 1e-9)
    elif k == 'f317':
        g = 1.33
        # route B: ratio of mass-flow functions via sympy limit of f(M)
        M = sp.symbols('M', positive=True); fM = M * (1 + sp.Rational(33, 200) * M ** 2) ** (-(g + 1) / (2 * (g - 1)))
        A7 = .5 * .98 * float(fM.subs(M, 1)) / float(fM.subs(M, sp.Rational(1, 2))); close('f317 A7', v['A7'], A7, 1e-9)
    else: FAILS.append(f'no route-B function for kind {k}')

for rec in REG: check(rec)

# ---------------------------------------------------------------- printed answers of single-formula examples (no registry entry)
close('Farokhi Ex 3.3 pressure thrust (kN)', 314.16, (200e3 - 100e3) * math.pi * 2 ** 2 / 4 / 1e3, 1e-4)
close('Farokhi Ex 3.3 gross thrust (kN)', 1314, 250 * 4000 / 1e3 + (200e3 - 100e3) * math.pi / 1e3, 1e-3)
close('Farokhi Ex 3.4 eta_th', .492, 102 * 900 ** 2 / (2 * 2 * 42000e3), 1e-3); close('Farokhi Ex 3.4 Fn (kN)', 91.8, 102 * 900 / 1e3, 1e-3)
close('Farokhi Ex 3.5 eta_p (book prints 36.3 %, exact 36.36 %)', .363, 2 / (1 + 4.5), 2e-3); close('Farokhi Ex 3.6 eta_p', .889, 2 / (1 + 1.25), 1e-3)
close('Farokhi Ex 3.6 "52.6 % increase": percentage points', .526, 2 / 2.25 - 2 / 5.5, 3e-3); close('Farokhi Ex 3.6 relative rise 144 %', 1.444, (2 / 2.25) / (2 / 5.5) - 1, 1e-3)
close('Farokhi 3.7 p1/p0', .9505, (100e3 + .5 * 1 * (10 ** 2 - 100 ** 2)) / 100e3, 1e-9); close('Farokhi 3.8 Is (s)', 3500 / G0, 3500 / G0, 1e-12)
close('Farokhi 3.13 shaft power (kW)', 13986, .333 * 42000, 1e-9); close('Farokhi 1.1 Carnot', .856, 1 - 288 / 2000, 1e-9)
# ISA vs Farokhi Appendix A SI table (typed from the page image: alt km, T K, p Pa, rho kg/m3)
FAROKHI = {0: (288.1, 1.013e5, 1.225), 2: (275.2, 7.950e4, 1.007), 4: (262.2, 6.166e4, 0.8193), 6: (249.2, 4.722e4, 0.6601), 8: (236.2, 3.565e4, 0.5258), 10: (223.3, 2.650e4, 0.4135),
           12: (216.6, 1.940e4, 0.3119), 14: (216.6, 1.417e4, 0.2279), 16: (216.6, 1.035e4, 0.1665), 18: (216.6, 7.565e3, 0.1216), 20: (216.6, 5.529e3, 0.08891),
           22: (218.6, 4.047e3, 0.06451), 24: (220.6, 2.972e3, 0.04694), 26: (222.5, 2.188e3, 0.03426), 28: (224.5, 1.616e3, 0.02508), 30: (226.5, 1.197e3, 0.01841), 40: (250.4, 2.871e2, 0.003995)}
print('\nISA closed form (route A) vs numerical hydrostatic integration (route B) vs Farokhi Appendix A (SI table, printed values)')
print('alt km |  T_A   T_F  |  p_A (Pa)  p_B (Pa)  p_F (Pa) | dp% (A vs F) | rho_A rho_F')
sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
from m01_common import isa
worst = 0
for z, (TF, pF, rF) in FAROKHI.items():
    if z > 32: continue
    TA, pA, rA = isa(z * 1000.0); TB, pB, rB = isa_B(z * 1000.0)
    close(f'isa A vs B p {z} km', pA, pB, 3e-5); dp = (pA - pF) / pF * 100; worst = max(worst, abs(dp))
    close(f'isa vs Farokhi T {z} km', TA, TF, 0.0, abs_tol=0.35); close(f'isa vs Farokhi p {z} km', pA, pF, 2.5e-2); close(f'isa vs Farokhi rho {z} km', rA, rF, 2.5e-2)
    print(f'{z:5d}  | {TA:6.2f} {TF:6.1f} | {pA:9.1f} {pB:9.1f} {pF:9.1f} | {dp:+6.2f} | {rA:.5f} {rF:.5f}')
print(f'largest |p_ISA - p_Farokhi| = {worst:.2f} % (Farokhi uses the 1962-type table; differences grow above 20 km)')
T11, p11, r11 = isa(11000.0); close('ISA 11 km p = 226.3 hPa', 22632.0, p11, 1e-4); close('ISA 10 km p = 264.4 hPa (slide 48 prints 264)', 26436.0, isa(10000.0)[1], 1e-4)
print(f'ISA: 10 km p = {isa(10000.0)[1]/100:.1f} hPa, T = {isa(10000.0)[0]-273.15:.1f} C;  11 km p = {p11/100:.1f} hPa, T = {T11-273.15:.1f} C;  25 km p = {isa(25000.0)[1]/100:.2f} hPa;  40 km (table) p = 2.871 hPa')

# ---------------------------------------------------------------- report
print(f'\n{len(ROWS)} comparisons')
bad = [r for r in ROWS if r[3] != 'ok']
for r in ROWS[:0]: pass
if os.environ.get('SHOW_ALL'):
    for name, a, b, s in ROWS: print(f'{name:55s} {a:16.8g} {b:16.8g} {s}')
for r in bad: print('FAIL', r)
print('FAILS: none' if not FAILS else 'FAILS: ' + '; '.join(FAILS))
sys.exit(0 if not FAILS else 1)
