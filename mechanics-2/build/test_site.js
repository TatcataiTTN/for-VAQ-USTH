const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new'
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push('PAGEERROR: ' + err.message));

  await page.goto('http://localhost:8177/', { waitUntil: 'networkidle0', timeout: 20000 });
  await new Promise(r => setTimeout(r, 800));

  const homeText = await page.$eval('#content', el => el.innerText.slice(0, 200));
  console.log('HOME TEXT:', homeText.replace(/\n/g,' | '));

  // click through every nav button and check for KaTeX errors / parse errors visible in text
  const buttons = await page.$$eval('nav button', btns => btns.map(b => b.textContent));
  console.log('NAV BUTTONS:', buttons.length, buttons);

  for (let i = 1; i < buttons.length; i++) { // skip "Trang chủ"
    await page.evaluate(idx => {
      document.querySelectorAll('nav button')[idx].click();
    }, i);
    await new Promise(r => setTimeout(r, 500));
    const bodyText = await page.$eval('#content', el => el.innerText);
    const katexErr = await page.$$eval('.katex-error', els => els.length);
    console.log(`[${i}] "${buttons[i]}" -> length=${bodyText.length} katex_errors=${katexErr}`);
    if (katexErr > 0) {
      const sample = await page.$$eval('.katex-error', els => els.slice(0,3).map(e=>e.textContent));
      console.log('   KATEX ERROR SAMPLE:', sample);
    }
  }

  console.log('CONSOLE ERRORS:', errors.length);
  errors.slice(0, 20).forEach(e => console.log(' -', e));

  await browser.close();
})();
