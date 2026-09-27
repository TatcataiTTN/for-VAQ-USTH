import json, random, os
from collections import Counter

# =====================================================================================
# Nguon: cau hoi trac nghiem TRICH XUAT tu sach Mike Tooley, "Aircraft Digital Electronic
# and Computer Systems", 3rd ed., cac chuong 2/5/8/9/6/7 (ban OCR force-ocr, xem session).
# Moi cau da duoc tinh toan LAI DOC LAP (khong doc dap an goc trong Appendix 3 vi trang do
# OCR bi loi/khong the doc ro - xem ghi chu trong bao cao) truoc khi dua vao day.
# Cac cau PHU THUOC HINH VE goc (vd "Figure 5.30 See Question 1") bi LOAI vi khong the
# hien thi lai hinh chinh xac tu OCR - khong doan mo ta hinh.
# "correct" la INDEX trong opts o dang nguyen ban (truoc khi script xao vi tri ben duoi).
# =====================================================================================

MOD1_ORIG = [
  dict(q="Số nhị phân 10101 tương ứng với số thập phân nào?", en="The binary number 10101 is equivalent to the decimal number:",
       opts=["19","21","35"], correct=1, src="Tooley Ch.2 Q1",
       explain="10101₂ = 1·16+0·8+1·4+0·2+1·1 = 21."),
  dict(q="Số thập phân 29 tương ứng với số nhị phân nào?", en="The decimal number 29 is equivalent to the binary number:",
       opts=["10111","11011","11101"], correct=2, src="Tooley Ch.2 Q2",
       explain="29 = 16+8+4+1 → 11101₂."),
  dict(q="Bù hai (two's complement) của số nhị phân 10110 là:", en="The two's complement of the binary number 10110 is:",
       opts=["01010","01001","10001"], correct=0, src="Tooley Ch.2 Q3",
       explain="Đảo bit: 01001, cộng 1 → 01010."),
  dict(q="Số BCD 10010001 tương ứng với số thập phân nào?", en="The BCD number 10010001 is equivalent to the decimal number:",
       opts=["19","91","145"], correct=1, src="Tooley Ch.2 Q4",
       explain="Tách nhóm 4 bit: 1001=9, 0001=1 → 91."),
  dict(q="Số thập phân 37 tương ứng với mã BCD nào?", en="The decimal number 37 is equivalent to the BCD number:",
       opts=["00110111","00100101","00101111"], correct=0, src="Tooley Ch.2 Q5",
       explain="3→0011, 7→0111 → 00110111."),
  dict(q="Dãy số nào sau đây KHÔNG THỂ là một số bát phân (octal)?", en="Which one of the following numbers could not be an octal number:",
       opts=["11011","771","139"], correct=2, src="Tooley Ch.2 Q6",
       explain="Số bát phân chỉ dùng chữ số 0-7; 139 chứa chữ số 9 nên không hợp lệ."),
  dict(q="Số bát phân 73 tương ứng với số thập phân nào?", en="The octal number 73 is equivalent to the decimal number:",
       opts=["47","59","111"], correct=1, src="Tooley Ch.2 Q7",
       explain="73₈ = 7·8+3 = 59."),
  dict(q="Số nhị phân 100010001 tương ứng với số bát phân nào?", en="The binary number 100010001 is equivalent to the octal number:",
       opts=["111","273","421"], correct=2, src="Tooley Ch.2 Q8",
       explain="Nhóm 3 bit từ phải: 100 010 001 → 4 2 1 → 421₈."),
  dict(q="Số thập lục phân (hex) 111 tương ứng với số bát phân nào?", en="The hexadecimal number 111 is equivalent to the octal number:",
       opts=["73","273","421"], correct=2, src="Tooley Ch.2 Q9",
       explain="111₁₆ = 273₁₀; 273₁₀ = 421₈ (273 = 4·64+2·8+1)."),
  dict(q="Số hex C9 tương ứng với số thập phân nào?", en="The hexadecimal number C9 is equivalent to the decimal number:",
       opts=["21","129","201"], correct=2, src="Tooley Ch.2 Q10",
       explain="C9₁₆ = 12·16+9 = 201."),
  dict(q="Số nhị phân 10110011 tương ứng với số hex nào?", en="The binary number 10110011 is equivalent to the hexadecimal number:",
       opts=["93","B3","113"], correct=1, src="Tooley Ch.2 Q11",
       explain="Nhóm 4 bit: 1011=B, 0011=3 → B3."),
  dict(q="Số hex AD tương ứng với số nhị phân nào?", en="The hexadecimal number AD is equivalent to the binary number:",
       opts=["10101101","11011010","10001101"], correct=0, src="Tooley Ch.2 Q12",
       explain="A=1010, D=1101 → 10101101."),
  dict(q="Số bát phân 706₈ tương ứng với:", en="The number 706₈ is equivalent to:",
       opts=["1C6₁₆","111001110₂","484₁₀"], correct=0, src="Tooley Ch.2 Q13",
       explain="706₈ = 7·64+0·8+6 = 454₁₀ = 1C6₁₆ (1·256+12·16+6=454). Nhị phân đúng của 454 là 111000110, không phải phương án (b)."),
]

