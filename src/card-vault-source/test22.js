// Value history: taking the first snapshot must visibly do something. Before this,
// one snapshot rendered the same "not enough history" panel as zero snapshots, so the
// button looked dead even though it had saved.
const { chromium } = require('playwright');
const FILE = 'file:///home/claude/card-vault.html';
let fails = 0;
const ok = (n, c, x = '') => { console.log((c ? '  ok   ' : '  FAIL ') + n + (c ? '' : '  ' + x)); if (!c) fails++; };

const look = p => p.evaluate(() => {
  const vis = s => getComputedStyle(document.querySelector(s)).display !== 'none';
  const s = JSON.parse(localStorage.getItem('cardvault.v2') || '{}');
  return {
    empty: vis('#histEmpty'), wrap: vis('#histWrap'),
    chart: vis('#chartBox'), note: vis('#histOne'),
    noteText: document.querySelector('#histOne').textContent.replace(/\s+/g, ' ').trim(),
    toast: document.querySelector('#toast').textContent,
    rows: document.querySelectorAll('#histTbl tr').length,
    hist: (s.hist || {}).MEW || [],
  };
});

(async () => {
  const b = await chromium.launch();

  // ---------- a fresh vault: nothing owned, no history ----------
  let p = await b.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(FILE);
  await p.waitForSelector('#sets .settab');
  await p.click('.tab[data-v="history"]');
  await p.waitForTimeout(200);
  let v = await look(p);
  ok('empty vault: shows the no-snapshots panel', v.empty && !v.wrap, JSON.stringify(v));

  await p.click('#bSnapNow');
  await p.waitForTimeout(250);
  v = await look(p);
  ok('first click saves a snapshot', v.hist.length === 1, JSON.stringify(v.hist));
  ok('first click shows the table, not the empty panel', !v.empty && v.wrap && v.rows === 1,
     JSON.stringify(v));
  ok('chart stays hidden with one point', !v.chart);
  ok('a note explains why there is no line yet', v.note && /One snapshot so far/.test(v.noteText),
     v.noteText);
  ok('note says a second save revises rather than adds',
     /revises this figure/.test(v.noteText), v.noteText);
  ok('toast names the figure saved', /^Snapshot saved — \$/.test(v.toast), v.toast);

  await p.click('#bSnapNow');
  await p.waitForTimeout(250);
  v = await look(p);
  ok('second click same day revises, does not duplicate', v.hist.length === 1, JSON.stringify(v.hist));
  ok('toast says updated, not saved', /^Today's snapshot updated — /.test(v.toast), v.toast);

  // logging a card and re-saving revises today's figure
  await p.click('.tab[data-v="bulk"]');
  await p.waitForSelector('#bulk input.qin');
  const i = await p.$('#bulk input.qin');
  await i.fill('3'); await i.dispatchEvent('change');
  await p.waitForTimeout(200);
  await p.click('.tab[data-v="history"]');
  await p.click('#bSnapNow');
  await p.waitForTimeout(250);
  v = await look(p);
  ok('revised snapshot picks up the new copies',
     v.hist.length === 1 && v.hist[0].c === 3 && v.hist[0].v > 0, JSON.stringify(v.hist));
  await p.close();

  // ---------- a vault that already has yesterday's point ----------
  p = await b.newPage();
  p.on('pageerror', e => errs.push(String(e)));
  await p.addInitScript(() => {
    const d = new Date(Date.now() - 864e5).toISOString().slice(0, 10);
    localStorage.setItem('cardvault.v2', JSON.stringify({
      c: {}, hist: { MEW: [{ d, v: 120.5, c: 8 }] }, setId: 'MEW', view: 'history',
    }));
  });
  await p.goto(FILE);
  await p.waitForSelector('#sets .settab');
  await p.click('.tab[data-v="history"]');
  await p.click('#bSnapNow');
  await p.waitForTimeout(300);
  v = await look(p);
  ok('a snapshot on a new day appends a second point', v.hist.length === 2, JSON.stringify(v.hist));
  ok('two points: the chart appears and the note goes away', v.chart && !v.note, JSON.stringify(v));
  ok('table lists both days', v.rows === 2, String(v.rows));
  const svg = await p.$$eval('#chartSvg svg path', n => n.length);
  ok('chart actually drew a line', svg > 0, String(svg));
  await p.close();

  console.log('page errors:', errs.length ? errs : 'none');
  await b.close();
  console.log(fails ? `\n${fails} FAILED` : '\nall passed');
  process.exit(fails ? 1 : 0);
})();
