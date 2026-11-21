/* Loc bang thuat ngu theo o tim kiem (khong phan biet hoa thuong, bo dau tieng Viet). */
(function () {
  var q = document.getElementById('gloss-q'), t = document.getElementById('gloss'); if (!q || !t) return;
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd'); }
  var rows = Array.prototype.slice.call(t.rows, 1).map(function (r) { return [r, norm(r.textContent)]; });
  q.addEventListener('input', function () { var k = norm(q.value.trim()); rows.forEach(function (x) { x[0].style.display = !k || x[1].indexOf(k) >= 0 ? '' : 'none'; }); });
})();
