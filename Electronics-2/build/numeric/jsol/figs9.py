"""Jaeger 5e Chapter 9 (bipolar logic) problems that refer to a figure, solved with the hand-calculation values of the chapter: VBE = 0.7 V, ECL levels from Eqs. (9.12)–(9.18) (output = collector level − VBE of the emitter
follower, ΔV = IEE·RC, VREF centred between VH and VL).  Second route for the ECL levels: KCL with a finite βF = 40 (Table 9.3) instead of neglecting the base currents iB·RC."""
import math
from core import *
from fighelp import cir
BF = 40.0                                                                                   # Table 9.3
def ecl_exact(IEE, RC, If, R1=0.0, beta=BF, vbe=0.7):
    """output levels (VH, VL) of the current switch with emitter followers by KCL with a finite beta: the off transistor's collector resistor carries only the base current ib of its follower,
    the on transistor's carries α·IEE + ib; a common resistor R1 (if any) carries the sum α·IEE + 2·ib; each follower subtracts VBE"""
    a = beta / (beta + 1); ib = If / (beta + 1); v_sh = -R1 * (a * IEE + 2 * ib)
    return v_sh - ib * RC - vbe, v_sh - (a * IEE + ib) * RC - vbe
def ecl_simple(IEE, RC, R1=0.0, vbe=0.7):
    vh = -R1 * IEE - vbe; dv = IEE * RC; return vh, vh - dv, vh - dv / 2, dv
def ecl_rows(num, IEE, RC, R1, vbe, If, fig, txt, extra_rows=None, assume=None):
    vh, vl, vref, dv = ecl_simple(IEE, RC, R1, vbe); eh, el = ecl_exact(IEE, RC, If, R1, vbe=vbe); close(eh - el, dv, 0.06); close(eh, vh, 0.06, 0.02)
    rows = [('VH, VL', f'{g(vh, 4)} V, {g(vl, 4)} V'), ('ΔV = IEE·RC', f'{g(dv, 4)} V'), ('VREF = (VH + VL)/2', f'{g(vref, 4)} V')] + (extra_rows or [])
    return rows, f'Eqs. (9.12)–(9.18): the follower outputs are one VBE below the collector levels. With Q1 off the collector is at 0 V (minus R1·IEE if the common resistor R1 is present), with the current switched in it is IEE·RC lower: VH = −R1·IEE − VBE, VL = VH − IEE·RC, VREF = (VH + VL)/2. Check by KCL with βF = 40 (base currents of the followers included): ΔV = {g(eh - el, 4)} V and VH = {g(eh, 4)} V, i.e. the neglected iB·RC terms are below 6 %.', (assume or []), cir(num, fig, txt)
FIG6 = 'ECL gate with emitter followers: current switch Q1 (input vI), Q2 (base at VREF) with RC = 2 kΩ in each collector and the tail current source IEE = 0.3 mA to −VEE = −5.2 V; emitter followers Q3, Q4 take the outputs vO1 (= Ā) and vO2 from the collectors, each loaded by R = 42 kΩ to −5.2 V.'
@solve('9.8')
def _(): return ecl_rows('9.8', 5e-3, 200.0, 0.0, 0.7, 0.1e-3, 'Fig. 9.6', FIG6 + ' (IEE changed to 5 mA and RC to 200 Ω).', assume=['The follower resistors R = 42 kΩ are unchanged (follower current ≈ 0.1 mA).'])
@solve('9.9')
def _(): return ecl_rows('9.9', 1e-3, 600.0, 0.0, 0.7, 0.3e-3, 'Fig. 9.6', FIG6 + ' (IEE = 1 mA, RC = 600 Ω, follower currents I3 = I4 = 0.3 mA).')
def vbe_rows(num, vbe):
    vh, vl, vref, dv = ecl_simple(0.3e-3, 2e3, 0.0, vbe); eh, el = ecl_exact(0.3e-3, 2e3, 0.1e-3, 0.0, vbe=vbe); close(eh, vh, 0.06, 0.02)
    return [(f'VBE = {vbe} V', f'VOH = {g(vh, 4)} V, VOL = {g(vl, 4)} V, VREF = {g(vref, 4)} V (ΔV = {g(dv, 3)} V unchanged)')]
