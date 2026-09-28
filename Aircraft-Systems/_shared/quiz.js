(function(){
  const LANG = document.documentElement.lang === 'en' ? 'en' : 'vi';
  const L = {
    vi: {restart: '↺ Làm lại từ đầu', score: 'Điểm', confirm: 'Bạn đã trả lời một số câu — làm lại từ đầu?'},
    en: {restart: '↺ Restart', score: 'Score', confirm: 'You have answered some questions — restart from the beginning?'}
  }[LANG];

  document.querySelectorAll('.quiz').forEach(function(quizEl){
    const dataEl = quizEl.querySelector('script[type="application/json"]');
    if (!dataEl) return;
    const Q = JSON.parse(dataEl.textContent);
    const root = quizEl.querySelector('.quiz-root') || (function(){
      const r = document.createElement('div'); r.className = 'quiz-root'; quizEl.appendChild(r); return r;
    })();
    let scoreBar = quizEl.querySelector('.quiz-score');
    if (!scoreBar){ scoreBar = document.createElement('div'); scoreBar.className='quiz-score'; quizEl.insertBefore(scoreBar, root); }
    let answered = 0, score = 0;

    function updateScore(){
      scoreBar.textContent = `${L.score}: ${score}/${Q.items.length}` + (answered < Q.items.length ? ` (${answered}/${Q.items.length} đã làm)`.replace('đã làm', LANG==='en' ? 'answered' : 'đã làm') : '');
    }

    function build(){
      root.innerHTML = '';
      score = 0; answered = 0;
      Q.items.forEach((q, qi) => {
        const box = document.createElement('div'); box.className = 'qitem';
        const head = document.createElement('div');
        head.innerHTML = `<b>${qi+1}. ${q.q}</b>`;
        if (q.src) { const s = document.createElement('div'); s.className='pill'; s.style.marginTop='4px'; s.textContent = q.src; head.appendChild(s); }
        box.appendChild(head);
        if (q.img) {
          const img = document.createElement('img');
          img.src = q.img; img.alt = q.src || ('Question ' + (qi+1));
          img.style.cssText = 'max-width:100%;max-height:340px;display:block;margin:10px 0;border:1px solid var(--border);border-radius:8px;background:#fff;padding:6px';
          box.appendChild(img);
        }
        const explain = document.createElement('div');
        explain.className = 'explain'; explain.textContent = q.explain || '';
        q.opts.forEach((opt, oi) => {
          const b = document.createElement('button'); b.type='button'; b.className = 'opt'; b.textContent = opt;
          b.addEventListener('click', () => {
            if (box.dataset.done) return;
            box.dataset.done = '1'; answered++;
            [...box.querySelectorAll('.opt')].forEach(x => x.disabled = true);
            const correct = oi === q.correct;
            b.classList.add(correct ? 'correct' : 'wrong');
            if (!correct) box.querySelectorAll('.opt')[q.correct]?.classList.add('correct');
            explain.classList.add('show');
            if (correct) score++;
            updateScore();
          });
          box.appendChild(b);
        });
        box.appendChild(explain); root.appendChild(box);
      });
      updateScore();
    }
    let restartBtn = quizEl.querySelector('.quiz-restart');
    if (!restartBtn){
      restartBtn = document.createElement('button'); restartBtn.type='button'; restartBtn.className='quiz-restart';
      restartBtn.textContent = L.restart;
      restartBtn.addEventListener('click', () => {
        if (answered > 0 && !window.confirm(L.confirm)) return;
        build();
      });
      quizEl.appendChild(restartBtn);
    }
    build();
  });
})();
