# -*- coding: utf-8 -*-
"""Cau hoi module 10 (chuyen doi du lieu A/D, D/A) -> data/qsrc/m10.json (cau goc co nguon), m10_gen.json (sinh theo dang, bo_sung), m10_ess.json (tu luan co dap an in).
Khoa Tooley Ch.3 (App.3 tr.377, DOC TU ANH QUET): 1a 2b 3b 4b 5c 6c 7b 8c 9c 10a 11b 12c 13b. Dap an Floyd (tr.737-738 va A-26) doc tu text.
Dap an cua moi cau tinh bang build/numlib/adda.py; verify_m10.py doi chieu lai bang cach doc lap."""
import json, os, sys, random, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'numlib')); import adda as A
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); OUT = os.path.join(ROOT, 'data', 'qsrc')
TOP = {'sampling': ('Lấy mẫu, Nyquist, lượng tử hoá', 'Sampling, Nyquist, quantisation'), 'dac': ('DAC trọng số nhị phân và thang R-2R', 'Binary-weighted and R-2R ladder DACs'),
       'adc': ('Các kiểu ADC', 'Types of ADC'), 'specs': ('Độ phân giải, độ chính xác, lỗi chuyển đổi', 'Resolution, accuracy, conversion errors'),
       'opamp': ('Op-amp trong bộ chuyển đổi', 'Op-amps in converters')}
items, gen, ess = [], [], []
def p(*t): return ''.join(f'<p>{x}</p>' for x in t)
def Q(lst, tid, level, origin, kind, qv, qe, ov, oe, c, xv, xe, sv, se, dv='', de=''):
    d = dict(kind=kind, q=dict(vi=qv, en=qe), opts=[dict(vi=a, en=b) for a, b in zip(ov, oe)], correct=c, explain=dict(vi=xv, en=xe),
             topic=dict(vi=TOP[tid][0], en=TOP[tid][1]), topic_id=tid, level=level, origin=origin, src=dict(vi=sv, en=se))
    if dv: d['detail'] = dict(vi=dv, en=de)
    lst.append(d)
TF = (['Đúng', 'Sai'], ['True', 'False'])

# ---------------- A. Tooley Ch.3: 13 cau, khoa doc tu anh quet A.3 ----------------
T = lambda n: (f'Tooley Ch.3 · Câu {n} (khoá A.3, tr.377)', f'Tooley Ch.3 · Q{n} (key A.3, p.377)')
def TQ(n, tid, lv, qv, qe, ov, oe, c, xv, xe, dv='', de=''):
    sv, se = T(n); Q(items, tid, lv, 'goc', 'mcq', qv, qe, ov, oe, c, xv, xe, sv, se, dv, de)
TQ(1, 'specs', 1, 'Một DAC tạo ra được 256 điện áp ra khác nhau. DAC này có độ phân giải:', 'A DAC can produce 256 different output voltages. This DAC has a resolution of:',
   ['8 bit', '128 bit', '256 bit'], ['8 bits', '128 bits', '256 bits'], 0, '2^8 = 256 mức nên cần 8 bit.', '2^8 = 256 levels so 8 bits are needed.',
   p('Số mức ra của DAC n bit là $2^n$; 256 mức nghĩa là $n=\\log_2 256=8$. Độ phân giải của DAC được nêu bằng SỐ BIT dùng trong chuyển đổi (Tooley 3.2.1), không phải số mức.', 'Bẫy: 256 là số mức chứ không phải số bit; 128 là $2^{7}$.'),
   p('A DAC with $n$ bits has $2^n$ output levels; 256 levels means $n=\\log_2 256=8$. The resolution of a DAC is stated as the NUMBER OF BITS used in the conversion (Tooley 3.2.1), not the number of levels.', 'Trap: 256 is the number of levels, not bits; 128 is $2^{7}$.'))
TQ(2, 'sampling', 1, 'Trong ADC lưỡng cực, mức logic 1 ở vị trí MSB cho biết:', 'In a bipolar ADC a logic 1 in the MSB position indicates:',
   ['điện áp vào bằng không', 'điện áp vào âm', 'điện áp vào dương'], ['zero input voltage', 'negative input voltage', 'positive input voltage'], 1,
   'Mã bù hai: MSB = 1 là số âm (Tooley 3.1).', 'Two\'s complement code: MSB = 1 means a negative value (Tooley 3.1).',
   p('Tooley dùng biểu diễn bù hai cho ADC 4 bit lưỡng cực (Hình 3.3): các mã $0001$ đến $0111$ ứng với điện áp dương, $1000$ đến $1111$ ứng với điện áp âm. Mọi mã có MSB bằng 1 là điện áp âm.', 'Nhớ lại Module 01: bù hai, MSB là bit dấu.'),
   p('Tooley uses two\'s complement for the 4-bit bipolar ADC (Figure 3.3): codes $0001$ to $0111$ are positive voltages, $1000$ to $1111$ are negative. Every code whose MSB is 1 is a negative voltage.', 'Recall Module 01: two\'s complement, the MSB is the sign bit.'))
TQ(3, 'adc', 1, 'Kiểu ADC nào sau đây nhanh nhất?', 'Which one of the following types of ADC is the fastest:',
   ['kiểu dốc (ramp)', 'kiểu flash', 'kiểu xấp xỉ liên tiếp'], ['ramp type', 'flash type', 'successive approximation type'], 1,
   'Flash 50 ns đến 1 µs; xấp xỉ liên tiếp 10 đến 100 µs; hai dốc 500 µs đến 20 ms.', 'Flash 50 ns to 1 µs; successive approximation 10 to 100 µs; dual slope 500 µs to 20 ms.',
   p('Flash so sánh đồng thời với mọi mức chuẩn nên chỉ cần một bước. Thời gian điển hình theo Tooley 3.3: flash 50 ns đến 1 µs, xấp xỉ liên tiếp 10 đến 100 µs, dốc đôi 500 µs đến 20 ms. Floyd cũng kết luận phương pháp flash (đồng thời) nhanh nhất (Checkup 12-2 câu 1).'),
   p('Flash compares with every reference at the same time so one step is enough. Typical times in Tooley 3.3: flash 50 ns to 1 µs, successive approximation 10 to 100 µs, dual slope 500 µs to 20 ms. Floyd also concludes that the flash (simultaneous) method is fastest (Checkup 12-2 question 1).'))
TQ(4, 'adc', 1, 'Kiểu ADC nào dùng một số lượng lớn bộ so sánh?', 'Which one of the following ADC types uses a large number of comparators:',
   ['kiểu dốc (ramp)', 'kiểu flash', 'kiểu xấp xỉ liên tiếp'], ['ramp type', 'flash type', 'successive approximation type'], 1,
   'Flash n bit cần $2^n-1$ bộ so sánh.', 'An n-bit flash needs $2^n-1$ comparators.',
   p('ADC flash n bit cần $2^n-1$ bộ so sánh (Floyd 12-2): 3 bit cần 7, 4 bit cần 15, 8 bit cần 255. Tooley nói tròn 256 cho 8 bit và 1 024 cho 10 bit; con số chính xác là 255 và 1 023.', 'Đây là nhược điểm chính của flash: phức tạp và đắt khi số bit tăng.'),
   p('An n-bit flash ADC needs $2^n-1$ comparators (Floyd 12-2): 3 bits need 7, 4 bits need 15, 8 bits need 255. Tooley says 256 for 8 bits and 1,024 for 10 bits in round numbers; the exact counts are 255 and 1,023.', 'This is the main drawback of flash: complexity and cost grow quickly with the bit count.'))
