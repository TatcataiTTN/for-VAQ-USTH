# -*- coding: utf-8 -*-
"""Render site tu cac content_NN.build(lang). Chay: python3 -I render.py"""
import os, sys, json, html, hashlib, importlib, copy
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
MODS = ["content_01", "content_02", "content_03", "content_04"]
import extras

def ver():
    h = hashlib.md5()
    d = os.path.join(ROOT, "_shared")
    for fn in sorted(os.listdir(d)):
        h.update(open(os.path.join(d, fn), "rb").read())
    return h.hexdigest()[:8]
VER = ver()

T = {
 "vi": dict(site="Khí động lực học & Cơ học bay", sub="Tự học AE2.008 · USTH",
   hero="Tự học môn AE2.008: Khí động lực học và Cơ học bay",
   hero_sub="4 module bám EASA Module 08 (Basic Aerodynamics), đối chiếu Anderson "
            "<i>Fundamentals of Aerodynamics</i> (6th) và Etkin &amp; Reid <i>Dynamics of Flight</i> (3rd). "
            "Có slide song ngữ kèm hình gốc, demo tương tác, quiz tự chấm, bài tập có lời giải và notebook Python.",
   open="Mở bài giảng →", back="← Trang chủ", other="English", part="PHẦN", fs="⛶ Toàn màn hình",
   prev="◀ Trước", next="Sau ▶", explain="📖 Giải thích cho người mới bắt đầu",
   formula="Công thức", history="lịch sử", case="tình huống", warn="lưu ý",
   quiz="✅ Quiz tự kiểm tra", prob="✍️ Bài tập có lời giải", reveal="👁️ Xem lời giải",
   nb="📓 Notebook Python đi kèm", nbopen="Xem/tải notebook (.ipynb) →",
   map="📚 Ánh xạ chương giáo trình", mapnav="Ánh xạ chương sách",
   maptitle="Bảng ánh xạ: module ↔ chương giáo trình",
   mapintro="Mỗi module đối chiếu mục lục thật của ba giáo trình trong đề cương AE2.008 (đọc từ bản OCR, không suy đoán). "
            "Đề cương không có bảng chương nên thứ tự lấy theo EASA Module 08, giáo trình chính của môn.",
   foot="Biên soạn từ OCR và đối chiếu chéo tài liệu môn AE2.008 (USTH). Mọi đáp án số đều tính lại bằng Python; "
        "câu gốc ghi rõ nguồn, câu bổ sung gắn nhãn riêng."),
 "en": dict(site="Aerodynamics & Flight Mechanics", sub="Self-study AE2.008 · USTH",
   hero="Self-study AE2.008: Aerodynamics and Flight Mechanics",
   hero_sub="4 modules following EASA Module 08 (Basic Aerodynamics), cross-referenced with Anderson "
            "<i>Fundamentals of Aerodynamics</i> (6th) and Etkin &amp; Reid <i>Dynamics of Flight</i> (3rd). "
            "Bilingual slides with original figures, live demos, self-graded quizzes, worked problems and Python notebooks.",
   open="Open lesson →", back="← Home", other="Tiếng Việt", part="PART", fs="⛶ Fullscreen",
   prev="◀ Prev", next="Next ▶", explain="📖 Explained for complete beginners",
   formula="Formula", history="history", case="case", warn="watch out",
   quiz="✅ Self-check quiz", prob="✍️ Worked problems", reveal="👁️ Show the solution",
   nb="📓 Companion Python notebook", nbopen="View/download notebook (.ipynb) →",
   map="📚 Textbook chapter mapping", mapnav="Chapter mapping",
   maptitle="Mapping: module ↔ textbook chapters",
   mapintro="Each module is matched against the real tables of contents of the three textbooks listed in the AE2.008 syllabus "
            "(read from the OCR text, not guessed). The syllabus has no chapter table, so the order follows EASA Module 08, the course's main text.",
   foot="Built from OCR and cross-referenced AE2.008 (USTH) materials. Every numeric answer is recomputed in Python; "
        "original questions cite their source and supplementary ones carry their own label."),
}

