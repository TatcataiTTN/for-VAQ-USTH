"""verify_m05: recompute EVERY numeric answer of module m05 (compressible flow) by ROUTE B and compare with the stored route-A values (data/verify/m05_values.json, written by
build/gen/gen_m05.py), then compare with the answers PRINTED in the slides (Ch.5) and in Cengel Ch.17, with the printed rows of Table A-32 and with _shared/thermo.js run through node.
Route A = closed forms of the slides (equations (1)-(17)) with constant specific heats.
Route B = independent descriptions that do not use equations (9)-(17):
  stagnation T0, P0           -> scipy solve_ivp of dT/dV = -V/(1000 cp) and d ln P = (cp/R) d ln T (isentropic: ds = 0);
  speed of sound c            -> numerical derivative c^2 = (dP/d rho)_s on the isentrope P(rho) = const rho^k (central difference), not sqrt(kRT);
  critical state, choked flow -> NUMERICAL MAXIMUM (scipy minimize_scalar) of the mass flux rho V along the isentrope (energy equation V = sqrt(2 cp (T0 - T)), rho = rho0 (T/T0)^(1/(k-1)));
  area ratio A/A*, Ma(A/A*)   -> flux ratio (rho* V*)/(rho V) with T found by brentq on the energy equation V(T) = Ma c(T); the Hugoniot ODE d ln A = (Ma^2-1) dMa/[Ma(1+(k-1)Ma^2/2)]
                                 integrated with solve_ivp;
  compressor/turbine work     -> w = |integral of R T d ln P| (scipy quad) along the isentrope (ODE T(ln P));
  converging nozzle           -> P_e = max(P_b, P at the flux maximum), then energy equation + ideal gas (no equation (15)/(16));
  variable specific heats     -> Table A-17 / A-20 (props library) against CoolProp ideal-gas enthalpy and entropy;
  Mach/Pitot                  -> brentq on the energy equation with P/P0 = (T/T0)^(cp/R).
Also: all printed rows of Table A-32 (five columns, half-unit-of-last-digit tolerance, the printed error rho/rho0 at Ma = 3.0 reported), _shared/thermo.js through node (stagnation, chokedMdot,
convergingNozzle, duct, critical, fromMa), the interpolation warning of A-32, and no question may use the flagged cell.
Tolerances are explicit (per model, printed in the table); none was tuned to hide a gap: the observed maxima are printed.
Run:  .venv/bin/python -I build/verify/verify_m05.py"""
import json, math, os, sys, subprocess, collections
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, minimize_scalar
import CoolProp.CoolProp as CP
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'props')); sys.path.insert(0, os.path.join(ROOT, 'build', 'gen'))
import props
V = json.load(open(os.path.join(ROOT, 'data', 'verify', 'm05_values.json'), encoding='utf-8'))
FAILS = []; ROWS = []; DEV = collections.defaultdict(float)
def rec(name, a, b, tol, note=''):
    """tol: float = relative, {'abs': x} = absolute."""
    if isinstance(tol, dict): err = abs(a - b); lim = tol['abs']
    else: err = abs(a - b) / max(abs(a), abs(b), 1e-300); lim = tol
    ok = err <= lim; fam = name.split(' ')[0]; DEV[fam] = max(DEV[fam], err / lim if lim else 0)
    ROWS.append((name, a, b, err, lim, 'ok' if ok else 'FAIL'))
    if not ok: FAILS.append(f'{name}: A={a:.8g} B={b:.8g} err={err:.3g} > {lim} {note}')

# ---------------------------------------------------------------- route-B building blocks
def cp_(k, R): return k * R / (k - 1.0)
def isentrope_T(T, P, Pnew, k):
    """T at Pnew from T at P: solve d ln T / d ln P = (k-1)/k with solve_ivp (route B)."""
    s = solve_ivp(lambda x, y: [(k - 1.0) / k], [0.0, math.log(Pnew / P)], [math.log(T)], rtol=1e-11, atol=1e-13)
    return math.exp(s.y[0, -1])
def stag_ode(T, P, Vv, cp, R, k_ex=None):
    k_ex = k_ex if k_ex else cp / (cp - R)
    """T0, P0 by integrating dT/dV = -V/(1000 cp) from V to 0, then d ln P = (cp/R) d ln T (ds = 0)."""
    s = solve_ivp(lambda v, y: [-v / (1000.0 * cp)], [Vv, 0.0], [T], rtol=1e-11, atol=1e-11); T0 = s.y[0, -1]
    I, _ = quad(lambda t: (k_ex / (k_ex - 1.0)) / t, T, T0)       # isentropic exponent k/(k-1) of the gas (cp only enters through the energy equation)
    return T0, P * math.exp(I)
