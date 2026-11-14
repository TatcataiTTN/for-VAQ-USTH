"""m03 figures (matplotlib, dpi 100, figsize = displayed px / 100, text >= 13 pt), Vietnamese and English versions -> assets/figs/m03/*.png
R-134a curves are computed with CoolProp (ASHRAE reference state: h = s = 0 for saturated liquid at -40 C, as in Cengel's tables); the cycle state values printed on the
figures come from the table route (props library: A-11/A-12/A-13), the same numbers as the worked examples. Air curves use constant cp = 1.005, R = 0.287.
Nothing is traced or read from the slide charts; the cooling-pack figure only draws numbers that the slides (Ch.3 p.32-36) print, or sums of them (hatched).
Run: .venv/bin/python -I build/gen/figs_m03.py"""
import os, sys, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP
CP.set_reference_state('R134a', 'ASHRAE')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
from m03_common import vcrc_ideal, gas_simple, carnot_R, sT, sP, shP, h_at_s, c2k, CP_AIR, R_AIR
OUT = os.path.join(ROOT, 'assets', 'figs', 'm03'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14, 'axes.titlesize': 14, 'axes.labelsize': 14, 'legend.fontsize': 13, 'xtick.labelsize': 13, 'ytick.labelsize': 13, 'axes.grid': False})
NAVY, RED, GRN, ORG, GRY, PUR, BLU = '#1f3a5f', '#c0392b', '#2e8b57', '#d98324', '#7f8c8d', '#7d3c98', '#2f6db5'
F = 'R134a'
def save(fig, name, lang): fig.savefig(os.path.join(OUT, f'{name}_{lang}.png'), dpi=100); plt.close(fig)
Ps = lambda P, Q: CP.PropsSI('S', 'P', P, 'Q', Q, F) / 1e3
Hs = lambda P, Q: CP.PropsSI('H', 'P', P, 'Q', Q, F) / 1e3
Hps = lambda P, s: CP.PropsSI('H', 'P', P, 'S', s * 1e3, F) / 1e3
Tps = lambda P, s: CP.PropsSI('T', 'P', P, 'S', s * 1e3, F) - 273.15
Tsat = lambda P: CP.PropsSI('T', 'P', P, 'Q', 0, F) - 273.15
PT = lambda T_C: CP.PropsSI('P', 'T', T_C + 273.15, 'Q', 0, F)
Tcrit = CP.PropsSI('Tcrit', F) - 273.15
def dome_T(n=140):
    T = np.linspace(-45, Tcrit - 0.05, n); sf = [CP.PropsSI('S', 'T', t + 273.15, 'Q', 0, F) / 1e3 for t in T]; sg = [CP.PropsSI('S', 'T', t + 273.15, 'Q', 1, F) / 1e3 for t in T]
    return T, np.array(sf), np.array(sg)
def dome_p(n=140):
    T = np.linspace(-45, Tcrit - 0.05, n); P = np.array([CP.PropsSI('P', 'T', t + 273.15, 'Q', 0, F) for t in T])
    hf = np.array([CP.PropsSI('H', 'T', t + 273.15, 'Q', 0, F) / 1e3 for t in T]); hg = np.array([CP.PropsSI('H', 'T', t + 273.15, 'Q', 1, F) / 1e3 for t in T])
    return P, hf, hg
def draw_Ts_dome(ax):
    T, sf, sg = dome_T(); ax.plot(sf, T, color=GRY, lw=1.8); ax.plot(sg, T, color=GRY, lw=1.8)
    ax.set_xlabel('s [kJ/(kg·K)]'); ax.set_ylabel('T [°C]')
def draw_logph_dome(ax, xlines=False):
    P, hf, hg = dome_p(); ax.plot(hf, P / 1e3, color=GRY, lw=1.8); ax.plot(hg, P / 1e3, color=GRY, lw=1.8); ax.set_yscale('log')
    ax.set_xlabel('h [kJ/kg]'); ax.set_ylabel('p [kPa]')
    ax.set_yticks([100, 200, 500, 1000, 2000]); ax.set_yticklabels(['100', '200', '500', '1000', '2000']); ax.minorticks_off()
    return P, hf, hg
