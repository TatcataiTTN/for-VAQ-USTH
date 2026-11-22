# -*- coding: utf-8 -*-
"""Hinh cho module 11 (tu ve lai bang matplotlib, du lieu tinh bang seq.py): assets/figs/m11/{ripple_timing,astable_555}_{vi,en}.png. figsize = px/100, chu >= 14 pt."""
import os, sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import seq as S
OUT = os.path.join(ROOT, 'assets', 'figs', 'm11'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size': 14, 'axes.titlesize': 15, 'axes.labelsize': 14, 'figure.dpi': 100, 'savefig.dpi': 100})
L = {'vi': dict(t1='Bộ đếm gợn sóng 3 bit: mỗi tầng chia đôi tần số của tầng trước', cap1='tự vẽ lại theo ý Floyd Hình 9-6 (trễ lan truyền bỏ qua)', clk='CLK', cnt='đếm', t2='555 dao động: R1 = 1 kΩ, R2 = 2 kΩ, C = 0,1 μF', th='$t_H$ = %s', tl='$t_L$ = %s', per='$T$ = %s  (f = %s)', time='thời gian (ms)', out='ngõ ra', cap2='tự vẽ theo công thức Floyd 7-6'),
     'en': dict(t1='3-bit ripple counter: each stage halves the frequency of the previous one', cap1='redrawn after the idea of Floyd Figure 9-6 (propagation delay ignored)', clk='CLK', cnt='count', t2='555 astable: R1 = 1 kΩ, R2 = 2 kΩ, C = 0.1 μF', th='$t_H$ = %s', tl='$t_L$ = %s', per='$T$ = %s  (f = %s)', time='time (ms)', out='output', cap2='drawn from the Floyd 7-6 formulas')}
for lg, s in L.items():
    dec = (lambda x: x.replace('.', ',')) if lg == 'vi' else (lambda x: x)
    # 1) gian do thoi gian bo dem gon song 3 bit: trang thai tu seq.ripple (mo phong tung FF), bit i = Qi
    n, pulses = 3, 9
    fig, ax = plt.subplots(n + 2, 1, figsize=(11, 6.4), sharex=True)
    xs = np.arange(0, pulses + 0.001, 0.5); ck = [1 if (x % 1) < 0.5 else 0 for x in xs]
    ax[0].step(xs, ck, where='post', color='#444', lw=2); ax[0].set_ylabel(s['clk'], rotation=0, labelpad=26, va='center')
    for i in range(n):                                   # FF kich o suon xuong (x = k + 0,5): sau j suon xuong trang thai = seq.ripple(n, j)
        y = [(S.ripple(n, int(np.floor(x + 0.5))) >> i) & 1 for x in xs]
        a = ax[1 + i]; a.step(xs, y, where='post', color='#c8102e' if i == n - 1 else '#1d3f8a', lw=2.2); a.set_ylabel(f'Q{i}', rotation=0, labelpad=22, va='center')
    a = ax[n + 1]; a.set_ylim(0, 1)
    for j in range(pulses): a.text(j if j else 0.25, 0.45, str(S.ripple(n, j)), ha='center', va='center', fontsize=14, color='#222')
    a.set_ylabel(s['cnt'], rotation=0, labelpad=26, va='center'); a.set_yticks([]); a.set_xlabel('clock'); a.set_xticks(range(pulses + 1))
    for a in ax[:n + 1]: a.set_ylim(-0.2, 1.3); a.set_yticks([0, 1]); a.grid(alpha=.2)
    fig.suptitle(s['t1'], fontsize=15); fig.tight_layout(); fig.savefig(os.path.join(OUT, f'ripple_timing_{lg}.png')); plt.close(fig)
    # 2) 555 dao dong: tH, tL, T, f tu seq.t555_astable
    a2 = S.t555_astable(1e3, 2e3, 0.1e-6); tH, tL, T = a2['tH'] * 1e3, a2['tL'] * 1e3, a2['T'] * 1e3
    fig, a = plt.subplots(figsize=(10, 4)); xs, ys = [0], [1]
    for k in range(3):
        t0 = k * T; xs += [t0, t0 + tH, t0 + tH, t0 + T]; ys += [1, 1, 0, 0]
    xs.append(3 * T); ys.append(1); a.plot(xs, ys, color='#1d3f8a', lw=2.6)
    a.annotate('', (0, 1.15), (tH, 1.15), arrowprops=dict(arrowstyle='<->', color='#c8102e')); a.text(tH / 2, 1.22, dec(s['th'] % f'{tH:.2f} ms'), ha='center', color='#c8102e')
    a.annotate('', (tH, -0.15), (T, -0.15), arrowprops=dict(arrowstyle='<->', color='#444')); a.text((tH + T) / 2, -0.38, dec(s['tl'] % f'{tL:.2f} ms'), ha='center', color='#444')
    a.text(T * 1.5, 1.22, dec(s['per'] % (f'{T:.2f} ms', f'{a2["f"]:.0f} Hz')), ha='center'); a.set_ylim(-0.55, 1.5); a.set_xlim(-0.02, 3 * T + 0.02); a.set_yticks([0, 1]); a.set_xlabel(s['time']); a.set_ylabel(s['out']); a.set_title(s['t2'], fontsize=15); a.grid(alpha=.2); a.xaxis.set_major_formatter(FuncFormatter(lambda v, _: dec(f'{v:g}')))
    fig.tight_layout(); fig.savefig(os.path.join(OUT, f'astable_555_{lg}.png')); plt.close(fig)
print('ok', os.listdir(OUT))
