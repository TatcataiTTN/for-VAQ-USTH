# -*- coding: utf-8 -*-
"""Sinh notebook 06_electronic-displays.ipynb (chi file nay, khong dong cham 5 notebook cu)."""
import nbformat as nbf, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebooks")
os.makedirs(OUT, exist_ok=True)
def md(t): return nbf.v4.new_markdown_cell(t)
def code(t): return nbf.v4.new_code_cell(t)

cells = [
md("""# Module 06: Màn hình điện tử / Electronic Displays
**AE2.021 · USTH: Aircraft Digital Electronic & Computer Systems**

🇻🇳 Notebook này tính lại bằng code các con số của module: kích thước điểm ảnh theo thị lực, tần số quét raster, giải mã 7 đoạn (kèm các biểu thức tối giản của Floyd bằng sympy), mô phỏng zero suppression của 74HC47, và kiểm tra các con số trên slide ECAM (nhiên liệu, chênh áp ISA, thời gian đến điểm bay). Cuối notebook đối chiếu khoá đáp án in của Tooley (đọc trực tiếp từ ảnh scan Appendix 3) với các câu tính được.

🇬🇧 This notebook recomputes the module's numbers in code: pixel size from visual acuity, raster scan frequencies, 7-segment decoding (with Floyd's minimal expressions via sympy), a 74HC47 zero-suppression simulation, and checks of the numbers on the ECAM slides (fuel, ISA differential pressure, time to waypoint). It ends by cross-checking Tooley's printed answer key (read directly from scanned Appendix 3 images) against the questions that can be computed."""),

md("""## 1. Thị lực và kích thước điểm ảnh / Visual acuity and pixel size
🎯 **Trả lời câu hỏi gì?** Ở khoảng cách D, điểm ảnh nhỏ cỡ nào thì mắt người không còn phân biệt được (slide 5 và 6 của bài giảng)."""),
code("""import math
theta = (1/60) * math.pi / 180            # 1 phut cung -> radian
print(f"theta = {theta:.4e} rad")
assert abs(theta - 2.91e-4) < 0.01e-4

lecture = {1: 0.29, 3: 0.87, 5: 1.45, 10: 2.91, 20: 5.82}   # bang trong slide 6 (mm)
for D, mm_slide in lecture.items():
    h_small = D * theta * 1000                         # h ~ D*theta
    h_exact = 2 * D * math.tan(theta / 2) * 1000       # chinh xac hon
    print(f"D = {D:>2} m  h(D*theta) = {h_small:.3f} mm   h(2D tan(theta/2)) = {h_exact:.3f} mm   slide: {mm_slide}")
    assert abs(h_small - mm_slide) < 0.006

for name, (w, h) in {"HD": (1280, 720), "Full HD": (1920, 1080), "4K UHD": (3840, 2160)}.items():
    print(f"{name:8s} {w}x{h} = {w*h:>9,d} pixel = {w*h/1e6:.2f} MP")
assert round(1280*720/1e6, 1) == 0.9 and round(1920*1080/1e6, 1) == 2.1 and round(3840*2160/1e6, 1) == 8.3
assert 3840*2160 == 4 * 1920*1080               # 4K = 4 lan Full HD"""),

md("""## 2. Quét raster của CRT / CRT raster scan (Tooley 11.1.3)"""),
code("""# Vi du 1: raster 4 dong, Y = 50 Hz -> X = 4 * 50 = 200 Hz, mot khung = 1/50 s = 20 ms
n_lines, f_y = 4, 50
f_x = n_lines * f_y
print("4 dong:", f_x, "Hz, khung =", 1000 / f_y, "ms")
assert f_x == 200 and 1000 / f_y == 20

# Vi du 2: 400 dong, Y = 100 Hz -> X = 40 kHz
n_lines, f_y = 400, 100
f_x = n_lines * f_y
print("400 dong:", f_x / 1000, "kHz, khung =", 1000 / f_y, "ms")
assert f_x == 40_000

# So mau cua mot diem anh khi moi kenh R,G,B co 256 muc (Tooley 11.3.3: 'hon 16 trieu mau')
print("So mau 256^3 =", 256**3)
assert 256**3 == 16_777_216 and 256**3 > 16_000_000"""),

md("""## 3. LED, hiển thị 7 đoạn và các câu hỏi của Tooley / LEDs, 7-segment and Tooley's questions"""),
code("""SEG = {  # doan sang cho tung chu so (chuan 7 doan)
 0:"abcdef", 1:"bc", 2:"abged", 3:"abgcd", 4:"fgbc", 5:"afgcd", 6:"afgecd", 7:"abc", 8:"abcdefg", 9:"abcdfg"}
SEGSET = {k: frozenset(v) for k, v in SEG.items()}
def show(segs): return [k for k, v in SEGSET.items() if v == frozenset(segs)]

print("Doan a,b,c,d,g sang ->", show("abcdg"))       # Tooley Ch.11 Q5
print("BCD 1001 ->", int("1001", 2), "->", sorted(SEG[int('1001', 2)]))   # Tooley Ch.11 Q6
assert show("abcdg") == [3] and int("1001", 2) == 9
assert SEGSET[1] == frozenset("bc") and SEGSET[2] == frozenset("abged")   # Tooley muc 11.2.2 (so 1 va so 2)

# Dien tro han dong cho LED chuan 5 mm (bang 11.1: 10 mA, 2.0 V), nguon 5 V (bai tinh them cua module)
R = (5 - 2.0) / 0.010
print("R =", R, "ohm")
assert abs(R - 300) < 1e-9"""),

md("""## 4. Floyd Applied Logic: bộ giải mã chữ cái 7 đoạn (sympy) / Floyd Applied Logic: letter decoder (sympy)
🎯 Chữ A, b, C, d, E dùng các đoạn trong Bảng 4-14; ngõ ra tích cực THẤP (0 = sáng); mã 0 đến 9 là "không quan tâm"; F tắt hết. Từ đó tìm biểu thức tối thiểu và kiểm tra các đáp án in của Bài 63, 65, 67, 69 (A-6)."""),
code("""from sympy import symbols, SOPform
from sympy.logic.boolalg import simplify_logic
H3, H2, H1, H0 = symbols("H3 H2 H1 H0"); V = [H3, H2, H1, H0]
on = {10: "abcefg", 11: "cdefg", 12: "adef", 13: "bcdeg", 14: "adefg", 15: ""}   # A b C d E F
dc = [[int(b) for b in format(c, "04b")] for c in range(10)]
def sop(seg, table=on):
    ones = [[int(b) for b in format(c, "04b")] for c in table if seg not in table[c]]   # ngo ra = 1 khi doan TAT
    return SOPform(V, ones, dc)
def cost(e):
    terms = e.args if e.func.__name__ == "Or" else [e]
    ands, inv = {}, set()
    for t in terms:
        lits = t.args if t.func.__name__ == "And" else [t]
        if len(lits) > 1: ands[len(lits)] = ands.get(len(lits), 0) + 1
        inv |= {str(l.args[0]) for l in lits if l.func.__name__ == "Not"}
    return dict(AND=ands, OR=len(terms) if len(terms) > 1 else 0, inverters=len(inv))
res = {s: sop(s) for s in "abcdefg"}
for s, e in res.items(): print(s, "=", e, cost(e))

# Dap an in Bai 65 (A-6): d = AND2 + AND3 + OR2 + 2 dao; e = AND3; f = AND2; g = AND2 + AND3 + OR2 + 2 dao
assert cost(res["d"]) == dict(AND={3: 1, 2: 1}, OR=2, inverters=2)
assert cost(res["e"]) == dict(AND={3: 1}, OR=0, inverters=0)
assert cost(res["f"]) == dict(AND={2: 1}, OR=0, inverters=0)
assert cost(res["g"]) == dict(AND={3: 1, 2: 1}, OR=2, inverters=2)
assert str(res["a"]) == "H0"                      # Floyd: doan a noi thang H0
print("Khop dap an in Bai 65 va doan a = H0.")"""),
code("""# Bai 67: them chu F (F sang a,e,f,g). Kiem tra mach in o Hinh P-19: a = H3.~H2.H1 + ~H1.H0
on67 = dict(on); on67[15] = "aefg"
need = {c: (0 if "a" in on67[c] else 1) for c in on67}          # a = 0 la sang
printed = lambda h3, h2, h1, h0: (h3 & (1 - h2) & h1) | ((1 - h1) & h0)
mine = lambda h3, h2, h1, h0: (h0 & (1 - h1)) | (h0 & (1 - h2))
bad = []
for c, v in need.items():
    h = [int(b) for b in format(c, "04b")]
    if printed(*h) != v: bad.append(format(c, "04b"))
    assert mine(*h) == v
print("Ma tren in sai o:", bad)
assert bad == ["1010"]                 # chi sai o chu A: doan a cua chu A khong sang
print("Mach tu thiet ke a = H0.~H1 + H0.~H2 dung tren ca 6 chu:", all(mine(*[int(b) for b in format(c, '04b')]) == v for c, v in need.items()))"""),
code("""# Bai 69: bo phat hien ma khong hop le X = H3.(H1 + H2): 1 voi 1010..1111, 0 voi 0000..1001
for c in range(16):
    h3, h2, h1, h0 = [int(b) for b in format(c, "04b")]
    x = h3 & (h1 | h2)
    assert x == (1 if c >= 10 else 0)
print("Bai 69: X = H3.(H1 + H2) dung tren ca 16 ma.")
print(simplify_logic(H3 & (H1 | H2), "dnf"))"""),

md("""## 5. 74HC47: zero suppression và lamp test / 74HC47: zero suppression and lamp test (Floyd 6-5)"""),
code("""def show_digits(digits, leading=True):
    \"\"\"Mo phong chuoi RBI/RBO cua cac 74HC47: so 0 o dau (hoac cuoi) bi xoa cho den khi gap chu so khac 0.\"\"\"
    out = []; suppress = True
    seq = digits if leading else digits[::-1]
    for d in seq:
        if suppress and d == 0:
            out.append(" ")         # RBI = 0 va ma 0000 -> tat het doan, RBO = 0
        else:
            suppress = False; out.append(str(d))
    return "".join(out if leading else out[::-1])

# Vi du Floyd: 030.080 hien thi 30.08 (so 0 can thiet o giua va truoc dau thap phan duoc giu)
print(repr(show_digits([0, 0, 3, 0], leading=True)))     # 0030 -> '  30'  (hinh 6-35a)
print(repr(show_digits([0, 5, 7, 0, 0], leading=False))) # 05700: chi xoa cac so 0 o CUOI -> '057  '
assert show_digits([0, 0, 3, 0], leading=True) == "  30"
assert show_digits([0, 5, 7, 0, 0], leading=False) == "057  "
assert show_digits([0, 3, 0, 0, 8, 0], leading=True) == " 30080"   # 030080: chi so 0 dau bi xoa, cac so 0 can thiet duoc giu
print("OK")"""),

md("""## 6. Các con số trên slide ECAM của bài giảng / Numbers on the lecture's ECAM slides
🎯 Kiểm tra độc lập một số con số: tổng nhiên liệu (slide 32), chênh áp cabin ISA (slide 29), thời gian đến điểm bay (slide 22 và 24), kênh ACARS (Tooley bảng 15.1)."""),
code("""# 6.1 Nhien lieu: tong cac thung so voi FOB hien thi
off = [686, 2742, 5852, 2741, 686]; on_ = [106, 2742, 4902, 2741, 106]
print("Bom TAT:", sum(off), "(FOB tren slide 12707)"); print("Bom BAT:", sum(on_), "(FOB tren slide 10598)")
assert sum(off) == 12707 and sum(on_) == 10597 and abs(sum(on_) - 10598) <= 1   # chenh 1 kg = lam tron tung thung"""),
code("""# 6.2 Chenh ap cabin o FL140 trong khi quyen chuan ISA (slide 29: dP = 2.9 psi, CAB ALT = 2870 ft)
def p_isa_psi(h_ft):
    return 14.696 * (1 - 6.8756e-6 * h_ft) ** 5.2559        # troposphere, h < 36089 ft
p_amb = p_isa_psi(14000); p_cab = p_isa_psi(2870)
dP = p_cab - p_amb
print(f"p(14000 ft) = {p_amb:.2f} psi, p(2870 ft) = {p_cab:.2f} psi, dP = {dP:.2f} psi (slide ghi 2.9)")
assert abs(p_amb - 8.63) < 0.02 and abs(p_cab - 13.24) < 0.02 and abs(dP - 4.6) < 0.05
T_isa = 15 - 1.98 * 14                                       # ~ -12.7 C: slide ghi SAT = -13 C (dung ISA)
print(f"SAT ISA tai FL140 = {T_isa:.1f} C")
assert abs(T_isa - (-13)) < 0.5
# Do lech ISA khong giai thich duoc: muon dP = 2.9 psi voi CAB ALT 2870 ft can ap ngoai = p_cab - 2.9 ->
p_need = p_cab - 2.9
h_need = (1 - (p_need / 14.696) ** (1 / 5.2559)) / 6.8756e-6
print(f"Voi dP = 2.9 psi, do cao ngoai phai chi khoang {h_need:.0f} ft (khong phai 14000 ft)")"""),
code("""# 6.3 Thoi gian bay den diem bay tren ND: 37 NM o toc do mat dat 257 kt
t_min = 37 / 257 * 60
print(f"t = {t_min:.1f} phut  (slide ghi nhan '23 33' la 23 phut 33 giay, hoac '2 33' o slide khac)")
assert abs(t_min - 8.6) < 0.05
# 6.4 Kenh ACARS (Tooley bang 15.1) deu nam trong 129-137 MHz
ch = [129.125, 130.025, 130.450, 131.125, 131.475, 131.525, 131.550, 131.725, 136.900]
assert all(129 <= f <= 137 for f in ch) and len(ch) == 9
print("9 kenh ACARS trong dai 129-137 MHz: OK")"""),

md("""## 7. Đối chiếu khoá đáp án in của Tooley / Cross-checking Tooley's printed answer key
🇻🇳 Khoá đáp án đọc trực tiếp từ ảnh scan Appendix 3 (A.1 trang 376, A.11 trang 380, A.15 trang 381). Với các câu tự tính được, notebook tính lại và so sánh; câu 4 chương 11 là lỗi in thật.

🇬🇧 The key was read directly from the scanned images of Appendix 3 (A.1 p.376, A.11 p.380, A.15 p.381). For questions that can be computed, the notebook recomputes and compares; Chapter 11 Q4 is a genuine printing error."""),
code("""KEY_CH1 = "b a c a a b b b a a a a b b a c c b a a c b b a a c b c".split()   # cau 1..28 (A.1)
KEY_CH11 = "c b a a b c b a c b c c b a c a".split()                             # cau 1..16 (A.11)
KEY_CH15 = "c a c b c c b a c a b b a b".split()                                 # cau 1..14 (A.15)
assert len(KEY_CH1) == 28 and len(KEY_CH11) == 16 and len(KEY_CH15) == 14

# Cau tinh duoc cua chuong 11
assert KEY_CH11[4] == "b"         # Q5: a,b,c,d,g -> '3' la lua chon (b) trong (a)2 (b)3 (c)5
assert KEY_CH11[5] == "c"         # Q6: BCD 1001 = 9 la lua chon (c) trong (a)7 (b)8 (c)9
assert KEY_CH11[0] == "c"         # Q1: 635 nm la lua chon (c) trong (a)475 (b)525 (c)635 (bang 11.1)
assert KEY_CH11[13] == "a"        # Q14: 0.03 A la (a) trong (a)0.03 (b)0.3 (c)3 (bang 11.1: 30-40 mA)
assert KEY_CH11[12] == "b"        # Q13: ramp la (b)
# Cau 2 va cau 4 phai nhat quan (mat nhay nhat o ~550 nm = anh sang luc)
q2_peak_nm = {"a": 450, "b": 550, "c": 650}[KEY_CH11[1]]
q4_choice = {"a": "red", "b": "blue", "c": "green"}[KEY_CH11[3]]
print("Cau 2 (khoa in):", q2_peak_nm, "nm  ->", "luc" if 520 <= q2_peak_nm <= 570 else "khac")
print("Cau 4 (khoa in):", q4_choice, " -> MAU THUAN voi cau 2: dap an dung la green = (c)")
assert 520 <= q2_peak_nm <= 570 and q4_choice != "green"        # xac nhan loi in cua khoa dap an
print("Chuong 1: tong 28 cau, bo cau 20 ('secondary heading information'): khoa in (a) gyro, chua tu kiem duoc nen khong dua len site.")"""),
md("""#### 📤 Nhận xét / Takeaway
🇻🇳 Mọi con số tự tính được đều khớp bài giảng và sách, ngoại trừ ba điểm đã nêu rõ trong module: ΔP 2,9 psi ở FL140 (tính ra 4,6 psi), nhãn "23 33" (8,6 phút), và khoá đáp án in sai ở Tooley Chương 11 câu 4. Bài 67 của Floyd có đáp án in sai ở mã 1010 (chữ A).

🇬🇧 Every number that can be recomputed matches the lecture and the books, except the three points flagged in the module: ΔP 2.9 psi at FL140 (computes to 4.6 psi), the "23 33" label (8.6 minutes), and the wrong printed answer key in Tooley Chapter 11 question 4. Floyd Problem 67's printed answer is wrong at code 1010 (the letter A)."""),
]

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                  "language_info": {"name": "python", "version": "3"}}
path = os.path.join(OUT, "06_electronic-displays.ipynb")
nbf.write(nb, path)
print("wrote", path)