MOD1_GEN = [
  dict(q="Số thập phân 45 tương ứng với số nhị phân nào?", en="The decimal number 45 is equivalent to the binary number:",
       opts=["101101","101110","100101"], correct=0, explain="45 = 32+8+4+1 → 101101₂."),
  dict(q="Số nhị phân 11001 tương ứng với số thập phân nào?", en="The binary number 11001 is equivalent to the decimal number:",
       opts=["25","27","19"], correct=0, explain="16+8+0+0+1 = 25."),
  dict(q="Số hex 2F tương ứng với số thập phân nào?", en="The hex number 2F is equivalent to the decimal number:",
       opts=["45","47","49"], correct=1, explain="2·16+15 = 47."),
  dict(q="Số thập phân 200 tương ứng với số hex nào?", en="The decimal number 200 is equivalent to the hex number:",
       opts=["C8","D2","B4"], correct=0, explain="200 = 12·16+8 → C8."),
  dict(q="Số bát phân 47 tương ứng với số thập phân nào?", en="The octal number 47 is equivalent to the decimal number:",
       opts=["37","39","41"], correct=1, explain="4·8+7 = 39."),
  dict(q="Số thập phân 68 tương ứng với mã BCD nào?", en="The decimal number 68 is equivalent to the BCD code:",
       opts=["01101000","01100100","01111000"], correct=0, explain="6→0110, 8→1000 → 01101000."),
  dict(q="Số nhị phân 11110000 tương ứng với số hex nào?", en="The binary number 11110000 is equivalent to the hex number:",
       opts=["F0","0F","FF"], correct=0, explain="1111=F, 0000=0 → F0."),
  dict(q="Bù hai của số nhị phân 01101 (5 bit) là:", en="The two's complement of the 5-bit binary number 01101 is:",
       opts=["10011","10010","01100"], correct=0, explain="Đảo bit: 10010, cộng 1 → 10011."),
  dict(q="Số nhị phân 11100101 tương ứng với số bát phân nào?", en="The binary number 11100101 is equivalent to the octal number:",
       opts=["345","344","354"], correct=0, explain="Nhóm 3 bit từ phải (đệm trái): 011 100 101 → 3 4 5 → 345₈."),
  dict(q="Mã ASCII (hex) của ký tự 'A' là:", en="The ASCII code (hex) of the character 'A' is:",
       opts=["41","42","40"], correct=0, explain="'A' = 65 thập phân = 41 hex (chuẩn ASCII)."),
]

MOD2_ORIG = [
  dict(q="Điện áp nguồn danh định của một linh kiện logic TTL là:", en="The normal supply voltage for a TTL logic device is:",
       opts=["2.5V ±5%","5V ±5%","12V ±5%"], correct=1, src="Tooley Ch.5 Q2",
       explain="Họ logic TTL chuẩn hoạt động ở nguồn 5V ±5%."),
  dict(q="Cổng NAND 2 đầu vào cho ra mức logic 0 khi nào?", en="A two-input NAND gate will produce a logic 0 output when:",
       opts=["cả hai đầu vào ở mức logic 0","một trong hai đầu vào ở mức logic 0","cả hai đầu vào ở mức logic 1"], correct=2, src="Tooley Ch.5 Q3",
       explain="NAND = NOT(AND); AND=1 chỉ khi cả 2 vào đều 1, nên NAND=0 khi cả 2 vào đều 1."),
  dict(q="Trong một bộ đếm nhị phân, xung clock của mỗi tầng bistable (trừ tầng đầu) thường được lấy từ:", en="In a binary counter, the clock input of each bistable stage is fed from:",
       opts=["cùng một đường clock chung","đầu ra Q của tầng trước","đường CLEAR"], correct=1, src="Tooley Ch.5 Q4",
       explain="Đây là cấu trúc bộ đếm không đồng bộ (ripple counter): mỗi tầng lấy clock từ Q của tầng trước."),
  dict(q="Họ logic phù hợp nhất cho thiết bị kiểm tra cầm tay (portable test equipment) là:", en="The most appropriate logic family for use in a portable item of test equipment is:",
       opts=["CMOS","TTL","low-power Schottky TTL"], correct=0, src="Tooley Ch.5 Q6",
       explain="CMOS tiêu thụ dòng tĩnh cực thấp, phù hợp thiết bị chạy pin/cầm tay."),
  dict(q="Biên độ nhiễu (noise margin) của linh kiện TTL chuẩn là khoảng:", en="The noise margin for standard TTL devices is:",
       opts=["400 mV","800 mV","2 V"], correct=0, src="Tooley Ch.5 Q8",
       explain="TTL chuẩn có noise margin danh định khoảng 400mV."),
  dict(q="Một cổng logic CMOS được cấp nguồn 12V. Nếu đo được 3V tại đầu vào, mức này được coi là:", en="A CMOS logic gate is operated from a 12V supply. A voltage of 3V measured at the input is considered:",
       opts=["logic 0","không xác định (indeterminate)","logic 1"], correct=0, src="Tooley Ch.5 Q9",
       explain="Ngưỡng chuyển mức của CMOS thường ở khoảng 50% Vdd = 6V; 3V < 6V nên được coi là logic 0."),
]