def c_num(T, k, R):
    """c from the numerical derivative (dP/d rho)_s on P = C rho^k through the ideal-gas state at T (P in Pa, rho in kg/m3)."""
    P0_ = 1.0e5; rho = P0_ / (R * 1000.0 * T); C = P0_ / rho ** k; h = 1e-5 * rho
    dP = (C * (rho + h) ** k - C * (rho - h) ** k) / (2 * h); return math.sqrt(dP)
def flux_max(k):
    """x* = T*/T0 that maximises f(x) = x^(1/(k-1)) sqrt(1-x) (mass flux per unit stagnation scales); returns x*, f*."""
    f = lambda x: -(x ** (1.0 / (k - 1.0)) * math.sqrt(1.0 - x))
    r = minimize_scalar(f, bounds=(1e-6, 1 - 1e-9), method='bounded', options=dict(xatol=1e-13)); return r.x, -r.fun
def flux(x, k): return x ** (1.0 / (k - 1.0)) * math.sqrt(1.0 - x)
def x_of_Ma(Ma, k, R=0.287, T0=1000.0):
    """x = T/T0 by brentq on the energy equation Ma c(T) = sqrt(2000 cp (T0 - T)) (c from the numerical derivative)."""
    cp = cp_(k, R)
    g = lambda T: Ma * c_num(T, k, R) - math.sqrt(max(2000.0 * cp * (T0 - T), 0.0))
    return brentq(g, 1e-3 * T0, T0 * (1 - 1e-12), xtol=1e-12, rtol=1e-13) / T0
def x_of_P(pr, k): return pr ** ((k - 1.0) / k) if False else math.exp(((k - 1.0) / k) * math.log(pr))   # isentrope: ds = 0
def AA_flux(Ma, k):
    xs, fs = flux_max(k); x = x_of_Ma(Ma, k); return fs / flux(x, k)
def Ma_of_AA_ode(Ma1, ratio, k):
    """Hugoniot ODE in ln A: dMa/d lnA = Ma (1 + (k-1)Ma^2/2)/(Ma^2 - 1) from lnA = 0 to ln ratio (never crosses Ma = 1)."""
    s = solve_ivp(lambda x, y: [y[0] * (1 + (k - 1) / 2 * y[0] ** 2) / (y[0] ** 2 - 1)], [0.0, math.log(ratio)], [Ma1], rtol=1e-11, atol=1e-13); return s.y[0, -1]
def Ma_of_AA_flux(r, k, branch):
    """Ma from A/A* by brentq on the flux ratio."""
    if branch == 'sub': return brentq(lambda M: AA_flux(M, k) - r, 1e-4, 1 - 1e-9, xtol=1e-12)
    return brentq(lambda M: AA_flux(M, k) - r, 1 + 1e-9, 12.0, xtol=1e-12)
def mflux_state(T0, P0, k, R, x):
    """mass flux rho V [kg/(m2 s)] at x = T/T0 (rho0 from P0 kPa and R kJ/(kg K) in kg/m3)."""
    rho0 = P0 / (R * T0); return rho0 * x ** (1.0 / (k - 1.0)) * math.sqrt(2000.0 * cp_(k, R) * T0 * (1.0 - x))

# ---------------------------------------------------------------- node (thermo.js) calls
def node(js):
    r = subprocess.run(['node', '-e', f"const T=require({json.dumps(os.path.join(ROOT, '_shared', 'thermo.js'))});console.log({js})"], capture_output=True, text=True, timeout=60)
    if r.returncode: raise RuntimeError(r.stderr[:400])
    return json.loads(r.stdout)

