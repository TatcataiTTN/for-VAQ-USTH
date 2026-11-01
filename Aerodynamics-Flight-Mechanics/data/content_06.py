# -*- coding: utf-8 -*-
"""Module 06: Dong nen duoc: quan he dang entropi va song xung kich thang. Nguon: Anderson 6th ch.7 (7.1, 7.4, 7.5), ch.8 (8.3, 8.5, 8.8, 8.9, 8.11, 8.16),
EASA M08 SM3 (tr.3.10-3.13: dong cao toc, so Mach, song xung kich)."""
import math
from aero import *
from common import num, ul, table, mcq


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)
    g = GAMMA

    rho71 = 7.8 * 2116 / (1716 * 934)
    rho74 = (4.35e4 / (287 * 245)) * (3.6e4 / 4.35e4) ** (1 / g)
    Te75 = 500 * (1 / 10) ** ((g - 1) / g); rho75 = 1.01e5 / (R_SI * Te75)
    M83 = 250 / speed_of_sound(300, R_SI); p083 = 1.2 * p0_over_p(M83); T083 = 300 * T0_over_T(M83)
    p085 = p0_over_p(2.0); T085 = 230 * T0_over_T(2.0)
    M88 = math.sqrt((10.33 - 1) * (g + 1) / (2 * g) + 1); T1_88 = 1390 / normal_shock(M88)[3]
    M89 = mach_from_shock_entropy(199.5 / R_SI)
    M816 = mach_from_rayleigh(1.13 / 0.1)
    M2_87, p_87, rho_87, T_87 = normal_shock(2.6)
    p02p01_87 = normal_shock_p0(2.6)
    M810 = 3.1; M2_810, p810, r810, T810 = normal_shock(M810); T2_810 = 480 * T810
    V2_810 = M2_810 * math.sqrt(g * 1716 * T2_810)

    m = {"num": "06", "slug": "06-compressible-flow", "tag": L("Dòng nén được", "Compressible flow")}
    m["title"] = L("Dòng nén được: quan hệ đẳng entropi và sóng xung kích thẳng", "Compressible flow: isentropic relations and normal shock waves")
    m["src"] = L("Anderson ch.7 (Bài 7.1, 7.4, 7.5) và ch.8 (Bài 8.3, 8.5, 8.8, 8.9, 8.16) · EASA Module 08, Sub-module 03 (tr. 3.10–3.13)",
                 "Anderson ch. 7 (Problems 7.1, 7.4, 7.5) and ch. 8 (Problems 8.3, 8.5, 8.8, 8.9, 8.16) · EASA Module 08, Sub-module 03 (pp. 3.10–3.13)")
    m["intro"] = L("Module 03 đã nêu số Mach, số Mach tới hạn và sóng xung kích ở mức định tính cùng vài số. Module này đặt nền định lượng: khí lý tưởng nhiệt dung không đổi, các đại lượng toàn phần (p₀, T₀), quan hệ đẳng entropi theo số Mach, rồi các hệ thức sóng xung kích thẳng và ý nghĩa của tổn thất áp suất toàn phần. Tất cả bài tập ch.7 và 8 của Anderson được tính lại bằng Python, có hai bài cho đáp án tròn (M₁ = 2,5 và M = 2,9) làm bằng chứng kiểm chứng.",
                   "Module 03 introduced Mach number, critical Mach number and shock waves qualitatively with a few numbers. This module lays the quantitative foundation: the calorically perfect gas, stagnation quantities (p₀, T₀), isentropic relations in terms of Mach number, then the normal-shock relations and what the loss of total pressure means. The Anderson ch. 7 and 8 problems are recomputed in Python, and two give round answers (M₁ = 2.5 and M = 2.9) as a check.")
    m["mapping"] = {
        "easa": L("Sub-module 03 (tr. 3.10–3.13: dòng cận âm và siêu âm, dải tốc độ, Mach so với tốc độ, sóng xung kích) và các câu Q3-5, Q3-6", "Sub-module 03 (pp. 3.10–3.13: subsonic and supersonic flow, speed ranges, Mach number versus airspeed, shock waves) and questions Q3-5, Q3-6"),
        "anderson": L("Ch.7 Compressible Flow: Some Preliminary Aspects (7.2 nhiệt động, 7.5 đại lượng toàn phần); Ch.8 Normal Shock Waves and Related Topics (8.2 phương trình sóng xung kích thẳng, 8.3 tốc độ âm thanh, 8.4 đẳng entropi, 8.7 ống Pitot nén được); Bài 7.1, 7.4, 7.5, 8.3, 8.5, 8.8, 8.9, 8.10, 8.16",
                      "Ch.7 Compressible Flow: Some Preliminary Aspects (7.2 thermodynamics, 7.5 total quantities); Ch.8 Normal Shock Waves and Related Topics (8.2 normal-shock equations, 8.3 speed of sound, 8.4 isentropic flow, 8.7 compressible Pitot); Problems 7.1, 7.4, 7.5, 8.3, 8.5, 8.8, 8.9, 8.10, 8.16"),
        "etkin": L("Không có: Etkin &amp; Reid xét máy bay dưới tốc độ có ảnh hưởng nén được đáng kể (Etkin 6.3 ghi rõ giới hạn này); ảnh hưởng của số Mach lên đạo hàm ổn định xuất hiện ở Phụ lục B", "None: Etkin &amp; Reid treat flight below significant compressibility effects (Etkin 6.3 states this limit); the Mach-number effect on the stability derivatives appears in Appendix B"),
        "note": L("Anderson cung cấp toàn bộ lý thuyết; EASA cho tên gọi và hình minh họa. Các bảng trong phụ lục A, B, C của Anderson được thay bằng công thức tính trực tiếp.", "Anderson provides the full theory; EASA provides names and illustrations. The tables in Anderson's Appendices A, B, C are replaced by direct evaluation of the formulas."),
    }
    parts = []
    parts.append({"title": L("Khí lý tưởng nhiệt dung không đổi", "The calorically perfect gas"),
                  "bullets": [L("p = ρRT với c_p, c_v không đổi và γ = c_p/c_v = 1,4 cho không khí", "p = ρRT with constant c_p, c_v and γ = c_p/c_v = 1.4 for air"),
                              L("Tốc độ âm thanh a = √(γRT); số Mach M = V/a", "Speed of sound a = √(γRT); Mach number M = V/a"),
                              L("Dòng đoạn nhiệt thuận nghịch giữ entropi không đổi", "Reversible adiabatic flow keeps the entropy constant")],
                  "slides": [
                      {"title": L("Phương trình trạng thái ở điểm đình trệ (Anderson 7.1)", "Equation of state at a stagnation point (Anderson 7.1)"),
                       "body": ul(L(f"Mũi tên lửa: T₀ = 934 °R, p₀ = 7,8 atm = {N(7.8 * 2116, 0)} lb/ft² cho ρ₀ = p/(RT) = {N(rho71, 5)} slug/ft³ với R = 1716 ft·lb/(slug·°R)", f"Missile nose: T₀ = 934 °R, p₀ = 7.8 atm = {N(7.8 * 2116, 0)} lb/ft² gives ρ₀ = p/(RT) = {N(rho71, 5)} slug/ft³ with R = 1716 ft·lb/(slug·°R)"),
                                  L(f"Anderson 8.1 đã tính a = 304,0 m/s ở 230 K (γ = 1,4, R = 287)", f"Anderson 8.1 already gave a = 304.0 m/s at 230 K (γ = 1.4, R = 287)"),
                                  L("Hằng số khí R = 287 J/(kg·K) = 1716 ft·lb/(slug·°R) cho không khí", "The gas constant R = 287 J/(kg·K) = 1716 ft·lb/(slug·°R) for air")),
                       "explain": L("Nhớ dùng nhiệt độ tuyệt đối (K hoặc °R) và áp suất tuyệt đối khi áp dụng p = ρRT.", "Always use absolute temperature (K or °R) and absolute pressure in p = ρRT.")}]})
    parts.append({"title": L("Đại lượng toàn phần và quan hệ đẳng entropi", "Total quantities and isentropic relations"),
                  "bullets": [L("T₀/T = 1 + (γ−1)M²/2; p₀/p = (T₀/T)^{γ/(γ−1)}; ρ₀/ρ = (T₀/T)^{1/(γ−1)}", "T₀/T = 1 + (γ−1)M²/2; p₀/p = (T₀/T)^{γ/(γ−1)}; ρ₀/ρ = (T₀/T)^{1/(γ−1)}"),
                              L("Mọi đại lượng toàn phần giữ nguyên dọc dòng đoạn nhiệt thuận nghịch", "All total quantities are constant along a reversible adiabatic flow"),
                              L("Từ số Mach và p, T tại một điểm suy ra p₀, T₀", "From the Mach number and p, T at a point we get p₀, T₀")],
                  "slides": [
                      {"title": L("Bài 8.3 và 8.5: tính p₀, T₀", "Problems 8.3 and 8.5: finding p₀, T₀"),
                       "body": table([L("Bài", "Problem"), L("Dữ liệu", "Data"), L("Kết quả", "Result")],
                                     [["8.3", "T = 300 K, p = 1,2 atm, V = 250 m/s" if lang == "vi" else "T = 300 K, p = 1.2 atm, V = 250 m/s", f"M = {N(M83, 3)}; p₀ = {N(p083, 3)} atm; T₀ = {N(T083, 1)} K"],
                                      ["8.5", L("p = 1 atm, T = 230 K, M = 2", "p = 1 atm, T = 230 K, M = 2"), f"p₀ = {N(p085, 3)} atm; T₀ = {N(T085, 0)} K"]]) +
                       f"<p class='pill'>{L('Bài 8.5 cho p₀/p = 7,824 và T₀/T = 1,8 đúng với bảng đẳng entropi ở M = 2', 'Problem 8.5 gives p₀/p = 7.824 and T₀/T = 1.8, matching the isentropic table at M = 2')}</p>",
                       "explain": L("Áp suất toàn phần là áp suất ta thu được khi hãm dòng đẳng entropi về 0; ống Pitot đo gần đúng đại lượng này.", "Total pressure is the pressure obtained by bringing the flow isentropically to rest; a Pitot tube measures approximately this.")},
                      {"title": L("Dòng đẳng entropi qua biên dạng và vòi phun (Anderson 7.4, 7.5)", "Isentropic flow over an airfoil and in a nozzle (Anderson 7.4, 7.5)"),
                       "body": ul(L(f"7.4: T∞ = 245 K, p∞ = 4,35×10⁴, p = 3,6×10⁴ N/m² cho ρ = ρ∞(p/p∞)^{{1/γ}} = {N(rho74, 4)} kg/m³", f"7.4: T∞ = 245 K, p∞ = 4.35×10⁴, p = 3.6×10⁴ N/m² gives ρ = ρ∞(p/p∞)^{{1/γ}} = {N(rho74, 4)} kg/m³"),
                                  L(f"7.5: T₀ = 500 K, p₀ = 10 atm, p_e = 1 atm cho T_e = T₀(p_e/p₀)^{{(γ−1)/γ}} = {N(Te75, 1)} K và ρ_e = {N(rho75, 3)} kg/m³", f"7.5: T₀ = 500 K, p₀ = 10 atm, p_e = 1 atm gives T_e = T₀(p_e/p₀)^{{(γ−1)/γ}} = {N(Te75, 1)} K and ρ_e = {N(rho75, 3)} kg/m³"),
                                  L("Giảm áp suất thì nhiệt độ và mật độ cũng giảm", "Falling pressure means falling temperature and density too")),
                       "explain": L("Quan hệ đẳng entropi p/ρ^γ = hằng số chỉ dùng được khi không có sóng xung kích hay ma sát giữa hai điểm.", "The isentropic relation p/ρ^γ = constant holds only when there is no shock or friction between the two points.")}]})
    parts.append({"title": L("Sóng xung kích thẳng", "The normal shock wave"),
                  "bullets": [L("Sóng xung kích thẳng chuyển dòng siêu âm thành cận âm", "A normal shock turns a supersonic flow subsonic"),
                              L("Qua sóng: p, ρ, T tăng đột ngột; T₀ không đổi nhưng p₀ giảm", "Across the wave p, ρ, T jump up; T₀ is unchanged but p₀ falls"),
                              L("Quá trình không thuận nghịch: entropi tăng", "The process is irreversible: entropy increases")],
                  "slides": [
                      {"title": L("Các hệ thức và Bài 8.7, 8.8", "The relations and Problems 8.7, 8.8"),
                       "body": ul(L("M₂² = [(γ−1)M₁²+2]/[2γM₁²−(γ−1)]; p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1); ρ₂/ρ₁ = (γ+1)M₁²/[(γ−1)M₁²+2]", "M₂² = [(γ−1)M₁²+2]/[2γM₁²−(γ−1)]; p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1); ρ₂/ρ₁ = (γ+1)M₁²/[(γ−1)M₁²+2]"),
                                  L(f"8.7 (M₁ = 2,6): M₂ = {N(M2_87, 3)}, p₂/p₁ = {N(p_87, 2)}, T₂/T₁ = {N(T_87, 3)}, p₀,₂/p₀,₁ = {N(p02p01_87, 4)}", f"8.7 (M₁ = 2.6): M₂ = {N(M2_87, 3)}, p₂/p₁ = {N(p_87, 2)}, T₂/T₁ = {N(T_87, 3)}, p₀,₂/p₀,₁ = {N(p02p01_87, 4)}"),
                                  L(f"8.8: p₂/p₁ = 10,33 suy ra M₁ = {N(M88, 3)} và T₁ = 1390/{N(normal_shock(M88)[3], 3)} = {N(T1_88, 0)} °R", f"8.8: p₂/p₁ = 10.33 gives M₁ = {N(M88, 3)} and T₁ = 1390/{N(normal_shock(M88)[3], 3)} = {N(T1_88, 0)} °R")),
                       "explain": L("Số tròn M₁ = 3,000 và T₁ = 519 °R (nhiệt độ mực biển chuẩn) cho thấy Bài 8.8 được thiết kế quanh M₁ = 3.", "The round numbers M₁ = 3.000 and T₁ = 519 °R (standard sea-level temperature) show Problem 8.8 was designed around M₁ = 3.")},
                      {"title": L("Entropi và tổn thất áp suất toàn phần (Bài 8.9)", "Entropy and loss of total pressure (Problem 8.9)"),
                       "body": ul(L("s₂ − s₁ = −R ln(p₀,₂/p₀,₁)", "s₂ − s₁ = −R ln(p₀,₂/p₀,₁)"),
                                  L(f"Bài 8.9: Δs = 199,5 J/(kg·K) suy ra p₀,₂/p₀,₁ = e^{{−Δs/R}} = {N(math.exp(-199.5 / R_SI), 4)} và M₁ = {N(M89, 3)}", f"Problem 8.9: Δs = 199.5 J/(kg·K) gives p₀,₂/p₀,₁ = e^{{−Δs/R}} = {N(math.exp(-199.5 / R_SI), 4)} and M₁ = {N(M89, 3)}"),
                                  L("Sóng yếu (M₁ gần 1) gần như thuận nghịch; sóng mạnh làm mất nhiều p₀", "A weak shock (M₁ near 1) is almost reversible; a strong one loses a lot of p₀")),
                       "explain": L("Mất p₀ nghĩa là mất khả năng làm việc của dòng: đó là lý do cửa hút động cơ siêu âm dùng nhiều sóng xiên rồi mới đến một sóng thẳng yếu (module 07).", "Losing p₀ means the flow loses its ability to do work: that is why supersonic engine inlets use several oblique shocks before one weak normal shock (module 07).")}]})
    parts.append({"title": L("Đo vận tốc: ống Pitot siêu âm", "Measuring speed: the supersonic Pitot tube"),
                  "bullets": [L("Cận âm: p₀/p = (1 + 0,2M²)^3,5 (Bài 8.11 ở module 03)", "Subsonic: p₀/p = (1 + 0.2M²)^3.5 (Problem 8.11 in module 03)"),
                              L("Siêu âm: có sóng cung trước ống; đo p₀,₂ sau sóng thẳng, dùng công thức Rayleigh", "Supersonic: a bow shock forms ahead of the tube; the tube reads p₀,₂ behind a normal shock, use the Rayleigh formula"),
                              L("Dùng Bernoulli không nén được cho dòng nén được gây sai lớn", "Using incompressible Bernoulli for compressible flow gives large errors")],
                  "slides": [
                      {"title": L("Bài 8.16: Pitot và áp suất tĩnh thành bên", "Problem 8.16: Pitot and wall static pressure"),
                       "body": ul(L(f"Pitot đọc 1,13 atm, áp suất tĩnh thành bên 0,1 atm: p₀,₂/p₁ = 11,3 suy ra M₁ = {N(M816, 3)}", f"The Pitot tube reads 1.13 atm and wall static pressure 0.1 atm: p₀,₂/p₁ = 11.3 so M₁ = {N(M816, 3)}"),
                                  L("Công thức Rayleigh: p₀,₂/p₁ = [(γ+1)M₁²/2]^{γ/(γ−1)}·[(γ+1)/(2γM₁²−(γ−1))]^{1/(γ−1)}", "Rayleigh formula: p₀,₂/p₁ = [(γ+1)M₁²/2]^{γ/(γ−1)}·[(γ+1)/(2γM₁²−(γ−1))]^{1/(γ−1)}"),
                                  L("Giải ngược M₁ từ tỉ số áp suất cần phương pháp số hoặc bảng", "Solving for M₁ from the pressure ratio needs a numerical method or a table")),
                       "explain": L("M₁ = 2,900 gần như tròn: Bài 8.16 được dựng từ M₁ = 2,9.", "M₁ = 2.900 is almost round: Problem 8.16 was built from M₁ = 2.9.")}]})
    parts.append({"title": L("Ý nghĩa cho bay tốc độ cao", "Meaning for high-speed flight"),
                  "bullets": [L("Số Mach tới hạn là giới hạn bắt đầu có sóng xung kích cục bộ (module 03)", "The critical Mach number marks the onset of local shocks (module 03)"),
                              L("Sóng xung kích sinh lực cản sóng, rung giật và mất mômen nâng đầu", "Shock waves bring wave drag, buffeting and Mach tuck"),
                              L("Cánh xuôi sau trì hoãn các hiệu ứng này", "Sweepback delays these effects")],
                  "slides": [
                      {"title": L("Bài 8.10: sau sóng xung kích mạnh", "Problem 8.10: behind a strong shock"),
                       "body": ul(L(f"M₁ = 3,1, p₁ = 1800 lb/ft², T₁ = 480 °R: M₂ = {N(M2_810, 3)}, T₂ = {N(T2_810, 0)} °R, V₂ = M₂·√(γRT₂) = {N(V2_810, 0)} ft/s", f"M₁ = 3.1, p₁ = 1800 lb/ft², T₁ = 480 °R: M₂ = {N(M2_810, 3)}, T₂ = {N(T2_810, 0)} °R, V₂ = M₂·√(γRT₂) = {N(V2_810, 0)} ft/s"),
                                  L("Dòng sau sóng là cận âm nhưng vẫn rất nóng và nhanh", "The flow behind the wave is subsonic but still very hot and fast"),
                                  L("Đây là lý do cần lớp chịu nhiệt ở mũi các phương tiện siêu âm", "This is why supersonic vehicles need heat protection at the nose")),
                       "explain": L("Trong thực tế, ở M₁ lớn khí không còn nhiệt dung không đổi; mô hình γ = 1,4 chỉ dùng tốt tới khoảng M = 4 hoặc 5.", "In practice at large M₁ the gas no longer has constant specific heats; the γ = 1.4 model works well only up to about M = 4 or 5.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Đại lượng toàn phần và sóng xung kích thẳng", "Total quantities and the normal shock")
    m["formula_math"] = ("T₀/T = 1 + (γ−1)M²/2  ·  p₀/p = (T₀/T)^{γ/(γ−1)}  ·  M₂² = [(γ−1)M₁²+2]/[2γM₁²−(γ−1)]<br>p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1)  ·  s₂−s₁ = −R ln(p₀,₂/p₀,₁)" if lang == "vi" else
                         "T₀/T = 1 + (γ−1)M²/2  ·  p₀/p = (T₀/T)^{γ/(γ−1)}  ·  M₂² = [(γ−1)M₁²+2]/[2γM₁²−(γ−1)]<br>p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1)  ·  s₂−s₁ = −R ln(p₀,₂/p₀,₁)")
    m["legend"] = [("γ", L("tỉ số nhiệt dung 1,4", "specific-heat ratio 1.4")), ("p₀, T₀", L("áp suất và nhiệt độ toàn phần", "total pressure and temperature")), ("M₁, M₂", L("Mach trước và sau sóng", "Mach before and after the wave")), ("Δs", L("tăng entropi (J/(kg·K))", "entropy increase (J/(kg·K))")), ("R", "287 J/(kg·K)"), ("a", L("tốc độ âm thanh √(γRT)", "speed of sound √(γRT)"))]
    m["history_title"] = L("Rankine, Hugoniot và Rayleigh", "Rankine, Hugoniot and Rayleigh")
    m["history"] = L("Các hệ thức sóng xung kích thẳng được William Rankine (1870) và Pierre Hugoniot (1887 đến 1889) rút ra độc lập; công thức Pitot siêu âm mang tên Lord Rayleigh (1910). Anderson trình bày các mốc này trong các mục Historical Note của chương 8 và 9, và nhắc lại rằng bảng nén được của NACA (báo cáo TR-1135) là tài liệu \"kinh thánh\" của người làm khí động tốc độ cao.",
                     "The normal-shock relations were derived independently by William Rankine (1870) and Pierre Hugoniot (1887 to 1889); the supersonic Pitot formula bears the name of Lord Rayleigh (1910). Anderson presents these milestones in the Historical Note sections of chapters 8 and 9, and recalls that the NACA compressible-flow tables (report TR-1135) were the \"bible\" of high-speed aerodynamicists.")
    m["case_title"] = L("Tình huống: đọc Pitot khi bay M 2,9", "Case: reading a Pitot tube at Mach 2.9")
    m["case"] = L(f"Một ống Pitot trong hầm gió siêu âm đọc 1,13 atm trong khi áp suất thành bên là 0,1 atm. Nếu tính như dòng không nén được, V = √(2Δp/ρ) sẽ cho kết quả sai nhiều. Tính đúng bằng công thức Rayleigh cho M₁ = {N(M816, 3)}. Thiết bị phải xét sóng cung trước đầu ống, nếu không số Mach đọc ra sẽ sai. (Bài 8.16, số liệu từ sách.)",
                  f"A Pitot tube in a supersonic wind tunnel reads 1.13 atm while the wall pressure is 0.1 atm. Computing as incompressible flow, V = √(2Δp/ρ) would be badly wrong. The Rayleigh formula gives M₁ = {N(M816, 3)}. The instrument has to account for the bow shock ahead of the tube or the Mach number read would be wrong. (Problem 8.16, data from the book.)")
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L("(1) p₀ giảm qua sóng xung kích nhưng T₀ giữ nguyên. (2) Tỉ số p₀,₂/p₁ (Rayleigh) khác p₀,₂/p₀,₁ (liên hệ qua M₁); Anderson 9.3 và 9.4 nhấn mạnh sai khác này ở sóng xiên. (3) Phải dùng số Mach pháp tuyến M₁ sin β khi dùng bảng sóng thẳng cho sóng xiên. (4) Các công thức giả sử γ = 1,4 và khí lý tưởng nhiệt dung không đổi. (5) Bài 8.8 và 8.16 cho số Mach tròn là dấu hiệu tốt nhưng không thay thế phép tính độc lập.",
                  "(1) p₀ falls across a shock but T₀ stays the same. (2) The ratio p₀,₂/p₁ (Rayleigh) differs from p₀,₂/p₀,₁ (related through M₁); Anderson 9.3 and 9.4 stress this difference for oblique shocks. (3) Use the normal Mach number M₁ sin β when applying normal-shock tables to an oblique shock. (4) The formulas assume γ = 1.4 and a calorically perfect gas. (5) Problems 8.8 and 8.16 giving round Mach numbers is a good sign but not a substitute for an independent calculation.")
    m["nb_desc"] = L("Notebook cài đặt các hệ thức đẳng entropi và sóng thẳng, giải lại Anderson 7.1, 7.4, 7.5, 8.3, 8.5, 8.8, 8.9, 8.10, 8.16, và assert các đáp án quiz.", "The notebook implements the isentropic and normal-shock relations, re-solves Anderson 7.1, 7.4, 7.5, 8.3, 8.5, 8.8, 8.9, 8.10, 8.16, and asserts the quiz answers.")

    SD = lambda i: 600 + i
    SUP = L("Bổ sung (biên soạn)", "Supplementary (authored)")
    def Q(i, src, q, right, wrongs, ex, det=None): return mcq(SD(i), src, q, right, wrongs, ex, det)
    book = [
        Q(1, "Anderson 6th, Problem 7.1", L("Ở mũi tên lửa T₀ = 934 °R và p₀ = 7,8 atm. Mật độ tại điểm này (R = 1716) là:", "At the nose of a missile T₀ = 934 °R and p₀ = 7.8 atm. The density there (R = 1716) is:"), f"{N(rho71, 4)} slug/ft³", [f"{N(rho71 * 7.8, 4)} slug/ft³", f"{N(rho71 / 2.1, 4)} slug/ft³", f"{N(0.002377, 4)} slug/ft³"], L("ρ = p/(RT), 1 atm = 2116 lb/ft².", "ρ = p/(RT), 1 atm = 2116 lb/ft².")),
        Q(2, "Anderson 6th, Problem 7.4", L("Dòng đẳng entropi qua biên dạng: T∞ = 245 K, p∞ = 4,35×10⁴ N/m², tại một điểm p = 3,6×10⁴ N/m². Mật độ tại điểm đó là:", "Isentropic flow over an airfoil: T∞ = 245 K, p∞ = 4.35×10⁴ N/m²; at one point p = 3.6×10⁴ N/m². The density there is:"), f"{N(rho74, 3)} kg/m³", [f"{N(3.6e4 / (287 * 245), 3)} kg/m³", f"{N(rho74 * 1.3, 3)} kg/m³", f"{N(rho74 / 1.3, 3)} kg/m³"], L("ρ = ρ∞(p/p∞)^{1/γ}; ρ∞ = p∞/(RT∞).", "ρ = ρ∞(p/p∞)^{1/γ}; ρ∞ = p∞/(RT∞).")),
        Q(3, "Anderson 6th, Problem 7.5", L("Vòi phun siêu âm đẳng entropi, T₀ = 500 K, p₀ = 10 atm, p ở lối ra = 1 atm. Nhiệt độ ở lối ra là:", "An isentropic supersonic nozzle with T₀ = 500 K, p₀ = 10 atm and exit p = 1 atm. The exit temperature is:"), f"{N(Te75, 1)} K", [f"{N(500 / 10, 1)} K", f"{N(Te75 * 1.4, 1)} K", f"{N(Te75 / 1.4, 1)} K"], L("T = T₀(p/p₀)^{(γ−1)/γ}.", "T = T₀(p/p₀)^{(γ−1)/γ}.")),
        Q(4, "Anderson 6th, Problem 8.3", L("Tại một điểm T = 300 K, p = 1,2 atm, V = 250 m/s. Nhiệt độ toàn phần T₀ là:", "At a point T = 300 K, p = 1.2 atm, V = 250 m/s. The total temperature T₀ is:"), f"{N(T083, 1)} K", [f"{N(T083 + 31, 1)} K", "300 K", f"{N(T083 * 1.4, 1)} K"], L("M = 0,72; T₀ = T(1 + 0,2M²).", "M = 0.72; T₀ = T(1 + 0.2M²)."), L(f"<p>M = V/√(γRT) = {N(M83, 4)}; T₀/T = {N(T0_over_T(M83), 4)}; p₀ = {N(p083, 3)} atm.</p>", f"<p>M = V/√(γRT) = {N(M83, 4)}; T₀/T = {N(T0_over_T(M83), 4)}; p₀ = {N(p083, 3)} atm.</p>")),
        Q(5, "Anderson 6th, Problem 8.5", L("Vòi phun đẳng entropi, buồng thử p = 1 atm, T = 230 K, M = 2. Áp suất buồng chứa p₀ là:", "An isentropic nozzle with test section p = 1 atm, T = 230 K, M = 2. The reservoir pressure p₀ is:"), f"{N(p085, 2)} atm", [f"{N(p085 / 2, 2)} atm", f"{N(1.8, 2)} atm", f"{N(p085 * 2, 2)} atm"], L("p₀/p = (1 + 0,2M²)^3,5 = 7,824.", "p₀/p = (1 + 0.2M²)^3.5 = 7.824.")),
        Q(6, "Anderson 6th, Problem 8.8", L("Trước sóng thẳng p₁ = 1 atm; sau sóng p₂ = 10,33 atm và T₂ = 1390 °R. Số Mach M₁ là:", "Ahead of a normal shock p₁ = 1 atm; behind it p₂ = 10.33 atm and T₂ = 1390 °R. The Mach number M₁ is:"), N(M88, 2), [N(2.0, 2), N(2.6, 2), N(4.0, 2)], L("p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1) = 10,33.", "p₂/p₁ = 1 + 2γ(M₁²−1)/(γ+1) = 10.33."), L(f"<p>M₁² = (10,33−1)(γ+1)/(2γ) + 1 = {N(M88 ** 2, 3)} nên M₁ = {N(M88, 3)}. T₁ = 1390/{N(normal_shock(M88)[3], 3)} = {N(T1_88, 0)} °R.</p>", f"<p>M₁² = (10.33−1)(γ+1)/(2γ) + 1 = {N(M88 ** 2, 3)} so M₁ = {N(M88, 3)}. T₁ = 1390/{N(normal_shock(M88)[3], 3)} = {N(T1_88, 0)} °R.</p>")),
        Q(7, "Anderson 6th, Problem 8.9", L("Entropi tăng qua sóng thẳng là 199,5 J/(kg·K). Số Mach thượng nguồn là:", "The entropy increase across a normal shock is 199.5 J/(kg·K). The upstream Mach number is:"), N(M89, 2), [N(1.5, 2), N(2.0, 2), N(3.0, 2)], L("Δs = −R ln(p₀,₂/p₀,₁), giải số cho M₁.", "Δs = −R ln(p₀,₂/p₀,₁), solved numerically for M₁."), L(f"<p>p₀,₂/p₀,₁ = e^(−199,5/287) = {N(math.exp(-199.5 / 287), 4)}, ứng với M₁ = {N(M89, 4)}.</p>", f"<p>p₀,₂/p₀,₁ = e^(−199.5/287) = {N(math.exp(-199.5 / 287), 4)}, corresponding to M₁ = {N(M89, 4)}.</p>")),
        Q(8, "Anderson 6th, Problem 8.16", L("Hầm gió siêu âm: Pitot đọc 1,13 atm, áp suất tĩnh thành bên 0,1 atm. Số Mach buồng thử là:", "In a supersonic tunnel a Pitot tube reads 1.13 atm and the sidewall static pressure is 0.1 atm. The test-section Mach number is:"), N(M816, 2), [N(0.98, 2), N(2.0, 2), N(3.5, 2)], L("Dùng công thức Rayleigh p₀,₂/p₁ = 11,3.", "Use the Rayleigh formula with p₀,₂/p₁ = 11.3.")),
    ]
    gen = [
        Q(11, SUP, L("Ở M = 2, tỉ số T₀/T bằng:", "At M = 2 the ratio T₀/T is:"), N(1.8, 2), [N(4.0, 2), N(2.0, 2), N(7.82, 2)], L("1 + 0,2 × 4 = 1,8.", "1 + 0.2 × 4 = 1.8.")),
        Q(12, SUP, L("Qua sóng xung kích thẳng, nhiệt độ toàn phần T₀:", "Across a normal shock the total temperature T₀:"), L("không đổi", "stays the same"), [L("tăng", "increases"), L("giảm", "decreases"), L("bằng 0", "becomes zero")], L("Dòng đoạn nhiệt nên T₀ không đổi; p₀ giảm.", "The flow is adiabatic so T₀ is constant; p₀ falls.")),
        Q(13, SUP, L("Số Mach sau sóng xung kích thẳng luôn:", "The Mach number behind a normal shock is always:"), L("nhỏ hơn 1", "less than 1"), [L("lớn hơn 1", "greater than 1"), L("bằng 1", "equal to 1"), L("bằng M₁", "equal to M₁")], L("Sóng thẳng chuyển siêu âm thành cận âm.", "A normal shock turns supersonic flow subsonic.")),
        Q(14, SUP, L("Tốc độ âm thanh ở 300 K (γ = 1,4, R = 287) xấp xỉ:", "The speed of sound at 300 K (γ = 1.4, R = 287) is about:"), f"{N(speed_of_sound(300, 287), 1)} m/s", [f"{N(speed_of_sound(300, 287) * 1.4, 1)} m/s", f"{N(340.3, 1)} m/s", f"{N(300.0, 1)} m/s"], L("a = √(1,4 × 287 × 300) = 347,2.", "a = √(1.4 × 287 × 300) = 347.2.")),
        Q(15, SUP, L("Sóng xung kích thẳng ở M₁ = 1,0 là:", "A normal shock at M₁ = 1.0 is:"), L("sóng có cường độ bằng 0 (sóng âm)", "a wave of zero strength (a sound wave)"), [L("sóng mạnh nhất", "the strongest possible shock"), L("không tồn tại", "impossible"), L("sóng làm M₂ = 0", "a wave giving M₂ = 0")], L("M₂ = 1, p₂/p₁ = 1, không tăng entropi.", "M₂ = 1, p₂/p₁ = 1, no entropy rise.")),
        Q(16, SUP, L("Entropi tăng qua sóng thẳng ở M₁ = 2,6 là Δs = −R ln(p₀,₂/p₀,₁) xấp xỉ:", "The entropy rise across a normal shock at M₁ = 2.6, Δs = −R ln(p₀,₂/p₀,₁), is about:"), f"{N(-R_SI * math.log(p02p01_87), 0)} J/(kg·K)", [f"{N(-R_SI * math.log(p02p01_87) * 3, 0)} J/(kg·K)", f"{N(-R_SI * math.log(p02p01_87) / 3, 0)} J/(kg·K)", "0 J/(kg·K)"], L(f"p₀,₂/p₀,₁ = {N(p02p01_87, 4)}.", f"p₀,₂/p₀,₁ = {N(p02p01_87, 4)}.")),
        Q(17, SUP, L("Vì sao dùng Bernoulli không nén được cho Pitot ở M = 0,82 gây sai lớn?", "Why is incompressible Bernoulli badly wrong for a Pitot tube at M = 0.82?"), L("Vì mật độ thay đổi đáng kể khi dòng bị hãm", "Because density changes significantly as the flow is brought to rest"), [L("Vì độ nhớt tăng", "Because viscosity rises"), L("Vì nhiệt độ giảm", "Because temperature falls"), L("Vì ống Pitot bị tắc", "Because the tube blocks")], L("Anderson 8.13: sai khoảng 9% ở bài 8.11.", "Anderson 8.13: an error of about 9% in problem 8.11.")),
        Q(18, SUP, L("T₀ ở điểm đình trệ của dòng M = 2 ở 230 K là:", "The total temperature at the stagnation point of an M = 2 flow at 230 K is:"), f"{N(T085, 0)} K", [f"{N(230 * 4, 0)} K", f"{N(230 * 2, 0)} K", f"{N(230 * 1.4, 0)} K"], L("T₀ = 230 × 1,8 = 414 K.", "T₀ = 230 × 1.8 = 414 K.")),
    ]
    m["quiz_sets"] = [
        {"key": "anderson", "title": L("Sách 2: Anderson, bài tập cuối chương 7 và 8 (đáp án tính lại bằng Python)", "Book 2: Anderson, end-of-chapter 7 and 8 problems (answers recomputed in Python)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập bổ sung (biên soạn thêm, đáp án tự kiểm chứng bằng tính toán)", "Additional practice (authored, answers self-verified by computation)"), "items": gen},
    ]
    m["problems_intro"] = L("Ba nhóm bài của Anderson giải từng bước; đã đối chiếu Solution Manual bản 4th: các bài 7.1, 7.4, 7.5, 8.3, 8.5, 8.7, 8.8, 8.9, 8.10, 8.11, 8.16 đều khớp (M₁ = 3,0; 2,5 và 2,9 là số tròn).", "Three Anderson problem groups solved step by step; compared with the 4th-edition Solution Manual: problems 7.1, 7.4, 7.5, 8.3, 8.5, 8.7, 8.8, 8.9, 8.10, 8.11 and 8.16 all agree (M₁ = 3.0, 2.5 and 2.9 are round numbers).")
    m["problems"] = [
        {"num": "8.3, 8.5", "src": "Anderson 6th, Problems 8.3, 8.5", "q": L("(8.3) T = 300 K, p = 1,2 atm, V = 250 m/s: tính p₀, T₀. (8.5) Vòi phun: p = 1 atm, T = 230 K, M = 2: tính buồng chứa.", "(8.3) T = 300 K, p = 1.2 atm, V = 250 m/s: find p₀, T₀. (8.5) Nozzle: p = 1 atm, T = 230 K, M = 2: find the reservoir."),
         "ans": L(f"<p>(8.3) a = {N(speed_of_sound(300, 287), 1)} m/s; M = <b>{N(M83, 3)}</b>; T₀ = 300(1 + 0,2M²) = <b>{N(T083, 1)} K</b>; p₀ = 1,2(1 + 0,2M²)^3,5 = <b>{N(p083, 3)} atm</b>.</p><p>(8.5) p₀ = (1 + 0,2·4)^3,5 = <b>{N(p085, 3)} atm</b>; T₀ = 230 × 1,8 = <b>{N(T085, 0)} K</b>.</p>", f"<p>(8.3) a = {N(speed_of_sound(300, 287), 1)} m/s; M = <b>{N(M83, 3)}</b>; T₀ = 300(1 + 0.2M²) = <b>{N(T083, 1)} K</b>; p₀ = 1.2(1 + 0.2M²)^3.5 = <b>{N(p083, 3)} atm</b>.</p><p>(8.5) p₀ = (1 + 0.2·4)^3.5 = <b>{N(p085, 3)} atm</b>; T₀ = 230 × 1.8 = <b>{N(T085, 0)} K</b>.</p>")},
        {"num": "8.8, 8.9", "src": "Anderson 6th, Problems 8.8, 8.9", "q": L("(8.8) p₁ = 1 atm, p₂ = 10,33 atm, T₂ = 1390 °R: tìm M₁, T₁. (8.9) Δs = 199,5 J/(kg·K): tìm M₁.", "(8.8) p₁ = 1 atm, p₂ = 10.33 atm, T₂ = 1390 °R: find M₁, T₁. (8.9) Δs = 199.5 J/(kg·K): find M₁."),
         "ans": L(f"<p>(8.8) M₁ = <b>{N(M88, 3)}</b>; T₂/T₁ = {N(normal_shock(M88)[3], 3)} nên T₁ = <b>{N(T1_88, 0)} °R</b>.</p><p>(8.9) p₀,₂/p₀,₁ = e^(−Δs/R) = {N(math.exp(-199.5 / 287), 4)} nên M₁ = <b>{N(M89, 3)}</b>.</p>", f"<p>(8.8) M₁ = <b>{N(M88, 3)}</b>; T₂/T₁ = {N(normal_shock(M88)[3], 3)} so T₁ = <b>{N(T1_88, 0)} °R</b>.</p><p>(8.9) p₀,₂/p₀,₁ = e^(−Δs/R) = {N(math.exp(-199.5 / 287), 4)} so M₁ = <b>{N(M89, 3)}</b>.</p>")},
        {"num": "8.10, 8.16", "src": "Anderson 6th, Problems 8.10, 8.16", "q": L("(8.10) M₁ = 3,1, T₁ = 480 °R: vận tốc sau sóng. (8.16) Pitot 1,13 atm, tĩnh 0,1 atm: M₁.", "(8.10) M₁ = 3.1, T₁ = 480 °R: the velocity behind the shock. (8.16) Pitot 1.13 atm, static 0.1 atm: M₁."),
         "ans": L(f"<p>(8.10) M₂ = {N(M2_810, 3)}; T₂ = 480×{N(T810, 3)} = {N(T2_810, 0)} °R; V₂ = M₂√(γRT₂) = <b>{N(V2_810, 0)} ft/s</b>.</p><p>(8.16) Rayleigh: p₀,₂/p₁ = 11,3 ⇒ M₁ = <b>{N(M816, 3)}</b>.</p>", f"<p>(8.10) M₂ = {N(M2_810, 3)}; T₂ = 480×{N(T810, 3)} = {N(T2_810, 0)} °R; V₂ = M₂√(γRT₂) = <b>{N(V2_810, 0)} ft/s</b>.</p><p>(8.16) Rayleigh: p₀,₂/p₁ = 11.3 ⇒ M₁ = <b>{N(M816, 3)}</b>.</p>")},
    ]
    return m
