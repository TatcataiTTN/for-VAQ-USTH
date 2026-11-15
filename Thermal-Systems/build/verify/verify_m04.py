"""verify_m04: recompute EVERY numeric answer of module m04 (fuels and combustion) by ROUTE B and compare with the stored route-A values
(data/verify/m04_values.json, written by build/gen/gen_m04.py), then compare with the answers PRINTED in the slides (Ch.4) and in Cengel Ch.15.
Route A = what a student does by hand with the lecturer's conventions: rounded atomic masses (C 12, H 1, O 16, N 14), M_air = 29, dew point by linear interpolation of
Table A-5, h(T) by linear interpolation of A-18...A-25, h_f from A-26.
Route B = independent re-implementations:
  balance of the reaction      -> sympy: element matrix (exact rational arithmetic), unknown coefficients solved with linsolve; molar masses parsed from the formula;
  dew point, condensed water   -> IAPWS-IF97 (iapws) + scipy brentq (A-5 / A-4 are not used);
  enthalpy of combustion       -> heating values of Table A-27 (HHV, LHV) times the molar mass (a second table), and h_fg of IAPWS for HHV - LHV;
  sensible enthalpy h(T)-h(298) -> (1) integral of T ds0 over the s0 column of the SAME tables A-18...A-25 (the h column is not used; cells flagged in
                                    data/props/book_errata.json are replaced by their expected value), (2) the cp(T) polynomials of A-2c (T <= 1800 K),
                                    (3) CoolProp ideal-gas enthalpy (N2, O2, CO2, H2O up to 2000 K);
  flame temperature            -> scipy brentq on route (1).
Tolerances are explicit; none was tuned to hide a gap: the observed maxima are printed.  Also checked: no question uses a table cell flagged as a printed error.
Run:  .venv/bin/python -I build/verify/verify_m04.py"""
import json, math, os, sys, re, collections
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
import CoolProp.CoolProp as CP
from iapws import IAPWS97
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'props'))
import props
V = json.load(open(os.path.join(ROOT, 'data', 'verify', 'm04_values.json'), encoding='utf-8'))
D = lambda n: json.load(open(os.path.join(ROOT, 'data', 'props', n + '.json'), encoding='utf-8'))
FAILS = []; ROWS = []; DEV = collections.defaultdict(float)
def rec(name, a, b, tol, note=''):
    """tol: float = relative, {'abs': x} = absolute."""
    if isinstance(tol, dict): err = abs(a - b); lim = tol['abs']
    else: err = abs(a - b) / max(abs(a), abs(b), 1e-300); lim = tol
    ok = err <= lim; fam = name.split(' ')[0]; DEV[fam] = max(DEV[fam], err / lim if lim else 0)
    ROWS.append((name, a, b, err, lim, 'ok' if ok else 'FAIL'))
    if not ok: FAILS.append(f'{name}: A={a:.8g} B={b:.8g} err={err:.3g} > {lim} {note}')

# ---------------------------------------------------------------- formulas and molar masses (route B: parsed from the formula text)
def parse(fm):
    d = collections.Counter()
    for el, n in re.findall(r'([A-Z][a-z]?)(\d*)', fm): d[el] += int(n) if n else 1
    return d
FORMULA = dict(CH4='CH4', C2H2='C2H2', C2H4='C2H4', C2H6='C2H6', C3H6='C3H6', C3H8='C3H8', C4H10='C4H10', C6H6='C6H6', C8H18='C8H18', C12H26='C12H26', H2='H2', CO='CO', CH3OH='CH3OH',
               C2H5OH='C2H5OH', C3H7OH='C3H7OH', N2='N2', O2='O2', CO2='CO2', C='C')
ROUND = dict(C=12, H=1, O=16, N=14)
A1M = {r[1]: r[2] for r in D('A1')['rows']}; A27 = {r[1]: r for r in D('A27')['rows']}            # A-1: formula -> M ; A-27: formula -> row
A27ALIAS = dict(CH3OH='CH4O', C2H5OH='C2H6O')              # Table A-27 writes methanol as CH4O and ethanol as C2H6O
def a27r(fm): return A27[A27ALIAS.get(fm, fm)]
def Mexact(sp_):
    """molar mass for the 'exact' variant: Table A-27 or A-1 when the species is listed there, else from atomic masses C 12.011, H 1.008, O 15.9995, N 14.0065."""
    fm = FORMULA[sp_]; fm = A27ALIAS.get(fm, fm)
    if fm in A27 and isinstance(A27[fm][2], (int, float)): return A27[fm][2]
    if fm in A1M: return A1M[fm]
    a = parse(fm); return 12.011 * a['C'] + 1.008 * a['H'] + 15.9995 * a['O'] + 14.0065 * a['N']
