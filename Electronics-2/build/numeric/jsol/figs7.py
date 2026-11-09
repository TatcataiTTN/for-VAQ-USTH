"""Jaeger 5e Chapter 7 (CMOS) problems that refer to a figure (Figs. P7.5, P7.14, P7.22 and the reference circuits of Figs. 7.12, 7.20, 7.22, 7.27).  Constants of the problem set: K'n = 100 μA/V²,
K'p = 40 μA/V², VTN = 0.6 V, VTP = −0.6 V unless the statement says otherwise.  Each solver is checked by solving the transistor equations a second way (full piecewise square-law model by bisection)."""
import math
import numpy as np
from core import *
from fighelp import cir
from ch07 import KN, KP, vtc
from scipy.optimize import brentq
def region(vgs, vds, vt):
    """n-channel convention (use the source-referenced magnitudes for the PMOS): cutoff / triode / saturation"""
    if vgs <= vt: return 'cutoff'
    return 'triode' if vds < vgs - vt else 'saturation'
def idn(vgs, vds, kn, vt):
    if vgs <= vt: return 0.0
    return kn * ((vgs - vt) * vds - vds * vds / 2) if vds < vgs - vt else kn / 2 * (vgs - vt) ** 2
def z(x): return 0.0 if abs(x) < 1e-9 else x                                              # the numerical solution leaves 1e-24 V at a rail
INV = 'CMOS inverter: PMOS MP (source to VDD) above NMOS MN (source to −VSS/ground), gates tied to vI, drains tied to vO.'
def levels(vdd, vss, vtn=0.6, vtp=-0.6, kn=2 * KN, kp=5 * KP):
    """VH and VL by the numerical transfer curve at the two extreme inputs (supplies shifted to 0 … vdd − vss)"""
    top = vdd - vss; vh = vtc(0.0, top, vtn, vtp, kn, kp) + vss; vl = vtc(top, top, vtn, vtp, kn, kp) + vss; return vh, vl          # input low → output VH; input high → output VL
@solve('7.5')
def _():
    rows = []
    for tag, vdd, vss in (('(a) VDD = 2.5 V, VSS = 0', 2.5, 0.0), ('(b) VDD = 1.8 V, VSS = 0', 1.8, 0.0), ('(c) VDD = 1 V, VSS = −1 V', 1.0, -1.0)):
        vh, vl = levels(vdd, vss); close(vh, vdd, 1e-6, 1e-6); close(vl, vss, 1e-6, 1e-6); rows.append((tag, f'VH = VDD = {g(vh, 4)} V, VL = VSS = {g(z(vl), 4)} V'))
    return rows, 'In a static CMOS inverter one transistor is always cut off in each logic state, so the output reaches the supply rails: VH = VDD and VL = VSS (−VSS = −1 V means the lower rail is at −1 V). The numerical transfer curve (full square-law model) at the two extreme inputs confirms it.', ['W/L ratios and thresholds do not matter for the levels.'], cir('7.5', 'Fig. P7.5', INV)
def levels_problem(num, cases):
    rows = []
    for tag, vdd, wn, wp in cases:
        vh, vl = levels(vdd, 0.0, 0.6, -0.6, KN * wn, KP * wp); close(vh, vdd, 1e-6, 1e-6); close(vl, 0.0, 1e-6, 1e-6); rows.append((tag, f'VH = {g(vh, 4)} V, VL = {g(z(vl), 4)} V'))
    return rows, 'Static CMOS inverter: VH = VDD and VL = 0 whatever the W/L ratios (one transistor is cut off in each state and the other is in the triode region with zero current); the numerical transfer curve confirms it for these sizes.', ['The W/L ratios are given but do not change VH and VL.'], cir(num, 'Fig. P7.5', INV)
