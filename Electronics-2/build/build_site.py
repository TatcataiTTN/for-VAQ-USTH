"""Build the whole static site (vi/ + en/) from build/content/mNN.py + data/qbank/*.json.
Run:  python3 build/assemble.py && python3 build/build_site.py"""
import os, sys, json, importlib, random, html
sys.path.insert(0, os.path.dirname(__file__))
import hx
from hx import esc, deck, divider, callout, quiz_block, table, ul
from sitelib import page, write, ROOT
from modules import MODS, COURSE, BOOKS, BYID
LANGS = ('vi', 'en')
S = {
 'vi': dict(home='Trang chủ', objectives='🎯 Sau module này bạn sẽ', source='Nguồn', easa='EASA Part-66', time='Thời lượng', nq='Câu hỏi',
            orig='gốc', notes='Nội dung chi tiết', quiz='Tự kiểm tra nhanh (10 câu, ưu tiên câu gốc trong sách)', practice='Luyện tập sâu',
            open_bank='Mở ngân hàng câu hỏi của module', nb='Notebook Jupyter', nb_txt='Tải notebook (đã chạy sẵn, có đầu ra thật):',
            prev='← Module trước', next='Module sau →', soon='Sắp có', openm='Mở bài giảng →', modules='Các module', clo='CLO',
            prac_title='Luyện tập theo module', exam_title='Luyện đề tổng hợp', src_title='Nguồn tài liệu và bảng đối chiếu', books_title='Bản đồ nội dung sách', ex_title='Tra cứu bài tập có số', wr_title='Luyện viết tay', an_title='Phân tích đề', lab_title='Phòng thí nghiệm'),
 'en': dict(home='Home', objectives='🎯 After this module you will', source='Source', easa='EASA Part-66', time='Time', nq='Questions',
            orig='original', notes='Detailed notes', quiz='Quick self-check (10 questions, textbook originals first)', practice='Deep practice',
            open_bank='Open this module\'s question bank', nb='Jupyter notebook', nb_txt='Download the notebook (already executed, real outputs):',
            prev='← Previous module', next='Next module →', soon='Coming soon', openm='Open lesson →', modules='Modules', clo='CLO',
            prac_title='Practice by module', exam_title='Mixed mock tests', src_title='Sources and mapping', books_title='Book content map', ex_title='Exercise finder', wr_title='Written practice', an_title='Question analyser', lab_title='Lab'),
}

def loc(v, lang):
    return v.get(lang, v.get('en', '')) if isinstance(v, dict) else v

def localize(it, lang, r):
    d = dict(id=it['id'], kind=it['kind'], q=loc(it['q'], lang), topic=loc(it['topic'], lang), level=it['level'],
             src=loc(it['src'], lang), origin=it['origin'])
    if it.get('fig'): d['fig'] = r + it['fig']
    if it['kind'] == 'ess': d['sol'] = loc(it['sol'], lang)
    else:
        d['opts'] = [loc(o, lang) for o in it['opts']]; d['correct'] = it['correct']; d['explain'] = loc(it['explain'], lang)
    return d

