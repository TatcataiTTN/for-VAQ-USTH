// Node: moi ham tra cua _shared/props.js so voi build/props/props.py (tests/props_cases.json do gen_cases.py sinh)
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const P = require(path.join(root, '_shared', 'props.js'));
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'props_cases.json'), 'utf8'));
let fails = 0, n = 0;
function near(a, b, tol) { return Math.abs(a - b) <= tol * Math.max(1, Math.abs(b)); }
function cmpRes(c, r, e) {
  const bad = [];
  if (!near(r.value, e.value, 1e-12)) bad.push('value ' + r.value + ' vs ' + e.value);
  for (const k of ['unit', 'table', 'pdf_page', 'printed_page', 'method', 'suspect']) if (r[k] !== e[k]) bad.push(k + ' ' + r[k] + ' vs ' + e[k]);
  if (JSON.stringify(r.pdf_pages) !== JSON.stringify(e.pdf_pages)) bad.push('pdf_pages');
  if (r.rows_used.length !== e.rows_used.length) bad.push('rows_used length');
  else r.rows_used.forEach((u, i) => {
    const w = e.rows_used[i];
    if (JSON.stringify(Object.keys(u.key)) !== JSON.stringify(Object.keys(w.key)) || Object.values(u.key).some((v, j) => { const q = Object.values(w.key)[j]; return typeof q === 'string' ? v !== q : !near(v, q, 1e-12); })) bad.push('rows_used key ' + i);
    if (u.pdf_page !== w.pdf_page) bad.push('rows_used page ' + i);
    for (const k of Object.keys(w.cells)) if (!near(u.cells[k], w.cells[k], 1e-12)) bad.push('cell ' + k);
  });
  if (e.extra) for (const k of Object.keys(e.extra)) if (!near(r.extra[k], e.extra[k], 1e-12)) bad.push('extra ' + k);
  if (typeof r.note !== typeof e.note) bad.push('note type');
  if (r.note !== e.note) bad.push('note text: ' + JSON.stringify(r.note).slice(0, 80) + ' vs ' + JSON.stringify(e.note).slice(0, 80));
  return bad;
}
P.load(P.nodeLoader(path.join(root, 'data', 'props'))).then(() => {
  for (const c of cases) {
    n++; P.setLang(c.lang || 'vi');
    let r = null, err = null;
    try { r = P[c.fn](...c.args); } catch (x) { err = x; }
    if (c.ok) {
      if (err) { fails++; console.log('FAIL', c.fn, JSON.stringify(c.args), 'JS error', err.message); continue; }
      const bad = cmpRes(c, r, c.result);
      if (bad.length) { fails++; console.log('FAIL', c.fn, JSON.stringify(c.args), bad.join('; ')); }
    } else {
      if (!err || err.name !== 'PropsRangeError') { fails++; console.log('FAIL (expected range error)', c.fn, JSON.stringify(c.args), err && err.message); }
      else if (err.message !== c.error) { fails++; console.log('FAIL msg', c.fn, JSON.stringify(c.args), '\n   js:', err.message, '\n   py:', c.error); }
    }
  }
  console.log(n + ' cases, ' + fails + ' failures');
  console.log(fails ? 'FAILS: ' + fails : 'FAILS: none');
  process.exit(fails ? 1 : 0);
});
