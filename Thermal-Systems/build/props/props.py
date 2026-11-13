"""Thu vien tra bang thuoc tinh (Appendix 1, Cengel) - cung thuat toan voi _shared/props.js.

Moi lan tra tra ve dict:
  value, unit, table, pdf_page, printed_page, rows_used, method ('exact'|'linear'|'bilinear'|'polynomial'|'formula'),
  suspect (bool), note.
Noi suy TUYEN TINH theo bien in cua bang (T, P, Ma, ...). Khong ngoai suy: ngoai pham vi -> PropsRangeError.
Hoi qua nhiet / nuoc nen: noi suy hai chieu (T trong tung khoi P, sau do tuyen tinh theo P).
Vung am: y = y_f + x (y_g - y_f)."""
import json, math, os, re

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'props'))
EPS = 1e-9


def _n(x):
    """dinh dang so giong _shared/props.js (toPrecision(12))"""
    return '%.12g' % x if isinstance(x, (int, float)) and not isinstance(x, bool) else str(x)


LANG = 'vi'


def set_lang(l):
    global LANG
    LANG = 'en' if l == 'en' else 'vi'


def _m(_k, **kw):
    t = _load('messages')[_k][LANG]
    return re.sub(r'\{(\w+)\}', lambda m: _n(kw[m.group(1)]), t)


class PropsRangeError(ValueError):
    pass


_cache = {}


def _load(name):
    if name not in _cache:
        with open(os.path.join(DATA, name + '.json'), encoding='utf-8') as f:
            _cache[name] = json.load(f)
    return _cache[name]


def _errata():
    if '_errata' not in _cache:
        _cache['_errata'] = _load('book_errata')['errors']
    return _cache['_errata']


def _suspect(table, keyval, col):
    """-> (suspect, note) cho o (table, gia tri khoa hang, cot)."""
    for e in _errata():
        if e['table'] == table and e['col'] == col:
            kv = list(e['key'].values())[0]
            if isinstance(kv, (int, float)) and isinstance(keyval, (int, float)) and abs(kv - keyval) < EPS:
                return True, e
    return False, None


def _note_of(es):
    out = []
    for e in es:
        tag = _m('err_tag') if e.get('kind') != 'systematic_offset' else _m('err_sys_tag')
        how = e['how_en'] if (LANG == 'en' and e.get('how_en')) else e['how']
        out.append(_m('err_fmt', tag=tag, col=e['col'], key=list(e['key'].values())[0], printed=e['printed'], expected=e['expected'], how=how))
    return ' | '.join(out)


def _res(value, table, pages, rows_used, method, unit, es=(), note=''):
    pages = sorted(set(pages))
    n = _note_of(es)
    nt = ' | '.join(x for x in (note, n) if x)
    return dict(value=value, unit=unit, table=table, pdf_page=pages[0], printed_page=pages[0] + 908,
                pdf_pages=pages, rows_used=rows_used, method=method, suspect=bool(es), note=nt)


def _bracket(xs, x, what):
    """xs tang ngat; -> (i, j, f); i==j neu trung nut."""
    lo, hi = xs[0], xs[-1]
    if x < lo - EPS or x > hi + EPS:
        raise PropsRangeError(_m('range_out', what=what, x=x, lo=lo, hi=hi))
    for i, v in enumerate(xs):
        if abs(v - x) < EPS:
            return i, i, 0.0
    for i in range(len(xs) - 1):
        if xs[i] < x < xs[i + 1]:
            return i, i + 1, (x - xs[i]) / (xs[i + 1] - xs[i])
    raise PropsRangeError(_m('no_interval', what=what, x=x))


def _bracket_dec(xs, x, what):
    """xs giam ngat (vr)"""
    neg = [-v for v in xs]
    return _bracket(neg, -x, what)


def _unit(t, col):
    return t['units'].get(col, '')


def _flat_rows(t):
    return t['rows']


def _cell(t, i, col):
    return t['rows'][i][t['columns'].index(col)]


def _row_ref(t, i, cols):
    r = t['rows'][i]
    key = t['columns'][0] if t['index'] not in t['columns'] else t['index']
    kc = t['columns'].index(t['index']) if t['index'] in t['columns'] else 0
    return dict(key={t['columns'][kc]: r[kc]}, pdf_page=t['row_pages'][i] if 'row_pages' in t else t['pdf_pages'][0],
                cells={c: r[t['columns'].index(c)] for c in cols})


