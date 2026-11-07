"""Bodies of the 'Exercise finder' page and of the Written Practice hub (vi / en). Numbers come from data/numeric/summary.json (build/numeric/scan_all.py)."""
import os, json
from hx import esc, table, callout, ul
from modules import MODS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KIND = {'vi': {'exercise': 'Exercise (khung trong bài, có ANSWERS in sẵn)', 'example': 'Example (ví dụ có lời giải)', 'problem': 'Problem (bài cuối chương)', 'related_problem': 'Related Problem (bài tương tự sau ví dụ)',
               'selftest': 'Self-Test', 'truefalse': 'True/False Quiz', 'circuit_action': 'Circuit-Action Quiz', 'checkup': 'Section Checkup (câu hỏi cuối mục)', 'question': 'Câu hỏi EASA (có đáp án in)'},
        'en': {'exercise': 'Exercise (in-text box with printed ANSWERS)', 'example': 'Example (worked)', 'problem': 'Problem (end of chapter)', 'related_problem': 'Related Problem (after an example)',
               'selftest': 'Self-Test', 'truefalse': 'True/False Quiz', 'circuit_action': 'Circuit-Action Quiz', 'checkup': 'Section Checkup (end-of-section question)', 'question': 'EASA question (printed answer)'}}
BOOK = {'floyd': 'Floyd 9e', 'jaeger5': 'Jaeger 5e', 'easa': 'EASA M04'}

def summary(): return json.load(open(os.path.join(ROOT, 'data', 'numeric', 'summary.json'), encoding='utf-8'))