TQ(5, 'dac', 2, 'Ưu điểm của DAC thang R-2R là:', 'The advantage of an R-2R ladder DAC is that:',
   ['dùng tổng số điện trở ít hơn', 'dùng ít công tắc tương tự hơn', 'tránh phải dùng nhiều giá trị điện trở khác nhau'], ['it uses fewer resistors overall', 'it uses a smaller number of analogue switches', 'it avoids having a large number of different value resistors'], 2,
   'Chỉ cần hai giá trị điện trở, R và 2R.', 'Only two resistor values are needed, R and 2R.',
   p('DAC trọng số nhị phân 10 bit với R = 1 kΩ cần các điện trở từ 1 kΩ đến 512 kΩ, tất cả phải sai số 1 % hoặc tốt hơn (Tooley 3.2). Thang R-2R chỉ cần hai giá trị, một giá trị gấp đôi giá trị kia, nên dễ chế tạo cặp điện trở khớp nhau trên chip. Tổng số điện trở thì thang R-2R không ít hơn.'),
   p('A 10-bit binary-weighted DAC with R = 1 kΩ needs resistors from 1 kΩ to 512 kΩ, all to 1 % or better (Tooley 3.2). The R-2R ladder needs only two values, one double the other, so matched resistors are easy to make on a chip. The total number of resistors is not smaller.'))
TQ(6, 'specs', 1, 'DAC 10 bit có thể tạo ra:', 'A 10-bit DAC is capable of producing:',
   ['10 mức ra khác nhau', '100 mức ra khác nhau', '1 024 mức ra khác nhau'], ['10 different output levels', '100 different output levels', '1,024 different output levels'], 2,
   '$2^{10}=1024$.', '$2^{10}=1024$.',
   p('Số mức ra là $2^n$. Với $n=10$ ta có 1 024 mức (Tooley 3.2.1). Số bước giữa mức nhỏ nhất và lớn nhất là $2^n-1=1023$ (cách Floyd tính độ phân giải).'),
   p('The number of output levels is $2^n$. For $n=10$ that is 1,024 levels (Tooley 3.2.1). The number of steps from the lowest to the highest level is $2^n-1=1023$ (how Floyd computes resolution).'))
TQ(7, 'sampling', 1, 'Quá trình xấp xỉ một tín hiệu tương tự bằng một chuỗi mức rời rạc gọi là:', 'The process of approximating an analogue signal to a series of discrete levels is referred to as:',
   ['ghép nối (interfacing)', 'lượng tử hoá (quantising)', 'chuyển đổi dữ liệu'], ['interfacing', 'quantising', 'data conversion'], 1,
   'Tooley 3.1: lượng tử hoá.', 'Tooley 3.1: quantising.',
   p('Lượng tử hoá gán mỗi giá trị đã lấy mẫu vào một mức rời rạc rồi mã hoá nhị phân (Hình 3.2: điện áp 9,9 V thành mức 10, mã 1010). "Chuyển đổi dữ liệu" là tên cả quá trình A/D hay D/A, rộng hơn.'),
   p('Quantising assigns each sampled value to a discrete level and then codes it in binary (Figure 3.2: 9.9 V becomes level 10, code 1010). "Data conversion" names the whole A/D or D/A process, which is broader.'))
TQ(8, 'dac', 2, 'Trong DAC trọng số nhị phân, hệ số khuếch đại điện áp của mỗi đầu vào số được quyết định bởi:', 'In a binary-weighted DAC the voltage gain for each digital input is determined by:',
   ['một dốc có độ nghiêng thay đổi', 'một điện áp chuẩn thay đổi', 'các điện trở có giá trị khác nhau'], ['a variable slope ramp', 'a variable reference voltage', 'resistors having different values'], 2,
   'Gain $=-R_f/R_i$ với $R_i=R,2R,4R,8R$ (Bảng 3.1).', 'Gain $=-R_f/R_i$ with $R_i=R,2R,4R,8R$ (Table 3.1).',
   p('Bảng 3.1: bit 3 (MSB) có hệ số $-R/R=-1$, bit 2 là $-0{,}5$, bit 1 là $-0{,}25$, bit 0 (LSB) là $-0{,}125$. Điện trở đầu vào càng lớn thì hệ số càng nhỏ và trọng số càng thấp.'),
   p('Table 3.1: bit 3 (MSB) has gain $-R/R=-1$, bit 2 is $-0.5$, bit 1 is $-0.25$, bit 0 (LSB) is $-0.125$. The larger the input resistor, the smaller the gain and the lower the weight.'))
TQ(9, 'specs', 1, 'Độ phân giải của DAC được nêu bằng:', 'The resolution of a DAC is stated in terms of:',
   ['độ chính xác của điện áp chuẩn', 'độ lợi vòng hở của bộ so sánh', 'số bit dùng trong chuyển đổi'], ['the accuracy of the voltage reference', 'the open-loop gain of the comparator', 'the number of bits used in the conversion'], 2,
   'Tooley 3.2.1, Key Point.', 'Tooley 3.2.1, Key Point.',
   p('Độ chính xác (accuracy) phụ thuộc điện trở và điện áp chuẩn; độ phân giải (resolution) chỉ phụ thuộc số bit. Hai khái niệm này hay bị nhầm. DAC thường có 8, 10 hoặc 12 bit; độ chính xác điển hình 1 % đến 2 %.'),
   p('Accuracy depends on the resistors and the reference voltage; resolution depends only on the number of bits. The two are often confused. Typical DACs have 8, 10 or 12 bits; typical accuracy is 1 % to 2 %.'))
TQ(10, 'adc', 1, 'Thời gian chuyển đổi điển hình của ADC flash nằm trong khoảng:', 'The conversion time of a flash ADC is typically in the range:',
   ['50 ns đến 1 µs', '50 µs đến 1 ms', '50 ms đến 1 s'], ['50 ns to 1 µs', '50 µs to 1 ms', '50 ms to 1 s'], 0,
   'Tooley 3.3: 50 ns đến 1 µs.', 'Tooley 3.3: 50 ns to 1 µs.',
   p('Lớp quét OCR của Tooley in nhầm "1 ps"; ảnh trang và khoá (a) cho thấy đơn vị là micro giây. Flash dùng cho tín hiệu thay đổi nhanh, giá cao vì phức tạp.'),
   p('Tooley\'s OCR layer misprints "1 ps"; the page image and key (a) show the unit is the microsecond. Flash serves rapidly changing signals and costs more because of its complexity.'))
TQ(11, 'adc', 2, 'DAC dùng trong ADC xấp xỉ liên tiếp thường là kiểu:', 'The DAC used in a successive approximation ADC is usually:',
   ['kiểu dốc', 'kiểu trọng số nhị phân', 'kiểu xấp xỉ liên tiếp'], ['ramp type', 'binary-weighted type', 'successive approximation type'], 1,
   'Khoá (b). Văn bản Tooley nói "thường dựa trên thang R-2R", là một mạng trọng số nhị phân.', 'Key (b). The Tooley text says "usually based on an R-2R ladder", which is a binary-weighted network.',
   p('Có một khác biệt nhỏ trong nguồn: Tooley 3.3 mô tả DAC của SAR "thường dựa trên thang R-2R", còn khoá chọn "trọng số nhị phân". Thang R-2R cho các dòng theo trọng số nhị phân nên (b) là đáp án gần nhất; hai phương án còn lại không phải loại DAC (ramp và xấp xỉ liên tiếp là kiểu ADC).'),
   p('A small mismatch in the source: Tooley 3.3 describes the SAR\'s DAC as "usually based on an R-2R ladder", while the key chooses "binary-weighted". The R-2R ladder produces binary-weighted currents so (b) is the closest answer; the other two are not DAC types (ramp and successive approximation are ADC types).'))
TQ(12, 'adc', 1, 'Ở ADC xấp xỉ liên tiếp, khoảng thời gian giữa tín hiệu SC và EOC là:', 'In a successive approximation ADC, the time interval between the SC and EOC signals is:',
   ['thời gian xung nhịp', 'thời gian chu kỳ', 'thời gian chuyển đổi'], ['the clock time', 'the cycle time', 'the conversion time'], 2,
   'SC = bắt đầu chuyển đổi, EOC = kết thúc chuyển đổi.', 'SC = start conversion, EOC = end of conversion.',
   p('Khi nhận SC, các bit của SAR lần lượt được đặt và xoá theo ngõ ra bộ so sánh. Khi xong, EOC phát ra và mã 8 bit được đọc. Thời gian giữa hai tín hiệu là thời gian chuyển đổi, điển hình 10 µs đến 100 µs.'),
   p('On SC the SAR bits are set and cleared in turn according to the comparator output. When done, EOC is issued and the 8-bit code is read. The time between the two signals is the conversion time, typically 10 µs to 100 µs.'))