def lookup_flat(tname, fname, idxcol, x, prop, note=''):
    """Noi suy tuyen tinh mot cot theo cot chi so (bang phang)."""
    t = _load(fname)
    cols = t['columns']
    ic = cols.index(idxcol); pc = cols.index(prop)
    xs = [r[ic] for r in t['rows'] if r[ic] is not None]
    rows = [r for r in t['rows'] if r[ic] is not None]
    i, j, f = _bracket(xs, x, f'{idxcol}')
    used = []; es = []
    pgs = []
    for k in sorted({i, j}):
        pg = t['row_pages'][k] if 'row_pages' in t else t['pdf_pages'][0]
        pgs.append(pg)
        used.append(dict(key={idxcol: rows[k][ic]}, pdf_page=pg, cells={prop: rows[k][pc]}))
        s, e = _suspect(t['table'], rows[k][ic], prop)
        if s: es.append(e)
    if i == j:
        v = rows[i][pc]; m = 'exact'
    else:
        v = rows[i][pc] + f * (rows[j][pc] - rows[i][pc]); m = 'linear'
    return _res(v, t['table'], pgs, used, m, _unit(t, prop), es, note)


# ---------------- bao hoa ----------------
SAT_T = {'water': 'A4', 'R134a': 'A11'}
SAT_P = {'water': 'A5', 'R134a': 'A12'}


def sat_T(sub, T_C, prop):
    f = SAT_T[sub]; t = _load(f)
    return lookup_flat(t['table'], f, 'T_C', T_C, prop)


def sat_P(sub, P_kPa, prop):
    f = SAT_P[sub]; t = _load(f)
    return lookup_flat(t['table'], f, 'Psat_kPa', P_kPa, prop)


def _wet(sub, by, val, x, prop):
    if not (0 <= x <= 1):
        raise PropsRangeError(_m('q_range'))
    fn = sat_T if by == 'T' else sat_P
    a = fn(sub, val, prop + 'f' if prop != 'v' else 'vf')
    b = fn(sub, val, prop + 'g' if prop != 'v' else 'vg')
    v = a['value'] + x * (b['value'] - a['value'])
    used = a['rows_used'] + b['rows_used']
    es = a['suspect'] or b['suspect']
    meth = 'exact' if a['method'] == 'exact' else 'linear'
    r = dict(a)
    r.update(value=v, rows_used=used, method=meth, suspect=es,
             note=_m('wet_note', prop=prop, x=x) + (a['note'] or '') + (b['note'] if b['note'] != a['note'] else ''))
    r['pdf_pages'] = sorted(set(a['pdf_pages'] + b['pdf_pages']))
    r['pdf_page'] = r['pdf_pages'][0]; r['printed_page'] = r['pdf_page'] + 908
    return r


def wet_T(sub, T_C, x, prop):
    return _wet(sub, 'T', T_C, x, prop)


def wet_P(sub, P_kPa, x, prop):
    return _wet(sub, 'P', P_kPa, x, prop)


def quality(sub, by, val, prop, y):
    """x = (y - y_f)/(y_g - y_f) o diem bao hoa (by = 'T' hoac 'P')"""
    fn = sat_T if by == 'T' else sat_P
    a = fn(sub, val, prop + 'f' if prop != 'v' else 'vf'); b = fn(sub, val, prop + 'g' if prop != 'v' else 'vg')
    x = (y - a['value']) / (b['value'] - a['value'])
    r = dict(a); r.update(value=x, unit='-', rows_used=a['rows_used'] + b['rows_used'], suspect=a['suspect'] or b['suspect'],
                          note=_m('q_note') + ('' if 0 <= x <= 1 else _m('q_warn', x=f'{x:.4f}')))
    return r


# ---------------- khoi theo P (A-6, A-13, A-7) ----------------
BLK = {'water': 'A6', 'R134a': 'A13', 'compressed': 'A7'}


