/* Ngân hàng câu hỏi: lọc theo mức/chủ đề, phân trang, chấm ngay + giải thích, làm lại từng câu/toàn bộ, xáo trộn, lưu tiến độ. */
(function(){
var root=document.getElementById('bank');if(!root)return;
var D=JSON.parse(document.getElementById('bank-data').textContent);
var KEY='bank:'+D.module;
var state={ans:{},ess:{},level:'all',topic:'all',origin:'all',tab:'mcq',page:0,onlyWrong:false,order:D.items.map(function(_,i){return i}),size:15};
try{var s=JSON.parse(localStorage.getItem(KEY)||'null');if(s){state.ans=s.ans||{};state.ess=s.ess||{}}}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify({ans:state.ans,ess:state.ess}));var a=0,c=0;D.items.forEach(function(it){var v=state.ans[it.id];if(v!==undefined){a++;if(v===it.correct)c++}});localStorage.setItem('prog:bank:'+D.module,JSON.stringify({t:Date.now(),a:a,c:c,n:D.items.length,e:Object.keys(state.ess).length,en:(D.essays||[]).length}))}catch(e){}}
var topics=[];D.items.forEach(function(i){if(topics.indexOf(i.topic)<0)topics.push(i.topic)});
function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!==undefined)e.textContent=txt;return e}
function stats(){var n=D.items.length,a=0,c=0;D.items.forEach(function(it){var v=state.ans[it.id];if(v!==undefined){a++;if(v===it.correct)c++}});return {n:n,a:a,c:c}}
function filtered(){return state.order.map(function(i){return D.items[i]}).filter(function(it){
  if(state.origin!=='all'&&it.origin!==state.origin)return false;if(state.level!=='all'&&String(it.level)!==state.level)return false;if(state.topic!=='all'&&it.topic!==state.topic)return false;
  if(state.onlyWrong){var v=state.ans[it.id];return v!==undefined&&v!==it.correct}return true})}
