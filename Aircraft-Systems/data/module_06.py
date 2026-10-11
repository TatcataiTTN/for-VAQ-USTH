# -*- coding: utf-8 -*-
"""Noi dung module 06 (VI + EN): Man hinh dien tu va he thong thong tin buong lai (EFIS/EIS, ECAM/EICAS, ACARS).
Nguon: bai giang "Electronic displays - ver 2026" (36 slide) + Tooley Ch.1, Ch.11, Ch.15 (15.1-15.3) + Floyd Ch.4 (Applied Logic) va Ch.6 (7-segment)."""

MOD06 = {
  "slug": "06-electronic-displays",
  "num": "06",
  "target_slides": 47,
  "vi": {
    "title": "Màn hình điện tử và hệ thống thông tin buồng lái",
    "tag": "Electronic Displays",
    "src": "Tooley ch.1, ch.11, ch.15 (mục 15.1 đến 15.3) · Floyd ch.4 (Applied Logic) và ch.6 (7 đoạn) · Bài giảng \"Electronic displays\" (36 slide)",
    "intro": "Màn hình là điểm cuối của mọi chuỗi dữ liệu trên máy bay: số đo từ cảm biến, ADIRU hay máy tính hệ thống cuối cùng phải đến mắt phi công qua một mặt kính. Module này đi từ lịch sử buồng lái và yêu cầu đối với hệ thống hiển thị, qua các công nghệ CRT, LED 7 đoạn và LCD (kèm các phép tính độ phân giải, quét raster và giải mã 7 đoạn), đến hệ thống EFIS/EIS (PFD, ND) và ECAM/EICAS trên Airbus A320, rồi kết thúc bằng bảo trì tập trung (CMC) và ACARS.",
    "parts": [
      {"title": "Từ đồng hồ cơ đến buồng lái kính",
       "bullets": [
         "Buồng lái đi từ không có đồng hồ (1903) đến hàng trăm đồng hồ analog (thập niên 1960 và 1970), rồi đến vài màn hình lớn",
         "Mỗi thế hệ Airbus (A310, A320, A380, A350) thay thêm đồng hồ cơ bằng màn hình đa chức năng",
         "Hệ thống hiển thị phải đáp ứng yêu cầu hiệu năng, nhân tố con người, an toàn và chứng nhận (DO-160, DO-178, DO-254)",
         "Kiến trúc đi từ monobloc, qua segregated, đến integrated modular"]},
      {"title": "Công nghệ hiển thị và thị giác con người",
       "bullets": [
         "Kích thước điểm ảnh không nhìn thấy được phụ thuộc thị lực 1 phút cung: h ≈ D·θ",
         "CRT: súng điện tử, lưới điều khiển độ sáng, anode, quét raster bằng tín hiệu răng cưa",
         "LED 7 đoạn cần bộ giải mã (BCD sang 7 đoạn, ví dụ 74HC47); LCD không tự phát sáng",
         "AMLCD dùng transistor màng mỏng (TFT) cho từng điểm ảnh, vượt CRT về khối lượng, công suất, thể tích và độ tin cậy"]},
      {"title": "EFIS và EIS: PFD, ND",
       "bullets": [
         "EFIS gồm PFD (tư thế, tốc độ, độ cao) và ND (mặt phẳng ngang, định hướng, radar thời tiết)",
         "Airbus đi từ CRT 5x5 inch (A310), CRT 6x6 inch (A320), đến LCDU 725 và EDU 725",
         "Trên A320, DMC tạo hình ảnh cho PFD, ND, ECAM; FWC tạo cảnh báo; SDAC thu dữ liệu hệ thống",
         "Ba bộ tạo ký hiệu (symbol generator): trái, phải và giữa (dự phòng)"]},
      {"title": "ECAM và EICAS: giám sát động cơ và hệ thống",
       "bullets": [
         "ECAM của Airbus và EICAS của Boeing là hai tên gọi cho cùng một ý tưởng: gom thông số động cơ, hệ thống và cảnh báo lên hai màn hình",
         "Màn hình trên (E/WD) hiển thị động cơ và cảnh báo; màn hình dưới (SD) hiển thị trang hệ thống (PRESS, ELEC, HYD, FUEL, COND, F/CTL)",
         "N1 là tốc độ quạt (cụm áp thấp), N2 là tốc độ cụm áp cao; EPR, EGT và lưu lượng nhiên liệu đi kèm",
         "Mỗi trang đọc theo màu: xanh lá bình thường, hổ phách (amber) thận trọng, đỏ giới hạn"]},
      {"title": "Bảo trì tập trung (CMC) và ACARS",
       "bullets": [
         "CMC thu dữ liệu lỗi từ mọi LRU qua ARINC 429, có hai máy (một hoạt động, một dự phòng) và đồng hồ gắn thời gian",
         "MCDU, máy in và ACARS là ba đường đưa dữ liệu bảo trì ra ngoài CMC",
         "ACARS là liên kết dữ liệu VHF (129 đến 137 MHz) giữa máy bay và mặt đất, bản tin OOOI, FMS, bảo trì",
         "Mọi con số trên các trang ECAM trong bài giảng cần được đọc có phản biện, một số giá trị minh hoạ không khớp lý thuyết"]},
    ],
    "formula_label": "Kích thước điểm ảnh không nhìn thấy và tần số quét raster",
    "formula_math": "h ≈ D · θ  (θ = 1' = (1/60)° = 2,91×10⁻⁴ rad; D = 5 m ⇒ h ≈ 1,45 mm)<br>f_X = N_dòng · f_Y  (400 dòng, f_Y = 100 Hz ⇒ f_X = 40 kHz)",
    "legend": [
      ["h", "kích thước điểm ảnh nhỏ nhất mà mắt người chưa phân biệt được ở khoảng cách D"],
      ["D", "khoảng cách từ mắt đến màn hình"],
      ["θ", "thị lực của mắt, 1 phút cung (1/60 độ), tính bằng radian"],
      ["N_dòng", "số dòng quét của một khung hình"],
      ["f_Y", "tần số răng cưa quét dọc (một khung hình mỗi chu kỳ)"],
      ["f_X", "tần số răng cưa quét ngang, bằng N_dòng nhân f_Y"],
    ],
    "history_title": "📜 Bối cảnh lý thuyết và lịch sử",
    "history": "Theo sách Tooley, ngoài đồng hồ cơ, đèn sợi đốt và đồng hồ cuộn dây chuyển động, CRT là công nghệ hiển thị lâu đời nhất còn dùng trên máy bay; nó vẫn cho độ sáng rất cao và góc nhìn rộng. Tuy vậy xu hướng chung là thay bằng AMLCD (màn hình tinh thể lỏng ma trận chủ động), nhẹ hơn, ít tốn điện, nhỏ hơn và tin cậy hơn, đồng thời cho phép một thiết bị phức tạp nằm gọn trong một hộp duy nhất. Bài giảng của môn kể cùng câu chuyện qua mốc thời gian buồng lái: Wright Flyer 1903 không có đồng hồ nào; khoảng 10 đồng hồ vào 1918; khoảng 600 đồng hồ ở buồng lái \"conventional\" năm 1969; CRT vào những năm 1990; và màn hình LCD lớn, cảm ứng ở A350 và Boeing 787 ngày nay. Với Airbus, trình tự là A310 (1978, màn hình đa chức năng đầu tiên), A320 (1988, sáu màn hình CRT), A380 (2007, AMLCD và IMA) và A350 (2015, màn hình lớn có cảm ứng).",
    "case_title": "🔎 Case study: đường đi của một con số tốc độ từ ADIRU đến điểm ảnh trên PFD A320",
    "case": "ADIRU đo và tính các tham số khí động, rồi phát lên bus ARINC 429 (Module 05). DMC (Display Management Computer) nhận dữ liệu, tính ký hiệu và hình ảnh cho PFD, ND và ECAM; FWC bổ sung cảnh báo, SDAC bổ sung dữ liệu hệ thống. Dữ liệu định dạng đi tới LCDU 725 qua bus tốc độ cao; trong LCDU, mô-đun tiền xử lý định dạng dữ liệu, mô-đun xử lý đồ hoạ vẽ ký hiệu và văn bản, mô-đun LCD (có mạch điều khiển) bật từng điểm ảnh còn mô-đun đèn nền chiếu sáng. Mỗi điểm ảnh gồm ba điểm con đỏ, lục, lam; nếu mỗi kênh màu có 256 mức thì một điểm ảnh biểu diễn được 256³ = 16 777 216 màu, khớp với \"hơn 16 triệu màu\" trong sách Tooley (mục 11.3.3, tự kiểm chứng trong notebook). Phi công đọc kết quả trên thước tốc độ của PFD: số trong ô xanh lá là tốc độ hiện tại, cờ vàng là tốc độ chọn.",
    "warn_title": "⚠️ Bẫy hay gặp (và các điểm cần đọc có phản biện trong bài giảng)",
    "warn": "Bẫy chung: nhầm N1 với N2. Slide E/WD của bài giảng ghi N2 là \"tốc độ tuabin áp thấp\" trong khi cùng slide ghi N1 là cụm áp thấp; Tooley (mục 1.1.6) ghi rõ N1 là tốc độ quạt, N2 là tốc độ tuabin áp cao, nên N2 phải là áp cao. Slide ACARS ghi SDAC là \"System Data Analog Computer\" nhưng slide sơ đồ EIS ghi \"System Data Acquisition Concentrator\" (tên đúng theo mô tả chức năng là thu thập dữ liệu). Slide ELEC của ECAM vẽ máy phát \"420 V, 200 Hz\" trong khi nguồn xoay chiều máy bay là 115 V, 400 Hz (Tooley nhắc nguồn 115 V AC 400 Hz). Slide PRESS ở FL140 ghi chênh áp 2,9 psi cùng độ cao cabin 2 870 ft; tính bằng khí quyển chuẩn ISA thì chênh áp phải khoảng 4,6 psi (xem notebook), nên đây chỉ là số minh hoạ, đừng học thuộc. Trên slide ND, \"23 33\" được dán nhãn là thời gian đến điểm bay (23 phút 33 giây), nhưng 37 NM ở tốc độ mặt đất 257 kt chỉ mất khoảng 8,6 phút; nhiều khả năng đó là giờ dự kiến đến (ETA) theo giờ UTC, chưa kiểm chứng với tài liệu hãng nên ghi là nghi vấn. Slide A310 ghi \"EICAS\" nhưng theo Tooley, tên của Airbus là ECAM. Cuối cùng, một lỗi in thật trong sách Tooley: khoá đáp án chương 11 ghi câu 4 là (a), nhưng mắt người nhạy nhất với ánh sáng lục (cực đại khoảng 550 nm, đúng như câu 2 và slide 6), nên đáp án đúng là (c); site dùng đáp án đúng và ghi chú rõ. Về Floyd: đáp án in của Bài 67, chương 4 (mạch ở Hình P-19) làm chữ A không sáng được đoạn a (kiểm tra bảng chân trị đầy đủ), nên không dùng làm đáp án chuẩn.",
    "notebook_desc": "Notebook đi kèm: tính kích thước điểm ảnh theo thị lực, tần số quét raster, giải mã 7 đoạn và các biểu thức tối giản của Floyd bằng sympy, mô phỏng zero suppression của 74HC47, kiểm tra các con số trên slide ECAM (nhiên liệu, chênh áp ISA, thời gian đến điểm bay) và chạy lại các câu trắc nghiệm có thể tính được."
  },
  "en": {
    "title": "Electronic Displays and Flight Deck Information Systems",
    "tag": "Electronic Displays",
    "src": "Tooley ch.1, ch.11, ch.15 (sections 15.1 to 15.3) · Floyd ch.4 (Applied Logic) and ch.6 (7-segment) · Lecture \"Electronic displays\" (36 slides)",
    "intro": "A display is the last link of every data chain in an aircraft: whatever a sensor, the ADIRU or a system computer measures must finally reach the pilot's eye through a sheet of glass. This module goes from cockpit history and display system requirements, through CRT, 7-segment LED and LCD technology (with resolution, raster scanning and 7-segment decoding calculations), to the EFIS/EIS (PFD, ND) and the ECAM/EICAS on the Airbus A320, and ends with centralised maintenance (CMC) and ACARS.",
    "parts": [
      {"title": "From mechanical dials to the glass cockpit",
       "bullets": [
         "Cockpits went from no instruments at all (1903) to hundreds of analogue dials (1960s and 1970s), then to a few large screens",
         "Each Airbus generation (A310, A320, A380, A350) replaced more mechanical dials with multifunction displays",
         "A display system must satisfy performance, human factors, safety and certification requirements (DO-160, DO-178, DO-254)",
         "Architectures progressed from monobloc, through segregated, to integrated modular"]},
      {"title": "Display technology and human vision",
       "bullets": [
         "The smallest invisible pixel size follows from 1 arcminute visual acuity: h ≈ D·θ",
         "CRT: electron gun, brightness-controlling grid, anodes, raster scan driven by sawtooth waveforms",
         "7-segment LEDs need a decoder (BCD to 7-segment, for example the 74HC47); an LCD does not emit light",
         "AMLCD uses a thin-film transistor (TFT) per pixel and beats CRT on weight, power, volume and reliability"]},
      {"title": "EFIS and EIS: PFD, ND",
       "bullets": [
         "EFIS comprises the PFD (attitude, airspeed, altitude) and the ND (horizontal situation, navigation, weather radar)",
         "Airbus went from 5x5 inch CRT (A310) and 6x6 inch CRT (A320) to the LCDU 725 and EDU 725",
         "On the A320 the DMC generates the PFD, ND and ECAM images; the FWC generates warnings; the SDAC collects system data",
         "Three symbol generators: left, right and a centre one as backup"]},
      {"title": "ECAM and EICAS: monitoring engines and systems",
       "bullets": [
         "Airbus ECAM and Boeing EICAS are two names for the same idea: engine data, systems data and alerts on two screens",
         "The upper screen (E/WD) shows engines and warnings; the lower screen (SD) shows system pages (PRESS, ELEC, HYD, FUEL, COND, F/CTL)",
         "N1 is fan (low pressure spool) speed, N2 is the high pressure spool speed; EPR, EGT and fuel flow accompany them",
         "Each page is read by colour: green normal, amber caution, red limit"]},
      {"title": "Centralised maintenance (CMC) and ACARS",
       "bullets": [
         "The CMC collects fault data from every LRU over ARINC 429; there are two units (one active, one standby) and a time-stamping clock",
         "The MCDU, the printer and ACARS are the three ways to get maintenance data out of the CMC",
         "ACARS is a VHF data link (129 to 137 MHz) between aircraft and ground carrying OOOI, FMS and maintenance messages",
         "Numbers shown on the ECAM pages in the lecture deserve a critical reading: some illustrative values do not match the theory"]},
    ],
    "formula_label": "Invisible pixel size and raster scan frequency",
    "formula_math": "h ≈ D · θ  (θ = 1' = (1/60)° = 2.91×10⁻⁴ rad; D = 5 m ⇒ h ≈ 1.45 mm)<br>f_X = N_lines · f_Y  (400 lines, f_Y = 100 Hz ⇒ f_X = 40 kHz)",
    "legend": [
      ["h", "smallest pixel size the eye cannot yet resolve at distance D"],
      ["D", "distance from the eye to the screen"],
      ["θ", "visual acuity of the eye, 1 arcminute (1/60 degree), in radians"],
      ["N_lines", "number of scan lines per frame"],
      ["f_Y", "vertical sawtooth frequency (one frame per period)"],
      ["f_X", "horizontal sawtooth frequency, equal to N_lines times f_Y"],
    ],
    "history_title": "📜 Theory and historical background",
    "history": "According to Tooley, apart from mechanical indicators, filament lamps and moving-coil meters, the CRT is the oldest display technology still in aircraft use; it still offers very high brightness and a wide viewing angle. The general trend, however, is to replace it with the AMLCD (active matrix liquid crystal display), which is lighter, uses less power, is smaller and more reliable, and lets a complex instrument fit into a single box. The course lecture tells the same story with a cockpit timeline: the 1903 Wright Flyer had no instruments at all; about 10 instruments by 1918; about 600 in the \"conventional\" cockpit of 1969; CRT screens in the 1990s; and large touch LCD screens on the A350 and Boeing 787 today. For Airbus the sequence is the A310 (1978, first multifunction displays), A320 (1988, six CRT screens), A380 (2007, AMLCD and IMA) and A350 (2015, large touch displays).",
    "case_title": "🔎 Case study: the path of a speed value from the ADIRU to a PFD pixel on the A320",
    "case": "The ADIRU measures and computes the air data and puts it on an ARINC 429 bus (Module 05). The DMC (Display Management Computer) receives the data and computes the symbols and images for the PFD, ND and ECAM; the FWC adds warnings and the SDAC adds system data. The formatted data travels to the LCDU 725 over a high-speed bus; inside the LCDU, the pre-processing module formats the data, the graphic processor module draws the symbols and text, the LCD assembly (with its driver electronics) switches every pixel and the backlight module provides the light. Each pixel has red, green and blue sub-pixels; with 256 levels per colour channel, one pixel can represent 256³ = 16,777,216 colours, matching the \"more than 16 million colours\" stated by Tooley (section 11.3.3, verified in the notebook). The pilot reads the result on the PFD speed scale: the number in the green box is the current speed, the yellow bug is the selected speed.",
    "warn_title": "⚠️ Common traps (and points in the lecture that need a critical reading)",
    "warn": "General trap: mixing up N1 and N2. The lecture's E/WD slide calls N2 the \"low pressure turbine speed\" while the same slide calls N1 the low pressure spool; Tooley (section 1.1.6) states that N1 is fan speed and N2 is high pressure turbine speed, so N2 must be the high pressure one. The ACARS slide expands SDAC as \"System Data Analog Computer\" but the EIS diagram slide says \"System Data Acquisition Concentrator\" (the second matches the function: it acquires data). The ECAM ELEC slide draws generators at \"420 V, 200 Hz\" while aircraft AC power is 115 V, 400 Hz (Tooley mentions a 115 V AC 400 Hz supply). The PRESS slide at FL140 shows a differential pressure of 2.9 psi together with a cabin altitude of 2,870 ft; in the ISA standard atmosphere the differential pressure should be about 4.6 psi (see notebook), so these are illustrative numbers and should not be memorised. On the ND slide, \"23 33\" is labelled as time to waypoint (23 min 33 s), yet 37 NM at a ground speed of 257 kt takes only about 8.6 minutes; it is probably an estimated time of arrival (ETA) as a UTC clock time, not yet checked against manufacturer documents, so it is flagged as doubtful. The A310 slide says \"EICAS\" while Airbus's name, per Tooley, is ECAM. Finally, a genuine printing error in Tooley: the chapter 11 answer key gives question 4 as (a), but the human eye is most sensitive to green light (peak near 550 nm, exactly as question 2 and lecture slide 6 say), so the correct answer is (c); the site uses the correct answer and says so. On the Floyd side, the printed answer to Problem 67, chapter 4 (the circuit in Figure P-19) cannot light segment a for the letter A (checked with the full truth table), so it is not used as the reference answer.",
    "notebook_desc": "Companion notebook: computes pixel size from visual acuity, raster scan frequencies, 7-segment decoding and Floyd's minimal expressions with sympy, simulates 74HC47 zero suppression, checks the numbers shown on the ECAM slides (fuel, ISA differential pressure, time to waypoint) and re-runs every multiple-choice question that can be computed."
  },
}