def exercises_body(lang):
    vi = lang == 'vi'; S = summary(); bk = S['by_kind']
    h = '<h1>' + ('Tra cứu bài tập có số' if vi else 'Exercise finder (numeric problems)') + '</h1>'
    tot = sum(v['total'] for v in bk.values()); num = sum(v['numeric'] for v in bk.values()); ans = sum(v['answer'] for v in bk.values()); sol = sum(v.get('solved', 0) for v in bk.values()); skp = sum(v.get('skipped', 0) for v in bk.values())
    h += '<p class="lead">' + (f'Đã quét TOÀN BỘ bài tập của bốn quyển trong thư mục tài liệu: {tot:,} mục, trong đó {num:,} mục có số liệu, {ans:,} mục có đáp án in sẵn trong sách và {sol:,} bài Jaeger không có đáp án in nhưng đã được site giải và kiểm lại (nhãn riêng, không lẫn với đáp án của sách). Mỗi mục ghi rõ vị trí (chương, mục, trang in, trang PDF), có số hay không, có cần hình hay mô phỏng không, thuộc module nào và site đã có chưa.'
                              if vi else f'Every exercise of the four books in the source folder has been scanned: {tot:,} items, {num:,} of them with numbers, {ans:,} with an answer printed in the book and {sol:,} Jaeger problems that print no answer but were solved and re-checked by this site (labelled separately from the book\'s answers). Each item shows where it is (chapter, section, printed page, PDF page), whether it has numbers, needs a figure or a simulator, which module it belongs to and whether the site already has it.') + '</p>'
    rows = []
    for k, v in sorted(bk.items()):
        b, kind = k.split('/')
        rows.append([BOOK[b], esc(KIND[lang].get(kind, kind)), f"{v['total']:,}", f"{v['numeric']:,}", f"{v['figure']:,}", f"{v['answer']:,}", f"{v.get('solved', 0):,}", f"{v['mapped']:,}", f"{v['in_site']:,}"])
    head = ['Sách', 'Loại', 'Tổng', 'Có số', 'Cần hình', 'Đáp án in', 'Site tự giải', 'Thuộc module', 'Đã có trên site'] if vi else ['Book', 'Type', 'Total', 'Numeric', 'Figure', 'Printed answer', 'Solved by site', 'In a module', 'On the site']
    h += table(head, rows, 'left')
    h += callout('info', 'Cách đọc' if vi else 'How to read', ul([
        ('“Có số” nghĩa là đề có ít nhất một đại lượng kèm đơn vị (V, mA, kΩ, Hz, dB…) hoặc ≥ 3 số; “cần hình” là đề nhắc Hình/Bảng trong sách; “cần mô phỏng” là đề đòi SPICE/MATLAB…' if vi else
         '“Numeric” means at least one quantity with a unit (V, mA, kΩ, Hz, dB…) or three or more numbers; “figure” means the statement refers to a Figure/Table in the book; “simulator” means it asks for SPICE/MATLAB…'),
        ('Đề Floyd được dựng lại từ từng ký tự của PDF: chỉ số dưới (VGS(off)), ký hiệu Hy Lạp, ±, ′, Δ, |x| và dấu trừ đều được giữ; hình vẽ, chú thích hình và khung bên lề không bị dính vào đề. Đã đối chiếu 345 đề với một lần đọc độc lập bằng Apple Vision OCR (độ trùng 98,8 %). Đề Jaeger đã dựng lại số mũ (10^6 không bị dính thành 106). Công thức trình bày thành dòng riêng (phân số, căn) vẫn nên đọc ở trang sách đã ghi.' if vi else
         'Floyd statements are rebuilt character by character from the PDF: subscripts (VGS(off)), Greek letters, ±, ′, Δ, |x| and minus signs are kept, and figures, figure captions and sidebars are never glued to a statement. 345 statements were cross-checked against an independent reading with Apple Vision OCR (98.8 % agreement). Jaeger statements have their exponents rebuilt (10^6 is not flattened to 106). Formulas set on their own line (fractions, roots) are still best read on the book page given.'),
        ('Chỉ trích ngắn (khoảng 190 ký tự) để nhận diện bài; đáp án in là đáp án của sách (chỉ kết quả cuối).' if vi else 'Only a short snippet (about 190 characters) is shown to identify the exercise; the printed answer is the book\'s (final result only).'),
        (f'“Site tự giải” = problem Jaeger sách không in đáp án; đáp án do site tính bằng công thức của sách và kiểm lại bằng cách độc lập (mô phỏng số, mạch chính xác, FFT, nghiệm đa thức…), kèm cách tính và giả định. {skp} bài Jaeger thuộc nhóm này được giữ lại chưa giải kèm lý do (cần hình, đề thiếu dữ kiện, đòi vẽ/chứng minh…). Các bài khác có số nhưng ngoài tập này vẫn chưa có đáp án.' if vi else
         f'“Solved by site” = Jaeger problems with no printed answer; the answer was computed by this site with the book\'s formulas and re-checked by an independent route (numerical simulation, exact circuit, FFT, polynomial roots…), with the method and assumptions. {skp} Jaeger problems of this group are left unsolved, each with its reason (figure needed, data missing, asks for a sketch or proof…). Other numeric problems outside this set still have no answer.'),
    ]))
    # per module: how many numeric exercises are ready to be added / already on the site
    pm = S['per_module']; rows = []
    for m in MODS:
        v = pm.get(m['id'], {})
        rows.append([m['id'][1:], esc(m[lang]), v.get('mapped', 0), v.get('numeric', 0), v.get('in_site', 0), v.get('solved', 0), v.get('ready', 0), v.get('figure', 0), v.get('simulation', 0), v.get('conceptual', 0)])
    head2 = ['#', 'Module', 'Bài thuộc module', 'Có số', 'Đã có trên site', 'Site tự giải', 'Sẵn sàng thêm', 'Cần hình', 'Cần mô phỏng', 'Lý thuyết'] if vi else ['#', 'Module', 'Exercises in module', 'Numeric', 'On the site', 'Solved by site', 'Ready to add', 'Figure', 'Simulator', 'Conceptual']
    h += '<h2>' + ('Theo module' if vi else 'By module') + '</h2>' + table(head2, rows, 'left')
    cov = json.load(open(os.path.join(ROOT, 'data', 'numeric', 'coverage.json'), encoding='utf-8'))
    cols = ['printed', 'solved', 'bank', 'figure', 'sim', 'skipped', 'open']
    ch = {'vi': ['Module', 'Bài có số', 'Đáp án in (Viết tay)', 'Site giải và kiểm', 'Trong ngân hàng câu hỏi', 'Cần hình của sách', 'Cần mô phỏng', 'Chưa giải (có lý do)', 'Chưa làm'],
          'en': ['Module', 'Numeric exercises', 'Printed answer (Written)', 'Solved and checked', 'In the question bank', 'Needs a book figure', 'Needs a simulator', 'Not solved (reason given)', 'Nothing yet']}[lang]
    rows = []
    for m in MODS:
        v = cov['per_module'].get(m['id'])
        if v: rows.append([m['id'][1:], esc(m[lang]), v['total']] + [v.get(c, 0) for c in cols])
    u = cov['unique']; rows.append(['Σ', '', cov['unique_total']] + [u.get(c, 0) for c in cols])
    h += '<h2>' + ('Độ phủ của các bài tính' if vi else 'Coverage of the calculation exercises') + '</h2>' + table(ch, rows, 'left')
    cov_note = {'vi': f'Bài “có số” của bốn quyển thuộc các module (một bài thuộc hai module được đếm ở mỗi module, dòng Σ đếm mỗi bài một lần): {cov["unique_total"]} bài. Có đáp án để luyện (in sẵn, site giải và kiểm, hoặc đã thành câu của ngân hàng): {u.get("printed", 0) + u.get("solved", 0) + u.get("bank", 0)}. Còn lại không phải là sót: {u.get("figure", 0)} bài cần hình của sách (finder ghi trang chứa hình, sách chỉ in đáp án cho bài số lẻ nên phần lớn chưa có đáp án), {u.get("sim", 0)} bài cần SPICE/MATLAB, {u.get("skipped", 0)} bài đã xem và không giải, mỗi bài có lý do (đòi vẽ hay thiết kế nhiều đáp án, phụ thuộc hình hay bài trước, đề thiếu dữ kiện). “Chưa làm” = bài giải được mà chưa giải: phải bằng 0.',
                'en': f'“Numeric” exercises of the four books that belong to the modules (an exercise in two modules is counted in each; the Σ row counts every exercise once): {cov["unique_total"]}. With an answer to practise on (printed, solved and checked by this site, or turned into a bank question): {u.get("printed", 0) + u.get("solved", 0) + u.get("bank", 0)}. The rest is not an oversight: {u.get("figure", 0)} need a figure of the book (the finder gives the page; the book prints answers only for odd-numbered problems so most have none yet), {u.get("sim", 0)} need SPICE/MATLAB, {u.get("skipped", 0)} were examined and left unsolved, each with its reason (asks for a drawing or a design with several answers, depends on a figure or an earlier problem, data missing). “Nothing yet” = solvable but not solved: it must be 0.'}[lang]
    h += '<p class="srcnote">' + cov_note + '</p>'
    h += '<h2>' + ('Danh mục đầy đủ' if vi else 'Full index') + '</h2><div id="exfind" data-src="../../exercises/catalog.json"></div>'
    return h

