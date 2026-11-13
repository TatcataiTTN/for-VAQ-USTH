"""P0 gate: gather OCR_output/_qa/*.json (one file per source, written by the P0 checkers) into OCR_output/QA_REPORT.md.
Every number printed comes from those JSON files (rule R8); nothing is typed by hand.  Run:  python3 -I build/verify/qa_report.py
Exit code 1 when a required JSON is missing or invalid (the P0 gate is not passed)."""
import json, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.abspath(os.path.join(HERE, '..', '..')); SRC = os.path.dirname(P)
QA = os.path.join(SRC, 'OCR_output', '_qa'); OUT = os.path.join(SRC, 'OCR_output', 'QA_REPORT.md')
SLIDES = [('ch1', 'Chapter 1', 49), ('ch2', 'Chapter 2 Power Cycles', 56), ('ch3', 'Chapter 3 Refrigeration', 38), ('ch4', 'Chapter 4 Combustion', 61),
          ('ch5', 'Chapter 5 Compressible Flow', 63), ('tut', 'Tutorials I', 29)]
missing = []

def load(k):
    p = os.path.join(QA, k + '.json')
    if not os.path.exists(p): missing.append(k); return None
    try: return json.load(open(p, encoding='utf-8'))
    except Exception as e: missing.append(f'{k} (invalid JSON: {e})'); return None

