/* Node test of _shared/thermo.js against data/lab_expected.json (written by build/verify/verify_lab.py).
   Run: node tests/lab_node_test.js   (env THERMO_PATH = another thermo.js, used by the mutation test of verify_lab.py)
   Three groups: cases = independent expectations (numpy/scipy/sympy), refs = reference values of the checked sources, examples = the worked examples of the Lab page
   (inputs of the page run through thermo.js, compared with the reference values shown beside them). Exit code 1 and a FAILS line on any miss. */
const fs = require('fs'), path = require('path');
const TH = require(process.env.THERMO_PATH || path.join(__dirname, '..', '_shared', 'thermo.js'));
const EXP = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'lab_expected.json'), 'utf8'));
const get = (o, k) => k === '' ? o : k.split('.').reduce((a, b) => a == null ? a : a[b], o);

/* same adapters as _shared/lab.js (what the page computes for each calculator) */
function labRun(calc, a) {
  switch (calc) {
    case 'otto': return TH.otto(a);
    case 'diesel': return TH.diesel(a);
    case 'brayton': { const o = TH.brayton(a); o.rpOpt = TH.braytonOptRp(a).rp; if (o.eps > 0) o.rpCross = TH.regenCrossover(a); return o; }
    case 'flow_ma': return TH.fromMa(a.Ma, a.k);
    case 'flow_aas': { const p = { k: a.k, branch: a.branch, A2A1: a.mode === 'A1s' ? 1 : a.A2A1, T1: a.T1, P1: a.P1 }; if (a.mode === 'Ma1') p.Ma1 = a.Ma1; else p.A1s = a.A1s; return TH.duct(p); }
    case 'flow_pr': { const p = { k: a.k, R: a.R, T0: a.T0, P0: a.P0, mdot: a.mdot }; if (a.mode === 'abs') p.P = a.P; else p.PP0 = a.PP0; const o = TH.fromPratio(p); if (o.A !== undefined) o.A_cm2 = o.A * 1e4; return o; }
    case 'flow_stag': return TH.stagnation(a);
    case 'flow_crit': { const c = TH.critical({ k: a.k }); return Object.assign({}, c, { mdot: TH.chokedMdot(a), Tstar: a.T0 * c.TsT0, Pstar: a.P0 * c.PsP0 }); }
    case 'flow_noz': return TH.convergingNozzle(a);
    case 'comb': return TH.combustion(a);
  }
  throw new Error('unknown calc ' + calc);
}

const fails = [], rows = []; let n = 0, maxRel = { v: 0, id: '' }, maxRefDev = { v: 0, id: '' };
function check(group, id, key, got, want, tol, src) {
  n++; const dev = Math.abs(got - want), ok = isFinite(got) && dev <= tol + 1e-15;
  const rel = dev / Math.max(Math.abs(want), 1e-12);
  if (group === 'cases' && ok && rel > maxRel.v) maxRel = { v: rel, id: id + ':' + key };
  if (group !== 'cases' && ok) { const rr = dev / Math.max(tol, 1e-12); if (rr > maxRefDev.v) maxRefDev = { v: rr, id: id + ':' + key }; }
  rows.push([group, id, key, want, got, dev, tol, ok]);
  if (!ok) fails.push(`${group}/${id}/${key || '(value)'}: got ${got}, want ${want} +/- ${tol}`);
}
function call(c) {
  if (c.argv) return TH[c.fn](...c.argv);
  return TH[c.fn](c.args);
}
for (const grp of ['cases', 'refs']) for (const c of EXP[grp]) {
  let out; try { out = call(c); } catch (e) { fails.push(`${grp}/${c.id}: threw ${e.message}`); continue; }
  for (const [k, [v, tol]] of Object.entries(c.expect)) check(grp, c.id, k, +get(out, k), v, tol);
}
for (const ex of EXP.examples) {
  let out; try { out = labRun(ex.calc, ex.args); } catch (e) { fails.push(`examples/${ex.id}: threw ${e.message}`); continue; }
  for (const r of ex.refs) check('examples', ex.id, r.key, +get(out, r.key), r.v, r.tol);
}
const cnt = g => rows.filter(r => r[0] === g).length, bad = g => rows.filter(r => r[0] === g && !r[7]).length;
console.log('group      checks  failed');
for (const g of ['cases', 'refs', 'examples']) console.log(g.padEnd(10), String(cnt(g)).padStart(6), String(bad(g)).padStart(7));
console.log(`total checks: ${n}; cases ${EXP.cases.length}, refs ${EXP.refs.length}, examples ${EXP.examples.length}`);
console.log(`largest relative deviation from the independent route: ${maxRel.v.toExponential(2)} at ${maxRel.id}`);
console.log(`largest deviation from a source reference, as a fraction of its tolerance: ${maxRefDev.v.toFixed(3)} at ${maxRefDev.id}`);
if (process.env.LAB_TABLE) for (const r of rows) console.log(r[0].padEnd(9), String(r[1]).padEnd(28), String(r[2]).padEnd(10), String(r[3]).padStart(14), String(r[4]).padStart(14), r[5].toExponential(1).padStart(9), r[6].toExponential(1).padStart(9), r[7] ? 'ok' : 'FAIL');
if (fails.length) { console.log(fails.slice(0, 60).join('\n')); console.log(`FAILS: ${fails.length}`); process.exit(1); }
console.log('FAILS: none');
