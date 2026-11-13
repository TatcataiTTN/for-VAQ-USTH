"""Body of the 'Book map' page (vi / en) of AE2.013.  Static parts (overview, answers, gaps) are built here from data/bookmap/*.json;
the three table-of-contents blocks and the slide list are rendered by _shared/bookmap.js from the same JSON (fetch, with error message and retry).
Data: data/bookmap/{cengel,farokhi,elsayed,slides,ecs_search}.json (build/bookmap/build_map.py), optional data/bookmap/qcount.json."""
import os, json
from hx import esc, callout
from modules import MODS, DECKS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def J(n):
    with open(os.path.join(ROOT, 'data', 'bookmap', n + '.json'), encoding='utf-8') as f: return json.load(f)

def fm(x, vi, nd=1):
    s = f'{x:.{nd}f}'
    return s.replace('.', ',') if vi else s

CH_VI = {1: 'Nhập môn và khái niệm cơ bản', 2: 'Chuyển hoá năng lượng và phân tích năng lượng tổng quát', 3: 'Tính chất của chất tinh khiết', 4: 'Phân tích năng lượng hệ kín',
         5: 'Cân bằng khối lượng và năng lượng cho thể tích kiểm soát', 6: 'Định luật nhiệt động thứ hai', 7: 'Entropi', 8: 'Exergy: thước đo khả năng sinh công', 9: 'Chu trình công suất khí',
         10: 'Chu trình hơi và chu trình kết hợp', 11: 'Chu trình lạnh', 12: 'Các hệ thức tính chất nhiệt động', 13: 'Hỗn hợp khí', 14: 'Hỗn hợp khí–hơi và điều hoà không khí',
         15: 'Phản ứng hoá học', 16: 'Cân bằng hoá học và cân bằng pha', 17: 'Dòng chảy nén được'}
ENDNAME = {'PROBLEMS': ('Bài tập', 'Problems'), 'Review Problems': ('Bài tập ôn', 'Review Problems'), 'Problems': ('Bài tập', 'Problems'),
           'Fundamentals of Engineering (FE) Exam Problems': ('Bài FE', 'FE Exam Problems'), 'Design and Essay Problems': ('Bài thiết kế và tiểu luận', 'Design and Essay Problems'),
           'SUMMARY': ('Tóm tắt', 'Summary'), 'REFERENCES AND SUGGESTED READING': ('Tài liệu tham khảo', 'References and Suggested Reading'), 'References': ('Tài liệu tham khảo', 'References'),
           'Summary': ('Tóm tắt', 'Summary')}
DECK_SHORT = {'ch1': 'Ch.1', 'ch2': 'Ch.2', 'ch3': 'Ch.3', 'ch4': 'Ch.4', 'ch5': 'Ch.5', 'tut': 'Tutorials I'}

def T(vi, en, lang): return vi if lang == 'vi' else en

STYLE = '''<style>
.bm-app{margin:.4em 0}.bm-app *{box-sizing:border-box}
.bm-wrap{overflow-x:auto;max-width:100%;padding:0 6px 8px}
.bm-tbl{border-collapse:collapse;width:100%;font-size:.84rem;min-width:640px}
.bm-tbl th,.bm-tbl td{border-bottom:1px solid var(--border);padding:4px 7px;text-align:left;vertical-align:top}
.bm-tbl th{background:var(--code);position:sticky;top:0}
.bm-tbl td.n{white-space:nowrap}.bm-tbl td.b{font-size:.76rem;color:var(--muted);min-width:200px}
.bm-ov{min-width:760px}.bm-ov td{font-size:.8rem}
.bm-ov a{white-space:nowrap}
tr.bm-chap td{background:var(--code);font-weight:700}
.bm-r{display:inline-block;font-size:.7rem;font-weight:700;padding:1px 7px;border-radius:99px;margin:1px 4px 1px 0;border:1px solid var(--border);white-space:nowrap}
.bm-r.r-core{background:var(--goodbg);color:var(--good);border-color:var(--good)}
.bm-r.r-ref{color:var(--accent2);border:1px dashed var(--accent2)}
.bm-r.r-background{background:var(--code);color:var(--muted)}
.bm-r.r-optional{color:var(--warn);border:1px dotted var(--warn)}
.bm-r.r-out{color:var(--bad);border:1px solid var(--bad);background:var(--badbg)}
.bm-mm{display:block;margin:2px 0}
.bm-bar{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin:.6em 0}
.bm-bar select,.bm-bar input{font:inherit;padding:4px 8px;border:1px solid var(--border);border-radius:8px;background:var(--card);color:var(--text);max-width:100%}
.bm-bar input[type=search]{flex:1 1 180px}
details.bm-bk{border:1px solid var(--border);border-radius:10px;margin:.5em 0;background:var(--card)}
details.bm-bk>summary{cursor:pointer;padding:8px 12px;font-weight:700}
details.bm-bk>summary .srcnote{font-weight:400}
tr.bm-hide{display:none}
.bm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;padding:8px}
.bm-card{border:1px solid var(--border);border-radius:8px;padding:4px;font-size:.76rem;background:var(--card)}
.bm-card a{display:block}.bm-card img{width:100%;height:auto;display:block;border:1px solid var(--border);background:#fff;border-radius:4px;aspect-ratio:4/3;object-fit:contain}
.bm-card.bm-hide{display:none}.bm-card.k-blank img{opacity:.45}
.bm-noq .bm-qc{display:none}
.bm-err{border:1px solid var(--bad);background:var(--badbg);padding:8px 12px;border-radius:8px}
.bm-ans tr.hl td{background:var(--goodbg)}
.bm-lg{list-style:none;padding-left:0}.bm-lg li{margin:.25em 0}
</style>'''

