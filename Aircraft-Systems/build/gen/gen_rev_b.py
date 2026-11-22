# -*- coding: utf-8 -*-
"""Tooley Revision Papers 3, 4, 5 (cac cau con thieu). Khoa in: Appendix 3, B.3 den B.5."""
from gen_rev import R

# ---------------- Paper 3 (1,2,3,7,8,9,10,11,13,14,16,17,19,20) ----------------
R('m06', 3, 1, 'a', 'a', 'efis', 1, 'EADI hiển thị:', 'The EADI displays:',
  [('các góc tư thế chúc ngóc và nghiêng', 'pitch and roll attitudes'), ('hướng bay và radar thời tiết', 'heading and weather radar'), ('chúc ngóc, nghiêng và các điểm đường bay', 'pitch, roll and waypoints')],
  'EADI là đồng hồ chỉ tư thế/director điện tử: hiển thị góc chúc ngóc (pitch) và nghiêng (roll). Hướng bay, điểm đường bay và radar thời tiết thuộc EHSI.',
  'The EADI is the electronic attitude director indicator: it shows pitch and roll. Heading, waypoints and weather radar belong to the EHSI.', ev=['EADI'])
R('m06', 3, 2, 'c', 'c', 'efis', 1, 'Trên EHSI ở chế độ radar thời tiết, cơn bão mạnh được hiển thị là:', 'On an EHSI in weather radar mode, a severe storm would be shown as:',
  [('vùng màu cam có viền đen hoặc vàng', 'orange areas with black or yellow surrounds'), ('vùng xanh dương trên nền trắng', 'blue areas with white background'), ('vùng đỏ có viền đen', 'red areas with black surrounds')],
  'Mã màu radar thời tiết: xanh lá (mưa nhẹ), vàng, đỏ (mưa mạnh/bão dữ dội), magenta (xoáy mạnh nhất). Bão mạnh hiển thị màu đỏ.',
  'Weather radar colour code: green (light rain), yellow, red (heavy rain/severe storm), magenta (most intense turbulence). A severe storm is shown in red.')
R('m05', 3, 3, 'c', 'c', 'general', 2, 'Chi tiết nào trong Hình A2.12 dùng để tránh vấn đề phản xạ và không phối hợp trở kháng:', 'Which feature in Figure A2.12 is used to prevent problems with reflection and mismatch:',
  ['P', 'Q', 'S'], 'S là điện trở chặn cuối (terminator) màu đen ở cuối bus: nó phối hợp trở kháng của cáp nên tín hiệu không bị phản xạ ngược. P là cáp bus, Q là bộ ghép.',
  'S is the black bus terminator at the end of the line: it matches the cable impedance so the signal is not reflected. P is the bus cable and Q the coupler.', fig=12, ev=['terminator'])
R('m06', 3, 7, 'a', 'a', 'ecam', 1, 'Nếu một màn hình EICAS bị hỏng:', 'If one EICAS display fails:',
  [('màn hình CRT còn lại sẽ hiển thị dữ liệu EICAS chính', 'the remaining CRT will display primary EICAS data'), ('CDU của FMS sẽ hiển thị dữ liệu của CRT hỏng', 'the FMS CDU will display the failed CRT data'), ('CRT dự phòng sẽ tự động thay thế', 'the standby CRT will automatically take over')],
  'EICAS có hai màn hình (chính và phụ). Khi một màn hình hỏng, màn hình còn lại hiện dữ liệu động cơ chính; không có CRT dự phòng thứ ba.',
  'EICAS has two displays (primary and secondary). If one fails, the remaining CRT shows the primary engine data; there is no third standby CRT.', ev=['EICAS'])
