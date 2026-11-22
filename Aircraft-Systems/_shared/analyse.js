/* Phan tich de / Question analyser: dan mot de bai, tim cau tuong tu trong ngan hang bang TF-IDF (khong dau, unigram + bigram), du doan chu de va muc, bao 'ngoai danh muc' khi khong khop. Chay hoan toan trong trinh duyet. */
(function () {
  var root = document.getElementById('analyse'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi';
  var X = vi ? { load: 'Đang tải ngân hàng…', fail: 'Không tải được dữ liệu: ', ph: 'Dán hoặc gõ một đề bài (tiếng Việt hoặc tiếng Anh)…', go: 'Phân tích', topic: 'Chủ đề dự đoán', mod: 'Module', level: 'Mức dự đoán', sim: 'Câu tương tự nhất', score: 'độ giống', out: 'Ngoài danh mục: không câu nào của môn giống đề này đủ nhiều. Có thể đề thuộc môn khác hoặc phần chưa có trong site.', hint: 'Kết quả chỉ là gợi ý dựa trên từ khoá và độ giống với ngân hàng (' , empty: 'Hãy nhập đề bài.', kinds: { mcq: 'trắc nghiệm', tf: 'đúng/sai', ess: 'tự luận' }, orig: 'câu gốc', add: 'bổ sung', how: 'Cách chấm: tách từ không dấu, trọng số TF-IDF, độ giống cosin giữa đề và từng câu (đề bài + nguồn + chủ đề).' }
    : { load: 'Loading the bank…', fail: 'Could not load the data: ', ph: 'Paste or type a question (Vietnamese or English)…', go: 'Analyse', topic: 'Predicted topic', mod: 'Module', level: 'Predicted level', sim: 'Most similar questions', score: 'similarity', out: 'Out of scope: no question of this course resembles it enough. It may belong to another course or to a part not on the site.', hint: 'The result is only a hint based on keywords and similarity with the bank (', empty: 'Please enter a question.', kinds: { mcq: 'multiple choice', tf: 'true/false', ess: 'worked' }, orig: 'original', add: 'added', how: 'Method: accent-free tokens, TF-IDF weights, cosine similarity between your text and each item (stem + source + topic).' };
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; }
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd'); }
  var STOP = {}; ('la va cua cho cac mot nhung trong khi the nao gi nao co khong duoc de voi tu den ra vao tren duoi sau truoc nay do thi ma hay hoac neu thi the cau sau day sau the a an the of in on to is are was were be by for from with and or at as it its this that these those which what when how why do does did can may will shall not no if then than so such').split(' ').forEach(function (w) { STOP[w] = 1; });
  function toks(s) { var w = norm(s).split(/[^a-z0-9]+/).filter(function (x) { return x && x.length > 1 && !STOP[x]; }), out = w.slice(); for (var i = 0; i + 1 < w.length; i++) out.push(w[i] + '_' + w[i + 1]); return out; }
  root.appendChild(el('p', 'muted', X.load));
  fetch('../data/search.json').then(function (r) { return r.json(); }).then(init).catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });
  function init(S) {
    var df = {}, docs = S.items.map(function (it) { var t = toks(it.q + ' ' + it.t + ' ' + it.s + ' ' + it.a), tf = {}; t.forEach(function (w) { tf[w] = (tf[w] || 0) + 1; }); Object.keys(tf).forEach(function (w) { df[w] = (df[w] || 0) + 1; }); return { it: it, tf: tf }; });
    var N = docs.length; function idf(w) { return Math.log((N + 1) / ((df[w] || 0) + 1)) + 1; }
    docs.forEach(function (d) { var s = 0; Object.keys(d.tf).forEach(function (w) { var v = (1 + Math.log(d.tf[w])) * idf(w); d.tf[w] = v; s += v * v; }); d.norm = Math.sqrt(s) || 1; });
    root.innerHTML = ''; var ta = el('textarea'); ta.rows = 5; ta.placeholder = X.ph; ta.style.cssText = 'width:100%;padding:8px;border:1px solid var(--border);border-radius:8px;background:transparent;color:inherit'; var go = el('button', 'btn', X.go); go.type = 'button'; var out = el('div');
    root.appendChild(ta); root.appendChild(el('p')).appendChild(go); root.appendChild(out); root.appendChild(el('p', 'srcnote', X.how));
    function run() {
      out.innerHTML = ''; var q = ta.value.trim(); if (!q) { out.appendChild(el('div', 'callout warn', X.empty)); return; }
      var qt = toks(q), tf = {}; qt.forEach(function (w) { tf[w] = (tf[w] || 0) + 1; }); var qn = 0; Object.keys(tf).forEach(function (w) { tf[w] = (1 + Math.log(tf[w])) * idf(w); qn += tf[w] * tf[w]; }); qn = Math.sqrt(qn) || 1;
      var sc = docs.map(function (d) { var dot = 0; Object.keys(tf).forEach(function (w) { if (d.tf[w]) dot += tf[w] * d.tf[w]; }); return { it: d.it, s: dot / (qn * d.norm) }; }).sort(function (a, b) { return b.s - a.s; });
      var top = sc.slice(0, 8); if (!top.length || top[0].s < 0.12) { out.appendChild(el('div', 'callout warn', X.out)); return; }
      var votes = {}; top.slice(0, 5).forEach(function (r) { var k = r.it.m + '|' + r.it.t; votes[k] = (votes[k] || 0) + r.s; }); var best = Object.keys(votes).sort(function (a, b) { return votes[b] - votes[a]; })[0].split('|');
      var lv = top.slice(0, 5).map(function (r) { return r.it.l; }).sort(); var med = lv[Math.floor(lv.length / 2)];
      var box = el('div', 'panel'); box.appendChild(el('p', null, X.mod + ': ' + best[0].toUpperCase() + ' · ' + S.mods[best[0]])); box.appendChild(el('p', null, X.topic + ': ' + best[1])); box.appendChild(el('p', null, X.level + ': ' + med)); box.appendChild(el('p', 'srcnote', X.hint + top[0].s.toFixed(2) + ').')); out.appendChild(box);
      out.appendChild(el('h3', null, X.sim)); top.forEach(function (r) { var c = el('div', 'qitem'); c.appendChild(el('div', 'srcnote', r.it.m.toUpperCase() + ' · ' + (X.kinds[r.it.k] || '') + ' · ' + (r.it.o === 'g' ? X.orig : X.add) + ' · L' + r.it.l + ' · ' + X.score + ' ' + Math.round(r.s * 100) + '%')); var p = el('div', null, r.it.q); var a = el('a', null, ' ↗'); a.href = '../practice/' + r.it.m + '.html#' + r.it.id; p.appendChild(a); c.appendChild(p); c.appendChild(el('div', 'srcnote', r.it.s)); out.appendChild(c); });
    }
    go.onclick = run;
  }
})();
