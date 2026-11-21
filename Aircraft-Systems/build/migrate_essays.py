# -*- coding: utf-8 -*-
"""MOT LAN: chuyen data/essay_questions.py (ESSAY) sang data/qsrc/mNN_ess.json (kind 'ess'): de, anh dap an in (afig), anh de (figs), loi giai chu neu co."""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__)); ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(ROOT, "data"))
from modules import MODS
from topics import classify
import essay_questions as E
BY = {m["slug"]: m for m in MODS}
def clean(t): return re.sub(r"~\{([^{}]*)\}", lambda m: "$\\overline{" + m.group(1).replace("*", "\\cdot ").replace("+", "+") + "}$", t)
tot = 0
for slug, entry in E.ESSAY.items():
    m = BY[slug]; items = []
    for it in entry["items"]:
        qv, qe = clean(it["q_vi"]), clean(it["q_en"])
        tid, tname = classify(m["id"], (qv + " " + qe).lower())
        nv, ne = it.get("note_vi", ""), it.get("note_en", "")
        av, ae = it.get("ans_vi"), it.get("ans_en")
        if av:
            solv, sole = av, ae or av
        else:
            solv = "Đáp án in trong sách/tài liệu (xem ảnh dưới đây)." + (" " + nv if nv else ""); sole = "The printed answer is shown in the image below." + (" " + ne if ne else "")
        d = dict(kind="ess", q=dict(vi=qv, en=qe), sol=dict(vi=solv, en=sole), topic=tname, topic_id=tid, level=2, origin="goc",
                 src=dict(vi=it["src"], en=it.get("src_en") or it["src"]))
        if not av and it.get("img"): d["afig"] = "assets/figures/" + it["img"]
        if it.get("qimgs"): d["figs"] = ["assets/figures/" + x for x in it["qimgs"]]
        items.append(d)
    json.dump(items, open(os.path.join(ROOT, "data", "qsrc", f"{m['id']}_ess.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot += len(items); print(m["id"], len(items), sum(1 for i in items if i.get("afig")), "co anh dap an")
print("TONG", tot)
