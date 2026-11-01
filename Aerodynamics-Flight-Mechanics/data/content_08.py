# -*- coding: utf-8 -*-
"""Module 08: Dong luc bay ngang: Dutch roll, xoan oc, hoi tu lan. Nguon: Etkin & Reid 3rd ch.6 muc 6.7 (tr.187-190: ma tran A, Bang 6.6, 6.8, tri rieng B747), muc 6.8 (xoan oc),
EASA M08 SM4 (tr.4.7-4.9: dihedral, sweepback, keel, directional, Dutch roll)."""
import math
from aero import *
from common import num, ul, table, mcq


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    md = modes_b747_lat(); dr = md["dr"]; lam_roll = md["roll"]; lam_sp = md["spiral"]
    import numpy as np
    A = np.array(B747_LAT)
    coef = np.poly(A)
    Bc, Cc, Dc, Ec = coef[1], coef[2], coef[3], coef[4]
    Rcrit = Bc * Cc * Dc - Dc ** 2 - Bc ** 2 * Ec
    T_dr = 2 * math.pi / dr.imag; th_dr = math.log(2) / -dr.real; Nhalf = th_dr / T_dr
    th_roll = math.log(2) / -lam_roll; th_sp = math.log(2) / -lam_sp
    z_dr = -dr.real / abs(dr)
    sumd = -(2 * dr.real + lam_roll + lam_sp)
    zs = {}
    for dn in (0.25, 0.5, 1.0):
        B = A.copy(); B[2, 2] -= dn
        e = [x for x in np.linalg.eigvals(B) if x.imag > 1e-9][0]; zs[dn] = -e.real / abs(e)

    m = {"num": "08", "slug": "08-lateral-dynamics", "tag": L("Động lực ngang", "Lateral dynamics")}
    m["title"] = L("Động lực học ngang: hội tụ lăn, mode xoắn ốc và Dutch roll của B747", "Lateral dynamics: roll convergence, the spiral mode and the Dutch roll of the B747")
    m["src"] = L("Etkin &amp; Reid ch.6 mục 6.7 (tr. 187–190) và 6.8 · EASA Module 08, Sub-module 04 (tr. 4.7–4.9)", "Etkin &amp; Reid ch. 6 sec. 6.7 (pp. 187–190) and 6.8 · EASA Module 08, Sub-module 04 (pp. 4.7–4.9)")
    m["intro"] = L("Module 04 xét ổn định dọc và hai mode dọc. Module này làm tương tự cho chuyển động ngang: bốn biến [v, p, r, φ] và ma trận hệ thống của B747 in trong Etkin, cho ba mode: hội tụ lăn (rất nhanh), xoắn ốc (rất chậm) và Dutch roll (dao động tắt yếu). Ta tính lại trị riêng, các thời gian đặc trưng của Bảng 6.8, các tiêu chí E và R, và dùng demo mô phỏng để xem tác dụng của bộ giảm xoay.",
                   "Module 04 handled longitudinal stability and the two longitudinal modes. This module does the same for lateral motion: four variables [v, p, r, φ] and the B747 system matrix printed in Etkin, giving three modes: roll convergence (very fast), the spiral (very slow) and the Dutch roll (a lightly damped oscillation). We recompute the eigenvalues, the characteristic times of Table 6.8, the criteria E and R, and use a simulation demo to see the effect of a yaw damper.")
    m["mapping"] = {
        "easa": L("Sub-module 04 (tr. 4.7 ổn định ngang: dihedral, sweepback, keel; tr. 4.8 ổn định hướng; tr. 4.9 Dutch roll; Hình 4-9, 4-10, 4-11); Q4-5, Q4-6", "Sub-module 04 (p. 4.7 lateral stability: dihedral, sweepback, keel; p. 4.8 directional stability; p. 4.9 Dutch roll; Figures 4-9, 4-10, 4-11); Q4-5, Q4-6"),
        "anderson": L("Không có (Anderson không có chương ổn định động)", "None (Anderson has no dynamic-stability chapter)"),
        "etkin": L("Ch.6 mục 6.7 Lateral Modes of a Jet Transport (Bảng 6.6, 6.7, 6.8, 6.9; tr. 187–190), mục 6.8 Spiral stability; ch.3 mục 3.8–3.11 (đạo hàm ngang); Bài tập 6.4, 6.5, 6.11", "Ch.6 sec. 6.7 Lateral Modes of a Jet Transport (Tables 6.6, 6.7, 6.8, 6.9; pp. 187–190), sec. 6.8 Spiral stability; ch. 3 sec. 3.8–3.11 (lateral derivatives); Exercises 6.4, 6.5, 6.11"),
        "note": L("Etkin cho ma trận và trị riêng; EASA cho ý nghĩa vật lý của dihedral, keel và Dutch roll. Ma trận A chép từ ảnh trang Etkin tr. 187 và được kiểm lại bằng đa thức đặc trưng in trong sách.", "Etkin gives the matrix and eigenvalues; EASA gives the physical meaning of dihedral, keel effect and Dutch roll. The matrix A was copied from the image of Etkin p. 187 and checked against the characteristic polynomial printed in the book."),
    }
    parts = []
    parts.append({"title": L("Đạo hàm ổn định ngang", "Lateral stability derivatives"),
                  "bullets": [L("Ba mômen ngang: lực bên Y, mômen lăn l và mômen xoay n", "Three lateral quantities: side force Y, rolling moment l and yawing moment n"),
                              L("C_nβ dương: ổn định hướng (weathercock); C_lβ âm: hiệu ứng dihedral ổn định", "C_nβ positive: directional (weathercock) stability; C_lβ negative: a stabilising dihedral effect"),
                              L("C_lp âm và C_nr âm: giảm lăn và giảm xoay", "C_lp negative and C_nr negative: roll damping and yaw damping")],
                  "slides": [{"title": L("Bảng 6.6 của Etkin: các đạo hàm không thứ nguyên của B747", "Etkin Table 6.6: nondimensional derivatives of the B747"),
                              "body": table([L("Đạo hàm", "Derivative"), "C_y", "C_l", "C_n"], [["β", N(-0.8771, 4), N(-0.2797, 4), N(0.1946, 4)], ["p̂", N(0, 4), N(-0.3295, 4), N(-0.04073, 5)], ["r̂", N(0, 4), N(0.304, 3), N(-0.2737, 4)]]) +
                              ul(L("C_nβ = +0,1946 > 0: đuôi đứng đưa mũi về hướng gió (EASA tr. 4.8)", "C_nβ = +0.1946 > 0: the fin turns the nose into the wind (EASA p. 4.8)"), L("C_lβ = −0,2797 < 0: dihedral và cánh xuôi cho hiệu ứng ổn định (EASA tr. 4.7)", "C_lβ = −0.2797 < 0: dihedral and sweep give a stabilising effect (EASA p. 4.7)"), L("C_lp = −0,3295 < 0 và C_nr = −0,2737 < 0: giảm lăn và giảm xoay", "C_lp = −0.3295 < 0 and C_nr = −0.2737 < 0: roll and yaw damping")),
                              "explain": L("Dấu của từng đạo hàm cho biết mỗi hiệu ứng ổn định hay mất ổn định; độ lớn quyết định mode nào mạnh.", "The sign of each derivative says whether an effect is stabilising or destabilising; the magnitude decides which mode is strong.")}]})
    parts.append({"title": L("Ma trận hệ thống và đa thức đặc trưng", "The system matrix and the characteristic polynomial"),
                  "bullets": [L("Trạng thái x = [v, p, r, φ], ẋ = A·x", "State x = [v, p, r, φ], ẋ = A·x"),
                              L("Đa thức bậc 4: λ⁴ + Bλ³ + Cλ² + Dλ + E = 0", "A fourth-order polynomial: λ⁴ + Bλ³ + Cλ² + Dλ + E = 0"),
                              L("Điều kiện ổn định Routh: mọi hệ số dương và R = BCD − D² − B²E > 0", "Routh stability condition: all coefficients positive and R = BCD − D² − B²E > 0")],
                  "slides": [{"title": L("Tính lại các hệ số và tiêu chí (Etkin 6.7,2)", "Recomputing the coefficients and the criteria (Etkin 6.7,2)"),
                              "body": table([L("Hệ số", "Coefficient"), L("Tính lại", "Recomputed"), L("In trong sách", "Printed")], [["B", N(Bc, 4), "0.6358" if lang == "en" else "0,6358"], ["C", N(Cc, 4), "0.9388" if lang == "en" else "0,9388"], ["D", N(Dc, 4), "0.5114" if lang == "en" else "0,5114"], ["E", N(Ec, 6), "0.003682" if lang == "en" else "0,003682"], ["R = BCD − D² − B²E", N(Rcrit, 5), "0.04223" if lang == "en" else "0,04223"]]) +
                              f"<p class='pill'>{L('E và R đều dương nên không có mode mất ổn định. Khác biệt nhỏ ở R do sách làm tròn các hệ số trước khi nhân.', 'E and R are both positive so there are no unstable modes. The small difference in R is because the book rounds the coefficients before multiplying.')}</p>",
                              "explain": L("E > 0 loại trừ nghiệm thực dương nhỏ (xoắn ốc mất ổn định); R > 0 loại trừ dao động tăng dần.", "E > 0 rules out a small positive real root (an unstable spiral); R > 0 rules out a growing oscillation.")}]})
    parts.append({"title": L("Ba mode ngang", "The three lateral modes"),
                  "bullets": [L("Hội tụ lăn: λ = −0,562, t½ ≈ 1,2 s", "Roll convergence: λ = −0.562, t½ ≈ 1.2 s"),
                              L("Xoắn ốc: λ = −0,0073, t½ ≈ 95 s", "Spiral: λ = −0.0073, t½ ≈ 95 s"),
                              L("Dutch roll: λ = −0,0330 ± 0,9465i, T ≈ 6,64 s", "Dutch roll: λ = −0.0330 ± 0.9465i, T ≈ 6.64 s")],
                  "slides": [{"title": L("Bảng 6.8 tính lại từ trị riêng", "Table 6.8 recomputed from the eigenvalues"),
                              "body": table([L("Mode", "Mode"), L("Trị riêng", "Eigenvalue"), L("T (s)", "T (s)"), L("t½ (s)", "t½ (s)"), "N½"],
                                            [[L("Xoắn ốc", "Spiral"), N(lam_sp, 5), "–", N(th_sp, 0), "–"], [L("Hội tụ lăn", "Roll convergence"), N(lam_roll, 4), "–", N(th_roll, 2), "–"], ["Dutch roll", f"{N(dr.real, 4)} ± {N(dr.imag, 4)}i", N(T_dr, 2), N(th_dr, 0), N(Nhalf, 2)]]) +
                              f"<p class='pill'>{L('Khớp Bảng 6.8 của Etkin: 95 s, 1,23 s; Dutch roll T = 6,64 s, t½ = 21 s, N½ = 3,16 chu kỳ. Hệ số tắt dần của Dutch roll ζ = ', 'Matches Etkin Table 6.8: 95 s, 1.23 s; Dutch roll T = 6.64 s, t½ = 21 s, N½ = 3.16 cycles. The Dutch roll damping ratio is ζ = ')}{N(z_dr, 3)}</p>",
                              "explain": L("Mode xoắn ốc ổn định nhưng chậm đến mức phi công coi nó là \"trôi\" dần; Dutch roll tắt yếu (ζ = 0,035) nên cần bộ giảm xoay.", "The spiral is stable but so slow that pilots see it as a gradual drift; the Dutch roll is lightly damped (ζ = 0.035) which is why a yaw damper is needed.")},
                             {"title": L("Hình dạng từng mode", "The shape of each mode"),
                              "body": ul(L("Xoắn ốc: chủ yếu xoay quanh trục đứng với trượt ngang rất nhỏ, tức một vòng nghiêng thật (Etkin 6.7)", "Spiral: mainly yawing at nearly zero sideslip with some rolling, i.e. a truly banked turn (Etkin 6.7)"),
                                         L("Hội tụ lăn: tốc độ lăn p tắt nhanh sau một nhiễu lăn", "Roll convergence: the roll rate p dies out quickly after a rolling disturbance"),
                                         L("Dutch roll: xoay và lăn kết hợp, chu kỳ gần bằng chu kỳ ngắn dọc (6,6 s so với 7,1 s)", "Dutch roll: coupled yaw and roll with a period close to the longitudinal short period (6.6 s against 7.1 s)")),
                              "explain": L("Etkin bài 6.11: ở Dutch roll hai đầu cánh chuyển động ngược pha giống người trượt băng.", "Etkin Exercise 6.11: in the Dutch roll the two wing tips move out of phase like an ice skater.")}]})
    parts.append({"title": L("Bộ giảm xoay và điều khiển", "The yaw damper and control"),
                  "bullets": [L("Dutch roll tắt yếu ở máy bay cánh xuôi bay cao", "The Dutch roll is lightly damped on high-flying swept-wing aircraft"),
                              L("Bộ giảm xoay đưa tốc độ xoay r về bánh lái để tăng tắt dần", "A yaw damper feeds yaw rate r to the rudder to add damping"),
                              L("Mô hình đơn giản: trừ ΔN_r khỏi phần tử r-r của ma trận A", "Simple model: subtract ΔN_r from the r-r element of matrix A")],
                  "slides": [{"title": L("Tăng tắt dần bằng bộ giảm xoay (mô hình đơn giản)", "Adding damping with a yaw damper (simple model)"),
                              "body": table([L("ΔN_r (1/s)", "ΔN_r (1/s)"), L("ζ của Dutch roll", "Dutch-roll ζ")], [["0", N(z_dr, 3)], ["0,25" if lang == "vi" else "0.25", N(zs[0.25], 3)], ["0,5" if lang == "vi" else "0.5", N(zs[0.5], 3)], ["1", N(zs[1.0], 3)]]) +
                              f"<p class='pill'>{L('Chỉ là mô hình đơn giản hóa: bộ giảm xoay thật dùng bánh lái với độ trễ và giới hạn; xem Etkin 8.7', 'This is a simplified model only: a real yaw damper acts through the rudder with lag and limits; see Etkin 8.7')}</p>",
                              "explain": L("Thêm một chút giảm xoay đã đưa ζ từ 0,035 lên khoảng 0,3: mô phỏng ở demo cho thấy dao động tắt trong vài giây.", "A modest added yaw damping raises ζ from 0.035 to about 0.3: the demo shows the oscillation dying in a few seconds.")}]})
    parts.append({"title": L("Tổng kết dọc và ngang", "Longitudinal and lateral compared"),
                  "bullets": [L("Cả hai chuyển động đều có một dao động tắt yếu và một dao động nhanh hơn", "Both motions have a lightly damped oscillation and a faster one"),
                              L("Tổng độ tắt dần: hệ số λ³ = −ΣRe (Etkin Bài tập 6.4)", "The sum of dampings: the λ³ coefficient equals −ΣRe (Etkin Exercise 6.4)"),
                              L("Ổn định mọi mode là điều kiện cần, không phải đủ, cho chất lượng bay tốt", "Stability of every mode is necessary but not sufficient for good handling")],
                  "slides": [{"title": L("Bảng so sánh B747", "B747 comparison table"),
                              "body": table([L("Mode", "Mode"), L("Chu kỳ (s)", "Period (s)"), "ζ", L("t½ (s)", "t½ (s)")],
                                            [["Phugoid", "93,5" if lang == "vi" else "93.5", "0,049" if lang == "vi" else "0.049", "211"], [L("Chu kỳ ngắn", "Short period"), "7,08" if lang == "vi" else "7.08", "0,387" if lang == "vi" else "0.387", "1,86" if lang == "vi" else "1.86"], ["Dutch roll", N(T_dr, 2), N(z_dr, 3), N(th_dr, 0)], [L("Xoắn ốc", "Spiral"), "–", "–", N(th_sp, 0)], [L("Hội tụ lăn", "Roll convergence"), "–", "–", N(th_roll, 2)]]) +
                              ul(L(f"Tổng độ tắt dần ngang: −ΣRe = {N(sumd, 4)} = hệ số λ³ ({N(Bc, 4)})", f"Lateral sum of dampings: −ΣRe = {N(sumd, 4)} = the λ³ coefficient ({N(Bc, 4)})")),
                              "explain": L("Bảng này gom kết quả module 04 và 08: sáu mode, hai nhóm thời gian rất khác nhau (giây so với phút).", "This table collects modules 04 and 08: six modes in two very different time scales (seconds against minutes).")}]})
    m["parts"] = parts
    m["formula_label"] = L("Đa thức đặc trưng, tiêu chí Routh và thời gian đặc trưng", "Characteristic polynomial, Routh criteria and characteristic times")
    m["formula_math"] = ("λ⁴ + Bλ³ + Cλ² + Dλ + E = 0  ·  E &gt; 0  ·  R = BCD − AD² − B²E &gt; 0<br>t½ = ln 2/|σ|  ·  T = 2π/ω  ·  N½ = t½/T  ·  ζ = −σ/|λ|" if lang == "vi" else
                         "λ⁴ + Bλ³ + Cλ² + Dλ + E = 0  ·  E &gt; 0  ·  R = BCD − AD² − B²E &gt; 0<br>t½ = ln 2/|σ|  ·  T = 2π/ω  ·  N½ = t½/T  ·  ζ = −σ/|λ|")
    m["legend"] = [("v, p, r, φ", L("trượt ngang, tốc độ lăn, tốc độ xoay, góc nghiêng", "sideslip velocity, roll rate, yaw rate, bank angle")), ("E, R", L("tiêu chí ổn định", "stability criteria")), ("t½", L("thời gian giảm một nửa", "time to half amplitude")), ("N½", L("số chu kỳ để giảm một nửa", "cycles to half amplitude")), ("ζ", L("hệ số tắt dần", "damping ratio")), ("ΔN_r", L("giảm xoay thêm", "added yaw damping"))]
    m["history_title"] = L("Tên gọi Dutch roll", "The name \"Dutch roll\"")
    m["history"] = L("Etkin (bài tập 6.11) giải thích rằng tên Dutch roll đến từ sự giống nhau với chuyển động của người trượt băng Hà Lan; ông đề nghị cầm một mô hình máy bay ở hai đầu cánh và tập thực hiện chuyển động đó trước gương. Mode này trở nên quan trọng hơn khi máy bay phản lực cánh xuôi bay cao, nơi ổn định tự nhiên yếu và bộ giảm xoay thành thiết bị chuẩn.",
                     "Etkin (Exercise 6.11) explains that the name Dutch roll comes from the resemblance to the motion of a Dutch ice skater; he suggests holding a model aeroplane by its wing tips and practising the motion in front of a mirror. The mode became more important as swept-wing jets flew high, where natural damping is weak and the yaw damper became standard equipment.")
    m["case_title"] = L("Tình huống: nhiễu trượt ngang 10 ft/s", "Case: a 10 ft/s sideslip disturbance")
    m["case"] = L(f"Với B747 trong Etkin, một nhiễu trượt ngang v = 10 ft/s ban đầu gây dao động xoay-lăn chu kỳ {N(T_dr, 1)} s, biên độ chỉ giảm nửa sau {N(th_dr, 0)} s ({N(Nhalf, 1)} chu kỳ). Khi thêm ΔN_r = 0,5 vào mô hình, ζ tăng lên {N(zs[0.5], 2)} và dao động tắt gần hẳn trong vài giây (xem demo). Đây là lý do bộ giảm xoay là thiết bị bắt buộc về tiện nghi và an toàn.",
                  f"For the B747 in Etkin, an initial 10 ft/s sideslip disturbance causes a yaw-roll oscillation of period {N(T_dr, 1)} s whose amplitude only halves after {N(th_dr, 0)} s ({N(Nhalf, 1)} cycles). Adding ΔN_r = 0.5 to the model raises ζ to {N(zs[0.5], 2)} and the oscillation almost vanishes within seconds (see the demo). This is why a yaw damper is essential for comfort and safety.")
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L("(1) Xoắn ốc ổn định (σ < 0) nhưng rất chậm; sách chỉ nói không có mode mất ổn định. (2) Ổn định hướng quá mạnh so với ổn định ngang sinh Dutch roll, quá yếu sinh xoắn ốc: hai đòi hỏi mâu thuẫn. (3) ΔN_r trong demo là mô hình đơn giản, không phải vòng điều khiển bánh lái. (4) Ma trận A cho điều kiện bay cụ thể (u₀ = 774 ft/s); đổi tốc độ hay độ cao thì trị riêng đổi. (5) EASA mô tả định tính; không dùng số liệu của EASA để tính Dutch roll.",
                  "(1) The spiral is stable (σ < 0) but very slow; the book only says there is no unstable mode. (2) Directional stability that is strong relative to lateral stability makes Dutch roll, too weak makes the spiral: the two demands conflict. (3) ΔN_r in the demo is a simplified model, not the rudder control loop. (4) Matrix A is for one flight condition (u₀ = 774 ft/s); change speed or altitude and the eigenvalues change. (5) EASA is qualitative; do not use its figures to compute the Dutch roll.")
    m["nb_desc"] = L("Notebook nhập ma trận ngang B747 từ Etkin tr. 187, tính lại đa thức đặc trưng, trị riêng, Bảng 6.8, tiêu chí E và R, ζ khi có bộ giảm xoay, và assert các đáp án quiz.", "The notebook enters the B747 lateral matrix from Etkin p. 187, recomputes the characteristic polynomial, eigenvalues, Table 6.8, the criteria E and R, ζ with a yaw damper, and asserts the quiz answers.")

    SD = lambda i: 800 + i
    SUP = L("Bổ sung (biên soạn)", "Supplementary (authored)")
    Q = lambda i, src, q, r, w, ex, det=None: mcq(SD(i), src, q, r, w, ex, det)
    ES = L("Etkin &amp; Reid, mục 6.7", "Etkin &amp; Reid, sec. 6.7")
    book = [
        Q(1, ES, L("Trị riêng Dutch roll của B747 là λ = −0,03301 ± 0,94655i. Chu kỳ là:", "The B747 Dutch-roll eigenvalue is λ = −0.03301 ± 0.94655i. The period is:"), f"{N(T_dr, 2)} s", [f"{N(T_dr * 14, 1)} s", f"{N(T_dr / 2, 2)} s", f"{N(2 * math.pi / 0.03301, 0)} s"], L("T = 2π/ω.", "T = 2π/ω."), L(f"<p>T = 2π/0,94655 = {N(T_dr, 3)} s (Etkin Bảng 6.8: 6,64 s).</p>", f"<p>T = 2π/0.94655 = {N(T_dr, 3)} s (Etkin Table 6.8: 6.64 s).</p>")),
        Q(2, ES, L("Mode xoắn ốc có λ = −0,0072973. Thời gian giảm một nửa là:", "The spiral mode has λ = −0.0072973. The time to half amplitude is:"), f"{N(th_sp, 0)} s", [f"{N(th_sp / 10, 0)} s", f"{N(th_sp * 3, 0)} s", f"{N(1 / 0.0072973, 0)} s"], L("t½ = ln 2/|σ|.", "t½ = ln 2/|σ|."), L(f"<p>t½ = 0,6931/0,0072973 = {N(th_sp, 1)} s (Bảng 6.8: 95 s).</p>", f"<p>t½ = 0.6931/0.0072973 = {N(th_sp, 1)} s (Table 6.8: 95 s).</p>")),
        Q(3, ES, L("Mode hội tụ lăn có λ = −0,56248. Thời gian giảm một nửa là:", "The roll-convergence mode has λ = −0.56248. The time to half amplitude is:"), f"{N(th_roll, 2)} s", [f"{N(th_roll * 10, 1)} s", f"{N(1 / 0.56248 * 2, 2)} s", f"{N(th_roll / 2, 2)} s"], L("t½ = ln 2/0,56248.", "t½ = ln 2/0.56248.")),
        Q(4, ES, L("Số chu kỳ để Dutch roll giảm một nửa biên độ, N½ = t½/T, là:", "The number of cycles for the Dutch roll to halve, N½ = t½/T, is:"), N(Nhalf, 2), [N(Nhalf * 3, 2), N(Nhalf / 3, 2), N(th_dr, 2)], L("t½ = 21,0 s; T = 6,64 s.", "t½ = 21.0 s; T = 6.64 s.")),
        Q(5, ES, L("Hệ số tắt dần ζ của Dutch roll B747 xấp xỉ:", "The damping ratio ζ of the B747 Dutch roll is about:"), N(z_dr, 3), [N(0.387, 3), N(0.5, 3), N(0.0, 3)], L("ζ = 0,03301/|λ| với |λ| = 0,947; tắt yếu.", "ζ = 0.03301/|λ| with |λ| = 0.947; lightly damped.")),
        Q(6, ES, L("Với đa thức λ⁴ + 0,6358λ³ + 0,9388λ² + 0,5114λ + 0,003682, tiêu chí R = BCD − D² − B²E xấp xỉ:", "For the polynomial λ⁴ + 0.6358λ³ + 0.9388λ² + 0.5114λ + 0.003682 the criterion R = BCD − D² − B²E is about:"), N(Rcrit, 4), [N(Rcrit * 10, 3), N(-Rcrit, 4), N(0.003682, 4)], L("R > 0 nên không có dao động mất ổn định.", "R > 0 so there is no unstable oscillation.")),
        Q(7, L("Etkin &amp; Reid, Bài tập 6.4", "Etkin &amp; Reid, Exercise 6.4"), L("Hệ số của λ³ (0,6358) bằng −ΣRe λ của bốn trị riêng. Giá trị tính từ trị riêng là:", "The λ³ coefficient (0.6358) equals −ΣRe λ of the four eigenvalues. The value computed from the eigenvalues is:"), N(sumd, 4), [N(sumd / 2, 4), N(0.9388, 4), N(2 * 0.03301, 4)], L("2(0,03301) + 0,56248 + 0,0072973.", "2(0.03301) + 0.56248 + 0.0072973.")),
        Q(8, L("Etkin &amp; Reid, mục 6.7 (Hình dạng mode)", "Etkin &amp; Reid, sec. 6.7 (mode shapes)"), L("Mode nào của B747 chủ yếu là xoay ở trượt ngang gần bằng không (vòng nghiêng thật)?", "Which B747 mode is mainly yawing at nearly zero sideslip (a truly banked turn)?"), L("Mode xoắn ốc", "The spiral mode"), [L("Hội tụ lăn", "Roll convergence"), L("Dutch roll", "The Dutch roll"), L("Phugoid", "The phugoid")], L("Etkin 6.7 mô tả mode này là vòng nghiêng thật.", "Etkin 6.7 describes this mode as a truly banked turn.")),
    ]
    gen = [
        Q(11, SUP, L("Dấu của C_nβ trong B747 là dương. Điều đó có nghĩa là:", "The sign of C_nβ for the B747 is positive. That means:"), L("ổn định hướng (đuôi đứng đưa mũi về hướng gió)", "directional stability (the fin turns the nose into the wind)"), [L("mất ổn định hướng", "directional instability"), L("ổn định ngang", "lateral stability"), L("mất ổn định dọc", "longitudinal instability")], L("C_nβ = +0,1946 trong Bảng 6.6.", "C_nβ = +0.1946 in Table 6.6.")),
        Q(12, SUP, L("C_lp âm có nghĩa là:", "A negative C_lp means:"), L("giảm lăn: tốc độ lăn tự tắt", "roll damping: a roll rate damps itself"), [L("tăng lăn", "roll amplification"), L("ổn định hướng", "directional stability"), L("không ảnh hưởng", "no effect")], L("C_lp = −0,3295.", "C_lp = −0.3295.")),
        Q(13, SUP, L("Thêm giảm xoay ΔN_r = 0,5 làm ζ của Dutch roll tăng từ 0,035 lên khoảng:", "Adding yaw damping ΔN_r = 0.5 raises the Dutch-roll ζ from 0.035 to about:"), N(zs[0.5], 2), [N(0.035, 2), N(0.9, 2), N(0.05, 2)], L("Tính trực tiếp bằng trị riêng của A đã sửa.", "Computed directly from the eigenvalues of the modified A.")),
        Q(14, SUP, L("Mode ngang nào có thời gian đặc trưng gần nhất với chu kỳ ngắn dọc?", "Which lateral mode has a time scale closest to the longitudinal short period?"), L("Dutch roll (6,6 s so với 7,1 s)", "The Dutch roll (6.6 s against 7.1 s)"), [L("Xoắn ốc", "The spiral"), L("Hội tụ lăn (nhưng không dao động)", "Roll convergence (but non-oscillatory)"), L("Không mode nào", "None")], L("Cả hai là dao động nhanh, tắt dần.", "Both are fast damped oscillations.")),
        Q(15, SUP, L("Ổn định hướng quá mạnh so với ổn định ngang dẫn tới:", "Directional stability that is too strong relative to lateral stability leads to:"), L("Dutch roll tắt yếu", "a lightly damped Dutch roll"), [L("xoắn ốc nhanh chóng ổn định", "a quickly stable spiral"), L("phugoid bất ổn", "an unstable phugoid"), L("mất lực nâng", "loss of lift")], L("Ngược lại, ổn định hướng yếu sinh xoắn ốc mất ổn định.", "Conversely, weak directional stability produces a spiral instability.")),
        Q(16, SUP, L("Vì sao mode xoắn ốc ổn định vẫn được xem là nguy hiểm tiềm tàng?", "Why can a stable spiral mode still be considered a potential hazard?"), L("Vì nó chậm đến mức phi công không nhận ra máy bay đang nghiêng dần", "Because it is so slow that the pilot may not notice the aircraft slowly banking"), [L("Vì nó tăng biên độ nhanh", "Because it grows quickly"), L("Vì nó đòi hỏi bánh lái", "Because it requires rudder"), L("Vì nó chỉ xảy ra ở mặt đất", "Because it happens only on the ground")], L("t½ = 95 s.", "t½ = 95 s.")),
    ]
    m["quiz_sets"] = [
        {"key": "etkin", "title": L("Sách 3: Etkin &amp; Reid, mục 6.7 và Bài tập 6.4 (tính lại bằng Python từ ma trận A in trong sách)", "Book 3: Etkin &amp; Reid, sec. 6.7 and Exercise 6.4 (recomputed in Python from the A matrix printed in the book)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập bổ sung (biên soạn thêm, đáp án tự kiểm chứng bằng tính toán)", "Additional practice (authored, answers self-verified by computation)"), "items": gen},
    ]
    m["problems_intro"] = L("Hai bài giải bằng số liệu B747 của Etkin; các đáp án khớp số in trong sách (Bảng 6.8, phương trình 6.7,2).", "Two problems solved with Etkin's B747 data; the answers match the numbers printed in the book (Table 6.8, equation 6.7,2).")
    m["problems"] = [
        {"num": "6.7", "src": "Etkin & Reid 3rd, sec. 6.7, Table 6.8", "q": L("Từ ma trận A ngang của B747, tìm ba mode và các thời gian đặc trưng (Bảng 6.8).", "From the B747 lateral matrix A find the three modes and their characteristic times (Table 6.8)."),
         "ans": L(f"<p>Trị riêng: xoắn ốc <b>{N(lam_sp, 5)}</b>, hội tụ lăn <b>{N(lam_roll, 5)}</b>, Dutch roll <b>{N(dr.real, 5)} ± {N(dr.imag, 5)}i</b>.</p><p>t½: xoắn ốc {N(th_sp, 1)} s; hội tụ lăn {N(th_roll, 2)} s; Dutch roll {N(th_dr, 1)} s, T = {N(T_dr, 2)} s, N½ = {N(Nhalf, 2)}.</p>", f"<p>Eigenvalues: spiral <b>{N(lam_sp, 5)}</b>, roll convergence <b>{N(lam_roll, 5)}</b>, Dutch roll <b>{N(dr.real, 5)} ± {N(dr.imag, 5)}i</b>.</p><p>t½: spiral {N(th_sp, 1)} s; roll convergence {N(th_roll, 2)} s; Dutch roll {N(th_dr, 1)} s, T = {N(T_dr, 2)} s, N½ = {N(Nhalf, 2)}.</p>")},
        {"num": "6.4", "src": "Etkin & Reid 3rd, Exercise 6.4", "q": L("Kiểm tra cho B747 ngang: hệ số λ³ của đa thức đặc trưng bằng −ΣRe.", "Check for the lateral B747 that the λ³ coefficient of the characteristic polynomial equals −ΣRe."),
         "ans": L(f"<p>−ΣRe = 2×{N(-dr.real, 5)} + {N(-lam_roll, 5)} + {N(-lam_sp, 6)} = <b>{N(sumd, 5)}</b>, trùng hệ số 0,6358 của (6.7,2).</p><p>E = {N(Ec, 6)} &gt; 0 và R = {N(Rcrit, 5)} &gt; 0 nên mọi mode ổn định.</p>", f"<p>−ΣRe = 2×{N(-dr.real, 5)} + {N(-lam_roll, 5)} + {N(-lam_sp, 6)} = <b>{N(sumd, 5)}</b>, equal to the 0.6358 of (6.7,2).</p><p>E = {N(Ec, 6)} &gt; 0 and R = {N(Rcrit, 5)} &gt; 0 so every mode is stable.</p>")},
    ]
    return m
