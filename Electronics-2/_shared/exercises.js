/* Exercise finder: every exercise of the four books (Floyd, Jaeger, EASA) with its place in the book, whether it has numbers, a figure, a simulator,
   a printed answer, which module it belongs to and whether the site already has it. Filter, search, paginate. */
(function () {
  var root = document.getElementById('exfind'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2);
  var X = {
    vi: { load: 'Đang tải danh mục bài tập…', fail: 'Không tải được danh mục: ', book: 'Sách', kind: 'Loại', mod: 'Module', cls: 'Phân loại', all: 'Tất cả', none: 'Không thuộc module nào',
      num: 'Chỉ bài có số', ans: 'Chỉ bài có đáp án (in hoặc site tính)', search: 'Tìm trong đề, số bài, mục…', n: function (a, b) { return a + ' / ' + b + ' bài'; }, page: 'Trang', prev: '◀ Trước', next: 'Sau ▶',
      pg: function (p, d) { return 'tr.' + p + ' (PDF ' + d + ')'; }, ansl: 'Đáp án in trong sách', calc: 'Đáp án do site tính (sách không in)', skipl: 'Chưa giải (lý do): ', fig: 'cần hình', sim: 'cần mô phỏng', numt: 'có số', site: 'đã có trên site', nonum: 'lý thuyết',
      books: { floyd: 'Floyd 9e', jaeger5: 'Jaeger 5e', easa: 'EASA M04' },
      kinds: { exercise: 'Exercise (trong bài)', example: 'Example', problem: 'Problem (cuối chương)', related_problem: 'Related Problem', selftest: 'Self-Test', truefalse: 'True/False', circuit_action: 'Circuit-Action', checkup: 'Section Checkup', question: 'Câu hỏi EASA' },
      classes: { solved: 'Site đã giải và kiểm (sách không in đáp án)', ready: 'Sẵn sàng luyện (có số, không cần hình)', figure: 'Cần hình trong sách', simulation: 'Cần mô phỏng (SPICE/MATLAB…)', conceptual: 'Lý thuyết (không số)', in_site: 'Đã có trong ngân hàng của site', outside: 'Ngoài các module (nền tảng / ngoài đề cương)' } },
    en: { load: 'Loading the exercise index…', fail: 'Could not load the index: ', book: 'Book', kind: 'Type', mod: 'Module', cls: 'Class', all: 'All', none: 'In no module',
      num: 'Numeric only', ans: 'With an answer only (printed or computed)', search: 'Search statement, number, section…', n: function (a, b) { return a + ' of ' + b + ' exercises'; }, page: 'Page', prev: '◀ Previous', next: 'Next ▶',
      pg: function (p, d) { return 'p.' + p + ' (PDF ' + d + ')'; }, ansl: 'Printed answer', calc: 'Computed by this site (the book prints none)', skipl: 'Not solved (reason): ', fig: 'figure needed', sim: 'simulator needed', numt: 'numeric', site: 'already on the site', nonum: 'conceptual',
      books: { floyd: 'Floyd 9e', jaeger5: 'Jaeger 5e', easa: 'EASA M04' },
      kinds: { exercise: 'Exercise (in-text)', example: 'Example', problem: 'Problem (end of chapter)', related_problem: 'Related Problem', selftest: 'Self-Test', truefalse: 'True/False', circuit_action: 'Circuit-Action', checkup: 'Section Checkup', question: 'EASA question' },
      classes: { solved: 'Solved and checked by this site (no printed answer)', ready: 'Ready to practise (numeric, no figure)', figure: 'Needs a figure from the book', simulation: 'Needs a simulator (SPICE/MATLAB…)', conceptual: 'Conceptual (no numbers)', in_site: 'Already in the site\'s bank', outside: 'Outside the modules (background / beyond syllabus)' } }
  }[L];
  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }
  var renderNow = function () { };
  var S = { book: 'all', kind: 'all', mod: 'all', cls: 'all', num: false, ans: false, q: '', page: 0, size: 30 }, D = [], F = {};
  root.appendChild(el('p', 'muted', X.load));
  fetch(root.getAttribute('data-src')).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); }).then(function (j) {
    F = {}; j.fields.forEach(function (f, i) { F[f] = i; });
    D = j.rows; init();
  }).catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });

  function sel(label, opts, key) {
    var l = el('label', null, label + ' '), s = el('select');
    opts.forEach(function (o) { var op = el('option', null, o[1]); op.value = o[0]; s.appendChild(op); });
    s.onchange = function () { S[key] = s.value; S.page = 0; renderNow(); };
    l.appendChild(s); return l;
  }
  function init() {
    root.innerHTML = '';
    var bar = el('div', 'bm-bar');
    bar.appendChild(sel(X.book, [['all', X.all]].concat(Object.keys(X.books).map(function (k) { return [k, X.books[k]]; })), 'book'));
    bar.appendChild(sel(X.kind, [['all', X.all]].concat(Object.keys(X.kinds).map(function (k) { return [k, X.kinds[k]]; })), 'kind'));
    var mods = []; for (var i = 1; i <= 10; i++) mods.push(['m' + (i < 10 ? '0' : '') + i, 'M' + (i < 10 ? '0' : '') + i]);
    bar.appendChild(sel(X.mod, [['all', X.all], ['none', X.none]].concat(mods), 'mod'));
    bar.appendChild(sel(X.cls, [['all', X.all]].concat(Object.keys(X.classes).map(function (k) { return [k, X.classes[k]]; })), 'cls'));
    [['num', X.num], ['ans', X.ans]].forEach(function (p) { var l = el('label'), c = el('input'); c.type = 'checkbox'; c.onchange = function () { S[p[0]] = c.checked; S.page = 0; render(); }; l.appendChild(c); l.appendChild(document.createTextNode(' ' + p[1])); bar.appendChild(l); });
    var q = el('input'); q.type = 'search'; q.placeholder = X.search; q.oninput = function () { S.q = q.value.toLowerCase(); S.page = 0; render(); }; bar.appendChild(q);
    root.appendChild(bar);
    var info = el('div', 'score'); root.appendChild(info);
    var list = el('div'); root.appendChild(list);
    var nav = el('div', 'row'); root.appendChild(nav);
    function ok(r) {
      if (S.book !== 'all' && r[F.book] !== S.book) return false;
      if (S.kind !== 'all' && r[F.kind] !== S.kind) return false;
      if (S.mod === 'none') { if (r[F.modules].length) return false; } else if (S.mod !== 'all' && r[F.modules].indexOf(S.mod) < 0) return false;
      if (S.cls !== 'all' && r[F.cls] !== S.cls) return false;
      if (S.num && !r[F.numeric]) return false;
      if (S.ans && !r[F.answer]) return false;
      if (S.q) { var t = (r[F.text] + ' ' + r[F.number] + ' ' + (r[F.section] || '') + ' ' + (r[F.answer] || '') + ' ' + X.books[r[F.book]] + ' ' + r[F.chapter]).toLowerCase(); if (t.indexOf(S.q) < 0) return false; }
      return true;
    }
    function card(r) {
      var d = el('div', 'qitem'), h = el('div');
      var tags = [X.books[r[F.book]] + (r[F.book] === 'easa' ? ' SM0' + r[F.chapter] : ' · ' + (L === 'vi' ? 'Ch.' : 'Ch.') + r[F.chapter]) + (r[F.section] ? ' §' + r[F.section] : ''), X.kinds[r[F.kind]] + (r[F.number] ? ' ' + r[F.number] : ''), X.pg(r[F.printed] || '–', r[F.pdf])];
      tags.forEach(function (t) { h.appendChild(el('span', 'tag', t)); });
      [[r[F.numeric], X.numt, 'tag good'], [!r[F.numeric], X.nonum, 'tag'], [r[F.figure], X.fig, 'tag exam'], [r[F.sim], X.sim, 'tag exam'], [r[F.in_site].length, X.site + ' (' + r[F.in_site].join(', ') + ')', 'tag good']].forEach(function (p) { if (p[0]) h.appendChild(el('span', p[2], p[1])); });
      r[F.modules].forEach(function (m) { h.appendChild(el('span', 'bm-chip r-core', m)); });
      d.appendChild(h); d.appendChild(el('div', 'qtxt', r[F.text] || '—'));
      if (r[F.answer]) { var a = el('details'); a.appendChild(el('summary', null, r[F.ans_kind] === 'computed' ? X.calc : X.ansl)); a.appendChild(el('div', 'explain show', r[F.answer])); d.appendChild(a); }
      if (r[F.skip]) d.appendChild(el('div', 'srcnote', X.skipl + r[F.skip]));
      return d;
    }
    function render() {
      var f = D.filter(ok), pages = Math.max(1, Math.ceil(f.length / S.size)); if (S.page >= pages) S.page = pages - 1;
      info.textContent = X.n(f.length, D.length) + ' · ' + X.page + ' ' + (S.page + 1) + '/' + pages;
      list.innerHTML = ''; f.slice(S.page * S.size, (S.page + 1) * S.size).forEach(function (r) { list.appendChild(card(r)); });
      nav.innerHTML = '';
      var p = el('button', 'btn alt', X.prev), n = el('button', 'btn alt', X.next); p.disabled = S.page === 0; n.disabled = S.page >= pages - 1;
      p.onclick = function () { S.page--; render(); window.scrollTo(0, 0); }; n.onclick = function () { S.page++; render(); window.scrollTo(0, 0); };
      nav.appendChild(p); nav.appendChild(n);
    }
    renderNow = render; render();
  }
})();
