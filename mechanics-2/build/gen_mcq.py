#!/usr/bin/env python3
"""Shuffle each MCQ's 4 options with a fixed seed (independent of authoring order) and remap
the correct-answer letter accordingly -- never trust a hand-typed 'correct: A'. Then run the
position-bias / length-bias audit from build-practical-website's pitfalls.md before writing
the final JSON. Tries several seeds, keeps the one with the most even A/B/C/D distribution.
"""
import random, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from questions_source import QUESTIONS

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"
LETTERS = ["A", "B", "C", "D"]

def build_with_seed(seed):
    rnd = random.Random(seed)
    out = []
    for i, q in enumerate(QUESTIONS):
        options = [q["correct"]] + list(q["wrong"])
        idx = list(range(4))
        rnd.shuffle(idx)
        shuffled = [options[j] for j in idx]
        correct_letter = LETTERS[idx.index(0)]
        out.append({
            "id": f"mcq-{i+1:02d}",
            "lecture": q["lecture"],
            "question": q["q"],
            "options": {LETTERS[k]: shuffled[k] for k in range(4)},
            "correct": correct_letter,
        })
    return out

def chisq(counts):
    total = sum(counts)
    expected = total / len(counts)
    return sum((c - expected) ** 2 / expected for c in counts)

def audit(items):
    counts = [0, 0, 0, 0]
    for it in items:
        counts[LETTERS.index(it["correct"])] += 1
    stat = chisq(counts)
    # length bias
    ratios = []
    for it in items:
        correct_len = len(it["options"][it["correct"]])
        other_lens = [len(v) for k, v in it["options"].items() if k != it["correct"]]
        avg_other = sum(other_lens) / len(other_lens)
        if avg_other > 0:
            ratios.append(correct_len / avg_other)
    avg_ratio = sum(ratios) / len(ratios)
    return counts, stat, avg_ratio

def main():
    best = None
    for seed in range(1, 200):
        items = build_with_seed(seed)
        counts, stat, ratio = audit(items)
        if best is None or stat < best[1]:
            best = (seed, stat, counts, ratio, items)
    seed, stat, counts, ratio, items = best
    print(f"Chosen seed={seed}  A/B/C/D counts={counts}  chi2={stat:.3f}  "
          f"avg_len_ratio(correct/distractor)={ratio:.3f}")
    assert stat < 7.815, "position bias too high (chi2 >= critical value at df=3, p=0.05)"
    assert 0.7 < ratio < 1.4, "length bias detected -- correct answers systematically longer/shorter"

    by_lecture = {}
    for it in items:
        by_lecture.setdefault(it["lecture"], []).append(it)

    json.dump({"items": items, "by_lecture": by_lecture, "seed": seed},
              open(f"{OUT_DIR}/mcq.json", "w"), ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} MCQ items -> data/mcq.json")

if __name__ == "__main__":
    main()
