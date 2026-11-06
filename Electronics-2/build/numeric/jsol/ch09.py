"""Jaeger 5e chapter 9 (bipolar logic): ECL noise margin NM = ΔV/2 − VT[1 + ln(ΔV/VT − 1)] (Eqs. 9.29/9.30, checked with the book's 0.197 V for ΔV = 0.6 V) and PDP = P·τ."""
import math
from core import *
def nm(dv, vt): return dv / 2 - vt * (1 + math.log(dv / vt - 1))
def solve_dv(target, vt):
    lo, hi = 2.5 * vt, 5.0
    for _ in range(100):
        m = (lo + hi) / 2
        if nm(m, vt) < target: lo = m
        else: hi = m
    return (lo + hi) / 2
close(nm(0.6, 0.025), 0.1966, 2e-3)                                     # the book's own check
@solve('9.19')
def _():
    dv = solve_dv(0.1, 0.025); close(nm(dv, 0.025), 0.1, 1e-6)
    return [('Minimum logic swing ΔV (VT = 25 mV)', f'{g(dv)} V')], 'Solve NM = ΔV/2 − VT[1 + ln(ΔV/VT − 1)] = 0.1 V numerically (the NM grows with ΔV).', ['Room temperature: VT = 25 mV (the value the book uses in Section 9.3).']
@solve('9.22')
def _():
    k = 8.617333e-5; out = []; worst = 0
    for t in (-55, 27, 75):
        vt = k * (t + 273.15); dv = solve_dv(0.1, vt); out.append((f'{t} °C: VT = {g(vt * 1000)} mV, ΔV needed for NM = 0.1 V', f'{g(dv)} V')); worst = max(worst, dv)
    close(nm(worst, k * (75 + 273.15)), 0.1, 1e-6)
    return out + [('Logic swing to design for', f'ΔV ≥ {g(worst)} V (set by the hottest case, +75 °C)')], 'NM falls as VT = kT/q rises, so the +75 °C end of the range sets ΔV; the same ΔV then gives NM > 0.1 V at lower temperatures.', ['ΔV = IEE·RC is taken as temperature independent.']
@solve('9.106')
def _(): return [('(a) τ = PDP/P at 0.3 mW', si(0.5e-12 / 0.3e-3, 's')), ('(b) P = PDP/τ for τ = 1 ns', si(0.5e-12 / 1e-9, 'W'))], 'PDP = P·τ (Eq. 9.x, definition of the power-delay product).', []
@solve('9.109')
def _(): p = 20 / 50000; return [('Power per gate', si(p, 'W')), ('Minimum gate delay τ = PDP/P', si(25e-15 / p, 's'))], 'All gates dissipate the same power: P = 20 W/50,000, τ = PDP/P.', []
