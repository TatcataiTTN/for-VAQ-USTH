# -*- coding: utf-8 -*-
"""Hinh EASA cat tu trang, demo tuong tac, cau hoi luyen tap bo sung. Moi dap an so tinh bang aero.py."""
import math
from aero import *
from common import num, mcq, ul

F = "assets/figures/"

def figure_slides(slug, lang):
    """-> {part_index: [slide dict,...]} (slide co 'img', 'cap')."""
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)
    out = {}
    cap = lambda fig, page: L(f"Hình {fig} của EASA Module 08 (tr. {page}), cắt từ bản scan; bấm để xem cỡ gốc", f"Figure {fig} of EASA Module 08 (p. {page}), cropped from the scan; click for full size")
    if slug == "01-atmosphere":
        out[1] = [{"title": L("Hình gốc: áp suất giảm theo độ cao", "Original figure: pressure falls with altitude"), "img": "fig_1-4.jpg", "cap": cap("1-4", "1.4"),
                   "body": ul(L(f"Đường cong giảm nhanh rồi thoải dần; ở 40 000 ft đồ thị chỉ 2,72 psi, đúng bằng công thức ISA ({N(isa_ft(40000)[1] / PSI, 2)} psi)", f"The curve falls steeply then flattens; at 40 000 ft the chart shows 2.72 psi, equal to the ISA formula ({N(isa_ft(40000)[1] / PSI, 2)} psi)"))}]
        out[4] = [{"title": L("Hình gốc: bảng ISA của EASA", "Original figure: the EASA ISA table"), "img": "fig_1-7.jpg", "cap": cap("1-7", "1.6"),
                   "body": ul(L("Đối chiếu với bảng tính lại ở slide trước: cùng nhiệt độ, áp suất và mật độ tới làm tròn", "Compare with the recomputed table on the previous slide: same temperature, pressure and density to rounding"), L("Lưu ý bảng EASA ghi mật độ 0,3 kg/m³ ở 40 000 ft, bản tính cho 0,3016", "Note the EASA table gives 0.3 kg/m³ at 40 000 ft, the computation gives 0.3016"))}]
    elif slug == "02-aerodynamics":
        out[4] = [{"title": L("Hình gốc: C_L, C_D và L/D theo góc tấn", "Original figure: C_L, C_D and L/D against angle of attack"), "img": "fig_2-15.jpg", "cap": cap("2-15", "2.11"),
                   "body": ul(L("C_L tăng gần tuyến tính theo góc tấn rồi đạt cực đại C_Lmax và giảm: thất tốc", "C_L rises almost linearly with angle of attack, peaks at C_Lmax and falls: the stall"), L("Tỉ số L/D đạt cực đại ở góc tấn nhỏ hơn nhiều so với C_Lmax", "L/D peaks at a much smaller angle of attack than C_Lmax"), L("Lực cản C_D tăng nhanh gần thất tốc vì lực cản cảm ứng", "C_D rises sharply near the stall because of induced drag"))}]
    elif slug == "03-theory-of-flight":
        out[1] = [{"title": L("Hình gốc: tốc độ thất tốc tăng theo góc nghiêng", "Original figure: stall speed rises with bank angle"), "img": "fig_3-8.jpg", "cap": cap("3-8", "3.9"),
                   "body": ul(L(f"Đối chiếu bảng tính ở slide trước: ở 60° hệ số tải là 2 g và tốc độ thất tốc tăng {N((math.sqrt(2) - 1) * 100, 0)}%, đúng với đường cong trên hình", f"Compare with the table on the earlier slide: at 60° the load factor is 2 g and the stall speed rises {N((math.sqrt(2) - 1) * 100, 0)}%, matching the curve"), L("Trên 60° cả hai đường dốc lên rất nhanh", "Beyond 60° both curves climb very steeply"))}]
        out[3] = [{"title": L("Hình gốc: sóng xung kích quanh biên dạng", "Original figure: shock waves around an airfoil"), "img": "fig_3-11.jpg", "cap": cap("3-11", "3.13"),
                   "body": ul(L("Ở M = 0,82 đã có sóng xung kích thẳng trên mặt cánh dù máy bay cận âm", "At M = 0.82 there is already a normal shock on the wing surface although the aircraft is subsonic"), L("Ở M = 1,05 xuất hiện sóng đầu (bow wave) phía trước", "At M = 1.05 a bow wave forms ahead of the airfoil"))},
                  {"title": L("Hình gốc: hiệu ứng cánh xuôi sau", "Original figure: the sweepback effect"), "img": "fig_3-12.jpg", "cap": cap("3-12", "3.14"),
                   "body": ul(L(f"Tốc độ thực M 0,85 nhưng thành phần vuông góc mép trước chỉ là M 0,70; với M_n = M cos Λ thì Λ = {N(math.degrees(math.acos(0.70 / 0.85)), 1)}° (suy ra từ hai số trên hình, không phải số liệu in)", f"True speed M 0.85 but the component normal to the leading edge is only M 0.70; with M_n = M cos Λ this means Λ = {N(math.degrees(math.acos(0.70 / 0.85)), 1)}° (inferred from the two numbers on the figure, not printed data)"), L("Dòng chảy dọc sải (spanwise flow) là nguyên nhân thất tốc đầu cánh của cánh xuôi", "Spanwise flow is the cause of tip stall on swept wings"))}]
        out[4] = [{"title": L("Hình gốc: bốn kiểu cánh tà", "Original figure: four types of flap"), "img": "fig_3-15.jpg", "cap": cap("3-15", "3.16"),
                   "body": ul(L("Từ trên xuống: tiết diện cơ bản, plain, split, slotted, Fowler và slotted Fowler", "Top to bottom: basic section, plain, split, slotted, Fowler and slotted Fowler"), L("Khe trên cánh tà có khe dẫn khí năng lượng cao từ mặt dưới lên mặt trên, trì hoãn tách dòng", "The slot in a slotted flap leads high-energy air from the lower to the upper surface, delaying separation"))}]
    elif slug == "04-stability":
        out[1] = [{"title": L("Hình gốc: dao động tắt dần, không tắt và phân kỳ", "Original figure: damped, undamped and divergent oscillations"), "img": "fig_4-3.jpg", "cap": cap("4-3", "4.4"),
                   "body": ul(L("Cùng ổn định tĩnh dương nhưng ba kiểu đáp ứng theo thời gian khác nhau: tắt dần, trung tính và phân kỳ", "The same positive static stability with three different time responses: damped, neutral and divergent"))}]
        out[2] = [{"title": L("Hình gốc: đòn bẩy CG-CL-T", "Original figure: the CG-CL-T lever"), "img": "fig_4-4.jpg", "cap": cap("4-4", "4.5"),
                   "body": ul(L("Lực nâng lên tại CL, trọng lượng xuống tại CG, lực đè nhỏ xuống tại đuôi T giữ thăng bằng", "Lift up at CL, weight down at CG and a small download at the tail T hold the balance"))},
                  {"title": L("Hình gốc: tốc độ và downwash trên đuôi", "Original figure: speed and tail downwash"), "img": "fig_4-5.jpg", "cap": cap("4-5", "4.5"),
                   "body": ul(L("Tốc độ cao thì downwash lớn, lực đè đuôi lớn; tốc độ thấp thì lực đè nhỏ và mũi chúi xuống", "At high speed the downwash and tail download are large; at low speed they are small and the nose drops"))}]
    return out