def _block_points(b):
    """cac diem (T, v,u,h,s) cua khoi theo T tang, gom hang 'Sat.' neu co."""
    pts = [list(r) for r in b['rows']]
    if b['sat'] is not None and b['param'].get('Tsat_C') is not None:
        pts = [[b['param']['Tsat_C']] + b['sat']] + pts
    return pts, (1 if (b['sat'] is not None and b['param'].get('Tsat_C') is not None) else 0)


def _block_interp(t, b, T, prop, pc):
    pts, sat0 = _block_points(b)
    xs = [p[0] for p in pts]
    try:
        i, j, f = _bracket(xs, T, 'T')
    except PropsRangeError:
        raise PropsRangeError(_m('blk_T_out', T=T, P=b['param']['P_MPa'], lo=xs[0], hi=xs[-1]))
    es = []; used = []
    for k in sorted({i, j}):
        is_sat = (sat0 == 1 and k == 0)
        used.append(dict(key={'P_MPa': b['param']['P_MPa'], 'T_C': xs[k]}, pdf_page=b['pdf_page'], sat_row=is_sat, cells={prop: pts[k][pc]}))
        s, e = _suspect(t['table'], xs[k], prop)
        # khoi: khoa la T; chi tinh neu cung P
        if s and abs(e.get('P_MPa', b['param']['P_MPa']) - b['param']['P_MPa']) < EPS:
            es.append(e)
    v = pts[i][pc] if i == j else pts[i][pc] + f * (pts[j][pc] - pts[i][pc])
    return v, used, es, i == j


def block_lookup(kind, P_MPa, T_C, prop):
    """kind in 'water','R134a','compressed'. Noi suy hai chieu: T trong hai khoi P ke nhau roi tuyen tinh theo P."""
    t = _load(BLK[kind]); pc = t['columns'].index(prop)
    if prop == 'T_C':
        raise PropsRangeError(_m('T_input'))
    Ps = [b['param']['P_MPa'] for b in t['blocks']]
    i, j, f = _bracket(Ps, P_MPa, 'P (MPa)')
    vi, ui, ei, exi = _block_interp(t, t['blocks'][i], T_C, prop, pc)
    pgs = [t['blocks'][i]['pdf_page']]
    if i == j:
        return _res(vi, t['table'], pgs, ui, 'exact' if exi else 'linear', _unit(t, prop), ei,
                    '' if exi else _m('blk_lin', P=Ps[i]))
    try:
        vj, uj, ej, exj = _block_interp(t, t['blocks'][j], T_C, prop, pc)
    except PropsRangeError as ex:
        raise PropsRangeError(_m('blk_between', P=P_MPa, P1=Ps[i], P2=Ps[j], T=T_C, why=str(ex)))
    v = vi + f * (vj - vi)
    pgs.append(t['blocks'][j]['pdf_page'])
    return _res(v, t['table'], pgs, ui + uj, 'bilinear', _unit(t, prop), ei + ej,
                _m('blk_bi', P1=Ps[i], P2=Ps[j], f=f'{f:.4f}') + (' | ' + _m('blk_v_warn') if prop == 'v' else ''))


def superheated(sub, P_MPa, T_C, prop):
    return block_lookup(sub, P_MPa, T_C, prop)


def compressed(P_MPa, T_C, prop):
    return block_lookup('compressed', P_MPa, T_C, prop)


def compressed_approx(T_C, prop):
    """Xap xi lieu nuoc long nen = long bao hoa o cung T (y ~ y_f@T)"""
    col = {'v': 'vf', 'u': 'uf', 'h': 'hf', 's': 'sf'}[prop]
    r = sat_T('water', T_C, col)
    r['note'] = _m('comp_approx') + (' | ' + r['note'] if r['note'] else '')
    return r


def _block_inv(t, b, prop, value):
    pc = t['columns'].index(prop)
    pts, sat0 = _block_points(b)
    ys = [p[pc] for p in pts]
    try:
        i, j, f = _bracket(ys, value, prop)
    except PropsRangeError:
        raise PropsRangeError(_m('inv_out_block', prop=prop, value=value, P=b['param']['P_MPa'], lo=ys[0], hi=ys[-1]))
    cols = t['columns']
    out = {c: (pts[i][k] if i == j else pts[i][k] + f * (pts[j][k] - pts[i][k])) for k, c in enumerate(cols)}
    used = []; es = []
    for k in sorted({i, j}):
        used.append(dict(key={'P_MPa': b['param']['P_MPa'], 'T_C': pts[k][0]}, pdf_page=b['pdf_page'], sat_row=(sat0 == 1 and k == 0), cells={prop: pts[k][pc]}))
        s_, e = _suspect(t['table'], pts[k][0], prop)
        if s_ and abs(e.get('P_MPa', b['param']['P_MPa']) - b['param']['P_MPa']) < EPS:
            es.append(e)
    return out, used, es, i == j


