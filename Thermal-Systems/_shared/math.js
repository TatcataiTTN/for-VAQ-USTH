/* KaTeX auto-render for the whole page, including content that scripts insert later (quiz, bank, exam, written practice).
   Delimiters: $$..$$ and \[..\] (display), $..$ and \(..\) (inline).  <pre>, <code>, textarea and elements with class "no-math" are skipped. */
(function () {
  var opts = {
    delimiters: [{ left: '$$', right: '$$', display: true }, { left: '\\[', right: '\\]', display: true },
                 { left: '\\(', right: '\\)', display: false }, { left: '$', right: '$', display: false }],
    throwOnError: false, ignoredClasses: ['katex', 'no-math'], ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option']
  };
  var timer = null, busy = false;
  function run(root) {
    if (!window.renderMathInElement) return;
    busy = true;
    try { window.renderMathInElement(root || document.body, opts); } catch (e) { /* a bad formula must never break the page */ }
    busy = false;
  }
  window.renderMath = run;
  function init() {
    run();
    new MutationObserver(function () { if (busy) return; clearTimeout(timer); timer = setTimeout(run, 60); })
      .observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