@solve('9.12')
def _():
    rows = vbe_rows('9.12', 0.85)[:1] + vbe_rows('9.12', 0.95)[:1]
    ra = 5.2 - 0.85; rb = 5.2 - 0.95
    rows += [('Follower resistors for the same 0.1 mA currents (VEE = −5.2 V)', f'R ≈ (VOH + 5.2 V)/0.1 mA: {g((5.2 - 0.85) / 0.1e-3 / 1e3, 4)} kΩ (a) and {g((5.2 - 0.95) / 0.1e-3 / 1e3, 4)} kΩ (b) instead of 42 kΩ (optional)')]
    return rows, 'Same design equations as Prob. 9.8: the output high level is one VBE below the collector level (0 V), VOH = −VBE; the swing ΔV = IEE·RC = 0.6 V and VREF = VOH − ΔV/2 are kept. A larger VBE lowers both levels and VREF by the same amount.', ['The swing 0.6 V (IEE = 0.3 mA, RC = 2 kΩ) of Fig. 9.6 is kept; the supply −5.2 V and R are only touched if the follower current should stay at 0.1 mA (optional).'], cir('9.12', 'Fig. 9.6', FIG6)
P94 = 'current switch: Q1 (input vI) and Q2 (base at VREF) with RC in each collector, a common resistor R1 from ground to the two collector resistors, tail current source IEE to −VEE; emitter followers (as in Fig. 9.6) are added to the two outputs.'
@solve('9.13')
def _():
    IEE, R1, RC, VREF = 0.3e-3, 3.33e3, 2e3, -2.0
    vh, vl, vref, dv = ecl_simple(IEE, RC, R1); eh, el = ecl_exact(IEE, RC, 0.1e-3, R1); close(eh, vh, 0.06, 0.02); close(eh - el, dv, 0.06)
    vih, vil = VREF + dv / 2, VREF - dv / 2; ok = abs(vih - vh) < 0.01 and abs(vil - vl) < 0.01
    return [('(b) VH, VL, ΔV', f'VH = −IEE·R1 − VBE = {g(vh, 4)} V, VL = {g(vl, 4)} V, ΔV = IEE·RC = {g(dv, 3)} V'), ('(c) input levels expected with VREF = −2 V', f'VREF ± ΔV/2 = {g(vih, 4)} V and {g(vil, 4)} V; output levels {g(vh, 4)} V and {g(vl, 4)} V: {"compatible: the outputs equal the input levels" if ok else "not compatible"}')], \
        'With R1 in the common collector path the collector levels are −IEE·R1 (current switched away) and −IEE·R1 − IEE·RC; the emitter followers subtract VBE = 0.7 V. The logic levels sit symmetrically about VREF = −2 V only if VREF = (VH + VL)/2 = −2.0 V, which holds here. KCL check with βF = 40 agrees within 6 %.', ['Part (a) is a drawing (emitter followers on both outputs, as in Fig. 9.6) and is not reproduced.'], cir('9.13', 'Fig. P9.4', P94)
@solve('9.14')
def _():
    IEE, R1, DV = 1.5e-3, 800.0, 0.4; RC = DV / IEE; vh = -IEE * R1 - 0.7; vl = vh - DV; vref = (vh + vl) / 2; eh, el = ecl_exact(IEE, RC, 0.1e-3, R1); close(eh, vh, 0.06, 0.03); close(eh - el, DV, 0.06)
    return [('RC = ΔV/IEE', si(RC, 'Ω', 4)), ('VH, VL, VREF', f'{g(vh, 4)} V, {g(vl, 4)} V, {g(vref, 4)} V')], 'ΔV = IEE·RC gives RC; VH = −IEE·R1 − VBE; VL = VH − ΔV; VREF = (VH + VL)/2. KCL check with βF = 40 agrees within 6 %.', ['Part (a) is a drawing and is not reproduced.'], cir('9.14', 'Fig. P9.4', P94)
@solve('9.81')
def _():
    VCC, RC, VBE, VD, VCES, BETA = 5.0, 1.6e3, 0.7, 0.7, 0.15, 100.0
    IB = (VCC - VBE - VD) / RC; IE_a = (BETA + 1) * IB                                       # (a) RS = 0
    def solve_rs(RS):
        IC_act = BETA * IB; IC_max = (VCC - (VD + VCES)) / RS if RS else float('inf')
        if IC_act <= IC_max: return 'forward active', IC_act + IB
        return 'saturated', IC_max + IB
    mode_b, IE_b = solve_rs(130.0)
    # second route: the collector circuit as a load line, KVL of the whole branch with the output at 0 V (D1 drop VD, transistor VBE or VCEsat)
    VC = VCC - 130 * (IE_b - IB); assert VC >= VD + VCES - 1e-9
    return [('(a) RS = 0, βF = 100', f'IB = (VCC − VBE − VD1)/RC = {si(IB, "A", 4)}, IE = (βF + 1)·IB = {si(IE_a, "A", 4)}'), ('(b) RS = 130 Ω', f'βF·IB = {si(BETA * IB, "A", 4)} would need {g(130 * BETA * IB, 3)} V across RS, so Q4 saturates (VCE = {VCES} V): IC = (VCC − VD1 − VCEsat)/RS = {si(IE_b - IB, "A", 4)}, IE = IC + IB = {si(IE_b, "A", 4)} ({mode_b})')], \
        'With the output shorted to ground the base current is set by RC alone: IB = (5 − 0.7 − 0.7)/1.6 kΩ. Without RS the transistor is forward active: IE = (βF + 1)IB. With RS = 130 Ω the collector current cannot exceed (VCC − VD − VCEsat)/RS, so the transistor saturates and the emitter current is limited to that value plus IB. KVL around the collector branch checks that VC stays above VD1 + VCEsat.', ['VBE = VD1 = 0.7 V, VCEsat = 0.15 V (Table 9.3); the output short circuit holds vO = 0 V.'], cir('9.81', 'Fig. P9.81', 'TTL totem-pole output stage: VCC = +5 V; RC = 1.6 kΩ to the base of Q4 and RS = 130 Ω to its collector; emitter of Q4 through diode D1 to the output vO, which sinks the load current iL (here shorted to ground).')
