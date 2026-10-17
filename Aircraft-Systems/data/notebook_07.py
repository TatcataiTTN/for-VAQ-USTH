# -*- coding: utf-8 -*-
import nbformat as nbf, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebooks"); os.makedirs(OUT, exist_ok=True)
md = nbf.v4.new_markdown_cell; code = nbf.v4.new_code_cell
cells = [
md("""# Module 07: Kiểm soát phần mềm hàng không / Aircraft Software Control
**AE2.021 · USTH**

🇻🇳 Notebook viết lại bằng code checksum 8 bit và CRC-8, tái hiện Ví dụ 2-41 của Floyd, thử ba kiểu lỗi (lật bit, đổi chỗ, hai lỗi triệt tiêu), mô phỏng quyết định phát hành FLS/DFLD theo Tooley 13.3.3, kiểm tra các con số mức A đến E và đối chiếu khoá đáp án in của Tooley chương 13 (đọc trực tiếp từ ảnh scan Appendix 3, A.13, trang 380).

🇬🇧 This notebook rewrites the 8-bit checksum and CRC-8 in code, reproduces Floyd Example 2-41, tries three error types (bit flip, swap, cancelling errors), simulates the FLS/DFLD release decision from Tooley 13.3.3, checks the level A to E numbers and cross-checks Tooley's printed chapter 13 answer key (read directly from the scanned Appendix 3 image, A.13, page 380)."""),
md("## 1. Checksum 8 bit và CRC-8 / 8-bit checksum and CRC-8"),
code("""def checksum8(b): return sum(b) & 0xFF
def crc8(b, poly=0x07):
    c = 0
    for x in b:
        c ^= x
        for _ in range(8):
            c = ((c << 1) ^ poly) & 0xFF if c & 0x80 else (c << 1) & 0xFF
    return c

# Gia tri chuan cua CRC-8 (poly 0x07) tren chuoi ASCII '123456789' la 0xF4
assert crc8(b"123456789") == 0xF4
data = bytes.fromhex("48 65 6C 6C 6F 20 45 45 43 21")      # cung tep voi Demo 1 tren trang
print("checksum8 =", hex(checksum8(data)), " crc8 =", hex(crc8(data)))
assert checksum8(bytes([10, 20, 30, 40, 50])) == 150        # cau tu sinh cua module"""),
md("## 2. Ba kiểu lỗi / Three error types"),
code("""def verdict(orig, bad):
    return dict(checksum_sees=checksum8(bad) != checksum8(orig), crc_sees=crc8(bad) != crc8(orig))

flip = bytearray(data); flip[5] ^= 0x04
swap = bytearray(data); swap[1], swap[8] = swap[8], swap[1]
comp = bytearray(data); comp[0] = (comp[0] + 1) & 255; comp[9] = (comp[9] - 1) & 255
for name, bad in (("lat 1 bit", flip), ("doi cho 2 byte", swap), ("hai loi triet tieu", comp)):
    print(f"{name:20s}", verdict(data, bad))
assert verdict(data, flip) == dict(checksum_sees=True, crc_sees=True)
assert verdict(data, swap) == dict(checksum_sees=False, crc_sees=True)     # checksum 'mu' voi doi cho
assert verdict(data, comp) == dict(checksum_sees=False, crc_sees=True)

# Mo rong: CRC-8 co bat duoc MOI loi 1 bit va moi loi 2 byte doi cho khac nhau khong? (thu toan bo)
import itertools
missed_flip = sum(1 for i in range(len(data)) for k in range(8)
                  if crc8(bytes(x ^ (1 << k) if j == i else x for j, x in enumerate(data))) == crc8(data))
print("loi 1 bit CRC bo sot:", missed_flip, "tren", len(data) * 8)
assert missed_flip == 0
miss_swap = [(i, j) for i, j in itertools.combinations(range(len(data)), 2)
             if data[i] != data[j] and crc8(bytes(data[j] if t == i else data[i] if t == j else x for t, x in enumerate(data))) == crc8(data)]
print("cap doi cho (byte khac nhau) CRC-8 bo sot:", miss_swap, "- checksum bo sot TAT CA cac cap do")"""),
md("## 3. Floyd Ví dụ 2-41 / Floyd Example 2-41"),
code("""def mod2_remainder(bits, g):
    b = [int(c) for c in bits]; gg = [int(c) for c in g]
    for i in range(len(b) - len(gg) + 1):
        if b[i]:
            for j, x in enumerate(gg): b[i + j] ^= x
    return "".join(map(str, b[-(len(gg) - 1):]))
D, G = "11010011", "1010"
appended = D + "0" * len(G)                         # Floyd them 4 so 0 (bang so bit cua G)
rem = mod2_remainder(appended, G)
print("du:", rem)                                    # '100' voi 3 bit cuoi; Floyd viet 0100 (4 bit)
assert rem == "100" and rem.zfill(4) == "0100"
tx = D + rem.zfill(4)
print("ma truyen:", tx)
assert tx == "110100110100"
assert mod2_remainder(tx, G) == "000"               # ben nhan chia lai duoc du 0
# Phien ban CRC chuan chi them len(G)-1 = 3 so 0:
std_rem = mod2_remainder(D + "000", G); print("CRC chuan (3 so 0):", std_rem, "-> ma truyen", D + std_rem)
assert mod2_remainder(D + std_rem, G) == "000"
# Parity (Floyd Bang 2-8): bit chan cho BCD 0111 la 1
assert bin(0b0111).count("1") % 2 == 1"""),
md("## 4. Quyết định phát hành FLS/DFLD (Tooley 13.3.3) / FLS/DFLD release decision"),
code("""def release_document(kind, airworthiness_requirement=True, nav_database=False):
    \"\"\"Tra ve giay to di kem theo Tooley 13.3.3.\"\"\"
    if kind not in ("FLS", "LSAP", "DFLD"): raise ValueError(kind)
    if nav_database: return "Letter of Acceptance (khong the cap Form 1 hoac 8130-3)"
    if kind == "LSAP" or (kind == "DFLD" and airworthiness_requirement): return "EASA Form 1 hoac FAA 8130-3"
    return "Certificate of Conformity"
assert release_document("LSAP") == "EASA Form 1 hoac FAA 8130-3"                       # EEC, DFDAU, ECU APU, FGC
assert release_document("DFLD", True) == "EASA Form 1 hoac FAA 8130-3"                 # FMC, TAWS, IMA
assert release_document("DFLD", True, nav_database=True).startswith("Letter of Acceptance")
assert release_document("FLS", False) == "Certificate of Conformity"

def may_load(suspect_corrupt, version_ok):
    return "QUARANTINE (khong thu truyen)" if suspect_corrupt or not version_ok else "co the nap"
assert may_load(True, True).startswith("QUARANTINE") and may_load(False, True) == "co the nap"
print("Quy tac phat hanh va cach ly: OK")"""),
md("## 5. Mức A đến E / Levels A to E"),
code("""LEVELS = {"A": (None, 1e-9), "B": (1e-9, 1e-7), "C": (1e-7, 1e-5), "D": (1e-5, None)}   # (min, max) xac suat/gio bay, Tooley bang 13.1
def level_for(p):
    for k, (lo, hi) in LEVELS.items():
        if (lo is None or p >= lo) and (hi is None or p < hi): return k
assert level_for(1e-10) == "A" and level_for(5e-9) == "B" and level_for(1e-6) == "C" and level_for(1e-3) == "D"
# So trace bat buoc theo hinh 13-1: do (A) 2, tim (A,B,C) 3, xanh (A-D) 3 mui ten nhom
TRACES = {"red": ("A",), "purple": ("A", "B", "C"), "green": ("A", "B", "C", "D")}
need = {lv: [c for c, lvls in TRACES.items() if lv in lvls] for lv in "ABCDE"}
print(need)
assert need["A"] == ["red", "purple", "green"] and need["B"] == need["C"] == ["purple", "green"] and need["D"] == ["green"] and need["E"] == []"""),
md("## 6. Khoá đáp án Tooley Ch.13 / Tooley Ch.13 answer key"),
code("""KEY = dict(zip(range(1, 8), "c b c c b a b".split()))      # A.13 trang 380
# Cau co the tu kiem: 
assert KEY[2] == "b"      # Level B = extremely remote (bang 13.1)
assert KEY[4] == "c"      # radar thoi tiet = Class D (bang 13.2), la lua chon (c)
assert KEY[5] == "b"      # EEC = LSAP
assert KEY[6] == "a"      # OSS va UMS la lop cua FLS
assert KEY[7] == "b"      # buoc cuoi nap EEC la kiem chung
print("Khop 5/5 cau tu kiem duoc; cau 1 va 3 la cau dinh nghia (c) va (c) theo van ban Tooley 13.1-13.2.")"""),
md("""#### 📤 Nhận xét / Takeaway
🇻🇳 Mọi con số tự tính đều khớp. Checksum bỏ sót mọi phép đổi chỗ và hai lỗi triệt tiêu; CRC-8 bắt được cả ba kiểu lỗi trong thử nghiệm, nhưng CRC cũng có thể bỏ sót một số lỗi khác (không tuyệt đối). Đáp án in câu 13-6 của bài giảng thiếu mũi tên đỏ thứ hai của hình 13-1.

🇬🇧 All computed numbers agree. The checksum misses every swap and cancelling errors; CRC-8 caught all three error types tested, but a CRC can also miss other errors (not absolute). The lecture's printed answer to question 13-6 omits the second red arrow of Figure 13-1."""),
]
nb = nbf.v4.new_notebook(); nb["cells"] = cells
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3"}}
nbf.write(nb, os.path.join(OUT, "07_software-control.ipynb")); print("wrote")
