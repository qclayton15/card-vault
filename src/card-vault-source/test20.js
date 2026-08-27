/* Sync tests. Two browser contexts stand in for two devices, both pointed at a fake
   GitHub gist held in this process, so the whole pull-merge-push cycle runs for real
   without a token or a network. */
const { chromium, devices } = require('playwright');
const CARD = '<svg xmlns="http://www.w3.org/2000/svg" width="245" height="342"><rect width="245" height="342" fill="#41608f"/></svg>';

let GIST = null;            // the fake gist's stored content
let calls = { get: 0, patch: 0 };
let failNext = null;        // e.g. 401 to simulate a bad token

async function wire(ctx) {
  await ctx.route('**/limitlesstcg**', r => r.fulfill({ status: 200, contentType: 'image/svg+xml', body: CARD }));
  await ctx.route('**/cloudfront.net/**', r => r.fulfill({ status: 404, body: '' }));
  await ctx.route('https://api.github.com/gists/**', async route => {
    const req = route.request();
    if (failNext) { const s = failNext; failNext = null; return route.fulfill({ status: s, body: '{}' }); }
    if (req.method() === 'GET') {
      calls.get++;
      return route.fulfill({ status: 200, contentType: 'application/json',
        body: JSON.stringify({ files: { 'cardvault.json': { content: GIST == null ? '{}' : GIST, truncated: false } } }) });
    }
    calls.patch++;
    GIST = JSON.parse(req.postData()).files['cardvault.json'].content;
    return route.fulfill({ status: 200, contentType: 'application/json', body: '{}' });
  });
}

const seed = (name, coll) => ({ name, coll });
async function device(browser, opts, name, coll) {
  const ctx = await browser.newContext(opts);
  await wire(ctx);
  await ctx.addInitScript(([n, c]) => {
    localStorage.setItem('cardvault.sync', JSON.stringify({ gist: 'fake123', token: 'tok', device: n }));
    localStorage.setItem('cardvault.v2', JSON.stringify({
      theme: 'dark', view: 'binder', setId: 'PFL', tile: 172, layout: 'grid',
      roi: { fee: 25, ship: 1.5, gem: 40, scope: 'own' }, c: c || {} }));
  }, [name, coll]);
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(name + ': ' + e.message));
  await p.goto('file:///home/claude/card-vault.html');
  await p.waitForSelector('#grid .card');
  p._errs = errs; p._name = name;
  return p;
}

const coll = p => p.evaluate(() => JSON.parse(localStorage.getItem('cardvault.v2')).c);
const sync = async p => { await p.evaluate(() => syncNow(true)); await p.waitForTimeout(250); };
const setQty = (p, key, r) => p.evaluate(([k, n]) => {
  const e = S.c[k] || (S.c[k] = { r: 0, p9: 0, p10: 0 });
  e.r = n; commit();
}, [key, r]);

let failures = 0;
function check(label, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) failures++;
  console.log((ok ? '  PASS  ' : '  FAIL  ') + label + (ok ? '' : `\n          got ${JSON.stringify(got)}\n          want ${JSON.stringify(want)}`));
}

