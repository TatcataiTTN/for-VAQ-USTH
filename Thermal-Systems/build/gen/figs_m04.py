"""m04 figures (matplotlib, dpi 100, figsize = displayed px / 100, text >= 13 pt), Vietnamese and English versions -> assets/figs/m04/*.png
All curves are computed: air-fuel ratio and product composition from the element balance (rounded masses, as the slides), dew point from IAPWS-IF97 with the A-5 interpolation points
marked, sensible enthalpy from the tables A-18...A-23 (props library), formation/combustion levels from A-26.  Nothing is traced from a slide; the lecturer's numeric examples
(Ch.4 p.17, 30, 32, 36, 37, 44, 54) are drawn as marked points.  Run: .venv/bin/python -I build/gen/figs_m04.py"""
import os, sys, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from iapws import IAPWS97
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
from m04_common import *
OUT = os.path.join(ROOT, 'assets', 'figs', 'm04'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14, 'axes.titlesize': 14, 'axes.labelsize': 14, 'legend.fontsize': 13, 'xtick.labelsize': 13, 'ytick.labelsize': 13, 'axes.grid': False})
NAVY, RED, GRN, ORG, GRY, PUR, BLU = '#1f3a5f', '#c0392b', '#2e8b57', '#d98324', '#7f8c8d', '#7d3c98', '#2f6db5'
def save(fig, name, lang): fig.savefig(os.path.join(OUT, f'{name}_{lang}.png'), dpi=100); plt.close(fig)
def T(lang, vi, en): return vi if lang == 'vi' else en
def dec(lang, x, nd=1):
    s = f'{x:.{nd}f}'; return s.replace('.', ',') if lang == 'vi' else s

def fig_af(lang):
    fig, ax = plt.subplots(figsize=(7.6, 4.5)); lam = np.linspace(0.8, 3.0, 50)
    for f, c, lab in (('CH4', GRN, 'CH$_4$'), ('C2H6', ORG, 'C$_2$H$_6$'), ('C8H18', NAVY, 'C$_8$H$_{18}$'), ('C2H5OH', PUR, 'C$_2$H$_5$OH')):
        st = combustion(single(f), 1.0)['AF']; ax.plot(lam * 100, lam * st, color=c, lw=2.2, label=f'{lab}  (AF$_{{st}}$ = {dec(lang, st, 1)})')
    pts = [(160.0, combustion(single('C8H18'), 1.6)['AF'], 'C$_8$H$_{18}$, 20 kmol O$_2$', 'tr.17'), (120.0, combustion(single('C2H6'), 1.2)['AF'], 'C$_2$H$_6$, 20 %', 'tr.30')]
    for x, y, lab, pg in pts:
        ax.plot([x], [y], 'o', color=RED, ms=8, zorder=5); ax.annotate(f'{dec(lang, y, 1)}', (x, y), textcoords='offset points', xytext=(8, -16), color=RED, fontsize=13)
    ax.axvline(100, color=GRY, lw=1, ls='--'); ax.text(102, 3, T(lang, '100 % lý thuyết', '100 % theoretical'), color=GRY, fontsize=12)
    ax.set_xlabel(T(lang, 'không khí đã dùng [% lý thuyết]', 'air used [% theoretical]')); ax.set_ylabel(T(lang, 'AF [kg không khí/kg nhiên liệu]', 'AF [kg air/kg fuel]'))
    ax.set_title(T(lang, 'AF tăng tuyến tính theo lượng không khí (chấm đỏ: ví dụ slide)', 'AF grows linearly with the air used (red dots: slide examples)'), fontsize=13)
    ax.legend(loc='upper left', frameon=False); ax.set_xlim(80, 300); ax.set_ylim(0, 50); fig.tight_layout(); save(fig, 'fig_af', lang)

