/* Lab (bilingual VI/EN) of AE2.013 Thermal Systems: calculators that CHECK a hand calculation. They run 100% in the browser on top of thermo.js
   (constant-k ideal gas). Inputs accept a decimal comma or a decimal point. Every result comes with its steps (KaTeX) and, after "Load worked example",
   with the reference values of the checked source (data embedded by build/lab_body.py from data/lab_expected.json). */
(function () {
  var root = document.getElementById('lab'); if (!root) return;
  var TH = window.Thermo; if (!TH) { root.textContent = 'thermo.js missing'; return; }
  var L = (document.documentElement.lang || 'vi').slice(0, 2), vi = L === 'vi';
  function T(a, b) { return vi ? a : b; }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

  /* ---------- numbers: parse (comma or point) and format (comma in VI) ---------- */
  function parseNum(s) {
    s = String(s).trim().replace(/\s+/g, '').replace(/−/g, '-'); if (s === '') return null;
    var c = (s.match(/,/g) || []).length, d = (s.match(/\./g) || []).length;
    if (c && d) { if (s.lastIndexOf(',') > s.lastIndexOf('.')) s = s.replace(/\./g, '').replace(',', '.'); else s = s.replace(/,/g, ''); }
    else if (c > 1 || d > 1) return NaN;
    else if (c) s = s.replace(',', '.');
    if (!/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(s)) return NaN;
    return parseFloat(s);
  }
  function fmt(x, sig) {
    sig = sig || 5; if (x === Infinity) return '∞'; if (typeof x !== 'number' || !isFinite(x)) return '–';
    var s = String(Number(x.toPrecision(sig))); return vi ? s.replace('.', ',') : s;
  }
  function n(x, sig) { var s = fmt(x, sig); s = s.replace(/e([+-]?\d+)/, function (m, e) { return String.raw`\times 10^{${parseInt(e, 10)}}`; }); return vi ? s.replace(',', '{,}') : s; }
  var U = { K: String.raw`\,\mathrm{K}`, kPa: String.raw`\,\mathrm{kPa}`, kJkg: String.raw`\,\mathrm{kJ/kg}`, kJkgK: String.raw`\,\mathrm{kJ/(kg\,K)}`, m3kg: String.raw`\,\mathrm{m^3/kg}`, kmol: String.raw`\,\mathrm{kmol}`,
    ms: String.raw`\,\mathrm{m/s}`, kgs: String.raw`\,\mathrm{kg/s}`, kg: String.raw`\,\mathrm{kg}`, m3: String.raw`\,\mathrm{m^3}`, kJ: String.raw`\,\mathrm{kJ}`, m2: String.raw`\,\mathrm{m^2}`, kgm3: String.raw`\,\mathrm{kg/m^3}` };

  /* ---------- error messages ---------- */
  var NAMES = { r: 'r', rc: 'r_c', k: 'k', R: 'R', cp: 'c_p', cv: 'c_v', T1: 'T1', T3: 'T3', T4: 'T4', P1: 'P1', qin: 'q_in', V1: 'V1', rp: 'r_p', etac: 'η_c', etat: 'η_t', eps: 'ε', Nc: 'N_c', Nt: 'N_t',
    Ma: 'Ma', Ma1: 'Ma1', A1s: 'A/A*', A2A1: 'A2/A1', P: 'P', P0: 'P0', T0: 'T0', T: 'T', V: 'V', Pb: 'Pb', Ae: 'A', Astar: 'A*', PP0: 'P/P0', a: 'a', b: 'b', c: 'c', d: 'd', excess: T('% thừa', '% excess'), Pprod: 'P', mdot: 'ṁ' };
  function errMsg(e) {
    if (!e || e.name !== 'ThermoError') return T('Lỗi không xác định: ', 'Unexpected error: ') + (e && e.message);
    var d = e.data || {}, nm = NAMES[d.name] || d.name;
    switch (e.code) {
      case 'missing': return T('Thiếu giá trị: ', 'Missing value: ') + nm + '.';
      case 'range': return nm + ' = ' + fmt(d.value) + T(' nằm ngoài miền cho phép (xem điều kiện của đại lượng này).', ' is outside the allowed range (see the condition for this quantity).');
      case 't3le2': return T('T₃ (' + fmt(d.T3) + ' K) phải lớn hơn nhiệt độ cuối nén (' + fmt(d.T2) + ' K): nếu không chu trình không nhận nhiệt. Tăng q_in hoặc T₃ (hoặc giảm tỉ số nén).', 'T₃ (' + fmt(d.T3) + ' K) must exceed the end-of-compression temperature (' + fmt(d.T2) + ' K), otherwise the cycle receives no heat. Increase q_in or T₃ (or lower the compression ratio).');
      case 'rcge_r': return T('Tỉ số cutoff r_c (' + fmt(d.rc) + ') phải nhỏ hơn tỉ số nén r (' + fmt(d.r) + '), nếu không giãn nở kết thúc ở thể tích lớn hơn V₁.', 'Cutoff ratio r_c (' + fmt(d.rc) + ') must be smaller than the compression ratio r (' + fmt(d.r) + '), otherwise the expansion would end at a volume above V₁.');
      case 't3le1': return T('T₃ phải lớn hơn T₁ (nếu không không có công ra).', 'T₃ must exceed T₁ (otherwise there is no net work).');
      case 'eff': return nm + ' = ' + fmt(d.value) + T(' phải nằm trong (0; 1] (riêng ε: [0; 1]).', ' must lie in (0, 1] (for ε: [0, 1]).');
      case 'stages': return nm + T(' phải là số nguyên từ 1 đến 10.', ' must be an integer from 1 to 10.');
      case 'noregen': return T('Không thể hồi nhiệt: nhiệt độ khí ra tuabin (' + fmt(d.Tt) + ' K) không cao hơn khí ra máy nén (' + fmt(d.Tc) + ' K). Đặt ε = 0 hoặc giảm tỉ số áp.', 'Regeneration is impossible: the turbine exhaust (' + fmt(d.Tt) + ' K) is not hotter than the compressor exit (' + fmt(d.Tc) + ' K). Set ε = 0 or lower the pressure ratio.');
      case 'noheat': return T('Nhiệt nhận vào bằng 0 hoặc âm: kiểm tra T₃, ε và hiệu suất.', 'Heat input is zero or negative: check T₃, ε and the efficiencies.');
      case 'aas_lt1': return T('A/A* = ' + fmt(d.value) + ' < 1: không có nghiệm, vì A/A* nhỏ nhất bằng 1 (tại Ma = 1).', 'A/A* = ' + fmt(d.value) + ' < 1: no solution, because A/A* has its minimum 1 at Ma = 1.');
      case 'aas_below1': return T('Diện tích mặt cắt 2 nhỏ hơn diện tích họng cần thiết (A₂/A* = ' + fmt(d.value) + ' < 1): dòng bị nghẹt trước, không thể giữ cùng lưu lượng.', 'Section 2 is smaller than the throat the flow needs (A₂/A* = ' + fmt(d.value) + ' < 1): the flow would choke before, the same mass flow cannot be kept.');
      case 'pr_range': return T('P/P₀ phải nằm trong (0; 1].', 'P/P₀ must lie in (0, 1].');
      case 'tr_range': return T('T/T₀ phải nằm trong (0; 1].', 'T/T₀ must lie in (0, 1].');
      case 'pb_gt_p0': return T('Áp suất ngược (' + fmt(d.Pb) + ' kPa) lớn hơn P₀ (' + fmt(d.P0) + ' kPa): không có dòng chảy vào vòi.', 'Back pressure (' + fmt(d.Pb) + ' kPa) is above P₀ (' + fmt(d.P0) + ' kPa): no flow through the nozzle.');
      case 'nofuel': return T('Nhiên liệu cần ít nhất một nguyên tử C hoặc H.', 'The fuel needs at least one C or H atom.');
      case 'no_o2': return T('Nhiên liệu chứa quá nhiều oxy (a + b/4 − c/2 ≤ 0): không cần không khí, không áp dụng công thức này.', 'The fuel holds too much oxygen (a + b/4 − c/2 ≤ 0): no air is needed, this model does not apply.');
      case 'rich': return T('Phần trăm không khí thừa phải ≥ 0. Hỗn hợp giàu (thiếu không khí) tạo CO và H₂: CHƯA LÀM trong bản này.', 'Excess air must be ≥ 0. A rich mixture (air deficiency) makes CO and H₂: NOT DONE in this version.');
    }
    return e.message;
  }

  /* ---------- generic calculator widget ---------- */
  var EX = {}; try { EX = JSON.parse(document.getElementById('lab-examples').textContent); } catch (e) { EX = { examples: [] }; }
  var examples = EX.examples || [];

  function Calc(host, spec) {
    var self = this, form = el('div', 'labform'), inputs = {}, errs = {}, out = el('div', 'laboutput'), activeEx = null;
    spec.fields.forEach(function (f) {
      var wrap = el('label', 'lf'), cap = el('span', 'lfc', (vi ? f.vi : f.en)), box = el('span', 'lfb'), inp;
      if (f.sel) { inp = el('select'); f.sel.forEach(function (o) { var op = el('option'); op.value = o[0]; op.textContent = vi ? o[1] : o[2]; inp.appendChild(op); }); inp.value = f.def || f.sel[0][0]; box.appendChild(inp); }
      else { inp = el('input'); inp.type = 'text'; inp.setAttribute('inputmode', 'decimal'); inp.autocomplete = 'off'; inp.spellcheck = false; inp.value = f.def !== undefined ? fmtField(f.def) : ''; inp.placeholder = f.ph !== undefined ? fmtField(f.ph) : (f.opt ? T('tùy chọn', 'optional') : ''); box.appendChild(inp); if (f.u) box.appendChild(el('span', 'lfu', f.u)); }
      inp.id = 'lab-' + spec.id + '-' + f.k; inp.setAttribute('data-k', f.k); wrap.appendChild(cap); wrap.appendChild(box);
      var er = el('span', 'lferr'); er.setAttribute('role', 'alert'); wrap.appendChild(er);
      if (f.hint) wrap.title = vi ? f.hint[0] : f.hint[1];
      form.appendChild(wrap); inputs[f.k] = inp; errs[f.k] = er; f._wrap = wrap;
    });
    function fmtField(v) { return typeof v === 'number' ? fmt(v, 12) : String(v); }
    var bar = el('div', 'labbar'), btn = el('button', 'labbtn', T('Tính', 'Calculate')); btn.type = 'button';
    var exWrap = el('span', 'exwrap'), exSel, exBtn = el('button', 'labbtn ex', T('Nạp ví dụ có lời giải', 'Load worked example')); exBtn.type = 'button';
    var myEx = examples.filter(function (x) { return x.calc === spec.id; });
    if (myEx.length) {
      exSel = el('select', 'exsel'); myEx.forEach(function (x, i) { var o = el('option'); o.value = i; o.textContent = vi ? x.title.vi : x.title.en; exSel.appendChild(o); });
      exSel.setAttribute('aria-label', T('Chọn ví dụ', 'Choose an example'));
      if (myEx.length > 1) exWrap.appendChild(exSel); exWrap.appendChild(exBtn);
    }
    bar.appendChild(btn); bar.appendChild(exWrap);
    var clr = el('button', 'labbtn ghost', T('Xóa', 'Clear')); clr.type = 'button'; bar.appendChild(clr);
    host.appendChild(form); host.appendChild(bar); host.appendChild(out);

    function visible(f) { return !f.showIf || f.showIf(raw()); }
    function raw() { var o = {}; spec.fields.forEach(function (f) { o[f.k] = inputs[f.k].value; }); return o; }
    function refresh() { var r = raw(); spec.fields.forEach(function (f) { f._wrap.style.display = visible(f) ? '' : 'none'; }); }
    function collect(show) {
      var r = raw(), vals = {}, ok = true;
      spec.fields.forEach(function (f) {
        errs[f.k].textContent = ''; inputs[f.k].classList.remove('bad'); if (!visible(f)) return;
        if (f.sel) { vals[f.k] = r[f.k]; return; }
        var v = parseNum(r[f.k]), isReq = typeof f.req === 'function' ? f.req(r) : (f.req !== false && !f.opt);
        if (v === null) { if (isReq) { ok = false; if (show) setErr(f.k, T('Bắt buộc nhập.', 'Required.')); } return; }
        if (isNaN(v)) { ok = false; setErr(f.k, T('Không phải số: dùng dấu phẩy hoặc dấu chấm thập phân, ví dụ 1,4 hoặc 1.4.', 'Not a number: use a decimal comma or point, e.g. 1,4 or 1.4.')); return; }
        if (f.min !== undefined && v < f.min || f.minx !== undefined && v <= f.minx || f.max !== undefined && v > f.max) { ok = false; setErr(f.k, f.msg ? (vi ? f.msg[0] : f.msg[1]) : T('Giá trị ngoài miền cho phép.', 'Value outside the allowed range.')); return; }
        if (f.int && v !== Math.floor(v)) { ok = false; setErr(f.k, T('Phải là số nguyên.', 'Must be an integer.')); return; }
        vals[f.k] = v * (f.scale || 1);
      });
      return ok ? vals : null;
    }
    function setErr(k, m) { errs[k].textContent = m; inputs[k].classList.add('bad'); }
    function run(show) {
      refresh(); out.innerHTML = '';
      var vals = collect(show); if (!vals) { if (show) out.appendChild(el('div', 'callout warn', '<b class="t">' + T('Chưa tính được', 'Cannot compute yet') + '</b>' + T('Sửa các ô báo lỗi (màu đỏ) hoặc điền các ô bắt buộc.', 'Fix the red fields or fill in the required ones.'))); return null; }
      var res;
      try { res = spec.run(vals); } catch (e) {
        if (e && e.name === 'ThermoError') {
          var m = errMsg(e); if (e.data && e.data.name && errs[e.data.name]) setErr(e.data.name, T('Xem thông báo bên dưới.', 'See the message below.'));
          out.appendChild(el('div', 'callout bad', '<b class="t">' + T('Đầu vào không hợp lệ', 'Invalid input') + '</b>' + esc(m))); return null;
        } throw e;
      }
      render(res, vals); return res;
    }
    function render(res, vals) {
      (res.warn || []).forEach(function (w) { out.appendChild(el('div', 'callout warn', esc(vi ? w[0] : w[1]))); });
      var tb = '<table class="t labres"><thead><tr><th>' + T('Đại lượng', 'Quantity') + '</th><th>' + T('Giá trị', 'Value') + '</th><th>' + T('Đơn vị SI', 'SI unit') + '</th></tr></thead><tbody>';
      res.rows.forEach(function (r) {
        if (r.h) { tb += '<tr class="sec"><th colspan="3">' + (vi ? r.vi : r.en) + '</th></tr>'; return; }
        tb += '<tr data-k="' + r.k + '"><td class="lq">' + (vi ? r.vi : r.en) + '</td><td class="v" data-v="' + r.v + '">' + (r.txt !== undefined ? r.txt : fmt(r.v)) + '</td><td class="u">' + (r.u || '') + '</td></tr>';
      });
      out.appendChild(el('div', 'tw', tb + '</tbody></table>'));
      var st = el('details', 'steps'); st.open = true; st.appendChild(el('summary', '', T('Các bước tính (công thức và số)', 'Calculation steps (formulas and numbers)')));
      res.steps.forEach(function (s, i) { st.appendChild(el('div', 'step', '<span class="sn">' + (i + 1) + '</span><div class="sb">' + (s.t ? '<p>' + (vi ? s.t[0] : s.t[1]) + '</p>' : '') + (s.f ? '<div class="sf">$' + s.f + '$</div>' : '') + '</div>')); });
      out.appendChild(st);
      if (activeEx) renderRefs(res);
      if (window.renderMath) window.renderMath(out);
    }
    function renderRefs(res) {
      var ex = activeEx, box = el('div', 'refs'), h = '<h4>' + T('Giá trị tham chiếu', 'Reference values') + ' <span class="refsrc">' + esc(vi ? ex.src.vi : ex.src.en) + '</span></h4>';
      h += '<div class="tw"><table class="t refT"><thead><tr><th>' + T('Đại lượng', 'Quantity') + '</th><th>' + T('Máy tính', 'Calculator') + '</th><th>' + T('Tham chiếu', 'Reference') + '</th><th>' + T('Độ lệch', 'Deviation') + '</th><th>' + T('Dung sai', 'Tolerance') + '</th><th></th></tr></thead><tbody>';
      ex.refs.forEach(function (r) {
        var got = res.raw[r.key], dev = Math.abs(got - r.v), ok = dev <= r.tol + 1e-12;
        h += '<tr class="refrow ' + (ok ? 'ok' : 'bad') + '" data-key="' + r.key + '" data-ref="' + r.v + '" data-tol="' + r.tol + '"><td class="lq">' + (vi ? r.vi : r.en) + '</td><td class="v">' + fmt(got) + '</td><td class="rv">' + fmt(r.v, 6) + '</td><td class="dv">' + fmt(dev, 2) + '</td><td>±' + fmt(r.tol, 2) + '</td><td class="mk">' + (ok ? '✓' : '✗') + '</td></tr>';
      });
      h += '</tbody></table></div>';
      var nt = ex.note && (vi ? ex.note.vi : ex.note.en); if (nt) h += '<p class="refnote">' + esc(nt) + '</p>';
      box.innerHTML = h; out.appendChild(box);
    }
    function loadEx() {
      var ex = myEx[exSel ? +exSel.value : 0]; if (!ex) return;
      spec.fields.forEach(function (f) { if (f.sel) { if (ex.args[f.k] !== undefined) inputs[f.k].value = ex.args[f.k]; } else inputs[f.k].value = ex.args[f.k] === undefined ? (f.def !== undefined && !f.opt ? fmtField(f.def) : '') : fmtField(ex.args[f.k] / (f.scale || 1)); });
      activeEx = null; var res = run(true); activeEx = ex; if (res) { out.querySelectorAll('.refs').forEach(function (x) { x.remove(); }); renderRefs(res); if (window.renderMath) window.renderMath(out); }
    }
    btn.addEventListener('click', function () { run(true); });
    exBtn.addEventListener('click', loadEx);
    clr.addEventListener('click', function () { spec.fields.forEach(function (f) { inputs[f.k].value = f.sel ? (f.def || f.sel[0][0]) : (f.def !== undefined ? fmtField(f.def) : ''); }); activeEx = null; run(false); });
    var timer = null;
    host.addEventListener('input', function (ev) { if (ev.isTrusted) activeEx = null; clearTimeout(timer); timer = setTimeout(function () { run(false); }, 250); });
    host.addEventListener('change', function (ev) { if (ev.isTrusted) activeEx = null; clearTimeout(timer); run(false); });
    host.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' && ev.target.tagName === 'INPUT') run(true); });
    refresh();
    this.run = run;
  }

  /* ---------- helpers for rows and steps ---------- */
  function row(k, vi_, en_, v, u, txt) { return { k: k, vi: vi_, en: en_, v: v, u: u || '', txt: txt }; }
  function sec(a, b) { return { h: 1, vi: a, en: b }; }
  function st(f, a, b) { return { f: f, t: a ? [a, b] : null }; }
  var kField = { k: 'k', vi: 'Tỉ số nhiệt dung k = c_p/c_v', en: 'Specific-heat ratio k = c_p/c_v', def: 1.4, u: '–', minx: 1, msg: ['k phải lớn hơn 1.', 'k must be greater than 1.'] };
  var RField = { k: 'R', vi: 'Hằng số khí R', en: 'Gas constant R', def: 0.287, u: 'kJ/(kg·K)', minx: 0, msg: ['R phải dương.', 'R must be positive.'] };
  var cvField = { k: 'cv', vi: 'c_v (tùy chọn; trống = R/(k−1))', en: 'c_v (optional; blank = R/(k−1))', opt: true, u: 'kJ/(kg·K)', minx: 0 };
  var cpField = { k: 'cp', vi: 'c_p (tùy chọn; trống = k·c_v)', en: 'c_p (optional; blank = k·c_v)', opt: true, u: 'kJ/(kg·K)', minx: 0 };
  var T1F = { k: 'T1', vi: 'Nhiệt độ đầu nén T₁', en: 'Inlet temperature T₁', u: 'K', ph: 300, minx: 0, msg: ['T₁ phải dương (kelvin).', 'T₁ must be positive (kelvin).'] };
  var P1F = { k: 'P1', vi: 'Áp suất đầu nén P₁', en: 'Inlet pressure P₁', u: 'kPa', ph: 100, minx: 0, msg: ['P₁ phải dương.', 'P₁ must be positive.'] };
  var V1F = { k: 'V1', vi: 'Thể tích xylanh V₁ (tùy chọn, cho khối lượng và công tổng)', en: 'Cylinder volume V₁ (optional, for mass and total work)', opt: true, u: 'm³', minx: 0 };
  function mixedWarn(o) { return o.mixed ? [[ 'c_p/c_v khác k đã nhập: nhiệt độ, áp suất tính bằng k; nhiệt lượng tính bằng c_p, c_v (cách làm của Tutorials I #2).', 'c_p/c_v differs from the k you entered: temperatures and pressures use k, heats use c_p and c_v (the method of Tutorials I #2).' ]] : []; }

  /* ---------- 1. Otto ---------- */
  var cOtto = { id: 'otto', fields: [
    { k: 'r', vi: 'Tỉ số nén r = V₁/V₂', en: 'Compression ratio r = V₁/V₂', u: '–', ph: 8, minx: 1, msg: ['r phải lớn hơn 1.', 'r must be greater than 1.'] }, kField, RField, T1F, P1F,
    { k: 'mode', vi: 'Cho biết', en: 'Given', sel: [['qin', 'nhiệt cấp q_in', 'heat input q_in'], ['T3', 'nhiệt độ cực đại T₃', 'peak temperature T₃'], ['T4', 'nhiệt độ cuối giãn nở T₄', 'end-of-expansion temperature T₄']] },
    { k: 'qin', vi: 'Nhiệt cấp q_in', en: 'Heat input q_in', u: 'kJ/kg', ph: 800, minx: 0, showIf: function (v) { return v.mode === 'qin'; }, msg: ['q_in phải dương.', 'q_in must be positive.'] },
    { k: 'T3', vi: 'Nhiệt độ cực đại T₃', en: 'Peak temperature T₃', u: 'K', ph: 1800, minx: 0, showIf: function (v) { return v.mode === 'T3'; } },
    { k: 'T4', vi: 'Nhiệt độ cuối giãn nở T₄', en: 'End-of-expansion temperature T₄', u: 'K', ph: 800, minx: 0, showIf: function (v) { return v.mode === 'T4'; } },
    cvField, cpField, V1F ],
    run: function (v) {
      var o = TH.otto(v), r = o.r, k = o.k, rows = [], s = [];
      s.push(st(String.raw`T_2=T_1\,r^{k-1}=${n(o.T1)}\cdot ${n(r)}^{${n(k - 1)}}=${n(o.T2)}${U.K}`, 'Nén đẳng entropi 1→2 (k hằng).', 'Isentropic compression 1→2 (constant k).'));
      s.push(st(String.raw`P_2=P_1\,r^{k}=${n(o.P1)}\cdot ${n(r)}^{${n(k)}}=${n(o.P2)}${U.kPa}`, '', ''));
      if (v.mode === 'qin') s.push(st(String.raw`T_3=T_2+\frac{q_{in}}{c_v}=${n(o.T2)}+\frac{${n(o.qin)}}{${n(o.cv)}}=${n(o.T3)}${U.K}`, 'Cấp nhiệt đẳng tích 2→3: q_in = c_v (T₃ − T₂).', 'Constant-volume heat addition 2→3: q_in = c_v (T₃ − T₂).'));
      else if (v.mode === 'T4') s.push(st(String.raw`T_3=T_4\,r^{k-1}=${n(o.T4)}\cdot ${n(r)}^{${n(k - 1)}}=${n(o.T3)}${U.K}`, 'Cho T₄: giãn nở đẳng entropi 3→4 cho T₃ = T₄·r^(k−1).', 'T₄ is given: isentropic expansion 3→4 gives T₃ = T₄·r^(k−1).'));
      else s.push(st(String.raw`T_3=${n(o.T3)}${U.K}`, 'T₃ do đề cho.', 'T₃ is given.'));
      s.push(st(String.raw`T_4=T_3\,r^{1-k}=${n(o.T3)}\cdot ${n(r)}^{${n(1 - k)}}=${n(o.T4)}${U.K}`, 'Giãn nở đẳng entropi 3→4.', 'Isentropic expansion 3→4.'));
      s.push(st(String.raw`P_3=P_2\frac{T_3}{T_2}=${n(o.P3)}${U.kPa},\qquad P_4=P_1\frac{T_4}{T_1}=${n(o.P4)}${U.kPa}`, 'Đẳng tích: P/T không đổi; 4→1 cũng đẳng tích.', 'Constant volume: P/T is constant; 4→1 is also constant volume.'));
      s.push(st(String.raw`q_{in}=c_v(T_3-T_2)=${n(o.qin)}${U.kJkg},\quad q_{out}=c_v(T_4-T_1)=${n(o.qout)}${U.kJkg}`, 'c_v = ' + fmt(o.cv) + ' kJ/(kg·K).', 'c_v = ' + fmt(o.cv) + ' kJ/(kg·K).'));
      s.push(st(String.raw`w_{net}=q_{in}-q_{out}=${n(o.wnet)}${U.kJkg},\qquad \eta_{th}=\frac{w_{net}}{q_{in}}=${n(o.eta, 5)}`, '', ''));
      s.push(st(String.raw`\eta_{Otto}=1-r^{1-k}=1-${n(r)}^{${n(1 - k)}}=${n(o.etaOtto, 5)}`, 'So sánh: hai cách cho cùng hiệu suất khi c_v không đổi.', 'Check: both routes give the same efficiency when c_v is constant.'));
      s.push(st(String.raw`v_1=\frac{R T_1}{P_1}=${n(o.v1)}${U.m3kg},\quad v_2=\frac{v_1}{r}=${n(o.v2)}${U.m3kg},\quad MEP=\frac{w_{net}}{v_1-v_2}=${n(o.mep)}${U.kPa}`, 'kJ/kg chia cho m³/kg = kPa.', 'kJ/kg divided by m³/kg = kPa.'));
      rows.push(sec('Trạng thái', 'States'), row('T2', '$T_2$', '$T_2$', o.T2, 'K'), row('P2', '$P_2$', '$P_2$', o.P2, 'kPa'), row('T3', '$T_3$', '$T_3$', o.T3, 'K'), row('P3', '$P_3$', '$P_3$', o.P3, 'kPa'), row('T4', '$T_4$', '$T_4$', o.T4, 'K'), row('P4', '$P_4$', '$P_4$', o.P4, 'kPa'),
        sec('Năng lượng riêng và hiệu suất', 'Specific energy and efficiency'), row('qin', '$q_{in}$', '$q_{in}$', o.qin, 'kJ/kg'), row('qout', '$q_{out}$', '$q_{out}$', o.qout, 'kJ/kg'), row('wnet', '$w_{net}$', '$w_{net}$', o.wnet, 'kJ/kg'),
        row('eta', '$\\eta_{th}=w_{net}/q_{in}$', '$\\eta_{th}=w_{net}/q_{in}$', o.eta, '–'), row('etaOtto', '$\\eta_{Otto}=1-r^{1-k}$', '$\\eta_{Otto}=1-r^{1-k}$', o.etaOtto, '–'), row('mep', 'MEP', 'MEP', o.mep, 'kPa'));
      if (o.m !== undefined) {
        s.push(st(String.raw`m=\frac{P_1V_1}{R T_1}=${n(o.m, 5)}${U.kg},\quad Q_{in}=m\,q_{in}=${n(o.Qin)}${U.kJ},\quad W_{net}=m\,w_{net}=${n(o.Wnet)}${U.kJ}`, 'kPa·m³ = kJ.', 'kPa·m³ = kJ.'));
        rows.push(sec('Theo thể tích V₁ đã cho', 'For the given V₁'), row('m', 'm', 'm', o.m, 'kg'), row('Qin', '$Q_{in}$', '$Q_{in}$', o.Qin, 'kJ'), row('Qout', '$Q_{out}$', '$Q_{out}$', o.Qout, 'kJ'), row('Wnet', '$W_{net}$', '$W_{net}$', o.Wnet, 'kJ'));
      }
      return { rows: rows, steps: s, raw: o, warn: mixedWarn(o) };
    } };

  /* ---------- 2. Diesel ---------- */
  var cDiesel = { id: 'diesel', fields: [
    { k: 'r', vi: 'Tỉ số nén r = V₁/V₂', en: 'Compression ratio r = V₁/V₂', u: '–', ph: 18, minx: 1, msg: ['r phải lớn hơn 1.', 'r must be greater than 1.'] }, kField, RField, T1F, P1F,
    { k: 'mode', vi: 'Cho biết', en: 'Given', sel: [['rc', 'tỉ số cutoff r_c', 'cutoff ratio r_c'], ['T3', 'nhiệt độ cực đại T₃', 'peak temperature T₃'], ['qin', 'nhiệt cấp q_in', 'heat input q_in']] },
    { k: 'rc', vi: 'Tỉ số cutoff r_c = V₃/V₂', en: 'Cutoff ratio r_c = V₃/V₂', u: '–', ph: 2, minx: 1, showIf: function (v) { return v.mode === 'rc'; }, msg: ['r_c phải lớn hơn 1 (và nhỏ hơn r).', 'r_c must be greater than 1 (and smaller than r).'] },
    { k: 'T3', vi: 'Nhiệt độ cực đại T₃', en: 'Peak temperature T₃', u: 'K', ph: 2200, minx: 0, showIf: function (v) { return v.mode === 'T3'; } },
    { k: 'qin', vi: 'Nhiệt cấp q_in', en: 'Heat input q_in', u: 'kJ/kg', ph: 1200, minx: 0, showIf: function (v) { return v.mode === 'qin'; } },
    cvField, cpField, V1F ],
    run: function (v) {
      var o = TH.diesel(v), r = o.r, k = o.k, s = [], rows = [];
      s.push(st(String.raw`T_2=T_1\,r^{k-1}=${n(o.T1)}\cdot ${n(r)}^{${n(k - 1)}}=${n(o.T2)}${U.K},\qquad P_2=P_3=P_1 r^{k}=${n(o.P2)}${U.kPa}`, 'Nén đẳng entropi 1→2.', 'Isentropic compression 1→2.'));
      if (v.mode === 'rc') s.push(st(String.raw`T_3=r_c\,T_2=${n(o.rc)}\cdot ${n(o.T2)}=${n(o.T3)}${U.K}`, 'Cấp nhiệt đẳng áp 2→3: V/T không đổi nên T₃/T₂ = r_c.', 'Constant-pressure heat addition 2→3: V/T is constant so T₃/T₂ = r_c.'));
      else if (v.mode === 'T3') s.push(st(String.raw`r_c=\frac{T_3}{T_2}=\frac{${n(o.T3)}}{${n(o.T2)}}=${n(o.rc)}`, 'T₃ cho trước, suy ra tỉ số cutoff.', 'T₃ is given, the cutoff ratio follows.'));
      else s.push(st(String.raw`T_3=T_2+\frac{q_{in}}{c_p}=${n(o.T2)}+\frac{${n(o.qin)}}{${n(o.cp)}}=${n(o.T3)}${U.K},\quad r_c=\frac{T_3}{T_2}=${n(o.rc)}`, 'q_in = c_p (T₃ − T₂).', 'q_in = c_p (T₃ − T₂).'));
      s.push(st(String.raw`T_4=T_3\left(\frac{v_3}{v_4}\right)^{k-1}=T_1\,r_c^{\,k}=${n(o.T1)}\cdot ${n(o.rc)}^{${n(k)}}=${n(o.T4)}${U.K},\quad P_4=P_1\frac{T_4}{T_1}=${n(o.P4)}${U.kPa}`, 'Giãn nở đẳng entropi 3→4 với v₄ = v₁.', 'Isentropic expansion 3→4 with v₄ = v₁.'));
      s.push(st(String.raw`q_{in}=c_p(T_3-T_2)=${n(o.qin)}${U.kJkg},\quad q_{out}=c_v(T_4-T_1)=${n(o.qout)}${U.kJkg},\quad w_{net}=${n(o.wnet)}${U.kJkg}`, '', ''));
      s.push(st(String.raw`\eta_{th}=\frac{w_{net}}{q_{in}}=${n(o.eta, 5)}`, '', ''));
      s.push(st(String.raw`\eta_{Diesel}=1-\frac{1}{r^{k-1}}\,\frac{r_c^{\,k}-1}{k\,(r_c-1)}=${n(o.etaDiesel, 5)}\quad(\eta_{Otto}=${n(o.etaOtto, 5)})`, 'Công thức theo r, r_c, k; luôn nhỏ hơn η_Otto cùng r vì thừa số trong ngoặc > 1.', 'Formula in r, r_c, k; always below η_Otto at the same r because the bracket factor is > 1.'));
      s.push(st(String.raw`v_1=\frac{R T_1}{P_1}=${n(o.v1)}${U.m3kg},\quad MEP=\frac{w_{net}}{v_1-v_2}=\frac{w_{net}}{v_1(1-1/r)}=${n(o.mep)}${U.kPa}`, '', ''));
      rows.push(sec('Trạng thái', 'States'), row('rc', '$r_c$', '$r_c$', o.rc, '–'), row('T2', '$T_2$', '$T_2$', o.T2, 'K'), row('P2', '$P_2=P_3$', '$P_2=P_3$', o.P2, 'kPa'), row('T3', '$T_3$', '$T_3$', o.T3, 'K'), row('T4', '$T_4$', '$T_4$', o.T4, 'K'), row('P4', '$P_4$', '$P_4$', o.P4, 'kPa'),
        sec('Năng lượng riêng và hiệu suất', 'Specific energy and efficiency'), row('qin', '$q_{in}$', '$q_{in}$', o.qin, 'kJ/kg'), row('qout', '$q_{out}$', '$q_{out}$', o.qout, 'kJ/kg'), row('wnet', '$w_{net}$', '$w_{net}$', o.wnet, 'kJ/kg'),
        row('eta', '$\\eta_{th}=w_{net}/q_{in}$', '$\\eta_{th}=w_{net}/q_{in}$', o.eta, '–'), row('etaDiesel', '$\\eta_{Diesel}(r,r_c,k)$', '$\\eta_{Diesel}(r,r_c,k)$', o.etaDiesel, '–'), row('etaOtto', '$\\eta_{Otto}$ (' + T('cùng r', 'same r') + ')', '$\\eta_{Otto}$ (same r)', o.etaOtto, '–'), row('mep', 'MEP', 'MEP', o.mep, 'kPa'));
      if (o.m !== undefined) {
        s.push(st(String.raw`m=\frac{P_1V_1}{R T_1}=${n(o.m, 5)}${U.kg},\quad Q_{in}=${n(o.Qin)}${U.kJ},\quad W_{net}=${n(o.Wnet)}${U.kJ}`, 'kPa·m³ = kJ.', 'kPa·m³ = kJ.'));
        rows.push(sec('Theo thể tích V₁ đã cho', 'For the given V₁'), row('m', 'm', 'm', o.m, 'kg'), row('Qin', '$Q_{in}$', '$Q_{in}$', o.Qin, 'kJ'), row('Qout', '$Q_{out}$', '$Q_{out}$', o.Qout, 'kJ'), row('Wnet', '$W_{net}$', '$W_{net}$', o.Wnet, 'kJ'));
      }
      return { rows: rows, steps: s, raw: o, warn: mixedWarn(o) };
    } };

  /* ---------- 3. Brayton ---------- */
  var cBray = { id: 'brayton', fields: [
    { k: 'rp', vi: 'Tỉ số áp tổng r_p = P₂/P₁', en: 'Overall pressure ratio r_p = P₂/P₁', u: '–', ph: 8, minx: 1, msg: ['r_p phải lớn hơn 1.', 'r_p must be greater than 1.'] }, T1F,
    { k: 'T3', vi: 'Nhiệt độ vào tuabin T₃', en: 'Turbine inlet temperature T₃', u: 'K', ph: 1000, minx: 0 }, Object.assign({}, P1F, { def: 100, ph: undefined }), kField, RField,
    { k: 'cp', vi: 'c_p (tùy chọn; trống = kR/(k−1))', en: 'c_p (optional; blank = kR/(k−1))', opt: true, u: 'kJ/(kg·K)', minx: 0 },
    { k: 'etac', vi: 'Hiệu suất đẳng entropi máy nén η_c', en: 'Compressor isentropic efficiency η_c', def: 1, u: '–', minx: 0, max: 1, msg: ['η_c phải trong (0; 1].', 'η_c must lie in (0, 1].'] },
    { k: 'etat', vi: 'Hiệu suất đẳng entropi tuabin η_t', en: 'Turbine isentropic efficiency η_t', def: 1, u: '–', minx: 0, max: 1, msg: ['η_t phải trong (0; 1].', 'η_t must lie in (0, 1].'] },
    { k: 'eps', vi: 'Hiệu suất bộ hồi nhiệt ε (0 = không hồi nhiệt)', en: 'Regenerator effectiveness ε (0 = none)', def: 0, u: '–', min: 0, max: 1, msg: ['ε phải trong [0; 1].', 'ε must lie in [0, 1].'] },
    { k: 'Nc', vi: 'Số tầng nén (làm mát trung gian giữa các tầng)', en: 'Compression stages (intercooling between stages)', def: 1, u: '–', min: 1, max: 10, int: true, msg: ['Số tầng: số nguyên 1 đến 10.', 'Stages: integer 1 to 10.'] },
    { k: 'Nt', vi: 'Số tầng giãn nở (hâm nóng giữa các tầng)', en: 'Expansion stages (reheat between stages)', def: 1, u: '–', min: 1, max: 10, int: true, msg: ['Số tầng: số nguyên 1 đến 10.', 'Stages: integer 1 to 10.'] } ],
    run: function (v) {
      var o = TH.brayton(v), opt = TH.braytonOptRp(v), k = o.k, e = (k - 1) / k, s = [], rows = [], eff = o.etac < 1 || o.etat < 1;
      s.push(st(String.raw`c_p=\frac{kR}{k-1}=${n(o.cp)}${U.kJkgK},\qquad r_{p,c}=r_p^{1/N_c}=${n(o.prc)},\quad r_{p,t}=r_p^{1/N_t}=${n(o.prt)}`, 'Tỉ số áp chia đều cho mỗi tầng (slide Ch.2 tr.33–48).', 'The pressure ratio is split equally between stages (slide Ch.2 p.33–48).'));
      s.push(st(String.raw`T_{2s}=T_1\,r_{p,c}^{(k-1)/k}=${n(o.T1)}\cdot ${n(o.prc)}^{${n(e)}}=${n(o.Tcs)}${U.K},\qquad T_2=T_1+\frac{T_{2s}-T_1}{\eta_c}=${n(o.Tc)}${U.K}`, 'Máy nén (mỗi tầng vào ở T₁ nhờ làm mát trung gian hoàn hảo).', 'Compressor (each stage starts at T₁ thanks to perfect intercooling).'));
      s.push(st(String.raw`T_{4s}=\frac{T_3}{r_{p,t}^{(k-1)/k}}=${n(o.Tts)}${U.K},\qquad T_4=T_3-\eta_t(T_3-T_{4s})=${n(o.Tt)}${U.K}`, 'Tuabin (mỗi tầng vào ở T₃ nhờ hâm nóng hoàn hảo).', 'Turbine (each stage starts at T₃ thanks to perfect reheating).'));
      s.push(st(String.raw`w_c=N_c c_p(T_2-T_1)=${n(o.wc)}${U.kJkg},\quad w_t=N_t c_p(T_3-T_4)=${n(o.wt)}${U.kJkg},\quad w_{net}=${n(o.wnet)}${U.kJkg},\quad \frac{w_c}{w_t}=${n(o.bwr, 4)}`, 'Tỉ số công nén/công tuabin (back-work ratio).', 'Back-work ratio = compressor work / turbine work.'));
      if (o.eps > 0) s.push(st(String.raw`T_5=T_2+\varepsilon(T_4-T_2)=${n(o.T5)}${U.K},\qquad T_6=T_4-(T_5-T_2)=${n(o.T6)}${U.K}`, 'Hồi nhiệt: ε = (T₅ − T₂)/(T₄ − T₂); cân bằng năng lượng cho dòng nóng.', 'Regeneration: ε = (T₅ − T₂)/(T₄ − T₂); energy balance for the hot stream.'));
      s.push(st(String.raw`q_{in}=c_p(T_3-T_5)${o.Nt > 1 ? String.raw`+(N_t-1)c_p(T_3-T_4)` : ''}=${n(o.qin)}${U.kJkg},\qquad \eta_{th}=\frac{w_{net}}{q_{in}}=${n(o.eta, 5)}`, o.eps > 0 ? 'T₅ = T₂ khi không hồi nhiệt; có hồi nhiệt thì buồng đốt chỉ nâng từ T₅ lên T₃.' : '', o.eps > 0 ? 'T₅ = T₂ with no regeneration; with it the combustor only heats from T₅ to T₃.' : ''));
      s.push(st(String.raw`q_{out}=q_{in}-w_{net}=${n(o.qout)}${U.kJkg},\qquad c_p(T_6-T_1)+(N_c-1)c_p(T_2-T_1)=${n(o.qoutCheck)}${U.kJkg}`, 'Kiểm tra: nhiệt thải tính bằng hai cách (hiệu số q_in − w_net và cộng các bộ làm mát) phải bằng nhau.', 'Check: the heat rejected computed two ways (q_in − w_net, and the sum over the coolers) must agree.'));
      s.push(st(String.raw`\eta_{ideal}=1-r_p^{-(k-1)/k}=${n(o.etaIdeal, 5)}`, 'Hiệu suất của chu trình đơn giản đẳng entropi, để so sánh.', 'Efficiency of the simple isentropic cycle, for comparison.'));
      s.push(st(String.raw`r_{p,opt}=\left(\eta_c\eta_t\frac{T_3}{T_1}\right)^{N k/(2(k-1))}=${n(opt.rp)}`, opt.method === 'closed' ? 'Công thức đóng cho w_net cực đại (khi N_c = N_t = N): x = r_p^((k−1)/k) = N-lũy thừa của √(η_c η_t T₃/T₁).' : 'N_c ≠ N_t: không có công thức đóng, tìm số (golden-section) trên w_net(r_p).', opt.method === 'closed' ? 'Closed form for maximum w_net (when N_c = N_t = N): x = r_p^((k−1)/k) = (√(η_c η_t T₃/T₁))^N.' : 'N_c ≠ N_t: no closed form, found numerically (golden section) on w_net(r_p).'));
      rows.push(sec('Trạng thái (nhiệt độ)', 'States (temperatures)'), row('T1', '$T_1$', '$T_1$', o.T1, 'K'), row('Tc', '$T_2$ (' + T('ra máy nén, mỗi tầng', 'compressor exit, per stage') + ')', '$T_2$ (compressor exit, per stage)', o.Tc, 'K'));
      if (o.eps > 0) rows.push(row('T5', '$T_5$ (' + T('vào buồng đốt sau hồi nhiệt', 'combustor inlet after regenerator') + ')', '$T_5$ (combustor inlet after regenerator)', o.T5, 'K'));
      rows.push(row('T3', '$T_3$', '$T_3$', o.T3, 'K'), row('Tt', '$T_4$ (' + T('ra tuabin, mỗi tầng', 'turbine exit, per stage') + ')', '$T_4$ (turbine exit, per stage)', o.Tt, 'K'));
      if (o.eps > 0) rows.push(row('T6', '$T_6$ (' + T('khí thải sau hồi nhiệt', 'exhaust after regenerator') + ')', '$T_6$ (exhaust after regenerator)', o.T6, 'K'));
      rows.push(sec('Áp suất', 'Pressures'), row('P2', '$P_2$', '$P_2$', o.P2, 'kPa'));
      if (o.Nc > 1) rows.push(row('Pmid_c', T('$P$ giữa các tầng nén (làm mát trung gian)', '$P$ between compressor stages (intercooler)'), '$P$ between compressor stages (intercooler)', o.Pmid_c, 'kPa'));
      if (o.Nt > 1) rows.push(row('Pmid_t', T('$P$ vào tầng giãn nở cuối (hâm nóng)', '$P$ at the last expansion stage (reheat)'), '$P$ at the last expansion stage (reheat)', o.Pmid_t, 'kPa'));
      rows.push(sec('Công, nhiệt, hiệu suất', 'Work, heat, efficiency'), row('wc', '$w_{comp}$', '$w_{comp}$', o.wc, 'kJ/kg'), row('wt', '$w_{turb}$', '$w_{turb}$', o.wt, 'kJ/kg'), row('wnet', '$w_{net}$', '$w_{net}$', o.wnet, 'kJ/kg'), row('bwr', 'back-work ratio $w_{comp}/w_{turb}$', 'back-work ratio $w_{comp}/w_{turb}$', o.bwr, '–'),
        row('qin', '$q_{in}$', '$q_{in}$', o.qin, 'kJ/kg'), row('qout', '$q_{out}$', '$q_{out}$', o.qout, 'kJ/kg'), row('eta', '$\\eta_{th}$', '$\\eta_{th}$', o.eta, '–'), row('etaIdeal', '$\\eta_{ideal}=1-r_p^{-(k-1)/k}$', '$\\eta_{ideal}=1-r_p^{-(k-1)/k}$', o.etaIdeal, '–'),
        row('rpOpt', '$r_{p,opt}$ (' + T('cực đại $w_{net}$', 'maximum $w_{net}$') + ')', '$r_{p,opt}$ (maximum $w_{net}$)', opt.rp, '–'));
      o.rpOpt = opt.rp;
      if (o.eps > 0) { o.rpCross = TH.regenCrossover(v); rows.push(row('rpCross', T('$r_p$ tại đó hồi nhiệt hết lợi (ε = 1, lý tưởng)', '$r_p$ above which regeneration stops helping (ε = 1, ideal)'), '$r_p$ above which regeneration stops helping (ε = 1, ideal)', o.rpCross, '\u2013'));
        s.push(st(String.raw`r_{p,x}=\left(\frac{T_3}{T_1}\right)^{k/(2(k-1))}=${n(o.rpCross)}`, 'Hồi nhiệt lý tưởng (ε = 1) chỉ có lợi khi r_p < giá trị này (slide Ch.2 tr.45): nghiệm của 1 − (T₁/T₃)·x = 1 − 1/x.', 'Ideal regeneration (ε = 1) only helps for r_p below this value (slide Ch.2 p.45): the solution of 1 − (T₁/T₃)·x = 1 − 1/x.')); }
      var warn = mixedWarn(o); if (o.etac < 1 || o.etat < 1) warn.push(['Có tổn thất (η < 1): η_th thấp hơn η_ideal; r_p,opt tính cho w_net.', 'With losses (η < 1): η_th falls below η_ideal; r_p,opt is for w_net.']);
      return { rows: rows, steps: s, raw: o, warn: warn };
    } };

  /* ---------- 4. Isentropic flow: six small tools ---------- */
  var kF = { k: 'k', vi: 'Tỉ số nhiệt dung k', en: 'Specific-heat ratio k', def: 1.4, u: '–', minx: 1, msg: ['k phải lớn hơn 1.', 'k must be greater than 1.'] };
  var RF = { k: 'R', vi: 'Hằng số khí R (không khí: Appendix 1 Table A-1)', en: 'Gas constant R (air: Appendix 1 Table A-1)', def: 0.287, u: 'kJ/(kg·K)', minx: 0, msg: ['R phải dương.', 'R must be positive.'] };
  var cMa = { id: 'flow_ma', fields: [kF, { k: 'Ma', vi: 'Số Mach Ma', en: 'Mach number Ma', u: '–', ph: 2, min: 0, msg: ['Ma ≥ 0.', 'Ma ≥ 0.'] }],
    run: function (v) {
      var o = TH.fromMa(v.Ma, v.k), k = o.k, M = o.Ma, f = String.raw`1+\frac{k-1}{2}Ma^2`, s = [];
      s.push(st(String.raw`\frac{T}{T_0}=\left(${f}\right)^{-1}=${n(o.TT0, 5)}`, 'Dòng đẳng entropi của khí lý tưởng, k hằng.', 'Isentropic flow of an ideal gas, constant k.'));
      s.push(st(String.raw`\frac{P}{P_0}=\left(\frac{T}{T_0}\right)^{k/(k-1)}=${n(o.PP0, 5)},\qquad \frac{\rho}{\rho_0}=\left(\frac{T}{T_0}\right)^{1/(k-1)}=${n(o.rr0, 5)}`, '', ''));
      s.push(st(String.raw`\frac{A}{A^*}=\frac{1}{Ma}\left[\frac{2}{k+1}\left(${f}\right)\right]^{\frac{k+1}{2(k-1)}}=${M === 0 ? String.raw`\infty` : n(o.AAs, 5)}`, 'Mỗi A/A* > 1 ứng với hai số Mach: một dưới âm, một trên âm.', 'Every A/A* > 1 belongs to two Mach numbers: one subsonic, one supersonic.'));
      return { rows: [row('TT0', '$T/T_0$', '$T/T_0$', o.TT0, '–'), row('PP0', '$P/P_0$', '$P/P_0$', o.PP0, '–'), row('rr0', '$\\rho/\\rho_0$', '$\\rho/\\rho_0$', o.rr0, '–'), row('AAs', '$A/A^*$', '$A/A^*$', o.AAs, '–')], steps: s, raw: o };
    } };
  var cAas = { id: 'flow_aas', fields: [kF,
    { k: 'mode', vi: 'Cho biết', en: 'Given', sel: [['A1s', 'A/A* của mặt cắt 1', 'A/A* of section 1'], ['Ma1', 'Ma của mặt cắt 1 và A₂/A₁', 'Ma of section 1 and A₂/A₁']] },
    { k: 'A1s', vi: 'A/A* (≥ 1)', en: 'A/A* (≥ 1)', u: '–', ph: 2.0351, min: 1, showIf: function (v) { return v.mode === 'A1s'; }, msg: ['A/A* phải ≥ 1.', 'A/A* must be ≥ 1.'] },
    { k: 'Ma1', vi: 'Ma của mặt cắt 1', en: 'Ma of section 1', u: '–', ph: 0.3, minx: 0, showIf: function (v) { return v.mode === 'Ma1'; }, msg: ['Ma phải dương.', 'Ma must be positive.'] },
    { k: 'A2A1', vi: 'Tỉ số diện tích A₂/A₁ (1 = giữ nguyên)', en: 'Area ratio A₂/A₁ (1 = unchanged)', u: '–', def: 1, minx: 0, showIf: function (v) { return v.mode === 'Ma1'; } },
    { k: 'branch', vi: 'Nhánh nghiệm', en: 'Root branch', sel: [['sub', 'dưới âm (Ma < 1)', 'subsonic (Ma < 1)'], ['sup', 'trên âm (Ma > 1)', 'supersonic (Ma > 1)']] },
    { k: 'T1', vi: 'T₁ (tùy chọn, để tính T₂)', en: 'T₁ (optional, to get T₂)', opt: true, u: 'K', minx: 0, showIf: function (v) { return v.mode === 'Ma1'; } },
    { k: 'P1', vi: 'P₁ (tùy chọn, để tính P₂)', en: 'P₁ (optional, to get P₂)', opt: true, u: 'kPa', minx: 0, showIf: function (v) { return v.mode === 'Ma1'; } } ],
    run: function (v) {
      var p = { k: v.k, branch: v.branch, A2A1: v.mode === 'A1s' ? 1 : v.A2A1, T1: v.T1, P1: v.P1 };
      if (v.mode === 'Ma1') p.Ma1 = v.Ma1; else p.A1s = v.A1s;
      var o = TH.duct(p), s = [], rows = [];
      if (v.mode === 'Ma1') s.push(st(String.raw`\frac{A_1}{A^*}=f(Ma_1)=${n(o.A1s, 5)},\quad \frac{T_1}{T_0}=${n(o.T1T0, 5)},\quad \frac{P_1}{P_0}=${n(o.P1P0, 5)}`, 'Mặt cắt 1 từ số Mach (hàm đẳng entropi).', 'Section 1 from the Mach number (isentropic functions).'));
      s.push(st(String.raw`\frac{A_2}{A^*}=\frac{A_2}{A_1}\cdot\frac{A_1}{A^*}=${n(p.A2A1)}\cdot ${n(o.A1s, 5)}=${n(o.A2s, 5)}`, v.mode === 'Ma1' ? 'Dòng đẳng entropi giữ nguyên A*.' : 'A/A* cho trước.', v.mode === 'Ma1' ? 'Isentropic flow keeps A* unchanged.' : 'A/A* is given.'));
      s.push(st(String.raw`\frac{A}{A^*}\bigl(Ma_2\bigr)=${n(o.A2s, 5)}\ \Rightarrow\ Ma_2=${n(o.Ma2, 5)}\quad(${o.branch === 'sub' ? T('nhánh dưới âm', 'subsonic branch') : T('nhánh trên âm', 'supersonic branch')})`, 'Giải phương trình A/A*(Ma) bằng chia đôi trên nhánh đã chọn.', 'A/A*(Ma) is solved by bisection on the chosen branch.'));
      s.push(st(String.raw`\frac{T_2}{T_0}=${n(o.T2T0, 5)},\quad \frac{P_2}{P_0}=${n(o.P2P0, 5)},\quad \frac{\rho_2}{\rho_0}=${n(o.r2r0, 5)}`, '', ''));
      if (o.T2 !== undefined) s.push(st(String.raw`T_2=T_1\frac{T_2/T_0}{T_1/T_0}=${n(o.T2)}${U.K}`, '', ''));
      if (o.P2 !== undefined) s.push(st(String.raw`P_2=P_1\frac{P_2/P_0}{P_1/P_0}=${n(o.P2)}${U.kPa}`, '', ''));
      if (v.mode === 'Ma1') rows.push(row('A1s', '$A_1/A^*$', '$A_1/A^*$', o.A1s, '–'), row('T1T0', '$T_1/T_0$', '$T_1/T_0$', o.T1T0, '–'), row('P1P0', '$P_1/P_0$', '$P_1/P_0$', o.P1P0, '–'));
      rows.push(row('A2s', '$A_2/A^*$', '$A_2/A^*$', o.A2s, '–'), row('Ma2', '$Ma_2$', '$Ma_2$', o.Ma2, '–'), row('T2T0', '$T_2/T_0$', '$T_2/T_0$', o.T2T0, '–'), row('P2P0', '$P_2/P_0$', '$P_2/P_0$', o.P2P0, '–'), row('r2r0', '$\\rho_2/\\rho_0$', '$\\rho_2/\\rho_0$', o.r2r0, '–'));
      if (o.T2 !== undefined) rows.push(row('T2', '$T_2$', '$T_2$', o.T2, 'K')); if (o.P2 !== undefined) rows.push(row('P2', '$P_2$', '$P_2$', o.P2, 'kPa'));
      return { rows: rows, steps: s, raw: o };
    } };
  var cPr = { id: 'flow_pr', fields: [kF, RF,
    { k: 'mode', vi: 'Cho biết', en: 'Given', sel: [['ratio', 'tỉ số P/P₀', 'ratio P/P₀'], ['abs', 'P và P₀', 'P and P₀']] },
    { k: 'PP0', vi: 'Tỉ số P/P₀ (0 < P/P₀ ≤ 1)', en: 'Ratio P/P₀ (0 < P/P₀ ≤ 1)', u: '–', ph: 0.857, minx: 0, max: 1, showIf: function (v) { return v.mode === 'ratio'; }, msg: ['P/P₀ phải trong (0; 1].', 'P/P₀ must lie in (0, 1].'] },
    { k: 'P', vi: 'Áp suất tĩnh P', en: 'Static pressure P', u: 'kPa', ph: 1200, minx: 0, showIf: function (v) { return v.mode === 'abs'; } },
    { k: 'P0', vi: 'Áp suất hãm P₀ (tùy chọn nếu chọn tỉ số)', en: 'Stagnation pressure P₀ (optional with a ratio)', u: 'kPa', ph: 1400, minx: 0, opt: true, req: function (r) { return r.mode === 'abs'; } },
    { k: 'T0', vi: 'Nhiệt độ hãm T₀ (tùy chọn, để tính T, c, V)', en: 'Stagnation temperature T₀ (optional, to get T, c, V)', u: 'K', minx: 0, opt: true },
    { k: 'mdot', vi: 'Lưu lượng khối lượng (tùy chọn, để tính diện tích)', en: 'Mass flow (optional, to get the area)', u: 'kg/s', minx: 0, opt: true } ],
    run: function (v) {
      var p = { k: v.k, R: v.R, T0: v.T0, P0: v.P0, mdot: v.mdot }; if (v.mode === 'abs') p.P = v.P; else p.PP0 = v.PP0;
      var o = TH.fromPratio(p), s = [], rows = [];
      s.push(st(String.raw`Ma=\sqrt{\frac{2}{k-1}\left[\left(\frac{P_0}{P}\right)^{(k-1)/k}-1\right]}=${n(o.Ma, 5)}`, 'Đảo phương trình P/P₀(Ma): có nghiệm kín.', 'Inverting P/P₀(Ma) has a closed-form solution.'));
      s.push(st(String.raw`\frac{T}{T_0}=${n(o.TT0, 5)},\quad \frac{\rho}{\rho_0}=${n(o.rr0, 5)},\quad \frac{A}{A^*}=${o.Ma === 0 ? String.raw`\infty` : n(o.AAs, 5)}`, '', ''));
      rows.push(row('PP0', '$P/P_0$', '$P/P_0$', o.PP0, '–'), row('Ma', 'Ma', 'Ma', o.Ma, '–'), row('TT0', '$T/T_0$', '$T/T_0$', o.TT0, '–'), row('rr0', '$\\rho/\\rho_0$', '$\\rho/\\rho_0$', o.rr0, '–'), row('AAs', '$A/A^*$', '$A/A^*$', o.AAs, '–'));
      if (o.T !== undefined) {
        s.push(st(String.raw`T=T_0\frac{T}{T_0}=${n(o.T)}${U.K},\qquad c=\sqrt{kRT}=\sqrt{${n(o.k)}\cdot ${n(o.R * 1000)}\cdot ${n(o.T)}}=${n(o.c)}${U.ms},\qquad V=Ma\,c=${n(o.V)}${U.ms}`, 'R đổi sang J/(kg·K) (×1000) để c ra m/s.', 'R is converted to J/(kg·K) (×1000) so that c comes out in m/s.'));
        rows.push(sec('Theo T₀ đã cho', 'For the given T₀'), row('T', '$T$', '$T$', o.T, 'K'), row('c', T('vận tốc âm $c$', 'speed of sound $c$'), 'speed of sound $c$', o.c, 'm/s'), row('V', '$V=Ma\\,c$', '$V=Ma\\,c$', o.V, 'm/s'));
      }
      if (o.P !== undefined) { s.push(st(String.raw`P=P_0\frac{P}{P_0}=${n(o.P)}${U.kPa},\qquad \rho=\frac{P}{RT}=${n(o.rho)}${U.kgm3}`, 'kPa / (kJ/(kg·K) · K) = kg/m³.', 'kPa / (kJ/(kg·K) · K) = kg/m³.')); rows.push(row('P', '$P$', '$P$', o.P, 'kPa'), row('rho', '$\\rho$', '$\\rho$', o.rho, 'kg/m³')); }
      if (o.A !== undefined) { s.push(st(String.raw`A=\frac{\dot m}{\rho V}=\frac{${n(p.mdot)}}{${n(o.rho)}\cdot ${n(o.V)}}=${n(o.A, 5)}${U.m2}=${n(o.A * 1e4, 5)}\,\mathrm{cm^2}`, '', '')); rows.push(row('A', '$A$', '$A$', o.A * 1e4, 'cm²')); o.A_cm2 = o.A * 1e4; rows[rows.length - 1].k = 'A_cm2'; }
      return { rows: rows, steps: s, raw: o };
    } };
  var cStag = { id: 'flow_stag', fields: [kF, RF,
    { k: 'T', vi: 'Nhiệt độ tĩnh T', en: 'Static temperature T', u: 'K', ph: 255.7, minx: 0 },
    { k: 'P', vi: 'Áp suất tĩnh P', en: 'Static pressure P', u: 'kPa', ph: 54.05, minx: 0 },
    { k: 'V', vi: 'Vận tốc V', en: 'Velocity V', u: 'm/s', ph: 250, min: 0 } ],
    run: function (v) {
      var o = TH.stagnation(v), cr = TH.critical({ k: v.k }), s = [], rows = [];
      s.push(st(String.raw`c_p=\frac{kR}{k-1}=${n(o.cp)}${U.kJkgK},\qquad T_0=T+\frac{V^2}{2c_p}=${n(o.T)}+\frac{${n(o.V)}^2}{2\cdot ${n(o.cp * 1000)}}=${n(o.T0)}${U.K}`, 'V²/(2c_p) tính bằng J/kg nên c_p đổi sang J/(kg·K).', 'V²/(2c_p) is in J/kg so c_p is converted to J/(kg·K).'));
      s.push(st(String.raw`P_0=P\left(\frac{T_0}{T}\right)^{k/(k-1)}=${n(o.P)}\cdot\left(\frac{${n(o.T0)}}{${n(o.T)}}\right)^{${n(o.k / (o.k - 1))}}=${n(o.P0)}${U.kPa}`, 'Hãm đẳng entropi.', 'Isentropic stagnation.'));
      s.push(st(String.raw`c=\sqrt{kRT}=${n(o.c)}${U.ms},\qquad Ma=\frac{V}{c}=${n(o.Ma, 5)},\qquad \Delta T=T_0-T=${n(o.dT)}${U.K},\quad \Delta P=P_0-P=${n(o.dP)}${U.kPa}`, '', ''));
      rows.push(row('T0', '$T_0$', '$T_0$', o.T0, 'K'), row('P0', '$P_0$', '$P_0$', o.P0, 'kPa'), row('dT', '$T_0-T$', '$T_0-T$', o.dT, 'K'), row('dP', '$P_0-P$', '$P_0-P$', o.dP, 'kPa'), row('Ma', 'Ma', 'Ma', o.Ma, '–'), row('c', '$c$', '$c$', o.c, 'm/s'));
      return { rows: rows, steps: s, raw: o };
    } };
  var cCrit = { id: 'flow_crit', fields: [kF, RF,
    { k: 'P0', vi: 'Áp suất hãm P₀', en: 'Stagnation pressure P₀', u: 'kPa', ph: 1000, minx: 0 },
    { k: 'T0', vi: 'Nhiệt độ hãm T₀', en: 'Stagnation temperature T₀', u: 'K', ph: 500, minx: 0 },
    { k: 'Astar', vi: 'Diện tích họng A*', en: 'Throat area A*', u: 'cm²', ph: 10, scale: 1e-4, minx: 0, msg: ['A* phải dương.', 'A* must be positive.'] } ],
    run: function (v) {
      var cr = TH.critical({ k: v.k }), md = TH.chokedMdot({ Astar: v.Astar, P0: v.P0, T0: v.T0, k: v.k, R: v.R }), k = v.k, s = [], rows = [], o = Object.assign({}, cr, { mdot: md, Tstar: v.T0 * cr.TsT0, Pstar: v.P0 * cr.PsP0 });
      s.push(st(String.raw`\frac{T^*}{T_0}=\frac{2}{k+1}=${n(cr.TsT0, 5)},\quad \frac{P^*}{P_0}=\left(\frac{2}{k+1}\right)^{\frac{k}{k-1}}=${n(cr.PsP0, 5)},\quad \frac{\rho^*}{\rho_0}=\left(\frac{2}{k+1}\right)^{\frac{1}{k-1}}=${n(cr.rsr0, 5)}`, 'Tỉ số tới hạn: đặt Ma = 1.', 'Critical ratios: set Ma = 1.'));
      s.push(st(String.raw`T^*=${n(o.Tstar)}${U.K},\qquad P^*=${n(o.Pstar)}${U.kPa}`, '', ''));
      s.push(st(String.raw`\dot m=A^*P_0\sqrt{\frac{k}{RT_0}}\left(\frac{2}{k+1}\right)^{\frac{k+1}{2(k-1)}}=${n(v.Astar, 5)}\cdot ${n(v.P0 * 1000)}\cdot\sqrt{\frac{${n(k)}}{${n(v.R * 1000)}\cdot ${n(v.T0)}}}\cdot ${n(Math.pow(2 / (k + 1), (k + 1) / (2 * (k - 1))), 5)}=${n(md, 5)}${U.kgs}`, 'Đơn vị: P₀ đổi sang Pa (×1000), R sang J/(kg·K) (×1000), A* theo m²: ra kg/s.', 'Units: P₀ in Pa (×1000), R in J/(kg·K) (×1000), A* in m²: gives kg/s.'));
      rows.push(row('TsT0', '$T^*/T_0$', '$T^*/T_0$', cr.TsT0, '–'), row('PsP0', '$P^*/P_0$', '$P^*/P_0$', cr.PsP0, '–'), row('rsr0', '$\\rho^*/\\rho_0$', '$\\rho^*/\\rho_0$', cr.rsr0, '–'), row('Tstar', '$T^*$', '$T^*$', o.Tstar, 'K'), row('Pstar', '$P^*$', '$P^*$', o.Pstar, 'kPa'), row('mdot', T('lưu lượng nghẹt $\\dot m$', 'choked flow $\\dot m$'), 'choked flow $\\dot m$', md, 'kg/s'));
      return { rows: rows, steps: s, raw: o };
    } };
  var cNoz = { id: 'flow_noz', fields: [kF, RF,
    { k: 'T', vi: 'Nhiệt độ tĩnh ở cửa vào T', en: 'Inlet static temperature T', u: 'K', ph: 873, minx: 0 },
    { k: 'P', vi: 'Áp suất tĩnh ở cửa vào P', en: 'Inlet static pressure P', u: 'kPa', ph: 1000, minx: 0 },
    { k: 'V', vi: 'Vận tốc cửa vào V (0 = đã là điều kiện hãm)', en: 'Inlet velocity V (0 = already stagnation)', u: 'm/s', def: 0, min: 0 },
    { k: 'Pb', vi: 'Áp suất ngược P_b', en: 'Back pressure P_b', u: 'kPa', ph: 700, minx: 0 },
    { k: 'Ae', vi: 'Diện tích cửa ra A (= họng)', en: 'Exit (throat) area A', u: 'cm²', ph: 50, scale: 1e-4, minx: 0, msg: ['A phải dương.', 'A must be positive.'] } ],
    run: function (v) {
      var o = TH.convergingNozzle(v), s = [], rows = [], k = o.k;
      var st0 = TH.stagnation({ T: v.T, P: v.P, V: v.V, k: v.k, R: v.R });
      s.push(st(String.raw`T_0=T+\frac{V^2}{2c_p}=${n(o.T0)}${U.K},\qquad P_0=P\left(\frac{T_0}{T}\right)^{k/(k-1)}=${n(o.P0)}${U.kPa}`, 'Tính chất hãm tại cửa vào.', 'Stagnation properties at the inlet.'));
      s.push(st(String.raw`\left(\frac{P^*}{P_0}\right)=\left(\frac{2}{k+1}\right)^{k/(k-1)}=${n(o.PcritP0, 5)}\ \Rightarrow\ P^*=${n(o.Pcrit)}${U.kPa}\ ,\qquad \frac{P_b}{P_0}=${n(o.PbP0, 5)}`, 'Vòi hội tụ nghẹt khi P_b/P₀ ≤ P*/P₀.', 'A converging nozzle chokes when P_b/P₀ ≤ P*/P₀.'));
      if (o.choked) s.push(st(String.raw`Ma_e=1,\ P_e=P^*=${n(o.Pe)}${U.kPa},\ T_e=T^*=${n(o.Te)}${U.K}`, 'NGHẸT: P_b/P₀ nhỏ hơn tỉ số tới hạn nên cửa ra đạt Ma = 1; lưu lượng cực đại, không phụ thuộc P_b nữa.', 'CHOKED: P_b/P₀ is below the critical ratio so the exit reaches Ma = 1; the mass flow is at its maximum and no longer depends on P_b.'));
      else s.push(st(String.raw`P_e=P_b,\ Ma_e=${n(o.Ma, 5)},\ T_e=T_0\frac{T}{T_0}=${n(o.Te)}${U.K}`, 'KHÔNG nghẹt: P_b > P*, áp suất cửa ra bằng P_b, dòng dưới âm.', 'NOT choked: P_b > P*, the exit pressure equals P_b and the flow is subsonic.'));
      s.push(st(String.raw`\rho_e=\frac{P_e}{RT_e}=${n(o.rho)}${U.kgm3},\quad V_e=Ma_e\sqrt{kRT_e}=${n(o.V)}${U.ms},\quad \dot m=\rho_e A V_e=${n(o.mdot, 5)}${U.kgs}`, 'Khối lượng chảy: ṁ = ρ A V.', 'Mass flow: ṁ = ρ A V.'));
      s.push(st(String.raw`\dot m_{max}=A\,P_0\sqrt{\frac{k}{RT_0}}\left(\frac{2}{k+1}\right)^{\frac{k+1}{2(k-1)}}=${n(o.mdotChoked, 5)}${U.kgs}`, 'Lưu lượng nghẹt tại họng (so sánh).', 'Choked flow at the throat (for comparison).'));
      rows.push(row('T0', '$T_0$', '$T_0$', o.T0, 'K'), row('P0', '$P_0$', '$P_0$', o.P0, 'kPa'), row('PcritP0', '$P^*/P_0$', '$P^*/P_0$', o.PcritP0, '–'), row('PbP0', '$P_b/P_0$', '$P_b/P_0$', o.PbP0, '–'),
        row('state', T('Trạng thái', 'State'), 'State', o.choked ? 1 : 0, '', o.choked ? T('NGHẸT', 'CHOKED') : T('không nghẹt', 'not choked')), row('Ma', '$Ma_e$', '$Ma_e$', o.Ma, '–'), row('Pe', '$P_e$', '$P_e$', o.Pe, 'kPa'), row('Te', '$T_e$', '$T_e$', o.Te, 'K'), row('rho', '$\\rho_e$', '$\\rho_e$', o.rho, 'kg/m³'), row('V', '$V_e$', '$V_e$', o.V, 'm/s'), row('mdot', '$\\dot m$', '$\\dot m$', o.mdot, 'kg/s'), row('mdotChoked', '$\\dot m_{max}$', '$\\dot m_{max}$', o.mdotChoked, 'kg/s'));
      return { rows: rows, steps: s, raw: o };
    } };

  /* ---------- 5. Combustion ---------- */
  function formula(a, b, c, d) { function p(sym, x) { return x === 0 ? '' : sym + (x === 1 ? '' : '_{' + n(x) + '}'); } return p('C', a) + p('H', b) + p('O', c) + p('N', d); }
  var cComb = { id: 'comb', fields: [
    { k: 'a', vi: 'Số nguyên tử C (a)', en: 'Carbon atoms (a)', u: '–', ph: 8, min: 0 }, { k: 'b', vi: 'Số nguyên tử H (b)', en: 'Hydrogen atoms (b)', u: '–', ph: 18, min: 0 },
    { k: 'c', vi: 'Số nguyên tử O (c)', en: 'Oxygen atoms (c)', u: '–', def: 0, min: 0 }, { k: 'd', vi: 'Số nguyên tử N (d)', en: 'Nitrogen atoms (d)', u: '–', def: 0, min: 0 },
    { k: 'excess', vi: 'Không khí thừa (0 = đủ, lý thuyết)', en: 'Excess air (0 = stoichiometric)', u: '%', def: 0, min: 0, msg: ['Không khí thừa phải ≥ 0 (hỗn hợp giàu: CHƯA LÀM).', 'Excess air must be ≥ 0 (rich mixtures: NOT DONE).'] },
    { k: 'Pprod', vi: 'Áp suất sản phẩm (để tính áp suất riêng phần hơi nước)', en: 'Product pressure (for the partial pressure of water vapour)', u: 'kPa', def: 100, minx: 0 } ],
    run: function (v) {
      var D376 = vi ? '3{,}76' : '3.76', D476 = vi ? '4{,}76' : '4.76', o = TH.combustion(v), s = [], rows = [], lam = o.lambda, f = formula(o.a, o.b, o.c, o.d), xs = n(o.nO2);
      s.push(st(String.raw`${f}+${xs}\,(\mathrm{O_2}+${D376}\,\mathrm{N_2})\;\to\;${n(o.co2)}\,\mathrm{CO_2}+${n(o.h2o)}\,\mathrm{H_2O}+${n(o.o2)}\,\mathrm{O_2}+${n(o.n2)}\,\mathrm{N_2}`, 'Phản ứng với không khí (3,76 N₂ cho mỗi O₂).', 'Reaction with air (3.76 N₂ per O₂).'));
      s.push(st(String.raw`a_{th}=a+\frac{b}{4}-\frac{c}{2}=${n(o.a)}+\frac{${n(o.b)}}{4}-\frac{${n(o.c)}}{2}=${n(o.ath)}\ \mathrm{kmol\ O_2/kmol\ fuel}`, 'Cân bằng oxy khi cháy hoàn toàn thành CO₂ và H₂O.', 'Oxygen balance for complete combustion to CO₂ and H₂O.'));
      s.push(st(String.raw`x=\left(1+\frac{${n(o.excess)}}{100}\right)a_{th}=${n(lam, 5)}\cdot ${n(o.ath)}=${n(o.nO2)}`, 'x = lượng O₂ cấp thực tế (kmol/kmol nhiên liệu).', 'x = actual O₂ supplied (kmol/kmol fuel).'));
      s.push(st(String.raw`\mathrm{CO_2}:\ ${n(o.co2)};\quad \mathrm{H_2O}:\ \frac{b}{2}=${n(o.h2o)};\quad \mathrm{O_2}:\ (\lambda-1)a_{th}=${n(o.o2)};\quad \mathrm{N_2}:\ ${D376}x+\frac{d}{2}=${n(o.n2)}`, 'Cân bằng C, H, O, N từng nguyên tố.', 'Element balances for C, H, O, N.'));
      s.push(st(String.raw`M_f=${n(ATOM.C)}\,a+${n(ATOM.H)}\,b+${n(ATOM.O)}\,c+${n(ATOM.N)}\,d=${n(o.Mf, 6)}\,\mathrm{kg/kmol}`, 'Nguyên tử khối: Appendix 1 (C từ Table A-27; H, O, N bằng một nửa khối lượng mol phân tử trong Table A-1).', 'Atomic masses: Appendix 1 (C from Table A-27; H, O, N are half the molecular masses in Table A-1).'));
      s.push(st(String.raw`AF_{mol}=${D476}\,x=${n(o.AFmol, 5)}\ \tfrac{\mathrm{kmol\ air}}{\mathrm{kmol\ fuel}},\qquad AF=\frac{${D476}\,x\,M_{air}}{M_f}=\frac{${n(o.AFmol, 5)}\cdot ${n(o.Mair)}}{${n(o.Mf, 6)}}=${n(o.AFmass, 5)}\ \tfrac{\mathrm{kg\ air}}{\mathrm{kg\ fuel}}`, 'M_không khí = 28,97 kg/kmol (Appendix 1 Table A-1).', 'M_air = 28.97 kg/kmol (Appendix 1 Table A-1).'));
      s.push(st(String.raw`N_{prod}=${n(o.tot, 5)}\,\mathrm{kmol},\qquad y_{\mathrm{H_2O}}=\frac{${n(o.h2o)}}{${n(o.tot, 5)}}=${n(o.y.h2o, 5)},\qquad P_v=y_{\mathrm{H_2O}}P=${n(o.Pv, 5)}${U.kPa}`, 'Áp suất riêng phần của hơi nước (chưa tính điểm sương, xem thẻ CHƯA LÀM).', 'Partial pressure of the water vapour (no dew point yet, see the NOT DONE card).'));
      rows.push(sec('Hệ số cân bằng (kmol / kmol nhiên liệu)', 'Balance coefficients (kmol / kmol fuel)'), row('co2', '$\\mathrm{CO_2}$', '$\\mathrm{CO_2}$', o.co2, 'kmol'), row('h2o', '$\\mathrm{H_2O}$', '$\\mathrm{H_2O}$', o.h2o, 'kmol'), row('n2', '$\\mathrm{N_2}$', '$\\mathrm{N_2}$', o.n2, 'kmol'), row('o2', '$\\mathrm{O_2}$', '$\\mathrm{O_2}$', o.o2, 'kmol'),
        row('ath', '$a_{th}$ (' + T('O₂ lý thuyết', 'theoretical O₂') + ')', '$a_{th}$ (theoretical O₂)', o.ath, 'kmol'), row('nO2', '$x$ (' + T('O₂ thực cấp', 'actual O₂') + ')', '$x$ (actual O₂)', o.nO2, 'kmol'), row('tot', '$N_{prod}$', '$N_{prod}$', o.tot, 'kmol'),
        sec('Tỉ lệ không khí–nhiên liệu', 'Air–fuel ratio'), row('AFmass', '$AF$ (' + T('theo khối lượng', 'mass basis') + ')', '$AF$ (mass basis)', o.AFmass, 'kg/kg'), row('AFmol', '$AF$ (' + T('theo kmol', 'mole basis') + ')', '$AF$ (mole basis)', o.AFmol, 'kmol/kmol'), row('AFth', '$AF_{th}$ (' + T('lý thuyết, khối lượng', 'stoichiometric, mass') + ')', '$AF_{th}$ (stoichiometric, mass)', o.AFth, 'kg/kg'), row('Mf', '$M_f$', '$M_f$', o.Mf, 'kg/kmol'),
        sec('Phần mol sản phẩm', 'Product mole fractions'), row('yco2', '$y_{\\mathrm{CO_2}}$', '$y_{\\mathrm{CO_2}}$', o.y.co2, '–'), row('yh2o', '$y_{\\mathrm{H_2O}}$', '$y_{\\mathrm{H_2O}}$', o.y.h2o, '–'), row('yn2', '$y_{\\mathrm{N_2}}$', '$y_{\\mathrm{N_2}}$', o.y.n2, '–'), row('yo2', '$y_{\\mathrm{O_2}}$', '$y_{\\mathrm{O_2}}$', o.y.o2, '–'), row('Pv', '$P_v$', '$P_v$', o.Pv, 'kPa'));
      o.yco2 = o.y.co2; o.yh2o = o.y.h2o; o.yn2 = o.y.n2; o.yo2 = o.y.o2;
      return { rows: rows, steps: s, raw: o };
    } };
  var ATOM = TH.consts.ATOM;

  /* ---------- mount ---------- */
  var specs = [cOtto, cDiesel, cBray, cMa, cAas, cPr, cStag, cCrit, cNoz, cComb];
  specs.forEach(function (sp) { var host = document.querySelector('[data-calc="' + sp.id + '"]'); if (host) new Calc(host, sp); });
})();