MOD2_GEN = [
  dict(q="Cổng NOR 2 đầu vào cho ra mức logic 1 khi nào?", en="A two-input NOR gate produces logic 1 when:",
       opts=["cả hai đầu vào ở mức logic 0","một trong hai đầu vào ở mức logic 1","cả hai đầu vào ở mức logic 1"], correct=0,
       explain="NOR=NOT(OR); OR=0 chỉ khi cả hai vào đều 0, nên NOR=1 khi cả hai vào đều 0."),
  dict(q="Cổng XOR 2 đầu vào với cả hai đầu vào bằng 1 sẽ cho đầu ra:", en="A two-input XOR gate with both inputs at 1 gives an output of:",
       opts=["0","1","không xác định"], correct=0, explain="XOR chỉ ra 1 khi hai đầu vào KHÁC nhau; (1,1) cho ra 0."),
  dict(q="Theo đại số Boolean, biểu thức A + A'B rút gọn thành:", en="In Boolean algebra, the expression A + A'B simplifies to:",
       opts=["A + B","A · B","A"], correct=0, explain="Đây là luật hấp thụ mở rộng: A + A'B = A + B."),
  dict(q="Theo định lý De Morgan, (A·B)' bằng:", en="By De Morgan's theorem, (A·B)' equals:",
       opts=["A' + B'","A'·B'","A + B"], correct=0, explain="(AB)' = A' + B' theo định lý De Morgan."),
  dict(q="Một bảng chân trị (truth table) có 3 biến đầu vào sẽ có bao nhiêu tổ hợp?", en="A truth table with 3 input variables has how many rows (combinations)?",
       opts=["8","6","9"], correct=0, explain="Số tổ hợp = 2ⁿ với n=3 → 2³ = 8."),
  dict(q="Một flip-flop JK với J=K=1 tại cạnh xung clock sẽ:", en="A JK flip-flop with J=K=1 at the clock edge will:",
       opts=["đảo trạng thái (toggle)","giữ nguyên trạng thái","luôn reset về 0"], correct=0, explain="J=K=1 là chế độ toggle đặc trưng của JK flip-flop."),
  dict(q="So với TTL, họ logic CMOS thường có biên độ nhiễu (noise margin):", en="Compared with TTL, CMOS logic generally has a noise margin that is:",
       opts=["lớn hơn","nhỏ hơn","bằng nhau"], correct=0, explain="CMOS có dải điện áp ra gần sát 2 mức nguồn (rail-to-rail) nên noise margin thường lớn hơn TTL."),
  dict(q="Một bộ đệm ba trạng thái (tri-state buffer) có bao nhiêu trạng thái đầu ra khả dĩ?", en="A tri-state buffer has how many possible output states?",
       opts=["3 (0, 1, và trở kháng cao Z)","2 (0 và 1)","4"], correct=0, explain="Tri-state có thêm trạng thái trở kháng cao (high-Z) ngoài 0 và 1."),
  dict(q="Cổng logic nào được gọi là 'cổng vạn năng' vì có thể dùng để tạo mọi hàm logic khác?", en="Which gate is called a 'universal gate' because any logic function can be built from it alone?",
       opts=["NAND","AND","XOR"], correct=0, explain="NAND (và NOR) là cổng vạn năng; chỉ dùng NAND có thể tạo AND, OR, NOT, v.v."),
  dict(q="Trong quy ước logic dương (positive logic), mức logic 1 tương ứng với:", en="In positive logic convention, logic 1 corresponds to:",
       opts=["mức điện áp cao hơn","mức điện áp thấp hơn","luôn đúng bằng 5V"], correct=0, explain="Quy ước logic dương: điện áp cao hơn = 1, điện áp thấp hơn = 0."),
]

