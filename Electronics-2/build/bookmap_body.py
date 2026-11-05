"""Body of the 'Book content map' page (vi / en): module -> book overview, then the real table of contents of every book with page numbers,
the modules that use each section and how many questions are anchored to it.  Data: data/bookmap/map.json (build/bookmap/build_map.py)."""
import os, json
from hx import esc, callout, ul
from modules import MODS, BOOKS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def data(): return json.load(open(os.path.join(ROOT, 'data', 'bookmap', 'map.json'), encoding='utf-8'))

ROLE = {
 'core': dict(vi='Nội dung chính: bài giảng và/hoặc câu hỏi lấy từ mục này', en='Core: the lesson and/or the questions are built from this section'),
 'lab': dict(vi='Dùng cho phần thực hành servo (m10)', en='Used for the servomotor lab (m10)'),
 'ref': dict(vi='Đọc thêm theo đề cương: đã ánh xạ, CHƯA trích câu hỏi', en='Reading reference from the syllabus map: mapped, NOT quoted'),
 'cited': dict(vi='Câu hỏi/bài giảng có nhắc tới mục này', en='Questions or lesson mention this section'),
 'optional': dict(vi='Phần phụ của chương (Application Activity, Programmable Analog Technology): không dùng trong bài giảng', en='Chapter feature (Application Activity, Programmable Analog Technology): not used by the lessons'),
}
STATUS = {'background': dict(vi='nền tảng (thiết bị rời, học phần trước)', en='background (discrete-device theory, previous course)', svi='nền tảng', sen='background'),
          'other': dict(vi='cùng chương, sâu hơn yêu cầu', en='same chapter, deeper than required', svi='sâu hơn', sen='deeper'),
          'out': dict(vi='ngoài đề cương', en='outside the syllabus', svi='ngoài đề cương', sen='outside syllabus')}
def stl(st, lang): return f'<span class="bm-st st-{st}" title="{esc(STATUS[st][lang])}">{STATUS[st]["s" + lang]}</span>'
VI_FLOYD = {1: 'Nhập môn điện tử', 2: 'Điốt và ứng dụng', 3: 'Điốt chuyên dụng', 4: 'Transistor lưỡng cực (BJT)', 5: 'Mạch phân cực transistor', 6: 'Bộ khuếch đại BJT',
            7: 'Bộ khuếch đại công suất', 8: 'Transistor hiệu ứng trường (FET)', 9: 'Khuếch đại FET và mạch chuyển mạch', 10: 'Đáp ứng tần số của bộ khuếch đại', 11: 'Thyristor',
            12: 'Bộ khuếch đại thuật toán', 13: 'Mạch op-amp cơ bản', 14: 'Mạch op-amp chuyên dụng', 15: 'Bộ lọc tích cực', 16: 'Mạch dao động', 17: 'Bộ ổn áp',
            18: 'Khái niệm lập trình cơ bản cho kiểm thử tự động'}
VI_JAEGER = {1: 'Nhập môn điện tử', 2: 'Điện tử chất rắn', 3: 'Điốt bán dẫn và mạch điốt', 4: 'Transistor hiệu ứng trường', 5: 'Transistor lưỡng cực', 6: 'Nhập môn điện tử số',
             7: 'Thiết kế logic CMOS', 8: 'Mạch nhớ MOS', 9: 'Mạch logic lưỡng cực', 10: 'Hệ tương tự và op-amp lý tưởng', 11: 'Op-amp thực và ổn định bộ khuếch đại hồi tiếp',
             12: 'Ứng dụng op-amp', 13: 'Mô hình tín hiệu nhỏ và khuếch đại tuyến tính', 14: 'Bộ khuếch đại một transistor', 15: 'Khuếch đại vi sai và thiết kế op-amp',
             16: 'Kỹ thuật thiết kế IC tương tự', 17: 'Đáp ứng tần số bộ khuếch đại', 18: 'Khuếch đại hồi tiếp dùng transistor và mạch dao động'}
