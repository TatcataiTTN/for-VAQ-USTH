# -*- coding: utf-8 -*-
"""
Noi dung tung module (VI + EN). Day la "nguon su that" duy nhat cho noi dung -
render_site.py doc tu day de sinh HTML, khong sua truc tiep file HTML da sinh.
"""

MODULES = [
  {
    "slug": "01-number-systems",
    "num": "01",
    "target_slides": 60,  # Tooley + Floyd deu co chuong rieng -> trung nhau -> 60 slide
    "vi": {
      "title": "Hệ đếm trong hệ thống số hàng không",
      "tag": "Number Systems",
      "src": "Tooley ch.2 (tr.25-38) · Floyd ch.2 (tr.65-124)",
      "intro": "Mọi dữ liệu bên trong máy tính hàng không (FMGC, FWC, SDAC…) đều được xử lý ở dạng nhị phân, "
               "nhưng con người cần các hệ đếm trung gian (bát phân, thập lục phân, BCD) để đọc/nhập dữ liệu "
               "thuận tiện hơn. Module này xây lại 4 hệ đếm cốt lõi và ứng dụng thực tế của từng hệ trên Airbus A320.",
      "parts": [
        {"title": "Vì sao máy tính hàng không cần nhiều hệ đếm?", "bullets": [
            "Ôn lại hệ thập phân (decimal): hệ con người dùng hằng ngày",
            "Hệ nhị phân (binary): nền tảng của mọi mạch số",
            "Hệ bát phân (octal) và thập lục phân (hexadecimal): cách viết gọn của nhị phân",
            "Mã BCD: cầu nối giữa số thập phân và hiển thị 7 đoạn"]},
        {"title": "Hệ nhị phân và phép chuyển đổi", "bullets": [
            "Trọng số bit: MSB/LSB, luỹ thừa của 2",
            "Chuyển thập phân ↔ nhị phân bằng phép chia/nhân liên tiếp",
            "Bù hai (two's complement) để biểu diễn số âm"]},
        {"title": "Hệ bát phân và thập lục phân", "bullets": [
            "Nhóm 3 bit ↔ 1 chữ số bát phân, nhóm 4 bit ↔ 1 chữ số hex",
            "Ứng dụng: mã trạng thái hệ thống (octal), địa chỉ bộ nhớ/mã lỗi BITE (hex)"]},
        {"title": "Mã BCD và ASCII", "bullets": [
            "BCD: mỗi chữ số thập phân → 4 bit riêng biệt",
            "Ứng dụng BCD trên MCDU, hiển thị 7 đoạn",
            "ASCII: mã hoá ký tự cho trao đổi dữ liệu văn bản"]},
        {"title": "Áp dụng trên Airbus A320", "bullets": [
            "Dữ liệu bus ARINC 429 truyền ở dạng nhị phân, hiển thị log ở dạng hex",
            "ECAM/EWD hiển thị BCD cho N1, EGT, độ cao",
            "Mã lỗi BITE hiển thị ở dạng hex (vd 0xACDE)"]},
      ],
      "formula_label": "Đổi cơ số bằng phép chia liên tiếp (thập phân → cơ số b)",
      "formula_math": "N₁₀ = Σ dᵢ · bⁱ  ⇒  chia N cho b liên tiếp, lấy phần dư theo thứ tự ngược",
      "legend": [("N", "số thập phân cần đổi"), ("b", "cơ số đích (2, 8, hoặc 16)"), ("dᵢ", "chữ số ở vị trí i, trọng số bⁱ")],
      "history_title": "📜 Bối cảnh lý thuyết & lịch sử",
      "history": "Hệ nhị phân được Gottfried Leibniz hệ thống hoá vào năm 1703 trong công trình "
                 "<i>Explication de l'Arithmétique Binaire</i>, nhưng phải tới công trình của Claude Shannon "
                 "(luận văn thạc sĩ 1937, ứng dụng đại số Boole vào mạch chuyển mạch) thì hệ nhị phân mới trở "
                 "thành nền tảng thực sự của điện tử số. Mã BCD được chuẩn hoá để đơn giản hoá việc hiển thị "
                 "số thập phân trên các thiết bị điện tử sơ khai (đồng hồ số, máy tính bỏ túi) mà không cần "
                 "mạch chuyển đổi nhị phân sang thập phân đầy đủ.",
      "case_title": "🔎 Case study thực tế: đọc mã lỗi BITE trên Airbus A320",
      "case": "Khi một LRU (Line Replaceable Unit) trên A320 phát hiện lỗi, hệ thống BITE tạo ra một mã lỗi "
              "hiển thị dạng hex trên MCDU/ECAM (ví dụ <code>0xACDE</code>). Kỹ thuật viên bảo dưỡng tra mã "
              "này trong AMM (Aircraft Maintenance Manual) để xác định đúng LRU và nguyên nhân lỗi. Việc hiển "
              "thị hex thay vì chuỗi nhị phân 16-bit đầy đủ (<code>1010 1100 1101 1110</code>) giúp rút ngắn "
              "đáng kể thời gian tra cứu và giảm sai sót khi ghi chép bằng tay.",
      "warn_title": "⚠️ Bẫy hay gặp",
      "warn": "Nhầm lẫn phổ biến nhất là đổi trực tiếp giữa hex và octal mà không qua bước trung gian nhị phân. "
              "Vì hex nhóm theo 4 bit còn octal nhóm theo 3 bit, hai nhóm này KHÔNG thẳng hàng: luôn phải "
              "quy về nhị phân đầy đủ trước, rồi nhóm lại theo đúng cơ số đích, như minh hoạ ở câu 9 trong bộ "
              "câu hỏi bên dưới (111₁₆ → 421₈, không thể suy trực tiếp).",
      "notebook_desc": "Notebook đi kèm: bộ chuyển đổi cơ số (thập phân/nhị phân/bát phân/hex/BCD) viết bằng Python, "
                        "tự kiểm tra lại toàn bộ 13 câu hỏi gốc từ sách Tooley bằng code thay vì tính tay: "
                        "cộng thêm mục giải TOÀN BỘ 69 bài tập cuối chương 2 của Floyd (Problems 2-1 tới 2-12).",
    },
    "en": {
      "title": "Number Systems in Aircraft Digital Data",
      "tag": "Number Systems",
      "src": "Tooley ch.2 (p.25-38) · Floyd ch.2 (p.65-124)",
      "intro": "All data inside aircraft computers (FMGC, FWC, SDAC…) is processed in binary, but humans need "
               "intermediate number systems (octal, hexadecimal, BCD) to read and enter data conveniently. "
               "This module rebuilds the four core number systems and their real applications on the Airbus A320.",
      "parts": [
        {"title": "Why does an aircraft computer need several number systems?", "bullets": [
            "Review of the decimal system: the one humans use every day",
            "Binary: the foundation of every digital circuit",
            "Octal and hexadecimal: compact shorthand for binary",
            "BCD: the bridge between decimal digits and 7-segment displays"]},
        {"title": "Binary numbers and conversion", "bullets": [
            "Bit weighting: MSB/LSB, powers of two",
            "Decimal ↔ binary conversion by repeated division/multiplication",
            "Two's complement for representing negative numbers"]},
        {"title": "Octal and hexadecimal", "bullets": [
            "Group of 3 bits ↔ 1 octal digit, group of 4 bits ↔ 1 hex digit",
            "Applications: system status codes (octal), memory addresses/BITE fault codes (hex)"]},
        {"title": "BCD and ASCII codes", "bullets": [
            "BCD: each decimal digit → its own 4-bit group",
            "BCD on MCDU input panels and 7-segment displays",
            "ASCII: character encoding for text data exchange"]},
        {"title": "Application on the Airbus A320", "bullets": [
            "ARINC 429 bus data is transmitted in binary, logged/displayed in hex",
            "ECAM/EWD display BCD-coded N1, EGT, altitude",
            "BITE fault codes are shown in hex (e.g. 0xACDE)"]},
      ],
      "formula_label": "Base conversion by repeated division (decimal → base b)",
      "formula_math": "N₁₀ = Σ dᵢ · bⁱ  ⇒  divide N by b repeatedly, read remainders in reverse order",
      "legend": [("N", "decimal number to convert"), ("b", "target base (2, 8, or 16)"), ("dᵢ", "digit at position i, weight bⁱ")],
      "history_title": "📜 Theoretical & historical background",
      "history": "The binary system was formalised by Gottfried Leibniz in 1703 in his <i>Explication de "
                 "l'Arithmétique Binaire</i>, but it only became the true foundation of digital electronics "
                 "after Claude Shannon's 1937 master's thesis applied Boolean algebra to switching circuits. "
                 "BCD was standardised to simplify decimal display on early electronic devices (digital clocks, "
                 "calculators) without requiring a full binary-to-decimal conversion circuit.",
      "case_title": "🔎 Real case study: reading a BITE fault code on the Airbus A320",
      "case": "When an LRU (Line Replaceable Unit) on the A320 detects a fault, the BITE system generates a "
              "fault code shown in hex on the MCDU/ECAM (e.g. <code>0xACDE</code>). Maintenance technicians "
              "look this code up in the AMM (Aircraft Maintenance Manual) to identify the LRU and root cause. "
              "Displaying hex instead of the full 16-bit binary string (<code>1010 1100 1101 1110</code>) "
              "significantly shortens lookup time and reduces manual transcription errors.",
      "warn_title": "⚠️ Common trap",
      "warn": "The most common mistake is converting directly between hex and octal without going through binary. "
              "Because hex groups bits in 4s while octal groups them in 3s, the two groupings do NOT line up: "
              "always expand to full binary first, then regroup for the target base, as illustrated in question 9 "
              "below (111₁₆ → 421₈ cannot be inferred directly).",
      "notebook_desc": "Companion notebook: a Python base-converter (decimal/binary/octal/hex/BCD) that re-checks "
                        "all 13 original Tooley textbook questions by code instead of by hand: plus a section "
                        "that auto-solves all 69 end-of-chapter Problems from Floyd Chapter 2.",
    },
  },
  {
    "slug": "02-logic-boolean",
    "num": "02",
    "target_slides": 60,  # Tooley + Floyd deu co chuong rieng -> trung nhau -> 60 slide
    "vi": {
      "title": "Cổng logic & Đại số Boolean",
      "tag": "Logic Circuits",
      "src": "Tooley ch.5 (tr.70-94) · Floyd ch.3-4 (tr.125-260), ch.7 (bistable, tr.387+)",
      "intro": "Toàn bộ hệ thống số trên máy bay, từ cảnh báo cửa càng đáp cho tới điều khiển APU, đều được xây "
               "từ các cổng logic cơ bản kết hợp theo quy tắc đại số Boolean. Module này đi từ cổng logic đơn "
               "lẻ tới mạch tổ hợp thực tế và các họ linh kiện logic dùng trên máy bay.",
      "parts": [
        {"title": "Từ cổng logic cơ bản tới bài toán thực tế", "bullets": [
            "AND, OR, NOT, NAND, NOR, XOR: bảng chân trị và ký hiệu",
            "Ví dụ mở đầu: cảnh báo cửa càng đáp chưa khoá (landing gear door warning)"]},
        {"title": "Đại số Boolean", "bullets": [
            "Các định luật cơ bản (giao hoán, kết hợp, phân phối, hấp thụ)",
            "Định lý De Morgan",
            "Rút gọn biểu thức logic từng bước"]},
        {"title": "Mạch logic tổ hợp (combinational logic)", "bullets": [
            "Từ bảng chân trị tới sơ đồ mạch",
            "Ví dụ: mạch điều khiển khởi động APU"]},
        {"title": "Logic ba trạng thái, mạch đơn ổn & song ổn", "bullets": [
            "Tri-state logic dùng để chia sẻ bus",
            "Monostable (one-shot) và bistable (flip-flop)"]},
        {"title": "Các họ linh kiện logic (logic families)", "bullets": [
            "TTL và các biến thể (LS, S…)",
            "CMOS: ưu điểm điện năng thấp, biên độ nhiễu cao",
            "Chọn họ logic phù hợp theo ứng dụng"]},
      ],
      "formula_label": "Định lý De Morgan",
      "formula_math": "(A·B)′ = A′ + B′        (A+B)′ = A′·B′",
      "legend": [("A, B", "biến logic đầu vào (0 hoặc 1)"), ("′", "phép đảo (NOT)"), ("·  +", "phép AND, phép OR")],
      "history_title": "📜 Bối cảnh lý thuyết & lịch sử",
      "history": "Đại số Boolean do George Boole công bố năm 1854 trong <i>An Investigation of the Laws of "
                 "Thought</i>, ban đầu chỉ là công cụ hình thức hoá logic mệnh đề, không liên quan tới điện tử. "
                 "Phải tới luận văn thạc sĩ năm 1937 của Claude Shannon tại MIT, đại số Boole mới được chứng "
                 "minh là công cụ toán học chính xác để phân tích và thiết kế mạch chuyển mạch rơle: đặt nền "
                 "móng trực tiếp cho toàn bộ thiết kế mạch số hiện đại, bao gồm hệ thống logic trên máy bay.",
      "case_title": "🔎 Case study thực tế: mạch cảnh báo cửa càng đáp",
      "case": "Một mạch cảnh báo đơn giản trên máy bay cần bật đèn cảnh báo khi CÓ ÍT NHẤT MỘT cửa càng đáp "
              "chưa đóng khoá hoàn toàn VÀ máy bay đang ở chế độ bay bằng (không phải trên mặt đất). Đây là "
              "ví dụ kinh điển trong sách Tooley: đầu ra cảnh báo = OR của các công tắc cửa càng, AND với tín "
              "hiệu 'in-flight': minh hoạ trực tiếp cách kết hợp AND/OR để mã hoá một điều kiện an toàn thực.",
      "warn_title": "⚠️ Bẫy hay gặp",
      "warn": "Nhầm giữa NAND/NOR với 'phủ định của AND/OR theo nghĩa thông thường' khi lập bảng chân trị bằng "
              "trực giác thay vì tính từng bước: cách an toàn nhất luôn là viết bảng chân trị đầy đủ AND/OR "
              "trước, rồi đảo bit kết quả, không suy luận tắt.",
      "notebook_desc": "Notebook đi kèm: sinh bảng chân trị tự động cho biểu thức Boolean bất kỳ, rút gọn bằng "
                        "sympy và đối chiếu kết quả với rút gọn tay theo các định luật đã học: cộng thêm mục "
                        "tự động giải phần lớn bài tập chương 4 của Floyd (luật Boolean, De Morgan, SOP/POS, "
                        "Karnaugh map, Quine-McCluskey) bằng sympy.logic.",
    },
    "en": {
      "title": "Logic Gates & Boolean Algebra",
      "tag": "Logic Circuits",
      "src": "Tooley ch.5 (p.70-94) · Floyd ch.3-4 (p.125-260), ch.7 (bistables, p.387+)",
      "intro": "Every digital system on an aircraft, from a landing-gear-door warning to APU start control, is "
               "built from basic logic gates combined according to Boolean algebra rules. This module moves "
               "from single gates to real combinational circuits and the logic families used on aircraft.",
      "parts": [
        {"title": "From basic gates to a real problem", "bullets": [
            "AND, OR, NOT, NAND, NOR, XOR: truth tables and symbols",
            "Opening example: landing gear door unlocked warning"]},
        {"title": "Boolean algebra", "bullets": [
            "Basic laws (commutative, associative, distributive, absorption)",
            "De Morgan's theorem",
            "Step-by-step logic expression simplification"]},
        {"title": "Combinational logic circuits", "bullets": [
            "From truth table to circuit diagram",
            "Example: APU starter control circuit"]},
        {"title": "Tri-state logic, monostables & bistables", "bullets": [
            "Tri-state logic for bus sharing",
            "Monostable (one-shot) and bistable (flip-flop) devices"]},
        {"title": "Logic families", "bullets": [
            "TTL and its variants (LS, S…)",
            "CMOS: low power, high noise margin",
            "Choosing the right logic family for an application"]},
      ],
      "formula_label": "De Morgan's theorem",
      "formula_math": "(A·B)′ = A′ + B′        (A+B)′ = A′·B′",
      "legend": [("A, B", "logic input variables (0 or 1)"), ("′", "NOT / inversion"), ("·  +", "AND, OR operators")],
      "history_title": "📜 Theoretical & historical background",
      "history": "Boolean algebra was published by George Boole in 1854 in <i>An Investigation of the Laws of "
                 "Thought</i>, originally a pure formalisation of propositional logic with no link to electronics. "
                 "It only became a precise tool for analysing and designing relay switching circuits after Claude "
                 "Shannon's 1937 MIT master's thesis: laying the direct foundation for all modern digital circuit "
                 "design, including aircraft logic systems.",
      "case_title": "🔎 Real case study: landing gear door warning circuit",
      "case": "A simple aircraft warning circuit must light a warning lamp when AT LEAST ONE landing gear door "
              "is not fully locked AND the aircraft is in flight mode (not on ground). This is a classic example "
              "from Tooley's textbook: warning output = OR of the gear-door switches, ANDed with the 'in-flight' "
              "signal: a direct illustration of combining AND/OR to encode a real safety condition.",
      "warn_title": "⚠️ Common trap",
      "warn": "Confusing NAND/NOR with 'the everyday negation of AND/OR' by guessing the truth table intuitively "
              "instead of computing it step by step: the safest approach is always to write out the full AND/OR "
              "truth table first, then invert the result bit by bit, never skip straight to the answer.",
      "notebook_desc": "Companion notebook: auto-generates the truth table for any Boolean expression, simplifies "
                        "it with sympy, and cross-checks the result against the manual simplification steps: plus "
                        "a section that auto-solves most of Floyd Chapter 4's Problems (Boolean laws, De Morgan, "
                        "SOP/POS, Karnaugh maps, Quine-McCluskey) using sympy.logic.",
    },
  },
  {
    "slug": "03-ic-multiplexing",
    "num": "03",
    "target_slides": 60,  # Tooley + Floyd deu co chuong rieng -> trung nhau -> 60 slide
    "vi": {
      "title": "Mạch tích hợp (IC) & Kỹ thuật dồn kênh",
      "tag": "Integrated Circuits & MSI",
      "src": "Tooley ch.8-9 (tr.139-164) · Floyd ch.6 (tr.313-386), ch.15 (công nghệ IC)",
      "intro": "Từ một cổng logic đơn lẻ (SSI) tới vi xử lý hàng triệu transistor (VLSI), quy mô tích hợp quyết "
               "định cách đóng gói, cách kiểm tra và cách sử dụng một linh kiện. Module này trình bày các mức "
               "tích hợp, kỹ thuật đóng gói IC, và các mạch MSI phổ biến nhất trên máy bay: bộ giải mã, bộ mã "
               "hoá và bộ dồn kênh (multiplexer).",
      "parts": [
        {"title": "Quy mô tích hợp: từ SSI tới VLSI", "bullets": [
            "SSI (vài cổng) → MSI (vài chục-trăm cổng) → LSI → VLSI (triệu transistor)",
            "Công nghệ chế tạo và đóng gói IC (DIL, PLCC, QFP, SOIC…)"]},
        {"title": "Fan-in và fan-out", "bullets": [
            "Định nghĩa và giới hạn tải của một cổng logic",
            "Vì sao vượt fan-out gây lỗi mức logic"]},
        {"title": "Bộ giải mã và bộ mã hoá (decoder/encoder)", "bullets": [
            "Giải mã địa chỉ bộ nhớ, mã hoá bàn phím",
            "Chân enable để ghép tầng (cascading)"]},
        {"title": "Bộ dồn kênh (multiplexer/data selector)", "bullets": [
            "Nguyên lý: n đường chọn cho 2ⁿ kênh vào",
            "Ứng dụng: bộ chọn dữ liệu độ cao 4 kênh trên hệ thống altimeter"]},
        {"title": "Áp dụng trong hệ thống avionics", "bullets": [
            "Ví dụ thực tế: bộ dồn kênh ARINC 429 4 kênh (Figure 9.21, Tooley)",
            "Chuyển đổi mã BCD sang 7 đoạn cho hiển thị"]},
      ],
      "formula_label": "Số đường chọn cần thiết cho bộ dồn kênh",
      "formula_math": "n = log₂(N)   với N kênh dữ liệu đầu vào",
      "legend": [("N", "số kênh dữ liệu đầu vào của multiplexer"), ("n", "số đường chọn (select lines) cần thiết")],
      "history_title": "📜 Bối cảnh lý thuyết & lịch sử",
      "history": "Mạch tích hợp đầu tiên được Jack Kilby (Texas Instruments) trình diễn năm 1958, tiếp theo là "
                 "phương án thực tế hơn của Robert Noyce (Fairchild) năm 1959 dựa trên công nghệ planar. Từ đó, "
                 "định luật Moore (1965) dự đoán số transistor trên một chip tăng gấp đôi mỗi 18-24 tháng: xu "
                 "hướng phản ánh trực tiếp qua các mức tích hợp SSI→MSI→LSI→VLSI được trình bày trong chương "
                 "này của Tooley.",
      "case_title": "🔎 Case study thực tế: bộ dồn kênh dữ liệu độ cao trên A320",
      "case": "Hệ thống altimeter trên A320 cần chọn 1 trong 4 nguồn dữ liệu độ cao (độ cao đã chọn và độ cao "
              "thực tế từ ADC trái/phải) để đưa vào bộ mã hoá dữ liệu nối tiếp ARINC 429 (xem Figure 9.21, "
              "Tooley). Một bộ dồn kênh kép 4 kênh (dual four-channel multiplexer) thực hiện việc chuyển mạch "
              "này chỉ với 2 đường chọn nhị phân, thay vì cần 4 đường truyền vật lý riêng biệt: tiết kiệm đáng "
              "kể trọng lượng dây dẫn trên máy bay.",
      "warn_title": "⚠️ Bẫy hay gặp",
      "warn": "Nhầm lẫn giữa 'demultiplexer' (1 vào → nhiều ra) và 'decoder' (giải mã địa chỉ): cả hai đôi khi "
              "dùng chung một IC vật lý (vì decoder không có input dữ liệu cũng có thể hoạt động như demux khi "
              "gán 1 đường làm dữ liệu, còn lại làm địa chỉ chọn), nhưng về chức năng mạch, chúng phục vụ hai "
              "mục đích khác nhau.",
      "notebook_desc": "Notebook đi kèm: mô phỏng bảng chân trị của bộ giải mã 3-sang-8, bộ mã hoá ưu tiên, và "
                        "bộ dồn kênh 4-sang-1/8-sang-1 bằng Python, kiểm tra công thức n=log₂(N): cộng thêm mục "
                        "giải các bài tập chương 6 của Floyd không cần hình vẽ gốc (bộ cộng bán phần/toàn phần).",
    },
    "en": {
      "title": "Integrated Circuits & Multiplexing",
      "tag": "Integrated Circuits & MSI",
      "src": "Tooley ch.8-9 (p.139-164) · Floyd ch.6 (p.313-386), ch.15 (IC technologies)",
      "intro": "From a single logic gate (SSI) to a microprocessor with millions of transistors (VLSI), the "
               "scale of integration determines how a device is packaged, tested and used. This module covers "
               "integration scales, IC packaging technology, and the most common MSI circuits found on aircraft: "
               "decoders, encoders and multiplexers.",
      "parts": [
        {"title": "Scale of integration: from SSI to VLSI", "bullets": [
            "SSI (a few gates) → MSI (tens-hundreds of gates) → LSI → VLSI (millions of transistors)",
            "IC fabrication and packaging technology (DIL, PLCC, QFP, SOIC…)"]},
        {"title": "Fan-in and fan-out", "bullets": [
            "Definition and loading limits of a logic gate",
            "Why exceeding fan-out causes logic-level failures"]},
        {"title": "Decoders and encoders", "bullets": [
            "Memory address decoding, keyboard encoding",
            "Enable pins for cascading"]},
        {"title": "Multiplexers (data selectors)", "bullets": [
            "Principle: n select lines for 2ⁿ input channels",
            "Application: 4-channel altitude data selector in an altimeter system"]},
        {"title": "Application in avionics systems", "bullets": [
            "Real example: 4-channel ARINC 429 multiplexer (Figure 9.21, Tooley)",
            "BCD to 7-segment code conversion for displays"]},
      ],
      "formula_label": "Select lines required for a multiplexer",
      "formula_math": "n = log₂(N)   for N input data channels",
      "legend": [("N", "number of multiplexer input data channels"), ("n", "number of select lines required")],
      "history_title": "📜 Theoretical & historical background",
      "history": "The first integrated circuit was demonstrated by Jack Kilby (Texas Instruments) in 1958, "
                 "followed by Robert Noyce's (Fairchild) more practical planar-technology version in 1959. "
                 "Moore's Law (1965) then predicted the number of transistors per chip doubling every 18-24 "
                 "months: a trend directly reflected in the SSI→MSI→LSI→VLSI progression covered in this "
                 "chapter of Tooley.",
      "case_title": "🔎 Real case study: altitude data multiplexer on the A320",
      "case": "The A320 altimeter system needs to select 1 of 4 altitude data sources (selected altitude and "
              "actual altitude from the left/right ADC) to feed into the ARINC 429 serial data encoder (see "
              "Figure 9.21, Tooley). A dual four-channel multiplexer performs this switching with only 2 binary "
              "select lines instead of 4 separate physical data paths: a meaningful weight saving in aircraft "
              "wiring.",
      "warn_title": "⚠️ Common trap",
      "warn": "Confusing a 'demultiplexer' (1 input → many outputs) with a 'decoder' (address decoding): the "
              "two sometimes share the same physical IC (a decoder with no dedicated data input can act as a "
              "demux by treating one line as data and the rest as select address), but functionally they serve "
              "different purposes.",
      "notebook_desc": "Companion notebook: simulates the truth table of a 3-to-8 decoder, a priority encoder, "
                        "and 4-to-1/8-to-1 multiplexers in Python, verifying the n=log₂(N) formula: plus a section "
                        "solving Floyd Chapter 6's figure-free Problems (half/full adders).",
    },
  },
  {
    "slug": "04-computer-cpu",
    "num": "04",
    "target_slides": 40,  # Floyd KHONG co chuong CPU rieng -> khop yeu -> 40 slide
    "vi": {
      "title": "Cấu trúc máy tính & Vi xử lý (CPU)",
      "tag": "Computers & Microprocessors",
      "src": "Tooley ch.6-7 (tr.95-138) · Floyd ch.11 (bộ nhớ bán dẫn, tr.627-696)",
      "intro": "Mọi máy tính hàng không, từ đồng hồ buồng lái cho tới AIDS data recorder, đều dựa trên 3 khối cơ "
               "bản: CPU, bộ nhớ (RAM/ROM), và hệ thống bus kết nối. Module này trình bày cấu trúc máy tính, "
               "nguyên lý hoạt động của CPU, và các loại bộ nhớ bán dẫn dùng trong avionics.",
      "parts": [
        {"title": "Cấu trúc cơ bản của một hệ thống máy tính", "bullets": [
            "Mô hình IPO: Input → Process → Output",
            "Ba loại bus: address, data, control",
            "Ví dụ: đồng hồ buồng lái (clock computer) và AIDS data recorder"]},
        {"title": "Bộ nhớ bán dẫn", "bullets": [
            "RAM (đọc/ghi) và ROM (chỉ đọc), EPROM, Flash",
            "Cấu trúc ma trận hàng-cột, CAS/RAS",
            "Backplane bus (vd VMEbus) cho hệ thống nhiều bo mạch"]},
        {"title": "Kiến trúc bên trong CPU", "bullets": [
            "Accumulator, thanh ghi đa dụng, ALU",
            "Bộ đếm chương trình (PC) và con trỏ ngăn xếp (SP)",
            "Bus buffer và cách CPU giao tiếp với bus ngoài"]},
        {"title": "Chu trình lệnh & thời gian thực thi", "bullets": [
            "Chu trình fetch – decode – execute",
            "T-state, chu kỳ máy (machine cycle M0/M1/M2…)",
            "Tính thời gian thực thi lệnh từ tần số xung nhịp"]},
        {"title": "Kiến trúc nâng cao & ứng dụng hàng không", "bullets": [
            "Pipelining, kiến trúc ba bus",
            "Ngắt (interrupt) qua đường IRQ",
            "Ví dụ: Boeing 777 AIMS dùng 2 vi xử lý giống hệt cho hệ thống avionics tới hạn"]},
      ],
      "formula_label": "Thời gian thực thi lệnh theo T-state",
      "formula_math": "t = n_T × (1 / f_clk)",
      "legend": [("n_T", "số T-state mà lệnh cần"), ("f_clk", "tần số xung nhịp CPU (Hz)"), ("t", "thời gian thực thi lệnh")],
      "history_title": "📜 Bối cảnh lý thuyết & lịch sử",
      "history": "Vi xử lý thương mại đầu tiên, Intel 4004 (1971), chỉ có 2.300 transistor và xử lý 4-bit dữ liệu. "
                 "Kiến trúc CPU với accumulator, thanh ghi đa dụng và ALU trình bày trong chương này của Tooley "
                 "phản ánh trực tiếp dòng vi xử lý Intel x86 phát triển từ 8086 (1978): kiến trúc mà nhiều hệ "
                 "thống máy tính hàng không thế hệ trước dựa vào, trước khi chuyển sang các vi xử lý chuyên dụng "
                 "cho hàng không như AMD 29050 (dùng trong ASIC của Honeywell).",
      "case_title": "🔎 Case study thực tế: đồng hồ buồng lái Airbus (clock computer)",
      "case": "Đồng hồ buồng lái điện tử trên A320 (Figure 6.11, Tooley) là một máy tính hoàn chỉnh thu nhỏ: "
              "dao động thạch anh tạo xung UTC chính xác, vi xử lý xử lý dữ liệu thời gian, ROM lưu phần mềm "
              "điều khiển, RAM lưu dữ liệu tạm thời, và bộ mã hoá dữ liệu nối tiếp gửi thời gian ra bus ARINC "
              "429 cho các hệ thống khác sử dụng: minh hoạ đầy đủ mô hình IPO + 3 bus trong một ứng dụng thực.",
      "warn_title": "⚠️ Bẫy hay gặp",
      "warn": "Nhầm lẫn giữa 'bộ nhớ truy cập ngẫu nhiên' (random access, nghĩa kỹ thuật là mọi ô nhớ truy xuất "
              "nhanh như nhau) với RAM (read/write memory) theo cách dùng thông thường. Về mặt kỹ thuật, ROM "
              "CŨNG là bộ nhớ truy cập ngẫu nhiên (không phải tuần tự như băng từ), dù không thể ghi được.",
      "notebook_desc": "Notebook đi kèm: tính thời gian thực thi lệnh theo T-state/tần số xung nhịp, tính dung "
                        "lượng bộ nhớ cần thiết từ số IC DRAM, và mô phỏng đơn giản chu trình fetch-decode-execute "
                        ": cộng thêm mục giải các bài tập chương 11 của Floyd không cần hình vẽ gốc (địa chỉ bộ "
                        "nhớ, RAM tĩnh).",
    },
    "en": {
      "title": "Computer Structure & Microprocessors (CPU)",
      "tag": "Computers & Microprocessors",
      "src": "Tooley ch.6-7 (p.95-138) · Floyd ch.11 (semiconductor memory, p.627-696)",
      "intro": "Every aircraft computer, from the cockpit clock to the AIDS data recorder, rests on three basic "
               "blocks: the CPU, memory (RAM/ROM), and the interconnecting bus system. This module covers "
               "computer structure, CPU operating principles, and the semiconductor memory types used in avionics.",
      "parts": [
        {"title": "Basic structure of a computer system", "bullets": [
            "The IPO model: Input → Process → Output",
            "Three buses: address, data, control",
            "Examples: the cockpit clock computer and the AIDS data recorder"]},
        {"title": "Semiconductor memory", "bullets": [
            "RAM (read/write) and ROM (read-only), EPROM, Flash",
            "Row-column matrix structure, CAS/RAS",
            "Backplane buses (e.g. VMEbus) for multi-board systems"]},
        {"title": "Internal CPU architecture", "bullets": [
            "Accumulator, general-purpose registers, ALU",
            "Program Counter (PC) and Stack Pointer (SP)",
            "Bus buffers and how the CPU talks to the external bus"]},
        {"title": "Instruction cycle & execution timing", "bullets": [
            "The fetch – decode – execute cycle",
            "T-states, machine cycles (M0/M1/M2…)",
            "Computing instruction execution time from clock frequency"]},
        {"title": "Advanced architecture & aviation applications", "bullets": [
            "Pipelining, three-bus architecture",
            "Interrupts via the IRQ line",
            "Example: Boeing 777 AIMS uses two identical microprocessors for a critical avionics system"]},
      ],
      "formula_label": "Instruction execution time from T-states",
      "formula_math": "t = n_T × (1 / f_clk)",
      "legend": [("n_T", "number of T-states the instruction requires"), ("f_clk", "CPU clock frequency (Hz)"), ("t", "instruction execution time")],
      "history_title": "📜 Theoretical & historical background",
      "history": "The first commercial microprocessor, the Intel 4004 (1971), had only 2,300 transistors and "
                 "processed 4-bit data. The CPU architecture with accumulator, general-purpose registers and ALU "
                 "described in this chapter of Tooley directly reflects the Intel x86 family that grew from the "
                 "8086 (1978): an architecture many earlier-generation aircraft computers relied on, before "
                 "moving to aviation-specific processors such as the AMD 29050 (used in Honeywell's ASIC).",
      "case_title": "🔎 Real case study: the Airbus cockpit clock computer",
      "case": "The A320's electronic cockpit clock (Figure 6.11, Tooley) is a complete miniature computer: a "
              "crystal oscillator generates a precise UTC time base, a microprocessor processes the time data, "
              "ROM stores the control software, RAM holds working data, and a serial data encoder sends the time "
              "out on the ARINC 429 bus for other systems to use: a full illustration of the IPO model plus the "
              "three-bus architecture in a real application.",
      "warn_title": "⚠️ Common trap",
      "warn": "Confusing 'random access memory' (the technical meaning: every cell is accessed with equal ease) "
              "with RAM (read/write memory) in everyday usage. Technically, ROM is ALSO random-access memory "
              "(not sequential like magnetic tape), even though it cannot be written to.",
      "notebook_desc": "Companion notebook: computes instruction execution time from T-states/clock frequency, "
                        "computes required memory capacity from the number of DRAM chips, and simulates a simple "
                        "fetch-decode-execute cycle: plus a section solving Floyd Chapter 11's figure-free "
                        "Problems (memory addressing, static RAM).",
    },
  },
  {
    "slug": "05-data-buses",
    "num": "05",
    "target_slides": 28,
    "vi": {
      "title": "Bus dữ liệu hàng không (Data Buses)",
      "tag": "Data Buses",
      "src": "Tooley ch.4 (tr.53-69) · Bài giảng \"Data Buses\" (18 slide)",
      "intro": "Một máy bay hiện đại có hàng trăm LRU (Line Replaceable Unit) cần trao đổi dữ liệu với nhau. "
               "Thay vì nối dây riêng cho từng cặp thiết bị, các hệ thống avionics dùng BUS DỮ LIỆU: một (hoặc "
               "vài) đường truyền dùng chung theo đúng một chuẩn giao tiếp. Module này đi từ lý do cần bus, qua "
               "chuẩn phổ biến nhất (ARINC 429), tới các chuẩn khác (ARINC 629, AFDX/664, MIL-STD-1553) và ứng "
               "dụng thật trên Airbus A320.",
      "parts": [
        {"title": "Vì sao máy bay cần bus dữ liệu?", "bullets": [
            "Kết nối điểm-điểm (point-to-point): mỗi cảm biến nối dây riêng tới mỗi thiết bị dùng dữ liệu đó",
            "Vấn đề: số dây tăng rất nhanh, nặng, khó bảo trì, khó mở rộng",
            "Giải pháp: bus dữ liệu dùng chung, nhiều thiết bị chia sẻ cùng 1 đường truyền",
            "6 lý do dùng bus: giảm dây, chia sẻ dữ liệu, tăng độ tin cậy, dễ bảo trì, dễ mở rộng, hỗ trợ nhiều loại dữ liệu"]},
        {"title": "ARINC 429: chuẩn bus phổ biến nhất", "bullets": [
            "Bus điểm-điểm (point-to-point), 1 chiều (unidirectional), 1 transmitter → tối đa 20 receiver",
            "Cáp xoắn đôi có vỏ bọc (shielded twisted pair), điện áp ±5V trên mỗi dây, vi sai ±10V",
            "Mã hoá Bipolar Return to Zero (BPRZ): mỗi bit luôn trở về 0V, tự đồng bộ (self-clocking)",
            "Tốc độ: 12,5 kbps (low speed) hoặc 100 kbps (high speed)"]},
        {"title": "Cấu trúc 1 từ dữ liệu ARINC 429 (32 bit)", "bullets": [
            "Label (8 bit) → SDI (2 bit) → Data (19 bit) → SSM (2 bit) → Parity (1 bit)",
            "Label: mã nhận diện loại dữ liệu (vd 203 = tốc độ bay IAS)",
            "Hai định dạng Data: BCD (mỗi chữ số thập phân 4 bit) hoặc BNR (số nhị phân có dấu, bù hai)",
            "SSM báo trạng thái dữ liệu (hợp lệ/lỗi/đang kiểm tra), Parity dùng bit lẻ để tự kiểm tra"]},
        {"title": "Các chuẩn bus khác", "bullets": [
            "ARINC 629: 2 Mbps, hai chiều, không cần bộ điều khiển trung tâm, dùng trên B777/A330/A340",
            "AFDX/ARINC 664: Ethernet chuyển mạch 100 Mbps, dùng Virtual Link, trên A380/A350",
            "MIL-STD-1553B: bus quân sự có bộ điều khiển trung tâm (bus controller), 1 Mbps",
            "Các chuẩn cũ/đặc thù: ARINC 419/561/573/575/615/708, CSDB, ASCB, FDDI"]},
        {"title": "Áp dụng trên Airbus A320", "bullets": [
            "ADIRU → FMGC/EFIS qua ARINC 429: dữ liệu khí động, quán tính",
            "ELAC/SEC/FAC ↔ nhau qua ARINC 629: dữ liệu điều khiển bay thời gian thực",
            "FMS ↔ ECAM ↔ CIDS ↔ ACMS qua AFDX: dữ liệu khối lượng lớn, bảo trì",
            "FADEC dùng MIL-STD-1553/ARINC 717: dữ liệu động cơ, ghi âm buồng lái"]},
      ],
      "formula_label": "Thời gian truyền 1 từ dữ liệu ARINC 429 (32 bit)",
      "formula_math": "t_từ = N_bit / R  (N=32 bit; R=12,5 kbps ⇒ t=2,56 ms; R=100 kbps ⇒ t=0,32 ms)",
      "legend": [("N_bit", "số bit trong 1 từ dữ liệu (ARINC 429 luôn là 32 bit)"), ("R", "tốc độ truyền (bit/giây)"), ("t_từ", "thời gian truyền trọn 1 từ dữ liệu")],
      "history_title": "📜 Bối cảnh lý thuyết & lịch sử",
      "history": "ARINC (Aeronautical Radio, Inc.) là một tổ chức gồm các hãng hàng không lớn và nhà sản xuất máy "
                 "bay, với mục tiêu chuẩn hoá thiết bị hàng không để các LRU của nhiều hãng sản xuất khác nhau vẫn "
                 "tương thích được với nhau. ARINC 429 có tên kỹ thuật đầy đủ là <i>Mark 33 Digital Information "
                 "Transfer System (DITS)</i>, và theo đúng lời sách Tooley, đây vẫn là một trong những chuẩn bus "
                 "phổ biến nhất trên máy bay thương mại (Airbus A310/A320/A330/A340; Boeing 737/747/757/767; "
                 "McDonnell Douglas MD-11), dù các máy bay mới hơn như A380 và Boeing 777 đã chuyển sang các "
                 "chuẩn nhanh hơn, hai chiều hơn (ARINC 629, AFDX).",
      "case_title": "🔎 Case study thực tế: đo tốc độ bay IAS từ ADIRU tới PFD trên A320",
      "case": "ADIRU tính được tốc độ bay chỉ thị (IAS) = 250 kt, mã hoá theo định dạng BCD rồi gắn vào 1 từ "
              "dữ liệu 32 bit mang đúng Label dành riêng cho IAS. Giá trị 250 được tách thành 3 chữ số BCD: "
              "2→0010, 5→0101, 0→0000, ghép vào 19 bit trường Data (tự kiểm chứng lại được bằng notebook đi "
              "kèm). Từ dữ liệu 32 bit hoàn chỉnh (Label + SDI + Data + SSM + Parity) được gửi liên tục mỗi "
              "khoảng 100 ms qua ARINC 429 BUS A tới PFD, nơi bộ giải mã kiểm tra parity, đọc Label để biết đây "
              "là dữ liệu IAS, rồi cập nhật thước đo tốc độ hiển thị 250 kt. Đây là ví dụ đầy đủ cả chu trình: "
              "mã hoá → truyền → giải mã → hiển thị, dựa theo đúng kịch bản trong slide bài giảng. (Riêng giá "
              "trị số cụ thể của Label mà slide ghi không khớp phép đổi hex/nhị phân độc lập, xem mục cảnh báo "
              "bên dưới, nên không trích lại số Label đó ở đây.)",
      "warn_title": "⚠️ Bẫy hay gặp (và một lỗi thật tìm thấy ngay trong bài giảng)",
      "warn": "Bẫy phổ biến: nhầm \"tốc độ cao nhất 100 kbps\" của ARINC 429 với tốc độ Mbps của ARINC 629 "
              "(2 Mbps) hay MIL-STD-1553 (1 Mbps); đây là 3 chuẩn khác nhau, chênh lệch tốc độ tới hàng chục lần. "
              "Đáng chú ý hơn: một slide trong chính bài giảng môn này ghi mã hoá của ARINC 429 là \"Manchester "
              "Biphase-L\", nhưng đối chiếu với sách Tooley (mục Electrical Characteristics, và bảng chú giải "
              "thuật ngữ BPRZ) cũng như 2 slide khác trong CÙNG bài giảng đó, mã hoá ĐÚNG của ARINC 429 là "
              "Bipolar Return to Zero (BPRZ), không phải Manchester (Manchester là mã hoá của ARINC 708/573, "
              "một chuẩn bus KHÁC). Đây là một ví dụ thực tế cho thấy luôn cần đối chiếu nhiều nguồn trước khi "
              "ghi nhớ một sự kiện kỹ thuật.",
      "notebook_desc": "Notebook đi kèm: mã hoá/giải mã 1 từ ARINC 429 (Label/SDI/Data BCD hoặc BNR/SSM/Parity) "
                        "bằng Python, tự kiểm tra lại toàn bộ 17 câu hỏi gốc cuối chương 4 sách Tooley bằng code.",
    },
    "en": {
      "title": "Aircraft Data Buses",
      "tag": "Data Buses",
      "src": "Tooley ch.4 (p.53-69) · Lecture \"Data Buses\" (18 slides)",
      "intro": "A modern aircraft has hundreds of LRUs (Line Replaceable Units) that need to exchange data. "
               "Instead of wiring every device pair separately, avionics systems use a DATA BUS: one (or a few) "
               "shared transmission lines following a single communication standard. This module goes from why a "
               "bus is needed, through the most common standard (ARINC 429), to other standards (ARINC 629, "
               "AFDX/664, MIL-STD-1553) and real applications on the Airbus A320.",
      "parts": [
        {"title": "Why does an aircraft need a data bus?", "bullets": [
            "Point-to-point wiring: each sensor is wired separately to every device that needs its data",
            "Problem: the number of wires grows very fast, adding weight, hurting maintainability and expandability",
            "Solution: a shared data bus, with multiple devices sharing the same transmission line",
            "6 reasons to use a bus: fewer wires, shared data, higher reliability, easier maintenance, easier expansion, support for multiple data types"]},
        {"title": "ARINC 429: the most common bus standard", "bullets": [
            "Point-to-point, unidirectional bus: 1 transmitter → up to 20 receivers",
            "Shielded twisted pair cable, ±5V on each wire, ±10V differential",
            "Bipolar Return to Zero (BPRZ) encoding: every bit returns to 0V, self-clocking",
            "Data rate: 12.5 kbps (low speed) or 100 kbps (high speed)"]},
        {"title": "Structure of an ARINC 429 word (32 bits)", "bullets": [
            "Label (8 bits) → SDI (2 bits) → Data (19 bits) → SSM (2 bits) → Parity (1 bit)",
            "Label: identifies the data type (e.g. 203 = indicated airspeed, IAS)",
            "Two Data formats: BCD (each decimal digit as 4 bits) or BNR (signed binary, two's complement)",
            "SSM reports data status (valid/failure/test), Parity uses odd parity for self-checking"]},
        {"title": "Other bus standards", "bullets": [
            "ARINC 629: 2 Mbps, bidirectional, no central bus controller needed, used on B777/A330/A340",
            "AFDX/ARINC 664: 100 Mbps switched Ethernet, uses Virtual Links, on A380/A350",
            "MIL-STD-1553B: military bus with a central bus controller, 1 Mbps",
            "Older/specialised standards: ARINC 419/561/573/575/615/708, CSDB, ASCB, FDDI"]},
        {"title": "Application on the Airbus A320", "bullets": [
            "ADIRU → FMGC/EFIS via ARINC 429: air data and inertial data",
            "ELAC/SEC/FAC interlinked via ARINC 629: real-time flight control data",
            "FMS ↔ ECAM ↔ CIDS ↔ ACMS via AFDX: large-volume data, maintenance",
            "FADEC uses MIL-STD-1553/ARINC 717: engine data, cockpit voice/data recording"]},
      ],
      "formula_label": "Transmission time for one ARINC 429 word (32 bits)",
      "formula_math": "t_word = N_bit / R  (N=32 bits; R=12.5 kbps ⇒ t=2.56 ms; R=100 kbps ⇒ t=0.32 ms)",
      "legend": [("N_bit", "number of bits per data word (ARINC 429 is always 32 bits)"), ("R", "transmission rate (bits/second)"), ("t_word", "time to transmit one complete data word")],
      "history_title": "📜 Theoretical & historical background",
      "history": "ARINC (Aeronautical Radio, Inc.) is an organisation of major airlines and aircraft manufacturers "
                 "whose goal is to standardise aircraft equipment so that LRUs from different manufacturers remain "
                 "interoperable. ARINC 429's full technical name is the <i>Mark 33 Digital Information Transfer "
                 "System (DITS)</i>, and per Tooley's own text it remains one of the most widely used bus "
                 "standards on commercial aircraft (Airbus A310/A320/A330/A340; Boeing 737/747/757/767; "
                 "McDonnell Douglas MD-11), even though newer aircraft such as the A380 and Boeing 777 have "
                 "moved to faster, bidirectional standards (ARINC 629, AFDX).",
      "case_title": "🔎 Real case study: measuring IAS from the ADIRU to the PFD on the A320",
      "case": "The ADIRU computes an indicated airspeed (IAS) of 250 kt, encodes it in BCD format, and packs "
              "it into a 32-bit word carrying the dedicated Label for IAS. The value 250 splits into three BCD "
              "digits: 2→0010, 5→0101, 0→0000, packed into the 19-bit Data field (independently checkable with "
              "the companion notebook). The complete 32-bit word (Label + SDI + Data + SSM + Parity) is sent "
              "continuously about every 100 ms over ARINC 429 BUS A to the PFD, where the decoder checks parity, "
              "reads the Label to identify IAS data, and updates the airspeed display to 250 kt. This is a "
              "complete worked example of the full cycle (encode → transmit → decode → display), following the "
              "same scenario as the lecture slide. (The slide's specific Label figure does not survive an "
              "independent hex/binary cross-check, see the warning box below, so that specific number is not "
              "repeated here.)",
      "warn_title": "⚠️ Common trap (and a real error found in the lecture material itself)",
      "warn": "Common trap: confusing ARINC 429's top speed of 100 kbps with the Mbps-range speeds of ARINC 629 "
              "(2 Mbps) or MIL-STD-1553 (1 Mbps): these are three different standards, tens of times apart in "
              "speed. More notably: one slide in this very course's lecture deck states that ARINC 429 uses "
              "\"Manchester Biphase-L\" encoding, but cross-checking against Tooley (the Electrical "
              "Characteristics section, and the BPRZ glossary entry) and two OTHER slides in that SAME lecture "
              "deck shows the CORRECT encoding for ARINC 429 is Bipolar Return to Zero (BPRZ), not Manchester "
              "(Manchester is used by ARINC 708/573, a DIFFERENT bus standard). This is a real example of why "
              "cross-checking multiple sources matters before memorising a technical fact.",
      "notebook_desc": "Companion notebook: encodes/decodes an ARINC 429 word (Label/SDI/Data as BCD or BNR/SSM/"
                        "Parity) in Python, and re-checks all 17 original end-of-chapter-4 questions from Tooley "
                        "by code.",
    },
  },
]