# ---------------------------------------------------------------- route B per (model, out)
TOL = collections.OrderedDict()
def B(model, out, p):
    k = p.get('k'); R = p.get('R', 0.287)
    if model == 'stag':
        cp = p.get('cp', cp_(k, R)); T0, P0 = stag_ode(p['T'], p['P'], p['V'], cp, R, k)
        return dict(T0=T0, P0=P0, Ma=p['V'] / c_num(p['T'], k, R))[out], 2e-4
    if model == 'stagP':
        I, _ = quad(lambda t: k / (k - 1.0) / t, p['T'], p['T0']); return p['P'] * math.exp(I), 1e-7
    if model == 'stagMa':
        T, Pp, Ma = p['T'], p['P'], p['Ma']; Vv = Ma * c_num(T, k, R); cp = cp_(k, R); T0, P0 = stag_ode(T, Pp, Vv, cp, R, k)
        return dict(V=Vv, T0=T0, P0=P0, rho0=P0 / (R * T0))[out], 1e-6
    if model == 'stat_Ma':
        x = x_of_Ma(p['Ma'], k, R, p['T0']); return dict(T=p['T0'] * x, P=p['P0'] * math.exp(k / (k - 1.0) * math.log(x)))[out], 1e-6
    if model == 'stat':
        cp = p.get('cp', cp_(k, R)); T = brentq(lambda t: p['T0'] - t - p['V'] ** 2 / (2000.0 * cp), 1.0, p['T0']); return dict(T=T, P=p['P0'] * math.exp(k / (k - 1.0) * math.log(T / p['T0'])))[out], 1e-6
    if model == 'stat_var':                        # A-17 against CoolProp ideal-gas air
        T0, P0, Vv = p['T0'], p['P0'], p['V']; pref = 100.0
        hC = lambda T: CP.PropsSI('H', 'T', T, 'P', pref, 'Air') / 1000.0; sC = lambda T: CP.PropsSI('S', 'T', T, 'P', pref, 'Air') / 1000.0
        T = brentq(lambda t: hC(t) - (hC(T0) - Vv ** 2 / 2000.0), 300.0, T0); Pv = P0 * math.exp((sC(T) - sC(T0)) / 0.287)
        return (T, {'abs': 1.5}) if out == 'T' else (Pv, 6e-3)
    if model == 'comp':
        pr = p['pr']; T01 = p['T01']; kk, RR = k, R
        T02 = isentrope_T(T01, 1.0, pr, kk)
        if out == 'T02': return T02, 1e-7
        w, _ = quad(lambda x: RR * isentrope_T(T01, 1.0, math.exp(x), kk), 0.0, math.log(pr), epsabs=1e-10); w = abs(w)
        if out == 'w': return w, 1e-3                       # slide uses cp = 1.005 where kR/(k-1) = 1.0045 (0.05 %)
        return w * p['mdot'], 1e-3
    if model == 'isenP':
        T = isentrope_T(p['T0'], p['P0'], p['P'], k); cp = cp_(k, R); Vv = math.sqrt(2000.0 * (quad(lambda t: cp, T, p['T0'])[0]))
        rho = p['P'] / (R * T); c = c_num(T, k, R)
        return dict(T=T, V=Vv, rho=rho, c=c, A=(p['mdot'] / (rho * Vv) * 1e4 if Vv > 0 else float('inf')), Ma=Vv / c)[out], 1e-6
    if model == 'crit':
        xs, fs = flux_max(k); return dict(TT=xs, PP=math.exp(k / (k - 1.0) * math.log(xs)))[out], 1e-6
    if model == 'critst':
        xs, fs = flux_max(k); Ts = xs * p['T0']; Ps = p['P0'] * math.exp(k / (k - 1.0) * math.log(xs)); cp = cp_(k, R)
        return dict(Ts=Ts, Ps=Ps, rhos=Ps / (R * Ts), Vs=math.sqrt(2000.0 * cp * (p['T0'] - Ts)))[out], 1e-6
    if model == 'choked':
        xs, fs = flux_max(k); return p['A'] * mflux_state(p['T0'], p['P0'], k, R, xs), 1e-6
    if model == 'cnoz':
        xs, fs = flux_max(k); Pcrit = p['P0'] * math.exp(k / (k - 1.0) * math.log(xs)); Pe = max(p['Pb'], Pcrit)
        x = math.exp((k - 1.0) / k * math.log(Pe / p['P0'])); Te = p['T0'] * x; Vv = math.sqrt(2000.0 * cp_(k, R) * (p['T0'] - Te)); rho = Pe / (R * Te)
        return dict(Pe=Pe, Ma=Vv / c_num(Te, k, R), V=Vv, mdot=rho * Vv * p['A'])[out], 1e-6
    if model == 'isenMa':
        return AA_flux(p['Ma'], k), 1e-6
    if model == 'duct':
        Ma1, red = p['Ma1'], p['A2A1']; x1 = x_of_Ma(Ma1, k); Ma2 = Ma_of_AA_ode(Ma1, red, k); x2 = x_of_Ma(Ma2, k)
        pw = k / (k - 1.0)
        d = dict(Ma2=(Ma2, 1e-6), TT2=(x2, 1e-6), PP2=(x2 ** pw, 1e-6))
        if 'T1' in p: d['T2'] = (p['T1'] * x2 / x1, 1e-6)
        if 'P1' in p: d['P2'] = (p['P1'] * (x2 / x1) ** pw, 1e-6)
        return d[out]
    if model == 'diffuser':
        pw = k / (k - 1.0); x1 = x_of_Ma(p['Ma1'], k, R, 1000.0); x2 = x_of_Ma(p['Ma2'], k, R, 1000.0); T0 = p['T1'] / x1; P0 = p['P1'] / x1 ** pw
        if out == 'dP': return P0 * x2 ** pw - p['P1'], 1e-6
        V1 = p['Ma1'] * c_num(p['T1'], k, R); A1 = p['mdot'] / (p['P1'] / (R * p['T1']) * V1)           # m2 from mass conservation at section 1
        I, _ = quad(lambda M: (M * M - 1.0) / (M * (1.0 + (k - 1.0) / 2.0 * M * M)), p['Ma1'], p['Ma2'], epsabs=1e-12)       # Hugoniot: d ln A = (Ma^2-1) dMa / [Ma (1 + (k-1)Ma^2/2)]
        return A1 * math.exp(I), 1e-6
    if model == 'areaMa':
        return p['A1'] * AA_flux(p['Ma2'], k) / AA_flux(p['Ma1'], k), 1e-6
    if model == 'sound':
        c = c_num(p['T'], k, R)
        if out == 'c': return c, 1e-6
        if out == 'Ma': return p['V'] / c, 1e-6
        return p['Ma'] * c, 1e-6
    if model == 'isenT':
        T2 = isentrope_T(p['T1'], p['P1'], p['P2'], k); return c_num(p['T1'], k, R) / c_num(T2, k, R), 1e-6
    if model == 'co2noz':
        cp = p['cp']; c1 = c_num(p['T1'], k, p['R']); Vv2 = brentq(lambda v: cp * (p['T1'] - p['T2']) - (v ** 2 - p['V1'] ** 2) / 2000.0, 1.0, 5000.0)
        return dict(Ma1=p['V1'] / c1, V2=Vv2, Ma2=Vv2 / c_num(p['T2'], k, p['R']))[out], 1e-6
    if model == 'co2var':                           # A-20 (props) against CoolProp CO2 ideal gas
        dhC = (CP.PropsSI('H', 'T', p['T1'], 'P', 100.0, 'CO2') - CP.PropsSI('H', 'T', p['T2'], 'P', 100.0, 'CO2')) / 1000.0
        dhT = (props.gas_kmol('CO2', p['T1'], 'h')['value'] - props.gas_kmol('CO2', p['T2'], 'h')['value']) / 44.01
        dh = dhC if True else dhT
        return (dh if out == 'dh' else math.sqrt(p['V1'] ** 2 + 2000.0 * dh)), 1.5e-2
    if model == 'pitot':
        x = math.exp((k - 1.0) / k * math.log(p['P'] / (p['P'] + p['dP']))); T0 = p['T'] / x; Vv = math.sqrt(2000.0 * cp_(k, R) * (T0 - p['T']))
        Ma = Vv / c_num(p['T'], k, R); return (Ma if out == 'Ma' else Vv), 1e-6
    if model == 'sonic':
        cp = p.get('cp', cp_(k, R)); T0, P0 = stag_ode(p['T'], p['P'], p['V'], cp, R, k); xs, fs = flux_max(k); Ts = xs * T0; Ps = P0 * math.exp(k / (k - 1.0) * math.log(xs))
        rho1 = p['P'] / (R * p['T']); rhos = Ps / (R * Ts); Vs = math.sqrt(2000.0 * cp_(k, R) * (T0 - Ts))
        return dict(Ts=Ts, Ps=Ps, Vs=Vs, AsA1=(rho1 * p['V']) / (rhos * Vs))[out], 3e-3
    if model == 'cdexit':
        xs, fs = flux_max(k); cp = cp_(k, R)
        if 'As' in p:                              # throat and exit given Ma_e (Cengel Ex 17-7)
            As = p['As'] * 1e-4; Ts = xs * p['T0']; Ps = p['P0'] * math.exp(k / (k - 1.0) * math.log(xs)); xe = x_of_Ma(p['Mae'], k, R, p['T0']); Te = xe * p['T0']
            d = dict(Ts=Ts, Vs=math.sqrt(2000.0 * cp * (p['T0'] - Ts)), mdot=As * mflux_state(p['T0'], p['P0'], k, R, xs), Pe=p['P0'] * math.exp(k / (k - 1.0) * math.log(xe)),
                     Te=Te, Ae=p['As'] * fs / flux(xe, k), Ve=p['Mae'] * c_num(Te, k, R))
            return d[out], 1e-6
        mA = mflux_state(p['T0'], p['P0'], k, R, xs); As = p['mdot'] / mA; xe = math.exp((k - 1.0) / k * math.log(p['Pe'] / p['P0'])); Te = xe * p['T0']; Vv = math.sqrt(2000.0 * cp * (p['T0'] - Te))
        return dict(As=As * 1e4, Mae=Vv / c_num(Te, k, R), Ae=As * 1e4 * fs / flux(xe, k))[out], 1e-6
    if model == 'A32lin':
        if out == 'AA_exact': return AA_flux(p['Ma'], p['k']), 1e-6
        return 4.2346 + (p['Ma'] - 3.0) / 2.0 * (25.0 - 4.2346), 1e-9
    raise KeyError(model)

