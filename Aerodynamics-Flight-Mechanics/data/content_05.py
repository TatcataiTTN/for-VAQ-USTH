# -*- coding: utf-8 -*-
"""Module 05: Canh huu han va luc can cam ung. Nguon: EASA M08 SM2 (tr.2.7 xoay dau canh, 2.14 luc can cam ung, Hinh 2-20 winglet),
Anderson 6th ch.5 (5.1-5.3, Vi du 5.1, 5.2, Bai 5.1, 5.2), Etkin & Reid Phu luc B/C."""
import math
from aero import *
from common import num, ul, table, mcq


def biot_savart_loop_axis(R, A, gamma=1.0, n=20000):
    """Van toc cam ung tai khoang cach A tren truc vong xoay ban kinh R: tich phan so truc tiep cua dinh luat Biot-Savart (doc lap voi cong thuc)."""
    s = 0.0
    dth = 2 * math.pi / n
    for k in range(n):
        th = (k + 0.5) * dth
        # dl = R dth (-sin, cos, 0); r = (0,0,A) - (R cos, R sin, 0) ; dl x r z-comp
        rx, ry, rz = -R * math.cos(th), -R * math.sin(th), A
        dlx, dly = -R * math.sin(th) * dth, R * math.cos(th) * dth
        cz = dlx * ry - dly * rx
        r3 = (rx * rx + ry * ry + rz * rz) ** 1.5
        s += cz / r3
    return gamma * s / (4 * math.pi)


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    a0 = 2 * math.pi
    AR1, tau1 = 8.0, 0.055
    a51 = a0 / (1 + a0 / (math.pi * AR1) * (1 + tau1)); a51d = a51 * math.pi / 180
    CL51 = a51d * 5; CD51 = CL51 ** 2 * (1 + tau1) / (math.pi * AR1)
    # vi du 5.2
    CL6 = math.sqrt(math.pi * 6 * 0.01 / 1.055); a6 = CL6 / math.radians(3.4 + 2)
    a0b = a6 / (1 - a6 * 1.055 / (math.pi * 6))
    a10 = a0b / (1 + a0b * 1.105 / (math.pi * 10)); CL10 = a10 * math.radians(5.4); CD10 = CL10 ** 2 * 1.105 / (math.pi * 10)
    # bai 5.1, 5.2 (so)
    R, Gam = 2.0, 1.0
    w51 = biot_savart_loop_axis(R, 0.0, Gam); w51f = Gam / (2 * R)
    A52 = 1.5; w52 = biot_savart_loop_axis(R, A52, Gam); w52f = Gam * R ** 2 / (2 * (R ** 2 + A52 ** 2) ** 1.5)
    # cánh elip
    CLe, ARe = 0.5, 8.0
    ai = CLe / (math.pi * ARe); CDie = CLe ** 2 / (math.pi * ARe)
    CDi_AR12 = CLe ** 2 / (math.pi * 12)

    m = {"num": "05", "slug": "05-finite-wing", "tag": L("Cánh hữu hạn", "Finite wing")}
    m["title"] = L("Cánh hữu hạn: xoáy đầu cánh, downwash và lực cản cảm ứng", "Finite wings: tip vortices, downwash and induced drag")
    m["src"] = L("Anderson ch.5 (mục 5.1–5.3, Ví dụ 5.1, 5.2, Bài 5.1, 5.2) · EASA Module 08, Sub-module 02 (tr. 2.7, 2.14) · Etkin &amp; Reid Phụ lục B, C",
                 "Anderson ch. 5 (sec. 5.1–5.3, Examples 5.1, 5.2, Problems 5.1, 5.2) · EASA Module 08, Sub-module 02 (pp. 2.7, 2.14) · Etkin &amp; Reid Appendices B, C")
    m["intro"] = L("Module 02 mới chỉ nói rằng lực cản cảm ứng đi kèm với lực nâng. Module này giải thích vì sao: chênh lệch áp suất giữa hai mặt cánh làm không khí cuộn quanh đầu cánh thành xoáy; xoáy kéo dòng khí đi xuống (downwash) và làm vectơ lực nâng nghiêng ra sau. Đi từ mô hình xoáy, định luật Biot-Savart và lý thuyết đường nâng của Prandtl với phân bố lực nâng elip, ta được C_D,i = C_L²/(π·AR). Sau đó công thức được mở rộng cho cánh bất kỳ bằng các hệ số δ và τ, và ta giải lại Ví dụ 5.1, 5.2 của Anderson.",
                   "Module 02 only said that induced drag comes with lift. This module explains why: the pressure difference between the two wing surfaces makes the air curl round the tip into a vortex; the vortices pull the flow downwards (downwash) and tilt the lift vector backwards. Starting from the vortex model, the Biot-Savart law and Prandtl's lifting-line theory with an elliptical lift distribution, we obtain C_D,i = C_L²/(π·AR). The formula is then extended to any wing with the factors δ and τ, and we re-solve Anderson's Examples 5.1 and 5.2.")
    m["mapping"] = {
        "easa": L("Sub-module 02 (tr. 2.7 Planform và Vortices, tr. 2.14 Induced drag, Hình 2-6 xoáy đầu cánh, Hình 2-20 winglet)", "Sub-module 02 (p. 2.7 Planform and Vortices, p. 2.14 Induced drag, Figure 2-6 wingtip vortices, Figure 2-20 winglets)"),
        "anderson": L("Ch.5 Incompressible Flow over Finite Wings: 5.1 Downwash và lực cản cảm ứng, 5.2 Xoáy, Biot-Savart, định lý Helmholtz, 5.3 Lý thuyết đường nâng Prandtl (5.3.1 phân bố elip); Ví dụ 5.1, 5.2; Bài 5.1, 5.2, 5.4, 5.5",
                      "Ch.5 Incompressible Flow over Finite Wings: 5.1 Downwash and induced drag, 5.2 Vortex filament, Biot-Savart, Helmholtz theorems, 5.3 Prandtl's lifting-line theory (5.3.1 elliptical distribution); Examples 5.1, 5.2; Problems 5.1, 5.2, 5.4, 5.5"),
        "etkin": L("Phụ lục B (dữ liệu ước lượng đạo hàm khí động, độ dốc lực nâng cánh) và Phụ lục C (MAC, tâm khí động cánh); Bài tập 2.6(b) dùng Phụ lục B để ước lượng a_w", "Appendix B (data for estimating aerodynamic derivatives, wing lift slope) and Appendix C (MAC, wing aerodynamic centre); Exercise 2.6(b) uses Appendix B to estimate a_w"),
        "note": L("EASA chỉ mô tả định tính. Anderson cho phần toán. Etkin dùng các kết quả này (độ dốc lực nâng của cánh hữu hạn) để ước lượng đạo hàm ổn định ở các module sau.", "EASA is descriptive only. Anderson provides the mathematics. Etkin uses these results (the finite-wing lift slope) to estimate stability derivatives in later modules."),
    }
    parts = []
    parts.append({"title": L("Xoáy đầu cánh và downwash", "Tip vortices and downwash"),
                  "bullets": [L("Không khí áp suất cao dưới cánh trào vòng qua đầu cánh lên mặt trên và tạo thành xoáy", "High pressure under the wing leaks round the tip to the upper surface and forms a vortex"),
                              L("Xoáy sinh vận tốc hướng xuống (downwash) tại cánh", "The vortices induce a downward velocity (downwash) at the wing"),
                              L("Góc tấn hiệu dụng giảm và lực nâng nghiêng ra sau: đó là lực cản cảm ứng", "The effective angle of attack falls and the lift tilts backwards: this is induced drag")],
                  "slides": [
                      {"title": L("Vì sao cánh hữu hạn khác cánh vô hạn", "Why a finite wing differs from an infinite one"),
                       "body": ul(L("Cánh vô hạn (2D) chỉ có c_l, c_d; cánh hữu hạn có thêm dòng theo sải và hai xoáy đầu cánh", "An infinite (2D) wing has only c_l and c_d; a finite wing also has spanwise flow and two tip vortices"),
                                  L("Ở mép sau, dòng trên và dưới cánh có hướng khác nhau: một lớp xoáy (vortex sheet) kéo dài về phía sau và cuộn lại ở hai đầu", "At the trailing edge the upper and lower flows have different directions: a vortex sheet trails behind and rolls up at the tips"),
                                  L("Vận tốc hướng xuống w tại cánh làm góc tấn hiệu dụng α_eff = α − α_i, với α_i = w/V", "The downward velocity w at the wing reduces the effective angle of attack, α_eff = α − α_i with α_i = w/V")),
                       "explain": L("Giống như chèo thuyền: mái chèo đẩy nước ra sau và để lại các xoáy nước; cánh đẩy không khí xuống và để lại xoáy khí. Năng lượng nằm trong các xoáy ấy chính là công mà lực cản cảm ứng phải tiêu tốn.", "Like a rowing boat: the oar pushes water back and leaves eddies; the wing pushes air down and leaves vortices. The energy left in the vortices is the work paid for by induced drag.")}]})
    parts.append({"title": L("Xoáy và định luật Biot-Savart", "Vortex filament and the Biot-Savart law"),
                  "bullets": [L("Sợi xoáy cường độ Γ không thể kết thúc trong chất lưu (định lý Helmholtz)", "A vortex filament of strength Γ cannot end in the fluid (Helmholtz theorem)"),
                              L("Biot-Savart: dV = Γ/(4π)·dl×r/|r|³", "Biot-Savart: dV = Γ/(4π)·dl×r/|r|³"),
                              L("Vòng xoáy tròn bán kính R: tại tâm V = Γ/(2R)", "A circular vortex loop of radius R: at the centre V = Γ/(2R)")],
                  "slides": [
                      {"title": L("Vòng xoáy tròn (Anderson 5.1, 5.2)", "A circular vortex loop (Anderson 5.1, 5.2)"),
                       "body": ul(L("Tại tâm vòng: V = Γ/(2R)", "At the centre of the loop: V = Γ/(2R)"),
                                  L("Tại điểm cách mặt phẳng vòng một khoảng A trên trục: V = Γ R²/[2(R² + A²)^{3/2}]", "At a point on the axis a distance A from the plane of the loop: V = Γ R²/[2(R² + A²)^{3/2}]"),
                                  L(f"Kiểm lại bằng tích phân số của Biot-Savart (R = 2, Γ = 1): tâm {N(w51, 5)} so với công thức {N(w51f, 5)}; A = 1,5 cho {N(w52, 5)} so với {N(w52f, 5)}", f"Checked by numerical integration of Biot-Savart (R = 2, Γ = 1): centre {N(w51, 5)} against the formula {N(w51f, 5)}; A = 1.5 gives {N(w52, 5)} against {N(w52f, 5)}")),
                       "explain": L("Đây là viên gạch đầu tiên của mô hình đường nâng: cánh được thay bằng một dãy xoáy hình móng ngựa (horseshoe vortex).", "This is the building block of the lifting-line model: a wing is replaced by a row of horseshoe vortices.")}]})
    parts.append({"title": L("Lý thuyết đường nâng và phân bố elip", "Lifting-line theory and the elliptical distribution"),
                  "bullets": [L("Prandtl thay cánh bằng một đường xoáy kèm lớp xoáy kéo dài phía sau", "Prandtl replaced the wing by a lifting line with a trailing vortex sheet"),
                              L("Phân bố lực nâng elip cho downwash đều dọc sải", "An elliptical lift distribution gives a uniform downwash along the span"),
                              L("α_i = C_L/(π·AR) và C_D,i = C_L²/(π·AR): giá trị nhỏ nhất có thể với cùng C_L và AR", "α_i = C_L/(π·AR) and C_D,i = C_L²/(π·AR): the smallest possible values for a given C_L and AR")],
                  "slides": [
                      {"title": L("Kết quả cho cánh elip", "Results for the elliptical wing"),
                       "body": ul(L("Γ(y) = Γ₀ √[1 − (2y/b)²]; downwash w = −Γ₀/(2b) không đổi dọc sải", "Γ(y) = Γ₀ √[1 − (2y/b)²]; downwash w = −Γ₀/(2b) is constant along the span"),
                                  L(f"Ví dụ C_L = 0,5 và AR = 8: α_i = {N(math.degrees(ai), 3)}° và C_D,i = {N(CDie, 5)}", f"Example C_L = 0.5 and AR = 8: α_i = {N(math.degrees(ai), 3)}° and C_D,i = {N(CDie, 5)}"),
                                  L(f"Tăng AR lên 12 ở cùng C_L cho C_D,i = {N(CDi_AR12, 5)}, giảm {N((1 - CDi_AR12 / CDie) * 100, 0)}%", f"Raising AR to 12 at the same C_L gives C_D,i = {N(CDi_AR12, 5)}, a {N((1 - CDi_AR12 / CDie) * 100, 0)}% reduction"),
                                  L("Cánh máy bay Spitfire nổi tiếng với dạng gần elip", "The Spitfire is famous for its near-elliptical wing")),
                       "explain": L("C_D,i tỉ lệ với C_L², nên bay chậm (C_L lớn) thì lực cản cảm ứng lớn. Điều này khớp với Hình 2-21 của EASA (các loại lực cản theo tốc độ).", "C_D,i scales with C_L² so slow flight (large C_L) has large induced drag, matching EASA Figure 2-21 (types of drag against speed).")}]})
    parts.append({"title": L("Cánh bất kỳ: các hệ số δ, τ và e", "Any wing: the factors δ, τ and e"),
                  "bullets": [L("C_D,i = C_L²(1 + δ)/(π·AR) = C_L²/(π·e·AR) với e = 1/(1 + δ)", "C_D,i = C_L²(1 + δ)/(π·AR) = C_L²/(π·e·AR) with e = 1/(1 + δ)"),
                              L("Độ dốc lực nâng cánh hữu hạn a = a₀/[1 + (a₀/π·AR)(1 + τ)]", "The finite-wing lift slope a = a₀/[1 + (a₀/π·AR)(1 + τ)]"),
                              L("Cánh hữu hạn có độ dốc lực nâng nhỏ hơn biên dạng 2D", "A finite wing has a smaller lift slope than its 2D airfoil")],
                  "slides": [
                      {"title": L("Ví dụ 5.1 của Anderson: AR = 8, δ = τ = 0,055, α = 5°", "Anderson Example 5.1: AR = 8, δ = τ = 0.055, α = 5°"),
                       "body": table(["", L("Tính lại", "Recomputed"), L("Sách", "Book")],
                                     [["a (rad⁻¹)", N(a51, 3), "4,97" if lang == "vi" else "4.97"], ["a (độ⁻¹)" if lang == "vi" else "a (deg⁻¹)", N(a51d, 4), "0,0867" if lang == "vi" else "0.0867"], ["C_L", N(CL51, 4), "0,4335" if lang == "vi" else "0.4335"], ["C_D,i", N(CD51, 5), "0,00789" if lang == "vi" else "0.00789"]]) +
                       f"<p class='pill'>{L('Khác biệt nhỏ ở chữ số cuối do sách làm tròn a = 0,0867 trước khi nhân với α', 'The tiny differences in the last digit come from the book rounding a = 0.0867 before multiplying by α')}</p>",
                       "explain": L("Biên dạng mỏng đối xứng có α_L=0 = 0 nên C_L = a·α. Kiểm tra nhanh: C_D,i rất nhỏ so với C_D toàn máy bay, hợp lý.", "A thin symmetric airfoil has α_L=0 = 0, so C_L = a·α. Quick check: C_D,i is small compared with the total drag of a complete aircraft, as it should be.")},
                      {"title": L("Ví dụ 5.2: đổi tỉ số kích thước từ 6 lên 10", "Example 5.2: changing the aspect ratio from 6 to 10"),
                       "body": ul(L(f"AR = 6, C_D,i = 0,01, δ = 0,055 cho C_L = {N(CL6, 3)}, a = {N(a6, 3)}/rad, suy ra a₀ = {N(a0b, 3)}/rad (sách: 5,989)", f"AR = 6, C_D,i = 0.01, δ = 0.055 gives C_L = {N(CL6, 3)}, a = {N(a6, 3)}/rad, hence a₀ = {N(a0b, 3)}/rad (book: 5.989)"),
                                  L(f"AR = 10, δ = τ = 0,105: a = {N(a10, 3)}/rad, C_L = {N(CL10, 3)} (sách 0,464), C_D,i = {N(CD10, 4)} (sách 0,0076)", f"AR = 10, δ = τ = 0.105: a = {N(a10, 3)}/rad, C_L = {N(CL10, 3)} (book 0.464), C_D,i = {N(CD10, 4)} (book 0.0076)"),
                                  L("Cùng góc tấn nhưng C_L khác nhau, nên không thể suy C_D,i chỉ bằng tỉ lệ AR", "Same angle of attack but different C_L, so C_D,i cannot be scaled by AR alone")),
                       "explain": L("Sách tự ghi chú: bài sẽ đơn giản hơn nếu đề cho cùng C_L, khi đó C_D,i tỉ lệ nghịch với AR.", "The book itself notes the problem would be simpler if the same C_L were given, since then C_D,i is inversely proportional to AR.")}]})
    parts.append({"title": L("Hệ quả thiết kế: AR cao và winglet", "Design consequences: high AR and winglets"),
                  "bullets": [L("Tàu lượn có AR rất cao để giảm lực cản cảm ứng", "Gliders have very high AR to reduce induced drag"),
                              L("Winglet làm yếu xoáy đầu cánh (EASA Hình 2-20)", "Winglets weaken the tip vortices (EASA Figure 2-20)"),
                              L("Xoáy đuôi (wake vortex) của máy bay lớn là lý do phải giữ khoảng cách giữa các máy bay khi cất và hạ cánh", "The wake vortices of large aircraft are the reason for take-off and landing separations")],
                  "slides": [
                      {"title": L("Lực cản cảm ứng so với lực cản ký sinh", "Induced drag versus parasite drag"),
                       "body": ul(L("Lực cản cảm ứng giảm khi tốc độ tăng (vì C_L giảm), còn lực cản ký sinh tăng theo V². Tổng lực cản nhỏ nhất ở tốc độ mà hai phần bằng nhau (C_D,0 = C_D,i)", "Induced drag falls with speed (lower C_L) while parasite drag grows as V²; the total is a minimum at the speed where the two are equal (when C_D,0 = C_D,i)"),
                                  L(f"Ví dụ minh họa: C_D,0 = 0,02, AR = 8, e = 0,85: C_L tối ưu cho L/D lớn nhất là √(π·e·AR·C_D,0) = {N(math.sqrt(math.pi * 0.85 * 8 * 0.02), 3)}, (L/D)max = {N(math.sqrt(math.pi * 0.85 * 8 / (4 * 0.02)), 1)}", f"Illustrative example: C_D,0 = 0.02, AR = 8, e = 0.85: the C_L for maximum L/D is √(π·e·AR·C_D,0) = {N(math.sqrt(math.pi * 0.85 * 8 * 0.02), 3)}, (L/D)max = {N(math.sqrt(math.pi * 0.85 * 8 / (4 * 0.02)), 1)}"),
                                  L("Winglet cải thiện e mà không tăng sải cánh", "Winglets improve e without increasing the span")),
                       "explain": L("Công thức (L/D)max = ½√(π·e·AR/C_D,0) cho thấy hai đòn bẩy chính của tính năng: AR lớn (cánh dài) và C_D,0 nhỏ (máy bay sạch).", "The formula (L/D)max = ½√(π·e·AR/C_D,0) shows that a long wing and a clean aircraft (small C_D,0) are the two main levers of performance.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Lực cản cảm ứng và độ dốc lực nâng cánh hữu hạn", "Induced drag and the finite-wing lift slope")
    m["formula_math"] = ("V_tâm = Γ/(2R)  ·  α_i = C_L/(π AR)  ·  C_D,i = C_L²(1+δ)/(π AR) = C_L²/(π e AR)<br>a = a₀/[1 + (a₀/πAR)(1+τ)]  ·  (L/D)max = ½√(π e AR/C_D,0)" if lang == "vi" else
                         "V_centre = Γ/(2R)  ·  α_i = C_L/(π AR)  ·  C_D,i = C_L²(1+δ)/(π AR) = C_L²/(π e AR)<br>a = a₀/[1 + (a₀/πAR)(1+τ)]  ·  (L/D)max = ½√(π e AR/C_D,0)")
    m["legend"] = [("Γ", L("cường độ xoáy (m²/s)", "vortex strength (m²/s)")), ("α_i", L("góc tấn cảm ứng", "induced angle of attack")), ("δ, τ", L("hệ số hiệu chỉnh của cánh không elip", "correction factors for non-elliptical wings")),
                   ("e", L("hệ số hiệu suất sải cánh", "span efficiency factor")), ("AR", L("tỉ số kích thước b²/S", "aspect ratio b²/S")), ("a₀, a", L("độ dốc lực nâng 2D và 3D", "2D and 3D lift slopes"))]
    m["history_title"] = L("Lanchester, Prandtl và cánh elip", "Lanchester, Prandtl and the elliptical wing")
    m["history"] = L("Frederick Lanchester đưa ra ý tưởng về xoáy đầu cánh và lực cản cảm ứng trong khoảng 1894 đến 1907, nhưng công trình của ông ít được chú ý. Ludwig Prandtl phát triển lý thuyết đường nâng tại Göttingen trong giai đoạn 1911 đến 1918, cho ra các công thức định lượng mà Anderson trình bày ở mục 5.3. Các mục Historical Note 5.7 và 5.8 của sách kể lại câu chuyện này.",
                     "Frederick Lanchester proposed the idea of wing-tip vortices and induced drag between about 1894 and 1907, but his work was little noticed. Ludwig Prandtl developed lifting-line theory at Göttingen between 1911 and 1918, giving the quantitative formulas Anderson presents in section 5.3; the book's Historical Notes 5.7 and 5.8 tell the story.")
    m["case_title"] = L("Tình huống: tăng sải cánh", "Case: lengthening the wing")
    m["case"] = L(ul(f"Một cánh giả định bay ở C_L = 0,5, có AR = 8 và e = 1 (elip), cho C_D,i = {N(CDie, 5)}.",
                  f"Thiết kế lại với cùng diện tích nhưng AR = 12, cùng C_L: C_D,i = {N(CDi_AR12, 5)}, giảm {N((1 - CDi_AR12 / CDie) * 100, 0)}%, tức còn 8/12 giá trị cũ.",
                  "Cái giá phải trả: cánh dài nặng hơn và mômen uốn ở gốc cánh lớn hơn.",
                  "Số liệu chỉ để minh họa; công thức theo Anderson 5.3."),
                  ul(f"A hypothetical wing flying at C_L = 0.5 with AR = 8 and e = 1 (elliptical) has C_D,i = {N(CDie, 5)}.",
                  f"Redesigned with the same area but AR = 12 at the same C_L, C_D,i = {N(CDi_AR12, 5)}, a {N((1 - CDi_AR12 / CDie) * 100, 0)}% reduction: 8/12 of the old value.",
                  "The price: a longer wing is heavier and has a larger root bending moment.",
                  "The numbers are only illustrative; the formula is from Anderson 5.3."))
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L(ul("Cùng góc tấn không có nghĩa là cùng C_L khi AR khác nhau (Ví dụ 5.2).",
                  "Độ dốc a trong công thức tính theo rad⁻¹; muốn đổi sang độ thì chia cho 57,3.",
                  "δ và τ lấy từ đồ thị (Anderson Hình 5.20), phụ thuộc AR và độ thon. Ví dụ 5.1 và 5.2 dùng hai giá trị khác nhau.",
                  "Phân bố elip là tối ưu về C_D,i, nhưng cánh thật có e từ khoảng 0,7 đến 0,95.",
                  "Bài Anderson 5.1 và 5.2 cần Biot-Savart. Vận tốc tại tâm vòng xoáy là Γ/(2R), không phải Γ/(4πR)."),
                  ul("The same angle of attack does not mean the same C_L when AR differs (Example 5.2).",
                  "The slope a in the formula is per radian; divide by 57.3 to get per degree.",
                  "δ and τ come from a chart (Anderson Figure 5.20) and depend on AR and taper. Examples 5.1 and 5.2 use two different values.",
                  "The elliptical distribution is optimal for C_D,i, but real wings have e from about 0.7 to 0.95.",
                  "Anderson 5.1 and 5.2 need Biot-Savart. The velocity at the centre of the loop is Γ/(2R), not Γ/(4πR)."))
    m["nb_desc"] = L("Notebook tích phân số định luật Biot-Savart cho vòng xoáy (Bài 5.1, 5.2), giải lại Ví dụ 5.1 và 5.2, vẽ C_D,i theo AR và dùng assert để kiểm mọi đáp án quiz.",
                     "The notebook integrates the Biot-Savart law numerically for the vortex loop (Problems 5.1, 5.2), re-solves Examples 5.1 and 5.2, plots C_D,i against AR and uses assert to check every quiz answer.")

    SD = lambda i: 500 + i
    SUP = L("Câu luyện thêm", "Extra practice")
    book = [
        mcq(SD(1), "Anderson 6th, Problem 5.1", L("Vòng xoáy tròn bán kính R, cường độ Γ. Vận tốc cảm ứng tại tâm vòng là:", "A circular vortex loop of radius R and strength Γ. The induced velocity at the centre of the loop is:"),
            "Γ/(2R)", ["Γ/(4πR)", "Γ/(πR)", "Γ/(2πR)"], L("Tích phân Biot-Savart: mọi phần tử dl vuông góc r nên V = Γ/(4π) · 2πR/R² = Γ/(2R).", "Biot-Savart integral: every element dl is perpendicular to r so V = Γ/(4π) · 2πR/R² = Γ/(2R)."),
            L(f"<p>Kiểm số: R = 2, Γ = 1 cho {N(w51, 5)} (công thức {N(w51f, 5)}).</p>", f"<p>Numerical check: R = 2, Γ = 1 gives {N(w51, 5)} (formula {N(w51f, 5)}).</p>")),
        mcq(SD(2), "Anderson 6th, Problem 5.2", L("Với vòng xoáy bán kính R = 2 và Γ = 1, vận tốc cảm ứng trên trục tại A = 1,5 là:", "For a vortex loop of radius R = 2 and Γ = 1, the induced velocity on the axis at A = 1.5 is:"),
            N(w52f, 4), [N(w51f, 4), N(w52f * 2, 4), N(w52f / 2, 4)], L("V = ΓR²/[2(R² + A²)^{3/2}].", "V = ΓR²/[2(R² + A²)^{3/2}]."),
            L(f"<p>= 4/[2 × (4 + 2,25)^1,5] = {N(w52f, 5)}; tích phân số cho {N(w52, 5)}.</p>", f"<p>= 4/[2 × (4 + 2.25)^1.5] = {N(w52f, 5)}; numerical integration gives {N(w52, 5)}.</p>")),
        mcq(SD(3), L("Anderson 6th, Ví dụ 5.1", "Anderson 6th, Example 5.1"), L("Cánh AR = 8, δ = τ = 0,055, biên dạng mỏng đối xứng a₀ = 2π, α = 5°. Hệ số lực nâng C_L là:", "A wing with AR = 8, δ = τ = 0.055, thin symmetric airfoil a₀ = 2π, α = 5°. The lift coefficient C_L is:"),
            N(CL51, 3), [N(a0 * math.radians(5), 3), N(CL51 * 1.5, 3), N(CL51 / 2, 3)], L("a = a₀/[1 + (a₀/πAR)(1 + τ)] = 4,97/rad.", "a = a₀/[1 + (a₀/πAR)(1 + τ)] = 4.97/rad."),
            L(f"<p>a = {N(a51, 3)}/rad; C_L = a·α = {N(CL51, 4)} (sách 0,4335). Biên dạng 2D sẽ cho {N(a0 * math.radians(5), 3)}, sai nhiều.</p>", f"<p>a = {N(a51, 3)}/rad; C_L = a·α = {N(CL51, 4)} (book 0.4335). The 2D airfoil would give {N(a0 * math.radians(5), 3)}, much too high.</p>")),
        mcq(SD(4), L("Anderson 6th, Ví dụ 5.1", "Anderson 6th, Example 5.1"), L("Cũng cánh trên, lực cản cảm ứng C_D,i = C_L²(1 + δ)/(πAR) bằng:", "For the same wing, the induced drag coefficient C_D,i = C_L²(1 + δ)/(πAR) is:"),
            N(CD51, 5), [N(CD51 * 3, 5), N(CD51 / 3, 5), N(CL51 ** 2 / (math.pi * 8) / 2, 5)], L("(0,4339)²(1,055)/(8π).", "(0.4339)²(1.055)/(8π)."),
            L(f"<p>C_D,i = {N(CD51, 5)} (sách 0,00789).</p>", f"<p>C_D,i = {N(CD51, 5)} (book 0.00789).</p>")),
        mcq(SD(5), L("Anderson 6th, Ví dụ 5.2", "Anderson 6th, Example 5.2"), L("Cánh AR = 6, C_D,i = 0,01, δ = 0,055 cho C_L bằng:", "A wing with AR = 6, C_D,i = 0.01, δ = 0.055 has a C_L of:"),
            N(CL6, 3), [N(CL6 ** 2, 3), N(CL6 * 2, 3), N(0.01 * math.pi * 6, 3)], L("C_L² = πAR·C_D,i/(1 + δ).", "C_L² = πAR·C_D,i/(1 + δ)."),
            L(f"<p>C_L² = π·6·0,01/1,055 = {N(CL6 ** 2, 4)}; C_L = {N(CL6, 3)} (sách 0,423).</p>", f"<p>C_L² = π·6·0.01/1.055 = {N(CL6 ** 2, 4)}; C_L = {N(CL6, 3)} (book 0.423).</p>")),
        mcq(SD(6), L("Anderson 6th, Ví dụ 5.2", "Anderson 6th, Example 5.2"), L("Biên dạng của hai cánh (AR = 6 và AR = 10) có a₀ xấp xỉ:", "The airfoil of the two wings (AR = 6 and AR = 10) has a₀ of about:"),
            f"{N(a0b, 2)} rad⁻¹", [f"{N(2 * math.pi, 2)} rad⁻¹", f"{N(a6, 2)} rad⁻¹", f"{N(a0b * 1.3, 2)} rad⁻¹"], L("Giải a = a₀/[1 + (1 + τ)a₀/(π AR)] cho a₀.", "Solve a = a₀/[1 + (1 + τ)a₀/(π AR)] for a₀."),
            L(f"<p>a₀ = a/(1 − a(1 + τ)/(π·AR)) = {N(a0b, 3)}/rad (sách 5,989). Giá trị này gần 2π nhưng nhỏ hơn một chút do độ dày.</p>", f"<p>a₀ = a/(1 − a(1 + τ)/(π·AR)) = {N(a0b, 3)}/rad (book 5.989). It is close to 2π but slightly lower due to thickness.</p>")),
    ]
    gen = [
        mcq(SD(11), SUP, L("Cánh elip, C_L = 0,5 và AR = 8. Góc tấn cảm ứng α_i bằng:", "An elliptical wing with C_L = 0.5 and AR = 8. The induced angle of attack α_i is:"), f"{N(math.degrees(ai), 3)}°", [f"{N(math.degrees(ai) * 2, 3)}°", f"{N(math.degrees(ai) / 2, 3)}°", f"{N(math.degrees(0.5 / 8), 3)}°"], L("α_i = C_L/(π·AR) = 0,0199 rad.", "α_i = C_L/(π·AR) = 0.0199 rad.")),
        mcq(SD(12), SUP, L("Giữ nguyên C_L, tăng AR từ 8 lên 12 thì C_D,i:", "Keeping C_L fixed, raising AR from 8 to 12 makes C_D,i:"), L("giảm còn 2/3", "fall to 2/3"), [L("tăng gấp 1,5", "increase 1.5 times"), L("không đổi", "stay the same"), L("giảm còn 4/9", "fall to 4/9")], L("C_D,i tỉ lệ nghịch với AR: 8/12.", "C_D,i is inversely proportional to AR: 8/12.")),
        mcq(SD(13), SUP, L("Bay chậm hơn nhưng vẫn thẳng đều thì lực cản cảm ứng:", "Flying slower but still level makes the induced drag:"), L("tăng vì C_L tăng", "increase because C_L rises"), [L("giảm vì tốc độ giảm", "decrease because speed falls"), L("không đổi", "stay the same"), L("bằng không", "vanish")], L("C_D,i ∝ C_L² và C_L ∝ 1/V² nên D_i ∝ 1/V².", "C_D,i ∝ C_L² and C_L ∝ 1/V² so D_i ∝ 1/V².")),
        mcq(SD(14), SUP, L("Hệ số hiệu suất sải cánh e = 1/(1 + δ). Với δ = 0,055 thì e bằng:", "The span efficiency factor e = 1/(1 + δ). For δ = 0.055 e equals:"), N(1 / 1.055, 3), [N(1.055, 3), N(1 - 0.055 * 2, 3), N(0.055, 3)], L("e = 1/1,055 = 0,948.", "e = 1/1.055 = 0.948.")),
        mcq(SD(15), SUP, L("Với C_D,0 = 0,02, AR = 8, e = 0,85, (L/D)max = ½√(π e AR/C_D,0) xấp xỉ:", "With C_D,0 = 0.02, AR = 8, e = 0.85, (L/D)max = ½√(π e AR/C_D,0) is about:"), N(math.sqrt(math.pi * 0.85 * 8 / (4 * 0.02)), 1), [N(math.sqrt(math.pi * 0.85 * 8 / 0.02), 1), N(8.0, 1), N(30.0, 1)], L(f"Tại cực đại, C_D,i = C_D,0 nên C_D = 0,04 và C_L = {N(math.sqrt(math.pi * 0.85 * 8 * 0.02), 3)}.", f"At the maximum C_D,i = C_D,0 so C_D = 0.04 and C_L = {N(math.sqrt(math.pi * 0.85 * 8 * 0.02), 3)}.")),
        mcq(SD(16), SUP, L("Winglet chủ yếu làm gì?", "What do winglets mainly do?"), L("Làm yếu xoáy đầu cánh, giảm lực cản cảm ứng", "Weaken the tip vortices and reduce induced drag"), [L("Tăng C_L max", "Raise C_Lmax"), L("Giảm lực cản ma sát da", "Reduce skin-friction drag"), L("Tăng độ dày cánh", "Increase the wing thickness")], L("EASA Hình 2-20.", "EASA Figure 2-20.")),
    ]
    m["quiz_sets"] = [
        {"key": "anderson", "title": L("Sách 2, Anderson: Bài 5.1, 5.2 và Ví dụ 5.1, 5.2 (đáp án đã tính lại)", "Book 2, Anderson: Problems 5.1, 5.2 and Examples 5.1, 5.2 (answers recomputed)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập thêm (tự soạn, đáp án đã kiểm bằng tính toán)", "Extra practice (written for this site, answers checked by calculation)"), "items": gen},
    ]
    m["problems_intro"] = L("Bài 5.1, 5.2 và Ví dụ 5.1, 5.2, giải từng bước. Kết quả được kiểm bằng tích phân số hoặc so với số in trong sách.", "Problems 5.1, 5.2 and Examples 5.1, 5.2, solved step by step. Results are checked by numerical integration or against the numbers printed in the book.")
    m["problems"] = [
        {"num": "5.1 – 5.2", "src": "Anderson 6th, Problems 5.1, 5.2", "q": L("Vòng xoáy tròn bán kính R, cường độ Γ: tìm vận tốc cảm ứng tại tâm và tại điểm cách mặt phẳng vòng khoảng A trên trục.", "A circular vortex loop of radius R and strength Γ: find the induced velocity at the centre and at a point on the axis a distance A from the plane of the loop."),
         "ans": L(f"<p>Biot-Savart: dV = (Γ/4π)·dl×r/r³. Tại tâm, |dl×r| = R dθ·R, r = R nên V = (Γ/4π)·2π/R = <b>Γ/(2R)</b>.</p><p>Trên trục chỉ thành phần dọc trục còn lại, nhân thêm R/r với r = √(R²+A²): V = <b>ΓR²/[2(R²+A²)^{{3/2}}]</b>.</p><p class='pill'>Kiểm số: R = 2, Γ = 1: tâm {N(w51, 5)}; A = 1,5: {N(w52, 5)}.</p>", f"<p>Biot-Savart: dV = (Γ/4π)·dl×r/r³. At the centre |dl×r| = R dθ·R and r = R so V = (Γ/4π)·2π/R = <b>Γ/(2R)</b>.</p><p>On the axis only the axial component survives, adding a factor R/r with r = √(R²+A²): V = <b>ΓR²/[2(R²+A²)^{{3/2}}]</b>.</p><p class='pill'>Numerical check: R = 2, Γ = 1: centre {N(w51, 5)}; A = 1.5: {N(w52, 5)}.</p>")},
        {"num": "Ví dụ 5.1" if lang == "vi" else "Ex. 5.1", "src": "Anderson 6th, Example 5.1", "q": L("AR = 8, δ = τ = 0,055, biên dạng mỏng đối xứng, α = 5°: tính C_L và C_D,i.", "AR = 8, δ = τ = 0.055, thin symmetric airfoil, α = 5°: find C_L and C_D,i."),
         "ans": L(f"<p>a = 2π/[1 + (2π/8π)(1,055)] = <b>{N(a51, 3)} rad⁻¹</b> = {N(a51d, 4)}/độ.</p><p>C_L = aα = <b>{N(CL51, 4)}</b>; C_D,i = C_L²(1+δ)/(πAR) = <b>{N(CD51, 5)}</b>.</p>", f"<p>a = 2π/[1 + (2π/8π)(1.055)] = <b>{N(a51, 3)} rad⁻¹</b> = {N(a51d, 4)}/deg.</p><p>C_L = aα = <b>{N(CL51, 4)}</b>; C_D,i = C_L²(1+δ)/(πAR) = <b>{N(CD51, 5)}</b>.</p>")},
        {"num": "Ví dụ 5.2" if lang == "vi" else "Ex. 5.2", "src": "Anderson 6th, Example 5.2", "q": L("Cánh AR = 6 có C_D,i = 0,01 tại α = 3,4° (α_L=0 = −2°, δ = τ = 0,055). Tìm C_D,i của cánh AR = 10 (δ = τ = 0,105) cùng biên dạng, cùng α.", "A wing of AR = 6 has C_D,i = 0.01 at α = 3.4° (α_L=0 = −2°, δ = τ = 0.055). Find C_D,i of a wing of AR = 10 (δ = τ = 0.105) with the same airfoil at the same α."),
         "ans": L(f"<p>C_L = √(πAR·C_D,i/(1+δ)) = {N(CL6, 3)}; a = C_L/(5,4°) = {N(a6, 3)}/rad; a₀ = a/[1 − a(1+τ)/(πAR)] = <b>{N(a0b, 3)}</b>/rad.</p><p>AR = 10: a = {N(a10, 3)}/rad; C_L = a(5,4°) = <b>{N(CL10, 3)}</b>; C_D,i = <b>{N(CD10, 4)}</b> (sách 0,0076).</p>", f"<p>C_L = √(πAR·C_D,i/(1+δ)) = {N(CL6, 3)}; a = C_L/(5.4°) = {N(a6, 3)}/rad; a₀ = a/[1 − a(1+τ)/(πAR)] = <b>{N(a0b, 3)}</b>/rad.</p><p>AR = 10: a = {N(a10, 3)}/rad; C_L = a(5.4°) = <b>{N(CL10, 3)}</b>; C_D,i = <b>{N(CD10, 4)}</b> (book 0.0076).</p>")},
    ]
    return m
