# -*- coding: utf-8 -*-
"""Phan mo rong module 04: he may tinh, bo xu ly va VI DIEU KHIEN (CO5 cua de cuong). Nguon: Floyd Ch.14 (PDF tr.803-854 = trang in 802-853).
Cau goc: Floyd Ch.14 Dung/Sai (15) va Self-Test (15), khoa doc tu van ban cua sach (PDF tr.854); hai khoa in SAI so voi chinh van ban (Dung/Sai 12, Self-Test 13) nen dung dap an DUNG va ghi ro.
Tu luan goc: Floyd 14-8 Checkup (6) va 14-9 Checkup (3) co dap an in. Cau bo sung: 5 ho cau so (dia chi, PWM, bo dinh thoi, bo dem tran, trang thai cho) tinh bang build/numlib/mcu.py, verify_m04_mcu.py tinh lai doc lap.
Ghi ra data/qsrc/m04_mcu.json (goc + bo sung) va m04_mcu_ess.json (tu luan)."""
import os, sys, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'numlib'))
from qdsl import Bank, OUT, opt
import mcu as F
def topics():
    t = {}
    for f in glob.glob(os.path.join(OUT, 'm04*.json')):
        if f.endswith(('m04_mcu.json', 'm04_mcu_ess.json')): continue
        for it in json.load(open(f, encoding='utf-8')): t[it['topic_id']] = (it['topic']['vi'], it['topic']['en'])
    t['mcu'] = ('Vi điều khiển, hệ nhúng và SoC', 'Microcontrollers, embedded systems and SoC')
    t['prog'] = ('Hệ điều hành và lập trình', 'Operating systems and programming')
    return t
B = Bank(topics()); META = []
TFO = [('Đúng', 'True'), ('Sai', 'False')]
PG = 853      # trang in cua khoa Ch.14 (PDF tr.854)
EVD = []      # (nhan, [cum tu bang chung trong van ban Floyd])
def tf(n, tid, lv, vi, en, key, xv, xe, ev=(), printed=None):
    ans = key if printed is None else key; pk = printed or key
    sv = f'Floyd Ch.14 · Đúng/Sai {n} (khoá tr.{PG})'; se = f'Floyd Ch.14 · True/False {n} (key p.{PG})'
    if printed: sv = f'Floyd Ch.14 · Đúng/Sai {n} (khoá in ({pk}), đúng ({ans}); tr.{PG})'; se = f'Floyd Ch.14 · True/False {n} (printed key ({pk}), correct ({ans}); p.{PG})'
    it = B._item('tf', tid, lv, 'goc', vi, en, TFO, 0 if ans == 'T' else 1, xv, xe, sv, se); B.goc.append(it)
    META.append(dict(kind='tf', n=n, printed=pk, ans=ans, ev=list(ev), q=en))
def st(n, tid, lv, vi, en, opts, key, xv, xe, ev=(), printed=None):
    ans = key; pk = printed or key; assert len(opts) in (3, 4) and ans in 'abcd'
    sv = f'Floyd Ch.14 · Self-Test {n} (khoá tr.{PG})'; se = f'Floyd Ch.14 · Self-Test {n} (key p.{PG})'
    if printed: sv = f'Floyd Ch.14 · Self-Test {n} (khoá in ({pk}), đúng ({ans}); tr.{PG})'; se = f'Floyd Ch.14 · Self-Test {n} (printed key ({pk}), correct ({ans}); p.{PG})'
    it = B._item('mcq', tid, lv, 'goc', vi, en, opts, 'abcd'.index(ans), xv, xe, sv, se); B.goc.append(it)
    META.append(dict(kind='st', n=n, printed=pk, ans=ans, ev=list(ev), q=en, opts=[opt(o)[1] for o in opts]))

