# -*- coding: utf-8 -*-
"""Slide Module 02 (VI + EN): body + explain (giai thich cho nguoi moi) + img (anh goc tu bai giang)."""

SLIDES = {
 "vi": [
  [
   {
    "title": "Cổng logic là gì?",
    "body": "<p>Một cổng logic (logic gate) là mạch điện tử có 1 hoặc nhiều đầu vào nhị phân (0 hoặc 1) và MỘT đầu ra nhị phân, được xác định bởi một hàm Boolean cố định của các đầu vào. Đây là khối xây dựng nhỏ nhất của mọi hệ thống số.</p>",
    "explain": "<p>Hãy hình dung một cổng logic như một công tắc thông minh: nó nhìn vào một hoặc nhiều tín hiệu 0/1 đưa vào, rồi theo một quy tắc cố định (đã khắc sẵn trong mạch, không đổi được), quyết định đưa ra đúng một tín hiệu 0 hoặc 1 duy nhất.</p><p>Mọi thứ phức tạp trong máy tính, từ phép cộng, phép so sánh, cho tới quyết định bật đèn cảnh báo trên máy bay, đều được xây từ việc ghép nối rất nhiều cổng logic đơn giản này lại với nhau. Học kỹ 6 loại cổng cơ bản trong module này là điều kiện bắt buộc trước khi hiểu bất kỳ mạch số nào phức tạp hơn.</p>"
   },
   {
    "title": "Cổng AND và OR",
    "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>AND</th><th>OR</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td></tr></tbody></table><p>AND chỉ ra 1 khi TẤT CẢ đầu vào đều 1. OR ra 1 khi ÍT NHẤT MỘT đầu vào là 1.</p>",
    "explain": "<p>AND và OR là hai cổng cơ bản nhất, thường bị nhầm với nhau. Cách nhớ chắc chắn nhất: hãy tưởng tượng AND như một dây xích cần TẤT CẢ các mắt xích đều chắc mới chịu được lực, chỉ cần một mắt xích lỏng (giá trị 0) là cả dây đứt (kết quả 0). OR ngược lại, giống như một mạng lưới nhiều cửa thoát hiểm: chỉ cần MỘT cửa mở (giá trị 1) là người ta thoát được, không cần mọi cửa đều mở.</p><p>Nhìn vào bảng chân trị: AND chỉ có đúng một hàng cho ra 1 (khi cả A và B đều là 1), còn OR có tới ba hàng cho ra 1 (chỉ có đúng một hàng cho ra 0, khi cả A và B đều là 0). Đây là cách nhanh nhất để phân biệt hai cổng khi nhìn vào bảng chân trị mà quên mất định nghĩa bằng lời.</p>",
    "img": "logic_apps_p18.jpg"
   },
   {
    "title": "Cổng NOT (đảo)",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Cổng NOT</div><div class='pd-formula-math'>Y = A′</div></div><p>NOT chỉ có 1 đầu vào, đảo ngược trạng thái: đầu vào 0 → đầu ra 1, đầu vào 1 → đầu ra 0.</p>",
    "explain": "<p>NOT là cổng đơn giản nhất vì chỉ có một đầu vào duy nhất, không cần bảng chân trị 4 hàng như các cổng 2 đầu vào khác, chỉ cần 2 hàng. Ký hiệu dấu phẩy trên (A′, đọc là “A phẩy” hoặc “not A”) hoặc dấu gạch ngang trên đầu chữ cái đều mang cùng một ý nghĩa: đảo ngược giá trị.</p><p>Một mẹo nhớ trực quan: NOT giống như một cái gương phản chiếu ngược lại đúng giá trị nhận được, không hề “suy nghĩ” gì thêm, chỉ đơn giản lật ngược 0 thành 1 và 1 thành 0.</p>",
    "img": "logic_apps_p16.jpg"
   },
   {
    "title": "Cổng NAND và NOR",
    "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>NAND</th><th>NOR</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table><p>NAND = NOT(AND), NOR = NOT(OR): mỗi cổng chỉ đơn giản đảo ngược toàn bộ cột kết quả của AND/OR tương ứng.</p>",
    "explain": "<p>NAND và NOR là hai cổng “phái sinh”: lấy đúng kết quả của AND hoặc OR rồi đảo ngược toàn bộ cột kết quả đó. Cách nhớ nhanh nhất không cần lập bảng chân trị mới từ đầu: lấy bảng AND đã biết, đảo hết cột kết quả (0 thành 1, 1 thành 0) sẽ ra ngay bảng NAND; làm y hệt với OR sẽ ra bảng NOR.</p><p>Đây chính là điều tên gọi “NOT-AND” (viết tắt NAND) và “NOT-OR” (viết tắt NOR) đã nói rõ ngay từ đầu: không cần học thuộc lòng riêng biệt hai bảng chân trị mới, chỉ cần nhớ quy tắc “lấy AND/OR rồi đảo ngược” là suy ra được ngay.</p>",
    "img": "logic_apps_p28.jpg"
   },
   {
    "title": "Cổng XOR và XNOR",
    "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>XOR</th><th>XNOR</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td></tr></tbody></table><p>XOR ra 1 khi hai đầu vào KHÁC nhau; XNOR (đảo của XOR) ra 1 khi hai đầu vào GIỐNG nhau : thường dùng để so sánh bit.</p>",
    "explain": "<p>XOR (Exclusive-OR, HOẶC LOẠI TRỪ) là cổng dễ gây nhầm lẫn nhất vì tên gọi gần giống OR nhưng ý nghĩa khác hẳn. OR thông thường chấp nhận cả trường hợp CẢ HAI đầu vào đều là 1, còn XOR thì KHÔNG: XOR chỉ ra 1 khi hai đầu vào KHÁC NHAU (một cái là 0, cái kia là 1), và ra 0 khi hai đầu vào GIỐNG NHAU (dù cùng là 0 hay cùng là 1).</p><p>Ứng dụng thực tế quan trọng nhất của XOR là so sánh bit: nếu bạn muốn biết hai tín hiệu có đang “đồng ý” với nhau hay không, XOR sẽ báo ngay 1 khi chúng bất đồng. XNOR là cổng đảo của XOR, nên logic ngược lại: ra 1 khi hai đầu vào giống nhau.</p>",
    "img": "logic_apps_p34.jpg"
   },
   {
    "title": "Ví dụ: mạch 3 đầu vào A·B + C",
    "body": "<p>Tính Y = A·B + C với A=1, B=0, C=1:</p><ul><li>Bước 1: A·B = 1·0 = 0</li><li>Bước 2: Y = 0 + C = 0 + 1 = 1</li></ul><p>Kết quả: Y = 1. Cách làm: luôn tính AND trước (ưu tiên như phép nhân), rồi tới OR (như phép cộng), giống thứ tự toán tử số học thông thường.</p>",
    "explain": "<p>Đây là bài tập đầu tiên áp dụng quy tắc tính toán biểu thức Boolean có nhiều phép toán: giống hệt trong số học, AND (phép nhân) luôn được tính TRƯỚC OR (phép cộng) khi không có dấu ngoặc, đúng quy tắc “nhân trước, cộng sau” đã học từ lớp 1.</p><p>Với A=1, B=0, C=1, phải tính A·B trước (được 0), rồi mới cộng với C (0+1=1). Nếu tính sai thứ tự (cộng B+C trước rồi mới nhân với A), kết quả sẽ hoàn toàn khác. Luôn tự hỏi “phần nào có phép AND thì tính trước” mỗi khi gặp biểu thức có cả AND và OR.</p>"
   },
   {
    "title": "Ví dụ: mạch (A+B)·C",
    "body": "<p>Tính Y = (A+B)·C với A=0, B=1, C=0:</p><ul><li>Bước 1: A+B = 0+1 = 1</li><li>Bước 2: Y = 1·C = 1·0 = 0</li></ul><p>Kết quả: Y = 0. Dấu ngoặc buộc phải tính OR bên trong trước, dù AND thường có 'độ ưu tiên' cao hơn.</p>",
    "explain": "<p>Dấu ngoặc trong đại số Boolean có vai trò giống hệt trong toán số học thông thường: nó BẮT BUỘC phần bên trong phải được tính trước, bất kể phép toán bên trong đó là AND hay OR, và bất kể quy tắc “AND trước OR” thông thường.</p><p>Với (A+B)·C, dù OR thường được tính sau AND, nhưng vì OR nằm trong ngoặc nên phải tính A+B trước tiên (ra 1), rồi mới nhân với C (1·0=0). Đây là lỗi rất dễ mắc: nhiều người quên mất dấu ngoặc và áp dụng máy móc quy tắc “AND trước”, dẫn tới tính sai thứ tự hoàn toàn.</p>"
   },
   {
    "title": "Bảng tổng hợp 6 cổng cơ bản",
    "body": "<table class='tt'><thead><tr><th>Cổng</th><th>Ký hiệu</th><th>Ra 1 khi nào</th></tr></thead><tbody><tr><td>AND</td><td>A·B</td><td>mọi đầu vào = 1</td></tr><tr><td>OR</td><td>A+B</td><td>ít nhất 1 đầu vào = 1</td></tr><tr><td>NAND</td><td>(A·B)′</td><td>ít nhất 1 đầu vào = 0</td></tr><tr><td>NOR</td><td>(A+B)′</td><td>mọi đầu vào = 0</td></tr><tr><td>XOR</td><td>A⊕B</td><td>số đầu vào bằng 1 là LẺ</td></tr><tr><td>XNOR</td><td>(A⊕B)′</td><td>số đầu vào bằng 1 là CHẴN</td></tr></tbody></table>",
    "explain": "<p>Bảng tổng hợp này là công cụ tra cứu nhanh quan trọng nhất của cả Phần 1: thay vì phải nhớ 4 hàng bảng chân trị cho mỗi cổng trong 6 cổng, bạn chỉ cần nhớ ĐÚNG MỘT câu mô tả điều kiện “ra 1” của từng cổng.</p><p>Mẹo phân loại nhanh: AND và NAND liên quan tới “tất cả” (all), OR và NOR liên quan tới “ít nhất một” (at least one), còn XOR và XNOR liên quan tới việc đếm SỐ LƯỢNG đầu vào bằng 1 là chẵn hay lẻ. Ba cặp này, mỗi cặp gồm một cổng gốc và cổng đảo của nó (NAND đảo của AND, NOR đảo của OR, XNOR đảo của XOR).</p>",
    "img": "logic_apps_p04.jpg"
   },
   {
    "title": "⚠️ Bẫy: nhầm AND với OR khi đọc đề bằng lời",
    "body": "<div class='callout warn'><p>Từ 'và' trong tiếng Việt đôi khi được dùng lỏng lẻo cho cả hai nghĩa. Ví dụ đề bài 'đèn sáng khi công tắc A và công tắc B đều đóng' → đây là AND (cần CẢ HAI). Nhưng 'đèn sáng khi công tắc A hoặc công tắc B đóng' mới là OR. Luôn kiểm tra từ khóa 'đều/tất cả' (AND) so với 'hoặc/ít nhất một' (OR) trước khi vẽ mạch.</p></div>",
    "explain": "<p>Ngôn ngữ tự nhiên (cả tiếng Việt lẫn tiếng Anh) thường dùng từ “và”/“hoặc” một cách lỏng lẻo, không chặt chẽ như logic Boolean, nên đây là nguồn lỗi rất phổ biến khi chuyển một bài toán thực tế thành biểu thức logic.</p><p>Từ khoá đáng tin cậy nhất để nhận diện: nếu đề bài dùng “đều”, “tất cả”, “cả hai” thì đó là AND; nếu dùng “hoặc”, “ít nhất một”, “bất kỳ” thì đó là OR. Luôn gạch chân đúng những từ khoá này trong đề bài trước khi vẽ mạch, đừng dựa vào cảm giác đọc lướt qua.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Không chấm điểm: tự trả lời trước khi sang phần tiếp theo:</p><ul><li>Cổng nào cho ra 1 khi CẢ HAI đầu vào đều 0?</li><li>Nếu A=1, B=1, C=0, giá trị của A·B + C·A là bao nhiêu?</li></ul><p>Gợi ý đáp án: NOR; A·B+C·A = 1·1+0·1 = 1+0 = 1.</p>",
    "explain": "<p>Bài tự luyện áp dụng đúng hai kỹ năng vừa học: nhận diện cổng từ mô tả bảng chân trị (câu hỏi 1) và tính biểu thức nhiều phép toán theo đúng thứ tự ưu tiên (câu hỏi 2).</p><p>Với câu 2: A·B+C·A khi A=1,B=1,C=0, phải tính từng phép AND trước: A·B=1·1=1, C·A=0·1=0, rồi mới cộng hai kết quả: 1+0=1. Nếu bạn ra kết quả khác 1, rất có thể bạn đã cộng nhầm trước khi nhân, xem lại slide về thứ tự ưu tiên phép toán ở phía trên.</p>"
   }
  ],
  [
   {
    "title": "12 luật cơ bản của đại số Boolean",
    "body": "<table class='tt'><thead><tr><th>#</th><th>Luật</th></tr></thead><tbody><tr><td>1</td><td>A + 0 = A</td></tr><tr><td>2</td><td>A + 1 = 1</td></tr><tr><td>3</td><td>A · 0 = 0</td></tr><tr><td>4</td><td>A · 1 = A</td></tr><tr><td>5</td><td>A + A = A</td></tr><tr><td>6</td><td>A + A′ = 1</td></tr><tr><td>7</td><td>A · A = A</td></tr><tr><td>8</td><td>A · A′ = 0</td></tr><tr><td>9</td><td>A″ = A</td></tr><tr><td>10</td><td>A + AB = A</td></tr><tr><td>11</td><td>A + A′B = A + B</td></tr><tr><td>12</td><td>(A+B)(A+C) = A+BC</td></tr></tbody></table>",
    "explain": "<p>12 luật này không phải 12 công thức rời rạc cần học thuộc vẹt: chúng là những sự thật hiển nhiên nếu bạn thay A bằng 0 hoặc 1 và thử tính tay từng luật một. Ví dụ luật A+1=1: một cổng OR mà một đầu vào luôn là 1 thì đầu ra CHẮC CHẮN luôn là 1 bất kể đầu vào kia là gì, giống hệt việc “chỉ cần một cửa luôn mở sẵn thì phòng luôn có lối thoát”.</p><p>Hãy dùng các slide tiếp theo để hiểu Ý NGHĨA của từng nhóm luật (giao hoán, kết hợp, phân phối, De Morgan) thay vì cố nhồi nhét học thuộc cả bảng ngay từ slide này.</p>",
    "img": "logic_apps_p43.jpg"
   },
   {
    "title": "Luật giao hoán và kết hợp",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Giao hoán & kết hợp</div><div class='pd-formula-math'>A+B = B+A &nbsp;·&nbsp; (A+B)+C = A+(B+C)</div></div><p>Giống hệt số học thông thường: thứ tự cộng/nhân không ảnh hưởng kết quả, và cách nhóm ngoặc trong một chuỗi toàn AND (hoặc toàn OR) cũng không ảnh hưởng.</p>",
    "explain": "<p>Hai luật này đơn giản chỉ nói rằng: với một cổng AND hoặc OR thuần tuý (không trộn cả AND và OR), thứ tự viết các biến hoặc cách đặt dấu ngoặc không làm thay đổi kết quả, giống hệt trong số học (2+3=3+2, và (2+3)+4=2+(3+4)).</p><p>Điều cần lưu ý: hai luật này CHỈ áp dụng khi tất cả các số hạng dùng CÙNG một phép toán (toàn AND hoặc toàn OR). Khi biểu thức trộn cả AND và OR, cần dùng tới luật phân phối ở slide tiếp theo, không thể áp dụng giao hoán/kết hợp một cách ngây thơ.</p>"
   },
   {
    "title": "Luật phân phối",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Phân phối</div><div class='pd-formula-math'>A·(B+C) = A·B + A·C</div></div><p>Đây là bước then chốt để chuyển một biểu thức từ dạng tích-của-tổng (POS) sang tổng-của-tích (SOP): dạng chuẩn thường dùng khi thiết kế mạch AND-OR.</p>",
    "explain": "<p>Luật phân phối là chiếc cầu nối quan trọng nhất giữa hai dạng AND và OR trộn lẫn nhau, đóng vai trò y hệt phép nhân phân phối qua phép cộng trong số học (2×(3+4)=2×3+2×4).</p><p>Ý nghĩa thực tiễn: luật này cho phép “phá ngoặc” một biểu thức tích-của-tổng (POS, ví dụ A·(B+C)) thành dạng tổng-của-tích (SOP, ví dụ A·B+A·C). Dạng SOP là dạng chuẩn hay dùng nhất khi thiết kế mạch AND-OR hai tầng, sẽ được học chi tiết ở Phần 3.</p>"
   },
   {
    "title": "Ví dụ rút gọn: A + AB",
    "body": "<p>Rút gọn Y = A + AB theo luật 10 (A + AB = A):</p><ul><li>Áp dụng trực tiếp luật 10 → Y = A</li></ul><p>Kiểm tra bằng bảng chân trị: khi A=0, AB=0 nên Y=0=A; khi A=1, Y=1+B=1=A. Khớp cho mọi trường hợp → xác nhận luật 10 đúng.</p>",
    "explain": "<p>Luật số 10 (A+AB=A) nghe có vẻ khó tin lúc đầu: tại sao thêm hẳn một số hạng AB vào biểu thức mà kết quả cuối cùng lại KHÔNG đổi? Câu trả lời nằm ở việc kiểm tra từng trường hợp: khi A=0, số hạng AB luôn bằng 0 (vì 0 nhân gì cũng ra 0) nên Y=0+0=0=A; khi A=1, số hạng thứ hai AB không quan trọng nữa vì Y=1+B luôn bằng 1 (theo luật A+1... không, ở đây là 1+B=1 vì OR với 1 luôn ra 1), và A cũng bằng 1, nên Y=1=A.</p><p>Bài học quan trọng hơn cả kết quả: luôn kiểm tra lại một luật rút gọn bằng cách thử TỪNG giá trị của biến, đừng chỉ tin vào công thức suông.</p>"
   },
   {
    "title": "Ví dụ rút gọn: AB + AB′",
    "body": "<p>Rút gọn Y = AB + AB′:</p><ul><li>Bước 1: đặt A làm nhân tử chung → Y = A(B + B′)</li><li>Bước 2: áp dụng luật 6 (B+B′=1) → Y = A·1</li><li>Bước 3: áp dụng luật 4 (A·1=A) → Y = A</li></ul>",
    "explain": "<p>Đây là một ví dụ rút gọn hoàn chỉnh 3 bước, mỗi bước áp dụng đúng MỘT luật đã học, không nhảy cóc. Bước 1 dùng “đặt nhân tử chung” (giống hệt đặt thừa số chung trong đại số thông thường: AB+AB′=A(B+B′)). Bước 2 dùng luật 6 (B+B′=1, một biến OR với chính nó bị đảo LUÔN LUÔN ra 1, vì hoặc B=1 hoặc B′=1, không bao giờ cả hai cùng 0). Bước 3 dùng luật 4 (A·1=A, nhân với 1 không đổi giá trị).</p><p>Cách trình bày từng bước rõ ràng thế này chính là kỹ năng cần luyện: khi làm bài rút gọn dài hơn, luôn ghi rõ ĐANG dùng luật số mấy ở mỗi bước, để dễ tự kiểm tra lại nếu sai.</p>"
   },
   {
    "title": "Ví dụ rút gọn nhiều bước: AB + A′C + BC",
    "body": "<p>Rút gọn Y = AB + A′C + BC (định lý đồng nhất/consensus theorem):</p><ul><li>Số hạng BC là 'dư thừa' khi đã có AB và A′C</li><li>Kết quả rút gọn: Y = AB + A′C</li></ul><p>Đây là ví dụ kinh điển cho thấy rút gọn Boolean đôi khi cần nhận ra một số hạng hoàn toàn dư thừa (consensus term), không chỉ áp dụng luật cơ bản từng bước.</p>",
    "explain": "<p>Đây là ví dụ khó nhất trong Phần 2, vì bước rút gọn số hạng BC không đến từ việc áp dụng máy móc một luật cơ bản nào trong 12 luật, mà đòi hỏi NHẬN RA rằng BC là “số hạng dư thừa” khi đã có sẵn AB và A′C.</p><p>Trực giác đơn giản: nếu AB=1 thì chắc chắn B=1; nếu A′C=1 thì chắc chắn A′=1 (tức A=0). Xét mọi trường hợp B và C cùng bằng 1: hoặc A=1 (khi đó AB=1, số hạng BC dù có mặt hay không cũng không ảnh hưởng vì Y đã bằng 1), hoặc A=0 (khi đó A′C=1, cũng đã đủ làm Y=1). Vậy BC không bao giờ là số hạng “cứu” được trường hợp mà AB và A′C đều chưa cứu, nên bỏ nó đi không ảnh hưởng kết quả.</p>"
   },
   {
    "title": "Định lý De Morgan",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>De Morgan</div><div class='pd-formula-math'>(A·B)′ = A′ + B′ &nbsp;&nbsp; (A+B)′ = A′·B′</div></div><ul class='pd-legend'><li><b>Ý nghĩa</b><span>đảo dấu của tích = tổng các đảo; đảo dấu của tổng = tích các đảo</span></li></ul>",
    "explain": "<p>De Morgan là định lý quan trọng bậc nhất trong toàn bộ đại số Boolean, vì nó cho biết cách “phá” dấu đảo (NOT) khi dấu đảo đó bao trùm cả một cụm AND hoặc OR, một thao tác cực kỳ hay gặp khi đơn giản hoá mạch.</p><p>Cách nhớ trực quan không cần học thuộc công thức: khi đảo một biểu thức có dấu ngoặc, hãy làm hai việc CÙNG LÚC: đổi phép toán bên trong (AND thành OR, hoặc OR thành AND), và đảo TỪNG biến riêng lẻ bên trong ngoặc. Nhớ đúng “đổi phép toán + đảo từng biến” là đủ để áp dụng đúng De Morgan mà không cần nhớ công thức bằng ký hiệu.</p>",
    "img": "logic_demorgan_nand.png"
   },
   {
    "title": "Ứng dụng De Morgan: đơn giản hoá (A′B′)′",
    "body": "<p>Rút gọn Y = (A′B′)′:</p><ul><li>Áp dụng De Morgan: (A′B′)′ = (A′)′ + (B′)′ = A + B</li></ul><p>Kết quả Y = A + B: một cổng NAND với 2 đầu vào đã đảo tương đương một cổng OR thường, minh hoạ vì sao NAND được coi là cổng vạn năng.</p>",
    "explain": "<p>Đây là một trong những kết quả bất ngờ nhất mà De Morgan mang lại: một cổng NAND (hai đầu vào đã bị đảo trước khi đưa vào) hoá ra tương đương HOÀN TOÀN với một cổng OR bình thường. Điều này giải thích vì sao cổng NAND được gọi là “cổng vạn năng” (universal gate): chỉ với NAND, người ta có thể dựng lại được cả AND, OR, và NOT.</p><p>Về mặt thực hành trong công nghiệp bán dẫn, đây không chỉ là một trò chơi công thức: nhà sản xuất chip có thể sản xuất hàng loạt CHỈ một loại cổng NAND, rồi ghép chúng lại theo nhiều cách khác nhau để tạo ra mọi loại cổng khác, giúp đơn giản hoá và giảm chi phí sản xuất.</p>"
   },
   {
    "title": "Bảng chân trị và Karnaugh map 2 biến",
    "body": "<p>Với Y = A′B + AB′ + AB (3 tổ hợp cho ra 1 trong 4 tổ hợp có thể):</p><table class='tt'><thead><tr><th>A\\B</th><th>0</th><th>1</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></tbody></table><p>Nhóm 2 ô kề trong K-map (hàng dưới) cho A, nhóm cột phải cho B → rút gọn về Y = A + B.</p>",
    "explain": "<p>Bìa Karnaugh (K-map) 2 biến là công cụ trực quan hoá bảng chân trị thành một lưới ô vuông, giúp mắt người NHÌN THẤY ngay các nhóm số 1 liền kề thay vì phải áp dụng đại số từng bước.</p><p>Với bảng đã cho, hàng dưới (A=1) toàn số 1: nhóm 2 ô này lại cho ra đúng biến A (không phụ thuộc B). Cột phải (B=1) cũng toàn số 1: nhóm này cho ra đúng biến B. Việc “thấy” được hai nhóm chồng lấn này trực tiếp trên lưới nhanh hơn nhiều so với làm đại số Boolean từng bước, đặc biệt khi số biến tăng lên 3 hoặc 4.</p>"
   },
   {
    "title": "⚠️ Bẫy: áp dụng De Morgan sai khi có 3 biến trở lên",
    "body": "<div class='callout warn'><p>Nhiều người chỉ đảo dấu phép toán ngoài cùng mà quên đảo TỪNG biến bên trong. (ABC)′ KHÔNG PHẢI là A′B′C: đáp án đúng là (ABC)′ = A′+B′+C′ (áp dụng liên tiếp De Morgan cho từng cặp biến).</p></div>",
    "explain": "<p>Đây là lỗi cực kỳ phổ biến khi áp dụng De Morgan cho 3 biến trở lên: nhiều người chỉ đảo dấu phép toán ở NGOÀI CÙNG mà quên phải đảo TỪNG biến bên trong. (ABC)′ tuyệt đối KHÔNG bằng A′B′C (chỉ đảo biến đầu tiên), mà phải đảo cả ba biến VÀ đổi phép toán: (ABC)′=A′+B′+C′.</p><p>Cách kiểm tra không cần nhớ công thức: áp dụng De Morgan LIÊN TIẾP từng cặp một, giống bóc từng lớp hành. (ABC)′=((AB)C)′, áp dụng De Morgan cho ngoặc ngoài trước: =(AB)′+C′, rồi áp dụng tiếp cho (AB)′: =(A′+B′)+C′=A′+B′+C′. Làm từng bước nhỏ như vậy sẽ không bao giờ bỏ sót biến nào.</p>"
   }
  ],
  [
   {
    "title": "Mạch tổ hợp là gì?",
    "body": "<p>Mạch tổ hợp (combinational logic) là mạch mà đầu ra tại một thời điểm CHỈ phụ thuộc vào giá trị đầu vào hiện tại, không phụ thuộc lịch sử/trạng thái trước đó: khác với mạch tuần tự (sequential) có nhớ trạng thái (sẽ học ở phần bistable).</p>",
    "explain": "<p>Định nghĩa “mạch tổ hợp” nghe trừu tượng, nhưng có một cách kiểm tra rất cụ thể: nếu bạn thiết lập đúng các giá trị đầu vào của một mạch tổ hợp, đầu ra sẽ LUÔN LUÔN giống hệt nhau mỗi lần, bất kể mạch đã “trải qua” những gì trước đó. Một cổng AND đơn giản là ví dụ điển hình: A=1,B=1 luôn cho ra 1, dù 1 giây trước đó đầu vào là gì đi nữa.</p><p>Ngược lại, mạch tuần tự (sẽ gặp ở Phần 4 với flip-flop) có “trí nhớ”: cùng một giá trị đầu vào có thể cho ra hai đầu ra khác nhau tuỳ vào trạng thái trước đó của mạch. Phân biệt được hai loại này là nền tảng để hiểu toàn bộ phần còn lại của module.</p>"
   },
   {
    "title": "Từ bài toán thực tế tới bảng chân trị",
    "body": "<p>Bài toán: đèn cảnh báo cửa càng đáp (Landing Gear Door Warning) sáng khi CÓ ÍT NHẤT MỘT trong 2 cửa (trái/phải) chưa khoá VÀ máy bay đang bay (không phải trên mặt đất).</p><p>Đặt L = cửa trái chưa khoá, R = cửa phải chưa khoá, F = đang bay (in-flight). Cần: Warning = (L+R)·F.</p>",
    "explain": "<p>Đây là bước quan trọng nhất trong toàn bộ quy trình thiết kế mạch số: dịch một câu mô tả bằng lời (ngôn ngữ tự nhiên) thành các biến logic rõ ràng và một biểu thức Boolean chính xác. Bước này thường bị bỏ qua vội vàng, nhưng chính là nơi dễ hiểu sai đề bài nhất.</p><p>Với bài toán cửa càng đáp: cụm từ “ít nhất một cửa chưa khoá” dịch thành phép OR (L+R), còn cụm từ “VÀ đang bay” dịch thành phép AND với biến F. Ghép lại đúng thứ tự: Warning=(L+R)·F, không phải L+R·F (thiếu ngoặc sẽ làm sai hoàn toàn ý nghĩa, vì khi đó theo thứ tự ưu tiên AND trước, R·F sẽ được tính trước, sai hẳn ý đồ ban đầu).</p>"
   },
   {
    "title": "Bảng chân trị mạch cảnh báo cửa càng đáp",
    "body": "<table class='tt'><thead><tr><th>L</th><th>R</th><th>F</th><th>Warning=(L+R)·F</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table><p>Hàng cuối minh hoạ: dù cả 2 cửa chưa khoá (L=R=1), nếu máy bay đang ở mặt đất (F=0) thì KHÔNG cảnh báo: đúng logic AND với F.</p>",
    "explain": "<p>Bảng chân trị này chỉ cần liệt kê những tổ hợp có Ý NGHĨA THỰC TẾ (ở đây giả định F là biến quan trọng nhất nên được xét đủ hai giá trị, nhưng bảng đầy đủ 3 biến sẽ có 8 hàng; bảng rút gọn ở đây chọn lọc 4 hàng minh hoạ then chốt).</p><p>Hàng đáng chú ý nhất là hàng cuối: L=1, R=1 (cả hai cửa đều chưa khoá, trường hợp nguy hiểm nhất xét riêng về cửa), nhưng F=0 (máy bay đang ở mặt đất) thì Warning vẫn bằng 0, KHÔNG cảnh báo. Đây chính là điểm mấu chốt của phép AND với F: dù điều kiện cửa tệ tới đâu, máy bay ở mặt đất thì không cần cảnh báo phi công giữa lúc đang cất/hạ cánh.</p>"
   },
   {
    "title": "Từ bảng chân trị tới sơ đồ cổng",
    "body": "<p>Sơ đồ mạch cho Warning = (L+R)·F cần:</p><ul><li>1 cổng OR 2 đầu vào (L, R) → cho ra tín hiệu 'có ít nhất 1 cửa mở'</li><li>1 cổng AND 2 đầu vào (đầu ra OR, và F) → cho ra tín hiệu cảnh báo cuối cùng</li></ul>",
    "explain": "<p>Việc vẽ sơ đồ cổng logic từ biểu thức Boolean gần như là “dịch ngược”: mỗi phép toán trong biểu thức tương ứng với đúng một cổng vật lý. Warning=(L+R)·F có hai phép toán (một OR, một AND), nên sơ đồ cần đúng hai cổng.</p><p>Thứ tự vẽ luôn đi từ TRONG NGOẶC ra ngoài: cổng OR (nhận L, R) phải được vẽ và tính trước, đầu ra của nó mới được đưa vào làm một trong hai đầu vào của cổng AND (đầu vào còn lại là F). Nếu vẽ sai thứ tự (đưa L, R, F cùng vào một cổng AND ba đầu vào), mạch sẽ tính sai hoàn toàn ý nghĩa phép OR.</p>",
    "img": "logic_apps_p25.jpg"
   },
   {
    "title": "Ví dụ 2: mạch khởi động APU (đơn giản hoá)",
    "body": "<p>Theo Tooley: mạch điều khiển khởi động APU (auxiliary power unit) cần điều kiện AND của nhiều tín hiệu an toàn (vd: không có cảnh báo cháy, tốc độ động cơ trong ngưỡng an toàn) trước khi cho phép relay khởi động đóng mạch: một ví dụ AND nhiều đầu vào trong thực tế, không chỉ 2 biến như ví dụ cửa càng đáp.</p>",
    "explain": "<p>Ví dụ khởi động APU (Auxiliary Power Unit, động cơ phụ trợ cấp điện/khí nén khi động cơ chính chưa chạy) cho thấy AND nhiều đầu vào trong thực tế không hề hiếm: an toàn hàng không thường đòi hỏi RẤT NHIỀU điều kiện phải đồng thời đúng trước khi cho phép một hành động quan trọng xảy ra.</p><p>Nguyên tắc thiết kế an toàn ở đây là “fail-safe”: chỉ cần MỘT điều kiện an toàn không thoả (ví dụ có cảnh báo cháy), toàn bộ chuỗi AND lập tức cho ra 0, ngăn không cho relay khởi động đóng mạch. Đây là lý do AND nhiều đầu vào (không chỉ 2 biến) xuất hiện rất phổ biến trong các hệ thống bảo vệ an toàn của máy bay.</p>"
   },
   {
    "title": "Thiết kế mạch 3 biến từ bảng chân trị (SOP)",
    "body": "<p>Cho bảng chân trị Y=1 khi (A,B,C) = (0,1,1) hoặc (1,0,1). Viết dạng tổng-của-tích (SOP) bằng cách lấy OR của các minterm ứng với mỗi hàng có Y=1:</p><div class='pd-formula'><div class='pd-formula-math'>Y = A′BC + AB′C</div></div><p>Rút gọn tiếp bằng cách đặt C chung: Y = C(A′B + AB′) = C(A⊕B).</p>",
    "explain": "<p>SOP (Sum of Products, tổng-của-tích) là một quy trình CƠ HỌC để viết biểu thức Boolean trực tiếp từ bảng chân trị, không cần đoán mò: với mỗi hàng có Y=1, viết ra đúng một “minterm” (một cụm AND của tất cả các biến, viết nguyên bản nếu biến đó bằng 1 trong hàng đó, viết đảo nếu biến đó bằng 0), rồi OR tất cả các minterm này lại với nhau.</p><p>Với (A,B,C)=(0,1,1) cho Y=1: A=0 nên viết A′, B=1 nên viết B, C=1 nên viết C, ghép AND lại được A′BC. Làm tương tự với hàng (1,0,1) được AB′C. OR hai minterm lại: Y=A′BC+AB′C. Sau đó mới rút gọn tiếp bằng đại số (ở đây đặt C chung, dùng nhận diện A′B+AB′=A⊕B).</p>"
   },
   {
    "title": "Mạch AND-OR hai tầng",
    "body": "<p>Một mạch tổ hợp SOP tổng quát luôn có thể vẽ dưới dạng 2 tầng: TẦNG 1 là các cổng AND (mỗi cổng ứng với 1 số hạng tích), TẦNG 2 là MỘT cổng OR gộp tất cả đầu ra của tầng 1: đây là cấu trúc chuẩn dùng khi lập trình PLD/PAL.</p>",
    "explain": "<p>Kiến trúc “AND-OR hai tầng” là một sự thật toán học rất mạnh: BẤT KỲ hàm Boolean nào, dù phức tạp tới đâu, luôn có thể viết được dưới dạng SOP, và do đó luôn vẽ được bằng đúng 2 tầng cổng (tầng AND rồi tới tầng OR), không cần nhiều tầng lồng nhau phức tạp hơn.</p><p>Đây chính là lý do các chip PLD/PAL (Programmable Logic Device) được thiết kế sẵn với cấu trúc cố định “một mảng AND rồi tới một mảng OR”: người lập trình chỉ cần cấu hình đúng các kết nối, không cần lo về việc “có đủ tầng cổng hay không” cho bất kỳ hàm logic nào.</p>"
   },
   {
    "title": "So sánh SOP và POS",
    "body": "<table class='tt'><thead><tr><th></th><th>SOP (tổng-của-tích)</th><th>POS (tích-của-tổng)</th></tr></thead><tbody><tr><td>Dạng</td><td>Y = AB + A′C</td><td>Y = (A+C)(A′+B)</td></tr><tr><td>Lấy từ</td><td>các hàng có Y=1 (minterm)</td><td>các hàng có Y=0 (maxterm), rồi đảo</td></tr><tr><td>Cấu trúc mạch</td><td>AND rồi OR</td><td>OR rồi AND</td></tr></tbody></table>",
    "explain": "<p>SOP và POS là hai cách viết TƯƠNG ĐƯƠNG của cùng một hàm Boolean, chỉ khác ở điểm xuất phát: SOP xuất phát từ các hàng CÓ Y=1 (minterm), còn POS xuất phát từ các hàng CÓ Y=0 (maxterm), rồi áp dụng De Morgan để đảo ngược lại.</p><p>Lựa chọn dùng SOP hay POS trong thực tế thường phụ thuộc vào việc dạng nào cho ra biểu thức GỌN HƠN sau khi rút gọn: nếu bảng chân trị có ÍT hàng Y=1 hơn hàng Y=0, SOP thường gọn hơn (ít minterm cần OR lại); ngược lại thì POS có thể gọn hơn.</p>"
   },
   {
    "title": "⚠️ Bẫy: quên kiểm tra lại toàn bộ bảng chân trị sau khi rút gọn",
    "body": "<div class='callout warn'><p>Sau khi rút gọn biểu thức bằng đại số, LUÔN dựng lại bảng chân trị của biểu thức đã rút gọn và so với bảng gốc cho TẤT CẢ tổ hợp: chỉ kiểm tra 1-2 hàng dễ khiến bỏ sót lỗi rút gọn sai ở một nhánh ít gặp.</p></div>",
    "explain": "<p>Đây là một thói quen kiểm tra chất lượng cực kỳ quan trọng nhưng rất hay bị bỏ qua khi làm bài tập: sau khi rút gọn một biểu thức bằng đại số qua nhiều bước, RẤT DỄ mắc lỗi ở một bước trung gian nào đó mà không nhận ra ngay.</p><p>Cách kiểm tra chắc chắn nhất: dựng lại TOÀN BỘ bảng chân trị của biểu thức đã rút gọn (tất cả các tổ hợp biến có thể, không chỉ 1-2 hàng ngẫu nhiên), rồi so với bảng chân trị GỐC ban đầu. Nếu khớp ở TẤT CẢ các hàng, phép rút gọn chắc chắn đúng; nếu chỉ kiểm tra 1-2 hàng “cho có” mà bỏ qua các hàng còn lại, rất dễ bỏ sót một lỗi rút gọn nằm ở nhánh ít gặp.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Không chấm điểm: viết biểu thức SOP cho mạch có Y=1 khi (A,B)=(0,1) hoặc (1,1). Gợi ý: Y = A′B + AB, rút gọn theo luật 11/luật hấp thụ sẽ ra Y = B.</p>",
    "explain": "<p>Bài tự luyện áp dụng đúng quy trình SOP đã học: với Y=1 khi (A,B)=(0,1) hoặc (1,1), viết hai minterm tương ứng (A′B cho hàng đầu, AB cho hàng sau) rồi OR lại: Y=A′B+AB.</p><p>Bước rút gọn tiếp theo dùng đúng luật 11 (A+A′B=A+B, đảo vai trò một chút: ở đây là B+A′B=B+A theo cách viết khác, hoặc trực tiếp đặt B làm nhân tử chung: Y=B(A′+A)=B·1=B theo luật 6 và luật 4). Kết quả B đơn giản hơn NHIỀU so với biểu thức SOP ban đầu, minh hoạ rõ giá trị của bước rút gọn đại số sau khi viết SOP thô.</p>"
   }
  ],
  [
   {
    "title": "Tri-state logic là gì?",
    "body": "<p>Logic 3 trạng thái (tri-state) có thêm trạng thái thứ 3 ngoài 0 và 1: trở kháng cao (High-Z), tại đó đầu ra 'ngắt' khỏi mạch như thể không kết nối. Điều này cho phép NHIỀU thiết bị chia sẻ chung MỘT đường bus mà không gây xung đột tín hiệu.</p>",
    "explain": "<p>Logic 3 trạng thái nghe có vẻ mâu thuẫn với nguyên lý “chỉ có 2 mức điện áp” đã học ở Module 01, nhưng thực ra không mâu thuẫn: High-Z không phải một MỨC ĐIỆN ÁP thứ ba, mà là trạng thái đầu ra hoàn toàn “buông tay”, không đẩy dòng điện ra cũng không hút dòng điện vào, giống hệt một công tắc đèn đang ở vị trí giữa, không nối vào đâu cả.</p><p>Lợi ích cốt lõi: nếu không có High-Z, mỗi thiết bị nối vào một đường bus chung sẽ luôn “cố gắng” áp đặt mức điện áp của mình lên đường dây, gây xung đột khi nhiều thiết bị nối chung. High-Z cho phép một thiết bị “im lặng hoàn toàn”, nhường đường bus cho thiết bị khác.</p>"
   },
   {
    "title": "Chân Enable trên bộ đệm tri-state",
    "body": "<table class='tt'><thead><tr><th>Enable</th><th>Input</th><th>Output</th></tr></thead><tbody><tr><td>0</td><td>X (bất kỳ)</td><td>High-Z (ngắt)</td></tr><tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></tbody></table><p>Chỉ khi Enable=1, bộ đệm mới truyền tín hiệu đầu vào ra đầu ra; Enable=0 luôn cho High-Z bất kể input.</p>",
    "explain": "<p>Chân Enable hoạt động như một “công tắc tổng” quyết định bộ đệm có được phép lên tiếng hay không, hoàn toàn tách biệt khỏi giá trị Input đang là gì. Bảng chân trị cho thấy rõ: dù Input là 0 hay 1, chỉ cần Enable=0 thì Output LUÔN LUÔN là High-Z, Input bị “khoá lại” không truyền ra ngoài.</p><p>Chỉ khi Enable=1, bộ đệm mới “mở cửa” cho Input đi thẳng qua Output không đổi. Đây là cơ chế cho phép nhiều thiết bị chia sẻ một đường bus: tại một thời điểm chỉ đúng một thiết bị được cấp Enable=1, mọi thiết bị còn lại đều Enable=0 để giữ im lặng ở High-Z.</p>"
   },
   {
    "title": "Vì sao bus cần tri-state",
    "body": "<p>Nếu 2 thiết bị cùng nối trực tiếp (không qua tri-state) vào 1 đường dây và một thiết bị đưa ra logic 1 trong khi thiết bị kia đưa ra logic 0 cùng lúc, sẽ xảy ra xung đột điện (bus contention): có thể gây hỏng linh kiện. Tri-state giải quyết bằng cách chỉ CHO PHÉP đúng 1 thiết bị 'nói' trên bus tại một thời điểm, các thiết bị còn lại ở High-Z.</p>",
    "explain": "<p>Hãy tưởng tượng hai người cùng hét lên hai từ khác nhau vào cùng một micro tại cùng một thời điểm: âm thanh thu được sẽ hỗn loạn, không nghe rõ ai nói gì. Trên một đường bus điện, nếu hai thiết bị cùng lúc cố gắng áp đặt logic 1 và logic 0 lên cùng một dây dẫn, dòng điện lớn bất thường có thể chạy qua (bus contention), sinh nhiệt và có nguy cơ làm hỏng vĩnh viễn linh kiện.</p><p>Giải pháp tri-state giống như một “quy tắc lịch sự”: tại một thời điểm, CHỈ đúng một thiết bị được phép “nói” (Enable=1, đưa ra 0 hoặc 1 rõ ràng), mọi thiết bị còn lại phải “im lặng hoàn toàn” (High-Z), không được cùng lúc cố gắng áp đặt tín hiệu của mình lên đường bus.</p>"
   },
   {
    "title": "Monostable (one-shot) là gì?",
    "body": "<p>Mạch đơn ổn định (monostable/one-shot) chỉ có 1 trạng thái ổn định. Khi nhận một xung kích (trigger), nó chuyển sang trạng thái thứ 2 trong một khoảng thời gian cố định (do hằng số RC quyết định), rồi TỰ ĐỘNG quay về trạng thái ổn định ban đầu.</p>",
    "explain": "<p>Từ “one-shot” (bắn một phát) mô tả rất chính xác hành vi của mạch monostable: nó chỉ phản ứng ĐÚNG MỘT LẦN cho mỗi xung kích, tạo ra một xung đầu ra có độ rộng CỐ ĐỊNH (không phụ thuộc độ rộng xung kích đầu vào), rồi tự động quay trở lại trạng thái nghỉ ban đầu mà không cần ai can thiệp.</p><p>Điểm mấu chốt cần nhớ: độ rộng của xung đầu ra được quyết định bởi các linh kiện R và C gắn ngoài mạch (hằng số thời gian RC), KHÔNG phụ thuộc vào việc xung kích đầu vào dài hay ngắn. Đây chính là lý do monostable được dùng để “chuẩn hoá” độ rộng một tín hiệu.</p>"
   },
   {
    "title": "Ứng dụng monostable",
    "body": "<p>Monostable thường dùng để tạo một xung có độ rộng CỐ ĐỊNH từ một xung kích có độ rộng bất kỳ (vd làm sạch/định hình tín hiệu nhiễu từ công tắc cơ khí: debounce), hoặc tạo trễ thời gian ngắn giữa 2 sự kiện trong một chuỗi điều khiển.</p>",
    "explain": "<p>Ứng dụng “debounce” (khử rung công tắc) là ví dụ kinh điển nhất của monostable: khi một công tắc cơ khí bị gạt, các tiếp điểm kim loại bên trong thực ra nảy qua nảy lại rất nhanh trong vài mili-giây trước khi ổn định hẳn, tạo ra một chuỗi xung nhiễu thay vì một cạnh chuyển trạng thái sạch sẽ.</p><p>Mạch monostable “lọc” chuỗi nhiễu này bằng cách chỉ phản ứng với xung kích ĐẦU TIÊN, rồi tạo ra một xung đầu ra sạch có độ rộng đủ dài để “che” hết khoảng thời gian nảy tiếp điểm còn lại, giúp mạch số phía sau chỉ nhận đúng MỘT sự kiện chuyển trạng thái duy nhất thay vì hàng chục xung nhiễu giả.</p>"
   },
   {
    "title": "Bistable (flip-flop) là gì?",
    "body": "<p>Mạch song ổn định (bistable) có HAI trạng thái ổn định, có thể duy trì mãi mãi cho tới khi có tín hiệu điều khiển làm nó chuyển trạng thái: đây chính là flip-flop, đơn vị nhớ 1-bit cơ bản của mọi mạch tuần tự (thanh ghi, bộ đếm, bộ nhớ).</p>",
    "explain": "<p>Từ “bistable” (song ổn định) nói lên đúng bản chất: mạch có HAI trạng thái đều ổn định như nhau, và một khi đã ở một trong hai trạng thái đó, nó sẽ Ở YÊN MÃI MÃI (không tự động quay về trạng thái nào cả, khác hẳn monostable) cho tới khi có một tín hiệu điều khiển bên ngoài chủ động yêu cầu nó đổi sang trạng thái kia.</p><p>Đây chính là cơ chế “nhớ” cơ bản nhất trong điện tử số: một bit dữ liệu (0 hoặc 1) được lưu giữ bằng cách mạch bistable duy trì đúng một trong hai trạng thái ổn định của nó, cho tới khi bị ghi đè bởi một lệnh ghi mới. Mọi thanh ghi, bộ đếm, và ô nhớ RAM tĩnh (SRAM) đều xây dựng từ nguyên lý này.</p>"
   },
   {
    "title": "Flip-flop R-S (Reset-Set) đơn giản",
    "body": "<table class='tt'><thead><tr><th>S</th><th>R</th><th>Q (tiếp theo)</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>giữ nguyên</td></tr><tr><td>1</td><td>0</td><td>1 (set)</td></tr><tr><td>0</td><td>1</td><td>0 (reset)</td></tr><tr><td>1</td><td>1</td><td>không hợp lệ</td></tr></tbody></table><p>Có thể dựng từ 2 cổng NOR hoặc 2 cổng NAND nối chéo: chính là ví dụ mạch dual R-S bistable dùng IC 4001 (CMOS NOR) nêu trong sách Tooley.</p>",
    "explain": "<p>Bảng chân trị flip-flop R-S đọc theo đúng nghĩa đen của tên gọi: S (Set) đặt đầu ra Q về 1, R (Reset) đặt Q về 0. Điều đặc biệt nhất nằm ở hàng đầu tiên (S=0, R=0): đầu ra Q “giữ nguyên” giá trị trước đó, đây chính là biểu hiện của “trí nhớ”, đầu ra không do đầu vào TẠI THỜI ĐIỂM HIỆN TẠI quyết định hoàn toàn, mà còn phụ thuộc lịch sử.</p><p>Hàng cuối (S=1, R=1) bị đánh dấu “không hợp lệ” vì đây là tình huống mạch được yêu cầu ĐỒNG THỜI set và reset, một mệnh lệnh mâu thuẫn mà mạch NOR/NAND chéo không thể xử lý nhất quán: kết quả thực tế phụ thuộc vào chi tiết trễ tín hiệu của từng cổng, không dự đoán chắc chắn được, nên luôn phải TRÁNH đưa mạch vào tổ hợp đầu vào này khi thiết kế.</p>"
   },
   {
    "title": "Bảng so sánh Monostable và Bistable",
    "body": "<table class='tt'><thead><tr><th></th><th>Monostable</th><th>Bistable</th></tr></thead><tbody><tr><td>Số trạng thái ổn định</td><td>1</td><td>2</td></tr><tr><td>Sau khi kích</td><td>tự quay về ban đầu</td><td>giữ nguyên tới khi bị đổi</td></tr><tr><td>Chức năng chính</td><td>tạo xung/độ trễ thời gian</td><td>lưu trữ 1 bit dữ liệu</td></tr></tbody></table>",
    "explain": "<p>Bảng so sánh này đúc kết lại điểm khác biệt cốt lõi nhất giữa hai loại mạch song ổn định và đơn ổn định chỉ trong một câu duy nhất: monostable TỰ ĐỘNG quay về sau một khoảng thời gian cố định (dùng để TẠO xung/độ trễ), còn bistable Ở YÊN MÃI MÃI cho tới khi bị chủ động thay đổi (dùng để LƯU TRỮ dữ liệu).</p><p>Ghi nhớ đúng một câu phân biệt này sẽ giúp bạn không bao giờ nhầm lẫn khi gặp một bài toán thực tế: nếu đề bài nói tới “tạo một xung có độ dài cố định” hay “làm chậm tín hiệu một khoảng thời gian”, đó là bài toán monostable; nếu đề bài nói tới “lưu lại trạng thái”, “nhớ đã bấm nút hay chưa”, đó là bài toán bistable.</p>"
   },
   {
    "title": "⚠️ Bẫy: nhầm High-Z với logic 0",
    "body": "<div class='callout warn'><p>High-Z KHÔNG phải là mức điện áp thấp (logic 0): đó là trạng thái đầu ra hoàn toàn 'thả nổi', không có dòng điện chảy ra. Đo bằng đồng hồ vạn năng ở chế độ điện áp có thể cho kết quả không ổn định/nhiễu vì đầu ra không được điều khiển bởi bất kỳ nguồn nào.</p></div>",
    "explain": "<p>Đây là một trong những bẫy đo lường thực tế hay gặp nhất khi làm việc với mạch tri-state: nhiều người mới học nghĩ rằng High-Z đơn giản là “logic 0” hay “điện áp thấp”, nhưng thực ra High-Z là trạng thái đầu ra hoàn toàn KHÔNG ĐƯỢC ĐIỀU KHIỂN bởi bất kỳ nguồn nào, không có dòng điện chảy ra từ đầu ra đó.</p><p>Hậu quả thực tế: nếu dùng đồng hồ vạn năng đo điện áp tại một chân đang ở High-Z, kết quả đo có thể dao động thất thường, bị nhiễu bởi các tín hiệu lân cận (do đầu vào của đồng hồ đo cũng có trở kháng hữu hạn), khác hẳn việc đo một chân đang thực sự ở logic 0 (luôn ổn định gần 0V). Đừng vội kết luận “mạch lỗi” chỉ vì thấy số đo dao động ở một chân tri-state đang ở High-Z.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Không chấm điểm: một bus có 4 thiết bị dùng chung, tại một thời điểm cho phép bao nhiêu thiết bị đang ở trạng thái KHÁC High-Z? Gợi ý: đúng 1 thiết bị (nguyên tắc chia sẻ bus).</p>",
    "explain": "<p>Nguyên tắc cốt lõi của việc chia sẻ bus bằng tri-state chỉ có đúng MỘT câu: tại bất kỳ thời điểm nào, dù bus có bao nhiêu thiết bị nối vào, luôn CHỈ ĐÚNG MỘT thiết bị được phép có Enable=1 (đang thực sự đưa ra 0 hoặc 1 lên bus), mọi thiết bị còn lại bắt buộc phải ở High-Z.</p><p>Với 4 thiết bị dùng chung một bus, đáp án luôn là 1, không phụ thuộc vào việc bus có bao nhiêu thiết bị: đây chính là nguyên tắc bảo vệ khỏi xung đột điện (bus contention) đã học ở slide đầu phần này, áp dụng cho MỌI số lượng thiết bị chia sẻ bus, không chỉ riêng trường hợp 4 thiết bị.</p>"
   }
  ],
  [
   {
    "title": "Vì sao cần nhiều họ logic khác nhau?",
    "body": "<p>Mỗi họ linh kiện logic (logic family) có đặc tính điện khác nhau: điện áp nguồn, tốc độ chuyển mạch, công suất tiêu thụ, khả năng chịu nhiễu: nên việc chọn đúng họ cho đúng ứng dụng (tốc độ cao, công suất thấp, môi trường nhiễu mạnh...) là một quyết định thiết kế quan trọng.</p>",
    "explain": "<p>“Họ logic” (logic family) là cách gọi một nhóm chip được chế tạo theo cùng một công nghệ bán dẫn (ví dụ toàn bằng transistor lưỡng cực, hay toàn bằng MOSFET), khiến chúng chia sẻ chung các đặc tính điện: mức điện áp nguồn cần cấp, tốc độ chuyển đổi giữa 0 và 1, lượng điện tiêu thụ, và khả năng chống nhiễu.</p><p>Không có một họ logic nào “tốt nhất tuyệt đối” cho mọi trường hợp: một họ nhanh thường tốn điện hơn, một họ tiết kiệm điện thường chậm hơn. Việc chọn đúng họ logic cho đúng ứng dụng (ví dụ mạch cần chạy pin lâu, hay mạch cần xử lý cực nhanh) là một quyết định kỹ thuật thực sự, không phải chi tiết vụn vặt.</p>"
   },
   {
    "title": "Họ TTL (Transistor-Transistor Logic)",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Nguồn TTL chuẩn</div><div class='pd-formula-math'>V_CC = 5V ± 5%</div></div><p>TTL dùng transistor lưỡng cực (BJT), tốc độ chuyển mạch nhanh, nhưng tiêu thụ dòng tĩnh lớn hơn CMOS: phù hợp ứng dụng cần tốc độ cao, ít quan tâm công suất.</p>",
    "explain": "<p>TTL (Transistor-Transistor Logic) là công nghệ logic ra đời sớm, dùng transistor lưỡng cực (BJT, loại transistor cổ điển hoạt động dựa trên dòng điện điều khiển, khác với MOSFET dùng điện áp điều khiển sẽ gặp ở CMOS).</p><p>Đặc điểm cần nhớ: TTL cần nguồn cấp khá chính xác, chỉ 5V và chỉ được dao động rất ít (±5%, tức từ 4.75V tới 5.25V), không linh hoạt như CMOS. Đổi lại, transistor lưỡng cực có tốc độ chuyển mạch nhanh, nên TTL từng là lựa chọn phổ biến cho các ứng dụng cần xử lý tốc độ cao vào thời kỳ nó thịnh hành.</p>"
   },
   {
    "title": "Các biến thể TTL",
    "body": "<table class='tt'><thead><tr><th>Biến thể</th><th>Đặc điểm</th></tr></thead><tbody><tr><td>Standard TTL</td><td>cơ bản, fan-out 10, noise margin ~400mV</td></tr><tr><td>LS-TTL (Low-power Schottky)</td><td>công suất thấp hơn, vẫn khá nhanh</td></tr><tr><td>S-TTL (Schottky)</td><td>nhanh hơn standard, công suất cao hơn</td></tr></tbody></table>",
    "explain": "<p>Ba biến thể TTL trong bảng cho thấy một sự đánh đổi rất điển hình trong thiết kế điện tử: tốc độ và công suất tiêu thụ thường TỈ LỆ THUẬN với nhau, muốn nhanh hơn thường phải trả giá bằng tiêu thụ điện nhiều hơn.</p><p>LS-TTL (Low-power Schottky) là phiên bản cải tiến dùng diode Schottky để giảm đáng kể công suất tiêu thụ so với TTL chuẩn, mà vẫn giữ được tốc độ khá tốt: đây là lý do LS-TTL từng trở thành biến thể TTL phổ biến nhất trong thực tế, cân bằng tốt giữa tốc độ và công suất so với hai lựa chọn còn lại.</p>"
   },
   {
    "title": "Họ CMOS (Complementary MOS)",
    "body": "<p>CMOS dùng cặp transistor MOSFET bổ sung (1 kênh N + 1 kênh P), gần như KHÔNG tiêu thụ dòng tĩnh khi ở trạng thái ổn định (chỉ tiêu thụ khi chuyển mạch): lý do CMOS thống trị các thiết bị chạy pin/di động hiện đại.</p>",
    "explain": "<p>CMOS (Complementary MOS) là bước tiến công nghệ quan trọng nhất trong lịch sử vi mạch số, dùng CẶP transistor MOSFET bổ sung cho nhau (một loại kênh N, một loại kênh P) trong mỗi cổng logic.</p><p>Điểm mấu chốt tạo nên ưu thế của CMOS: tại bất kỳ thời điểm ổn định nào (không đang chuyển mạch), LUÔN có đúng một trong hai transistor này ở trạng thái TẮT hoàn toàn, khiến gần như không có dòng điện nào chạy qua liên tục. CMOS chỉ tiêu thụ điện đáng kể trong khoảnh khắc CHUYỂN từ 0 sang 1 hoặc ngược lại: đây chính là lý do CMOS thống trị hoàn toàn các thiết bị điện tử chạy pin hiện đại, từ điện thoại tới đồng hồ thông minh.</p>"
   },
   {
    "title": "Ưu điểm CMOS: biên độ nhiễu cao",
    "body": "<p>Vì CMOS dùng gần trọn dải điện áp nguồn cho 2 mức logic (rail-to-rail), biên độ nhiễu (noise margin) của CMOS thường LỚN HƠN TTL đáng kể: chịu nhiễu tốt hơn trong môi trường điện từ khắc nghiệt như buồng động cơ/khoang điện tử máy bay.</p>",
    "explain": "<p>“Biên độ nhiễu” (noise margin) là khoảng cách an toàn giữa mức điện áp thực tế của tín hiệu và ngưỡng mà mạch sẽ hiểu nhầm mức logic: biên độ càng lớn, tín hiệu càng chịu được nhiễu điện từ bên ngoài mà không bị đọc sai.</p><p>CMOS thường dùng gần trọn cả dải điện áp nguồn cho hai mức logic (gọi là “rail-to-rail”, ví dụ mức thấp gần 0V và mức cao gần sát điện áp nguồn), trong khi TTL chỉ dùng một phần hẹp hơn của dải điện áp. Kết quả là CMOS thường có biên độ nhiễu lớn hơn TTL đáng kể, giải thích vì sao CMOS được ưu tiên trong môi trường điện từ khắc nghiệt như buồng động cơ hay khoang thiết bị điện tử của máy bay, nơi nhiễu điện từ các hệ thống khác luôn hiện diện.</p>"
   },
   {
    "title": "Bảng so sánh TTL và CMOS",
    "body": "<table class='tt'><thead><tr><th></th><th>TTL</th><th>CMOS</th></tr></thead><tbody><tr><td>Công nghệ transistor</td><td>lưỡng cực (BJT)</td><td>MOSFET bổ sung</td></tr><tr><td>Nguồn</td><td>5V ±5%</td><td>3V-15V (tuỳ dòng)</td></tr><tr><td>Công suất tĩnh</td><td>cao hơn</td><td>rất thấp</td></tr><tr><td>Biên độ nhiễu</td><td>~400mV</td><td>lớn hơn (rail-to-rail)</td></tr><tr><td>Phù hợp</td><td>tốc độ cao, ít quan tâm pin</td><td>thiết bị cầm tay/chạy pin</td></tr></tbody></table>",
    "explain": "<p>Bảng so sánh này gom lại đúng các điểm đã học riêng lẻ ở 4 slide trước thành một cái nhìn tổng quan duy nhất, giúp bạn tra cứu nhanh khi cần quyết định chọn họ logic nào cho một ứng dụng cụ thể.</p><p>Ghi nhớ hai “từ khoá quyết định” khi đọc bảng này: nếu ưu tiên hàng đầu là TỐC ĐỘ và không quá quan tâm tiêu thụ điện, nghiêng về TTL; nếu ưu tiên hàng đầu là TIẾT KIỆM ĐIỆN (chạy pin) hoặc CHỐNG NHIỄU tốt, nghiêng hẳn về CMOS.</p>"
   },
   {
    "title": "Ví dụ: chọn họ logic cho thiết bị kiểm tra cầm tay",
    "body": "<p>Bài toán (Tooley Ch.5 Q6): thiết bị kiểm tra cầm tay chạy pin cần họ logic nào? Vì tiêu chí quan trọng nhất là tiêu thụ điện thấp để kéo dài thời lượng pin, CMOS là lựa chọn phù hợp nhất trong 3 lựa chọn CMOS/TTL/LS-TTL.</p>",
    "explain": "<p>Bài toán chọn họ logic cho thiết bị kiểm tra cầm tay là một ví dụ áp dụng trực tiếp bảng so sánh vừa học vào tình huống thực tế: từ khoá quan trọng nhất trong đề bài là “chạy pin”, ngay lập tức gợi ý ưu tiên hàng đầu phải là TIẾT KIỆM ĐIỆN để kéo dài thời lượng sử dụng giữa các lần sạc.</p><p>Trong ba lựa chọn CMOS/TTL/LS-TTL, CMOS có công suất tĩnh thấp nhất (gần như không tiêu thụ khi không chuyển mạch), nên là lựa chọn hợp lý nhất. Đây chính là cách tư duy cần luyện: đọc đề bài, xác định TIÊU CHÍ QUAN TRỌNG NHẤT được nhấn mạnh, rồi tra lại đúng dòng tương ứng trong bảng so sánh, không cần nhớ tất cả chi tiết kỹ thuật.</p>"
   },
   {
    "title": "Fan-out và fan-in nhắc lại theo họ logic",
    "body": "<p>Fan-out chuẩn của TTL là 10 (điều khiển tối đa 10 đầu vào TTL cùng họ). CMOS thường có fan-out lớn hơn nhiều về mặt DC (do trở kháng vào cực cao), nhưng bị giới hạn thực tế bởi tốc độ (mỗi tải thêm làm chậm thời gian chuyển mạch do điện dung ký sinh).</p>",
    "explain": "<p>Fan-out (số tải tối đa một cổng có thể điều khiển) và fan-in (số đầu vào một cổng có thể nhận) là hai khái niệm đã gặp ở phần lý thuyết cổng logic cơ bản, nay được xem xét lại dưới góc độ khác biệt giữa các họ logic.</p><p>Điểm thú vị: TTL có fan-out cố định khá thấp (10) vì giới hạn bởi DÒNG ĐIỆN cần cấp cho mỗi tải. CMOS về lý thuyết có fan-out DC lớn hơn nhiều (vì đầu vào CMOS có trở kháng cực cao, gần như không rút dòng), nhưng trong thực tế vẫn bị giới hạn bởi TỐC ĐỘ: mỗi tải thêm vào sẽ cộng thêm một chút điện dung ký sinh, làm chậm dần thời gian chuyển mạch, nên số tải thực tế vẫn có giới hạn dù không phải do dòng điện.</p>"
   },
   {
    "title": "⚠️ Bẫy: trộn lẫn TTL và CMOS không đúng cách",
    "body": "<div class='callout warn'><p>Mức điện áp 'logic 1' của TTL (~2.4V trở lên) có thể KHÔNG đủ để CMOS công suất chuẩn (ngưỡng ~70% Vdd, vd 3.5V với Vdd=5V) nhận diện đúng là mức cao: cần dùng loại CMOS tương thích TTL (74HCT thay vì 74HC) khi ghép nối hai họ.</p></div>",
    "explain": "<p>Đây là một cạm bẫy thực tế rất dễ gặp khi hai hệ thống dùng hai họ logic khác nhau cần “nói chuyện” với nhau: mức điện áp mà TTL coi là “logic 1” (thường chỉ cần từ khoảng 2.4V trở lên) có thể KHÔNG ĐỦ CAO để một chip CMOS công suất chuẩn (dùng ngưỡng nhận diện logic 1 cao hơn, khoảng 70% điện áp nguồn, ví dụ 3.5V với nguồn 5V) nhận ra đúng là mức cao.</p><p>Hậu quả nếu ghép sai: chip CMOS có thể đọc nhầm tín hiệu “1” từ TTL thành “0”, gây lỗi logic khó phát hiện. Giải pháp chuẩn trong công nghiệp: dùng dòng CMOS có ký hiệu “T” (ví dụ 74HCT thay vì 74HC), được thiết kế riêng với ngưỡng nhận diện tương thích ngược với mức điện áp của TTL.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Không chấm điểm: một hệ thống buồng lái cần mạch logic chịu nhiễu điện từ mạnh và tiêu thụ điện thấp: nên ưu tiên họ logic nào? Gợi ý: CMOS (biên độ nhiễu cao + công suất tĩnh thấp).</p>",
    "explain": "<p>Bài tự luyện tổng hợp lại đúng hai tiêu chí quan trọng nhất đã học trong toàn bộ Phần 5: khả năng CHỐNG NHIỄU (biên độ nhiễu) và mức TIÊU THỤ ĐIỆN (công suất tĩnh), cả hai đều là thế mạnh nổi bật của CMOS so với TTL.</p><p>Một hệ thống buồng lái cần cả hai đặc tính này cùng lúc (chịu nhiễu điện từ mạnh từ các thiết bị lân cận, VÀ tiêu thụ điện thấp để giảm tải cho hệ thống điện máy bay): CMOS là lựa chọn phù hợp trên cả hai tiêu chí, không cần đánh đổi giữa chúng như khi so với TTL.</p>"
   }
  ]
 ],
 "en": [
  [
   {
    "title": "What is a logic gate?",
    "body": "<p>A logic gate is a circuit with one or more binary inputs (0 or 1) and ONE binary output, determined by a fixed Boolean function of its inputs. It is the smallest building block of every digital system.</p>",
    "explain": "<p>Picture a logic gate as a smart switch: it looks at one or more 0/1 signals coming in, then, following a fixed rule wired into the circuit that never changes, produces exactly one 0 or 1 output.</p><p>Everything complex a computer does, from addition to comparison to deciding whether to light a warning on an aircraft, is built by wiring together very large numbers of these simple gates. Mastering the 6 basic gates in this module is a prerequisite before any more complex digital circuit makes sense.</p>"
   },
   {
    "title": "AND and OR gates",
    "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>AND</th><th>OR</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td></tr></tbody></table><p>AND outputs 1 only when ALL inputs are 1. OR outputs 1 when AT LEAST ONE input is 1.</p>",
    "explain": "<p>AND and OR are the two most basic gates, and the ones most often confused. A reliable way to remember them: think of AND like a chain that needs every single link solid to hold weight, one weak link (a 0) and the whole chain fails (result 0). OR is the opposite, like a building with several exit doors: just one open door (a 1) lets people escape, not every door needs to be open.</p><p>Looking at the truth table: AND has exactly one row giving 1 (when both A and B are 1), while OR has three rows giving 1 (only one row gives 0, when both A and B are 0). This is the fastest way to tell the two apart from a truth table alone, without recalling the wording of the definition.</p>",
    "img": "logic_apps_p18.jpg"
   },
   {
    "title": "The NOT gate (inverter)",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>NOT gate</div><div class='pd-formula-math'>Y = A′</div></div><p>NOT has a single input and inverts it: a 0 input gives a 1 output, a 1 input gives a 0 output.</p>",
    "explain": "<p>NOT is the simplest gate because it has only one input, so it needs just 2 rows instead of the 4-row truth table other 2-input gates require. The prime symbol (A′, read \"A prime\" or \"not A\") and the bar drawn over a letter both mean exactly the same thing: invert the value.</p><p>A visual way to remember it: NOT behaves like a mirror that reflects back the exact opposite of what it receives, with no further \"thinking\" involved, simply flipping 0 to 1 and 1 to 0.</p>",
    "img": "logic_apps_p16.jpg"
   },
   {
    "title": "NAND and NOR gates",
    "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>NAND</th><th>NOR</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table><p>NAND = NOT(AND), NOR = NOT(OR): each gate simply inverts the entire result column of its underlying AND/OR gate.</p>",
    "explain": "<p>NAND and NOR are \"derived\" gates: take the exact result of AND or OR and invert the whole output column. The fastest way to remember them without building a new truth table from scratch: take the AND table you already know and flip every result (0 becomes 1, 1 becomes 0) to get the NAND table; do the same to OR to get NOR.</p><p>This is exactly what the names \"NOT-AND\" (shortened to NAND) and \"NOT-OR\" (shortened to NOR) already tell you: no need to memorise two separate new truth tables, just remember the rule \"take AND/OR, then invert\".</p>",
    "img": "logic_apps_p28.jpg"
   },
   {
    "title": "XOR and XNOR gates",
    "body": "<table class='tt'><thead><tr><th>A</th><th>B</th><th>XOR</th><th>XNOR</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td></tr></tbody></table><p>XOR outputs 1 when the two inputs DIFFER; XNOR (the inverse of XOR) outputs 1 when they are the SAME: often used to compare bits.</p>",
    "explain": "<p>XOR (Exclusive-OR) is the gate most likely to cause confusion, since its name sounds close to OR but its meaning differs sharply. Ordinary OR accepts the case where BOTH inputs are 1, but XOR does not: XOR outputs 1 only when the two inputs are DIFFERENT (one is 0, the other is 1), and outputs 0 when they are the SAME (both 0 or both 1).</p><p>XOR's most important practical use is bit comparison: if you want to know whether two signals \"agree\" with each other, XOR immediately flags 1 whenever they disagree. XNOR is XOR's inverse, so its logic runs the other way: it outputs 1 when the two inputs match.</p>",
    "img": "logic_apps_p34.jpg"
   },
   {
    "title": "Worked example: A·B + C",
    "body": "<p>Evaluate Y = A·B + C with A=1, B=0, C=1:</p><ul><li>Step 1: A·B = 1·0 = 0</li><li>Step 2: Y = 0 + C = 0 + 1 = 1</li></ul><p>Result: Y = 1. Always evaluate AND first (like multiplication), then OR (like addition): the same operator precedence as ordinary arithmetic.</p>",
    "explain": "<p>This is the first exercise applying the rule for evaluating a Boolean expression with more than one operator: exactly as in ordinary arithmetic, AND (multiplication) is always computed BEFORE OR (addition) when there are no parentheses, the same \"multiply first, add second\" rule learned in primary school.</p><p>With A=1, B=0, C=1, you must compute A·B first (giving 0), then add C (0+1=1). Getting the order wrong (adding B+C before multiplying by A) gives a completely different answer. Always ask \"which part has an AND\" and compute that first whenever an expression mixes AND and OR.</p>"
   },
   {
    "title": "Worked example: (A+B)·C",
    "body": "<p>Evaluate Y = (A+B)·C with A=0, B=1, C=0:</p><ul><li>Step 1: A+B = 0+1 = 1</li><li>Step 2: Y = 1·C = 1·0 = 0</li></ul><p>Result: Y = 0. The parentheses force the OR inside to be evaluated first, even though AND usually has 'higher precedence'.</p>",
    "explain": "<p>Parentheses in Boolean algebra play exactly the same role as in ordinary arithmetic: they FORCE the enclosed part to be computed first, regardless of whether it contains AND or OR, and regardless of the usual \"AND before OR\" rule.</p><p>With (A+B)·C, even though OR is normally computed after AND, the OR here sits inside parentheses, so A+B must be computed first (giving 1), then multiplied by C (1·0=0). This is a very easy mistake: forgetting the parentheses and mechanically applying \"AND first\" leads to a completely wrong order of operations.</p>"
   },
   {
    "title": "Summary table of the 6 basic gates",
    "body": "<table class='tt'><thead><tr><th>Gate</th><th>Symbol</th><th>Outputs 1 when</th></tr></thead><tbody><tr><td>AND</td><td>A·B</td><td>every input = 1</td></tr><tr><td>OR</td><td>A+B</td><td>at least one input = 1</td></tr><tr><td>NAND</td><td>(A·B)′</td><td>at least one input = 0</td></tr><tr><td>NOR</td><td>(A+B)′</td><td>every input = 0</td></tr><tr><td>XOR</td><td>A⊕B</td><td>an ODD number of inputs are 1</td></tr><tr><td>XNOR</td><td>(A⊕B)′</td><td>an EVEN number of inputs are 1</td></tr></tbody></table>",
    "explain": "<p>This summary table is the single most useful quick-reference tool in Part 1: instead of memorising a 4-row truth table for each of the 6 gates, you only need one short sentence describing when each gate outputs 1.</p><p>A quick way to classify them: AND and NAND are about \"all\" inputs, OR and NOR are about \"at least one\" input, and XOR and XNOR are about whether the COUNT of 1-inputs is odd or even. These form three pairs, each pair being one original gate and its inverse (NAND is AND inverted, NOR is OR inverted, XNOR is XOR inverted).</p>",
    "img": "logic_apps_p04.jpg"
   },
   {
    "title": "⚠️ Trap: confusing AND with OR when reading word problems",
    "body": "<div class='callout warn'><p>Everyday English can be loose about 'and'/'or'. E.g. 'the lamp lights when switch A AND switch B are both closed' is an AND (needs BOTH). But 'the lamp lights when switch A OR switch B is closed' is an OR. Always check for 'both/all' (AND) versus 'either/at least one' (OR) before drawing the circuit.</p></div>",
    "explain": "<p>Natural language (in both Vietnamese and English) often uses \"and\"/\"or\" loosely, not as strictly as Boolean logic does, which makes this a very common source of error when turning a real-world problem into a logic expression.</p><p>The most reliable keywords to look for: if the problem says \"both\", \"all\", \"every\", that signals AND; if it says \"either\", \"at least one\", \"any\", that signals OR. Always underline these exact keywords in the problem statement before drawing a circuit, rather than relying on a quick skim.</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>Not graded: answer before moving on:</p><ul><li>Which gate outputs 1 only when BOTH inputs are 0?</li><li>If A=1, B=1, C=0, what is A·B + C·A?</li></ul><p>Hint: NOR; A·B+C·A = 1·1+0·1 = 1+0 = 1.</p>",
    "explain": "<p>This practice exercise applies both skills just learned: recognising a gate from its truth-table description (question 1) and evaluating a multi-operator expression in the correct order (question 2).</p><p>For question 2: A·B+C·A with A=1, B=1, C=0 requires computing each AND first: A·B=1·1=1, C·A=0·1=0, then adding the two results: 1+0=1. If you got anything other than 1, you likely added before multiplying; review the operator-priority slide above.</p>"
   }
  ],
  [
   {
    "title": "The 12 basic laws of Boolean algebra",
    "body": "<table class='tt'><thead><tr><th>#</th><th>Law</th></tr></thead><tbody><tr><td>1</td><td>A + 0 = A</td></tr><tr><td>2</td><td>A + 1 = 1</td></tr><tr><td>3</td><td>A · 0 = 0</td></tr><tr><td>4</td><td>A · 1 = A</td></tr><tr><td>5</td><td>A + A = A</td></tr><tr><td>6</td><td>A + A′ = 1</td></tr><tr><td>7</td><td>A · A = A</td></tr><tr><td>8</td><td>A · A′ = 0</td></tr><tr><td>9</td><td>A″ = A</td></tr><tr><td>10</td><td>A + AB = A</td></tr><tr><td>11</td><td>A + A′B = A + B</td></tr><tr><td>12</td><td>(A+B)(A+C) = A+BC</td></tr></tbody></table>",
    "explain": "<p>These 12 laws are not 12 disconnected formulas to memorise by rote: each one is simply an obvious fact once you substitute 0 or 1 for A and work it out by hand. Take A+1=1: an OR gate with one input permanently tied to 1 will ALWAYS output 1 no matter what the other input is, exactly like \"a room with one door that's always open always has an exit\".</p><p>Use the following slides to understand the MEANING behind each group of laws (commutative, associative, distributive, De Morgan) rather than trying to cram the whole table from this slide alone.</p>",
    "img": "logic_apps_p43.jpg"
   },
   {
    "title": "Commutative and associative laws",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Commutative & associative</div><div class='pd-formula-math'>A+B = B+A &nbsp;·&nbsp; (A+B)+C = A+(B+C)</div></div><p>Exactly like ordinary arithmetic: the order of addition/multiplication doesn't matter, and grouping within a chain of all-AND (or all-OR) terms doesn't matter either.</p>",
    "explain": "<p>These two laws simply state that for a pure AND or pure OR gate (not mixing AND and OR), the order the variables are written in, or how parentheses are grouped, does not change the result, exactly as in arithmetic (2+3=3+2, and (2+3)+4=2+(3+4)).</p><p>One caveat: these two laws ONLY apply when every term uses the SAME operation (all AND, or all OR). Once AND and OR are mixed in one expression, the distributive law on the next slide is needed; commutative/associative cannot be applied naively there.</p>"
   },
   {
    "title": "The distributive law",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Distributive</div><div class='pd-formula-math'>A·(B+C) = A·B + A·C</div></div><p>This is the key step for converting an expression from product-of-sums (POS) to sum-of-products (SOP) form: the standard form used when designing AND-OR circuits.</p>",
    "explain": "<p>The distributive law is the most important bridge connecting mixed AND/OR expressions, playing exactly the role multiplication plays over addition in arithmetic (2×(3+4)=2×3+2×4).</p><p>Its practical meaning: this law lets you \"expand\" a product-of-sums expression (POS, e.g. A·(B+C)) into a sum-of-products form (SOP, e.g. A·B+A·C). SOP is the standard form most commonly used when designing a two-level AND-OR circuit, covered in detail in Part 3.</p>"
   },
   {
    "title": "Worked simplification: A + AB",
    "body": "<p>Simplify Y = A + AB using rule 10 (A + AB = A):</p><ul><li>Apply rule 10 directly → Y = A</li></ul><p>Check with a truth table: when A=0, AB=0 so Y=0=A; when A=1, Y=1+B=1=A. Matches in every case: confirms rule 10 is correct.</p>",
    "explain": "<p>Rule 10 (A+AB=A) can seem hard to believe at first: why does adding an entire extra term AB leave the final result unchanged? The answer comes from checking each case: when A=0, the term AB is always 0 (anything times 0 is 0), so Y=0+0=0=A; when A=1, the second term no longer matters because Y=1+B is always 1 (OR with 1 always gives 1), and A also equals 1, so Y=1=A.</p><p>The bigger lesson here matters more than the result itself: always verify a simplification rule by testing EACH value of the variable, rather than just trusting the formula blindly.</p>"
   },
   {
    "title": "Worked simplification: AB + AB′",
    "body": "<p>Simplify Y = AB + AB′:</p><ul><li>Step 1: factor out A → Y = A(B + B′)</li><li>Step 2: apply rule 6 (B+B′=1) → Y = A·1</li><li>Step 3: apply rule 4 (A·1=A) → Y = A</li></ul>",
    "explain": "<p>This is a complete 3-step simplification, each step applying exactly ONE law already learned, with no shortcuts skipped. Step 1 factors out the common term (exactly like factoring in ordinary algebra: AB+AB′=A(B+B′)). Step 2 applies law 6 (B+B′=1: a variable ORed with its own inverse ALWAYS gives 1, since either B=1 or B′=1, never both 0 at once). Step 3 applies law 4 (A·1=A, multiplying by 1 leaves the value unchanged).</p><p>Laying out each step this clearly is exactly the skill to practise: for longer simplifications, always note WHICH numbered law is used at each step, so mistakes are easy to trace back.</p>"
   },
   {
    "title": "Multi-step simplification: AB + A′C + BC",
    "body": "<p>Simplify Y = AB + A′C + BC (the consensus theorem):</p><ul><li>The term BC is redundant once AB and A′C are present</li><li>Simplified result: Y = AB + A′C</li></ul><p>A classic example showing simplification sometimes requires spotting one entirely redundant term (the 'consensus' term), not just applying basic laws step by step.</p>",
    "explain": "<p>This is the hardest example in Part 2, because simplifying away the BC term does not come from mechanically applying any single one of the 12 basic laws, it requires RECOGNISING that BC is a \"redundant term\" once AB and A′C are already present.</p><p>The intuition: if AB=1 then B must be 1; if A′C=1 then A′ must be 1 (meaning A=0). Consider every case where B and C are both 1: either A=1 (in which case AB=1, so BC being present or not makes no difference since Y is already 1), or A=0 (in which case A′C=1, which alone already makes Y=1). So BC can never be the term that \"saves\" a case that AB and A′C haven't already saved, so dropping it changes nothing.</p>"
   },
   {
    "title": "De Morgan's theorem",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>De Morgan</div><div class='pd-formula-math'>(A·B)′ = A′ + B′ &nbsp;&nbsp; (A+B)′ = A′·B′</div></div><ul class='pd-legend'><li><b>Meaning</b><span>the complement of a product equals the sum of complements; the complement of a sum equals the product of complements</span></li></ul>",
    "explain": "<p>De Morgan's theorem is arguably the single most important theorem in all of Boolean algebra, because it shows how to \"break open\" a NOT that spans an entire AND or OR cluster, an operation that comes up constantly when simplifying circuits.</p><p>A visual way to remember it without memorising the formula: when inverting an expression inside parentheses, do two things AT ONCE: swap the operation inside (AND becomes OR, or OR becomes AND), and invert EACH variable individually inside the parentheses. Remembering \"swap the operation + invert each variable\" is enough to apply De Morgan correctly without needing the symbolic formula.</p>",
    "img": "logic_demorgan_nand.png"
   },
   {
    "title": "Applying De Morgan: simplifying (A′B′)′",
    "body": "<p>Simplify Y = (A′B′)′:</p><ul><li>Apply De Morgan: (A′B′)′ = (A′)′ + (B′)′ = A + B</li></ul><p>Result: Y = A + B: a NAND gate with both inputs inverted is equivalent to a plain OR gate, illustrating why NAND is called a universal gate.</p>",
    "explain": "<p>This is one of the most surprising results De Morgan's theorem produces: a NAND gate (two inputs already inverted before being combined) turns out to be EXACTLY equivalent to an ordinary OR gate. This is exactly why the NAND gate is called a \"universal gate\": using only NAND gates, one can rebuild AND, OR, and NOT.</p><p>In semiconductor manufacturing this is not just a formula trick: a chip maker can mass-produce JUST one type of NAND gate, then wire them together in different combinations to create every other type of gate, greatly simplifying and cutting the cost of production.</p>"
   },
   {
    "title": "Truth table and 2-variable Karnaugh map",
    "body": "<p>For Y = A′B + AB′ + AB (1 in three of the four possible combinations):</p><table class='tt'><thead><tr><th>A\\B</th><th>0</th><th>1</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></tbody></table><p>Grouping the two adjacent cells in the bottom row gives A, and the right column gives B → simplifies to Y = A + B.</p>",
    "explain": "<p>The 2-variable Karnaugh map (K-map) is a tool that turns a truth table into a visual grid, letting the eye SEE adjacent groups of 1s directly instead of working through algebra step by step.</p><p>In the given table, the bottom row (A=1) is all 1s: grouping these two cells gives exactly the variable A (independent of B). The right column (B=1) is also all 1s: grouping this gives exactly the variable B. Seeing these two overlapping groups directly on the grid is much faster than working through Boolean algebra step by step, especially once the number of variables grows to 3 or 4.</p>"
   },
   {
    "title": "⚠️ Trap: misapplying De Morgan with 3+ variables",
    "body": "<div class='callout warn'><p>A common mistake is inverting only the outermost operator while forgetting to invert EACH inner variable. (ABC)′ is NOT A′B′C: the correct answer is (ABC)′ = A′+B′+C′ (apply De Morgan repeatedly, pair by pair).</p></div>",
    "explain": "<p>This is an extremely common mistake when applying De Morgan to 3 or more variables: many people only flip the outermost operation and forget to invert EACH variable inside. (ABC)′ is absolutely NOT equal to A′B′C (only inverting the first variable); all three variables must be inverted AND the operation changed: (ABC)′=A′+B′+C′.</p><p>A way to check without memorising the formula: apply De Morgan repeatedly, one pair at a time, like peeling layers off an onion. (ABC)′=((AB)C)′, apply De Morgan to the outer parentheses first: =(AB)′+C′, then apply it again to (AB)′: =(A′+B′)+C′=A′+B′+C′. Working in small steps like this never misses a variable.</p>"
   }
  ],
  [
   {
    "title": "What is combinational logic?",
    "body": "<p>A combinational circuit is one whose output at any instant depends ONLY on the current input values, not on any past history/state: unlike sequential circuits which retain state (covered in the bistable section).</p>",
    "explain": "<p>The definition of \"combinational circuit\" sounds abstract, but there is a very concrete test: if you set the same input values on a combinational circuit, the output will ALWAYS be identical every single time, no matter what the circuit \"went through\" before. A simple AND gate is the clearest example: A=1, B=1 always gives 1, regardless of what the inputs were a second earlier.</p><p>By contrast, sequential circuits (met in Part 4 with flip-flops) have \"memory\": the same input values can produce two different outputs depending on the circuit's previous state. Telling these two apart is the foundation for understanding everything else in this module.</p>"
   },
   {
    "title": "From a real problem to a truth table",
    "body": "<p>Problem: the Landing Gear Door Warning lamp should light when AT LEAST ONE of the two doors (left/right) is unlocked AND the aircraft is in flight (not on the ground).</p><p>Let L = left door unlocked, R = right door unlocked, F = in-flight. We need: Warning = (L+R)·F.</p>",
    "explain": "<p>This is the most important step in the entire digital design process: translating a plain-language description into clearly named logic variables and a precise Boolean expression. This step is often rushed through, yet it is exactly where a problem is most easily misread.</p><p>For the landing gear door problem: the phrase \"at least one door not locked\" translates to an OR (L+R), while \"AND currently flying\" translates to an AND with variable F. Combined in the right order: Warning=(L+R)·F, not L+R·F (missing parentheses would completely change the meaning, since by the usual AND-before-OR priority, R·F would be computed first, breaking the intended logic).</p>"
   },
   {
    "title": "Truth table for the landing gear door warning",
    "body": "<table class='tt'><thead><tr><th>L</th><th>R</th><th>F</th><th>Warning=(L+R)·F</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr></tbody></table><p>The last row shows: even with both doors unlocked (L=R=1), if the aircraft is on the ground (F=0) there is NO warning: correctly ANDed with F.</p>",
    "explain": "<p>This truth table only lists the combinations with real practical significance (here F is treated as the decisive variable, so both its values are shown, though a full 3-variable table would have 8 rows; this shortened table picks 4 key illustrative rows).</p><p>The most notable row is the last one: L=1, R=1 (both doors unlocked, the most dangerous case looking only at the doors), yet F=0 (aircraft on the ground) still gives Warning=0, NO warning. This is exactly the point of ANDing with F: no matter how bad the door condition, an aircraft on the ground does not need to alert the pilot mid takeoff or landing.</p>"
   },
   {
    "title": "From truth table to gate diagram",
    "body": "<p>The circuit for Warning = (L+R)·F needs:</p><ul><li>One 2-input OR gate (L, R) → produces 'at least one door open'</li><li>One 2-input AND gate (the OR's output, and F) → produces the final warning signal</li></ul>",
    "explain": "<p>Drawing a gate diagram from a Boolean expression is almost a direct \"reverse translation\": each operation in the expression corresponds to exactly one physical gate. Warning=(L+R)·F has two operations (one OR, one AND), so the diagram needs exactly two gates.</p><p>The drawing order always goes from the INSIDE of the parentheses outward: the OR gate (taking L, R) must be drawn and evaluated first, its output then feeding into one of the two inputs of the AND gate (the other input being F). Drawing it in the wrong order (feeding L, R, F all into a single 3-input AND gate) would compute an entirely wrong meaning for the OR.</p>",
    "img": "logic_apps_p25.jpg"
   },
   {
    "title": "Example 2: APU starter control (simplified)",
    "body": "<p>Per Tooley: the APU (auxiliary power unit) starter control circuit ANDs together several safety signals (e.g. no fire warning, engine speed within a safe range) before allowing the start relay to close: a real-world example of an AND with multiple inputs, not just the two-variable case above.</p>",
    "explain": "<p>The APU (Auxiliary Power Unit, an engine that supplies power/air when the main engines are not running) start example shows that multi-input AND is far from rare in practice: aviation safety often requires MANY conditions to be simultaneously true before an important action is permitted.</p><p>The design principle here is \"fail-safe\": if just ONE safety condition is not met (for example a fire warning is present), the whole AND chain immediately outputs 0, blocking the starter relay from closing. This is why multi-input AND (not just 2-variable AND) appears so frequently in an aircraft's safety-protection systems.</p>"
   },
   {
    "title": "Designing a 3-variable circuit from a truth table (SOP)",
    "body": "<p>Given a truth table where Y=1 for (A,B,C) = (0,1,1) or (1,0,1), write the sum-of-products (SOP) form by ORing the minterm for each row where Y=1:</p><div class='pd-formula'><div class='pd-formula-math'>Y = A′BC + AB′C</div></div><p>Simplify further by factoring out C: Y = C(A′B + AB′) = C(A⊕B).</p>",
    "explain": "<p>SOP (Sum of Products) is a MECHANICAL procedure for writing a Boolean expression directly from a truth table, with no guesswork: for every row where Y=1, write exactly one \"minterm\" (an AND cluster of every variable, written plain if it is 1 in that row, inverted if it is 0), then OR all these minterms together.</p><p>For (A,B,C)=(0,1,1) giving Y=1: A=0 so write A′, B=1 so write B, C=1 so write C, ANDed together gives A′BC. Doing the same for row (1,0,1) gives AB′C. ORing the two minterms: Y=A′BC+AB′C. Only afterward is algebraic simplification applied (here factoring out C and recognising A′B+AB′=A⊕B).</p>"
   },
   {
    "title": "The two-level AND-OR circuit",
    "body": "<p>Any general SOP combinational circuit can always be drawn as two levels: LEVEL 1 is a set of AND gates (one per product term), LEVEL 2 is a SINGLE OR gate combining all level-1 outputs: the standard structure used when programming PLDs/PALs.</p>",
    "explain": "<p>The \"two-level AND-OR\" architecture rests on a very powerful mathematical fact: ANY Boolean function, however complex, can always be written in SOP form, and therefore can always be drawn with exactly 2 layers of gates (an AND layer, then an OR layer), with no need for deeper nested layers.</p><p>This is precisely why PLD/PAL chips (Programmable Logic Devices) are built with a fixed \"one AND array feeding one OR array\" structure: the programmer only needs to configure the right connections, without worrying whether \"enough gate layers\" exist for any given logic function.</p>"
   },
   {
    "title": "SOP versus POS",
    "body": "<table class='tt'><thead><tr><th></th><th>SOP (sum-of-products)</th><th>POS (product-of-sums)</th></tr></thead><tbody><tr><td>Form</td><td>Y = AB + A′C</td><td>Y = (A+C)(A′+B)</td></tr><tr><td>Derived from</td><td>rows where Y=1 (minterms)</td><td>rows where Y=0 (maxterms), then inverted</td></tr><tr><td>Circuit structure</td><td>AND then OR</td><td>OR then AND</td></tr></tbody></table>",
    "explain": "<p>SOP and POS are two EQUIVALENT ways of writing the same Boolean function, differing only in their starting point: SOP starts from the rows WHERE Y=1 (minterms), while POS starts from the rows WHERE Y=0 (maxterms), then applies De Morgan to flip it back.</p><p>In practice, choosing SOP or POS usually depends on which form gives a SHORTER expression after simplification: if a truth table has FEWER rows with Y=1 than with Y=0, SOP is usually shorter (fewer minterms to OR together); otherwise POS may be shorter.</p>"
   },
   {
    "title": "⚠️ Trap: forgetting to re-check the full truth table after simplifying",
    "body": "<div class='callout warn'><p>After algebraically simplifying an expression, ALWAYS rebuild the truth table of the simplified expression and compare it against the original for EVERY combination: checking only 1-2 rows can hide an error in a less common branch.</p></div>",
    "explain": "<p>This is an extremely important quality-check habit that is very often skipped when doing exercises: after simplifying an expression through several algebraic steps, it is VERY EASY to slip up at some intermediate step without noticing right away.</p><p>The surest way to check: rebuild the ENTIRE truth table of the simplified expression (every possible variable combination, not just 1 or 2 random rows), and compare it against the ORIGINAL truth table. If they match at EVERY row, the simplification is certainly correct; checking only 1 or 2 rows \"for form's sake\" can easily miss a simplification error hiding in a rarely-hit branch.</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>Not graded: write the SOP expression for a circuit where Y=1 when (A,B)=(0,1) or (1,1). Hint: Y = A′B + AB, which simplifies via the absorption law to Y = B.</p>",
    "explain": "<p>This practice exercise applies the exact SOP procedure just learned: with Y=1 when (A,B)=(0,1) or (1,1), write the two corresponding minterms (A′B for the first row, AB for the second) and OR them: Y=A′B+AB.</p><p>The next simplification step applies rule 11 (A+A′B=A+B, with roles slightly rearranged: here it's B+A′B=B+A written differently, or more directly, factor out B: Y=B(A′+A)=B·1=B using laws 6 and 4). The result B is MUCH simpler than the raw SOP expression, showing clearly the value of the algebraic simplification step after writing a raw SOP.</p>"
   }
  ],
  [
   {
    "title": "What is tri-state logic?",
    "body": "<p>Tri-state logic adds a third state beyond 0 and 1: high impedance (High-Z), where the output 'disconnects' from the circuit as if not connected at all. This lets MULTIPLE devices share a SINGLE bus line without signal conflicts.</p>",
    "explain": "<p>Tri-state logic sounds like it contradicts the \"only 2 voltage levels\" principle learned in Module 01, but it does not: High-Z is not a third VOLTAGE LEVEL, it is a state where the output completely \"lets go\", neither pushing current out nor pulling current in, exactly like a light switch left halfway, connected to nothing.</p><p>The core benefit: without High-Z, every device wired onto a shared bus would always \"try\" to force its own voltage onto the line, causing conflicts when multiple devices share it. High-Z lets a device go completely \"silent\", yielding the bus to another device.</p>"
   },
   {
    "title": "The Enable pin on a tri-state buffer",
    "body": "<table class='tt'><thead><tr><th>Enable</th><th>Input</th><th>Output</th></tr></thead><tbody><tr><td>0</td><td>X (any)</td><td>High-Z (disconnected)</td></tr><tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></tbody></table><p>Only when Enable=1 does the buffer pass the input through; Enable=0 always gives High-Z regardless of the input.</p>",
    "explain": "<p>The Enable pin acts like a \"master switch\" deciding whether the buffer is allowed to speak at all, entirely separate from whatever the Input value happens to be. The truth table shows this clearly: whether Input is 0 or 1, as long as Enable=0, the Output is ALWAYS High-Z, the Input is \"locked out\" and never passed through.</p><p>Only when Enable=1 does the buffer \"open the gate\" and let Input pass straight through to Output unchanged. This is the mechanism that lets multiple devices share one bus: at any moment exactly one device has Enable=1, while every other device keeps Enable=0 to stay silent at High-Z.</p>"
   },
   {
    "title": "Why buses need tri-state",
    "body": "<p>If two devices are wired directly (without tri-state) to one line and one drives logic 1 while the other drives logic 0 at the same time, an electrical conflict (bus contention) results: potentially damaging components. Tri-state solves this by allowing only ONE device to 'talk' on the bus at a time, with all others in High-Z.</p>",
    "explain": "<p>Imagine two people shouting two different words into the same microphone at the exact same time: the recorded sound turns into an unintelligible mess. On an electrical bus, if two devices simultaneously try to force logic 1 and logic 0 onto the same wire, an abnormally large current can flow (bus contention), generating heat and risking permanent damage to components.</p><p>The tri-state solution works like a \"politeness rule\": at any given moment, ONLY one device is allowed to \"speak\" (Enable=1, driving a clear 0 or 1), and every other device must stay completely \"silent\" (High-Z), never simultaneously forcing its own signal onto the bus.</p>"
   },
   {
    "title": "What is a monostable (one-shot)?",
    "body": "<p>A monostable circuit has only ONE stable state. On receiving a trigger pulse, it switches to a second state for a fixed duration (set by an RC time constant), then AUTOMATICALLY returns to its original stable state.</p>",
    "explain": "<p>The term \"one-shot\" describes a monostable circuit's behaviour very precisely: it reacts EXACTLY ONCE per trigger pulse, producing an output pulse of a FIXED width (independent of how long the trigger pulse itself lasted), then automatically returns to its resting state with no outside intervention needed.</p><p>The key point to remember: the width of the output pulse is set by the external R and C components (the RC time constant), NOT by whether the trigger pulse was long or short. This is exactly why monostables are used to \"standardise\" a signal's width.</p>"
   },
   {
    "title": "Applications of monostables",
    "body": "<p>Monostables are commonly used to generate a pulse of FIXED width from a trigger pulse of arbitrary width (e.g. cleaning up/shaping a noisy signal from a mechanical switch: debouncing), or to create a short time delay between two events in a control sequence.</p>",
    "explain": "<p>The \"debounce\" application is the classic textbook use of a monostable: when a mechanical switch is flipped, the metal contacts inside actually bounce back and forth rapidly for a few milliseconds before settling, producing a burst of noisy pulses instead of one clean transition edge.</p><p>A monostable circuit \"filters\" this noise by reacting only to the FIRST trigger pulse, then producing one clean output pulse wide enough to \"cover\" the remaining bounce time, so the digital circuit downstream sees exactly ONE transition event instead of dozens of false pulses.</p>"
   },
   {
    "title": "What is a bistable (flip-flop)?",
    "body": "<p>A bistable circuit has TWO stable states and can hold either one indefinitely until a control signal forces a change: this is the flip-flop, the basic 1-bit memory element underlying every sequential circuit (registers, counters, memory).</p>",
    "explain": "<p>The term \"bistable\" tells you exactly what it is: a circuit with TWO equally stable states, and once it settles into one of them, it STAYS THERE FOREVER (it does not automatically return anywhere, unlike a monostable) until an external control signal actively tells it to switch to the other state.</p><p>This is the most basic \"memory\" mechanism in digital electronics: one bit of data (0 or 1) is stored by having a bistable circuit hold one of its two stable states, until a new write command overwrites it. Every register, counter, and static RAM (SRAM) cell is built on this exact principle.</p>"
   },
   {
    "title": "A simple R-S (Reset-Set) flip-flop",
    "body": "<table class='tt'><thead><tr><th>S</th><th>R</th><th>Next Q</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>unchanged</td></tr><tr><td>1</td><td>0</td><td>1 (set)</td></tr><tr><td>0</td><td>1</td><td>0 (reset)</td></tr><tr><td>1</td><td>1</td><td>invalid</td></tr></tbody></table><p>Can be built from two cross-coupled NOR gates or two cross-coupled NAND gates: exactly the dual R-S bistable example built with a 4001 (CMOS NOR) IC mentioned in Tooley's textbook.</p>",
    "explain": "<p>The R-S flip-flop truth table reads exactly as its name suggests: S (Set) forces the output Q to 1, R (Reset) forces Q to 0. The most interesting row is the first one (S=0, R=0): the output Q \"holds\" its previous value, which is exactly what \"memory\" looks like, the output is not fully determined by the CURRENT inputs alone, but also by history.</p><p>The last row (S=1, R=1) is marked \"invalid\" because this asks the circuit to set and reset AT THE SAME TIME, a contradictory command that a cross-coupled NOR/NAND circuit cannot resolve consistently: the actual result depends on the fine timing details of each gate and cannot be reliably predicted, so this input combination must always be AVOIDED in a design.</p>"
   },
   {
    "title": "Monostable vs bistable comparison",
    "body": "<table class='tt'><thead><tr><th></th><th>Monostable</th><th>Bistable</th></tr></thead><tbody><tr><td>Stable states</td><td>1</td><td>2</td></tr><tr><td>After triggering</td><td>returns automatically</td><td>holds until forced to change</td></tr><tr><td>Main function</td><td>pulse/time-delay generation</td><td>storing 1 bit of data</td></tr></tbody></table>",
    "explain": "<p>This comparison table condenses the core difference between the two bistable and monostable circuit types into one single sentence: a monostable AUTOMATICALLY returns after a fixed time (used to CREATE a pulse or a delay), while a bistable STAYS PUT forever until actively changed (used to STORE data).</p><p>Remembering this one distinguishing sentence will keep you from ever confusing the two in a real problem: if a problem asks to \"create a pulse of fixed length\" or \"delay a signal by some time\", that is a monostable problem; if it asks to \"remember a state\" or \"remember whether a button was pressed\", that is a bistable problem.</p>"
   },
   {
    "title": "⚠️ Trap: confusing High-Z with logic 0",
    "body": "<div class='callout warn'><p>High-Z is NOT a low voltage level (logic 0): it is a fully 'floating' output state with no current being driven. Measuring it with a voltmeter can give unstable/noisy readings because the output isn't being driven by any source.</p></div>",
    "explain": "<p>This is one of the most common real-world measurement traps when working with tri-state circuits: beginners often assume High-Z simply means \"logic 0\" or \"low voltage\", but High-Z is actually a state where the output is NOT DRIVEN by any source at all, with no current flowing out of that output.</p><p>The practical consequence: measuring the voltage at a pin currently in High-Z with a multimeter can give erratic, wildly fluctuating readings, picked up from nearby signals (since the meter's own input has finite impedance), quite unlike measuring a pin genuinely at logic 0 (which stays stable near 0V). Do not rush to conclude \"the circuit is broken\" just because a High-Z pin reads unstable.</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>Not graded: on a bus shared by 4 devices, how many devices should be in a state OTHER than High-Z at any one time? Hint: exactly 1 (the bus-sharing principle).</p>",
    "explain": "<p>The core principle of sharing a bus with tri-state fits in one sentence: at any given moment, no matter how many devices are wired onto the bus, ONLY ONE device is ever permitted to have Enable=1 (actually driving a 0 or 1 onto the bus), and every other device must sit at High-Z.</p><p>With 4 devices sharing one bus, the answer is always 1, regardless of how many devices are on the bus: this is exactly the bus-contention protection principle learned at the start of this part, applying to ANY number of devices sharing a bus, not just the case of 4.</p>"
   }
  ],
  [
   {
    "title": "Why are there several different logic families?",
    "body": "<p>Each logic family has different electrical characteristics: supply voltage, switching speed, power consumption, noise immunity: so choosing the right family for the right application (high speed, low power, high-noise environment...) is an important design decision.</p>",
    "explain": "<p>A \"logic family\" is a group of chips built using the same underlying semiconductor technology (for example, all built from bipolar transistors, or all from MOSFETs), which makes them share the same electrical characteristics: the supply voltage they need, how fast they switch between 0 and 1, how much power they consume, and how well they resist noise.</p><p>No single logic family is \"best\" in every situation: a fast family usually consumes more power, and a power-saving family usually runs slower. Choosing the right family for the right application (say, a battery-powered circuit versus one that must process signals extremely fast) is a genuine engineering decision, not a minor footnote.</p>"
   },
   {
    "title": "The TTL family (Transistor-Transistor Logic)",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Standard TTL supply</div><div class='pd-formula-math'>V_CC = 5V ± 5%</div></div><p>TTL uses bipolar (BJT) transistors, offering fast switching but higher static current draw than CMOS: suitable for high-speed applications where power is less of a concern.</p>",
    "explain": "<p>TTL (Transistor-Transistor Logic) is an early logic technology built from bipolar transistors (BJTs, the classic transistor type controlled by current, unlike the voltage-controlled MOSFETs found in CMOS).</p><p>The key fact to remember: TTL needs a fairly precise supply voltage, only 5V, allowed to vary very little (±5%, i.e. between 4.75V and 5.25V), far less flexible than CMOS. In exchange, bipolar transistors switch quickly, which is why TTL was once a popular choice for high-speed applications during its heyday.</p>"
   },
   {
    "title": "TTL variants",
    "body": "<table class='tt'><thead><tr><th>Variant</th><th>Characteristic</th></tr></thead><tbody><tr><td>Standard TTL</td><td>baseline, fan-out 10, noise margin ~400mV</td></tr><tr><td>LS-TTL (Low-power Schottky)</td><td>lower power, still fairly fast</td></tr><tr><td>S-TTL (Schottky)</td><td>faster than standard, higher power</td></tr></tbody></table>",
    "explain": "<p>The three TTL variants in the table illustrate a very typical engineering trade-off: speed and power consumption usually move TOGETHER, wanting more speed usually costs more power.</p><p>LS-TTL (Low-power Schottky) is an improved version using Schottky diodes to significantly cut power consumption compared with standard TTL, while still keeping reasonably good speed: this is why LS-TTL became the most widely used TTL variant in practice, striking a good balance between speed and power compared with the other two options.</p>"
   },
   {
    "title": "The CMOS family (Complementary MOS)",
    "body": "<p>CMOS uses complementary MOSFET pairs (one N-channel + one P-channel), drawing virtually NO static current in a steady state (power is drawn mainly while switching) : the reason CMOS dominates modern battery-powered/portable devices.</p>",
    "explain": "<p>CMOS (Complementary MOS) is arguably the single most important technological leap in the history of digital chips, using a COMPLEMENTARY PAIR of MOSFETs (one N-channel, one P-channel) inside every gate.</p><p>The key fact that gives CMOS its edge: at any stable moment (not actively switching), exactly one of these two transistors is ALWAYS fully OFF, meaning almost no current flows continuously. CMOS only draws meaningful power during the brief moment of SWITCHING from 0 to 1 or back: this is exactly why CMOS completely dominates modern battery-powered devices, from phones to smartwatches.</p>"
   },
   {
    "title": "CMOS advantage: high noise margin",
    "body": "<p>Because CMOS outputs swing almost the entire supply range for its two logic levels (rail-to-rail), its noise margin is typically MUCH LARGER than TTL's: better immunity in harsh electromagnetic environments such as an engine bay/avionics compartment.</p>",
    "explain": "<p>\"Noise margin\" is the safety gap between a signal's actual voltage and the threshold at which the circuit would misread the logic level: the larger the margin, the more electrical noise a signal can tolerate without being misread.</p><p>CMOS typically uses almost the entire supply voltage range for its two logic levels (called \"rail-to-rail\": the low level sits near 0V and the high level sits near the supply voltage), while TTL uses a narrower slice of that range. As a result, CMOS usually has a significantly larger noise margin than TTL, explaining why CMOS is preferred in harsh electromagnetic environments such as an engine bay or an avionics bay, where interference from other systems is always present.</p>"
   },
   {
    "title": "TTL vs CMOS comparison table",
    "body": "<table class='tt'><thead><tr><th></th><th>TTL</th><th>CMOS</th></tr></thead><tbody><tr><td>Transistor technology</td><td>bipolar (BJT)</td><td>complementary MOSFET</td></tr><tr><td>Supply</td><td>5V ±5%</td><td>3V-15V (depending on series)</td></tr><tr><td>Static power</td><td>higher</td><td>very low</td></tr><tr><td>Noise margin</td><td>~400mV</td><td>larger (rail-to-rail)</td></tr><tr><td>Best suited for</td><td>high speed, power less critical</td><td>portable/battery-powered devices</td></tr></tbody></table>",
    "explain": "<p>This comparison table gathers everything learned separately across the previous 4 slides into a single overview, useful for a quick lookup when deciding which logic family suits a given application.</p><p>Remember two \"decision keywords\" when reading this table: if SPEED is the top priority and power consumption matters less, lean toward TTL; if the top priority is SAVING POWER (battery operation) or good NOISE IMMUNITY, lean firmly toward CMOS.</p>"
   },
   {
    "title": "Example: choosing a logic family for portable test equipment",
    "body": "<p>Problem (Tooley Ch.5 Q6): which logic family suits a battery-powered, portable piece of test equipment? Since the key requirement is low power consumption to extend battery life, CMOS is the most appropriate choice among CMOS/TTL/LS-TTL.</p>",
    "explain": "<p>Choosing a logic family for portable test equipment is a direct application of the comparison table just learned to a real situation: the key word in the problem is \"battery-powered\", which immediately signals that the top priority must be SAVING POWER to extend time between charges.</p><p>Among the three choices CMOS/TTL/LS-TTL, CMOS has the lowest static power consumption (drawing almost nothing when not switching), making it the most sensible choice. This is exactly the reasoning skill to practise: read the problem, identify the SINGLE MOST IMPORTANT criterion being emphasised, then look up the matching row in the comparison table rather than trying to recall every technical detail.</p>"
   },
   {
    "title": "Fan-out and fan-in revisited by family",
    "body": "<p>Standard TTL fan-out is 10 (drives up to 10 same-family TTL inputs). CMOS typically has a much higher DC fan-out (due to its extremely high input impedance), but is limited in practice by speed (each added load slows switching time due to parasitic capacitance).</p>",
    "explain": "<p>Fan-out (the maximum number of loads a gate can drive) and fan-in (the number of inputs a gate can accept) were introduced back in basic logic gate theory, and are now revisited from the angle of differences between logic families.</p><p>An interesting point: TTL has a fairly low fixed fan-out (10) because it is limited by the CURRENT each load requires. CMOS in theory has a much larger DC fan-out (since CMOS inputs have extremely high impedance and draw almost no current), but in practice is still limited by SPEED: each added load contributes a little parasitic capacitance, gradually slowing switching time, so the practical load limit still exists even though it is not caused by current.</p>"
   },
   {
    "title": "⚠️ Trap: mixing TTL and CMOS incorrectly",
    "body": "<div class='callout warn'><p>TTL's 'logic 1' voltage level (~2.4V or above) may NOT be high enough for standard-power CMOS (threshold ~70% of Vdd, e.g. 3.5V at Vdd=5V) to reliably recognise as high: use a TTL-compatible CMOS variant (74HCT instead of 74HC) when interfacing the two families.</p></div>",
    "explain": "<p>This is a very real trap when two systems using different logic families need to \"talk\" to each other: the voltage TTL considers \"logic 1\" (often as low as about 2.4V) might NOT be HIGH ENOUGH for a standard-power CMOS chip (which uses a higher logic-1 threshold, around 70% of supply voltage, e.g. 3.5V on a 5V supply) to correctly recognise it as high.</p><p>The consequence of getting this wrong: a CMOS chip might misread a TTL \"1\" as a \"0\", causing a hard-to-find logic error. The standard industry fix: use a CMOS variant marked with a \"T\" (for example 74HCT instead of 74HC), specifically designed with a threshold backward-compatible with TTL voltage levels.</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>Not graded: a cockpit system needs logic circuits that resist strong electromagnetic interference and draw low power: which family should be preferred? Hint: CMOS (high noise margin plus low static power).</p>",
    "explain": "<p>This practice exercise ties together the two most important criteria learned across all of Part 5: NOISE IMMUNITY (noise margin) and POWER CONSUMPTION (static power), both of which are CMOS's standout strengths over TTL.</p><p>A cockpit system needing both properties at once (withstanding strong electromagnetic interference from nearby equipment, AND consuming little power to reduce the load on the aircraft's electrical system): CMOS is the right choice on both criteria, with no trade-off needed as there would be against TTL.</p>"
   }
  ]
 ]
}
