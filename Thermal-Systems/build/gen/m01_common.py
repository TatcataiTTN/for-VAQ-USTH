"""Shared helpers for module m01: route-A formulas (closed forms), number formatting, item constructors, registry of every
numeric answer (data/verify/m01_values.json) that build/verify/verify_m01.py recomputes by a DIFFERENT route (route B)."""
import json, math, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
G0 = 9.80665; R_AIR = 287.0; GAM = 1.4
REG = []          # registry of numeric results: dict(kind, params, value, tol)

def reg(kind, params, value, tol=2e-3):
    REG.append(dict(kind=kind, params=params, value=value, tol=tol)); return value

def N(x, nd=2):
    """English-style number: thousands comma, decimal point (assemble.py localises the Vietnamese text: decimal comma, thousands dot)."""
    s = f'{x:,.{nd}f}'
    return s.replace('-', '−')

# ---------------------------------------------------------------- ISA (route A: closed forms of the 1976 standard atmosphere, 0-32 km)
def isa(z_m):
    T0, p0, L, R, g = 288.15, 101325.0, 0.0065, 287.053, 9.80665
    if z_m <= 11000:
        T = T0 - L * z_m; p = p0 * (T / T0) ** (g / (R * L))
    elif z_m <= 20000:
        T = 216.65; p11 = p0 * (216.65 / T0) ** (g / (R * L)); p = p11 * math.exp(-g * (z_m - 11000) / (R * 216.65))
    else:
        p11 = p0 * (216.65 / T0) ** (g / (R * L)); p20 = p11 * math.exp(-g * 9000 / (R * 216.65))
        T = 216.65 + 0.001 * (z_m - 20000); p = p20 * (T / 216.65) ** (-g / (R * 0.001))
    return T, p, p / (R * T)

# ---------------------------------------------------------------- thrust and efficiencies (route A)
def thrust(ma, f, ue, u, pe=None, pa=None, Ae=0.0):
    return ma * ((1 + f) * ue - u) + ((pe - pa) * Ae if pe is not None else 0.0)
def eta_p_first(T, u, me, ue):                  # El-Sayed Eq. 2.7a, wake = 1/2 me (ue-u)^2
    return T * u / (T * u + 0.5 * me * (ue - u) ** 2)
def eta_p_simple(u, ue): return 2 * u / (u + ue)
def eta_th_unchoked(f, ue, u, QR): return ((1 + f) * ue ** 2 - u ** 2) / (2 * f * QR)
def breguet(eta_o, QR, LD, m1m2, g=G0): return eta_o * QR / g * LD * math.log(m1m2)

# ---------------------------------------------------------------- item constructors
def B(vi, en): return dict(vi=vi, en=en)
def opt(txt): return dict(vi=txt, en=txt)
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
    """option list (identical text in both languages) with the correct value first; wrongs: list of floats (distinct from correct)."""
    vals = [correct]; seen = {N(correct, nd)}
    for w in wrongs:
        if N(w, nd) not in seen: vals.append(w); seen.add(N(w, nd))
    u = (' ' + unit) if unit else ''
    return [opt(N(v, nd) + u) for v in vals]

def dump(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)