def demo_html(slug, lang):
    L = lambda vi, en: vi if lang == "vi" else en
    def box(title, text, cls):
        return f"<div class='demo-box'><h3>🧪 {title}</h3><p>{text}</p><div class='{cls}'></div></div>"
    if slug == "01-atmosphere":
        return box(L("Demo: máy tính khí quyển chuẩn ISA", "Demo: ISA atmosphere calculator"),
                   L("Kéo độ cao và độ lệch nhiệt độ so với ISA để xem T, p, ρ, tốc độ âm thanh và độ cao mật độ. Mặc định 5 000 ft, ΔT = 0.", "Drag the altitude and the temperature deviation from ISA to see T, p, ρ, the speed of sound and the density altitude. Default 5 000 ft, ΔT = 0."), "demo-isa")
    if slug == "02-aerodynamics":
        return box(L("Demo: lực nâng của một cánh (NACA 2412)", "Demo: lift of a wing (NACA 2412)"),
                   L("Chọn độ cao, tốc độ, diện tích, góc tấn và khối lượng; trang tính q, C_L, lực nâng và C_L cần để bay thẳng đều.", "Choose altitude, speed, area, angle of attack and mass; the page computes q, C_L, lift and the C_L needed for level flight."), "demo-lift")
    if slug == "03-theory-of-flight":
        return (box(L("Demo: vòng bay thăng bằng, hệ số tải và thất tốc", "Demo: level turn, load factor and stall"), L("Kéo góc nghiêng để xem n = 1/cos φ và tốc độ thất tốc tăng bao nhiêu.", "Drag the bank angle to see n = 1/cos φ and how much the stall speed rises."), "demo-turn") +
                box(L("Demo: số Mach, tốc độ âm thanh và sóng xung kích thẳng", "Demo: Mach number, speed of sound and the normal shock"), L("Chọn độ cao và M₁ để tính tốc độ thực và các tỉ số qua sóng xung kích thẳng. Mặc định là bài Anderson 8.7 (M₁ = 2,6).", "Choose altitude and M₁ to get true airspeed and the normal-shock ratios. The default is Anderson problem 8.7 (M₁ = 2.6)."), "demo-shock"))
    if slug == "04-stability":
        return (box(L("Demo: vị trí CG, lề ổn định và độ cứng chúc ngóc", "Demo: CG position, static margin and pitch stiffness"), L("Kéo CG ra phía sau và quan sát C_mα đổi dấu khi CG vượt điểm trung hòa.", "Drag the CG aft and watch C_mα change sign when the CG passes the neutral point."), "demo-stab") +
                box(L("Demo: phugoid và chu kỳ ngắn của B747", "Demo: B747 phugoid and short period"), L("Mô phỏng đáp ứng với ma trận A in trong Etkin. Chọn nhiễu tốc độ để thấy phugoid (T ≈ 93 s) hoặc nhiễu tốc độ chúc ngóc để thấy chu kỳ ngắn (T ≈ 7 s).", "Simulates the response with the A matrix printed in Etkin. Choose a speed disturbance to see the phugoid (T ≈ 93 s) or a pitch-rate disturbance to see the short period (T ≈ 7 s)."), "demo-modes"))
    return ""