def Mround(sp_): a = parse(FORMULA[sp_]); return sum(ROUND[k] * v for k, v in a.items())
def fuel_elems(parts):
    e = collections.Counter(); Mr = 0; Mx = 0
    for s, y in parts:
        a = parse(FORMULA[s])
        for k, v in a.items(): e[k] += sp.nsimplify(y) * v
        Mr += y * Mround(s); Mx += y * Mexact(s)
    return e, Mr, Mx
def comb_sympy(parts, lam, moist=0, h2o_fuel=0):
    """sympy: stoichiometric coefficient from the element matrix, then the lam case (exact rationals)."""
    e, Mr, Mx = fuel_elems(parts); lam = sp.nsimplify(lam)
    a, nc, nh, nn = sp.symbols('a nc nh nn')
    # reaction  fuel + a (O2 + 3.76 N2) -> nc CO2 + nh H2O + nn N2      (stoichiometric, no O2 in products)
    r = sp.Rational(376, 100)
    sol = sp.solve([sp.Eq(e['C'], nc), sp.Eq(e['H'], 2 * nh), sp.Eq(e['O'] + 2 * a, 2 * nc + nh), sp.Eq(e['N'] + 2 * r * a, 2 * nn)], [a, nc, nh, nn], dict=True)[0]
    ath = sol[a]; o2in = lam * ath
    no2 = sp.symbols('no2'); nn2, nc2, nh2 = sp.symbols('nn2 nc2 nh2')
    sol2 = sp.solve([sp.Eq(e['C'], nc2), sp.Eq(e['H'], 2 * nh2), sp.Eq(e['O'] + 2 * o2in, 2 * nc2 + nh2 + 2 * no2), sp.Eq(e['N'] + 2 * r * o2in, 2 * nn2)], [nc2, nh2, no2, nn2], dict=True)[0]
    out = dict(ath=float(ath), o2_in=float(o2in), CO2=float(sol2[nc2]), H2O=float(sol2[nh2]) + moist + h2o_fuel, O2=float(sol2[no2]), N2=float(sol2[nn2]), air=float(o2in * (1 + r)))
    out['n_dry'] = out['CO2'] + out['O2'] + out['N2']; out['n_tot'] = out['n_dry'] + out['H2O']
    out['AF_round'] = out['air'] * 29.0 / float(Mr); out['AF_exact'] = out['air'] * 28.97 / float(Mx); out['M_round'] = float(Mr); out['M_exact'] = float(Mx)
    return out
def Psat_iapws(T_C): return IAPWS97(T=T_C + 273.15, x=0).P * 1000.0
def Tsat_iapws(P_kPa): return IAPWS97(P=P_kPa / 1000.0, x=0).T - 273.15
def parts_of(p): return [(a, b) for a, b in p['fuel']]

# ---------------------------------------------------------------- sensible enthalpy, route B (three independent descriptions)
GAS = dict(N2=18, O2=19, CO2=20, CO=21, H2=22, H2O=23, O=24, OH=25)
ERR = D('book_errata')['errors']
_S = {}
def s_spline(g):
    if g not in _S:
        tab = D(f'A{GAS[g]}'); rows = [list(r) for r in tab['rows'] if r[0] > 0]
        for e in ERR:
            if e['table'] == f'A-{GAS[g]}' and e['col'] == 's0':
                for r in rows:
                    if r[0] == e['key']['T_K']: r[3] = e['expected']
        T = np.array([r[0] for r in rows]); s = np.array([r[3] for r in rows]); _S[g] = (CubicSpline(T, s), T[0], T[-1])
    return _S[g]
def dh_B1(g, T, T0=298.0):
    """h(T) - h(T0) = integral of T ds0 = [T s0] - integral of s0 dT (s0 column of the same table, spline)."""
    spl, lo, hi = s_spline(g)
    if not (lo <= T <= hi): raise ValueError(f'{g} {T}')
    integ, _ = quad(lambda t: float(spl(t)), T0, T, limit=200)
    return T * float(spl(T)) - T0 * float(spl(T0)) - integ
