"""Cong P3: kiem chung bo tra thuoc tinh.  .venv/bin/python -I build/verify/verify_props.py   (ket thuc bang 'FAILS: none')
 a. cau truc  b. doc tay tu anh vs bang trich  c. doi chieu thu vien (-> data/props/crosscheck.json)  d. bai co dap an in  e. Node = Python"""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(P, 'build', 'props'))
import props as L
import pagetext
D = os.path.join(P, 'data', 'props')
FAILS = []
def fail(msg): FAILS.append(msg); print('  FAIL:', msg)
def load(n): return json.load(open(os.path.join(D, n + '.json')))
def hu(d): return 0.5 * 10 ** (-d)

FILES = ['A1', 'A2a', 'A2b', 'A2c', 'A4', 'A5', 'A6', 'A7', 'A11', 'A12', 'A13', 'A17', 'A17E', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A32']

# ---------------------------------------------------------------- a. cau truc
EXPECT_ROWS = {  # so hang: dem tren ANH trang (A-4: 41+35; A-5: 37+36; A-11: 30+26; A-12: 34) hoac theo so lieu muc luc
    'A4': 76, 'A5': 73, 'A11': 56, 'A12': 34, 'A1': 34, 'A2a': 16, 'A2b': 84, 'A2c': 28, 'A26': 29, 'A27': 23, 'A32': 23,
}
EXPECT_PAGE_ROWS = {'A4': {8: 41, 9: 35}, 'A5': {10: 37, 11: 36}, 'A11': {20: 30, 21: 26}, 'A12': {22: 34}}
EXPECT_BLOCKS = {'A6': 36, 'A7': 6, 'A13': 18}
ALLOW_NONE = {'A27': True, 'A32': True}
D_PAGES = pagetext.pages()

def indep_token_count(pages, ncol, mode):
    """dem doc lap (khong qua tonum/clean): tong so token so tren cac dong du lieu / ncol"""
    NUMRE = re.compile(r'^[\u2212-]?(\d{1,3}(,\d{3})+|\d*\.?\d+)$')
    n = 0
    for p in pages:
        txt = D_PAGES[int(str(p)[:2])] if not isinstance(p, str) else D_PAGES[41]
        if p == '41a': txt = txt[:txt.find('TABLE A–25')]
        if p == '41b': txt = txt[txt.find('TABLE A–25'):]
        for l in txt.split('\n'):
            tk = l.split()
            if not tk: continue
            nums = [bool(NUMRE.match(t) or re.match(r'^s\d', t)) for t in tk]
            if mode == 'flat' and all(nums) and len(tk) % ncol == 0 and len(tk) >= ncol:
                n += len(tk) // ncol
    return n

def structure():
    print('a. cau truc')
    summary = {}
    for f in FILES:
        t = load(f)
        for k in ('table', 'title', 'pdf_pages', 'printed_pages', 'substance', 'units', 'columns', 'index'):
            if k not in t: fail(f'{f}: thiếu khóa {k}')
        if not t['title'].get('vi') or not t['title'].get('en'): fail(f'{f}: thiếu tiêu đề song ngữ')
        if [p + 908 for p in t['pdf_pages']] != t['printed_pages']: fail(f'{f}: trang in ≠ PDF+908')
        ncol = len(t['columns'])
        if 'rows' in t:
            rows = t['rows']
            if f in EXPECT_ROWS and len(rows) != EXPECT_ROWS[f]: fail(f'{f}: {len(rows)} hàng ≠ kỳ vọng {EXPECT_ROWS[f]}')
            for i, r in enumerate(rows):
                if len(r) != ncol: fail(f'{f} hàng {i}: {len(r)} cột ≠ {ncol}')
                for j, v in enumerate(r):
                    if v is None and not ALLOW_NONE.get(f): fail(f'{f} hàng {i} cột {j}: ô trống')
                    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)): fail(f'{f} hàng {i}: NaN/inf')
            if 'prec' in t and len(t['prec']) != len(rows): fail(f'{f}: prec không khớp')
            ic = t['columns'].index(t['index']) if t['index'] in t['columns'] else None
            if ic is not None and f not in ('A2b',):
                xs = [r[ic] for r in rows if r[ic] is not None and not isinstance(r[ic], str)]
                if any(b <= a for a, b in zip(xs, xs[1:])): fail(f'{f}: biến độc lập không đơn điệu')
            if f == 'A2b':
                for g in ('Air', 'CO2', 'CO', 'H2', 'N2', 'O2'):
                    xs = [r[1] for r in rows if r[0] == g]
                    if len(xs) != 14 or any(b <= a for a, b in zip(xs, xs[1:])): fail(f'A2b {g}: {len(xs)} nhiệt độ hoặc không đơn điệu')
            # dem doc lap theo trang
            if 'row_pages' in t and f in EXPECT_PAGE_ROWS:
                for pg, n in EXPECT_PAGE_ROWS[f].items():
                    got = t['row_pages'].count(pg)
                    if got != n: fail(f'{f} trang {pg}: {got} hàng ≠ {n} (đếm trên ảnh)')
            if f in ('A4', 'A5', 'A11', 'A12', 'A17', 'A17E') or f in ('A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25'):
                pgs = ['41a'] if f == 'A24' else (['41b'] if f == 'A25' else t['pdf_pages'])
                cnt = indep_token_count(pgs, ncol, 'flat')
                # hai cot: moi dong co the 1 hoac 2 hang -> tong token/ncol chinh xac neu khong dong nao thua token
                if cnt != len(rows): fail(f'{f}: đếm token độc lập {cnt} ≠ {len(rows)} hàng')
            summary[f] = len(rows)
        else:
            bl = t['blocks']
            if len(bl) != EXPECT_BLOCKS[f]: fail(f'{f}: {len(bl)} khối ≠ {EXPECT_BLOCKS[f]}')
            tot = 0
            for b in bl:
                for r in b['rows']:
                    if len(r) != ncol or any(v is None for v in r): fail(f'{f} khối {b["param"]} hàng {r}')
                xs = [r[0] for r in b['rows']]
                if any(y <= x for x, y in zip(xs, xs[1:])): fail(f'{f} khối {b["param"]}: T không đơn điệu')
                tsat = b['param'].get('Tsat_C')
                if f != 'A7' and tsat is not None and xs and xs[0] < tsat - 1e-9: fail(f'{f} khối {b["param"]}: có T < Tsat')
                if f == 'A7' and tsat is not None and xs and xs[-1] > tsat + 1e-9: fail(f'{f} khối {b["param"]}: có T > Tsat')
                if b['sat'] is not None and len(b['sat']) != ncol - 1: fail(f'{f}: sat sai cột')
                tot += len(b['rows']) + (1 if b['sat'] else 0)
            # dem token doc lap theo trang: dong co T/Sat dau + 4k so
            cnt = 0
            for p in t['pdf_pages']:
                for l in D_PAGES[p].split('\n'):
                    tk = l.split()
                    if tk and (tk[0].lower().startswith('sat') or re.match(r'^[\u2212-]?\d+(\.\d+)?$', tk[0])):
                        rest = tk[1:]
                        if rest and all(re.match(r'^[\u2212-]?(\d{1,3}(,\d{3})+|\d*\.?\d+)$', x) for x in rest) and len(rest) % 4 == 0:
                            cnt += len(rest) // 4
            if cnt != tot: fail(f'{f}: đếm token độc lập {cnt} ≠ {tot} (hàng + sat)')
            summary[f] = tot
    # A-7: cau truc dac biet (khong co T=380 o khoi 20 MPa)
    a7 = load('A7'); b20 = [b for b in a7['blocks'] if b['param']['P_MPa'] == 20.0][0]
    if any(r[0] > 360 for r in b20['rows']): fail('A7: khối 20 MPa có hàng T > 360 (ô trống bị gán sai nhóm)')
    a6 = load('A6')
    for b in a6['blocks']:
        if b['param']['P_MPa'] <= 20 and b['sat'] is None: fail('A6: thiếu hàng Sat.')
    print('  hàng mỗi bảng (gồm sat của khối):', summary)
    return summary

