#!/usr/bin/env python3
"""Convert the Mechanics II .tex/.md source files into HTML fragments for the static site.
No answers are invented here -- this only reformats LaTeX/Markdown we already authored and
verified against the source textbooks. Math delimiters ($ ... $ and \\[ ... \\]) are left as-is
for KaTeX auto-render to pick up in the browser.
"""
import re, os, sys, html, json

SRC_TEX_DIR = "/Users/tuannghiat/Downloads/USTH - Mechanics /Mechanics 2/Mechanics_II_USTH/Exam_Practice"
SRC_MD_DIR = "/Users/tuannghiat/Downloads/USTH - Mechanics /Mechanics 2/Mechanics_II_USTH/Reading_Notes"
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"

def get_title(tex):
    m = re.search(r"\\title\{(.*?)\}\s*\\author", tex, re.S)
    if not m:
        return ""
    t = m.group(1)
    # take the \Huge\textbf{...} main line and the \Large line as subtitle
    lines = re.findall(r"\\(?:Huge|huge|Large|large|normalsize|small)\\textbf\{(.*?)\}|\\(?:Large|large|normalsize|small)\s+([^\\]+?)(?:\\\\|\Z)", t)
    parts = []
    for a,b in lines:
        parts.append(a or b)
    if not parts:
        # fallback: strip all latex sizing commands
        parts=[re.sub(r"\\\w+", " ", t)]
    title = " — ".join(p.strip() for p in parts if p.strip())
    title = title.replace(r"\&", "&").replace("---", "—").replace("--", "–")
    return title

MATH_RE = re.compile(r"(\\\[.*?\\\]|\$[^$]*\$)", re.S)

def tex_inline_to_html(s):
    # Protect math spans ($...$ and \[...\]) from text-mode substitutions --
    # KaTeX needs the raw LaTeX untouched inside them.
    protected = []
    def stash(m):
        protected.append(m.group(1))
        return f"\x00MATH{len(protected)-1}\x00"
    s = MATH_RE.sub(stash, s)

    s = re.sub(r"\\textbf\{(.*?)\}", r"<strong>\1</strong>", s, flags=re.S)
    s = re.sub(r"\\textit\{(.*?)\}", r"<em>\1</em>", s, flags=re.S)
    s = re.sub(r"\\texttt\{(.*?)\}", r"<code>\1</code>", s, flags=re.S)
    s = re.sub(r"\\hrulefill", "<hr class='mini'/>", s)
    s = re.sub(r"\\newpage", "", s)
    s = s.replace(r"\%", "%")
    s = s.replace(r"\_", "_")
    s = s.replace("---", "—").replace("--", "–")
    s = re.sub(r"\\quad", " &nbsp; ", s)

    for i, m in enumerate(protected):
        s = s.replace(f"\x00MATH{i}\x00", m)
    return s

def convert_table(block):
    """Convert a \\begin{tabular}{...} ... \\end{tabular} block to an HTML table."""
    body = re.search(r"\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}", block, re.S)
    if not body:
        return block
    rows_src = body.group(1)
    rows_src = rows_src.replace(r"\hline", "")
    rows = [r.strip() for r in rows_src.split(r"\\") if r.strip()]
    html_rows = []
    for r in rows:
        cells = [c.strip() for c in r.split("&")]
        cells_html = "".join(f"<td>{tex_inline_to_html(c)}</td>" for c in cells)
        html_rows.append(f"<tr>{cells_html}</tr>")
    return "<table class='answer-table'>" + "".join(html_rows) + "</table>"