def count_slides(S, mid): return sum(1 for d in S.values() for x in d['slides'] if x['module'] == mid and x['kind'] == 'content')

def slide_cell(m, S, lang):
    vi = lang == 'vi'; pre = T('tr.', 'p.', lang); parts = []
    for d, a, b in m['slides']:
        parts.append(f'{DECK_SHORT[d]} {pre}{a}–{b}' if b > a else f'{DECK_SHORT[d]} {pre}{a}')
    n = count_slides(S, m['id'])
    return '<br>'.join(parts) + f'<br><span class="srcnote">{n} ' + T('slide nội dung', 'content slides', lang) + '</span>'

def rng(a, b): return f'{a}–{b}' if b > a else f'{a}'

def cengel_cell(C, mid, lang):
    vi = lang == 'vi'; pre = T('tr. in', 'printed p.', lang); out = []; off = C['offset']
    for role in ('core', 'ref'):
        lines = []
        for ch in C['chapters']:
            secs = [s for s in ch['sections'] if s['mods'].get(mid, {}).get('role') == role]
            ends = [e for e in ch['end_parts'] if e['mods'].get(mid, {}).get('role') == role]
            if role == 'ref' and out: continue
            if role == 'ref':
                if secs and not any(s['mods'].get(mid, {}).get('role') == 'core' for c2 in C['chapters'] for s in c2['sections']): pass
                else: continue
            if not secs and not ends: continue
            txt = ''
            if secs:
                nums = [s['num'] for s in secs]; lab = nums[0] if len(nums) == 1 else f'{nums[0]}…{nums[-1]}' if len(nums) > 3 else ', '.join(nums)
                lo = min(s['printed'] for s in secs); hi = max(s['pdf_end'] for s in secs) - off
                txt = f'<a href="#bm-cengel-{ch["num"]}">Ch.{ch["num"]} §{lab}</a> · {pre} {rng(lo, hi)} · PDF {rng(min(s["pdf"] for s in secs), max(s["pdf_end"] for s in secs))}'
            for e in ends:
                nm = ENDNAME.get(e['name'], (e['name'], e['name']))[0 if vi else 1]
                txt += (' · ' if txt else f'Ch.{ch["num"]} ') + f'{nm} {T("tr.", "p.", lang)}{e["printed"]} (PDF {e["pdf"]})'
            lines.append(txt)
        if lines:
            out.append(('<i>' + T('đọc thêm (ref):', 'reference (ref):', lang) + '</i> ' if role == 'ref' else '') + '<br>'.join(lines))
    return '<br>'.join(out) or '–'

