# -*- coding: utf-8 -*-
"""Slide Module 03 (VI + EN): body + explain (giai thich cho nguoi moi) + img (anh goc tu bai giang)."""

SLIDES = {
 "vi": [
  [
   {
    "title": "Bốn mức quy mô tích hợp",
    "body": "<p>Quy mô tích hợp (scale of integration) đo bằng số cổng logic tương đương trên một chip:</p><table class='tt'><thead><tr><th>Mức</th><th>Số cổng logic</th><th>Ví dụ</th></tr></thead><tbody><tr><td>SSI</td><td>1–11</td><td>Một cổng AND/OR/NAND đơn lẻ</td></tr><tr><td>MSI</td><td>12–99</td><td>Bộ giải mã, bộ dồn kênh, bus transceiver</td></tr><tr><td>LSI</td><td>100–9.999</td><td>Bộ nhớ nhỏ, mạch điều khiển</td></tr><tr><td>VLSI</td><td>≥10.000</td><td>Vi xử lý (hàng triệu transistor)</td></tr></tbody></table>",
    "explain": "<p>Hình đính kèm (trích từ bài giảng gốc) cho thấy trực quan cả 5 mức quy mô tích hợp trên cùng một trục: càng đi sang phải, số cổng logic tương đương càng tăng theo cấp số nhân, từ một cổng NAND đơn lẻ (SSI) cho tới cả một bộ vi xử lý (VLSI/ULSI) chứa hàng triệu cổng.</p><p>Điều quan trọng cần nắm: đây không phải một thang đo tuyến tính. Từ SSI (1 đến 11 cổng) lên MSI (12 đến 99 cổng) chỉ tăng khoảng 10 lần, nhưng từ LSI lên VLSI đã nhảy vọt hàng nghìn lần. Vì vậy khi nói “chip phức tạp hơn”, phải luôn hỏi rõ phức tạp hơn ở MỨC nào, không thể so sánh mơ hồ.</p>",
    "img": "icmux_apps_p09.jpg"
   },
   {
    "title": "Công nghệ chế tạo: từ wafer tới die",
    "body": "<p>Một IC bắt đầu từ một <b>wafer</b> silicon tròn, trên đó hàng trăm mạch giống hệt nhau được khắc đồng thời bằng công nghệ quang khắc (photolithography). Sau khi kiểm tra, wafer được cắt thành từng <b>die</b> riêng lẻ, rồi mỗi die được đóng gói (packaging) và nối chân ra ngoài.</p>",
    "explain": "<p>Quy trình từ wafer tới die giống hệt việc nướng một chiếc bánh lớn rồi cắt thành nhiều miếng nhỏ giống hệt nhau: photolithography (quang khắc) “in” đồng thời hàng trăm mạch giống hệt nhau lên cùng một tấm wafer tròn, sau đó máy cắt wafer thành từng die riêng lẻ.</p><p>Lý do làm theo cách này thay vì chế tạo từng chip một: chi phí thiết lập quy trình khắc (mặt nạ quang khắc, máy móc) rất cao, nhưng một khi đã thiết lập xong, in thêm hàng trăm bản sao trên cùng một wafer gần như không tốn thêm chi phí đáng kể, giúp giảm mạnh giá thành mỗi chip khi sản xuất số lượng lớn.</p>"
   },
   {
    "title": "Ví dụ phân loại 1: cổng logic chuẩn",
    "body": "<p>Một cổng NAND 2 đầu vào đơn lẻ chỉ chứa vài transistor.</p><div class='pd-formula'><div class='pd-formula-label'>Phân loại</div><div class='pd-formula-math'>1 cổng logic → SSI</div></div><p>Vì số cổng &lt; 12, đây là ví dụ điển hình của quy mô tích hợp nhỏ nhất.</p>",
    "explain": "<p>Đây là ví dụ đơn giản nhất để bắt đầu làm quen với việc phân loại: chỉ cần đếm số cổng logic trong một linh kiện, rồi tra vào bảng 4 mức đã học ở slide đầu.</p><p>Một cổng NAND 2 đầu vào chỉ cần vài transistor để chế tạo (thường 4 transistor với công nghệ CMOS), và số cổng logic tương đương là 1, nằm rõ ràng trong khoảng 1 đến 11 của SSI, không cần bàn cãi gì thêm.</p>"
   },
   {
    "title": "Ví dụ phân loại 2: IC bus transceiver 64 cổng",
    "body": "<p>Một IC bus transceiver chứa 64 cổng logic và bộ đệm (Tooley Ch.8 Q9).</p><div class='pd-formula'><div class='pd-formula-label'>Phân loại</div><div class='pd-formula-math'>64 cổng → nằm trong khoảng 12–99 → MSI</div></div>",
    "explain": "<p>Với 64 cổng logic, con số này rơi đúng vào khoảng 12 đến 99 của MSI, không thuộc SSI (dưới 12) và cũng chưa đủ để lên LSI (từ 100 trở lên).</p><p>Đây là bài tập rèn kỹ năng tra bảng chính xác: chỉ cần nhớ đúng 3 ranh giới số (12, 100, 10.000) là có thể phân loại NGAY bất kỳ chip nào chỉ cần biết số cổng logic của nó, không cần nhớ thêm chi tiết gì khác.</p>"
   },
   {
    "title": "Ví dụ phân loại 3: vi xử lý",
    "body": "<p>Một vi xử lý hiện đại chứa từ vài triệu tới hàng tỉ transistor.</p><div class='pd-formula'><div class='pd-formula-label'>Phân loại</div><div class='pd-formula-math'>≥10.000 cổng tương đương → VLSI</div></div><p>Đây là lý do vi xử lý luôn được xếp vào VLSI, dù chức năng logic bên trong vẫn dựa trên cùng nguyên lý cổng logic cơ bản đã học.</p>",
    "explain": "<p>Vi xử lý là ví dụ cực đoan nhất của quy mô tích hợp: một CPU hiện đại có thể chứa từ vài triệu tới hàng chục tỉ transistor, vượt xa ngưỡng 10.000 cổng logic tương đương (mức thấp nhất để được xếp vào VLSI) tới hàng nghìn, thậm chí hàng triệu lần.</p><p>Điều thú vị cần ghi nhớ: dù số lượng cổng logic bên trong một CPU khổng lồ như vậy, MỖI cổng riêng lẻ vẫn hoạt động theo đúng nguyên lý AND/OR/NOT cơ bản đã học ở Module 02, không có “phép màu” nào khác: sự phức tạp chỉ đến từ số LƯỢNG cổng được kết nối với nhau, không phải từ một loại logic mới.</p>"
   },
   {
    "title": "Ví dụ so sánh: DIP và PLCC",
    "body": "<p>Cùng một mạch MSI có thể đóng gói theo DIP (Dual-In-line Package, 2 hàng chân song song) hoặc PLCC (Plastic Leaded Chip Carrier, chân bố trí quanh 4 cạnh).</p><p>PLCC cho phép nhiều chân hơn trên cùng diện tích đế: hữu ích khi mạch cần nhiều tín hiệu vào/ra nhưng không gian board hạn chế (Tooley Ch.8 Q5).</p>",
    "explain": "<p>DIP và PLCC là hai cách “đóng gói” hoàn toàn khác nhau cho cùng một mạch bên trong: DIP xếp chân theo 2 hàng song song (giống một con rết có chân hai bên), còn PLCC xếp chân đều quanh cả 4 cạnh của gói vuông.</p><p>Lý do PLCC tồn tại: khi một mạch cần rất nhiều chân vào/ra (ví dụ 44, 68 chân) nhưng diện tích board mạch lại hạn chế, xếp chân quanh 4 cạnh cho phép nhồi nhiều chân hơn trong cùng một diện tích so với chỉ xếp ở 2 cạnh như DIP, giống như một căn phòng có cửa sổ ở cả 4 bức tường sẽ đón nhiều ánh sáng hơn phòng chỉ có cửa sổ ở 2 bức tường đối diện.</p>"
   },
   {
    "title": "Bảng so sánh các kiểu đóng gói IC",
    "body": "<table class='tt'><thead><tr><th>Kiểu đóng gói</th><th>Đặc điểm</th><th>Lắp đặt</th></tr></thead><tbody><tr><td>DIL/DIP</td><td>2 hàng chân song song</td><td>Xuyên lỗ hoặc đế cắm</td></tr><tr><td>PGA</td><td>Chân dạng lưới (pin grid array)</td><td>Đế cắm (socket)</td></tr><tr><td>PLCC</td><td>Chân quanh 4 cạnh, gọn hơn DIP</td><td>Đế cắm hoặc hàn</td></tr><tr><td>SOIC</td><td>Dán bề mặt, nhỏ gọn</td><td>Luôn hàn cố định</td></tr><tr><td>QFP</td><td>Chân mật độ cao quanh 4 cạnh</td><td>Hàn bề mặt</td></tr></tbody></table>",
    "explain": "<p>Bảng này liệt kê 5 kiểu đóng gói phổ biến, mỗi kiểu có một đặc điểm hình dạng và cách lắp đặt riêng. Điều quan trọng không phải là học thuộc từng chi tiết, mà là nhận ra XU HƯỚNG chung: các kiểu đóng gói hiện đại (SOIC, QFP) đều hướng tới việc hàn cố định trực tiếp lên board (surface-mount), thay vì cắm vào đế (socket) như DIP/PGA truyền thống.</p><p>Xu hướng này phản ánh đúng nhu cầu thu nhỏ kích thước và tăng độ tin cậy của thiết bị điện tử hiện đại, điều sẽ được giải thích rõ hơn ở slide tiếp theo về ứng dụng hàng không.</p>",
    "img": "icmux_apps_p14.jpg"
   },
   {
    "title": "Ứng dụng hàng không: chọn đóng gói chịu rung động",
    "body": "<p>Thiết bị avionics phải hoạt động ổn định trong môi trường rung động mạnh và thay đổi nhiệt độ lớn. Đóng gói kiểu DIP/PGA có đế cắm (socket) tiềm ẩn rủi ro tiếp xúc lỏng do rung động theo thời gian, nên nhiều LRU hàng không ưu tiên linh kiện hàn cố định (SOIC, QFP) hoặc đế cắm có khoá cơ khí chống rung, kết hợp keo/verni bảo vệ mối hàn.</p>",
    "explain": "<p>Rung động là kẻ thù của mọi mối nối điện không chắc chắn: một chip cắm vào đế (socket) có thể, theo thời gian, bị rung lỏng dần ra khỏi vị trí tiếp xúc, gây ra hiện tượng chập chờn cực kỳ khó chẩn đoán (đôi khi hoạt động, đôi khi không, tuỳ vào việc rung động vừa làm chân tiếp xúc lại hay chưa).</p><p>Đó là lý do thiết bị avionics thường ưu tiên hàn cố định (SOIC, QFP) thay vì dùng đế cắm: mối hàn không thể “lỏng dần” theo thời gian như tiếp xúc cơ khí của đế cắm. Khi vẫn cần dùng đế cắm (để dễ thay thế linh kiện), người ta bổ sung khoá cơ khí chống rung và phủ keo/verni bảo vệ để giảm rủi ro.</p>",
    "img": "icmux_apps_p04.jpg"
   },
   {
    "title": "⚠️ Cảnh báo: đừng suy luận quy mô tích hợp chỉ từ 'tuổi đời' của chip",
    "body": "<div class='callout warn'><p>Một chip sản xuất năm 1981 nhiều khả năng là DIP/SSI-MSI, nhưng đây chỉ là suy luận theo <i>công nghệ phổ biến thời kỳ đó</i>, không phải quy luật tuyệt đối. Quy mô tích hợp được xác định bằng SỐ CỔNG LOGIC THỰC TẾ trên chip, không phải năm sản xuất.</p></div>",
    "explain": "<p>Đây là một cảnh báo quan trọng về TƯ DUY suy luận: rất dễ bị cám dỗ để nghĩ “chip cũ chắc chắn là SSI/MSI vì công nghệ hồi đó còn đơn giản”, nhưng đây chỉ là một quy luật THỐNG KÊ (đúng phần lớn trường hợp thời đó), không phải một ĐỊNH NGHĨA.</p><p>Định nghĩa CHÍNH XÁC của quy mô tích hợp chỉ dựa vào một tiêu chí duy nhất: đếm số cổng logic tương đương thực tế có trên chip. Một chip sản xuất năm 1981 vẫn có thể là VLSI nếu nó thực sự chứa trên 10.000 cổng (dù hiếm ở thời kỳ đó), và ngược lại một chip sản xuất gần đây vẫn có thể chỉ là SSI nếu chức năng của nó đơn giản (ví dụ một cổng logic rời).</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Trước khi sang phần tiếp theo, hãy tự trả lời: một IC chứa khoảng 200 cổng logic thuộc quy mô tích hợp nào? Nó có khả năng được đóng gói theo kiểu nào nếu sản xuất sau năm 2000?</p>",
    "explain": "<p>Bài tự kiểm tra áp dụng lại đúng bảng phân loại: 200 cổng logic nằm ngoài khoảng 12 đến 99 của MSI (vượt quá 99), nên phải xếp vào LSI (100 đến 9.999).</p><p>Về đóng gói, nếu sản xuất sau năm 2000, khả năng cao chip này sẽ dùng kiểu hàn bề mặt hiện đại (SOIC hoặc QFP) thay vì DIP/PGA cắm đế truyền thống, đúng xu hướng công nghệ đã học ở các slide trước, dù đây chỉ là suy luận theo xu hướng phổ biến, không phải quy luật tuyệt đối (như đã cảnh báo ở slide trước).</p>"
   }
  ],
  [
   {
    "title": "Định nghĩa fan-out",
    "body": "<p><b>Fan-out</b> là số đầu vào chuẩn (cùng họ logic) tối đa mà một đầu ra có thể điều khiển an toàn mà không làm mức logic bị lệch khỏi giới hạn cho phép.</p><div class='pd-formula'><div class='pd-formula-label'>Fan-out TTL chuẩn</div><div class='pd-formula-math'>Fan-out = 10 đầu vào TTL cùng họ</div></div>",
    "explain": "<p>Hãy tưởng tượng fan-out như “sức kéo” tối đa của một chiếc xe: nếu xe được thiết kế để kéo tối đa 10 toa hàng cùng loại, gắn thêm toa thứ 11 sẽ khiến xe không đủ sức, dẫn tới vận hành ì ạch hoặc hỏng hóc. Tương tự, một cổng logic có fan-out=10 chỉ đủ “sức” (dòng điện) để giữ đúng mức điện áp logic cho tối đa 10 đầu vào cùng họ ở tầng sau.</p><p>Điểm mấu chốt: fan-out là thuộc tính của ĐẦU RA (bên phát tín hiệu), mô tả khả năng “gánh” bao nhiêu tải, khác hẳn với fan-in ở slide sau, vốn là thuộc tính của ĐẦU VÀO.</p>"
   },
   {
    "title": "Định nghĩa fan-in",
    "body": "<p><b>Fan-in</b> là tải tương đương (tính theo số đầu vào chuẩn cùng họ logic) mà MỘT đầu vào cụ thể áp lên tầng trước nó.</p><ul class='pd-legend'><li><b>Đầu vào chuẩn</b><span>fan-in = 1</span></li><li><b>Đầu vào nối 2 cổng cùng lúc</b><span>fan-in = 2</span></li></ul>",
    "explain": "<p>Nếu fan-out là “sức kéo” của xe, thì fan-in giống như “trọng lượng” của mỗi toa hàng: một đầu vào bình thường chỉ nặng bằng đúng 1 đơn vị tải chuẩn, nhưng nếu một đường tín hiệu bị nối vào NHIỀU cổng cùng lúc (như đường B trong ví dụ), nó sẽ tạo ra tải nặng hơn tương ứng với số cổng đó.</p><p>Đây là lý do khi tính toán tải thực tế của một mạch, không thể chỉ đếm số “đường dây” mà phải đếm số “đầu vào cổng logic” thực sự được nối vào, vì một đường dây có thể rẽ nhánh tới nhiều cổng khác nhau.</p>"
   },
   {
    "title": "Ví dụ: tính fan-in của một mạch",
    "body": "<p>Cho mạch có đầu vào B nối đồng thời tới cổng G3 và G4 (mỗi cổng là thiết bị chuẩn, fan-in mỗi đầu vào = 1). Vậy tải mà B áp lên tầng trước = 1 (từ G3) + 1 (từ G4) = <b>2</b>.</p>",
    "explain": "<p>Bài tập này minh hoạ chính xác điểm đã nêu ở slide trước: dù chỉ có MỘT đường tín hiệu B duy nhất, nó rẽ nhánh vào HAI cổng khác nhau (G3 và G4), nên tải thực tế mà B phải “gánh” không phải là 1, mà là tổng của từng nhánh: 1 (từ G3) cộng 1 (từ G4) bằng 2.</p><p>Cách tính đơn giản nhưng dễ bị bỏ sót nếu chỉ nhìn thoáng qua sơ đồ mạch và đếm “một đường thì tải bằng 1”: luôn phải lần theo TỪNG nhánh rẽ của một đường tín hiệu để đếm đủ tải.</p>"
   },
   {
    "title": "Ví dụ: tính fan-out tối thiểu của một cổng",
    "body": "<p>Cổng G1 phải điều khiển 6 cổng phía sau (G2 đến G7), mỗi cổng là thiết bị chuẩn (fan-in=1 mỗi cổng). Vậy G1 cần fan-out tối thiểu là:</p><div class='pd-formula'><div class='pd-formula-label'>Fan-out tối thiểu</div><div class='pd-formula-math'>6 cổng tải × 1 (fan-in mỗi cổng) = 6</div></div>",
    "explain": "<p>Bài toán ngược lại với slide trước: thay vì tính tải áp lên MỘT đầu vào, giờ ta tính fan-out TỐI THIỂU cần có ở đầu ra của G1 để nó đủ sức nuôi toàn bộ 6 cổng phía sau.</p><p>Phép tính rất trực quan: nếu mỗi cổng tải (G2 đến G7) chỉ có fan-in tiêu chuẩn bằng 1, tổng tải cần “gánh” đơn giản là phép cộng 6 lần con số 1, ra 6. Nếu một trong các cổng tải đó lại có fan-in lớn hơn 1 (ví dụ một cổng đặc biệt cần tải gấp đôi), fan-out tối thiểu cần thiết sẽ tăng tương ứng.</p>"
   },
   {
    "title": "Điều gì xảy ra nếu vượt quá fan-out?",
    "body": "<p>Khi số tải vượt fan-out cho phép, cổng nguồn không đủ dòng để giữ mức logic 'cao' (không đủ nguồn dòng ra) hoặc mức 'thấp' (không đủ khả năng hút dòng vào), khiến điện áp thực tế trôi khỏi ngưỡng logic hợp lệ: mạch hoạt động sai hoặc không ổn định.</p>",
    "explain": "<p>Đây là hậu quả VẬT LÝ thực sự, không chỉ là một con số lý thuyết bị vi phạm: khi một cổng phải nuôi nhiều tải hơn khả năng thiết kế, nó không đủ dòng điện để “đẩy” điện áp lên đủ cao (mức logic 1) hoặc không đủ khả năng “hút” dòng điện xuống đủ thấp (mức logic 0).</p><p>Kết quả thực tế: điện áp đo được tại các tải sẽ trôi vào vùng “không xác định” (nằm giữa ngưỡng logic 0 và logic 1 hợp lệ), khiến các tầng sau đọc tín hiệu SAI một cách không nhất quán, có lúc đúng có lúc sai tuỳ điều kiện nhiệt độ/điện áp nguồn, cực kỳ khó chẩn đoán bằng mắt thường.</p>"
   },
   {
    "title": "Ví dụ số: dùng bộ đệm (buffer) khi vượt fan-out",
    "body": "<p>Một cổng TTL chuẩn (fan-out=10) cần điều khiển 25 đầu vào TTL. Vì 25 &gt; 10, cần chèn thêm bộ đệm (buffer/driver) có fan-out cao hơn (vd 30) giữa cổng nguồn và các tải, thay vì nối trực tiếp.</p>",
    "explain": "<p>Giải pháp “chèn bộ đệm” (buffer) khi vượt fan-out giống hệt việc dùng loa trợ âm khi một người nói không đủ to cho cả một hội trường lớn nghe: bộ đệm không “tạo ra” tín hiệu mới, nó chỉ khuếch đại đủ dòng điện để tín hiệu gốc có thể nuôi được nhiều tải hơn.</p><p>Với 25 tải cần điều khiển nhưng cổng gốc chỉ có fan-out 10, phải chèn một bộ đệm có fan-out đủ lớn (ví dụ 30) vào giữa, để bộ đệm mới là bên thực sự “gánh” toàn bộ 25 tải, còn cổng gốc chỉ cần nuôi đúng 1 tải là bộ đệm đó.</p>"
   },
   {
    "title": "Bảng fan-out danh định theo họ logic",
    "body": "<table class='tt'><thead><tr><th>Họ logic</th><th>Fan-out danh định (cùng họ)</th></tr></thead><tbody><tr><td>TTL chuẩn</td><td>10</td></tr><tr><td>TTL Schottky công suất thấp (LS)</td><td>20</td></tr><tr><td>CMOS chuẩn</td><td>~50 (do trở kháng vào rất cao)</td></tr></tbody></table>",
    "explain": "<p>Bảng này cho thấy một điểm rất thú vị: CMOS có fan-out danh định cao hơn hẳn TTL (khoảng 50 so với 10), nhưng lý do hoàn toàn khác với lý do TTL bị giới hạn.</p><p>TTL giới hạn fan-out vì DÒNG ĐIỆN mỗi tải rút ra khá lớn. CMOS có trở kháng đầu vào cực cao (gần như không rút dòng ở trạng thái tĩnh), nên về lý thuyết có thể nuôi rất nhiều tải mà không gặp vấn đề dòng điện: con số fan-out của CMOS thường bị giới hạn bởi yếu tố khác (tốc độ, như sẽ học ở Phần 5) chứ không phải dòng điện như TTL.</p>"
   },
   {
    "title": "Ứng dụng hàng không: phân phối tín hiệu clock",
    "body": "<p>Trong máy tính buồng lái, một xung clock từ dao động thạch anh trung tâm thường cần cấp cho nhiều mạch con (bộ đếm thời gian, bộ mã hoá dữ liệu, bộ hiển thị). Kỹ sư thiết kế phải tính tổng fan-in của toàn bộ mạch nhận clock để chọn đúng bộ đệm phân phối clock (clock buffer/driver) đủ fan-out, tránh suy hao tín hiệu định thời quan trọng.</p>",
    "explain": "<p>Ứng dụng phân phối xung clock cho thấy fan-out không chỉ là lý thuyết sách vở: một xung clock trung tâm thường phải “nuôi” rất nhiều mạch con khác nhau trong cùng hệ thống buồng lái (bộ đếm, bộ mã hoá, bộ hiển thị), mỗi mạch con lại có fan-in riêng.</p><p>Kỹ sư phải CỘNG DỒN tổng fan-in của TOÀN BỘ mạch nhận clock (tương tự bài tập fan-in đã học), rồi chọn đúng bộ đệm phân phối clock (clock driver) có fan-out đủ lớn hơn tổng đó. Nếu tính thiếu, xung clock bị suy hao có thể khiến các mạch con nhận thời điểm đồng bộ SAI LỆCH, gây lỗi nghiêm trọng trong hệ thống thời gian thực.</p>"
   },
   {
    "title": "⚠️ Cảnh báo: fan-out không cộng dồn qua nhiều họ logic khác nhau",
    "body": "<div class='callout warn'><p>Fan-out danh định (vd 10 của TTL) chỉ đúng khi tải là đầu vào CÙNG HỌ logic. Khi trộn TTL với CMOS, phải quy đổi tải theo bảng tương thích giữa 2 họ (input loading khác nhau), không được cộng trực tiếp số lượng đầu vào như cùng họ.</p></div>",
    "explain": "<p>Đây là một cạm bẫy rất thực tế: con số fan-out=10 của TTL chỉ đúng khi TẤT CẢ tải đều là đầu vào TTL, vì con số này được tính dựa trên đặc tính dòng điện riêng của họ TTL.</p><p>Khi trộn TTL với CMOS, không thể áp dụng công thức cộng đơn giản như cùng họ, vì CMOS có đặc tính dòng điện đầu vào hoàn toàn khác (gần như không rút dòng). Phải tra bảng “input loading” chính thức của nhà sản xuất để biết chính xác một đầu vào CMOS tương đương bao nhiêu “đơn vị tải TTL chuẩn”, rồi mới cộng dồn đúng cách.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Một cổng CMOS có fan-out 50 cần điều khiển 12 đầu vào CMOS chuẩn: có an toàn không? Nếu 3 trong số đó là đầu vào TTL (không phải CMOS), bạn cần kiểm tra thêm điều gì trước khi kết luận?</p>",
    "explain": "<p>Với 12 đầu vào CMOS chuẩn và fan-out 50, phép tính rất đơn giản: 12 nhỏ hơn nhiều so với 50, nên hoàn toàn an toàn nếu TẤT CẢ tải đều là CMOS.</p><p>Nhưng câu hỏi phụ (3 trong số đó là TTL) chính là cái bẫy: một khi trộn lẫn họ logic, không thể áp dụng trực tiếp con số fan-out=50 (vốn tính riêng cho tải CMOS) cho cả 3 tải TTL kia. Phải tra bảng quy đổi tải giữa hai họ (như cảnh báo ở slide trước) trước khi kết luận có an toàn hay không, không được giả định đơn giản là “12 nhỏ hơn 50 nên chắc chắn ổn”.</p>"
   }
  ],
  [
   {
    "title": "Định nghĩa bộ giải mã (decoder)",
    "body": "<p>Bộ giải mã nhận n đường địa chỉ nhị phân và kích hoạt ĐÚNG MỘT trong 2ⁿ đường ra tương ứng với tổ hợp địa chỉ đó: dùng để chọn 1 thiết bị/vị trí nhớ trong nhiều lựa chọn.</p>",
    "explain": "<p>Hãy hình dung bộ giải mã như một nhân viên tổng đài chuyển tiếp cuộc gọi: khách gọi tới cung cấp một “số máy lẻ” (địa chỉ nhị phân n bit), và nhân viên chỉ nối đúng MỘT đường dây duy nhất (trong 2ⁿ đường có thể) tương ứng với số máy lẻ đó, mọi đường khác đều để im.</p><p>Công thức 2ⁿ chính là số lượng “đường dây” tối đa có thể phân biệt được bằng n bit địa chỉ, đúng nguyên lý đã học ở Module 01 khi đếm số tổ hợp nhị phân. Với n=2 bit địa chỉ, có đúng 2²=4 đường ra có thể, khớp với ví dụ decoder 2-sang-4 ở slide sau.</p>"
   },
   {
    "title": "Định nghĩa bộ mã hoá (encoder)",
    "body": "<p>Bộ mã hoá thực hiện chức năng NGƯỢC LẠI: nhận tín hiệu tích cực trên 1 trong N đường vào, xuất ra mã nhị phân tương ứng trên log₂(N) đường ra.</p>",
    "explain": "<p>Bộ mã hoá làm công việc NGƯỢC LẠI hoàn toàn với bộ giải mã: thay vì nhận địa chỉ để chọn 1 đường, nó nhận tín hiệu tích cực trên MỘT trong N đường vào, rồi “báo cáo lại” đúng địa chỉ nhị phân của đường đó bằng log₂(N) bit đầu ra.</p><p>Đây là quan hệ đối xứng rất đẹp trong thiết kế số: encoder và decoder là hai mặt của cùng một đồng xu, một cái đi từ địa chỉ ra tín hiệu chọn, cái kia đi từ tín hiệu chọn ngược lại ra địa chỉ, và công thức 2ⁿ↔log₂(N) áp dụng cho cả hai chiều.</p>"
   },
   {
    "title": "Ví dụ: thiết kế bảng chân trị decoder 2-sang-4",
    "body": "<table class='tt'><thead><tr><th>A1</th><th>A0</th><th>Y0</th><th>Y1</th><th>Y2</th><th>Y3</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr></tbody></table><p>Ở mỗi hàng, đúng một ngõ ra bằng 1, có chỉ số bằng giá trị nhị phân của A1A0.</p>",
    "explain": "<p>Bảng chân trị này thể hiện đúng nguyên lý “một địa chỉ, một đường ra tích cực” đã nêu ở slide đầu: với địa chỉ A1A0=00 (tức số 0 ở hệ nhị phân), chỉ có Y0 bật lên 1, ba đường Y1/Y2/Y3 còn lại đều là 0.</p><p>Điều đáng chú ý: chỉ số của đường ra tích cực LUÔN khớp đúng với giá trị nhị phân của địa chỉ đầu vào (địa chỉ 00→Y0, địa chỉ 01→Y1, địa chỉ 10→Y2, địa chỉ 11→Y3). Đây không phải sự trùng hợp, mà là chính định nghĩa của bộ giải mã nhị phân chuẩn.</p>",
    "img": "icmux_apps_p41.jpg"
   },
   {
    "title": "Ví dụ: bộ mã hoá ưu tiên 4-sang-2",
    "body": "<p>Nếu nhiều đầu vào cùng tích cực, bộ mã hoá ƯU TIÊN chọn đầu vào có chỉ số CAO NHẤT để mã hoá. Vd đầu vào I1 và I3 cùng tích cực → mã hoá theo I3 (ưu tiên cao hơn) → ngõ ra = 11 (nhị phân của 3), bỏ qua I1.</p>",
    "explain": "<p>Bộ mã hoá ưu tiên giải quyết một tình huống thực tế mà bộ mã hoá thường (không ưu tiên) không xử lý được: nếu HAI đầu vào cùng tích cực một lúc, bộ mã hoá thường sẽ cho ra kết quả sai hoặc không xác định, vì nó không được thiết kế để “chọn” giữa hai tín hiệu.</p><p>Bộ mã hoá ưu tiên giải quyết bằng một quy tắc đơn giản: LUÔN chọn đầu vào có chỉ số cao nhất trong số các đầu vào đang tích cực, bỏ qua hoàn toàn các đầu vào có chỉ số thấp hơn. Với I1 và I3 cùng tích cực, hệ thống hoàn toàn phớt lờ I1 và chỉ mã hoá theo I3, giống hệt quy tắc phân xử ưu tiên trong hàng đợi khẩn cấp: người có mức ưu tiên cao nhất luôn được xử lý trước.</p>",
    "img": "icmux_apps_p50.jpg"
   },
   {
    "title": "Ví dụ: chuyển đổi mã BCD sang 7 đoạn",
    "body": "<p>Bộ chuyển đổi mã (code converter) BCD-sang-7-đoạn nhận 4 bit BCD (0000-1001) và xuất ra 7 tín hiệu điều khiển từng đoạn (a-g) của LED 7 đoạn để hiển thị đúng chữ số thập phân tương ứng: nguyên lý dùng trong hiển thị số trên nhiều thiết bị đo lường buồng lái.</p>",
    "explain": "<p>Bộ chuyển đổi mã BCD-sang-7-đoạn là một ví dụ đặc biệt của “bộ giải mã”: thay vì có ĐÚNG MỘT đường ra tích cực như decoder thông thường, nó có 7 đường ra (a đến g), và với mỗi mã BCD đầu vào, một TỔ HỢP các đường ra cụ thể được bật lên để tạo hình đúng chữ số cần hiển thị.</p><p>Ví dụ, để hiển thị chữ số “0”, cần bật các đoạn a,b,c,d,e,f (tất cả trừ đoạn g ở giữa); để hiển thị “1”, chỉ cần bật đúng 2 đoạn b,c (hai đoạn bên phải). Mỗi chữ số 0-9 có một “khuôn mẫu” bật/tắt 7 đoạn riêng, được mạch giải mã tính sẵn theo đúng mã BCD nhận vào.</p>"
   },
   {
    "title": "Ví dụ: chân enable dùng để ghép tầng",
    "body": "<p>Một IC decoder 3-sang-8 có thêm 1 chân Enable. Khi Enable=0, TOÀN BỘ ngõ ra bị khoá về mức không tích cực bất kể địa chỉ vào là gì. Ghép 2 IC decoder 3-sang-8 qua chân Enable cho phép mở rộng thành 1 decoder 4-sang-16 (dùng bit địa chỉ thứ 4 để chọn IC nào được Enable).</p>",
    "explain": "<p>Chân Enable biến một IC decoder đơn lẻ thành một “khối xây dựng” (building block) có thể ghép lại thành hệ thống lớn hơn: khi Enable=0, TOÀN BỘ ngõ ra bị khoá về mức không tích cực, bất kể địa chỉ đưa vào là gì, giống như tắt hẳn nguồn điện của cả khối decoder đó.</p><p>Kỹ thuật ghép tầng: dùng bit địa chỉ thứ 4 (bit cao nhất) để quyết định BẬT Enable của IC decoder nào trong 2 IC (mỗi IC xử lý 8 địa chỉ với 3 bit thấp), còn 3 bit thấp dùng chung cho cả hai IC để chọn đúng đường ra trong 8 đường của IC đang được Enable. Kết quả: 2 IC 3-sang-8 ghép lại thành đúng 1 hệ thống 4-sang-16, không cần thiết kế IC mới từ đầu.</p>"
   },
   {
    "title": "Bảng so sánh 4 mạch MSI cơ bản",
    "body": "<table class='tt'><thead><tr><th>Mạch</th><th>Chiều xử lý</th><th>Ứng dụng chính</th></tr></thead><tbody><tr><td>Decoder</td><td>n vào → 2ⁿ ra (đúng 1 ra tích cực)</td><td>Giải mã địa chỉ bộ nhớ</td></tr><tr><td>Encoder</td><td>N vào → log₂N ra</td><td>Mã hoá bàn phím</td></tr><tr><td>Multiplexer</td><td>N kênh dữ liệu → 1 ra</td><td>Chọn 1 trong nhiều nguồn tín hiệu</td></tr><tr><td>Demultiplexer</td><td>1 vào → N kênh ra</td><td>Phân phối tín hiệu tới nhiều đích</td></tr></tbody></table>",
    "explain": "<p>Bảng này tổng hợp lại 4 mạch MSI theo đúng một tiêu chí duy nhất: hướng xử lý dữ liệu đi như thế nào. Decoder và encoder đối xứng nhau (n↔2ⁿ theo hai chiều ngược nhau), còn multiplexer và demultiplexer cũng đối xứng nhau (N kênh↔1 kênh theo hai chiều ngược nhau).</p><p>Ghi nhớ theo cặp đối xứng này (decoder-encoder, mux-demux) dễ hơn nhiều so với học thuộc 4 định nghĩa rời rạc: mỗi cặp chỉ là “đảo chiều” của nhau, và một khi hiểu rõ MỘT mạch trong cặp, mạch còn lại chỉ cần đảo ngược tư duy là hiểu được ngay.</p>"
   },
   {
    "title": "Ứng dụng hàng không: giải mã địa chỉ bộ nhớ trong máy tính buồng lái",
    "body": "<p>Trong máy tính buồng lái (Tooley Figure 6.11), CPU cần chọn đúng vùng ROM/RAM để đọc/ghi. Một mạch giải mã địa chỉ (address decoder) nhận các bit cao của address bus và kích hoạt đúng chân Chip-Select (CS) của ROM hoặc RAM tương ứng, tránh 2 thiết bị nhớ cùng tranh chấp bus dữ liệu.</p>",
    "explain": "<p>Địa chỉ bộ nhớ trong máy tính buồng lái hoạt động đúng theo nguyên lý decoder đã học: CPU đưa ra một địa chỉ nhị phân trên address bus, và mạch giải mã địa chỉ có nhiệm vụ “phiên dịch” địa chỉ đó thành TÍN HIỆU CHỌN đúng một chip nhớ (ROM hoặc RAM) cụ thể thông qua chân Chip-Select (CS) của chip đó.</p><p>Vai trò an toàn cực kỳ quan trọng của mạch này: nếu 2 chip nhớ CÙNG LÚC được kích hoạt CS (do mạch giải mã lỗi hoặc thiết kế sai), cả hai sẽ cùng lúc cố gắng đưa dữ liệu ra chung một đường data bus, gây xung đột điện y hệt vấn đề “bus contention” đã học ở Module 02 khi nói về tri-state.</p>",
    "img": "icmux_apps_p20.jpg"
   },
   {
    "title": "⚠️ Cảnh báo: đừng nhầm decoder 'không có input dữ liệu' với demultiplexer",
    "body": "<div class='callout warn'><p>Về mặt vật lý, decoder và demultiplexer có thể dùng CHUNG một IC (gán thêm 1 chân làm 'dữ liệu' thay vì luôn giữ mức tích cực cố định). Nhưng về MỤC ĐÍCH chức năng: decoder dùng để CHỌN đường theo địa chỉ, demux dùng để PHÂN PHỐI 1 luồng dữ liệu tới nhiều đích: đừng đánh đồng 2 khái niệm chỉ vì cùng linh kiện vật lý.</p></div>",
    "explain": "<p>Đây là điểm rất tinh tế dễ gây nhầm lẫn: về mặt VẬT LÝ, một IC decoder và một IC demultiplexer có thể là CÙNG một con chip, chỉ khác cách người thiết kế “gán vai trò” cho các chân của nó (một chân luôn giữ mức cố định để làm “dữ liệu” giả, biến decoder thành demux).</p><p>Nhưng về mặt MỤC ĐÍCH sử dụng, hai khái niệm này hoàn toàn khác nhau: decoder dùng để CHỌN một đường dựa theo địa chỉ (mục đích chọn lựa), còn demultiplexer dùng để PHÂN PHỐI một luồng dữ liệu thực sự tới nhiều đích khác nhau (mục đích truyền dữ liệu). Đừng đánh đồng hai khái niệm chỉ vì chúng có thể dùng chung một linh kiện vật lý.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Một bộ mã hoá ưu tiên 8-sang-3 nhận tín hiệu tích cực đồng thời ở đầu vào 2, 4 và 6. Ngõ ra mã hoá sẽ ứng với đầu vào nào? Vì sao?</p>",
    "explain": "<p>Bài tự luyện áp dụng đúng quy tắc “chọn chỉ số cao nhất” của bộ mã hoá ưu tiên đã học: với ba đầu vào 2, 4, 6 cùng tích cực đồng thời, bộ mã hoá ưu tiên sẽ hoàn toàn bỏ qua đầu vào 2 và 4, chỉ mã hoá theo đầu vào có chỉ số CAO NHẤT trong ba số đó, tức đầu vào 6.</p><p>Lý do bộ mã hoá ưu tiên làm vậy: trong nhiều ứng dụng thực tế (ví dụ xử lý ngắt trong CPU), tín hiệu có chỉ số cao thường đại diện cho sự kiện quan trọng/khẩn cấp hơn, nên quy tắc “luôn ưu tiên chỉ số cao nhất” đảm bảo sự kiện quan trọng nhất luôn được xử lý trước, bất kể có bao nhiêu sự kiện khác đang chờ đồng thời.</p>"
   }
  ],
  [
   {
    "title": "Định nghĩa multiplexer",
    "body": "<p>Multiplexer (bộ dồn kênh/data selector) chọn 1 trong N kênh dữ liệu đầu vào để đưa ra 1 ngõ ra duy nhất, dựa theo tổ hợp nhị phân trên các đường chọn (select lines).</p><div class='pd-formula'><div class='pd-formula-label'>Số đường chọn cần thiết</div><div class='pd-formula-math'>n = log₂(N)</div></div>",
    "explain": "<p>Hãy hình dung multiplexer như một nhân viên gác cổng một sân bay nhỏ với N đường băng nhưng chỉ có MỘT đường lăn ra khỏi sân bay: tại một thời điểm, nhân viên chỉ cho phép ĐÚNG MỘT máy bay từ một đường băng cụ thể (do “phiếu chọn” quyết định) đi ra đường lăn chung, các máy bay ở đường băng khác phải chờ.</p><p>Công thức n=log₂(N) cho biết cần bao nhiêu bit trên “phiếu chọn” (đường chọn/select lines) để phân biệt đủ N đường băng khác nhau: đây chính là công thức ngược của 2ⁿ đã học ở decoder, vì bản chất việc “chọn 1 trong N kênh” cũng là một dạng giải mã địa chỉ.</p>"
   },
   {
    "title": "Ví dụ: bảng chân trị mux 4-sang-1",
    "body": "<table class='tt'><thead><tr><th>S1</th><th>S0</th><th>Ngõ ra Y</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>D0</td></tr><tr><td>0</td><td>1</td><td>D1</td></tr><tr><td>1</td><td>0</td><td>D2</td></tr><tr><td>1</td><td>1</td><td>D3</td></tr></tbody></table>",
    "explain": "<p>Bảng chân trị mux 4-sang-1 đọc rất trực quan: tổ hợp 2 bit trên đường chọn (S1S0) đóng vai trò như một “địa chỉ”, và giá trị đó xác định CHÍNH XÁC kênh dữ liệu nào (D0 đến D3) được nối thông ra ngõ Y.</p><p>Quan sát thú vị: đây chính xác là bảng chân trị của một decoder 2-sang-4 đã học ở Phần 3, chỉ khác cách diễn giải: thay vì “bật đường ra tương ứng”, ta diễn giải là “cho kênh dữ liệu tương ứng đi qua”. Hai khái niệm mux và decoder có mối liên hệ mật thiết về mặt cấu trúc mạch bên trong.</p>",
    "img": "icmux_apps_p52.jpg"
   },
   {
    "title": "Ví dụ tính: số đường chọn cho 16 kênh và 32 kênh",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Áp dụng công thức n=log₂(N)</div><div class='pd-formula-math'>N=16 → n=4 &nbsp;&nbsp;|&nbsp;&nbsp; N=32 → n=5</div></div><p>Số đường chọn tăng chậm hơn nhiều so với số kênh dữ liệu: đây chính là lý do multiplexer giúp tiết kiệm dây dẫn so với truyền song song trực tiếp.</p>",
    "explain": "<p>Công thức n=log₂(N) cho thấy một tính chất rất có lợi: số đường chọn tăng RẤT CHẬM so với số kênh dữ liệu. Từ 16 kênh lên 32 kênh (tăng gấp đôi số kênh), số đường chọn chỉ tăng thêm đúng 1 (từ 4 lên 5), không phải tăng gấp đôi.</p><p>Đây chính là lý do cốt lõi khiến multiplexer trở thành công cụ tiết kiệm dây dẫn cực kỳ hiệu quả: nếu không dùng mux mà truyền song song trực tiếp, 32 kênh cần tới 32 đường dây riêng biệt; dùng mux, chỉ cần 5 đường chọn cộng 1 đường dữ liệu ra chung, tổng cộng 6 đường thay vì 32.</p>"
   },
   {
    "title": "Ví dụ: ghép tầng 2 IC mux 4-sang-1 thành mux 8-sang-1",
    "body": "<p>Dùng 2 IC mux 4-sang-1 xử lý 2 nhóm 4 kênh, rồi dùng thêm 1 mux 2-sang-1 để chọn kết quả từ 2 IC đó: tổng cộng cần 3 đường chọn (2 đường chọn nội bộ dùng chung cho cả 2 IC + 1 đường chọn nhóm), đúng khớp n=log₂(8)=3.</p>",
    "explain": "<p>Ghép tầng 2 IC mux 4-sang-1 để tạo thành mux 8-sang-1 là một kỹ thuật xây dựng “khối lớn từ khối nhỏ” rất phổ biến trong thiết kế số: thay vì phải tìm mua hoặc thiết kế riêng một IC mux 8-sang-1 chuyên dụng, ta ghép 2 IC mux 4-sang-1 sẵn có, cộng thêm 1 mux 2-sang-1 nhỏ ở tầng sau để “chọn” giữa kết quả của 2 IC đầu.</p><p>Số đường chọn tổng cộng khớp chính xác với công thức đã học: 2 đường chọn dùng chung cho cả hai IC 4-sang-1 (chọn kênh trong nhóm 4), cộng thêm 1 đường chọn nhóm (chọn IC nào), tổng 3 đường, đúng bằng log₂(8)=3. Đây là minh chứng cụ thể cho thấy công thức lý thuyết áp dụng đúng cả khi ghép nhiều IC lại với nhau.</p>"
   },
   {
    "title": "Định nghĩa demultiplexer",
    "body": "<p>Demultiplexer thực hiện chức năng ngược: nhận 1 luồng dữ liệu đầu vào và phân phối tới đúng 1 trong N ngõ ra, theo địa chỉ trên các đường chọn: thường dùng chung IC vật lý với decoder.</p>",
    "explain": "<p>Demultiplexer là “gương soi ngược” của multiplexer: thay vì gộp N nguồn thành 1 đường chung, nó lấy MỘT luồng dữ liệu duy nhất và “rải” nó ra đúng 1 trong N đích, theo đúng địa chỉ trên đường chọn.</p><p>Điểm kỹ thuật thú vị: về mặt mạch điện, demultiplexer thường dùng CHUNG cấu trúc vật lý với decoder (chỉ khác vai trò gán cho một chân), đúng như đã lưu ý ở Phần 3: một IC có thể “đóng vai” decoder hoặc demultiplexer tuỳ vào cách kỹ sư sử dụng chân dữ liệu của nó.</p>",
    "img": "icmux_apps_p58.jpg"
   },
   {
    "title": "Ví dụ thực tế: mux dữ liệu độ cao trên A320 (Tooley Figure 9.21)",
    "body": "<p>Bộ dồn kênh kép 4 kênh chọn 1 trong 4 nguồn dữ liệu độ cao (độ cao đã chọn, độ cao thực tế từ ADC trái/phải) để đưa vào bộ mã hoá dữ liệu nối tiếp ARINC 429, chỉ cần 2 đường chọn nhị phân thay vì 4 đường truyền vật lý riêng biệt.</p>",
    "explain": "<p>Ví dụ dồn kênh dữ liệu độ cao trên A320 cho thấy multiplexer giải quyết đúng vấn đề thực tế: thay vì phải có 4 đường truyền vật lý riêng biệt cho 4 nguồn dữ liệu độ cao khác nhau (mỗi nguồn cần một bộ mã hoá ARINC 429 riêng, tốn kém và phức tạp), hệ thống chỉ cần MỘT bộ mã hoá dùng chung, với multiplexer đứng trước để lần lượt chọn nguồn nào được mã hoá tại mỗi thời điểm.</p><p>Chỉ cần 2 đường chọn nhị phân (đủ phân biệt 4 nguồn theo công thức n=log₂(4)=2) là đủ điều khiển toàn bộ quá trình chọn nguồn, tiết kiệm đáng kể phần cứng so với việc nhân bản bộ mã hoá cho từng nguồn riêng.</p>"
   },
   {
    "title": "Bảng: số kênh, số đường chọn, và số dây tiết kiệm được",
    "body": "<table class='tt'><thead><tr><th>Số kênh N</th><th>Đường chọn n</th><th>Không dùng mux (N dây)</th></tr></thead><tbody><tr><td>4</td><td>2</td><td>4</td></tr><tr><td>8</td><td>3</td><td>8</td></tr><tr><td>16</td><td>4</td><td>16</td></tr></tbody></table><p>Với mux, chỉ cần n đường chọn + 1 đường dữ liệu ra chung, thay vì N đường dữ liệu song song.</p>",
    "explain": "<p>Bảng này làm nổi bật rõ lợi ích tiết kiệm dây dẫn của multiplexer bằng con số cụ thể: với 16 kênh, nếu không dùng mux cần tới 16 đường dây riêng biệt chạy song song, còn dùng mux chỉ cần 4 đường chọn cộng 1 đường dữ liệu chung, tổng 5 đường.</p><p>Khoảng cách tiết kiệm càng lớn khi số kênh càng nhiều: đây là lý do multiplexer gần như luôn được dùng bất cứ khi nào cần truyền dữ liệu từ nhiều nguồn qua một khoảng cách xa hoặc qua một không gian dây dẫn hạn chế (như bên trong thân máy bay), thay vì kéo hàng chục đường dây riêng biệt.</p>"
   },
   {
    "title": "Ứng dụng hàng không: chia sẻ 1 bus hiển thị cho nhiều tham số",
    "body": "<p>Màn hình ECAM cần luân phiên hiển thị nhiều tham số động cơ (N1, EGT, N2, dầu bôi trơn...). Một mux tốc độ cao có thể chọn lần lượt từng nguồn tín hiệu để đưa vào bộ xử lý hiển thị chung, giảm số kênh xử lý tín hiệu độc lập cần thiết.</p>",
    "explain": "<p>Màn hình ECAM cần hiển thị luân phiên rất nhiều tham số động cơ khác nhau (N1, EGT, N2, dầu bôi trơn...), nhưng bộ xử lý hiển thị phía sau màn hình không cần và không nên có một kênh xử lý tín hiệu riêng biệt cho MỖI tham số.</p><p>Giải pháp dùng multiplexer tốc độ cao: lần lượt “quét” qua từng nguồn tín hiệu tham số, đưa mỗi nguồn vào đúng một kênh xử lý DUY NHẤT tại từng thời điểm, giống hệt cách mắt người quét nhanh qua nhiều dòng chữ để đọc cả trang mà không cần nhìn tất cả các dòng cùng lúc. Kỹ thuật này giảm đáng kể số lượng mạch xử lý tín hiệu độc lập cần thiết trong hệ thống.</p>"
   },
   {
    "title": "⚠️ Cảnh báo: đường chọn không đủ sẽ làm mất dữ liệu, không phải lỗi ngẫu nhiên",
    "body": "<div class='callout warn'><p>Nếu thiết kế mux 8 kênh nhưng chỉ dùng 2 đường chọn (chỉ phân biệt được 4 tổ hợp), 4 kênh còn lại sẽ KHÔNG BAO GIỜ được chọn tới: đây là lỗi thiết kế có thể dự đoán trước bằng công thức n=log₂(N), không phải lỗi ngẫu nhiên cần dò tìm bằng thực nghiệm.</p></div>",
    "explain": "<p>Đây là một lỗi thiết kế có thể TIÊN LƯỢNG TRƯỚC bằng toán học, không phải một lỗi ngẫu nhiên cần dò tìm bằng thực nghiệm: nếu một mux cần chọn giữa 8 kênh nhưng chỉ dùng 2 đường chọn (chỉ tạo được 2²=4 tổ hợp địa chỉ khác nhau), thì CHẮC CHẮN có 4 kênh còn lại (kênh 4 đến 7) sẽ không bao giờ được chọn tới, bất kể đường chọn được set giá trị gì.</p><p>Trước khi lắp ráp mạch thực tế, luôn áp dụng công thức n=log₂(N) để tính TRƯỚC số đường chọn cần thiết: với 8 kênh cần đúng 3 đường chọn (2³=8), không phải 2. Đây là cách phát hiện lỗi thiết kế ngay trên giấy, tiết kiệm rất nhiều thời gian debug phần cứng sau này.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh",
    "body": "<p>Bạn cần chọn 1 trong 6 cảm biến nhiệt độ để đưa vào 1 bộ xử lý duy nhất. Cần tối thiểu bao nhiêu đường chọn? Có kênh nào bị 'thừa' không sử dụng đến trong không gian địa chỉ tạo ra không?</p>",
    "explain": "<p>Bài tự luyện áp dụng công thức n=log₂(N) cho trường hợp N=6 (không phải luỹ thừa của 2 chẵn): vì 2²=4 chưa đủ (nhỏ hơn 6) và 2³=8 đã đủ (lớn hơn hoặc bằng 6), cần tối thiểu 3 đường chọn.</p><p>Điều thú vị của trường hợp này: với 3 đường chọn tạo ra 2³=8 tổ hợp địa chỉ có thể, nhưng chỉ có 6 cảm biến thực tế cần chọn, nghĩa là CÓ 2 tổ hợp địa chỉ “thừa” (ví dụ ứng với địa chỉ 110 và 111) không nối tới cảm biến nào cả. Đây là hiện tượng bình thường và không tránh khỏi mỗi khi số kênh thực tế không phải là luỹ thừa chẵn của 2, không phải là lỗi thiết kế.</p>"
   }
  ],
  [
   {
    "title": "Tổng quan: MSI logic trong avionics dùng ở đâu?",
    "body": "<p>Theo Tooley, MSI logic trong máy bay tập trung ở 5 nhóm ứng dụng chính: giải mã địa chỉ, mã hoá ưu tiên, dồn kênh dữ liệu, chuyển đổi mã BCD-sang-7-đoạn, và kiểm tra chẵn lẻ (parity) trên đường truyền dữ liệu.</p>",
    "explain": "<p>Slide này liệt kê đúng 5 “vai trò nghề nghiệp” mà mạch MSI đảm nhận trong một chiếc máy bay thực tế, và điều thú vị là cả 5 vai trò này đều đã được học chi tiết ở các phần trước: giải mã địa chỉ (Phần 3), mã hoá ưu tiên (Phần 3), dồn kênh dữ liệu (Phần 4), chuyển đổi mã BCD-sang-7-đoạn (Phần 3), và kiểm tra chẵn lẻ (mới, sẽ học ở slide sau).</p><p>Hãy dùng slide này như một “mục lục tổng kết”: nếu còn mơ hồ về vai trò nào, đây là lúc quay lại đúng phần tương ứng trước khi tiếp tục xem các ví dụ thực tế phía sau.</p>"
   },
   {
    "title": "Ví dụ lại: bộ dồn kênh ARINC 429 (Figure 9.21)",
    "body": "<p>4 nguồn dữ liệu độ cao được dồn kênh trước khi đưa vào bộ mã hoá dữ liệu nối tiếp ARINC 429 : đây là ví dụ trực tiếp lấy từ sách, minh hoạ multiplexer trong hệ thống altimeter thực tế.</p>",
    "explain": "<p>Đây không phải một ví dụ mới, mà là việc NHẮC LẠI có chủ đích ví dụ multiplexer dữ liệu độ cao đã học ở Phần 4, để nhấn mạnh rằng đây là một ứng dụng THẬT được trích trực tiếp từ sách giáo trình (Tooley Figure 9.21), không phải một tình huống giả định.</p><p>Việc gặp lại cùng một ví dụ ở hai phần khác nhau (một lần tập trung vào NGUYÊN LÝ multiplexer, một lần tập trung vào VAI TRÒ trong hệ thống altimeter) giúp củng cố hiểu biết theo hai góc nhìn bổ sung cho nhau.</p>"
   },
   {
    "title": "Ví dụ: parity checker trên bus dữ liệu",
    "body": "<p>Mạch tạo/kiểm tra chẵn lẻ (built chủ yếu từ chuỗi cổng XOR) thêm 1 bit parity vào dữ liệu truyền trên bus. Bên nhận tính lại parity và so sánh: nếu khác, phát hiện có lỗi truyền dữ liệu (dù không xác định được lỗi ở bit nào).</p>",
    "explain": "<p>Mạch kiểm tra chẵn lẻ (parity) là một ứng dụng đơn giản nhưng cực kỳ hiệu quả của cổng XOR đã học ở Module 02: XOR vốn chỉ ra 1 khi số lượng đầu vào bằng 1 là LẺ, nên chuỗi nhiều cổng XOR nối tiếp có thể tính ra “tổng số bit 1 trong dữ liệu là chẵn hay lẻ” chỉ bằng phép toán logic thuần tuý, không cần bộ đếm phức tạp.</p><p>Nguyên lý phát hiện lỗi: bên gửi tính sẵn bit parity sao cho tổng số bit 1 (kể cả bit parity) luôn là số chẵn (hoặc luôn lẻ, tuỳ quy ước). Bên nhận tính lại và so sánh: nếu kết quả khác với parity đã gửi, chắc chắn có lỗi xảy ra trong quá trình truyền, dù không biết chính xác lỗi ở bit nào.</p>"
   },
   {
    "title": "Ví dụ tính: parity chẵn (even parity) của 1 byte dữ liệu",
    "body": "<p>Byte dữ liệu <code>10110010</code> có 4 bit 1 → số chẵn.</p><div class='pd-formula'><div class='pd-formula-label'>Bit parity chẵn cần thêm</div><div class='pd-formula-math'>0 (giữ tổng số bit 1 là số chẵn)</div></div>",
    "explain": "<p>Đây là bài tập áp dụng cụ thể nguyên lý parity chẵn: đếm số bit 1 trong byte 10110010, ta được đúng 4 bit 1 (ở các vị trí có giá trị 1), một số CHẴN.</p><p>Vì mục tiêu của parity chẵn là giữ TỔNG số bit 1 (kể cả bit parity thêm vào) luôn là số chẵn, và hiện tại đã có sẵn 4 (chẵn), bit parity cần thêm vào phải là 0 để không làm thay đổi tính chẵn của tổng. Nếu byte gốc có số bit 1 là lẻ, bit parity thêm vào phải là 1 để “kéo” tổng về chẵn.</p>"
   },
   {
    "title": "Ví dụ: giải mã địa chỉ trong hệ thống backplane bus",
    "body": "<p>Trong hệ thống nhiều board cắm chung 1 backplane bus (vd VMEbus), mỗi board có 1 mã địa chỉ cố định. Mạch giải mã trên mỗi board so sánh địa chỉ trên bus với mã của chính nó: chỉ board khớp địa chỉ mới đáp ứng, tránh xung đột dữ liệu.</p>",
    "explain": "<p>Trong một hệ thống nhiều board mạch cùng cắm chung một backplane bus (đường bus vật lý chạy xuyên suốt khung máy), mỗi board cần “nhận diện” được khi nào dữ liệu trên bus là dành cho chính nó, không phải cho board khác.</p><p>Giải pháp: mỗi board được gán một mã địa chỉ cố định, và có sẵn một mạch giải mã địa chỉ (decoder, đúng nguyên lý đã học ở Phần 3) liên tục so sánh địa chỉ đang xuất hiện trên bus với mã địa chỉ riêng của board đó. Chỉ khi hai địa chỉ khớp nhau, board mới “lên tiếng” đáp ứng, các board khác giữ im lặng, tránh xung đột dữ liệu trên cùng một bus chung.</p>"
   },
   {
    "title": "Ví dụ: hiển thị N1, EGT trên ECAM bằng BCD-sang-7-đoạn",
    "body": "<p>Giá trị N1 động cơ (vd 92%) được xử lý dưới dạng BCD nội bộ, sau đó bộ chuyển đổi mã BCD-sang-7-đoạn tạo tín hiệu điều khiển đúng các đoạn LED/segment hiển thị để phi công đọc trực tiếp con số thập phân, không cần diễn giải mã nhị phân.</p>",
    "explain": "<p>Đây là một ví dụ thực tế hoàn chỉnh, kết hợp CẢ HAI khái niệm đã học: giá trị N1 (tốc độ động cơ, ví dụ 92%) được lưu trữ và xử lý nội bộ dưới dạng BCD (đúng nguyên lý BCD đã học ở Module 01), sau đó được đưa qua bộ chuyển đổi mã BCD-sang-7-đoạn (đúng nguyên lý decoder đặc biệt đã học ở Phần 3 module này) để tạo tín hiệu điều khiển đúng các đoạn LED cần bật.</p><p>Kết quả cuối cùng: phi công nhìn thấy trực tiếp con số “92” quen thuộc trên màn hình ECAM, không cần “giải mã” bất kỳ chuỗi nhị phân hay hex nào trong đầu, dù toàn bộ quá trình xử lý bên trong đều dựa trên các nguyên lý số học nhị phân/BCD đã học.</p>"
   },
   {
    "title": "Bảng tổng hợp: mạch MSI ↔ ứng dụng avionics thực tế",
    "body": "<table class='tt'><thead><tr><th>Mạch MSI</th><th>Ứng dụng avionics</th></tr></thead><tbody><tr><td>Multiplexer</td><td>Dồn kênh dữ liệu độ cao trước khi mã hoá ARINC 429</td></tr><tr><td>Decoder</td><td>Giải mã địa chỉ bộ nhớ / board trên backplane bus</td></tr><tr><td>Encoder ưu tiên</td><td>Mã hoá phím bấm trên bàn phím MCDU</td></tr><tr><td>Code converter</td><td>BCD-sang-7-đoạn cho hiển thị ECAM</td></tr><tr><td>Parity generator/checker</td><td>Kiểm tra lỗi truyền trên bus dữ liệu</td></tr></tbody></table>",
    "explain": "<p>Bảng tổng hợp cuối cùng này gom lại đúng 5 mạch MSI đã học (multiplexer, decoder, encoder ưu tiên, code converter, parity generator/checker) cùng với ĐÚNG MỘT ứng dụng avionics cụ thể cho mỗi mạch, giúp bạn nhìn thấy ngay mối liên hệ giữa lý thuyết trừu tượng và ứng dụng thực tế cụ thể chỉ trong một bảng.</p><p>Hãy dùng bảng này như bài tự kiểm tra ngược: che cột “ứng dụng avionics” lại, thử tự nhớ xem mỗi mạch MSI có thể ứng dụng ở đâu trên máy bay, rồi mở ra kiểm tra lại.</p>"
   },
   {
    "title": "Vì sao MSI (thay vì SSI hoặc VLSI) phù hợp cho các chức năng này?",
    "body": "<p>Các chức năng trên (giải mã, mã hoá, dồn kênh) đều là logic cố định, không cần khả năng lập trình phức tạp của VLSI, nhưng cũng phức tạp hơn một vài cổng SSI đơn lẻ: MSI là lựa chọn cân bằng giữa chi phí, độ tin cậy (ít điểm hàn hơn khi gộp nhiều cổng vào 1 IC) và đủ chức năng cần thiết.</p>",
    "explain": "<p>Câu hỏi này giúp hiểu SÂU hơn về lý do lựa chọn công nghệ, không chỉ dừng lại ở việc biết định nghĩa. Các chức năng như giải mã, mã hoá, dồn kênh đều là LOGIC CỐ ĐỊNH (không cần thay đổi hành vi sau khi sản xuất), nên không cần tới khả năng LẬP TRÌNH phức tạp và chi phí cao của VLSI.</p><p>Nhưng đồng thời các chức năng này cũng phức tạp hơn một vài cổng logic SSI đơn lẻ (cần từ hàng chục tới hàng trăm cổng phối hợp). MSI là điểm cân bằng tối ưu: đủ chức năng, chi phí hợp lý, và quan trọng với avionics, GỘP nhiều cổng vào một IC nghĩa là ÍT mối hàn hơn so với dùng nhiều IC SSI rời rạc, giúp tăng độ tin cậy tổng thể của hệ thống.</p>"
   },
   {
    "title": "⚠️ Cảnh báo: đường trễ tín hiệu (propagation delay) cộng dồn qua nhiều tầng MSI",
    "body": "<div class='callout warn'><p>Khi ghép tầng nhiều IC MSI (vd 2 tầng decoder, hoặc mux rồi tới encoder), độ trễ lan truyền tín hiệu của từng tầng CỘNG DỒN lại. Với hệ thống cần đáp ứng thời gian thực nghiêm ngặt (vd cảnh báo an toàn), phải tính tổng trễ qua toàn bộ chuỗi MSI, không chỉ xét trễ của từng IC riêng lẻ.</p></div>",
    "explain": "<p>Đây là một bài học về TƯ DUY HỆ THỐNG thay vì chỉ nhìn từng linh kiện riêng lẻ: mỗi IC MSI có độ trễ lan truyền tín hiệu (propagation delay) riêng, thường chỉ vài nano giây, tưởng chừng không đáng kể.</p><p>Nhưng khi ghép NHIỀU tầng IC nối tiếp nhau (ví dụ tín hiệu phải đi qua 2 tầng decoder rồi tới một mux, rồi tới một encoder), các độ trễ nhỏ này CỘNG DỒN lại thành một độ trễ tổng đáng kể. Với hệ thống cần phản ứng cực nhanh (như cảnh báo an toàn khẩn cấp), kỹ sư bắt buộc phải tính TỔNG độ trễ qua toàn bộ chuỗi tín hiệu, không chỉ xét độ trễ của từng IC riêng lẻ, để đảm bảo hệ thống vẫn kịp phản ứng trong thời gian yêu cầu.</p>"
   },
   {
    "title": "Tổng kết module & tự kiểm tra",
    "body": "<p>Bạn đã đi qua: quy mô tích hợp (SSI→VLSI), fan-in/fan-out, decoder/encoder, multiplexer, và ứng dụng thực tế trong avionics. Hãy tự hỏi: nếu phải thiết kế một mạch chọn 1 trong 5 cảm biến áp suất để hiển thị luân phiên trên 1 màn hình, bạn sẽ dùng mạch MSI nào, cần bao nhiêu đường chọn, và tại sao?</p>",
    "explain": "<p>Đây là bài tổng kết yêu cầu vận dụng LIÊN TIẾP nhiều khái niệm đã học trong toàn bộ module: chọn 1 trong 5 cảm biến áp suất cần một multiplexer (đúng nguyên lý Phần 4), với công thức n=log₂(5) cho thấy cần tối thiểu 3 đường chọn (vì 2²=4 chưa đủ, 2³=8 mới đủ).</p><p>Câu hỏi “tại sao” đòi hỏi giải thích được: multiplexer tiết kiệm dây dẫn hơn hẳn so với việc kéo 5 đường tín hiệu riêng biệt tới bộ xử lý hiển thị, chỉ cần 3 đường chọn cộng 1 đường dữ liệu chung. Nếu bạn trả lời được câu hỏi này một cách trôi chảy, bạn đã sẵn sàng cho bộ câu hỏi trắc nghiệm cuối trang và cho Module 04 tiếp theo.</p>"
   }
  ]
 ],
 "en": [
  [
   {
    "title": "Four scales of integration",
    "body": "<p>Scale of integration is measured by the number of equivalent logic gates on a chip:</p><table class='tt'><thead><tr><th>Scale</th><th>Gate count</th><th>Example</th></tr></thead><tbody><tr><td>SSI</td><td>1–11</td><td>A single AND/OR/NAND gate</td></tr><tr><td>MSI</td><td>12–99</td><td>Decoders, multiplexers, bus transceivers</td></tr><tr><td>LSI</td><td>100–9,999</td><td>Small memory, control circuits</td></tr><tr><td>VLSI</td><td>≥10,000</td><td>Microprocessors (millions of transistors)</td></tr></tbody></table>",
    "explain": "<p>The attached image (from the original lecture) shows all 5 integration scales visually on one axis: moving right, the equivalent gate count grows exponentially, from a single NAND gate (SSI) up to a whole microprocessor (VLSI/ULSI) containing millions of gates.</p><p>The key point to grasp: this is not a linear scale. Going from SSI (1 to 11 gates) to MSI (12 to 99 gates) only multiplies by about 10, but going from LSI to VLSI jumps by thousands of times. So whenever someone says a chip is “more complex”, always ask at WHICH scale, rather than comparing vaguely.</p>",
    "img": "icmux_apps_p09.jpg"
   },
   {
    "title": "Fabrication technology: from wafer to die",
    "body": "<p>An IC starts life on a round silicon <b>wafer</b>, on which hundreds of identical circuits are etched simultaneously using photolithography. After testing, the wafer is cut into individual <b>dies</b>, each of which is then packaged and wired out to external pins.</p>",
    "explain": "<p>The wafer-to-die process is like baking one giant sheet cake and cutting it into many identical small pieces: photolithography “prints” hundreds of identical circuits simultaneously onto one round wafer, then a dicing machine cuts the wafer into individual dies.</p><p>The reason for working this way rather than fabricating one chip at a time: setting up the etching process (photomasks, machinery) is very expensive, but once set up, printing hundreds more copies on the same wafer costs almost nothing extra, sharply cutting the per-chip price at large production volumes.</p>"
   },
   {
    "title": "Classification example 1: a standard logic gate",
    "body": "<p>A single 2-input NAND gate contains only a handful of transistors.</p><div class='pd-formula'><div class='pd-formula-label'>Classification</div><div class='pd-formula-math'>1 gate → SSI</div></div><p>Since the gate count is below 12, this is the classic example of the smallest integration scale.</p>",
    "explain": "<p>This is the simplest classification example to start with: just count the logic gates in a device, then look it up against the 4-level table from the first slide.</p><p>A single 2-input NAND gate needs only a handful of transistors to build (typically 4 with CMOS technology), and its equivalent gate count is 1, sitting clearly within the SSI range of 1 to 11, with nothing further to argue about.</p>"
   },
   {
    "title": "Classification example 2: a 64-gate bus transceiver",
    "body": "<p>An IC bus transceiver contains 64 logic gates and buffers (Tooley Ch.8 Q9).</p><div class='pd-formula'><div class='pd-formula-label'>Classification</div><div class='pd-formula-math'>64 gates falls in 12–99 → MSI</div></div>",
    "explain": "<p>At 64 logic gates, this number falls exactly within the MSI range of 12 to 99, neither SSI (below 12) nor yet enough for LSI (100 and above).</p><p>This exercise builds the skill of accurate lookup: remembering just 3 boundary numbers (12, 100, 10,000) lets you classify ANY chip immediately, as long as you know its gate count, with nothing else to memorise.</p>"
   },
   {
    "title": "Classification example 3: a microprocessor",
    "body": "<p>A modern microprocessor contains from a few million to several billion transistors.</p><div class='pd-formula'><div class='pd-formula-label'>Classification</div><div class='pd-formula-math'>≥10,000 equivalent gates → VLSI</div></div><p>This is why microprocessors are always classed as VLSI, even though the logic inside still rests on the same basic gates covered earlier.</p>",
    "explain": "<p>The microprocessor is the most extreme example of integration scale: a modern CPU can contain anywhere from a few million to tens of billions of transistors, exceeding the 10,000-gate threshold for VLSI (the lowest bar for that class) by thousands or even millions of times.</p><p>An interesting fact worth remembering: no matter how enormous the gate count inside a CPU, EACH individual gate still operates on the exact same basic AND/OR/NOT principles learned in Module 02, with no other “magic” involved: the complexity comes entirely from the NUMBER of gates wired together, not from any new kind of logic.</p>"
   },
   {
    "title": "Comparison example: DIP vs PLCC",
    "body": "<p>The same MSI circuit can be packaged as DIP (Dual-In-line Package, two parallel rows of pins) or PLCC (Plastic Leaded Chip Carrier, pins around all four sides).</p><p>PLCC allows more pins in the same footprint area: useful when a circuit needs many I/O signals but board space is limited (Tooley Ch.8 Q5).</p>",
    "explain": "<p>DIP and PLCC are two entirely different “packaging” styles for the same underlying circuit: DIP arranges pins in two parallel rows (like a centipede with legs on two sides), while PLCC spreads pins evenly around all four edges of a square package.</p><p>The reason PLCC exists: when a circuit needs a great many I/O pins (say, 44 or 68) but board space is limited, placing pins around all four edges packs more pins into the same footprint than placing them on only two edges like DIP, much like a room with windows on all four walls lets in more light than one with windows on only two facing walls.</p>"
   },
   {
    "title": "Comparison table of IC package types",
    "body": "<table class='tt'><thead><tr><th>Package</th><th>Feature</th><th>Mounting</th></tr></thead><tbody><tr><td>DIL/DIP</td><td>Two parallel rows of pins</td><td>Through-hole or socket</td></tr><tr><td>PGA</td><td>Pin grid array</td><td>Socket</td></tr><tr><td>PLCC</td><td>Pins on all four sides, smaller than DIP</td><td>Socket or soldered</td></tr><tr><td>SOIC</td><td>Surface-mount, compact</td><td>Always soldered</td></tr><tr><td>QFP</td><td>High pin density on all four sides</td><td>Surface-mount soldering</td></tr></tbody></table>",
    "explain": "<p>This table lists 5 common package types, each with its own shape and mounting style. What matters is not memorising every detail, but noticing the overall TREND: modern package styles (SOIC, QFP) all move toward permanently soldering directly onto the board (surface-mount), instead of plugging into a socket like traditional DIP/PGA.</p><p>This trend reflects the real demand for smaller size and higher reliability in modern electronics, explained further in the next slide on aviation applications.</p>",
    "img": "icmux_apps_p14.jpg"
   },
   {
    "title": "Aviation application: choosing a vibration-resistant package",
    "body": "<p>Avionics equipment must operate reliably under strong vibration and wide temperature swings. Socketed packages (DIP/PGA) carry a risk of loose contact over time from vibration, so many aircraft LRUs favour soldered packages (SOIC, QFP) or sockets with mechanical vibration-locking features plus conformal coating over solder joints.</p>",
    "explain": "<p>Vibration is the enemy of any loosely secured electrical connection: a chip plugged into a socket can, over time, gradually vibrate loose from its contact point, causing intermittent faults that are extremely hard to diagnose (working sometimes, failing other times, depending on whether vibration has just re-seated the contact or not).</p><p>This is why avionics equipment usually favours soldered packages (SOIC, QFP) over sockets: a solder joint cannot gradually “loosen” the way a mechanical socket contact can. When a socket is still needed (for easy component replacement), engineers add mechanical vibration-locking features plus a protective conformal coating to reduce the risk.</p>",
    "img": "icmux_apps_p04.jpg"
   },
   {
    "title": "⚠️ Warning: don't infer integration scale from chip 'age' alone",
    "body": "<div class='callout warn'><p>A chip made in 1981 was most likely DIP/SSI-MSI, but that is only an inference from the technology common at that time, not an absolute rule. Scale of integration is defined by the ACTUAL gate count on the chip, not its manufacturing year.</p></div>",
    "explain": "<p>This is an important warning about REASONING itself: it is tempting to think “an old chip must be SSI/MSI because the technology back then was simpler”, but that is only a STATISTICAL pattern (true for most chips of that era), not a DEFINITION.</p><p>The PRECISE definition of integration scale rests on exactly one criterion: counting the actual equivalent gate count on the chip. A chip made in 1981 could still be VLSI if it genuinely contained over 10,000 gates (rare for that era), and conversely a recently made chip could still be just SSI if its function is simple (say, a single standalone logic gate).</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>Before moving on: a chip containing about 200 logic gates belongs to which integration scale? If it were made after 2000, what packaging style would it likely use?</p>",
    "explain": "<p>This self-check exercise applies the exact same classification table: 200 logic gates falls outside the 12-to-99 MSI range (exceeding 99), so it must be classified as LSI (100 to 9,999).</p><p>As for packaging, if made after the year 2000, this chip would most likely use a modern surface-mount style (SOIC or QFP) rather than the traditional socketed DIP/PGA, following the technology trend from the earlier slides, though this is only an inference from a general trend, not an absolute rule (as warned on the previous slide).</p>"
   }
  ],
  [
   {
    "title": "Defining fan-out",
    "body": "<p><b>Fan-out</b> is the maximum number of standard inputs of the same logic family that an output can safely drive without pushing logic levels outside spec.</p><div class='pd-formula'><div class='pd-formula-label'>Standard TTL fan-out</div><div class='pd-formula-math'>Fan-out = 10 same-family TTL inputs</div></div>",
    "explain": "<p>Picture fan-out as a vehicle's maximum towing capacity: if a vehicle is rated to tow at most 10 identical cargo cars, hitching an 11th car will leave it unable to cope, causing sluggish or faulty operation. Likewise, a gate with fan-out=10 only has enough drive (current) to hold the correct logic level for up to 10 same-family inputs downstream.</p><p>The key point: fan-out is a property of the OUTPUT (the signal source), describing how much load it can carry, quite different from fan-in on the next slide, which is a property of the INPUT.</p>"
   },
   {
    "title": "Defining fan-in",
    "body": "<p><b>Fan-in</b> is the equivalent load (in standard same-family inputs) that ONE specific input places on the preceding stage.</p><ul class='pd-legend'><li><b>Standard input</b><span>fan-in = 1</span></li><li><b>Input feeding two gates at once</b><span>fan-in = 2</span></li></ul>",
    "explain": "<p>If fan-out is a vehicle's towing capacity, fan-in is like the weight of each cargo car: a normal input weighs exactly 1 standard load unit, but if one signal line is wired into MULTIPLE gates at once (like line B in the example), it creates a correspondingly heavier load matching that number of gates.</p><p>This is why, when calculating a circuit's real load, you cannot just count “wires”, you must count how many actual logic-gate inputs are connected, since one wire can branch out to several different gates.</p>"
   },
   {
    "title": "Example: computing the fan-in of a circuit",
    "body": "<p>Input B feeds both gate G3 and gate G4 simultaneously (each a standard device, fan-in 1 per input). The load B places on the previous stage = 1 (from G3) + 1 (from G4) = <b>2</b>.</p>",
    "explain": "<p>This exercise illustrates exactly the point from the previous slide: even though there is only ONE signal line B, it branches into TWO different gates (G3 and G4), so the actual load B must “carry” is not 1, but the sum of each branch: 1 (from G3) plus 1 (from G4) equals 2.</p><p>A calculation easy to get wrong if you just glance at the diagram and count “one line means load 1”: you must always trace EVERY branch of a signal line to count the full load.</p>"
   },
   {
    "title": "Example: computing minimum required fan-out",
    "body": "<p>Gate G1 must drive 6 downstream gates (G2 through G7), each a standard device (fan-in=1 each). The minimum fan-out G1 needs is:</p><div class='pd-formula'><div class='pd-formula-label'>Minimum fan-out</div><div class='pd-formula-math'>6 loads × 1 (fan-in each) = 6</div></div>",
    "explain": "<p>This is the reverse of the previous slide's problem: instead of calculating the load placed on ONE input, we now calculate the MINIMUM fan-out G1's output needs to sufficiently drive all 6 gates downstream.</p><p>The calculation is straightforward: if each load gate (G2 through G7) has the standard fan-in of 1, the total load to “carry” is simply 6 copies of 1 added together, giving 6. If one of those load gates instead had a fan-in greater than 1 (say, a special gate needing double the load), the required minimum fan-out would increase accordingly.</p>"
   },
   {
    "title": "What happens if fan-out is exceeded?",
    "body": "<p>When the load exceeds the rated fan-out, the source gate cannot supply enough current to hold the 'high' level (insufficient source current) or sink enough current for the 'low' level (insufficient sink current), so the actual voltage drifts outside valid logic thresholds: the circuit misbehaves or becomes unreliable.</p>",
    "explain": "<p>This is a genuine PHYSICAL consequence, not just a theoretical number being violated: when a gate must drive more load than it was designed for, it lacks enough current to “push” the voltage high enough (logic 1) or lacks enough capacity to “pull” the voltage low enough (logic 0).</p><p>The practical result: the voltage measured at the loads drifts into an “undefined” zone (between the valid logic 0 and logic 1 thresholds), causing downstream stages to read the signal WRONGLY and inconsistently, sometimes correct, sometimes not, depending on temperature or supply-voltage conditions, extremely hard to diagnose by inspection alone.</p>"
   },
   {
    "title": "Numeric example: adding a buffer when fan-out is exceeded",
    "body": "<p>A standard TTL gate (fan-out=10) must drive 25 TTL inputs. Since 25 &gt; 10, a buffer/driver with higher fan-out (e.g. 30) must be inserted between the source gate and the loads, instead of connecting them directly.</p>",
    "explain": "<p>Inserting a buffer when fan-out is exceeded works exactly like using a PA speaker when one person's voice isn't loud enough for a large hall: the buffer does not “create” a new signal, it simply amplifies enough current so the original signal can drive more loads.</p><p>With 25 loads to drive but the source gate only rated for fan-out 10, a buffer with sufficiently high fan-out (say, 30) must be inserted in between, so the buffer becomes the one actually carrying all 25 loads, while the source gate only needs to drive that single buffer as its one load.</p>"
   },
   {
    "title": "Table: rated fan-out by logic family",
    "body": "<table class='tt'><thead><tr><th>Logic family</th><th>Rated fan-out (same family)</th></tr></thead><tbody><tr><td>Standard TTL</td><td>10</td></tr><tr><td>Low-power Schottky TTL (LS)</td><td>20</td></tr><tr><td>Standard CMOS</td><td>~50 (due to very high input impedance)</td></tr></tbody></table>",
    "explain": "<p>This table reveals something quite interesting: CMOS has a much higher rated fan-out than TTL (about 50 versus 10), but for an entirely different reason than what limits TTL.</p><p>TTL's fan-out is limited because each load draws a fairly large CURRENT. CMOS has extremely high input impedance (drawing almost no current at rest), so in theory it can drive very many loads without any current problem: CMOS's fan-out figure is usually limited by a different factor (speed, covered in Part 5) rather than current the way TTL is.</p>"
   },
   {
    "title": "Aviation application: distributing a clock signal",
    "body": "<p>In a cockpit clock computer, a clock pulse from the central crystal oscillator often must feed several sub-circuits (timekeeping counter, data encoder, display driver). Engineers must sum the total fan-in of every circuit receiving that clock to select a clock distribution buffer/driver with adequate fan-out, avoiding degradation of a critical timing signal.</p>",
    "explain": "<p>The clock-distribution application shows fan-out is far from just textbook theory: a central clock pulse often has to “feed” many different sub-circuits in the same cockpit computer system (timers, encoders, display drivers), each with its own fan-in.</p><p>Engineers must ADD UP the total fan-in of ALL circuits receiving the clock (similar to the fan-in exercise learned earlier), then choose a clock distribution buffer (clock driver) with fan-out large enough to exceed that total. Underestimating this can cause the clock signal to degrade, making sub-circuits receive a MISALIGNED timing reference, a serious fault in a real-time system.</p>"
   },
   {
    "title": "⚠️ Warning: fan-out does not add up across different logic families",
    "body": "<div class='callout warn'><p>A rated fan-out (e.g. TTL's 10) only holds when the loads are inputs of the SAME logic family. When mixing TTL with CMOS, loads must be converted using the cross-family input-loading compatibility table, not simply added as if they were the same family.</p></div>",
    "explain": "<p>This is a very real trap: TTL's fan-out=10 figure only holds when ALL loads are TTL inputs, since that number is calculated based on TTL's own specific current characteristics.</p><p>When mixing TTL with CMOS, you cannot simply add loads the same way as within one family, since CMOS has entirely different input current behaviour (drawing almost no current). You must consult the manufacturer's official “input loading” table to find exactly how many “standard TTL load units” one CMOS input is equivalent to, before adding them up correctly.</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>A CMOS gate with fan-out 50 must drive 12 standard CMOS inputs: is that safe? If 3 of those 12 are actually TTL inputs (not CMOS), what else must you check before concluding it's safe?</p>",
    "explain": "<p>With 12 standard CMOS inputs and a fan-out of 50, the calculation is simple: 12 is much smaller than 50, so it is perfectly safe if ALL loads are CMOS.</p><p>But the follow-up question (3 of them being TTL) is exactly the trap: once logic families are mixed, the fan-out=50 figure (calculated specifically for CMOS loads) cannot be applied directly to those 3 TTL loads. You must consult the cross-family loading conversion table (as warned on the previous slide) before concluding whether it is safe, rather than simply assuming “12 is less than 50, so it must be fine”.</p>"
   }
  ],
  [
   {
    "title": "Defining a decoder",
    "body": "<p>A decoder takes n binary address lines and activates EXACTLY ONE of 2ⁿ output lines corresponding to that address combination: used to select one device/memory location among many.</p>",
    "explain": "<p>Picture a decoder like a telephone switchboard operator: a caller provides an “extension number” (an n-bit binary address), and the operator connects exactly ONE line (out of 2ⁿ possible lines) matching that extension, leaving every other line untouched.</p><p>The formula 2ⁿ gives the maximum number of distinguishable “lines” that n address bits can select, the same principle learned in Module 01 when counting binary combinations. With n=2 address bits, there are exactly 2²=4 possible output lines, matching the 2-to-4 decoder example on the next slide.</p>"
   },
   {
    "title": "Defining an encoder",
    "body": "<p>An encoder performs the OPPOSITE function: given an active signal on 1 of N input lines, it outputs the corresponding binary code on log₂(N) output lines.</p>",
    "explain": "<p>An encoder does exactly the OPPOSITE job of a decoder: instead of receiving an address to select one line, it receives an active signal on ONE of N input lines, then “reports back” that line's binary address using log₂(N) output bits.</p><p>This is a beautifully symmetric relationship in digital design: encoder and decoder are two sides of the same coin, one going from address to selected signal, the other going from selected signal back to address, and the 2ⁿ↔log₂(N) formula applies in both directions.</p>"
   },
   {
    "title": "Example: building the truth table of a 2-to-4 decoder",
    "body": "<table class='tt'><thead><tr><th>A1</th><th>A0</th><th>Y0</th><th>Y1</th><th>Y2</th><th>Y3</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr></tbody></table><p>In each row, exactly one output is 1, with index equal to the binary value of A1A0.</p>",
    "explain": "<p>This truth table shows exactly the “one address, one active output” principle from the first slide: for address A1A0=00 (the value 0 in binary), only Y0 turns on to 1, while the other three lines Y1/Y2/Y3 all stay at 0.</p><p>Worth noticing: the index of the active output line ALWAYS matches the binary value of the input address (address 00→Y0, 01→Y1, 10→Y2, 11→Y3). This is not a coincidence, it is exactly the definition of a standard binary decoder.</p>",
    "img": "icmux_apps_p41.jpg"
   },
   {
    "title": "Example: a 4-to-2 priority encoder",
    "body": "<p>If several inputs are active at once, a PRIORITY encoder selects the HIGHEST-indexed input to encode. E.g. if both I1 and I3 are active → encode based on I3 (higher priority) → output = 11 (binary for 3), ignoring I1.</p>",
    "explain": "<p>A priority encoder solves a real situation an ordinary (non-priority) encoder cannot handle: if TWO inputs are active at the same time, an ordinary encoder produces a wrong or undefined result, since it was not designed to “choose” between two signals.</p><p>A priority encoder resolves this with a simple rule: ALWAYS pick the highest-indexed active input, completely ignoring any lower-indexed ones. With I1 and I3 both active, the system entirely ignores I1 and encodes only I3, exactly like a triage rule in an emergency queue: whoever has the highest priority is always handled first.</p>",
    "img": "icmux_apps_p50.jpg"
   },
   {
    "title": "Example: BCD-to-7-segment code conversion",
    "body": "<p>A BCD-to-7-segment code converter takes a 4-bit BCD input (0000-1001) and drives 7 segment control signals (a-g) of an LED display to show the correct decimal digit: the same principle used for numeric readouts on many cockpit instruments.</p>",
    "explain": "<p>The BCD-to-7-segment code converter is a special case of a “decoder”: instead of having EXACTLY ONE active output like an ordinary decoder, it has 7 outputs (a through g), and for each BCD input, a SPECIFIC COMBINATION of these outputs is turned on to shape the correct digit.</p><p>For example, displaying “0” requires turning on segments a,b,c,d,e,f (everything except the middle segment g); displaying “1” only needs segments b,c (the two right-side segments). Each digit 0-9 has its own on/off “template” for the 7 segments, precomputed by the decoder circuit from the incoming BCD code.</p>"
   },
   {
    "title": "Example: using enable pins to cascade decoders",
    "body": "<p>A 3-to-8 decoder IC has an extra Enable pin. When Enable=0, ALL outputs are forced inactive regardless of the address inputs. Cascading two 3-to-8 decoder ICs through their Enable pins extends the design to a 4-to-16 decoder (using the 4th address bit to select which IC is enabled).</p>",
    "explain": "<p>The Enable pin turns a standalone decoder IC into a “building block” that can be combined into a larger system: when Enable=0, ALL outputs are locked to their inactive level regardless of the input address, effectively powering off that entire decoder block.</p><p>The cascading technique: use the 4th (highest) address bit to decide which of 2 decoder ICs gets its Enable turned ON (each IC handling 8 addresses using the low 3 bits), while the low 3 bits are shared by both ICs to select the correct output among the 8 lines of whichever IC is currently enabled. Result: 2 3-to-8 decoders combine into exactly one 4-to-16 system, with no need to design a new IC from scratch.</p>"
   },
   {
    "title": "Comparison table of the four basic MSI circuits",
    "body": "<table class='tt'><thead><tr><th>Circuit</th><th>Direction</th><th>Main use</th></tr></thead><tbody><tr><td>Decoder</td><td>n in → 2ⁿ out (exactly 1 active)</td><td>Memory address decoding</td></tr><tr><td>Encoder</td><td>N in → log₂N out</td><td>Keyboard encoding</td></tr><tr><td>Multiplexer</td><td>N data channels → 1 out</td><td>Select one of many signal sources</td></tr><tr><td>Demultiplexer</td><td>1 in → N out channels</td><td>Distribute a signal to many destinations</td></tr></tbody></table>",
    "explain": "<p>This table gathers the 4 MSI circuits under exactly one criterion: which direction the data flows. Decoder and encoder mirror each other (n↔2ⁿ in opposite directions), and multiplexer and demultiplexer mirror each other too (N channels↔1 channel in opposite directions).</p><p>Remembering them as symmetric pairs (decoder-encoder, mux-demux) is much easier than memorising 4 separate definitions: each pair is just a “reversal” of the other, and once you understand ONE circuit in a pair, the other is understood simply by flipping the direction of thought.</p>"
   },
   {
    "title": "Aviation application: memory address decoding in a cockpit computer",
    "body": "<p>In a cockpit clock computer (Tooley Figure 6.11), the CPU must select the right ROM/RAM region to read/write. An address decoder takes the high-order address bus bits and activates the correct Chip-Select (CS) pin of the matching ROM or RAM, preventing two memory devices from contending for the data bus at once.</p>",
    "explain": "<p>Memory addressing in the cockpit computer works exactly on the decoder principle just learned: the CPU places a binary address on the address bus, and an address decoder circuit “translates” that address into a SELECT SIGNAL for exactly one specific memory chip (ROM or RAM) via that chip's Chip-Select (CS) pin.</p><p>The critically important safety role of this circuit: if 2 memory chips were EVER simultaneously enabled by CS (due to a decoder fault or design error), both would try to drive the shared data bus at the same time, causing exactly the same electrical conflict as the “bus contention” problem learned in Module 02 on tri-state logic.</p>",
    "img": "icmux_apps_p20.jpg"
   },
   {
    "title": "⚠️ Warning: don't confuse a 'dataless' decoder with a demultiplexer",
    "body": "<div class='callout warn'><p>Physically, a decoder and a demultiplexer can share the SAME IC (by treating one pin as 'data' instead of a fixed active level). But by PURPOSE: a decoder selects a line based on an address, while a demux distributes one data stream to many destinations: don't equate the two concepts just because they can share the same physical chip.</p></div>",
    "explain": "<p>This is a subtle point easy to confuse: PHYSICALLY, a decoder IC and a demultiplexer IC can be the very SAME chip, differing only in how the designer “assigns roles” to its pins (holding one pin at a fixed level to act as a dummy “data” input turns a decoder into a demux).</p><p>But in terms of PURPOSE, the two concepts are entirely different: a decoder is used to SELECT a line based on an address (a selection purpose), while a demultiplexer is used to DISTRIBUTE an actual stream of data to multiple destinations (a data-transfer purpose). Do not conflate the two concepts just because they can share the same physical component.</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>An 8-to-3 priority encoder has simultaneous active signals on inputs 2, 4, and 6. Which input will the encoded output correspond to, and why?</p>",
    "explain": "<p>This practice exercise applies exactly the “pick the highest index” rule of a priority encoder just learned: with inputs 2, 4 and 6 all active simultaneously, the priority encoder entirely ignores inputs 2 and 4, encoding only the HIGHEST-indexed of the three, namely input 6.</p><p>The reason a priority encoder behaves this way: in many real applications (say, CPU interrupt handling), a higher-indexed signal often represents a more urgent or important event, so the “always prioritise the highest index” rule ensures the most important event is always handled first, no matter how many other events are waiting simultaneously.</p>"
   }
  ],
  [
   {
    "title": "Defining a multiplexer",
    "body": "<p>A multiplexer (data selector) selects 1 of N input data channels to route to a single output, based on the binary combination on its select lines.</p><div class='pd-formula'><div class='pd-formula-label'>Select lines required</div><div class='pd-formula-math'>n = log₂(N)</div></div>",
    "explain": "<p>Picture a multiplexer like a gate agent at a small airport with N runways but only ONE taxiway leading out: at any moment, the agent allows EXACTLY ONE aircraft from a specific runway (decided by a “selection ticket”) onto the shared taxiway, while aircraft on other runways must wait.</p><p>The formula n=log₂(N) tells you how many bits are needed on that “selection ticket” (the select lines) to distinguish N different runways: this is exactly the inverse of the 2ⁿ formula learned for decoders, since “selecting 1 of N channels” is itself a form of address decoding.</p>"
   },
   {
    "title": "Example: truth table of a 4-to-1 multiplexer",
    "body": "<table class='tt'><thead><tr><th>S1</th><th>S0</th><th>Output Y</th></tr></thead><tbody><tr><td>0</td><td>0</td><td>D0</td></tr><tr><td>0</td><td>1</td><td>D1</td></tr><tr><td>1</td><td>0</td><td>D2</td></tr><tr><td>1</td><td>1</td><td>D3</td></tr></tbody></table>",
    "explain": "<p>The 4-to-1 mux truth table reads very intuitively: the 2-bit combination on the select lines (S1S0) acts like an “address”, and that value determines EXACTLY which data channel (D0 through D3) gets connected through to output Y.</p><p>An interesting observation: this is exactly the truth table of a 2-to-4 decoder learned in Part 3, just interpreted differently: instead of “turning on the matching output line”, we interpret it as “letting the matching data channel pass through”. Mux and decoder are closely related in their underlying circuit structure.</p>",
    "img": "icmux_apps_p52.jpg"
   },
   {
    "title": "Worked example: select lines for 16 and 32 channels",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Applying n=log₂(N)</div><div class='pd-formula-math'>N=16 → n=4 &nbsp;&nbsp;|&nbsp;&nbsp; N=32 → n=5</div></div><p>The number of select lines grows much slower than the number of data channels: this is exactly why multiplexers save wiring compared with direct parallel transmission.</p>",
    "explain": "<p>The formula n=log₂(N) reveals a very useful property: the number of select lines grows MUCH more slowly than the number of data channels. Going from 16 channels to 32 channels (doubling the channel count) only adds 1 more select line (from 4 to 5), not doubling it.</p><p>This is exactly why a multiplexer is such an effective wire-saving tool: without a mux, transmitting 32 channels in parallel needs 32 separate wires; with a mux, only 5 select lines plus 1 shared output line are needed, 6 wires total instead of 32.</p>"
   },
   {
    "title": "Example: cascading two 4-to-1 muxes into an 8-to-1 mux",
    "body": "<p>Two 4-to-1 mux ICs each handle a group of 4 channels, then a 2-to-1 mux selects between the two ICs' outputs: 3 select lines total (2 shared select lines for both ICs + 1 group-select line), exactly matching n=log₂(8)=3.</p>",
    "explain": "<p>Cascading 2 4-to-1 mux ICs to build an 8-to-1 mux is a very common “build a bigger block from smaller blocks” technique in digital design: instead of finding or designing a dedicated 8-to-1 mux IC, two off-the-shelf 4-to-1 mux ICs are combined, with a small extra 2-to-1 mux added downstream to “choose” between the two first-stage results.</p><p>The total select-line count matches the formula exactly: 2 select lines shared by both 4-to-1 ICs (choosing the channel within a group of 4), plus 1 group-select line (choosing which IC), for a total of 3, exactly equal to log₂(8)=3. This concretely demonstrates the theoretical formula holding true even when several ICs are chained together.</p>"
   },
   {
    "title": "Defining a demultiplexer",
    "body": "<p>A demultiplexer performs the reverse function: it takes one input data stream and routes it to exactly 1 of N outputs, chosen by the select lines: often sharing the same physical IC as a decoder.</p>",
    "explain": "<p>A demultiplexer is the “mirror image” of a multiplexer: instead of merging N sources into one shared line, it takes a SINGLE stream of data and “scatters” it out to exactly 1 of N destinations, according to the address on the select lines.</p><p>An interesting technical point: circuit-wise, a demultiplexer often shares the exact same physical structure as a decoder (differing only in the role assigned to one pin), exactly as noted in Part 3: one IC can “play the role” of either a decoder or a demultiplexer depending on how the engineer uses its data pin.</p>",
    "img": "icmux_apps_p58.jpg"
   },
   {
    "title": "Real example: A320 altitude data multiplexer (Tooley Figure 9.21)",
    "body": "<p>A dual four-channel multiplexer selects 1 of 4 altitude data sources (selected altitude, actual altitude from the left/right ADC) to feed the ARINC 429 serial data encoder, needing only 2 binary select lines instead of 4 separate physical data paths.</p>",
    "explain": "<p>The A320 altitude data-multiplexing example shows a multiplexer solving a genuinely practical problem: instead of needing 4 separate physical transmission lines for 4 different altitude data sources (each requiring its own ARINC 429 encoder, expensive and complex), the system needs only ONE shared encoder, with a multiplexer in front selecting which source gets encoded at each moment.</p><p>Just 2 binary select lines (enough to distinguish 4 sources per n=log₂(4)=2) are enough to control the entire source-selection process, a significant hardware saving compared with duplicating the encoder for each source.</p>"
   },
   {
    "title": "Table: channels, select lines, and wiring saved",
    "body": "<table class='tt'><thead><tr><th>Channels N</th><th>Select lines n</th><th>Without mux (N wires)</th></tr></thead><tbody><tr><td>4</td><td>2</td><td>4</td></tr><tr><td>8</td><td>3</td><td>8</td></tr><tr><td>16</td><td>4</td><td>16</td></tr></tbody></table><p>With a mux, only n select lines plus one shared data output are needed, instead of N parallel data lines.</p>",
    "explain": "<p>This table highlights the multiplexer's wire-saving benefit with concrete numbers: with 16 channels, not using a mux requires 16 separate parallel wires, while using a mux needs only 4 select lines plus 1 shared data line, 5 total.</p><p>The saving grows larger as the channel count increases: this is why a multiplexer is used almost universally whenever data from many sources must travel a long distance or through a constrained wiring space (like inside an aircraft fuselage), instead of running dozens of separate wires.</p>"
   },
   {
    "title": "Aviation application: sharing one display bus among several parameters",
    "body": "<p>An ECAM display must cycle through several dynamic engine parameters (N1, EGT, N2, oil quantity...). A fast multiplexer can select each signal source in turn to feed a shared display processing path, reducing the number of independent signal-processing channels needed.</p>",
    "explain": "<p>The ECAM display needs to show many different engine parameters in rotation (N1, EGT, N2, oil pressure...), but the display-processing electronics behind the screen do not need, and should not have, a separate processing channel for EACH parameter.</p><p>The high-speed multiplexer solution: sequentially “scan” through each parameter source, feeding each one into a SINGLE processing channel at each moment, much like how the human eye rapidly scans across many lines of text to read a whole page without seeing every line at once. This technique significantly reduces the number of independent signal-processing circuits needed in the system.</p>"
   },
   {
    "title": "⚠️ Warning: too few select lines silently drops data, it's not a random fault",
    "body": "<div class='callout warn'><p>If you design an 8-channel mux but only wire 2 select lines (distinguishing only 4 combinations), the remaining 4 channels will NEVER be selected: this is a predictable design error from the n=log₂(N) formula, not a random fault requiring experimental troubleshooting.</p></div>",
    "explain": "<p>This is a design mistake PREDICTABLE by mathematics, not a random fault to be found by trial and error: if a mux needs to choose among 8 channels but uses only 2 select lines (creating only 2²=4 distinct address combinations), then CERTAINLY the remaining 4 channels (channels 4 through 7) will never be selectable, no matter what value the select lines are set to.</p><p>Before assembling the actual circuit, always apply the formula n=log₂(N) to calculate IN ADVANCE how many select lines are needed: for 8 channels, exactly 3 select lines are required (2³=8), not 2. This is how a design flaw is caught on paper, saving a great deal of hardware debugging time later.</p>"
   },
   {
    "title": "Quick self-check",
    "body": "<p>You need to select 1 of 6 temperature sensors to feed a single processor. What is the minimum number of select lines required, and are any address combinations left unused?</p>",
    "explain": "<p>This practice exercise applies the formula n=log₂(N) to the case N=6 (not an even power of 2): since 2²=4 is not enough (less than 6) and 2³=8 is enough (greater than or equal to 6), a minimum of 3 select lines is needed.</p><p>The interesting part of this case: 3 select lines create 2³=8 possible address combinations, but only 6 real sensors need selecting, meaning there are 2 “spare” address combinations (say, corresponding to addresses 110 and 111) connected to no sensor at all. This is a normal, unavoidable outcome whenever the real channel count is not an even power of 2, not a design flaw.</p>"
   }
  ],
  [
   {
    "title": "Overview: where MSI logic is used in avionics",
    "body": "<p>Per Tooley, MSI logic in aircraft falls into five main application groups: address decoding, priority encoding, data multiplexing, BCD-to-7-segment code conversion, and parity checking on data links.</p>",
    "explain": "<p>This slide lists exactly 5 “job roles” that MSI circuits fill in a real aircraft, and interestingly all 5 have already been covered in detail in earlier parts: address decoding (Part 3), priority encoding (Part 3), data multiplexing (Part 4), BCD-to-7-segment code conversion (Part 3), and parity checking (new, covered on the next slide).</p><p>Use this slide as a “summary index”: if any role is still unclear, this is the moment to revisit that specific part before moving on to the real-world examples that follow.</p>"
   },
   {
    "title": "Revisited: the ARINC 429 data multiplexer (Figure 9.21)",
    "body": "<p>4 altitude data sources are multiplexed before being fed into the ARINC 429 serial data encoder: a direct textbook example illustrating a multiplexer in a real altimeter system.</p>",
    "explain": "<p>This is not a new example, it is a deliberate CALLBACK to the altitude-data multiplexer example learned in Part 4, emphasising that this is a REAL application taken directly from the textbook (Tooley Figure 9.21), not a hypothetical scenario.</p><p>Encountering the same example twice, in two different parts (once focused on the multiplexer PRINCIPLE, once focused on its ROLE in the altimeter system), reinforces understanding from two complementary angles.</p>"
   },
   {
    "title": "Example: a parity checker on a data bus",
    "body": "<p>A parity generator/checker (built mainly from cascaded XOR gates) appends a parity bit to data transmitted on a bus. The receiver recomputes parity and compares it: a mismatch signals a transmission error (though it can't identify which bit failed).</p>",
    "explain": "<p>A parity-checking circuit is a simple yet remarkably effective application of the XOR gate learned in Module 02: XOR outputs 1 exactly when the count of 1-inputs is ODD, so a chain of XOR gates can compute “is the total number of 1-bits in this data even or odd” using pure logic, with no need for a complex counter.</p><p>The error-detection principle: the sender precomputes a parity bit so that the total number of 1-bits (including the parity bit) is always even (or always odd, by convention). The receiver recomputes it and compares: if the result differs from the parity received, an error definitely occurred during transmission, though exactly which bit is wrong remains unknown.</p>"
   },
   {
    "title": "Worked example: even parity of a data byte",
    "body": "<p>Data byte <code>10110010</code> has 4 ones: an even count.</p><div class='pd-formula'><div class='pd-formula-label'>Required even-parity bit</div><div class='pd-formula-math'>0 (keeps the total number of 1s even)</div></div>",
    "explain": "<p>This exercise applies the even-parity principle concretely: counting the 1-bits in the byte 10110010 gives exactly 4 ones (at the positions holding value 1), an EVEN number.</p><p>Since the goal of even parity is to keep the TOTAL number of 1-bits (including the added parity bit) always even, and the count is already 4 (even), the parity bit to add must be 0 so as not to change that evenness. If the original byte instead had an odd count of 1-bits, the added parity bit would need to be 1 to “pull” the total back to even.</p>"
   },
   {
    "title": "Example: address decoding on a backplane bus system",
    "body": "<p>In a multi-board system sharing one backplane bus (e.g. VMEbus), each board has a fixed address code. A decoder circuit on each board compares the bus address against its own code: only the matching board responds, avoiding data conflicts.</p>",
    "explain": "<p>In a system with several circuit boards sharing one backplane bus (a physical bus line running through the whole chassis), each board needs to “recognise” when data on the bus is meant for it, and not for another board.</p><p>The solution: each board is assigned a fixed address code, and has a built-in address decoder circuit (exactly the principle learned in Part 3) continuously comparing the address currently on the bus against its own fixed code. Only when the two addresses match does that board “speak up” and respond, while all other boards stay silent, avoiding data conflicts on the shared bus.</p>"
   },
   {
    "title": "Example: displaying N1/EGT on ECAM via BCD-to-7-segment",
    "body": "<p>Engine N1 (e.g. 92%) is processed internally as BCD, then a BCD-to-7-segment code converter drives the correct LED/segment control signals so the pilot reads the decimal figure directly, with no need to interpret raw binary.</p>",
    "explain": "<p>This is a complete real-world example combining BOTH concepts learned so far: the N1 value (engine speed, say 92%) is stored and processed internally as BCD (exactly the BCD principle from Module 01), then passed through a BCD-to-7-segment code converter (exactly the special decoder principle from Part 3 of this module) to generate the signals lighting up the right LED segments.</p><p>The end result: the pilot sees the familiar number “92” directly on the ECAM screen, with no need to “decode” any binary or hex string mentally, even though the entire internal process rests on the binary/BCD arithmetic principles learned earlier.</p>"
   },
   {
    "title": "Summary table: MSI circuit ↔ real avionics application",
    "body": "<table class='tt'><thead><tr><th>MSI circuit</th><th>Avionics application</th></tr></thead><tbody><tr><td>Multiplexer</td><td>Multiplexing altitude data before ARINC 429 encoding</td></tr><tr><td>Decoder</td><td>Memory/board address decoding on a backplane bus</td></tr><tr><td>Priority encoder</td><td>Encoding key presses on an MCDU keypad</td></tr><tr><td>Code converter</td><td>BCD-to-7-segment for ECAM displays</td></tr><tr><td>Parity generator/checker</td><td>Detecting transmission errors on a data bus</td></tr></tbody></table>",
    "explain": "<p>This final summary table gathers the 5 MSI circuits learned (multiplexer, decoder, priority encoder, code converter, parity generator/checker) alongside EXACTLY ONE concrete avionics application for each, letting you see at a glance how abstract theory connects to concrete real-world use, all in one table.</p><p>Use this table as a reverse self-check: cover the “avionics application” column, try to recall from memory where each MSI circuit might be used on the aircraft, then uncover it to verify.</p>"
   },
   {
    "title": "Why MSI (not SSI or VLSI) fits these functions",
    "body": "<p>These functions (decoding, encoding, multiplexing) are fixed logic that doesn't need VLSI's programmability, yet are more complex than a few standalone SSI gates: MSI strikes a balance between cost, reliability (fewer solder joints by combining several gates into one IC), and just enough functionality.</p>",
    "explain": "<p>This question digs DEEPER into the reasoning behind a technology choice, beyond just knowing a definition. Functions like decoding, encoding, and multiplexing are all FIXED LOGIC (behaviour that never needs to change after manufacturing), so they do not need VLSI's complex and costly PROGRAMMABILITY.</p><p>Yet at the same time these functions are more complex than a handful of standalone SSI gates (needing tens to hundreds of coordinated gates). MSI is the optimal balance point: enough functionality, reasonable cost, and, importantly for avionics, PACKING many gates into one IC means FEWER solder joints compared with using many separate SSI ICs, improving the overall system's reliability.</p>"
   },
   {
    "title": "⚠️ Warning: propagation delay accumulates across cascaded MSI stages",
    "body": "<div class='callout warn'><p>When cascading multiple MSI ICs (e.g. two decoder stages, or a mux feeding an encoder), each stage's propagation delay ADDS UP. For systems with strict real-time requirements (e.g. safety warnings), total delay across the whole MSI chain must be computed, not just each IC's individual delay.</p></div>",
    "explain": "<p>This is a lesson in SYSTEMS THINKING rather than looking at individual components in isolation: each MSI IC has its own propagation delay, usually just a few nanoseconds, seemingly negligible.</p><p>But when MANY stages of ICs are chained in series (say, a signal passing through 2 decoder stages, then a mux, then an encoder), these small delays ADD UP into a significant total delay. For systems requiring extremely fast response (such as urgent safety warnings), engineers must calculate the TOTAL delay across the entire signal chain, not just consider each IC's delay in isolation, to ensure the system still responds within the required time.</p>"
   },
   {
    "title": "Module summary & self-check",
    "body": "<p>You've covered: scale of integration (SSI→VLSI), fan-in/fan-out, decoders/encoders, multiplexers, and real avionics applications. Ask yourself: if you had to design a circuit that selects 1 of 5 pressure sensors to display in turn on one screen, which MSI circuit would you use, how many select lines would you need, and why?</p>",
    "explain": "<p>This wrap-up exercise requires applying SEVERAL concepts learned throughout the module IN SEQUENCE: selecting 1 of 5 pressure sensors needs a multiplexer (exactly the Part 4 principle), and the formula n=log₂(5) shows a minimum of 3 select lines is needed (since 2²=4 is not enough, 2³=8 is enough).</p><p>The “why” part requires explaining that a multiplexer saves far more wiring than running 5 separate signal lines to the display processor, needing only 3 select lines plus 1 shared data line. If you can answer this fluently, you are ready for the multiple-choice questions at the bottom of the page and for the upcoming Module 04.</p>"
   }
  ]
 ]
}