R('m08', 3, 8, 'c', 'c', 'loss', 1, 'Bước sóng ánh sáng điển hình trong sợi quang là:', 'The typical wavelength of light in an optical fibre is:',
  ['575 nm', '635 nm', ('1.300 nm', '1,300 nm')], 'Đường suy hao theo bước sóng (Hình 10.4) có các cực tiểu ở hồng ngoại gần, quanh 850 nm, 1.300 nm và 1.550 nm, nên sợi dùng các "cửa sổ" đó; 575 nm (vàng) và 635 nm (đỏ) bị suy hao nhiều hơn.',
  'The attenuation-against-wavelength curve (Figure 10.4) has minima in the near infrared, around 850 nm, 1,300 nm and 1,550 nm, so fibre uses those windows; 575 nm (yellow) and 635 nm (red) suffer higher attenuation.', ev=['attenuation in an optical fibre'])
R('m08', 3, 9, 'b', 'b', 'loss', 1, 'Sợi quang đơn mode (monomode) có:', 'A monomode optical fibre has:',
  [('lõi đường kính lớn hơn sợi đa mode', 'a larger diameter core than a multimode fibre'), ('lõi đường kính nhỏ hơn sợi đa mode', 'a smaller diameter core than a multimode fibre'), ('lõi cùng đường kính với sợi đa mode', 'the same diameter core as a multimode fibre')],
  'Sợi đơn mode có lõi chỉ vài micromet nên chỉ cho một mode lan truyền; sợi đa mode có lõi 50 đến 62,5 µm.', 'A monomode fibre has a core of only a few micrometres so only one mode propagates; multimode fibre has a 50 to 62.5 µm core.', ev=['monomode'])
R('m05', 3, 10, 'c', 'c', 'arinc429', 1, 'Từ dữ liệu ARINC 429 cơ bản có độ dài:', 'A basic ARINC 429 data word has a length of:',
  [('8 bit', '8 bits'), ('16 bit', '16 bits'), ('32 bit', '32 bits')], 'Từ ARINC 429 dài 32 bit: nhãn (8), SDI (2), dữ liệu (19), SSM (2), chẵn lẻ (1).', 'An ARINC 429 word is 32 bits: label (8), SDI (2), data (19), SSM (2), parity (1).', ev=['32-bit data words'])
R('m07', 3, 11, 'b', 'b', 'loading', 1, 'Phần mềm điều khiển động cơ điện tử là một ví dụ của:', 'Electronic engine control software is an example of:',
  ['DFLD', 'LSAP', 'OSS'], 'Mục 13.3: phần cứng đích của LSAP (phần mềm nạp được của máy bay) gồm bộ điều khiển động cơ điện tử (EEC), DFDAU, ECU của APU, FGC. DFLD là dữ liệu cơ sở dữ liệu, OSS là phần mềm chọn tuỳ chọn.',
  'Section 13.3: target hardware for LSAP (loadable software aircraft part) includes electronic engine controls (EEC), DFDAU, APU ECUs and flight guidance computers. DFLD is database data and OSS is option-selectable software.', ev=['electronic engine controls'])
R('m05', 3, 13, 'c', 'c', 'arinc429', 2, 'Trường dữ liệu BCD của ARINC 429 nằm trong các bit:', 'The BCD data field of ARINC 429 is contained within bits:',
  ['1–8', '1–10', '11–29'], 'Bit 1 đến 8 là nhãn, 9 đến 10 là SDI, 11 đến 29 là trường dữ liệu (các nhóm 4 bit BCD), 30 đến 31 là SSM, bit 32 là chẵn lẻ.', 'Bits 1 to 8 are the label, 9 to 10 the SDI, 11 to 29 the data field (groups of four BCD bits), 30 to 31 the SSM and bit 32 parity.', ev=['bcd word format'])
R('m05', 3, 14, 'b', 'b', 'arinc429', 1, 'Để tạo liên kết truyền thông hai chiều trong hệ ARINC 429:', 'To create a bidirectional communications link within an ARINC 429 system:',
  [('chỉ cần một kết nối bus dữ liệu', 'only one data bus connection is required'), ('cần hai kết nối bus dữ liệu', 'two data bus connections are required'), ('cần bốn kết nối bus dữ liệu', 'four data bus connections are required')],
  'Một cặp dây xoắn ARINC 429 chỉ có một máy phát nên là một chiều; liên kết hai chiều cần hai bus riêng, mỗi bus một chiều.', 'An ARINC 429 twisted pair has a single transmitter so it is one-way; a two-way link needs two separate buses, one for each direction.', ev=['separate bus connections'])
