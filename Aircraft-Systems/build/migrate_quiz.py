# -*- coding: utf-8 -*-
"""MOT LAN: chuyen ngan hang cu (data/quiz/NN.{vi,en}.json: nhom tooley/floyd/generated) sang data/qsrc/mNN.json (+ mNN_gen.json) cua pipeline moi.
Sau lan chay nay data/qsrc la NGUON SU THAT; data/quiz/*.json chi con la ban luu. Chay lai se GHI DE: dung chi khi muon dung lai tu dau.
Quy tac (ghi vao data/verify/migration_notes.json): topic gan bang tu khoa (build/topics.py); level gan bang quy tac (tf=1; tinh toan 2; nhieu buoc 3);
origin: nhom tooley/floyd = 'goc', generated = 'bo_sung'; kind: 2 lua chon = 'tf', con lai 'mcq'; fixed_order khi lua chon tham chieu nhau."""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from modules import MODS
from topics import classify
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OLD = os.path.join(ROOT, "data", "quiz"); OUT = os.path.join(ROOT, "data", "qsrc"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, "data"))
REF = re.compile(r"tất cả|cả hai|cả a|none of|all of the|both|neither|cả \(|không có|phương án (a|b|c)", re.I)
CALC = re.compile(r"tính|bao nhiêu|calculate|compute|how many|how much|what is the (value|result|output|sum|product)|=|\d\s*(v|mv|khz|mhz|ghz|db|dbm|kb|mb|bit|ω|ohm)\b", re.I)
HARD = re.compile(r"so sánh|khác nhau|đúng nhất|không phải|không đúng|except|not (a|an|true)|compare|difference|why|tại sao|vì sao", re.I)

def numeric_opts(opts): return sum(1 for o in opts if re.search(r"\d", o)) >= len(opts) - 0

def level_of(kind, q, opts, expl, det):
    if kind == "tf": return 1
    steps = (expl or "").count("=") + re.sub(r"<[^>]+>", " ", det or "").count("=")
    if steps >= 4 or (numeric_opts(opts) and steps >= 2 and len(q) > 90): return 3
    if numeric_opts(opts) and CALC.search(q + " " + (expl or "")): return 2
    if CALC.search(q) and steps >= 2: return 2
    if HARD.search(q) or len(q) > 170: return 2
    return 1

def main():
    notes = dict(mismatch=[], dup=[], per_module={})
    tot = collections.Counter()
    for m in MODS:
        slug = m["slug"]; pv = os.path.join(OLD, f"{slug}.vi.json")
        if not os.path.exists(pv): continue
        dv = json.load(open(pv, encoding="utf-8")); de = json.load(open(os.path.join(OLD, f"{slug}.en.json"), encoding="utf-8"))
        main_items, gen_items = [], []
        for grp in ("tooley", "floyd", "generated"):
            for j, (v, e) in enumerate(zip(dv[grp], de[grp])):
                if len(v["opts"]) != len(e["opts"]) or v["correct"] != e["correct"]:
                    notes["mismatch"].append(f'{slug}/{grp}/{j}'); continue
                kind = "tf" if len(v["opts"]) == 2 else "mcq"
                tid, tname = classify(m["id"], " ".join([v["q"], e["q"], " ".join(v["opts"]), " ".join(e["opts"]), v.get("explain", ""), e.get("explain", "")]).lower())
                it = dict(kind=kind, q=dict(vi=v["q"], en=e["q"]), opts=[dict(vi=a, en=b) for a, b in zip(v["opts"], e["opts"])], correct=v["correct"],
                          explain=dict(vi=v.get("explain", ""), en=e.get("explain", "")), topic=tname, topic_id=tid,
                          level=level_of(kind, v["q"], v["opts"], v.get("explain", ""), v.get("detail", "")), origin="goc" if grp != "generated" else "bo_sung")
                if v.get("detail"): it["detail"] = dict(vi=v["detail"], en=e.get("detail") or "")
                sv, se = (v.get("src") or "").strip(), (e.get("src") or "").strip()
                if not sv:
                    sv = f"Bổ sung · tự sinh theo nội dung module {m['id'][1:]} (chưa gắn số slide)"; se = f"Added · generated from the content of module {m['id'][1:]} (slide number not yet attached)"
                it["src"] = dict(vi=sv, en=se or sv)
                if kind == "mcq" and REF.search(" ".join(v["opts"])): it["fixed_order"] = True
                if v.get("fig"): it["fig"] = v["fig"]
                if it["q"]["en"].startswith("The hexadecimal number E3") and v["opts"][0] == v["opts"][2]:   # in Tooley tr.366 (a) va (c) in giong het nhau: sua (c), giu dap an (b), ghi vao notes
                    it["opts"][2] = dict(vi="00111110", en="00111110"); it["note_fix"] = "Tooley in (a) và (c) cùng là 11100111 (tr.366, PDF 380); (c) được thay bằng 00111110 (hai nhóm 4 bit đảo chỗ)."
                    notes.setdefault("source_fixes", []).append(dict(item="Tooley Revision Paper 6 Q2", what="options (a) and (c) printed identically as 11100111 (printed p.366, PDF p.380); option (c) replaced by 00111110, key (b) 11100011 unchanged"))
                (gen_items if grp == "generated" else main_items).append(it)
        json.dump(main_items, open(os.path.join(OUT, f"{m['id']}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(gen_items, open(os.path.join(OUT, f"{m['id']}_gen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        c = collections.Counter(i["topic_id"] for i in main_items + gen_items); lv = collections.Counter(i["level"] for i in main_items + gen_items)
        notes["per_module"][m["id"]] = dict(n=len(main_items) + len(gen_items), main=len(main_items), gen=len(gen_items), topics=dict(c), levels=dict(lv))
        tot["n"] += len(main_items) + len(gen_items)
        print(m["id"], len(main_items), "+", len(gen_items), "levels", dict(sorted(lv.items())), "topics", dict(c))
    os.makedirs(os.path.join(ROOT, "data", "verify"), exist_ok=True)
    json.dump(notes, open(os.path.join(ROOT, "data", "verify", "migration_notes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("TONG", tot["n"], "| lech VI/EN:", notes["mismatch"])
main()
