"""Single source of truth: course info, books, module list and source mapping (vi/en) for AE2.013 Thermal Systems.
Every number below was read from the files in the project (syllabus, slide titles in OCR_output/, PDF bookmarks, EPUB toc.ncx); nothing is guessed.
Slide ranges: (deck key, first page, last page) in the lecturer's PDF decks.  Section-level book mapping lives in data/bookmap/*.json (P2) and MAPPING.md.
"""
COURSE = dict(code='AE2.013', vi='Hệ thống nhiệt', en='Thermal Systems', ects=4,
              hours=dict(lecture=40, lab=12, tutorial=0, total=52), prereq='AE1.030 Thermodynamics')

# Syllabus text, verbatim in English (OCR_output/01_*.md); Vietnamese is this site's translation.
CO = {
    'CO1': dict(en='Understand fundamental thermodynamic concepts and propulsion systems',
                vi='Hiểu các khái niệm nhiệt động lực học cơ bản và các hệ động lực đẩy'),
    'CO2': dict(en='Analyze thermal system components and processes',
                vi='Phân tích các thành phần và quá trình của hệ thống nhiệt'),
    'CO3': dict(en='Apply mathematical and analytical tools to solve thermal system problems',
                vi='Vận dụng công cụ toán học và phân tích để giải các bài toán hệ thống nhiệt'),
}
CLO = {
    'CLO1': dict(en='Demonstrate a comprehensive understanding of thermodynamic principles and the classification of aerospace propulsion systems and engines.',
                 vi='Chứng tỏ hiểu đầy đủ các nguyên lý nhiệt động lực học và cách phân loại hệ động lực đẩy và động cơ hàng không vũ trụ.'),
    'CLO2': dict(en='Apply mathematical models and computational tools to analyze and solve problems related to power cycles, combustion processes, and compressive flow in thermal systems.',
                 vi='Vận dụng mô hình toán và công cụ tính toán để phân tích, giải các bài toán về chu trình công suất, quá trình cháy và dòng nén được trong hệ thống nhiệt.'),
    'CLO3': dict(en='Evaluate the performance and efficiency of refrigeration cycles and air conditioning systems used in aircraft, including real and ideal processes.',
                 vi='Đánh giá hiệu năng và hiệu suất của các chu trình lạnh và hệ điều hoà không khí dùng trên tàu bay, gồm cả quá trình thực và lý tưởng.'),
    'CLO4': dict(en='Identify, analyze, and balance combustion equations, and assess enthalpy changes in theoretical and practical combustion processes.',
                 vi='Nhận biết, phân tích và cân bằng phương trình cháy, đánh giá biến thiên entanpi trong các quá trình cháy lý thuyết và thực tế.'),
}

# The syllabus lists three references. Reference [1] is misspelt in the syllabus ("Michsl s.Bols"); the book is Cengel & Boles.
BOOKS = {
    'cengel': dict(short='Cengel & Boles', full='Yunus A. Çengel & Michael A. Boles, Thermodynamics: An Engineering Approach, McGraw-Hill (PDF 963 pp.)',
                   syllabus_ref=1, syllabus_name='Michsl s.Bols - Thermodynamics_ an engineering approach-McGraw-Hill Higher Education'),
    'elsayed': dict(short='El-Sayed', full='Ahmed F. El-Sayed, Aircraft Propulsion and Gas Turbine Engines, 2nd ed., CRC Press, 2017 (EPUB)',
                    syllabus_ref=2, syllabus_name='Aircraft propulsion and gas turbine engines, 2nd edition, by Ahmed F. El-Sayed, 2017.'),
    'farokhi': dict(short='Farokhi', full='Saeed Farokhi, Aircraft Propulsion, 2nd ed., Wiley, 2014 (PDF 1048 pp.)',
                    syllabus_ref=3, syllabus_name='Aircraft Propulsion, 2nd edition, by Saeed Farokhi, 2014.'),
}