def lab(ax, x, y, t, dx=6, dy=6, c=NAVY, fs=15, ha='left'): ax.annotate(t, (x, y), xytext=(dx, dy), textcoords='offset points', fontsize=fs, fontweight='bold', color=c, ha=ha)
def pts(ax, xs, ys): ax.scatter(xs, ys, color=NAVY, zorder=6, s=34)
def arrow(ax, x0, y0, x1, y1, c, lw=1.8): ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='-|>', color=c, lw=lw))
def isentrope_logph(Pa, Pb, s, n=60): P = np.geomspace(Pa, Pb, n); return np.array([Hps(p, s) for p in P]), P / 1e3

# ================================================================= 1. wet-vapour area on log p-h (slide p.8), regions + isotherms 0 and 20 C + x lines
def fig_dome(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    fig, ax = plt.subplots(figsize=(7.2, 4.4)); fig.subplots_adjust(left=.11, right=.98, bottom=.14, top=.93)
    P, hf, hg = draw_logph_dome(ax)
    ax.fill_betweenx(P / 1e3, hf, hg, color='#cfe3f7', zorder=0)
    ax.fill_betweenx(P / 1e3, hg, 420, color='#f7d6d3', zorder=0); ax.fill_betweenx(P / 1e3, 0, hf, color='#e6e6e6', zorder=0)
    ax.set_xlim(0, 400); ax.set_ylim(60, 5000)
    for x in (0.2, 0.4, 0.6, 0.8):
        h = hf + x * (hg - hf); ax.plot(h, P / 1e3, color=GRY, lw=0.9, ls='--'); k = np.argmin(abs(P / 1e3 - 90)); ax.annotate(f'x={x:g}'.replace('.', ',') if lang == 'vi' else f'x={x:g}', (h[k], 90), fontsize=13, color=GRY, rotation=72, ha='center', va='bottom')
    for T_C, c in ((0, BLU), (20, RED)):
        Psat = CP.PropsSI('P', 'T', T_C + 273.15, 'Q', 0, F); h1 = Hs(Psat, 0); h2 = Hs(Psat, 1)
        Pl = np.geomspace(Psat * 1.001, 4500e3, 30); hl = [CP.PropsSI('H', 'T', T_C + 273.15, 'P', p, F) / 1e3 for p in Pl]
        Pv = np.geomspace(Psat * 0.999, 70e3, 30); hv = [CP.PropsSI('H', 'T', T_C + 273.15, 'P', p, F) / 1e3 for p in Pv]
        ax.plot(hl, Pl / 1e3, color=c, lw=2); ax.plot([h1, h2], [Psat / 1e3] * 2, color=c, lw=2); ax.plot(hv, Pv / 1e3, color=c, lw=2)
        ax.annotate(f'T = {T_C + 273} K', ((h1 + h2) / 2, Psat / 1e3), xytext=(0, 5), textcoords='offset points', fontsize=13, color=c, fontweight='bold', ha='center')
    ax.text(8, 1500, L('Lỏng', 'Liquid'), fontsize=14, fontweight='bold', color='#555'); ax.text(150, 1250, L('Hơi ẩm', 'Wet vapour'), fontsize=14, fontweight='bold', color=BLU)
    ax.text(330, 900, L('Hơi', 'Vapour'), fontsize=14, fontweight='bold', color=RED)
    ax.annotate(L('x = 0 (đường sôi)', 'x = 0 (boiling line)'), (hf[110], P[110] / 1e3), xytext=(6, 3300), textcoords='data', fontsize=13, ha='left', va='center', bbox=dict(fc='white', ec='none', alpha=.85, pad=1.5), arrowprops=dict(arrowstyle='-', color=GRY))
    ax.annotate(L('x = 1 (hơi bão hòa)', 'x = 1 (sat. vapour)'), (hg[110], P[110] / 1e3), xytext=(284, 3300), textcoords='data', fontsize=13, ha='left', va='center', bbox=dict(fc='white', ec='none', alpha=.85, pad=1.5), arrowprops=dict(arrowstyle='-', color=GRY))
    ax.set_title(L('R-134a trên log p–h (tự vẽ lại bằng CoolProp)', 'R-134a on log p–h (redrawn with CoolProp)'), loc='left', fontsize=13)
    save(fig, 'fig_dome', lang)

# ================================================================= 2. reversed Carnot cycle inside the dome (slides p.11-14; Cengel Prob. 11-2 numbers)
def fig_carnot(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    TH = 30.0; PL = 160e3; TL = Tsat(PL); PH = PT(TH); sf_H, sg_H = Ps(PH, 0), Ps(PH, 1)
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.0, 3.9)); fig.subplots_adjust(left=.085, right=.99, bottom=.16, top=.9, wspace=.3)
    draw_Ts_dome(a); a.set_xlim(0.2, 1.3); a.set_ylim(-45, 105)
    s_ = {1: sf_H, 2: sg_H, 3: sg_H, 4: sf_H}; T_ = {1: TL, 2: TL, 3: TH, 4: TH}
    cyc = [(1, 2), (2, 3), (3, 4), (4, 1)]
    for i, j in cyc: a.plot([s_[i], s_[j]], [T_[i], T_[j]], color=RED, lw=2.6)
    pts(a, [s_[k] for k in s_], [T_[k] for k in s_]); lab(a, s_[1], T_[1], '1', -16, -16); lab(a, s_[2], T_[2], '2', 4, -16); lab(a, s_[3], T_[3], '3', 4, 4); lab(a, s_[4], T_[4], '4', -16, 4)
    a.text((sf_H + sg_H) / 2, TL - 10, r'$Q_L$', color=BLU, fontsize=14, fontweight='bold', ha='center'); a.text((sf_H + sg_H) / 2, TH + 4, r'$Q_H$', color=ORG, fontsize=14, fontweight='bold', ha='center')
    a.set_title(L('T–s: Carnot đảo ngược', 'T–s: reversed Carnot'), loc='left', fontsize=13)
    P_, hf, hg = draw_logph_dome(b); b.set_xlim(40, 330); b.set_ylim(80, 2500)
    h_ = {1: Hps(PL, sf_H), 2: Hps(PL, sg_H), 3: Hs(PH, 1), 4: Hs(PH, 0)}; p_ = {1: PL / 1e3, 2: PL / 1e3, 3: PH / 1e3, 4: PH / 1e3}
    b.plot([h_[1], h_[2]], [p_[1]] * 2, color=RED, lw=2.6); b.plot([h_[3], h_[4]], [p_[3]] * 2, color=RED, lw=2.6)
    hh, pp = isentrope_logph(PL, PH, sg_H); b.plot(hh, pp, color=RED, lw=2.6); hh, pp = isentrope_logph(PL, PH, sf_H); b.plot(hh, pp, color=RED, lw=2.6)
    pts(b, [h_[k] for k in h_], [p_[k] for k in h_]); lab(b, h_[1], p_[1], '1', -14, -16); lab(b, h_[2], p_[2], '2', 4, -16); lab(b, h_[3], p_[3], '3', 4, 4); lab(b, h_[4], p_[4], '4', -16, 4)
    b.set_title(L('log p–h: 2→3, 4→1 là đường cong', 'log p–h: 2→3, 4→1 are curves'), loc='left', fontsize=13)
    save(fig, 'fig_carnot', lang)