# ---------------------------------------------------------------- b. doc tay
def find_cell(h):
    t = load(h['table'].replace('-', ''))
    col = h['col']; at = h['at']
    ci = t['columns'].index(col)
    if 'blocks' in t:
        for b in t['blocks']:
            if abs(b['param']['P_MPa'] - at['P_MPa']) > 1e-9: continue
            if at.get('sat'):
                if b['sat'] is None: return None
                return b['sat'][ci - 1]
            for r in b['rows']:
                if abs(r[0] - at['T_C']) < 1e-9: return r[ci]
        return None
    for r in t['rows']:
        ok = True
        for k, v in at.items():
            c = t['columns'].index(k)
            if isinstance(v, str):
                ok &= (str(r[c]) == v)
            else:
                ok &= (r[c] is not None and abs(r[c] - v) < 1e-9)
        if ok: return r[ci]
    return None

def handread():
    print('b. đọc tay từ ảnh')
    H = json.load(open(os.path.join(D, 'handread.json')))['cells']
    match = 0; bad = []; per = {}
    for h in H:
        v = find_cell(h)
        per.setdefault(h['table'], [0, 0])
        per[h['table']][1] += 1
        if v is None: bad.append((h, 'không tìm thấy ô')); continue
        if abs(v - h['value']) <= 1e-9 * max(1, abs(h['value'])) + 1e-15:
            match += 1; per[h['table']][0] += 1
        else: bad.append((h, f'bảng trích = {v}'))
    for h, why in bad: fail(f'đọc tay lệch: {h["table"]} {h["at"]} {h["col"]} đọc {h["value"]}: {why}')
    print(f'  khớp {match}/{len(H)} ô; theo bảng:', {k: f'{a}/{b}' for k, (a, b) in per.items()})
    neg = sum(1 for h in H if h['value'] < 0); exp = sum(1 for h in H if h['table'] == 'A-2c' and abs(h['value']) < 0.01)
    return dict(n=len(H), match=match, per_table=per, negatives=neg, exponent_cells=exp, pages=sorted({h['pdf_page'] for h in H}))

