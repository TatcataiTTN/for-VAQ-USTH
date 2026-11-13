"""Build the whole static site (vi/ + en/) for AE2.013 Thermal Systems from build/content/mNN.py + data/qbank/*.json + data/*.
Run:  python3 build/assemble.py && python3 build/build_site.py      (ONLY=m02,m03 limits the module pages that are regenerated)
Pages that are not built yet are generated as honest 'not built yet' stubs so that no navigation link is dead (rule R4: say what is not done)."""
import os, sys, json, importlib, random, html
sys.path.insert(0, os.path.dirname(__file__))
import hx
from hx import esc, deck, divider, callout, quiz_block, table, ul
from sitelib import page, write, ROOT
from modules import MODS, COURSE, BOOKS, BYID, DECKS, CLO, CO, TUT, slides_of
LANGS = ('vi', 'en')
S = {
 'vi': dict(home='Trang chủ', objectives='🎯 Sau module này bạn sẽ', time='Thời lượng (ước tính)', nq='Câu hỏi', orig='gốc', notes='Ghi chú chi tiết', quiz='Tự kiểm tra nhanh (10 câu, ưu tiên câu gốc)',
            practice='Luyện sâu', open_bank='Mở ngân hàng câu hỏi của module', nb='Notebook Jupyter', nb_txt='Tải notebook (đã chạy sẵn, có đầu ra thật):', prev='← Module trước', next='Module sau →',
            soon='Sắp có', openm='Mở bài giảng →', modules='Các module', clo='CLO', prac_title='Luyện tập theo module', exam_title='Luyện đề thi thử', src_title='Nguồn, độ phủ và lỗi của nguồn',
            books_title='Bản đồ nội dung sách', ex_title='Tra cứu bài tập có số', wr_title='Viết tay (chu trình nhiều bước)', an_title='Phân tích đề', cf_title='Khái niệm', lab_title='Phòng thí nghiệm',
            props_title='Tra bảng thuộc tính', slides_title='Slide của giảng viên', strip='📷 Slide gốc của giảng viên (bấm để phóng to)', slides_n='slide', hours='giờ lý thuyết',
            lecture='Bài giảng', selfcheck='Tự kiểm tra', written='Bài viết tay', errors='Lỗi và nghi vấn của nguồn', none_err='Chưa ghi nhận lỗi nào cho module này.', blank='slide trống',
            nbnone='Chưa có notebook cho module này.', stubnote='Phần này chưa được dựng trong lần làm việc hiện tại. Trạng thái và kế hoạch nằm trong CONTINUE.md của dự án.'),
 'en': dict(home='Home', objectives='🎯 After this module you will', time='Time (estimate)', nq='Questions', orig='original', notes='Detailed notes', quiz='Quick self-check (10 questions, originals first)',
            practice='Deep practice', open_bank='Open this module\'s question bank', nb='Jupyter notebook', nb_txt='Download the notebook (already executed, real outputs):', prev='← Previous module',
            next='Next module →', soon='Coming soon', openm='Open lesson →', modules='Modules', clo='CLO', prac_title='Practice by module', exam_title='Mock exams', src_title='Sources, coverage and source errors',
            books_title='Book content map', ex_title='Exercise finder', wr_title='Written practice (multi-step)', an_title='Question analyser', cf_title='Concept finder', lab_title='Lab',
            props_title='Property tables', slides_title='Lecturer slides', strip='📷 The lecturer\'s original slides (click to enlarge)', slides_n='slides', hours='lecture hours',
            lecture='Lecture', selfcheck='Self-check', written='Written practice', errors='Source errors and doubts', none_err='No errors recorded for this module yet.', blank='blank slides',
            nbnone='No notebook for this module yet.', stubnote='This part has not been built in the current work session. Status and plan are in the project\'s CONTINUE.md.'),
}

def loc(v, lang): return v.get(lang, v.get('en', '')) if isinstance(v, dict) else v
def jload(rel, default=None):
    p = os.path.join(ROOT, rel)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default

