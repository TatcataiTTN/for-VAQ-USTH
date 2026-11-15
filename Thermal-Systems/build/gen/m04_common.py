"""Shared helpers for module m04 (fuels and combustion): ROUTE A = what a student does by hand with the lecturer's conventions
(rounded atomic masses C = 12, H = 1, O = 16, N = 14 and M_air = 29 as on the slides and in Cengel's examples; dew point = A-5 linear interpolation;
enthalpies = A-26 (h_f), A-27 (heating values) and A-18...A-25 (h(T), linear between rows)), number formatting, item constructors and a registry of every
numeric answer (data/verify/m04_values.json) that build/verify/verify_m04.py recomputes by a DIFFERENT route (sympy element matrix, iapws, A-27, A-2c cp(T),
CoolProp ideal-gas enthalpy, integral of T ds0 from the same tables).
Run with the project venv:  .venv/bin/python -I build/gen/gen_m04.py   (props needs the venv)."""
import json, math, os, sys, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'props'))
import props
REG = []                                       # registry: dict(model, params, out, value, tol, what)
AT = dict(C=12.0, H=1.0, O=16.0, N=14.0)       # rounded atomic masses (route A, slides tr.17/30/36 use 12, 2 (H2), 29 (air))
MAIR = 29.0                                    # rounded molar mass of air used on the slides (tr.14 prints 28.97)
R3 = 3.76                                      # kmol N2 per kmol O2 in dry air (0.79/0.21)
AIR = 1 + R3                                   # 4.76 kmol air per kmol O2
ATX = dict(C=12.011, H=1.008, O=15.9995, N=14.0065)     # "exact" atomic masses (A-1 / A-27: C 12.011, H2 2.016, O2 31.999, N2 28.013); M_air = 28.97 (A-1)
MAIRX = 28.97

def reg(model, params, out, value, tol=2e-3, what=''):
    """tol: relative tolerance, or {'abs': x} for an absolute one."""
    REG.append(dict(model=model, params=params, out=out, value=value, tol=tol, what=what)); return value

def N(x, nd=2):
    """English-style number: thousands comma, decimal point, minus sign U+2212 (assemble.py localises the Vietnamese text)."""
    return f'{x:,.{nd}f}'.replace('-', '−')

# ---------------------------------------------------------------- item constructors (same schema as m01..m03)
TOK = re.compile(r'(?<![\w.,])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+)(?!\w|[.,]\d)')
def loc(s): return s.replace(',', '\0').replace('.', ',').replace('\0', '.')
ANYNUM = re.compile(r'(?<![\w.,])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+,\d+|\d{1,3}(?: \d{3})+(?!\d))(?![\w]|[.,]\d)')
def fixvi(vi, en):
    """Numbers typed by hand in the Vietnamese text (decimal comma '2,256', thousands space '393 520') are put into the English notation when the English text does not contain
    the token as written, so that loc_text() can localise every number the same way; a token that is also in the English text is an English-format number (kept as is)."""
    def rep(m):
        t = m.group(0)
        if t in en: return t
        if ' ' in t:
            e = t.replace(' ', ','); return e if e in en else t
        if re.fullmatch(r'\d+,\d+', t): return t.replace(',', '.')
        return t
    return ANYNUM.sub(rep, vi)
def loc_text(vi, en):
    """English-formatted numbers of the Vietnamese text that also occur verbatim in the English text become Vietnamese (1.575,1 / 0,287)."""
    vi = fixvi(vi, en)
    return TOK.sub(lambda m: loc(m.group(0)) if m.group(0) in en else m.group(0), vi)
def B(vi, en): return dict(vi=loc_text(vi, en), en=en)
def opt(txt): return dict(vi=loc_text(txt, txt), en=txt)
def mcq(q, opts, correct, expl, level, topic, src, origin, check, fig=None, fixed=False):
    d = dict(kind='mcq', q=q, opts=opts, correct=correct, explain=expl, level=level, topic=topic, src=src, origin=origin, fixed_order=fixed, check=check)
    if fig: d['fig'] = fig
    return d
def tf(q, truth, expl, level, topic, src, origin, check):
    opts = [B('Đúng', 'True'), B('Sai', 'False')]
    return dict(kind='tf', q=q, opts=opts, correct=0 if truth else 1, explain=expl, level=level, topic=topic, src=src, origin=origin, fixed_order=True, check=check)
def ess(q, sol, level, topic, src, origin, check, fig=None):
    d = dict(kind='ess', q=q, sol=sol, level=level, topic=topic, src=src, origin=origin, fixed_order=False, check=check)
    if fig: d['fig'] = fig
    return d
def numopts(correct, wrongs, unit='', nd=2):
    """option list (same text in both languages), correct first; wrongs: floats, deduplicated after rounding."""
    vals = [correct]; seen = {N(correct, nd)}
    for w in wrongs:
        if N(w, nd) not in seen: vals.append(w); seen.add(N(w, nd))
    u = (' ' + unit) if unit else ''
    return [opt(N(v, nd) + u) for v in vals]