# ---------------------------------------------------------------- c. doi chieu
def crosscheck():
    print('c. đối chiếu thư viện (iapws / CoolProp)')
    py = os.path.join(P, '.venv', 'bin', 'python')
    import importlib
    try:
        import crosscheck as X
    except ImportError as e:
        fail(f'không nạp được crosscheck (chạy bằng .venv/bin/python -I): {e}')
        return None
    pts = X.run()
    import CoolProp.CoolProp as CP
    # chan doan nuoc: CoolProp Water (IAPWS-95) cho cac diem vuot dung sai IF97
    def alt_water(p):
        try:
            if p['table'] == 'A-4':
                T = p['key']['T_C'] + 273.15; q = 1 if p['col'] in ('vg', 'ug', 'hg', 'sg') else 0
                if p['col'] == 'Psat_kPa': return CP.PropsSI('P', 'T', T, 'Q', 0, 'Water') / 1000
                prop = {'v': 'D', 'u': 'U', 'h': 'H', 's': 'S'}.get(p['col'][0])
                if p['col'].endswith('fg'):
                    return (CP.PropsSI(prop, 'T', T, 'Q', 1, 'Water') - CP.PropsSI(prop, 'T', T, 'Q', 0, 'Water')) / 1000
                v = CP.PropsSI(prop, 'T', T, 'Q', q, 'Water')
                return 1 / v if prop == 'D' else v / 1000
            if p['table'] == 'A-5':
                Pp = p['key']['Psat_kPa'] * 1000; q = 1 if p['col'] in ('vg', 'ug', 'hg', 'sg') else 0
                if p['col'] == 'Tsat_C': return CP.PropsSI('T', 'P', Pp, 'Q', 0, 'Water') - 273.15
                prop = {'v': 'D', 'u': 'U', 'h': 'H', 's': 'S'}.get(p['col'][0])
                if p['col'].endswith('fg'):
                    return (CP.PropsSI(prop, 'P', Pp, 'Q', 1, 'Water') - CP.PropsSI(prop, 'P', Pp, 'Q', 0, 'Water')) / 1000
                v = CP.PropsSI(prop, 'P', Pp, 'Q', q, 'Water')
                return 1 / v if prop == 'D' else v / 1000
            if p['table'] in ('A-6', 'A-7') and 'T_C' in p['key']:
                prop = {'v': 'D', 'u': 'U', 'h': 'H', 's': 'S'}[p['col']]
                v = CP.PropsSI(prop, 'T', p['key']['T_C'] + 273.15, 'P', p['key']['P_MPa'] * 1e6, 'Water')
                return 1 / v if prop == 'D' else v / 1000
        except Exception:
            return None
        return None
    S = {}
    out = []
    for p in pts:
        key = f"{p['group']}|{p['table']}|{p['col']}"
        s = S.setdefault(key, dict(group=p['group'], table=p['table'], col=p['col'], n=0, n_out=0, max_abs_dev=0.0, max_rel_dev=0.0, max_factor=0.0, n_out_alt=0, n_alt=0))
        s['n'] += 1
        factor = abs(p['dev']) / p['tol']
        rel = abs(p['dev']) / max(abs(p['printed']), 10 * p['tol'])
        s['max_abs_dev'] = max(s['max_abs_dev'], abs(p['dev'])); s['max_rel_dev'] = max(s['max_rel_dev'], rel); s['max_factor'] = max(s['max_factor'], factor)
        alt = None
        if p['group'].startswith('water'):
            a = alt_water(p)
            if a is not None:
                alt = a - p['printed']; s['n_alt'] += 1
                if abs(alt) > p['tol'] + 1e-12: s['n_out_alt'] += 1
        if not p['ok']:
            s['n_out'] += 1
            out.append([p['table'], p['key'], p['col'], p['printed'], p['lib'], p['dev'], p['tol'], round(factor, 2), rel, alt])
    for s in S.values():
        s['max_abs_dev'] = float(s['max_abs_dev']); s['max_rel_dev'] = float(s['max_rel_dev']); s['max_factor'] = float(s['max_factor'])
    n = len(pts); nout = len(out)
    # xep nhom theo he so vuot
    buckets = {'<=2x': 0, '2-5x': 0, '5-20x': 0, '>20x': 0}
    for o in out:
        f = o[7]; buckets['<=2x' if f <= 2 else '2-5x' if f <= 5 else '5-20x' if f <= 20 else '>20x'] += 1
    rows_cmp = {}
    for p in pts:
        k = (p['group'], p['table'], json.dumps(p['key'], sort_keys=True))
        rows_cmp.setdefault(k, 0)
    causes = {
        'water/iapws': 'Bảng Cengel in từ EES (Steam_IAPWS, IAPWS-95); iapws.IAPWS97 là IF97 (hồi quy xấp xỉ IAPWS-95). Lệch thường ≤ vài đơn vị chữ số cuối, lớn nhất gần điểm tới hạn (T ≥ 350 °C hoặc P ≥ 20 MPa, vd A-5 tại 22 MPa: h_f lệch 10,8 kJ/kg với IF97 nhưng 0,24 với IAPWS-95) nơi IF97 kém IAPWS-95. Cột n_out_alt cho số điểm CoolProp Water (IAPWS-95) vẫn vượt dung sai: phần còn lại là làm tròn của bảng (dung sai = ½ chữ số in, chặt hơn sai số thực của các công thức). Quy chiếu đúng (u_f = s_f = 0 tại điểm ba): không có lệch hằng số.',
        'R134a/CoolProp': 'Quy chiếu ASHRAE khớp (h_f = s_f = 0 tại −40 °C: lệch 0,000). Lệch có hệ thống, trơn theo T: P_sat của CoolProp thấp hơn bảng 0,07 % ở 100 °C (T_sat cao hơn 0,015–0,043 K tại P tương ứng) và kéo theo lệch h, s cỡ 1e-4 tương đối. Nghi do EES dùng R134a (Tillner-Roth & Baehr 1994) với triển khai/hằng số khác CoolProp 8.0.0. Gần điểm tới hạn (T_c = 101,06 °C; ≥ 90 °C) lệch tăng mạnh (s_g lệch 0,003 kJ/(kg·K) ở 100 °C): hai triển khai của cùng phương trình trạng thái khác nhau nhiều nhất ở đó. Nguyên nhân chính xác: chưa xác định. So sánh theo hiệu h, s cho kết quả tương tự (độ lệch cùng bậc).',
        'air/CoolProp-idealgas': 'Hiệu h(T)−h(300 K), s°(T)−s°(300 K) của bảng Keenan–Kaye (1948) so với giới hạn khí lý tưởng của CoolProp Air (hỗn hợp Lemmon 2000, M = 28,9586): khác nhau về cp0(T) và thành phần; lệch tăng đều theo T (cỡ 0,04 % ở 2250 K); Pr lệch theo e^(Δs°/R) nên lệch tương đối bậc 0,1–1 % ở T cao. Nguyên nhân chính xác: chưa xác định (nghi dữ liệu cp0 và thành phần khác).',
    }
    def near_crit(o):
        k = o[1]
        if o[0] in ('A-4',): return k['T_C'] >= 350
        if o[0] in ('A-5',): return k['Psat_kPa'] >= 20000
        if o[0] in ('A-6', 'A-7'): return k.get('P_MPa', 0) >= 20
        if o[0] == 'A-11': return k['T_C'] >= 90
        if o[0] == 'A-12': return False
        return False
    n_nc = sum(1 for o in out if near_crit(o))
    J = dict(out_excluding_near_critical=nout - n_nc, out_near_critical=n_nc, description='Đối chiếu bảng in (Cengel Appendix 1) với thư viện. Dung sai mỗi ô = ½ đơn vị chữ số cuối in. Mọi điểm vượt dung sai được liệt kê trong out_of_tolerance, không che.',
             references=dict(water='iapws 1.5.5 IAPWS97 (u_f = s_f = 0 tại điểm ba); chẩn đoán thêm CoolProp Water (IAPWS-95)', R134a='CoolProp 8.0.0 R134a, set_reference_state(ASHRAE)', air='CoolProp Air ở 100 Pa (khí lý tưởng), so theo hiệu với 300 K'),
             total_points=n, out_of_tolerance_count=nout, within_tolerance=n - nout, out_buckets_by_tolerance_multiple=buckets, causes=causes,
             summary=sorted(S.values(), key=lambda s: (s['group'], s['table'], s['col'])),
             out_columns=['table', 'key', 'col', 'printed', 'lib', 'dev', 'tol', 'factor', 'rel_dev', 'dev_coolprop_water'], out_of_tolerance=out)
    with open(os.path.join(D, 'crosscheck.json'), 'w') as f: json.dump(J, f, ensure_ascii=False, separators=(',', ':'))
    print(f'  {n} điểm (ô), {nout} vượt dung sai ½ chữ số cuối (trong đó {n_nc} gần tới hạn); theo bội dung sai: {buckets}')
    for g in ('water/iapws', 'R134a/CoolProp', 'air/CoolProp-idealgas'):
        sub = [p for p in pts if p['group'] == g]
        print(f'  {g}: {len(sub)} điểm, {sum(1 for p in sub if not p["ok"])} vượt; max độ lệch tương đối {max(abs(p["dev"]) / max(abs(p["printed"]), 10 * p["tol"]) for p in sub):.3e}')
    # so luong "diem" theo hang
    rows = {(p['table'], json.dumps(p['key'], sort_keys=True)) for p in pts}
    print(f'  số hàng/trạng thái khác nhau đã đối chiếu: {len(rows)}')
    if len(rows) < 30: fail('ít hơn 30 điểm đối chiếu')
    return dict(points=n, rows=len(rows), out=nout, buckets=buckets)