R('m07', 3, 16, 'c', 'c', 'levels', 1, 'Radar thời tiết là một ví dụ của:', 'Weather radar is an example of:',
  [('phần mềm lớp B', 'Class B software'), ('phần mềm lớp C', 'Class C software'), ('phần mềm lớp D', 'Class D software')],
  'Bảng 13.2: radar thời tiết thuộc mức D (cùng AHRS, CMC/CFDIU, bộ nạp dữ liệu); DME, TCAS, transponder thuộc mức C.', 'Table 13.2: weather radar is level D (with AHRS, CMC/CFDIU and the data loader); DME, TCAS and transponder are level C.', ev=['data loader weather radar'])
R('m12', 3, 17, 'a', 'a', 'gps', 1, 'GPS gồm các phân đoạn (segment) sau:', 'GPS consists of the following segments:',
  [('không gian, người dùng và điều khiển', 'space, user and control'), ('vĩ độ, kinh độ, thời gian', 'latitude, longitude, time'), ('sóng mang, điều chế, mã hoá', 'carrier, modulation, encoding')],
  'GPS gồm ba phân đoạn: không gian (vệ tinh), điều khiển (trạm mặt đất) và người dùng (máy thu).', 'GPS has three segments: space (satellites), control (ground stations) and user (receivers).', ev=['user segment'])
R('m06', 3, 19, 'b', 'b', 'cmc', 1, 'Tín hiệu ACARS được phát ở:', 'ACARS signals are transmitted at:',
  [('HF trong dải 11 MHz đến 14 MHz', 'HF in the range 11 MHz to 14 MHz'), ('VHF trong dải 118 MHz đến 136 MHz', 'VHF in the range 118 MHz to 136 MHz'), ('UHF trong dải 405 MHz đến 420 MHz', 'UHF in the range 405 MHz to 420 MHz')],
  'ACARS dùng liên lạc dữ liệu VHF trong băng hàng không 118 đến 136 MHz (dùng HF hoặc vệ tinh khi ngoài tầm VHF).', 'ACARS uses VHF data link in the 118 to 136 MHz aeronautical band (HF or satellite beyond VHF range).', ev=['ACARS'])
R('m10', 3, 20, 'b', 'b', 'adc', 1, 'Một ưu điểm của ADC hai độ dốc (dual-slope) là:', 'An advantage of a dual-slope ADC is:',
  [('thời gian chuyển đổi nhanh', 'a fast conversion time'), ('khả năng vốn có để khử nhiễu', 'an inherent ability to reject noise'), ('khả năng hoạt động không cần xung nhịp', 'the ability to operate without a clock')],
  'ADC hai độ dốc lấy tích phân tín hiệu nên khử được nhiễu và dao động ngẫu nhiên, nhưng chậm; nó vẫn cần xung nhịp để đếm.', 'A dual-slope ADC integrates the input so it rejects noise and random variation, but it is slow; it still needs a clock for counting.', ev=['rejects noise'])

# ---------------- Paper 4 (1,3,5,6,7,8,9,10,11,14,15,16,17,19; Q20 la cau 'chan DIL' da co, chi doi nhan) ----------------
R('m08', 4, 1, 'a', 'a', 'system', 2, 'Cáp dữ liệu sợi quang là:', 'Fibre-optic data cables are:',
  [('hai chiều (bidirectional)', 'bidirectional'), ('một chiều (unidirectional)', 'unidirectional'), ('simplex', 'simplex')],
  'Cáp dữ liệu sợi quang chứa một cặp sợi (một sợi mỗi chiều) nên liên kết là hai chiều. Lưu ý: "một chiều" và "simplex" là hai từ cùng nghĩa (Tooley tr.170 gọi liên kết một sợi là simplex), nên chúng không thể là đáp án đơn duy nhất; khoá in chọn (a).',
  'A fibre-optic data cable holds a pair of fibres (one per direction) so the link is bidirectional. Note: "unidirectional" and "simplex" mean the same thing (Tooley p.170 calls a single-fibre link simplex), so neither can be the single correct choice; the printed key picks (a).', ev=['simplex'])
