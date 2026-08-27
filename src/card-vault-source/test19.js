const { chromium, devices } = require('playwright');
const CARD='<svg xmlns="http://www.w3.org/2000/svg" width="245" height="342"><rect width="245" height="342" rx="12" fill="#41608f"/></svg>';
const LOGO='<svg xmlns="http://www.w3.org/2000/svg" width="400" height="160"><rect width="400" height="160" fill="#6a4aa0"/></svg>';
const routes = async p => {
  await p.route('**limitlesstcg**', r=>r.fulfill({status:200,contentType:'image/svg+xml',body:CARD}));
  await p.route('**cloudfront.net**', r=>r.fulfill({status:200,contentType:'image/svg+xml',body:LOGO}));
  await p.route('**bulbagarden**', r=>r.fulfill({status:403,body:''}));
};
const seed = () => localStorage.setItem('cardvault.v2', JSON.stringify({
  theme:'dark', view:'binder', setId:'JTG', tile:172, layout:'grid',
  roi:{fee:25,ship:1.5,gem:40,scope:'all'},
  c:{"JTG:190:base":{r:1,p10:1},"DRI:231:base":{r:2},"JTG:69:jumbostamp":{r:1},
     "PRE:161:base":{r:1},"PRE:4:master":{r:2},"PRE:4:ball":{r:1},
     "MEW:199:base":{r:1},"MEW:4:rhcosmos":{r:1},"SSP:29:horizons":{r:1}} }));

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport:{width:1500,height:1000}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('dialog',d=>d.accept());
  p.on('console',m=>{if(m.type()==='error'&&!/ERR_TUNNEL|Failed to load/.test(m.text()))errs.push('C:'+m.text());});
  await routes(p); await p.addInitScript(seed);
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForTimeout(2000);

  console.log('tabs:', await p.locator('#sets .settab[data-s]').evaluateAll(n=>n.map(x=>x.dataset.s)));

  for (const [id, n, checks] of [['MEW',207,[[4,'Charmander'],[49,'Venomoth'],[68,'Machamp holo-only'],[207,'Basic Psychic']]],
                                 ['SSP',252,[[29,'Fuecoco horizons'],[176,'ACE SPEC w/ reverse'],[188,'TM colon'],[252,'Jet Energy']]],
                                 ['PRE',180,[[4,'Budew'],[51,'Lucario'],[96,'Trainer'],[131,'ACE SPEC'],[161,'Umbreon']]],
                                 ['JTG',190,[[26,'N’s'],[69,'Mimikyu'],[142,'Billy'],[190,'Spiky']]],
                                 ['DRI',244,[[1,'Pinsir'],[114,'Nidoran'],[174,'Watchtower'],[244,'Levincia']]]]) {
    await p.locator(`.settab[data-s="${id}"]`).click(); await p.waitForTimeout(1200);
    console.log(`\n--- ${id} ---`);
    console.log('cards:', await p.locator('#grid .card').count(), 'expected', n);
    console.log('hero sub:', await p.locator('#hSub').innerText());
    console.log('rarity bands:', await p.evaluate(()=>{const o={};curSet().cards.forEach(c=>o[c.rarity]=(o[c.rarity]||0)+1);return o;}));
    for (const [num] of checks) {
      await p.locator(`#grid .card[data-n="${num}"] .thumb`).click(); await p.waitForTimeout(500);
      const name = await p.locator('#modal h2, #modal .mtitle').first().innerText();
      const slots = await p.locator('#modal .vhead b').allInnerTexts();
      const links = await p.locator('#modal a[href*="pricecharting"]').evaluateAll(a=>a.map(x=>x.href.split('/').pop()));
      console.log(` #${num}`, name.replace(/\s+/g,' ').slice(0,44), '|', slots.join(', '), '|', links.join(' '));
      await p.keyboard.press('Escape'); await p.waitForTimeout(250);
    }
    const stats = await p.evaluate(()=>{const s=curSet();
      return {slots:s.cards.reduce((a,c)=>a+c.v.length,0),
              noRaw:s.cards.filter(c=>c.v[0].raw==null).length,
              dupIds:s.cards.filter(c=>new Set(c.v.map(v=>v.id)).size!==c.v.length).length};});
    console.log('slots:', stats.slots, '| base cards missing raw:', stats.noRaw, '| dup slot ids:', stats.dupIds);
    console.log('rarity filter order:', await p.locator('#fRar option').allInnerTexts());
    console.log('reverse slots:', await p.evaluate(()=>{const o={};curSet().cards.forEach(c=>c.v.forEach(v=>{if(REV.has(v.id))o[v.id]=(o[v.id]||0)+1;}));return o;}));
  }

  // cross-set surfaces
  await p.locator('.tab[data-v="roi"]').click(); await p.waitForTimeout(900);
  await p.locator('#roiScope button[data-v="all"]').click(); await p.waitForTimeout(700);
  console.log('\nROI rows (all sets):', await p.locator('#roi tr').count(), '|', await p.locator('#roiCount').innerText());
  console.log('ROI top:', (await p.locator('#roi tr').first().innerText()).replace(/\t/g,' | '));
  await p.locator('.tab[data-v="bulk"]').click(); await p.waitForTimeout(900);
  console.log('bulk rows:', await p.locator('#bulk tr').count());
  const rv = p.locator('#bulkOnly, #bulkFilter, [data-bulk="rev"]');
  console.log('bulk filter present:', await rv.count());
  await p.locator('.tab[data-v="binder"]').click(); await p.waitForTimeout(700);

  await p.locator('.settab[data-s="DRI"]').click(); await p.waitForTimeout(900);
  await p.screenshot({path:'/home/claude/t19-dri.png'});
  await p.locator('.settab[data-s="JTG"]').click(); await p.waitForTimeout(900);
  await p.screenshot({path:'/home/claude/t19-jtg.png'});
  console.log('ERRORS:', errs.length?errs:'none');

  const m = await b.newPage({...devices['iPhone 13'], hasTouch:true});
  const merr=[]; m.on('pageerror',e=>merr.push(e.message));
  await routes(m); await m.addInitScript(seed);
  await m.goto('file:///home/claude/card-vault.html'); await m.waitForTimeout(2000);
  console.log('\nPHONE overflow:', await m.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth));
  await m.locator('.settab[data-s="DRI"]').click(); await m.waitForTimeout(1200);
  console.log('PHONE DRI cards:', await m.locator('#grid .card').count(),
              '| overflow:', await m.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth));
  await m.screenshot({path:'/home/claude/t19-phone.png'});
  console.log('MOBILE ERRORS:', merr.length?merr:'none');
  await b.close();
})();
