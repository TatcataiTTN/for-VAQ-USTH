/* Quick quiz in a module page: click = graded at once, explanation always shown, retry per question / all. Plain text only. */
(function(){
  document.querySelectorAll('script.quiz-data').forEach(function(dataEl){
    var Q=JSON.parse(dataEl.textContent);var root=document.getElementById(dataEl.getAttribute('data-root'));if(!root)return;
    var key='quiz:'+location.pathname+':'+dataEl.getAttribute('data-root');
    function build(){
      root.innerHTML='';var score=0,done=0;
      var bar=document.createElement('div');bar.className='quiz-score';root.appendChild(bar);
      function upd(){bar.textContent=T.score+': '+score+'/'+Q.items.length+'  ('+done+'/'+Q.items.length+' '+T.done+')';try{localStorage.setItem(key,JSON.stringify({score:score,done:done,n:Q.items.length}))}catch(e){}}
      Q.items.forEach(function(q,qi){
        var box=document.createElement('div');box.className='qitem';
        var t=document.createElement('div');t.className='qtxt';var b=document.createElement('b');b.textContent=(qi+1)+'. ';t.appendChild(b);t.appendChild(document.createTextNode(q.q));box.appendChild(t);
        if(q.fig){var im=document.createElement('img');im.className='qfig';im.src=q.fig;im.loading='lazy';box.appendChild(im)}if(q.src){var s=document.createElement('div');s.className='srcnote';s.textContent='📎 '+q.src;box.appendChild(s)}
        var ex=document.createElement('div');ex.className='explain';ex.textContent=q.explain||'';
        q.opts.forEach(function(opt,oi){
          var btn=document.createElement('button');btn.type='button';btn.className='opt';btn.textContent=LETTERS[oi]+'. '+opt;
          btn.addEventListener('click',function(){
            if(btn.dataset.done)return;
            [].forEach.call(box.querySelectorAll('.opt'),function(x){x.dataset.done='1'});
            var ok=oi===q.correct;btn.classList.add(ok?'correct':'wrong');
            if(!ok)box.querySelectorAll('.opt')[q.correct].classList.add('correct');
            var head=document.createElement('div');head.style.fontWeight='800';head.textContent=ok?T.correct:T.wrongAns+LETTERS[q.correct]+'.';
            ex.insertBefore(head,ex.firstChild);ex.classList.add('show');if(ok)score++;done++;box.dataset.ok=ok?'1':'0';upd();
          });box.appendChild(btn);
        });
        var rb=document.createElement('button');rb.type='button';rb.className='btn alt';rb.style.marginTop='6px';rb.textContent=T.retryOne;
        rb.addEventListener('click',function(){
          if(!box.querySelector('.opt[data-done]'))return;
          if(box.dataset.ok==='1')score--;done--;delete box.dataset.ok;
          [].forEach.call(box.querySelectorAll('.opt'),function(x){x.classList.remove('correct','wrong');delete x.dataset.done});
          ex.classList.remove('show');ex.textContent=q.explain||'';upd();});
        box.appendChild(ex);box.appendChild(rb);root.appendChild(box);
      });
      var r=document.createElement('button');r.type='button';r.className='btn';r.textContent=T.retryAll;
      r.addEventListener('click',function(){if(done>0&&!confirm(T.confirmAll))return;build();window.scrollTo({top:root.getBoundingClientRect().top+window.scrollY-70,behavior:'smooth'})});root.appendChild(r);
      upd();
    }
    build();
  });
})();
