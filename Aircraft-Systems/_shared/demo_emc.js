/* Demo 09: máy tính dB/dBm, tổng hợp Fourier của sóng vuông, tụ thực (ESL/ESR) và tần số cộng hưởng. 100% trong trình duyệt. */
(function () {
  function dbPower(p2, p1) { return 10 * Math.log10(p2 / p1); }
  function dbAmp(a2, a1) { return 20 * Math.log10(a2 / a1); }
  function dbm(pW) { return 10 * Math.log10(pW / 1e-3); }
  function fromDbm(d) { return 1e-3 * Math.pow(10, d / 10); }
  function squareAmp(n, V) { return n % 2 === 1 ? V / n : 0; }       // dạng của bài giảng/Tooley: V/n cho hài lẻ
  function fr(L, C) { return 1 / (2 * Math.PI * Math.sqrt(L * C)); }
  function zcap(f, C, L, R) { var w = 2 * Math.PI * f, x = w * L - 1 / (w * C); return Math.sqrt(R * R + x * x); }
  if (typeof module !== "undefined") module.exports = { dbPower: dbPower, dbAmp: dbAmp, dbm: dbm, fromDbm: fromDbm, squareAmp: squareAmp, fr: fr, zcap: zcap };
  if (typeof document === "undefined") return;
  function num(root, k) { return parseFloat(root.querySelector('[data-k="' + k + '"]').value); }
  function f(x, d) { return isFinite(x) ? x.toFixed(d) : "-"; }
  function db(root) {
    var en = root.getAttribute("data-lang") === "en";
    var T = en ? { p: "Power (W)", g1: "Stage 1 gain (dB)", g2: "Stage 2 gain (dB)", l: "Cable/filter loss (dB)", dbm: "Input level", out: "Output level", tot: "Total gain", pw: "Output power", amp: "Voltage ratio for the total gain (×)", pr: "Power ratio (×)" }
                 : { p: "Công suất vào (W)", g1: "Khuếch đại tầng 1 (dB)", g2: "Khuếch đại tầng 2 (dB)", l: "Tổn hao cáp/bộ lọc (dB)", dbm: "Mức vào", out: "Mức ra", tot: "Tổng độ lợi", pw: "Công suất ra", amp: "Tỉ số điện áp ứng với tổng độ lợi (lần)", pr: "Tỉ số công suất (lần)" };
    root.innerHTML = '<div class="fb-grid">' + [["p", 0.001], ["g1", 10], ["g2", 6], ["l", 3]].map(function (x) { return '<label>' + T[x[0]] + '<input type="number" step="any" data-k="' + x[0] + '" value="' + x[1] + '"/></label>'; }).join("") + '</div><table class="tt"><tbody class="o"></tbody></table>';
    var o = root.querySelector(".o");
    function u() {
      var p = num(root, "p"), g = num(root, "g1") + num(root, "g2") - num(root, "l"), din = dbm(p), pout = p * Math.pow(10, g / 10);
      o.innerHTML = [[T.dbm, f(din, 2) + " dBm"], [T.tot, f(g, 2) + " dB"], [T.out, f(din + g, 2) + " dBm"], [T.pw, pout.toPrecision(4) + " W"], [T.pr, f(Math.pow(10, g / 10), 3)], [T.amp, f(Math.pow(10, g / 20), 3)]]
        .map(function (r) { return '<tr><td>' + r[0] + '</td><td class="m">' + r[1] + '</td></tr>'; }).join("");
    }
    root.addEventListener("input", u); u();
  }
  function fourier(root) {
    var en = root.getAttribute("data-lang") === "en";
    var T = en ? { n: "Highest harmonic included", note: "Each added odd harmonic (V/n) sharpens the edges. The sharper the edge, the more high-frequency content, hence more EMI." } : { n: "Hài bậc cao nhất được cộng", note: "Mỗi hài lẻ (V/n) thêm vào làm cạnh xung dốc hơn. Cạnh càng dốc thì nội dung tần cao càng nhiều, nên EMI càng lớn." };
    root.innerHTML = '<div class="fb-grid"><label>' + T.n + ': <b class="nv"></b><input type="range" min="1" max="41" step="2" value="7" data-k="n"/></label></div><canvas width="560" height="300" class="fb-cv"></canvas><p class="di-note"><i>' + T.note + '</i></p>';
    var cv = root.querySelector("canvas"), ctx = cv.getContext("2d");
    function d() {
      var N = num(root, "n"); root.querySelector(".nv").textContent = N;
      var W = cv.width, H = cv.height; ctx.clearRect(0, 0, W, H);
      var mid = 100, A = 70; ctx.strokeStyle = "#999"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(0, mid); ctx.lineTo(W, mid); ctx.stroke();
      ctx.strokeStyle = "#c33"; ctx.lineWidth = 2; ctx.beginPath();
      for (var x = 0; x <= W; x++) { var t = x / W * 2 * 2 * Math.PI, y = 0; for (var n = 1; n <= N; n += 2) y += Math.sin(n * t) / n; y *= 4 / Math.PI; x ? ctx.lineTo(x, mid - A * y) : ctx.moveTo(x, mid - A * y); }
      ctx.stroke();
      ctx.fillStyle = "#37a"; var base = H - 10, bw = Math.max(6, 520 / (N + 1) * .6);
      for (var k = 1; k <= N; k += 2) { var h = 90 * squareAmp(k, 1), bx = 20 + (k - 1) / 40 * 520; ctx.fillRect(bx, base - h, 7, h); }
      ctx.fillStyle = "#555"; ctx.font = "12px sans-serif"; ctx.fillText("f, 3f, 5f, ... (V/n)", 20, 190);
    }
    root.addEventListener("input", d); d();
  }
  function cap(root) {
    var en = root.getAttribute("data-lang") === "en";
    var T = en ? { C: "C (nF)", L: "ESL (nH)", R: "ESR (mΩ)", fr: "Resonant frequency f_r", zmin: "Impedance at f_r (≈ ESR)", z10: "|Z| at 10·f_r", z01: "|Z| at 0.1·f_r", ind: "Above f_r the part behaves as an inductor." }
                 : { C: "C (nF)", L: "ESL (nH)", R: "ESR (mΩ)", fr: "Tần số cộng hưởng f_r", zmin: "Trở kháng tại f_r (≈ ESR)", z10: "|Z| tại 10·f_r", z01: "|Z| tại 0,1·f_r", ind: "Trên f_r linh kiện hoạt động như cuộn cảm." };
    root.innerHTML = '<div class="fb-grid">' + [["C", 100], ["L", 10], ["R", 50]].map(function (x) { return '<label>' + T[x[0]] + '<input type="number" step="any" data-k="' + x[0] + '" value="' + x[1] + '"/></label>'; }).join("") + '</div><table class="tt"><tbody class="o"></tbody></table><p class="di-note"><i>' + T.ind + '</i></p>';
    var o = root.querySelector(".o");
    function u() {
      var C = num(root, "C") * 1e-9, L = num(root, "L") * 1e-9, R = num(root, "R") * 1e-3, F = fr(L, C);
      o.innerHTML = [[T.fr, (F / 1e6).toFixed(3) + " MHz"], [T.zmin, (zcap(F, C, L, R) * 1e3).toFixed(1) + " mΩ"], [T.z01, zcap(.1 * F, C, L, R).toFixed(3) + " Ω"], [T.z10, zcap(10 * F, C, L, R).toFixed(3) + " Ω"]]
        .map(function (r) { return '<tr><td>' + r[0] + '</td><td class="m">' + r[1] + '</td></tr>'; }).join("");
    }
    root.addEventListener("input", u); u();
  }
  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll(".demo-emc-db"), db);
    Array.prototype.forEach.call(document.querySelectorAll(".demo-emc-fourier"), fourier);
    Array.prototype.forEach.call(document.querySelectorAll(".demo-emc-cap"), cap);
  });
})();