def load_bank(mid):
    p = os.path.join(ROOT, 'data', 'qbank', f'{mid}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None

def load_content(mid, lang):
    p = os.path.join(ROOT, 'build', 'content', f'{mid}.py')
    if not os.path.exists(p): return None
    hx.LANG = lang
    mod = importlib.import_module(f'content.{mid}'); importlib.reload(mod)
    return mod.module(lang)

def pick_quiz(bank, n=10):
    items = bank['items']; rng = random.Random(len(items))
    goc = [i for i in items if i['origin'] == 'goc']; gen = [i for i in items if i['origin'] != 'goc']
    pool = goc[:]; rng.shuffle(pool); out = pool[:n]
    if len(out) < n: g = gen[:]; rng.shuffle(g); out += g[:n - len(out)]
    return out

def notebooks(m):
    out = []
    for lang in LANGS:
        fn = f'{m["id"]}_{m["slug"][3:].replace("-", "_")}_{lang}.ipynb'
        if os.path.exists(os.path.join(ROOT, 'notebooks', fn)): out.append((lang, fn))
    return out

def module_page(m, c, bank, lang):
    s = S[lang]; rel = f'modules/{m["slug"]}/index.html'; r = '../../../'
    nq = len(bank['items']) if bank else 0; ng = sum(1 for i in bank['items'] if i['origin'] == 'goc') if bank else 0
    slides = []; P = len(c['parts'])
    for k, part in enumerate(c['parts'], 1):
        slides.append((divider(k, P, part['title'], part['bullets']), True))
        slides += [(x, False) for x in part['slides']]
    h = f'<div class="crumbs"><a href="../../index.html">{s["home"]}</a> › {s["modules"]} › {m["id"].upper()}</div>'
    h += f'<h1>{m["id"][1:]}. {esc(m[lang])}</h1><p class="lead">{c.get("subtitle", "")}</p>'
    h += (f'<p><span class="tag">{s["easa"]} {esc(m["easa"])}</span><span class="tag">{s["clo"]}: {m["clo"]}</span>'
          f'<span class="tag">{s["time"]}: {c.get("time", "")}</span><span class="tag exam">{s["nq"]}: {nq} ({ng} {s["orig"]})</span></p>')
    h += '<p class="srcnote">' + ' · '.join(esc(x) for x in m['src']) + f' · <a href="../../books/index.html#overview">{s["books_title"]}</a></p>'
    h += callout('good', s['objectives'], ul(c['objectives']))
    h += deck(slides, 'd-' + m['id'])
    h += f'<h2>{s["notes"]}</h2>' + c['notes']
    if bank:
        h += f'<h2>{s["quiz"]}</h2>' + quiz_block('q-' + m['id'], [localize(i, lang, r) for i in pick_quiz(bank)])
        h += f'<h2>{s["practice"]}</h2><p><a class="btn" href="../../practice/{m["id"]}.html">{s["open_bank"]} ({nq} + {len(bank["essays"])})</a></p>'
    nbs = notebooks(m)
    if nbs:
        h += f'<h2>{s["nb"]}</h2><p>{s["nb_txt"]}</p><ul>' + ''.join(f'<li><a href="{r}notebooks/{fn}" download>{fn}</a> ({l.upper()})</li>' for l, fn in nbs) + '</ul>'
    i = MODS.index(m); nav = '<div class="modnav">'
    if i > 0: nav += f'<a href="../{MODS[i-1]["slug"]}/index.html">{s["prev"]}: {esc(MODS[i-1][lang])}</a>'
    if i < len(MODS) - 1: nav += f'<a href="../{MODS[i+1]["slug"]}/index.html">{s["next"]}: {esc(MODS[i+1][lang])}</a>'
    h += nav + '</div>'
    write(f'{lang}/{rel}', page(m[lang], h, lang, rel, c.get('subtitle', ''), scripts=('deck.js', 'quiz.js')))

def bank_page(m, bank, lang):
    s = S[lang]; rel = f'practice/{m["id"]}.html'; r = '../../'
    data = dict(module=m['id'], items=[localize(i, lang, r) for i in bank['items']], essays=[localize(e, lang, r) for e in bank['essays']])
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    h = (f'<div class="crumbs"><a href="../index.html">{s["home"]}</a> › <a href="index.html">{s["prac_title"]}</a> › {m["id"].upper()}</div>'
         f'<h1>{m["id"][1:]}. {esc(m[lang])}</h1><p class="srcnote">' + ' · '.join(esc(x) for x in m['src']) + '</p>'
         f'<div id="bank"></div><script type="application/json" id="bank-data">{js}</script>')
    write(f'{lang}/{rel}', page(m[lang], h, lang, rel, scripts=('bank.js',)))

def main():
    banks = {m['id']: load_bank(m['id']) for m in MODS}
    contents = {}
    for lang in LANGS:
        only = set(filter(None, os.environ.get('ONLY', '').split(',')))
        for m in MODS:
            if only and m['id'] not in only:
                contents[(m['id'], lang)] = os.path.exists(os.path.join(ROOT, f'{lang}/modules/{m["slug"]}/index.html')) or None
                if contents[(m['id'], lang)] and (m['id'], lang) not in contents: pass
                continue
            c = load_content(m['id'], lang); contents[(m['id'], lang)] = c
            b = banks[m['id']]
            if c: module_page(m, c, b, lang)
            if b: bank_page(m, b, lang)
        index_page(lang, contents, banks); practice_index(lang, banks); exam_page(lang, banks); sources_page(lang, banks); books_page(lang); exercises_page(lang); written_pages(lang); tool_pages(lang)
    write('index.html', '<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=vi/index.html"><title>AE2.025 Electronics 2</title></head>'
          '<body><p><a href="vi/index.html">Tiếng Việt</a> · <a href="en/index.html">English</a></p></body></html>')
    print('built', sum(1 for v in contents.values() if v), 'module pages')

def index_page(lang, contents, banks):
    s = S[lang]
    intro = {'vi': f'<h1>{COURSE["code"]} · {COURSE["vi"]}</h1><p class="lead">Hệ thống tự học song ngữ bám đề cương USTH: vi mạch tích hợp (IC), bảng mạch in (PCB), hệ servo và ứng dụng trên tàu bay. '
                   f'{COURSE["ects"]} ECTS · {COURSE["hours"]["lecture"]} giờ lý thuyết · {COURSE["hours"]["tutorial"]} giờ bài tập · {COURSE["hours"]["lab"]} giờ thực hành · học trước: {COURSE["prereq"]}.</p>',
             'en': f'<h1>{COURSE["code"]} · {COURSE["en"]}</h1><p class="lead">Bilingual self-study system following the USTH syllabus: integrated circuits (IC), printed circuit boards (PCB), servomechanisms and their aircraft applications. '
                   f'{COURSE["ects"]} ECTS · {COURSE["hours"]["lecture"]} h lecture · {COURSE["hours"]["tutorial"]} h tutorial · {COURSE["hours"]["lab"]} h lab · prerequisite: {COURSE["prereq"]}.</p>'}[lang]
    clo = {'vi': ['CLO1: Trình bày và minh hoạ nguyên lý IC, PCB và hệ servo', 'CLO2: Dùng toán và vật lý để phân tích các phương trình chức năng của mạch điện tử',
                  'CLO3: Phân tích, tính tham số từng linh kiện để dựng một mạch cụ thể', 'CLO4: Làm việc nhóm để lắp mạch điều khiển động cơ servo'],
           'en': ['CLO1: Clearly state and illustrate the principles of IC, PCB and servomechanism', 'CLO2: Apply maths and physics to analyze and interpret equations related to functions of the electronic circuits',
                  'CLO3: Analyze and calculate parameters of each electronic component used to build a specific electronic circuit', 'CLO4: Work in group to build a circuit to control a servomotor']}[lang]
    h = intro + callout('info', 'Course learning outcomes', ul(clo))
    h += f'<h2 id="modules">{s["modules"]}</h2><div class="grid">'
    for m in MODS:
        b = banks[m['id']]; c = contents[(m['id'], lang)]
        cnt = f'<p>{s["nq"]}: {len(b["items"])} ({sum(1 for i in b["items"] if i["origin"]=="goc")} {s["orig"]}) + {len(b["essays"])}</p>' if b else ''
        inner = f'<div class="num">MODULE {m["id"][1:]} · EASA {esc(m["easa"])}</div><h3>{esc(m[lang])}</h3><p>{esc(" · ".join(m["src"]))}</p>{cnt}'
        if c: h += f'<a class="mod-card" href="modules/{m["slug"]}/index.html">{inner}<p><b>{s["openm"]}</b></p></a>'
        else: h += f'<div class="mod-card" style="opacity:.5;cursor:default">{inner}<p>{s["soon"]}</p></div>'
    h += '</div>'
    tools = {'vi': [('Ngân hàng câu hỏi theo module', 'practice/index.html'), ('Đề tính giờ trộn mọi module', 'exam/index.html'), ('Luyện viết tay có đáp án in', 'written/index.html'), ('Tra cứu bài tập có số của cả bốn quyển', 'exercises/index.html'), ('Phân tích một câu hỏi: module và bài tương tự trong sách', 'analyse/index.html'), ('Phòng thí nghiệm: máy tính op-amp, lọc, 555, ổn áp, nhị phân', 'lab/index.html'), ('Bản đồ nội dung sách', 'books/index.html'), ('Nguồn và bảng đối chiếu', 'sources/index.html')],
             'en': [('Practice bank by module', 'practice/index.html'), ('Timed sets mixed from every module', 'exam/index.html'), ('Written practice with printed answers', 'written/index.html'), ('Exercise finder for all four books', 'exercises/index.html'), ('Question analyser: module and similar exercises in the books', 'analyse/index.html'), ('Lab: op-amp, filter, 555, regulator and binary calculators', 'lab/index.html'), ('Book content map', 'books/index.html'), ('Sources and coverage', 'sources/index.html')]}[lang]
    h += '<h2>' + ('Công cụ luyện tập' if lang == 'vi' else 'Practice tools') + '</h2><ul>' + ''.join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in tools) + '</ul>'
    mods_json = json.dumps([dict(id=m['id'], title=m[lang], href=f'practice/{m["id"]}.html') for m in MODS], ensure_ascii=False).replace("'", '&#39;')
    h += '<h2>' + ('Tiến độ của bạn' if lang == 'vi' else 'Your progress') + f'</h2><div id="progress" data-mods=\'{mods_json}\'><p class="muted">…</p></div>'
    write(f'{lang}/index.html', page(COURSE[lang], h, lang, 'index.html', scripts=('progress.js',)))