def localize(it, lang, r):
    d = dict(id=it['id'], kind=it['kind'], q=loc(it['q'], lang), topic=loc(it['topic'], lang), level=it['level'], src=loc(it['src'], lang), origin=it['origin'])
    if it.get('fig'): d['fig'] = r + it['fig']
    if it['kind'] == 'ess': d['sol'] = loc(it['sol'], lang)
    else:
        d['opts'] = [loc(o, lang) for o in it['opts']]; d['correct'] = it['correct']; d['explain'] = loc(it['explain'], lang)
    return d

def load_bank(mid): return jload(f'data/qbank/{mid}.json')
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

# ---------- slides ----------
_SL = None
def slide_index():
    global _SL
    if _SL is None: _SL = {(s['deck'], s['page']): s for s in (jload('data/slides/index.json') or [])}
    return _SL

def deck_tag(d, p): return f'Ch.{d[2]}·{p}' if d.startswith('ch') else f'Tut·{p}'
def slide_label(lang, d, p):
    base = f'Slide Ch.{d[2]} tr.{p}' if d.startswith('ch') else f'Tutorials I tr.{p}'
    if lang == 'en': base = f'Slide Ch.{d[2]} p.{p}' if d.startswith('ch') else f'Tutorials I p.{p}'
    t = slide_index().get((d, p), {}).get('title', '')
    return f'{base} — {t}' if t else base

def slide_strip(m, lang, r):
    s = S[lang]; items = []
    for d, p in slides_of(m): items.append((d, p, False))
    for d, a, b in m['blank_slides']:
        for p in range(a, b + 1): items.append((d, p, True))
    if not slide_index(): return ''
    out = f'<h2 id="slides">{s["strip"]}</h2><p class="slidestrip-cap">{len(items) - sum(1 for i in items if i[2])} {s["slides_n"]}' + (f' + {sum(1 for i in items if i[2])} {s["blank"]}' if any(i[2] for i in items) else '') + '</p><div class="slidestrip">'
    for d, p, blank in items:
        lab = slide_label(lang, d, p) + (' (blank)' if blank and lang == 'en' else ' (trống)' if blank else '')
        out += f'<a href="{r}assets/slides/{d}/p{p:02d}.jpg" data-cap="{esc(lab)}" class="{"blank" if blank else ""}"><img loading="lazy" src="{r}assets/slides/{d}/p{p:02d}.jpg" alt="{esc(lab)}"><span class="n">{deck_tag(d, p)}</span></a>'
    return out + '</div>'

def est_hours(m):
    tot = sum(len(slides_of(x)) for x in MODS)
    return COURSE['hours']['lecture'] * len(slides_of(m)) / tot

