# -*- coding: utf-8 -*-
"""Noi dung 6 slide/phan x 5 phan cho Module 04 - Computers & CPU (VI + EN). Target 40 slide (khop yeu voi Floyd)."""

SLIDES = {
  "vi": [
    # ===== Phan 1: Cau truc co ban cua he thong may tinh =====
    [
      {"title": "Mô hình IPO: khung tư duy cho MỌI hệ thống máy tính",
       "body": "<p>Input (nhập) → Process (xử lý) → Output (xuất) là khung tư duy áp dụng được cho mọi máy tính, từ máy tính bỏ túi tới FMGC. Trước khi phân tích một hệ thống mới, luôn xác định trước: đâu là input, đâu là process, đâu là output.</p>"},
      {"title": "Ba loại bus và vai trò riêng biệt",
       "body": "<table class='tt'><thead><tr><th>Bus</th><th>Mang gì</th><th>Chiều truyền</th></tr></thead><tbody>"
               "<tr><td>Address bus</td><td>địa chỉ ô nhớ/thiết bị</td><td>1 chiều (CPU→bộ nhớ)</td></tr>"
               "<tr><td>Data bus</td><td>dữ liệu thực tế</td><td>2 chiều</td></tr>"
               "<tr><td>Control bus</td><td>tín hiệu điều khiển/định thời</td><td>2 chiều</td></tr></tbody></table>"},
      {"title": "Ví dụ từng bước: địa chỉ lớn nhất trên bus 24-bit",
       "body": "<p>Bus địa chỉ 24-bit → 2²⁴ = 16.777.216 địa chỉ khả dĩ, từ 0 tới 16.777.215. Đổi giá trị lớn nhất sang hex (6 chữ số hex vì 24÷4=6): <b>FFFFFF</b>. (Khớp Tooley Ch.6 Q5: đã kiểm chứng bằng notebook 04.)</p>"},
      {"title": "Case study: đồng hồ buồng lái A320 (Figure 6.11, Tooley)",
       "body": "<p>Dao động thạch anh tạo xung UTC → vi xử lý xử lý dữ liệu thời gian → ROM lưu phần mềm điều khiển → RAM lưu dữ liệu tạm → bộ mã hoá dữ liệu nối tiếp gửi ra bus ARINC 429. Đây là ví dụ IPO + 3-bus hoàn chỉnh trong MỘT thiết bị thật.</p>"},
      {"title": "⚠️ Bẫy: nhầm 'bus' là một sợi dây đơn",
       "body": "<div class='callout warn'><p>Mỗi 'bus' thực chất là một BÓ nhiều đường dây song song (vd address bus 24-bit = 24 đường dây riêng biệt truyền đồng thời), không phải một đường dây duy nhất. Số đường dây quyết định trực tiếp số bit truyền được đồng thời.</p></div>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>Nếu bus địa chỉ chỉ có 8 đường dây, tối đa định vị được bao nhiêu ô nhớ khác nhau? (Gợi ý: 2⁸). So sánh với kết quả 24-bit ở slide trên để thấy rõ vì sao mở rộng thêm vài bit làm tăng vọt số ô nhớ định vị được.</p></div>"},
    ],
    # ===== Phan 2: Bo nho ban dan =====
    [
      {"title": "RAM vs ROM: khác biệt cốt lõi",
       "body": "<table class='tt'><thead><tr><th>Tiêu chí</th><th>RAM</th><th>ROM</th></tr></thead><tbody>"
               "<tr><td>Ghi được?</td><td>Có (đọc/ghi)</td><td>Không (chỉ đọc, trừ EPROM/Flash)</td></tr>"
               "<tr><td>Mất dữ liệu khi tắt điện?</td><td>Có (volatile)</td><td>Không (non-volatile)</td></tr></tbody></table>"},
      {"title": "EPROM, OTP EPROM, Mask ROM: phân biệt 3 loại dễ nhầm",
       "body": "<p>Mask ROM: ghi cố định từ khi sản xuất, không đổi được. OTP EPROM: ghi được đúng MỘT lần bởi người dùng. EPROM (UV-erasable): xoá bằng tia UV, ghi lại được NHIỀU lần: đây là loại duy nhất trong 3 loại 'xoá và lập trình lại được' (Tooley Ch.6 Q8).</p>"},
      {"title": "Ví dụ từng bước: cần bao nhiêu IC DRAM cho 32KB",
       "body": "<p>Mỗi IC 16K×4-bit chứa 16.384×4 = 65.536 bit = 8KB. Cần 32KB ÷ 8KB = <b>4 IC</b>. (Khớp Tooley Ch.6 Q13: đã verify bằng code trong notebook 04.)</p>"},
      {"title": "Cấu trúc ma trận hàng-cột và tín hiệu CAS/RAS",
       "body": "<p>Bộ nhớ bán dẫn tổ chức theo lưới hàng×cột để giảm số chân địa chỉ cần thiết. RAS (Row Address Select) chốt địa chỉ hàng, CAS (Column Address Select) chốt địa chỉ cột: gửi 2 lần thay vì gửi toàn bộ địa chỉ cùng lúc, tiết kiệm chân IC.</p>"},
      {"title": "⚠️ Bẫy: nhầm 'random access' với 'RAM' theo nghĩa thông thường",
       "body": "<div class='callout warn'><p>Về mặt kỹ thuật, ROM CŨNG là bộ nhớ 'truy cập ngẫu nhiên' (mọi ô nhớ truy xuất nhanh như nhau): chỉ là không ghi được. Thuật ngữ 'RAM' trong giao tiếp hàng ngày bị hiểu lệch thành 'bộ nhớ đọc/ghi', khác với định nghĩa kỹ thuật gốc của 'random access'.</p></div>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>Một hệ thống cần lưu phần mềm điều khiển KHÔNG được phép người dùng vô tình ghi đè: nên chọn RAM, ROM hay EPROM? Vì sao?</p></div>"},
    ],
    # ===== Phan 3: Kien truc ben trong CPU =====
    [
      {"title": "Bốn khối chức năng chính bên trong CPU",
       "body": "<ul><li>Thanh ghi (registers): lưu tạm địa chỉ/dữ liệu</li><li>ALU (Arithmetic Logic Unit): thực hiện phép toán số học/logic</li><li>Bộ giải mã lệnh (instruction decoder)</li><li>Khối điều khiển/định thời (control & timing)</li></ul>"},
      {"title": "Accumulator: thanh ghi được dùng nhiều nhất",
       "body": "<p>Accumulator vừa là nguồn (chứa toán hạng đầu vào) vừa là đích (chứa kết quả) cho phần lớn phép toán của CPU: đây là lý do nó được nhắc tới nhiều hơn hẳn các thanh ghi khác trong tài liệu kỹ thuật CPU.</p>"},
      {"title": "Program Counter (PC) và Stack Pointer (SP)",
       "body": "<p>PC luôn chứa địa chỉ của LỆNH KẾ TIẾP sẽ nạp: còn gọi là 'instruction pointer'. SP trỏ tới đỉnh hiện tại của ngăn xếp (stack), một vùng bộ nhớ RAM ngoài dùng lưu tạm địa chỉ trả về/giá trị thanh ghi khi gọi hàm hoặc xử lý ngắt.</p>"},
      {"title": "Bus buffer: vì sao data bus buffer phải là hai chiều",
       "body": "<p>CPU vừa cần ĐỌC dữ liệu từ bộ nhớ (chiều vào) vừa cần GHI dữ liệu ra bộ nhớ (chiều ra) qua cùng một data bus: bus buffer nối CPU với data bus do đó bắt buộc phải hỗ trợ cả 2 chiều (bidirectional), khác với address bus chỉ cần 1 chiều.</p>"},
      {"title": "⚠️ Bẫy: nhầm ALU với bộ giải mã lệnh",
       "body": "<div class='callout warn'><p>ALU thực hiện PHÉP TOÁN (cộng, trừ, AND, OR, đảo bit...) trên dữ liệu; bộ giải mã lệnh chỉ XÁC ĐỊNH lệnh vừa nạp là lệnh gì để điều khiển đúng khối chức năng: hai khối hoàn toàn khác nhiệm vụ dù đều nằm sát nhau trong sơ đồ CPU.</p></div>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>Một byte dữ liệu cần đảo bit (NOT): khối nào trong CPU thực hiện việc này: accumulator, ALU, hay instruction register?</p></div>"},
    ],
    # ===== Phan 4: Chu trinh lenh & thoi gian thuc thi =====
    [
      {"title": "Chu trình Fetch – Decode – Execute",
       "body": "<p>Fetch: CPU đọc mã lệnh từ ô nhớ được PC trỏ tới. Decode: bộ giải mã xác định lệnh là gì. Execute: ALU/khối chức năng liên quan thực hiện lệnh. Chu trình này lặp lại liên tục cho tới khi gặp lệnh HALT.</p>"},
      {"title": "T-state và chu kỳ máy (machine cycle)",
       "body": "<p>Một T-state = đúng 1 chu kỳ xung nhịp (clock). Một lệnh thường cần NHIỀU T-state, gộp thành các chu kỳ máy M0, M1, M2...: theo Tooley, M1 là chu kỳ nạp và giải mã lệnh (opcode fetch).</p>"},
      {"title": "Ví dụ từng bước: thời gian thực thi ở 50MHz, 11 T-state",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Thời gian thực thi</div><div class='pd-formula-math'>t = n_T × (1/f_clk)</div></div><p>Chu kỳ xung nhịp T = 1/50.000.000 = 20ns. Thời gian thực thi = 11 × 20ns = <b>220ns</b>. (Khớp Tooley Ch.7 Q15: đã verify bằng code trong notebook 04.)</p>"},
      {"title": "Ví dụ: theo dõi thanh ghi AL sau lệnh MOV AX, 07FEh",
       "body": "<p>AX (16-bit) gồm AH (byte cao) và AL (byte thấp). 07FEh tách thành AH=07h, AL=FEh. Đổi FEh sang nhị phân: <b>11111110</b>. (Khớp Tooley Ch.7 Q18.)</p>"},
      {"title": "⚠️ Bẫy: quên rằng 1 lệnh có thể cần NHIỀU chu kỳ máy khác nhau",
       "body": "<div class='callout warn'><p>Không phải mọi lệnh đều tốn cùng số T-state: một lệnh truy cập bộ nhớ (đọc/ghi RAM) luôn cần nhiều T-state hơn một lệnh chỉ thao tác trong thanh ghi nội bộ CPU, vì phải chờ thêm thời gian truyền tín hiệu qua address/data bus ra ngoài.</p></div>"},
      {"title": "Tự kiểm tra nhanh (không chấm điểm)",
       "body": "<div class='callout good'><p>Ở xung nhịp 20MHz, một lệnh cần 4 T-state mất bao lâu để thực thi? (Gợi ý: T=1/20MHz=50ns). Đối chiếu với notebook 04 sau khi tự tính.</p></div>"},
    ],
    # ===== Phan 5: Kien truc nang cao & ung dung hang khong =====
    [
      {"title": "Pipelining: chồng lấn các giai đoạn xử lý lệnh",
       "body": "<p>Thay vì fetch-decode-execute TUẦN TỰ từng lệnh một, pipelining cho phép CPU fetch lệnh kế tiếp trong khi đang decode lệnh hiện tại, và decode lệnh đó trong khi đang execute lệnh trước nữa: tăng thông lượng thực thi tổng thể (Tooley Ch.7 Q19).</p>"},
      {"title": "Kiến trúc ba bus: tách riêng bus lệnh và bus dữ liệu",
       "body": "<p>Một số vi xử lý hiệu năng cao dùng bus địa chỉ riêng, bus dữ liệu hệ thống riêng, và bộ nhớ lệnh (instruction ROM) tách biệt khỏi bộ nhớ dữ liệu: cho phép CPU đọc lệnh mới VÀ đọc/ghi dữ liệu CÙNG LÚC, không phải chờ nhau trên một bus chung duy nhất.</p>"},
      {"title": "Ngắt (interrupt) qua đường IRQ",
       "body": "<p>Một thiết bị ngoại vi cần CPU xử lý ngay (vd cảm biến phát hiện lỗi khẩn) sẽ tạo tín hiệu trên đường IRQ (Interrupt Request) thay vì chờ CPU tự hỏi thăm định kỳ (polling): CPU tạm dừng chương trình đang chạy, lưu trạng thái vào stack, xử lý ngắt, rồi khôi phục lại.</p>"},
      {"title": "Case study: Boeing 777 AIMS dùng 2 vi xử lý giống hệt nhau",
       "body": "<p>Hệ thống AIMS (Airplane Information Management System) trên Boeing 777 dùng hai vi xử lý giống hệt nhau chạy song song, liên tục so sánh kết quả: nếu kết quả hai bên khác nhau, hệ thống phát hiện lỗi ngay lập tức. Đây là ứng dụng thực tế của kiến trúc CPU dự phòng (redundancy) cho hệ thống avionics tới hạn.</p>"},
      {"title": "⚠️ Bẫy: nghĩ rằng pipelining luôn làm lệnh chạy nhanh hơn TỪNG LỆNH riêng lẻ",
       "body": "<div class='callout warn'><p>Pipelining tăng THÔNG LƯỢNG tổng thể (nhiều lệnh hoàn thành hơn trong cùng thời gian), nhưng thời gian hoàn thành của MỘT lệnh đơn lẻ (latency) không nhất thiết giảm: thậm chí có thể tăng nhẹ do chi phí quản lý pipeline. Đừng nhầm 'nhanh hơn' ở cấp độ hệ thống với 'nhanh hơn' ở cấp độ từng lệnh.</p></div>"},
      {"title": "Tự kiểm tra tổng kết module (không chấm điểm)",
       "body": "<div class='callout good'><p>Vì sao hệ thống avionics tới hạn (critical) thường KHÔNG dùng một vi xử lý đơn lẻ dù nó đủ mạnh về hiệu năng? Liên hệ lại với case study AIMS ở trên trước khi làm quiz cuối trang.</p></div>"},
    ],
  ],
  "en": [
    # ===== Part 1 =====
    [
      {"title": "The IPO model: a thinking framework for EVERY computer system",
       "body": "<p>Input → Process → Output is a framework that applies to every computer, from a pocket calculator to an FMGC. Before analysing any new system, always identify first: what is the input, what is the process, what is the output.</p>"},
      {"title": "Three buses and their distinct roles",
       "body": "<table class='tt'><thead><tr><th>Bus</th><th>Carries</th><th>Direction</th></tr></thead><tbody>"
               "<tr><td>Address bus</td><td>memory/device address</td><td>one-way (CPU→memory)</td></tr>"
               "<tr><td>Data bus</td><td>actual data</td><td>two-way</td></tr>"
               "<tr><td>Control bus</td><td>control/timing signals</td><td>two-way</td></tr></tbody></table>"},
      {"title": "Worked example: the largest address on a 24-bit bus",
       "body": "<p>A 24-bit address bus → 2²⁴ = 16,777,216 possible addresses, from 0 to 16,777,215. Converting the largest value to hex (6 hex digits since 24÷4=6): <b>FFFFFF</b>. (Matches Tooley Ch.6 Q5: verified in notebook 04.)</p>"},
      {"title": "Case study: the A320 cockpit clock (Figure 6.11, Tooley)",
       "body": "<p>A crystal oscillator generates the UTC time base → the microprocessor processes the time data → ROM stores the control software → RAM holds working data → a serial data encoder sends time out on the ARINC 429 bus. This is a complete real-world IPO + 3-bus example in ONE actual device.</p>"},
      {"title": "⚠️ Trap: thinking a 'bus' is a single wire",
       "body": "<div class='callout warn'><p>Each 'bus' is actually a BUNDLE of many parallel wires (e.g. a 24-bit address bus = 24 separate wires carrying signals simultaneously), not a single wire. The number of wires directly determines how many bits can be transferred at once.</p></div>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>If an address bus has only 8 wires, how many unique memory locations can it address? (Hint: 2⁸.) Compare with the 24-bit result above to see how a few extra bits dramatically increase addressable memory.</p></div>"},
    ],
    # ===== Part 2 =====
    [
      {"title": "RAM vs ROM: the core difference",
       "body": "<table class='tt'><thead><tr><th>Criterion</th><th>RAM</th><th>ROM</th></tr></thead><tbody>"
               "<tr><td>Writable?</td><td>Yes (read/write)</td><td>No (read-only, except EPROM/Flash)</td></tr>"
               "<tr><td>Loses data on power-off?</td><td>Yes (volatile)</td><td>No (non-volatile)</td></tr></tbody></table>"},
      {"title": "EPROM, OTP EPROM, Mask ROM: three easily confused types",
       "body": "<p>Mask ROM: fixed at manufacture, never changeable. OTP EPROM: user-writable exactly ONCE. EPROM (UV-erasable): erased with UV light, rewritable MANY times: the only one of the three that is truly 'erasable and reprogrammable' (Tooley Ch.6 Q8).</p>"},
      {"title": "Worked example: how many DRAM chips for 32KB",
       "body": "<p>Each 16K×4-bit chip holds 16,384×4 = 65,536 bits = 8KB. Required: 32KB ÷ 8KB = <b>4 chips</b>. (Matches Tooley Ch.6 Q13: verified by code in notebook 04.)</p>"},
      {"title": "Row-column matrix structure and the CAS/RAS signals",
       "body": "<p>Semiconductor memory is organised as a row×column grid to reduce the number of address pins needed. RAS (Row Address Select) latches the row address, CAS (Column Address Select) latches the column address: sent in two steps instead of the full address at once, saving IC pins.</p>"},
      {"title": "⚠️ Trap: confusing 'random access' with everyday 'RAM' usage",
       "body": "<div class='callout warn'><p>Technically, ROM is ALSO 'random-access' memory (every cell is accessed with equal ease): it simply cannot be written to. Everyday usage of the term 'RAM' has drifted to mean 'read/write memory', which differs from the original technical definition of 'random access'.</p></div>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>A system must store control software that users should NEVER be able to accidentally overwrite: should you choose RAM, ROM, or EPROM? Why?</p></div>"},
    ],
    # ===== Part 3 =====
    [
      {"title": "Four main functional blocks inside a CPU",
       "body": "<ul><li>Registers: temporary storage for addresses/data</li><li>ALU (Arithmetic Logic Unit): performs arithmetic/logic operations</li><li>Instruction decoder</li><li>Control & timing unit</li></ul>"},
      {"title": "The accumulator: the most heavily used register",
       "body": "<p>The accumulator is both a source (holding an input operand) and a destination (holding the result) for most CPU operations: this is why it is referenced far more often than any other register in CPU technical documentation.</p>"},
      {"title": "Program Counter (PC) and Stack Pointer (SP)",
       "body": "<p>The PC always holds the address of the NEXT instruction to be fetched: also called the 'instruction pointer'. The SP points to the current top of the stack, an area of external RAM used to temporarily store return addresses/register values during function calls or interrupt handling.</p>"},
      {"title": "Bus buffers: why the data bus buffer must be bidirectional",
       "body": "<p>The CPU needs to both READ data from memory (inbound) and WRITE data to memory (outbound) through the same data bus: the bus buffer connecting the CPU to the data bus must therefore support both directions (bidirectional), unlike the address bus which only needs one direction.</p>"},
      {"title": "⚠️ Trap: confusing the ALU with the instruction decoder",
       "body": "<div class='callout warn'><p>The ALU performs OPERATIONS (add, subtract, AND, OR, invert...) on data; the instruction decoder only DETERMINES what instruction was just fetched so it can direct the correct functional block: two completely different jobs despite sitting close together on a CPU block diagram.</p></div>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>A byte of data needs to be inverted (NOT): which CPU block performs this: the accumulator, the ALU, or the instruction register?</p></div>"},
    ],
    # ===== Part 4 =====
    [
      {"title": "The Fetch – Decode – Execute cycle",
       "body": "<p>Fetch: the CPU reads the opcode from the memory location the PC points to. Decode: the decoder determines what the instruction is. Execute: the ALU/relevant functional block carries it out. This cycle repeats continuously until a HALT instruction is met.</p>"},
      {"title": "T-states and machine cycles",
       "body": "<p>One T-state = exactly one clock cycle. An instruction usually needs SEVERAL T-states, grouped into machine cycles M0, M1, M2...: per Tooley, M1 is the opcode fetch-and-decode cycle.</p>"},
      {"title": "Worked example: execution time at 50MHz, 11 T-states",
       "body": "<div class='pd-formula'><div class='pd-formula-label'>Execution time</div><div class='pd-formula-math'>t = n_T × (1/f_clk)</div></div><p>Clock period T = 1/50,000,000 = 20ns. Execution time = 11 × 20ns = <b>220ns</b>. (Matches Tooley Ch.7 Q15: verified by code in notebook 04.)</p>"},
      {"title": "Example: tracing the AL register after MOV AX, 07FEh",
       "body": "<p>AX (16-bit) consists of AH (high byte) and AL (low byte). 07FEh splits into AH=07h, AL=FEh. Converting FEh to binary: <b>11111110</b>. (Matches Tooley Ch.7 Q18.)</p>"},
      {"title": "⚠️ Trap: forgetting that instructions can need DIFFERENT numbers of machine cycles",
       "body": "<div class='callout warn'><p>Not every instruction costs the same number of T-states: a memory-access instruction (reading/writing RAM) always needs more T-states than one operating purely on internal CPU registers, because it must wait for extra signal propagation time over the external address/data bus.</p></div>"},
      {"title": "Quick self-check (ungraded)",
       "body": "<div class='callout good'><p>At a 20MHz clock, how long does an instruction requiring 4 T-states take to execute? (Hint: T=1/20MHz=50ns.) Check against notebook 04 after computing it yourself.</p></div>"},
    ],
    # ===== Part 5 =====
    [
      {"title": "Pipelining: overlapping instruction processing stages",
       "body": "<p>Instead of fetching-decoding-executing instructions strictly SEQUENTIALLY, pipelining lets the CPU fetch the next instruction while decoding the current one, and decode that one while executing the instruction before it: increasing overall execution throughput (Tooley Ch.7 Q19).</p>"},
      {"title": "Three-bus architecture: separating the instruction and data buses",
       "body": "<p>Some high-performance processors use a separate address bus, a separate system data bus, and instruction memory (instruction ROM) kept apart from data memory: letting the CPU fetch a new instruction AND read/write data AT THE SAME TIME, instead of both waiting on one shared bus.</p>"},
      {"title": "Interrupts via the IRQ line",
       "body": "<p>A peripheral device needing immediate CPU attention (e.g. a sensor detecting an urgent fault) raises a signal on the IRQ (Interrupt Request) line instead of waiting for the CPU to periodically check in (polling): the CPU pauses its current program, saves state to the stack, services the interrupt, then resumes.</p>"},
      {"title": "Case study: the Boeing 777 AIMS uses two identical microprocessors",
       "body": "<p>The AIMS (Airplane Information Management System) on the Boeing 777 runs two identical microprocessors in parallel, continuously comparing their results: if the two disagree, the system detects the fault immediately. This is a real application of redundant CPU architecture for a critical avionics system.</p>"},
      {"title": "⚠️ Trap: assuming pipelining always makes EACH instruction run faster",
       "body": "<div class='callout warn'><p>Pipelining increases overall THROUGHPUT (more instructions complete per unit time), but the completion time of any ONE individual instruction (latency) is not necessarily reduced: it can even increase slightly due to pipeline management overhead. Don't confuse system-level 'faster' with per-instruction 'faster'.</p></div>"},
      {"title": "Final module self-check (ungraded)",
       "body": "<div class='callout good'><p>Why do critical avionics systems typically NOT rely on a single microprocessor, even one powerful enough on its own? Relate your answer back to the AIMS case study above before taking the quiz at the bottom of the page.</p></div>"},
    ],
  ],
}