# ================================================================== 1. every registry entry by route B
seen = collections.Counter()
for r in V['registry']:
    try: b, tol = B(r['model'], r['out'], r['params'])
    except Exception as e: FAILS.append(f'{r["model"]}.{r["out"]} {r["what"]}: route B error {e!r}'); continue
    rec(f'{r["model"]}.{r["out"]} [{r["what"][:38]}]', r['value'], b, tol); seen[r['model']] += 1

# ================================================================== 2. printed answers (slides and Cengel)
for p in V['printed']:
    rec(f'PRINTED {p["key"]}', p['printed'], p['ours'], p['tol'], p.get('note', ''))

# ================================================================== 3. Table A-32 printed rows (five columns) against closed forms
A32 = json.load(open(os.path.join(ROOT, 'data', 'props', 'A32.json'), encoding='utf-8')); k = 1.4; flagged = []
for row, prec in zip(A32['rows'], A32['prec']):
    Ma = row[0]
    if Ma is None or Ma == 0: continue
    f = dict(Ma_star=Ma * math.sqrt((k + 1) / (2 + (k - 1) * Ma ** 2)), A_Astar=1 / Ma * ((2 / (k + 1)) * (1 + (k - 1) / 2 * Ma ** 2)) ** ((k + 1) / (2 * (k - 1))),
             P_P0=(1 + 0.2 * Ma ** 2) ** -3.5, rho_rho0=(1 + 0.2 * Ma ** 2) ** -2.5, T_T0=(1 + 0.2 * Ma ** 2) ** -1)
    for j, col in enumerate(A32['columns'][1:], 1):
        pv = row[j]
        if pv is None: continue
        half = 0.5 * 10 ** (-prec[j]) * 1.001
        if abs(pv - f[col]) > half: flagged.append((Ma, col, pv, f[col]))
        else: rec(f'A32 Ma={Ma} {col}', pv, f[col], {'abs': half})