VI_SERVO = {1: 'Synchro', 2: 'Resolver', 3: 'Hệ servo'}
VI_FEAT = {'Application Activity': 'Hoạt động ứng dụng', 'Programmable Analog Technology': 'Công nghệ tương tự lập trình được'}
VI_END = {'SUMMARY': 'Tóm tắt', 'KEY TERMS': 'Thuật ngữ', 'KEY FORMULAS': 'Công thức chính', 'TRUE/FALSE QUIZ': 'Đúng/Sai', 'CIRCUIT-ACTION QUIZ': 'Hỏi đáp tác động mạch (Circuit-Action)',
          'SELF-TEST': 'Tự kiểm tra (Self-Test)', 'PROBLEMS': 'Bài tập (Problems)'}
VI_JEND = {'Summary': 'Tóm tắt', 'Key Terms': 'Thuật ngữ', 'Reference': 'Tài liệu tham khảo', 'References': 'Tài liệu tham khảo', 'Additional Reading': 'Đọc thêm', 'Problems': 'Bài tập'}
EN_END = {'SUMMARY': 'Summary', 'KEY TERMS': 'Key Terms', 'KEY FORMULAS': 'Key Formulas', 'TRUE/FALSE QUIZ': 'True/False Quiz', 'CIRCUIT-ACTION QUIZ': 'Circuit-Action Quiz',
          'SELF-TEST': 'Self-Test', 'PROBLEMS': 'Problems'}
T = {
 'vi': dict(h1='Bản đồ nội dung sách', lead='Mục lục thật của cả bốn quyển trong thư mục tài liệu (Floyd 9e, Jaeger 5e, EASA M04, SERVOMECHANISM), có số trang, module nào dùng mục nào, và có bao nhiêu câu hỏi neo vào đó. Đây là bản đồ để tra nhanh “học phần này nằm ở đâu trong sách”.',
            how='Cách đọc', ov='Module → sách', ovsub='Mỗi ô liệt kê mục sách của module kèm trang PDF (mở file PDF theo số trang PDF).',
            books='Mục lục từng quyển', c_sec='Mục', c_in='Trang in', c_pdf='Trang PDF', c_mod='Module (vai trò)', c_q='Câu hỏi', chap='Chương', endm='Cuối chương (câu hỏi): trang bắt đầu của từng phần',
            filt='Lọc', allm='Tất cả module', onlyassigned='Chỉ mục đã gán', search='Tìm tên mục…', nomatch='Không có mục nào khớp.',
            whole='toàn bộ', pages='tr.', pdf='PDF', ofw='trong đó', legend='Chú giải vai trò', quoted='trích', modelled='dựa theo', cited='neo trang', pcb='nhiều nội dung bảng mạch',
            fl='Floyd, Electronic Devices 9e', ja='Jaeger, Microelectronic Circuit Design 5e', ea='EASA Module 04 (B2) Electronic Fundamentals', sv='SERVOMECHANISM (sv).pdf',
            part='Phần', backm='Cuối sách', ans='Đáp án câu lẻ', glo='Thuật ngữ', idx='Chỉ mục', apx='Phụ lục', qa='Hỏi–đáp (câu hỏi và đáp án xen kẽ từng trang)', none='–', ch='Ch.'),
 'en': dict(h1='Book content map', lead='The real table of contents of all four books in the source folder (Floyd 9e, Jaeger 5e, EASA M04, SERVOMECHANISM), with page numbers, which modules use which section and how many questions are anchored to it. Use it to find “where is this topic in the book”.',
            how='How to read', ov='Module → books', ovsub='Each cell lists the module\'s book sections with their PDF pages (open the PDF at the PDF page number).',
            books='Table of contents of each book', c_sec='Section', c_in='Printed p.', c_pdf='PDF p.', c_mod='Module (role)', c_q='Questions', chap='Chapter', endm='End of chapter (questions): start page of each part',
            filt='Filter', allm='All modules', onlyassigned='Assigned sections only', search='Search section title…', nomatch='No section matches.',
            whole='all of it', pages='p.', pdf='PDF', ofw='of which', legend='Role legend', quoted='quoted', modelled='modelled on', cited='page-anchored', pcb='much circuit-board content',
            fl='Floyd, Electronic Devices 9e', ja='Jaeger, Microelectronic Circuit Design 5e', ea='EASA Module 04 (B2) Electronic Fundamentals', sv='SERVOMECHANISM (sv).pdf',
            part='Part', backm='Back matter', ans='Answers to odd-numbered problems', glo='Glossary', idx='Index', apx='Appendix', qa='Questions & answers (question and answer pages alternate)', none='–', ch='Ch.'),
}