def farokhi_cell(F, mid, lang):
    pre = T('tr. in', 'printed p.', lang); out = []
    ents = [e for e in F['entries'] if e['mods'].get(mid, {}).get('role') == 'core' and e['kind'] in ('section', 'endpart', 'appendix', 'chapter')]
    role = 'core'
    if not ents:
        ents = [e for e in F['entries'] if e['mods'].get(mid, {}).get('role') == 'ref' and e['kind'] in ('section', 'endpart', 'appendix', 'chapter')]; role = 'ref'
    if not ents: return None
    byc = {}
    for e in ents: byc.setdefault(e['chapter'], []).append(e)
    for c, es in byc.items():
        ss = [e for e in es if e['kind'] == 'section']; others = [e for e in es if e['kind'] != 'section']
        if not ss and others and all(e['kind'] == 'chapter' for e in others): ss = others; others = []
        txt = ''
        if ss:
            nums = [e['num'] for e in ss]; lab = ', '.join(nums) if len(nums) <= 3 else f'{nums[0]}…{nums[-1]}'
            lo = min(e['printed'] for e in ss if e['printed']); hi = max(e['pdf_end'] for e in ss) - F['offset']
            txt = f'<a href="#bm-farokhi-{ss[0]["i"]}">{"Ch." if str(c).isdigit() else ""}{c} §{lab}</a> · {pre} {rng(lo, hi)} · PDF {rng(min(e["pdf"] for e in ss), max(e["pdf_end"] for e in ss))}'
        for e in others:
            nm = ENDNAME.get(e['title'], (e['title'], e['title']))[0 if lang == 'vi' else 1] if e['kind'] == 'endpart' else f'{e["num"]} {e["title"]}'
            txt += (' · ' if txt else f'{"Ch." if str(c).isdigit() else ""}{c} ') + f'{nm} {T("tr.", "p.", lang)}{e["printed"]} (PDF {e["pdf"]})'
        out.append(txt)
    return ('<i>' + T('đọc thêm (ref):', 'reference (ref):', lang) + '</i><br>' if role == 'ref' else '') + '<br>'.join(out)

def elsayed_cell(E, mid, lang):
    out = []; pre = T('tr.', 'p.', lang)
    es = [e for e in E['entries'] if e['mods'].get(mid, {}).get('role') == 'core' and (e['kind'] == 'endpart' or e['depth'] <= 2)]
    role = 'core'
    if not es:
        es = [e for e in E['entries'] if e['mods'].get(mid, {}).get('role') == 'ref' and (e['kind'] == 'endpart' or e['depth'] <= 2)]; role = 'ref'
    if not es: return None
    byc = {}
    for e in es: byc.setdefault(e['chapter'], []).append(e)
    for c, l in byc.items():
        parts = [f'§{e["num"]} ({pre}{e["printed"]})' if e['num'] else f'{ENDNAME.get(e["title"], (e["title"], e["title"]))[0 if lang == "vi" else 1]} ({pre}{e["printed"]})' for e in l]
        out.append(f'<a href="#bm-elsayed-{l[0]["chapter"]}">Ch.{c}</a> ' + ', '.join(parts))
    return ('<i>' + T('đọc thêm (ref):', 'reference (ref):', lang) + '</i><br>' if role == 'ref' else '') + '<br>'.join(out)

def overview(lang, C, F, E, S):
    vi = lang == 'vi'; rows = []
    none = f'<a href="#gaps">{T("không có mục về ECS/cooling pack", "no section on ECS/cooling pack", lang)}</a>'
    for m in MODS:
        fc, ec = farokhi_cell(F, m['id'], lang), elsayed_cell(E, m['id'], lang)
        rows.append('<tr><td><b>' + m['id'] + '</b> ' + esc(m[lang]) + '</td><td>' + slide_cell(m, S, lang) + '</td><td>' + cengel_cell(C, m['id'], lang) + '</td><td>' + (fc or (none if m['id'] == 'm03' else '–')) + '</td><td>' + (ec or (none if m['id'] == 'm03' else '–')) + '</td></tr>')
    head = ['Module', T('Slide của giảng viên', "Lecturer's slides", lang), 'Cengel &amp; Boles', 'Farokhi', 'El-Sayed']
    return '<div class="bm-wrap"><table class="bm-tbl bm-ov"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'