def written_body(lang):
    vi = lang == 'vi'
    h = '<h1>' + ('Luyện viết tay (Written Practice)' if vi else 'Written Practice') + '</h1>'
    h += '<p class="lead">' + ('Bài tập từ chính sách giáo trình: khung EXERCISE của Jaeger và problem cuối chương của Floyd có đáp án in sẵn, cùng problem của Jaeger không có đáp án in do site tự giải và kiểm. Làm như đi thi (đồng hồ, chỉ hiện đề), rồi tự chấm từng bài; hoặc học với đáp án. Kết quả lưu trong trình duyệt và hiện ở bảng tiến độ trên trang chủ.'
                              if vi else 'Exercises from the textbooks themselves: Jaeger EXERCISE boxes and Floyd end-of-chapter problems with printed answers, plus Jaeger problems without a printed answer that this site solved and checked. Take a paper as an exam (timer, statements only) and mark yourself exercise by exercise, or study with the answers. Results are kept in this browser and feed the progress panel on the home page.') + '</p>'
    h += callout('info', 'Quy trình' if vi else 'Workflow', ul([
        ('1) Làm một đề như đi thi. 2) Tự chấm từng bài so với đáp án in. 3) Làm lại những bài mất điểm ở chế độ học, rồi luyện thêm ở Ngân hàng câu hỏi.' if vi else '1) Take a paper as an exam. 2) Mark yourself against the printed answers. 3) Redo the lost exercises in study mode, then drill more in the Practice bank.'),
        ('Đáp án là kết quả cuối in trong sách; cách làm bạn tự viết ra. Bài ghi “cần hình” dùng hình vẽ của sách ở trang đã nêu.' if vi else 'The answer is the final result printed in the book; you write the working yourself. Exercises marked “figure needed” use the book\'s figure at the page given.'),
    ]))
    h += '<div id="written-hub" data-src="../../written/papers.json"><p class="muted">…</p></div>'
    return h

def written_paper_body(lang):
    return '<div id="written" data-src="../../written/papers.json"><p class="muted">…</p></div>'