@solve('9.99')
def _():
    iBB, iCC, BF_, BR = 250e-6, 1e-3, 20.0, 2.0
    # KCL: base node iBB = iD1 + iD2; collector node iC = iCC + iD1; iD2 = iB = iC/βF (edge of saturation, D1 diverts the excess base drive)
    iD1 = (iBB - iCC / BF_) / (1 + 1 / BF_); iC = iCC + iD1; iD2 = iBB - iD1; close(iD2, iC / BF_, 1e-9)
    return [('Collector-emitter voltage (identical diodes)', 'vCE = vBE + vD2 − vD1 = vBE ≈ 0.7 V: the base-collector junction stays at about 0 V, so the transistor is not saturated'), ('iD1', si(iD1, 'A', 4)), ('iD2 = iB', si(iD2, 'A', 4)), ('iC = iCC + iD1', si(iC, 'A', 4))], \
        'Baker clamp: D2 feeds the base, D1 returns the excess base drive to the collector. KCL at the base node: iBB = iD1 + iD2; at the collector node: iC = iCC + iD1; the transistor stays at the edge of the forward-active region, iB = iD2 = iC/βF. Solving gives iD1 = (iBB − iCC/βF)/(1 + 1/βF). The loop vCE = vBE + vD2 − vD1 gives 0.7 V for identical diodes.', ['Ideal identical diodes and forward-active operation (βR = 2 is not needed).'], cir('9.99', 'Fig. P9.99', 'Baker clamp: current source iBB into the node joined to the base through diode D2 and to the collector through diode D1; current source iCC into the collector; emitter grounded.')
@solve('9.102')
def _():
    VEE, RC, RE, VBE, VD = 3.0, 3.3e3, 2.4e3, 0.7, 0.4; VH = 0.0
    # VL: QR on; the Schottky diode clamps the collector at VREF − VD when RC·IC would pull it lower; VREF centred: VREF = (VH + VL)/2
    IE = lambda vref: (vref - VBE + VEE) / RE
    VREF = -VD; VL = VREF - VD; ie = IE(VREF); assert VL > -ie * RC                           # the unclamped swing would be IE·RC = 2.6 V: the clamp is active
    return [('Logic function', 'Y = A + B + C (OR): Y is the collector of QR, which is off (Y = 0 V) when any input transistor is on'), ('VH', '0 V (QR off, no current in RC)'), ('VL', f'{g(VL, 3)} V: the Schottky diode clamps the collector of QR at VREF − VD (without the clamp RC would drop {g(ie * RC, 3)} V)'), ('VREF = (VH + VL)/2', f'{g(VREF, 3)} V')], \
        'The three input transistors and QR share the emitter resistor RE; with all inputs low QR conducts and the collector level would be −IE·RC (IE = (VREF − VBE + VEE)/RE), far below VREF, so the Schottky diode clamps it at VREF − VD. With VREF centred between the levels, VREF = VL/2 and VL = VREF − VD give VREF = −VD = −0.4 V and VL = −0.8 V; then IE = 0.79 mA, so the clamp is indeed active.', ['VREF is taken centred between VH and VL as in Eq. (9.18a) (the statement does not say how VREF is chosen).'], cir('9.102', 'Fig. P9.102', 'ECL OR gate: input transistors A, B, C (collectors to ground) and the reference transistor QR (Schottky-clamped, base at VREF, collector Y through RC to ground) with emitters tied to RE and −VEE.')
