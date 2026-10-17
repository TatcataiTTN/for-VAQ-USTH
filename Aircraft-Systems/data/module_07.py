# -*- coding: utf-8 -*-
"""Module 07 (VI + EN): Quan ly kiem soat phan mem (Software Management Control, DO-178, du lieu tai duoc).
Nguon: tai lieu 'software management control.pdf' (EASA Part-66 Module 05, sub-module 13, 6 trang) + Tooley Ch.13 (p.207-217)
+ Floyd Ch.2 muc 2-12 (parity, CRC; p.109-114) va Ch.11 muc 11-11 (checksum ROM)."""

DEMO_VI = ("<div class='demo-box'><h3>🧪 Demo 1: checksum có thấy được lỗi không? (chạy ngay trong trình duyệt)</h3>"
  "<p>Tệp 10 byte được \"phát hành\" cùng một checksum 8 bit và một CRC-8. Bấm một nút để làm hỏng tệp rồi xem phương pháp nào phát hiện được.</p>"
  "<div class='demo-integrity' data-lang='vi' data-bytes='48 65 6C 6C 6F 20 45 45 43 21'></div></div>"
  "<div class='demo-box'><h3>🧪 Demo 2: mức DAL đòi hỏi những gì?</h3>"
  "<div class='demo-dal' data-lang='vi'></div></div>")
DEMO_EN = DEMO_VI.replace("data-lang='vi'", "data-lang='en'").replace(
  "🧪 Demo 1: checksum có thấy được lỗi không? (chạy ngay trong trình duyệt)", "🧪 Demo 1: does the checksum see the error? (runs in your browser)").replace(
  "Tệp 10 byte được \"phát hành\" cùng một checksum 8 bit và một CRC-8. Bấm một nút để làm hỏng tệp rồi xem phương pháp nào phát hiện được.",
  "A 10-byte file is \"released\" together with an 8-bit checksum and a CRC-8. Press a button to corrupt the file and see which method detects it.").replace(
  "🧪 Demo 2: mức DAL đòi hỏi những gì?", "🧪 Demo 2: what does each software level demand?")

