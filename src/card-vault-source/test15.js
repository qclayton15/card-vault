const { chromium, devices } = require('playwright');
const CARD='<svg xmlns="http://www.w3.org/2000/svg" width="245" height="342"><rect width="245" height="342" rx="12" fill="#41608f"/></svg>';
const LOGO='<svg xmlns="http://www.w3.org/2000/svg" width="400" height="160"><rect width="400" height="160" fill="#5a3f8f"/></svg>';
const routes = async p => {
  await p.route('**limitlesstcg**', r=>r.fulfill({status:200,contentType:'image/svg+xml',body:CARD}));
  await p.route('**cloudfront.net**', r=>r.fulfill({status:200,contentType:'image/svg+xml',body:LOGO}));
  await p.route('**bulbagarden**', r=>r.fulfill({status:403,body:''}));
};
const seed = () => localStorage.setItem('cardvault.v2', JSON.stringify({
  theme:'dark', view:'binder', setId:'PFL', tile:172, layout:'grid', ms:{}, hist:{},
  roi:{fee:25,ship:1.5,gem:40,scope:'own'}, c:{"PFL:125:base":{r:1},"POR:124:base":{r:1}} }));

async function check(p, label, open, panelSel, closeFn){
  // scroll the page down first so we can prove it doesn't move
  await p.evaluate(()=>window.scrollTo(0, 400));
  await p.waitForTimeout(300);
  const pageBefore = await p.evaluate(()=>window.scrollY);
  await open();
  await p.waitForTimeout(600);
  const locked = await p.evaluate(()=>document.body.classList.contains('locked'));
  const pane = p.locator(panelSel);
  const canScroll = await pane.evaluate(e=>e.scrollHeight - e.clientHeight);
  const box = await pane.boundingBox();
  await p.mouse.move(box.x + box.width/2, box.y + Math.min(box.height/2, 300));
  await p.mouse.wheel(0, 700);
  await p.waitForTimeout(500);
  const paneScrolled = await pane.evaluate(e=>e.scrollTop);
  const pageNow = await p.evaluate(()=>window.scrollY);
  console.log(`${label}: locked=${locked} scrollable=${canScroll>0}(${canScroll}px) panelScrolled=${paneScrolled}px pageMoved=${pageNow!==0}`);
  await closeFn();
  await p.waitForTimeout(500);
  const pageAfter = await p.evaluate(()=>window.scrollY);
  console.log(`   after close: body.locked=${await p.evaluate(()=>document.body.classList.contains('locked'))} scrollY restored ${pageBefore}→${pageAfter}`);
  return {paneScrolled, canScroll};
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport:{width:1400,height:820}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await routes(p); await p.addInitScript(seed);
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForTimeout(1300);

  await check(p, 'DESKTOP sets panel',
    async()=>{ await p.locator('#bAddSet').scrollIntoViewIfNeeded(); await p.locator('#bAddSet').click(); },
    '#setModal .setbody', async()=>p.keyboard.press('Escape'));

  await check(p, 'DESKTOP card modal',
    async()=>{ await p.locator('#grid .card[data-n="26"] .thumb').click(); },
    '#modal .mbody', async()=>p.keyboard.press('Escape'));

  // reopen sets and scroll all the way to the bottom to reach the last controls
  await p.locator('#bAddSet').scrollIntoViewIfNeeded();
  await p.locator('#bAddSet').click(); await p.waitForTimeout(500);
  await p.locator('#setModal .setbody').evaluate(e=>e.scrollTo(0, e.scrollHeight));
  await p.waitForTimeout(400);
  console.log('bottom controls reachable:', await p.locator('#bOther').isVisible(), '| whynote visible:', await p.locator('.whynote').isVisible());
  await p.screenshot({path:'sc-panel-bottom.png'});
  await p.keyboard.press('Escape');
  console.log('ERRORS:', errs.length?errs.join('|'):'none');
  await p.close();

  // ---- phone: touch drag inside the panel ----
  const ctx = await b.newContext({...devices['iPhone 13']});
  const m = await ctx.newPage();
  const merr=[]; m.on('pageerror',e=>merr.push(e.message));
  await routes(m); await m.addInitScript(seed);
  await m.goto('file:///home/claude/card-vault.html');
  await m.waitForTimeout(1300);
  await m.evaluate(()=>window.scrollTo(0,300));
  await m.locator('#bAddSet').scrollIntoViewIfNeeded();
  await m.locator('#bAddSet').tap(); await m.waitForTimeout(700);
  const pane = m.locator('#setModal .setbody');
  console.log('\nPHONE locked:', await m.evaluate(()=>document.body.classList.contains('locked')));
  const before = await pane.evaluate(e=>e.scrollTop);
  await pane.evaluate(e=>e.scrollBy(0, 500));
  await m.waitForTimeout(400);
  console.log('PHONE panel scrolled:', before, '→', await pane.evaluate(e=>e.scrollTop));
  console.log('PHONE page frozen at:', await m.evaluate(()=>window.scrollY));
  await m.screenshot({path:'sc-panel-phone.png'});
  await m.locator('#sx').tap(); await m.waitForTimeout(500);
  console.log('PHONE after close scrollY:', await m.evaluate(()=>window.scrollY), '| locked:', await m.evaluate(()=>document.body.classList.contains('locked')));
  console.log('MOBILE ERRORS:', merr.length?merr.join('|'):'none');
  await b.close();
})();