# ================================================================= 3. ideal vapour-compression cycle, Tutorials I numbers (0.14 - 0.8 MPa)
def fig_vcrc(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    c = vcrc_ideal(140, 800); PL, PH = 140e3, 800e3; s1 = c['s1']; sf3 = sP(800, 'sf')
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.0, 3.9)); fig.subplots_adjust(left=.085, right=.99, bottom=.16, top=.9, wspace=.3)
    draw_Ts_dome(a); a.set_xlim(0.2, 1.3); a.set_ylim(-45, 105)
    T1 = c['Tl']; T2 = c['T2']; T3 = c['Th']; T4 = c['Tl']; s4 = Ps(PL, 0) + c['x4'] * (Ps(PL, 1) - Ps(PL, 0)); s4s = sf3
    a.plot([s1, s1], [T1, T2], color=RED, lw=2.6)                                                              # 1-2 isentropic
    Ts = np.linspace(T2, T3 + 0.05, 40); a.plot([CP.PropsSI('S', 'P', PH, 'T', t + 273.15, F) / 1e3 for t in Ts], Ts, color=RED, lw=2.6)   # 2 -> sat. vapour at 0.8 MPa (isobar)
    a.plot([Ps(PH, 1), sf3], [T3, T3], color=RED, lw=2.6)                                                       # condensation
    a.plot([sf3, s4], [T3, T4], color=RED, lw=2.0, ls='--')                                                     # throttling (not a path)
    a.plot([s4, s1], [T4, T1], color=RED, lw=2.6)
    a.plot([sf3, sf3], [T3, T4], color=GRY, lw=1.2, ls=':')
    P_ = {1: (s1, T1), 2: (s1, T2), 3: (sf3, T3), 4: (s4, T4), '4s': (s4s, T4)}; pts(a, [v[0] for v in P_.values()], [v[1] for v in P_.values()])
    lab(a, *P_[1], '1', 4, 4); lab(a, *P_[2], '2', 4, 2); lab(a, *P_[3], '3', -16, 2); lab(a, *P_[4], '4', 0, -18); lab(a, *P_['4s'], '4s', -22, -18)
    a.text(0.55, 60, r'$Q_H$', color=ORG, fontsize=14, fontweight='bold'); a.text(0.9, -38, r'$Q_L$', color=BLU, fontsize=14, fontweight='bold')
    a.set_title(L('T–s (Tutorials I: 0,14 – 0,8 MPa)', 'T–s (Tutorials I: 0.14 – 0.8 MPa)'), loc='left', fontsize=13)
    P2, hf, hg = draw_logph_dome(b); b.set_xlim(40, 330); b.set_ylim(80, 2500)
    h = {1: c['h1'], 2: c['h2'], 3: c['h3'], 4: c['h4']}; p = {1: 140, 2: 800, 3: 800, 4: 140}
    hh, pp = isentrope_logph(PL, PH, s1); b.plot(hh, pp, color=RED, lw=2.6)
    b.plot([h[2], h[3]], [800, 800], color=RED, lw=2.6); b.plot([h[3], h[4]], [800, 140], color=RED, lw=2.6); b.plot([h[4], h[1]], [140, 140], color=RED, lw=2.6)
    pts(b, [h[k] for k in h], [p[k] for k in h]); lab(b, h[1], 140, '1', 4, -16); lab(b, h[2], 800, '2', 4, 2); lab(b, h[3], 800, '3', -16, 4); lab(b, h[4], 140, '4', -16, -16)
    b.text((h[3] + h[2]) / 2 - 30, 800 * 1.12, r'$Q_H$', color=ORG, fontsize=14, fontweight='bold'); b.text((h[4] + h[1]) / 2 - 14, 140 * 0.76, r'$Q_L$', color=BLU, fontsize=14, fontweight='bold')
    b.text(h[1] + 28, 330, r'$W_{in}$', color=GRN, fontsize=14, fontweight='bold')
    b.set_title(L('log p–h: 3 đường thẳng, 1 cong', 'log p–h: 3 straight lines + 1 curve'), loc='left', fontsize=13)
    save(fig, 'fig_vcrc', lang)