# ---------------- Floyd Ch.14 Dung/Sai (khoa in: 1T 2F 3T 4T 5T 6T 7F 8F 9T 10T 11T 12F 13F 14T 15F) ----------------
tf(1, 'cpu', 1, 'CPU gồm ALU, bộ giải mã lệnh và khối định thời và điều khiển.', 'A CPU consists of an ALU, an instruction decoder, and a timing and control unit.', 'T', 'Ba khối chức năng của CPU là ALU, bộ giải mã lệnh và khối định thời và điều khiển (Floyd 14-1).', 'The three functional units of a CPU are the ALU, the instruction decoder and the timing and control unit (Floyd 14-1).', ev=['instruction decoder'])
tf(2, 'structure', 1, 'CPU là viết tắt của "computer peripheral unit".', 'CPU stands for computer peripheral unit.', 'F', 'CPU là "central processing unit" (khối xử lý trung tâm).', 'CPU stands for central processing unit.', ev=['central processing unit'])
tf(3, 'memory', 1, 'Bộ nhớ là các linh kiện bán dẫn lưu thông tin dưới dạng điện tử và giao tiếp với hệ máy tính qua các bus.', 'Memory devices are semiconductor devices that store information electronically and interface with the computer system through buses.', 'T', 'Bộ nhớ nối với CPU qua bus địa chỉ, dữ liệu và điều khiển (Floyd 14-1).', 'Memory connects to the CPU over the address, data and control buses (Floyd 14-1).', ev=['semiconductor'])
tf(4, 'prog', 1, 'Hệ điều hành của máy tính là một thành phần phần mềm.', 'The operating system of a computer is a software component.', 'T', 'Hệ điều hành là phần mềm hệ thống, một trong hai nhóm phần mềm chạy trong máy tính (Floyd 14-6).', 'The operating system is system software, one of the two groups of software that run in a computer (Floyd 14-6).', ev=['operating system'])
tf(5, 'cpu', 1, 'ALU là một phần tử then chốt của bộ vi xử lý.', 'The ALU is a key element in a microprocessor.', 'T', 'ALU thực hiện phép toán số học và logic, là một trong các phần tử cơ bản của vi xử lý (Floyd 14-3).', 'The ALU performs the arithmetic and logic operations and is one of the basic elements of a microprocessor (Floyd 14-3).', ev=['arithmetic logic unit'])
tf(6, 'structure', 1, 'Bộ vi xử lý thường có ba loại bus: địa chỉ, dữ liệu và điều khiển.', 'Microprocessors generally have three types of buses: address, data, and control.', 'T', 'Ba bus của vi xử lý là bus địa chỉ, bus dữ liệu và bus điều khiển (Floyd 14-3).', 'The three microprocessor buses are the address, data and control buses (Floyd 14-3).', ev=['address bus'])
tf(7, 'memory', 1, 'Bộ nhớ BIOS chứa mã bậc cao riêng của từng chương trình ứng dụng.', 'The BIOS memory contains program-specific high-level code.', 'F', 'BIOS là phần mềm cơ sở lưu trong bộ nhớ không khả biến để khởi động và điều khiển phần cứng cấp thấp, không phải mã bậc cao của từng chương trình.', 'The BIOS is basic firmware held in nonvolatile memory for start-up and low-level hardware control, not high-level code specific to a program.', ev=['BIOS'])
tf(8, 'cpu', 1, 'Bộ xử lý đa lõi có một bộ xử lý và nhiều bộ nhớ.', 'A multicore processor has one processor and more than one memory.', 'F', 'Bộ xử lý đa lõi có nhiều lõi xử lý trong một vi mạch, không phải nhiều bộ nhớ.', 'A multicore processor has several processor cores in one chip, not several memories.', ev=['multicore'])
tf(9, 'cpu', 1, 'Pipelining cho phép máy tính chạy chương trình nhanh hơn.', 'Pipelining allows a computer to execute a program faster.', 'T', 'Pipelining chồng lấn các giai đoạn của nhiều lệnh nên thông lượng tăng (Floyd 14-3).', 'Pipelining overlaps the stages of several instructions so throughput rises (Floyd 14-3).', ev=['pipelining'])
tf(10, 'prog', 1, 'Ba mức ngôn ngữ lập trình máy tính là ngôn ngữ máy, hợp ngữ và ngôn ngữ bậc cao.', 'Three levels of computer programming languages are machine, assembly, and high level.', 'T', 'Floyd 14-7 phân ba mức: ngôn ngữ máy, hợp ngữ và ngôn ngữ bậc cao.', 'Floyd 14-7 distinguishes three levels: machine language, assembly language and high-level language.', ev=['assembly'])
tf(11, 'structure', 1, 'DMA là viết tắt của "direct memory access" (truy cập bộ nhớ trực tiếp).', 'DMA stands for direct memory access.', 'T', 'DMA = direct memory access (Floyd 14-5).', 'DMA = direct memory access (Floyd 14-5).', ev=['direct memory access'])
tf(12, 'structure', 2, 'Các tín hiệu của một thao tác DMA là yêu cầu bus (bus request), cấp bus (bus grant) và xác nhận cấp bus (bus grant acknowledge).', 'The signals associated with a DMA operation are bus request, bus grant, and bus grant acknowledge.', 'T',
   'Bộ điều khiển DMA là một bus master dùng thao tác yêu cầu bus với ba tín hiệu BR, BG và BGACK (Floyd 14-5, Hình 14–25). Khoá in của sách ghi (F) mâu thuẫn với chính văn bản; site dùng đáp án đúng theo văn bản.',
   'A DMA controller is a bus master that uses the bus request operation with the three signals BR, BG and BGACK (Floyd 14-5, Figure 14–25). The book\'s printed key says (F), which contradicts its own text; the site uses the answer that follows the text.', ev=['bus grant acknowledge'], printed='F')