# ---------------------------------------------------------------- d. bai co dap an in
def close(name, got, exp, tol):
    ok = abs(got - exp) <= tol
    print(f'  {"ok  " if ok else "FAIL"} {name}: {got:.4f} (đáp án {exp}, dung sai {tol})')
    if not ok: fail(f'ví dụ {name}: {got} ≠ {exp} ± {tol}')

def examples():
    print('d. bài có đáp án in (Tutorials I)')
    A = L.air; AI = L.air_inverse
    # Otto #1 (slide Tutorials tr.2-6)
    r, q, T1, P1 = 8, 800.0, 290.0, 100.0
    u1 = A(T1, 'u')['value']; vr1 = A(T1, 'vr')['value']
    i2 = AI('vr', vr1 / r); T2 = i2['value']; u2 = i2['extra']['u']
    P2 = P1 * (T2 / T1) * r
    close('Otto#1 T2 [K]', T2, 652.4, 0.1); close('Otto#1 u2', u2, 475.11, 0.05); close('Otto#1 P2', P2, 1799.7, 1.0)
    i3 = AI('u', u2 + q); T3 = i3['value']; vr3 = i3['extra']['vr']
    close('Otto#1 T3', T3, 1575.1, 0.3); close('Otto#1 vr3', vr3, 6.108, 0.01)
    P3 = P2 * T3 / T2; close('Otto#1 P3', P3, 4345.0, 2.0)
    i4 = AI('vr', r * vr3); T4 = i4['value']; u4 = i4['extra']['u']
    close('Otto#1 T4', T4, 795.6, 0.2); close('Otto#1 u4', u4, 588.74, 0.1)
    w = q - (u4 - u1); close('Otto#1 w_net', w, 418.17, 0.15); close('Otto#1 eta', w / q, 0.523, 0.0006)
    v1 = 0.287 * T1 / P1; mep = w / (v1 * (1 - 1 / r)); close('Otto#1 MEP', mep, 574.0, 1.0)
    # Brayton rp = 8 (Tutorials tr.19-23)
    h1 = A(300, 'h')['value']; Pr1 = A(300, 'Pr')['value']
    i2 = AI('Pr', 8 * Pr1); T2 = i2['value']; h2 = i2['extra']['h']
    close('Brayton T2 (nội suy; slide làm tròn 540)', T2, 539.84, 0.01); close('Brayton h2', h2, 544.18, 0.01)
    h3 = A(1300, 'h')['value']; Pr3 = A(1300, 'Pr')['value']
    i4 = AI('Pr', Pr3 / 8); T4 = i4['value']; h4 = i4['extra']['h']
    close('Brayton T4', T4, 770.26, 0.01)
    close('Brayton w_turb', h3 - h4, 606.60, 0.05)
    close('Brayton w_comp (h2 nội suy; slide 244,16 dùng h2=544,35)', h2 - h1, 243.99, 0.01)
    close('Brayton bwr', (h2 - h1) / (h3 - h4), 0.403, 0.001)
    close('Brayton eta', ((h3 - h4) - (h2 - h1)) / (h3 - h2), 0.426, 0.0006)
    close('Brayton q_out', h4 - h1, 489.2, 0.3)
    # Diesel #5 (A-17, QA: T3 = 1724,7; eta = 0,563; MEP 675,6)
    rr, rc, T1 = 16, 2, 300.0
    i2 = AI('vr', A(T1, 'vr')['value'] / rr); T2 = i2['value']; h2 = i2['extra']['h']
    T3 = rc * T2; h3 = A(T3, 'h')['value']; vr3 = A(T3, 'vr')['value']
    i4 = AI('vr', vr3 * rr / rc); T4 = i4['value']; u4 = i4['extra']['u']
    qin = h3 - h2; qout = u4 - A(T1, 'u')['value']
    close('Diesel#5 T3', T3, 1724.7, 0.3); close('Diesel#5 eta', 1 - qout / qin, 0.563, 0.001)
    # #4 Otto (E): r = 8, 540 R, T3 = 2400 R
    i2 = AI('vr', A(540, 'vr', 'E')['value'] / 8, 'E'); u2 = i2['extra']['u']
    u3 = A(2400, 'u', 'E')['value']; vr3 = A(2400, 'vr', 'E')['value']
    i4 = AI('vr', 8 * vr3, 'E'); u4 = i4['extra']['u']
    close('#4 q_in [Btu/lbm]', u3 - u2, 241.4, 0.15); close('#4 eta', 1 - (u4 - A(540, 'u', 'E')['value']) / (u3 - u2), 0.530, 0.001)
    # #7 Brayton (E): rp = 10, 520 R / 2000 R
    h1 = A(520, 'h', 'E')['value']; Pr1 = A(520, 'Pr', 'E')['value']
    i2 = AI('Pr', 10 * Pr1, 'E'); T2 = i2['value']; h2 = i2['extra']['h']
    h3 = A(2000, 'h', 'E')['value']; Pr3 = A(2000, 'Pr', 'E')['value']
    i4 = AI('Pr', Pr3 / 10, 'E'); h4 = i4['extra']['h']
    close('#7 T2 [R]', T2, 996.5, 0.1); close('#7 bwr', (h2 - h1) / (h3 - h4), 0.485, 0.001); close('#7 eta', ((h3 - h4) - (h2 - h1)) / (h3 - h2), 0.465, 0.001)
    # #8: T3 tu h3 = h(580) + 950
    h2 = A(580, 'h')['value']; T3 = AI('h', h2 + 950)['value']; close('#8 T3', T3, 1417, 0.5)
    # R-134a 0,14-0,8 MPa (Tutorials tr.24-27)
    h1 = L.sat_P('R134a', 140, 'hg')['value']; s1 = L.sat_P('R134a', 140, 'sg')['value']
    r2 = L.superheated_inverse('R134a', 0.8, 's', s1); h2 = r2['extra']['h']
    h3 = L.sat_P('R134a', 800, 'hf')['value']
    close('R134a h1', h1, 239.16, 0.005); close('R134a h2', h2, 275.39, 0.02); close('R134a h3', h3, 95.47, 0.005)
    cop = (h1 - h3) / (h2 - h1); close('R134a COP', cop, 3.97, 0.01)
    close('R134a Q_L [kW]', 0.05 * (h1 - h3), 7.18, 0.005); close('R134a W_in [kW]', 0.05 * (h2 - h1), 1.81, 0.005)
    # cac o lien quan phai gan co suspect
    if not L.air(550, 'h')['suspect'] or not L.air(630, 'Pr')['suspect'] or not L.air(1040, 'vr')['suspect'] or not L.air(2150, 'Pr', 'E')['suspect'] or not L.isentropic(3.0, 'rho_rho0')['suspect']:
        fail('ô lỗi in đã biết không được đánh dấu suspect')
    # truy van tren o khong loi khong duoc suspect
    if L.air(600, 'h')['suspect']: fail('ô 600 K h bị đánh dấu suspect oan')
    # khong ngoai suy
    for fn, args in ((L.sat_T, ('water', 400, 'hg')), (L.air, (100, 'h')), (L.superheated, ('water', 0.001, 100, 'h')), (L.isentropic, (6, 'P_P0'))):
        try:
            fn(*args); fail(f'{fn.__name__}{args} phải báo ngoài phạm vi')
        except L.PropsRangeError:
            pass
    print('  ngoài phạm vi bị từ chối (4/4), ô suspect được đánh dấu')

