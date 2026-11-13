"""Kiem nhat quan noi bang (khong dung thu vien ngoai): tim cac o nghi la LOI IN cua sach.
Chay: python3 -I build/props/consistency.py  -> in ket qua; ham run() tra ve danh sach phat hien."""
import json, math, os, statistics
P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
D = os.path.join(P, 'data', 'props')
def load(n): return json.load(open(os.path.join(D, n + '.json')))
def hu(d): return 0.5 * 10 ** (-d)

def run():
    F = []   # finding: dict(table, key, issue, detail)
    # ---- bao hoa ----
    for fn, kcol in (('A4', 'T_C'), ('A5', 'Psat_kPa'), ('A11', 'T_C'), ('A12', 'Psat_kPa')):
        t = load(fn); cols = t['columns']; ix = {c: i for i, c in enumerate(cols)}
        for r, pr, pg in zip(t['rows'], t['prec'], t['row_pages']):
            key = {kcol: r[ix[kcol]]}
            Ps = r[ix['Psat_kPa']]
            for a, b, c, nm in (('hf', 'hfg', 'hg', 'h_fg=h_g-h_f'), ('uf', 'ufg', 'ug', 'u_fg=u_g-u_f'), ('sf', 'sfg', 'sg', 's_fg=s_g-s_f')):
                tol = hu(pr[ix[a]]) + hu(pr[ix[b]]) + hu(pr[ix[c]])
                dif = r[ix[c]] - r[ix[a]] - r[ix[b]]
                if abs(dif) > tol + 1e-12:
                    F.append(dict(table=t['table'], key=key, pdf_page=pg, check=nm, diff=round(dif, 6), tol=round(tol, 6)))
            for u, h, v, nm in (('uf', 'hf', 'vf', 'u_f=h_f-P v_f'), ('ug', 'hg', 'vg', 'u_g=h_g-P v_g')):
                tol = hu(pr[ix[u]]) + hu(pr[ix[h]]) + Ps * hu(pr[ix[v]])
                dif = r[ix[h]] - Ps * r[ix[v]] - r[ix[u]]
                if abs(dif) > tol + 1e-12:
                    F.append(dict(table=t['table'], key=key, pdf_page=pg, check=nm, diff=round(dif, 6), tol=round(tol, 6)))
    # ---- khoi: h = u + P v ----
    for fn in ('A6', 'A7', 'A13'):
        t = load(fn)
        for b in t['blocks']:
            Pk = b['param']['P_MPa'] * 1000
            allr = [(r, p) for r, p in zip(b['rows'], b['prec'])]
            if b['sat']: allr.append(([b['param']['Tsat_C']] + b['sat'], [0] + b['sat_prec']))
            for r, pr in allr:
                v, u, h = r[1], r[2], r[3]
                tol = hu(pr[2]) + hu(pr[3]) + Pk * hu(pr[1])
                dif = h - u - Pk * v
                if abs(dif) > tol + 1e-12:
                    F.append(dict(table=t['table'], key={'P_MPa': b['param']['P_MPa'], 'T_C': r[0]}, pdf_page=b['pdf_page'], check='h=u+Pv', diff=round(dif, 5), tol=round(tol, 5)))
    # ---- A-17 / A-17E ----
    for fn, kcol in (('A17', 'T_K'), ('A17E', 'T_R')):
        t = load(fn); rows = t['rows']; pr = t['prec']; pg = t['row_pages']
        Rs = [(r[1] - r[3]) / r[0] for r in rows]; Rm = statistics.median(Rs)
        C = [r[4] * r[2] / r[0] for r in rows]; Cm = statistics.median(C)
        for i, r in enumerate(rows):
            T, h, Pr, u, vr, s = r
            tolh = (hu(pr[i][1]) + hu(pr[i][3])) / T
            if abs((h - u) / T - Rm) > tolh + 0.00012 * 1:   # R theo median
                F.append(dict(table=t['table'], key={kcol: T}, pdf_page=pg[i], check='h-u=R*T', diff=round(h - u - Rm * T, 4), tol=round((tolh + 0.00012) * T, 4), R_median=round(Rm, 6)))
            tolc = Cm * (0.5 * 10 ** (-pr[i][2]) / Pr + 0.5 * 10 ** (-pr[i][4]) / vr) + 3e-4
            if abs(C[i] - Cm) > tolc:
                F.append(dict(table=t['table'], key={kcol: T}, pdf_page=pg[i], check='v_r*P_r/T=const', diff=round(C[i] / Cm - 1, 5), tol=round(tolc / Cm, 5), const_median=round(Cm, 5)))
        Rg = Rm
        for i in range(len(rows) - 1):
            a, b = rows[i], rows[i + 1]
            Tl = (b[0] - a[0]) / math.log(b[0] / a[0])
            ds = (b[1] - a[1]) / Tl
            tol = 6e-5 + (hu(pr[i][1]) + hu(pr[i + 1][1])) / Tl + hu(pr[i][5]) * 2 + 2e-4 * (b[0] - a[0]) / 100 * 0 
            # ds nho sai so cua cp(T) tuyen tinh: cho phep 3e-4 * (dT/T)^2... dung nguong thuc nghiem
            tol += 0.02 * ((b[0] - a[0]) / b[0]) ** 2 * 0.1
            if abs((b[5] - a[5]) - ds) > tol:
                F.append(dict(table=t['table'], key={kcol: (a[0], b[0])}, pdf_page=pg[i], check='ds0=dh/T', diff=round((b[5] - a[5]) - ds, 6), tol=round(tol, 6)))
            lnr = math.log(b[2] / a[2]); ex = (b[5] - a[5]) / Rg
            tolp = 0.5 * 10 ** (-pr[i][2]) / a[2] + 0.5 * 10 ** (-pr[i + 1][2]) / b[2] + 6e-5 / Rg * 2
            if abs(lnr - ex) > tolp + 4e-4:
                F.append(dict(table=t['table'], key={kcol: (a[0], b[0])}, pdf_page=pg[i], check='ln(Pr2/Pr1)=ds0/R', diff=round(lnr - ex, 6), tol=round(tolp + 4e-4, 6)))
    # ---- khi theo kmol ----
    for fn in ('A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25'):
        t = load(fn); rows = t['rows']; pr = t['prec']; pg = t['row_pages']
        for i, r in enumerate(rows):
            if r[0] == 0: continue
            T, h, u, s = r
            tol = 0.5 + 0.5 + 0.02 * T * 0 + 0.01 * 0
            if abs(h - u - 8.31447 * T) > 1.2 + 0.001 * T / 100:
                F.append(dict(table=t['table'], key={'T_K': T}, pdf_page=pg[i], check='h-u=Ru*T', diff=round(h - u - 8.31447 * T, 3), tol=1.2))
        for i in range(1, len(rows) - 1):
            a, b = rows[i], rows[i + 1]
            if a[0] == 0 or b[0] == 0: continue
            Tl = (b[0] - a[0]) / math.log(b[0] / a[0]); ds = (b[1] - a[1]) / Tl
            tol = 0.0015 + 1.0 / Tl + 0.002 * ((b[0] - a[0]) / b[0]) * 0
            if abs((b[3] - a[3]) - ds) > 0.06 + 0.0005 * ds * 0 + 2 * 1.0 / Tl + 0.01 * (b[3] - a[3]):
                F.append(dict(table=t['table'], key={'T_K': (a[0], b[0])}, pdf_page=pg[i], check='ds0=dh/T', diff=round((b[3] - a[3]) - ds, 4), tol=round(0.06 + 2.0 / Tl + 0.01 * (b[3] - a[3]), 4)))
    # ---- A-1, A-2 ----
    a1 = load('A1')
    for r, pr in zip(a1['rows'], a1['prec']):
        Rv = 8.31447 / r[2]; tol = hu(pr[3]) + 8.31447 * hu(pr[2]) / r[2] ** 2
        if abs(Rv - r[3]) > tol + 1e-9:
            F.append(dict(table='A-1', key={'substance': r[0]}, pdf_page=2, check='R=Ru/M', diff=round(r[3] - Rv, 6), tol=round(tol, 6)))
    a2 = load('A2a')
    for r, pr in zip(a2['rows'], a2['prec']):
        _, _, R, cp, cv, k = r
        if abs(cp - cv - R) > hu(pr[3]) + hu(pr[4]) + hu(pr[2]) + 1e-9:
            F.append(dict(table='A-2a', key={'gas': r[0]}, pdf_page=3, check='cp-cv=R', diff=round(cp - cv - R, 5), tol=round(hu(pr[3]) + hu(pr[4]) + hu(pr[2]), 5)))
        if abs(cp / cv - k) > hu(pr[5]) + (cp / cv) * (hu(pr[3]) / cp + hu(pr[4]) / cv) + 1e-9:
            F.append(dict(table='A-2a', key={'gas': r[0]}, pdf_page=3, check='k=cp/cv', diff=round(cp / cv - k, 5), tol=0))
    a2b = load('A2b')
    for r, pr in zip(a2b['rows'], a2b['prec']):
        g, T, cp, cv, k = r
        tol = hu(pr[4]) + (cp / cv) * (hu(pr[2]) / cp + hu(pr[3]) / cv)
        if abs(cp / cv - k) > tol + 1e-9:
            F.append(dict(table='A-2b', key={'gas': g, 'T_K': T}, pdf_page=4, check='k=cp/cv', diff=round(cp / cv - k, 5), tol=round(tol, 5)))
    # ---- A-32 ----
    t = load('A32'); kk = 1.4
    for r, pr in zip(t['rows'], t['prec']):
        M = r[0]
        if M is None or M == 0: continue
        th = 1 / (1 + 0.2 * M * M)
        calc = dict(Ma_star=M * math.sqrt((kk + 1) / (2 + (kk - 1) * M * M)), A_Astar=(1 / M) * ((2 / (kk + 1)) * (1 + (kk - 1) / 2 * M * M)) ** ((kk + 1) / (2 * (kk - 1))),
                    P_P0=th ** 3.5, rho_rho0=th ** 2.5, T_T0=th)
        for j, c in enumerate(('Ma_star', 'A_Astar', 'P_P0', 'rho_rho0', 'T_T0'), start=1):
            val = r[j]
            if val is None: continue
            tol = hu(pr[j]) + 1e-9
            if abs(calc[c] - val) > tol:
                F.append(dict(table='A-32', key={'Ma': M}, pdf_page=48, col=c, check='cong thuc k=1.4', printed=val, expected=round(calc[c], 5), diff=round(val - calc[c], 5), tol=tol))
    return F

if __name__ == '__main__':
    F = run()
    from collections import Counter
    print(len(F), Counter((f['table'], f['check']) for f in F))
    for f in F: print(f)