@solve('7.6')
def _(): return levels_problem('7.6', [('(a) VDD = 3.3 V, (W/L)N = 4/1, (W/L)P = 10/1', 3.3, 4, 10), ('(b) (W/L)N = 6/1, (W/L)P = 15/1', 3.3, 6, 15)])
@solve('7.7')
def _(): return levels_problem('7.7', [('(a) VDD = 2.5 V, (W/L)N = 4/1, (W/L)P = 10/1', 2.5, 4, 10), ('(b) (W/L)N = 4/1, (W/L)P = 4/1', 2.5, 4, 4)])
def regions_problem(num, vdd, vt, vmid, vtag):
    rows = []; vl, vh = 0.0, vdd
    for tag, vi, vo in (('(a) vI = VL', vl, vh), ('(b) vI = VH', vh, vl), (f'(c) vI = vO = {vtag} V', vmid, vmid)):
        rn = region(vi, vo, vt); rp = region(vdd - vi, vdd - vo, vt)
        assert rn == region(vi - 0, vo - 0, vt)
        rows.append((tag, f'NMOS (vGS = {g(vi, 4)} V, vDS = {g(vo, 4)} V): {rn}; PMOS (vSG = {g(vdd - vi, 4)} V, vSD = {g(vdd - vo, 4)} V): {rp}'))
    return rows, 'A transistor is cut off if vGS ≤ VT, in the triode region if vDS < vGS − VT and saturated if vDS ≥ vGS − VT (PMOS with the source-referenced magnitudes vSG, vSD, |VTP|). In the static states one transistor is off and the other is in the triode region with vDS = 0.', [], cir(num, 'Fig. P7.5', INV)
@solve('7.8')
def _():
    rows, how, ass, c = regions_problem('7.8', 1.8, 0.45, 1.65, '1.65'); return rows, how, ['Point (c) is just a pair of voltages (the PMOS is cut off there, so it is not a dc operating point of the circuit).'], c
@solve('7.9')
def _(): return regions_problem('7.9', 2.5, 0.6, 1.25, '1.25')
@solve('7.14')
def _():
    rows = []
    for tag, vdd in (('(a) VDD = 3.3 V', 3.3), ('(b) VDD = 2.5 V', 2.5), ('(c) VDD = 1.8 V', 1.8)):
        kn, kp = KN * 5, KP * 1; vt = 0.6
        # vI = VH = VDD: NMOS in triode, PMOS (gate grounded) in saturation while vSD ≥ vSG − |VT| i.e. vO ≤ |VT|
        ip = kp / 2 * (vdd - vt) ** 2; vo = (vdd - vt) - math.sqrt((vdd - vt) ** 2 - 2 * ip / kn); assert vo < vt
        f = lambda v: idn(vdd, v, kn, vt) - (idn(vdd, vdd - v, kp, vt))                             # PMOS: vSG = vdd, vSD = vdd − vO
        vo2 = brentq(f, 1e-9, vdd - 1e-9); close(vo, vo2, 1e-6)
        vh = vdd                                                                              # vI = 0: the NMOS is cut off, the PMOS carries no current: vO = VDD
        assert abs(idn(0.0, 0.0, kn, vt)) < 1e-18
        rows.append((tag, f'VH = {g(vh, 4)} V, VL = {g(vo, 4)} V'))
    return rows, 'Pseudo-NMOS: the PMOS gate is grounded, so it is always on. vI = 0: the NMOS is off and VH = VDD. vI = VDD: the NMOS (Kn = 5·100 μA/V²) is in the triode region and the PMOS (Kp = 40 μA/V², vSG = VDD) is in saturation: ½Kp(VDD − |VTP|)² = Kn[(VDD − VTN)VL − VL²/2], so VL = (VDD − VTN) − √[(VDD − VTN)² − Kp(VDD − |VTP|)²/Kn]. A bisection on the full piecewise model gives the same value.', ['VTN = 0.6 V and VTP = −0.6 V, K′n = 100 and K′p = 40 μA/V² (problem-set defaults).'], cir('7.14', 'Fig. P7.14', 'pseudo-NMOS gate: PMOS MP with its gate grounded (W/L = 1/1) from VDD (= 3.3 V) to the output, NMOS MN (W/L = 5/1) with the input vI from the output to ground.')
