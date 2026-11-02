# -*- coding: utf-8 -*-
"""Module 09: Dong the co ban va hinh tru. Nguon: Anderson 6th ch.3 (3.9-3.16: dong so cap, hinh tru, Kutta-Joukowski; Bai 3.15-3.22); EASA M08 SM2 (Bernoulli, luu so, tr.2.3).
Doi chieu Solution Manual (4th): 3.15, 3.16, 3.17, 3.18, 3.19, 3.20 khop."""
import math
from aero import *
from common import num, ul, table, mcq, sol


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    cp90 = 1 - 4 * 1.0
    # 3.18
    rho = 1.23; Gam318 = 6 / (rho * 30)
    # 3.19
    rho_s = 0.002377; Vs = 120 * 5280 / 3600; q = 0.5 * rho_s * Vs ** 2
    D_str = q * (25 * 2 / 12) * 1.0; D_wire = q * (80 * (3 / 32) / 12) * 1.0; D_sum = D_str + D_wire
    D0 = q * 230 * 0.036; frac = D_sum / D0
    # 3.21
    psi2 = 1.2 - 1 / 1.2
    lo, hi = 1.0001, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if (mid - 1 / mid) < 2 * psi2: lo = mid
        else: hi = mid
    r3 = (lo + hi) / 2
    # 3.22
    a_sl = speed_of_sound(T0); Vloc = 250 * 0.44704; Vinf = Vloc / 2; Mloc = Vloc / a_sl
    # cylinder example with circulation
    GV = 0.5                                   # Gamma/(4 pi V R)
    th_stag = math.degrees(math.asin(-GV))     # sin(theta) = -Gamma/(4 pi V R)
    Vmax_surf = 2 + 2 * GV                     # |V_theta|/V max on the surface at theta = -90 deg
    CL_cyl = 4 * math.pi * GV * 2 / 2          # not used

    m = {"num": "09", "slug": "09-potential-flow", "tag": L("Dòng thế", "Potential flow")}
    m["title"] = L("Dòng thế cơ bản: nguồn, xoáy, lưỡng cực và dòng quanh hình trụ", "Elementary potential flows: source, vortex, doublet and flow past a cylinder")
    m["src"] = L("Anderson ch.3 (mục 3.9–3.16; Bài 3.15–3.22) · EASA Module 08, Sub-module 02 (tr. 2.3)", "Anderson ch. 3 (sec. 3.9–3.16; Problems 3.15–3.22) · EASA Module 08, Sub-module 02 (p. 2.3)")
    m["intro"] = L("Module 02 dùng Bernoulli và hệ số lực nâng như công cụ có sẵn. Module này cho thấy chúng đến từ đâu: với dòng không nhớt, không nén được và không xoáy, vận tốc là gradient của một hàm thế φ, và có hàm dòng ψ. Cộng các dòng sơ cấp (đều, nguồn, xoáy, lưỡng cực) ta được dòng quanh hình trụ, có áp suất C_p = 1 − 4 sin²θ, lực cản bằng không (nghịch lý d'Alembert) và, khi thêm lưu số Γ, lực nâng L′ = ρVΓ. Mọi bài tập đều có lời giải theo bốn bước: đề nói gì, ý tưởng, các bước, kiểm tra.",
                   "Module 02 used Bernoulli and the lift coefficient as ready-made tools. This module shows where they come from: for inviscid, incompressible, irrotational flow the velocity is the gradient of a potential φ and there is a stream function ψ. Adding the elementary flows (uniform, source, vortex, doublet) gives flow past a cylinder with C_p = 1 − 4 sin²θ, zero drag (d'Alembert's paradox) and, with circulation Γ added, a lift L′ = ρVΓ. Every problem is solved in four steps: what the problem says, the idea, the steps, a check.")
    m["mapping"] = {
        "easa": L("Sub-module 02 (tr. 2.3 Bernoulli và dòng cận âm: đường dòng, vận tốc và áp suất; tr. 2.11 lực nâng)", "Sub-module 02 (p. 2.3 Bernoulli and subsonic flow: streamlines, velocity and pressure; p. 2.11 lift)"),
        "anderson": L("Ch.3 mục 3.7 Laplace, 3.9 dòng đều, 3.10 nguồn và hố, 3.11 xoáy, 3.12 lưỡng cực, 3.13 hình trụ không nâng, 3.15 hình trụ có nâng, 3.16 Kutta-Joukowski; Bài 3.15–3.22", "Ch.3 sec. 3.7 Laplace, 3.9 uniform flow, 3.10 source and sink, 3.11 vortex, 3.12 doublet, 3.13 non-lifting cylinder, 3.15 lifting cylinder, 3.16 Kutta-Joukowski; Problems 3.15–3.22"),
        "etkin": L("Không có (Etkin &amp; Reid dùng kết quả khí động, không dẫn xuất dòng thế)", "None (Etkin &amp; Reid use aerodynamic results and do not derive potential flow)"),
        "note": L("Nền toán cho module 02 (lưu số, Kutta–Joukowski) và module 05 (xoáy, Biot-Savart).", "The mathematical basis for module 02 (circulation, Kutta–Joukowski) and module 05 (vortices, Biot-Savart)."),
    }
    parts = []
    parts.append({"title": L("Hàm dòng, hàm thế và các dòng sơ cấp", "Stream function, potential and the elementary flows"),
                  "bullets": [L("Dòng không xoáy: V = ∇φ; dòng không nén được: ∇·V = 0, nên ∇²φ = 0 (phương trình Laplace)", "Irrotational flow: V = ∇φ; incompressible flow: ∇·V = 0, so ∇²φ = 0 (Laplace's equation)"),
                              L("Đường ψ = hằng số là đường dòng", "Lines of constant ψ are streamlines"),
                              L("Vì Laplace tuyến tính, có thể cộng các nghiệm đơn giản", "Laplace's equation is linear, so simple solutions can be added")],
                  "slides": [{"title": L("Bốn dòng sơ cấp", "The four elementary flows"),
                              "body": table([L("Dòng", "Flow"), "ψ", "φ", L("Vận tốc", "Velocity")],
                                            [[L("Đều", "Uniform"), "V r sin θ", "V r cos θ", "V_r = V cos θ, V_θ = −V sin θ"],
                                             [L("Nguồn (Λ)", "Source (Λ)"), "Λθ/2π", "(Λ/2π) ln r", "V_r = Λ/(2πr), V_θ = 0"],
                                             [L("Xoáy (Γ)", "Vortex (Γ)"), "−(Γ/2π) ln r", "−Γθ/2π", "V_r = 0, V_θ = −Γ/(2πr)"],
                                             [L("Lưỡng cực (κ)", "Doublet (κ)"), "−(κ/2π) sin θ/r", "(κ/2π) cos θ/r", "V_r = −κ cos θ/(2πr²), V_θ = −κ sin θ/(2πr²)"]]) +
                              f"<p class='pill'>{L('Bài 3.9–3.14 chứng minh các dòng này thỏa Laplace; xoáy và nguồn không xoáy trừ tại gốc', 'Problems 3.9–3.14 prove these flows satisfy Laplace; the source and vortex are irrotational except at the origin')}</p>",
                              "explain": L("Lưỡng cực là nguồn và hố đặt sát nhau với cường độ tăng khi khoảng cách giảm; nó là \"hình trụ thu nhỏ\" cho bước sau.", "A doublet is a source and a sink brought together with strength rising as the spacing shrinks; it is the \"shrunken cylinder\" for the next step.")}]})
    parts.append({"title": L("Hình trụ không nâng", "The non-lifting cylinder"),
                  "bullets": [L("Dòng đều + lưỡng cực cho ψ = V r sin θ (1 − R²/r²)", "Uniform flow + doublet gives ψ = V r sin θ (1 − R²/r²)"),
                              L("Trên mặt (r = R): V_θ = −2V sin θ và C_p = 1 − 4 sin²θ", "On the surface (r = R): V_θ = −2V sin θ and C_p = 1 − 4 sin²θ"),
                              L("Lực cản và lực nâng đều bằng 0 (nghịch lý d'Alembert)", "Drag and lift are both zero (d'Alembert's paradox)")],
                  "slides": [{"title": L("Áp suất quanh hình trụ", "Pressure round the cylinder"),
                              "body": table(["θ", L("V/V∞ trên mặt", "V/V∞ on the surface"), "C_p"],
                                            [[f"{a}°", N(2 * abs(math.sin(math.radians(a))), 3), N(1 - 4 * math.sin(math.radians(a)) ** 2, 3)] for a in (0, 30, 60, 90)]) +
                              ul(L("Tại θ = 0° và 180°: điểm đình trệ, C_p = +1", "At θ = 0° and 180°: stagnation points, C_p = +1"),
                                 L("Tại θ = 90°: vận tốc lớn nhất 2V∞ và C_p = −3 (hút mạnh nhất)", "At θ = 90°: maximum velocity 2V∞ and C_p = −3 (strongest suction)"),
                                 L("Phân bố đối xứng trước–sau nên hợp lực theo dòng bằng 0", "The distribution is symmetric front-to-back so the force along the flow is zero")),
                              "explain": L("Thực tế hình trụ có lực cản lớn vì lớp biên giới tách ra phía sau (module 02): lý thuyết không nhớt không thấy điều đó.", "A real cylinder has large drag because the boundary layer separates behind it (module 02): inviscid theory cannot see that.")}]})
    parts.append({"title": L("Hình trụ có lưu số và định lý Kutta-Joukowski", "The lifting cylinder and the Kutta-Joukowski theorem"),
                  "bullets": [L("Thêm xoáy Γ ở tâm: V_θ(mặt) = −2V sin θ − Γ/(2πR)", "Add a vortex Γ at the centre: V_θ(surface) = −2V sin θ − Γ/(2πR)"),
                              L("Điểm đình trệ dịch xuống: sin θ = −Γ/(4πVR)", "The stagnation points move down: sin θ = −Γ/(4πVR)"),
                              L("Lực nâng trên đơn vị sải L′ = ρ V Γ, đúng cho mọi vật hai chiều", "Lift per unit span L′ = ρ V Γ, valid for any two-dimensional body")],
                  "slides": [{"title": L("Ví dụ: Γ/(4πVR) = 0,5", "Example: Γ/(4πVR) = 0.5"),
                              "body": ul(L(f"sin θ_dt = −0,5 nên các điểm đình trệ ở θ = {N(th_stag, 0)}° và {N(180 - th_stag, 0)}°, cùng nằm dưới trục ngang", f"sin θ_s = −0.5 so the stagnation points are at θ = {N(th_stag, 0)}° and {N(180 - th_stag, 0)}°, both below the horizontal axis"),
                                         L(f"Vận tốc lớn nhất trên mặt xảy ra ở đỉnh (θ = 90°): |V_θ| = 2V + V = {N(Vmax_surf, 1)} V∞ (ở đáy chỉ còn 2V − V = V∞), nên mặt trên có áp suất thấp hơn: đó là lực nâng", f"The maximum surface velocity occurs at the top (θ = 90°): |V_θ| = 2V + V = {N(Vmax_surf, 1)} V∞ (at the bottom only 2V − V = V∞ remains), so the upper surface has lower pressure: that is the lift"),
                                         L("Khi Γ/(4πVR) = 1 hai điểm đình trệ nhập làm một ở đáy; vượt quá thì điểm đình trệ rời khỏi mặt vật", "When Γ/(4πVR) = 1 the two stagnation points merge at the bottom; beyond that the stagnation point leaves the surface")),
                              "explain": L("Dòng nhanh hơn ở một phía nghĩa là áp suất thấp hơn ở phía đó: đó là cơ chế của lực nâng (module 02) và của hiệu ứng Magnus.", "Faster flow on one side means lower pressure on that side: this is the mechanism of lift (module 02) and of the Magnus effect.")}]})
    parts.append({"title": L("Áp dụng: giới hạn nén được và lực cản của dây", "Applications: the compressibility limit and the drag of wires"),
                  "bullets": [L("Vận tốc cục bộ trên hình trụ lên tới 2V∞, nên nén được xuất hiện sớm hơn nhiều so với vận tốc dòng tự do", "Local velocity on a cylinder reaches 2V∞, so compressibility appears long before the free-stream limit"),
                              L("Lực cản vật trụ ở Re lớn tính bằng D = q S C_D với C_D đo từ thí nghiệm", "The drag of a cylinder at high Re is D = q S C_D with C_D from experiment"),
                              L("Lý thuyết thế không cho lực cản: phải dùng số liệu thực nghiệm", "Potential theory gives no drag: experimental data are needed")],
                  "slides": [{"title": L("Bài 3.19 và 3.22", "Problems 3.19 and 3.22"),
                              "body": ul(L(f"3.19: q = ½ρV² = {N(q, 1)} lb/ft² ở 120 mi/h; cột chống 25 ft × 2 in: D = {N(D_str, 0)} lb; dây 80 ft × 3/32 in: D = {N(D_wire, 0)} lb; tổng {N(D_sum, 0)} lb, bằng {N(frac * 100, 0)}% lực cản không nâng {N(D0, 0)} lb (Solution Manual dùng C_D = 1 đọc từ đồ thị)", f"3.19: q = ½ρV² = {N(q, 1)} lb/ft² at 120 mi/h; 25 ft of 2 in struts: D = {N(D_str, 0)} lb; 80 ft of 3/32 in wires: D = {N(D_wire, 0)} lb; total {N(D_sum, 0)} lb, which is {N(frac * 100, 0)}% of the zero-lift drag {N(D0, 0)} lb (the Solution Manual uses C_D = 1 read from a chart)"),
                                         L(f"3.22: 250 mi/h = {N(Vloc, 2)} m/s là vận tốc cục bộ lớn nhất; vì V_max = 2V∞ nên V∞ = {N(Vinf, 2)} m/s ≈ 125 mi/h; khi đó M cục bộ = {N(Mloc, 2)}", f"3.22: 250 mi/h = {N(Vloc, 2)} m/s is the maximum local velocity; since V_max = 2V∞, V∞ = {N(Vinf, 2)} m/s ≈ 125 mi/h; the local Mach number is then {N(Mloc, 2)}")),
                              "explain": L("Đây là lý do máy bay cánh hai tầng với dây giằng chậm: dây chiếm hơn một nửa lực cản không nâng ở 120 mi/h; Anderson ghi nhận các nhà thiết kế thập niên 1930 chuyển sang cánh giằng bên trong.", "This is why biplanes with bracing wires were slow: the struts and wires are over half the zero-lift drag at 120 mi/h; Anderson notes that designers in the 1930s moved to internally braced wings.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Hình trụ và định lý Kutta-Joukowski", "The cylinder and the Kutta-Joukowski theorem")
    m["formula_math"] = ("ψ = V r sin θ (1 − R²/r²)  ·  V_θ|_{r=R} = −2V sin θ − Γ/(2πR)  ·  C_p = 1 − (V/V∞)²  ·  L′ = ρ V Γ" if lang == "vi" else
                         "ψ = V r sin θ (1 − R²/r²)  ·  V_θ|_{r=R} = −2V sin θ − Γ/(2πR)  ·  C_p = 1 − (V/V∞)²  ·  L′ = ρ V Γ")
    m["legend"] = [("ψ, φ", L("hàm dòng, hàm thế", "stream function, potential")), ("Γ", L("lưu số (m²/s)", "circulation (m²/s)")), ("Λ, κ", L("cường độ nguồn, lưỡng cực", "source and doublet strengths")), ("R", L("bán kính hình trụ", "cylinder radius")), ("C_p", L("hệ số áp suất", "pressure coefficient")), ("L′", L("lực nâng trên đơn vị sải", "lift per unit span"))]
    m["history_title"] = L("Bernoulli, Euler, Kutta và Joukowski", "Bernoulli, Euler, Kutta and Joukowski")
    m["history"] = L("Anderson dành các mục Historical Note 3.19 và 4.15 cho Bernoulli và Euler (nguồn gốc của lý thuyết chất lưu) và cho Kutta và Joukowski. Martin Kutta (1902) và Nikolai Joukowski (1906) độc lập đưa ra mối quan hệ L′ = ρVΓ; Joukowski nhận ra lực nâng tỉ lệ với lưu số quanh cánh.",
                     "Anderson devotes Historical Notes 3.19 and 4.15 to Bernoulli and Euler (the origins of fluid theory) and to Kutta and Joukowski. Martin Kutta (1902) and Nikolai Joukowski (1906) independently reached L′ = ρVΓ; Joukowski recognised that lift is proportional to the circulation round the wing.")
    m["case_title"] = L("Tình huống: hình trụ quay", "Case: the spinning cylinder")
    m["case"] = L(f"Một hình trụ quay trong dòng 30 m/s ở mực biển (ρ = 1,23 kg/m³) chịu lực nâng 6 N trên mỗi mét sải. Từ L′ = ρVΓ ta tìm lưu số Γ = 6/(1,23 × 30) = {N(Gam318, 3)} m²/s (Bài 3.18). Đây là hiệu ứng Magnus: quả bóng xoáy cong, và tàu Flettner dùng rôto quay thay cho buồm.",
                  f"A spinning cylinder in a 30 m/s stream at sea level (ρ = 1.23 kg/m³) feels a lift of 6 N per metre of span. From L′ = ρVΓ the circulation is Γ = 6/(1.23 × 30) = {N(Gam318, 3)} m²/s (Problem 3.18). This is the Magnus effect: a spinning ball curves, and Flettner ships use rotors instead of sails.")
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L("(1) Lực nâng của cánh không đến từ việc cánh \"quay\": lưu số là công cụ toán học, được xác định bởi điều kiện Kutta. (2) Hình trụ không nhớt có lực cản bằng 0, nhưng trụ thật thì lớn: đó là sự tách dòng. (3) Dấu của V_θ phụ thuộc quy ước: trong sách xoáy theo chiều kim đồng hồ có Γ > 0. (4) Nếu V∞ gấp đôi mà Γ giữ nguyên, hình dạng các đường dòng đổi; nếu không có lưu số, hình dạng giữ nguyên (Bài 3.16, 3.17). (5) Bài 3.19 phụ thuộc C_D = 1 đọc từ đồ thị; số này là gần đúng.",
                  "(1) A wing's lift does not come from the wing \"spinning\": circulation is a mathematical tool fixed by the Kutta condition. (2) An inviscid cylinder has zero drag but a real one has large drag: that is flow separation. (3) The sign of V_θ depends on convention: in the book a clockwise vortex has Γ > 0. (4) If V∞ doubles with Γ unchanged the streamline shape changes; without circulation the shape stays the same (Problems 3.16, 3.17). (5) Problem 3.19 depends on C_D = 1 read from a chart; that number is approximate.")
    m["nb_desc"] = L("Notebook kiểm hàm dòng và áp suất trên hình trụ, giải lại Anderson 3.15–3.22 và assert các đáp án quiz.", "The notebook checks the stream function and the surface pressure of the cylinder, re-solves Anderson 3.15–3.22 and asserts the quiz answers.")

    SD = lambda i: 900 + i
    SUP = L("Bổ sung (biên soạn)", "Supplementary (authored)")
    Q = lambda i, src, q_, r, w, ex, det=None: mcq(SD(i), src, q_, r, w, ex, det)
    book = [
        Q(1, "Anderson 6th, Problem 3.15", L("Hình trụ không nâng. Hệ số áp suất trên mặt tại θ = 90° là:", "Non-lifting cylinder. The pressure coefficient on the surface at θ = 90° is:"), N(cp90, 0), [N(1.0, 0), N(-1.0, 0), N(-2.0, 0)], L("C_p = 1 − (V/V∞)², V = 2V∞ sin θ.", "C_p = 1 − (V/V∞)², V = 2V∞ sin θ."),
          L("<p>Trên mặt V_θ = −2V∞ sin θ nên V²/V∞² = 4 sin²θ; tại 90° bằng 4, C_p = 1 − 4 = −3.</p>", "<p>On the surface V_θ = −2V∞ sin θ so V²/V∞² = 4 sin²θ; at 90° this is 4 and C_p = 1 − 4 = −3.</p>")),
        Q(2, "Anderson 6th, Problem 3.16", L("Dòng không nâng quanh hình trụ: nếu V∞ tăng gấp đôi, hình dạng đường dòng:", "Non-lifting flow round a cylinder: if V∞ doubles the shape of the streamlines:"), L("không đổi", "does not change"), [L("đổi vì áp suất đổi", "changes because the pressure changes"), L("đổi chỉ gần vật", "changes only near the body"), L("đổi chỉ ở xa vật", "changes only far from the body")], L("V_r và V_θ đều tỉ lệ với V∞ nên hướng vận tốc tại mỗi điểm không đổi.", "V_r and V_θ are both proportional to V∞ so the velocity direction at every point is unchanged.")),
        Q(3, "Anderson 6th, Problem 3.17", L("Dòng quanh hình trụ có lưu số Γ cố định: nếu V∞ tăng gấp đôi, hình dạng đường dòng:", "Flow round a cylinder with fixed circulation Γ: if V∞ doubles the shape of the streamlines:"), L("thay đổi", "changes"), [L("không đổi", "does not change"), L("chỉ đảo chiều", "only reverses"), L("chỉ co lại theo tỉ lệ", "only scales")], L("V_θ có thêm số hạng Γ/(2πr) không tỉ lệ với V∞.", "V_θ has an extra term Γ/(2πr) that does not scale with V∞.")),
        Q(4, "Anderson 6th, Problem 3.18", L("Hình trụ quay, V∞ = 30 m/s, ρ = 1,23 kg/m³, lực nâng 6 N/m. Lưu số là:", "Spinning cylinder, V∞ = 30 m/s, ρ = 1.23 kg/m³, lift 6 N/m. The circulation is:"), f"{N(Gam318, 3)} m²/s", [f"{N(Gam318 * 2, 3)} m²/s", f"{N(Gam318 / 2, 3)} m²/s", f"{N(6 / 30, 3)} m²/s"], L("Γ = L′/(ρV∞).", "Γ = L′/(ρV∞)."), L(f"<p>Γ = 6/(1,23 × 30) = {N(Gam318, 4)} m²/s. Solution Manual: 0,163.</p>", f"<p>Γ = 6/(1.23 × 30) = {N(Gam318, 4)} m²/s. Solution Manual: 0.163.</p>")),
        Q(5, "Anderson 6th, Problem 3.19", L("Cột chống 25 ft đường kính 2 in, bay 120 mi/h mực biển (ρ = 0,002377 slug/ft³), lấy C_D = 1 theo diện tích chắn. Lực cản của các cột là:", "25 ft of 2 in diameter struts at 120 mi/h sea level (ρ = 0.002377 slug/ft³) with C_D = 1 on the frontal area. The strut drag is:"), f"{N(D_str, 0)} lb", [f"{N(D_str / 2, 0)} lb", f"{N(D_str * 2, 0)} lb", f"{N(D_wire, 0)} lb"], L("D = q S C_D với S = chiều dài × đường kính.", "D = q S C_D with S = length × diameter."), L(f"<p>q = {N(q, 2)} lb/ft²; S = 25 × (2/12) = 4,167 ft²; D = {N(D_str, 1)} lb (Solution Manual 153 lb).</p>", f"<p>q = {N(q, 2)} lb/ft²; S = 25 × (2/12) = 4.167 ft²; D = {N(D_str, 1)} lb (Solution Manual 153 lb).</p>")),
        Q(6, "Anderson 6th, Problem 3.21", L("Dòng quanh hình trụ, ψ₁ = 0 trên mặt, ψ₂ đi qua (1,2R, π/2), các đường dòng cách đều ở thượng nguồn. Đường dòng ψ₃ đi qua điểm trên đỉnh có r/R bằng:", "Flow round a cylinder, ψ₁ = 0 on the surface, ψ₂ through (1.2R, π/2), streamlines equally spaced upstream. The streamline ψ₃ passes over the top at r/R equal to:"), N(r3, 3), [N(1.4, 3), N(1.2 * 1.2, 3), N(1.6, 3)], L("ψ₃ = 2ψ₂ và ψ(r) = V R (r/R − R/r) tại θ = 90°.", "ψ₃ = 2ψ₂ and ψ(r) = V R (r/R − R/r) at θ = 90°."), L(f"<p>ψ₂/(VR) = 1,2 − 1/1,2 = {N(psi2, 4)}; cần x − 1/x = {N(2 * psi2, 4)} ⇒ x = {N(r3, 4)}. Khoảng cách: 1,0→1,2 là 0,2R, 1,2→{N(r3, 2)} là {N(r3 - 1.2, 3)}R.</p>", f"<p>ψ₂/(VR) = 1.2 − 1/1.2 = {N(psi2, 4)}; we need x − 1/x = {N(2 * psi2, 4)} ⇒ x = {N(r3, 4)}. Gaps: 1.0→1.2 is 0.2R, 1.2→{N(r3, 2)} is {N(r3 - 1.2, 3)}R.</p>")),
        Q(7, "Anderson 6th, Problem 3.22", L("Hình trụ trong hầm gió ở mực biển; nén được bắt đầu quan trọng khi vận tốc cục bộ vượt 250 mi/h. Vận tốc dòng tự do tương ứng (V_max = 2V∞) là:", "A cylinder in a sea-level wind tunnel; compressibility starts to matter when the local velocity exceeds 250 mi/h. The corresponding free-stream velocity (V_max = 2V∞) is:"), f"{N(Vinf, 1)} m/s (125 mi/h)", [f"{N(Vloc, 1)} m/s (250 mi/h)", f"{N(Vloc / 4, 1)} m/s", f"{N(Vloc * 2, 1)} m/s"], L("Điểm vai (θ = 90°) có V = 2V∞.", "The shoulder (θ = 90°) has V = 2V∞."), L(f"<p>V∞ = 250 mi/h / 2 = 125 mi/h = {N(Vinf, 2)} m/s. Khi đó M cục bộ = {N(Mloc, 2)}.</p>", f"<p>V∞ = 250 mi/h / 2 = 125 mi/h = {N(Vinf, 2)} m/s. The local Mach number is then {N(Mloc, 2)}.</p>")),
    ]
    gen = [
        Q(11, SUP, L("Vận tốc lớn nhất trên mặt hình trụ không nâng bằng bao nhiêu lần V∞?", "How many times V∞ is the maximum surface velocity of a non-lifting cylinder?"), "2", ["1", "π", "4"], L("V = 2V∞ sin θ lớn nhất tại θ = 90°.", "V = 2V∞ sin θ is largest at θ = 90°.")),
        Q(12, SUP, L("Điểm đình trệ của hình trụ không nâng nằm ở:", "The stagnation points of a non-lifting cylinder are at:"), "θ = 0° và 180°" if lang == "vi" else "θ = 0° and 180°", ["θ = 90° và 270°", "θ = 45° và 135°", "θ = 60° và 120°"], L("V_θ = −2V sin θ = 0 ⇒ sin θ = 0.", "V_θ = −2V sin θ = 0 ⇒ sin θ = 0.")),
        Q(13, SUP, L("Với Γ/(4πVR) = 0,5, điểm đình trệ ở θ bằng:", "With Γ/(4πVR) = 0.5 the stagnation point is at θ equal to:"), f"{N(th_stag, 0)}°", ["30°", "−60°", "0°"], L("sin θ = −Γ/(4πVR) = −0,5.", "sin θ = −Γ/(4πVR) = −0.5.")),
        Q(14, SUP, L("Nghịch lý d'Alembert nói rằng dòng không nhớt, không nén được quanh vật hai chiều có lực cản:", "d'Alembert's paradox says inviscid incompressible flow round a two-dimensional body has a drag of:"), L("bằng 0", "zero"), [L("rất lớn", "very large"), L("tỉ lệ với V", "proportional to V"), L("tỉ lệ với V²", "proportional to V²")], L("Phân bố áp suất đối xứng trước–sau.", "The pressure distribution is symmetric front-to-back.")),
        Q(15, SUP, L("Tăng gấp đôi vận tốc ở cùng Γ và ρ thì lực nâng L′ = ρVΓ:", "Doubling the velocity at the same Γ and ρ makes the lift L′ = ρVΓ:"), L("tăng gấp đôi", "double"), [L("tăng gấp bốn", "quadruple"), L("không đổi", "stay the same"), L("giảm một nửa", "halve")], L("L′ tỉ lệ thuận với V (khác với L ∝ V² ở cánh có C_L không đổi).", "L′ is proportional to V (unlike L ∝ V² for a wing at fixed C_L).")),
        Q(16, SUP, L("Lưỡng cực được tạo từ:", "A doublet is made from:"), L("một nguồn và một hố cùng cường độ đặt sát nhau", "a source and a sink of equal strength brought together"), [L("hai xoáy cùng chiều", "two vortices of the same sense"), L("một nguồn và một xoáy", "a source and a vortex"), L("dòng đều và xoáy", "uniform flow and a vortex")], L("Anderson 3.12.", "Anderson 3.12.")),
    ]
    m["quiz_sets"] = [
        {"key": "anderson", "title": L("Sách 2: Anderson, bài tập cuối chương 3 (đáp án tính lại bằng Python)", "Book 2: Anderson, end-of-chapter 3 problems (answers recomputed in Python)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập bổ sung (biên soạn thêm, đáp án tự kiểm chứng bằng tính toán)", "Additional practice (authored, answers self-verified by computation)"), "items": gen},
    ]
    m["problems_intro"] = L("Lời giải theo bốn bước. Đã đối chiếu Solution Manual (bản 4th): 3.15, 3.16, 3.17, 3.18, 3.19, 3.20 khớp. Bài 3.21 và 3.22 chưa có trong Solution Manual bản 4th nên kiểm bằng hai cách (đại số và nghiệm số).", "Solved in four steps. Compared with the 4th-edition Solution Manual: 3.15, 3.16, 3.17, 3.18, 3.19, 3.20 agree. Problems 3.21 and 3.22 are not in the 4th-edition Solution Manual so they are checked two ways (algebra and a numerical root).")
    m["problems"] = [
        {"num": "3.15", "src": "Anderson 6th, Problem 3.15", "q": L("Dòng không nâng quanh hình trụ: dẫn xuất C_p tại điểm (r, θ) bất kỳ và chứng minh trên mặt nó thành C_p = 1 − 4 sin²θ.", "Non-lifting flow round a cylinder: derive C_p at any point (r, θ) and show that on the surface it reduces to C_p = 1 − 4 sin²θ."),
         "ans": sol(lang, L("Cần C_p ở mọi điểm, không chỉ trên mặt.", "We need C_p everywhere, not only on the surface."), L("C_p = 1 − (V/V∞)², nên chỉ cần V² = V_r² + V_θ² từ hàm dòng.", "C_p = 1 − (V/V∞)², so we only need V² = V_r² + V_θ² from the stream function."),
                    [L("Từ ψ = V∞ r sin θ (1 − R²/r²): V_r = (1/r)∂ψ/∂θ = V∞ cos θ (1 − R²/r²).", "From ψ = V∞ r sin θ (1 − R²/r²): V_r = (1/r)∂ψ/∂θ = V∞ cos θ (1 − R²/r²)."),
                     L("V_θ = −∂ψ/∂r = −V∞ sin θ (1 + R²/r²).", "V_θ = −∂ψ/∂r = −V∞ sin θ (1 + R²/r²)."),
                     L("V²/V∞² = (1 − R²/r²)² cos²θ + (1 + R²/r²)² sin²θ.", "V²/V∞² = (1 − R²/r²)² cos²θ + (1 + R²/r²)² sin²θ."),
                     L("<b>C_p = 1 − (1 − R²/r²)² cos²θ − (1 + R²/r²)² sin²θ.</b>", "<b>C_p = 1 − (1 − R²/r²)² cos²θ − (1 + R²/r²)² sin²θ.</b>"),
                     L("Trên mặt r = R: số hạng đầu bằng 0 và (1 + 1)² = 4, nên <b>C_p = 1 − 4 sin²θ</b>.", "On the surface r = R: the first term vanishes and (1 + 1)² = 4, so <b>C_p = 1 − 4 sin²θ</b>.")],
                    L("Solution Manual cho cùng kết quả. Kiểm số: θ = 90° ⇒ C_p = −3; θ = 0° ⇒ +1.", "The Solution Manual gives the same result. Numerical check: θ = 90° ⇒ C_p = −3; θ = 0° ⇒ +1."))},
        {"num": "3.16 – 3.17", "src": "Anderson 6th, Problems 3.16, 3.17", "q": L("Nếu V∞ tăng gấp đôi, hình dạng đường dòng quanh hình trụ có đổi không: (a) không lưu số; (b) lưu số Γ cố định?", "If V∞ doubles, does the shape of the streamlines round a cylinder change: (a) without circulation; (b) with fixed circulation Γ?"),
         "ans": sol(lang, L("Hình dạng đường dòng được quyết định bởi hướng của vận tốc tại mỗi điểm.", "The shape of the streamlines is fixed by the direction of the velocity at each point."), L("Xét tỉ số V_θ/V_r: nếu nó không đổi khi V∞ đổi thì hình dạng không đổi.", "Look at the ratio V_θ/V_r: if it does not change with V∞ the shape does not change."),
                    [L("(a) V_r = V∞ f(r, θ) và V_θ = V∞ g(r, θ), nên V_θ/V_r = g/f không phụ thuộc V∞. <b>Hình dạng không đổi.</b>", "(a) V_r = V∞ f(r, θ) and V_θ = V∞ g(r, θ), so V_θ/V_r = g/f is independent of V∞. <b>The shape does not change.</b>"),
                     L("(b) V_θ = −(1 + R²/r²) V∞ sin θ − Γ/(2πr): số hạng thứ hai không có V∞.", "(b) V_θ = −(1 + R²/r²) V∞ sin θ − Γ/(2πr): the second term has no V∞."),
                     L("Do đó V_θ/V_r phụ thuộc V∞. <b>Hình dạng thay đổi.</b>", "Hence V_θ/V_r depends on V∞. <b>The shape changes.</b>")],
                    L("Ví dụ: điểm đình trệ sin θ = −Γ/(4πV∞R) dịch khi V∞ đổi, xác nhận (b).", "Example: the stagnation point sin θ = −Γ/(4πV∞R) moves when V∞ changes, confirming (b)."))},
        {"num": "3.19", "src": "Anderson 6th, Problem 3.19", "q": L("Máy bay hai tầng bay 120 mi/h mực biển: cột chống tổng 25 ft đường kính 2 in, dây giằng tổng 80 ft đường kính 3/32 in. Tính lực cản của chúng và so với lực cản không nâng (S = 230 ft², C_D,0 = 0,036).", "A biplane at 120 mi/h sea level: struts totalling 25 ft of 2 in diameter and bracing wires totalling 80 ft of 3/32 in diameter. Find their drag and compare it with the zero-lift drag (S = 230 ft², C_D,0 = 0.036)."),
         "ans": sol(lang, L("Vật trụ nên lực cản phụ thuộc diện tích chắn dòng = chiều dài × đường kính.", "They are cylinders so drag depends on the frontal area = length × diameter."), L("Dùng D = q S C_D; Solution Manual lấy C_D = 1 từ đồ thị (Re khoảng 2×10⁵ cho cột, 9×10³ cho dây).", "Use D = q S C_D; the Solution Manual takes C_D = 1 from a chart (Re about 2×10⁵ for the struts, 9×10³ for the wires)."),
                    [L(f"V = 120 mi/h = 176 ft/s; q = ½ × 0,002377 × 176² = {N(q, 1)} lb/ft².", f"V = 120 mi/h = 176 ft/s; q = ½ × 0.002377 × 176² = {N(q, 1)} lb/ft²."),
                     L(f"Cột: S = 25 × (2/12) = 4,167 ft² ⇒ D = {N(q, 1)} × 4,167 × 1 = <b>{N(D_str, 0)} lb</b>.", f"Struts: S = 25 × (2/12) = 4.167 ft² ⇒ D = {N(q, 1)} × 4.167 × 1 = <b>{N(D_str, 0)} lb</b>."),
                     L(f"Dây: S = 80 × (3/32/12) = 0,625 ft² ⇒ D = <b>{N(D_wire, 0)} lb</b>.", f"Wires: S = 80 × (3/32/12) = 0.625 ft² ⇒ D = <b>{N(D_wire, 0)} lb</b>."),
                     L(f"Tổng <b>{N(D_sum, 0)} lb</b>. Lực cản không nâng toàn máy bay D₀ = q S C_D,0 = {N(q, 1)} × 230 × 0,036 = {N(D0, 0)} lb.", f"Total <b>{N(D_sum, 0)} lb</b>. Zero-lift drag of the whole aircraft D₀ = q S C_D,0 = {N(q, 1)} × 230 × 0.036 = {N(D0, 0)} lb."),
                     L(f"Tỉ lệ = {N(D_sum, 0)}/{N(D0, 0)} = <b>{N(frac * 100, 0)}%</b>.", f"Ratio = {N(D_sum, 0)}/{N(D0, 0)} = <b>{N(frac * 100, 0)}%</b>.")],
                    L("Solution Manual: 153 + 23 = 176 lb và 58%. Chênh lệch nhỏ do SM làm tròn đường kính 2 in = 0,167 ft.", "Solution Manual: 153 + 23 = 176 lb and 58%. The tiny difference is because it rounds 2 in to 0.167 ft."))},
        {"num": "3.21 – 3.22", "src": "Anderson 6th, Problems 3.21, 3.22", "q": L("(3.21) ψ₁ = 0 trên mặt, ψ₂ qua (1,2R, π/2); tìm điểm trên đỉnh mà ψ₃ đi qua. (3.22) Vận tốc hầm gió để nén được bắt đầu quan trọng khi vận tốc cục bộ vượt 250 mi/h.", "(3.21) ψ₁ = 0 on the surface and ψ₂ passes through (1.2R, π/2); find the point over the top through which ψ₃ passes. (3.22) The wind-tunnel speed at which compressibility starts to matter when the local velocity exceeds 250 mi/h."),
         "ans": sol(lang, L("(3.21) Các đường dòng cách đều ở thượng nguồn nên ψ₃ = 2ψ₂. (3.22) Nén được quan trọng ở nơi vận tốc lớn nhất.", "(3.21) The streamlines are equally spaced upstream so ψ₃ = 2ψ₂. (3.22) Compressibility matters where the velocity is highest."), L("Dùng ψ = V r sin θ (1 − R²/r²) tại θ = 90°; và V_max = 2V∞ trên hình trụ.", "Use ψ = V r sin θ (1 − R²/r²) at θ = 90°; and V_max = 2V∞ on the cylinder."),
                    [L(f"(3.21) Tại θ = 90°, ψ/(VR) = x − 1/x với x = r/R. ψ₂/(VR) = 1,2 − 1/1,2 = {N(psi2, 4)}.", f"(3.21) At θ = 90°, ψ/(VR) = x − 1/x with x = r/R. ψ₂/(VR) = 1.2 − 1/1.2 = {N(psi2, 4)}."),
                     L(f"ψ₃ = 2ψ₂ ⇒ x − 1/x = {N(2 * psi2, 4)} ⇒ x² − {N(2 * psi2, 4)}x − 1 = 0 ⇒ <b>x = {N(r3, 3)}</b>.", f"ψ₃ = 2ψ₂ ⇒ x − 1/x = {N(2 * psi2, 4)} ⇒ x² − {N(2 * psi2, 4)}x − 1 = 0 ⇒ <b>x = {N(r3, 3)}</b>."),
                     L(f"Khoảng cách giữa các đường dòng trên đỉnh: 0,2R rồi {N(r3 - 1.2, 3)}R: chúng bị ép lại gần vật vì dòng nhanh lên (liên tục).", f"Gaps between the streamlines over the top: 0.2R then {N(r3 - 1.2, 3)}R: they are squeezed close to the body because the flow speeds up (continuity)."),
                     L(f"(3.22) V_max = 2V∞ ⇒ V∞ = 250/2 = <b>125 mi/h = {N(Vinf, 1)} m/s</b>.", f"(3.22) V_max = 2V∞ ⇒ V∞ = 250/2 = <b>125 mi/h = {N(Vinf, 1)} m/s</b>.")],
                    L(f"Kiểm (3.21): thay x = {N(r3, 3)}: x − 1/x = {N(r3 - 1 / r3, 4)} = 2ψ₂ ✓. Kiểm (3.22): M cục bộ = {N(Mloc, 2)}.", f"Check (3.21): substituting x = {N(r3, 3)}: x − 1/x = {N(r3 - 1 / r3, 4)} = 2ψ₂ ✓. Check (3.22): local Mach number = {N(Mloc, 2)}."))},
    ]
    return m
