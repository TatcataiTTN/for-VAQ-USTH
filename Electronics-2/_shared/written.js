/* Written Practice (bilingual): hub of papers, study mode (statement, then the printed answer), exam mode (countdown, statements only, scratch notes),
   self-marking part by part at the end; the score is saved to the progress panel (localStorage 'prog:written:<paper>'). */
(function () {
  var hub = document.getElementById('written-hub'), page = document.getElementById('written'); if (!hub && !page) return;
  var host = hub || page, L = (document.documentElement.lang || 'vi').slice(0, 2);
  var X = {
    vi: { fail: 'Không tải được đề: ', start: '▶ Bắt đầu làm bài', study: '📖 Học với đáp án', exam: '⏱ Làm như đi thi', all: '◀ Tất cả đề', toStudy: '📖 Chuyển sang chế độ học', toExam: '⏱ Làm như đi thi',
      parts: function (n) { return n + ' bài'; }, marks: function (n) { return n + ' điểm'; }, minutes: function (m) { return m + ' phút'; }, best: function (s, t) { return 'điểm tự chấm tốt nhất ' + s + ' / ' + t; },
      ans: '✔ Xem đáp án in trong sách', hide: 'Ẩn đáp án', ansl: 'Đáp án in trong sách', calc: 'Đáp án do site tính (sách không in đáp án)', hw: 'Cách tính: ', as: 'Giả định: ', howc: 'Cách dùng: che đáp án, tự giải trên giấy trước, rồi so cả phương pháp. Sách KHÔNG in đáp án các bài này: đáp án do site tính bằng công thức của sách và kiểm lại bằng một cách độc lập; chỗ đề chưa nói rõ đã ghi ở phần Giả định, nếu bạn chọn khác thì kết quả khác theo.', groups: { 'jaeger-box': 'Jaeger 5e: khung EXERCISE có đáp án in', floyd: 'Floyd 9e: problem cuối chương có đáp án in (các bài số lẻ)', 'jaeger-solved': 'Jaeger 5e: problem không có đáp án in (site tự giải và kiểm)' }, ref: 'Nguồn: ', fig: 'Cần hình vẽ trong sách (xem trang đã ghi).', unknown: 'Không có đề này. ',
      how: 'Cách dùng: che đáp án, tự giải trên giấy trước, rồi mở đáp án và so cả phương pháp, không chỉ con số. Đáp án là đáp án IN trong sách (chỉ có kết quả cuối); lời giải chi tiết bạn tự viết ra.',
      examIntro: function (m, n) { return 'Thời gian ' + m + ' phút cho ' + n + ' bài. Làm trên giấy; trang chỉ hiện đề. Hết giờ hoặc khi bấm Kết thúc, đáp án hiện ra và bạn tự chấm từng bài.'; },
      notes: 'Ghi nháp (lưu trong trình duyệt này)', finish: 'Kết thúc và chấm', sure: 'Kết thúc bài thi và xem đáp án?', up: '⏱ Hết giờ — ', mark: 'Tự chấm', used: function (u, m) { return 'Thời gian đã dùng: ' + u + ' / ' + m + ':00. Mỗi bài 0, 0,5 hoặc 1 điểm: đúng con số mà thiếu cách làm thì chỉ nửa điểm.'; },
      mine: 'Điểm của tôi: ', save: 'Lưu kết quả', saved: function (s, t) { return ' Đã lưu: ' + s + ' / ' + t + '. Kết quả hiện ở bảng tiến độ trên trang chủ.'; }, part: 'Bài ', total: 'Tổng' },
    en: { fail: 'Could not load the papers: ', start: '▶ Start', study: '📖 Study with answers', exam: '⏱ Take it as an exam', all: '◀ All papers', toStudy: '📖 Switch to study mode', toExam: '⏱ Take it as an exam',
      parts: function (n) { return n + ' exercise' + (n === 1 ? '' : 's'); }, marks: function (n) { return n + ' mark' + (n === 1 ? '' : 's'); }, minutes: function (m) { return m + ' min'; }, best: function (s, t) { return 'best self-mark ' + s + ' / ' + t; },
      ans: '✔ Show the printed answer', hide: 'Hide the answer', ansl: 'Printed answer', calc: 'Computed by this site (the book prints no answer)', hw: 'Method: ', as: 'Assumptions: ', howc: 'How to use: cover the answer, solve on paper first, then compare your method. The book prints NO answer for these exercises: the answers were computed by this site with the book\'s formulas and re-checked by an independent route; whatever the statement leaves open is listed under Assumptions, and a different choice changes the result accordingly.', groups: { 'jaeger-box': 'Jaeger 5e: EXERCISE boxes with printed answers', floyd: 'Floyd 9e: end-of-chapter problems with printed answers (odd-numbered)', 'jaeger-solved': 'Jaeger 5e: problems without a printed answer (solved and checked by this site)' }, ref: 'Source: ', fig: 'A figure from the book is needed (see the page given).', unknown: 'Unknown paper. ',
      how: 'How to use: cover the answer, solve on paper first, then open the answer and compare your method, not only the number. The answer is the one PRINTED in the book (final result only); you write the full working yourself.',
      examIntro: function (m, n) { return m + ' minutes for ' + n + ' exercises. Work on paper; the page shows the statements only. At the end (or when time is up) the answers appear and you mark yourself exercise by exercise.'; },
      notes: 'Scratch notes (kept in this browser)', finish: 'Finish and mark', sure: 'Finish the exam and see the answers?', up: '⏱ Time is up — ', mark: 'Self-marking', used: function (u, m) { return 'Time used: ' + u + ' of ' + m + ':00. Each exercise is worth 0, 0.5 or 1: a correct number without the method earns half.'; },
      mine: 'My marks: ', save: 'Save my result', saved: function (s, t) { return ' Saved: ' + s + ' / ' + t + '. It appears in the progress panel on the home page.'; }, part: 'Exercise ', total: 'Total' }
  }[L];
  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }
  function fmt(n) { return (Math.round(n * 2) / 2).toString().replace('.', L === 'vi' ? ',' : '.'); }
  function tm(s) { s = Math.max(0, Math.round(s)); var m = Math.floor(s / 60), r = s % 60; return m + ':' + (r < 10 ? '0' : '') + r; }
  function total(p) { var t = 0; p.problems.forEach(function (q) { q.forEach(function (x) { t += x.marks; }); }); return t; }
  function get(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  fetch(host.getAttribute('data-src')).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (ps) { hub ? renderHub(ps) : renderPaper(ps); })
    .catch(function (e) { host.innerHTML = ''; host.appendChild(el('div', 'callout bad', X.fail + e.message)); });

  function renderHub(ps) {
    hub.innerHTML = ''; var order = ['jaeger-box', 'floyd', 'jaeger-solved'], shown = {};
    ps = ps.slice().sort(function (a, b) { var ia = order.indexOf(a.group), ib = order.indexOf(b.group); return (ia < 0 ? 9 : ia) - (ib < 0 ? 9 : ib); });
    ps.forEach(function (p) {
      if (p.group && !shown[p.group]) { shown[p.group] = 1; hub.appendChild(el('h2', null, X.groups[p.group] || p.group)); }
      var best = get('prog:written:' + p.id, null), c = el('div', 'panel');
      c.appendChild(el('h3', null, p.title[L])); c.appendChild(el('p', 'muted', [X.parts(p.problems.length), X.marks(total(p)), X.minutes(p.minutes)].join(' · '))); c.appendChild(el('p', 'small', p.note[L]));
      var row = el('div', 'row'), a1 = el('a', 'btn', X.study), a2 = el('a', 'btn alt', X.exam);
      a1.href = 'paper.html?p=' + encodeURIComponent(p.id); a2.href = 'paper.html?p=' + encodeURIComponent(p.id) + '&mode=exam'; row.appendChild(a1); row.appendChild(a2);
      if (best) row.appendChild(el('span', 'tag good', X.best(fmt(best.best != null ? best.best : best.score), fmt(best.total))));
      c.appendChild(row); hub.appendChild(c);
    });
  }
  function head(P, mode) {
    var h = el('div'); h.appendChild(el('h1', null, P.title[L])); h.appendChild(el('p', 'muted', [X.parts(P.problems.length), X.marks(total(P)), X.minutes(P.minutes)].join(' · ') + ' — ' + P.note[L]));
    var sw = el('p'), o = el('a', 'btn small alt', mode === 'exam' ? X.toStudy : X.toExam); o.href = 'paper.html?p=' + encodeURIComponent(P.id) + (mode === 'exam' ? '' : '&mode=exam'); sw.appendChild(o);
    var b = el('a', 'btn small alt', X.all); b.href = './'; b.style.marginLeft = '6px'; sw.appendChild(b); h.appendChild(sw); return h;
  }
  function answerBox(pt, cls) {
    var a = el('div', 'callout good' + (cls ? ' ' + cls : ''));
    if (!pt.computed) { a.innerHTML = '<b>' + X.ansl + '.</b> '; a.appendChild(document.createTextNode(pt.answer)); return a; }
    var h = el('b', null, X.calc + '.'); a.appendChild(h);
    pt.answer.forEach(function (r) { var d = el('div'); d.appendChild(el('span', 'muted', r[0] + (r[1] ? ': ' : ''))); if (r[1]) d.appendChild(el('b', null, r[1])); a.appendChild(d); });
    if (pt.how) a.appendChild(el('div', 'small', X.hw + pt.how));
    if (pt.assume && pt.assume.length) a.appendChild(el('div', 'small', X.as + pt.assume.join(' ')));
    return a;
  }
  function statement(pt, n) {
    var b = el('div', 'part'); b.appendChild(el('div', 'qtxt', n + '. ' + pt.text));
    var m = el('div', 'srcnote', X.ref + pt.ref + (pt.fig ? ' · ' + X.fig : '')); b.appendChild(m); return b;
  }
  function renderPaper(ps) {
    var qp = new URLSearchParams(location.search), id = qp.get('p'), mode = qp.get('mode') === 'exam' ? 'exam' : 'study';
    var P = ps.filter(function (p) { return p.id === id; })[0];
    if (!P) { page.innerHTML = ''; var d = el('div', 'callout bad', X.unknown), a = el('a', null, X.all); a.href = './'; d.appendChild(a); page.appendChild(d); return; }
    document.title = P.title[L] + ' · ' + document.title; mode === 'exam' ? examFlow(P) : study(P);
  }
  function study(P) {
    page.innerHTML = ''; page.appendChild(head(P, 'study')); var k = 0;
    P.problems.forEach(function (q) {
      q.forEach(function (pt) {
        var box = el('div', 'panel'), b = statement(pt, ++k), ans = answerBox(pt, 'hide');
        var bt = el('button', 'btn alt small', X.ans); bt.type = 'button';
        bt.onclick = function () { ans.classList.toggle('hide'); bt.textContent = ans.classList.contains('hide') ? X.ans : X.hide; };
        b.appendChild(bt); b.appendChild(ans); box.appendChild(b); page.appendChild(box);
      });
    });
    page.appendChild(el('div', 'callout', P.problems[0] && P.problems[0][0].computed ? X.howc : X.how));
  }
  function examFlow(P) {
    var key = 'written:notes:' + P.id, notes = get(key, {}), secs = P.minutes * 60, t0 = null, timer = null, finished = false, n = 0;
    P.problems.forEach(function (q) { n += q.length; });
    page.innerHTML = ''; page.appendChild(head(P, 'exam'));
    var intro = el('div', 'panel'); intro.appendChild(el('p', null, X.examIntro(P.minutes, n))); var go = el('button', 'btn', X.start); intro.appendChild(go); page.appendChild(intro);
    go.onclick = begin;
    function begin() {
      page.innerHTML = ''; page.appendChild(head(P, 'exam')); t0 = Date.now();
      var bar = el('div', 'exambar'), tl = el('span', 'timer'), pg = el('span', 'prog', X.marks(total(P))), bf = el('button', 'btn small alt', X.finish);
      bar.appendChild(pg); bar.appendChild(tl); bar.appendChild(bf); page.appendChild(bar); var k = 0, i = 0;
      P.problems.forEach(function (q) {
        q.forEach(function (pt) {
          var box = el('div', 'panel'); box.appendChild(statement(pt, ++k)); var ta = el('textarea'); ta.rows = 3; ta.placeholder = X.notes; ta.style.width = '100%'; var key2 = 'p' + i++; ta.value = notes[key2] || '';
          ta.oninput = function () { notes[key2] = ta.value; put(key, notes); }; box.appendChild(ta); page.appendChild(box);
        });
      });
      function tick() { var left = Math.max(0, secs - Math.round((Date.now() - t0) / 1000)); tl.textContent = '⏱ ' + tm(left); tl.className = 'timer' + (left < 120 ? ' low' : ''); if (left <= 0) fin(true); }
      timer = setInterval(tick, 500); tick();
      bf.onclick = function () { if (confirm(X.sure)) fin(false); };
      function fin(auto) { if (finished) return; finished = true; clearInterval(timer); mark(auto, Math.min(secs, Math.round((Date.now() - t0) / 1000))); }
    }
    function mark(auto, used) {
      page.innerHTML = ''; page.appendChild(head(P, 'exam'));
      var top = el('div', 'panel'); top.appendChild(el('h2', null, (auto ? X.up : '') + X.mark)); top.appendChild(el('p', null, X.used(tm(used), P.minutes)));
      var sc = el('div', 'bigscore', '0 / ' + fmt(total(P))); top.appendChild(sc); var save = el('button', 'btn', X.save), msg = el('span', 'muted'); top.appendChild(save); top.appendChild(msg); page.appendChild(top);
      var sels = [], k = 0;
      function upd() { var s = 0; sels.forEach(function (x) { s += parseFloat(x.value); }); sc.textContent = fmt(s) + ' / ' + fmt(total(P)); return s; }
      P.problems.forEach(function (q) {
        q.forEach(function (pt) {
          var box = el('div', 'panel'), b = statement(pt, ++k), ans = answerBox(pt); b.appendChild(ans);
          var row = el('div', 'row'), lab = el('label', null, X.mine), sel = el('select');
          for (var m = 0; m <= pt.marks + 1e-9; m += 0.5) { var o = el('option', null, fmt(m) + ' / ' + fmt(pt.marks)); o.value = String(m); sel.appendChild(o); }
          sel.onchange = upd; sels.push(sel); lab.appendChild(sel); row.appendChild(lab); b.appendChild(row); box.appendChild(b); page.appendChild(box);
        });
      });
      upd();
      save.onclick = function () { var s = upd(); put('prog:written:' + P.id, { t: Date.now(), score: s, best: Math.max(s, (get('prog:written:' + P.id, { best: 0 }).best) || 0), total: total(P), secs: used, title: P.title[L] }); msg.textContent = X.saved(fmt(s), fmt(total(P))); save.disabled = true; };
      window.scrollTo(0, 0);
    }
  }
})();
