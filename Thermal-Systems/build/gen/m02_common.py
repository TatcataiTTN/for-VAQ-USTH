"""Shared helpers for module m02 (gas power cycles): ROUTE A = the closed forms and table look-ups that a student writes by hand, number formatting, item constructors,
and a registry of every numeric answer (data/verify/m02_values.json) that build/verify/verify_m02.py recomputes by a DIFFERENT route (route B).
Run with the project venv:  .venv/bin/python -I build/gen/gen_m02.py   (props needs the venv for A-17 / A-17E)."""
import json, math, os, sys, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'props'))
import props
REG = []                                   # registry: dict(model, params, out, value, tol, what)
R_AIR = 0.287; K_AIR = 1.4; CV_AIR = 0.718; CP_AIR = 1.005       # Table A-2a at 300 K (cp 1.005, cv 0.718, R 0.287, k 1.4)

def reg(model, params, out, value, tol=2e-3, what=''):
    """tol: relative tolerance (use [abs] key in tol dict for absolute)."""
    REG.append(dict(model=model, params=params, out=out, value=value, tol=tol, what=what)); return value

def N(x, nd=2):
    """English-style number: thousands comma, decimal point (assemble.py localises the Vietnamese text); minus sign U+2212."""
    return f'{x:,.{nd}f}'.replace('-', '−')

# ---------------------------------------------------------------- item constructors (same schema as m01)
TOK = re.compile(r'(?<![\w.,])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+)(?!\w|[.,]\d)')
def loc(s): return s.replace(',', '\0').replace('.', ',').replace('\0', '.')
def loc_text(vi, en):
    """English-formatted numbers (1,575.1 / 0.287) of the Vietnamese text that also occur verbatim in the English text become Vietnamese (1.575,1 / 0,287); hand-typed Vietnamese numbers are left alone."""
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
def dump(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)

# ================================================================== constant-k models (cold-air-standard)
def otto(r, T1, P1, k=K_AIR, R=R_AIR, cv=CV_AIR, qin=None, T3=None, T4=None):
    """ideal Otto cycle, constant specific heats. Exactly one of qin [kJ/kg], T3 [K], T4 [K] fixes the heat addition."""
    T2 = T1 * r ** (k - 1); P2 = P1 * r ** k
    if qin is not None: T3 = T2 + qin / cv
    elif T4 is not None: T3 = T4 * r ** (k - 1)
    q_in = cv * (T3 - T2); T4 = T3 / r ** (k - 1); P3 = P2 * T3 / T2; P4 = P1 * T4 / T1
    q_out = cv * (T4 - T1); w = q_in - q_out; v1 = R * T1 / P1
    return dict(T2=T2, T3=T3, T4=T4, P2=P2, P3=P3, P4=P4, qin=q_in, qout=q_out, wnet=w, eta=w / q_in, mep=w / (v1 * (1 - 1 / r)), v1=v1, eta_formula=1 - r ** (1 - k))

def diesel(r, T1, P1, k=K_AIR, R=R_AIR, cp=None, cv=None, rc=None, T3=None, qin=None):
    """ideal Diesel cycle; temperatures use k, heats use cp, cv (they default to R k/(k-1), R/(k-1)); one of rc, T3 [K], qin [kJ/kg]."""
    cp = cp if cp is not None else R * k / (k - 1); cv = cv if cv is not None else R / (k - 1)
    T2 = T1 * r ** (k - 1); P2 = P1 * r ** k
    if T3 is not None: rc = T3 / T2
    elif qin is not None: rc = 1 + qin / (cp * T2)
    T3 = T2 * rc; T4 = T3 * (rc / r) ** (k - 1); P4 = P1 * T4 / T1
    q_in = cp * (T3 - T2); q_out = cv * (T4 - T1); w = q_in - q_out; v1 = R * T1 / P1
    return dict(T2=T2, T3=T3, T4=T4, P2=P2, P3=P2, P4=P4, rc=rc, qin=q_in, qout=q_out, wnet=w, eta=w / q_in, mep=w / (v1 * (1 - 1 / r)), v1=v1,
                eta_formula=1 - r ** (1 - k) * (rc ** k - 1) / (k * (rc - 1)))

