"""Shared helpers for module m03 (refrigeration cycles and aircraft air conditioning): ROUTE A = what a student does by hand
(R-134a: A-11/A-12/A-13 read exactly, h2 by linear interpolation in s as in the book; air: closed forms with k = 1.4, cp = 1.005, or A-17 with P_r),
number formatting, item constructors, and a registry of every numeric answer (data/verify/m03_values.json) that build/verify/verify_m03.py
recomputes by a DIFFERENT route (CoolProp R134a / CoolProp Air / cp(T) integration / sympy).
Run with the project venv:  .venv/bin/python -I build/gen/gen_m03.py   (props needs the venv)."""
import json, math, os, sys, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'props'))
import props
REG = []                                       # registry: dict(model, params, out, value, tol, what)
K_AIR = 1.4; CP_AIR = 1.005; R_AIR = 0.287; CV_AIR = 0.718      # Table A-2a at 300 K
PSI = 6.894757                                 # kPa per psi (1 psi = 6.894757 kPa)
TON = 211.0 / 60.0                             # 1 ton of refrigeration = 211 kJ/min (Cengel p.609) = 3.5167 kW

def reg(model, params, out, value, tol=2e-3, what=''):
    """tol: relative tolerance, or {'abs': x} for an absolute one."""
    REG.append(dict(model=model, params=params, out=out, value=value, tol=tol, what=what)); return value

def N(x, nd=2):
    """English-style number: thousands comma, decimal point, minus sign U+2212 (assemble.py localises the Vietnamese text)."""
    return f'{x:,.{nd}f}'.replace('-', '−')

# ---------------------------------------------------------------- item constructors (same schema as m01/m02)
TOK = re.compile(r'(?<![\w.,])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+)(?!\w|[.,]\d)')
def loc(s): return s.replace(',', '\0').replace('.', ',').replace('\0', '.')
def loc_text(vi, en):
    """English-formatted numbers of the Vietnamese text that also occur verbatim in the English text become Vietnamese (1.575,1 / 0,287)."""
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

# ================================================================== R-134a, route A: tables A-11, A-12, A-13 (props library, rows read from the page images)
def sP(P_kPa, prop): return props.sat_P('R134a', P_kPa, prop)['value']          # A-12 (exact rows only in this module)
def sT(T_C, prop): return props.sat_T('R134a', T_C, prop)['value']              # A-11
def shP(P_MPa, T_C, prop): return props.superheated('R134a', P_MPa, T_C, prop)['value']   # A-13 (exact grid points only)
def h_at_s(P_MPa, s):
    """superheated state at pressure P_MPa and entropy s: linear interpolation in s inside the A-13 block (the book's method)."""
    r = props.superheated_inverse('R134a', P_MPa, 's', s)['extra']
    return r['h'], r['T_C']

def vcrc_ideal(Pl_kPa, Ph_kPa):
    """Ideal vapour-compression cycle (slides tr.15-25): 1 sat. vapour at Pl, 1-2 isentropic to Ph, 3 sat. liquid at Ph, 3-4 throttle (h4 = h3)."""
    h1 = sP(Pl_kPa, 'hg'); s1 = sP(Pl_kPa, 'sg'); h3 = sP(Ph_kPa, 'hf')
    h2, T2 = h_at_s(Ph_kPa / 1000.0, s1); h4 = h3
    hf_l, hg_l = sP(Pl_kPa, 'hf'), sP(Pl_kPa, 'hg')
    qL = h1 - h4; w = h2 - h1; qH = h2 - h3
    return dict(h1=h1, h2=h2, h3=h3, h4=h4, s1=s1, T2=T2, qL=qL, w=w, qH=qH, cop=qL / w, cop_hp=qH / w, x4=(h4 - hf_l) / (hg_l - hf_l),
                Tl=sP(Pl_kPa, 'Tsat_C'), Th=sP(Ph_kPa, 'Tsat_C'), hfg_l=hg_l - hf_l)

def carnot_R(TL_K, TH_K): return 1.0 / (TH_K / TL_K - 1.0)
def carnot_HP(TL_K, TH_K): return 1.0 / (1.0 - TL_K / TH_K)