def practice_index(lang, banks):
    s = S[lang]
    rows = [[m['id'][1:], f'<a href="{m["id"]}.html">{esc(m[lang])}</a>', len(b['items']), sum(1 for i in b['items'] if i['origin'] == 'goc'), len(b['essays'])]
            for m in MODS for b in [banks[m['id']]] if b]
    head = ['#', 'Module', s['nq'], s['orig'], 'Worked' if lang == 'en' else 'Tự luận']
    h = f'<h1>{s["prac_title"]}</h1>' + table(head, rows, 'left')
    write(f'{lang}/practice/index.html', page(s['prac_title'], h, lang, 'practice/index.html'))

def exam_page(lang, banks, nsets=6, per=20):
    s = S[lang]; rng = random.Random(2025); pool = []
    for m in MODS:
        b = banks[m['id']]
        if b: pool += [i for i in b['items'] if i['kind'] == 'mcq']
    if not pool: return
    sets = []
    for k in range(nsets):
        pick = rng.sample(pool, min(per, len(pool)))
        sets.append(dict(name=('Đề ' if lang == 'vi' else 'Set ') + str(k + 1), items=[localize(i, lang, '../../') for i in pick]))
    js = json.dumps(dict(minutes=30, sets=sets), ensure_ascii=False).replace('</', '<\\/')
    note = {'vi': 'Mỗi đề 20 câu trộn từ mọi module (cả câu gốc và câu bổ sung), 30 phút; đáp án chỉ hiện sau khi nộp.',
            'en': 'Each set has 20 questions mixed from all modules (originals and generated), 30 minutes; answers appear only after you submit.'}[lang]
    h = f'<h1>{s["exam_title"]}</h1><p class="lead">{note}</p><div id="exam"></div><script type="application/json" id="exam-data">{js}</script>'
    write(f'{lang}/exam/index.html', page(s['exam_title'], h, lang, 'exam/index.html', scripts=('exam.js',)))

