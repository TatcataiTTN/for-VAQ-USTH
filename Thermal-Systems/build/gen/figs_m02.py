"""m02 figures (matplotlib, dpi 100, figsize = displayed px / 100, text >= 13 pt), Vietnamese and English versions -> assets/figs/m02/*.png
All curves are computed (cold air, k = 1.4, R = 0.287, cp = 1.005, cv = 0.718), not traced from the slides; the points read off slide images are marked as such.
Run: .venv/bin/python -I build/gen/figs_m02.py"""
import os, sys, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
from m02_common import brayton, rp_opt, turbojet_unchoked, CP_AIR, CV_AIR, R_AIR
OUT = os.path.join(ROOT, 'assets', 'figs', 'm02'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13, 'axes.titlesize': 14, 'axes.labelsize': 14, 'legend.fontsize': 12, 'xtick.labelsize': 12, 'ytick.labelsize': 12, 'axes.grid': False})
NAVY, RED, GRN, ORG, GRY, PUR = '#1f3a5f', '#c0392b', '#2e8b57', '#d98324', '#7f8c8d', '#7d3c98'
K, R, CP, CV = 1.4, R_AIR, CP_AIR, CV_AIR
def save(fig, name, lang): fig.savefig(os.path.join(OUT, f'{name}_{lang}.png'), dpi=100); plt.close(fig)
def label_pts(ax, pts, dx, fs=15):
    for n, (x, y) in pts.items(): ax.annotate(str(n), (x, y), xytext=(dx.get(n, (6, 6))[0], dx.get(n, (6, 6))[1]), textcoords='offset points', fontsize=fs, fontweight='bold', color=NAVY)
def arrow(ax, x0, y0, x1, y1, c): ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='-|>', color=c, lw=1.6))
def styl(ax, xl, yl):
    ax.set_xlabel(xl); ax.set_ylabel(yl); ax.set_xticks([]); ax.set_yticks([])
    for s in ('top', 'right'): ax.spines[s].set_visible(False)

# ---------------------------------------------------------------- 1,2: Otto and Diesel in P-v and T-s
def cycles(kind, lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    r = 8.0 if kind == 'otto' else 18.0; T1, P1 = 300.0, 1.0; v1 = R * T1 / P1; v2 = v1 / r
    T2 = T1 * r ** (K - 1); P2 = P1 * r ** K
    if kind == 'otto': T3 = 1800.0; v3 = v2; P3 = P2 * T3 / T2; rc = 1.0
    else: rc = 2.0; T3 = T2 * rc; v3 = v2 * rc; P3 = P2
    T4 = T3 * (v3 / v1) ** (K - 1); P4 = P1 * T4 / T1
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.0, 3.3)); fig.subplots_adjust(left=.07, right=.99, bottom=.15, top=.88, wspace=.2)
    v = np.linspace(v1, v2, 120); a.plot(v, P1 * (v1 / v) ** K, color=RED, lw=2.4)
    if kind == 'otto': a.plot([v2, v2], [P2, P3], color=RED, lw=2.4)
    else: a.plot([v2, v3], [P2, P3], color=RED, lw=2.4)
    v = np.linspace(v3, v1, 120); a.plot(v, P3 * (v3 / v) ** K, color=RED, lw=2.4); a.plot([v1, v1], [P4, P1], color=RED, lw=2.4)
    pts = {1: (v1, P1), 2: (v2, P2), 3: (v3, P3), 4: (v1, P4)}; a.scatter(*zip(*pts.values()), color=NAVY, zorder=5, s=28)
    label_pts(a, pts, {1: (-14, -16), 2: (-18, 2), 3: ((-4, 8) if kind == 'otto' else (6, 4)), 4: (-14, 6)}); styl(a, L('thể tích riêng v', 'specific volume v'), L('áp suất P', 'pressure P'))
    if kind == 'otto': a.text(v2 + (v1 - v2) * .06, (P2 + P3) / 2 * 0.9, 'q_in', color=ORG, fontsize=14, fontweight='bold')
    else: a.text(v3 + 0.1 * v1, P3 * 0.93, 'q_in', color=ORG, fontsize=14, fontweight='bold', ha='left'); a.set_ylim(0, P3 * 1.2)
    a.text(v1 * 1.03, (P4 * P1) ** .5, 'q_out', color=GRN, fontsize=14, fontweight='bold', ha='left'); a.set_xlim(0, v1 * 1.3)
    a.set_title(L('P–v (tự vẽ lại)', 'P–v (redrawn)'), loc='left', fontsize=13)
    # T-s
    s = lambda T, P: CP * math.log(T / T1) - R * math.log(P / P1)
    s1, s2 = 0.0, 0.0; s3 = s(T3, P3) if kind == 'diesel' else CV * math.log(T3 / T2); s4 = s3
    b.plot([s1, s2], [T1, T2], color=RED, lw=2.4)
    if kind == 'otto': Ts = np.linspace(T2, T3, 80); b.plot(CV * np.log(Ts / T2), Ts, color=RED, lw=2.4)
    else: Ts = np.linspace(T2, T3, 80); b.plot(CP * np.log(Ts / T2), Ts, color=RED, lw=2.4)
    b.plot([s3, s4], [T3, T4], color=RED, lw=2.4); Ts = np.linspace(T1, T4, 80); b.plot(CV * np.log(Ts / T1), Ts, color=RED, lw=2.4)
    pts = {1: (0, T1), 2: (0, T2), 3: (s3, T3), 4: (s4, T4)}; b.scatter(*zip(*pts.values()), color=NAVY, zorder=5, s=28)
    label_pts(b, pts, {1: (-16, -4), 2: (-18, 2), 3: (4, 6), 4: (6, -4)}); styl(b, L('entropi riêng s', 'specific entropy s'), L('nhiệt độ T', 'temperature T'))
    xm = max(s3, s4) * .5; b.text(xm * .85, (T2 + T3) / 2 * (1.25 if kind == 'otto' else 1.05), 'q_in', color=ORG, fontsize=14, fontweight='bold'); b.text(xm * 1.0, T1 * 0.8, 'q_out', color=GRN, fontsize=14, fontweight='bold'); b.set_ylim(T1 * 0.7, T3 * 1.08)
    b.set_title(L('T–s (tự vẽ lại)', 'T–s (redrawn)'), loc='left', fontsize=13)
    save(fig, f'fig_{kind}', lang)