TQ(13, 'adc', 1, 'Ưu điểm của ADC hai dốc (dual-ramp) là:', 'An advantage of a dual-ramp ADC is:',
   ['thời gian chuyển đổi nhanh', 'khả năng vốn có là loại bỏ nhiễu', 'hoạt động không cần xung nhịp'], ['a fast conversion time', 'an inherent ability to reject noise', 'the ability to operate without the need for a clock'], 1,
   'Dốc xuống có độ nghiêng cố định nên độ chính xác cao và loại nhiễu; đổi lại chậm.', 'The negative ramp has a fixed slope so accuracy is high and noise is rejected; the price is speed.',
   p('Trong ADC hai dốc, độ nghiêng dốc lên phụ thuộc điện áp vào nhưng dốc xuống cố định (Tooley 3.3), nên độ chính xác cao và nhiễu cùng hiện tượng ngẫu nhiên trên đầu vào bị triệt. Nhược điểm là chậm, 500 µs đến 20 ms. Floyd: dùng nhiều trong vôn kế số.'),
   p('In a dual-ramp ADC the slope of the rising ramp depends on the input but the falling ramp is fixed (Tooley 3.3), so accuracy is high and noise and random variation on the input are rejected. The drawback is speed, 500 µs to 20 ms. Floyd: widely used in digital voltmeters.'))
print('Tooley:', sum(1 for i in items if 'Tooley' in i['src']['en']))

# ---------------- B. Floyd Ch.12: dung/sai, Self-Test, Checkup (dap an in tr.737-738) ----------------
def FQ(src_vi, src_en, tid, lv, kind, qv, qe, ov, oe, c, xv, xe, dv='', de=''):
    Q(items, tid, lv, 'goc', kind, qv, qe, ov, oe, c, xv, xe, src_vi, src_en, dv, de)
def tf(n, tid, qv, qe, val, xv, xe, dv='', de=''):
    FQ(f'Floyd Ch.12 · True/False #{n} (đáp án tr.738)', f'Floyd Ch.12 · True/False #{n} (answer p.738)', tid, 1, 'tf', qv, qe, TF[0], TF[1], 0 if val else 1, xv, xe, dv, de)
tf(1, 'sampling', 'Một tín hiệu tương tự có thể được chuyển thành tín hiệu số bằng cách lấy mẫu.', 'An analog signal can be converted to a digital signal using sampling.', True,
   'Đúng: lấy mẫu là bước đầu của chuyển đổi A/D.', 'True: sampling is the first step of A/D conversion.',
   p('Lấy mẫu rồi giữ rồi lượng tử hoá: ba việc nối tiếp. Chỉ lấy mẫu chưa cho mã số, nhưng là điều kiện cần của chuyển đổi (Floyd 12-1).'), p('Sample, then hold, then quantise: three steps in sequence. Sampling alone does not give a code, but it is required for the conversion (Floyd 12-1).'))
tf(2, 'adc', 'ADC là một "thành phần dữ liệu tương tự" (analog data component).', 'An ADC is an analog data component.', False,
   'Sai: ADC là bộ chuyển đổi tương tự sang số.', 'False: an ADC is an analog-to-digital converter.')
tf(3, 'sampling', 'Hiện tượng chồng phổ (aliasing) là yếu tố mong muốn khi lấy mẫu.', 'Aliasing is a desired factor in sampling.', False,
   'Sai: aliasing là méo không mong muốn, được loại bằng bộ lọc thông thấp chống chồng phổ.', 'False: aliasing is unwanted distortion, removed by a low-pass anti-aliasing filter.')
tf(4, 'sampling', 'Với cùng một tín hiệu tương tự, tần số lấy mẫu cao hơn cho kết quả chính xác hơn.', 'A higher sampling rate is more accurate than a lower sampling rate for a given analog signal.', True,
   'Đúng: càng nhiều mẫu thì dạng sóng càng được xác định chính xác.', 'True: the more samples, the more accurately the waveform is defined.')
tf(6, 'adc', '"Successful approximation" (xấp xỉ thành công) là một phương pháp chuyển đổi A/D.', 'Successful approximation is an analog-to-digital conversion method.', False,
   'Sai theo khoá của Floyd: tên đúng là successive approximation (xấp xỉ liên tiếp); đề in "Successful".', 'False in Floyd\'s key: the correct name is successive approximation; the item prints "Successful".',
   p('Câu này là một lỗi chữ trong sách: đề in "Successful" thay vì "Successive". Khoá in là F, nghĩa là phương pháp tên "successful approximation" không tồn tại. Phương pháp thật là xấp xỉ liên tiếp (successive approximation), có trong Floyd 12-2.'),
   p('A typo in the book: the item prints "Successful" instead of "Successive". The printed key is F, meaning a method called "successful approximation" does not exist. The real method is successive approximation, in Floyd 12-2.'))
tf(7, 'adc', 'Điều chế delta dựa trên hiệu của hai mẫu liên tiếp.', 'Delta modulation is based on the difference of two successive samples.', True,
   'Đúng (sigma-delta, Floyd 12-2): lượng tử hoá độ chênh, 1 bit.', 'True (sigma-delta, Floyd 12-2): the difference is quantised, 1 bit.')
tf(8, 'dac', 'Hai loại DAC là DAC đầu vào trọng số nhị phân và DAC thang R/2R.', 'Two types of DAC are the binary-weighted input and the R/2R ladder.', True,
   'Đúng (Floyd 12-3, tóm tắt chương).', 'True (Floyd 12-3, chapter summary).')
tf(9, 'sampling', 'Quá trình chuyển một giá trị tương tự thành mã gọi là lượng tử hoá.', 'The process of converting an analog value to a code is called quantization.', True,
   'Đúng (Floyd 12-1).', 'True (Floyd 12-1).')
tf(10, 'adc', 'ADC flash khác với ADC đồng thời (simultaneous).', 'A flash ADC differs from a simultaneous ADC.', False,
   'Sai: flash và simultaneous là hai tên của cùng một kiểu.', 'False: flash and simultaneous are two names for the same type.')
ST = lambda n: (f'Floyd Ch.12 · Self-Test #{n} (đáp án tr.738)', f'Floyd Ch.12 · Self-Test #{n} (answer p.738)')
def sq(n, tid, lv, qv, qe, ov, oe, c, xv, xe, dv='', de=''):
    sv, se = ST(n); Q(items, tid, lv, 'goc', 'mcq', qv, qe, ov, oe, c, xv, xe, sv, se, dv, de)
sq(1, 'adc', 1, 'Loại nào sau đây KHÔNG phải là một kiểu ADC?', 'Which of the following is not a type of ADC?', ['ADC flash', 'ADC hai dốc', 'ADC xấp xỉ "lùi" (recessive)', 'ADC sigma-delta'], ['Flash ADC', 'Dual slope ADC', 'Recessive approximation ADC', 'sigma-delta ADC'], 2,
   'Có xấp xỉ liên tiếp (successive), không có "recessive".', 'There is successive approximation, not "recessive".')
sq(2, 'adc', 1, 'DAC là viết tắt của:', 'A DAC is a:', ['máy tính tương tự sang số', 'máy tính phân tích số', 'bộ chuyển đổi tích luỹ dữ liệu', 'bộ chuyển đổi số sang tương tự'], ['digital-to-analog computer', 'digital analysis calculator', 'data accumulation converter', 'digital-to-analog converter'], 3,
   'DAC = digital-to-analog converter.', 'DAC = digital-to-analog converter.')
sq(3, 'sampling', 1, 'Hiện tượng chồng phổ (aliasing) là kết quả của:', 'Aliasing results in:', ['lấy mẫu quá mức', 'lấy mẫu dưới mức (undersampling)', 'tạo dải bảo vệ', 'lấy mẫu hoàn hảo'], ['oversampling', 'undersampling', 'guard-band formation', 'perfect sampling'], 1,
   'Alias xuất hiện khi tần số lấy mẫu thấp hơn hai lần tần số tín hiệu.', 'An alias appears when the sampling frequency is below twice the signal frequency.')
