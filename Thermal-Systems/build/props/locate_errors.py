"""Dinh vi o in sai (khong chi cap o lech): dung cac quan he vat ly + noi suy hang xom.
Tra ve danh sach dict(table, key, col, printed, expected, how). Dung boi build_errata.py."""
import json, math, os, statistics
P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
D = os.path.join(P, 'data', 'props')
RU = 8.31447
def load(n): return json.load(open(os.path.join(D, n + '.json')))

def neighbour_pred(rows, i, c):
    a, b, d = rows[i - 1], rows[i], rows[i + 1]
    f = (b[0] - a[0]) / (d[0] - a[0])
    return a[c] + f * (d[c] - a[c])

def kmol_tables():
    out = []
    for fn in ('A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25'):
        t = load(fn); R = [list(r) for r in t['rows']]; pg = t['row_pages']; tb = t['table']
        orig = [list(r) for r in R]
        found = {}
        for _ in range(6):
            ch = False
            for i in range(1, len(R) - 1):
                if R[i][0] in (0, 298) or R[i - 1][0] == 0 or R[i + 1][0] == 0: continue
                T, h, u, s = R[i]
                diff = h - u - RU * T
                if abs(diff) > 2.6:
                    dh = abs(h - neighbour_pred(R, i, 1)); du = abs(u - neighbour_pred(R, i, 2))
                    if dh > du:
                        ex = round(u + RU * T); R[i][1] = ex; col = 'h'; how = 'h̄ = ū + Ru·T (ū khớp nội suy hàng xóm)'
                    else:
                        ex = round(h - RU * T); R[i][2] = ex; col = 'u'; how = 'ū = h̄ − Ru·T (h̄ khớp nội suy hàng xóm)'
                    found[(i, col)] = dict(table=tb, key={'T_K': T}, col=col, printed=orig[i][1 if col == 'h' else 2], expected=ex, pdf_page=pg[i], how=how, diff=round(diff, 1)); ch = True
            if not ch: break
        out += list(found.values())
        # s0 (sau khi da sua h)
        def ds(x, y):
            Tl = (y[0] - x[0]) / math.log(y[0] / x[0]); return (y[3] - x[3]) - (y[1] - x[1]) / Tl
        for i in range(1, len(R) - 1):
            a, b, c = R[i - 1], R[i], R[i + 1]
            if 0 in (a[0], b[0], c[0]): continue
            d1, d2 = ds(a, b), ds(b, c)
            lim = 0.045 + 1.5 / b[0]
            if abs(d1) > lim and abs(d2) > lim and abs(d1 + d2) < 0.35 * max(abs(d1), abs(d2)):
                Tl = (b[0] - a[0]) / math.log(b[0] / a[0]); exp = a[3] + (b[1] - a[1]) / Tl
                out.append(dict(table=tb, key={'T_K': b[0]}, col='s0', printed=b[3], expected=round(exp, 3), pdf_page=pg[i], how='s̄° = s̄°(hàng trước) + Δh̄/T_lm; hai hiệu liền kề lệch bằng nhau, ngược dấu', diff=round(b[3] - exp, 3)))
    return out

def air_tables():
    out = []
    for fn, kc in (('A17', 'T_K'), ('A17E', 'T_R')):
        t = load(fn); R = t['rows']; pg = t['row_pages']; tb = t['table']
        Rm = statistics.median([(r[1] - r[3]) / r[0] for r in R]); Cm = statistics.median([r[4] * r[2] / r[0] for r in R])
        for i in range(1, len(R) - 1):
            T, h, Pr, u, vr, s = R[i]
            tolr = 0.5 / 100
            # h - u
            if abs((h - u) / T - Rm) * T > 0.35 + T * 1.5e-4 * 0 and abs(h - u - Rm * T) > 0.25 + 1.5e-4 * T:
                dh = abs(h - neighbour_pred(R, i, 1)); du = abs(u - neighbour_pred(R, i, 3))
                # dung do cong: so sanh lech so voi ky vong
                (col, pr_, ex) = ('h', h, u + Rm * T) if dh > du else ('u', u, h - Rm * T)
                out.append(dict(table=tb, key={kc: T}, col=col, printed=pr_, expected=round(ex, 2), pdf_page=pg[i], how=f'h − u = R·T với R = {Rm:.5f} (trung vị cả bảng); hàng xóm cho biết ô {col} lệch', diff=round(h - u - Rm * T, 3)))
            # Pr theo s0
            a, b = R[i - 1], R[i]; c = R[i + 1]
            e1 = math.log(b[2] / a[2]) - (b[5] - a[5]) / Rm; e2 = math.log(c[2] / b[2]) - (c[5] - b[5]) / Rm
            if abs(e1) > 0.0015 and abs(e2) > 0.0015 and e1 * e2 < 0 and abs(e1 + e2) < 0.5 * abs(e1):
                exp = a[2] * math.exp((b[5] - a[5]) / Rm)
                out.append(dict(table=tb, key={kc: T}, col='Pr', printed=Pr, expected=float('%.4g' % exp), pdf_page=pg[i], how='P_r = P_r(hàng trước)·exp(Δs°/R); hai cặp liền kề lệch ngược dấu', diff=round(Pr / exp - 1, 4)))
            # vr
            if abs(vr * Pr / T / Cm - 1) > 0.006:
                # neu Pr khong bi danh dau thi vr sai
                exp = Cm * T / Pr
                out.append(dict(table=tb, key={kc: T}, col='vr', printed=vr, expected=float('%.4g' % exp), pdf_page=pg[i], how=f'v_r = const·T/P_r, const = {Cm:.4f} (trung vị)', diff=round(vr / exp - 1, 4)))
            # s0 sai (hai cap ds deu lech nguoc dau)
            def ds(x, y):
                Tl = (y[0] - x[0]) / math.log(y[0] / x[0]); return (y[5] - x[5]) - (y[1] - x[1]) / Tl
            d1, d2 = ds(a, b), ds(b, c)
            if abs(d1) > 2.5e-4 and abs(d2) > 2.5e-4 and d1 * d2 < 0 and abs(abs(d1) - abs(d2)) < 3e-4:
                # nghi h hoac s0 sai: neu Pr khong lech thi la h
                Tl = (b[0] - a[0]) / math.log(b[0] / a[0])
                out.append(dict(table=tb, key={kc: T}, col='h|s0', printed=[h, s], expected=None, pdf_page=pg[i], how='Δs° vs Δh/T lệch ngược dấu ở hai cặp liền kề: h hoặc s° tại hàng này', diff=[round(d1, 5), round(d2, 5)]))
    return out

if __name__ == '__main__':
    for e in kmol_tables() + air_tables(): print(e)