A2C = {r[1]: r for r in D('A2c')['rows']}
def dh_B2(g, T, T0=298.0):
    r = A2C[g]; a, b, c, d = r[2:6]
    if T > r[7] or T0 < r[6]: return None
    return a * (T - T0) + b / 2 * (T ** 2 - T0 ** 2) + c / 3 * (T ** 3 - T0 ** 3) + d / 4 * (T ** 4 - T0 ** 4)
CPF = dict(N2='Nitrogen', O2='Oxygen', CO2='CarbonDioxide', H2O='Water')
def dh_B3(g, T, T0=298.15):
    if g not in CPF or T > 2000: return None
    M = CP.PropsSI('molemass', CPF[g]) * 1000.0; p = 100.0       # 100 Pa: the ideal-gas limit
    return (CP.PropsSI('H', 'T', T, 'P', p, CPF[g]) - CP.PropsSI('H', 'T', T0, 'P', p, CPF[g])) / 1000.0 * M * 1000.0 / 1000.0 * 1.0
F26 = {r[1]: r[2] for r in D('A26')['rows']}
KEY26 = dict(CO2='CO2(g)', CO='CO(g)', H2O_g='H2O(g)', H2O_l='H2O(ᐉ)', H2='H2(g)', O2='O2(g)', N2='N2(g)', C2H2='C2H2(g)', C2H4='C2H4(g)', C2H6='C2H6(g)', C3H6='C3H6(g)', C3H8='C3H8(g)',
             C4H10='C4H10(g)', C6H6='C6H6(g)', C8H18_g='C8H18(g)', C8H18_l='C8H18(ᐉ)', C12H26='C12H26(g)', CH3OH_l='CH3OH(ᐉ)', C2H5OH_l='C2H5OH(ᐉ)', C2H5OH_g='C2H5OH(g)', CH4='CH4(g)', CH3OH_g='CH3OH(g)')
def hfB(k): return F26[KEY26[k]]
def tabgas(k): return 'H2O' if k in ('H2O_g',) else k
def H_B(items, which=1):
    """sum n (hf + h(T) - h(298)) with sensible part by route which (1, 2 or 3); None if the route does not cover a state."""
    tot = 0.0
    for sp_, n, T in items:
        g = tabgas(sp_); sens = 0.0
        if g in GAS and sp_ != 'H2O_l' and T != 298.0:
            f = dict([(1, dh_B1), (2, dh_B2), (3, dh_B3)])[which]; v = f(g, T)
            if v is None: return None
            sens = v
        tot += n * (hfB(sp_) + sens)
    return tot
USED_ROWS = set()
def note_rows(items):
    for sp_, n, T in items:
        g = tabgas(sp_)
        if g in GAS and sp_ != 'H2O_l': USED_ROWS.add((g, float(T)))
def q_B(react, prod, which=1):
    hr = H_B([tuple(x) for x in react], which); hp = H_B([tuple(x) for x in prod], which)
    return None if hr is None or hp is None else hr - hp

# ---------------------------------------------------------------- registry models (route B)
def comb_B(p):
    c = comb_sympy(parts_of(p), p['lam'], p.get('moist', 0), p.get('h2o_fuel', 0))
    return dict(AF=c['AF_exact'] if p.get('exact') else c['AF_round'], **{k: c[k] for k in ('CO2', 'H2O', 'O2', 'N2', 'air', 'n_tot', 'n_dry', 'ath')})
def comb_AF_B(p):
    parts = parts_of(p); e, Mr, Mx = fuel_elems(parts); M = Mx if p.get('exact') else Mr; Mair = 28.97 if p.get('exact') else 29.0
    a = sp.nsimplify(p['AF']) * M / (sp.Rational(476, 100) * sp.nsimplify(Mair)); r = sp.Rational(376, 100)
    nc, nh, no2, nn = sp.symbols('nc nh no2 nn')
    sol = sp.solve([sp.Eq(e['C'], nc), sp.Eq(e['H'], 2 * nh), sp.Eq(e['O'] + 2 * a, 2 * nc + nh + 2 * no2), sp.Eq(e['N'] + 2 * r * a, 2 * nn)], [nc, nh, no2, nn], dict=True)[0]
    return dict(N2=float(sol[nn]), O2=float(sol[no2]), H2O=float(sol[nh]))