# Lecturer's slide decks (PDF page counts measured with pdfinfo).
DECKS = {
    'ch1': dict(pdf='Chapter 1 Introduction and Generality_continued.pdf', pages=49, md='02_Chapter1_Introduction_and_Generality.md',
                vi='Chương 1 Giới thiệu và tổng quan', en='Chapter 1 Introduction and Generality'),
    'ch2': dict(pdf='Chapter 2 Power Cycles.pdf', pages=56, md='03_Chapter2_Power_Cycles.md', vi='Chương 2 Chu trình công suất', en='Chapter 2 Power Cycles'),
    'ch3': dict(pdf='Chapter 3 REFRIGERATION CYCLES.pdf', pages=38, md='04_Chapter3_Refrigeration_Cycles.md', vi='Chương 3 Chu trình lạnh', en='Chapter 3 Refrigeration Cycles'),
    'ch4': dict(pdf='Chapter 4 Combustion process.pdf', pages=61, md='05_Chapter4_Combustion_Process.md', vi='Chương 4 Quá trình cháy', en='Chapter 4 Combustion process'),
    'ch5': dict(pdf='Chapter 5 COMPRESSIBLE FLOW.pdf', pages=63, md='06_Chapter5_Compressible_Flow.md', vi='Chương 5 Dòng nén được', en='Chapter 5 Compressible Flow'),
    'tut': dict(pdf='Tutorials I.pdf', pages=29, md='07_Tutorials_I.md', vi='Tutorials I (bài tập mẫu)', en='Tutorials I'),
}

# Tutorials I structure (from slide titles, P1): worked solutions and unsolved problems.
TUT = [
    dict(pages=(1, 6), topic='Ideal Otto cycle', vi='Chu trình Otto lý tưởng', en='The ideal Otto cycle', module='m02', solved=True),
    dict(pages=(7, 13), topic='Ideal Diesel cycle', vi='Chu trình Diesel lý tưởng', en='The ideal Diesel cycle', module='m02', solved=True),
    dict(pages=(14, 17), topic='Problems 3-6 (Otto, Otto, Diesel, Diesel)', vi='Bài 3–6 (Otto, Diesel)', en='Problems 3–6 (Otto, Diesel)', module='m02', solved=False),
    dict(pages=(18, 23), topic='Simple ideal Brayton cycle', vi='Chu trình Brayton đơn giản lý tưởng', en='The simple ideal Brayton cycle', module='m02', solved=True),
    dict(pages=(24, 27), topic='Ideal vapor-compression refrigeration cycle', vi='Chu trình lạnh nén hơi lý tưởng', en='The ideal vapor-compression refrigeration cycle', module='m03', solved=True),
    dict(pages=(28, 29), topic='Problems 7-8 (Brayton)', vi='Bài 7–8 (Brayton)', en='Problems 7–8 (Brayton)', module='m02', solved=False),
]

