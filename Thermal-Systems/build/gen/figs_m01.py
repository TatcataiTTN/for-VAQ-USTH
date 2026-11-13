"""m01 figures (matplotlib, dpi 100, figsize = displayed px / 100, text >= 14 pt), Vietnamese and English versions -> assets/figs/m01/*.png
Run: .venv/bin/python -I build/gen/figs_m01.py"""
import os, sys, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
from m01_common import isa, thrust, eta_p_simple
OUT = os.path.join(ROOT, 'assets', 'figs', 'm01'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14, 'axes.titlesize': 15, 'axes.labelsize': 14, 'legend.fontsize': 13, 'xtick.labelsize': 14, 'ytick.labelsize': 14, 'axes.grid': True, 'grid.alpha': .3})
NAVY, RED, GRN, ORG, GRY = '#1f3a5f', '#c0392b', '#2e8b57', '#d98324', '#7f8c8d'

def save(fig, name, lang):
    fig.savefig(os.path.join(OUT, f'{name}_{lang}.png'), dpi=100); plt.close(fig)

# ---------------------------------------------------------------- 1. classification tree (redrawn from slides 13 and 27)
def tree(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    fig, ax = plt.subplots(figsize=(12, 6.6)); ax.set_xlim(0, 12); ax.set_ylim(0, 6.6); ax.axis('off'); ax.grid(False)
    def box(x, y, w, h, t, ec, fs=13):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc='white', ec=ec, lw=2))
        ax.text(x, y, t, ha='center', va='center', fontsize=fs)
    def line(x1, y1, x2, y2): ax.plot([x1, x1, x2, x2], [y1, (y1 + y2) / 2, (y1 + y2) / 2, y2], color=GRY, lw=1.5, zorder=0)
    box(6, 6.1, 3.7, .6, L('Động cơ hàng không vũ trụ', 'Aerospace engine'), RED)
    box(3.3, 5.0, 3.0, .6, L('Hút khí (airbreathing)', 'Airbreathing'), NAVY); box(9.5, 5.0, 3.2, .6, L('Không hút khí: tên lửa', 'Non-airbreathing: rocket'), NAVY)
    line(6, 5.8, 3.3, 5.3); line(6, 5.8, 9.5, 5.3)
    box(1.7, 3.9, 3.0, .6, L('Piston (reciprocating)', 'Reciprocating'), GRN); box(5.3, 3.9, 3.0, .6, L('Phản lực (jet propulsion)', 'Jet propulsion'), GRN)
    line(3.3, 4.7, 1.7, 4.2); line(3.3, 4.7, 5.3, 4.2)
    names = [L('Scramjet', 'Scramjet'), 'Ramjet', 'Pulsejet', 'Turboramjet', 'Turborocket', L('Tuabin khí (gas turbine)', 'Gas turbine')]
    xs = [0.9, 2.5, 4.0, 5.7, 7.5, 9.7]
    for x, n in zip(xs, names): box(x, 2.8, 1.45 if n != names[-1] else 2.95, .6, n, '#7d3c98', 12 if n != names[-1] else 13); line(5.3, 3.6, x, 3.1)
    gt = [L('Turbojet', 'Turbojet'), 'Turboprop', 'Turboshaft', 'Turbofan']
    gx = [6.6, 8.15, 9.7, 11.2]
    for x, n in zip(gx, gt): box(x, 1.6, 1.45, .6, n, ORG, 12); line(9.7, 2.5, x, 1.9)
    box(8.3, .55, 3.0, .6, L('Propfan / Advanced ducted fan', 'Propfan / Advanced ducted fan'), ORG, 12); line(9.7, 2.5, 8.3, .85)
    ax.text(.2, 1.7, L('Piston: nạp – nén – sinh công – xả', 'Piston: intake – compression – power – exhaust'), fontsize=13, color=GRN, va='center')
    ax.text(.2, 1.15, L('Phản lực: nén – cháy – giãn nở (đồng thời)', 'Jet: compression – combustion – expansion (simultaneous)'), fontsize=13, color=NAVY, va='center')
    ax.text(.2, .55, L('Sơ đồ tự vẽ lại từ Slide Ch.1 tr.13 và tr.27', 'Redrawn from Slide Ch.1 pp.13 and 27'), fontsize=13, color=GRY, va='center')
    save(fig, 'fig_classification', lang)