# ================================================================= 4. real cycle (Cengel Example 11-2 states) against the ideal one
def fig_real(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    c = vcrc_ideal(140, 800)
    h1 = shP(0.14, -10, 'h'); s1r = shP(0.14, -10, 's'); h2 = shP(0.8, 50, 'h'); s2 = shP(0.8, 50, 's'); h3 = sT(26, 'hf'); s3 = sT(26, 'sf'); h2s, T2s = h_at_s(0.8, s1r)
    st = {"1'": (s1r, -10.0, h1, 140), "2'": (s2, 50.0, h2, 800), "3'": (s3, 26.0, h3, 720), "4'": (None, None, h3, 150)}
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.0, 3.9)); fig.subplots_adjust(left=.085, right=.99, bottom=.16, top=.9, wspace=.3)
    draw_Ts_dome(a); a.set_xlim(0.2, 1.3); a.set_ylim(-45, 105)
    s4 = Ps(150e3, 0) + (h3 - Hs(150e3, 0)) / (Hs(150e3, 1) - Hs(150e3, 0)) * (Ps(150e3, 1) - Ps(150e3, 0)); T4 = Tsat(150e3)
    st["4'"] = (s4, T4, h3, 150)
    xs = [st[k][0] for k in ("1'", "2'", "3'", "4'")] + [st["1'"][0]]; ys = [st[k][1] for k in ("1'", "2'", "3'", "4'")] + [st["1'"][1]]
    a.plot(xs, ys, color=RED, lw=2.0, ls='-'); pts(a, xs[:-1], ys[:-1]); a.scatter([s1r], [T2s], color=GRN, s=34, zorder=6)
    lab(a, s1r, -10, "1'", 4, -18); lab(a, s2, 50, "2'", 4, 2); lab(a, s3, 26, "3'", -22, 2); lab(a, s4, T4, "4'", -4, -18); lab(a, s1r, T2s, "2s'", -30, -4, c=GRN)
    a.set_title(L('T–s: Ví dụ 11–2 (đường nối chỉ để nhìn)', 'T–s: Example 11–2 (joining lines for the eye)'), loc='left', fontsize=13)
    P2, hf, hg = draw_logph_dome(b); b.set_xlim(40, 330); b.set_ylim(80, 2500)
    hh, pp = isentrope_logph(140e3, 800e3, c['s1']); b.plot(hh, pp, color=GRY, lw=1.4)
    b.plot([c['h2'], c['h3'], c['h3'], c['h1'], c['h2']][:4], [800, 800, 140, 140], color=GRY, lw=1.4)
    seq = ["1'", "2'", "3'", "4'", "1'"]; hx = [st[k][2] for k in seq]; py = [st[k][3] for k in seq]
    b.plot(hx, py, color=RED, lw=2.0); pts(b, hx[:-1], py[:-1]); b.scatter([h2s], [800], color=GRN, s=34, zorder=6)
    lab(b, h1, 140, "1'", 4, -18); lab(b, h2, 800, "2'", 4, 4); lab(b, h3, 720, "3'", -24, -6); lab(b, h3, 150, "4'", -26, 4); lab(b, h2s, 800, "2s'", -36, 6, c=GRN)
    b.set_title(L('log p–h: xám = lý tưởng, đỏ = thực', 'log p–h: grey = ideal, red = actual'), loc='left', fontsize=13)
    save(fig, 'fig_real', lang)

