# -*- coding: utf-8 -*-
SLIDES = {
  "vi": [
    # PHẦN 1: Quy mô tích hợp: từ SSI tới VLSI
    [
      {"title": "Bốn mức quy mô tích hợp",
       "body": "<p>Quy mô tích hợp (scale of integration) đo bằng số cổng logic tương đương trên một chip:</p>"
               "<table class='tt'><thead><tr><th>Mức</th><th>Số cổng logic</th><th>Ví dụ</th></tr></thead>"
               "<tbody><tr><td>SSI</td><td>1–11</td><td>Một cổng AND/OR/NAND đơn lẻ</td></tr>"
               "<tr><td>MSI</td><td>12–99</td><td>Bộ giải mã, bộ dồn kênh, bus transceiver</td></tr>"
               "<tr><td>LSI</td><td>100–9.999</td><td>Bộ nhớ nhỏ, mạch điều khiển</td></tr>"
               "<tr><td>VLSI</td><td>≥10.000</td><td>Vi xử lý (hàng triệu transistor)</td></tr></tbody></table>"},
      {"title": "Công nghệ chế tạo: từ wafer tới die",
       "body": "<p>Một IC bắt đầu từ một <b>wafer</b> silicon tròn, trên đó hàng trăm mạch giống hệt nhau được "
               "khắc đồng thời bằng công nghệ quang khắc (photolithography). Sau khi kiểm tra, wafer được cắt "
               "thành từng <b>die</b> riêng lẻ, rồi mỗi die được đóng gói (packaging) và nối chân ra ngoài.</p>"},
      {"title": "Ví dụ phân loại 1: cổng logic chuẩn",
       "body": "<p>Một cổng NAND 2 đầu vào đơn lẻ chỉ chứa vài transistor.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Phân loại</div>"
               "<div class='pd-formula-math'>1 cổng logic → SSI</div></div>"
               "<p>Vì số cổng &lt; 12, đây là ví dụ điển hình của quy mô tích hợp nhỏ nhất.</p>"},
      {"title": "Ví dụ phân loại 2: IC bus transceiver 64 cổng",
       "body": "<p>Một IC bus transceiver chứa 64 cổng logic và bộ đệm (Tooley Ch.8 Q9).</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Phân loại</div>"
               "<div class='pd-formula-math'>64 cổng → nằm trong khoảng 12–99 → MSI</div></div>"},
      {"title": "Ví dụ phân loại 3: vi xử lý",
       "body": "<p>Một vi xử lý hiện đại chứa từ vài triệu tới hàng tỉ transistor.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Phân loại</div>"
               "<div class='pd-formula-math'>≥10.000 cổng tương đương → VLSI</div></div>"
               "<p>Đây là lý do vi xử lý luôn được xếp vào VLSI, dù chức năng logic bên trong vẫn dựa trên "
               "cùng nguyên lý cổng logic cơ bản đã học.</p>"},
      {"title": "Ví dụ so sánh: DIP và PLCC",
       "body": "<p>Cùng một mạch MSI có thể đóng gói theo DIP (Dual-In-line Package, 2 hàng chân song song) hoặc "
               "PLCC (Plastic Leaded Chip Carrier, chân bố trí quanh 4 cạnh).</p>"
               "<p>PLCC cho phép nhiều chân hơn trên cùng diện tích đế: hữu ích khi mạch cần nhiều tín hiệu "
               "vào/ra nhưng không gian board hạn chế (Tooley Ch.8 Q5).</p>"},
      {"title": "Bảng so sánh các kiểu đóng gói IC",
       "body": "<table class='tt'><thead><tr><th>Kiểu đóng gói</th><th>Đặc điểm</th><th>Lắp đặt</th></tr></thead>"
               "<tbody><tr><td>DIL/DIP</td><td>2 hàng chân song song</td><td>Xuyên lỗ hoặc đế cắm</td></tr>"
               "<tr><td>PGA</td><td>Chân dạng lưới (pin grid array)</td><td>Đế cắm (socket)</td></tr>"
               "<tr><td>PLCC</td><td>Chân quanh 4 cạnh, gọn hơn DIP</td><td>Đế cắm hoặc hàn</td></tr>"
               "<tr><td>SOIC</td><td>Dán bề mặt, nhỏ gọn</td><td>Luôn hàn cố định</td></tr>"
               "<tr><td>QFP</td><td>Chân mật độ cao quanh 4 cạnh</td><td>Hàn bề mặt</td></tr></tbody></table>"},
      {"title": "Ứng dụng hàng không: chọn đóng gói chịu rung động",
       "body": "<p>Thiết bị avionics phải hoạt động ổn định trong môi trường rung động mạnh và thay đổi nhiệt độ "
               "lớn. Đóng gói kiểu DIP/PGA có đế cắm (socket) tiềm ẩn rủi ro tiếp xúc lỏng do rung động theo "
               "thời gian, nên nhiều LRU hàng không ưu tiên linh kiện hàn cố định (SOIC, QFP) hoặc đế cắm có "
               "khoá cơ khí chống rung, kết hợp keo/verni bảo vệ mối hàn.</p>"},
      {"title": "⚠️ Cảnh báo: đừng suy luận quy mô tích hợp chỉ từ 'tuổi đời' của chip",
       "body": "<div class='callout warn'><p>Một chip sản xuất năm 1981 nhiều khả năng là DIP/SSI-MSI, nhưng đây "
               "chỉ là suy luận theo <i>công nghệ phổ biến thời kỳ đó</i>, không phải quy luật tuyệt đối. Quy mô "
               "tích hợp được xác định bằng SỐ CỔNG LOGIC THỰC TẾ trên chip, không phải năm sản xuất.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Trước khi sang phần tiếp theo, hãy tự trả lời: một IC chứa khoảng 200 cổng logic thuộc quy mô "
               "tích hợp nào? Nó có khả năng được đóng gói theo kiểu nào nếu sản xuất sau năm 2000?</p>"},
    ],
    # PHẦN 2: Fan-in và fan-out
    [
      {"title": "Định nghĩa fan-out",
       "body": "<p><b>Fan-out</b> là số đầu vào chuẩn (cùng họ logic) tối đa mà một đầu ra có thể điều khiển an "
               "toàn mà không làm mức logic bị lệch khỏi giới hạn cho phép.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Fan-out TTL chuẩn</div>"
               "<div class='pd-formula-math'>Fan-out = 10 đầu vào TTL cùng họ</div></div>"},
      {"title": "Định nghĩa fan-in",
       "body": "<p><b>Fan-in</b> là tải tương đương (tính theo số đầu vào chuẩn cùng họ logic) mà MỘT đầu vào cụ "
               "thể áp lên tầng trước nó.</p>"
               "<ul class='pd-legend'><li><b>Đầu vào chuẩn</b><span>fan-in = 1</span></li>"
               "<li><b>Đầu vào nối 2 cổng cùng lúc</b><span>fan-in = 2</span></li></ul>"},
      {"title": "Ví dụ: tính fan-in của một mạch",
       "body": "<p>Cho mạch có đầu vào B nối đồng thời tới cổng G3 và G4 (mỗi cổng là thiết bị chuẩn, fan-in mỗi "
               "đầu vào = 1). Vậy tải mà B áp lên tầng trước = 1 (từ G3) + 1 (từ G4) = <b>2</b>.</p>"},
      {"title": "Ví dụ: tính fan-out tối thiểu của một cổng",
       "body": "<p>Cổng G1 phải điều khiển 6 cổng phía sau (G2 đến G7), mỗi cổng là thiết bị chuẩn (fan-in=1 mỗi "
               "cổng). Vậy G1 cần fan-out tối thiểu là:</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Fan-out tối thiểu</div>"
               "<div class='pd-formula-math'>6 cổng tải × 1 (fan-in mỗi cổng) = 6</div></div>"},
      {"title": "Điều gì xảy ra nếu vượt quá fan-out?",
       "body": "<p>Khi số tải vượt fan-out cho phép, cổng nguồn không đủ dòng để giữ mức logic 'cao' (không đủ "
               "nguồn dòng ra) hoặc mức 'thấp' (không đủ khả năng hút dòng vào), khiến điện áp thực tế trôi "
               "khỏi ngưỡng logic hợp lệ: mạch hoạt động sai hoặc không ổn định.</p>"},
      {"title": "Ví dụ số: dùng bộ đệm (buffer) khi vượt fan-out",
       "body": "<p>Một cổng TTL chuẩn (fan-out=10) cần điều khiển 25 đầu vào TTL. Vì 25 &gt; 10, cần chèn thêm bộ "
               "đệm (buffer/driver) có fan-out cao hơn (vd 30) giữa cổng nguồn và các tải, thay vì nối trực "
               "tiếp.</p>"},
      {"title": "Bảng fan-out danh định theo họ logic",
       "body": "<table class='tt'><thead><tr><th>Họ logic</th><th>Fan-out danh định (cùng họ)</th></tr></thead>"
               "<tbody><tr><td>TTL chuẩn</td><td>10</td></tr><tr><td>TTL Schottky công suất thấp (LS)</td><td>20</td></tr>"
               "<tr><td>CMOS chuẩn</td><td>~50 (do trở kháng vào rất cao)</td></tr></tbody></table>"},
      {"title": "Ứng dụng hàng không: phân phối tín hiệu clock",
       "body": "<p>Trong máy tính buồng lái, một xung clock từ dao động thạch anh trung tâm thường cần cấp cho "
               "nhiều mạch con (bộ đếm thời gian, bộ mã hoá dữ liệu, bộ hiển thị). Kỹ sư thiết kế phải tính "
               "tổng fan-in của toàn bộ mạch nhận clock để chọn đúng bộ đệm phân phối clock (clock buffer/driver) "
               "đủ fan-out, tránh suy hao tín hiệu định thời quan trọng.</p>"},
      {"title": "⚠️ Cảnh báo: fan-out không cộng dồn qua nhiều họ logic khác nhau",
       "body": "<div class='callout warn'><p>Fan-out danh định (vd 10 của TTL) chỉ đúng khi tải là đầu vào CÙNG "
               "HỌ logic. Khi trộn TTL với CMOS, phải quy đổi tải theo bảng tương thích giữa 2 họ (input "
               "loading khác nhau), không được cộng trực tiếp số lượng đầu vào như cùng họ.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Một cổng CMOS có fan-out 50 cần điều khiển 12 đầu vào CMOS chuẩn: có an toàn không? Nếu 3 "
               "trong số đó là đầu vào TTL (không phải CMOS), bạn cần kiểm tra thêm điều gì trước khi kết luận?</p>"},
    ],
    # PHẦN 3: Bộ giải mã và bộ mã hoá (decoder/encoder)
    [
      {"title": "Định nghĩa bộ giải mã (decoder)",
       "body": "<p>Bộ giải mã nhận n đường địa chỉ nhị phân và kích hoạt ĐÚNG MỘT trong 2ⁿ đường ra tương ứng "
               "với tổ hợp địa chỉ đó: dùng để chọn 1 thiết bị/vị trí nhớ trong nhiều lựa chọn.</p>"},
      {"title": "Định nghĩa bộ mã hoá (encoder)",
       "body": "<p>Bộ mã hoá thực hiện chức năng NGƯỢC LẠI: nhận tín hiệu tích cực trên 1 trong N đường vào, xuất "
               "ra mã nhị phân tương ứng trên log₂(N) đường ra.</p>"},
      {"title": "Ví dụ: thiết kế bảng chân trị decoder 2-sang-4",
       "body": "<table class='tt'><thead><tr><th>A1</th><th>A0</th><th>Y0</th><th>Y1</th><th>Y2</th><th>Y3</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr>"
               "<tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr></tbody></table>"
               "<p>Ở mỗi hàng, đúng một ngõ ra bằng 1, có chỉ số bằng giá trị nhị phân của A1A0.</p>"},
      {"title": "Ví dụ: bộ mã hoá ưu tiên 4-sang-2",
       "body": "<p>Nếu nhiều đầu vào cùng tích cực, bộ mã hoá ƯU TIÊN chọn đầu vào có chỉ số CAO NHẤT để mã hoá. "
               "Vd đầu vào I1 và I3 cùng tích cực → mã hoá theo I3 (ưu tiên cao hơn) → ngõ ra = 11 (nhị phân "
               "của 3), bỏ qua I1.</p>"},
      {"title": "Ví dụ: chuyển đổi mã BCD sang 7 đoạn",
       "body": "<p>Bộ chuyển đổi mã (code converter) BCD-sang-7-đoạn nhận 4 bit BCD (0000-1001) và xuất ra 7 tín "
               "hiệu điều khiển từng đoạn (a-g) của LED 7 đoạn để hiển thị đúng chữ số thập phân tương ứng: "
               "nguyên lý dùng trong hiển thị số trên nhiều thiết bị đo lường buồng lái.</p>"},
      {"title": "Ví dụ: chân enable dùng để ghép tầng",
       "body": "<p>Một IC decoder 3-sang-8 có thêm 1 chân Enable. Khi Enable=0, TOÀN BỘ ngõ ra bị khoá về mức "
               "không tích cực bất kể địa chỉ vào là gì. Ghép 2 IC decoder 3-sang-8 qua chân Enable cho phép mở "
               "rộng thành 1 decoder 4-sang-16 (dùng bit địa chỉ thứ 4 để chọn IC nào được Enable).</p>"},
      {"title": "Bảng so sánh 4 mạch MSI cơ bản",
       "body": "<table class='tt'><thead><tr><th>Mạch</th><th>Chiều xử lý</th><th>Ứng dụng chính</th></tr></thead>"
               "<tbody><tr><td>Decoder</td><td>n vào → 2ⁿ ra (đúng 1 ra tích cực)</td><td>Giải mã địa chỉ bộ nhớ</td></tr>"
               "<tr><td>Encoder</td><td>N vào → log₂N ra</td><td>Mã hoá bàn phím</td></tr>"
               "<tr><td>Multiplexer</td><td>N kênh dữ liệu → 1 ra</td><td>Chọn 1 trong nhiều nguồn tín hiệu</td></tr>"
               "<tr><td>Demultiplexer</td><td>1 vào → N kênh ra</td><td>Phân phối tín hiệu tới nhiều đích</td></tr></tbody></table>"},
      {"title": "Ứng dụng hàng không: giải mã địa chỉ bộ nhớ trong máy tính buồng lái",
       "body": "<p>Trong máy tính buồng lái (Tooley Figure 6.11), CPU cần chọn đúng vùng ROM/RAM để đọc/ghi. Một "
               "mạch giải mã địa chỉ (address decoder) nhận các bit cao của address bus và kích hoạt đúng chân "
               "Chip-Select (CS) của ROM hoặc RAM tương ứng, tránh 2 thiết bị nhớ cùng tranh chấp bus dữ liệu.</p>"},
      {"title": "⚠️ Cảnh báo: đừng nhầm decoder 'không có input dữ liệu' với demultiplexer",
       "body": "<div class='callout warn'><p>Về mặt vật lý, decoder và demultiplexer có thể dùng CHUNG một IC "
               "(gán thêm 1 chân làm 'dữ liệu' thay vì luôn giữ mức tích cực cố định). Nhưng về MỤC ĐÍCH chức "
               "năng: decoder dùng để CHỌN đường theo địa chỉ, demux dùng để PHÂN PHỐI 1 luồng dữ liệu tới "
               "nhiều đích: đừng đánh đồng 2 khái niệm chỉ vì cùng linh kiện vật lý.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Một bộ mã hoá ưu tiên 8-sang-3 nhận tín hiệu tích cực đồng thời ở đầu vào 2, 4 và 6. Ngõ ra mã "
               "hoá sẽ ứng với đầu vào nào? Vì sao?</p>"},
    ],
    # PHẦN 4: Bộ dồn kênh (multiplexer/data selector)
    [
      {"title": "Định nghĩa multiplexer",
       "body": "<p>Multiplexer (bộ dồn kênh/data selector) chọn 1 trong N kênh dữ liệu đầu vào để đưa ra 1 ngõ "
               "ra duy nhất, dựa theo tổ hợp nhị phân trên các đường chọn (select lines).</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Số đường chọn cần thiết</div>"
               "<div class='pd-formula-math'>n = log₂(N)</div></div>"},
      {"title": "Ví dụ: bảng chân trị mux 4-sang-1",
       "body": "<table class='tt'><thead><tr><th>S1</th><th>S0</th><th>Ngõ ra Y</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>D0</td></tr><tr><td>0</td><td>1</td><td>D1</td></tr>"
               "<tr><td>1</td><td>0</td><td>D2</td></tr><tr><td>1</td><td>1</td><td>D3</td></tr></tbody></table>"},
      {"title": "Ví dụ tính: số đường chọn cho 16 kênh và 32 kênh",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Áp dụng công thức n=log₂(N)</div>"
               "<div class='pd-formula-math'>N=16 → n=4 &nbsp;&nbsp;|&nbsp;&nbsp; N=32 → n=5</div></div>"
               "<p>Số đường chọn tăng chậm hơn nhiều so với số kênh dữ liệu: đây chính là lý do multiplexer "
               "giúp tiết kiệm dây dẫn so với truyền song song trực tiếp.</p>"},
      {"title": "Ví dụ: ghép tầng 2 IC mux 4-sang-1 thành mux 8-sang-1",
       "body": "<p>Dùng 2 IC mux 4-sang-1 xử lý 2 nhóm 4 kênh, rồi dùng thêm 1 mux 2-sang-1 để chọn kết quả từ "
               "2 IC đó: tổng cộng cần 3 đường chọn (2 đường chọn nội bộ dùng chung cho cả 2 IC + 1 đường chọn "
               "nhóm), đúng khớp n=log₂(8)=3.</p>"},
      {"title": "Định nghĩa demultiplexer",
       "body": "<p>Demultiplexer thực hiện chức năng ngược: nhận 1 luồng dữ liệu đầu vào và phân phối tới đúng 1 "
               "trong N ngõ ra, theo địa chỉ trên các đường chọn: thường dùng chung IC vật lý với decoder.</p>"},
      {"title": "Ví dụ thực tế: mux dữ liệu độ cao trên A320 (Tooley Figure 9.21)",
       "body": "<p>Bộ dồn kênh kép 4 kênh chọn 1 trong 4 nguồn dữ liệu độ cao (độ cao đã chọn, độ cao thực tế từ "
               "ADC trái/phải) để đưa vào bộ mã hoá dữ liệu nối tiếp ARINC 429, chỉ cần 2 đường chọn nhị phân "
               "thay vì 4 đường truyền vật lý riêng biệt.</p>"},
      {"title": "Bảng: số kênh, số đường chọn, và số dây tiết kiệm được",
       "body": "<table class='tt'><thead><tr><th>Số kênh N</th><th>Đường chọn n</th><th>Không dùng mux (N dây)</th></tr></thead>"
               "<tbody><tr><td>4</td><td>2</td><td>4</td></tr><tr><td>8</td><td>3</td><td>8</td></tr>"
               "<tr><td>16</td><td>4</td><td>16</td></tr></tbody></table>"
               "<p>Với mux, chỉ cần n đường chọn + 1 đường dữ liệu ra chung, thay vì N đường dữ liệu song song.</p>"},
      {"title": "Ứng dụng hàng không: chia sẻ 1 bus hiển thị cho nhiều tham số",
       "body": "<p>Màn hình ECAM cần luân phiên hiển thị nhiều tham số động cơ (N1, EGT, N2, dầu bôi trơn...). "
               "Một mux tốc độ cao có thể chọn lần lượt từng nguồn tín hiệu để đưa vào bộ xử lý hiển thị chung, "
               "giảm số kênh xử lý tín hiệu độc lập cần thiết.</p>"},
      {"title": "⚠️ Cảnh báo: đường chọn không đủ sẽ làm mất dữ liệu, không phải lỗi ngẫu nhiên",
       "body": "<div class='callout warn'><p>Nếu thiết kế mux 8 kênh nhưng chỉ dùng 2 đường chọn (chỉ phân biệt "
               "được 4 tổ hợp), 4 kênh còn lại sẽ KHÔNG BAO GIỜ được chọn tới: đây là lỗi thiết kế có thể dự "
               "đoán trước bằng công thức n=log₂(N), không phải lỗi ngẫu nhiên cần dò tìm bằng thực nghiệm.</p></div>"},
      {"title": "Tự kiểm tra nhanh",
       "body": "<p>Bạn cần chọn 1 trong 6 cảm biến nhiệt độ để đưa vào 1 bộ xử lý duy nhất. Cần tối thiểu bao "
               "nhiêu đường chọn? Có kênh nào bị 'thừa' không sử dụng đến trong không gian địa chỉ tạo ra không?</p>"},
    ],
    # PHẦN 5: Áp dụng trong hệ thống avionics
    [
      {"title": "Tổng quan: MSI logic trong avionics dùng ở đâu?",
       "body": "<p>Theo Tooley, MSI logic trong máy bay tập trung ở 5 nhóm ứng dụng chính: giải mã địa chỉ, mã "
               "hoá ưu tiên, dồn kênh dữ liệu, chuyển đổi mã BCD-sang-7-đoạn, và kiểm tra chẵn lẻ (parity) trên "
               "đường truyền dữ liệu.</p>"},
      {"title": "Ví dụ lại: bộ dồn kênh ARINC 429 (Figure 9.21)",
       "body": "<p>4 nguồn dữ liệu độ cao được dồn kênh trước khi đưa vào bộ mã hoá dữ liệu nối tiếp ARINC 429 "
               ": đây là ví dụ trực tiếp lấy từ sách, minh hoạ multiplexer trong hệ thống altimeter thực tế.</p>"},
      {"title": "Ví dụ: parity checker trên bus dữ liệu",
       "body": "<p>Mạch tạo/kiểm tra chẵn lẻ (built chủ yếu từ chuỗi cổng XOR) thêm 1 bit parity vào dữ liệu "
               "truyền trên bus. Bên nhận tính lại parity và so sánh: nếu khác, phát hiện có lỗi truyền dữ liệu "
               "(dù không xác định được lỗi ở bit nào).</p>"},
      {"title": "Ví dụ tính: parity chẵn (even parity) của 1 byte dữ liệu",
       "body": "<p>Byte dữ liệu <code>10110010</code> có 4 bit 1 → số chẵn.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Bit parity chẵn cần thêm</div>"
               "<div class='pd-formula-math'>0 (giữ tổng số bit 1 là số chẵn)</div></div>"},
      {"title": "Ví dụ: giải mã địa chỉ trong hệ thống backplane bus",
       "body": "<p>Trong hệ thống nhiều board cắm chung 1 backplane bus (vd VMEbus), mỗi board có 1 mã địa chỉ "
               "cố định. Mạch giải mã trên mỗi board so sánh địa chỉ trên bus với mã của chính nó: chỉ board "
               "khớp địa chỉ mới đáp ứng, tránh xung đột dữ liệu.</p>"},
      {"title": "Ví dụ: hiển thị N1, EGT trên ECAM bằng BCD-sang-7-đoạn",
       "body": "<p>Giá trị N1 động cơ (vd 92%) được xử lý dưới dạng BCD nội bộ, sau đó bộ chuyển đổi mã "
               "BCD-sang-7-đoạn tạo tín hiệu điều khiển đúng các đoạn LED/segment hiển thị để phi công đọc trực "
               "tiếp con số thập phân, không cần diễn giải mã nhị phân.</p>"},
      {"title": "Bảng tổng hợp: mạch MSI ↔ ứng dụng avionics thực tế",
       "body": "<table class='tt'><thead><tr><th>Mạch MSI</th><th>Ứng dụng avionics</th></tr></thead>"
               "<tbody><tr><td>Multiplexer</td><td>Dồn kênh dữ liệu độ cao trước khi mã hoá ARINC 429</td></tr>"
               "<tr><td>Decoder</td><td>Giải mã địa chỉ bộ nhớ / board trên backplane bus</td></tr>"
               "<tr><td>Encoder ưu tiên</td><td>Mã hoá phím bấm trên bàn phím MCDU</td></tr>"
               "<tr><td>Code converter</td><td>BCD-sang-7-đoạn cho hiển thị ECAM</td></tr>"
               "<tr><td>Parity generator/checker</td><td>Kiểm tra lỗi truyền trên bus dữ liệu</td></tr></tbody></table>"},
      {"title": "Vì sao MSI (thay vì SSI hoặc VLSI) phù hợp cho các chức năng này?",
       "body": "<p>Các chức năng trên (giải mã, mã hoá, dồn kênh) đều là logic cố định, không cần khả năng lập "
               "trình phức tạp của VLSI, nhưng cũng phức tạp hơn một vài cổng SSI đơn lẻ: MSI là lựa chọn cân "
               "bằng giữa chi phí, độ tin cậy (ít điểm hàn hơn khi gộp nhiều cổng vào 1 IC) và đủ chức năng cần "
               "thiết.</p>"},
      {"title": "⚠️ Cảnh báo: đường trễ tín hiệu (propagation delay) cộng dồn qua nhiều tầng MSI",
       "body": "<div class='callout warn'><p>Khi ghép tầng nhiều IC MSI (vd 2 tầng decoder, hoặc mux rồi tới "
               "encoder), độ trễ lan truyền tín hiệu của từng tầng CỘNG DỒN lại. Với hệ thống cần đáp ứng thời "
               "gian thực nghiêm ngặt (vd cảnh báo an toàn), phải tính tổng trễ qua toàn bộ chuỗi MSI, không chỉ "
               "xét trễ của từng IC riêng lẻ.</p></div>"},
      {"title": "Tổng kết module & tự kiểm tra",
       "body": "<p>Bạn đã đi qua: quy mô tích hợp (SSI→VLSI), fan-in/fan-out, decoder/encoder, multiplexer, và "
               "ứng dụng thực tế trong avionics. Hãy tự hỏi: nếu phải thiết kế một mạch chọn 1 trong 5 cảm biến "
               "áp suất để hiển thị luân phiên trên 1 màn hình, bạn sẽ dùng mạch MSI nào, cần bao nhiêu đường "
               "chọn, và tại sao?</p>"},
    ],
  ],
  "en": [
    # PART 1: Scale of integration: from SSI to VLSI
    [
      {"title": "Four scales of integration",
       "body": "<p>Scale of integration is measured by the number of equivalent logic gates on a chip:</p>"
               "<table class='tt'><thead><tr><th>Scale</th><th>Gate count</th><th>Example</th></tr></thead>"
               "<tbody><tr><td>SSI</td><td>1–11</td><td>A single AND/OR/NAND gate</td></tr>"
               "<tr><td>MSI</td><td>12–99</td><td>Decoders, multiplexers, bus transceivers</td></tr>"
               "<tr><td>LSI</td><td>100–9,999</td><td>Small memory, control circuits</td></tr>"
               "<tr><td>VLSI</td><td>≥10,000</td><td>Microprocessors (millions of transistors)</td></tr></tbody></table>"},
      {"title": "Fabrication technology: from wafer to die",
       "body": "<p>An IC starts life on a round silicon <b>wafer</b>, on which hundreds of identical circuits are "
               "etched simultaneously using photolithography. After testing, the wafer is cut into individual "
               "<b>dies</b>, each of which is then packaged and wired out to external pins.</p>"},
      {"title": "Classification example 1: a standard logic gate",
       "body": "<p>A single 2-input NAND gate contains only a handful of transistors.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Classification</div>"
               "<div class='pd-formula-math'>1 gate → SSI</div></div>"
               "<p>Since the gate count is below 12, this is the classic example of the smallest integration scale.</p>"},
      {"title": "Classification example 2: a 64-gate bus transceiver",
       "body": "<p>An IC bus transceiver contains 64 logic gates and buffers (Tooley Ch.8 Q9).</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Classification</div>"
               "<div class='pd-formula-math'>64 gates falls in 12–99 → MSI</div></div>"},
      {"title": "Classification example 3: a microprocessor",
       "body": "<p>A modern microprocessor contains from a few million to several billion transistors.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Classification</div>"
               "<div class='pd-formula-math'>≥10,000 equivalent gates → VLSI</div></div>"
               "<p>This is why microprocessors are always classed as VLSI, even though the logic inside still "
               "rests on the same basic gates covered earlier.</p>"},
      {"title": "Comparison example: DIP vs PLCC",
       "body": "<p>The same MSI circuit can be packaged as DIP (Dual-In-line Package, two parallel rows of pins) "
               "or PLCC (Plastic Leaded Chip Carrier, pins around all four sides).</p>"
               "<p>PLCC allows more pins in the same footprint area: useful when a circuit needs many I/O "
               "signals but board space is limited (Tooley Ch.8 Q5).</p>"},
      {"title": "Comparison table of IC package types",
       "body": "<table class='tt'><thead><tr><th>Package</th><th>Feature</th><th>Mounting</th></tr></thead>"
               "<tbody><tr><td>DIL/DIP</td><td>Two parallel rows of pins</td><td>Through-hole or socket</td></tr>"
               "<tr><td>PGA</td><td>Pin grid array</td><td>Socket</td></tr>"
               "<tr><td>PLCC</td><td>Pins on all four sides, smaller than DIP</td><td>Socket or soldered</td></tr>"
               "<tr><td>SOIC</td><td>Surface-mount, compact</td><td>Always soldered</td></tr>"
               "<tr><td>QFP</td><td>High pin density on all four sides</td><td>Surface-mount soldering</td></tr></tbody></table>"},
      {"title": "Aviation application: choosing a vibration-resistant package",
       "body": "<p>Avionics equipment must operate reliably under strong vibration and wide temperature swings. "
               "Socketed packages (DIP/PGA) carry a risk of loose contact over time from vibration, so many "
               "aircraft LRUs favour soldered packages (SOIC, QFP) or sockets with mechanical vibration-locking "
               "features plus conformal coating over solder joints.</p>"},
      {"title": "⚠️ Warning: don't infer integration scale from chip 'age' alone",
       "body": "<div class='callout warn'><p>A chip made in 1981 was most likely DIP/SSI-MSI, but that is only an "
               "inference from the technology common at that time, not an absolute rule. Scale of integration is "
               "defined by the ACTUAL gate count on the chip, not its manufacturing year.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>Before moving on: a chip containing about 200 logic gates belongs to which integration scale? "
               "If it were made after 2000, what packaging style would it likely use?</p>"},
    ],
    # PART 2: Fan-in and fan-out
    [
      {"title": "Defining fan-out",
       "body": "<p><b>Fan-out</b> is the maximum number of standard inputs of the same logic family that an "
               "output can safely drive without pushing logic levels outside spec.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Standard TTL fan-out</div>"
               "<div class='pd-formula-math'>Fan-out = 10 same-family TTL inputs</div></div>"},
      {"title": "Defining fan-in",
       "body": "<p><b>Fan-in</b> is the equivalent load (in standard same-family inputs) that ONE specific input "
               "places on the preceding stage.</p>"
               "<ul class='pd-legend'><li><b>Standard input</b><span>fan-in = 1</span></li>"
               "<li><b>Input feeding two gates at once</b><span>fan-in = 2</span></li></ul>"},
      {"title": "Example: computing the fan-in of a circuit",
       "body": "<p>Input B feeds both gate G3 and gate G4 simultaneously (each a standard device, fan-in 1 per "
               "input). The load B places on the previous stage = 1 (from G3) + 1 (from G4) = <b>2</b>.</p>"},
      {"title": "Example: computing minimum required fan-out",
       "body": "<p>Gate G1 must drive 6 downstream gates (G2 through G7), each a standard device (fan-in=1 "
               "each). The minimum fan-out G1 needs is:</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Minimum fan-out</div>"
               "<div class='pd-formula-math'>6 loads × 1 (fan-in each) = 6</div></div>"},
      {"title": "What happens if fan-out is exceeded?",
       "body": "<p>When the load exceeds the rated fan-out, the source gate cannot supply enough current to hold "
               "the 'high' level (insufficient source current) or sink enough current for the 'low' level "
               "(insufficient sink current), so the actual voltage drifts outside valid logic thresholds: the "
               "circuit misbehaves or becomes unreliable.</p>"},
      {"title": "Numeric example: adding a buffer when fan-out is exceeded",
       "body": "<p>A standard TTL gate (fan-out=10) must drive 25 TTL inputs. Since 25 &gt; 10, a buffer/driver "
               "with higher fan-out (e.g. 30) must be inserted between the source gate and the loads, instead "
               "of connecting them directly.</p>"},
      {"title": "Table: rated fan-out by logic family",
       "body": "<table class='tt'><thead><tr><th>Logic family</th><th>Rated fan-out (same family)</th></tr></thead>"
               "<tbody><tr><td>Standard TTL</td><td>10</td></tr><tr><td>Low-power Schottky TTL (LS)</td><td>20</td></tr>"
               "<tr><td>Standard CMOS</td><td>~50 (due to very high input impedance)</td></tr></tbody></table>"},
      {"title": "Aviation application: distributing a clock signal",
       "body": "<p>In a cockpit clock computer, a clock pulse from the central crystal oscillator often must feed "
               "several sub-circuits (timekeeping counter, data encoder, display driver). Engineers must sum the "
               "total fan-in of every circuit receiving that clock to select a clock distribution buffer/driver "
               "with adequate fan-out, avoiding degradation of a critical timing signal.</p>"},
      {"title": "⚠️ Warning: fan-out does not add up across different logic families",
       "body": "<div class='callout warn'><p>A rated fan-out (e.g. TTL's 10) only holds when the loads are inputs "
               "of the SAME logic family. When mixing TTL with CMOS, loads must be converted using the "
               "cross-family input-loading compatibility table, not simply added as if they were the same "
               "family.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>A CMOS gate with fan-out 50 must drive 12 standard CMOS inputs: is that safe? If 3 of those "
               "12 are actually TTL inputs (not CMOS), what else must you check before concluding it's safe?</p>"},
    ],
    # PART 3: Decoders and encoders
    [
      {"title": "Defining a decoder",
       "body": "<p>A decoder takes n binary address lines and activates EXACTLY ONE of 2ⁿ output lines "
               "corresponding to that address combination: used to select one device/memory location among "
               "many.</p>"},
      {"title": "Defining an encoder",
       "body": "<p>An encoder performs the OPPOSITE function: given an active signal on 1 of N input lines, it "
               "outputs the corresponding binary code on log₂(N) output lines.</p>"},
      {"title": "Example: building the truth table of a 2-to-4 decoder",
       "body": "<table class='tt'><thead><tr><th>A1</th><th>A0</th><th>Y0</th><th>Y1</th><th>Y2</th><th>Y3</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr>"
               "<tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr>"
               "<tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr>"
               "<tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr></tbody></table>"
               "<p>In each row, exactly one output is 1, with index equal to the binary value of A1A0.</p>"},
      {"title": "Example: a 4-to-2 priority encoder",
       "body": "<p>If several inputs are active at once, a PRIORITY encoder selects the HIGHEST-indexed input to "
               "encode. E.g. if both I1 and I3 are active → encode based on I3 (higher priority) → output = 11 "
               "(binary for 3), ignoring I1.</p>"},
      {"title": "Example: BCD-to-7-segment code conversion",
       "body": "<p>A BCD-to-7-segment code converter takes a 4-bit BCD input (0000-1001) and drives 7 segment "
               "control signals (a-g) of an LED display to show the correct decimal digit: the same principle "
               "used for numeric readouts on many cockpit instruments.</p>"},
      {"title": "Example: using enable pins to cascade decoders",
       "body": "<p>A 3-to-8 decoder IC has an extra Enable pin. When Enable=0, ALL outputs are forced inactive "
               "regardless of the address inputs. Cascading two 3-to-8 decoder ICs through their Enable pins "
               "extends the design to a 4-to-16 decoder (using the 4th address bit to select which IC is "
               "enabled).</p>"},
      {"title": "Comparison table of the four basic MSI circuits",
       "body": "<table class='tt'><thead><tr><th>Circuit</th><th>Direction</th><th>Main use</th></tr></thead>"
               "<tbody><tr><td>Decoder</td><td>n in → 2ⁿ out (exactly 1 active)</td><td>Memory address decoding</td></tr>"
               "<tr><td>Encoder</td><td>N in → log₂N out</td><td>Keyboard encoding</td></tr>"
               "<tr><td>Multiplexer</td><td>N data channels → 1 out</td><td>Select one of many signal sources</td></tr>"
               "<tr><td>Demultiplexer</td><td>1 in → N out channels</td><td>Distribute a signal to many destinations</td></tr></tbody></table>"},
      {"title": "Aviation application: memory address decoding in a cockpit computer",
       "body": "<p>In a cockpit clock computer (Tooley Figure 6.11), the CPU must select the right ROM/RAM region "
               "to read/write. An address decoder takes the high-order address bus bits and activates the "
               "correct Chip-Select (CS) pin of the matching ROM or RAM, preventing two memory devices from "
               "contending for the data bus at once.</p>"},
      {"title": "⚠️ Warning: don't confuse a 'dataless' decoder with a demultiplexer",
       "body": "<div class='callout warn'><p>Physically, a decoder and a demultiplexer can share the SAME IC "
               "(by treating one pin as 'data' instead of a fixed active level). But by PURPOSE: a decoder "
               "selects a line based on an address, while a demux distributes one data stream to many "
               "destinations: don't equate the two concepts just because they can share the same physical "
               "chip.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>An 8-to-3 priority encoder has simultaneous active signals on inputs 2, 4, and 6. Which input "
               "will the encoded output correspond to, and why?</p>"},
    ],
    # PART 4: Multiplexers (data selectors)
    [
      {"title": "Defining a multiplexer",
       "body": "<p>A multiplexer (data selector) selects 1 of N input data channels to route to a single output, "
               "based on the binary combination on its select lines.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Select lines required</div>"
               "<div class='pd-formula-math'>n = log₂(N)</div></div>"},
      {"title": "Example: truth table of a 4-to-1 multiplexer",
       "body": "<table class='tt'><thead><tr><th>S1</th><th>S0</th><th>Output Y</th></tr></thead>"
               "<tbody><tr><td>0</td><td>0</td><td>D0</td></tr><tr><td>0</td><td>1</td><td>D1</td></tr>"
               "<tr><td>1</td><td>0</td><td>D2</td></tr><tr><td>1</td><td>1</td><td>D3</td></tr></tbody></table>"},
      {"title": "Worked example: select lines for 16 and 32 channels",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Applying n=log₂(N)</div>"
               "<div class='pd-formula-math'>N=16 → n=4 &nbsp;&nbsp;|&nbsp;&nbsp; N=32 → n=5</div></div>"
               "<p>The number of select lines grows much slower than the number of data channels: this is "
               "exactly why multiplexers save wiring compared with direct parallel transmission.</p>"},
      {"title": "Example: cascading two 4-to-1 muxes into an 8-to-1 mux",
       "body": "<p>Two 4-to-1 mux ICs each handle a group of 4 channels, then a 2-to-1 mux selects between the two "
               "ICs' outputs: 3 select lines total (2 shared select lines for both ICs + 1 group-select line), "
               "exactly matching n=log₂(8)=3.</p>"},
      {"title": "Defining a demultiplexer",
       "body": "<p>A demultiplexer performs the reverse function: it takes one input data stream and routes it to "
               "exactly 1 of N outputs, chosen by the select lines: often sharing the same physical IC as a "
               "decoder.</p>"},
      {"title": "Real example: A320 altitude data multiplexer (Tooley Figure 9.21)",
       "body": "<p>A dual four-channel multiplexer selects 1 of 4 altitude data sources (selected altitude, "
               "actual altitude from the left/right ADC) to feed the ARINC 429 serial data encoder, needing only "
               "2 binary select lines instead of 4 separate physical data paths.</p>"},
      {"title": "Table: channels, select lines, and wiring saved",
       "body": "<table class='tt'><thead><tr><th>Channels N</th><th>Select lines n</th><th>Without mux (N wires)</th></tr></thead>"
               "<tbody><tr><td>4</td><td>2</td><td>4</td></tr><tr><td>8</td><td>3</td><td>8</td></tr>"
               "<tr><td>16</td><td>4</td><td>16</td></tr></tbody></table>"
               "<p>With a mux, only n select lines plus one shared data output are needed, instead of N parallel "
               "data lines.</p>"},
      {"title": "Aviation application: sharing one display bus among several parameters",
       "body": "<p>An ECAM display must cycle through several dynamic engine parameters (N1, EGT, N2, oil "
               "quantity...). A fast multiplexer can select each signal source in turn to feed a shared display "
               "processing path, reducing the number of independent signal-processing channels needed.</p>"},
      {"title": "⚠️ Warning: too few select lines silently drops data, it's not a random fault",
       "body": "<div class='callout warn'><p>If you design an 8-channel mux but only wire 2 select lines "
               "(distinguishing only 4 combinations), the remaining 4 channels will NEVER be selected: this is "
               "a predictable design error from the n=log₂(N) formula, not a random fault requiring "
               "experimental troubleshooting.</p></div>"},
      {"title": "Quick self-check",
       "body": "<p>You need to select 1 of 6 temperature sensors to feed a single processor. What is the minimum "
               "number of select lines required, and are any address combinations left unused?</p>"},
    ],
    # PART 5: Application in avionics systems
    [
      {"title": "Overview: where MSI logic is used in avionics",
       "body": "<p>Per Tooley, MSI logic in aircraft falls into five main application groups: address decoding, "
               "priority encoding, data multiplexing, BCD-to-7-segment code conversion, and parity checking on "
               "data links.</p>"},
      {"title": "Revisited: the ARINC 429 data multiplexer (Figure 9.21)",
       "body": "<p>4 altitude data sources are multiplexed before being fed into the ARINC 429 serial data "
               "encoder: a direct textbook example illustrating a multiplexer in a real altimeter system.</p>"},
      {"title": "Example: a parity checker on a data bus",
       "body": "<p>A parity generator/checker (built mainly from cascaded XOR gates) appends a parity bit to data "
               "transmitted on a bus. The receiver recomputes parity and compares it: a mismatch signals a "
               "transmission error (though it can't identify which bit failed).</p>"},
      {"title": "Worked example: even parity of a data byte",
       "body": "<p>Data byte <code>10110010</code> has 4 ones: an even count.</p>"
               "<div class='pd-formula'><div class='pd-formula-label'>Required even-parity bit</div>"
               "<div class='pd-formula-math'>0 (keeps the total number of 1s even)</div></div>"},
      {"title": "Example: address decoding on a backplane bus system",
       "body": "<p>In a multi-board system sharing one backplane bus (e.g. VMEbus), each board has a fixed "
               "address code. A decoder circuit on each board compares the bus address against its own code: "
               "only the matching board responds, avoiding data conflicts.</p>"},
      {"title": "Example: displaying N1/EGT on ECAM via BCD-to-7-segment",
       "body": "<p>Engine N1 (e.g. 92%) is processed internally as BCD, then a BCD-to-7-segment code converter "
               "drives the correct LED/segment control signals so the pilot reads the decimal figure directly, "
               "with no need to interpret raw binary.</p>"},
      {"title": "Summary table: MSI circuit ↔ real avionics application",
       "body": "<table class='tt'><thead><tr><th>MSI circuit</th><th>Avionics application</th></tr></thead>"
               "<tbody><tr><td>Multiplexer</td><td>Multiplexing altitude data before ARINC 429 encoding</td></tr>"
               "<tr><td>Decoder</td><td>Memory/board address decoding on a backplane bus</td></tr>"
               "<tr><td>Priority encoder</td><td>Encoding key presses on an MCDU keypad</td></tr>"
               "<tr><td>Code converter</td><td>BCD-to-7-segment for ECAM displays</td></tr>"
               "<tr><td>Parity generator/checker</td><td>Detecting transmission errors on a data bus</td></tr></tbody></table>"},
      {"title": "Why MSI (not SSI or VLSI) fits these functions",
       "body": "<p>These functions (decoding, encoding, multiplexing) are fixed logic that doesn't need VLSI's "
               "programmability, yet are more complex than a few standalone SSI gates: MSI strikes a balance "
               "between cost, reliability (fewer solder joints by combining several gates into one IC), and just "
               "enough functionality.</p>"},
      {"title": "⚠️ Warning: propagation delay accumulates across cascaded MSI stages",
       "body": "<div class='callout warn'><p>When cascading multiple MSI ICs (e.g. two decoder stages, or a mux "
               "feeding an encoder), each stage's propagation delay ADDS UP. For systems with strict real-time "
               "requirements (e.g. safety warnings), total delay across the whole MSI chain must be computed, "
               "not just each IC's individual delay.</p></div>"},
      {"title": "Module summary & self-check",
       "body": "<p>You've covered: scale of integration (SSI→VLSI), fan-in/fan-out, decoders/encoders, "
               "multiplexers, and real avionics applications. Ask yourself: if you had to design a circuit that "
               "selects 1 of 5 pressure sensors to display in turn on one screen, which MSI circuit would you "
               "use, how many select lines would you need, and why?</p>"},
    ],
  ],
}
