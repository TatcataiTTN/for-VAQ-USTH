# -*- coding: utf-8 -*-
"""Ban dich EN cho notebook cu 07, 08, 09 (cau truc nhu legacy_en_a.py)."""
from legacy_en_a import D
D['07'] = dict(
 md={
  0: "# Module 07: Aircraft Software Control\n**AE2.021 · USTH**\n\nThis notebook rewrites the 8-bit checksum and CRC-8 in code, reproduces Floyd Example 2-41, tries three error types (bit flip, swap, cancelling errors), simulates the FLS/DFLD release decision from Tooley 13.3.3, checks the level A to E numbers and cross-checks Tooley's printed chapter 13 answer key (read directly from the scanned Appendix 3 image, A.13, page 380).",
  1: "## 1. 8-bit checksum and CRC-8", 3: "## 2. Three error types", 5: "## 3. Floyd Example 2-41", 7: "## 4. FLS/DFLD release decision (Tooley 13.3.3)", 9: "## 5. Levels A to E", 11: "## 6. Tooley Ch.13 answer key",
  13: "#### 📤 Takeaway\nAll computed numbers agree. The checksum misses every swap and cancelling errors; CRC-8 caught all three error types tested, but a CRC can also miss other errors (not absolute). The lecture's printed answer to question 13-6 omits the second red arrow of Figure 13-1.",
 },
 code=[
  ("# Gia tri chuan cua CRC-8 (poly 0x07) tren chuoi ASCII '123456789' la 0xF4", "# Standard CRC-8 value (poly 0x07) of the ASCII string '123456789' is 0xF4"), ("# cung tep voi Demo 1 tren trang", "# same file as Demo 1 on the page"), ("Tra ve giay to di kem theo Tooley 13.3.3.", "Return the release document accompanying the item per Tooley 13.3.3."), ("# cau tu sinh cua module", "# generated question of the module"),
  ('"lat 1 bit"', '"flip 1 bit"'), ('"doi cho 2 byte"', '"swap 2 bytes"'), ('"hai loi triet tieu"', '"two cancelling errors"'), ("# checksum 'mu' voi doi cho", "# the checksum is 'blind' to swaps"),
  ("# Mo rong: CRC-8 co bat duoc MOI loi 1 bit va moi loi 2 byte doi cho khac nhau khong? (thu toan bo)", "# Extension: does CRC-8 catch EVERY 1-bit error and every swap of 2 different bytes? (exhaustive test)"),
  ("loi 1 bit CRC bo sot:", "1-bit errors missed by CRC:"), ('"tren", len(data)', '"out of", len(data)'),
  ("cap doi cho (byte khac nhau) CRC-8 bo sot:", "swapped pairs (different bytes) missed by CRC-8:"), ("- checksum bo sot TAT CA cac cap do", "- the checksum misses ALL of those pairs"),
  ("# Floyd them 4 so 0 (bang so bit cua G)", "# Floyd appends 4 zeros (the number of bits of G)"), ('print("du:", rem)', 'print("remainder:", rem)'), ("# '100' voi 3 bit cuoi; Floyd viet 0100 (4 bit)", "# '100' with the last 3 bits; Floyd writes 0100 (4 bits)"),
  ("ma truyen:", "transmitted code:"), ("# ben nhan chia lai duoc du 0", "# the receiver divides again and gets remainder 0"), ("# Phien ban CRC chuan chi them len(G)-1 = 3 so 0:", "# The standard CRC version appends only len(G)-1 = 3 zeros:"),
  ("CRC chuan (3 so 0):", "Standard CRC (3 zeros):"), ("-> ma truyen", "-> transmitted code"), ("# Parity (Floyd Bang 2-8): bit chan cho BCD 0111 la 1", "# Parity (Floyd Table 2-8): the even-parity bit for BCD 0111 is 1"),
  ("(khong the cap Form 1 hoac 8130-3)", "(Form 1 or 8130-3 cannot be issued)"), ("EASA Form 1 hoac FAA 8130-3", "EASA Form 1 or FAA 8130-3"), ("QUARANTINE (khong thu truyen)", "QUARANTINE (do not transfer)"), ('"co the nap"', '"can be loaded"'),
  ("Quy tac phat hanh va cach ly: OK", "Release and quarantine rules: OK"), ("# (min, max) xac suat/gio bay, Tooley bang 13.1", "# (min, max) probability per flight hour, Tooley table 13.1"),
  ("# So trace bat buoc theo hinh 13-1: do (A) 2, tim (A,B,C) 3, xanh (A-D) 3 mui ten nhom", "# Mandatory number of traces per figure 13-1: red (A) 2, purple (A,B,C) 3, green (A-D) 3 group arrows"),
  ("(bang 13.1)", "(table 13.1)"), ("(bang 13.2)", "(table 13.2)"),
  ("# Cau co the tu kiem:", "# Questions that can be self-checked:"), ("# radar thoi tiet = Class D (bang 13.2), la lua chon (c)", "# weather radar = Class D (table 13.2), is option (c)"), ("# OSS va UMS la lop cua FLS", "# OSS and UMS are classes of FLS"),
  ("# buoc cuoi nap EEC la kiem chung", "# the final step of loading the EEC is verification"),
  ("Khop 5/5 cau tu kiem duoc; cau 1 va 3 la cau dinh nghia (c) va (c) theo van ban Tooley 13.1-13.2.", "5/5 self-checkable questions match; questions 1 and 3 are definition questions (c) and (c) per the text of Tooley 13.1-13.2."),
 ])
