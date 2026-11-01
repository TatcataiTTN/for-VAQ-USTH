/* Demo tuong tac cho AE2.008. Ham thuan (AERO) kiem bang Node so voi aero.py; phan giao dien chi chay trong trinh duyet. */
(function (root) {
  'use strict';
  var G0 = 9.80665, R = 287.05287, GAMMA = 1.4, P0 = 101325, T0 = 288.15, RHO0 = 1.225, FT = 0.3048, KT = 0.514444, PSI = 6894.757;

  function isa(hm, dT) {            // ISA 0..20 km, dT = do lech nhiet do (K) so voi ISA
    dT = dT || 0;
    var T, p;
    if (hm <= 11000) { var Lr = -0.0065; T = T0 + Lr * hm; p = P0 * Math.pow(T / T0, -G0 / (Lr * R)); }
    else { T = 216.65; var p11 = P0 * Math.pow(216.65 / T0, -G0 / (-0.0065 * R)); p = p11 * Math.exp(-G0 * (hm - 11000) / (R * T)); }
    var Tact = T + dT;
    return { T: Tact, p: p, rho: p / (R * Tact) };
  }
  function densityAltitudeFt(rho) {
    var lo = 0, hi = 20000;
    for (var i = 0; i < 80; i++) { var mid = (lo + hi) / 2; if (isa(mid, 0).rho > rho) lo = mid; else hi = mid; }
    return lo / FT;
  }
  function soundSpeed(T) { return Math.sqrt(GAMMA * R * T); }
  // NACA 2412, bang bai 1.6 Anderson
  var ALPHA = [-2, 0, 2, 4, 6, 8, 10, 12, 14], CLT = [0.05, 0.25, 0.44, 0.64, 0.85, 1.08, 1.26, 1.43, 1.56],
      CDT = [0.006, 0.006, 0.006, 0.007, 0.0075, 0.0092, 0.0115, 0.015, 0.0186];
  function interp(x, xs, ys) {
    if (x <= xs[0]) return ys[0];
    for (var i = 1; i < xs.length; i++) if (x <= xs[i]) { var t = (x - xs[i - 1]) / (xs[i] - xs[i - 1]); return ys[i - 1] + t * (ys[i] - ys[i - 1]); }
    return ys[ys.length - 1];
  }
  function turn(bankDeg, vs) { var n = 1 / Math.cos(bankDeg * Math.PI / 180); return { n: n, vs: vs * Math.sqrt(n) }; }
  function normalShock(M1) {
    var g = GAMMA, M2 = Math.sqrt(((g - 1) * M1 * M1 + 2) / (2 * g * M1 * M1 - (g - 1)));
    var p = 1 + 2 * g / (g + 1) * (M1 * M1 - 1), rho = (g + 1) * M1 * M1 / ((g - 1) * M1 * M1 + 2);
    return { M2: M2, p: p, rho: rho, T: p / rho, p0: Math.pow((g + 1) * M1 * M1 / ((g - 1) * M1 * M1 + 2), g / (g - 1)) * Math.pow((g + 1) / (2 * g * M1 * M1 - (g - 1)), 1 / (g - 1)) };
  }
  function thetaBetaM(M, b) { var g = GAMMA; return Math.atan(2 / Math.tan(b) * (M * M * Math.sin(b) * Math.sin(b) - 1) / (M * M * (g + Math.cos(2 * b)) + 2)); }
  function thetaMax(M) { var mu = Math.asin(1 / M), best = 0, bb = mu, n = 4000; for (var i = 1; i < n; i++) { var b = mu + (Math.PI / 2 - mu) * i / n, t = thetaBetaM(M, b); if (t > best) { best = t; bb = b; } } return { theta: best, beta: bb }; }
  function betaFromTheta(M, th, strong) {
    var tm = thetaMax(M); if (th > tm.theta) return null; var mu = Math.asin(1 / M), lo = strong ? tm.beta : mu, hi = strong ? Math.PI / 2 : tm.beta;
    for (var i = 0; i < 100; i++) { var mid = (lo + hi) / 2, f = thetaBetaM(M, mid) - th; if ((!strong && f < 0) || (strong && f > 0)) lo = mid; else hi = mid; }
    return (lo + hi) / 2;
  }
  function oblique(M1, beta, th) { var s = normalShock(M1 * Math.sin(beta)); return { Mn1: M1 * Math.sin(beta), M2: s.M2 / Math.sin(beta - th), p: s.p, rho: s.rho, T: s.T, p0: s.p0 }; }
  function cdInduced(CL, AR, e) { return CL * CL / (Math.PI * e * AR); }
  function staticStab(h, hn, cla) { return { Kn: hn - h, Cma: cla * (h - hn) }; }
  // B747, Etkin 6.2,1: state [du, w, q, dtheta]
  var A747 = [[-0.006868, 0.01395, 0, -32.2], [-0.09055, -0.3151, 773.98, 0], [0.0001187, -0.001026, -0.4285, 0], [0, 0, 1, 0]];
  function matvec(A, x) { return A.map(function (r) { return r.reduce(function (s, a, j) { return s + a * x[j]; }, 0); }); }
  function rk4(A, x0, tEnd, dt) {
    var x = x0.slice(), t = 0, out = [[0].concat(x)];
    var n = Math.round(tEnd / dt);
    for (var k = 0; k < n; k++) {
      var k1 = matvec(A, x), k2 = matvec(A, x.map(function (v, i) { return v + dt / 2 * k1[i]; })),
          k3 = matvec(A, x.map(function (v, i) { return v + dt / 2 * k2[i]; })), k4 = matvec(A, x.map(function (v, i) { return v + dt * k3[i]; }));
      x = x.map(function (v, i) { return v + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]); });
      t += dt; out.push([t].concat(x));
    }
    return out;
  }

  var ALAT = [[-0.0558, 0, -774, 32.2], [-0.003865, -0.4342, 0.4136, 0], [0.001086, -0.006112, -0.1458, 0], [0, 1, 0, 0]];
  function latWithDamper(dNr) { var A = ALAT.map(function (r) { return r.slice(); }); A[2][2] -= dNr; return A; }
  var AERO = { thetaBetaM: thetaBetaM, thetaMax: thetaMax, betaFromTheta: betaFromTheta, oblique: oblique, cdInduced: cdInduced, isa: isa, ALAT: ALAT, latWithDamper: latWithDamper, densityAltitudeFt: densityAltitudeFt, soundSpeed: soundSpeed, interp: interp, ALPHA: ALPHA, CLT: CLT, CDT: CDT,
               turn: turn, normalShock: normalShock, staticStab: staticStab, A747: A747, rk4: rk4, FT: FT, KT: KT, PSI: PSI, RHO0: RHO0 };
  if (typeof module !== 'undefined' && module.exports) { module.exports = AERO; return; }
  root.AERO = AERO;

  // ------------------------------------------------------------------ UI
  var LANG = document.documentElement.lang === 'en' ? 'en' : 'vi';
  var T = function (vi, en) { return LANG === 'vi' ? vi : en; };
  var fmt = function (x, d) { var s = x.toFixed(d); return LANG === 'vi' ? s.replace('.', ',') : s; };

  function slider(label, min, max, step, val, unit, onchange, host) {
    var row = document.createElement('div'); row.className = 'demo-row';
    var lab = document.createElement('label'); lab.textContent = label + ' ';
    var inp = document.createElement('input'); inp.type = 'range'; inp.min = min; inp.max = max; inp.step = step; inp.value = val;
    var out = document.createElement('b'); out.className = 'demo-val';
    function upd() { out.textContent = fmt(parseFloat(inp.value), step < 1 ? 2 : 0) + ' ' + unit; onchange(); }
    inp.addEventListener('input', upd); lab.appendChild(inp); row.appendChild(lab); row.appendChild(out); host.appendChild(row);
    out.textContent = fmt(parseFloat(inp.value), step < 1 ? 2 : 0) + ' ' + unit;
    return { get: function () { return parseFloat(inp.value); }, el: inp };
  }
  function resultBox(host) { var d = document.createElement('div'); d.className = 'demo-out'; host.appendChild(d); return d; }
  function css(name, fb) { var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim(); return v || fb; }
  function chart(canvas, series, o) {
    var ctx = canvas.getContext('2d'), W = canvas.width, H = canvas.height, ml = 64, mb = 34, mt = 10, mr = 12;
    var fg = css('--text', css('--fg', '#1c2333')), muted = css('--muted', '#667'), bd = css('--border', '#ccd');
    ctx.clearRect(0, 0, W, H);
    var xs = [], ys = []; series.forEach(function (s) { s.pts.forEach(function (p) { xs.push(p[0]); ys.push(p[1]); }); });
    var x0 = o.xmin !== undefined ? o.xmin : Math.min.apply(null, xs), x1 = o.xmax !== undefined ? o.xmax : Math.max.apply(null, xs);
    var y0 = o.ymin !== undefined ? o.ymin : Math.min.apply(null, ys), y1 = o.ymax !== undefined ? o.ymax : Math.max.apply(null, ys);
    if (y1 === y0) y1 = y0 + 1;
    var X = function (x) { return ml + (x - x0) / (x1 - x0) * (W - ml - mr); }, Y = function (y) { return H - mb - (y - y0) / (y1 - y0) * (H - mb - mt); };
    ctx.strokeStyle = bd; ctx.fillStyle = muted; ctx.font = '12px sans-serif'; ctx.lineWidth = 1;
    for (var i = 0; i <= 5; i++) {
      var gx = x0 + (x1 - x0) * i / 5, gy = y0 + (y1 - y0) * i / 5;
      ctx.beginPath(); ctx.moveTo(X(gx), mt); ctx.lineTo(X(gx), H - mb); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(ml, Y(gy)); ctx.lineTo(W - mr, Y(gy)); ctx.stroke();
      ctx.fillText(fmt(gx, o.xd === undefined ? 1 : o.xd), X(gx) - 12, H - mb + 14); ctx.fillText(fmt(gy, o.yd === undefined ? 2 : o.yd), 4, Y(gy) + 4);
    }
    ctx.fillStyle = fg; ctx.fillText(o.xlabel || '', W / 2 - 30, H - 6); ctx.save(); ctx.translate(14, H / 2 + 20); ctx.rotate(-Math.PI / 2); ctx.fillText(o.ylabel || '', 0, 0); ctx.restore();
    series.forEach(function (s) {
      ctx.strokeStyle = s.color; ctx.lineWidth = s.w || 2; ctx.beginPath();
      s.pts.forEach(function (p, k) { if (k === 0) ctx.moveTo(X(p[0]), Y(p[1])); else ctx.lineTo(X(p[0]), Y(p[1])); }); ctx.stroke();
      if (s.dot) { ctx.fillStyle = s.color; ctx.beginPath(); ctx.arc(X(s.dot[0]), Y(s.dot[1]), 5, 0, 7); ctx.fill(); }
    });
    if (o.legend) { ctx.fillStyle = fg; o.legend.forEach(function (l, k) { ctx.fillStyle = l.color; ctx.fillRect(ml + 8, mt + 6 + k * 16, 12, 3); ctx.fillStyle = fg; ctx.fillText(l.text, ml + 26, mt + 11 + k * 16); }); }
  }
  function canvasFor(host, h) { var c = document.createElement('canvas'); c.width = 640; c.height = h || 260; c.style.cssText = 'max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px'; host.appendChild(c); return c; }

  function demoISA(host) {
    var alt = slider(T('Độ cao', 'Altitude'), 0, 60000, 500, 5000, 'ft', upd, host), dt = slider(T('Lệch ISA (ΔT)', 'ISA deviation (ΔT)'), -30, 30, 1, 0, '°C', upd, host), out = resultBox(host);
    function upd() {
      var s = isa(alt.get() * FT, dt.get()), a = soundSpeed(s.T) / KT, sig = s.rho / RHO0, da = densityAltitudeFt(s.rho);
      out.innerHTML = '<p><b>T</b> = ' + fmt(s.T - 273.15, 1) + ' °C &nbsp; <b>p</b> = ' + fmt(s.p / 100, 1) + ' hPa (' + fmt(s.p / PSI, 2) + ' psi) &nbsp; <b>ρ</b> = ' + fmt(s.rho, 4) + ' kg/m³ &nbsp; <b>σ = ρ/ρ₀</b> = ' + fmt(sig, 3) +
        '</p><p><b>a</b> = ' + fmt(a, 0) + ' kt &nbsp; <b>' + T('Độ cao mật độ', 'Density altitude') + '</b> ≈ ' + fmt(da, 0) + ' ft</p>';
    }
    upd();
  }
  function demoLift(host) {
    var alt = slider(T('Độ cao', 'Altitude'), 0, 40000, 500, 0, 'ft', upd, host), V = slider(T('Tốc độ thực', 'True airspeed'), 20, 250, 1, 60, 'm/s', upd, host),
        S = slider(T('Diện tích cánh S', 'Wing area S'), 5, 200, 1, 16, 'm²', upd, host), al = slider(T('Góc tấn α', 'Angle of attack α'), -2, 14, 0.5, 4, '°', upd, host),
        mass = slider(T('Khối lượng', 'Mass'), 200, 20000, 50, 1000, 'kg', upd, host), out = resultBox(host), cv = canvasFor(host, 260);
    function upd() {
      var s = isa(alt.get() * FT, 0), q = 0.5 * s.rho * V.get() * V.get(), cl = interp(al.get(), ALPHA, CLT), cd = interp(al.get(), ALPHA, CDT), Lf = q * S.get() * cl, W = mass.get() * G0, clreq = W / (q * S.get());
      out.innerHTML = '<p>q = ' + fmt(q, 1) + ' Pa &nbsp; C<sub>L</sub>(α) = ' + fmt(cl, 2) + ' &nbsp; <b>L</b> = ' + fmt(Lf, 0) + ' N &nbsp; (' + T('trọng lượng', 'weight') + ' W = ' + fmt(W, 0) + ' N)</p><p>' +
        T('C_L cần để bay thẳng đều: ', 'C_L needed for level flight: ') + '<b>' + fmt(clreq, 2) + '</b> ' + (clreq > 1.56 ? '⚠️ ' + T('vượt dải số liệu (c_l tối đa trong bảng 1,56)', 'beyond the table range (max c_l in the table is 1.56)') : (clreq <= cl ? '✅ ' + T('L ≥ W', 'L ≥ W') : '⬇️ ' + T('L &lt; W: tăng α hoặc tốc độ', 'L &lt; W: raise α or speed'))) +
        '</p><p>' + T('Số liệu c_l, c_d của NACA 2412 từ Anderson bài 1.6 (biên dạng 2D, nội suy tuyến tính, không có thất tốc ngoài 14°); đây là minh họa.', 'c_l and c_d of the NACA 2412 from Anderson problem 1.6 (2D section, linear interpolation, no stall data beyond 14°); this is an illustration.') + '</p>';
      chart(cv, [{ pts: ALPHA.map(function (a, i) { return [a, CLT[i]]; }), color: '#1657d6', dot: [al.get(), cl] }], { xlabel: 'α (°)', ylabel: 'c_l', xmin: -2, xmax: 14, ymin: 0, ymax: 1.8 });
    }
    upd();
  }
  function demoTurn(host) {
    var bank = slider(T('Góc nghiêng φ', 'Bank angle φ'), 0, 75, 1, 45, '°', upd, host), vs = slider(T('Tốc độ thất tốc bay thẳng V_s', 'Straight-flight stall speed V_s'), 30, 150, 1, 60, 'kt', upd, host), out = resultBox(host), cv = canvasFor(host, 240);
    function upd() {
      var r = turn(bank.get(), vs.get());
      out.innerHTML = '<p><b>n</b> = 1/cos φ = ' + fmt(r.n, 2) + ' g &nbsp; <b>V<sub>s,turn</sub></b> = V<sub>s</sub>√n = ' + fmt(r.vs, 1) + ' kt (+' + fmt((r.vs / vs.get() - 1) * 100, 0) + '%)</p><p>' + T('Hệ số tải giới hạn hạng Normal là +3,8 g: vòng bay thăng bằng đạt tới mức đó ở φ ≈ ', 'The Normal category limit load factor is +3.8 g: a level turn reaches it at φ ≈ ') + fmt(Math.acos(1 / 3.8) * 180 / Math.PI, 1) + '°.</p>';
      var pts = [], pts2 = []; for (var b = 0; b <= 75; b += 1) { var t = turn(b, 1); pts.push([b, t.n]); pts2.push([b, t.vs]); }
      chart(cv, [{ pts: pts, color: '#d4421d' }, { pts: pts2, color: '#1657d6', dot: [bank.get(), r.vs / vs.get()] }], { xlabel: 'φ (°)', ylabel: 'n, V_s,turn/V_s', xmin: 0, xmax: 75, ymin: 1, ymax: 4, xd: 0, legend: [{ color: '#d4421d', text: 'n' }, { color: '#1657d6', text: 'V_s,turn / V_s' }] });
    }
    upd();
  }
  function demoShock(host) {
    var alt = slider(T('Độ cao', 'Altitude'), 0, 60000, 500, 40000, 'ft', upd, host), M = slider(T('Số Mach dòng tự do M₁', 'Free-stream Mach M₁'), 0.3, 4, 0.05, 2.6, '', upd, host), out = resultBox(host);
    function upd() {
      var s = isa(alt.get() * FT, 0), a = soundSpeed(s.T) / KT, m = M.get(), tas = m * a, h = '<p><b>a</b> = ' + fmt(a, 0) + ' kt &nbsp; <b>' + T('Tốc độ thực', 'True airspeed') + '</b> = ' + fmt(tas, 0) + ' kt</p>';
      if (m > 1) { var sh = normalShock(m); h += '<p>' + T('Sóng xung kích thẳng: ', 'Normal shock: ') + 'M₂ = ' + fmt(sh.M2, 3) + ', p₂/p₁ = ' + fmt(sh.p, 2) + ', ρ₂/ρ₁ = ' + fmt(sh.rho, 3) + ', T₂/T₁ = ' + fmt(sh.T, 3) + ', p₀₂/p₀₁ = ' + fmt(sh.p0, 3) + '</p>'; }
      else h += '<p>' + T('M₁ ≤ 1: không có sóng xung kích thẳng. Số Mach tới hạn thường nằm dưới 1 (ví dụ 0,74 cho C_p,0 = −0,41).', 'M₁ ≤ 1: no normal shock. The critical Mach number usually lies below 1 (e.g. 0.74 for C_p,0 = −0.41).') + '</p>';
      out.innerHTML = h;
    }
    upd();
  }
  function demoStab(host) {
    var h = slider(T('Vị trí CG h (theo MAC)', 'CG position h (MAC fraction)'), 0.05, 0.6, 0.01, 0.25, '', upd, host), hn = slider(T('Điểm trung hòa h_n', 'Neutral point h_n'), 0.2, 0.6, 0.01, 0.35, '', upd, host), cla = slider('C_Lα', 2, 6, 0.1, 4.5, '/rad', upd, host), out = resultBox(host), cv = canvasFor(host, 240);
    function upd() {
      var s = staticStab(h.get(), hn.get(), cla.get()), stable = s.Cma < 0;
      out.innerHTML = '<p><b>K<sub>n</sub></b> = h_n − h = ' + fmt(s.Kn, 2) + ' &nbsp; <b>C<sub>mα</sub></b> = C_Lα(h − h_n) = ' + fmt(s.Cma, 2) + ' /rad &nbsp; ' + (stable ? '✅ ' + T('ổn định tĩnh dọc (CG trước NP)', 'statically stable (CG ahead of the NP)') : (Math.abs(s.Cma) < 1e-9 ? '⚠️ ' + T('trung tính', 'neutral') : '❌ ' + T('bất ổn tĩnh (CG sau NP)', 'statically unstable (CG behind the NP)'))) + '</p>' +
        (s.Kn >= 0.05 ? '' : '<p>⚠️ ' + T('Lề ổn định dưới 5% MAC: thấp hơn yêu cầu thông thường trong Etkin 1.5.', 'Static margin below 5% MAC: less than the usual requirement in Etkin 1.5.') + '</p>');
      var pts = []; for (var a = -0.1; a <= 0.1001; a += 0.01) pts.push([a * 180 / Math.PI, s.Cma * a]);
      chart(cv, [{ pts: pts, color: stable ? '#1a8a4a' : '#d4421d' }], { xlabel: 'Δα (°)', ylabel: 'ΔC_m', xmin: -5.7, xmax: 5.7, ymin: -1.6, ymax: 1.6, xd: 1 });
    }
    upd();
  }
  function demoModes(host) {
    var sel = document.createElement('div'); sel.className = 'demo-row';
    sel.innerHTML = '<label>' + T('Nhiễu ban đầu', 'Initial disturbance') + ' <select><option value="u">' + T('Δu = 10 ft/s (kích phugoid)', 'Δu = 10 ft/s (excites the phugoid)') + '</option><option value="q">' + T('q = 0,05 rad/s (kích chu kỳ ngắn)', 'q = 0.05 rad/s (excites the short period)') + '</option></select></label> <label>' + T('Cửa sổ thời gian', 'Time window') + ' <select><option value="300">300 s</option><option value="20">20 s</option></select></label>';
    host.appendChild(sel); var out = resultBox(host), c1 = canvasFor(host, 240), c2 = canvasFor(host, 240); var ss = sel.querySelectorAll('select');
    function upd() {
      var x0 = ss[0].value === 'u' ? [10, 0, 0, 0] : [0, 0, 0.05, 0], tEnd = parseFloat(ss[1].value), dt = tEnd > 100 ? 0.05 : 0.01, tr = rk4(A747, x0, tEnd, dt);
      var step = Math.max(1, Math.floor(tr.length / 600)), du = [], th = [];
      for (var i = 0; i < tr.length; i += step) { du.push([tr[i][0], tr[i][1]]); th.push([tr[i][0], tr[i][4] * 180 / Math.PI]); }
      out.innerHTML = '<p>' + T('Mô phỏng ẋ = A·x với ma trận A của B747 (Etkin 6.2,1), tích phân Runge-Kutta bậc 4. Trạng thái x = [Δu, w, q, Δθ].', 'Simulation of ẋ = A·x with the B747 matrix A (Etkin 6.2,1), fourth-order Runge-Kutta. State x = [Δu, w, q, Δθ].') + '</p>';
      chart(c1, [{ pts: du, color: '#1657d6' }], { xlabel: 't (s)', ylabel: 'Δu (ft/s)', xd: 0, yd: 1 });
      chart(c2, [{ pts: th, color: '#d4421d' }], { xlabel: 't (s)', ylabel: 'Δθ (°)', xd: 0, yd: 2 });
    }
    ss[0].addEventListener('change', upd); ss[1].addEventListener('change', upd); upd();
  }

  function demoLat(host) {
    var sel = document.createElement('div'); sel.className = 'demo-row';
    sel.innerHTML = '<label>' + T('Nhiễu ban đầu', 'Initial disturbance') + ' <select><option value="v">' + T('trượt ngang v = 10 ft/s (Dutch roll)', 'sideslip v = 10 ft/s (Dutch roll)') + '</option><option value="p">' + T('tốc độ lăn p = 0,05 rad/s (hội tụ lăn)', 'roll rate p = 0.05 rad/s (roll convergence)') + '</option><option value="phi">' + T('nghiêng φ = 5° (mode xoắn ốc)', 'bank φ = 5° (spiral mode)') + '</option></select></label> <label>' + T('Cửa sổ', 'Window') + ' <select><option value="30">30 s</option><option value="300">300 s</option></select></label>';
    host.appendChild(sel); var dn = slider(T('Giảm xoay nhân tạo thêm ΔN_r', 'Added artificial yaw damping ΔN_r'), 0, 1, 0.05, 0, '1/s', upd, host), out = resultBox(host), c1 = canvasFor(host, 240); var ss = sel.querySelectorAll('select');
    function upd() {
      var k = ss[0].value, x0 = k === 'v' ? [10, 0, 0, 0] : (k === 'p' ? [0, 0.05, 0, 0] : [0, 0, 0, 5 * Math.PI / 180]), tEnd = parseFloat(ss[1].value), dt = tEnd > 100 ? 0.05 : 0.01;
      var tr = rk4(latWithDamper(dn.get()), x0, tEnd, dt), step = Math.max(1, Math.floor(tr.length / 600)), ph = [], be = [];
      for (var i = 0; i < tr.length; i += step) { ph.push([tr[i][0], tr[i][4] * 180 / Math.PI]); be.push([tr[i][0], tr[i][1] / 774 * 180 / Math.PI]); }
      out.innerHTML = '<p>' + T('Mô phỏng ẋ = A·x với ma trận ngang của B747 (Etkin 6.7,1), x = [v, p, r, φ]. Thanh trượt cộng thêm ΔN_r vào phần tử r của hàng r: mô hình đơn giản hóa một bộ giảm xoay, không phải vòng điều khiển bánh lái thật.', 'Simulation of ẋ = A·x with the B747 lateral matrix (Etkin 6.7,1), x = [v, p, r, φ]. The slider subtracts ΔN_r from the r-r element: a simplified model of a yaw damper, not the real rudder loop.') + '</p>';
      chart(c1, [{ pts: ph, color: '#1657d6' }, { pts: be, color: '#d4421d' }], { xlabel: 't (s)', ylabel: 'φ (°), β (°)', xd: 0, yd: 2, legend: [{ color: '#1657d6', text: 'φ' }, { color: '#d4421d', text: 'β = v/u₀' }] });
    }
    ss[0].addEventListener('change', upd); ss[1].addEventListener('change', upd); upd();
  }

  function demoOblique(host) {
    var M = slider(T('Mach thượng nguồn M₁', 'Upstream Mach M₁'), 1.2, 5, 0.05, 2.5, '', upd, host), th = slider(T('Góc lệch dòng θ', 'Flow deflection θ'), 1, 40, 0.1, 22.2, '°', upd, host), out = resultBox(host), cv = canvasFor(host, 250);
    function upd() {
      var m = M.get(), t = th.get() * Math.PI / 180, tm = thetaMax(m), h;
      if (t > tm.theta) h = '<p>❌ ' + T('θ lớn hơn θ_max = ', 'θ exceeds θ_max = ') + fmt(tm.theta * 180 / Math.PI, 2) + '°: ' + T('sóng tách rời, không có nghiệm sóng bám.', 'the shock detaches; there is no attached solution.') + '</p>';
      else { var bw = betaFromTheta(m, t, false), bs = betaFromTheta(m, t, true), ow = oblique(m, bw, t), os = oblique(m, bs, t);
        h = '<p><b>' + T('Sóng yếu', 'Weak shock') + '</b> β = ' + fmt(bw * 180 / Math.PI, 2) + '°, M₂ = ' + fmt(ow.M2, 3) + ', p₂/p₁ = ' + fmt(ow.p, 3) + ', T₂/T₁ = ' + fmt(ow.T, 3) + ', p₀₂/p₀₁ = ' + fmt(ow.p0, 3) + '</p><p><b>' + T('Sóng mạnh', 'Strong shock') + '</b> β = ' + fmt(bs * 180 / Math.PI, 2) + '°, M₂ = ' + fmt(os.M2, 3) + ', p₂/p₁ = ' + fmt(os.p, 3) + '</p><p>θ_max = ' + fmt(tm.theta * 180 / Math.PI, 2) + '°, μ = ' + fmt(Math.asin(1 / m) * 180 / Math.PI, 2) + '°</p>'; }
      out.innerHTML = h;
      var pts = []; var mu = Math.asin(1 / m); for (var i = 1; i < 200; i++) { var b = mu + (Math.PI / 2 - mu) * i / 200; pts.push([b * 180 / Math.PI, thetaBetaM(m, b) * 180 / Math.PI]); }
      chart(cv, [{ pts: pts, color: '#1657d6', dot: t <= tm.theta ? [betaFromTheta(m, t, false) * 180 / Math.PI, th.get()] : null }], { xlabel: 'β (°)', ylabel: 'θ (°)', xd: 0, yd: 0 });
    }
    upd();
  }
  function demoAR(host) {
    var CL = slider('C_L', 0.1, 1.5, 0.05, 0.5, '', upd, host), AR = slider('AR', 3, 30, 0.5, 8, '', upd, host), e = slider('e', 0.6, 1, 0.01, 1, '', upd, host), out = resultBox(host), cv = canvasFor(host, 240);
    function upd() {
      var cd = cdInduced(CL.get(), AR.get(), e.get());
      out.innerHTML = '<p><b>α<sub>i</sub></b> = C_L/(π·AR) = ' + fmt(CL.get() / (Math.PI * AR.get()) * 180 / Math.PI, 3) + '° &nbsp; <b>C<sub>D,i</sub></b> = C_L²/(π e AR) = ' + fmt(cd, 5) + '</p><p>' + T('Cùng C_L, AR = 12 cho ', 'At the same C_L, AR = 12 gives ') + fmt(cdInduced(CL.get(), 12, e.get()), 5) + '.</p>';
      var pts = []; for (var a = 3; a <= 30; a += 0.5) pts.push([a, cdInduced(CL.get(), a, e.get())]);
      chart(cv, [{ pts: pts, color: '#1657d6', dot: [AR.get(), cd] }], { xlabel: 'AR', ylabel: 'C_D,i', xd: 0, yd: 4, xmin: 3, xmax: 30 });
    }
    upd();
  }

  var MAP = { 'demo-oblique': demoOblique, 'demo-ar': demoAR, 'demo-lat': demoLat, 'demo-isa': demoISA, 'demo-lift': demoLift, 'demo-turn': demoTurn, 'demo-shock': demoShock, 'demo-stab': demoStab, 'demo-modes': demoModes };
  function init() { Object.keys(MAP).forEach(function (k) { document.querySelectorAll('.' + k).forEach(function (el) { if (!el.dataset.ready) { el.dataset.ready = '1'; MAP[k](el); } }); }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})(typeof window !== 'undefined' ? window : globalThis);
