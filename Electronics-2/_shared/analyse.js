/* Question analyser (bilingual): paste a question (English or Vietnamese) -> the quantities it contains, the kind of question, the modules it belongs to and
   the most similar exercises of the four books (from the scanned catalogue) with their place in the book and the printed answer.  Plain TF-IDF matching in the browser. */
(function () {
  var root = document.getElementById('analyser'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2);
  var X = {
    vi: { load: 'Đang tải danh mục bài tập…', fail: 'Không tải được danh mục: ', ph: 'Dán một câu hỏi vào đây (tiếng Anh hoặc tiếng Việt)…', go: 'Phân tích', clear: 'Xóa', ex: 'Ví dụ…',
      qty: 'Đại lượng có trong đề', kind: 'Dạng đề', mods: 'Module phù hợp nhất', sim: 'Bài tương tự trong sách', none: 'Không khớp bài nào trong danh mục: đề có thể nằm ngoài các sách và module của học phần.',
      outside: 'Các bài giống nhất không thuộc module nào của học phần (nền tảng hoặc ngoài đề cương).', score: 'độ giống', pg: function (p, d) { return 'tr.' + p + ' (PDF ' + d + ')'; }, ans: 'Đáp án in trong sách', site: 'đã có trên site',
      kinds: { calc: 'Tính toán: liệt kê đại lượng đã cho, chọn công thức, đổi đơn vị trước khi thế số, kiểm tra bậc độ lớn.', design: 'Thiết kế: chọn giá trị chuẩn gần nhất (E-series) rồi tính lại thông số thực.', fault: 'Tìm lỗi: xem điện áp một chiều trước, rồi đến tín hiệu; kiểm tra từng linh kiện hở/ngắn.', concept: 'Lý thuyết: nêu định nghĩa và điều kiện, đối chiếu từng phương án với định nghĩa.', binary: 'Nhị phân/logic: lập bảng chân trị hoặc đổi cơ số từng bước.' },
      examples: ['An inverting amplifier has Ri = 10 kΩ and Rf = 220 kΩ. What is the voltage gain and the output for a 50 mV input?', 'Tính tần số cắt của bộ lọc thông thấp RC với R = 2,2 kΩ và C = 0,0015 μF.', 'A 555 timer astable circuit has R1 = 1 kΩ, R2 = 3.3 kΩ and C = 0.047 μF. Find the frequency and the duty cycle.', 'Mạch ổn áp LM317 có R1 = 240 Ω và R2 = 2,4 kΩ. Tính điện áp ra.', 'Convert the decimal number 87 to binary and to BCD.'] },
    en: { load: 'Loading the exercise index…', fail: 'Could not load the index: ', ph: 'Paste a question here (English or Vietnamese)…', go: 'Analyse', clear: 'Clear', ex: 'Examples…',
      qty: 'Quantities in the question', kind: 'Kind of question', mods: 'Best-matching modules', sim: 'Similar exercises in the books', none: 'Nothing in the catalogue matches: the question may lie outside the books and modules of the course.',
      outside: 'The closest exercises belong to no module of the course (background or beyond the syllabus).', score: 'similarity', pg: function (p, d) { return 'p.' + p + ' (PDF ' + d + ')'; }, ans: 'Printed answer', site: 'already on the site',
      kinds: { calc: 'Calculation: list the given quantities, pick the formula, convert units before substituting, check the order of magnitude.', design: 'Design: choose the nearest standard value (E-series), then recompute the real parameter.', fault: 'Troubleshooting: dc voltages first, then the signal; test each component for open or short.', concept: 'Concept: state the definition and its conditions, test every option against the definition.', binary: 'Binary/logic: build the truth table or convert the base step by step.' },
      examples: ['An inverting amplifier has Ri = 10 kΩ and Rf = 220 kΩ. What is the voltage gain and the output for a 50 mV input?', 'Calculate the cutoff frequency of an RC low-pass filter with R = 2.2 kΩ and C = 0.0015 μF.', 'A 555 timer astable circuit has R1 = 1 kΩ, R2 = 3.3 kΩ and C = 0.047 μF. Find the frequency and the duty cycle.', 'An LM317 regulator has R1 = 240 Ω and R2 = 2.4 kΩ. Find the output voltage.', 'Convert the decimal number 87 to binary and to BCD.'] }
  }[L];
  var VI = { 'khuếch đại': 'amplifier', 'bộ khuếch đại': 'amplifier', 'độ lợi': 'gain', 'điện trở': 'resistor', 'tụ điện': 'capacitor', 'cuộn cảm': 'inductor', 'bộ lọc': 'filter', 'thông thấp': 'low-pass', 'thông cao': 'high-pass',
    'tần số cắt': 'cutoff frequency critical frequency', 'tần số': 'frequency', 'dao động': 'oscillator', 'ổn áp': 'regulator voltage', 'hồi tiếp': 'feedback', 'điện áp': 'voltage', 'dòng điện': 'current', 'công suất': 'power',
    'nhị phân': 'binary', 'thập phân': 'decimal', 'cổng logic': 'logic gate', 'so sánh': 'comparator', 'cộng': 'summing', 'tích phân': 'integrator', 'vi phân': 'differentiator', 'đệm': 'follower', 'băng thông': 'bandwidth',
    'ngõ vào': 'input', 'ngõ ra': 'output', 'đảo': 'inverting', 'không đảo': 'noninverting', 'tốc độ quay': 'slew rate', 'đẩy kéo': 'push-pull', 'bảng mạch in': 'printed circuit board', 'chu kỳ làm việc': 'duty cycle', 'phi ổn': 'astable' };
  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }
  var STOP = {}; 'the and for with that this from are was were what which find calculate determine value values given when then than its into over under between each have has will can how does not one two three four'.split(' ').forEach(function (w) { STOP[w] = 1; });
  function stem(w) { return w.length > 4 ? w.replace(/(ies|ing|ed|es|s)$/, function (m) { return m === 'ies' ? 'y' : ''; }) : w; }
  function toks(t) { return (t.toLowerCase().match(/[a-zà-ỹ][a-zà-ỹ0-9\-]{2,}/g) || []).map(stem).filter(function (w) { return !STOP[w]; }); }
  var Q = /[-−+]?\d+(?:[.,]\d+)?\s*(?:[kKMGmμµnpf]?(?:Ω|ohms?|V|A|W|F|H|Hz|s)|dB|%|°C|°)(?![A-Za-z])/g;
  var D = [], F = {}, idf = {}, docs = [];
  root.appendChild(el('p', 'muted', X.load));
  fetch(root.getAttribute('data-src')).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); }).then(function (j) {
    j.fields.forEach(function (f, i) { F[f] = i; }); D = j.rows; var df = {};
    docs = D.map(function (r) { var t = toks(r[F.text] || ''), set = {}; t.forEach(function (w) { set[w] = 1; }); Object.keys(set).forEach(function (w) { df[w] = (df[w] || 0) + 1; }); return { t: t, n: Math.max(t.length, 1) }; });
    Object.keys(df).forEach(function (w) { idf[w] = Math.log(1 + D.length / df[w]); }); init();
  }).catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });
  function init() {
    root.innerHTML = '';
    var ta = el('textarea'); ta.rows = 5; ta.placeholder = X.ph; ta.style.width = '100%'; root.appendChild(ta);
    var bar = el('div', 'row'), go = el('button', 'btn', X.go), cl = el('button', 'btn alt', X.clear), ex = el('select'); var o0 = el('option', null, X.ex); o0.value = ''; ex.appendChild(o0);
    X.examples.forEach(function (e, i) { var o = el('option', null, e.slice(0, 70) + '…'); o.value = i; ex.appendChild(o); });
    ex.onchange = function () { if (ex.value !== '') { ta.value = X.examples[+ex.value]; run(); } }; cl.onclick = function () { ta.value = ''; out.innerHTML = ''; };
    bar.appendChild(go); bar.appendChild(cl); bar.appendChild(ex); root.appendChild(bar); var out = el('div'); root.appendChild(out); go.onclick = run;
    function expand(t) { var s = t.toLowerCase(); Object.keys(VI).forEach(function (k) { if (s.indexOf(k) >= 0) s += ' ' + VI[k]; }); return s; }
    function run() {
      var text = ta.value.trim(); out.innerHTML = ''; if (!text) return;
      var qt = toks(expand(text)), qset = {}; qt.forEach(function (w) { qset[w] = 1; });
      var qty = text.match(Q) || [];
      var sc = []; D.forEach(function (r, i) { var s = 0, d = docs[i]; var seen = {}; d.t.forEach(function (w) { if (qset[w] && !seen[w]) { seen[w] = 1; s += idf[w]; } }); if (s > 0) sc.push([s / Math.pow(d.n, 0.35), i]); });
      sc.sort(function (a, b) { return b[0] - a[0]; });
      var top = sc.slice(0, 8), best = top.length ? top[0][0] : 0;
      var kind = /design|choose the values|thiết kế|chọn giá trị/i.test(text) ? 'design' : /fault|troubleshoot|open|shorted|lỗi|hở|ngắn mạch/i.test(text) ? 'fault' : /binary|decimal|hex|bcd|truth table|logic gate|nhị phân|thập phân|bảng chân/i.test(text) ? 'binary' : qty.length ? 'calc' : 'concept';
      var h = el('div', 'callout'); h.innerHTML = '<b>' + X.kind + '.</b> '; h.appendChild(document.createTextNode(X.kinds[kind])); out.appendChild(h);
      if (qty.length) { var q = el('p'); q.appendChild(el('b', null, X.qty + ': ')); qty.forEach(function (v) { q.appendChild(el('span', 'tag', v)); }); out.appendChild(q); }
      if (!top.length || best < 1.2) { out.appendChild(el('div', 'callout warn', X.none)); return; }
      var ms = {}; top.forEach(function (p) { D[p[1]][F.modules].forEach(function (m) { ms[m] = (ms[m] || 0) + p[0]; }); });
      var mk = Object.keys(ms).sort(function (a, b) { return ms[b] - ms[a]; });
      out.appendChild(el('h3', null, X.mods)); var mp = el('p');
      if (mk.length) mk.slice(0, 3).forEach(function (m) { var a = el('a', 'bm-chip r-core', m.toUpperCase()); a.href = '../practice/' + m + '.html'; mp.appendChild(a); }); else mp.appendChild(el('span', 'muted', X.outside));
      out.appendChild(mp); out.appendChild(el('h3', null, X.sim));
      top.forEach(function (p) {
        var r = D[p[1]], d = el('div', 'qitem'), hh = el('div');
        [(r[F.book] === 'floyd' ? 'Floyd 9e' : r[F.book] === 'jaeger5' ? 'Jaeger 5e' : 'EASA M04') + ' · ' + (r[F.book] === 'easa' ? 'SM0' + r[F.chapter] : 'Ch.' + r[F.chapter]) + (r[F.section] ? ' §' + r[F.section] : ''), r[F.kind] + (r[F.number] ? ' ' + r[F.number] : ''), X.pg(r[F.printed] || '–', r[F.pdf]), X.score + ' ' + p[0].toFixed(1)].forEach(function (t) { hh.appendChild(el('span', 'tag', t)); });
        r[F.modules].forEach(function (m) { hh.appendChild(el('span', 'bm-chip r-core', m)); }); if (r[F.in_site].length) hh.appendChild(el('span', 'tag good', X.site));
        d.appendChild(hh); d.appendChild(el('div', 'qtxt', r[F.text])); if (r[F.answer]) { var a = el('details'); a.appendChild(el('summary', null, X.ans)); a.appendChild(el('div', 'explain show', r[F.answer])); d.appendChild(a); }
        out.appendChild(d);
      });
    }
  }
})();
