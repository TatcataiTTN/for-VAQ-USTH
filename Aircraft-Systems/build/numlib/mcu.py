# -*- coding: utf-8 -*-
"""Cong cu tinh cho phan mo rong 'vi dieu khien va he nhung' cua module 04 (Floyd 14-8, 14-9; bo nho dia chi, PWM, bo dinh thoi, bo dem ma hoa vuong goc).
Moi ham co hai cai dat doc lap (_a, _b); build/verify/verify_m04_mcu.py doi chieu."""
from fractions import Fraction as Fr
def addresses_a(n): return 2 ** n
def addresses_b(n):
    c = 1
    for _ in range(n): c *= 2
    return c
addresses = addresses_a
def pwm_avg_a(vs, t_high, period): return vs * t_high / period                      # dien ap trung binh cua xung PWM
def pwm_avg_b(vs, t_high, period): return float(Fr(vs) * Fr(t_high) / Fr(period))
pwm_avg = pwm_avg_a
def duty_a(t_high, period): return t_high / period
def duty_b(t_high, period): return float(Fr(t_high, 1) / Fr(period, 1))
duty = duty_a
def timer_s_a(f_clk, prescale, count): return count * prescale / f_clk                 # giay: (so dem x he so chia) / tan so xung nhip
def timer_s_b(f_clk, prescale, count): return float(Fr(count) * Fr(prescale) / Fr(f_clk))
timer_s = timer_s_a
def rollover_s_a(bits, rate): return 2 ** bits / rate                                    # giay de bo dem n bit tran khi dem voi toc do rate (xung/s)
def rollover_s_b(bits, rate): return float(Fr(addresses_b(bits)) / Fr(rate))
rollover_s = rollover_s_a
def access_ns_a(f_mhz, base_clocks, wait): return (base_clocks + wait) * 1000 / f_mhz     # thoi gian chu ky bus (ns) khi them 'wait' trang thai cho
def access_ns_b(f_mhz, base_clocks, wait): return float((Fr(base_clocks) + Fr(wait)) * Fr(1000) / Fr(f_mhz))
access_ns = access_ns_a