sq(4, 'sampling', 1, 'Theo định lý lấy mẫu, tần số lấy mẫu nên:', 'According to the sampling theorem, the sampling frequency should be:', ['nhỏ hơn một nửa tần số tín hiệu cao nhất', 'lớn hơn hai lần tần số tín hiệu cao nhất', 'nhỏ hơn một nửa tần số tín hiệu thấp nhất', 'lớn hơn tần số tín hiệu thấp nhất'], ['less than half the highest signal frequency', 'greater than twice the highest signal frequency', 'less than half the lowest signal frequency', 'greater than the lowest signal frequency'], 1,
   '$f_{sample}\\geq 2f_{a(max)}$; trong thực tế nên lớn hơn.', '$f_{sample}\\geq 2f_{a(max)}$; in practice it should be greater.',
   p('Floyd Phương trình 12-1: tần số lấy mẫu ít nhất bằng hai lần thành phần tần số cao nhất của tín hiệu tương tự, gọi là tần số Nyquist. Lớp chữ của PDF làm mất dấu $\\geq$; ảnh trang xác nhận. Thực tế nên chọn lớn hơn 2 lần.'),
   p('Floyd Equation 12-1: the sampling frequency must be at least twice the highest frequency component of the analog signal, the Nyquist frequency. The PDF text layer lost the $\\geq$ sign; the page image confirms it. In practice choose more than twice.'))
sq(5, 'opamp', 1, 'Op-amp là một bộ khuếch đại tuyến tính có:', 'An op-amp is a linear amplifier which has:', ['một ngõ vào, một ngõ ra', 'một ngõ vào, hai ngõ ra', 'hai ngõ vào, một ngõ ra', 'hai ngõ vào, hai ngõ ra'], ['one input and one output', 'one input and two outputs', 'two inputs and one output', 'two inputs and two outputs'], 2,
   'Hai ngõ vào (đảo, không đảo), một ngõ ra.', 'Two inputs (inverting, non-inverting), one output.')
sq(6, 'sampling', 2, 'Quá trình lượng tử hoá:', 'The quantization process:', ['đổi ngõ ra mạch lấy mẫu-giữ thành mã nhị phân', 'đổi một xung lấy mẫu thành một mức', 'đổi chuỗi mã nhị phân thành tín hiệu tương tự dựng lại', 'lọc bỏ tần số không mong muốn trước khi lấy mẫu'], ['converts the sample-and-hold output to binary code', 'converts a sample impulse to a level', 'converts a sequence of binary codes to a reconstructed analog signal', 'filters out unwanted frequencies before sampling takes place'], 0,
   'Phương án 3 là việc của DAC, phương án 4 là việc của bộ lọc chống chồng phổ.', 'Option 3 is the DAC\'s job, option 4 is the anti-aliasing filter\'s job.')
sq(7, 'sampling', 2, 'Nói chung, tín hiệu tương tự được dựng lại chính xác hơn khi có:', 'Generally, an analog signal can be reconstructed more accurately with:', ['nhiều mức lượng tử hơn', 'ít mức lượng tử hơn', 'tần số lấy mẫu cao hơn', 'tần số lấy mẫu thấp hơn', 'phương án (a) hoặc (c)'], ['more quantization levels', 'fewer quantization levels', 'a higher sampling frequency', 'a lower sampling frequency', 'either answer (a) or (c)'], 4,
   'Cả nhiều mức hơn lẫn lấy mẫu nhanh hơn đều cải thiện.', 'Both more levels and faster sampling improve it.')
sq(8, 'adc', 1, 'Thông lượng (throughput) của ADC flash được đo bằng:', 'The throughput of a flash ADC is measured in:', ['độ dời trên giây', 'quãng đường trên giây', 'mẫu trên phút', 'mẫu trên giây'], ['displacement per second', 'distance per second', 'samples per minute', 'samples per second'], 3,
   'Đơn vị: sps (samples per second).', 'Unit: sps (samples per second).')
sq(9, 'adc', 1, 'Vôn kế số dùng:', 'A digital voltmeter uses a:', ['ADC flash', 'ADC xấp xỉ liên tiếp', 'ADC sigma-delta', 'ADC hai dốc'], ['flash ADC', 'successive approximation ADC', 'sigma-delta ADC', 'dual-slope ADC'], 3,
   'Hai dốc: chính xác, chống nhiễu, chậm; hợp đo lường.', 'Dual slope: accurate, noise-rejecting, slow; suits measurement.')
sq(10, 'adc', 1, 'ADC phổ biến nhất trong viễn thông cho tín hiệu âm thanh là:', 'The most common ADC seen in telecommunications based on audio signals is:', ['ADC flash', 'ADC xấp xỉ liên tiếp', 'ADC sigma-delta', 'ADC hai dốc'], ['flash ADC', 'successive approximation ADC', 'sigma-delta ADC', 'dual-slope ADC'], 2,
   'Sigma-delta (Floyd 12-2).', 'Sigma-delta (Floyd 12-2).')
sq(11, 'dac', 2, 'Trong DAC trọng số nhị phân, điện trở có giá trị nhỏ nhất ứng với:', 'In a binary weighted DAC, the lowest-value resistor corresponds to:', ['đầu vào có trọng số nhị phân cao nhất', 'đầu vào có trọng số nhị phân thấp nhất', 'đầu vào thứ nhất', 'đầu vào cuối cùng'], ['the highest binary weighted input', 'the lowest binary weighted input', 'the first input', 'the last input'], 0,
   'Điện trở R ứng với $2^3$ (MSB); 2R, 4R, 8R ứng với các bit thấp hơn.', 'Resistor R matches $2^3$ (MSB); 2R, 4R, 8R match the lower bits.')
CK = lambda a, n: (f'Floyd Ch.12 · Section {a} Checkup #{n} (đáp án tr.737)', f'Floyd Ch.12 · Section {a} Checkup #{n} (answer p.737)')
def ck(a, n, tid, lv, qv, qe, ov, oe, c, xv, xe, dv='', de=''):
    sv, se = CK(a, n); Q(items, tid, lv, 'goc', 'mcq', qv, qe, ov, oe, c, xv, xe, sv, se, dv, de)
ck('12-1', 3, 'sampling', 2, 'Thành phần cao nhất của một tín hiệu tương tự là 20 kHz. Tần số lấy mẫu tối thiểu là:', 'The highest frequency component in an analog signal is 20 kHz. The minimum sampling frequency is:', ['40 kHz', '20 kHz', '10 kHz', '80 kHz'], ['40 kHz', '20 kHz', '10 kHz', '80 kHz'], 0,
   '$f_s\\geq 2\\times20=40$ kHz.', '$f_s\\geq 2\\times20=40$ kHz.')
ck('12-2', 2, 'adc', 1, 'Phương pháp chuyển đổi A/D nào tạo ra luồng dữ liệu một bit?', 'Which analog-to-digital conversion method produces a single-bit data stream?', ['flash', 'hai dốc', 'xấp xỉ liên tiếp', 'sigma-delta'], ['flash', 'dual-slope', 'successive-approximation', 'sigma-delta'], 3,
   'Sigma-delta (điều chế delta, 1 bit); số bit 1 trong một khoảng cho biết biên độ.', 'Sigma-delta (delta modulation, 1 bit); the count of 1s over an interval gives the amplitude.')
ck('12-2', 4, 'specs', 1, 'Ba loại lỗi ngõ ra của ADC được Floyd nêu là:', 'The ADC output errors named by Floyd are:', ['mã bị thiếu, mã sai và độ lệch (offset)', 'mã dư, mã trễ và nhiễu', 'méo, trễ và chồng phổ', 'độ lợi cao, độ lợi thấp và đơn điệu'], ['missing code, incorrect code and offset', 'extra code, late code and noise', 'distortion, delay and aliasing', 'high gain, low gain and monotonic'], 0,
   'Floyd Hình 12-24 và Checkup 12-2 câu 4.', 'Floyd Figure 12-24 and Checkup 12-2 question 4.')
