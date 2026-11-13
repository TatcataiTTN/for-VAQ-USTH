/* Props: tra bang thuoc tinh Appendix 1 (Cengel). Cung thuat toan voi build/props/props.py.
   Dung duoc trong trinh duyet va Node:  Props.load(loader).then(()=>Props.sat_T('water',100,'hg'))
   loader(name) -> Promise<json> ; Props.fetchLoader(baseUrl) hoac Props.nodeLoader(dir).
   Moi lan tra: {value, unit, table, pdf_page, printed_page, pdf_pages, rows_used, method, suspect, note}.
   Noi suy tuyen tinh theo bien in cua bang; khong ngoai suy (nem PropsRangeError). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Props = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var EPS = 1e-9;
  function N(x) { return (typeof x === 'number') ? String(+x.toPrecision(12)) : String(x); }
  var db = {};
  var LANG = 'vi';
  function setLang(l) { LANG = (l === 'en') ? 'en' : 'vi'; }
  function m(key, kw) {
    var t = T_('messages')[key][LANG];
    return t.replace(/\{(\w+)\}/g, function (_, k) { return N(kw[k]); });
  }
  function PropsRangeError(msg) { var e = new Error(msg); e.name = 'PropsRangeError'; return e; }
  var NAMES = ['A1', 'A2a', 'A2b', 'A2c', 'A4', 'A5', 'A6', 'A7', 'A11', 'A12', 'A13', 'A17', 'A17E', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A32', 'book_errata', 'messages'];

  function load(loader, names) {
    var want = names || NAMES;
    return Promise.all(want.map(function (n) {
      if (db[n]) return Promise.resolve();
      return Promise.resolve(loader(n)).then(function (j) { db[n] = j; });
    }));
  }
  function fetchLoader(base) {
    return function (n) { return fetch(base + n + '.json').then(function (r) { if (!r.ok) throw new Error(n + ' ' + r.status); return r.json(); }); };
  }
  function nodeLoader(dir) {
    return function (n) {
      var fs = require('fs'), path = require('path');
      return Promise.resolve(JSON.parse(fs.readFileSync(path.join(dir, n + '.json'), 'utf8')));
    };
  }
  function T_(n) { if (!db[n]) throw new Error('chưa nạp bảng ' + n + ' (gọi Props.load trước)'); return db[n]; }
  function errata() { return T_('book_errata').errors; }
  function firstVal(o) { for (var k in o) return o[k]; }
  function suspectOf(table, keyval, col) {
    var E = errata();
    for (var i = 0; i < E.length; i++) {
      var e = E[i];
      if (e.table === table && e.col === col) {
        var kv = firstVal(e.key);
        if (typeof kv === 'number' && typeof keyval === 'number' && Math.abs(kv - keyval) < EPS) return e;
      }
    }
    return null;
  }
  function noteOf(es) {
    return es.map(function (e) {
      var tag = e.kind !== 'systematic_offset' ? m('err_tag', {}) : m('err_sys_tag', {});
      var how = (LANG === 'en' && e.how_en) ? e.how_en : e.how;
      return m('err_fmt', { tag: tag, col: e.col, key: firstVal(e.key), printed: e.printed, expected: e.expected, how: how });
    }).join(' | ');
  }
  function uniqSort(a) { var s = {}; a.forEach(function (x) { s[x] = 1; }); return Object.keys(s).map(Number).sort(function (x, y) { return x - y; }); }
  function res(value, table, pages, rows_used, method, unit, es, note) {
    pages = uniqSort(pages);
    var n = noteOf(es || []);
    var nt = [note || '', n].filter(function (x) { return x; }).join(' | ');
    return { value: value, unit: unit, table: table, pdf_page: pages[0], printed_page: pages[0] + 908, pdf_pages: pages,
      rows_used: rows_used, method: method, suspect: (es || []).length > 0, note: nt };
  }
  function bracket(xs, x, what) {
    var lo = xs[0], hi = xs[xs.length - 1];
    if (x < lo - EPS || x > hi + EPS) throw PropsRangeError(m('range_out', { what: what, x: x, lo: lo, hi: hi }));
    var i;
    for (i = 0; i < xs.length; i++) if (Math.abs(xs[i] - x) < EPS) return [i, i, 0];
    for (i = 0; i < xs.length - 1; i++) if (xs[i] < x && x < xs[i + 1]) return [i, i + 1, (x - xs[i]) / (xs[i + 1] - xs[i])];
    throw PropsRangeError(m('no_interval', { what: what, x: x }));
  }
  function bracketDec(xs, x, what) { return bracket(xs.map(function (v) { return -v; }), -x, what); }
  function unit(t, col) { return (t.units && t.units[col]) || ''; }
  function uniqInts(a, b) { return a === b ? [a] : [a, b]; }

  function lookupFlat(fname, idxcol, x, prop, note) {
    var t = T_(fname), cols = t.columns, ic = cols.indexOf(idxcol), pc = cols.indexOf(prop);
    var rows = t.rows.filter(function (r) { return r[ic] !== null; });
    var xs = rows.map(function (r) { return r[ic]; });
    var b = bracket(xs, x, idxcol), i = b[0], j = b[1], f = b[2];
    var used = [], es = [], pgs = [];
    uniqInts(i, j).forEach(function (k) {
      var pg = t.row_pages ? t.row_pages[t.rows.indexOf(rows[k])] : t.pdf_pages[0];
      pgs.push(pg);
      var key = {}; key[idxcol] = rows[k][ic];
      var cells = {}; cells[prop] = rows[k][pc];
      used.push({ key: key, pdf_page: pg, cells: cells });
      var e = suspectOf(t.table, rows[k][ic], prop); if (e) es.push(e);
    });
    var v, m;
    if (i === j) { v = rows[i][pc]; m = 'exact'; } else { v = rows[i][pc] + f * (rows[j][pc] - rows[i][pc]); m = 'linear'; }
    return res(v, t.table, pgs, used, m, unit(t, prop), es, note || '');
  }
  var SAT_T = { water: 'A4', R134a: 'A11' }, SAT_P = { water: 'A5', R134a: 'A12' };
  function sat_T(sub, T, prop) { return lookupFlat(SAT_T[sub], 'T_C', T, prop); }
  function sat_P(sub, P, prop) { return lookupFlat(SAT_P[sub], 'Psat_kPa', P, prop); }
  function wet(sub, by, val, x, prop) {
    if (!(x >= 0 && x <= 1)) throw PropsRangeError(m('q_range', {}));
    var fn = by === 'T' ? sat_T : sat_P;
    var a = fn(sub, val, prop === 'v' ? 'vf' : prop + 'f'), b = fn(sub, val, prop === 'v' ? 'vg' : prop + 'g');
    var r = JSON.parse(JSON.stringify(a));
    r.value = a.value + x * (b.value - a.value);
    r.rows_used = a.rows_used.concat(b.rows_used);
    r.suspect = a.suspect || b.suspect;
    r.method = a.method === 'exact' ? 'exact' : 'linear';
    r.note = m('wet_note', { prop: prop, x: x }) + (a.note || '') + (b.note !== a.note ? b.note : '');
    r.pdf_pages = uniqSort(a.pdf_pages.concat(b.pdf_pages)); r.pdf_page = r.pdf_pages[0]; r.printed_page = r.pdf_page + 908;
    return r;
  }
  function wet_T(sub, T, x, prop) { return wet(sub, 'T', T, x, prop); }
  function wet_P(sub, P, x, prop) { return wet(sub, 'P', P, x, prop); }
  function quality(sub, by, val, prop, y) {
    var fn = by === 'T' ? sat_T : sat_P;
    var a = fn(sub, val, prop === 'v' ? 'vf' : prop + 'f'), b = fn(sub, val, prop === 'v' ? 'vg' : prop + 'g');
    var x = (y - a.value) / (b.value - a.value);
    var r = JSON.parse(JSON.stringify(a));
    r.value = x; r.unit = '-'; r.rows_used = a.rows_used.concat(b.rows_used); r.suspect = a.suspect || b.suspect;
    r.note = m('q_note', {}) + ((x >= 0 && x <= 1) ? '' : m('q_warn', { x: x.toFixed(4) }));
    return r;
  }

  var BLK = { water: 'A6', R134a: 'A13', compressed: 'A7' };
  function blockPoints(b) {
    var pts = b.rows.map(function (r) { return r.slice(); });
    var sat0 = (b.sat !== null && b.param.Tsat_C !== null) ? 1 : 0;
    if (sat0) pts.unshift([b.param.Tsat_C].concat(b.sat));
    return [pts, sat0];
  }
  function blockInterp(t, b, T, prop, pc) {
    var pp = blockPoints(b), pts = pp[0], sat0 = pp[1];
    var xs = pts.map(function (p) { return p[0]; });
    var br;
    try { br = bracket(xs, T, 'T'); } catch (e) {
      throw PropsRangeError(m('blk_T_out', { T: T, P: b.param.P_MPa, lo: xs[0], hi: xs[xs.length - 1] }));
    }
    var i = br[0], j = br[1], f = br[2], es = [], used = [];
    uniqInts(i, j).forEach(function (k) {
      var key = { P_MPa: b.param.P_MPa, T_C: xs[k] }, cells = {}; cells[prop] = pts[k][pc];
      used.push({ key: key, pdf_page: b.pdf_page, sat_row: (sat0 === 1 && k === 0), cells: cells });
      var e = suspectOf(t.table, xs[k], prop);
      if (e && Math.abs((e.key.P_MPa !== undefined ? e.key.P_MPa : b.param.P_MPa) - b.param.P_MPa) < EPS) es.push(e);
    });
    var v = i === j ? pts[i][pc] : pts[i][pc] + f * (pts[j][pc] - pts[i][pc]);
    return [v, used, es, i === j];
  }
  function blockLookup(kind, P, T, prop) {
    var t = T_(BLK[kind]), pc = t.columns.indexOf(prop);
    if (prop === 'T_C') throw PropsRangeError(m('T_input', {}));
    var Ps = t.blocks.map(function (b) { return b.param.P_MPa; });
    var br = bracket(Ps, P, 'P (MPa)'), i = br[0], j = br[1], f = br[2];
    var a = blockInterp(t, t.blocks[i], T, prop, pc);
    var pgs = [t.blocks[i].pdf_page];
    if (i === j) return res(a[0], t.table, pgs, a[1], a[3] ? 'exact' : 'linear', unit(t, prop), a[2], a[3] ? '' : m('blk_lin', { P: Ps[i] }));
    var c;
    try { c = blockInterp(t, t.blocks[j], T, prop, pc); } catch (e) {
      throw PropsRangeError(m('blk_between', { P: P, P1: Ps[i], P2: Ps[j], T: T, why: e.message }));
    }
    var v = a[0] + f * (c[0] - a[0]);
    pgs.push(t.blocks[j].pdf_page);
    return res(v, t.table, pgs, a[1].concat(c[1]), 'bilinear', unit(t, prop), a[2].concat(c[2]),
      m('blk_bi', { P1: Ps[i], P2: Ps[j], f: f.toFixed(4) }) + (prop === 'v' ? ' | ' + m('blk_v_warn', {}) : ''));
  }
  function blockInv(t, b, prop, value) {
    var pc = t.columns.indexOf(prop), pp = blockPoints(b), pts = pp[0], sat0 = pp[1];
    var ys = pts.map(function (p) { return p[pc]; }), br;
    try { br = bracket(ys, value, prop); } catch (e) {
      throw PropsRangeError(m('inv_out_block', { prop: prop, value: value, P: b.param.P_MPa, lo: ys[0], hi: ys[ys.length - 1] }));
    }
    var i = br[0], j = br[1], f = br[2], out = {};
    t.columns.forEach(function (c, k) { out[c] = i === j ? pts[i][k] : pts[i][k] + f * (pts[j][k] - pts[i][k]); });
    var used = [], es = [];
    uniqInts(i, j).forEach(function (k) {
      var cells = {}; cells[prop] = pts[k][pc];
      used.push({ key: { P_MPa: b.param.P_MPa, T_C: pts[k][0] }, pdf_page: b.pdf_page, sat_row: (sat0 === 1 && k === 0), cells: cells });
      var e = suspectOf(t.table, pts[k][0], prop);
      if (e && Math.abs((e.key.P_MPa !== undefined ? e.key.P_MPa : b.param.P_MPa) - b.param.P_MPa) < EPS) es.push(e);
    });
    return [out, used, es, i === j];
  }
  function block_inverse(kind, P, prop, value) {
    var t = T_(BLK[kind]);
    var Ps = t.blocks.map(function (b) { return b.param.P_MPa; });
    var br = bracket(Ps, P, 'P (MPa)'), i = br[0], j = br[1], f = br[2];
    var a = blockInv(t, t.blocks[i], prop, value), pgs = [t.blocks[i].pdf_page], r;
    if (i === j) {
      r = res(a[0].T_C, t.table, pgs, a[1], a[3] ? 'exact' : 'linear', '°C', a[2], m('inv_note_block', { prop: prop, value: value, P: Ps[i] }));
      r.extra = a[0]; return r;
    }
    var b2 = blockInv(t, t.blocks[j], prop, value);
    pgs.push(t.blocks[j].pdf_page);
    var out = {}; Object.keys(a[0]).forEach(function (c) { out[c] = a[0][c] + f * (b2[0][c] - a[0][c]); });
    r = res(out.T_C, t.table, pgs, a[1].concat(b2[1]), 'bilinear', '°C', a[2].concat(b2[2]),
      m('inv_note_bi', { prop: prop, value: value, P1: Ps[i], P2: Ps[j], f: f.toFixed(4) }));
    r.extra = out; return r;
  }
  function superheated_inverse(sub, P, prop, value) { return block_inverse(sub, P, prop, value); }

  function superheated(sub, P, T, prop) { return blockLookup(sub, P, T, prop); }
  function compressed(P, T, prop) { return blockLookup('compressed', P, T, prop); }
  function compressed_approx(T, prop) {
    var col = { v: 'vf', u: 'uf', h: 'hf', s: 'sf' }[prop];
    var r = sat_T('water', T, col);
    r.note = m('comp_approx', {}) + (r.note ? ' | ' + r.note : '');
    return r;
  }

  function air(T, prop, system) {
    var s = system || 'SI';
    return lookupFlat(s === 'SI' ? 'A17' : 'A17E', s === 'SI' ? 'T_K' : 'T_R', T, prop);
  }
  function air_inverse(prop, value, system) {
    var s = system || 'SI', f = s === 'SI' ? 'A17' : 'A17E', ic = s === 'SI' ? 'T_K' : 'T_R';
    var t = T_(f), cols = t.columns, pc = cols.indexOf(prop), rows = t.rows;
    var ys = rows.map(function (r) { return r[pc]; });
    var dec = ys[0] > ys[ys.length - 1];
    var br = (dec ? bracketDec : bracket)(ys, value, prop), i = br[0], j = br[1], fr = br[2];
    var T = i === j ? rows[i][0] : rows[i][0] + fr * (rows[j][0] - rows[i][0]);
    var used = [], es = [], pgs = [];
    uniqInts(i, j).forEach(function (k) {
      var key = {}; key[cols[0]] = rows[k][0]; var cells = {}; cells[prop] = rows[k][pc];
      used.push({ key: key, pdf_page: t.row_pages[k], cells: cells }); pgs.push(t.row_pages[k]);
      var e = suspectOf(t.table, rows[k][0], prop); if (e) es.push(e);
    });
    var extra = {};
    cols.slice(1).forEach(function (c) { var ci = cols.indexOf(c); extra[c] = i === j ? rows[i][ci] : rows[i][ci] + fr * (rows[j][ci] - rows[i][ci]); });
    var r = res(T, t.table, pgs, used, i === j ? 'exact' : 'linear', t.units[ic], es, m('inv_note', { prop: prop, value: value }));
    r.extra = extra; return r;
  }
  var GAS = { N2: 'A18', O2: 'A19', CO2: 'A20', CO: 'A21', H2: 'A22', H2O: 'A23', O: 'A24', OH: 'A25' };
  function gas_kmol(gas, T, prop) { return lookupFlat(GAS[gas], 'T_K', T, prop); }
  function gas_kmol_inverse(gas, prop, value) {
    var t = T_(GAS[gas]), cols = t.columns, pc = cols.indexOf(prop);
    var rows = t.rows.filter(function (r) { return r[0] !== 0; });
    var ys = rows.map(function (r) { return r[pc]; });
    var br = bracket(ys, value, prop), i = br[0], j = br[1], fr = br[2];
    var T = i === j ? rows[i][0] : rows[i][0] + fr * (rows[j][0] - rows[i][0]);
    var used = [], es = [];
    uniqInts(i, j).forEach(function (k) {
      var cells = {}; cells[prop] = rows[k][pc];
      used.push({ key: { T_K: rows[k][0] }, pdf_page: t.row_pages[t.rows.indexOf(rows[k])], cells: cells });
      var e = suspectOf(t.table, rows[k][0], prop); if (e) es.push(e);
    });
    return res(T, t.table, used.map(function (u) { return u.pdf_page; }), used, i === j ? 'exact' : 'linear', 'K', es, m('inv_note_k', { prop: prop, value: value }));
  }

  function byName(fname, namecols, name, prop) {
    var t = T_(fname), cols = t.columns, pc = cols.indexOf(prop), nm = String(name).toLowerCase();
    var hit = t.rows.filter(function (r) { return namecols.some(function (c) { return String(r[cols.indexOf(c)]).toLowerCase() === nm; }); });
    if (!hit.length) hit = t.rows.filter(function (r) { return namecols.some(function (c) { return String(r[cols.indexOf(c)]).toLowerCase().indexOf(nm) >= 0; }); });
    if (hit.length !== 1) throw PropsRangeError(m('no_match', { name: name, n: hit.length, table: t.table }));
    var r = hit[0], pg = t.pdf_pages[0], key = {}, cells = {}; key[namecols[0]] = r[cols.indexOf(namecols[0])]; cells[prop] = r[pc];
    return res(r[pc], t.table, [pg], [{ key: key, pdf_page: pg, cells: cells }], 'exact', unit(t, prop), []);
  }
  function critical(sub, prop) { return byName('A1', ['substance', 'formula'], sub, prop); }
  function cp_300(gas, prop) {
    var r = byName('A2a', ['gas', 'formula'], gas, prop);
    var ex = errata().filter(function (e) { return e.table === 'A-2a' && e.col === prop && String(e.key.gas || '').toLowerCase().indexOf(String(gas).toLowerCase()) >= 0; });
    if (ex.length) { r.suspect = true; r.note = noteOf(ex); }
    return r;
  }
  function cp_T(gas, T, prop) {
    var t = T_('A2b'), cols = t.columns, pc = cols.indexOf(prop);
    var rows = t.rows.filter(function (r) { return r[0] === gas; });
    if (!rows.length) throw PropsRangeError(m('no_gas', { gas: gas }));
    var br = bracket(rows.map(function (r) { return r[1]; }), T, 'T (K)'), i = br[0], j = br[1], f = br[2];
    var used = uniqInts(i, j).map(function (k) { var cells = {}; cells[prop] = rows[k][pc]; return { key: { gas: gas, T_K: rows[k][1] }, pdf_page: 4, cells: cells }; });
    var v = i === j ? rows[i][pc] : rows[i][pc] + f * (rows[j][pc] - rows[i][pc]);
    return res(v, t.table, [4], used, i === j ? 'exact' : 'linear', unit(t, prop), []);
  }
  function cp_poly(sub, T, mass) {
    var t = T_('A2c'), s = String(sub).toLowerCase();
    var hit = t.rows.filter(function (r) { return r[1].toLowerCase() === s || r[0].toLowerCase() === s; });
    if (hit.length !== 1) throw PropsRangeError(m('no_match', { name: sub, n: hit.length, table: 'A-2c' }));
    var r = hit[0], a = r[2], b = r[3], c = r[4], d = r[5], lo = r[6], hi = r[7];
    if (T < lo || T > hi) throw PropsRangeError(m('poly_out', { T: T, lo: lo, hi: hi, name: r[0] }));
    var cp = a + b * T + c * T * T + d * T * T * T, u = 'kJ/(kmol·K)';
    var note = m('poly_note', { emax: r[8], eavg: r[9] });
    if (mass) { var M = critical(r[0], 'M').value; cp = cp / M; u = 'kJ/(kg·K)'; note += m('poly_mass', { M: M }); }
    return { value: cp, unit: u, table: 'A-2c', pdf_page: 5, printed_page: 913, pdf_pages: [5],
      rows_used: [{ key: { substance: r[0] }, pdf_page: 5, cells: { a: a, b: b, c: c, d: d, Tmin: lo, Tmax: hi } }], method: 'polynomial', suspect: false, note: note };
  }
  function formation(name, prop) {
    var t = T_('A26'), pc = t.columns.indexOf(prop), n = String(name).toLowerCase();
    var hit = t.rows.filter(function (r) { return r[1].toLowerCase() === n; });
    if (hit.length !== 1) throw PropsRangeError(m('no_match_form', { name: name, n: hit.length }));
    var r = hit[0], cells = {}; cells[prop] = r[pc];
    return res(r[pc], 'A-26', [42], [{ key: { formula: r[1] }, pdf_page: 42, cells: cells }], 'exact', unit(t, prop), []);
  }
  function fuel(name, prop) {
    var t = T_('A27'), pc = t.columns.indexOf(prop), n = String(name).toLowerCase();
    var hit = t.rows.filter(function (r) { return r[1].toLowerCase() === n; });
    if (!hit.length) hit = t.rows.filter(function (r) { return r[0].toLowerCase().indexOf(n) >= 0; });
    if (hit.length !== 1) throw PropsRangeError(m('no_match', { name: name, n: hit.length, table: 'A-27' }));
    var r = hit[0], cells = {}; cells[prop] = r[pc];
    return res(r[pc], 'A-27', [43], [{ key: { fuel: r[0] }, pdf_page: 43, cells: cells }], 'exact', unit(t, prop), []);
  }
  function isentropic(Ma, prop) {
    var t = T_('A32'), pc = t.columns.indexOf(prop);
    var rows = t.rows.filter(function (r) { return r[0] !== null; });
    var br = bracket(rows.map(function (r) { return r[0]; }), Ma, 'Ma'), i = br[0], j = br[1], f = br[2];
    var used = [], es = [];
    uniqInts(i, j).forEach(function (k) {
      var cells = {}; cells[prop] = rows[k][pc];
      used.push({ key: { Ma: rows[k][0] }, pdf_page: 48, cells: cells });
      var e = suspectOf('A-32', rows[k][0], prop); if (e) es.push(e);
    });
    var a = rows[i][pc], b = rows[j][pc];
    if (a === null || b === null) throw PropsRangeError(m('iso_inf', {}));
    var v = i === j ? a : a + f * (b - a);
    return res(v, 'A-32', [48], used, i === j ? 'exact' : 'linear', unit(t, prop), es,
      m('iso_note', {}));
  }
  function isentropic_inverse(prop, value, branch) {
    branch = branch || 'sub';
    var t = T_('A32'), pc = t.columns.indexOf(prop);
    var rows = t.rows.filter(function (r) { return r[0] !== null && r[pc] !== null; });
    if (prop === 'A_Astar') rows = rows.filter(function (r) { return (branch === 'sub' ? r[0] <= 1 : r[0] >= 1) && r[0] > 0; });
    var ys = rows.map(function (r) { return r[pc]; }), dec = ys[0] > ys[ys.length - 1];
    var br = (dec ? bracketDec : bracket)(ys, value, prop), i = br[0], j = br[1], fr = br[2];
    var Ma = i === j ? rows[i][0] : rows[i][0] + fr * (rows[j][0] - rows[i][0]);
    var used = uniqInts(i, j).map(function (k) { var cells = {}; cells[prop] = rows[k][pc]; return { key: { Ma: rows[k][0] }, pdf_page: 48, cells: cells }; });
    return res(Ma, 'A-32', [48], used, i === j ? 'exact' : 'linear', '-', [], m('iso_inv_note', { prop: prop, value: value }) + (prop === 'A_Astar' ? (branch === 'sub' ? m('iso_sub', {}) : m('iso_sup', {})) : ''));
  }
  function table(name) { return T_(name); }

  return { setLang: setLang, load: load, fetchLoader: fetchLoader, nodeLoader: nodeLoader, table: table, PropsRangeError: PropsRangeError,
    sat_T: sat_T, sat_P: sat_P, wet_T: wet_T, wet_P: wet_P, quality: quality, superheated: superheated, compressed: compressed,
    compressed_approx: compressed_approx, block_inverse: block_inverse, superheated_inverse: superheated_inverse, air: air, air_inverse: air_inverse, gas_kmol: gas_kmol, gas_kmol_inverse: gas_kmol_inverse,
    critical: critical, cp_300: cp_300, cp_T: cp_T, cp_poly: cp_poly, formation: formation, fuel: fuel,
    isentropic: isentropic, isentropic_inverse: isentropic_inverse, NAMES: NAMES };
});
