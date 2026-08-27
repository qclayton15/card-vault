// A second game must build from the same app.js / style.css / shell.html, run, and be
// unable to touch the Pokémon collection. /tmp/demo.html is a throwaway three-card
// fixture built with CV_GAME=fixture_game_demo — the point is the isolation, not the data.
const { chromium } = require('playwright');
let fails = 0;
const ok = (n, c, x = '') => { console.log((c ? '  ok   ' : '  FAIL ') + n + (c ? '' : '  ' + x)); if (!c) fails++; };

const POKE = { c: { 'MEW:45:base': { r: 7, p9: 0, p10: 0, t: 1 } }, hist: {}, setId: 'MEW' };

(async () => {
  const b = await chromium.launch();
  const errs = [];
  // one browser context: both apps share an origin under file://, which is the
  // worst case for key collisions and therefore the right thing to test
  const ctx = await b.newContext();
  await ctx.addInitScript(P => {
    if (!localStorage.getItem('cardvault.v2')) localStorage.setItem('cardvault.v2', JSON.stringify(P));
  }, POKE);

  const p = await ctx.newPage();
  p.on('pageerror', e => errs.push('pokemon: ' + e));
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForSelector('#sets .settab');

  const d = await ctx.newPage();
  d.on('pageerror', e => errs.push('demo: ' + e));
  await d.goto('file:///tmp/demo.html');
  await d.waitForSelector('#sets .settab');

  const g = await d.evaluate(() => ({
    KEY, SKEY, rorder: RORDER, rev: [...REV],
    title: document.title, h1: document.querySelector('.brand h1').textContent,
    sub: document.querySelector('.brand span').textContent,
    cards: DATA.sets[0].cards.length,
    labels: DATA.sets[0].cards.map(c => c.v.map(v => v.label).join('+')),
  }));
  ok('second game runs on the unmodified app code', errs.length === 0, JSON.stringify(errs));
  ok('it has its own storage key', g.KEY === 'crewvault.v1', g.KEY);
  ok('it has its own sync key', g.SKEY === 'crewvault.sync', g.SKEY);
  ok('it uses its own rarity ladder', g.rorder.includes('Super Rare') &&
     !g.rorder.includes('Double Rare'), JSON.stringify(g.rorder));
  ok('a game with no reverse-holo concept has an empty REV', g.rev.length === 0);
  ok('it names itself, not Card Vault', g.h1 === 'Crew Vault' && /One Piece/.test(g.sub) &&
     /One Piece/.test(g.title), [g.h1, g.sub].join(' | '));
  ok('non-holo rarity still labels Base, higher ones Holo',
     g.labels[2] === 'Base' && g.labels[1].startsWith('Holo'), JSON.stringify(g.labels));

  // log a card in the demo app, then confirm the Pokémon collection is untouched
  await d.click('.tab[data-v="bulk"]');
  await d.waitForSelector('#bulk input.qin');
  const inp = await d.$('#bulk input.qin');
  await inp.fill('5'); await inp.dispatchEvent('change');
  await d.waitForTimeout(300);

  const both = await d.evaluate(() => ({
    demo: JSON.parse(localStorage.getItem('crewvault.v1') || '{}').c,
    poke: JSON.parse(localStorage.getItem('cardvault.v2') || '{}').c,
  }));
  ok('the demo card saved under the demo key',
     Object.values(both.demo || {}).some(e => e.r === 5), JSON.stringify(both.demo));
  ok('the Pokémon collection is byte-for-byte untouched',
     JSON.stringify(both.poke) === JSON.stringify(POKE.c), JSON.stringify(both.poke));

  await p.reload();
  await p.waitForSelector('#sets .settab');
  const still = await p.evaluate(() => JSON.parse(localStorage.getItem('cardvault.v2')).c);
  ok('and still reads back intact in the Pokémon app',
     still['MEW:45:base'] && still['MEW:45:base'].r === 7, JSON.stringify(still));

  console.log('page errors:', errs.length ? errs : 'none');
  await b.close();
  console.log(fails ? `\n${fails} FAILED` : '\nall passed');
  process.exit(fails ? 1 : 0);
})();