# ---------------------------------------------------------------- 2. propulsive efficiency vs speed ratio
def etap(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    fig, ax = plt.subplots(figsize=(9, 5.4)); r = np.linspace(1.0, 6, 300)
    ax.plot(r, 2 / (1 + r), color=NAVY, lw=3)
    pts = [(4.5, L('Turbojet (Farokhi Ex 3.5)', 'Turbojet (Farokhi Ex 3.5)'), RED, (4.55, .62)), (1.25, L('Turbofan (Farokhi Ex 3.6)', 'Turbofan (Farokhi Ex 3.6)'), GRN, (1.4, .96)),
           (560 / 240, L('El-Sayed Problem 2.5', 'El-Sayed Problem 2.5'), ORG, (2.5, .72))]
    for x, lab, c, xy in pts:
        y = 2 / (1 + x); ax.plot([x], [y], 'o', color=c, ms=11); ax.annotate(f'{lab}\nue/u = {x:.2f}, ηp = {y*100:.1f} %', (x, y), xytext=xy, fontsize=13, color=c, arrowprops=dict(arrowstyle='-', color=c))
    ax.axhline(1, color=GRY, ls='--', lw=1)
    ax.set_xlabel(L('Tỉ số vận tốc phụt / vận tốc bay  ue/u', 'Jet-to-flight speed ratio  ue/u')); ax.set_ylabel(L('Hiệu suất đẩy ηp = 2/(1 + ue/u)', 'Propulsive efficiency ηp = 2/(1 + ue/u)'))
    ax.set_ylim(0, 1.08); ax.set_title(L('Gia tốc ít khối lượng lớn hơn thì ηp cao hơn (tự vẽ lại)', 'Accelerating more mass less gives higher ηp (redrawn)'))
    fig.tight_layout(); save(fig, 'fig_etap', lang)

# ---------------------------------------------------------------- 3. ISA with slide-48 markers and Farokhi table points
def isa_fig(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    z = np.linspace(0, 40000, 801); T = []; p = []
    for h in z:
        if h <= 32000: t, pp, _ = isa(h)
        else:
            t, pp = np.nan, np.nan
        T.append(t); p.append(pp)
    # 32-40 km: continue with the 32-47 km layer (T = 228.65 + 0.0028 (z-32000)); p32 from the 20-32 km layer
    t32, p32, _ = isa(32000.0)
    for i, h in enumerate(z):
        if h > 32000:
            T[i] = 228.65 + 0.0028 * (h - 32000); p[i] = p32 * (T[i] / 228.65) ** (-9.80665 / (287.053 * 0.0028))
    T = np.array(T); p = np.array(p) / 100
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.6))
    a1.plot(T - 273.15, z / 1e3, color=NAVY, lw=3); a1.set_xlabel(L('Nhiệt độ T (°C)', 'Temperature T (°C)')); a1.set_ylabel(L('Độ cao z (km)', 'Altitude z (km)'))
    a1.plot([-56], [11], 'o', color=RED, ms=10); a1.annotate(L('11 km: −56.5 °C\n(slide ghi −56 °C)', '11 km: −56.5 °C\n(slide: −56 °C)'), (-56.5, 11), xytext=(-52, 20), fontsize=13, color=RED, arrowprops=dict(arrowstyle='-', color=RED))
    a1.set_title(L('Nhiệt độ ISA', 'ISA temperature'))
    a2.semilogx(p, z / 1e3, color=NAVY, lw=3); a2.set_xlabel(L('Áp suất p (hPa), thang log', 'Pressure p (hPa), log scale')); a2.set_title(L('Áp suất ISA', 'ISA pressure'))
    a2.plot([isa(10000.0)[1] / 100], [10], 's', color=GRN, ms=10); a2.annotate(L('10 km: 264.4 hPa\n(= số "264" trên slide)', '10 km: 264.4 hPa\n(= the "264" on the slide)'), (264.4, 10), xytext=(1.5, 6), fontsize=13, color=GRN, arrowprops=dict(arrowstyle='-', color=GRN))
    a2.plot([isa(11000.0)[1] / 100], [11], 'o', color=RED, ms=10); a2.annotate(L('11 km: 226.3 hPa', '11 km: 226.3 hPa'), (226.3, 11), xytext=(12, 15), fontsize=13, color=RED, arrowprops=dict(arrowstyle='-', color=RED))
    a2.plot([26, 3], [25, 40], 'v', color=ORG, ms=9); a2.annotate(L('slide: 26 hPa @ 25 km\nISA 25.1 hPa', 'slide: 26 hPa @ 25 km\nISA 25.1 hPa'), (26, 25), xytext=(120, 28), fontsize=13, color=ORG, arrowprops=dict(arrowstyle='-', color=ORG))
    a2.annotate(L('slide: 3 hPa @ 40 km\nISA 2.87 hPa', 'slide: 3 hPa @ 40 km\nISA 2.87 hPa'), (3, 40), xytext=(20, 36.5), fontsize=13, color=ORG, arrowprops=dict(arrowstyle='-', color=ORG))
    for ax in (a1, a2): ax.set_ylim(0, 41)
    a2.set_xlim(1, 1500)
    fig.tight_layout(); save(fig, 'fig_isa', lang)

