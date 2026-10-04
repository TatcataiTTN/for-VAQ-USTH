# -*- coding: utf-8 -*-
"""Slide Module 05 (VI + EN): body + explain (giai thich cho nguoi moi) + img (anh goc tu bai giang)."""

SLIDES = {
 "vi": [
  [
   {
    "title": "Kết nối điểm-điểm: cách làm cũ và vấn đề của nó",
    "body": "<p>Trước khi có bus dữ liệu, mỗi cảm biến/máy tính (ADC, FADEC, cảm biến càng đáp...) phải nối dây RIÊNG tới MỌI thiết bị cần dùng dữ liệu đó (EFIS, FMS, ECAM...). Với hàng chục cảm biến và hàng chục màn hình/máy tính, số dây tăng theo kiểu tổ hợp, không tuyến tính.</p>",
    "explain": "<p>Hãy tưởng tượng 5 cảm biến, mỗi cảm biến cần gửi dữ liệu tới 5 màn hình khác nhau: nối điểm-điểm cần tới 5×5=25 đường dây riêng biệt. Nếu thêm 1 cảm biến mới, phải kéo thêm 5 dây mới (một dây tới mỗi màn hình). Đây chính xác là sơ đồ bên trái trong slide bài giảng: ADC, FADEC, cảm biến càng đáp, cảm biến nhiên liệu... mỗi thiết bị có một bó dây màu riêng chạy chằng chịt tới EFIS, Flight Control Computer, ECAM, FMS.</p><p>4 nhược điểm chính được liệt kê ngay trong bài giảng: cần rất nhiều dây (nặng, tốn chỗ), khó lắp đặt/bảo trì/dò lỗi, khó mở rộng khi thêm thiết bị mới, và dễ đấu nhầm dây do số lượng quá lớn.</p>",
    "img": "databus_p02.jpg"
   },
   {
    "title": "Giải pháp: mạng bus dữ liệu dùng chung",
    "body": "<p>Thay vì dây riêng cho từng cặp thiết bị, TẤT CẢ thiết bị cùng nối vào 1 (hoặc vài) đường bus chung, gửi/nhận dữ liệu theo đúng 1 chuẩn giao tiếp (protocol). Ví dụ trong bài giảng: ARINC 429, ARINC 629, AFDX/664, MIL-STD-1553 là 4 “làn” bus khác nhau, mỗi làn phục vụ một nhóm nhu cầu riêng.</p>",
    "explain": "<p>Quay lại ví dụ 5 cảm biến × 5 màn hình: nếu dùng 1 đường bus chung, mỗi cảm biến chỉ cần ĐÚNG 1 dây nối vào bus, và mỗi màn hình cũng chỉ cần ĐÚNG 1 dây đọc từ bus: tổng cộng chỉ 10 dây thay vì 25, và con số này CHỈ TĂNG TUYẾN TÍNH khi thêm thiết bị (thêm 1 cảm biến = thêm đúng 1 dây), không tăng theo tổ hợp như kiểu điểm-điểm.</p><p>Bài giảng liệt kê rõ 5 lợi ích tương ứng với 5 nhược điểm ở slide trước: giảm hẳn số dây/khối lượng, nhiều thiết bị chia sẻ được cùng dữ liệu, dễ lắp đặt/bảo trì/cô lập lỗi hơn, dễ tích hợp thiết bị mới, và hỗ trợ kiểm tra lỗi/giám sát bus theo chuẩn.</p>"
   },
   {
    "title": "6 lý do kỹ thuật để dùng bus dữ liệu trên máy bay",
    "body": "<table class='tt'><thead><tr><th>#</th><th>Lý do</th><th>Giải thích ngắn</th></tr></thead><tbody><tr><td>1</td><td>Giảm dây, khối lượng, không gian</td><td>Thay hàng nghìn dây điểm-điểm bằng vài cáp bus</td></tr><tr><td>2</td><td>Chia sẻ dữ liệu</td><td>1 cảm biến phát, nhiều thiết bị cùng nhận</td></tr><tr><td>3</td><td>Tăng độ tin cậy/an toàn</td><td>Nhiều bus độc lập (vd Bus A/B) hoạt động song song</td></tr><tr><td>4</td><td>Dễ bảo trì, cô lập lỗi</td><td>Cơ chế giám sát/báo lỗi tích hợp sẵn theo chuẩn</td></tr><tr><td>5</td><td>Dễ mở rộng, nâng cấp</td><td>Thiết bị mới chỉ cần nối vào bus, không kéo dây mới</td></tr><tr><td>6</td><td>Hỗ trợ nhiều loại dữ liệu, tốc độ phù hợp</td><td>Mỗi loại bus có tốc độ/đặc tính riêng cho đúng nhu cầu</td></tr></tbody></table>",
    "explain": "<p>Bảng này gộp lại đúng 6 ô vuông ở phần dưới cùng slide 2 của bài giảng. Điểm đáng chú ý: lý do số 3 (tăng độ tin cậy) không chỉ nhờ CÓ bus, mà nhờ THIẾT KẾ DƯ THỪA (redundancy) của bus đó, ví dụ ARINC 629 có Bus A (chính) và Bus B (dự phòng) hoạt động ĐỘC LẬP, nếu Bus A hỏng thì Bus B vẫn tiếp tục hoạt động bình thường.</p><p>Lý do số 6 giải thích vì sao máy bay không dùng DUY NHẤT một loại bus cho mọi thứ: dữ liệu điều khiển bay cần độ tin cậy/thời gian thực cao nhưng khối lượng nhỏ (hợp với ARINC 429/629), còn dữ liệu bảo trì/hình ảnh/video cần băng thông lớn (hợp với AFDX 100 Mbps). Đây chính là lý do một chiếc A320 dùng SONG SONG nhiều loại bus khác nhau, không chỉ 1 loại duy nhất.</p>"
   },
   {
    "title": "Bốn họ bus chính trên avionics hiện đại",
    "body": "<table class='tt'><thead><tr><th>Bus</th><th>Tốc độ</th><th>Kiểu</th><th>Dùng cho</th></tr></thead><tbody><tr><td>ARINC 429</td><td>12,5/100 kbps</td><td>1 chiều, điểm-điểm</td><td>Avionics cơ bản, dữ liệu cảm biến</td></tr><tr><td>ARINC 629</td><td>2 Mbps</td><td>2 chiều, dư thừa kép</td><td>Điều khiển bay thời gian thực</td></tr><tr><td>AFDX/ARINC 664</td><td>100 Mbps</td><td>Ethernet chuyển mạch</td><td>Dữ liệu khối lượng lớn, đa hệ thống</td></tr><tr><td>MIL-STD-1553/ARINC 717</td><td>1 Mbps / 2-8 Mbps</td><td>Chuyên dụng</td><td>Quân sự, FADEC, ghi dữ liệu bay</td></tr></tbody></table>",
    "explain": "<p>Bảng này tóm tắt đúng 4 cột màu trong sơ đồ “Data Buses in an Aircraft (A320)” của bài giảng: xanh lá (ARINC 429), xanh dương (ARINC 629), đỏ (AFDX/664), cam (MIL-STD-1553/ARINC 717). Mỗi màu dây trong sơ đồ gốc nối một nhóm thiết bị khác nhau: ARINC 429 nối cảm biến tới ADIRU/EFIS/FMS, ARINC 629 nối các máy tính điều khiển bay với nhau, AFDX nối hầu hết hệ thống avionics hiện đại, còn MIL-STD-1553/717 dành riêng cho động cơ (FADEC) và thiết bị ghi âm/dữ liệu buồng lái.</p><p>Thứ tự tốc độ (429 &lt; 1553 &lt; 629 &lt; AFDX) không tỉ lệ thuận với “độ quan trọng”: ARINC 429 chậm nhất nhưng vẫn được dùng rộng rãi nhất vì đơn giản, rẻ, cực kỳ tin cậy cho dữ liệu KHÔNG cần băng thông lớn.</p>"
   },
   {
    "title": "⚠️ Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Một máy bay có 8 cảm biến, mỗi cảm biến cần gửi dữ liệu riêng tới 6 màn hình hiển thị khác nhau. Nếu nối điểm-điểm, cần bao nhiêu đường dây? Nếu dùng 1 bus chung, cần bao nhiêu đường dây (giả sử mỗi thiết bị chỉ cần 1 dây nối vào bus)?</p></div>",
    "explain": "<p>Điểm-điểm: 8×6=48 đường dây riêng biệt (mỗi cảm biến nối riêng tới từng màn hình). Dùng bus chung: 8+6=14 dây (mỗi thiết bị, dù là cảm biến hay màn hình, chỉ cần đúng 1 dây nối vào bus).</p><p>Chênh lệch 48 so với 14 (gần gấp 3.5 lần) minh hoạ rõ: cách nối điểm-điểm tăng theo TÍCH số thiết bị (n×m), còn bus chung tăng theo TỔNG số thiết bị (n+m). Khoảng cách này càng lớn khi số thiết bị càng nhiều, đúng như lý do số 1 đã nêu ở slide trước.</p>"
   }
  ],
  [
   {
    "title": "ARINC 429: chuẩn bus avionics phổ biến nhất",
    "body": "<p>ARINC 429 là bus ĐIỂM-ĐIỂM, MỘT CHIỀU: 1 transmitter (LRU phát) có thể nối tới tối đa 20 receiver (LRU nhận), nhưng dữ liệu chỉ chạy một chiều duy nhất. Muốn 2 LRU trao đổi dữ liệu qua lại, cần 2 kênh ARINC 429 riêng biệt, mỗi kênh một chiều.</p>",
    "explain": "<p>Đây là điểm dễ gây nhầm lẫn nhất khi mới học ARINC 429: tại sao một LRU như ADIRU vừa có chân Tx (phát) vừa có chân Rx (nhận)? Câu trả lời nằm ở đúng slide 11 của bài giảng: vì ARINC 429 là bus MỘT CHIỀU, nên 1 kênh vật lý chỉ truyền được 1 hướng. Nếu ADIRU cần GỬI dữ liệu khí động cho FMGC VÀ NHẬN lệnh chọn chế độ từ FMGC, đó là 2 kênh ARINC 429 hoàn toàn riêng biệt chạy song song, không phải 1 kênh “hai chiều”.</p><p>Một LRU phức tạp như ADIRU có thể có hàng chục kênh Tx/Rx khác nhau, mỗi kênh phục vụ đúng 1 luồng dữ liệu 1 chiều tới/từ đúng 1 nhóm thiết bị.</p>"
   },
   {
    "title": "Đặc tính điện của ARINC 429",
    "body": "<p>Cáp xoắn đôi có vỏ bọc (shielded twisted pair). Mỗi dây (A, B) mang điện áp +5V/0V/-5V so với đất. Bộ nhận chỉ quan tâm điện áp VI SAI (A-B): +10V = bit 1, -10V = bit 0, 0V = trạng thái NULL (không truyền).</p>",
    "explain": "<p>Dùng tín hiệu VI SAI (differential signaling) thay vì đo điện áp tuyệt đối trên 1 dây so với đất là một kỹ thuật chống nhiễu kinh điển: nếu có nhiễu điện từ bên ngoài tác động, nó thường ảnh hưởng GẦN NHƯ BẰNG NHAU lên cả 2 dây A và B (vì chúng xoắn sát nhau), nên hiệu số (A-B) hầu như KHÔNG đổi, giữ nguyên được thông tin bit dù môi trường điện từ xung quanh (động cơ, radar) rất nhiễu.</p><p>Bảng điện áp trong bài giảng rất dễ nhớ theo quy tắc đối xứng: bit 1 → A dương/B âm; bit 0 → A âm/B dương (đảo ngược hoàn toàn); NULL → cả 2 dây về 0V (không lệch).</p>"
   },
   {
    "title": "Mã hoá BPRZ: vì sao mỗi bit phải “về lại 0V”?",
    "body": "<p>ARINC 429 dùng mã hoá Bipolar Return to Zero (BPRZ): giữa mỗi bit, tín hiệu luôn trở về mức 0V trước khi sang bit kế tiếp. Nhờ vậy bộ nhận TỰ TÁCH được nhịp (self-clocking) ngay từ tín hiệu dữ liệu, không cần một đường dây clock riêng.</p>",
    "explain": "<p>So sánh trực tiếp ở slide bài giảng: nếu KHÔNG về 0 (như mã NRZ), một chuỗi “1111” liên tiếp sẽ giữ nguyên điện áp +10V suốt 4 bit liền, không có cạnh chuyển mức nào để bên nhận biết chính xác ranh giới giữa các bit: dễ bị “trôi nhịp” (lệch đếm bit) nếu đồng hồ 2 bên không khớp hoàn hảo. Với BPRZ, MỖI bit đều có ít nhất 1 cạnh lên và 1 cạnh xuống (kể cả chuỗi 1111 liên tục), nên bên nhận luôn có mốc để đếm lại nhịp, không bị trôi.</p><p>Cái giá phải trả: BPRZ cần TẦN SỐ CHUYỂN MẠCH cao hơn NRZ ở cùng tốc độ bit (vì có thêm cạnh chuyển về 0 giữa mỗi bit), nhưng đổi lại độ tin cậy đồng bộ cao hơn hẳn, đáng giá cho ứng dụng avionics quan trọng.</p>",
    "img": "databus_p13.jpg"
   },
   {
    "title": "Hai tốc độ của ARINC 429 và thời gian truyền 1 từ",
    "body": "<p>ARINC 429 có 2 tốc độ: low speed 12,5 kbps (phổ biến nhất) và high speed 100 kbps. Với từ dữ liệu luôn dài 32 bit: t_từ = 32/R. Ở 12,5 kbps: t=2,56 ms. Ở 100 kbps: t=0,32 ms (nhanh gấp 8 lần).</p>",
    "explain": "<p>Đây chính là công thức “Công thức” của module này (xem khung công thức bên dưới deck). Thay số trực tiếp: 32 bit / 12.500 bit/s = 0,00256 s = 2,56 ms; và 32 bit / 100.000 bit/s = 0,00032 s = 0,32 ms. Hai con số này khớp CHÍNH XÁC với bảng “Data Rate and Bit Timing” trong bài giảng, đã tự kiểm tra lại bằng notebook đi kèm.</p><p>Vì sao đa số hệ thống A320 vẫn dùng tốc độ THẤP (12,5 kbps) thay vì tốc độ cao? Vì phần lớn dữ liệu avionics cơ bản (tốc độ bay, độ cao, trạng thái cảnh báo...) không thay đổi nhanh tới mức cần cập nhật hơn vài trăm lần/giây, nên tốc độ thấp đã quá đủ và còn tiết kiệm hơn về mạch điện.</p>"
   },
   {
    "title": "Tổng quan các kết nối ARINC 429 trên A320",
    "body": "<p>ARINC 429 nối gần như MỌI nhóm hệ thống trên A320: điều khiển bay (ELAC/SEC/FAC), dẫn đường (FMGC/MCDU/FCU), khí động/quán tính (ADIRU), hiển thị/cảnh báo (DMC/DU/FWC), liên lạc (VHF/HF/AMU/RMP), và cả động cơ, điện, càng đáp, nhiên liệu...</p>",
    "explain": "<p>Sơ đồ trong bài giảng cho thấy ARINC 429 không phải bus “nhỏ lẻ” chỉ dùng cho vài thiết bị, mà là XƯƠNG SỐNG kết nối hầu hết LRU trên A320, với 2 bus song song Bus A và Bus B để dự phòng. Mỗi LRU trong sơ đồ đều có ký hiệu Tx (đỏ, phát) và/hoặc Rx (xanh, nhận) riêng biệt, đúng với nguyên tắc 1-chiều đã học ở slide trước.</p><p>Bảng “Receiver of some LRUs” trong bài giảng là một ví dụ thực hành tốt: ADIRU phát dữ liệu khí động/quán tính, được NHIỀU LRU khác cùng nhận (FMGC, FWC, DMC) nhờ đặc tính multi-drop (1 transmitter → tối đa 20 receiver) của ARINC 429.</p>"
   },
   {
    "title": "⚠️ Bẫy: nhầm điện áp trên dây với điện áp vi sai",
    "body": "<div class='callout warn'><p>Đề thi hay hỏi “điện áp TRÊN CÁP ARINC 429 là bao nhiêu?”: đáp án ĐÚNG là ±5V (điện áp từng dây A hoặc B so với đất), KHÔNG phải ±10V (đó là điện áp VI SAI giữa 2 dây, chỉ xuất hiện khi so sánh A với B).</p></div>",
    "explain": "<p>Đây là đúng câu hỏi số 9 trong bộ 17 câu trắc nghiệm gốc của sách Tooley, và đáp án chính thức của sách là ±5V chứ không phải +5V/+10V hay ±15V. Nhầm lẫn này rất phổ biến vì nhiều tài liệu khác chỉ nhắc tới con số “10V” (điện áp vi sai) mà quên nói rõ đó là hiệu số giữa 2 dây, không phải điện áp đo trực tiếp trên 1 dây.</p><p>Mẹo nhớ: luôn hỏi lại “điện áp NÀY đo so với đất (ground) hay so với dây còn lại?” trước khi chọn đáp án cho bất kỳ câu hỏi điện áp vi sai nào.</p>"
   }
  ],
  [
   {
    "title": "Cấu trúc 1 từ dữ liệu ARINC 429: 5 trường, 32 bit",
    "body": "<p>Mỗi từ ARINC 429 dài CỐ ĐỊNH 32 bit, gồm 5 trường theo đúng thứ tự: <b>Label</b> (8 bit, bit 1-8) → <b>SDI</b> (2 bit) → <b>Data</b> (19 bit) → <b>SSM</b> (2 bit) → <b>Parity</b> (1 bit, bit 32). Bit 1 (Label) truyền ĐI TRƯỚC, bit 32 (Parity) truyền SAU CÙNG.</p>",
    "explain": "<p>Thứ tự truyền “LSB trước, MSB sau” (bit 1 là LSB của toàn từ, truyền đầu tiên) là một chi tiết dễ bị bỏ sót nhưng quan trọng khi tự tay giải mã một từ ARINC 429 từ dạng sóng: nếu đếm bit sai thứ tự, toàn bộ Label/Data sẽ bị đọc sai.</p><p>8+2+19+2+1 = 32, khớp đúng tổng độ dài từ. Đây là lý do CÂU HỎI số 8 và số 15 trong bộ trắc nghiệm gốc (Label=8 bit, độ dài từ=32 bit) có thể tính được trực tiếp từ sơ đồ này mà không cần học thuộc lòng, chỉ cần nhớ đúng công thức cộng 5 trường.</p>"
   },
   {
    "title": "Trường Label: “tên” của dữ liệu đang truyền",
    "body": "<p>Label (8 bit) xác định LOẠI dữ liệu đang được truyền, ví dụ Label 203 = tốc độ bay chỉ thị (Indicated Airspeed), Label 204 = số Mach, Label 205 = độ cao khí áp (Pressure Altitude). Có tối đa 256 giá trị Label khác nhau (0-255).</p>",
    "explain": "<p>Label hoạt động giống như “nhãn dán” trên một gói hàng: bên nhận không cần biết trước nội dung gói hàng là gì, chỉ cần đọc nhãn (Label) để biết CÁCH xử lý 19 bit Data đi kèm (vd đọc theo định dạng BCD hay BNR, đơn vị gì, thang đo nào).</p><p>Vì Label chỉ có 8 bit (256 giá trị) nhưng số loại dữ liệu avionics thực tế nhiều hơn 256, nên trường SDI (Source/Destination Identifier) đi kèm được dùng để PHÂN BIỆT THÊM nguồn/đích trong cùng 1 Label, mở rộng số lượng “kênh” phân biệt được.</p>"
   },
   {
    "title": "Hai định dạng Data: BCD và BNR",
    "body": "<table class='tt'><thead><tr><th>Định dạng</th><th>Cách mã hoá</th><th>Dấu âm/dương</th></tr></thead><tbody><tr><td>BCD</td><td>Mỗi chữ số thập phân = 4 bit riêng</td><td>1 bit dấu (S) + chữ số</td></tr><tr><td>BNR</td><td>Toàn bộ giá trị = 1 số nhị phân</td><td>Bù hai (two's complement)</td></tr></tbody></table>",
    "explain": "<p>BCD (như đã học ở Module 01) tách TỪNG chữ số thập phân thành 4 bit riêng: ví dụ 250 → CHAR1=2(0010), CHAR2=5(0101), CHAR3=0(0000). Ưu điểm: dễ hiển thị trực tiếp ra màn hình 7 đoạn mà không cần đổi cơ số. Nhược điểm: lãng phí bit (4 bit chỉ biểu diễn được 10 trong 16 tổ hợp).</p><p>BNR mã hoá TOÀN BỘ giá trị thành 1 số nhị phân duy nhất (không tách từng chữ số), dùng bù hai để biểu diễn số âm: bit 29 (MSB của trường Data) là bit dấu, 0=dương, 1=âm. BNR hiệu quả hơn BCD về mặt bit, nên được dùng cho dữ liệu cần độ chính xác cao như toạ độ, tốc độ góc.</p>",
    "img": "databus_p16.jpg"
   },
   {
    "title": "Trường SSM: báo trạng thái của chính dữ liệu đang gửi",
    "body": "<p>SSM (Sign/Status Matrix, 2 bit) báo dữ liệu đang ở trạng thái nào. Với BNR: 00=Failure Warning (lỗi), 01=No Computed Data (chưa có dữ liệu), 10=Functional Test (đang tự kiểm tra), 11=Normal Operation (bình thường, hợp lệ).</p>",
    "explain": "<p>Đây là một cơ chế TỰ BÁO LỖI rất thông minh: thay vì chỉ gửi SỐ LIỆU và hy vọng nó đúng, mỗi từ ARINC 429 LUÔN kèm theo “nhãn độ tin cậy” của chính số liệu đó. Nếu ADIRU phát hiện cảm biến tốc độ bay bị lỗi, nó vẫn gửi từ dữ liệu như bình thường nhưng đặt SSM=00 (Failure Warning): bên nhận (PFD) đọc thấy SSM này sẽ hiển thị cảnh báo thay vì tin vào con số (có thể sai) trong trường Data.</p><p>Đây là lý do một kỹ sư avionics khi debug KHÔNG BAO GIỜ chỉ nhìn trường Data để kết luận dữ liệu đúng hay sai: phải luôn kiểm tra SSM trước tiên.</p>"
   },
   {
    "title": "Trường Parity: tự kiểm tra lỗi truyền bằng 1 bit",
    "body": "<p>Bit cuối cùng (bit 32) là bit chẵn lẻ LẺ (odd parity): tổng số bit 1 trong toàn bộ 32 bit LUÔN LÀ SỐ LẺ. Nếu bên nhận đếm được tổng số bit 1 là SỐ CHẴN, từ dữ liệu bị coi là lỗi và bị loại bỏ.</p>",
    "explain": "<p>Cách hoạt động: bên phát đếm số bit 1 trong 31 bit đầu (Label+SDI+Data+SSM); nếu con số đó đã LẺ, đặt Parity=0 (không cần thêm); nếu con số đó CHẴN, đặt Parity=1 (để tổng cộng thành lẻ). Bên nhận chỉ cần đếm lại tổng 32 bit, nếu ra số chẵn thì chắc chắn có ít nhất 1 bit đã bị lật do nhiễu trên đường truyền.</p><p>Giới hạn của parity 1-bit: nó chỉ phát hiện được số LẺ bit lỗi (1, 3, 5...), còn nếu đúng 2 bit bị lật cùng lúc (hiếm nhưng có thể), tổng vẫn đúng tính chẵn/lẻ nên KHÔNG phát hiện được: đây là lý do các hệ thống an toàn cao hơn (như AFDX) dùng CRC nhiều bit thay vì chỉ 1 bit parity.</p>"
   },
   {
    "title": "Ví dụ hoàn chỉnh: mã hoá tốc độ bay 250 kt",
    "body": "<p>ADIRU tính IAS=250kt → mã hoá BCD: 2→0010, 5→0101, 0→0000 → ghép vào 19 bit Data. Gắn thêm Label (nhận diện IAS), SDI, SSM=11 (Normal), tính Parity → đóng gói thành 1 từ 32 bit → gửi lặp lại mỗi ~100ms qua ARINC 429 Bus A tới PFD.</p>",
    "explain": "<p>Đây là ví dụ “đi từ đầu tới cuối” tổng hợp lại TẤT CẢ các trường đã học trong phần này: Label (nhận diện đây là IAS), SDI (xác định nguồn/đích), Data dạng BCD (giá trị 250), SSM (báo dữ liệu hợp lệ), Parity (tự kiểm tra lỗi). Bên nhận (PFD) làm NGƯỢC LẠI đúng các bước đó: kiểm tra parity trước, đọc Label để biết đây là IAS, đọc SSM để chắc chắn dữ liệu hợp lệ, rồi mới đọc Data và hiển thị lên thước tốc độ.</p><p>Việc gửi LẶP LẠI liên tục (không chỉ gửi 1 lần) rất quan trọng: nếu PFD bỏ lỡ 1 từ (nhiễu, lỗi parity), nó chỉ cần đợi khoảng 100ms là có ngay giá trị mới, không bị “đứng hình” vĩnh viễn vì mất đúng 1 gói tin.</p>",
    "img": "databus_p12.jpg"
   }
  ],
  [
   {
    "title": "ARINC 629: khi cần hai chiều và không có bộ điều khiển trung tâm",
    "body": "<p>ARINC 629 (2 Mbps, nhanh gấp 20 lần ARINC 429) là bus HAI CHIỀU: mỗi LRU vừa có thể phát (Tx) vừa có thể nhận (Rx) trên CÙNG một đường bus. Dùng TDMA (Time Division Multiple Access): mỗi LRU được cấp sẵn (các) khe thời gian cố định để phát, tránh xung đột dữ liệu.</p>",
    "explain": "<p>Điểm đặc biệt nhất của ARINC 629, được chính bài giảng nhấn mạnh: đạt được giao tiếp HAI CHIỀU mà KHÔNG CẦN một bộ điều khiển trung tâm (bus controller) riêng, vốn có thể trở thành điểm lỗi đơn (single point of failure) nếu nó hỏng. Thay vào đó, mỗi LRU tự biết “lượt” của mình (slot) trong Major Frame nhờ đồng bộ thời gian chung, không cần ai ra lệnh “tới lượt anh phát”.</p><p>Với 125 khe (slot) mỗi 16 μs trong 1 Major Frame dài 2ms, và tối đa 20-21 LRU trên 1 bus: đây là con số thực tế trong bài giảng, có thể dùng để tính lại thời gian 1 chu kỳ hoàn chỉnh (125×16μs=2000μs=2ms, khớp đúng).</p>",
    "img": "databus_p06.jpg"
   },
   {
    "title": "Cấu trúc khung tin ARINC 629: 52 bit",
    "body": "<p>Mỗi khung tin ARINC 629 gồm: Sync (8 bit) + Data (32 bit, 4 byte) + SDI (2 bit) + Label (8 bit) + SSM (2 bit) = 52 bit. So với ARINC 429 (32 bit/từ, không có Sync riêng), ARINC 629 thêm trường Sync để đồng bộ khung trong hệ thống TDMA nhiều LRU dùng chung 1 bus.</p>",
    "explain": "<p>Nhận xét thú vị: phần Label (8 bit), SDI (2 bit), SSM (2 bit) của ARINC 629 GIỐNG HỆT ARINC 429 về kích thước và ý nghĩa, cho thấy ARINC 629 được thiết kế kế thừa trực tiếp từ ARINC 429, chỉ MỞ RỘNG thêm để hỗ trợ nhiều LRU dùng chung bus (cần Sync để biết khi nào 1 khung bắt đầu) và hai chiều.</p><p>Vì mỗi khung 52 bit truyền trong 1 khe 16μs ở tốc độ 2 Mbps: 16μs × 2.000.000 bit/s = 32.000 bit... thực tế con số này lớn hơn 52 bit rất nhiều vì mỗi khe còn có khoảng nghỉ (gap) giữa các khung để tránh chồng lấn tín hiệu giữa các LRU liền kề.</p>"
   },
   {
    "title": "AFDX/ARINC 664: khi dữ liệu cần băng thông lớn",
    "body": "<p>AFDX (Avionics Full-Duplex Switched Ethernet) là Ethernet chuyển mạch 100 Mbps, dùng trên A380/A350 (và một phần A320 đời mới). Thay vì bus dùng chung như 429/629, AFDX dùng SWITCH trung tâm, mỗi thiết bị nối vào 1 cổng riêng của switch.</p>",
    "explain": "<p>Khác biệt kiến trúc quan trọng nhất: ARINC 429/629 là bus KIỂU “đường dây chung” (mọi thiết bị nghe chung 1 đường truyền vật lý), còn AFDX là mạng KIỂU “hình sao qua switch” (giống mạng Ethernet văn phòng): mỗi LRU có 1 dây RIÊNG nối tới switch, switch chịu trách nhiệm chuyển tiếp đúng gói tin tới đúng đích.</p><p>Vì dùng switch, AFDX đạt băng thông 100 Mbps, đủ cho dữ liệu “nặng” như hình ảnh bảo trì, video camera, dữ liệu đồng thời từ nhiều hệ thống: những loại dữ liệu hoàn toàn KHÔNG khả thi trên ARINC 429 (chỉ 12,5-100 kbps).</p>",
    "img": "databus_p07.jpg"
   },
   {
    "title": "Virtual Link (VL): “làn đường riêng” trong AFDX",
    "body": "<p>Một mạng AFDX vật lý được chia thành nhiều Virtual Link (VL) LOGIC, mỗi VL có băng thông, kích thước khung, và chu kỳ truyền tối thiểu (BAG - Bandwidth Allocation Gap) RIÊNG. Switch đảm bảo các VL CÁCH LY với nhau, không VL nào chiếm hết băng thông của VL khác.</p>",
    "explain": "<p>Hãy hình dung VL như các làn đường riêng trên cùng 1 con đường cao tốc (dây Ethernet vật lý): dù tất cả xe (dữ liệu) cùng chạy trên 1 con đường, mỗi làn (VL) có giới hạn tốc độ và lưu lượng RIÊNG, xe ở làn này không thể tràn sang chiếm làn khác. Đây chính là cách AFDX đạt được tính XÁC ĐỊNH (deterministic): dù mạng Ethernet thông thường có thể bị “tắc nghẽn” khó đoán trước, AFDX đảm bảo mỗi luồng dữ liệu quan trọng (vd lệnh điều khiển bay) LUÔN có đúng phần băng thông đã cam kết, không bị dữ liệu khác (vd video giải trí hành khách) chiếm dụng.</p><p>Đây là lý do AFDX phù hợp cho cả dữ liệu AN TOÀN-QUAN TRỌNG (flight control) LẪN dữ liệu không quan trọng (cabin, giải trí) chạy chung 1 mạng vật lý mà không lo xung đột.</p>"
   },
   {
    "title": "MIL-STD-1553B: bus quân sự có bộ điều khiển trung tâm",
    "body": "<p>MIL-STD-1553B dùng kiến trúc command-response với 1 Bus Controller (BC) điều khiển tối đa 31 Remote Terminal (RT), tốc độ 1 Mbps. MIL-STD-1773B là phiên bản cáp quang, chống nhiễu điện từ cường độ cao (HIRF) tốt hơn hẳn.</p>",
    "explain": "<p>Khác hẳn triết lý “không cần điều khiển trung tâm” của ARINC 629, MIL-STD-1553B CỐ Ý dùng 1 Bus Controller duy nhất ra lệnh cho mọi Remote Terminal: BC hỏi “RT số 5, anh có dữ liệu gì” rồi RT5 trả lời, giống hệt mô hình hỏi-đáp (command-response). Lựa chọn này phù hợp với môi trường quân sự nơi cần kiểm soát chặt chẽ, dự đoán được chính xác thiết bị nào đang nói vào thời điểm nào.</p><p>Trên A320 dân dụng, chuẩn này (cùng ARINC 717) chủ yếu dùng cho FADEC (điều khiển động cơ) và thiết bị ghi âm/dữ liệu buồng lái (CVR/FDR), những nơi cần độ tin cậy cực cao nhưng không cần băng thông lớn.</p>"
   },
   {
    "title": "Các chuẩn bus cũ/đặc thù khác (lược sử)",
    "body": "<table class='tt'><thead><tr><th>Chuẩn</th><th>Đặc điểm chính</th></tr></thead><tbody><tr><td>ARINC 419/561</td><td>Tiền thân của 429, trước 1970, hệ 6 dây hoặc 2 dây</td></tr><tr><td>ARINC 573/717</td><td>Ghi dữ liệu chuyến bay (FDR), mã Harvard Bi-Phase</td></tr><tr><td>ARINC 708</td><td>Radar thời tiết, mã hoá Manchester, 1 Mbps</td></tr><tr><td>CSDB / ASCB</td><td>Chuẩn riêng Collins/Honeywell, máy bay nhỏ</td></tr><tr><td>FDDI</td><td>Mạng vòng đôi 100 Mbps, phát triển cho Boeing 777</td></tr></tbody></table>",
    "explain": "<p>Bảng này không yêu cầu nhớ chi tiết, chỉ cần nắm Ý CHÍNH: hàng không có RẤT NHIỀU chuẩn bus chuyên dụng ra đời qua từng thời kỳ, mỗi chuẩn giải quyết đúng 1 nhu cầu hẹp (radar, ghi âm, máy bay nhỏ...). Điểm đáng nhớ nhất cho module này: ARINC 708 dùng mã hoá MANCHESTER thật sự (khác ARINC 429 dùng BPRZ): đây chính là chuẩn bị nhầm lẫn với ARINC 429 trong 1 slide bài giảng (xem khung cảnh báo ⚠️ ở đầu module).</p><p>FDDI đáng chú ý vì lý do “thất bại thú vị”: Boeing tự phát triển riêng cho 777, nhưng sau đó chính Boeing lại quyết định bỏ FDDI để chuyển sang Ethernet 10Mbps rẻ hơn, cho thấy ngay cả chuẩn công nghệ cao cũng có thể bị thay thế vì lý do CHI PHÍ, không chỉ vì lý do kỹ thuật.</p>"
   }
  ],
  [
   {
    "title": "Toàn cảnh bus dữ liệu trên Airbus A320",
    "body": "<p>A320 dùng ĐỒNG THỜI nhiều loại bus, mỗi loại phục vụ đúng nhóm hệ thống phù hợp: AFDX cho hầu hết avionics hiện đại, ARINC 429 cho cảm biến/dữ liệu cơ bản, ARINC 629 cho điều khiển bay thời gian thực, MIL-STD-1553/717 cho động cơ và ghi dữ liệu.</p>",
    "explain": "<p>Sơ đồ “A320 - Connection between major LRUs” trong bài giảng là bản đồ tổng hợp TẤT CẢ nội dung đã học trong module: 5 nhóm LRU (FCS, FMS/Guidance, Air Data, Display/Warning, Communication) ở trên cùng kết nối xuống các TẦNG bus khác nhau (AFDX → ARINC 429 → ARINC 629), rồi xuống các nhóm hệ thống con (Navigation, Engine, Electrical, A/C, Landing Gear, Fuel, Maintenance) ở dưới cùng.</p><p>Thứ tự xếp tầng không phải ngẫu nhiên: AFDX ở trên cùng vì tốc độ cao nhất, kết nối nhiều nhất; ARINC 629 ở gần đáy vì chỉ phục vụ nhóm điều khiển bay hẹp hơn nhưng cần thời gian thực cao nhất.</p>",
    "img": "databus_p03.jpg"
   },
   {
    "title": "Ví dụ dữ liệu thật chảy qua từng loại bus",
    "body": "<table class='tt'><thead><tr><th>Luồng dữ liệu</th><th>Qua bus nào</th></tr></thead><tbody><tr><td>ADIRU → FMGC (dữ liệu khí động, quán tính)</td><td>ARINC 429</td></tr><tr><td>ELAC ↔ SEC ↔ FAC (điều khiển bay)</td><td>ARINC 629</td></tr><tr><td>FMGC ↔ ECAM ↔ CIDS ↔ ACMS (dữ liệu lớn, bảo trì)</td><td>AFDX</td></tr><tr><td>FADEC ↔ động cơ (tham số động cơ)</td><td>MIL-STD-1553/ARINC 717</td></tr></tbody></table>",
    "explain": "<p>Bảng này tổng hợp các ví dụ “Example Connections” rải rác trong nhiều slide của bài giảng thành MỘT bảng duy nhất, giúp thấy rõ: cùng một chiếc máy bay, nhưng từng CẶP thiết bị cụ thể lại dùng ĐÚNG loại bus phù hợp nhất với nhu cầu của riêng cặp đó, không có loại bus nào “làm được tất cả mọi việc tốt nhất”.</p><p>Đây cũng là câu trả lời thực tế cho câu hỏi “tại sao không dùng 1 loại bus duy nhất cho đơn giản”: vì mỗi loại bus đánh đổi tốc độ/độ tin cậy/chi phí khác nhau, dùng SAI loại bus cho 1 nhu cầu cụ thể (vd dùng ARINC 429 chậm cho video bảo trì) sẽ gây nghẽn hoặc không khả thi.</p>"
   },
   {
    "title": "So sánh nhanh 4 chuẩn bus chính",
    "body": "<table class='tt'><thead><tr><th>Tiêu chí</th><th>ARINC 429</th><th>ARINC 629</th><th>AFDX</th><th>MIL-STD-1553</th></tr></thead><tbody><tr><td>Tốc độ</td><td>12,5/100 kbps</td><td>2 Mbps</td><td>100 Mbps</td><td>1 Mbps</td></tr><tr><td>Chiều truyền</td><td>1 chiều</td><td>2 chiều</td><td>2 chiều</td><td>2 chiều</td></tr><tr><td>Điều khiển trung tâm?</td><td>Không cần</td><td>Không cần</td><td>Switch trung tâm</td><td>Bus Controller bắt buộc</td></tr></tbody></table>",
    "explain": "<p>Bảng so sánh này là công cụ hữu ích nhất để TRẢ LỜI NHANH câu hỏi trắc nghiệm kiểu “chuẩn nào có đặc điểm X”: chỉ cần nhớ đúng VỊ TRÍ của 4 chuẩn trong bảng, không cần nhớ rời rạc từng con số.</p><p>Nhận xét xuyên suốt: tốc độ và độ phức tạp kiến trúc TỈ LỆ THUẬN với nhau: ARINC 429 (chậm nhất) có kiến trúc đơn giản nhất (1 chiều, không cần điều khiển gì), còn AFDX (nhanh nhất) có kiến trúc phức tạp nhất (cần switch, quản lý Virtual Link). Đây là sự đánh đổi kỹ thuật kinh điển: muốn nhanh hơn, phải chấp nhận hệ thống phức tạp và tốn kém hơn.</p>"
   },
   {
    "title": "⚠️ Tổng kết bẫy: đối chiếu đa nguồn trước khi ghi nhớ",
    "body": "<div class='callout warn'><p>Chính bài giảng môn này có 1 slide ghi SAI mã hoá của ARINC 429 là “Manchester Biphase-L” (slide 14), trong khi 2 slide KHÁC trong CÙNG bài giảng (slide 3, 13) VÀ sách Tooley đều xác nhận mã hoá ĐÚNG là Bipolar Return to Zero (BPRZ). Manchester là mã hoá của ARINC 708 (radar thời tiết), một chuẩn HOÀN TOÀN KHÁC.</p></div>",
    "explain": "<p>Đây không phải lỗi suy diễn mà là phát hiện TRỰC TIẾP khi đối chiếu nhiều nguồn: cùng 1 bộ slide bài giảng, 2 chỗ nói BPRZ (đúng, khớp sách Tooley và bảng chú giải thuật ngữ BPRZ=bipolar return to zero), 1 chỗ nói Manchester (sai, có lẽ do người soạn nhầm với ARINC 708 hoặc MIL-STD-1553, các chuẩn khác dùng Manchester thật).</p><p>Bài học áp dụng được cho MỌI môn học, không riêng module này: một thông tin kỹ thuật chỉ nên được coi là ĐÁNG TIN khi xuất hiện NHẤT QUÁN ở nhiều chỗ/nhiều nguồn độc lập; nếu 1 nguồn mâu thuẫn với chính nó hoặc với nguồn khác, đó là tín hiệu cần kiểm tra lại, không nên học thuộc ngay chi tiết gây mâu thuẫn đó.</p>"
   },
   {
    "title": "Tự kiểm tra cuối module (không chấm điểm)",
    "body": "<div class='callout good'><p>FADEC cần gửi dữ liệu tham số động cơ với độ tin cậy rất cao, băng thông nhỏ, trong môi trường nhiễu điện từ mạnh gần động cơ. Trong 4 chuẩn đã học (ARINC 429/629/AFDX/MIL-STD-1553), chuẩn nào PHÙ HỢP NHẤT, và vì sao?</p></div>",
    "explain": "<p>Đáp án hợp lý nhất: MIL-STD-1553/ARINC 717, đúng như thực tế bài giảng đã nêu (FADEC trên A320 dùng MIL-STD-1553/ARINC 717). Lý do: đây là chuẩn dành riêng cho ứng dụng cần độ tin cậy cao trong môi trường khắc nghiệt (thiết kế gốc cho quân sự), không cần băng thông lớn (chỉ 1 Mbps là đủ cho tham số động cơ), và có kiến trúc command-response giúp kiểm soát chặt chẽ luồng dữ liệu.</p><p>AFDX dù nhanh nhất nhưng “quá mức cần thiết” và phức tạp hơn mức cần cho riêng dữ liệu động cơ; ARINC 429 có thể dùng được nhưng không tối ưu bằng 1553 cho đúng ngữ cảnh “môi trường nhiễu mạnh + cần độ tin cậy cực cao” này.</p>"
   }
  ]
 ],
 "en": [
  [
   {
    "title": "Point-to-point wiring: the old approach and its problem",
    "body": "<p>Before data buses, every sensor/computer (ADC, FADEC, landing-gear sensor...) had to be wired SEPARATELY to EVERY device that needed its data (EFIS, FMS, ECAM...). With dozens of sensors and dozens of displays/computers, the number of wires grows combinatorially, not linearly.</p>",
    "explain": "<p>Picture 5 sensors, each needing to send data to 5 different displays: point-to-point wiring needs 5×5=25 separate wires. Adding one new sensor means running 5 more new wires (one to each display). This is exactly the left-hand diagram in the lecture slide: ADC, FADEC, landing-gear sensor, fuel-quantity sensor... each device has its own colour-coded bundle of wires running every which way to EFIS, Flight Control Computer, ECAM, FMS.</p><p>The lecture slide lists 4 main drawbacks: a large number of cables (heavy, space-consuming), difficult installation/maintenance/troubleshooting, difficult expansion when adding new equipment, and a high risk of wiring errors due to sheer volume.</p>",
    "img": "databus_p02.jpg"
   },
   {
    "title": "The solution: a shared data bus network",
    "body": "<p>Instead of separate wires for every device pair, ALL devices connect to one (or a few) shared bus lines, sending/receiving data following a single protocol. In the lecture: ARINC 429, ARINC 629, AFDX/664, MIL-STD-1553 are 4 different bus “lanes”, each serving a different set of needs.</p>",
    "explain": "<p>Back to the 5 sensors × 5 displays example: with one shared bus, each sensor needs exactly ONE wire into the bus, and each display needs exactly ONE wire reading from the bus: 10 wires total instead of 25, and this count grows only LINEARLY as devices are added (one more sensor = exactly one more wire), not combinatorially like point-to-point.</p><p>The lecture lists 5 benefits mirroring the 5 drawbacks from the previous slide: significantly fewer cables/less weight, multiple devices can share the same data, easier installation/maintenance/fault isolation, easier integration of new equipment, and standardised error-checking/bus-monitoring support.</p>"
   },
   {
    "title": "6 technical reasons to use a data bus on an aircraft",
    "body": "<table class='tt'><thead><tr><th>#</th><th>Reason</th><th>Short explanation</th></tr></thead><tbody><tr><td>1</td><td>Reduce wiring, weight, space</td><td>Replace thousands of point-to-point wires with a few bus cables</td></tr><tr><td>2</td><td>Share data</td><td>One sensor transmits, many devices receive</td></tr><tr><td>3</td><td>Increase reliability/safety</td><td>Multiple independent buses (e.g. Bus A/B) run in parallel</td></tr><tr><td>4</td><td>Easier maintenance, fault isolation</td><td>Built-in monitoring/error-reporting per the standard</td></tr><tr><td>5</td><td>Easier expansion, upgrade</td><td>New equipment just connects to the bus, no new wiring run</td></tr><tr><td>6</td><td>Supports multiple data types at the right speed</td><td>Each bus type has its own speed/characteristics for its need</td></tr></tbody></table>",
    "explain": "<p>This table combines exactly the 6 boxes at the bottom of slide 2 in the lecture. Worth noting: reason #3 (higher reliability) doesn't come just from HAVING a bus, but from the REDUNDANT design of that bus, e.g. ARINC 629 has Bus A (primary) and Bus B (secondary) operating INDEPENDENTLY: if Bus A fails, Bus B keeps working normally.</p><p>Reason #6 explains why an aircraft does NOT use a single bus type for everything: flight-control data needs high reliability/real-time performance but low volume (suited to ARINC 429/629), while maintenance/image/video data needs high bandwidth (suited to AFDX at 100 Mbps). This is exactly why an A320 runs SEVERAL different bus types IN PARALLEL, not just one.</p>"
   },
   {
    "title": "Four main bus families in modern avionics",
    "body": "<table class='tt'><thead><tr><th>Bus</th><th>Speed</th><th>Type</th><th>Used for</th></tr></thead><tbody><tr><td>ARINC 429</td><td>12.5/100 kbps</td><td>Unidirectional, point-to-point</td><td>Basic avionics, sensor data</td></tr><tr><td>ARINC 629</td><td>2 Mbps</td><td>Bidirectional, dual redundant</td><td>Real-time flight control</td></tr><tr><td>AFDX/ARINC 664</td><td>100 Mbps</td><td>Switched Ethernet</td><td>Large-volume, multi-system data</td></tr><tr><td>MIL-STD-1553/ARINC 717</td><td>1 Mbps / 2-8 Mbps</td><td>Specialised</td><td>Military, FADEC, flight data recording</td></tr></tbody></table>",
    "explain": "<p>This table summarises the 4 coloured columns in the lecture's “Data Buses in an Aircraft (A320)” diagram: green (ARINC 429), blue (ARINC 629), red (AFDX/664), orange (MIL-STD-1553/ARINC 717). Each coloured wire in the original diagram connects a different group of devices: ARINC 429 links sensors to the ADIRU/EFIS/FMS, ARINC 629 interlinks the flight-control computers, AFDX links most modern avionics systems, and MIL-STD-1553/717 is reserved for the engines (FADEC) and the cockpit voice/data recorders.</p><p>The speed ordering (429 &lt; 1553 &lt; 629 &lt; AFDX) is NOT proportional to “importance”: ARINC 429 is the slowest yet remains the most widely used because it is simple, cheap, and extremely reliable for data that does NOT need high bandwidth.</p>"
   },
   {
    "title": "⚠️ Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>An aircraft has 8 sensors, each needing to send its own data to 6 different displays. With point-to-point wiring, how many wires are needed? With a shared bus (assuming each device needs just one wire into the bus), how many wires are needed?</p></div>",
    "explain": "<p>Point-to-point: 8×6=48 separate wires (each sensor wired individually to each display). Shared bus: 8+6=14 wires (every device, whether sensor or display, needs exactly one wire into the bus).</p><p>The gap between 48 and 14 (nearly 3.5 times) clearly shows: point-to-point wiring grows with the PRODUCT of device counts (n×m), while a shared bus grows with the SUM (n+m). This gap widens further as device counts grow, exactly matching reason #1 from the previous slide.</p>"
   }
  ],
  [
   {
    "title": "ARINC 429: the most common avionics bus standard",
    "body": "<p>ARINC 429 is a POINT-TO-POINT, UNIDIRECTIONAL bus: one transmitter (a sending LRU) can connect to up to 20 receivers (receiving LRUs), but data flows in only one direction. For two LRUs to exchange data both ways, two separate ARINC 429 channels are needed, each one-way.</p>",
    "explain": "<p>This is the most confusing point when first learning ARINC 429: why does an LRU like the ADIRU have both Tx (transmit) and Rx (receive) pins? The answer is exactly in slide 11 of the lecture: because ARINC 429 is UNIDIRECTIONAL, one physical channel only carries data one way. If the ADIRU needs to SEND air data to the FMGC AND RECEIVE mode-selection commands from the FMGC, that is two completely separate ARINC 429 channels running in parallel, not one “two-way” channel.</p><p>A complex LRU like the ADIRU can have dozens of different Tx/Rx channels, each one serving exactly one one-way data flow to/from one specific group of devices.</p>"
   },
   {
    "title": "ARINC 429 electrical characteristics",
    "body": "<p>Shielded twisted pair cable. Each wire (A, B) carries +5V/0V/-5V relative to ground. The receiver only cares about the DIFFERENTIAL voltage (A-B): +10V = bit 1, -10V = bit 0, 0V = NULL state (no data).</p>",
    "explain": "<p>Using DIFFERENTIAL signalling instead of measuring the absolute voltage of one wire against ground is a classic noise-immunity technique: if external electromagnetic interference strikes, it typically affects BOTH wires A and B nearly EQUALLY (since they are tightly twisted together), so the difference (A-B) stays nearly UNCHANGED, preserving the bit value even in a very electrically noisy environment (engines, radar).</p><p>The voltage table in the lecture is easy to remember by its symmetry: bit 1 → A positive/B negative; bit 0 → A negative/B positive (fully inverted); NULL → both wires return to 0V (no difference).</p>"
   },
   {
    "title": "BPRZ encoding: why must every bit “return to 0V”?",
    "body": "<p>ARINC 429 uses Bipolar Return to Zero (BPRZ) encoding: between every bit, the signal always returns to 0V before the next bit starts. This lets the receiver recover timing (self-clocking) directly from the data signal, with no separate clock wire needed.</p>",
    "explain": "<p>A direct comparison from the lecture slide: WITHOUT return-to-zero (like NRZ encoding), a run of consecutive “1111” bits would hold the voltage at +10V for all 4 bit periods, with no transition edge for the receiver to tell exactly where one bit ends and the next begins: easy to “lose count” of bits if the two clocks are not perfectly matched. With BPRZ, EVERY bit has at least one rising and one falling edge (even during a run of 1111s), so the receiver always has a reference point to re-count timing and never drifts.</p><p>The trade-off: BPRZ needs a higher SWITCHING FREQUENCY than NRZ at the same bit rate (because of the extra return-to-zero transition within every bit), but in exchange gets much better synchronisation reliability, well worth it for safety-relevant avionics data.</p>",
    "img": "databus_p13.jpg"
   },
   {
    "title": "ARINC 429's two speeds and the time to send one word",
    "body": "<p>ARINC 429 has two speeds: low speed 12.5 kbps (most common) and high speed 100 kbps. Since a data word is always 32 bits: t_word = 32/R. At 12.5 kbps: t=2.56 ms. At 100 kbps: t=0.32 ms (8 times faster).</p>",
    "explain": "<p>This is exactly this module's “formula” (see the formula box below the deck). Plugging in numbers directly: 32 bits / 12,500 bit/s = 0.00256 s = 2.56 ms; and 32 bits / 100,000 bit/s = 0.00032 s = 0.32 ms. Both figures match EXACTLY the “Data Rate and Bit Timing” table in the lecture, independently re-checked with the companion notebook.</p><p>Why do most A320 systems still use the LOW speed (12.5 kbps) instead of the high speed? Because most basic avionics data (airspeed, altitude, warning status...) does not change fast enough to need updates more than a few hundred times per second, so the low speed is already more than sufficient, and is cheaper in terms of circuitry.</p>"
   },
   {
    "title": "Overview of ARINC 429 connections on the A320",
    "body": "<p>ARINC 429 connects almost EVERY system group on the A320: flight control (ELAC/SEC/FAC), guidance (FMGC/MCDU/FCU), air data/inertial (ADIRU), display/warning (DMC/DU/FWC), communication (VHF/HF/AMU/RMP), plus engines, electrical, landing gear, fuel, and more.</p>",
    "explain": "<p>The lecture's diagram shows that ARINC 429 is not a “small, niche” bus used by only a few devices, but rather the BACKBONE connecting most LRUs on the A320, with two parallel buses, Bus A and Bus B, for redundancy. Every LRU in the diagram has its own Tx (red, transmit) and/or Rx (blue, receive) markers, consistent with the unidirectional principle from the previous slide.</p><p>The lecture's “Receiver of some LRUs” table is a good worked example: the ADIRU transmits air data/inertial data, received by MULTIPLE other LRUs (FMGC, FWC, DMC) thanks to ARINC 429's multi-drop property (one transmitter → up to 20 receivers).</p>"
   },
   {
    "title": "⚠️ Trap: confusing cable voltage with differential voltage",
    "body": "<div class='callout warn'><p>Exams often ask “what voltage is present ON THE CABLE of ARINC 429?”: the CORRECT answer is ±5V (the voltage of each individual wire A or B relative to ground), NOT ±10V (that is the DIFFERENTIAL voltage between the two wires, which only appears when comparing A to B).</p></div>",
    "explain": "<p>This is exactly question 9 of the 17 original multiple-choice questions from Tooley, and the book's official answer is ±5V, not +5V/+10V or ±15V. This mix-up is very common because many other sources only mention the “10V” figure (the differential voltage) without clarifying that it is the difference between two wires, not a voltage measured directly on one wire.</p><p>Memory tip: always ask “is THIS voltage measured relative to ground, or relative to the other wire?” before choosing an answer to any differential-voltage question.</p>"
   }
  ],
  [
   {
    "title": "Structure of an ARINC 429 word: 5 fields, 32 bits",
    "body": "<p>Every ARINC 429 word is a FIXED 32 bits long, made of 5 fields in this exact order: <b>Label</b> (8 bits, bits 1-8) → <b>SDI</b> (2 bits) → <b>Data</b> (19 bits) → <b>SSM</b> (2 bits) → <b>Parity</b> (1 bit, bit 32). Bit 1 (part of the Label) is transmitted FIRST, bit 32 (Parity) is transmitted LAST.</p>",
    "explain": "<p>The “LSB first, MSB last” transmission order (bit 1 is the LSB of the whole word, sent first) is a detail that is easy to miss but important when manually decoding an ARINC 429 word from a waveform: counting bits in the wrong order will misread the entire Label/Data.</p><p>8+2+19+2+1 = 32, matching the total word length. This is why questions 8 and 15 of the original multiple-choice bank (Label=8 bits, word length=32 bits) can be derived directly from this diagram without memorisation, just by remembering to add the 5 field lengths correctly.</p>"
   },
   {
    "title": "The Label field: the “name” of the data being sent",
    "body": "<p>The Label (8 bits) identifies the TYPE of data being transmitted, e.g. Label 203 = Indicated Airspeed, Label 204 = Mach Number, Label 205 = Pressure Altitude. Up to 256 distinct Label values are possible (0-255).</p>",
    "explain": "<p>The Label works like a “shipping label” on a package: the receiver does not need to know the package contents in advance, it just reads the Label to know HOW to process the accompanying 19-bit Data (e.g. decode it as BCD or BNR, what unit, what scale).</p><p>Since the Label only has 8 bits (256 values) but the real number of avionics data types exceeds 256, the accompanying SDI (Source/Destination Identifier) field is used to FURTHER distinguish source/destination under the same Label, expanding the number of distinguishable “channels”.</p>"
   },
   {
    "title": "Two Data formats: BCD and BNR",
    "body": "<table class='tt'><thead><tr><th>Format</th><th>Encoding</th><th>Sign</th></tr></thead><tbody><tr><td>BCD</td><td>Each decimal digit = its own 4 bits</td><td>1 sign bit (S) + digits</td></tr><tr><td>BNR</td><td>The whole value = one binary number</td><td>Two's complement</td></tr></tbody></table>",
    "explain": "<p>BCD (as learned in Module 01) splits EACH decimal digit into its own 4 bits: e.g. 250 → CHAR1=2(0010), CHAR2=5(0101), CHAR3=0(0000). Advantage: easy to display directly on a 7-segment display without base conversion. Drawback: wastes bits (4 bits can only represent 10 of 16 possible patterns).</p><p>BNR encodes the ENTIRE value as a single binary number (no digit-splitting), using two's complement for negative values: bit 29 (the Data field's MSB) is the sign bit, 0=positive, 1=negative. BNR is more bit-efficient than BCD, so it is used for data needing high precision such as position or angular rate.</p>",
    "img": "databus_p16.jpg"
   },
   {
    "title": "The SSM field: reporting the status of the data itself",
    "body": "<p>SSM (Sign/Status Matrix, 2 bits) reports what state the data is in. For BNR: 00=Failure Warning, 01=No Computed Data, 10=Functional Test, 11=Normal Operation (valid data).</p>",
    "explain": "<p>This is a very clever SELF-REPORTING mechanism: instead of just sending a NUMBER and hoping it is correct, every ARINC 429 word ALWAYS carries a “confidence label” alongside the data itself. If the ADIRU detects a faulty airspeed sensor, it still sends the word as usual but sets SSM=00 (Failure Warning): the receiver (PFD) reading this SSM will display a warning instead of trusting the (possibly wrong) number in the Data field.</p><p>This is why an avionics engineer debugging a system should NEVER conclude data is correct or wrong just by looking at the Data field alone: the SSM must always be checked first.</p>"
   },
   {
    "title": "The Parity field: self-checking transmission errors with 1 bit",
    "body": "<p>The last bit (bit 32) is an ODD parity bit: the total count of 1-bits across the entire 32-bit word is ALWAYS odd. If the receiver counts an EVEN total, the word is considered corrupted and discarded.</p>",
    "explain": "<p>How it works: the transmitter counts the 1-bits in the first 31 bits (Label+SDI+Data+SSM); if that count is already ODD, it sets Parity=0 (no change needed); if that count is EVEN, it sets Parity=1 (to make the total odd). The receiver simply recounts all 32 bits; an even result means at least one bit was flipped by noise during transmission.</p><p>The limitation of 1-bit parity: it only detects an ODD number of bit errors (1, 3, 5...); if exactly 2 bits flip at the same time (rare but possible), the odd/even total stays correct and the error goes UNDETECTED: this is why higher-safety systems (like AFDX) use a multi-bit CRC instead of a single parity bit.</p>"
   },
   {
    "title": "Complete worked example: encoding an airspeed of 250 kt",
    "body": "<p>The ADIRU computes IAS=250kt → BCD-encodes it: 2→0010, 5→0101, 0→0000 → packs it into the 19-bit Data field. It adds the Label (identifying IAS), SDI, SSM=11 (Normal), computes Parity → packages a 32-bit word → sends it repeatedly about every 100ms over ARINC 429 Bus A to the PFD.</p>",
    "explain": "<p>This is an end-to-end example that brings together EVERY field learned in this section: Label (identifies this as IAS), SDI (identifies source/destination), Data in BCD (the value 250), SSM (reports valid data), Parity (self-checks for errors). The receiver (PFD) does the EXACT REVERSE: checks parity first, reads the Label to know this is IAS, reads the SSM to confirm the data is valid, then finally reads the Data and displays it on the airspeed tape.</p><p>Sending the word REPEATEDLY (not just once) matters a lot: if the PFD misses one word (noise, parity error), it only has to wait about 100ms for the next one, rather than being “stuck” indefinitely from losing exactly one packet.</p>",
    "img": "databus_p12.jpg"
   }
  ],
  [
   {
    "title": "ARINC 629: when you need bidirectional with no central controller",
    "body": "<p>ARINC 629 (2 Mbps, 20 times faster than ARINC 429) is a BIDIRECTIONAL bus: each LRU can both transmit (Tx) and receive (Rx) on the SAME bus. It uses TDMA (Time Division Multiple Access): each LRU is pre-assigned fixed time slot(s) to transmit, avoiding data collisions.</p>",
    "explain": "<p>The single most distinctive feature of ARINC 629, emphasised directly in the lecture: it achieves BIDIRECTIONAL communication WITHOUT needing a separate central bus controller, which could otherwise become a single point of failure if it broke down. Instead, each LRU knows its own “turn” (slot) within the Major Frame through shared timing synchronisation, with no need for anyone to signal “it's your turn to transmit”.</p><p>With 125 slots of 16 μs each within a 2ms Major Frame, and up to 20-21 LRUs on one bus: these are the actual figures from the lecture, and can be used to re-derive the full cycle time (125×16μs=2000μs=2ms, which checks out exactly).</p>",
    "img": "databus_p06.jpg"
   },
   {
    "title": "ARINC 629 frame structure: 52 bits",
    "body": "<p>Each ARINC 629 frame consists of: Sync (8 bits) + Data (32 bits, 4 bytes) + SDI (2 bits) + Label (8 bits) + SSM (2 bits) = 52 bits. Compared to ARINC 429 (32 bits/word, no separate Sync), ARINC 629 adds a Sync field to synchronise frames in a TDMA system shared by many LRUs.</p>",
    "explain": "<p>An interesting observation: ARINC 629's Label (8 bits), SDI (2 bits) and SSM (2 bits) are IDENTICAL in size and meaning to ARINC 429's, showing that ARINC 629 was designed as a direct extension of ARINC 429, simply EXPANDED to support many LRUs sharing one bus (needing Sync to know when a frame starts) and bidirectional flow.</p><p>Since each 52-bit frame transmits within a 16μs slot at 2 Mbps: 16μs × 2,000,000 bit/s = 32,000 bits, far more than the 52-bit frame itself, because each slot also includes a gap between frames to prevent signal overlap between adjacent LRUs.</p>"
   },
   {
    "title": "AFDX/ARINC 664: when data needs high bandwidth",
    "body": "<p>AFDX (Avionics Full-Duplex Switched Ethernet) is 100 Mbps switched Ethernet, used on the A380/A350 (and partly on newer A320s). Instead of a shared bus like 429/629, AFDX uses a central SWITCH, with each device connected to its own dedicated switch port.</p>",
    "explain": "<p>The most important architectural difference: ARINC 429/629 is a “shared line” type bus (all devices listen on the same physical transmission line), while AFDX is a “star via switch” type network (similar to an office Ethernet network): each LRU has its own DEDICATED wire to the switch, and the switch is responsible for forwarding each packet to the correct destination.</p><p>Because it uses a switch, AFDX reaches 100 Mbps bandwidth, enough for “heavy” data like maintenance imagery, camera video, and simultaneous data from many systems: data types that are simply NOT feasible on ARINC 429 (only 12.5-100 kbps).</p>",
    "img": "databus_p07.jpg"
   },
   {
    "title": "Virtual Link (VL): a “dedicated lane” inside AFDX",
    "body": "<p>A physical AFDX network is divided into multiple LOGICAL Virtual Links (VLs), each with its own bandwidth, frame size, and minimum transmission period (BAG - Bandwidth Allocation Gap). The switch ensures VLs are ISOLATED from each other, so no VL can consume another VL's bandwidth.</p>",
    "explain": "<p>Think of VLs as dedicated lanes on the same highway (the physical Ethernet cable): although all cars (data) travel on the same road, each lane (VL) has its own speed limit and traffic capacity, and cars in one lane cannot spill over into another. This is exactly how AFDX achieves DETERMINISM: while ordinary Ethernet networks can suffer unpredictable “congestion”, AFDX guarantees that each critical data flow (e.g. flight-control commands) ALWAYS gets its committed share of bandwidth, unaffected by other data (e.g. passenger entertainment video).</p><p>This is why AFDX is suitable for carrying BOTH safety-critical data (flight control) AND non-critical data (cabin, entertainment) on the same physical network without fear of conflict.</p>"
   },
   {
    "title": "MIL-STD-1553B: a military bus with a central controller",
    "body": "<p>MIL-STD-1553B uses a command-response architecture with one Bus Controller (BC) managing up to 31 Remote Terminals (RT), at 1 Mbps. MIL-STD-1773B is the fibre-optic version, with much greater immunity to high-intensity radiated electromagnetic fields (HIRF).</p>",
    "explain": "<p>Quite the opposite philosophy from ARINC 629's “no central controller needed”: MIL-STD-1553B DELIBERATELY uses a single Bus Controller to command every Remote Terminal: the BC asks “RT number 5, what data do you have”, and RT5 responds, exactly a command-response pattern. This choice suits military environments where tight control and precise predictability of which device is “speaking” at any moment are required.</p><p>On a civilian A320, this standard (along with ARINC 717) is mainly used for FADEC (engine control) and the cockpit voice/data recorders (CVR/FDR), where extremely high reliability is needed but high bandwidth is not.</p>"
   },
   {
    "title": "Other older/specialised bus standards (brief history)",
    "body": "<table class='tt'><thead><tr><th>Standard</th><th>Key feature</th></tr></thead><tbody><tr><td>ARINC 419/561</td><td>Predecessors of 429, pre-1970, six-wire or two-wire systems</td></tr><tr><td>ARINC 573/717</td><td>Flight data recording (FDR), Harvard Bi-Phase encoding</td></tr><tr><td>ARINC 708</td><td>Weather radar, Manchester encoding, 1 Mbps</td></tr><tr><td>CSDB / ASCB</td><td>Proprietary Collins/Honeywell standards, small aircraft</td></tr><tr><td>FDDI</td><td>100 Mbps dual-ring network, developed for the Boeing 777</td></tr></tbody></table>",
    "explain": "<p>This table does not need to be memorised in detail, only the KEY IDEA: aviation has MANY specialised bus standards that emerged over different eras, each solving one narrow need (radar, voice recording, small aircraft...). The single most memorable point for this module: ARINC 708 genuinely uses MANCHESTER encoding (unlike ARINC 429's BPRZ): this is exactly the standard that got mixed up with ARINC 429 in one lecture slide (see the ⚠️ warning box at the start of this module).</p><p>FDDI is notable for an “interesting failure” story: Boeing developed it specifically for the 777, but later Boeing itself decided to drop FDDI in favour of cheaper 10Mbps Ethernet, showing that even a technically advanced standard can be replaced for COST reasons, not just technical ones.</p>"
   }
  ],
  [
   {
    "title": "Overview of data buses on the Airbus A320",
    "body": "<p>The A320 uses SEVERAL bus types SIMULTANEOUSLY, each serving the group of systems it fits best: AFDX for most modern avionics, ARINC 429 for sensors/basic data, ARINC 629 for real-time flight control, MIL-STD-1553/717 for engines and data recording.</p>",
    "explain": "<p>The lecture's “A320 - Connection between major LRUs” diagram is a map that ties together EVERYTHING learned in this module: 5 LRU groups (FCS, FMS/Guidance, Air Data, Display/Warning, Communication) at the top connect down through different bus LAYERS (AFDX → ARINC 429 → ARINC 629), then down to sub-system groups (Navigation, Engine, Electrical, A/C, Landing Gear, Fuel, Maintenance) at the bottom.</p><p>The layering order is not random: AFDX sits at the top because it is the fastest and connects the most devices; ARINC 629 sits nearer the bottom because it only serves the narrower flight-control group, but with the highest real-time requirement.</p>",
    "img": "databus_p03.jpg"
   },
   {
    "title": "Real data flow examples through each bus type",
    "body": "<table class='tt'><thead><tr><th>Data flow</th><th>Via which bus</th></tr></thead><tbody><tr><td>ADIRU → FMGC (air data, inertial data)</td><td>ARINC 429</td></tr><tr><td>ELAC ↔ SEC ↔ FAC (flight control)</td><td>ARINC 629</td></tr><tr><td>FMGC ↔ ECAM ↔ CIDS ↔ ACMS (large data, maintenance)</td><td>AFDX</td></tr><tr><td>FADEC ↔ engines (engine parameters)</td><td>MIL-STD-1553/ARINC 717</td></tr></tbody></table>",
    "explain": "<p>This table gathers “Example Connections” scattered across several lecture slides into ONE table, making it clear: on the same aircraft, each SPECIFIC device pair uses the bus type that best fits ITS OWN need, and no single bus type “does everything best”.</p><p>This is also the real-world answer to “why not just use one bus type for simplicity”: because each bus type trades off speed/reliability/cost differently, and using the WRONG bus type for a specific need (e.g. slow ARINC 429 for maintenance video) would either cause congestion or simply not work.</p>"
   },
   {
    "title": "Quick comparison of the 4 main bus standards",
    "body": "<table class='tt'><thead><tr><th>Criterion</th><th>ARINC 429</th><th>ARINC 629</th><th>AFDX</th><th>MIL-STD-1553</th></tr></thead><tbody><tr><td>Speed</td><td>12.5/100 kbps</td><td>2 Mbps</td><td>100 Mbps</td><td>1 Mbps</td></tr><tr><td>Direction</td><td>Unidirectional</td><td>Bidirectional</td><td>Bidirectional</td><td>Bidirectional</td></tr><tr><td>Central control?</td><td>Not needed</td><td>Not needed</td><td>Central switch</td><td>Bus Controller required</td></tr></tbody></table>",
    "explain": "<p>This comparison table is the most useful tool for QUICKLY answering multiple-choice questions like “which standard has feature X”: just remember each of the 4 standards' POSITION in the table, instead of memorising scattered individual facts.</p><p>A consistent pattern: speed and architectural complexity are PROPORTIONAL: ARINC 429 (slowest) has the simplest architecture (unidirectional, no control needed), while AFDX (fastest) has the most complex architecture (needs a switch, manages Virtual Links). This is a classic engineering trade-off: going faster requires accepting a more complex and more expensive system.</p>"
   },
   {
    "title": "⚠️ Wrap-up trap: cross-check multiple sources before memorising",
    "body": "<div class='callout warn'><p>This very course's lecture deck has one slide (slide 14) that WRONGLY states ARINC 429's encoding as “Manchester Biphase-L”, while two OTHER slides in the SAME lecture (slides 3 and 13) AND the Tooley textbook both confirm the CORRECT encoding is Bipolar Return to Zero (BPRZ). Manchester is the encoding used by ARINC 708 (weather radar), a COMPLETELY DIFFERENT standard.</p></div>",
    "explain": "<p>This is not a speculative claim but a DIRECT finding from cross-checking multiple sources: within the SAME lecture slide deck, 2 places say BPRZ (correct, matching Tooley and the BPRZ=bipolar-return-to-zero glossary entry), 1 place says Manchester (wrong, likely confused with ARINC 708 or MIL-STD-1553, standards that genuinely do use Manchester).</p><p>The lesson applies to every subject, not just this module: a technical fact should only be trusted when it appears CONSISTENTLY across multiple independent sources/locations; if one source contradicts itself or another source, that is a signal to double-check, not a cue to memorise the conflicting detail right away.</p>"
   },
   {
    "title": "Final self-check (ungraded)",
    "body": "<div class='callout good'><p>FADEC needs to send engine-parameter data with very high reliability, low bandwidth, in an environment with strong electromagnetic interference near the engines. Of the 4 standards covered (ARINC 429/629/AFDX/MIL-STD-1553), which fits BEST, and why?</p></div>",
    "explain": "<p>The most reasonable answer: MIL-STD-1553/ARINC 717, exactly matching what the lecture states as real-world practice (FADEC on the A320 uses MIL-STD-1553/ARINC 717). Reason: this standard was purpose-built for applications needing high reliability in a harsh environment (originally designed for military use), does not need high bandwidth (1 Mbps is enough for engine parameters), and has a command-response architecture that tightly controls the data flow.</p><p>AFDX, although the fastest, is “overkill” and more complex than engine data alone requires; ARINC 429 could technically work but is not as well-suited as 1553 for this specific “strong interference + extremely high reliability needed” context.</p>"
   }
  ]
 ]
}