def page(lang, prefix, body, title, desc, extra_css=""):
    t = T[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{prefix}_shared/common.css?v={VER}"/>
{extra_css}
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}"/>
</head>
<body>
<header class="site"><div class="bar">
  <a class="brand" href="{prefix}index.html">{t['site']}<small>{t['sub']}</small></a>
  <div class="toolbar"><a href="__OTHER__">{t['other']}</a>
    <details><summary>🎨</summary><div class="menu">
      <button data-set-theme="light">☀️ Light</button><button data-set-theme="dark">🌙 Dark</button>
      <button data-set-theme="sepia">📜 Sepia</button><button data-set-theme="ocean">🌊 Ocean</button>
    </div></details></div></div></header>
{body}
<footer class="site"><div class="wrap"><p>{t['foot']}</p>
<p><a href="https://github.com/TatcataiTTN/for-VAQ-USTH" target="_blank" rel="noopener">GitHub</a></p></div></footer>
<script src="{prefix}_shared/theme.js?v={VER}"></script>
</body></html>"""

def slide(kicker, inner, divider=False):
    return f'<div class="mdeck-slide{" part-divider" if divider else ""}"><div class="kicker">{kicker}</div>{inner}</div>'

def deck(lang, m):
    t = T[lang]; sl = []
    sl.append(slide(f"MODULE {m['num']} · {m['tag']}", f"<h2>{m['title']}</h2><p>{m['intro']}</p><p class='pill'>{m['src']}</p>"))
    for i, p in enumerate(m["parts"], 1):
        sl.append(slide(f"{t['part']} {i}/5", f"<div class='part-num'>{i:02d}</div><h2>{p['title']}</h2><ul class='part-list'>" +
                        "".join(f"<li>{b}</li>" for b in p["bullets"]) + "</ul>", True))
        for cs in p["slides"]:
            ex = (f"<details class='slide-explain'><summary>{t['explain']}</summary><div class='slide-explain-body'>{cs['explain']}</div></details>"
                  if cs.get("explain") else "")
            fig = ""
            if cs.get("img"):
                src = "../../../assets/figures/" + cs["img"]
                fig = (f"<figure class='slide-fig'><a href='{src}' target='_blank' rel='noopener'><img src='{src}' alt='{html.escape(cs['title'], quote=True)}' loading='lazy'/></a>"
                       f"<figcaption>{cs.get('cap', '')}</figcaption></figure>")
            sl.append(slide(f"{t['part']} {i}/5 · {m['num']}", f"<h2>{cs['title']}</h2>{cs['body']}{fig}{ex}"))
    legend = "".join(f"<li><b>{k}</b><span>{v}</span></li>" for k, v in m["legend"])
    sl.append(slide(f"{t['part']} · {t['formula']}", f"<h2>{m['formula_label']}</h2><div class='pd-formula'><div class='pd-formula-label'>{m['formula_label']}</div><div class='pd-formula-math'>{m['formula_math']}</div></div><ul class='pd-legend'>{legend}</ul>"))
    for key, ic in (("history", "📜"), ("case", "🔎"), ("warn", "⚠️")):
        sl.append(slide(f"{ic} {t[key]}", f"<h2>{m[key+'_title']}</h2><p>{m[key]}</p>"))
    return ('<div class="mdeck"><div class="mdeck-viewport">' + "\n".join(sl) + '</div><div class="mdeck-bar">'
            f'<button class="mdeck-prev">{t["prev"]}</button><button class="mdeck-next">{t["next"]}</button>'
            f'<span class="mdeck-count"></span><div class="mdeck-dots"></div><button class="mdeck-fs">{t["fs"]}</button></div></div>')

def quiz_block(s):
    for it in s['items']:
        it['src'] = html.unescape(it.get('src', ''))
    js = json.dumps({"items": s["items"]}, ensure_ascii=False).replace("</", "<\\/")
    intro = f"<p class='essay-intro'>{s['intro']}</p>" if s.get("intro") else ""
    return f"<h3>{s['title']}</h3>{intro}<div class=\"quiz\"><script type=\"application/json\">{js}</script></div>"

def problems_block(lang, m):
    t = T[lang]
    if not m.get("problems"): return ""
    rows = []
    for p in m["problems"]:
        rows.append(f"""<div class="essay-item"><p class="essay-q"><b>{p['num']}.</b> {p['q']}</p>
<p class="pill">{p['src']}</p>
<details class="essay-answer"><summary>{t['reveal']}</summary><div class="essay-answer-body"><div class='essay-own'>{p['ans']}</div></div></details></div>""")
    return f"<h2>{t['prob']}</h2><p class='essay-intro'>{m['problems_intro']}</p>" + "\n".join(rows)

def module_page(lang, m, prefix="../../../"):
    t = T[lang]; mp = m["mapping"]
    body = f"""<div class="wrap">
