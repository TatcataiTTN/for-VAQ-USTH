/* Bang tra ma: loc bang, may doi ma (thap phan, bat phan, thap luc, nhi phan, ky tu ASCII) va Luyen doi ma. Dap an cua Luyen doi ma tinh bang chinh may doi ma. */
(function () {
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi';
  var X = vi ? { dec: 'Thập phân', oct: 'Bát phân', hex: 'Thập lục phân', bin: 'Nhị phân', chr: 'Ký tự ASCII', bad: 'Giá trị không hợp lệ (0 đến 127).', ctl: 'mã điều khiển', go: 'Kiểm tra', next: 'Câu khác', ok: '✔ Đúng', no: '✘ Sai, đáp án: ', score: 'Điểm', ph: 'Nhập câu trả lời', q: { d2h: function (n) { return 'Đổi ' + n + ' (thập phân) sang thập lục phân'; }, h2d: function (h) { return 'Đổi ' + h + ' (thập lục phân) sang thập phân'; }, d2b: function (n) { return 'Đổi ' + n + ' (thập phân) sang nhị phân 8 bit'; }, b2o: function (b) { return 'Đổi ' + b + ' (nhị phân) sang bát phân 3 chữ số'; }, c2h: function (c) { return 'Mã ASCII của "' + c + '" ở dạng thập lục phân'; }, h2c: function (h) { return 'Ký tự ASCII có mã thập lục phân ' + h; } } }
    : { dec: 'Decimal', oct: 'Octal', hex: 'Hexadecimal', bin: 'Binary', chr: 'ASCII character', bad: 'Invalid value (0 to 127).', ctl: 'control code', go: 'Check', next: 'Another', ok: '✔ Correct', no: '✘ Wrong, the answer is: ', score: 'Score', ph: 'Type your answer', q: { d2h: function (n) { return 'Convert ' + n + ' (decimal) to hexadecimal'; }, h2d: function (h) { return 'Convert ' + h + ' (hexadecimal) to decimal'; }, d2b: function (n) { return 'Convert ' + n + ' (decimal) to 8-bit binary'; }, b2o: function (b) { return 'Convert ' + b + ' (binary) to 3-digit octal'; }, c2h: function (c) { return 'The ASCII code of "' + c + '" in hexadecimal'; }, h2c: function (h) { return 'The ASCII character with hexadecimal code ' + h; } } };
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; }
  function pad(s, n) { s = String(s); while (s.length < n) s = '0' + s; return s; }
  var rows = Array.prototype.slice.call(document.querySelectorAll('#code-table tr')).slice(1);
  var q = document.getElementById('code-q'); if (q) q.oninput = function () { var w = q.value.toLowerCase(); rows.forEach(function (r) { r.style.display = r.textContent.toLowerCase().indexOf(w) < 0 ? 'none' : ''; }); };
  var NAME = {}; rows.forEach(function (r) { var c = r.children; NAME[+c[0].textContent] = c[4].textContent; });
  function parse(kind, v) { v = v.trim(); if (!v) return null; var n; if (kind === 'dec') n = /^\d+$/.test(v) ? parseInt(v, 10) : NaN; else if (kind === 'oct') n = /^[0-7]+$/.test(v) ? parseInt(v, 8) : NaN; else if (kind === 'hex') n = /^(0x)?[0-9a-f]+$/i.test(v) ? parseInt(v.replace(/^0x/i, ''), 16) : NaN; else if (kind === 'bin') n = /^[01]+$/.test(v) ? parseInt(v, 2) : NaN; else n = v.length === 1 ? v.charCodeAt(0) : NaN; return n; }
  var conv = document.getElementById('conv');
  if (conv) {
    var kinds = ['dec', 'oct', 'hex', 'bin', 'chr'], inp = {}, msg = el('p', 'muted small'), row = el('div', 'row');
    kinds.forEach(function (k) { var l = el('label', null, X[k] + ' '), i = el('input'); i.style.width = k === 'bin' ? '120px' : '90px'; i.setAttribute('data-k', k); inp[k] = i; l.appendChild(i); row.appendChild(l); i.oninput = function () { var n = parse(k, i.value); msg.textContent = ''; kinds.forEach(function (o) { if (o !== k) inp[o].value = ''; }); if (n === null) return; if (isNaN(n) || n < 0 || n > 127) { msg.textContent = X.bad; return; }
      if (k !== 'dec') inp.dec.value = n; if (k !== 'oct') inp.oct.value = pad(n.toString(8), 3); if (k !== 'hex') inp.hex.value = pad(n.toString(16).toUpperCase(), 2); if (k !== 'bin') inp.bin.value = pad(n.toString(2), 8); if (k !== 'chr') inp.chr.value = n > 32 && n < 127 ? String.fromCharCode(n) : '';
      msg.textContent = NAME[n] ? 'ASCII: ' + NAME[n] + (n < 32 || n === 127 ? ' (' + X.ctl + ')' : '') : ''; }; });
    conv.appendChild(row); conv.appendChild(msg);
  }
  var drill = document.getElementById('drill');
  if (drill) {
    var score = 0, total = 0, box = el('div', 'panel'), qt = el('div'), ans = el('input'), res = el('div'), sc = el('p', 'muted small'), go = el('button', 'btn small', X.go), nx = el('button', 'btn alt small', X.next), cur;
    ans.placeholder = X.ph; ans.style.cssText = 'padding:6px 8px;margin-right:6px'; go.type = 'button'; nx.type = 'button'; [qt, ans, go, nx, res, sc].forEach(function (e) { box.appendChild(e); }); drill.appendChild(box);
    function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
    function make() {
      var t = rnd(0, 5), n = rnd(0, 127), c = rnd(33, 126), ch = String.fromCharCode(c), a;
      if (t === 0) { qt.textContent = X.q.d2h(n); a = n.toString(16).toUpperCase(); } else if (t === 1) { qt.textContent = X.q.h2d(pad(n.toString(16).toUpperCase(), 2)); a = String(n); } else if (t === 2) { qt.textContent = X.q.d2b(n); a = pad(n.toString(2), 8); }
      else if (t === 3) { qt.textContent = X.q.b2o(pad(n.toString(2), 8)); a = pad(n.toString(8), 3); } else if (t === 4) { qt.textContent = X.q.c2h(ch); a = c.toString(16).toUpperCase(); } else { qt.textContent = X.q.h2c(c.toString(16).toUpperCase()); a = ch; }
      cur = a; ans.value = ''; res.textContent = ''; ans.focus();
    }
    function check() { var v = ans.value.trim(); if (!v) return; total++; var strip = function (x) { return x.replace(/^0+(?=.)/, '').toLowerCase(); }, okv = v.toLowerCase() === cur.toLowerCase() || (/^[0-9a-f]+$/i.test(v) && /^[0-9a-f]+$/i.test(cur) && strip(v) === strip(cur)); if (okv) { score++; res.textContent = X.ok; } else res.textContent = X.no + cur; sc.textContent = X.score + ': ' + score + ' / ' + total; }
    go.onclick = check; nx.onclick = make; ans.onkeydown = function (e) { if (e.key === 'Enter') { if (res.textContent) make(); else check(); } }; make();
  }
})();
