"""m01 generator: writes data/qsrc/m01.json (originals + conceptual slide questions), data/qsrc/m01_gen.json (generated variants)
and data/verify/m01_values.json (registry of every numeric answer, recomputed by build/verify/verify_m01.py through a different route).
Run:  python3 -I build/gen/gen_m01.py"""
import math, os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from m01_common import *
import gen_m01_orig as O

T_THR, T_EFF, T_SFC, T_RNG, T_ISA, T_CLS, T_AER, T_PRI, T_JET, T_APP = O.T_THR, O.T_EFF, O.T_SFC, O.T_RNG, O.T_ISA, O.T_CLS, O.T_AER, O.T_PRI, O.T_JET, O.T_APP
GEN = lambda what_vi, what_en: B(f'Bổ sung – sinh theo dạng {what_vi}', f'Added – generated from the type: {what_en}')

# ======================================================================================== conceptual (slides)
def concept():
    Q = []
    def sx(n): return B(f'Slide Ch.1 tr.{n}', f'Slide Ch.1 p.{n}')
    def sn(vi, en): return B(vi, en)
    def cq(q, opts, correct, expl, level, topic, src, fixed=False):
        Q.append(mcq(q, [dict(vi=a, en=b) for a, b in opts], correct, expl, level, topic, src, 'bo_sung', 'slide (xem ảnh) + sách', fixed=fixed))
    def tq(q, truth, expl, level, topic, src):
        Q.append(tf(q, truth, expl, level, topic, src, 'bo_sung', 'slide (xem ảnh) + sách'))
    # --- aerodynamics tr.5-6
    cq(B('Slide Ch.1 tr.5: máy bay bay bằng đều (level cruise, vận tốc không đổi). Cặp đẳng thức nào đúng?', 'Slide Ch.1 p.5: an aircraft in level cruise at constant speed. Which pair of equalities holds?'),
       [('Lực đẩy = lực cản và lực nâng = trọng lượng', 'Thrust = drag and lift = weight'), ('Lực đẩy = trọng lượng và lực nâng = lực cản', 'Thrust = weight and lift = drag'),
        ('Lực đẩy = lực nâng và lực cản = trọng lượng', 'Thrust = lift and drag = weight'), ('Lực đẩy + lực nâng = lực cản + trọng lượng', 'Thrust + lift = drag + weight')],
       0, B('Bay bằng không gia tốc: theo phương ngang T_u = F_x, theo phương đứng P = F_z (slide tr.5). Các cặp còn lại ghép lực khác phương với nhau.', 'Unaccelerated level flight: horizontally T_u = F_x, vertically P = F_z (slide p.5). The other pairs match forces acting in different directions.'),
       1, T_AER, sx(5))
    tq(B('Slide Ch.1 tr.6: F_x = C_D·V²·(ρ/2)·S. Nếu vận tốc bay tăng gấp đôi (ρ, S, C_D không đổi) thì lực cản tăng gấp bốn.', 'Slide Ch.1 p.6: F_x = C_D·V²·(ρ/2)·S. If the flight speed doubles (ρ, S, C_D unchanged) the drag becomes four times larger.'),
       True, B('Lực cản tỉ lệ với V², nên V → 2V cho F_x → 4F_x. Công suất cản F_x·V tăng 8 lần.', 'Drag is proportional to V², so V → 2V gives F_x → 4F_x. The drag power F_x·V rises eightfold.'), 1, T_AER, sx(6))
    tq(B('Slide Ch.1 tr.6: ở bay bằng, lực đẩy cần thiết bằng trọng lượng của máy bay.', 'Slide Ch.1 p.6: in level flight the required thrust equals the weight of the aircraft.'),
       False, B('Lực đẩy cần bằng lực cản: T_u = F_x = (C_D/C_L)·m·g (suy ra từ F_z = P; ô T_u trên slide để trống). Máy bay có C_L/C_D ≈ 17 chỉ cần lực đẩy cỡ 1/17 trọng lượng.', 'Required thrust equals drag: T_u = F_x = (C_D/C_L)·m·g (derived from F_z = P; the T_u box on the slide is left blank). An aircraft with C_L/C_D ≈ 17 needs a thrust of only about 1/17 of its weight.'), 2, T_AER, sx(6))
    tq(B('Slide Ch.1 tr.6 (ρ = "air density (attitude)", nghĩa là altitude): ở cùng V, S, C_L, bay cao hơn thì lực nâng nhỏ hơn vì ρ giảm.', 'Slide Ch.1 p.6 (ρ = "air density (attitude)", meaning altitude): at the same V, S and C_L, flying higher gives less lift because ρ falls.'),
       True, B('F_z ∝ ρ; mật độ ISA giảm từ 1.225 kg/m³ (mực nước biển) còn 0.413 kg/m³ ở 10 km, nên muốn giữ F_z = P phải tăng V hoặc C_L.', 'F_z ∝ ρ; ISA density falls from 1.225 kg/m³ (sea level) to 0.413 kg/m³ at 10 km, so V or C_L must rise to keep F_z = P.'), 2, T_AER, sx(6))
    # --- propulsion tr.7-10
    cq(B('Slide Ch.1 tr.7: động cơ máy bay tạo lực đẩy dựa trên nguyên lý nào?', 'Slide Ch.1 p.7: on which principle does the airplane engine generate its propulsive force?'),
       [('Nguyên lý tác dụng – phản lực (định luật 3 Newton)', 'The action–reaction principle (Newton\'s third law)'), ('Nguyên lý Archimedes về lực đẩy nổi', 'Archimedes\' buoyancy principle'),
        ('Hiệu ứng Magnus trên cánh quạt quay', 'The Magnus effect on a rotating propeller'), ('Nguyên lý bảo toàn mômen động lượng của rôto', 'Conservation of angular momentum of the rotor')],
       0, B('Động cơ gia tốc một khối lượng khí về phía sau; phản lực của khí lên động cơ là lực đẩy (slide tr.7–10).', 'The engine accelerates a mass of gas rearwards; the reaction of the gas on the engine is the thrust (slides pp.7–10).'), 1, T_PRI, sx(7))
    cq(B('Slide Ch.1 tr.8 và tr.10: so với đẩy bằng cánh quạt ("propulsion by action"), đẩy bằng phản lực ("by reaction") thường:', 'Slide Ch.1 pp.8 and 10: compared with propeller propulsion ("by action"), jet propulsion ("by reaction") typically:'),
       [('hất ra sau một khối lượng khí nhỏ với gia tốc lớn', 'expels a small mass of air rearwards with a great acceleration'), ('hất ra sau một khối lượng khí lớn với gia tốc nhỏ', 'expels a large mass of air rearwards with a small acceleration'),
        ('hất ra sau một khối lượng khí nhỏ với gia tốc nhỏ', 'expels a small mass of air rearwards with a small acceleration'), ('hất ra sau một khối lượng khí lớn với gia tốc lớn', 'expels a large mass of air rearwards with a great acceleration')],
       0, B('Cánh quạt: khối lượng khí lớn, tăng tốc ít (tr.8). Phản lực: khối lượng nhỏ, tăng tốc nhiều (tr.10). Cùng một lực đẩy T = ṁ(ue − u) có thể đạt bằng ṁ lớn/ue − u nhỏ (hiệu suất đẩy cao) hoặc ngược lại.', 'Propeller: large air mass, little acceleration (p.8). Jet: small mass, great acceleration (p.10). The same thrust T = ṁ(ue − u) can come from large ṁ with small ue − u (high propulsive efficiency) or the opposite.'), 1, T_PRI, sx(8))
    tq(B('Slide Ch.1 tr.10 (quả bóng được bơm): khi mở miệng bóng, khí phụt ra phía sau và quả bóng dịch chuyển ngược chiều dòng phụt; trước khi mở, hợp lực trên bóng bằng 0 vì P1 tác dụng đều lên thành bóng.', 'Slide Ch.1 p.10 (inflated balloon): when the mouth is opened the gas jets backwards and the balloon moves opposite to the jet; before opening, the net force on the balloon is zero because P1 acts evenly on the walls.'),
       True, B('Áp suất trong P1 > P0 tác dụng đều lên mọi phía nên F = 0; khi mở miệng, thiếu mặt thành chịu áp suất ở phía miệng, phản lực đẩy bóng ngược chiều dòng phụt.', 'The internal pressure P1 > P0 acts evenly in all directions so F = 0; when the mouth opens, the wall area at the mouth no longer carries pressure and the reaction pushes the balloon opposite to the jet.'), 1, T_PRI, sx(10))
    # --- energy / classification tr.11-16
    cq(B('Slide Ch.1 tr.11: động cơ hàng không vũ trụ là máy biến đổi:', 'Slide Ch.1 p.11: aerospace engines are machines that transform:'),
       [('thế năng (hoá năng) chứa trong nhiên liệu và không khí thành động năng hoặc cơ năng', 'the potential energy contained in fuel and air into kinetic or mechanical energy'), ('nhiệt của khí quyển thành điện năng', 'atmospheric heat into electrical energy'),
        ('động năng của dòng khí thành hoá năng của nhiên liệu', 'the kinetic energy of the airflow into chemical energy of the fuel'), ('cơ năng của cánh quạt thành nhiệt năng của khí xả', 'propeller mechanical energy into exhaust thermal energy')],
       0, B('Năng lượng E của khí sinh ra từ cháy hỗn hợp nhiên liệu–không khí chuyển thành động năng E_c (phản lực) hoặc cơ năng E_m (trục).', 'The gas energy E produced by burning the air–fuel mixture becomes kinetic energy E_c (jet) or mechanical energy E_m (shaft).'), 1, T_CLS, sx(11))
    cq(B('Slide Ch.1 tr.12: ba giai đoạn biến đổi của không khí trong phần lớn hệ đẩy, theo thứ tự, là:', 'Slide Ch.1 p.12: the three transformation phases of air in most propulsion systems, in order, are:'),
       [('nén, cháy, giãn nở', 'compression, combustion, expansion'), ('cháy, nén, giãn nở', 'combustion, compression, expansion'), ('giãn nở, cháy, nén', 'expansion, combustion, compression'), ('nén, giãn nở, cháy', 'compression, expansion, combustion')],
       0, B('Không khí được nén, nhận nhiên liệu và cháy, rồi giãn nở cho ra động năng và/hoặc cơ năng (sơ đồ tr.12). Đây cũng là thứ tự chu trình Brayton (chương 2).', 'Air is compressed, receives fuel and burns, then expands to give kinetic and/or mechanical energy (diagram p.12). This is also the order of the Brayton cycle (chapter 2).'), 1, T_CLS, sx(12), fixed=True)
    cq(B('Slide Ch.1 tr.13: trong sơ đồ phân loại, động cơ piston (reciprocating) và động cơ phản lực (jet propulsion) cùng thuộc nhánh nào?', 'Slide Ch.1 p.13: in the classification tree, reciprocating engines and jet propulsion engines both belong to which branch?'),
       [('Động cơ hút khí (airbreathing)', 'Airbreathing engines'), ('Động cơ không hút khí (non-airbreathing)', 'Non-airbreathing engines'), ('Động cơ tên lửa', 'Rocket engines'), ('Động cơ điện', 'Electric engines')],
       0, B('Cả hai lấy không khí khí quyển làm chất oxy hoá nên là airbreathing; nhánh non-airbreathing là tên lửa (tr.13–14).', 'Both take atmospheric air as oxidiser, so they are airbreathing; the non-airbreathing branch is the rocket (pp.13–14).'), 1, T_CLS, sx(13))
    tq(B('Slide Ch.1 tr.14: tên lửa không dùng không khí nên có thể hoạt động trong chân không vì nó mang theo cả chất oxy hoá lẫn nhiên liệu.', 'Slide Ch.1 p.14: a rocket does not use air, so it can operate in a vacuum because it carries both oxidiser and fuel.'),
       True, B('Hình tr.14 chỉ rõ "Oxidiser" và "Fuel" đưa vào buồng đốt; nhờ đó tên lửa hoạt động ngoài khí quyển, còn ramjet, turbojet… phụ thuộc vào không khí.', 'The figure on p.14 shows "Oxidiser" and "Fuel" feeding the combustion chamber; that is why a rocket works outside the atmosphere while ramjets, turbojets etc. depend on air.'), 1, T_CLS, sx(14))
    cq(B('Slide Ch.1 tr.16: bốn kỳ của động cơ piston bốn kỳ, theo thứ tự vòng làm việc, là:', 'Slide Ch.1 p.16: the four strokes of a four-stroke piston engine, in working order, are:'),
       [('nạp, nén, sinh công (cháy–giãn nở), xả', 'intake, compression, power (combustion–expansion), exhaust'), ('nạp, sinh công, nén, xả', 'intake, power, compression, exhaust'), ('nén, nạp, xả, sinh công', 'compression, intake, exhaust, power'), ('nạp, nén, xả, sinh công', 'intake, compression, exhaust, power')],
       0, B('Intake → Compression → Power → Exhaust (các đĩa màu trên hình tr.16). Trong động cơ piston bốn giai đoạn này diễn ra lần lượt trong cùng một xi-lanh; trong động cơ phản lực chúng diễn ra đồng thời ở các bộ phận khác nhau.', 'Intake → Compression → Power → Exhaust (coloured discs in the figure on p.16). In a piston engine the four phases follow each other in the same cylinder; in a jet engine they occur simultaneously in different components.'), 1, T_CLS, sx(16), fixed=True)
    # --- jet engines tr.17-26
    tq(B('Slide Ch.1 tr.17: động cơ phản lực chỉ cần bugi để khởi động và không cần hệ thống đánh lửa liên tục hay bộ chế hoà khí như động cơ piston.', 'Slide Ch.1 p.17: a jet engine uses spark plugs only for starting and needs neither the continuous ignition system nor the carburetor of a piston engine.'),
       True, B('Cháy trong buồng đốt phản lực là liên tục nên chỉ cần mồi lửa khi khởi động; cùng với khả năng bay cao và nhanh, đó là lý do phản lực thay thế piston từ thập niên 1940.', 'Combustion in a jet combustor is continuous, so ignition is needed only at start; together with higher altitude and speed capability this is why jets replaced pistons from the 1940s.'), 1, T_JET, sx(17))
    cq(B('Slide Ch.1 tr.18–19: ramjet thích hợp nhất với điều kiện nào và có đặc điểm gì?', 'Slide Ch.1 pp.18–19: under which condition is a ramjet most suitable and what is its feature?'),
       [('chỉ hiệu quả ở tốc độ cao; không có chi tiết cơ khí chuyển động; cần vận tốc ban đầu từ nguồn ngoài', 'efficient at high speed only; no moving mechanical parts; needs initial motion from an external source'), ('hiệu quả ở mọi tốc độ kể cả đứng yên; có máy nén hướng trục', 'efficient at all speeds including standstill; has an axial compressor'),
        ('chỉ hiệu quả ở tốc độ thấp; có van một chiều lò xo', 'efficient at low speed only; has spring-loaded one-way valves'), ('hiệu quả ở tốc độ cao; dùng tuabin dẫn động cánh quạt', 'efficient at high speed; uses a turbine driving a propeller')],
       0, B('Ramjet nén không khí bằng hiệu ứng ram ở cửa hút nên chỉ có lực đẩy thực khi bay đủ nhanh; không có máy nén/tuabin; ứng dụng điển hình là tên lửa hành trình BrahMos (tr.19).', 'The ramjet compresses air by the ram effect in the inlet, so it gives net thrust only when flying fast enough; no compressor/turbine; a typical application is the BrahMos cruise missile (p.19).'), 2, T_JET, sx(18))
    tq(B('Slide Ch.1 tr.20–21: pulsejet có van hoạt động giống ramjet nhưng thêm van một chiều lò xo, nên quá trình cháy gián đoạn (theo xung); pulsejet không van dựa vào sóng áp suất truyền qua lại trong động cơ.', 'Slide Ch.1 pp.20–21: a valved pulsejet works like a ramjet plus spring-loaded one-way valves, so combustion is intermittent (pulsing); the valveless pulsejet relies on pressure waves travelling back and forth in the engine.'),
       True, B('Van đóng khi áp suất cháy tăng, buộc khí xả ra phía sau; áp suất giảm thì van mở nạp khí mới. Loại không van thay van bằng sóng áp suất, không có chi tiết mòn (slide tr.20 minh hoạ bằng PULSJET ARGUS AR 019-014 trên đường ray phóng; El-Sayed §1.4.2 nêu bom bay V-1).', 'The valves close as combustion pressure rises, forcing gas rearwards; when pressure falls they open to admit fresh air. The valveless type replaces valves by pressure waves, with no wearing parts (p.20 illustrates it with the PULSJET ARGUS AR 019-014 on a launch rail; El-Sayed §1.4.2 mentions the V-1 buzz bomb).'), 2, T_JET, sx(20))
    cq(B('Slide Ch.1 tr.22: scramjet khác ramjet thông thường ở điểm nào?', 'Slide Ch.1 p.22: how does a scramjet differ from a conventional ramjet?'),
       [('Cháy diễn ra khi không khí qua động cơ vẫn siêu âm', 'Combustion takes place while the air through the engine is still supersonic'), ('Không khí bị làm chậm xuống cận âm trước khi cháy', 'The air is slowed to subsonic speed before combustion'),
        ('Có thêm máy nén ly tâm để nén khí ở tốc độ thấp', 'It adds a centrifugal compressor for compression at low speed'), ('Mang theo oxy lỏng riêng để cháy', 'It carries its own liquid oxygen for combustion')],
       0, B('Scramjet = Supersonic Combustion RAMJET; vì không phải hãm dòng xuống cận âm nên tổn thất ít hơn ở tốc độ rất lớn và đạt tốc độ cao hơn ramjet (tr.22). Phương án "mang oxy riêng" là turborocket.', 'Scramjet = Supersonic Combustion RAMJET; since the flow need not be slowed to subsonic speed it loses less at very high speeds and exceeds ramjet speeds (p.22). The "own oxygen" option is the turborocket.'), 1, T_JET, sx(22))
    cq(B('Slide Ch.1 tr.24: turboramjet là:', 'Slide Ch.1 p.24: a turboramjet is:'),
       [('một turbojet đặt bên trong một ramjet; van rẽ dòng chặn khí vào turbojet ở chế độ ramjet', 'a turbojet mounted inside a ramjet; bypass flaps block the flow into the turbojet in ramjet mode'), ('một ramjet đặt bên trong một turbojet; van rẽ dòng chặn khí vào ramjet ở chế độ turbojet', 'a ramjet mounted inside a turbojet; bypass flaps block the flow into the ramjet in turbojet mode'),
        ('một turbojet và một tên lửa dùng chung buồng đốt', 'a turbojet and a rocket sharing the combustor'), ('một turbofan có cánh quạt không bọc ống', 'a turbofan with an unducted fan')],
       0, B('Hình tr.24: (a) van rẽ dòng cho khí vào turbojet; (b) van chặn khi chuyển sang ramjet ở tốc độ cao. Ứng dụng: SR-71 Blackbird, "máy bay phản lực nhanh nhất thế giới: Ma 3" (tr.25).', 'Figure p.24: (a) bypass flaps let flow into the turbojet; (b) flaps block it in ramjet mode at high speed. Application: SR-71 Blackbird, "the world\'s fastest jet-powered plane: Mach 3" (p.25).'), 2, T_JET, sx(24))
    tq(B('Slide Ch.1 tr.26: turborocket mang theo oxy của riêng nó và tiêu hao nhiên liệu nhiều hơn turboramjet, phù hợp với máy bay đánh chặn hoặc phương tiện phóng có hành trình toàn tăng tốc, ngắn.', 'Slide Ch.1 p.26: a turborocket carries its own oxygen and burns more fuel than a turboramjet; it suits interceptors or space launchers with an entirely accelerative, short flight plan.'),
       True, B('Vì có oxy riêng nên không bị giới hạn bởi không khí loãng ở độ cao lớn, nhưng khối lượng oxy làm tăng tiêu hao; thích hợp hành trình ngắn (tr.26).', 'With its own oxygen it is not limited by thin air at high altitude, but the oxygen mass raises consumption; hence short missions (p.26).'), 1, T_JET, sx(26))
    # --- gas turbines tr.27-42
    cq(B('Slide Ch.1 tr.27: bốn họ chính trong khung nét đứt của nhánh gas turbine là:', 'Slide Ch.1 p.27: the four main families in the dashed box of the gas-turbine branch are:'),
       [('turbojet, turboprop, turboshaft, turbofan', 'turbojet, turboprop, turboshaft, turbofan'), ('turbojet, ramjet, scramjet, turbofan', 'turbojet, ramjet, scramjet, turbofan'), ('turboprop, turboshaft, pulsejet, turborocket', 'turboprop, turboshaft, pulsejet, turborocket'), ('turbojet, turbofan, propfan, rocket', 'turbojet, turbofan, propfan, rocket')],
       0, B('Ngoài khung còn propfan/turboprofan và advanced ducted fan. Ramjet, scramjet, pulsejet, turboramjet, turborocket là các nhánh jet propulsion khác trên cây phân loại tr.13.', 'Outside the box are propfan/turboprofan and advanced ducted fan. Ramjet, scramjet, pulsejet, turboramjet and turborocket are other jet-propulsion branches of the tree on p.13.'), 1, T_CLS, sx(27))
    tq(B('Slide Ch.1 tr.28: trong turbojet, tuabin lấy từ khí cháy năng lượng cần thiết để dẫn động máy nén; phần năng lượng còn lại giãn nở trong ống phun tạo lực đẩy.', 'Slide Ch.1 p.28: in a turbojet the turbine extracts from the gases the energy needed to drive the compressor; the remaining energy expands in the nozzle to produce thrust.'),
       True, B('Tuabin và máy nén nối cùng một trục; công tuabin = công máy nén (cộng tổn thất cơ khí). Phần enthalpy còn lại biến thành động năng phụt (xem chương 2: chu trình Brayton).', 'Turbine and compressor share a shaft; turbine work = compressor work (plus mechanical losses). The remaining enthalpy becomes jet kinetic energy (see chapter 2: Brayton cycle).'), 1, T_JET, sx(28))
    cq(B('Slide Ch.1 tr.31: trong turboprop, lực đẩy chủ yếu do bộ phận nào cung cấp?', 'Slide Ch.1 p.31: in a turboprop, which component provides most of the thrust?'),
       [('Cánh quạt, được tuabin dẫn động qua hộp giảm tốc', 'The propeller, driven by the turbine through a reduction gearbox'), ('Ống phun của bộ phát khí', 'The gas-generator thrust nozzle'), ('Quạt bọc ống phía trước', 'The ducted fan at the front'), ('Bộ đốt sau', 'The afterburner')],
       0, B('"The propulsive force is provided by the propeller and not by a thrust nozzle" (tr.31); ống xả chỉ thoát khí cháy và cho lực đẩy dư. Vì thế turboprop thuộc nhóm phản lực gián tiếp (tr.45).', '"The propulsive force is provided by the propeller and not by a thrust nozzle" (p.31); the exhaust only evacuates burnt gas and gives a residual thrust. So the turboprop belongs to indirect reaction (p.45).'), 1, T_JET, sx(31))
    cq(B('Slide Ch.1 tr.32: dải tốc độ và độ cao mà turboprop hiệu quả hơn turbojet, theo slide, là:', 'Slide Ch.1 p.32: the speed and altitude range where a turboprop is more efficient than a turbojet, per the slide, is:'),
       [('dưới 400–450 mph và dưới 30 000 ft', 'below 400–450 mph and below 30,000 ft'), ('trên 400–450 mph và trên 30 000 ft', 'above 400–450 mph and above 30,000 ft'), ('dưới 400–450 mph và trên 30 000 ft', 'below 400–450 mph and above 30,000 ft'), ('trên 400–450 mph và dưới 30 000 ft', 'above 400–450 mph and below 30,000 ft')],
       0, B('Cánh quạt hiệu quả ở tốc độ thấp hơn, đầu cánh quay dưới tốc độ siêu âm; turbojet hiệu quả hơn ở tốc độ và độ cao lớn hơn. 400–450 mph ≈ 640–720 km/h; 30 000 ft ≈ 9.1 km.', 'The propeller is efficient at lower speed with tips turning below the speed of sound; the turbojet is better at higher speed and altitude. 400–450 mph ≈ 640–720 km/h; 30,000 ft ≈ 9.1 km.'), 2, T_JET, sx(32), fixed=True)
    tq(B('Slide Ch.1 tr.34–35: turboshaft dùng cho trực thăng; hộp số chính thuộc về trực thăng chứ không thuộc động cơ, và lực đẩy dư được tránh bằng cách cho giãn nở thêm trong tuabin hoặc quay ống xả 90°.', 'Slide Ch.1 pp.34–35: the turboshaft is used for helicopters; the main gearbox belongs to the vehicle, not the engine, and residual thrust is avoided by further expansion in the turbine or by turning the exhaust 90°.'),
       True, B('Tuabin công suất tự do (free power turbine) lấy gần hết năng lượng khí thành công trục; khí xả ra có năng lượng thấp nên lực đẩy dư không đáng kể.', 'The free power turbine takes almost all the gas energy as shaft work; the exhaust has little energy left so residual thrust is negligible.'), 1, T_JET, sx(35))
    cq(B('Slide Ch.1 tr.37: tỉ số rẽ nhánh (bypass ratio) của turbofan được định nghĩa là:', 'Slide Ch.1 p.37: the bypass ratio of a turbofan is defined as:'),
       [('lưu lượng khối lượng dòng rẽ nhánh chia lưu lượng khối lượng vào lõi', 'bypass mass flow rate divided by the mass flow rate entering the core'), ('lưu lượng khối lượng vào lõi chia lưu lượng khối lượng dòng rẽ nhánh', 'core mass flow rate divided by the bypass mass flow rate'),
        ('lưu lượng dòng rẽ nhánh chia tổng lưu lượng qua động cơ', 'bypass flow divided by the total engine flow'), ('lực đẩy của quạt chia lực đẩy của lõi', 'fan thrust divided by core thrust')],
       0, B('BPR = ṁ_c/ṁ_h (lạnh/nóng). Ví dụ BPR = 5 ⇒ ṁ_c = 5/6·ṁ_a, ṁ_h = 1/6·ṁ_a. Phương án chia cho tổng lưu lượng cho kết quả bé hơn 1 và không phải BPR.', 'BPR = ṁ_c/ṁ_h (cold/hot). E.g. BPR = 5 ⇒ ṁ_c = 5/6·ṁ_a, ṁ_h = 1/6·ṁ_a. Dividing by the total flow gives a number below 1, which is not the BPR.'), 1, T_JET, sx(37))
    cq(B('Slide Ch.1 tr.37: so với turbojet, hai lợi ích chính của turbofan trên slide là:', 'Slide Ch.1 p.37: compared with a turbojet, the two main benefits of the turbofan on the slide are:'),
       [('hiệu suất đẩy và hiệu suất tổng tốt hơn; ồn giảm', 'better propulsive and global efficiency; lower noise'), ('hiệu suất đẩy thấp hơn nhưng lực đẩy lớn hơn; ồn tăng', 'lower propulsive efficiency but more thrust; higher noise'), ('không cần máy nén; nhẹ hơn', 'no compressor needed; lighter'), ('bay được ở Ma 3; không cần nhiên liệu', 'can fly at Mach 3; needs no fuel')],
       0, B('Khối lượng không khí lớn hơn được tăng tốc ít hơn nên ue gần u hơn: η_p = 2/(1 + ue/u) tăng (tr.37); vận tốc phụt nhỏ hơn làm giảm tiếng ồn.', 'A larger air mass is accelerated less, so ue is closer to u and η_p = 2/(1 + ue/u) rises (p.37); a lower jet speed reduces noise.'), 1, T_JET, sx(37))
    tq(B('Slide Ch.1 tr.38: trong turbofan hai trục, cụm trục thấp áp (LP spool) và cao áp (HP spool) độc lập về cơ khí, nhờ vậy ghép máy nén–tuabin tốt hơn và giảm khối lượng, chiều dài.', 'Slide Ch.1 p.38: in a twin-spool turbofan the low-pressure (LP) and high-pressure (HP) spools are mechanically independent, giving better compressor–turbine matching and less weight and length.'),
       True, B('"1 spool = 1 cụm máy nén–tuabin". Mỗi cụm quay ở tốc độ tối ưu riêng; tăng lực đẩy mà không tăng kích thước động cơ (tr.38).', '"1 spool = 1 compressor–turbine assembly". Each assembly turns at its own optimum speed; thrust rises without increasing engine size (p.38).'), 2, T_JET, sx(38))
    tq(B('Slide Ch.1 tr.40 và tr.42: Trent XWB (Airbus A350) là động cơ hai trục, còn CFM56 (họ Airbus A320) là động cơ ba trục.', 'Slide Ch.1 pp.40 and 42: the Trent XWB (Airbus A350) is a two-spool engine and the CFM56 (Airbus A320 family) is a three-spool engine.'),
       False, B('Ngược lại: Trent XWB là 3 trục (3 spool), CFM56 là 2 trục (2 spool), theo chú thích trên slide.', 'The opposite: the Trent XWB is 3-spool and the CFM56 is 2-spool, as the slide captions say.'), 2, T_JET, sx(40))
    # --- direct / indirect tr.43-47
    cq(B('Slide Ch.1 tr.43–45: động cơ nào thuộc phản lực trực tiếp mà toàn bộ năng lượng khí E chuyển hoàn toàn thành động năng E_c dùng để đẩy?', 'Slide Ch.1 pp.43–45: which engines belong to direct reaction with the whole gas energy E turned into kinetic energy E_c used for propulsion?'),
       [('Tên lửa và ramjet', 'Rockets and ramjets'), ('Turbojet', 'Turbojets'), ('Turboshaft và turboprop', 'Turboshaft and turboprop engines'), ('Động cơ piston', 'Reciprocating engines')],
       0, B('Tr.43: tất cả năng lượng khí là E_c (tên lửa, ramjet). Tr.44: turbojet vẫn là phản lực trực tiếp nhưng một phần nhỏ chuyển thành cơ năng E_m (kéo máy nén) . Tr.45: turboshaft/turboprop là gián tiếp (phần chính là E_m).', 'p.43: all the gas energy is E_c (rockets, ramjets). p.44: the turbojet is still direct reaction but a small part becomes mechanical energy E_m (driving the compressor). p.45: turboshaft/turboprop are indirect (main part E_m).'), 2, T_CLS, sx(43))
    cq(B('Slide Ch.1 tr.45: "phản lực gián tiếp" (indirect reaction) nghĩa là phần chính của năng lượng khí E được biến thành:', 'Slide Ch.1 p.45: "indirect reaction propulsion" means the main part of the gas energy E is transformed into:'),
       [('cơ năng E_m, dùng để đẩy qua cánh quạt hoặc rôto', 'mechanical energy E_m, used for propulsion through a propeller or rotor'), ('động năng E_c, dùng để đẩy trực tiếp qua ống phun', 'kinetic energy E_c, used directly through the nozzle'), ('nhiệt thải ra khí quyển', 'heat rejected to the atmosphere'), ('năng lượng điện nạp vào ắc quy', 'electric energy stored in a battery')],
       0, B('Turboshaft và turboprop: phần chính là E_m, phần còn lại thành E_c (lực đẩy dư). Turbojet đảo lại: phần chính là E_c (tr.44).', 'Turboshaft and turboprop: the main part is E_m and the rest becomes E_c (residual thrust). The turbojet is the opposite: the main part is E_c (p.44).'), 1, T_CLS, sx(45))
    cq(B('Slide Ch.1 tr.46–47: "gas generator" (bộ phát khí) là:', 'Slide Ch.1 p.46–47: the "gas generator" is:'),
       [('phần của cụm động cơ trong đó thực hiện chu trình nhiệt động cần thiết để sinh năng lượng', 'the part of the engine assembly in which the thermodynamic cycle necessary to produce energy is achieved'), ('bộ phận cung cấp khí nén cho cabin', 'the component that supplies compressed air to the cabin'),
        ('máy phát điện gắn với trục cánh quạt', 'the electric generator attached to the propeller shaft'), ('bộ khởi động bằng khí nén', 'the compressed-air starter')],
       0, B('Gas generator = máy nén + buồng đốt + tuabin dẫn máy nén (hình tr.46). Gắn thêm vòi phun thì thành turbojet; lấy khí nén ra thì thành turbo-air generator; lấy công trục ra thì thành APU (tr.47).', 'Gas generator = compressor + combustor + compressor turbine (figure p.46). Adding a nozzle gives a turbojet; bleeding compressed air gives a turbo-air generator; extracting shaft work gives an APU (p.47).'), 1, T_CLS, sx(46))
    cq(B('Slide Ch.1 tr.47: "turbo-air generator" và "auxiliary power unit" khác nhau ở sản phẩm đầu ra:', 'Slide Ch.1 p.47: the "turbo-air generator" and the "auxiliary power unit" differ in their output:'),
       [('khí nén cấp ra (turbo-air generator) và công/năng lượng cho các ứng dụng khác (APU)', 'delivered compressed air (turbo-air generator) and energy for various applications (APU)'), ('lực đẩy (turbo-air generator) và khí nén (APU)', 'thrust (turbo-air generator) and compressed air (APU)'),
        ('công trục (turbo-air generator) và lực đẩy (APU)', 'shaft work (turbo-air generator) and thrust (APU)'), ('chúng không khác nhau', 'they do not differ')],
       0, B('Slide ghi "Delivery of air under pressure" cho turbo-air generator và "Energy used for various applications" cho APU; hình APU có hai mũi tên công W1, W2 (slide không nói rõ ý nghĩa của W1, W2).', 'The slide says "Delivery of air under pressure" for the turbo-air generator and "Energy used for various applications" for the APU; the APU figure shows two work arrows W1 and W2 (the slide does not explain W1 and W2).'), 2, T_CLS, sx(47))
    # --- application tr.48
    cq(B('Slide Ch.1 tr.48 (đồ thị độ cao – vận tốc): theo thứ tự từ thấp/chậm đến cao/nhanh, các động cơ được xếp là:', 'Slide Ch.1 p.48 (altitude–speed chart): from low/slow to high/fast the engines are ordered:'),
       [('turboshaft, turboprop, turbofan (by-pass turbojet), turbojet, ramjet, tên lửa', 'turboshaft, turboprop, turbofan (by-pass turbojet), turbojet, ramjet, rocket'), ('turboprop, turboshaft, turbojet, turbofan, tên lửa, ramjet', 'turboprop, turboshaft, turbojet, turbofan, rocket, ramjet'),
        ('turbojet, turbofan, turboprop, turboshaft, ramjet, tên lửa', 'turbojet, turbofan, turboprop, turboshaft, ramjet, rocket'), ('tên lửa, ramjet, turbojet, turbofan, turboprop, turboshaft', 'rocket, ramjet, turbojet, turbofan, turboprop, turboshaft')],
       0, B('Trực thăng (turboshaft) sát mặt đất; turboprop thấp hơn (dưới ~9 km trên hình); turbofan ~10 km (máy bay dân dụng); turbojet (Concorde, Rafale) cao và nhanh hơn; ramjet ~25 km; tên lửa trên ~40 km.', 'Helicopters (turboshaft) near the ground; turboprops lower down (below ~9 km on the chart); turbofans ~10 km (airliners); turbojets (Concorde, Rafale) higher and faster; ramjet ~25 km; rockets above ~40 km.'), 2, T_APP, sx(48), fixed=True)
    # --- ISA (slide 48 + Farokhi Appendix A)
    cq(B('Slide Ch.1 tr.48 ghi tropopause ("~10–11 km") tại −56 °C và 264 hPa. Theo khí quyển chuẩn ISA (Farokhi Appendix A), áp suất tại độ cao 11 km (đỉnh tầng đối lưu theo ISA) là:', 'Slide Ch.1 p.48 labels the tropopause ("~10–11 km") at −56 °C and 264 hPa. According to the ISA (Farokhi Appendix A), the pressure at 11 km (ISA tropopause) is:'),
       [('khoảng 226.3 hPa', 'about 226.3 hPa'), ('khoảng 264 hPa', 'about 264 hPa'), ('khoảng 101.3 hPa', 'about 101.3 hPa'), ('khoảng 500 hPa', 'about 500 hPa')],
       0, B('ISA: p(11 km) = 101 325×(216.65/288.15)^5.2559 = 22 632 Pa = 226.3 hPa; nằm giữa 26.50 kPa (10 km) và 19.40 kPa (12 km) của bảng Farokhi. 264 hPa là áp suất ở 10 km (ISA 264.4 hPa), còn −56 °C là nhiệt độ ở 11 km: slide ghép giá trị của hai độ cao khác nhau.', 'ISA: p(11 km) = 101,325×(216.65/288.15)^5.2559 = 22,632 Pa = 226.3 hPa; it lies between 26.50 kPa (10 km) and 19.40 kPa (12 km) of the Farokhi table. 264 hPa is the pressure at 10 km (ISA 264.4 hPa) while −56 °C is the temperature at 11 km: the slide pairs values of two different altitudes.'), 2, T_ISA, sx(48))
    # --- false statements (balance True/False)
    tq(B('Slide Ch.1 tr.8: trong đẩy bằng cánh quạt ("propulsion by action"), một khối lượng khí nhỏ được hất ra sau với gia tốc rất lớn.', 'Slide Ch.1 p.8: in propeller propulsion ("propulsion by action") a small mass of air is expelled rearwards with a very great acceleration.'),
       False, B('Ngược lại: cánh quạt hất một khối lượng khí lớn ra sau và chỉ tăng tốc nhẹ (tr.8). "Khối lượng nhỏ, gia tốc lớn" là đặc trưng của phản lực (tr.10).', 'The opposite: a propeller expels a large mass of air with only a low increase of speed (p.8). "Small mass, great acceleration" characterises jet reaction (p.10).'), 1, T_PRI, sx(8))
    tq(B('Slide Ch.1 tr.18–19: ramjet hiệu quả ở tốc độ thấp và có thể tự khởi động từ trạng thái đứng yên.', 'Slide Ch.1 pp.18–19: a ramjet is efficient at low speed and can start by itself from standstill.'),
       False, B('Ramjet chỉ hiệu quả ở tốc độ cao (tr.18) và cần được cấp chuyển động từ nguồn ngoài (tr.19): nén chỉ nhờ hiệu ứng ram, nên thiếu lực đẩy tĩnh.', 'A ramjet is efficient only at high speed (p.18) and needs motion imparted from an external source (p.19): compression comes only from the ram effect, so there is no static thrust.'), 1, T_JET, sx(18))
    tq(B('Slide Ch.1 tr.13: động cơ tuabin khí (gas turbine) thuộc nhánh không hút khí (non-airbreathing).', 'Slide Ch.1 p.13: the gas turbine engine belongs to the non-airbreathing branch.'),
       False, B('Gas turbine nằm dưới Jet propulsion engines của nhánh Airbreathing: nó lấy không khí làm chất oxy hoá. Chỉ tên lửa mới là non-airbreathing.', 'The gas turbine sits under Jet propulsion engines of the Airbreathing branch: it takes air as oxidiser. Only the rocket is non-airbreathing.'), 1, T_CLS, sx(13))
    tq(B('Slide Ch.1 tr.31: trong turboprop, lực đẩy chính do ống phun cung cấp còn cánh quạt chỉ phụ trợ.', 'Slide Ch.1 p.31: in a turboprop the main thrust comes from the nozzle and the propeller only assists.'),
       False, B('Ngược lại: "The propulsive force is provided by the propeller and not by a thrust nozzle". Ống xả chỉ thoát khí cháy từ bộ phát khí.', 'The opposite: "The propulsive force is provided by the propeller and not by a thrust nozzle". The exhaust only evacuates burnt gas from the gas generator.'), 1, T_JET, sx(31))
    tq(B('Slide Ch.1 tr.37: so với turbojet, turbofan làm tăng tiếng ồn nhưng giảm hiệu suất đẩy.', 'Slide Ch.1 p.37: compared with a turbojet, the turbofan increases noise but lowers propulsive efficiency.'),
       False, B('Turbofan cho hiệu suất đẩy và hiệu suất tổng tốt hơn, tiếng ồn giảm (tr.37) nhờ vận tốc phụt thấp hơn trên khối lượng khí lớn hơn.', 'The turbofan gives better propulsive and global efficiency and lower noise (p.37) thanks to a lower jet speed on a larger air mass.'), 1, T_JET, sx(37))
    tq(B('Slide Ch.1 tr.44: turbojet thuộc loại phản lực gián tiếp vì phần chính của năng lượng khí biến thành cơ năng E_m.', 'Slide Ch.1 p.44: the turbojet is indirect reaction propulsion because the main part of the gas energy becomes mechanical energy E_m.'),
       False, B('Tr.44: turbojet là phản lực TRỰC TIẾP; phần chính của năng lượng thành động năng E_c dùng để đẩy, phần còn lại thành E_m (kéo máy nén). Gián tiếp là turboshaft và turboprop (tr.45).', 'p.44: the turbojet is DIRECT reaction; the main part of the energy becomes kinetic energy E_c for propulsion and the rest E_m (driving the compressor). Indirect reaction is the turboshaft and turboprop (p.45).'), 2, T_CLS, sx(44))
    tq(B('Slide Ch.1 tr.22: scramjet làm không khí chậm xuống tốc độ cận âm trước khi cháy giống ramjet thông thường.', 'Slide Ch.1 p.22: a scramjet slows the air to subsonic speed before combustion, like a conventional ramjet.'),
       False, B('Điểm khác biệt là scramjet cháy khi dòng vẫn siêu âm ("Combustion takes place at supersonic air velocities"); ramjet thông thường mới làm chậm dòng xuống cận âm.', 'The difference is that the scramjet burns while the flow is still supersonic ("Combustion takes place at supersonic air velocities"); the conventional ramjet slows the flow to subsonic speed.'), 1, T_JET, sx(22))
    tq(B('Slide Ch.1 tr.35: hộp số chính của trực thăng thuộc về động cơ turboshaft.', 'Slide Ch.1 p.35: the main gearbox of a helicopter is part of the turboshaft engine.'),
       False, B('Slide nhấn mạnh: hộp số chính là một phần của phương tiện (hộp giảm tốc rôto), không phải của động cơ. Ở turboprop thì hộp giảm tốc cánh quạt thuộc cụm động cơ (tr.31).', 'The slide stresses that the main gearbox is part of the vehicle (rotor reduction gearbox), not of the engine. In a turboprop the propeller reduction gearbox is part of the engine assembly (p.31).'), 2, T_JET, sx(35))
    tq(B('Slide Ch.1 tr.30: Rolls-Royce/Snecma Olympus 593 của Concorde là động cơ turboprop.', 'Slide Ch.1 p.30: the Rolls-Royce/Snecma Olympus 593 of the Concorde is a turboprop engine.'),
       False, B('Slide xếp Olympus 593 ở mục "Turbojet – Application" (Concorde); El-Sayed §1.5.1 nêu Concorde là máy bay dân dụng duy nhất có bộ đốt sau.', 'The slide lists the Olympus 593 under "Turbojet – Application" (Concorde); El-Sayed §1.5.1 notes the Concorde was the only civil transport with afterburners.'), 1, T_JET, sx(30))
    tq(B('Slide Ch.1 tr.48: đồ thị cho thấy turboshaft và turboprop hoạt động ở vùng độ cao lớn hơn vùng của ramjet và tên lửa.', 'Slide Ch.1 p.48: the chart shows turboshaft and turboprop operating at higher altitudes than ramjets and rockets.'),
       False, B('Ngược lại: turboshaft/turboprop ở vùng thấp, chậm (sát mặt đất đến khoảng 9 km trên hình); ramjet ~25 km và tên lửa ~40 km trở lên.', 'The opposite: turboshaft/turboprop are in the low, slow region (near the ground up to about 9 km on the chart); ramjet ~25 km and rockets ~40 km and above.'), 1, T_APP, sx(48))
    return Q

