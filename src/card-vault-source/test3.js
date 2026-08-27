const { chromium } = require('playwright');
const SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="245" height="342"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#46628c"/><stop offset="1" stop-color="#20293a"/></linearGradient></defs><rect width="245" height="342" rx="12" fill="url(#g)"/><rect x="14" y="14" width="217" height="158" rx="7" fill="#5d7ba6"/><rect x="14" y="188" width="150" height="11" rx="5" fill="#7c94b8"/><rect x="14" y="208" width="190" height="9" rx="4" fill="#4d6party"/></svg>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1500, height: 1000 } });
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  p.on('console', m => { if (m.type()==='error' && !/ERR_TUNNEL|Failed to load resource/.test(m.text())) errs.push('CONSOLE: '+m.text()); });
  await p.route('**limitlesstcg**', r => r.fulfill({status:200, contentType:'image/svg+xml', body:SVG}));

  // seed a v1 save to test migration
  await p.addInitScript(() => {
    localStorage.setItem('cardvault.v1', JSON.stringify({
      "PFL:125": {r:1,p9:0,p10:0}, "PFL:130": {r:0,p9:0,p10:1}, "PFL:11": {r:3,p9:0,p10:0}
    }));
  });
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForTimeout(1400);
  // this suite is written against Phantasmal Flames — pin it, don't rely on set order
  await p.locator('.settab[data-s="PFL"]').click();
  await p.waitForTimeout(900);
  console.log('MIGRATED stats:', (await p.locator('#hero').innerText()).replace(/\n/g,' | '));
  console.log('cards:', await p.locator('#grid .card').count());

  // wishlist via keyboard
  await p.locator('#grid .card[data-n="106"] .thumb').hover();
  await p.waitForTimeout(150);
  await p.locator('#grid .card[data-n="106"] [data-star]').click();
  await p.waitForTimeout(200);
  console.log('wish pill:', await p.locator('#nWish').innerText());

  // modal + variants
  await p.locator('#grid .card[data-n="26"] .thumb').click();
  await p.waitForTimeout(500);
  console.log('variant blocks on #26:', await p.locator('#modal .vblock').count());
  console.log('modal head:', (await p.locator('#modal .sub').innerText()).replace(/\n/g,' '));
  await p.locator('#modal .vblock').nth(2).locator('[data-f][data-d="1"]').first().click();
  await p.waitForTimeout(200);
  console.log('after +1 cosmos raw, card total:', await p.locator('#mtot').innerText());
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(350);
  console.log('arrow-right modal now:', await p.locator('#modal h2').innerText());
  await p.keyboard.press('Escape'); await p.waitForTimeout(250);

  // bulk entry
  await p.locator('.tab[data-v="bulk"]').click(); await p.waitForTimeout(600);
  console.log('bulk rows:', await p.locator('#bulk tr').count(), '|', await p.locator('#bCount').innerText());
  const rows = p.locator('#bulk tr');
  await rows.nth(1).locator('[data-q="r"]').fill('4');
  await p.waitForTimeout(250);
  console.log('bulk row1 value cell:', await rows.nth(1).locator('[data-sv]').innerText());
  await p.selectOption('#bVar','rh'); await p.waitForTimeout(400);
  console.log('reverse-holo slots:', await p.locator('#bulk tr').count());
  await p.selectOption('#bVar','promo'); await p.waitForTimeout(400);
  console.log('promo slots:', await p.locator('#bulk tr').count());
  await p.selectOption('#bVar','all');

  // roi
  await p.locator('.tab[data-v="roi"]').click(); await p.waitForTimeout(600);
  console.log('ROI rows (own):', await p.locator('#roi tr').count(), '|', await p.locator('#roiCount').innerText());
  console.log('ROI top row:', (await p.locator('#roi tr').first().innerText()).replace(/\t/g,' | '));
  await p.locator('#roiScope button[data-v="all"]').click(); await p.waitForTimeout(500);
  console.log('ROI rows (all):', await p.locator('#roi tr').count(), '|', await p.locator('#roiCount').innerText());
  console.log('ROI summary:', await p.locator('#roiSum').innerText());
  await p.locator('#roiGem').fill('80'); await p.waitForTimeout(400);
  console.log('at 80% gem:', await p.locator('#roiSum').innerText());
  await p.locator('#roiGem').fill('40');
  await p.locator('#roiScope button[data-v="own"]').click();

  // wishlist + trades
  await p.locator('.tab[data-v="wish"]').click(); await p.waitForTimeout(400);
  console.log('wish rows:', await p.locator('#wish tr').count(), '|', await p.locator('#wishSum').innerText());
  await p.locator('.tab[data-v="trade"]').click(); await p.waitForTimeout(400);
  console.log('trade rows:', await p.locator('#trade tr').count(), '|', await p.locator('#tradeSum').innerText());

  // history: fake older snapshots then render
  await p.evaluate(() => {
    const s = JSON.parse(localStorage.getItem('cardvault.v2'));
    s.hist = { PFL: [
      {d:'2026-07-20', v: 640.10, c: 4},{d:'2026-07-27', v: 712.44, c: 6},
      {d:'2026-08-03', v: 690.02, c: 6},{d:'2026-08-10', v: 861.75, c: 9},
      ...(s.hist.PFL || [])] };
    localStorage.setItem('cardvault.v2', JSON.stringify(s));
  });
  console.log('DBG in-memory S.hist before reload:', await p.evaluate(()=>JSON.stringify(S.hist)));
  console.log('DBG ls hist after inject:', await p.evaluate(()=>JSON.parse(localStorage.getItem('cardvault.v2')).hist.PFL.length));
  await p.waitForTimeout(300);
  // Chromium under Playwright intermittently drops file:// localStorage across a reload,
  // which has nothing to do with the app — carry the state over explicitly.
  const carried = await p.evaluate(()=>localStorage.getItem('cardvault.v2'));
  await p.addInitScript(v => { if(!localStorage.getItem('cardvault.v2')) localStorage.setItem('cardvault.v2', v); }, carried);
  await p.reload(); await p.waitForTimeout(1200);
  console.log('DBG ls raw after reload:', await p.evaluate(()=>JSON.parse(localStorage.getItem('cardvault.v2')).hist && Object.keys(JSON.parse(localStorage.getItem('cardvault.v2')).hist).map(k=>k+'='+JSON.parse(localStorage.getItem('cardvault.v2')).hist[k].length).join(',')));
  console.log('DBG S.hist after reload:', await p.evaluate(()=>S.hist.PFL.length));
  await p.locator('.tab[data-v="history"]').click(); await p.waitForTimeout(700);
  console.log('chart sub:', await p.locator('#chartSub').innerText());
  console.log('hist rows:', await p.locator('#histTbl tr').count());
  await p.locator('#hit').hover({position:{x:300,y:80}}); await p.waitForTimeout(350);
  console.log('tooltip:', (await p.locator('#ctip').innerText()).replace(/\n/g,' · '), '| visible:', await p.locator('#ctip').evaluate(e=>e.classList.contains('on')));
  await p.screenshot({path:'s-hist.png'});

  // light mode
  await p.locator('#bTheme').click(); await p.waitForTimeout(500);
  console.log('theme now:', await p.evaluate(()=>document.documentElement.dataset.theme));
  await p.screenshot({path:'s-light-hist.png'});
  await p.locator('.tab[data-v="binder"]').click(); await p.waitForTimeout(700);
  await p.screenshot({path:'s-light-binder.png'});
  await p.locator('#bTheme').click(); await p.waitForTimeout(400);

  // keyboard nav in grid
  await p.locator('body').click({position:{x:5,y:400}});
  await p.keyboard.press('ArrowRight'); await p.keyboard.press('ArrowRight');
  await p.keyboard.press('ArrowDown'); await p.waitForTimeout(250);
  console.log('selected card:', await p.locator('#grid .card.sel').getAttribute('data-n'));
  await p.keyboard.press('+'); await p.waitForTimeout(250);
  console.log('after + :', (await p.locator('#hero').innerText()).split('\n').slice(6,9).join(' | '));

  // exports
  const [csv] = await Promise.all([p.waitForEvent('download'), p.locator('#bMenu').click().then(()=>p.locator('#mCSV').click())]);
  console.log('csv file:', csv.suggestedFilename());
  const path = await csv.path();
  const lines = require('fs').readFileSync(path,'utf8').split('\n');
  console.log('csv lines:', lines.length, '| header:', lines[0].slice(0,90));
  console.log('csv sample:', lines[1]);

  // print checklist
  await p.evaluate(()=>{ document.querySelector('#bMenu').click(); });
  await p.waitForTimeout(150);
  await p.evaluate(()=>{ const o=window.print; window.print=()=>{}; document.querySelector('#mPrint').click(); window.print=o; });
  await p.waitForTimeout(400);
  console.log('print area rows:', await p.locator('#print tbody tr').count());
  console.log('print header:', await p.locator('#print .pm').innerText());

  // size slider + list view
  await p.locator('#tile').fill('120'); await p.waitForTimeout(300);
  console.log('tile var:', await p.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--tile')));
  await p.locator('#fLay button[data-v="list"]').click(); await p.waitForTimeout(400);
  console.log('list rows:', await p.locator('#list tr').count());
  await p.locator('#fLay button[data-v="grid"]').click();
  await p.locator('#tile').fill('172'); await p.waitForTimeout(300);

  // filters
  await p.locator('#fOwn button[data-v="wish"]').click(); await p.waitForTimeout(300);
  console.log('wish filter cards:', await p.locator('#grid .card').count());
  await p.locator('#fOwn button[data-v="all"]').click();
  await p.waitForTimeout(1500);
  await p.screenshot({path:'s-binder.png'});
  await p.locator('#grid .card[data-n="130"] .thumb').click(); await p.waitForTimeout(900);
  await p.screenshot({path:'s-modal.png'});

  console.log('ERRORS:', errs.length ? errs.join('\n') : 'none');
  await b.close();
})();