L = ['# QA_REPORT: kiểm OCR_output (P0)', '',
     'Tạo bằng `build/verify/qa_report.py` từ `OCR_output/_qa/*.json`. Mọi con số dưới đây được đếm bằng script, không gõ tay. '
     'Mỗi dòng cho biết kiểm được bao nhiêu và CHƯA kiểm bao nhiêu. Chi tiết từng trang, từng giá trị: `_qa/<khóa>.json` và `_qa/<khóa>/QA.md`.', '',
     '## 1. Bộ slide của giảng viên', '',
     '| Bộ | Số trang | Trang đã xem ảnh | ok | minor | wrong | Giá trị số kiểm | ok | slide_error | ocr_error | not_checked / computed_only / input | Trang đã vá |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
tot = collections.Counter(); slide_err = []
for k, name, n in SLIDES:
    d = load(k)
    if not d: L.append(f'| {name} | {n} | (chưa có JSON) |' + ' |' * 9); continue
    v = collections.Counter(s.get('verdict') for s in d.get('sampled', []))
    nu = collections.Counter(r.get('status') for r in d.get('numeric', []))
    seen = len({s['page'] for s in d.get('sampled', [])})
    other = nu.get('not_checked', 0) + nu.get('computed_only', 0) + nu.get('input', 0)
    checked = nu.get('ok', 0) + nu.get('slide_error', 0) + nu.get('ocr_error', 0)
    fixed = len({c.get('page') for c in d.get('changes', [])})
    L.append(f'| {name} | {n} | {seen} | {v.get("ok", 0)} | {v.get("minor", 0)} | {v.get("wrong", 0)} | {checked} | {nu.get("ok", 0)} | {nu.get("slide_error", 0)} | {nu.get("ocr_error", 0)} | {other} | {fixed} |')
    tot.update(dict(pages=n, seen=seen, ok=v.get('ok', 0), minor=v.get('minor', 0), wrong=v.get('wrong', 0), checked=checked, nok=nu.get('ok', 0), serr=nu.get('slide_error', 0), oerr=nu.get('ocr_error', 0)))
    for e in d.get('slide_errors', []): slide_err.append((name, e))
L.append(f'| **Tổng** | {tot["pages"]} | {tot["seen"]} | {tot["ok"]} | {tot["minor"]} | {tot["wrong"]} | {tot["checked"]} | {tot["nok"]} | {tot["serr"]} | {tot["oerr"]} | | |')
L += ['', f'Phần chưa xem ảnh: {tot["pages"] - tot["seen"]}/{tot["pages"]} trang slide. Trang chưa xem phải được xem ảnh trước khi trích bất kỳ công thức hay con số nào từ chúng (xem cột `pages_to_reread` trong JSON). '
      '"minor/wrong" đã được vá ở `OCR_output/0X_*.md` và `_visual_src/` khi checker ghi `fixed: true`.', '']

L += ['## 2. Lỗi của slide (giữ nguyên, ghi nhận, không sửa phép tính của giảng viên)', '']
for name, e in slide_err:
    L.append(f'- **{name}**, tr.{e.get("page", "?")}: {e.get("what", e)}')
if not slide_err: L.append('(không có)')
L.append('')

a = load('app')
L += ['## 3. Appendix 1 (bảng thuộc tính)', '']
if a:
    v = collections.Counter(s.get('verdict') for s in a.get('sampled', []))
    L.append(f'Mẫu trang kiểm: {len(a.get("sampled", []))} (ok {v.get("ok", 0)}, minor {v.get("minor", 0)}, wrong {v.get("wrong", 0)}); thay đổi đã áp vào `08_*.md`: {len(a.get("changes", []))}. Chi tiết: `_qa/app.json`.')
    for k in ('numtoken', 'chart_inventory', 'eq_pages', 'limits'):
        if k in a: L.append(f'- {k}: {json.dumps(a[k], ensure_ascii=False)[:400]}')
else:
    L.append('**CHƯA CÓ** `_qa/app.json` (checker bị dừng; đang chạy lại). Không dùng số liệu Appendix cho bài chưa có đáp án in cho đến khi cổng này qua.')
L.append('')

L += ['## 4. Hai giáo trình PDF', '']
b = load('books')
if b:
    t = b.get('equation_totals', {})
    L += ['| Sách | Trang mẫu | Phương trình hiển thị | ok | scrambled (xáo) | wrong (sai) |', '|---|---|---|---|---|---|']
    for k in ('cengel', 'farokhi'):
        x = t.get(k, {}); L.append(f'| {k} | {x.get("pages")} | {x.get("eq")} | {x.get("ok")} | {x.get("scrambled")} | {x.get("wrong")} |')
    off = b.get('page_offset', {})
    L += ['', '- Trang `## [Trang N]` = trang PDF. ' + '; '.join(f'{k}: in = PDF − {v.get("value")}' for k, v in off.items() if isinstance(v, dict) and 'value' in v) + '.']
    rule = b.get('practical_rule', {})
    for k, v in rule.items(): L.append(f'- **Quy tắc dùng {k}**: {v}')
    L.append(f'- {len(b.get("pages_to_reread", []))} mục trong `pages_to_reread`; giới hạn: {b.get("limits", "")[:300]}')
else: L.append('(chưa có JSON)')
L.append('')

L += ['## 5. El-Sayed (EPUB)', '']
e = load('elsayed')
if e:
    c = e.get('counts', {}); ep = e.get('equations_population', {}); pm = e.get('page_markers', {}); tc = e.get('toc', {})
    L += [f'- Phương trình trong EPUB: {ep.get("total_in_xhtml")}; khớp hệt MathML sau chuẩn hoá: {ep.get("matched_identical_after_normalization")}; {ep.get("no_single_line_md")} không có dòng đơn để so; {ep.get("diff_triaged")} khác (đã xem xét).',
          f'- Kiểm tay: phương trình {c.get("equation")}, bảng {c.get("table")}, hình {c.get("diagram")}, mốc trang in {c.get("page_marker")}.',
          f'- Mục lục thật: {tc.get("entries")} mục, định vị được {tc.get("anchor_located", 0) + tc.get("file_start_located", 0)}, không định vị {tc.get("unlocated")}.',
          f'- Mốc trang in trong bản chữ: {pm.get("unique_marks_in_md")}/{pm.get("page_list_entries")} (thiếu {pm.get("md_labels_missing")}).',
          f'- Lỗi từ nguồn EPUB: ' + '; '.join(e.get('source_defects', [])), f'- Đã vá: {len(e.get("changes", []))} chỗ. Chưa làm: {e.get("limits", "")[:300]}', '',
          '| Chương sách | Tên | Trang in | Phạm vi môn |', '|---|---|---|---|']
    for s in e.get('scope_chapters', []): L.append(f'| {s.get("book_chapter")} | {s.get("title")} | {s.get("printed_pages")} | {s.get("course_part")} |')
else: L.append('(chưa có JSON)')
L.append('')

L += ['## 6. Kết luận cổng P0', '']
gate_ok = not missing
if missing: L.append('**Cổng P0 CHƯA qua.** Thiếu hoặc lỗi: ' + ', '.join(missing) + '.')
else: L.append('Đủ JSON của mọi bộ.')
L.append('Cổng này chỉ nói rằng đã kiểm lấy mẫu và vá những gì thấy; nó KHÔNG nói rằng cả bản chữ đã đúng. Với mọi trang chưa xem ảnh, mọi công thức Cengel/Farokhi và mọi biểu đồ vector: xem ảnh trang trước khi dùng.')
open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('wrote', OUT, '| missing:', missing or 'none'); sys.exit(0 if gate_ok else 1)