# ---------------------------------------------------------------- errata
def errata_check():
    print('e. book_errata.json')
    E = load('book_errata')
    for e in E['errors']:
        t = load(e['table'].replace('-', ''))
        ci = t['columns'].index(e['col']); kv = list(e['key'].values())[0]
        row = [r for r in t['rows'] if r[0] is not None and not isinstance(r[0], str) and abs(r[0] - kv) < 1e-9] if e['table'] != 'A-2a' else [r for r in t['rows'] if r[0] == e['key']['gas']]
        if len(row) != 1 or abs(row[0][ci] - e['printed']) > 1e-9:
            fail(f'errata không khớp bảng: {e["table"]} {e["key"]} {e["col"]}')
    kinds = {}
    for e in E['errors']: kinds[e['kind']] = kinds.get(e['kind'], 0) + 1
    seen = sum(1 for e in E['errors'] if e['seen_image'])
    print(f'  {E["n"]} mục: {kinds}; đã xem ảnh trang: {seen}/{E["n"]}')

def node_parity():
    print('f. JS = Python')
    r = subprocess.run(['node', os.path.join(P, 'tests', 'props_node_test.js')], capture_output=True, text=True)
    print('  ' + r.stdout.strip().split('\n')[-2])
    if r.returncode != 0: fail('props_node_test.js thất bại:\n' + r.stdout[-800:])

if __name__ == '__main__':
    st = structure(); hr = handread(); errata_check(); cc = crosscheck(); examples(); node_parity()
    print('FAILS:', 'none' if not FAILS else f'{len(FAILS)}')
    sys.exit(1 if FAILS else 0)