R('m04', 4, 3, 'a', 'a', 'memory', 1, 'Ví dụ về thiết bị lưu trữ khối "ghi một lần, đọc nhiều lần" là:', 'An example of a "write once and read many" mass storage device is:',
  [('CD-ROM', 'a CD-ROM'), ('đĩa mềm', 'a floppy disk'), ('RAM động', 'a dynamic RAM')], 'Đĩa quang chỉ ghi được một lần rồi đọc nhiều lần (WORM); đĩa mềm ghi xoá được và RAM động mất dữ liệu khi mất nguồn.',
  'An optical disc is written once and read many times (WORM); a floppy disk is rewritable and dynamic RAM loses its data when power is removed.')
R('m10', 4, 5, 'a', 'a', 'adc', 1, 'Trong bộ chuyển đổi tương tự sang số, điện áp đầu vào:', 'In an analogue to digital converter, the input voltage:',
  [('có thể biến thiên liên tục', 'can vary continuously in voltage level'), ('chỉ có hai mức điện áp', 'can have two possible voltage levels'), ('chỉ có một mức cố định', 'can only have one fixed voltage level')],
  'Tín hiệu tương tự có thể nhận mọi giá trị trong dải; ADC lượng tử hoá nó thành các mã nhị phân rời rạc.', 'An analogue signal can take any value in its range; the ADC quantises it into discrete binary codes.', ev=['analogue to digital'])
R('m09', 4, 6, 'c', 'c', 'what', 1, 'Tương thích điện từ đạt được bằng:', 'Electromagnetic compatibility is achieved by:',
  [('dùng nguồn một chiều đã lọc và ổn áp tốt', 'using smoothed and well-regulated DC supplies'), ('sơn dẫn điện toàn bộ vỏ thiết bị', 'coating all equipment enclosures with conductive paint'), ('che chắn, nối đất, nối đẳng thế và bộ lọc nhiễu', 'shielding, screening, earthing, bonding and interference filtering')],
  'EMC dựa trên tổ hợp nhiều biện pháp: che chắn, nối đất, nối đẳng thế và lọc nhiễu; không biện pháp đơn lẻ nào đủ.', 'EMC comes from a combination of measures: screening, earthing, bonding and filtering; no single measure is enough.', ev=['filtering'])
R('m06', 4, 7, 'c', 'c', 'cockpit', 2, 'Màn hình trong Hình A2.15 là:', 'The display shown in Figure A2.15 is:',
  ['EICAS', 'EFIS PED', 'FMS CDU'], 'Ảnh có bàn phím chữ-số và các phím chọn dòng cạnh màn hình menu (CFDS, báo cáo hệ thống): đây là CDU của FMS, không phải màn hình EICAS hay bảng điều khiển EFIS.',
  'The photo shows an alphanumeric keypad and line-select keys beside a menu screen (CFDS, system report): this is the FMS CDU, not an EICAS display or an EFIS control panel.', fig=15, ev=['CDU'])
R('m05', 4, 8, 'a', 'a', 'arinc629', 1, 'Cáp bus dữ liệu ARINC 629 dùng:', 'An ARINC 629 data bus cable uses:',
  [('một cặp dây xoắn', 'a pair of twisted wires'), ('một dây đơn và mass', 'a single wire and ground'), ('cáp đồng trục có một lõi bọc kim', 'a coaxial cable with a single screened conductor')],
  'Bus ARINC 629 là cặp dây xoắn có bọc chống nhiễu nối qua bộ ghép dòng điện; không dùng dây đơn hay cáp đồng trục.', 'The ARINC 629 bus is a screened twisted pair coupled through current couplers; it is neither a single wire nor a coaxial cable.', ev=['ARINC 629'])