MOD3_ORIG = [
  dict(q="Một cổng logic chuẩn sản xuất năm 1981 nhiều khả năng được đóng gói dạng:", en="A standard logic gate manufactured in 1981 is likely to be supplied in a:",
       opts=["gói DIL","gói PGA","gói QFP"], correct=0, src="Tooley Ch.8 Q1",
       explain="Thập niên 1980, DIL (Dual-In-Line) là kiểu đóng gói phổ biến nhất cho IC logic chuẩn."),
  dict(q="Một cổng logic chuẩn (standard logic gate) là ví dụ điển hình của loại tích hợp nào?", en="A standard logic gate is a typical example of:",
       opts=["thiết bị SSI","thiết bị LSI","thiết bị VLSI"], correct=0, src="Tooley Ch.8 Q2",
       explain="Cổng logic đơn lẻ chỉ chứa vài transistor → thuộc quy mô tích hợp nhỏ SSI."),
  dict(q="Trong các mức độ tích hợp sau, mức nào có mật độ transistor LỚN HƠN?", en="Which one of the following scales of integration is the largest:",
       opts=["SSI","LSI","MSI"], correct=1, src="Tooley Ch.8 Q3",
       explain="Thứ tự tăng dần mật độ: SSI < MSI < LSI < VLSI; trong 3 lựa chọn, LSI lớn nhất."),
  dict(q="Vi xử lý (microprocessor) là ví dụ của công nghệ:", en="A microprocessor is an example of:",
       opts=["công nghệ SSI","công nghệ MSI","công nghệ VLSI"], correct=2, src="Tooley Ch.8 Q4",
       explain="Vi xử lý chứa hàng triệu transistor → thuộc quy mô tích hợp rất lớn VLSI."),
  dict(q="So với đóng gói DIP, đóng gói PLCC mang lại ưu điểm nào?", en="Compared with DIP packaging, PLCC offers:",
       opts=["nhiều chân hơn trên cùng kích thước","kích thước lớn hơn","độ tin cậy cao hơn"], correct=0, src="Tooley Ch.8 Q5",
       explain="PLCC (Plastic Leaded Chip Carrier) cho phép bố trí nhiều chân hơn trong diện tích nhỏ gọn hơn so với DIP."),
  dict(q="Kiểu đóng gói IC nào bắt buộc phải hàn cố định (không thể cắm vào đế/socket)?", en="Which IC packaging technology requires the chip to always be soldered in place:",
       opts=["DIL","SOIC","PGA"], correct=1, src="Tooley Ch.8 Q6",
       explain="SOIC là gói dán bề mặt (surface-mount), luôn được hàn trực tiếp lên board, không dùng đế cắm như DIL/PGA."),
  dict(q="Công nghệ đóng gói IC nào ra đời SỚM NHẤT trong các lựa chọn sau?", en="Which of the following IC packaging technologies was the earliest to be used:",
       opts=["ceramic DIP","ceramic QFP","PLCC"], correct=0, src="Tooley Ch.8 Q7",
       explain="Ceramic DIP là kiểu đóng gói IC thương mại sớm nhất trong ba lựa chọn."),
  dict(q="Các mối nối từ pad trên die IC tới chân ra thường được:", en="The connections from the pads on an integrated circuit die are:",
       opts=["hàn thiếc vào dây nối trong","bấm (crimp) vào dây nối trong","hàn siêu âm/nhiệt (welded) vào dây nối trong"], correct=2, src="Tooley Ch.8 Q8",
       explain="Kỹ thuật wire-bonding gắn dây vàng/nhôm từ pad tới khung dẫn bằng hàn siêu âm/nhiệt (welded), không phải hàn thiếc thông thường."),
  dict(q="Một IC bus transceiver chứa 64 cổng logic và bộ đệm. Chip này là ví dụ của quy mô tích hợp:", en="An IC bus transceiver containing 64 logic gates and buffers is an example of:",
       opts=["SSI","MSI","LSI"], correct=1, src="Tooley Ch.8 Q9",
       explain="Vài chục tới ~100 cổng logic tương ứng quy mô tích hợp vừa MSI."),
  dict(q="Việc kiểm tra sản xuất (production test) trên một wafer IC được thực hiện:", en="Production tests are performed on an integrated circuit wafer:",
       opts=["trước khi cắt thành từng chip riêng","sau khi cắt thành từng chip riêng","chỉ khi chip đã được gắn lên board"], correct=0, src="Tooley Ch.8 Q13",
       explain="Wafer được kiểm tra (wafer probing) ngay khi còn nguyên tấm, trước công đoạn cắt (dicing)."),
  dict(q="Mỗi mạch tích hợp riêng lẻ được cắt ra từ một wafer được gọi là:", en="Each individual integrated circuit produced from a wafer is known as a:",
       opts=["blank","die","gate"], correct=1, src="Tooley Ch.8 Q15",
       explain="Thuật ngữ chuẩn cho một chip cắt rời từ wafer là 'die'."),
  dict(q="Fan-out của một cổng logic TTL chuẩn là:", en="A standard TTL logic gate has a fan-out of:",
       opts=["5","10","20"], correct=1, src="Tooley Ch.9 Q1",
       explain="TTL chuẩn có fan-out danh định là 10 (điều khiển được tối đa 10 đầu vào TTL cùng họ)."),
  dict(q="Số lượng tải đầu vào chuẩn (cùng họ logic) mà MỘT đầu vào của mạch logic tạo ra được gọi là:", en="The equivalent number of standard input loads imposed by the input of a logic circuit is known as:",
       opts=["fan-in","fan-out","fan-load"], correct=0, src="Tooley Ch.9 Q2",
       explain="Đây chính là định nghĩa của fan-in."),
  dict(q="Tên gọi khác của bộ dồn kênh (multiplexer) là:", en="Another name for a multiplexer is:",
       opts=["bộ chọn dữ liệu (data selector)","bộ thu phát bus (bus transceiver)","thanh ghi dịch (shift register)"], correct=0, src="Tooley Ch.9 Q4",
       explain="Multiplexer thường được gọi là 'data selector' vì chức năng chọn 1 trong nhiều nguồn dữ liệu đưa ra 1 ngõ ra."),
  dict(q="Một bộ dồn kênh 4-sang-1 (4-to-1 multiplexer) cần bao nhiêu đường chọn (select input)?", en="A four-to-one multiplexer has:",
       opts=["một đường chọn","hai đường chọn","bốn đường chọn"], correct=1, src="Tooley Ch.9 Q5",
       explain="Cần n đường chọn để phân biệt 2ⁿ kênh vào; với 4 kênh, n=2."),
  dict(q="Một số bộ mã hoá (encoder) có thêm chân enable input/output để cho phép:", en="Additional enable inputs and outputs are provided in some encoders in order to permit:",
       opts=["đảo tín hiệu (inverting)","ghép tầng (cascading)","phát hiện lỗi (error detection)"], correct=1, src="Tooley Ch.9 Q8",
       explain="Chân enable cho phép nối tầng (cascade) nhiều IC encoder để mở rộng số đầu vào mã hoá."),
]