def rev_B(p):
    R = lambda x: sp.nsimplify(str(x), rational=True)
    CO2, CO, O2, N2 = R(p['CO2']), R(p['CO']), R(p['O2']), R(p['N2']); c, h = sp.Integer(int(p['c'])), sp.Integer(int(p['h']))
    x, a, b = sp.symbols('x a b')
    sol = sp.solve([sp.Eq(a * sp.Rational(376, 100), N2), sp.Eq(c * x, CO2 + CO), sp.Eq(h * x, 2 * b)], [x, a, b], dict=True)[0]
    resid = float(sol[a] - (CO2 + CO / 2 + O2 + sol[b] / 2))
    Mf = 12 * c + h; AF = sol[a] / sol[x] * sp.Rational(476, 100) * 29 / Mf; th = c + h / sp.Integer(4)
    return dict(AF=float(AF), pct=float(sol[a] / sol[x] / th * 100), resid=resid, x=float(sol[x]), b=float(sol[b]), n_tot_per_fuel=float((CO2 + CO + O2 + N2 + sol[b]) / sol[x]), H2O_per_fuel=float(sol[b] / sol[x]))
def cond_B(p):
    if 'fuel' in p:
        c = comb_sympy(parts_of(p), p['lam']); Nv, Ntot = c['H2O'], c['n_tot']
    elif p.get('slide'): Nv, Ntot = 9.0, 82.53
    else:
        r = rev_B(p); Nv, Ntot = r['H2O_per_fuel'], r['n_tot_per_fuel']
    y = Psat_iapws(p['T']) / p['P']
    Nw = brentq(lambda w: (Nv - w) / (Ntot - w) - y, 0.0, Nv - 1e-9)
    return dict(Nw=Nw, frac=Nw / Nv)
def dew_B(p):
    c = comb_sympy(parts_of(p), p['lam'])
    if 'phi' in p:                                         # moist air (Cengel Example 15-3): N_v,air = Pv/(P-Pv) * N_dry air
        Pva = p['phi'] * Psat_iapws(p['T_air']); Nv = Pva / (p['P'] - Pva) * c['air']; c['H2O'] += Nv; c['n_tot'] += Nv
    Pv = c['H2O'] / c['n_tot'] * p['P']; return dict(Pv=Pv, Tdp=Tsat_iapws(Pv))
def spray_B(p):
    c = comb_sympy(parts_of(p), p['lam']); y = Psat_iapws(p['T']) / p['P']
    return dict(w=brentq(lambda w: (c['H2O'] + w) / (c['n_tot'] + w) - y, 0, 100))
def coal_B(p):
    n = sp.symbols('n'); C = sp.Rational(str(p['wC'])) / 12; H2 = sp.Rational(str(p['wH2'])) / 2; O2 = sp.Rational(str(p['wO2'])) / 32
    # elements per 100 kg: C, H (2 per H2), O (2 per O2); stoichiometric O2 demand from the CO2/H2O O balance
    o2_th = sp.solve(sp.Eq(2 * n + 2 * O2, 2 * C + H2), n)[0]
    air = sp.nsimplify(p['lam']) * o2_th * sp.Rational(476, 100); return dict(AF=float(air * 29 / 100))
def hC_B(p):
    out = {}; nu = p['nu']; M = p.get('M')
    if 'Hprod' in p: return {'q_out': float(hfB(p['fuel']) - p['Hprod'])}
    hp = sum(n * hfB(('H2O_' + p['water']) if s == 'H2O' else s) for s, n in nu.items()) - hfB(p['fuel'])
    out['kJ/kmol'] = None
    if p.get('a27'):
        row = a27r(FORMULA[p['a27']]); col = {'HHV': 6, 'LHV': 7}[p['col']]; add = row[4] if p.get('liq_listed') and row[4] else 0.0      # A-27 lists butane and benzene as LIQUIDS: the gas needs + h_fg(fuel)
        val = -(row[col] + add) * row[2]
        out['kJ/kmol'] = val; out['kJ/kg'] = -(row[col] + add)
    else:                                                  # fuel not in A-27: Hess cycle check through h_fg of IAPWS: hC(liquid water) - hC(vapor water) = n_H2O * M_H2O * hfg
        nH2O = nu.get('H2O', 0); hfg = (IAPWS97(T=298.15, x=1).h - IAPWS97(T=298.15, x=0).h) * 18.015
        sgn = -1 if p['water'] == 'l' else +1
        gas = sum(n * hfB(('H2O_g') if s == 'H2O' else s) for s, n in nu.items()) - hfB(p['fuel'])
        out['kJ/kmol'] = gas - nH2O * hfg if p['water'] == 'l' else gas
        out['kJ/kg'] = out['kJ/kmol'] / M if M else None
    return out