R('m08', 4, 9, 'c', 'c', 'loss', 1, 'Suy hao trong cáp dữ liệu sợi quang tăng khi:', 'Losses in optical fibre data cables increase when:',
  [('dùng tốc độ dữ liệu thấp', 'a low data rate is used'), ('cáp được giữ càng ngắn càng tốt', 'the cable is kept as short as possible'), ('cáp bị uốn quanh bán kính nhỏ', 'the cable is bent around a small radius')],
  'Uốn cong gấp làm một phần ánh sáng vượt góc tới hạn và thoát ra khỏi lõi (suy hao uốn); cáp ngắn thì suy hao nhỏ đi, tốc độ dữ liệu không ảnh hưởng.', 'A tight bend makes part of the light exceed the critical angle and escape the core (bend loss); a shorter cable lowers the loss and the data rate does not matter.', ev=['bend'])
R('m08', 4, 10, 'b', 'b', 'snell', 1, 'Cáp sợi quang dùng:', 'Fibre-optic cables use:',
  [('lớp bọc phản xạ', 'a reflective cladding'), ('lớp bọc có chiết suất (refractive cladding)', 'a refractive cladding'), ('lớp bọc đục', 'an opaque cladding')],
  'Lớp bọc trong suốt có chiết suất thấp hơn lõi, nhờ đó ánh sáng bị phản xạ toàn phần ở mặt phân cách; đó là lớp bọc khúc xạ.', 'The cladding is transparent with a lower refractive index than the core so light undergoes total internal reflection at the boundary: a refractive cladding.', ev=['cladding'])
R('m06', 4, 11, 'a', 'a', 'tech', 1, 'Màn hình LCD dùng loại nguồn nào:', 'An LCD uses what type of power supply:',
  [('điện áp xoay chiều', 'AC voltage'), ('dòng một chiều giới hạn dòng', 'current-limited DC current'), ('điện áp một chiều giới hạn điện áp', 'voltage-limited DC voltage')],
  'LCD được kích bằng điện áp xoay chiều; dòng một chiều làm tinh thể lỏng bị phân cực và suy giảm nhanh.', 'An LCD is driven by an AC voltage; direct current would polarise the liquid crystal and degrade it quickly.', ev=['LCD'])
R('m12', 4, 14, 'c', 'c', 'fms', 1, 'Cơ sở dữ liệu vận hành của FMS có thể phải sửa đổi trong chuyến bay:', 'The operational data base of the FMS may have to be modified in flight:',
  [('bởi phi công', 'by the pilot'), ('tự động bởi DADC', 'automatically by the DADC'), ('không thể sửa đổi trong chuyến bay', 'it cannot be modified in flight')],
  'Cơ sở dữ liệu dẫn đường vận hành được cập nhật trên mặt đất theo chu kỳ (thường 28 ngày); phi công chỉ thêm điểm vào cơ sở dữ liệu riêng, không sửa dữ liệu vận hành khi bay.', 'The operational navigation database is updated on the ground on a cycle (typically 28 days); the pilot can only add waypoints to a separate pilot database and cannot change the operational data in flight.', ev=['database'])
R('m06', 4, 15, 'b', 'b', 'efis', 1, 'Trên hệ EFIS, radar thời tiết được hiển thị trên:', 'On an EFIS system the weather radar is displayed on:',
  [('EADI', 'the EADI'), ('EHSI', 'the EHSI'), ('CDU của FMC', 'the FMC CDU')], 'Radar thời tiết phủ lên bản đồ điều hướng nên hiển thị trên EHSI (ND); EADI chỉ báo tư thế.', 'Weather radar is overlaid on the navigation map, so it appears on the EHSI (ND); the EADI shows attitude.', ev=['weather radar'])
R('m06', 4, 16, 'b', 'b', 'cmc', 1, 'Một phương pháp dùng trong máy bay hiện đại để báo lỗi trong chuyến bay cho trạm kỹ thuật và giám sát mặt đất là:', 'A method used in modern aircraft for reporting in-flight faults to an engineering and monitoring ground station is:',
  ['TCAS II', 'ACARS', 'TAWS'], 'ACARS truyền dữ liệu bảo dưỡng và báo cáo lỗi xuống mặt đất; TCAS tránh va chạm, TAWS cảnh báo địa hình.', 'ACARS sends maintenance data and fault reports to the ground; TCAS avoids collisions and TAWS warns of terrain.', ev=['ACARS'])
