# -*- coding: utf-8 -*-
"""Slide Module 06 (VI + EN): body + explain (giai thich cho nguoi moi) + img.
Moi slide khai bao 1 lan voi du ca 2 ngon ngu de tranh loi 'ban EN dung lai chu VI'."""

def fig(name, alt):
    src = "../../../assets/figures/" + name
    return (f"<figure class='slide-fig'><a href='{src}' target='_blank' rel='noopener'>"
            f"<img src='{src}' alt='{alt}' loading='lazy'/></a></figure>")

# (title_vi, title_en, body_vi, body_en, explain_vi, explain_en, img)
S = [
# ------------------------------------------------------------------ PART 1
[
("Buồng lái 100 năm: từ không có đồng hồ đến buồng lái kính",
 "A century of cockpits: from no instruments to the glass cockpit",
 "<table class='tt'><thead><tr><th>Mốc</th><th>Buồng lái</th></tr></thead><tbody>"
 "<tr><td>1903</td><td>Wright Flyer: không có buồng lái, không đồng hồ</td></tr>"
 "<tr><td>1918</td><td>Khoảng 10 đồng hồ cơ bản (tốc độ, độ cao, la bàn, vòng tua động cơ)</td></tr>"
 "<tr><td>1969, 1970</td><td>Khoảng 600 đồng hồ (Boeing 707, rồi 747): tải công việc rất cao</td></tr>"
 "<tr><td>1976</td><td>Concorde: buồng lái analog tiên tiến nhưng nặng và phức tạp</td></tr>"
 "<tr><td>Thập niên 1990</td><td>Chuyển sang màn hình số CRT</td></tr>"
 "<tr><td>Thập niên 2000</td><td>Màn hình LCD thay đồng hồ analog (A320, A330, A340)</td></tr>"
 "<tr><td>Ngày nay</td><td>Màn hình lớn LCD/OLED đa chức năng, cảm ứng (A350, Boeing 787)</td></tr></tbody></table>",
 "<table class='tt'><thead><tr><th>Date</th><th>Cockpit</th></tr></thead><tbody>"
 "<tr><td>1903</td><td>Wright Flyer: no cockpit, no instruments</td></tr>"
 "<tr><td>1918</td><td>About 10 basic instruments (speed, altitude, compass, engine rpm)</td></tr>"
 "<tr><td>1969, 1970</td><td>About 600 instruments (Boeing 707, then 747): very high workload</td></tr>"
 "<tr><td>1976</td><td>Concorde: advanced analogue cockpit, but heavy and complex</td></tr>"
 "<tr><td>1990s</td><td>Move to digital CRT displays</td></tr>"
 "<tr><td>2000s</td><td>LCD screens replace analogue gauges (A320, A330, A340)</td></tr>"
 "<tr><td>Today</td><td>Large multifunction LCD/OLED touch screens (A350, Boeing 787)</td></tr></tbody></table>",
 "<p>Lịch sử này gói trong một xu hướng: càng về sau, số đồng hồ riêng lẻ giảm còn số thông tin trên mỗi màn hình tăng. Hàng trăm đồng hồ ở thập niên 1960 và 1970 nghĩa là hàng trăm dây dẫn, hàng trăm điểm hỏng và rất nhiều thứ phi công phải liếc qua liên tục. Màn hình số gom nhiều dữ liệu vào cùng một chỗ, lại có thể đổi trang tuỳ giai đoạn bay.</p><p>Sách Tooley gọi kết quả cuối là <b>glass cockpit</b> (buồng lái kính), dùng CRT và LCD để hiển thị cùng loại thông tin mà trước kia dùng đồng hồ cơ điện (mục 1.1).</p>",
 "<p>This history wraps up one trend: later cockpits have fewer separate instruments and more information per screen. Hundreds of dials in the 1960s and 1970s meant hundreds of wires, hundreds of failure points and a lot for the pilot to scan constantly. A digital screen gathers data in one place and can change pages with the phase of flight.</p><p>Tooley calls the end result the <b>glass cockpit</b>: CRT and LCD screens show the same kind of information that used to come from electromechanical dials (section 1.1).</p>",
 "disp_p07.jpg"),

("Bốn thế hệ Airbus: A310, A320, A380, A350",
 "Four Airbus generations: A310, A320, A380, A350",
 "<table class='tt'><thead><tr><th>Năm</th><th>Máy bay</th><th>Điểm mới về hiển thị</th></tr></thead><tbody>"
 "<tr><td>1978</td><td>A310</td><td>Màn hình đa chức năng đầu tiên (màn hình điện tử hiển thị thông số động cơ và hệ thống)</td></tr>"
 "<tr><td>1988</td><td>A320</td><td>Buồng lái \"toàn màn hình\": 6 màn hình CRT, điều khiển bay điện, có FMS</td></tr>"
 "<tr><td>2007</td><td>A380</td><td>AMLCD độ sáng cao, IMA (avionics mô-đun tích hợp), thiết bị tương tác (FCU, MCDU, bàn phím)</td></tr>"
 "<tr><td>2015</td><td>A350</td><td>Màn hình LCD rất lớn, độ phân giải cao, cảm ứng, ít công tắc vật lý</td></tr></tbody></table>"
 "<p>Mục tiêu thiết kế xuyên suốt: đơn giản hoá nhiệm vụ của phi hành đoàn, tăng nhận thức tình huống, tăng an toàn và hiệu quả.</p>",
 "<table class='tt'><thead><tr><th>Year</th><th>Aircraft</th><th>What is new in displays</th></tr></thead><tbody>"
 "<tr><td>1978</td><td>A310</td><td>First multifunction displays (electronic screens for engine and system data)</td></tr>"
 "<tr><td>1988</td><td>A320</td><td>\"Full display\" cockpit: 6 CRT screens, electric flight controls, FMS</td></tr>"
 "<tr><td>2007</td><td>A380</td><td>High-brightness AMLCD, IMA (integrated modular avionics), interaction devices (FCU, MCDU, keypad)</td></tr>"
 "<tr><td>2015</td><td>A350</td><td>Very large high-resolution LCD, touch input, fewer physical switches</td></tr></tbody></table>"
 "<p>The design goal stays the same throughout: simplify the crew's task, improve situational awareness, improve safety and efficiency.</p>",
 "<p>Đếm số màn hình giúp nhớ mốc A320: hai PFD, hai ND và hai màn hình ECAM, tổng cộng sáu, đúng như slide ghi \"6 CRT displays\". Ở A350, mỗi bên phi công có màn hình lớn cỡ 15 inch và thêm màn hình thông tin trên máy bay (OIS), trong khi cách bố trí vẫn giống A320 để phi công chuyển loại máy bay dễ (slide gọi là cross crew qualification).</p><p>Lưu ý: slide ghi tên màn hình sớm của A310 là \"EICAS\", nhưng theo Tooley (mục 15.3) EICAS là tên của Boeing, còn Airbus gọi là ECAM. Hãy dùng ECAM khi nói về Airbus.</p>",
 "<p>Counting screens helps to remember the A320 milestone: two PFDs, two NDs and two ECAM screens make six, exactly as the slide says \"6 CRT displays\". On the A350 each pilot has a screen of about 15 inches and there are extra onboard information system (OIS) screens, while the layout stays similar to the A320 so pilots can transition easily (the slide calls it cross crew qualification).</p><p>Note: the slide labels the A310's early electronic displays \"EICAS\", but per Tooley (section 15.3) EICAS is Boeing's name and Airbus calls it ECAM. Use ECAM when talking about Airbus.</p>",
 "disp_p08.jpg"),

("Một hệ thống hiển thị phải đáp ứng những gì?",
 "What must a display system satisfy?",
 "<p>Slide chia yêu cầu làm ba nhóm:</p><ul>"
 "<li><b>Hiệu năng:</b> chịu môi trường máy bay (nhiệt độ, rung, sốc, ẩm), quang học (độ sáng và tương phản cao, màu chính xác, góc nhìn rộng, đọc được dưới nắng lẫn ban đêm), kích thước, trọng lượng, công suất, tản nhiệt.</li>"
 "<li><b>Nhân tố con người:</b> hỗ trợ các nhiệm vụ cất cánh, bay hành trình, tiếp cận, hạ cánh; giao diện HMI trực quan, ký hiệu và màu nhất quán.</li>"
 "<li><b>Dịch vụ và hệ thống:</b> an toàn (BITE, dự phòng, không đưa thông tin gây hiểu lầm), chứng nhận (DO-160 môi trường, DO-178 phần mềm, DO-254 phần cứng, ARP 4754A và ARP 4761 an toàn hệ thống), chức năng (PFD, ND, EWD/SD, MFD), chế tạo và bảo trì (LRU).</li></ul>",
 "<p>The slide splits the requirements into three groups:</p><ul>"
 "<li><b>Performance:</b> survive the aircraft environment (temperature, vibration, shock, humidity), optics (high brightness and contrast, accurate colour, wide viewing angle, readable in sunlight and at night), size, weight, power, cooling.</li>"
 "<li><b>Human factors:</b> support take-off, cruise, approach and landing tasks; an intuitive HMI with consistent symbology and colour.</li>"
 "<li><b>Services and system:</b> safety (BITE, redundancy, no misleading information), certification (DO-160 environment, DO-178 software, DO-254 hardware, ARP 4754A and ARP 4761 system safety), functions (PFD, ND, EWD/SD, MFD), manufacturing and maintenance (LRU).</li></ul>",
 "<p>Điểm hay bị bỏ sót: màn hình trên máy bay là thiết bị an toàn bay, nên chuẩn chứng nhận của nó tách thành ba tầng. DO-160 kiểm tra thiết bị chịu nhiệt, rung, nhiễu điện từ; DO-178 quản lý chất lượng phần mềm; DO-254 quản lý chất lượng phần cứng điện tử. Một màn hình bán lẻ có thể sáng hơn nhưng không qua được ba tầng này.</p><p>BITE (built-in test equipment) là khả năng tự kiểm tra: thiết bị phát hiện lỗi của chính nó và báo lên hệ thống bảo trì (xem phần 5).</p>",
 "<p>An easily missed point: an aircraft display is flight-safety equipment, so its certification has three layers. DO-160 tests environmental tolerance (temperature, vibration, electromagnetic interference); DO-178 governs software quality; DO-254 governs electronic hardware quality. A retail screen might be brighter but would not pass all three.</p><p>BITE (built-in test equipment) is self-test capability: the equipment detects its own faults and reports them to the maintenance system (see part 5).</p>",
 "disp_p02.jpg"),

("Cách tiếp cận chức năng: từ dữ liệu đến mắt phi công",
 "The functional approach: from data to the pilot's eye",
 "<p>Chuỗi tín hiệu trong buồng lái gồm năm khối:</p><ol>"
 "<li><b>Nguồn dữ liệu:</b> cảm biến (khí động, tư thế, động cơ), máy tính (FMGC, FADEC), dữ liệu dẫn đường (VOR, ILS, GNSS), giám sát (TCAS).</li>"
 "<li><b>Tạo đồ hoạ (graphic generator):</b> nhận dữ liệu qua bus A429 hoặc AFDX, tạo đối tượng (đường, chữ, ký hiệu, ảnh), quản lý độ sáng và lớp.</li>"
 "<li><b>Màn hình (display unit):</b> nhận tín hiệu video (LVDS/Display port) và hiển thị.</li>"
 "<li><b>HMI:</b> phi công đọc và tác động bằng nút, núm, cảm ứng; lệnh chọn trang, chế độ, độ sáng.</li>"
 "<li><b>Môi trường:</b> nắng, nhiệt độ, rung, ẩm tác động lên cả hệ thống.</li></ol>",
 "<p>The cockpit signal chain has five blocks:</p><ol>"
 "<li><b>Data sources:</b> sensors (air data, attitude, engine), computers (FMGC, FADEC), navigation data (VOR, ILS, GNSS), surveillance (TCAS).</li>"
 "<li><b>Graphic generator:</b> receives data over A429 or AFDX buses, builds objects (lines, text, symbols, images), manages brightness and layers.</li>"
 "<li><b>Display unit:</b> receives the video signal (LVDS/Display port) and shows it.</li>"
 "<li><b>HMI:</b> the pilot reads and acts with buttons, knobs and touch; commands select pages, modes and brightness.</li>"
 "<li><b>Environment:</b> sunlight, temperature, vibration and humidity act on the whole system.</li></ol>",
 "<p>Điều quan trọng cần thấy là màn hình không tự biết cần vẽ gì. Nó chỉ nhận video đã vẽ sẵn từ bộ tạo đồ hoạ, còn bộ tạo đồ hoạ nhận con số từ bus. Đó là lý do Module 05 (bus dữ liệu) đứng ngay trước module này: một con số tốc độ đi từ ADIRU qua ARINC 429 đến DMC, DMC vẽ thành thước tốc độ rồi mới hiện trên PFD.</p><p>Khi một màn hình hiện sai hoặc trống, kỹ sư bảo trì phải biết lỗi nằm ở khâu nào trong năm khối này: nguồn dữ liệu, bus, bộ tạo đồ hoạ, hay chính màn hình.</p>",
 "<p>The key point is that a screen does not know by itself what to draw. It only receives video that the graphic generator has already drawn, and the graphic generator receives numbers from the bus. That is why Module 05 (data buses) comes right before this one: a speed value goes from the ADIRU over ARINC 429 to the DMC, the DMC draws it as a speed scale, and only then does it appear on the PFD.</p><p>When a screen shows wrong or blank data, the maintenance engineer must know in which of the five blocks the fault sits: data source, bus, graphic generator, or the screen itself.</p>",
 "disp_p03.jpg"),

("Tải nhận thức: vì sao nhiều thông tin hơn chưa chắc tốt hơn",
 "Cognitive load: why more information is not always better",
 "<p>Hệ thống càng phức tạp, tài nguyên nhận thức mà nó đòi hỏi ở phi công càng lớn. Nếu vượt quá khả năng tối đa của con người, hiệu năng HMI giảm (vùng \"overload\"). Mục tiêu thiết kế là giữ tải trong <b>vùng thoải mái</b> (comfort zone).</p>"
 "<p>Slide nêu bốn nguyên tắc của kỹ nghệ nhận thức: <b>Routinize</b> (quy trình chuẩn và tự động hoá việc lặp), <b>Anticipate</b> (dự đoán sự cố sớm), <b>Delegate</b> (giao việc cho tự động hoá hoặc đồng đội), <b>Schematize</b> (cấu trúc, ưu tiên và rút gọn thông tin).</p>",
 "<p>The more complex the system, the more cognitive resources it demands from the pilot. If this exceeds the human maximum, HMI performance drops (the \"overload\" region). The design aim is to keep the load inside the <b>comfort zone</b>.</p>"
 "<p>The slide lists four cognitive engineering principles: <b>Routinize</b> (standard procedures and automation for routine tasks), <b>Anticipate</b> (predict problems early), <b>Delegate</b> (assign tasks to automation or crew members), <b>Schematize</b> (structure, prioritise and simplify information).</p>",
 "<p>Hình đồ thị trong slide cho thấy hai đường: đường đỏ đứt là tài nguyên nhận thức hệ thống đòi hỏi (tăng theo độ phức tạp), đường xanh là hiệu năng HMI (giảm dần khi độ phức tạp tăng). Hai đường cắt nhau ở ngưỡng quá tải. Hai ảnh ví dụ ở dưới cho thấy cùng một trang với quá nhiều cảnh báo (stress, chậm quyết định, dễ sai) so với trang đã được sắp xếp và ưu tiên (dễ quản lý, quyết định nhanh).</p><p>Đây là lý do ECAM chỉ hiển thị cảnh báo theo thứ tự ưu tiên và có nút CLR/RCL để xoá và gọi lại thông báo (xem phần 4).</p>",
 "<p>The chart in the slide shows two curves: the dashed red line is the cognitive resource the system demands (rising with complexity), the blue line is HMI performance (falling as complexity rises). They cross at the overload threshold. The two example photos below show the same page with too many alerts (stress, slow decisions, error-prone) versus a page that has been organised and prioritised (manageable, fast decisions).</p><p>This is why ECAM shows alerts in priority order and has CLR/RCL keys to clear and recall messages (see part 4).</p>",
 "disp_p10.jpg"),

("Kiến trúc hệ thống hiển thị: monobloc, segregated, integrated modular",
 "Display system architecture: monobloc, segregated, integrated modular",
 "<table class='tt'><thead><tr><th>Thế hệ</th><th>Đặc điểm</th><th>Ví dụ</th></tr></thead><tbody>"
 "<tr><td>1. Monobloc (sớm)</td><td>Một hộp, phần cứng chuyên dụng, đồ hoạ 2D cố định, linh hoạt thấp</td><td>Buồng lái kính thế hệ đầu</td></tr>"
 "<tr><td>2. Segregated (nâng cao)</td><td>Mỗi chức năng một bộ xử lý riêng; màn hình theo chức năng (PFD, ND)</td><td>Họ A320</td></tr>"
 "<tr><td>3. Integrated modular (hiện đại)</td><td>Nền tảng tính toán chung chạy nhiều ứng dụng; đồ hoạ 2D/3D hiệu năng cao; định dạng màn hình cấu hình lại được</td><td>A350 và A320 mới nhất</td></tr></tbody></table>",
 "<table class='tt'><thead><tr><th>Generation</th><th>Features</th><th>Example</th></tr></thead><tbody>"
 "<tr><td>1. Monobloc (early)</td><td>Single box, dedicated hardware, fixed-function 2D graphics, low flexibility</td><td>First-generation glass cockpits</td></tr>"
 "<tr><td>2. Segregated (advanced)</td><td>Each function has its own processor; function-specific displays (PFD, ND)</td><td>A320 family</td></tr>"
 "<tr><td>3. Integrated modular (modern)</td><td>Common computing platform running several applications; high-performance 2D/3D graphics; reconfigurable display formats</td><td>A350 and latest A320</td></tr></tbody></table>",
 "<p>Hãy nghĩ như máy tính cá nhân. Monobloc giống một máy chơi game đời cũ chỉ chạy đúng một trò. Segregated giống nhiều thiết bị chuyên dụng đặt cạnh nhau, mỗi cái làm một việc. Integrated modular giống một máy tính chung chạy nhiều phần mềm, thêm tính năng bằng cách nâng cấp phần mềm thay vì thay phần cứng.</p><p>Lợi ích của tích hợp: nhẹ hơn, ít LRU hơn, dễ bảo trì và nâng cấp. Cái giá: phần mềm dùng chung phải được chứng nhận rất nghiêm (DO-178), vì một lỗi có thể ảnh hưởng nhiều chức năng cùng lúc.</p>",
 "<p>Think of personal computers. Monobloc is like an old game console that runs exactly one game. Segregated is like several dedicated devices side by side, each doing one job. Integrated modular is like a shared computer running many programs, where you add features by upgrading software instead of replacing hardware.</p><p>Benefits of integration: lighter, fewer LRUs, easier maintenance and upgrades. The price: the shared software must be certified very strictly (DO-178), because one defect could affect several functions at once.</p>",
 "disp_p12.jpg"),
],
# ------------------------------------------------------------------ PART 2
[
("Điểm ảnh, độ phân giải và kích thước ảnh",
 "Pixels, resolution and image size",
 "<p><b>Điểm ảnh (pixel)</b> là phần tử nhỏ nhất mang thông tin màu và độ sáng; thường gồm ba điểm con đỏ (R), lục (G), lam (B). <b>Kích thước ảnh</b> là chiều rộng nhân chiều cao tính bằng pixel.</p>"
 "<table class='tt'><thead><tr><th>Chuẩn</th><th>Kích thước</th><th>Số điểm ảnh</th></tr></thead><tbody>"
 "<tr><td>HD</td><td>1280 × 720</td><td>0,92 MP (slide ghi khoảng 0,9)</td></tr>"
 "<tr><td>Full HD</td><td>1920 × 1080</td><td>2,07 MP (khoảng 2,1)</td></tr>"
 "<tr><td>4K UHD</td><td>3840 × 2160</td><td>8,29 MP (khoảng 8,3)</td></tr></tbody></table>"
 "<p><b>Độ phân giải</b> là số pixel trên một inch (PPI) hoặc kích thước pixel tính bằng mm.</p>",
 "<p>A <b>pixel</b> is the smallest picture element carrying colour and brightness information; it usually has three sub-pixels, red (R), green (G) and blue (B). <b>Image size</b> is width times height in pixels.</p>"
 "<table class='tt'><thead><tr><th>Standard</th><th>Size</th><th>Pixel count</th></tr></thead><tbody>"
 "<tr><td>HD</td><td>1280 × 720</td><td>0.92 MP (slide says about 0.9)</td></tr>"
 "<tr><td>Full HD</td><td>1920 × 1080</td><td>2.07 MP (about 2.1)</td></tr>"
 "<tr><td>4K UHD</td><td>3840 × 2160</td><td>8.29 MP (about 8.3)</td></tr></tbody></table>"
 "<p><b>Resolution</b> is pixels per inch (PPI), or equivalently pixel size in mm.</p>",
 "<p>Ba con số megapixel trong bảng đã được kiểm lại bằng phép nhân: 1280×720 = 921 600; 1920×1080 = 2 073 600; 3840×2160 = 8 294 400 (khớp slide sau khi làm tròn).</p><p>Một điểm cần nhớ khi so sánh: 4K UHD có gấp đôi chiều rộng và gấp đôi chiều cao của Full HD nên gấp <b>bốn</b> lần số pixel (8,29 so với 2,07 MP), không phải gấp đôi.</p>",
 "<p>The three megapixel figures were re-checked by multiplication: 1280×720 = 921,600; 1920×1080 = 2,073,600; 3840×2160 = 8,294,400 (they match the slide after rounding).</p><p>A point to remember when comparing: 4K UHD has twice the width and twice the height of Full HD, so it has <b>four</b> times as many pixels (8.29 versus 2.07 MP), not twice.</p>",
 "disp_p05.jpg"),

("Thị lực 1 phút cung: khi nào mắt không còn thấy điểm ảnh",
 "Visual acuity of 1 arcminute: when the eye can no longer see pixels",
 "<p>Mắt người bình thường phân biệt được hai điểm cách nhau tối thiểu <b>1 phút cung</b> (1' = 1/60 độ = 2,91×10⁻⁴ rad). Với góc nhỏ, tan θ ≈ θ nên kích thước tối thiểu nhìn thấy ở khoảng cách D là <b>h ≈ D·θ</b>.</p>"
 "<table class='tt'><thead><tr><th>D</th><th>1 m</th><th>3 m</th><th>5 m</th><th>10 m</th><th>20 m</th></tr></thead><tbody>"
 "<tr><td>h</td><td>0,29 mm</td><td>0,87 mm</td><td>1,45 mm</td><td>2,91 mm</td><td>5,82 mm</td></tr></tbody></table>"
 "<p>Phổ nhạy của mắt có cực đại ở <b>555 nm</b> (ánh sáng lục); các mốc xanh lam 470 nm, lục 532 nm, đỏ 615 nm.</p>",
 "<p>A normal human eye can separate two points at least <b>1 arcminute</b> apart (1' = 1/60 degree = 2.91×10⁻⁴ rad). For small angles tan θ ≈ θ, so the smallest visible size at distance D is <b>h ≈ D·θ</b>.</p>"
 "<table class='tt'><thead><tr><th>D</th><th>1 m</th><th>3 m</th><th>5 m</th><th>10 m</th><th>20 m</th></tr></thead><tbody>"
 "<tr><td>h</td><td>0.29 mm</td><td>0.87 mm</td><td>1.45 mm</td><td>2.91 mm</td><td>5.82 mm</td></tr></tbody></table>"
 "<p>The eye's spectral sensitivity peaks at <b>555 nm</b> (green light); reference marks are blue 470 nm, green 532 nm, red 615 nm.</p>",
 "<p>Cách tự kiểm: đổi 1/60 độ ra radian: (π/180)/60 = 2,909×10⁻⁴. Ở D = 5 m, h = 5 × 2,909×10⁻⁴ = 1,45×10⁻³ m = 1,45 mm. Cách tính chính xác hơn 2·D·tan(θ/2) cho cùng kết quả đến chữ số thứ tư. Cả năm giá trị trong bảng đã được tính lại trong notebook.</p><p>Ý nghĩa thiết kế: nếu pixel của màn hình trong buồng lái nhỏ hơn h tại khoảng cách phi công ngồi (khoảng 0,6 đến 0,8 m), mắt sẽ không thấy từng pixel; đó là lý do độ phân giải cao quan trọng cho màn hình gần mắt. Đỉnh 555 nm cũng giải thích vì sao màu lục được dùng cho các giá trị bình thường: đó là màu mắt nhạy nhất.</p>",
 "<p>Self-check: convert 1/60 degree to radians: (π/180)/60 = 2.909×10⁻⁴. At D = 5 m, h = 5 × 2.909×10⁻⁴ = 1.45×10⁻³ m = 1.45 mm. The more exact 2·D·tan(θ/2) gives the same result to four digits. All five table values were recomputed in the notebook.</p><p>Design meaning: if a cockpit screen's pixels are smaller than h at the distance the pilot sits (about 0.6 to 0.8 m), the eye cannot see individual pixels, which is why high resolution matters for screens close to the eye. The 555 nm peak also explains why green is used for normal values: it is the colour the eye is most sensitive to.</p>",
 "disp_p06.jpg"),

("CRT: súng điện tử, lưới điều khiển và anode",
 "CRT: electron gun, control grid and anodes",
 "<p>Ống tia âm cực (CRT) gồm một <b>súng điện tử</b> (cathode kèm sợi nung, lưới, các anode hội tụ) bắn chùm electron vào lớp phosphor ở mặt sau màn hình.</p><ul>"
 "<li><b>Cathode</b> phủ tungsten thori; sợi nung làm nóng để electron \"bị đun ra\".</li>"
 "<li><b>Lưới (grid)</b> âm hơn cathode; điện áp lưới điều khiển số electron đi qua, tức độ sáng.</li>"
 "<li><b>Anode hội tụ</b> uốn và hội tụ chùm như thấu kính lồi.</li>"
 "<li><b>Anode cuối</b> (lớp than chì trong ống) có thế dương rất cao (vài kilôvôn, dòng một chiều) để gia tốc chùm.</li>"
 "<li>Va chạm với phosphor biến năng lượng electron thành ánh sáng.</li></ul>" + fig("tooley_fig11_3_crt.png", "Tooley Fig 11.3 CRT"),
 "<p>The cathode ray tube (CRT) has an <b>electron gun</b> (cathode with heater, grid, focus anodes) firing a beam of electrons at the phosphor coating on the back of the screen.</p><ul>"
 "<li>The <b>cathode</b> is coated with thoriated tungsten; the heater makes electrons \"boil off\".</li>"
 "<li>The <b>grid</b> is negative with respect to the cathode; the grid voltage controls how many electrons pass, i.e. brightness.</li>"
 "<li>The <b>focus anodes</b> bend and focus the beam like a biconvex lens.</li>"
 "<li>The <b>final anode</b> (graphite coating inside the tube) is held at a very high positive potential (several kilovolts, DC) to accelerate the beam.</li>"
 "<li>Impact on the phosphor converts electron energy into light.</li></ul>" + fig("tooley_fig11_3_crt.png", "Tooley Fig 11.3 CRT"),
 "<p>Ba câu hỏi trắc nghiệm của sách xoay quanh đúng phần này: lưới có điện thế <b>âm</b> so với cathode (câu 7), anode cuối có chức năng <b>gia tốc</b> chùm (câu 8) và cần nguồn <b>một chiều cao áp</b> (câu 12). Muốn nhớ, hãy hình dung lưới như một van nước: càng âm càng đẩy electron trở lại nên càng ít electron đến màn hình, tối hơn.</p><p>Nguồn: Tooley mục 11.1.1, trang 180, hình 11.3 (ảnh bên dưới cắt từ chính trang đó).</p>",
 "<p>Three of the book's multiple-choice questions revolve around exactly this: the grid is <b>negative</b> with respect to the cathode (Q7), the final anode <b>accelerates</b> the beam (Q8) and needs a <b>high-voltage DC</b> supply (Q12). To remember: picture the grid as a water valve; the more negative it is, the more it pushes electrons back, so fewer reach the screen and it is darker.</p><p>Source: Tooley section 11.1.1, page 180, Figure 11.3 (the image below is cropped from that page).</p>",
 None),

("Quét raster: răng cưa, số dòng và tần số",
 "Raster scan: sawtooth waveforms, line count and frequency",
 "<p>Để phủ kín màn hình, chùm electron quét từ trên xuống và từ trái sang phải, tạo một <b>raster</b>. Điện áp lên các bản X và Y có dạng <b>răng cưa</b> (ramp) với hai tần số khác nhau.</p>"
 "<table class='tt'><thead><tr><th>Ví dụ trong sách</th><th>Y (dọc)</th><th>X (ngang)</th><th>Một khung</th></tr></thead><tbody>"
 "<tr><td>Raster 4 dòng</td><td>50 Hz</td><td>200 Hz</td><td>20 ms</td></tr>"
 "<tr><td>400 dòng</td><td>100 Hz</td><td>40 kHz</td><td>10 ms</td></tr></tbody></table>"
 "<p>Quy tắc: <b>f_X = N_dòng × f_Y</b>, thời gian một khung T = 1/f_Y.</p>",
 "<p>To cover the whole screen the electron beam scans top to bottom and left to right, producing a <b>raster</b>. The voltages on the X and Y plates are <b>sawtooth</b> (ramp) waveforms at two different frequencies.</p>"
 "<table class='tt'><thead><tr><th>Book example</th><th>Y (vertical)</th><th>X (horizontal)</th><th>One frame</th></tr></thead><tbody>"
 "<tr><td>4-line raster</td><td>50 Hz</td><td>200 Hz</td><td>20 ms</td></tr>"
 "<tr><td>400 lines</td><td>100 Hz</td><td>40 kHz</td><td>10 ms</td></tr></tbody></table>"
 "<p>Rule: <b>f_X = N_lines × f_Y</b>, frame time T = 1/f_Y.</p>",
 "<p>Vì sao nhân? Trong một chu kỳ của tín hiệu quét dọc, chùm phải vẽ đủ N dòng ngang, nên tín hiệu quét ngang phải chạy N chu kỳ trong cùng khoảng thời gian: 4 dòng × 50 Hz = 200 Hz; 400 dòng × 100 Hz = 40 000 Hz. Cả hai ví dụ trong Tooley mục 11.1.3 (trang 182) đều khớp công thức này, đã tự kiểm chứng trong notebook.</p><p>Thêm ở mục 15.2.2 của Tooley: màn hình CRT trên EFIS quét raster ở 50 hoặc 60 Hz, còn ký hiệu và chữ được vẽ bằng <b>stroke scanning</b> chồng lên raster; CRT màu dùng làm lệch từ trường nên dạng sóng cuộn dây phải hình thang chứ không phải răng cưa thẳng, vì cuộn dây có điện trở.</p>",
 "<p>Why multiply? Within one period of the vertical scan the beam must draw N horizontal lines, so the horizontal scan runs N periods in the same time: 4 lines × 50 Hz = 200 Hz; 400 lines × 100 Hz = 40,000 Hz. Both Tooley examples in section 11.1.3 (page 182) fit this rule and were verified in the notebook.</p><p>Also from Tooley section 15.2.2: CRTs in the EFIS scan the raster at 50 or 60 Hz, while symbols and characters are drawn by <b>stroke scanning</b> superimposed on the raster; colour CRTs use magnetic deflection, so the coil waveform must be trapezoidal rather than a straight sawtooth, because the coil has resistance.</p>",
 None),

("CRT màu và bộ điều khiển CRT",
 "Colour CRT and the CRT controller",
 "<p>CRT màu có <b>ba cathode</b> (đỏ, lục, lam) và các phosphor ba màu xen kẽ. Mỗi chùm chỉ chạm vào phosphor cùng màu. Trộn: đỏ + lục = vàng, lục + lam = lục lam (cyan), đỏ + lam = đỏ tươi (magenta), cả ba = trắng.</p>"
 "<p>Phía điều khiển: một <b>bộ điều khiển CRT</b> phối hợp với giao diện video/đồng bộ, dưới sự điều khiển của CPU riêng. Bộ nhớ DMA đưa dữ liệu vào để CPU đỡ phải xử lý từng byte; hình dạng ký tự lưu trong <b>ROM tạo ký tự</b> (character generator ROM), mỗi ký tự là một ma trận ô (8×8 hoặc 9×14).</p>",
 "<p>A colour CRT has <b>three cathodes</b> (red, green, blue) and interleaved phosphors of three colours. Each beam hits only phosphors of its own colour. Mixing: red + green = yellow, green + blue = cyan, red + blue = magenta, all three = white.</p>"
 "<p>On the control side, a <b>CRT controller</b> works with a video/sync interface under a dedicated CPU. DMA feeds data in so the CPU does not process each byte; the character shapes live in a <b>character generator ROM</b>, each character being a cell matrix (8×8 or 9×14).</p>",
 "<p>Đây là chỗ điện tử số gặp màn hình. ROM tạo ký tự chính là bộ nhớ chỉ đọc của Module 04: địa chỉ là mã ký tự cộng số thứ tự dòng trong ô ký tự, dữ liệu là chuỗi bit của dòng đó, được dồn thành luồng nối tiếp đưa vào kênh video. Bật bit nào thì pixel đó sáng.</p><p>Câu trắc nghiệm 15 của sách (mẫu ký tự lưu ở đâu) có đáp án là ROM tạo ký tự; câu 10 hỏi ba chùm tia của CRT màu ứng với đỏ, lục, lam.</p>",
 "<p>This is where digital electronics meets the display. The character generator ROM is exactly the read-only memory of Module 04: the address is the character code plus the row number within the character cell, the data is the bit pattern of that row, serialised into the video channel. Each bit that is on lights its pixel.</p><p>The book's multiple-choice question 15 (where are the character patterns stored) has the character generator ROM as the answer; question 10 asks which colours the three beams of a colour CRT correspond to: red, green, blue.</p>",
 None),

("LED và hiển thị 7 đoạn",
 "LEDs and the 7-segment display",
 "<p>LED hoạt động ở dòng thuận khoảng <b>5 đến 20 mA</b>, áp thuận khoảng 2 V, tin cậy hơn đèn sợi đốt rất nhiều. LED đỏ phổ biến nhất (cực đại khoảng 635 đến 650 nm); góc nhìn LED tròn khoảng 20 đến 40 độ.</p>"
 "<p><b>Hiển thị 7 đoạn</b> dùng bảy LED a đến g. Hiển thị chữ số \"1\": sáng đoạn b và c; chữ số \"2\": sáng a, b, g, e, d. Vì mỗi đoạn là một LED riêng nên cần <b>bộ giải mã</b> chuyển BCD sang bảy đường điều khiển.</p>" + fig("tooley_fig11_14_seg.png", "Tooley Fig 11.14 seven-segment"),
 "<p>An LED works at a forward current of about <b>5 to 20 mA</b> and about 2 V forward drop, and is far more reliable than a filament lamp. Red LEDs are the most common (peak about 635 to 650 nm); a round LED's viewing angle is about 20 to 40 degrees.</p>"
 "<p>A <b>7-segment display</b> uses seven LEDs a to g. Digit \"1\" lights segments b and c; digit \"2\" lights a, b, g, e, d. Since each segment is its own LED, a <b>decoder</b> is needed to turn BCD into seven drive lines.</p>" + fig("tooley_fig11_14_seg.png", "Tooley Fig 11.14 seven-segment"),
 "<p>Ba câu trắc nghiệm của sách nằm ở đây. Câu 1: LED đỏ có cực đại khoảng 635 nm (bảng 11.1). Câu 5: các đoạn a, b, c, d, g sáng hiển thị số <b>3</b> (số 2 cần e thay cho c, số 5 cần f thay cho b). Câu 6: mã BCD 1001 hiển thị số <b>9</b>. Notebook của module tự kiểm cả ba.</p><p>Ví dụ tự tính điện trở hạn dòng: nguồn 5 V, LED chuẩn 5 mm dòng 10 mA, áp thuận 2,0 V (bảng 11.1 của Tooley): R = (5 − 2,0)/0,010 = 300 Ω. Đây là phép tính ví dụ của module, không phải bài của sách.</p>",
 "<p>Three of the book's multiple-choice questions sit here. Q1: a red LED peaks near 635 nm (Table 11.1). Q5: segments a, b, c, d, g displays the digit <b>3</b> (a 2 needs e instead of c, a 5 needs f instead of b). Q6: BCD 1001 displays the digit <b>9</b>. The module notebook checks all three.</p><p>A self-computed current-limiting resistor example: 5 V supply, standard 5 mm LED at 10 mA with 2.0 V forward drop (Tooley Table 11.1): R = (5 − 2.0)/0.010 = 300 Ω. This is the module's own worked example, not a book exercise.</p>",
 None),

("Giải mã BCD sang 7 đoạn và hiển thị chữ cái (Floyd)",
 "BCD to 7-segment decoding and letter display (Floyd)",
 "<p>Trong chương 4, mục Applied Logic (trang 244 đến 249), Floyd thiết kế bộ giải mã thập lục phân sang 7 đoạn cho các chữ <b>A, b, C, d, E</b> (F tắt hết). Hiển thị anode chung nên đoạn <b>sáng khi ngõ ra THẤP</b>; mã 0 đến 9 là ô \"không quan tâm\" (X) trên bản đồ Karnaugh.</p>"
 "<table class='tt'><thead><tr><th>Chữ</th><th>Mã H3H2H1H0</th><th>Đoạn sáng (Bảng 4-14)</th></tr></thead><tbody>"
 "<tr><td>A</td><td>1010</td><td>a, b, c, e, f, g</td></tr><tr><td>b</td><td>1011</td><td>c, d, e, f, g</td></tr>"
 "<tr><td>C</td><td>1100</td><td>a, d, e, f</td></tr><tr><td>d</td><td>1101</td><td>b, c, d, e, g</td></tr>"
 "<tr><td>E</td><td>1110</td><td>a, d, e, f, g</td></tr></tbody></table>",
 "<p>In chapter 4, the Applied Logic section (pages 244 to 249), Floyd designs a hexadecimal to 7-segment decoder for the letters <b>A, b, C, d, E</b> (F is all off). The display is common-anode, so a segment <b>lights when its output is LOW</b>; codes 0 to 9 are \"don't care\" (X) cells on the Karnaugh map.</p>"
 "<table class='tt'><thead><tr><th>Letter</th><th>Code H3H2H1H0</th><th>Segments on (Table 4-14)</th></tr></thead><tbody>"
 "<tr><td>A</td><td>1010</td><td>a, b, c, e, f, g</td></tr><tr><td>b</td><td>1011</td><td>c, d, e, f, g</td></tr>"
 "<tr><td>C</td><td>1100</td><td>a, d, e, f</td></tr><tr><td>d</td><td>1101</td><td>b, c, d, e, g</td></tr>"
 "<tr><td>E</td><td>1110</td><td>a, d, e, f, g</td></tr></tbody></table>",
 "<p>Kết quả rút gọn (đã tự kiểm chứng bằng sympy trong notebook): a = H0; e = H2H1H0 (một cổng AND 3 ngõ vào); f = H2H0 (một AND 2 ngõ vào). Phép rút gọn gọn đến mức đoạn a chỉ cần nối thẳng ngõ vào H0, không cần cổng nào.</p><p>Các chữ viết thường b và d được dùng vì chữ B in hoa giống số 8 và chữ D in hoa giống số 0. Một bộ \"phát hiện mã không hợp lệ\" H3(H1 + H2) chỉ cho hiển thị sáng khi mã nằm trong 1010 đến 1111 (xem bài tập 63 và 69 bên dưới). LED thấy được trong bóng tối còn LCD thì không, vì LCD không tự phát sáng.</p>",
 "<p>Simplified results (verified with sympy in the notebook): a = H0; e = H2H1H0 (one 3-input AND gate); f = H2H0 (one 2-input AND). The simplification is so strong that segment a just wires through the H0 input, with no gate at all.</p><p>Lowercase b and d are used because a capital B looks like an 8 and a capital D looks like a 0. An \"invalid code detector\" H3(H1 + H2) enables the display only for codes 1010 to 1111 (see Problems 63 and 69 below). An LED can be seen in the dark but an LCD cannot, since an LCD does not emit light.</p>",
 None),

("74HC47, zero suppression và ghép kênh chữ số (Floyd ch.6)",
 "74HC47, zero suppression and digit multiplexing (Floyd ch.6)",
 "<p><b>74HC47</b> (Floyd mục 6-5, trang 338 đến 340) giải mã BCD và có thể lái trực tiếp hiển thị 7 đoạn anode chung. Mọi ngõ ra a đến g và các chân LT, RBI, BI/RBO đều tích cực mức <b>THẤP</b>.</p><ul>"
 "<li><b>LT = 0</b> (và BI/RBO = 1): bật cả bảy đoạn, dùng thử đèn.</li>"
 "<li><b>RBI = 0</b> và mã 0000: ngắt hết đoạn, ra RBO = 0 để xoá số 0 thừa (leading zero suppression: 030.080 hiển thị 30.08).</li>"
 "<li>Ghép kênh (Hình 6-49, trang 353): 74HC157 chọn giữa hai mã BCD, 74HC47 giải mã, 74HC139 bật lần lượt từng chữ số; tần số đủ cao thì mắt không thấy nhấp nháy.</li></ul>",
 "<p>The <b>74HC47</b> (Floyd section 6-5, pages 338 to 340) decodes BCD and can drive a common-anode 7-segment display directly. All outputs a to g and the LT, RBI, BI/RBO pins are active <b>LOW</b>.</p><ul>"
 "<li><b>LT = 0</b> (with BI/RBO = 1): turns on all seven segments, a lamp test.</li>"
 "<li><b>RBI = 0</b> with code 0000: turns every segment off and drives RBO = 0, to blank unnecessary zeros (leading zero suppression: 030.080 shows as 30.08).</li>"
 "<li>Multiplexing (Figure 6-49, page 353): the 74HC157 selects between two BCD codes, the 74HC47 decodes, the 74HC139 enables each digit in turn; if the rate is high enough the eye sees no flicker.</li></ul>",
 "<p>Ba câu hỏi Section Checkup của Floyd (đáp án in ở trang 384): bộ giải mã dùng cho hiển thị catốt chung phải có ngõ ra <b>tích cực mức CAO</b> (nên 74HC47 hợp với anode chung chứ không phải catốt chung); 74HC157 đa hợp hai mã BCD; 74HC139 bật hai hiển thị luân phiên.</p><p>Floyd Bài 38 (xử lý sự cố hệ ghép kênh 7 đoạn) và Bài 44 (thêm hai chữ số) là bài chẵn nên sách không in đáp án; module này vì vậy không đưa lời giải của chúng. Điều sách xác nhận là: tần số chọn phải đủ cao để mắt không thấy nhấp nháy.</p>",
 "<p>Three Floyd Section Checkup questions (printed answers on page 384): a decoder used with a common-cathode display must have <b>active-HIGH</b> outputs (so the 74HC47 suits common-anode, not common-cathode); the 74HC157 multiplexes two BCD codes; the 74HC139 enables the two displays alternately.</p><p>Floyd Problem 38 (troubleshooting the 7-segment multiplexing system) and Problem 44 (adding two digits) are even-numbered, so the book prints no answers; this module therefore gives no solution for them. What the book does confirm: the select frequency must be high enough that the eye sees no flicker.</p>",
 None),

("LCD: công tắc ánh sáng điện tử",
 "LCD: an electronic light switch",
 "<p>Tinh thể lỏng nằm giữa trạng thái rắn và lỏng; hướng các phân tử (và đường đi của ánh sáng) được điều khiển bằng điện trường. LCD <b>không tự phát sáng</b>, nên cần đèn nền hoặc ánh sáng phản xạ.</p><ul>"
 "<li>Cấu trúc: đèn nền, kính phân cực sau, kính TFT có điện cực, tinh thể lỏng, kính lọc màu RGB, kính phân cực trước.</li>"
 "<li>Pixel TẮT: phân tử xoay làm ánh sáng bị chặn (tối). Pixel BẬT: ánh sáng đi qua (sáng).</li>"
 "<li>Độ sáng theo điện áp (slide: 0 V đen đến 5 V trắng); màu tạo từ ba điểm con R, G, B.</li>"
 "<li><b>TFT</b> hoạt động như công tắc: đường gate chọn hàng, đường data mang điện áp, tụ giữ điện tích tới lần làm tươi sau.</li></ul>",
 "<p>Liquid crystals sit between solid and liquid; their molecular orientation (and thus the path of light) is controlled by an electric field. An LCD <b>emits no light itself</b>, so it needs a backlight or reflected light.</p><ul>"
 "<li>Structure: backlight, rear polariser, TFT glass with electrodes, liquid crystal, RGB colour-filter glass, front polariser.</li>"
 "<li>Pixel OFF: molecules rotate so light is blocked (dark). Pixel ON: light passes (bright).</li>"
 "<li>Brightness follows the voltage (slide: 0 V black to 5 V white); colour comes from three sub-pixels R, G, B.</li>"
 "<li>A <b>TFT</b> acts as a switch: the gate line selects the row, the data line carries the voltage, a capacitor holds the charge until the next refresh.</li></ul>",
 "<p>Slide còn nêu ba kiểu căn chỉnh tinh thể: <b>TN</b> (đơn giản, rẻ, đáp ứng nhanh nhưng góc nhìn hẹp; dùng trong màn hình máy bay đời đầu), <b>IPS</b> (phân tử xoay trong mặt phẳng, góc nhìn rộng, màu đẹp; dẫn đầu ở màn hình máy bay hiện đại), <b>MVA</b> (đa vùng dọc, tương phản cao, màu đen sâu; dùng cho buồng lái cao cấp).</p><p>Hình bên là một slide infographic dày thông tin, bấm vào ảnh để phóng to.</p>",
 "<p>The slide also lists three crystal alignment technologies: <b>TN</b> (simple, cheap, fast response but a narrow viewing angle; used in early aircraft displays), <b>IPS</b> (molecules rotate in the plane, wide viewing angle, good colour; the leader in modern aircraft displays), <b>MVA</b> (multi-domain vertical, high contrast, deep blacks; used in high-end cockpits).</p><p>The figure is a dense infographic slide; click it to enlarge.</p>",
 "disp_p04.jpg"),

("LCD phản xạ và có đèn nền, ma trận thụ động và chủ động, so với CRT",
 "Reflective and backlit LCDs, passive and active matrix, versus CRT",
 "<p>Theo Tooley (mục 11.3): LCD <b>phản xạ</b> dùng ánh sáng tới và gương; LCD <b>có đèn nền</b> dùng nguồn sáng riêng. <b>Ma trận thụ động</b> địa chỉ hàng và cột như ma trận nhớ, đáp ứng chậm và kém nét hơn. <b>Ma trận chủ động (AMLCD)</b> thêm một transistor màng mỏng (TFT) cho từng ô; mỗi kênh R, G, B có 256 mức, tổng cộng 256³ = hơn 16 triệu màu.</p>"
 "<p><b>So với CRT:</b> AMLCD thắng ở khối lượng, công suất, thể tích và độ tin cậy; đồng đều về độ sáng, độ phân giải, tiêu cự trên toàn màn hình; không bị \"rửa trôi\" dưới ánh sáng mạnh; chịu rung và sốc tốt. CRT vẫn có góc nhìn rộng hơn và dải nhiệt độ rộng hơn.</p>" + fig("tooley_fig11_19_lcd.png", "Tooley Fig 11.19 LCD"),
 "<p>Per Tooley (section 11.3): a <b>reflective</b> LCD uses incident light and a mirror; a <b>backlit</b> LCD uses its own light source. A <b>passive matrix</b> addresses rows and columns like a memory matrix, with a slow response and lower sharpness. An <b>active matrix (AMLCD)</b> adds a thin-film transistor (TFT) per cell; each R, G, B channel has 256 levels, giving 256³ = more than 16 million colours.</p>"
 "<p><b>Versus CRT:</b> the AMLCD wins on weight, power, volume and reliability; has uniform brightness, resolution and focus across the screen; does not wash out in strong light; tolerates vibration and shock. The CRT still has a wider viewing angle and a wider temperature range.</p>" + fig("tooley_fig11_19_lcd.png", "Tooley Fig 11.19 LCD"),
 "<p>Hai đáp án cần nhớ cho phần trắc nghiệm: câu 11, AMLCD có <b>thể tích nhỏ hơn và độ tin cậy cao hơn</b> CRT; câu 16, so với ma trận thụ động, AMLCD <b>nhanh hơn và nét hơn</b>. Câu key point của sách: CRT có góc nhìn rộng hơn và dải nhiệt độ rộng hơn, nhưng AMLCD hơn ở khả năng hiển thị phức tạp và dễ cấu hình.</p>",
 "<p>Two answers to remember for the quiz: Q11, the AMLCD has <b>smaller volume and greater reliability</b> than a CRT; Q16, compared with a passive matrix the AMLCD is <b>faster and sharper</b>. The book's key point: the CRT has a wider viewing angle and temperature range, but the AMLCD is superior in showing complex, highly configurable displays.</p>",
 None),
],
# ------------------------------------------------------------------ PART 3
[
("Đồng hồ bay cơ bản, bố trí chữ T và EADI/EHSI (Tooley ch.1)",
 "Basic flight instruments, the T layout and EADI/EHSI (Tooley ch.1)",
 "<p>Sáu đại lượng cơ bản: hướng bay, độ cao, tốc độ, tốc độ quay, tốc độ lên xuống, tư thế. Nhóm <b>đồng hồ số liệu khí (air data)</b> chạy bằng ống pitot-tĩnh: tốc độ (ASI), độ cao và tốc độ lên xuống (VSI). Áp tĩnh đi tới cả ba; áp ram chỉ tới ASI.</p>"
 "<p><b>Bố trí chữ T:</b> ASI bên trái, ADI (chân trời giả) ở giữa trên, độ cao bên phải, HSI ở dưới ADI. EFIS gom lại thành <b>EADI</b> (tư thế, thanh chỉ lệnh, kim glide slope, chỉ báo localiser, chỉ báo trượt) và <b>EHSI</b> (hướng, VOR, DME, ILS, gió).</p>",
 "<p>Six basic quantities: heading, altitude, airspeed, rate of turn, rate of climb, attitude. The <b>air data instruments</b> run from the pitot-static system: airspeed (ASI), altimeter and vertical speed (VSI). Static pressure goes to all three; ram pressure only to the ASI.</p>"
 "<p><b>The T layout:</b> ASI on the left, ADI (artificial horizon) top centre, altimeter on the right, HSI below the ADI. EFIS gathers them into the <b>EADI</b> (attitude, command bars, glide slope pointer, localiser indicator, slip indicator) and the <b>EHSI</b> (heading, VOR, DME, ILS, wind).</p>",
 "<p>Đây là phần nền của 27 câu trắc nghiệm chương 1. Ví dụ: kim glide slope và \"đường băng nổi lên\" (rising runway) nằm trên <b>EADI</b>; chỉ báo trượt cũng ở EADI; hướng, VOR và track hiển thị ở <b>EHSI</b>; thông số động cơ như tốc độ tuabin hiển thị ở <b>ECAM</b>. Hệ thống chỉ huy bay (flight director) nhận dữ liệu từ cả con quay tư thế lẫn VOR/localiser.</p><p>Nguồn: Tooley mục 1.1 và 1.2 (trang 1 đến 19); bố trí chữ T ở hình 1.23.</p>",
 "<p>This is the groundwork for the 27 chapter 1 quiz questions. For example: the glide slope pointer and the \"rising runway\" are on the <b>EADI</b>; the slip indicator is also on the EADI; heading, VOR and track appear on the <b>EHSI</b>; engine parameters such as turbine speed appear on the <b>ECAM</b>. The flight director system takes data from both the attitude gyro and the VOR/localiser.</p><p>Source: Tooley sections 1.1 and 1.2 (pages 1 to 19); the T layout is in Figure 1.23.</p>",
 None),

("EFI và EFIS: màn hình thay đồng hồ cơ",
 "EFI and EFIS: screens replacing mechanical dials",
 "<p><b>EFI</b> (Electronic Flight Indicator) là thiết bị bay hiển thị tham số bay bằng màn hình LCD, thay chỉ báo tư thế, tốc độ, độ cao cơ điện. Kích thước chuẩn 3 ATI hoặc 4 ATI (cùng cỡ đồng hồ cơ), dùng nhiều trên máy bay huấn luyện và quân sự.</p>"
 "<p>Cấu trúc: dữ liệu cảm biến (ADIRU, dữ liệu khí, FMS/GPS) qua ARINC 429 → bộ xử lý điện tử (nhận dữ liệu, tính tham số bay, tạo đồ hoạ, điều khiển LCD) → màn hình LCD (đèn nền LED, panel, kính phân cực, kính bezel) → thông tin bay.</p>",
 "<p>An <b>EFI</b> (Electronic Flight Indicator) is a flight instrument that shows flight parameters on an LCD screen, replacing electromechanical attitude, speed and altitude indicators. Standard sizes are 3 ATI or 4 ATI (the same case size as mechanical dials); it is widely used on training and military aircraft.</p>"
 "<p>Structure: sensor data (ADIRU, air data, FMS/GPS) over ARINC 429 → electronic processing unit (receives data, computes flight parameters, generates graphics, drives the LCD) → LCD screen (LED backlight, panel, polariser, glass bezel) → flight information.</p>",
 "<p>EFI là phiên bản nhỏ của ý tưởng EFIS: cùng chuỗi cảm biến, bộ xử lý, bus, màn hình, chỉ khác là thu gọn trong một hộp thay vì nhiều LRU trên máy bay thương mại. Đây là ví dụ \"single-box concept\" mà Tooley nhắc ở đầu chương 11: màn hình và điện tử nằm chung một vỏ giúp giảm cáp và đơn giản hoá bảo trì.</p>",
 "<p>The EFI is the small version of the EFIS idea: the same chain of sensor, processor, bus and display, just packed into one box instead of several LRUs as on an airliner. It is an example of the \"single-box concept\" Tooley mentions at the start of chapter 11: the display and its electronics in one enclosure cut cabling and simplify maintenance.</p>",
 "disp_p13.jpg"),

("EIS = EFIS + ECAM trong buồng lái A320",
 "EIS = EFIS + ECAM in the A320 cockpit",
 "<p><b>EIS</b> (Electronic Instrument System) gồm hai phần: <b>EFIS</b> (Electronic Flight Instrument System) gồm PFD và ND ở mỗi bên (cơ trưởng và phó cơ trưởng), và <b>ECAM</b> (Electronic Centralised Aircraft Monitoring) hai màn hình ở giữa (E/WD trên, SD dưới).</p>"
 "<table class='tt'><thead><tr><th></th><th>EFIS</th><th>ECAM</th></tr></thead><tbody>"
 "<tr><td>Màn hình</td><td>PFD, ND</td><td>E/WD (động cơ, cảnh báo), SD (trang hệ thống)</td></tr>"
 "<tr><td>Dữ liệu</td><td>Khí động, dẫn đường, điều khiển bay</td><td>Động cơ, trạng thái hệ thống, cảnh báo</td></tr></tbody></table>",
 "<p>The <b>EIS</b> (Electronic Instrument System) has two parts: the <b>EFIS</b> (Electronic Flight Instrument System), a PFD and an ND on each side (captain and first officer), and the <b>ECAM</b> (Electronic Centralised Aircraft Monitoring), two screens in the middle (E/WD upper, SD lower).</p>"
 "<table class='tt'><thead><tr><th></th><th>EFIS</th><th>ECAM</th></tr></thead><tbody>"
 "<tr><td>Screens</td><td>PFD, ND</td><td>E/WD (engines, warnings), SD (system pages)</td></tr>"
 "<tr><td>Data</td><td>Air data, navigation, flight control</td><td>Engines, system status, warnings</td></tr></tbody></table>",
 "<p>Cách nhớ gọn: <b>EFIS lo việc \"máy bay đang bay thế nào và đi đâu\"</b>, <b>ECAM lo việc \"máy bay đang khoẻ ra sao\"</b>. Cả hai chia sẻ dữ liệu từ máy tính hệ thống (ADIRU, FMGC, OMS) và được trình bày theo cách tích hợp để phi công nhận ra tình huống nhanh. Câu trắc nghiệm 9 (chương 1) và 2 (chương 15): thông số động cơ hiển thị trên ECAM, không phải EHSI hay EADI.</p>",
 "<p>A short way to remember: <b>EFIS handles \"how is the aircraft flying and where is it going\"</b>, <b>ECAM handles \"how healthy is the aircraft\"</b>. Both share data from the system computers (ADIRU, FMGC, OMS) and present it in an integrated way so pilots grasp the situation quickly. Quiz question 9 (chapter 1) and 2 (chapter 15): engine parameters appear on the ECAM, not on the EHSI or EADI.</p>",
 "disp_p14.jpg"),

("Các thế hệ EIS của Airbus: CRT rồi LCD",
 "Airbus EIS generations: CRT, then LCD",
 "<table class='tt'><thead><tr><th>Thế hệ</th><th>Máy bay</th><th>Màn hình</th><th>Bộ tạo hình</th></tr></thead><tbody>"
 "<tr><td>EIS đầu tiên</td><td>A310, A300-600</td><td>CRT màu 5\"×5\"</td><td>VDU</td></tr>"
 "<tr><td>EIS 1</td><td>A318 đến A321, A330, A340</td><td>CRT màu 6\"×6\"</td><td>DMC hoặc DIEHL</td></tr>"
 "<tr><td>EIS 2</td><td>Airbus</td><td>LCDU 725 (LCD)</td><td>DMC (Diehl)</td></tr>"
 "<tr><td>Evolution F3</td><td>Airbus</td><td>EDU 725 (CRT 6\"×6\")</td><td>VCGP trong EDU</td></tr></tbody></table>"
 "<p>LCDU 725 gồm tám mô-đun: vỏ, kết nối, nguồn (115 V AC sang DC), tiền xử lý, bộ xử lý đồ hoạ, xử lý video (tuỳ chọn), cụm LCD, đèn nền.</p>" + fig("disp_p16.jpg", "LCDU 725 modules"),
 "<table class='tt'><thead><tr><th>Generation</th><th>Aircraft</th><th>Screen</th><th>Image generator</th></tr></thead><tbody>"
 "<tr><td>First EIS</td><td>A310, A300-600</td><td>5\"×5\" colour CRT</td><td>VDU</td></tr>"
 "<tr><td>EIS 1</td><td>A318 to A321, A330, A340</td><td>6\"×6\" colour CRT</td><td>DMC or DIEHL</td></tr>"
 "<tr><td>EIS 2</td><td>Airbus</td><td>LCDU 725 (LCD)</td><td>DMC (Diehl)</td></tr>"
 "<tr><td>Evolution F3</td><td>Airbus</td><td>EDU 725 (6\"×6\" CRT)</td><td>VCGP inside the EDU</td></tr></tbody></table>"
 "<p>The LCDU 725 has eight modules: housing, interconnection, power supply (115 V AC to DC), pre-processing, graphic processor, video processor (optional), LCD assembly, backlight.</p>" + fig("disp_p16.jpg", "LCDU 725 modules"),
 "<p>Evolution F3 không phải màn hình mới: mục tiêu là giảm chi phí và khối lượng, giảm số LRU, tái dùng khối có sẵn, giữ tương thích với EIS 2. Tên mới là <b>EDU</b> (Enhanced Display Unit) và <b>EEIS</b> (Enhanced Electronic Instrument System). Bên trong EDU 725: ICB (bảng điều khiển giao diện), VCGP (bộ xử lý đồ hoạ video), DMB (bảng mô-đun màn hình), BLU (đèn nền), PSB (bảng nguồn).</p><p>Chuỗi tín hiệu tổng quát không đổi: hệ thống máy bay → bus ARINC 429/AFDX → DMC → màn hình.</p>",
 "<p>Evolution F3 is not a new screen type: its aim is lower cost and weight, fewer LRUs, reuse of existing blocks and compatibility with EIS 2. The new names are <b>EDU</b> (Enhanced Display Unit) and <b>EEIS</b> (Enhanced Electronic Instrument System). Inside the EDU 725: ICB (interface control board), VCGP (video graphic processor), DMB (display module board), BLU (backlight unit), PSB (power supply board).</p><p>The overall signal chain stays the same: aircraft systems → ARINC 429/AFDX bus → DMC → display.</p>",
 "disp_p15.jpg"),

("Hệ thống EIS A320: DMC, FWC và SDAC",
 "The A320 EIS: DMC, FWC and SDAC",
 "<ul><li><b>DMC 1, 2, 3</b> (Display Management Computer): thu dữ liệu từ hệ thống máy bay và tạo thông tin cho PFD, ND và ECAM. DMC 3 là dự phòng cho DMC 1 hoặc 2.</li>"
 "<li><b>FWC 1, 2</b> (Flight Warning Computer): tạo cảnh báo và thông báo thận trọng, gửi tới EIS và đèn Master Warning/Caution.</li>"
 "<li><b>SDAC 1, 2</b> (System Data Acquisition Concentrator): thu thập dữ liệu hệ thống rồi chuyển cho DMC qua ARINC 429.</li>"
 "<li><b>Hộp điều khiển ECAM</b>: chọn trang; <b>bảng điều khiển EFIS</b> ở hai bên: chế độ, tầm, độ sáng.</li></ul>"
 "<p>Các LRU này đều có BITE (tự kiểm tra) và trao đổi qua hai bus ARINC 429 dự phòng.</p>",
 "<ul><li><b>DMC 1, 2, 3</b> (Display Management Computer): collect data from aircraft systems and generate the information for the PFD, ND and ECAM. DMC 3 backs up DMC 1 or 2.</li>"
 "<li><b>FWC 1, 2</b> (Flight Warning Computer): generate warnings and cautions, sending them to the EIS and the Master Warning/Caution lights.</li>"
 "<li><b>SDAC 1, 2</b> (System Data Acquisition Concentrator): gather system data and pass it to the DMCs over ARINC 429.</li>"
 "<li><b>ECAM control box</b>: page selection; the <b>EFIS control panels</b> on each side: mode, range, brightness.</li></ul>"
 "<p>All these LRUs have BITE (self-test) and exchange data over two redundant ARINC 429 buses.</p>",
 "<p>Đây là sơ đồ nối lại toàn bộ phần 3 và 4. Chú ý tính dự phòng: ba DMC cho năm màn hình, hai FWC, hai SDAC, hai bus ARINC 429. Nếu một DMC hỏng, DMC 3 thay thế, và các màn hình có thể chuyển đổi nội dung cho nhau, đúng như nguyên tắc \"không đưa thông tin sai\" ở slide yêu cầu hệ thống.</p><p>Lưu ý nhỏ: slide ACARS (phần 5) ghi SDAC là \"System Data Analog Computer\"; đó là cách viết khác với slide này (và với chức năng \"thu thập\"), xem khung cảnh báo của module.</p>",
 "<p>This diagram ties parts 3 and 4 together. Note the redundancy: three DMCs for five screens, two FWCs, two SDACs, two ARINC 429 buses. If one DMC fails, DMC 3 takes over, and the screens can swap content among themselves, in line with the \"no misleading information\" principle on the requirements slide.</p><p>A small note: the ACARS slide (part 5) expands SDAC as \"System Data Analog Computer\"; that differs from this slide (and from the \"acquisition\" function), see the module's warning box.</p>",
 "disp_p18.jpg"),

("Bộ tạo ký hiệu và dự phòng trong EFIS (Tooley 15.2)",
 "Symbol generators and redundancy in the EFIS (Tooley 15.2)",
 "<p>EFIS có <b>ba bộ tạo ký hiệu</b> (symbol generator), là ba máy tính vi xử lý nhận dữ liệu VOR, DME, IRS... rồi tạo tín hiệu vẽ ký hiệu: bộ <b>trái</b> nuôi EADI và EHSI của cơ trưởng, bộ <b>phải</b> nuôi của phó cơ trưởng, bộ <b>giữa</b> là dự phòng thay một trong hai bộ kia khi hỏng. Cảm biến ánh sáng gắn trên từng màn hình tự chỉnh độ sáng; bảng điều khiển cho phép chỉnh tay.</p>"
 "<p>Màu ký hiệu: <b>trắng</b> trạng thái, <b>vàng</b> thận trọng, <b>đỏ</b> cảnh báo. Đầu ra bộ trái và giữa còn đi tới DFDAU rồi đầu ghi dữ liệu bay (DFDR).</p>",
 "<p>The EFIS has <b>three symbol generators</b>, microprocessor computers that take VOR, DME, IRS... data and generate the symbol drawing signals: the <b>left</b> one feeds the captain's EADI and EHSI, the <b>right</b> one the first officer's, and the <b>centre</b> one is a backup that can replace either of the others on failure. Light sensors on each display adjust brightness automatically; a control panel allows manual adjustment.</p>"
 "<p>Symbol colours: <b>white</b> status, <b>yellow</b> caution, <b>red</b> warning. The left and centre generator outputs also go to the DFDAU and then the flight data recorder (DFDR).</p>",
 "<p>Ba câu trắc nghiệm chương 15 nằm ở đây. Câu 5: hai màn hình trái và phải <b>chỉ</b> dùng chung một bộ tạo ký hiệu khi các bộ còn lại đều hỏng. Câu 7: nếu MỌI màn hình đều mất thông tin của cùng một nguồn thì nguyên nhân hợp lý nhất nằm ở cái chung cho tất cả (cảm biến, bus vào hay bộ điều khiển hiển thị), không phải một bộ tạo ký hiệu riêng lẻ. Câu 11: bộ thứ ba để dự phòng. Câu 10: dạng sóng quét của CRT điện từ là hình thang (xem slide quét raster).</p>",
 "<p>Three chapter 15 quiz questions sit here. Q5: the left and right displays share one symbol generator <b>only</b> when all the others have failed. Q7: if ALL displays lose information from one particular source, the most likely cause is whatever is common to all (the sensor, the input bus or the display controller), not one individual symbol generator. Q11: the third one is a standby. Q10: the electromagnetic CRT sweep waveform is trapezoidal (see the raster slide).</p>",
 None),

("PFD của A320: đọc một màn hình bay",
 "The A320 PFD: reading a flight display",
 "<ul><li><b>Cửa sổ thông báo chế độ</b> (trên cùng): chế độ đang bật (xanh lá) và đã chuẩn bị (trắng), ví dụ MACH, ALT, NAV.</li>"
 "<li><b>Thước tốc độ</b> (trái): ô xanh lá là tốc độ hiện tại, con trỏ vàng là tốc độ chọn.</li>"
 "<li><b>Chỉ báo tư thế</b> (giữa): trời xanh phía trên, đất nâu phía dưới; góc nghiêng và chúc ngóc.</li>"
 "<li><b>Thước độ cao</b> (phải) và <b>tốc độ lên xuống</b> (thang chừng ±6000 ft/min).</li>"
 "<li><b>Thang hướng</b> (dưới): hướng hiện tại, ±30° quanh đó.</li></ul>",
 "<ul><li><b>Mode annunciator window</b> (top): engaged modes (green) and armed modes (white), for example MACH, ALT, NAV.</li>"
 "<li><b>Speed scale</b> (left): the green box is the current speed, the yellow bug the selected speed.</li>"
 "<li><b>Attitude indicator</b> (centre): blue sky above, brown ground below; roll and pitch.</li>"
 "<li><b>Altitude scale</b> (right) and <b>vertical speed</b> (scale about ±6000 ft/min).</li>"
 "<li><b>Heading scale</b> (bottom): current heading, ±30° around it.</li></ul>",
 "<p>Cách học PFD nhanh nhất là nhớ theo bố cục chữ T của đồng hồ cơ: tốc độ trái, tư thế giữa, độ cao phải, hướng dưới. EFIS giữ nguyên vị trí để phi công đổi loại máy bay không phải học lại (Tooley mục 1.2 nhấn mạnh việc giữ nguyên vị trí tương đối). Màu sắc cũng có nghĩa: xanh lá là trạng thái hoạt động, trắng là đã chuẩn bị, magenta/vàng là giá trị chọn.</p>",
 "<p>The fastest way to learn the PFD is to follow the T layout of the old mechanical dials: speed left, attitude centre, altitude right, heading below. The EFIS keeps those positions so pilots switching aircraft types need not relearn them (Tooley section 1.2 stresses preserving relative positions). Colours also carry meaning: green is active, white is armed, magenta/yellow are selected values.</p>",
 "disp_p21.jpg"),

("ND của A320: núm chọn chế độ và tầm",
 "The A320 ND: mode and range selectors",
 "<p>Bảng điều khiển EFIS (ND control panel) cho phép:</p><ul>"
 "<li>Chọn chế độ hiển thị: <b>ROSE ILS, ROSE VOR, ROSE NAV, ARC, PLAN</b>.</li>"
 "<li>Chọn tầm: 20, 40, 80, 160, 320 NM (núm tầm).</li>"
 "<li>Bật dữ liệu bổ sung: CSTR (ràng buộc), WPT (điểm đường bay), VOR.D, NDB, ARPT (sân bay); FD (chỉ huy bay), LS (localiser/glide slope).</li>"
 "<li>Đặt QNH và bật/tắt ND (núm kéo/đẩy).</li></ul>"
 "<p>Chế độ <b>PLAN</b>: xem trước kế hoạch bay quanh một điểm, hướng bắc luôn hướng lên.</p>",
 "<p>The EFIS (ND) control panel lets you:</p><ul>"
 "<li>Choose the display mode: <b>ROSE ILS, ROSE VOR, ROSE NAV, ARC, PLAN</b>.</li>"
 "<li>Choose the range: 20, 40, 80, 160, 320 NM (range knob).</li>"
 "<li>Turn on extra data: CSTR (constraints), WPT (waypoints), VOR.D, NDB, ARPT (airports); FD (flight director), LS (localiser/glide slope).</li>"
 "<li>Set QNH and switch the ND on/off (pull/push knob).</li></ul>"
 "<p><b>PLAN</b> mode: preview the flight plan around a point, north always up.</p>",
 "<p>Slide này bị cắt ở phía dưới (các khung \"ND display modes\" và \"PLAN mode characteristics\" chỉ còn tiêu đề), nên nội dung PLAN ở trên lấy từ phần còn thấy được của slide và từ các slide kế tiếp. Trên hình ND chế độ PLAN, phi công thấy tốc độ mặt đất (GS) và tốc độ thực (TAS) ở góc trên trái, gió dưới đó, điểm đến đã chọn (VESTI) và khoảng cách bên phải, các vòng khoảng cách 20 và 40 NM.</p>",
 "<p>This slide is cut off at the bottom (the \"ND display modes\" and \"PLAN mode characteristics\" boxes show only their headings), so the PLAN content above comes from the visible part of the slide and the following slides. On the ND image in PLAN mode the pilot sees ground speed (GS) and true airspeed (TAS) at the top left, wind below it, the selected waypoint (VESTI) and its distance on the right, and range rings at 20 and 40 NM.</p>",
 "disp_p22.jpg"),

("ND: ROSE ILS và ROSE VOR",
 "ND: ROSE ILS and ROSE VOR",
 "<p><b>ROSE ILS</b> (tiếp cận ILS): hiển thị kim <b>localiser</b> (lệch ngang) và kim <b>glide slope</b> (lệch đứng) quanh biểu tượng máy bay; góc trên phải ghi tần số ILS, hướng tuyến chọn và nhận dạng đường băng. Các vòng tròn đồng tâm biểu thị khoảng cách (NM).</p>"
 "<p><b>ROSE VOR</b>: đường xanh lam là hướng tuyến chọn tới/từ đài VOR, con trỏ phương vị (bearing pointer) chỉ về đài đang chọn; góc trên phải ghi tần số VOR và hướng tuyến, góc dưới ghi tên và khoảng cách VOR 1 và VOR 2. \"OOD\" nghĩa là ngoài tầm (out of range, chưa thu được đài).</p>",
 "<p><b>ROSE ILS</b> (ILS approach): shows the <b>localiser</b> needle (lateral deviation) and the <b>glide slope</b> needle (vertical deviation) around the aircraft symbol; the top right gives the ILS frequency, selected course and runway identifier. Concentric circles give distance (NM).</p>"
 "<p><b>ROSE VOR</b>: the blue line is the selected course to/from the VOR station and the bearing pointer points to the selected station; the top right gives VOR frequency and course, the bottom gives name and distance for VOR 1 and VOR 2. \"OOD\" means out of range (station not received).</p>",
 "<p>Kim <b>localiser</b> cho biết máy bay lệch trái hay phải so với trục đường băng, kim <b>glide slope</b> cho biết lệch trên hay dưới đường lượn. Phi công điều khiển để đưa cả hai kim về giữa. Trên EADI, cùng thông tin đó xuất hiện dưới dạng \"đường băng nổi lên\" (rising runway) và kim glide slope (câu trắc nghiệm 10, 11 chương 1).</p>",
 "<p>The <b>localiser</b> needle tells whether the aircraft is left or right of the runway centreline, the <b>glide slope</b> needle tells whether it is above or below the glide path. The pilot flies to bring both needles to the centre. On the EADI the same information appears as the \"rising runway\" and the glide slope pointer (chapter 1 quiz questions 10 and 11).</p>",
 "disp_p23.jpg"),

("ND: ROSE NAV và ARC NAV",
 "ND: ROSE NAV and ARC NAV",
 "<table class='tt'><thead><tr><th></th><th>ROSE NAV</th><th>ARC NAV</th></tr></thead><tbody>"
 "<tr><td>Góc nhìn</td><td>360° quanh máy bay (plan view)</td><td>Phía trước, khoảng 80°</td></tr>"
 "<tr><td>Vị trí máy bay</td><td>Cố định ở tâm</td><td>Cố định ở dưới giữa</td></tr>"
 "<tr><td>La bàn</td><td>Quay theo hướng bay, bắc ở trên khi bay hướng bắc</td><td>Chỉ hiện cung phía trước</td></tr>"
 "<tr><td>Dùng khi</td><td>Hành trình và tiếp cận</td><td>Hành trình, cần nhìn rõ phía trước</td></tr></tbody></table>"
 "<p>Cả hai hiển thị: tuyến bay (xanh lá/đỏ tươi), điểm đường bay, VOR/NDB, sân bay, echo radar thời tiết, vòng khoảng cách 20 và 40 NM, độ nghiêng anten radar (TILT).</p>",
 "<table class='tt'><thead><tr><th></th><th>ROSE NAV</th><th>ARC NAV</th></tr></thead><tbody>"
 "<tr><td>View</td><td>360° around the aircraft (plan view)</td><td>Forward sector, about 80°</td></tr>"
 "<tr><td>Aircraft symbol</td><td>Fixed at the centre</td><td>Fixed at bottom centre</td></tr>"
 "<tr><td>Compass</td><td>Rotates with heading</td><td>Shows only the forward arc</td></tr>"
 "<tr><td>Use</td><td>En-route and approach</td><td>En-route, when a clearer forward view is needed</td></tr></tbody></table>"
 "<p>Both show: flight plan route (green/magenta), waypoints, VOR/NDB, airports, weather radar echoes, range rings at 20 and 40 NM, radar antenna tilt (TILT).</p>",
 "<p>Về dữ liệu \"thời gian đến điểm bay\" trên ND: slide ghi nhãn \"23 33\" là thời gian ước tính (23 phút 33 giây), nhưng ở khoảng cách 37 NM và tốc độ mặt đất 257 kt, thời gian bay chỉ khoảng 8,6 phút (37/257 giờ). Vì vậy \"23 33\" nhiều khả năng là giờ dự kiến đến (ETA) theo giờ UTC. Đây là nghi vấn tự kiểm tra, chưa xác nhận bằng tài liệu hãng.</p>",
 "<p>About the \"time to waypoint\" data on the ND: the slide labels \"23 33\" as an estimated time (23 min 33 s), but at 37 NM and a ground speed of 257 kt the flight time is only about 8.6 minutes (37/257 hour). So \"23 33\" is more likely an estimated time of arrival (ETA) as UTC clock time. This is a self-check doubt, not confirmed against manufacturer documents.</p>",
 "disp_p24.jpg"),
],
# ------------------------------------------------------------------ PART 4
[
("ECAM và EICAS: hai tên cho một ý tưởng",
 "ECAM and EICAS: two names for one idea",
 "<p>Theo Tooley (mục 1.1.6, 1.1.7, 15.3): <b>ECAM</b> (Airbus) và <b>EICAS</b> (Boeing) đều dùng <b>hai màn hình dọc đặt giữa bảng điều khiển</b>. Màn hình trên (chính) hiển thị thông số động cơ (N1, EGT, N2, lưu lượng nhiên liệu, vị trí cánh tà và slat) và cảnh báo; màn hình dưới (phụ) hiển thị thông tin bổ sung và hậu quả khi có hỏng hóc.</p>"
 "<p>Lợi ích: loại bỏ đồng hồ động cơ truyền thống, giảm số đồng hồ riêng lẻ, giảm tải công việc phi công, hỗ trợ bảo trì và giảm chi phí vận hành. Bài giảng thêm: ECAM có bảng điều khiển ở giữa (độ sáng, chọn trang, EMER CANC, CLR, STS, RCL).</p>",
 "<p>Per Tooley (sections 1.1.6, 1.1.7, 15.3): <b>ECAM</b> (Airbus) and <b>EICAS</b> (Boeing) both use <b>two vertical screens centrally mounted on the panel</b>. The upper (primary) screen shows engine parameters (N1, EGT, N2, fuel flow, flap and slat positions) and alerts; the lower (secondary) screen shows additional information and the consequences of any malfunction.</p>"
 "<p>Benefits: no traditional engine gauges, fewer separate instruments, lower pilot workload, maintenance support and lower operating cost. The lecture adds: ECAM has a central control panel (brightness, page selection, EMER CANC, CLR, STS, RCL).</p>",
 "<p>Hai tên này đúng với hai hãng: Airbus dùng ECAM, Boeing dùng EICAS. EICAS của Boeing có thêm khối DCU (data concentrator unit) nhận dữ liệu từ bus ARINC 429 tốc độ cao và thấp, tín hiệu analog và rời rạc, rồi gom lại cho màn hình, bộ ghi dữ liệu bay và bộ điều khiển đèn (LDU điều khiển tới 120 đèn). Nếu một màn hình EICAS hỏng, màn hình còn lại hiển thị dữ liệu EICAS chính (câu trắc nghiệm 13 chương 15).</p><p>Slide ECAM của bài giảng viết ECAM \"xử lý trong CFDIU\", trong khi slide sơ đồ EIS ghi DMC, FWC, SDAC làm việc đó; hai slide mô tả hơi khác nhau, cần đối chiếu tài liệu bảo dưỡng của hãng khi học sâu.</p>",
 "<p>The two names match the two manufacturers: Airbus uses ECAM, Boeing uses EICAS. Boeing's EICAS also has a DCU (data concentrator unit) that takes data from high- and low-speed ARINC 429 buses, analogue and discrete inputs and gathers it for the screens, the flight data recorder and the lamp driver (the LDU drives up to 120 lamps). If one EICAS display fails, the remaining display shows the primary EICAS data (chapter 15 quiz question 13).</p><p>The lecture's ECAM slide says ECAM is \"processed in the CFDIU\", while the EIS diagram slide has the DMC, FWC and SDAC do this; the two slides describe it slightly differently, so check the manufacturer's maintenance documents when studying in depth.</p>",
 "disp_p26.jpg"),

("E/WD: thông số động cơ trên màn hình trên",
 "E/WD: engine parameters on the upper screen",
 "<table class='tt'><thead><tr><th>Ký hiệu</th><th>Ý nghĩa</th><th>Ghi chú từ slide</th></tr></thead><tbody>"
 "<tr><td>EPR</td><td>Tỉ số áp suất động cơ</td><td>Chỉ lực đẩy; giá trị thường khoảng 1,0 đến 1,6</td></tr>"
 "<tr><td>N1</td><td>Tốc độ quạt (cụm áp THẤP)</td><td>Hiển thị theo % tối đa; nhàn rỗi khoảng 20 đến 25%</td></tr>"
 "<tr><td>N2</td><td>Tốc độ cụm áp CAO</td><td>Khoảng 90 đến 100% lúc cất cánh</td></tr>"
 "<tr><td>EGT</td><td>Nhiệt độ khí xả (°C)</td><td>Có vùng đỏ giới hạn</td></tr>"
 "<tr><td>F.F</td><td>Lưu lượng nhiên liệu (kg/h)</td><td>Tăng theo lực đẩy</td></tr>"
 "<tr><td>FLX/TOGA</td><td>Chế độ lực đẩy</td><td>FLX: cất cánh giảm lực đẩy với nhiệt độ giả định; TOGA: tối đa</td></tr></tbody></table>",
 "<table class='tt'><thead><tr><th>Symbol</th><th>Meaning</th><th>Slide note</th></tr></thead><tbody>"
 "<tr><td>EPR</td><td>Engine pressure ratio</td><td>Indicates thrust; typical value about 1.0 to 1.6</td></tr>"
 "<tr><td>N1</td><td>Fan speed (LOW pressure spool)</td><td>Shown as % of maximum; idle about 20 to 25%</td></tr>"
 "<tr><td>N2</td><td>HIGH pressure spool speed</td><td>About 90 to 100% at take-off</td></tr>"
 "<tr><td>EGT</td><td>Exhaust gas temperature (°C)</td><td>Has a red limit zone</td></tr>"
 "<tr><td>F.F</td><td>Fuel flow (kg/h)</td><td>Rises with thrust</td></tr>"
 "<tr><td>FLX/TOGA</td><td>Thrust mode</td><td>FLX: reduced take-off thrust with assumed temperature; TOGA: maximum</td></tr></tbody></table>",
 "<p><b>Sửa một lỗi trong slide:</b> slide ghi N2 là \"tốc độ tuabin áp thấp\". Chính slide ghi N1 là cụm áp thấp, và Tooley (mục 1.1.6) viết \"N1/fan speed, EGT, N2/high pressure turbine speed\", nên N2 là áp cao. Bảng trên đã sửa lại theo Tooley.</p><p>Màu trên thang đo: xanh lá bình thường, hổ phách thận trọng, đỏ giới hạn. Ví dụ \"FLX 1.498 49°C\" nghĩa là cất cánh giảm lực đẩy tính với nhiệt độ giả định 49 °C. Dòng chữ ở dưới là thông báo ECAM (đây là tàu bay trên mặt đất: SEAT BELTS, NO SMOKING, GND SPLRS ARMED; T.O INHIBIT nghĩa là lực đẩy cất cánh bị chặn).</p>",
 "<p><b>Correcting a slide error:</b> the slide calls N2 the \"low pressure turbine speed\". The same slide calls N1 the low pressure spool, and Tooley (section 1.1.6) writes \"N1/fan speed, EGT, N2/high pressure turbine speed\", so N2 is the high pressure one. The table above has been corrected to follow Tooley.</p><p>Scale colours: green normal, amber caution, red limit. For example \"FLX 1.498 49°C\" means a reduced-thrust take-off computed with an assumed temperature of 49 °C. The text lines below are ECAM messages (this is an aircraft on the ground: SEAT BELTS, NO SMOKING, GND SPLRS ARMED; T.O INHIBIT means take-off thrust is inhibited).</p>",
 "disp_p25.jpg"),

("Trang PRESS: áp suất cabin",
 "The PRESS page: cabin pressure",
 "<p>Trang <b>CAB PRESS</b> cho biết áp suất cabin do hệ thống điều áp duy trì:</p><ul>"
 "<li><b>ΔP</b> (psi): chênh áp giữa cabin và bên ngoài.</li>"
 "<li><b>V/S</b> (ft/min): tốc độ thay đổi độ cao cabin; UP là tăng áp, DN là giảm áp.</li>"
 "<li><b>CAB ALT</b> (ft): độ cao cabin mô phỏng, tức mức mà hành khách \"cảm nhận\".</li>"
 "<li><b>LDG ELEV</b>: cao độ sân bay hạ cánh (AUTO).</li>"
 "<li>Van: <b>INLET</b> (khí từ động cơ), <b>EXTRACT</b> (van xả điều chỉnh áp), <b>SAFETY</b> (tự mở khi quá áp); <b>PACK 1, 2</b> cấp khí điều hoà.</li></ul>"
 "<p>Giá trị điển hình khi bay hành trình: ΔP khoảng 7 đến 8 psi, CAB ALT 0 đến 8 000 ft, V/S gần 0.</p>",
 "<p>The <b>CAB PRESS</b> page shows the cabin pressure maintained by the pressurisation system:</p><ul>"
 "<li><b>ΔP</b> (psi): differential pressure between cabin and outside.</li>"
 "<li><b>V/S</b> (ft/min): rate of change of cabin altitude; UP is pressurising, DN is depressurising.</li>"
 "<li><b>CAB ALT</b> (ft): simulated cabin altitude, what passengers \"feel\".</li>"
 "<li><b>LDG ELEV</b>: landing airport elevation (AUTO).</li>"
 "<li>Valves: <b>INLET</b> (air from engines), <b>EXTRACT</b> (outflow valve regulating pressure), <b>SAFETY</b> (opens automatically on overpressure); <b>PACK 1, 2</b> supply conditioned air.</li></ul>"
 "<p>Typical cruise values: ΔP about 7 to 8 psi, CAB ALT 0 to 8,000 ft, V/S near 0.</p>",
 "<p><b>Một con số trong slide không khớp lý thuyết.</b> Ở FL140 (14 000 ft) trong khí quyển chuẩn ISA, áp suất ngoài khoảng 8,63 psi; độ cao cabin 2 870 ft ứng với áp suất khoảng 13,23 psi. Hiệu của chúng là ΔP ≈ 4,6 psi, trong khi slide hiển thị 2,9 psi. SAT −13 °C của slide đúng với ISA ở FL140 (15 − 2×14 = −13 °C), nên khó giải thích bằng nhiệt độ lệch ISA. Kết luận: ΔP 2,9 psi chỉ là số minh hoạ, đừng học thuộc. Phép tính nằm trong notebook (công thức khí áp ISA).</p>",
 "<p><b>One number in the slide does not match theory.</b> At FL140 (14,000 ft) in the ISA standard atmosphere the outside pressure is about 8.63 psi; a cabin altitude of 2,870 ft corresponds to about 13.23 psi. Their difference is ΔP ≈ 4.6 psi, whereas the slide shows 2.9 psi. The slide's SAT of −13 °C is exactly ISA at FL140 (15 − 2×14 = −13 °C), so a non-ISA temperature does not explain it. Conclusion: the 2.9 psi ΔP is just an illustrative number, do not memorise it. The calculation is in the notebook (ISA pressure formula).</p>",
 "disp_p29.jpg"),

("Trang ELEC: sơ đồ nguồn điện",
 "The ELEC page: the electrical power diagram",
 "<ul><li><b>GEN 1, GEN 2</b>: máy phát xoay chiều chạy bởi động cơ (qua IDG), cấp thanh cái <b>AC 1</b> và <b>AC 2</b>.</li>"
 "<li><b>TR 1, TR 2</b> (transformer rectifier): đổi AC sang DC, cấp <b>DC 1</b> và <b>DC 2</b>.</li>"
 "<li><b>BAT 1, 2</b>: ắc quy cấp DC khởi động và dự phòng.</li>"
 "<li><b>AC ESS, DC ESS</b>: thanh cái thiết yếu; có thể được cấp từ <b>EMER GEN</b> (máy phát khẩn cấp chạy bằng tuabin gió RAT) qua ESS TR khi cần.</li>"
 "<li><b>IDG 1, 2</b>: hiển thị nhiệt độ dầu của máy phát.</li></ul>"
 "<p>Slide so sánh hai trạng thái: hai động cơ chạy (bình thường) và một động cơ chạy (GEN mất, TR tương ứng không có nguồn).</p>",
 "<ul><li><b>GEN 1, GEN 2</b>: AC generators driven by the engines (through the IDG), feeding the <b>AC 1</b> and <b>AC 2</b> buses.</li>"
 "<li><b>TR 1, TR 2</b> (transformer rectifier): convert AC to DC, feeding <b>DC 1</b> and <b>DC 2</b>.</li>"
 "<li><b>BAT 1, 2</b>: batteries supplying DC for start-up and backup.</li>"
 "<li><b>AC ESS, DC ESS</b>: essential buses; they can be supplied by the <b>EMER GEN</b> (emergency generator driven by the RAT wind turbine) through the ESS TR when required.</li>"
 "<li><b>IDG 1, 2</b>: display the generator oil temperature.</li></ul>"
 "<p>The slide compares two states: both engines running (normal) and one engine running (a GEN is lost, the corresponding TR has no supply).</p>",
 "<p>Luồng điện logic: GEN (AC) → thanh cái AC → TR (AC sang DC) → thanh cái DC. Khi GEN 1 mất, AC 1 và TR 1 và DC 1 cũng mất nguồn (hiện \"0 V, 0 A\"), nhưng AC ESS và DC ESS vẫn được cấp từ phía còn lại.</p><p><b>Điểm nghi vấn trong slide:</b> hình màn hình vẽ GEN \"420 V, 200 Hz\". Nguồn xoay chiều máy bay là <b>115 V, 400 Hz</b> (Tooley có nhắc nguồn 115 V AC 400 Hz), nên hai con số trên hình rõ ràng là giá trị minh hoạ sai.</p>",
 "<p>The logical power flow: GEN (AC) → AC bus → TR (AC to DC) → DC bus. When GEN 1 is lost, AC 1, TR 1 and DC 1 also lose supply (showing \"0 V, 0 A\"), but AC ESS and DC ESS are still fed from the other side.</p><p><b>A doubtful point in the slide:</b> the screen picture draws GEN as \"420 V, 200 Hz\". Aircraft AC power is <b>115 V, 400 Hz</b> (Tooley mentions a 115 V AC 400 Hz supply), so those two numbers on the picture are clearly wrong illustrative values.</p>",
 "disp_p30.jpg"),

("Trang HYD: ba hệ thuỷ lực",
 "The HYD page: three hydraulic systems",
 "<p>Ba hệ <b>GREEN</b> (trái), <b>BLUE</b> (giữa), <b>YELLOW</b> (phải), áp suất bình thường khoảng <b>3000 psi</b>.</p><ul>"
 "<li><b>Bơm do động cơ</b> (EDP) số 1 (hệ xanh lá) và số 2 (hệ vàng): hiện màu xanh lá khi sẵn sàng.</li>"
 "<li><b>Bơm điện</b> (ELEC): theo slide, dành cho hệ GREEN và YELLOW, hiện xanh lá khi sẵn sàng.</li>"
 "<li><b>RAT</b> (tuabin gió khẩn cấp) và <b>APU</b>: nguồn dự phòng; có đường nối chéo giữa các hệ.</li>"
 "<li>Bơm tắt: hiện chữ <b>LO</b> màu hổ phách, áp suất 0 psi (tình huống tàu nằm đất, động cơ tắt).</li></ul>",
 "<p>Three systems, <b>GREEN</b> (left), <b>BLUE</b> (centre), <b>YELLOW</b> (right), with a normal pressure of about <b>3000 psi</b>.</p><ul>"
 "<li><b>Engine-driven pumps</b> (EDP) 1 (green system) and 2 (yellow system): shown green when available.</li>"
 "<li><b>Electric pumps</b> (ELEC): per the slide, for the GREEN and YELLOW systems, shown green when available.</li>"
 "<li><b>RAT</b> (emergency wind turbine) and <b>APU</b>: backup sources; cross-ties link the systems.</li>"
 "<li>Pump off: a <b>LO</b> in amber and 0 psi (aircraft on the ground, engines off).</li></ul>",
 "<p>Hệ thuỷ lực cấp năng lượng cho điều khiển bay chính, càng đáp, phanh, spoiler. Ba hệ độc lập là một ví dụ của nguyên tắc dự phòng trong yêu cầu thiết kế. Quy ước màu nhất quán xuyên suốt ECAM: xanh lá là bình thường, hổ phách là cần chú ý, đỏ là giới hạn.</p><p>Lưu ý khi đọc slide: các nhãn bơm trong slide (bơm động cơ cho hệ trái và phải, bơm điện cho hệ GREEN và YELLOW) là cách bài giảng mô tả; hãy đối chiếu tài liệu bảo dưỡng của hãng nếu cần chi tiết cấu hình thật của từng hệ.</p>",
 "<p>The hydraulic systems power the primary flight controls, landing gear, brakes and spoilers. Three independent systems exemplify the redundancy principle from the design requirements. The colour convention is consistent across ECAM: green is normal, amber needs attention, red is a limit.</p><p>A note when reading the slide: the pump labels (engine pumps for the left and right systems, electric pumps for GREEN and YELLOW) are how the lecture describes it; check the manufacturer's maintenance documents if you need the real configuration of each system.</p>",
 "disp_p31.jpg"),

("Trang FUEL: nhiên liệu",
 "The FUEL page: fuel",
 "<p>Trang FUEL hiển thị: nhiên liệu đã dùng của từng động cơ (<b>F.USED 1, 2</b>), nhiên liệu trên tàu (<b>FOB</b>), lượng và nhiệt độ từng thùng (trái ngoài, trái trong, giữa, phải trong, phải ngoài), bơm (xanh lá khi chạy, hổ phách khi dừng), tiêu thụ APU.</p>"
 "<table class='tt'><thead><tr><th>Trạng thái</th><th>Các thùng (kg)</th><th>Tổng</th><th>FOB hiển thị</th></tr></thead><tbody>"
 "<tr><td>Bơm TẮT</td><td>686 + 2742 + 5852 + 2741 + 686</td><td>12 707</td><td>12 707</td></tr>"
 "<tr><td>Bơm BẬT</td><td>106 + 2742 + 4902 + 2741 + 106</td><td>10 597</td><td>10 598</td></tr></tbody></table>",
 "<p>The FUEL page shows: fuel used by each engine (<b>F.USED 1, 2</b>), fuel on board (<b>FOB</b>), quantity and temperature of each tank (left outer, left inner, centre, right inner, right outer), pumps (green when running, amber when stopped), APU consumption.</p>"
 "<table class='tt'><thead><tr><th>State</th><th>Tanks (kg)</th><th>Sum</th><th>FOB shown</th></tr></thead><tbody>"
 "<tr><td>Pumps OFF</td><td>686 + 2742 + 5852 + 2741 + 686</td><td>12,707</td><td>12,707</td></tr>"
 "<tr><td>Pumps ON</td><td>106 + 2742 + 4902 + 2741 + 106</td><td>10,597</td><td>10,598</td></tr></tbody></table>",
 "<p>Phép cộng kiểm tra: ở trạng thái bơm TẮT, năm thùng cộng đúng 12 707 kg, khớp FOB; ở trạng thái bơm BẬT, tổng là 10 597 kg trong khi FOB hiển thị 10 598 kg. Chênh một kilôgam là sai số làm tròn của từng thùng (mỗi thùng được làm tròn riêng), nên đây không phải lỗi của slide. Notebook kiểm lại hai tổng này.</p><p>Một quy tắc đọc: bơm hổ phách (dừng) thì F.USED giữ 0 vì không có dòng nhiên liệu; bơm xanh lá (chạy) thì F.USED tăng và FOB giảm dần.</p>",
 "<p>A check by addition: with the pumps OFF the five tanks add up to exactly 12,707 kg, matching the FOB; with the pumps ON the sum is 10,597 kg while the FOB shows 10,598 kg. The one-kilogram difference is rounding in each tank (each is rounded separately), so it is not a slide error. The notebook rechecks both sums.</p><p>A reading rule: with amber (stopped) pumps F.USED stays 0 because no fuel flows; with green (running) pumps F.USED rises and FOB falls steadily.</p>",
 "disp_p32.jpg"),

("Trang COND và F/CTL",
 "The COND and F/CTL pages",
 "<p><b>COND</b> (điều hoà không khí): nhiệt độ buồng lái (CKPT), cabin trước (FWD), cabin sau (AFT) tính bằng °C; khí nóng \"HOT AIR\" lấy từ động cơ, qua bộ điều hoà (pack), mỗi vùng có van điều chỉnh nhiệt độ (ký hiệu H).</p>"
 "<p><b>F/CTL</b> (điều khiển bay): trạng thái các bề mặt điều khiển (spoiler, aileron, elevator, rudder) và các máy tính <b>ELAC</b> (Elevator Aileron Computer) và <b>SEC</b> (Spoiler Elevator Computer), cùng hệ thuỷ lực G, B, Y. Hộp xanh lá là máy tính hoạt động, hộp hổ phách nét đứt là không sẵn sàng.</p>" + fig("disp_p33.jpg", "ECAM COND page"),
 "<p><b>COND</b> (air conditioning): cockpit (CKPT), forward cabin (FWD) and aft cabin (AFT) temperatures in °C; \"HOT AIR\" bleed from the engines passes through the air conditioning pack, and each zone has a temperature control valve (symbol H).</p>"
 "<p><b>F/CTL</b> (flight controls): status of the control surfaces (spoiler, aileron, elevator, rudder) and of the <b>ELAC</b> (Elevator Aileron Computer) and <b>SEC</b> (Spoiler Elevator Computer) computers, plus hydraulic systems G, B, Y. A green box is an active computer, a dashed amber box is unavailable.</p>" + fig("disp_p33.jpg", "ECAM COND page"),
 "<p>Với F/CTL, hai điểm cần nhớ: mũi tên xanh lên trên cánh nghĩa là spoiler đang mở; màn hình trái hiện spoiler trái mở là máy bay đang rẽ trái (roll trái), màn hình phải hiện spoiler phải mở là rẽ phải. Slide sau cùng đặt hai trạng thái này cạnh nhau.</p><p>Thận trọng: ở slide F/CTL \"tất cả điều khiển bay dừng\", bài giảng kết luận khi hệ GBY mất áp thì mọi máy tính điều khiển bay không còn khả dụng. Đây là một tình huống minh hoạ đơn giản hoá, đừng suy ra như một quy tắc vận hành thực tế.</p>",
 "<p>For F/CTL, two points to remember: green upward arrows on the wing mean spoilers deployed; the left screen with left spoilers deployed means the aircraft is turning left (rolling left), the right screen with right spoilers deployed means turning right. The last slide puts the two states side by side.</p><p>Caution: on the \"all flight controls stopped\" F/CTL slide the lecture concludes that when the GBY hydraulics lose pressure all flight control computers become unavailable. This is a simplified illustrative case; do not take it as a real operating rule.</p>",
 "disp_p34.jpg"),

("EICAS của Boeing và bộ DCU (Tooley 15.3)",
 "Boeing EICAS and the DCU (Tooley 15.3)",
 "<p>EICAS gồm <b>hai màn hình màu độ phân giải cao</b> cùng bảng điều khiển, hai hoặc ba <b>DCU</b> và một bộ điều khiển đèn (LDU). Màn hình EICAS <b>chính</b> có định dạng cố định: tốc độ và nhiệt độ, lưu lượng và lượng nhiên liệu, rung động động cơ, vị trí cánh tà, thông báo cảnh báo CAS (mã màu theo mức độ quan trọng). Màn hình <b>phụ</b> chọn theo trang: càng đáp, cánh tà/trim, APU, điều áp/chống băng, nhiên liệu/thuỷ lực, vị trí điều khiển bay, cửa, điện AC/DC.</p>"
 "<p>EICAS liên tục giám sát vượt dung sai và thông báo cho phi hành đoàn khi có sự kiện. ECAM của Airbus cũng tự động cảnh báo khi hỏng hóc, nhưng phi hành đoàn còn có thể chọn thủ công từng hệ để xem.</p>",
 "<p>EICAS comprises <b>two large high-resolution colour displays</b> with control panels, two or three <b>DCUs</b> and a lamp driver unit (LDU). The <b>primary</b> EICAS display has a fixed format: speed and temperature, fuel flow and quantity, engine vibration, flap positions, CAS caution messages (colour-coded by importance). The <b>secondary</b> display is page-selectable: landing gear, flaps/trim, APU, cabin pressure/anti-ice, fuel/hydraulics, flight control positions, doors, AC and DC electrics.</p>"
 "<p>EICAS continuously monitors for out-of-tolerance conditions and tells the crew when an event occurs. Airbus's ECAM also warns automatically on malfunctions, but the crew can also select each system manually to view it.</p>",
 "<p>Có hai điểm trắc nghiệm đáng nhớ: một là EICAS cung cấp <b>thông số động cơ và cảnh báo hệ thống</b>, không chỉ riêng động cơ (câu 18 chương 1); hai là ở phần ECAM, tin nhắn lỗi do phi hành đoàn ghi lại có thể được nhân viên bảo trì truy vết tiếp bằng chức năng thử hệ thống trên bảng bảo trì trong buồng lái và BITE trên từng máy tính (Tooley 15.10).</p>",
 "<p>Two quiz points worth remembering: first, EICAS provides <b>engine parameters and system warnings</b>, not engine data only (chapter 1 Q18); second, for ECAM, failure messages noted by the crew can be followed up by maintenance staff with the system test facility on the cockpit maintenance panel and the BITE on each computer (Tooley 15.10).</p>",
 None),
],
# ------------------------------------------------------------------ PART 5
[
("CMC: máy tính bảo trì tập trung và MCDU",
 "CMC: the centralised maintenance computer and the MCDU",
 "<p>Nhiều LRU (động cơ, điều hoà, điều khiển bay...) liên tục gửi dữ liệu bảo trì, từ trạng thái, thông tin lỗi qua <b>ARINC 429</b> và tín hiệu rời rạc tới <b>CMC</b>.</p><ul>"
 "<li>Có <b>hai CMC giống nhau</b>: CMC 1 hoạt động, CMC 2 dự phòng.</li>"
 "<li>CMC thu, xử lý, lưu dữ liệu; gắn dấu thời gian bằng đồng hồ nội; phát hiện và ghi lỗi.</li>"
 "<li>Đưa dữ liệu ra: <b>MCDU</b> (xem thông báo, ví dụ CFDS), <b>máy in</b>, và <b>ACARS</b> (tuỳ chọn) gửi báo cáo bảo trì xuống mặt đất.</li></ul>"
 "<p>Ví dụ truy cập: trên MCDU chọn MCDU MENU → CFDS để xem lỗi lưu trong CMC.</p>",
 "<p>Many LRUs (engines, air conditioning, flight controls...) continuously send maintenance data, status and fault information over <b>ARINC 429</b> and discrete signals to the <b>CMC</b>.</p><ul>"
 "<li>There are <b>two identical CMCs</b>: CMC 1 active, CMC 2 standby.</li>"
 "<li>The CMC collects, processes and stores data; time-stamps it with an internal clock; detects and logs faults.</li>"
 "<li>Data leaves through the <b>MCDU</b> (viewing messages, for example CFDS), the <b>printer</b>, and <b>ACARS</b> (optional) which sends maintenance reports to the ground.</li></ul>"
 "<p>Access example: on the MCDU choose MCDU MENU → CFDS to view faults stored in the CMC.</p>",
 "<p>Hình dung CMC như \"hộp đen bảo trì\" nhưng cho kỹ sư mặt đất, không phải để điều tra tai nạn. Nó là lý do một kỹ thuật viên chỉ cần cắm vào một điểm (MCDU) là xem được lỗi của hàng chục hệ thống thay vì mở từng LRU. Câu trắc nghiệm 8 chương 15: CMC cho phép giám sát và kiểm tra cả trên mặt đất lẫn khi bay.</p>",
 "<p>Picture the CMC as a \"maintenance black box\", but for ground engineers, not for accident investigation. It is why a technician can plug in at a single point (the MCDU) and see the faults of dozens of systems instead of opening each LRU. Chapter 15 quiz question 8: the CMC provides monitoring and testing both on the ground and in flight.</p>",
 "disp_p19.jpg"),

("ACARS: liên kết dữ liệu VHF giữa máy bay và mặt đất",
 "ACARS: the VHF data link between aircraft and ground",
 "<p>ACARS (Aircraft Communications Addressing and Reporting System) là liên kết dữ liệu số trong dải <b>VHF 129 đến 137 MHz</b>, cho phép hãng bay trao đổi dữ liệu với máy bay mà không cần người, tương tự thư điện tử. Chuẩn ban đầu ARINC 597, sau sửa thành ARINC 724B.</p>"
 "<ul><li><b>ACMU</b> (management unit) thu phát qua bộ thu phát VHF 3; <b>MCDU</b> là giao diện phi công; có máy in.</li>"
 "<li>Loại bản tin: <b>OOOI</b> (rời cổng, rời mặt đất, chạm đất, vào cổng), dữ liệu FMS, tình trạng thiết bị, bản tin ping định kỳ, bản tin phi công gửi tay.</li>"
 "<li>Bản tin gồm: chế độ, số đăng ký máy bay, nhãn bản tin, mã khối, số bản tin, số chuyến bay, nội dung.</li></ul>",
 "<p>ACARS (Aircraft Communications Addressing and Reporting System) is a digital data link in the <b>VHF band 129 to 137 MHz</b>, letting an airline exchange data with an aircraft without human involvement, much like e-mail. The original standard was ARINC 597, later revised as ARINC 724B.</p>"
 "<ul><li>The <b>ACMU</b> (management unit) transmits and receives through VHF 3; the <b>MCDU</b> is the pilot interface; there is a printer.</li>"
 "<li>Message types: <b>OOOI</b> (out of the gate, off the ground, on the ground, into the gate), FMS data, equipment health, periodic ping messages, crew-sent manual messages.</li>"
 "<li>A message contains: mode, aircraft registration, message label, block id, message number, flight id, content.</li></ul>",
 "<p>Tốc độ dữ liệu thấp và bản tin chỉ là văn bản ký tự, nên ACARS thay thế phần lớn liên lạc thoại HF/VHF nhàm chán (trọng tải, báo cáo khởi hành và đến, nhiên liệu, hiệu năng động cơ). Chín kênh trong Bảng 15.1 của Tooley đều nằm trong dải 129 đến 137 MHz (đã kiểm lại trong notebook).</p><p>Hai câu trắc nghiệm chương 15: chuẩn ACARS được định nghĩa trong <b>ARINC 724</b> (không phải 429 hay 573); ACARS dùng kênh trong phổ <b>VHF</b>; và ACARS là phương pháp báo lỗi trong chuyến bay về trạm kỹ thuật mặt đất.</p>",
 "<p>The data rate is low and messages are plain characters, so ACARS replaces much of the mundane HF/VHF voice traffic (passenger loads, departure and arrival reports, fuel, engine performance). All nine channels in Tooley's Table 15.1 lie inside 129 to 137 MHz (rechecked in the notebook).</p><p>Two chapter 15 quiz questions: the ACARS standard is defined in <b>ARINC 724</b> (not 429 or 573); ACARS uses channels in the <b>VHF</b> spectrum; and ACARS is a method of reporting in-flight faults to an engineering and monitoring ground station.</p>",
 "disp_p20.jpg"),

("Tổng kết: màn hình nằm ở đâu trong mạng avionics",
 "Wrap-up: where displays sit in the avionics network",
 "<ol><li>Cảm biến và máy tính đo hoặc tính dữ liệu và phát qua <b>bus</b> (ARINC 429, AFDX) (Module 05).</li>"
 "<li><b>DMC/bộ tạo ký hiệu</b> biến số thành hình ảnh, <b>FWC</b> thêm cảnh báo, <b>SDAC</b> thêm dữ liệu hệ thống.</li>"
 "<li>Màn hình <b>CRT hoặc AMLCD</b> hiển thị: PFD, ND (EFIS) và E/WD, SD (ECAM).</li>"
 "<li>Phi công đọc và thao tác qua <b>HMI</b> (bảng EFIS, bảng ECAM, MCDU).</li>"
 "<li><b>CMC</b> ghi lỗi; <b>ACARS</b> đưa dữ liệu xuống mặt đất.</li></ol>"
 "<p>Bên dưới mọi tầng này là điện tử số: mã BCD sang 7 đoạn (Floyd), ROM tạo ký tự (Module 04), bộ giải mã và ghép kênh (Module 03), bus nối tiếp (Module 05).</p>",
 "<ol><li>Sensors and computers measure or compute data and send it over a <b>bus</b> (ARINC 429, AFDX) (Module 05).</li>"
 "<li>The <b>DMC/symbol generators</b> turn numbers into images, the <b>FWC</b> adds warnings, the <b>SDAC</b> adds system data.</li>"
 "<li>A <b>CRT or AMLCD</b> screen displays: PFD, ND (EFIS) and E/WD, SD (ECAM).</li>"
 "<li>The pilot reads and operates through the <b>HMI</b> (EFIS panel, ECAM panel, MCDU).</li>"
 "<li>The <b>CMC</b> logs faults; <b>ACARS</b> sends data to the ground.</li></ol>"
 "<p>Under every layer sits digital electronics: BCD to 7-segment codes (Floyd), the character generator ROM (Module 04), decoders and multiplexers (Module 03), serial buses (Module 05).</p>",
 "<p>Nếu cần nhớ MỘT điều từ module này: mọi thứ phi công nhìn thấy trên màn hình đều đã đi qua một chuỗi số hoá, và mỗi mắt xích có cách hỏng riêng. Khi gặp một bài toán chẩn đoán, hãy hỏi lần lượt: nguồn dữ liệu có đúng không (SSM của ARINC 429), bus có thông không, bộ tạo hình có tính đúng không, màn hình có hiển thị đúng không.</p>",
 "<p>If you remember ONE thing from this module: everything the pilot sees on a screen has gone through a chain of digitisation, and each link fails in its own way. In a diagnostic problem, ask in order: is the data source right (the ARINC 429 SSM), is the bus working, did the image generator compute correctly, is the screen displaying correctly.</p>",
 None),
],
]

def _build(lang):
    idx = 0 if lang == "vi" else 1
    parts = []
    for part in S:
        slides = []
        for (tv, te, bv, be, ev, ee, img) in part:
            d = {"title": tv if idx == 0 else te,
                 "body": bv if idx == 0 else be,
                 "explain": ev if idx == 0 else ee}
            if img: d["img"] = img
            slides.append(d)
        parts.append(slides)
    return parts

SLIDES = {"vi": _build("vi"), "en": _build("en")}