# ---------------------------------------------------------------- 4. El-Sayed Example 2.3: thrust versus flight speed
def thrust_speed(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    U = np.linspace(500, 6000, 200); Ua = U / 3.6
    rho = 30.8e3 / (287 * 229.74); Tp = .25 * (200 - 30.8) * 1e3
    g1 = 40 * 1.02 * 600 + Tp; n1 = g1 - 40 * Ua
    ma2 = rho * Ua * .235; n2 = ma2 * 1.02 * 600 + Tp - ma2 * Ua
    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.plot(U, n1 / 1e3, color=NAVY, lw=3, label=L('Lưu lượng không đổi 40 kg/s', 'Constant air flow 40 kg/s')); ax.plot(U, n2 / 1e3, color=RED, lw=3, label=L('Lưu lượng ṁa = ρ·U·Ai', 'Air flow ṁa = ρ·U·Ai'))
    ax.axhline(g1 / 1e3, color=GRY, ls='--'); ax.text(3300, g1 / 1e3 + 2, L('lực đẩy tổng 66.78 kN', 'gross thrust 66.78 kN'), color=GRY, fontsize=13)
    ax.axhline(0, color='k', lw=1); ax.set_xlabel(L('Vận tốc bay U (km/h)', 'Flight speed U (km/h)')); ax.set_ylabel(L('Lực đẩy thực (kN)', 'Net thrust (kN)'))
    ax.set_title(L('El-Sayed Ví dụ 2.3: lực đẩy thực giảm khi bay nhanh (tự vẽ lại)', 'El-Sayed Example 2.3: net thrust vs flight speed (redrawn)'), fontsize=14); ax.legend(loc='lower left')
    fig.tight_layout(); save(fig, 'fig_thrust_speed', lang)

# ---------------------------------------------------------------- 5. El-Sayed Problem 2.7: eta_p and thrust vs u/ue
def prob27(lang):
    L = lambda vi, en: vi if lang == 'vi' else en
    ma, ue, pa, pe, Ae = 50., 500., 60e3, 120e3, .25; x = np.linspace(0, 1, 201); u = x * ue
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.4)); cols = [NAVY, GRN, ORG, RED]
    for f, c in zip((0.0, 0.01, 0.015, 0.02), cols):
        T = ma * ((1 + f) * ue - u) + (pe - pa) * Ae; me = ma * (1 + f); wake = .5 * me * (ue - u) ** 2
        a1.plot(x, T / 1e3, color=c, lw=2.5, label=f'f = {f}'); a2.plot(x, T * u / (T * u + wake), color=c, lw=2.5, label=f'f = {f}')
    a1.set_xlabel('u/ue'); a1.set_ylabel(L('Lực đẩy thực (kN)', 'Net thrust (kN)')); a1.set_title(L('Lực đẩy giảm tuyến tính theo u', 'Thrust falls linearly with u')); a1.legend()
    a2.set_xlabel('u/ue'); a2.set_ylabel(L('Hiệu suất đẩy ηp (biểu thức 1)', 'Propulsive efficiency ηp (expression 1)')); a2.set_title(L('ηp tăng theo u/ue (Pe = 120, Pa = 60 kPa)', 'ηp rises with u/ue (Pe = 120, Pa = 60 kPa)'), fontsize=13)
    fig.tight_layout(); save(fig, 'fig_problem27', lang)

if __name__ == '__main__':
    for lang in ('vi', 'en'):
        tree(lang); etap(lang); isa_fig(lang); thrust_speed(lang); prob27(lang)
    print('figures written to', OUT, sorted(os.listdir(OUT)))
