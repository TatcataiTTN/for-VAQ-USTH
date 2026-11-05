// Browser test of the built site. Usage: node tests/site_test.js [baseURL]  (default: local server on :8765)
// Checks every HTML page in vi/ and en/: HTTP errors, console errors, images loaded, deck slides, quiz click -> explanation,
// bank page renders + grading works, exam renders. Saves screenshots in tests/shots/.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const BASE = process.argv[2] || 'http://127.0.0.1:8765/';
function pages() {
  const out = [];
  for (const lang of ['vi', 'en']) {
    (function walk(d) {
      for (const f of fs.readdirSync(d)) {
        const p = path.join(d, f);
        if (fs.statSync(p).isDirectory()) walk(p); else if (f.endsWith('.html')) out.push(path.relative(ROOT, p));
      }
    })(path.join(ROOT, lang));
  }
  return out.sort();
}
(async () => {
  fs.mkdirSync(path.join(__dirname, 'shots'), { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  let fails = 0; const report = [];
  for (const rel of pages()) {
    const page = await ctx.newPage(); const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    page.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
    await page.goto(BASE + rel, { waitUntil: 'load' });
    const info = await page.evaluate(() => {
      const imgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.loading !== 'lazy').map(i => i.src);
      return { slides: document.querySelectorAll('.mdeck-slide').length, quiz: document.querySelectorAll('.quiz .qitem').length,
               bank: document.querySelectorAll('#bank .qitem').length, exam: document.querySelectorAll('#exam .qitem').length, broken: imgs,
               title: document.title };
    });
    // lazy images: scroll through page then re-check
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } });
    await page.waitForTimeout(300);
    const broken2 = await page.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src));
    if (info.quiz) {   // click first option of first quiz question -> explanation visible
      await page.evaluate(() => document.querySelector('.quiz .qitem .opt').click());
      const ok = await page.evaluate(() => !!document.querySelector('.quiz .qitem .explain.show'));
      if (!ok) errs.push('quiz explanation not shown');
    }
    if (info.bank) {
      await page.evaluate(() => document.querySelector('#bank .qitem .opt').click());
      const ok = await page.evaluate(() => !!document.querySelector('#bank .qitem .explain.show'));
      if (!ok) errs.push('bank explanation not shown');
    }
    if (rel.includes('/modules/') && info.slides < 15) errs.push('only ' + info.slides + ' slides');
    if (rel.includes('/practice/m') && info.bank === 0) errs.push('bank empty');
    if (rel.endsWith('exam/index.html') && info.exam === 0) errs.push('exam empty');
    const all = errs.concat(broken2.map(s => 'broken img ' + s));
    if (all.length) fails++;
    report.push(`${all.length ? 'FAIL' : 'ok  '} ${rel} slides=${info.slides} quiz=${info.quiz} bank=${info.bank} exam=${info.exam}` + (all.length ? '\n      ' + all.slice(0, 6).join('\n      ') : ''));
    if (/modules\/0[2-3]|index.html$|practice\/m02|exam/.test(rel) && !rel.includes('sources'))
      await page.screenshot({ path: path.join(__dirname, 'shots', rel.replace(/[\/]/g, '_') + '.png'), fullPage: false });
    await page.close();
  }
  console.log(report.join('\n'));
  console.log(`\n${report.length} pages, ${fails} with problems`);
  await browser.close(); process.exit(fails ? 1 : 0);
})();
