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
  // existing v2 collection must survive
  await p.addInitScript(()=>localStorage.setItem('cardvault.v2', JSON.stringify({
    theme:'dark', view:'binder', setId:'PFL', tile:172, layout:'grid',
    roi:{fee:25,ship:1.5,gem:40,scope:'own'}, ms:{'PFL:first':1},
    hist:{PFL:[{d:'2026-08-10',v:900,c:6}]},
    c:{"PFL:125:base":{r:1},"POR:124:base":{r:1}} })));
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForTimeout(1800);

  console.log('set tabs:', await p.locator('#sets .settab[data-s]').evaluateAll(n=>n.map(x=>x.dataset.s)));
  console.log('old data intact:', await p.evaluate(()=>JSON.stringify(S.c)));

  await p.locator('.settab[data-s="AHE"]').click(); await p.waitForTimeout(1200);
  console.log('\n--- ASCENDED HEROES ---');
  console.log('cards rendered:', await p.locator('#grid .card').count());
  console.log('hero:', await p.locator('#hVal').innerText(), '|', await p.locator('#hSub').innerText());
  console.log('ring %:', await p.locator('.settab[data-s="AHE"] .ring b').innerText());
  const rar = await p.locator('#fRar option').allInnerTexts();
  console.log('rarity filter:', rar.join(', '));

  // card 1 should have three slots
  await p.locator('#grid .card[data-n="1"] .thumb').click(); await p.waitForTimeout(700);
  console.log('card 1 variants:', await p.locator('#modal .vhead b').allInnerTexts());
  console.log('card 1 header:', (await p.locator('#modal .sub').innerText()).replace(/\n/g,' '));
  await p.locator('#modal .vblock').nth(1).locator('[data-f][data-d="1"]').first().click();
  await p.waitForTimeout(300);
  console.log('after +1 Ball reverse:', await p.locator('#mtot').innerText());
  await p.keyboard.press('Escape'); await p.waitForTimeout(400);

  // bulk filters
  await p.locator('.tab[data-v="bulk"]').click(); await p.waitForTimeout(1200);
  console.log('\nall slots:', await p.locator('#bulk tr').count());
  for (const [v,label] of [['base','base'],['rh','reverse holos'],['promo','promos']]) {
    await p.selectOption('#bVar', v); await p.waitForTimeout(700);
    console.log(`  ${label}:`, await p.locator('#bulk tr').count());
  }
  await p.selectOption('#bVar','all');

  // roi + chase card
  await p.locator('.tab[data-v="roi"]').click(); await p.waitForTimeout(900);
  await p.locator('#roiScope button[data-v="all"]').click(); await p.waitForTimeout(900);
  console.log('\nROI candidates:', await p.locator('#roiCount').innerText());
  console.log('ROI top:', (await p.locator('#roi tr').first().innerText()).replace(/\t/g,' | '));

  // hero top card + all-sets pill
  await p.locator('.tab[data-v="binder"]').click(); await p.waitForTimeout(600);
  await p.locator('#grid .card[data-n="284"] [data-inc]').click(); await p.waitForTimeout(700);
  console.log('\nafter +Mega Gengar SIR:', await p.locator('#hVal').innerText());
  console.log('hero card:', (await p.locator('#heroR .hcap').innerText()).replace(/\n/g,' · '));
  console.log('pills:', (await p.locator('#hPills').innerText()).replace(/\n/g,' | '));

  // csv + print for the new set
  const [csv] = await Promise.all([p.waitForEvent('download'), p.locator('#bMenu').click().then(()=>p.locator('#mCSV').click())]);
  const lines = require('fs').readFileSync(await csv.path(),'utf8').split('\n');
  console.log('\nCSV:', csv.suggestedFilename(), '|', lines.length-1, 'rows');
  console.log('CSV row 2:', lines[2].slice(0,110));
  await p.evaluate(()=>{ window.print=()=>{}; document.querySelector('#bMenu').click(); document.querySelector('#mPrint').click(); });
  await p.waitForTimeout(700);
  console.log('print rows:', await p.locator('#print tbody tr').count(), '|', (await p.locator('#print .pm').innerText()).replace(/\n/g,' '));

  await p.waitForTimeout(1200);
  await p.screenshot({path:'a-binder.png', clip:{x:0,y:0,width:1500,height:620}});
  console.log('\nERRORS:', errs.length?errs.join('\n'):'none');
  await p.close();

  const ctx = await b.newContext({...devices['iPhone 13']});
  const m = await ctx.newPage(); const merr=[]; m.on('pageerror',e=>merr.push(e.message));
  await routes(m);
  await m.addInitScript(()=>localStorage.setItem('cardvault.v2', JSON.stringify({theme:'dark',view:'binder',setId:'AHE',tile:172,layout:'grid',ms:{},hist:{},roi:{fee:25,ship:1.5,gem:40,scope:'own'},c:{}})));
  await m.goto('file:///home/claude/card-vault.html');
  await m.waitForTimeout(1600);
  console.log('PHONE overflow:', await m.evaluate(()=>document.documentElement.scrollWidth-innerWidth), '| tabs:', await m.locator('#sets .settab[data-s]').count());
  await m.locator('.tab[data-v="bulk"]').tap(); await m.waitForTimeout(1400);
  console.log('PHONE bulk rows:', await m.locator('#bulk tr').count(), '| overflow:', await m.evaluate(()=>document.documentElement.scrollWidth-innerWidth));
  console.log('MOBILE ERRORS:', merr.length?merr.join('|'):'none');
  await b.close();
})();
