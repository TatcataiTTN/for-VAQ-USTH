"""Generated questions for module 03 (Floyd ch.13). Run: python3 build/gen/gen_m03.py"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'author'))
from _lib import *
G = Gen('m03', 13, 20250303, dict(cmp=('Comparators and hysteresis', 'Mạch so sánh và trễ (hysteresis)'), sum=('Summing, averaging, scaling amplifiers', 'Mạch cộng, trung bình, cộng có trọng số'),
        intg=('Integrator', 'Mạch tích phân'), dif=('Differentiator', 'Mạch vi phân')))
g, fmt, add = G.g, G.fmt, G.add
S = lambda a, b: (a, b)
# 1 trigger points
for r1, r2, vm in [(47, 18, 10), (33, 18, 11), (150, 68, 11), (100, 100, 12), (68, 10, 8), (22, 4.7, 12), (56, 15, 10), (10, 2.2, 13)]:
    ut = r2 / (r1 + r2) * vm
    add('cmp', f'A comparator with positive feedback has R1 = {r1} kΩ, R2 = {r2} kΩ and Vout(max) = ±{vm} V. What is VUTP?', f'Mạch so sánh có hồi tiếp dương với R1 = {r1} kΩ, R2 = {r2} kΩ và Vout(max) = ±{vm} V. VUTP là bao nhiêu?',
        fmt(ut, 'V'), [fmt(r1 / (r1 + r2) * vm, 'V'), fmt(vm, 'V'), fmt(2 * ut, 'V'), fmt(r2 / r1 * vm, 'V')], f'VUTP = R2/(R1+R2)·Vout(max) = {r2}/({r1}+{r2}) × {vm} = {g(ut)} V.', f'VUTP = R2/(R1+R2)·Vout(max) = {r2}/({r1}+{r2}) × {vm} = {g(ut)} V.', S('Floyd Problem 3', 'Floyd Bài 3'), 2)
    add('cmp', f'A comparator with positive feedback has R1 = {r1} kΩ, R2 = {r2} kΩ and Vout(max) = ±{vm} V. What is the hysteresis voltage?', f'Mạch so sánh có hồi tiếp dương với R1 = {r1} kΩ, R2 = {r2} kΩ và Vout(max) = ±{vm} V. Điện áp hysteresis là bao nhiêu?',
        fmt(2 * ut, 'V'), [fmt(ut, 'V'), fmt(2 * r1 / (r1 + r2) * vm, 'V'), fmt(2 * vm, 'V'), fmt(ut / 2, 'V')], f'VHYS = VUTP − VLTP = 2·R2/(R1+R2)·Vout(max) = {g(2*ut)} V.', f'VHYS = VUTP − VLTP = 2·R2/(R1+R2)·Vout(max) = {g(2*ut)} V.', S('Floyd Problem 6', 'Floyd Bài 6'), 2)
# 2 bounded output
for vz in [3.3, 4.7, 5.6, 6.2, 8.2, 9.1]:
    add('cmp', f'A comparator is bounded with two back-to-back {vz} V zener diodes (0.7 V forward drop). What is the output amplitude?', f'Mạch so sánh được giới hạn bằng hai zener {vz} V mắc ngược chiều nhau (sụt áp thuận 0,7 V). Biên độ ngõ ra là bao nhiêu?',
        f'±{g(vz+0.7)} V', [f'±{g(vz)} V', f'±{g(2*vz)} V', f'±{g(vz-0.7)} V', f'±{g(2*vz+1.4)} V'], f'One zener conducts in breakdown and the other forward: |Vout| = VZ + 0.7 = {g(vz+0.7)} V.', f'Một zener dẫn ở vùng đánh thủng và zener kia dẫn thuận: |Vout| = VZ + 0.7 = {g(vz+0.7)} V.', S('Floyd Self-Test Q7', 'Floyd Self-Test câu 7'))
# 3 comparator output level
for vin, ref in [(2.5, 1.5), (-1, 0), (3, 5), (0.4, -0.4), (6, 2), (-3, -1)]:
    out = '+Vout(max)' if vin > ref else '−Vout(max)'
    add('cmp', f'A comparator has Vin = {vin} V on the noninverting input and Vref = {ref} V on the inverting input. The output is', f'Mạch so sánh có Vin = {vin} V ở ngõ vào không đảo và Vref = {ref} V ở ngõ vào đảo. Ngõ ra ở',
        out, ['+Vout(max)' if out[0] == '−' else '−Vout(max)', '0 V', 'Vin − Vref', 'Aol·Vref'], f'(+) input {"above" if vin>ref else "below"} (−) input → the output saturates at {out}.', f'Ngõ (+) {"cao hơn" if vin>ref else "thấp hơn"} ngõ (−) → ngõ ra bão hòa ở {out}.', S('Floyd Problem 2', 'Floyd Bài 2'))
# 4 summing amp (equal Ri)
for rf, ri, vs in [(10, 10, (1, 1.5)), (22, 10, (0.1, 1, 0.5)), (47, 4.7, (0.2, 0.3)), (100, 10, (0.5, 0.25, 0.1)), (15, 5, (1, 2)), (68, 22, (3, 1, 2))]:
    vo = -rf / ri * sum(vs)
    add('sum', f'A summing amplifier has Ri = {ri} kΩ on every input, Rf = {rf} kΩ and inputs {", ".join(str(v) for v in vs)} V. What is VOUT?', f'Mạch cộng có Ri = {ri} kΩ ở mọi ngõ vào, Rf = {rf} kΩ và các ngõ vào {", ".join(str(v).replace(".", ",") for v in vs)} V. VOUT là bao nhiêu?',
        fmt(vo, 'V'), [fmt(-vo, 'V'), fmt(-sum(vs), 'V'), fmt(-ri / rf * sum(vs), 'V'), fmt(-rf / ri * sum(vs) / len(vs), 'V')], f'VOUT = −(Rf/Ri)(V1 + … + Vn) = −({rf}/{ri})({sum(vs):g}) = {g(vo)} V.', f'VOUT = −(Rf/Ri)(V1 + … + Vn) = −({rf}/{ri})({sum(vs):g}) = {g(vo)} V.', S('Floyd Problem 9', 'Floyd Bài 9'), 2)
# 5 averaging amp
for n, ri in [(2, 10), (3, 12), (4, 10), (5, 47), (8, 10), (10, 22)]:
    rf = ri / n
    add('sum', f'To average {n} inputs with an inverting summer using Ri = {ri} kΩ on each input, Rf must be', f'Để lấy trung bình {n} ngõ vào bằng mạch cộng đảo với Ri = {ri} kΩ mỗi ngõ, Rf phải bằng',
        fmt(rf, 'kΩ'), [fmt(ri * n, 'kΩ'), fmt(ri, 'kΩ'), fmt(ri / (n + 1), 'kΩ'), fmt(ri / n / 2, 'kΩ')], f'Gain per input = 1/n → Rf = Ri/n = {ri}/{n} = {g(rf)} kΩ.', f'Độ lợi mỗi ngõ = 1/n → Rf = Ri/n = {ri}/{n} = {g(rf)} kΩ.', S('Floyd Self-Test Q10', 'Floyd Self-Test câu 10'))
# 6 scaling adder input resistor
for rf, w in [(100, 2), (100, 8), (47, 4), (10, 5), (220, 20), (68, 16)]:
    ri = rf / w
    add('sum', f'In a scaling adder with Rf = {rf} kΩ, what input resistor gives an input a weight (gain) of {w}?', f'Trong mạch cộng có trọng số với Rf = {rf} kΩ, điện trở vào nào cho ngõ đó trọng số (độ lợi) {w}?',
        fmt(ri, 'kΩ'), [fmt(rf * w, 'kΩ'), fmt(rf, 'kΩ'), fmt(rf / (w + 1), 'kΩ'), fmt(rf / w / 2, 'kΩ')], f'Weight = Rf/Ri → Ri = {rf}/{w} = {g(ri)} kΩ (bigger weight needs a smaller resistor).', f'Trọng số = Rf/Ri → Ri = {rf}/{w} = {g(ri)} kΩ (trọng số lớn cần điện trở nhỏ).', S('Floyd Problem 14', 'Floyd Bài 14'), 2)
# 7 integrator ramp rate
for vin, r, c in [(5, 56, 0.022), (2, 10, 0.01), (10, 100, 0.1), (1, 22, 0.047), (3, 47, 0.01), (8, 33, 0.068)]:
    s = vin / (r * 1e3 * c * 1e-6) / 1e3
    add('intg', f'An integrator has R = {r} kΩ and C = {c} μF and a {vin} V step input. What is the rate of change of the output?', f'Mạch tích phân có R = {r} kΩ và C = {c} μF với bước nhảy vào {vin} V. Tốc độ biến thiên của ngõ ra là bao nhiêu?',
        fmt(-s, 'V/ms'), [fmt(s, 'V/ms'), fmt(-s * 1000, 'V/ms'), fmt(-s / 1000, 'V/ms'), fmt(-vin * r * c, 'V/ms')], f'ΔVout/Δt = −Vin/(R·C) = −{vin}/({r} kΩ × {c} μF) = {g(-s)} V/ms.', f'ΔVout/Δt = −Vin/(R·C) = −{vin}/({r} kΩ × {c} μF) = {g(-s)} V/ms.', S('Floyd Problem 15', 'Floyd Bài 15'), 2)
# 8 integrator voltage after t
for vin, r, c, t in [(5, 10, 10, 10), (2, 10, 1, 5), (4, 20, 5, 10), (1, 50, 2, 20)]:
    dv = vin * t * 1e-3 / (r * 1e3 * c * 1e-6)
    add('intg', f'An integrator (R = {r} kΩ, C = {c} μF) with output initially 0 V receives {vin} V for {t} ms. What is the output at the end?', f'Mạch tích phân (R = {r} kΩ, C = {c} μF) có ngõ ra ban đầu 0 V nhận {vin} V trong {t} ms. Ngõ ra cuối khoảng này là bao nhiêu?',
        fmt(-dv, 'V'), [fmt(dv, 'V'), fmt(-dv * 10, 'V'), fmt(-dv / 10, 'V'), fmt(-vin * t, 'V')], f'Vout = −Vin·t/(R·C) = −{vin} × {t} ms/({r} kΩ × {c} μF) = {g(-dv)} V.', f'Vout = −Vin·t/(R·C) = −{vin} × {t} ms/({r} kΩ × {c} μF) = {g(-dv)} V.', S('Floyd Problem 19', 'Floyd Bài 19'), 3)
# 9 differentiator amplitude for triangle
for rf, c, vpp, per in [(15, 0.047, 2, 1000), (10, 0.001, 5, 20), (22, 0.01, 4, 200), (47, 0.022, 1, 500), (10, 0.1, 2, 2000)]:
    sl = vpp / (per / 2 * 1e-6); a = rf * 1e3 * c * 1e-6 * sl
    add('dif', f'A triangular wave of {vpp} V peak-to-peak and period {per} μs drives a differentiator with Rf = {rf} kΩ and C = {c} μF. What is the output amplitude (magnitude of each level)?', f'Sóng tam giác {vpp} V đỉnh–đỉnh, chu kỳ {per} μs đưa vào mạch vi phân có Rf = {rf} kΩ và C = {c} μF. Biên độ ngõ ra (độ lớn mỗi mức) là bao nhiêu?',
        fmt(a, 'V'), [fmt(a * 2, 'V'), fmt(a / 2, 'V'), fmt(vpp, 'V'), fmt(a * 10, 'V')], f'|slope| = {vpp} V/({per/2:g} μs) = {g(sl)} V/s; |Vout| = Rf·C·slope = {g(a)} V (square wave).', f'|độ dốc| = {vpp} V/({per/2:g} μs) = {g(sl)} V/s; |Vout| = Rf·C·độ dốc = {g(a)} V (sóng vuông).', S('Floyd Problem 18', 'Floyd Bài 18'), 3)
# conceptual
C = [('cmp', 'The reference voltage of a comparator sets', 'Điện áp tham chiếu của mạch so sánh đặt', ('the trip (threshold) level', 'mức ngưỡng chuyển'), [('the voltage gain', 'độ lợi điện áp'), ('the bandwidth', 'băng thông'), ('the supply voltage', 'điện áp nguồn')], 'The output changes state when Vin crosses Vref.', 'Ngõ ra đổi trạng thái khi Vin cắt Vref.'),
 ('cmp', 'Compared with a plain comparator, a comparator with hysteresis is less sensitive to', 'So với mạch so sánh thường, mạch có hysteresis ít nhạy hơn với', ('noise near the threshold', 'nhiễu gần ngưỡng'), [('the supply voltage', 'điện áp nguồn'), ('the input frequency', 'tần số vào'), ('the load', 'tải')], 'Two trigger points separated by VHYS ignore noise smaller than VHYS.', 'Hai ngưỡng cách nhau VHYS bỏ qua nhiễu nhỏ hơn VHYS.'),
 ('cmp', 'Positive feedback in a comparator makes the transition', 'Hồi tiếp dương trong mạch so sánh làm quá trình chuyển trạng thái', ('faster and regenerative', 'nhanh và tự tái sinh'), [('slower', 'chậm hơn'), ('linear', 'tuyến tính'), ('impossible', 'không thể xảy ra')], 'Once triggered, the feedback pushes the input further past the threshold.', 'Khi đã kích, hồi tiếp đẩy ngõ vào vượt xa ngưỡng hơn.'),
 ('sum', 'The inverting input of a summing amplifier is called the', 'Ngõ vào đảo của mạch cộng được gọi là', ('summing point (virtual ground)', 'điểm cộng (đất ảo)'), [('reference point', 'điểm tham chiếu'), ('output node', 'nút ra'), ('bias node', 'nút phân cực')], 'All input currents add there while the node stays at ≈0 V.', 'Mọi dòng vào cộng tại đó trong khi nút này giữ ≈0 V.'),
 ('sum', 'A scaling adder gives the inputs different', 'Mạch cộng có trọng số cho các ngõ vào khác nhau về', ('weights, by using different input resistors', 'trọng số, bằng các điện trở vào khác nhau'), [('supply voltages', 'điện áp nguồn'), ('feedback capacitors', 'tụ hồi tiếp'), ('phase shifts', 'độ lệch pha')], 'Weight of input n = Rf/Rn.', 'Trọng số ngõ n = Rf/Rn.'),
 ('sum', 'An R/2R ladder is used in a', 'Mạch thang R/2R được dùng trong', ('digital-to-analog converter', 'bộ chuyển đổi số–tương tự'), [('comparator with hysteresis', 'mạch so sánh có hysteresis'), ('differentiator', 'mạch vi phân'), ('voltage follower', 'mạch lặp điện áp')], 'It needs only two resistor values and produces a weighted sum of bits.', 'Chỉ cần hai giá trị điện trở và tạo tổng có trọng số của các bit.'),
 ('intg', 'The output of an ideal integrator for a constant nonzero input is', 'Ngõ ra của mạch tích phân lý tưởng với tín hiệu vào hằng khác không là', ('a linear ramp', 'đường dốc tuyến tính'), [('a constant dc level', 'mức một chiều không đổi'), ('a sine wave', 'sóng sin'), ('a square wave', 'sóng vuông')], 'A constant current charges C at a constant rate.', 'Dòng không đổi nạp C với tốc độ không đổi.'),
 ('intg', 'Applying a square wave to an integrator gives', 'Đưa sóng vuông vào mạch tích phân cho', ('a triangular wave', 'sóng tam giác'), [('a sine wave', 'sóng sin'), ('a dc level', 'mức một chiều'), ('narrow spikes', 'các xung nhọn hẹp')], 'Alternating constant input gives alternating up and down ramps.', 'Vào hằng đổi dấu cho các đường dốc lên xuống luân phiên.'),
 ('intg', 'The resistor in parallel with the feedback capacitor of a practical integrator', 'Điện trở song song với tụ hồi tiếp của mạch tích phân thực tế', ('limits the dc gain and prevents offset-induced saturation', 'giới hạn độ lợi một chiều và ngăn bão hòa do offset'), [('increases the bandwidth', 'làm tăng băng thông'), ('makes the output a square wave', 'làm ngõ ra thành sóng vuông'), ('reduces the supply current', 'giảm dòng nguồn')], 'Without it the dc offset is integrated until the output saturates.', 'Không có nó thì offset một chiều bị tích phân đến khi ngõ ra bão hòa.'),
 ('dif', 'A differentiator tends to be noisy because', 'Mạch vi phân dễ nhiễu vì', ('its gain rises with frequency', 'độ lợi của nó tăng theo tần số'), [('it has no feedback', 'nó không có hồi tiếp'), ('its gain falls with frequency', 'độ lợi của nó giảm theo tần số'), ('it uses a zener diode', 'nó dùng điốt zener')], 'XC falls at high frequency, so Rf/XC grows and amplifies noise.', 'XC giảm ở tần số cao nên Rf/XC tăng và khuếch đại nhiễu.'),
 ('dif', 'A differentiator with a step input produces', 'Mạch vi phân với tín hiệu vào là bước nhảy cho ra', ('a spike at the transitions', 'xung nhọn tại các thời điểm chuyển'), [('a ramp', 'đường dốc'), ('a triangular wave', 'sóng tam giác'), ('a dc level equal to the step', 'mức một chiều bằng bước nhảy')], 'The derivative of a step is nonzero only at the edge.', 'Đạo hàm của bước nhảy chỉ khác không tại cạnh.'),
 ('dif', 'Applying a ramp to a differentiator gives', 'Đưa đường dốc vào mạch vi phân cho', ('a constant (dc) output', 'ngõ ra hằng (một chiều)'), [('a ramp', 'đường dốc'), ('a sine wave', 'sóng sin'), ('zero output', 'ngõ ra bằng không')], 'The slope of a ramp is constant, so the derivative is a dc level.', 'Độ dốc của đường dốc không đổi nên đạo hàm là mức một chiều.')]
for tp, qe, qv, ca, ws, xe, xv in C: G.concept(tp, qe, qv, ca, ws, xe, xv)
# magnitude-worded circuit-action variants (replace the sign-ambiguous book items)
F = 'assets/figs/m03/'
G.ca('sum', 'If the top 10 kΩ input resistor opens in Figure 13–22, the magnitude of the output voltage |VOUT| will', 'Nếu điện trở vào 10 kΩ trên cùng bị hở trong Hình 13–22 thì độ lớn điện áp ra |VOUT| sẽ', F + 'fig13_22.png', 1, '|VOUT| = 3 + 1 + 8 = 12 V before; without the +3 V input: 1 + 8 = 9 V.', '|VOUT| = 3 + 1 + 8 = 12 V trước đó; bỏ ngõ +3 V: 1 + 8 = 9 V.', ('Floyd CA Q4', 'Floyd CA câu 4'))
G.ca('sum', 'If VIN2 is changed to −1 V in Figure 13–22, the magnitude |VOUT| will', 'Nếu đổi VIN2 thành −1 V trong Hình 13–22 thì độ lớn |VOUT| sẽ', F + 'fig13_22.png', 1, '|VOUT| = |3 − 1 + 8| = 10 V instead of 12 V.', '|VOUT| = |3 − 1 + 8| = 10 V thay vì 12 V.', ('Floyd CA Q5', 'Floyd CA câu 5'))
G.ca('sum', 'If VIN3 is changed to −7 V in Figure 13–24, the magnitude |VOUT| will', 'Nếu đổi VIN3 thành −7 V trong Hình 13–24 thì độ lớn |VOUT| sẽ', F + 'fig13_24.png', 1, '|VOUT| = (25/100)|1 + 2 − 7 + 4| = 0 V instead of 2.5 V.', '|VOUT| = (25/100)|1 + 2 − 7 + 4| = 0 V thay vì 2,5 V.', ('Floyd CA Q7', 'Floyd CA câu 7'))
G.ca('sum', 'If Rf opens in Figure 13–25, the magnitude |VOUT| will', 'Nếu Rf bị hở trong Hình 13–25 thì độ lớn |VOUT| sẽ', F + 'fig13_25.png', 0, 'Before: |VOUT| ≈ 8.8 V. With no feedback the op-amp is open loop and the output saturates at its limit (larger).', 'Trước đó: |VOUT| ≈ 8,8 V. Không có hồi tiếp thì op-amp vòng hở và ngõ ra bão hòa ở mức giới hạn (lớn hơn).', ('Floyd CA Q8', 'Floyd CA câu 8'))
G.ca('sum', 'If R2 in Figure 13–23 is changed from 1.0 kΩ to 2.0 kΩ, the magnitude |VOUT| will', 'Nếu đổi R2 trong Hình 13–23 từ 1,0 kΩ lên 2,0 kΩ thì độ lớn |VOUT| sẽ', F + 'fig13_23.png', 1, 'The 0.5 V input’s gain falls from 10 to 5: |VOUT| = 2 + 2.5 = 4.5 V instead of 7 V.', 'Độ lợi của ngõ 0,5 V giảm từ 10 xuống 5: |VOUT| = 2 + 2,5 = 4,5 V thay vì 7 V.', ('Floyd CA Q6', 'Floyd CA câu 6'))
G.ca('dif', 'If Rf is increased in Figure 13–40, the amplitude of the output voltage will', 'Nếu tăng Rf trong Hình 13–40 thì biên độ điện áp ra sẽ', F + 'fig13_40.png', 0, '|Vout| = Rf·C·|dVin/dt| is proportional to Rf.', '|Vout| = Rf·C·|dVin/dt| tỉ lệ với Rf.', ('Floyd CA Q10', 'Floyd CA câu 10'))
G.ca('intg', 'If Ri is increased in Figure 13–35, the slope of the output ramp will', 'Nếu tăng Ri trong Hình 13–35 thì độ dốc của đường dốc ngõ ra sẽ', F + 'fig13_35.png', 1, 'Slope = Vin/(Ri·C): larger Ri, smaller slope.', 'Độ dốc = Vin/(Ri·C): Ri lớn hơn thì độ dốc nhỏ hơn.', ('Floyd CA Q9', 'Floyd CA câu 9'))
G.write()