ck('12-3', 3, 'specs', 1, 'Trong thử nghiệm DAC, các bước đi ngược (step reversal) cho biết:', 'In a DAC test, a step reversal indicates:', ['hoạt động không đơn điệu (nonmonotonic)', 'độ lợi thấp', 'độ lệch ngõ ra', 'tần số lấy mẫu thấp'], ['nonmonotonic behavior', 'low gain', 'output offset', 'a low sampling frequency'], 0,
   'Đơn điệu nghĩa là không có bước lùi khi quét toàn bộ dải mã.', 'Monotonic means no reverse steps over the whole code range.')
ck('12-3', 4, 'specs', 2, 'Khi DAC có độ lợi thấp, biên độ các bước:', 'With low gain in a DAC, the step amplitudes are:', ['nhỏ hơn lý tưởng', 'lớn hơn lý tưởng', 'bằng lý tưởng nhưng lệch gốc', 'đảo chiều'], ['less than ideal', 'greater than ideal', 'ideal but shifted', 'reversed'], 0,
   'Độ lợi thấp: mọi bước nhỏ hơn; độ lợi cao: mọi bước lớn hơn.', 'Low gain: all steps smaller; high gain: all steps larger.')
print('Floyd+Tooley goc:', len(items))

# ---------------- C. Cau sinh theo dang (bo_sung): dap an tinh bang adda.py ----------------
rng = random.Random(10101)
GS = lambda f: (f'Bổ sung · sinh theo dạng: {f[0]}', f'Added · generated pattern: {f[1]}')
def G(tid, lv, qv, qe, ov, oe, c, xv, xe, fam, dv='', de=''):
    sv, se = GS(fam); Q(gen, tid, lv, 'bo_sung', 'mcq', qv, qe, ov, oe, c, xv, xe, sv, se, dv, de)
def fmt(x, d=3):
    s = f'{x:.{d}f}'.rstrip('0').rstrip('.') if '.' in f'{x:.{d}f}' else f'{x:.{d}f}'
    return s
def shuffle_with(correct, wrongs):
    """tra ve (opts, c) voi dap an dung o vi tri co dinh theo rng (kich thuoc 4)."""
    ws = [w for w in dict.fromkeys(wrongs) if w != correct]
    assert len(ws) >= 3, ('distractor trung dap an', correct, wrongs)
    opts = [correct] + ws[:3]; rng.shuffle(opts); return opts, opts.index(correct)

# G1: do phan giai % cua DAC n bit
for n in (4, 6, 8, 10, 12, 16):
    r = A.resolution_pct(n); cor = f'{r:.3g} %'
    wr = [f'{100 / 2 ** n:.3g} %', f'{100 / n:.3g} %', f'{100 / 2 ** (n - 1):.3g} %', f'{100 / n ** 2:.3g} %', f'{100 / (2 * n):.3g} %']
    opts, c = shuffle_with(cor, wr)
    G('specs', 1 if n <= 8 else 2, f'Độ phân giải của DAC {n} bit, tính theo phần trăm (một phần của $2^n-1$ bước), là:', f'The resolution of an {n}-bit DAC as a percentage (one part in $2^n-1$ steps) is:',
      opts, opts, c, f'$100/(2^{{{n}}}-1)=100/{2 ** n - 1}={r:.3g}\\%$.', f'$100/(2^{{{n}}}-1)=100/{2 ** n - 1}={r:.3g}\\%$.', ('độ phân giải DAC', 'DAC resolution'))
# G2: so bo so sanh cua ADC flash
for n in (3, 5, 6, 8, 10):
    cor = str(A.comparators(n)); opts, c = shuffle_with(cor, [str(2 ** n), str(n), str(2 ** (n - 1))])
    G('adc', 1 if n <= 4 else 2, f'ADC flash {n} bit cần bao nhiêu bộ so sánh?', f'How many comparators does a {n}-bit flash ADC need?', opts, opts, c,
      f'$2^{n}-1={A.comparators(n)}$ (không cần bộ so sánh cho trường hợp toàn 0).', f'$2^{n}-1={A.comparators(n)}$ (no comparator is needed for the all-zeros case).', ('số bộ so sánh flash', 'flash comparator count'))
# G3: tan so lay mau toi thieu
for f in (3, 15, 20, 4, 8):
    cor = f'{2 * f} kHz'; opts, c = shuffle_with(cor, [f'{f} kHz', f'{f / 2:g} kHz', f'{4 * f} kHz'])
    G('sampling', 1, f'Thành phần tần số cao nhất của một tín hiệu là {f} kHz. Tần số lấy mẫu tối thiểu theo định lý lấy mẫu là:', f'The highest frequency component of a signal is {f} kHz. The minimum sampling frequency by the sampling theorem is:', opts, opts, c,
      f'$f_s\\geq2f_{{a(max)}}=2\\times{f}={2 * f}$ kHz.', f'$f_s\\geq2f_{{a(max)}}=2\\times{f}={2 * f}$ kHz.', ('Nyquist', 'Nyquist'))
# G4: DAC trong so nhi phan Tooley (Hinh 3.6a, muc logic 5 V)
for code in (0b0110, 0b1001, 0b0011, 0b1100, 0b0101, 0b1011):
    v = A.dac_weighted_closed(code); cor = f'{v:.3f} V'.replace('.000', '')
    wr = [f'{-v:.3f} V', f'{A.dac_weighted_closed(code ^ 0b1111):.3f} V', f'{v / 2:.3f} V']
    opts, c = shuffle_with(cor, [w.replace('.000', '') for w in wr])
    b = format(code, '04b')
    G('dac', 2, f'DAC trọng số nhị phân 4 bit của Tooley (Hình 3.6a, mức logic 1 là +5 V, bộ khuếch đại đảo) nhận mã {b}. Điện áp ra là:', f'The 4-bit binary-weighted DAC of Tooley (Figure 3.6a, logic 1 = +5 V, inverting amplifier) receives code {b}. The output voltage is:', opts, opts, c,
      f'$V_{{out}}=-5\\,(b_3\\cdot1+b_2\\cdot0{{,}}5+b_1\\cdot0{{,}}25+b_0\\cdot0{{,}}125)={v:.3f}$ V; cũng là $-0{{,}}625\\times{code}$.', f'$V_{{out}}=-5\\,(b_3\\cdot1+b_2\\cdot0.5+b_1\\cdot0.25+b_0\\cdot0.125)={v:.3f}$ V; also $-0.625\\times{code}$.', ('DAC trọng số nhị phân', 'binary-weighted DAC'))
# G5: DAC thang R-2R (Floyd), Rf = 2R, Vref = 5 V
for code in (0b1010, 0b0111, 0b1110, 0b0011, 0b1001):
    v = A.dac_r2r_closed(code); cor = f'{v:.4g} V'
    opts, c = shuffle_with(cor, [f'{-v / 2:.4g} V', f'{v * 2:.4g} V', f'{-v:.4g} V'])
    b = format(code, '04b')
    G('dac', 3, f'DAC thang R/2R 4 bit của Floyd (mức cao +5 V, $R_f=2R$) nhận mã {b}. Điện áp ra là:', f'Floyd\'s 4-bit R/2R ladder DAC (high level +5 V, $R_f=2R$) receives code {b}. The output voltage is:', opts, opts, c,
      f'Cộng các thành phần: $-5(b_3+b_2/2+b_1/4+b_0/8)={v:.4g}$ V (1000 cho −5 V, 0100 cho −2,5 V, 0010 cho −1,25 V, 0001 cho −0,625 V).', f'Sum the contributions: $-5(b_3+b_2/2+b_1/4+b_0/8)={v:.4g}$ V (1000 gives −5 V, 0100 gives −2.5 V, 0010 gives −1.25 V, 0001 gives −0.625 V).', ('DAC R-2R', 'R-2R DAC'))