def textopts(correct, wrongs):
    seen = {correct}; out = [opt(correct)]
    for w in wrongs:
        if w not in seen: out.append(opt(w)); seen.add(w)
    return out
def dump(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)

# ================================================================== species and fuels (route A)
# element content per kmol of species: C, H, O, N atoms
SP = dict(CH4=dict(C=1, H=4), C2H2=dict(C=2, H=2), C2H4=dict(C=2, H=4), C2H6=dict(C=2, H=6), C3H6=dict(C=3, H=6), C3H8=dict(C=3, H=8), C4H10=dict(C=4, H=10),
          C6H6=dict(C=6, H=6), C8H18=dict(C=8, H=18), C12H26=dict(C=12, H=26), H2=dict(H=2), CO=dict(C=1, O=1), CH3OH=dict(C=1, H=4, O=1),
          C2H5OH=dict(C=2, H=6, O=1), C3H7OH=dict(C=3, H=8, O=1), N2=dict(N=2), O2=dict(O=2), CO2=dict(C=1, O=2), C=dict(C=1))
def el(f, k): return SP[f].get(k, 0)
def Mf(f):
    """molar mass with the rounded atomic masses (route A)."""
    return sum(AT[k] * v for k, v in SP[f].items())
def mix(parts):
    """gaseous fuel mixture given as [(species, mole fraction)]: element content and molar mass per kmol of mixture."""
    e = dict(C=0.0, H=0.0, O=0.0, N=0.0); M = 0.0
    for f, y in parts:
        for k, v in SP[f].items(): e[k] += y * v
        M += y * Mf(f)
    return dict(C=e['C'], H=e['H'], O=e['O'], N=e['N'], M=M)
def single(f): return mix([(f, 1.0)])
def MfX(f): return sum(ATX[k] * v for k, v in SP[f].items())
def mixX(parts):
    """same as mix() with the exact masses of A-1 / A-27 (used where the printed answer needs them, e.g. Cengel 15-104)."""
    r = mix(parts); r['M'] = sum(y * MfX(f) for f, y in parts); return r
def parts_fuel(parts, exact=False): return (mixX if exact else mix)([(f, y) for f, y in parts])

def combustion(fuel, lam=1.0, moist=0.0, h2o_fuel=0.0, exact=False):
    """Complete combustion of 1 kmol of fuel (dict C, H, O, N, M) with lam = fraction of theoretical air (1.2 = 120 % theoretical = 20 % excess).
    moist: kmol of water vapour entering with the air per kmol of fuel; h2o_fuel: kmol of H2O accompanying the fuel (inert).
    Products: CO2, H2O, O2 (excess), N2.  Returns kmol per kmol fuel and the mass air-fuel ratio with the rounded masses (route A)."""
    ath = fuel['C'] + fuel['H'] / 4.0 - fuel['O'] / 2.0          # theoretical O2 per kmol fuel (the O in the fuel counts)
    o2_in = lam * ath; n2_in = R3 * o2_in; air = o2_in * AIR
    co2 = fuel['C']; h2o = fuel['H'] / 2.0 + moist + h2o_fuel; o2 = (lam - 1.0) * ath; n2 = n2_in + fuel['N'] / 2.0
    n_dry = co2 + o2 + n2; n_tot = n_dry + h2o
    return dict(ath=ath, o2_in=o2_in, n2_in=n2_in, air=air, CO2=co2, H2O=h2o, O2=o2, N2=n2, n_dry=n_dry, n_tot=n_tot, AF=air * (MAIRX if exact else MAIR) / fuel['M'], AF_mol=air)

def dew_point(n_v, n_tot, P_kPa):
    """dew point = T_sat at P_v = (N_v/N_prod) P (slides tr.31-32); A-5 linear interpolation (route A)."""
    Pv = n_v / n_tot * P_kPa
    return Pv, props.sat_P('water', Pv, 'Tsat_C')['value']

def condensed(n_v, n_tot, P_kPa, T_C):
    """kmol of H2O that condenses when the products are cooled to T_C at P (slide tr.38-39): (Nv - Nw)/(Ntot - Nw) = Psat/P."""
    r = props.sat_T('water', T_C, 'Psat_kPa')['value'] / P_kPa
    return (n_v - r * n_tot) / (1.0 - r)

def reverse(c, h, CO2, CO, O2, N2):
    """Reverse analysis (slides tr.33-39): x CcHh + a(O2+3.76N2) -> CO2 + CO + O2 + N2 + b H2O for 100 kmol of dry products.
    Mass balances N2, C, H (the O2 balance is a check).  Returns per kmol of fuel."""
    a = N2 / R3; x = (CO2 + CO) / c; b = h * x / 2.0
    resid = a - (CO2 + CO / 2.0 + O2 + b / 2.0)            # O2 balance must close (slide: 22.20 = 22.20)
    th = c + h / 4.0; Mfuel = AT['C'] * c + AT['H'] * h
    return dict(a=a, x=x, b=b, resid=resid, air=a / x * AIR, th=th, pct=a / x / th * 100.0, AF=a / x * AIR * MAIR / Mfuel,
                CO2=CO2 / x, CO=CO / x, O2=O2 / x, N2=N2 / x, H2O=b / x, n_tot=(CO2 + CO + O2 + N2 + b) / x)

