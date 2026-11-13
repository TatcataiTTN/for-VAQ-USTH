"""P3: trich bang Appendix 1 tu 08_*.md thanh data/props/*.json.
Chay: python3 -I build/props/extract_tables.py
Giu dung so nhu in; 'prec' = so chu so thap phan in cua tung o (dung lam dung sai = nua don vi chu so cuoi)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagetext import pages, lines, tonum, norm

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(P, 'data', 'props')
os.makedirs(OUT, exist_ok=True)
D = pages()
_i = D[41].find('TABLE A–25')
D['41a'], D['41b'] = D[41][:_i], D[41][_i:]
CLEANED = []   # cac o phai go ky tu rac OCR

def tok_num(t, ctx=''):
    """token -> (value, dec) ; go tien to chu rac nhu 's237.17' (ghi lai)."""
    r = tonum(t)
    if r is not None:
        return r
    m = re.match(r'^[A-Za-z]+(-?\d[\d,]*\.?\d*)$', norm(t))
    if m:
        CLEANED.append({'ctx': ctx, 'token': t, 'used': m.group(1)})
        return tonum(m.group(1))
    return None

def save(name, obj):
    with open(os.path.join(OUT, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=0)

def meta(table, en, vi, pdf_pages, substance, index, notes=None, **kw):
    o = dict(table=table, title={'en': en, 'vi': vi}, pdf_pages=[int(str(p)[:2]) if len(str(p))>2 else p for p in pdf_pages],
             printed_pages=[int(str(p)[:2] if str(p)[:2].isdigit() and len(str(p))>2 else p) + 908 for p in pdf_pages], substance=substance,
             index=index, notes=notes or [])
    o.update(kw)
    return o

def flat_table(pgs, ncol, ctx, first_numeric=True):
    rows, prec, rp = [], [], []
    for p in pgs:
        for l in lines(D[p]):
            tk = l.split()
            if len(tk) != ncol:
                continue
            nums = [tok_num(t, f'{ctx} p{p}') for t in tk]
            if all(n is not None for n in nums):
                rows.append([n[0] for n in nums]); prec.append([n[1] for n in nums]); rp.append(p)
    return rows, prec, rp

U_SAT = {'T_C': '°C', 'Psat_kPa': 'kPa', 'Tsat_C': '°C', 'vf': 'm3/kg', 'vg': 'm3/kg', 'uf': 'kJ/kg', 'ufg': 'kJ/kg',
         'ug': 'kJ/kg', 'hf': 'kJ/kg', 'hfg': 'kJ/kg', 'hg': 'kJ/kg', 'sf': 'kJ/(kg·K)', 'sfg': 'kJ/(kg·K)', 'sg': 'kJ/(kg·K)'}
REST = ['vf', 'vg', 'uf', 'ufg', 'ug', 'hf', 'hfg', 'hg', 'sf', 'sfg', 'sg']

def sat_tables():
    spec = [('A-4', [8, 9], ['T_C', 'Psat_kPa'], 'water', 'T_C', 'Saturated water: temperature table', 'Nước bão hòa: bảng theo nhiệt độ', 'A4'),
            ('A-5', [10, 11], ['Psat_kPa', 'Tsat_C'], 'water', 'Psat_kPa', 'Saturated water: pressure table', 'Nước bão hòa: bảng theo áp suất', 'A5'),
            ('A-11', [20, 21], ['T_C', 'Psat_kPa'], 'R134a', 'T_C', 'Saturated refrigerant-134a: temperature table', 'R-134a bão hòa: bảng theo nhiệt độ', 'A11'),
            ('A-12', [22], ['Psat_kPa', 'Tsat_C'], 'R134a', 'Psat_kPa', 'Saturated refrigerant-134a: pressure table', 'R-134a bão hòa: bảng theo áp suất', 'A12')]
    for tb, pgs, head, sub, idx, en, vi, fn in spec:
        rows, prec, rp = flat_table(pgs, 13, tb)
        cols = head + REST
        notes = ['Mỗi hàng: 13 cột như in. Quy chiếu: nước u_f=s_f=0 tại điểm ba (0,01 °C); R-134a h_f=s_f=0 tại -40 °C.']
        if tb == 'A-4':
            notes.append('Hàng cuối T=373,95 °C là điểm tới hạn (u_fg = h_fg = s_fg = 0, v_f = v_g).')
        save(fn, meta(tb, en, vi, pgs, sub, idx, notes, units={c: U_SAT[c] for c in cols}, columns=cols,
                      rows=rows, prec=prec, row_pages=rp))

def blocks_table(pgs, tb, fn, en, vi, sub, cols, units, nvals, notes, pkey='P_MPa', tkey='Tsat_C', rightfill=False):
    HDR = re.compile(r'P\s*=[^0-9]*([\d.]+)\s*MPa(?:\s*\(\s*(?:T\.?sat\s*=\s*)?([-−—–]?\s*[\d.]+)\s*°?\s*C)?')
    blocks = {}
    order = []
    ng = 0; groups = []
    for p in pgs:
        for l in lines(D[p]):
            if 'MPa' in l and '=' in l and 'P' in l:
                h = HDR.findall(l); assert h, l
                groups = []
                for pv, ts in h:
                    key = (p, pv)
                    tsv = float(norm(ts).replace(' ', '')) if ts else None
                    b = {'param': {pkey: float(pv), tkey: tsv}, 'pdf_page': p, 'sat': None, 'rows': [], 'prec': [], 'sat_prec': None}
                    order.append(b); groups.append(b)
                continue
            tk = l.split()
            if not tk or not groups:
                continue
            first = tk[0]
            issat = first.lower().startswith('sat')
            if not (issat or tonum(first)):
                continue
            nums = [tok_num(t, f'{tb} p{p}') for t in tk[1:]]
            if not nums or not all(n is not None for n in nums) or len(nums) % nvals or len(nums) > nvals * len(groups):
                continue
            T = None if issat else tonum(first)
            k = len(nums) // nvals
            off = (len(groups) - k) if (rightfill and not issat) else 0
            for gi in range(k):
                seg = nums[gi * nvals:(gi + 1) * nvals]
                tgt = groups[gi + off]
                vals = [s[0] for s in seg]; pr = [s[1] for s in seg]
                if issat:
                    tgt['sat'] = vals; tgt['sat_prec'] = pr
                else:
                    tgt['rows'].append([T[0]] + vals); tgt['prec'].append([T[1]] + pr)
    for b in order:
        b['n_rows'] = len(b['rows'])
    return meta(tb, en, vi, pgs, sub, 'P_MPa, T_C', notes, units=units, columns=cols, blocks=order,
                sat_columns=cols[1:])

def superheated():
    cols = ['T_C', 'v', 'u', 'h', 's']
    u = {'T_C': '°C', 'v': 'm3/kg', 'u': 'kJ/kg', 'h': 'kJ/kg', 's': 'kJ/(kg·K)', 'P_MPa': 'MPa', 'Tsat_C': '°C'}
    n6 = ['Khối theo áp suất P (MPa); mỗi hàng T, v, u, h, s. Hàng "Sat." in ở đầu mỗi khối được lưu ở khóa sat (v, u, h, s) với T = Tsat.',
          'Ô trống của sách (T dưới Tsat của khối) không có hàng: bảng chỉ liệt kê T ≥ Tsat (gán nhóm trái-sang-phải được kiểm T ≥ Tsat).']
    save('A6', blocks_table([12, 13, 14, 15], 'A-6', 'A6', 'Superheated water', 'Hơi nước quá nhiệt', 'water', cols, u, 4,
                            n6 + ['Các khối P ≥ 25 MPa là vùng siêu tới hạn (không có Tsat in).']))
    n7 = ['Nước nén (lỏng nén): các khối P = 5…50 MPa, T 0…380 °C. Hàng "Sat." ghi giá trị lỏng bão hòa ở P (chỉ in cho P ≤ 20 MPa).',
          'Chỉ in các hàng T ≤ Tsat của mỗi P (ô trống của sách không có hàng).']
    save('A7', blocks_table([16], 'A-7', 'A7', 'Compressed liquid water', 'Nước lỏng nén', 'water', cols, u, 4, n7 + ['Nhóm ô: trong A-7 các ô trống nằm ở nhóm P thấp khi T cao (T ≤ Tsat), nên hàng ít nhóm thuộc các nhóm P cao bên phải.'], rightfill=True))
    n13 = ['Khối theo P (MPa) với Tsat (°C, có thể âm). Tsat in: "−36,95" ở P=0,06 MPa v.v.; mỗi hàng T, v, u, h, s.',
           'Quy chiếu ASHRAE: h = s = 0 của lỏng bão hòa tại −40 °C.']
    save('A13', blocks_table([23, 24], 'A-13', 'A13', 'Superheated refrigerant-134a', 'R-134a quá nhiệt', 'R134a', cols, u, 4, n13))

def A2():
    rows = []; pr = []
    for l in lines(D[3]):
        tk = l.split()
        if len(tk) >= 6:
            nums = [tonum(t) for t in tk[-4:]]
            if all(nums):
                # tên = các token trước formula; formula = token trước 4 số
                rows.append([' '.join(tk[:-5]), tk[-5]] + [n[0] for n in nums]); pr.append([None, None] + [n[1] for n in nums])
    save('A2a', meta('A-2a', 'Ideal-gas specific heats of common gases at 300 K', 'Nhiệt dung riêng khí lý tưởng ở 300 K', [3], 'gases', 'name',
                     ['R = Ru/M; cv = cp − R; k = cp/cv.'], units={'R': 'kJ/(kg·K)', 'cp': 'kJ/(kg·K)', 'cv': 'kJ/(kg·K)', 'k': '-'},
                     columns=['gas', 'formula', 'R', 'cp', 'cv', 'k'], rows=rows, prec=pr))
    # A-2b
    rows = []; pr = []; groups = None
    for l in lines(D[4]):
        tk = l.split()
        if tk[0] == 'K' and 'Air' in tk:
            groups = ['Air', 'CO2', 'CO']; continue
        if tk[0].startswith('Hydrogen,'):
            groups = ['H2', 'N2', 'O2']; continue
        if groups and len(tk) == 10:
            nums = [tonum(t) for t in tk]
            if all(nums):
                for gi, g in enumerate(groups):
                    seg = nums[1 + 3 * gi:4 + 3 * gi]
                    rows.append([g, nums[0][0]] + [s[0] for s in seg]); pr.append([None, 0] + [s[1] for s in seg])
    save('A2b', meta('A-2b', 'Ideal-gas specific heats at various temperatures', 'Nhiệt dung riêng khí lý tưởng theo nhiệt độ', [4], 'gases', 'T_K',
                     ['Mỗi hàng: (chất, T, cp, cv, k); 6 chất × 14 nhiệt độ 250–1000 K.'],
                     units={'T_K': 'K', 'cp': 'kJ/(kg·K)', 'cv': 'kJ/(kg·K)', 'k': '-'}, columns=['gas', 'T_K', 'cp', 'cv', 'k'], rows=rows, prec=pr))
    # A-2c
    rows = []; pr = []; pend = ''
    pat = re.compile(r'^(.*?)\s+([A-Za-z0-9—\-]+)\s+(-?[\d.]+)\s+(-?[\d.]+) × 10\^(-?\d+)\s+(-?[\d.]+) × 10\^(-?\d+)\s+(-?[\d.]+) × 10\^(-?\d+)\s+(\d+)[-–](\d+)\s+([\d.]+)\s+([\d.]+)\s*$')
    for l in lines(D[5]):
        l2 = norm(l).replace('−', '-')
        # trường hợp dấu '-' dính liền số ở cột a
        m = pat.match(re.sub(r' {1,}', ' ', l2.replace('−', '-')))
        if not m:
            pend = l.strip() if re.match(r'^[A-Za-z][a-z]+$', l.strip()) else pend
            continue
        name = (pend + ' ' + m.group(1)).strip() if pend and len(m.group(1)) < 12 and m.group(1)[:1].islower() else m.group(1)
        if pend and name != m.group(1):
            pass
        g = m.groups()
        def sci(mant, ex): return float(f'{mant}e{ex}')
        rows.append([name, g[1], float(g[2]), sci(g[3], g[4]), sci(g[5], g[6]), sci(g[7], g[8]), int(g[9]), int(g[10]), float(g[11]), float(g[12])])
        pr.append({'a': g[2], 'b': f'{g[3]}e{g[4]}', 'c': f'{g[5]}e{g[6]}', 'd': f'{g[7]}e{g[8]}'})
        pend = ''
    save('A2c', meta('A-2c', 'Ideal-gas molar specific heat cp(T) = a + bT + cT^2 + dT^3', 'Nhiệt dung mol cp(T) = a + bT + cT² + dT³ của khí lý tưởng', [5], 'gases', 'name',
                     ['T tính bằng K, cp bằng kJ/(kmol·K). b, c, d in dạng mantissa × 10^mũ; ở đây lưu giá trị thật (vd 0,1967×10^-2 = 0,001967); chuỗi in nằm ở khóa printed.',
                      'Khoảng T hợp lệ (T_min–T_max) và sai số lớn nhất/trung bình (%) theo sách.'],
                     units={'a': 'kJ/(kmol·K)', 'b': 'kJ/(kmol·K^2)', 'c': 'kJ/(kmol·K^3)', 'd': 'kJ/(kmol·K^4)', 'Tmin': 'K', 'Tmax': 'K', 'err_max': '%', 'err_avg': '%'},
                     columns=['substance', 'formula', 'a', 'b', 'c', 'd', 'Tmin', 'Tmax', 'err_max', 'err_avg'], rows=rows, printed=pr))

def A1():
    out = {}
    for pg, tb, fn, en, vi in ((2, 'A-1', 'A1', 'Molar mass, gas constant and critical-point properties (SI)', 'Khối lượng mol, hằng số khí, thông số tới hạn (SI)'),):
        rows = []; pr = []
        for l in lines(D[pg]):
            tk = l.split()
            if len(tk) >= 7:
                nums = [tonum(t) for t in tk[-5:]]
                if all(nums):
                    rows.append([' '.join(tk[:-6]), tk[-6]] + [n[0] for n in nums]); pr.append([None, None] + [n[1] for n in nums])
        save(fn, meta(tb, en, vi, [pg], 'gases', 'name', ['R = Ru/M với Ru = 8,31447 kJ/(kmol·K).'],
                      units={'M': 'kg/kmol', 'R': 'kJ/(kg·K)', 'Tcr': 'K', 'Pcr': 'MPa', 'Vcr': 'm3/kmol'},
                      columns=['substance', 'formula', 'M', 'R', 'Tcr', 'Pcr', 'Vcr'], rows=rows, prec=pr))

def twocol(pgs, tb, fn, en, vi, sub, cols, units, note, unitnote=None):
    n = len(cols); rows = {}
    for p in pgs:
        for l in lines(D[p]):
            tk = l.split()
            if len(tk) not in (n, 2 * n):
                continue
            nums = [tok_num(t, f'{tb} p{p}') for t in tk]
            if not all(x is not None for x in nums):
                continue
            for s in range(0, len(tk), n):
                seg = nums[s:s + n]
                rows[seg[0][0]] = ([x[0] for x in seg], [x[1] for x in seg], p)
    ks = sorted(rows)
    return meta(tb, en, vi, pgs, sub, cols[0], note, units=units, columns=cols, rows=[rows[k][0] for k in ks],
                prec=[rows[k][1] for k in ks], row_pages=[int(str(rows[k][2])[:2]) if len(str(rows[k][2]))>2 else rows[k][2] for k in ks])

def gas_tables():
    save('A17', twocol([28, 29], 'A-17', 'A17', 'Ideal-gas properties of air', 'Khí lý tưởng: không khí',
        'air', ['T_K', 'h', 'Pr', 'u', 'vr', 's0'], {'T_K': 'K', 'h': 'kJ/kg', 'Pr': '-', 'u': 'kJ/kg', 'vr': '-', 's0': 'kJ/(kg·K)'},
        ['Thứ tự cột in: T, h, Pr, u, vr, s°. s° là entropi tuyệt đối ở 1 atm; Pr, vr là áp suất/thể tích tương đối (không phải P, v).',
         'Quy chiếu: h = u = 0 ở 0 K (không phải tại điểm ba).']))
    save('A17E', twocol([76, 77], 'A-17E', 'A17E', 'Ideal-gas properties of air (English units)', 'Khí lý tưởng: không khí (đơn vị Anh)',
        'air', ['T_R', 'h', 'Pr', 'u', 'vr', 's0'], {'T_R': 'R', 'h': 'Btu/lbm', 'Pr': '-', 'u': 'Btu/lbm', 'vr': '-', 's0': 'Btu/(lbm·R)'},
        ['Đơn vị Anh: T tính bằng rankine (R), h, u bằng Btu/lbm, s° bằng Btu/(lbm·R).',
         'Tutorials I bài 2, 4, 7 dùng bảng này.']))
    sp = [('A-18', [30, 31], 'N2', 'nitrogen', 'Nitơ'), ('A-19', [32, 33], 'O2', 'oxygen', 'Ôxy'), ('A-20', [34, 35], 'CO2', 'carbon dioxide', 'Cacbon đioxit'),
          ('A-21', [36, 37], 'CO', 'carbon monoxide', 'Cacbon monoxit'), ('A-22', [38], 'H2', 'hydrogen', 'Hiđro'),
          ('A-23', [39, 40], 'H2O', 'water vapor', 'Hơi nước'), ('A-24', ['41a'], 'O', 'monatomic oxygen', 'Ôxy nguyên tử')]
    for tb, pgs, sub, en, vi in sp:
        o = twocol(pgs, tb, tb.replace('-', ''), f'Ideal-gas properties of {en}, {sub}', f'Khí lý tưởng: {vi} ({sub})', sub,
                   ['T_K', 'h', 'u', 's0'], {'T_K': 'K', 'h': 'kJ/kmol', 'u': 'kJ/kmol', 's0': 'kJ/(kmol·K)'},
                   ['Bảng theo kmol: h̄, ū (kJ/kmol) và s̄° (kJ/(kmol·K)) ở 1 atm; h̄ là entanpi tuyệt đối với h̄_f° tại 25 °C đã gồm trong bảng theo quy ước Cengel (h̄ = h̄_f° + Δh̄ ở 298 K).'])
        o['notes'][0] = 'Bảng theo kmol: h̄, ū (kJ/kmol) và s̄° (kJ/(kmol·K)) ở 1 atm. h̄ trong bảng là Δh̄ so với 0 K (h̄ = 0 ở 0 K), không gồm h̄_f°.'
        if sub != 'O':
            pass
        save(tb.replace('-', ''), o)
    # OH: cung trang 41 voi A-24 -> tach theo tieu de
    o = twocol(['41b'], 'A-25', 'A25', 'Ideal-gas properties of hydroxyl, OH', 'Khí lý tưởng: hiđrôxyl (OH)', 'OH', ['T_K', 'h', 'u', 's0'],
               {'T_K': 'K', 'h': 'kJ/kmol', 'u': 'kJ/kmol', 's0': 'kJ/(kmol·K)'}, ['Bảng theo kmol; Δh̄ so với 0 K.'])
    o['row_pages'] = [41] * len(o['rows'])
    save('A25', o)

def A26_27_32():
    rows = []; pr = []
    for l in lines(D[42]):
        tk = l.split()
        if len(tk) >= 5:
            nums = [tonum(t.lstrip('+')) for t in tk[-3:]]
            if all(nums) and re.search(r'\((s|g|ᐉ|l)\)', tk[-4]):
                rows.append([' '.join(tk[:-4]), tk[-4]] + [n[0] for n in nums]); pr.append([None, None] + [n[1] for n in nums])
    save('A26', meta('A-26', 'Enthalpy of formation, Gibbs function of formation, absolute entropy at 25 °C, 1 atm', 'Entanpi hình thành, hàm Gibbs hình thành và entropi tuyệt đối ở 25 °C, 1 atm',
                     [42], 'various', 'formula', ['Dấu − và + của h_f°, g_f° đã kiểm với ảnh trang (17 hàng âm khớp).'],
                     units={'hf0': 'kJ/kmol', 'gf0': 'kJ/kmol', 's0': 'kJ/(kmol·K)'}, columns=['substance', 'formula', 'hf0', 'gf0', 's0'], rows=rows, prec=pr))
    rows = []; pr = []
    for l in lines(D[43]):
        tk = l.split()
        if len(tk) >= 8 and re.search(r'\((s|g|ᐉ)\)', tk[len(tk) - 8 + 0] if False else ' '.join(tk[:-6])):
            vals = tk[-6:]
            conv = []; p_ = []
            for v in vals:
                n = tonum(v)
                if n: conv.append(n[0]); p_.append(n[1])
                elif v in ('—', '-', '–'): conv.append(None); p_.append(None)
                else: conv.append(v); p_.append(None)   # khoang gia tri in nhu 100–110
            rows.append([' '.join(tk[:-7]), tk[-7]] + conv); pr.append([None, None] + p_)
    save('A27', meta('A-27', 'Properties of some common fuels and hydrocarbons', 'Tính chất một số nhiên liệu và hiđrôcacbon thông dụng', [43], 'fuels', 'name',
                     ['null = "—" (không có số liệu); chuỗi = khoảng giá trị in (vd "100–110"). HHV, LHV ở 25 °C; nhân với M để ra kJ/kmol.',
                      'Khối lượng riêng ở 1 atm, 20 °C; h_fg ở 25 °C với nhiên liệu lỏng.'],
                     units={'M': 'kg/kmol', 'rho': 'kg/L', 'hfg': 'kJ/kg', 'cp': 'kJ/(kg·K)', 'HHV': 'kJ/kg', 'LHV': 'kJ/kg'},
                     columns=['fuel', 'formula', 'M', 'rho', 'hfg', 'cp', 'HHV', 'LHV'], rows=rows, prec=pr))
    rows = []; pr = []
    for l in lines(D[48]):
        tk = l.split()[-6:]
        if len(tk) == 6:
            nums = []
            for t in tk:
                n = tonum(t)
                if n: nums.append(n)
                elif t in ('∞', '\x19'): nums.append((None, 0))
                else: nums = None; break
            if nums and not (rows and rows[-1][0] is None):
                rows.append([x[0] for x in nums]); pr.append([x[1] for x in nums])
    save('A32', meta('A-32', 'One-dimensional isentropic compressible-flow functions, ideal gas, k = 1.4', 'Hàm dòng nén được đẳng entropi một chiều, khí lý tưởng k = 1,4', [48], 'ideal gas k=1.4', 'Ma',
                     ['null = ∞ (A/A* tại Ma = 0 và ∞). Công thức: T/T0 = (1+0,2Ma²)^-1; P/P0 = (T/T0)^3,5; ρ/ρ0 = (T/T0)^2,5; A/A* = (1/Ma)[(2/2,4)(1+0,2Ma²)]^3.'],
                     units={'Ma': '-', 'Ma_star': '-', 'A_Astar': '-', 'P_P0': '-', 'rho_rho0': '-', 'T_T0': '-'},
                     columns=['Ma', 'Ma_star', 'A_Astar', 'P_P0', 'rho_rho0', 'T_T0'], rows=rows, prec=pr))

if __name__ == '__main__':
    sat_tables(); superheated(); A2(); A1(); gas_tables(); A26_27_32()
    # A-6/7/13 phai chay bang ham rieng (khong qua 'save' trong ham)
    json.dump(CLEANED, open(os.path.join(OUT, '_cleaned_tokens.json'), 'w'), ensure_ascii=False, indent=1)
    for f in sorted(os.listdir(OUT)):
        if f.endswith('.json') and not f.startswith('_'):
            o = json.load(open(os.path.join(OUT, f)))
            n = len(o['rows']) if 'rows' in o else sum(len(b['rows']) for b in o['blocks'])
            print(f, n, 'blocks=%d' % len(o['blocks']) if 'blocks' in o else '')
