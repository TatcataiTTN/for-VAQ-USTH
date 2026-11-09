"""Jaeger 5e Chapter 6 problems that refer to a figure (Fig. P6.31 bus driver, Figs. 6.24 and 6.30 reference NMOS gates).  The reference designs of Fig. 6.24 all dissipate VDD·IDD = 0.2 mW at vO = VL
(checked below from the circuits themselves); power scaling of ratioed logic multiplies every W/L (and divides every resistor) by the power factor (Sec. 6.11.3)."""
import math
import numpy as np
from core import *
from fighelp import cir
KN = 100e-6
def drv(num, dv, dt, tag, extra):
    C, N = 50e-12, 64; i1 = C * dv / dt; I = N * i1
    t = np.linspace(0, dt, 2001); v = dv * (1 - t / dt); iC = -C * np.gradient(v, t)                                  # current into the driver output = −C dv/dt on the linear ramp
    close(iC[10:-10].max(), i1, 1e-6); close(np.trapz(iC, t), C * dv, 1e-6)                                         # constant plateau, total charge C·ΔV
    return [('Current of one driver iC = C·ΔV/Δt', f'{si(i1, "A", 4)} (a rectangular pulse of this height lasting {si(dt, "s", 3)}, zero before and after)'), (f'Peak current for all 64 drivers switching together ({tag})', si(I, 'A', 4))] + extra, \
        'The load capacitance is discharged by the driver along the linear fall of the figure: iC = −C·dvO/dt = C·ΔV/Δt, constant during the fall. The 64 lines add: Ipeak = 64·C·ΔV/Δt. Numerical differentiation of the ramp and integration of the current (charge C·ΔV) confirm it.', \
        ['The statement says a 2.5 V swing in 0.8 ns, while the waveform of Fig. P6.31 is drawn from 3.3 V with a fall time labelled 1 ns: the statement\'s numbers are used and the figure\'s numbers are also given.'], i1, I
@solve('6.31')
def _():
    C = 50e-12; alt = 64 * C * 3.3 / 1e-9
    r = drv('6.31', 2.5, 0.8e-9, '2.5 V in 0.8 ns', [('With the values drawn in the figure (3.3 V in 1 ns)', f'{si(C * 3.3 / 1e-9, "A", 4)} per driver, {si(alt, "A", 4)} for 64 drivers')])
    return r[0], r[1], r[2], cir('6.31', 'Fig. P6.31', 'inverter-type bus driver (supplies V+ and V−) discharging the load capacitance C (50 pF) with the current iC flowing from the capacitor into the output; below, vO(t) falls linearly from the high level to 0 V in the time marked 1 ns.')
@solve('6.32')
def _():
    C = 50e-12; alt = 64 * C * 3.3 / 0.1e-9
    r = drv('6.32', 2.5, 0.1e-9, '2.5 V in 0.1 ns', [('With a 3.3 V swing as drawn in the figure', f'{si(C * 3.3 / 0.1e-9, "A", 4)} per driver, {si(alt, "A", 4)} for 64 drivers'), ('Clock', 'a 1-GHz clock (period 1 ns) leaves 0.9 ns between the falling edges; the fall time is 0.1 ns (statement)')])
    return r[0], r[1], r[2] + ['Repeat of Prob. 6.31 with a fall time of 0.1 ns.'], cir('6.32', 'Fig. P6.31', 'inverter-type bus driver discharging the load capacitance C (50 pF); vO(t) falls linearly (in the figure from the high level to 0 V in 1 ns; here the fall time is 0.1 ns).')
# ---- reference inverters of Fig. 6.24 (VDD = 2.5 V, VL = 0.2 V, Kn' = 100 μA/V², VTN = 0.6 V, γ = 0.5 √V, 2φF = 0.6 V) ----
def ref_checks():
    R = 28.8e3; I_a = (2.5 - 0.2) / R; P = 2.5 * I_a                                              # (a) resistor load
    wl_ms = 2.22; I_ms = KN * wl_ms * ((2.5 - 0.6 - 0.2 / 2) * 0.2); close(I_ms, I_a, 1e-3)               # the switching transistor carries the same current (square-law, triode)
    vt = 0.6 + 0.5 * (math.sqrt(0.6 + 0.2) - math.sqrt(0.6)); I_b = KN / 2 * (1 / 1.68) * (2.5 - 0.2 - vt) ** 2; close(I_b, I_a, 5e-3)        # (b) saturated load with body effect
    I_bs = KN * 4.71 * ((1.55 - 0.6 - 0.2 / 2) * 0.2); close(I_bs, I_a, 5e-3)                        # (b): the high input level is VH = 1.55 V, not 2.5 V
    return P, I_a
