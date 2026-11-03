# -*- coding: utf-8 -*-
"""Module 07: Song xung kich xien va song gian no. Nguon: Anderson 6th ch.9 (Bai 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20), EASA M08 SM3 (tr.3.13 song xung kich, Hinh 3-11)."""
import math
from aero import *
from common import num, ul, table, mcq

d2r = math.radians


def theta_max(M):
    mu = math.asin(1 / M)
    return max(theta_beta_m(M, mu + (math.pi / 2 - mu) * i / 20000) for i in range(1, 20000))


def flat_plate(M, alpha_deg):
    """Shock-expansion cho tam phang mong: (cl, cdw) hoac None neu song tach."""
    th = d2r(alpha_deg)
    if th > theta_max(M): return None
    b = beta_from_theta(M, th); pl = oblique(M, b, th)["p"]
    Mu = mach_from_pm(prandtl_meyer(M) + th); pu = p0_over_p(M) / p0_over_p(Mu)
    q = GAMMA / 2 * M * M
    return (pl - pu) / q * math.cos(th), (pl - pu) / q * math.sin(th)


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    mu91 = math.degrees(math.asin(1 / 1.5)); alt91 = 559 * math.tan(math.asin(1 / 1.5))
    o92 = oblique(4, d2r(30)); p92 = 2.65e4 * o92["p"]; T92 = 223.3 * o92["T"]; p02_92 = 2.65e4 * p0_over_p(4) * o92["p0"]; T02_92 = 223.3 * T0_over_T(4); ds92 = -R_SI * math.log(o92["p0"])
    o94 = oblique(3, d2r(36.87)); p02_94 = p0_over_p(3) * o94["p0"]; p02_94w = rayleigh_pitot_ratio(3 * math.sin(d2r(36.87)))
    b95 = beta_from_theta(2.5, d2r(22.2)); o95 = oblique(2.5, b95, d2r(22.2))
    tm96 = theta_max(2.4); b96 = beta_from_theta(2.4, tm96 - 1e-6); p96 = oblique(2.4, b96, tm96)["p"]
    p98a = normal_shock_p0(4)
    b98 = beta_from_theta(4, d2r(25.3)); o98 = oblique(4, b98, d2r(25.3)); p98b = o98["p0"] * normal_shock_p0(o98["M2"])
    b98c = beta_from_theta(o98["M2"], d2r(20)); o98c = oblique(o98["M2"], b98c, d2r(20)); p98c = o98["p0"] * o98c["p0"] * normal_shock_p0(o98c["M2"])
    fp = {a: flat_plate(2.6, a) for a in (5, 15, 30)}
    nu_max = math.degrees(prandtl_meyer(1e7))
    nu920 = prandtl_meyer(3) + d2r(20); M920 = mach_from_pm(nu920); pexp = p0_over_p(3) / p0_over_p(M920)
    b920 = beta_from_theta(M920, d2r(20)); o920 = oblique(M920, b920, d2r(20)); p920 = pexp * o920["p"]

    m = {"num": "07", "slug": "07-oblique-shocks", "tag": L("Sóng xiên", "Oblique shocks")}
    m["title"] = L("Sóng xung kích xiên, sóng giãn nở Prandtl-Meyer và cánh siêu âm", "Oblique shocks, Prandtl-Meyer expansion waves and the supersonic airfoil")
    m["src"] = L("Anderson ch.9 (Bài 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20) · EASA Module 08, Sub-module 03 (tr. 3.13, Hình 3-11)", "Anderson ch. 9 (Problems 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20) · EASA Module 08, Sub-module 03 (p. 3.13, Figure 3-11)")
    m["intro"] = L("Khi dòng siêu âm bị bẻ lệch một góc, nó tạo ra sóng xung kích xiên (nén) hoặc sóng giãn nở Prandtl-Meyer (mở rộng). Module này giải các bài ch.9 của Anderson: góc Mach, quan hệ θ-β-M, góc lệch cực đại và sóng tách rời; tổn thất áp suất toàn phần của hệ nhiều sóng (cửa hút siêu âm); góc quay Prandtl-Meyer tối đa 130,45° từ dòng âm thanh; và lý thuyết sóng xung kích-giãn nở cho tấm phẳng ở M = 2,6. Mọi số đều được tính trực tiếp từ công thức, không tra bảng.",
                   "When a supersonic flow is turned through an angle it forms an oblique shock (compression) or a Prandtl-Meyer expansion fan. This module solves the ch. 9 problems of Anderson: Mach angle, the θ-β-M relation, maximum deflection and detached shocks; total-pressure loss in multi-wave systems (supersonic inlets); the maximum Prandtl-Meyer turn of 130.45° from sonic flow; and shock-expansion theory for a flat plate at M = 2.6. Every number is computed directly from the formulas, with no tables.")
    m["mapping"] = {
        "easa": L("Sub-module 03 (tr. 3.13 Shock waves, Hình 3-11: sóng thẳng và sóng cung quanh biên dạng; tr. 3.14 Sweepback)", "Sub-module 03 (p. 3.13 Shock waves, Figure 3-11: normal and bow shocks around an airfoil; p. 3.14 Sweepback)"),
        "anderson": L("Ch.9 Oblique Shock and Expansion Waves (9.2 sóng xiên, 9.3 θ-β-M và nêm, 9.4 tương tác, 9.5 sóng tách rời, 9.6 sóng giãn nở, 9.7 sóng xung kích-giãn nở); Bài 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20", "Ch.9 Oblique Shock and Expansion Waves (9.2 oblique shock, 9.3 θ-β-M and wedges, 9.4 interactions, 9.5 detached shock, 9.6 expansion waves, 9.7 shock-expansion theory); Problems 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20"),
        "etkin": L("Không có. Etkin &amp; Reid chỉ xét tốc độ chưa có hiệu ứng nén được mạnh", "None. Etkin &amp; Reid only treat speeds below strong compressibility effects"),
        "note": L("Phần này vượt ra ngoài EASA Module 08 (Level 2) nhưng nằm trong mục tiêu CO2 của đề cương (hiệu ứng ở tốc độ cao).", "This goes beyond EASA Module 08 (Level 2) but sits within the syllabus objective CO2 (high-speed effects)."),
    }
    parts = []
    parts.append({"title": L("Sóng Mach và sóng xiên", "Mach waves and oblique shocks"),
                  "bullets": [L("Nhiễu nhỏ trong dòng siêu âm tạo sóng Mach với góc μ = arcsin(1/M)", "A small disturbance in supersonic flow makes a Mach wave at angle μ = arcsin(1/M)"),
                              L("Nhiễu hữu hạn tạo sóng xiên với góc β > μ", "A finite disturbance makes an oblique shock at β > μ"),
                              L("Sóng xiên là sóng thẳng ở thành phần pháp tuyến M₁ sin β", "An oblique shock is a normal shock for the normal component M₁ sin β")],
                  "slides": [{"title": L("Bài 9.1 và 9.2", "Problems 9.1 and 9.2"),
                              "body": ul(L(f"9.1: tên lửa bay M = 1,5 ở độ cao thấp, sóng Mach từ mũi cắt mặt đất tại điểm cách mũi 559 ft về phía sau. μ = arcsin(1/1,5) = {N(mu91, 2)}°, nên độ cao = 559·tan μ = {N(alt91, 0)} ft", f"9.1: a missile flies at M = 1.5 at low altitude and the Mach wave from its nose meets the ground 559 ft behind the nose. μ = arcsin(1/1.5) = {N(mu91, 2)}°, so the altitude = 559·tan μ = {N(alt91, 0)} ft"),
                                         L("9.2: M = 4, β = 30°, p₁ = 2,65×10⁴ N/m², T₁ = 223,3 K (độ cao chuẩn 10 000 m). Kết quả:", "9.2: M = 4, β = 30°, p₁ = 2.65×10⁴ N/m², T₁ = 223.3 K (standard altitude 10 000 m). Results:")) +
                                  table([L("Đại lượng", "Quantity"), L("Giá trị", "Value")],
                                        [["M_n1 = M₁ sin β", N(o92['Mn1'], 3)], [L("Góc lệch dòng θ", "Flow deflection θ"), f"{N(math.degrees(o92['theta']), 2)}°"], [L("M₂ sau sóng", "M₂ behind the wave"), N(o92['M2'], 3)],
                                         ["p₂", f"{N(p92, 0)} N/m²"], ["T₂", f"{N(T92, 1)} K"], ["p₀,₂", f"{N(p02_92, 0)} N/m²"], ["T₀,₂", f"{N(T02_92, 1)} K"], [L("Δs (tăng entropi)", "Δs (entropy rise)"), f"{N(ds92, 1)} J/(kg·K)"]]),
                              "explain": L("Độ cao ra đúng 500 ft, một số tròn. Ở 9.2, M_n1 = M₁ sin β = 4 sin 30° = 2,000, nên có thể dùng bảng sóng thẳng ở M = 2.", "The altitude comes out as exactly 500 ft, a round number. In 9.2, M_n1 = M₁ sin β = 4 sin 30° = 2.000, so the normal-shock table at M = 2 applies.")}]})
    parts.append({"title": L("Quan hệ θ-β-M và góc lệch cực đại", "The θ-β-M relation and maximum deflection"),
                  "bullets": [L("tan θ = 2cot β·(M₁²sin²β − 1)/[M₁²(γ + cos 2β) + 2]", "tan θ = 2cot β·(M₁²sin²β − 1)/[M₁²(γ + cos 2β) + 2]"),
                              L("Với mỗi M₁ có một góc lệch cực đại θ_max; vượt quá giá trị đó, sóng tách khỏi vật, cong và đứng phía trước vật", "For a given M₁ there is a maximum deflection θ_max; beyond it the shock detaches and curves ahead of the body"),
                              L("Mỗi θ < θ_max có hai nghiệm β: sóng yếu (thường gặp) và sóng mạnh", "Every θ < θ_max has two solutions β: the weak (usual) and the strong shock")],
                  "slides": [{"title": L("Bài 9.5 và 9.6", "Problems 9.5 and 9.6"),
                              "body": ul(L(f"9.5: nêm nửa góc 22,2°, M₁ = 2,5: β = {N(math.degrees(b95), 2)}°, p₂ = {N(o95['p'], 2)} atm, T₂ = {N(300 * o95['T'], 0)} K, M₂ = {N(o95['M2'], 3)}", f"9.5: 22.2° half-angle wedge, M₁ = 2.5: β = {N(math.degrees(b95), 2)}°, p₂ = {N(o95['p'], 2)} atm, T₂ = {N(300 * o95['T'], 0)} K, M₂ = {N(o95['M2'], 3)}"),
                                         L(f"9.6: ở M = 2,4, θ_max = {N(math.degrees(tm96), 2)}° là góc tấn lớn nhất để sóng còn bám vào mép trước, và áp suất lớn nhất trên mặt tấm khi đó là p₂/p₁ = {N(p96, 2)}", f"9.6: at M = 2.4, θ_max = {N(math.degrees(tm96), 2)}° is the largest angle of attack with the shock still attached at the leading edge, and the maximum surface pressure is then p₂/p₁ = {N(p96, 2)}"),
                                         L("β là nghiệm của một phương trình lượng giác; ở đây ta tìm nó bằng phương pháp chia đôi", "β is the root of a trigonometric equation; here it is found by bisection")),
                              "explain": L("Góc lệch 22,2° ở M 2,5 khá gần θ_max (≈ 29,8°) nên sóng khá mạnh; lệch thêm nữa thì sóng sẽ tách rời.", "A 22.2° deflection at M 2.5 is fairly close to θ_max (≈ 29.8°) so the shock is quite strong; more would detach it.")}]})
    parts.append({"title": L("Tổn thất áp suất toàn phần và cửa hút siêu âm", "Total-pressure loss and the supersonic inlet"),
                  "bullets": [L("Làm chậm dòng siêu âm bằng nhiều sóng xiên rồi một sóng thẳng yếu mất ít p₀ hơn một sóng thẳng mạnh", "Slowing a supersonic flow with several oblique shocks and then a weak normal shock loses less p₀ than one strong normal shock"),
                              L("Với sóng xiên, dùng p₀,₂/p₀,₁ theo M_n1; không dùng được cột p₀,₂/p₁ của bảng sóng thẳng (Bài 9.3, 9.4)", "For an oblique shock use p₀,₂/p₀,₁ with M_n1; the p₀,₂/p₁ column of the normal-shock table cannot be used (Problems 9.3, 9.4)"),
                              L("Đó là nguyên lý của cửa hút khí động cơ siêu âm", "This is the principle of the supersonic engine inlet")],
                  "slides": [{"title": L("Bài 9.4 và 9.8", "Problems 9.4 and 9.8"),
                              "body": table([L("Hệ sóng ở M = 4", "Shock system at M = 4"), "p₀,final/p₀,1"],
                                            [[L("(a) một sóng thẳng", "(a) one normal shock"), N(p98a, 3)], [L("(b) sóng xiên 25,3° + sóng thẳng", "(b) 25.3° oblique + normal"), N(p98b, 3)], [L("(c) sóng xiên 25,3° + 20° + sóng thẳng", "(c) 25.3° + 20° obliques + normal"), N(p98c, 3)]]) +
                              ul(L(f"9.4: β = 36,87°, M₁ = 3: tính đúng thì p₀,₂ = {N(p02_94, 2)} atm, còn dùng nhầm p₀,₂/p₁ sẽ ra {N(p02_94w, 2)} atm", f"9.4: β = 36.87°, M₁ = 3: computed correctly p₀,₂ = {N(p02_94, 2)} atm, whereas misusing p₀,₂/p₁ gives {N(p02_94w, 2)} atm")),
                              "explain": L(f"Thêm sóng xiên nâng phần p₀ giữ lại từ {N(p98a * 100, 0)}% lên {N(p98c * 100, 0)}%: càng chia thành nhiều bước nén nhỏ thì càng ít tổn thất.", f"Adding oblique shocks lifts the retained p₀ from {N(p98a * 100, 0)}% to {N(p98c * 100, 0)}%: the more small compression steps, the smaller the loss.")}]})
    parts.append({"title": L("Sóng giãn nở Prandtl-Meyer", "Prandtl-Meyer expansion waves"),
                  "bullets": [L("Dòng siêu âm đi qua một góc lồi sẽ giãn nở qua một quạt sóng Mach, và không mất p₀", "Supersonic flow turning round a convex corner expands through a fan of Mach waves with no loss in p₀"),
                              L("Góc Prandtl-Meyer ν(M): θ = ν(M₂) − ν(M₁)", "The Prandtl-Meyer angle ν(M): θ = ν(M₂) − ν(M₁)"),
                              L("Quay tối đa từ dòng âm thanh là ν(∞) = 130,45°", "The maximum turn from sonic flow is ν(∞) = 130.45°")],
                  "slides": [{"title": L("Bài 9.15 và 9.20", "Problems 9.15 and 9.20"),
                              "body": ul(L(f"9.15: ν(∞) = (√((γ+1)/(γ−1)) − 1)·90° = {N(nu_max, 2)}°", f"9.15: ν(∞) = (√((γ+1)/(γ−1)) − 1)·90° = {N(nu_max, 2)}°"),
                                         L(f"9.20: M₁ = 3, p₁ = 1 atm, giãn nở 20° rồi nén 20°: sau giãn nở M = {N(M920, 3)}, p/p₁ = {N(pexp, 3)}; sau nén M₃ = {N(o920['M2'], 3)}, p₃ = {N(p920, 3)} atm", f"9.20: M₁ = 3, p₁ = 1 atm, a 20° expansion then a 20° compression: after the expansion M = {N(M920, 3)}, p/p₁ = {N(pexp, 3)}; after the compression M₃ = {N(o920['M2'], 3)}, p₃ = {N(p920, 3)} atm"),
                                         L("p₃ ≠ p₁ dù dòng cùng hướng: sóng nén mất p₀, sóng giãn nở thì không", "p₃ ≠ p₁ although the flow direction is the same: the compression shock loses p₀ while the expansion does not")),
                              "explain": L("Bài 9.20 hỏi vì sao áp suất cuối khác ban đầu. Lý do: sóng xung kích không thuận nghịch, entropi tăng, nên dòng không thể trở về trạng thái ban đầu.", "Problem 9.20 asks why the final pressure differs from the initial one. The reason is that the shock is irreversible and entropy rises, so the original state cannot be recovered.")}]})
    parts.append({"title": L("Tấm phẳng siêu âm: lý thuyết sóng xung kích-giãn nở", "The supersonic flat plate: shock-expansion theory"),
                  "bullets": [L("Mặt dưới nhận sóng xiên (áp suất tăng), mặt trên nhận sóng giãn nở (áp suất giảm)", "The lower surface gets an oblique shock (pressure up), the upper surface an expansion (pressure down)"),
                              L("Lực nâng c_l = (p_l − p_u)cos α/q và lực cản sóng c_d,w = (p_l − p_u)sin α/q", "Lift c_l = (p_l − p_u)cos α/q and wave drag c_d,w = (p_l − p_u)sin α/q"),
                              L("Lý thuyết tuyến tính của Ackeret: c_l = 4α/√(M² − 1)", "Ackeret's linear theory: c_l = 4α/√(M² − 1)")],
                  "slides": [{"title": L("Bài 9.13: tấm phẳng ở M = 2,6", "Problem 9.13: a flat plate at M = 2.6"),
                              "body": table([L("α", "α"), "c_l", "c_d,w", L("c_l Ackeret", "Ackeret c_l")],
                                            [[f"{a}°", N(fp[a][0], 3), N(fp[a][1], 3), N(4 * d2r(a) / math.sqrt(2.6 ** 2 - 1), 3)] for a in (5, 15, 30)]) +
                              f"<p class='pill'>{L('Ackeret chỉ chính xác với α nhỏ: ở 30° c_l thật lớn hơn 17% so với tuyến tính', 'Ackeret is accurate only for small α: at 30° the true c_l is 17% above the linear value')}</p>",
                              "explain": L("Ở 5° hai lý thuyết gần như trùng; từ 15° trở lên cần dùng sóng xung kích-giãn nở chính xác.", "At 5° the two theories almost coincide; from 15° up the exact shock-expansion method is needed.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Quan hệ θ-β-M, Prandtl-Meyer và Ackeret", "The θ-β-M relation, Prandtl-Meyer and Ackeret")
    m["formula_math"] = ("tan θ = 2cot β (M₁²sin²β − 1)/[M₁²(γ + cos 2β) + 2]  ·  μ = arcsin(1/M)  ·  M_n1 = M₁ sin β<br>ν(M) = √((γ+1)/(γ−1)) arctan√((γ−1)(M²−1)/(γ+1)) − arctan√(M²−1)  ·  θ = ν(M₂) − ν(M₁)  ·  c_l = 4α/√(M²−1)" if lang == "vi" else
                         "tan θ = 2cot β (M₁²sin²β − 1)/[M₁²(γ + cos 2β) + 2]  ·  μ = arcsin(1/M)  ·  M_n1 = M₁ sin β<br>ν(M) = √((γ+1)/(γ−1)) arctan√((γ−1)(M²−1)/(γ+1)) − arctan√(M²−1)  ·  θ = ν(M₂) − ν(M₁)  ·  c_l = 4α/√(M²−1)")
    m["legend"] = [("θ, β", L("góc lệch dòng và góc sóng", "flow deflection and wave angle")), ("μ", L("góc Mach", "Mach angle")), ("M_n1", L("Mach pháp tuyến", "normal Mach number")), ("ν", L("hàm Prandtl-Meyer", "Prandtl-Meyer function")), ("p₀", L("áp suất toàn phần", "total pressure")), ("α", L("góc tấn", "angle of attack"))]
    m["history_title"] = L("Mach, Prandtl, Meyer và Ackeret", "Mach, Prandtl, Meyer and Ackeret")
    m["history"] = L("Năm 1887, Ernst Mach chụp được ảnh viên đạn siêu âm cùng sóng xung kích của nó; Anderson dành riêng một mục Historical Note (9.11) cho ông. Theodor Meyer (học trò của Prandtl) đưa ra lời giải sóng giãn nở trong luận án năm 1908, nên có tên Prandtl-Meyer. Jakob Ackeret công bố lý thuyết tuyến tính cho cánh siêu âm năm 1925. Các bảng nén được NACA TR-1135 (1953) tổng hợp các kết quả này.",
                     "In 1887 Ernst Mach photographed a supersonic bullet with its shock waves; Anderson devotes a Historical Note (9.11) to him. Theodor Meyer, a student of Prandtl, gave the expansion-wave solution in his 1908 dissertation, hence the name Prandtl-Meyer. Jakob Ackeret published the linear theory for supersonic airfoils in 1925. The NACA compressible-flow tables TR-1135 (1953) collect these results.")
    m["case_title"] = L("Tình huống: nén dòng ở cửa hút M = 4", "Case: slowing an M = 4 flow at an inlet")
    m["case"] = L(ul(f"Một cửa hút giả định nhận dòng M = 4. Dùng một sóng thẳng thì chỉ còn {N(p98a * 100, 1)}% áp suất toàn phần.",
                  f"Thêm trước đó một sóng xiên 25,3° thì còn {N(p98b * 100, 1)}%, và thêm sóng xiên 20° nữa thì còn {N(p98c * 100, 1)}% (Anderson 9.8).",
                  "Vì vậy cửa hút của máy bay siêu âm có nón hoặc dốc nén nhiều bước.",
                  "Các số là kết quả của bài trong sách, không phải dữ liệu của một cửa hút cụ thể."),
                  ul(f"A hypothetical inlet receives M = 4 flow. With one normal shock only {N(p98a * 100, 1)}% of the total pressure remains.",
                  f"Adding a 25.3° oblique shock ahead raises it to {N(p98b * 100, 1)}%, and a further 20° oblique shock to {N(p98c * 100, 1)}% (Anderson 9.8).",
                  "That is why supersonic aircraft inlets have a multi-step cone or ramp.",
                  "The numbers come from the book problem, not from a specific inlet."))
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L(ul("Số Mach sau sóng xiên là M₂ = M_n2/sin(β − θ), không phải M_n2.",
                  "Phải chọn đúng nghiệm β (yếu hay mạnh); sóng yếu là trường hợp thường gặp.",
                  "Cột p₀,₂/p₁ của bảng chỉ dùng cho sóng thẳng, nên không thể dùng với M_n1 của sóng xiên để tính p₀,₂ (Bài 9.3, 9.4).",
                  "Sau khi giãn nở rồi nén cùng một góc, áp suất không trở về giá trị ban đầu vì sóng nén làm mất p₀ (Bài 9.20).",
                  "Lý thuyết Ackeret chỉ dùng cho góc nhỏ."),
                  ul("The Mach number behind an oblique shock is M₂ = M_n2/sin(β − θ), not M_n2.",
                  "Choose the correct root β (weak or strong); the weak one is the usual case.",
                  "The p₀,₂/p₁ column of the table applies only to a normal shock, so it cannot be used with the M_n1 of an oblique shock to find p₀,₂ (Problems 9.3, 9.4).",
                  "After an expansion and an equal compression the pressure does not return to its original value, because the compression shock loses p₀ (Problem 9.20).",
                  "Ackeret theory is for small angles only."))
    m["nb_desc"] = L("Notebook giải phương trình θ-β-M bằng chia đôi, tính Prandtl-Meyer, giải lại Anderson 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20, và dùng assert để kiểm các đáp án quiz.", "The notebook solves the θ-β-M equation by bisection, evaluates Prandtl-Meyer, re-solves Anderson 9.1, 9.2, 9.4, 9.5, 9.6, 9.8, 9.13, 9.15, 9.20, and uses assert to check the quiz answers.")

    SD = lambda i: 700 + i
    SUP = L("Câu luyện thêm", "Extra practice")
    Q = lambda i, src, q, r, w, ex, det=None: mcq(SD(i), src, q, r, w, ex, det)
    book = [
        Q(1, "Anderson 6th, Problem 9.1", L("Tên lửa bay M = 1,5; sóng Mach từ mũi cắt mặt đất ở 559 ft phía sau mũi. Độ cao bay là:", "A missile flies at M = 1.5; the Mach wave from the nose meets the ground 559 ft behind the nose. The altitude is:"), f"{N(alt91, 0)} ft", [f"{N(559 / math.tan(math.asin(1 / 1.5)), 0)} ft", f"{N(559 * math.sin(math.asin(1 / 1.5)), 0)} ft", "559 ft"], L("μ = arcsin(1/1,5) = 41,81°; h = 559 tan μ.", "μ = arcsin(1/1.5) = 41.81°; h = 559 tan μ.")),
        Q(2, "Anderson 6th, Problem 9.2", L("Sóng xiên β = 30° trong dòng M = 4. Thành phần Mach pháp tuyến M_n1 là:", "An oblique shock with β = 30° in an M = 4 flow. The normal Mach number M_n1 is:"), N(o92["Mn1"], 2), [N(4 * math.cos(d2r(30)), 2), N(4.0, 2), N(0.5, 2)], L("M_n1 = M₁ sin β.", "M_n1 = M₁ sin β.")),
        Q(3, "Anderson 6th, Problem 9.2", L("Cũng bài 9.2 (p₁ = 2,65×10⁴ N/m²). Áp suất sau sóng p₂ là:", "Same problem 9.2 (p₁ = 2.65×10⁴ N/m²). The pressure behind the wave p₂ is:"), f"{N(p92, 0)} N/m²", [f"{N(p92 / 2, 0)} N/m²", f"{N(2.65e4 * 7.2, 0)} N/m²", f"{N(2.65e4, 0)} N/m²"], L("p₂/p₁ = 4,5 ở M_n1 = 2.", "p₂/p₁ = 4.5 at M_n1 = 2.")),
        Q(4, "Anderson 6th, Problem 9.4", L("Sóng β = 36,87°, M₁ = 3, p₁ = 1 atm. Áp suất toàn phần sau sóng, tính đúng, là:", "A wave with β = 36.87°, M₁ = 3, p₁ = 1 atm. The total pressure behind it, computed correctly, is:"), f"{N(p02_94, 1)} atm", [f"{N(p02_94w, 1)} atm", f"{N(p0_over_p(3), 1)} atm", f"{N(p02_94 * 1.4, 1)} atm"], L("Dùng p₀,₂/p₀,₁ với M_n1 rồi nhân p₀,₁.", "Use p₀,₂/p₀,₁ with M_n1 then multiply by p₀,₁."), L(f"<p>p₀,₁ = {N(p0_over_p(3), 2)} atm; p₀,₂/p₀,₁ = {N(o94['p0'], 4)} nên p₀,₂ = {N(p02_94, 2)} atm. Cách sai (p₀,₂/p₁) cho {N(p02_94w, 2)} atm.</p>", f"<p>p₀,₁ = {N(p0_over_p(3), 2)} atm; p₀,₂/p₀,₁ = {N(o94['p0'], 4)} so p₀,₂ = {N(p02_94, 2)} atm. The wrong way (p₀,₂/p₁) gives {N(p02_94w, 2)} atm.</p>")),
        Q(5, "Anderson 6th, Problem 9.5", L("Nêm nửa góc 22,2° trong dòng M₁ = 2,5. Góc sóng β (sóng yếu) là:", "A 22.2° half-angle wedge in an M₁ = 2.5 flow. The (weak) wave angle β is:"), f"{N(math.degrees(b95), 1)}°", [f"{N(22.2, 1)}°", f"{N(math.degrees(math.asin(1 / 2.5)), 1)}°", f"{N(70.0, 1)}°"], L("Giải θ-β-M cho β nhỏ.", "Solve θ-β-M for the smaller β.")),
        Q(6, "Anderson 6th, Problem 9.6", L("Tấm phẳng trong dòng M = 2,4; góc tấn lớn nhất còn sóng bám xấp xỉ:", "A flat plate in an M = 2.4 flow; the largest angle of attack with an attached shock is about:"), f"{N(math.degrees(tm96), 1)}°", [f"{N(math.degrees(tm96) - 8, 1)}°", f"{N(45.0, 1)}°", f"{N(90.0, 1)}°"], L("θ_max(M = 2,4) từ cực đại của hàm θ(β).", "θ_max(M = 2.4) from the maximum of θ(β).")),
        Q(7, "Anderson 6th, Problem 9.15", L("Góc quay lớn nhất mà dòng âm thanh (M = 1) có thể giãn nở bằng sóng Prandtl-Meyer là:", "The maximum angle through which a sonic flow can be expanded by a Prandtl-Meyer wave is:"), f"{N(nu_max, 2)}°", [f"{N(90.0, 2)}°", f"{N(180.0, 2)}°", f"{N(nu_max / 2, 2)}°"], L("ν(∞) = (√6 − 1)·90° = 130,45°.", "ν(∞) = (√6 − 1)·90° = 130.45°.")),
        Q(8, "Anderson 6th, Problem 9.20", L("Dòng M = 3, 1 atm giãn nở 20° rồi nén 20° trở lại phương ngang. Áp suất cuối khác 1 atm vì:", "A Mach 3 flow at 1 atm expands 20° then compresses 20° back to horizontal. The final pressure differs from 1 atm because:"), L("sóng xung kích nén mất áp suất toàn phần", "the compression shock loses total pressure"), [L("sóng giãn nở mất áp suất toàn phần", "the expansion loses total pressure"), L("góc quay hai lần khác nhau", "the two turning angles differ"), L("dòng nén được", "the flow is compressible")], L("Sóng giãn nở thuận nghịch, sóng xung kích thì không.", "The expansion is reversible, the shock is not."), L(f"<p>Sau giãn nở M = {N(M920, 3)}, p = {N(pexp, 3)} atm; sau nén M = {N(o920['M2'], 3)}, p = {N(p920, 3)} atm.</p>", f"<p>After the expansion M = {N(M920, 3)}, p = {N(pexp, 3)} atm; after the compression M = {N(o920['M2'], 3)}, p = {N(p920, 3)} atm.</p>")),
    ]
    gen = [
        Q(11, SUP, L("Góc Mach ở M = 2 là:", "The Mach angle at M = 2 is:"), "30°", ["60°", "45°", "26,4°" if lang == "vi" else "26.4°"], L("μ = arcsin(1/2) = 30°.", "μ = arcsin(1/2) = 30°.")),
        Q(12, SUP, L("Hàm Prandtl-Meyer ν(2,0) xấp xỉ:", "The Prandtl-Meyer function ν(2.0) is approximately:"), f"{N(math.degrees(prandtl_meyer(2.0)), 2)}°", [f"{N(math.degrees(prandtl_meyer(2.0)) * 2, 2)}°", f"{N(30.0, 2)}°", f"{N(0.0, 2)}°"], L("ν(1) = 0 và ν tăng theo M.", "ν(1) = 0 and ν increases with M.")),
        Q(13, SUP, L("Với tấm phẳng M = 2,6, α = 5°, c_l Ackeret = 4α/√(M²−1) xấp xỉ:", "For a flat plate at M = 2.6, α = 5°, the Ackeret c_l = 4α/√(M²−1) is about:"), N(4 * d2r(5) / math.sqrt(2.6 ** 2 - 1), 3), [N(2 * math.pi * d2r(5), 3), N(0.5, 3), N(0.05, 3)], L("2π α dành cho dòng không nén được.", "2π α is for incompressible flow.")),
        Q(14, SUP, L("Sóng giãn nở Prandtl-Meyer so với sóng xung kích về entropi:", "A Prandtl-Meyer expansion compared with a shock in terms of entropy:"), L("giữ entropi không đổi", "keeps the entropy constant"), [L("tăng entropi", "raises the entropy"), L("giảm entropi", "lowers the entropy"), L("tăng entropi nhiều hơn sóng thẳng", "raises entropy more than a normal shock")], L("Sóng giãn nở đẳng entropi.", "The expansion is isentropic.")),
        Q(15, SUP, L("Với M₁ cố định, góc lệch dòng lớn hơn θ_max thì sóng xung kích:", "At fixed M₁, a flow deflection larger than θ_max makes the shock:"), L("tách rời và cong trước vật", "detach and curve ahead of the body"), [L("trở thành sóng Mach", "become a Mach wave"), L("biến mất", "disappear"), L("trở thành sóng giãn nở", "become an expansion")], L("Sóng bám chỉ tồn tại khi θ ≤ θ_max.", "An attached shock exists only for θ ≤ θ_max.")),
        Q(16, SUP, L("Trong hệ nhiều sóng ở M = 4, dùng thêm sóng xiên trước sóng thẳng làm p₀ còn lại:", "In a multi-wave system at M = 4, adding oblique shocks before the normal shock leaves the p₀:"), L("nhiều hơn", "higher"), [L("ít hơn", "lower"), L("bằng nhau", "equal"), L("bằng không", "zero")], L("0,139 → 0,314 → 0,420.", "0.139 → 0.314 → 0.420.")),
    ]
    m["quiz_sets"] = [
        {"key": "anderson", "title": L("Sách 2, Anderson: bài tập cuối chương 9 (đáp án đã tính lại)", "Book 2, Anderson: end-of-chapter 9 problems (answers recomputed)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập thêm (tự soạn, đáp án đã kiểm bằng tính toán)", "Extra practice (written for this site, answers checked by calculation)"), "items": gen},
    ]
    m["problems_intro"] = L("Ba nhóm bài ch.9 của Anderson, giải từng bước và đã so với Solution Manual (bản 4). Các bài 9.1, 9.2, 9.4, 9.6, 9.8 khớp (9.8 lệch dưới 1% vì sách đọc số liệu từ đồ thị); bài 9.13 khớp ở 5° và 15°. Có hai khác biệt cần biết. (a) Bài 9.5 ở bản 4 dùng nêm 22,5° (β = 46°, p₂ = 3,613 atm), còn bản 6 dùng 22,2°, nên kết quả ở đây là 45,89° và 3,592 atm. (b) Ở α = 30°, Solution Manual ghi c_l = 1,19 và c_d,w = 0,687 vì bỏ mất hệ số cos α; giá trị đúng là 1,02 và 0,59.", "Three groups of Anderson ch. 9 problems, solved step by step and compared with the 4th-edition Solution Manual. Problems 9.1, 9.2, 9.4, 9.6 and 9.8 agree (9.8 within 1% because the book reads values from charts); 9.13 agrees at 5° and 15°. There are two differences to know. (a) Problem 9.5 in the 4th edition uses a 22.5° wedge (β = 46°, p₂ = 3.613 atm) while the 6th uses 22.2°, so the results here are 45.89° and 3.592 atm. (b) At α = 30° the Solution Manual prints c_l = 1.19 and c_d,w = 0.687 because it drops the cos α factor; the correct values are 1.02 and 0.59.")
    m["problems"] = [
        {"num": "9.2", "src": "Anderson 6th, Problem 9.2", "q": L("Một sóng xung kích xiên có góc sóng β = 30° trong dòng M₁ = 4, với áp suất và nhiệt độ thượng nguồn p₁ = 2,65×10⁴ N/m², T₁ = 223,3 K. Tính áp suất, nhiệt độ, số Mach, áp suất toàn phần và nhiệt độ toàn phần sau sóng, và độ tăng entropi qua sóng.", "An oblique shock with wave angle β = 30° in an M₁ = 4 flow, with upstream pressure and temperature p₁ = 2.65×10⁴ N/m², T₁ = 223.3 K. Find the pressure, temperature, Mach number, total pressure and total temperature behind the wave, and the entropy increase across it."),
         "ans": L(f"<p>M_n1 = 4 sin 30° = {N(o92['Mn1'], 3)}; sóng thẳng ở M = 2: p₂/p₁ = 4,5, T₂/T₁ = {N(o92['T'], 4)}, p₀,₂/p₀,₁ = {N(o92['p0'], 4)}; θ = {N(math.degrees(o92['theta']), 2)}°.</p><p><b>p₂ = {N(p92, 0)} N/m², T₂ = {N(T92, 1)} K, M₂ = M_n2/sin(β−θ) = {N(o92['M2'], 3)}</b>.</p><p>p₀,₁ = {N(2.65e4 * p0_over_p(4), 0)}; <b>p₀,₂ = {N(p02_92, 0)} N/m²; T₀ = {N(T02_92, 1)} K; Δs = −R ln(p₀,₂/p₀,₁) = {N(ds92, 1)} J/(kg·K)</b>.</p>", f"<p>M_n1 = 4 sin 30° = {N(o92['Mn1'], 3)}; normal shock at M = 2: p₂/p₁ = 4.5, T₂/T₁ = {N(o92['T'], 4)}, p₀,₂/p₀,₁ = {N(o92['p0'], 4)}; θ = {N(math.degrees(o92['theta']), 2)}°.</p><p><b>p₂ = {N(p92, 0)} N/m², T₂ = {N(T92, 1)} K, M₂ = M_n2/sin(β−θ) = {N(o92['M2'], 3)}</b>.</p><p>p₀,₁ = {N(2.65e4 * p0_over_p(4), 0)}; <b>p₀,₂ = {N(p02_92, 0)} N/m²; T₀ = {N(T02_92, 1)} K; Δs = −R ln(p₀,₂/p₀,₁) = {N(ds92, 1)} J/(kg·K)</b>.</p>")},
        {"num": "9.5, 9.8", "src": "Anderson 6th, Problems 9.5, 9.8", "q": L("(9.5) Dòng M₁ = 2,5, p₁ = 1 atm, T₁ = 300 K thổi qua một nêm nửa góc 22,2°. Tìm góc sóng β, p₂, T₂ và M₂. (9.8) So sánh phần p₀ còn lại của ba hệ sóng ở M = 4: một sóng thẳng; sóng xiên 25,3° rồi sóng thẳng; sóng xiên 25,3° và 20° rồi sóng thẳng.", "(9.5) A flow with M₁ = 2.5, p₁ = 1 atm, T₁ = 300 K passes over a 22.2° half-angle wedge. Find the wave angle β, p₂, T₂ and M₂. (9.8) Compare the p₀ retained by three shock systems at M = 4: one normal shock; a 25.3° oblique shock then a normal shock; 25.3° and 20° oblique shocks then a normal shock."),
         "ans": L(f"<p>(9.5) β = <b>{N(math.degrees(b95), 2)}°</b>; p₂ = <b>{N(o95['p'], 2)} atm</b>; T₂ = <b>{N(300 * o95['T'], 0)} K</b>; M₂ = <b>{N(o95['M2'], 3)}</b>.</p><p>(9.8) p₀ giữ lại: (a) {N(p98a, 3)}; (b) {N(p98b, 3)}; (c) {N(p98c, 3)}. Hệ nhiều sóng hiệu quả hơn hẳn.</p>", f"<p>(9.5) β = <b>{N(math.degrees(b95), 2)}°</b>; p₂ = <b>{N(o95['p'], 2)} atm</b>; T₂ = <b>{N(300 * o95['T'], 0)} K</b>; M₂ = <b>{N(o95['M2'], 3)}</b>.</p><p>(9.8) p₀ retained: (a) {N(p98a, 3)}; (b) {N(p98b, 3)}; (c) {N(p98c, 3)}. The multi-wave systems are far more efficient.</p>")},
        {"num": "9.13, 9.20", "src": "Anderson 6th, Problems 9.13, 9.20", "q": L("(9.13) Tấm phẳng mỏng vô hạn ở góc tấn α trong dòng M = 2,6. Tính c_l và c_d,w ở α = 5°, 15° và 30°. (9.20) Dòng M = 3, p = 1 atm giãn nở 20° rồi nén 20° trở lại phương ban đầu. Tìm số Mach và áp suất cuối, và giải thích vì sao áp suất không trở về 1 atm.", "(9.13) An infinitely thin flat plate at angle of attack α in an M = 2.6 flow. Find c_l and c_d,w at α = 5°, 15° and 30°. (9.20) A flow at M = 3, p = 1 atm expands through 20° then is compressed through 20° back to the original direction. Find the final Mach number and pressure, and explain why the pressure does not return to 1 atm."),
         "ans": L("<p>(9.13) " + "; ".join(f"α = {a}°: c_l = <b>{N(fp[a][0], 3)}</b>, c_d,w = <b>{N(fp[a][1], 3)}</b>" for a in (5, 15, 30)) + f".</p><p>(9.20) Giãn nở: M = {N(M920, 3)}, p = {N(pexp, 3)} atm; nén: M = {N(o920['M2'], 3)}, <b>p = {N(p920, 3)} atm</b> (≠ 1 atm do mất p₀ ở sóng nén).</p>", "<p>(9.13) " + "; ".join(f"α = {a}°: c_l = <b>{N(fp[a][0], 3)}</b>, c_d,w = <b>{N(fp[a][1], 3)}</b>" for a in (5, 15, 30)) + f".</p><p>(9.20) Expansion: M = {N(M920, 3)}, p = {N(pexp, 3)} atm; compression: M = {N(o920['M2'], 3)}, <b>p = {N(p920, 3)} atm</b> (≠ 1 atm because of the p₀ loss in the compression shock).</p>")},
    ]
    return m
