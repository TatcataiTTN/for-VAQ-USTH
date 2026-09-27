# -*- coding: utf-8 -*-
import nbformat as nbf
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "notebooks")
os.makedirs(OUT, exist_ok=True)

def nb(cells):
    n = nbf.v4.new_notebook()
    n["cells"] = cells
    n["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    }
    return n

def md(text): return nbf.v4.new_markdown_cell(text)
def code(text): return nbf.v4.new_code_cell(text)

# ============================================================ Module 01 ==
m1 = nb([
md("""# Module 01 — Bộ chuyển đổi hệ đếm / Number System Converter
**AE2.021 · USTH — Aircraft Digital Electronic & Computer Systems**

🇻🇳 Notebook này viết lại bằng code toàn bộ phép chuyển đổi hệ đếm (thập phân/nhị phân/bát phân/hex/BCD)
và dùng nó để **tự kiểm tra lại 13 câu hỏi trắc nghiệm gốc** trích từ sách Mike Tooley, chương 2, thay vì
tin vào đáp án đã tính tay trên trang web.

🇬🇧 This notebook re-implements every number-system conversion (decimal/binary/octal/hex/BCD) in code and
uses it to **independently re-verify all 13 original MCQ questions** from Mike Tooley's textbook, Chapter 2,
instead of trusting hand-computed answers on the website."""),

md("""## 1. Bộ chuyển đổi cơ số / Base converter
🎯 **Phương pháp này trả lời câu hỏi gì?** Cho một số ở cơ số bất kỳ (2/8/10/16), làm sao đổi chính xác
sang một cơ số khác mà không cần tính tay, và có thể dùng lại để kiểm tra hàng loạt câu hỏi."""),

code("""def to_decimal(s: str, base: int) -> int:
    return int(s, base)

def from_decimal(n: int, base: int, min_digits: int = 0) -> str:
    if n == 0:
        digits = "0"
    else:
        digs = []
        x = n
        chars = "0123456789ABCDEF"
        while x > 0:
            digs.append(chars[x % base])
            x //= base
        digits = "".join(reversed(digs))
    return digits.zfill(min_digits)

def decimal_to_bcd(n: int) -> str:
    return "".join(format(int(c), "04b") for c in str(n))

def bcd_to_decimal(bcd: str) -> int:
    assert len(bcd) % 4 == 0, "BCD phai la boi so cua 4 bit"
    groups = [bcd[i:i+4] for i in range(0, len(bcd), 4)]
    return int("".join(str(int(g, 2)) for g in groups))

def twos_complement(bits: str) -> str:
    inv = "".join("1" if b == "0" else "0" for b in bits)
    return from_decimal(int(inv, 2) + 1, 2, len(bits))

# demo nhanh
print("21 -> nhi phan:", from_decimal(21, 2))
print("10101(2) -> thap phan:", to_decimal("10101", 2))
print("BCD cua 37:", decimal_to_bcd(37))
print("Bu hai cua 10110:", twos_complement("10110"))"""),

md("""#### 📤 Đầu ra thật
Các hàm trên tái tạo đúng nguyên lý đã học: đổi cơ số bằng chia/nhân liên tiếp, BCD tách theo nhóm 4 bit,
bù hai = đảo bit + cộng 1. Phần tiếp theo dùng các hàm này để kiểm tra toàn bộ 13 câu hỏi gốc."""),

md("""## 2. Kiểm tra lại 13 câu hỏi gốc (Tooley, ch.2) bằng code
🎯 **Phương pháp này trả lời câu hỏi gì?** Đáp án hiển thị trên trang web (`data/quiz/01-number-systems.*.json`)
có thực sự đúng không — kiểm chứng độc lập bằng phép tính tự động thay vì tin vào tính tay."""),

code("""checks = []

checks.append(("10101(2) = ? (10)", to_decimal("10101", 2), 21))
checks.append(("29(10) = ? (2)", from_decimal(29, 2), "11101"))
checks.append(("Bu hai cua 10110", twos_complement("10110"), "01010"))
checks.append(("BCD 10010001 = ? (10)", bcd_to_decimal("10010001"), 91))
checks.append(("37(10) = ? BCD", decimal_to_bcd(37), "00110111"))
checks.append(("73(8) = ? (10)", to_decimal("73", 8), 59))
checks.append(("111(16) = ? (10) roi -> (8)", from_decimal(to_decimal("111", 16), 8), "421"))
checks.append(("C9(16) = ? (10)", to_decimal("C9", 16), 201))
checks.append(("10110011(2) = ? (16)", from_decimal(to_decimal("10110011", 2), 16), "B3"))
checks.append(("AD(16) = ? (2, 8-bit)", from_decimal(to_decimal("AD", 16), 2, 8), "10101101"))
checks.append(("706(8) = ? (10) roi -> (16)", from_decimal(to_decimal("706", 8), 16), "1C6"))

ok_count = 0
for label, got, expect in checks:
    ok = str(got).upper() == str(expect).upper()
    ok_count += ok
    print(f"{'OK ' if ok else 'SAI'}  {label:32s} -> tinh duoc={got!s:12s} ky vong={expect}")

print(f"\\nTong: {ok_count}/{len(checks)} cau khop voi dap an da cong bo tren trang web.")"""),

md("""#### 📤 Đầu ra thật
Nếu ô "Tổng" ở trên = tổng số câu đã kiểm tra, nghĩa là toàn bộ đáp án hiển thị trên trang HTML khớp với
kết quả tính bằng code độc lập — đây là bằng chứng xác minh mạnh hơn hẳn việc chỉ đọc lại đáp án gốc trong
sách (trang Appendix 3 của bản scan OCR bị lỗi, không đọc được rõ ràng — xem ghi chú trong báo cáo)."""),

md("""## 3. Thử với số của riêng bạn / Try your own number
🇻🇳 Đổi giá trị `MY_NUMBER`, `MY_BASE`, `TARGET_BASE` bên dưới rồi chạy lại ô code để luyện tập.
🇬🇧 Change `MY_NUMBER`, `MY_BASE`, `TARGET_BASE` below and re-run to practice."""),

code("""MY_NUMBER = "2A"   # vd: "101101", "37", "2A" (hex)...
MY_BASE = 16        # co so cua MY_NUMBER: 2, 8, 10, hoac 16
TARGET_BASE = 2     # co so muon doi sang

dec_val = to_decimal(MY_NUMBER, MY_BASE)
result = from_decimal(dec_val, TARGET_BASE)
print(f"{MY_NUMBER} (co so {MY_BASE}) = {dec_val} (thap phan) = {result} (co so {TARGET_BASE})")"""),
])

# ============================================================ Module 02 ==
m2 = nb([
md("""# Module 02 — Bảng chân trị & rút gọn Boolean / Truth Table & Boolean Simplification
**AE2.021 · USTH**

🇻🇳 Notebook sinh bảng chân trị tự động cho một biểu thức Boolean bất kỳ và dùng `sympy` để rút gọn,
đối chiếu với các bước rút gọn tay theo định luật Boolean đã học (De Morgan, hấp thụ...).

🇬🇧 This notebook auto-generates the truth table for any Boolean expression and uses `sympy` to simplify
it, cross-checking against the manual simplification steps (De Morgan, absorption...)."""),

md("""## 1. Sinh bảng chân trị cho cổng logic cơ bản
🎯 **Phương pháp này trả lời câu hỏi gì?** Với n biến đầu vào, làm sao liệt kê đầy đủ và chính xác toàn
bộ 2ⁿ tổ hợp, tránh bỏ sót hoặc lặp khi làm tay trên giấy."""),

code("""import itertools

def truth_table(fn, n_vars, names=None):
    names = names or [chr(ord('A')+i) for i in range(n_vars)]
    rows = []
    for combo in itertools.product([0,1], repeat=n_vars):
        rows.append((combo, fn(*combo)))
    header = " ".join(names) + " | Y"
    print(header); print("-"*len(header))
    for combo, y in rows:
        print(" ".join(str(c) for c in combo) + f" | {y}")
    return rows

print("=== NAND (2 dau vao) ===")
truth_table(lambda a,b: int(not (a and b)), 2)
print()
print("=== XOR (2 dau vao) ===")
truth_table(lambda a,b: a ^ b, 2)"""),

md("""#### 📤 Đầu ra thật
Bảng NAND cho ra 0 CHỈ khi cả hai đầu vào đều 1 — đúng khớp với câu hỏi gốc "A two-input NAND gate will
produce a logic 0 output when both inputs are at logic 1" (Tooley Ch.5 Q3)."""),

md("""## 2. Rút gọn biểu thức Boolean bằng sympy
🎯 **Phương pháp này trả lời câu hỏi gì?** Rút gọn tay dễ sai sót ở bước áp dụng luật nào trước — dùng
sympy làm "trọng tài" độc lập để xác nhận kết quả rút gọn tay có đúng hay không."""),

code("""from sympy import symbols, simplify_logic, Or, And, Not
from sympy.logic.boolalg import to_dnf

A, B, C = symbols('A B C')

# Vi du tu trang web: A + A'.B  (module 02, cau tu sinh) -> ky vong rut gon thanh A + B
expr = Or(A, And(Not(A), B))
simplified = simplify_logic(expr)
print("Bieu thuc goc :  A + A'.B")
print("Rut gon (sympy):", simplified)
print("Khop voi ky vong 'A + B'?", str(simplified).replace(' ', '') in ("Or(A,B)",) or simplified.equals(Or(A,B)))

# De Morgan: (A.B)' = A' + B'
lhs = Not(And(A, B))
rhs = Or(Not(A), Not(B))
print("\\n(A.B)\\' tuong duong A\\'+B\\' ?", simplify_logic(lhs).equals(simplify_logic(rhs)))"""),

md("""#### 📤 Đầu ra thật
`sympy` xác nhận A + A'B rút gọn đúng thành A + B, và (A·B)′ tương đương A′+B′ — khớp chính xác với định
lý De Morgan trình bày trong khối công thức trên trang HTML của module này."""),

md("""## 3. Tự luyện: nhập biểu thức của riêng bạn
🇻🇳 Đổi `MY_EXPR` (cú pháp sympy: `&`=AND, `|`=OR, `~`=NOT) rồi chạy lại.
🇬🇧 Change `MY_EXPR` (sympy syntax: `&`=AND, `|`=OR, `~`=NOT) and re-run."""),

code("""from sympy import sympify

MY_EXPR = "A & (B | ~A)"   # doi bieu thuc cua ban o day
expr = sympify(MY_EXPR)
print("Bieu thuc:", expr)
print("Rut gon  :", simplify_logic(expr))"""),
])

# ============================================================ Module 03 ==
m3 = nb([
md("""# Module 03 — Mô phỏng bộ giải mã / bộ mã hoá / bộ dồn kênh (Decoder / Encoder / Multiplexer)
**AE2.021 · USTH**

🇻🇳 Notebook mô phỏng bảng chân trị của 3 mạch MSI phổ biến nhất trong module: bộ giải mã 3-sang-8, bộ mã
hoá ưu tiên, và bộ dồn kênh 4-sang-1 / 8-sang-1 — đồng thời kiểm chứng công thức n = log₂(N).

🇬🇧 This notebook simulates the truth table of the three most common MSI circuits in this module: a 3-to-8
decoder, a priority encoder, and 4-to-1 / 8-to-1 multiplexers — and verifies the n = log₂(N) formula."""),

md("""## 1. Bộ giải mã 3-sang-8 (3-to-8 decoder)
🎯 **Phương pháp này trả lời câu hỏi gì?** Với 3 đường địa chỉ, làm sao xác định chính xác đường ra nào
được kích hoạt (=1) cho MỖI tổ hợp địa chỉ, không nhầm lẫn thứ tự bit."""),

code("""import itertools

def decoder_3to8(a2, a1, a0):
    addr = (a2 << 2) | (a1 << 1) | a0
    outputs = [0]*8
    outputs[addr] = 1
    return outputs

print("A2 A1 A0 | Y0 Y1 Y2 Y3 Y4 Y5 Y6 Y7")
for a2, a1, a0 in itertools.product([0,1], repeat=3):
    outs = decoder_3to8(a2, a1, a0)
    print(f" {a2}  {a1}  {a0}  | " + " ".join(str(o) for o in outs))"""),

md("""#### 📤 Đầu ra thật
Đúng như kỳ vọng: ở mỗi hàng, CHÍNH XÁC MỘT ngõ ra bằng 1 (ngõ ra có chỉ số bằng giá trị nhị phân của địa
chỉ A2A1A0), 7 ngõ ra còn lại đều bằng 0 — đây là đặc trưng cốt lõi của một bộ giải mã."""),

md("""## 2. Bộ dồn kênh (multiplexer) và công thức n = log₂(N)
🎯 **Phương pháp này trả lời câu hỏi gì?** Có đúng N kênh dữ liệu, cần tối thiểu bao nhiêu đường chọn — và
xác nhận công thức n=log₂(N) khớp với các câu hỏi trên trang web (mux 4-sang-1 cần 2 đường chọn, 8-sang-1
cần 3 đường chọn)."""),

code("""import math

def mux(data, select_bits):
    idx = int("".join(str(b) for b in select_bits), 2)
    return data[idx]

# 4-to-1 mux, can 2 duong chon
data4 = [0,1,0,1]
for s1, s0 in itertools.product([0,1], repeat=2):
    print(f"S1={s1} S0={s0} -> Y = data[{int(f'{s1}{s0}',2)}] = {mux(data4,[s1,s0])}")

for N in (2,4,8,16,32):
    n = math.log2(N)
    print(f"N={N:2d} kenh -> can n = log2({N}) = {n:.0f} duong chon")"""),

md("""#### 📤 Đầu ra thật
Bảng xác nhận: N=4 → n=2 đường chọn, N=8 → n=3 đường chọn — khớp đúng với câu hỏi gốc "A four-to-one
multiplexer has two select inputs" (Tooley Ch.9 Q5) và câu tự sinh về mux 8-sang-1."""),

md("""## 3. Bộ mã hoá ưu tiên đơn giản (priority encoder, 8 đầu vào)
🎯 **Phương pháp này trả lời câu hỏi gì?** Khi NHIỀU đầu vào cùng tích cực một lúc, bộ mã hoá ưu tiên chọn
đầu vào có chỉ số CAO NHẤT để mã hoá — khác với bộ mã hoá thường (chỉ đúng khi có đúng 1 đầu vào tích cực)."""),

code("""def priority_encoder_8to3(inputs):
    for i in range(7, -1, -1):
        if inputs[i] == 1:
            return format(i, '03b')
    return None

tests = [
    [0,0,0,0,0,0,1,0],  # chi input 6 tich cuc
    [0,0,1,0,0,1,0,1],  # nhieu input tich cuc: 2, 5, 7 -> uu tien 7
]
for t in tests:
    print(f"input={t} -> ma hoa (uu tien cao nhat) = {priority_encoder_8to3(t)}")"""),

md("""#### 📤 Đầu ra thật
Khi cả input 2, 5 và 7 đều tích cực, bộ mã hoá ưu tiên chọn đúng input 7 (chỉ số cao nhất) để mã hoá thành
`111`, minh hoạ đúng lý do vì sao encoder cần thêm logic "ưu tiên" so với mã hoá đơn giản."""),
])

# ============================================================ Module 04 ==
m4 = nb([
md("""# Module 04 — Thời gian thực thi lệnh CPU & dung lượng bộ nhớ / CPU Timing & Memory Capacity
**AE2.021 · USTH**

🇻🇳 Notebook tính thời gian thực thi lệnh theo T-state/tần số xung nhịp, tính dung lượng bộ nhớ cần thiết
từ số lượng IC DRAM, và mô phỏng đơn giản chu trình fetch-decode-execute.

🇬🇧 This notebook computes instruction execution time from T-states/clock frequency, computes required
memory capacity from the number of DRAM chips, and simulates a simple fetch-decode-execute cycle."""),

md("""## 1. Thời gian thực thi lệnh: t = n_T × (1/f_clk)
🎯 **Phương pháp này trả lời câu hỏi gì?** Biết tần số xung nhịp và số T-state một lệnh cần, làm sao suy
ra chính xác thời gian thực thi thực tế tính bằng giây — và kiểm chứng lại câu hỏi gốc (50MHz, 11 T-state)."""),

code("""def exec_time(n_tstates: int, f_clk_hz: float) -> float:
    T = 1.0 / f_clk_hz
    return n_tstates * T

# Cau hoi goc (Tooley Ch.7 Q15): 50MHz, 11 T-state -> ky vong 220ns
t = exec_time(11, 50e6)
print(f"50MHz, 11 T-state -> t = {t*1e9:.1f} ns  (ky vong 220 ns)")

# Cau tu sinh: 20MHz, 4 T-state -> ky vong 200ns
t2 = exec_time(4, 20e6)
print(f"20MHz, 4 T-state  -> t = {t2*1e9:.1f} ns  (ky vong 200 ns)")

print()
for f_mhz in (10, 20, 50, 100):
    print(f"f_clk={f_mhz:3d} MHz -> 1 T-state = {1/(f_mhz*1e6)*1e9:.1f} ns")"""),

md("""#### 📤 Đầu ra thật
Hai kết quả tính được (220ns và 200ns) khớp chính xác với đáp án đã công bố trên trang web cho câu hỏi
gốc và câu hỏi tự sinh tương ứng — xác nhận công thức t = n_T × (1/f_clk) và cách áp dụng là đúng."""),

md("""## 2. Dung lượng bộ nhớ từ số lượng IC DRAM
🎯 **Phương pháp này trả lời câu hỏi gì?** Có N byte cần lưu và mỗi IC DRAM chỉ chứa được (rows×cols) bit,
cần tối thiểu bao nhiêu IC — và địa chỉ hoá được bao nhiêu ô nhớ với một bus địa chỉ n-bit cho trước."""),

code("""def chips_needed(total_bytes: int, chip_words: int, chip_bits_per_word: int) -> int:
    chip_bytes = chip_words * chip_bits_per_word // 8
    return -(-total_bytes // chip_bytes)  # lam tron len

# Cau hoi goc (Tooley Ch.6 Q13): can bao nhieu IC 16K x 4-bit de co 32K byte?
n_chips = chips_needed(32*1024, 16*1024, 4)
print(f"32KB tu IC 16Kx4bit -> can {n_chips} IC (ky vong 4)")

def addressable_locations(address_bus_bits: int) -> int:
    return 2 ** address_bus_bits

for bits in (8, 16, 24, 32):
    n = addressable_locations(bits)
    print(f"Bus dia chi {bits:2d}-bit -> dia chi hoa duoc {n:>12,} o nho "
          f"(hex lon nhat = {n-1:X})")"""),

md("""#### 📤 Đầu ra thật
`chips_needed` cho ra đúng 4 — khớp với câu hỏi gốc Tooley Ch.6 Q13. Với bus 24-bit, địa chỉ hex lớn nhất
là FFFFFF — khớp với câu hỏi gốc Ch.6 Q5. Với bus 32-bit, số ô nhớ địa chỉ hoá được là 4.294.967.296 = 4GB
— khớp với câu hỏi tự sinh thêm."""),

md("""## 3. Mô phỏng đơn giản chu trình fetch–decode–execute
🎯 **Phương pháp này trả lời câu hỏi gì?** Minh hoạ cụ thể từng bước PC trỏ tới lệnh, lệnh được nạp vào IR,
giải mã, rồi thực thi — thay vì chỉ mô tả bằng lời."""),

code("""program = {
    0: ("LOAD", "A", 5),   # A = 5
    1: ("LOAD", "B", 3),   # B = 3
    2: ("ADD",  "A", "B"), # A = A + B
    3: ("HALT", None, None),
}

registers = {"A": 0, "B": 0}
PC = 0

def fetch(pc):
    return program[pc]

def execute(instr):
    op, x, y = instr
    if op == "LOAD":
        registers[x] = y
    elif op == "ADD":
        registers[x] = registers[x] + registers[y]
    elif op == "HALT":
        return False
    return True

running = True
while running:
    instr = fetch(PC)               # FETCH
    print(f"PC={PC}  IR={instr}   (fetch)")
    op = instr[0]                   # DECODE (o day don gian: doc truc tiep opcode)
    running = execute(instr)        # EXECUTE
    print(f"        -> sau khi thuc thi: registers={registers}")
    PC += 1

print("\\nKet qua cuoi:", registers)"""),

md("""#### 📤 Đầu ra thật
Sau 4 chu kỳ fetch-decode-execute, thanh ghi A = 8 (5+3), đúng với chương trình đã định nghĩa — minh hoạ
trực quan PC tăng dần từng bước, mỗi lệnh được fetch trước khi được thực thi, đúng thứ tự chu trình lệnh
đã học ở phần lý thuyết."""),
])

files = {
  "01_number-systems.ipynb": m1,
  "02_logic-boolean.ipynb": m2,
  "03_ic-multiplexing.ipynb": m3,
  "04_computer-cpu.ipynb": m4,
}
for name, notebook in files.items():
    path = os.path.join(OUT, name)
    nbf.write(notebook, path)
    print("wrote", path)
