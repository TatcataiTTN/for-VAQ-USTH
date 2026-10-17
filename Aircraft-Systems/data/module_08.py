# -*- coding: utf-8 -*-
"""Module 08: Cap quang trong may bay (Fibre Optics). Nguon: bai giang 'Optic_Fiber_ver 2026' (37 slide) + Tooley Ch.10 (tr.162-177)
+ Floyd Ch.13 muc 13-1 (tr.740-745; bai 4-8 tr.793; dap an A-27)."""
DEMO_VI = ("<div class='demo-box'><h3>🧪 Demo 1: máy tính sợi quang (chạy ngay trong trình duyệt)</h3>"
  "<p>Mặc định là sợi của bài tập slide 20 (n₁ = 1,53; n₂ = 1,50; SiO₂) với lõi 62,5 µm ở 1300 nm. Đổi số để xem góc tới hạn, khẩu độ số, tần số chuẩn hoá V, số mode và chiều dài tối đa theo ngân sách suy hao (bài slide 27: 1 mW vào, 50 µW tối thiểu, 0,35 dB/km).</p>"
  "<div class='demo-fibre-calc' data-lang='vi'></div></div>"
  "<div class='demo-box'><h3>🧪 Demo 2: tia sáng tại biên hai môi trường (định luật Snell và phản xạ toàn phần)</h3>"
  "<p>Môi trường tới n₁ nằm dưới biên. Kéo thanh trượt qua góc tới hạn để thấy tia khúc xạ biến mất và chỉ còn tia phản xạ.</p>"
  "<div class='demo-fibre-ray' data-lang='vi'></div></div>")
DEMO_EN = (DEMO_VI.replace("data-lang='vi'", "data-lang='en'")
  .replace("🧪 Demo 1: máy tính sợi quang (chạy ngay trong trình duyệt)", "🧪 Demo 1: fibre calculator (runs in your browser)")
  .replace("Mặc định là sợi của bài tập slide 20 (n₁ = 1,53; n₂ = 1,50; SiO₂) với lõi 62,5 µm ở 1300 nm. Đổi số để xem góc tới hạn, khẩu độ số, tần số chuẩn hoá V, số mode và chiều dài tối đa theo ngân sách suy hao (bài slide 27: 1 mW vào, 50 µW tối thiểu, 0,35 dB/km).",
           "Defaults are the fibre of the slide 20 exercise (n₁ = 1.53; n₂ = 1.50; SiO₂) with a 62.5 µm core at 1300 nm. Change the numbers to see the critical angle, numerical aperture, normalised frequency V, number of modes and the maximum length from the attenuation budget (slide 27 exercise: 1 mW in, 50 µW minimum, 0.35 dB/km).")
  .replace("🧪 Demo 2: tia sáng tại biên hai môi trường (định luật Snell và phản xạ toàn phần)", "🧪 Demo 2: a light ray at the boundary of two media (Snell's law and total internal reflection)")
  .replace("Môi trường tới n₁ nằm dưới biên. Kéo thanh trượt qua góc tới hạn để thấy tia khúc xạ biến mất và chỉ còn tia phản xạ.",
           "The incident medium n₁ is below the boundary. Drag the slider past the critical angle to see the refracted ray vanish and only the reflected ray remain."))