# ---------------------------------------------------------------- 3: Brayton in T-s and P-v
def brayton_fig(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    rp, T1, T3 = 8.0, 300.0, 1300.0; P1 = 1.0; x = rp ** ((K - 1) / K); T2 = T1 * x; T4 = T3 / x
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.0, 3.3)); fig.subplots_adjust(left=.07, right=.99, bottom=.15, top=.88, wspace=.2)
    s = lambda T, P: CP * math.log(T / T1) - R * math.log(P / P1)
    b.plot([0, 0], [T1, T2], color=RED, lw=2.4); Ts = np.linspace(T2, T3, 80); b.plot([s(t, rp) for t in Ts], Ts, color=RED, lw=2.4); s3 = s(T3, rp)
    b.plot([s3, s3], [T3, T4], color=RED, lw=2.4); Ts = np.linspace(T1, T4, 80); b.plot([s(t, 1) for t in Ts], Ts, color=RED, lw=2.4)
    pts = {1: (0, T1), 2: (0, T2), 3: (s3, T3), 4: (s3, T4)}; b.scatter(*zip(*pts.values()), color=NAVY, zorder=5, s=28); label_pts(b, pts, {1: (-16, -4), 2: (-18, 2), 3: (4, 6), 4: (6, -4)})
    b.text(s3 * .42, (T2 + T3) / 2 + 80, 'q_in', color=ORG, fontsize=14, fontweight='bold'); b.text(s3 * .6, T1 * 0.8, 'q_out', color=GRN, fontsize=14, fontweight='bold')
    b.set_ylim(T1 * 0.7, T3 * 1.08); styl(b, L('entropi riêng s', 'specific entropy s'), L('nhiệt độ T', 'temperature T'))
    b.set_title(L('T–s (tự vẽ lại)', 'T–s (redrawn)'), loc='left', fontsize=13)
    v1 = R * T1 / P1; v2 = R * T2 / (rp * P1); v3 = R * T3 / (rp * P1); v4 = R * T4 / P1
    v = np.linspace(v1, v2, 100); a.plot(v, P1 * (v1 / v) ** K, color=RED, lw=2.4); a.plot([v2, v3], [rp, rp], color=RED, lw=2.4)
    v = np.linspace(v3, v4, 100); a.plot(v, rp * (v3 / v) ** K, color=RED, lw=2.4); a.plot([v4, v1], [P1, P1], color=RED, lw=2.4)
    pts = {1: (v1, P1), 2: (v2, rp), 3: (v3, rp), 4: (v4, P1)}; a.scatter(*zip(*pts.values()), color=NAVY, zorder=5, s=28); label_pts(a, pts, {1: (-14, 4), 2: (-16, 2), 3: (4, 6), 4: (6, 4)})
    a.text((v2 + v3) / 2, rp * 1.08, 'q_in', color=ORG, fontsize=14, fontweight='bold', ha='center'); a.text((v1 + v4) / 2, P1 * .55, 'q_out', color=GRN, fontsize=14, fontweight='bold', ha='center'); a.set_ylim(0, rp * 1.3)
    styl(a, L('thể tích riêng v', 'specific volume v'), L('áp suất P', 'pressure P')); a.set_title(L('P–v (tự vẽ lại)', 'P–v (redrawn)'), loc='left', fontsize=13)
    save(fig, 'fig_brayton', lang)