def brayton(rp, T1, T3, k=K_AIR, cp=CP_AIR, etac=1.0, etat=1.0, eps=0.0):
    """Brayton cycle with constant cp; isentropic efficiencies etac, etat; regenerator effectiveness eps (0 = none)."""
    x = rp ** ((k - 1) / k)
    T2s = T1 * x; T4s = T3 / x
    wc = cp * (T2s - T1) / etac; wt = etat * cp * (T3 - T4s)
    T2 = T1 + wc / cp; T4 = T3 - wt / cp
    T5 = T2 + eps * (T4 - T2)
    qin = cp * (T3 - T5); w = wt - wc
    return dict(T2=T2, T4=T4, T5=T5, wc=wc, wt=wt, wnet=w, qin=qin, qout=qin - w, bwr=wc / wt, eta=w / qin, eta_formula=1 - 1 / x if (etac == 1 and etat == 1 and eps == 0) else None)

def rp_opt(T3, T1, k=K_AIR): return (T3 / T1) ** (k / (2 * (k - 1)))        # slide tr.40

# ================================================================== variable specific heats: Appendix A-17 (SI) / A-17E (English), linear interpolation as students do
def A(T, prop, E=False): return props.air(T, prop, system='E' if E else 'SI')['value']
def Ainv(prop, val, E=False): return props.air_inverse(prop, val, system='E' if E else 'SI')

def otto_var(r, T1, P1=None, qin=None, T3=None, E=False, R=R_AIR):
    """Table route (A-17 / A-17E): state 2 from v_r, state 3 from u3 = u2 + q_in (or T3), state 4 from v_r. P in any unit; R only for MEP (v1 = R T1/P1, kJ/kg per P unit)."""
    u1, vr1 = A(T1, 'u', E), A(T1, 'vr', E)
    T2 = Ainv('vr', vr1 / r, E)['value']; u2 = A(T2, 'u', E)
    if qin is not None: u3 = u2 + qin; T3 = Ainv('u', u3, E)['value']
    else: u3 = A(T3, 'u', E)
    vr3 = A(T3, 'vr', E); T4 = Ainv('vr', vr3 * r, E)['value']; u4 = A(T4, 'u', E)
    q_in = u3 - u2; q_out = u4 - u1; w = q_in - q_out
    d = dict(T2=T2, T3=T3, T4=T4, u1=u1, u2=u2, u3=u3, u4=u4, vr3=vr3, qin=q_in, qout=q_out, wnet=w, eta=w / q_in)
    if P1 is not None:
        P2 = P1 * T2 / T1 * r; v1 = R * T1 / P1; d.update(P2=P2, P3=P2 * T3 / T2, mep=w / (v1 * (1 - 1 / r)), v1=v1)
    return d

def diesel_var(r, T1, P1=None, rc=None, T3=None, E=False, R=R_AIR):
    """Table route for the Diesel cycle: v_r relation for the isentropes, h for the constant-pressure heat addition, u for the constant-volume rejection."""
    u1, vr1 = A(T1, 'u', E), A(T1, 'vr', E)
    T2 = Ainv('vr', vr1 / r, E)['value']; h2 = A(T2, 'h', E)
    if rc is not None: T3 = rc * T2
    else: rc = T3 / T2
    h3, vr3 = A(T3, 'h', E), A(T3, 'vr', E)
    T4 = Ainv('vr', vr3 * r / rc, E)['value']; u4 = A(T4, 'u', E)
    q_in = h3 - h2; q_out = u4 - u1; w = q_in - q_out
    d = dict(T2=T2, T3=T3, T4=T4, rc=rc, h2=h2, h3=h3, u4=u4, qin=q_in, qout=q_out, wnet=w, eta=w / q_in)
    if P1 is not None:
        v1 = R * T1 / P1; d.update(P2=P1 * T2 / T1 * r, mep=w / (v1 * (1 - 1 / r)), v1=v1)
    return d