# ================================================================= 5. gas refrigeration (reversed Brayton) cycle, Cengel Prob. 11-97 numbers
def fig_gas(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    T1, T3, rp = c2k(30.0), c2k(70.0), 2.5; g = gas_simple(T1, T3, rp); T2, T4 = g['T2'], g['T4']
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.0, 3.9)); fig.subplots_adjust(left=.095, right=.9, bottom=.16, top=.9, wspace=.52)
    s = lambda T, P: CP_AIR * np.log(np.asarray(T) / T1) - R_AIR * math.log(P / 100.0)               # relative to state 1 (100 kPa, T1)
    Tl = np.linspace(T4, T1, 40); a.plot(s(Tl, 100.0), Tl - 273.15, color=BLU, lw=2.6)       # 4-1 absorption at 100 kPa
    Tl = np.linspace(T1, T2, 40); a.plot([s(T1, 100.0)] * 40, Tl - 273.15, color=RED, lw=2.6)  # 1-2 isentropic
    Tl = np.linspace(T3, T2, 40); a.plot(s(Tl, 250.0), Tl - 273.15, color=ORG, lw=2.6)       # 2-3 cooling at 250 kPa
    Tl = np.linspace(T4, T3, 40); a.plot([s(T4, 100.0)] * 40, Tl - 273.15, color=RED, lw=2.6)  # 3-4 isentropic
    P_ = {1: (s(T1, 100.0), T1), 2: (s(T1, 100.0), T2), 3: (s(T3, 250.0), T3), 4: (s(T4, 100.0), T4)}
    pts(a, [v[0] for v in P_.values()], [v[1] - 273.15 for v in P_.values()])
    lab(a, P_[1][0], P_[1][1] - 273.15, '1', 6, -14); lab(a, P_[2][0], P_[2][1] - 273.15, '2', 6, 2); lab(a, P_[3][0], P_[3][1] - 273.15, '3', -14, 2); lab(a, P_[4][0], P_[4][1] - 273.15, '4', -16, -14)
    a.text(s(T3, 250.0) + 0.02, 100, 'p = 250 kPa', color=ORG, fontsize=13, fontweight='bold'); a.text(s(T4, 100.0) + 0.012, 8, 'p = 100 kPa', color=BLU, fontsize=13, fontweight='bold')
    a.set_xlabel(L('s − s₁ [kJ/(kg·K)]', 's − s₁ [kJ/(kg·K)]')); a.set_ylabel('T [°C]'); a.set_title(L('T–s khí lạnh (Prob. 11–97)', 'T–s gas refrigeration (Prob. 11–97)'), loc='left', fontsize=13)
    r = np.linspace(1.3, 6.0, 80); x = r ** (0.4 / 1.4); cop = 1 / (x - 1); T4v = T3 / x - 273.15
    b.plot(r, cop, color=GRN, lw=2.6); b.set_xlabel(L('tỉ số áp r_p', 'pressure ratio r_p')); b.set_ylabel('COP', color=GRN); b.set_ylim(0, 8); b.tick_params(axis='y', colors=GRN)
    b2 = b.twinx(); b2.plot(r, T4v, color=PUR, lw=2.6, ls='--'); b2.set_ylabel(L('T₄ [°C]', 'T₄ [°C]'), color=PUR); b2.tick_params(axis='y', colors=PUR); b2.set_ylim(-80, 60)
    b.scatter([rp], [g['cop']], color=NAVY, zorder=6, s=34); b.annotate(f'r_p = 2,5' if lang == 'vi' else 'r_p = 2.5', (rp, g['cop']), xytext=(10, -22), textcoords='offset points', fontsize=13, fontweight='bold', color=NAVY)
    b.set_title(L('COP và T₄ theo r_p (T₃ = 343 K)', 'COP and T₄ versus r_p (T₃ = 343 K)'), loc='left', fontsize=13)
    save(fig, 'fig_gas', lang)