# ======================================================================================== generated numeric
def generated():
    rng = random.Random(20261113); Q = []
    def add(item): Q.append(item)
    def four(correct, wrongs, unit, nd):
        o = numopts(correct, wrongs, unit, nd)
        return o
    seen_q = set()
    def mkq(q, correct, wrongs, unit, nd, expl, level, topic, what, check):
        o = four(correct, wrongs, unit, nd)
        if len(o) < 4 or q['en'] in seen_q:
            if REG and REG[-1]['kind'] != 'dup': REG.pop()      # the registry entry of a dropped duplicate is removed too
            return False
        seen_q.add(q['en'])
        add(mcq(q, o, 0, expl, level, topic, GEN(*what), 'bo_sung', check)); return True
    # G1 thrust (unchoked)
    for _ in range(4):
        ma = rng.choice([20, 30, 45, 60, 80, 100, 120]); f = rng.choice([.01, .015, .02, .025]); ue = rng.choice([450, 500, 600, 700, 800]); u = rng.choice([100, 150, 200, 250])
        T = reg('g_thrust', dict(ma=ma, f=f, ue=ue, u=u), thrust(ma, f, ue, u))
        mkq(B(f'Động cơ phản lực hút {ma} kg/s không khí, f = {f}, vận tốc phụt {ue} m/s (vòi giãn nở hoàn toàn), bay ở {u} m/s. Lực đẩy thực là:', f'A jet engine takes in {ma} kg/s of air, f = {f}, exhaust speed {ue} m/s (fully expanded nozzle), flight speed {u} m/s. The net thrust is:'),
            T/1e3, [ma*(ue-u)/1e3, ma*(1+f)*ue/1e3, ma*((1+f)*ue+u)/1e3], 'kN', 2,
            B(f'T = ṁa[(1+f)ue − u] = {ma}×[{1+f}×{ue} − {u}] = {N(T,0)} N = {N(T/1e3,2)} kN. Bỏ f cho {N(ma*(ue-u)/1e3,2)}; quên trừ lực cản ram ṁa·u cho {N(ma*(1+f)*ue/1e3,2)}; cộng u cho {N(ma*((1+f)*ue+u)/1e3,2)}.',
              f'T = ṁa[(1+f)ue − u] = {ma}×[{1+f}×{ue} − {u}] = {N(T,0)} N = {N(T/1e3,2)} kN. Dropping f gives {N(ma*(ue-u)/1e3,2)}; forgetting the ram drag ṁa·u gives {N(ma*(1+f)*ue/1e3,2)}; adding u gives {N(ma*((1+f)*ue+u)/1e3,2)}.'), 1, T_THR, ('lực đẩy turbojet', 'turbojet thrust'), 'script (verify_m01: g_thrust)')
    # G2 propulsive efficiency simple
    for _ in range(3):
        u = rng.choice([100, 150, 200, 250, 300]); ue = u*rng.choice([1.5, 2, 2.5, 3, 4])
        e = reg('g_etap_s', dict(u=u, ue=ue), eta_p_simple(u, ue))
        mkq(B(f'Động cơ bay ở {u} m/s với vận tốc phụt {N(ue,0)} m/s (vòi giãn nở hoàn toàn, bỏ qua f). Hiệu suất đẩy η_p = 2u/(u + ue) là:', f'An engine flies at {u} m/s with an exhaust speed of {N(ue,0)} m/s (fully expanded nozzle, f neglected). The propulsive efficiency η_p = 2u/(u + ue) is:'),
            e*100, [u/ue*100, (ue-u)/ue*100, 100*ue/(ue+u)], '%', 1,
            B(f'η_p = 2×{u}/({u} + {N(ue,0)}) = {N(e*100,1)} %. Đảo tỉ số cho {N(ue/(ue+u)*100,1)} %; dùng u/ue cho {N(u/ue*100,1)} %. Càng gần ue ≈ u thì η_p càng cao (nhưng lực đẩy càng nhỏ).',
              f'η_p = 2×{u}/({u} + {N(ue,0)}) = {N(e*100,1)} %. Inverting the ratio gives {N(ue/(ue+u)*100,1)} %; using u/ue gives {N(u/ue*100,1)} %. The closer ue is to u, the higher η_p (but the smaller the thrust).'), 1, T_EFF, ('hiệu suất đẩy', 'propulsive efficiency'), 'script (verify_m01: g_etap_s)')
    # G3 propulsive efficiency, first expression, with f
    for _ in range(3):
        ma = rng.choice([40, 50, 80, 100]); f = rng.choice([.015, .02, .03]); ue = rng.choice([500, 600, 700, 800]); u = rng.choice([150, 200, 250, 300])
        T = thrust(ma, f, ue, u); me = ma*(1+f)
        e = reg('g_etap_1', dict(ma=ma, f=f, ue=ue, u=u), eta_p_first(T, u, me, ue))
        e2 = 2*u/(u+ue); e3 = T*u/(.5*ma*((1+f)*ue**2-u**2))
        mkq(B(f'Turbojet: ṁa = {ma} kg/s, f = {f}, ue = {ue} m/s, u = {u} m/s, Pe = Pa. Hiệu suất đẩy theo biểu thức thứ nhất (công đẩy chia công đẩy cộng tổn thất vệt ½ṁe(ue − u)²) là:', f'Turbojet: ṁa = {ma} kg/s, f = {f}, ue = {ue} m/s, u = {u} m/s, Pe = Pa. The propulsive efficiency by the first expression (thrust power over thrust power plus wake loss ½ṁe(ue − u)²) is:'),
            e*100, [e2*100, e3*100 if abs(e3-e) > 5e-4 else e*100+3.0, (ue-u)/ue*100], '%', 2,
            B(f'T = {N(T,0)} N; T·u = {N(T*u/1e6,3)} MW; ½ṁe(ue − u)² = ½×{N(me,1)}×{ue-u}² = {N(.5*me*(ue-u)**2/1e6,3)} MW; η_p = {N(e*100,2)} %. Công thức 2u/(u+ue) = {N(e2*100,2)} % bỏ qua f nên chỉ gần đúng.',
              f'T = {N(T,0)} N; T·u = {N(T*u/1e6,3)} MW; ½ṁe(ue − u)² = ½×{N(me,1)}×{ue-u}² = {N(.5*me*(ue-u)**2/1e6,3)} MW; η_p = {N(e*100,2)} %. The formula 2u/(u+ue) = {N(e2*100,2)} % ignores f, so it is only approximate.'), 3, T_EFF, ('hiệu suất đẩy có f', 'propulsive efficiency with f'), 'script (verify_m01: g_etap_1)')
    # G4 thermal efficiency
    for _ in range(3):
        f = rng.choice([.015, .02, .025]); ue = rng.choice([500, 600, 700, 800]); u = rng.choice([100, 200, 250]); QR = rng.choice([42e6, 43e6, 44e6])
        e = reg('g_etath', dict(f=f, ue=ue, u=u, QR=QR), eta_th_unchoked(f, ue, u, QR))
        mkq(B(f'Turbojet (vòi không nghẹt): f = {f}, ue = {ue} m/s, u = {u} m/s, nhiệt trị QR = {N(QR/1e6,0)} MJ/kg. Hiệu suất nhiệt η_th = [(1+f)ue² − u²]/(2f·QR) là:', f'Turbojet (unchoked nozzle): f = {f}, ue = {ue} m/s, u = {u} m/s, heating value QR = {N(QR/1e6,0)} MJ/kg. The thermal efficiency η_th = [(1+f)ue² − u²]/(2f·QR) is:'),
            e*100, [(ue**2-u**2)/(f*QR)*100, ((1+f)*ue**2-u**2)/(f*QR)*100, ((1+f)*ue**2)/(2*f*QR)*100], '%', 2,
            B(f'Tử số = {N((1+f)*ue**2-u**2,0)} m²/s²; mẫu = 2×{f}×{N(QR/1e6,0)}×10⁶ = {N(2*f*QR,0)}; η_th = {N(e*100,2)} %. Quên hệ số 2 cho {N(((1+f)*ue**2-u**2)/(f*QR)*100,2)} % (vượt quá thực tế); quên trừ u² cho {N(((1+f)*ue**2)/(2*f*QR)*100,2)} %.',
              f'Numerator = {N((1+f)*ue**2-u**2,0)} m²/s²; denominator = 2×{f}×{N(QR/1e6,0)}×10⁶ = {N(2*f*QR,0)}; η_th = {N(e*100,2)} %. Forgetting the factor 2 gives {N(((1+f)*ue**2-u**2)/(f*QR)*100,2)} % (unrealistic); forgetting −u² gives {N(((1+f)*ue**2)/(2*f*QR)*100,2)} %.'), 2, T_EFF, ('hiệu suất nhiệt', 'thermal efficiency'), 'script (verify_m01: g_etath)')
    # G5 overall efficiency from thrust, speed, fuel, QR
    for _ in range(3):
        T = rng.choice([20e3, 30e3, 45e3, 60e3]); u = rng.choice([180, 220, 250, 280]); mf = rng.choice([.5, .75, 1.0, 1.5]); QR = rng.choice([42e6, 43e6, 44e6])
        eo = reg('g_etao', dict(T=T, u=u, mf=mf, QR=QR), T*u/(mf*QR))
        mkq(B(f'Một động cơ cho lực đẩy {N(T/1e3,0)} kN ở vận tốc bay {u} m/s, đốt {mf} kg/s nhiên liệu có nhiệt trị {N(QR/1e6,0)} MJ/kg. Hiệu suất tổng η_o = η_p·η_th là:', f'An engine gives a thrust of {N(T/1e3,0)} kN at {u} m/s and burns {mf} kg/s of fuel of heating value {N(QR/1e6,0)} MJ/kg. The overall efficiency η_o = η_p·η_th is:'),
            eo*100, [T*u/(mf*QR*2)*100, T/(mf*QR)*100*u/100, (T*u/3.6)/(mf*QR)*100], '%', 2,
            B(f'η_o = T·u/(ṁf·QR) = {N(T,0)}×{u}/({mf}×{N(QR,0)}) = {N(eo*100,2)} % (công đẩy chia nhiệt cấp). Quên khi đổi: u phải là m/s (không phải km/h): chia 3.6 cho {N((T*u/3.6)/(mf*QR)*100,2)} %.',
              f'η_o = T·u/(ṁf·QR) = {N(T,0)}×{u}/({mf}×{N(QR,0)}) = {N(eo*100,2)} % (thrust power over fuel heat rate). Beware units: u must be in m/s; dividing by 3.6 wrongly gives {N((T*u/3.6)/(mf*QR)*100,2)} %.'), 2, T_EFF, ('hiệu suất tổng', 'overall efficiency'), 'script (verify_m01: g_etao)')
    # G6 TSFC
    for _ in range(3):
        mf = rng.choice([.4, .6, .8, 1.2, 2.0]); T = rng.choice([8e3, 12e3, 20e3, 30e3])
        ts = reg('g_tsfc', dict(mf=mf, T=T), mf/T*1e6)
        mkq(B(f'Động cơ đốt {mf} kg/s nhiên liệu và sinh lực đẩy {N(T/1e3,0)} kN. TSFC tính bằng mg/(N·s) là:', f'An engine burns {mf} kg/s of fuel and produces {N(T/1e3,0)} kN of thrust. The TSFC in mg/(N·s) is:'),
            ts, [ts/1e3, ts*3.6, ts*1e3], 'mg/(N·s)', 1,
            B(f'TSFC = ṁf/T = {mf}/{N(T,0)} = {N(mf/T,7)} kg/(N·s) = {N(ts,1)} mg/(N·s). Nhầm kg với mg cho hệ số 10³; đổi sang giờ thêm 3600 cho {N(ts*3.6,1)}.',
              f'TSFC = ṁf/T = {mf}/{N(T,0)} = {N(mf/T,7)} kg/(N·s) = {N(ts,1)} mg/(N·s). Confusing kg with mg gives a factor of 10³; converting to hours multiplies by 3600 and gives {N(ts*3.6,1)}.'), 1, T_SFC, ('TSFC', 'TSFC'), 'script (verify_m01: g_tsfc)')
    # G7 ISA at altitude
    for z in rng.sample([2000, 4000, 6000, 8000, 10000], 4):
        T_, p_, r_ = isa(z); reg('g_isa', dict(z=z), dict(T=T_, p=p_, rho=r_), tol=3e-3)
        mkq(B(f'Theo khí quyển chuẩn ISA, áp suất tĩnh ở độ cao {z/1000:g} km (tầng đối lưu, T = 288.15 − 0.0065z) xấp xỉ:', f'According to the ISA, the static pressure at {z/1000:g} km (troposphere, T = 288.15 − 0.0065z) is approximately:'),
            p_/1e3, [101.325*(1-z/44330*1.0)**1.0, 101.325*(T_/288.15), 101.325*(T_/288.15)**3.5], 'kPa', 1,
            B(f'T = 288.15 − 0.0065×{z} = {N(T_,2)} K; p = 101.325×(T/288.15)^5.2559 = {N(p_/1e3,2)} kPa (Farokhi Appendix A, mốc chẵn km, cho sai lệch ≤ 1 %). Nhầm tỉ lệ tuyến tính theo T cho {N(101.325*T_/288.15,1)} kPa: áp suất giảm nhanh hơn nhiệt độ vì mũ 5.26.',
              f'T = 288.15 − 0.0065×{z} = {N(T_,2)} K; p = 101.325×(T/288.15)^5.2559 = {N(p_/1e3,2)} kPa (Farokhi Appendix A at whole kilometres agrees within 1 %). Taking p linear in T gives {N(101.325*T_/288.15,1)} kPa: pressure falls faster than temperature because of the exponent 5.26.'), 2, T_ISA, ('khí quyển ISA', 'ISA'), 'ISA closed form; Farokhi Appendix A (verify_m01: g_isa)')
    # G8 flight speed from Mach number
    for z, M in [(9000, .78), (11000, .85), (3000, .45), (10000, .8)]:
        T_, p_, r_ = isa(z); a_ = math.sqrt(GAM*R_AIR*T_); u = M*a_; reg('g_speed', dict(z=z, M=M), u, tol=2e-3)
        mkq(B(f'Máy bay bay ở Ma {M} tại độ cao {z/1000:g} km (ISA, T = {N(T_,2)} K). Vận tốc bay thực (γ = 1.4, R = 287 J/kg·K) là:', f'An aircraft flies at Ma {M} at {z/1000:g} km (ISA, T = {N(T_,2)} K). The true flight speed (γ = 1.4, R = 287 J/kg·K) is:'),
            u, [M*math.sqrt(GAM*R_AIR*288.15), M*math.sqrt(R_AIR*T_), M*GAM*R_AIR*T_/1000], 'm/s', 1,
            B(f'a = √(γRT) = √(1.4×287×{N(T_,2)}) = {N(a_,1)} m/s; u = Ma·a = {N(u,1)} m/s = {N(u*3.6,0)} km/h. Dùng T mực nước biển (288.15 K) cho {N(M*math.sqrt(GAM*R_AIR*288.15),1)} m/s: vận tốc âm giảm theo độ cao nên cùng Ma thì u nhỏ hơn.',
              f'a = √(γRT) = √(1.4×287×{N(T_,2)}) = {N(a_,1)} m/s; u = Ma·a = {N(u,1)} m/s = {N(u*3.6,0)} km/h. Using the sea-level temperature (288.15 K) gives {N(M*math.sqrt(GAM*R_AIR*288.15),1)} m/s: the speed of sound falls with altitude, so the same Ma means a lower u.'), 3, T_ISA, ('Mach và vận tốc bay', 'Mach number and flight speed'), 'script (verify_m01: g_speed)')
    # G9 Breguet range
    for _ in range(4):
        eo = rng.choice([.20, .25, .30, .35]); QR = rng.choice([42e6, 43e6, 44e6]); LD = rng.choice([10, 14, 16, 18]); r = rng.choice([1.2, 1.3, 1.4, 1.5])
        S = reg('g_breguet', dict(eo=eo, QR=QR, LD=LD, r=r), breguet(eo, QR, LD, r))
        mkq(B(f'Máy bay có η_o = {eo}, nhiệt trị {N(QR/1e6,0)} MJ/kg, L/D = {LD}; khối lượng đầu chặng bay gấp {r} lần cuối chặng. Tầm bay theo Breguet (g = 9.80665 m/s²) là:', f'An aircraft has η_o = {eo}, heating value {N(QR/1e6,0)} MJ/kg, L/D = {LD}; the start-of-cruise mass is {r} times the end mass. The Breguet range (g = 9.80665 m/s²) is:'),
            S/1e3, [S/1e3*(r-1)/math.log(r), S/1e3/LD, S/1e3*math.log(r)/(1-1/r)], 'km', 0,
            B(f'S = η_o·QR/g·(L/D)·ln(m1/m2) = {eo}×{N(QR,0)}/9.80665×{LD}×ln({r}) = {N(S/1e3,0)} km. Lỗi: dùng (m1 − m2)/m2 thay cho ln(m1/m2) cho {N(S/1e3*(r-1)/math.log(r),0)} km; quên L/D cho {N(S/1e3/LD,0)} km.',
              f'S = η_o·QR/g·(L/D)·ln(m1/m2) = {eo}×{N(QR,0)}/9.80665×{LD}×ln({r}) = {N(S/1e3,0)} km. Slips: using (m1 − m2)/m2 instead of ln(m1/m2) gives {N(S/1e3*(r-1)/math.log(r),0)} km; forgetting L/D gives {N(S/1e3/LD,0)} km.'), 3, T_RNG, ('tầm bay Breguet', 'Breguet range'), 'script (verify_m01: g_breguet)')
    # G10 Isp
    for _ in range(2):
        T = rng.choice([80e3, 150e3, 300e3]); mp = rng.choice([30., 60., 100.]); 
        I_ = reg('g_isp', dict(T=T, mp=mp), T/(mp*G0))
        mkq(B(f'Động cơ tên lửa sinh lực đẩy {N(T/1e3,0)} kN, tiêu thụ {N(mp,0)} kg/s thuốc phóng. Xung riêng Is = F/(ṁp·g0) là:', f'A rocket engine produces {N(T/1e3,0)} kN of thrust and consumes {N(mp,0)} kg/s of propellant. The specific impulse Is = F/(ṁp·g0) is:'),
            I_, [T/mp, I_*G0/9.0, I_/2], 's', 1,
            B(f'Is = {N(T,0)}/({N(mp,0)}×9.80665) = {N(I_,1)} s. T/ṁp = {N(T/mp,0)} m/s là vận tốc phụt hiệu dụng, không phải Is (cần chia g0).',
              f'Is = {N(T,0)}/({N(mp,0)}×9.80665) = {N(I_,1)} s. T/ṁp = {N(T/mp,0)} m/s is the effective exhaust velocity, not Is (divide by g0).'), 1, T_SFC, ('xung riêng', 'specific impulse'), 'script (verify_m01: g_isp)')
    # G11 bypass flows
    for _ in range(2):
        ma = rng.choice([200., 400., 600.]); be = rng.choice([4., 5., 8.]); mc = ma*be/(1+be)
        reg('g_bpr', dict(ma=ma, be=be), mc)
        mkq(B(f'Turbofan hút tổng cộng {N(ma,0)} kg/s không khí, tỉ số rẽ nhánh BPR = {N(be,0)}. Lưu lượng đi qua quạt (dòng lạnh, rẽ nhánh) là:', f'A turbofan takes in {N(ma,0)} kg/s of air in total with BPR = {N(be,0)}. The flow through the fan bypass (cold stream) is:'),
            mc, [ma/(1+be), ma*be, ma/be], 'kg/s', 1,
            B(f'BPR = ṁc/ṁh và ṁc + ṁh = ṁa ⇒ ṁc = BPR/(1+BPR)·ṁa = {N(be,0)}/{N(1+be,0)}×{N(ma,0)} = {N(mc,1)} kg/s; lõi chỉ nhận {N(ma/(1+be),1)} kg/s.',
              f'BPR = ṁc/ṁh and ṁc + ṁh = ṁa ⇒ ṁc = BPR/(1+BPR)·ṁa = {N(be,0)}/{N(1+be,0)}×{N(ma,0)} = {N(mc,1)} kg/s; the core receives only {N(ma/(1+be),1)} kg/s.'), 1, T_JET, ('tỉ số rẽ nhánh', 'bypass ratio'), 'script (verify_m01: g_bpr)')
    # G12 turbofan thrust (two streams, unchoked)
    for _ in range(3):
        mh = rng.choice([15., 20., 25.]); be = rng.choice([4., 5., 6.]); f = rng.choice([.02, .025]); uh = rng.choice([450., 500., 550.]); uc = rng.choice([300., 350., 400.]); u = rng.choice([200., 230., 250.])
        Tt = mh*((1+f)*uh-u) + be*mh*(uc-u); reg('g_tf', dict(mh=mh, be=be, f=f, uh=uh, uc=uc, u=u), Tt)
        mkq(B(f'Turbofan (vòi không nghẹt): ṁh = {N(mh,0)} kg/s, BPR = {N(be,0)}, f = {f}, ue,h = {N(uh,0)} m/s, ue,c = {N(uc,0)} m/s, bay ở {N(u,0)} m/s. Lực đẩy thực là:', f'Turbofan (unchoked nozzles): ṁh = {N(mh,0)} kg/s, BPR = {N(be,0)}, f = {f}, ue,h = {N(uh,0)} m/s, ue,c = {N(uc,0)} m/s, flying at {N(u,0)} m/s. The net thrust is:'),
            Tt/1e3, [mh*((1+f)*uh-u)/1e3, ((1+be)*mh*(uc-u)+mh*f*uh)/1e3, (mh*((1+f)*uh-u)+mh*(uc-u))/1e3], 'kN', 2,
            B(f'T = ṁh[(1+f)ue,h − u] + ṁc(ue,c − u) với ṁc = BPR·ṁh = {N(be*mh,0)} kg/s: {N(mh*((1+f)*uh-u),0)} + {N(be*mh*(uc-u),0)} = {N(Tt,0)} N = {N(Tt/1e3,2)} kN. Bỏ dòng quạt chỉ còn {N(mh*((1+f)*uh-u)/1e3,2)} kN (lõi); quên nhân BPR cho dòng quạt cho {N((mh*((1+f)*uh-u)+mh*(uc-u))/1e3,2)} kN.',
              f'T = ṁh[(1+f)ue,h − u] + ṁc(ue,c − u) with ṁc = BPR·ṁh = {N(be*mh,0)} kg/s: {N(mh*((1+f)*uh-u),0)} + {N(be*mh*(uc-u),0)} = {N(Tt,0)} N = {N(Tt/1e3,2)} kN. Dropping the fan stream leaves {N(mh*((1+f)*uh-u)/1e3,2)} kN (core only); forgetting to multiply by BPR for the fan stream gives {N((mh*((1+f)*uh-u)+mh*(uc-u))/1e3,2)} kN.'), 3, T_THR, ('lực đẩy turbofan', 'turbofan thrust'), 'script (verify_m01: g_tf)')
    # G13 cruise thrust from weight and CL/CD
    for _ in range(3):
        m = rng.choice([60e3, 78e3, 120e3, 250e3]); CL = rng.choice([.4, .5, .55]); CD = rng.choice([.02, .025, .03])
        Fx = reg('g_cruise', dict(m=m, CL=CL, CD=CD), CD/CL*m*G0)
        mkq(B(f'Máy bay khối lượng {N(m,0)} kg bay bằng đều với C_L = {CL}, C_D = {CD}. Lực đẩy cần thiết (T_u = F_x = (C_D/C_L)·m·g) là:', f'An aircraft of mass {N(m,0)} kg is in level cruise with C_L = {CL}, C_D = {CD}. The required thrust (T_u = F_x = (C_D/C_L)·m·g) is:'),
            Fx/1e3, [m*G0/1e3, CL/CD*m*G0/1e3, CD*m*G0/1e3], 'kN', 1,
            B(f'P = F_z ⇒ lực đẩy = lực cản = (C_D/C_L)·P = ({CD}/{CL})×{N(m,0)}×9.80665 = {N(Fx/1e3,1)} kN (≈ {N(Fx/(m*G0)*100,1)} % trọng lượng). Đảo tỉ số cho {N(CL/CD*m*G0/1e3,0)} kN (lớn hơn cả trọng lượng, vô lý).',
              f'P = F_z ⇒ thrust = drag = (C_D/C_L)·P = ({CD}/{CL})×{N(m,0)}×9.80665 = {N(Fx/1e3,1)} kN (≈ {N(Fx/(m*G0)*100,1)} % of the weight). Inverting the ratio gives {N(CL/CD*m*G0/1e3,0)} kN (more than the weight, absurd).'), 2, T_AER, ('bốn lực khi bay bằng', 'four forces in cruise'), 'script (verify_m01: g_cruise)')
    # G14 lift
    for _ in range(3):
        z = rng.choice([0, 5000, 10000]); V = rng.choice([70., 120., 230.]); S_ = rng.choice([122., 260., 361.]); CL = rng.choice([.3, .5, 1.2])
        rho = isa(z)[2]; Fz = reg('g_lift', dict(z=z, V=V, S=S_, CL=CL), CL*.5*rho*V**2*S_, tol=3e-3)
        mkq(B(f'Lực nâng F_z = C_L·V²·(ρ/2)·S của máy bay có S = {N(S_,0)} m², C_L = {CL}, V = {N(V,0)} m/s ở {z/1000:g} km (mật độ ISA ρ = {N(rho,4)} kg/m³) là:', f'The lift F_z = C_L·V²·(ρ/2)·S of an aircraft with S = {N(S_,0)} m², C_L = {CL}, V = {N(V,0)} m/s at {z/1000:g} km (ISA density ρ = {N(rho,4)} kg/m³) is:'),
            Fz/1e3, [CL*rho*V**2*S_/1e3, CL*.5*rho*V*S_/1e3, Fz/G0/1e3], 'kN', 1,
            B(f'F_z = {CL}×{N(V,0)}²×({N(rho,4)}/2)×{N(S_,0)} = {N(Fz,0)} N = {N(Fz/1e3,1)} kN. Quên hệ số ½ cho {N(CL*rho*V**2*S_/1e3,1)} kN; dùng V thay V² cho {N(CL*.5*rho*V*S_/1e3,1)} kN.',
              f'F_z = {CL}×{N(V,0)}²×({N(rho,4)}/2)×{N(S_,0)} = {N(Fz,0)} N = {N(Fz/1e3,1)} kN. Forgetting the factor ½ gives {N(CL*rho*V**2*S_/1e3,1)} kN; using V instead of V² gives {N(CL*.5*rho*V*S_/1e3,1)} kN.'), 2, T_AER, ('lực nâng', 'lift'), 'script (verify_m01: g_lift)')
    # G15 turboprop ESP / ESFC
    for _ in range(2):
        SP = rng.choice([1500e3, 2000e3, 2500e3]); Te = rng.choice([1500., 2500.]); u = rng.choice([120., 150.]); epr = rng.choice([.8, .85]); mf = rng.choice([.15, .2, .25])
        ESP = SP + Te*u/epr; esfc = reg('g_esp', dict(SP=SP, Te=Te, u=u, epr=epr, mf=mf), mf/ESP*3.6e9)
        mkq(B(f'Turboprop: công suất trục SP = {N(SP/1e3,0)} kW, lực đẩy khí xả Te = {N(Te,0)} N, bay {N(u,0)} m/s, η_pr = {epr}, nhiên liệu {mf} kg/s. ESFC = ṁf/ESP (ESP = SP + Te·u/η_pr) tính bằng g/(kW·h) là:', f'Turboprop: shaft power SP = {N(SP/1e3,0)} kW, exhaust thrust Te = {N(Te,0)} N, flying at {N(u,0)} m/s, η_pr = {epr}, fuel {mf} kg/s. ESFC = ṁf/ESP (ESP = SP + Te·u/η_pr) in g/(kW·h) is:'),
            esfc, [mf/SP*3.6e9, mf/(SP+Te*u)*3.6e9, mf/(SP+Te*u*epr)*3.6e9], 'g/(kW·h)', 1,
            B(f'ESP = {N(SP,0)} + {N(Te,0)}×{N(u,0)}/{epr} = {N(ESP,0)} W; ESFC = {mf}/{N(ESP,0)} kg/(W·s) = {N(esfc,1)} g/(kW·h). Bỏ phần khí xả cho {N(mf/SP*3.6e9,1)}; bỏ chia η_pr cho {N(mf/(SP+Te*u)*3.6e9,1)}.',
              f'ESP = {N(SP,0)} + {N(Te,0)}×{N(u,0)}/{epr} = {N(ESP,0)} W; ESFC = {mf}/{N(ESP,0)} kg/(W·s) = {N(esfc,1)} g/(kW·h). Dropping the exhaust part gives {N(mf/SP*3.6e9,1)}; not dividing by η_pr gives {N(mf/(SP+Te*u)*3.6e9,1)}.'), 3, T_SFC, ('ESFC của turboprop', 'turboprop ESFC'), 'script (verify_m01: g_esp)')
    # G16 takeoff thrust from thermal efficiency
    for _ in range(2):
        eth = rng.choice([.3, .35, .4]); mf = rng.choice([1.0, 1.5, 2.0]); QR = 43e6; ue = rng.choice([400., 600., 800.])
        Tk = reg('g_takeoff', dict(eth=eth, mf=mf, QR=QR, ue=ue), 2*eth*mf*QR/ue)
        mkq(B(f'Lực đẩy tĩnh (cất cánh) của động cơ không nghẹt: η_th = {eth}, ṁf = {mf} kg/s, QR = 43 MJ/kg, ue = {N(ue,0)} m/s. Dùng T = 2η_th·ṁf·QR/ue, lực đẩy là:', f'Static (takeoff) thrust of an unchoked engine: η_th = {eth}, ṁf = {mf} kg/s, QR = 43 MJ/kg, ue = {N(ue,0)} m/s. Using T = 2η_th·ṁf·QR/ue, the thrust is:'),
            Tk/1e3, [eth*mf*QR/ue/1e3, 2*eth*mf*QR/ue**2, 2*eth*QR/ue/1e3], 'kN', 1,
            B(f'T = 2×{eth}×{mf}×43×10⁶/{N(ue,0)} = {N(Tk,0)} N = {N(Tk/1e3,1)} kN. Với cùng η_th và ṁf, ue lớn thì lực đẩy tĩnh nhỏ (T ∝ 1/ue): lợi thế của turboprop và turbofan khi cất cánh. Quên hệ số 2 cho {N(eth*mf*QR/ue/1e3,1)} kN.',
              f'T = 2×{eth}×{mf}×43×10⁶/{N(ue,0)} = {N(Tk,0)} N = {N(Tk/1e3,1)} kN. For the same η_th and ṁf a larger ue gives a smaller static thrust (T ∝ 1/ue): the takeoff advantage of turboprops and turbofans. Forgetting the factor 2 gives {N(eth*mf*QR/ue/1e3,1)} kN.'), 3, T_THR, ('lực đẩy cất cánh', 'takeoff thrust'), 'script (verify_m01: g_takeoff)')
    # G17 pressure thrust
    for _ in range(2):
        Ae = rng.choice([.2, .3, .5]); pe = rng.choice([80e3, 120e3, 200e3]); pa = rng.choice([20e3, 30e3, 50e3])
        Pt = reg('g_pthrust', dict(Ae=Ae, pe=pe, pa=pa), (pe-pa)*Ae)
        mkq(B(f'Vòi phun nghẹt có Ae = {Ae} m², Pe = {N(pe/1e3,0)} kPa, môi trường Pa = {N(pa/1e3,0)} kPa. Lực đẩy áp suất (Pe − Pa)·Ae là:', f'A choked nozzle has Ae = {Ae} m², Pe = {N(pe/1e3,0)} kPa and ambient Pa = {N(pa/1e3,0)} kPa. The pressure thrust (Pe − Pa)·Ae is:'),
            Pt/1e3, [pe*Ae/1e3, pa*Ae/1e3, (pe+pa)*Ae/1e3], 'kN', 1,
            B(f'(Pe − Pa)·Ae = ({N(pe,0)} − {N(pa,0)})×{Ae} = {N(Pt,0)} N = {N(Pt/1e3,1)} kN, dương vì Pe > Pa (vòi nghẹt, chưa giãn nở hết). Nếu Pe = Pa (vòi giãn nở hoàn toàn) thì bằng 0.',
              f'(Pe − Pa)·Ae = ({N(pe,0)} − {N(pa,0)})×{Ae} = {N(Pt,0)} N = {N(Pt/1e3,1)} kN, positive because Pe > Pa (choked, under-expanded). If Pe = Pa (fully expanded) it is zero.'), 2, T_THR, ('lực đẩy áp suất', 'pressure thrust'), 'script (verify_m01: g_pthrust)')
    # G18 speed needed for level flight at sea level vs altitude
    for _ in range(3):
        m = rng.choice([60e3, 70e3, 78e3]); S_ = rng.choice([122., 122.6, 160.]); CL = rng.choice([.8, .9, 1.0]); z = rng.choice([5000, 8000, 10000])
        rho0 = isa(0)[2]; rz = isa(z)[2]; V0 = math.sqrt(2*m*G0/(rho0*S_*CL)); Vz = math.sqrt(2*m*G0/(rz*S_*CL))
        reg('g_vreq', dict(m=m, S=S_, CL=CL, z=z), Vz, tol=3e-3)
        mkq(B(f'Máy bay {N(m,0)} kg, S = {N(S_,1)} m², bay bằng đều với C_L = {CL} (F_z = P). Vận tốc cần thiết ở {z/1000:g} km (ISA) là:', f'An aircraft of {N(m,0)} kg with S = {N(S_,1)} m² flies level with C_L = {CL} (F_z = P). The required speed at {z/1000:g} km (ISA) is:'),
            Vz, [V0, V0*rz/rho0, Vz**2/100], 'm/s', 1,
            B(f'V = √(2P/(ρ·S·C_L)). Ở mực nước biển ρ = {N(rho0,3)} kg/m³ cho V = {N(V0,1)} m/s; ở {z/1000:g} km ρ = {N(rz,4)} kg/m³ nên V = √(2×{N(m,0)}×9.80665/({N(rz,4)}×{N(S_,1)}×{CL})) = {N(Vz,1)} m/s, tức gấp √(ρ0/ρ) = {N(math.sqrt(rho0/rz),3)} lần. Nhân thay vì lấy căn cho {N(V0*rz/rho0,1)}.',
              f'V = √(2P/(ρ·S·C_L)). At sea level ρ = {N(rho0,3)} kg/m³ gives V = {N(V0,1)} m/s; at {z/1000:g} km ρ = {N(rz,4)} kg/m³ so V = √(2×{N(m,0)}×9.80665/({N(rz,4)}×{N(S_,1)}×{CL})) = {N(Vz,1)} m/s, i.e. √(ρ0/ρ) = {N(math.sqrt(rho0/rz),3)} times larger. Scaling by the ratio instead of its square root gives {N(V0*rz/rho0,1)}.'), 3, T_AER, ('vận tốc bay bằng theo độ cao', 'level-flight speed versus altitude'), 'script (verify_m01: g_vreq)')
    # G19 two engines, same thrust, different ue: propulsive efficiency comparison
    for _ in range(2):
        u = rng.choice([200., 250.]); T = rng.choice([10e3, 20e3]); ueA = u*rng.choice([1.25, 1.5]); ueB = u*rng.choice([2.5, 3.0])
        mA = T/(ueA-u); mB = T/(ueB-u); eA = eta_p_simple(u, ueA); eB = eta_p_simple(u, ueB)
        reg('g_cmp', dict(u=u, ueA=ueA, ueB=ueB), eA/eB)
        mkq(B(f'Hai động cơ cùng lực đẩy {N(T/1e3,0)} kN ở u = {N(u,0)} m/s (bỏ qua f, vòi giãn nở hoàn toàn): A có ue = {N(ueA,0)} m/s (lưu lượng lớn, như turbofan), B có ue = {N(ueB,0)} m/s (lưu lượng nhỏ, như turbojet). Tỉ số η_p(A)/η_p(B) là:', f'Two engines give the same thrust of {N(T/1e3,0)} kN at u = {N(u,0)} m/s (f neglected, fully expanded nozzle): A has ue = {N(ueA,0)} m/s (large flow, turbofan-like), B has ue = {N(ueB,0)} m/s (small flow, turbojet-like). The ratio η_p(A)/η_p(B) is:'),
            eA/eB, [eB/eA, ueB/ueA, mA/mB], '', 2,
            B(f'Lưu lượng cần: ṁA = T/(ue − u) = {N(mA,1)} kg/s, ṁB = {N(mB,1)} kg/s. η_p(A) = 2u/(u + ueA) = {N(eA,3)}, η_p(B) = {N(eB,3)} ⇒ tỉ số {N(eA/eB,3)}. Động cơ tăng tốc khối lượng khí lớn hơn với gia tốc nhỏ hơn thì hiệu suất đẩy cao hơn: đây là lý do turbofan thay turbojet cho máy bay dân dụng (slide tr.8, 10, 37).',
              f'Required flows: ṁA = T/(ue − u) = {N(mA,1)} kg/s, ṁB = {N(mB,1)} kg/s. η_p(A) = 2u/(u + ueA) = {N(eA,3)}, η_p(B) = {N(eB,3)} ⇒ ratio {N(eA/eB,3)}. The engine that accelerates a larger air mass by a smaller amount has the higher propulsive efficiency: this is why turbofans replaced turbojets in airliners (slides pp.8, 10, 37).'), 3, T_PRI, ('so sánh hiệu suất đẩy', 'propulsive efficiency comparison'), 'script (verify_m01: g_cmp)')
    return Q

def main():
    orig_ess = O.orig(); closed = O.closed_orig(); conc = concept(); gen = generated()
    items = closed + orig_ess + conc
    dump(os.path.join(ROOT, 'data', 'qsrc', 'm01.json'), items)
    dump(os.path.join(ROOT, 'data', 'qsrc', 'm01_gen.json'), gen)
    dump(os.path.join(ROOT, 'data', 'verify', 'm01_values.json'), REG)
    allc = [i for i in items + gen if i['kind'] != 'ess']
    print('originals closed', sum(1 for i in closed), '| orig ess', len(orig_ess), '| concept', len(conc), '| generated', len(gen))
    print('closed total', len(allc), '| level3', sum(1 for i in allc if i['level'] == 3), '| goc closed', sum(1 for i in allc if i['origin'] == 'goc'), '| REG', len(REG))

if __name__ == '__main__':
    main()
