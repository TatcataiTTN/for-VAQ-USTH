# -*- coding: utf-8 -*-
"""Sinh quiz_en_overlay.py: ban tieng Anh cua `explain` va `opts` (quiz EN truoc day lay nham ban tieng Viet).
- Floyd: phuong an lay NGUYEN VAN tu sach (pdftotext /tmp/floyd_full3.txt), ghep theo tung cau.
- Tooley/generated: quiz_en_opts.OPT_EN_MANUAL (tra nguoc ve cach dien dat goc).
- explain: /tmp/expl_list.json (khoa tieng Viet, sap xep) ghep voi /tmp/en_expl_{0,1,2}.py."""
import re, json, sys, pprint
sys.path.insert(0, ".")
import floyd_quiz_source as F
from quiz_en_opts import OPT_EN_MANUAL
txt = open("/tmp/floyd_full3.txt", encoding="utf-8").read()
norm = lambda s: re.sub(r"[\s­]+", " ", s).strip()
T = norm(txt.replace("’", "'").replace("−", "-"))
vi_re = re.compile(r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]')
per_item = {}
for slug, mod in F.FLOYD_MODULES.items():
    for it in mod["st"]:
        q = norm(it["en"].replace("’", "'"))
        i = T.find(q[:45])
        if i < 0:
            continue
        seg = T[i:i + 900]
        m = re.search(r"\(a\)(.*?)\(b\)(.*?)\(c\)(.*?)(?:\(d\)(.*?))?(?=\s\d{1,2}\.\s|\s\(e\)|$)", seg)
        if not m:
            continue
        eng = [re.sub(r"\s(M\d\d_FLOY|Problems Answers to odd|Chapter \d+ |\d{3}\s+[A-Z][a-z]+ ).*$", "", norm(g)) for g in m.groups() if g is not None]
        if len(eng) == len(it["opts"]):
            per_item[it["vi"]] = dict(zip(it["opts"], eng))
sys.path.insert(0, "/tmp")
import en_expl_0, en_expl_1, en_expl_2
E = en_expl_0.E0 + en_expl_1.E1 + en_expl_2.E2
keys = json.load(open("/tmp/expl_list.json", encoding="utf-8"))
assert len(E) == len(keys)
out = "# -*- coding: utf-8 -*-\n# TU DONG SINH boi build_en_overlay.py, khong sua tay.\n"
out += "EXPLAIN_EN = " + pprint.pformat(dict(zip(keys, E)), width=140) + "\n"
out += "OPT_EN_BY_Q = " + pprint.pformat(per_item, width=140) + "\n"
open("quiz_en_overlay.py", "w", encoding="utf-8").write(out)
print("explain", len(E), "per-item option maps", len(per_item))