tf(13, 'mcu', 1, 'Vi xử lý (microprocessor) và vi điều khiển (microcontroller) là hai tên gọi của cùng một thứ.', 'Microprocessor and microcontroller are different names for the same thing.', 'F', 'Vi điều khiển gộp lõi vi xử lý, bộ nhớ và các ngoại vi trong một vỏ; vi xử lý chỉ là CPU (Floyd 14-8).', 'A microcontroller combines a processor core, memory and peripherals in one package; a microprocessor is only the CPU (Floyd 14-8).', ev=['processor core, memory'])
tf(14, 'mcu', 1, 'Một số ví dụ về ngoại vi của vi điều khiển là GPIO, ADC và bộ mã hoá vuông góc (quadrature encoder).', 'Some examples of microcontroller peripherals are GPIOs, ADCs, and quadrature encoders.', 'T', 'Floyd 14-8 liệt kê GPIO, bộ điều khiển truyền thông, bộ định thời, bộ mã hoá vuông góc, PWM, bộ điều khiển bộ nhớ ngoài, ADC và DAC.', 'Floyd 14-8 lists GPIO, communication controllers, timers, quadrature encoders, PWMs, external memory controllers, ADCs and DACs.', ev=['quadrature encoder'])
tf(15, 'mcu', 1, 'SoC là viết tắt của "sequential output computer".', 'SoC stands for sequential output computer.', 'F', 'SoC = system on chip: mạch tích hợp gộp mọi thành phần của một hệ máy tính trên một chip (Floyd 14-9).', 'SoC = system on chip: an integrated circuit that combines all components of a computer system on one chip (Floyd 14-9).', ev=['system on chip'])

# ---------------- Floyd Ch.14 Self-Test (khoa in: 1d 2a 3b 4b 5d 6c 7a 8d 9c 10c 11c 12d 13c 14d 15a) ----------------
st(1, 'structure', 1, 'Khối nào sau đây là thiết bị ngoại vi của máy tính?', 'Which of the following is a peripheral unit of a computer?', [('khối số học và logic', 'Arithmetic and logic unit'), ('khối điều khiển', 'Control unit'), ('khối bộ nhớ', 'Memory unit'), ('bàn phím', 'Keyboard')], 'd',
   'ALU và khối điều khiển thuộc CPU, bộ nhớ là một khối chính của máy tính; bàn phím là thiết bị vào/ra, tức ngoại vi.', 'The ALU and control unit are in the CPU and memory is a main block of the computer; the keyboard is an input/output device, i.e. a peripheral.', ev=['peripheral'])
st(2, 'cpu', 2, 'Hoạt động của khối định thời và điều khiển trong vi xử lý chịu ảnh hưởng của:', 'The operation of the timing and control unit in a microprocessor is affected by', [('bộ giải mã lệnh', 'the instruction decoder'), ('thanh ghi tích luỹ', 'the accumulator'), ('khối số học và logic', 'the arithmetic logic unit'), ('dãy thanh ghi', 'the register array')], 'a',
   'Bộ giải mã lệnh cho khối định thời và điều khiển biết lệnh cần thực hiện nên quyết định chuỗi tín hiệu điều khiển.', 'The instruction decoder tells the timing and control unit which instruction to carry out, so it determines the sequence of control signals.', ev=['instruction decoder'])
st(3, 'structure', 1, 'Bus địa chỉ 10 bit hỗ trợ:', 'A 10-bit address bus supports', [('1 000 000 địa chỉ bộ nhớ', '1,000,000 memory addresses'), ('1024 địa chỉ bộ nhớ', '1024 memory addresses'), ('100 địa chỉ bộ nhớ', '100 memory addresses'), ('1000 địa chỉ bộ nhớ', '1000 memory addresses')], 'b',
   'n bit địa chỉ cho 2ⁿ vị trí: 2¹⁰ = 1024.', 'n address bits give 2ⁿ locations: 2¹⁰ = 1024.')
st(4, 'structure', 1, 'Bus dùng để truyền thông tin cả đến lẫn đi từ vi xử lý là:', 'A bus that is used to transfer information both to and from the microprocessor is the', [('bus địa chỉ', 'address bus'), ('bus dữ liệu', 'data bus'), ('cả hai bus trên', 'both of the above'), ('không bus nào trong hai bus trên', 'none of the above')], 'b',
   'Bus dữ liệu hai chiều; bus địa chỉ một chiều, từ CPU ra.', 'The data bus is bidirectional; the address bus is one-way, out of the CPU.', ev=['data bus'])
