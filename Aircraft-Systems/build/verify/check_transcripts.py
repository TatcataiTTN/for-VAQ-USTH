# -*- coding: utf-8 -*-
"""Kiem cau truc cac file data/slides/transcript/*.json: du trang, khong rong, khong gach ngang dai/ngan, kind hop le, VI co dau tieng Viet."""
import json, sys, re, glob, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VI = re.compile("[ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]", re.I)
KINDS = {"content", "title", "divider", "blank", "thanks"}
def main(paths):
    bad = 0; total = 0
    for p in paths:
        d = json.load(open(p, encoding="utf-8")); a, b = d["range"]; got = [s["page"] for s in d["slides"]]
        if got != list(range(a, b + 1)): print("FAIL", p, "trang khong lien tuc/du:", got[:5], "..."); bad += 1
        for s in d["slides"]:
            total += 1
            for k in ("text_en", "text_vi"):
                if not isinstance(s.get(k), str) or not s[k].strip(): print("FAIL", p, s["page"], k, "rong"); bad += 1
            if s.get("kind") not in KINDS: print("FAIL", p, s["page"], "kind", s.get("kind")); bad += 1
            blob = json.dumps(s, ensure_ascii=False)
            if "–" in blob or "—" in blob: print("FAIL", p, s["page"], "co gach ngang dai/ngan"); bad += 1
            if s.get("text_vi") and s["kind"] != "blank" and len(s["text_vi"]) > 40 and not VI.search(s["text_vi"]): print("FAIL", p, s["page"], "text_vi khong co dau tieng Viet"); bad += 1
            for k in ("formulas", "numbers", "issues"):
                if not isinstance(s.get(k), list): print("FAIL", p, s["page"], k, "khong phai list"); bad += 1
    print(("OK" if not bad else "LOI") + f": {total} slide trong {len(paths)} file")
    return bad
if __name__ == "__main__":
    ps = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "data", "slides", "transcript", "*.json")))
    sys.exit(1 if main(ps) else 0)
