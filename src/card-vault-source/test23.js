// The game profile moved out of app.js and into DATA.game. Nothing about the Pokémon
// build may change as a result — above all the storage key, because the collection
// lives under it and a rename would orphan every card the user has logged.
const { chromium } = require('playwright');
const FILE = 'file:///home/claude/card-vault.html';
let fails = 0;
const ok = (n, c, x = '') => { console.log((c ? '  ok   ' : '  FAIL ') + n + (c ? '' : '  ' + x)); if (!c) fails++; };

// A collection written by the pre-refactor build: real slots, wishlist, price
// override, history and milestones, across three sets.
const LEGACY = {
  theme: 'light', view: 'binder', setId: 'DRI', tile: 200, layout: 'list',
  c: {
    'MEW:45:base':  { r: 2, p9: 0, p10: 1, t: 1 },
    'MEW:45:rh':    { r: 1, p9: 0, p10: 0, t: 1 },
    'MEW:6:base':   { r: 1, p9: 0, p10: 0, w: 1, t: 1 },
    'DRI:34:base':  { r: 3, p9: 1, p10: 0, t: 1 },
    'DRI:34:deck':  { r: 1, p9: 0, p10: 0, t: 1 },
    'SSP:176:rh':   { r: 4, p9: 0, p10: 0, px: { raw: 9.99 }, t: 1 },
    'AHE:1:ball':   { r: 2, p9: 0, p10: 0, t: 1 },
  },
  hist: { DRI: [{ d: '2026-08-17', v: 100, c: 5 }, { d: '2026-08-18', v: 140, c: 9 }] },
  ms: { 'DRI:first': 1 },
  roi: { fee: 30, ship: 2, gem: 55, scope: 'all' },
};

(async () => {
  const b = await chromium.launch();
  const errs = [];

  // ---------- the keys themselves ----------
  let p = await b.newPage();
  p.on('pageerror', e => errs.push(String(e)));
  await p.goto(FILE);
  await p.waitForSelector('#sets .settab');
  const g = await p.evaluate(() => ({
    game: DATA.game, KEY: KEY, SKEY: SKEY,
    rorder: RORDER, rev: [...REV], chase: [...CHASE],
    title: document.title, h1: document.querySelector('.brand h1').textContent,
    sub: document.querySelector('.brand span').textContent,
  }));
  ok('storage key is still exactly cardvault.v2', g.KEY === 'cardvault.v2', g.KEY);
  ok('sync key is still exactly cardvault.sync', g.SKEY === 'cardvault.sync', g.SKEY);
  ok('rarity ladder came from the game profile, complete',
     g.rorder.length === 10 && g.rorder[0] === 'Common' && g.rorder[9] === 'Mega Hyper Rare',
     JSON.stringify(g.rorder));
  ok('reverse-holo slot ids unchanged (8)', g.rev.length === 8 && g.rev.includes('rh') &&
     g.rev.includes('ball') && g.rev.includes('master'), JSON.stringify(g.rev));
  ok('chase rarities unchanged (5)', g.chase.length === 5, JSON.stringify(g.chase));
  ok('title and header still say Pokémon', /Pokémon/.test(g.title) && g.h1 === 'Card Vault' &&
     /Pokémon/.test(g.sub), [g.title, g.h1, g.sub].join(' | '));

  // every rarity present in the data must appear in the ladder, or sorting silently breaks
  const missing = await p.evaluate(() => {
    const set = new Set(RORDER), out = new Set();
    for (const s of DATA.sets) for (const c of s.cards) if (!set.has(c.rarity)) out.add(c.rarity);
    return [...out];
  });
  ok('no rarity in the data is missing from the ladder', missing.length === 0, JSON.stringify(missing));
  await p.close();

  // ---------- an existing collection survives ----------
  p = await b.newPage();
  p.on('pageerror', e => errs.push(String(e)));
  await p.addInitScript(L => localStorage.setItem('cardvault.v2', JSON.stringify(L)), LEGACY);
  await p.goto(FILE);
  await p.waitForSelector('#sets .settab');
  await p.waitForTimeout(400);

  const after = await p.evaluate(() => {
    const s = JSON.parse(localStorage.getItem('cardvault.v2'));
    return { c: s.c, hist: s.hist, ms: s.ms, roi: s.roi, setId: S.setId, theme: S.theme };
  });
  const keys = Object.keys(LEGACY.c);
  ok('every logged slot still present', keys.every(k => after.c[k]), JSON.stringify(Object.keys(after.c)));
  ok('copy counts identical',
     keys.every(k => after.c[k].r === LEGACY.c[k].r && after.c[k].p9 === LEGACY.c[k].p9 &&
                     after.c[k].p10 === LEGACY.c[k].p10));
  ok('wishlist flag survived', after.c['MEW:6:base'].w === 1);
  ok('price override survived', after.c['SSP:176:rh'].px.raw === 9.99);
  ok('value history survived', (after.hist.DRI || []).length >= 2, JSON.stringify(after.hist));
  ok('milestones survived', !!after.ms['DRI:first'], JSON.stringify(after.ms));
  ok('ROI settings survived', after.roi.fee === 30 && after.roi.gem === 55, JSON.stringify(after.roi));
  ok('remembered set and theme survived', after.setId === 'DRI' && after.theme === 'light',
     after.setId + '/' + after.theme);

  // and the collection is actually rendered, not just sitting in storage
  const shown = await p.evaluate(() => {
    document.querySelector('.settab[data-s="MEW"]').click();
    return new Promise(r => setTimeout(() => r(document.querySelector('#hVal').textContent), 400));
  });
  ok('MEW value renders from the restored collection', /^\$[1-9]/.test(shown), shown);
  await p.close();

  console.log('page errors:', errs.length ? errs : 'none');
  await b.close();
  console.log(fails ? `\n${fails} FAILED` : '\nall passed');
  process.exit(fails ? 1 : 0);
})();