st(5, 'structure', 1, 'Bus hệ thống (system bus) gồm:', 'A system bus is composed of', [('bus địa chỉ', 'address bus'), ('bus dữ liệu', 'data bus'), ('bus điều khiển (sách in "system bus")', 'control bus (the book prints "system bus")'), ('các câu (a), (b) và (c)', 'answers (a), (b), and (c)')], 'd',
   'Bus hệ thống gồm bus địa chỉ, bus dữ liệu và bus điều khiển. Ở phương án (c) sách in "system bus" (có lẽ là lỗi in của "control bus"); khoá d vẫn đúng.', 'The system bus is made up of the address, data and control buses. Option (c) is printed "system bus" in the book (probably a misprint of "control bus"); key (d) still stands.', ev=['control bus'])
st(6, 'structure', 1, 'Trạng thái đầu ra thứ ba của linh kiện ba trạng thái (tri-state) gọi là:', 'The third output state of a tri-state device is called', [('logic 0', 'logic 0'), ('logic 1', 'logic 1'), ('trạng thái trở kháng cao (high-Z)', 'high-Z state'), ('không phải các trạng thái trên', 'none of the above')], 'c',
   'Ngoài mức 0 và 1, đầu ra ba trạng thái có trạng thái trở kháng cao (high-Z): như bị ngắt khỏi bus.', 'Besides 0 and 1 a tri-state output has the high-impedance (high-Z) state: it is effectively disconnected from the bus.', ev=['high-Z'])
st(7, 'cycle', 1, 'Trong chu kỳ nạp lệnh (fetch) của bộ xử lý:', 'During the fetch cycle of a processor', [('lệnh được đọc từ bộ nhớ', 'instructions are read from the memory'), ('dữ liệu được lưu làm kết quả', 'data is stored as a result'), ('dữ liệu được xử lý trong ALU', 'the data is processed in the ALU'), ('các lệnh được thực hiện trong bộ xử lý', 'the instructions are executed in the processor')], 'a',
   'Chu kỳ nạp lệnh đọc lệnh từ bộ nhớ; thực hiện lệnh là chu kỳ execute.', 'The fetch cycle reads the instruction from memory; carrying it out is the execute cycle.', ev=['fetch'])
st(8, 'cpu', 1, 'Vai trò của CPU là:', 'The role of the CPU is to', [('điều khiển phần cứng hệ thống', 'control the system hardware'), ('hỗ trợ phần cứng cho hệ điều hành', 'provide hardware support to the operating system'), ('thực thi các chương trình ứng dụng', 'execute application programs'), ('các câu (a), (b) và (c)', 'answers (a), (b), and (c)')], 'd',
   'CPU điều khiển phần cứng, hỗ trợ hệ điều hành và chạy chương trình ứng dụng: cả ba.', 'The CPU controls the hardware, supports the operating system and runs application programs: all three.', ev=['central processing unit'])
st(9, 'prog', 1, 'Ngôn ngữ bậc cao được chuyển thành ngôn ngữ máy nhờ:', 'High level languages are converted to machine level language through', [('trình hợp dịch (assembler)', 'an assembler'), ('trình gỡ lỗi (debugger)', 'a debugger'), ('trình biên dịch (compiler)', 'a compiler'), ('trình dịch (translator)', 'a translator')], 'c',
   'Trình biên dịch dịch mã bậc cao thành mã máy; trình hợp dịch chuyển hợp ngữ thành mã máy.', 'A compiler translates high-level code into machine code; an assembler turns assembly language into machine code.', ev=['compiler'])
st(10, 'prog', 1, 'Chương trình máy tính là một danh sách các:', 'A computer program is a list of', [('địa chỉ bộ nhớ chứa dữ liệu dùng trong một phép toán', 'memory addresses that contain data to be used in an operation'), ('địa chỉ chứa các lệnh dùng trong một phép toán', 'addresses that contain instructions to be used in an operation'), ('lệnh được sắp xếp để đạt một kết quả xác định', 'instructions arranged to achieve a specific result')], 'c',
   'Chương trình là một dãy lệnh được sắp xếp để đạt kết quả nhất định (Floyd 14-7).', 'A program is a list of instructions arranged to achieve a specific result (Floyd 14-7).', ev=['program'])
st(11, 'prog', 1, 'Loại lệnh hợp ngữ làm thay đổi hướng chạy của chương trình gọi là:', 'A type of assembly language instruction that alters the course of the program is called a', [('lặp (loop)', 'loop'), ('nhảy (jump)', 'jump'), ('cả hai câu trên', 'both of the above'), ('không câu nào trong hai câu trên', 'none of the above')], 'c',
   'Cả lệnh lặp lẫn lệnh nhảy đều làm thay đổi luồng chạy chương trình (Floyd 14-7).', 'Both loop and jump instructions change the course of the program (Floyd 14-7).', ev=['jump'])
