"""m05 figures (matplotlib, dpi 100, figsize = displayed px / 100, text >= 13 pt), Vietnamese and English versions -> assets/figs/m05/*.png
Every curve is computed from the isentropic relations (slide equations (9)-(17)); the printed rows of Table A-32 (data/props/A32.json) and the lecturer's numeric examples
(Ch.5 p.12, 22, 38, 54-55, 57-59) are drawn as marked points.  Nothing is traced from a slide chart.  The C-D nozzle figure draws only the ISENTROPIC branches; the branch with a
normal shock inside the nozzle is labelled (Added from the book, not computed here).  Run: python3 -I build/gen/figs_m05.py"""
import os, sys, json, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
from m05_common import *
OUT = os.path.join(ROOT, 'assets', 'figs', 'm05'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14, 'axes.titlesize': 14, 'axes.labelsize': 14, 'legend.fontsize': 13, 'xtick.labelsize': 13, 'ytick.labelsize': 13, 'axes.grid': False})
NAVY, RED, GRN, ORG, GRY, PUR, BLU = '#1f3a5f', '#c0392b', '#2e8b57', '#d98324', '#7f8c8d', '#7d3c98', '#2f6db5'
A32 = json.load(open(os.path.join(ROOT, 'data', 'props', 'A32.json'), encoding='utf-8')); ROWS = [r for r in A32['rows'] if r[0] is not None and r[0] > 0]
def save(fig, name, lang): fig.savefig(os.path.join(OUT, f'{name}_{lang}.png'), dpi=100); plt.close(fig)
def T(lang, vi, en): return vi if lang == 'vi' else en
def dec(lang, x, nd=1):
    s = f'{x:.{nd}f}'; return s.replace('.', ',') if lang == 'vi' else s
k = 1.4

def fig_ratios(lang):
    fig, ax = plt.subplots(figsize=(7.6, 4.6)); Ma = np.linspace(0, 5, 300)
    for f, c, lab, col in ((TT0, NAVY, 'T/T$_0$', 5), (PP0, RED, 'P/P$_0$', 3), (rr0, GRN, r'$\rho/\rho_0$', 4)):
        ax.plot(Ma, [f(m, k) for m in Ma], color=c, lw=2.3, label=lab)
        ax.plot([r[0] for r in ROWS], [r[col] for r in ROWS], 'o', color=c, ms=4.5, mfc='white', mew=1.4)
    ax.axvline(1.0, color=GRY, lw=1, ls='--'); ax.text(1.04, 0.93, T(lang, 'Ma = 1: P/P$_0$ = 0,5283', 'Ma = 1: P/P$_0$ = 0.5283'), color=GRY, fontsize=12)
    ax.annotate(T(lang, 'hàng in A-32\n(vòng tròn rỗng)', 'printed A-32 rows\n(open circles)'), (3.0, 0.3571), xytext=(3.2, 0.62), arrowprops=dict(arrowstyle='->', color=GRY), fontsize=12, color=GRY)
    ax.set_xlabel('Ma'); ax.set_ylabel(T(lang, 'tỉ số tĩnh / hãm', 'static / stagnation ratio')); ax.set_xlim(0, 5); ax.set_ylim(0, 1.02)
    ax.set_title(T(lang, 'T/T₀, P/P₀, ρ/ρ₀ giảm đơn điệu theo Ma (k = 1,4)', 'T/T₀, P/P₀, ρ/ρ₀ fall monotonically with Ma (k = 1.4)'), fontsize=13); ax.legend(loc='upper right', frameon=False, ncol=3, bbox_to_anchor=(1.0, 0.85)); fig.tight_layout(); save(fig, 'fig_ratios', lang)