MOD3_GEN = [
  dict(q="Một bộ dồn kênh 8-sang-1 (8-to-1 multiplexer) cần bao nhiêu đường chọn?", en="An 8-to-1 multiplexer needs how many select lines?",
       opts=["3","4","2"], correct=0, explain="2ⁿ=8 → n=3 đường chọn."),
  dict(q="Một bộ giải mã (decoder) 3-sang-8 đường có bao nhiêu ngõ ra?", en="A 3-to-8 line decoder has how many output lines?",
       opts=["8","3","6"], correct=0, explain="Decoder n-sang-2ⁿ với n=3 → 2³=8 ngõ ra."),
  dict(q="Một IC chứa khoảng 500 cổng logic thường được xếp vào quy mô tích hợp nào?", en="A chip containing roughly 500 logic gates is typically classified as:",
       opts=["LSI","SSI","MSI"], correct=0, explain="Khoảng vài trăm tới ~10.000 cổng tương ứng LSI (theo phân loại dùng trong chương này)."),
  dict(q="Bộ giải dồn kênh (demultiplexer) thực hiện chức năng ngược lại với:", en="A demultiplexer performs the opposite function of a:",
       opts=["bộ dồn kênh (multiplexer)","bộ mã hoá (encoder)","bộ so sánh (comparator)"], correct=0, explain="Demux đưa 1 nguồn vào ra nhiều đường, ngược với chức năng dồn nhiều vào 1 của mux."),
  dict(q="Một bộ mã hoá (encoder) có 8 đầu vào sẽ cho ra bao nhiêu bit mã nhị phân?", en="An encoder with 8 inputs will typically produce how many binary output bits?",
       opts=["3","8","4"], correct=0, explain="log2(8)=3 bit đủ để mã hoá 8 trạng thái đầu vào."),
  dict(q="Trong đóng gói IC, thuật ngữ 'DIL' là viết tắt của:", en="In IC packaging, 'DIL' stands for:",
       opts=["Dual-In-Line","Digital Integrated Logic","Direct Input Line"], correct=0, explain="DIL = Dual-In-Line, kiểu đóng gói hai hàng chân song song."),
  dict(q="Mạch tạo/kiểm tra parity (parity generator/checker) thường được xây dựng chủ yếu từ:", en="A parity generator/checker circuit is commonly built mainly from:",
       opts=["các cổng XOR nối tầng","các cổng AND","các cổng NAND"], correct=0, explain="Chuỗi cổng XOR cho phép tính tổng modulo-2 của các bit, đúng nguyên lý tính parity."),
  dict(q="Kiểu đóng gói IC nào được thiết kế cho lắp ráp dán bề mặt (surface-mount), không xuyên lỗ?", en="Which IC package type is designed for surface-mount (not through-hole) assembly?",
       opts=["SOIC","DIP","PGA"], correct=0, explain="SOIC (Small Outline IC) là gói dán bề mặt điển hình."),
  dict(q="Nếu fan-out của một cổng là 10, điều này có nghĩa là cổng có thể an toàn điều khiển tối đa bao nhiêu đầu vào chuẩn cùng họ?", en="If a gate's fan-out is 10, it can safely drive up to how many standard inputs of the same family?",
       opts=["10","5","20"], correct=0, explain="Định nghĩa fan-out chính là số tải đầu vào chuẩn tối đa mà ngõ ra có thể điều khiển."),
  dict(q="Mạch so sánh (comparator) được dùng để:", en="A comparator circuit is used to:",
       opts=["xác định số nào lớn hơn/bằng/nhỏ hơn giữa hai số nhị phân","chuyển đổi nhị phân sang thập phân","lưu trữ dữ liệu nhị phân"], correct=0, explain="Comparator so sánh hai số nhị phân và đưa ra tín hiệu A>B, A=B hoặc A<B."),
]