def convert_body(tex):
    # cut everything up to \begin{document} ... first real content
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", tex, re.S)
    body = m.group(1) if m else tex
    # drop \maketitle...\tableofcontents\newpage boilerplate
    body = re.sub(r"\\maketitle.*?\\newpage", "", body, flags=re.S)
    body = re.sub(r"\\thispagestyle\{empty\}", "", body)

    out = []
    pos = 0
    # tokenize top-level constructs in order of appearance
    pattern = re.compile(
        r"\\section\{(?P<sec>.*?)\}|"
        r"\\subsection\*?\{(?P<sub>.*?)\}|"
        r"\\begin\{(?P<envname>problembox|solutionbox|notebox)\}(?:\[(?P<envtitle>.*?)\])?(?P<envbody>.*?)\\end\{(?P=envname)\}|"
        r"\\begin\{center\}(?P<tbl>.*?)\\end\{center\}",
        re.S)
    for mm in pattern.finditer(body):
        if mm.start() > pos:
            gap = body[pos:mm.start()].strip()
            if gap and not gap.startswith('%'):
                out.append(f"<p>{tex_inline_to_html(gap)}</p>")
        if mm.group('sec') is not None:
            out.append(f"<h2>{tex_inline_to_html(mm.group('sec'))}</h2>")
        elif mm.group('sub') is not None:
            out.append(f"<h3>{tex_inline_to_html(mm.group('sub'))}</h3>")
        elif mm.group('envname'):
            cls = {"problembox":"problem","solutionbox":"solution","notebox":"note"}[mm.group('envname')]
            title = mm.group('envtitle') or {"problembox":"Đề bài","solutionbox":"Lời giải","notebox":"Ghi chú"}[mm.group('envname')]
            inner = mm.group('envbody')
            out.append(f"<div class='box {cls}'><div class='box-title'>{tex_inline_to_html(title)}</div><div class='box-body'>{tex_inline_to_html(inner)}</div></div>")
        elif mm.group('tbl') is not None:
            out.append(convert_table(mm.group('tbl')))
        pos = mm.end()
    tail = body[pos:].strip()
    if tail and not tail.startswith('%'):
        out.append(f"<p>{tex_inline_to_html(tail)}</p>")
    return "\n".join(out)

def process_tex_file(path):
    tex = open(path, encoding="utf-8").read()
    title = get_title(tex)
    body_html = convert_body(tex)
    return {"title": title, "html": body_html}

SUB_RE = r"(_[A-Za-z0-9]+)?"

def fix_combining_marks(text):
    """The reading notes use Unicode combining marks (vector arrow, dot-above for time
    derivative, circumflex for unit vectors) directly on letters -- most fonts render these
    as tofu boxes instead of a proper diacritic. Convert each occurrence into a small KaTeX
    math snippet ($\\vec{F}_{net}$ etc.) instead, which renders correctly in every browser."""
    def wrap(macro):
        def repl(m):
            base, sub = m.group(1), m.group(2)
            sub_tex = "_{" + sub[1:] + "}" if sub else ""
            return f"${macro}{{{base}}}{sub_tex}$"
        return repl
    text = re.sub(r"([A-Za-zΑ-Ωα-ω])⃗" + SUB_RE, wrap(r"\\vec"), text)
    text = re.sub(r"([A-Za-zΑ-Ωα-ω])̇" + SUB_RE, wrap(r"\\dot"), text)
    text = re.sub(r"([A-Za-zΑ-Ωα-ω])̂" + SUB_RE, wrap(r"\\hat"), text)
    return text

def process_md_file(path):
    import markdown as md
    text = open(path, encoding="utf-8").read()
    text = fix_combining_marks(text)
    # first line "# ..." as title
    lines = text.splitlines()
    title = lines[0].lstrip("#").strip() if lines and lines[0].startswith("#") else os.path.basename(path)
    body = "\n".join(lines[1:])
    html_body = md.markdown(body, extensions=["tables", "fenced_code"])
    return {"title": title, "html": html_body}

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = {"tex": [], "md": []}
    for fn in sorted(os.listdir(SRC_TEX_DIR)):
        if fn.endswith(".tex"):
            rec = process_tex_file(os.path.join(SRC_TEX_DIR, fn))
            slug = fn[:-4]
            json.dump(rec, open(f"{OUT_DIR}/{slug}.json","w"), ensure_ascii=False)
            manifest["tex"].append({"slug": slug, "title": rec["title"]})
            print("tex:", slug, "->", rec["title"])
    for fn in sorted(os.listdir(SRC_MD_DIR)):
        if fn.endswith(".md") and "Master_Exercise_List" not in fn:
            rec = process_md_file(os.path.join(SRC_MD_DIR, fn))
            slug = fn[:-3]
            json.dump(rec, open(f"{OUT_DIR}/{slug}.json","w"), ensure_ascii=False)
            manifest["md"].append({"slug": slug, "title": rec["title"]})
            print("md:", slug, "->", rec["title"])
    json.dump(manifest, open(f"{OUT_DIR}/manifest.json","w"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
