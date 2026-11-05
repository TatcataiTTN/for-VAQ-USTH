import os, subprocess, nbformat as nbf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
def build(lang):
    vi = lang == 'vi'; T = lambda a, b: a if vi else b; nb = nbf.v4.new_notebook(); C = []
    md = lambda s: C.append(nbf.v4.new_markdown_cell(s)); code = lambda s: C.append(nbf.v4.new_code_cell(s))
    md(T('# Module 01 · IC và mạch logic (EASA M04 SM01)', '# Module 01 · Integrated circuits and logic (EASA M04 SM01)'))
    md(T('## 1. Đổi nhị phân ↔ thập phân', '## 1. Binary ↔ decimal conversion'))
    code('for d in (13, 29, 45, 100, 255): print(d, "->", format(d, "b"))\nfor b in ("1011", "11001", "100101"): print(b, "->", int(b, 2))\nprint("5 + 3 =", format(5+3, "b"), "; 13 + 3 =", format(13+3, "b"))')
    md(T('**Nhận xét:** 13 → 1101, 45 → 101101, 255 → 11111111; 1011₂ = 11, 11001₂ = 25; 5 + 3 = 1000₂ và 13 + 3 = 10000₂ (nhớ lan qua nhiều cột).', '**Comment:** 13 → 1101, 45 → 101101, 255 → 11111111; 1011₂ = 11, 11001₂ = 25; 5 + 3 = 1000₂ and 13 + 3 = 10000₂ (the carry ripples through several columns).'))
    md(T('## 2. Bảng chân lý các cổng', '## 2. Gate truth tables'))
    code('import itertools\nG = {"AND": lambda a,b: a&b, "OR": lambda a,b: a|b, "NAND": lambda a,b: 1-(a&b), "NOR": lambda a,b: 1-(a|b), "XOR": lambda a,b: a^b}\nprint("A B | " + " ".join(f"{n:>4}" for n in G))\nfor a, b in itertools.product((0,1), repeat=2): print(a, b, "| " + " ".join(f"{G[n](a,b):>4}" for n in G))\nprint("De Morgan check (NOR == AND of inverted inputs):", all(G["NOR"](a,b) == ((1-a)&(1-b)) for a,b in itertools.product((0,1), repeat=2)))\nprint("De Morgan check (NAND == OR of inverted inputs):", all(G["NAND"](a,b) == ((1-a)|(1-b)) for a,b in itertools.product((0,1), repeat=2)))')
    md(T('**Nhận xét:** XOR chỉ khác OR ở dòng 1-1 (0 thay vì 1); NOR bằng AND của các ngõ vào đảo và NAND bằng OR của các ngõ vào đảo (cả hai kiểm tra đều True) — đó là lý do Negative AND ≡ NOR, Negative OR ≡ NAND.', '**Comment:** XOR differs from OR only on the 1-1 row (0 instead of 1); NOR equals the AND of inverted inputs and NAND equals the OR of inverted inputs (both checks print True) — which is why Negative AND ≡ NOR and Negative OR ≡ NAND.'))
    md(T('## 3. Bộ cộng nửa và bộ cộng đầy đủ', '## 3. Half-adder and full-adder'))
    code('def half(a, b): return a ^ b, a & b\ndef full(a, b, cin):\n    s1, c1 = half(a, b); s, c2 = half(s1, cin); return s, c1 | c2\nfor a in (0,1):\n    for b in (0,1): print(f"half({a},{b}) -> (sum,carry) = {half(a,b)}")\nA, B = 0b1101, 0b0011; carry = 0; out = []\nfor i in range(4):\n    s, carry = full((A>>i)&1, (B>>i)&1, carry); out.append(s)\nprint("ripple add 1101 + 0011 =", carry, "".join(map(str, reversed(out))))')
    md(T('**Nhận xét:** bộ cộng nửa cho (0,0), (1,0), (1,0), (0,1); cộng 1101 + 0011 bằng chuỗi bộ cộng đầy đủ cho nhớ ra 1 và tổng 0000, tức 10000₂ = 16.', '**Comment:** the half-adder gives (0,0), (1,0), (1,0), (0,1); adding 1101 + 0011 with a chain of full-adders gives a final carry of 1 and sum bits 0000, i.e. 10000₂ = 16.'))
    md(T('## 4. JK flip-flop', '## 4. The JK flip-flop'))
    code('def jk(q, j, k): return {(0,0): q, (0,1): 0, (1,0): 1, (1,1): 1-q}[(j,k)]\nfor j, k in ((0,0),(0,1),(1,0),(1,1)): print(f"J={j} K={k}: Q=0 -> {jk(0,j,k)},  Q=1 -> {jk(1,j,k)}")\nq = 0; seq = []\nfor _ in range(6): q = jk(q, 1, 1); seq.append(q)\nprint("J=K=1 over 6 clocks:", seq, "-> divide-by-2 of the clock")')
    md(T('**Nhận xét:** J = K = 1 làm Q đảo mỗi xung nhịp (1,0,1,0,1,0) nên flip-flop chia tần số xung nhịp cho 2 — nền tảng của bộ đếm.', '**Comment:** J = K = 1 toggles Q on every clock (1,0,1,0,1,0) so the flip-flop divides the clock frequency by 2 — the basis of counters.'))
    nb['cells'] = C; return nb
if __name__ == '__main__':
    for lang in ('vi', 'en'):
        p = os.path.join(ROOT, 'notebooks', f'm01_ic_logic_{lang}.ipynb'); nbf.write(build(lang), p)
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', p], check=True, capture_output=True); print('executed', p)