MOD4_ORIG = [
  dict(q="Đường bus nào dùng để xác định vị trí ô nhớ (memory location)?", en="Which computer bus is used to specify memory locations:",
       opts=["address bus","control bus","data bus"], correct=0, src="Tooley Ch.6 Q4",
       explain="Address bus mang địa chỉ ô nhớ/thiết bị cần truy cập."),
  dict(q="Địa chỉ hex lớn nhất có thể xuất hiện trên một bus địa chỉ 24-bit là:", en="What is the largest hexadecimal address that can appear on a 24-bit address bus:",
       opts=["FFFF","FFFFF","FFFFFF"], correct=2, src="Tooley Ch.6 Q5",
       explain="24 bit = 6 chữ số hex, giá trị lớn nhất toàn bit 1 → FFFFFF."),
  dict(q="Trọng tài bus (bus arbitration) được dùng để:", en="Bus arbitration is required in order to:",
       opts=["ngăn mất dữ liệu bộ nhớ","tránh tranh chấp bus (bus contention)","giảm lỗi do nhiễu và EMI"], correct=1, src="Tooley Ch.6 Q6",
       explain="Bus arbitration quyết định thiết bị nào được quyền dùng bus tại một thời điểm, tránh nhiều thiết bị cùng truyền lúc."),
  dict(q="Một thiết bị nhớ mà mọi ô dữ liệu đều truy xuất được với độ trễ như nhau gọi là bộ nhớ:", en="A memory device in which any item of data can be retrieved with equal ease is known as:",
       opts=["truy cập tuần tự","truy cập ngẫu nhiên (random access)","truy cập song song"], correct=1, src="Tooley Ch.6 Q7",
       explain="Đây chính là định nghĩa của bộ nhớ truy cập ngẫu nhiên (RAM/ROM về bản chất vật lý)."),
  dict(q="Loại bộ nhớ nào sau đây có thể xoá và lập trình lại được?", en="Which one of the following memory devices can be erased and reprogrammed:",
       opts=["Mask-programmed ROM","OTP EPROM","EPROM"], correct=2, src="Tooley Ch.6 Q8",
       explain="EPROM (Erasable Programmable ROM) xoá bằng tia UV và lập trình lại được nhiều lần; OTP chỉ ghi được 1 lần, Mask ROM cố định từ khi sản xuất."),
  dict(q="Lệnh vi xử lý HLT được xếp vào loại:", en="The processor instruction HLT is classed as:",
       opts=["lệnh điều khiển (control instruction)","lệnh truyền dữ liệu","lệnh logic"], correct=0, src="Tooley Ch.6 Q9",
       explain="HLT dừng CPU, thuộc nhóm lệnh điều khiển hoạt động của bộ xử lý."),
  dict(q="Chuẩn bus VME sử dụng:", en="The VME bus standard uses:",
       opts=["một đầu nối 32-way DIN 41612 duy nhất","hai đầu nối 32-way DIN 41612","đầu nối rìa board 100-way"], correct=1, src="Tooley Ch.6 Q10",
       explain="Chuẩn VMEbus dùng hai đầu nối DIN 41612 (P1 và P2) mỗi đầu 32 hàng chân."),
  dict(q="Loại bộ nhớ nào sử dụng nguyên lý lưu trữ bằng điện tích (charge storage)?", en="What type of memory uses the principle of charge storage:",
       opts=["bipolar static RAM","MOS static memory","MOS dynamic memory"], correct=2, src="Tooley Ch.6 Q11",
       explain="DRAM (MOS dynamic memory) lưu dữ liệu bằng điện tích trên tụ điện của từng ô nhớ, cần refresh định kỳ."),
  dict(q="Cần bao nhiêu IC DRAM loại 16K×4-bit để tạo bộ nhớ 32K byte?", en="How many 16K×4-bit DRAM devices are required to provide 32K bytes of storage:",
       opts=["2","4","8"], correct=1, src="Tooley Ch.6 Q13",
       explain="16K×4bit = 8KB/chip; 32KB ÷ 8KB = 4 chip."),
  dict(q="Chân IC có ký hiệu CAS có chức năng:", en="A memory device has a pin marked CAS. The function of this pin is:",
       opts=["chọn chip hoạt động","tín hiệu điều khiển địa chỉ","chọn địa chỉ cột (column address select)"], correct=2, src="Tooley Ch.6 Q14",
       explain="CAS = Column Address Select, dùng trong DRAM để chốt phần địa chỉ cột."),
  dict(q="Một bộ nhớ bán dẫn gồm 256 hàng và 256 cột có dung lượng là:", en="A semiconductor memory consisting of 256 rows and 256 columns has a capacity of:",
       opts=["256 bit","512 bit","64K bit"], correct=2, src="Tooley Ch.6 Q15",
       explain="256×256 = 65.536 bit = 64K bit."),
  dict(q="Trong lệnh hợp ngữ MOV AX, 07FEh, phần nào là mã lệnh (operation code)?", en="In the assembly language instruction MOV AX, 07FEh, the operation code is:",
       opts=["MOV","AX","07FE"], correct=0, src="Tooley Ch.6 Q16",
       explain="MOV là mã lệnh (opcode); AX là thanh ghi đích, 07FEh là toán hạng dữ liệu."),
  dict(q="Ngăn xếp (stack) được dùng để:", en="The stack is used for:",
       opts=["lưu trữ dữ liệu vĩnh viễn","lưu trữ tạm thời dữ liệu","lưu trữ tạm thời chương trình"], correct=1, src="Tooley Ch.7 Q4",
       explain="Stack dùng lưu tạm địa chỉ trả về, giá trị thanh ghi khi gọi hàm/ngắt."),
  dict(q="Ngăn xếp (stack) thường nằm ở:", en="The stack is a structure located:",
       opts=["trong ALU","trong các thanh ghi đa dụng","trong bộ nhớ đọc/ghi ngoài (external R/W memory)"], correct=2, src="Tooley Ch.7 Q5",
       explain="Stack là một vùng của bộ nhớ RAM ngoài, được quản lý bởi con trỏ stack (SP)."),
  dict(q="Thao tác đảo bit (invert) của một byte dữ liệu được thực hiện bởi:", en="A byte of data is to be inverted. This task is performed by:",
       opts=["ALU","thanh ghi lệnh (instruction register)","bộ giải mã lệnh (instruction decoder)"], correct=0, src="Tooley Ch.7 Q6",
       explain="Phép đảo bit (NOT) là một phép toán logic, do ALU thực hiện."),
  dict(q="Đầu ra của con trỏ lệnh (instruction pointer) xuất hiện trên:", en="The output of the instruction pointer appears on:",
       opts=["address bus","data bus","control bus"], correct=0, src="Tooley Ch.7 Q8",
       explain="Instruction pointer/PC chứa địa chỉ lệnh kế tiếp, đưa ra address bus để CPU nạp lệnh."),
  dict(q="Bộ đệm (buffer) của data bus trong CPU có tính chất:", en="The CPU data bus buffer is:",
       opts=["một chiều (unidirectional)","hai chiều (bidirectional)","đa chiều (omnidirectional)"], correct=1, src="Tooley Ch.7 Q12",
       explain="Data bus cần truyền dữ liệu cả hai chiều (đọc và ghi) nên buffer phải là hai chiều."),
  dict(q="Một tên gọi khác của thanh ghi đóng vai trò con trỏ lệnh (instruction pointer) là:", en="Another way to describe the CPU register that acts as an instruction pointer is:",
       opts=["bộ đếm chương trình (program counter)","con trỏ ngăn xếp (stack pointer)","thanh ghi lệnh (instruction register)"], correct=0, src="Tooley Ch.7 Q13",
       explain="Program Counter (PC) chính là tên gọi khác của instruction pointer."),
  dict(q="Chu kỳ máy nào thực hiện việc nạp và giải mã lệnh (fetch & decode)?", en="In which cycle is an instruction fetched and decoded:",
       opts=["M0","M1","M2"], correct=1, src="Tooley Ch.7 Q14",
       explain="Theo mô tả sách, chu kỳ máy M1 là chu kỳ nạp và giải mã lệnh (opcode fetch)."),
  dict(q="Nếu vi xử lý chạy ở xung nhịp 50MHz, một lệnh cần 11 T-state sẽ thực hiện trong thời gian:", en="If a microprocessor clock runs at 50MHz, an instruction requiring 11 T-states will execute in a time of:",
       opts=["220 ns","440 ns","2.2 µs"], correct=0, src="Tooley Ch.7 Q15",
       explain="Chu kỳ xung nhịp T = 1/50MHz = 20ns; 11 T-state × 20ns = 220ns."),
  dict(q="Một thiết bị ngoại vi thu hút sự chú ý của CPU bằng cách tạo tín hiệu trên đường:", en="An external device can gain the attention of the CPU by generating a signal on the:",
       opts=["R/W line","RESET line","IRQ line"], correct=2, src="Tooley Ch.7 Q16",
       explain="IRQ (Interrupt Request) là đường tín hiệu chuẩn để thiết bị ngoại vi yêu cầu CPU phục vụ ngắt."),
  dict(q="Khi thực thi lệnh hợp ngữ MOV AX, 07FEh, mã lệnh (operation code) được chuyển tới:", en="When executing the instruction MOV AX, 07FEh, the operation code will be transferred to:",
       opts=["accumulator","thanh ghi lệnh (instruction register)","con trỏ lệnh (instruction pointer)"], correct=1, src="Tooley Ch.7 Q17",
       explain="Opcode sau khi nạp được đưa vào thanh ghi lệnh (IR) để giải mã."),
  dict(q="Sau khi thực thi lệnh MOV AX, 07FEh, dữ liệu nhị phân trong thanh ghi AL sẽ là:", en="After executing MOV AX, 07FEh, the binary data in the AL register will be:",
       opts=["11101111","00000111","11111110"], correct=2, src="Tooley Ch.7 Q18",
       explain="AX 16-bit gồm AH (byte cao) và AL (byte thấp); 07FEh → AH=07h, AL=FEh=11111110₂."),
  dict(q="Ưu điểm chính của kỹ thuật pipelining là:", en="The advantage of pipelining is:",
       opts=["lập trình dễ hơn","thực thi nhanh hơn","hoạt động tin cậy hơn"], correct=1, src="Tooley Ch.7 Q19",
       explain="Pipelining cho phép chồng lấn các giai đoạn xử lý lệnh, tăng thông lượng thực thi."),
  dict(q="Kỹ thuật phân đoạn (segmentation) trong vi xử lý họ x86 dùng để:", en="Segmentation is used with x86 processors in order to:",
       opts=["tăng tốc độ xử lý","thiết lập pipeline lệnh","mở rộng phạm vi địa chỉ (addressing range)"], correct=2, src="Tooley Ch.7 Q22",
       explain="Segmentation kết hợp segment+offset giúp CPU 16-bit địa chỉ hoá vùng nhớ lớn hơn khả năng thanh ghi 16-bit thuần tuý."),
]