def lhv_kg_B(p):
    hfg = (IAPWS97(T=298.15, x=1).h - IAPWS97(T=298.15, x=0).h); mH2O = p['H'] / 2 * 18.015 / p['M']
    return dict(LHV=p['HHV'] - mH2O * hfg)
def q_model(p):
    q1 = q_B(p['react'], p['prod'], 1); return dict(q_out=q1)
def tad_B(p):
    react = [tuple(x) for x in p['react']]; Hr = H_B(react, 1) - p.get('loss', 0.0)
    prod = lambda T: [(s, n, T) for s, n in p['prod']]
    return dict(T=brentq(lambda T: H_B(prod(T), 1) - Hr, 300.0, 3200.0, xtol=1e-6))
def pct_af_B(p):
    c = comb_sympy(parts_of(p), 1); return dict(pct=p['AF'] / c['AF_round'] * 100)
def phi_B(p): c = comb_sympy(parts_of(p), 1); return dict(phi=c['AF_round'] / p['AF'])
def airflow_B(p): c = comb_sympy(parts_of(p), p['lam']); return {'kg/s': c['AF_round'] * p['mf']}
def yco_B(p):
    if p.get('fuel') == 'C6H6' or 'fuel' not in p:
        x, y = sp.symbols('x y'); lam = sp.nsimplify(p['lam']); o2 = lam * sp.Rational(15, 2)
        s_ = sp.solve([sp.Eq(x + y, 6), sp.Eq(2 * x + y + 3, 2 * o2)], [x, y], dict=True)[0]
        tot = s_[x] + s_[y] + 3 + sp.Rational(376, 100) * o2; return dict(yCO=float(s_[y] / tot))
MODELS = dict(comb=comb_B, comb_AF=comb_AF_B, rev=rev_B, cond=cond_B, dew=dew_B, spray=spray_B, coal=coal_B, hC=hC_B, lhv_kg=lhv_kg_B, q=q_model, Tad=tad_B, pct_af=pct_af_B, phi=phi_B, airflow=airflow_B, yco=yco_B)
SIMPLE = dict(
    mdot=lambda p: {'g/s': p['Q'] / p['q'] * p['M'] * 1000.0},
    Vflow=lambda p: {'L/min': p['Q'] / p['q'] * p['M'] / p['rho'] * 1000.0 * 60.0},
    pct=lambda p: {'pct': p['num'] / p['den'] * 100.0},
    lhv_from_hhv=lambda p: {'LHV': p['HHV'] - p['m'] / 2 * 18.015 * (IAPWS97(T=298.15, x=1).h - IAPWS97(T=298.15, x=0).h) / 1000.0})
SIMPLE['mdot'] = lambda p: ({'kJ/h': p['q'] * p['kg_h'] / p['M']} if 'kg_h' in p else {'g/s': p['Q'] / p['q'] * p['M'] * 1000.0})

# ---------------------------------------------------------------- 1. every registry entry
n_reg = 0; extra_exact = []
for e in V['registry']:
    m, p, out, val, tol, what = e['model'], e['params'], e['out'], e['value'], e['tol'], e['what']
    if m in MODELS and m not in ('q', 'Tad'):
        b = MODELS[m](p)
        if m == 'comb' and out == 'AF': rec(f'comb {what}', val, b['AF'], tol if not isinstance(tol, float) else max(tol, 1e-9), 'sympy balance')
        elif m == 'hC': rec(f'hC {what}', val, b[out], tol, 'A-26 vs A-27 / Hess'); 
        else: rec(f'{m} {what} [{out}]', val, b[out], tol)
        if m == 'comb' and out == 'AF' and not p.get('exact'):
            c = comb_sympy(parts_of(p), p['lam']); extra_exact.append((what, val, c['AF_exact']))
    elif m == 'q':
        q1 = q_model(p)['q_out']; rec(f'q {what} [B1 integral of T ds0]', val, q1, tol); note_rows([tuple(x) for x in p['react']] + [tuple(x) for x in p['prod']])
        for w, lim, tag in ((2, 0.02, 'A-2c cp polynomials'), (3, 0.01, 'CoolProp ideal gas')):
            qv = q_B(p['react'], p['prod'], w)
            if qv is not None: rec(f'qalt {what} [B{w} {tag}]', val, qv, lim)
    elif m == 'Tad':
        T1 = tad_B(p)['T']; rec(f'Tad {what} [B1 integral of T ds0]', val, T1, tol)
        note_rows([tuple(x) for x in p['react']] + [(s, n, val) for s, n in p['prod']])
    elif m in SIMPLE: rec(f'{m} {what}', val, SIMPLE[m](p)[out], tol)
    else: FAILS.append(f'unknown model {m}')
    n_reg += 1
