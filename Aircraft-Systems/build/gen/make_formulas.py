# -*- coding: utf-8 -*-
"""data/formulas.json: tom tat cong thuc theo module. Moi cong thuc: id, module, ten VI/EN, LaTeX, chu giai bien, nguon (chi ghi muc sach da doc; module cu ghi o cap chuong va module).
Cong thuc da duoc kiem trong module tuong ung (demo, notebook hoac verify). Chua gan so slide."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
F = [
 ('m01', 'Giá trị theo vị trí', 'Positional value', r'N_{10}=\sum_i d_i\,b^{\,i}', 'd_i: chữ số ở vị trí i; b: cơ số.', 'd_i: digit at position i; b: radix.', 'Tooley Ch.2; Floyd Ch.2'),
 ('m01', 'Khoảng giá trị của số n bit', 'Range of an n-bit number', r'0\ \text{đến}\ 2^n-1\ \ (\text{không dấu});\quad -2^{n-1}\ \text{đến}\ 2^{n-1}-1\ \ (\text{bù hai})', 'n: số bit.', 'n: number of bits.', 'Floyd Ch.2'),
 ('m01', 'Số bit mỗi chữ số', 'Bits per digit', r'\text{bát phân}=3\ \text{bit},\quad \text{thập lục phân}=4\ \text{bit}', '', '', 'Tooley Ch.2'),
 ('m02', 'Định lý De Morgan', "De Morgan's theorem", r'\overline{A\cdot B}=\overline{A}+\overline{B},\qquad \overline{A+B}=\overline{A}\cdot\overline{B}', 'A, B: biến logic.', 'A, B: logic variables.', 'Floyd Ch.4; Tooley Ch.5'),
 ('m02', 'Số hàng của bảng chân trị', 'Rows of a truth table', r'2^n', 'n: số biến vào.', 'n: number of input variables.', 'Floyd Ch.3'),
 ('m02', 'Biên chống nhiễu', 'Noise margin', r'V_{NH}=V_{OH(min)}-V_{IH(min)},\qquad V_{NL}=V_{IL(max)}-V_{OL(max)}', 'Mức ra của cổng lái trừ mức vào của cổng nhận, cùng mức logic.', 'Output level of the driving gate minus input level of the receiving gate, same logic level.', 'Floyd §15-3 (Phương trình 15-1, 15-2)'),
 ('m03', 'Số đường chọn của bộ dồn kênh', 'Select lines of a multiplexer', r'n=\log_2 N', 'N: số kênh vào; n: số đường chọn.', 'N: number of input channels; n: number of select lines.', 'Tooley Ch.9; Floyd Ch.6'),
 ('m03', 'Bộ giải mã n sang $2^n$', 'n-to-$2^n$ decoder', r'n\ \text{đầu vào}\rightarrow 2^n\ \text{đầu ra}', '', '', 'Tooley Ch.9; Floyd Ch.6'),
 ('m04', 'Dung lượng bộ nhớ', 'Memory capacity', r'\text{số ô}=2^{a},\qquad \text{bit}=2^{a}\times w', 'a: số đường địa chỉ; w: số bit mỗi ô.', 'a: number of address lines; w: bits per cell.', 'Floyd Ch.11; Tooley Ch.6'),
 ('m04', 'Thời gian thực thi lệnh', 'Instruction execution time', r't=n_T\cdot\dfrac{1}{f_{clk}}', 'n_T: số T-state; f_clk: tần số xung nhịp.', 'n_T: number of T-states; f_clk: clock frequency.', 'Module 04, bài giảng'),
 ('m05', 'Thời gian truyền một từ ARINC 429', 'Transmission time of one ARINC 429 word', r't=\dfrac{32}{R}\quad(R=12{,}5\ \text{kbps}\Rightarrow 2{,}56\ \text{ms};\ R=100\ \text{kbps}\Rightarrow 0{,}32\ \text{ms})', 'R: tốc độ bit.', 'R: bit rate.', 'Tooley Ch.4; Module 05'),
 ('m06', 'Tần số quét dòng của raster', 'Line frequency of a raster', r'f_X=N_{line}\cdot f_Y', 'N_line: số dòng; f_Y: tần số quét khung.', 'N_line: number of lines; f_Y: frame frequency.', 'Module 06'),
 ('m07', 'Checksum', 'Checksum', r'\text{checksum}=\left(\sum_i b_i\right)\bmod 256', 'b_i: byte thứ i.', 'b_i: i-th byte.', 'Tooley Ch.13; Floyd §11-11'),
 ('m07', 'Xác suất theo mức hỏng', 'Probability by failure level', r'A<10^{-9},\quad B:10^{-9}\ \text{đến}\ 10^{-7},\quad C:10^{-7}\ \text{đến}\ 10^{-5},\quad D>10^{-5}', 'Xác suất cho phép của hỏng; mức A nghiêm trọng nhất.', 'Allowed failure probability; level A is the most severe.', 'Tooley Bảng 13.1'),
 ('m08', 'Định luật Snell', "Snell's law", r'n_1\sin\theta_1=n_2\sin\theta_2', 'n: chiết suất; θ: góc so với pháp tuyến.', 'n: refractive index; θ: angle from the normal.', 'Tooley §10.2; Module 08'),
 ('m08', 'Góc tới hạn', 'Critical angle', r'\sin\theta_c=\dfrac{n_2}{n_1}', 'n_1 > n_2.', 'n_1 > n_2.', 'Tooley §10.2'),
 ('m08', 'Khẩu độ số và góc chấp nhận', 'Numerical aperture and acceptance angle', r'NA=\sqrt{n_1^2-n_2^2}=\sin\theta_a', 'Trong không khí.', 'In air.', 'Tooley §10.2'),
 ('m08', 'Tần số chuẩn hoá và số mode', 'Normalised frequency and number of modes', r'V=\dfrac{\pi\,d\,NA}{\lambda},\qquad N\approx\dfrac{V^2}{2}', 'd: đường kính lõi; λ: bước sóng.', 'd: core diameter; λ: wavelength.', 'Bài giảng cáp quang; Module 08'),
 ('m08', 'Suy hao và độ dài tối đa', 'Attenuation and maximum length', r'L_{max}=\dfrac{10\log_{10}(P_{in}/P_{min})}{A}', 'A: suy hao dB/km.', 'A: attenuation in dB/km.', 'Bài giảng cáp quang (slide 27); Tooley §10.2'),
 ('m08', 'Tán sắc mode (công thức đã sửa)', 'Modal dispersion (corrected)', r'\Delta t=\dfrac{n_1(n_1-n_2)\,L}{c\,n_2}', 'L: chiều dài sợi.', 'L: fibre length.', 'Module 08 (slide 28 in thiếu hệ số $n_1/n_2$)'),
 ('m09', 'dB theo công suất và biên độ', 'dB for power and amplitude', r'L_P=10\log_{10}\dfrac{P_2}{P_1},\qquad L_A=20\log_{10}\dfrac{A_2}{A_1}', 'Hệ số 20 vì $P\\propto V^2$.', 'The factor 20 is because $P\\propto V^2$.', 'Bài giảng EMC; Tooley Ch.14'),
 ('m09', 'dBm', 'dBm', r'P_{dBm}=10\log_{10}\dfrac{P}{1\ \text{mW}}', '0 dBm = 1 mW.', '0 dBm = 1 mW.', 'Bài giảng EMC'),
 ('m09', 'Hài của sóng vuông', 'Harmonics of a square wave', r'v(t)=V\left[\sin\omega t+\tfrac13\sin3\omega t+\tfrac15\sin5\omega t+\cdots\right]', 'Chỉ hài lẻ; V là biên độ hài cơ bản.', 'Odd harmonics only; V is the fundamental amplitude.', 'Tooley §14.1; bài giảng EMC'),
 ('m09', 'Cộng hưởng của tụ thực', 'Resonance of a real capacitor', r'f_r=\dfrac{1}{2\pi\sqrt{LC}}', 'L: điện cảm ký sinh (ESL).', 'L: parasitic inductance (ESL).', 'Bài giảng EMC'),
 ('m09', 'Tần số cắt bộ lọc RC', 'RC filter cutoff', r'f_c=\dfrac{1}{2\pi RC}', 'Tại $f_c$ giảm 3 dB.', 'Down 3 dB at $f_c$.', 'Công thức chuẩn, dùng ở Module 09'),
 ('m10', 'Định lý lấy mẫu', 'Sampling theorem', r'f_{sample}\geq 2f_{a(max)}', 'f_a(max): tần số tín hiệu cao nhất.', 'f_a(max): highest signal frequency.', 'Floyd §12-1 (Phương trình 12-1)'),
 ('m10', 'Độ phân giải DAC', 'DAC resolution', r'\dfrac{1}{2^n-1}\times100\%', 'n: số bit.', 'n: number of bits.', 'Floyd §12-3'),
 ('m10', 'Số bộ so sánh của ADC flash', 'Comparators in a flash ADC', r'2^n-1', 'n: số bit.', 'n: number of bits.', 'Floyd §12-2; Tooley §3.3'),
 ('m10', 'DAC trọng số nhị phân (Tooley)', 'Binary-weighted DAC (Tooley)', r'V_{out}=-V\left(b_3+\tfrac{b_2}{2}+\tfrac{b_1}{4}+\tfrac{b_0}{8}\right)', 'V: mức logic 1 (+5 V); $b_3$ là MSB.', 'V: logic-1 level (+5 V); $b_3$ is the MSB.', 'Tooley §3.2'),
 ('m10', 'DAC thang R-2R (Floyd)', 'R-2R ladder DAC (Floyd)', r'V_{out}=-V_{ref}\dfrac{\text{code}}{2^{\,n-1}}\quad(R_f=2R)', 'n = 4 trong Floyd Hình 12-29.', 'n = 4 in Floyd Figure 12-29.', 'Floyd §12-3'),
 ('m10', 'Khuếch đại đảo', 'Inverting amplifier', r'\dfrac{V_{out}}{V_{in}}=-\dfrac{R_f}{R_i}', '', '', 'Floyd §12-2 (Phương trình 12-2)'),
 ('m10', 'Sai số lớn nhất của DAC', 'Maximum DAC error', r'\varepsilon=\text{accuracy}\times V_{FS}', 'Độ chính xác tính theo phần trăm toàn thang.', 'Accuracy as a percentage of full scale.', 'Floyd §12-3'),
]
out = [dict(id=f'f{i + 1:02d}', module=m, name=dict(vi=nv, en=ne), latex=lx, legend=dict(vi=lv, en=le), src=s) for i, (m, nv, ne, lx, lv, le, s) in enumerate(F)]
json.dump(out, open(os.path.join(ROOT, 'data', 'formulas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'cong thuc')