MOD08 = {
  "slug": "08-fibre-optics", "num": "08", "target_slides": 40,
  "demo": {"js": "demo_fibre.js", "html_vi": DEMO_VI, "html_en": DEMO_EN},
  "vi": {
    "title": "Cáp quang trên máy bay",
    "tag": "Fibre Optics",
    "src": "Tooley ch.10 (tr.162-177) · Bài giảng \"Fiber optics\" (37 slide) · Floyd ch.13 mục 13-1 (tr.740-745)",
    "intro": "Khi mạng avionics và giải trí cabin cần băng thông lớn hơn nhiều so với dây đồng (Module 05, 06), sợi quang trở thành lựa chọn: nhẹ, băng thông rất rộng, miễn nhiễm điện từ. Module này giải thích sợi quang dẫn sáng bằng phản xạ toàn phần ra sao, tính góc tới hạn, khẩu độ số và số mode, rồi đến suy hao, tán sắc, các loại sợi, cấu tạo cáp và hệ thống truyền tin, kèm hai demo chạy ngay trên trang.",
    "parts": [
      {"title": "Vì sao máy bay dùng sợi quang", "bullets": [
        "Sợi quang là ống dẫn sóng cho ánh sáng với tổn hao rất nhỏ; cấu tạo gồm lõi, vỏ phản xạ và lớp bảo vệ",
        "Ưu điểm: nhẹ, nhỏ, băng thông cực rộng, miễn nhiễm EMI, ít nhiễu xuyên âm, tin cậy; cáp đồng nặng gấp khoảng 5 lần, tiết kiệm đến khoảng 1 300 kg trên máy bay lớn",
        "Hạn chế: chi phí, độ chính xác khi lắp, bán kính uốn tối thiểu, độ bền cơ học",
        "A380, Boeing 787 và Boeing 777 (ARINC 636) đã có mạng quang; máy bay cũ cần nâng cấp, nhất là cho giải trí"]},
      {"title": "Ánh sáng, chiết suất và định luật Snell", "bullets": [
        "Ánh sáng là sóng điện từ: λ = v/f; tốc độ trong vật liệu v = c/n với n = √ε_r",
        "Định luật Snell: n₁ sin θi = n₂ sin θr; từ chiết suất thấp vào cao thì tia gập về pháp tuyến",
        "Góc tới hạn sin θc = n₂/n₁ (n₁ > n₂), tại đó tia khúc xạ chạy dọc biên (90°)",
        "Với θi > θc có phản xạ toàn phần: toàn bộ ánh sáng quay lại môi trường cũ"]},
      {"title": "Dẫn sáng trong sợi: góc chấp nhận, NA và mode", "bullets": [
        "Ánh sáng được giữ trong lõi bằng chuỗi phản xạ toàn phần, kể cả khi sợi bị uốn",
        "Góc chấp nhận θa và khẩu độ số: NA = sin θa = √(n₁² − n₂²) trong không khí",
        "Tần số chuẩn hoá V = π d NA / λ; số mode N ≈ V²/2 với sợi đa mode chiết suất bậc",
        "Mỗi tia với một góc truyền khác nhau là một mode; mode bậc cao đi đường dài hơn"]},
      {"title": "Suy hao, tán sắc và các loại sợi", "bullets": [
        "Suy hao P(z) = P_in e^(−αz); A(dB/km) = −(10/L) log₁₀[P(L)/P(0)]; cực tiểu quanh 1310 nm và 1550 nm",
        "Tán sắc mode (sợi đa mode) và tán sắc màu (vật liệu) làm giãn xung, giới hạn tốc độ dữ liệu",
        "Ba loại: đa mode chiết suất bậc, đa mode chiết suất biến thiên, đơn mode; đơn mode có băng thông cao nhất",
        "Cáp thực tế: 5 sợi + 2 sợi đệm, băng keo, sợi aramid chịu kéo, vỏ ngoài; buffer mã màu"]},
      {"title": "Hệ thống truyền thông tin quang", "bullets": [
        "Bộ phát (LED hoặc laser 850, 1310, 1550 nm) → đầu nối → sợi → bộ thu (photodiode PIN hoặc APD)",
        "Đầu nối phải căn chỉnh chính xác và sạch; ánh sáng hồng ngoại vô hình có thể làm tổn thương mắt",
        "ARINC 636 (dựa trên FDDI, 100 Mbps) cho AVLAN và CABLAN của Boeing 777",
        "Ứng dụng tương lai: truyền dữ liệu, liên lạc an toàn, cảm biến quang (va chạm, biến dạng, nhiệt độ)"]},
    ],
    "formula_label": "Góc tới hạn, khẩu độ số, số mode và suy hao",
    "formula_math": "sin θc = n₂/n₁  ·  NA = √(n₁² − n₂²)  ·  V = π d NA / λ  ·  N ≈ V²/2<br>A (dB/km) = −(10/L) log₁₀[P(L)/P(0)]  ⇒  L_max = 10 log₁₀(P_in/P_min) / A",
    "legend": [
      ["n₁, n₂", "chiết suất của lõi và của vỏ (n₁ > n₂)"],
      ["θc", "góc tới hạn tại biên lõi và vỏ"],
      ["NA", "khẩu độ số, bằng sin của góc chấp nhận khi ở không khí"],
      ["d, λ", "đường kính lõi và bước sóng trong chân không"],
      ["V, N", "tần số chuẩn hoá và số mode truyền được"],
      ["A, L_max", "suy hao theo dB/km và chiều dài sợi tối đa với ngân sách công suất"],
    ],
    "history_title": "📜 Bối cảnh lý thuyết và lịch sử",
    "history": "Theo bài giảng, năm 1910 Hondros và Debye phân tích lý thuyết ống dẫn sóng điện môi và chỉ ra ánh sáng có thể được dẫn trong cấu trúc trụ nhờ phản xạ toàn phần. Năm 1970 Corning chế tạo sợi quang thực dụng đầu tiên với suy hao dưới 20 dB/km, mở đường cho truyền thông đường dài. Sợi quang xuất hiện trên máy bay từ khoảng 1990, vì truyền dữ liệu tốc độ cao, miễn nhiễm EMI và nhẹ. Theo Tooley, Boeing 777 là máy bay thương mại đầu tiên vào sản xuất với mạng cục bộ bằng sợi quang, phát triển từ thập niên 1980, gồm AVLAN ở buồng lái và khoang thiết bị điện, và CABLAN ở trần khoang khách, theo chuẩn ARINC 636 cải biên từ FDDI để đạt tới 100 Mbps.",
    "case_title": "🔎 Case study: nên dùng sợi quang nào cho một liên kết trên máy bay, và dài nhất bao nhiêu?",
    "case": "Giả sử một bộ phát công suất 1 mW, bộ thu đo được tối thiểu 50 µW, hoạt động ở 1310 nm trên sợi SiO₂ có suy hao 0,35 dB/km (bài tập slide 27). Ngân sách công suất là 10 log₁₀(1 mW / 50 µW) = 13,01 dB, nên chiều dài tối đa là 13,01 / 0,35 ≈ 37,2 km. Trên máy bay chỉ cần vài chục mét, nên ngân sách này rất dư; điều quan trọng hơn là đầu nối: Tooley tính sáu đầu nối, mỗi đầu 0,5 dB, tổng 3 dB, tương đương hàng km sợi. Với sợi đa mode lõi 62,5 µm, NA = 0,275 ở 1300 nm, V = 41,5 và khoảng 863 mode (bài slide 22), nên tán sắc mode là giới hạn chính của tốc độ. Vì thế mạng máy bay hiện nay vẫn dùng nhiều sợi đa mode (dễ cắt, nối, đầu nối), còn sợi đơn mode có băng thông cao hơn nhưng khó hơn khi căn chỉnh (Tooley 10.2.2).",
    "warn_title": "⚠️ Bẫy hay gặp (và các chỗ không khớp tìm thấy trong tài liệu)",
    "warn": "Bẫy chung: nhầm góc tới hạn θc (tính ở biên lõi và vỏ) với góc chấp nhận θa (tính ở đầu vào sợi, từ không khí). Với n₁ = 1,53 và n₂ = 1,50 thì θc = 78,6° còn θa chỉ 17,5°. Chính vì vậy slide 19 ghi \"θ₁ = θc = θa\" là không đúng: hai góc đó đo ở hai nơi khác nhau và không bằng nhau; điều kiện giới hạn đúng là góc φ tại biên (tính từ pháp tuyến) bằng θc, hay tương đương góc trong sợi so với trục bằng 90° − θc. Ký hiệu θ₁ cũng bị dùng khác nhau giữa slide 17 (góc trong không khí) và slide 19 (góc trong lõi). Slide 9 ghi nước có ε_r ≈ 80 nhưng n ≈ 1,33; √80 ≈ 8,9, không phải 1,33: ε_r = 80 là hằng số điện môi tĩnh, còn ở tần số ánh sáng ε_r ≈ 1,77 (= 1,33²). Slide 28 viết Δt ≈ (n₁ − n₂)L/c, thiếu hệ số n₁/n₂ (công thức đúng cho tia xiên tới hạn là n₁(n₁ − n₂)L/(c n₂)), và nói điển hình 10 đến 50 ns/km trong khi với n₁ − n₂ = 0,02 đến 0,04 công thức cho khoảng 67 đến 137 ns/km. Slide 30 ghi nhãn sợi chiết suất biến thiên là \"MM-SI\" trong khi bảng so sánh bên dưới ghi MM-GI. Slide 24 ghi suy hao 0,2 đến 0,5 dB/km ở 1550 nm còn slide 26 ghi 0,18 dB/km. Cuối cùng, Tooley mục 10.2 viết ngược quy tắc khúc xạ: sách nói khi ánh sáng đi từ chiết suất cao sang thấp thì tia \"bị bẻ về phía pháp tuyến\", nhưng theo định luật Snell tia bị bẻ ra xa pháp tuyến (slide 12 của bài giảng viết đúng); đây là câu chữ của sách mâu thuẫn với định luật Snell và với bài giảng, nên không dùng để học.",
    "notebook_desc": "Notebook đi kèm: tính lại góc tới hạn, NA, V và số mode cho cả bốn bài tập của bài giảng (slide 20, 22, 27, 36) và đối chiếu với đáp án in ở slide 36; ngân sách suy hao và chuyển đổi dB/km với Np/m; mô phỏng Snell và TIR; kiểm tra các điểm không khớp (θc và θa, nước ε_r, Δt giữa các mode, 20 câu Tooley chương 10)."
  },
  "en": {
    "title": "Fibre Optics in Aircraft",
    "tag": "Fibre Optics",
    "src": "Tooley ch.10 (p.162-177) · Lecture \"Fiber optics\" (37 slides) · Floyd ch.13 section 13-1 (p.740-745)",
    "intro": "When avionics and cabin networks need far more bandwidth than copper wire can give (Modules 05, 06), optical fibre becomes the choice: light, extremely wide bandwidth, immune to electromagnetic interference. This module explains how a fibre guides light by total internal reflection, how to compute the critical angle, numerical aperture and number of modes, then attenuation, dispersion, fibre types, cable construction and communication systems, with two live demos on the page.",
    "parts": [
      {"title": "Why aircraft use optical fibre", "bullets": [
        "An optical fibre is a waveguide for light with very little loss; it has a core, a reflective cladding and a protective layer",
        "Advantages: light, small, extremely wide bandwidth, immune to EMI, little crosstalk, reliable; copper is about 5 times heavier, saving up to about 1,300 kg on a large aircraft",
        "Drawbacks: cost, fitting precision, minimum bend radius, mechanical strength",
        "A380, Boeing 787 and Boeing 777 (ARINC 636) have optical networks; older aircraft need upgrades, especially for entertainment"]},
      {"title": "Light, refractive index and Snell's law", "bullets": [
        "Light is an electromagnetic wave: λ = v/f; speed in a material v = c/n with n = √ε_r",
        "Snell's law: n₁ sin θi = n₂ sin θr; from lower to higher index the ray bends toward the normal",
        "Critical angle sin θc = n₂/n₁ (n₁ > n₂), where the refracted ray runs along the boundary (90°)",
        "For θi > θc there is total internal reflection: all the light returns to the original medium"]},
      {"title": "Guiding light: acceptance angle, NA and modes", "bullets": [
        "Light is kept in the core by a chain of total internal reflections, even when the fibre is bent",
        "Acceptance angle θa and numerical aperture: NA = sin θa = √(n₁² − n₂²) in air",
        "Normalised frequency V = π d NA / λ; number of modes N ≈ V²/2 for multimode step-index fibre",
        "Each ray at a different propagation angle is a mode; higher-order modes travel longer paths"]},
      {"title": "Attenuation, dispersion and fibre types", "bullets": [
        "Attenuation P(z) = P_in e^(−αz); A(dB/km) = −(10/L) log₁₀[P(L)/P(0)]; minima near 1310 nm and 1550 nm",
        "Modal dispersion (multimode) and chromatic (material) dispersion stretch pulses and limit the data rate",
        "Three types: multimode step-index, multimode graded-index, single-mode; single-mode has the highest bandwidth",
        "Real cable: 5 fibres + 2 fillers, tape, aramid strength member, outer jacket; colour-coded buffers"]},
      {"title": "An optical communication system", "bullets": [
        "Transmitter (LED or laser at 850, 1310, 1550 nm) → connector → fibre → receiver (PIN or APD photodiode)",
        "Connectors must be precisely aligned and clean; invisible infrared light can damage the eyes",
        "ARINC 636 (based on FDDI, 100 Mbps) for the Boeing 777 AVLAN and CABLAN",
        "Future uses: data communications, secure links, fibre sensing (impact, strain, temperature)"]},
    ],
    "formula_label": "Critical angle, numerical aperture, mode count and attenuation",
    "formula_math": "sin θc = n₂/n₁  ·  NA = √(n₁² − n₂²)  ·  V = π d NA / λ  ·  N ≈ V²/2<br>A (dB/km) = −(10/L) log₁₀[P(L)/P(0)]  ⇒  L_max = 10 log₁₀(P_in/P_min) / A",
    "legend": [
      ["n₁, n₂", "refractive indices of the core and of the cladding (n₁ > n₂)"],
      ["θc", "critical angle at the core-cladding boundary"],
      ["NA", "numerical aperture, equal to the sine of the acceptance angle in air"],
      ["d, λ", "core diameter and vacuum wavelength"],
      ["V, N", "normalised frequency and number of propagating modes"],
      ["A, L_max", "attenuation in dB/km and the maximum fibre length for a power budget"],
    ],
    "history_title": "📜 Theory and historical background",
    "history": "According to the lecture, in 1910 Hondros and Debye analysed dielectric waveguides theoretically and showed that light can be guided in a cylindrical structure by total internal reflection. In 1970 Corning made the first practical optical fibre with attenuation below 20 dB/km, opening the way to long-distance communication. Optical fibre entered aircraft around 1990 for high-speed data, EMI immunity and low weight. Per Tooley, the Boeing 777 was the first commercial aircraft to enter production with an optical-fibre LAN, developed in the 1980s, comprising an AVLAN in the flight deck and electrical equipment bay and a CABLAN in the cabin roof, conforming to ARINC 636, adapted from FDDI to reach 100 Mbps.",
    "case_title": "🔎 Case study: which fibre for an aircraft link, and how long can it be?",
    "case": "Suppose a transmitter of 1 mW, a receiver that can measure at least 50 µW, working at 1310 nm on SiO₂ fibre with 0.35 dB/km attenuation (the slide 27 exercise). The power budget is 10 log₁₀(1 mW / 50 µW) = 13.01 dB, so the maximum length is 13.01 / 0.35 ≈ 37.2 km. An aircraft only needs a few tens of metres, so this budget is generous; connectors matter more: Tooley counts six connectors at 0.5 dB each, 3 dB in total, equal to several kilometres of fibre. For a multimode fibre with a 62.5 µm core, NA = 0.275 at 1300 nm, V = 41.5 and about 863 modes (the slide 22 exercise), so modal dispersion is the main limit on speed. That is why today's aircraft networks still use a lot of multimode fibre (easier to cut, splice and connect), while single-mode has higher bandwidth but is harder to align (Tooley 10.2.2).",
    "warn_title": "⚠️ Common traps (and mismatches found in the material)",
    "warn": "General trap: mixing up the critical angle θc (computed at the core-cladding boundary) with the acceptance angle θa (computed at the fibre input, from air). With n₁ = 1.53 and n₂ = 1.50, θc = 78.6° but θa is only 17.5°. That is why slide 19, which writes \"θ₁ = θc = θa\", is wrong: the two angles are measured in different places and are not equal; the correct limiting condition is that the angle φ at the boundary (measured from the normal) equals θc, equivalently that the ray angle to the fibre axis inside equals 90° − θc. The symbol θ₁ is also used differently on slide 17 (angle in air) and slide 19 (angle in the core). Slide 9 lists water with ε_r ≈ 80 but n ≈ 1.33; √80 ≈ 8.9, not 1.33: ε_r = 80 is the static permittivity, while at light frequencies ε_r ≈ 1.77 (= 1.33²). Slide 28 writes Δt ≈ (n₁ − n₂)L/c, missing a factor n₁/n₂ (the correct expression for the critical ray is n₁(n₁ − n₂)L/(c n₂)), and gives a typical 10 to 50 ns/km whereas n₁ − n₂ = 0.02 to 0.04 gives about 67 to 137 ns/km. Slide 30 labels the graded-index fibre \"MM-SI\" while the comparison table below says MM-GI. Slide 24 gives 0.2 to 0.5 dB/km at 1550 nm while slide 26 gives 0.18 dB/km. Finally, Tooley section 10.2 states the refraction rule backwards: the book says that going from higher to lower refractive index the ray is \"bent towards the normal\", but by Snell's law it bends away from the normal (lecture slide 12 states it correctly); the book's wording contradicts Snell's law and the lecture, so do not use it for study.",
    "notebook_desc": "Companion notebook: recomputes the critical angle, NA, V and mode count for all four lecture exercises (slides 20, 22, 27, 36) and compares them with the printed answer on slide 36; attenuation budget and the dB/km to Np/m conversion; Snell and TIR simulation; checks of the mismatches (θc versus θa, water ε_r, inter-mode Δt, the 20 Tooley chapter 10 questions)."
  },
}