def extra_quiz(slug, lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)
    SUP = L("Bổ sung (biên soạn)", "Supplementary (authored)")
    sd = {"01-atmosphere": 120, "02-aerodynamics": 220, "03-theory-of-flight": 320, "04-stability": 420}[slug]
    I = []
    if slug == "01-atmosphere":
        r10 = isa_ft(10000)[2]; p20 = isa_ft(20000)[1] / 100; T10 = isa_ft(10000)[0] - 273.15
        rdev = 101325 / (R_AIR * (15 + 288.15)); lo, hi = 0.0, 15000.0
        for _ in range(80):
            mid = (lo + hi) / 2
            if isa(mid)[2] > rdev: lo = mid
            else: hi = mid
        da = lo / FT
        I = [
            mcq(sd + 1, SUP, L("Mật độ ISA ở 10 000 ft xấp xỉ:", "ISA density at 10 000 ft is approximately:"), f"{N(r10, 3)} kg/m³", [f"{N(RHO0, 3)} kg/m³", f"{N(r10 / 2, 3)} kg/m³", f"{N(r10 * 1.5, 3)} kg/m³"], L("EASA Hình 1-7 ghi 0,9; tính được 0,905.", "EASA Figure 1-7 gives 0.9; the computation gives 0.905.")),
            mcq(sd + 2, SUP, L("Áp suất ISA ở 20 000 ft theo hPa xấp xỉ:", "ISA pressure at 20 000 ft in hPa is approximately:"), N(p20, 0), [N(p20 * 1.5, 0), N(p20 / 2, 0), N(1013, 0)], L("EASA ghi 465,4 hPa; tính được 465,6 hPa.", "EASA gives 465.4 hPa; the computation gives 465.6 hPa.")),
            mcq(sd + 3, SUP, L("Nhiệt độ ISA ở 10 000 ft xấp xỉ:", "ISA temperature at 10 000 ft is approximately:"), f"{N(T10, 1)} °C", [f"{N(T10 + 15, 1)} °C", "15 °C", f"{N(T10 - 20, 1)} °C"], L("15 − 2 × 10 = −5 °C theo quy tắc −2 °C/1000 ft; EASA ghi −4,8 °C.", "15 − 2 × 10 = −5 °C by the −2 °C per 1000 ft rule; EASA gives −4.8 °C.")),
            mcq(sd + 4, SUP, L("Trong tầng nào nhiệt độ tăng theo độ cao (ngoài ISA đẳng nhiệt)?", "In which layer does temperature increase with altitude (outside the isothermal ISA model)?"), L("Tầng bình lưu", "The stratosphere"), [L("Tầng đối lưu", "The troposphere"), L("Chỉ ở tropopause", "Only at the tropopause"), L("Không tầng nào", "None")], L("Ôzôn hấp thụ tia cực tím làm không khí ấm lên (EASA tr. 1.5).", "Ozone absorbs ultraviolet and warms the air (EASA p. 1.5).")),
            mcq(sd + 5, SUP, L("Ở mực biển, nhiệt độ cao hơn ISA 15 °C (30 °C). Độ cao mật độ xấp xỉ:", "At sea level the temperature is 15 °C above ISA (30 °C). The density altitude is approximately:"), f"{N(da, 0)} ft", [f"{N(da / 3, 0)} ft", "0 ft", f"{N(da * 2, 0)} ft"], L("Mật độ thật thấp hơn ISA nên máy bay hoạt động như ở độ cao cao hơn.", "The real density is below ISA so the aircraft behaves as if higher.")),
            mcq(sd + 6, SUP, L("Theo EASA, tầng đối lưu ở xích đạo mở rộng tới khoảng:", "According to EASA the troposphere at the equator extends to about:"), L("60 000 ft", "60 000 ft"), ["25 000 ft", "38 000 ft", "100 000 ft"], L("Ở hai cực chỉ 25 000 đến 30 000 ft, trung bình khoảng 38 000 ft.", "Over the poles only 25 000–30 000 ft, on average about 38 000 ft.")),
        ]
    elif slug == "02-aerodynamics":
        q100 = 0.5 * RHO0 * 100 ** 2; L1 = 0.5 * RHO0 * 60 ** 2 * 20 * 0.5; cdi = 0.8 ** 2 / (math.pi * 0.9 * 8); Re = RHO0 * 50 * 2 / 1.789e-5; r3 = isa(3000)[2] / RHO0
        I = [
            mcq(sd + 1, SUP, L("Áp suất động q ở 100 m/s tại mực biển ISA (ρ = 1,225) là:", "The dynamic pressure q at 100 m/s at ISA sea level (ρ = 1.225) is:"), f"{N(q100, 0)} Pa", [f"{N(q100 * 2, 0)} Pa", f"{N(q100 / 2, 0)} Pa", f"{N(100 * 1.225, 0)} Pa"], L("q = ½ρV² = 0,5 × 1,225 × 10 000.", "q = ½ρV² = 0.5 × 1.225 × 10 000.")),
            mcq(sd + 2, SUP, L("Cánh S = 20 m², V = 60 m/s, C_L = 0,5 ở mực biển ISA tạo lực nâng:", "A wing with S = 20 m², V = 60 m/s and C_L = 0.5 at ISA sea level produces a lift of:"), f"{N(L1, 0)} N", [f"{N(L1 * 2, 0)} N", f"{N(L1 / 2, 0)} N", f"{N(L1 * 3.6, 0)} N"], L("L = ½ρV²·S·C_L.", "L = ½ρV²·S·C_L.")),
            mcq(sd + 3, SUP, L("Cánh AR = 8, e = 0,9, C_L = 0,8 có C_Di bằng:", "A wing with AR = 8, e = 0.9 and C_L = 0.8 has C_Di equal to:"), N(cdi, 4), [N(cdi * 2, 4), N(cdi / 2, 4), N(0.8 / (math.pi * 8), 4) if abs(0.8 / (math.pi * 8) - cdi) > 1e-4 else N(0.05, 4)], L("C_Di = C_L²/(π e AR).", "C_Di = C_L²/(π e AR).")),
            mcq(sd + 4, SUP, L("Tăng gấp đôi diện tích cánh, giữ nguyên tốc độ, mật độ và C_L thì lực nâng:", "Doubling the wing area while keeping speed, density and C_L, the lift:"), L("tăng gấp đôi", "doubles"), [L("tăng gấp bốn", "quadruples"), L("không đổi", "stays the same"), L("giảm một nửa", "halves")], L("L tỉ lệ thuận với S.", "L is proportional to S.")),
            mcq(sd + 5, SUP, L("Số Reynolds Re = ρVc/μ với ρ = 1,225, V = 50 m/s, c = 2 m, μ = 1,789×10⁻⁵ kg/(m·s) xấp xỉ:", "The Reynolds number Re = ρVc/μ with ρ = 1.225, V = 50 m/s, c = 2 m, μ = 1.789×10⁻⁵ kg/(m·s) is approximately:"), f"{N(Re / 1e6, 2)}×10⁶", [f"{N(Re / 1e5, 2)}×10⁵", f"{N(Re / 1e6 * 10, 1)}×10⁶", f"{N(Re / 1e7, 2)}×10⁶"], L("Re lớn nghĩa là lớp biên giới dễ chuyển sang rối.", "A large Re means the boundary layer readily turns turbulent.")),
            mcq(sd + 6, SUP, L("Với cùng V, S và C_L, lực nâng ở độ cao chuẩn 3 km bằng bao nhiêu phần lực nâng ở mực biển?", "With the same V, S and C_L, what fraction of the sea-level lift is produced at a standard 3 km altitude?"), N(r3, 2), [N(1 / r3, 2), N(r3 ** 2, 2), N(0.5, 2)], L("L tỉ lệ thuận với ρ; σ(3 km) = 0,9093/1,225.", "L is proportional to ρ; σ(3 km) = 0.9093/1.225.")),
        ]
    elif slug == "03-theory-of-flight":
        n45 = 1 / math.cos(math.radians(45)); a20 = soundSpeed(isa_ft(20000)[0]) if False else speed_of_sound(isa_ft(20000)[0]); M2, p2, _, _ = normal_shock(2.0); phi = math.degrees(math.acos(1 / 2.5))
        I = [
            mcq(sd + 1, SUP, L("Bay vòng thăng bằng nghiêng 45°: tốc độ thất tốc tăng khoảng:", "In a 45° bank level turn the stall speed rises by about:"), f"{N((math.sqrt(n45) - 1) * 100, 0)}%", [f"{N((n45 - 1) * 100, 0)}%", "0%", "100%"], L("V_s,turn = V_s√n, n = 1,414, √n = 1,189.", "V_s,turn = V_s√n, n = 1.414, √n = 1.189.")),
            mcq(sd + 2, SUP, L("Tốc độ âm thanh ở 20 000 ft ISA xấp xỉ:", "The speed of sound at 20 000 ft ISA is approximately:"), f"{N(a20 / KT_, 0)} kt" if False else f"{N(a20 / 0.514444, 0)} kt", [f"{N(a20 / 0.514444 * 1.08, 0)} kt", "661 kt", f"{N(574, 0)} kt"], L("T = 248,5 K nên a = 316 m/s; nằm giữa 661 kt (mực biển) và 574 kt (40 000 ft).", "T = 248.5 K so a = 316 m/s; between 661 kt (sea level) and 574 kt (40 000 ft).")),
            mcq(sd + 3, SUP, L("Sóng xung kích thẳng ở M₁ = 2: M₂ và p₂/p₁ là:", "A normal shock at M₁ = 2: M₂ and p₂/p₁ are:"), f"{N(M2, 3)} ; {N(p2, 2)}", [f"{N(1 / 2, 3)} ; {N(2.0, 2)}", f"{N(M2, 3)} ; {N(p2 / 2, 2)}", f"{N(1.2, 3)} ; {N(p2, 2)}"], L("M₂ = √[(γ−1)M₁²+2]/[2γM₁²−(γ−1)] = 0,5774.", "M₂ = √[(γ−1)M₁²+2]/[2γM₁²−(γ−1)] = 0.5774.")),
            mcq(sd + 4, SUP, L("Một máy bay có L/D = 15 tắt động cơ ở độ cao 2 000 ft trên đất bằng, không gió. Quãng đường lướt tối đa là:", "An aircraft with L/D = 15 loses power at 2 000 ft above level ground in still air. The maximum glide distance is:"), "30 000 ft", ["13 333 ft", "2 000 ft", "300 000 ft"], L("Quãng đường = độ cao × tỉ số lướt = 2 000 × 15.", "Distance = height × glide ratio = 2 000 × 15.")),
            mcq(sd + 5, SUP, L("Hệ số tải 3 g nghĩa là:", "A load factor of 3 g means:"), L("tổng tải lên kết cấu bằng 3 lần trọng lượng", "the total load on the structure is three times the weight"), [L("máy bay nặng gấp 3", "the aircraft weighs three times as much"), L("tốc độ gấp 3", "the speed is three times as high"), L("lực cản gấp 3", "the drag is three times as high")], L("EASA tr. 3.9.", "EASA p. 3.9.")),
            mcq(sd + 6, SUP, L("Cần hệ số tải n = 2,5 trong vòng bay thăng bằng thì góc nghiêng là:", "A level turn with n = 2.5 requires a bank angle of:"), f"{N(phi, 1)}°", [f"{N(phi - 15, 1)}°", f"{N(math.degrees(math.acos(0.5)), 1)}°", f"{N(phi + 10, 1)}°"], L("cos φ = 1/n = 0,4.", "cos φ = 1/n = 0.4.")),
        ]
    elif slug == "04-stability":
        Tl = math.pi * math.sqrt(2) * 200 / G0; z = 0.1 / math.sqrt(0.1 ** 2 + 1); th = math.log(2) / 0.05
        I = [
            mcq(sd + 1, SUP, L("Xấp xỉ Lanchester cho máy bay bay 200 m/s: chu kỳ phugoid xấp xỉ:", "In the Lanchester approximation an aircraft flying at 200 m/s has a phugoid period of about:"), f"{N(Tl, 1)} s", [f"{N(Tl * 2, 1)} s", f"{N(Tl / 2, 1)} s", f"{N(2 * math.pi * 200 / G0, 1)} s"], L("T = π√2·V/g.", "T = π√2·V/g.")),
            mcq(sd + 2, SUP, L("Trị riêng λ = −0,1 ± 1,0i có hệ số tắt dần ζ xấp xỉ:", "An eigenvalue λ = −0.1 ± 1.0i has a damping ratio ζ of about:"), N(z, 3), [N(0.1, 3), N(1.0, 3), N(0.5, 3)], L("ζ = −σ/|λ| = 0,1/√1,01.", "ζ = −σ/|λ| = 0.1/√1.01.")),
            mcq(sd + 3, SUP, L("Một mode có phần thực σ dương thì:", "A mode whose real part σ is positive is:"), L("không ổn định: biên độ tăng theo e^{σt}", "unstable: the amplitude grows like e^{σt}"), [L("ổn định và tắt dần", "stable and decaying"), L("trung tính", "neutral"), L("chỉ không ổn định nếu ω = 0", "unstable only if ω = 0")], L("Nghiệm có phần thực dương làm phân kỳ.", "A root with a positive real part diverges.")),
            mcq(sd + 4, SUP, L("Thời gian giảm một nửa biên độ khi σ = −0,05 1/s là:", "The time to half amplitude when σ = −0.05 1/s is:"), f"{N(th, 1)} s", [f"{N(1 / 0.05, 1)} s", f"{N(th * 2, 1)} s", f"{N(th / 2, 1)} s"], L("t½ = ln 2/|σ|.", "t½ = ln 2/|σ|.")),
            mcq(sd + 5, SUP, L("Bộ giảm xoay (yaw damper) chủ yếu dùng để tăng tắt dần cho:", "A yaw damper is mainly used to add damping to:"), L("Dutch roll", "the Dutch roll"), [L("phugoid", "the phugoid"), L("chu kỳ ngắn dọc", "the longitudinal short period"), L("hạ cánh", "landing")], L("Etkin 8.7: yaw damper cho máy bay cánh xuôi.", "Etkin 8.7: the yaw damper on swept-wing aircraft.")),
            mcq(sd + 6, SUP, L("Theo Etkin 2.3, CG càng lùi về phía điểm trung hòa thì lề ổn định tĩnh K_n:", "According to Etkin 2.3, the closer the CG moves to the neutral point the static margin K_n:"), L("càng nhỏ", "becomes smaller"), [L("càng lớn", "becomes larger"), L("không đổi", "stays unchanged"), L("đổi dấu ngay lập tức", "changes sign immediately")], L("K_n = h_n − h giảm dần về 0.", "K_n = h_n − h shrinks to zero.")),
        ]
    return I