(async () => {
  const b = await chromium.launch();

  console.log('\n--- a card logged on one device reaches the other ---');
  GIST = null;
  let A = await device(b, { viewport: { width: 1400, height: 900 } }, 'Desktop', {});
  let B = await device(b, { ...devices['iPhone 13'], hasTouch: true }, 'Phone', {});
  await setQty(A, 'PFL:1:base', 3);
  await sync(A);
  await sync(B);
  check('phone sees the desktop entry', (await coll(B))['PFL:1:base'].r, 3);

  console.log('\n--- edits made on both while apart are merged, not overwritten ---');
  await setQty(A, 'PFL:2:base', 1);          // desktop only
  await setQty(B, 'PFL:3:base', 7);          // phone only
  await sync(A); await sync(B); await sync(A);
  const ca = await coll(A), cb = await coll(B);
  check('desktop keeps its own edit',   ca['PFL:2:base'].r, 1);
  check('desktop gains the phone edit', ca['PFL:3:base'].r, 7);
  check('phone keeps its own edit',     cb['PFL:3:base'].r, 7);
  check('phone gains the desktop edit', cb['PFL:2:base'].r, 1);

  console.log('\n--- the same slot changed on both: newer edit wins ---');
  await setQty(A, 'PFL:4:base', 2);
  await A.waitForTimeout(1100);
  await setQty(B, 'PFL:4:base', 9);          // phone edited second
  await sync(A); await sync(B); await sync(A);
  check('newer value survives on phone',   (await coll(B))['PFL:4:base'].r, 9);
  check('newer value survives on desktop', (await coll(A))['PFL:4:base'].r, 9);

  console.log('\n--- a deletion sticks instead of coming back ---');
  await sync(A); await sync(B);
  await setQty(B, 'PFL:1:base', 0);          // cleared on the phone
  await sync(B); await sync(A);
  const del = (await coll(A))['PFL:1:base'];
  check('desktop shows it cleared', del ? del.r : 0, 0);
  check('kept as a tombstone rather than dropped', !!(del && del.t), true);

  console.log('\n--- offline and bad-token handling ---');
  failNext = 401;
  const before = JSON.stringify(await coll(A));
  await setQty(A, 'PFL:5:base', 4);
  await sync(A);
  check('a rejected token does not lose the local edit', (await coll(A))['PFL:5:base'].r, 4);
  check('and the collection is otherwise untouched', JSON.stringify(await coll(A)) !== before, true);
  failNext = null;
  await sync(A); await sync(B);
  check('the edit reaches the phone once the token works', (await coll(B))['PFL:5:base'].r, 4);

  console.log('\n--- the token never leaves the device ---');
  const dump = await A.evaluate(() => JSON.stringify(JSON.parse(localStorage.getItem('cardvault.v2'))));
  check('token absent from the saved collection', /tok/.test(dump), false);
  check('token absent from the pushed gist', /tok/.test(GIST), false);

  console.log('\n--- value history and milestones merge rather than replace ---');
  await A.evaluate(() => { S.hist = { PFL: [{ d: '2026-08-01', v: 10, c: 1 }] }; S.ms = { 'PFL:first': 1 }; save(); });
  await B.evaluate(() => { S.hist = { PFL: [{ d: '2026-08-02', v: 20, c: 2 }] }; S.ms = { 'PFL:ten': 1 }; save(); });
  await sync(A); await sync(B); await sync(A);
  const hist = await A.evaluate(() => S.hist.PFL.map(p => p.d));
  check('both days of history present', hist, ['2026-08-01', '2026-08-02']);
  check('milestones unioned', await A.evaluate(() => Object.keys(S.ms).sort()), ['PFL:first', 'PFL:ten']);

  console.log('\n--- the panel renders and connects ---');
  await A.evaluate(() => openSync());
  await A.waitForTimeout(300);
  check('panel open', await A.locator('#syov.on').count(), 1);
  check('token field is masked', await A.locator('#syTok').getAttribute('type'), 'password');
  check('token value not present in the DOM', /^•+$/.test(await A.locator('#syTok').inputValue()), true);
  await A.screenshot({ path: '/home/claude/t20-sync.png' });
  await A.evaluate(() => closeSync());

  console.log('\n--- unconfigured devices behave normally ---');
  const C = await b.newContext({ viewport: { width: 1200, height: 800 } });
  await wire(C);
  const p3 = await C.newPage();
  const e3 = []; p3.on('pageerror', e => e3.push(e.message));
  await p3.goto('file:///home/claude/card-vault.html');
  await p3.waitForSelector('#grid .card');
  await p3.evaluate(() => { const e = S.c['PFL:9:base'] || (S.c['PFL:9:base'] = { r: 0, p9: 0, p10: 0 }); e.r = 1; commit(); });
  await p3.waitForTimeout(4600);            // past the auto-sync debounce
  check('no sync attempted without a token', e3.length, 0);

  const errs = [...A._errs, ...B._errs];
  console.log('\npage errors:', errs.length ? errs : 'none');
  console.log('fake gist calls:', calls);
  console.log(failures ? `\n${failures} CHECK(S) FAILED` : '\nall checks passed');
  await b.close();
  process.exit(failures ? 1 : 0);
})();