# ================================================================= 6. COP of the ideal cycle against evaporating temperature, and the reversed Carnot COP
def fig_cop(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    TH = 40.0; Tl = np.linspace(-30, 10, 41); cop = []; car = []
    for t in Tl:
        Pl = PT(t); Ph = PT(TH); h1 = Hs(Pl, 1); s1 = Ps(Pl, 1); h2 = Hps(Ph, s1); h3 = Hs(Ph, 0); cop.append((h1 - h3) / (h2 - h1)); car.append(carnot_R(t + 273.15, TH + 273.15))
    fig, ax = plt.subplots(figsize=(7.2, 4.2)); fig.subplots_adjust(left=.1, right=.98, bottom=.15, top=.92)
    ax.plot(Tl, car, color=NAVY, lw=2.6, label=L('Carnot đảo ngược', 'reversed Carnot')); ax.plot(Tl, cop, color=RED, lw=2.6, label=L('nén hơi lý tưởng R-134a', 'ideal vapour-compression R-134a'))
    ax.set_xlabel(L('nhiệt độ bay hơi T_L [°C] (T_H = 40 °C)', 'evaporating temperature T_L [°C] (T_H = 40 °C)')); ax.set_ylabel('COP'); ax.set_ylim(0, 14); ax.legend(loc='upper left')
    i = int(np.argmin(abs(Tl + 10))); ax.annotate(f'{cop[i]:.2f}'.replace('.', ',') if lang == 'vi' else f'{cop[i]:.2f}', (Tl[i], cop[i]), xytext=(6, -16), textcoords='offset points', fontsize=13, color=RED, fontweight='bold')
    ax.annotate(f'{car[i]:.2f}'.replace('.', ',') if lang == 'vi' else f'{car[i]:.2f}', (Tl[i], car[i]), xytext=(6, 6), textcoords='offset points', fontsize=13, color=NAVY, fontweight='bold')
    ax.set_title(L('COP tăng khi T_L tăng; chu trình thực tế luôn thấp hơn Carnot', 'COP rises with T_L; the real-fluid cycle is always below Carnot'), loc='left', fontsize=13)
    save(fig, 'fig_cop', lang)

# ================================================================= 7. cooling-pack temperature trace: ONLY numbers printed on Slide Ch.3 p.32-36 (solid) or their sums (hatched)
def fig_pack(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    fig, ax = plt.subplots(figsize=(9.0, 3.9)); fig.subplots_adjust(left=.085, right=.99, bottom=.3, top=.9)
    names = [L('khí xả\nvào pack\n(tr.32)', 'bleed air\nentering\n(p.32)'), L('sau bộ trao\nđổi nhiệt\nsơ cấp', 'after primary\nheat exch.'), L('sau máy nén\ncủa ACM', 'after ACM\ncompressor'), L('sau bộ trao\nđổi nhiệt\nthứ cấp', 'after secondary\nheat exch.'), L('vào tuabin\ncủa ACM\n(tr.34)', 'ACM turbine\ninlet\n(p.34)'), L('ra tuabin\ncủa ACM\n(tr.35)', 'ACM turbine\noutlet\n(p.35)')]
    lo = [150, 50, 80, 10, 10, -10]; hi = [150, 50, 90, 30, 20, -10]; stated = [True, False, False, False, True, True]
    for i, (a_, b_, s_) in enumerate(zip(lo, hi, stated)):
        h = max(b_ - a_, 3.0); y0 = a_ if b_ > a_ else a_ - 1.5
        ax.bar(i, h, bottom=y0, width=0.5, color=BLU if s_ else 'white', edgecolor=BLU, hatch=None if s_ else '///', lw=2)
        txt = f'{a_}' if a_ == b_ else f'{a_}–{b_}'
        ax.text(i, b_ + 6, txt + ' °C', ha='center', fontsize=13, fontweight='bold', color=NAVY, bbox=dict(fc='white', ec='none', pad=1.0))
    ax.annotate('', xy=(0.8, 64), xytext=(0.25, 140), arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.6)); ax.text(0.5, 122, L('−100 (tr.32)', '−100 (p.32)'), color=RED, fontsize=13, fontweight='bold')
    ax.annotate('', xy=(1.78, 80), xytext=(1.25, 54), arrowprops=dict(arrowstyle='-|>', color=ORG, lw=1.6)); ax.text(1.1, 38, L('+30…40 (tr.33)', '+30…40 (p.33)'), color=ORG, fontsize=13, fontweight='bold')
    ax.annotate('', xy=(2.8, 38), xytext=(2.25, 88), arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.6)); ax.text(2.5, 78, L('−60…70 (tr.33)', '−60…70 (p.33)'), color=RED, fontsize=13, fontweight='bold')
    ax.annotate('', xy=(4.75, -4), xytext=(4.25, 14), arrowprops=dict(arrowstyle='-|>', color=PUR, lw=1.6)); ax.text(4.35, 30, L('giãn nở', 'expansion'), color=PUR, fontsize=13, fontweight='bold')
    ax.set_xticks(range(6)); ax.set_xticklabels(names, fontsize=13); ax.set_ylabel('T [°C]'); ax.set_ylim(-30, 175); ax.axhline(0, color=GRY, lw=0.8)
    ax.set_title(L('Đặc: số in trên slide · gạch chéo: tổng/hiệu suy ra từ số slide (minh hoạ)', 'Solid: printed on the slides · hatched: sums/differences of slide numbers (illustrative)'), loc='left', fontsize=13)
    save(fig, 'fig_pack', lang)

if __name__ == '__main__':
    for lang in ('vi', 'en'):
        fig_dome(lang); fig_carnot(lang); fig_vcrc(lang); fig_real(lang); fig_gas(lang); fig_cop(lang); fig_pack(lang)
    print('figures written to', OUT)