def chip(mid, role, t):
    return f'<span class="bm-chip r-{role}" data-m="{mid}" title="{esc(mid)}: {esc(ROLE[role][t["_l"]])}">{mid}</span>'

def qtxt(q, lang, t):
    if not q: return ''
    out = []
    for mid, d in sorted(q.items()):
        parts = []
        for k, lab in (('quoted', t['quoted']), ('modelled', t['modelled']), ('cited', t['cited'])):
            if d.get(k): parts.append(f'{d[k]} {lab}')
        pg = d.get('pages')
        if parts: out.append(f'<b>{mid}</b> ' + ', '.join(parts) + (f' ({t["pdf"]} {",".join(str(p) for p in pg)})' if pg and len(pg) <= 6 else ''))
    return '<br>'.join(out)

def row(cells, mods, text, cls=''):
    ms = ' '.join(sorted(mods))
    return f'<tr class="{cls}" data-mods="{ms}" data-text="{esc(text.lower())}">' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'

def table(head, rows, cls='bm-t'):
    return f'<div class="bm-scroll"><table class="t left {cls}"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'

def modcell(mods, t):
    return ' '.join(chip(m, r, t) for m, r in sorted(mods.items()))

def status_floyd(ch, s):
    if s['mods']: return ''
    return 'background' if ch['num'] <= 11 else ('out' if ch['num'] == 18 else 'other')

def status_jaeger(ch):
    return 'background' if ch['num'] <= 5 else ('out' if ch['num'] in (8, 13, 14, 15, 16, 17, 18) else 'other')

# ---------------------------------------------------------------------------------------------- overview (module -> books)
def floyd_cell(M, mid, t):
    out = []
    for ch in M['floyd']['chapters']:
        ents = [s for s in ch['sections'] if s['mods'].get(mid) in ('core', 'lab')]
        if not ents: continue
        nums = [s for s in ch['sections'] if s['kind'] == 'section']
        if nums and all(s['mods'].get(mid) == 'core' for s in nums):
            lab = f'{t["ch"]}{ch["num"]} §{nums[0]["num"]}…{nums[-1]["num"]}'
        else:
            lab = ', '.join('§' + s['num'] if s['num'] else esc(s['title']) for s in ents)
        lo = min(s['pdf'] for s in ents); hi = max(s['pdf_end'] for s in ents)
        if nums and all(s['mods'].get(mid) == 'core' for s in nums): lo = ch['pdf']; hi = ch['pdf_end']
        role = 'lab' if all(s['mods'].get(mid) == 'lab' for s in ents) else 'core'
        out.append(f'<a href="#floyd-ch{ch["num"]}">{lab}</a> · {t["pdf"]} {lo}–{hi}' + (' <span class="bm-chip r-lab">lab</span>' if role == 'lab' else ''))
    return '<br>'.join(out) or t['none']

def jaeger_cell(M, mid, t):
    out = []
    for ch in M['jaeger5']['chapters']:
        ents = [s for s in ch['sections'] if s['mods'].get(mid)]
        if not ents: continue
        # merge consecutive section numbers
        groups = []; idx = [ch['sections'].index(s) for s in ents]
        for i in idx:
            if groups and i == groups[-1][-1] + 1: groups[-1].append(i)
            else: groups.append([i])
        lab = ', '.join((ch['sections'][g[0]]['num'] if len(g) == 1 else f"{ch['sections'][g[0]]['num']}–{ch['sections'][g[-1]]['num']}") for g in groups)
        out.append(f'<a href="#jaeger-ch{ch["num"]}">{t["ch"]}{ch["num"]} §{lab}</a> · {t["pdf"]} ' + ', '.join(f"{ch['sections'][g[0]]['pdf']}–{ch['sections'][g[-1]]['pdf_end']}" for g in groups))
    return '<br>'.join(out) or t['none']

