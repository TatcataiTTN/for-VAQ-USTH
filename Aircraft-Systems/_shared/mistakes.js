/* So loi / Mistake log: cac cau lam sai (lan gan nhat) o Ngan hang cau hoi va o cac de; nhom theo module; danh dau da hieu; nut vao de 'On lai cau sai'. */
(function () {
  var root = document.getElementById('mistakes'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi', LET = 'ABCDEF';
  var X = vi ? { load: 'Đang tải…', fail: 'Không tải được dữ liệu: ', none: 'Chưa có câu nào làm sai. Hãy làm vài câu ở Ngân hàng câu hỏi hoặc một đề trước.', total: function (n) { return n + ' câu đang sai ở lần làm gần nhất.'; }, review: '▶ Ôn lại các câu sai như một đề', ok: 'Đã hiểu (ẩn)', correct: 'Đáp án đúng', src: 'Nguồn: ', yours: 'Bạn chọn', restore: 'Hiện lại các câu đã ẩn', hidden: function (n) { return n + ' câu đã ẩn.'; }, open: 'Mở trong ngân hàng ↗', times: 'lần sai' }
    : { load: 'Loading…', fail: 'Could not load the data: ', none: 'No mistakes yet. Try some questions in the Question bank or an exam first.', total: function (n) { return n + ' questions are wrong at your latest attempt.'; }, review: '▶ Review the mistakes as an exam', ok: 'Understood (hide)', correct: 'Correct answer', src: 'Source: ', yours: 'You chose', restore: 'Show the hidden ones again', hidden: function (n) { return n + ' hidden.'; }, open: 'Open in the bank ↗', times: 'wrong' };
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; }
  function get(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  root.appendChild(el('p', 'muted', X.load));
  fetch('../exam/data.json').then(function (r) { return r.json(); }).then(init).catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });
  function init(D) {
    var BY = {}; D.pool.forEach(function (q) { BY[q.id] = q; });
    function collect() {
      var w = get('ae2021:prog:wrong', {}), mine = {}, out = {}, hid = get('ae2021:mistakes:ok', {});
      Object.keys(w).forEach(function (id) { if (BY[id] && w[id].k === 'w') out[id] = { n: w[id].n || 1 }; });
      Object.keys(D.mods).forEach(function (m) { var b = get('ae2021:bank:' + m, null); if (!b || !b.ans) return; Object.keys(b.ans).forEach(function (id) { var q = BY[id]; if (!q) return; if (b.ans[id] !== q.c && !(w[id] && w[id].k === 'r')) { out[id] = out[id] || { n: 1 }; mine[id] = b.ans[id]; } }); });
      return { out: out, mine: mine, hid: hid };
    }
    function draw() {
      root.innerHTML = ''; var C = collect(), ids = Object.keys(C.out).filter(function (id) { return !C.hid[id]; }), nh = Object.keys(C.out).length - ids.length;
      if (!ids.length) { root.appendChild(el('div', 'callout', X.none)); } else {
        root.appendChild(el('p', 'lead', X.total(ids.length))); var go = el('a', 'btn', X.review); go.href = '../exam/run.html?exam=review'; root.appendChild(el('p')).appendChild(go);
        var by = {}; ids.forEach(function (id) { (by[BY[id].m] = by[BY[id].m] || []).push(id); });
        Object.keys(by).sort().forEach(function (m) {
          root.appendChild(el('h2', null, m.toUpperCase() + ' · ' + D.mods[m] + ' (' + by[m].length + ')'));
          by[m].forEach(function (id) {
            var q = BY[id], box = el('div', 'qitem'); var t = el('div', 'qtxt', q.q); t.style.fontWeight = '600'; box.appendChild(t); if (q.f) { var im = el('img', 'qfig'); im.src = q.f; im.alt = ''; box.appendChild(im); }
            q.o.forEach(function (o, i) { var d = el('div', 'opt', LET[i] + '. ' + o); d.setAttribute('data-done', '1'); d.style.cursor = 'default'; if (i === q.c) d.classList.add('correct'); else if (C.mine[id] === i) d.classList.add('wrong'); box.appendChild(d); });
            var ex = el('div', 'explain show'); ex.appendChild(el('b', null, X.correct + ': ' + LET[q.c] + '. ')); ex.appendChild(document.createTextNode(q.e)); box.appendChild(ex); box.appendChild(el('div', 'srcnote', X.src + q.s + ' · ' + C.out[id].n + ' ' + X.times));
            var row = el('div', 'row'), ok = el('button', 'btn alt small', X.ok), a = el('a', 'btn alt small', X.open); ok.type = 'button'; a.href = '../practice/' + q.m + '.html#' + id; ok.onclick = function () { var h = get('ae2021:mistakes:ok', {}); h[id] = 1; put('ae2021:mistakes:ok', h); draw(); }; row.appendChild(ok); row.appendChild(a); box.appendChild(row); root.appendChild(box);
          });
        });
      }
      if (nh) { var rs = el('button', 'btn alt small', X.restore); rs.type = 'button'; rs.onclick = function () { put('ae2021:mistakes:ok', {}); draw(); }; root.appendChild(el('p', 'muted small', X.hidden(nh) + ' ')).appendChild(rs); }
    }
    draw();
  }
})();
