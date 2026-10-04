# -*- coding: utf-8 -*-
import json, os, html, importlib

from module_content import MODULES
from essay_questions import ESSAY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../Aircraft-Systems

def _ver():
    import hashlib
    h = hashlib.md5()
    d = os.path.join(ROOT, "_shared")
    for fn in sorted(os.listdir(d)):
        h.update(open(os.path.join(d, fn), "rb").read())
    return h.hexdigest()[:8]
VER = _ver()
QUIZ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz")

def load_extra_slides(mod):
    """Doc data/slides_<NN>.py (neu co) va gan vao mod[lang]['parts'][i]['slides']."""
    modname = f"slides_{mod['num']}"
    try:
        m = importlib.import_module(modname)
    except ModuleNotFoundError:
        return
    for lang in ("vi", "en"):
        part_slides = m.SLIDES.get(lang, [])
        parts = mod[lang]["parts"]
        for i, part in enumerate(parts):
            if i < len(part_slides):
                part["slides"] = part_slides[i]

L = {
  "vi": {
    "site_title": "Hệ thống điện tử số & máy tính hàng không",
    "site_sub": "Tự học AE2.021 · USTH",
    "home_hero_title": "Tự học môn AE2.021 (Electronics Systems: Analog & Digital Systems)",
    "home_hero_sub": "5 module bám sát bộ slide giảng dạy thật của môn, đối chiếu 2 giáo trình tham khảo "
                      "(Mike Tooley & Thomas Floyd), có quiz tự chấm và notebook Python đi kèm.",
    "open": "Mở bài giảng →", "soon": "Sắp có",
    "mapping_link": "📚 Bảng ánh xạ 5 bài giảng ↔ chương sách giáo trình",
    "footer": "Biên soạn từ OCR + đối chiếu chéo tài liệu môn AE2.021 (USTH). Câu hỏi gốc trích Tooley, "
              "đã tính toán lại độc lập để xác minh đáp án: xem ghi chú nguồn trong từng câu.",
    "explain_more": "📖 Giải thích cho người mới bắt đầu", "zoom_hint": "Bấm vào ảnh để phóng to",
    "part_label": "PHẦN", "fs": "⛶ Toàn màn hình", "prev": "◀ Trước", "next": "Sau ▶",
    "formula_box": "Công thức", "history": "history", "case": "case", "warn": "warn",
    "essay_title": "✍️ Câu hỏi tự luận (nguồn: Floyd, Digital Fundamentals)",
    "essay_intro": "Các câu hỏi tự luận dưới đây trích từ phần \"Problems\" cuối chương sách Floyd (chỉ chọn câu số lẻ, vì sách chỉ in đáp án cho câu số lẻ ở phụ lục cuối sách). Mỗi câu có bản dịch tiếng Việt kèm nguyên văn tiếng Anh của sách; những câu nhắc \"Figure\" cần xem hình đó trong sách. Đáp án luôn là ẢNH CHỤP THẬT từ đúng trang phụ lục, không gõ lại, để bạn tự đối chiếu.",
    "essay_reveal": "👁️ Xem đáp án gốc trong sách",
    "quiz_title": "✅ Quiz tự kiểm tra", "quiz_tooley": "Sách 1: Mike Tooley, Aircraft Digital Electronic and Computer Systems (câu MCQ cuối chương, đã tính lại để xác minh đáp án)", "quiz_floyd": "Sách 2: Thomas Floyd, Digital Fundamentals (True/False Quiz + Self-Test cuối chương, đối chiếu đúng đáp án in trong sách)", "quiz_gen": "Câu luyện tập bổ sung (do AI biên soạn thêm theo cùng dạng, đáp án tự kiểm chứng bằng tính toán)",
    "notebook": "📓 Notebook Python đi kèm", "notebook_open": "Xem/tải notebook (.ipynb) →",
    "back_home": "← Trang chủ", "lang_switch": "English",
    "nav_mapping": "Ánh xạ chương sách",
    "mapping_title": "Bảng ánh xạ: 5 bài giảng ↔ chương giáo trình tham khảo",
    "mapping_intro": "Bảng dưới đối chiếu trực tiếp mục lục 2 sách tham khảo của môn AE2.021 với 4 bộ slide "
                      "giảng dạy thật: dựa trên việc đọc mục lục và nội dung đã OCR của cả hai sách, không suy đoán.",
  },
  "en": {
    "site_title": "Aircraft Digital Electronics & Computer Systems",
    "site_sub": "Self-study AE2.021 · USTH",
    "home_hero_title": "Self-study AE2.021 (Electronics Systems: Analog & Digital Systems)",
    "home_hero_sub": "5 modules following the course's real lecture slides, cross-referenced with 2 textbooks "
                      "(Mike Tooley & Thomas Floyd), with a self-graded quiz and companion Python notebook.",
    "open": "Open lesson →", "soon": "Coming soon",
    "mapping_link": "📚 Chapter mapping: 5 lectures ↔ textbook chapters",
    "footer": "Built from OCR + cross-referenced AE2.021 (USTH) course materials. Original questions are from "
              "Tooley, independently recomputed to verify each answer: see the source note on each question.",
    "explain_more": "📖 Explained for complete beginners", "zoom_hint": "Click the image to enlarge",
    "part_label": "PART", "fs": "⛶ Fullscreen", "prev": "◀ Prev", "next": "Next ▶",
    "formula_box": "Formula", "history": "history", "case": "case", "warn": "warn",
    "essay_title": "✍️ Free-response questions (source: Floyd, Digital Fundamentals)",
    "essay_intro": "The free-response questions below are copied verbatim from the \"Problems\" section at the end of the relevant Floyd chapter (odd-numbered only, since the book only prints answers for odd-numbered problems in its back-of-book appendix). Questions are retyped by hand (overlines mark complements, as in the book); a few mention a \"Figure\" that you need to look up in the book. The answer is always a REAL PHOTOGRAPH of that exact appendix page, never retyped, so you can check it yourself.",
    "essay_reveal": "👁️ Show the book's original answer",
    "quiz_title": "✅ Self-check quiz", "quiz_tooley": "Book 1: Mike Tooley, Aircraft Digital Electronic and Computer Systems (end-of-chapter MCQs, independently recomputed to verify each answer)", "quiz_floyd": "Book 2: Thomas Floyd, Digital Fundamentals (True/False Quiz + Self-Test, cross-checked against the book’s own printed answer key)", "quiz_gen": "Additional practice questions (AI-authored in the same style, answers self-verified by computation)",
    "notebook": "📓 Companion Python notebook", "notebook_open": "View/download notebook (.ipynb) →",
    "back_home": "← Home", "lang_switch": "Tiếng Việt",
    "nav_mapping": "Chapter mapping",
    "mapping_title": "Chapter mapping: 5 lectures ↔ reference textbook chapters",
    "mapping_intro": "The table below directly cross-references the tables of contents of AE2.021's two "
                      "reference textbooks against the 4 real lecture slide decks: based on reading the OCR'd "
                      "table of contents and content of both books, not guesswork.",
  },
}