def fig_area(lang):
    fig, ax = plt.subplots(figsize=(7.6, 4.6)); sub = np.linspace(0.1, 1.0, 200); sup = np.linspace(1.0, 4.0, 200)
    ax.plot(sub, [AAs(m, k) for m in sub], color=BLU, lw=2.3, label=T(lang, 'nhánh cận âm', 'subsonic branch')); ax.plot(sup, [AAs(m, k) for m in sup], color=RED, lw=2.3, label=T(lang, 'nhánh siêu âm', 'supersonic branch'))
    ax.plot([r[0] for r in ROWS if r[0] <= 4], [r[2] for r in ROWS if r[0] <= 4], 'o', color=GRY, ms=4.5, mfc='white', mew=1.3, label=T(lang, 'hàng in A-32', 'printed A-32 rows'))
    pts = [(0.3, AAs(0.3, k), 'Ma₁ = 0,3; 2,0351', (0.38, 3.9)), (Ma_of_AA(0.8 * AAs(0.3, k), k), 0.8 * AAs(0.3, k), 'Ma₂ = 0,3887; 1,6281', (0.5, 2.5)), (2.0, AAs(2.0, k), 'Ex 17-7: Ma = 2; 1,6875', (2.3, 3.2))]
    for x, y, lab, xy in pts:
        ax.plot([x], [y], 's', color=ORG, ms=8, zorder=5); ax.annotate(lab if lang == 'vi' else lab.replace(',', '.'), (x, y), xytext=xy, fontsize=12, color=ORG, arrowprops=dict(arrowstyle='->', color=ORG))
    ax.axhline(1.0, color=GRY, lw=1, ls='--'); ax.text(3.0, 1.12, T(lang, 'cổ họng: A/A* = 1', 'throat: A/A* = 1'), color=GRY, fontsize=12)
    ax.set_xlabel('Ma'); ax.set_ylabel('A/A*'); ax.set_xlim(0, 4); ax.set_ylim(0.8, 6)
    ax.set_title(T(lang, 'Mỗi A/A* > 1 có hai số Mach: một cận âm, một siêu âm', 'Every A/A* > 1 has two Mach numbers: one subsonic, one supersonic'), fontsize=13); ax.legend(loc='upper right', frameon=False); fig.tight_layout(); save(fig, 'fig_area', lang)