MOD07 = {
  "slug": "07-software-control", "num": "07", "target_slides": 30,
  "demo": {"js": "demo_integrity.js", "html_vi": DEMO_VI, "html_en": DEMO_EN},
  "vi": {
    "title": "Quản lý kiểm soát phần mềm hàng không",
    "tag": "Software Control",
    "src": "Tooley ch.13 (tr.207-217) · Bài giảng EASA Part-66 Module 5.13 (6 trang) · Floyd ch.2 mục 2-12 và ch.11 mục 11-11",
    "intro": "Phần mềm máy bay không nhìn thấy, không sờ được, nhưng phải được đối xử như mọi chi tiết máy bay khác. Một thay đổi phần mềm chưa được phê duyệt có thể gây mất máy bay. Module này trả lời bốn câu hỏi: phần mềm hỏng nặng đến đâu thì được coi là nguy hiểm (5 mức A đến E), chuẩn DO-178B/C bắt buộc những tài liệu và truy vết nào, phần mềm và dữ liệu được nạp lên máy bay ra sao (FLS, LSAP, UMS, OSS, DFLD), và làm sao biết tệp nạp không bị hỏng (checksum, CRC), kèm hai demo chạy trực tiếp.",
    "parts": [
      {"title": "Vì sao phải kiểm soát phần mềm", "bullets": [
        "Hàng triệu dòng mã chạy đồng thời trên hàng chục máy tính; mã cũng như dữ liệu và hệ điều hành nhúng đều được coi là phần mềm",
        "Phần mềm điều khiển bay hỏng lúc tiếp cận IFR trong tầm nhìn bằng 0 là kịch bản mà quy trình kiểm soát sinh ra để ngăn",
        "Chỉ thị khả phi (Airworthiness Directive) có thể yêu cầu sửa phần mềm, ví dụ lỗi EEC làm mất thông số động cơ và đóng băng cần ga"]},
      {"title": "Năm mức nghiêm trọng A đến E", "bullets": [
        "A thảm hoạ (mất máy bay), B nguy hiểm, C đáng kể, D nhẹ, E không ảnh hưởng",
        "Xác suất hỏng mỗi giờ bay: A dưới 10⁻⁹, B từ 10⁻⁹ đến 10⁻⁷, C từ 10⁻⁷ đến 10⁻⁵, D trên 10⁻⁵",
        "Điều khiển bay và dẫn đường là mức A; giải trí trên chuyến bay là mức E",
        "Mức khác nhau thường không chạy chung bộ xử lý, trừ khi có phân vùng được duyệt như ARINC 653"]},
      {"title": "DO-178B/C và truy vết", "bullets": [
        "DO-178B/ED-12B (1992) do RTCA và EUROCAE công bố; FAA và EASA dùng làm hướng dẫn chứng nhận",
        "DO-178C (2011) thay DO-178B, kèm các phụ lục DO-330 (công cụ), DO-331 (mô hình), DO-332 (hướng đối tượng), DO-333 (phương pháp hình thức)",
        "Hình 13-1: mức A cần thêm hai trace đỏ; mức A đến C cần trace tím; mức A đến D cần trace xanh; mức E không cần",
        "Thay đổi phần mềm sau chứng nhận ở mức A, B, C phải được tổ chức thiết kế (DO) phê duyệt"]},
      {"title": "Nạp phần mềm và dữ liệu lên máy bay", "bullets": [
        "FLS (field loadable software) gồm LSAP, UMS và OSS; DFLD là dữ liệu nạp được (cơ sở dữ liệu của FMC, TAWS, IMA)",
        "LSAP là bộ phận máy bay cần phát hành có kiểm soát, đi kèm EASA Form 1 hoặc FAA 8130-3",
        "Phân phối bằng phương tiện lưu trữ, truyền điện tử bằng thiết bị nạp, hoặc phân phối điện tử; nghi ngờ thì cách ly",
        "Quy trình nạp EEC bằng PDL gồm 10 bước, tối đa 3 lần thử nếu hỏng"]},
      {"title": "Kiểm tra tính toàn vẹn dữ liệu", "bullets": [
        "Checksum cộng các byte rồi gắn kết quả vào tệp; CRC chia khối bit cho một số định trước rồi gắn phần dư",
        "Cả hai chỉ báo tệp có hỏng hay không và không tuyệt đối an toàn",
        "Floyd mục 2-12 dạy parity và CRC; mục 11-11 dạy checksum kiểm tra ROM",
        "Mạng bộ nhớ, bus (Module 04, 05) và phần mềm gặp nhau ở đây: cùng một ý tưởng kiểm tra lỗi"]},
    ],
    "formula_label": "Checksum, CRC và số mức xác suất",
    "formula_math": "checksum = (b₁ + b₂ + … + b_n) mod 256<br>CRC: phần dư của phép chia modulo-2 (XOR) khối bit cho mã sinh G; phần dư bằng 0 nghĩa là không phát hiện lỗi",
    "legend": [
      ["b_i", "giá trị byte thứ i của tệp"],
      ["mod 256", "chỉ giữ 8 bit thấp, vì checksum chỉ có 1 byte"],
      ["G", "mã sinh (generator), cả bên gửi lẫn bên nhận đều biết trước"],
      ["modulo-2", "phép cộng/trừ không nhớ, chính là cổng XOR (Floyd bảng 2-9)"],
    ],
    "history_title": "📜 Bối cảnh lý thuyết và lịch sử",
    "history": "Theo bài giảng, nhu cầu kiểm soát phần mềm xuất hiện khi máy bay hiện đại chứa hàng triệu dòng mã trong hàng chục máy tính. RTCA công bố DO-178B năm 1992 và EUROCAE công bố bản tương đương ED-12B; FAA và EASA dùng chúng để xét xem phần mềm có chạy tin cậy trên máy bay hay không. Ban đầu phần lớn mã viết tay; về sau việc sinh mã tự động từ mô hình (MATLAB, Simulink, Embedded Coder) phổ biến, nên cần làm rõ ranh giới giữa yêu cầu hệ thống cấp cao và yêu cầu phần mềm cấp thấp, và cần cách kiểm chứng phần mềm sinh từ mô hình. Vì vậy DO-178C ra đời năm 2011; tháng 7 năm 2013 FAA ban hành thông tư AC 20-115C công nhận DO-178C là phương tiện tuân thủ cho khía cạnh phần mềm của hệ thống trên không.",
    "case_title": "🔎 Case study: nạp phần mềm cho bộ điều khiển động cơ điện tử (EEC)",
    "case": "Tooley mô tả quy trình nạp EEC bằng thiết bị nạp cầm tay PDL. Tắt nguồn EEC, nối cáp PDL vào bộ nạp rồi vào EEC, cấp 28 V DC cho bộ nạp, bật 115 V AC (400 Hz) cho EEC, kiểm tra đúng đĩa phiên bản phần mềm (cùng phiên bản cho cả động cơ trái lẫn phải) và đĩa không bị khoá ghi, rồi nạp trong khoảng 12 đến 16 phút. Nếu thành công, PDL hiện LOAD COMPLETE; nếu đèn lỗi truyền sáng, kiểm tra cáp và thử lại, tối đa ba lần. Cuối cùng chạy chương trình kiểm tra bộ nhớ: PASS cho số hiệu phần cứng và checksum thì EEC đã được lập trình đúng, rồi ghi phiên bản phần mềm, số Service Bulletin và ngày lên nhãn kim loại của EEC. Mỗi bước tương ứng với một nguyên tắc của module: đúng phiên bản (truy vết), có kiểm tra toàn vẹn (checksum), có hồ sơ (phát hành có kiểm soát).",
    "warn_title": "⚠️ Bẫy hay gặp (và chỗ bài giảng chưa đầy đủ)",
    "warn": "Bẫy phổ biến: cho rằng checksum và CRC chứng minh phần mềm đúng. Chúng chỉ phát hiện tệp bị thay đổi; Tooley nói rõ không phương pháp nào tuyệt đối an toàn (xem Demo 1: đổi chỗ hai byte hoặc hai lỗi triệt tiêu nhau qua mặt được checksum). Bẫy thứ hai: nhầm FLS với DFLD; DFLD là dữ liệu, nhưng vẫn phải có số hiệu và hồ sơ phát hành riêng như mã chạy. Một chỗ bài giảng chưa đầy đủ: Câu hỏi 13-6 hỏi trace nào chỉ bắt buộc ở mức A, đáp án in chỉ nêu mã nguồn với mã đối tượng thực thi, nhưng Hình 13-1 của chính bài giảng vẽ hai mũi tên đỏ (chỉ mức A): ngoài mã nguồn với mã đối tượng còn có kiến trúc phần mềm với yêu cầu cấp cao. Tooley dùng cả \"Level\" (bảng 13.1) lẫn \"Class\" (câu trắc nghiệm 4) cho cùng một khái niệm. Về Floyd: phép chia CRC trong mục 2-12 thêm số chữ số 0 bằng số bit của mã sinh (4 bit thì thêm 4 số 0), trong khi CRC chuẩn thêm số bit của mã sinh trừ 1; cả hai đều cho phần dư 0 khi nhận đúng, nên đây chỉ là khác biệt về cách trình bày, không phải lỗi.",
    "notebook_desc": "Notebook đi kèm: checksum 8 bit và CRC-8 viết lại bằng Python (kiểm với giá trị chuẩn 0xF4), tái hiện Ví dụ 2-41 của Floyd (phần dư 0100, mã truyền 110100110100), thử các kiểu lỗi (lật bit, đổi chỗ, hai lỗi triệt tiêu), mô phỏng quyết định phát hành FLS/DFLD, và đối chiếu khoá đáp án in của Tooley chương 13."
  },
  "en": {
    "title": "Aircraft Software Management Control",
    "tag": "Software Control",
    "src": "Tooley ch.13 (p.207-217) · EASA Part-66 Module 5.13 lecture notes (6 pages) · Floyd ch.2 section 2-12 and ch.11 section 11-11",
    "intro": "Aircraft software cannot be seen or touched, yet it must be treated like any other aircraft part. An unapproved software change can lose an aircraft. This module answers four questions: how bad a software failure must be to count as dangerous (five levels A to E), which documents and traceability DO-178B/C require, how software and data are loaded onto the aircraft (FLS, LSAP, UMS, OSS, DFLD), and how to know a loaded file is not corrupt (checksum, CRC), with two live demos.",
    "parts": [
      {"title": "Why software needs control", "bullets": [
        "Millions of lines of code run at once on dozens of computers; code, data and embedded operating systems all count as software",
        "Flight control software failing during a zero-visibility IFR approach is the scenario that control procedures exist to prevent",
        "An Airworthiness Directive can require a software fix, for example an EEC fault that lost engine parameters and froze the power setting"]},
      {"title": "Five severity levels A to E", "bullets": [
        "A catastrophic (aircraft loss), B hazardous, C major, D minor, E no effect",
        "Failure probability per flight hour: A below 10⁻⁹, B between 10⁻⁹ and 10⁻⁷, C between 10⁻⁷ and 10⁻⁵, D above 10⁻⁵",
        "Flight control and navigation are level A; in-flight entertainment is level E",
        "Different levels usually do not share a processor, unless an approved partitioning scheme such as ARINC 653 is used"]},
      {"title": "DO-178B/C and traceability", "bullets": [
        "DO-178B/ED-12B (1992) was published by RTCA and EUROCAE; FAA and EASA use it as certification guidance",
        "DO-178C (2011) replaced DO-178B, with supplements DO-330 (tools), DO-331 (models), DO-332 (object-oriented), DO-333 (formal methods)",
        "Figure 13-1: level A needs two extra red traces; levels A to C need purple traces; levels A to D need green traces; level E needs none",
        "A post-certification software change at level A, B or C must be approved by the design organisation (DO)"]},
      {"title": "Loading software and data onto the aircraft", "bullets": [
        "FLS (field loadable software) includes LSAP, UMS and OSS; DFLD is field loadable data (FMC, TAWS, IMA databases)",
        "An LSAP is an aircraft part needing controlled release with an EASA Form 1 or FAA 8130-3",
        "Distribution by storage media, electronic transfer with a data loader, or electronic distribution; if in doubt, quarantine",
        "The EEC loading procedure with a PDL has 10 steps and at most 3 attempts if it fails"]},
      {"title": "Checking data integrity", "bullets": [
        "A checksum adds the bytes and appends the result; a CRC divides blocks of bits by a fixed number and appends the remainder",
        "Both only indicate whether a file changed and neither is completely fool-proof",
        "Floyd section 2-12 teaches parity and CRC; section 11-11 teaches the ROM checksum test",
        "Memory, buses (Modules 04, 05) and software meet here: the same error-checking idea"]},
    ],
    "formula_label": "Checksum, CRC and probability levels",
    "formula_math": "checksum = (b₁ + b₂ + … + b_n) mod 256<br>CRC: remainder of modulo-2 (XOR) division of the bit block by a generator code G; a zero remainder means no error detected",
    "legend": [
      ["b_i", "value of byte i of the file"],
      ["mod 256", "keep only the low 8 bits, because the checksum is one byte"],
      ["G", "generator code, known in advance to both sender and receiver"],
      ["modulo-2", "addition/subtraction without carry, i.e. the XOR gate (Floyd Table 2-9)"],
    ],
    "history_title": "📜 Theory and historical background",
    "history": "According to the lecture notes, the need for software control arose when modern aircraft came to contain millions of lines of code across dozens of computers. RTCA published DO-178B in 1992 and EUROCAE the equivalent ED-12B; FAA and EASA use them to judge whether software will perform reliably on aircraft. Early software was mostly hand-coded; later, automatic code generation from models (MATLAB, Simulink, Embedded Coder) became common, so the boundary between high-level system requirements and low-level software requirements needed clarifying, and a way to verify model-based software was needed. DO-178C was therefore developed in 2011; in July 2013 the FAA issued Advisory Circular AC 20-115C recognising DO-178C as a means of compliance for the software aspects of airborne systems.",
    "case_title": "🔎 Case study: loading software into an electronic engine controller (EEC)",
    "case": "Tooley describes the EEC loading procedure with a portable data loader (PDL). Switch off power to the EEC, connect the PDL cable to the loader and to the EEC, supply 28 V DC to the loader, switch on 115 V AC (400 Hz) to the EEC, check the correct software version disk (the same version for the left and right engines) and that the disk is not write-protected, then load for about 12 to 16 minutes. If it succeeds the PDL shows LOAD COMPLETE; if the transfer-fail lamp lights, check the cables and try again, at most three attempts. Finally run the memory verification program: PASS for the hardware part number and checksums means the EEC is correctly programmed, then write the software version, Service Bulletin number and date on the EEC's metal plate. Each step maps to a principle of this module: correct version (traceability), integrity check (checksum), record keeping (controlled release).",
    "warn_title": "⚠️ Common traps (and where the lecture notes are incomplete)",
    "warn": "General trap: believing that a checksum or CRC proves the software is correct. They only detect that a file changed; Tooley states plainly that neither method is completely fool-proof (see Demo 1: swapping two bytes or two cancelling errors fool the checksum). Second trap: mixing up FLS and DFLD; DFLD is data, but it still needs its own part number and release documentation like executable code. One place where the lecture notes are incomplete: Question 13-6 asks which trace is required only at level A, and the printed answer names only source code to executable object code, yet the notes' own Figure 13-1 draws two red arrows (level A only): besides source code to object code there is also software architecture to high-level requirements. Tooley itself uses both \"Level\" (Table 13.1) and \"Class\" (multiple-choice question 4) for the same concept. On the Floyd side: the CRC division in section 2-12 appends as many zeros as the generator has bits (4 bits means 4 zeros), whereas the standard CRC appends the generator length minus one; both give a zero remainder on a correct reception, so this is a difference of presentation, not an error.",
    "notebook_desc": "Companion notebook: 8-bit checksum and CRC-8 rewritten in Python (checked against the standard value 0xF4), a reproduction of Floyd Example 2-41 (remainder 0100, transmitted code 110100110100), error experiments (bit flip, swap, cancelling errors), a FLS/DFLD release decision simulation, and a cross-check of Tooley's printed chapter 13 answer key."
  },
}