@solve('9.103')
def _():
    VBE, R, VCC = 0.7, 4e3, 5.0
    iin = (VCC - VBE) / R; iB = iin / (BF + 1); iC = BF * iB
    # second route: the Schottky diode (0.45 V) forces VCE = VBE − 0.45 = 0.25 V; the external collector current is zero, so all of iC comes through the diode
    vce = VBE - 0.45; assert vce > 0.15                                                       # above VCEsat: the transistor stays forward active
    close(iB + iC, iin, 1e-12)
    return [('Current from the 4 kΩ resistor', si(iin, 'A', 4)), ('iB', si(iB, 'A', 4)), ('iC (through the Schottky diode)', si(iC, 'A', 4)), ('Check', f'VCE = VBE − VSchottky = {g(vce, 3)} V > VCEsat = 0.15 V: forward active')], \
        'With the external collector open the whole collector current is supplied through the Schottky diode from the base node, so the current from the resistor splits as iin = iB + iC = (βF + 1)iB with βF = 40 (Table 9.3) and iin = (5 − 0.7)/4 kΩ.', ['βF = 40 and VBE = 0.7 V (Table 9.3) are used; the Schottky forward voltage is 0.45 V as given.'], cir('9.103', 'Fig. P9.103', 'Schottky-clamped transistor Q1: the base is fed from +5 V through 4 kΩ, the emitter is grounded and the external collector terminal is open (i = 0).')
# ---- power-delay product, graph of Fig. 9.51 (points read from the vector drawing: 74LS at 2 mW, 10 ns; ECL 100K at 40 mW, 0.7 ns; axes 0.1 … 100 mW and 0.1 … 100 ns) ----
P74LS, T74LS, P100K, T100K = 2e-3, 10e-9, 40e-3, 0.7e-9
G951 = 'power-delay graph: propagation delay 0.1–100 ns against power dissipation 0.1–100 mW (log axes) with lines of constant PDP (50 pJ, 1 pJ, 100 fJ) and points for the logic families (74LS: 2 mW, 10 ns; ECL 100K: about 40 mW, 0.7 ns); the gate on the left is the Schottky TTL gate.'
def pdp_prob(num, P, N, tau, tag):
    pg = P / N; pdp = pg * tau; low = 0.1e-3 * 0.1e-9
    return [(f'(a) power per gate = {si(P, "W", 3)}/{N:g}', si(pg, 'W', 3)), ('(a) power-delay product = P·τ', si(pdp, 'J', 3)), ('(b) lowest PDP on the graph (lower left corner: 0.1 mW × 0.1 ns)', si(low, 'J', 3)), ('Comparison', f'the required PDP is {"below" if pdp < low else "above"} the lowest value that can be plotted (ratio {g(pdp / low, 3)})')], 'PDP = (chip power/number of gates) × delay; the corner of the graph of Fig. 9.51 (0.1 mW, 0.1 ns) gives the smallest plottable PDP, 10 fJ (axes read from the vector drawing).', ['The graph limits (0.1 mW … 100 mW, 0.1 ns … 100 ns) are read from the axis labels of Fig. 9.51.'], cir(num, 'Fig. 9.51', G951)
@solve('9.104')
def _(): return pdp_prob('9.104', 50.0, 50e6, 1e-9, 'a')
@solve('9.105')
def _(): return pdp_prob('9.105', 100.0, 250e6, 0.25e-9, 'a')
@solve('9.107')
def _():
    pdp = P74LS * T74LS; t = pdp / 5e-3; P = pdp / 0.3e-9
    return [('PDP of the 74LS gate read from Fig. 9.51', f'{si(P74LS, "W", 2)} × {si(T74LS, "s", 2)} = {si(pdp, "J", 3)}'), ('(a) delay at 5 mW (constant PDP)', si(t, 's', 3)), ('(b) power for a 0.3 ns delay', si(P, 'W', 3))], 'Constant power-delay product: τ = PDP/P. The 74LS point of Fig. 9.51 was read from the vector drawing (log interpolation between the axis labels: 1.99 mW, 10.0 ns).', ['Reading of the graph: about 2 mW and 10 ns for 74LS (±3 %).'], cir('9.107', 'Fig. 9.51', G951)
@solve('9.108')
def _():
    pdp = P100K * T100K; t = pdp / 10e-3; P = pdp / 0.2e-9
    return [('PDP of the ECL 100K gate read from Fig. 9.51', f'{si(P100K, "W", 2)} × {si(T100K, "s", 2)} = {si(pdp, "J", 3)}'), ('(a) delay at 10 mW (constant PDP)', si(t, 's', 3)), ('(b) power for a 0.2 ns delay', si(P, 'W', 3))], 'Constant power-delay product: τ = PDP/P. The ECL 100K point of Fig. 9.51 was read from the vector drawing (39.6 mW, 0.70 ns).', ['Reading of the graph: about 40 mW and 0.7 ns for ECL 100K (±3 %).'], cir('9.108', 'Fig. 9.51', G951)