R('m06', 4, 17, 'b', 'b', 'tech', 1, 'So với LCD, màn hình CRT có ưu điểm là:', 'When compared with an LCD, a CRT display offers the advantage that:',
  [('độ phân giải và độ nét tốt hơn', 'the resolution and focus are better'), ('có thể nhìn ở góc rộng', 'it can be viewed over a large angle'), ('dùng điện áp thấp và tiết kiệm năng lượng hơn', 'it uses low voltages and is more energy efficient')],
  'CRT nhìn được ở góc rất rộng; LCD bị hạn chế góc nhìn. Điện áp thấp và tiết kiệm điện là ưu điểm của LCD.', 'A CRT can be viewed over a very wide angle whereas an LCD has a limited viewing angle; low voltage and energy saving favour the LCD.', ev=['viewing angle'])
R('m03', 4, 19, 'b', 'b', 'mux', 2, 'Sắp xếp logic trong Hình A2.18 (hai cổng đảo cho A và B, các cổng AND chọn theo tổ hợp A, B và các đường dữ liệu, rồi một cổng OR ra Y) hoạt động như:', 'The logic arrangement shown in Figure A2.18 acts as:',
  [('bộ giải mã', 'a decoder'), ('bộ dồn kênh (multiplexer)', 'a multiplexer'), ('thanh ghi dịch', 'a shift register')],
  'A và B (cùng dạng đảo) làm đầu vào chọn; mỗi cổng AND cho qua một đường dữ liệu khi tổ hợp chọn tương ứng, cổng OR gộp lại thành một đầu ra Y: đó là bộ dồn kênh. Bộ giải mã có nhiều đầu ra, thanh ghi dịch cần phần tử nhớ.',
  'A and B (true and inverted) are the select inputs; each AND gate passes one data line for its select code and the OR gate merges them into one output Y: a multiplexer. A decoder has many outputs and a shift register needs memory elements.', fig=18, ev=['multiplexer'])

# ---------------- Paper 5 (1,2,5,9,11,12,13,14,15,16,17,18,19,20) ----------------
R('m06', 5, 1, 'c', 'c', 'cockpit', 1, 'Tốc độ lên (rate of climb) được chỉ báo bởi:', 'Rate of climb is indicated by the:',
  [('đồng hồ độ cao', 'altimeter'), ('HSI', 'HSI'), ('VSI', 'VSI')], 'Chỉ báo tốc độ thẳng đứng (VSI) cho tốc độ lên/xuống; đồng hồ độ cao chỉ độ cao, HSI chỉ hướng và dẫn đường.', 'The vertical speed indicator (VSI) shows rate of climb or descent; the altimeter shows height and the HSI shows heading and navigation.', ev=['VSI'])
R('m06', 5, 2, 'c', 'c', 'ecam', 1, 'Hệ thống điện tử hàng không nào có thể hiển thị dữ liệu động cơ:', 'Which one of the following avionic systems is capable of displaying engine data:',
  ['AFCS', 'EADI', 'EICAS'], 'EICAS (hệ chỉ báo động cơ và cảnh báo tổ lái) hiển thị thông số động cơ; AFCS là lái tự động, EADI là chỉ báo tư thế.', 'EICAS (engine indicating and crew alerting system) displays engine parameters; AFCS is the autopilot system and EADI the attitude indicator.', ev=['EICAS'])
R('m05', 5, 5, 'a', 'a', 'general', 1, 'Để giảm thiểu ảnh hưởng của phản xạ do không phối hợp trở kháng, cáp bus nên:', 'In order to minimise the effect of reflections caused by a mismatch, a bus cable should be:',
  [('được kết cuối ở mỗi đầu', 'terminated at each end'), ('giữ càng ngắn càng tốt', 'kept as short as possible'), ('gắn bộ lặp (repeater) đều đặn', 'fitted with repeaters at regular intervals')],
  'Điện trở kết cuối bằng trở kháng đặc tính ở hai đầu hấp thụ sóng tới, nên không có phản xạ ngược.', 'A terminator equal to the characteristic impedance at each end absorbs the incident wave so nothing reflects back.', ev=['terminator'])