def answers(lang, C, F, E):
    vi = lang == 'vi'; pc = C['answers']['per_chapter']; tp = sum(v['problems'] for v in pc.values()); ta = sum(v['with_answer'] for v in pc.values())
    mod_of = {9: 'm02', 11: 'm03', 14: 'm03', 15: 'm04', 17: 'm05'}
    rows = []
    for n in range(1, 18):
        v = pc[str(n)]; hl = n in mod_of
        rows.append(f'<tr class="{"hl" if hl else ""}"><td><b>Ch.{n}</b> {esc(CH_VI[n]) if vi else ""}{"" if vi else esc(C["chapters"][n - 1]["title"])}</td><td>{v["problems"]}</td><td>{v["with_answer"]}</td>'
                    f'<td>{fm(100 * v["with_answer"] / v["problems"], vi)} %</td><td>{mod_of.get(n, "–")}</td></tr>')
    rows.append(f'<tr><td><b>{T("Cộng", "Total", lang)}</b></td><td><b>{tp}</b></td><td><b>{ta}</b></td><td><b>{fm(100 * ta / tp, vi)} %</b></td><td></td></tr>')
    head = [T('Chương', 'Chapter', lang), T('Số bài', 'Problems', lang), T('Có đáp án in', 'With printed answer', lang), T('Tỉ lệ', 'Share', lang), T('Module môn học', 'Course module', lang)]
    tbl = '<div class="bm-wrap"><table class="bm-tbl bm-ans" style="min-width:520px"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
    b = C['back']
    ul = ('<ul>'
          f'<li>{T("<b>Cengel &amp; Boles</b> in đáp án ngay sau đề bài, dạng “Answers: …”, chỉ với một số bài: " + str(ta) + "/" + str(tp) + " bài (" + fm(100 * ta / tp, vi) + " %). Bài loại C (câu hỏi khái niệm) không có đáp án số.", "<b>Cengel &amp; Boles</b> prints answers right after the problem statement, as “Answers: …”, for some problems only: " + str(ta) + "/" + str(tp) + " (" + fm(100 * ta / tp, vi) + " %). Problems marked C (concept questions) have no numeric answer.", lang)}</li>'
          f'<li>{T("Các chương của môn học: Ch.9 " + str(pc["9"]["with_answer"]) + "/" + str(pc["9"]["problems"]) + ", Ch.11 " + str(pc["11"]["with_answer"]) + "/" + str(pc["11"]["problems"]) + ", Ch.14 " + str(pc["14"]["with_answer"]) + "/" + str(pc["14"]["problems"]) + ", Ch.15 " + str(pc["15"]["with_answer"]) + "/" + str(pc["15"]["problems"]) + ", Ch.17 " + str(pc["17"]["with_answer"]) + "/" + str(pc["17"]["problems"]) + " (dòng tô nền ở bảng).", "Chapters of this course: Ch.9 " + str(pc["9"]["with_answer"]) + "/" + str(pc["9"]["problems"]) + ", Ch.11 " + str(pc["11"]["with_answer"]) + "/" + str(pc["11"]["problems"]) + ", Ch.14 " + str(pc["14"]["with_answer"]) + "/" + str(pc["14"]["problems"]) + ", Ch.15 " + str(pc["15"]["with_answer"]) + "/" + str(pc["15"]["problems"]) + ", Ch.17 " + str(pc["17"]["with_answer"]) + "/" + str(pc["17"]["problems"]) + " (shaded rows).", lang)}</li>'
          f'<li>{T("Cengel <b>không có</b> phụ lục “Answers to selected problems”: file PDF dừng ở trang PDF " + str(b["last_chapter_pdf"]) + " (trang in " + str(b["last_chapter_pdf"] - C["offset"]) + "), giữa phần bài FE của Ch.17; Glossary bắt đầu ở PDF " + str(b["glossary_pdf"]) + ".", "Cengel has <b>no</b> “Answers to selected problems” appendix: the PDF stops at PDF page " + str(b["last_chapter_pdf"]) + " (printed " + str(b["last_chapter_pdf"] - C["offset"]) + "), in the middle of the Ch.17 FE problems; the Glossary starts at PDF " + str(b["glossary_pdf"]) + ".", lang)}</li>'
          f'<li>{T("<b>Farokhi</b> và <b>El-Sayed</b> không in đáp án (không có đáp án bài tập chương, không có phụ lục đáp án; Farokhi cũng không in đáp án cho " + str(F["back"]["quizzes"]) + " câu Quiz ở Appendix K).", "<b>Farokhi</b> and <b>El-Sayed</b> print no answers (no answers to the chapter problems, no answer appendix; Farokhi also prints none for its " + str(F["back"]["quizzes"]) + " Appendix K quizzes).", lang)}</li></ul>')
    note = (f'<p class="srcnote">{T("Ghi chú: tổng theo từng chương là " + str(ta) + "; trường back.answers_total của dữ liệu ghi " + str(b["answers_total"]) + " (khác " + str(b["answers_total"] - ta) + ": chưa rõ nguyên nhân, dùng số theo chương).", "Note: the per-chapter total is " + str(ta) + "; the back.answers_total field of the data says " + str(b["answers_total"]) + " (difference " + str(b["answers_total"] - ta) + ", cause not determined; the per-chapter figure is used).", lang)}</p>')
    return ul + tbl + note