# ================================================================== enthalpies (route A: A-26, A-27, A-18...A-25)
def hf(key): return props.formation(key, 'hf0')['value']         # kJ/kmol, A-26
FORM = dict(CO2='CO2(g)', CO='CO(g)', H2O_g='H2O(g)', H2O_l='H2O(ᐉ)', H2='H2(g)', O2='O2(g)', N2='N2(g)', C='C(s)', CH4='CH4(g)', C2H2='C2H2(g)', C2H4='C2H4(g)', C2H6='C2H6(g)',
            C3H6='C3H6(g)', C3H8='C3H8(g)', C4H10='C4H10(g)', C8H18_g='C8H18(g)', C8H18_l='C8H18(ᐉ)', C12H26='C12H26(g)', C6H6='C6H6(g)', CH3OH_g='CH3OH(g)',
            CH3OH_l='CH3OH(ᐉ)', C2H5OH_g='C2H5OH(g)', C2H5OH_l='C2H5OH(ᐉ)')
def HF(k): return hf(FORM[k])
A27 = dict(CH4='Methane (g)', C2H6='Ethane (g)', C2H2='Acetylene (g)', H2='Hydrogen (g)', CO='Carbon monoxide (g)', C8H18='Octane (ᐉ)', C3H8='Propane (ᐉ)', C4H10='Butane (ᐉ)',
           C6H6='Benzene (ᐉ)', C2H5OH='Ethanol (ᐉ)', CH3OH='Methanol (ᐉ)', C='Carbon (s)')
_A27 = None
def A27row(k, col):
    """A-27 cell read from data/props/A27.json by exact fuel name (the library's fuzzy match confuses Methane/Ethane)."""
    global _A27
    if _A27 is None:
        d = json.load(open(os.path.join(ROOT, 'data', 'props', 'A27.json'), encoding='utf-8')); _A27 = {r[0]: dict(zip(d['columns'], r)) for r in d['rows']}
    return _A27[A27[k]][col]
def hC_nu(fuel_key, nu_prod, water='l'):
    """enthalpy of combustion at 25 C, 1 atm from A-26: sum N_p hf_p - 1*hf_fuel (kJ/kmol fuel); nu_prod = {species: kmol}."""
    hP = sum(n * HF(s if s != 'H2O' else 'H2O_' + water) for s, n in nu_prod.items())
    return hP - HF(fuel_key)

def A_gas(g):
    return json.load(open(os.path.join(ROOT, 'data', 'props', f'A{ {"N2":18,"O2":19,"CO2":20,"CO":21,"H2":22,"H2O":23,"O":24,"OH":25}[g] }.json'), encoding='utf-8'))
_TAB = {}
def tab(g):
    if g not in _TAB: _TAB[g] = [(r[0], r[1]) for r in A_gas(g)['rows'] if r[0] > 0]
    return _TAB[g]
def hbar(g, T):
    """h(T) in kJ/kmol from A-18..A-25, linear interpolation between rows (the book's method)."""
    t = tab(g)
    for (T0, h0), (T1, h1) in zip(t, t[1:]):
        if T0 <= T <= T1: return h0 + (T - T0) / (T1 - T0) * (h1 - h0)
    raise ValueError(f'{g}: {T} K outside the table')
def sens(g, T): return hbar(g, T) - hbar(g, 298.0)                  # h(T) - h(298 K): sensible enthalpy relative to the standard reference state (slide tr.44)
def Tinv(g, hval):
    """T from h (kJ/kmol) by linear interpolation in the table (students' method)."""
    t = tab(g)
    for (T0, h0), (T1, h1) in zip(t, t[1:]):
        if h0 <= hval <= h1: return T0 + (hval - h0) / (h1 - h0) * (T1 - T0)
    raise ValueError('h outside the table')

def Hstate(comp, T):
    """absolute enthalpy of a mixture {species-key: kmol} at T relative to the standard state: sum N (hf + h(T) - h298).  species keys are A-26 keys for hf
    and gas names for the table (CO2, H2O_g, N2 ... -> table gas name)."""
    tot = 0.0
    for s, n in comp.items():
        g = s.split('_')[0] if s in ('H2O_g', 'H2O_l') else s
        tot += n * (HF(s) + (sens(g, T) if g in ('N2', 'O2', 'CO2', 'CO', 'H2', 'H2O') and s != 'H2O_l' else 0.0))
    return tot

def q_out(react, T_r, prod, T_p):
    """heat transferred OUT of the chamber per kmol fuel (positive = loss): H_react - H_prod (steady flow, no work)."""
    return Hstate(react, T_r) - Hstate(prod, T_p)

def T_adiabatic(react, T_r, prod, lo=298.0, hi=3200.0, tol=1e-6):
    """adiabatic flame temperature by bisection on the table-interpolated enthalpy (route A)."""
    target = Hstate(react, T_r)
    f = lambda T: Hstate(prod, T) - target
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0: hi = mid
        else: lo = mid
        if hi - lo < tol: break
    return (lo + hi) / 2