# G6: ADC xap xi lien tiep 4 bit, trong so 8,4,2,1 V (Floyd Hinh 12-17, 12-18)
for vin in (5.1, 11.7, 3.4, 9.2, 13.8, 6.6):
    code, steps = A.sar_trace(vin); cor = format(code, '04b'); alt = [format(min(15, code + 1), '04b'), format(max(0, code - 1), '04b'), format(15 - code, '04b')]
    alt = [a for a in dict.fromkeys(alt) if a != cor][:3]
    while len(alt) < 3: alt.append(format(rng.randrange(16), '04b')) if format(rng.randrange(16), '04b') not in alt + [cor] else None
    opts, c = shuffle_with(cor, alt)
    tr = ', '.join(f'{d:g} V {"giữ" if k else "bỏ"}' for _, _, d, k in steps); tre = ', '.join(f'{d:g} V {"kept" if k else "reset"}' for _, _, d, k in steps)
    G('adc', 3, f'ADC xấp xỉ liên tiếp 4 bit có DAC với các bit nặng 8 V, 4 V, 2 V, 1 V. Điện áp vào không đổi {vin:g} V. Mã nhị phân cuối cùng trong SAR là:', f'A 4-bit successive-approximation ADC has a DAC with bit weights of 8 V, 4 V, 2 V and 1 V. The constant input is {vin:g} V. The final binary code in the SAR is:', opts, opts, c,
      f'Thử lần lượt từ MSB: {tr}. Mã {cor}.', f'Try each bit from the MSB: {tre}. Code {cor}.', ('SAR', 'SAR'))
# G7: flash 3 bit (Tooley Hinh 3.9, nguong 0,5 V ... 6,5 V)
for vin in (2.0, 4.7, 0.3, 6.9, 3.2, 5.9):
    code = A.flash_closed(vin); hi, outs = A.flash_comparators(vin)
    assert hi == code, (vin, hi, code)
    cor = format(code, '03b'); alt = [a for a in dict.fromkeys([format(min(7, code + 1), '03b'), format(max(0, code - 1), '03b'), format(7 - code, '03b'), format((code + 2) % 8, '03b')]) if a != cor][:3]
    opts, c = shuffle_with(cor, alt)
    G('adc', 2, f'ADC flash 3 bit của Tooley (Hình 3.9: ngưỡng 0,5 V; 1,5 V; ...; 6,5 V) nhận điện áp vào {vin:g} V. Mã ra (Bit 2, Bit 1, Bit 0) là:', f'Tooley\'s 3-bit flash ADC (Figure 3.9: thresholds 0.5 V, 1.5 V, ..., 6.5 V) receives {vin:g} V. The output code (Bit 2, Bit 1, Bit 0) is:', opts, opts, c,
      f'{hi} bộ so sánh đầu có ngõ ra 1 (ngưỡng thấp hơn {vin:g} V); bộ mã hoá ưu tiên cho mã {cor}.', f'The first {hi} comparators output 1 (thresholds below {vin:g} V); the priority encoder gives {cor}.', ('ADC flash', 'flash ADC'))
# G8: khuech dai dao
for rf, ri in ((220, 1), (33, 1), (100, 4), (47, 2)):
    g = -rf / ri; cor = fmt(g, 2); opts, c = shuffle_with(cor, [fmt(rf / ri, 2), fmt(-ri / rf, 3), fmt(-(rf + ri) / ri, 2)])
    G('opamp', 1, f'Bộ khuếch đại đảo dùng op-amp có $R_f={rf}$ kΩ và $R_i={ri}$ kΩ. Độ lợi vòng kín $V_{{out}}/V_{{in}}$ là:', f'An inverting op-amp amplifier has $R_f={rf}$ kΩ and $R_i={ri}$ kΩ. The closed-loop gain $V_{{out}}/V_{{in}}$ is:', opts, opts, c,
      f'$V_{{out}}/V_{{in}}=-R_f/R_i=-{rf}/{ri}={cor}$ (dấu trừ là đảo pha).', f'$V_{{out}}/V_{{in}}=-R_f/R_i=-{rf}/{ri}={cor}$ (the minus sign is the inversion).', ('op-amp đảo', 'inverting op-amp'))
# G9: sai so toi da cua DAC
for fs, acc in ((10, 0.1), (5, 0.2), (12, 0.5), (8, 1.0)):
    err = fs * acc / 100 * 1000; cor = f'{err:g} mV'; opts, c = shuffle_with(cor, [f'{err / 10:g} mV', f'{err * 10:g} mV', f'{fs * acc:g} mV', f'{err * 2:g} mV', f'{err / 2:g} mV'])
    G('specs', 2, f'DAC có điện áp ra toàn thang {fs} V và độ chính xác ±{acc:g} % của toàn thang. Sai số lớn nhất của một điện áp ra bất kỳ là:', f'A DAC has a full-scale output of {fs} V and an accuracy of ±{acc:g} % of full scale. The maximum error of any output voltage is:', opts, opts, c,
      f'${fs}\\times{acc / 100:g}={err / 1000:g}$ V $={err:g}$ mV.', f'${fs}\\times{acc / 100:g}={err / 1000:g}$ V $={err:g}$ mV.', ('độ chính xác DAC', 'DAC accuracy'))
# G10: alias (muc 3, dung dinh nghia lay mau)
for f, fs in ((5, 8), (7, 10), (9, 12)):
    al = abs(f - fs); cor = f'{al} kHz'; opts, c = shuffle_with(cor, [f'{f} kHz', f'{fs} kHz', f'{f + fs} kHz'])
    G('sampling', 3, f'Một tín hiệu hình sin {f} kHz được lấy mẫu ở {fs} kHz mà không có bộ lọc chống chồng phổ. Sau khi dựng lại, tần số alias xuất hiện là:', f'A {f} kHz sine wave is sampled at {fs} kHz with no anti-aliasing filter. After reconstruction the alias frequency that appears is:', opts, opts, c,
      f'Vì $f>f_s/2$, tần số bị gập về $|f_s-f|=|{fs}-{f}|={al}$ kHz, nằm trong băng $0$ đến $f_s/2={fs / 2:g}$ kHz.', f'Because $f>f_s/2$, the frequency folds to $|f_s-f|=|{fs}-{f}|={al}$ kHz, inside the band $0$ to $f_s/2={fs / 2:g}$ kHz.', ('chồng phổ', 'aliasing'),
      p('Floyd 12-1 chỉ mô tả alias bằng phổ (Hình 12-3) và không cho công thức gập; kết quả $|f_s-f|$ ở đây là phép tính theo định nghĩa lấy mẫu của một sóng sin.'), p('Floyd 12-1 describes aliasing through the spectrum (Figure 12-3) and gives no folding formula; the result $|f_s-f|$ here is the standard computation for a sine wave.'))
# G11: DAC voi dien tro dau vao (Floyd Vi du 12-2): Rf = 10 kOhm, R = 25k,50k,100k,200k, muc cao 5 V
for code in (0b1010, 0b0110, 0b1111, 0b0001, 0b1100):
    rs = [25, 50, 100, 200]; v = -sum(5 * 10 / rs[k] for k in range(4) if (code >> (3 - k)) & 1)
    cor = f'{v:.4g} V'; opts, c = shuffle_with(cor, [f'{-v:.4g} V', f'{v / 2:.4g} V', f'{v * 2:.4g} V'])
    G('dac', 3, f'DAC trọng số 4 bit của Floyd (Hình 12-27: $R$ đầu vào 25 kΩ, 50 kΩ, 100 kΩ, 200 kΩ cho D3 đến D0; $R_f=10$ kΩ; mức cao +5 V) nhận mã {format(code, "04b")}. Điện áp ra là:', f'Floyd\'s 4-bit weighted DAC (Figure 12-27: input resistors 25 kΩ, 50 kΩ, 100 kΩ, 200 kΩ for D3 to D0; $R_f=10$ kΩ; high level +5 V) receives code {format(code, "04b")}. The output voltage is:', opts, opts, c,
      f'Mỗi bit 1 cho dòng $5/R_i$ qua $R_f$: D3 cho −2 V, D2 −1 V, D1 −0,5 V, D0 −0,25 V; tổng {v:.4g} V (mỗi bước mã là −0,25 V).', f'Each 1 bit gives a current $5/R_i$ through $R_f$: D3 gives −2 V, D2 −1 V, D1 −0.5 V, D0 −0.25 V; total {v:.4g} V (each code step is −0.25 V).', ('DAC trọng số (Floyd)', 'weighted DAC (Floyd)'))
