/* Bai tap co dap an / Exercise finder: moi cau trong ngan hang (cau goc co khoa in cua sach truoc, cau bo sung sau) la mot bai tap; loc theo nguon (sach, chuong), module, loai, muc, dap an in; dem do phu theo chuong. */
(function () {
  var root = document.getElementById('exercises'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi';
  var X = vi ? { load: 'Đang tải…', fail: 'Không tải được dữ liệu: ', ph: 'Tìm theo đề bài, nguồn, chủ đề…', book: 'Nguồn', all: 'tất cả', mod: 'Module', kind: 'Loại', lvl: 'Mức', orig: 'Chỉ câu gốc có đáp án in', shown: function (a, b) { return a + ' / ' + b + ' bài'; }, more: 'Hiện thêm', kinds: { mcq: 'trắc nghiệm', tf: 'đúng/sai', ess: 'tự luận' }, cov: 'Độ phủ theo nguồn', open: 'Mở', th: ['Nguồn', 'Module', 'Loại', 'Mức', 'Đề bài', 'Đáp án (rút gọn)'], b: { Tooley: 'Tooley', Floyd: 'Floyd', Slide: 'Slide giảng viên', Added: 'Bổ sung của site' } }
    : { load: 'Loading…', fail: 'Could not load the data: ', ph: 'Search by stem, source, topic…', book: 'Source', all: 'all', mod: 'Module', kind: 'Kind', lvl: 'Level', orig: 'Original questions with a printed answer only', shown: function (a, b) { return a + ' / ' + b + ' exercises'; }, more: 'Show more', kinds: { mcq: 'multiple choice', tf: 'true/false', ess: 'worked' }, cov: 'Coverage by source', open: 'Open', th: ['Source', 'Module', 'Kind', 'Level', 'Stem', 'Answer (short)'], b: { Tooley: 'Tooley', Floyd: 'Floyd', Slide: 'Lecturer slides', Added: 'Added by the site' } };
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; }
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd'); }
  function bookOf(it) { var s = it.s; if (/^(Bổ sung|Added)/.test(s)) return 'Added'; if (/^Tooley/.test(s)) return 'Tooley'; if (/^Floyd/.test(s)) return 'Floyd'; return 'Slide'; }
  function chapOf(it) { var m = /^(Tooley|Floyd) (Ch\.\d+|Revision Paper \d+|Appendix \d+)/.exec(it.s); return m ? m[1] + ' ' + m[2] : null; }
  root.appendChild(el('p', 'muted', X.load));
  fetch('../data/search.json').then(function (r) { return r.json(); }).then(init).catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });
  function init(S) {
    var items = S.items.slice().sort(function (a, b) { return (a.o === 'g' ? 0 : 1) - (b.o === 'g' ? 0 : 1) || (a.m < b.m ? -1 : a.m > b.m ? 1 : 0); });
    items.forEach(function (it) { it.bk = bookOf(it); it.key = norm(it.q + ' ' + it.s + ' ' + it.t + ' ' + it.a); });
    root.innerHTML = ''; var f = { q: '', bk: '', m: '', k: '', l: '', g: false }, size = 40, bar = el('div', 'row'), tb = el('div', 'tablewrap'), mb = el('button', 'btn alt small', X.more); mb.type = 'button';
    var q = el('input'); q.type = 'search'; q.placeholder = X.ph; q.style.cssText = 'flex:1 1 240px;padding:8px 10px;border:1px solid var(--border);border-radius:8px;background:transparent;color:inherit'; bar.appendChild(q);
    function sel(lbl, opts, key) { var l = el('label', null, lbl + ' '), s = el('select'); opts.forEach(function (o) { var op = el('option', null, o[1]); op.value = o[0]; s.appendChild(op); }); s.onchange = function () { f[key] = s.value; size = 40; draw(); }; l.appendChild(s); bar.appendChild(l); }
    sel(X.book, [['', X.all]].concat(['Tooley', 'Floyd', 'Slide', 'Added'].map(function (b) { return [b, X.b[b]]; })), 'bk');
    sel(X.mod, [['', X.all]].concat(Object.keys(S.mods).map(function (m) { return [m, m.toUpperCase()]; })), 'm'); sel(X.kind, [['', X.all], ['mcq', X.kinds.mcq], ['tf', X.kinds.tf], ['ess', X.kinds.ess]], 'k'); sel(X.lvl, [['', X.all], ['1', '1'], ['2', '2'], ['3', '3']], 'l');
    var lg = el('label'), cb = el('input'); cb.type = 'checkbox'; cb.onchange = function () { f.g = cb.checked; size = 40; draw(); }; lg.appendChild(cb); lg.appendChild(document.createTextNode(' ' + X.orig)); bar.appendChild(lg);
    var cnt = el('p', 'muted small'); root.appendChild(bar); root.appendChild(cnt); root.appendChild(tb); root.appendChild(mb);
    var covh = el('h2', null, X.cov), cov = {}; items.forEach(function (it) { var c = chapOf(it); if (c) cov[c] = (cov[c] || 0) + 1; });
    var ct = el('table', 't left'), hr = el('tr'); [X.th[0], '#'].forEach(function (h) { hr.appendChild(el('th', null, h)); }); ct.appendChild(hr);
    Object.keys(cov).sort(function (a, b) { return a.localeCompare(b, undefined, { numeric: true }); }).forEach(function (c) { var tr = el('tr'); tr.appendChild(el('td', null, c)); tr.appendChild(el('td', null, String(cov[c]))); ct.appendChild(tr); }); root.appendChild(covh); root.appendChild(el('div', 'tablewrap')).appendChild(ct);
    q.oninput = function () { f.q = norm(q.value); size = 40; draw(); }; mb.onclick = function () { size += 80; draw(); };
    function draw() {
      var w = f.q.split(/\s+/).filter(Boolean), list = items.filter(function (it) { return (!f.bk || it.bk === f.bk) && (!f.m || it.m === f.m) && (!f.k || it.k === f.k) && (!f.l || String(it.l) === f.l) && (!f.g || it.o === 'g') && !w.some(function (x) { return it.key.indexOf(x) < 0; }); });
      tb.innerHTML = ''; var t = el('table', 't left'), h = el('tr'); X.th.forEach(function (c) { h.appendChild(el('th', null, c)); }); t.appendChild(h);
      list.slice(0, size).forEach(function (it) { var tr = el('tr'), td = el('td'); td.appendChild(document.createTextNode(it.s + ' ')); var a = el('a', null, '↗'); a.href = '../practice/' + it.m + '.html#' + it.id; a.title = X.open; td.appendChild(a); tr.appendChild(td);
        [it.m.toUpperCase(), X.kinds[it.k] || '', String(it.l), it.q, it.a].forEach(function (v) { tr.appendChild(el('td', null, v)); }); t.appendChild(tr); });
      tb.appendChild(t); cnt.textContent = X.shown(Math.min(size, list.length), list.length); mb.style.display = list.length > size ? '' : 'none';
    }
    draw();
  }
})();
