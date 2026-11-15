"""Shared helpers for module m05 (compressible flow): ROUTE A = closed forms of the slides (Ch.5 eqs. 1-17) with constant specific heats, SI units
(P in kPa, R in kJ/(kg K), V in m/s, A in m^2, mdot in kg/s), number formatting, item constructors and a registry of every numeric answer
(data/verify/m05_values.json) that build/verify/verify_m05.py recomputes by DIFFERENT routes (scipy brentq on A/A*, the Hugoniot ODE integrated with scipy,
the energy equation with mass flux maximised numerically, Table A-32 at printed rows, _shared/thermo.js through node).
Run with the project venv when props is needed:  .venv/bin/python -I build/gen/gen_m05.py"""
import json, math, os, sys, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REG = []                                       # registry: dict(model, params, out, value, tol, what)
R_AIR = 0.287                                  # kJ/(kg K), Table A-2a
K_AIR = 1.4
CP_AIR = 1.005                                 # kJ/(kg K), Table A-2a (slides use 1.005)

def reg(model, params, out, value, tol=2e-3, what=''):
    """tol: relative tolerance, or {'abs': x} for an absolute one."""
    REG.append(dict(model=model, params=params, out=out, value=value, tol=tol, what=what)); return value

# ---------------------------------------------------------------- closed forms (slides eqs. 1-17)
def cp_of(k, R): return k * R / (k - 1.0)                                  # kJ/(kg K)
def T0_of(T, V, cp): return T + V * V / (2000.0 * cp)                      # slide eq. (1)/(7): V^2/2 in J/kg -> /1000 to kJ/kg
def P0_of(P, T, T0, k): return P * (T0 / T) ** (k / (k - 1.0))             # slide eq. (2)
def csound(k, R, T): return math.sqrt(k * R * 1000.0 * T)                  # m/s, R in kJ/(kg K) -> J/(kg K)
def TT0(Ma, k): return 1.0 / (1.0 + (k - 1.0) / 2.0 * Ma * Ma)             # eq. (9) inverted
def PP0(Ma, k): return TT0(Ma, k) ** (k / (k - 1.0))                       # eq. (10) inverted
def rr0(Ma, k): return TT0(Ma, k) ** (1.0 / (k - 1.0))                     # eq. (11) inverted
def AAs(Ma, k):                                                            # eq. (17)
    return (1.0 / Ma) * ((2.0 / (k + 1.0)) * (1.0 + (k - 1.0) / 2.0 * Ma * Ma)) ** ((k + 1.0) / (2.0 * (k - 1.0)))
def crit(k): return dict(TT=2.0 / (k + 1.0), PP=(2.0 / (k + 1.0)) ** (k / (k - 1.0)), rr=(2.0 / (k + 1.0)) ** (1.0 / (k - 1.0)))   # eqs. (12)-(14)
def Ma_of_PP(pr, k): return math.sqrt(2.0 / (k - 1.0) * (pr ** (-(k - 1.0) / k) - 1.0))
def Ma_of_AA(r, k, branch='sub'):
    """Ma from A/A* by bisection of eq. (17) (route A, monotone on each branch)."""
    if r < 1.0 - 1e-12: raise ValueError('A/A* < 1')
    if abs(r - 1.0) < 1e-12: return 1.0
    lo, hi = (1e-9, 1.0) if branch == 'sub' else (1.0, 2.0)
    if branch != 'sub':
        while AAs(hi, k) < r: hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi); f = AAs(mid, k)
        if branch == 'sub':
            if f > r: lo = mid
            else: hi = mid
        else:
            if f < r: lo = mid
            else: hi = mid
    return 0.5 * (lo + hi)
def mdot_choked(A, P0, T0, k, R):
    """eq. (16) in SI: A [m2], P0 [kPa], T0 [K], R [kJ/(kg K)]  ->  kg/s.  P0 in Pa and R in J/(kg K) make the root dimensionally right."""
    return A * (P0 * 1000.0) * math.sqrt(k / (R * 1000.0 * T0)) * (2.0 / (k + 1.0)) ** ((k + 1.0) / (2.0 * (k - 1.0)))
def mdot_Ma(A, Ma, P0, T0, k, R):                                          # eq. (15)
    return A * Ma * (P0 * 1000.0) * math.sqrt(k / (R * 1000.0 * T0)) / (1.0 + (k - 1.0) / 2.0 * Ma * Ma) ** ((k + 1.0) / (2.0 * (k - 1.0)))
def conv_nozzle(Pb, P0, T0, k, R, A):
    """converging nozzle (slides tr.39-55): returns dict(choked, Pe, Ma, Te, V, rho, mdot)."""
    c = crit(k); Pcrit = c['PP'] * P0
    if Pb >= Pcrit:
        Pe = Pb; Ma = Ma_of_PP(Pe / P0, k); ch = False
    else:
        Pe = Pcrit; Ma = 1.0; ch = True
    Te = T0 * TT0(Ma, k); V = Ma * csound(k, R, Te); rho = Pe / (R * Te)
    return dict(choked=ch, Pcrit=Pcrit, Pe=Pe, Ma=Ma, Te=Te, V=V, rho=rho, mdot=rho * A * V)

