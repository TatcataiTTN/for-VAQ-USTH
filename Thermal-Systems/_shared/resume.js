/* "Continue learning": module pages remember the last module visited (localStorage, this browser only); the home page shows a button that returns to it. */
(function () {
  var mark = document.getElementById('resume-mark'), L = (document.documentElement.lang || 'vi').slice(0, 2);
  try {
    if (mark) localStorage.setItem('prog:last', JSON.stringify({ href: location.pathname, title: mark.getAttribute('data-title'), t: Date.now() }));
    var box = document.getElementById('resume'); if (!box) return;
    var v = JSON.parse(localStorage.getItem('prog:last') || 'null'); if (!v || !v.href) return;
    var a = document.createElement('a'); a.className = 'btn'; a.href = v.href;
    a.textContent = (L === 'vi' ? '▶ Tiếp tục học: ' : '▶ Continue: ') + v.title; box.appendChild(a);
  } catch (e) { /* storage may be blocked */ }
})();
