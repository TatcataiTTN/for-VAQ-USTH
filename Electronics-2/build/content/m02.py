"""Module 02 — The operational amplifier (Floyd 9e Ch.12). Deck 5 parts x 4 slides + notes. Numbers computed here, not typed."""
import math
from hx import *
db = lambda r: 20 * math.log10(r)
def module(lang):
    vi = lang == 'vi'
    # ---- numbers used in slides/notes (same as verify_m02.py)
    cmrr5 = 175000 / 0.18; acl13 = 1 + 560 / 1.5; vo13 = acl13 * 0.01; b12 = 1 / 101
    aol37 = 10 ** (89 / 20); acl37 = aol37 / (5500 / 750); ft37 = acl37 * 5500
    f = lambda x, d=2: f'{x:,.{d}f}'
    P = []
    # ===== PART 1 Foundations
    s1 = sl(ul([tr('Op-amp = bộ khuếch đại vi sai ngõ vào–ra đơn, độ lợi vòng hở rất lớn', 'Op-amp = single-ended-output differential amplifier with very high open-loop gain'),
                tr('Hai ngõ vào: đảo (−) và không đảo (+); một ngõ ra; nguồn đối xứng ±V', 'Two inputs: inverting (−) and noninverting (+); one output; dual ±V supply'),
                tr('Lý tưởng: Zin = ∞, Zout = 0, Aol = ∞, băng thông = ∞, CMRR = ∞', 'Ideal: Zin = ∞, Zout = 0, Aol = ∞, bandwidth = ∞, CMRR = ∞')]) +
            table([tr('Tham số', 'Parameter'), tr('Lý tưởng', 'Ideal'), tr('Thực tế (điển hình)', 'Practical (typical)')],
                  [['Aol', '∞', '10⁵–2·10⁵'], ['Zin', '∞', '≈ MΩ–GΩ'], ['Zout', '0', '≈ 10–100 Ω'], ['CMRR', '∞', '≳ 90 dB']]),
            tr('Phần 1 · Nền tảng', 'Part 1 · Foundations'), tr('Op-amp lý tưởng và thực tế', 'Ideal and practical op-amps'),
            tr('Op-amp là “viên gạch” khuếch đại: nhận hiệu hai điện áp rồi nhân lên hàng trăm nghìn lần. Mạch ngoài (điện trở) mới quyết định độ lợi thực dùng.', 'An op-amp is an amplifier building block: it takes the difference of two voltages and multiplies it by hundreds of thousands. External resistors set the gain you actually use.'))
    s2 = sl(ul([tr('Vi sai ngõ vào đơn: một ngõ vào nối đất, tín hiệu vào ngõ còn lại', 'Single-ended differential: one input grounded, signal on the other'),
                tr('Vi sai ngõ vào kép: tín hiệu đặt giữa hai ngõ vào', 'Double-ended differential: signal between the two inputs'),
                tr('Chế độ chung: cùng một tín hiệu ở cả hai ngõ vào → ngõ ra ≈ 0 (nhiễu bị triệt)', 'Common mode: same signal on both inputs → output ≈ 0 (noise cancels)')]) +
            formula(tr('Độ lợi vi sai và chung', 'Differential and common-mode gain'), 'Vout = Aol·(V₊ − V₋) + Acm·V_cm'),
            tr('Phần 1 · Nền tảng', 'Part 1 · Foundations'), tr('Ba chế độ ngõ vào', 'Three input modes'),
            tr('Nhiễu thường xuất hiện giống hệt trên cả hai dây dẫn; vi sai chỉ khuếch đại phần khác nhau nên nhiễu bị loại.', 'Noise usually hits both wires identically; a differential stage amplifies only the difference, so the noise is rejected.'))
    s3 = sl(formula(tr('Tỉ số triệt tín hiệu chung', 'Common-mode rejection ratio'), 'CMRR = Aol / Acm  ,  CMRR(dB) = 20·log₁₀(Aol/Acm)', [('Aol', tr('độ lợi vòng hở', 'open-loop gain')), ('Acm', tr('độ lợi chế độ chung', 'common-mode gain'))]) +
            ex(tr('Bài 5 (Floyd)', 'Problem 5 (Floyd)'), f'Aol = 175 000, Acm = 0,18 → CMRR = {f(cmrr5,0)} → {f(db(cmrr5),1)} dB ≈ 120 dB'.replace('0,18', tr('0,18', '0.18'))),
            tr('Phần 1 · Nền tảng', 'Part 1 · Foundations'), tr('Tỉ số CMRR và đơn vị dB', 'CMRR and the decibel scale'),
            tr('CMRR càng lớn càng tốt. 20 dB nghĩa là gấp 10 lần điện áp, 40 dB là 100 lần, 80 dB là 10 000 lần.', 'Bigger CMRR is better. 20 dB is a factor of 10 in voltage, 40 dB is 100, 80 dB is 10,000.'))
    s4 = sl(table([tr('Tham số', 'Parameter'), tr('Công thức', 'Formula'), tr('Ý nghĩa', 'Meaning')],
                  [['I_BIAS', '(I₁ + I₂)/2', tr('dòng vào trung bình', 'average input current')], ['I_OS', '|I₁ − I₂|', tr('chênh lệch hai dòng vào', 'difference of the two input currents')],
                   ['V_OS', tr('áp vào để ngõ ra = 0', 'input voltage that nulls the output'), tr('lệch cân bằng tầng vào', 'input-stage imbalance')], ['SR', 'ΔV_out / Δt', tr('tốc độ đổi ngõ ra tối đa (V/μs)', 'maximum output change rate (V/μs)')]]) +
            ex(tr('Bài 7–10', 'Problems 7–10'), tr('I_BIAS = 8,1 μA; I_OS = 0,4 μA; SR = 24 V/15 μs = 1,6 V/μs; đổi −10→+10 V với 0,5 V/μs mất 40 μs', 'I_BIAS = 8.1 μA; I_OS = 0.4 μA; SR = 24 V/15 μs = 1.6 V/μs; −10→+10 V at 0.5 V/μs takes 40 μs')),
            tr('Phần 1 · Nền tảng', 'Part 1 · Foundations'), tr('Dòng phân cực, offset và slew rate', 'Bias, offset and slew rate'),
            tr('Hai ngõ vào luôn hút một dòng nhỏ; nếu hai dòng khác nhau sẽ có sai số một chiều. Slew rate giới hạn tín hiệu lớn, tần số cao.', 'Both inputs always draw a small current; if they differ you get a dc error. Slew rate limits large, fast signals.'))
    P.append(dict(title=tr('Nền tảng của op-amp', 'Op-amp foundations'), bullets=[tr('Lý tưởng so với thực tế', 'Ideal versus practical'), tr('Chế độ vi sai và chung, CMRR', 'Differential/common modes, CMRR'), tr('Dòng phân cực, offset, slew rate', 'Bias, offset, slew rate')], slides=[s1, s2, s3, s4]))
    # ===== PART 2 Methods
    s5 = sl(fig('assets/figs/m02/fig12_18.png', 'noninverting amplifier', tr('Floyd Hình 12–18', 'Floyd Fig. 12–18'), 420) +
            formula(tr('Mạch không đảo', 'Noninverting amplifier'), 'Acl(NI) = 1 + Rf/Ri  ,  B = Ri/(Ri + Rf)  ,  Acl ≈ 1/B') +
            tr('<p>Với Rf = 100 kΩ, Ri = 4,7 kΩ: Acl = ' + f(1 + 100 / 4.7, 1) + '.</p>', '<p>With Rf = 100 kΩ, Ri = 4.7 kΩ: Acl = ' + f(1 + 100 / 4.7, 1) + '.</p>'),
            tr('Phần 2 · Phương pháp', 'Part 2 · Methods'), tr('Bộ khuếch đại không đảo', 'The noninverting amplifier'),
            tr('Tín hiệu vào ngõ (+), một phần ngõ ra B được trả về ngõ (−). Ngõ (−) luôn bám theo ngõ (+), nên Vout = Vin/B.', 'The signal enters the (+) input and a fraction B of the output returns to (−). The (−) input follows (+), so Vout = Vin/B.'))
    s6 = sl(fig('assets/figs/m02/fig12_22.png', 'inverting amplifier', tr('Floyd Hình 12–22', 'Floyd Fig. 12–22'), 420) +
            formula(tr('Mạch đảo', 'Inverting amplifier'), 'Acl(I) = −Rf/Ri') +
            tr('<p>Ngõ vào đảo là “đất ảo”: dòng qua Ri bằng dòng qua Rf.</p>', '<p>The inverting input is a “virtual ground”: the current through Ri equals the current through Rf.</p>'),
            tr('Phần 2 · Phương pháp', 'Part 2 · Methods'), tr('Bộ khuếch đại đảo', 'The inverting amplifier'),
            tr('Vì (−) ≈ 0 V, dòng vào = Vin/Ri chạy hết qua Rf nên Vout = −Vin·Rf/Ri. Dấu trừ nghĩa là đảo pha 180°.', 'Because (−) ≈ 0 V, the input current Vin/Ri flows entirely through Rf, so Vout = −Vin·Rf/Ri. The minus sign means a 180° phase inversion.'))
    s7 = sl(table([tr('Cấu hình', 'Configuration'), 'Zin', 'Zout'],
                  [[tr('Không đảo', 'Noninverting'), '(1 + B·Aol)·Zin', 'Zout / (1 + B·Aol)'], [tr('Lặp điện áp', 'Voltage-follower'), '(1 + Aol)·Zin', 'Zout / (1 + Aol)'], [tr('Đảo', 'Inverting'), '≈ Ri', 'Zout / (1 + B·Aol)']]) +
            callout('info', tr('Mạch lặp điện áp', 'Voltage-follower'), tr('Ngõ ra nối thẳng về (−): Acl = 1, cùng pha, Zin cực lớn → mạch đệm.', 'Output wired straight to (−): Acl = 1, in phase, very large Zin → buffer.')),
            tr('Phần 2 · Phương pháp', 'Part 2 · Methods'), tr('Trở kháng vào/ra và mạch lặp', 'Input/output impedance and the follower'),
            tr('Hồi tiếp âm làm mạch “cứng” hơn: dễ nhận tín hiệu (Zin cao) và dễ cấp tải (Zout thấp).', 'Negative feedback makes the circuit “stiffer”: easy to drive (high Zin) and good at driving loads (low Zout).'))
    s8 = sl(formula(tr('Đáp ứng tần số', 'Frequency response'), 'Aol = Aol(mid)/√(1 + (f/fc)²)  ,  θ = −tan⁻¹(f/fc)  ,  fT = Aol(mid)·fc(ol)') +
            formula(tr('Vòng kín', 'Closed loop'), 'fc(cl) = fc(ol)(1 + B·Aol(mid))  ,  BWcl = BWol(1 + B·Aol(mid))  ,  fT = Acl·fc(cl)') +
            tr('<p>Độ dốc −20 dB/decade phía trên fc; tích độ lợi–băng thông không đổi.</p>', '<p>Roll-off is −20 dB/decade above fc; the gain–bandwidth product stays constant.</p>'),
            tr('Phần 2 · Phương pháp', 'Part 2 · Methods'), tr('Băng thông và tích độ lợi–băng thông', 'Bandwidth and the gain–bandwidth product'),
            tr('Muốn độ lợi lớn gấp 10 thì băng thông chỉ còn 1/10: đổi độ lợi lấy băng thông.', 'Ten times more gain leaves one tenth of the bandwidth: you trade gain for bandwidth.'))
    P.append(dict(title=tr('Phương pháp phân tích', 'Analysis methods'), bullets=[tr('Mạch không đảo và đảo', 'Noninverting and inverting'), tr('Trở kháng với hồi tiếp', 'Impedances with feedback'), tr('Đáp ứng tần số vòng kín', 'Closed-loop frequency response')], slides=[s5, s6, s7, s8]))
    # ===== PART 3 Worked examples
    s9 = sl(ex(tr('Floyd Bài 13', 'Floyd Problem 13'), f'Acl = 1 + 560/1,5 = {f(acl13,1)}; Vout = {f(vo13,3)} V rms; Vf = 10 mV'.replace('1,5', tr('1,5', '1.5')) if vi else f'Acl = 1 + 560/1.5 = {f(acl13,1)}; Vout = {f(vo13,3)} V rms; Vf ≈ 10 mV') +
            ex(tr('Floyd Bài 12', 'Floyd Problem 12'), f'B = 1/101 = {b12:.4f}; Vf = B·5 V = {b12*5*1e3:.1f} mV') +
            ex(tr('Floyd Bài 15', 'Floyd Problem 15'), tr('Rf = 49 kΩ, 3 MΩ, 84 kΩ, 165 kΩ (khớp đáp án sách)', 'Rf = 49 kΩ, 3 MΩ, 84 kΩ, 165 kΩ (match the book)')),
            tr('Phần 3 · Ví dụ từ sách', 'Part 3 · Book examples'), tr('Tính độ lợi và Rf (Floyd Bài 12–15)', 'Gain and Rf calculations (Floyd Problems 12–15)'),
            tr('Quy trình: xác định cấu hình → chọn công thức → thay số → kiểm tra bằng sách.', 'Procedure: identify the configuration → pick the formula → substitute → check against the book.'))
    s10 = sl(ex(tr('Floyd Bài 9', 'Floyd Problem 9'), 'SR = 24 V / 15 μs = 1,6 V/μs'.replace(',', tr(',', '.')) if True else '') +
              ex(tr('Floyd Bài 10', 'Floyd Problem 10'), tr('Δt = 20 V / (0,5 V/μs) = 40 μs', 'Δt = 20 V / (0.5 V/μs) = 40 μs')) +
              callout('warn', tr('Giới hạn slew rate', 'Slew-rate limit'), tr('Sin biên độ Vp tần số f cần SR ≥ 2π·f·Vp. Với 10 V đỉnh và 0,5 V/μs: f ≤ 7,96 kHz.', 'A sine of peak Vp at frequency f needs SR ≥ 2π·f·Vp. At 10 V peak and 0.5 V/μs: f ≤ 7.96 kHz.')),
              tr('Phần 3 · Ví dụ từ sách', 'Part 3 · Book examples'), tr('Slew rate và thời gian chuyển mức', 'Slew rate and transition time'),
              tr('Tần số tối đa không méo của sin: f_max = SR/(2π·Vp).', 'Maximum undistorted sine frequency: f_max = SR/(2π·Vp).'))
    s11 = sl(ex(tr('Floyd Bài 37', 'Floyd Problem 37'), f'fc(cl)/fc(ol) = 5500/750 = 7,333; Aol = {f(aol37,0)}; Acl = {f(acl37,0)} → {f(db(acl37),1)} dB'.replace('7,333', tr('7,333', '7.333')) if vi else f'fc(cl)/fc(ol) = 5500/750 = 7.333; Aol = {f(aol37,0)}; Acl = {f(acl37,0)} → {f(db(acl37),1)} dB') +
              ex(tr('Floyd Bài 38', 'Floyd Problem 38'), f'fT = Acl·fc(cl) = {f(acl37,0)} × 5,5 kHz = {f(ft37/1e6,1)} MHz'.replace('5,5', tr('5,5', '5.5'))) +
              tr('<p>Kiểm tra chéo: Aol·fc(ol) = ' + f(aol37 * 750 / 1e6, 1) + ' MHz.</p>', '<p>Cross-check: Aol·fc(ol) = ' + f(aol37 * 750 / 1e6, 1) + ' MHz.</p>'),
              tr('Phần 3 · Ví dụ từ sách', 'Part 3 · Book examples'), tr('Đáp ứng tần số vòng kín (Floyd Bài 37–38)', 'Closed-loop response (Floyd Problems 37–38)'),
              tr('Hai cách tính độ lợi–băng thông phải cho cùng kết quả: đó là phép tự kiểm tra tốt.', 'The two gain–bandwidth routes must agree: a good self-check.'))
    s12 = sl(fig('assets/figs/m02/fig12_43.png', 'closed-loop bandwidth circuits', tr('Floyd Hình 12–43', 'Floyd Fig. 12–43'), 520) +
             tr('<p>(a) Acl = 1 + 220/3,3 = ' + f(1 + 220 / 3.3, 1) + '; (b) |Acl| = 47.</p>', '<p>(a) Acl = 1 + 220/3.3 = ' + f(1 + 220 / 3.3, 1) + '; (b) |Acl| = 47.</p>'),
             tr('Phần 3 · Ví dụ từ sách', 'Part 3 · Book examples'), tr('So sánh hai mạch ở Hình 12–43', 'Comparing the two circuits of Fig. 12–43'),
             tr('Đổi Rf, Ri nhưng giữ tỉ số Rf/Ri thì độ lợi và băng thông không đổi (Circuit-Action câu 7).', 'Changing Rf and Ri while keeping Rf/Ri leaves gain and bandwidth unchanged (Circuit-Action Q7).'))
    P.append(dict(title=tr('Ví dụ từ sách', 'Worked examples from the book'), bullets=[tr('Độ lợi, B, Rf', 'Gain, B, Rf'), tr('Slew rate', 'Slew rate'), tr('Băng thông vòng kín', 'Closed-loop bandwidth')], slides=[s9, s10, s11, s12]))
    # ===== PART 4 Pitfalls
    s13 = sl(table([tr('Sự cố', 'Fault'), tr('Triệu chứng', 'Symptom')],
                   [[tr('Rf hở', 'Rf open'), tr('Hết hồi tiếp → độ lợi = Aol → bão hòa', 'No feedback → gain = Aol → saturation')], [tr('Ri hở (mạch đảo)', 'Ri open (inverting)'), tr('Tín hiệu không vào → ngõ ra ≈ 0', 'Signal cannot enter → output ≈ 0')],
                    [tr('Rf chập', 'Rf shorted'), tr('Độ lợi = 1 hoặc 0 (mạch đảo)', 'Gain = 1 (NI) or 0 (inverting)')]]),
             tr('Phần 4 · Sai lầm và mở rộng', 'Part 4 · Pitfalls and extensions'), tr('Sự cố điện trở hồi tiếp', 'Feedback-resistor faults'),
             tr('Hỏi “đường hồi tiếp còn nguyên không?” là câu đầu tiên khi sửa mạch op-amp.', '“Is the feedback path intact?” is the first question when troubleshooting an op-amp circuit.'))
    s14 = sl(callout('warn', tr('Bù dòng phân cực', 'Bias-current compensation'), tr('Thêm Rc = Ri‖Rf vào ngõ (+) của mạch đảo để hai sụt áp do dòng phân cực bằng nhau; sai số ngõ ra còn lại chỉ do I_OS và V_OS.', 'Add Rc = Ri‖Rf at the (+) input of an inverting amplifier so both bias-current drops are equal; the remaining output error comes only from I_OS and V_OS.')) +
             formula(tr('Điện trở bù', 'Compensating resistor'), 'Rc = Ri‖Rf = Ri·Rf/(Ri + Rf)'),
             tr('Phần 4 · Sai lầm và mở rộng', 'Part 4 · Pitfalls and extensions'), tr('Bù dòng phân cực và chỉnh null offset', 'Bias compensation and offset nulling'),
             tr('Dòng phân cực nhỏ nhưng qua điện trở lớn sẽ tạo điện áp một chiều đáng kể ở ngõ ra.', 'A small bias current through a large resistor still produces a noticeable dc output error.'))
    s15 = sl(ul([tr('Biên độ nhỏ, tần số cao → bị giới hạn bởi băng thông (GBP)', 'Small amplitude, high frequency → limited by bandwidth (GBP)'), tr('Biên độ lớn, tần số cao → bị giới hạn bởi slew rate → méo thành tam giác', 'Large amplitude, high frequency → limited by slew rate → triangular distortion'), tr('Cả hai đều xuất hiện khi tăng tần số; hãy kiểm tra cả hai', 'Both appear as frequency rises; check both')]),
             tr('Phần 4 · Sai lầm và mở rộng', 'Part 4 · Pitfalls and extensions'), tr('Hai giới hạn tần số: băng thông và slew rate', 'Two frequency limits: bandwidth and slew rate'),
             tr('Một tín hiệu có thể “đủ băng thông” nhưng vẫn méo vì đổi mức quá nhanh so với slew rate.', 'A signal can be “within bandwidth” yet distorted because it changes faster than the slew rate allows.'))
    s16 = sl(formula(tr('Độ lợi chính xác', 'Exact closed-loop gain'), 'Acl = Aol / (1 + B·Aol)  →  1/B khi B·Aol ≫ 1') +
             tr('<p>Với Aol = 100 000 và B = 1/101: Acl = ' + f(100000 / (1 + 100000 / 101), 4) + ' (so với 101). Sai số ≈ 0,1 %.</p>', '<p>With Aol = 100,000 and B = 1/101: Acl = ' + f(100000 / (1 + 100000 / 101), 4) + ' (versus 101). Error ≈ 0.1 %.</p>'),
             tr('Phần 4 · Sai lầm và mở rộng', 'Part 4 · Pitfalls and extensions'), tr('Sai số do Aol hữu hạn', 'Error from finite Aol'),
             tr('Công thức 1 + R f/Ri chỉ đúng khi Aol rất lớn; Aol thấp hoặc ở tần số cao sai số tăng.', 'The 1 + Rf/Ri formula assumes a huge Aol; with a low Aol or at high frequency the error grows.').replace('R f/Ri', 'Rf/Ri'))
    P.append(dict(title=tr('Sai lầm thường gặp', 'Common pitfalls'), bullets=[tr('Sự cố Rf/Ri', 'Rf/Ri faults'), tr('Bù dòng phân cực', 'Bias compensation'), tr('Băng thông so với slew rate', 'Bandwidth versus slew rate')], slides=[s13, s14, s15, s16]))
    # ===== PART 5 Aircraft + summary
    s17 = sl(ul([tr('Minh hoạ: bộ khuếch đại thiết bị cho cảm biến (nhiệt ngẫu, cầu đo biến dạng) cần CMRR cao vì dây dài mang nhiễu chung', 'Illustrative: instrumentation amplifiers for sensors (thermocouples, strain-gauge bridges) need high CMRR because long wires pick up common-mode noise'),
                 tr('Minh hoạ: mạch lặp đệm tín hiệu từ cảm biến trở kháng cao trước bộ chuyển đổi A/D', 'Illustrative: a follower buffers a high-impedance sensor before an A/D converter'),
                 tr('Điều kiện bay: nhiệt độ rộng làm I_BIAS và V_OS trôi → chọn op-amp offset thấp', 'Flight conditions: wide temperature drifts I_BIAS and V_OS → choose a low-offset part')]),
             tr('Phần 5 · Ứng dụng trên tàu bay', 'Part 5 · Aircraft applications'), tr('Điều hoà tín hiệu cảm biến', 'Sensor signal conditioning'),
             tr('Các ví dụ này chỉ minh hoạ nguyên lý, không mô tả một hệ thống tàu bay cụ thể.', 'These examples only illustrate the principle; they do not describe a specific aircraft system.'))
    s18 = sl(table([tr('Đại lượng', 'Quantity'), tr('Công thức', 'Formula')],
                   [['CMRR', 'Aol/Acm = 20·log₁₀(Aol/Acm) dB'], ['I_BIAS, I_OS', '(I₁+I₂)/2 ; |I₁−I₂|'], ['SR', 'ΔVout/Δt'], ['Acl(NI)', '1 + Rf/Ri'], ['Acl(I)', '−Rf/Ri'], ['Zin(NI), Zout(NI)', '(1+B·Aol)·Zin ; Zout/(1+B·Aol)'], ['fc(cl), BWcl', 'fc(ol)(1+B·Aol(mid))'], ['fT', 'Acl·fc(cl) = Aol(mid)·fc(ol)']]),
             tr('Phần 5 · Tổng kết', 'Part 5 · Summary'), tr('Bảng công thức chương 12', 'Chapter 12 formula table'),
             tr('Thuộc ba công thức độ lợi, CMRR và fT là đủ giải phần lớn bài tập.', 'The three formulas for gain, CMRR and fT solve most exercises.'))
    s19 = sl(ul([tr('Nêu 4 đặc điểm của op-amp lý tưởng', 'State 4 ideal op-amp characteristics'), tr('Tính CMRR (dB) khi Aol = 100 000, Acm = 0,5', 'Compute CMRR (dB) for Aol = 100,000 and Acm = 0.5') + f' → {f(db(100000/0.5),1)} dB', tr('Mạch không đảo Rf = 47 kΩ, Ri = 4,7 kΩ: Acl = ?', 'Noninverting amp Rf = 47 kΩ, Ri = 4.7 kΩ: Acl = ?') + ' → 11',
                 tr('Op-amp có fT = 5 MHz, Acl = 50: BW = ?', 'Op-amp with fT = 5 MHz, Acl = 50: BW = ?') + ' → 100 kHz']),
             tr('Phần 5 · Tổng kết', 'Part 5 · Summary'), tr('Tự kiểm tra nhanh', 'Quick self-check'),
             tr('Làm thêm ở ngân hàng câu hỏi bên dưới (165 câu trắc nghiệm + 13 bài tự luận).', 'Practise more in the question bank below (165 multiple-choice + 13 worked problems).'))
    s20 = sl(ul([tr('Op-amp thực dùng với hồi tiếp âm: độ lợi do điện trở quyết định', 'Real op-amps are used with negative feedback: resistors set the gain'), tr('Hồi tiếp đổi độ lợi lấy băng thông, tăng Zin, giảm Zout', 'Feedback trades gain for bandwidth, raises Zin, lowers Zout'), tr('Module sau: mạch so sánh, cộng, tích phân, vi phân', 'Next module: comparators, summers, integrators, differentiators')]),
             tr('Phần 5 · Tổng kết', 'Part 5 · Summary'), tr('Ba ý chính của module', 'Three take-aways'), tr('Nắm chắc công thức vòng kín là nền cho mọi mạch op-amp về sau.', 'Mastering the closed-loop formulas is the base for every later op-amp circuit.'))
    P.append(dict(title=tr('Ứng dụng và tổng kết', 'Applications and summary'), bullets=[tr('Cảm biến trên tàu bay (minh hoạ)', 'Aircraft sensors (illustrative)'), tr('Bảng công thức', 'Formula table'), tr('Tự kiểm tra', 'Self-check')], slides=[s17, s18, s19, s20]))
    # ===== NOTES
    nt = '<h3>1. ' + tr('Nội dung chi tiết đối chiếu sách', 'Detailed content mapped to the books') + '</h3>' + ul([
        tr('Floyd §12–1: op-amp lý tưởng/thực tế, ký hiệu. §12–2: ngõ vào đơn/kép, chế độ chung, CMRR, I_BIAS, I_OS, V_OS, slew rate.', 'Floyd §12–1: ideal/practical op-amp, symbol. §12–2: single/double-ended and common mode, CMRR, I_BIAS, I_OS, V_OS, slew rate.'),
        tr('Floyd §12–3 đến §12–5: hồi tiếp âm, mạch không đảo/đảo/lặp, ảnh hưởng lên Zin và Zout.', 'Floyd §12–3 to §12–5: negative feedback, noninverting/inverting/follower, effect on Zin and Zout.'),
        tr('Floyd §12–6: bù dòng phân cực. §12–7: đáp ứng tần số và pha vòng hở. §12–8: đáp ứng vòng kín. §12–9: kiểm tra sự cố.', 'Floyd §12–6: bias-current compensation. §12–7: open-loop frequency and phase. §12–8: closed-loop response. §12–9: troubleshooting.'),
        tr('Đọc thêm: Jaeger 5e Ch.10 §10.5–10.9 và Ch.11 §11.2, 11.11–11.13 theo bản đồ đề cương (chưa trích trang cụ thể).', 'See also Jaeger 5e Ch.10 §10.5–10.9 and Ch.11 §11.2, 11.11–11.13 per the syllabus map (no page-level quotes).')])
    nt += '<h3>2. ' + tr('Năm ví dụ có lời giải số', 'Five worked examples') + '</h3>' + ''.join([
        ex(tr('Ví dụ 1 – CMRR (Floyd Bài 5)', 'Example 1 – CMRR (Floyd Problem 5)'), f'CMRR = 175000/0.18 = {f(cmrr5,0)}; 20·log₁₀ = {f(db(cmrr5),2)} dB'),
        ex(tr('Ví dụ 2 – Không đảo (Floyd Bài 13)', 'Example 2 – Noninverting (Floyd Problem 13)'), f'Acl = 1 + 560/1.5 = {f(acl13,2)}; Vout = {f(vo13,3)} V rms; B = 1.5/561.5 = {1.5/561.5:.5f}; Vf = {f(1.5/561.5*vo13*1e3,2)} mV'),
        ex(tr('Ví dụ 3 – Slew rate (Floyd Bài 9–10)', 'Example 3 – Slew rate (Floyd Problems 9–10)'), 'SR = 24/15 = 1.6 V/μs; Δt = 20/0.5 = 40 μs'),
        ex(tr('Ví dụ 4 – Vòng kín (Floyd Bài 37–38)', 'Example 4 – Closed loop (Floyd Problems 37–38)'), f'Acl = {f(acl37,0)} ({f(db(acl37),1)} dB); fT = {f(ft37/1e6,1)} MHz'),
        ex(tr('Ví dụ 5 – Trở kháng không đảo', 'Example 5 – Noninverting impedances'), f'Aol = 100 000, B = 1/101 → 1 + B·Aol = {f(1+100000/101,1)}; Zin = 2 MΩ → {f((1+100000/101)*2e6/1e9,2)} GΩ; Zout = 75 Ω → {f(75/(1+100000/101)*1e3,1)} mΩ')])
    nt += '<h3>3. ' + tr('Bối cảnh lịch sử/lý thuyết', 'History and theory context') + '</h3><p>' + tr('Op-amp xuất phát từ máy tính tương tự (thực hiện phép cộng, tích phân); vi mạch đơn khối như 741 làm cho chúng rẻ và ổn định. Ý tưởng cốt lõi là hồi tiếp âm: độ lợi lớn được đổi lấy sự chính xác và độ ổn định.', 'Op-amps began in analog computers (summing and integrating); monolithic ICs such as the 741 made them cheap and stable. The core idea is negative feedback: large gain is traded for precision and stability.') + '</p>'
    nt += '<h3>4. ' + tr('Ca ứng dụng trên tàu bay (minh hoạ)', 'Aircraft case study (illustrative)') + '</h3><p>' + tr('Minh hoạ: điều hoà tín hiệu cho cảm biến nhiệt độ hoặc áp suất — bộ khuếch đại vi sai CMRR cao loại nhiễu chung trên dây dài, mạch lặp đệm trước bộ chuyển đổi A/D. Đây là ví dụ nguyên lý, không phải mô tả hệ thống cụ thể.', 'Illustrative: signal conditioning for temperature or pressure sensors — a high-CMRR differential stage rejects common-mode noise on long wires and a follower buffers the signal ahead of the A/D converter. A principle example, not a specific system description.') + '</p>'
    nt += '<h3>5. ' + tr('Bẫy khi làm bài thi', 'Exam pitfalls') + '</h3>' + ul([
        tr('Quên “+1” ở mạch không đảo; nhầm dấu ở mạch đảo.', 'Forgetting the “+1” in the noninverting gain; dropping the sign in the inverting gain.'),
        tr('Dùng 10·log thay 20·log cho tỉ số điện áp.', 'Using 10·log instead of 20·log for voltage ratios.'),
        tr('Nhầm I_BIAS (trung bình) với I_OS (hiệu).', 'Mixing up I_BIAS (average) with I_OS (difference).'),
        tr('Đổi đơn vị μs/ms khi tính slew rate.', 'Unit slips between μs and ms in slew rate.'),
        tr('Rf hở → độ lợi KHÔNG bằng 0 mà tăng lên Aol.', 'Rf open → gain does NOT become zero but rises to Aol.')])
    return dict(subtitle=tr('Op-amp lý tưởng và thực tế, CMRR, slew rate, hồi tiếp âm và đáp ứng tần số (Floyd chương 12).', 'Ideal and practical op-amps, CMRR, slew rate, negative feedback and frequency response (Floyd Chapter 12).'),
                time=tr('≈ 6 giờ lý thuyết + bài tập', '≈ 6 h lecture + exercises'),
                objectives=[tr('Phân biệt op-amp lý tưởng và thực tế', 'Distinguish ideal from practical op-amps'), tr('Tính CMRR, I_BIAS, I_OS, slew rate', 'Compute CMRR, I_BIAS, I_OS, slew rate'), tr('Tính độ lợi, B, Zin, Zout của mạch hồi tiếp âm', 'Compute gain, B, Zin, Zout of negative-feedback circuits'), tr('Dùng fT để tìm băng thông vòng kín', 'Use fT to find closed-loop bandwidth')],
                parts=P, notes=nt)
