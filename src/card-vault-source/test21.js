// Printing labels: the standard slot must name the finish the card was actually
// printed in, and the Battle Deck non-holo reprints must sit in their own slot
// rather than masquerading as the set card.
const { chromium } = require('playwright');

const FILE = 'file:///home/claude/card-vault.html';
let fails = 0;
const ok = (name, cond, extra = '') => {
  console.log((cond ? '  ok   ' : '  FAIL ') + name + (cond ? '' : '  ' + extra));
  if (!cond) fails++;
};

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(FILE);
  await page.waitForSelector('#sets .settab');

  const D = await page.evaluate(() => DATA);

  // ---- 1. every base slot is labelled by rarity, with no exceptions
  const bad = [];
  for (const s of D.sets)
    for (const c of s.cards) {
      const want = ['Common', 'Uncommon'].includes(c.rarity) ? 'Base' : 'Holo';
      if (c.v[0].id !== 'base' || c.v[0].label !== want)
        bad.push(`${s.id} ${c.n} ${c.name} ${c.rarity} -> ${c.v[0].label}`);
    }
  ok('base slot labelled by finish across all 1810 cards', bad.length === 0, bad.slice(0, 5).join(' | '));

  // ---- 2. the cards the user actually reported
  const find = (sid, n) => D.sets.find(s => s.id === sid).cards.find(c => c.n === n);
  const labels = (sid, n) => find(sid, n).v.map(v => v.label);
  // both also carry a Cosmos Holo promo, which is correct and hidden by default —
  // what matters is the pair of pack printings that lead the list
  ok('PFL 3 Vileplume leads with Holo + Reverse Holo',
     labels('PFL', 3).slice(0, 2).join(',') === 'Holo,Reverse Holo', labels('PFL', 3).join(','));
  ok('PFL 1 Oddish leads with Base + Reverse Holo',
     labels('PFL', 1).slice(0, 2).join(',') === 'Base,Reverse Holo', labels('PFL', 1).join(','));

  // ---- 3. deck exclusives: swapped into their own slot, base points at the holo row
  const decks = [];
  for (const s of D.sets)
    for (const c of s.cards)
      if (c.v.some(v => v.id === 'deck')) decks.push([s.id, c]);
  ok('23 deck-exclusive reprints carried as their own slot', decks.length === 23, String(decks.length));
  const swapped = decks.every(([, c]) =>
    c.v[0].label === 'Holo' && /-holo-\d+$/.test(c.v[0].pc) &&
    c.v.find(v => v.id === 'deck').label === 'Deck Exclusive (non-holo)');
  ok('deck cards: base is the holo pack row, reprint is its own slot', swapped);
  const noHoloSlot = D.sets.every(s => s.cards.every(c => !c.v.some(v => v.id === 'holo')));
  ok('no card carries both a base and a separate "holo" slot', noHoloSlot);

  // ---- 4. slot ids and totals are untouched by the relabel
  const slots = D.sets.reduce((a, s) => a + s.cards.reduce((b, c) => b + c.v.length, 0), 0);
  ok('slot count unchanged at 3639', slots === 3639, String(slots));
  const dupe = [];
  for (const s of D.sets)
    for (const c of s.cards) {
      const ids = c.v.map(v => v.id);
      if (new Set(ids).size !== ids.length) dupe.push(`${s.id} ${c.n}`);
    }
  ok('no duplicate slot ids', dupe.length === 0, dupe.join(','));

  // ---- 5. bulk view: deck exclusives hidden under "set only", visible under promos
  await page.click('.tab[data-v="bulk"]');
  await page.waitForSelector('#bulk tr');
  const rowsFor = async (name, filter) => {
    await page.selectOption('#bVar', filter);
    await page.fill('#bq', name);
    await page.waitForTimeout(120);
    return page.$$eval('#bulk tr', trs => trs.map(tr => tr.textContent.replace(/\s+/g, ' ').trim()));
  };
  const setOnly = await rowsFor('Vileplume', 'set');
  ok('bulk "set only" shows Vileplume as Holo + Reverse Holo, no Base row',
     setOnly.some(r => /Holo/.test(r)) && !setOnly.some(r => / Base /.test(r)),
     JSON.stringify(setOnly));
  const ditto = await rowsFor('Ditto', 'set');
  ok('bulk "set only" hides the deck exclusive',
     !ditto.some(r => /Deck Exclusive/.test(r)), JSON.stringify(ditto.slice(0, 3)));
  const dittoAll = await rowsFor('Ditto', 'promo');
  ok('bulk promo filter still surfaces the deck exclusive',
     dittoAll.some(r => /Deck Exclusive/.test(r)), JSON.stringify(dittoAll.slice(0, 3)));

  // ---- 6. logging a copy against the relabelled slot still saves
  await rowsFor('Vileplume', 'set');
  const input = await page.$('#bulk input.qin');
  await input.fill('2');
  await input.dispatchEvent('change');
  await page.waitForTimeout(200);
  const saved = await page.evaluate(() => {
    const s = JSON.parse(localStorage.getItem('cardvault.v2'));
    return Object.entries(s.c).filter(([, e]) => e.r).map(([k, e]) => k + '=' + e.r);
  });
  ok('a copy logged on a Holo slot persists', saved.length === 1 && saved[0].endsWith('=2'),
     JSON.stringify(saved));

  await browser.close();
  console.log(fails ? `\n${fails} FAILED` : '\nall passed');
  process.exit(fails ? 1 : 0);
})();
