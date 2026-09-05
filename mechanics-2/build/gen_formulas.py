#!/usr/bin/env python3
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from formulas_source import FORMULAS, COLORS

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"

def main():
    items = []
    for i, f in enumerate(FORMULAS):
        items.append({**f, "num": i + 1, "color": COLORS[i % len(COLORS)]})
    m1 = sum(1 for f in FORMULAS if f["topic"] == "M1")
    m2 = sum(1 for f in FORMULAS if f["topic"] == "M2")
    json.dump({"items": items, "count_m1": m1, "count_m2": m2},
              open(f"{OUT_DIR}/formulas.json", "w"), ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} formula cards -> data/formulas.json  (M1={m1}, M2={m2})")

if __name__ == "__main__":
    main()