def block_inverse(kind, P_MPa, prop, value):
    """T (va cac cot khac, trong 'extra') khi biet P va mot trong v,u,h,s: noi suy tuyen tinh theo cot do trong khoi, roi theo P."""
    t = _load(BLK[kind])
    Ps = [b['param']['P_MPa'] for b in t['blocks']]
    i, j, f = _bracket(Ps, P_MPa, 'P (MPa)')
    a, ua, ea, exa = _block_inv(t, t['blocks'][i], prop, value)
    pgs = [t['blocks'][i]['pdf_page']]
    if i == j:
        r = _res(a['T_C'], t['table'], pgs, ua, 'exact' if exa else 'linear', '°C', ea, _m('inv_note_block', prop=prop, value=value, P=Ps[i]))
        r['extra'] = a
        return r
    b2, ub, eb, exb = _block_inv(t, t['blocks'][j], prop, value)
    pgs.append(t['blocks'][j]['pdf_page'])
    out = {c: a[c] + f * (b2[c] - a[c]) for c in a}
    r = _res(out['T_C'], t['table'], pgs, ua + ub, 'bilinear', '°C', ea + eb,
             _m('inv_note_bi', prop=prop, value=value, P1=Ps[i], P2=Ps[j], f=f'{f:.4f}'))
    r['extra'] = out
    return r


def superheated_inverse(sub, P_MPa, prop, value):
    return block_inverse(sub, P_MPa, prop, value)


# ---------------- khong khi, khi theo kmol ----------------
def air(T, prop, system='SI'):
    f, ic = ('A17', 'T_K') if system == 'SI' else ('A17E', 'T_R')
    t = _load(f)
    return lookup_flat(t['table'], f, ic, T, prop)


def air_inverse(prop, value, system='SI'):
    """T khi biet h, Pr, u, vr hoac s0 (noi suy tuyen tinh T theo cot do). Tra them 'extra' = cac cot khac tai T."""
    f, ic = ('A17', 'T_K') if system == 'SI' else ('A17E', 'T_R')
    t = _load(f); cols = t['columns']; pc = cols.index(prop)
    ys = [r[pc] for r in t['rows']]
    dec = ys[0] > ys[-1]
    i, j, fr = (_bracket_dec if dec else _bracket)(ys, value, prop)
    rows = t['rows']
    T = rows[i][0] if i == j else rows[i][0] + fr * (rows[j][0] - rows[i][0])
    used = []; es = []; pgs = []
    for k in sorted({i, j}):
        used.append(_row_ref(t, k, [prop])); pgs.append(t['row_pages'][k])
        s, e = _suspect(t['table'], rows[k][0], prop)
        if s: es.append(e)
    extra = {}
    for c in cols[1:]:
        ci = cols.index(c)
        extra[c] = rows[i][ci] if i == j else rows[i][ci] + fr * (rows[j][ci] - rows[i][ci])
    r = _res(T, t['table'], pgs, used, 'exact' if i == j else 'linear', t['units'][ic], es,
             _m('inv_note', prop=prop, value=value))
    r['extra'] = extra
    return r


GAS = {'N2': 'A18', 'O2': 'A19', 'CO2': 'A20', 'CO': 'A21', 'H2': 'A22', 'H2O': 'A23', 'O': 'A24', 'OH': 'A25'}


def gas_kmol(gas, T_K, prop):
    f = GAS[gas]; t = _load(f)
    return lookup_flat(t['table'], f, 'T_K', T_K, prop)


