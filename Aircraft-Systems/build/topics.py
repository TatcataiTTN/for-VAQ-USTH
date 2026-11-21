# -*- coding: utf-8 -*-
"""Chu de (topic) cua cau hoi theo module. GAN BANG QUY TAC tu khoa tren de + dap an + giai thich (VI va EN gop lai); thu tu quy tac = do uu tien.
Day la phan loai cho Concept finder / loc ngan hang, khong phai nhan do nguoi doc tung cau: moi cau cap nhat o P4 co the dat topic tay bang truong `topic_id` trong data/qsrc.
Cau khong khop quy tac nao roi vao chu de cuoi cung (chung)."""
import re
T = {
 'm01': [
  ('base-conv', 'Đổi cơ số', 'Base conversion', r'chuyển|đổi sang|convert|to binary|to decimal|to hex|to octal|sang nhị phân|sang thập|sang hex|sang bát|repeated division|chia liên tiếp'),
  ('complement', 'Số có dấu, bù 1 và bù 2', 'Signed numbers, 1s and 2s complement', r'bù|complement|signed|có dấu|sign bit|bit dấu|two.s|overflow|tràn'),
  ('float', 'Dấu chấm động', 'Floating point', r'floating|chấm động|ieee|mantissa|exponent|phần định trị|số mũ'),
  ('codes', 'Mã BCD, Gray, ASCII', 'BCD, Gray and ASCII codes', r'bcd|gray|ascii|\bmã\b|\bcode|8421|unicode|ebcdic|excess'),
  ('errors', 'Phát hiện lỗi: parity, checksum, CRC', 'Error detection: parity, checksum, CRC', r'parity|chẵn lẻ|checksum|crc|hamming|error'),
  ('hexoct', 'Bát phân và thập lục phân', 'Octal and hexadecimal', r'hex|octal|bát phân|thập lục|base 8|base 16|cơ số 8|cơ số 16'),
  ('binary', 'Hệ nhị phân và số học nhị phân', 'Binary numbers and arithmetic', r'binary|nhị phân|\bbit\b|\bbyte\b|cộng|trừ|nhân|chia|add|subtract|carry|nhớ|weight|trọng số|msb|lsb'),
  ('aircraft', 'Ứng dụng trên tàu bay', 'Aircraft applications', r'a320|adiru|aircraft|tàu bay|máy bay|arinc|avionic'),
  ('general', 'Khái niệm chung về hệ đếm', 'General number-system concepts', r''),
 ],
 'm02': [
  ('boolean-laws', 'Luật Boolean và De Morgan', 'Boolean laws and De Morgan', r'de ?morgan|luật|law|identity|hấp thụ|absorb|distribut|phân phối|commutat|associat|boolean'),
  ('simplify', 'Tối giản: K-map, SOP, POS', 'Simplification: K-map, SOP, POS', r'karnaugh|k-map|bản đồ|sop|pos|minterm|maxterm|tối giản|simplif|quine|don.t care|không xác định|tích các tổng|tổng các tích'),
  ('gates', 'Cổng logic và bảng chân trị', 'Logic gates and truth tables', r'\band\b|\bor\b|\bnot\b|nand|nor|xor|xnor|cổng|gate|truth table|bảng chân|inverter|đảo'),
  ('combinational', 'Mạch tổ hợp', 'Combinational circuits', r'adder|bộ cộng|comparator|so sánh|half|full|tổ hợp|combinational|7.segment|7 đoạn|decoder|giải mã|parity gen'),
  ('seq', 'Mạch song ổn, đơn ổn, chốt', 'Bistable, monostable and latches', r'latch|flip|bistable|monostable|song ổn|đơn ổn|astable|timer|555|sr |set.reset|clock|xung nhịp|chốt'),
  ('tri', 'Logic ba trạng thái', 'Three-state logic', r'tri.state|ba trạng thái|high.z|trở kháng cao|bus driver|buffer'),
  ('family', 'Họ logic và đặc tính điện', 'Logic families and electrical characteristics', r'ttl|cmos|ecl|họ logic|famil|fan.?out|propagation|trễ|noise margin|biên nhiễu|điện áp mức|v_?ih|v_?il|v_?oh|v_?ol|mức logic|logic level'),
  ('general', 'Khái niệm chung về logic', 'General logic concepts', r''),
 ],
 'm03': [
  ('scale', 'Quy mô tích hợp SSI đến VLSI', 'Integration scale SSI to VLSI', r'ssi|msi|lsi|vlsi|ulsi|quy mô|scale|transistor|số cổng|gate count|tích hợp'),
  ('fan', 'Fan-in, fan-out và đặc tính IC', 'Fan-in, fan-out and IC characteristics', r'fan.?(in|out)|propagation|trễ|power dissip|công suất|noise margin|biên nhiễu|dòng|current|sink|source'),
  ('decoder', 'Bộ giải mã và bộ mã hoá', 'Decoders and encoders', r'decoder|encoder|giải mã|mã hoá|priority|ưu tiên|7.segment|7 đoạn|bcd.to|74138|74148|74147|bộ chọn chip|chip select'),
  ('mux', 'Bộ dồn kênh và phân kênh', 'Multiplexers and demultiplexers', r'multiplex|dồn kênh|demultiplex|phân kênh|data selector|74151|74153|mux|tdm|fdm|chọn dữ liệu|serial'),
  ('adder', 'Bộ cộng, so sánh, parity', 'Adders, comparators, parity', r'adder|bộ cộng|comparator|so sánh|parity|alu|74283|carry|nhớ|half|full'),
  ('aircraft', 'Ứng dụng avionics', 'Avionics applications', r'avionic|aircraft|tàu bay|máy bay|arinc|a320|display|màn hình'),
  ('general', 'Khái niệm chung về IC', 'General IC concepts', r''),
 ],
 'm04': [
  ('memory', 'Bộ nhớ bán dẫn: RAM, ROM, Flash', 'Semiconductor memory: RAM, ROM, flash', r'\bram\b|\brom\b|prom|eprom|eeprom|flash|sram|dram|bộ nhớ|memory|volatile|không bay hơi|address|địa chỉ|dung lượng|capacity|\bkb\b|\bmb\b|byte'),
  ('cpu', 'Kiến trúc bên trong CPU', 'CPU internal architecture', r'cpu|alu|register|thanh ghi|program counter|\bpc\b|accumulator|control unit|khối điều khiển|instruction register|stack|con trỏ|flag|cờ|bus'),
  ('cycle', 'Chu trình lệnh và thời gian', 'Instruction cycle and timing', r'fetch|decode|execute|nhận lệnh|giải mã lệnh|thực thi|chu trình|cycle|clock|xung nhịp|mhz|ghz|pipeline|đường ống|mips|opcode|instruction'),
  ('advanced', 'Kiến trúc nâng cao', 'Advanced architecture', r'risc|cisc|harvard|von neumann|cache|multicore|đa nhân|dsp|asic|fpga|microcontroller|vi điều khiển|embedded|nhúng|interrupt|ngắt|dma'),
  ('structure', 'Cấu trúc hệ máy tính', 'Computer system structure', r'input|output|nhập|xuất|peripheral|ngoại vi|backplane|computer|máy tính|motherboard|i/o|serial|parallel'),
  ('general', 'Khái niệm chung về máy tính', 'General computer concepts', r''),
 ],
 'm05': [
  ('arinc429', 'ARINC 429: điện, từ dữ liệu, label', 'ARINC 429: electrical, word, label', r'429|label|sdi|ssm|bnr|bcd|32.bit|12[,.]5|100 kbps|parity|transmitter|receiver|point.to.point|điểm.điểm|rz|return.to.zero'),
  ('arinc629', 'ARINC 629 và các bus hai chiều', 'ARINC 629 and bidirectional buses', r'629|1553|2 mbps|manchester|terminal|bus controller|bộ điều khiển|bidirectional|hai chiều|command|word|rt\b|bc\b'),
  ('afdx', 'AFDX/ARINC 664, Ethernet', 'AFDX/ARINC 664, Ethernet', r'afdx|664|ethernet|virtual link|switch|chuyển mạch|100 mbps|deterministic|tt-?ethernet|bag|redundan'),
  ('generic', 'Bus chung: USB, I²C, SPI, CAN', 'Generic buses: USB, I2C, SPI, CAN', r'usb|i2c|i²c|spi|\bcan\b|uart|serial|rs-?232|rs-?485|parallel|song song|nối tiếp|firewire|pci|sata|asynchron|bất đồng bộ|baud|simplex|duplex'),
  ('rationale', 'Vì sao dùng bus dữ liệu', 'Why aircraft use data buses', r'bus|wiring|dây|weight|khối lượng|lru|a320|adiru|network|mạng|topology'),
  ('general', 'Khái niệm chung về bus', 'General bus concepts', r''),
 ],
 'm06': [
  ('seven', 'Màn hình 7 đoạn', 'Seven-segment displays', r'7.segment|7 đoạn|seven|led|common (anode|cathode)|anode|cathode|decoder|bcd.to'),
  ('tech', 'Công nghệ hiển thị: CRT, LCD, LED', 'Display technology: CRT, LCD, LED', r'crt|lcd|led|oled|plasma|tft|pixel|điểm ảnh|raster|stroke|resolution|độ phân giải|backlight|nền|colour|màu|contrast|độ tương phản|luminance|độ sáng'),
  ('efis', 'EFIS: PFD và ND', 'EFIS: PFD and ND', r'efis|pfd|\bnd\b|attitude|adi|hsi|primary flight|navigation display|flight director|horizon|tốc độ|speed tape|altitude|độ cao|vor|ils|compass|la bàn'),
  ('ecam', 'EICAS và ECAM', 'EICAS and ECAM', r'eicas|ecam|engine|động cơ|n1|n2|egt|ff|fuel|nhiên liệu|warning|cảnh báo|caution|master|memo|sd page|ewd|crew alert'),
  ('cmc', 'Bảo trì tập trung và ACARS', 'Central maintenance and ACARS', r'cmc|cmcs|cfdiu|bite|acars|maintenance|bảo trì|fault|lỗi|data link|datalink|vhf|printer'),
  ('cockpit', 'Buồng lái và dụng cụ cơ', 'Cockpit and electromechanical instruments', r'cockpit|buồng lái|glass|kính|analogue|analog|tương tự|mechanical|cơ|pitot|static|tĩnh|gyro|con quay|instrument|đồng hồ|layout|bố trí|human|con người|mắt'),
  ('general', 'Khái niệm chung về hiển thị', 'General display concepts', r''),
 ],
 'm07': [
  ('levels', 'Mức nghiêm trọng A đến E', 'Severity levels A to E', r'level|mức|catastrophic|hazardous|major|minor|no effect|thảm hoạ|nguy hiểm|probab|xác suất|10[-⁻]'),
  ('do178', 'DO-178B/C và truy vết', 'DO-178B/C and traceability', r'do-?178|do-?254|do-?160|arinc 653|trace|truy vết|requirement|yêu cầu|certif|chứng nhận|faa|easa|caa|ac 20|partition|phân vùng'),
  ('loading', 'Nạp phần mềm và dữ liệu', 'Loading software and data', r'load|nạp|lsap|fls|dfld|oss|ums|eec|fadec|part number|pdl|data loader|bộ nạp|portable|database|cơ sở dữ liệu|upgrade|nâng cấp|configuration|cấu hình'),
  ('integrity', 'Toàn vẹn dữ liệu: parity, checksum, CRC', 'Data integrity: parity, checksum, CRC', r'parity|checksum|crc|hamming|toàn vẹn|integrity|error|lỗi|modulo|generator|đa thức|remainder|phần dư|xor|cyclic'),
  ('why', 'Vì sao kiểm soát phần mềm', 'Why software is controlled', r'software|phần mềm|safety|an toàn|flight.critical|failure|hỏng'),
  ('general', 'Khái niệm chung', 'General concepts', r''),
 ],
 'm08': [
  ('snell', 'Chiết suất, Snell và phản xạ toàn phần', 'Refractive index, Snell and total internal reflection', r'snell|refract|khúc xạ|chiết suất|critical angle|góc tới hạn|total internal|phản xạ toàn|reflect|θc|theta_c|speed of light|tốc độ ánh sáng'),
  ('na', 'Góc chấp nhận, NA và mode', 'Acceptance angle, NA and modes', r'numerical aperture|\bna\b|acceptance|chấp nhận|mode|v number|v =|normalised|chuẩn hoá|core|lõi|cladding|vỏ|single.mode|đơn mode|multimode|đa mode'),
  ('loss', 'Suy hao, tán sắc và loại sợi', 'Attenuation, dispersion and fibre types', r'attenuation|suy hao|db/km|dispersion|tán sắc|bandwidth|băng thông|step.index|graded|window|cửa sổ|1310|1550|850|loss|budget|ngân sách'),
  ('system', 'Hệ thống truyền thông tin quang', 'Optical communication systems', r'led|laser|photodiode|phototransistor|transmitter|receiver|connector|đầu nối|splice|nối|cable|cáp|avlan|cablan|arinc 636|fddi|bsu|ring|vòng|duplex'),
  ('why', 'Vì sao dùng sợi quang', 'Why aircraft use fibre', r'advantage|ưu điểm|weight|khối lượng|emi|noise|nhiễu|crosstalk|isolat|cách điện|safety|an toàn|infrared|hồng ngoại'),
  ('general', 'Khái niệm chung', 'General concepts', r''),
 ],
 'm09': [
  ('db', 'Đơn vị dB và dBm', 'dB and dBm units', r'\bdb\b|dbm|dbµ|dbuv|dbmv|decibel|gain|độ lợi|khuếch đại|amplifier|suy hao|loss|log'),
  ('spectrum', 'Tín hiệu, phổ Fourier, máy phân tích phổ', 'Signals, Fourier spectrum, spectrum analyser', r'harmonic|hài|fourier|spectrum|phổ|square wave|sóng vuông|aperiodic|periodic|tuần hoàn|random|ngẫu nhiên|pulse|xung|oscilloscope|dao động ký|analyser|analyzer'),
  ('standards', 'Chuẩn EMC và DO-160', 'EMC standards and DO-160', r'do-?160|cispr|iec|61000|rtca|standard|chuẩn|limit|giới hạn|emission|phát xạ|immunity|miễn nhiễm|esd|surge|burst|lisn'),
  ('bonding', 'Nối đất, liên kết, che chắn', 'Grounding, bonding, screening', r'bond|liên kết|ground|nối đất|screen|che chắn|shield|faraday|lightning|sét|hirf|static|tĩnh điện|resistance|điện trở'),
  ('filter', 'Lọc, ferrite, tụ tách', 'Filtering, ferrite, decoupling', r'filter|lọc|ferrite|decoupl|tụ tách|capacitor|tụ|inductor|cuộn|esl|esr|resonan|cộng hưởng|common.mode|chế độ chung|differential|vi sai|low.pass'),
  ('what', 'EMC là gì và nhiễu từ đâu ra', 'What EMC is and where interference comes from', r'emc|emi|interference|nhiễu|coupling|ghép|conduct|bức xạ|radiat|source|nguồn|wi-?fi|crosstalk|xuyên âm|noise|twisted|xoắn'),
  ('general', 'Khái niệm chung', 'General concepts', r''),
 ],
}
TOPICS = {m: [(i, dict(vi=v, en=e), re.compile(p, re.I) if p else None) for i, v, e, p in rows] for m, rows in T.items()}

def classify(mid, text):
    """Tra ve (topic_id, {'vi','en'}) cua quy tac DAU TIEN khop; khong khop -> chu de cuoi (chung)."""
    rows = TOPICS[mid]
    for i, t, rx in rows[:-1]:
        if rx.search(text): return i, t
    i, t, _ = rows[-1]; return i, t
