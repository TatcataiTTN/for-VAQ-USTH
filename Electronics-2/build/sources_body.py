"""Body of the 'Sources & mapping' page: books, syllabus→chapter map, how answers were verified, errata found."""
import os, json
from hx import esc, table, callout, ul
from modules import MODS, BOOKS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def notes(mid):
    p = os.path.join(ROOT, 'data', 'verify', f'{mid}_notes.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}

def body(lang, banks):
    vi = lang == 'vi'
    h = '<h2>' + ('Tài liệu nguồn' if vi else 'Source documents') + '</h2>'
    h += table(['#', 'Book' if not vi else 'Sách', 'Drive'],
               [[b['syllabus_ref'], esc(b['full']), f'<a href="https://drive.google.com/file/d/{b["drive"]}/view" target="_blank" rel="noopener">PDF</a>'] for b in BOOKS.values()], 'left')
    h += callout('info', 'Ghi chú phiên bản' if vi else 'Edition notes', ul([
        ('Đề cương ghi Floyd 9th ed. 2012: trùng đúng bản trong Drive (bản Conventional Current Version).' if vi else 'Syllabus lists Floyd 9th ed. 2012: matches the Drive copy (Conventional Current Version).'),
        ('Đề cương ghi Jaeger 4th ed. 2011; Drive có bản 5th (2015, có phần Digital Electronics ch.6–9) và 6th (chỉ còn analog). Module dùng bản 5th làm chính vì đủ cả phần mạch logic.' if vi else
         'Syllabus lists Jaeger 4th ed. 2011; Drive has the 5th (2015, includes Digital Electronics ch.6–9) and the 6th (analog only). Modules use the 5th as primary because it covers logic circuits.'),
        ('Tài liệu EASA M04 trong Drive là bản scan (không có lớp chữ). Đã OCR bằng Tesseract (ocrmypdf) → file sources/easa_m04_ocr.pdf chọn được chữ.' if vi else
         'The EASA M04 PDF in Drive is a scan (no text layer). It was OCR-ed with Tesseract (ocrmypdf) → sources/easa_m04_ocr.pdf is selectable.'),
    ]))
    h += '<h2>' + ('Đề cương → chương sách' if vi else 'Syllabus → textbook chapters') + '</h2>'
    rows = []
    for m in MODS:
        b = banks.get(m['id'])
        rows.append([m['id'][1:], esc(m[lang]), esc(m['easa']), '<br>'.join(esc(x) for x in m['src']), m['clo'],
                     (f'{len(b["items"])} / {sum(1 for i in b["items"] if i["origin"]=="goc")}' if b else '–')])
    h += table(['#', 'Module', 'EASA Part-66 M04', 'Floyd / Jaeger / EASA', 'CLO', ('Câu / gốc' if vi else 'Qs / orig')], rows, 'left')
    h += '<h2>' + ('Cách kiểm chứng đáp án' if vi else 'How answers were verified') + '</h2>'
    h += ul([
        ('Floyd 9e không in đáp án cho Self-Test, True/False Quiz và Circuit-Action Quiz (chỉ ghi "answers at pearsonhighered.com"). Mọi đáp án ở đây do chúng tôi giải lại: câu định tính đối chiếu với nội dung chương; câu có số được tính bằng script Python (thư mục build/verify/).' if vi else
         'Floyd 9e prints no answers for its Self-Test, True/False and Circuit-Action quizzes (it points to pearsonhighered.com). Every answer here was re-solved: conceptual items against the chapter text, numeric items by Python scripts (build/verify/).'),
        ('Bài Problems có số lẻ được đối chiếu với "Answers to Odd-Numbered Problems" cuối sách Floyd.' if vi else 'Odd-numbered Problems were cross-checked with Floyd\'s "Answers to Odd-Numbered Problems".'),
        ('Câu hỏi EASA M04 có đáp án in sẵn trong sách; vẫn được kiểm tra lại, chỗ sai được ghi bên dưới.' if vi else 'EASA M04 questions have printed answers; they were still re-checked and disagreements are listed below.'),
        ('Câu "Bổ sung" sinh bằng chương trình có tham số ngẫu nhiên (seed cố định); đáp án tính bằng công thức và kiểm tra độc lập.' if vi else '"Generated" questions come from seeded parameter generators; answers are computed and independently checked.'),
    ])
    h += '<h2>' + ('Lỗi/nghi vấn phát hiện trong tài liệu gốc' if vi else 'Errata and doubtful items found in the sources') + '</h2>'
    any_note = False
    for m in MODS:
        n = notes(m['id']).get(lang, [])
        if n:
            any_note = True
            h += f'<h3>{m["id"][1:]}. {esc(m[lang])}</h3>' + ul([esc(x) for x in n])
    if not any_note: h += '<p>–</p>'
    return h
