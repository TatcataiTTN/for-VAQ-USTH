/* "Your progress" panel (bilingual): reads the small summaries the practice bank, the timed sets, the quick quizzes and Written Practice keep in
   localStorage (prog:bank:*, prog:exam:*, prog:written:*, quiz:*). Nothing leaves the browser. */
(function () {
  var root = document.getElementById('progress'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), mods = JSON.parse(root.getAttribute('data-mods') || '[]');
  var X = {
    vi: { empty: 'Chưa có kết quả. Làm một vài câu ở Ngân hàng câu hỏi, một đề tính giờ hoặc một đề viết tay: kết quả, module cần ôn và các đề đã làm sẽ hiện ở đây (chỉ lưu trong trình duyệt này).',
      answered: 'Câu đã làm', correct: 'Đúng', worked: 'Bài tự luận đã làm được', sets: 'Đề đã nộp', bymod: 'Độ chính xác theo module', none: 'chưa làm', revisit: 'Module cần ôn (đúng dưới 60 %, ít nhất 5 câu)',
      recent: 'Kết quả gần đây', col: ['Khi nào', 'Đề', 'Điểm', 'Thời gian'], exam: 'Đề tính giờ ', written: 'Viết tay · ', reset: 'Xóa toàn bộ tiến độ của tôi', confirm: 'Xóa mọi kết quả đã lưu trong trình duyệt này?', quick: 'Quiz nhanh trong bài giảng' },
    en: { empty: 'No results yet. Answer a few questions in the Practice bank, take a timed set or a written paper: your results, the modules to revisit and the papers you took will appear here (stored only in this browser).',
      answered: 'Questions answered', correct: 'Correct', worked: 'Worked problems solved', sets: 'Sets submitted', bymod: 'Accuracy by module', none: 'not started', revisit: 'Modules to revisit (below 60 %, at least 5 answers)',
      recent: 'Recent results', col: ['When', 'Set', 'Score', 'Time'], exam: 'Timed set ', written: 'Written · ', reset: 'Delete all my progress', confirm: 'Delete every result saved in this browser?', quick: 'Quick quizzes inside the lessons' }
  }[L];
  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }
  function get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function pct(a, b) { return b ? Math.round(100 * a / b) : 0; }
  function tm(s) { s = Math.round(s || 0); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }
  var keys = []; try { for (var i = 0; i < localStorage.length; i++) keys.push(localStorage.key(i)); } catch (e) { }
  var bank = {}, exams = [], written = [], quick = [];
  keys.forEach(function (k) {
    var v = get(k); if (!v) return;
    if (k.indexOf('prog:bank:') === 0) bank[k.slice(10)] = v;
    else if (k.indexOf('prog:exam:') === 0) exams.push(v);
    else if (k.indexOf('prog:written:') === 0) written.push(v);
    else if (k.indexOf('quiz:') === 0 && v.n) quick.push(v);
  });
  var a = 0, c = 0, es = 0; Object.keys(bank).forEach(function (m) { a += bank[m].a; c += bank[m].c; es += bank[m].e || 0; });
  quick.forEach(function (q) { a += q.done || 0; c += q.score || 0; });
  root.innerHTML = '';
  if (!a && !exams.length && !written.length && !es) { root.appendChild(el('p', 'muted', X.empty)); return; }
  var line = el('div', 'stats');
  [[X.answered, a], [X.correct, c + ' (' + pct(c, a) + '%)'], [X.worked, es], [X.sets, exams.length + written.length]].forEach(function (p) { var d = el('div', 'stat'); d.appendChild(el('b', null, String(p[1]))); d.appendChild(el('span', null, p[0])); line.appendChild(d); });
  root.appendChild(line);
  root.appendChild(el('h3', null, X.bymod));
  var box = el('div', 'bars'), weak = [];
  mods.forEach(function (m) {
    var b = bank[m.id] || { a: 0, c: 0 }, p = pct(b.c, b.a), row = el('div', 'barrow');
    row.appendChild(el('span', 'barl', m.id.toUpperCase() + ' · ' + m.title));
    var tr = el('span', 'bar'), f = el('span', 'fill ' + (b.a === 0 ? 'none' : p >= 75 ? 'hi' : p >= 50 ? 'mid' : 'lo')); f.style.width = (b.a ? Math.max(p, 3) : 0) + '%'; tr.appendChild(f); row.appendChild(tr);
    row.appendChild(el('span', 'barv', b.a ? p + '% (' + b.c + '/' + b.a + ')' : X.none)); box.appendChild(row);
    if (b.a >= 5 && p < 60) weak.push([m, b, p]);
  });
  root.appendChild(box);
  if (weak.length) { root.appendChild(el('h3', null, X.revisit)); var ul = el('ul'); weak.sort(function (x, y) { return x[2] - y[2]; }).forEach(function (w) { var li = el('li'), ln = el('a', null, w[0].id.toUpperCase() + ' · ' + w[0].title + ' — ' + w[2] + '%'); ln.href = w[0].href; li.appendChild(ln); ul.appendChild(li); }); root.appendChild(ul); }
  var rec = [];
  exams.forEach(function (e) { rec.push({ t: e.t, title: X.exam + e.name, score: e.score + '/' + e.n + ' (' + pct(e.score, e.n) + '%)', secs: e.secs }); });
  written.forEach(function (w) { rec.push({ t: w.t, title: X.written + (w.title || ''), score: w.score + '/' + w.total, secs: w.secs }); });
  if (rec.length) {
    root.appendChild(el('h3', null, X.recent)); var tb = el('table', 't left'), hr = el('tr'); X.col.forEach(function (h) { hr.appendChild(el('th', null, h)); }); tb.appendChild(hr);
    rec.sort(function (x, y) { return y.t - x.t; }).slice(0, 8).forEach(function (r) { var tr = el('tr'); [new Date(r.t).toLocaleString(), r.title, r.score, r.secs ? tm(r.secs) : '–'].forEach(function (v) { tr.appendChild(el('td', null, String(v))); }); tb.appendChild(tr); });
    root.appendChild(tb);
  }
  var rs = el('button', 'btn alt small', X.reset); rs.onclick = function () { if (!confirm(X.confirm)) return; keys.forEach(function (k) { if (/^(prog:|bank:|quiz:|written:notes:)/.test(k)) try { localStorage.removeItem(k); } catch (e) { } }); location.reload(); };
  root.appendChild(rs);
})();
