const { chromium, devices } = require('playwright');
const CARD='<svg xmlns="http://www.w3.org/2000/svg" width="245" height="342"><rect width="245" height="342" rx="12" fill="#41608f"/></svg>';
const LOGO=t=>`<svg xmlns="http://www.w3.org/2000/svg" width="400" height="160"><text x="200" y="60" text-anchor="middle" font-family="Impact,sans-serif" font-size="30" fill="#ffd76a" stroke="#2a1400" stroke-width="4" paint-order="stroke">MEGA EVOLUTION</text><text x="200" y="125" text-anchor="middle" font-family="Impact,sans-serif" font-size="46" fill="#e07bff" stroke="#140a1e" stroke-width="6" paint-order="stroke">${t}</text></svg>`;
const routes = async p => {
  await p.route('**limitlesstcg**', r=>r.fulfill({status:200,contentType:'image/svg+xml',body:CARD}));
  await p.route('**cloudfront.net**', r=>{
    const m=(r.request().url().match(/([a-z0-9pt]+)\.png/)||[])[1]||'SET';
    r.fulfill({status:200,contentType:'image/svg+xml',body:LOGO(m.toUpperCase())});
  });
  await p.route('**bulbagarden**', r=>r.fulfill({status:403,body:''}));
};
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport:{width:1420,height:1000}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  p.on('dialog', d => d.accept());
  await routes(p);
  await p.addInitScript(()=>localStorage.setItem('cardvault.v2', JSON.stringify({
    theme:'dark', view:'binder', setId:'PFL', tile:172, layout:'grid', ms:{}, hist:{},
    roi:{fee:25,ship:1.5,gem:40,scope:'own'},
    c:{"PFL:125:base":{r:1},"PFL:11:base":{r:3},"POR:124:base":{r:1}} })));
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForTimeout(1300);

  console.log('ghost button:', await p.locator('#bAddSet').innerText());
  await p.locator('#bAddSet').click(); await p.waitForTimeout(600);
  console.log('panel open:', await p.locator('#setov').evaluate(e=>e.classList.contains('on')));
  console.log('managed rows:', await p.locator('#setModal .mgrow').count());
  console.log('addable cards:', await p.locator('#setModal .addcard').count());
  console.log('groups:', await p.locator('#setModal .addhead').allInnerTexts());
  await p.screenshot({path:'s-setpanel.png'});

  // reorder
  console.log('order before:', await p.locator('#sets .settab[data-s]').evaluateAll(n=>n.map(x=>x.dataset.s)));
  await p.locator('#setModal [data-mv="POR"][data-d="-1"]').click();
  await p.waitForTimeout(500);
  console.log('order after  :', await p.locator('#sets .settab[data-s]').evaluateAll(n=>n.map(x=>x.dataset.s)));
  console.log('S.order:', await p.evaluate(()=>JSON.stringify(S.order)));

  // copy request
  await p.context().grantPermissions(['clipboard-read','clipboard-write']);
  await p.locator('#setModal [data-req="Chaos Rising"]').click();
  await p.waitForTimeout(400);
  console.log('clipboard:', await p.evaluate(()=>navigator.clipboard.readText().catch(e=>'ERR')));
  console.log('toast:', await p.locator('#toast').innerText());

  // other set field
  await p.fill('#otherSet','Twilight Masquerade');
  await p.locator('#bOther').click(); await p.waitForTimeout(400);
  console.log('clipboard2:', await p.evaluate(()=>navigator.clipboard.readText().catch(e=>'ERR')));

  // hide a set with data logged (dialog auto-accepted)
  await p.locator('#setModal [data-hide="PFL"]').click();
  await p.waitForTimeout(700);
  console.log('visible tabs after hide:', await p.locator('#sets .settab[data-s]').evaluateAll(n=>n.map(x=>x.dataset.s)));
  console.log('active set now:', await p.evaluate(()=>S.setId), '| hidden:', await p.evaluate(()=>JSON.stringify(S.hidden)));
  console.log('collection kept:', await p.evaluate(()=>Object.keys(S.c).filter(k=>k.startsWith('PFL')).length + ' PFL slots still in state'));
  console.log('hero pill:', (await p.locator('#hPills').innerText()).replace(/\n/g,' | '));

  // try hiding the last one
  await p.locator('#setModal [data-hide="POR"]').click(); await p.waitForTimeout(500);
  console.log('blocked last-hide:', await p.locator('#toast').innerText());

  // restore
  await p.locator('#setModal [data-show="PFL"]').click(); await p.waitForTimeout(700);
  console.log('after restore:', await p.locator('#sets .settab[data-s]').evaluateAll(n=>n.map(x=>x.dataset.s)));
  console.log('PFL value back:', await p.evaluate(()=>{ S.setId='PFL'; return 1; }) && await p.locator('#hVal').innerText());
  await p.keyboard.press('Escape'); await p.waitForTimeout(300);
  console.log('panel closed:', !(await p.locator('#setov').evaluate(e=>e.classList.contains('on'))));
  console.log('ERRORS:', errs.length?errs.join('|'):'none');
  await p.close();

  // mobile
  const ctx = await b.newContext({...devices['iPhone 13']});
  const m = await ctx.newPage();
  const merr=[]; m.on('pageerror',e=>merr.push(e.message));
  await routes(m);
  await m.goto('file:///home/claude/card-vault.html');
  await m.waitForTimeout(1200);
  await m.locator('#bAddSet').scrollIntoViewIfNeeded();
  await m.locator('#bAddSet').tap(); await m.waitForTimeout(700);
  console.log('\nmobile overflow:', await m.evaluate(()=>document.documentElement.scrollWidth-innerWidth));
  await m.screenshot({path:'s-setpanel-mobile.png'});
  console.log('MOBILE ERRORS:', merr.length?merr.join('|'):'none');
  await b.close();
})();
