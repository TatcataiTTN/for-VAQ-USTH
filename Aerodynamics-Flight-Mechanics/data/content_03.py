# -*- coding: utf-8 -*-
"""Module 03: Ly thuyet bay. Nguon: EASA M08 Sub-module 03 (tr.3.1-3.20), Anderson 6th ch.5 (5.3-5.4), ch.8 (8.1-8.7, 8.11), ch.11 (11.4-11.6),
Etkin & Reid 3rd ch.3 (muc 3.1, 3.3). Moi con so tinh trong module nay."""
import math
from aero import *
from common import num, ul, table, mcq


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    # ---- tinh toan ----
    AR54 = 32 ** 2 / 170
    V54 = 120 * 5280 / 3600
    q54 = 0.5 * 0.002377 * V54 ** 2
    CL54 = 2450 / (q54 * 170)
    a0 = 0.1033
    a54 = a0 / (1 + 57.3 * a0 / (math.pi * AR54) * (1 + 0.12))
    alpha54 = CL54 / a54 + (-3.0)
    CDi55 = CL54 ** 2 / (math.pi * 0.64 * AR54)
    Di55 = CDi55 * q54 * 170
    a81 = speed_of_sound(230, 287)
    M811 = mach_from_pitot_ratio(1.555)
    V811 = M811 * speed_of_sound(288, 287)
    M2_87, p_87, rho_87, T_87 = normal_shock(2.6)
    Mcr114 = mcr_prandtl_glauert(-0.41)
    a_sl_kt = speed_of_sound(T0) / 0.514444
    a_40_kt = speed_of_sound(isa_ft(40000)[0]) / 0.514444
    n_rows = []
    for phi in (0, 30, 45, 60, 70):
        n = 1 / math.cos(math.radians(phi))
        n_rows.append((f"{phi}°", N(n, 2), N(math.sqrt(n), 2), f"{N((math.sqrt(n) - 1) * 100, 0)}%"))

    m = {"num": "03", "slug": "03-theory-of-flight", "tag": L("Lý thuyết bay", "Theory of Flight")}
    m["title"] = L("Lý thuyết bay: bốn lực, hệ số tải, thất tốc, dòng tốc độ cao và thiết bị tăng lực nâng", "Theory of Flight: the four forces, load factor, stall, high-speed flow and lift augmentation")
    m["src"] = L("EASA Module 08, Sub-module 03 (tr. 3.1–3.20) · Anderson ch.5, 8, 11 · Etkin &amp; Reid ch.3 mục 3.1 và 3.3",
                 "EASA Module 08, Sub-module 03 (pp. 3.1–3.20) · Anderson ch. 5, 8, 11 · Etkin &amp; Reid ch. 3 sec. 3.1 and 3.3")
    m["intro"] = L("Module này dùng các hệ số khí động của module 02 để mô tả một chuyến bay thật. Trước hết là cân bằng bốn lực, tỉ số lướt và đường cực; sau đó là hệ số tải và thất tốc khi bay vòng; rồi đến dòng tốc độ cao với số Mach, sóng xung kích và cánh xuôi sau. Phần cuối nói về các thiết bị tăng lực nâng (cánh tà, thiết bị mép trước, tấm xoáy) mà kỹ thuật viên bảo dưỡng gặp hằng ngày. Bài tập lấy từ Anderson ch.5, 8, 11.",
                   "This module uses the aerodynamic coefficients of module 02 to describe a real flight. First the balance of the four forces, glide ratio and the polar; then load factor and the stall in turns; then high-speed flow with Mach number, shock waves and sweepback. The last part covers the lift-augmentation devices (flaps, leading-edge devices, vortex generators) that a maintenance technician meets every day. The problems come from Anderson ch. 5, 8 and 11.")
    m["mapping"] = {
        "easa": L("Sub-module 03 Theory of Flight (tr. 3.1–3.20): cân bằng lực, tỉ số lướt, đường cực, lực trong vòng bay, thất tốc, hệ số tải, dòng tốc độ cao, số Mach, sóng xung kích, cánh xuôi, tăng lực nâng, thiết bị cố định; 8 câu hỏi cuối chương (Q3-1 đến Q3-8)",
                  "Sub-module 03 Theory of Flight (pp. 3.1–3.20): force balance, glide ratio, polar curve, forces in turns, stalls, load factors, high-speed flight, Mach number, shock waves, sweepback, lift augmentation, fixed devices; 8 end-of-chapter questions (Q3-1 to Q3-8)"),
        "anderson": L("Ch.5 mục 5.1–5.3 (lực cản cảm ứng, đường cong lực nâng cánh hữu hạn); ch.8 mục 8.1–8.7 (vận tốc âm thanh, sóng xung kích thẳng, đo vận tốc bằng ống Pitot nén được); ch.11 mục 11.4–11.6 (quy tắc Prandtl-Glauert, số Mach tới hạn); Bài 5.4, 5.5, 8.1, 8.7, 8.11, 11.4",
                      "Ch.5 sec. 5.1–5.3 (induced drag, finite-wing lift curve); ch.8 sec. 8.1–8.7 (speed of sound, normal shocks, compressible Pitot measurement); ch.11 sec. 11.4–11.6 (Prandtl-Glauert rule, critical Mach number); Problems 5.4, 5.5, 8.1, 8.7, 8.11, 11.4"),
        "etkin": L("Ch.3 mục 3.1 Maneuverability (độ lệch bánh lái độ cao trên mỗi g, tr. 60–63) và mục 3.3 Influence of High-Lift Devices on Trim and Pitch Stiffness (tr. 64–66); Bài tập 3.14 thiên về ổn định nên thuộc sub-module 04",
                   "Ch.3 sec. 3.1 Maneuverability (elevator angle per g, pp. 60–63) and sec. 3.3 Influence of High-Lift Devices on Trim and Pitch Stiffness (pp. 64–66); the ch. 3 exercises focus on stability and belong to sub-module 04"),
        "note": L("EASA đủ cho phần định tính và vài công thức. Anderson có phần sóng xung kích và dòng nén được. Etkin cho thấy hệ số tải g và cánh tà ảnh hưởng thế nào đến cân bằng và ổn định; phần này sẽ dùng nhiều hơn ở module 04.",
                  "EASA covers the qualitative part and a few formulas. Anderson has the shocks and compressible flow. Etkin shows how load factor g and flaps affect trim and stability; that part is used more in module 04."),
    }

    parts = []
    parts.append({"title": L("Bốn lực và bay ổn định", "The four forces and steady flight"),
                  "bullets": [L("Lực nâng cân bằng trọng lượng, lực đẩy cân bằng lực cản ở bay thẳng đều", "Lift balances weight and thrust balances drag in steady level flight"),
                              L("Tỉ số lướt là quãng đường đi được trên độ cao mất đi khi tắt động cơ", "Glide ratio is the distance travelled per unit of height lost with the engine off"),
                              L("Đường cực cho thấy mối liên hệ giữa C_L và C_D", "The polar curve shows how C_L and C_D are related")],
                  "slides": [
                      {"title": L("Cân bằng lực: L = W, T = D", "Force balance: L = W, T = D"),
                       "body": ul(L("Lực nâng (lift) vuông góc với gió tương đối và hướng lên (EASA Q3-1)", "Lift acts perpendicular to the relative wind and upwards (EASA Q3-1)"),
                                  L("Để thắng lực cản (drag) và đưa máy bay tiến lên cần có lực đẩy (EASA Q3-2)", "To overcome drag and move the aircraft forward, thrust is needed (EASA Q3-2)"),
                                  L("Bay thẳng đều: L = W và T = D; mất cân bằng thì máy bay lên, xuống hoặc tăng, giảm tốc", "Steady level flight: L = W and T = D; any imbalance makes the aircraft climb, descend, accelerate or decelerate"),
                                  L(f"Cánh Piper Cherokee (Anderson 5.4): W = 2450 lb, S = 170 ft², 120 mi/h ở mực biển cần C_L = {N(CL54, 3)}", f"Piper Cherokee wing (Anderson 5.4): W = 2450 lb, S = 170 ft², 120 mi/h at sea level needs C_L = {N(CL54, 3)}")),
                       "explain": L("Bay thẳng đều giống như đứng yên trên một cái cân: lực hướng lên bằng lực hướng xuống, lực kéo tới bằng lực cản lùi.", "Steady level flight is like standing still on a scale: the upward force equals the downward force, and the forward force equals the backward force.")},
                      {"title": L("Tỉ số lướt và đường cực", "Glide ratio and the polar curve"),
                       "body": ul(L("Tỉ số lướt = quãng đường tiến / độ cao mất. Tiến 10 000 ft trong khi mất 1000 ft là tỉ số 10 trên 1 (EASA)", "Glide ratio = forward distance / height lost; travelling 10 000 ft forward while losing 1000 ft is 10 to 1 (EASA)"),
                                  L("Khi lướt thẳng đều, tỉ số lướt bằng L/D = C_L/C_D", "In a steady glide the glide ratio equals L/D = C_L/C_D"),
                                  L("Đường cực vẽ C_L theo C_D; tiếp tuyến kẻ từ gốc tọa độ cho L/D lớn nhất, tức góc lướt nhỏ nhất", "The polar plots C_L against C_D; the tangent from the origin gives the maximum L/D, the shallowest glide angle"),
                                  L("Tốc độ lướt được xa nhất khác với tốc độ cho độ rơi chậm nhất", "The speed for best glide range differs from the speed for minimum sink")),
                       "explain": L("Gió ngược làm quãng lướt so với mặt đất ngắn đi, dù tỉ số lướt so với không khí không đổi.", "A headwind shortens the ground range even though the glide ratio through the air is unchanged.")}]})
    parts.append({"title": L("Vòng bay, hệ số tải và thất tốc", "Turns, load factor and the stall"),
                  "bullets": [L("Trong vòng bay thăng bằng, L cos φ = W nên hệ số tải n = 1/cos φ", "In a level turn L cos φ = W so the load factor is n = 1/cos φ"),
                              L("Tốc độ thất tốc tăng theo √n", "Stall speed increases as √n"),
                              L("Thất tốc xảy ra ở một góc tấn tới hạn, không phải một tốc độ cố định", "The stall occurs at a critical angle of attack, not at one fixed speed")],
                  "slides": [
                      {"title": L("Lực trong vòng bay", "Forces in a turn"),
                       "body": ul(L("Khi nghiêng cánh một góc φ, thành phần thẳng đứng của lực nâng là L cos φ. Muốn giữ độ cao phải tăng lực nâng sao cho L cos φ = W", "When banked by φ the vertical component of lift is L cos φ; to hold altitude lift must grow so that L cos φ = W"),
                                  L("Hệ số tải n = L/W = 1/cos φ, đo bằng g", "Load factor n = L/W = 1/cos φ, measured in g"),
                                  L("Tốc độ thất tốc trong vòng bay: V_s,turn = V_s √n", "Stall speed in the turn: V_s,turn = V_s √n")) +
                       table([L("Góc nghiêng", "Bank"), "n", "√n", L("Tăng tốc độ thất tốc", "Stall-speed increase")], n_rows),
                       "explain": L("Nghiêng 60° thì hệ số tải là 2 g và tốc độ thất tốc tăng 41%. Một máy bay thất tốc ở 60 kt khi bay thẳng sẽ thất tốc ở khoảng 85 kt trong vòng bay đó.", "At a 60° bank the load factor is 2 g and the stall speed rises 41%. An aircraft that stalls at 60 kt in straight flight stalls at about 85 kt in that turn.")},
                      {"title": L("Thất tốc và biên dạng bay", "Stalls and the flight envelope"),
                       "body": ul(L("Thất tốc xảy ra khi góc tấn vượt giá trị tới hạn: dòng tách khỏi mặt trên cánh và C_L giảm", "A stall occurs when the angle of attack exceeds the critical value: flow separates from the upper surface and C_L falls"),
                                  L("Tốc độ thất tốc phụ thuộc trọng lượng, hệ số tải và mật độ, nên máy bay có thể thất tốc ở một tốc độ tưởng là an toàn (EASA tr. 3.7)", "Stall speed depends on weight, load factor and density, so an aircraft can stall at a seemingly safe speed (EASA p. 3.7)"),
                                  L("Trên cánh xuôi hoặc thon, thất tốc thường bắt đầu từ đầu cánh; dải chống thất tốc (stall strip) ở gốc cánh giúp thất tốc bắt đầu từ gốc (EASA)", "On swept or tapered wings the stall tends to start at the tip; stall strips at the wing root make the stall start at the root (EASA)")),
                       "explain": L("\"Flight envelope\" (biên dạng bay) là vùng tốc độ và hệ số tải cho phép. Ra ngoài vùng đó là thất tốc hoặc hỏng kết cấu.", "The \"flight envelope\" is the permitted region of speed and load factor. Outside it lies stall or structural failure.")}]})
    parts.append({"title": L("Hệ số tải và giới hạn kết cấu", "Load factor and structural limits"),
                  "bullets": [L("Hệ số tải đo bằng g: 3 g nghĩa là tổng tải gấp 3 lần trọng lượng", "Load factor is measured in g: 3 g means total load three times the weight"),
                              L("Tải giới hạn của hạng Normal là +3,8 và −1,52 g", "The limit load of the Normal category is +3.8 and −1.52 g"),
                              L("Hệ số an toàn 1,5 áp dụng cho tải giới hạn để có tải phá hủy", "A safety factor of 1.5 applied to the limit load gives the ultimate load")],
                  "slides": [
                      {"title": L("Hệ số tải trong thiết kế", "Load factors in design"),
                       "body": table([L("Hạng", "Category"), L("Hệ số tải giới hạn", "Limit load factor"), L("Tải phá hủy ×1,5", "Ultimate ×1.5")],
                                     [["Normal", "+3,8 / −1,52".replace(",", ".") if lang == "en" else "+3,8 / −1,52", f"+{N(3.8 * 1.5, 2)} / −{N(1.52 * 1.5, 2)}"],
                                      ["Utility", "+4,4 / −1,76".replace(",", ".") if lang == "en" else "+4,4 / −1,76", f"+{N(4.4 * 1.5, 2)} / −{N(1.76 * 1.5, 2)}"],
                                      ["Acrobatic", "+6,0 / −3,0".replace(",", ".") if lang == "en" else "+6,0 / −3,0", f"+{N(6.0 * 1.5, 2)} / −{N(3.0 * 1.5, 2)}"]]) +
                       f"<p class='pill'>{L('EASA tr. 3.9; chứng chỉ các nước có thể khác; hệ số 1,5 là \"factor of safety\" của EASA', 'EASA p. 3.9; certification standards of other countries may differ; 1.5 is the \"factor of safety\" in EASA')}</p>",
                       "explain": L("Với kỹ thuật viên: sau khi gặp nhiễu động mạnh hoặc hạ cánh nặng, cần kiểm tra kết cấu, vì nó có thể đã vượt tải giới hạn dù bên ngoài trông bình thường.", "For a technician: after severe turbulence or a hard landing the structure must be inspected, because it may have exceeded the limit load even though it looks normal outside.")}]})
    parts.append({"title": L("Dòng tốc độ cao, số Mach và sóng xung kích", "High-speed flow, Mach number and shock waves"),
                  "bullets": [L("Số Mach là tỉ số giữa tốc độ khí thực và tốc độ âm thanh", "Mach number is the ratio of true airspeed to the speed of sound"),
                              L("Tốc độ âm thanh phụ thuộc nhiệt độ: a = √(γRT)", "The speed of sound depends on temperature: a = √(γRT)"),
                              L("Số Mach tới hạn là M của dòng tự do khi điểm nào đó trên cánh đạt tốc độ âm", "The critical Mach number is the free-stream M at which some point on the wing reaches sonic speed")],
                  "slides": [
                      {"title": L("Tốc độ âm thanh và số Mach", "Speed of sound and Mach number"),
                       "body": ul(L(f"Ở 15 °C mực biển, a = {N(a_sl_kt, 0)} kt (EASA ghi 661 kt); ở 40 000 ft nhiệt độ ISA −56,5 °C nên a = {N(a_40_kt, 0)} kt (EASA ghi 574 kt)", f"At 15 °C sea level a = {N(a_sl_kt, 0)} kt (EASA gives 661 kt); at 40 000 ft ISA temperature is −56.5 °C so a = {N(a_40_kt, 0)} kt (EASA gives 574 kt)"),
                                  L(f"Anderson 8.1: ở 230 K, a = {N(a81, 1)} m/s", f"Anderson 8.1: at 230 K, a = {N(a81, 1)} m/s"),
                                  L("Cùng một số Mach tương ứng tốc độ thực nhỏ hơn ở độ cao lớn vì không khí lạnh hơn", "The same Mach number corresponds to a lower true airspeed at altitude because the air is colder"),
                                  L("Khoảng 260 kt trở xuống có thể coi không khí không nén được (EASA)", "Up to about 260 kt air can be treated as incompressible (EASA)")),
                       "explain": L("Cùng bay ở M 0,8, trên cao tốc độ thực thấp hơn gần mực biển, vì ở đó a nhỏ hơn.", "At the same M 0.8, the true airspeed is lower at altitude than near sea level, because a is smaller there.")},
                      {"title": L("Số Mach tới hạn, sóng xung kích và nén được", "Critical Mach, shock waves and compressibility"),
                       "body": ul(L("Không khí trên mặt cánh có thể chảy nhanh gấp đôi tốc độ máy bay, nên có chỗ đạt tốc độ âm trong khi máy bay vẫn bay cận âm (EASA)", "Air over the wing can move at up to twice the aircraft speed, so sonic flow can appear locally while the aircraft is still subsonic (EASA)"),
                                  L(f"Anderson 11.4: với C_p,0 = −0,41, quy tắc Prandtl-Glauert cho M_cr ≈ {N(Mcr114, 3)}", f"Anderson 11.4: with C_p,0 = −0.41 the Prandtl-Glauert rule gives M_cr ≈ {N(Mcr114, 3)}"),
                                  L(f"Qua sóng xung kích thẳng ở M₁ = 2,6: M₂ = {N(M2_87, 3)}, p₂/p₁ = {N(p_87, 2)}, ρ₂/ρ₁ = {N(rho_87, 3)}, T₂/T₁ = {N(T_87, 3)} (Anderson 8.7)", f"Across a normal shock at M₁ = 2.6: M₂ = {N(M2_87, 3)}, p₂/p₁ = {N(p_87, 2)}, ρ₂/ρ₁ = {N(rho_87, 3)}, T₂/T₁ = {N(T_87, 3)} (Anderson 8.7)"),
                                  L("Hiệu ứng nén được gây ra lực cản sóng, rung giật và khó điều khiển; đáp án EASA Q3-6 là \"compressibility\"", "Compressibility brings wave drag, buffeting and control difficulty; EASA answer Q3-6 is \"compressibility\"")),
                       "explain": L("Sóng xung kích thẳng luôn đưa dòng từ siêu âm xuống cận âm, đồng thời làm áp suất, nhiệt độ và mật độ tăng vọt.", "A normal shock always takes the flow from supersonic to subsonic, while pressure, temperature and density jump abruptly.")}]})
    parts.append({"title": L("Cánh xuôi và thiết bị tăng lực nâng", "Sweepback and lift augmentation"),
                  "bullets": [L("Cánh xuôi sau trì hoãn ảnh hưởng của nén được", "Sweepback delays the onset of compressibility effects"),
                              L("Cánh tà (flap) ở mép sau tăng lực nâng và lực cản; cánh trước (slat, slot) làm dòng bám lâu hơn", "Flaps on the trailing edge increase lift and drag; leading-edge devices keep the flow attached longer"),
                              L("Thiết bị cố định như tấm xoáy và hàng rào thất tốc điều khiển dòng khí", "Fixed devices such as vortex generators and stall fences manage the airflow")],
                  "slides": [
                      {"title": L("Cánh xuôi sau", "Sweepback"),
                       "body": ul(L("Chỉ thành phần vận tốc vuông góc với đường 1/4 dây cung mới tạo hiệu ứng nén; cánh xuôi làm thành phần này nhỏ đi", "Only the velocity component normal to the quarter-chord line produces the compressibility effect; sweeping the wing reduces it"),
                                  L("Kết quả: số Mach tới hạn tăng, lực cản sóng xuất hiện muộn hơn (EASA Q3-6 \"delay in the onset of compressibility effects\")", "Result: the critical Mach number rises and wave drag appears later (EASA Q3-6 \"a delay in the onset of compressibility effects\")"),
                                  L("Đổi lại, độ dốc đường lực nâng giảm và thất tốc đầu cánh dễ xảy ra hơn", "In return the lift-curve slope falls and tip stall becomes more likely")),
                       "explain": L("Giống như lội chéo qua một dòng suối thay vì lội thẳng ngược dòng: nước \"thấy\" mình chỉ đi với tốc độ nhỏ hơn.", "Like wading diagonally across a stream rather than straight against it: the water \"sees\" a smaller speed.")},
                      {"title": L("Cánh tà, thiết bị mép trước và thiết bị cố định", "Flaps, leading-edge devices and fixed devices"),
                       "body": table([L("Thiết bị", "Device"), L("Vị trí và tác dụng (EASA tr. 3.16–3.18)", "Position and effect (EASA pp. 3.16–3.18)")],
                                     [[L("Cánh tà đơn giản (plain flap)", "Plain flap"), L("đơn giản nhất, tăng độ cong, tăng lực nâng và lực cản", "simplest type, increases camber, lift and drag")],
                                      [L("Cánh tà tách (split flap)", "Split flap"), L("hạ từ mặt dưới, lực cản lớn hơn plain flap", "deflects from the lower surface, more drag than a plain flap")],
                                      [L("Cánh tà có khe (slotted flap)", "Slotted flap"), L("phổ biến nhất; khe dẫn khí qua cánh tà nên C_L tăng nhiều hơn", "most popular; the slot leads air over the flap and raises C_L more")],
                                      [L("Cánh tà Fowler", "Fowler flap"), L("loại slotted flap trượt về sau, tăng thêm diện tích cánh", "a slotted flap that slides aft, also adding wing area")],
                                      [L("Khe cố định, slat, flap mép trước, cuff", "Fixed slot, slat, leading-edge flap, cuff"), L("làm dòng bám ở góc tấn cao, trì hoãn thất tốc", "keep flow attached at high angle of attack and delay the stall")],
                                      [L("Tấm xoáy (vortex generator), hàng rào, dải thất tốc", "Vortex generator, fence, stall strip"), L("tấm xoáy tạo xoáy cấp năng lượng cho lớp biên giới; hàng rào chặn dòng chảy dọc sải; dải thất tốc làm thất tốc bắt đầu ở gốc cánh", "vortices energise the boundary layer; fences stop spanwise flow; stall strips make the stall start at the root")]]),
                       "explain": L("Đáp án EASA: 3-7 là flap, 3-8 là vortex generator.", "EASA answers: 3-7 is the flap, 3-8 is the vortex generator.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Hệ số tải, tốc độ âm thanh, số Mach và lực cản cảm ứng", "Load factor, speed of sound, Mach number and induced drag")
    m["formula_math"] = ("n = L/W = 1/cos φ  ·  V_s,turn = V_s√n  ·  a = √(γRT)  ·  M = V/a<br>C_Di = C_L²/(π e AR)  ·  a_finite = a₀/[1 + (57,3 a₀/πAR)(1+τ)]  ·  p₀/p = (1 + 0,2M²)^3,5" if lang == "vi" else
                         "n = L/W = 1/cos φ  ·  V_s,turn = V_s√n  ·  a = √(γRT)  ·  M = V/a<br>C_Di = C_L²/(π e AR)  ·  a_finite = a₀/[1 + (57.3 a₀/πAR)(1+τ)]  ·  p₀/p = (1 + 0.2M²)^3.5")
    m["legend"] = [("n", L("hệ số tải (g)", "load factor (g)")), ("φ", L("góc nghiêng", "bank angle")), ("γ, R", L("1,4 và 287 J/(kg·K) cho không khí", "1.4 and 287 J/(kg·K) for air")),
                   ("M", L("số Mach", "Mach number")), ("τ", L("hệ số hiệu chỉnh của cánh hữu hạn", "finite-wing correction factor")), ("AR", L("tỉ số kích thước", "aspect ratio"))]
    m["history_title"] = L("Vùng chạm âm và cánh xuôi", "Reaching the sound barrier and the swept wing")
    m["history"] = L("Những năm 1940, khi máy bay tiến gần tốc độ âm thanh, các kỹ sư gặp lực cản tăng vọt, rung giật và mất điều khiển, thường gọi là \"bức tường âm\". Giải pháp là cánh xuôi sau, do Adolf Busemann đề xuất tại hội nghị Volta năm 1935, và về sau được dùng trên hầu hết máy bay phản lực. Anderson dành các mục Historical Note ở chương 9 và 11 cho lịch sử này. EASA chỉ tóm tắt kết quả: cánh xuôi trì hoãn ảnh hưởng của nén được.",
                     "In the 1940s, as aircraft approached the speed of sound, engineers ran into soaring drag, buffeting and loss of control, often called the \"sound barrier\". The remedy was the swept wing, proposed by Adolf Busemann at the 1935 Volta conference and later used on most jet aircraft. Anderson devotes Historical Note sections of chapters 9 and 11 to this history. EASA only summarises the result: sweepback delays the onset of compressibility effects.")
    m["case_title"] = L("Tình huống: cánh Piper Cherokee ở 120 mi/h", "Case: a Piper Cherokee wing at 120 mi/h")
    m["case"] = L(ul(f"<b>Anderson 5.4.</b> Cánh có S = 170 ft², b = 32 ft nên AR = {N(AR54, 2)}. Bay 120 mi/h = {N(V54, 0)} ft/s ở mực biển với W = 2450 lb thì q = {N(q54, 2)} lb/ft² và C_L = {N(CL54, 3)}. Độ dốc lực nâng của cánh hữu hạn là a = {N(a54, 4)} mỗi độ, nên góc tấn hình học là α = C_L/a + α_L=0 = {N(alpha54, 2)}°.",
                  f"<b>Anderson 5.5.</b> Với e = 0,64, hệ số lực cản cảm ứng là C_Di = {N(CDi55, 4)} và lực cản cảm ứng là {N(Di55, 1)} lb."),
                  ul(f"<b>Anderson 5.4.</b> The wing has S = 170 ft² and b = 32 ft, so AR = {N(AR54, 2)}. Flying at 120 mi/h = {N(V54, 0)} ft/s at sea level with W = 2450 lb gives q = {N(q54, 2)} lb/ft² and C_L = {N(CL54, 3)}. The finite-wing lift slope is a = {N(a54, 4)} per degree, so the geometric angle of attack is α = C_L/a + α_L=0 = {N(alpha54, 2)}°.",
                  f"<b>Anderson 5.5.</b> With e = 0.64 the induced-drag coefficient is C_Di = {N(CDi55, 4)} and the induced drag is {N(Di55, 1)} lb."))
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L(ul("EASA định nghĩa hệ số tải là tỉ số giữa tải tối đa máy bay chịu được và trọng lượng. Trong một vòng bay thực tế người ta dùng n = L/W. Cả hai đều đo bằng g, nhưng một cái là giới hạn thiết kế, cái kia là giá trị đang xảy ra.",
                  "Thất tốc phụ thuộc góc tấn, không phải một tốc độ cố định.",
                  "EASA ghi nhiệt độ ở 40 000 ft là −55 °C, còn ISA cho −56,5 °C. Hai số khác nhau do làm tròn, không phải sai sót.",
                  "Số Mach tới hạn không phải tốc độ âm: tại M_cr máy bay vẫn bay cận âm.",
                  "Bài Anderson 5.4 dùng độ dốc của cánh hữu hạn a = a₀/[1 + 57,3a₀(1+τ)/(πAR)], không phải a₀ của biên dạng."),
                  ul("EASA defines load factor as the ratio of the maximum load the aircraft can sustain to its weight. In a real turn you use n = L/W. Both are measured in g, but one is a design limit and the other is the value occurring.",
                  "A stall depends on angle of attack, not on one fixed speed.",
                  "EASA gives the temperature at 40 000 ft as −55 °C, while the ISA gives −56.5 °C. The difference is rounding, not an error.",
                  "The critical Mach number is not the speed of sound: at M_cr the aircraft is still subsonic.",
                  "Anderson 5.4 uses the finite-wing slope a = a₀/[1 + 57.3a₀(1+τ)/(πAR)], not the airfoil's a₀."))
    m["nb_desc"] = L("Notebook giải lại Anderson 5.4, 5.5, 8.1, 8.7, 8.11, 11.4, tính bảng hệ số tải và tốc độ thất tốc trong vòng bay, kiểm tốc độ âm thanh EASA (661 kt và 574 kt) và dùng assert để kiểm mọi đáp án quiz.",
                     "The notebook re-solves Anderson 5.4, 5.5, 8.1, 8.7, 8.11 and 11.4, builds the load-factor and turn-stall table, checks the EASA speeds of sound (661 kt and 574 kt) and uses assert to check every quiz answer.")

    SD = lambda i: 300 + i
    SRC = lambda q, p1, p2: L(f"EASA M08 Q3-{q} (tr. {p1}, đáp án tr. {p2})", f"EASA M08 Q3-{q} (p. {p1}, answer p. {p2})")
    easa = [
        mcq(SD(1), SRC(1, "3.19", "3.20"), L("____ là lực hướng lên tác dụng lên cánh, vuông góc với gió tương đối.", "____ is the upward force on the wing acting perpendicular to the relative wind."),
            L("Lực nâng (lift)", "Lift"), [L("Lực cản (drag)", "Drag"), L("Lực đẩy (thrust)", "Thrust"), L("Trọng lượng (weight)", "Weight")],
            L("Lực nâng vuông góc với gió tương đối; lực cản song song với nó.", "Lift is perpendicular to the relative wind; drag is parallel to it.")),
        mcq(SD(2), SRC(2, "3.19", "3.20"), L("Để thắng ____ và đưa máy bay tiến lên, cần có lực đẩy.", "To overcome ____ and move the aircraft forward, thrust is needed."),
            L("lực cản (drag)", "drag"), [L("lực nâng (lift)", "lift"), L("lực ly tâm", "centrifugal force"), L("trọng lượng", "weight")],
            L("Lực đẩy cân bằng lực cản ở bay thẳng đều.", "Thrust balances drag in steady level flight.")),
        mcq(SD(3), SRC(3, "3.19", "3.20"), L("Một vật đứng yên hoặc chuyển động thẳng đều giữ nguyên trạng thái đó cho đến khi:", "An object at rest or moving in a straight line remains at rest or continues to move in a straight line until:"),
            L("bị một lực khác tác động", "acted on by some other force"), [L("trọng lượng của nó thay đổi", "its weight changes"), L("nhiệt độ của nó thay đổi", "its temperature changes"), L("nó chạm mặt đất", "it touches the ground")],
            L("Đây là định luật 1 của Newton.", "This is Newton's first law.")),
        mcq(SD(4), SRC(4, "3.19", "3.20"), L("Tỉ số giữa tải tối đa máy bay chịu được và trọng lượng toàn phần của máy bay gọi là:", "The ratio of the maximum load an aircraft can sustain to the gross weight of the aircraft is called:"),
            L("hệ số tải (load factor)", "load factor"), [L("tỉ số lướt (glide ratio)", "glide ratio"), L("tỉ số kích thước (aspect ratio)", "aspect ratio"), L("hệ số an toàn thông thường", "ordinary safety factor")],
            L("EASA tr. 3.9; đo bằng g.", "EASA p. 3.9; measured in g.")),
        mcq(SD(5), SRC(5, "3.19", "3.20"), L("Tỉ số giữa tốc độ thực của máy bay và tốc độ âm thanh gọi là:", "The ratio of true airspeed to the speed of sound is known as:"),
            L("số Mach", "Mach number"), [L("hệ số tải", "load factor"), L("tốc độ chỉ thị (IAS)", "indicated airspeed (IAS)"), L("tỉ số nén", "compression ratio")],
            L("M = V/a, EASA tr. 3.12.", "M = V/a, EASA p. 3.12.")),
        mcq(SD(6), SRC(6, "3.19", "3.20"), L("Tác dụng của cánh xuôi sau là trì hoãn sự xuất hiện của các hiệu ứng ____.", "The effect of a sweptback wing is a delay in the onset of ____ effects."),
            L("nén được (compressibility)", "compressibility"), [L("độ nhớt", "viscosity"), L("ma sát da", "skin friction"), L("nhiễu loạn tầng", "laminar turbulence")],
            L("Xuôi cánh làm giảm thành phần vận tốc vuông góc đường 1/4 dây cung.", "Sweep reduces the velocity component normal to the quarter-chord line.")),
        mcq(SD(7), SRC(7, "3.19", "3.20"), L("Thiết bị tăng lực nâng phổ biến nhất ở mép sau cánh, tăng lực nâng và lực cản, gọi là:", "The most common high-lift device fitted to the aft edge of the wing which increases lift and drag is known as a:"),
            L("cánh tà (flap)", "flap"), [L("tấm xoáy (vortex generator)", "vortex generator"), L("slat", "slat"), L("hàng rào thất tốc (stall fence)", "stall fence")],
            L("Cánh tà đặt ở mép sau; slat ở mép trước.", "Flaps sit on the trailing edge; slats on the leading edge.")),
        mcq(SD(8), SRC(8, "3.19", "3.20"), L("____ là một biên dạng nhỏ gắn trên mặt trên cánh, thúc đẩy dòng tầng dương trên cánh và các bề mặt điều khiển.", "A ____ is a small airfoil section attached to the upper surface of a wing that promotes positive laminar airflow over the wing and control surfaces."),
            L("tấm xoáy (vortex generator)", "vortex generator"), [L("cánh tà Fowler", "Fowler flap"), L("khe cố định", "fixed slot"), L("cuff mép trước", "leading-edge cuff")],
            L("Tấm xoáy tạo xoáy nhỏ cấp năng lượng cho lớp biên giới (EASA tr. 3.18).", "Vortex generators make small vortices that energise the boundary layer (EASA p. 3.18).")),
    ]
    book = [
        mcq(SD(11), "Anderson 6th, Problem 5.4",
            L("Piper Cherokee: S = 170 ft², b = 32 ft, W = 2450 lb, biên dạng có a₀ = 0,1033/độ và α_L=0 = −3°, τ = 0,12. Bay 120 mi/h ở mực biển, thẳng đều. Góc tấn hình học của cánh là:", "Piper Cherokee: S = 170 ft², b = 32 ft, W = 2450 lb, airfoil a₀ = 0.1033/degree and α_L=0 = −3°, τ = 0.12. Cruising straight and level at 120 mi/h at sea level. The geometric angle of attack of the wing is:"),
            f"{N(alpha54, 2)}°", [f"{N(CL54 / a0 - 3, 2)}°", f"{N(CL54 / a54, 2)}°", f"{N(alpha54 * 2, 2)}°"],
            L("C_L = W/(qS), rồi α = C_L/a + α_L=0 với a của cánh hữu hạn.", "C_L = W/(qS), then α = C_L/a + α_L=0 with the finite-wing a."),
            L(f"<p>AR = b²/S = {N(AR54, 3)}; V = 176 ft/s; q = {N(q54, 2)} lb/ft²; C_L = {N(CL54, 4)}; a = a₀/[1 + 57,3a₀(1+τ)/(πAR)] = {N(a54, 4)}/độ; α = {N(CL54 / a54, 3)} − 3 = {N(alpha54, 2)}°. Dùng a₀ thay a cho kết quả sai {N(CL54 / a0 - 3, 2)}°.</p>", f"<p>AR = b²/S = {N(AR54, 3)}; V = 176 ft/s; q = {N(q54, 2)} lb/ft²; C_L = {N(CL54, 4)}; a = a₀/[1 + 57.3a₀(1+τ)/(πAR)] = {N(a54, 4)}/degree; α = {N(CL54 / a54, 3)} − 3 = {N(alpha54, 2)}°. Using a₀ instead of a gives the wrong {N(CL54 / a0 - 3, 2)}°.</p>")),
        mcq(SD(12), "Anderson 6th, Problem 5.5",
            L("Với máy bay ở bài 5.4 và hệ số hiệu suất toàn máy bay e = 0,64, lực cản cảm ứng xấp xỉ:", "For the aircraft of Problem 5.4 with an airplane span-efficiency factor e = 0.64, the induced drag is about:"),
            f"{N(Di55, 1)} lb", [f"{N(Di55 * 0.64, 1)} lb", f"{N(Di55 * 1.8, 1)} lb", f"{N(Di55 / 2.5, 1)} lb"],
            L("C_Di = C_L²/(π e AR), D_i = C_Di q S.", "C_Di = C_L²/(π e AR), D_i = C_Di q S."),
            L(f"<p>C_Di = {N(CL54, 4)}²/(π·0,64·{N(AR54, 3)}) = {N(CDi55, 5)}; D_i = {N(CDi55, 5)}×{N(q54, 2)}×170 = {N(Di55, 1)} lb.</p>", f"<p>C_Di = {N(CL54, 4)}²/(π·0.64·{N(AR54, 3)}) = {N(CDi55, 5)}; D_i = {N(CDi55, 5)}×{N(q54, 2)}×170 = {N(Di55, 1)} lb.</p>")),
        mcq(SD(13), "Anderson 6th, Problem 8.1",
            L("Tốc độ âm thanh trong không khí ở 230 K (γ = 1,4, R = 287 J/(kg·K)) là:", "The speed of sound in air at 230 K (γ = 1.4, R = 287 J/(kg·K)) is:"),
            f"{N(a81, 1)} m/s", [f"{N(a81 * 1.12, 1)} m/s", f"{N(a81 / 1.18, 1)} m/s", f"{N(a81 ** 2 / 100, 1)} m/s"],
            L("a = √(γRT).", "a = √(γRT)."),
            L(f"<p>a = √(1,4 × 287 × 230) = √{N(1.4 * 287 * 230, 0)} = {N(a81, 1)} m/s.</p>", f"<p>a = √(1.4 × 287 × 230) = √{N(1.4 * 287 * 230, 0)} = {N(a81, 1)} m/s.</p>")),
        mcq(SD(14), "Anderson 6th, Problem 8.11",
            L("Dòng khí ở 1 atm và 288 K; ống Pitot đo 1,555 atm. Vận tốc dòng (dùng quan hệ cận âm nén được) là:", "A flow at 1 atm and 288 K; a Pitot tube reads 1.555 atm. The flow velocity (using the compressible subsonic relation) is:"),
            f"{N(V811, 1)} m/s (M = {N(M811, 3)})", [f"{N(math.sqrt(2 * 0.555 * 101325 / 1.225), 1)} m/s (Bernoulli)", f"{N(V811 * 1.3, 1)} m/s", f"{N(V811 / 1.3, 1)} m/s"],
            L("p₀/p = (1 + 0,2M²)^3,5, giải M rồi V = M·a.", "p₀/p = (1 + 0.2M²)^3.5, solve M then V = M·a."),
            L(f"<p>Giải (1 + 0,2M²)^3,5 = 1,555 cho M = {N(M811, 4)}; a = √(1,4×287×288) = {N(speed_of_sound(288, 287), 1)} m/s; V = {N(V811, 1)} m/s. Bernoulli không nén được cho {N(math.sqrt(2 * 0.555 * 101325 / 1.225), 1)} m/s, sai lớn ở M ≈ 0,8 (Anderson 8.13).</p>", f"<p>Solving (1 + 0.2M²)^3.5 = 1.555 gives M = {N(M811, 4)}; a = √(1.4×287×288) = {N(speed_of_sound(288, 287), 1)} m/s; V = {N(V811, 1)} m/s. Incompressible Bernoulli gives {N(math.sqrt(2 * 0.555 * 101325 / 1.225), 1)} m/s, a large error at M ≈ 0.8 (Anderson 8.13).</p>")),
        mcq(SD(15), "Anderson 6th, Problem 8.7",
            L("Dòng ngay trước sóng xung kích thẳng: p₁ = 1 atm, T₁ = 288 K, M₁ = 2,6. Ngay sau sóng, M₂ và p₂ là:", "The flow just upstream of a normal shock has p₁ = 1 atm, T₁ = 288 K, M₁ = 2.6. Just downstream, M₂ and p₂ are:"),
            f"M₂ = {N(M2_87, 3)} ; p₂ = {N(p_87, 2)} atm", [f"M₂ = {N(1 / 2.6, 3)} ; p₂ = {N(2.6 ** 2, 2)} atm", f"M₂ = {N(M2_87, 3)} ; p₂ = {N(p_87 / 2, 2)} atm", f"M₂ = {N(1.5, 3)} ; p₂ = {N(p_87, 2)} atm"],
            L("Quan hệ sóng xung kích thẳng với γ = 1,4.", "Normal-shock relations with γ = 1.4."),
            L(f"<p>M₂² = [(γ−1)M₁² + 2]/[2γM₁² − (γ−1)] nên M₂ = {N(M2_87, 4)}; p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1) = {N(p_87, 3)}; ρ₂/ρ₁ = {N(rho_87, 3)}; T₂/T₁ = {N(T_87, 3)} nên T₂ = {N(T_87 * 288, 1)} K.</p>", f"<p>M₂² = [(γ−1)M₁² + 2]/[2γM₁² − (γ−1)] so M₂ = {N(M2_87, 4)}; p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1) = {N(p_87, 3)}; ρ₂/ρ₁ = {N(rho_87, 3)}; T₂/T₁ = {N(T_87, 3)} so T₂ = {N(T_87 * 288, 1)} K.</p>")),
        mcq(SD(16), "Anderson 6th, Problem 11.4",
            L("Trong dòng không nén được, C_p nhỏ nhất của một biên dạng là −0,41. Ước lượng số Mach tới hạn bằng quy tắc Prandtl-Glauert:", "In incompressible flow the peak pressure coefficient of an airfoil is −0.41. Estimate the critical Mach number with the Prandtl-Glauert rule:"),
            N(Mcr114, 3), [N(0.5, 3), N(0.9, 3), N(1.0, 3)],
            L("Giải C_p,0/√(1−M²) = C_p,cr(M).", "Solve C_p,0/√(1−M²) = C_p,cr(M)."),
            L(f"<p>Cp,cr(M) = (2/γM²)[((1+0,2M²)/1,2)^3,5 − 1]; cân bằng với −0,41/√(1−M²) cho M_cr = {N(Mcr114, 4)} (nghiệm số).</p>", f"<p>Cp,cr(M) = (2/γM²)[((1+0.2M²)/1.2)^3.5 − 1]; equating it with −0.41/√(1−M²) gives M_cr = {N(Mcr114, 4)} (numerical root).</p>")),
    ]
    SUP = L("Câu luyện thêm", "Extra practice")
    gen = [
        mcq(SD(21), SUP, L("Máy bay mất 3000 ft độ cao khi tiến 36 000 ft trong lướt thẳng đều. Tỉ số lướt là:", "An aircraft loses 3000 ft of height while travelling 36 000 ft in a steady glide. The glide ratio is:"),
            L("12 trên 1", "12 to 1"), [L("3 trên 1", "3 to 1"), L("33 trên 1", "33 to 1"), L("108 trên 1", "108 to 1")],
            L("36 000/3000 = 12; tỉ số lướt cũng bằng L/D.", "36 000/3000 = 12; the glide ratio also equals L/D.")),
        mcq(SD(22), SUP, L("Vòng bay thăng bằng với góc nghiêng 60° có hệ số tải:", "A level turn with a 60° bank has a load factor of:"),
            "2,0 g" if lang == "vi" else "2.0 g", ["1,5 g" if lang == "vi" else "1.5 g", "0,5 g" if lang == "vi" else "0.5 g", "1,73 g" if lang == "vi" else "1.73 g"],
            L("n = 1/cos 60° = 2.", "n = 1/cos 60° = 2.")),
        mcq(SD(23), SUP, L("Máy bay thất tốc ở 60 kt khi bay thẳng. Trong vòng bay 60° nghiêng, tốc độ thất tốc xấp xỉ:", "An aircraft stalls at 60 kt in straight flight. In a 60° bank turn its stall speed is about:"),
            f"{N(60 * math.sqrt(2), 0)} kt", [f"{N(120, 0)} kt", f"{N(60, 0)} kt", f"{N(60 / math.sqrt(2), 0)} kt"],
            L("V_s,turn = V_s√n = 60√2.", "V_s,turn = V_s√n = 60√2.")),
        mcq(SD(24), SUP, L("Trong hạng Normal, hệ số tải giới hạn dương là +3,8. Tải phá hủy theo hệ số an toàn 1,5 là:", "In the Normal category the positive limit load factor is +3.8. The ultimate load with a safety factor of 1.5 is:"),
            f"+{N(3.8 * 1.5, 2)} g", [f"+{N(3.8 / 1.5, 2)} g", f"+{N(3.8 + 1.5, 2)} g", f"+{N(3.8 * 2, 2)} g"],
            L("3,8 × 1,5 = 5,7 g (EASA tr. 3.9).", "3.8 × 1.5 = 5.7 g (EASA p. 3.9).")),
        mcq(SD(25), SUP, L("Một máy bay bay M 0,8 ở 40 000 ft (a ≈ 574 kt). Tốc độ thực xấp xỉ:", "An aircraft flies M 0.8 at 40 000 ft (a ≈ 574 kt). Its true airspeed is about:"),
            f"{N(0.8 * a_40_kt, 0)} kt", [f"{N(0.8 * a_sl_kt, 0)} kt", f"{N(a_40_kt / 0.8, 0)} kt", f"{N(a_40_kt, 0)} kt"],
            L("V = M·a = 0,8 × 573,6.", "V = M·a = 0.8 × 573.6.")),
        mcq(SD(26), SUP, L("Số Mach tới hạn là:", "The critical Mach number is the:"),
            L("số Mach dòng tự do mà tại đó điểm nhanh nhất trên cánh đạt M = 1", "free-stream Mach number at which the fastest point on the wing reaches M = 1"), [L("số Mach mà máy bay đạt tốc độ âm thanh", "Mach number at which the aircraft reaches the speed of sound"), L("số Mach mà lớp biên giới thành rối", "Mach number at which the boundary layer becomes turbulent"), L("số Mach tại đó cánh thất tốc", "Mach number at which the wing stalls")],
            L("Máy bay vẫn cận âm khi tới M_cr (EASA tr. 3.11).", "The aircraft is still subsonic at M_cr (EASA p. 3.11).")),
        mcq(SD(27), SUP, L("Cánh tà nào tăng cả diện tích cánh lẫn độ cong khi hạ?", "Which flap increases both wing area and camber when lowered?"),
            L("Cánh tà Fowler", "Fowler flap"), [L("Cánh tà đơn giản", "Plain flap"), L("Cánh tà tách", "Split flap"), L("Flap mép trước", "Leading-edge flap")],
            L("Fowler trượt về sau trên ray, thêm diện tích rồi mới hạ góc.", "The Fowler slides aft on tracks, adding area before it deflects.")),
        mcq(SD(28), SUP, L("Dải thất tốc (stall strip) gắn ở khoảng 20–25% gốc cánh nhằm:", "A stall strip fitted on the inner 20–25% of the wing is meant to:"),
            L("cho thất tốc bắt đầu ở gốc cánh, giữ hiệu lực aileron", "make the stall start at the root and keep aileron control"), [L("tăng lực nâng ở đầu cánh", "increase lift at the tip"), L("giảm lực cản cảm ứng", "reduce induced drag"), L("tăng tốc độ tối đa", "raise maximum speed")],
            L("EASA (mục Stalls): gắn dải ở 20–25% đầu tiên của cánh; thất tốc bắt đầu ở gốc nên aileron ở đầu cánh còn hiệu lực.", "EASA (Stalls section): strips on the first 20–25% of the wing; the stall begins at the root so the tip ailerons stay effective.")),
    ]
    m["quiz_sets"] = [
        {"key": "easa", "title": L("Sách 1, EASA Module 08: câu hỏi cuối Sub-module 03 (8 câu, đổi từ điền khuyết sang trắc nghiệm)", "Book 1, EASA Module 08: end of Sub-module 03 (8 questions, converted from fill-in to multiple choice)"),
         "intro": L("Đáp án đúng giữ nguyên như bản in (tr. 3.20); các phương án sai được viết thêm.", "The correct answer is the printed one (p. 3.20); the wrong options were added for this quiz."), "items": easa},
        {"key": "anderson", "title": L("Sách 2, Anderson: bài tập cuối chương 5, 8, 11 (đáp án đã tính lại)", "Book 2, Anderson: end-of-chapter problems from ch. 5, 8, 11 (answers recomputed)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập thêm (tự soạn, đáp án đã kiểm bằng tính toán)", "Extra practice (written for this site, answers checked by calculation)"), "items": gen},
    ]
    m["problems_intro"] = L("Ba nhóm bài của Anderson, giải từng bước. Đề lấy từ bản 6 (mục 5.10, 8.9, 11.17). Solution Manual bản 4 không có chương 5 nên bài 5.4 và 5.5 chưa đối chiếu được; kết quả của chúng được kiểm lại độc lập trong notebook. Bài 8.1, 8.7, 8.11 khớp Solution Manual. Bài 11.4 cũng khớp: Solution Manual đọc M_cr ≈ 0,74 từ đồ thị (xem thêm module 10).",
                            "Three groups of Anderson problems, solved step by step. The problems come from the 6th edition (sec. 5.10, 8.9, 11.17). The 4th-edition Solution Manual has no chapter 5, so problems 5.4 and 5.5 could not be compared; their results were rechecked independently in the notebook. Problems 8.1, 8.7 and 8.11 agree with the Solution Manual. Problem 11.4 agrees too: the Solution Manual reads M_cr ≈ 0.74 from a graph (see also module 10).")
    m["problems"] = [
        {"num": "5.4 – 5.5", "src": "Anderson 6th, Problems 5.4 and 5.5", "q": L("Máy bay Piper Cherokee có S = 170 ft², b = 32 ft, W = 2450 lb, bay 120 mi/h ở mực biển. Biên dạng cánh có a₀ = 0,1033/độ, α_L=0 = −3°, τ = 0,12. Tìm góc tấn hình học; sau đó tìm lực cản cảm ứng với e = 0,64.", "A Piper Cherokee has S = 170 ft², b = 32 ft, W = 2450 lb and flies at 120 mi/h at sea level. The airfoil has a₀ = 0.1033/degree, α_L=0 = −3°, τ = 0.12. Find the geometric angle of attack; then find the induced drag with e = 0.64."),
         "ans": L(f"<p>AR = {N(AR54, 3)}; q = {N(q54, 2)} lb/ft²; C_L = W/(qS) = <b>{N(CL54, 4)}</b>.</p><p>a = {N(a54, 4)}/độ; α = C_L/a + α_L=0 = <b>{N(alpha54, 2)}°</b>.</p><p>C_Di = C_L²/(π e AR) = {N(CDi55, 5)}; D_i = <b>{N(Di55, 1)} lb</b>.</p>", f"<p>AR = {N(AR54, 3)}; q = {N(q54, 2)} lb/ft²; C_L = W/(qS) = <b>{N(CL54, 4)}</b>.</p><p>a = {N(a54, 4)}/degree; α = C_L/a + α_L=0 = <b>{N(alpha54, 2)}°</b>.</p><p>C_Di = C_L²/(π e AR) = {N(CDi55, 5)}; D_i = <b>{N(Di55, 1)} lb</b>.</p>")},
        {"num": "8.1, 8.11", "src": "Anderson 6th, Problems 8.1 and 8.11", "q": L("(8.1) Tính tốc độ âm thanh ở 230 K. (8.11) Dòng khí ở 1 atm và 288 K, ống Pitot đo được 1,555 atm. Tính vận tốc dòng.", "(8.1) Find the speed of sound at 230 K. (8.11) A flow at 1 atm and 288 K; a Pitot tube reads 1.555 atm. Find the flow velocity."),
         "ans": L(f"<p>(8.1) a = √(γRT) = <b>{N(a81, 1)} m/s</b>.</p><p>(8.11) (1 + 0,2M²)^3,5 = 1,555 ⇒ M = {N(M811, 4)}; V = M√(γRT) = <b>{N(V811, 1)} m/s</b>.</p>", f"<p>(8.1) a = √(γRT) = <b>{N(a81, 1)} m/s</b>.</p><p>(8.11) (1 + 0.2M²)^3.5 = 1.555 ⇒ M = {N(M811, 4)}; V = M√(γRT) = <b>{N(V811, 1)} m/s</b>.</p>")},
        {"num": "8.7, 11.4", "src": "Anderson 6th, Problems 8.7 and 11.4", "q": L("(8.7) Sóng xung kích thẳng với M₁ = 2,6, p₁ = 1 atm, T₁ = 288 K: tính M₂, p₂, T₂. (11.4) Giá trị C_p nhỏ nhất của biên dạng trong dòng không nén được là C_p,0 = −0,41: ước lượng M_cr.", "(8.7) A normal shock with M₁ = 2.6, p₁ = 1 atm, T₁ = 288 K: find M₂, p₂, T₂. (11.4) The minimum pressure coefficient of an airfoil in incompressible flow is C_p,0 = −0.41: estimate M_cr."),
         "ans": L(f"<p>(8.7) M₂ = <b>{N(M2_87, 3)}</b>; p₂ = <b>{N(p_87, 2)} atm</b>; T₂ = {N(T_87, 3)} × 288 = <b>{N(T_87 * 288, 1)} K</b>.</p><p>(11.4) M_cr = <b>{N(Mcr114, 3)}</b> (nghiệm số của C_p,0/√(1−M²) = C_p,cr(M)).</p>", f"<p>(8.7) M₂ = <b>{N(M2_87, 3)}</b>; p₂ = <b>{N(p_87, 2)} atm</b>; T₂ = {N(T_87, 3)} × 288 = <b>{N(T_87 * 288, 1)} K</b>.</p><p>(11.4) M_cr = <b>{N(Mcr114, 3)}</b> (numerical root of C_p,0/√(1−M²) = C_p,cr(M)).</p>")},
    ]
    return m