def module_page(m, c, bank, lang):
    s = S[lang]; rel = f'modules/{m["slug"]}/index.html'; r = '../../../'
    nq = len(bank['items']) if bank else 0; ng = sum(1 for i in bank['items'] if i['origin'] == 'goc') if bank else 0
    slides = []; P = len(c['parts'])
    for k, part in enumerate(c['parts'], 1):
        slides.append((divider(k, P, part['title'], part['bullets']), True))
        slides += [(x, False) for x in part['slides']]
    h = f'<div class="crumbs"><a href="../../index.html">{s["home"]}</a> › {s["modules"]} › {m["id"].upper()}</div>'
    h += f'<h1>{m["id"][1:]}. {esc(m[lang])}</h1><p class="lead">{c.get("subtitle", "")}</p>'
    h += (f'<p><span class="tag">{s["clo"]}: {", ".join(m["clo"])}</span><span class="tag">{s["time"]}: ≈ {est_hours(m):.1f} {s["hours"]}</span>'
          f'<span class="tag">{len(slides_of(m))} {s["slides_n"]}</span><span class="tag exam">{s["nq"]}: {nq} ({ng} {s["orig"]})</span></p>')
    h += '<p class="srcnote">' + ' · '.join(esc(x) for x in m['src']) + f' · <a href="../../books/index.html#overview">{s["books_title"]}</a></p>'
    toc = [('#slides', s['strip'].split(' (')[0]), ('#lecture', s['lecture']), ('#notes', s['notes']), ('#selfcheck', s['selfcheck']), ('#practice', s['practice']), ('#nb', s['nb']), ('#errors', s['errors'])]
    h += callout('good', s['objectives'], ul(c['objectives']))
    h += '<div class="stickytoc">' + ''.join(f'<a href="{a}">{esc(t)}</a>' for a, t in toc) + '</div>'
    h += slide_strip(m, lang, r)
    h += f'<h2 id="lecture">{s["lecture"]}</h2>' + deck(slides, 'd-' + m['id'])
    h += f'<h2 id="notes">{s["notes"]}</h2>' + c['notes']
    if bank:
        h += f'<h2 id="selfcheck">{s["quiz"]}</h2>' + quiz_block('q-' + m['id'], [localize(i, lang, r) for i in pick_quiz(bank)])
        h += f'<h2 id="practice">{s["practice"]}</h2><p><a class="btn" href="../../practice/{m["id"]}.html">{s["open_bank"]} ({nq} + {len(bank["essays"])})</a></p>'
    nbs = notebooks(m)
    h += f'<h2 id="nb">{s["nb"]}</h2>' + (f'<p>{s["nb_txt"]}</p><ul>' + ''.join(f'<li><a href="{r}notebooks/{fn}" download>{fn}</a> ({l.upper()})</li>' for l, fn in nbs) + '</ul>' if nbs else f'<p class="muted">{s["nbnone"]}</p>')
    notes = (jload(f'data/verify/{m["id"]}_notes.json') or {}).get(lang, [])
    h += f'<h2 id="errors">{s["errors"]}</h2>' + (ul([esc(x) if not x.startswith('<') else x for x in notes]) if notes else f'<p class="muted">{s["none_err"]}</p>')
    i = MODS.index(m); nav = '<div class="modnav">'
    if i > 0: nav += f'<a href="../{MODS[i-1]["slug"]}/index.html">{s["prev"]}: {esc(MODS[i-1][lang])}</a>'
    if i < len(MODS) - 1: nav += f'<a href="../{MODS[i+1]["slug"]}/index.html">{s["next"]}: {esc(MODS[i+1][lang])}</a>'
    h += nav + '</div>' + f'<div id="resume-mark" data-title="{esc(m["id"].upper() + " · " + m[lang])}" hidden></div>'
    write(f'{lang}/{rel}', page(m[lang], h, lang, rel, c.get('subtitle', ''), scripts=('deck.js', 'quiz.js', 'strip.js', 'resume.js')))

def bank_page(m, bank, lang):
    s = S[lang]; rel = f'practice/{m["id"]}.html'; r = '../../'
    data = dict(module=m['id'], items=[localize(i, lang, r) for i in bank['items']], essays=[localize(e, lang, r) for e in bank['essays']])
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    h = (f'<div class="crumbs"><a href="../index.html">{s["home"]}</a> › <a href="index.html">{s["prac_title"]}</a> › {m["id"].upper()}</div>'
         f'<h1>{m["id"][1:]}. {esc(m[lang])}</h1><p class="srcnote">' + ' · '.join(esc(x) for x in m['src']) + '</p>'
         f'<div id="bank"></div><script type="application/json" id="bank-data">{js}</script>')
    write(f'{lang}/{rel}', page(m[lang], h, lang, rel, scripts=('bank.js',)))

def stub_page(lang, rel, title):
    s = S[lang]
    write(f'{lang}/{rel}', page(title, f'<h1>{esc(title)}</h1>' + callout('warn', s['soon'], f'<p>{s["stubnote"]}</p>'), lang, rel))

