# -*- coding: utf-8 -*-
"""Module 04: On dinh va dong luc hoc bay. Nguon: EASA M08 Sub-module 04 (tr.4.1-4.12), Etkin & Reid 3rd ch.1 (1.6 truc), ch.2 (2.3 diem trung hoa),
ch.3 (3.8-3.11), ch.6 (6.2-6.3: cac mode B747, Lanchester; Bai tap 6.1, 6.4), Anderson 6th ch.4 muc 4.9 (tam khi dong)."""
import math
from aero import *
from common import num, ul, table, mcq


def build(lang):
    L = lambda vi, en: vi if lang == "vi" else en
    N = lambda x, nd=2: num(x, nd, lang)

    ph, sp = modes_b747()
    TL = lanchester_period(B747_U0_FPS)
    coef3 = 0.750468
    sum_damp = -2 * (ph["lam"].real + sp["lam"].real)
    # vi du minh hoa
    h_cg, h_n, cla = 0.25, 0.35, 4.5
    Kn = h_n - h_cg
    cma = cla * (h_cg - h_n)
    TL_slow = lanchester_period(400.0)

    m = {"num": "04", "slug": "04-stability", "tag": L("Ổn định bay", "Stability")}
    m["title"] = L("Ổn định và động lực học bay: trục máy bay, ổn định tĩnh và động, các mode dao động", "Flight stability and dynamics: aircraft axes, static and dynamic stability, oscillation modes")
    m["src"] = L("EASA Module 08, Sub-module 04 (tr. 4.1–4.12) · Etkin &amp; Reid ch.1, 2, 3, 6 · Anderson ch.4 mục 4.9",
                 "EASA Module 08, Sub-module 04 (pp. 4.1–4.12) · Etkin &amp; Reid ch. 1, 2, 3, 6 · Anderson ch. 4 sec. 4.9")
    m["intro"] = L("Máy bay phải tự trở về trạng thái cân bằng sau khi bị nhiễu, và phải đáp ứng đúng lệnh điều khiển. Module này bắt đầu từ ba trục và ba bề mặt điều khiển, rồi phân biệt ổn định tĩnh với ổn định động. Tiếp theo là ổn định dọc (điểm trung hòa, lề ổn định), ổn định ngang và ổn định hướng. Phần cuối xét các mode dao động thật của Boeing 747, phugoid và chu kỳ ngắn, với trị riêng lấy từ ma trận hệ thống trong Etkin và được tính lại để đối chiếu với giá trị in trong sách. Hai demo ngay trên trang cho phép kéo trọng tâm và mô phỏng đáp ứng.",
                   "An aircraft must return to equilibrium after a disturbance and respond properly to the controls. This module starts with the three axes and three control surfaces and separates static from dynamic stability. It then covers longitudinal stability (neutral point, static margin), lateral stability and directional stability. The last part looks at the real oscillation modes of the Boeing 747, the phugoid and the short period, with eigenvalues taken from the system matrix in Etkin and recomputed to compare with the printed values. Two live demos on the page let you drag the centre of gravity and simulate the response.")
    m["mapping"] = {
        "easa": L("Sub-module 04 Flight Stability and Dynamics (tr. 4.1–4.12): ba trục, ổn định và điều khiển, ổn định tĩnh, ổn định dọc, ngang (dihedral, sweepback, keel), hướng, Dutch roll; 4 câu hỏi cuối chương (Q4-1, Q4-2, Q4-5, Q4-6)",
                  "Sub-module 04 Flight Stability and Dynamics (pp. 4.1–4.12): three axes, stability and control, static stability, longitudinal, lateral (dihedral, sweepback, keel), directional, Dutch roll; 4 end-of-chapter questions (Q4-1, Q4-2, Q4-5, Q4-6)"),
        "anderson": L("Ch.4 mục 4.9 (tâm khí động, mômen quanh tâm khí động) làm nền cho ổn định dọc; Anderson không có chương ổn định động nên phần mode dao động lấy từ Etkin",
                      "Ch.4 sec. 4.9 (aerodynamic centre, moment about the aerodynamic centre) underlies longitudinal stability; Anderson has no dynamic-stability chapter, so the oscillation modes come from Etkin"),
        "etkin": L("Ch.1 mục 1.6 (trục và ký hiệu); ch.2 mục 2.3 (mômen chúc ngóc tổng và điểm trung hòa, tr. 29–33); ch.3 mục 3.8–3.11 (khí động học ngang, ổn định hướng, ổn định lăn, tr. 76–83); ch.6 mục 6.2–6.3 (các mode của máy bay phản lực B747, xấp xỉ Lanchester, tr. 165–175); Bài tập 6.1 và 6.4",
                   "Ch.1 sec. 1.6 (axes and notation); ch.2 sec. 2.3 (total pitching moment and neutral point, pp. 29–33); ch.3 sec. 3.8–3.11 (lateral aerodynamics, weathercock stability, roll stiffness, pp. 76–83); ch.6 sec. 6.2–6.3 (longitudinal modes of the B747 jet transport, Lanchester approximation, pp. 165–175); Exercises 6.1 and 6.4"),
        "note": L("Đây là module bám sát Etkin nhất: EASA mô tả định tính, còn Etkin cho phương trình và số liệu B747. Bài tập ch.6 của Etkin được giải bằng chính số liệu trong sách. Các bài ch.2 và ch.3 cần bản vẽ ba hình chiếu và dữ liệu máy bay nên chỉ đối chiếu về khái niệm. Solution Manual của Etkin là bản chụp chữ viết tay nên không dùng để lấy đáp án.",
                  "This module follows Etkin most closely: EASA is descriptive, while Etkin provides the equations and the B747 data. The ch.6 exercises are solved with the book's own data. The ch.2 and ch.3 exercises need three-view drawings and aircraft data, so they are matched on concepts only. Etkin's Solution Manual is a set of handwritten scans and is not used for answers."),
    }

    parts = []
    parts.append({"title": L("Ba trục và ba bề mặt điều khiển", "Three axes and three control surfaces"),
                  "bullets": [L("Trục dọc (longitudinal) chạy từ mũi đến đuôi; trục ngang (lateral) từ đầu cánh này đến đầu cánh kia; trục đứng (vertical) từ trên xuống", "The longitudinal axis runs nose to tail, the lateral axis wingtip to wingtip and the vertical axis top to bottom"),
                              L("Lăn (roll), chúc ngóc (pitch) và xoay (yaw) được điều khiển bằng aileron, elevator và rudder", "Roll, pitch and yaw are controlled by the ailerons, elevator and rudder"),
                              L("Ổn định, khả năng cơ động và khả năng điều khiển là ba khái niệm khác nhau", "Stability, manoeuvrability and controllability are three different ideas")],
                  "slides": [
                      {"title": L("Ba trục, ba chuyển động, ba loại ổn định", "Three axes, three motions, three kinds of stability"),
                       "body": table([L("Trục", "Axis"), L("Chuyển động", "Motion"), L("Bề mặt điều khiển", "Control surface"), L("Loại ổn định", "Stability about it")],
                                     [[L("Dọc (longitudinal)", "Longitudinal"), L("lăn (roll)", "roll"), L("aileron ở mép sau cánh", "ailerons on the wing trailing edges"), L("ổn định ngang (lateral)", "lateral (rolling)")],
                                      [L("Ngang (lateral)", "Lateral"), L("chúc ngóc (pitch)", "pitch"), L("elevator ở đuôi ngang", "elevator on the horizontal tail"), L("ổn định dọc (longitudinal)", "longitudinal (pitching)")],
                                      [L("Đứng (vertical)", "Vertical"), L("xoay (yaw)", "yaw"), L("rudder ở đuôi đứng", "rudder on the vertical tail"), L("ổn định hướng (directional)", "directional (yawing)")]]) +
                       f"<p class='pill'>{L('EASA Q4-1: ba trục là longitudinal, lateral, vertical; Q4-6: ổn định quanh trục đứng gọi là yawing hay directional', 'EASA Q4-1: the three axes are longitudinal, lateral, vertical; Q4-6: stability about the vertical axis is called yawing or directional')}</p>",
                       "explain": L("Tên gọi dễ gây nhầm: ổn định dọc là ổn định quanh trục NGANG, vì khi chúc ngóc (mũi lên xuống) máy bay quay quanh trục ngang.", "The names are confusing: longitudinal stability is about the LATERAL axis, because pitching rotates the aircraft about the lateral axis.")},
                      {"title": L("Ổn định, cơ động và điều khiển", "Stability, manoeuvrability and controllability"),
                       "body": ul(L("Ổn định (stability): đặc tính khiến máy bay bay thẳng bằng khi buông tay", "Stability: the characteristic that makes an aircraft fly straight and level hands off"),
                                  L("Khả năng cơ động (manoeuvrability): đặc tính cho phép bay theo quỹ đạo mong muốn và chịu được ứng suất do cơ động", "Manoeuvrability: the characteristic that lets the aircraft be directed along a desired path and withstand the stresses imposed"),
                                  L("Khả năng điều khiển (controllability): chất lượng đáp ứng của máy bay với thao tác điều khiển của phi công", "Controllability: the quality of the aircraft's response to the pilot's control application"),
                                  L("Quá ổn định thì khó cơ động: hai tính chất này đánh đổi nhau", "Too much stability makes the aircraft hard to manoeuvre: the two trade off against each other")),
                       "explain": L("Máy bay chiến đấu thường được thiết kế gần trung tính, thậm chí bất ổn, để cơ động tốt; máy tính điều khiển bay sẽ giữ ổn định thay cho thiết kế.", "Fighters are designed near neutral or even unstable for agility, with a flight-control computer providing the stability.")}]})
    parts.append({"title": L("Ổn định tĩnh và ổn định động", "Static and dynamic stability"),
                  "bullets": [L("Ổn định tĩnh: xu hướng ban đầu sau khi bị nhiễu (về, đứng yên hay đi xa cân bằng)", "Static stability: the initial tendency after a disturbance (return, stay, or move away from equilibrium)"),
                              L("Ổn định động: đáp ứng theo thời gian, biên độ dao động giảm, không đổi hay tăng", "Dynamic stability: the response over time, with amplitude decreasing, constant or growing"),
                              L("Ổn định tĩnh dương không đảm bảo ổn định động dương", "Positive static stability does not guarantee positive dynamic stability")],
                  "slides": [
                      {"title": L("Dương, trung tính, âm", "Positive, neutral, negative"),
                       "body": table([L("Loại", "Type"), L("Ổn định tĩnh (xu hướng ban đầu)", "Static (initial tendency)"), L("Ổn định động (biên độ theo thời gian)", "Dynamic (amplitude over time)")],
                                     [[L("Dương", "Positive"), L("quay về trạng thái cân bằng ban đầu", "returns to the original equilibrium"), L("dao động tắt dần", "oscillation dies out")],
                                      [L("Trung tính", "Neutral"), L("ở nguyên trạng thái mới", "stays in the new condition"), L("dao động không đổi (như giảm xóc mòn)", "constant oscillation (like a worn shock absorber)")],
                                      [L("Âm", "Negative"), L("tiếp tục đi xa cân bằng", "keeps moving away"), L("biên độ tăng dần", "amplitude grows")]]) +
                       f"<p class='pill'>{L('EASA tr. 4.3, Hình 4-2 và 4-3', 'EASA p. 4.3, Figures 4-2 and 4-3')}</p>",
                       "explain": L("Một con lắc có ma sát: kéo ra và thả, nó về giữa (tĩnh dương) và dao động nhỏ dần (động dương). Bỏ ma sát, nó dao động mãi (động trung tính).", "A pendulum with friction: pull and release, it returns to the centre (static positive) and the swings die out (dynamic positive). Remove the friction and it swings forever (dynamic neutral).")}]})
    parts.append({"title": L("Ổn định dọc: trọng tâm, đuôi và điểm trung hòa", "Longitudinal stability: centre of gravity, tail and the neutral point"),
                  "bullets": [L("Ổn định dọc tĩnh phụ thuộc vị trí cánh so với CG, vị trí đuôi ngang so với CG và diện tích đuôi", "Static longitudinal stability depends on the wing location relative to the CG, the tail location relative to the CG and the tail area"),
                              L("Tâm áp lực của cánh có độ cong dịch về phía trước khi góc tấn tăng, nên bản thân cánh không ổn định", "The centre of lift of a cambered wing moves forward as AOA grows: the wing alone is unstable"),
                              L("Điều kiện ổn định: CG nằm trước điểm trung hòa (lề ổn định dương)", "The condition for stability: the CG lies ahead of the neutral point (positive static margin)")],
                  "slides": [
                      {"title": L("Ba yếu tố và cơ chế đòn bẩy CG-CL-T", "Three factors and the CG-CL-T lever"),
                       "body": ul(L("Cánh nâng tại tâm nâng CL nằm sau CG, nên máy bay thiên về nặng mũi", "The wing lifts at the centre of lift CL aft of the CG, so the aircraft tends to be nose-heavy"),
                                  L("Đuôi ngang đặt ở góc âm nhỏ tạo lực đè xuống tại T để cân bằng mômen", "The horizontal tail at a small negative angle produces a downward force at T to balance the moment"),
                                  L("Tốc độ giảm thì downwash yếu đi, lực đè ở đuôi giảm, mũi chúi xuống và tốc độ lại tăng. Chu trình này lặp lại và tạo ra dao động phugoid (EASA Hình 4-5)", "Lower speed reduces downwash and the download on the tail, the nose drops and speed rises again: the root of the phugoid (EASA Figure 4-5)"),
                                  L("Giảm công suất làm mũi chúi xuống; đường lực đẩy cao hoặc thấp so với CG cũng ảnh hưởng ổn định dọc (EASA Hình 4-6 đến 4-8)", "Reducing power lets the nose pitch down; a thrust line above or below the CG also affects longitudinal stability (EASA Figures 4-6 to 4-8)")),
                       "explain": L("Đuôi ngang giống phần lông gắn ở đuôi mũi tên: nó kéo phần sau xuôi theo dòng gió, nên mũi luôn hướng về phía bay.", "The horizontal tail acts like the fletching of an arrow: it pulls the rear into the airstream so the nose keeps pointing the way it flies.")},
                      {"title": L("Điểm trung hòa và lề ổn định (Etkin 2.3)", "Neutral point and static margin (Etkin 2.3)"),
                       "body": ul(L("Điểm trung hòa h_n là vị trí CG làm C_mα = 0: biên giới giữa độ cứng chúc ngóc dương và âm", "The neutral point h_n is the CG position for which C_mα = 0: the boundary between positive and negative pitch stiffness"),
                                  L("C_mα = C_Lα (h − h_n) và lề ổn định K_n = h_n − h; ổn định khi h &lt; h_n, tức K_n &gt; 0 (CG nằm trước NP)", "C_mα = C_Lα (h − h_n) and static margin K_n = h_n − h; stable when h &lt; h_n, i.e. K_n &gt; 0 (CG ahead of the NP)"),
                                  L("Yêu cầu thường gặp: NP phải nằm sau vị trí CG sau cùng một khoảng nhất định, ví dụ 5% dây cung trung bình (Etkin 1.5)", "A typical requirement: the NP must lie some distance behind the most aft CG, for example 5% of the mean aerodynamic chord (Etkin 1.5)"),
                                  L(f"Ví dụ minh họa: h = {N(h_cg, 2)}, h_n = {N(h_n, 2)}, C_Lα = {N(cla, 1)} /rad cho K_n = {N(Kn, 2)} và C_mα = {N(cma, 2)} /rad", f"Illustrative example: h = {N(h_cg, 2)}, h_n = {N(h_n, 2)}, C_Lα = {N(cla, 1)} per rad gives K_n = {N(Kn, 2)} and C_mα = {N(cma, 2)} per rad")),
                       "explain": L("Dời CG về sau tới điểm trung hòa thì C_mα về 0 và máy bay mất độ cứng chúc ngóc. Vì thế giới hạn CG sau là giới hạn an toàn khi chất tải và bảo dưỡng.", "Move the CG aft to the neutral point and C_mα goes to zero: the aircraft loses pitch stiffness. That is why the aft CG limit is a safety limit for loading and maintenance.")}]})
    parts.append({"title": L("Ổn định ngang và hướng", "Lateral and directional stability"),
                  "bullets": [L("Góc V ngang (dihedral) của cánh càng lớn thì ổn định ngang càng tăng (EASA Q4-5)", "More wing dihedral means more lateral stability (EASA Q4-5)"),
                              L("Cánh xuôi sau, hiệu ứng keel và phân bố trọng lượng cũng đóng góp", "Sweepback, the keel effect and weight distribution also contribute"),
                              L("Đuôi đứng và thân sau cho ổn định hướng; Dutch roll là dao động hướng kết hợp lăn", "The fin and rear fuselage give directional stability; Dutch roll is a coupled yaw-roll oscillation")],
                  "slides": [
                      {"title": L("Ổn định ngang", "Lateral stability"),
                       "body": ul(L("Khi cánh nghiêng, máy bay trượt về phía cánh thấp; với dihedral, cánh thấp có góc tấn hiệu dụng lớn hơn nên lực nâng tăng và đưa máy bay trở lại ngang bằng", "When a wing drops the aircraft slips towards the low wing; with dihedral the low wing meets the air at a larger effective angle of attack, so its lift grows and levels the aircraft"),
                                  L("Cánh xuôi sau có tác dụng tương tự dihedral", "Sweepback acts like dihedral"),
                                  L("Hiệu ứng keel: thân và đuôi đứng ở phía trên hoặc dưới trọng tâm tạo mômen lăn khi trượt", "Keel effect: the fuselage and fin above or below the CG create a rolling moment when sideslipping"),
                                  L("Trọng lượng thấp so với cánh (pendulum effect) cũng giúp ổn định, nhưng chỉ là phần nhỏ", "Weight low relative to the wing (the pendulum effect) also helps, but only slightly")),
                       "explain": L("Etkin 3.11 gọi đặc tính này là độ cứng lăn (roll stiffness) và đo nó bằng đạo hàm ổn định C_lβ, tức mômen lăn sinh ra trên mỗi đơn vị góc trượt.", "Etkin sec. 3.11 calls this roll stiffness and measures it by the stability derivative C_lβ, the rolling moment produced per unit of sideslip angle.")},
                      {"title": L("Ổn định hướng và Dutch roll", "Directional stability and Dutch roll"),
                       "body": ul(L("Đuôi đứng hoạt động như chong chóng gió: khi máy bay trượt ngang, mặt đứng tạo mômen xoay đưa mũi về hướng gió (weathercock stability, Etkin 3.9)", "The vertical fin acts like a weather vane: when the aircraft sideslips the fin produces a yawing moment that turns the nose into the wind (weathercock stability, Etkin 3.9)"),
                                  L("Dutch roll là dao động kết hợp xoay và lăn, tên gọi mô phỏng động tác của người trượt băng (Etkin bài 6.11)", "Dutch roll is a coupled yawing and rolling oscillation, named after the motion of an ice skater (Etkin Exercise 6.11)"),
                                  L("Ổn định hướng quá mạnh so với ổn định ngang dễ gây bất ổn xoắn ốc (spiral); quá yếu thì gây Dutch roll. Nhà thiết kế chọn điểm giữa, và EASA nói hầu hết máy bay hơi thiên về xoắn ốc vì Dutch roll khó chịu hơn", "Directional stability that is strong relative to lateral stability tends to give spiral instability; too weak gives Dutch roll. Designers choose a midpoint, and EASA says most aircraft lean slightly towards the spiral because Dutch roll is more objectionable"),
                                  L("Bộ giảm xoay (yaw damper) là giải pháp phổ biến cho máy bay phản lực cánh xuôi (Etkin 8.7)", "A yaw damper is the usual cure on swept-wing jets (Etkin 8.7)")),
                       "explain": L("Khi gặp \"directional stability\" trong tài liệu bảo dưỡng, hãy nghĩ tới đuôi đứng: sửa chữa nào làm đổi hình dạng hoặc diện tích đuôi đứng cũng ảnh hưởng đến nó.", "When you meet \"directional stability\" in maintenance literature think of the fin: any repair that changes its shape or area affects it.")}]})
    parts.append({"title": L("Các mode dao động: số liệu Boeing 747", "The oscillation modes: Boeing 747 data"),
                  "bullets": [L("Hai mode dọc: phugoid (chu kỳ dài, tắt chậm) và chu kỳ ngắn (tắt nhanh)", "Two longitudinal modes: phugoid (long period, lightly damped) and short period (heavily damped)"),
                              L("Trị riêng λ = σ ± iω cho chu kỳ T = 2π/ω và hệ số tắt dần ζ = −σ/|λ|", "The eigenvalue λ = σ ± iω gives the period T = 2π/ω and damping ratio ζ = −σ/|λ|"),
                              L("Xấp xỉ Lanchester cho chu kỳ phugoid chỉ phụ thuộc tốc độ bay", "The Lanchester approximation gives a phugoid period that depends on flight speed only")],
                  "slides": [
                      {"title": L("Trị riêng của B747 (Etkin tr. 166)", "B747 eigenvalues (Etkin p. 166)"),
                       "body": table([L("Mode", "Mode"), "λ = σ ± iω", L("T (s)", "T (s)"), "ζ", L("t½ (s)", "t½ (s)")],
                                     [["Phugoid", f"{N(ph['lam'].real, 6)} ± {N(ph['lam'].imag, 5)}i", N(ph["T"], 1), N(ph["zeta"], 3), N(ph["t_half"], 0)],
                                      [L("Chu kỳ ngắn", "Short period"), f"{N(sp['lam'].real, 4)} ± {N(sp['lam'].imag, 4)}i", N(sp["T"], 2), N(sp["zeta"], 3), N(sp["t_half"], 2)]]) +
                       f"<p class='pill'>{L('Tính lại từ ma trận A của Etkin (6.2,1); khớp với trị riêng in trong sách (6.2,3): −0,003289 ± 0,06723i và −0,3719 ± 0,8875i. Các hệ số của đa thức đặc trưng cũng khớp: 0,750468; 0,935494; 0,0094630; 0,0041959.', 'Recomputed from the A matrix of Etkin (6.2,1); it matches the printed eigenvalues (6.2,3): −0.003289 ± 0.06723i and −0.3719 ± 0.8875i. The coefficients of the characteristic polynomial also match: 0.750468; 0.935494; 0.0094630; 0.0041959.')}</p>",
                       "explain": L("σ âm nghĩa là dao động tắt dần. Phugoid có σ rất nhỏ nên mất hơn ba phút để giảm một nửa biên độ, trong khi dao động chu kỳ ngắn giảm một nửa chỉ sau gần hai giây.", "A negative σ means the oscillation dies out. The phugoid has a tiny σ so it takes over three minutes to halve, while the short-period oscillation halves in under two seconds.")},
                      {"title": L("Phugoid và chu kỳ ngắn: khác nhau thế nào", "Phugoid versus short period: how they differ"),
                       "body": ul(L("Phugoid: tốc độ và góc chúc ngóc thay đổi mạnh, góc tấn và tốc độ chúc ngóc gần như không đổi; năng lượng đổi chỗ giữa độ cao và tốc độ (Etkin 6.2)", "Phugoid: speed and pitch attitude change strongly while angle of attack and pitch rate barely change; energy trades between height and speed (Etkin 6.2)"),
                                  L("Chu kỳ ngắn: góc tấn và tốc độ chúc ngóc đổi nhanh, tốc độ bay gần như không đổi", "Short period: angle of attack and pitch rate change quickly while airspeed barely changes"),
                                  L(f"Lanchester: T = π√2·u₀/g = {N(TL, 1)} s với u₀ = 773,98 ft/s, trong khi chu kỳ thật từ trị riêng là {N(ph['T'], 1)} s (Etkin ghi 107 s và 93 s)", f"Lanchester: T = π√2·u₀/g = {N(TL, 1)} s for u₀ = 773.98 ft/s, while the true period from the eigenvalues is {N(ph['T'], 1)} s (Etkin quotes 107 s and 93 s)"),
                                  L("EASA mô tả đúng hiện tượng: các dao động nhỏ dần, mũi lên xuống luân phiên rồi máy bay ổn định lại ở tốc độ cân bằng", "EASA describes the same behaviour: diminishing oscillations with the nose alternately rising and lowering, until the aircraft settles at the balancing speed")),
                       "explain": L("Theo xấp xỉ này, chu kỳ phugoid chỉ tỉ lệ với tốc độ bay: bay chậm đi một nửa thì chu kỳ cũng giảm một nửa, và nó không phụ thuộc loại máy bay hay độ cao.", "In this approximation the phugoid period is proportional to flight speed alone: half the speed gives half the period, and it depends on neither the aircraft nor the altitude.")}]})
    m["parts"] = parts
    m["formula_label"] = L("Lề ổn định, trị riêng, chu kỳ và xấp xỉ Lanchester", "Static margin, eigenvalue, period and the Lanchester approximation")
    m["formula_math"] = ("C_mα = C_Lα (h − h_n)  ·  K_n = h_n − h<br>λ = σ ± iω  ·  T = 2π/ω  ·  ζ = −σ/|λ|  ·  t½ = ln 2/|σ|  ·  T_phugoid ≈ π√2·u₀/g" if lang == "vi" else
                         "C_mα = C_Lα (h − h_n)  ·  K_n = h_n − h<br>λ = σ ± iω  ·  T = 2π/ω  ·  ζ = −σ/|λ|  ·  t½ = ln 2/|σ|  ·  T_phugoid ≈ π√2·u₀/g")
    m["legend"] = [("h, h_n", L("vị trí CG và điểm trung hòa (theo dây cung trung bình)", "CG and neutral-point positions (fractions of the MAC)")), ("K_n", L("lề ổn định tĩnh", "static margin")),
                   ("σ, ω", L("phần thực và phần ảo của trị riêng", "real and imaginary parts of the eigenvalue")), ("ζ", L("hệ số tắt dần", "damping ratio")),
                   ("t½", L("thời gian giảm một nửa biên độ", "time to half amplitude")), ("u₀", L("tốc độ bay cân bằng", "steady flight speed"))]
    m["history_title"] = L("Lanchester và tên gọi \"phugoid\"", "Lanchester and the name \"phugoid\"")
    m["history"] = L("Frederick Lanchester mô tả dao động chu kỳ dài này năm 1908 và đặt tên là phugoid. Etkin ghi chú: từ này bắt nguồn từ một gốc Hy Lạp nghĩa là \"chạy trốn\", trong khi Lanchester định dùng gốc nghĩa là \"bay\". Dù không chính xác, tên gọi ấy vẫn thành thuật ngữ chuẩn (Etkin tr. 167). Lời giải của ông giả sử năng lượng toàn phần không đổi, nên chu kỳ chỉ phụ thuộc tốc độ.",
                     "Frederick Lanchester described this long-period oscillation in 1908 and named it the phugoid. Etkin notes that the name comes from a Greek root meaning \"fugitive\", while Lanchester meant the root for \"fly\". It is not exact, but the word has become standard (Etkin p. 167). His solution assumed constant total energy, so the period depends only on speed.")
    m["case_title"] = L("Tình huống: kiểm tra trọng tâm sau khi chất tải", "Case: checking the CG after loading")
    m["case"] = L(ul(f"Giả sử máy bay có điểm trung hòa ở {N(h_n * 100, 0)}% MAC, và quy định yêu cầu CG sau cùng cách NP ít nhất 5% MAC (ví dụ trong Etkin 1.5), tức CG ≤ {N((h_n - 0.05) * 100, 0)}% MAC.",
                  f"Sau một lần chất tải, CG ở {N(h_cg * 100, 0)}% MAC: lề ổn định K_n = {N(Kn, 2)} ({N(Kn * 100, 0)}% MAC), thỏa yêu cầu.",
                  f"Nếu CG lùi tới 32% MAC thì K_n chỉ còn {N(h_n - 0.32, 2)}, không đủ.",
                  "Số liệu chỉ để minh họa; công thức K_n = h_n − h là của Etkin 2.3."),
                  ul(f"Suppose an aircraft has its neutral point at {N(h_n * 100, 0)}% MAC and the rules require the aft CG limit to stay at least 5% MAC ahead of the NP (an example in Etkin 1.5), i.e. CG ≤ {N((h_n - 0.05) * 100, 0)}% MAC.",
                  f"After loading, the CG is at {N(h_cg * 100, 0)}% MAC: the static margin K_n = {N(Kn, 2)} ({N(Kn * 100, 0)}% MAC) meets the requirement.",
                  f"If the CG slipped back to 32% MAC, K_n would be only {N(h_n - 0.32, 2)}, which is not enough.",
                  "The numbers are only illustrative; the formula K_n = h_n − h is from Etkin 2.3."))
    m["warn_title"] = L("Những chỗ dễ nhầm", "Common pitfalls")
    m["warn"] = L(ul("Ổn định dọc là ổn định quanh trục NGANG, còn ổn định ngang là ổn định quanh trục DỌC.",
                  "EASA đánh số đáp án 4-1 đến 4-4, nhưng các câu hỏi là 4-1, 4-2, 4-5, 4-6. Đáp án 4-3 (dihedral) và 4-4 (yawing, directional) thực ra thuộc câu 4-5 và 4-6, nên module này ghép theo nội dung.",
                  "Ổn định tĩnh dương chưa đủ: một dao động có thể tĩnh dương nhưng động âm (biên độ tăng dần).",
                  "Phugoid không phải dao động nhỏ về tốc độ: tốc độ và độ cao đổi mạnh, chỉ riêng góc tấn là gần như không đổi.",
                  "Xấp xỉ Lanchester bỏ qua lực cản, nên cho 107 s thay vì 93 s của B747."),
                  ul("Longitudinal stability is about the LATERAL axis, and lateral stability is about the LONGITUDINAL axis.",
                  "EASA numbers the answers 4-1 to 4-4, but the questions are 4-1, 4-2, 4-5, 4-6. Answers 4-3 (dihedral) and 4-4 (yawing, directional) actually belong to questions 4-5 and 4-6, so this module pairs them by content.",
                  "Positive static stability is not enough: an oscillation can be statically positive but dynamically negative (growing amplitude).",
                  "The phugoid is not a small oscillation in speed: speed and height change a lot, and only the angle of attack stays almost constant.",
                  "The Lanchester approximation neglects drag, so it gives 107 s instead of the B747's 93 s."))
    m["nb_desc"] = L("Notebook nhập ma trận A của B747 từ Etkin, tính trị riêng và so với giá trị in trong sách, tính T, ζ, t½, mô phỏng đáp ứng bằng ma trận mũ và dùng assert để kiểm mọi đáp án quiz.",
                     "The notebook enters the B747 A matrix from Etkin, computes the eigenvalues and compares them with the printed values, computes T, ζ and t½, simulates the response with the matrix exponential and uses assert to check every quiz answer.")

    SD = lambda i: 400 + i
    SRCQ = lambda q, a: L(f"EASA M08 Q4-{q} (tr. 4.11, đáp án 4-{a} ở tr. 4.12)", f"EASA M08 Q4-{q} (p. 4.11, answer 4-{a} on p. 4.12)")
    easa = [
        mcq(SD(1), SRCQ(1, 1), L("Kể tên ba trục của máy bay.", "Name the three axes of an aircraft."),
            L("Dọc (longitudinal), ngang (lateral), đứng (vertical)", "Longitudinal, lateral, vertical"), [L("Dọc, ngang, chéo (diagonal)", "Longitudinal, lateral, diagonal"), L("Dọc, hướng tâm (radial), đứng", "Longitudinal, radial, vertical"), L("Ngang, đứng, tiếp tuyến (tangential)", "Lateral, vertical, tangential")],
            L("Lăn quanh trục dọc, chúc ngóc quanh trục ngang, xoay quanh trục đứng (EASA tr. 4.2).", "Roll about the longitudinal axis, pitch about the lateral axis, yaw about the vertical axis (EASA p. 4.2).")),
        mcq(SD(2), SRCQ(2, 2), L("Ổn định dọc tĩnh của máy bay phụ thuộc vào ba yếu tố nào?", "Static longitudinal stability of an aircraft depends on what three things?"),
            L("Vị trí cánh so với CG; vị trí đuôi ngang so với CG; diện tích đuôi", "Location of the wing relative to the CG; location of the horizontal tail relative to the CG; area of the tail"),
            [L("Sải cánh; chiều dài thân; số động cơ", "Wingspan; fuselage length; number of engines"), L("Trọng lượng; công suất động cơ; độ cao bay", "Weight; engine power; altitude"), L("Vị trí cánh; hình dạng thân; màu sơn", "Wing location; fuselage shape; paint colour")],
            L("EASA tr. 4.4: ba yếu tố đều xoay quanh CG vì vật tự do luôn quay quanh CG.", "EASA p. 4.4: all three revolve around the CG because a free body always rotates about its CG.")),
        mcq(SD(3), SRCQ(5, 3), L("Tăng ____ của cánh làm tăng ổn định ngang của máy bay khi bay.", "An increase in wing ____ increases the lateral stability of the aircraft in flight."),
            L("góc V ngang (dihedral)", "dihedral"), [L("độ cong (camber)", "camber"), L("độ dày", "thickness"), L("tải trọng cánh", "wing loading")],
            L("Dihedral là phương tiện chính của ổn định ngang (EASA tr. 4.7, Hình 4-9). Đáp án in là 4-3 nhưng thuộc câu 4-5.", "Dihedral is the main means of lateral stability (EASA p. 4.7, Figure 4-9). The printed answer is labelled 4-3 but belongs to question 4-5.")),
        mcq(SD(4), SRCQ(6, 4), L("Ổn định quanh trục đứng của máy bay được gọi là ổn định ____ hay ____.", "Stability about the vertical axis of an aircraft is known as ____ or ____ stability."),
            L("xoay (yawing); hướng (directional)", "yawing; directional"), [L("chúc ngóc (pitching); dọc (longitudinal)", "pitching; longitudinal"), L("lăn (rolling); ngang (lateral)", "rolling; lateral"), L("chúc ngóc (pitching); hướng (directional)", "pitching; directional")],
            L("Đáp án in là 4-4 nhưng thuộc câu 4-6; đuôi đứng quyết định ổn định này.", "The printed answer is labelled 4-4 but belongs to question 4-6; the fin governs this stability.")),
    ]
    book = [
        mcq(SD(11), L("Etkin &amp; Reid, mục 6.2 (trị riêng 6.2,3)", "Etkin &amp; Reid, sec. 6.2 (eigenvalues 6.2,3)"),
            L("Phugoid của B747 có trị riêng λ = −0,003289 ± 0,06723i (đơn vị 1/s). Chu kỳ dao động là:", "The B747 phugoid has eigenvalue λ = −0.003289 ± 0.06723i (units 1/s). The period of the oscillation is:"),
            f"{N(ph['T'], 1)} s", [f"{N(ph['T'] / 6.2, 1)} s", f"{N(ph['T'] * 1.15, 1)} s", f"{N(2 * math.pi / 0.003289, 0)} s"],
            L("T = 2π/ω với ω là phần ảo.", "T = 2π/ω with ω the imaginary part."),
            L(f"<p>T = 2π/0,06723 = {N(ph['T'], 1)} s. Etkin ghi 93 s. Dùng phần thực 0,003289 sẽ cho {N(2 * math.pi / 0.003289, 0)} s, sai hoàn toàn.</p>", f"<p>T = 2π/0.06723 = {N(ph['T'], 1)} s. Etkin quotes 93 s. Using the real part 0.003289 would give {N(2 * math.pi / 0.003289, 0)} s, completely wrong.</p>")),
        mcq(SD(12), L("Etkin &amp; Reid, mục 6.2", "Etkin &amp; Reid, sec. 6.2"),
            L("Mode chu kỳ ngắn của B747 có λ = −0,3719 ± 0,8875i. Hệ số tắt dần ζ = −σ/|λ| xấp xỉ:", "The B747 short-period mode has λ = −0.3719 ± 0.8875i. The damping ratio ζ = −σ/|λ| is approximately:"),
            N(sp["zeta"], 3), [N(0.3719, 3), N(0.8875, 3), N(sp["zeta"] * 2, 3)],
            L("|λ| = √(σ² + ω²).", "|λ| = √(σ² + ω²)."),
            L(f"<p>|λ| = √(0,3719² + 0,8875²) = {N(sp['wn'], 4)} rad/s; ζ = 0,3719/{N(sp['wn'], 4)} = {N(sp['zeta'], 3)}. Chu kỳ T = {N(sp['T'], 2)} s.</p>", f"<p>|λ| = √(0.3719² + 0.8875²) = {N(sp['wn'], 4)} rad/s; ζ = 0.3719/{N(sp['wn'], 4)} = {N(sp['zeta'], 3)}. Period T = {N(sp['T'], 2)} s.</p>")),
        mcq(SD(13), L("Etkin &amp; Reid, mục 6.3 (6.3,10) và Bài tập 6.1", "Etkin &amp; Reid, sec. 6.3 (6.3,10) and Exercise 6.1"),
            L("Xấp xỉ Lanchester T = π√2·u₀/g cho B747 với u₀ = 773,98 ft/s (g = 32,174 ft/s²) là:", "The Lanchester approximation T = π√2·u₀/g for the B747 with u₀ = 773.98 ft/s (g = 32.174 ft/s²) gives:"),
            f"{N(TL, 0)} s", [f"{N(ph['T'], 0)} s", f"{N(TL / 2, 0)} s", f"{N(TL * 2, 0)} s"],
            L("Lanchester giả sử không có lực cản: nên lệch so với 93 s thật.", "Lanchester assumes no drag, so it differs from the true 93 s."),
            L(f"<p>T = π√2 × 773,98/32,174 = {N(TL, 1)} s (Etkin ghi 107 s). Phép tính theo hệ SI cho cùng kết quả: u₀ = 235,9 m/s, g = 9,807 m/s² cho {N(math.pi * math.sqrt(2) * 235.9 / 9.80665, 1)} s.</p>", f"<p>T = π√2 × 773.98/32.174 = {N(TL, 1)} s (Etkin quotes 107 s). The SI calculation gives the same: u₀ = 235.9 m/s, g = 9.807 m/s² gives {N(math.pi * math.sqrt(2) * 235.9 / 9.80665, 1)} s.</p>")),
        mcq(SD(14), L("Etkin &amp; Reid, Bài tập 6.4", "Etkin &amp; Reid, Exercise 6.4"),
            L("Đa thức đặc trưng B747 là λ⁴ + 0,750468λ³ + 0,935494λ² + 0,0094630λ + 0,0041959 = 0. Theo Bài tập 6.4, hệ số của λ³ bằng:", "The B747 characteristic polynomial is λ⁴ + 0.750468λ³ + 0.935494λ² + 0.0094630λ + 0.0041959 = 0. According to Exercise 6.4, the coefficient of λ³ equals:"),
            L(f"trừ tổng phần thực của mọi nghiệm: {N(sum_damp, 4)}", f"minus the sum of the real parts of all roots: {N(sum_damp, 4)}"),
            [L("tổng bình phương các phần ảo", "the sum of the squares of the imaginary parts"), L("tích của các nghiệm", "the product of the roots"), L("tổng các tần số riêng không tắt", "the sum of the undamped natural frequencies")],
            L("Tổng \"độ tắt dần\" của các mode.", "The \"sum of the dampings\" of the modes."),
            L(f"<p>−Σ Re λ = 2(0,003289 + 0,3719) ≈ {N(sum_damp, 6)}, đúng bằng hệ số in trong sách. Hệ số này cho biết tổng \"độ tắt dần\" của các mode, nên nó phải dương thì mới có thể ổn định.</p>", f"<p>−Σ Re λ = 2(0.003289 + 0.3719) ≈ {N(sum_damp, 6)}, the coefficient printed in the book. This coefficient is the total \"damping\" of the modes, so it must be positive for stability.</p>")),
        mcq(SD(15), L("Etkin &amp; Reid, mục 6.2", "Etkin &amp; Reid, sec. 6.2"),
            L("Thời gian để biên độ phugoid của B747 giảm một nửa (t½ = ln 2/|σ|, σ = −0,003289) là:", "The time for the B747 phugoid amplitude to halve (t½ = ln 2/|σ|, σ = −0.003289) is:"),
            f"{N(ph['t_half'], 0)} s", [f"{N(ph['t_half'] / 100, 1)} s", f"{N(ph['t_half'] / 10, 0)} s", f"{N(ph['T'], 0)} s"],
            L("t½ = ln 2/0,003289.", "t½ = ln 2/0.003289."),
            L(f"<p>t½ = 0,6931/0,003289 = {N(ph['t_half'], 1)} s ≈ {N(ph['t_half'] / ph['T'], 1)} chu kỳ. Phugoid tắt rất chậm, nên phi công phải chú ý nó.</p>", f"<p>t½ = 0.6931/0.003289 = {N(ph['t_half'], 1)} s ≈ {N(ph['t_half'] / ph['T'], 1)} periods. The phugoid decays very slowly, so pilots must watch for it.</p>")),
        mcq(SD(16), L("Etkin &amp; Reid, mục 6.3", "Etkin &amp; Reid, sec. 6.3"),
            L(f"Theo xấp xỉ Lanchester, nếu B747 bay ở u₀ = 400 ft/s thay vì 773,98 ft/s thì chu kỳ phugoid xấp xỉ:", "In the Lanchester approximation, if the B747 flew at u₀ = 400 ft/s instead of 773.98 ft/s the phugoid period would be about:"),
            f"{N(TL_slow, 0)} s", [f"{N(TL, 0)} s", f"{N(TL * 400 ** 2 / 773.98 ** 2, 0)} s", f"{N(TL_slow * 2, 0)} s"],
            L("T tỉ lệ thuận với tốc độ.", "T is directly proportional to speed."),
            L(f"<p>T = π√2 × 400/32,174 = {N(TL_slow, 1)} s. Khác với nhiều đại lượng khí động, T không đổi theo bình phương tốc độ mà theo tốc độ.</p>", f"<p>T = π√2 × 400/32.174 = {N(TL_slow, 1)} s. Unlike many aerodynamic quantities, T scales with speed, not speed squared.</p>")),
    ]
    SUP = L("Câu luyện thêm", "Extra practice")
    gen = [
        mcq(SD(21), SUP, L("Máy bay có CG tại h = 0,25 và điểm trung hòa h_n = 0,35 (theo MAC). Lề ổn định tĩnh K_n bằng:", "An aircraft has its CG at h = 0.25 and neutral point h_n = 0.35 (in MAC fractions). The static margin K_n is:"),
            N(Kn, 2), [N(-Kn, 2), N(0.60, 2), N(0.0875, 4)],
            L("K_n = h_n − h = 0,10; dương nên ổn định.", "K_n = h_n − h = 0.10; positive, hence stable.")),
        mcq(SD(22), SUP, L("Dời CG ra phía sau đến đúng điểm trung hòa thì C_mα:", "Moving the CG aft to exactly the neutral point makes C_mα:"),
            L("bằng 0 (mất độ cứng chúc ngóc)", "zero (pitch stiffness is lost)"), [L("âm lớn nhất", "most negative"), L("dương lớn nhất", "most positive"), L("không xác định", "undefined")],
            L("C_mα = C_Lα(h − h_n) = 0 khi h = h_n (Etkin 2.3).", "C_mα = C_Lα(h − h_n) = 0 when h = h_n (Etkin 2.3).")),
        mcq(SD(23), SUP, L("Với C_Lα = 4,5/rad, h = 0,25, h_n = 0,35, giá trị C_mα là:", "With C_Lα = 4.5 per rad, h = 0.25, h_n = 0.35, C_mα is:"),
            f"{N(cma, 2)} /rad", [f"{N(-cma, 2)} /rad", f"{N(cla * 0.6, 2)} /rad", f"{N(-0.1, 2)} /rad"],
            L("C_mα = 4,5 × (0,25 − 0,35) = −0,45; âm nghĩa là ổn định.", "C_mα = 4.5 × (0.25 − 0.35) = −0.45; negative means stable.")),
        mcq(SD(24), SUP, L("Một dao động có biên độ ban đầu giảm rồi lại tăng dần theo thời gian thì có:", "An oscillation whose initial tendency is to return but whose amplitude then grows over time shows:"),
            L("ổn định tĩnh dương nhưng ổn định động âm", "positive static but negative dynamic stability"), [L("ổn định tĩnh âm và ổn định động dương", "negative static and positive dynamic stability"), L("ổn định tĩnh và động đều dương", "positive static and dynamic stability"), L("ổn định động trung tính", "neutral dynamic stability")],
            L("Xu hướng ban đầu quay về là tĩnh dương; biên độ tăng theo thời gian là động âm (EASA tr. 4.3).", "The initial tendency to return is static positive; amplitude growing in time is dynamic negative (EASA p. 4.3).")),
        mcq(SD(25), SUP, L("Cánh có dihedral bị nghiêng; máy bay trượt về phía cánh thấp. Cánh thấp sẽ có:", "A wing with dihedral drops and the aircraft slips towards the low wing. The low wing then has:"),
            L("góc tấn hiệu dụng lớn hơn nên lực nâng tăng", "a larger effective angle of attack so its lift increases"), [L("góc tấn hiệu dụng nhỏ hơn", "a smaller effective angle of attack"), L("lực nâng không đổi", "unchanged lift"), L("lực cản giảm còn bằng 0", "its drag fall to zero")],
            L("Mômen lăn phục hồi đưa máy bay về ngang bằng.", "The restoring rolling moment levels the aircraft.")),
        mcq(SD(26), SUP, L("Dutch roll là dao động kết hợp của:", "Dutch roll is a coupled oscillation of:"),
            L("xoay (yaw) và lăn (roll)", "yaw and roll"), [L("chúc ngóc và tốc độ", "pitch and speed"), L("lăn và chúc ngóc", "roll and pitch"), L("tốc độ và độ cao", "speed and height")],
            L("Etkin bài 6.11 và EASA tr. 4.9 mô tả đây là dao động hướng gắn với lăn.", "Etkin Exercise 6.11 and EASA p. 4.9 describe it as a directional oscillation tied to rolling.")),
        mcq(SD(27), SUP, L("Giảm tốc độ bay làm downwash lên đuôi ngang:", "Reducing airspeed makes the downwash on the horizontal tail:"),
            L("giảm, nên lực đè trên đuôi giảm và mũi chúi xuống", "weaker, so the download on the tail falls and the nose drops"), [L("tăng, nên mũi ngóc lên", "stronger, so the nose rises"), L("không đổi", "unchanged"), L("tăng và làm đuôi đứng bị thất tốc", "stronger and stalls the fin")],
            L("EASA Hình 4-5: tốc độ giảm thì downwash giảm.", "EASA Figure 4-5: lower speed means less downwash.")),
        mcq(SD(28), SUP, L("Vì sao giới hạn CG sau là giới hạn an toàn khi chất tải?", "Why is the aft CG limit a safety limit when loading?"),
            L("Vì CG lùi gần điểm trung hòa làm máy bay mất độ cứng chúc ngóc", "Because an aft CG near the neutral point makes the aircraft lose pitch stiffness"), [L("Vì CG lùi làm tăng lực cản cảm ứng", "Because an aft CG raises induced drag"), L("Vì CG lùi làm cánh thất tốc sớm hơn", "Because an aft CG stalls the wing earlier"), L("Vì CG lùi làm động cơ nóng lên", "Because an aft CG overheats the engines")],
            L("Lề ổn định K_n giảm khi CG lùi; K_n = 0 là bất ổn tĩnh.", "Static margin K_n shrinks as the CG moves aft; K_n = 0 is the edge of static instability.")),
    ]
    m["quiz_sets"] = [
        {"key": "easa", "title": L("Sách 1, EASA Module 08: câu hỏi cuối Sub-module 04 (4 câu, đổi sang trắc nghiệm)", "Book 1, EASA Module 08: end of Sub-module 04 (4 questions, converted to multiple choice)"),
         "intro": L("Bản in đánh số câu hỏi là 4-1, 4-2, 4-5, 4-6 nhưng đáp án là 4-1 đến 4-4, nên các câu được ghép theo nội dung. Đáp án đúng giữ nguyên như bản in (tr. 4.12).", "The printed questions are numbered 4-1, 4-2, 4-5, 4-6 but the printed answers 4-1 to 4-4, so they are paired by content. The correct answers are the printed ones (p. 4.12)."), "items": easa},
        {"key": "etkin", "title": L("Sách 3, Etkin &amp; Reid: các mode của B747 và Bài tập 6.1, 6.4 (tính lại từ ma trận A in trong sách)", "Book 3, Etkin &amp; Reid: the B747 modes and Exercises 6.1, 6.4 (recomputed from the A matrix printed in the book)"), "items": book},
        {"key": "generated", "title": L("Câu luyện tập thêm (tự soạn, đáp án đã kiểm bằng tính toán)", "Extra practice (written for this site, answers checked by calculation)"), "items": gen},
    ]
    m["problems_intro"] = L("Hai bài tập cuối chương 6 của Etkin, giải từng bước với số liệu B747 in trong sách (Bảng 6.1, ma trận A, trị riêng 6.2,3). Đáp án kiểm được vì sách in sẵn các trị riêng.",
                            "Two end-of-chapter 6 exercises from Etkin, solved step by step with the B747 data printed in the book (Table 6.1, matrix A, eigenvalues 6.2,3). The answers can be checked because the book prints the eigenvalues.")
    m["problems"] = [
        {"num": "6.1", "src": "Etkin & Reid 3rd, Exercise 6.1", "q": L("Dùng (6.3,10) để tính chu kỳ phugoid xấp xỉ T = 2π/ω_n, giả sử M_u = 0, cho B747 ở u₀ = 773,98 ft/s.", "Use (6.3,10) to compute the approximate phugoid period T = 2π/ω_n for the B747 at u₀ = 773.98 ft/s, assuming M_u = 0."),
         "ans": L(f"<p>Với M_u = 0 xấp xỉ Lanchester cho ω_n = g√2/u₀ nên T = 2π/ω_n = π√2·u₀/g.</p><p>T = π√2 × 773,98/32,174 = <b>{N(TL, 1)} s</b>.</p><p class='pill'>Etkin ghi 107 s; chu kỳ thật từ trị riêng là {N(ph['T'], 1)} s (sai khác {N((TL - ph['T']) / ph['T'] * 100, 0)}% vì xấp xỉ bỏ qua lực cản).</p>", f"<p>With M_u = 0 the Lanchester approximation gives ω_n = g√2/u₀ so T = 2π/ω_n = π√2·u₀/g.</p><p>T = π√2 × 773.98/32.174 = <b>{N(TL, 1)} s</b>.</p><p class='pill'>Etkin quotes 107 s; the true period from the eigenvalues is {N(ph['T'], 1)} s (a {N((TL - ph['T']) / ph['T'] * 100, 0)}% difference because the approximation neglects drag).</p>")},
        {"num": "6.4", "src": "Etkin & Reid 3rd, Exercise 6.4", "q": L("Chứng minh hệ số của λ^(N−1) trong đa thức đặc trưng bậc N bằng trừ tổng phần thực của mọi nghiệm; kiểm lại cho B747.", "Prove that the coefficient of λ^(N−1) in an Nth-order characteristic polynomial is the negative of the sum of the real parts of all the roots; check it for the B747."),
         "ans": L(f"<p>Đa thức có nghiệm λ₁…λ_N thì p(λ) = Π(λ − λ_i); hệ số của λ^(N−1) là −Σλ_i. Nghiệm phức đi theo cặp liên hợp nên phần ảo triệt tiêu, còn −ΣRe λ_i.</p><p>B747: nghiệm −0,003289 ± 0,06723i và −0,3719 ± 0,8875i nên −ΣRe = 2(0,003289 + 0,3719) = <b>{N(sum_damp, 6)}</b>, trùng hệ số 0,750468 của (6.2,2).</p>", f"<p>If the polynomial has roots λ₁…λ_N then p(λ) = Π(λ − λ_i); the coefficient of λ^(N−1) is −Σλ_i. Complex roots come in conjugate pairs so the imaginary parts cancel, leaving −ΣRe λ_i.</p><p>B747: roots −0.003289 ± 0.06723i and −0.3719 ± 0.8875i so −ΣRe = 2(0.003289 + 0.3719) = <b>{N(sum_damp, 6)}</b>, matching the 0.750468 of (6.2,2).</p>")},
    ]
    return m
