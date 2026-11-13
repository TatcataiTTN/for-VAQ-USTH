/* thermo.js: pure functions of the Lab (AE2.013 Thermal Systems). Works in the browser (window.Thermo) and in Node (module.exports).
   Units: T in K, P in kPa, specific energy in kJ/kg, R/cp/cv in kJ/(kg K), v in m3/kg, areas in m2, mass flow in kg/s, V in m/s.
   Model: ideal gas with constant k (air-standard / cold-air), no property tables (variable cp is NOT DONE: needs the property library P3).
   Errors are thrown as ThermoError with .code (a short key) and .data (numbers for the message); the UI translates them. */
(function (root) {
  'use strict';
  function ThermoError(code, data) { var e = new Error(code); e.name = 'ThermoError'; e.code = code; e.data = data || {}; return e; }
  function isNum(x) { return typeof x === 'number' && isFinite(x); }
  function has(x) { return x !== undefined && x !== null && x !== '' && !(typeof x === 'number' && isNaN(x)); }
  function need(p, key, cond, code) {
    if (!has(p[key]) || !isNum(p[key])) throw ThermoError('missing', { name: key });
    if (cond && !cond(p[key])) throw ThermoError(code || 'range', { name: key, value: p[key] });
    return p[key];
  }
  var pos = function (x) { return x > 0; };

  var R_AIR = 0.287, K_AIR = 1.4;            // Appendix 1 Table A-2 (a): air R = 0.2870 kJ/(kg K), k = 1.400 at 300 K
  var M_AIR = 28.97;                         // Appendix 1 Table A-1: air 28.97 kg/kmol
  var ATOM = { C: 12.011, H: 1.008, O: 15.999, N: 14.007 };   // see lab_body.py note: C from Table A-27; H,O,N = half of the molecular masses of Table A-1 (2.016, 31.999, 28.013)

  /* gas model: k from k, or cp/cv, or R and cv; heats use cp, cv when they are given (the slides do this in Tutorials I #2) */
  function gas(p) {
    var k = has(p.k) ? p.k : (has(p.cp) && has(p.cv)) ? p.cp / p.cv : K_AIR;
    if (!isNum(k) || k <= 1) throw ThermoError('range', { name: 'k', value: k });
    var R = has(p.R) ? p.R : (has(p.cp) && has(p.cv)) ? p.cp - p.cv : R_AIR;
    if (!(R > 0)) throw ThermoError('range', { name: 'R', value: R });
    var cv = has(p.cv) ? p.cv : R / (k - 1);
    var cp = has(p.cp) ? p.cp : k * cv;
    if (!(cv > 0) || !(cp > 0)) throw ThermoError('range', { name: has(p.cv) ? 'cv' : 'cp', value: 0 });
    var mixed = has(p.cp) && has(p.cv) && has(p.k) && Math.abs(p.cp / p.cv - p.k) > 1e-3;
    return { k: k, R: R, cv: cv, cp: cp, mixed: mixed, ratio: cp / cv };
  }
  function mass(p, g, T1, P1) { return has(p.V1) ? (need(p, 'V1', pos), p.V1 * P1 / (g.R * T1)) : null; }

  /* ---------------- 1. Otto ---------------- */
  function otto(p) {
    var r = need(p, 'r', function (x) { return x > 1; }), T1 = need(p, 'T1', pos), P1 = need(p, 'P1', pos);
    var g = gas(p), k = g.k, mode = p.mode || 'qin';
    var T2 = T1 * Math.pow(r, k - 1), P2 = P1 * Math.pow(r, k), T3;
    if (mode === 'T3') T3 = need(p, 'T3', pos);
    else if (mode === 'T4') T3 = need(p, 'T4', pos) * Math.pow(r, k - 1);
    else T3 = T2 + need(p, 'qin', pos) / g.cv;
    if (!(T3 > T2)) throw ThermoError('t3le2', { T2: T2, T3: T3 });
    var T4 = T3 * Math.pow(r, 1 - k), P3 = P2 * T3 / T2, P4 = P1 * T4 / T1;
    var qin = g.cv * (T3 - T2), qout = g.cv * (T4 - T1), wnet = qin - qout;
    var v1 = g.R * T1 / P1, v2 = v1 / r;
    var out = { r: r, k: k, R: g.R, cv: g.cv, cp: g.cp, mixed: g.mixed, T1: T1, T2: T2, T3: T3, T4: T4, P1: P1, P2: P2, P3: P3, P4: P4,
      qin: qin, qout: qout, wnet: wnet, eta: wnet / qin, etaOtto: 1 - Math.pow(r, 1 - k), v1: v1, v2: v2, mep: wnet / (v1 - v2) };
    var m = mass(p, g, T1, P1);
    if (m !== null) { out.m = m; out.Qin = m * qin; out.Qout = m * qout; out.Wnet = m * wnet; }
    return out;
  }

  /* ---------------- 2. Diesel ---------------- */
  function diesel(p) {
    var r = need(p, 'r', function (x) { return x > 1; }), T1 = need(p, 'T1', pos), P1 = need(p, 'P1', pos);
    var g = gas(p), k = g.k, mode = p.mode || 'rc';
    var T2 = T1 * Math.pow(r, k - 1), P2 = P1 * Math.pow(r, k), T3, rc;
    if (mode === 'T3') { T3 = need(p, 'T3', pos); rc = T3 / T2; }
    else if (mode === 'qin') { T3 = T2 + need(p, 'qin', pos) / g.cp; rc = T3 / T2; }
    else { rc = need(p, 'rc', function (x) { return x > 1; }); T3 = rc * T2; }
    if (!(rc > 1)) throw ThermoError('t3le2', { T2: T2, T3: T3 });
    if (!(rc < r)) throw ThermoError('rcge_r', { rc: rc, r: r });
    var T4 = T1 * Math.pow(rc, k), P4 = P1 * T4 / T1;
    var qin = g.cp * (T3 - T2), qout = g.cv * (T4 - T1), wnet = qin - qout;
    var v1 = g.R * T1 / P1, v2 = v1 / r;
    var out = { r: r, rc: rc, k: k, R: g.R, cv: g.cv, cp: g.cp, mixed: g.mixed, T1: T1, T2: T2, T3: T3, T4: T4, P1: P1, P2: P2, P3: P2, P4: P4,
      qin: qin, qout: qout, wnet: wnet, eta: wnet / qin, etaDiesel: dieselEta(r, rc, k), etaOtto: 1 - Math.pow(r, 1 - k),
      v1: v1, v2: v2, v3: rc * v2, mep: wnet / (v1 - v2) };
    var m = mass(p, g, T1, P1);
    if (m !== null) { out.m = m; out.Qin = m * qin; out.Qout = m * qout; out.Wnet = m * wnet; }
    return out;
  }
  function dieselEta(r, rc, k) { return 1 - (1 / Math.pow(r, k - 1)) * (Math.pow(rc, k) - 1) / (k * (rc - 1)); }

  /* ---------------- 3. Brayton ---------------- */
  /* Nc compressor stages with perfect intercooling back to T1, Nt turbine stages with reheat back to T3, equal pressure ratio rp^(1/N) per stage,
     isentropic efficiencies etac, etat, regenerator effectiveness eps = (T5 - Tc)/(Tt - Tc), Tc = last compressor exit, Tt = last turbine exit. */
  function brayton(p) {
    var rp = need(p, 'rp', function (x) { return x > 1; }), T1 = need(p, 'T1', pos), T3 = need(p, 'T3', pos);
    if (!(T3 > T1)) throw ThermoError('t3le1', { T1: T1, T3: T3 });
    var g = gas(p), k = g.k, cp = g.cp;
    var etac = has(p.etac) ? p.etac : 1, etat = has(p.etat) ? p.etat : 1, eps = has(p.eps) ? p.eps : 0;
    var Nc = has(p.Nc) ? p.Nc : 1, Nt = has(p.Nt) ? p.Nt : 1, P1 = has(p.P1) ? p.P1 : 100;
    if (!(etac > 0 && etac <= 1)) throw ThermoError('eff', { name: 'etac', value: etac });
    if (!(etat > 0 && etat <= 1)) throw ThermoError('eff', { name: 'etat', value: etat });
    if (!(eps >= 0 && eps <= 1)) throw ThermoError('eff', { name: 'eps', value: eps });
    if (!(Nc >= 1 && Nc <= 10 && Nc === Math.floor(Nc))) throw ThermoError('stages', { name: 'Nc', value: Nc });
    if (!(Nt >= 1 && Nt <= 10 && Nt === Math.floor(Nt))) throw ThermoError('stages', { name: 'Nt', value: Nt });
    var e = (k - 1) / k, prc = Math.pow(rp, 1 / Nc), prt = Math.pow(rp, 1 / Nt);
    var Tcs = T1 * Math.pow(prc, e), Tc = T1 + (Tcs - T1) / etac;                  // each compressor stage (inlet T1)
    var Tts = T3 / Math.pow(prt, e), Tt = T3 - etat * (T3 - Tts);                  // each turbine stage (inlet T3)
    var wc = Nc * cp * (Tc - T1), wt = Nt * cp * (T3 - Tt), wnet = wt - wc;
    var regenOK = Tt > Tc;
    if (eps > 0 && !regenOK) throw ThermoError('noregen', { Tc: Tc, Tt: Tt });
    var T5 = eps > 0 ? Tc + eps * (Tt - Tc) : Tc;                                   // cold side leaving the regenerator
    var T6 = eps > 0 ? Tt - (T5 - Tc) : Tt;                                         // hot side leaving the regenerator
    var qmain = cp * (T3 - T5), qreheat = (Nt - 1) * cp * (T3 - Tt), qin = qmain + qreheat;
    if (!(qin > 0)) throw ThermoError('noheat', {});
    var qout = qin - wnet;
    return { k: k, cp: cp, R: g.R, mixed: g.mixed, rp: rp, prc: prc, prt: prt, T1: T1, T3: T3, Tcs: Tcs, Tc: Tc, Tts: Tts, Tt: Tt, T5: T5, T6: T6,
      P1: P1, P2: P1 * rp, Pmid_c: P1 * prc, Pmid_t: P1 * rp / prt,
      wc: wc, wt: wt, wnet: wnet, bwr: wc / wt, qmain: qmain, qreheat: qreheat, qin: qin, qout: qout, eta: wnet / qin,
      etaIdeal: 1 - 1 / Math.pow(rp, e), Nc: Nc, Nt: Nt, etac: etac, etat: etat, eps: eps,
      qoutCheck: cp * (T6 - T1) + (Nc - 1) * cp * (Tc - T1) };
  }
  /* pressure ratio for maximum w_net. Closed form x = sqrt(etac etat T3/T1) with x = rp^((k-1)/k) when Nc = Nt (including 1); otherwise golden-section search */
  function braytonOptRp(p) {
    var T1 = need(p, 'T1', pos), T3 = need(p, 'T3', pos), k = has(p.k) ? p.k : (has(p.cp) && has(p.cv) ? p.cp / p.cv : K_AIR);
    if (!(k > 1)) throw ThermoError('range', { name: 'k', value: k });
    var etac = has(p.etac) ? p.etac : 1, etat = has(p.etat) ? p.etat : 1, Nc = has(p.Nc) ? p.Nc : 1, Nt = has(p.Nt) ? p.Nt : 1;
    var tau = T3 / T1, e = (k - 1) / k;
    if (Nc === Nt) {
      var u = Math.sqrt(etac * etat * tau);
      return { rp: Math.pow(u, Nc / e), method: 'closed', u: u };
    }
    function wn(lx) { var x = Math.exp(lx); return Nt * etat * tau * (1 - Math.pow(x, -1 / Nt)) - Nc * (Math.pow(x, 1 / Nc) - 1) / etac; }
    var a = 1e-6, b = Math.log(Math.pow(Math.max(etac * etat * tau, 1.0001), Math.max(Nc, Nt) * 2)), gr = (Math.sqrt(5) - 1) / 2;
    var c = b - gr * (b - a), d = a + gr * (b - a);
    for (var i = 0; i < 200; i++) { if (wn(c) > wn(d)) b = d; else a = c; c = b - gr * (b - a); d = a + gr * (b - a); }
    return { rp: Math.pow(Math.exp((a + b) / 2), 1 / e), method: 'numeric' };
  }
  /* pressure ratio above which a ideal regenerative cycle (eps = 1) is worse than the simple one: solve 1 - t x = 1 - 1/x with t = T1/T3 -> x = 1/sqrt(t) */
  function regenCrossover(p) {
    var T1 = need(p, 'T1', pos), T3 = need(p, 'T3', pos), k = has(p.k) ? p.k : K_AIR;
    return Math.pow(T3 / T1, k / (2 * (k - 1)));
  }

  /* ---------------- 4. Isentropic flow (ideal gas, constant k) ---------------- */
  function chkK(k) { if (!isNum(k) || !(k > 1)) throw ThermoError('range', { name: 'k', value: k }); return k; }
  function chkR(R) { if (!isNum(R) || !(R > 0)) throw ThermoError('range', { name: 'R', value: R }); return R; }
  function chkMa(M) { if (!isNum(M) || M < 0) throw ThermoError('range', { name: 'Ma', value: M }); return M; }
  function TT0(M, k) { return 1 / (1 + (k - 1) / 2 * M * M); }
  function PP0(M, k) { return Math.pow(TT0(M, k), k / (k - 1)); }
  function RR0(M, k) { return Math.pow(TT0(M, k), 1 / (k - 1)); }
  function AAs(M, k) { return (1 / M) * Math.pow(2 / (k + 1) * (1 + (k - 1) / 2 * M * M), (k + 1) / (2 * (k - 1))); }
  function fromMa(Ma, k) {
    k = has(k) ? chkK(k) : K_AIR; chkMa(Ma);
    return { Ma: Ma, k: k, TT0: TT0(Ma, k), PP0: PP0(Ma, k), rr0: RR0(Ma, k), AAs: Ma === 0 ? Infinity : AAs(Ma, k) };
  }
  function MaFromAAstar(ratio, k, branch) {
    k = has(k) ? chkK(k) : K_AIR;
    if (!isNum(ratio) || ratio < 1) throw ThermoError('aas_lt1', { value: ratio });
    if (ratio === 1) return 1;
    var sub = branch !== 'sup', lo, hi;
    if (sub) { lo = 1e-12; hi = 1; } else { lo = 1; hi = 2; while (AAs(hi, k) < ratio) { hi *= 2; if (hi > 1e6) throw ThermoError('range', { name: 'A/A*', value: ratio }); } }
    for (var i = 0; i < 300; i++) {
      var mid = (lo + hi) / 2, f = AAs(mid, k);
      if (sub) { if (f > ratio) lo = mid; else hi = mid; } else { if (f < ratio) lo = mid; else hi = mid; }
    }
    return (lo + hi) / 2;
  }
  function MaFromPratio(pr, k) {
    k = has(k) ? chkK(k) : K_AIR;
    if (!isNum(pr) || !(pr > 0 && pr <= 1)) throw ThermoError('pr_range', { value: pr });
    return Math.sqrt(2 / (k - 1) * (Math.pow(pr, -(k - 1) / k) - 1));
  }
  function MaFromTratio(tr, k) {
    k = has(k) ? chkK(k) : K_AIR;
    if (!isNum(tr) || !(tr > 0 && tr <= 1)) throw ThermoError('tr_range', { value: tr });
    return Math.sqrt(2 / (k - 1) * (1 / tr - 1));
  }
  /* stagnation properties from static T, P and speed V: T0 = T + V^2/(2 cp) with cp = kR/(k-1); R in kJ/(kg K), so V^2/2 in J/kg is divided by 1000 */
  function stagnation(p) {
    var T = need(p, 'T', pos), P = need(p, 'P', pos), V = has(p.V) ? p.V : 0, k = has(p.k) ? chkK(p.k) : K_AIR, R = has(p.R) ? chkR(p.R) : R_AIR;
    if (!isNum(V) || V < 0) throw ThermoError('range', { name: 'V', value: V });
    var cp = k * R / (k - 1), T0 = T + V * V / (2000 * cp), P0 = P * Math.pow(T0 / T, k / (k - 1));
    var c = Math.sqrt(k * R * 1000 * T), Ma = V / c;
    return { T: T, P: P, V: V, k: k, R: R, cp: cp, c: c, Ma: Ma, T0: T0, P0: P0, dT: T0 - T, dP: P0 - P, TT0: T / T0, PP0: P / P0, rho: P / (R * T), rho0: P0 / (R * T0) };
  }
  function critical(p) {
    var k = has(p.k) ? chkK(p.k) : K_AIR;
    return { k: k, TsT0: 2 / (k + 1), PsP0: Math.pow(2 / (k + 1), k / (k - 1)), rsr0: Math.pow(2 / (k + 1), 1 / (k - 1)) };
  }
  /* choked mass flow through a throat of area Astar [m2]: mdot = A* P0 sqrt(k/(R T0)) (2/(k+1))^((k+1)/(2(k-1))), with P0 in Pa and R in J/(kg K) */
  function chokedMdot(p) {
    var A = need(p, 'Astar', pos), P0 = need(p, 'P0', pos), T0 = need(p, 'T0', pos), k = has(p.k) ? chkK(p.k) : K_AIR, R = has(p.R) ? chkR(p.R) : R_AIR;
    return A * (P0 * 1000) * Math.sqrt(k / (R * 1000 * T0)) * Math.pow(2 / (k + 1), (k + 1) / (2 * (k - 1)));
  }
  /* state from P/P0 with optional T0, P0 and mass flow: T, rho, c, V, area */
  function fromPratio(p) {
    var k = has(p.k) ? chkK(p.k) : K_AIR, R = has(p.R) ? chkR(p.R) : R_AIR, pr;
    if (has(p.P) && has(p.P0)) pr = need(p, 'P', pos) / need(p, 'P0', pos); else pr = need(p, 'PP0');
    var Ma = MaFromPratio(pr, k), out = { k: k, R: R, PP0: pr, Ma: Ma, TT0: TT0(Ma, k), rr0: RR0(Ma, k), AAs: Ma === 0 ? Infinity : AAs(Ma, k) };
    if (has(p.T0)) {
      out.T0 = p.T0; out.T = p.T0 * out.TT0; out.c = Math.sqrt(k * R * 1000 * out.T); out.V = Ma * out.c;
      if (has(p.P0)) { out.P0 = p.P0; out.P = p.P0 * pr; out.rho = out.P / (R * out.T);
        if (has(p.mdot) && out.V > 0) out.A = p.mdot / (out.rho * out.V); }                   // kg/s / (kg/m3 m/s) = m2
    }
    return out;
  }
  /* duct between two sections with area ratio A2/A1 (subsonic or supersonic branch), given Ma1 (or A1/A*) */
  function duct(p) {
    var k = has(p.k) ? chkK(p.k) : K_AIR, Ma1, A1s;
    if (has(p.Ma1)) { Ma1 = chkMa(p.Ma1); if (Ma1 === 0) throw ThermoError('range', { name: 'Ma1', value: 0 }); A1s = AAs(Ma1, k); }
    else { A1s = need(p, 'A1s', function (x) { return x >= 1; }, 'aas_lt1'); Ma1 = MaFromAAstar(A1s, k, p.branch); }
    var ratio = has(p.A2A1) ? need(p, 'A2A1', pos) : 1, A2s = A1s * ratio;
    if (A2s < 1) throw ThermoError('aas_below1', { value: A2s });
    var branch = p.branch || (Ma1 < 1 ? 'sub' : 'sup');
    var Ma2 = MaFromAAstar(A2s, k, branch);
    var out = { k: k, Ma1: Ma1, A1s: A1s, A2s: A2s, Ma2: Ma2, T1T0: TT0(Ma1, k), P1P0: PP0(Ma1, k), r1r0: RR0(Ma1, k), T2T0: TT0(Ma2, k), P2P0: PP0(Ma2, k), r2r0: RR0(Ma2, k), branch: branch };
    if (has(p.T1)) out.T2 = p.T1 * out.T2T0 / out.T1T0;
    if (has(p.P1)) out.P2 = p.P1 * out.P2P0 / out.P1P0;
    return out;
  }
  /* converging nozzle with back pressure Pb. Inlet T, P, V (V = 0 means stagnation values). Exit area Ae [m2] */
  function convergingNozzle(p) {
    var k = has(p.k) ? chkK(p.k) : K_AIR, R = has(p.R) ? chkR(p.R) : R_AIR;
    var st = stagnation({ T: p.T, P: p.P, V: has(p.V) ? p.V : 0, k: k, R: R }), Pb = need(p, 'Pb', pos), Ae = need(p, 'Ae', pos);
    if (Pb > st.P0 * (1 + 1e-12)) throw ThermoError('pb_gt_p0', { Pb: Pb, P0: st.P0 });
    var cr = critical({ k: k }), Pcrit = st.P0 * cr.PsP0, choked = Pb < Pcrit, Pe, Ma, Te, rho, V, mdot;
    if (choked) { Pe = Pcrit; Ma = 1; } else { Pe = Pb; Ma = MaFromPratio(Pe / st.P0, k); }
    Te = st.T0 * TT0(Ma, k); rho = Pe / (R * Te); V = Ma * Math.sqrt(k * R * 1000 * Te);
    mdot = rho * Ae * V;
    var mdotChoked = chokedMdot({ Astar: Ae, P0: st.P0, T0: st.T0, k: k, R: R });
    return { k: k, R: R, T0: st.T0, P0: st.P0, Pcrit: Pcrit, PbP0: Pb / st.P0, PcritP0: cr.PsP0, choked: choked, Pe: Pe, Ma: Ma, Te: Te, rho: rho, V: V, mdot: mdot, mdotChoked: mdotChoked, Ae: Ae };
  }

  /* ---------------- 5. Combustion (complete, lean or stoichiometric) ---------------- */
  /* fuel CaHbOcNd + (1+e) a_th (O2 + 3.76 N2) -> a CO2 + b/2 H2O + e a_th O2 + (3.76 (1+e) a_th + d/2) N2 ; e = excess air fraction >= 0 */
  function molarMass(f) { return ATOM.C * f.a + ATOM.H * f.b + ATOM.O * f.c + ATOM.N * f.d; }
  function combustion(p) {
    var a = has(p.a) ? p.a : 0, b = has(p.b) ? p.b : 0, c = has(p.c) ? p.c : 0, d = has(p.d) ? p.d : 0, ex = has(p.excess) ? p.excess : 0;
    [['a', a], ['b', b], ['c', c], ['d', d]].forEach(function (z) { if (!isNum(z[1]) || z[1] < 0) throw ThermoError('range', { name: z[0], value: z[1] }); });
    if (!(a > 0 || b > 0)) throw ThermoError('nofuel', {});
    if (!isNum(ex)) throw ThermoError('range', { name: 'excess', value: ex });
    if (ex < 0) throw ThermoError('rich', { value: ex });
    var Pprod = has(p.Pprod) ? need(p, 'Pprod', pos) : 100;
    var ath = a + b / 4 - c / 2;
    if (!(ath > 0)) throw ThermoError('no_o2', { ath: ath });
    var lam = 1 + ex / 100, nO2 = lam * ath, nN2air = 3.76 * nO2;
    var co2 = a, h2o = b / 2, o2 = (lam - 1) * ath, n2 = nN2air + d / 2, tot = co2 + h2o + o2 + n2;
    var Mf = molarMass({ a: a, b: b, c: c, d: d }), nAir = nO2 * 4.76;
    var AFmass = nAir * M_AIR / Mf, AFmol = nAir, AFth = ath * 4.76 * M_AIR / Mf;
    return { a: a, b: b, c: c, d: d, excess: ex, lambda: lam, ath: ath, nO2: nO2, nN2air: nN2air, nAir: nAir, Mf: Mf, Mair: M_AIR,
      co2: co2, h2o: h2o, o2: o2, n2: n2, tot: tot, y: { co2: co2 / tot, h2o: h2o / tot, o2: o2 / tot, n2: n2 / tot },
      AFmass: AFmass, AFmol: AFmol, AFth: AFth, Pv: Pprod * h2o / tot, Pprod: Pprod, pctTheoretical: 100 + ex,
      mProducts: { co2: co2 * (ATOM.C + 2 * ATOM.O), h2o: h2o * (2 * ATOM.H + ATOM.O), o2: o2 * 2 * ATOM.O, n2: n2 * 2 * ATOM.N } };
  }

  var api = { ThermoError: ThermoError, otto: otto, diesel: diesel, dieselEta: dieselEta, brayton: brayton, braytonOptRp: braytonOptRp, regenCrossover: regenCrossover,
    fromMa: fromMa, MaFromAAstar: MaFromAAstar, MaFromPratio: MaFromPratio, MaFromTratio: MaFromTratio, stagnation: stagnation, critical: critical,
    chokedMdot: chokedMdot, fromPratio: fromPratio, duct: duct, convergingNozzle: convergingNozzle, combustion: combustion, molarMass: molarMass,
    consts: { R_AIR: R_AIR, K_AIR: K_AIR, M_AIR: M_AIR, ATOM: ATOM }, gas: gas };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Thermo = api;
})(typeof window !== 'undefined' ? window : this);