def gas_kmol_inverse(gas, prop, value):
    f = GAS[gas]; t = _load(f); cols = t['columns']; pc = cols.index(prop)
    rows = [r for r in t['rows'] if r[0] != 0]
    ys = [r[pc] for r in rows]
    i, j, fr = _bracket(ys, value, prop)
    T = rows[i][0] if i == j else rows[i][0] + fr * (rows[j][0] - rows[i][0])
    used = [dict(key={'T_K': rows[k][0]}, pdf_page=t['row_pages'][t['rows'].index(rows[k])], cells={prop: rows[k][pc]}) for k in sorted({i, j})]
    es = []
    for k in sorted({i, j}):
        s, e = _suspect(t['table'], rows[k][0], prop)
        if s: es.append(e)
    return _res(T, t['table'], [u['pdf_page'] for u in used], used, 'exact' if i == j else 'linear', 'K', es, _m('inv_note_k', prop=prop, value=value))


# ---------------- A-1, A-2, A-26, A-27 ----------------
def _byname(fname, namecols, name, prop):
    t = _load(fname); cols = t['columns']; pc = cols.index(prop)
    hit = [r for r in t['rows'] if any(str(r[cols.index(c)]).lower() == name.lower() for c in namecols)]
    if not hit:
        hit = [r for r in t['rows'] if any(name.lower() in str(r[cols.index(c)]).lower() for c in namecols)]
    if len(hit) != 1:
        raise PropsRangeError(_m('no_match', name=name, n=len(hit), table=t['table']))
    r = hit[0]
    pg = t['pdf_pages'][0] if len(t['pdf_pages']) == 1 else t['pdf_pages'][0]
    es = []
    return _res(r[pc], t['table'], [pg], [dict(key={namecols[0]: r[cols.index(namecols[0])]}, pdf_page=pg, cells={prop: r[pc]})], 'exact', _unit(t, prop), es)


def critical(substance, prop):
    """A-1: prop in M, R, Tcr, Pcr, Vcr"""
    return _byname('A1', ['substance', 'formula'], substance, prop)


def cp_300(gas, prop):
    """A-2a: prop in R, cp, cv, k"""
    r = _byname('A2a', ['gas', 'formula'], gas, prop)
    ex = [e for e in _errata() if e['table'] == 'A-2a' and e['col'] == prop and gas.lower() in str(e['key'].get('gas', '')).lower()]
    if ex:
        r['suspect'] = True; r['note'] = _note_of(ex)
    return r


def cp_T(gas, T_K, prop):
    """A-2b (gas in Air, CO2, CO, H2, N2, O2): noi suy tuyen tinh theo T; prop in cp, cv, k."""
    t = _load('A2b'); cols = t['columns']; pc = cols.index(prop)
    rows = [r for r in t['rows'] if r[0] == gas]
    if not rows:
        raise PropsRangeError(_m('no_gas', gas=gas))
    xs = [r[1] for r in rows]
    i, j, f = _bracket(xs, T_K, 'T (K)')
    used = [dict(key={'gas': gas, 'T_K': rows[k][1]}, pdf_page=4, cells={prop: rows[k][pc]}) for k in sorted({i, j})]
    v = rows[i][pc] if i == j else rows[i][pc] + f * (rows[j][pc] - rows[i][pc])
    return _res(v, t['table'], [4], used, 'exact' if i == j else 'linear', _unit(t, prop), [])


def cp_poly(substance, T_K, mass_basis=False):
    """A-2c: cp_mol = a + bT + cT^2 + dT^3 [kJ/(kmol K)] (T trong khoang in); mass_basis: chia M (A-1)."""
    t = _load('A2c')
    hit = [r for r in t['rows'] if r[1].lower() == substance.lower() or r[0].lower() == substance.lower()]
    if len(hit) != 1:
        raise PropsRangeError(_m('no_match', name=substance, n=len(hit), table='A-2c'))
    r = hit[0]
    a, b, c, d, lo, hi = r[2], r[3], r[4], r[5], r[6], r[7]
    if T_K < lo or T_K > hi:
        raise PropsRangeError(_m('poly_out', T=T_K, lo=lo, hi=hi, name=r[0]))
    cp = a + b * T_K + c * T_K ** 2 + d * T_K ** 3
    unit = 'kJ/(kmol·K)'
    note = _m('poly_note', emax=r[8], eavg=r[9])
    if mass_basis:
        M = critical(r[0] if r[0] != 'Air' else 'Air', 'M')['value']
        cp = cp / M; unit = 'kJ/(kg·K)'; note += _m('poly_mass', M=M)
    pg = 5
    return dict(value=cp, unit=unit, table='A-2c', pdf_page=pg, printed_page=pg + 908, pdf_pages=[pg],
                rows_used=[dict(key={'substance': r[0]}, pdf_page=pg, cells=dict(a=a, b=b, c=c, d=d, Tmin=lo, Tmax=hi))],
                method='polynomial', suspect=False, note=note)