def main():
    banks = {m['id']: load_bank(m['id']) for m in MODS}
    contents = {}
    only = set(filter(None, os.environ.get('ONLY', '').split(',')))
    for lang in LANGS:
        for m in MODS:
            if only and m['id'] not in only:
                contents[(m['id'], lang)] = os.path.exists(os.path.join(ROOT, f'{lang}/modules/{m["slug"]}/index.html')) or None
                continue
            c = load_content(m['id'], lang); contents[(m['id'], lang)] = c
            b = banks[m['id']]
            if c: module_page(m, c, b, lang)
            if b: bank_page(m, b, lang)
        index_page(lang, contents, banks); practice_index(lang, banks); exam_page(lang, banks); slides_page(lang); optional_pages(lang, banks)
    write('index.html', f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=vi/index.html"><title>{COURSE["code"]} {COURSE["en"]}</title></head>'
          '<body><p><a href="vi/index.html">Tiếng Việt</a> · <a href="en/index.html">English</a></p></body></html>')
    print('built', sum(1 for v in contents.values() if v), 'module pages')

def index_page(lang, contents, banks):
    s = S[lang]; vi = lang == 'vi'; H = COURSE['hours']
    intro = (f'<h1>{COURSE["code"]} · {COURSE[lang]}</h1><p class="lead">' + (
        f'Hệ thống tự học song ngữ bám đề cương USTH, slide của giảng viên và ba tài liệu tham khảo: chu trình công suất khí, chu trình lạnh và điều hoà trên tàu bay, quá trình cháy, dòng nén được. '
        f'{COURSE["ects"]} ECTS · {H["lecture"]} giờ lý thuyết · {H["lab"]} giờ thực hành · {H["tutorial"]} giờ bài tập (đề cương ghi 0 giờ nhưng giảng viên có bộ Tutorials I) · học trước: {COURSE["prereq"]}.'
        if vi else
        f'Bilingual self-study system following the USTH syllabus, the lecturer\'s slides and the three references: gas power cycles, refrigeration and aircraft air conditioning, combustion, compressible flow. '
        f'{COURSE["ects"]} ECTS · {H["lecture"]} h lecture · {H["lab"]} h lab · {H["tutorial"]} h tutorial (the syllabus says 0 h but the lecturer has a Tutorials I set) · prerequisite: {COURSE["prereq"]}.') + '</p>')
    h = intro + '<div id="resume"></div>'
    h += callout('info', 'CO / CLO' + (' (đề cương)' if vi else ' (syllabus)'), ul([f'<b>{k}</b>: {esc(v[lang])}' for k, v in CO.items()] + [f'<b>{k}</b>: {esc(v[lang])}' for k, v in CLO.items()]))
    h += f'<h2 id="modules">{s["modules"]}</h2><div class="grid">'
    for m in MODS:
        b = banks[m['id']]; c = contents[(m['id'], lang)]
        cnt = f'<p>{s["nq"]}: {len(b["items"])} ({sum(1 for i in b["items"] if i["origin"]=="goc")} {s["orig"]}) + {len(b["essays"])}</p>' if b else ''
        inner = f'<div class="num">MODULE {m["id"][1:]} · {", ".join(m["clo"])}</div><h3>{esc(m[lang])}</h3><p>{len(slides_of(m))} {s["slides_n"]} · ≈ {est_hours(m):.1f} {s["hours"]}</p>{cnt}'
        if c: h += f'<a class="mod-card" href="modules/{m["slug"]}/index.html">{inner}<p><b>{s["openm"]}</b></p></a>'
        else: h += f'<div class="mod-card" style="opacity:.55;cursor:default">{inner}<p>{s["soon"]}</p></div>'
    h += '</div>'
    # coverage matrix CLO x module (counts from build/modules.py)
    head = ['CLO'] + [m['id'].upper() for m in MODS]
    rows = [[f'<b>{k}</b>'] + ['●' if k in m['clo'] else '' for m in MODS] for k in CLO]
    rows.append([('Số slide' if vi else 'Slides')] + [str(len(slides_of(m))) for m in MODS])
    for bk in ('cengel', 'elsayed', 'farokhi'):
        rows.append([BOOKS[bk]['short']] + [esc(m['books'][bk]) for m in MODS])
    h += f'<h2>{"Ma trận độ phủ: CLO × module × slide × sách" if vi else "Coverage matrix: CLO × module × slides × books"}</h2>' + table(head, rows, 'left')
    h += '<p class="srcnote">' + ('Ánh xạ module–sách là ánh xạ cấp chương; ánh xạ cấp mục nằm ở Bản đồ sách. Giờ lý thuyết theo module là ước tính theo số slide (đề cương không chia giờ theo chương).' if vi else
                                  'The module–book mapping is chapter level; section level is in the Book map. Lecture hours per module are an estimate by slide count (the syllabus does not split hours by chapter).') + '</p>'
    mods_json = json.dumps([dict(id=m['id'], title=m[lang], href=f'practice/{m["id"]}.html') for m in MODS], ensure_ascii=False).replace("'", '&#39;')
    h += '<h2>' + ('Tiến độ của bạn' if vi else 'Your progress') + f'</h2><div id="progress" data-mods=\'{mods_json}\'><p class="muted">…</p></div>'
    write(f'{lang}/index.html', page(COURSE[lang], h, lang, 'index.html', scripts=('progress.js', 'resume.js')))

