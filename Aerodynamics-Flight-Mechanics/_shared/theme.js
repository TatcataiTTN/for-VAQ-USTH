(function(){
  var THEMES = ['light', 'dark', 'sepia', 'ocean'];
  function apply(t){
    if (t && t !== 'light' && THEMES.indexOf(t) !== -1) document.documentElement.setAttribute('data-theme', t);
    else document.documentElement.setAttribute('data-theme', 'light');
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