function render(){
  root.innerHTML='';var st=stats();
  var top=el('div','sim');top.innerHTML='<div class="simh">'+T.panel+'</div>';
  var row=el('div','row');
  function sel(lbl,opts,val,cb){var l=el('label');l.appendChild(document.createTextNode(lbl+' '));var s=el('select');opts.forEach(function(o){var op=el('option',null,o[1]);op.value=o[0];if(o[0]===val)op.selected=true;s.appendChild(op)});s.onchange=function(){cb(s.value)};l.appendChild(s);row.appendChild(l)}
  sel(T.source,[['all',T.all],['goc',T.orig+' ('+D.items.filter(function(i){return i.origin==='goc'}).length+')'],['bo_sung',T.gen+' ('+D.items.filter(function(i){return i.origin!=='goc'}).length+')']],state.origin,function(v){state.origin=v;state.page=0;render()});
  sel(T.level,[['all',T.all],['1',T.l1],['2',T.l2],['3',T.l3]],state.level,function(v){state.level=v;state.page=0;render()});
  sel(T.topic,[['all',T.all+' ('+D.items.length+')']].concat(topics.map(function(t){return [t,t+' ('+D.items.filter(function(i){return i.topic===t}).length+')']})),state.topic,function(v){state.topic=v;state.page=0;render()});
  var lw=el('label');var cb=el('input');cb.type='checkbox';cb.checked=state.onlyWrong;cb.onchange=function(){state.onlyWrong=cb.checked;state.page=0;render()};lw.appendChild(cb);lw.appendChild(document.createTextNode(T.onlyWrong));row.appendChild(lw);
  top.appendChild(row);
  var row2=el('div','row');
  var b1=el('button','btn alt',T.shuffle);b1.onclick=function(){var o=state.order.slice();for(var i=o.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=o[i];o[i]=o[j];o[j]=t}state.order=o;state.page=0;render()};
  var b2=el('button','btn',T.reset);b2.onclick=function(){if(confirm(T.confirmReset)){state.ans={};state.ess={};save();state.page=0;render()}};
  var b3=el('button','btn alt',T.origOrder);b3.onclick=function(){state.order=D.items.map(function(_,i){return i});state.page=0;render()};
  row2.appendChild(b1);row2.appendChild(b3);row2.appendChild(b2);top.appendChild(row2);
  var p=el('div','quiz-score',T.progress(st.a,st.n,st.c));top.appendChild(p);
  root.appendChild(top);
  var tabs=el('div','row');[['mcq',T.mcq+' ('+D.items.length+')'],['ess',T.ess+' ('+D.essays.length+')']].forEach(function(t){var b=el('button','btn'+(state.tab===t[0]?'':' alt'),t[1]);b.onclick=function(){state.tab=t[0];state.page=0;render()};tabs.appendChild(b)});root.appendChild(tabs);
  if(state.tab==='mcq')renderMcq();else renderEss();
}
function renderMcq(){
  var list=filtered(),pages=Math.max(1,Math.ceil(list.length/state.size));if(state.page>=pages)state.page=pages-1;
  root.appendChild(el('p','lead',T.showing(list.length,state.page+1,pages)));
  list.slice(state.page*state.size,(state.page+1)*state.size).forEach(function(it){
    var box=el('div','qitem');box.id=it.id;
    var head=el('div');head.innerHTML='<span class="tag">'+it.id+'</span><span class="tag">'+(T.kinds[it.kind]||'')+'</span><span class="tag">'+it.topic+'</span><span class="tag'+(it.level===3?' exam':'')+'">'+T.lvl+it.level+'</span>';box.appendChild(head);var sr=el('div',null,(it.origin==='goc'?T.origTag:T.genTag)+it.src);sr.style.fontSize='.78rem';sr.style.color='var(--muted)';box.appendChild(sr);
    var t=el('div','qtxt');t.textContent=it.q;t.style.marginTop='6px';t.style.fontWeight='600';box.appendChild(t);if(it.fig){var im=el('img','qfig');im.src=it.fig;im.alt=it.id;im.loading='lazy';box.appendChild(im)}
    var ex=el('div','explain');var chosen=state.ans[it.id];
    function showResult(c){
      var opts=box.querySelectorAll('.opt');[].forEach.call(opts,function(o){o.dataset.done='1'});
      opts[c].classList.add(c===it.correct?'correct':'wrong');if(c!==it.correct)opts[it.correct].classList.add('correct');
      ex.innerHTML='';var h=el('div',null,c===it.correct?T.correct:T.wrongAns+LETTERS[it.correct]+'.');h.style.fontWeight='800';ex.appendChild(h);ex.appendChild(document.createTextNode(it.explain));ex.classList.add('show')}
    it.opts.forEach(function(o,oi){var b=el('button','opt',LETTERS[oi]+'. '+o);b.type='button';b.onclick=function(){if(b.dataset.done)return;state.ans[it.id]=oi;save();showResult(oi);refreshStats()};box.appendChild(b)});
    box.appendChild(ex);
    var rb=el('button','btn alt',T.retryOne);rb.type='button';rb.style.marginTop='6px';rb.onclick=function(){delete state.ans[it.id];save();render()};box.appendChild(rb);
    root.appendChild(box);
    if(chosen!==undefined)showResult(chosen);
  });
  var nav=el('div','row');
  var pv=el('button','btn alt',T.prev);pv.disabled=state.page===0;pv.onclick=function(){state.page--;render();window.scrollTo(0,0)};
  var nx=el('button','btn alt',T.next);nx.disabled=state.page>=pages-1;nx.onclick=function(){state.page++;render();window.scrollTo(0,0)};
  nav.appendChild(pv);nav.appendChild(nx);root.appendChild(nav);
}
function refreshStats(){var st=stats();var p=root.querySelector('.quiz-score');if(p)p.textContent=T.progress(st.a,st.n,st.c)}
function renderEss(){
  var list=D.essays.filter(function(e){return (state.origin==='all'||e.origin===state.origin)&&(state.level==='all'||String(e.level)===state.level)&&(state.topic==='all'||e.topic===state.topic)});
  root.appendChild(el('p','lead',T.essIntro));
  list.forEach(function(e){
    var box=el('div','qitem');var head=el('div');head.innerHTML='<span class="tag">'+e.id+'</span><span class="tag">'+e.topic+'</span><span class="tag'+(e.level===3?' exam':'')+'">'+T.lvl+e.level+'</span>';box.appendChild(head);var sr=el('div',null,(e.origin==='goc'?T.origTag:T.genTag)+e.src);sr.style.fontSize='.78rem';sr.style.color='var(--muted)';box.appendChild(sr);
    var t=el('div','qtxt');t.textContent=e.q;t.style.fontWeight='600';t.style.marginTop='6px';box.appendChild(t);if(e.fig){var im=el('img','qfig');im.src=e.fig;im.alt=e.id;im.loading='lazy';box.appendChild(im)}
    var sol=el('div','explain');sol.textContent=e.sol;box.appendChild(sol);
    var sb=el('button','btn alt',T.showSol);sb.type='button';sb.onclick=function(){sol.classList.toggle('show');sb.textContent=sol.classList.contains('show')?T.hideSol:T.showSol};
    var mk=el('button','btn'+(state.ess[e.id]?'':' alt'),state.ess[e.id]?T.marked:T.mark);mk.type='button';mk.style.marginLeft='6px';mk.onclick=function(){if(state.ess[e.id])delete state.ess[e.id];else state.ess[e.id]=1;save();render()};
    box.appendChild(sb);box.appendChild(mk);root.appendChild(box)});
  var done=D.essays.filter(function(e){return state.ess[e.id]}).length;root.insertBefore(el('div','quiz-score',T.essDone(done,D.essays.length)),root.children[2]||null);
}
render();
})();