def sources_page(lang, banks):
    s = S[lang]
    p = os.path.join(ROOT, 'build', 'sources_body.py')
    import sources_body; importlib.reload(sources_body)
    h = f'<h1>{s["src_title"]}</h1>' + sources_body.body(lang, banks)
    write(f'{lang}/sources/index.html', page(s['src_title'], h, lang, 'sources/index.html'))

def books_page(lang):
    s = S[lang]
    import bookmap_body; importlib.reload(bookmap_body)
    desc = ('Mục lục thật của Floyd, Jaeger, EASA M04 và SERVOMECHANISM với số trang, module dùng và số câu hỏi theo từng mục.' if lang == 'vi'
            else 'Real tables of contents of Floyd, Jaeger, EASA M04 and SERVOMECHANISM with page numbers, the modules that use each section and question counts.')
    write(f'{lang}/books/index.html', page(s['books_title'], bookmap_body.body(lang), lang, 'books/index.html', desc=desc, scripts=('bookmap.js',)))

def exercises_page(lang):
    s = S[lang]
    import exercises_body; importlib.reload(exercises_body)
    write(f'{lang}/exercises/index.html', page(s['ex_title'], exercises_body.exercises_body(lang), lang, 'exercises/index.html', scripts=('exercises.js', 'bookmap.js'),
          desc=('Danh mục mọi bài tập của Floyd, Jaeger và EASA: bài có số, cần hình, đáp án in, thuộc module nào.' if lang == 'vi' else 'Index of every exercise of Floyd, Jaeger and EASA: numeric, figure, printed answer, module.')))

