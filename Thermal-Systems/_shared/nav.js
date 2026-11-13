/* Header navigation: four groups (details/summary). Opening one closes the others; a click outside or Escape closes all. */
(function () {
  var groups = Array.prototype.slice.call(document.querySelectorAll('header.top details.navgrp, header.top details.menu'));
  groups.forEach(function (g) {
    g.addEventListener('toggle', function () { if (g.open) groups.forEach(function (o) { if (o !== g) o.open = false; }); });
  });
  document.addEventListener('click', function (e) { groups.forEach(function (g) { if (g.open && !g.contains(e.target)) g.open = false; }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') groups.forEach(function (g) { g.open = false; }); });
})();
