"""Doi chieu bang in voi thu vien: nuoc = iapws IF97 (+CoolProp Water de tim nguyen nhan), R-134a = CoolProp (ASHRAE), khong khi = Air (khi ly tuong).
Dung sai moi o = 1/2 don vi chu so cuoi IN (o bang). Chay: .venv/bin/python -I build/props/crosscheck.py"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CoolProp.CoolProp as CP
from iapws import IAPWS97
CP.set_reference_state('R134a', 'ASHRAE')
P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
D = os.path.join(P, 'data', 'props')
def load(n): return json.load(open(os.path.join(D, n + '.json')))
def hu(d): return 0.5 * 10 ** (-d)

pts = []   # dict(group, table, key, col, printed, lib, tol, dev, ok)
def add(group, table, key, col, printed, lib, dec, tol_extra=0.0, ref='lib'):
    tol = hu(dec) + tol_extra
    pts.append(dict(group=group, table=table, key=key, col=col, printed=printed, lib=lib, tol=tol, dev=lib - printed, ok=abs(lib - printed) <= tol + 1e-12, ref=ref))

def water_sat(T=None, P=None, x=0):
    w = IAPWS97(T=T, x=x) if T is not None else IAPWS97(P=P, x=x)
    return w

def water():
    t = load('A4'); c = t['columns']; ix = {k: i for i, k in enumerate(c)}
    for r, pr in zip(t['rows'], t['prec']):
        T = r[0]; Tk = T + 273.15
        try:
            f = IAPWS97(T=Tk, x=0); g = IAPWS97(T=Tk, x=1)
        except Exception:
            continue
        key = {'T_C': T}
        vals = dict(Psat_kPa=f.P * 1000, vf=f.v, vg=g.v, uf=f.u, ug=g.u, hf=f.h, hg=g.h, sf=f.s, sg=g.s, ufg=g.u - f.u, hfg=g.h - f.h, sfg=g.s - f.s)
        for k, v in vals.items():
            add('water/iapws', 'A-4', key, k, r[ix[k]], v, pr[ix[k]], tol_extra=(hu(pr[ix[k]]) if k.endswith('fg') else 0))
    t = load('A5'); c = t['columns']; ix = {k: i for i, k in enumerate(c)}
    for r, pr in zip(t['rows'], t['prec']):
        Pk = r[0] / 1000
        try:
            f = IAPWS97(P=Pk, x=0); g = IAPWS97(P=Pk, x=1)
        except Exception:
            continue
        key = {'Psat_kPa': r[0]}
        vals = dict(Tsat_C=f.T - 273.15, vf=f.v, vg=g.v, uf=f.u, ug=g.u, hf=f.h, hg=g.h, sf=f.s, sg=g.s, ufg=g.u - f.u, hfg=g.h - f.h, sfg=g.s - f.s)
        for k, v in vals.items():
            add('water/iapws', 'A-5', key, k, r[ix[k]], v, pr[ix[k]], tol_extra=(hu(pr[ix[k]]) if k.endswith('fg') else 0))
    for fn in ('A6', 'A7'):
        t = load(fn)
        for b in t['blocks']:
            Pm = b['param']['P_MPa']
            for r, pr in zip(b['rows'], b['prec']):
                try:
                    w = IAPWS97(P=Pm, T=r[0] + 273.15)
                except Exception:
                    continue
                for k, (n, v) in zip(('v', 'u', 'h', 's'), ((1, w.v), (2, w.u), (3, w.h), (4, w.s))):
                    add('water/iapws', t['table'], {'P_MPa': Pm, 'T_C': r[0]}, k, r[n], v, pr[n])
            if b['sat']:
                try:
                    w = IAPWS97(P=Pm, x=1 if fn == 'A6' else 0)
                except Exception:
                    continue
                for k, (n, v) in zip(('v', 'u', 'h', 's'), ((0, w.v), (1, w.u), (2, w.h), (3, w.s))):
                    add('water/iapws', t['table'], {'P_MPa': Pm, 'sat': True}, k, b['sat'][n], v, b['sat_prec'][n])

def r134a():
    f = 'R134a'
    def pf(prop, **kw):
        return CP.PropsSI(prop, *sum(([k[0], v] for k, v in []), []), f) if False else None
    t = load('A11'); c = t['columns']; ix = {k: i for i, k in enumerate(c)}
    for r, pr in zip(t['rows'], t['prec']):
        T = r[0] + 273.15
        key = {'T_C': r[0]}
        g = lambda p, q: CP.PropsSI(p, 'T', T, 'Q', q, f)
        vals = dict(Psat_kPa=g('P', 0) / 1000, vf=1 / g('D', 0), vg=1 / g('D', 1), uf=g('U', 0) / 1000, ug=g('U', 1) / 1000, hf=g('H', 0) / 1000, hg=g('H', 1) / 1000, sf=g('S', 0) / 1000, sg=g('S', 1) / 1000)
        vals['ufg'] = vals['ug'] - vals['uf']; vals['hfg'] = vals['hg'] - vals['hf']; vals['sfg'] = vals['sg'] - vals['sf']
        for k, v in vals.items():
            add('R134a/CoolProp', 'A-11', key, k, r[ix[k]], v, pr[ix[k]], tol_extra=(hu(pr[ix[k]]) if k.endswith('fg') else 0))
    t = load('A12'); c = t['columns']; ix = {k: i for i, k in enumerate(c)}
    for r, pr in zip(t['rows'], t['prec']):
        Pp = r[0] * 1000; key = {'Psat_kPa': r[0]}
        g = lambda p, q: CP.PropsSI(p, 'P', Pp, 'Q', q, f)
        vals = dict(Tsat_C=g('T', 0) - 273.15, vf=1 / g('D', 0), vg=1 / g('D', 1), uf=g('U', 0) / 1000, ug=g('U', 1) / 1000, hf=g('H', 0) / 1000, hg=g('H', 1) / 1000, sf=g('S', 0) / 1000, sg=g('S', 1) / 1000)
        vals['ufg'] = vals['ug'] - vals['uf']; vals['hfg'] = vals['hg'] - vals['hf']; vals['sfg'] = vals['sg'] - vals['sf']
        for k, v in vals.items():
            add('R134a/CoolProp', 'A-12', key, k, r[ix[k]], v, pr[ix[k]], tol_extra=(hu(pr[ix[k]]) if k.endswith('fg') else 0))
    t = load('A13')
    for b in t['blocks']:
        Pm = b['param']['P_MPa']
        for r, pr in zip(b['rows'], b['prec']):
            Tk = r[0] + 273.15
            h = lambda p: CP.PropsSI(p, 'T', Tk, 'P', Pm * 1e6, f)
            for k, (n, v) in zip(('v', 'u', 'h', 's'), ((1, 1 / h('D')), (2, h('U') / 1000), (3, h('H') / 1000), (4, h('S') / 1000))):
                add('R134a/CoolProp', 'A-13', {'P_MPa': Pm, 'T_C': r[0]}, k, r[n], v, pr[n])
        if b['sat']:
            g = lambda p: CP.PropsSI(p, 'P', Pm * 1e6, 'Q', 1, f)
            for k, (n, v) in zip(('v', 'u', 'h', 's'), ((0, 1 / g('D')), (1, g('U') / 1000), (2, g('H') / 1000), (3, g('S') / 1000))):
                add('R134a/CoolProp', 'A-13', {'P_MPa': Pm, 'sat': True}, k, b['sat'][n], v, b['sat_prec'][n])

def air():
    """Dai luong so sanh: h(T)-h(300 K), u(T)-u(300), s0(T)-s0(300) (SI) va Pr(T)/Pr(300) = exp(Δs0/R). Air o 100 Pa ~ khi ly tuong."""
    R = 8.314462618 / 28.9586
    for fn, T0, conv in (('A17', 300.0, 1.0), ):
        t = load(fn); rows = t['rows']; pr = t['prec']
        r0 = [r for r in rows if r[0] == T0][0]; p0 = pr[[r[0] for r in rows].index(T0)]
        Pc = 100.0   # Pa
        h0 = CP.PropsSI('H', 'T', T0, 'P', Pc, 'Air') / 1000; s0 = CP.PropsSI('S', 'T', T0, 'P', Pc, 'Air') / 1000
        for r, p in zip(rows, pr):
            T = r[0]
            if T == T0: continue
            h = CP.PropsSI('H', 'T', T, 'P', Pc, 'Air') / 1000; s = CP.PropsSI('S', 'T', T, 'P', Pc, 'Air') / 1000
            key = {'T_K': T, 'ref_T_K': T0}
            add('air/CoolProp-idealgas', 'A-17', key, 'dh', r[1] - r0[1], h - h0, 2, tol_extra=0)
            add('air/CoolProp-idealgas', 'A-17', key, 'ds0', r[5] - r0[5], s - s0, 5, tol_extra=hu(5))
            du = (h - R * T) - (h0 - R * T0)
            add('air/CoolProp-idealgas', 'A-17', key, 'du', r[3] - r0[3], du, 2)
            Prc = r0[2] * math.exp((s - s0) / R)
            add('air/CoolProp-idealgas', 'A-17', key, 'Pr', r[2], Prc, p[2], tol_extra=r[2] * 1e-4 * 0)

def run():
    water(); r134a(); air()
    return pts

if __name__ == '__main__':
    run()
    from collections import defaultdict
    S = defaultdict(lambda: [0, 0, 0.0])
    for p in pts:
        s = S[(p['group'], p['table'], p['col'])]
        s[0] += 1; s[1] += (not p['ok']); s[2] = max(s[2], abs(p['dev']))
    tot = len(pts); bad = sum(1 for p in pts if not p['ok'])
    print(tot, 'points', bad, 'out of tol')
    for k, v in sorted(S.items()):
        print(k, v)
