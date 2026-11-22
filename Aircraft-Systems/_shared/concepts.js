/* Khai niem / Concept finder: moi chu de cua ngan hang cau hoi (module x chu de) la mot khai niem; tim khong dau, loc theo module, so cau theo muc, cau mau, thuat ngu lien quan, nut luyen chu de. */
(function () {
  var root = document.getElementById('concepts'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi';
  var X = vi ? { load: 'Đang tải…', fail: 'Không tải được dữ liệu: ', ph: 'Gõ một khái niệm, ví dụ: thanh ghi dịch, AFDX, Nyquist…', all: 'Mọi module', n: 'câu', goc: 'câu gốc', lv3: 'mức 3', practice: 'Luyện chủ đề này →', samples: 'Câu mẫu', terms: 'Thuật ngữ liên quan', none: 'Không có khái niệm nào khớp. Nếu bạn nghĩ nó thuộc môn này, thử từ khoá khác; nếu không khớp gì thì có thể nằm ngoài danh mục của môn.', count: function (a, b) { return a + ' / ' + b + ' khái niệm'; } }
    : { load: 'Loading…', fail: 'Could not load the data: ', ph: 'Type a concept, e.g. shift register, AFDX, Nyquist…', all: 'All modules', n: 'questions', goc: 'original', lv3: 'level 3', practice: 'Practise this topic →', samples: 'Sample questions', terms: 'Related terms', none: 'No concept matches. If you think it belongs to this course try another keyword; if nothing matches it may be outside the course list.', count: function (a, b) { return a + ' / ' + b + ' concepts'; } };
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; }
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd'); }
  root.appendChild(el('p', 'muted', X.load));
  Promise.all([fetch('../data/search.json').then(function (r) { return r.json(); }), fetch('../data/glossary.json').then(function (r) { return r.json(); })]).then(function (r) { init(r[0], r[1]); })
    .catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });
  function init(S, G) {
    var map = {}, list = [];
    S.items.forEach(function (it) { var k = it.m + '|' + it.t; var c = map[k]; if (!c) { c = map[k] = { m: it.m, t: it.t, n: 0, g: 0, l3: 0, items: [] }; list.push(c); } c.n++; if (it.o === 'g') c.g++; if (it.l === 3) c.l3++; c.items.push(it); });
    list.forEach(function (c) {
      var toks = norm(c.t + ' ' + c.items.slice(0, 6).map(function (i) { return i.q; }).join(' ')).split(/[^a-z0-9]+/).filter(function (w) { return w.length >= 4; });
      var set = {}; toks.forEach(function (w) { set[w] = 1; });
      c.terms = G.filter(function (g) { return g.m.indexOf(c.m) >= 0 && norm(g.en + ' ' + g.vi).split(/[^a-z0-9]+/).some(function (w) { return w.length >= 4 && set[w]; }); }).slice(0, 6);
      c.key = norm(c.t + ' ' + c.terms.map(function (g) { return g.en + ' ' + g.vi; }).join(' ') + ' ' + S.mods[c.m]);
    });
    list.sort(function (a, b) { return a.m < b.m ? -1 : a.m > b.m ? 1 : b.n - a.n; });
    root.innerHTML = ''; var bar = el('div', 'row'), q = el('input'), sel = el('select'), cnt = el('span', 'muted small'), box = el('div', 'grid');
    q.type = 'search'; q.placeholder = X.ph; q.style.cssText = 'flex:1 1 280px;padding:8px 10px;border:1px solid var(--border);border-radius:8px;background:var(--bg2,transparent);color:inherit';
    var o0 = el('option', null, X.all); o0.value = ''; sel.appendChild(o0); Object.keys(S.mods).forEach(function (m) { var o = el('option', null, m.toUpperCase() + ' · ' + S.mods[m]); o.value = m; sel.appendChild(o); });
    bar.appendChild(q); bar.appendChild(sel); bar.appendChild(cnt); root.appendChild(bar); root.appendChild(box);
    function draw() {
      var w = norm(q.value).split(/\s+/).filter(Boolean), m = sel.value; box.innerHTML = ''; var shown = 0;
      list.forEach(function (c) {
        if (m && c.m !== m) return; if (w.some(function (x) { return c.key.indexOf(x) < 0; })) return; shown++;
        var card = el('div', 'mod-card'); card.style.cursor = 'default'; card.appendChild(el('div', 'num', c.m.toUpperCase() + ' · ' + S.mods[c.m])); card.appendChild(el('h3', null, c.t));
        card.appendChild(el('p', null, c.n + ' ' + X.n + ' · ' + c.g + ' ' + X.goc + (c.l3 ? ' · ' + c.l3 + ' ' + X.lv3 : '')));
        var a = el('a', 'btn small', X.practice); a.href = '../practice/' + c.m + '.html?topic=' + encodeURIComponent(c.t); card.appendChild(a);
        var det = el('details'); det.appendChild(el('summary', null, X.samples)); c.items.slice().sort(function (x, y) { return (x.o === 'g' ? 0 : 1) - (y.o === 'g' ? 0 : 1); }).slice(0, 3).forEach(function (i) { var p = el('p', 'small', i.q); var ln = el('a', null, ' ↗'); ln.href = '../practice/' + c.m + '.html#' + i.id; p.appendChild(ln); det.appendChild(p); }); card.appendChild(det);
        if (c.terms.length) { var tp = el('p', 'small muted', X.terms + ': ' + c.terms.map(function (g) { return vi ? g.vi + ' (' + g.en + ')' : g.en; }).join(' · ')); card.appendChild(tp); }
        box.appendChild(card);
      });
      cnt.textContent = X.count(shown, list.length); if (!shown) box.appendChild(el('div', 'callout warn', X.none));
    }
    q.oninput = draw; sel.onchange = draw; draw();
  }
})();