MOD4_GEN = [
  dict(q="Nếu CPU chạy ở xung nhịp 100MHz, một chu kỳ xung nhịp (T-state) kéo dài:", en="If a CPU runs at 100MHz, one clock period (T-state) lasts:",
       opts=["10 ns","100 ns","1 ns"], correct=0, explain="T = 1/f = 1/100.000.000 = 10ns."),
  dict(q="Một bus dữ liệu 8-bit biểu diễn được giá trị thập phân từ 0 đến:", en="An 8-bit data bus can represent decimal values from 0 to:",
       opts=["255","256","128"], correct=0, explain="2⁸-1 = 255."),
  dict(q="Một bus địa chỉ 16-bit định vị được bao nhiêu ô nhớ khác nhau?", en="A 16-bit address bus can address how many unique memory locations?",
       opts=["65.536","32.768","16.384"], correct=0, explain="2¹⁶ = 65.536."),
  dict(q="ROM được mô tả đúng nhất là:", en="ROM is best described as:",
       opts=["bộ nhớ chỉ đọc, không mất dữ liệu khi mất điện (non-volatile)","bộ nhớ đọc/ghi, mất dữ liệu khi mất điện","bộ nhớ chỉ đọc nhưng mất dữ liệu khi mất điện"], correct=0, explain="ROM là bộ nhớ non-volatile: dữ liệu vẫn còn khi mất điện."),
  dict(q="RAM (bán dẫn thông thường) sẽ mất dữ liệu đã lưu khi nào?", en="RAM loses its stored data when:",
       opts=["mất nguồn điện cấp (volatile)","không bao giờ mất","chỉ sau 24 giờ"], correct=0, explain="RAM là bộ nhớ volatile (dễ bay hơi), mất dữ liệu ngay khi ngắt điện."),
  dict(q="ALU trong CPU chịu trách nhiệm chính cho việc:", en="The ALU is primarily responsible for:",
       opts=["thực hiện các phép toán số học và logic","lưu địa chỉ lệnh kế tiếp","tạo xung clock hệ thống"], correct=0, explain="ALU = Arithmetic Logic Unit, thực hiện cộng/trừ/AND/OR..."),
  dict(q="Thanh ghi bộ đếm chương trình (Program Counter) chứa:", en="The Program Counter (PC) register holds:",
       opts=["địa chỉ của lệnh kế tiếp sẽ thực thi","kết quả phép toán ALU gần nhất","giá trị con trỏ ngăn xếp hiện tại"], correct=0, explain="PC luôn trỏ tới địa chỉ lệnh tiếp theo cần nạp."),
  dict(q="Trong chu trình fetch-decode-execute, bước nào lấy lệnh từ bộ nhớ?", en="In the fetch-decode-execute cycle, which step retrieves the instruction from memory?",
       opts=["fetch (nạp lệnh)","decode (giải mã)","execute (thực thi)"], correct=0, explain="Bước fetch đọc mã lệnh từ ô nhớ được PC trỏ tới."),
  dict(q="Một vi điều khiển thực thi lệnh cần 4 T-state ở xung nhịp 20MHz, thời gian thực thi là:", en="A microcontroller executes an instruction requiring 4 T-states at 20MHz clock; execution time is:",
       opts=["200 ns","80 ns","20 ns"], correct=0, explain="T=1/20MHz=50ns; 4×50ns=200ns."),
  dict(q="Một IC nhớ 16K×8-bit có tổng dung lượng lưu trữ là:", en="A 16K×8-bit memory device has a total storage capacity of:",
       opts=["16 KB","8 KB","32 KB"], correct=0, explain="16K từ × 8 bit/từ = 16K byte = 16KB."),
  dict(q="Bus nào mang tín hiệu định thời và điều khiển xuyên suốt hệ thống máy tính?", en="Which bus carries timing and control signals throughout the computer system?",
       opts=["control bus","address bus","data bus"], correct=0, explain="Control bus mang các tín hiệu điều khiển/định thời (R/W, clock, interrupt...)."),
  dict(q="Một vi xử lý có bus địa chỉ 32-bit định vị trực tiếp được tối đa:", en="A microprocessor with a 32-bit address bus can directly address up to:",
       opts=["4 GB","4 MB","4 TB"], correct=0, explain="2³² byte = 4.294.967.296 byte = 4GB."),
]