def tool_pages(lang):
    s = S[lang]; vi = lang == 'vi'
    h = f'<h1>{s["an_title"]}</h1><p class="lead">' + ('Dán một câu hỏi: hệ thống nhận ra các đại lượng, dạng đề, module phù hợp và các bài giống nhất trong 4.858 bài đã quét của bốn quyển, kèm vị trí trong sách và đáp án in. Câu không khớp bài nào được đánh dấu là nằm ngoài danh mục.' if vi else 'Paste a question: the system finds its quantities, its kind, the best-matching modules and the most similar exercises among the 4,858 scanned from the four books, with the place in the book and the printed answer. A question that matches nothing is flagged as outside the catalogue.') + '</p><div id="analyser" data-src="../../exercises/catalog.json"></div>'
    write(f'{lang}/analyse/index.html', page(s['an_title'], h, lang, 'analyse/index.html', scripts=('analyse.js',)))
    h = f'<h1>{s["lab_title"]}</h1><p class="lead">' + ('Máy tính để kiểm bài làm tay: op-amp, decibel, bộ lọc, IC 555, ổn áp LM317, đổi cơ số. Nhập giá trị có hậu tố SI (10k, 2,2k, 0,0015u, 47n, 1M).' if vi else 'Calculators to check your hand work: op-amp, decibel, filters, 555 timer, LM317 regulator, base conversion. Values accept SI suffixes (10k, 2.2k, 0.0015u, 47n, 1M).') + '</p><div id="lab"></div>'
    write(f'{lang}/lab/index.html', page(s['lab_title'], h, lang, 'lab/index.html', scripts=('lab.js',)))

def written_pages(lang):
    s = S[lang]
    import exercises_body; importlib.reload(exercises_body)
    write(f'{lang}/written/index.html', page(s['wr_title'], exercises_body.written_body(lang), lang, 'written/index.html', scripts=('written.js',)))
    write(f'{lang}/written/paper.html', page(s['wr_title'], exercises_body.written_paper_body(lang), lang, 'written/paper.html', scripts=('written.js',)))

if __name__ == '__main__':
    main()