def easa_cell(M, mid, t):
    rows = M['easa']['rows']; out = []
    for sm in (1, 2, 3):
        rs = [r for r in rows if r['sm'] == sm]; mine = [r for r in rs if r['mods'].get(mid) in ('core', 'ref')]
        if not mine: continue
        if len(mine) >= 0.9 * len(rs) or all(r['mods'].get(mid) == 'core' for r in rs if r['title'] != 'Knowledge Requirements'):
            out.append(f'<a href="#easa-sm{sm}">SM0{sm} ({t["whole"]})</a> · {t["pdf"]} {M["easa"]["submodules"][str(sm)]["first"]}–{M["easa"]["submodules"][str(sm)]["last"]}'); continue
        top = []
        for i, r in enumerate(rs):
            if r['mods'].get(mid) not in ('core', 'ref'): continue
            par = next((x for x in reversed(rs[:i]) if x['level'] < r['level']), None)
            if par is None or par['mods'].get(mid) not in ('core', 'ref'): top.append(r)
        top.sort(key=lambda r: r['pdf'])
        for r in top:
            ref = ' <i>(ref)</i>' if r['mods'].get(mid) == 'ref' else ''
            out.append(f'<a href="#easa-sm{sm}">{esc(r["title"])}</a>{ref} · {r["printed_label"]} · {t["pdf"]} {r["pdf"]}–{r["pdf_end"]}')
    return '<br>'.join(out) or t['none']

def servo_cell(M, mid, t):
    return f'<a href="#servo-ch1">Ch.1–3</a> · {t["pdf"]} 1–{M["servo"]["pages"]}' if mid == 'm10' else t['none']

def overview(M, lang, t):
    head = ['Module', 'Floyd 9e', 'Jaeger 5e', 'EASA M04', 'SERVO (sv)']
    rows = []
    for m in MODS:
        mid = m['id']; ms = M['modules'][mid]
        rows.append(row([f'<b>{mid[1:]}</b> {esc(m[lang])}<br><span class="srcnote">{ms["items"]} ' + ('câu hỏi' if lang == 'vi' else 'items') + f' ({ms["original"]} ' + ('gốc' if lang == 'vi' else 'original') + ')</span>',
                         floyd_cell(M, mid, t), jaeger_cell(M, mid, t), easa_cell(M, mid, t), servo_cell(M, mid, t)], {mid}, m[lang]))
    return table(head, rows, 'bm-t bm-ov')

