# -*- coding: utf-8 -*-
"""Module 02: Khi dong luc hoc. Nguon: EASA M08 Sub-module 02 (tr.2.1-2.20), Anderson 6th ch.1 (1.5-1.6), ch.3 (3.2-3.4, 3.15-3.16),
ch.4 (4.1-4.9), ch.5 (5.1-5.3); Etkin & Reid 3rd ch.2 (muc 2.2, Phu luc C: MAC). Moi con so tinh trong module nay."""
import math
from aero import *
from common import num, ul, table, mcq


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)
    D = lambda x: x  # giu cho de doc

    # ---- tinh toan ----
    al = math.radians(12)
    cl15 = 1.2 * math.cos(al) - 0.03 * math.sin(al)
    cd15 = 1.2 * math.sin(al) + 0.03 * math.cos(al)
    rho_sl = 1.23
    dp34 = 1.36e4 * 9.81 * 0.1
    V34 = math.sqrt(2 * dp34 / (rho_sl * (1 - 1 / 144)))
    V36 = math.sqrt(2 * (1.07e5 - 1.01e5) / rho_sl)
    cp37 = 1 - (130 / V36) ** 2
    vac33 = 0.5 * rho_sl * 90 ** 2 * (1 / 0.85 ** 2 - 1)
    V32 = math.sqrt(2 * (2116 - 2100) / (0.002377 * (1 / 0.8 ** 2 - 1)))
    G318 = 6 / (rho_sl * 30)
    q41 = 0.5 * 0.002377 * 50 ** 2
    L41 = q41 * 2 * 0.65
    M41 = q41 * 4 * (-0.037)
    cl42 = 1353 / (0.5 * rho_sl * 50 ** 2 * 2)
    cl45 = 2 * math.pi * math.radians(1.5)
    cm45 = -cl45 / 4
    hac = 0.25 - (-0.037 - (-0.045)) / (0.65 - (-0.39))
    r3 = isa(3000)[2]
    q411 = 0.5 * r3 * 60 ** 2
    L411 = q411 * 2 * 0.65
    G412 = L411 / (r3 * 60)

    m = {"num": "02", "slug": "02-aerodynamics", "tag": L("Khí động học", "Aerodynamics")}
    m["title"] = L("Khí động lực học: dòng chảy, biên giới, cánh và các hệ số lực", "Aerodynamics: airflow, boundary layer, wings and force coefficients")
    m["src"] = L("EASA Module 08, Sub-module 02 (tr. 2.1–2.20) · Anderson ch.1, 3, 4, 5 · Etkin &amp; Reid ch.2 mục 2.2 và Phụ lục C",
                 "EASA Module 08, Sub-module 02 (pp. 2.1–2.20) · Anderson ch. 1, 3, 4, 5 · Etkin &amp; Reid ch. 2 sec. 2.2 and Appendix C")
    m["intro"] = L("Module này giải thích vì sao cánh tạo ra lực nâng và lực cản. Ta đi từ chuyển động tương đối, định luật Newton, nguyên lý Bernoulli và lớp biên giới, sang hình học cánh (dây cung, độ cong, tỉ số kích thước, dây cung khí động trung bình), rồi đến các hệ số C_L, C_D, đường cực và tâm áp lực. Phần bài tập lấy từ Anderson: ống Venturi, ống Pitot, cánh NACA 2412 và lý thuyết cánh mỏng.",
                   "This module explains why a wing produces lift and drag. We go from relative motion, Newton's laws, Bernoulli's principle and the boundary layer to wing geometry (chord, camber, aspect ratio, mean aerodynamic chord), then to the coefficients C_L and C_D, the polar and the centre of pressure. The problems come from Anderson: the venturi, the Pitot tube, the NACA 2412 airfoil and thin-airfoil theory.")
    m["mapping"] = {
        "easa": L("Sub-module 02 Aerodynamics (tr. 2.1–2.20): vận tốc, Newton, Bernoulli, lớp biên giới, planform và xoáy, thuật ngữ cánh, biên dạng, T-W-L-D, sinh lực nâng và lực cản, hệ số, AOA, lực cản; 8 câu hỏi cuối chương (Q2-1 đến Q2-8)",
                  "Sub-module 02 Aerodynamics (pp. 2.1–2.20): velocity, Newton, Bernoulli, boundary layer, planform and vortices, wing terms, airfoils, T-W-L-D, generation of lift and drag, coefficients, AOA, drag; 8 end-of-chapter questions (Q2-1 to Q2-8)"),
        "anderson": L("Ch.1 mục 1.5–1.6 (lực, mômen và tâm áp lực); ch.3 mục 3.2–3.4 (Bernoulli, Venturi, Pitot), 3.15–3.16 (Kutta-Joukowski); ch.4 mục 4.2–4.9 (biên dạng, lý thuyết cánh mỏng, tâm khí động); ch.5 mục 5.1–5.3 (cánh hữu hạn, lực cản cảm ứng); Bài 1.5, 3.3, 3.4, 3.6, 3.7, 3.18, 4.2, 4.5, 4.10–4.12",
                      "Ch.1 sec. 1.5–1.6 (forces, moments and centre of pressure); ch.3 sec. 3.2–3.4 (Bernoulli, venturi, Pitot), 3.15–3.16 (Kutta-Joukowski); ch.4 sec. 4.2–4.9 (airfoils, thin-airfoil theory, aerodynamic centre); ch.5 sec. 5.1–5.3 (finite wings, induced drag); Problems 1.5, 3.3, 3.4, 3.6, 3.7, 3.18, 4.2, 4.5, 4.10–4.12"),
        "etkin": L("Ch.2 mục 2.2 Synthesis of Lift and Pitching Moment (tr. 23–29); Phụ lục C Mean Aerodynamic Chord, Mean Aerodynamic Center (tr. 357–363); Bài tập 2.1 tính S, AR, λ và MAC của cánh xuôi sau (cần bản vẽ ba hình chiếu nên không đưa vào quiz)",
                   "Ch.2 sec. 2.2 Synthesis of Lift and Pitching Moment (pp. 23–29); Appendix C Mean Aerodynamic Chord, Mean Aerodynamic Center (pp. 357–363); Exercise 2.1 computing S, AR, taper ratio and MAC of a swept wing (needs a three-view drawing so it is not in the quiz)"),
        "note": L("EASA mô tả định tính. Anderson cho phần toán và hầu hết bài tập số. Etkin dùng lại các hệ số này để xây phương trình ổn định, nên chỉ đối chiếu về mặt khái niệm. Solution Manual của Anderson là bản 4.",
                  "EASA is descriptive. Anderson supplies the mathematics and most of the numeric problems. Etkin reuses the same coefficients to build the stability equations, so the mapping is conceptual only. Anderson's Solution Manual is the 4th edition."),
    }

    parts = []
    parts.append({"title": L("Chuyển động tương đối và định luật Newton", "Relative motion and Newton's laws"),
                  "bullets": [L("Lực tác dụng lên vật như nhau dù vật chuyển động trong không khí đứng yên hay không khí chuyển động qua vật", "The force on a body is the same whether it moves through still air or air moves past it"),
                              L("Tốc độ (speed) khác vận tốc (velocity): vận tốc có hướng", "Speed differs from velocity: velocity has a direction"),
                              L("Ba định luật Newton giải thích tác dụng của không khí lên cánh", "Newton's three laws govern the action of air on a wing")],
                  "slides": [
                      {"title": L("Vận tốc, gia tốc và dòng tự do", "Velocity, acceleration and the free stream"),
                       "body": ul(L("Tốc độ (speed) cho biết vật chuyển động nhanh đến đâu; vận tốc (velocity) là tốc độ kèm hướng", "Speed is the rate of motion in relation to time; velocity is speed with a direction"),
                                  L("Gia tốc là tốc độ thay đổi của vận tốc (dương khi tăng tốc, âm khi giảm tốc)", "Acceleration is the rate of change of velocity (positive when speeding up, negative when slowing)"),
                                  L("Dòng tự do (free stream) là không khí ở xa, chưa bị máy bay làm nhiễu; vận tốc của nó bằng tốc độ bay và áp suất của nó là áp suất tĩnh", "The free stream is air not yet disturbed by the aircraft; its velocity equals the aircraft speed and its pressure is the static pressure"),
                                  L("Tại điểm đình trệ (stagnation point) phía trước cánh, vận tốc bằng không", "At the stagnation point ahead of the wing the velocity is zero")),
                       "explain": L("Nói \"máy bay bay 260 km/h\" chưa cho biết nó đi đâu; nói \"260 km/h về hướng tây nam\" thì có. Trong khí động học, hướng của dòng khí so với cánh mới quyết định lực.", "\"The aircraft flies at 260 km/h\" does not say where it is going; \"260 km/h to the south-west\" does. In aerodynamics it is the direction of the flow relative to the wing that decides the force.")},
                      {"title": L("Ba định luật Newton trong bay", "Newton's three laws in flight"),
                       "body": ul(L("Định luật 1 (quán tính): vật đứng yên hoặc chuyển động đều thẳng giữ nguyên trạng thái nếu không có ngoại lực", "Law 1 (inertia): a body at rest or in uniform straight motion keeps its state unless acted on by an external force"),
                                  L("Định luật 2: thay đổi chuyển động tỉ lệ với lực và cùng hướng với lực (F = ma)", "Law 2: the change of motion is proportional to the force and in the direction of the force (F = ma)"),
                                  L("Định luật 3: mỗi lực có một phản lực bằng và ngược chiều; cánh đẩy không khí xuống thì không khí đẩy cánh lên", "Law 3: every force has an equal and opposite reaction; the wing pushes air down and the air pushes the wing up")),
                       "explain": L("Đáp án EASA câu 3-3: một vật giữ nguyên trạng thái \"cho đến khi bị một lực khác tác động\". Đó là định luật 1.", "EASA answer 3-3: a body keeps its state \"until acted on by some other force\". That is Newton's first law.")}]})
    parts.append({"title": L("Nguyên lý Bernoulli và dòng cận âm", "Bernoulli's principle and subsonic flow"),
                  "bullets": [L("Chất lưu chảy qua chỗ thắt thì tốc độ tăng và áp suất giảm", "Fluid flowing through a constriction speeds up and its pressure drops"),
                              L("Mặt cong của cánh tác dụng lên dòng giống chỗ thắt của ống Venturi", "The curved wing surface acts on the flow like the constriction in a venturi"),
                              L("Chênh lệch áp suất giữa mặt trên và mặt dưới cánh tạo ra lực nâng", "The pressure difference between the upper and lower surfaces produces lift")],
                  "slides": [
                      {"title": L("Bernoulli: p + ½ρV² = hằng số", "Bernoulli: p + ½ρV² = constant"),
                       "body": ul(L("Với dòng không nhớt, không nén được: áp suất tĩnh p cộng áp suất động q = ½ρV² bằng áp suất toàn phần p₀, dọc theo một đường dòng", "For inviscid, incompressible flow, static pressure p plus dynamic pressure q = ½ρV² equals the total pressure p₀ along a streamline"),
                                  L("Đường dòng càng sát nhau thì vận tốc càng cao và áp suất càng thấp; càng thưa thì vận tốc càng thấp", "Streamlines close together mean high velocity and low pressure; far apart means low velocity"),
                                  L("Tại điểm đình trệ, áp suất bằng áp suất toàn phần: lớn hơn áp suất khí quyển đúng một lượng bằng áp suất động", "The stagnation point has the total pressure, larger than atmospheric by the dynamic pressure"),
                                  L("Ống Pitot đo áp suất toàn phần, từ đó suy ra vận tốc", "A Pitot tube measures total pressure, from which the speed follows")),
                       "explain": L("Có thể coi năng lượng của dòng gồm hai phần: phần \"nén\" (p) và phần \"chuyển động\" (½ρV²). Dòng nhanh lên thì phần nén phải giảm đi.", "The flow's energy has a \"squeeze\" part (p) and a \"motion\" part (½ρV²). If the flow speeds up, the squeeze part must fall.")},
                      {"title": L("Ống Venturi, ống Pitot và hầm gió", "Venturi, Pitot tube and wind tunnel"),
                       "body": ul(L(f"Hầm gió tỉ số diện tích 12, chênh áp 10 cm thủy ngân: V = {N(V34, 1)} m/s (Anderson 3.4)", f"A wind tunnel with area ratio 12 and a 10 cm mercury pressure difference: V = {N(V34, 1)} m/s (Anderson 3.4)"),
                                  L(f"Ống Pitot trên máy bay đọc 1,07×10⁵ N/m² ở mực biển: V = {N(V36, 1)} m/s (Anderson 3.6)", f"A Pitot tube on an aircraft reads 1.07×10⁵ N/m² at sea level: V = {N(V36, 1)} m/s (Anderson 3.6)"),
                                  L(f"Venturi có tỉ số diện tích họng 0,85 trong dòng 90 m/s tạo chân không tối đa {N(vac33, 0)} N/m² (Anderson 3.3)", f"A venturi with a 0.85 throat area ratio in a 90 m/s stream creates a maximum vacuum of {N(vac33, 0)} N/m² (Anderson 3.3)"),
                                  L("Bernoulli chỉ dùng được khi dòng còn bám bề mặt; dòng đã tách thì không còn áp dụng (EASA)", "Bernoulli holds only while the flow stays attached; once it separates it no longer applies (EASA)")),
                       "explain": L("Cả ba ví dụ dùng cùng một phương trình, chỉ khác phần nào đã biết và phần nào cần tìm.", "All three examples use the same equation; only what is known and what is unknown change.")}]})
    parts.append({"title": L("Lớp biên giới và ma sát", "Boundary layer and friction"),
                  "bullets": [L("Lớp biên giới là phần không khí sát bề mặt máy bay", "The boundary layer is the air closest to the aircraft surface"),
                              L("Do độ nhớt, tại bề mặt vận tốc gần bằng không", "Because of viscosity, velocity at the surface is nearly zero"),
                              L("Lớp tầng chuyển thành lớp rối rồi có thể tách khỏi bề mặt", "A laminar layer becomes turbulent and may then separate from the surface")],
                  "slides": [
                      {"title": L("Lớp tầng, lớp rối và sự tách dòng", "Laminar, turbulent and separated flow"),
                       "body": ul(L("Lớp biên giới tầng: các lớp khí trượt đều đặn, ma sát nhỏ nhưng dễ tách", "Laminar boundary layer: smooth sliding layers, low friction but easily separated"),
                                  L("Lớp biên giới rối: dày hơn, nhanh hơn, ma sát lớn hơn nhưng bám bề mặt tốt hơn", "Turbulent boundary layer: thicker, faster, more friction but clings better to the surface"),
                                  L("Dòng tách khỏi cánh tạo ra vùng xoáy rối không sinh lực nâng; đó là nguyên nhân của hiện tượng thất tốc (stall)", "Flow that separates from the wing makes turbulence that produces no lift; this is the origin of the stall"),
                                  L("Ma sát da (skin friction) là phần lực cản do độ nhớt trong lớp biên giới", "Skin friction is the drag due to viscosity within the boundary layer")),
                       "explain": L("Quả bóng golf có các lõm nhỏ để cố tình làm lớp biên giới rối, giúp dòng bám lâu hơn phía sau và giảm lực cản chung.", "A golf ball has dimples to make the boundary layer turbulent on purpose, so the flow clings longer behind the ball and total drag falls.")}]})
    parts.append({"title": L("Hình học cánh và thuật ngữ", "Wing geometry and terminology"),
                  "bullets": [L("Biên dạng (airfoil): dây cung, độ cong, độ dày", "Airfoil: chord, camber, thickness"),
                              L("Tỉ số kích thước (aspect ratio) = sải cánh / dây cung", "Aspect ratio = span / chord"),
                              L("Xoáy đầu cánh sinh ra do chênh áp giữa hai mặt cánh", "Wing-tip vortices come from the pressure difference between the two wing surfaces")],
                  "slides": [
                      {"title": L("Các thuật ngữ cánh trong đề cương", "Wing terms in the syllabus"),
                       "body": table([L("Thuật ngữ", "Term"), L("Ý nghĩa", "Meaning")],
                                     [[L("Chord (dây cung)", "Chord"), L("khoảng cách từ mép trước đến mép sau cánh (EASA 2-4 gọi là bề rộng cánh)", "distance from leading to trailing edge (EASA 2-4 calls it the width of the wing)")],
                                      [L("Camber (độ cong)", "Camber"), L("độ cong của đường trung bình biên dạng", "curvature of the mean line of the airfoil")],
                                      [L("Aspect ratio (AR)", "Aspect ratio (AR)"), L("sải cánh / dây cung; với cánh bất kỳ AR = b²/S", "span / chord; for any wing AR = b²/S")],
                                      [L("MAC", "MAC"), L("dây cung khí động trung bình: dây cung của một cánh chữ nhật tương đương", "mean aerodynamic chord, the chord of an equivalent rectangular wing")],
                                      [L("Wash-in / wash-out", "Wash-in / wash-out"), L("góc đặt cánh tăng / giảm dần về phía đầu cánh", "wing incidence increasing / decreasing towards the tip")],
                                      [L("Fineness ratio", "Fineness ratio"), L("tỉ số chiều dài trên đường kính lớn nhất của thân", "ratio of body length to maximum diameter")]]),
                       "explain": L("Cánh dài, hẹp (AR cao) như tàu lượn có lực cản cảm ứng thấp; cánh ngắn, rộng (AR thấp) như máy bay chiến đấu thì ngược lại.", "A long, narrow wing (high AR) like a glider has low induced drag; a short, broad wing (low AR) like a fighter has the opposite.")},
                      {"title": L("Xoáy đầu cánh, upwash, downwash và nhiễm bẩn biên dạng", "Tip vortices, upwash, downwash and airfoil contamination"),
                       "body": ul(L("Không khí áp suất cao dưới cánh trào vòng qua đầu cánh lên mặt trên và tạo thành xoáy; xoáy kéo theo luồng khí đi xuống (downwash) phía sau cánh", "High pressure under the wing leaks round the tip to the upper side and forms a vortex; vortices cause downwash behind the wing"),
                                  L("Upwash là luồng đi lên ngay phía trước cánh khi cánh nghiêng so với dòng", "Upwash is the upward flow just ahead of the wing when it is tilted to the stream"),
                                  L("Băng, tuyết, sương giá bám lên cánh làm thô bề mặt, giảm lực nâng và tăng lực cản; phải loại bỏ trước khi bay (EASA tr. 2.9)", "Ice, snow and frost on the wing roughen the surface, cut lift and raise drag; they must be removed before flight (EASA p. 2.9)")),
                       "explain": L("Chính downwash sinh ra lực cản cảm ứng: cánh \"thấy\" dòng khí bị hướng xuống, nên vectơ lực nâng nghiêng ra sau một chút.", "Downwash is the source of induced drag: the wing \"sees\" a downward-tilted flow, so its lift vector tilts slightly backwards.")}]})
    parts.append({"title": L("Lực nâng, lực cản và hệ số", "Lift, drag and coefficients"),
                  "bullets": [L("L = ½ρV²·S·C_L và D = ½ρV²·S·C_D", "L = ½ρV²·S·C_L and D = ½ρV²·S·C_D"),
                              L("Góc tấn (AOA) là góc giữa dây cung và gió tương đối", "The angle of attack (AOA) is the angle between the chord line and the relative wind"),
                              L("Lực cản gồm lực cản ký sinh (parasite) và lực cản cảm ứng (induced)", "Drag is parasite drag plus induced drag")],
                  "slides": [
                      {"title": L("Hệ số lực nâng và đường cong C_L theo góc tấn", "Lift coefficient and the C_L versus angle curve"),
                       "body": ul(L("Lực nâng tỉ lệ với bình phương tốc độ: máy bay bay 200 kt có lực nâng gấp bốn lần ở 100 kt (EASA)", "Lift is proportional to speed squared: an aircraft at 200 kt has four times the lift at 100 kt (EASA)"),
                                  L(f"Lý thuyết cánh mỏng đối xứng: c_l = 2πα; ở α = 1,5° cho c_l = {N(cl45, 3)} và c_m,LE = −c_l/4 = {N(cm45, 4)} (Anderson 4.5)", f"Thin symmetric airfoil theory: c_l = 2πα; at α = 1.5° it gives c_l = {N(cl45, 3)} and c_m,LE = −c_l/4 = {N(cm45, 4)} (Anderson 4.5)"),
                                  L(f"NACA 2412 với c = 2 m, V = 50 m/s, ρ = 1,23 kg/m³ và L′ = 1353 N/m cho c_l = {N(cl42, 2)}, tức góc tấn khoảng 2° (Anderson 4.2)", f"A NACA 2412 with c = 2 m, V = 50 m/s, ρ = 1.23 kg/m³ and L′ = 1353 N/m gives c_l = {N(cl42, 2)}, i.e. an angle of attack of about 2° (Anderson 4.2)"),
                                  L("Vượt quá một góc tới hạn, dòng tách ra và C_L giảm: đó là thất tốc", "Beyond a critical angle the flow separates and C_L falls: the stall")),
                       "explain": L("C_L giúp so sánh công bằng: với cùng một hình dạng cánh, C_L cho biết cánh \"hiệu quả\" đến đâu, dù máy bay to hay nhỏ, nhanh hay chậm.", "C_L makes comparison fair: for one wing shape it tells how \"effective\" the wing is, whether the aircraft is big or small, fast or slow.")},
                      {"title": L("Lực cản, đường cực và tâm khí động", "Drag, the polar and the aerodynamic centre"),
                       "body": ul(L("Lực cản ký sinh gồm lực cản hình dạng, ma sát da và nhiễu (interference, EASA 2-7); nó tăng liên tục theo tốc độ", "Parasite drag includes form drag, skin friction and interference (EASA 2-7); it increases continuously with speed"),
                                  L("Lực cản cảm ứng C_Di = C_L²/(π e AR) giảm khi tốc độ tăng và khi AR lớn", "Induced drag C_Di = C_L²/(π e AR) falls as speed rises and as AR grows"),
                                  L("Đường cực là đồ thị C_L theo C_D; tiếp tuyến từ gốc cho L/D lớn nhất", "The polar plots C_L against C_D; the tangent from the origin gives the maximum L/D"),
                                  L(f"Tâm khí động NACA 2412 nằm ở x/c = {N(hac, 3)}, rất gần điểm một phần tư dây cung (Anderson 4.10)", f"The NACA 2412 aerodynamic centre is at x/c = {N(hac, 3)}, very near the quarter chord (Anderson 4.10)")),
                       "explain": L("Hai loại lực cản thay phiên nhau trội hơn: bay chậm thì lực cản cảm ứng lớn, bay nhanh thì lực cản ký sinh lớn, nên tổng lực cản nhỏ nhất ở một tốc độ nhất định.", "Each drag dominates in turn: slow flight has large induced drag, fast flight large parasite drag, so total drag is lowest at one particular speed.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Bernoulli, hệ số lực và lực cản cảm ứng", "Bernoulli, force coefficients and induced drag")
    m["formula_math"] = ("p + ½ρV² = p₀  ·  L = ½ρV²S·C_L  ·  D = ½ρV²S·C_D  ·  AR = b²/S<br>c_l = 2πα (cánh mỏng)  ·  C_Di = C_L²/(π e AR)  ·  Γ = L′/(ρV)" if lang == "vi" else
                         "p + ½ρV² = p₀  ·  L = ½ρV²S·C_L  ·  D = ½ρV²S·C_D  ·  AR = b²/S<br>c_l = 2πα (thin airfoil)  ·  C_Di = C_L²/(π e AR)  ·  Γ = L′/(ρV)")
    m["legend"] = [("q", L("áp suất động ½ρV²", "dynamic pressure ½ρV²")), ("S", L("diện tích cánh", "wing area")), ("C_L, C_D", L("hệ số lực nâng, lực cản", "lift and drag coefficients")),
                   ("AR", L("tỉ số kích thước", "aspect ratio")), ("e", L("hệ số hiệu suất sải cánh", "span efficiency factor")), ("Γ", L("lưu số quanh cánh", "circulation around the wing"))]
    m["history_title"] = L("Bernoulli, Prandtl và hiểu lực nâng", "Bernoulli, Prandtl and understanding lift")
    m["history"] = L("Daniel Bernoulli công bố mối quan hệ giữa áp suất và vận tốc trong Hydrodynamica (1738). Năm 1904, Ludwig Prandtl đề xuất khái niệm lớp biên giới, giải thích vì sao có lực cản ma sát và sự tách dòng. Sau đó, Lanchester, Kutta, Joukowski và Prandtl xây dựng lý thuyết lưu số và lý thuyết cánh hữu hạn. Anderson ghi lại các mốc này trong các mục Historical Note ở chương 3, 4 và 5.",
                     "Daniel Bernoulli published the pressure-velocity relation in Hydrodynamica (1738). Ludwig Prandtl introduced the boundary layer in 1904, explaining skin friction and flow separation. Lanchester, Kutta, Joukowski and Prandtl then built circulation theory and finite-wing theory; Anderson records these milestones in the Historical Note sections of chapters 3, 4 and 5.")
    m["case_title"] = L("Tình huống: lực nâng của một cánh nhỏ (minh họa)", "Case: lift of a small wing (illustrative)")
    S_ex, V_ex, CL_ex = 16.0, 50.0, 0.65
    L_ex = 0.5 * RHO0 * V_ex ** 2 * S_ex * CL_ex
    L_ex2 = 0.5 * RHO0 * (2 * V_ex) ** 2 * S_ex * CL_ex
    m["case"] = L(ul(f"Cánh giả định có S = 16 m², bay 50 m/s ở mực biển ISA (ρ = 1,225 kg/m³), C_L = 0,65. Lực nâng L = ½ρV²SC_L = {N(L_ex, 0)} N, đủ nâng khoảng {N(L_ex / 9.80665, 0)} kg.",
                  f"Tăng tốc gấp đôi lên 100 m/s, giữ nguyên C_L: L = {N(L_ex2, 0)} N, gấp bốn lần. Đây đúng là ví dụ 100 kt và 200 kt trong EASA.",
                  "Số liệu chỉ để minh họa; cách tính dựa trên Bernoulli và định nghĩa của C_L."),
                  ul(f"A hypothetical wing with S = 16 m² flies at 50 m/s at ISA sea level (ρ = 1.225 kg/m³) with C_L = 0.65. Its lift is L = ½ρV²SC_L = {N(L_ex, 0)} N, enough to lift about {N(L_ex / 9.80665, 0)} kg.",
                  f"Double the speed to 100 m/s at the same C_L and L = {N(L_ex2, 0)} N, four times as much. This is the 100 kt versus 200 kt example in EASA.",
                  "The numbers are only illustrative; the method rests on Bernoulli and the definition of C_L."))
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L(ul("\"Hai phần khí đi qua cánh phải gặp nhau cùng lúc ở mép sau\" là quan niệm sai. Bernoulli cho quan hệ giữa áp suất và vận tốc, không đòi hỏi thời gian đi qua hai mặt cánh phải bằng nhau.",
                  "Theo EASA, khoảng ba phần tư lực nâng đến từ vùng áp suất thấp ở mặt trên. Đó là con số của giáo trình EASA, không phải hằng số vật lý.",
                  "Bernoulli (dòng không nhớt) không dùng được khi dòng đã tách.",
                  "Dây cung (chord) là kích thước dọc theo dòng, không phải sải cánh. Tỉ số kích thước AR = sải cánh / dây cung.",
                  "Bài Anderson 4.1 và 4.2 dùng số liệu c_l trong bảng NACA 2412. Cùng một biên dạng, lấy ρ = 1,23 hay 1,225 sẽ cho kết quả hơi khác, nên đọc kỹ giả thiết của đề trước khi so đáp án."),
                  ul("\"The two air parcels must meet at the trailing edge at the same time\" is a misconception. Bernoulli relates pressure and velocity; it does not require equal transit times over the two surfaces.",
                  "EASA says about three quarters of the lift comes from the low pressure on the upper surface. That is the EASA text's figure, not a physical constant.",
                  "Bernoulli (inviscid flow) does not apply once the flow has separated.",
                  "Chord is the dimension along the stream, not the span. Aspect ratio is span / chord.",
                  "Anderson 4.1 and 4.2 use the NACA 2412 table. For the same airfoil, ρ = 1.23 or 1.225 gives slightly different results, so read the stated assumptions before comparing answers."))
    m["nb_desc"] = L("Notebook giải lại các bài Anderson 1.5, 3.3, 3.4, 3.6, 3.7, 3.18, 4.2, 4.5, 4.10, 4.11, 4.12, vẽ đường cong C_L theo góc tấn của NACA 2412 và đường cực, rồi dùng assert để kiểm mọi đáp án quiz.",
                     "The notebook re-solves Anderson 1.5, 3.3, 3.4, 3.6, 3.7, 3.18, 4.2, 4.5, 4.10, 4.11 and 4.12, plots the NACA 2412 C_L versus angle curve and a polar, then uses assert to check every quiz answer.")

    SD = lambda i: 200 + i
    SRC = lambda q, p1, p2: L(f"EASA M08 Q2-{q} (tr. {p1}, đáp án tr. {p2})", f"EASA M08 Q2-{q} (p. {p1}, answer p. {p2})")
    easa = [
        mcq(SD(1), SRC(1, "2.19", "2.20"), L("____ là tốc độ chuyển động theo một hướng nhất định.", "____ is the rate of motion in a particular direction in relation to time."),
            L("Vận tốc (velocity)", "Velocity"), [L("Tốc độ vô hướng (speed)", "Speed"), L("Gia tốc (acceleration)", "Acceleration"), L("Quán tính (inertia)", "Inertia")],
            L("Vận tốc là tốc độ kèm hướng; EASA phân biệt rõ với speed.", "Velocity is speed with a direction; EASA distinguishes it clearly from speed.")),
        mcq(SD(2), SRC(2, "2.19", "2.20"), L("Khi chất lưu chảy trong ống qua chỗ thắt, tốc độ của chất lưu ____ và áp suất của chất lưu ____.", "When fluid flowing through a tube reaches a constriction, the speed of the fluid ____ and the pressure of the fluid ____."),
            L("tăng; giảm", "increases; decreases"), [L("giảm; tăng", "decreases; increases"), L("tăng; tăng", "increases; increases"), L("giảm; giảm", "decreases; decreases")],
            L("Đây là nguyên lý Bernoulli (EASA tr. 2.3).", "This is Bernoulli's principle (EASA p. 2.3).")),
        mcq(SD(3), SRC(3, "2.19", "2.20"), L("Lớp biên giới là phần dòng khí ____ bề mặt máy bay.", "The boundary layer is the part of the airflow that is ____ to the surface of the aircraft."),
            L("gần nhất", "closest"), [L("xa nhất", "farthest"), L("vuông góc", "perpendicular"), L("song song và cách xa", "parallel and distant")],
            L("Lớp biên giới là phần dòng khí sát bề mặt (EASA tr. 2.4).", "The boundary layer is the air closest to the surface (EASA p. 2.4).")),
        mcq(SD(4), SRC(4, "2.19", "2.20"), L("____ của cánh là bề rộng của cánh từ đỉnh mép trước đến mép sau.", "The ____ of a wing is the width of the wing from the leading edge apex to the trailing edge."),
            L("dây cung (chord)", "chord"), [L("sải cánh (span)", "span"), L("độ cong (camber)", "camber"), L("tỉ số kích thước (aspect ratio)", "aspect ratio")],
            L("Sải cánh là chiều dài từ đầu cánh này đến đầu cánh kia, dây cung là chiều dọc dòng.", "Span runs tip to tip; the chord runs along the stream.")),
        mcq(SD(5), SRC(5, "2.19", "2.20"), L("Phép so sánh giữa sải cánh và dây cung của cánh gọi là ____.", "A comparison between the wingspan and the chord of a wing is known as ____."),
            L("tỉ số kích thước (aspect ratio)", "aspect ratio"), [L("tỉ số thon (taper ratio)", "taper ratio"), L("tỉ số mảnh (fineness ratio)", "fineness ratio"), L("tỉ số lực nâng/cản", "lift-to-drag ratio")],
            L("AR = sải cánh / dây cung = b²/S.", "AR = span / chord = b²/S.")),
        mcq(SD(6), SRC(6, "2.19", "2.20"), L("____ được định nghĩa là góc giữa dây cung của cánh và hướng gió tương đối.", "____ is defined as the angle between the chord line of the wing and the direction of the relative wind."),
            L("Góc tấn (AOA)", "Angle of attack (AOA)"), [L("Góc đặt cánh (incidence)", "Angle of incidence"), L("Góc chữ V ngang (dihedral)", "Dihedral angle"), L("Góc xuôi (sweepback)", "Sweepback angle")],
            L("AOA đo so với gió tương đối, còn góc đặt cánh đo so với trục thân.", "AOA is measured against the relative wind, while incidence is measured against the fuselage datum.")),
        mcq(SD(7), SRC(7, "2.19", "2.20"), L("Lực cản ____ sinh ra do dòng khí trộn lẫn giữa các bộ phận khung máy bay như cánh và thân.", "____ drag is generated by the mixing of airflow streamlines between airframe components such as the wing and fuselage."),
            L("nhiễu (interference)", "Interference"), [L("cảm ứng (induced)", "Induced"), L("sóng (wave)", "Wave"), L("ma sát da (skin friction)", "Skin friction")],
            L("Hai chi tiết giao nhau (cánh-thân) sinh thêm lực cản nhiễu.", "Two components meeting (wing-fuselage) add interference drag.")),
        mcq(SD(8), SRC(8, "2.19", "2.20"), L("Loại lực cản nào tăng liên tục khi tốc độ bay tăng?", "What type of drag continually increases as airspeed increases?"),
            L("Lực cản ký sinh (parasite drag)", "Parasite drag"), [L("Lực cản cảm ứng (induced drag)", "Induced drag"), L("Lực cản đáy (base drag)", "Base drag"), L("Không loại nào", "None of them")],
            L("Lực cản cảm ứng giảm khi tốc độ tăng; lực cản ký sinh tăng.", "Induced drag falls with speed; parasite drag rises.")),
    ]
    book = [
        mcq(SD(11), "Anderson 6th, Problem 1.5",
            L("Biên dạng ở góc tấn 12° có hệ số lực pháp tuyến 1,2 và lực dọc trục 0,03. Hệ số lực nâng là:", "An airfoil at 12° angle of attack has normal and axial force coefficients of 1.2 and 0.03. The lift coefficient is:"),
            N(cl15, 3), [N(cd15, 3), N(1.2 * math.cos(al) + 0.03 * math.sin(al), 3), N(1.2, 3)],
            L("c_l = c_n cos α − c_a sin α.", "c_l = c_n cos α − c_a sin α."),
            L(f"<p>c_l = 1,2 cos 12° − 0,03 sin 12° = {N(cl15, 3)}; c_d = 1,2 sin 12° + 0,03 cos 12° = {N(cd15, 3)}. Dấu của số hạng thứ hai là chỗ dễ nhầm.</p>", f"<p>c_l = 1.2 cos 12° − 0.03 sin 12° = {N(cl15, 3)}; c_d = 1.2 sin 12° + 0.03 cos 12° = {N(cd15, 3)}. The sign of the second term is the usual slip.</p>")),
        mcq(SD(12), "Anderson 6th, Problem 3.4",
            L("Hầm gió hở tốc độ thấp, tỉ số diện tích đầu vào/họng = 12, áp kế thủy ngân chênh 10 cm (ρ_Hg = 1,36×10⁴ kg/m³, ρ = 1,23 kg/m³). Vận tốc trong buồng thử là:", "A low-speed open-circuit wind tunnel has an inlet-to-throat area ratio of 12 and a mercury manometer difference of 10 cm (ρ_Hg = 1.36×10⁴ kg/m³, ρ = 1.23 kg/m³). The test-section velocity is:"),
            f"{N(V34, 1)} m/s", [f"{N(V34 / 12, 1)} m/s", f"{N(V34 * 1.4, 1)} m/s", f"{N(V34 / 1.4, 1)} m/s"],
            L("Bernoulli kết hợp liên tục: Δp = ½ρV₂²(1 − 1/144).", "Bernoulli with continuity: Δp = ½ρV₂²(1 − 1/144)."),
            L(f"<p>Δp = ρ_Hg g h = {N(dp34, 0)} N/m²; V₂ = √[2Δp/(ρ(1 − (A₂/A₁)²))] = {N(V34, 1)} m/s. Bỏ hệ số (1 − 1/144) chỉ đổi kết quả khoảng 0,35%.</p>", f"<p>Δp = ρ_Hg g h = {N(dp34, 0)} N/m²; V₂ = √[2Δp/(ρ(1 − (A₂/A₁)²))] = {N(V34, 1)} m/s. Dropping the (1 − 1/144) factor changes the result by only about 0.35%.</p>")),
        mcq(SD(13), "Anderson 6th, Problem 3.6",
            L("Ống Pitot trên máy bay ở mực biển chuẩn (p = 1,01×10⁵ N/m², ρ = 1,23 kg/m³) đọc 1,07×10⁵ N/m². Tốc độ máy bay là:", "A Pitot tube on an aircraft at standard sea level (p = 1.01×10⁵ N/m², ρ = 1.23 kg/m³) reads 1.07×10⁵ N/m². The aircraft speed is:"),
            f"{N(V36, 1)} m/s", [f"{N(V36 ** 2 / 100, 1)} m/s", f"{N(V36 * 1.414, 1)} m/s", f"{N(V36 / 1.414, 1)} m/s"],
            L("V = √[2(p₀ − p)/ρ].", "V = √[2(p₀ − p)/ρ]."),
            L(f"<p>V = √[2(1,07×10⁵ − 1,01×10⁵)/1,23] = √[{N(2 * 6000 / 1.23, 0)}] = {N(V36, 1)} m/s ≈ {N(V36 * 1.944, 0)} kt. Lỗi hay gặp là quên hệ số 2 hoặc quên căn bậc hai.</p>", f"<p>V = √[2(1.07×10⁵ − 1.01×10⁵)/1.23] = √[{N(2 * 6000 / 1.23, 0)}] = {N(V36, 1)} m/s ≈ {N(V36 * 1.944, 0)} kt. Typical slips are forgetting the factor 2 or the square root.</p>")),
        mcq(SD(14), "Anderson 6th, Problem 3.7",
            L("Tại một điểm trên cánh của máy bay ở bài 3.6, vận tốc cục bộ là 130 m/s. Hệ số áp suất C_p tại đó là:", "At a point on the wing of the aircraft in Problem 3.6 the local velocity is 130 m/s. The pressure coefficient C_p there is:"),
            N(cp37, 3), [N(-cp37, 3), N(1 - (V36 / 130) ** 2, 3), N((130 / V36) ** 2, 3)],
            L("C_p = 1 − (V/V∞)².", "C_p = 1 − (V/V∞)²."),
            L(f"<p>C_p = 1 − (130/{N(V36, 2)})² = {N(cp37, 3)}. Âm nghĩa là áp suất thấp hơn áp suất dòng tự do, đúng với mặt hút của cánh.</p>", f"<p>C_p = 1 − (130/{N(V36, 2)})² = {N(cp37, 3)}. Negative means pressure below the free stream, as expected on a suction surface.</p>")),
        mcq(SD(15), "Anderson 6th, Problem 4.2",
            L("Cánh NACA 2412 dây cung 2 m, V = 50 m/s ở mực biển chuẩn, lực nâng trên đơn vị sải 1353 N/m (ρ = 1,23). Hệ số lực nâng và góc tấn (theo bảng c_l của NACA 2412 ở bài 1.6) là:", "A NACA 2412 airfoil with a 2 m chord at 50 m/s at standard sea level has a lift per unit span of 1353 N/m (ρ = 1.23). The lift coefficient and angle of attack (from the NACA 2412 c_l table of Problem 1.6) are:"),
            f"c_l = {N(cl42, 2)}, α = 2°", [f"c_l = {N(cl42, 2)}, α = 4°", f"c_l = {N(cl42 * 2, 2)}, α = 4°", f"c_l = {N(cl42 / 2, 2)}, α = 0°"],
            L("c_l = L′/(q c), rồi đọc α từ bảng.", "c_l = L′/(q c), then read α from the table."),
            L(f"<p>q = ½(1,23)(50²) = 1537,5 N/m²; c_l = 1353/(1537,5×2) = {N(cl42, 2)}. Bảng NACA 2412: α = 2° cho c_l = 0,44.</p>", f"<p>q = ½(1.23)(50²) = 1537.5 N/m²; c_l = 1353/(1537.5×2) = {N(cl42, 2)}. NACA 2412 table: α = 2° gives c_l = 0.44.</p>")),
        mcq(SD(16), "Anderson 6th, Problem 4.5",
            L("Biên dạng mỏng đối xứng ở góc tấn 1,5°. Theo lý thuyết cánh mỏng, c_l và c_m,LE lần lượt là:", "A thin symmetric airfoil at 1.5° angle of attack. From thin-airfoil theory c_l and c_m,LE are respectively:"),
            f"{N(cl45, 4)} ; {N(cm45, 4)}", [f"{N(cl45 / 2, 4)} ; {N(-cl45 / 2, 4)}", f"{N(cl45, 4)} ; {N(-cl45 / 2, 4)}", f"{N(cl45 * 1.5, 4)} ; {N(cm45, 4)}"],
            L("c_l = 2πα (α tính bằng radian), c_m,LE = −c_l/4.", "c_l = 2πα (α in radians), c_m,LE = −c_l/4."),
            L(f"<p>α = 1,5° = {N(math.radians(1.5), 5)} rad nên c_l = 2π·α = {N(cl45, 4)}. Tâm áp lực của cánh mỏng đối xứng ở x = c/4 nên c_m,LE = −c_l/4 = {N(cm45, 4)}.</p>", f"<p>α = 1.5° = {N(math.radians(1.5), 5)} rad so c_l = 2π·α = {N(cl45, 4)}. The centre of pressure of a thin symmetric airfoil is at c/4, so c_m,LE = −c_l/4 = {N(cm45, 4)}.</p>")),
        mcq(SD(17), "Anderson 6th, Problem 4.10",
            L("NACA 2412: ở α = −6° có c_l = −0,39 và c_m,c/4 = −0,045; ở α = 4° có c_l = 0,65 và c_m,c/4 = −0,037. Vị trí tâm khí động x_ac/c là:", "NACA 2412: at α = −6° c_l = −0.39 and c_m,c/4 = −0.045; at α = 4° c_l = 0.65 and c_m,c/4 = −0.037. The aerodynamic centre x_ac/c is:"),
            N(hac, 3), [N(0.25, 3), N(0.300, 3), N(0.200, 3)],
            L("h_ac = 0,25 − dc_m,c/4/dc_l.", "h_ac = 0.25 − dc_m,c/4/dc_l."),
            L(f"<p>dc_m/dc_l = (−0,037 + 0,045)/(0,65 + 0,39) = 0,00769; h_ac = 0,25 − 0,00769 = {N(hac, 4)}. Tâm khí động gần như ở một phần tư dây cung.</p>", f"<p>dc_m/dc_l = (−0.037 + 0.045)/(0.65 + 0.39) = 0.00769; h_ac = 0.25 − 0.00769 = {N(hac, 4)}. The aerodynamic centre is almost at the quarter chord.</p>")),
        mcq(SD(18), "Anderson 6th, Problem 4.11",
            L("Cánh NACA 2412 dây cung 2 m bay 60 m/s ở độ cao chuẩn 3 km (ρ ≈ 0,909 kg/m³) với α = 4° (c_l = 0,65). Lực nâng trên đơn vị sải là:", "A NACA 2412 airfoil of 2 m chord flies at 60 m/s at a standard altitude of 3 km (ρ ≈ 0.909 kg/m³) with α = 4° (c_l = 0.65). The lift per unit span is:"),
            f"{N(L411, 0)} N/m", [f"{N(L411 * 1.225 / 0.9093, 0)} N/m", f"{N(L411 / 2, 0)} N/m", f"{N(L411 * 2, 0)} N/m"],
            L("L′ = ½ρV²·c·c_l.", "L′ = ½ρV²·c·c_l."),
            L(f"<p>ρ(3 km) = {N(r3, 4)} kg/m³ từ ISA; q = {N(q411, 1)} N/m²; L′ = {N(q411, 1)}×2×0,65 = {N(L411, 0)} N/m. Dùng mật độ mực biển thay cho 3 km làm kết quả lệch khoảng 35%.</p>", f"<p>ρ(3 km) = {N(r3, 4)} kg/m³ from ISA; q = {N(q411, 1)} N/m²; L′ = {N(q411, 1)}×2×0.65 = {N(L411, 0)} N/m. Using sea-level density instead of 3 km density shifts the result by about 35%.</p>")),
    ]
    SUP = L("Câu luyện thêm", "Extra practice")
    AR1 = 12 ** 2 / 20
    gen = [
        mcq(SD(21), SUP, L("Một máy bay giữ nguyên C_L và mật độ; tốc độ tăng từ 100 kt lên 200 kt. Lực nâng thay đổi thế nào?", "An aircraft keeps the same C_L and air density; speed rises from 100 kt to 200 kt. What happens to lift?"),
            L("tăng gấp 4", "it increases 4 times"), [L("tăng gấp 2", "it doubles"), L("tăng gấp 8", "it increases 8 times"), L("không đổi", "it does not change")],
            L("L ∝ V²; EASA nêu đúng ví dụ này ở phần Lift.", "L ∝ V²; EASA gives exactly this example in the Lift section.")),
        mcq(SD(22), SUP, L("Cánh có sải 12 m và diện tích 20 m². Tỉ số kích thước AR bằng:", "A wing has a 12 m span and 20 m² area. Its aspect ratio AR is:"),
            N(AR1, 1), [N(12 / 20, 1), N(20 / 12, 1), N(12 * 20, 0)],
            L("AR = b²/S = 144/20.", "AR = b²/S = 144/20.")),
        mcq(SD(23), SUP, L("Giữ nguyên mọi thứ, tăng AR của cánh sẽ làm lực cản cảm ứng:", "Everything else equal, increasing the wing AR makes induced drag:"),
            L("giảm", "decrease"), [L("tăng", "increase"), L("không đổi", "stay the same"), L("trở thành lực cản ký sinh", "become parasite drag")],
            L("C_Di = C_L²/(π e AR): AR lớn thì C_Di nhỏ.", "C_Di = C_L²/(π e AR): larger AR gives smaller C_Di.")),
        mcq(SD(24), SUP, L("Áp suất tại điểm đình trệ của dòng tự do bằng:", "The pressure at the stagnation point of a free stream equals:"),
            L("p∞ + ½ρV∞² (áp suất toàn phần)", "p∞ + ½ρV∞² (total pressure)"), [L("p∞ − ½ρV∞²", "p∞ − ½ρV∞²"), L("chỉ p∞", "p∞ only"), L("½ρV∞² một mình", "½ρV∞² alone")],
            L("Dòng bị hãm hoàn toàn nên toàn bộ áp suất động đổi thành áp suất tĩnh.", "The flow is brought fully to rest, so all the dynamic pressure becomes static pressure.")),
        mcq(SD(25), SUP, L("Hệ số áp suất C_p = −1 xảy ra ở điểm có vận tốc cục bộ bằng:", "A pressure coefficient C_p = −1 occurs at a point where the local velocity equals:"),
            L("√2 lần vận tốc dòng tự do", "√2 times the free-stream velocity"), [L("vận tốc dòng tự do", "the free-stream velocity"), L("2 lần vận tốc dòng tự do", "twice the free-stream velocity"), L("0", "0")],
            L("C_p = 1 − (V/V∞)² = −1 suy ra V = √2·V∞.", "C_p = 1 − (V/V∞)² = −1 gives V = √2·V∞.")),
        mcq(SD(26), SUP, L("Băng bám trên cánh trước khi cất cánh gây ra hậu quả chính nào?", "What is the main effect of ice left on the wing before take-off?"),
            L("Giảm lực nâng và tăng lực cản", "Lift falls and drag rises"), [L("Tăng lực nâng", "Lift rises"), L("Chỉ làm tăng trọng lượng", "It only adds weight"), L("Không ảnh hưởng nếu lớp băng mỏng", "No effect if the layer is thin")],
            L("Bề mặt thô làm lớp biên giới xấu đi (EASA tr. 2.9); lớp băng mỏng vẫn nguy hiểm.", "A rough surface degrades the boundary layer (EASA p. 2.9); even thin ice is dangerous.")),
        mcq(SD(27), SUP, L("Với cánh mỏng đối xứng theo lý thuyết, tâm áp lực nằm ở:", "For a thin symmetric airfoil in theory the centre of pressure lies at:"),
            L("một phần tư dây cung", "the quarter chord"), [L("mép trước", "the leading edge"), L("giữa dây cung", "mid-chord"), L("mép sau", "the trailing edge")],
            L("Cánh mỏng đối xứng có tâm áp lực trùng tâm khí động ở c/4 (Anderson 4.7–4.9).", "A thin symmetric airfoil has its centre of pressure at the aerodynamic centre, c/4 (Anderson 4.7–4.9).")),
        mcq(SD(28), SUP, L("Lớp biên giới rối so với lớp tầng thì thường:", "Compared with a laminar boundary layer, a turbulent one usually:"),
            L("ma sát lớn hơn nhưng tách dòng muộn hơn", "has more friction but separates later"), [L("ma sát nhỏ hơn và tách sớm hơn", "has less friction and separates sooner"), L("ma sát nhỏ hơn và tách muộn hơn", "has less friction and separates later"), L("giống nhau về mọi mặt", "is the same in every respect")],
            L("Lớp rối mang nhiều động lượng hơn sát bề mặt nên bám tốt hơn, đổi lại ma sát da cao hơn.", "A turbulent layer carries more momentum near the wall so it clings better, at the price of higher skin friction.")),
    ]
    m["quiz_sets"] = [
        {"key": "easa", "title": L("Sách 1, EASA Module 08: câu hỏi cuối Sub-module 02 (8 câu, đổi từ điền khuyết sang trắc nghiệm)", "Book 1, EASA Module 08: end of Sub-module 02 (8 questions, converted from fill-in to multiple choice)"),
         "intro": L("Đáp án đúng giữ nguyên như bản in (tr. 2.20); các phương án sai được viết thêm.", "The correct answer is the printed one (p. 2.20); the wrong options were added for this quiz."), "items": easa},
        {"key": "anderson", "title": L("Sách 2, Anderson: bài tập cuối chương 1, 3, 4 (đáp án đã tính lại)", "Book 2, Anderson: end-of-chapter problems from ch. 1, 3, 4 (answers recomputed)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập thêm (tự soạn, đáp án đã kiểm bằng tính toán)", "Extra practice (written for this site, answers checked by calculation)"), "items": gen},
    ]
    m["problems_intro"] = L("Bốn nhóm bài của Anderson, giải từng bước. Đề lấy từ bản 6 (mục 1.17, 3.24, 4.18). Lời giải được tính lại và so với Solution Manual (bản 4) cho các bài 3.3, 3.4, 3.6, 3.7, 3.18, 4.2, 4.5: tất cả đều khớp. Bài 4.10–4.12 theo đề bản 6 không có tương ứng trong bản 4 nên chưa đối chiếu được.",
                            "Four groups of Anderson problems, solved step by step. The problems come from the 6th edition (sec. 1.17, 3.24, 4.18). Solutions were recomputed and compared with the 4th-edition Solution Manual for problems 3.3, 3.4, 3.6, 3.7, 3.18, 4.2 and 4.5: all agree. Problems 4.10–4.12 follow the 6th-edition wording, have no counterpart in the 4th and could not be compared.")
    m["problems"] = [
        {"num": "1.5", "src": "Anderson 6th, Problem 1.5", "q": L("Một biên dạng ở góc tấn α = 12° có hệ số lực pháp tuyến c_n = 1,2 và hệ số lực dọc trục c_a = 0,03. Tính hệ số lực nâng c_l và hệ số lực cản c_d.", "An airfoil at α = 12° has a normal-force coefficient c_n = 1.2 and an axial-force coefficient c_a = 0.03. Find the lift coefficient c_l and the drag coefficient c_d."),
         "ans": L(f"<p>c_l = c_n cos α − c_a sin α = <b>{N(cl15, 3)}</b>.</p><p>c_d = c_n sin α + c_a cos α = <b>{N(cd15, 3)}</b>.</p>", f"<p>c_l = c_n cos α − c_a sin α = <b>{N(cl15, 3)}</b>.</p><p>c_d = c_n sin α + c_a cos α = <b>{N(cd15, 3)}</b>.</p>")},
        {"num": "3.4 – 3.7", "src": "Anderson 6th, Problems 3.4, 3.6, 3.7", "q": L("(3.4) Hầm gió hở có tỉ số diện tích 12, áp kế chênh 10 cm Hg: tính vận tốc trong buồng thử. (3.6) Ống Pitot trên máy bay ở mực biển đọc 1,07×10⁵ N/m²: tính tốc độ bay. (3.7) Tại một điểm trên cánh máy bay đó, vận tốc cục bộ là 130 m/s: tính C_p.", "(3.4) An open-circuit wind tunnel has an area ratio of 12 and a 10 cm Hg manometer difference: find the test-section velocity. (3.6) A Pitot tube on an aircraft at sea level reads 1.07×10⁵ N/m²: find the flight speed. (3.7) At a point on the wing of that aircraft the local velocity is 130 m/s: find C_p."),
         "ans": L(f"<p>(3.4) Δp = {N(dp34, 0)} N/m²; V = <b>{N(V34, 1)} m/s</b>.</p><p>(3.6) V = √[2(1,07−1,01)×10⁵/1,23] = <b>{N(V36, 1)} m/s</b>.</p><p>(3.7) C_p = 1 − (130/{N(V36, 1)})² = <b>{N(cp37, 3)}</b>.</p>", f"<p>(3.4) Δp = {N(dp34, 0)} N/m²; V = <b>{N(V34, 1)} m/s</b>.</p><p>(3.6) V = √[2(1.07−1.01)×10⁵/1.23] = <b>{N(V36, 1)} m/s</b>.</p><p>(3.7) C_p = 1 − (130/{N(V36, 1)})² = <b>{N(cp37, 3)}</b>.</p>")},
        {"num": "4.2", "src": "Anderson 6th, Problem 4.2", "q": L("Cánh NACA 2412 dây cung c = 2 m, bay V = 50 m/s ở mực biển chuẩn, lực nâng trên đơn vị sải L′ = 1353 N/m. Tìm góc tấn.", "A NACA 2412 airfoil of chord c = 2 m flies at V = 50 m/s at standard sea level with a lift per unit span of L′ = 1353 N/m. Find the angle of attack."),
         "ans": L(f"<p>q = 1537,5 N/m²; c_l = L′/(qc) = <b>{N(cl42, 2)}</b>. Bảng NACA 2412 (bài 1.6): c_l = 0,44 tại <b>α = 2°</b>.</p>", f"<p>q = 1537.5 N/m²; c_l = L′/(qc) = <b>{N(cl42, 2)}</b>. NACA 2412 table (Problem 1.6): c_l = 0.44 at <b>α = 2°</b>.</p>")},
        {"num": "4.10 – 4.12", "src": "Anderson 6th, Problems 4.10, 4.11, 4.12", "q": L("Cánh NACA 2412: (4.10) tìm vị trí tâm khí động từ số liệu trong bảng; (4.11) tính lực nâng trên đơn vị sải khi bay 60 m/s ở độ cao chuẩn 3 km, c = 2 m, α = 4°; (4.12) tính lưu số quanh cánh trong điều kiện đó.", "NACA 2412: (4.10) find the aerodynamic centre from the tabulated data; (4.11) find the lift per unit span at 60 m/s at a standard 3 km, c = 2 m, α = 4°; (4.12) find the circulation around the airfoil in those conditions."),
         "ans": L(f"<p>(4.10) h_ac = 0,25 − (0,008/1,04) = <b>{N(hac, 3)}</b>.</p><p>(4.11) ρ = {N(r3, 4)}; q = {N(q411, 1)}; L′ = qc·c_l = <b>{N(L411, 0)} N/m</b>.</p><p>(4.12) Kutta-Joukowski: Γ = L′/(ρV) = <b>{N(G412, 1)} m²/s</b>.</p>", f"<p>(4.10) h_ac = 0.25 − (0.008/1.04) = <b>{N(hac, 3)}</b>.</p><p>(4.11) ρ = {N(r3, 4)}; q = {N(q411, 1)}; L′ = qc·c_l = <b>{N(L411, 0)} N/m</b>.</p><p>(4.12) Kutta-Joukowski: Γ = L′/(ρV) = <b>{N(G412, 1)} m²/s</b>.</p>")},
    ]
    return m