D['08'] = dict(
 md={
  0: "# Module 08: Fibre Optics in Aircraft\n**AE2.021 · USTH**\n\nThis notebook recomputes the four lecture exercises (slides 20, 22, 27, 36), compares the printed answer on slide 36, checks the mismatches (θc versus θa, water ε_r, inter-mode Δt), simulates Snell/TIR and re-runs the 20 Tooley chapter 10 questions (key read from the scanned image A.10, p.379-380).",
  1: "## 1. Core formulas", 3: "## 2. Exercises on slides 20, 22, 27", 5: "## 3. Slide 36 and its printed answer", 7: "## 4. Mismatches", 9: "## 5. Tooley chapter 10 key",
  11: "#### 📤 Takeaway\nThe slide 36 exercise matches its printed answer within rounding. Slides 20, 22, 27 had no printed answer, so they were solved and checked. Seven mismatches in the material: θc versus θa on slide 19, water ε_r, the Δt formula and numbers on slide 28, the MM-SI label, 0.2 to 0.5 versus 0.18 dB/km, Tooley 10.2's reversed refraction rule, and the aircraft label on slide 6.",
 },
 code=[
  ("# Snell: kinh -> khong khi voi theta_i = 30 do: bi be RA XA phap tuyen (Tooley 10.2 viet nguoc)", "# Snell: glass -> air with theta_i = 30 deg: the ray bends AWAY from the normal (Tooley 10.2 states it backwards)"),
  ('"do  > 30: be ra xa phap tuyen"', '"deg  > 30: bends away from the normal"'), ("# Tooley TYU 10.2 / slide 32: kinh-khong khi", "# Tooley TYU 10.2 / slide 32: glass-air"), ("theta_c kinh-khong khi =", "theta_c glass-air ="),
  ("# Tooley Q7: theta_a = 45 do -> NA = 0.707", "# Tooley Q7: theta_a = 45 deg -> NA = 0.707"),
  ("# theta_c va theta_a KHONG bang nhau nhu slide 19 viet 'theta1 = theta_c = theta_a'", "# theta_c and theta_a are NOT equal, unlike slide 19 which writes 'theta1 = theta_c = theta_a'"),
  ("um  (in tren slide: 60.49)", "um  (printed on the slide: 60.49)"), ("Khop dap an in tren slide 36 trong sai so lam tron.", "Matches the answer printed on slide 36 within rounding error."),
  ("# (a) Slide 9: nuoc co eps_r ~ 80 nhung n ~ 1.33 -> sqrt(80) khong phai 1.33", "# (a) Slide 9: water has eps_r ~ 80 but n ~ 1.33 -> sqrt(80) is not 1.33"), ("(eps_r o tan so anh sang)", "(eps_r at optical frequencies)"),
  ("# (b) Slide 28: dt ~ (n1-n2)L/c va 'dien hinh 10-50 ns/km'", "# (b) Slide 28: dt ~ (n1-n2)L/c and 'typically 10-50 ns/km'"), ("# ns/km theo cong thuc slide", "# ns/km by the slide's formula"), ("# tia toi han: L/sin(theta_c) - L", "# critical ray: L/sin(theta_c) - L"),
  ("slide {slide:6.1f} ns/km, chinh xac {exact:6.1f} ns/km", "slide {slide:6.1f} ns/km, exact {exact:6.1f} ns/km"), ("# 0.02 -> ~67 ns/km, ngoai 10-50", "# 0.02 -> ~67 ns/km, outside 10-50"),
  ("# de ra 10-50 ns/km can n1-n2 khoang 0.003..0.015:", "# to get 10-50 ns/km needs n1-n2 of about 0.003..0.015:"), ("n1-n2 cho 10 ns/km:", "n1-n2 for 10 ns/km:"), ("; cho 50 ns/km:", "; for 50 ns/km:"),
  ("20 dB mat cong suat =", "20 dB power loss ="), ('(-20 / 10), "lan")', '(-20 / 10), "times")'),
  ("# A.10: tr.379 (1-10) va tr.380 (11-20)", "# A.10: p.379 (1-10) and p.380 (11-20)"), ("# NA = sin 45 = 0.707 -> lua chon (b)", "# NA = sin 45 = 0.707 -> option (b)"), ("# goc toi han: tia di doc theo bien", "# critical angle: the ray travels along the boundary"),
  ("# suy hao < 2 dB/km", "# attenuation < 2 dB/km"), ("# Nhat quan voi tinh toan: NA = 1 <=> theta_a = 90 do (Q9 = a)", "# Consistent with the calculation: NA = 1 <=> theta_a = 90 deg (Q9 = a)"), ("# Tooley 10.4.2: 6 dau noi x 0.5 dB = 3 dB", "# Tooley 10.4.2: 6 connectors x 0.5 dB = 3 dB"),
  ("Khoa 20/20 doc tu anh scan; cac cau tinh duoc deu khop.", "Key 20/20 read from the scan image; all the computable questions match."),
 ])