# ---------------------------------------------------------------- number formatting
def N(x, nd=2):
    """English-style number: thousands comma, decimal point, minus sign U+2212 (assemble.py localises the Vietnamese text)."""
    return f'{x:,.{nd}f}'.replace('-', '−')

# ---------------------------------------------------------------- item constructors (same schema as m01..m04)
TOK = re.compile(r'(?<![\w.,])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+)(?!\w|[.,]\d)')
def loc(s): return s.replace(',', '\0').replace('.', ',').replace('\0', '.')
ANYNUM = re.compile(r'(?<![\w.,])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+,\d+|\d{1,3}(?: \d{3})+(?!\d))(?![\w]|[.,]\d)')
def fixvi(vi, en):
    def rep(m):
        t = m.group(0)
        if t in en: return t
        if ' ' in t:
            e = t.replace(' ', ','); return e if e in en else t
        if re.fullmatch(r'\d+,\d+', t): return t.replace(',', '.')
        return t
    return ANYNUM.sub(rep, vi)
def loc_text(vi, en):
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

TOP = dict(stag=dict(vi='Tính chất hãm', en='Stagnation properties'),
           snd=dict(vi='Tốc độ âm và số Mach', en='Speed of sound and Mach number'),
           comp=dict(vi='Công máy nén / tuabin đẳng entropi', en='Isentropic compressor / turbine work'),
           hug=dict(vi='Hình dạng ống và biến thiên tính chất (Hugoniot)', en='Duct shape and property trends (Hugoniot)'),
           rel=dict(vi='Quan hệ đẳng entropi theo Ma', en='Isentropic relations in Ma'),
           crit=dict(vi='Tính chất tới hạn', en='Critical properties'),
           area=dict(vi='Tỉ số diện tích A/A*', en='Area ratio A/A*'),
           mdot=dict(vi='Lưu lượng khối và dòng nghẹt', en='Mass flow and choked flow'),
           back=dict(vi='Áp suất ngược và vòi hội tụ', en='Back pressure and converging nozzle'),
           cd=dict(vi='Vòi hội tụ–phân kỳ', en='Converging–diverging nozzle'),
           unit=dict(vi='Bẫy đơn vị (kPa/Pa, kJ/kg·K)', en='Unit traps (kPa/Pa, kJ/kg·K)'))

# ---------------------------------------------------------------- helpers shared by gen_m05_orig*.py / gen_m05.py
PRN = []                                       # printed (book/slide) answers next to ours: dict(key, printed, ours, tol, note)
def prn(key, printed, ours, tol, note=''): PRN.append(dict(key=key, printed=printed, ours=ours, tol=tol, note=note))
SLIDE = lambda pg, book: dict(vi=f'Slide Ch.5 tr.{pg} = Cengel {book}', en=f'Slide Ch.5 p.{pg} = Cengel {book}')
SL = lambda pg, what='': dict(vi=f'Slide Ch.5 tr.{pg}' + (f': {what[0]}' if what else ''), en=f'Slide Ch.5 p.{pg}' + (f': {what[1]}' if what else ''))
CEN = lambda num, vi='', en='': dict(vi=f'Cengel Ch.17 Bài {num}{vi}', en=f'Cengel Ch.17 Problem {num}{en}')
CEX = lambda num, vi='', en='': dict(vi=f'Cengel Ch.17 Ví dụ {num}{vi}', en=f'Cengel Ch.17 Example {num}{en}')
GS = lambda vi, en: dict(vi='Bổ sung – sinh theo dạng ' + vi, en='Added – generated from the type: ' + en)

def numq(qv, qe, correct, wrongs, unit, nd, ev, ee, level, topic, src, origin, check, fig=None, fixed=False):
    """closed numeric question: wrongs = [(value, reason_vi, reason_en)]; the explanation ends with the reason of each wrong option (no option letters)."""
    kk = []; seen = {N(correct, nd)}
    for w in wrongs:
        if N(w[0], nd) in seen: continue
        seen.add(N(w[0], nd)); kk.append(w)
    kk = kk[:3]
    opts = numopts(correct, [w[0] for w in kk], unit, nd)
    u_ = (' ' + unit) if unit else ''
    tv = ' '.join(f'{N(v, nd)}{u_} {rv}.' for v, rv, re_ in kk); te = ' '.join(f'{N(v, nd)}{u_} {re_}.' for v, rv, re_ in kk)
    return mcq(B(qv, qe), opts, 0, B(ev + ' ' + tv, ee + ' ' + te), level, topic, src, origin, check, fig, fixed)
def gq(qv, qe, correct, wrongs, unit, nd, ev, ee, level, topic, src, check, sep=0.012, origin='bo_sung'):
    """numq for generated items: wrongs closer than `sep` (relative) to the answer or to each other are dropped; at least 3 options required."""
    keep = []
    for w in wrongs:
        v = w[0]
        if abs(v - correct) < sep * max(abs(correct), 1e-9): continue
        if any(abs(v - k_[0]) < sep * max(abs(k_[0]), 1e-9) for k_ in keep): continue
        keep.append(w)
    assert len(keep) >= 2, (qv[:70], correct, [w[0] for w in wrongs])
    return numq(qv, qe, correct, keep[:3], unit, nd, ev, ee, level, topic, src, origin, check)
def fp(*pairs): return [[a, b] for a, b in pairs]
