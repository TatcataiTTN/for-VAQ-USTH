/* Slide strip: small thumbnails of the lecturer's original slides (with slide numbers); click opens a lightbox with the full image, arrows/Esc work. */
(function () {
  function open(list, i) {
    var box = document.createElement('div'); box.className = 'lightbox'; box.setAttribute('role', 'dialog');
    box.innerHTML = '<img alt=""><div class="lb-cap"></div><div class="lb-bar"><button type="button" data-d="-1">◀</button><button type="button" data-x="1">✕</button><button type="button" data-d="1">▶</button></div>';
    document.body.appendChild(box);
    var img = box.querySelector('img'), cap = box.querySelector('.lb-cap');
    function show() { var a = list[i]; img.src = a.href; img.alt = a.getAttribute('data-cap') || ''; cap.textContent = a.getAttribute('data-cap') || ''; }
    function close() { document.removeEventListener('keydown', key); box.remove(); }
    function key(e) { if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') { i = (i + list.length - 1) % list.length; show(); } else if (e.key === 'ArrowRight') { i = (i + 1) % list.length; show(); } }
    box.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b && b.dataset.d) { i = (i + list.length + +b.dataset.d) % list.length; show(); } else if (!b && e.target !== img) close(); else if (b && b.dataset.x) close(); });
    document.addEventListener('keydown', key); show();
  }
  document.querySelectorAll('.slidestrip').forEach(function (strip) {
    var list = Array.prototype.slice.call(strip.querySelectorAll('a'));
    list.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); open(list, i); }); });
  });
})();
