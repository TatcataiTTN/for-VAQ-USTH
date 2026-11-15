"""m05 conceptual items derived from the lecturer's slides (Ch.5 tr.3-59).  They are NOT questions of the lecturer: origin 'bo_sung', src names the slide
("Slide Ch.5 tr.N: ...").  Numbers inside come from m05_common (route A) and are registered for verify_m05.py."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from m05_common import *
ITEMS = []
def add(it): ITEMS.append(it); return it
def C(qv, qe, opts, ci, ev, ee, level, topic, pg, what, check):
    """text MCQ: opts = [(vi, en), ...]; src names the slide."""
    return add(mcq(B(qv, qe), [B(a, b) for a, b in opts], ci, B(ev, ee), level, topic, SL(pg, what), 'bo_sung', check))
def TF(qv, qe, truth, ev, ee, level, topic, pg, what, check):
    return add(tf(B(qv, qe), truth, B(ev, ee), level, topic, SL(pg, what), 'bo_sung', check))

def build():
    k = 1.4
    # ---------------------------------------------------------------- stagnation (tr.3-9)
    C('Dòng khí ổn định, đoạn nhiệt chảy qua vòi phun hoặc diffuser, không có công trục và bỏ qua thay đổi thế năng. Đại lượng nào KHÔNG đổi dọc ống?',
      'A steady, adiabatic gas flow passes through a nozzle or diffuser with no shaft work and negligible potential-energy change. Which quantity does NOT change along the duct?',
      [('entanpi hãm h₀ = h + V²/2', 'the stagnation enthalpy h₀ = h + V²/2'), ('entanpi tĩnh h', 'the static enthalpy h'), ('nhiệt độ tĩnh T', 'the static temperature T'), ('vận tốc V', 'the velocity V')], 0,
      'Cân bằng năng lượng h₁ + V₁²/2 = h₂ + V₂²/2 cho h₀₁ = h₀₂ (slide tr.5). h, T và V đều đổi: V tăng thì h và T giảm trong vòi phun và ngược lại trong diffuser.',
      'The energy balance h₁ + V₁²/2 = h₂ + V₂²/2 gives h₀₁ = h₀₂ (slide p.5). h, T and V all change: when V rises h and T fall in a nozzle and the reverse in a diffuser.',
      1, TOP['stag'], 5, ('h₀ không đổi', 'h₀ constant'), 'slide p.5')
    C('Với khí lý tưởng c_p không đổi, "nhiệt độ động" (dynamic temperature) V²/(2c_p) là',
      'For an ideal gas with constant c_p, the "dynamic temperature" V²/(2c_p) is',
      [('độ tăng nhiệt độ khi khí bị hãm đoạn nhiệt từ vận tốc V về 0', 'the temperature rise when the gas is brought to rest adiabatically from speed V'), ('nhiệt độ tĩnh của khí đang chuyển động với vận tốc V', 'the static temperature of the gas moving at speed V'), ('độ giảm nhiệt độ khi khí giãn nở tới vận tốc V', 'the temperature drop when the gas expands to speed V from rest'), ('hiệu giữa nhiệt độ hãm và nhiệt độ tới hạn T*', 'the difference between the stagnation and the critical temperature T*')], 0,
      'T₀ = T + V²/(2c_p) nên V²/(2c_p) = T₀ − T, độ tăng nhiệt độ khi hãm (slide tr.7: 100 m/s cho 5 K). Nó không phải nhiệt độ tĩnh và không liên quan trực tiếp tới T*.',
      'T₀ = T + V²/(2c_p), so V²/(2c_p) = T₀ − T, the temperature rise on stagnation (slide p.7: 100 m/s gives 5 K). It is not the static temperature and is not directly related to T*.',
      1, TOP['stag'], 7, ('nhiệt độ động', 'dynamic temperature'), 'slide p.7')
    TF('Đầu dò nhiệt độ đứng yên đặt trong dòng khí đang chảy (không có bức xạ hay dẫn nhiệt) cho số chỉ bằng nhiệt độ tĩnh của khí.',
       'A stationary temperature probe in a flowing gas (no radiation or conduction losses) reads the static temperature of the gas.',
       False, 'Sai. Khí bị hãm tại đầu dò nên nhiệt kế chỉ nhiệt độ hãm T₀ = T + V²/(2c_p), cao hơn T (slide tr.7, 14). Với 100 m/s ở 300 K chênh gần 5 K; với 1000 m/s chênh gần 500 K.',
       'False. The gas is brought to rest at the probe, so it reads the stagnation temperature T₀ = T + V²/(2c_p), above T (slide p.7, 14). At 100 m/s and 300 K the difference is nearly 5 K; at 1000 m/s nearly 500 K.',
       1, TOP['stag'], 14, ('đầu dò đứng yên', 'stationary probe'), 'slide p.7, 14 + script')
    C('Trong quá trình hãm (stagnation), động năng của dòng khí chuyển thành',
      'During a stagnation process the kinetic energy of the flow is converted into',
      [('entanpi (nội năng cộng công dòng), làm T và P tăng', 'enthalpy (internal energy plus flow energy), so T and P rise'), ('chỉ nội năng, T tăng còn P không đổi', 'internal energy only, so T rises while P stays constant'), ('thế năng, T và P đều không đổi', 'potential energy, with T and P unchanged'), ('entropi, nên T giảm', 'entropy, so T falls')], 0,
      'Slide tr.6: động năng chuyển thành entanpi (nội năng + công dòng) nên cả nhiệt độ và áp suất tăng (ví dụ tr.12: +31,1 °C và +26,72 kPa khi hãm từ 250 m/s).',
      'Slide p.6: kinetic energy is converted to enthalpy (internal energy + flow energy), so both temperature and pressure rise (example p.12: +31.1 °C and +26.72 kPa on stopping from 250 m/s).',
      1, TOP['stag'], 6, ('động năng → entanpi', 'kinetic energy → enthalpy'), 'slide p.6, 12')
    C('Áp suất hãm P₀ theo định nghĩa của slide tr.8 là áp suất khí đạt được khi',
      'The stagnation pressure P₀ in the sense of slide p.8 is the pressure the gas reaches when',
      [('bị hãm về 0 một cách đẳng entropi', 'it is brought to rest isentropically'), ('bị hãm về 0 qua một sóng xung kích', 'it is brought to rest through a shock wave'), ('giãn nở đẳng nhiệt tới áp suất khí quyển', 'it expands isothermally to atmospheric pressure'), ('chảy qua cổ họng với Ma = 1', 'it flows through a throat at Ma = 1')], 0,
      'P₀ là áp suất của quá trình hãm ĐẲNG ENTROPI (tr.8), liên hệ với P qua (T₀/T)^(k/(k−1)). Hãm không thuận nghịch (ví dụ qua sóng xung kích) cho áp suất thấp hơn; điều đó không nằm trong slide.',
      'P₀ is the pressure of an ISENTROPIC stop (p.8), related to P through (T₀/T)^(k/(k−1)). An irreversible stop (for example through a shock) gives a lower pressure; that is not on the slides.',
      1, TOP['stag'], 8, ('P₀ đẳng entropi', 'isentropic P₀'), 'slide p.8')
    # ---------------------------------------------------------------- Hugoniot (tr.25-31)
    C('Theo hệ thức Hugoniot dA/A = −(dV/V)(1 − Ma²), dòng cận âm (Ma < 1) muốn tăng tốc thì diện tích ống phải',
      'By the Hugoniot relation dA/A = −(dV/V)(1 − Ma²), a subsonic flow (Ma < 1) can accelerate only if the duct area',
      [('giảm theo chiều dòng (ống hội tụ)', 'decreases in the flow direction (converging duct)'), ('tăng theo chiều dòng (ống phân kỳ)', 'increases in the flow direction (diverging duct)'), ('không đổi', 'stays constant'), ('đổi tùy theo khí', 'changes in a way that depends on the gas')], 0,
      'Với Ma < 1 thì 1 − Ma² > 0 nên dA và dV ngược dấu: dV > 0 đòi hỏi dA < 0 (slide tr.30). Vòi phun cận âm là ống thu hẹp, diffuser cận âm là ống mở rộng (tr.31).',
      'For Ma < 1, 1 − Ma² > 0 so dA and dV have opposite signs: dV > 0 requires dA < 0 (slide p.30). A subsonic nozzle converges, a subsonic diffuser diverges (p.31).',
      1, TOP['hug'], 30, ('Hugoniot cận âm', 'subsonic Hugoniot'), 'slide p.30-31')
    C('Dòng siêu âm (Ma > 1) đi qua ống phân kỳ (diện tích tăng theo chiều dòng). Các tính chất thay đổi thế nào?',
      'A supersonic flow (Ma > 1) goes through a diverging duct (area increasing in the flow direction). How do the properties change?',
      [('V và Ma tăng; P, T, ρ giảm', 'V and Ma rise; P, T and ρ fall'), ('V và Ma giảm; P, T, ρ tăng', 'V and Ma fall; P, T and ρ rise'), ('V tăng nhưng P tăng', 'V rises but P rises too'), ('V giảm nhưng T giảm', 'V falls but T falls')], 0,
      'Với Ma > 1 thì dA và dV cùng dấu: ống phân kỳ làm V tăng, nên P, T, ρ giảm; đó là vòi phun siêu âm (slide tr.31b). Đường nén và diffuser siêu âm là ống hội tụ.',
      'For Ma > 1 dA and dV have the same sign: a diverging duct raises V, so P, T and ρ fall; this is the supersonic nozzle (slide p.31b). The supersonic diffuser is a converging duct.',
      2, TOP['hug'], 31, ('vòi phun siêu âm', 'supersonic nozzle'), 'slide p.31')
    C('Để làm một dòng khí tăng tốc từ vận tốc cận âm lên siêu âm, hình dạng ống phải là',
      'To accelerate a gas from subsonic to supersonic velocity the duct must be',
      [('hội tụ rồi phân kỳ, với Ma = 1 tại cổ họng', 'converging then diverging, with Ma = 1 at the throat'), ('chỉ hội tụ, Ma = 1 ở cửa ra rồi tiếp tục tăng', 'converging only, with Ma = 1 at the exit and rising beyond it'), ('chỉ phân kỳ từ đầu', 'diverging from the start'), ('hình trụ, tăng nhiệt độ hãm', 'cylindrical, with a rising stagnation temperature')], 0,
      'Phần hội tụ tăng tốc dòng cận âm tới Ma = 1 ở tiết diện nhỏ nhất (dA/dV = 0); phần phân kỳ tiếp tục tăng tốc dòng siêu âm (slide tr.24, 30). Ống chỉ hội tụ không vượt được Ma = 1 (cửa ra bị nghẹt).',
      'The converging part accelerates the subsonic flow to Ma = 1 at the smallest area (dA/dV = 0); the diverging part keeps accelerating the supersonic flow (slide p.24, 30). A converging-only duct cannot exceed Ma = 1 (the exit chokes).',
      2, TOP['hug'], 24, ('ống thu–giãn', 'converging–diverging duct'), 'slide p.24, 30')
    TF('Trong ống thu–giãn của ví dụ CO₂ (slide tr.18–24), vận tốc vẫn tiếp tục tăng sau cổ họng dù diện tích dòng chảy tăng nhanh.',
       'In the converging–diverging CO₂ duct of the slide example (p.18–24), the velocity keeps increasing after the throat although the flow area increases rapidly.',
       True, 'Đúng. Sau cổ họng dòng là siêu âm (Ma > 1) nên diện tích tăng đi kèm vận tốc tăng; bảng tr.22 cho V = 317,2 → 371,4 → 441,9 → 530,9 m/s trong khi A tăng 9,63 → 16,3 cm².',
       'True. After the throat the flow is supersonic (Ma > 1), so a growing area goes together with a growing velocity; the table on p.22 shows V = 317.2 → 371.4 → 441.9 → 530.9 m/s while A grows 9.63 → 16.3 cm².',
       2, TOP['cd'], 24, ('V tăng sau cổ họng', 'V rises after the throat'), 'slide p.22, 24')
    C('Dòng siêu âm đi vào ống HỘI TỤ (diffuser siêu âm). Điều gì xảy ra theo chiều dòng?',
      'A supersonic flow enters a CONVERGING duct (a supersonic diffuser). What happens along the flow direction?',
      [('V và Ma giảm; P, T, ρ tăng', 'V and Ma fall; P, T and ρ rise'), ('V và Ma tăng; P, T, ρ giảm', 'V and Ma rise; P, T and ρ fall'), ('V giảm còn P giảm', 'V falls and P falls'), ('mọi tính chất không đổi', 'all properties stay constant')], 0,
      'Ma > 1: dA < 0 kéo theo dV < 0 (tr.30), nên dòng chậm lại và nén: P, T, ρ tăng (hình tr.31b, diffuser siêu âm).',
      'Ma > 1: dA < 0 implies dV < 0 (p.30), so the flow slows and is compressed: P, T and ρ rise (figure p.31b, supersonic diffuser).',
      2, TOP['hug'], 31, ('diffuser siêu âm', 'supersonic diffuser'), 'slide p.31')
    # ---------------------------------------------------------------- critical, area ratio (tr.32-38, 49)
    pc14, pc133 = crit(1.4)['PP'], crit(1.33)['PP']
    C(f'Tỉ số áp suất tới hạn P*/P₀ = (2/(k+1))^(k/(k−1)) của khí có k = 1,33 (sản phẩm cháy) so với không khí (k = 1,4) là',
      f'The critical pressure ratio P*/P₀ = (2/(k+1))^(k/(k−1)) of a gas with k = 1.33 (combustion products) compared with air (k = 1.4) is',
      [(f'lớn hơn một chút: {N(pc133,4)} so với {N(pc14,4)}'.replace('.', ','), f'slightly larger: {N(pc133,4)} against {N(pc14,4)}'), (f'nhỏ hơn một chút: {N(0.5,4)} so với {N(pc14,4)}'.replace('.', ','), f'slightly smaller: {N(0.5,4)} against {N(pc14,4)}'), (f'bằng nhau: {N(pc14,4)}'.replace('.', ','), f'equal: {N(pc14,4)}'), (f'phụ thuộc cả P₀ lẫn T₀ nên không so được', 'depends on P₀ and T₀ so no comparison is possible')], 0,
      f'(2/2,33)^(1,33/0,33) = {N(pc133,4)} > (2/2,4)^3,5 = {N(pc14,4)}: k nhỏ hơn cho tỉ số tới hạn lớn hơn. Tỉ số tới hạn chỉ phụ thuộc k (slide tr.35, phương trình (13)), không phụ thuộc P₀, T₀.',
      f'(2/2.33)^(1.33/0.33) = {N(pc133,4)} > (2/2.4)^3.5 = {N(pc14,4)}: a smaller k gives a larger critical ratio. The critical ratio depends only on k (slide p.35, equation (13)), not on P₀ or T₀.',
      3, TOP['crit'], 35, ('P*/P₀ theo k', 'P*/P₀ against k'), 'slide p.35 + script')
    TF('Với mỗi giá trị A/A* > 1 chỉ có một số Mach thỏa mãn phương trình (17).',
       'For each value A/A* > 1 only one Mach number satisfies equation (17).',
       False, 'Sai. Có một A/A* cho mỗi Ma nhưng có HAI Ma cho mỗi A/A* > 1: một cận âm, một siêu âm (slide tr.49). Ví dụ A/A* = 1,6875 cho Ma ≈ 0,38 và Ma = 2. Phải chọn nhánh theo dòng cận âm hay siêu âm (tr.58).',
       'False. There is one A/A* for each Ma but TWO Ma for each A/A* > 1: one subsonic, one supersonic (slide p.49). For example A/A* = 1.6875 gives Ma ≈ 0.38 and Ma = 2. The branch must be chosen by whether the flow is subsonic or supersonic (p.58).',
       2, TOP['area'], 49, ('hai nghiệm Ma', 'two Mach roots'), 'slide p.49 + script')
    C('Trong ví dụ N₂ (slide tr.56–59) diện tích ống thu hẹp 20 %, dòng vào cận âm Ma₁ = 0,3. Vì sao chọn Ma₂ cận âm chứ không phải nghiệm siêu âm của A₂/A* = 1,6281?',
      'In the N₂ example (slide p.56–59) the duct converges by 20 % and the inlet flow is subsonic, Ma₁ = 0.3. Why is the subsonic Ma₂ chosen instead of the supersonic root of A₂/A* = 1.6281?',
      [('ống hội tụ và dòng đầu cận âm nên dòng chỉ tăng tốc tới Ma < 1 (chưa tới cổ họng)', 'the duct converges and the flow starts subsonic, so it only accelerates to Ma < 1 (the throat is not reached)'), ('nghiệm siêu âm không tồn tại với k = 1,4', 'the supersonic root does not exist for k = 1.4'), ('vì bảng A-32 chỉ liệt kê nhánh cận âm', 'because Table A-32 lists only the subsonic branch'), ('vì nitơ không thể đạt Ma > 1', 'because nitrogen cannot exceed Ma = 1')], 0,
      'Slide tr.58: ống thu hẹp theo chiều dòng và dòng đầu cận âm nên Ma₂ cận âm (0,3887). Nghiệm siêu âm Ma ≈ 1,9 tồn tại về mặt toán nhưng sẽ đòi dòng đi qua Ma = 1 trước, tức là cần một cổ họng.',
      'Slide p.58: the duct converges in the flow direction and the flow starts subsonic, so Ma₂ is subsonic (0.3887). A supersonic root Ma ≈ 1.9 exists mathematically but would require the flow to pass through Ma = 1 first, i.e. a throat.',
      2, TOP['area'], 58, ('chọn nhánh cận âm', 'choosing the subsonic branch'), 'slide p.58 + script')
    # ---------------------------------------------------------------- back pressure and choking (tr.39-48)
    C('Vòi phun hội tụ có điều kiện vào cố định. Giảm áp suất ngược P_b từ P₀ xuống đúng P* thì lưu lượng khối',
      'A converging nozzle has fixed inlet conditions. Lowering the back pressure P_b from P₀ down to exactly P*, the mass flow rate',
      [('tăng từ 0 tới giá trị cực đại ṁ_max', 'rises from 0 to the maximum value ṁ_max'), ('giảm từ cực đại xuống 0', 'falls from the maximum to 0'), ('giữ nguyên bằng ṁ_max suốt quá trình', 'stays at ṁ_max throughout'), ('tăng rồi giảm, cực đại ở P_b = P₀/2', 'rises then falls, with a maximum at P_b = P₀/2')], 0,
      'Slide tr.42–43, 47: P_b = P₀ thì ṁ = 0; giảm P_b làm ṁ tăng và đạt cực đại tại P_b = P* (dòng nghẹt).',
      'Slide p.42–43, 47: P_b = P₀ gives ṁ = 0; lowering P_b raises ṁ and it reaches its maximum at P_b = P* (choked flow).',
      1, TOP['back'], 47, ('ṁ theo P_b/P₀', 'ṁ against P_b/P₀'), 'slide p.43, 47')
    C('Vòi phun hội tụ đang nghẹt (P_b < P*). Giảm tiếp áp suất ngược thì',
      'A converging nozzle is choked (P_b < P*). Lowering the back pressure further,',
      [('lưu lượng khối và phân bố áp suất trong vòi không đổi; P_e vẫn bằng P*', 'the mass flow and the pressure distribution in the nozzle do not change; P_e stays equal to P*'), ('lưu lượng khối tăng tiếp vì chênh áp tăng', 'the mass flow keeps increasing because the pressure difference grows'), ('P_e giảm theo P_b', 'P_e falls with P_b'), ('dòng quay về cận âm và lưu lượng giảm', 'the flow returns to subsonic and the flow rate falls')], 0,
      'Slide tr.43, 47: giảm P_b dưới P* không làm đổi gì dọc vòi; P_e = P* với mọi P_b < P*. Giãn nở tiếp xảy ra ngoài vòi phun. Tin tức không truyền ngược lên thượng nguồn vì Ma = 1 ở cửa ra.',
      'Slide p.43, 47: lowering P_b below P* changes nothing along the nozzle; P_e = P* for every P_b < P*. The rest of the expansion happens outside the nozzle. Information cannot travel upstream because Ma = 1 at the exit.',
      2, TOP['back'], 43, ('dòng nghẹt', 'choked flow'), 'slide p.43, 47')
    TF('Với vòi phun hội tụ, áp suất ở mặt cắt cửa ra P_e bằng áp suất ngược P_b với mọi giá trị P_b.',
       'For a converging nozzle the exit-plane pressure P_e equals the back pressure P_b for every value of P_b.',
       False, 'Sai. P_e = P_b chỉ khi P_b ≥ P*; khi P_b < P* thì P_e = P* (slide tr.47, hàm hai nhánh). Ví dụ slide tr.54: P_b = 0,4 MPa < P* = 0,552 MPa nên P_e = 0,552 MPa.',
       'False. P_e = P_b only when P_b ≥ P*; when P_b < P* then P_e = P* (slide p.47, a two-branch function). Slide example p.54: P_b = 0.4 MPa < P* = 0.552 MPa so P_e = 0.552 MPa.',
       2, TOP['back'], 47, ('P_e theo P_b', 'P_e against P_b'), 'slide p.47, 54')
    C('Với vòi phun hội tụ có cùng P_b < P* và cùng A*, tăng áp suất hãm P₀ (giữ T₀) hoặc giảm T₀ (giữ P₀) thì lưu lượng khối ṁ_max',
      'For a converging nozzle with the same P_b < P* and the same A*, raising the stagnation pressure P₀ (T₀ fixed) or lowering T₀ (P₀ fixed) makes the maximum mass flow ṁ_max',
      [('tăng, vì ṁ_max ∝ P₀/√T₀', 'increase, because ṁ_max ∝ P₀/√T₀'), ('giảm, vì ṁ_max ∝ √T₀/P₀', 'decrease, because ṁ_max ∝ √T₀/P₀'), ('không đổi, vì dòng nghẹt', 'stay the same, because the flow is choked'), ('tăng khi P₀ tăng nhưng không đổi theo T₀', 'increase with P₀ but not depend on T₀')], 0,
      'Phương trình (16): ṁ_max = A*P₀√(k/(RT₀))·hằng số. Nghẹt không có nghĩa lưu lượng cố định: nó cố định theo A*, P₀, T₀ (slide tr.46, 48).',
      'Equation (16): ṁ_max = A*P₀√(k/(RT₀))·constant. Choked does not mean the flow is fixed: it is fixed by A*, P₀ and T₀ (slide p.46, 48).',
      2, TOP['mdot'], 48, ('ṁ_max ∝ P₀/√T₀', 'ṁ_max ∝ P₀/√T₀'), 'slide p.46, 48')
    C('Một vòi phun nghẹt. Nếu P₀ tăng gấp đôi và T₀ tăng gấp bốn (A* và khí không đổi) thì lưu lượng khối cực đại ṁ_max',
      'A nozzle is choked. If P₀ doubles and T₀ quadruples (A* and the gas unchanged) the maximum mass flow ṁ_max',
      [('không đổi (2/√4 = 1)', 'is unchanged (2/√4 = 1)'), ('tăng gấp đôi', 'doubles'), ('giảm một nửa', 'is halved'), ('tăng gấp 4', 'increases four-fold')], 0,
      'ṁ_max ∝ P₀/√T₀ (phương trình (16)): hệ số = 2/√4 = 1. Hai thay đổi bù trừ nhau. Nếu nhầm ṁ ∝ P₀/T₀ sẽ cho 1/2; nếu nhầm ṁ ∝ P₀ sẽ cho 2.',
      'ṁ_max ∝ P₀/√T₀ (equation (16)): factor = 2/√4 = 1. The two changes cancel. Taking ṁ ∝ P₀/T₀ by mistake would give 1/2; taking ṁ ∝ P₀ would give 2.',
      3, TOP['mdot'], 46, ('ṁ_max ∝ P₀/√T₀', 'ṁ_max ∝ P₀/√T₀'), 'slide p.46 + script')
    C('Lưu lượng khối qua mặt cắt có diện tích A và số Mach Ma của một dòng khí đạt cực đại khi',
      'The mass flow through a section of area A and Mach number Ma of a gas flow is a maximum when',
      [('Ma = 1 tại mặt cắt nhỏ nhất (cổ họng)', 'Ma = 1 at the smallest section (the throat)'), ('Ma = 0, tức khí đứng yên', 'Ma = 0, i.e. the gas is at rest'), ('Ma → ∞', 'Ma → ∞'), ('Ma = 0,5 ở mọi mặt cắt', 'Ma = 0.5 at every section')], 0,
      'Đạo hàm ṁ trong (15) theo Ma bằng 0 cho Ma = 1 (slide tr.45). Ma = 0 và Ma → ∞ đều cho ṁ = 0. Ma = 1 chỉ có thể xảy ra ở mặt cắt nhỏ nhất.',
      'Setting the derivative of ṁ in (15) with respect to Ma to zero gives Ma = 1 (slide p.45). Both Ma = 0 and Ma → ∞ give ṁ = 0. Ma = 1 can occur only at the smallest section.',
      2, TOP['mdot'], 45, ('cực đại tại Ma = 1', 'maximum at Ma = 1'), 'slide p.45')
    # ---------------------------------------------------------------- unit traps (tr.20, 55)
    C('Slide tr.55 viết ṁ = A*P₀√(k/(RT₀))(2/(k+1))^… với P₀ = 1045 kPa và R = 0,287 kJ/(kg·K), kết quả in 7,10 kg/s. Phép tính nguyên văn bằng các số đó (không đổi đơn vị) cho 0,2246 kg/s vì thiếu',
      'Slide p.55 writes ṁ = A*P₀√(k/(RT₀))(2/(k+1))^… with P₀ = 1045 kPa and R = 0.287 kJ/(kg·K) and prints 7.10 kg/s. The literal calculation with those numbers (no unit conversion) gives 0.2246 kg/s because it misses',
      [('hệ số √1000 do đổi P₀ sang Pa và R sang J/(kg·K)', 'the factor √1000 from converting P₀ to Pa and R to J/(kg·K)'), ('hệ số 1000 vì 1 MPa = 1000 kPa', 'a factor 1000 because 1 MPa = 1000 kPa'), ('hệ số 1,4 của tỉ số nhiệt dung', 'the factor 1.4 of the specific-heat ratio'), ('hệ số 10⁴ đổi cm² sang m²', 'the factor 10⁴ converting cm² to m²')], 0,
      'Dùng P₀ theo kPa (thay vì Pa) làm tích nhỏ đi 1000 lần; dùng R theo kJ/(kg·K) (thay vì J/(kg·K)) làm căn √(k/(RT₀)) lớn lên √1000 lần. Kết quả nguyên văn = đúng × √1000/1000 = đúng/√1000, tức 7,10/31,62 = 0,2246. Đây là lỗi slide (ghi trong mục lỗi nguồn); đáp số 7,10 đúng khi tính theo SI.',
      'Using P₀ in kPa (instead of Pa) makes the product 1000 times smaller; using R in kJ/(kg·K) (instead of J/(kg·K)) makes the root √(k/(RT₀)) √1000 times larger. The literal result = true × √1000/1000 = true/√1000, i.e. 7.10/31.62 = 0.2246. This is a slide error (listed in the source-errors section); 7.10 is right in SI units.',
      3, TOP['unit'], 55, ('thiếu √1000', 'missing √1000'), 'slide p.55 + script')
    TF('Ở slide tr.20, hệ số đổi đơn vị in là 1000 m²/s³ trên kJ/kg; đúng phải là 1000 m²/s² trên kJ/kg.',
       'On slide p.20 the printed conversion factor is 1000 m²/s³ per kJ/kg; the correct one is 1000 m²/s² per kJ/kg.',
       True, 'Đúng. 1 kJ/kg = 1000 J/kg = 1000 m²/s²: đơn vị m²/s² (không phải m²/s³). Kết quả V = 164,5 m/s trên slide vẫn đúng; lỗi chỉ nằm ở đơn vị in.',
       'True. 1 kJ/kg = 1000 J/kg = 1000 m²/s²: the unit is m²/s² (not m²/s³). The result V = 164.5 m/s on the slide is still right; only the printed unit is wrong.',
       1, TOP['unit'], 20, ('m²/s² không phải m²/s³', 'm²/s², not m²/s³'), 'slide p.20 + dimensional analysis')
    TF('Slide tr.58–59 có hai số khác với tính chính xác (Ma₂ = 0,391 và P₂ = 95,7 kPa) vì slide nội suy tuyến tính từ bảng A-32 thưa, không vì sai công thức.',
       'Slide p.58–59 has two numbers that differ from the exact calculation (Ma₂ = 0.391 and P₂ = 95.7 kPa) because the slide interpolates linearly in the coarse Table A-32, not because the formula is wrong.',
       True, 'Đúng. A₂/A* = 1,6281 nằm giữa hai hàng Ma = 0,3 và 0,4; nội suy cho 0,3915 trong khi (17) cho 0,3887 (P₂ = 95,91 kPa chính xác, T₂ = 395 K trùng).',
       'True. A₂/A* = 1.6281 lies between the rows Ma = 0.3 and 0.4; interpolation gives 0.3915 while (17) gives 0.3887 (exact P₂ = 95.91 kPa, T₂ = 395 K agrees).',
       2, TOP['area'], 58, ('Ma₂ nội suy thô', 'coarse interpolation of Ma₂'), 'slide p.58-59 + script')
    # A-32 interpolation warning (numbers from the closed forms)
    Mi = 3.5; lin = 4.2346 + (Mi - 3.0) / 2.0 * (25.0 - 4.2346); ex = AAs(Mi, 1.4)
    C(f'Table A-32 chỉ có các hàng Ma = 3,0 (A/A* = 4,2346) và Ma = 5,0 (A/A* = 25,000). Nội suy tuyến tính giữa hai hàng này cho A/A* tại Ma = 3,5 là {N(lin,2)}; giá trị đúng theo phương trình (17) là',
      f'Table A-32 has only the rows Ma = 3.0 (A/A* = 4.2346) and Ma = 5.0 (A/A* = 25.000). Linear interpolation between them gives A/A* at Ma = 3.5 as {N(lin,2)}; the exact value from equation (17) is',
      [(f'{N(ex,2)}: nội suy tuyến tính quá cao (≈ +{N((lin/ex-1)*100,0)} %)'.replace('.', ','), f'{N(ex,2)}: the linear interpolation is far too high (≈ +{N((lin/ex-1)*100,0)} %)'), (f'{N(lin,2)}: nội suy tuyến tính là đủ chính xác', f'{N(lin,2)}: the linear interpolation is accurate enough'), (f'{N(4.2346,2)}: lấy hàng in gần nhất Ma = 3,0', f'{N(4.2346,2)}: take the nearest printed row Ma = 3.0'), (f'{N(25.0,2)}: lấy hàng in Ma = 5,0 phía trên', f'{N(25.0,2)}: take the printed row Ma = 5.0 above')], 0,
      f'A/A* = (1/3,5)[(2/2,4)(1 + 0,2 × 12,25)]³ = {N(ex,3)}. A/A* là hàm cong của Ma nên nội suy tuyến tính trên khoảng thưa Ma 3 → 5 sai +{N((lin/ex-1)*100,0)} %. Dùng công thức đóng (17), chỉ dùng bảng để kiểm tại hàng in (cảnh báo trong thư viện P3).',
      f'A/A* = (1/3.5)[(2/2.4)(1 + 0.2 × 12.25)]³ = {N(ex,3)}. A/A* is a curved function of Ma so linear interpolation over the sparse interval Ma 3 → 5 is off by +{N((lin/ex-1)*100,0)} %. Use the closed form (17) and use the table only to check at the printed rows (warning in the P3 library).',
      3, TOP['area'], 49, ('nội suy A-32 thưa', 'sparse A-32 interpolation'), 'script + equation (17)')
    reg('A32lin', dict(Ma=3.5, k=1.4), 'AA_exact', ex, 1e-9, 'A-32 interpolation warning'); reg('A32lin', dict(Ma=3.5, k=1.4), 'AA_lin', lin, 1e-9, 'A-32 interpolation')
    return ITEMS