D['09'] = dict(
 md={
  0: "# Module 09: EMC in Aircraft\n**AE2.021 · USTH**\n\nThis notebook recomputes every dB, dBm and cascade number in the lecture (slides 13 to 21), catches the 10 kW versus 100 kW error on slide 21, verifies the square-wave Fourier series, the real capacitor (ESL, ESR, f_r), Tooley's spectrum examples, Floyd's noise margins and Tooley's chapter 14 key (read from the scanned image A.14, p.381).",
  1: "## 1. dB and dBm", 3: "## 2. Exercises on slides 20 and 21", 5: "## 3. Square wave and spectrum", 7: "## 4. A real capacitor", 9: "## 5. Tooley and Floyd numbers", 11: "## 6. Tooley Ch.14 key",
  13: "#### 📤 Takeaway\nEvery dB figure agrees, except the 10 kW result box on slide 21 (it should be 100 kW). In the V/n series V must be read as the fundamental amplitude (the real square-wave amplitude is π/4 times the series sum). A 26 dB rise in the noise floor is about 20 times in amplitude, not 50. The two bonding resistance thresholds (slides 43 and 45) conflict and the tester picture on slide 45 itself fails.",
 },
 code=[
  ("# slide 13: ba vi du", "# slide 13: three examples"), ("# slide 14-15: bang ti so", "# slide 14-15: ratio table"), ("# slide 17: bai tap", "# slide 17: exercise"), ("# slide 19: bang dBm", "# slide 19: dBm table"), ("# 0 dBm = 1 mW, khong phai 0 W", "# 0 dBm = 1 mW, not 0 W"),
  ("# slide 20: noi tang", "# slide 20: cascade"), ("# slide in nham '10000 W (10 kW)'", "# the slide misprints '10000 W (10 kW)'"), ("Loi tren slide 21: ket qua in 10000 W khac 100000 W cua chinh phep tinh.", "Error on slide 21: the printed result 10000 W differs from the 100000 W of its own calculation."),
  ("# Hai bac 1 cua day V/n co bien do 4/pi * V_vuong: kiem tra gia tri tren plateau", "# The first harmonic (n=1) of the V/n series has amplitude 4/pi * V_square: check the value on the plateau"), ("# Tooley TYU 14.1: 50 V, 2 kHz -> hai bac 5", "# Tooley TYU 14.1: 50 V, 2 kHz -> fifth harmonic"), ("# giua nua chu ky duong", "# middle of the positive half-cycle"),
  ("gia tri plateau cua chuoi V/n =", "plateau value of the V/n series ="), ("# => bien do song vuong that = (pi/4) * V, nghia la hai co ban = 4V_sq/pi", "# => the real square-wave amplitude = (pi/4) * V, meaning the fundamental = 4V_sq/pi"),
  ("# Tooley hinh 14.9: ba bac 3 thap hon co ban 70 dB", "# Tooley figure 14.9: the third harmonic is 70 dB below the fundamental"), ("# tren f_r: cam khang cua cuon cam chiem uu the", "# above f_r: the inductive reactance of the inductance dominates"), ("# tu 1 nF co f_r cao hon nhieu", "# the 1 nF capacitor has a much higher f_r"),
  ("# Tooley hinh 14.14: san nhieu tang tu -110 den -84 dB = 26 dB; sach viet '50 lan'", "# Tooley figure 14.14: the noise floor rises from -110 to -84 dB = 26 dB; the book writes '50 times'"),
  ('"tang",d,"dB ->"', '"rise",d,"dB ->"'), ('"lan bien do,"', '"times in amplitude,"'), ('"lan cong suat"', '"times in power"'), ("# khong phai 50 lan", "# not 50 times"),
  ("# Tooley 14.3: phan tich pho: bien do hai con tro -26 dBm tai 121 MHz, san nhieu -95 dBm => 69 dB tren san nhieu", "# Tooley 14.3: spectrum analysis: marker amplitude -26 dBm at 121 MHz, noise floor -95 dBm => 69 dB above the noise floor"),
  ("# CISPR 11 (slide 26): doi dBuV/m sang uV/m", "# CISPR 11 (slide 26): convert dBuV/m to uV/m"), ("# Floyd Ch.15 Bai 3 va vi du 15-1 (CMOS 5 V)", "# Floyd Ch.15 Problem 3 and example 15-1 (CMOS 5 V)"),
  ("# nguon: bo loc thong thap", "# power supply: low-pass filter"), ("# dong cat nhanh va dong lon", "# fast-switching and large currents"), ("# bien do theo tan so", "# amplitude versus frequency"), ("# < 0.005 ohm (Tooley 14.6 noi < 0.001-0.003 ohm)", "# < 0.005 ohm (Tooley 14.6 says < 0.001-0.003 ohm)"),
  ("# Cac nguong lien ket: slide 43 (0.001-0.003), slide 45 (<2.5 mohm, tester 0.003 ohm), Tooley Q6 (<0.005)", "# Bonding thresholds: slide 43 (0.001-0.003), slide 45 (<2.5 mohm, tester 0.003 ohm), Tooley Q6 (<0.005)"),
  ("ohm  > gioi han slide 45", "ohm  > limit of slide 45"), ('"KHONG DAT theo chinh slide"', '"FAILS by the slide itself"'), ('else "dat")', 'else "passes")'), ("Khoa 9/9 doc tu anh scan.", "Key 9/9 read from the scan image."),
 ])
