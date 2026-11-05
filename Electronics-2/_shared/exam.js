/* Timed practice sets: pick set, countdown, submit -> score + explanation per question, retry. */
(function(){
var root=document.getElementById('exam');if(!root)return;
var D=JSON.parse(document.getElementById('exam-data').textContent);
var MIN=D.minutes||30;var cur=0,timer=null,left=MIN*60,submitted=false,ans={};
function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!==undefined)e.textContent=txt;return e}
function fmt(s){return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}
function render(){
  clearInterval(timer);root.innerHTML='';
  var tabs=el('div','row');D.sets.forEach(function(s,i){var b=el('button','btn'+(i===cur?'':' alt'),(s.name||T.set+' '+(i+1)));b.onclick=function(){cur=i;left=MIN*60;submitted=false;ans={};render()};tabs.appendChild(b)});root.appendChild(tabs);
  var set=D.sets[cur].items;
  var bar=el('div','sim');var hh=el('div','simh',(D.sets[cur].name||T.set+' '+(cur+1))+' · '+set.length+' '+T.qs+' · '+MIN+' '+T.minutes);bar.appendChild(hh);
  var tm=el('span','quiz-score',T.timeLeft+fmt(left));bar.appendChild(tm);
  var sb=el('button','btn',T.submit);sb.style.marginLeft='10px';sb.onclick=function(){submit()};bar.appendChild(sb);
  var rb=el('button','btn alt',T.retrySet);rb.style.marginLeft='6px';rb.onclick=function(){left=MIN*60;submitted=false;ans={};render()};bar.appendChild(rb);
  root.appendChild(bar);
  set.forEach(function(q,qi){
    var box=el('div','qitem');var t=el('div','qtxt');t.style.fontWeight='600';t.textContent=(qi+1)+'. '+q.q;box.appendChild(t);
    var meta=el('div','srcnote','📎 '+q.src);box.appendChild(meta);if(q.fig){var im=el('img','qfig');im.src=q.fig;im.loading='lazy';box.appendChild(im)}
    q.opts.forEach(function(o,oi){var b=el('button','opt',LETTERS[oi]+'. '+o);b.type='button';
      b.onclick=function(){if(submitted)return;ans[qi]=oi;[].forEach.call(box.querySelectorAll('.opt'),function(x){x.style.outline=''});b.style.outline='2px solid var(--accent)'};box.appendChild(b)});
    var ex=el('div','explain');box.appendChild(ex);root.appendChild(box)});
  var res=el('div','quiz-score');res.id='res';root.appendChild(res);
  timer=setInterval(function(){left--;tm.textContent=T.timeLeft+fmt(left);if(left<=0){submit()}},1000);
}
function submit(){
  if(submitted)return;submitted=true;clearInterval(timer);var set=D.sets[cur].items,score=0;
  set.forEach(function(q,qi){var box=root.querySelectorAll('.qitem')[qi],opts=box.querySelectorAll('.opt');[].forEach.call(opts,function(o){o.dataset.done='1';o.style.outline=''});
    var ok=ans[qi]===q.correct;if(ok)score++;
    opts[q.correct].classList.add('correct');if(ans[qi]!==undefined&&!ok)opts[ans[qi]].classList.add('wrong');
    var ex=box.querySelector('.explain');ex.innerHTML='';var h=el('div',null,ok?T.ok:(ans[qi]===undefined?T.noAns:T.bad)+(ok?'':LETTERS[q.correct]));h.style.fontWeight='800';ex.appendChild(h);ex.appendChild(document.createTextNode(q.explain));ex.classList.add('show')});
  try{localStorage.setItem('prog:exam:'+cur,JSON.stringify({t:Date.now(),name:D.sets[cur].name||String(cur+1),score:score,n:set.length,secs:MIN*60-left}))}catch(e){}
  var r=document.getElementById('res');r.textContent=T.result(score,set.length);r.scrollIntoView({behavior:'smooth',block:'center'});
}
render();
})();