R('m08', 5, 9, 'a', 'a', 'loss', 1, 'Lõi của sợi quang đơn mode có đường kính điển hình là:', 'The core of a monomode optical fibre has a typical diameter of:',
  ['5 µm', '25 µm', '50 µm'], 'Lõi sợi đơn mode cỡ 5 đến 10 µm; 25 µm và 50 µm thuộc sợi đa mode. (Bản OCR của đề in "µm" thành "m/w/y".)', 'A monomode core is about 5 to 10 µm; 25 µm and 50 µm belong to multimode fibre. (The OCR of the paper prints "µm" as "m/w/y".)', ev=['monomode'])
R('m07', 5, 11, 'b', 'b', 'levels', 2, 'Ứng dụng phần mềm máy bay nào sau đây có mức độ quan trọng (criticality) cao nhất:', 'Which one of the following aircraft software applications has the highest level of criticality:',
  ['DME', 'GPS', 'WXR'], 'Bảng 13.2: dẫn đường vệ tinh (GPS) ở mức B, DME ở mức C, radar thời tiết (WXR) ở mức D; mức B quan trọng hơn C và D.', 'Table 13.2: satellite navigation (GPS) is level B, DME level C and weather radar (WXR) level D; B is more critical than C and D.', ev=['satnav voradf'])
R('m12', 5, 12, 'a', 'a', 'test', 1, 'Giám sát thời gian thực các hệ thống quan trọng là chức năng của:', 'Real-time monitoring of critical systems is a function of:',
  ['BITE', 'FMS', 'EFIS'], 'BITE (kiểm tra tích hợp sẵn) liên tục giám sát và báo lỗi các hệ thống quan trọng; FMS quản lý chuyến bay, EFIS hiển thị.', 'BITE (built-in test equipment) continuously monitors critical systems and reports faults; FMS manages the flight and EFIS displays data.', ev=['BITE'])
R('m13', 5, 13, 'c', 'c', 'afdx', 1, 'Kiến trúc mạng cơ bản dùng trong mạng AFDX là:', 'The fundamental network architecture used in an AFDX network is:',
  [('bus', 'bus'), ('cây', 'tree'), ('sao tầng (cascaded star)', 'cascaded star')], 'AFDX dùng các bộ chuyển mạch nối tầng với mỗi hệ thống đầu cuối nối vào một chuyển mạch: sao tầng.', 'AFDX uses cascaded switches with each end system attached to one switch: a cascaded star.', ev=['cascaded star'])
R('m13', 5, 14, 'b', 'b', 'frame', 1, 'Trong mạng AFDX, các khung ethernet của một liên kết ảo (virtual link) có thể xuất phát từ:', 'Within an AFDX network, the ethernet frames associated with a particular virtual link can originate at:',
  [('nhiều hệ thống đầu cuối', 'multiple end systems'), ('một và chỉ một hệ thống đầu cuối', 'one, and only one, end system'), ('mọi hệ thống đầu cuối trong mạng', 'each end system present in the network')],
  'Liên kết ảo là đường một chiều từ đúng một hệ thống đầu cuối nguồn tới một hoặc nhiều đích, vì thế khung của nó có một nguồn duy nhất.', 'A virtual link is a one-way path from exactly one source end system to one or more destinations, so its frames have a single origin.', ev=['virtual link'])
R('m13', 5, 15, 'c', 'c', 'afdx', 1, 'Trong mạng AFDX, các liên kết từ mỗi máy chủ đến bộ chuyển mạch là:', 'In an AFDX network the links from each host to the switch are:',
  [('simplex', 'simplex'), ('bán song công', 'half-duplex'), ('song công toàn phần', 'full-duplex')], 'Mỗi liên kết gồm hai cặp xoắn (Tx và Rx) cho truyền và nhận đồng thời: song công toàn phần.', 'Each link has two twisted pairs (Tx and Rx) for simultaneous send and receive: full-duplex.', ev=['full-duplex link'])