@solve('7.22')
def _():
    vdd, vt = 2.5, 0.6; kn, kp = KN * 20, KP * 40                                           # MN2 (20/1) with its gate at 2.5 V, MP1 (40/1) with its gate at 0 V
    f = lambda v: idn(vdd, v, kn, vt) - idn(vdd, vdd - v, kp, vt)
    vo = brentq(f, 1e-9, vdd - 1e-9); I = idn(vdd, vo, kn, vt)
    # second route: both transistors in the triode region -> quadratic in vO
    a, b = vdd - vt, vdd - vt
    g_ = np.poly1d([-kn / 2, kn * a, 0]) - (np.poly1d([kp * b]) * np.poly1d([-1, vdd]) - np.poly1d([kp / 2]) * np.poly1d([-1, vdd]) ** 2)
    roots = [r.real for r in g_.roots if abs(r.imag) < 1e-12 and 0 < r.real < vdd]; v2 = min(roots, key=lambda r: abs(r - vo)); close(v2, vo, 1e-6)
    rn = region(vdd, vo, vt); rp = region(vdd, vdd - vo, vt)
    return [('Output voltage (both outputs tied: MP1 on, MN2 on, MN1 and MP2 off)', f'vO = {g(vo, 4)} V (NMOS: {rn}, PMOS: {rp})'), ('Current from VDD through MP1 and MN2', si(I, 'A', 4))], \
        'Left inverter input 0 V: MP1 (40/1) on, MN1 off; right inverter input 2.5 V: MN2 (20/1) on, MP2 off. The current of MP1 equals that of MN2: Kp[(VDD − |VTP|)(VDD − vO) − (VDD − vO)²/2] = Kn[(VDD − VTN)vO − vO²/2] (both in the triode region), a quadratic in vO; the bisection on the full piecewise model gives the same value, and the current follows from either transistor.', \
        ['K′n = 100, K′p = 40 μA/V², VTN = 0.6 V, VTP = −0.6 V; the NMOS transistors are 20/1 and the PMOS 40/1.'], cir('7.22', 'Fig. P7.22', 'the outputs of two CMOS inverters tied together: left input 0 V (MP1, MN1), right input +2.5 V (MP2, MN2), both between +2.5 V and ground; the current I flows from MP1 through MN2.')
TAU_REF = 1.2 * 1e-12 / (KN * 2 * (2.5 - 0.6))                                              # reference inverter of Fig. 7.12 (2/1, 5/1), 1 pF: 3.158 ns (Eq. 7.15)
def scale_problem(num, tau, c, c2, txt):
    S = TAU_REF * (c / 1e-12) / tau; wn, wp = 2 * S, 5 * S
    t_new = TAU_REF * (c2 / 1e-12) / S
    close(TAU_REF, 3.16e-9, 2e-3)
    from ch07 import delays
    d = delays(2.5, 0.6, -0.6, wn, wp, c, 1.2); close(d[2], tau, 1e-6)                    # τP of the scaled inverter by Eq. (7.15) with the sized transistors
    d2 = delays(2.5, 0.6, -0.6, wn, wp, c2, 1.2); close(d2[2], t_new, 1e-6)
    return [('Scale factor S = (τref/τ′)·(C′/Cref)', f'{g(S, 4)} (τref = {si(TAU_REF, "s", 3)} for 1 pF)'), ('(a) new sizes', f'(W/L)N = {g(wn, 4)}/1, (W/L)P = {g(wp, 4)}/1'), ('(b) delay with the new load', f'τP′ = {si(t_new, "s", 4)} (C = {si(c2, "F", 2)})')], \
        'Performance scaling, Eq. (7.20): τP′ = [(W/L)/(W/L)′]·(C′/Cref)·τref with the reference inverter of Fig. 7.12 ((W/L)N = 2/1, (W/L)P = 5/1, τref = 3.16 ns for 1 pF). The scaled sizes were put back into the delay equation (7.15, 1.2·Ron·C with the new Kn, Kp) and reproduce the target delay. (The book\'s own exercise for 5 pF and 1 ns prints 31.5/1 and 78.8/1; this method gives 31.6/1 and 78.9/1: 0.3 % rounding of τref.)', \
        ['The revised delay estimate (Eq. 7.23, 2.4·Ron·C) would double τref but leaves the scaling rule unchanged only if the reference delay is taken from the same equation; the book\'s reference value 3.16 ns/pF is used.'], cir(num, 'Fig. 7.12', txt)
