const { chromium, devices } = require('playwright');
const CARD = c => `<svg xmlns="http://www.w3.org/2000/svg" width="245" height="342"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c}"/><stop offset="1" stop-color="#161d2c"/></linearGradient></defs><rect width="245" height="342" rx="12" fill="url(#g)"/><rect x="16" y="16" width="213" height="152" rx="8" fill="#ffffff22"/><rect x="16" y="184" width="140" height="12" rx="6" fill="#ffffff33"/><rect x="16" y="205" width="185" height="9" rx="4" fill="#ffffff1a"/></svg>`;
const route = r => { const n=(r.request().url().match(/_(\d{3})_/)||[])[1]|0;
  r.fulfill({status:200,contentType:'image/svg+xml',body:CARD(n>=118?'#c04a8a':n>=100?'#c2703a':n>=89?'#8a5ac8':'#3b5a86')}); };
const seed = () => localStorage.setItem('cardvault.v2', JSON.stringify({
  theme:'dark', view:'binder', setId:'POR', tile:172, layout:'grid', ms:{},
  roi:{fee:25,ship:1.5,gem:40,scope:'own'},
  hist:{POR:[{d:'2026-08-01',v:120,c:3},{d:'2026-08-09',v:340.5,c:7},{d:'2026-08-18',v:512.75,c:11}]},
  c:{"POR:124:base":{r:1},"POR:121:base":{r:2},"POR:50:base":{r:1,w:1},"POR:1:rh":{r:3},"POR:94:base":{p10:1}} }));
(async () => {
  const b = await chromium.launch();
  for (const [name, dev] of [['iphone', devices['iPhone 13']], ['pixel', devices['Pixel 5']], ['ipad', devices['iPad Mini']]]) {
    const ctx = await b.newContext({...dev});
    const p = await ctx.newPage();
    const errs=[]; p.on('pageerror',e=>errs.push(e.message));
    await p.route('**limitlesstcg**', route);
    await p.addInitScript(seed);
    await p.goto('file:///home/claude/card-vault.html');
    await p.waitForTimeout(1300);
    const w = await p.evaluate(()=>innerWidth);
    console.log(`\n== ${name} (${w}px) ==`);
    console.log('overflow:', await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth));
    const heroH = await p.locator('#hero').evaluate(e=>Math.round(e.getBoundingClientRect().height));
    console.log('hero height:', heroH+'px', '| grid cols:', await p.evaluate(()=>getComputedStyle(document.querySelector('#grid')).gridTemplateColumns.split(' ').length));
    console.log('tab widths ok:', await p.locator('.tab').evaluateAll(ns=>ns.map(n=>Math.round(n.getBoundingClientRect().width)).join(',')));
    if (name==='iphone') await p.screenshot({path:'m2-binder.png'});
    for (const v of ['bulk','roi','wish','trade','history']) {
      await p.locator(`.tab[data-v="${v}"]`).scrollIntoViewIfNeeded();
      await p.locator(`.tab[data-v="${v}"]`).tap();
      await p.waitForTimeout(650);
      const of = await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
      if (of > 1) console.log('  !! overflow on', v, of);
      if (name==='iphone') await p.screenshot({path:`m2-${v}.png`});
    }
    console.log('tabs all clean, errors:', errs.length?errs.join('|'):'none');
    await ctx.close();
  }
  await b.close();
})();
