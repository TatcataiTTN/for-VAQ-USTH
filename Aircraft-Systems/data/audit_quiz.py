# -*- coding: utf-8 -*-
"""Audit thien lech quiz: vi tri dap an dung (chi-square), do dai (dap an dung la dai nhat), ti le Dung/Sai.
Chay: python3 data/audit_quiz.py  (doc data/quiz/*.vi.json)."""
import json, glob, os
from collections import Counter
from scipy.stats import chisquare, binomtest
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz")
rows = []
tot_pos = Counter(); tot_n = 0
for fn in sorted(glob.glob(os.path.join(D, "*.vi.json"))):
    slug = os.path.basename(fn).replace(".vi.json", "")
    data = json.load(open(fn, encoding="utf-8"))
    for key, items in data.items():
        mc = [it for it in items if len(it["opts"]) >= 3]
        tf = [it for it in items if len(it["opts"]) == 2]
        if mc:
            k = max(len(it["opts"]) for it in mc)
            pos = Counter(it["correct"] for it in mc)
            n = len(mc)
            obs = [pos.get(i, 0) for i in range(k)]
            p = chisquare(obs, [n / k] * k).pvalue if n >= 5 else float("nan")
            L = sum(1 for it in mc if len(it["opts"][it["correct"]]) == max(len(o) for o in it["opts"]))
            strict = sum(1 for it in mc if len(it["opts"][it["correct"]]) > max(len(o) for i, o in enumerate(it["opts"]) if i != it["correct"]))
            pl = binomtest(strict, n, 1 / 3).pvalue if n >= 5 else float("nan")
            rows.append((slug, key, n, obs, p, strict, pl))
            for i, v in enumerate(obs): tot_pos[i] += v
            tot_n += n
        if tf:
            ok = sum(1 for it in tf if it["correct"] == 0)
            pt = binomtest(ok, len(tf), 0.5).pvalue if len(tf) >= 5 else float("nan")
            rows.append((slug, key + " [dung/sai]", len(tf), [ok, len(tf) - ok], pt, None, None))
print(f"{'module':26s} {'nhom':24s} {'n':>3s}  vi_tri_dung(A,B,C,..)      p(vi tri)  dap an DAI NHAT(strict)  p(do dai)")
flag = []
for slug, key, n, obs, p, strict, pl in rows:
    s = f"{slug:26s} {key:24s} {n:3d}  {str(obs):26s} {p:9.4f}"
    if strict is not None: s += f"   {strict:3d}/{n:<3d}={strict/n*100:4.0f}%        {pl:8.4f}"
    print(s)
    if p == p and p < 0.05: flag.append((slug, key, "vi tri", p))
    if pl is not None and pl == pl and pl < 0.05: flag.append((slug, key, "do dai", pl))
print("\nTong hop vi tri dap an tren toan site:", dict(tot_pos), "n =", tot_n)
print("Nhom co p < 0.05:", *[f"{a}/{b} ({c}, p={p:.4f})" for a, b, c, p in flag], sep="\n  ")
