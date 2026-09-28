# -*- coding: utf-8 -*-
"""Slide Module 01 (VI + EN): body + explain (giai thich cho nguoi moi) + img (anh goc tu bai giang)."""

SLIDES = {
 "vi": [
  [
   {
    "title": "Vì sao không dùng luôn hệ thập phân trong mạch điện tử?",
    "body": "<p>Mạch điện tử số chỉ phân biệt tin cậy được <b>hai mức điện áp</b> (cao/thấp), không thể phân biệt chính xác 10 mức điện áp khác nhau để biểu diễn 10 chữ số thập phân. Vì vậy phần cứng buộc phải dùng hệ nhị phân (2 mức), còn các hệ đếm khác (bát phân, hex, BCD) chỉ là cách con người viết gọn lại chuỗi nhị phân đó.</p>",
    "explain": "<p>Hãy hình dung một công tắc đèn: nó chỉ có hai trạng thái bật hoặc tắt, và ta phân biệt được ngay dù điện áp dao động nhẹ. Bây giờ hình dung công tắc có 10 nấc ứng với các chữ số 0 đến 9: chỉ cần nhiễu điện hoặc linh kiện xuống cấp, mạch có thể đọc nhầm nấc 4 thành nấc 5.</p><p>Vì thế kỹ sư thiết kế mạch số chỉ cho phép <b>hai mức điện áp</b> (thường 0V và 5V). Khoảng cách giữa hai mức đủ rộng để chịu nhiễu tốt. Bát phân, hex và BCD ở các phần sau <b>không phải</b> cách tính khác trong phần cứng, chúng chỉ là cách con người viết gọn lại đúng chuỗi nhị phân đó.</p>"
   },
   {
    "title": "Bốn hệ đếm cốt lõi trong avionics",
    "body": "<table class='tt'><thead><tr><th>Hệ đếm</th><th>Cơ số</th><th>Chữ số dùng</th><th>Vai trò chính</th></tr></thead><tbody><tr><td>Nhị phân</td><td>2</td><td>0,1</td><td>Xử lý bên trong máy tính</td></tr><tr><td>Bát phân</td><td>8</td><td>0-7</td><td>Mã trạng thái hệ thống gọn</td></tr><tr><td>Thập lục phân</td><td>16</td><td>0-9,A-F</td><td>Địa chỉ bộ nhớ, mã lỗi BITE</td></tr><tr><td>BCD</td><td>n/a</td><td>4 bit/chữ số</td><td>Hiển thị số thập phân trên màn hình</td></tr></tbody></table>",
    "explain": "<p>Hình trên trích từ slide bài giảng gốc, tóm tắt bốn hệ đếm của module cùng vai trò thật của từng hệ trên A320. Nhị phân là ngôn ngữ nội bộ của mọi máy tính (FMGC, FWC, SDAC). Bát phân viết gọn mã trạng thái trên vài trang MCDU đời cũ. Hex dùng cho địa chỉ bộ nhớ và mã lỗi BITE vì ngắn gọn, dễ tra. BCD là cầu nối để số nhị phân hiện thành các chữ số quen thuộc trên màn hình buồng lái.</p><p>Nếu mới học lần đầu, đừng cố nhớ từng chi tiết trong hình. Chỉ cần giữ ý chính: bốn hệ đếm, bốn vai trò, nhưng cùng mô tả <b>một</b> dữ liệu bên dưới.</p>",
    "img": "numsys_apps_p03.jpg"
   },
   {
    "title": "Trọng số vị trí: nguyên lý dùng chung cho MỌI hệ đếm",
    "body": "<p>Trong bất kỳ hệ đếm cơ số b nào, mỗi chữ số ở vị trí i (tính từ phải, bắt đầu từ 0) có trọng số bⁱ. Giá trị của cả số = tổng (chữ số × trọng số).</p><div class='pd-formula'><div class='pd-formula-label'>Giá trị của một số ở cơ số b</div><div class='pd-formula-math'>N = Σ dᵢ·bⁱ</div></div>",
    "explain": "<p>Đây là công thức tổng quát nhất của cả module, đúng cho mọi cơ số, nên hãy đọc chậm. \"Trọng số vị trí\" nghĩa là giá trị thật của một chữ số phụ thuộc vào việc nó đứng <b>ở đâu</b>. Trong số 528, chữ số 5 không đáng giá 5 mà đáng giá 500 vì nó đứng ở hàng trăm.</p><p>Công thức N = Σ dᵢ·bⁱ chỉ nói lại điều đó bằng ký hiệu. dᵢ là chữ số ở vị trí i (đếm từ phải sang, bắt đầu từ 0), b là cơ số, bⁱ là trọng số của vị trí, còn Σ nghĩa là \"cộng tất cả lại\". Slide sau sẽ dùng công thức này cho một số thập phân quen thuộc trước khi sang nhị phân.</p>"
   },
   {
    "title": "Ví dụ: áp dụng trọng số cho số thập phân quen thuộc",
    "body": "<p>Số 528 (hệ 10) = 5·10² + 2·10¹ + 8·10⁰ = 500+20+8 = 528. Đây chính là nguyên lý mà chương trình học sẽ áp dụng lại y hệt cho cơ số 2, 8, 16: chỉ đổi giá trị b.</p>",
    "explain": "<p>Ví dụ 528 = 5×10² + 2×10¹ + 8×10⁰ chỉ là cách viết tường minh của phép cộng 500+20+8 mà ai cũng đã học từ tiểu học. Điều mới duy nhất là bạn thấy nó khớp với công thức trọng số vừa học.</p><p>Hình đính kèm cho thấy hệ thập phân vẫn là thứ phi công và kỹ sư nhìn thấy hằng ngày trên EFIS, FMS và bảng trọng lượng máy bay. Lý do chỉ là con người quen đếm bằng mười ngón tay. Bên trong máy tính, mọi số này đã được đổi sang nhị phân trước khi tính, rồi đổi ngược lại thập phân chỉ để người đọc.</p>",
    "img": "numsys_apps_p09.jpg"
   },
   {
    "title": "Vì sao kỹ thuật viên KHÔNG đọc trực tiếp chuỗi nhị phân dài?",
    "body": "<p>Một địa chỉ bộ nhớ 16-bit viết ở nhị phân dài 16 ký tự (vd <code>1010110011110000</code>), rất dễ đọc nhầm hoặc chép sai 1 bit khi ghi tay. Viết lại ở hex chỉ còn 4 ký tự (<code>ACF0</code>): giảm sai sót thao tác, đây là lý do kỹ thuật thực dụng chứ không chỉ lý thuyết.</p>",
    "explain": "<p>Thử so sánh: chuỗi nhị phân 1010110011110000 dài 16 ký tự. Chép nhầm hoặc đọc nhầm <b>một</b> bit ở giữa là cả địa chỉ sai, và mắt người rất khó phát hiện lỗi trong một dãy toàn số 0 và 1 giống nhau.</p><p>Viết lại ở hex chỉ còn 4 ký tự (ACF0). Ít ký tự hơn thì ít cơ hội chép sai hơn, và mắt phân biệt các ký tự 0-9, A-F dễ hơn nhiều so với dãy 0 và 1. Đây là lý do thực dụng, không chỉ lý do toán học, khiến tài liệu bảo dưỡng luôn ghi địa chỉ và mã lỗi bằng hex.</p>"
   },
   {
    "title": "Bốn hệ đếm không tách rời: luôn phải quy đổi qua lại",
    "body": "<ul><li>Máy tính XỬ LÝ ở nhị phân</li><li>Màn hình HIỂN THỊ cho phi công ở BCD/thập phân</li><li>Tài liệu bảo dưỡng GHI LẠI mã lỗi ở hex</li><li>Một số trang trạng thái hệ thống cũ dùng bát phân</li></ul><p>Kỹ sư bảo dưỡng phải thành thạo quy đổi cả 4 chiều, không chỉ 1 chiều duy nhất.</p>",
    "explain": "<p>Sơ đồ tam giác đính kèm cho thấy không hệ đếm nào đứng một mình. Cả bốn hệ đều có mũi tên \"Conversion\" hai chiều nối với các hệ còn lại, nghĩa là kỹ sư phải đổi qua lại liên tục.</p><p>Trong hình, mỗi hệ có một số minh hoạ riêng: (9856)₁₀, (101010101)₂, (7537)₈ và (A89DE)₁₆. Đây là bốn số khác nhau, chỉ để cho thấy mỗi hệ dùng ký hiệu và chữ số riêng, và chỉ số nhỏ bên dưới cho biết cơ số. Bốn gạch đầu dòng bên cạnh nêu vai trò thật: máy tính xử lý ở nhị phân, màn hình hiển thị ở BCD hoặc thập phân, tài liệu bảo dưỡng ghi mã lỗi ở hex, một số trang trạng thái cũ dùng bát phân.</p>",
    "img": "numsys_conversion_diagram.png"
   },
   {
    "title": "⚠️ Bẫy: nhầm 'hệ đếm' với 'đơn vị đo'",
    "body": "<div class='callout warn'><p>Học viên mới thường nhầm 10₁₆ (mười sáu, hệ hex) với 10 (mười, hệ thập phân) vì cách viết giống hệt nhau. Luôn phải ghi rõ subscript cơ số khi trình bày, đúng quy ước trong sách Tooley: (75)₈, (75)₁₀, (75)₁₆ là BA giá trị hoàn toàn khác nhau dù cùng ba ký tự '7','5'.</p></div>",
    "explain": "<p>Đây là lỗi rất dễ mắc: thấy \"10\" và đọc ngay là \"mười\" theo thói quen. Nhưng 10₁₆ (đọc \"một không, hệ mười sáu\") có giá trị thật là 16, còn 10₂ có giá trị 2 và 10₈ có giá trị 8.</p><p>Ba số (75)₈, (75)₁₀, (75)₁₆ có ký tự giống hệt nhau nhưng là ba giá trị khác hẳn: 61, 75 và 117 ở hệ thập phân. Quy tắc sống còn: luôn ghi rõ chỉ số cơ số (₂, ₈, ₁₀, ₁₆) mỗi khi viết một số không thuộc hệ thập phân mặc định.</p>"
   },
   {
    "title": "Áp dụng A320: vì sao FMGC cần hiểu cả 4 hệ đếm",
    "body": "<p>FMGC (Flight Management Guidance Computer) nhận dữ liệu nhị phân từ cảm biến, tính toán nội bộ ở nhị phân, nhưng phải XUẤT RA hex cho log bảo dưỡng, BCD cho hiển thị MCDU, và đôi khi bát phân cho mã trạng thái: một chip xử lý số phải chuyển đổi qua lại liên tục giữa các hệ này trong thời gian thực.</p>",
    "explain": "<p>FMGC (Flight Management Guidance Computer) cho thấy bốn hệ đếm không phải lý thuyết suông. Nó nhận tín hiệu cảm biến đã số hoá thành nhị phân và làm mọi phép tính nội bộ bằng nhị phân, vì đó là ngôn ngữ duy nhất bộ vi xử lý hiểu.</p><p>Khi cần xuất kết quả ra ngoài, nó phải \"phiên dịch\" theo mục đích: hex cho log bảo dưỡng, BCD cho màn hình MCDU của phi công, đôi khi bát phân cho vài mã trạng thái cũ. Một con chip làm việc phiên dịch này hàng nghìn lần mỗi giây, theo thời gian thực.</p>"
   },
   {
    "title": "Sơ đồ luồng dữ liệu số trong buồng lái",
    "body": "<p>Cảm biến (analog) → ADC → nhị phân (xử lý trong FMGC/FWC) → mã hoá lại thành BCD/hex → hiển thị EFIS/ECAM hoặc ghi log BITE. Mỗi mũi tên trong chuỗi này là một điểm cần hiểu đúng hệ đếm đang dùng.</p>",
    "explain": "<p>Sơ đồ mô tả vòng đời của <b>một</b> giá trị đo, ví dụ áp suất khí quyển. Cảm biến tạo tín hiệu analog (điện áp biến thiên liên tục). Bộ ADC (Analog-to-Digital Converter) đổi tín hiệu đó thành chuỗi nhị phân rời rạc. FMGC hoặc FWC tính toán hoàn toàn bằng nhị phân. Kết quả cuối cùng được mã hoá lại thành BCD hoặc hex tuỳ nơi hiển thị (EFIS/ECAM) hay nơi ghi log (BITE).</p><p>Mỗi mũi tên là một phép đổi hệ đếm thật trong phần cứng. Nếu một bước đổi sai hệ đếm, giá trị phi công nhìn thấy sẽ sai theo.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Dừng lại 30 giây: bạn có thể giải thích bằng lời vì sao một kỹ sư bảo dưỡng KHÔNG thể chỉ học một hệ đếm duy nhất mà bỏ qua 3 hệ còn lại không? Nếu chưa chắc, xem lại 2 slide đầu trước khi sang Phần 2.</p></div>",
    "explain": "<p>Trước khi sang Phần 2, hãy tự giải thích bằng lời của mình, không nhìn slide: vì sao kỹ sư bảo dưỡng không thể chỉ học một hệ đếm rồi bỏ qua ba hệ còn lại?</p><p>Câu trả lời đầy đủ nên có ba ý. Máy tính bên trong luôn xử lý ở nhị phân. Màn hình cho phi công luôn hiện thập phân hoặc BCD dễ đọc. Tài liệu bảo dưỡng và log lỗi dùng hex vì gọn và ít sai khi tra cứu. Nếu bạn nói trôi chảy cả ba ý mà không cần đọc lại, bạn đã sẵn sàng cho Phần 2.</p>"
   }
  ],
  [
   {
    "title": "MSB, LSB và trọng số luỹ thừa của 2",
    "body": "<p>Trong số nhị phân, bit ngoài cùng bên trái là <b>MSB</b> (Most Significant Bit: trọng số lớn nhất), bit ngoài cùng bên phải là <b>LSB</b> (Least Significant Bit: trọng số 2⁰=1).</p><table class='tt'><thead><tr><th>2⁷</th><th>2⁶</th><th>2⁵</th><th>2⁴</th><th>2³</th><th>2²</th><th>2¹</th><th>2⁰</th></tr></thead><tbody><tr><td>128</td><td>64</td><td>32</td><td>16</td><td>8</td><td>4</td><td>2</td><td>1</td></tr></tbody></table>",
    "explain": "<p>MSB (Most Significant Bit) là bit có trọng số lớn nhất, LSB (Least Significant Bit) là bit có trọng số nhỏ nhất. Chúng giống \"hàng trăm\" và \"hàng đơn vị\" trong số thập phân. Trong số 110100, bit ngoài cùng bên trái (MSB) có trọng số 2⁵=32, bit ngoài cùng bên phải (LSB) có trọng số 2⁰=1.</p><p>Bảng luỹ thừa của 2 (1, 2, 4, 8, 16, 32, 64, 128) là \"bảng cửu chương\" của hệ nhị phân. Thuộc tám giá trị này, mọi phép đổi nhị phân sang thập phân ở các slide sau sẽ nhanh hơn nhiều.</p>"
   },
   {
    "title": "Ví dụ từng bước: đổi nhị phân → thập phân",
    "body": "<p>Đổi 11011010₂ sang thập phân: cộng đúng trọng số của các bit bằng 1:</p><p>11011010 = 128+64+0+16+8+0+2+0 = <b>218</b></p><p>(Đây chính là ví dụ gốc trong Tooley: chỉ cộng trọng số ở vị trí có bit 1, bỏ qua vị trí bit 0.)</p>",
    "explain": "<p>Quy tắc chỉ có một dòng: <b>cộng</b> trọng số của những vị trí có bit 1, bỏ qua hoàn toàn những vị trí có bit 0. Không trừ, không nhân, chỉ đơn giản là không cộng.</p><p>Với 11011010, các vị trí có bit 1 mang trọng số 128, 64, 16, 8 và 2. Hai vị trí bit 0 (trọng số 32 và 1) bị bỏ qua. Cộng lại: 128+64+16+8+2 = 218. Mẹo kiểm tra: đếm số bit 1 trong dãy gốc (ở đây là 5), rồi đếm số số hạng bạn đã cộng. Hai con số khác nhau nghĩa là bạn đã bỏ sót hoặc cộng thừa một trọng số.</p>"
   },
   {
    "title": "Ví dụ từng bước: đổi thập phân → nhị phân (chia liên tiếp)",
    "body": "<p>Đổi 45 sang nhị phân bằng chia liên tiếp cho 2, đọc số dư từ dưới lên:</p><table class='tt'><thead><tr><th>Phép chia</th><th>Thương</th><th>Dư</th></tr></thead><tbody><tr><td>45÷2</td><td>22</td><td>1</td></tr><tr><td>22÷2</td><td>11</td><td>0</td></tr><tr><td>11÷2</td><td>5</td><td>1</td></tr><tr><td>5÷2</td><td>2</td><td>1</td></tr><tr><td>2÷2</td><td>1</td><td>0</td></tr><tr><td>1÷2</td><td>0</td><td>1</td></tr></tbody></table><p>Đọc dư từ dưới lên: <b>101101</b> (khớp đúng kết quả đã kiểm chứng bằng code trong notebook 01).</p>",
    "explain": "<p>Cách này chạy ngược slide trước. Thay vì cộng trọng số, ta chia số thập phân cho 2 liên tiếp và ghi lại <b>số dư</b> (luôn là 0 hoặc 1) sau mỗi lần chia, dừng khi thương bằng 0.</p><p>Với 45: 45÷2 = 22 dư 1; 22÷2 = 11 dư 0; 11÷2 = 5 dư 1; 5÷2 = 2 dư 1; 2÷2 = 1 dư 0; 1÷2 = 0 dư 1. Chỗ dễ nhầm nhất là thứ tự đọc: phải đọc số dư <b>từ dưới lên</b> để ra 101101, vì số dư đầu tiên là bit nhỏ nhất (LSB) còn số dư cuối cùng là bit lớn nhất (MSB).</p>"
   },
   {
    "title": "Cách nhanh hơn: cộng trực tiếp trọng số 2ⁱ (không cần chia)",
    "body": "<p>45 = 32+8+4+1 → đánh dấu 1 vào đúng 4 vị trí trọng số 32,8,4,1, còn lại là 0 → 101101. Cách này nhanh hơn khi làm tay, nhưng cách chia liên tiếp ở slide trước là cách TỔNG QUÁT áp dụng được cho cả octal/hex.</p>",
    "explain": "<p>Cách này cũng là đảo ngược của phép đổi nhị phân sang thập phân: ta đi tìm những trọng số cộng lại đúng bằng số cho trước. Với 45, trừ dần trọng số lớn nhất còn vừa: 45-32 = 13, 13-8 = 5, 5-4 = 1, 1-1 = 0. Vậy các trọng số 32, 8, 4, 1 nhận bit 1, còn 64, 16, 2 nhận bit 0, ra 101101 khớp slide trước.</p><p>Cách này nhanh khi nhẩm số nhỏ. Nhưng phép chia liên tiếp mới là cách chắc chắn không bỏ sót, nhất là với số lớn hoặc khi thi có áp lực thời gian.</p>"
   },
   {
    "title": "Phép cộng nhị phân: quy tắc nhớ (carry)",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Bảng cộng 1 bit</div><div class='pd-formula-math'>0+0=0 · 0+1=1 · 1+0=1 · 1+1=10 (nhớ 1)</div></div><p>Ví dụ: 0110 + 0101 = 1011 (6+5=11, kiểm tra lại bằng thập phân để tự tin quy tắc nhớ đã áp dụng đúng).</p>",
    "explain": "<p>Bảng cộng nhị phân chỉ có bốn trường hợp cần nhớ (bảng cộng thập phân có tới 100 trường hợp): 0+0=0, 0+1=1, 1+0=1 và trường hợp đặc biệt 1+1=10, đọc là \"viết 0, nhớ 1\", giống hệt \"9+1=10, viết 0 nhớ 1\" trong thập phân.</p><p>Mạch điện tử làm đúng phép cộng này gọi là <b>half adder</b> (bộ cộng bán phần). Hình cho thấy nó chỉ cần hai cổng: cổng XOR cho ra tổng Σ = A⊕B (kết quả cộng, chưa tính nhớ), và cổng AND cho ra số nhớ Cout = AB. Cổng AND chỉ ra 1 khi cả hai đầu vào đều là 1, khớp đúng quy tắc 1+1 là trường hợp duy nhất sinh ra số nhớ. Bạn sẽ gặp lại XOR và AND ở Module 02.</p>",
    "img": "numsys_half_adder.png"
   },
   {
    "title": "Số âm trong nhị phân: vì sao cần bù hai",
    "body": "<p>Nhị phân thuần không có dấu trừ. Để biểu diễn số âm, hệ thống số dùng <b>bù hai (two's complement)</b>: đảo tất cả bit rồi cộng thêm 1. Đây là cách CPU thực hiện phép trừ chỉ bằng mạch cộng.</p>",
    "explain": "<p>Toán thông thường viết dấu trừ trước một số để chỉ số âm. Nhưng mạch điện tử chỉ có hai mức điện áp (0 và 1), không còn mức thứ ba để biểu diễn riêng dấu trừ.</p><p>Giải pháp của các kỹ sư thiết kế CPU là <b>bù hai</b> (two's complement): một quy tắc biến đổi bit sao cho việc cộng một số với bù hai của số khác cho ra đúng kết quả phép trừ. Nhờ đó CPU chỉ cần xây một mạch cộng duy nhất mà làm được cả cộng lẫn trừ, tiết kiệm đáng kể số linh kiện trong chip.</p>"
   },
   {
    "title": "Ví dụ từng bước: bù hai của 10110",
    "body": "<p>Bước 1: đảo bit: 10110 → 01001.</p><p>Bước 2: cộng 1: 01001 + 1 = <b>01010</b>.</p><p>(Khớp đúng câu hỏi gốc Tooley Ch.2 Q3: xem quiz Module 01.)</p>",
    "explain": "<p>Bù hai chỉ có hai bước, làm đúng thứ tự. Bước 1: đảo từng bit (0 thành 1, 1 thành 0), 10110 thành 01001. Bước 2: cộng thêm 1, 01001 + 1 = 01010. Vậy 01010 là bù hai của 10110, tức giá trị âm tương ứng.</p><p>Cách tự kiểm tra không cần tra bảng: cộng số gốc với kết quả, 10110 + 01010 = 100000. Bỏ bit tràn ở đầu còn 00000, nghĩa là bạn làm đúng, vì một số cộng với số âm của chính nó luôn bằng 0.</p>"
   },
   {
    "title": "⚠️ Bẫy: quên bước cộng 1 sau khi đảo bit",
    "body": "<div class='callout warn'><p>Lỗi phổ biến nhất khi tính bù hai là chỉ đảo bit rồi DỪNG LẠI: đó là <b>bù một (one's complement)</b>, không phải bù hai. Luôn kiểm tra lại bằng cách cộng số gốc với kết quả bù hai: nếu tổng tràn ra ngoài số bit ban đầu (vd 10110+01010=100000, bỏ bit tràn còn 00000), kết quả đúng.</p></div>",
    "explain": "<p>Đây là lỗi phổ biến nhất khi mới học bù hai: chỉ làm Bước 1 (đảo bit) rồi dừng, nghĩ rằng thế là xong. Kết quả đó gọi là <b>bù một</b> (one's complement), một khái niệm khác, không dùng để biểu diễn số âm trong hầu hết hệ thống hiện đại.</p><p>Bù một của 10110 chỉ là 01001, còn bù hai đúng phải là 01010. Cách phát hiện mình có quên bước cộng 1 không: luôn làm phép cộng kiểm tra ở slide trước. Nếu tổng không ra 0 (sau khi bỏ bit tràn), gần như chắc chắn bạn đã quên cộng 1.</p>"
   },
   {
    "title": "Áp dụng A320: vì sao ADIRU xuất dữ liệu nhị phân 2 chiều",
    "body": "<p>ADIRU (Air Data Inertial Reference Unit) phải biểu diễn cả giá trị dương (độ cao tăng) và âm (tốc độ giảm/góc nghiêng âm): bù hai cho phép FMGC cộng/trừ các giá trị này bằng đúng một mạch cộng nhị phân duy nhất, không cần mạch trừ riêng.</p>",
    "explain": "<p>ADIRU (Air Data Inertial Reference Unit) đo những giá trị có thể tăng hoặc giảm liên tục khi bay: độ cao tăng lúc leo, tốc độ giảm lúc hãm, góc chúc mũi dương hoặc âm. Nếu không có bù hai, hệ thống cần một mạch cộng cho số dương và một mạch trừ riêng cho số âm, phần cứng phức tạp gấp đôi.</p><p>Nhờ bù hai, FMGC chỉ cần <b>một</b> mạch cộng nhị phân để xử lý cả hai chiều tăng và giảm của mọi giá trị bay. Hình đính kèm cho thấy toàn bộ dữ liệu cảm biến trên A320 được xử lý theo nguyên lý nhị phân này.</p>",
    "img": "numsys_apps_p11.jpg"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Tự tính nhẩm: bù hai của số nhị phân 4-bit 0110 là gì? (Gợi ý: đảo thành 1001, cộng 1 → 1010). Nếu ra khác, xem lại 2 bước ở slide bù hai phía trên.</p></div>",
    "explain": "<p>Tự làm trước khi sang Phần 3: tìm bù hai của số 4-bit 0110, chưa nhìn gợi ý. Nhắc lại hai bước: đảo bit (0110 thành 1001), rồi cộng 1 (1001 + 1 = 1010).</p><p>Nếu bạn ra 1010, hãy kiểm tra bằng phép cộng: 0110 + 1010 = 10000, bỏ bit tràn còn 0000, đúng như mong đợi. Nếu ra kết quả khác, nhiều khả năng bạn dừng ở bước đảo bit (ra 1001) mà quên cộng 1, đúng cái bẫy của slide trước. Xem lại slide đó rồi thử lại.</p>"
   }
  ],
  [
   {
    "title": "Vì sao nhóm 3 bit cho octal, nhóm 4 bit cho hex?",
    "body": "<p>2³=8 nên mỗi chữ số bát phân biểu diễn đúng 3 bit; 2⁴=16 nên mỗi chữ số hex biểu diễn đúng 4 bit. Đây KHÔNG phải quy ước tuỳ ý: nó xuất phát trực tiếp từ định nghĩa cơ số.</p>",
    "explain": "<p>Câu trả lời nằm ở luỹ thừa. 2³ = 8 nghĩa là 3 bit biểu diễn được đúng 8 giá trị (000 đến 111), khớp chính xác với 8 chữ số bát phân (0 đến 7). Vì vậy mỗi chữ số bát phân tương ứng gọn đúng 3 bit. Tương tự, 2⁴ = 16 khớp với 16 ký hiệu hex (0-9 và A-F), nên mỗi chữ số hex tương ứng đúng 4 bit.</p><p>Đây không phải quy ước tuỳ tiện mà là hệ quả toán học. Nhóm sai số bit, ví dụ nhóm 3 bit rồi gán cho hex, sẽ cho kết quả sai ngay.</p>"
   },
   {
    "title": "Bảng tra nhanh: nhị phân ↔ hex (bắt buộc thuộc lòng)",
    "body": "<table class='tt'><thead><tr><th>Hex</th><th>Nhị phân</th><th>Hex</th><th>Nhị phân</th></tr></thead><tbody><tr><td>0</td><td>0000</td><td>8</td><td>1000</td></tr><tr><td>1</td><td>0001</td><td>9</td><td>1001</td></tr><tr><td>2</td><td>0010</td><td>A</td><td>1010</td></tr><tr><td>3</td><td>0011</td><td>B</td><td>1011</td></tr><tr><td>4</td><td>0100</td><td>C</td><td>1100</td></tr><tr><td>5</td><td>0101</td><td>D</td><td>1101</td></tr><tr><td>6</td><td>0110</td><td>E</td><td>1110</td></tr><tr><td>7</td><td>0111</td><td>F</td><td>1111</td></tr></tbody></table>",
    "explain": "<p>Bảng này là công cụ quan trọng nhất của Phần 3. Nó liệt kê đủ 16 giá trị hex và đúng 4 bit nhị phân của từng giá trị. Vì mỗi chữ số hex luôn ứng với một mẫu 4 bit cố định, bạn đổi bằng cách tra bảng, không cần tính gì thêm. Đó là lý do đổi nhị phân sang hex nhanh và ít sai hơn nhiều so với đi vòng qua thập phân.</p><p>Lời khuyên: chép tay bảng này vài lần cho tới khi nhớ được A=1010, B=1011, C=1100, D=1101, E=1110, F=1111. Sáu giá trị này là những chỗ người mới hay nhầm nhất.</p>"
   },
   {
    "title": "Ví dụ từng bước: nhị phân → bát phân bằng nhóm 3 bit",
    "body": "<p>Đổi 100010001₂ sang bát phân: nhóm từ phải sang trái theo 3 bit: 100 | 010 | 001 → 4 2 1 → <b>421₈</b>. (Khớp Tooley Ch.2 Q8.)</p>",
    "explain": "<p>Quy trình nhóm 3 bit áp dụng đúng nguyên lý 2³ = 8 ở slide đầu phần. Tách chuỗi 100010001 thành từng nhóm 3 bit, <b>bắt đầu từ bên phải</b>: 100 | 010 | 001. Tra từng nhóm ở bảng bát phân (000=0, 001=1, 010=2, ..., 111=7) được 4, 2, 1, ghép lại thành 421₈.</p><p>Lỗi hay gặp nhất là nhóm từ bên trái. Các nhóm bị lệch và kết quả sai hoàn toàn, nhất là khi tổng số bit không chia hết cho 3 (xem slide đệm số 0 ở phía sau).</p>"
   },
   {
    "title": "Ví dụ từng bước: hex → bát phân PHẢI qua nhị phân trung gian",
    "body": "<p>111₁₆ → nhị phân từng chữ số hex (4 bit/số): 1→0001, 1→0001, 1→0001 → 000100010001₂.</p><p>Nhóm lại theo 3 bit từ phải: 000 100 010 001 → 4 2 1 → <b>421₈</b>. Không thể suy trực tiếp hex→octal mà bỏ qua bước này.</p>",
    "explain": "<p>Không có công thức đổi thẳng từ hex sang bát phân. Bạn luôn phải đi qua nhị phân trung gian, gồm hai giai đoạn.</p><p>Giai đoạn 1: mở mỗi chữ số hex thành đúng 4 bit: 1→0001, 1→0001, 1→0001, ghép lại 000100010001. Giai đoạn 2: nhóm lại chuỗi đó theo 3 bit từ phải sang: 000 100 010 001, tức 4, 2, 1, ra 421₈. Nếu cố đoán tắt kiểu \"hex F ứng với chữ số bát phân nào\" mà bỏ bước trung gian, bạn gần như chắc chắn sai, vì hai hệ này không có quan hệ chia hết đơn giản với nhau.</p>"
   },
   {
    "title": "Ví dụ từng bước: nhị phân → hex bằng nhóm 4 bit",
    "body": "<p>Đổi 10110011₂ sang hex: nhóm 4 bit: 1011 | 0011 → B | 3 → <b>B3₁₆</b>. (Khớp Tooley Ch.2 Q11.)</p>",
    "explain": "<p>Nhóm 4 bit cho hex làm giống hệt nhóm 3 bit cho bát phân, chỉ khác kích thước nhóm. Tách 10110011 thành hai nhóm 4 bit từ bên phải: 1011 | 0011. Tra bảng hex được B (1011) và 3 (0011), ghép lại B3₁₆.</p><p>Mẹo nhớ nhanh: chữ B đứng sau A=10 một bậc, nên B = 11 = 1011 ở nhị phân. Khi quen bạn sẽ không phải tra bảng mọi lần. Nhớ luôn nhóm từ phải sang trái, giống lưu ý ở slide nhóm 3 bit.</p>"
   },
   {
    "title": "Đệm 0 ở đầu khi số bit không chia hết",
    "body": "<p>Đổi 111001110₂ (9 bit) sang octal: đệm thêm 0 ở đầu cho đủ bội số 3 → 011 100 111 0 → sai, phải đệm cho đủ 9→9 chia hết cho 3 rồi: 111 001 110 → 7 1 6 → 716₈. Luôn đếm số bit trước khi nhóm, đệm 0 bên TRÁI nếu thiếu.</p>",
    "explain": "<p>Trước khi nhóm bit, luôn đếm tổng số bit để biết có cần đệm số 0 hay không: bát phân cần bội số của 3, hex cần bội số của 4. Với 111001110 (đúng 9 bit, đã là bội của 3) thì nhóm thẳng: 111 001 110, tức 7, 1, 6, ra 716₈.</p><p>Nếu số bit không chia hết, ví dụ 7 bit mà nhóm theo 3, hãy thêm số 0 vào <b>đầu bên trái</b>, không phải bên phải. Thêm 0 bên trái không đổi giá trị, giống viết 007 thay cho 7 trong thập phân. Thêm 0 bên phải thì đổi hẳn giá trị của số.</p>"
   },
   {
    "title": "Vì sao hex phổ biến hơn octal trong hệ thống hiện đại",
    "body": "<p>Hầu hết bus dữ liệu hiện đại (8/16/32-bit) là bội số của 4, nên hex nhóm vừa khít không cần đệm; trong khi octal (nhóm 3) thường lệch với các độ rộng bus phổ biến. Đây là lý do hex chiếm ưu thế trong tài liệu bảo dưỡng hiện đại hơn octal.</p>",
    "explain": "<p>Bus dữ liệu trong máy tính và avionics hiện đại thường rộng 8, 16 hoặc 32 bit, đều là bội số của 4 nên chia hex vừa khít, nhưng không phải lúc nào cũng là bội số của 3. Ví dụ thanh ghi 16 bit chia thành đúng 4 nhóm hex, không thừa. Chia thành nhóm bát phân thì dư một bit lẻ phải đệm thêm, gây bất tiện khi lập trình hoặc đọc log.</p><p>Đó là lý do thực tế khiến hex dần thay bát phân trong tài liệu kỹ thuật và bảo dưỡng hiện đại, dù bát phân vẫn còn ở vài hệ thống cũ.</p>"
   },
   {
    "title": "⚠️ Bẫy: cộng/trừ trực tiếp các chữ số hex như thập phân",
    "body": "<div class='callout warn'><p>Không được cộng '9'+'9'=18 rồi viết '18' vào kết quả hex: hex chỉ có 16 ký hiệu (0-F). 9+9=18 (thập phân) = 12₁₆, viết là 2, nhớ 1. Luôn đổi qua thập phân để cộng rồi đổi ngược lại nếu chưa quen bảng cộng hex.</p></div>",
    "explain": "<p>Người quen cộng thập phân dễ mang thói quen đó sang hex: cộng 9+9 ra 18 rồi viết luôn \"18\" vào kết quả. Nhưng hex chỉ có 16 ký hiệu (0-9 và A-F), không có ký hiệu nào là \"18\".</p><p>Cách đúng: 9+9 = 18 ở thập phân, đổi 18 sang hex được 12₁₆ (vì 18 = 16+2). Vậy viết chữ số 2 ở vị trí đó và <b>nhớ 1</b> sang cột bên trái, đúng nguyên lý nhớ đã học ở phép cộng nhị phân. Khi chưa quen bảng cộng hex, cách an toàn là đổi các chữ số hex sang thập phân, cộng bình thường, rồi đổi kết quả về hex.</p>"
   },
   {
    "title": "Áp dụng A320: mã lỗi BITE luôn hiển thị ở hex 4 chữ số",
    "body": "<p>Một fault code kiểu <code>0xACDE</code> tương ứng đúng 16 bit nhị phân (4 chữ số hex × 4 bit). Kỹ sư tra cứu trong AMM không cần đếm 16 bit riêng lẻ: chỉ cần khớp đúng 4 ký tự hex, giảm mạnh khả năng đọc nhầm so với nhìn chuỗi nhị phân dài.</p>",
    "explain": "<p>BITE (Built-In Test Equipment) là hệ thống tự phát hiện lỗi trên máy bay. Mọi mã lỗi của nó được viết bằng 4 ký tự hex, ví dụ 0xACDE, vì 4 ký tự hex ứng đúng 16 bit nhị phân, đủ mã hoá hàng chục nghìn loại lỗi mà không cần một chuỗi số dài.</p><p>Khi tra mã trong tài liệu bảo dưỡng AMM (Aircraft Maintenance Manual), kỹ sư chỉ cần khớp đúng 4 ký tự hex, nhanh và ít nhầm hơn nhiều so với đếm và so 16 bit bằng mắt. Hình đính kèm cho thấy cả chuỗi ứng dụng thật: địa chỉ bộ nhớ, nhãn dữ liệu ARINC 429, mã lỗi bảo dưỡng, tất cả đều dùng hex vì cùng một lý do.</p>",
    "img": "numsys_apps_p17.jpg"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Không dùng máy tính: 2F₁₆ đổi sang nhị phân là gì? (Gợi ý: 2→0010, F→1111 → 00101111). Kiểm tra lại bằng bảng tra ở slide đầu phần này nếu chưa chắc.</p></div>",
    "explain": "<p>Bài tự kiểm tra: đổi 2F₁₆ sang nhị phân mà không dùng máy tính và không tra bảng. Cách làm: tách hai chữ số hex, đổi chữ số 2 thành 0010, đổi chữ số F thành 1111 (F là giá trị lớn nhất của hex nên toàn bit 1), rồi ghép hai nhóm đúng thứ tự: 00101111.</p><p>Nếu ra kết quả khác, quay lại bảng tra nhanh ở đầu Phần 3 để xem bạn nhớ sai nhóm bit nào, rồi thử một ví dụ tương tự cho tới khi làm được mà không cần tra.</p>"
   }
  ],
  [
   {
    "title": "BCD khác nhị phân thuần ở điểm nào?",
    "body": "<p>Nhị phân thuần đổi CẢ SỐ cùng lúc; BCD đổi TỪNG CHỮ SỐ THẬP PHÂN riêng biệt thành 4 bit. Vì vậy BCD luôn dùng nhiều bit hơn nhị phân thuần cho cùng một giá trị, đổi lại việc chuyển sang hiển thị 7 đoạn cực kỳ đơn giản.</p>",
    "explain": "<p>Khác biệt cốt lõi là <b>đơn vị được đổi</b>. Nhị phân thuần coi cả con số là một khối và đổi một lần (45 thành 101101). BCD tách con số thành từng chữ số thập phân rồi đổi mỗi chữ số thành đúng 4 bit.</p><p>Với 45, nhị phân thuần cho 101101 (6 bit), còn BCD cho 0100 0101 (8 bit, ghép từ 4→0100 và 5→0101). Vậy BCD luôn tốn nhiều bit hơn cho cùng giá trị. Đổi lại, khi điều khiển màn hình 7 đoạn, BCD chỉ cần một mạch giải mã đơn giản cho mỗi nhóm 4 bit. Nhị phân thuần cần mạch phức tạp hơn nhiều để tách lại từng chữ số thập phân.</p>"
   },
   {
    "title": "Bảng chuyển đổi 10 chữ số thập phân ↔ BCD",
    "body": "<table class='tt'><thead><tr><th>Chữ số</th><th>BCD</th><th>Chữ số</th><th>BCD</th></tr></thead><tbody><tr><td>0</td><td>0000</td><td>5</td><td>0101</td></tr><tr><td>1</td><td>0001</td><td>6</td><td>0110</td></tr><tr><td>2</td><td>0010</td><td>7</td><td>0111</td></tr><tr><td>3</td><td>0011</td><td>8</td><td>1000</td></tr><tr><td>4</td><td>0100</td><td>9</td><td>1001</td></tr></tbody></table>",
    "explain": "<p>Bảng chỉ có đúng 10 tổ hợp, ứng với 10 chữ số thập phân. Bảng hex ở Phần 3 có tới 16 tổ hợp. Đây chính là khác biệt cốt lõi giữa BCD và hex, sẽ được nhắc lại ở slide \"bẫy\" phía sau.</p><p>Bảng này dễ thuộc vì nó trùng với cách đếm nhị phân thông thường từ 0000 đến 1001, chỉ dừng sớm hơn. Nhị phân 4 bit đếm được tới 1111 = 15, còn BCD dừng ở 1001 = 9. Nhớ điểm dừng này là cách nhanh nhất để nhận ra một tổ hợp có phải BCD hợp lệ hay không.</p>"
   },
   {
    "title": "Ví dụ từng bước: thập phân → BCD",
    "body": "<p>Đổi 37 sang BCD: tách riêng từng chữ số: 3→0011, 7→0111 → ghép lại <b>00110111</b>. (Khớp Tooley Ch.2 Q5.)</p>",
    "explain": "<p>Quy trình chỉ có một bước: tách từng chữ số thập phân, rồi đổi mỗi chữ số thành 4 bit theo bảng ở slide trước. Không cần tính toán như khi đổi sang nhị phân thuần.</p><p>Với 37: chữ số 3 thành 0011, chữ số 7 thành 0111, ghép đúng thứ tự (hàng chục trước, hàng đơn vị sau) được 00110111. Lưu ý đây <b>không</b> phải đổi 37 sang nhị phân thuần (kết quả sẽ là 100101, chỉ 6 bit). Hai cách đổi phục vụ hai mục đích khác nhau, đừng nhầm.</p>"
   },
   {
    "title": "Ví dụ từng bước: BCD → thập phân",
    "body": "<p>Đổi 10010001 (BCD) sang thập phân: tách nhóm 4 bit từ phải: 1001 | 0001 → 9 | 1 → <b>91</b>. (Khớp Tooley Ch.2 Q4.)</p>",
    "explain": "<p>Quy trình đảo ngược slide trước. Từ một chuỗi bit BCD, việc đầu tiên là tách thành các nhóm đúng 4 bit bắt đầu từ bên phải, giống cách nhóm cho hex. Sau đó tra bảng để đổi mỗi nhóm thành một chữ số thập phân.</p><p>Với 10010001: tách thành 1001 | 0001, tra ra 9 và 1, ghép đúng thứ tự thành 91. Nếu khi tách nhóm bạn gặp một nhóm nằm ngoài khoảng 0000 đến 1001 (ví dụ 1010 hay 1111), chuỗi đó không phải BCD hợp lệ. Slide tiếp theo nói rõ hơn về các tổ hợp này.</p>"
   },
   {
    "title": "6 tổ hợp KHÔNG hợp lệ trong BCD",
    "body": "<p>BCD 4-bit có 16 tổ hợp khả dĩ (0000-1111) nhưng chỉ 10 tổ hợp (0000-1001) hợp lệ. Sáu tổ hợp 1010-1111 KHÔNG tương ứng chữ số thập phân nào: nếu mạch giải mã BCD gặp các mã này, đó là dấu hiệu lỗi phần cứng/nhiễu dữ liệu.</p>",
    "explain": "<p>Với 4 bit có thể tạo 2⁴ = 16 tổ hợp (0000 đến 1111), nhưng BCD chỉ dùng 10 tổ hợp đầu (0000 đến 1001) cho 10 chữ số thập phân. Sáu tổ hợp còn lại (1010, 1011, 1100, 1101, 1110, 1111) không có nghĩa gì trong BCD.</p><p>Điều này không vô hại. Nếu mạch xử lý BCD, ví dụ bộ giải mã 7 đoạn, nhận phải một trong sáu tổ hợp \"rác\" đó, chắc chắn có lỗi phần cứng, nhiễu tín hiệu hoặc dữ liệu hỏng khi truyền. Nhiều hệ thống tự kiểm tra (BITE) trên máy bay tận dụng chính đặc điểm này để phát hiện dữ liệu BCD bị lỗi.</p>"
   },
   {
    "title": "ASCII: mã hoá ký tự, không phải mã hoá số lượng",
    "body": "<p>ASCII chuẩn dùng 7 bit, biểu diễn 128 ký tự (chữ, số, dấu câu, ký tự điều khiển). Lưu ý: ASCII của ký tự '5' (mã 0110101₂ = 35₁₆) KHÁC HOÀN TOÀN với số nhị phân của giá trị 5 (00000101₂): đây là hai khái niệm mã hoá độc lập.</p>",
    "explain": "<p>Cần phân biệt hai khái niệm hay bị gộp nhầm. Mã hoá <b>số lượng</b> (nhị phân, BCD) cho biết có bao nhiêu. Mã hoá <b>ký tự</b> (ASCII) cho biết đó là chữ cái, chữ số dạng văn bản, dấu câu hay lệnh điều khiển nào.</p><p>ASCII chuẩn dùng 7 bit, đủ mã hoá 2⁷ = 128 ký tự, gồm chữ hoa, chữ thường, chữ số và các ký tự điều khiển không nhìn thấy (xuống dòng, tab). Điểm dễ nhầm nhất: mã ASCII của <b>ký tự</b> '5' là 0110101₂, hoàn toàn khác số nhị phân của <b>giá trị</b> 5 là 00000101₂. Một cái mô tả hình dạng ký tự để hiển thị, một cái mô tả số lượng để tính toán.</p>"
   },
   {
    "title": "Ví dụ: mã ASCII của ký tự 'A'",
    "body": "<p>'A' = 65 (thập phân) = 41₁₆ = 1000001₂. Chuỗi văn bản 'TCAS' được truyền đi dưới dạng 4 byte ASCII liên tiếp, không phải một con số duy nhất.</p>",
    "explain": "<p>Ví dụ cụ thể cho ký tự 'A': mã ASCII ở thập phân là 65, đổi sang hex là 41₁₆, đổi sang nhị phân là 1000001₂ (đúng 7 bit theo chuẩn ASCII).</p><p>Khi hệ thống truyền chuỗi 'TCAS' (Traffic Collision Avoidance System), nó không gửi một con số duy nhất cho cả từ mà gửi lần lượt 4 byte ASCII, mỗi byte ứng với một ký tự T, C, A, S. Vì vậy, khi xem dữ liệu thô trong công cụ debug, bạn có thể thấy dãy hex 54 43 41 53 và cần biết đó là chữ 'TCAS' chứ không phải một số nhị phân đơn lẻ.</p>"
   },
   {
    "title": "⚠️ Bẫy: nhầm BCD với hex khi nhìn 4-bit đơn lẻ",
    "body": "<div class='callout warn'><p>Cả BCD và hex đều nhóm theo 4 bit, dễ nhầm lẫn. Khác biệt cốt lõi: hex 4-bit có đủ 16 giá trị hợp lệ (0-F), còn BCD 4-bit chỉ 10 giá trị hợp lệ (0-9): luôn hỏi rõ ngữ cảnh (đây là địa chỉ/mã hex, hay chữ số thập phân/BCD) trước khi diễn giải một nhóm 4-bit.</p></div>",
    "explain": "<p>BCD và hex đều nhóm dữ liệu theo cụm 4 bit, nên nhìn thoáng qua rất dễ nhầm. Nhóm 0111 thì cả hai cách đọc đều ra 7, nên chưa lộ vấn đề. Nhưng thử nhóm 1100: đó là chữ 'C' hợp lệ ở hex, còn ở BCD nó là tổ hợp không hợp lệ.</p><p>Khác biệt cốt lõi: hex có đủ 16 giá trị hợp lệ (0 đến F), BCD chỉ có 10 giá trị hợp lệ (0 đến 9), sáu giá trị còn lại là rác. Quy tắc an toàn: trước khi diễn giải một nhóm 4 bit, luôn xác định ngữ cảnh từ tài liệu đi kèm (đây là địa chỉ hex hay chữ số BCD), đừng đoán theo hình dạng của bit.</p>"
   },
   {
    "title": "Áp dụng A320: vì sao MCDU nhập liệu bằng BCD",
    "body": "<p>Khi phi công nhập độ cao/tốc độ trên MCDU, bàn phím tạo ra mã BCD cho từng chữ số gõ vào: CPU chỉ cần tách nhóm 4-bit để biết chính xác từng chữ số, đơn giản hơn nhiều so với phải giải mã một số nhị phân nguyên khối rồi tách lại từng chữ số thập phân.</p>",
    "explain": "<p>Khi phi công gõ số trên bàn phím MCDU (Multi-purpose Control and Display Unit) để nhập độ cao hay tốc độ, mỗi phím số tạo ra một mã BCD 4 bit của đúng chữ số đó, chứ không mã hoá cả con số thành nhị phân thuần ngay từ đầu.</p><p>Lợi ích thực tế: bộ xử lý chỉ cần tách các nhóm 4 bit là biết chính xác từng chữ số phi công đã gõ. Cách này đơn giản hơn nhiều so với việc nhận một số nhị phân nguyên khối rồi chạy thuật toán tách lại từng chữ số thập phân. Hình đính kèm cho thấy quy trình đó: phi công nhập 350 trên MCDU, và từng chữ số được mã hoá BCD (3→0011, 5→0101, 0→0000).</p>",
    "img": "numsys_apps_p25.jpg"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>68 (thập phân) đổi sang BCD là gì? (Gợi ý: 6→0110, 8→1000). So khớp với đáp án trong bộ câu hỏi luyện tập ở cuối trang sau khi tự làm xong.</p></div>",
    "explain": "<p>Bài luyện: đổi 68 (thập phân) sang BCD mà không nhìn bảng. Tách hai chữ số 6 và 8, đổi từng chữ số (6→0110, 8→1000), ghép theo đúng thứ tự (hàng chục trước) được 01101000.</p><p>Đây là bước luyện cuối của Phần 4 trước khi bạn làm bộ trắc nghiệm cuối trang. Nếu làm trôi chảy, bạn đã nắm bốn phần lý thuyết (thập phân, nhị phân, bát phân và hex, BCD và ASCII) và sẵn sàng cho Phần 5, nơi tổng hợp mọi thứ qua các ví dụ thật trên A320.</p>"
   }
  ],
  [
   {
    "title": "Toàn cảnh: một giá trị độ cao đi qua bao nhiêu hệ đếm?",
    "body": "<p>Cảm biến khí áp (analog) → ADC → nhị phân 16-bit trong ADIRU/FMGC → mã hoá BCD để hiển thị trên PFD → có thể ghi log bảo dưỡng ở hex nếu có lỗi cảm biến. MỘT giá trị vật lý duy nhất (độ cao) đi qua ít nhất 3 hệ đếm khác nhau trước khi tới mắt phi công/kỹ sư.</p>",
    "explain": "<p>Slide này gom bốn phần đã học thành một câu chuyện liền mạch. Hãy theo dõi một giá trị độ cao từ lúc sinh ra tới lúc hiển thị. Cảm biến khí áp tạo tín hiệu analog liên tục. Bộ ADC lấy mẫu và số hoá nó thành chuỗi nhị phân 16 bit. Trong ADIRU và FMGC, chuỗi nhị phân được tính toán và hiệu chỉnh. Cuối cùng kết quả được mã hoá lại thành BCD để hiện đúng các chữ số quen thuộc trên màn hình PFD (Primary Flight Display) cho phi công.</p><p>Nếu cảm biến lỗi, hệ thống còn ghi thêm một dòng log bằng mã hex để kỹ sư tra cứu sau. Một giá trị vật lý, ít nhất ba hệ đếm khác nhau.</p>"
   },
   {
    "title": "Ví dụ từng bước: 10.000 ft biểu diễn nhị phân 16-bit",
    "body": "<p>10.000 (thập phân) → nhị phân bằng phép chia liên tiếp cho 2 đã học ở Phần 2: 10000, 5000, 2500, 1250, 625, 312, 156, 78, 39, 19, 9, 4, 2, 1, 0. Đọc số dư từ dưới lên và đệm 0 ở đầu cho đủ 16 bit → <b>0010011100010000₂</b>. Đây chính là dữ liệu thô mà FMGC xử lý nội bộ.</p>",
    "explain": "<p>Đây là bài tổng hợp dùng lại phép chia liên tiếp cho 2 của Phần 2: đổi 10000 (feet) sang nhị phân. Kết quả 16 bit là 0010011100010000, đã đệm số 0 ở đầu cho đủ 16 bit vì thanh ghi máy tính hàng không thường có độ rộng cố định là bội số của 8.</p><p>Cách kiểm tra nhanh bằng hex: nhóm 4 bit được 0010 | 0111 | 0001 | 0000, tức 2710₁₆, và 2710₁₆ = 2×4096 + 7×256 + 1×16 = 10000. Chuỗi bit này là dữ liệu thô mà FMGC lưu và tính bên trong, khác hẳn con số 10000 quen mắt trên màn hình, vốn đã được mã hoá lại sang BCD trước khi hiển thị.</p>"
   },
   {
    "title": "Ví dụ: dữ liệu bus ARINC 429 hiển thị dạng hex trong log",
    "body": "<p>Một từ dữ liệu ARINC 429 32-bit khi ghi log bảo dưỡng được rút gọn thành 8 ký tự hex thay vì 32 ký tự nhị phân: kỹ sư đọc log nhanh hơn gấp nhiều lần, đúng ứng dụng thực tế của hex đã học ở Phần 3.</p>",
    "explain": "<p>ARINC 429 là chuẩn truyền dữ liệu phổ biến trên máy bay, mỗi từ dữ liệu dài đúng 32 bit. Ghi nguyên 32 ký tự nhị phân vào log bảo dưỡng thì một trang sẽ đầy chữ số 0 và 1 rất khó đọc.</p><p>Vì vậy hệ thống nhóm theo từng 4 bit (đúng nguyên lý ở Phần 3) để rút còn 8 ký tự hex. Kỹ sư đọc 8 ký tự hex nhanh hơn nhiều so với đếm và so khớp 32 bit, và cũng ít đọc nhầm hơn, đúng lý do thực dụng đã nêu ở slide \"vì sao kỹ thuật viên không đọc chuỗi nhị phân dài\" trong Phần 1.</p>"
   },
   {
    "title": "Ví dụ: EGT hiển thị BCD trên ECAM",
    "body": "<p>Nhiệt độ khí xả động cơ (EGT), ví dụ 650°C, được mã hoá BCD (6-5-0) trước khi đưa ra driver hiển thị 7 đoạn trên ECAM: đúng nguyên lý BCD→7-segment đã học ở Phần 4, không cần mạch giải mã nhị phân→thập phân phức tạp.</p>",
    "explain": "<p>EGT (Exhaust Gas Temperature, nhiệt độ khí xả động cơ) là ví dụ hoàn hảo cho nguyên lý BCD sang màn hình 7 đoạn. Giá trị 650°C được tách thành ba chữ số 6, 5, 0, mỗi chữ số đổi sang BCD (6→0110, 5→0101, 0→0000). Mỗi nhóm 4 bit này đi thẳng vào một mạch giải mã 7 đoạn đơn giản để bật đúng các đoạn cần thiết trên màn hình ECAM.</p><p>Nếu ở bước này hệ thống dùng nhị phân thuần thay vì BCD, sẽ cần mạch phức tạp hơn nhiều để tách lại từng chữ số thập phân. Đó là lý do BCD vẫn được ưa chuộng cho hiển thị dù tốn nhiều bit hơn.</p>"
   },
   {
    "title": "Bảng tổng hợp: hệ đếm nào dùng ở đâu trên A320",
    "body": "<table class='tt'><thead><tr><th>Vị trí trong hệ thống</th><th>Hệ đếm</th></tr></thead><tbody><tr><td>Xử lý nội bộ FMGC/FWC/SDAC</td><td>Nhị phân</td></tr><tr><td>Hiển thị EGT, N1, độ cao trên ECAM</td><td>BCD</td></tr><tr><td>Mã lỗi BITE, log bảo dưỡng</td><td>Hex</td></tr><tr><td>Một số trang trạng thái hệ thống cũ (MCDU STATUS)</td><td>Bát phân</td></tr></tbody></table>",
    "explain": "<p>Bảng gom bốn kết luận từ bốn phần trước vào một chỗ để bạn nhìn toàn cảnh. Nhị phân dùng cho mọi phép tính nội bộ vì phần cứng chỉ hiểu hai mức điện áp. BCD dùng khi cần hiển thị số quen thuộc (EGT, N1, độ cao) cho phi công. Hex dùng cho mã lỗi và log bảo dưỡng vì gọn, ít sai khi tra. Bát phân chỉ còn ở vài trang trạng thái cũ.</p><p>Hãy coi bảng này như bản đồ tra nhanh. Gặp một con số lạ trong tài liệu kỹ thuật, trước tiên xác định nó xuất hiện ở <b>vị trí nào</b> trong hệ thống, từ đó suy ra hệ đếm nhiều khả năng đang được dùng.</p>"
   },
   {
    "title": "Vì sao thợ bảo dưỡng không được phép làm tròn khi đọc hex",
    "body": "<p>Khác với số thập phân (làm tròn thường chấp nhận được), một mã lỗi hex đọc SAI DÙ CHỈ 1 KÝ TỰ (vd tra 0xACDE thay vì 0xACDF) sẽ dẫn tới tra cứu SAI hoàn toàn mã lỗi trong AMM: không có khái niệm 'gần đúng' khi làm việc với mã hex hệ thống.</p>",
    "explain": "<p>Với số thập phân thường, làm tròn 250,4 thành 250 hiếm khi gây hậu quả nghiêm trọng. Mã lỗi hex thì khác. Nếu kỹ sư đọc nhầm 0xACDE thành 0xACDF (chỉ sai ký tự cuối), khi tra AMM hai mã này có thể chỉ hai lỗi hoàn toàn khác nhau.</p><p>Hậu quả là sửa nhầm bộ phận, tốn thời gian và chi phí, và điều quan trọng nhất là lỗi thật vẫn chưa được khắc phục. Vì vậy quy trình bảo dưỡng luôn yêu cầu chép lại nguyên vẹn mọi ký tự của mã hex, không được ước lượng hay làm tròn.</p>"
   },
   {
    "title": "⚠️ Bẫy: đọc nhầm thứ tự byte (endianness) khi ghép hex",
    "body": "<div class='callout warn'><p>Một số hệ thống ghi log theo thứ tự byte đảo ngược (little-endian) so với thứ tự đọc trực quan (big-endian). Trước khi kết luận một mã lỗi hex, LUÔN kiểm tra tài liệu AMM của đúng hệ thống đó quy định thứ tự byte nào: không giả định mặc định.</p></div>",
    "explain": "<p>\"Endianness\" là thứ tự byte khi lưu hoặc truyền một giá trị nhiều byte. Hệ big-endian lưu byte có trọng số lớn nhất trước, khớp với thứ tự đọc thông thường của con người. Hệ little-endian lưu byte có trọng số nhỏ nhất trước, ngược với trực giác.</p><p>Nếu kỹ sư quen đọc kiểu big-endian nhưng hệ thống ghi log kiểu little-endian, việc ghép các byte hex theo thứ tự sai sẽ ra một mã lỗi khác hẳn mã thật, và dẫn tới tra sai trong AMM như ở slide trước. Quy tắc an toàn: không bao giờ giả định thứ tự byte, hãy kiểm tra tài liệu kỹ thuật của đúng hệ thống đang xử lý.</p>"
   },
   {
    "title": "Case bổ sung: chuyển đổi bát phân cho trang STATUS cũ",
    "body": "<p>Một số MCDU thế hệ cũ hiển thị STATUS PAGE bằng mã bát phân 3 chữ số. Ví dụ mã 657₈ tương ứng nhị phân 110101111₂: kỹ sư cần nhóm lại theo 3-bit đúng như đã học ở Phần 3 để tra cứu đúng ý nghĩa mã trạng thái.</p>",
    "explain": "<p>Dù hex đã thay bát phân ở phần lớn hệ thống hiện đại, một số MCDU đời cũ vẫn hiển thị mã trạng thái bằng bát phân vì được thiết kế từ nhiều thập kỷ trước. Hình đính kèm cho thấy những ứng dụng bát phân kiểu này trên A320.</p><p>Với mã 657₈, dùng bảng bát phân sang nhị phân đã học (6→110, 5→101, 7→111), ghép lại được 110101111₂, chuỗi bit thật mà hệ thống xử lý bên trong. Bài học thực tế: kỹ sư làm việc trên máy bay đời cũ vẫn cần thành thạo cả bát phân lẫn hex.</p>",
    "img": "numsys_apps_p21.jpg"
   },
   {
    "title": "Vì sao đây là module NỀN TẢNG cho toàn bộ các module sau",
    "body": "<p>Module 02 (cổng logic) sẽ dùng lại bảng chân trị nhị phân; Module 03 (multiplexer) sẽ dùng địa chỉ chọn kênh dạng nhị phân/hex; Module 04 (CPU) sẽ dùng địa chỉ bộ nhớ hex và opcode nhị phân. Nắm chắc 4 hệ đếm ở đây là điều kiện bắt buộc để hiểu đúng 3 module tiếp theo.</p>",
    "explain": "<p>Nhìn trước một chút. Module 02 về cổng logic sẽ liên tục dùng bảng chân trị viết bằng 0 và 1 để mô tả đầu vào, đầu ra của cổng AND, OR, NOT. Module 03 về bộ dồn kênh sẽ dùng địa chỉ chọn kênh dạng nhị phân hoặc hex. Module 04 về CPU sẽ dùng địa chỉ bộ nhớ dạng hex và mã lệnh dạng nhị phân.</p><p>Nếu bốn hệ đếm và các phép đổi qua lại chưa vững, bạn sẽ vấp ngay từ đầu Module 02, vì mọi ví dụ ở đó mặc định bạn đọc và viết nhị phân, hex một cách tự nhiên mà không phải dừng lại tính từng bước.</p>"
   },
   {
    "title": "Tự kiểm tra tổng kết module (không chấm điểm)",
    "body": "<div class='callout good'><p>Trước khi làm quiz cuối trang: bạn có thể tự đổi một số bất kỳ qua đủ cả 4 hệ đếm (thập phân→nhị phân→bát phân→hex→BCD) mà không cần xem lại slide nào không? Nếu còn vướng bước nào, quay lại đúng phần tương ứng ở trên trước khi làm quiz.</p></div>",
    "explain": "<p>Bài tự kiểm tra tổng kết cả module. Chọn một số bất kỳ, ví dụ 91, rồi đổi qua cả bốn hệ liên tiếp mà không mở slide nào. Thập phân sang nhị phân bằng chia liên tiếp cho 2 (91 = 1011011₂). Nhị phân sang bát phân bằng nhóm 3 bit từ chuỗi vừa có. Nhị phân sang hex bằng nhóm 4 bit, cũng từ chính chuỗi nhị phân đó chứ không phải từ bát phân. Cuối cùng, tách từng chữ số thập phân gốc và đổi sang BCD (9→1001, 1→0001).</p><p>Nếu bạn làm trôi chảy cả chuỗi, bạn đã sẵn sàng cho bộ trắc nghiệm bên dưới. Nếu vướng ở bước nào, quay lại đúng phần tương ứng phía trên.</p>"
   }
  ]
 ],
 "en": [
  [
   {
    "title": "Why not just use decimal directly in electronic circuits?",
    "body": "<p>Digital electronic circuits can only reliably distinguish <b>two voltage levels</b> (high/low), not ten distinct levels needed for decimal digits. Hardware is therefore forced into binary (2 levels); every other number system (octal, hex, BCD) is simply a human-friendly shorthand for that same binary string.</p>",
    "explain": "<p>Picture a light switch: it has two states, on or off, and you can tell them apart instantly even if the voltage wobbles a little. Now picture a switch with ten notches for the digits 0 to 9. A bit of electrical noise or an aging component could make the circuit read notch 4 as notch 5.</p><p>That is why digital circuits are built to separate only <b>two voltage levels</b> (typically 0 V and 5 V). The wide gap between them tolerates noise well. Octal, hex and BCD, covered later, are <b>not</b> different ways of computing inside the hardware. They are shorthand that lets people write the same binary string more compactly.</p>"
   },
   {
    "title": "Four core number systems in avionics",
    "body": "<table class='tt'><thead><tr><th>System</th><th>Base</th><th>Digits used</th><th>Main role</th></tr></thead><tbody><tr><td>Binary</td><td>2</td><td>0,1</td><td>Internal computer processing</td></tr><tr><td>Octal</td><td>8</td><td>0-7</td><td>Compact system status codes</td></tr><tr><td>Hexadecimal</td><td>16</td><td>0-9,A-F</td><td>Memory addresses, BITE fault codes</td></tr><tr><td>BCD</td><td>n/a</td><td>4 bits/digit</td><td>Decimal display on screens</td></tr></tbody></table>",
    "explain": "<p>The image above comes from the original lecture slide. It summarises the four number systems in this module and the real job each one does on the A320. Binary is the internal language of every onboard computer (FMGC, FWC, SDAC). Octal shortens status codes on some older MCDU pages. Hex covers memory addresses and BITE fault codes because it is compact and easy to look up. BCD bridges the internal binary value to the familiar decimal digits on cockpit displays.</p><p>On a first pass, do not try to memorise every detail in the picture. Keep the main idea: four systems, four roles, all describing the <b>same</b> data underneath.</p>",
    "img": "numsys_apps_p03.jpg"
   },
   {
    "title": "Positional weighting: the principle shared by every base",
    "body": "<p>In any base-b system, the digit at position i (from the right, starting at 0) carries weight bⁱ. The value of the whole number equals the sum of (digit × weight).</p><div class='pd-formula'><div class='pd-formula-label'>Value of a number in base b</div><div class='pd-formula-math'>N = Σ dᵢ·bⁱ</div></div>",
    "explain": "<p>This is the most general formula in the module and it works for any base, so read it slowly. \"Positional weighting\" means a digit's real value depends on <b>where</b> it sits. In 528, the digit 5 is worth 500, not 5, because it stands in the hundreds place.</p><p>The formula N = Σ dᵢ·bⁱ restates that in symbols. dᵢ is the digit at position i (counted from the right, starting at 0), b is the base, bⁱ is the weight of that position, and Σ means \"add everything up\". The next slide applies it to a familiar decimal number before we move to binary.</p>"
   },
   {
    "title": "Example: applying positional weight to a familiar decimal number",
    "body": "<p>528 (base 10) = 5·10² + 2·10¹ + 8·10⁰ = 500+20+8 = 528. This is exactly the same principle the course will re-apply to base 2, 8 and 16: only the value of b changes.</p>",
    "explain": "<p>The example 528 = 5×10² + 2×10¹ + 8×10⁰ is just a formal spelling of the sum 500+20+8 that everyone learned in primary school. The only new thing is seeing that it matches the positional-weight formula.</p><p>The attached image shows that decimal is still what pilots and engineers see every day on EFIS, FMS and weight tables. The reason is simply that people count on ten fingers. Inside the computer, each of these numbers has already been converted to binary before any calculation, then converted back only so a human can read it.</p>",
    "img": "numsys_apps_p09.jpg"
   },
   {
    "title": "Why technicians don't read raw long binary strings",
    "body": "<p>A 16-bit memory address written in binary is 16 characters long (e.g. <code>1010110011110000</code>), easy to mistype or misread a single bit. Rewritten in hex it is only 4 characters (<code>ACF0</code>): this reduces transcription error, a practical engineering reason, not just a theoretical one.</p>",
    "explain": "<p>Compare the two forms. The binary string 1010110011110000 is 16 characters long. Misreading or mistyping just <b>one</b> bit in the middle ruins the whole address, and the eye struggles to spot the slip in a long run of look-alike 0s and 1s.</p><p>Written in hex, the same value is only 4 characters (ACF0). Fewer characters mean fewer chances to slip, and the eye tells 0-9 and A-F apart far more easily than a wall of 0s and 1s. This is a practical reason, not only a mathematical one, and it is why maintenance documents record addresses and fault codes in hex.</p>"
   },
   {
    "title": "The four systems are not independent: constant conversion is required",
    "body": "<ul><li>The computer PROCESSES in binary</li><li>The display SHOWS the pilot BCD/decimal</li><li>Maintenance logs RECORD fault codes in hex</li><li>Some legacy status pages use octal</li></ul><p>Maintenance engineers must be fluent converting in all four directions, not just one.</p>",
    "explain": "<p>The triangle diagram shows that no number system stands alone. All four have two-way \"Conversion\" arrows linking them to the others, so engineers convert back and forth constantly.</p><p>In the figure, each system has its own sample number: (9856)₁₀, (101010101)₂, (7537)₈ and (A89DE)₁₆. These are four different numbers, shown only to illustrate that each system has its own digits, with the small subscript naming the base. The bullets beside the diagram state the real roles: computers process in binary, displays show BCD or decimal, maintenance documents record fault codes in hex, and a few legacy status pages use octal.</p>",
    "img": "numsys_conversion_diagram.png"
   },
   {
    "title": "⚠️ Trap: confusing a 'number system' with a 'unit of measure'",
    "body": "<div class='callout warn'><p>Beginners often confuse 10₁₆ (sixteen, base 16) with 10 (ten, base 10) because the digits look identical. Always mark the base subscript explicitly, as Tooley's convention shows: (75)₈, (75)₁₀, (75)₁₆ are THREE completely different values despite sharing the digits '7','5'.</p></div>",
    "explain": "<p>This is an easy trap: you see \"10\" and read \"ten\" out of habit. But 10₁₆ (read \"one zero, base sixteen\") is really sixteen, while 10₂ is two and 10₈ is eight.</p><p>The three numbers (75)₈, (75)₁₀ and (75)₁₆ look identical character by character, yet they stand for three different values: 61, 75 and 117 in decimal. The rule that saves you: always write the base subscript (₂, ₈, ₁₀, ₁₆) whenever a number is not in default decimal.</p>"
   },
   {
    "title": "Application on the A320: why the FMGC must understand all four systems",
    "body": "<p>The FMGC (Flight Management Guidance Computer) receives binary sensor data, computes internally in binary, but must OUTPUT hex for maintenance logs, BCD for the MCDU display, and sometimes octal for status codes: one processing chip constantly converts between these systems in real time.</p>",
    "explain": "<p>The FMGC (Flight Management Guidance Computer) shows these four systems are not idle theory. It receives sensor data already digitised into binary and performs every internal calculation in binary, because that is the only language its processor understands.</p><p>When it must send results outward, it translates to suit the purpose: hex for maintenance logs, BCD for the pilot's MCDU display, and occasionally octal for some legacy status codes. One chip does this translation thousands of times per second, in real time.</p>"
   },
   {
    "title": "Data flow diagram of a numeric value in the cockpit",
    "body": "<p>Sensor (analog) → ADC → binary (processed inside FMGC/FWC) → re-encoded as BCD/hex → shown on EFIS/ECAM or logged by BITE. Every arrow in this chain is a point where the active number system must be correctly identified.</p>",
    "explain": "<p>The diagram traces the life of <b>one</b> measured quantity, say air pressure. The sensor produces an analog signal (a smoothly varying voltage). The ADC (Analog-to-Digital Converter) turns it into a discrete binary string. The FMGC or FWC calculates entirely in binary. The result is then re-encoded as BCD or hex, depending on whether it goes to a display (EFIS/ECAM) or to a log (BITE).</p><p>Each arrow is a real conversion inside real hardware. If any step uses the wrong number system, the value the pilot sees ends up wrong too.</p>"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>Pause for 30 seconds: can you explain out loud why a maintenance engineer CANNOT learn just one number system and skip the other three? If unsure, revisit the first two slides before moving to Part 2.</p></div>",
    "explain": "<p>Before Part 2, test yourself by answering aloud, in your own words and without the slides: why can't a maintenance engineer learn one number system and skip the other three?</p><p>A complete answer has three points. The computer inside always works in binary. The pilot's display shows easy-to-read decimal or BCD. Maintenance documents and fault logs use hex because it is compact and less error-prone to look up. If you can say all three fluently, you are ready for Part 2.</p>"
   }
  ],
  [
   {
    "title": "MSB, LSB and powers-of-two weighting",
    "body": "<p>In a binary number, the leftmost bit is the <b>MSB</b> (Most Significant Bit: highest weight), the rightmost bit is the <b>LSB</b> (Least Significant Bit: weight 2⁰=1).</p><table class='tt'><thead><tr><th>2⁷</th><th>2⁶</th><th>2⁵</th><th>2⁴</th><th>2³</th><th>2²</th><th>2¹</th><th>2⁰</th></tr></thead><tbody><tr><td>128</td><td>64</td><td>32</td><td>16</td><td>8</td><td>4</td><td>2</td><td>1</td></tr></tbody></table>",
    "explain": "<p>MSB (Most Significant Bit) is the bit with the largest weight and LSB (Least Significant Bit) is the bit with the smallest. They play the role of the \"hundreds place\" and the \"units place\" in a decimal number. In 110100, the leftmost bit (MSB) has weight 2⁵ = 32 and the rightmost bit (LSB) has weight 2⁰ = 1.</p><p>The table of powers of two (1, 2, 4, 8, 16, 32, 64, 128) is the multiplication table of binary. Learn these eight values and every binary-to-decimal conversion on the following slides becomes quick.</p>"
   },
   {
    "title": "Worked example: binary → decimal",
    "body": "<p>Convert 11011010₂ to decimal: sum the weights of bits that are 1:</p><p>11011010 = 128+64+0+16+8+0+2+0 = <b>218</b></p><p>(This is Tooley's own worked example: only add weights where the bit is 1, skip positions with 0.)</p>",
    "explain": "<p>The rule fits on one line: <b>add</b> the weights of positions holding a 1 and skip positions holding a 0. Do not subtract or multiply, just leave those positions out.</p><p>In 11011010, the positions holding 1 carry weights 128, 64, 16, 8 and 2. The two positions holding 0 (weights 32 and 1) are skipped. The sum is 128+64+16+8+2 = 218. A quick check: count the 1-bits in the original string (five here) and count the terms you added. If the counts differ, you skipped or double-counted a weight.</p>"
   },
   {
    "title": "Worked example: decimal → binary by repeated division",
    "body": "<p>Convert 45 to binary by repeatedly dividing by 2, reading remainders bottom-up:</p><table class='tt'><thead><tr><th>Division</th><th>Quotient</th><th>Remainder</th></tr></thead><tbody><tr><td>45÷2</td><td>22</td><td>1</td></tr><tr><td>22÷2</td><td>11</td><td>0</td></tr><tr><td>11÷2</td><td>5</td><td>1</td></tr><tr><td>5÷2</td><td>2</td><td>1</td></tr><tr><td>2÷2</td><td>1</td><td>0</td></tr><tr><td>1÷2</td><td>0</td><td>1</td></tr></tbody></table><p>Reading remainders bottom-up: <b>101101</b> (matches the result independently verified in notebook 01).</p>",
    "explain": "<p>This method runs opposite to the previous slide. Instead of adding weights, divide the decimal number by 2 again and again, noting the <b>remainder</b> (always 0 or 1) each time, and stop when the quotient reaches 0.</p><p>For 45: 45÷2 = 22 r 1; 22÷2 = 11 r 0; 11÷2 = 5 r 1; 5÷2 = 2 r 1; 2÷2 = 1 r 0; 1÷2 = 0 r 1. The usual slip is the reading order: read the remainders <b>bottom to top</b> to get 101101, because the first remainder is the least significant bit and the last is the most significant.</p>"
   },
   {
    "title": "A faster shortcut: sum weights 2ⁱ directly (no division needed)",
    "body": "<p>45 = 32+8+4+1 → mark 1 at exactly those four weight positions (32,8,4,1), 0 elsewhere → 101101. This shortcut is faster by hand, but the division method on the previous slide is the GENERAL method that also works for octal/hex.</p>",
    "explain": "<p>This shortcut also reverses binary-to-decimal: we look for the weights that add up to the given number. For 45, subtract the largest weight that still fits: 45-32 = 13, 13-8 = 5, 5-4 = 1, 1-1 = 0. So the weights 32, 8, 4 and 1 get a 1, while 64, 16 and 2 get a 0, giving 101101, the same as the previous slide.</p><p>It is fast for small numbers done in your head. Repeated division is the reliable method that never skips a step, especially for large numbers or under exam pressure.</p>"
   },
   {
    "title": "Binary addition: the carry rule",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>1-bit addition table</div><div class='pd-formula-math'>0+0=0 · 0+1=1 · 1+0=1 · 1+1=10 (carry 1)</div></div><p>Example: 0110 + 0101 = 1011 (6+5=11: cross-check in decimal to confirm the carry rule was applied correctly).</p>",
    "explain": "<p>The binary addition table has only four cases (the decimal table has 100): 0+0 = 0, 0+1 = 1, 1+0 = 1, and the special case 1+1 = 10, read as \"write 0, carry 1\", just like \"9+1 = 10, write 0 carry 1\" in decimal.</p><p>The circuit that performs exactly this addition is the <b>half adder</b>. The figure shows it needs only two gates: an XOR gate giving the sum Σ = A⊕B (the result before any carry) and an AND gate giving the carry Cout = AB. The AND gate outputs 1 only when both inputs are 1, matching the fact that 1+1 is the only case that produces a carry. You will meet XOR and AND again in Module 02.</p>",
    "img": "numsys_half_adder.png"
   },
   {
    "title": "Negative numbers in binary: why two's complement is needed",
    "body": "<p>Pure binary has no minus sign. Negative numbers are represented using <b>two's complement</b>: invert every bit, then add 1. This is how a CPU performs subtraction using only an adder circuit.</p>",
    "explain": "<p>Ordinary arithmetic puts a minus sign in front of a negative number. Electronic circuits have only two voltage levels (0 and 1), with no third level left over to stand for a sign.</p><p>CPU designers solved this with <b>two's complement</b>, a bit transformation built so that adding a number to another number's two's complement gives exactly the result of subtraction. A CPU therefore needs only one adder circuit to do both addition and subtraction, which saves a good deal of hardware inside the chip.</p>"
   },
   {
    "title": "Worked example: two's complement of 10110",
    "body": "<p>Step 1: invert bits: 10110 → 01001.</p><p>Step 2: add 1: 01001 + 1 = <b>01010</b>.</p><p>(Matches the original Tooley Ch.2 Q3: see the Module 01 quiz.)</p>",
    "explain": "<p>Two's complement takes two steps, in order. Step 1: invert every bit (0 becomes 1, 1 becomes 0), so 10110 becomes 01001. Step 2: add 1, so 01001 + 1 = 01010. Therefore 01010 is the two's complement of 10110, meaning the matching negative value.</p><p>You can check it without a table: add the original to the result, 10110 + 01010 = 100000. Drop the overflow bit and you get 00000, which confirms the answer, since a number plus its own negative must equal zero.</p>"
   },
   {
    "title": "⚠️ Trap: forgetting the '+1' step after inverting",
    "body": "<div class='callout warn'><p>The most common error is inverting the bits and STOPPING there: that is <b>one's complement</b>, not two's complement. Always verify by adding the original number to its two's complement: if the sum overflows past the original bit width (e.g. 10110+01010=100000, drop the overflow bit → 00000), the result is correct.</p></div>",
    "explain": "<p>This is the most common mistake when learning two's complement: performing only Step 1 (inverting the bits) and stopping, believing the job is done. That result is <b>one's complement</b>, a different concept that most modern systems do not use for negative numbers.</p><p>The one's complement of 10110 is just 01001, while the correct two's complement is 01010. To catch a forgotten +1, always run the addition check from the previous slide. If the sum is not zero after dropping the overflow bit, you almost certainly forgot to add 1.</p>"
   },
   {
    "title": "Application on the A320: why the ADIRU outputs signed binary data",
    "body": "<p>The ADIRU (Air Data Inertial Reference Unit) must represent both positive values (climbing altitude) and negative values (decreasing speed/negative pitch angle): two's complement lets the FMGC add/subtract these using a single adder circuit, with no separate subtractor needed.</p>",
    "explain": "<p>The ADIRU (Air Data Inertial Reference Unit) measures values that can rise or fall continuously in flight: altitude rising in the climb, airspeed dropping under braking, pitch angle positive or negative. Without two's complement the system would need one adder for positive values and a separate subtractor for negative ones, doubling the hardware.</p><p>With two's complement, the FMGC needs just <b>one</b> binary adder to handle both directions of every flight value. The attached image shows how all A320 sensor data follows this binary principle.</p>",
    "img": "numsys_apps_p11.jpg"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>Try mentally: what is the two's complement of the 4-bit binary number 0110? (Hint: invert to 1001, add 1 → 1010.) If you got something else, review the two-step process above.</p></div>",
    "explain": "<p>Try this before Part 3: find the two's complement of the 4-bit number 0110 without looking at the hint. Recall the two steps: invert the bits (0110 becomes 1001), then add 1 (1001 + 1 = 1010).</p><p>If you got 1010, check it by addition: 0110 + 1010 = 10000, drop the overflow bit and you have 0000, as expected. If you got something else, you probably stopped at the inversion step (1001) and forgot the +1, which is exactly the trap on the previous slide. Review that slide and try again.</p>"
   }
  ],
  [
   {
    "title": "Why octal groups 3 bits and hex groups 4 bits",
    "body": "<p>2³=8, so each octal digit represents exactly 3 bits; 2⁴=16, so each hex digit represents exactly 4 bits. This is NOT an arbitrary convention: it follows directly from the definition of the base itself.</p>",
    "explain": "<p>The answer lies in exponents. 2³ = 8 means 3 bits can represent exactly 8 values (000 to 111), which matches the 8 octal digits (0 to 7). So each octal digit corresponds to exactly 3 bits. Likewise 2⁴ = 16 matches the 16 hex symbols (0-9 and A-F), so each hex digit corresponds to exactly 4 bits.</p><p>This is not an arbitrary convention but a mathematical consequence. Grouping the wrong number of bits, say 3 bits mapped to a hex digit, gives a wrong conversion immediately.</p>"
   },
   {
    "title": "Quick reference table: binary ↔ hex (must be memorised)",
    "body": "<table class='tt'><thead><tr><th>Hex</th><th>Binary</th><th>Hex</th><th>Binary</th></tr></thead><tbody><tr><td>0</td><td>0000</td><td>8</td><td>1000</td></tr><tr><td>1</td><td>0001</td><td>9</td><td>1001</td></tr><tr><td>2</td><td>0010</td><td>A</td><td>1010</td></tr><tr><td>3</td><td>0011</td><td>B</td><td>1011</td></tr><tr><td>4</td><td>0100</td><td>C</td><td>1100</td></tr><tr><td>5</td><td>0101</td><td>D</td><td>1101</td></tr><tr><td>6</td><td>0110</td><td>E</td><td>1110</td></tr><tr><td>7</td><td>0111</td><td>F</td><td>1111</td></tr></tbody></table>",
    "explain": "<p>This table is the most important tool in Part 3. It lists all 16 hex values with their exact 4-bit patterns. Because each hex digit always maps to one fixed 4-bit pattern, you convert by lookup with no further calculation. That is why binary-to-hex is faster and less error-prone than going through decimal.</p><p>A practical tip: copy the table by hand a few times until you remember A=1010, B=1011, C=1100, D=1101, E=1110 and F=1111. Those six values are where beginners slip most often.</p>"
   },
   {
    "title": "Worked example: binary → octal by grouping 3 bits",
    "body": "<p>Convert 100010001₂ to octal: group from the right in 3s: 100 | 010 | 001 → 4 2 1 → <b>421₈</b>. (Matches Tooley Ch.2 Q8.)</p>",
    "explain": "<p>The group-in-3s procedure applies the 2³ = 8 principle from the first slide of this part. Split 100010001 into groups of 3 bits, <b>starting from the right</b>: 100 | 010 | 001. Look each group up in the octal table (000 = 0, 001 = 1, 010 = 2, ..., 111 = 7) to get 4, 2, 1 and join them as 421₈.</p><p>The most common mistake is grouping from the left. Every group is then misaligned and the answer is wrong, especially when the bit count is not divisible by 3 (see the padding slide later).</p>"
   },
   {
    "title": "Worked example: hex → octal MUST go through binary",
    "body": "<p>111₁₆ → expand each hex digit to 4 bits: 1→0001, 1→0001, 1→0001 → 000100010001₂.</p><p>Regroup in 3s from the right: 000 100 010 001 → 4 2 1 → <b>421₈</b>. You cannot infer hex→octal directly, skipping this step.</p>",
    "explain": "<p>There is no single-step formula from hex to octal. You always go through binary, in two stages.</p><p>Stage 1: expand each hex digit to exactly 4 bits: 1→0001, 1→0001, 1→0001, joined as 000100010001. Stage 2: regroup that string in 3s from the right: 000 100 010 001, which reads 4, 2, 1, so 421₈. If you try to guess \"which octal digit matches hex F\" and skip the binary step, you will almost always be wrong, because the two systems have no simple divisibility relationship.</p>"
   },
   {
    "title": "Worked example: binary → hex by grouping 4 bits",
    "body": "<p>Convert 10110011₂ to hex: group in 4s: 1011 | 0011 → B | 3 → <b>B3₁₆</b>. (Matches Tooley Ch.2 Q11.)</p>",
    "explain": "<p>Grouping in 4s for hex works exactly like grouping in 3s for octal, only the group size changes. Split 10110011 into two 4-bit groups from the right: 1011 | 0011. Look up the hex table to get B (1011) and 3 (0011), joined as B3₁₆.</p><p>A memory aid: B is one step after A = 10, so B = 11 = 1011 in binary. With practice you will stop needing the table. Always group from right to left, the same caveat as on the 3-bit slide.</p>"
   },
   {
    "title": "Padding with leading zeros when bit count isn't divisible",
    "body": "<p>Convert 111001110₂ (9 bits) to octal: 9 is already divisible by 3, so group directly: 111 001 110 → 7 1 6 → 716₈. Always count the bits first and pad with LEADING zeros if the count is not a multiple of the group size.</p>",
    "explain": "<p>Before grouping bits, always count the total number of bits to see whether padding is needed: octal needs a multiple of 3, hex needs a multiple of 4. With 111001110 (exactly 9 bits, already a multiple of 3) group directly: 111 001 110, which reads 7, 1, 6, so 716₈.</p><p>If the count does not divide evenly, say 7 bits grouped by 3, add zeros on the <b>left</b>, not the right. Leading zeros never change a value, just as 007 equals 7 in decimal. Zeros added on the right would change the value completely.</p>"
   },
   {
    "title": "Why hex dominates over octal in modern systems",
    "body": "<p>Most modern data buses (8/16/32-bit) are multiples of 4, so hex groups fit exactly with no padding, while octal (groups of 3) often misaligns with common bus widths. This is why hex dominates modern maintenance documentation over octal.</p>",
    "explain": "<p>Most data buses in modern computers and avionics are 8, 16 or 32 bits wide. These are multiples of 4, so they split into hex digits with nothing left over, but they are not always multiples of 3. A 16-bit register splits into exactly 4 hex digits, while splitting it into octal digits leaves one stray bit that needs padding, which is a nuisance when programming or reading logs.</p><p>This practical reason explains why hex gradually replaced octal in modern technical and maintenance documents, although octal survives in a few legacy systems.</p>"
   },
   {
    "title": "⚠️ Trap: adding/subtracting hex digits as if they were decimal",
    "body": "<div class='callout warn'><p>Never add '9'+'9'=18 and write '18' into a hex result: hex only has 16 symbols (0-F). 9+9=18 (decimal) = 12₁₆, written as digit 2 with a carry of 1. Convert through decimal to add if you are not yet fluent with the hex addition table.</p></div>",
    "explain": "<p>People used to decimal arithmetic can carry that habit into hex, adding 9+9 to get 18 and writing \"18\" straight into the answer. But hex has only 16 symbols (0-9 and A-F), and there is no symbol \"18\".</p><p>The right way: 9+9 = 18 in decimal, and 18 in hex is 12₁₆ (since 18 = 16+2). So write the digit 2 in that column and <b>carry 1</b> to the next column on the left, the same carry principle as binary addition. Until the hex addition table feels natural, the safe approach is to convert the hex digits to decimal, add, and convert the result back to hex.</p>"
   },
   {
    "title": "Application on the A320: BITE fault codes are always shown as 4-digit hex",
    "body": "<p>A fault code such as <code>0xACDE</code> corresponds to exactly 16 bits of binary (4 hex digits × 4 bits). Technicians looking it up in the AMM don't need to count 16 individual bits: matching 4 hex characters is enough, drastically reducing misreading compared with a long binary string.</p>",
    "explain": "<p>BITE (Built-In Test Equipment) is the subsystem that detects faults on the aircraft automatically. Every fault code it produces is written as 4 hex characters, for example 0xACDE, because 4 hex characters match exactly 16 bits, enough to encode tens of thousands of fault types without a long string of digits.</p><p>When looking the code up in the AMM (Aircraft Maintenance Manual), the technician only has to match 4 hex characters, which is much faster and less error-prone than counting and comparing 16 bits by eye. The attached image shows the whole chain of real uses: memory addresses, ARINC 429 data labels and maintenance fault codes, all in hex for the same reason.</p>",
    "img": "numsys_apps_p17.jpg"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>Without a calculator: what is 2F₁₆ in binary? (Hint: 2→0010, F→1111 → 00101111.) Check against the reference table at the start of this part if unsure.</p></div>",
    "explain": "<p>Self-check: convert 2F₁₆ to binary with no calculator and no table. Split the hex digits, turn 2 into 0010, turn F into 1111 (F is the largest hex value, so every bit is set), and join the two groups in order: 00101111.</p><p>If you got a different answer, return to the quick-reference table at the start of Part 3 to find which group you remembered wrongly, then try a similar example until you can do it without the table.</p>"
   }
  ],
  [
   {
    "title": "How is BCD different from pure binary?",
    "body": "<p>Pure binary converts the WHOLE number at once; BCD converts EACH decimal digit separately into 4 bits. BCD therefore always uses more bits than pure binary for the same value, in exchange for a trivially simple conversion to 7-segment display.</p>",
    "explain": "<p>The core difference is <b>what unit gets converted</b>. Pure binary treats the whole number as one block and converts it once (45 becomes 101101). BCD splits the number into decimal digits and converts each digit into 4 bits.</p><p>For 45, pure binary gives 101101 (6 bits) while BCD gives 0100 0101 (8 bits, built from 4→0100 and 5→0101). So BCD always spends more bits on the same value. In exchange, a 7-segment display needs only a simple decoder per 4-bit group, whereas pure binary would need a much more complex circuit to split the value back into decimal digits.</p>"
   },
   {
    "title": "Conversion table: 10 decimal digits ↔ BCD",
    "body": "<table class='tt'><thead><tr><th>Digit</th><th>BCD</th><th>Digit</th><th>BCD</th></tr></thead><tbody><tr><td>0</td><td>0000</td><td>5</td><td>0101</td></tr><tr><td>1</td><td>0001</td><td>6</td><td>0110</td></tr><tr><td>2</td><td>0010</td><td>7</td><td>0111</td></tr><tr><td>3</td><td>0011</td><td>8</td><td>1000</td></tr><tr><td>4</td><td>0100</td><td>9</td><td>1001</td></tr></tbody></table>",
    "explain": "<p>The table lists just 10 combinations, one per decimal digit. The hex table in Part 3 had 16. This is the core difference between BCD and hex, and it returns on the \"trap\" slide later.</p><p>The table is easy to learn because it matches ordinary binary counting from 0000 to 1001, only stopping earlier. Plain 4-bit binary counts up to 1111 = 15, while BCD stops at 1001 = 9. Remembering that stopping point is the fastest way to tell whether a pattern is valid BCD.</p>"
   },
   {
    "title": "Worked example: decimal → BCD",
    "body": "<p>Convert 37 to BCD: encode each digit separately: 3→0011, 7→0111 → concatenate <b>00110111</b>. (Matches Tooley Ch.2 Q5.)</p>",
    "explain": "<p>The procedure has one step: split the decimal digits apart, then convert each digit to 4 bits using the table on the previous slide. No calculation like converting to pure binary is needed.</p><p>For 37: digit 3 becomes 0011 and digit 7 becomes 0111. Join them in the original order (tens first, then units) to get 00110111. Note that this is <b>not</b> converting 37 to pure binary, which would give 100101, only 6 bits. The two conversions serve different purposes, so do not mix them up.</p>"
   },
   {
    "title": "Worked example: BCD → decimal",
    "body": "<p>Convert 10010001 (BCD) to decimal: split into 4-bit groups from the right: 1001 | 0001 → 9 | 1 → <b>91</b>. (Matches Tooley Ch.2 Q4.)</p>",
    "explain": "<p>This reverses the previous slide. Starting from a BCD bit string, first split it into groups of exactly 4 bits from the right, the same grouping used for hex. Then look up each group to get one decimal digit.</p><p>For 10010001: split into 1001 | 0001, look up 9 and 1, and join them in order to get 91. If you meet a group outside 0000 to 1001 while splitting (for example 1010 or 1111), the string is not valid BCD. The next slide says more about those patterns.</p>"
   },
   {
    "title": "The 6 invalid BCD combinations",
    "body": "<p>4-bit BCD has 16 possible patterns (0000-1111) but only 10 (0000-1001) are valid. The six patterns 1010-1111 do NOT correspond to any decimal digit: if a BCD decoder circuit encounters these, it signals a hardware fault or data corruption.</p>",
    "explain": "<p>With 4 bits you can form 2⁴ = 16 patterns (0000 to 1111), but BCD uses only the first 10 (0000 to 1001) for the 10 decimal digits. The remaining six patterns (1010, 1011, 1100, 1101, 1110, 1111) mean nothing in BCD.</p><p>This is not harmless. If a BCD circuit, such as a 7-segment decoder, receives one of those \"garbage\" patterns, something is definitely wrong: a hardware fault, signal noise or corrupted data in transit. Many onboard self-test systems (BITE) exploit exactly this property to detect corrupted BCD data.</p>"
   },
   {
    "title": "ASCII: encoding characters, not encoding a quantity",
    "body": "<p>Standard ASCII uses 7 bits, representing 128 characters (letters, digits, punctuation, control characters). Note: the ASCII code for the character '5' (0110101₂ = 35₁₆) is COMPLETELY DIFFERENT from the binary number representing the value 5 (00000101₂): these are two independent encoding concepts.</p>",
    "explain": "<p>Two concepts are often mixed up. Encoding a <b>quantity</b> (binary, BCD) says how much. Encoding a <b>character</b> (ASCII) says which letter, text digit, punctuation mark or control command it is.</p><p>Standard ASCII uses 7 bits, enough for 2⁷ = 128 characters: upper and lower case letters, digits and invisible control characters such as newline and tab. The point that trips people most: the ASCII code for the <b>character</b> '5' is 0110101₂, quite different from the binary number for the <b>value</b> 5, which is 00000101₂. One describes a symbol to display, the other a quantity to calculate with.</p>"
   },
   {
    "title": "Example: the ASCII code for the letter 'A'",
    "body": "<p>'A' = 65 (decimal) = 41₁₆ = 1000001₂. The text string 'TCAS' is transmitted as 4 consecutive ASCII bytes, not as a single number.</p>",
    "explain": "<p>A concrete example for the character 'A': its ASCII code is 65 in decimal, 41₁₆ in hex and 1000001₂ in binary (exactly 7 bits under the ASCII standard).</p><p>When a system transmits the string 'TCAS' (Traffic Collision Avoidance System), it does not send one number for the whole word. It sends 4 separate ASCII bytes, one each for T, C, A and S. That is why raw data in a debugging tool may show the hex sequence 54 43 41 53, and you need to recognise it as the text 'TCAS' rather than a single binary number.</p>"
   },
   {
    "title": "⚠️ Trap: confusing BCD with hex when looking at an isolated 4-bit group",
    "body": "<div class='callout warn'><p>Both BCD and hex group data in 4 bits, which is easy to confuse. The key difference: hex has all 16 valid 4-bit values (0-F), while BCD only has 10 valid values (0-9): always ask what the context is (an address/hex value, or a decimal digit/BCD) before interpreting a 4-bit group.</p></div>",
    "explain": "<p>BCD and hex both group data in 4-bit clusters, so at a glance they are easy to confuse. The group 0111 reads as 7 either way, so no problem shows up. Try 1100 instead: it is a valid 'C' in hex but an invalid pattern in BCD.</p><p>The core distinction: hex has all 16 values valid (0 to F), while BCD has only 10 valid values (0 to 9), and the other six are garbage. The safe rule: before interpreting a 4-bit group, always find the context in the accompanying documentation (an address in hex, or a BCD digit), and never guess from the bit pattern alone.</p>"
   },
   {
    "title": "Application on the A320: why the MCDU keypad enters data in BCD",
    "body": "<p>When a pilot types an altitude/speed on the MCDU, the keypad generates a BCD code for each keystroke: the CPU only needs to split 4-bit groups to know each digit exactly, far simpler than decoding one large binary number and then splitting it back into decimal digits.</p>",
    "explain": "<p>When a pilot types a number on the MCDU (Multi-purpose Control and Display Unit) keypad to enter an altitude or speed, each digit key produces the BCD code of that exact digit. The whole number is not encoded into pure binary at the start.</p><p>The practical benefit: the processor only has to split the 4-bit groups to know exactly which digit was typed. That is much simpler than receiving one large binary number and running an algorithm to split it back into decimal digits. The attached image shows the process: the pilot enters 350 on the MCDU, and each digit is BCD-encoded (3→0011, 5→0101, 0→0000).</p>",
    "img": "numsys_apps_p25.jpg"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>What is 68 (decimal) in BCD? (Hint: 6→0110, 8→1000.) Compare your answer with the practice question bank at the bottom of the page after trying it yourself.</p></div>",
    "explain": "<p>Practice: convert 68 (decimal) to BCD without looking at the table. Split the digits 6 and 8, convert each (6→0110, 8→1000), and join them in order (tens first) to get 01101000.</p><p>This is the last exercise of Part 4 before the multiple-choice questions at the bottom of the page. If you finish it fluently, you have covered all four theory parts (decimal, binary, octal and hex, BCD and ASCII) and are ready for Part 5, which ties everything together with real A320 examples.</p>"
   }
  ],
  [
   {
    "title": "The full picture: how many number systems does one altitude value pass through?",
    "body": "<p>Barometric sensor (analog) → ADC → 16-bit binary inside the ADIRU/FMGC → BCD-encoded for the PFD display → possibly logged in hex if a sensor fault occurs. A SINGLE physical quantity (altitude) passes through at least 3 different number systems before reaching the pilot's/engineer's eyes.</p>",
    "explain": "<p>This slide ties the four earlier parts into one story. Follow a single altitude value from birth to display. A barometric sensor produces a continuous analog signal. The ADC samples it and digitises it into a 16-bit binary string. Inside the ADIRU and FMGC that string is calculated and corrected. Finally the result is re-encoded as BCD so the PFD (Primary Flight Display) can show familiar digits to the pilot.</p><p>If a sensor fault occurs, the system also records a hex-coded log entry for engineers to look up later. One physical value, at least three number systems.</p>"
   },
   {
    "title": "Worked example: 10,000 ft as a 16-bit binary value",
    "body": "<p>10,000 (decimal) → binary using the repeated-division-by-2 method learned in Part 2: 10000, 5000, 2500, 1250, 625, 312, 156, 78, 39, 19, 9, 4, 2, 1, 0. Reading the remainders bottom-up and zero-padding to 16 bits gives <b>0010011100010000₂</b>. This is the raw data the FMGC processes internally.</p>",
    "explain": "<p>This exercise reuses the repeated division by 2 from Part 2: convert 10,000 (feet) to binary. The 16-bit result is 0010011100010000, zero-padded at the front because aircraft computer registers usually have fixed widths that are multiples of 8.</p><p>A quick hex check: grouping in 4s gives 0010 | 0111 | 0001 | 0000, which is 2710₁₆, and 2710₁₆ = 2×4096 + 7×256 + 1×16 = 10,000. This bit string is the raw data the FMGC stores and computes with, quite unlike the familiar 10,000 on the display, which was re-encoded to BCD before being shown.</p>"
   },
   {
    "title": "Example: ARINC 429 bus data shown in hex in maintenance logs",
    "body": "<p>A 32-bit ARINC 429 data word, when logged for maintenance, is shortened to 8 hex characters instead of 32 binary characters: engineers read the log far faster, a direct real application of the hex conversion learned in Part 3.</p>",
    "explain": "<p>ARINC 429 is a widely used avionics data standard in which each data word is exactly 32 bits. Writing all 32 binary characters into a maintenance log would fill a page with hard-to-read 0s and 1s.</p><p>So the system groups the bits in 4s (the principle from Part 3) and shortens them to 8 hex characters. Engineers read 8 hex characters far faster than they can count and compare 32 bits, and misread them less often. This is the practical reason given in Part 1 on why technicians do not read long binary strings.</p>"
   },
   {
    "title": "Example: EGT shown as BCD on the ECAM",
    "body": "<p>Engine exhaust gas temperature (EGT), e.g. 650°C, is BCD-encoded (6-5-0) before being sent to the 7-segment display driver on the ECAM: exactly the BCD→7-segment principle learned in Part 4, avoiding a complex binary-to-decimal decoder.</p>",
    "explain": "<p>EGT (Exhaust Gas Temperature) is a perfect example of BCD driving a 7-segment display. The value 650°C splits into three digits 6, 5, 0, each converted to BCD (6→0110, 5→0101, 0→0000). Each 4-bit group goes straight into a simple 7-segment decoder that lights the right segments on the ECAM screen.</p><p>If the system used pure binary here, a far more complex circuit would be needed to split one binary number back into decimal digits. That is why BCD remains popular for displays despite using more bits.</p>"
   },
   {
    "title": "Summary table: which number system is used where on the A320",
    "body": "<table class='tt'><thead><tr><th>Location in the system</th><th>Number system</th></tr></thead><tbody><tr><td>Internal processing in FMGC/FWC/SDAC</td><td>Binary</td></tr><tr><td>EGT, N1, altitude display on ECAM</td><td>BCD</td></tr><tr><td>BITE fault codes, maintenance logs</td><td>Hex</td></tr><tr><td>Some legacy status pages (MCDU STATUS)</td><td>Octal</td></tr></tbody></table>",
    "explain": "<p>The table collects the four conclusions from the four earlier parts so you can see the whole picture. Binary handles all internal calculation because the hardware understands only two voltage levels. BCD is used when familiar figures (EGT, N1, altitude) must be shown to pilots. Hex serves fault codes and maintenance logs because it is compact and low-error to look up. Octal survives only on some legacy status pages.</p><p>Treat the table as a quick lookup map. When you meet an unfamiliar number in technical documents, first identify <b>where</b> in the system it appears, and you can infer which number system is probably in use.</p>"
   },
   {
    "title": "Why maintenance staff cannot round off when reading hex",
    "body": "<p>Unlike a decimal value (where rounding is often acceptable), a hex fault code read WRONG BY EVEN ONE CHARACTER (e.g. looking up 0xACDE instead of 0xACDF) leads to a COMPLETELY WRONG AMM lookup: there is no concept of 'close enough' when working with system hex codes.</p>",
    "explain": "<p>With an ordinary decimal value, rounding 250.4 to 250 rarely causes real harm. A hex fault code is different. If an engineer misreads 0xACDE as 0xACDF (one final character off), the AMM lookup could point to two entirely different faults.</p><p>The result is the wrong part repaired, lost time and money, and, most importantly, the real fault left unfixed. That is why maintenance procedures require copying a hex code exactly and completely, with no estimating or rounding.</p>"
   },
   {
    "title": "⚠️ Trap: misreading byte order (endianness) when assembling hex",
    "body": "<div class='callout warn'><p>Some systems log data in reversed byte order (little-endian) compared with the intuitive reading order (big-endian). Before concluding a hex fault code's meaning, ALWAYS check that specific system's AMM for the byte order it specifies: never assume a default.</p></div>",
    "explain": "<p>\"Endianness\" is the order in which the bytes of a multi-byte value are stored or sent. Big-endian stores the most significant byte first, which matches the way people naturally read. Little-endian stores the least significant byte first, which feels backwards.</p><p>If an engineer used to reading big-endian assumes that order while the system logs in little-endian, joining the hex bytes in the wrong order produces a fault code very different from the real one, and the AMM lookup goes wrong as on the previous slide. The safe rule: never assume a byte order. Check the documentation of the specific system you are working on.</p>"
   },
   {
    "title": "Extra case: octal conversion for a legacy STATUS page",
    "body": "<p>Some older-generation MCDUs display the STATUS PAGE using a 3-digit octal code. For example, code 657₈ corresponds to binary 110101111₂: the engineer must regroup by 3 bits, exactly as learned in Part 3, to correctly look up the status meaning.</p>",
    "explain": "<p>Although hex has replaced octal in most modern systems, some older MCDUs still show status codes in octal, a holdover from designs decades old. The attached image shows this kind of octal use on the A320.</p><p>For the code 657₈, use the octal-to-binary table already learned (6→110, 5→101, 7→111) and join the groups to get 110101111₂, the actual bit string the system handles inside. The practical lesson: engineers working on older aircraft still need fluency in both octal and hex.</p>",
    "img": "numsys_apps_p21.jpg"
   },
   {
    "title": "Why this is the FOUNDATION module for everything that follows",
    "body": "<p>Module 02 (logic gates) will reuse binary truth tables; Module 03 (multiplexers) will use binary/hex channel-select addresses; Module 04 (CPU) will use hex memory addresses and binary opcodes. Mastering all four number systems here is a prerequisite for correctly understanding the next three modules.</p>",
    "explain": "<p>A look ahead. Module 02 on logic gates will constantly use truth tables written in 0s and 1s to describe the inputs and outputs of AND, OR and NOT gates. Module 03 on multiplexers will use channel-select addresses in binary or hex. Module 04 on CPUs will use hex memory addresses and binary opcodes.</p><p>If the four number systems and their conversions are not solid yet, you will stumble right at the start of Module 02, because every example there assumes you read and write binary and hex naturally, without stopping to work things out step by step.</p>"
   },
   {
    "title": "Final module self-check (ungraded)",
    "body": "<div class='callout good'><p>Before taking the quiz below: can you convert any given number through all four systems (decimal→binary→octal→hex→BCD) without looking back at any slide? If any step is still shaky, revisit that specific part above before starting the quiz.</p></div>",
    "explain": "<p>This is the final self-check for the whole module. Pick any number, say 91, and convert it through all four systems in turn without opening a slide. Decimal to binary by repeated division by 2 (91 = 1011011₂). Binary to octal by grouping that string in 3s. Binary to hex by grouping the same string in 4s, not from the octal result. Finally, split the original decimal digits and convert each to BCD (9→1001, 1→0001).</p><p>If you get through the whole chain fluently, you are ready for the multiple-choice questions below. If you stall at any step, go back to that part above first.</p>"
   }
  ]
 ]
}