MAPPING_ROWS = [
  {
    "module": "01: Number Systems",
    "tooley": "Ch.2 Number systems (p.25-38): decimal, binary, octal, hex, ASCII",
    "floyd": "Ch.2 Number Systems, Operations, and Codes (p.65-124)",
    "note_vi": "Khớp trực tiếp gần như 1-1: cả 2 sách đều dành nguyên 1 chương cho đúng 4 hệ đếm này.",
    "note_en": "Near 1-to-1 match: both books devote exactly one chapter to these same four number systems.",
  },
  {
    "module": "02: Logic Circuits & Boolean Algebra",
    "tooley": "Ch.5 Logic circuits (p.70-94): gates, Boolean algebra, combinational logic, tri-state, "
              "monostable/bistable, logic families",
    "floyd": "Ch.3 Logic Gates (p.125-190) + Ch.4 Boolean Algebra and Logic Simplification (p.191-260); "
             "phần bistable đối chiếu thêm Ch.7 Latches, Flip-Flops, and Timers (p.387-448)",
    "floyd_en": "Ch.3 Logic Gates (p.125-190) + Ch.4 Boolean Algebra and Logic Simplification (p.191-260); "
                "the bistable part is cross-referenced with Ch.7 Latches, Flip-Flops, and Timers (p.387-448)",
    "note_vi": "Tooley gộp cả gate + Boolean + bistable vào 1 chương; Floyd tách thành 3 chương riêng chi tiết hơn.",
    "note_en": "Tooley bundles gates + Boolean algebra + bistables into one chapter; Floyd splits this into three "
               "more detailed chapters.",
  },
  {
    "module": "03: Integrated Circuits & Multiplexing",
    "tooley": "Ch.8 Integrated circuits (p.139-148) + Ch.9 MSI logic (p.149-164): fan-in/out, decoders, "
              "encoders, multiplexers",
    "floyd": "Ch.6 Functions of Combinational Logic (p.313-386): decoders, encoders, multiplexers, "
             "demultiplexers, comparators; công nghệ chế tạo IC đối chiếu thêm Ch.15 Integrated Circuit "
             "Technologies (p.855+)",
    "floyd_en": "Ch.6 Functions of Combinational Logic (p.313-386): decoders, encoders, multiplexers, "
                "demultiplexers, comparators; IC fabrication technology is cross-referenced with Ch.15 "
                "Integrated Circuit Technologies (p.855+)",
    "note_vi": "Tooley tách 'công nghệ IC' (ch.8) và 'ứng dụng MSI' (ch.9) thành 2 chương; Floyd gộp toàn bộ "
               "ứng dụng MSI vào Ch.6 và để công nghệ chế tạo riêng ở cuối sách (Ch.15).",
    "note_en": "Tooley splits 'IC technology' (ch.8) and 'MSI applications' (ch.9) into two chapters; Floyd "
               "bundles all MSI applications into Ch.6 and keeps fabrication technology separate at the end "
               "of the book (Ch.15).",
  },
  {
    "module": "04: Computers & Microprocessors",
    "tooley": "Ch.6 Computers (p.95-115): computer systems, data storage, backplane bus + Ch.7 The CPU "
              "(p.116-138): internal architecture, x86/Pentium/AMD 29050",
    "floyd": "Ch.11 Data Storage (p.627-696): RAM/ROM/Flash memory. Floyd KHÔNG có chương riêng về kiến trúc "
             "CPU/vi xử lý: đây là điểm khác biệt lớn nhất giữa 2 sách cho module này.",
    "floyd_en": "Ch.11 Data Storage (p.627-696): RAM/ROM/Flash memory. Floyd has NO dedicated chapter on CPU/"
                "microprocessor architecture: this is the biggest difference between the two books for this module.",
    "note_vi": "Đây là module có độ khớp THẤP NHẤT giữa 2 sách: Floyd là sách nền tảng logic số thuần tuý, "
               "không đi sâu kiến trúc máy tính/CPU như Tooley: phần CPU trong module này chủ yếu dựa vào Tooley.",
    "note_en": "This module has the WEAKEST match between the two books: Floyd is a pure digital-logic "
               "fundamentals text and does not cover computer/CPU architecture in depth like Tooley: the CPU "
               "content in this module relies mainly on Tooley.",
  },
  {
    "module": "05: Data Buses",
    "tooley": "Ch.4 Data buses (p.53-69): bus rationale, ARINC 429 (electrical/word format/BCD-BNR), other "
              "standards (ARINC 629/AFDX/MIL-STD-1553/legacy buses), 17-question MCQ bank",
    "floyd": "KHÔNG CÓ chương nào về bus dữ liệu hàng không trong Floyd: đây là giáo trình điện tử số thuần tuý "
             "(cổng logic, bộ nhớ), không đề cập avionics/giao tiếp nối tiếp chuyên dụng. Toàn bộ module này dựa "
             "vào Tooley và bộ slide bài giảng riêng của môn.",
    "floyd_en": "Floyd has NO chapter on aircraft data buses whatsoever: it is a pure digital-electronics "
                "textbook (logic gates, memory) with no coverage of avionics-specific serial communication. This "
                "module relies entirely on Tooley and the course's own lecture slides.",
    "note_vi": "Module có độ khớp THẤP NHẤT với Floyd trong cả 5 module (thấp hơn cả Module 04): chủ đề bus "
               "hàng không hoàn toàn vắng mặt trong Floyd, nên quiz của module này chỉ có 2 nguồn (Tooley + câu "
               "bổ sung), không có mục quiz riêng từ Floyd.",
    "note_en": "This module has the LOWEST match with Floyd of all 5 modules (even lower than Module 04): "
               "aircraft bus topics are entirely absent from Floyd, so this module's quiz has only 2 sources "
               "(Tooley + supplementary questions), with no separate Floyd quiz section.",
  },
]

