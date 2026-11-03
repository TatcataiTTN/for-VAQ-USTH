# -*- coding: utf-8 -*-
"""Module 10: Dong can am nen duoc quanh canh: Prandtl-Glauert, Karman-Tsien, Laitone, Mcr. Nguon: Anderson 6th ch.11 (11.1-11.7, Bai 11.1-11.7);
EASA M08 SM3 (tr.3.10-3.11). Doi chieu Solution Manual (4th): 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7 khop."""
import math
from aero import *
from common import num, ul, table, mcq, sol

g = GAMMA


def pg(cp0, M): return cp0 / math.sqrt(1 - M * M)
def kt(cp0, M):
    b = math.sqrt(1 - M * M); return cp0 / (b + M * M / (1 + b) * cp0 / 2)
def lai(cp0, M):
    b = math.sqrt(1 - M * M); return cp0 / (b + M * M * (1 + (g - 1) / 2 * M * M) / (2 * b) * cp0)


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    # 11.1
    b = math.sqrt(1 - 0.6269 ** 2)
    u = 700 + 2 * math.pi * 70 / b * math.exp(-2 * math.pi * b * 0.2) * math.cos(2 * math.pi * 0.2)
    v = -140 * math.pi * math.exp(-2 * math.pi * b * 0.2) * math.sin(2 * math.pi * 0.2)
    V = math.hypot(u, v); Minf = 700 / math.sqrt(g * 1716 * 519); T0 = 519 * (1 + 0.2 * Minf ** 2)
    M111 = V / math.sqrt(g * 1716 * T0 - (g - 1) / 2 * V * V); T111 = T0 / (1 + 0.2 * M111 ** 2); p111 = p0_over_p(Minf) / p0_over_p(M111)
    # 11.2
    cl0 = 0.75; cl112 = cl0 / math.sqrt(1 - 0.36)
    # 11.3
    c1, c2, c3 = pg(-0.54, 0.58), kt(-0.54, 0.58), lai(-0.54, 0.58)
    # 11.4
    Mcr = mcr_prandtl_glauert(-0.41)
    # 11.5
    p115 = p0_over_p(0.8) / p0_over_p(1.0)
    # 11.6
    pr116 = p0_over_p(0.5) / p0_over_p(0.86); cp116 = 2 / (g * 0.25) * (pr116 - 1)
    # 11.7
    Mi = 0.3; MA0 = 0.435
    cp_a = 2 / (g * Mi * Mi) * (p0_over_p(Mi) / p0_over_p(MA0) - 1); cp0 = cp_a * math.sqrt(1 - Mi * Mi)
    def MAof(Minf_):
        cp = cp0 / math.sqrt(1 - Minf_ ** 2); pr = 1 + g * Minf_ ** 2 * cp / 2
        lo, hi = 0.01, 3.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if p0_over_p(Minf_) / p0_over_p(mid) > pr: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    MA061 = MAof(0.61); MAs = {x: MAof(x) for x in (0.5, 0.55, 0.6)}
    ex111 = pg(-0.3, 0.6); slope = 2 * math.pi / math.sqrt(1 - 0.49) / (2 * math.pi)

    m = {"num": "10", "slug": "10-subsonic-compressible", "tag": L("Cận âm nén được", "Subsonic compressible")}
    m["title"] = L("Dòng cận âm nén được quanh cánh: quy tắc Prandtl-Glauert và số Mach tới hạn", "Subsonic compressible flow past airfoils: the Prandtl-Glauert rule and the critical Mach number")
    m["src"] = L("Anderson ch.11 (mục 11.1–11.6; Bài 11.1–11.7) · EASA Module 08, Sub-module 03 (tr. 3.10–3.11)", "Anderson ch. 11 (sec. 11.1–11.6; Problems 11.1–11.7) · EASA Module 08, Sub-module 03 (pp. 3.10–3.11)")
    m["intro"] = L("Module 03 nói rằng gần tốc độ âm thanh, tính nén được làm đổi lực nâng và gây sóng xung kích, nhưng chưa nói đổi bao nhiêu. Module này cho con số: với dòng cận âm và cánh mỏng, hệ số áp suất và hệ số lực nâng đều được nhân thêm 1/√(1 − M²) (quy tắc Prandtl-Glauert). Kármán-Tsien và Laitone là các hiệu chỉnh chính xác hơn. Kết hợp với hệ số áp suất tới hạn, ta tính được số Mach tới hạn, tức lúc bắt đầu có dòng siêu âm cục bộ trên cánh.",
                   "Module 03 said that near the speed of sound compressibility changes lift and causes shocks, but not by how much. This module gives the numbers: for subsonic flow past a thin airfoil the pressure and lift coefficients are multiplied by 1/√(1 − M²) (the Prandtl-Glauert rule). Kármán-Tsien and Laitone are more accurate corrections. Combined with the critical pressure coefficient this gives the critical Mach number, the point at which supersonic flow first appears locally on the wing.")
    m["mapping"] = {
        "easa": L("Sub-module 03 (tr. 3.10 dòng cận âm so với siêu âm, tr. 3.11 số Mach tới hạn, Hình 3-10)", "Sub-module 03 (p. 3.10 subsonic versus supersonic flow, p. 3.11 critical Mach number, Figure 3-10)"),
        "anderson": L("Ch.11 Subsonic Compressible Flow over Airfoils: Linear Theory: 11.2 phương trình thế tuyến tính, 11.4 quy tắc Prandtl-Glauert, 11.5 hiệu chỉnh cải tiến (Kármán-Tsien, Laitone), 11.6 số Mach tới hạn; Bài 11.1–11.7", "Ch.11 Subsonic Compressible Flow over Airfoils: Linear Theory: 11.2 linearised potential equation, 11.4 Prandtl-Glauert rule, 11.5 improved corrections (Kármán-Tsien, Laitone), 11.6 critical Mach number; Problems 11.1–11.7"),
        "etkin": L("Etkin 6.3 nêu giới hạn: xấp xỉ phugoid chỉ dùng cho tốc độ chưa có ảnh hưởng nén được đáng kể. Phụ lục B có hệ số hiệu chỉnh Mach cho độ dốc lực nâng (tương ứng với 1/√(1 − M²))", "Etkin 6.3 states the limit: the phugoid approximation holds only below speeds with significant compressibility effects. Appendix B has Mach-number corrections for the lift slope (corresponding to 1/√(1 − M²))"),
        "note": L("Tiếp nối module 03 (số Mach tới hạn) và module 06–07 (sóng xung kích).", "Continues module 03 (critical Mach number) and modules 06–07 (shock waves)."),
    }
    parts = []
    parts.append({"title": L("Quy tắc Prandtl-Glauert", "The Prandtl-Glauert rule"),
                  "bullets": [L("C_p = C_p,0/√(1 − M∞²), c_l = c_l,0/√(1 − M∞²), c_m = c_m,0/√(1 − M∞²)", "C_p = C_p,0/√(1 − M∞²), c_l = c_l,0/√(1 − M∞²), c_m = c_m,0/√(1 − M∞²)"),
                              L("Cho cánh mỏng, góc tấn nhỏ, M∞ không quá gần 1", "For thin airfoils at small angle of attack, M∞ not too near 1"),
                              L("Hệ số tăng dần: 1,25 ở M = 0,6; 1,40 ở M = 0,7; 1,67 ở M = 0,8", "The factor grows: 1.25 at M = 0.6; 1.40 at M = 0.7; 1.67 at M = 0.8")],
                  "slides": [{"title": L("Hệ số hiệu chỉnh theo số Mach", "The correction factor against Mach number"),
                              "body": table(["M∞", "1/√(1 − M∞²)"], [[N(x, 1), N(1 / math.sqrt(1 - x * x), 3)] for x in (0.3, 0.5, 0.6, 0.7, 0.8, 0.9)]) +
                              ul(L(f"Ví dụ 11.1 của sách: C_p,0 = −0,3 ở M = 0,6 cho C_p = {N(ex111, 3)}", f"Book Example 11.1: C_p,0 = −0.3 at M = 0.6 gives C_p = {N(ex111, 3)}"),
                                 L(f"Ví dụ 11.2: độ dốc lực nâng 2π được nhân thêm hệ số 1/√(1 − 0,49) = {N(1 / math.sqrt(0.51), 2)} ở M = 0,7, tức tăng khoảng 40%", f"Example 11.2: the lift slope 2π is multiplied by 1/√(1 − 0.49) = {N(1 / math.sqrt(0.51), 2)} at M = 0.7, an increase of about 40%")),
                              "explain": L("Dòng nén được \"khuếch đại\" mọi nhiễu áp suất: một biên dạng nâng nhiều hơn và hút mạnh hơn khi tốc độ gần âm thanh.", "Compressible flow \"amplifies\" every pressure disturbance: an airfoil lifts more and sucks harder as the speed approaches that of sound.")}]})
    parts.append({"title": L("Hiệu chỉnh Kármán-Tsien và Laitone", "The Kármán-Tsien and Laitone corrections"),
                  "bullets": [L("Kármán-Tsien: C_p = C_p,0/[√(1 − M²) + (M²/(1 + √(1 − M²)))·C_p,0/2]", "Kármán-Tsien: C_p = C_p,0/[√(1 − M²) + (M²/(1 + √(1 − M²)))·C_p,0/2]"),
                              L("Laitone: C_p = C_p,0/[√(1 − M²) + (M²(1 + (γ−1)M²/2)/(2√(1 − M²)))·C_p,0]", "Laitone: C_p = C_p,0/[√(1 − M²) + (M²(1 + (γ−1)M²/2)/(2√(1 − M²)))·C_p,0]"),
                              L("Cả hai tính đến phi tuyến nên cho |C_p| lớn hơn Prandtl-Glauert", "Both include nonlinearity so they give a larger |C_p| than Prandtl-Glauert")],
                  "slides": [{"title": L("Bài 11.3: so sánh ba quy tắc", "Problem 11.3: comparing the three rules"),
                              "body": table([L("Quy tắc", "Rule"), "C_p (M = 0,58; C_p,0 = −0,54)" if lang == "vi" else "C_p (M = 0.58; C_p,0 = −0.54)"],
                                            [["Prandtl-Glauert", N(c1, 3)], ["Kármán-Tsien", N(c2, 4)], ["Laitone", N(c3, 4)]]) +
                              f"<p class='pill'>{L('Khớp Solution Manual: −0,663; −0,7063; −0,7763. Ba quy tắc chênh nhau khoảng 17%. Theo Solution Manual, kinh nghiệm cho thấy Kármán-Tsien chính xác nhất trong ba.', 'Matches the Solution Manual: −0.663; −0.7063; −0.7763. The three rules differ by about 17%. According to the Solution Manual, experience shows Kármán-Tsien to be the most accurate of the three.')}</p>",
                              "explain": L("Prandtl-Glauert là tuyến tính nên đánh giá thấp lực hút; hai quy tắc kia tính thêm hiệu ứng phi tuyến.", "Prandtl-Glauert is linear so it underestimates the suction; the other two add the nonlinear effect.")}]})
    parts.append({"title": L("Hệ số áp suất tới hạn và số Mach tới hạn", "Critical pressure coefficient and critical Mach number"),
                  "bullets": [L("Số Mach tới hạn M_cr là M∞ mà điểm hút mạnh nhất đạt M cục bộ = 1", "The critical Mach number M_cr is the M∞ at which the point of strongest suction reaches local M = 1"),
                              L("Tại đó p/p∞ = (p₀/p∞)/(p₀/p tại M = 1) và C_p,cr = 2/(γM²)·(p/p∞ − 1)", "There p/p∞ = (p₀/p∞)/(p₀/p at M = 1) and C_p,cr = 2/(γM²)·(p/p∞ − 1)"),
                              L("M_cr là giao điểm của đường Prandtl-Glauert và đường C_p,cr(M)", "M_cr is the intersection of the Prandtl-Glauert curve with the C_p,cr(M) curve")],
                  "slides": [{"title": L("Bài 11.4 và 11.5", "Problems 11.4 and 11.5"),
                              "body": ul(L(f"11.4: C_p,0 = −0,41 cho M_cr = {N(Mcr, 3)} (Solution Manual vẽ đồ thị và đọc M_cr = 0,74)", f"11.4: C_p,0 = −0.41 gives M_cr = {N(Mcr, 3)} (the Solution Manual plots the curves and reads M_cr = 0.74)"),
                                         L(f"11.5: M_cr = 0,8 thì tại điểm hút mạnh nhất p/p∞ = {N(p115, 3)} (Solution Manual 0,805)", f"11.5: with M_cr = 0.8 the pressure ratio at the minimum-pressure point is p/p∞ = {N(p115, 3)} (Solution Manual 0.805)"),
                                         L("Cánh càng mỏng và hút càng nhẹ (|C_p,0| nhỏ) thì M_cr càng cao. Đó là một lý do cánh máy bay phản lực mỏng và xuôi sau", "A thinner airfoil with gentler suction (small |C_p,0|) has a higher M_cr. That is one reason jet-aircraft wings are thin and swept")),
                              "explain": L("Vượt M_cr thì chưa có sóng mạnh ngay. Lực cản sóng chỉ tăng vọt ở số Mach phân kỳ lực cản, cao hơn M_cr khoảng 5–10% (EASA tr. 3.14).", "Passing M_cr does not mean a strong shock at once. Wave drag rises sharply only at the drag-divergence Mach number, 5–10% above M_cr (EASA p. 3.14).")}]})
    parts.append({"title": L("Từ số Mach cục bộ đến hệ số áp suất", "From local Mach number to pressure coefficient"),
                  "bullets": [L("Dòng nén được: C_p là hàm của M cục bộ và M∞, không phải của vận tốc", "In compressible flow C_p is a function of the local and free-stream Mach numbers, not of velocity"),
                              L("C_p = (2/γM∞²)·[((1 + 0,2M∞²)/(1 + 0,2M²))^3,5 − 1]", "C_p = (2/γM∞²)·[((1 + 0.2M∞²)/(1 + 0.2M²))^3.5 − 1]"),
                              L("Tổng quát hóa công thức C_p = 1 − (V/V∞)² của dòng không nén được", "A generalisation of the incompressible C_p = 1 − (V/V∞)²")],
                  "slides": [{"title": L("Bài 11.1, 11.6 và 11.7", "Problems 11.1, 11.6 and 11.7"),
                              "body": ul(L(f"11.1: tại (0,2; 0,2) ft: V = {N(V, 1)} ft/s, M = {N(M111, 3)}, p = {N(p111, 3)} atm, T = {N(T111, 1)} °R", f"11.1: at (0.2, 0.2) ft: V = {N(V, 1)} ft/s, M = {N(M111, 3)}, p = {N(p111, 3)} atm, T = {N(T111, 1)} °R"),
                                         L(f"11.6: M∞ = 0,5, M cục bộ = 0,86: p/p∞ = {N(pr116, 4)}, C_p = {N(cp116, 3)} (Solution Manual −1,53)", f"11.6: M∞ = 0.5, local M = 0.86: p/p∞ = {N(pr116, 4)}, C_p = {N(cp116, 3)} (Solution Manual −1.53)"),
                                         L(f"11.7: bắt đầu M∞ = 0,3 với M_A = 0,435 ⇒ C_p,0 = {N(cp0, 3)}; Prandtl-Glauert đưa M_A = {N(MAs[0.5], 3)} (M∞ = 0,5), {N(MAs[0.6], 3)} (0,6) và {N(MA061, 3)} ở M∞ = 0,61: đúng M_cr ≈ 0,61", f"11.7: starting from M∞ = 0.3 with M_A = 0.435 ⇒ C_p,0 = {N(cp0, 3)}; Prandtl-Glauert takes M_A to {N(MAs[0.5], 3)} (M∞ = 0.5), {N(MAs[0.6], 3)} (0.6) and {N(MA061, 3)} at M∞ = 0.61: so M_cr ≈ 0.61")),
                              "explain": L("Con số M_cr = 0,61 trong Hình 11.5 của sách không phải tùy ý: nó chính là kết quả của phép tính ở bài 11.7.", "The value M_cr = 0.61 in the book's Figure 11.5 is not arbitrary: it is the result of the calculation in Problem 11.7.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Prandtl-Glauert, Kármán-Tsien và C_p theo số Mach", "Prandtl-Glauert, Kármán-Tsien and C_p in terms of Mach number")
    m["formula_math"] = ("C_p = C_p,0/√(1−M²)  ·  C_p = C_p,0/[√(1−M²) + (M²/(1+√(1−M²)))C_p,0/2]<br>C_p = (2/γM∞²)[(p/p∞) − 1], p/p∞ = [(1+0,2M∞²)/(1+0,2M²)]^3,5" if lang == "vi" else
                         "C_p = C_p,0/√(1−M²)  ·  C_p = C_p,0/[√(1−M²) + (M²/(1+√(1−M²)))C_p,0/2]<br>C_p = (2/γM∞²)[(p/p∞) − 1], p/p∞ = [(1+0.2M∞²)/(1+0.2M²)]^3.5")
    m["legend"] = [("C_p,0", L("hệ số áp suất ở tốc độ thấp", "low-speed pressure coefficient")), ("M∞, M", L("Mach dòng tự do và cục bộ", "free-stream and local Mach numbers")), ("β", L("√(1 − M∞²)", "√(1 − M∞²)")), ("M_cr", L("số Mach tới hạn", "critical Mach number")), ("C_p,cr", L("hệ số áp suất tại M = 1", "pressure coefficient at M = 1")), ("γ", "1,4" if lang == "vi" else "1.4")]
    m["history_title"] = L("Prandtl, Glauert và thời chiến", "Prandtl, Glauert and wartime")
    m["history"] = L("Anderson viết rằng quy tắc Prandtl-Glauert không chỉ nằm trong công trình của Ludwig Prandtl (khoảng 1922) và Hermann Glauert (1928) mà còn xuất hiện trong những nghiên cứu sớm hơn. Ông cũng ghi nhận nhu cầu về các hiệu chỉnh chính xác hơn khi tốc độ máy bay tăng vọt trong Chiến tranh thế giới II; từ đó quy tắc Kármán-Tsien được ngành hàng không dùng rộng rãi (Anderson 11.5).",
                     "Anderson writes that the Prandtl-Glauert rule appears not only in the work of Ludwig Prandtl (about 1922) and Hermann Glauert (1928) but also in earlier studies. He also notes the need for more accurate corrections as aircraft speeds soared in World War II; the Kármán-Tsien rule has been widely used in the industry since then (Anderson 11.5).")
    m["case_title"] = L("Tình huống: lực nâng của biên dạng ở M = 0,6", "Case: airfoil lift at M = 0.6")
    m["case"] = L(ul("Biên dạng NACA 2412 ở α = 5° có c_l,0 = 0,75 ở tốc độ thấp (Solution Manual đọc từ Hình 4.5; nội suy bảng bài 1.6 cho 0,745).",
                  f"Ở M = 0,6, c_l = 0,75/√(1 − 0,36) = {N(cl112, 3)}: tăng 25% chỉ nhờ tính nén được (Bài 11.2).",
                  "Với cùng góc tấn, máy bay bay nhanh hơn thì nâng nhiều hơn, nên tư thế cân bằng thay đổi theo số Mach."),
                  ul("A NACA 2412 airfoil at α = 5° has c_l,0 = 0.75 at low speed (the Solution Manual reads it from Figure 4.5; interpolating the table of Problem 1.6 gives 0.745).",
                  f"At M = 0.6, c_l = 0.75/√(1 − 0.36) = {N(cl112, 3)}: 25% more from compressibility alone (Problem 11.2).",
                  "At the same angle of attack a faster aircraft lifts more, so the trim attitude changes with Mach number."))
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L(ul("Prandtl-Glauert chỉ đúng cho M∞ dưới M_cr và cánh mỏng. Gần M = 1 nó cho kết quả vô hạn, không phản ánh thực tế.",
                  "Trong dòng nén được, C_p phụ thuộc số Mach cục bộ, không phụ thuộc vận tốc (Bài 11.6).",
                  "Hệ số hiệu chỉnh áp dụng cho C_p,0, c_l,0 và c_m,0, không áp dụng cho lực cản.",
                  "M_cr nhỏ hơn 1: máy bay vẫn bay cận âm khi dòng siêu âm cục bộ đầu tiên xuất hiện trên cánh.",
                  "Bài 11.2 cần c_l,0 từ Hình 4.5. Module dùng 0,75 như Solution Manual; nội suy bảng của bài 1.6 cho 0,745 (kết quả 0,931 thay vì 0,938)."),
                  ul("Prandtl-Glauert holds only for M∞ below M_cr and for thin airfoils. Near M = 1 it gives infinity, which does not reflect reality.",
                  "In compressible flow C_p depends on the local Mach number, not on velocity (Problem 11.6).",
                  "The correction applies to C_p,0, c_l,0 and c_m,0, not to drag.",
                  "M_cr is below 1: the aircraft is still subsonic when supersonic flow first appears locally on the wing.",
                  "Problem 11.2 needs c_l,0 from Figure 4.5. The module uses 0.75 as the Solution Manual does; interpolating the table of Problem 1.6 gives 0.745 (0.931 instead of 0.938)."))
    m["nb_desc"] = L("Notebook cài ba quy tắc hiệu chỉnh, tìm M_cr bằng chia đôi, giải lại Anderson 11.1–11.7 và dùng assert để kiểm các đáp án quiz.", "The notebook implements the three correction rules, finds M_cr by bisection, re-solves Anderson 11.1–11.7 and uses assert to check the quiz answers.")

    SD = lambda i: 1000 + i
    SUP = L("Câu luyện thêm", "Extra practice")
    Q = lambda i, src, q_, r, w, ex, det=None: mcq(SD(i), src, q_, r, w, ex, det)
    book = [
        Q(1, "Anderson 6th, Problem 11.1", L("Dòng cận âm nén được có thế vận tốc φ = V∞x + [70/√(1−M∞²)]·sin(2πx)·e^(−2πy√(1−M∞²)), V∞ = 700 ft/s, p∞ = 1 atm, T∞ = 519 °R. Số Mach tại (0,2; 0,2) ft là:", "A subsonic compressible flow has velocity potential φ = V∞x + [70/√(1−M∞²)]·sin(2πx)·e^(−2πy√(1−M∞²)), V∞ = 700 ft/s, p∞ = 1 atm, T∞ = 519 °R. The Mach number at (0.2, 0.2) ft is:"), N(M111, 3), [N(Minf, 3), N(0.8, 3), N(M111 * 1.2, 3)], L("Tính u, v từ φ, rồi M từ năng lượng.", "Compute u, v from φ, then M from the energy equation."), L(f"<p>u = {N(u, 1)}, v = {N(v, 1)} ft/s, V = {N(V, 1)}; T₀ = 1,079 × 519 = {N(T0, 1)} °R; a² = γRT₀ − (γ−1)V²/2 ⇒ M = {N(M111, 4)} (Solution Manual 0,7067).</p>", f"<p>u = {N(u, 1)}, v = {N(v, 1)} ft/s, V = {N(V, 1)}; T₀ = 1.079 × 519 = {N(T0, 1)} °R; a² = γRT₀ − (γ−1)V²/2 ⇒ M = {N(M111, 4)} (Solution Manual 0.7067).</p>")),
        Q(2, "Anderson 6th, Problem 11.2", L("Biên dạng NACA 2412 ở 5° có c_l,0 = 0,75. Theo Prandtl-Glauert, c_l ở M = 0,6 là:", "A NACA 2412 airfoil at 5° has c_l,0 = 0.75. By Prandtl-Glauert, c_l at M = 0.6 is:"), N(cl112, 3), [N(0.75 * 0.8, 3), N(0.75 * 1.6, 3), N(0.75, 3)], L("c_l = c_l,0/√(1 − M²) = 0,75/0,8.", "c_l = c_l,0/√(1 − M²) = 0.75/0.8.")),
        Q(3, "Anderson 6th, Problem 11.3a", L("C_p,0 = −0,54, M∞ = 0,58. Theo Prandtl-Glauert, C_p là:", "C_p,0 = −0.54, M∞ = 0.58. By Prandtl-Glauert, C_p is:"), N(c1, 3), [N(c2, 3), N(c3, 3), N(-0.54 * 0.8146, 3)], L("C_p = C_p,0/√(1 − 0,58²) = −0,54/0,8146.", "C_p = C_p,0/√(1 − 0.58²) = −0.54/0.8146.")),
        Q(4, "Anderson 6th, Problem 11.3b", L("Cùng số liệu; theo Kármán-Tsien, C_p là:", "Same data; by Kármán-Tsien, C_p is:"), N(c2, 4), [N(c1, 4), N(c3, 4), N(c2 * 0.9, 4)], L("Mẫu số: 0,8146 + (0,3364/(1 + 0,8146))·(−0,54)/2.", "Denominator: 0.8146 + (0.3364/(1 + 0.8146))·(−0.54)/2.")),
        Q(5, "Anderson 6th, Problem 11.3c", L("Cùng số liệu; theo Laitone, C_p là:", "Same data; by Laitone, C_p is:"), N(c3, 4), [N(c1, 4), N(c2, 4), N(c3 * 1.1, 4)], L("Mẫu số: 0,8146 + [0,3364 × 1,0673/(2 × 0,8146)]·(−0,54).", "Denominator: 0.8146 + [0.3364 × 1.0673/(2 × 0.8146)]·(−0.54).")),
        Q(6, "Anderson 6th, Problem 11.4", L("C_p,0 = −0,41; theo Prandtl-Glauert, số Mach tới hạn xấp xỉ:", "C_p,0 = −0.41; by Prandtl-Glauert the critical Mach number is about:"), N(Mcr, 2), [N(0.6, 2), N(0.9, 2), N(1.0, 2)], L("M_cr là giao của C_p,0/√(1 − M²) với C_p,cr(M).", "M_cr is the intersection of C_p,0/√(1 − M²) with C_p,cr(M)."), L(f"<p>Giải bằng chia đôi: M_cr = {N(Mcr, 4)}; đồ thị của Solution Manual đọc 0,74.</p>", f"<p>Bisection gives M_cr = {N(Mcr, 4)}; the Solution Manual graph reads 0.74.</p>")),
        Q(7, "Anderson 6th, Problem 11.5", L("M_cr = 0,8. Tỉ số áp suất p/p∞ tại điểm hút mạnh nhất khi M∞ = 0,8 là:", "M_cr = 0.8. The pressure ratio p/p∞ at the minimum-pressure point when M∞ = 0.8 is:"), N(p115, 3), [N(0.528, 3), N(1.0, 3), N(1.524, 3)], L("p/p∞ = (p/p₀ tại M = 1)(p₀/p∞ tại M = 0,8) = 0,528 × 1,524.", "p/p∞ = (p/p₀ at M = 1)(p₀/p∞ at M = 0.8) = 0.528 × 1.524.")),
        Q(8, "Anderson 6th, Problem 11.6", L("M∞ = 0,5, số Mach cục bộ 0,86. Hệ số áp suất tại điểm đó là:", "M∞ = 0.5, local Mach number 0.86. The pressure coefficient at that point is:"), N(cp116, 2), [N(-0.86, 2), N(-1.0, 2), N(1 - (0.86 / 0.5) ** 2, 2)], L("C_p = (2/γM∞²)(p/p∞ − 1) với p/p∞ = 0,7316.", "C_p = (2/γM∞²)(p/p∞ − 1) with p/p∞ = 0.7316."), L(f"<p>Dùng vận tốc như dòng không nén được cho C_p = {N(1 - (0.86 / 0.5) ** 2, 2)}: sai hoàn toàn; phải dùng số Mach.</p>", f"<p>Using velocities as for incompressible flow gives C_p = {N(1 - (0.86 / 0.5) ** 2, 2)}: completely wrong; Mach numbers must be used.</p>")),
    ]
    gen = [
        Q(11, SUP, L("Hệ số 1/√(1 − M²) ở M = 0,8 bằng:", "The factor 1/√(1 − M²) at M = 0.8 is:"), N(1 / 0.6, 2), [N(1.25, 2), N(0.6, 2), N(1.8, 2)], L("√(1 − 0,64) = 0,6.", "√(1 − 0.64) = 0.6.")),
        Q(12, SUP, L("Theo Prandtl-Glauert, ở M = 0,6 độ dốc lực nâng cánh mỏng tăng so với dòng không nén được:", "By Prandtl-Glauert, at M = 0.6 the thin-airfoil lift slope rises relative to incompressible flow by:"), "25%", ["60%", "8%", "0%"], L("1/0,8 = 1,25.", "1/0.8 = 1.25.")),
        Q(13, SUP, L("Mỏng hơn và hút nhẹ hơn (|C_p,0| nhỏ) thì số Mach tới hạn:", "A thinner airfoil with gentler suction (small |C_p,0|) has a critical Mach number:"), L("cao hơn", "higher"), [L("thấp hơn", "lower"), L("không đổi", "unchanged"), L("bằng 1", "equal to 1")], L("Cần M∞ lớn hơn để đạt M = 1 tại điểm hút.", "A larger M∞ is needed to reach M = 1 at the suction point.")),
        Q(14, SUP, L("Theo thứ tự |C_p| giảm dần cho cùng C_p,0 và M∞ trong Bài 11.3:", "In decreasing order of |C_p| for the same C_p,0 and M∞ in Problem 11.3:"), "Laitone > Kármán-Tsien > Prandtl-Glauert", ["Prandtl-Glauert > Kármán-Tsien > Laitone", "Kármán-Tsien > Laitone > Prandtl-Glauert", "Cả ba bằng nhau" if lang == "vi" else "All three are equal"], L("0,776 > 0,706 > 0,663.", "0.776 > 0.706 > 0.663.")),
        Q(15, SUP, L("Tại M cục bộ = 1 và M∞ = 0,5, p/p∞ bằng:", "At local M = 1 and M∞ = 0.5, p/p∞ equals:"), N(p0_over_p(0.5) / p0_over_p(1.0), 3), [N(0.528, 3), N(1.0, 3), N(1.186, 3)], L("1,186 × 0,528.", "1.186 × 0.528.")),
        Q(16, SUP, L("Khi nào Prandtl-Glauert không còn dùng được?", "When does Prandtl-Glauert stop being usable?"), L("Khi M∞ gần 1 hoặc dòng có sóng xung kích cục bộ", "When M∞ is near 1 or the flow has local shocks"), [L("Khi M∞ dưới 0,3", "When M∞ is below 0.3"), L("Khi cánh rất mỏng", "When the airfoil is very thin"), L("Khi góc tấn bằng 0", "When the angle of attack is zero")], L("Lý thuyết là tuyến tính và giả sử dòng cận âm hoàn toàn.", "The theory is linear and assumes fully subsonic flow.")),
    ]
    m["quiz_sets"] = [
        {"key": "anderson", "title": L("Sách 2, Anderson: bài tập cuối chương 11 (đáp án đã tính lại và so với Solution Manual)", "Book 2, Anderson: end-of-chapter 11 problems (answers recomputed and compared with the Solution Manual)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập thêm (tự soạn, đáp án đã kiểm bằng tính toán)", "Extra practice (written for this site, answers checked by calculation)"), "items": gen},
    ]
    m["problems_intro"] = L("Các bài 11.1–11.7 đều khớp Solution Manual (bản 4). Riêng bài 11.7 lệch nhỏ vì Solution Manual nội suy bảng; kết luận M_cr ≈ 0,61 vẫn giống nhau.", "Problems 11.1–11.7 all agree with the 4th-edition Solution Manual. Problem 11.7 differs slightly because the Solution Manual interpolates tables; the conclusion M_cr ≈ 0.61 is the same.")
    m["problems"] = [
        {"num": "11.3", "src": "Anderson 6th, Problem 11.3", "q": L("Trong dòng không nén được, hệ số áp suất tại một điểm trên biên dạng là −0,54. Tính C_p tại điểm đó khi M∞ = 0,58 bằng (a) quy tắc Prandtl-Glauert, (b) quy tắc Kármán-Tsien, (c) quy tắc Laitone.", "In incompressible flow the pressure coefficient at a point on an airfoil is −0.54. Find C_p at that point when M∞ = 0.58 using (a) the Prandtl-Glauert rule, (b) the Kármán-Tsien rule, (c) Laitone's rule."),
         "ans": sol(lang, L("Cùng một giá trị tốc độ thấp được hiệu chỉnh bằng ba công thức khác nhau.", "The same low-speed value is corrected by three different formulas."), L("Tính trước β = √(1 − M²) = 0,8146 rồi thay vào từng công thức.", "Compute β = √(1 − M²) = 0.8146 first and substitute into each formula."),
                    [L(f"β = √(1 − 0,58²) = 0,8146; M² = 0,3364.", f"β = √(1 − 0.58²) = 0.8146; M² = 0.3364."),
                     L(f"(a) C_p = −0,54/0,8146 = <b>{N(c1, 3)}</b>.", f"(a) C_p = −0.54/0.8146 = <b>{N(c1, 3)}</b>."),
                     L(f"(b) Mẫu số = 0,8146 + (0,3364/1,8146)(−0,54/2) = 0,7646 ⇒ C_p = <b>{N(c2, 4)}</b>.", f"(b) Denominator = 0.8146 + (0.3364/1.8146)(−0.54/2) = 0.7646 ⇒ C_p = <b>{N(c2, 4)}</b>."),
                     L(f"(c) Mẫu số = 0,8146 + [0,3364 × (1 + 0,2 × 0,3364)/(2 × 0,8146)](−0,54) = 0,6956 ⇒ C_p = <b>{N(c3, 4)}</b>.", f"(c) Denominator = 0.8146 + [0.3364 × (1 + 0.2 × 0.3364)/(2 × 0.8146)](−0.54) = 0.6956 ⇒ C_p = <b>{N(c3, 4)}</b>.")],
                    L("Solution Manual: −0,663; −0,7063; −0,7763 (chênh khoảng 17% giữa ba quy tắc).", "Solution Manual: −0.663; −0.7063; −0.7763 (about 17% spread between the three rules)."))},
        {"num": "11.4 – 11.5", "src": "Anderson 6th, Problems 11.4, 11.5", "q": L("(11.4) Trong dòng không nén được, hệ số áp suất nhỏ nhất (tại điểm hút mạnh nhất) của một biên dạng là −0,41. Ước lượng số Mach tới hạn bằng quy tắc Prandtl-Glauert. (11.5) Một biên dạng có M_cr = 0,8. Tính p/p∞ tại điểm hút mạnh nhất khi M∞ = 0,8.", "(11.4) In incompressible flow the peak pressure coefficient (at the minimum-pressure point) of an airfoil is −0.41. Estimate the critical Mach number with the Prandtl-Glauert rule. (11.5) An airfoil has M_cr = 0.8. Find p/p∞ at the minimum-pressure point when M∞ = 0.8."),
         "ans": sol(lang, L("M_cr là M∞ làm điểm hút mạnh nhất đạt M = 1.", "M_cr is the M∞ that brings the strongest-suction point to M = 1."), L("(11.4) Hai đường C_p(M) cắt nhau: Prandtl-Glauert và C_p,cr. (11.5) Khi M∞ = M_cr, M cục bộ = 1 nên dùng tỉ số áp suất đẳng entropi.", "(11.4) Two curves C_p(M) intersect: Prandtl-Glauert and C_p,cr. (11.5) When M∞ = M_cr the local M is 1 so use the isentropic pressure ratio."),
                    [L("C_p,cr(M) = (2/γM²)[((1 + 0,2M²)/1,2)^3,5 − 1].", "C_p,cr(M) = (2/γM²)[((1 + 0.2M²)/1.2)^3.5 − 1]."),
                     L(f"Giải −0,41/√(1 − M²) = C_p,cr(M) bằng chia đôi: <b>M_cr = {N(Mcr, 3)}</b>.", f"Solving −0.41/√(1 − M²) = C_p,cr(M) by bisection: <b>M_cr = {N(Mcr, 3)}</b>."),
                     L(f"(11.5) p/p∞ = (p₀/p∞ tại M = 0,8)/(p₀/p tại M = 1) = 1,524/1,893 = <b>{N(p115, 3)}</b>.", f"(11.5) p/p∞ = (p₀/p∞ at M = 0.8)/(p₀/p at M = 1) = 1.524/1.893 = <b>{N(p115, 3)}</b>.")],
                    L("Solution Manual: đồ thị cho M_cr = 0,74 và p/p∞ = 0,805.", "Solution Manual: the graph gives M_cr = 0.74 and p/p∞ = 0.805."))},
        {"num": "11.6 – 11.7", "src": "Anderson 6th, Problems 11.6, 11.7", "q": L("(11.6) Biên dạng trong dòng M∞ = 0,5; tại một điểm số Mach cục bộ là 0,86. Tính hệ số áp suất tại điểm đó. (11.7) Hình 11.5 của sách cho M∞ tăng từ 0,3 đến M_cr = 0,61, với M_A = 0,435 tại điểm hút mạnh nhất A khi M∞ = 0,3. Dùng Prandtl-Glauert để chứng minh M_cr ≈ 0,61, tức M_A = 1 khi M∞ = 0,61.", "(11.6) An airfoil in an M∞ = 0.5 stream; at one point the local Mach number is 0.86. Find the pressure coefficient there. (11.7) Figure 11.5 of the book raises M∞ from 0.3 to M_cr = 0.61, with M_A = 0.435 at the minimum-pressure point A when M∞ = 0.3. Use Prandtl-Glauert to show that M_cr ≈ 0.61, i.e. M_A = 1 when M∞ = 0.61."),
         "ans": sol(lang, L("Dòng nén được: C_p là hàm của hai số Mach.", "Compressible flow: C_p is a function of two Mach numbers."), L("Dùng p/p∞ = (p₀/p∞)/(p₀/p cục bộ) rồi C_p = (2/γM∞²)(p/p∞ − 1).", "Use p/p∞ = (p₀/p∞)/(local p₀/p) then C_p = (2/γM∞²)(p/p∞ − 1)."),
                    [L(f"(11.6) p₀/p∞ = 1,186; p₀/p (M = 0,86) = 1,621 ⇒ p/p∞ = {N(pr116, 4)} ⇒ <b>C_p = {N(cp116, 2)}</b>.", f"(11.6) p₀/p∞ = 1.186; p₀/p (M = 0.86) = 1.621 ⇒ p/p∞ = {N(pr116, 4)} ⇒ <b>C_p = {N(cp116, 2)}</b>."),
                     L(f"(11.7) Ở M∞ = 0,3: C_p,A = {N(cp_a, 3)} ⇒ C_p,0 = C_p,A√(1 − 0,09) = {N(cp0, 3)}.", f"(11.7) At M∞ = 0.3: C_p,A = {N(cp_a, 3)} ⇒ C_p,0 = C_p,A√(1 − 0.09) = {N(cp0, 3)}."),
                     L(f"Ở M∞ = 0,61: C_p,A = C_p,0/√(1 − 0,61²) = {N(cp0 / math.sqrt(1 - 0.61 ** 2), 3)} ⇒ p/p∞ = {N(1 + g * 0.61 ** 2 * cp0 / math.sqrt(1 - 0.61 ** 2) / 2, 3)}.", f"At M∞ = 0.61: C_p,A = C_p,0/√(1 − 0.61²) = {N(cp0 / math.sqrt(1 - 0.61 ** 2), 3)} ⇒ p/p∞ = {N(1 + g * 0.61 ** 2 * cp0 / math.sqrt(1 - 0.61 ** 2) / 2, 3)}."),
                     L(f"Giải M_A từ p₀/p: <b>M_A = {N(MA061, 3)} ≈ 1</b>, nên M_cr = 0,61.", f"Solving M_A from p₀/p: <b>M_A = {N(MA061, 3)} ≈ 1</b>, so M_cr = 0.61.")],
                    L("Solution Manual nội suy bảng nên có C_p,0 = −0,9969 (so với −0,9894 ở đây); kết luận giống nhau.", "The Solution Manual interpolates tables so it has C_p,0 = −0.9969 (against −0.9894 here); the conclusion is the same."))},
    ]
    return m
