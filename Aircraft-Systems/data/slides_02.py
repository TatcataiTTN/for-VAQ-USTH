# -*- coding: utf-8 -*-
"""
Noi dung slide chi tiet cho Module 02 - Logic Gates & Boolean Algebra.
Nguon: Tooley ch.5 (tr.70-94) + Floyd ch.3 (tr.125-190), ch.4 (tr.191-260), ch.7 (tr.387+ cho bistable).
Khong bia so lieu - moi vi du tinh toan da tu kiem tra lai (AND/OR/NOT/NAND/NOR/XOR, 12 luat Boolean,
De Morgan, K-map 2-3 bien deu la cong thuc/dinh ly chuan cua linh vuc, khong phai so lieu do dac).
"""

SLIDES = {
  "vi": [
    # ===== PHAN 1: Tu cong logic co ban toi bai toan thuc te =====
    [
      {"title": "Cổng logic là gì?",
       "body": "<p>Một cổng logic (logic gate) là mạch điện tử có 1 hoặc nhiều đầu vào nhị phân "
               "(0 hoặc 1) và MỘT đầu ra nhị phân, được xác định bởi một hàm Boolean cố định của "
               "các đầu vào. Đây là khối xây dựng nhỏ nhất của mọi hệ thống số.</p>"},
      {"title": "Cổng AND và OR",
       "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>AND</th><th>OR</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr>"
               "<tr><td>0</td><td>1</td><td>0</td><td>1</td></tr>"
               "<tr><td>1</td><td>0</td><td>0</td><td>1</td></tr>"
               "<tr><td>1</td><td>1</td><td>1</td><td>1</td></tr></tbody></table>"
               "<p>AND chỉ ra 1 khi TẤT CẢ đầu vào đều 1. OR ra 1 khi ÍT NHẤT MỘT đầu vào là 1.</p>"},
      {"title": "Cổng NOT (đảo)",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Cổng NOT</div>"
               "<div class='pd-formula-math'>Y = A′</div></div>"
               "<p>NOT chỉ có 1 đầu vào, đảo ngược trạng thái: đầu vào 0 → đầu ra 1, đầu vào 1 → đầu ra 0.</p>"},
      {"title": "Cổng NAND và NOR",
       "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>NAND</th><th>NOR</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr>"
               "<tr><td>0</td><td>1</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table>"
               "<p>NAND = NOT(AND), NOR = NOT(OR): mỗi cổng chỉ đơn giản đảo ngược toàn bộ cột kết quả "
               "của AND/OR tương ứng.</p>"},
      {"title": "Cổng XOR và XNOR",
       "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>XOR</th><th>XNOR</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>0</td><td>1</td></tr>"
               "<tr><td>0</td><td>1</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>1</td></tr></tbody></table>"
               "<p>XOR ra 1 khi hai đầu vào KHÁC nhau; XNOR (đảo của XOR) ra 1 khi hai đầu vào GIỐNG nhau "
               ": thường dùng để so sánh bit.</p>"},
      {"title": "Ví dụ: mạch 3 đầu vào A·B + C",
       "body": "<p>Tính Y = A·B + C với A=1, B=0, C=1:</p>"
               "<ul><li>Bước 1: A·B = 1·0 = 0</li><li>Bước 2: Y = 0 + C = 0 + 1 = 1</li></ul>"
               "<p>Kết quả: Y = 1. Cách làm: luôn tính AND trước (ưu tiên như phép nhân), rồi tới OR "
               "(như phép cộng), giống thứ tự toán tử số học thông thường.</p>"},
      {"title": "Ví dụ: mạch (A+B)·C",
       "body": "<p>Tính Y = (A+B)·C với A=0, B=1, C=0:</p>"
               "<ul><li>Bước 1: A+B = 0+1 = 1</li><li>Bước 2: Y = 1·C = 1·0 = 0</li></ul>"
               "<p>Kết quả: Y = 0. Dấu ngoặc buộc phải tính OR bên trong trước, dù AND thường có "
               "'độ ưu tiên' cao hơn.</p>"},
      {"title": "Bảng tổng hợp 6 cổng cơ bản",
       "body": "<table class='tt'><thead><tr><th>Cổng</th><th>Ký hiệu</th><th>Ra 1 khi nào</th></tr></thead>"
               "<tbody><tr><td>AND</td><td>A·B</td><td>mọi đầu vào = 1</td></tr>"
               "<tr><td>OR</td><td>A+B</td><td>ít nhất 1 đầu vào = 1</td></tr>"
               "<tr><td>NAND</td><td>(A·B)′</td><td>ít nhất 1 đầu vào = 0</td></tr>"
               "<tr><td>NOR</td><td>(A+B)′</td><td>mọi đầu vào = 0</td></tr>"
               "<tr><td>XOR</td><td>A⊕B</td><td>số đầu vào bằng 1 là LẺ</td></tr>"
               "<tr><td>XNOR</td><td>(A⊕B)′</td><td>số đầu vào bằng 1 là CHẴN</td></tr></tbody></table>"},
      {"title": "⚠️ Bẫy: nhầm AND với OR khi đọc đề bằng lời",
       "body": "<div class='callout warn'><p>Từ 'và' trong tiếng Việt đôi khi được dùng lỏng lẻo cho cả "
               "hai nghĩa. Ví dụ đề bài 'đèn sáng khi công tắc A và công tắc B đều đóng' → đây là AND "
               "(cần CẢ HAI). Nhưng 'đèn sáng khi công tắc A hoặc công tắc B đóng' mới là OR. Luôn kiểm "
               "tra từ khóa 'đều/tất cả' (AND) so với 'hoặc/ít nhất một' (OR) trước khi vẽ mạch.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Không chấm điểm: tự trả lời trước khi sang phần tiếp theo:</p>"
               "<ul><li>Cổng nào cho ra 1 khi CẢ HAI đầu vào đều 0?</li>"
               "<li>Nếu A=1, B=1, C=0, giá trị của A·B + C·A là bao nhiêu?</li></ul>"
               "<p>Gợi ý đáp án: NOR; A·B+C·A = 1·1+0·1 = 1+0 = 1.</p>"},
    ],
    # ===== PHAN 2: Dai so Boolean =====
    [
      {"title": "12 luật cơ bản của đại số Boolean",
       "body": "<table class='tt'><thead><tr><th>#</th><th>Luật</th></tr></thead><tbody>"
               "<tr><td>1</td><td>A + 0 = A</td></tr><tr><td>2</td><td>A + 1 = 1</td></tr>"
               "<tr><td>3</td><td>A · 0 = 0</td></tr><tr><td>4</td><td>A · 1 = A</td></tr>"
               "<tr><td>5</td><td>A + A = A</td></tr><tr><td>6</td><td>A + A′ = 1</td></tr>"
               "<tr><td>7</td><td>A · A = A</td></tr><tr><td>8</td><td>A · A′ = 0</td></tr>"
               "<tr><td>9</td><td>A″ = A</td></tr><tr><td>10</td><td>A + AB = A</td></tr>"
               "<tr><td>11</td><td>A + A′B = A + B</td></tr><tr><td>12</td><td>(A+B)(A+C) = A+BC</td></tr>"
               "</tbody></table>"},
      {"title": "Luật giao hoán và kết hợp",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Giao hoán & kết hợp</div>"
               "<div class='pd-formula-math'>A+B = B+A &nbsp;·&nbsp; (A+B)+C = A+(B+C)</div></div>"
               "<p>Giống hệt số học thông thường: thứ tự cộng/nhân không ảnh hưởng kết quả, và cách "
               "nhóm ngoặc trong một chuỗi toàn AND (hoặc toàn OR) cũng không ảnh hưởng.</p>"},
      {"title": "Luật phân phối",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Phân phối</div>"
               "<div class='pd-formula-math'>A·(B+C) = A·B + A·C</div></div>"
               "<p>Đây là bước then chốt để chuyển một biểu thức từ dạng tích-của-tổng (POS) sang "
               "tổng-của-tích (SOP): dạng chuẩn thường dùng khi thiết kế mạch AND-OR.</p>"},
      {"title": "Ví dụ rút gọn: A + AB",
       "body": "<p>Rút gọn Y = A + AB theo luật 10 (A + AB = A):</p>"
               "<ul><li>Áp dụng trực tiếp luật 10 → Y = A</li></ul>"
               "<p>Kiểm tra bằng bảng chân trị: khi A=0, AB=0 nên Y=0=A; khi A=1, Y=1+B=1=A. Khớp cho "
               "mọi trường hợp → xác nhận luật 10 đúng.</p>"},
      {"title": "Ví dụ rút gọn: AB + AB′",
       "body": "<p>Rút gọn Y = AB + AB′:</p>"
               "<ul><li>Bước 1: đặt A làm nhân tử chung → Y = A(B + B′)</li>"
               "<li>Bước 2: áp dụng luật 6 (B+B′=1) → Y = A·1</li>"
               "<li>Bước 3: áp dụng luật 4 (A·1=A) → Y = A</li></ul>"},
      {"title": "Ví dụ rút gọn nhiều bước: AB + A′C + BC",
       "body": "<p>Rút gọn Y = AB + A′C + BC (định lý đồng nhất/consensus theorem):</p>"
               "<ul><li>Số hạng BC là 'dư thừa' khi đã có AB và A′C</li>"
               "<li>Kết quả rút gọn: Y = AB + A′C</li></ul>"
               "<p>Đây là ví dụ kinh điển cho thấy rút gọn Boolean đôi khi cần nhận ra một số hạng "
               "hoàn toàn dư thừa (consensus term), không chỉ áp dụng luật cơ bản từng bước.</p>"},
      {"title": "Định lý De Morgan",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>De Morgan</div>"
               "<div class='pd-formula-math'>(A·B)′ = A′ + B′ &nbsp;&nbsp; (A+B)′ = A′·B′</div></div>"
               "<ul class='pd-legend'><li><b>Ý nghĩa</b><span>đảo dấu của tích = tổng các đảo; "
               "đảo dấu của tổng = tích các đảo</span></li></ul>"},
      {"title": "Ứng dụng De Morgan: đơn giản hoá (A′B′)′",
       "body": "<p>Rút gọn Y = (A′B′)′:</p>"
               "<ul><li>Áp dụng De Morgan: (A′B′)′ = (A′)′ + (B′)′ = A + B</li></ul>"
               "<p>Kết quả Y = A + B: một cổng NAND với 2 đầu vào đã đảo tương đương một cổng OR "
               "thường, minh hoạ vì sao NAND được coi là cổng vạn năng.</p>"},
      {"title": "Bảng chân trị và Karnaugh map 2 biến",
       "body": "<p>Với Y = A′B + AB′ + AB (3 tổ hợp cho ra 1 trong 4 tổ hợp có thể):</p>"
               "<table class='tt'><thead><tr><th>A\\B</th><th>0</th><th>1</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td></tr>"
               "</tbody></table><p>Nhóm 2 ô kề trong K-map (hàng dưới) cho A, nhóm cột phải cho B → "
               "rút gọn về Y = A + B.</p>"},
      {"title": "⚠️ Bẫy: áp dụng De Morgan sai khi có 3 biến trở lên",
       "body": "<div class='callout warn'><p>Nhiều người chỉ đảo dấu phép toán ngoài cùng mà quên đảo "
               "TỪNG biến bên trong. (ABC)′ KHÔNG PHẢI là A′B′C: đáp án đúng là (ABC)′ = A′+B′+C′ "
               "(áp dụng liên tiếp De Morgan cho từng cặp biến).</p></div>"},
    ],
    # ===== PHAN 3: Mach logic to hop =====
    [
      {"title": "Mạch tổ hợp là gì?",
       "body": "<p>Mạch tổ hợp (combinational logic) là mạch mà đầu ra tại một thời điểm CHỈ phụ thuộc "
               "vào giá trị đầu vào hiện tại, không phụ thuộc lịch sử/trạng thái trước đó: khác với "
               "mạch tuần tự (sequential) có nhớ trạng thái (sẽ học ở phần bistable).</p>"},
      {"title": "Từ bài toán thực tế tới bảng chân trị",
       "body": "<p>Bài toán: đèn cảnh báo cửa càng đáp (Landing Gear Door Warning) sáng khi CÓ ÍT NHẤT "
               "MỘT trong 2 cửa (trái/phải) chưa khoá VÀ máy bay đang bay (không phải trên mặt đất).</p>"
               "<p>Đặt L = cửa trái chưa khoá, R = cửa phải chưa khoá, F = đang bay (in-flight). "
               "Cần: Warning = (L+R)·F.</p>"},
      {"title": "Bảng chân trị mạch cảnh báo cửa càng đáp",
       "body": "<table class='tt'><thead><tr><th>L</th><th>R</th><th>F</th><th>Warning=(L+R)·F</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>1</td><td>1</td></tr>"
               "<tr><td>0</td><td>1</td><td>1</td><td>1</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table>"
               "<p>Hàng cuối minh hoạ: dù cả 2 cửa chưa khoá (L=R=1), nếu máy bay đang ở mặt đất (F=0) "
               "thì KHÔNG cảnh báo: đúng logic AND với F.</p>"},
      {"title": "Từ bảng chân trị tới sơ đồ cổng",
       "body": "<p>Sơ đồ mạch cho Warning = (L+R)·F cần:</p>"
               "<ul><li>1 cổng OR 2 đầu vào (L, R) → cho ra tín hiệu 'có ít nhất 1 cửa mở'</li>"
               "<li>1 cổng AND 2 đầu vào (đầu ra OR, và F) → cho ra tín hiệu cảnh báo cuối cùng</li></ul>"},
      {"title": "Ví dụ 2: mạch khởi động APU (đơn giản hoá)",
       "body": "<p>Theo Tooley: mạch điều khiển khởi động APU (auxiliary power unit) cần điều kiện AND "
               "của nhiều tín hiệu an toàn (vd: không có cảnh báo cháy, tốc độ động cơ trong ngưỡng an "
               "toàn) trước khi cho phép relay khởi động đóng mạch: một ví dụ AND nhiều đầu vào trong "
               "thực tế, không chỉ 2 biến như ví dụ cửa càng đáp.</p>"},
      {"title": "Thiết kế mạch 3 biến từ bảng chân trị (SOP)",
       "body": "<p>Cho bảng chân trị Y=1 khi (A,B,C) = (0,1,1) hoặc (1,0,1). Viết dạng tổng-của-tích (SOP) "
               "bằng cách lấy OR của các minterm ứng với mỗi hàng có Y=1:</p>"
               "<div class='pd-formula'><div class='pd-formula-math'>Y = A′BC + AB′C</div></div>"
               "<p>Rút gọn tiếp bằng cách đặt C chung: Y = C(A′B + AB′) = C(A⊕B).</p>"},
      {"title": "Mạch AND-OR hai tầng",
       "body": "<p>Một mạch tổ hợp SOP tổng quát luôn có thể vẽ dưới dạng 2 tầng: TẦNG 1 là các cổng AND "
               "(mỗi cổng ứng với 1 số hạng tích), TẦNG 2 là MỘT cổng OR gộp tất cả đầu ra của tầng 1: "
               "đây là cấu trúc chuẩn dùng khi lập trình PLD/PAL.</p>"},
      {"title": "So sánh SOP và POS",
       "body": "<table class='tt'><thead><tr><th></th><th>SOP (tổng-của-tích)</th><th>POS (tích-của-tổng)</th></tr></thead>"
               "<tbody><tr><td>Dạng</td><td>Y = AB + A′C</td><td>Y = (A+C)(A′+B)</td></tr>"
               "<tr><td>Lấy từ</td><td>các hàng có Y=1 (minterm)</td><td>các hàng có Y=0 (maxterm), rồi đảo</td></tr>"
               "<tr><td>Cấu trúc mạch</td><td>AND rồi OR</td><td>OR rồi AND</td></tr></tbody></table>"},
      {"title": "⚠️ Bẫy: quên kiểm tra lại toàn bộ bảng chân trị sau khi rút gọn",
       "body": "<div class='callout warn'><p>Sau khi rút gọn biểu thức bằng đại số, LUÔN dựng lại bảng "
               "chân trị của biểu thức đã rút gọn và so với bảng gốc cho TẤT CẢ tổ hợp: chỉ kiểm tra "
               "1-2 hàng dễ khiến bỏ sót lỗi rút gọn sai ở một nhánh ít gặp.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Không chấm điểm: viết biểu thức SOP cho mạch có Y=1 khi (A,B)=(0,1) hoặc (1,1). "
               "Gợi ý: Y = A′B + AB, rút gọn theo luật 11/luật hấp thụ sẽ ra Y = B.</p>"},
    ],
    # ===== PHAN 4: Logic 3 trang thai, don on & song on =====
    [
      {"title": "Tri-state logic là gì?",
       "body": "<p>Logic 3 trạng thái (tri-state) có thêm trạng thái thứ 3 ngoài 0 và 1: trở kháng cao "
               "(High-Z), tại đó đầu ra 'ngắt' khỏi mạch như thể không kết nối. Điều này cho phép NHIỀU "
               "thiết bị chia sẻ chung MỘT đường bus mà không gây xung đột tín hiệu.</p>"},
      {"title": "Chân Enable trên bộ đệm tri-state",
       "body": "<table class='tt'><thead><tr><th>Enable</th><th>Input</th><th>Output</th></tr></thead>"
               "<tbody><tr><td>0</td><td>X (bất kỳ)</td><td>High-Z (ngắt)</td></tr>"
               "<tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></tbody></table>"
               "<p>Chỉ khi Enable=1, bộ đệm mới truyền tín hiệu đầu vào ra đầu ra; Enable=0 luôn cho "
               "High-Z bất kể input.</p>"},
      {"title": "Vì sao bus cần tri-state",
       "body": "<p>Nếu 2 thiết bị cùng nối trực tiếp (không qua tri-state) vào 1 đường dây và một thiết bị "
               "đưa ra logic 1 trong khi thiết bị kia đưa ra logic 0 cùng lúc, sẽ xảy ra xung đột điện "
               "(bus contention): có thể gây hỏng linh kiện. Tri-state giải quyết bằng cách chỉ CHO PHÉP "
               "đúng 1 thiết bị 'nói' trên bus tại một thời điểm, các thiết bị còn lại ở High-Z.</p>"},
      {"title": "Monostable (one-shot) là gì?",
       "body": "<p>Mạch đơn ổn định (monostable/one-shot) chỉ có 1 trạng thái ổn định. Khi nhận một xung "
               "kích (trigger), nó chuyển sang trạng thái thứ 2 trong một khoảng thời gian cố định (do "
               "hằng số RC quyết định), rồi TỰ ĐỘNG quay về trạng thái ổn định ban đầu.</p>"},
      {"title": "Ứng dụng monostable",
       "body": "<p>Monostable thường dùng để tạo một xung có độ rộng CỐ ĐỊNH từ một xung kích có độ rộng "
               "bất kỳ (vd làm sạch/định hình tín hiệu nhiễu từ công tắc cơ khí: debounce), hoặc tạo trễ "
               "thời gian ngắn giữa 2 sự kiện trong một chuỗi điều khiển.</p>"},
      {"title": "Bistable (flip-flop) là gì?",
       "body": "<p>Mạch song ổn định (bistable) có HAI trạng thái ổn định, có thể duy trì mãi mãi cho tới "
               "khi có tín hiệu điều khiển làm nó chuyển trạng thái: đây chính là flip-flop, đơn vị nhớ "
               "1-bit cơ bản của mọi mạch tuần tự (thanh ghi, bộ đếm, bộ nhớ).</p>"},
      {"title": "Flip-flop R-S (Reset-Set) đơn giản",
       "body": "<table class='tt'><thead><tr><th>S</th><th>R</th><th>Q (tiếp theo)</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>giữ nguyên</td></tr>"
               "<tr><td>1</td><td>0</td><td>1 (set)</td></tr>"
               "<tr><td>0</td><td>1</td><td>0 (reset)</td></tr>"
               "<tr><td>1</td><td>1</td><td>không hợp lệ</td></tr></tbody></table>"
               "<p>Có thể dựng từ 2 cổng NOR hoặc 2 cổng NAND nối chéo: chính là ví dụ mạch dual R-S "
               "bistable dùng IC 4001 (CMOS NOR) nêu trong sách Tooley.</p>"},
      {"title": "Bảng so sánh Monostable và Bistable",
       "body": "<table class='tt'><thead><tr><th></th><th>Monostable</th><th>Bistable</th></tr></thead>"
               "<tbody><tr><td>Số trạng thái ổn định</td><td>1</td><td>2</td></tr>"
               "<tr><td>Sau khi kích</td><td>tự quay về ban đầu</td><td>giữ nguyên tới khi bị đổi</td></tr>"
               "<tr><td>Chức năng chính</td><td>tạo xung/độ trễ thời gian</td><td>lưu trữ 1 bit dữ liệu</td></tr>"
               "</tbody></table>"},
      {"title": "⚠️ Bẫy: nhầm High-Z với logic 0",
       "body": "<div class='callout warn'><p>High-Z KHÔNG phải là mức điện áp thấp (logic 0): đó là "
               "trạng thái đầu ra hoàn toàn 'thả nổi', không có dòng điện chảy ra. Đo bằng đồng hồ vạn "
               "năng ở chế độ điện áp có thể cho kết quả không ổn định/nhiễu vì đầu ra không được điều "
               "khiển bởi bất kỳ nguồn nào.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Không chấm điểm: một bus có 4 thiết bị dùng chung, tại một thời điểm cho phép bao nhiêu "
               "thiết bị đang ở trạng thái KHÁC High-Z? Gợi ý: đúng 1 thiết bị (nguyên tắc chia sẻ bus).</p>"},
    ],
    # ===== PHAN 5: Cac ho linh kien logic =====
    [
      {"title": "Vì sao cần nhiều họ logic khác nhau?",
       "body": "<p>Mỗi họ linh kiện logic (logic family) có đặc tính điện khác nhau: điện áp nguồn, "
               "tốc độ chuyển mạch, công suất tiêu thụ, khả năng chịu nhiễu: nên việc chọn đúng họ cho "
               "đúng ứng dụng (tốc độ cao, công suất thấp, môi trường nhiễu mạnh...) là một quyết định "
               "thiết kế quan trọng.</p>"},
      {"title": "Họ TTL (Transistor-Transistor Logic)",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Nguồn TTL chuẩn</div>"
               "<div class='pd-formula-math'>V_CC = 5V ± 5%</div></div>"
               "<p>TTL dùng transistor lưỡng cực (BJT), tốc độ chuyển mạch nhanh, nhưng tiêu thụ dòng "
               "tĩnh lớn hơn CMOS: phù hợp ứng dụng cần tốc độ cao, ít quan tâm công suất.</p>"},
      {"title": "Các biến thể TTL",
       "body": "<table class='tt'><thead><tr><th>Biến thể</th><th>Đặc điểm</th></tr></thead>"
               "<tbody><tr><td>Standard TTL</td><td>cơ bản, fan-out 10, noise margin ~400mV</td></tr>"
               "<tr><td>LS-TTL (Low-power Schottky)</td><td>công suất thấp hơn, vẫn khá nhanh</td></tr>"
               "<tr><td>S-TTL (Schottky)</td><td>nhanh hơn standard, công suất cao hơn</td></tr></tbody></table>"},
      {"title": "Họ CMOS (Complementary MOS)",
       "body": "<p>CMOS dùng cặp transistor MOSFET bổ sung (1 kênh N + 1 kênh P), gần như KHÔNG tiêu thụ "
               "dòng tĩnh khi ở trạng thái ổn định (chỉ tiêu thụ khi chuyển mạch): lý do CMOS thống trị "
               "các thiết bị chạy pin/di động hiện đại.</p>"},
      {"title": "Ưu điểm CMOS: biên độ nhiễu cao",
       "body": "<p>Vì CMOS dùng gần trọn dải điện áp nguồn cho 2 mức logic (rail-to-rail), biên độ nhiễu "
               "(noise margin) của CMOS thường LỚN HƠN TTL đáng kể: chịu nhiễu tốt hơn trong môi trường "
               "điện từ khắc nghiệt như buồng động cơ/khoang điện tử máy bay.</p>"},
      {"title": "Bảng so sánh TTL và CMOS",
       "body": "<table class='tt'><thead><tr><th></th><th>TTL</th><th>CMOS</th></tr></thead>"
               "<tbody><tr><td>Công nghệ transistor</td><td>lưỡng cực (BJT)</td><td>MOSFET bổ sung</td></tr>"
               "<tr><td>Nguồn</td><td>5V ±5%</td><td>3V-15V (tuỳ dòng)</td></tr>"
               "<tr><td>Công suất tĩnh</td><td>cao hơn</td><td>rất thấp</td></tr>"
               "<tr><td>Biên độ nhiễu</td><td>~400mV</td><td>lớn hơn (rail-to-rail)</td></tr>"
               "<tr><td>Phù hợp</td><td>tốc độ cao, ít quan tâm pin</td><td>thiết bị cầm tay/chạy pin</td></tr>"
               "</tbody></table>"},
      {"title": "Ví dụ: chọn họ logic cho thiết bị kiểm tra cầm tay",
       "body": "<p>Bài toán (Tooley Ch.5 Q6): thiết bị kiểm tra cầm tay chạy pin cần họ logic nào? "
               "Vì tiêu chí quan trọng nhất là tiêu thụ điện thấp để kéo dài thời lượng pin, CMOS là "
               "lựa chọn phù hợp nhất trong 3 lựa chọn CMOS/TTL/LS-TTL.</p>"},
      {"title": "Fan-out và fan-in nhắc lại theo họ logic",
       "body": "<p>Fan-out chuẩn của TTL là 10 (điều khiển tối đa 10 đầu vào TTL cùng họ). CMOS thường có "
               "fan-out lớn hơn nhiều về mặt DC (do trở kháng vào cực cao), nhưng bị giới hạn thực tế bởi "
               "tốc độ (mỗi tải thêm làm chậm thời gian chuyển mạch do điện dung ký sinh).</p>"},
      {"title": "⚠️ Bẫy: trộn lẫn TTL và CMOS không đúng cách",
       "body": "<div class='callout warn'><p>Mức điện áp 'logic 1' của TTL (~2.4V trở lên) có thể KHÔNG "
               "đủ để CMOS công suất chuẩn (ngưỡng ~70% Vdd, vd 3.5V với Vdd=5V) nhận diện đúng là mức "
               "cao: cần dùng loại CMOS tương thích TTL (74HCT thay vì 74HC) khi ghép nối hai họ.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Không chấm điểm: một hệ thống buồng lái cần mạch logic chịu nhiễu điện từ mạnh và tiêu "
               "thụ điện thấp: nên ưu tiên họ logic nào? Gợi ý: CMOS (biên độ nhiễu cao + công suất tĩnh "
               "thấp).</p>"},
    ],
  ],
  "en": [
    # ===== PART 1 =====
    [
      {"title": "What is a logic gate?",
       "body": "<p>A logic gate is a circuit with one or more binary inputs (0 or 1) and ONE binary "
               "output, determined by a fixed Boolean function of its inputs. It is the smallest "
               "building block of every digital system.</p>"},
      {"title": "AND and OR gates",
       "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>AND</th><th>OR</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr>"
               "<tr><td>0</td><td>1</td><td>0</td><td>1</td></tr>"
               "<tr><td>1</td><td>0</td><td>0</td><td>1</td></tr>"
               "<tr><td>1</td><td>1</td><td>1</td><td>1</td></tr></tbody></table>"
               "<p>AND outputs 1 only when ALL inputs are 1. OR outputs 1 when AT LEAST ONE input is 1.</p>"},
      {"title": "The NOT gate (inverter)",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>NOT gate</div>"
               "<div class='pd-formula-math'>Y = A′</div></div>"
               "<p>NOT has a single input and inverts it: a 0 input gives a 1 output, a 1 input gives "
               "a 0 output.</p>"},
      {"title": "NAND and NOR gates",
       "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>NAND</th><th>NOR</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr>"
               "<tr><td>0</td><td>1</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table>"
               "<p>NAND = NOT(AND), NOR = NOT(OR): each gate simply inverts the entire result column "
               "of its underlying AND/OR gate.</p>"},
      {"title": "XOR and XNOR gates",
       "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>XOR</th><th>XNOR</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>0</td><td>1</td></tr>"
               "<tr><td>0</td><td>1</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>1</td></tr></tbody></table>"
               "<p>XOR outputs 1 when the two inputs DIFFER; XNOR (the inverse of XOR) outputs 1 when "
               "they are the SAME: often used to compare bits.</p>"},
      {"title": "Worked example: A·B + C",
       "body": "<p>Evaluate Y = A·B + C with A=1, B=0, C=1:</p>"
               "<ul><li>Step 1: A·B = 1·0 = 0</li><li>Step 2: Y = 0 + C = 0 + 1 = 1</li></ul>"
               "<p>Result: Y = 1. Always evaluate AND first (like multiplication), then OR (like "
               "addition): the same operator precedence as ordinary arithmetic.</p>"},
      {"title": "Worked example: (A+B)·C",
       "body": "<p>Evaluate Y = (A+B)·C with A=0, B=1, C=0:</p>"
               "<ul><li>Step 1: A+B = 0+1 = 1</li><li>Step 2: Y = 1·C = 1·0 = 0</li></ul>"
               "<p>Result: Y = 0. The parentheses force the OR inside to be evaluated first, even "
               "though AND usually has 'higher precedence'.</p>"},
      {"title": "Summary table of the 6 basic gates",
       "body": "<table class='tt'><thead><tr><th>Gate</th><th>Symbol</th><th>Outputs 1 when</th></tr></thead>"
               "<tbody><tr><td>AND</td><td>A·B</td><td>every input = 1</td></tr>"
               "<tr><td>OR</td><td>A+B</td><td>at least one input = 1</td></tr>"
               "<tr><td>NAND</td><td>(A·B)′</td><td>at least one input = 0</td></tr>"
               "<tr><td>NOR</td><td>(A+B)′</td><td>every input = 0</td></tr>"
               "<tr><td>XOR</td><td>A⊕B</td><td>an ODD number of inputs are 1</td></tr>"
               "<tr><td>XNOR</td><td>(A⊕B)′</td><td>an EVEN number of inputs are 1</td></tr></tbody></table>"},
      {"title": "⚠️ Trap: confusing AND with OR when reading word problems",
       "body": "<div class='callout warn'><p>Everyday English can be loose about 'and'/'or'. E.g. "
               "'the lamp lights when switch A AND switch B are both closed' is an AND (needs BOTH). "
               "But 'the lamp lights when switch A OR switch B is closed' is an OR. Always check for "
               "'both/all' (AND) versus 'either/at least one' (OR) before drawing the circuit.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>Not graded: answer before moving on:</p>"
               "<ul><li>Which gate outputs 1 only when BOTH inputs are 0?</li>"
               "<li>If A=1, B=1, C=0, what is A·B + C·A?</li></ul>"
               "<p>Hint: NOR; A·B+C·A = 1·1+0·1 = 1+0 = 1.</p>"},
    ],
    # ===== PART 2 =====
    [
      {"title": "The 12 basic laws of Boolean algebra",
       "body": "<table class='tt'><thead><tr><th>#</th><th>Law</th></tr></thead><tbody>"
               "<tr><td>1</td><td>A + 0 = A</td></tr><tr><td>2</td><td>A + 1 = 1</td></tr>"
               "<tr><td>3</td><td>A · 0 = 0</td></tr><tr><td>4</td><td>A · 1 = A</td></tr>"
               "<tr><td>5</td><td>A + A = A</td></tr><tr><td>6</td><td>A + A′ = 1</td></tr>"
               "<tr><td>7</td><td>A · A = A</td></tr><tr><td>8</td><td>A · A′ = 0</td></tr>"
               "<tr><td>9</td><td>A″ = A</td></tr><tr><td>10</td><td>A + AB = A</td></tr>"
               "<tr><td>11</td><td>A + A′B = A + B</td></tr><tr><td>12</td><td>(A+B)(A+C) = A+BC</td></tr>"
               "</tbody></table>"},
      {"title": "Commutative and associative laws",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Commutative & associative</div>"
               "<div class='pd-formula-math'>A+B = B+A &nbsp;·&nbsp; (A+B)+C = A+(B+C)</div></div>"
               "<p>Exactly like ordinary arithmetic: the order of addition/multiplication doesn't "
               "matter, and grouping within a chain of all-AND (or all-OR) terms doesn't matter either.</p>"},
      {"title": "The distributive law",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Distributive</div>"
               "<div class='pd-formula-math'>A·(B+C) = A·B + A·C</div></div>"
               "<p>This is the key step for converting an expression from product-of-sums (POS) to "
               "sum-of-products (SOP) form: the standard form used when designing AND-OR circuits.</p>"},
      {"title": "Worked simplification: A + AB",
       "body": "<p>Simplify Y = A + AB using rule 10 (A + AB = A):</p>"
               "<ul><li>Apply rule 10 directly → Y = A</li></ul>"
               "<p>Check with a truth table: when A=0, AB=0 so Y=0=A; when A=1, Y=1+B=1=A. Matches in "
               "every case: confirms rule 10 is correct.</p>"},
      {"title": "Worked simplification: AB + AB′",
       "body": "<p>Simplify Y = AB + AB′:</p>"
               "<ul><li>Step 1: factor out A → Y = A(B + B′)</li>"
               "<li>Step 2: apply rule 6 (B+B′=1) → Y = A·1</li>"
               "<li>Step 3: apply rule 4 (A·1=A) → Y = A</li></ul>"},
      {"title": "Multi-step simplification: AB + A′C + BC",
       "body": "<p>Simplify Y = AB + A′C + BC (the consensus theorem):</p>"
               "<ul><li>The term BC is redundant once AB and A′C are present</li>"
               "<li>Simplified result: Y = AB + A′C</li></ul>"
               "<p>A classic example showing simplification sometimes requires spotting one entirely "
               "redundant term (the 'consensus' term), not just applying basic laws step by step.</p>"},
      {"title": "De Morgan's theorem",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>De Morgan</div>"
               "<div class='pd-formula-math'>(A·B)′ = A′ + B′ &nbsp;&nbsp; (A+B)′ = A′·B′</div></div>"
               "<ul class='pd-legend'><li><b>Meaning</b><span>the complement of a product equals the "
               "sum of complements; the complement of a sum equals the product of complements</span></li></ul>"},
      {"title": "Applying De Morgan: simplifying (A′B′)′",
       "body": "<p>Simplify Y = (A′B′)′:</p>"
               "<ul><li>Apply De Morgan: (A′B′)′ = (A′)′ + (B′)′ = A + B</li></ul>"
               "<p>Result: Y = A + B: a NAND gate with both inputs inverted is equivalent to a plain "
               "OR gate, illustrating why NAND is called a universal gate.</p>"},
      {"title": "Truth table and 2-variable Karnaugh map",
       "body": "<p>For Y = A′B + AB′ + AB (1 in three of the four possible combinations):</p>"
               "<table class='tt'><thead><tr><th>A\\B</th><th>0</th><th>1</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td></tr>"
               "</tbody></table><p>Grouping the two adjacent cells in the bottom row gives A, and the "
               "right column gives B → simplifies to Y = A + B.</p>"},
      {"title": "⚠️ Trap: misapplying De Morgan with 3+ variables",
       "body": "<div class='callout warn'><p>A common mistake is inverting only the outermost operator "
               "while forgetting to invert EACH inner variable. (ABC)′ is NOT A′B′C: the correct answer "
               "is (ABC)′ = A′+B′+C′ (apply De Morgan repeatedly, pair by pair).</p></div>"},
    ],
    # ===== PART 3 =====
    [
      {"title": "What is combinational logic?",
       "body": "<p>A combinational circuit is one whose output at any instant depends ONLY on the "
               "current input values, not on any past history/state: unlike sequential circuits which "
               "retain state (covered in the bistable section).</p>"},
      {"title": "From a real problem to a truth table",
       "body": "<p>Problem: the Landing Gear Door Warning lamp should light when AT LEAST ONE of the two "
               "doors (left/right) is unlocked AND the aircraft is in flight (not on the ground).</p>"
               "<p>Let L = left door unlocked, R = right door unlocked, F = in-flight. We need: "
               "Warning = (L+R)·F.</p>"},
      {"title": "Truth table for the landing gear door warning",
       "body": "<table class='tt'><thead><tr><th>L</th><th>R</th><th>F</th><th>Warning=(L+R)·F</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>1</td><td>1</td></tr>"
               "<tr><td>0</td><td>1</td><td>1</td><td>1</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table>"
               "<p>The last row shows: even with both doors unlocked (L=R=1), if the aircraft is on the "
               "ground (F=0) there is NO warning: correctly ANDed with F.</p>"},
      {"title": "From truth table to gate diagram",
       "body": "<p>The circuit for Warning = (L+R)·F needs:</p>"
               "<ul><li>One 2-input OR gate (L, R) → produces 'at least one door open'</li>"
               "<li>One 2-input AND gate (the OR's output, and F) → produces the final warning signal</li></ul>"},
      {"title": "Example 2: APU starter control (simplified)",
       "body": "<p>Per Tooley: the APU (auxiliary power unit) starter control circuit ANDs together "
               "several safety signals (e.g. no fire warning, engine speed within a safe range) before "
               "allowing the start relay to close: a real-world example of an AND with multiple "
               "inputs, not just the two-variable case above.</p>"},
      {"title": "Designing a 3-variable circuit from a truth table (SOP)",
       "body": "<p>Given a truth table where Y=1 for (A,B,C) = (0,1,1) or (1,0,1), write the sum-of-"
               "products (SOP) form by ORing the minterm for each row where Y=1:</p>"
               "<div class='pd-formula'><div class='pd-formula-math'>Y = A′BC + AB′C</div></div>"
               "<p>Simplify further by factoring out C: Y = C(A′B + AB′) = C(A⊕B).</p>"},
      {"title": "The two-level AND-OR circuit",
       "body": "<p>Any general SOP combinational circuit can always be drawn as two levels: LEVEL 1 is a "
               "set of AND gates (one per product term), LEVEL 2 is a SINGLE OR gate combining all "
               "level-1 outputs: the standard structure used when programming PLDs/PALs.</p>"},
      {"title": "SOP versus POS",
       "body": "<table class='tt'><thead><tr><th></th><th>SOP (sum-of-products)</th><th>POS (product-of-sums)</th></tr></thead>"
               "<tbody><tr><td>Form</td><td>Y = AB + A′C</td><td>Y = (A+C)(A′+B)</td></tr>"
               "<tr><td>Derived from</td><td>rows where Y=1 (minterms)</td><td>rows where Y=0 (maxterms), then inverted</td></tr>"
               "<tr><td>Circuit structure</td><td>AND then OR</td><td>OR then AND</td></tr></tbody></table>"},
      {"title": "⚠️ Trap: forgetting to re-check the full truth table after simplifying",
       "body": "<div class='callout warn'><p>After algebraically simplifying an expression, ALWAYS rebuild "
               "the truth table of the simplified expression and compare it against the original for "
               "EVERY combination: checking only 1-2 rows can hide an error in a less common branch.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>Not graded: write the SOP expression for a circuit where Y=1 when (A,B)=(0,1) or "
               "(1,1). Hint: Y = A′B + AB, which simplifies via the absorption law to Y = B.</p>"},
    ],
    # ===== PART 4 =====
    [
      {"title": "What is tri-state logic?",
       "body": "<p>Tri-state logic adds a third state beyond 0 and 1: high impedance (High-Z), where "
               "the output 'disconnects' from the circuit as if not connected at all. This lets MULTIPLE "
               "devices share a SINGLE bus line without signal conflicts.</p>"},
      {"title": "The Enable pin on a tri-state buffer",
       "body": "<table class='tt'><thead><tr><th>Enable</th><th>Input</th><th>Output</th></tr></thead>"
               "<tbody><tr><td>0</td><td>X (any)</td><td>High-Z (disconnected)</td></tr>"
               "<tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></tbody></table>"
               "<p>Only when Enable=1 does the buffer pass the input through; Enable=0 always gives "
               "High-Z regardless of the input.</p>"},
      {"title": "Why buses need tri-state",
       "body": "<p>If two devices are wired directly (without tri-state) to one line and one drives "
               "logic 1 while the other drives logic 0 at the same time, an electrical conflict (bus "
               "contention) results: potentially damaging components. Tri-state solves this by "
               "allowing only ONE device to 'talk' on the bus at a time, with all others in High-Z.</p>"},
      {"title": "What is a monostable (one-shot)?",
       "body": "<p>A monostable circuit has only ONE stable state. On receiving a trigger pulse, it "
               "switches to a second state for a fixed duration (set by an RC time constant), then "
               "AUTOMATICALLY returns to its original stable state.</p>"},
      {"title": "Applications of monostables",
       "body": "<p>Monostables are commonly used to generate a pulse of FIXED width from a trigger "
               "pulse of arbitrary width (e.g. cleaning up/shaping a noisy signal from a mechanical "
               "switch: debouncing), or to create a short time delay between two events in a control "
               "sequence.</p>"},
      {"title": "What is a bistable (flip-flop)?",
       "body": "<p>A bistable circuit has TWO stable states and can hold either one indefinitely until a "
               "control signal forces a change: this is the flip-flop, the basic 1-bit memory element "
               "underlying every sequential circuit (registers, counters, memory).</p>"},
      {"title": "A simple R-S (Reset-Set) flip-flop",
       "body": "<table class='tt'><thead><tr><th>S</th><th>R</th><th>Next Q</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>unchanged</td></tr>"
               "<tr><td>1</td><td>0</td><td>1 (set)</td></tr>"
               "<tr><td>0</td><td>1</td><td>0 (reset)</td></tr>"
               "<tr><td>1</td><td>1</td><td>invalid</td></tr></tbody></table>"
               "<p>Can be built from two cross-coupled NOR gates or two cross-coupled NAND gates: "
               "exactly the dual R-S bistable example built with a 4001 (CMOS NOR) IC mentioned in "
               "Tooley's textbook.</p>"},
      {"title": "Monostable vs bistable comparison",
       "body": "<table class='tt'><thead><tr><th></th><th>Monostable</th><th>Bistable</th></tr></thead>"
               "<tbody><tr><td>Stable states</td><td>1</td><td>2</td></tr>"
               "<tr><td>After triggering</td><td>returns automatically</td><td>holds until forced to change</td></tr>"
               "<tr><td>Main function</td><td>pulse/time-delay generation</td><td>storing 1 bit of data</td></tr>"
               "</tbody></table>"},
      {"title": "⚠️ Trap: confusing High-Z with logic 0",
       "body": "<div class='callout warn'><p>High-Z is NOT a low voltage level (logic 0): it is a "
               "fully 'floating' output state with no current being driven. Measuring it with a "
               "voltmeter can give unstable/noisy readings because the output isn't being driven by "
               "any source.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>Not graded: on a bus shared by 4 devices, how many devices should be in a state OTHER "
               "than High-Z at any one time? Hint: exactly 1 (the bus-sharing principle).</p>"},
    ],
    # ===== PART 5 =====
    [
      {"title": "Why are there several different logic families?",
       "body": "<p>Each logic family has different electrical characteristics: supply voltage, "
               "switching speed, power consumption, noise immunity: so choosing the right family for "
               "the right application (high speed, low power, high-noise environment...) is an "
               "important design decision.</p>"},
      {"title": "The TTL family (Transistor-Transistor Logic)",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Standard TTL supply</div>"
               "<div class='pd-formula-math'>V_CC = 5V ± 5%</div></div>"
               "<p>TTL uses bipolar (BJT) transistors, offering fast switching but higher static "
               "current draw than CMOS: suitable for high-speed applications where power is less "
               "of a concern.</p>"},
      {"title": "TTL variants",
       "body": "<table class='tt'><thead><tr><th>Variant</th><th>Characteristic</th></tr></thead>"
               "<tbody><tr><td>Standard TTL</td><td>baseline, fan-out 10, noise margin ~400mV</td></tr>"
               "<tr><td>LS-TTL (Low-power Schottky)</td><td>lower power, still fairly fast</td></tr>"
               "<tr><td>S-TTL (Schottky)</td><td>faster than standard, higher power</td></tr></tbody></table>"},
      {"title": "The CMOS family (Complementary MOS)",
       "body": "<p>CMOS uses complementary MOSFET pairs (one N-channel + one P-channel), drawing "
               "virtually NO static current in a steady state (power is drawn mainly while switching) "
               ": the reason CMOS dominates modern battery-powered/portable devices.</p>"},
      {"title": "CMOS advantage: high noise margin",
       "body": "<p>Because CMOS outputs swing almost the entire supply range for its two logic levels "
               "(rail-to-rail), its noise margin is typically MUCH LARGER than TTL's: better immunity "
               "in harsh electromagnetic environments such as an engine bay/avionics compartment.</p>"},
      {"title": "TTL vs CMOS comparison table",
       "body": "<table class='tt'><thead><tr><th></th><th>TTL</th><th>CMOS</th></tr></thead>"
               "<tbody><tr><td>Transistor technology</td><td>bipolar (BJT)</td><td>complementary MOSFET</td></tr>"
               "<tr><td>Supply</td><td>5V ±5%</td><td>3V-15V (depending on series)</td></tr>"
               "<tr><td>Static power</td><td>higher</td><td>very low</td></tr>"
               "<tr><td>Noise margin</td><td>~400mV</td><td>larger (rail-to-rail)</td></tr>"
               "<tr><td>Best suited for</td><td>high speed, power less critical</td><td>portable/battery-powered devices</td></tr>"
               "</tbody></table>"},
      {"title": "Example: choosing a logic family for portable test equipment",
       "body": "<p>Problem (Tooley Ch.5 Q6): which logic family suits a battery-powered, portable piece "
               "of test equipment? Since the key requirement is low power consumption to extend battery "
               "life, CMOS is the most appropriate choice among CMOS/TTL/LS-TTL.</p>"},
      {"title": "Fan-out and fan-in revisited by family",
       "body": "<p>Standard TTL fan-out is 10 (drives up to 10 same-family TTL inputs). CMOS typically "
               "has a much higher DC fan-out (due to its extremely high input impedance), but is limited "
               "in practice by speed (each added load slows switching time due to parasitic capacitance).</p>"},
      {"title": "⚠️ Trap: mixing TTL and CMOS incorrectly",
       "body": "<div class='callout warn'><p>TTL's 'logic 1' voltage level (~2.4V or above) may NOT be "
               "high enough for standard-power CMOS (threshold ~70% of Vdd, e.g. 3.5V at Vdd=5V) to "
               "reliably recognise as high: use a TTL-compatible CMOS variant (74HCT instead of 74HC) "
               "when interfacing the two families.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>Not graded: a cockpit system needs logic circuits that resist strong electromagnetic "
               "interference and draw low power: which family should be preferred? Hint: CMOS (high "
               "noise margin plus low static power).</p>"},
    ],
  ],
}