# G12: khai niem
Gc = lambda *a, **k: G(*a, **k)
Gc('sampling', 1, 'Mạch lấy mẫu-giữ (sample-and-hold) giữ mức đã lấy mẫu không đổi cho đến mẫu kế để:', 'The sample-and-hold circuit keeps the sampled level constant until the next sample so that:', ['ADC có thời gian xử lý giá trị đó', 'tần số lấy mẫu tăng gấp đôi', 'tín hiệu không cần lọc nữa', 'DAC không cần điện áp chuẩn'], ['the ADC has time to process that value', 'the sampling frequency doubles', 'the signal needs no filtering', 'the DAC needs no reference voltage'], 0,
   'Floyd 12-1: giữ giá trị để ADC có thời gian chuyển đổi.', 'Floyd 12-1: the value is held so the ADC has time to convert.', ('mạch lấy mẫu-giữ', 'sample-and-hold'))
Gc('sampling', 1, 'Bộ lọc chống chồng phổ đặt TRƯỚC mạch lấy mẫu là bộ lọc:', 'The anti-aliasing filter placed BEFORE the sampling circuit is a:', ['thông thấp', 'thông cao', 'thông dải', 'chắn dải'], ['low-pass filter', 'high-pass filter', 'band-pass filter', 'band-stop filter'], 0,
   'Nó loại các thành phần cao hơn tần số Nyquist.', 'It removes components above the Nyquist frequency.', ('chống chồng phổ', 'anti-aliasing'))
Gc('dac', 1, 'Bộ lọc thông thấp ở ngõ ra của DAC (Tooley 3.2.2) dùng để:', 'The low-pass filter at a DAC output (Tooley 3.2.2) is used to:', ['làm mịn các bậc thang của điện áp ra', 'tăng số bit của DAC', 'đổi tín hiệu ra thành số', 'giảm điện áp chuẩn'], ['smooth the steps of the output voltage', 'increase the number of bits of the DAC', 'turn the output into a digital signal', 'reduce the reference voltage'], 0,
   'Các thành phần tần số lấy mẫu dư (tạo "bậc thang") nằm xa tần số cắt nên bị suy giảm.', 'The residual sampling-frequency components (the "steps") lie well beyond the cut-off and are attenuated.', ('lọc ngõ ra DAC', 'DAC output filter'))
Gc('adc', 2, 'Khi dựng lại tín hiệu thử là đường dốc tuyến tính, ADC flash bị hỏng một bộ so sánh (kẹt ở mức THẤP) cho dạng bậc thang thiếu một bước. Lỗi này là:', 'A flash ADC with one comparator stuck LOW, tested with a linear ramp, gives a staircase missing one step. This error is:', ['mã bị thiếu (missing code)', 'độ lệch (offset)', 'không đơn điệu', 'chồng phổ'], ['a missing code', 'an offset', 'nonmonotonic behavior', 'aliasing'], 0,
   'Floyd Ví dụ 12-4: mã 0011 thiếu, bộ so sánh 3 kẹt LOW.', 'Floyd example: code 0011 is missing, comparator 3 stuck LOW.', ('lỗi ADC', 'ADC faults'))
Gc('adc', 2, 'ADC hai dốc (dual-slope): thời gian xả tụ về 0 V tỉ lệ với điều gì?', 'In a dual-slope ADC the time for the capacitor to discharge to 0 V is proportional to:', ['điện áp vào đã tích vào tụ', 'điện áp chuẩn', 'tần số nguồn', 'số bit của bộ đếm'], ['the input voltage that charged the capacitor', 'the reference voltage', 'the supply frequency', 'the counter size'], 0,
   'Dốc xả có độ nghiêng cố định nên thời gian xả tỉ lệ điện áp ban đầu, tức tỉ lệ $V_{in}$ (Floyd 12-2).', 'The discharge ramp has a fixed slope so the discharge time is proportional to the starting voltage, i.e. to $V_{in}$ (Floyd 12-2).', ('ADC hai dốc', 'dual slope ADC'))
Gc('adc', 2, 'ADC xấp xỉ liên tiếp n bit cần bao nhiêu phép so sánh cho một lần chuyển đổi?', 'How many comparisons does an n-bit successive-approximation ADC make per conversion?', ['n', '$2^n-1$', '$2^n$', '$n^2$'], ['n', '$2^n-1$', '$2^n$', '$n^2$'], 0,
   'Một bit mỗi lần, từ MSB: n bước (ADC0804: 8 phép so sánh, 64 chu kỳ xung nhịp).', 'One bit at a time from the MSB: n steps (ADC0804: eight comparisons, 64 clock periods).', ('SAR', 'SAR'))
Gc('specs', 2, 'Tại sao thang R-2R dễ chế tạo trên IC hơn DAC trọng số nhị phân 8 bit?', 'Why is the R-2R ladder easier to make on an IC than an 8-bit binary-weighted DAC?', ['chỉ cần hai giá trị điện trở và dễ khớp nhau', 'không cần op-amp', 'không cần điện áp chuẩn', 'dùng ít bit hơn'], ['only two resistor values are needed and they match easily', 'it needs no op-amp', 'it needs no reference voltage', 'it uses fewer bits'], 0,
   'DAC trọng số 8 bit cần R đến 128R với sai số dưới 0,5 % (Floyd), dải giá trị rộng khó khớp.', 'An 8-bit weighted DAC needs R to 128R at better than 0.5 % (Floyd), a wide range that is hard to match.', ('R-2R', 'R-2R'))
Gc('sampling', 1, 'Âm thanh CD lấy mẫu ở 44,1 kHz. Tần số âm tối đa được ghi lại xấp xỉ:', 'CD audio is sampled at 44.1 kHz. The highest audio frequency captured is about:', ['22 kHz', '44 kHz', '88 kHz', '11 kHz'], ['22 kHz', '44 kHz', '88 kHz', '11 kHz'], 0,
   'Một nửa tần số lấy mẫu: 22,05 kHz, trên 20 kHz của thiết bị âm thanh thông thường (Floyd 12-1).', 'Half the sampling rate: 22.05 kHz, above the 20 kHz usual for audio equipment (Floyd 12-1).', ('lấy mẫu âm thanh', 'audio sampling'))

# G13: tinh nhieu buoc (muc 3): so bit can thiet, toc do ADC va tan so toi da
for pct in (1.0, 0.5, 0.1, 0.05):
    n = next(k for k in range(1, 33) if A.resolution_pct(k) < pct); cor = f'{n} bit'
    opts, c = shuffle_with(cor, [f'{n - 1} bit', f'{n + 1} bit', f'{n + 2} bit'])
    G('specs', 3, f'Cần DAC có độ phân giải tốt hơn {pct:g} % (một phần của $2^n-1$ bước). Số bit n nhỏ nhất là:', f'A DAC must have a resolution better than {pct:g} % (one part in $2^n-1$ steps). The smallest number of bits n is:', opts, opts, c,
      f'Cần $100/(2^n-1)<{pct:g}$. Với $n={n}$: ${A.resolution_pct(n):.4g}\\%$ (đạt); với $n={n - 1}$: ${A.resolution_pct(n - 1):.4g}\\%$ (không đạt).', f'Need $100/(2^n-1)<{pct:g}$. For $n={n}$: ${A.resolution_pct(n):.4g}\\%$ (passes); for $n={n - 1}$: ${A.resolution_pct(n - 1):.4g}\\%$ (fails).', ('số bit cần thiết', 'bits required'))
