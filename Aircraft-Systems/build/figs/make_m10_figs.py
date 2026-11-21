# -*- coding: utf-8 -*-
"""Hinh cho module 10 (tu ve lai bang matplotlib, du lieu tu adda.py): assets/figs/m10/{sample_quant,dac_steps,sar_steps}_{vi,en}.png. figsize = px/100, chu >= 14 pt."""
import os, sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import adda as A
OUT = os.path.join(ROOT, 'assets', 'figs', 'm10'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size': 14, 'axes.titlesize': 15, 'axes.labelsize': 14, 'figure.dpi': 100, 'savefig.dpi': 100})
L = {'vi': dict(t='Lấy mẫu, giữ và lượng tử hoá một sóng', a='tín hiệu tương tự', h='sau mạch giữ (bậc thang)', q2='lượng tử hoá 2 bit (4 mức)', q4='lượng tử hoá 4 bit (16 mức)', time='thời gian (khoảng lấy mẫu)', lev='mức lượng tử', cap='tự vẽ lại',
             t2='DAC trọng số nhị phân 4 bit của Tooley: điện áp ra theo mã', code='mã nhị phân đưa vào DAC (thập phân)', v='$V_{out}$ (V)', t3='ADC xấp xỉ liên tiếp: $V_{in}=5{,}1$ V', trial='lần thử', dac='ngõ ra DAC (V)', vin='điện áp vào 5,1 V', keep='giữ bit', reset='bỏ bit'),
     'en': dict(t='Sampling, holding and quantising a waveform', a='analog signal', h='after the hold circuit (staircase)', q2='2-bit quantisation (4 levels)', q4='4-bit quantisation (16 levels)', time='time (sampling intervals)', lev='quantisation level', cap='redrawn',
             t2='Tooley 4-bit binary-weighted DAC: output voltage against code', code='binary code applied to the DAC (decimal)', v='$V_{out}$ (V)', t3='Successive-approximation ADC: $V_{in}=5.1$ V', trial='trial', dac='DAC output (V)', vin='input voltage 5.1 V', keep='bit kept', reset='bit reset')}
for lg, s in L.items():
    # 1) lay mau - giu - luong tu hoa
    t = np.linspace(0, 13, 600); x = lambda t: 1.5 + 1.4 * np.sin(2 * np.pi * t / 13 * 1.1 + 0.4) * (0.6 + 0.4 * np.cos(2 * np.pi * t / 13))
    ts = np.arange(0.5, 13, 1.0)
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.6), sharey=True)
    for a, nb, lab in ((ax[0], 2, s['q2']), (ax[1], 4, s['q4'])):
        lv = 2 ** nb; xmax = 3.0
        a.plot(t, x(t), color='#9aa3b2', lw=2, label=s['a'])
        step = xmax / (lv - 1); q = np.floor(np.clip(x(ts), 0, xmax) / step) * step
        a.step(np.append(ts - 0.5, ts[-1] + 0.5), np.append(q, q[-1]), where='post', color='#c8102e', lw=2.2, label=lab)
        a.set_title(lab); a.set_xlabel(s['time']); a.grid(alpha=.25); a.set_ylim(-0.1, 3.2)
    ax[0].set_ylabel('V'); ax[0].legend(loc='lower left', fontsize=12)
    fig.suptitle(s['t'] + f' ({s["cap"]})', fontsize=15); fig.tight_layout(); fig.savefig(os.path.join(OUT, f'sample_quant_{lg}.png')); plt.close(fig)
    # 2) DAC trong so nhi phan: bac thang
    codes = np.arange(16); v = [A.dac_weighted_closed(int(c)) for c in codes]
    fig, a = plt.subplots(figsize=(9, 5)); a.step(codes, v, where='mid', color='#1d3f8a', lw=2.4); a.plot(codes, v, 'o', color='#c8102e')
    for c in (10, 15): a.annotate(f'{format(c, "04b")}: {v[c]:.3f} V'.replace('.', ',' if lg == 'vi' else '.'), (c, v[c]), textcoords='offset points', xytext=(-6, 14 if c == 15 else -22), ha='right', fontsize=13)
    a.set_title(s['t2'], fontsize=15); a.set_xlabel(s['code']); a.set_ylabel(s['v']); a.set_xticks(codes); a.grid(alpha=.25); fig.tight_layout(); fig.savefig(os.path.join(OUT, f'dac_steps_{lg}.png')); plt.close(fig)
    # 3) SAR
    code, st = A.sar_trace(5.1); fig, a = plt.subplots(figsize=(9, 5)); a.axhline(5.1, color='#9aa3b2', lw=2, ls='--', label=s['vin'])
    for k, trial, dac, keep in st:
        a.bar(k, dac, color='#2e8b57' if keep else '#c8102e', width=.55); a.text(k, dac + .25, f'{dac:g} V', ha='center', fontsize=13)
    from matplotlib.patches import Patch
    a.legend(handles=[plt.Line2D([], [], color='#9aa3b2', lw=2, ls='--', label=s['vin']), Patch(color='#2e8b57', label=s['keep']), Patch(color='#c8102e', label=s['reset'])], fontsize=12, loc='upper right')
    a.set_xticks([1, 2, 3, 4]); a.set_xlabel(s['trial']); a.set_ylabel(s['dac']); a.set_title(s['t3'], fontsize=15); a.set_ylim(0, 10); a.grid(alpha=.2, axis='y')
    fig.tight_layout(); fig.savefig(os.path.join(OUT, f'sar_steps_{lg}.png')); plt.close(fig)
print(sorted(os.listdir(OUT)))