def fig_prod(lang):
    fig, ax = plt.subplots(figsize=(7.6, 4.5)); lam = np.linspace(1.0, 4.0, 60); s = single('C8H18')
    rs = [combustion(s, l) for l in lam]
    for key, c, lab in (('N2', BLU, 'N$_2$'), ('H2O', GRN, 'H$_2$O'), ('O2', ORG, 'O$_2$'), ('CO2', RED, 'CO$_2$')):
        ax.plot(lam * 100, [r[key] / r['n_tot'] * 100 for r in rs], color=c, lw=2.2, label=lab)
    ax.set_xlabel(T(lang, 'không khí đã dùng [% lý thuyết]', 'air used [% theoretical]')); ax.set_ylabel(T(lang, 'phần mol trong sản phẩm [%]', 'mole fraction in the products [%]'))
    ax.set_title(T(lang, 'Octan: thành phần sản phẩm (cơ sở ướt) theo lượng không khí', 'Octane: wet product composition versus the air used'), fontsize=13)
    r = combustion(s, 1.6); ax.plot([160], [r['O2'] / r['n_tot'] * 100], 'o', color=RED, ms=8); ax.annotate(T(lang, 'slide tr.16: 7,5 O$_2$', 'slide p.16: 7.5 O$_2$'), (160, r['O2'] / r['n_tot'] * 100), xytext=(175, 45), fontsize=12, color=RED, arrowprops=dict(arrowstyle='->', color=RED))
    ax.legend(loc='center right', frameon=False, ncol=2); ax.set_xlim(100, 400); ax.set_ylim(0, 85); fig.tight_layout(); save(fig, 'fig_prod', lang)

def fig_dew(lang):
    fig, ax = plt.subplots(figsize=(7.6, 4.5)); lam = np.linspace(1.0, 3.0, 40)
    for f, c, lab in (('CH4', GRN, 'CH$_4$'), ('C2H6', ORG, 'C$_2$H$_6$'), ('C8H18', NAVY, 'C$_8$H$_{18}$')):
        Tdp = []
        for l in lam:
            r = combustion(single(f), l); Pv = r['H2O'] / r['n_tot'] * 100.0; Tdp.append(IAPWS97(P=Pv / 1000.0, x=0).T - 273.15)
        ax.plot(lam * 100, Tdp, color=c, lw=2.2, label=lab)
    r = combustion(single('C2H6'), 1.2); Pv, Ta5 = dew_point(r['H2O'], r['n_tot'], 100.0); Ti = IAPWS97(P=Pv / 1000, x=0).T - 273.15
    ax.plot([120], [Ta5], 's', color=RED, ms=9, zorder=5, label=T(lang, f'slide tr.32: {dec(lang, Ta5, 1)} (nội suy A-5)', f'slide p.32: {dec(lang, Ta5, 1)} (A-5 interpolation)'))
    ax.plot([120], [Ti], 'o', color=BLU, ms=7, zorder=5, label=T(lang, f'IAPWS: {dec(lang, Ti, 2)}', f'IAPWS: {dec(lang, Ti, 2)}'))
    ax.set_xlabel(T(lang, 'không khí đã dùng [% lý thuyết]', 'air used [% theoretical]')); ax.set_ylabel(T(lang, 'nhiệt độ điểm sương [°C]', 'dew-point temperature [°C]'))
    ax.set_title(T(lang, 'Điểm sương ở 100 kPa: càng nhiều không khí thừa càng thấp', 'Dew point at 100 kPa: the more excess air, the lower'), fontsize=13)
    ax.legend(loc='upper right', frameon=False, fontsize=12); ax.set_xlim(100, 300); fig.tight_layout(); save(fig, 'fig_dew', lang)

