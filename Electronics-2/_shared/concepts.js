/* Concept finder (bilingual).  Four tabs: analyse a question (concepts it matches, with the keywords found as evidence), browse the concepts
   (definition, formulas, steps, traps, how it is asked, how many bank questions and book exercises mention it, links to the bank and the finder),
   keyword index, and the coverage table.  Matching is plain keyword scoring in the browser; keywords you teach it are kept in localStorage 'prog:customkw'. */
(function () {
  var root = document.getElementById('concepts'); if (!root) return;
  var L = (document.documentElement.lang || 'vi').slice(0, 2);
  var X = {
    vi: { load: 'Đang tải dữ liệu khái niệm…', fail: 'Không tải được dữ liệu khái niệm: ', tabs: ['Phân tích đề', 'Duyệt khái niệm', 'Chỉ mục từ khoá', 'Độ phủ'],
      ph: 'Dán một câu hỏi (tiếng Anh hoặc tiếng Việt)…', go: 'Tìm khái niệm', clear: 'Xóa', ex: 'Ví dụ…', found: 'Khái niệm khớp nhất', evid: 'Bằng chứng (từ khoá tìm thấy)', score: 'điểm',
      none: 'Không khái niệm nào của học phần khớp đủ mạnh: câu này có thể nằm ngoài danh mục (xem “Ngoài phạm vi” ở tab Độ phủ). Bạn có thể dạy từ khoá mới ở bên dưới.',
      outside: 'Nằm ngoài phạm vi các module của site', teach: 'Dạy hệ thống một từ khoá', kwph: 'cụm từ trong đề (vd “đất ảo”)', toc: 'gán cho khái niệm…', add: 'Thêm', taught: 'Đã lưu trong trình duyệt này.', mine: 'Từ khoá của bạn', del: 'xóa',
      def: 'Định nghĩa', facts: 'Công thức', steps: 'Các bước', traps: 'Bẫy thường gặp', angles: 'Cách ra đề', src: 'Nguồn đã đọc', rel: 'Liên quan', verified: 'Công thức đã được tính lại bằng một đường độc lập',
      nq: function (n) { return n + ' câu trong ngân hàng'; }, nex: function (a, b) { return a + ' bài tập sách nhắc tới (' + b + ' có số)'; }, orig: function (n) { return n + ' câu gốc của sách'; },
      bank: 'Mở ngân hàng câu hỏi theo chủ đề', ex: 'Ví dụ…', exl: 'Xem bài tập của sách', mod: 'Module', all: 'Tất cả', search: 'Tìm khái niệm hoặc từ khoá…', sort: 'Xếp theo', s1: 'Thứ tự module', s2: 'Ít câu nhất trước',
      brief: 'Đưa vào brief', copy: 'Chép brief cho câu hỏi mới', copied: 'Đã chép', briefTitle: 'Khái niệm cần thêm câu hỏi', n: function (a, b) { return a + ' / ' + b + ' khái niệm'; },
      idx: 'Từ khoá → khái niệm', cov: 'Độ phủ của ngân hàng câu hỏi', covHead: ['Module', 'Khái niệm', 'Câu hỏi', 'Câu nhắc tới khái niệm', 'Khái niệm < ' , 'Câu bổ sung lấp khoảng trống'],
      thin: function (t) { return 'Khái niệm có ít hơn ' + t + ' câu nhắc trực tiếp'; }, nothin: 'Không còn khái niệm nào dưới ngưỡng: vòng lấp khoảng trống đã đóng.', gapnote: function (n) { return 'Các câu bổ sung (gắn thẻ gap) được viết sau lần đầu đo độ phủ, đáp án tính bằng chương trình: ' + n + ' câu.'; },
      byc: 'Từng khái niệm', outs: 'Ngoài phạm vi của các module', ncol: ['Khái niệm', 'Module', 'Câu', 'Câu gốc', 'Bài sách'], howread: 'Cách đọc: “câu nhắc tới khái niệm” là số câu có chứa từ khoá của khái niệm trong đề hoặc lời giải; một câu có thể thuộc nhiều khái niệm.' },
    en: { load: 'Loading the concept data…', fail: 'Could not load the concept data: ', tabs: ['Analyse a question', 'Browse concepts', 'Keyword index', 'Coverage'],
      ph: 'Paste a question (English or Vietnamese)…', go: 'Find concepts', clear: 'Clear', ex: 'Examples…', found: 'Best-matching concepts', evid: 'Evidence (keywords found)', score: 'score',
      none: 'No concept of the course matches strongly enough: this question may lie outside the catalogue (see “Out of scope” in the Coverage tab). You can teach a new keyword below.',
      outside: 'Outside the modules of this site', teach: 'Teach the system a keyword', kwph: 'a phrase from the question (e.g. “virtual ground”)', toc: 'assign to concept…', add: 'Add', taught: 'Saved in this browser.', mine: 'Your keywords', del: 'delete',
      def: 'Definition', facts: 'Formulas', steps: 'Steps', traps: 'Common traps', angles: 'How it is asked', src: 'Sources read', rel: 'Related', verified: 'Formulas recomputed by an independent route',
      nq: function (n) { return n + ' bank question' + (n === 1 ? '' : 's'); }, nex: function (a, b) { return a + ' book exercises mention it (' + b + ' numeric)'; }, orig: function (n) { return n + ' original book question' + (n === 1 ? '' : 's'); },
      bank: 'Open the question bank on this topic', exl: 'See the book exercises', mod: 'Module', all: 'All', search: 'Search a concept or keyword…', sort: 'Sort by', s1: 'Module order', s2: 'Fewest questions first',
      brief: 'Add to brief', copy: 'Copy brief for new questions', copied: 'Copied', briefTitle: 'Concepts that need more questions', n: function (a, b) { return a + ' of ' + b + ' concepts'; },
      idx: 'Keyword → concepts', cov: 'Question-bank coverage', covHead: ['Module', 'Concepts', 'Questions', 'Questions mentioning a concept', 'Concepts < ', 'Gap-fill questions'],
      thin: function (t) { return 'Concepts mentioned directly by fewer than ' + t + ' questions'; }, nothin: 'No concept is below the threshold: the gap-fill loop has closed.', gapnote: function (n) { return 'Gap-fill questions (tag gap) were written after the first coverage measurement, with answers computed by script: ' + n + ' questions.'; },
      byc: 'Concept by concept', outs: 'Outside the modules', ncol: ['Concept', 'Module', 'Questions', 'Original', 'Book exercises'], howread: 'How to read: “questions mentioning a concept” counts questions whose statement or explanation contains one of the concept\'s keywords; one question can belong to several concepts.' }
  }[L];
  var EXAMPLES = { vi: ['Tính độ lợi của mạch khuếch đại đảo có Rf = 220 kΩ và Ri = 10 kΩ, đất ảo ở ngõ vào đảo.', 'Một bộ lọc Butterworth hai cực Sallen-Key cần R1/R2 bằng bao nhiêu và hệ số tắt dần là gì?', 'Chọn R1, R2 cho 555 phi ổn có tần số 4 kHz và chu kỳ làm việc 60 %.', 'Hunting trong servo là gì và chống bằng cách nào?', 'Thiết kế bộ khuếch đại thiết bị có độ lợi 1000, tính RG.', 'Giải thích cách một PLL khoá pha tần số tín hiệu vào.'],
    en: ['Find the gain of an inverting amplifier with Rf = 220 kΩ and Ri = 10 kΩ; the inverting input is a virtual ground.', 'What R1/R2 and damping factor does a two-pole Sallen-Key Butterworth filter need?', 'Choose R1, R2 for an astable 555 with f = 4 kHz and 60 % duty cycle.', 'What is hunting in a servo and how is it prevented?', 'Design an instrumentation amplifier with a gain of 1000: find RG.', 'Explain how a PLL locks onto the frequency of the input signal.'] }[L];
  function el(t, c, txt) { var e = document.createElement(t); if (c) e.className = c; if (txt !== undefined) e.textContent = txt; return e; }
  function norm(t) { return t.toLowerCase().replace(/đ/g, 'd').normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function stem(w) { return w.length > 4 ? w.replace(/(ies|ing|ed|es|s)$/, function (m) { return m === 'ies' ? 'y' : ''; }) : w; }
  function stems(t) { return (norm(t).match(/[a-z][a-z0-9\-]{2,}/g) || []).map(stem); }
  function get(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  var D = null, BYID = {}, MODS = {}, IDF = {}, PHR = [], custom = get('prog:customkw', {}), brief = get('prog:conceptbrief', {});
  root.appendChild(el('p', 'muted', X.load));
  fetch(root.getAttribute('data-src')).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); }).then(function (j) { D = j; prepare(); init(); })
    .catch(function (e) { root.innerHTML = ''; root.appendChild(el('div', 'callout bad', X.fail + e.message)); });

  function cname(c) { return c.name[L]; }
  function prepare() {
    D.concepts.forEach(function (c) { BYID[c.id] = c; }); D.modules.forEach(function (m) { MODS[m.id] = m; });
    var df = {}; function reg(p, id) { (df[p] = df[p] || {})[id] = 1; }
    D.concepts.forEach(function (c) { c.kw.forEach(function (k) { reg(norm(k), c.id); }); c.kwv.forEach(function (k) { reg(norm(k), c.id); }); });
    D.out.forEach(function (o) { o.kw.forEach(function (k) { reg(norm(k), o.id); }); o.kwv.forEach(function (k) { reg(norm(k), o.id); }); });
    var N = D.concepts.length + D.out.length;
    Object.keys(df).forEach(function (p) { IDF[p] = Math.log(1 + N / Object.keys(df[p]).length) * (1 + 0.5 * (p.split(/\s+/).length - 1)); });
  }
  function phraseRe(p) { return new RegExp('(^|[^a-z0-9])' + p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + (p.length <= 4 ? '($|[^a-z0-9])' : ''), 'i'); }
  function scoreAll(text) {
    var nt = norm(text), st = {}; stems(text).forEach(function (w) { st[w] = 1; });
    function one(id, kw, kwv, ak) {
      var s = 0, ev = [], seen = {};
      kw.concat(kwv).forEach(function (k) { var p = norm(k); if (p.length < 2 || seen[p]) return; seen[p] = 1; if (phraseRe(p).test(nt)) { s += IDF[p] || 1; ev.push(k); } });
      (ak || []).forEach(function (w) { if (st[w]) { s += 0.25; } });
      Object.keys(custom).forEach(function (p) { if (custom[p] === id && phraseRe(norm(p)).test(nt)) { s += 3; ev.push(p + ' ★'); } });
      return [s, ev];
    }
    var res = D.concepts.map(function (c) { var r = one(c.id, c.kw, c.kwv, c.ak); return { c: c, s: r[0], ev: r[1] }; }).filter(function (r) { return r.ev.length > 0; });
    var outs = D.out.map(function (o) { var r = one(o.id, o.kw, o.kwv, []); return { o: o, s: r[0], ev: r[1] }; }).filter(function (r) { return r.ev.length > 0; });
    res.sort(function (a, b) { return b.s - a.s; }); outs.sort(function (a, b) { return b.s - a.s; });
    return { res: res, outs: outs };
  }
  function wrap(t) { var w = el('div'); w.style.overflowX = 'auto'; w.appendChild(t); return w; }
  function chip(m) { var a = el('a', 'bm-chip r-core', m.toUpperCase()); a.href = '../practice/' + m + '.html'; return a; }
  function conceptCard(c, open, withId) {
    var d = el('details', 'qitem'); if (withId) d.id = 'c-' + c.id; if (open) d.open = true;
    var sm = el('summary'); sm.appendChild(el('b', null, cname(c) + ' ')); sm.appendChild(chip(c.mod));
    sm.appendChild(el('span', 'tag', X.nq(c.n))); if (c.n_orig) sm.appendChild(el('span', 'tag good', '★ ' + X.orig(c.n_orig)));
    d.appendChild(sm);
    d.appendChild(el('p', null, c.defn[L]));
    if (c.facts.length) {
      d.appendChild(el('h4', null, X.facts)); var ul = el('ul');
      c.facts.forEach(function (f) { var li = el('li'); li.appendChild(el('code', 'cf-formula', f.f)); li.appendChild(document.createTextNode(' — ' + f.note[L])); ul.appendChild(li); });
      d.appendChild(ul); if (c.checked) d.appendChild(el('div', 'srcnote', '✓ ' + X.verified));
    }
    function list(title, arr, tag) { if (!arr.length) return; d.appendChild(el('h4', null, title)); var l = el(tag); arr.forEach(function (x) { l.appendChild(el('li', null, x[L])); }); d.appendChild(l); }
    list(X.steps, c.steps, 'ol'); list(X.traps, c.traps, 'ul'); list(X.angles, c.angles, 'ul');
    d.appendChild(el('div', 'srcnote', X.src + ': ' + c.src.join(' · ')));
    d.appendChild(el('div', 'srcnote', X.nex(c.n_ex, c.n_ex_num)));
    var row = el('p'); var topic = c.topics.length ? c.topics[0][L] : '';
    var a1 = el('a', 'btn small alt', X.bank); a1.href = '../practice/' + c.mod + '.html' + (topic ? '?topic=' + encodeURIComponent(topic) : ''); row.appendChild(a1);
    var a2 = el('a', 'btn small alt', X.exl); a2.href = '../exercises/index.html?mod=' + c.mod + '&q=' + encodeURIComponent(c.kw[0] || ''); a2.style.marginLeft = '6px'; row.appendChild(a2);
    var lb = el('label'); lb.style.marginLeft = '10px'; var cb = el('input'); cb.type = 'checkbox'; cb.checked = !!brief[c.id];
    cb.onchange = function () { if (cb.checked) brief[c.id] = 1; else delete brief[c.id]; put('prog:conceptbrief', brief); refreshBrief(); };
    lb.appendChild(cb); lb.appendChild(document.createTextNode(' ' + X.brief)); row.appendChild(lb); d.appendChild(row);
    if (c.related.length) { var rp = el('p', 'srcnote', X.rel + ': '); c.related.forEach(function (id) { if (!BYID[id]) return; var a = el('a', 'tag', cname(BYID[id])); a.href = '#' + id; a.onclick = function () { gotoConcept(id); return false; }; rp.appendChild(a); }); d.appendChild(rp); }
    return d;
  }
  var tabsBox, panes = [], briefBox, gotoConcept = function () { };
  function refreshBrief() {
    if (!briefBox) return; briefBox.innerHTML = ''; var ids = Object.keys(brief).filter(function (id) { return BYID[id]; }); if (!ids.length) return;
    var t = X.briefTitle + ':\n' + ids.map(function (id) { var c = BYID[id]; return '- ' + c.id + ' · ' + cname(c) + ' (' + X.nq(c.n) + ')'; }).join('\n');
    var b = el('button', 'btn small', X.copy + ' (' + ids.length + ')'); b.type = 'button';
    b.onclick = function () { function done() { b.textContent = X.copied + ' ✓'; } if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function () { fallback(); }); else fallback(); function fallback() { var ta = el('textarea'); ta.value = t; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); done(); } catch (e) { } ta.remove(); } };
    briefBox.appendChild(b);
  }
  function init() {
    root.innerHTML = ''; tabsBox = el('div', 'row'); root.appendChild(tabsBox);
    var builders = [paneAnalyse, paneBrowse, paneIndex, paneCoverage];
    builders.forEach(function (bf, i) {
      var pane = el('div'); pane.setAttribute('data-pane', i); panes.push(pane); root.appendChild(pane); bf(pane);
      var b = el('button', 'btn alt', X.tabs[i]); b.type = 'button'; b.onclick = function () { show(i); }; tabsBox.appendChild(b);
    });
    briefBox = el('p'); root.appendChild(briefBox); refreshBrief();
    function show(i) { panes.forEach(function (p, k) { p.classList.toggle('hide', k !== i); tabsBox.children[k].className = 'btn' + (k === i ? '' : ' alt'); }); }
    window.__cfShow = show; show(0);
    gotoConcept = function (id) { show(1); var d = document.getElementById('c-' + id); if (!d) { if (window.__cfClear) window.__cfClear(); d = document.getElementById('c-' + id); } if (d) { d.open = true; d.scrollIntoView({ behavior: 'smooth', block: 'start' }); } };
    var h = (location.hash || '').replace('#', ''); if (h && BYID[h]) gotoConcept(h);
  }
  // ------------------------------------------------------------ tab 1
  function paneAnalyse(pane) {
    var ta = el('textarea'); ta.rows = 4; ta.placeholder = X.ph; ta.style.width = '100%'; pane.appendChild(ta);
    var bar = el('div', 'row'), go = el('button', 'btn', X.go), cl = el('button', 'btn alt', X.clear), ex = el('select'), o0 = el('option', null, X.ex); o0.value = ''; ex.appendChild(o0);
    EXAMPLES.forEach(function (e, i) { var o = el('option', null, e.slice(0, 70) + '…'); o.value = i; ex.appendChild(o); });
    ex.style.maxWidth = '100%'; bar.appendChild(go); bar.appendChild(cl); bar.appendChild(ex); pane.appendChild(bar); var out = el('div'); pane.appendChild(out);
    ex.onchange = function () { if (ex.value !== '') { ta.value = EXAMPLES[+ex.value]; run(); } }; cl.onclick = function () { ta.value = ''; out.innerHTML = ''; }; go.onclick = run;
    var tb = el('div', 'panel'); tb.appendChild(el('h3', null, X.teach)); var row = el('div', 'bm-bar'), ki = el('input'); ki.type = 'search'; ki.placeholder = X.kwph; var sel = el('select');
    var s0 = el('option', null, X.toc); s0.value = ''; sel.appendChild(s0); D.concepts.forEach(function (c) { var o = el('option', null, c.mod.toUpperCase() + ' · ' + cname(c)); o.value = c.id; sel.appendChild(o); });
    var ad = el('button', 'btn small', X.add), msg = el('span', 'muted'); ad.type = 'button';
    ad.onclick = function () { var k = ki.value.trim().toLowerCase(); if (k.length < 2 || !sel.value) return; custom[k] = sel.value; put('prog:customkw', custom); msg.textContent = X.taught; ki.value = ''; showMine(); if (ta.value.trim()) run(); };
    row.appendChild(ki); row.appendChild(sel); row.appendChild(ad); row.appendChild(msg); tb.appendChild(row); var mine = el('p', 'srcnote'); tb.appendChild(mine); pane.appendChild(tb);
    function showMine() { mine.innerHTML = ''; var ks = Object.keys(custom).filter(function (k) { return BYID[custom[k]]; }); if (!ks.length) return; mine.appendChild(document.createTextNode(X.mine + ': '));
      ks.forEach(function (k) { var t = el('span', 'tag', k + ' → ' + cname(BYID[custom[k]]) + ' '); var x = el('a', null, '×'); x.href = '#'; x.title = X.del; x.onclick = function () { delete custom[k]; put('prog:customkw', custom); showMine(); return false; }; t.appendChild(x); mine.appendChild(t); }); }
    showMine();
    function run() {
      var text = ta.value.trim(); out.innerHTML = ''; if (!text) return; var r = scoreAll(text), best = r.res.length ? r.res[0].s : 0, bestOut = r.outs.length ? r.outs[0].s : 0;
      var outStrong = bestOut >= 1.5 && bestOut >= best;
      if (outStrong) { var o = r.outs[0].o, bx = el('div', 'callout warn'); bx.appendChild(el('b', null, X.outside + ': ' + o.name[L] + '. ')); bx.appendChild(document.createTextNode(o.note[L])); out.appendChild(bx); }
      if (best < 1.5) { if (!outStrong) out.appendChild(el('div', 'callout warn', X.none)); return; }
      out.appendChild(el('h3', null, X.found));
      r.res.filter(function (x) { return x.s >= Math.max(1.5, best * 0.35); }).slice(0, 4).forEach(function (x, i) {
        var box = el('div'); var head = el('p'); head.appendChild(el('span', 'tag', X.score + ' ' + x.s.toFixed(1))); var evp = el('span', 'srcnote', ' ' + X.evid + ': ' + x.ev.join(', ')); head.appendChild(evp); box.appendChild(head);
        box.appendChild(conceptCard(x.c, i === 0)); out.appendChild(box);
      });
    }
  }
  // ------------------------------------------------------------ tab 2
  function paneBrowse(pane) {
    var S = { mod: 'all', q: '', sort: 'mod' }, bar = el('div', 'bm-bar'), info = el('div', 'score'), list = el('div');
    function sel(label, opts, key) { var l = el('label', null, label + ' '), s = el('select'); opts.forEach(function (o) { var op = el('option', null, o[1]); op.value = o[0]; s.appendChild(op); }); s.onchange = function () { S[key] = s.value; render(); }; l.appendChild(s); return l; }
    var mods = [['all', X.all]].concat(D.modules.map(function (m) { return [m.id, m.id.toUpperCase() + ' · ' + m[L]]; }));
    bar.appendChild(sel(X.mod, mods, 'mod')); bar.appendChild(sel(X.sort, [['mod', X.s1], ['few', X.s2]], 'sort'));
    var q = el('input'); q.type = 'search'; q.placeholder = X.search; q.oninput = function () { S.q = norm(q.value); render(); }; bar.appendChild(q); pane.appendChild(bar); pane.appendChild(info); pane.appendChild(list);
    function hay(c) { return norm([cname(c), c.defn[L], c.kw.join(' '), c.kwv.join(' '), c.facts.map(function (f) { return f.f; }).join(' ')].join(' ')); }
    function render() {
      var f = D.concepts.filter(function (c) { return (S.mod === 'all' || c.mod === S.mod) && (!S.q || hay(c).indexOf(S.q) >= 0); });
      if (S.sort === 'few') f.sort(function (a, b) { return a.n - b.n; });
      info.textContent = X.n(f.length, D.concepts.length); list.innerHTML = ''; f.forEach(function (c) { list.appendChild(conceptCard(c, false, true)); });
    }
    window.__cfClear = function () { S.mod = 'all'; S.q = ''; render(); }; render();
  }
  // ------------------------------------------------------------ tab 3
  function paneIndex(pane) {
    pane.appendChild(el('h3', null, X.idx)); var map = {};
    D.concepts.forEach(function (c) { c.kw.concat(c.kwv).forEach(function (k) { var key = norm(k); (map[key] = map[key] || { label: k, ids: {} }).ids[c.id] = 1; }); });
    var keys = Object.keys(map).sort(); var ul = el('ul'); ul.style.columns = '2 260px';
    keys.forEach(function (k) { var li = el('li'); li.appendChild(el('b', null, map[k].label + ' → ')); Object.keys(map[k].ids).forEach(function (id) { var a = el('a', 'tag', cname(BYID[id])); a.href = '#' + id; a.onclick = function () { gotoConcept(id); return false; }; li.appendChild(a); }); ul.appendChild(li); });
    pane.appendChild(el('p', 'muted', keys.length + ' / ' + D.concepts.length)); pane.appendChild(ul);
  }
  // ------------------------------------------------------------ tab 4
  function paneCoverage(pane) {
    pane.appendChild(el('h3', null, X.cov)); pane.appendChild(el('p', 'srcnote', X.howread));
    var t = el('table'), th = el('tr'); X.covHead.forEach(function (h, i) { th.appendChild(el('th', null, i === 4 ? h + D.thin : h)); }); t.appendChild(th);
    var tot = { c: 0, q: 0, m: 0, t: 0, g: 0 };
    D.modules.forEach(function (m) { var tr = el('tr'); [m.id.toUpperCase() + ' · ' + m[L], m.concepts, m.items, m.matched, m.thin, m.gap].forEach(function (v) { tr.appendChild(el('td', null, String(v))); }); t.appendChild(tr); tot.c += m.concepts; tot.q += m.items; tot.m += m.matched; tot.t += m.thin; tot.g += m.gap; });
    var trt = el('tr'); ['Σ', tot.c, tot.q, tot.m, tot.t, tot.g].forEach(function (v) { trt.appendChild(el('th', null, String(v))); }); t.appendChild(trt); pane.appendChild(wrap(t));
    pane.appendChild(el('h4', null, X.thin(D.thin))); var thin = D.concepts.filter(function (c) { return c.n < D.thin; });
    if (!thin.length) pane.appendChild(el('div', 'callout good', X.nothin + ' ' + X.gapnote(tot.g))); else { var ul = el('ul'); thin.forEach(function (c) { var li = el('li'); var a = el('a', null, cname(c) + ' (' + c.n + ')'); a.href = '#' + c.id; a.onclick = function () { gotoConcept(c.id); return false; }; li.appendChild(a); ul.appendChild(li); }); pane.appendChild(ul); pane.appendChild(el('p', 'srcnote', X.gapnote(tot.g))); }
    pane.appendChild(el('h4', null, X.byc)); var t2 = el('table'), h2 = el('tr'); X.ncol.forEach(function (h) { h2.appendChild(el('th', null, h)); }); t2.appendChild(h2);
    D.concepts.slice().sort(function (a, b) { return a.n - b.n; }).forEach(function (c) { var tr = el('tr'), td = el('td'), a = el('a', null, cname(c)); a.href = '#' + c.id; a.onclick = function () { gotoConcept(c.id); return false; }; td.appendChild(a); tr.appendChild(td);
      [c.mod.toUpperCase(), c.n, c.n_orig, c.n_ex].forEach(function (v) { tr.appendChild(el('td', null, String(v))); }); t2.appendChild(tr); });
    pane.appendChild(wrap(t2));
    pane.appendChild(el('h4', null, X.outs)); var ul2 = el('ul'); D.out.forEach(function (o) { var li = el('li'); li.appendChild(el('b', null, o.name[L] + ': ')); li.appendChild(document.createTextNode(o.note[L])); ul2.appendChild(li); }); pane.appendChild(ul2);
  }
})();