# id, slug, titles, CLO, slide ranges, textbook chapters (section level: data/bookmap), role of each source.
MODS = [
    dict(id='m01', slug='01-introduction-propulsion', vi='Giới thiệu, nguyên lý đẩy và phân loại động cơ', en='Introduction, principles of propulsion and engine classification',
         clo=['CLO1'], slides=[('ch1', 5, 48)], blank_slides=[],
         books=dict(cengel='Ch.1–2 (nền AE1.030, chỉ background); §9-11 (ref)', farokhi='Ch.3 (core); Ch.1 (ref: lịch sử)', elsayed='Ch.1 §1.3–1.5 (core), Ch.2'),
         src=['Slide Ch.1 tr.5–48', 'Cengel Ch.1–2 (background: review of AE1.030); Cengel §9-11 Ideal Jet-Propulsion Cycles (ref)', 'El-Sayed Ch.1 History and Classifications of Aeroengines, Ch.2 Performance Parameters of Jet Engines', 'Farokhi Ch.3 Engine Thrust and Performance Parameters (core); Ch.1 Introduction (ref, history)']),
    dict(id='m02', slug='02-gas-power-cycles', vi='Chu trình công suất khí: Carnot, Otto, Diesel, Brayton và chu trình phản lực', en='Gas power cycles: Carnot, Otto, Diesel, Brayton and jet-propulsion cycles',
         clo=['CLO2'], slides=[('ch2', 3, 55), ('tut', 1, 23), ('tut', 28, 29)], blank_slides=[],
         books=dict(cengel='Ch.9 (nền: Ch.6–7)', farokhi='Ch.4 (core §4.3.1 turbojet; còn lại ref)', elsayed='Ch.4 (core §4.2 single spool; còn lại ref)'),
         src=['Slide Ch.2 tr.3–55', 'Tutorials I tr.1–23, 28–29', 'Cengel Ch.9 Gas Power Cycles', 'Farokhi Ch.4 Gas Turbine Engine Cycle Analysis', 'El-Sayed Ch.4 Turbojet Engine']),
    dict(id='m03', slug='03-refrigeration-aircraft-air-conditioning', vi='Chu trình lạnh và điều hoà không khí trên tàu bay', en='Refrigeration cycles and aircraft air conditioning',
         clo=['CLO3'], slides=[('ch3', 3, 36), ('tut', 24, 27)], blank_slides=[('ch3', 37, 38)],
         books=dict(cengel='Ch.11 §11-1…11-4 (core); §11-8 gas refrigeration (gần nhất với cooling pack); Ch.14 §14-7 (ref)', farokhi='— (không có mục ECS/cooling pack: đã grep, xem data/bookmap/ecs_search.json)', elsayed='— (không có mục ECS/cooling pack; chỉ một câu ở tr.301 ngoài phạm vi)'),
         src=['Slide Ch.3 tr.3–36', 'Tutorials I tr.24–27', 'Cengel Ch.11 Refrigeration Cycles (§11-8 Gas Refrigeration Cycles is the nearest section to the air-cycle cooling pack of the slides); Ch.14 Gas–Vapor Mixtures and Air Conditioning §14-7 (ref)', 'Farokhi and El-Sayed: no section on ECS/cooling pack found (data/bookmap/ecs_search.json)']),
    dict(id='m04', slug='04-fuels-and-combustion', vi='Nhiên liệu và quá trình cháy', en='Fuels and the combustion process',
         clo=['CLO2', 'CLO4'], slides=[('ch4', 3, 55)], blank_slides=[('ch4', 56, 61)],
         books=dict(cengel='Ch.15 §15-1…15-3 (core)', farokhi='Ch.7 §7.2–7.3 (core)', elsayed='Ch.10 §10.7–10.8 (core)'),
         src=['Slide Ch.4 tr.3–55', 'Cengel Ch.15 Chemical Reactions', 'El-Sayed Ch.10 Combustion Systems', 'Farokhi Ch.7 Combustion Chambers and Afterburners']),
    dict(id='m05', slug='05-compressible-flow', vi='Dòng chảy nén được', en='Compressible flow',
         clo=['CLO2'], slides=[('ch5', 3, 59)], blank_slides=[('ch5', 60, 63)],
         books=dict(cengel='Ch.17 §17-1…17-4 (core; slide dừng ở vòi hội tụ; §17-5 sóng xung kích chỉ ref)', farokhi='Ch.2 §2.10–2.14 (ref), Ch.6, Appendix B', elsayed='Ch.3 §3.8 (ref), Ch.9, Ch.11'),
         src=['Slide Ch.5 tr.3–59', 'Cengel Ch.17 Compressible Flow', 'Farokhi Ch.2 Compressible Flow with Friction and Heat; Ch.6 Aircraft Engine Inlets and Nozzles; Appendix B Isentropic Table', 'El-Sayed Ch.3 §3.8 Shock waves and isentropic flow; Ch.9 Intakes; Ch.11 Exhaust System']),
]
BYID = {m['id']: m for m in MODS}

# Slides that are not content (title/thank-you pages) and slides without text layer: recorded so every slide has a module or a reason (P1 gate).
OUT_OF_SCOPE = [('ch1', 1, 4, 'title and chapter pages (to be confirmed by image in P0)'), ('ch1', 49, 49, '"Thank you" page'),
                ('ch2', 1, 2, 'title pages'), ('ch2', 56, 56, '"Thank you" page'),
                ('ch3', 1, 2, 'title pages'), ('ch4', 1, 2, 'title pages'), ('ch5', 1, 2, 'title pages')]

def slides_of(m):
    """List of (deck, page) for a module, in lecture order."""
    return [(d, p) for d, a, b in m['slides'] for p in range(a, b + 1)]
