/* Viet tay / Written practice: bai tu luan co dap an in cua sach; lam nhap trong o ghi chu, bam Xem dap an, tu danh dau da lam duoc; luu 'ae2021:prog:written:<id>'. */
(function () {
  var root = document.getElementById('written'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi';
  var X = vi ? { load: 'Đang tải…', fail: 'Không tải được dữ liệu: ', mod: 'Module', lvl: 'Mức', all: 'tất cả', show: 'Xem lời giải và đáp án', hide: 'Ẩn lời giải', notes: 'Nháp của bạn (lưu trong trình duyệt)', done: 'Tôi làm được', undone: 'Bỏ đánh dấu', counts: function (a, b, c) { return a + ' / ' + b + ' bài đã làm được · ' + c + ' bài đang hiện'; }, pre: 'Chỉ đánh dấu "làm được" sau khi bạn tự làm xong rồi đối chiếu với đáp án.' }
    : { load: 'Loading…', fail: 'Could not load the data: ', mod: 'Module', lvl: 'Level', all: 'all', show: 'Show solution and answer', hide: 'Hide solution', notes: 'Your draft (kept in this browser)', done: 'I can do it', undone: 'Unmark', counts: function (a, b, c) { return a + ' / ' + b + ' solved · ' + c + ' shown'; }, pre: 'Mark "I can do it" only after you have worked it out and compared it with the answer.' };
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; }
  function get(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }
  function put(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  root.appendChild(el('p', 'muted', X.load));
  fetch('../data/essays.json').then(function (r) { return r.json(); }).then(init).catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });
  function init(D) {
    root.innerHTML = ''; var f = { m: '', l: '' }, bar = el('div', 'row'), cnt = el('p', 'muted small'), list = el('div');
    function sel(lbl, opts, key) { var l = el('label', null, lbl + ' '), s = el('select'); opts.forEach(function (o) { var op = el('option', null, o[1]); op.value = o[0]; s.appendChild(op); }); s.onchange = function () { f[key] = s.value; draw(); }; l.appendChild(s); bar.appendChild(l); }
    sel(X.mod, [['', X.all]].concat(Object.keys(D.mods).filter(function (m) { return D.essays.some(function (e) { return e.m === m; }); }).map(function (m) { return [m, m.toUpperCase() + ' · ' + D.mods[m]]; })), 'm'); sel(X.lvl, [['', X.all], ['1', '1'], ['2', '2'], ['3', '3']], 'l');
    root.appendChild(el('p', 'srcnote', X.pre)); root.appendChild(bar); root.appendChild(cnt); root.appendChild(list);
    function key(e) { return 'ae2021:prog:written:' + e.id; }
    function draw() {
      list.innerHTML = ''; var es = D.essays.filter(function (e) { return (!f.m || e.m === f.m) && (!f.l || String(e.l) === f.l); }), solved = D.essays.filter(function (e) { var r = get(key(e)); return r && r.score; }).length;
      cnt.textContent = X.counts(solved, D.essays.length, es.length);
      es.forEach(function (e) {
        var box = el('div', 'qitem'), r = get(key(e)) || { note: '' }; box.id = e.id; box.appendChild(el('div', 'srcnote', e.m.toUpperCase() + ' · ' + e.t + ' · L' + e.l + ' · ' + e.s)); var q = el('div', 'qtxt', e.q); q.style.fontWeight = '600'; box.appendChild(q);
        (e.figs || []).forEach(function (u) { var im = el('img', 'qfig'); im.src = u; im.alt = ''; box.appendChild(im); });
        var ta = el('textarea'); ta.rows = 3; ta.style.width = '100%'; ta.placeholder = X.notes; ta.value = r.note || ''; ta.oninput = function () { var v = get(key(e)) || {}; v.note = ta.value; v.t = Date.now(); v.title = e.s; v.total = 1; v.score = v.score || 0; put(key(e), v); }; box.appendChild(ta);
        var row = el('div', 'row'), sb = el('button', 'btn small', X.show), ok = el('button', 'btn alt small', r.score ? X.undone : X.done), sol = el('div', 'explain'); sb.type = 'button'; ok.type = 'button';
        sol.appendChild(el('div', null, e.sol)); if (e.af) { var im = el('img', 'qfig'); im.src = e.af; im.alt = ''; sol.appendChild(im); }
        sb.onclick = function () { sol.classList.toggle('show'); sb.textContent = sol.classList.contains('show') ? X.hide : X.show; };
        ok.onclick = function () { var v = get(key(e)) || {}; v.score = v.score ? 0 : 1; v.t = Date.now(); v.title = e.s; v.total = 1; put(key(e), v); draw(); };
        row.appendChild(sb); row.appendChild(ok); box.appendChild(row); box.appendChild(sol); list.appendChild(box);
      });
    }
    draw();
  }
})();
