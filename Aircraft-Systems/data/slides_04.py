# -*- coding: utf-8 -*-
"""Slide Module 04 (VI + EN): body + explain (giai thich cho nguoi moi) + img (anh goc tu bai giang)."""

SLIDES = {
 "vi": [
  [
   {
    "title": "Mô hình IPO: khung tư duy cho MỌI hệ thống máy tính",
    "body": "<p>Input (nhập) → Process (xử lý) → Output (xuất) là khung tư duy áp dụng được cho mọi máy tính, từ máy tính bỏ túi tới FMGC. Trước khi phân tích một hệ thống mới, luôn xác định trước: đâu là input, đâu là process, đâu là output.</p>",
    "explain": "<p>Mô hình IPO đơn giản tới mức dễ bị coi nhẹ, nhưng chính sự đơn giản đó là sức mạnh của nó: bất kể một hệ thống trông phức tạp tới đâu, bạn LUÔN có thể bóc tách nó thành đúng ba câu hỏi. Dữ liệu đi vào từ đâu (Input)? Nó được biến đổi ra sao (Process)? Kết quả cuối cùng là gì và đi tới đâu (Output)?</p><p>Với một máy tính bỏ túi, Input là các phím bấm, Process là phép tính, Output là con số hiện trên màn hình. Với FMGC, Input là hàng chục cảm biến, Process là hàng nghìn dòng lệnh điều khiển bay, Output là lệnh gửi tới bề mặt điều khiển. Cùng một khung tư duy, áp dụng cho cả hai thái cực về độ phức tạp.</p>"
   },
   {
    "title": "Ba loại bus và vai trò riêng biệt",
    "body": "<table class='tt'><thead><tr><th>Bus</th><th>Mang gì</th><th>Chiều truyền</th></tr></thead><tbody><tr><td>Address bus</td><td>địa chỉ ô nhớ/thiết bị</td><td>1 chiều (CPU→bộ nhớ)</td></tr><tr><td>Data bus</td><td>dữ liệu thực tế</td><td>2 chiều</td></tr><tr><td>Control bus</td><td>tín hiệu điều khiển/định thời</td><td>2 chiều</td></tr></tbody></table>",
    "explain": "<p>Ba loại bus giống như ba loại đường trong một thành phố phục vụ ba mục đích khác nhau: address bus giống bảng chỉ đường (chỉ cho biết ĐẾN ĐÂU, không chở hàng), data bus giống xe tải chở hàng thật (chở DỮ LIỆU thực sự), còn control bus giống hệ thống đèn giao thông (ra lệnh khi nào đi, khi nào dừng, đi hướng nào).</p><p>Điểm khác biệt quan trọng nhất cần nhớ: address bus chỉ truyền MỘT chiều (CPU luôn là bên phát địa chỉ, bộ nhớ/thiết bị luôn là bên nhận), trong khi data bus và control bus đều truyền HAI chiều, vì CPU vừa cần đọc vừa cần ghi dữ liệu, và cả tín hiệu điều khiển cũng cần phản hồi ngược lại từ thiết bị.</p>",
    "img": "cpu_apps_p14.jpg"
   },
   {
    "title": "Ví dụ từng bước: địa chỉ lớn nhất trên bus 24-bit",
    "body": "<p>Bus địa chỉ 24-bit → 2²⁴ = 16.777.216 địa chỉ khả dĩ, từ 0 tới 16.777.215. Đổi giá trị lớn nhất sang hex (6 chữ số hex vì 24÷4=6): <b>FFFFFF</b>. (Khớp Tooley Ch.6 Q5: đã kiểm chứng bằng notebook 04.)</p>",
    "explain": "<p>Công thức 2ⁿ (đã học từ Module 01 khi đếm tổ hợp nhị phân, và từ Module 03 khi đếm số đường ra decoder) giờ được áp dụng lại đúng nguyên lý đó: số đường dây địa chỉ (n) quyết định số ô nhớ tối đa có thể phân biệt (2ⁿ).</p><p>Với bus 24-bit, 2²⁴ cho ra 16.777.216 địa chỉ, và địa chỉ lớn nhất (toàn bit 1) khi đổi sang hex chỉ cần đúng 6 chữ số (vì 24 chia hết cho 4) là FFFFFF: đây chính là ví dụ thực hành trực tiếp của nguyên lý nhóm 4-bit cho hex đã học ở Module 01.</p>",
    "img": "cpu_apps_p16.jpg"
   },
   {
    "title": "Case study: đồng hồ buồng lái A320 (Figure 6.11, Tooley)",
    "body": "<p>Dao động thạch anh tạo xung UTC → vi xử lý xử lý dữ liệu thời gian → ROM lưu phần mềm điều khiển → RAM lưu dữ liệu tạm → bộ mã hoá dữ liệu nối tiếp gửi ra bus ARINC 429. Đây là ví dụ IPO + 3-bus hoàn chỉnh trong MỘT thiết bị thật.</p>",
    "explain": "<p>Đây là một ví dụ THẬT hoàn chỉnh, gói gọn toàn bộ khung IPO và cả ba loại bus vào đúng MỘT thiết bị cụ thể: đồng hồ buồng lái A320. Dao động thạch anh (nguồn thời gian, giống Input), vi xử lý xử lý dữ liệu (Process, dùng cả ba bus để giao tiếp với ROM/RAM), rồi xuất ra bus ARINC 429 (Output).</p><p>Hình đính kèm cho thấy một sơ đồ khối tương tự, với dữ liệu cảm biến/lệnh phi công đi vào, được xử lý bởi CPU cùng bộ nhớ, rồi xuất ra lệnh điều khiển bề mặt và thông tin hiển thị: đúng cấu trúc IPO + 3-bus đã học, áp dụng cho một hệ thống máy bay thực tế thay vì ví dụ trừu tượng.</p>",
    "img": "cpu_apps_p04.jpg"
   },
   {
    "title": "⚠️ Bẫy: nhầm 'bus' là một sợi dây đơn",
    "body": "<div class='callout warn'><p>Mỗi 'bus' thực chất là một BÓ nhiều đường dây song song (vd address bus 24-bit = 24 đường dây riêng biệt truyền đồng thời), không phải một đường dây duy nhất. Số đường dây quyết định trực tiếp số bit truyền được đồng thời.</p></div>",
    "explain": "<p>Đây là một hình ảnh trực quan sai lầm rất phổ biến khi mới học: nghĩ “bus” là một đường dây đơn, giống như một sợi cáp mạng. Thực tế hoàn toàn khác: một “bus” là một BÓ dây chạy song song, mỗi dây mang đúng một bit.</p><p>Bus địa chỉ 24-bit không phải “một đường truyền 24 lần”, mà là 24 ĐƯỜNG DÂY VẬT LÝ riêng biệt, mỗi đường mang đúng 1 bit của địa chỉ, cả 24 đường hoạt động ĐỒNG THỜI để truyền trọn vẹn một địa chỉ trong một nhịp. Số lượng dây vật lý này chính là con số quyết định “độ rộng bus” (bus width) nhắc tới trong tài liệu kỹ thuật.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Nếu bus địa chỉ chỉ có 8 đường dây, tối đa định vị được bao nhiêu ô nhớ khác nhau? (Gợi ý: 2⁸). So sánh với kết quả 24-bit ở slide trên để thấy rõ vì sao mở rộng thêm vài bit làm tăng vọt số ô nhớ định vị được.</p></div>",
    "explain": "<p>Bài tự luyện áp dụng ngược công thức 2ⁿ với n nhỏ hơn nhiều: bus 8-bit cho ra 2⁸=256 địa chỉ khả dĩ, ít hơn HẲN so với 16.777.216 địa chỉ của bus 24-bit ở slide trước.</p><p>Sự chênh lệch khổng lồ này (256 so với hơn 16 triệu, dù số bit chỉ tăng từ 8 lên 24, tức gấp 3 lần) minh hoạ rõ bản chất TĂNG THEO CẤP SỐ NHÂN của hàm luỹ thừa: mỗi bit thêm vào KHÔNG cộng thêm một lượng cố định vào số địa chỉ, mà NHÂN ĐÔI số địa chỉ hiện có. Đây là lý do các hệ thống hiện đại luôn cố gắng tăng độ rộng bus địa chỉ dù chỉ thêm vài bit, vì lợi ích tăng vọt không tuyến tính.</p>"
   }
  ],
  [
   {
    "title": "RAM vs ROM: khác biệt cốt lõi",
    "body": "<table class='tt'><thead><tr><th>Tiêu chí</th><th>RAM</th><th>ROM</th></tr></thead><tbody><tr><td>Ghi được?</td><td>Có (đọc/ghi)</td><td>Không (chỉ đọc, trừ EPROM/Flash)</td></tr><tr><td>Mất dữ liệu khi tắt điện?</td><td>Có (volatile)</td><td>Không (non-volatile)</td></tr></tbody></table>",
    "explain": "<p>Hãy hình dung RAM như một tấm bảng trắng (viết xoá được thoải mái, nhưng xoá sạch khi tắt đèn phòng), còn ROM như một trang sách đã in sẵn (đọc được nhưng không viết đè lên được, và vẫn còn nguyên dù tắt đèn).</p><p>Hai tiêu chí phân biệt trong bảng chính là hai câu hỏi cốt lõi cần hỏi về bất kỳ loại bộ nhớ nào: nó có GHI được không (read/write hay chỉ read-only), và nó có GIỮ được dữ liệu khi mất điện không (volatile hay non-volatile). Hai tiêu chí này độc lập với nhau, và như slide sau sẽ cho thấy, có những loại bộ nhớ “lai” (như EEPROM/Flash) phá vỡ ranh giới đơn giản RAM/ROM truyền thống.</p>",
    "img": "cpu_apps_p25.jpg"
   },
   {
    "title": "EPROM, OTP EPROM, Mask ROM: phân biệt 3 loại dễ nhầm",
    "body": "<p>Mask ROM: ghi cố định từ khi sản xuất, không đổi được. OTP EPROM: ghi được đúng MỘT lần bởi người dùng. EPROM (UV-erasable): xoá bằng tia UV, ghi lại được NHIỀU lần: đây là loại duy nhất trong 3 loại 'xoá và lập trình lại được' (Tooley Ch.6 Q8).</p>",
    "explain": "<p>Ba loại ROM này khác nhau ở đúng MỘT điểm: AI được phép ghi, và ghi được BAO NHIÊU LẦN. Mask ROM: nhà sản xuất ghi cố định ngay từ khâu chế tạo, người dùng không bao giờ ghi được. OTP EPROM: người dùng ghi được, nhưng chỉ đúng MỘT lần duy nhất (giống như một tờ giấy chỉ viết được bằng bút không tẩy xoá được).</p><p>EPROM (loại xoá bằng tia UV) là loại “linh hoạt” nhất trong ba loại: người dùng có thể ghi, rồi dùng đèn UV chiếu qua một cửa sổ trong suốt trên vỏ chip để XOÁ SẠCH, rồi ghi lại từ đầu, lặp lại nhiều lần. Đây chính là điểm khiến EPROM khác hẳn hai loại còn lại và là loại duy nhất thực sự “tái lập trình được” trong nhóm ba loại này.</p>",
    "img": "cpu_apps_p26.jpg"
   },
   {
    "title": "Ví dụ từng bước: cần bao nhiêu IC DRAM cho 32KB",
    "body": "<p>Mỗi IC 16K×4-bit chứa 16.384×4 = 65.536 bit = 8KB. Cần 32KB ÷ 8KB = <b>4 IC</b>. (Khớp Tooley Ch.6 Q13: đã verify bằng code trong notebook 04.)</p>",
    "explain": "<p>Bài tính này là một bài toán “quy đổi đơn vị” điển hình, cần đi qua đúng ba bước không được bỏ sót bước nào. Bước 1: tính dung lượng MỘT IC bằng cách nhân số địa chỉ với số bit mỗi địa chỉ (16.384×4=65.536 bit). Bước 2: đổi từ bit sang byte (chia 8, ra 8.192 byte = 8KB, vì 1 byte=8 bit).</p><p>Bước 3: chia tổng dung lượng cần có (32KB) cho dung lượng một IC (8KB) để ra số IC cần dùng: 32÷8=4. Lỗi hay gặp nhất ở bài toán dạng này là quên đổi đơn vị bit sang byte ở bước 2, dẫn tới kết quả sai gấp 8 lần.</p>"
   },
   {
    "title": "Cấu trúc ma trận hàng-cột và tín hiệu CAS/RAS",
    "body": "<p>Bộ nhớ bán dẫn tổ chức theo lưới hàng×cột để giảm số chân địa chỉ cần thiết. RAS (Row Address Select) chốt địa chỉ hàng, CAS (Column Address Select) chốt địa chỉ cột: gửi 2 lần thay vì gửi toàn bộ địa chỉ cùng lúc, tiết kiệm chân IC.</p>",
    "explain": "<p>Cấu trúc ma trận hàng-cột giải quyết một vấn đề thực tế rất tinh tế: nếu gửi toàn bộ địa chỉ cùng một lúc, một chip nhớ dung lượng lớn sẽ cần RẤT NHIỀU chân địa chỉ vật lý (ví dụ chip 1 triệu ô nhớ cần 20 chân địa chỉ nếu gửi 1 lần).</p><p>Giải pháp: tổ chức các ô nhớ thành lưới hàng×cột, rồi gửi địa chỉ hàng TRƯỚC (chốt bằng tín hiệu RAS), sau đó gửi địa chỉ cột SAU (chốt bằng tín hiệu CAS), dùng CHUNG một bộ chân địa chỉ cho cả hai lần gửi. Cùng một chip 1 triệu ô nhớ giờ chỉ cần khoảng 10 chân địa chỉ (thay vì 20), đổi lại việc đọc/ghi mất thêm một chút thời gian vì phải gửi địa chỉ thành 2 đợt thay vì 1.</p>"
   },
   {
    "title": "⚠️ Bẫy: nhầm 'random access' với 'RAM' theo nghĩa thông thường",
    "body": "<div class='callout warn'><p>Về mặt kỹ thuật, ROM CŨNG là bộ nhớ 'truy cập ngẫu nhiên' (mọi ô nhớ truy xuất nhanh như nhau): chỉ là không ghi được. Thuật ngữ 'RAM' trong giao tiếp hàng ngày bị hiểu lệch thành 'bộ nhớ đọc/ghi', khác với định nghĩa kỹ thuật gốc của 'random access'.</p></div>",
    "explain": "<p>Đây là một trong những trường hợp thuật ngữ kỹ thuật và cách dùng thông thường trong đời sống bị LỆCH NHAU, dễ gây hiểu nhầm nghiêm trọng nếu không phân biệt rõ. Về mặt kỹ thuật chặt chẽ, “random access” (truy cập ngẫu nhiên) chỉ có nghĩa là mọi ô nhớ được truy xuất nhanh như nhau, bất kể vị trí, KHÔNG liên quan gì tới việc có ghi được hay không.</p><p>Theo định nghĩa đó, ROM hoàn toàn xứng đáng được gọi là “random access” (đối lập với bộ nhớ truy cập tuần tự như băng từ, nơi phải “tua” qua từng vị trí). Nhưng trong giao tiếp hàng ngày, từ “RAM” đã bị hiểu lệch thành đồng nghĩa với “bộ nhớ ghi/đọc được”: đây là lý do bạn không bao giờ nghe ai gọi ROM là “một loại RAM” dù về mặt kỹ thuật ROM cũng random-access.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Một hệ thống cần lưu phần mềm điều khiển KHÔNG được phép người dùng vô tình ghi đè: nên chọn RAM, ROM hay EPROM? Vì sao?</p></div>",
    "explain": "<p>Bài tự luyện áp dụng đúng logic loại trừ dựa trên hai tiêu chí đã học: RAM bị loại ngay vì dữ liệu mất khi tắt điện (không phù hợp lưu phần mềm điều khiển cần tồn tại lâu dài) VÀ vì RAM ghi được (rủi ro bị ghi đè ngoài ý muốn, đúng điều đề bài cấm).</p><p>Giữa ROM và EPROM, cả hai đều không cho phép người dùng vô tình ghi đè trong quá trình vận hành bình thường (ROM không ghi được chút nào, EPROM chỉ ghi lại được qua một quy trình đặc biệt có chủ đích dùng tia UV, không thể xảy ra “vô tình”). Cả hai đều là lựa chọn hợp lý, tuỳ vào việc phần mềm có cần cập nhật định kỳ (chọn EPROM) hay hoàn toàn cố định vĩnh viễn (chọn Mask ROM rẻ hơn khi sản xuất số lượng lớn).</p>"
   }
  ],
  [
   {
    "title": "Bốn khối chức năng chính bên trong CPU",
    "body": "<ul><li>Thanh ghi (registers): lưu tạm địa chỉ/dữ liệu</li><li>ALU (Arithmetic Logic Unit): thực hiện phép toán số học/logic</li><li>Bộ giải mã lệnh (instruction decoder)</li><li>Khối điều khiển/định thời (control & timing)</li></ul>",
    "explain": "<p>Hãy hình dung CPU như một văn phòng nhỏ với đúng bốn nhân viên chuyên trách. Thanh ghi là những ngăn kéo nhỏ trên bàn (chứa tài liệu đang xử lý ngay lúc này). ALU là nhân viên tính toán (thực hiện phép cộng/trừ/so sánh). Bộ giải mã lệnh là nhân viên tiếp nhận (đọc yêu cầu rồi xác định cần làm gì). Khối điều khiển là quản lý (điều phối cả ba nhân viên kia làm đúng việc, đúng lúc).</p><p>Bốn khối này không hoạt động độc lập: chúng phối hợp CHẶT CHẼ trong từng chu kỳ lệnh, và slide sau sẽ đi sâu vào từng thanh ghi cụ thể quan trọng nhất trong số đó.</p>"
   },
   {
    "title": "Accumulator: thanh ghi được dùng nhiều nhất",
    "body": "<p>Accumulator vừa là nguồn (chứa toán hạng đầu vào) vừa là đích (chứa kết quả) cho phần lớn phép toán của CPU: đây là lý do nó được nhắc tới nhiều hơn hẳn các thanh ghi khác trong tài liệu kỹ thuật CPU.</p>",
    "explain": "<p>Accumulator xứng đáng được gọi tên riêng (thay vì chỉ là “một trong nhiều thanh ghi”) vì vai trò ĐẶC BIỆT của nó: hầu hết các lệnh số học/logic đều dùng accumulator làm cả điểm XUẤT PHÁT (chứa toán hạng đầu) lẫn điểm ĐÍCH (chứa kết quả sau khi tính).</p><p>Hãy tưởng tượng nó như một cái bát trộn duy nhất trên bàn bếp: bạn đổ nguyên liệu đầu vào bát, trộn (tính toán), rồi kết quả cũng nằm NGAY TRONG chính cái bát đó, sẵn sàng cho bước tiếp theo hoặc đổ ra ngoài. Đây là lý do accumulator xuất hiện dày đặc trong tài liệu kỹ thuật CPU hơn hẳn các thanh ghi khác.</p>",
    "img": "cpu_apps_p45.jpg"
   },
   {
    "title": "Program Counter (PC) và Stack Pointer (SP)",
    "body": "<p>PC luôn chứa địa chỉ của LỆNH KẾ TIẾP sẽ nạp: còn gọi là 'instruction pointer'. SP trỏ tới đỉnh hiện tại của ngăn xếp (stack), một vùng bộ nhớ RAM ngoài dùng lưu tạm địa chỉ trả về/giá trị thanh ghi khi gọi hàm hoặc xử lý ngắt.</p>",
    "explain": "<p>PC (Program Counter) và SP (Stack Pointer) đều là những “con trỏ” (register chỉ lưu MỘT địa chỉ, không lưu dữ liệu thực), nhưng trỏ tới hai thứ hoàn toàn khác nhau. PC luôn trỏ tới lệnh KẾ TIẾP sẽ được nạp (giống một ngón tay đang chỉ vào dòng tiếp theo cần đọc trong một cuốn sách hướng dẫn).</p><p>SP trỏ tới đỉnh hiện tại của ngăn xếp (stack), một vùng RAM đặc biệt hoạt động theo nguyên tắc “vào sau ra trước” (giống chồng đĩa: chỉ có thể thêm/lấy đĩa từ trên đỉnh). Ngăn xếp được dùng để tạm lưu địa chỉ trở về khi gọi một hàm con, hoặc lưu trạng thái các thanh ghi khi xử lý một ngắt, để sau đó có thể khôi phục lại chính xác.</p>"
   },
   {
    "title": "Bus buffer: vì sao data bus buffer phải là hai chiều",
    "body": "<p>CPU vừa cần ĐỌC dữ liệu từ bộ nhớ (chiều vào) vừa cần GHI dữ liệu ra bộ nhớ (chiều ra) qua cùng một data bus: bus buffer nối CPU với data bus do đó bắt buộc phải hỗ trợ cả 2 chiều (bidirectional), khác với address bus chỉ cần 1 chiều.</p>",
    "explain": "<p>Lý do data bus buffer bắt buộc phải hai chiều nằm ở chính bản chất công việc của CPU với bộ nhớ: CPU không chỉ ĐỌC lệnh và dữ liệu (chiều vào), mà còn phải GHI kết quả tính toán trở lại bộ nhớ (chiều ra), và cả hai việc này đều đi qua CHUNG một data bus vật lý.</p><p>So sánh với address bus: CPU CHỈ BAO GIỜ phát địa chỉ ra ngoài (không bao giờ “nhận” địa chỉ từ bộ nhớ gửi ngược lại), nên address bus buffer chỉ cần một chiều là đủ. Đây chính là lý do vì sao trong sơ đồ khối CPU, bus buffer nối với data bus luôn được vẽ với mũi tên hai đầu, còn bus buffer nối với address bus chỉ có mũi tên một đầu.</p>"
   },
   {
    "title": "⚠️ Bẫy: nhầm ALU với bộ giải mã lệnh",
    "body": "<div class='callout warn'><p>ALU thực hiện PHÉP TOÁN (cộng, trừ, AND, OR, đảo bit...) trên dữ liệu; bộ giải mã lệnh chỉ XÁC ĐỊNH lệnh vừa nạp là lệnh gì để điều khiển đúng khối chức năng: hai khối hoàn toàn khác nhiệm vụ dù đều nằm sát nhau trong sơ đồ CPU.</p></div>",
    "explain": "<p>Đây là một cặp khối chức năng rất dễ gộp lẫn vì chúng luôn “làm việc sát cạnh nhau” trong mọi chu kỳ lệnh, nhưng nhiệm vụ lại hoàn toàn tách biệt. ALU giống như “đôi tay” của CPU: nó THỰC SỰ thực hiện phép tính (cộng, trừ, AND, OR...) trên dữ liệu cụ thể.</p><p>Bộ giải mã lệnh giống như “đôi mắt và bộ não phiên dịch”: nó không tính toán gì cả, chỉ NHÌN vào mã lệnh vừa nạp và XÁC ĐỊNH đó là lệnh gì (cộng? so sánh? nhảy?), rồi ra tín hiệu cho ALU (hoặc khối khác) biết PHẢI làm gì. Nếu bộ giải mã lệnh “đọc nhầm” một lệnh, ALU sẽ thực hiện đúng thao tác nhưng lại là thao tác SAI, minh chứng rõ hai khối này độc lập về chức năng dù luôn đi cùng nhau.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Một byte dữ liệu cần đảo bit (NOT): khối nào trong CPU thực hiện việc này: accumulator, ALU, hay instruction register?</p></div>",
    "explain": "<p>Bài tự luyện yêu cầu áp dụng đúng phân biệt vừa học ở slide trước: đảo bit (NOT) là một PHÉP TOÁN LOGIC thực sự thực hiện trên dữ liệu, nên khối chịu trách nhiệm chắc chắn là ALU, không phải accumulator (chỉ là nơi CHỨA dữ liệu, không tự tính toán) và cũng không phải instruction register (chỉ lưu mã lệnh, không xử lý dữ liệu).</p><p>Quy trình đầy đủ: dữ liệu cần đảo bit thường được nạp vào accumulator trước, ALU đọc dữ liệu đó, thực hiện phép NOT, rồi ghi kết quả TRỞ LẠI accumulator: ba khối (accumulator, ALU) phối hợp, nhưng phép tính THỰC SỰ chỉ do một khối duy nhất (ALU) đảm nhiệm.</p>"
   }
  ],
  [
   {
    "title": "Chu trình Fetch – Decode – Execute",
    "body": "<p>Fetch: CPU đọc mã lệnh từ ô nhớ được PC trỏ tới. Decode: bộ giải mã xác định lệnh là gì. Execute: ALU/khối chức năng liên quan thực hiện lệnh. Chu trình này lặp lại liên tục cho tới khi gặp lệnh HALT.</p>",
    "explain": "<p>Chu trình Fetch-Decode-Execute là “nhịp tim” của mọi CPU, lặp đi lặp lại hàng tỉ lần mỗi giây mà không bao giờ dừng (trừ khi gặp lệnh HALT). Hãy hình dung nó như việc đọc một cuốn công thức nấu ăn từng dòng một: Fetch là “đọc dòng tiếp theo” (lấy đúng lệnh mà PC đang trỏ tới), Decode là “hiểu dòng đó bảo làm gì” (ví dụ “thêm 2 thìa đường”), Execute là “thực sự làm theo” (đổ đường vào).</p><p>Điều quan trọng cần nắm: đây không phải ba bước làm MỘT LẦN rồi dừng, mà là một VÒNG LẶP vô hạn, mỗi vòng xử lý đúng một lệnh, rồi tự động quay lại Fetch cho lệnh kế tiếp, cứ thế tiếp diễn.</p>",
    "img": "cpu_apps_p51.jpg"
   },
   {
    "title": "T-state và chu kỳ máy (machine cycle)",
    "body": "<p>Một T-state = đúng 1 chu kỳ xung nhịp (clock). Một lệnh thường cần NHIỀU T-state, gộp thành các chu kỳ máy M0, M1, M2...: theo Tooley, M1 là chu kỳ nạp và giải mã lệnh (opcode fetch).</p>",
    "explain": "<p>Phân biệt T-state và chu kỳ máy giống như phân biệt “một nhịp đồng hồ” với “một công đoạn công việc”: một T-state chỉ là MỘT tích tắc đơn lẻ của đồng hồ hệ thống (không làm được việc gì trọn vẹn), còn một chu kỳ máy (M0, M1...) là một NHÓM các T-state gộp lại để hoàn thành một công đoạn có ý nghĩa (ví dụ M1 là toàn bộ công đoạn nạp và giải mã một lệnh).</p><p>Ví von: T-state giống như từng bước chân riêng lẻ, còn chu kỳ máy giống như “đi từ phòng này sang phòng kia”, một hành động trọn vẹn cần GHÉP nhiều bước chân lại mới hoàn thành.</p>"
   },
   {
    "title": "Ví dụ từng bước: thời gian thực thi ở 50MHz, 11 T-state",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Thời gian thực thi</div><div class='pd-formula-math'>t = n_T × (1/f_clk)</div></div><p>Chu kỳ xung nhịp T = 1/50.000.000 = 20ns. Thời gian thực thi = 11 × 20ns = <b>220ns</b>. (Khớp Tooley Ch.7 Q15: đã verify bằng code trong notebook 04.)</p>",
    "explain": "<p>Bài tính này áp dụng công thức vật lý cơ bản nhất về thời gian và tần số: chu kỳ (T) luôn là NGHỊCH ĐẢO của tần số (f), vì tần số đo “bao nhiêu lần mỗi giây” còn chu kỳ đo “mỗi lần mất bao lâu”.</p><p>Với xung nhịp 50MHz (50 triệu lần mỗi giây), một chu kỳ đơn lẻ chỉ kéo dài 1/50.000.000 giây = 20 nano giây (ns, tức một phần tỉ giây). Nếu một lệnh cần 11 T-state để hoàn thành, tổng thời gian thực thi đơn giản là 11 nhân với thời gian một T-state: 11×20ns=220ns, nhanh hơn một cái chớp mắt hàng triệu lần.</p>"
   },
   {
    "title": "Ví dụ: theo dõi thanh ghi AL sau lệnh MOV AX, 07FEh",
    "body": "<p>AX (16-bit) gồm AH (byte cao) và AL (byte thấp). 07FEh tách thành AH=07h, AL=FEh. Đổi FEh sang nhị phân: <b>11111110</b>. (Khớp Tooley Ch.7 Q18.)</p>",
    "explain": "<p>Bài tập tách thanh ghi AX thành hai nửa AH/AL là ví dụ cụ thể cho thấy một thanh ghi “lớn” (16-bit) thực chất có thể được truy cập như hai thanh ghi “nhỏ” (8-bit mỗi nửa) độc lập, một kỹ thuật rất phổ biến trong kiến trúc x86.</p><p>Với giá trị hex 07FEh, việc tách thành AH=07h (byte cao, 8 bit đầu) và AL=FEh (byte thấp, 8 bit sau) chỉ đơn giản là “cắt đôi” chuỗi hex 4 chữ số thành hai cặp 2 chữ số. Đổi FEh sang nhị phân dùng đúng bảng tra hex-binary đã học ở Module 01 (F=1111, E=1110), ghép lại được 11111110.</p>"
   },
   {
    "title": "⚠️ Bẫy: quên rằng 1 lệnh có thể cần NHIỀU chu kỳ máy khác nhau",
    "body": "<div class='callout warn'><p>Không phải mọi lệnh đều tốn cùng số T-state: một lệnh truy cập bộ nhớ (đọc/ghi RAM) luôn cần nhiều T-state hơn một lệnh chỉ thao tác trong thanh ghi nội bộ CPU, vì phải chờ thêm thời gian truyền tín hiệu qua address/data bus ra ngoài.</p></div>",
    "explain": "<p>Đây là một điều rất dễ bị bỏ qua khi mới học chu kỳ máy: ngầm giả định TẤT CẢ lệnh đều tốn số T-state giống hệt nhau, trong khi thực tế hoàn toàn không phải vậy.</p><p>Nguyên nhân sâu xa: một lệnh chỉ thao tác NỘI BỘ trong CPU (ví dụ cộng hai thanh ghi với nhau) có thể hoàn thành ngay trong vài T-state vì mọi dữ liệu đều đã sẵn có bên trong chip. Nhưng một lệnh cần TRUY CẬP BỘ NHỚ NGOÀI (đọc/ghi RAM) phải chờ thêm thời gian để tín hiệu truyền qua address bus ra ngoài, chờ bộ nhớ phản hồi, rồi truyền dữ liệu ngược lại qua data bus: mỗi bước này đều tốn thêm T-state, khiến lệnh truy cập bộ nhớ LUÔN chậm hơn lệnh chỉ dùng thanh ghi nội bộ.</p>"
   },
   {
    "title": "Tự kiểm tra nhanh (không chấm điểm)",
    "body": "<div class='callout good'><p>Ở xung nhịp 20MHz, một lệnh cần 4 T-state mất bao lâu để thực thi? (Gợi ý: T=1/20MHz=50ns). Đối chiếu với notebook 04 sau khi tự tính.</p></div>",
    "explain": "<p>Bài tự luyện áp dụng đúng công thức đã học ở slide tính toán 50MHz: trước tiên tính chu kỳ T=1/20.000.000=50ns (chú ý đơn vị MHz nghĩa là triệu Hz, không phải nghìn), sau đó nhân với số T-state cần thiết: 4×50ns=200ns.</p><p>So sánh với ví dụ 50MHz/11 T-state ở slide trước (220ns): dù tần số THẤP HƠN (20MHz so với 50MHz, mỗi T-state chậm hơn), nhưng vì số T-state cần thiết cũng ÍT HƠN (4 so với 11), tổng thời gian thực thi lại NHANH HƠN một chút. Đây là ví dụ cho thấy thời gian thực thi phụ thuộc vào CẢ HAI yếu tố (tần số và số T-state), không chỉ riêng một yếu tố nào.</p>"
   }
  ],
  [
   {
    "title": "Pipelining: chồng lấn các giai đoạn xử lý lệnh",
    "body": "<p>Thay vì fetch-decode-execute TUẦN TỰ từng lệnh một, pipelining cho phép CPU fetch lệnh kế tiếp trong khi đang decode lệnh hiện tại, và decode lệnh đó trong khi đang execute lệnh trước nữa: tăng thông lượng thực thi tổng thể (Tooley Ch.7 Q19).</p>",
    "explain": "<p>Pipelining là một trong những ý tưởng cải tiến hiệu năng khôn ngoan nhất trong kiến trúc CPU, và cách dễ hình dung nhất là so sánh với một dây chuyền giặt là: thay vì một người giặt ĐẦY ĐỦ một mẻ đồ (giặt xong mới phơi, phơi xong mới gấp) rồi mới bắt đầu mẻ tiếp theo, ba người làm ba công đoạn khác nhau CÙNG LÚC trên ba mẻ đồ khác nhau: người 1 đang giặt mẻ 3, người 2 đang phơi mẻ 2, người 3 đang gấp mẻ 1, tất cả diễn ra đồng thời.</p><p>Áp dụng vào CPU: trong khi lệnh A đang được Execute, lệnh B (đến sau) đã có thể được Decode, và lệnh C (đến sau nữa) đã có thể được Fetch, tất cả CÙNG một lúc thay vì phải đợi lệnh A xong hoàn toàn rồi mới bắt đầu lệnh B.</p>"
   },
   {
    "title": "Kiến trúc ba bus: tách riêng bus lệnh và bus dữ liệu",
    "body": "<p>Một số vi xử lý hiệu năng cao dùng bus địa chỉ riêng, bus dữ liệu hệ thống riêng, và bộ nhớ lệnh (instruction ROM) tách biệt khỏi bộ nhớ dữ liệu: cho phép CPU đọc lệnh mới VÀ đọc/ghi dữ liệu CÙNG LÚC, không phải chờ nhau trên một bus chung duy nhất.</p>",
    "explain": "<p>Kiến trúc tách riêng bus lệnh và bus dữ liệu (được minh hoạ trong hình bằng kiến trúc Harvard, đối lập với kiến trúc Von Neumann dùng chung một bộ nhớ và một bus cho cả lệnh lẫn dữ liệu) giải quyết một điểm nghẽn cổ điển: nếu chỉ có MỘT bus dùng chung, CPU không thể vừa lấy lệnh mới vừa đọc/ghi dữ liệu trong cùng một nhịp, vì cả hai việc đều phải “xếp hàng” chờ dùng chung đường truyền.</p><p>Với hai bus tách biệt (một cho bộ nhớ lệnh, một cho bộ nhớ dữ liệu), CPU có thể làm CẢ HAI việc CÙNG LÚC: vừa lấy lệnh tiếp theo, vừa đọc hoặc ghi dữ liệu của lệnh hiện tại, không ai phải chờ ai. Đây chính là lý do các bộ vi điều khiển nhúng (embedded) hiệu năng cao thường chọn kiến trúc Harvard thay vì Von Neumann đơn giản hơn.</p>",
    "img": "cpu_apps_p40.jpg"
   },
   {
    "title": "Ngắt (interrupt) qua đường IRQ",
    "body": "<p>Một thiết bị ngoại vi cần CPU xử lý ngay (vd cảm biến phát hiện lỗi khẩn) sẽ tạo tín hiệu trên đường IRQ (Interrupt Request) thay vì chờ CPU tự hỏi thăm định kỳ (polling): CPU tạm dừng chương trình đang chạy, lưu trạng thái vào stack, xử lý ngắt, rồi khôi phục lại.</p>",
    "explain": "<p>Ngắt (interrupt) giải quyết một vấn đề rất thực tế: nếu CPU phải liên tục “hỏi thăm” từng thiết bị ngoại vi xem có sự kiện gì mới không (gọi là polling, giống việc cứ vài giây lại ngó ra cửa xem có khách tới chưa), sẽ rất lãng phí thời gian xử lý cho những lần hỏi thăm “không có gì mới”.</p><p>Với cơ chế ngắt, thiết bị ngoại vi TỰ CHỦ ĐỘNG “gõ cửa” (tạo tín hiệu trên đường IRQ) đúng khi có sự kiện cần xử lý, còn CPU có thể tập trung làm việc khác cho tới khi thực sự có tiếng gõ cửa. Khi ngắt xảy ra, CPU tạm dừng công việc đang làm, lưu lại TOÀN BỘ trạng thái hiện tại vào stack (đúng khái niệm stack đã học ở Phần 3), xử lý xong sự kiện khẩn cấp, rồi khôi phục lại đúng trạng thái cũ để tiếp tục công việc dở dang như chưa hề bị gián đoạn.</p>"
   },
   {
    "title": "Case study: Boeing 777 AIMS dùng 2 vi xử lý giống hệt nhau",
    "body": "<p>Hệ thống AIMS (Airplane Information Management System) trên Boeing 777 dùng hai vi xử lý giống hệt nhau chạy song song, liên tục so sánh kết quả: nếu kết quả hai bên khác nhau, hệ thống phát hiện lỗi ngay lập tức. Đây là ứng dụng thực tế của kiến trúc CPU dự phòng (redundancy) cho hệ thống avionics tới hạn.</p>",
    "explain": "<p>Hệ thống AIMS trên Boeing 777 là một ví dụ kinh điển về triết lý thiết kế an toàn “không tin tưởng một điểm lỗi duy nhất” (no single point of failure): thay vì tin tưởng hoàn toàn vào MỘT vi xử lý (dù nó có mạnh tới đâu), hệ thống chạy HAI vi xử lý giống hệt nhau song song, cùng nhận dữ liệu đầu vào giống hệt nhau, cùng chạy chương trình giống hệt nhau.</p><p>Nếu cả hai cho ra kết quả GIỐNG NHAU, hệ thống tin tưởng kết quả đó là đúng. Nếu kết quả KHÁC NHAU, đó là bằng chứng chắc chắn có LỖI xảy ra ở một trong hai vi xử lý (do hỏng phần cứng, nhiễu, hoặc lỗi phần mềm hiếm gặp), và hệ thống có thể phát hiện ngay lập tức thay vì âm thầm đưa ra một kết quả sai mà không ai biết.</p>"
   },
   {
    "title": "⚠️ Bẫy: nghĩ rằng pipelining luôn làm lệnh chạy nhanh hơn TỪNG LỆNH riêng lẻ",
    "body": "<div class='callout warn'><p>Pipelining tăng THÔNG LƯỢNG tổng thể (nhiều lệnh hoàn thành hơn trong cùng thời gian), nhưng thời gian hoàn thành của MỘT lệnh đơn lẻ (latency) không nhất thiết giảm: thậm chí có thể tăng nhẹ do chi phí quản lý pipeline. Đừng nhầm 'nhanh hơn' ở cấp độ hệ thống với 'nhanh hơn' ở cấp độ từng lệnh.</p></div>",
    "explain": "<p>Đây là một trong những hiểu nhầm phổ biến nhất về pipelining: nghĩ rằng nếu CPU xử lý “chồng lấn” nhiều lệnh cùng lúc, thì MỖI lệnh đơn lẻ cũng phải hoàn thành nhanh hơn. Thực tế hoàn toàn khác.</p><p>Pipelining cải thiện THÔNG LƯỢNG (throughput: tổng số lệnh hoàn thành trong một khoảng thời gian dài), giống như dây chuyền giặt là xử lý được nhiều mẻ đồ hơn trong một giờ. Nhưng THỜI GIAN để một mẻ đồ CỤ THỂ đi từ lúc bắt đầu giặt tới lúc gấp xong xuôi (latency, độ trễ của MỘT lệnh đơn lẻ) không hề rút ngắn, thậm chí có thể dài hơn một chút do phải “chờ tới lượt” trong dây chuyền. Đừng nhầm “nhanh hơn ở quy mô hệ thống” với “nhanh hơn ở quy mô từng lệnh riêng lẻ”.</p>"
   },
   {
    "title": "Tự kiểm tra tổng kết module (không chấm điểm)",
    "body": "<div class='callout good'><p>Vì sao hệ thống avionics tới hạn (critical) thường KHÔNG dùng một vi xử lý đơn lẻ dù nó đủ mạnh về hiệu năng? Liên hệ lại với case study AIMS ở trên trước khi làm quiz cuối trang.</p></div>",
    "explain": "<p>Câu hỏi tổng kết này buộc bạn liên kết lại TOÀN BỘ triết lý thiết kế đã học trong Phần 5: một vi xử lý dù mạnh tới đâu vẫn có thể hỏng bất ngờ (lỗi phần cứng ngẫu nhiên, nhiễu bức xạ vũ trụ ở độ cao lớn, lỗi phần mềm hiếm khi xảy ra), và khi hỏng, nó KHÔNG TỰ BÁO cho hệ thống biết nó đang sai.</p><p>Đó là lý do các hệ thống avionics tới hạn (critical, tức lỗi có thể gây hậu quả nghiêm trọng tới an toàn bay) không bao giờ đặt cược hoàn toàn vào MỘT điểm lỗi duy nhất, dù điểm đó có hiệu năng tốt tới đâu. Giải pháp luôn là REDUNDANCY (dự phòng): chạy nhiều bộ xử lý song song và so sánh chéo kết quả, đúng như case study AIMS đã học, để một lỗi đơn lẻ không bao giờ có thể âm thầm trở thành một quyết định sai lầm ảnh hưởng tới cả chuyến bay.</p>"
   }
  ]
 ],
 "en": [
  [
   {
    "title": "The IPO model: a thinking framework for EVERY computer system",
    "body": "<p>Input → Process → Output is a framework that applies to every computer, from a pocket calculator to an FMGC. Before analysing any new system, always identify first: what is the input, what is the process, what is the output.</p>",
    "explain": "<p>The IPO model looks simple enough to be dismissed, but that simplicity is exactly its strength: no matter how complex a system looks, you can ALWAYS break it down into exactly three questions. Where does the data come in from (Input)? How is it transformed (Process)? What is the final result and where does it go (Output)?</p><p>For a pocket calculator, Input is the key presses, Process is the arithmetic, Output is the number shown on screen. For an FMGC, Input is dozens of sensors, Process is thousands of lines of flight-control logic, Output is commands sent to control surfaces. The same framework, applied at both extremes of complexity.</p>"
   },
   {
    "title": "Three buses and their distinct roles",
    "body": "<table class='tt'><thead><tr><th>Bus</th><th>Carries</th><th>Direction</th></tr></thead><tbody><tr><td>Address bus</td><td>memory/device address</td><td>one-way (CPU→memory)</td></tr><tr><td>Data bus</td><td>actual data</td><td>two-way</td></tr><tr><td>Control bus</td><td>control/timing signals</td><td>two-way</td></tr></tbody></table>",
    "explain": "<p>The three buses are like three kinds of roads in a city, each serving a different purpose: the address bus is like a signpost (telling you WHERE to go, carrying no cargo), the data bus is like the actual delivery truck (carrying the real DATA), and the control bus is like the traffic light system (commanding when to go, when to stop, which direction).</p><p>The most important distinction to remember: the address bus is ONE-WAY only (the CPU always issues the address, memory/devices always receive it), while both the data bus and control bus are TWO-WAY, since the CPU needs to both read and write data, and control signals also need feedback flowing back from the device.</p>",
    "img": "cpu_apps_p14.jpg"
   },
   {
    "title": "Worked example: the largest address on a 24-bit bus",
    "body": "<p>A 24-bit address bus → 2²⁴ = 16,777,216 possible addresses, from 0 to 16,777,215. Converting the largest value to hex (6 hex digits since 24÷4=6): <b>FFFFFF</b>. (Matches Tooley Ch.6 Q5: verified in notebook 04.)</p>",
    "explain": "<p>The formula 2ⁿ (learned back in Module 01 for counting binary combinations, and again in Module 03 for counting decoder outputs) is applied here on the exact same principle: the number of address wires (n) determines the maximum number of distinguishable memory locations (2ⁿ).</p><p>With a 24-bit bus, 2²⁴ gives 16,777,216 addresses, and the largest address (all bits set to 1), converted to hex, needs exactly 6 digits (since 24 divides evenly by 4) to give FFFFFF: this is a direct hands-on application of the 4-bit-grouping-for-hex principle learned in Module 01.</p>",
    "img": "cpu_apps_p16.jpg"
   },
   {
    "title": "Case study: the A320 cockpit clock (Figure 6.11, Tooley)",
    "body": "<p>A crystal oscillator generates the UTC time base → the microprocessor processes the time data → ROM stores the control software → RAM holds working data → a serial data encoder sends time out on the ARINC 429 bus. This is a complete real-world IPO + 3-bus example in ONE actual device.</p>",
    "explain": "<p>This is a complete REAL example, packing the whole IPO framework and all three buses into ONE specific device: the A320 cockpit clock. The crystal oscillator (the time source, like an Input), the microprocessor processing the data (Process, using all three buses to talk to ROM/RAM), then sending it out on the ARINC 429 bus (Output).</p><p>The attached image shows a similar block diagram, with sensor data and pilot inputs flowing in, processed by the CPU together with memory, then output as control commands and displayed information: exactly the IPO plus 3-bus structure just learned, applied to a real aircraft system rather than an abstract example.</p>",
    "img": "cpu_apps_p04.jpg"
   },
   {
    "title": "⚠️ Trap: thinking a 'bus' is a single wire",
    "body": "<div class='callout warn'><p>Each 'bus' is actually a BUNDLE of many parallel wires (e.g. a 24-bit address bus = 24 separate wires carrying signals simultaneously), not a single wire. The number of wires directly determines how many bits can be transferred at once.</p></div>",
    "explain": "<p>This is a very common visual misconception for beginners: picturing a “bus” as a single wire, like a network cable. The reality is entirely different: a “bus” is a BUNDLE of parallel wires, each carrying exactly one bit.</p><p>A 24-bit address bus is not “one line used 24 times”, it is 24 SEPARATE PHYSICAL WIRES, each carrying exactly 1 bit of the address, all 24 wires operating SIMULTANEOUSLY to transfer a complete address in a single clock tick. This physical wire count is exactly what technical documents mean by “bus width”.</p>"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>If an address bus has only 8 wires, how many unique memory locations can it address? (Hint: 2⁸.) Compare with the 24-bit result above to see how a few extra bits dramatically increase addressable memory.</p></div>",
    "explain": "<p>This practice exercise runs the 2ⁿ formula in reverse with a much smaller n: an 8-bit bus gives 2⁸=256 possible addresses, far fewer than the 16,777,216 addresses of the 24-bit bus in the previous slide.</p><p>This enormous gap (256 versus over 16 million, even though the bit count only tripled from 8 to 24) vividly illustrates the EXPONENTIAL nature of the power function: each extra bit does NOT add a fixed amount to the address count, it DOUBLES the existing count. This is why modern systems always push hard to widen an address bus by even just a few bits, since the payoff grows non-linearly.</p>"
   }
  ],
  [
   {
    "title": "RAM vs ROM: the core difference",
    "body": "<table class='tt'><thead><tr><th>Criterion</th><th>RAM</th><th>ROM</th></tr></thead><tbody><tr><td>Writable?</td><td>Yes (read/write)</td><td>No (read-only, except EPROM/Flash)</td></tr><tr><td>Loses data on power-off?</td><td>Yes (volatile)</td><td>No (non-volatile)</td></tr></tbody></table>",
    "explain": "<p>Picture RAM as a whiteboard (freely erasable and rewritable, but wiped clean when the room lights go off), and ROM as a printed page in a book (readable but not overwritable, and still intact even with the lights off).</p><p>The two criteria in the table are the two core questions worth asking about any memory type: can it be WRITTEN to (read/write versus read-only), and does it KEEP its data when power is lost (volatile versus non-volatile). These two criteria are independent of each other, and as the next slide shows, some “hybrid” memory types (like EEPROM/Flash) blur the traditional simple RAM/ROM boundary.</p>",
    "img": "cpu_apps_p25.jpg"
   },
   {
    "title": "EPROM, OTP EPROM, Mask ROM: three easily confused types",
    "body": "<p>Mask ROM: fixed at manufacture, never changeable. OTP EPROM: user-writable exactly ONCE. EPROM (UV-erasable): erased with UV light, rewritable MANY times: the only one of the three that is truly 'erasable and reprogrammable' (Tooley Ch.6 Q8).</p>",
    "explain": "<p>These three ROM types differ in exactly ONE respect: WHO is allowed to write, and HOW MANY TIMES. Mask ROM: the manufacturer fixes the contents permanently during fabrication, the end user can never write to it. OTP EPROM: the user can write to it, but only ONCE (like a sheet of paper writable only with permanent ink).</p><p>EPROM (the UV-erasable kind) is the most “flexible” of the three: the user can write to it, then shine UV light through a transparent window on the chip's casing to WIPE IT CLEAN, then write it again, repeatable many times. This is exactly what sets EPROM apart from the other two, making it the only truly “erasable and reprogrammable” type among the three.</p>",
    "img": "cpu_apps_p26.jpg"
   },
   {
    "title": "Worked example: how many DRAM chips for 32KB",
    "body": "<p>Each 16K×4-bit chip holds 16,384×4 = 65,536 bits = 8KB. Required: 32KB ÷ 8KB = <b>4 chips</b>. (Matches Tooley Ch.6 Q13: verified by code in notebook 04.)</p>",
    "explain": "<p>This calculation is a classic “unit conversion” problem, and it needs exactly three steps, none of which can be skipped. Step 1: compute ONE chip's capacity by multiplying the number of addresses by the bits per address (16,384×4=65,536 bits). Step 2: convert bits to bytes (divide by 8, giving 8,192 bytes = 8KB, since 1 byte = 8 bits).</p><p>Step 3: divide the total capacity needed (32KB) by one chip's capacity (8KB) to get the number of chips required: 32÷8=4. The most common mistake in this type of problem is forgetting to convert bits to bytes in Step 2, which throws the final answer off by a factor of 8.</p>"
   },
   {
    "title": "Row-column matrix structure and the CAS/RAS signals",
    "body": "<p>Semiconductor memory is organised as a row×column grid to reduce the number of address pins needed. RAS (Row Address Select) latches the row address, CAS (Column Address Select) latches the column address: sent in two steps instead of the full address at once, saving IC pins.</p>",
    "explain": "<p>The row-column matrix structure solves a subtle but very real problem: sending an entire address all at once would require a large-capacity memory chip to have an enormous number of physical address pins (for example, a chip with 1 million cells would need 20 address pins if sent all at once).</p><p>The solution: arrange the memory cells into a row×column grid, then send the row address FIRST (latched by the RAS signal), followed by the column address (latched by the CAS signal), reusing the SAME set of address pins for both transmissions. That same 1-million-cell chip now needs only about 10 address pins (instead of 20), at the cost of a slightly longer read/write time since the address arrives in two steps instead of one.</p>"
   },
   {
    "title": "⚠️ Trap: confusing 'random access' with everyday 'RAM' usage",
    "body": "<div class='callout warn'><p>Technically, ROM is ALSO 'random-access' memory (every cell is accessed with equal ease): it simply cannot be written to. Everyday usage of the term 'RAM' has drifted to mean 'read/write memory', which differs from the original technical definition of 'random access'.</p></div>",
    "explain": "<p>This is a case where a strict technical term and everyday usage have DRIFTED APART, causing serious confusion if the two are not kept separate. Technically, “random access” simply means every memory cell is accessed with equal speed regardless of position, with NO connection whatsoever to whether it can be written to.</p><p>By that definition, ROM fully deserves the label “random access” too (as opposed to sequential-access memory like magnetic tape, which must be “wound” past every position in between). But in everyday usage, the word “RAM” has drifted to mean “read/write memory” specifically: this is exactly why no one ever calls ROM “a type of RAM”, even though technically ROM is random-access too.</p>"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>A system must store control software that users should NEVER be able to accidentally overwrite: should you choose RAM, ROM, or EPROM? Why?</p></div>",
    "explain": "<p>This practice exercise applies the exact elimination logic just learned, based on the two criteria: RAM is ruled out immediately because its data is lost when powered off (unsuitable for control software that must persist long-term) AND because RAM is writable (risking accidental overwrite, exactly what the problem forbids).</p><p>Between ROM and EPROM, neither allows the user to accidentally overwrite it during normal operation (ROM cannot be written at all, EPROM can only be rewritten through a special deliberate UV process, never “accidentally”). Both are reasonable choices, depending on whether the software needs periodic updates (choose EPROM) or is permanently fixed forever (choose the cheaper Mask ROM when mass-produced).</p>"
   }
  ],
  [
   {
    "title": "Four main functional blocks inside a CPU",
    "body": "<ul><li>Registers: temporary storage for addresses/data</li><li>ALU (Arithmetic Logic Unit): performs arithmetic/logic operations</li><li>Instruction decoder</li><li>Control & timing unit</li></ul>",
    "explain": "<p>Picture a CPU as a small office with exactly four dedicated staff. Registers are the small drawers on the desk (holding whatever is being worked on right now). The ALU is the calculator clerk (performing addition/subtraction/comparison). The instruction decoder is the intake clerk (reading a request and figuring out what it means). The control unit is the manager (coordinating all three of the others to do the right thing at the right time).</p><p>These four blocks do not work in isolation: they cooperate TIGHTLY within every single instruction cycle, and the next slide dives into the single most important register among them.</p>"
   },
   {
    "title": "The accumulator: the most heavily used register",
    "body": "<p>The accumulator is both a source (holding an input operand) and a destination (holding the result) for most CPU operations: this is why it is referenced far more often than any other register in CPU technical documentation.</p>",
    "explain": "<p>The accumulator earns a name of its own (rather than being just “one of many registers”) because of its SPECIAL role: most arithmetic/logic instructions use the accumulator as both the STARTING point (holding the first operand) and the ENDING point (holding the result after the calculation).</p><p>Picture it as the one and only mixing bowl on a kitchen counter: you pour ingredients in, mix (calculate), and the result also ends up RIGHT IN that same bowl, ready for the next step or to be poured out. This is exactly why the accumulator appears far more often in CPU technical documentation than any other register.</p>",
    "img": "cpu_apps_p45.jpg"
   },
   {
    "title": "Program Counter (PC) and Stack Pointer (SP)",
    "body": "<p>The PC always holds the address of the NEXT instruction to be fetched: also called the 'instruction pointer'. The SP points to the current top of the stack, an area of external RAM used to temporarily store return addresses/register values during function calls or interrupt handling.</p>",
    "explain": "<p>PC (Program Counter) and SP (Stack Pointer) are both “pointers” (registers holding only an address, not actual data), but they point at two entirely different things. The PC always points to the NEXT instruction to be fetched (like a finger tracking the next line to read in an instruction manual).</p><p>The SP points to the current top of the stack, a special area of RAM operating on a “last in, first out” principle (like a stack of plates: you can only add or remove a plate from the top). The stack is used to temporarily store a return address when calling a subroutine, or to save register states while handling an interrupt, so everything can later be restored exactly.</p>"
   },
   {
    "title": "Bus buffers: why the data bus buffer must be bidirectional",
    "body": "<p>The CPU needs to both READ data from memory (inbound) and WRITE data to memory (outbound) through the same data bus: the bus buffer connecting the CPU to the data bus must therefore support both directions (bidirectional), unlike the address bus which only needs one direction.</p>",
    "explain": "<p>The reason the data bus buffer must be bidirectional lies in the very nature of the CPU's work with memory: the CPU does not only READ instructions and data (inbound), it must also WRITE calculation results back to memory (outbound), and both of these travel over the SAME physical data bus.</p><p>Compare with the address bus: the CPU ONLY EVER issues an address outward (it never “receives” an address sent back from memory), so the address bus buffer only needs one direction. This is exactly why, on a CPU block diagram, the buffer connecting to the data bus is always drawn with a double-headed arrow, while the one connecting to the address bus has only a single-headed arrow.</p>"
   },
   {
    "title": "⚠️ Trap: confusing the ALU with the instruction decoder",
    "body": "<div class='callout warn'><p>The ALU performs OPERATIONS (add, subtract, AND, OR, invert...) on data; the instruction decoder only DETERMINES what instruction was just fetched so it can direct the correct functional block: two completely different jobs despite sitting close together on a CPU block diagram.</p></div>",
    "explain": "<p>This is a pair of functional blocks very easy to conflate, since they always “work right next to each other” in every instruction cycle, yet their jobs are entirely separate. The ALU is like the CPU's “hands”: it ACTUALLY performs the calculation (add, subtract, AND, OR...) on specific data.</p><p>The instruction decoder is like the “eyes and interpreting brain”: it does no calculation at all, it just LOOKS at the instruction just fetched and DETERMINES what it is (add? compare? jump?), then signals the ALU (or another block) what TO DO. If the instruction decoder “misreads” an instruction, the ALU will still correctly perform an operation, just the WRONG one, clearly demonstrating these two blocks are functionally independent despite always working side by side.</p>"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>A byte of data needs to be inverted (NOT): which CPU block performs this: the accumulator, the ALU, or the instruction register?</p></div>",
    "explain": "<p>This practice exercise requires applying exactly the distinction just learned: inverting a bit (NOT) is a genuine LOGIC OPERATION performed on data, so the responsible block is certainly the ALU, not the accumulator (which only HOLDS data, without calculating anything itself) and not the instruction register (which only stores the instruction code, without processing data).</p><p>The full sequence: the data to be inverted is usually loaded into the accumulator first, the ALU reads that data, performs the NOT operation, then writes the result BACK into the accumulator: three blocks cooperate (accumulator, ALU), but the actual calculation is carried out by exactly one of them (the ALU).</p>"
   }
  ],
  [
   {
    "title": "The Fetch – Decode – Execute cycle",
    "body": "<p>Fetch: the CPU reads the opcode from the memory location the PC points to. Decode: the decoder determines what the instruction is. Execute: the ALU/relevant functional block carries it out. This cycle repeats continuously until a HALT instruction is met.</p>",
    "explain": "<p>The Fetch-Decode-Execute cycle is the “heartbeat” of every CPU, repeating billions of times per second without ever stopping (unless a HALT instruction is hit). Picture it like reading a recipe book one line at a time: Fetch is “read the next line” (grab exactly the instruction the PC is pointing at), Decode is “understand what that line says to do” (say, “add 2 spoons of sugar”), Execute is “actually do it” (pour the sugar in).</p><p>The key point to grasp: this is not three steps done once and finished, it is an INFINITE LOOP, each pass handling exactly one instruction, then automatically looping back to Fetch for the next one, continuing indefinitely.</p>",
    "img": "cpu_apps_p51.jpg"
   },
   {
    "title": "T-states and machine cycles",
    "body": "<p>One T-state = exactly one clock cycle. An instruction usually needs SEVERAL T-states, grouped into machine cycles M0, M1, M2...: per Tooley, M1 is the opcode fetch-and-decode cycle.</p>",
    "explain": "<p>Distinguishing a T-state from a machine cycle is like distinguishing “one clock tick” from “one stage of work”: a T-state is just ONE single tick of the system clock (not enough to accomplish anything meaningful on its own), while a machine cycle (M0, M1...) is a GROUP of T-states combined to complete one meaningful stage (for example, M1 is the entire opcode fetch-and-decode stage).</p><p>An analogy: a T-state is like a single footstep, while a machine cycle is like “walking from this room to that room”, a complete action requiring several footsteps COMBINED to finish.</p>"
   },
   {
    "title": "Worked example: execution time at 50MHz, 11 T-states",
    "body": "<div class='pd-formula'><div class='pd-formula-label'>Execution time</div><div class='pd-formula-math'>t = n_T × (1/f_clk)</div></div><p>Clock period T = 1/50,000,000 = 20ns. Execution time = 11 × 20ns = <b>220ns</b>. (Matches Tooley Ch.7 Q15: verified by code in notebook 04.)</p>",
    "explain": "<p>This calculation applies the most basic physics formula relating time and frequency: the period (T) is always the RECIPROCAL of the frequency (f), since frequency measures “how many times per second” while period measures “how long each time takes”.</p><p>With a 50MHz clock (50 million times per second), a single cycle lasts only 1/50,000,000 second = 20 nanoseconds (ns, one billionth of a second). If an instruction needs 11 T-states to complete, the total execution time is simply 11 times the duration of one T-state: 11×20ns=220ns, faster than a blink of an eye by millions of times.</p>"
   },
   {
    "title": "Example: tracing the AL register after MOV AX, 07FEh",
    "body": "<p>AX (16-bit) consists of AH (high byte) and AL (low byte). 07FEh splits into AH=07h, AL=FEh. Converting FEh to binary: <b>11111110</b>. (Matches Tooley Ch.7 Q18.)</p>",
    "explain": "<p>Splitting the AX register into two halves, AH/AL, is a concrete example showing that a “large” 16-bit register can actually be accessed as two independent “small” 8-bit registers, a technique very common in x86 architecture.</p><p>With the hex value 07FEh, splitting it into AH=07h (the high byte, the first 8 bits) and AL=FEh (the low byte, the last 8 bits) is simply “slicing in half” a 4-digit hex string into two 2-digit pairs. Converting FEh to binary uses exactly the hex-binary lookup table learned in Module 01 (F=1111, E=1110), joined together to give 11111110.</p>"
   },
   {
    "title": "⚠️ Trap: forgetting that instructions can need DIFFERENT numbers of machine cycles",
    "body": "<div class='callout warn'><p>Not every instruction costs the same number of T-states: a memory-access instruction (reading/writing RAM) always needs more T-states than one operating purely on internal CPU registers, because it must wait for extra signal propagation time over the external address/data bus.</p></div>",
    "explain": "<p>This is something very easy to overlook when first learning about machine cycles: implicitly assuming EVERY instruction costs the same number of T-states, when in reality that is far from true.</p><p>The underlying reason: an instruction operating purely INTERNALLY within the CPU (say, adding two registers together) can finish in just a few T-states since all the data is already available on-chip. But an instruction needing to ACCESS EXTERNAL MEMORY (reading/writing RAM) must wait extra time for the signal to propagate out over the address bus, wait for memory to respond, then transfer data back over the data bus: each of these steps adds T-states, making a memory-access instruction ALWAYS slower than one operating purely on internal registers.</p>"
   },
   {
    "title": "Quick self-check (ungraded)",
    "body": "<div class='callout good'><p>At a 20MHz clock, how long does an instruction requiring 4 T-states take to execute? (Hint: T=1/20MHz=50ns.) Check against notebook 04 after computing it yourself.</p></div>",
    "explain": "<p>This practice exercise applies exactly the formula learned in the 50MHz calculation slide: first compute the period T=1/20,000,000=50ns (note that MHz means millions of Hz, not thousands), then multiply by the number of required T-states: 4×50ns=200ns.</p><p>Compare with the 50MHz/11-T-state example from the previous slide (220ns): although the frequency here is LOWER (20MHz versus 50MHz, so each T-state is slower), because FEWER T-states are needed (4 versus 11), the total execution time actually ends up slightly FASTER. This shows execution time depends on BOTH factors together (frequency and T-state count), not on either one alone.</p>"
   }
  ],
  [
   {
    "title": "Pipelining: overlapping instruction processing stages",
    "body": "<p>Instead of fetching-decoding-executing instructions strictly SEQUENTIALLY, pipelining lets the CPU fetch the next instruction while decoding the current one, and decode that one while executing the instruction before it: increasing overall execution throughput (Tooley Ch.7 Q19).</p>",
    "explain": "<p>Pipelining is one of the cleverest performance ideas in CPU architecture, and the easiest way to picture it is comparing it to a laundry assembly line: instead of one person washing an ENTIRE load (finishing the wash before starting to dry, finishing the dry before starting to fold) before starting the next load, three people handle three different stages AT THE SAME TIME on three different loads: person 1 is washing load 3, person 2 is drying load 2, person 3 is folding load 1, all happening simultaneously.</p><p>Applied to a CPU: while instruction A is being Executed, instruction B (which comes after) can already be Decoded, and instruction C (after that) can already be Fetched, ALL AT THE SAME TIME, instead of waiting for instruction A to fully finish before starting instruction B.</p>"
   },
   {
    "title": "Three-bus architecture: separating the instruction and data buses",
    "body": "<p>Some high-performance processors use a separate address bus, a separate system data bus, and instruction memory (instruction ROM) kept apart from data memory: letting the CPU fetch a new instruction AND read/write data AT THE SAME TIME, instead of both waiting on one shared bus.</p>",
    "explain": "<p>Separating the instruction bus from the data bus (illustrated here by Harvard architecture, as opposed to Von Neumann architecture, which shares one memory and one bus for both instructions and data) solves a classic bottleneck: with only ONE shared bus, the CPU cannot fetch a new instruction AND read/write data in the same clock tick, since both must “queue up” for the same shared pathway.</p><p>With two separate buses (one for instruction memory, one for data memory), the CPU can do BOTH at the SAME TIME: fetching the next instruction while reading or writing the current instruction's data, with neither having to wait for the other. This is exactly why high-performance embedded microcontrollers often choose Harvard architecture over the simpler Von Neumann design.</p>",
    "img": "cpu_apps_p40.jpg"
   },
   {
    "title": "Interrupts via the IRQ line",
    "body": "<p>A peripheral device needing immediate CPU attention (e.g. a sensor detecting an urgent fault) raises a signal on the IRQ (Interrupt Request) line instead of waiting for the CPU to periodically check in (polling): the CPU pauses its current program, saves state to the stack, services the interrupt, then resumes.</p>",
    "explain": "<p>Interrupts solve a very practical problem: if the CPU had to constantly “check in” with every peripheral device to see if anything new happened (called polling, like glancing out the door every few seconds to see if a guest has arrived), a great deal of processing time would be wasted on checks that find “nothing new”.</p><p>With the interrupt mechanism, a peripheral device PROACTIVELY “knocks on the door” (raising a signal on the IRQ line) exactly when there is something to handle, while the CPU is free to focus on other work until an actual knock occurs. When an interrupt fires, the CPU pauses its current task, saves its ENTIRE current state to the stack (exactly the stack concept learned in Part 3), handles the urgent event, then restores the exact previous state to resume the interrupted work as if nothing happened.</p>"
   },
   {
    "title": "Case study: the Boeing 777 AIMS uses two identical microprocessors",
    "body": "<p>The AIMS (Airplane Information Management System) on the Boeing 777 runs two identical microprocessors in parallel, continuously comparing their results: if the two disagree, the system detects the fault immediately. This is a real application of redundant CPU architecture for a critical avionics system.</p>",
    "explain": "<p>The AIMS system on the Boeing 777 is a textbook example of the “no single point of failure” design philosophy: instead of fully trusting ONE microprocessor (no matter how powerful), the system runs TWO identical microprocessors in parallel, both receiving the exact same input data, both running the exact same program.</p><p>If both produce the SAME result, the system trusts that result. If the results DIFFER, that is definite proof a FAULT occurred in one of the two processors (from hardware failure, interference, or a rare software bug), and the system can detect it immediately instead of silently producing a wrong answer that no one notices.</p>"
   },
   {
    "title": "⚠️ Trap: assuming pipelining always makes EACH instruction run faster",
    "body": "<div class='callout warn'><p>Pipelining increases overall THROUGHPUT (more instructions complete per unit time), but the completion time of any ONE individual instruction (latency) is not necessarily reduced: it can even increase slightly due to pipeline management overhead. Don't confuse system-level 'faster' with per-instruction 'faster'.</p></div>",
    "explain": "<p>This is one of the most common misconceptions about pipelining: assuming that if a CPU processes multiple instructions “overlapping” in time, EACH individual instruction must also finish faster. The reality is quite different.</p><p>Pipelining improves THROUGHPUT (the total number of instructions completed over a long stretch of time), just as a laundry assembly line handles more loads per hour. But the TIME for one SPECIFIC load to go from start-of-wash to finish-of-fold (latency, the delay of a single instruction) is not shortened at all, and can even lengthen slightly due to having to “wait its turn” in the pipeline. Do not confuse “faster at the system level” with “faster at the individual-instruction level”.</p>"
   },
   {
    "title": "Final module self-check (ungraded)",
    "body": "<div class='callout good'><p>Why do critical avionics systems typically NOT rely on a single microprocessor, even one powerful enough on its own? Relate your answer back to the AIMS case study above before taking the quiz at the bottom of the page.</p></div>",
    "explain": "<p>This wrap-up question requires connecting the ENTIRE design philosophy learned across Part 5: even the most powerful microprocessor can suddenly fail (random hardware fault, cosmic radiation interference at high altitude, a rare software bug), and when it fails, it does NOT automatically alert the system that it is now wrong.</p><p>This is why critical avionics systems (where a fault could seriously endanger flight safety) never bet everything on ONE single point of failure, no matter how good its performance. The solution is always REDUNDANCY: running multiple processors in parallel and cross-checking their results, exactly as in the AIMS case study, so that a single fault can never silently turn into a wrong decision affecting the entire flight.</p>"
   }
  ]
 ]
}
