# -*- coding: utf-8 -*-
"""Chuyen doi du lieu A/D va D/A: moi ham co HAI cai dat doc lap (cong thuc dong ↔ mo phong mach/thuat toan) de verify_m10 doi chieu (R2).
Quy uoc theo sach: do phan giai DAC = 1/(2^n - 1) (Floyd 12-3); DAC trong so nhi phan cua Tooley Hinh 3.6a: Vout = -(Vlogic) * sum(b_i * Rf/R_i) voi Rf = R, R_i = R, 2R, 4R, 8R."""
import numpy as np

# ---------- DAC trong so nhi phan (Tooley Hinh 3.6a, Bang 3.1, 3.2) ----------
def dac_weighted_closed(code, n=4, vlogic=5.0):
    """Vout = -vlogic * code / 2^(n-1)  (bit MSB co he so 1, bit tiep theo 1/2, ...)."""
    return -vlogic * code / 2 ** (n - 1)

def dac_weighted_sum(code, n=4, vlogic=5.0, R=1000.0):
    """Cong dong dien: I_i = vlogic*b_i/(2^k R) (k = vi tri tu MSB), Vout = -Rf * sum(I_i), Rf = R."""
    bits = [(code >> (n - 1 - k)) & 1 for k in range(n)]
    I = sum(vlogic * b / (R * 2 ** k) for k, b in enumerate(bits))
    return -R * I

# ---------- DAC thang R-2R (Floyd Hinh 12-29, 12-30) ----------
def dac_r2r_closed(code, n=4, vref=5.0):
    """Vout = -vref * code / 2^n (Floyd: D3 = 1 cho -5 V ... khi Rf = R? Sach: 1000 -> -5 V, 0100 -> -2.5 V, 0010 -> -1.25 V, 0001 -> -0.625 V  => -vref*code/2^(n-1))."""
    return -vref * code / 2 ** (n - 1)

def dac_r2r_nodal(code, n=4, vref=5.0, R=1000.0):
    """Giai he phuong trinh nut cua thang R-2R theo Floyd Hinh 12-29: bit MSB noi qua 2R thang vao nut tong (dat ao, 0 V); cac bit con lai noi qua 2R vao cac nut
    cua thang; nut tong - R - N(n-2) - R - ... - R - N0 - 2R - dat. Rf = 2R (de 1000 -> -vref nhu sach). Ma tran dan nap, giai bang numpy."""
    bits = [(code >> (n - 1 - k)) & 1 for k in range(n)]            # bits[0] = MSB
    m = n - 1                                                        # so nut thang: N_{m-1} ... N_0 (nut 0 = gan op-amp nhat)
    G = np.zeros((m, m)); b = np.zeros(m)
    for k in range(m):
        src = bits[1 + k] * vref                                     # nut k nhan bit bits[1+k]
        G[k, k] += 1 / (2 * R); b[k] += src / (2 * R)                # nhanh 2R toi nguon
        G[k, k] += 1 / R                                             # R ve phia nut tong (k = 0) hoac nut truoc
        if k > 0: G[k, k - 1] -= 1 / R
        if k < m - 1: G[k, k] += 1 / R; G[k, k + 1] -= 1 / R         # R toi nut ke tiep
        else: G[k, k] += 1 / (2 * R)                                 # nut cuoi: 2R xuong dat
    v = np.linalg.solve(G, b)
    i_sum = bits[0] * vref / (2 * R) + v[0] / R                      # dong vao nut tong (0 V)
    return -(2 * R) * i_sum

# ---------- ADC flash ----------
def flash_closed(vin, n=3, vfs=8.0):
    """Nguong tai (k - 0.5) * (vfs/(2^n - 1))? Tooley Hinh 3.9: nguong 0.5, 1.5, ..., 6.5 V (vfs = 7 buoc 1 V): ma = so nguong bi vuot, bao hoa o 2^n - 1."""
    return int(min(max(np.ceil(vin - 0.5), 0), 2 ** n - 1))     # so nguong (k + 0,5) nho hon vin; tai dung nguong: chua vuot (so sanh nghiem ngat)

def flash_comparators(vin, n=3):
    thr = [(k + 0.5) for k in range(2 ** n - 1)]
    outs = [1 if vin > t else 0 for t in thr]
    # bo ma hoa uu tien: chi so cao nhat co ngo ra 1 (k+1), 0 neu khong co
    hi = max([k + 1 for k, o in enumerate(outs) if o], default=0)
    return hi, outs

# ---------- ADC xap xi lien tiep (Floyd Hinh 12-17, 12-18; Tooley Hinh 3.10) ----------
def sar_trace(vin, n=4, weights=None):
    """Thu tung bit tu MSB: bat bit, so DAC voi vin; giu bit neu DAC <= vin. Floyd: trong so 8, 4, 2, 1 V (n = 4)."""
    w = weights or [2 ** (n - 1 - k) for k in range(n)]
    code = 0; steps = []
    for k in range(n):
        trial = code | (1 << (n - 1 - k)); dac = sum(w[j] for j in range(n) if (trial >> (n - 1 - j)) & 1)
        keep = dac <= vin
        steps.append((k + 1, trial, dac, keep))
        if keep: code = trial
    return code, steps

def sar_direct(vin, n=4):
    return int(min(np.floor(vin), 2 ** n - 1))        # voi trong so 8,4,2,1 V va buoc 1 V (xuong gan nhat)

# ---------- thong so ----------
def resolution_pct(n): return 100.0 / (2 ** n - 1)
def levels(n): return 2 ** n
def comparators(n): return 2 ** n - 1
def nyquist_min(fmax): return 2 * fmax
def lsb_pct_fullscale(n): return 100.0 / 2 ** n          # Floyd: LSB cua DAC 8-bit = 0,39 % so voi toan thang
def inv_gain(vin, vout): return -vout / vin

def code_bits(c, n): return format(c, f'0{n}b')