print('A-32 cells outside half a unit of the last printed digit:', [(m, c, pv, round(fv, 5)) for m, c, pv, fv in flagged])
assert flagged == [(3.0, 'rho_rho0', 0.076, flagged[0][3])] and abs(flagged[0][3] - 0.0762) < 1e-4, flagged
# the flagged printed error is reproduced by the library as suspect and must not be used by any question
ci = props.isentropic(3.0, 'rho_rho0'); assert ci['suspect'] is True, ci
ITEMS = json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm05.json'), encoding='utf-8')) + json.load(open(os.path.join(ROOT, 'data', 'qsrc', 'm05_gen.json'), encoding='utf-8'))
used = [i['src']['en'] for i in ITEMS if '0.0760' in json.dumps(i['q'], ensure_ascii=False) or '0,0760' in json.dumps(i['q'], ensure_ascii=False)]
if used: FAILS.append(f'question text uses the flagged A-32 cell: {used}')
# library vs closed form at printed rows (props.isentropic exact rows)
for Ma in (0.3, 0.8, 1.0, 1.2, 2.0, 2.4, 3.0, 5.0):
    rec(f'PROPS A_Astar Ma={Ma}', props.isentropic(Ma, 'A_Astar')['value'], AAs_ := (1 / Ma) * ((2 / 2.4) * (1 + 0.2 * Ma * Ma)) ** 3, {'abs': 5.1e-5 if Ma < 5 else 5.1e-4})