def fig_enth(lang):
    fig, ax = plt.subplots(figsize=(7.6, 4.8)); f = lambda k: HF(k)
    # levels in 10^6 kJ/kmol relative to the elements (C, H2, O2 at 25 C: 0)
    react = f('C8H18_l'); pl = 8 * f('CO2') + 9 * f('H2O_l'); pg = 8 * f('CO2') + 9 * f('H2O_g'); sc = 1e6
    levels = [(react, T(lang, 'chất phản ứng\nC$_8$H$_{18}$(ℓ) + không khí', 'reactants\nC$_8$H$_{18}$(ℓ) + air'), NAVY), (pg, T(lang, 'sản phẩm\nH$_2$O hơi', 'products\nH$_2$O vapor'), ORG), (pl, T(lang, 'sản phẩm\nH$_2$O lỏng', 'products\nH$_2$O liquid'), GRN)]
    ax.axhline(0, color=GRY, lw=1.2, ls='--'); ax.text(2.15, 0.15, T(lang, 'nguyên tố bền: h$_f^\\circ$ = 0', 'stable elements: h$_f^\\circ$ = 0'), fontsize=12, color=GRY, ha='right')
    xs = [0.2, 1.1, 1.95]
    for x, (y, lab, c) in zip(xs, levels):
        ax.plot([x - 0.25, x + 0.25], [y / sc] * 2, color=c, lw=4); ax.text(x, y / sc - 0.5, f'{dec(lang, y / sc, 3)}'.replace('-', '−'), ha='center', fontsize=13, color=c)
    ax.annotate('', xy=(0.65, pg / sc), xytext=(0.65, react / sc), arrowprops=dict(arrowstyle='->', color=RED, lw=2)); ax.text(0.58, (pg + react) / 2 / sc, T(lang, 'h$_C$ (LHV)\n' + dec(lang, (pg - react) / sc, 3).replace('-', '−'), 'h$_C$ (LHV)\n' + dec(lang, (pg - react) / sc, 3).replace('-', '−')), ha='right', va='center', fontsize=12, color=RED)
    ax.annotate('', xy=(1.5, pl / sc), xytext=(1.5, pg / sc), arrowprops=dict(arrowstyle='->', color=BLU, lw=2)); ax.text(1.56, (pl + pg) / 2 / sc, T(lang, '9 h$_{fg}$ ≈ 0,396', '9 h$_{fg}$ ≈ 0.396'), ha='left', va='center', fontsize=12, color=BLU)
    ax.annotate('', xy=(2.3, pl / sc), xytext=(2.3, react / sc), arrowprops=dict(arrowstyle='->', color=GRN, lw=2)); ax.text(2.25, (pl + react) / 2 / sc + 0.2, T(lang, 'h$_C$ (HHV)\n' + dec(lang, (pl - react) / sc, 3).replace('-', '−'), 'h$_C$ (HHV)\n' + dec(lang, (pl - react) / sc, 3).replace('-', '−')), ha='right', va='center', fontsize=12, color=GRN)
    ax.set_xticks(xs); ax.set_xticklabels([x[1] for x in levels], fontsize=11); ax.tick_params(axis='x', length=0)
    ax.set_ylabel(T(lang, 'entanpi hình thành [10$^6$ kJ/kmol C$_8$H$_{18}$]', 'formation enthalpy [10$^6$ kJ/kmol C$_8$H$_{18}$]'))
    ax.set_title(T(lang, 'Octan lỏng: HHV − LHV = 9 h$_{fg}$ (A-26, slide tr.54)', 'Liquid octane: HHV − LHV = 9 h$_{fg}$ (A-26, slide p.54)'), fontsize=13)
    ax.set_xlim(-0.2, 2.5); ax.set_ylim(-6.6, 0.6); fig.tight_layout(); save(fig, 'fig_enth', lang)

def fig_sens(lang):
    fig, ax = plt.subplots(figsize=(7.6, 4.5)); Ts = np.arange(300, 2001, 50)
    for g, c, lab in (('H2O', GRN, 'H$_2$O'), ('CO2', RED, 'CO$_2$'), ('O2', ORG, 'O$_2$'), ('N2', BLU, 'N$_2$')):
        ax.plot(Ts, [sens(g, float(t)) / 1000 for t in Ts], color=c, lw=2.2, label=lab)
    ax.plot([500], [sens('N2', 500.0) / 1000], 'o', color=NAVY, ms=8, zorder=5); ax.annotate(T(lang, 'slide tr.44: N$_2$, 500 K\n14 581 − 8669 = 5912', 'slide p.44: N$_2$, 500 K\n14,581 − 8669 = 5912'), (500, 5.912), xytext=(560, 50), fontsize=12, color=NAVY, arrowprops=dict(arrowstyle='->', color=NAVY))
    ax.set_xlabel('T [K]'); ax.set_ylabel(T(lang, 'h̄(T) − h̄(298 K) [10$^3$ kJ/kmol]', 'h̄(T) − h̄(298 K) [10$^3$ kJ/kmol]'))
    ax.set_title(T(lang, 'Entanpi hiển nhiệt so với trạng thái chuẩn (A-18…A-23)', 'Sensible enthalpy relative to the standard state (A-18…A-23)'), fontsize=13)
    ax.legend(loc='upper left', frameon=False); ax.set_xlim(300, 2000); fig.tight_layout(); save(fig, 'fig_sens', lang)

if __name__ == '__main__':
    for lang in ('vi', 'en'):
        for f in (fig_af, fig_prod, fig_dew, fig_enth, fig_sens): f(lang)
    print(sorted(os.listdir(OUT)))
