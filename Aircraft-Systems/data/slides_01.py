# -*- coding: utf-8 -*-
"""Noi dung 10 slide/phan x 5 phan cho Module 01 - Number Systems (VI + EN)."""

SLIDES = {
  "vi": [
    # ===== Phan 1: Vi sao may tinh hang khong can nhieu he dem? =====
    [
      {"title": "Vì sao không dùng luôn hệ thập phân trong mạch điện tử?",
       "body": "<p>Mạch điện tử số chỉ phân biệt tin cậy được <b>hai mức điện áp</b> (cao/thấp), không thể phân biệt chính xác 10 mức điện áp khác nhau để biểu diễn 10 chữ số thập phân. Vì vậy phần cứng buộc phải dùng hệ nhị phân (2 mức), còn các hệ đếm khác (bát phân, hex, BCD) chỉ là cách con người viết gọn lại chuỗi nhị phân đó.</p>"},
      {"title": "Bốn hệ đếm cốt lõi trong avionics",
       "body": "<table class='tt'><thead><tr><th>Hệ đếm</th><th>Cơ số</th><th>Chữ số dùng</th><th>Vai trò chính</th></tr></thead><tbody>"
               "<tr><td>Nhị phân</td><td>2</td><td>0,1</td><td>Xử lý bên trong máy tính</td></tr>"
               "<tr><td>Bát phân</td><td>8</td><td>0-7</td><td>Mã trạng thái hệ thống gọn</td></tr>"
               "<tr><td>Thập lục phân</td><td>16</td><td>0-9,A-F</td><td>Địa chỉ bộ nhớ, mã lỗi BITE</td></tr>"
               "<tr><td>BCD</td><td>—</td><td>4 bit/chữ số</td><td>Hiển thị số thập phân trên màn hình</td></tr>"
               "</tbody></table>"},
      {"title": "Trọng số vị trí — nguyên lý dùng chung cho MỌI hệ đếm",
       "body": "<p>Trong bất kỳ hệ đếm cơ số b nào, mỗi chữ số ở vị trí i (tính từ phải, bắt đầu từ 0) có trọng số bⁱ. Giá trị của cả số = tổng (chữ số × trọng số).</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Giá trị của một số ở cơ số b</div><div class='pd-formula-math'>N = Σ dᵢ·bⁱ</div></div>"},
      {"title": "Ví dụ: áp dụng trọng số cho số thập phân quen thuộc",
       "body": "<p>Số 528 (hệ 10) = 5·10² + 2·10¹ + 8·10⁰ = 500+20+8 = 528. Đây chính là nguyên lý mà chương trình học sẽ áp dụng lại y hệt cho cơ số 2, 8, 16 — chỉ đổi giá trị b.</p>"},
      {"title": "Vì sao kỹ thuật viên KHÔNG đọc trực tiếp chuỗi nhị phân dài?",
       "body": "<p>Một địa chỉ bộ nhớ 16-bit viết ở nhị phân dài 16 ký tự (vd <code>1010110011110000</code>), rất dễ đọc nhầm hoặc chép sai 1 bit khi ghi tay. Viết lại ở hex chỉ còn 4 ký tự (<code>ACF0</code>) — giảm sai sót thao tác, đây là lý do kỹ thuật thực dụng chứ không chỉ lý thuyết.</p>"},
      {"title": "Bốn hệ đếm không tách rời — luôn phải quy đổi qua lại",
       "body": "<ul><li>Máy tính XỬ LÝ ở nhị phân</li><li>Màn hình HIỂN THỊ cho phi công ở BCD/thập phân</li><li>Tài liệu bảo dưỡng GHI LẠI mã lỗi ở hex</li><li>Một số trang trạng thái hệ thống cũ dùng bát phân</li></ul><p>Kỹ sư bảo dưỡng phải thành thạo quy đổi cả 4 chiều, không chỉ 1 chiều duy nhất.</p>"},
      {"title": "⚠️ Bẫy: nhầm 'hệ đếm' với 'đơn vị đo'",
       "body": "<div class='callout warn'><p>Học viên mới thường nhầm 10₁₆ (mười sáu, hệ hex) với 10 (mười, hệ thập phân) vì cách viết giống hệt nhau. Luôn phải ghi rõ subscript cơ số khi trình bày, đúng quy ước trong sách Tooley: (75)₈, (75)₁₀, (75)₁₆ là BA giá trị hoàn toàn khác nhau dù cùng ba ký tự '7','5'.</p></div>"},
      {"title": "Áp dụng A320: vì sao FMGC cần hiểu cả 4 hệ đếm",
       "body": "<p>FMGC (Flight Management Guidance Computer) nhận dữ liệu nhị phân từ cảm biến, tính toán nội bộ ở nhị phân, nhưng phải XUẤT RA hex cho log bảo dưỡng, BCD cho hiển thị MCDU, và đôi khi bát phân cho mã trạng thái — một chip xử lý số phải chuyển đổi qua lại liên tục giữa các hệ này trong thời gian thực.</p>"},
      {"title": "Sơ đồ luồng dữ liệu số trong buồng lái",
       "body": "<p>Cảm biến (analog) → ADC → nhị phân (xử lý trong FMGC/FWC) → mã hoá lại thành BCD/hex → hiển thị EFIS/ECAM hoặc ghi log BITE. Mỗi mũi tên trong chuỗi này là một điểm cần hiểu đúng hệ đếm đang dùng.</p>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>Dừng lại 30 giây: bạn có thể giải thích bằng lời vì sao một kỹ sư bảo dưỡng KHÔNG thể chỉ học một hệ đếm duy nhất mà bỏ qua 3 hệ còn lại không? Nếu chưa chắc, xem lại 2 slide đầu trước khi sang Phần 2.</p></div>"},
    ],
    # ===== Phan 2: He nhi phan va phep chuyen doi =====
    [
      {"title": "MSB, LSB và trọng số luỹ thừa của 2",
       "body": "<p>Trong số nhị phân, bit ngoài cùng bên trái là <b>MSB</b> (Most Significant Bit — trọng số lớn nhất), bit ngoài cùng bên phải là <b>LSB</b> (Least Significant Bit — trọng số 2⁰=1).</p>"
               "<table class='tt'><thead><tr><th>2⁷</th><th>2⁶</th><th>2⁵</th><th>2⁴</th><th>2³</th><th>2²</th><th>2¹</th><th>2⁰</th></tr></thead>"
               "<tbody><tr><td>128</td><td>64</td><td>32</td><td>16</td><td>8</td><td>4</td><td>2</td><td>1</td></tr></tbody></table>"},
      {"title": "Ví dụ từng bước: đổi nhị phân → thập phân",
       "body": "<p>Đổi 11011010₂ sang thập phân — cộng đúng trọng số của các bit bằng 1:</p><p>11011010 = 128+64+0+16+8+0+2+0 = <b>218</b></p><p>(Đây chính là ví dụ gốc trong Tooley — chỉ cộng trọng số ở vị trí có bit 1, bỏ qua vị trí bit 0.)</p>"},
      {"title": "Ví dụ từng bước: đổi thập phân → nhị phân (chia liên tiếp)",
       "body": "<p>Đổi 45 sang nhị phân bằng chia liên tiếp cho 2, đọc số dư từ dưới lên:</p>"
               "<table class='tt'><thead><tr><th>Phép chia</th><th>Thương</th><th>Dư</th></tr></thead><tbody>"
               "<tr><td>45÷2</td><td>22</td><td>1</td></tr><tr><td>22÷2</td><td>11</td><td>0</td></tr>"
               "<tr><td>11÷2</td><td>5</td><td>1</td></tr><tr><td>5÷2</td><td>2</td><td>1</td></tr>"
               "<tr><td>2÷2</td><td>1</td><td>0</td></tr><tr><td>1÷2</td><td>0</td><td>1</td></tr></tbody></table>"
               "<p>Đọc dư từ dưới lên: <b>101101</b> (khớp đúng kết quả đã kiểm chứng bằng code trong notebook 01).</p>"},
      {"title": "Cách nhanh hơn: cộng trực tiếp trọng số 2ⁱ (không cần chia)",
       "body": "<p>45 = 32+8+4+1 → đánh dấu 1 vào đúng 4 vị trí trọng số 32,8,4,1, còn lại là 0 → 101101. Cách này nhanh hơn khi làm tay, nhưng cách chia liên tiếp ở slide trước là cách TỔNG QUÁT áp dụng được cho cả octal/hex.</p>"},
      {"title": "Phép cộng nhị phân — quy tắc nhớ (carry)",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Bảng cộng 1 bit</div><div class='pd-formula-math'>0+0=0 · 0+1=1 · 1+0=1 · 1+1=10 (nhớ 1)</div></div><p>Ví dụ: 0110 + 0101 = 1011 (6+5=11, kiểm tra lại bằng thập phân để tự tin quy tắc nhớ đã áp dụng đúng).</p>"},
      {"title": "Số âm trong nhị phân: vì sao cần bù hai",
       "body": "<p>Nhị phân thuần không có dấu trừ. Để biểu diễn số âm, hệ thống số dùng <b>bù hai (two's complement)</b>: đảo tất cả bit rồi cộng thêm 1. Đây là cách CPU thực hiện phép trừ chỉ bằng mạch cộng.</p>"},
      {"title": "Ví dụ từng bước: bù hai của 10110",
       "body": "<p>Bước 1 — đảo bit: 10110 → 01001.</p><p>Bước 2 — cộng 1: 01001 + 1 = <b>01010</b>.</p><p>(Khớp đúng câu hỏi gốc Tooley Ch.2 Q3 — xem quiz Module 01.)</p>"},
      {"title": "⚠️ Bẫy: quên bước cộng 1 sau khi đảo bit",
       "body": "<div class='callout warn'><p>Lỗi phổ biến nhất khi tính bù hai là chỉ đảo bit rồi DỪNG LẠI — đó là <b>bù một (one's complement)</b>, không phải bù hai. Luôn kiểm tra lại bằng cách cộng số gốc với kết quả bù hai: nếu tổng tràn ra ngoài số bit ban đầu (vd 10110+01010=100000, bỏ bit tràn còn 00000), kết quả đúng.</p></div>"},
      {"title": "Áp dụng A320: vì sao ADIRU xuất dữ liệu nhị phân 2 chiều",
       "body": "<p>ADIRU (Air Data Inertial Reference Unit) phải biểu diễn cả giá trị dương (độ cao tăng) và âm (tốc độ giảm/góc nghiêng âm) — bù hai cho phép FMGC cộng/trừ các giá trị này bằng đúng một mạch cộng nhị phân duy nhất, không cần mạch trừ riêng.</p>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>Tự tính nhẩm: bù hai của số nhị phân 4-bit 0110 là gì? (Gợi ý: đảo thành 1001, cộng 1 → 1010). Nếu ra khác, xem lại 2 bước ở slide bù hai phía trên.</p></div>"},
    ],
    # ===== Phan 3: He bat phan va thap luc phan =====
    [
      {"title": "Vì sao nhóm 3 bit cho octal, nhóm 4 bit cho hex?",
       "body": "<p>2³=8 nên mỗi chữ số bát phân biểu diễn đúng 3 bit; 2⁴=16 nên mỗi chữ số hex biểu diễn đúng 4 bit. Đây KHÔNG phải quy ước tuỳ ý — nó xuất phát trực tiếp từ định nghĩa cơ số.</p>"},
      {"title": "Bảng tra nhanh: nhị phân ↔ hex (bắt buộc thuộc lòng)",
       "body": "<table class='tt'><thead><tr><th>Hex</th><th>Nhị phân</th><th>Hex</th><th>Nhị phân</th></tr></thead><tbody>"
               "<tr><td>0</td><td>0000</td><td>8</td><td>1000</td></tr><tr><td>1</td><td>0001</td><td>9</td><td>1001</td></tr>"
               "<tr><td>2</td><td>0010</td><td>A</td><td>1010</td></tr><tr><td>3</td><td>0011</td><td>B</td><td>1011</td></tr>"
               "<tr><td>4</td><td>0100</td><td>C</td><td>1100</td></tr><tr><td>5</td><td>0101</td><td>D</td><td>1101</td></tr>"
               "<tr><td>6</td><td>0110</td><td>E</td><td>1110</td></tr><tr><td>7</td><td>0111</td><td>F</td><td>1111</td></tr></tbody></table>"},
      {"title": "Ví dụ từng bước: nhị phân → bát phân bằng nhóm 3 bit",
       "body": "<p>Đổi 100010001₂ sang bát phân — nhóm từ phải sang trái theo 3 bit: 100 | 010 | 001 → 4 2 1 → <b>421₈</b>. (Khớp Tooley Ch.2 Q8.)</p>"},
      {"title": "Ví dụ từng bước: hex → bát phân PHẢI qua nhị phân trung gian",
       "body": "<p>111₁₆ → nhị phân từng chữ số hex (4 bit/số): 1→0001, 1→0001, 1→0001 → 000100010001₂.</p><p>Nhóm lại theo 3 bit từ phải: 000 100 010 001 → 4 2 1 → <b>421₈</b>. Không thể suy trực tiếp hex→octal mà bỏ qua bước này.</p>"},
      {"title": "Ví dụ từng bước: nhị phân → hex bằng nhóm 4 bit",
       "body": "<p>Đổi 10110011₂ sang hex — nhóm 4 bit: 1011 | 0011 → B | 3 → <b>B3₁₆</b>. (Khớp Tooley Ch.2 Q11.)</p>"},
      {"title": "Đệm 0 ở đầu khi số bit không chia hết",
       "body": "<p>Đổi 111001110₂ (9 bit) sang octal: đệm thêm 0 ở đầu cho đủ bội số 3 → 011 100 111 0 → sai, phải đệm cho đủ 9→9 chia hết cho 3 rồi: 111 001 110 → 7 1 6 → 716₈. Luôn đếm số bit trước khi nhóm, đệm 0 bên TRÁI nếu thiếu.</p>"},
      {"title": "Vì sao hex phổ biến hơn octal trong hệ thống hiện đại",
       "body": "<p>Hầu hết bus dữ liệu hiện đại (8/16/32-bit) là bội số của 4, nên hex nhóm vừa khít không cần đệm; trong khi octal (nhóm 3) thường lệch với các độ rộng bus phổ biến. Đây là lý do hex chiếm ưu thế trong tài liệu bảo dưỡng hiện đại hơn octal.</p>"},
      {"title": "⚠️ Bẫy: cộng/trừ trực tiếp các chữ số hex như thập phân",
       "body": "<div class='callout warn'><p>Không được cộng '9'+'9'=18 rồi viết '18' vào kết quả hex — hex chỉ có 16 ký hiệu (0-F). 9+9=18 (thập phân) = 12₁₆, viết là 2, nhớ 1. Luôn đổi qua thập phân để cộng rồi đổi ngược lại nếu chưa quen bảng cộng hex.</p></div>"},
      {"title": "Áp dụng A320: mã lỗi BITE luôn hiển thị ở hex 4 chữ số",
       "body": "<p>Một fault code kiểu <code>0xACDE</code> tương ứng đúng 16 bit nhị phân (4 chữ số hex × 4 bit). Kỹ sư tra cứu trong AMM không cần đếm 16 bit riêng lẻ — chỉ cần khớp đúng 4 ký tự hex, giảm mạnh khả năng đọc nhầm so với nhìn chuỗi nhị phân dài.</p>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>Không dùng máy tính: 2F₁₆ đổi sang nhị phân là gì? (Gợi ý: 2→0010, F→1111 → 00101111). Kiểm tra lại bằng bảng tra ở slide đầu phần này nếu chưa chắc.</p></div>"},
    ],
    # ===== Phan 4: Ma BCD va ASCII =====
    [
      {"title": "BCD khác nhị phân thuần ở điểm nào?",
       "body": "<p>Nhị phân thuần đổi CẢ SỐ cùng lúc; BCD đổi TỪNG CHỮ SỐ THẬP PHÂN riêng biệt thành 4 bit. Vì vậy BCD luôn dùng nhiều bit hơn nhị phân thuần cho cùng một giá trị, đổi lại việc chuyển sang hiển thị 7 đoạn cực kỳ đơn giản.</p>"},
      {"title": "Bảng chuyển đổi 10 chữ số thập phân ↔ BCD",
       "body": "<table class='tt'><thead><tr><th>Chữ số</th><th>BCD</th><th>Chữ số</th><th>BCD</th></tr></thead><tbody>"
               "<tr><td>0</td><td>0000</td><td>5</td><td>0101</td></tr><tr><td>1</td><td>0001</td><td>6</td><td>0110</td></tr>"
               "<tr><td>2</td><td>0010</td><td>7</td><td>0111</td></tr><tr><td>3</td><td>0011</td><td>8</td><td>1000</td></tr>"
               "<tr><td>4</td><td>0100</td><td>9</td><td>1001</td></tr></tbody></table>"},
      {"title": "Ví dụ từng bước: thập phân → BCD",
       "body": "<p>Đổi 37 sang BCD — tách riêng từng chữ số: 3→0011, 7→0111 → ghép lại <b>00110111</b>. (Khớp Tooley Ch.2 Q5.)</p>"},
      {"title": "Ví dụ từng bước: BCD → thập phân",
       "body": "<p>Đổi 10010001 (BCD) sang thập phân — tách nhóm 4 bit từ phải: 1001 | 0001 → 9 | 1 → <b>91</b>. (Khớp Tooley Ch.2 Q4.)</p>"},
      {"title": "6 tổ hợp KHÔNG hợp lệ trong BCD",
       "body": "<p>BCD 4-bit có 16 tổ hợp khả dĩ (0000-1111) nhưng chỉ 10 tổ hợp (0000-1001) hợp lệ. Sáu tổ hợp 1010-1111 KHÔNG tương ứng chữ số thập phân nào — nếu mạch giải mã BCD gặp các mã này, đó là dấu hiệu lỗi phần cứng/nhiễu dữ liệu.</p>"},
      {"title": "ASCII — mã hoá ký tự, không phải mã hoá số lượng",
       "body": "<p>ASCII chuẩn dùng 7 bit, biểu diễn 128 ký tự (chữ, số, dấu câu, ký tự điều khiển). Lưu ý: ASCII của ký tự '5' (mã 0110101₂ = 35₁₆) KHÁC HOÀN TOÀN với số nhị phân của giá trị 5 (00000101₂) — đây là hai khái niệm mã hoá độc lập.</p>"},
      {"title": "Ví dụ: mã ASCII của ký tự 'A'",
       "body": "<p>'A' = 65 (thập phân) = 41₁₆ = 1000001₂. Chuỗi văn bản 'TCAS' được truyền đi dưới dạng 4 byte ASCII liên tiếp, không phải một con số duy nhất.</p>"},
      {"title": "⚠️ Bẫy: nhầm BCD với hex khi nhìn 4-bit đơn lẻ",
       "body": "<div class='callout warn'><p>Cả BCD và hex đều nhóm theo 4 bit, dễ nhầm lẫn. Khác biệt cốt lõi: hex 4-bit có đủ 16 giá trị hợp lệ (0-F), còn BCD 4-bit chỉ 10 giá trị hợp lệ (0-9) — luôn hỏi rõ ngữ cảnh (đây là địa chỉ/mã hex, hay chữ số thập phân/BCD) trước khi diễn giải một nhóm 4-bit.</p></div>"},
      {"title": "Áp dụng A320: vì sao MCDU nhập liệu bằng BCD",
       "body": "<p>Khi phi công nhập độ cao/tốc độ trên MCDU, bàn phím tạo ra mã BCD cho từng chữ số gõ vào — CPU chỉ cần tách nhóm 4-bit để biết chính xác từng chữ số, đơn giản hơn nhiều so với phải giải mã một số nhị phân nguyên khối rồi tách lại từng chữ số thập phân.</p>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>68 (thập phân) đổi sang BCD là gì? (Gợi ý: 6→0110, 8→1000). So khớp với đáp án trong bộ câu hỏi luyện tập ở cuối trang sau khi tự làm xong.</p></div>"},
    ],
    # ===== Phan 5: Ap dung tren Airbus A320 =====
    [
      {"title": "Toàn cảnh: một giá trị độ cao đi qua bao nhiêu hệ đếm?",
       "body": "<p>Cảm biến khí áp (analog) → ADC → nhị phân 16-bit trong ADIRU/FMGC → mã hoá BCD để hiển thị trên PFD → có thể ghi log bảo dưỡng ở hex nếu có lỗi cảm biến. MỘT giá trị vật lý duy nhất (độ cao) đi qua ít nhất 3 hệ đếm khác nhau trước khi tới mắt phi công/kỹ sư.</p>"},
      {"title": "Ví dụ từng bước: 10.000 ft biểu diễn nhị phân 16-bit",
       "body": "<p>10.000 (thập phân) → nhị phân: 10000×2=... (dùng phép chia liên tiếp đã học ở Phần 2) → kết quả 0010011100010000₂ (16-bit, đệm 0 ở đầu). Đây chính là dữ liệu thô mà FMGC xử lý nội bộ.</p>"},
      {"title": "Ví dụ: dữ liệu bus ARINC 429 hiển thị dạng hex trong log",
       "body": "<p>Một từ dữ liệu ARINC 429 32-bit khi ghi log bảo dưỡng được rút gọn thành 8 ký tự hex thay vì 32 ký tự nhị phân — kỹ sư đọc log nhanh hơn gấp nhiều lần, đúng ứng dụng thực tế của hex đã học ở Phần 3.</p>"},
      {"title": "Ví dụ: EGT hiển thị BCD trên ECAM",
       "body": "<p>Nhiệt độ khí xả động cơ (EGT), ví dụ 650°C, được mã hoá BCD (6-5-0) trước khi đưa ra driver hiển thị 7 đoạn trên ECAM — đúng nguyên lý BCD→7-segment đã học ở Phần 4, không cần mạch giải mã nhị phân→thập phân phức tạp.</p>"},
      {"title": "Bảng tổng hợp: hệ đếm nào dùng ở đâu trên A320",
       "body": "<table class='tt'><thead><tr><th>Vị trí trong hệ thống</th><th>Hệ đếm</th></tr></thead><tbody>"
               "<tr><td>Xử lý nội bộ FMGC/FWC/SDAC</td><td>Nhị phân</td></tr>"
               "<tr><td>Hiển thị EGT, N1, độ cao trên ECAM</td><td>BCD</td></tr>"
               "<tr><td>Mã lỗi BITE, log bảo dưỡng</td><td>Hex</td></tr>"
               "<tr><td>Một số trang trạng thái hệ thống cũ (MCDU STATUS)</td><td>Bát phân</td></tr></tbody></table>"},
      {"title": "Vì sao thợ bảo dưỡng không được phép làm tròn khi đọc hex",
       "body": "<p>Khác với số thập phân (làm tròn thường chấp nhận được), một mã lỗi hex đọc SAI DÙ CHỈ 1 KÝ TỰ (vd tra 0xACDE thay vì 0xACDF) sẽ dẫn tới tra cứu SAI hoàn toàn mã lỗi trong AMM — không có khái niệm 'gần đúng' khi làm việc với mã hex hệ thống.</p>"},
      {"title": "⚠️ Bẫy: đọc nhầm thứ tự byte (endianness) khi ghép hex",
       "body": "<div class='callout warn'><p>Một số hệ thống ghi log theo thứ tự byte đảo ngược (little-endian) so với thứ tự đọc trực quan (big-endian). Trước khi kết luận một mã lỗi hex, LUÔN kiểm tra tài liệu AMM của đúng hệ thống đó quy định thứ tự byte nào — không giả định mặc định.</p></div>"},
      {"title": "Case bổ sung: chuyển đổi bát phân cho trang STATUS cũ",
       "body": "<p>Một số MCDU thế hệ cũ hiển thị STATUS PAGE bằng mã bát phân 3 chữ số. Ví dụ mã 657₈ tương ứng nhị phân 110101111₂ — kỹ sư cần nhóm lại theo 3-bit đúng như đã học ở Phần 3 để tra cứu đúng ý nghĩa mã trạng thái.</p>"},
      {"title": "Vì sao đây là module NỀN TẢNG cho toàn bộ các module sau",
       "body": "<p>Module 02 (cổng logic) sẽ dùng lại bảng chân trị nhị phân; Module 03 (multiplexer) sẽ dùng địa chỉ chọn kênh dạng nhị phân/hex; Module 04 (CPU) sẽ dùng địa chỉ bộ nhớ hex và opcode nhị phân. Nắm chắc 4 hệ đếm ở đây là điều kiện bắt buộc để hiểu đúng 3 module tiếp theo.</p>"},
      {"title": "Tự kiểm tra tổng kết module (không chấm điểm)",
       "body": "<div class='callout good'><p>Trước khi làm quiz cuối trang: bạn có thể tự đổi một số bất kỳ qua đủ cả 4 hệ đếm (thập phân→nhị phân→bát phân→hex→BCD) mà không cần xem lại slide nào không? Nếu còn vướng bước nào, quay lại đúng phần tương ứng ở trên trước khi làm quiz.</p></div>"},
    ],
  ],
  "en": [
    # ===== Part 1 =====
    [
      {"title": "Why not just use decimal directly in electronic circuits?",
       "body": "<p>Digital electronic circuits can only reliably distinguish <b>two voltage levels</b> (high/low), not ten distinct levels needed for decimal digits. Hardware is therefore forced into binary (2 levels); every other number system (octal, hex, BCD) is simply a human-friendly shorthand for that same binary string.</p>"},
      {"title": "Four core number systems in avionics",
       "body": "<table class='tt'><thead><tr><th>System</th><th>Base</th><th>Digits used</th><th>Main role</th></tr></thead><tbody>"
               "<tr><td>Binary</td><td>2</td><td>0,1</td><td>Internal computer processing</td></tr>"
               "<tr><td>Octal</td><td>8</td><td>0-7</td><td>Compact system status codes</td></tr>"
               "<tr><td>Hexadecimal</td><td>16</td><td>0-9,A-F</td><td>Memory addresses, BITE fault codes</td></tr>"
               "<tr><td>BCD</td><td>—</td><td>4 bits/digit</td><td>Decimal display on screens</td></tr>"
               "</tbody></table>"},
      {"title": "Positional weighting — the principle shared by every base",
       "body": "<p>In any base-b system, the digit at position i (from the right, starting at 0) carries weight bⁱ. The value of the whole number equals the sum of (digit × weight).</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Value of a number in base b</div><div class='pd-formula-math'>N = Σ dᵢ·bⁱ</div></div>"},
      {"title": "Example: applying positional weight to a familiar decimal number",
       "body": "<p>528 (base 10) = 5·10² + 2·10¹ + 8·10⁰ = 500+20+8 = 528. This is exactly the same principle the course will re-apply to base 2, 8 and 16 — only the value of b changes.</p>"},
      {"title": "Why technicians don't read raw long binary strings",
       "body": "<p>A 16-bit memory address written in binary is 16 characters long (e.g. <code>1010110011110000</code>), easy to mistype or misread a single bit. Rewritten in hex it is only 4 characters (<code>ACF0</code>) — this reduces transcription error, a practical engineering reason, not just a theoretical one.</p>"},
      {"title": "The four systems are not independent — constant conversion is required",
       "body": "<ul><li>The computer PROCESSES in binary</li><li>The display SHOWS the pilot BCD/decimal</li><li>Maintenance logs RECORD fault codes in hex</li><li>Some legacy status pages use octal</li></ul><p>Maintenance engineers must be fluent converting in all four directions, not just one.</p>"},
      {"title": "⚠️ Trap: confusing a 'number system' with a 'unit of measure'",
       "body": "<div class='callout warn'><p>Beginners often confuse 10₁₆ (sixteen, base 16) with 10 (ten, base 10) because the digits look identical. Always mark the base subscript explicitly, as Tooley's convention shows: (75)₈, (75)₁₀, (75)₁₆ are THREE completely different values despite sharing the digits '7','5'.</p></div>"},
      {"title": "Application on the A320: why the FMGC must understand all four systems",
       "body": "<p>The FMGC (Flight Management Guidance Computer) receives binary sensor data, computes internally in binary, but must OUTPUT hex for maintenance logs, BCD for the MCDU display, and sometimes octal for status codes — one processing chip constantly converts between these systems in real time.</p>"},
      {"title": "Data flow diagram of a numeric value in the cockpit",
       "body": "<p>Sensor (analog) → ADC → binary (processed inside FMGC/FWC) → re-encoded as BCD/hex → shown on EFIS/ECAM or logged by BITE. Every arrow in this chain is a point where the active number system must be correctly identified.</p>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>Pause for 30 seconds: can you explain out loud why a maintenance engineer CANNOT learn just one number system and skip the other three? If unsure, revisit the first two slides before moving to Part 2.</p></div>"},
    ],
    # ===== Part 2 =====
    [
      {"title": "MSB, LSB and powers-of-two weighting",
       "body": "<p>In a binary number, the leftmost bit is the <b>MSB</b> (Most Significant Bit — highest weight), the rightmost bit is the <b>LSB</b> (Least Significant Bit — weight 2⁰=1).</p>"
               "<table class='tt'><thead><tr><th>2⁷</th><th>2⁶</th><th>2⁵</th><th>2⁴</th><th>2³</th><th>2²</th><th>2¹</th><th>2⁰</th></tr></thead>"
               "<tbody><tr><td>128</td><td>64</td><td>32</td><td>16</td><td>8</td><td>4</td><td>2</td><td>1</td></tr></tbody></table>"},
      {"title": "Worked example: binary → decimal",
       "body": "<p>Convert 11011010₂ to decimal — sum the weights of bits that are 1:</p><p>11011010 = 128+64+0+16+8+0+2+0 = <b>218</b></p><p>(This is Tooley's own worked example — only add weights where the bit is 1, skip positions with 0.)</p>"},
      {"title": "Worked example: decimal → binary by repeated division",
       "body": "<p>Convert 45 to binary by repeatedly dividing by 2, reading remainders bottom-up:</p>"
               "<table class='tt'><thead><tr><th>Division</th><th>Quotient</th><th>Remainder</th></tr></thead><tbody>"
               "<tr><td>45÷2</td><td>22</td><td>1</td></tr><tr><td>22÷2</td><td>11</td><td>0</td></tr>"
               "<tr><td>11÷2</td><td>5</td><td>1</td></tr><tr><td>5÷2</td><td>2</td><td>1</td></tr>"
               "<tr><td>2÷2</td><td>1</td><td>0</td></tr><tr><td>1÷2</td><td>0</td><td>1</td></tr></tbody></table>"
               "<p>Reading remainders bottom-up: <b>101101</b> (matches the result independently verified in notebook 01).</p>"},
      {"title": "A faster shortcut: sum weights 2ⁱ directly (no division needed)",
       "body": "<p>45 = 32+8+4+1 → mark 1 at exactly those four weight positions (32,8,4,1), 0 elsewhere → 101101. This shortcut is faster by hand, but the division method on the previous slide is the GENERAL method that also works for octal/hex.</p>"},
      {"title": "Binary addition — the carry rule",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>1-bit addition table</div><div class='pd-formula-math'>0+0=0 · 0+1=1 · 1+0=1 · 1+1=10 (carry 1)</div></div><p>Example: 0110 + 0101 = 1011 (6+5=11 — cross-check in decimal to confirm the carry rule was applied correctly).</p>"},
      {"title": "Negative numbers in binary: why two's complement is needed",
       "body": "<p>Pure binary has no minus sign. Negative numbers are represented using <b>two's complement</b>: invert every bit, then add 1. This is how a CPU performs subtraction using only an adder circuit.</p>"},
      {"title": "Worked example: two's complement of 10110",
       "body": "<p>Step 1 — invert bits: 10110 → 01001.</p><p>Step 2 — add 1: 01001 + 1 = <b>01010</b>.</p><p>(Matches the original Tooley Ch.2 Q3 — see the Module 01 quiz.)</p>"},
      {"title": "⚠️ Trap: forgetting the '+1' step after inverting",
       "body": "<div class='callout warn'><p>The most common error is inverting the bits and STOPPING there — that is <b>one's complement</b>, not two's complement. Always verify by adding the original number to its two's complement: if the sum overflows past the original bit width (e.g. 10110+01010=100000, drop the overflow bit → 00000), the result is correct.</p></div>"},
      {"title": "Application on the A320: why the ADIRU outputs signed binary data",
       "body": "<p>The ADIRU (Air Data Inertial Reference Unit) must represent both positive values (climbing altitude) and negative values (decreasing speed/negative pitch angle) — two's complement lets the FMGC add/subtract these using a single adder circuit, with no separate subtractor needed.</p>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>Try mentally: what is the two's complement of the 4-bit binary number 0110? (Hint: invert to 1001, add 1 → 1010.) If you got something else, review the two-step process above.</p></div>"},
    ],
    # ===== Part 3 =====
    [
      {"title": "Why octal groups 3 bits and hex groups 4 bits",
       "body": "<p>2³=8, so each octal digit represents exactly 3 bits; 2⁴=16, so each hex digit represents exactly 4 bits. This is NOT an arbitrary convention — it follows directly from the definition of the base itself.</p>"},
      {"title": "Quick reference table: binary ↔ hex (must be memorised)",
       "body": "<table class='tt'><thead><tr><th>Hex</th><th>Binary</th><th>Hex</th><th>Binary</th></tr></thead><tbody>"
               "<tr><td>0</td><td>0000</td><td>8</td><td>1000</td></tr><tr><td>1</td><td>0001</td><td>9</td><td>1001</td></tr>"
               "<tr><td>2</td><td>0010</td><td>A</td><td>1010</td></tr><tr><td>3</td><td>0011</td><td>B</td><td>1011</td></tr>"
               "<tr><td>4</td><td>0100</td><td>C</td><td>1100</td></tr><tr><td>5</td><td>0101</td><td>D</td><td>1101</td></tr>"
               "<tr><td>6</td><td>0110</td><td>E</td><td>1110</td></tr><tr><td>7</td><td>0111</td><td>F</td><td>1111</td></tr></tbody></table>"},
      {"title": "Worked example: binary → octal by grouping 3 bits",
       "body": "<p>Convert 100010001₂ to octal — group from the right in 3s: 100 | 010 | 001 → 4 2 1 → <b>421₈</b>. (Matches Tooley Ch.2 Q8.)</p>"},
      {"title": "Worked example: hex → octal MUST go through binary",
       "body": "<p>111₁₆ → expand each hex digit to 4 bits: 1→0001, 1→0001, 1→0001 → 000100010001₂.</p><p>Regroup in 3s from the right: 000 100 010 001 → 4 2 1 → <b>421₈</b>. You cannot infer hex→octal directly, skipping this step.</p>"},
      {"title": "Worked example: binary → hex by grouping 4 bits",
       "body": "<p>Convert 10110011₂ to hex — group in 4s: 1011 | 0011 → B | 3 → <b>B3₁₆</b>. (Matches Tooley Ch.2 Q11.)</p>"},
      {"title": "Padding with leading zeros when bit count isn't divisible",
       "body": "<p>Convert 111001110₂ (9 bits) to octal: 9 is already divisible by 3, so group directly: 111 001 110 → 7 1 6 → 716₈. Always count the bits first and pad with LEADING zeros if the count is not a multiple of the group size.</p>"},
      {"title": "Why hex dominates over octal in modern systems",
       "body": "<p>Most modern data buses (8/16/32-bit) are multiples of 4, so hex groups fit exactly with no padding, while octal (groups of 3) often misaligns with common bus widths. This is why hex dominates modern maintenance documentation over octal.</p>"},
      {"title": "⚠️ Trap: adding/subtracting hex digits as if they were decimal",
       "body": "<div class='callout warn'><p>Never add '9'+'9'=18 and write '18' into a hex result — hex only has 16 symbols (0-F). 9+9=18 (decimal) = 12₁₆, written as digit 2 with a carry of 1. Convert through decimal to add if you are not yet fluent with the hex addition table.</p></div>"},
      {"title": "Application on the A320: BITE fault codes are always shown as 4-digit hex",
       "body": "<p>A fault code such as <code>0xACDE</code> corresponds to exactly 16 bits of binary (4 hex digits × 4 bits). Technicians looking it up in the AMM don't need to count 16 individual bits — matching 4 hex characters is enough, drastically reducing misreading compared with a long binary string.</p>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>Without a calculator: what is 2F₁₆ in binary? (Hint: 2→0010, F→1111 → 00101111.) Check against the reference table at the start of this part if unsure.</p></div>"},
    ],
    # ===== Part 4 =====
    [
      {"title": "How is BCD different from pure binary?",
       "body": "<p>Pure binary converts the WHOLE number at once; BCD converts EACH decimal digit separately into 4 bits. BCD therefore always uses more bits than pure binary for the same value, in exchange for a trivially simple conversion to 7-segment display.</p>"},
      {"title": "Conversion table: 10 decimal digits ↔ BCD",
       "body": "<table class='tt'><thead><tr><th>Digit</th><th>BCD</th><th>Digit</th><th>BCD</th></tr></thead><tbody>"
               "<tr><td>0</td><td>0000</td><td>5</td><td>0101</td></tr><tr><td>1</td><td>0001</td><td>6</td><td>0110</td></tr>"
               "<tr><td>2</td><td>0010</td><td>7</td><td>0111</td></tr><tr><td>3</td><td>0011</td><td>8</td><td>1000</td></tr>"
               "<tr><td>4</td><td>0100</td><td>9</td><td>1001</td></tr></tbody></table>"},
      {"title": "Worked example: decimal → BCD",
       "body": "<p>Convert 37 to BCD — encode each digit separately: 3→0011, 7→0111 → concatenate <b>00110111</b>. (Matches Tooley Ch.2 Q5.)</p>"},
      {"title": "Worked example: BCD → decimal",
       "body": "<p>Convert 10010001 (BCD) to decimal — split into 4-bit groups from the right: 1001 | 0001 → 9 | 1 → <b>91</b>. (Matches Tooley Ch.2 Q4.)</p>"},
      {"title": "The 6 invalid BCD combinations",
       "body": "<p>4-bit BCD has 16 possible patterns (0000-1111) but only 10 (0000-1001) are valid. The six patterns 1010-1111 do NOT correspond to any decimal digit — if a BCD decoder circuit encounters these, it signals a hardware fault or data corruption.</p>"},
      {"title": "ASCII — encoding characters, not encoding a quantity",
       "body": "<p>Standard ASCII uses 7 bits, representing 128 characters (letters, digits, punctuation, control characters). Note: the ASCII code for the character '5' (0110101₂ = 35₁₆) is COMPLETELY DIFFERENT from the binary number representing the value 5 (00000101₂) — these are two independent encoding concepts.</p>"},
      {"title": "Example: the ASCII code for the letter 'A'",
       "body": "<p>'A' = 65 (decimal) = 41₁₆ = 1000001₂. The text string 'TCAS' is transmitted as 4 consecutive ASCII bytes, not as a single number.</p>"},
      {"title": "⚠️ Trap: confusing BCD with hex when looking at an isolated 4-bit group",
       "body": "<div class='callout warn'><p>Both BCD and hex group data in 4 bits, which is easy to confuse. The key difference: hex has all 16 valid 4-bit values (0-F), while BCD only has 10 valid values (0-9) — always ask what the context is (an address/hex value, or a decimal digit/BCD) before interpreting a 4-bit group.</p></div>"},
      {"title": "Application on the A320: why the MCDU keypad enters data in BCD",
       "body": "<p>When a pilot types an altitude/speed on the MCDU, the keypad generates a BCD code for each keystroke — the CPU only needs to split 4-bit groups to know each digit exactly, far simpler than decoding one large binary number and then splitting it back into decimal digits.</p>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>What is 68 (decimal) in BCD? (Hint: 6→0110, 8→1000.) Compare your answer with the practice question bank at the bottom of the page after trying it yourself.</p></div>"},
    ],
    # ===== Part 5 =====
    [
      {"title": "The full picture: how many number systems does one altitude value pass through?",
       "body": "<p>Barometric sensor (analog) → ADC → 16-bit binary inside the ADIRU/FMGC → BCD-encoded for the PFD display → possibly logged in hex if a sensor fault occurs. A SINGLE physical quantity (altitude) passes through at least 3 different number systems before reaching the pilot's/engineer's eyes.</p>"},
      {"title": "Worked example: 10,000 ft as a 16-bit binary value",
       "body": "<p>10,000 (decimal) → binary via repeated division (the method learned in Part 2) → result 0010011100010000₂ (16 bits, zero-padded). This is the raw data the FMGC processes internally.</p>"},
      {"title": "Example: ARINC 429 bus data shown in hex in maintenance logs",
       "body": "<p>A 32-bit ARINC 429 data word, when logged for maintenance, is shortened to 8 hex characters instead of 32 binary characters — engineers read the log far faster, a direct real application of the hex conversion learned in Part 3.</p>"},
      {"title": "Example: EGT shown as BCD on the ECAM",
       "body": "<p>Engine exhaust gas temperature (EGT), e.g. 650°C, is BCD-encoded (6-5-0) before being sent to the 7-segment display driver on the ECAM — exactly the BCD→7-segment principle learned in Part 4, avoiding a complex binary-to-decimal decoder.</p>"},
      {"title": "Summary table: which number system is used where on the A320",
       "body": "<table class='tt'><thead><tr><th>Location in the system</th><th>Number system</th></tr></thead><tbody>"
               "<tr><td>Internal processing in FMGC/FWC/SDAC</td><td>Binary</td></tr>"
               "<tr><td>EGT, N1, altitude display on ECAM</td><td>BCD</td></tr>"
               "<tr><td>BITE fault codes, maintenance logs</td><td>Hex</td></tr>"
               "<tr><td>Some legacy status pages (MCDU STATUS)</td><td>Octal</td></tr></tbody></table>"},
      {"title": "Why maintenance staff cannot round off when reading hex",
       "body": "<p>Unlike a decimal value (where rounding is often acceptable), a hex fault code read WRONG BY EVEN ONE CHARACTER (e.g. looking up 0xACDE instead of 0xACDF) leads to a COMPLETELY WRONG AMM lookup — there is no concept of 'close enough' when working with system hex codes.</p>"},
      {"title": "⚠️ Trap: misreading byte order (endianness) when assembling hex",
       "body": "<div class='callout warn'><p>Some systems log data in reversed byte order (little-endian) compared with the intuitive reading order (big-endian). Before concluding a hex fault code's meaning, ALWAYS check that specific system's AMM for the byte order it specifies — never assume a default.</p></div>"},
      {"title": "Extra case: octal conversion for a legacy STATUS page",
       "body": "<p>Some older-generation MCDUs display the STATUS PAGE using a 3-digit octal code. For example, code 657₈ corresponds to binary 110101111₂ — the engineer must regroup by 3 bits, exactly as learned in Part 3, to correctly look up the status meaning.</p>"},
      {"title": "Why this is the FOUNDATION module for everything that follows",
       "body": "<p>Module 02 (logic gates) will reuse binary truth tables; Module 03 (multiplexers) will use binary/hex channel-select addresses; Module 04 (CPU) will use hex memory addresses and binary opcodes. Mastering all four number systems here is a prerequisite for correctly understanding the next three modules.</p>"},
      {"title": "Final module self-check (ungraded)",
       "body": "<div class='callout good'><p>Before taking the quiz below: can you convert any given number through all four systems (decimal→binary→octal→hex→BCD) without looking back at any slide? If any step is still shaky, revisit that specific part above before starting the quiz.</p></div>"},
    ],
  ],
}