MODULES = {
  "01-number-systems": dict(orig=MOD1_ORIG, gen=MOD1_GEN),
  "02-logic-boolean":  dict(orig=MOD2_ORIG, gen=MOD2_GEN),
  "03-ic-multiplexing":dict(orig=MOD3_ORIG, gen=MOD3_GEN),
  "04-computer-cpu":   dict(orig=MOD4_ORIG, gen=MOD4_GEN),
}

def shuffle_positions(items, seed):
    random.seed(seed)
    n = len(items)
    if n == 0: return items
    k = len(items[0]["opts"])
    targets = [i % k for i in range(n)]
    random.shuffle(targets)
    for it, target in zip(items, targets):
        opts = it["opts"]; c = it["correct"]
        correct_val = opts[c]
        others = [o for i, o in enumerate(opts) if i != c]
        random.shuffle(others)
        it["opts"] = others[:target] + [correct_val] + others[target:]
        it["correct"] = target
    return items

def audit(items, label):
    n = len(items)
    if n == 0: return
    long_correct = sum(1 for it in items if len(it["opts"][it["correct"]]) == max(len(o) for o in it["opts"]))
    pos = Counter(it["correct"] for it in items)
    print(f"{label}: n={n}  correct==longest={long_correct}/{n}={long_correct/n*100:.1f}%  vi_tri_dung={dict(pos)}")

out_dir = os.path.join(os.path.dirname(__file__), "quiz")
os.makedirs(out_dir, exist_ok=True)

for slug, d in MODULES.items():
    orig = shuffle_positions(d["orig"], seed=2026)
    gen  = shuffle_positions(d["gen"],  seed=2027)
    audit(orig, f"{slug} [goc-textbook]")
    audit(gen,  f"{slug} [tu-sinh-them]")
    def to_items(lst, lang):
        res = []
        for it in lst:
            qtext = it["q"] if lang == "vi" else it["en"]
            res.append({"q": qtext, "opts": it["opts"], "correct": it["correct"],
                        "explain": it["explain"], "src": it.get("src", "")})
        return res
    for lang in ("vi", "en"):
        payload = {
            "original": to_items(orig, lang),
            "generated": to_items(gen, lang),
        }
        with open(os.path.join(out_dir, f"{slug}.{lang}.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)

print("DONE — wrote quiz JSON to", out_dir)