def brayton_var(rp, T1, T3, etac=1.0, etat=1.0, eps=0.0, E=False, T2_given=None, qin23=None):
    """Table route for the Brayton cycle: Pr relation (A-17). T2_given: actual compressor-exit temperature (Tutorials #8); qin23: heat added 2-3 instead of T3."""
    h1, Pr1 = A(T1, 'h', E), A(T1, 'Pr', E)
    T2s = Ainv('Pr', rp * Pr1, E)['value']; h2s = A(T2s, 'h', E)
    if qin23 is not None: T3 = Ainv('h', A(T2_given, 'h', E) + qin23, E)['value']
    h3, Pr3 = A(T3, 'h', E), A(T3, 'Pr', E)
    T4s = Ainv('Pr', Pr3 / rp, E)['value']; h4s = A(T4s, 'h', E)
    wc = (h2s - h1) / etac; h2 = h1 + wc if T2_given is None else A(T2_given, 'h', E)
    if T2_given is not None: wc = h2 - h1
    wt = etat * (h3 - h4s); h4 = h3 - wt
    h5 = h2 + eps * (h4 - h2); qin = h3 - h5; w = wt - wc
    return dict(T3=T3, T2s=T2s, T4s=T4s, h1=h1, h2=h2, h3=h3, h4=h4, h5=h5, wc=wc, wt=wt, wnet=w, qin=qin, qout=qin - w, bwr=wc / wt, eta=w / qin,
                T2=Ainv('h', h2, E)['value'], T4=Ainv('h', h4, E)['value'])

def lookup_note(E=False): return 'A-17E' if E else 'A-17'

# ================================================================== multistage, jets and the book problems that need their own model (route A)
def multistage_k(rp, Nst, T1, T3, k=K_AIR, cp=CP_AIR, etac=1.0, etat=1.0, eps=0.0):
    """Nst compressor stages with intercooling back to T1 and Nst turbine stages with reheating back to T3, equal pressure ratio per stage, constant cp; regenerator effectiveness eps."""
    x = (rp ** (1.0 / Nst)) ** ((k - 1) / k)
    wc = Nst * cp * T1 * (x - 1) / etac; Tc = T1 + T1 * (x - 1) / etac            # exit of every compressor stage
    wt = Nst * etat * cp * T3 * (1 - 1 / x); Tt = T3 - etat * T3 * (1 - 1 / x)    # exit of every turbine stage
    T5 = Tc + eps * (Tt - Tc)
    qin = cp * (T3 - T5) + (Nst - 1) * cp * (T3 - Tt); w = wt - wc
    return dict(wc=wc, wt=wt, wnet=w, bwr=wc / wt, qin=qin, eta=w / qin, T2=Tc, T4=Tt, T5=T5)

def multistage_var(rp, Nst, T1, T3, eps=0.0):
    """Ideal (isentropic) multistage cycle with A-17: equal pressure ratio per stage; eps = 1 means h5 = h9 (ideal regenerator)."""
    x = rp ** (1.0 / Nst)
    h1, Pr1 = A(T1, 'h'), A(T1, 'Pr'); T2 = Ainv('Pr', x * Pr1)['value']; h2 = A(T2, 'h')
    h6, Pr6 = A(T3, 'h'), A(T3, 'Pr'); T7 = Ainv('Pr', Pr6 / x)['value']; h7 = A(T7, 'h')
    wc = Nst * (h2 - h1); wt = Nst * (h6 - h7); h5 = h2 + eps * (h7 - h2)
    qin = (h6 - h5) + (Nst - 1) * (h6 - h7); w = wt - wc
    return dict(T2=T2, T7=T7, h2=h2, h7=h7, wc=wc, wt=wt, wnet=w, bwr=wc / wt, qin=qin, eta=w / qin)