HEAD_TEMPLATE = """<!doctype html>
<html lang="{lang_attr}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<script>(function(){{try{{
  var t = localStorage.getItem('site-theme');
  if (t && t !== 'light') document.documentElement.setAttribute('data-theme', t);
}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{prefix}_shared/common.css?v={VER}"/>
{extra_css}
<title>{page_title}</title>
<meta name="description" content="{description}"/>
</head>
<body>
"""

HEADER_TEMPLATE = """<header class="site"><div class="bar">
  <a class="brand" href="{prefix}index.html">{site_title}<small>{site_sub}</small></a>
  <div class="toolbar">
    <a href="{other_lang_href}">{lang_switch}</a>
    <details><summary>🎨</summary><div class="menu">
      <button data-set-theme="light">☀️ Light</button>
      <button data-set-theme="dark">🌙 Dark</button>
      <button data-set-theme="sepia">📜 Sepia</button>
      <button data-set-theme="ocean">🌊 Ocean</button>
    </div></details>
  </div>
</div></header>
"""

FOOTER_TEMPLATE = """<footer class="site"><div class="wrap">
  <p>{footer}</p>
  <p><a href="https://github.com/tatcataittn/for-VAQ-USTH" target="_blank" rel="noopener">GitHub</a></p>
</div></footer>
<script src="{prefix}_shared/theme.js?v={VER}"></script>
</body></html>
"""