st(12, 'cycle', 2, 'Trạng thái chờ (wait state):', 'A wait state', [('kết thúc một chu kỳ bus', 'terminates a bus cycle'), ('dừng xung nhịp bộ xử lý trong một chu kỳ', 'halts the processor clock for one period'), ('đưa vi xử lý vào chế độ tiết kiệm điện', 'places the microprocessor in a low-power mode'), ('làm chậm việc hoàn thành chu kỳ bus thêm một chu kỳ xung nhịp', 'delays completion of a bus cycle by one processor clock')], 'd',
   'Trạng thái chờ là độ trễ trên bus hệ thống bằng một chu kỳ xung nhịp của bộ xử lý, dùng khi bộ nhớ hoặc thiết bị chậm (Floyd, Từ khoá).', 'A wait state is a system-bus delay equal to one processor clock cycle, used when memory or a device is slow (Floyd, Key Terms).', ev=['wait state'])
st(13, 'structure', 2, 'Yêu cầu bus (bus request) khác với ngắt (interrupt) ở chỗ:', 'A bus request differs from an interrupt in that', [('ngắt cần một bus master bên ngoài để hoàn tất thao tác', 'an interrupt requires an external bus master to complete the operation'), ('yêu cầu bus sẽ cắt ngang chu kỳ lệnh đang thực hiện', 'a bus request will interrupt a current instruction cycle'), ('ngắt không thể bị che (mask)', 'an interrupt cannot be masked'), ('yêu cầu bus không cần bộ xử lý đáp ứng', 'a bus request does not involve a response from the processor')], 'b',
   'Floyd 14-5: thao tác yêu cầu bus KHÔNG đợi hoàn tất chu kỳ lệnh hiện tại, còn ngắt và ngoại lệ cho bộ xử lý hoàn tất lệnh rồi mới xử lý. Bộ xử lý phải đáp ứng bằng tín hiệu BG, và sách không nói ngắt "không thể che". Khoá in của sách ghi (c); site dùng (b) theo văn bản.',
   'Floyd 14-5: a bus request operation does NOT wait for the current instruction cycle to finish, whereas interrupts and exceptions let the processor complete the instruction first. The processor must respond with the BG signal, and the book never says an interrupt "cannot be masked". The book prints key (c); the site uses (b) from the text.', ev=['do not complete the current instruction cycle'], printed='c')
st(14, 'prog', 1, 'Một hệ điều hành:', 'An operating system', [('lập lịch và cấp phát tài nguyên hệ thống', 'schedules and allocates system resources'), ('bảo vệ các tiến trình và tài nguyên hệ thống', 'protects the system processes and resources'), ('cung cấp các dịch vụ hệ thống', 'provides system services'), ('các câu (a), (b) và (c)', 'answers (a), (b), and (c)')], 'd',
   'Hệ điều hành lập lịch và cấp phát tài nguyên, bảo vệ tiến trình và cung cấp dịch vụ hệ thống: cả ba (Floyd 14-6).', 'An operating system schedules and allocates resources, protects processes and provides system services: all three (Floyd 14-6).', ev=['operating system'])
st(15, 'prog', 1, 'Từ gợi nhớ (mnemonic) hay mã lệnh (op-code) là một phần của:', 'Mnemonics or op-codes are a part of', [('ngôn ngữ cấp hợp ngữ', 'assembly level languages'), ('ngôn ngữ cấp máy', 'machine level languages'), ('ngôn ngữ bậc cao', 'high level languages'), ('không loại nào ở trên', 'none of the above')], 'a',
   'Hợp ngữ dùng từ gợi nhớ (ví dụ MOV, ADD) thay cho mã nhị phân của lệnh.', 'Assembly language uses mnemonics (e.g. MOV, ADD) in place of the binary code of an instruction.', ev=['mnemonic'])

# ---------------- cau bo sung (tinh bang mcu.py) ----------------
X = B.X
def n_(v):                        # so nguyen lon: (vi, en) co dau phan cach nghin
    return (f'{v:,}'.replace(',', ' '), f'{v:,}') if v >= 1000 else str(v)