# ---------------------------------------------------------------------------------------------- Floyd
def floyd_html(M, lang, t):
    vi = lang == 'vi'; F = M['floyd']; h = ''
    for ch in F['chapters']:
        mods = {}
        for s in ch['sections'] + ch['end_parts']:
            for mid, r in s['mods'].items():
                if r in ('core', 'lab'): mods[mid] = r
        title = VI_FLOYD[ch['num']] if vi else ch['title']
        sub = f'{esc(ch["title"])} · ' if vi else ''
        head = (f'<summary><b>{t["ch"]}{ch["num"]}</b> {esc(title)} <span class="srcnote">{sub}{t["pages"]}{ch["printed"]}–{ch["pdf_end"] - F["offset"]} · {t["pdf"]} {ch["pdf"]}–{ch["pdf_end"]}</span> '
                + modcell(mods, {**t, '_l': lang}) + '</summary>')
        rows = []
        for s in ch['sections']:
            st = status_floyd(ch, s)
            if s['kind'] == 'feature':
                ttl = VI_FEAT.get(s['title'], s['title']) if vi else s['title']
                if s['title'] == 'Application Activity' and s.get('pcb_mentions', 0) >= 8: ttl += f' <span class="srcnote">({t["pcb"]}: {s["pcb_mentions"]}×)</span>'
                num = ''
            else: ttl, num = esc(s['title']), esc(s['num'])
            cells = [f'<b>{num}</b> {ttl}' if num else ttl, f'{s["printed"]}–{s["printed_end"]}' if s['printed_end'] > s['printed'] else f'{s["printed"]}',
                     f'{s["pdf"]}–{s["pdf_end"]}' if s['pdf_end'] > s['pdf'] else f'{s["pdf"]}',
                     modcell(s['mods'], {**t, '_l': lang}) + (stl(st, lang) if st else ''), qtxt(s['q'], lang, t)]
            rows.append(row(cells, s['mods'], f'{s["num"]} {s["title"]}'))
        if ch['end_parts']:
            rows.append(f'<tr class="bm-sep"><td colspan="5">{t["endm"]}</td></tr>')
            for e in ch['end_parts']:
                nm = VI_END[e['name']] if vi else EN_END[e['name']]
                cells = [nm, f'{e["printed"]}', f'{e["pdf"]}', modcell(e['mods'], {**t, '_l': lang}), qtxt(e['q'], lang, t)]
                rows.append(row(cells, e['mods'], e['name']))
        h += f'<details class="bm-ch" id="floyd-ch{ch["num"]}" data-mods="{" ".join(sorted(mods))}"{" open" if mods else ""}>{head}' + table([t['c_sec'], t['c_in'], t['c_pdf'], t['c_mod'], t['c_q']], rows) + '</details>'
    back = ' · '.join(f'{(t["ans"] if x["title"].startswith("Answers") else (t["glo"] if x["title"] == "Glossary" else t["idx"]))}: {t["pages"]}{x["printed"]} ({t["pdf"]} {x["pdf"]})' for x in F['back'])
    return h + f'<p class="srcnote">{t["backm"]}: {back}</p>'

# ---------------------------------------------------------------------------------------------- Jaeger
def jaeger_html(M, lang, t):
    vi = lang == 'vi'; J = M['jaeger5']; h = ''; last_part = None
    for ch in J['chapters']:
        if ch['part'] != last_part:
            last_part = ch['part']; h += f'<h3>{esc(last_part)}</h3>'
        mods = {}
        for s in ch['sections']:
            for mid, r in s['mods'].items(): mods[mid] = r
        title = VI_JAEGER[ch['num']] if vi else ch['title']; sub = f'{esc(ch["title"])} · ' if vi else ''
        stt = status_jaeger(ch)
        head = (f'<summary><b>{t["ch"]}{ch["num"]}</b> {esc(title)} <span class="srcnote">{sub}{t["pages"]}{ch["printed"]}–{ch["pdf_end"] - J["offset"]} · {t["pdf"]} {ch["pdf"]}–{ch["pdf_end"]}</span> '
                + modcell(mods, {**t, '_l': lang}) + (stl(stt, lang) if not mods else '') + '</summary>')
        rows = []
        for s in ch['sections']:
            num = esc(s['num']); ttl = esc(s['title']) if s['kind'] == 'section' else (VI_JEND.get(s['title'], s['title']) if vi else s['title'])
            rows.append(row([f'<b>{num}</b> {ttl}' if num else ttl, f'{s["printed"]}', f'{s["pdf"]}–{s["pdf_end"]}' if s['pdf_end'] > s['pdf'] else f'{s["pdf"]}', modcell(s['mods'], {**t, '_l': lang}), ''], s['mods'], f'{s["num"]} {s["title"]}'))
        h += f'<details class="bm-ch" id="jaeger-ch{ch["num"]}" data-mods="{" ".join(sorted(mods))}"{" open" if mods else ""}>{head}' + table([t['c_sec'], t['c_in'], t['c_pdf'], t['c_mod'], t['c_q']], rows) + '</details>'
    ap = ' · '.join(f'{t["apx"]} {a["title"][-1]}: {t["pages"]}{a["printed"]} ({t["pdf"]} {a["pdf"]})' for a in J['appendices'])
    return h + f'<p class="srcnote">{ap} · {t["idx"]}: {t["pdf"]} {J["index_pdf"]}</p>'