def gaps(lang, S, ECS):
    vi = lang == 'vi'; sl = [x for x in S['ch3']['slides'] if 29 <= x['page'] <= 36]
    titles = '; '.join(f'tr.{x["page"]} “{esc(x["title"])}”' if vi else f'p.{x["page"]} “{esc(x["title"])}”' for x in sl[:3]) + ' …'
    h = '<h3>' + T('ECS / cooling pack: không sách nào có', 'ECS / cooling pack: no book has it', lang) + '</h3><ul>'
    h += f'<li>{T("Slide Ch.3 tr.29–36 (" + titles + ") <b>không có đối ứng</b> trong Cengel, Farokhi và El-Sayed.", "Slide Ch.3 p.29–36 (" + titles + ") has <b>no counterpart</b> in Cengel, Farokhi or El-Sayed.", lang)}</li>'
    h += f'<li><b>Farokhi</b>: {T("tìm theo các từ khoá air conditioning, ECS, cooling pack, air cycle, customer bleed, cabin, refrigeration: không có mục nào. Chỉ có tăng áp thùng nhiên liệu tên lửa (Ch.12), khí trích làm mát tuabin và hút lớp biên ở cửa hút: không phải khí cho cabin.", "searched for air conditioning, ECS, cooling pack, air cycle, customer bleed, cabin, refrigeration: no section. Only rocket propellant-tank pressurisation (Ch.12), turbine-cooling bleed and inlet boundary-layer bleed turn up, none of them cabin air.", lang)}</li>'
    hits = ECS['elsayed']['hits']
    h += f'<li><b>El-Sayed</b>: {T("chỉ có vài câu nhắc thoáng, không mô tả ECS, máy chu trình khí hay cooling pack: " + "; ".join("tr.in " + str(x["printed"]) + " (Ch." + str(x["chapter"]) + ")" for x in hits) + ". Câu ở tr.in " + str(hits[0]["printed"]) + " chỉ nói khí trích “có ứng dụng cho điều hoà không khí cabin”, và nằm ngoài các chương trong phạm vi.", "only passing mentions, no description of an ECS, air cycle machine or cooling pack: " + "; ".join("printed p." + str(x["printed"]) + " (Ch." + str(x["chapter"]) + ")" for x in hits) + ". The sentence on printed p." + str(hits[0]["printed"]) + " only says bleed “has its applications for cabin-air conditioning” and lies outside the scope chapters.", lang)}</li>'
    h += f'<li>{T("Mục gần nhất: <b>Cengel §11-8 Gas Refrigeration Cycles</b> (chu trình Brayton ngược, tr.in 628, PDF 654), cộng Cengel Ch.14 §14-7 (các quá trình điều hoà không khí). Sách không mô tả cooling pack trên tàu bay, nên module m03 phần này chỉ dựa vào slide.", "Nearest section: <b>Cengel §11-8 Gas Refrigeration Cycles</b> (reversed Brayton cycle, printed p.628, PDF 654), plus Cengel Ch.14 §14-7 (air-conditioning processes). No book describes the aircraft cooling pack, so this part of m03 rests on the slides alone.", lang)}</li></ul>'
    h += '<h3>' + T('Lệch mục lục tìm thấy', 'Table-of-contents discrepancies found', lang) + '</h3><ul>'
    h += f'<li>{T("Cengel, trang Contents (PDF 2–17) đánh số lệch ở Ch.6: bỏ qua 6–4, nên các mục 6–5…6–12 ở Contents tương ứng 6–4…6–11 trong thân sách (mục cuối “The Carnot Refrigerator and Heat Pump” là 6–11 ở tr.in 309, PDF 335). Bản đồ dùng số trong thân sách.", "Cengel, the Contents pages (PDF 2–17) number Ch.6 off by one: 6–4 is skipped, so entries 6–5…6–12 in the Contents are 6–4…6–11 in the body (the last, “The Carnot Refrigerator and Heat Pump”, is 6–11 at printed p.309, PDF 335). The map uses the body numbers.", lang)}</li>'
    h += f'<li>{T("Cengel Ch.12: mục 12–4 “General Relations” có trong thân sách (tr.in 661, PDF 687) nhưng thiếu ở Contents; tên lấy từ tiêu đề thân sách.", "Cengel Ch.12: section 12–4 “General Relations” is in the body (printed p.661, PDF 687) but missing from the Contents; its title comes from the body heading.", lang)}</li>'
    h += f'<li>{T("Cengel: một số tên mục trong Contents khác chữ hoa/thường hoặc khoảng trắng so với thân sách (ví dụ “Brayton Cycle:  The Ideal…”); bản đồ dùng tên trong Contents.", "Cengel: some section names in the Contents differ in capitalisation or spacing from the body (for example “Brayton Cycle:  The Ideal…”); the map uses the Contents names.", lang)}</li>'
    h += f'<li>{T("El-Sayed: dấu ⟦p.N⟧ trong bản chữ OCR đôi khi trễ vài dòng so với dấu ngắt trang của EPUB; bản đồ dùng dấu ngắt trang trong xhtml (khớp 230/230 mục).", "El-Sayed: the ⟦p.N⟧ marks in the OCR text sometimes lag a few lines behind the EPUB page-break marks; the map uses the page breaks in the xhtml (230/230 entries match).", lang)}</li></ul>'
    return h