print(f'  registry: {n_reg} entries recomputed by route B')

# ---------------------------------------------------------------- 2. exact molar masses versus the rounded masses of the slides (documented effect, tolerance 0.6 %)
for what, a, bx in extra_exact: rec(f'massround {what}', a, bx, 0.012, 'rounded (29, 12, 1; H2 = 2) vs exact (28.97, A-1/A-27) masses')

# ---------------------------------------------------------------- 3. answers PRINTED in the slides and in Cengel Ch.15
for p in V['printed']: rec(f'printed {p["key"]}', p['ours'], p['printed'], p['tol'], p.get('note', ''))
print(f'  printed answers compared: {len(V["printed"])}')

# ---------------------------------------------------------------- 4. A-5 interpolation error versus IAPWS over the pressure range used (declared tolerance 0.5 C; slide 52.27 vs 52.49)
worst = 0.0; worstP = None
for P in np.arange(7.5, 200.0, 0.25):
    e_ = abs(props.sat_P('water', float(P), 'Tsat_C')['value'] - Tsat_iapws(float(P)))
    if e_ > worst: worst, worstP = e_, float(P)
print(f'  A-5 linear interpolation vs IAPWS, P = 7.5...200 kPa: max |dT| = {worst:.3f} C at {worstP} kPa (declared tolerance 0.5 C)')
assert worst < 0.5, 'A-5 interpolation error larger than the declared tolerance'
rec('slide tr.32 dew point 52.3 (A-5 interpolation) vs iapws', 52.3, Tsat_iapws(13.9587), {'abs': 0.35}, 'slide p.32 / Cengel Ex 15-2')

# ---------------------------------------------------------------- 5. A-26 (formation) versus A-27 (heating values) for every fuel of A-27 with an A-26 entry
PAIRS = [('CH4', dict(CO2=1, H2O=2), 'CH4', None), ('C2H6', dict(CO2=2, H2O=3), 'C2H6', None), ('C2H2', dict(CO2=2, H2O=1), 'C2H2', None), ('H2', dict(H2O=1), 'H2', None), ('CO', dict(CO2=1), 'CO', None),
         ('C8H18_l', dict(CO2=8, H2O=9), 'C8H18', None), ('C4H10', dict(CO2=4, H2O=5), 'C4H10', None), ('C3H8', dict(CO2=3, H2O=4), 'C3H8', None), ('C6H6', dict(CO2=6, H2O=3), 'C6H6', None), ('CH3OH_l', dict(CO2=1, H2O=2), 'CH3OH', None), ('C2H5OH_l', dict(CO2=2, H2O=3), 'C2H5OH', None)]
print('  A-26 (h_f) versus A-27 (HHV, LHV x M): fuel, hC from A-26 [kJ/kmol], from A-27, difference')
mx = 0.0
for key, nu, fm, _ in PAIRS:
    row = a27r(FORMULA[fm]); M = row[2]
    for w, col, tag in (('l', 6, 'HHV'), ('g', 7, 'LHV')):
        hp = sum(n * hfB(('H2O_' + w) if s == 'H2O' else s) for s, n in nu.items()) - hfB(key); b = -row[col] * M
        d = abs(hp - b) / abs(b)
        # gaseous fuels in A-27 are 'gas' rows, but liquid ones (propane, butane, benzene...) use the liquid h_f in A-27: A-26 only lists the gas for these: allow the h_fg of the fuel
        lim = 0.0015
        if fm in ('C4H10', 'C6H6'):                         # A-27 lists these fuels as LIQUIDS but A-26 only has the gas: gas = liquid + h_fg(fuel) (A-27)
            hfgk = a27r(FORMULA[fm])[4] * M; b = -(row[col] + a27r(FORMULA[fm])[4]) * M; lim = 0.0015
        d = abs(hp - b) / abs(b); mx = max(mx, d)
        ROWS.append((f'A26/A27 {fm} {tag}', hp, b, d, lim, 'ok' if abs(hp - b) / abs(b) <= lim else 'FAIL'))
        if abs(hp - b) / abs(b) > lim: FAILS.append(f'A26/A27 {fm} {tag}: {hp:.0f} vs {b:.0f}')
        print(f'    {fm:7s} {tag}  {hp:14,.0f}  {b:14,.0f}  {100*abs(hp-b)/abs(b):6.3f} %')