# ---------------------------------------------------------------------------------------------- EASA
def easa_html(M, lang, t):
    vi = lang == 'vi'; E = M['easa']; h = ''
    for sm in ('1', '2', '3'):
        S = E['submodules'][sm]; rs = [r for r in E['rows'] if str(r['sm']) == sm]
        mods = {}
        for r in rs:
            for mid, ro in r['mods'].items():
                if ro in ('core',) and mid not in mods: mods[mid] = ro
        head = f'<summary><b>SM0{sm}</b> {esc(S[lang])} <span class="srcnote">{t["pdf"]} {S["first"]}–{S["last"]} · {t["pages"]}{sm}.1–{sm}.{S["last"] - S["offset"]}</span> ' + modcell(mods, {**t, '_l': lang}) + '</summary>'
        rows = []
        for r in rs:
            ind = f'<span class="bm-ind" style="--d:{r["level"] - 1}"></span>'
            ttl = f'{ind}{esc(r["title"])}' + (' <span class="srcnote">*</span>' if r.get('by_hint') else '')
            st = ''
            if not r['mods'] and sm == '1' and r['pdf'] < 45: st = stl('background', lang)
            rows.append(row([ttl, r['printed_label'], f'{r["pdf"]}–{r["pdf_end"]}' if r['pdf_end'] > r['pdf'] else f'{r["pdf"]}', modcell(r['mods'], {**t, '_l': lang}) + st, qtxt(r['q'], lang, t)], r['mods'], r['title']))
        qa = S['qa']; rows.append(f'<tr class="bm-sep"><td colspan="5">{t["qa"]}: {t["pdf"]} {qa[0]}–{qa[1]}</td></tr>')
        h += f'<details class="bm-ch" id="easa-sm{sm}" data-mods="{" ".join(sorted(mods))}" open>{head}' + table([t['c_sec'], t['c_in'], t['c_pdf'], t['c_mod'], t['c_q']], rows) + '</details>'
    note = ('* Tiêu đề không có trong lớp chữ OCR của trang; dùng số trang in trong mục lục của sách.' if vi else '* The heading itself is missing from the page\'s OCR text; the page printed in the book\'s own contents is used.')
    return h + f'<p class="srcnote">{note}</p>'

# ---------------------------------------------------------------------------------------------- SERVO
def servo_html(M, lang, t):
    vi = lang == 'vi'; S = M['servo']; h = ''
    for chn in (1, 2, 3):
        rs = [r for r in S['rows'] if r['chapter'] == chn]; top = rs[0]
        head = (f'<summary><b>{t["ch"]}{chn}</b> {VI_SERVO[chn] if vi else esc(top["title"])} <span class="srcnote">{esc(top["title"]) + " · " if vi else ""}{t["pdf"]} {top["pdf"]}–{top["pdf_end"]}</span> '
                + modcell({'m10': 'core'}, {**t, '_l': lang}) + '</summary>')
        rows = []
        for r in rs[1:]:
            ind = f'<span class="bm-ind" style="--d:{r["level"] - 1}"></span>'
            rows.append(row([f'{ind}<b>{esc(r["rel"])}</b> {esc(r["title"])}', f'{r["pdf"]}', f'{r["pdf"]}–{r["pdf_end"]}' if r['pdf_end'] > r['pdf'] else f'{r["pdf"]}',
                             modcell(r['mods'], {**t, '_l': lang}), qtxt(r['q'], lang, t)], r['mods'], r['title']))
        h += f'<details class="bm-ch" id="servo-ch{chn}" data-mods="m10" open>{head}' + table([t['c_sec'], t['c_in'], t['c_pdf'], t['c_mod'], t['c_q']], rows) + '</details>'
    return h + '<p class="srcnote">' + ('File không có trang đánh số riêng: trang in = trang PDF.' if vi else 'The file has no page numbering of its own: printed page = PDF page.') + '</p>'