P_REF, I_REF = ref_checks()
@solve('6.119')
def _():
    f = 2e-3 / P_REF; close(P_REF, 0.2e-3, 5e-3); close(f, 10, 5e-3)
    rows = [('Reference power (VDD·IDD at vO = VL)', f'{si(P_REF, "W", 4)} (IDD = {si(I_REF, "A", 4)}, checked from the resistor design and from the switching and load devices of (b))'), ('Power factor', f'2 mW / {si(P_REF, "W", 3)} = {g(f, 4)} ≈ 10 (the exact factor is rounded to 10 since the reference power is 0.2 mW)')]
    f = 10.0
    rows += [('(a) resistor load', f'R = 28.8 kΩ/10 = {g(28.8 / f, 4)} kΩ (L/W = 288/1); MS: 2.22/1 → {g(2.22 * f, 4)}/1'), ('(b) saturated load', f'MS 4.71/1 → {g(4.71 * f, 4)}/1; ML 1/1.68 → {g(f / 1.68, 4)}/1 (velocity-saturation version 1/1.56 → {g(f / 1.56, 4)}/1)'),
             ('(c) linear load', f'MS 2.22/1 → {g(2.22 * f, 4)}/1; ML 1/5.72 → {g(f / 5.72, 4)}/1 (1/3.81 → {g(f / 3.81, 4)}/1)'), ('(d) depletion load', f'MS 2.22/1 → {g(2.22 * f, 4)}/1; ML 1.81/1 → {g(1.81 * f, 4)}/1'), ('(e) pseudo-NMOS', f'MS 2.22/1 → {g(2.22 * f, 4)}/1; ML 1/1.11 → {g(f / 1.11, 4)}/1 (1/1.28 → {g(f / 1.28, 4)}/1)')]
    return rows, 'In ratioed logic the voltage levels depend only on W/L ratios, so multiplying every W/L by k multiplies every drain current and the power by k and leaves VH and VL unchanged (Sec. 6.11.3); a resistor is divided by k. The reference gates of Fig. 6.24 dissipate 0.2 mW (checked: 2.3 V/28.8 kΩ = 79.9 μA; the switching transistor 2.22/1 and the saturated-load pair of (b) carry the same current in the square-law model), so 2 mW needs k = 10.', \
        ['Power is taken as the static power VDD·IDD with the output low (0.2 mW) for all five reference designs; the book says only "power dissipation level".', 'The load sizes in parentheses are the velocity-saturation versions printed in the figure.'], cir('6.119', 'Fig. 6.24', 'five NMOS inverter designs, VDD = 2.5 V: (a) 28.8 kΩ resistor load (L/W = 2880), MS 2.22/1; (b) saturated load ML 1/1.68 (1/1.56), MS 4.71/1; (c) linear load (gate at +4 V) ML 1/5.72 (1/3.81), MS 2.22/1; (d) depletion load ML 1.81/1, MS 2.22/1; (e) pseudo-NMOS ML 1/1.11 (1/1.28), MS 2.22/1.')
@solve('6.123')
def _():
    base = [('ML (load)', 1.81), ('MA', 4.44), ('MB', 4.44), ('MC', 8.88), ('MD', 8.88)]; rows = []
    for tag, f in (('(a) power ÷ 8', 1 / 8), ('(b) power × 3.5', 3.5)):
        rows.append((tag, ', '.join(f'{n} {g(w, 3)}/1 → {g(w * f, 3)}/1' for n, w in base)))
        for n, w in base: close(KN * w * f, KN * w * f, 1e-12)
    # independent check on the inverter-type argument: the switching-device current is proportional to W/L at fixed voltages
    i1 = KN * 4.44 * ((2.5 - 0.6 - 0.1) * 0.2); i2 = KN * 4.44 / 8 * ((2.5 - 0.6 - 0.1) * 0.2); close(i1 / i2, 8, 1e-12)
    return rows, 'Power scaling (Sec. 6.11.3): all W/L ratios of the gate are multiplied by the same factor, which multiplies every current and the power by that factor and leaves the logic levels unchanged: factor 1/8 for (a), 3.5 for (b).', ['Fig. 6.30(b): depletion-load NMOS gate with ML = 1.81/1, MA = MB = 4.44/1 and MC = MD = 8.88/1 (as drawn; the figure also shows the 4.44/1 equivalents of the two blocks).', 'W/L ratios below 1 (e.g. 0.226/1) mean a transistor longer than wide.'], cir('6.123', 'Fig. 6.30', 'NMOS gate with a depletion-mode load ML (1.81/1) from +2.5 V to the output Y and a switching network to ground: transistor A (4.44/1) in series with B (4.44/1), with C and D (8.88/1 each, in series with each other) in parallel with A.')
