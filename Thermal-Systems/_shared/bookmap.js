/* Book map (AE2.013): renders the three tables of contents and the slide list from data/bookmap/*.json, with instant filters
   (module, role, title search) remembered in the URL hash as "#f:m=m02&r=core&q=otto". Optional data/bookmap/qcount.json adds a "Questions" column. */
(function () {
  var app = document.getElementById('bm-app'); if (!app) return;
  var root = app.getAttribute('data-root') || '', vi = app.getAttribute('data-lang') === 'vi';
  function t(a, b) { return vi ? a : b; }
  var ROLE = { core: ['●', t('lõi', 'core')], ref: ['◐', t('đọc thêm', 'reference')], background: ['○', t('nền', 'background')], optional: ['◌', t('tùy chọn', 'optional')], out: ['✕', t('ngoài phạm vi', 'out of scope')] };
  var CHVI = { 1: 'Nhập môn và khái niệm cơ bản', 2: 'Chuyển hoá năng lượng và phân tích năng lượng tổng quát', 3: 'Tính chất của chất tinh khiết', 4: 'Phân tích năng lượng hệ kín', 5: 'Cân bằng khối lượng và năng lượng cho thể tích kiểm soát', 6: 'Định luật nhiệt động thứ hai', 7: 'Entropi', 8: 'Exergy: thước đo khả năng sinh công', 9: 'Chu trình công suất khí', 10: 'Chu trình hơi và chu trình kết hợp', 11: 'Chu trình lạnh', 12: 'Các hệ thức tính chất nhiệt động', 13: 'Hỗn hợp khí', 14: 'Hỗn hợp khí–hơi và điều hoà không khí', 15: 'Phản ứng hoá học', 16: 'Cân bằng hoá học và cân bằng pha', 17: 'Dòng chảy nén được' };
  var DECK = { ch1: t('Chương 1 · Giới thiệu và tổng quan', 'Chapter 1 · Introduction and Generality'), ch2: t('Chương 2 · Chu trình công suất', 'Chapter 2 · Power Cycles'), ch3: t('Chương 3 · Chu trình lạnh', 'Chapter 3 · Refrigeration Cycles'), ch4: t('Chương 4 · Quá trình cháy', 'Chapter 4 · Combustion process'), ch5: t('Chương 5 · Dòng nén được', 'Chapter 5 · Compressible Flow'), tut: t('Tutorials I (bài tập mẫu)', 'Tutorials I') };
  var DSHORT = { ch1: 'Ch.1', ch2: 'Ch.2', ch3: 'Ch.3', ch4: 'Ch.4', ch5: 'Ch.5', tut: 'Tut.' };
  var KIND = { content: t('nội dung', 'content'), blank: t('trống', 'blank'), title: t('bìa', 'cover') };
  var ENDVI = { 'PROBLEMS': 'Bài tập', 'Problems': 'Bài tập', 'Review Problems': 'Bài tập ôn', 'Fundamentals of Engineering (FE) Exam Problems': 'Bài FE', 'Design and Essay Problems': 'Bài thiết kế và tiểu luận', 'SUMMARY': 'Tóm tắt', 'Summary': 'Tóm tắt', 'REFERENCES AND SUGGESTED READING': 'Tài liệu tham khảo', 'References': 'Tài liệu tham khảo', 'TOPIC OF SPECIAL INTEREST': 'Chủ đề đặc biệt' };
  var ENDEN = { 'PROBLEMS': 'Problems', 'SUMMARY': 'Summary', 'REFERENCES AND SUGGESTED READING': 'References and Suggested Reading', 'TOPIC OF SPECIAL INTEREST': 'Topic of Special Interest' };
  var BOOKS = [['cengel', 'Cengel &amp; Boles, Thermodynamics 5e', t('PDF 963 tr.; in = PDF − 26', '963-page PDF; printed = PDF − 26')],
               ['farokhi', 'Farokhi, Aircraft Propulsion 2e', t('389 bookmark mức 1–3; in = PDF − 34', '389 bookmarks, levels 1–3; printed = PDF − 34')],
               ['elsayed', 'El-Sayed, Aircraft Propulsion and Gas Turbine Engines 2e', t('230 mục của Ch.1, 2, 3, 4, 9, 10, 11; chỉ trang in', '230 entries of Ch.1, 2, 3, 4, 9, 10, 11; printed page only')]];
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function rng(a, b) { return b > a ? a + '–' + b : '' + a; }
  var D = null, Q = null, state = { m: '', r: '', q: '', d: '' };

  // ---------- row model ----------
  function modsOf(mods) { return Object.keys(mods || {}).sort(); }
  function roleChips(mods) {
    var ks = modsOf(mods); if (!ks.length) return '<span class="bm-r r-out">✕ ' + ROLE.out[1] + '</span>';
    return ks.map(function (k) { var r = mods[k].role || 'ref'; return '<span class="bm-mm"><span class="bm-r r-' + r + '">' + k + ' · ' + ROLE[r][0] + ' ' + ROLE[r][1] + '</span><span class="b">' + esc(vi ? (mods[k].basis || '') : String(mods[k].basis || '').replace(/nền/g, 'background')) + '</span></span>'; }).join('');
  }
  function rowHtml(o) {
    var ks = modsOf(o.mods), roles = ks.length ? ks.map(function (k) { return o.mods[k].role; }).join(' ') : 'out';
    var q = ''; if (Q && Q[o.book]) { var v = Q[o.book][o.num || o.title]; q = typeof v === 'number' ? v : (v && typeof v.total === 'number' ? v.total : ''); }
    return '<tr' + (o.id ? ' id="' + o.id + '"' : '') + ' data-book="' + o.book + '" data-mods="' + ks.join(' ') + '" data-roles="' + roles + '" data-text="' + esc((o.num + ' ' + o.title).toLowerCase()) + '">' +
      '<td style="padding-left:' + (7 + (o.ind || 0) * 14) + 'px">' + (o.num ? '<b>' + esc(o.num) + '</b> ' : '') + esc(o.title) + '</td><td class="n">' + (o.pr == null || o.pr === '' ? '–' : o.pr) + '</td><td class="n">' + (o.pdf == null ? '–' : o.pdf) + '</td><td>' + roleChips(o.mods) + '</td><td class="bm-qc n">' + q + '</td></tr>';
  }
  function chapRow(id, html, mods) { return '<tr class="bm-chap" id="' + id + '" data-chap="1" data-mods="' + (mods || []).join(' ') + '"><td colspan="5">' + html + '</td></tr>'; }
  function endName(n) { return vi ? (ENDVI[n] || n) : (ENDEN[n] || n); }

  function cengelRows(C) {
    var off = C.offset, out = [], n = 0;
    C.chapters.forEach(function (ch) {
      out.push(chapRow('bm-cengel-' + ch.num, '<b>Ch.' + ch.num + '</b> ' + esc(vi ? CHVI[ch.num] : ch.title) + (vi ? ' <span class="srcnote">' + esc(ch.title) + '</span>' : '') + ' <span class="srcnote">' + t('tr. in ', 'printed p.') + rng(ch.printed, ch.pdf_end - off) + ' · PDF ' + rng(ch.pdf, ch.pdf_end) + '</span> ' + (ch.mods || []).map(function (m) { return '<span class="bm-r r-core">' + m + '</span>'; }).join(''), ch.mods));
      var items = [];
      ch.sections.forEach(function (s) { items.push({ pdf: s.pdf, o: { book: 'cengel', num: s.num, title: s.title, pr: rng(s.printed, s.pdf_end - off), pdf: rng(s.pdf, s.pdf_end), mods: s.mods } }); });
      ch.end_parts.forEach(function (e) { items.push({ pdf: e.pdf, o: { book: 'cengel', num: '', title: endName(e.name), pr: e.printed, pdf: e.pdf, mods: e.mods } }); });
      (ch.features || []).forEach(function (e) { items.push({ pdf: e.pdf, o: { book: 'cengel', num: '', title: endName(e.name), pr: e.printed, pdf: e.pdf, mods: e.mods || {} } }); });
      items.sort(function (a, b) { return a.pdf - b.pdf; });
      items.forEach(function (it) { out.push(rowHtml(it.o)); n++; });
    });
    return { html: out.join(''), n: n };
  }
  function farokhiRows(F) {
    var off = F.offset, out = [];
    F.entries.forEach(function (e) {
      var pr = e.printed == null ? '–' : rng(e.printed, e.pdf_end - off);
      var num = e.num || '', title = e.title, ind = e.level - 1;
      out.push(rowHtml({ book: 'farokhi', id: 'bm-farokhi-' + e.i, num: num, title: title, pr: pr, pdf: rng(e.pdf, e.pdf_end), mods: e.mods, ind: ind }));
    });
    return { html: out.join(''), n: F.entries.length };
  }
  function elsayedRows(E) {
    var out = [], seen = {};
    E.entries.forEach(function (e) {
      var id = e.kind === 'chapter' && !seen[e.chapter] ? 'bm-elsayed-' + e.chapter : ''; if (id) seen[e.chapter] = 1;
      out.push(rowHtml({ book: 'elsayed', id: id, num: e.kind === 'chapter' ? 'Ch.' + e.num : e.num, title: e.title, pr: e.printed, pdf: null, mods: e.mods, ind: e.depth - 1 }));
    });
    return { html: out.join(''), n: E.entries.length };
  }
  function table(rows) {
    return '<div class="bm-wrap"><table class="bm-tbl"><thead><tr><th>' + t('Mục', 'Section') + '</th><th>' + t('Tr. in', 'Printed p.') + '</th><th>' + t('Tr. PDF', 'PDF p.') + '</th><th>' + t('Vai trò · module · cơ sở', 'Role · module · basis') + '</th><th class="bm-qc">' + t('Câu hỏi', 'Questions') + '</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
  }

  // ---------- slides ----------
  function slideCards(S) {
    var out = [], n = 0;
    Object.keys(DECK).forEach(function (d) {
      if (!S[d]) return;
      S[d].slides.forEach(function (s) {
        var p = (s.page < 10 ? '0' : '') + s.page, title = s.kind === 'blank' ? t('(slide trống)', '(blank slide)') : s.title, mod = s.module || '–';
        var cap = DSHORT[d] + ' ' + t('tr.', 'p.') + s.page + ' · ' + title + ' · ' + mod;
        out.push('<div class="bm-card k-' + s.kind + '" data-deck="' + d + '" data-mods="' + (s.module || '') + '" data-text="' + esc(title.toLowerCase()) + '"><a href="' + root + 'assets/slides/' + d + '/p' + p + '.jpg" data-cap="' + esc(cap) + '"><img src="' + root + 'assets/slides/' + d + '/p' + p + '.jpg" alt="' + esc(cap) + '" width="160" height="120"></a><b>' + DSHORT[d] + ' ' + t('tr.', 'p.') + s.page + '</b> · ' + esc(title) +
          '<br><span class="bm-r r-' + (s.kind === 'content' ? 'core' : s.kind === 'blank' ? 'optional' : 'background') + '">' + KIND[s.kind] + '</span><span class="bm-r r-background">' + mod + '</span></div>'); n++;
      });
    });
    return { html: out.join(''), n: n };
  }
  function lightbox(list, i) {
    var box = document.createElement('div'); box.className = 'lightbox'; box.setAttribute('role', 'dialog');
    box.innerHTML = '<img alt=""><div class="lb-cap"></div><div class="lb-bar"><button type="button" data-d="-1">◀</button><button type="button" data-x="1">✕</button><button type="button" data-d="1">▶</button></div>';
    document.body.appendChild(box); var img = box.querySelector('img'), cap = box.querySelector('.lb-cap');
    function show() { var a = list[i]; img.src = a.href; img.alt = a.getAttribute('data-cap'); cap.textContent = a.getAttribute('data-cap'); }
    function close() { document.removeEventListener('keydown', key); box.remove(); }
    function key(e) { if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') { i = (i + list.length - 1) % list.length; show(); } else if (e.key === 'ArrowRight') { i = (i + 1) % list.length; show(); } }
    box.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b && b.dataset.d) { i = (i + list.length + +b.dataset.d) % list.length; show(); } else if (b && b.dataset.x) close(); else if (!b && e.target !== img) close(); });
    document.addEventListener('keydown', key); show();
  }

  // ---------- filters ----------
  function readHash() { var h = location.hash; if (h.indexOf('#f:') !== 0) return; h.slice(3).split('&').forEach(function (kv) { var p = kv.split('='), v = decodeURIComponent(p[1] || ''); if (p[0] === 'm') state.m = v; if (p[0] === 'r') state.r = v; if (p[0] === 'q') state.q = v; if (p[0] === 'd') state.d = v; }); }
  function writeHash() {
    var p = []; if (state.m) p.push('m=' + state.m); if (state.r) p.push('r=' + state.r); if (state.q) p.push('q=' + encodeURIComponent(state.q)); if (state.d) p.push('d=' + state.d);
    try { history.replaceState(null, '', location.pathname + location.search + (p.length ? '#f:' + p.join('&') : '')); } catch (e) { }
  }
  function apply() {
    var m = state.m, r = state.r, q = state.q.trim().toLowerCase(), filtering = !!(m || r || q), total = 0, per = {};
    var chap = null, chapVis = 0;
    function endChap() { if (chap) chap.classList.toggle('bm-hide', filtering && chapVis === 0); }
    app.querySelectorAll('tbody tr').forEach(function (tr) {
      if (tr.hasAttribute('data-chap')) { endChap(); chap = tr; chapVis = 0; return; }
      var mods = (tr.getAttribute('data-mods') || '').split(' ').filter(Boolean), roles = (tr.getAttribute('data-roles') || '').split(' '), ok = true;
      if (m && mods.indexOf(m) < 0) ok = false;
      if (r && roles.indexOf(r) < 0) ok = false;
      if (q && (tr.getAttribute('data-text') || '').indexOf(q) < 0) ok = false;
      tr.classList.toggle('bm-hide', !ok);
      if (ok) { chapVis++; total++; var b = tr.getAttribute('data-book'); per[b] = (per[b] || 0) + 1; }
    });
    endChap();
    app.querySelectorAll('.bm-cnt').forEach(function (c) { var b = c.getAttribute('data-book'); c.textContent = (per[b] || 0) + ' / ' + c.getAttribute('data-n'); });
    var sv = 0, sn = 0;
    app.querySelectorAll('.bm-card').forEach(function (c) {
      var ok = true; sn++;
      if (m && c.getAttribute('data-mods') !== m) ok = false;
      if (state.d && c.getAttribute('data-deck') !== state.d) ok = false;
      if (q && c.getAttribute('data-text').indexOf(q) < 0) ok = false;
      c.classList.toggle('bm-hide', !ok); if (ok) sv++;
    });
    var sc = document.getElementById('bm-scnt'); if (sc) sc.textContent = sv + ' / ' + sn;
    var none = document.getElementById('bm-none'); if (none) none.hidden = !(filtering && total === 0 && sv === 0);
    if (filtering) app.querySelectorAll('details.bm-bk').forEach(function (d) { if (!d.open && d.getAttribute('data-auto') === '1') d.open = true; });
    writeHash();
  }
  function syncControls() {
    var s = document.getElementById('bm-mod'), r = document.getElementById('bm-role'), q = document.getElementById('bm-q'), d = document.getElementById('bm-deck');
    if (s) s.value = state.m; if (r) r.value = state.r; if (q) q.value = state.q; if (d) d.value = state.d;
  }
  function bind() {
    var s = document.getElementById('bm-mod'), r = document.getElementById('bm-role'), q = document.getElementById('bm-q'), d = document.getElementById('bm-deck'), x = document.getElementById('bm-reset');
    if (s) s.addEventListener('change', function () { state.m = s.value; apply(); });
    if (r) r.addEventListener('change', function () { state.r = r.value; apply(); });
    if (q) q.addEventListener('input', function () { state.q = q.value; apply(); });
    if (d) d.addEventListener('change', function () { state.d = d.value; apply(); });
    if (x) x.addEventListener('click', function () { state = { m: '', r: '', q: '', d: '' }; syncControls(); apply(); });
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#bm-"]'); if (!a) return;
      var el = document.querySelector(a.getAttribute('href')); if (!el) return;
      var det = el.closest('details'); if (det) det.open = true; e.preventDefault(); el.scrollIntoView({ block: 'center' });
    });
    app.addEventListener('click', function (e) {
      var a = e.target.closest('.bm-card a'); if (!a) return; e.preventDefault();
      var list = Array.prototype.filter.call(app.querySelectorAll('.bm-card:not(.bm-hide) a'), function () { return true; }); lightbox(list, list.indexOf(a));
    });
  }

  // ---------- boot ----------
  function load(n) { return fetch(root + 'data/bookmap/' + n + '.json').then(function (r) { if (!r.ok) throw new Error(n + '.json: HTTP ' + r.status); return r.json(); }); }
  function render() {
    var C = cengelRows(D.cengel), F = farokhiRows(D.farokhi), E = elsayedRows(D.elsayed), S = slideCards(D.slides), h = '', rows = { cengel: C, farokhi: F, elsayed: E };
    BOOKS.forEach(function (b) {
      h += '<details class="bm-bk" id="bm-book-' + b[0] + '" data-auto="1"><summary>' + b[1] + ' <span class="srcnote">' + b[2] + ' · <span class="bm-cnt" data-book="' + b[0] + '" data-n="' + rows[b[0]].n + '">' + rows[b[0]].n + ' / ' + rows[b[0]].n + '</span> ' + t('mục', 'entries') + '</span></summary>' + table(rows[b[0]].html) + '</details>';
    });
    h += '<h3 id="slides">' + t('Slide của giảng viên', "Lecturer's slides") + '</h3><details class="bm-bk" id="bm-book-slides" data-auto="1"><summary>' + t('296 trang trong 6 bộ', '296 pages in 6 decks').replace('296', S.n) + ' <span class="srcnote">· <span id="bm-scnt">' + S.n + ' / ' + S.n + '</span></span></summary>' +
      '<div class="bm-bar" style="padding:0 12px"><label>' + t('Bộ slide', 'Deck') + ': <select id="bm-deck"><option value="">' + t('Tất cả bộ', 'All decks') + '</option>' + Object.keys(DECK).map(function (k) { return '<option value="' + k + '">' + esc(DECK[k]) + '</option>'; }).join('') + '</select></label></div><div class="bm-grid" id="bm-grid"></div></details>';
    app.innerHTML = h; app.className = 'bm-app' + (Q ? '' : ' bm-noq');
    // slide images are created when the block is first opened (about 12 MB of JPEG in total)
    var sd = document.getElementById('bm-book-slides'), done = false;
    function fill() { if (done) return; done = true; document.getElementById('bm-grid').innerHTML = S.html; apply(); }
    sd.addEventListener('toggle', function () { if (sd.open) fill(); });
    if (state.d || sd.open) { sd.open = true; fill(); }
    bind(); syncControls(); apply();
    var hh = location.hash; if (hh.indexOf('#bm-') === 0) { var el = document.querySelector(hh); if (el) { var dt = el.closest('details'); if (dt) dt.open = true; el.scrollIntoView(); } }
    app.setAttribute('data-ready', '1');
  }
  function boot() {
    app.innerHTML = '<p class="muted">' + t('Đang tải dữ liệu…', 'Loading data…') + '</p>';
    readHash();
    Promise.all([load('cengel'), load('farokhi'), load('elsayed'), load('slides')]).then(function (a) {
      D = { cengel: a[0], farokhi: a[1], elsayed: a[2], slides: a[3] };
      return fetch(root + 'data/bookmap/qcount.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (q) { Q = q && typeof q === 'object' ? q : null; render(); });
    }).catch(function (err) {
      app.innerHTML = '<div class="bm-err">' + t('Không tải được dữ liệu bản đồ sách: ', 'Could not load the book-map data: ') + esc(err.message) + ' <button type="button" id="bm-retry">' + t('Thử lại', 'Retry') + '</button></div>';
      document.getElementById('bm-retry').addEventListener('click', boot);
    });
  }
  boot();
})();