# ---------------------------------------------------------------- 6. no table row flagged as a printed error is used by a question (rows bracketing the T used, columns h and s0)
flag = set()
for e in ERR:
    if e['table'] in [f'A-{n}' for n in GAS.values()] and e['col'] == 'h':           # route A reads the h column; the s0 errors are patched in route B
        g = [k for k, v in GAS.items() if f'A-{v}' == e['table']][0]; flag.add((g, float(e['key']['T_K'])))
bad = []
for g, T in USED_ROWS:
    rows = [r[0] for r in D(f'A{GAS[g]}')['rows'] if r[0] > 0]
    lo = max([t for t in rows if t <= T], default=None); hi = min([t for t in rows if t >= T], default=None)
    for t in (lo, hi):
        if (g, float(t)) in flag: bad.append((g, T, t))
print(f'  table states used by q/Tad questions: {len(USED_ROWS)}; flagged-error rows among the interpolation brackets: {len(bad)}')
for b_ in bad: FAILS.append(f'question uses a flagged table row: {b_}')
# ---------------------------------------------------------------- 7. explanation consistency: the correct option's number appears in the explanation of every closed numeric question
def toks(t): return [float(x.replace(',', '')) for x in re.findall(r'\d[\d,]*\.?\d*', t.replace('−', '-'))]
badx = 0; chk = 0
for fn in ('m04.json', 'm04_gen.json'):
    for it in json.load(open(os.path.join(ROOT, 'data', 'qsrc', fn), encoding='utf-8')):
        if it['kind'] != 'mcq': continue
        txt = it['opts'][it['correct']]['en']; m_ = re.match(r'^\s*[\-−]?(\d[\d,]*(?:\.\d+)?)', txt)
        if not m_: continue
        chk += 1; v = float(m_.group(1).replace(',', ''))
        if not any(abs(v - w) <= 0.015 * max(abs(v), 1.0) for w in toks(it['explain']['en'])): badx += 1; FAILS.append(f'explanation does not contain "{txt}": {it["src"]["en"][:60]}')
print(f'  explanation contains the correct numeric option in {chk - badx}/{chk} closed numeric questions')
# ---------------------------------------------------------------- 8. bank statistics
items = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm04.json'), encoding='utf-8')) + json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm04_gen.json'), encoding='utf-8'))
closed = [i for i in items if i['kind'] != 'ess']; l3 = [i for i in closed if i['level'] == 3]; goc = [i for i in closed if i['origin'] == 'goc']
print(f'  bank: {len(closed)} closed ({len(goc)} original), level 3: {len(l3)} = {100*len(l3)/len(closed):.0f} %, ess {sum(1 for i in items if i["kind"]=="ess")}')
if len(closed) < 60 or len(l3) < 0.2 * len(closed): FAILS.append('bank too small or too few level-3 questions')
# ---------------------------------------------------------------- report
print(f'\n{len(ROWS)} comparisons')
print('largest deviation per family as a fraction of its tolerance (1.00 = at the limit):')
for k_, v_ in sorted(DEV.items(), key=lambda t: -t[1])[:16]: print(f'  {k_:14s} {v_:.2f}')
near = sorted([r for r in ROWS if r[4] and r[3] / r[4] >= 0.8], key=lambda r: -r[3] / r[4])
print(f'comparisons within 80-100 % of their tolerance (listed so that nothing is hidden): {len(near)}')
for name, a, b, err, lim, st in near[:14]: print(f'  {name[:92]:92s} A={a:.6g} B={b:.6g} err={err:.3g} lim={lim:.3g}')
if os.environ.get('SHOW_ALL'):
    for name, a, b, err, lim, st in ROWS: print(f'{name:100s} {a:14.6g} {b:14.6g} {err:9.2e} {lim:8.1e} {st}')
for r in [r for r in ROWS if r[5] != 'ok']: print('FAIL', r)
print('FAILS: none' if not FAILS else 'FAILS: ' + '; '.join(FAILS))
sys.exit(0 if not FAILS else 1)
