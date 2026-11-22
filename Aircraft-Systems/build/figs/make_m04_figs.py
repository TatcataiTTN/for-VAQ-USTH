# -*- coding: utf-8 -*-
"""Hinh cho phan mo rong vi dieu khien cua module 04 (tu ve lai theo y Floyd Hinh 14-34; PWM tinh bang mcu.py): assets/figs/m04/{mcu_block,pwm_duty}_{vi,en}.png. figsize = px/100, chu >= 14 pt."""
import os, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); sys.path.insert(0, os.path.join(ROOT, 'build', 'numlib')); import mcu as M
OUT = os.path.join(ROOT, 'assets', 'figs', 'm04'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size': 14, 'figure.dpi': 100, 'savefig.dpi': 100})
L = {'vi': dict(t1='Vi điều khiển: cả hệ máy tính trong một vỏ', cap='tự vẽ lại theo ý Floyd Hình 14–34', core='Lõi xử lý', rom='ROM / flash\n(chương trình)', ram='RAM\n(dữ liệu)', gp='GPIO', tm='Bộ định thời', ad='ADC / DAC', cm='UART, SPI, I²C,\nUSB, CAN', pw='PWM,\nmã hoá vuông góc', ext='Bộ điều khiển\nbus ngoài', pb='Bus ngoại vi', ib='Bus nội (địa chỉ, dữ liệu, điều khiển)', pin='chân vào/ra',
             t2='PWM: giữ biên độ {vs} V, đổi chu kỳ làm việc D để đổi điện áp trung bình', avg='trung bình', ms='thời gian (ms)', v='điện áp (V)'),
     'en': dict(t1='Microcontroller: a whole computer system in one package', cap='redrawn after the idea of Floyd Figure 14–34', core='Processor\ncore', rom='ROM / flash\n(program)', ram='RAM\n(data)', gp='GPIO', tm='Timers', ad='ADC / DAC', cm='UART, SPI, I²C,\nUSB, CAN', pw='PWM,\nquadrature encoder', ext='External bus\ncontroller', pb='Peripheral bus', ib='Internal buses (address, data, control)', pin='I/O pins',
             t2='PWM: keep the {vs} V amplitude, change the duty cycle D to change the average voltage', avg='average', ms='time (ms)', v='voltage (V)')}
for lg, s in L.items():
    fig, ax = plt.subplots(figsize=(11, 6.2)); ax.set_xlim(0, 11); ax.set_ylim(0, 6.2); ax.axis('off')
    ax.add_patch(FancyBboxPatch((0.2, 0.4), 10.6, 5.2, boxstyle='round,pad=0.05,rounding_size=0.15', fc='#f4f6fb', ec='#1d3f8a', lw=2.5))
    def box(x, y, w, h, t, fc='#dbe6ff', ec='#1d3f8a'):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc=fc, ec=ec, lw=1.8)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=14)
    box(0.6, 3.3, 2.3, 1.4, s['core'], '#ffe7b8', '#a86b00'); box(0.6, 1.4, 1.5, 1.1, s['rom']); box(2.3, 1.4, 1.2, 1.1, s['ram'])
    ax.plot([0.5, 10.5], [3.0, 3.0], color='#444', lw=3); ax.text(3.95, 2.62, s['ib'], fontsize=13, color='#444')
    ax.plot([1.7, 1.7], [3.0, 3.3], color='#444', lw=2); ax.plot([1.35, 1.35], [2.5, 3.0], color='#444', lw=2); ax.plot([2.9, 2.9], [2.5, 3.0], color='#444', lw=2)
    ax.plot([4.1, 10.5], [4.6, 4.6], color='#c8102e', lw=3); ax.text(4.15, 4.72, s['pb'], fontsize=13, color='#c8102e'); ax.plot([3.0, 4.1], [4.0, 4.6], color='#c8102e', lw=2)
    xs = [4.1, 5.4, 6.9, 8.4]; ws = [1.2, 1.4, 1.3, 2.1]; names = ['gp', 'tm', 'ad', 'cm']
    for x, w, nme in zip(xs, ws, names): box(x, 3.3, w, 1.0, s[nme], '#e1f5e1', '#2c7a2c'); ax.plot([x + w / 2, x + w / 2], [4.3, 4.6], color='#c8102e', lw=2)
    box(5.6, 1.4, 2.4, 1.1, s['pw'], '#e1f5e1', '#2c7a2c'); box(8.3, 1.4, 2.1, 1.1, s['ext'], '#ffe7b8', '#a86b00'); ax.plot([6.8, 6.8], [2.5, 4.6], color='#c8102e', lw=1.5, ls='--'); ax.plot([9.35, 9.35], [2.5, 3.0], color='#444', lw=2)
    ax.text(5.5, 0.62, '↕ ' + s['pin'], ha='center', fontsize=14, color='#444'); ax.set_title(s['t1'], fontsize=15)
    fig.text(0.5, 0.01, s['cap'], ha='center', fontsize=12, color='#555'); fig.tight_layout(); fig.savefig(os.path.join(OUT, f'mcu_block_{lg}.png')); plt.close(fig)
    vs = 12; T = 4.0; fig, axs = plt.subplots(3, 1, figsize=(10, 6.4), sharex=True)
    for a, th in zip(axs, (1.0, 2.0, 3.0)):
        d = M.duty(th, T); v = M.pwm_avg(vs, th, T); xs_, ys_ = [0], [vs]
        for k in range(3): t0 = k * T; xs_ += [t0, t0 + th, t0 + th, t0 + T]; ys_ += [vs, vs, 0, 0]
        xs_ = [0] + [x for x in xs_[1:]]; a.step(xs_, ys_, where='post', color='#1d3f8a', lw=2.2); a.axhline(v, color='#c8102e', ls='--', lw=1.8)
        a.text(11.9, 6 if abs(v - 6) > 1 else 10, f'{s["avg"]} = {v:g} V', ha='right', va='center', color='#c8102e', fontsize=14, bbox=dict(fc='white', ec='none', alpha=.9)); a.set_ylim(-1, 15); a.set_yticks([0, vs]); a.set_ylabel(f'D = {d * 100:g} %', rotation=0, labelpad=40, va='center'); a.grid(alpha=.2)
    axs[-1].set_xlabel(s['ms']); axs[-1].set_xticks(range(0, 13, 2)); axs[-1].set_xlim(0, 12); fig.suptitle(s['t2'].format(vs=vs), fontsize=15); fig.tight_layout(); fig.savefig(os.path.join(OUT, f'pwm_duty_{lg}.png')); plt.close(fig)
print('m04 figures written to', OUT)