def formation(name, prop):
    """A-26: prop in hf0, gf0, s0. name = cong thuc (vd 'CO2(g)') hoac ten + pha"""
    t = _load('A26'); cols = t['columns']; pc = cols.index(prop)
    hit = [r for r in t['rows'] if r[1].lower() == name.lower()]
    if len(hit) != 1:
        raise PropsRangeError(_m('no_match_form', name=name, n=len(hit)))
    r = hit[0]
    return _res(r[pc], 'A-26', [42], [dict(key={'formula': r[1]}, pdf_page=42, cells={prop: r[pc]})], 'exact', _unit(t, prop), [])


def fuel(name, prop):
    """A-27: prop in M, rho, hfg, cp, HHV, LHV; name = ten hoac cong thuc (khop duy nhat)"""
    t = _load('A27'); cols = t['columns']; pc = cols.index(prop)
    hit = [r for r in t['rows'] if r[1].lower() == name.lower()] or [r for r in t['rows'] if name.lower() in r[0].lower()]
    if len(hit) != 1:
        raise PropsRangeError(_m('no_match', name=name, n=len(hit), table='A-27'))
    r = hit[0]
    return _res(r[pc], 'A-27', [43], [dict(key={'fuel': r[0]}, pdf_page=43, cells={prop: r[pc]})], 'exact', _unit(t, prop), [])


# ---------------- A-32 ----------------
def isentropic(Ma, prop):
    t = _load('A32'); cols = t['columns']; pc = cols.index(prop)
    rows = [r for r in t['rows'] if r[0] is not None]
    xs = [r[0] for r in rows]
    i, j, f = _bracket(xs, Ma, 'Ma')
    used = []; es = []
    for k in sorted({i, j}):
        used.append(dict(key={'Ma': rows[k][0]}, pdf_page=48, cells={prop: rows[k][pc]}))
        s, e = _suspect('A-32', rows[k][0], prop)
        if s: es.append(e)
    a = rows[i][pc]; b = rows[j][pc]
    if a is None or b is None:
        raise PropsRangeError(_m('iso_inf'))
    v = a if i == j else a + f * (b - a)
    return _res(v, 'A-32', [48], used, 'exact' if i == j else 'linear', _unit(t, prop), es,
                _m('iso_note'))


def isentropic_inverse(prop, value, branch='sub'):
    """Tim Ma tu A/A*, P/P0, rho/rho0, T/T0 hoac Ma*; branch 'sub' (Ma<=1) hoac 'sup' (Ma>=1) cho A/A*."""
    t = _load('A32'); cols = t['columns']; pc = cols.index(prop)
    rows = [r for r in t['rows'] if r[0] is not None and r[pc] is not None]
    if prop == 'A_Astar':
        rows = [r for r in rows if (r[0] <= 1 if branch == 'sub' else r[0] >= 1) and r[0] > 0]
    ys = [r[pc] for r in rows]
    dec = ys[0] > ys[-1]
    i, j, f = (_bracket_dec if dec else _bracket)(ys, value, prop)
    Ma = rows[i][0] if i == j else rows[i][0] + f * (rows[j][0] - rows[i][0])
    used = [dict(key={'Ma': rows[k][0]}, pdf_page=48, cells={prop: rows[k][pc]}) for k in sorted({i, j})]
    return _res(Ma, 'A-32', [48], used, 'exact' if i == j else 'linear', '-', [], _m('iso_inv_note', prop=prop, value=value) + ((_m('iso_sub') if branch == 'sub' else _m('iso_sup')) if prop == 'A_Astar' else ''))


__all__ = [n for n in dir() if not n.startswith('_')]
