(function(){
  function apply(t){
    if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
    else document.documentElement.removeAttribute('data-theme');
  }
  document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('[data-set-theme]').forEach(function(btn){
      btn.addEventListener('click', function(){
        const t = btn.getAttribute('data-set-theme');
        try{ localStorage.setItem('site-theme', t); }catch(e){}
        apply(t);
      });
    });
  });
})();