REFTXT = 'reference inverter: PMOS (W/L = 5/1) above NMOS (W/L = 2/1), gates tied to vI, drains to vO with the load capacitance C; VDD = 2.5 V.'
@solve('7.39')
def _(): return scale_problem('7.39', 0.3e-9, 0.5e-12, 1.5e-12, REFTXT)
@solve('7.40')
def _(): return scale_problem('7.40', 0.4e-9, 2e-12, 3e-12, REFTXT)
SAT = 0.89 / 0.71                                                                           # Table 7.3 (C = 0.2 pF): τP = 0.71 ns without velocity saturation, 0.89 ns for VSAT = 1 V
def resize(num, fig, label, sizes, extra, txt):
    f = SAT * extra
    close(f, 1.2535 * extra, 1e-3)
    rows = [('Delay ratio from Table 7.3', f'τP(VSAT = 1 V)/τP(unlimited) = 0.89/0.71 = {g(SAT, 5)}'), ('Scale factor for the transistors', f'{g(f, 5)} (delay is inversely proportional to W/L)')]
    for name, wl in sizes: rows.append((name, f'{g(wl, 4)}/1 → {g(wl * f, 4)}/1'))
    return rows, 'Table 7.3 (symmetrical inverter of Fig. 7.12 with C = 0.2 pF) gives τP = 0.71 ns without velocity saturation and 0.89 ns with VSAT = 1 V, so every W/L must be multiplied by 0.89/0.71 to recover the same delay (and by a further factor for a shorter delay): τP is inversely proportional to W/L at fixed load (Eq. 7.20). Anchor: the book\'s exercise for the inverter gives 2.51/1 and 6.27/1, reproduced by 2·1.2535 and 5·1.2535.', ['The same factor is applied to every transistor of the circuit (the relative sizes that equalise the on-resistances are kept).'], cir(num, fig, txt)
@solve('7.48')
def _():
    r = resize('7.48', 'Fig. 7.20', 'b/c', [('(b) reference inverter: MN', 2), ('(b) reference inverter: MP', 5), ('(c) NOR gate: each NMOS', 2), ('(c) NOR gate: each PMOS', 10)], 1.0, 'reference inverter (PMOS 5/1, NMOS 2/1) and the two-input NOR gate (series PMOS 10/1, parallel NMOS 2/1), VDD = 2.5 V.')
    close(2 * SAT, 2.51, 2e-3); close(5 * SAT, 6.27, 2e-3); return r[0], r[1], r[2] + ['Fig. 7.20 contains the reference inverter (b) and the two-input NOR gate (c); both are resized.'], r[3]
@solve('7.49')
def _(): return resize('7.49', 'Fig. 7.22', 'nor3', [('each NMOS', 2), ('each PMOS', 15)], 2.0, 'three-input NOR gate: three series PMOS (15/1 each) and three parallel NMOS (2/1 each), load C, VDD = 2.5 V.')
@solve('7.50')
def _(): return resize('7.50', 'Fig. 7.27', 'cmos', [('PMOS A, C, D', 15), ('PMOS B', 7.5), ('NMOS MA', 2), ('NMOS MB, MC, MD', 4)], 3.0, 'complex gate Y = A + BC + BD (CMOS implementation): PMOS 15/1 (A, C, D) and 7.5/1 (B); NMOS MA 2/1, MB, MC, MD 4/1; VDD = 2.5 V.')
