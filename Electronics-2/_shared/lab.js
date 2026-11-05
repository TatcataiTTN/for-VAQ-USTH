/* Lab (bilingual): calculators that check a hand calculation of this course. Values accept SI suffixes: 10k, 2.2k, 0.0015u, 47n, 1M, 3.3m.
   Numeric output is a check of your own working, not a substitute for it. Formulas follow Floyd 9e (op-amps ch.12-13, filters ch.15, 555 ch.16, regulators ch.17). */
(function () {
  var root = document.getElementById('lab'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi';
  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }
  var MUL = { p: 1e-12, n: 1e-9, u: 1e-6, 'µ': 1e-6, 'μ': 1e-6, m: 1e-3, k: 1e3, K: 1e3, M: 1e6, G: 1e9 };
  function val(s) { var m = String(s).trim().replace(',', '.').match(/^([-+]?\d*\.?\d+(?:e[-+]?\d+)?)\s*([pnuµμmkKMG]?)(?:[A-Za-zΩ]*)$/); if (!m) return NaN; return parseFloat(m[1]) * (m[2] ? MUL[m[2]] : 1); }
  function eng(v, unit) {
    if (!isFinite(v)) return String(v); if (v === 0) return '0 ' + unit; var a = Math.abs(v), p = [[1e9, 'G'], [1e6, 'M'], [1e3, 'k'], [1, ''], [1e-3, 'm'], [1e-6, 'μ'], [1e-9, 'n'], [1e-12, 'p']];
    for (var i = 0; i < p.length; i++) if (a >= p[i][0] * 0.9999) return String(+(v / p[i][0]).toPrecision(4)) + ' ' + p[i][1] + unit; return String(+v.toPrecision(4)) + ' ' + unit;
  }
  function g(x, n) { return String(+x.toPrecision(n || 4)); }
  var T = {
    opamp: { vi: 'Op-amp: độ lợi, trở kháng vào và băng thông vòng kín', en: 'Op-amp: gain, input resistance and closed-loop bandwidth' },
    db: { vi: 'Đổi decibel', en: 'Decibel converter' },
    filter: { vi: 'Bộ lọc RC và Sallen-Key (Butterworth)', en: 'RC and Sallen-Key (Butterworth) filters' },
    timer555: { vi: 'IC 555: phi ổn và đơn ổn', en: '555 timer: astable and monostable' },
    regulator: { vi: 'Ổn áp LM317 và hạn dòng', en: 'LM317 regulator and current limit' },
    binary: { vi: 'Đổi cơ số, BCD, bù hai và bảng chân trị', en: 'Base conversion, BCD, two\'s complement and truth tables' }
  };
  var tools = [];
  function tool(id, fields, run, note) { tools.push({ id: id, fields: fields, run: run, note: note }); }
  // fields: [name, label vi, label en, default] or [name, label vi, label en, 'select', [[value, text]...]]
  tool('opamp', [['cfg', 'Mạch', 'Circuit', 'select', [['inv', vi ? 'Đảo' : 'Inverting'], ['ni', vi ? 'Không đảo' : 'Noninverting'], ['vf', vi ? 'Đệm điện áp' : 'Voltage follower']]], ['ri', 'Ri', 'Ri', '10k'], ['rf', 'Rf', 'Rf', '220k'], ['ft', 'fT (băng thông đơn vị)', 'fT (unity-gain bandwidth)', '1M'], ['vin', 'Vin (biên độ)', 'Vin (amplitude)', '50m']],
    function (v) {
      var ri = val(v.ri), rf = val(v.rf), ft = val(v.ft), vin = val(v.vin), A, rin;
      if (v.cfg === 'inv') { A = -rf / ri; rin = ri; } else if (v.cfg === 'ni') { A = 1 + rf / ri; rin = Infinity; } else { A = 1; rin = Infinity; }
      var aa = Math.abs(A);
      return [[vi ? 'Độ lợi vòng kín Acl' : 'Closed-loop gain Acl', g(A) + ' (' + g(20 * Math.log10(aa)) + ' dB)'], [vi ? 'Điện áp ra' : 'Output voltage', eng(A * vin, 'V')], [vi ? 'Trở kháng vào (lý tưởng)' : 'Input resistance (ideal)', isFinite(rin) ? eng(rin, 'Ω') : (vi ? 'rất lớn (hàng GΩ)' : 'very large (GΩ range)')], [vi ? 'Băng thông vòng kín fc(cl) = fT/|Acl|' : 'Closed-loop bandwidth fc(cl) = fT/|Acl|', eng(ft / aa, 'Hz')]];
    }, vi ? 'Đảo: Acl = −Rf/Ri. Không đảo: Acl = 1 + Rf/Ri. Floyd 12–4, 12–8.' : 'Inverting: Acl = −Rf/Ri. Noninverting: Acl = 1 + Rf/Ri. Floyd 12–4, 12–8.');
  tool('db', [['av', 'Tỉ số điện áp', 'Voltage ratio', '100'], ['ap', 'Tỉ số công suất', 'Power ratio', '1000'], ['dbv', 'dB (điện áp)', 'dB (voltage)', '40'], ['stages', 'Các tầng (dB, cách nhau dấu phẩy)', 'Stages (dB, comma separated)', '20, 14, 6']],
    function (v) {
      var av = val(v.av), ap = val(v.ap), d = val(v.dbv), s = String(v.stages).split(',').map(val).filter(isFinite), tot = s.reduce(function (a, b) { return a + b; }, 0);
      return [[vi ? 'Av → dB (20·log₁₀)' : 'Av → dB (20·log₁₀)', g(20 * Math.log10(av)) + ' dB'], [vi ? 'Ap → dB (10·log₁₀)' : 'Ap → dB (10·log₁₀)', g(10 * Math.log10(ap)) + ' dB'], [vi ? 'dB → Av (10^(dB/20))' : 'dB → Av (10^(dB/20))', g(Math.pow(10, d / 20))], [vi ? 'Tổng các tầng' : 'Cascade total', g(tot) + ' dB = ' + g(Math.pow(10, tot / 20)) + '×']];
    }, vi ? 'Độ lợi điện áp: 20·log₁₀; công suất: 10·log₁₀; các tầng nối tiếp thì cộng dB, nhân tỉ số. Floyd 6–6, 10–2.' : 'Voltage gain: 20·log₁₀; power: 10·log₁₀; cascaded stages add in dB and multiply as ratios. Floyd 6–6, 10–2.');
  tool('filter', [['r', 'R', 'R', '2.2k'], ['c', 'C', 'C', '1.5n'], ['fc', 'fc cần có', 'Wanted fc', '4.5k'], ['c2', 'C chọn (thiết kế Sallen-Key)', 'Chosen C (Sallen-Key design)', '10n'], ['df', 'Hệ số tắt dần DF', 'Damping factor DF', '1.414']],
    function (v) {
      var r = val(v.r), c = val(v.c), fc = val(v.fc), c2 = val(v.c2), df = val(v.df), R = 1 / (2 * Math.PI * fc * c2);
      return [[vi ? 'Lọc RC bậc 1: fc = 1/(2πRC)' : 'First-order RC: fc = 1/(2πRC)', eng(1 / (2 * Math.PI * r * c), 'Hz')], [vi ? 'Sallen-Key RC bằng nhau: R = 1/(2π·fc·C)' : 'Equal-component Sallen-Key: R = 1/(2π·fc·C)', eng(R, 'Ω')], [vi ? 'Tỉ số Rf/Ri = 2 − DF' : 'Rf/Ri = 2 − DF', g(2 - df)], [vi ? 'Độ lợi băng thông 1 + Rf/Ri = 3 − DF' : 'Passband gain 1 + Rf/Ri = 3 − DF', g(3 - df)]];
    }, vi ? 'Butterworth hai cực: DF = 1,414 nên Rf/Ri = 0,586, độ lợi 1,586. Floyd 15–3.' : 'Two-pole Butterworth: DF = 1.414, so Rf/Ri = 0.586 and gain 1.586. Floyd 15–3.');
  tool('timer555', [['r1', 'R1', 'R1', '1k'], ['r2', 'R2', 'R2', '3.3k'], ['c', 'Cext', 'Cext', '0.047u'], ['rm', 'R (đơn ổn)', 'R (monostable)', '10k'], ['cm', 'C (đơn ổn)', 'C (monostable)', '10u']],
    function (v) {
      var r1 = val(v.r1), r2 = val(v.r2), c = val(v.c), rm = val(v.rm), cm = val(v.cm), f = 1.44 / ((r1 + 2 * r2) * c);
      return [[vi ? 'Phi ổn: f = 1,44/((R1+2R2)·C)' : 'Astable: f = 1.44/((R1+2R2)·C)', eng(f, 'Hz')], [vi ? 'Chu kỳ T' : 'Period T', eng(1 / f, 's')], [vi ? 'Chu kỳ làm việc (R1+R2)/(R1+2R2)' : 'Duty cycle (R1+R2)/(R1+2R2)', g(100 * (r1 + r2) / (r1 + 2 * r2)) + ' %'], [vi ? 'Thời gian mức cao / thấp' : 'High time / low time', eng(0.693 * (r1 + r2) * c, 's') + ' / ' + eng(0.693 * r2 * c, 's')], [vi ? 'Đơn ổn: tW = 1,1·R·C' : 'Monostable: tW = 1.1·R·C', eng(1.1 * rm * cm, 's')]];
    }, vi ? 'Phi ổn theo Floyd 16–6. Công thức đơn ổn tW = 1,1RC là công thức chuẩn trong datasheet 555 (Floyd 9e chỉ nhắc đơn ổn, không phát triển).' : 'Astable follows Floyd 16–6. The monostable formula tW = 1.1RC is the standard 555 datasheet result (Floyd 9e only mentions the one-shot).');
  tool('regulator', [['r1', 'R1', 'R1', '1k'], ['r2', 'R2', 'R2', '10k'], ['iadj', 'Iadj', 'Iadj', '50u'], ['vwant', 'Vout cần có', 'Wanted Vout', '9'], ['ilim', 'Dòng giới hạn', 'Current limit', '250m']],
    function (v) {
      var r1 = val(v.r1), r2 = val(v.r2), ia = val(v.iadj), vw = val(v.vwant), il = val(v.ilim);
      return [[vi ? 'LM317: Vout = 1,25(1 + R2/R1) + Iadj·R2' : 'LM317: Vout = 1.25(1 + R2/R1) + Iadj·R2', g(1.25 * (1 + r2 / r1) + ia * r2) + ' V'], [vi ? 'Bỏ qua Iadj' : 'Ignoring Iadj', g(1.25 * (1 + r2 / r1)) + ' V'], [vi ? 'R2 cho Vout cần có (cùng R1)' : 'R2 for the wanted Vout (same R1)', eng((vw - 1.25) / (1.25 / r1 + ia), 'Ω')], [vi ? 'Điện trở hạn dòng Rlimit = 0,7 V / Ilimit' : 'Current-limit resistor Rlimit = 0.7 V / Ilimit', eng(0.7 / il, 'Ω') + (vi ? ', công suất ' : ', power ') + eng(il * il * 0.7 / il, 'W')]];
    }, vi ? 'Floyd 17–6: với R1 = 1 kΩ, R2 = 10 kΩ, Iadj = 50 μA thì Vout = 14,25 V (sách làm tròn 14,3 V).' : 'Floyd 17–6: with R1 = 1 kΩ, R2 = 10 kΩ and Iadj = 50 μA, Vout = 14.25 V (the book rounds to 14.3 V).');
  tool('binary', [['dec', 'Số thập phân', 'Decimal number', '87'], ['bin', 'Số nhị phân', 'Binary number', '1010111'], ['bits', 'Số bit (bù hai)', 'Bits (two\'s complement)', '8'], ['neg', 'Số âm', 'Negative number', '-37']],
    function (v) {
      var d = parseInt(v.dec, 10), b = String(v.bin).replace(/[^01]/g, ''), n = parseInt(v.bits, 10), ng = parseInt(v.neg, 10), bcd = String(Math.abs(d)).split('').map(function (x) { return ('0000' + (+x).toString(2)).slice(-4); }).join(' ');
      var tc = ng < 0 ? ((1 << n) + ng).toString(2).padStart(n, '0') : '';
      return [[vi ? 'Thập phân → nhị phân' : 'Decimal → binary', isNaN(d) ? '–' : d.toString(2)], [vi ? 'Thập phân → thập lục' : 'Decimal → hexadecimal', isNaN(d) ? '–' : d.toString(16).toUpperCase()], ['BCD', isNaN(d) ? '–' : bcd], [vi ? 'Nhị phân → thập phân' : 'Binary → decimal', b ? String(parseInt(b, 2)) : '–'], [vi ? 'Bù hai của số âm' : 'Two\'s complement of the negative number', tc || '–']];
    }, vi ? 'EASA M04 SM01 tr.1.44–1.47 (hệ nhị phân, BCD).' : 'EASA M04 SM01 pp.1.44–1.47 (binary system, BCD).');
  var title = L === 'vi' ? 'vi' : 'en';
  tools.forEach(function (t) {
    var box = el('div', 'panel'); box.id = 'tool-' + t.id; box.appendChild(el('h3', null, T[t.id][title]));
    var vals = {}, form = el('div', 'labform'), out = el('div', 'laboutput');
    t.fields.forEach(function (f) {
      var lab = el('label', null, (vi ? f[1] : f[2]) + ' '), inp;
      if (f[3] === 'select') { inp = el('select'); f[4].forEach(function (o) { var op = el('option', null, o[1]); op.value = o[0]; inp.appendChild(op); }); vals[f[0]] = f[4][0][0]; }
      else { inp = el('input'); inp.value = f[3]; vals[f[0]] = f[3]; inp.size = 9; }
      inp.oninput = inp.onchange = function () { vals[f[0]] = inp.value; calc(); }; lab.appendChild(inp); form.appendChild(lab);
    });
    function calc() {
      out.innerHTML = '';
      try { t.run(vals).forEach(function (r) { var d = el('div', 'labrow'); d.appendChild(el('span', 'labk', r[0] + ': ')); d.appendChild(el('b', null, r[1])); out.appendChild(d); }); } catch (e) { out.appendChild(el('div', 'callout bad', String(e.message))); }
    }
    box.appendChild(form); box.appendChild(out); box.appendChild(el('p', 'srcnote', t.note)); root.appendChild(box); calc();
  });
  root.appendChild(el('div', 'callout', vi ? 'Kết quả ở đây là để kiểm tra bài làm tay của bạn, không thay thế cách làm: đề thi cần trình bày công thức và các bước.' : 'The results here check your own hand calculation; they do not replace it: an exam asks for the formula and the steps.'));
})();