R('m13', 5, 16, 'b', 'b', 'afdx', 2, 'Khoảng cách phân bổ băng thông (BAG) tối đa cho một liên kết ảo cấp 250 thông điệp mỗi giây là bao nhiêu:', 'What is the maximum bandwidth allocation gap for a virtual link that supplies messages at a rate of 250 per second:',
  ['2 ms', '4 ms', '8 ms'], '250 thông điệp/s nghĩa là chu kỳ 1/250 = 4 ms. BAG phải ≤ chu kỳ này và là luỹ thừa của 2 ms (1, 2, 4, 8, … 128 ms): lớn nhất là 4 ms.', '250 messages per second is a period of 1/250 = 4 ms. The BAG must not exceed it and must be a power of two in ms (1, 2, 4, 8 … 128 ms): the largest is 4 ms.', ev=['bandwidth allocation gap'])
R('m14', 5, 17, 'a', 'a', 'entity', 1, 'Kiểu logic chuẩn VHDL "L" là:', 'The VHDL standard logic type L is:',
  [('mức thấp yếu (weak low)', 'a weak low'), ('logic 0 cưỡng bức', 'a forcing logic 0'), ('trạng thái logic chưa khởi tạo', 'an uninitialised logic state')],
  'std_logic có chín giá trị: U (chưa khởi tạo), X (cưỡng bức không xác định), 0 (cưỡng bức 0), 1, Z, W, L (thấp yếu), H (cao yếu), - (không quan tâm).', 'std_logic has nine values: U (uninitialised), X (forcing unknown), 0 (forcing 0), 1, Z, W, L (weak low), H (weak high) and - (don\'t care).', ev=['std_logic'])
R('m14', 5, 18, 'b', 'b', 'entity', 1, 'Trong mã VHDL, kiểu dữ liệu Boolean có thể nhận các giá trị:', 'In VHDL code a Boolean data type can have values:',
  [('0 và 1', '0 and 1'), ('FALSE và TRUE', 'FALSE and TRUE'), ('thấp và cao', 'low and high')], 'BOOLEAN của VHDL là kiểu liệt kê (FALSE, TRUE); 0/1 và thấp/cao thuộc kiểu BIT hoặc STD_LOGIC.', 'VHDL BOOLEAN is the enumerated type (FALSE, TRUE); 0/1 and low/high belong to BIT or STD_LOGIC.', ev=['boolean'])
R('m14', 5, 19, 'a', 'a', 'ops', 2, 'Khi X = 011 và Y = 110 thì biểu thức VHDL X AND NOT Y có giá trị:', 'When X = 011 and Y = 110 the VHDL expression X AND NOT Y will evaluate to:',
  ['001', '110', '010'], 'NOT Y = NOT 110 = 001; X AND 001 = 011 AND 001 = 001 (NOT có độ ưu tiên cao hơn AND).', 'NOT Y = NOT 110 = 001; X AND 001 = 011 AND 001 = 001 (NOT binds tighter than AND).')
R('m14', 5, 20, 'c', 'c', 'ops', 1, 'Phương án nào cho thứ tự ưu tiên của các toán tử VHDL (cao nhất trước):', 'Which one of the following gives the order of precedence of VHDL operators (highest first):',
  [('logic; quan hệ; dịch', 'logical; relational; shift'), ('quan hệ; logic; dịch', 'relational; logical; shift'), ('dịch; quan hệ; logic', 'shift; relational; logical')],
  'Từ cao đến thấp: toán tử dịch (sll, srl…), quan hệ (=, /=, <…), rồi logic (and, or, nand…). Toán tử logic có độ ưu tiên thấp nhất.', 'Highest to lowest: shift (sll, srl …), relational (=, /=, < …) and then logical (and, or, nand …). Logical operators bind loosest.', ev=['precedence'])