def g_(v): return f'{v:g}'
def meta(fam, args, ans, q): META.append(dict(kind='gen', fam=fam, args=list(args), ans=ans, q=q))
for nb in (10, 16, 20, 32):
    a = F.addresses(nb); ops = [n_(a), n_(a // 2), n_(2 * nb), n_(a * 2)]
    X('structure', 1 if nb <= 16 else 2, f'Một bộ xử lý có bus địa chỉ {nb} bit. Số vị trí bộ nhớ khác nhau mà nó có thể đánh địa chỉ là:', f'A processor has a {nb}-bit address bus. The number of different memory locations it can address is:', ops, 0,
      f'$2^{{{nb}}}$ = {n_(a)[0] if isinstance(n_(a), tuple) else n_(a)} vị trí.', f'$2^{{{nb}}}$ = {n_(a)[1] if isinstance(n_(a), tuple) else n_(a)} locations.', 'Không gian địa chỉ', 'Address space')
    meta('addr', [nb], a, f'{nb}-bit address bus')
for vs, th, T in ((12, 2, 8), (5, 3, 4), (24, 1, 5), (9, 6, 10)):
    v = F.pwm_avg(vs, th, T); d = F.duty(th, T) * 100
    X('mcu', 2, f'Một bộ điều chế độ rộng xung (PWM) cấp xung biên độ {vs} V, mức cao kéo dài {th} ms trong chu kỳ {T} ms cho một động cơ. Điện áp trung bình đặt lên động cơ là:', f'A pulse width modulator supplies a {vs} V pulse train, HIGH for {th} ms in each {T} ms period, to a motor. The average voltage applied to the motor is:',
      [f'{g_(v)} V', f'{g_(vs - v)} V', f'{g_(vs / 2)} V', f'{g_(vs * T / th)} V'] if len({v, vs - v, vs / 2, vs * T / th}) == 4 else [f'{g_(v)} V', f'{g_(vs - v)} V', f'{g_(vs / 2 + 1)} V', f'{g_(vs * T / th)} V'], 0,
      f'Chu kỳ làm việc $D={th}/{T}$ = {g_(d)} %; $V_{{tb}}=D\\times V_s={g_(d / 100)}\\times{vs}$ = {g_(v)} V (Floyd 14-8: đổi chu kỳ làm việc để chỉnh tốc độ động cơ).', f'Duty cycle $D={th}/{T}$ = {g_(d)} %; $V_{{avg}}=D\\times V_s={g_(d / 100)}\\times{vs}$ = {g_(v)} V (Floyd 14-8: the duty cycle sets the motor speed).', 'Điện áp trung bình PWM', 'Average PWM voltage')
    meta('pwm', [vs, th, T], v, f'PWM {vs} V {th}/{T}')
for th, T in ((2, 8), (3, 12), (5, 20), (6, 10)):
    d = F.duty(th, T) * 100
    X('mcu', 1, f'Một tín hiệu PWM ở mức cao {th} ms trong mỗi chu kỳ {T} ms. Chu kỳ làm việc (duty cycle) là:', f'A PWM signal is HIGH for {th} ms in every {T} ms period. Its duty cycle is:', [f'{g_(d)} %', f'{g_(100 - d)} %', f'{g_(T / th)} %', f'{g_(d / 2)} %'] if len({d, 100 - d, T / th, d / 2}) == 4 else [f'{g_(d)} %', f'{g_(100 - d)} %', f'{g_(d / 4)} %', f'{g_(d + 10)} %'], 0,
      f'$D=t_{{cao}}/T={th}/{T}$ = {g_(d)} %.', f'$D=t_{{high}}/T={th}/{T}$ = {g_(d)} %.', 'Chu kỳ làm việc', 'Duty cycle')
    meta('duty', [th, T], d, f'duty {th}/{T}')
for fm_, ps, cnt in ((16, 8, 2000), (8, 64, 1250), (1, 1, 1000), (20, 256, 78125)):
    t = F.timer_s(fm_ * 1e6, ps, cnt) * 1000        # ms
    X('mcu', 2, f'Một bộ định thời của vi điều khiển chạy xung nhịp {fm_} MHz, chia trước (prescaler) {ps}, và đếm {n_(cnt)[0] if isinstance(n_(cnt), tuple) else n_(cnt)} xung đã chia. Khoảng thời gian đo được là:', f'A microcontroller timer runs from a {fm_} MHz clock with a prescaler of {ps} and counts {n_(cnt)[1] if isinstance(n_(cnt), tuple) else n_(cnt)} prescaled pulses. The interval it measures is:',
      [f'{g_(t)} ms', f'{g_(t * 1000)} ms', f'{g_(t / 1000)} ms', f'{g_(t * 8 if ps != 8 else t * 4)} ms'], 0,
      f'$t=\\text{{đếm}}\\times\\text{{prescaler}}/f_{{clk}}={cnt}\\times{ps}/({fm_}\\times10^6)$ = {g_(t)} ms.', f'$t=\\text{{count}}\\times\\text{{prescaler}}/f_{{clk}}={cnt}\\times{ps}/({fm_}\\times10^6)$ = {g_(t)} ms.', 'Khoảng thời gian bộ định thời', 'Timer interval')
    meta('timer', [fm_, ps, cnt], t, f'timer {fm_} {ps} {cnt}')
for bits, rate, unit in ((16, 1000, 's'), (32, 1e6, 'min'), (32, 1000, 'day'), (16, 100, 's')):
    s = F.rollover_s(bits, rate); div = {'s': 1, 'min': 60, 'day': 86400}[unit]; val = s / div; un_vi = {'s': 'giây', 'min': 'phút', 'day': 'ngày'}[unit]; un_en = {'s': 's', 'min': 'min', 'day': 'days'}[unit]
    fx = lambda v: (f'{round(v, 2):.2f}').rstrip('0').rstrip('.')
    ops = [f'{fx(val)} {un_en}', f'{fx(val * 1000)} {un_en}', f'{fx(val / 1000)} {un_en}', f'{fx(val / 2)} {un_en}']
    X('mcu', 3, f'Bộ đếm {bits} bit của bộ mã hoá vuông góc đếm {rate:g} xung mỗi giây. Thời gian để nó đếm đủ 2^{bits} xung và tràn là:', f'The {bits}-bit counter of a quadrature encoder counts {rate:g} pulses per second. The time for it to count 2^{bits} pulses and overflow is:',
      [(o.replace(un_en, un_vi) if un_en != un_vi else o, o) for o in ops], 0,
      f'$t=2^{{{bits}}}/{rate:g}$ = {s:.10g} s = {fx(val)} {un_vi}. (Floyd: bộ đếm của bộ mã hoá vuông góc thường rộng 32 bit trở lên để tránh tràn.)', f'$t=2^{{{bits}}}/{rate:g}$ = {s:.10g} s = {fx(val)} {un_en}. (Floyd: quadrature-encoder counters are typically 32 bits or wider to avoid overflow.)', 'Thời gian tràn bộ đếm', 'Counter overflow time')
    meta('rollover', [bits, rate], s, f'rollover {bits} {rate}')
for f_mhz, base, w in ((50, 3, 2), (100, 4, 1), (25, 3, 0), (40, 2, 3)):
    t = F.access_ns(f_mhz, base, w); t0 = F.access_ns(f_mhz, base, 0)
    X('cycle', 2, f'Một chu kỳ bus gồm {base} chu kỳ xung nhịp ở {f_mhz} MHz. Nếu thêm {w} trạng thái chờ (wait state) thì chu kỳ bus kéo dài:', f'A bus cycle takes {base} clock periods at {f_mhz} MHz. If {w} wait state(s) are added the bus cycle lasts:',
      [f'{g_(t)} ns', f'{g_(t0)} ns', f'{g_(t + 1000 / f_mhz)} ns', f'{g_(t * 2)} ns'] if w > 0 else [f'{g_(t)} ns', f'{g_(t + 1000 / f_mhz)} ns', f'{g_(t * 2)} ns', f'{g_(t / 2)} ns'], 0,
      f'Chu kỳ xung nhịp = 1000/{f_mhz} = {g_(1000 / f_mhz)} ns; ({base} + {w}) × {g_(1000 / f_mhz)} = {g_(t)} ns (mỗi wait state thêm một chu kỳ xung nhịp, Floyd 14-2).', f'Clock period = 1000/{f_mhz} = {g_(1000 / f_mhz)} ns; ({base} + {w}) × {g_(1000 / f_mhz)} = {g_(t)} ns (each wait state adds one clock period, Floyd 14-2).', 'Trạng thái chờ', 'Wait states')
    meta('wait', [f_mhz, base, w], t, f'wait {f_mhz} {base} {w}')

# ---------------- tu luan goc: Floyd 14-8 Checkup va 14-9 Checkup (dap an in o tr.853) ----------------
E = B.E
def ec(tid, lv, qv, qe, sv, se, tagv, tage):
    E(tid, lv, qv, qe, sv, se, tagv, tage); B.ess[-1]['origin'] = 'goc'; B.ess[-1]['src'] = dict(vi=tagv, en=tage)
ec('mcu', 1, 'Vi điều khiển khác vi xử lý ở điểm nào?', 'How does a microcontroller differ from a microprocessor?', 'Vi điều khiển gồm nhiều phần tử của một hệ máy tính (lõi xử lý, bộ nhớ, ngoại vi), còn vi xử lý chỉ là CPU.', 'A microcontroller includes many elements of a computer system, whereas a microprocessor is only the CPU.', 'Floyd 14-8 Checkup 1 (đáp án tr.853)', 'Floyd 14-8 Checkup 1 (answer p.853)')
ec('mcu', 1, 'Nêu một số khối chức năng thường có trong một vi điều khiển.', 'What are some common functional units found in a typical microcontroller?', 'Lõi xử lý, ROM (bộ nhớ không khả biến), RAM, một hay nhiều ngoại vi phần cứng, khối kết nối tín hiệu giữa các khối chức năng và bộ điều khiển bộ nhớ ngoài.', 'The processor core, ROM, RAM, one or more hardware peripherals, a signal-connection block between the functional blocks and an external memory controller.', 'Floyd 14-8 Checkup 2 (đáp án tr.853)', 'Floyd 14-8 Checkup 2 (answer p.853)')
ec('mcu', 2, 'Nêu một ưu điểm và một nhược điểm của chân đa chức năng trên vi điều khiển.', 'Discuss an advantage and disadvantage of multifunctional pins on a microcontroller.', 'Ưu điểm: giảm số chân và kích thước vật lý của linh kiện. Nhược điểm: không phải lúc nào cũng dùng được mọi tính năng mà ứng dụng cần, nên thiết kế có thể cần thêm phần cứng ngoài.', 'Advantage: it reduces the number of pins and the physical size of the device. Disadvantage: it is not always possible to use every microcontroller feature an application needs, so the design may require additional external hardware.', 'Floyd 14-8 Checkup 3 (đáp án tr.853)', 'Floyd 14-8 Checkup 3 (answer p.853)')
ec('mcu', 1, 'Những ngoại vi nào cho phép vi điều khiển tương tác với thế giới thực?', 'Which peripherals allow a microcontroller to interact with the real world?', 'Bộ định thời, ADC, DAC, bộ điều khiển truyền thông, GPIO, bộ mã hoá vuông góc và bộ điều chế độ rộng xung (PWM).', 'Timers, ADCs, DACs, communication controllers, GPIOs, quadrature encoders and PWMs.', 'Floyd 14-8 Checkup 4 (đáp án tr.853)', 'Floyd 14-8 Checkup 4 (answer p.853)')
ec('mcu', 2, 'Hệ nhúng khác hệ máy tính cá nhân ở điểm nào?', 'How does an embedded system differ from a personal computer system?', 'Hệ nhúng được thiết kế để tương tác trực tiếp với thế giới thực và thực hiện một chức năng xác định; máy tính cá nhân xử lý dữ liệu và cấu hình được với phần mềm ứng dụng để làm nhiều việc.', 'An embedded system is designed to interact directly with the real world and perform a specific function; a personal computer processes data and can be configured with application software to perform a number of tasks.', 'Floyd 14-8 Checkup 5 (đáp án tr.853)', 'Floyd 14-8 Checkup 5 (answer p.853)')
ec('mcu', 1, 'Kể một số loại hệ nhúng có dùng vi điều khiển.', 'Identify some types of embedded systems in which microcontrollers are found.', 'Thiết bị cá nhân, đồ điện tử gia dụng, hệ thống trên ô tô và thiết bị truyền thông (và tự động hoá, robot).', 'Personal electronics, consumer electronics, automotive systems and communication devices (and automation and robotics).', 'Floyd 14-8 Checkup 6 (đáp án tr.853)', 'Floyd 14-8 Checkup 6 (answer p.853)')
ec('mcu', 1, 'SoC (system on chip) là gì?', 'What is a SoC?', 'SoC là một chip hệ thống: một máy tính hoàn chỉnh trên một chip silicon.', 'A SoC is a system chip, a complete computer on a single silicon chip.', 'Floyd 14-9 Checkup 1 (đáp án tr.853)', 'Floyd 14-9 Checkup 1 (answer p.853)')
ec('mcu', 1, 'Nêu hai ưu điểm quan trọng của SoC.', 'What are two important advantages of a SoC?', 'Kích thước nhỏ và công suất tiêu thụ thấp (hợp với thiết bị di động nhỏ).', 'Small size and reduced power consumption.', 'Floyd 14-9 Checkup 2 (đáp án tr.853)', 'Floyd 14-9 Checkup 2 (answer p.853)')
ec('mcu', 2, 'Kể các phần tử chức năng của một SoC.', 'List the functional elements of a SoC.', 'Một hay nhiều lõi xử lý; bộ xử lý tín hiệu số (DSP); bộ xử lý đồ hoạ (GPU); bộ nhớ; ADC và DAC; giao diện I/O; nguồn định thời; quản lý nguồn; cầu nối bus; ngoại vi; logic khả trình.', 'One or more processor cores; a DSP; a GPU; memory; ADC and DAC; I/O interfaces; timing sources; power management; bus bridges; peripherals; and programmable logic.', 'Floyd 14-9 Checkup 3 (đáp án tr.853)', 'Floyd 14-9 Checkup 3 (answer p.853)')

def write():
    fn = os.path.join(OUT, 'm04_mcu.json'); json.dump(B.goc + B.gen, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    fe = os.path.join(OUT, 'm04_mcu_ess.json'); json.dump(B.ess, open(fe, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(META, open(os.path.join(HERE, '..', '..', 'data', 'verify', 'm04_mcu_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('m04_mcu goc', len(B.goc), 'gen', len(B.gen), 'ess', len(B.ess))
if __name__ == '__main__': write()