# ---------------------------------------------------------------- 4: efficiency vs r (Otto, Diesel) with slide readings
def eta_otto_diesel(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    fig, ax = plt.subplots(figsize=(6.6, 3.3)); fig.subplots_adjust(left=.13, right=.98, bottom=.19, top=.97); r = np.linspace(4, 24, 300)
    ax.plot(r[r <= 14], 1 - r[r <= 14] ** -(K - 1), color=NAVY, lw=2.6, label='Otto')
    ax.plot(r[r > 14], 1 - r[r > 14] ** -(K - 1), color=NAVY, lw=1.6, ls=':')
    for rc, c in ((2.0, RED), (3.0, ORG)):
        ax.plot(r, 1 - r ** -(K - 1) * (rc ** K - 1) / (K * (rc - 1)), color=c, lw=2.2, label=f'Diesel, $r_c$ = {rc:g}'.replace('.', ',' if lang == 'vi' else '.'))
    ax.axvspan(7, 10, color='#f8c9e0', alpha=.6, lw=0); ax.text(8.5, .26, L('xăng\n7–10', 'gasoline\n7–10'), ha='center', fontsize=12); ax.axvspan(12, 24, color='#cfe3f7', alpha=.5, lw=0); ax.text(18, .26, L('diesel 12–24', 'diesel 12–24'), ha='center', fontsize=12)
    ax.scatter([14], [0.665], marker='x', color=GRY, s=60, zorder=6); ax.annotate(L('đọc từ hình tr.25: 0,665', 'read off slide p.25: 0.665'), (14, .665), xytext=(9.0, .70), fontsize=11, color=GRY, arrowprops=dict(arrowstyle='-', color=GRY))
    ax.set_xlabel(L('tỉ số nén r (k = 1,4)', 'compression ratio r (k = 1.4)')); ax.set_ylabel(L('hiệu suất nhiệt', 'thermal efficiency')); ax.set_ylim(.2, .78); ax.set_xlim(4, 24); ax.grid(alpha=.3); ax.legend(loc='lower right', fontsize=11)
    save(fig, 'fig_eta_otto_diesel', lang)

# ---------------------------------------------------------------- 5: Brayton eta and w_net vs rp, T1 = 300, T3 = 1000
def brayton_work(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    T1, T3 = 300.0, 1000.0; fig, ax = plt.subplots(figsize=(7.4, 3.3)); fig.subplots_adjust(left=.12, right=.87, bottom=.19, top=.97); rp = np.linspace(1.5, 28, 300)
    eta = 1 - rp ** -(0.4 / 1.4); w = np.array([brayton(x, T1, T3)['wnet'] for x in rp]); ro = rp_opt(T3, T1)
    ax.plot(rp, eta, color=NAVY, lw=2.6, label=L('η (k = 1,4)', 'η (k = 1.4)')); ax.set_ylabel('η', color=NAVY); ax.set_ylim(0, .8); ax.set_xlabel(L('tỉ số áp suất $r_p$ (300 K, 1000 K)', 'pressure ratio $r_p$ (300 K, 1000 K)'))
    ax.scatter([20, 25], [.63, .653], marker='x', color=GRY, s=60, zorder=6); ax.annotate(L('đọc từ hình tr.40', 'read off slide p.40'), (20, .63), xytext=(14.3, .72), fontsize=11, color=GRY, arrowprops=dict(arrowstyle='-', color=GRY))
    ax2 = ax.twinx(); ax2.plot(rp, w, color=RED, lw=2.6, label='$w_{net}$'); ax2.set_ylabel('$w_{net}$ [kJ/kg]', color=RED); ax2.set_ylim(0, 260)
    ax2.axvline(ro, color=GRY, ls='--', lw=1.4); ax2.text(ro + .6, 18, f'$r_p$ = {ro:.2f}'.replace('.', ',' if lang == 'vi' else '.'), fontsize=12, color=GRY); ax.grid(alpha=.3); ax.set_xlim(0, 28)
    save(fig, 'fig_brayton_work', lang)

# ---------------------------------------------------------------- 6: regeneration vs none
def regen(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    fig, ax = plt.subplots(figsize=(6.6, 3.3)); fig.subplots_adjust(left=.12, right=.98, bottom=.19, top=.97); rp = np.linspace(2, 28, 300); x = rp ** (.4 / 1.4)
    ax.plot(rp, 1 - 1 / x, color=NAVY, lw=2.6, label=L('không hồi nhiệt', 'no regeneration'))
    for ratio, c in ((0.2, GRN), (0.25, ORG), (0.33, RED)):
        cross = (1 / ratio) ** (1.4 / .8); m = rp <= cross; ax.plot(rp[m], (1 - ratio * x)[m], color=c, lw=2.2, label=f'$T_1/T_3$ = {ratio:g}'.replace('.', ',' if lang == 'vi' else '.')); ax.plot(rp[~m], (1 - ratio * x)[~m], color=c, lw=1.4, ls=':')
    ax.set_xlabel(L('tỉ số áp suất $r_p$', 'pressure ratio $r_p$')); ax.set_ylabel(L('hiệu suất nhiệt', 'thermal efficiency')); ax.set_ylim(0, .8); ax.set_xlim(2, 28); ax.grid(alpha=.3); ax.legend(loc='lower center', fontsize=11, ncol=2)
    save(fig, 'fig_regen', lang)

# ---------------------------------------------------------------- 7: ideal 10-state cycle with intercooling, reheating, regeneration (slide p.48), cold air
def multistage(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    T1, T3 = 300.0, 1300.0; rp = 8.0; x = rp ** (.5 * .4 / 1.4); P1 = 1.0; Pm = P1 * math.sqrt(rp); Ph = rp * P1
    s = lambda T, P: CP * math.log(T / T1) - R * math.log(P / P1)
    T2 = T1 * x; T7 = T3 / x                  # states: 1 (T1,P1) 2 (T2,Pm) 3 (T1,Pm) 4 (T2,Ph) 5 (T7,Ph) 6 (T3,Ph) 7 (T7,Pm) 8 (T3,Pm) 9 (T7,P1) 10 (T2,P1)
    st = {1: (T1, P1), 2: (T2, Pm), 3: (T1, Pm), 4: (T2, Ph), 5: (T7, Ph), 6: (T3, Ph), 7: (T7, Pm), 8: (T3, Pm), 9: (T7, P1), 10: (T2, P1)}
    pt = {n: (s(T, P), T) for n, (T, P) in st.items()}
    fig, ax = plt.subplots(figsize=(6.6, 3.3)); fig.subplots_adjust(left=.14, right=.98, bottom=.15, top=.97)
    def isobar(Ta, Tb, P, c=RED, ls='-'): Ts = np.linspace(Ta, Tb, 60); ax.plot([s(t, P) for t in Ts], Ts, color=c, lw=2.2, ls=ls)
    def isentrope(n1, n2): ax.plot([pt[n1][0], pt[n2][0]], [pt[n1][1], pt[n2][1]], color=RED, lw=2.2)
    isentrope(1, 2); isobar(T2, T1, Pm); isentrope(3, 4); isobar(T2, T7, Ph); isobar(T7, T3, Ph); isentrope(6, 7); isobar(T7, T3, Pm); isentrope(8, 9); isobar(T7, T2, P1); isobar(T2, T1, P1)
    for n, (sx, T) in pt.items(): ax.scatter([sx], [T], color=NAVY, s=26, zorder=5); ax.annotate(str(n), (sx, T), xytext=({1: (5, -15), 2: (-4, 7), 3: (-17, -14), 4: (-17, 3), 5: (-17, 3), 6: (-8, 6), 7: (3, -14), 8: (4, 5), 9: (5, 3), 10: (5, -15)}[n]), textcoords='offset points', fontsize=14, fontweight='bold', color=NAVY)
    ax.set_xlabel(L('entropi riêng s', 'specific entropy s')); ax.set_ylabel(L('nhiệt độ T [K]', 'temperature T [K]')); ax.set_xticks([]); ax.set_ylim(200, 1450); ax.grid(alpha=.25)
    ax.text(pt[1][0] + .02, 1230, L('r_p = 8, 300 K và 1300 K\n(tr.48, tự vẽ lại, khí lạnh)', 'r_p = 8, 300 K and 1300 K\n(p.48, redrawn, cold air)'), fontsize=11, color=GRY, va='center')
    save(fig, 'fig_multistage', lang)

# ---------------------------------------------------------------- 8: ideal jet cycle T-s with the El-Sayed Example 4.2 numbers (cold air)
def jet_ts(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    ex = turbojet_unchoked(240, 32, 310, 12, 1400, 42700); Pa = 32.0; T1 = 240.0
    s = lambda T, P: CP * math.log(T / T1) - R * math.log(P / Pa)
    P02, P03 = ex['P02'], 12 * ex['P02']
    st = {1: (240, Pa), 2: (ex['T02'], P02), 3: (ex['T03'], P03), 4: (1400, P03), 5: (ex['T05'], ex['P05']), 6: (ex['T7'], Pa)}
    pt = {n: (s(T, P), T) for n, (T, P) in st.items()}
    fig, ax = plt.subplots(figsize=(6.6, 3.3)); fig.subplots_adjust(left=.14, right=.98, bottom=.15, top=.97)
    def line(n1, n2): ax.plot([pt[n1][0], pt[n2][0]], [pt[n1][1], pt[n2][1]], color=RED, lw=2.2)
    def isobar(Ta, Tb, P): Ts = np.linspace(Ta, Tb, 60); ax.plot([s(t, P) for t in Ts], Ts, color=RED, lw=2.2)
    line(1, 2); line(2, 3); isobar(st[3][0], 1400, P03); line(4, 5); line(5, 6); isobar(240, st[6][0], Pa)
    for n, (sx, T) in pt.items(): ax.scatter([sx], [T], color=NAVY, s=26, zorder=5); ax.annotate(str(n), (sx, T), xytext=({1: (-16, -12), 2: (-18, 2), 3: (-18, 2), 4: (4, 6), 5: (6, 2), 6: (6, -4)}[n]), textcoords='offset points', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(pt[3][0] + .04, 800, L('buồng đốt', 'burner'), fontsize=12, color=ORG); ax.text(pt[5][0] - .02, 1230, L('tuabin', 'turbine'), fontsize=12, color=GRY, ha='right'); ax.text(pt[2][0] + .02, 360, L('máy nén', 'compressor'), fontsize=12, color=GRY)
    ax.text(pt[6][0] - .02, 830, L('vòi phun', 'nozzle'), fontsize=12, color=GRY, ha='right')
    ax.set_xlabel(L('entropi riêng s', 'specific entropy s')); ax.set_ylabel(L('nhiệt độ T [K]', 'temperature T [K]')); ax.set_xticks([]); ax.grid(alpha=.25); ax.set_ylim(150, 1500)
    save(fig, 'fig_jet_ts', lang)

if __name__ == '__main__':
    for lang in ('vi', 'en'):
        cycles('otto', lang); cycles('diesel', lang); brayton_fig(lang); eta_otto_diesel(lang); brayton_work(lang); regen(lang); multistage(lang); jet_ts(lang)
    print('figures written to', OUT, sorted(os.listdir(OUT)))