def body(lang):
    C, F, E, S, ECS = J('cengel'), J('farokhi'), J('elsayed'), J('slides'), J('ecs_search')
    vi = lang == 'vi'; t = lambda a, b: T(a, b, lang)
    nsl = sum(len(d['slides']) for d in S.values())
    h = STYLE + f'<h1>{t("Bản đồ sách", "Book map")}</h1>'
    h += f'<p class="lead">{t("Nội dung của ba sách và bộ slide của giảng viên được đặt cạnh nhau: module nào dùng mục nào, ở trang nào, với vai trò gì. Dùng để tra nhanh “phần này nằm ở đâu trong sách”.", "The three textbooks and the lecturer slides side by side: which module uses which section, on which page, and in what role. Use it to find where a topic sits in the books.")}</p>'
    h += '<div class="bm-bar" id="bm-filters">' + \
         f'<label>{t("Module", "Module")}: <select id="bm-mod"><option value="">{t("Tất cả module", "All modules")}</option>' + ''.join(f'<option value="{m["id"]}">{m["id"]} · {esc(m[lang])}</option>' for m in MODS) + '</select></label>' + \
         f'<label>{t("Vai trò", "Role")}: <select id="bm-role"><option value="">{t("Tất cả vai trò", "All roles")}</option>' + ''.join(f'<option value="{k}">{k} · {v}</option>' for k, v in (('core', t('lõi', 'core')), ('ref', t('đọc thêm', 'reference')), ('background', t('nền', 'background')), ('optional', t('tùy chọn', 'optional')), ('out', t('ngoài phạm vi', 'out of scope')))) + '</select></label>' + \
         f'<input type="search" id="bm-q" placeholder="{t("Tìm tên mục…", "Search section title…")}" aria-label="{t("Tìm tên mục", "Search section title")}"> <button type="button" id="bm-reset">{t("Xoá lọc", "Clear filters")}</button> <span id="bm-none" hidden>{t("Không có mục nào khớp.", "No entry matches.")}</span></div>'
    h += f'<p class="srcnote">{t("Bộ lọc áp dụng cho ba khối sách và danh sách slide; lựa chọn được lưu trong địa chỉ trang (phần sau dấu #).", "Filters apply to the three book blocks and the slide list; the choice is kept in the page address (after the #).")}</p>'
    h += f'<h2 id="overview">{t("Tổng quan: module × nguồn", "Overview: module × source")}</h2>'
    h += callout('info', t('Trang in và trang PDF', 'Printed page and PDF page'),
                 '<ul>' + f'<li>{t("<b>Cengel &amp; Boles</b> (PDF 963 tr.): trang in = trang PDF − 26 (PDF 27–907). Đo trên 349 trang đọc được số in, đều lệch 26; 7 mốc: PDF 44 = in 18, 183 = 157, 337 = 311, 488 = 462, 623 = 597, 763 = 737, 907 = 881; 10 tiêu đề mục kiểm bằng ảnh. Glossary (PDF 909–963) đánh số riêng: in = PDF − 908.", "<b>Cengel &amp; Boles</b> (963-page PDF): printed page = PDF page − 26 (PDF 27–907). Measured on 349 pages with a readable printed number, all offset by 26; 7 landmarks: PDF 44 = printed 18, 183 = 157, 337 = 311, 488 = 462, 623 = 597, 763 = 737, 907 = 881; 10 section headings checked on the page image. The Glossary (PDF 909–963) is numbered separately: printed = PDF − 908.")}</li>'
                 f'<li>{t("<b>Farokhi</b> (PDF 1048 tr.): trang in = trang PDF − 34 (PDF 36–1031). Đo trên 962 trang, đều lệch 34; 7 mốc: PDF 36 = in 2, 199 = 165, 364 = 330, 526 = 492, 689 = 655, 853 = 819, 1031 = 997.", "<b>Farokhi</b> (1048-page PDF): printed page = PDF page − 34 (PDF 36–1031). Measured on 962 pages, all offset by 34; 7 landmarks: PDF 36 = printed 2, 199 = 165, 364 = 330, 526 = 492, 689 = 655, 853 = 819, 1031 = 997.")}</li>'
                 f'<li>{t("<b>El-Sayed</b> (EPUB, không có PDF): chỉ có trang in, lấy từ dấu ngắt trang của EPUB; 230/230 mục trong phạm vi khớp giữa mục lục và dấu ngắt trang.", "<b>El-Sayed</b> (EPUB, no PDF): printed page only, taken from the EPUB page-break marks; 230/230 in-scope entries agree between the table of contents and the page breaks.")}</li>'
                 f'<li>{t("Bảng dưới chỉ liệt kê mục có vai trò <b>lõi</b> (core) của module; module chưa có mục lõi thì ghi <i>đọc thêm</i> hoặc “–”. Cột sách có tr. in (số in trên trang) và PDF (số trang trong file). Bấm số chương để nhảy tới khối sách.", "The table lists only sections with the <b>core</b> role for the module; where a module has none it shows <i>reference</i> items or “–”. Book columns give printed p. (the number on the page) and PDF (the page in the file). Click a chapter to jump to the book block.")}</li></ul>')
    h += overview(lang, C, F, E, S)
    leg = ''.join(f'<li><span class="bm-r r-{k}">{g} {n}</span> {d}</li>' for k, g, n, d in (
        ('core', '●', t('lõi', 'core'), t('bài giảng và câu hỏi lấy từ đây', 'lessons and questions are built from here')),
        ('ref', '◐', t('đọc thêm', 'reference'), t('đọc thêm, sâu hơn slide, chưa trích', 'further reading, deeper than the slides, not quoted')),
        ('background', '○', t('nền', 'background'), t('kiến thức nền từ học phần AE1.030', 'prerequisite knowledge from AE1.030')),
        ('optional', '◌', t('tùy chọn', 'optional'), t('phần phụ, không dùng trong bài giảng', 'side material, not used in the lessons')),
        ('out', '✕', t('ngoài phạm vi', 'out of scope'), t('không module nào dùng', 'no module uses it'))))
    h += f'<details class="bm-bk"><summary>{t("Chú giải vai trò", "Role legend")}</summary><ul class="bm-lg">{leg}</ul></details>'
    h += f'<h2 id="books">{t("Mục lục từng sách", "Table of contents of each book")}</h2><div id="bm-app" class="bm-app bm-noq" data-root="{{R}}" data-lang="{lang}"><p class="muted">{t("Đang tải dữ liệu…", "Loading data…")}</p></div>'
    h += f'<noscript><p class="bm-err">{t("Cần bật JavaScript để xem các mục lục.", "JavaScript is needed to show the tables of contents.")}</p></noscript>'
    h += f'<h2 id="answers">{t("Đáp án in và bài tập", "Printed answers and problems")}</h2>' + answers(lang, C, F, E)
    h += f'<h2 id="gaps">{t("Điều sách không có", "What the books do not have")}</h2>' + gaps(lang, S, ECS)
    return h
