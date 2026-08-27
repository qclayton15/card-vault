const { chromium, devices } = require('playwright');
const CARD='<svg xmlns="http://www.w3.org/2000/svg" width="245" height="342"><rect width="245" height="342" rx="12" fill="#41608f"/></svg>';
const LOGO='<svg xmlns="http://www.w3.org/2000/svg" width="400" height="160"><rect width="400" height="160" fill="#6a4aa0"/></svg>';
const routes = async p => {
  await p.route('**limitlesstcg**', r=>r.fulfill({status:200,contentType:'image/svg+xml',body:CARD}));
  await p.route('**cloudfront.net**', r=>r.fulfill({status:200,contentType:'image/svg+xml',body:LOGO}));
  await p.route('**bulbagarden**', r=>r.fulfill({status:403,body:''}));
};
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport:{width:1500,height:1000}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('dialog',d=>d.accept());
  p.on('console',m=>{if(m.type()==='error'&&!/ERR_TUNNEL|Failed to load/.test(m.text()))errs.push('C:'+m.text());});
  await routes(p);
  await p.addInitScript(()=>localStorage.setItem('cardvault.v2', JSON.stringify({
    theme:'dark', view:'binder', setId:'POR', tile:172, layout:'grid',
    roi:{fee:25,ship:1.5,gem:40,scope:'own'}, ms:{'PFL:first':1},
    hist:{PFL:[{d:'2026-08-10',v:900,c:6}]},
    c:{"PFL:125:base":{r:1},"POR:124:base":{r:1},"AHE:284:base":{r:1}} })));
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForTimeout(2000);

  console.log('tabs:', await p.locator('#sets .settab[data-s]').evaluateAll(n=>n.map(x=>x.dataset.s)));
  console.log('old data intact:', await p.evaluate(()=>Object.keys(S.c).sort().join(', ')));

  await p.locator('.settab[data-s="MEV"]').click(); await p.waitForTimeout(1200);
  console.log('\n--- MEGA EVOLUTION ---');
  console.log('cards:', await p.locator('#grid .card').count());
  console.log('hero sub:', await p.locator('#hSub').innerText());
  await p.locator('#grid .card[data-n="1"] .thumb').click(); await p.waitForTimeout(700);
  console.log('card 1 slots:', await p.locator('#modal .vhead b').allInnerTexts());
  await p.keyboard.press('Escape'); await p.waitForTimeout(300);
  await p.locator('#grid .card[data-n="88"] .thumb').click(); await p.waitForTimeout(700);
  console.log('card 88 slots:', await p.locator('#modal .vhead b').allInnerTexts());
  await p.keyboard.press('Escape'); await p.waitForTimeout(300);
  await p.locator('#grid .card[data-n="73"] .thumb').click(); await p.waitForTimeout(700);
  console.log('card 73 (holo-only) slots:', await p.locator('#modal .vhead b').allInnerTexts(),
              '| base raw:', await p.locator('#modal .pin').first().inputValue());
  await p.keyboard.press('Escape'); await p.waitForTimeout(300);

  await p.locator('.tab[data-v="bulk"]').click(); await p.waitForTimeout(1000);
  console.log('\nslots:', await p.locator('#bulk tr').count());
  for(const [v,l] of [['base','base'],['rh','reverses'],['promo','promos']]){
    await p.selectOption('#bVar', v); await p.waitForTimeout(600);
    console.log('  '+l+':', await p.locator('#bulk tr').count());
  }
  await p.selectOption('#bVar','all');

  await p.locator('.tab[data-v="roi"]').click(); await p.waitForTimeout(800);
  await p.locator('#roiScope button[data-v="all"]').click(); await p.waitForTimeout(900);
  console.log('\nROI:', await p.locator('#roiCount').innerText());
  console.log('top:', (await p.locator('#roi tr').first().innerText()).replace(/\t/g,' | '));

  await p.locator('.tab[data-v="binder"]').click(); await p.waitForTimeout(500);
  await p.locator('#grid .card[data-n="188"] [data-inc]').click(); await p.waitForTimeout(700);
  console.log('\nafter +Mega Lucario HR:', await p.locator('#hVal').innerText());
  console.log('pills:', (await p.locator('#hPills').innerText()).replace(/\n/g,' | '));

  // sets panel
  await p.locator('#bAddSet').click(); await p.waitForTimeout(700);
  console.log('\nmanaged rows:', await p.locator('#setModal .mgrow').count(),
              '| addable:', await p.locator('#setModal .addcard').count());
  console.log('groups:', (await p.locator('#setModal .addhead').allInnerTexts()).join(' / ').replace(/\n/g,' '));
  await p.keyboard.press('Escape'); await p.waitForTimeout(400);

  const [csv] = await Promise.all([p.waitForEvent('download'), p.locator('#bMenu').click().then(()=>p.locator('#mCSV').click())]);
  console.log('CSV:', csv.suggestedFilename(), require('fs').readFileSync(await csv.path(),'utf8').split('\n').length-1, 'rows');
  await p.waitForTimeout(1000);
  await p.screenshot({path:'me-binder.png', clip:{x:0,y:0,width:1500,height:600}});
  console.log('ERRORS:', errs.length?errs.join('\n'):'none');
  await p.close();

  const ctx = await b.newContext({...devices['iPhone 13']});
  const m = await ctx.newPage(); const merr=[]; m.on('pageerror',e=>merr.push(e.message));
  await routes(m);
  await m.addInitScript(()=>localStorage.setItem('cardvault.v2', JSON.stringify({theme:'dark',view:'binder',setId:'MEV',tile:172,layout:'grid',ms:{},hist:{},roi:{fee:25,ship:1.5,gem:40,scope:'own'},c:{}})));
  await m.goto('file:///home/claude/card-vault.html');
  await m.waitForTimeout(1800);
  console.log('\nPHONE overflow:', await m.evaluate(()=>document.documentElement.scrollWidth-innerWidth),
              '| set tabs:', await m.locator('#sets .settab[data-s]').count());
  await m.locator('.tab[data-v="bulk"]').tap(); await m.waitForTimeout(1400);
  console.log('PHONE bulk rows:', await m.locator('#bulk tr').count(), '| overflow:', await m.evaluate(()=>document.documentElement.scrollWidth-innerWidth));
  console.log('MOBILE ERRORS:', merr.length?merr.join('|'):'none');
  await b.close();
})();