def esc(s):
    return s

def render_page(lang, prefix, body, extra_css="", title_suffix="", description=""):
    t = L[lang]
    other = "en" if lang == "vi" else "vi"
    return (
        HEAD_TEMPLATE.format(
            lang_attr=lang, prefix=prefix, VER=VER, extra_css=extra_css,
            page_title=(t["site_title"] + (": " + title_suffix if title_suffix else "")),
            description=description or t["home_hero_sub"],
        )
        + HEADER_TEMPLATE.format(
            prefix=prefix, site_title=t["site_title"], site_sub=t["site_sub"],
            other_lang_href="__OTHER_LANG__", lang_switch=t["lang_switch"],
        )
        + body
        + FOOTER_TEMPLATE.format(footer=t["footer"], prefix=prefix, VER=VER)
    )

def slide_html(kicker, inner_html, part_divider=False, extra_class=""):
    cls = "mdeck-slide" + (" part-divider" if part_divider else "") + (" " + extra_class if extra_class else "")
    return f'<div class="{cls}"><div class="kicker">{kicker}</div>{inner_html}</div>'

def build_deck(lang, mod):
    t = L[lang]
    d = mod[lang]
    slides = []
    slides.append(slide_html(
        f"MODULE {mod['num']} · {d['tag']}",
        f"<h2>{d['title']}</h2><p>{d['intro']}</p><p class='pill'>{d['src']}</p>"
    ))
    total_content = 0
    for i, part in enumerate(d["parts"], start=1):
        bullets = "".join(f"<li>{b}</li>" for b in part["bullets"])
        slides.append(slide_html(
            f"{t['part_label']} {i}/5",
            f"<div class='part-num'>{i:02d}</div><h2>{part['title']}</h2><ul class='part-list'>{bullets}</ul>",
            part_divider=True,
        ))
        for cs in part.get("slides", []):
            img_html = ""
            if cs.get("img"):
                src = "../../../assets/figures/" + cs["img"]
                img_html = (f"<figure class='slide-fig'><a href='{src}' target='_blank' rel='noopener'>"
                            f"<img src='{src}' alt='{html.escape(cs['title'], quote=True)}' loading='lazy'/></a>"
                            f"<figcaption>{t['zoom_hint']}</figcaption></figure>")
            explain_html = ""
            if cs.get("explain"):
                explain_html = (f"<details class='slide-explain'><summary>{t['explain_more']}</summary>"
                                f"<div class='slide-explain-body'>{cs['explain']}</div></details>")
            slides.append(slide_html(
                f"{t['part_label']} {i}/5 · {mod['num']}",
                f"<h2>{cs['title']}</h2>{cs['body']}{img_html}{explain_html}",
            ))
            total_content += 1
    legend_items = "".join(f"<li><b>{k}</b><span>{v}</span></li>" for k, v in d["legend"])
    slides.append(slide_html(
        f"{t['part_label']} 2-3 · {t['formula_box']}",
        f"<h2>{d['formula_label']}</h2>"
        f"<div class='pd-formula'><div class='pd-formula-label'>{d['formula_label']}</div>"
        f"<div class='pd-formula-math'>{d['formula_math']}</div></div>"
        f"<ul class='pd-legend'>{legend_items}</ul>"
    ))
    slides.append(slide_html(
        "📜 " + t["history"],
        f"<h2>{d['history_title']}</h2><p>{d['history']}</p>"
    ))
    slides.append(slide_html(
        "🔎 " + t["case"],
        f"<h2>{d['case_title']}</h2><p>{d['case']}</p>"
    ))
    slides.append(slide_html(
        "⚠️ " + t["warn"],
        f"<h2>{d['warn_title']}</h2><p>{d['warn']}</p>"
    ))
    target = mod.get("target_slides")
    if target is not None and len(slides) != target:
        print(f"[SLIDE-COUNT] {mod['slug']} [{lang}]: {len(slides)} slides (target {target})")
    slides_html = "\n".join(slides)
    return f"""<div class="mdeck"><div class="mdeck-viewport">
{slides_html}
</div>
<div class="mdeck-bar">
  <button class="mdeck-prev">{t['prev']}</button><button class="mdeck-next">{t['next']}</button>
  <span class="mdeck-count"></span><div class="mdeck-dots"></div>
  <button class="mdeck-fs">{t['fs']}</button>
</div></div>"""