def jet_static_var(rp, T1, P1, mdot, mf, HV):
    """Cengel 9-119: stationary turbojet, A-17, turbine work = compressor work, nozzle expands from turbine exit to P1; returns thrust [N]."""
    q = mf * HV / mdot; h1, Pr1 = A(T1, 'h'), A(T1, 'Pr')
    T2 = Ainv('Pr', rp * Pr1)['value']; h2 = A(T2, 'h'); wc = h2 - h1
    h3 = h2 + q; T3 = Ainv('h', h3)['value']; Pr3 = A(T3, 'Pr'); h4 = h3 - wc; T4 = Ainv('h', h4)['value']; Pr4 = A(T4, 'Pr')
    P4 = P1 * rp * Pr4 / Pr3; T5 = Ainv('Pr', Pr4 * P1 / P4)['value']; h5 = A(T5, 'h')
    V = math.sqrt(2000 * (h4 - h5))
    return dict(T2=T2, T3=T3, T4=T4, P4=P4, T5=T5, V=V, F=mdot * V)

def ideal_jet_k(Ta, Pa, V, rp, T4, mdot, cp, k=K_AIR, J=1.0):
    """Ideal turbojet, constant cp (Cengel Ex 9-9 style). cp [energy/mass/K], V [velocity], J converts V^2/(2) to energy/mass: energy/mass = V^2/(2 J)."""
    T2 = Ta + V ** 2 / (2 * cp * J); P2 = Pa * (T2 / Ta) ** (k / (k - 1))
    x = rp ** ((k - 1) / k); T3 = T2 * x; P3 = rp * P2
    T5 = T4 - T3 + T2; P5 = P3 * (T5 / T4) ** (k / (k - 1))
    T6 = T5 * (Pa / P5) ** ((k - 1) / k); V6 = math.sqrt(2 * J * cp * (T5 - T6))
    Wp = mdot * (V6 - V) * V / J; Qin = mdot * cp * (T4 - T3)
    return dict(T2=T2, P2=P2, T3=T3, P3=P3, T5=T5, P5=P5, T6=T6, V6=V6, Wp=Wp, Qin=Qin, etaP=Wp / Qin)

def turbojet_unchoked(Ta, Pa, V, rp, T04, QR, cp=1.005, k=K_AIR):
    """El-Sayed Example 4.2 chain (ideal components, unchoked nozzle, SI: cp kJ/kg K, QR kJ/kg, V m/s); returns the quantities per kg of air."""
    T02 = Ta + V ** 2 / (2000 * cp); P02 = Pa * (T02 / Ta) ** (k / (k - 1))
    T03 = T02 * rp ** ((k - 1) / k); f = cp * (T04 - T03) / (QR - cp * T04)
    T05 = T04 - (T03 - T02) / (1 + f); P05 = rp * P02 * (T05 / T04) ** (k / (k - 1))
    T7 = T05 * (Pa / P05) ** ((k - 1) / k); Vj = math.sqrt(2000 * cp * (T05 - T7))
    spec_thrust = (1 + f) * Vj - V
    wake = 0.5 * (1 + f) * (Vj - V) ** 2     # (1/2) m_j (Vj - V)^2 per kg of air, as in El-Sayed expression (1)
    etap1 = spec_thrust * V / (spec_thrust * V + wake)
    etap2 = 2 * V / (V + Vj)
    etath = (spec_thrust * V + wake) / (f * QR * 1000)
    return dict(T02=T02, P02=P02, T03=T03, f=f, T05=T05, P05=P05, T7=T7, Vj=Vj, spec_thrust=spec_thrust, etap1=etap1, etap2=etap2, etath=etath, etao=etap1 * etath)

def carnot_var(TL, TH, P_before, P_after):
    """Cengel 9-23 (variable cp): isothermal compression at TL from P_before to P_after, isentropic compression to TH (Pr from A-17); returns Pmax, per-kg heats and work."""
    ds = R_AIR * math.log(P_after / P_before)
    Pmax = P_after * A(TH, 'Pr') / A(TL, 'Pr')
    return dict(Pmax=Pmax, ds=ds, qin=TH * ds, qout=TL * ds, wnet=(TH - TL) * ds)
