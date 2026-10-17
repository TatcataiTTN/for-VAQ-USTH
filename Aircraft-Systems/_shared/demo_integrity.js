/* Demo 07: toàn vẹn dữ liệu phần mềm (checksum 8-bit và CRC-8) + bộ chọn mức DAL.
   Chạy 100% trong trình duyệt. Hàm thuần được xuất cho kiểm thử bằng Node. */
(function () {
  function checksum8(bytes) { var s = 0; for (var i = 0; i < bytes.length; i++) s = (s + bytes[i]) & 0xFF; return s; }
  function crc8(bytes) { // đa thức x^8 + x^2 + x + 1 (0x07), khởi tạo 0, không đảo bit
    var c = 0;
    for (var i = 0; i < bytes.length; i++) {
      c ^= bytes[i];
      for (var b = 0; b < 8; b++) c = (c & 0x80) ? (((c << 1) ^ 0x07) & 0xFF) : ((c << 1) & 0xFF);
    }
    return c;
  }
  function parseHex(s) {
    var t = (s || "").replace(/[^0-9a-fA-F]/g, "");
    if (t.length % 2) t = t.slice(0, -1);
    var out = []; for (var i = 0; i < t.length; i += 2) out.push(parseInt(t.substr(i, 2), 16));
    return out;
  }
  function toHex(arr) { return arr.map(function (x) { return ("0" + x.toString(16)).slice(-2).toUpperCase(); }).join(" "); }
  function h2(x) { return "0x" + ("0" + x.toString(16)).slice(-2).toUpperCase(); }
  var DAL = {
    A: { p: "< 10⁻⁹", ex: "AHRS, GPS/ILS, SATNAV, VOR/ADF", tr: ["Trace ĐỎ (chỉ mức A): kiến trúc phần mềm ↔ yêu cầu cấp cao; mã nguồn ↔ mã đối tượng thực thi", "Trace TÍM (A, B, C): yêu cầu cấp cao ↔ yêu cầu cấp thấp; yêu cầu cấp thấp ↔ mã nguồn; yêu cầu cấp thấp ↔ test case", "Trace XANH (A đến D): yêu cầu hệ thống ↔ yêu cầu cấp cao; yêu cầu cấp cao ↔ test case; test case ↔ test procedure ↔ test result"] },
    B: { p: "10⁻⁹ … 10⁻⁷", ex: "TCAS, ADS-B transponder, flight displays", tr: ["Trace TÍM (A, B, C): yêu cầu cấp cao ↔ yêu cầu cấp thấp; yêu cầu cấp thấp ↔ mã nguồn; yêu cầu cấp thấp ↔ test case", "Trace XANH (A đến D): yêu cầu hệ thống ↔ yêu cầu cấp cao; yêu cầu cấp cao ↔ test case; test case ↔ test procedure ↔ test result"] },
    C: { p: "10⁻⁷ … 10⁻⁵", ex: "DME, VHF voice", tr: ["Giống mức B: trace TÍM và trace XANH (mức B và C có cùng tập trace theo hình 13-1)"] },
    D: { p: "> 10⁻⁵", ex: "CMC/CFDIU, data loader, weather radar", tr: ["Chỉ trace XANH (A đến D): yêu cầu hệ thống ↔ yêu cầu cấp cao; yêu cầu cấp cao ↔ test case; test case ↔ test procedure ↔ test result"] },
    E: { p: "không áp dụng", ex: "In-flight entertainment", tr: ["Không yêu cầu trace"] }
  };
  if (typeof module !== "undefined") module.exports = { checksum8: checksum8, crc8: crc8, parseHex: parseHex, toHex: toHex };
  if (typeof document === "undefined") return;

  function init(root) {
    var en = root.getAttribute("data-lang") === "en";
    var T = en ? {
      ok: "match (not detected)", bad: "MISMATCH (detected)", stored: "Stored when the file was released",
      now: "Recomputed now", sum: "8-bit checksum", crc: "CRC-8 (poly 0x07)", file: "File content (hex bytes)",
      flip: "Flip one bit", swap: "Swap two bytes", comp: "Two errors that cancel (+1 / −1)", reset: "Restore original",
      verdict_chk: "Checksum says: ", verdict_crc: "CRC says: ", note: "Try 'Swap two bytes' or 'Two errors that cancel': the simple checksum cannot see them, the CRC does. Neither method is completely fool-proof (Tooley 13.4).",
      lvl: "Software level (DO-178C)", pf: "Failure probability per flight hour", ex: "Typical applications (Tooley Table 13.2)", tr: "Required traceability (lecture Figure 13-1)"
    } : {
      ok: "khớp (không phát hiện)", bad: "LỆCH (phát hiện được)", stored: "Giá trị lưu lúc phát hành tệp",
      now: "Tính lại bây giờ", sum: "Checksum 8 bit", crc: "CRC-8 (đa thức 0x07)", file: "Nội dung tệp (các byte hex)",
      flip: "Lật 1 bit", swap: "Đổi chỗ 2 byte", comp: "Hai lỗi triệt tiêu nhau (+1 / −1)", reset: "Khôi phục bản gốc",
      verdict_chk: "Checksum báo: ", verdict_crc: "CRC báo: ", note: "Thử \"Đổi chỗ 2 byte\" hoặc \"Hai lỗi triệt tiêu nhau\": checksum đơn giản không thấy, CRC thì thấy. Không phương pháp nào tuyệt đối an toàn (Tooley 13.4).",
      lvl: "Mức phần mềm (DO-178C)", pf: "Xác suất hỏng mỗi giờ bay", ex: "Ứng dụng điển hình (Tooley Bảng 13.2)", tr: "Trace bắt buộc (hình 13-1 của bài giảng)"
    };
    var orig = parseHex(root.getAttribute("data-bytes")), cur = orig.slice();
    var s0 = checksum8(orig), c0 = crc8(orig);
    root.innerHTML =
      '<div class="di-row"><label>' + T.file + '</label><input class="di-in" spellcheck="false"/></div>' +
      '<div class="di-btns"><button data-a="flip">' + T.flip + '</button><button data-a="swap">' + T.swap + '</button><button data-a="comp">' + T.comp + '</button><button data-a="reset">' + T.reset + '</button></div>' +
      '<table class="tt di-t"><thead><tr><th></th><th>' + T.stored + '</th><th>' + T.now + '</th><th></th></tr></thead><tbody>' +
      '<tr><td>' + T.sum + '</td><td class="m">' + h2(s0) + '</td><td class="m di-s"></td><td class="di-vs"></td></tr>' +
      '<tr><td>' + T.crc + '</td><td class="m">' + h2(c0) + '</td><td class="m di-c"></td><td class="di-vc"></td></tr></tbody></table>' +
      '<p class="di-note"><i>' + T.note + '</i></p>';
    var inp = root.querySelector(".di-in");
    function show() {
      inp.value = toHex(cur);
      var s = checksum8(cur), c = crc8(cur);
      root.querySelector(".di-s").textContent = h2(s); root.querySelector(".di-c").textContent = h2(c);
      var vs = root.querySelector(".di-vs"), vc = root.querySelector(".di-vc");
      vs.textContent = s === s0 ? T.ok : T.bad; vs.className = "di-vs " + (s === s0 ? "warn" : "good");
      vc.textContent = c === c0 ? T.ok : T.bad; vc.className = "di-vc " + (c === c0 ? "warn" : "good");
      if (cur.join() === orig.join()) { vs.textContent = vc.textContent = "="; vs.className = vc.className = ""; }
    }
    inp.addEventListener("input", function () { cur = parseHex(inp.value); var s = checksum8(cur), c = crc8(cur);
      root.querySelector(".di-s").textContent = h2(s); root.querySelector(".di-c").textContent = h2(c);
      var vs = root.querySelector(".di-vs"), vc = root.querySelector(".di-vc");
      vs.textContent = s === s0 ? T.ok : T.bad; vc.textContent = c === c0 ? T.ok : T.bad; });
    root.querySelector(".di-btns").addEventListener("click", function (e) {
      var a = e.target.getAttribute("data-a"); if (!a) return;
      cur = orig.slice();
      if (a === "flip") cur[Math.floor(cur.length / 2)] ^= 0x04;
      if (a === "swap") { var i = 1, j = cur.length - 2; var t = cur[i]; cur[i] = cur[j]; cur[j] = t; if (cur[i] === cur[j]) cur[i] ^= 0; }
      if (a === "comp") { cur[0] = (cur[0] + 1) & 0xFF; cur[cur.length - 1] = (cur[cur.length - 1] - 1) & 0xFF; }
      show();
    });
    show();
  }
  function initDal(root) {
    var en = root.getAttribute("data-lang") === "en";
    var L = en ? { lvl: "Software level (DO-178C)", pf: "Failure probability per flight hour", ex: "Typical applications (Tooley Table 13.2)", tr: "Required traceability (lecture Figure 13-1)" }
               : { lvl: "Mức phần mềm (DO-178C)", pf: "Xác suất hỏng mỗi giờ bay", ex: "Ứng dụng điển hình (Tooley Bảng 13.2)", tr: "Trace bắt buộc (hình 13-1 của bài giảng)" };
    var EN_TR = { A: ["RED traces (level A only): software architecture ↔ high-level requirements; source code ↔ executable object code", "PURPLE traces (A, B, C): high-level ↔ low-level requirements; low-level requirements ↔ source code; low-level requirements ↔ test cases", "GREEN traces (A to D): system requirements ↔ high-level requirements; high-level requirements ↔ test cases; test cases ↔ test procedures ↔ test results"],
                  B: ["PURPLE traces (A, B, C): high-level ↔ low-level requirements; low-level requirements ↔ source code; low-level requirements ↔ test cases", "GREEN traces (A to D): system requirements ↔ high-level requirements; high-level requirements ↔ test cases; test cases ↔ test procedures ↔ test results"],
                  C: ["Same as level B: PURPLE and GREEN traces (levels B and C share the same set in Figure 13-1)"], D: ["GREEN traces only (A to D): system requirements ↔ high-level requirements; high-level requirements ↔ test cases; test cases ↔ test procedures ↔ test results"], E: ["No traceability required"] };
    root.innerHTML = '<div class="di-row"><label>' + L.lvl + '</label> <select class="dal-sel">' + Object.keys(DAL).map(function (k) { return "<option>" + k + "</option>"; }).join("") + '</select></div><div class="dal-out"></div>';
    var sel = root.querySelector(".dal-sel"), out = root.querySelector(".dal-out");
    function upd() { var d = DAL[sel.value]; var tr = en ? EN_TR[sel.value] : d.tr;
      out.innerHTML = '<p><b>' + L.pf + ':</b> ' + d.p + '</p><p><b>' + L.ex + ':</b> ' + d.ex + '</p><p><b>' + L.tr + ':</b></p><ul>' + tr.map(function (x) { return "<li>" + x + "</li>"; }).join("") + '</ul>'; }
    sel.addEventListener("change", upd); upd();
  }
  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll(".demo-integrity"), init);
    Array.prototype.forEach.call(document.querySelectorAll(".demo-dal"), initDal);
  });
})();