# ---------------------------------------------------------------------------------------------- page
def body(lang):
    M = data(); t = T[lang]; vi = lang == 'vi'
    fs = [s for c in M['floyd']['chapters'] for s in c['sections']]; js = [s for c in M['jaeger5']['chapters'] for s in c['sections']]
    nf, nfu = len(fs), sum(1 for s in fs if s['mods']); nj, nju = len(js), sum(1 for s in js if s['mods']); ne, neu = len(M['easa']['rows']), sum(1 for r in M['easa']['rows'] if r['mods'])
    h = f'<h1>{t["h1"]}</h1><p class="lead">{t["lead"]}</p>'
    h += callout('info', t['how'], ul([
        ('Trang in là số in trên trang sách; trang PDF là số trang trong file PDF (Floyd: trang PDF = trang in + 18; Jaeger: + 29; EASA: PDF = trang in của tiểu mô-đun + 11, + 87, + 101 cho SM01/SM02/SM03).' if vi else
         'Printed page is the number printed on the book page; PDF page is the page number inside the PDF file (Floyd: PDF = printed + 18; Jaeger: + 29; EASA: PDF = sub-module printed page + 11, + 87, + 101 for SM01/SM02/SM03).'),
        ('Số trang của Floyd và Jaeger lấy từ chính bookmark của file PDF, rồi đối chiếu với “Brief Contents” in trong sách. Mục lục EASA nhập theo mục lục in của sách, mỗi tiêu đề được tìm lại trong lớp chữ của trang PDF tương ứng. SERVO đọc từ các tiêu đề đánh số trong file.' if vi else
         'Floyd and Jaeger page numbers come from the PDF\'s own bookmarks, cross-checked with the printed Brief Contents. The EASA contents were typed from the book\'s printed contents and every heading was searched again in the text of its PDF page. SERVO is read from the numbered headings in the file.'),
        ('Tên mục giữ nguyên tiếng Anh của sách để tra cho dễ; chỉ tên chương có kèm bản tiếng Việt.' if vi else 'Section titles stay in the books\' English so they are easy to look up; only chapter titles carry a Vietnamese gloss.'),
        (f'Phạm vi: Floyd {nfu}/{nf} mục có module dùng; Jaeger {nju}/{nj} mục được ánh xạ (chỉ để đọc thêm, chưa đọc và chưa trích câu hỏi); EASA {neu}/{ne} tiêu đề có module dùng; SERVO: toàn bộ thuộc m10.' if vi else
         f'Coverage: Floyd {nfu}/{nf} sections used by a module; Jaeger {nju}/{nj} sections mapped (reading references only, not read and no questions quoted); EASA {neu}/{ne} headings used by a module; SERVO: all of it belongs to m10.'),
    ]))
    leg = ''.join(f'<li><span class="bm-chip r-{r}">{r}</span> {esc(ROLE[r][lang])}</li>' for r in ('core', 'lab', 'ref', 'cited', 'optional'))
    leg += ''.join(f'<li>{stl(k, lang)} {esc(v[lang])}</li>' for k, v in STATUS.items())
    h += f'<details class="bm-legend"><summary>{t["legend"]}</summary><ul>{leg}</ul></details>'
    h += f'<h2 id="overview">{t["ov"]}</h2><p class="srcnote">{t["ovsub"]}</p>' + overview(M, lang, t)
    opts = ''.join(f'<option value="{m["id"]}">{m["id"][1:]} · {esc(m[lang])}</option>' for m in MODS)
    h += (f'<h2 id="books">{t["books"]}</h2><div class="bm-bar"><label>{t["filt"]}: <select id="bm-mod"><option value="">{t["allm"]}</option>{opts}</select></label> '
          f'<label><input type="checkbox" id="bm-only"> {t["onlyassigned"]}</label> <input type="search" id="bm-q" placeholder="{t["search"]}"> <span id="bm-none" hidden>{t["nomatch"]}</span></div>')
    h += f'<h3 id="floyd">{t["fl"]}</h3>' + floyd_html(M, lang, t)
    h += f'<h3 id="jaeger">{t["ja"]}</h3>' + jaeger_html(M, lang, t)
    h += f'<h3 id="easa">{t["ea"]}</h3>' + easa_html(M, lang, t)
    h += f'<h3 id="servo">{t["sv"]}</h3>' + servo_html(M, lang, t)
    return h
