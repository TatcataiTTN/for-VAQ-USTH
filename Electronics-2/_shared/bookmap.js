/* Book map filters: module select, 'assigned only' checkbox and title search. Rows carry data-mods and data-text. */
(function () {
  var sel = document.getElementById('bm-mod'), only = document.getElementById('bm-only'), q = document.getElementById('bm-q'), none = document.getElementById('bm-none');
  if (!sel || !only || !q) return;
  function apply() {
    var m = sel.value, o = only.checked, s = (q.value || '').trim().toLowerCase(), filtering = !!(m || o || s), total = 0;
    document.querySelectorAll('details.bm-ch').forEach(function (d) {
      var vis = 0;
      d.querySelectorAll('tbody tr').forEach(function (tr) {
        if (tr.classList.contains('bm-sep')) return;
        var mods = (tr.getAttribute('data-mods') || '').split(' ').filter(Boolean), ok = true;
        if (m && mods.indexOf(m) < 0) ok = false;
        if (o && !mods.length) ok = false;
        if (s && (tr.getAttribute('data-text') || '').indexOf(s) < 0) ok = false;
        tr.classList.toggle('bm-hide', !ok); if (ok) vis++;
      });
      d.querySelectorAll('tr.bm-sep').forEach(function (tr) { tr.classList.toggle('bm-hide', filtering && !vis); });
      d.classList.toggle('bm-hide', filtering && !vis);
      if (filtering && vis) d.open = true;
      total += vis;
    });
    if (none) none.hidden = !(filtering && total === 0);
  }
  sel.addEventListener('change', apply); only.addEventListener('change', apply); q.addEventListener('input', apply);
})();
