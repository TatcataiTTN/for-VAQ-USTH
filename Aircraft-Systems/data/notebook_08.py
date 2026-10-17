# -*- coding: utf-8 -*-
import nbformat as nbf, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebooks"); os.makedirs(OUT, exist_ok=True)
md = nbf.v4.new_markdown_cell; code = nbf.v4.new_code_cell
cells = [
md("""# Module 08: Cáp quang trên máy bay / Fibre Optics in Aircraft
**AE2.021 · USTH**

🇻🇳 Notebook tính lại bốn bài tập của bài giảng (slide 20, 22, 27, 36), đối chiếu đáp án in ở slide 36, kiểm tra các điểm không khớp (θc và θa, ε_r của nước, Δt giữa các mode), mô phỏng Snell/TIR và chạy lại 20 câu Tooley chương 10 (khoá đáp án đọc từ ảnh scan A.10, tr.379-380).

🇬🇧 This notebook recomputes the four lecture exercises (slides 20, 22, 27, 36), compares the printed answer on slide 36, checks the mismatches (θc versus θa, water ε_r, inter-mode Δt), simulates Snell/TIR and re-runs the 20 Tooley chapter 10 questions (key read from the scanned image A.10, p.379-380)."""),
md("## 1. Công thức nền / Core formulas"),
code("""import math
deg = math.degrees; rad = math.radians
def theta_c(n1, n2): return deg(math.asin(n2 / n1))
def NA(n1, n2): return math.sqrt(n1**2 - n2**2)
def theta_a(na, n0=1.0): return deg(math.asin(na / n0))
def V(d_um, na, lam_nm): return math.pi * d_um * 1e-6 * na / (lam_nm * 1e-9)
def modes(v): return v * v / 2
def lmax_km(pin_mW, pmin_uW, a_dBkm): return 10 * math.log10(pin_mW * 1000 / pmin_uW) / a_dBkm

# Snell: kinh -> khong khi voi theta_i = 30 do: bi be RA XA phap tuyen (Tooley 10.2 viet nguoc)
s = 1.5 * math.sin(rad(30)) / 1.0
print("theta_r =", round(deg(math.asin(s)), 2), "do  > 30: be ra xa phap tuyen")
assert deg(math.asin(s)) > 30

# Tooley TYU 10.2 / slide 32: kinh-khong khi
print("theta_c kinh-khong khi =", round(theta_c(1.5, 1.0), 2))
assert abs(theta_c(1.5, 1.0) - 41.81) < 0.01
# Tooley Q7: theta_a = 45 do -> NA = 0.707
assert abs(math.sin(rad(45)) - 0.7071) < 1e-3"""),
md("## 2. Bài tập slide 20, 22, 27 / Exercises on slides 20, 22, 27"),
code("""n1, n2 = 1.53, 1.50
print("S20: theta_c =", round(theta_c(n1, n2), 2), " NA =", round(NA(n1, n2), 4), " theta_a =", round(theta_a(NA(n1, n2)), 2))
assert abs(theta_c(n1, n2) - 78.64) < 0.01 and abs(NA(n1, n2) - 0.3015) < 1e-4 and abs(theta_a(NA(n1, n2)) - 17.55) < 0.01
# theta_c va theta_a KHONG bang nhau nhu slide 19 viet 'theta1 = theta_c = theta_a'
assert abs(theta_c(n1, n2) - theta_a(NA(n1, n2))) > 60

v = V(62.5, 0.275, 1300)
print("S22: V =", round(v, 2), " N =", round(modes(v)), " theta_a =", round(theta_a(0.275), 2))
assert abs(v - 41.54) < 0.01 and round(modes(v)) == 863 and abs(theta_a(0.275) - 15.96) < 0.01

print("S27: Lmax =", round(lmax_km(1, 50, 0.35), 2), "km (0,35 dB/km),", round(lmax_km(1, 50, 0.18), 2), "km (0,18 dB/km),", round(lmax_km(1, 50, 2.0), 2), "km (2 dB/km, Tooley)")
assert abs(lmax_km(1, 50, 0.35) - 37.17) < 0.01"""),
md("## 3. Bài tập slide 36 và đáp án in / Slide 36 and its printed answer"),
code("""NA_, lam, M = 0.20, 850e-9, 1000
Vs = math.sqrt(2 * M); a = Vs * lam / (2 * math.pi * NA_); d_um = 2 * a * 1e6
print("d =", round(d_um, 2), "um  (in tren slide: 60.49)")
rows = {}
for l in (1320e-9, 1550e-9):
    v2 = 2 * math.pi * a * NA_ / l; rows[l] = (v2, v2 * v2 / 2); print(f"{l*1e9:.0f} nm: V = {v2:.2f}, M = {v2*v2/2:.1f}")
assert abs(d_um - 60.49) < 0.02
assert abs(rows[1320e-9][0] - 28.78) < 0.05 and abs(rows[1320e-9][1] - 414) < 1.0
assert abs(rows[1550e-9][0] - 24.51) < 0.05 and abs(rows[1550e-9][1] - 301) < 1.0
print("Khop dap an in tren slide 36 trong sai so lam tron.")"""),
md("## 4. Các điểm không khớp / Mismatches"),
code("""# (a) Slide 9: nuoc co eps_r ~ 80 nhung n ~ 1.33 -> sqrt(80) khong phai 1.33
print("sqrt(80) =", round(math.sqrt(80), 2), " ; 1.33^2 =", round(1.33**2, 2), "(eps_r o tan so anh sang)")
assert abs(math.sqrt(80) - 1.33) > 7 and abs(1.33**2 - 1.77) < 0.01

# (b) Slide 28: dt ~ (n1-n2)L/c va 'dien hinh 10-50 ns/km'
c = 3e8
for n1_, n2_ in ((1.48, 1.46), (1.50, 1.46), (1.46, 1.457), (1.46, 1.445)):
    slide = (n1_ - n2_) / c * 1e3 * 1e9            # ns/km theo cong thuc slide
    exact = n1_ * (n1_ - n2_) / (c * n2_) * 1e3 * 1e9  # tia toi han: L/sin(theta_c) - L
    print(f"n1={n1_} n2={n2_}: slide {slide:6.1f} ns/km, chinh xac {exact:6.1f} ns/km")
assert 60 < (1.48 - 1.46) / c * 1e12 < 70           # 0.02 -> ~67 ns/km, ngoai 10-50
# de ra 10-50 ns/km can n1-n2 khoang 0.003..0.015:
print("n1-n2 cho 10 ns/km:", 10e-9 * c / 1e3, "; cho 50 ns/km:", 50e-9 * c / 1e3)

# (c) dB/km <-> Np/km
alpha_np_km = 0.35 / (10 / math.log(10)); print("alpha =", round(alpha_np_km, 4), "Np/km")
assert abs(0.35 / alpha_np_km - 4.343) < 1e-3
print("20 dB mat cong suat =", 10 ** (-20 / 10), "lan")"""),
md("## 5. Khoá Tooley chương 10 / Tooley chapter 10 key"),
code("""KEY = dict(zip(range(1, 21), "b c a c a c b c a a c b b b c a c c b a".split()))   # A.10: tr.379 (1-10) va tr.380 (11-20)
assert len(KEY) == 20
assert KEY[7] == "b"          # NA = sin 45 = 0.707 -> lua chon (b)
assert KEY[13] == "b"         # goc toi han: tia di doc theo bien
assert KEY[16] == "a"         # suy hao < 2 dB/km
# Nhat quan voi tinh toan: NA = 1 <=> theta_a = 90 do (Q9 = a)
assert abs(theta_a(1.0) - 90) < 1e-9 and KEY[9] == "a"
# Tooley 10.4.2: 6 dau noi x 0.5 dB = 3 dB
assert 6 * 0.5 == 3
print("Khoa 20/20 doc tu anh scan; cac cau tinh duoc deu khop.")"""),
md("""#### 📤 Nhận xét / Takeaway
🇻🇳 Bài slide 36 khớp đáp án in trong sai số làm tròn. Bài slide 20, 22, 27 chưa có đáp án in nên đã giải và kiểm. Có 7 điểm không khớp trong tài liệu (θc và θa ở slide 19, ε_r của nước, công thức và con số Δt ở slide 28, nhãn MM-SI, suy hao 0,2 đến 0,5 so với 0,18, Tooley 10.2 viết ngược quy tắc khúc xạ, và nhãn máy bay ở slide 6).

🇬🇧 The slide 36 exercise matches its printed answer within rounding. Slides 20, 22, 27 had no printed answer, so they were solved and checked. Seven mismatches in the material: θc versus θa on slide 19, water ε_r, the Δt formula and numbers on slide 28, the MM-SI label, 0.2 to 0.5 versus 0.18 dB/km, Tooley 10.2's reversed refraction rule, and the aircraft label on slide 6."""),
]
nb = nbf.v4.new_notebook(); nb["cells"] = cells
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3"}}
nbf.write(nb, os.path.join(OUT, "08_fibre-optics.ipynb")); print("wrote")
