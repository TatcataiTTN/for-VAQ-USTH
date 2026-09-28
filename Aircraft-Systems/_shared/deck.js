document.querySelectorAll('.mdeck').forEach(function(deck){
  const slides = [...deck.querySelectorAll('.mdeck-slide')];
  const bar = deck.querySelector('.mdeck-bar');
  const prevBtn = bar.querySelector('.mdeck-prev'), nextBtn = bar.querySelector('.mdeck-next');
  const count = bar.querySelector('.mdeck-count'), dotsWrap = bar.querySelector('.mdeck-dots');
  const fsBtn = bar.querySelector('.mdeck-fs');
  let i = 0;
  slides.forEach((s, idx) => {
    const d = document.createElement('button'); d.type = 'button';
    d.setAttribute('aria-label', 'slide ' + (idx+1));
    d.addEventListener('click', () => go(idx));
    dotsWrap.appendChild(d);
  });
  const dots = [...dotsWrap.children];
  function render(){
    slides.forEach((s, idx) => s.classList.toggle('active', idx === i));
    dots.forEach((d, idx) => d.classList.toggle('on', idx === i));
    count.textContent = (i+1) + '/' + slides.length;
    prevBtn.disabled = i === 0; nextBtn.disabled = i === slides.length - 1;
    fitSoon();
  }
  function isFs(){ return document.fullscreenElement === deck || document.webkitFullscreenElement === deck; }
  function fit(){
    slides.forEach(s => { s.style.fontSize = ''; s.style.height = ''; });
    const s = slides[i], fs = isFs();
    let lo = 16, hi = fs ? 40 : 28;
    if (!fs) s.style.height = Math.max(380, Math.min(720, window.innerHeight * 0.62)) + 'px';
    if (fs) lo = 13;
    while (hi - lo > 0.5) {
      const mid = (lo + hi) / 2;
      s.style.fontSize = mid + 'px';
      if (s.scrollHeight <= s.clientHeight + 1) lo = mid; else hi = mid;
    }
    s.style.fontSize = lo + 'px';
    if (!fs) s.style.height = '';
  }
  function fitSoon(){ requestAnimationFrame(() => requestAnimationFrame(fit)); }
  function go(n){ i = Math.max(0, Math.min(slides.length - 1, n)); render(); }
  prevBtn.addEventListener('click', () => go(i - 1));
  nextBtn.addEventListener('click', () => go(i + 1));
  deck.tabIndex = 0;
  deck.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') go(i + 1);
    if (e.key === 'ArrowLeft') go(i - 1);
  });
  if (fsBtn) fsBtn.addEventListener('click', () => {
    if (!document.fullscreenElement) deck.requestFullscreen?.(); else document.exitFullscreen?.();
  });
  deck.addEventListener('toggle', fitSoon, true);
  document.addEventListener('fullscreenchange', fitSoon);
  document.addEventListener('webkitfullscreenchange', fitSoon);
  window.addEventListener('resize', fitSoon);
  render();
});
