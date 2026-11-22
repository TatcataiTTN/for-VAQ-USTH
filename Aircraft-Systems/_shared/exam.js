/* Mock exams (bilingual): hub (midterm, final, speed, custom, mixed, one test per module, hard level 3, Tooley Revision Papers, written, full paper, review of mistakes), runner (intro, one question per screen, timer, forward-only or free navigation with
   a question palette and flags, keyboard shortcuts, auto-submit), result (score, mark out of 10, accuracy by module, review, redo only the mistakes) and an A4 print view
   (paper + answer sheet + answer key with explanations).  Questions come from data.json (pool + fixed papers); random draws are made here.
   Results are kept in localStorage 'ae2021:prog:exam:<id>' and feed the progress panel; a run in progress survives a page reload (sessionStorage). */
(function () {
  var root = document.getElementById('exam'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), MODE = root.getAttribute('data-mode') || 'hub', LET = 'ABCDEF';
  var X = {
    vi: { load: 'Đang tải đề…', fail: 'Không tải được đề: ', start: '▶ Bắt đầu làm bài', print: '🖨 In đề + đáp án (A4)', best: 'tốt nhất', none: 'chưa làm', paper: 'Đề ', rnd: '🎲 Đề ngẫu nhiên', back: '◀ Tất cả đề',
      q: ' câu', min: ' phút', fwd: 'không quay lại câu trước', free: 'đi lại tự do giữa các câu', mods: 'Phạm vi', all: 'mọi module', quota: 'Số câu theo module',
      hub: { entry: 'Kiểm tra đầu vào', midterm: 'Giữa kỳ (Midterm)', final: 'Cuối kỳ (Final)', speed: 'Nhanh (Speed)', custom: 'Tùy chỉnh (Custom)', mixed: 'Đề luyện hỗn hợp', module: 'Kiểm tra theo module', hard: 'Thử thách mức 3 (Hard)', tooley: 'Đề ôn của Tooley (Revision Papers)', written: 'Tự luận (Written)', full: 'Đề tổng hợp: trắc nghiệm + tự luận', review: 'Ôn lại câu làm sai' },
      desc: { entry: 'Hai mươi câu về khái niệm số cơ bản của Floyd Chương 1 (analog và số, bit, chu kỳ, tần số, độ rộng xung, cổng cơ bản, IC số) để biết bạn đã sẵn sàng cho học phần chưa. Làm trước khi học module 01.', midterm: 'Nửa đầu học phần (module 01-04). Làm một mạch, không quay lại câu trước (kiểu Moodle).', final: 'Toàn bộ 9 module; được đi lại giữa các câu, có bảng số câu và cờ đánh dấu.',
        speed: 'Rút ngẫu nhiên từ mọi module, mỗi lần một đề khác; thời gian ngắn để luyện tốc độ.', custom: 'Chọn module, số câu, thời gian và có cho quay lại hay không.', mixed: 'Bốn đề cố định 20 câu trộn mọi module, 30 phút, đi lại tự do.',
        module: 'Mỗi module một đề 15 câu, 20 phút: dùng để kiểm tra ngay sau khi học xong module đó.', hard: 'Chỉ câu mức 3 (nhiều bước, tính toán, phân tích), tối đa 4 câu mỗi module, hai đề không trùng câu.',
        tooley: 'Các đề ôn trong Phụ lục 2 của giáo trình Tooley: mỗi đề gốc có 20 câu, 3 lựa chọn, 25 phút, không dùng máy tính. Thẻ ghi số câu của đề gốc mà ngân hàng đang có.',
        written: 'Sáu bài tự luận có đáp án in của giáo trình, 60 phút. Làm trên giấy hoặc gõ vào ô ghi chú, nộp rồi đối chiếu lời giải và tự chấm theo thang điểm của bài.',
        full: 'Phần I trắc nghiệm (20 câu, 30 phút, mỗi câu 2 điểm) rồi phần II tự luận (3 bài, 60 phút, mỗi bài 20 điểm): tổng 100 điểm, quy về thang 10.',
        review: 'Rút các câu bạn đã làm sai ở Ngân hàng câu hỏi hoặc ở các đề (lần làm gần nhất còn sai). Câu nào đúng sẽ rời khỏi danh sách.' },
      assume: 'Cấu trúc các loại đề này do site đặt: đề cương AE2.021 không nêu hình thức thi. Phạm vi giữa kỳ (module 01-04), số câu, thời gian và số câu theo module là giả định, chỉnh được ở mục Tùy chỉnh. Đề trắc nghiệm chỉ dùng câu nhiều lựa chọn trong ngân hàng (không dùng câu đúng/sai); các đề A, B, C của cùng một loại không trùng câu; câu gốc của sách được ưu tiên. Điểm từng bài tự luận (5, 10 hoặc 15 theo mức) và điểm tổng hợp là giả định của site; phần tự luận do bạn tự chấm. Đề ôn Tooley là đề gốc của sách nhưng chỉ gồm những câu đã vào ngân hàng.',
      cust: { mods: 'Module', n: 'Số câu', min: 'Thời gian (phút)', fwd: 'Không cho quay lại câu trước', orig: 'Chỉ câu gốc của sách', go: '▶ Tạo đề và bắt đầu', none: 'Hãy chọn ít nhất một module.', few: function (a, b) { return 'Các module đã chọn chỉ có ' + a + ' câu, sẽ rút ' + b + '.'; } },
      intro: function (n, m, fwd) { return n + ' câu, ' + m + ' phút, ' + (fwd ? 'KHÔNG quay lại câu trước (hết câu nào là qua câu đó)' : 'được đi lại giữa các câu'); },
      rules: ['Không có phản hồi đúng/sai cho tới khi nộp bài.', 'Câu bỏ trống tính 0 điểm; không trừ điểm câu sai.', 'Hết giờ bài tự nộp.', 'Phím tắt: A-F chọn đáp án, → hoặc Enter sang câu sau' + ', ← về câu trước (nếu được phép), M đánh dấu câu.'],
      qn: function (i, n) { return 'Câu ' + i + ' / ' + n; }, answered: function (a, n) { return 'Đã trả lời ' + a + ' / ' + n; }, prev: '◀ Câu trước', next: 'Câu sau ▶', finish: 'Nộp bài', flag: '⚑ Đánh dấu', unflag: '⚑ Bỏ đánh dấu',
      sure: function (blank) { return blank ? 'Còn ' + blank + ' câu chưa trả lời (tính 0 điểm). Nộp bài?' : 'Nộp bài và xem kết quả?'; }, sureLast: 'Đây là câu cuối. Nộp bài?', up: '⏱ Hết giờ · bài đã tự nộp.',
      res: 'Kết quả', score: 'Điểm', mark: 'Thang 10', time: 'Thời gian', bymod: 'Theo module', review: 'Xem lại bài', onlyWrong: 'Chỉ câu sai hoặc bỏ trống', allq: 'Tất cả câu', redo: 'Làm lại các câu sai (có phản hồi ngay)', again: 'Làm đề khác', saved: 'Đã lưu vào bảng tiến độ.',
      yours: 'Bạn chọn', correct: 'Đáp án đúng', blank: 'bỏ trống', ok: '✔ Đúng', bad: '✘ Sai', src: 'Nguồn: ', pr: 'Luyện lại các câu sai', pr1: 'Chọn đáp án: có phản hồi ngay.', done: 'Đã hết các câu.', noItems: 'Không có câu hỏi nào.', unknown: 'Không có đề này. ',
      wr: { part1: 'Phần I · Trắc nghiệm', part2: 'Phần II · Tự luận', intro: function (n, marks, m) { return n + ' bài tự luận, ' + marks + ' điểm, ' + m + ' phút'; }, rules: ['Làm trên giấy hoặc gõ nháp vào ô ghi chú (ghi chú chỉ lưu trong tab này).', 'Bấm Nộp bài để thấy lời giải và đáp án in; sau đó tự chấm từng bài.', 'Điểm tự chấm không phải điểm thi thật: thang điểm từng bài là giả định của site.'],
      problem: 'Bài ', marks: 'điểm', notes: 'Ghi chú của bạn (không bắt buộc)', submit: 'Nộp bài và xem lời giải', selfmark: 'Tự chấm', sol: 'Lời giải và đáp án', yourmark: 'Điểm của bạn', total: 'Tổng', done: 'Xong, tính điểm', cont: 'Sang phần II: tự luận ▶', mcqpart: 'Phần trắc nghiệm', wpart: 'Phần tự luận', all: 'Tổng cộng', book: 'Đề gốc 20 câu, ngân hàng có', blankLine: 'Chỗ làm bài', noans: '(chưa chấm)' },
      mist: { none: 'Chưa có câu nào làm sai: hãy làm vài câu ở Ngân hàng câu hỏi hoặc một đề trước.' },
      printTitle: 'Đề thi thử', printName: 'Họ tên: ', printId: 'Mã số: ', printDate: 'Ngày: ', printInst: 'Chọn một đáp án cho mỗi câu. Không dùng tài liệu. Thời gian: ', sheet: 'Phiếu trả lời', key: 'Đáp án và giải thích', doPrint: '🖨 In trang này' },
    en: { load: 'Loading the exam…', fail: 'Could not load the exam: ', start: '▶ Start', print: '🖨 Print paper + key (A4)', best: 'best', none: 'not taken', paper: 'Paper ', rnd: '🎲 Random paper', back: '◀ All exams',
      q: ' questions', min: ' min', fwd: 'no going back', free: 'free navigation', mods: 'Scope', all: 'every module', quota: 'Questions per module',
      hub: { entry: 'Entry test', midterm: 'Midterm', final: 'Final', speed: 'Speed', custom: 'Custom', mixed: 'Mixed practice sets', module: 'One test per module', hard: 'Hard (level 3)', tooley: 'Tooley Revision Papers', written: 'Written', full: 'Full paper: multiple choice + written', review: 'Review your mistakes' },
      desc: { entry: 'Twenty questions on the basic digital concepts of Floyd Chapter 1 (analog and digital, bits, period, frequency, pulse width, basic gates, digital ICs) to see whether you are ready for the course. Take it before module 01.', midterm: 'First half of the course (modules 01-04). Work straight through; you cannot go back to an earlier question (Moodle style).', final: 'All 9 modules; you may move between questions, with a question palette and flags.',
        speed: 'A fresh random draw from every module each time; a short time limit to train speed.', custom: 'Choose modules, number of questions, time and whether going back is allowed.', mixed: 'Four fixed sets of 20 questions mixed from every module, 30 minutes, free navigation.',
        module: 'One 15-question, 20-minute test per module: use it right after finishing that module.', hard: 'Level 3 only (multi-step, calculation, analysis), at most 4 questions per module, two papers that share no question.',
        tooley: 'The revision papers in Appendix 2 of Tooley: each original paper has 20 questions, 3 options, 25 minutes, no calculator. The card shows how many questions of the original paper the bank holds.',
        written: 'Six worked problems with the printed answer of the textbook, 60 minutes. Work on paper or in the notes box, submit, then compare with the solution and mark yourself on the problem\'s scale.',
        full: 'Part I multiple choice (20 questions, 30 minutes, 2 marks each) then part II written (3 problems, 60 minutes, 20 marks each): 100 marks in all, scaled to 10.',
        review: 'Draws the questions you got wrong in the Question bank or in the exams (still wrong at your latest attempt). A question leaves the list once you answer it correctly.' },
      assume: 'The structure of these exam types is this site\'s own design: the AE2.021 syllabus does not state an exam format. The midterm scope (modules 01-04), the number of questions, the time limits and the questions per module are assumptions, adjustable under Custom. The multiple-choice papers use only multi-option items of the bank (no true/false); papers A, B, C of one type share no question; textbook originals are favoured. The marks of each written problem (5, 10 or 15 by level) and of the full paper are the site\'s assumptions; you mark the written part yourself. The Tooley papers are the book\'s own but contain only the questions that are already in the bank.',
      cust: { mods: 'Modules', n: 'Questions', min: 'Time (minutes)', fwd: 'Do not allow going back', orig: 'Textbook originals only', go: '▶ Build the exam and start', none: 'Choose at least one module.', few: function (a, b) { return 'The chosen modules have only ' + a + ' questions; ' + b + ' will be drawn.'; } },
      intro: function (n, m, fwd) { return n + ' questions, ' + m + ' minutes, ' + (fwd ? 'NO going back (once you leave a question it is final)' : 'free navigation between questions'); },
      rules: ['No right/wrong feedback until you submit.', 'A blank question scores 0; wrong answers are not penalised.', 'The paper is submitted automatically when time is up.', 'Shortcuts: A-F choose an answer, → or Enter next question' + ', ← previous (when allowed), M flag the question.'],
      qn: function (i, n) { return 'Question ' + i + ' / ' + n; }, answered: function (a, n) { return 'Answered ' + a + ' / ' + n; }, prev: '◀ Previous', next: 'Next ▶', finish: 'Submit', flag: '⚑ Flag', unflag: '⚑ Unflag',
      sure: function (blank) { return blank ? blank + ' question' + (blank === 1 ? ' is' : 's are') + ' unanswered (0 marks). Submit?' : 'Submit and see the result?'; }, sureLast: 'This is the last question. Submit?', up: '⏱ Time is up · the paper was submitted.',
      res: 'Result', score: 'Score', mark: 'Out of 10', time: 'Time', bymod: 'By module', review: 'Review', onlyWrong: 'Wrong or blank only', allq: 'All questions', redo: 'Redo the wrong ones (instant feedback)', again: 'Take another paper', saved: 'Saved to the progress panel.',
      yours: 'You chose', correct: 'Correct answer', blank: 'blank', ok: '✔ Correct', bad: '✘ Wrong', src: 'Source: ', pr: 'Redo the mistakes', pr1: 'Choose an answer: you get feedback at once.', done: 'No more questions.', noItems: 'No questions.', unknown: 'Unknown exam. ',
      wr: { part1: 'Part I · Multiple choice', part2: 'Part II · Written', intro: function (n, marks, m) { return n + ' written problems, ' + marks + ' marks, ' + m + ' minutes'; }, rules: ['Work on paper or type rough notes in the box (notes stay only in this tab).', 'Press Submit to see the solutions and the printed answers; then mark each problem yourself.', 'The self-marked score is not a real exam score: the marks of each problem are the site\'s assumption.'],
      problem: 'Problem ', marks: 'marks', notes: 'Your notes (optional)', submit: 'Submit and see the solutions', selfmark: 'Mark yourself', sol: 'Solution and answer', yourmark: 'Your marks', total: 'Total', done: 'Done, compute the score', cont: 'Go to part II: written ▶', mcqpart: 'Multiple-choice part', wpart: 'Written part', all: 'Total', book: 'Original paper has 20 questions, the bank holds', blankLine: 'Working space', noans: '(not marked)' },
      mist: { none: 'No mistakes yet: try some questions in the Question bank or an exam first.' },
      printTitle: 'Mock exam', printName: 'Name: ', printId: 'ID: ', printDate: 'Date: ', printInst: 'Choose one answer per question. Closed book. Time: ', sheet: 'Answer sheet', key: 'Answer key and explanations', doPrint: '🖨 Print this page' }
  }[L];
  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }
  function get(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  function sget(k) { try { return JSON.parse(sessionStorage.getItem(k)); } catch (e) { return null; } }
  function sput(k, v) { try { if (v === null) sessionStorage.removeItem(k); else sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  function tm(s) { s = Math.max(0, Math.round(s)); var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), r = s % 60; return (h ? h + ':' + ('0' + m).slice(-2) : m) + ':' + ('0' + r).slice(-2); }
  function fmt(x) { return (Math.round(x * 10) / 10).toString().replace('.', L === 'vi' ? ',' : '.'); }
  function shuffle(a, rnd) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function qs() { var o = {}; location.search.replace(/^\?/, '').split('&').forEach(function (p) { if (!p) return; var kv = p.split('='); o[decodeURIComponent(kv[0])] = decodeURIComponent(kv[1] || ''); }); return o; }
  function modName(m) { return D.mods[m] ? m.toUpperCase() + ' · ' + D.mods[m] : m.toUpperCase(); }
  var WKEY = 'ae2021:prog:wrong';
  function noteWrong(qs, ans) {                      // remember the latest result of every question answered in an exam (feeds the review exam and the mistake log)
    var w = get(WKEY, {}), now = Date.now(); qs.forEach(function (q, i) { if (ans[i] === undefined) return; w[q.id] = { k: ans[i] === q.c ? 'r' : 'w', n: ((w[q.id] || {}).n || 0) + (ans[i] === q.c ? 0 : 1), t: now }; }); put(WKEY, w);
  }
  function wrongIds() {                              // wrong at the latest attempt: exam map + question bank state
    var out = {}, w = get(WKEY, {});
    Object.keys(w).forEach(function (id) { if (BY[id] && w[id].k === 'w') out[id] = 1; });
    Object.keys(D.mods).forEach(function (m) { var b = get('ae2021:bank:' + m, null); if (!b || !b.ans) return; Object.keys(b.ans).forEach(function (id) { var q = BY[id]; if (!q) return; if (b.ans[id] !== q.c && !(w[id] && w[id].k === 'r')) out[id] = 1; }); });
    return Object.keys(out);
  }
  var D = null, BY = {}, POOL = {}, WBY = {};
  root.appendChild(el('p', 'muted', X.load));
  fetch(root.getAttribute('data-src')).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); }).then(function (j) {
    D = j; D.pool.forEach(function (it) { BY[it.id] = it; (POOL[it.m] = POOL[it.m] || []).push(it); }); (D.wpool || []).forEach(function (w) { WBY[w.id] = w; });
    D.papers = D.papers.concat(D.mixed); root.innerHTML = ''; ({ hub: hub, run: run, print: printView })[MODE]();
  }).catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });

  // ------------------------------------------------------------------ random draws (same rules as the fixed papers: levels mixed, textbook originals favoured)
  // level targets per module so the WHOLE paper has the requested mix (same algorithm as build/exams.py allocate(): global largest remainder, per-module floors, leftovers by fractional part)
  function allocate(quota, W) {
    var ms = Object.keys(quota), lvs = [1, 2, 3], n = 0, tot = {}, t = {}, need = {}, slots = {};
    ms.forEach(function (m) { n += quota[m]; });
    var sum = 0; lvs.forEach(function (lv) { tot[lv] = Math.floor(n * (W[lv] || 0)); sum += tot[lv]; });
    lvs.slice().sort(function (a, b) { return ((n * (W[b] || 0) - tot[b]) - (n * (W[a] || 0) - tot[a])) || (b - a); }).slice(0, n - sum).forEach(function (lv) { tot[lv]++; });
    ms.forEach(function (m) { t[m] = {}; var s = 0; lvs.forEach(function (lv) { t[m][lv] = Math.floor(quota[m] * (W[lv] || 0)); s += t[m][lv]; }); slots[m] = quota[m] - s; });
    lvs.forEach(function (lv) { var s = 0; ms.forEach(function (m) { s += t[m][lv]; }); need[lv] = tot[lv] - s; });
    var cand = []; ms.forEach(function (m) { lvs.forEach(function (lv) { cand.push({ f: quota[m] * (W[lv] || 0) - t[m][lv], r: Math.random(), m: m, lv: lv }); }); });
    cand.sort(function (a, b) { return (b.f - a.f) || (b.r - a.r); });
    cand.forEach(function (c) { if (slots[c.m] > 0 && need[c.lv] > 0) { t[c.m][c.lv]++; slots[c.m]--; need[c.lv]--; } });
    lvs.forEach(function (lv) { ms.forEach(function (m) { while (slots[m] > 0 && need[lv] > 0) { t[m][lv]++; slots[m]--; need[lv]--; } }); });
    return t;
  }
  function draw(spec) {                                   // spec: {quota:{m:k}} or {mods:[..], n:k}, levels, orig
    var quota = spec.quota; if (!quota) { quota = {}; var ms = spec.mods.filter(function (m) { return POOL[m]; }), per = Math.floor(spec.n / ms.length), extra = spec.n - per * ms.length;
      ms.forEach(function (m) { quota[m] = per; }); shuffle(ms.slice(), Math.random).slice(0, extra).forEach(function (m) { quota[m]++; }); }
    var W = spec.levels || { 1: .35, 2: .5, 3: .15 }, out = [], TG = allocate(quota, W);
    Object.keys(quota).sort().forEach(function (m) {
      var k = quota[m], items = (POOL[m] || []).filter(function (it) { return !spec.orig || it.g; }); if (!k || !items.length) return;
      var by = {}; items.forEach(function (it) { (by[it.l] = by[it.l] || []).push(it); });
      Object.keys(by).forEach(function (lv) { by[lv].sort(function (a, b) { return (Math.random() + (a.g ? 0 : .5)) - (Math.random() + (b.g ? 0 : .5)); }); });
      var target = TG[m];
      var got = []; [1, 2, 3].forEach(function (lv) { var t = (by[lv] || []).splice(0, target[lv]); got = got.concat(t); });
      while (got.length < k) { var lv = Object.keys(by).sort(function (a, b) { return by[b].length - by[a].length; })[0]; if (lv === undefined || !by[lv].length) break; got.push(by[lv].shift()); }
      shuffle(got, Math.random).forEach(function (it) { out.push(it.id); });
    });
    return out;
  }
  // ------------------------------------------------------------------ the exam to run, from the query string
  function paperTitle(p) { return (X.hub[p.type] || p.type) + ' · ' + (p.type === 'module' ? modName(p.module) : p.type === 'tooley' ? 'Revision Paper ' + p.label : X.paper + p.label); }
  function resolve() {
    var Q = qs(), id = Q.exam || '', T = D.types;
    var p = D.papers.filter(function (x) { return x.id === id; })[0];
    if (p) return { key: p.id, title: paperTitle(p), ids: p.ids, wids: p.wids || [], minutes: p.minutes, wminutes: p.wminutes || 0, forward: p.forward, type: p.type, fixed: true, p: p };
    if (id === 'review') { var w = shuffle(wrongIds(), Math.random).slice(0, 40); return { key: 'review', title: X.hub.review, ids: w, wids: [], minutes: Math.max(5, Math.ceil(w.length * 1.2)), forward: false, type: 'review' }; }
    var m = /^(midterm|final)-random$/.exec(id);
    if (m) { var t = T[m[1]]; return { key: id, title: X.hub[m[1]] + ' · ' + X.rnd.replace('🎲 ', ''), ids: null, spec: { quota: t.quota, levels: t.levels }, minutes: t.minutes, forward: t.forward, type: m[1] }; }
    if (id === 'speed') { var sp = T.speed; return { key: 'speed', title: X.hub.speed, ids: null, spec: { quota: sp.quota, levels: sp.levels }, minutes: sp.minutes, forward: false, type: 'speed' }; }
    if (id === 'custom') {
      var mods = (Q.mods || '').split(',').filter(function (x) { return POOL[x]; }), n = Math.max(3, Math.min(100, +Q.n || 20)), mn = Math.max(3, Math.min(240, +Q.min || 20));
      return { key: 'custom', title: X.hub.custom, ids: null, spec: { mods: mods, n: n, orig: Q.orig === '1' }, minutes: mn, forward: Q.fwd === '1', type: 'custom' };
    }
    return null;
  }
  function typeTitle(type) { return X.hub[type] || type; }

  // ------------------------------------------------------------------ hub
  function bestOf(key) { var r = get('ae2021:prog:exam:' + key, null); return r ? ' · ' + X.best + ' ' + r.score + '/' + r.n : ' · ' + X.none; }
  function hub() {
    root.appendChild(el('div', 'callout', X.assume));
    ['midterm', 'final', 'speed'].forEach(function (t) {
      var T = D.types[t]; root.appendChild(el('h2', null, X.hub[t])); root.appendChild(el('p', null, X.desc[t]));
      var info = el('p', 'muted small', T.n + X.q + ' · ' + T.minutes + X.min + ' · ' + (T.forward ? X.fwd : X.free) + ' · ' + X.mods + ': ' + Object.keys(T.quota).map(function (m) { return m.toUpperCase() + '×' + T.quota[m]; }).join(' ')); root.appendChild(info);
      var box = el('div', 'row');
      D.papers.filter(function (p) { return p.type === t; }).forEach(function (p) { box.appendChild(card(p.id, X.paper + p.label, p.ids.length, p.minutes, p.forward, true)); });
      box.appendChild(card(t === 'speed' ? 'speed' : t + '-random', t === 'speed' ? X.hub.speed : X.rnd, T.n, T.minutes, T.forward, false)); root.appendChild(box);
    });
    root.appendChild(el('h2', null, X.hub.custom)); root.appendChild(el('p', null, X.desc.custom)); customForm();
    root.appendChild(el('h2', null, X.hub.mixed)); root.appendChild(el('p', null, X.desc.mixed));
    var mb = el('div', 'row'); D.mixed.forEach(function (p) { mb.appendChild(card(p.id, X.paper + p.label, p.ids.length, p.minutes, p.forward, true)); }); root.appendChild(mb);
    ['entry', 'module', 'hard', 'tooley', 'written', 'full'].forEach(section);
    root.appendChild(el('h2', null, X.hub.review)); root.appendChild(el('p', null, X.desc.review)); var nw = wrongIds().length, rb = el('div', 'row');
    if (nw) rb.appendChild(card('review', X.hub.review, Math.min(40, nw), Math.max(5, Math.ceil(Math.min(40, nw) * 1.2)), false, false)); else rb.appendChild(el('p', 'muted', X.mist.none)); root.appendChild(rb);
  }
  function section(t) {
    var ps = D.papers.filter(function (p) { return p.type === t; }); if (!ps.length) return;
    root.appendChild(el('h2', null, X.hub[t])); root.appendChild(el('p', null, X.desc[t])); var box = el('div', 'row');
    ps.forEach(function (p) {
      var label = p.type === 'module' ? modName(p.module) : p.type === 'tooley' ? 'Revision Paper ' + p.label : X.paper + p.label, wn = (p.wids || []).length, marks = 0;
      if (wn) Object.keys(p.wmarks || {}).forEach(function (k) { marks += p.wmarks[k]; });
      var line = []; if (p.ids.length) line.push(p.ids.length + X.q); if (wn) line.push(wn + (L === 'vi' ? ' bài tự luận' : ' written') + (marks ? ' · ' + marks + ' ' + X.wr.marks : '')); line.push(((p.minutes || 0) + (p.wminutes || 0)) + X.min);
      if (p.type === 'tooley') line.push(X.wr.book + ' ' + p.ids.length + '/' + p.book_n);
      box.appendChild(card(p.id, label, 0, 0, p.forward, true, line.join(' · ')));
    });
    root.appendChild(box);
  }
  function card(id, label, n, minutes, fwd, printable, custom) {
    var c = el('div', 'panel'); c.style.minWidth = '210px'; c.style.flex = '1 1 210px'; c.appendChild(el('b', null, label)); c.appendChild(el('div', 'muted small', custom || (n + X.q + ' · ' + minutes + X.min + (fwd ? ' · ' + X.fwd : ''))));
    c.appendChild(el('div', 'muted small', bestOf(id).slice(3)));
    var r = el('div', 'row'), a = el('a', 'btn small', X.start); a.href = 'run.html?exam=' + encodeURIComponent(id); r.appendChild(a);
    if (printable) { var p = el('a', 'btn small alt', '🖨'); p.href = 'print.html?exam=' + encodeURIComponent(id); p.title = X.print; r.appendChild(p); }
    c.appendChild(r); return c;
  }
  function customForm() {
    var f = el('div', 'panel'), g = el('div', 'row'); f.appendChild(el('b', null, X.cust.mods)); var boxes = [];
    Object.keys(D.mods).forEach(function (m) { var l = el('label'), c = el('input'); c.type = 'checkbox'; c.checked = true; c.value = m; boxes.push(c); l.appendChild(c); l.appendChild(document.createTextNode(' ' + modName(m))); l.style.marginRight = '10px'; g.appendChild(l); });
    f.appendChild(g);
    var r2 = el('div', 'row'), n = el('input'), mn = el('input'), fw = el('input'), og = el('input'), msg = el('span', 'muted small');
    n.type = 'number'; n.min = 3; n.max = 100; n.value = 20; n.style.width = '70px'; mn.type = 'number'; mn.min = 3; mn.max = 240; mn.value = 20; mn.style.width = '70px'; fw.type = 'checkbox'; og.type = 'checkbox';
    [[X.cust.n, n], [X.cust.min, mn]].forEach(function (p) { var l = el('label', null, p[0] + ' '); l.appendChild(p[1]); r2.appendChild(l); });
    [[X.cust.fwd, fw], [X.cust.orig, og]].forEach(function (p) { var l = el('label'); l.appendChild(p[1]); l.appendChild(document.createTextNode(' ' + p[0])); r2.appendChild(l); }); f.appendChild(r2);
    var go = el('button', 'btn', X.cust.go); go.type = 'button'; f.appendChild(go); f.appendChild(msg);
    function avail() { var ms = boxes.filter(function (c) { return c.checked; }).map(function (c) { return c.value; }), cnt = 0; ms.forEach(function (m) { cnt += (POOL[m] || []).filter(function (it) { return !og.checked || it.g; }).length; }); return [ms, cnt]; }
    go.onclick = function () {
      var a = avail(); if (!a[0].length) { msg.textContent = ' ' + X.cust.none; return; } var nn = Math.min(+n.value || 20, a[1]);
      if (nn < (+n.value || 20)) { msg.textContent = ' ' + X.cust.few(a[1], nn); }
      location.href = 'run.html?exam=custom&mods=' + a[0].join(',') + '&n=' + nn + '&min=' + (+mn.value || 20) + '&fwd=' + (fw.checked ? 1 : 0) + '&orig=' + (og.checked ? 1 : 0);
    };
    root.appendChild(f);
  }

  // ------------------------------------------------------------------ written part (worked problems, self-marked): work -> submit -> compare with the printed solution -> mark yourself
  function runWritten(E, mcq, nav) {
    var W = E.wids.map(function (id) { return WBY[id]; }).filter(Boolean), marks = (E.p && E.p.wmarks) || {}, total = 0, secs = (E.wminutes || 60) * 60, timer = null;
    W.forEach(function (w) { total += marks[w.id] || 5; });
    var skey = 'wrun:' + E.key, st = sget(skey) || { t0: null, txt: {}, mk: {}, phase: 0 }; st.mcq = mcq; sput(skey, st);
    function save() { sput(skey, st); }
    function mk(w) { return marks[w.id] || 5; }
    function figs(w, box) { (w.figs || []).forEach(function (f) { var im = el('img', 'qfig'); im.src = f; im.alt = ''; box.appendChild(im); }); }
    function head() { var h = el('div'); h.appendChild(el('h1', null, E.title)); if (mcq) h.appendChild(el('h2', null, X.wr.part2)); return h; }
    function intro() {
      root.innerHTML = ''; root.appendChild(head()); var p = el('div', 'panel'); p.appendChild(el('p', null, X.wr.intro(W.length, total, E.wminutes || 60)));
      var ul = el('ul'); X.wr.rules.forEach(function (r) { ul.appendChild(el('li', null, r)); }); p.appendChild(ul);
      var b = el('button', 'btn', X.start); b.type = 'button'; b.onclick = function () { st.t0 = Date.now(); save(); work(); }; p.appendChild(b); root.appendChild(p); root.appendChild(nav);
    }
    function work() {
      root.innerHTML = ''; root.appendChild(head()); var bar = el('div', 'exambar'), tl = el('span', 'timer'), sb = el('button', 'btn small', X.wr.submit); sb.type = 'button'; bar.appendChild(tl); bar.appendChild(sb); root.appendChild(bar);
      W.forEach(function (w, i) {
        var box = el('div', 'qitem'), t = el('div', 'qtxt'); t.style.fontWeight = '600'; t.textContent = X.wr.problem + (i + 1) + ' (' + mk(w) + ' ' + X.wr.marks + '). ' + w.q; box.appendChild(t); figs(w, box); box.appendChild(el('div', 'srcnote', modName(w.m) + ' · ' + X.src + w.s));
        var ta = el('textarea'); ta.rows = 4; ta.style.width = '100%'; ta.placeholder = X.wr.notes; ta.value = st.txt[w.id] || ''; ta.oninput = function () { st.txt[w.id] = ta.value; save(); }; box.appendChild(ta); root.appendChild(box);
      });
      function tick() { var left = Math.max(0, secs - Math.round((Date.now() - st.t0) / 1000)); tl.textContent = '⏱ ' + tm(left); tl.className = 'timer' + (left < 120 ? ' low' : ''); if (left <= 0) { clearInterval(timer); st.phase = 1; save(); mark(); } }
      sb.onclick = function () { clearInterval(timer); st.phase = 1; save(); mark(); }; timer = setInterval(tick, 500); tick();
    }
    function mark() {
      root.innerHTML = ''; root.appendChild(head()); root.appendChild(el('h2', null, X.wr.selfmark));
      var sum = el('b'); function recompute() { var t = 0; W.forEach(function (w) { t += st.mk[w.id] || 0; }); sum.textContent = X.wr.total + ': ' + t + ' / ' + total; }
      W.forEach(function (w, i) {
        var box = el('div', 'qitem'), t = el('div', 'qtxt'); t.style.fontWeight = '600'; t.textContent = X.wr.problem + (i + 1) + ' (' + mk(w) + ' ' + X.wr.marks + '). ' + w.q; box.appendChild(t); figs(w, box);
        if (st.txt[w.id]) { var mine = el('div', 'srcnote', X.wr.notes + ': ' + st.txt[w.id]); box.appendChild(mine); }
        var ex = el('div', 'explain show'); ex.appendChild(el('b', null, X.wr.sol)); ex.appendChild(el('div', null, w.sol)); if (w.af) { var im = el('img', 'qfig'); im.src = w.af; im.alt = ''; ex.appendChild(im); } box.appendChild(ex);
        var sel = el('select'); for (var k = 0; k <= mk(w); k++) { var o = el('option', null, String(k)); o.value = k; sel.appendChild(o); } sel.value = st.mk[w.id] === undefined ? '0' : String(st.mk[w.id]);
        sel.onchange = function () { st.mk[w.id] = +sel.value; save(); recompute(); }; var lb = el('label', null, X.wr.yourmark + ' (0-' + mk(w) + '): '); lb.appendChild(sel); box.appendChild(lb); root.appendChild(box);
      });
      var fin = el('button', 'btn', X.wr.done); fin.type = 'button'; fin.onclick = result; root.appendChild(el('p')).appendChild(sum); recompute(); root.appendChild(fin); window.scrollTo(0, 0);
    }
    function result() {
      var got = 0, byMod = {}; W.forEach(function (w) { var v = st.mk[w.id] || 0; got += v; var b = byMod[w.m] = byMod[w.m] || [0, 0]; b[0] += v; b[1] += mk(w); });
      var mm = (E.p && E.p.mcq_marks) || 2, mg = mcq ? mcq.score * mm : 0, mt = mcq ? mcq.n * mm : 0, S2 = got + mg, T2 = total + mt, used = st.t0 ? Math.min(secs, Math.round((Date.now() - st.t0) / 1000)) : 0;
      var prev = get('ae2021:prog:exam:' + E.key, null); put('ae2021:prog:exam:' + E.key, { t: Date.now(), name: E.title, score: S2, n: T2, secs: used, best: Math.max(S2, prev && prev.n === T2 ? (prev.best || 0) : 0), byMod: byMod }); sput(skey, null);
      root.innerHTML = ''; root.appendChild(head()); var top = el('div', 'panel'); top.appendChild(el('h2', null, X.res)); var sd = el('div', 'stats');
      var cells = []; if (mcq) cells.push([X.wr.mcqpart, mg + ' / ' + mt]); cells.push([X.wr.wpart, got + ' / ' + total]); cells.push([X.wr.all, S2 + ' / ' + T2 + ' (' + Math.round(100 * S2 / T2) + '%)']); cells.push([X.mark, fmt(10 * S2 / T2) + ' / 10']);
      cells.forEach(function (p) { var d = el('div', 'stat'); d.appendChild(el('b', null, p[1])); d.appendChild(el('span', null, p[0])); sd.appendChild(d); }); top.appendChild(sd); top.appendChild(el('p', 'srcnote', X.saved)); root.appendChild(top);
      root.appendChild(el('h3', null, X.bymod)); var bars = el('div', 'bars');
      Object.keys(byMod).sort().forEach(function (m) { var c = byMod[m], pc = c[1] ? Math.round(100 * c[0] / c[1]) : 0, row = el('div', 'barrow'); row.appendChild(el('span', 'barl', modName(m))); var trk = el('span', 'bar'), f = el('span', 'fill ' + (pc >= 75 ? 'hi' : pc >= 50 ? 'mid' : 'lo')); f.style.width = Math.max(pc, 3) + '%'; trk.appendChild(f); row.appendChild(trk); row.appendChild(el('span', 'barv', pc + '% (' + c[0] + '/' + c[1] + ')')); bars.appendChild(row); });
      root.appendChild(bars); var a = el('a', 'btn alt', X.again); a.href = './'; root.appendChild(el('p')).appendChild(a); window.scrollTo(0, 0);
    }
    st.phase === 1 ? mark() : st.t0 ? work() : intro();
  }

  // ------------------------------------------------------------------ runner
  function run() {
    var E = resolve(), nav = el('p'), back = el('a', 'btn small alt', X.back); back.href = './'; nav.appendChild(back);
    if (!E) { root.appendChild(el('div', 'callout bad', X.unknown)); root.appendChild(nav); return; }
    E.wids = E.wids || []; var wsaved = E.wids.length ? sget('wrun:' + E.key) : null;
    if (wsaved && wsaved.mcq !== undefined) { runWritten(E, wsaved.mcq, nav); return; }              // reload during part II of a full paper
    var skey = 'examrun:' + location.search, S = sget(skey);
    if (S && S.key === E.key && S.ids && S.ids.length) { E.ids = S.ids; }
    else { E.ids = E.ids || draw(E.spec); S = null; }
    if (!E.ids.length && E.wids.length) { runWritten(E, null, nav); return; }
    if (!E.ids.length) { root.appendChild(el('div', 'callout bad', X.noItems)); root.appendChild(nav); return; }
    var N = E.ids.length, Qs = E.ids.map(function (id) { return BY[id]; }), secs = E.minutes * 60;
    var st = S || { key: E.key, ids: E.ids, ans: {}, flag: {}, idx: 0, t0: null, done: false }; sput(skey, st);
    var timer = null, submitted = false;
    var perms = st.perm || (st.perm = Qs.map(function (q) { var pm = q.o.map(function (_, k) { return k; }); shuffle(pm, Math.random); return pm; }));      // options are shuffled for every attempt (the paper itself keeps the book order in the print view)
    Qs = Qs.map(function (q, i) { var pm = perms[i]; return { id: q.id, m: q.m, q: q.q, f: q.f, e: q.e, s: q.s, l: q.l, o: pm.map(function (k) { return q.o[k]; }), c: pm.indexOf(q.c) }; }); save();
    function save() { sput(skey, st); }
    if (st.done) { sput(skey, null); st = { key: E.key, ids: E.ids, ans: {}, flag: {}, idx: 0, t0: null, done: false }; }
    st.t0 ? begin(true) : intro();

    function head() { var h = el('div'); h.appendChild(el('h1', null, E.title)); return h; }
    function intro() {
      root.innerHTML = ''; root.appendChild(head()); var p = el('div', 'panel'); p.appendChild(el('p', null, X.intro(N, E.minutes, E.forward)));
      var ul = el('ul'); X.rules.forEach(function (r) { ul.appendChild(el('li', null, r)); }); p.appendChild(ul);
      var b = el('button', 'btn', X.start); b.type = 'button'; b.onclick = function () { st.t0 = Date.now(); save(); begin(false); }; p.appendChild(b); root.appendChild(p); root.appendChild(nav);
    }
    function answeredCount() { return Object.keys(st.ans).length; }
    var bar, tl, pg, body, pal;
    function begin() {
      root.innerHTML = ''; root.appendChild(head());
      bar = el('div', 'exambar'); pg = el('span', 'prog'); tl = el('span', 'timer'); var ac = el('span', 'muted small'); ac.id = 'xans'; var fb = el('button', 'btn small alt', X.finish); fb.type = 'button'; fb.onclick = function () { if (confirm(X.sure(N - answeredCount()))) submit(false); };
      bar.appendChild(pg); bar.appendChild(tl); bar.appendChild(ac); bar.appendChild(fb); root.appendChild(bar);
      body = el('div'); root.appendChild(body); pal = el('div', 'row'); if (!E.forward) root.appendChild(pal);
      show(st.idx); timer = setInterval(tick, 500); tick();
    }
    function tick() { var left = Math.max(0, secs - Math.round((Date.now() - st.t0) / 1000)); tl.textContent = '⏱ ' + tm(left); tl.className = 'timer' + (left < 120 ? ' low' : ''); if (left <= 0) submit(true); }
    function show(i) {
      if (submitted) return; st.idx = i; save(); body.innerHTML = ''; var q = Qs[i]; pg.textContent = X.qn(i + 1, N); document.getElementById('xans').textContent = X.answered(answeredCount(), N);
      var box = el('div', 'qitem'); var t = el('div', 'qtxt'); t.style.fontWeight = '600'; t.textContent = (i + 1) + '. ' + q.q; box.appendChild(t);
      if (q.f) { var im = el('img', 'qfig'); im.src = q.f; im.alt = ''; box.appendChild(im); }
      q.o.forEach(function (o, oi) { var b = el('button', 'opt', LET[oi] + '. ' + o); b.type = 'button'; if (st.ans[i] === oi) b.style.outline = '2px solid var(--accent)'; b.onclick = function () { choose(oi); }; box.appendChild(b); });
      var nb = el('div', 'row'); var pv = el('button', 'btn alt small', X.prev); pv.type = 'button'; pv.disabled = E.forward || i === 0; pv.onclick = function () { go(-1); };
      var nx = el('button', 'btn small', i === N - 1 ? X.finish : X.next); nx.type = 'button'; nx.onclick = function () { go(1); };
      var fl = el('button', 'btn alt small', st.flag[i] ? X.unflag : X.flag); fl.type = 'button'; fl.onclick = function () { toggleFlag(); };
      if (!E.forward) nb.appendChild(pv); nb.appendChild(nx); if (!E.forward) nb.appendChild(fl); box.appendChild(nb); body.appendChild(box); drawPalette();
    }
    function drawPalette() {
      if (E.forward) return; pal.innerHTML = '';
      for (var i = 0; i < N; i++) (function (i) { var b = el('button', 'btn small ' + (st.ans[i] !== undefined ? '' : 'alt'), String(i + 1)); b.type = 'button'; b.style.minWidth = '34px'; if (i === st.idx) b.style.outline = '2px solid var(--accent2)'; if (st.flag[i]) b.textContent = (i + 1) + '⚑'; b.onclick = function () { show(i); }; pal.appendChild(b); })(i);
    }
    function choose(oi) { if (submitted) return; st.ans[st.idx] = oi; save(); show(st.idx); }
    function toggleFlag() { if (E.forward) return; if (st.flag[st.idx]) delete st.flag[st.idx]; else st.flag[st.idx] = 1; save(); show(st.idx); }
    function go(d) {
      if (submitted) return; var j = st.idx + d;
      if (d > 0 && st.idx === N - 1) { if (confirm(X.sure(N - answeredCount()))) submit(false); return; }
      if (j < 0 || j >= N || (E.forward && d < 0)) return; show(j);
    }
    document.addEventListener('keydown', function (e) {
      if (submitted || !body || /input|textarea|select/i.test((e.target || {}).tagName || '')) return; var k = e.key;
      if (/^[a-fA-F]$/.test(k)) { var oi = LET.indexOf(k.toUpperCase()); if (oi < Qs[st.idx].o.length) choose(oi); }
      else if (/^[1-6]$/.test(k)) { if (+k - 1 < Qs[st.idx].o.length) choose(+k - 1); }
      else if (k === 'ArrowRight' || k === 'Enter') { e.preventDefault(); go(1); } else if (k === 'ArrowLeft') { e.preventDefault(); go(-1); } else if (k === 'm' || k === 'M') toggleFlag();
    });
    function submit(auto) {
      if (submitted) return; submitted = true; clearInterval(timer); var used = Math.min(secs, Math.round((Date.now() - st.t0) / 1000)), score = 0, byMod = {};
      Qs.forEach(function (q, i) { var ok = st.ans[i] === q.c; if (ok) score++; var b = byMod[q.m] = byMod[q.m] || [0, 0]; b[1]++; if (ok) b[0]++; });
      noteWrong(Qs, st.ans); var pk = E.wids.length ? E.key + '-mcq' : E.key, pn = E.title + (E.wids.length ? ' (' + X.wr.mcqpart + ')' : '');
      var prev = get('ae2021:prog:exam:' + pk, null); put('ae2021:prog:exam:' + pk, { t: Date.now(), name: pn, score: score, n: N, secs: used, best: Math.max(score, prev && prev.n === N ? (prev.best || 0) : 0), byMod: byMod });
      st.done = true; sput(skey, null); result(score, used, byMod, auto);
    }
    function result(score, used, byMod, auto) {
      root.innerHTML = ''; root.appendChild(head()); if (auto) root.appendChild(el('div', 'callout warn', X.up));
      var top = el('div', 'panel'); top.appendChild(el('h2', null, X.res)); var st2 = el('div', 'stats');
      [[X.score, score + ' / ' + N + ' (' + Math.round(100 * score / N) + '%)'], [X.mark, fmt(10 * score / N) + ' / 10'], [X.time, tm(used) + ' / ' + E.minutes + ':00']].forEach(function (p) { var d = el('div', 'stat'); d.appendChild(el('b', null, p[1])); d.appendChild(el('span', null, p[0])); st2.appendChild(d); });
      top.appendChild(st2); top.appendChild(el('p', 'srcnote', X.saved)); root.appendChild(top);
      root.appendChild(el('h3', null, X.bymod)); var bars = el('div', 'bars');
      Object.keys(byMod).sort().forEach(function (m) { var c = byMod[m], p = Math.round(100 * c[0] / c[1]), row = el('div', 'barrow'); row.appendChild(el('span', 'barl', modName(m))); var tr = el('span', 'bar'), f = el('span', 'fill ' + (p >= 75 ? 'hi' : p >= 50 ? 'mid' : 'lo')); f.style.width = Math.max(p, 3) + '%'; tr.appendChild(f); row.appendChild(tr); row.appendChild(el('span', 'barv', p + '% (' + c[0] + '/' + c[1] + ')')); bars.appendChild(row); });
      root.appendChild(bars);
      var acts = el('div', 'row'), wrong = []; Qs.forEach(function (q, i) { if (st.ans[i] !== q.c) wrong.push(q.id); });
      if (wrong.length) { var rb = el('button', 'btn', X.redo + ' (' + wrong.length + ')'); rb.type = 'button'; rb.onclick = function () { practice(wrong); }; acts.appendChild(rb); }
      if (E.wids.length) { var cb2 = el('button', 'btn', X.wr.cont); cb2.type = 'button'; cb2.onclick = function () { runWritten(E, { score: score, n: N }, nav); }; acts.insertBefore(cb2, acts.firstChild); }
      var ag = el('a', 'btn alt', X.again); ag.href = './'; acts.appendChild(ag); root.appendChild(acts);
      root.appendChild(el('h3', null, X.review)); var tg = el('label'), cb = el('input'); cb.type = 'checkbox'; cb.checked = wrong.length > 0; tg.appendChild(cb); tg.appendChild(document.createTextNode(' ' + X.onlyWrong)); root.appendChild(tg); var list = el('div'); root.appendChild(list);
      function draw2() { list.innerHTML = ''; Qs.forEach(function (q, i) { var ok = st.ans[i] === q.c; if (cb.checked && ok) return; list.appendChild(reviewCard(q, i, st.ans[i])); }); }
      cb.onchange = draw2; draw2(); window.scrollTo(0, 0);
    }
    function reviewCard(q, i, a) {
      var box = el('div', 'qitem'), ok = a === q.c, t = el('div', 'qtxt'); t.style.fontWeight = '600'; t.textContent = (i + 1) + '. ' + q.q; box.appendChild(t); if (q.f) { var im = el('img', 'qfig'); im.src = q.f; im.alt = ''; box.appendChild(im); }
      q.o.forEach(function (o, oi) { var b = el('div', 'opt', LET[oi] + '. ' + o); b.setAttribute('data-done', '1'); if (oi === q.c) b.classList.add('correct'); else if (oi === a) b.classList.add('wrong'); b.style.cursor = 'default'; box.appendChild(b); });
      var ex = el('div', 'explain show'); var h = el('div', null, (ok ? X.ok : X.bad) + (a === undefined ? ' (' + X.blank + ')' : '') + ' · ' + X.correct + ': ' + LET[q.c]); h.style.fontWeight = '800'; ex.appendChild(h); ex.appendChild(document.createTextNode(q.e)); box.appendChild(ex);
      box.appendChild(el('div', 'srcnote', X.src + q.s)); return box;
    }
    function practice(ids) {                                                    // redo the mistakes with instant feedback, no timer
      root.innerHTML = ''; root.appendChild(el('h1', null, E.title + ' · ' + X.pr)); root.appendChild(el('p', 'muted', X.pr1)); var list = el('div'), left = ids.slice(); root.appendChild(list);
      var wrong2 = []; var more = el('div', 'row'); root.appendChild(more);
      function next() {
        list.innerHTML = ''; more.innerHTML = ''; if (!left.length) { list.appendChild(el('div', 'callout good', X.done)); if (wrong2.length) { var b = el('button', 'btn', X.redo + ' (' + wrong2.length + ')'); b.type = 'button'; b.onclick = function () { practice(wrong2); }; more.appendChild(b); } var a = el('a', 'btn alt', X.again); a.href = './'; more.appendChild(a); return; }
        var q = BY[left[0]], box = el('div', 'qitem'), t = el('div', 'qtxt'); t.style.fontWeight = '600'; t.textContent = q.q; box.appendChild(t); if (q.f) { var im = el('img', 'qfig'); im.src = q.f; im.alt = ''; box.appendChild(im); }
        var ex = el('div', 'explain'), opts = [];
        q.o.forEach(function (o, oi) { var b = el('button', 'opt', LET[oi] + '. ' + o); b.type = 'button'; b.onclick = function () { opts.forEach(function (x) { x.setAttribute('data-done', '1'); }); opts[q.c].classList.add('correct'); if (oi !== q.c) { b.classList.add('wrong'); wrong2.push(q.id); }
          ex.innerHTML = ''; var h = el('div', null, oi === q.c ? X.ok : X.bad + ' · ' + X.correct + ': ' + LET[q.c]); h.style.fontWeight = '800'; ex.appendChild(h); ex.appendChild(document.createTextNode(q.e)); ex.classList.add('show');
          var nb = el('button', 'btn small', X.next); nb.type = 'button'; nb.onclick = function () { left.shift(); next(); }; box.appendChild(nb); }; opts.push(b); box.appendChild(b); });
        box.appendChild(ex); list.appendChild(box);
      }
      next();
    }
  }

  // ------------------------------------------------------------------ A4 print view: paper, answer sheet, key with explanations
  function printView() {
    var E = resolve(); if (!E || !E.fixed) { root.appendChild(el('div', 'callout bad', X.unknown)); return; }
    var Qs = E.ids.map(function (id) { return BY[id]; }), N = Qs.length, W = (E.wids || []).map(function (id) { return WBY[id]; }).filter(Boolean), wm = (E.p && E.p.wmarks) || {}, wt = 0; W.forEach(function (w) { wt += wm[w.id] || 5; });
    var bar = el('p', 'noprint'); var pb = el('button', 'btn', X.doPrint); pb.type = 'button'; pb.onclick = function () { window.print(); }; bar.appendChild(pb); var bk = el('a', 'btn alt', X.back); bk.href = './'; bk.style.marginLeft = '8px'; bar.appendChild(bk); root.appendChild(bar);
    var sheet = el('div', 'xprint'); root.appendChild(sheet);
    sheet.appendChild(el('h1', null, X.printTitle + ' · ' + E.title)); sheet.appendChild(el('p', null, 'AE2.021 · ' + (L === 'vi' ? 'Hệ thống điện tử: analog và số' : 'Electronics Systems: Analog and Digital') + ' · ' + (N ? N + X.q + ' · ' : '') + (W.length ? W.length + (L === 'vi' ? ' bài tự luận (' : ' written (') + wt + ' ' + X.wr.marks + ') · ' : '') + ((E.minutes || 0) + (E.wminutes || 0)) + X.min));
    var who = el('p', null, X.printName + '………………………………  ' + X.printId + '…………………  ' + X.printDate + '…………………'); sheet.appendChild(who); sheet.appendChild(el('p', 'small', X.printInst + ((E.minutes || 0) + (E.wminutes || 0)) + X.min + '.'));
    var ol = el('div');
    Qs.forEach(function (q, i) {
      var b = el('div', 'xq'); var t = el('div', null); t.style.fontWeight = '600'; t.textContent = (i + 1) + '. ' + q.q; b.appendChild(t); if (q.f) { var im = el('img', 'qfig'); im.src = q.f; im.alt = ''; b.appendChild(im); }
      q.o.forEach(function (o, oi) { b.appendChild(el('div', 'xo', '☐ ' + LET[oi] + '. ' + o)); }); ol.appendChild(b);
    });
    if (N) sheet.appendChild(el('h2', null, X.wr.part1)); sheet.appendChild(ol);
    if (W.length) {
      sheet.appendChild(el('h2', 'xbreak', X.wr.part2));
      W.forEach(function (w, i) { var b = el('div', 'xq'), t = el('div'); t.style.fontWeight = '600'; t.textContent = X.wr.problem + (i + 1) + ' (' + (wm[w.id] || 5) + ' ' + X.wr.marks + '). ' + w.q; b.appendChild(t); (w.figs || []).forEach(function (f) { var im = el('img', 'qfig'); im.src = f; im.alt = ''; b.appendChild(im); });
        var sp = el('div', 'srcnote', X.wr.blankLine + ':'); sp.style.minHeight = '120px'; sp.style.borderBottom = '1px solid #999'; b.appendChild(sp); sheet.appendChild(b); });
    }
    if (N) { sheet.appendChild(el('h2', 'xbreak', X.sheet)); var tb = el('table', 't'), r1 = el('tr'); ['#'].concat(LET.slice(0, 6).split('')).forEach(function (h) { r1.appendChild(el('th', null, h)); }); tb.appendChild(r1);
    for (var i = 0; i < N; i++) { var tr = el('tr'); tr.appendChild(el('td', null, String(i + 1))); for (var k = 0; k < 6; k++) tr.appendChild(el('td', null, k < Qs[i].o.length ? '○' : '')); tb.appendChild(tr); } sheet.appendChild(tb); }
    sheet.appendChild(el('h2', 'xbreak', X.key + ' · ' + E.title));
    if (N) {
      var kt = el('table', 't left'), kh = el('tr'); ['#', X.correct, L === 'vi' ? 'Giải thích' : 'Explanation', 'Module'].forEach(function (h) { kh.appendChild(el('th', null, h)); }); kt.appendChild(kh);
      Qs.forEach(function (q, i) { var tr = el('tr'); [String(i + 1), LET[q.c] + '. ' + q.o[q.c], q.e, q.m.toUpperCase()].forEach(function (v) { tr.appendChild(el('td', null, v)); }); kt.appendChild(tr); }); sheet.appendChild(kt);
    }
    W.forEach(function (w, i) { var b = el('div', 'xq'); b.appendChild(el('b', null, X.wr.problem + (i + 1) + ' · ' + X.wr.sol)); b.appendChild(el('div', null, w.sol)); if (w.af) { var im = el('img', 'qfig'); im.src = w.af; im.alt = ''; b.appendChild(im); } sheet.appendChild(b); });
  }
})();