def fig_conv(lang):
    """converging nozzle: mass flow and exit pressure against P_b/P_0 (air); slide Ex 17-5 points."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.6, 6.2), sharex=True, gridspec_kw=dict(hspace=0.12)); pc = crit(k)['PP']; pb = np.linspace(0.0, 1.0, 400)
    P0i, T0i, A = 1045.6026, 884.1940, 50e-4; mmax = mdot_choked(A, P0i, T0i, k, 0.287)
    m = [conv_nozzle(max(b, 1e-6) * P0i, P0i, T0i, k, 0.287, A)['mdot'] / mmax for b in pb]; pe = [conv_nozzle(max(b, 1e-6) * P0i, P0i, T0i, k, 0.287, A)['Pe'] / P0i for b in pb]
    a1.plot(pb, m, color=NAVY, lw=2.4); a1.axvline(pc, color=GRY, ls='--', lw=1); a1.set_ylabel(T(lang, 'ṁ/ṁ$_{max}$', 'ṁ/ṁ$_{max}$')); a1.set_ylim(0, 1.12)
    for pbp, lab in ((0.7 / 1.045, '(a) 6,77'), (0.4 / 1.045, '(b) 7,10')):
        r = conv_nozzle(pbp * P0i, P0i, T0i, k, 0.287, A); a1.plot([pbp], [r['mdot'] / mmax], 'o', color=RED, ms=9, zorder=5)
        a1.annotate(('Ex 17-5 ' + lab + ' kg/s') if lang == 'vi' else ('Ex 17-5 ' + lab.replace(',', '.') + ' kg/s'), (pbp, r['mdot'] / mmax), xytext=(pbp - 0.33 if pbp > 0.6 else pbp - 0.15, 0.55 if pbp > 0.6 else 0.35), fontsize=12, color=RED, arrowprops=dict(arrowstyle='->', color=RED))
    a1.text(0.02, 1.03, T(lang, 'nghẹt: ṁ = ṁ$_{max}$', 'choked: ṁ = ṁ$_{max}$'), fontsize=12, color=NAVY); a1.text(pc + 0.01, 0.1, 'P*/P$_0$ = ' + dec(lang, pc, 4), fontsize=12, color=GRY)
    a2.plot(pb, pe, color=GRN, lw=2.4); a2.axvline(pc, color=GRY, ls='--', lw=1); a2.plot([0, 1], [0, 1], color=GRY, lw=1, ls=':'); a2.set_ylabel('P$_e$/P$_0$'); a2.set_xlabel('P$_b$/P$_0$'); a2.set_xlim(0, 1); a2.set_ylim(0, 1.05)
    a2.text(0.02, pc + 0.04, T(lang, 'P$_e$ = P* khi P$_b$ < P* (dòng nghẹt)', 'P$_e$ = P* when P$_b$ < P* (choked)'), fontsize=12, color=GRN); a2.text(0.62, 0.45, T(lang, 'P$_e$ = P$_b$\n(chấm: đường thẳng)', 'P$_e$ = P$_b$\n(dotted line)'), fontsize=12, color=GRY)
    a1.set_title(T(lang, 'Vòi hội tụ: giảm áp suất ngược tới P* làm ṁ tăng, rồi ṁ không đổi', 'Converging nozzle: lowering back pressure to P* raises ṁ, then ṁ stays constant'), fontsize=12.5); fig.subplots_adjust(left=0.12, right=0.97, top=0.93, bottom=0.09); save(fig, 'fig_conv', lang)

def fig_cd(lang):
    """converging-diverging nozzle (A_inlet/A* = 3, A_e/A* = 1.6875): isentropic pressure distributions along the nozzle and the exit-plane regimes; the shock branch is only labelled."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 4.6), gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.34)); xt = 0.4; Ae = AAs(2.0, k); x = np.linspace(0, 1, 300)
    area = lambda xx: np.where(xx <= xt, 1.0 + (3.0 - 1.0) * ((xt - xx) / xt) ** 2, 1.0 + (Ae - 1.0) * ((xx - xt) / (1 - xt)) ** 2)
    def curve(Astar_ratio, sup):
        out = []
        for xx, aa in zip(x, area(x)):
            r = aa / Astar_ratio
            if r < 1: r = 1.0
            M = Ma_of_AA(r, k, 'sup' if (sup and xx > xt) else 'sub'); out.append(PP0(M, k))
        return out
    a1.plot(x, curve(1.0, True), color=RED, lw=2.3, label=T(lang, 'thiết kế: cửa ra siêu âm', 'design: supersonic exit'))
    a1.plot(x, curve(1.0, False), color=BLU, lw=2.3, label=T(lang, 'nghẹt, cửa ra cận âm', 'choked, subsonic exit'))
    a1.plot(x, curve(1.0 / AAs(0.6, k), False), color=GRN, lw=2.3, ls='--', label=T(lang, 'không nghẹt (Ma$_t$ = 0,6)', 'not choked (Ma$_t$ = 0.6)'))
    a1.axvline(xt, color=GRY, ls=':', lw=1); a1.text(xt + 0.01, 1.01, T(lang, 'cổ họng', 'throat'), fontsize=12, color=GRY)
    PF = PP0(2.0, k); PC = PP0(Ma_of_AA(Ae, k, 'sub'), k); a1.set_ylim(0, 1.1); a1.set_xlim(0, 1); a1.set_xlabel(T(lang, 'vị trí x/L', 'position x/L')); a1.set_ylabel('P/P$_0$'); a1.legend(loc='lower left', frameon=False, fontsize=11.5)
    a1.set_title(T(lang, 'P/P₀ dọc vòi (đẳng entropi)', 'P/P₀ along the nozzle (isentropic)'), fontsize=13)
    bs = np.linspace(0.999, PC, 80); mm = []
    for b in bs:
        Me = Ma_of_PP(b, k); mm.append(AAs(Me, k) / Ae)            # ṁ/ṁ_max = A_e/(A*') ... = AA(Me)/Ae ratio inverse: A*' = Ae/AA(Me); ṁ/ṁmax = A_t/A*' with A_t = A* = 1
    mm = [AAs(Ma_of_PP(b, k), k) / 1.0 for b in bs]; mm = [Ae / v for v in mm]
    a2.plot(list(bs) + [PC, 0.0], mm + [1.0, 1.0], color=NAVY, lw=2.4); a2.axvline(PC, color=BLU, ls='--', lw=1); a2.axvline(PF, color=RED, ls='--', lw=1)
    a2.set_xlim(0, 1); a2.set_ylim(0, 1.15); a2.set_xlabel('P$_b$/P$_0$'); a2.set_ylabel('ṁ/ṁ$_{max}$'); a2.text(PC - 0.045, 0.15, 'P$_C$ = ' + dec(lang, PC, 3), color=BLU, fontsize=11.5, rotation=90, va='bottom'); a2.text(PF + 0.02, 0.15, 'P$_F$ = ' + dec(lang, PF, 4), color=RED, fontsize=11.5, rotation=90, va='bottom')
    a2.text(0.15, 0.42, T(lang, 'giữa P$_F$ và P$_C$:\nsóng xung kích\n(Bổ sung từ sách,\nkhông tính ở đây)', 'between P$_F$ and P$_C$:\nshock wave\n(Added from the book,\nnot computed here)'), fontsize=11, color=GRY)
    a2.set_title(T(lang, 'Lưu lượng theo P$_b$/P₀', 'Flow against P$_b$/P₀'), fontsize=13); fig.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.14); save(fig, 'fig_cd', lang)

if __name__ == '__main__':
    for lang in ('vi', 'en'):
        fig_ratios(lang); fig_area(lang); fig_conv(lang); fig_cd(lang)
    print('figures written to', OUT, sorted(os.listdir(OUT)))