<p><a href="../../index.html">{t['back']}</a></p>
<div class="hero"><span class="pill">MODULE {m['num']}</span><h1>{m['title']}</h1><p>{m['src']}</p></div>
<div class="callout info"><h4>{t['map']}</h4><p><b>EASA Module 08:</b> {mp['easa']}</p><p><b>Anderson (6th):</b> {mp['anderson']}</p><p><b>Etkin &amp; Reid (3rd):</b> {mp['etkin']}</p><p>{mp['note']}</p><p><a href="../../../chapter-mapping-{lang}.html">{t['mapnav']} →</a></p></div>
{deck(lang, m)}
{extras.demo_html(m['slug'], lang)}
<div class="callout history"><h4>{m['history_title']}</h4><p>{m['history']}</p></div>
<div class="callout case"><h4>{m['case_title']}</h4><p>{m['case']}</p></div>
<div class="callout warn"><h4>{m['warn_title']}</h4><p>{m['warn']}</p></div>
<div class="callout good"><h4>{t['nb']}</h4><p>{m['nb_desc']}</p><p><a class="nb-link" href="../../../data/notebooks/{m['num']}_{m['slug'].split('-',1)[1]}.ipynb" download>📓 {t['nbopen']}</a></p></div>
<h2>{t['quiz']}</h2>
{''.join(quiz_block(s) for s in m['quiz_sets'])}
{problems_block(lang, m)}
</div>"""
    h = page(lang, prefix, body, f"{m['title']} · {t['site']}", m["intro"], f'<link rel="stylesheet" href="{prefix}_shared/deck.css?v={VER}"/>')
    h = h.replace("__OTHER__", f"../../../{'en' if lang=='vi' else 'vi'}/modules/{m['slug']}/index.html")
    dj = f'<script src="{prefix}_shared/demo_aero.js?v={VER}"></script>' if extras.demo_html(m['slug'], lang) else ''
    return h.replace("</body></html>", dj + f'<script src="{prefix}_shared/deck.js?v={VER}"></script><script src="{prefix}_shared/quiz.js?v={VER}"></script></body></html>')

def home(lang, mods):
    t = T[lang]
    cards = "\n".join(f"""<a class="mod-card" href="modules/{m['slug']}/index.html"><span class="tag">{m['tag']}</span>
<h3>MODULE {m['num']}: {m['title']}</h3><p style="color:var(--muted);font-size:.85rem">{m['src']}</p><span class="cta">{t['open']}</span></a>""" for m in mods)
    body = f"""<div class="wrap"><div class="hero"><h1>{t['hero']}</h1><p>{t['hero_sub']}</p><p><a href="../chapter-mapping-{lang}.html">{t['map']}</a></p></div><div class="mod-grid">{cards}</div></div>"""
    return page(lang, "../", body, t["site"], re_strip(t["hero_sub"])).replace("__OTHER__", f"../{'en' if lang=='vi' else 'vi'}/index.html")

def re_strip(s):
    import re
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&")

def mapping(lang, mods):
    t = T[lang]
    head = ("Module", "EASA Module 08", "Anderson, Fundamentals of Aerodynamics (6th ed.)", "Etkin &amp; Reid, Dynamics of Flight (3rd ed.)", "Ghi chú" if lang == "vi" else "Note")
    rows = "".join(f"<tr><td><b>{m['num']}: {m['title']}</b></td><td>{m['mapping']['easa']}</td><td>{m['mapping']['anderson']}</td><td>{m['mapping']['etkin']}</td><td>{m['mapping']['note']}</td></tr>" for m in mods)
    body = f"""<div class="wrap"><p><a href="{lang}/index.html">{t['back']}</a></p><div class="hero"><h1>{t['maptitle']}</h1><p>{t['mapintro']}</p></div>
<table class="chapmap"><thead><tr>{''.join(f'<th>{h}</th>' for h in head)}</tr></thead><tbody>{rows}</tbody></table></div>"""
    return page(lang, "./", body, f"{t['mapnav']} · {t['site']}", re_strip(t["mapintro"])).replace("__OTHER__", f"chapter-mapping-{'en' if lang=='vi' else 'vi'}.html")

def main():
    built = {}
    for lang in ("vi", "en"):
        built[lang] = [importlib.import_module(n).build(lang) for n in MODS]
        for m in built[lang]:
            for pi, slides in extras.figure_slides(m['slug'], lang).items():
                m['parts'][pi]['slides'].extend(slides)
            gen = [q for q in m['quiz_sets'] if q['key'] == 'generated'][0]
            gen['items'].extend(extras.extra_quiz(m['slug'], lang))
    for lang in ("vi", "en"):
        mods = built[lang]
        open(os.path.join(ROOT, lang, "index.html"), "w", encoding="utf-8").write(home(lang, mods))
        for m in mods:
            d = os.path.join(ROOT, lang, "modules", m["slug"]); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(module_page(lang, m))
        open(os.path.join(ROOT, f"chapter-mapping-{lang}.html"), "w", encoding="utf-8").write(mapping(lang, mods))
    # du lieu quiz de audit
    qd = os.path.join(HERE, "quiz"); os.makedirs(qd, exist_ok=True)
    for lang in ("vi", "en"):
        for m in built[lang]:
            json.dump({s["key"]: s["items"] for s in m["quiz_sets"]}, open(os.path.join(qd, f"{m['slug']}.{lang}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Rendered OK")
if __name__ == "__main__":
    main()
