# -*- coding: utf-8 -*-
"""Audit thien lech quiz: vi tri dap an dung (tong the) va ti le dap an dung dai nhat."""
import json, glob, collections
pos = collections.Counter(); longest = 0; total = 0; rows = []
for f in sorted(glob.glob("quiz/*.vi.json")):
    d = json.load(open(f, encoding="utf-8"))
    for k, items in d.items():
        for it in items:
            total += 1; pos[it["correct"]] += 1
            lens = [len(o) for o in it["opts"]]
            if lens[it["correct"]] == max(lens) and lens.count(max(lens)) == 1:
                longest += 1
n = total
print("tong cau:", n, "| vi tri dung:", dict(sorted(pos.items())), "| ti le dap an dung la duy nhat dai nhat: %.0f%% (ky vong ~25%%)" % (100 * longest / n))
# chi-square don gian cho vi tri (4 lua chon)
exp = n / 4; chi = sum((pos[i] - exp) ** 2 / exp for i in range(4)); print("chi2 vi tri =", round(chi, 2), "(nguong 0.05 voi 3 bac tu do: 7.81)")