# ================================================================== gas refrigeration (reversed Brayton), constant specific heats (route A)
def gas_simple(T1, T3, rp, k=K_AIR, cp=CP_AIR, etac=1.0, etat=1.0):
    """Cengel Fig. 11-16: 1 compressor inlet (= cold-space outlet), 2 compressor exit, 3 turbine inlet (cooled to ambient), 4 turbine exit (coldest)."""
    x = rp ** ((k - 1) / k)
    T2 = T1 + T1 * (x - 1) / etac; T4 = T3 - etat * (T3 - T3 / x)
    qL = cp * (T1 - T4); wc = cp * (T2 - T1); wt = cp * (T3 - T4); w = wc - wt
    return dict(T2=T2, T4=T4, qL=qL, wc=wc, wt=wt, w=w, cop=qL / w, qH=cp * (T2 - T3), x=x)
def gas_regen(T1, T3, T4, rp, k=K_AIR, cp=CP_AIR, etac=1.0, etat=1.0):
    """Cengel Fig. 11-19 (Prob. 11-61): T3 after the heat sink, T4 after the regenerator (turbine inlet), T6 = T1 - (T3 - T4) from the regenerator balance."""
    x = rp ** ((k - 1) / k)
    T2 = T1 + T1 * (x - 1) / etac; T5 = T4 - etat * (T4 - T4 / x); T6 = T1 - (T3 - T4)
    qL = cp * (T6 - T5); wc = cp * (T2 - T1); wt = cp * (T4 - T5); w = wc - wt
    return dict(T2=T2, T5=T5, T6=T6, qL=qL, wc=wc, wt=wt, w=w, cop=qL / w)
def cop_gas_closed(rp, k=K_AIR): return 1.0 / (rp ** ((k - 1) / k) - 1.0)      # simple ideal cycle, constant cp: COP = 1/(x - 1)

def c2k(c): return c + 273.15

def vcrc_real(P1_MPa, T1_C, P2_MPa, T2_C=None, eta_c=None, T3_C=None, sat_liquid_P_kPa=None):
    """Actual cycle (Cengel §11-4 style): state 1 superheated vapour read at a grid point of A-13; compressor exit either given (T2_C at P2_MPa) or from eta_c
    (h2 = h1 + (h2s - h1)/eta_c); condenser exit compressed liquid h3 ~ hf at T3_C (A-11), or saturated liquid at sat_liquid_P_kPa (A-12); h4 = h3."""
    h1 = shP(P1_MPa, T1_C, 'h'); s1 = shP(P1_MPa, T1_C, 's'); v1 = shP(P1_MPa, T1_C, 'v')
    h2s, T2s = h_at_s(P2_MPa, s1)
    if eta_c is not None: h2 = h1 + (h2s - h1) / eta_c
    else: h2 = shP(P2_MPa, T2_C, 'h')
    h3 = sT(T3_C, 'hf') if T3_C is not None else sP(sat_liquid_P_kPa, 'hf')
    qL = h1 - h3; w = h2 - h1; qH = h2 - h3
    return dict(h1=h1, s1=s1, v1=v1, h2s=h2s, T2s=T2s, h2=h2, h3=h3, h4=h3, qL=qL, w=w, qH=qH, cop=qL / w, eta_c=(h2s - h1) / w)

def rows_at_s(P_MPa, s):
    """the two A-13 rows (saturated row and/or superheated rows) between which h2 is interpolated, as [(T_C, s, h), ...] for the worked solutions."""
    r = props.superheated_inverse('R134a', P_MPa, 's', s)
    return [(x['key']['T_C'], x['cells']['s']) for x in r['rows_used']], r['extra']['h'], r['extra']['T_C']

def interp_line(x, x0, x1, y0, y1): return y0 + (x - x0) / (x1 - x0) * (y1 - y0)

_A2A = {r[0]: r for r in json.load(open(os.path.join(ROOT, 'data', 'props', 'A2a.json'), encoding='utf-8'))['rows']}
HE_CP = _A2A['Helium'][3]; HE_K = _A2A['Helium'][5]            # Table A-2a: cp = 5.1926 kJ/(kg K), k = 1.667