def practice_index(lang, banks):
    s = S[lang]
    rows = [[m['id'][1:], f'<a href="{m["id"]}.html">{esc(m[lang])}</a>', len(b['items']), sum(1 for i in b['items'] if i['origin'] == 'goc'), len(b['essays'])]
            for m in MODS for b in [banks[m['id']]] if b]
    head = ['#', 'Module', s['nq'], s['orig'], 'Worked' if lang == 'en' else 'Tự luận']
    h = f'<h1>{s["prac_title"]}</h1>' + (table(head, rows, 'left') if rows else callout('warn', s['soon'], f'<p>{s["stubnote"]}</p>'))
    write(f'{lang}/practice/index.html', page(s['prac_title'], h, lang, 'practice/index.html'))

def exam_page(lang, banks):
    """Mock exams: hub (index.html), runner (run.html), A4 print view (print.html) and the question pool + fixed papers (data.json); see build/exams.py."""
    import exams; importlib.reload(exams)
    s = S[lang]
    if not any(banks.values()):
        stub_page(lang, 'exam/index.html', s['exam_title']); return
    defs = exams.build(banks); pool = []
    for m in MODS:
        b = banks[m['id']]
        if not b: continue
        for it in b['items']:
            if exams.eligible(it):
                d = localize(it, lang, '../../'); pool.append(dict(id=d['id'], m=m['id'], q=d['q'], o=d['opts'], c=d['correct'], e=d['explain'], s=d['src'], l=d['level'], g=int(it['origin'] == 'goc'), **({'f': d['fig']} if 'fig' in d else {})))
    data = dict(lang=lang, mods={m['id']: m[lang] for m in MODS}, pool=pool, papers=defs['papers'], mixed=defs['mixed'], types=defs['types'])
    write(f'{lang}/exam/data.json', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    lead = {'vi': 'Đề giữa kỳ, cuối kỳ, đề nhanh, đề tùy chỉnh và các đề luyện hỗn hợp, lấy từ ngân hàng câu hỏi của site. Đề cương không nêu hình thức thi: cấu trúc đề do site tự thiết kế (xem khung dưới). Có đồng hồ, chế độ không quay lại, bảng số câu, chấm theo module, làm lại câu sai và bản in A4 có đáp án.',
            'en': 'Midterm, final, speed and custom exams plus mixed practice sets, drawn from the site\'s question bank. The syllabus does not state an exam format: the structure is this site\'s own design (see the box below). With a timer, a no-going-back mode, a question palette, scoring by module, redo of the wrong answers and an A4 print version with the key.'}[lang]
    for page_name, mode, head in (('index', 'hub', f'<h1>{s["exam_title"]}</h1><p class="lead">{lead}</p>'), ('run', 'run', ''), ('print', 'print', '')):
        h = head + f'<div id="exam" data-mode="{mode}" data-src="data.json"></div>'
        write(f'{lang}/exam/{page_name}.html', page(s['exam_title'], h, lang, f'exam/{page_name}.html', scripts=('exam.js',)))

def slides_page(lang):
    s = S[lang]; vi = lang == 'vi'; idx = slide_index(); h = f'<h1>{s["slides_title"]}</h1>'
    if not idx: stub_page(lang, 'slides/index.html', s['slides_title']); return
    h += '<p class="lead">' + ('Toàn bộ 296 slide của giảng viên (6 bộ), kèm tiêu đề và module dùng slide đó. Bấm ảnh để mở bản lớn.' if vi else 'All 296 slides of the lecturer (6 decks) with their titles and the module that uses each.') + '</p>'
    owner = {}
    for m in MODS:
        for d, p in slides_of(m): owner[(d, p)] = m['id']
        for d, a, b in m['blank_slides']:
            for p in range(a, b + 1): owner[(d, p)] = m['id'] + ' (blank)'
    for d, info in DECKS.items():
        h += f'<h2>{esc(info[lang])} ({info["pages"]})</h2><div class="slidestrip" style="flex-wrap:wrap;overflow:visible">'
        for p in range(1, info['pages'] + 1):
            t = idx.get((d, p), {}).get('title', ''); o = owner.get((d, p), '–')
            lab = f'{slide_label(lang, d, p)} · {o}'
            h += f'<a href="../assets/slides/{d}/p{p:02d}.jpg" data-cap="{esc(lab)}"><img loading="lazy" src="../assets/slides/{d}/p{p:02d}.jpg" alt="{esc(lab)}"><span class="n">{deck_tag(d, p)} · {o.split(" ")[0]}</span></a>'
        h += '</div>'
    write(f'{lang}/slides/index.html', page(s['slides_title'], h, lang, 'slides/index.html', scripts=('strip.js',)))

def optional_pages(lang, banks):
    """Pages whose builders live in separate files (sources_body, bookmap_body, exercises_body, written, props, lab, analyse, concepts).
    Each builder is optional: when its module or data is missing the page is an honest stub."""
    s = S[lang]
    spec = [('sources/index.html', s['src_title'], 'sources_body', 'body', (lang, banks), ()),
            ('books/index.html', s['books_title'], 'bookmap_body', 'body', (lang,), ('bookmap.js',)),
            ('exercises/index.html', s['ex_title'], 'exercises_body', 'exercises_body', (lang,), ('exercises.js', 'bookmap.js')),
            ('written/index.html', s['wr_title'], 'exercises_body', 'written_body', (lang,), ('written.js',)),
            ('written/paper.html', s['wr_title'], 'exercises_body', 'written_paper_body', (lang,), ('written.js',)),
            ('props/index.html', s['props_title'], 'props_body', 'body', (lang,), ('props.js',)),
            ('lab/index.html', s['lab_title'], 'lab_body', 'body', (lang,), ('lab.js',)),
            ('analyse/index.html', s['an_title'], 'analyse_body', 'body', (lang,), ('analyse.js',)),
            ('concepts/index.html', s['cf_title'], 'concepts_body', 'body', (lang,), ('concepts.js',))]
    for rel, title, modname, fn, args, scripts in spec:
        try:
            mod = importlib.import_module(modname); importlib.reload(mod); body = getattr(mod, fn)(*args)
        except (ImportError, AttributeError, FileNotFoundError) as e:
            stub_page(lang, rel, title); continue
        write(f'{lang}/{rel}', page(title, body, lang, rel, scripts=scripts))

if __name__ == '__main__':
    main()