for tc in (2.0, 10.0, 100.0, 0.5):                       # thoi gian chuyen doi (us)
    fs = 1e6 / tc; fmax = fs / 2; cor = f'{fmax / 1000:g} kHz'
    opts, c = shuffle_with(cor, [f'{fs / 1000:g} kHz', f'{fs / 500:g} kHz', f'{fmax / 2000:g} kHz', f'{fmax / 100:g} kHz'])
    G('adc', 3, f'ADC cần {tc:g} µs cho mỗi lần chuyển đổi và lấy mẫu liên tục với tốc độ tối đa (thông lượng = 1/thời gian chuyển đổi). Tần số tín hiệu cao nhất có thể số hoá không chồng phổ là:', f'An ADC takes {tc:g} µs per conversion and samples continuously at its maximum rate (throughput = 1/conversion time). The highest signal frequency that can be digitised without aliasing is:', opts, opts, c,
      f'$f_s=1/{tc:g}\\,\\mu s={fs / 1000:g}$ kS/s; $f_{{a(max)}}=f_s/2={fmax / 1000:g}$ kHz.', f'$f_s=1/{tc:g}\\,\\mu s={fs / 1000:g}$ kS/s; $f_{{a(max)}}=f_s/2={fmax / 1000:g}$ kHz.', ('thông lượng và Nyquist', 'throughput and Nyquist'),
      p('Floyd 12-2 định nghĩa thông lượng là tốc độ lấy mẫu mà ADC xử lý được (mẫu trên giây). Giả thiết "lấy mẫu liên tục ở tốc độ tối đa" là điều kiện của câu hỏi, không phải của sách.'), p('Floyd 12-2 defines throughput as the sampling rate an ADC can handle (samples per second). "Samples continuously at its maximum rate" is an assumption of the question, not of the book.'))

# ---------------- D. Tu luan: bai le Floyd co dap an in; bai chan do site giai ----------------
def E(num, qv, qe, solv, sole, src_v, src_e, tid, lv=2, origin='goc'):
    ess.append(dict(kind='ess', q=dict(vi=qv, en=qe), sol=dict(vi=solv, en=sole), topic=dict(vi=TOP[tid][0], en=TOP[tid][1]), topic_id=tid, level=lv, origin=origin, src=dict(vi=src_v, en=src_e)))
E(7, 'Điện áp vào của một mạch khuếch đại đảo dùng op-amp là 5 mV, điện áp ra là 1 V. Độ lợi vòng kín là bao nhiêu?', 'The input voltage to a certain op-amp inverting amplifier is 5 mV, and the output is 1 V. What is the closed-loop voltage gain?',
  'Độ lợi $=V_{out}/V_{in}=1\\,V/5\\,mV=200$. Đáp án in của Floyd là 200 (giá trị tuyệt đối); vì là mạch đảo nên về dấu độ lợi là $-200$ nếu $V_{in}$ và $V_{out}$ lấy theo dấu.', 'Gain $=V_{out}/V_{in}=1\\,V/5\\,mV=200$. Floyd\'s printed answer is 200 (magnitude); for an inverting circuit the signed gain would be $-200$ if $V_{in}$ and $V_{out}$ are taken with sign.',
  'Floyd Ch.12 · Bài 7 (đáp án A-26)', 'Floyd Ch.12 · Problem 7 (answer A-26)', 'opamp')
E(8, 'Cần độ lợi vòng kín 220 cho bộ khuếch đại đảo. Chọn điện trở hồi tiếp bao nhiêu nếu $R_i=2$ kΩ?', 'To achieve a closed-loop voltage gain of 220 with an inverting amplifier, what value of feedback resistor do you use if $R_i=2$ kΩ?',
  '$|A|=R_f/R_i$ nên $R_f=220\\times2$ kΩ $=440$ kΩ. Bài chẵn: sách không in đáp án; site tự giải.', '$|A|=R_f/R_i$ so $R_f=220\\times2$ kΩ $=440$ kΩ. Even-numbered: the book prints no answer; solved by this site.',
  'Floyd Ch.12 · Bài 8 (bài chẵn, không có đáp án in)', 'Floyd Ch.12 · Problem 8 (even, no printed answer)', 'opamp')
E(9, 'Độ lợi của bộ khuếch đại đảo có $R_f=33$ kΩ và $R_i=1$ kΩ là bao nhiêu?', 'What is the gain of an inverting amplifier that uses a 33 k$\\Omega$ feedback resistor if the input resistor is 1 k$\\Omega$?',
  '$A=-R_f/R_i=-33$. Đáp án in: $-33$.', '$A=-R_f/R_i=-33$. Printed answer: $-33$.', 'Floyd Ch.12 · Bài 9 (đáp án A-26)', 'Floyd Ch.12 · Problem 9 (answer A-26)', 'opamp', 1)
E(10, 'Cần bao nhiêu bộ so sánh cho một bộ chuyển đổi flash 4 bit?', 'How many comparators are required to form a 4-bit flash converter?',
  '$2^4-1=15$ (Floyd 12-2). Bài chẵn: sách không in đáp án; site tự giải.', '$2^4-1=15$ (Floyd 12-2). Even-numbered: the book prints no answer; solved by this site.', 'Floyd Ch.12 · Bài 10 (bài chẵn)', 'Floyd Ch.12 · Problem 10 (even)', 'adc', 1)
E(19, 'Xác định độ phân giải (theo phần trăm) của DAC (a) 2 bit (b) 5 bit (c) 12 bit.', 'Determine the resolution, expressed as a percentage, for each of the following DACs: (a) 2-bit (b) 5-bit (c) 12-bit.',
  '$100/(2^n-1)$: (a) $100/3=33{,}33\\%$; (b) $100/31=3{,}226\\%$ (làm tròn 3,23 %); (c) $100/4095=0{,}0244\\%$. Đáp án in của Floyd: 33,33 %, 3,22 %, 0,024 %: ý (b) in 3,22 % (cắt cụt thay vì làm tròn 3,23 %) và ý (c) làm tròn còn 0,024 %.',
  '$100/(2^n-1)$: (a) $100/3=33.33\\%$; (b) $100/31=3.226\\%$ (rounds to 3.23 %); (c) $100/4095=0.0244\\%$. Floyd\'s printed answers: 33.33 %, 3.22 %, 0.024 %: part (b) shows 3.22 % (truncated, not rounded to 3.23 %) and part (c) is rounded to 0.024 %.',
  'Floyd Ch.12 · Bài 19 (đáp án A-26)', 'Floyd Ch.12 · Problem 19 (answer A-26)', 'specs')
E(23, 'Làm thế nào để chuyển một tín hiệu tương tự thành một xấp xỉ dạng bậc thang?', 'How can an analog signal be converted into a stair-step approximation?',
  'Dùng mạch lấy mẫu-giữ (sample-and-hold): lấy mẫu rồi giữ mỗi mẫu không đổi tới mẫu kế (Floyd Hình 12-5). Đáp án in: "By using a sample-and-hold circuit".', 'Use a sample-and-hold circuit: sample, then hold each sample constant until the next (Floyd Figure 12-5). Printed answer: "By using a sample-and-hold circuit".',
  'Floyd Ch.12 · Bài 23 (đáp án A-26)', 'Floyd Ch.12 · Problem 23 (answer A-26)', 'sampling', 1)
E(0, 'Ví dụ 12-4: Xác định độ phân giải (phần trăm) của DAC (a) 8 bit (b) 12 bit. Bài liên quan: DAC 16 bit.', 'Example 12-4: Determine the resolution, expressed as a percentage, of (a) an 8-bit DAC (b) a 12-bit DAC. Related problem: a 16-bit DAC.',
  '(a) $100/255=0{,}392\\%$; (b) $100/4095=0{,}0244\\%$. Bài liên quan 16 bit: $100/65535=0{,}00153\\%$ (đáp án in: 0,00153 %).', '(a) $100/255=0.392\\%$; (b) $100/4095=0.0244\\%$. Related problem, 16 bit: $100/65535=0.00153\\%$ (printed answer: 0.00153 %).',
  'Floyd Ch.12 · Ví dụ 12-4 và bài liên quan (đáp án tr.738)', 'Floyd Ch.12 · Example 12-4 and related problem (answer p.738)', 'specs')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, data in (('m10.json', items), ('m10_gen.json', gen), ('m10_ess.json', ess)):
        json.dump(data, open(os.path.join(OUT, name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    import collections
    allq = items + gen
    print('goc', len(items), '| bo_sung', len(gen), '| tu luan', len(ess), '| muc', dict(collections.Counter(i['level'] for i in allq)), '| chu de', dict(collections.Counter(i['topic_id'] for i in allq)))