def build_quiz_section(lang, slug, title, qkey):
    path = os.path.join(QUIZ_DIR, f"{slug}.{lang}.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = data[qkey]
    if not items:
        return ""
    payload = {"items": items}
    js = json.dumps(payload, ensure_ascii=False)
    return f"""<h3>{title}</h3>
<div class="quiz"><script type="application/json">{js}</script></div>"""


def ovl(text):
    out, stack, i = [], [], 0
    while i < len(text):
        if text.startswith("~{", i):
            out.append('<span class="ov">'); stack.append(1); i += 2
        elif text[i] == "}" and stack:
            out.append("</span>"); stack.pop(); i += 1
        else:
            out.append(text[i]); i += 1
    return "".join(out)


def build_essay_section(lang, slug):
    entry = ESSAY.get(slug)
    if not entry:
        return ""
    t = L[lang]
    src_note = entry["src_book"] if lang == "vi" else entry["src_book_en"]
    extra_note = ""
    if entry.get("note_vi") and lang == "vi":
        extra_note = f"<p class='essay-intro'><i>{entry['note_vi']}</i></p>"
    elif entry.get("note_en") and lang == "en":
        extra_note = f"<p class='essay-intro'><i>{entry['note_en']}</i></p>"
    rows = []
    for it in entry["items"]:
        qtext = ovl(it["q_vi"] if lang == "vi" else it["q_en"])
        orig = ""
        if lang == "vi":
            orig = f'<p class="essay-orig"><b>Original (EN):</b> {ovl(it["q_en"])}</p>'
        img_src = "../../../assets/figures/" + it["img"]
        rows.append(f"""<div class="essay-item">
  <p class="essay-q"><b>{it['num']}.</b> {qtext}</p>
  {orig}
  <p class="pill">{it['src']}</p>
  <details class="essay-answer"><summary>{t['essay_reveal']}</summary>
    <div class="essay-answer-body"><img src="{img_src}" alt="{it['src']}" loading="lazy"/></div>
  </details>
</div>""")
    items_html = "\n".join(rows)
    return f"""<h2>{t['essay_title']}</h2>
<p class="essay-intro">{src_note}</p>
{extra_note}
{items_html}"""

def build_module_page(lang, mod, prefix):
    t = L[lang]
    d = mod[lang]
    deck = build_deck(lang, mod)
    quiz_tooley = build_quiz_section(lang, mod["slug"], t["quiz_tooley"], "tooley")
    quiz_floyd = build_quiz_section(lang, mod["slug"], t["quiz_floyd"], "floyd")
    quiz_gen = build_quiz_section(lang, mod["slug"], t["quiz_gen"], "generated")
    essay_section = build_essay_section(lang, mod["slug"])
    nb_name = f"{mod['num']}_{mod['slug'].split('-',1)[1]}.ipynb"
    mod_idx = MODULES.index(mod)
    mrow = MAPPING_ROWS[mod_idx]
    mnote = mrow["note_vi"] if lang == "vi" else mrow["note_en"]
    mapping_href = f"../../../chapter-mapping-{lang}.html"
    mapping_block = f"""<div class="callout info">
<h4>{t['mapping_link']}</h4>
<p><b>Tooley:</b> {mrow['tooley']}</p>
<p><b>Floyd:</b> {mrow.get('floyd_en', mrow['floyd']) if lang == 'en' else mrow['floyd']}</p>
<p>{mnote}</p>
<p><a href="{mapping_href}">{t['nav_mapping']} →</a></p>
</div>"""
    body = f"""<div class="wrap">
<p><a href="../../index.html">{t['back_home']}</a></p>
<div class="hero"><span class="pill">MODULE {mod['num']}</span>
<h1>{d['title']}</h1><p>{d['src']}</p></div>
{mapping_block}
{deck}
<div class="callout history"><h4>{d['history_title']}</h4><p>{d['history']}</p></div>
<div class="callout case"><h4>{d['case_title']}</h4><p>{d['case']}</p></div>
<div class="callout warn"><h4>{d['warn_title']}</h4><p>{d['warn']}</p></div>
<div class="callout good"><h4>{t['notebook']}</h4><p>{d['notebook_desc']}</p>
<p><a class="nb-link" href="../../../data/notebooks/{nb_name}" download>📓 {t['notebook_open']}</a></p></div>
<h2>{t['quiz_title']}</h2>
{quiz_tooley}
{quiz_floyd}
{quiz_gen}
{essay_section}
</div>"""
    extra_css = f'<link rel="stylesheet" href="{prefix}_shared/deck.css?v={VER}"/>'
    html_out = render_page(lang, prefix, body, extra_css=extra_css, title_suffix=d["title"], description=d["intro"])
    html_out = html_out.replace("__OTHER_LANG__", f"../../../{'en' if lang=='vi' else 'vi'}/modules/{mod['slug']}/index.html")
    scripts = f'<script src="{prefix}_shared/deck.js?v={VER}"></script><script src="{prefix}_shared/quiz.js?v={VER}"></script>'
    html_out = html_out.replace("</body></html>", scripts + "</body></html>")
    return html_out

def build_home_page(lang, prefix):
    t = L[lang]
    cards = []
    for mod in MODULES:
        d = mod[lang]
        cards.append(f"""<a class="mod-card" href="modules/{mod['slug']}/index.html">
  <span class="tag">{d['tag']}</span>
  <h3>MODULE {mod['num']}: {d['title']}</h3>
  <p style="color:var(--muted);font-size:.85rem">{d['src']}</p>
  <span class="cta">{t['open']}</span>
</a>""")
    cards_html = "\n".join(cards)
    mapping_href = f"../chapter-mapping-{lang}.html"
    body = f"""<div class="wrap">
<div class="hero"><h1>{t['home_hero_title']}</h1><p>{t['home_hero_sub']}</p>
<p><a href="{mapping_href}">{t['mapping_link']}</a></p></div>
<div class="mod-grid">{cards_html}</div>
</div>"""
    html_out = render_page(lang, prefix, body, title_suffix="", description=t["home_hero_sub"])
    html_out = html_out.replace("__OTHER_LANG__", f"../{'en' if lang=='vi' else 'vi'}/index.html")
    return html_out

def build_mapping_page(lang, prefix):
    t = L[lang]
    rows = []
    for r in MAPPING_ROWS:
        note = r["note_vi"] if lang == "vi" else r["note_en"]
        rows.append(f"""<tr><td><b>{r['module']}</b></td>
<td>{r['tooley']}</td><td>{r.get('floyd_en', r['floyd']) if lang == 'en' else r['floyd']}</td><td>{note}</td></tr>""")
    rows_html = "\n".join(rows)
    head_th = ("Module", "Tooley: Aircraft Digital Electronic and Computer Systems (3rd ed.)",
               "Floyd: Digital Fundamentals (11th ed.)", "Ghi chú đối chiếu") if lang == "vi" else \
              ("Module", "Tooley: Aircraft Digital Electronic and Computer Systems (3rd ed.)",
               "Floyd: Digital Fundamentals (11th ed.)", "Cross-reference note")
    body = f"""<div class="wrap">
<p><a href="{lang}/index.html">{t['back_home']}</a></p>
<div class="hero"><h1>{t['mapping_title']}</h1><p>{t['mapping_intro']}</p></div>
<table class="chapmap">
<thead><tr><th>{head_th[0]}</th><th>{head_th[1]}</th><th>{head_th[2]}</th><th>{head_th[3]}</th></tr></thead>
<tbody>{rows_html}</tbody>
</table>
</div>"""
    html_out = render_page(lang, "", body, title_suffix=t["nav_mapping"], description=t["mapping_intro"])
    html_out = html_out.replace("__OTHER_LANG__", f"chapter-mapping-{'en' if lang=='vi' else 'vi'}.html")
    return html_out

def main():
    for mod in MODULES:
        load_extra_slides(mod)
    for lang in ("vi", "en"):
        home_path = os.path.join(ROOT, lang, "index.html")
        with open(home_path, "w", encoding="utf-8") as f:
            f.write(build_home_page(lang, prefix="../"))
        for mod in MODULES:
            mod_dir = os.path.join(ROOT, lang, "modules", mod["slug"])
            os.makedirs(mod_dir, exist_ok=True)
            with open(os.path.join(mod_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(build_module_page(lang, mod, prefix="../../../"))
    # single shared mapping page (bilingual toggle via two files, simplest: one per lang at root)
    with open(os.path.join(ROOT, "chapter-mapping-vi.html"), "w", encoding="utf-8") as f:
        f.write(build_mapping_page("vi", prefix="./"))
    with open(os.path.join(ROOT, "chapter-mapping-en.html"), "w", encoding="utf-8") as f:
        f.write(build_mapping_page("en", prefix="./"))
    print("Rendered all pages.")

if __name__ == "__main__":
    main()