# ================================================================== 4. interpolation of A-32 between sparse rows (warning quoted in the notes)
lin = props.isentropic(3.5, 'A_Astar'); ex = AA_flux(3.5, 1.4)
rec('A32 interpolation A/A*(3.5) linear vs exact (expected +39 %)', lin['value'], ex, 0.40)
assert 0.38 < lin['value'] / ex - 1 < 0.40, lin['value'] / ex
lin4 = props.isentropic(4.0, 'P_P0')['value']; ex4 = math.exp(3.5 * math.log(x_of_Ma(4.0, 1.4))); assert 2.1 < lin4 / ex4 < 2.3, (lin4, ex4)   # +121 %: the '+120 %' of the library warning

# ================================================================== 5. _shared/thermo.js through node
calls = []
for r in V['registry']:
    p = r['params']; m, o = r['model'], r['out']
    if m == 'stag' and o in ('T0', 'P0', 'Ma') and abs(p.get('cp', 0) - cp_(p['k'], p['R'])) < 1e-3 * 1.005: calls.append((r, f"JSON.stringify(T.stagnation({{T:{p['T']},P:{p['P']},V:{p['V']},k:{p['k']},R:{p['R']}}}))", {'T0': 'T0', 'P0': 'P0', 'Ma': 'Ma'}[o], 4e-4))
    if m == 'choked' and o == 'mdot': calls.append((r, f"JSON.stringify(T.chokedMdot({{Astar:{p['A']},P0:{p['P0']},T0:{p['T0']},k:{p['k']},R:{p['R']}}}))", None, 1e-9))
    if m == 'cnoz': calls.append((r, f"JSON.stringify(T.convergingNozzle({{T:{p['T0']},P:{p['P0']},V:0,k:{p['k']},R:{p['R']},Pb:{p['Pb']},Ae:{p['A']}}}))", {'Pe': 'Pe', 'Ma': 'Ma', 'V': 'V', 'mdot': 'mdot'}[o], 1e-9))
    if m == 'duct': calls.append((r, f"JSON.stringify(T.duct({{Ma1:{p['Ma1']},A2A1:{p['A2A1']},k:{p['k']},branch:'{p['branch']}'" + (f",T1:{p['T1']},P1:{p['P1']}" if 'T1' in p else '') + '}))', {'Ma2': 'Ma2', 'TT2': 'T2T0', 'PP2': 'P2P0', 'T2': 'T2', 'P2': 'P2'}[o], 1e-9))
    if m == 'critst' and o in ('Ps', 'Ts'): calls.append((r, f"JSON.stringify(T.critical({{k:{p['k']}}}))", None, 1e-9))
    if m == 'isenMa': calls.append((r, f"JSON.stringify(T.fromMa({p['Ma']},{p['k']}))", 'AAs', 1e-9))
nn = 0
for r, js, key, tol in calls:
    d = node(js); p = r['params']; o = r['out']
    if r['model'] == 'choked': v = d
    elif r['model'] == 'critst': v = d['PsP0'] * p['P0'] if o == 'Ps' else d['TsT0'] * p['T0']
    else: v = d[key]
    # thermo.js uses cp = kR/(k-1) and no rounding: compare with the A value at the tolerance of the model
    rec(f'NODE {r["model"]}.{o} [{r["what"][:34]}]', r['value'], v, 1e-3 if r['model'] == 'stag' else max(tol, 1e-6)); nn += 1   # thermo.js: cp = kR/(k-1) = 1.0045 against the slide's 1.005 (0.05 % in V^2/2cp)
print('node thermo.js comparisons:', nn)

# ================================================================== 6. report
w = max(len(r[0]) for r in ROWS)
for name, a, b, err, lim, st in ROWS[:0]: pass
print(f'{"item":<{w}} {"A (stored)":>14} {"B (indep.)":>14} {"rel/abs err":>11} {"tol":>8}  ')
for name, a, b, err, lim, st in ROWS:
    if st != 'ok' or err > 0.3 * lim: print(f'{name:<{w}} {a:>14.7g} {b:>14.7g} {err:>11.3g} {lim:>8.2g}  {st}')
print(f'\n{len(ROWS)} comparisons ({sum(seen.values())} registry values by route B, {len(V["printed"])} printed answers, A-32 rows, node thermo.js); models: {dict(seen)}')
print('largest error/tolerance per family:', {k_: round(v, 3) for k_, v in sorted(DEV.items(), key=lambda kv: -kv[1])[:12]})
if FAILS:
    print('FAILS:'); [print(' -', f) for f in FAILS]; sys.exit(1)
print('FAILS: none')
