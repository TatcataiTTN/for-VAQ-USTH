/* Demo 08: máy tính sợi quang (góc tới hạn, NA, V, số mode, ngân sách suy hao) và mô phỏng tia sáng (Snell/TIR).
   Chạy 100% trong trình duyệt. Hàm thuần được xuất cho kiểm thử bằng Node. */
(function () {
  var RAD = Math.PI / 180;
  function fibre(n1, n2, n0, dum, lamnm) {
    var out = { ok: n1 > n2 && n2 > 0 && n0 > 0 };
    if (!out.ok) return out;
    out.thc = Math.asin(n2 / n1) / RAD;
    out.NA = Math.sqrt(n1 * n1 - n2 * n2);
    out.guided = out.NA / n0 <= 1;
    out.tha = out.guided ? Math.asin(out.NA / n0) / RAD : 90;
    if (dum > 0 && lamnm > 0) {
      out.V = Math.PI * dum * 1e-6 * out.NA / (lamnm * 1e-9);
      out.N = out.V * out.V / 2;
      out.single = out.V < 2.405;
    }
    out.delta = (n1 * n1 - n2 * n2) / (2 * n1 * n1);
    return out;
  }
  function lmax(pin_mW, pmin_uW, alpha_dBkm) { return 10 * Math.log10(pin_mW * 1000 / pmin_uW) / alpha_dBkm; }
  function snell(n1, n2, thDeg) { // tra ve {refracted:deg|null (TIR), thc:deg|null}
    var s = n1 * Math.sin(thDeg * RAD) / n2;
    var thc = n1 > n2 ? Math.asin(n2 / n1) / RAD : null;
    return { refracted: Math.abs(s) <= 1 ? Math.asin(s) / RAD : null, thc: thc };
  }
  if (typeof module !== "undefined") module.exports = { fibre: fibre, lmax: lmax, snell: snell };
  if (typeof document === "undefined") return;

  function f(x, d) { return (isFinite(x) ? x.toFixed(d) : "-"); }
  function initCalc(root) {
    var en = root.getAttribute("data-lang") === "en";
    var T = en ? {
      n1: "Core index n₁", n2: "Cladding index n₂", n0: "Outside index n₀ (air = 1)", d: "Core diameter (µm)", lam: "Wavelength (nm)",
      pin: "Input power (mW)", pmin: "Minimum detectable power (µW)", al: "Attenuation (dB/km)",
      thc: "Critical angle θc", na: "Numerical aperture NA", tha: "Acceptance angle θa", v: "V-number", n: "Modes N ≈ V²/2",
      lm: "Maximum length", mode: "Fibre type at this λ", sm: "single-mode (V < 2.405)", mm: "multimode", bad: "Need n₁ > n₂ > 0 for guiding.",
      deg: "°", km: "km", cond: "NA > n₀: every ray from outside is accepted (θa = 90°)"
    } : {
      n1: "Chiết suất lõi n₁", n2: "Chiết suất vỏ n₂", n0: "Chiết suất môi trường ngoài n₀ (không khí = 1)", d: "Đường kính lõi (µm)", lam: "Bước sóng (nm)",
      pin: "Công suất vào (mW)", pmin: "Công suất tối thiểu đo được (µW)", al: "Suy hao (dB/km)",
      thc: "Góc tới hạn θc", na: "Khẩu độ số NA", tha: "Góc chấp nhận θa", v: "Tần số chuẩn hoá V", n: "Số mode N ≈ V²/2",
      lm: "Chiều dài tối đa", mode: "Loại sợi ở bước sóng này", sm: "đơn mode (V < 2,405)", mm: "đa mode", bad: "Cần n₁ > n₂ > 0 để dẫn sáng.",
      deg: "°", km: "km", cond: "NA > n₀: mọi tia từ ngoài đều được nhận (θa = 90°)"
    };
    var F = [["n1", 1.53], ["n2", 1.50], ["n0", 1], ["d", 62.5], ["lam", 1300], ["pin", 1], ["pmin", 50], ["al", 0.35]];
    root.innerHTML = '<div class="fb-grid">' + F.map(function (x) { return '<label>' + T[x[0]] + '<input type="number" step="any" data-k="' + x[0] + '" value="' + x[1] + '"/></label>'; }).join("") +
      '</div><table class="tt fb-out"><tbody></tbody></table>';
    var body = root.querySelector("tbody");
    function upd() {
      var v = {}; Array.prototype.forEach.call(root.querySelectorAll("input"), function (i) { v[i.getAttribute("data-k")] = parseFloat(i.value); });
      var r = fibre(v.n1, v.n2, v.n0, v.d, v.lam), rows = [];
      if (!r.ok) { body.innerHTML = '<tr><td>' + T.bad + '</td></tr>'; return; }
      rows.push([T.thc, f(r.thc, 2) + T.deg]); rows.push([T.na, f(r.NA, 4)]);
      rows.push([T.tha, f(r.tha, 2) + T.deg + (r.guided ? "" : "  (" + T.cond + ")")]);
      if (r.V !== undefined) { rows.push([T.v, f(r.V, 2)]); rows.push([T.n, f(r.N, 0)]); rows.push([T.mode, r.single ? T.sm : T.mm]); }
      if (v.al > 0 && v.pin > 0 && v.pmin > 0) rows.push([T.lm, f(lmax(v.pin, v.pmin, v.al), 1) + " " + T.km]);
      body.innerHTML = rows.map(function (r) { return '<tr><td>' + r[0] + '</td><td class="m">' + r[1] + '</td></tr>'; }).join("");
    }
    root.addEventListener("input", upd); upd();
  }
  function initRay(root) {
    var en = root.getAttribute("data-lang") === "en";
    var T = en ? { n1: "n₁ (incident medium)", n2: "n₂ (second medium)", a: "Angle of incidence θi", r: "Refracted angle θr", tir: "TOTAL INTERNAL REFLECTION (θi > θc)", thc: "Critical angle θc", none: "none (n₁ ≤ n₂, no TIR possible)" }
                 : { n1: "n₁ (môi trường tới)", n2: "n₂ (môi trường thứ hai)", a: "Góc tới θi", r: "Góc khúc xạ θr", tir: "PHẢN XẠ TOÀN PHẦN (θi > θc)", thc: "Góc tới hạn θc", none: "không có (n₁ ≤ n₂, không thể phản xạ toàn phần)" };
    root.innerHTML = '<div class="fb-grid"><label>' + T.n1 + '<input type="number" step="0.01" data-k="n1" value="1.5"/></label><label>' + T.n2 + '<input type="number" step="0.01" data-k="n2" value="1.0"/></label>' +
      '<label>' + T.a + ': <b class="fb-av"></b><input type="range" min="0" max="89" value="30" data-k="a"/></label></div><canvas width="520" height="260" class="fb-cv"></canvas><p class="fb-st"></p>';
    var cv = root.querySelector("canvas"), ctx = cv.getContext("2d"), st = root.querySelector(".fb-st");
    function draw() {
      var v = {}; Array.prototype.forEach.call(root.querySelectorAll("input"), function (i) { v[i.getAttribute("data-k")] = parseFloat(i.value); });
      root.querySelector(".fb-av").textContent = v.a + "°";
      var W = cv.width, H = cv.height, cx = W / 2, cy = H / 2, L = 110;
      var dark = getComputedStyle(document.body).backgroundColor, fg = "#888";
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = "rgba(120,170,230,.18)"; ctx.fillRect(0, cy, W, H - cy);
      ctx.fillStyle = "rgba(230,200,120,.18)"; ctx.fillRect(0, 0, W, cy);
      ctx.strokeStyle = fg; ctx.setLineDash([5, 4]); ctx.beginPath(); ctx.moveTo(cx, 10); ctx.lineTo(cx, H - 10); ctx.stroke(); ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(W, cy); ctx.stroke();
      ctx.fillStyle = "#555"; ctx.font = "13px sans-serif"; ctx.fillText("n₂ = " + v.n2, 8, 20); ctx.fillText("n₁ = " + v.n1, 8, H - 10);
      var a = v.a * RAD, s = snell(v.n1, v.n2, v.a);
      // tia toi (tu duoi len) tu medium 1 (phia duoi)
      function ray(x0, y0, ang, col, len) { ctx.strokeStyle = col; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0 + len * Math.sin(ang), y0 - len * Math.cos(ang)); ctx.stroke(); }
      ctx.strokeStyle = "#d33"; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(cx - L * Math.sin(a), cy + L * Math.cos(a)); ctx.lineTo(cx, cy); ctx.stroke();
      ctx.strokeStyle = "#3a6"; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + L * Math.sin(a), cy + L * Math.cos(a)); ctx.stroke();
      if (s.refracted !== null) { var r = s.refracted * RAD; ctx.strokeStyle = "#27c"; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + L * Math.sin(r), cy - L * Math.cos(r)); ctx.stroke(); }
      st.innerHTML = (s.refracted === null ? "<b>" + T.tir + "</b>" : T.r + " = <b>" + s.refracted.toFixed(2) + "°</b>") + " &nbsp;·&nbsp; " + T.thc + ": " + (s.thc === null ? T.none : s.thc.toFixed(2) + "°");
    }
    root.addEventListener("input", draw); draw();
  }
  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll(".demo-fibre-calc"), initCalc);
    Array.prototype.forEach.call(document.querySelectorAll(".demo-fibre-ray"), initRay);
  });
})();
