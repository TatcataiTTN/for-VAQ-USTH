# -*- coding: utf-8 -*-
"""Viet lai loi giai cac bai cu theo cau truc 4 buoc (De noi gi / Y tuong / Cac buoc / Kiem tra). Moi so tinh tai cho."""
import math
from aero import *
from common import num, sol


def override(slug, lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)
    o = {}
    if slug == "01-atmosphere":
        rho_a = 1.9e4 / (287 * 203); T_b = 1058 / (1.23e-3 * 1716); p11 = 1.01e5 - 1.36e4 * 9.8 * 0.2
        rho1000 = isa(1000)[2]; B = 15000 * rho1000 * 9.8; S = math.pi * 14 ** 2 / 4; q = 0.5 * rho1000 * 900; Lz = q * S * 0.05; W = B + Lz
        o["1.1"] = sol(lang, L("Cho hai trong ba đại lượng p, ρ, T của không khí và hỏi đại lượng còn lại: (a) tìm ρ, (b) tìm T.", "Two of the three air properties p, ρ, T are given and the third is asked: (a) find ρ, (b) find T."),
                       L("Mọi phép tính đều dựa vào phương trình trạng thái p = ρRT; chỉ cần viết lại theo ẩn cần tìm và dùng đúng đơn vị của R.", "Everything rests on the equation of state p = ρRT; rewrite it for the unknown and use the matching units of R."),
                       [L("(a) Đơn vị SI nên R = 287 J/(kg·K): ρ = p/(RT).", "(a) SI units so R = 287 J/(kg·K): ρ = p/(RT)."), L(f"Thay số: ρ = 1,9×10⁴/(287 × 203) = 1,9×10⁴/58 261 = <b>{N(rho_a, 3)} kg/m³</b>.", f"Substituting: ρ = 1.9×10⁴/(287 × 203) = 1.9×10⁴/58 261 = <b>{N(rho_a, 3)} kg/m³</b>."),
                        L("(b) Đơn vị Anh nên R = 1716 ft·lb/(slug·°R): T = p/(ρR).", "(b) English units so R = 1716 ft·lb/(slug·°R): T = p/(ρR)."), L(f"Thay số: T = 1058/(1,23×10⁻³ × 1716) = 1058/2,1107 = <b>{N(T_b, 0)} °R</b>.", f"Substituting: T = 1058/(1.23×10⁻³ × 1716) = 1058/2.1107 = <b>{N(T_b, 0)} °R</b>.")],
                       L("Solution Manual cho 0,326 kg/m³ và 501 °R. Ghi chú: 501 °R ≈ 41 °F ≈ 278 K, hợp lý cho hầm gió; 0,326 kg/m³ bằng khoảng một phần ba mật độ mực biển, hợp lý ở độ cao lớn.", "The Solution Manual gives 0.326 kg/m³ and 501 °R. Sanity check: 501 °R ≈ 41 °F ≈ 278 K is reasonable for a tunnel; 0.326 kg/m³ is about a third of sea-level density, reasonable at altitude."))
        o["1.11"] = sol(lang, L("Áp kế chữ U thủy ngân: một nhánh nối với mô hình, nhánh kia thông khí quyển; hai mực thủy ngân chênh 20 cm và mực cao nằm ở phía mô hình.", "A mercury U-tube manometer: one leg on the model, the other open to the atmosphere; the mercury levels differ by 20 cm with the higher level on the model side."),
                        L("Cột thủy ngân cao hơn bị đẩy lên bởi áp suất thấp hơn. Vậy phía mô hình có áp suất thấp hơn khí quyển một lượng ρ_Hg g h.", "The higher mercury column is the one pushed up by the lower pressure. So the model side is below atmospheric by ρ_Hg g h."),
                        [L("Chọn dấu: mực cao ở phía mô hình ⇒ p_mô hình = p_atm − ρ_Hg g h.", "Choose the sign: higher level on the model side ⇒ p_model = p_atm − ρ_Hg g h."), L(f"ρ_Hg g h = 1,36×10⁴ × 9,8 × 0,2 = {N(1.36e4 * 9.8 * 0.2, 0)} N/m².", f"ρ_Hg g h = 1.36×10⁴ × 9.8 × 0.2 = {N(1.36e4 * 9.8 * 0.2, 0)} N/m²."),
                         L(f"p = 1,01×10⁵ − {N(1.36e4 * 9.8 * 0.2, 0)} = <b>{N(p11, 0)} N/m² ≈ 7,43×10⁴ N/m²</b>.", f"p = 1.01×10⁵ − {N(1.36e4 * 9.8 * 0.2, 0)} = <b>{N(p11, 0)} N/m² ≈ 7.43×10⁴ N/m²</b>.")],
                        L("Solution Manual: 7,43×10⁴ N/m². Nếu cộng thay vì trừ sẽ ra 1,28×10⁵, tức cao hơn khí quyển: ngược với quan sát.", "Solution Manual: 7.43×10⁴ N/m². Adding instead of subtracting would give 1.28×10⁵, above atmospheric: opposite to what is observed."))
        o["1.12"] = sol(lang, L("Khí cầu Zeppelin bay thẳng đều, thể tích 15 000 m³, đường kính lớn nhất 14 m, 30 m/s ở 1000 m chuẩn, C_L = 0,05 tính theo tiết diện ngang. Hỏi trọng lượng.", "A Zeppelin flies straight and level, volume 15 000 m³, maximum diameter 14 m, 30 m/s at a standard 1000 m, C_L = 0.05 based on the cross-section. Find its weight."),
                        L("Bay thẳng đều nên tổng lực nâng cân bằng trọng lượng; lực nâng có hai nguồn: lực đẩy Archimedes B và lực nâng khí động L.", "In level flight the total upward force balances the weight; there are two sources: Archimedes buoyancy B and aerodynamic lift L."),
                        [L(f"Tra mật độ ISA ở 1000 m: ρ = {N(rho1000, 4)} kg/m³.", f"Look up the ISA density at 1000 m: ρ = {N(rho1000, 4)} kg/m³."), L(f"B = ρ V g = {N(rho1000, 4)} × 15 000 × 9,8 = <b>{N(B, 0)} N</b>.", f"B = ρ V g = {N(rho1000, 4)} × 15 000 × 9.8 = <b>{N(B, 0)} N</b>."),
                         L(f"q = ½ρV² = ½ × {N(rho1000, 4)} × 30² = {N(q, 1)} Pa; S = πd²/4 = {N(S, 1)} m².", f"q = ½ρV² = ½ × {N(rho1000, 4)} × 30² = {N(q, 1)} Pa; S = πd²/4 = {N(S, 1)} m²."),
                         L(f"L = q S C_L = {N(q, 1)} × {N(S, 1)} × 0,05 = <b>{N(Lz, 0)} N</b>.", f"L = q S C_L = {N(q, 1)} × {N(S, 1)} × 0.05 = <b>{N(Lz, 0)} N</b>."),
                         L(f"W = B + L = {N(B, 0)} + {N(Lz, 0)} = <b>{N(W, 0)} N ≈ 1,67×10⁵ N</b>.", f"W = B + L = {N(B, 0)} + {N(Lz, 0)} = <b>{N(W, 0)} N ≈ 1.67×10⁵ N</b>.")],
                        L(f"Lực đẩy chiếm {N(B / W * 100, 1)}% trọng lượng. Solution Manual ghi nhầm L = 3487 N ở dòng giữa (đúng 3847 N) nhưng đáp án cuối 1,67×10⁵ N đúng.", f"Buoyancy carries {N(B / W * 100, 1)}% of the weight. The Solution Manual misprints L = 3487 N on the middle line (correct 3847 N) but its final 1.67×10⁵ N is right."))
    if slug == "02-aerodynamics":
        rho = 1.23; dp = 1.36e4 * 9.81 * 0.1; V34 = math.sqrt(2 * dp / (rho * (1 - 1 / 144))); V36 = math.sqrt(2 * 6000 / rho); cp = 1 - (130 / V36) ** 2
        o["3.4 – 3.7"] = sol(lang, L("Ba bài về ống đo vận tốc: (3.4) hầm gió tỉ số diện tích 12 và chênh áp 10 cm Hg; (3.6) ống Pitot đọc 1,07×10⁵ N/m² ở mực biển; (3.7) vận tốc cục bộ 130 m/s trên cánh máy bay của 3.6.", "Three problems on speed measurement: (3.4) a tunnel with area ratio 12 and a 10 cm Hg difference; (3.6) a Pitot tube reading 1.07×10⁵ N/m² at sea level; (3.7) a local velocity of 130 m/s on the wing of the aircraft in 3.6."),
                                L("Bernoulli: p + ½ρV² không đổi dọc đường dòng. Nếu biết hiệu áp thì suy ra vận tốc; hệ số áp suất C_p = 1 − (V/V∞)².", "Bernoulli: p + ½ρV² is constant along a streamline. A known pressure difference gives the velocity; the pressure coefficient is C_p = 1 − (V/V∞)²."),
                                [L(f"(3.4) Δp = ρ_Hg g h = 1,36×10⁴ × 9,81 × 0,1 = {N(dp, 0)} N/m².", f"(3.4) Δp = ρ_Hg g h = 1.36×10⁴ × 9.81 × 0.1 = {N(dp, 0)} N/m²."),
                                 L(f"Kết hợp Bernoulli và liên tục (V₁ = V₂/12): Δp = ½ρV₂²(1 − 1/144) ⇒ V₂ = √[2Δp/(ρ(1 − 1/144))] = <b>{N(V34, 1)} m/s</b>.", f"Combining Bernoulli and continuity (V₁ = V₂/12): Δp = ½ρV₂²(1 − 1/144) ⇒ V₂ = √[2Δp/(ρ(1 − 1/144))] = <b>{N(V34, 1)} m/s</b>."),
                                 L(f"(3.6) Pitot đo p₀: p₀ − p = ½ρV² ⇒ V = √[2(1,07 − 1,01)×10⁵/1,23] = <b>{N(V36, 1)} m/s</b>.", f"(3.6) The Pitot tube reads p₀: p₀ − p = ½ρV² ⇒ V = √[2(1.07 − 1.01)×10⁵/1.23] = <b>{N(V36, 1)} m/s</b>."),
                                 L(f"(3.7) C_p = 1 − (130/{N(V36, 1)})² = <b>{N(cp, 3)}</b>: âm nên áp suất thấp hơn dòng tự do, đúng với vùng hút trên cánh.", f"(3.7) C_p = 1 − (130/{N(V36, 1)})² = <b>{N(cp, 3)}</b>: negative so the pressure is below the free stream, as on the suction region of a wing.")],
                                L("Solution Manual: 147 m/s, 98,8 m/s và −0,73. Ở 3.4, thừa số (1 − 1/144) chỉ đổi kết quả khoảng 0,35%.", "Solution Manual: 147 m/s, 98.8 m/s and −0.73. In 3.4 the factor (1 − 1/144) changes the result by only about 0.35%."))
    if slug == "03-theory-of-flight":
        AR = 32 ** 2 / 170; V = 176.0; q = 0.5 * 0.002377 * V ** 2; CL = 2450 / (q * 170); a0 = 0.1033
        a = a0 / (1 + 57.3 * a0 / (math.pi * AR) * 1.12); al = CL / a - 3; CDi = CL ** 2 / (math.pi * 0.64 * AR); Di = CDi * q * 170
        o["5.4 – 5.5"] = sol(lang, L("Máy bay Piper Cherokee, S = 170 ft², b = 32 ft, W = 2450 lb bay thẳng đều 120 mi/h ở mực biển. Biên dạng a₀ = 0,1033/độ, α_L=0 = −3°, τ = 0,12. Tìm góc tấn hình học, rồi lực cản cảm ứng với e = 0,64.", "A Piper Cherokee, S = 170 ft², b = 32 ft, W = 2450 lb in level flight at 120 mi/h at sea level. The airfoil has a₀ = 0.1033/degree, α_L=0 = −3°, τ = 0.12. Find the geometric angle of attack, then the induced drag with e = 0.64."),
                                L("Bay thẳng đều ⇒ L = W, từ đó suy C_L. Biết C_L thì suy góc tấn qua độ dốc lực nâng của cánh hữu hạn (không phải của biên dạng), và suy C_D,i qua C_L²/(πeAR).", "Level flight ⇒ L = W, which gives C_L. Knowing C_L gives the angle of attack through the finite-wing lift slope (not the airfoil's) and C_D,i through C_L²/(π e AR)."),
                                [L(f"AR = b²/S = 32²/170 = {N(AR, 3)}; V = 120 mi/h = 176 ft/s; q = ½ × 0,002377 × 176² = {N(q, 2)} lb/ft².", f"AR = b²/S = 32²/170 = {N(AR, 3)}; V = 120 mi/h = 176 ft/s; q = ½ × 0.002377 × 176² = {N(q, 2)} lb/ft²."),
                                 L(f"L = W ⇒ C_L = W/(qS) = 2450/({N(q, 2)} × 170) = <b>{N(CL, 4)}</b>.", f"L = W ⇒ C_L = W/(qS) = 2450/({N(q, 2)} × 170) = <b>{N(CL, 4)}</b>."),
                                 L(f"Độ dốc cánh hữu hạn: a = a₀/[1 + 57,3a₀(1 + τ)/(πAR)] = {N(a, 4)}/độ.", f"Finite-wing slope: a = a₀/[1 + 57.3a₀(1 + τ)/(πAR)] = {N(a, 4)}/degree."),
                                 L(f"α = C_L/a + α_L=0 = {N(CL / a, 3)} − 3 = <b>{N(al, 2)}°</b>.", f"α = C_L/a + α_L=0 = {N(CL / a, 3)} − 3 = <b>{N(al, 2)}°</b>."),
                                 L(f"C_D,i = C_L²/(π e AR) = {N(CL, 4)}²/(π × 0,64 × {N(AR, 3)}) = {N(CDi, 5)}; D_i = C_D,i q S = <b>{N(Di, 1)} lb</b>.", f"C_D,i = C_L²/(π e AR) = {N(CL, 4)}²/(π × 0.64 × {N(AR, 3)}) = {N(CDi, 5)}; D_i = C_D,i q S = <b>{N(Di, 1)} lb</b>.")],
                                L(f"Nếu dùng a₀ thay a, góc tấn ra {N(CL / a0 - 3, 2)}°: sai vì cánh hữu hạn có độ dốc nhỏ hơn biên dạng. Lực cản cảm ứng {N(Di, 0)} lb là phần nhỏ so với trọng lượng 2450 lb.", f"Using a₀ instead of a gives {N(CL / a0 - 3, 2)}°: wrong because a finite wing has a smaller slope than its airfoil. The induced drag of {N(Di, 0)} lb is small against the 2450 lb weight."))
    return o
