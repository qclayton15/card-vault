/* ==================== state ==================== */
/* Everything game-specific — the name, the storage keys, the rarity ladder, which
   slot ids are a reverse-holo parallel — arrives in DATA.game, built from
   game_pokemon.py. Nothing below this line knows which card game it is running, so a
   second game is a second data file rather than a second copy of the app.
   The storage keys in particular must never change for a build already in use:
   the collection lives under that key and renaming it would orphan every card. */
const G = DATA.game;
const KEY = G.key, OLDKEY = "cardvault.v1";
let S = {
  theme:"dark", view:"binder", setId:DATA.sets[0].id, tile:172, layout:"grid",
  c:{}, hist:{}, roi:{fee:25, ship:1.5, gem:40, scope:"own"}
};
let storageOK = true;
let filt = {q:"", rar:"", own:"all", sort:"num", vari:"all"};
let selIdx = -1, visList = [], openN = null;

const RSLUG = r => r.toLowerCase().replace(/[^a-z]+/g,"-");
const CHASE  = new Set(G.chase);
const RORDER = G.rarities;               // lowest to highest; drives filter order and sort
const REV    = new Set(G.rev);           // parallels that count as part of the set
const $  = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];

function migrate(){
  // v2 kept one flat history array and unprefixed milestone ids — both were single-set
  const first = DATA.sets[0].id;
  if(Array.isArray(S.hist)) S.hist = S.hist.length ? {[first]:S.hist} : {};
  if(!S.hist || typeof S.hist !== "object") S.hist = {};
  if(S.ms){
    const out = {};
    for(const k in S.ms) out[k.includes(":") && /^[A-Z]{2,4}:/.test(k) ? k : first+":"+k] = 1;
    S.ms = out;
  }
  if(!DATA.sets.some(s => s.id === S.setId)) S.setId = first;
}
function loadState(){
  try{
    const raw = localStorage.getItem(KEY);
    if(raw){ Object.assign(S, JSON.parse(raw)); migrate(); return; }
    const old = localStorage.getItem(OLDKEY);
    if(old){                                    // migrate v1 -> v2
      const o = JSON.parse(old), c = {};
      for(const k in o){
        const e = o[k];
        if(!e || (!e.r && !e.p9 && !e.p10 && !e.price)) continue;
        c[k+":base"] = {r:e.r|0, p9:e.p9|0, p10:e.p10|0, px:e.price||undefined};
      }
      S.c = c;
      if(Object.keys(c).length) setTimeout(()=>toast("Imported your previous collection"), 700);
    }
  }catch(e){ storageOK = false; }
}
/* Every slot carries `t`, the moment it last changed, so two devices can be merged
   slot by slot instead of one clobbering the other. A slot emptied on purpose is kept
   as a zeroed tombstone — without it, a deletion here would simply come back from the
   other device on the next sync. Tombstones are dropped after six months.
   Entries with no `t` are either legacy saves or created incidentally by rendering;
   those are pruned as before. */
const TOMB_MS = 180 * 864e5;
let lastSig = {};
function sigOf(e){
  return (e.r|0)+"/"+(e.p9|0)+"/"+(e.p10|0)+"/"+(e.w?1:0)+"/"+(e.px?JSON.stringify(e.px):"");
}
function baseline(){                       // adopt current state as "unchanged"
  lastSig = {};
  for(const k in S.c) lastSig[k] = sigOf(S.c[k]);
}
function stampChanges(){
  const now = Date.now();
  for(const k in S.c){
    const s = sigOf(S.c[k]);
    if(lastSig[k] !== s){ S.c[k].t = now; lastSig[k] = s; }
  }
  for(const k in lastSig) if(!(k in S.c)) delete lastSig[k];
}
function prune(){
  const cut = Date.now() - TOMB_MS;
  for(const k in S.c){
    const e = S.c[k];
    const empty = !e.r && !e.p9 && !e.p10 && !e.w && !e.px;
    if(empty && (!e.t || e.t < cut)) delete S.c[k];
  }
  return S.c;
}
function save(){
  stampChanges();
  prune();
  try{ localStorage.setItem(KEY, JSON.stringify(S)); }catch(e){ storageOK = false; }
}

/* ==================== data helpers ==================== */
/* ---- set order / visibility ----
   Hiding never deletes: the collection stays in S.c and in every backup, so
   restoring a set brings its counts straight back. */
function visibleSets(){
  const hid = new Set(S.hidden || []);
  const ord = (S.order || []).filter(id => DATA.sets.some(s => s.id === id));
  const rest = DATA.sets.map(s => s.id).filter(id => !ord.includes(id));
  return [...ord, ...rest].filter(id => !hid.has(id))
    .map(id => DATA.sets.find(s => s.id === id));
}
const setById = id => DATA.sets.find(s => s.id === id);
const curSet = () => setById(S.setId) || visibleSets()[0] || DATA.sets[0];
const kOf = (sid,n,vid) => sid+":"+n+":"+vid;
function rec(key){ return S.c[key] || (S.c[key] = {r:0,p9:0,p10:0}); }
function peek(key){ return S.c[key]; }
function px(key, v, which){
  const e = peek(key);
  if(e && e.px && e.px[which] != null) return e.px[which];
  return v[which];
}
function copies(key){ const e = peek(key); return e ? (e.r|0)+(e.p9|0)+(e.p10|0) : 0; }
function cardCopies(sid, c){ return c.v.reduce((a,v)=>a+copies(kOf(sid,c.n,v.id)), 0); }
function slotVal(key, v){
  const e = peek(key); if(!e) return 0;
  return (e.r|0)*(px(key,v,"raw")||0) + (e.p9|0)*(px(key,v,"psa9")||0) + (e.p10|0)*(px(key,v,"psa10")||0);
}
function eachSlot(fn){
  const s = curSet();
  for(const c of s.cards) for(const v of c.v) fn(kOf(s.id,c.n,v.id), v, c, s);
}
function totals(){
  const s = curSet();
  let slots=0, owned=0, cps=0, val=0, need=0, base=0, wl=0, wlCost=0, dupes=0;
  eachSlot((k,v,c)=>{
    slots++;
    const q = copies(k);
    if(q>0){ owned++; cps+=q; dupes+=q-1; val+=slotVal(k,v); if(v.id==="base") base++; }
    else need += px(k,v,"raw")||0;
    const e = peek(k);
    if(e && e.w){ wl++; if(!q) wlCost += px(k,v,"raw")||0; }
  });
  return {slots, owned, cps, val, need, base, wl, wlCost, dupes, total:s.total};
}
function totalsAll(){
  let val = 0, cps = 0, owned = 0, slots = 0;
  for(const s of visibleSets()) for(const c of s.cards) for(const v of c.v){
    const k = kOf(s.id,c.n,v.id), q = copies(k);
    slots++;
    if(q){ owned++; cps += q; val += slotVal(k,v); }
  }
  return {val, cps, owned, slots};
}
function money(v){
  if(v==null || isNaN(v)) return "—";
  return "$"+Number(v).toLocaleString("en-US",{minimumFractionDigits:2, maximumFractionDigits:2});
}
function money0(v){
  if(v==null || isNaN(v)) return "—";
  return v>=10000 ? "$"+Math.round(v).toLocaleString("en-US") : money(v);
}
const esc = s => String(s).replace(/[&<>"]/g, m => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));
const today = () => new Date().toISOString().slice(0,10);

/* ==================== theme / chrome ==================== */
function applyTheme(){
  document.documentElement.setAttribute("data-theme", S.theme);
  $("#bTheme").innerHTML = S.theme === "dark" ? "&#9789; Dark" : "&#9788; Light";
  // keep the phone's status bar / address bar in step with the chosen theme
  const tc = S.theme === "dark" ? "#070b14" : "#eef1f7";
  $$('meta[name="theme-color"]').forEach(m => m.remove());
  const m = document.createElement("meta");
  m.name = "theme-color"; m.content = tc;
  document.head.appendChild(m);
  if(S.view === "history") drawHistory();
}
function setView(v){
  S.view = v; save();
  $$(".tab").forEach(t => t.classList.toggle("on", t.dataset.v === v));
  $$(".view").forEach(x => x.classList.toggle("on", x.id === "v-"+v));
  ({binder:drawBinder, bulk:drawBulk, roi:drawROI, wish:drawWish, trade:drawTrade, history:drawHistory}[v]||(()=>{}))();
}
function toast(msg){
  const t = $("#toast"); t.textContent = msg; t.classList.add("on");
  clearTimeout(t._h); t._h = setTimeout(()=>t.classList.remove("on"), 2500);
}

/* ==================== add / manage sets ==================== */
function copyText(txt, okMsg){
  const done = ()=>toast(okMsg || "Copied to clipboard");
  if(navigator.clipboard && navigator.clipboard.writeText)
    return navigator.clipboard.writeText(txt).then(done).catch(fallback);
  fallback();
  function fallback(){
    const ta = document.createElement("textarea");
    ta.value = txt; ta.style.cssText = "position:fixed;top:-1000px";
    document.body.appendChild(ta); ta.select();
    try{ document.execCommand("copy"); done(); }
    catch(e){ toast("Couldn't reach the clipboard — select the text manually"); }
    ta.remove();
  }
}
function moveSet(id, dir){
  const cur = visibleSets().map(s => s.id);
  const i = cur.indexOf(id), j = i + dir;
  if(i < 0 || j < 0 || j >= cur.length) return;
  [cur[i], cur[j]] = [cur[j], cur[i]];
  S.order = [...cur, ...(S.hidden || [])];
  S.metaT = Date.now();
  save(); drawSets(); openSets();
}
function hideSet(id){
  if(visibleSets().length <= 1){ toast("You need at least one set showing"); return; }
  const s = setById(id), t = setStats(s);
  const msg = t.owned
    ? `Hide ${s.name}?\n\nYou have ${t.owned} slot${t.owned===1?"":"s"} logged in it. Nothing is deleted — the counts stay in your backups and come straight back if you restore the set.`
    : `Hide ${s.name}? You can restore it from this panel at any time.`;
  if(!confirm(msg)) return;
  S.hidden = [...new Set([...(S.hidden || []), id])];
  S.metaT = Date.now();
  if(S.setId === id) S.setId = visibleSets()[0].id;
  save(); redraw(); openSets(); toast(s.name + " hidden");
}
function showSet(id){
  S.hidden = (S.hidden || []).filter(x => x !== id);
  S.metaT = Date.now();
  save(); redraw(); openSets(); toast(setById(id).name + " restored");
}
function openSets(){
  const vis = visibleSets(), hid = (S.hidden || []).map(setById).filter(Boolean);
  const row = (s, i) => {
    const t = setStats(s);
    return `<div class="mgrow" style="--sa:${s.accent}">
      <span class="mgmove">
        <button data-mv="${s.id}" data-d="-1" ${i===0?"disabled":""} title="Move left">←</button>
        <button data-mv="${s.id}" data-d="1" ${i===vis.length-1?"disabled":""} title="Move right">→</button>
      </span>
      <span class="mglogo">${logoBox(s, "mglogoimg")}</span>
      <span class="mgtxt"><b>${esc(s.name)}</b>
        <i>${t.cards}/${s.total} cards · ${t.owned}/${t.slots} slots · ${t.pct.toFixed(1)}%</i></span>
      <button class="btn" data-hide="${s.id}">Hide</button>
    </div>`;
  };
  const groups = {};
  (DATA.catalog || []).forEach(c => (groups[c.series] = groups[c.series] || []).push(c));

  $("#setModal").innerHTML = `
    <button class="mclose" id="sx" aria-label="Close">×</button>
    <div class="setbody">
      <h2>Sets</h2>
      <p class="vs">Reorder or hide the sets you track, and see what's ready to be added.</p>

      <div class="lab">Your sets</div>
      ${vis.map(row).join("")}
      ${hid.length ? `<div class="lab" style="margin-top:16px">Hidden</div>` + hid.map(s=>`
        <div class="mgrow dim" style="--sa:${s.accent}">
          <span class="mgmove"></span>
          <span class="mglogo">${logoBox(s, "mglogoimg")}</span>
          <span class="mgtxt"><b>${esc(s.name)}</b><i>counts kept — nothing was deleted</i></span>
          <button class="btn" data-show="${s.id}">Restore</button></div>`).join("") : ""}

      <div class="lab" style="margin-top:20px">Ready to add
        <span class="labn">${(DATA.catalog||[]).length}</span></div>
      <p class="vs" style="margin-bottom:12px">Every expansion with an official gallery on
        ${esc(G.source)}. Pick one and paste the request to me — I'll pull the checklist, every
        variant and Raw / PSA 9 / PSA 10 prices, then send back an updated app with your
        collection carried over untouched.</p>
      ${Object.keys(groups).map(g => `
        <div class="addgroup">
          <div class="addhead">${esc(g)} <span>${groups[g].length}</span></div>
          <div class="addgrid">${groups[g].map(c=>`
            <div class="addcard">
              <img src="${c.logo}" alt="${esc(c.name)}" loading="lazy"
                   onerror="this.style.display='none'">
              <b>${esc(c.name)}</b>
              ${c.note?`<i>${esc(c.note)}</i>`:""}
              <button class="btn" data-req="${esc(c.name)}">Copy request</button>
              ${c.gallery?`<a class="glink" href="${c.gallery}" target="_blank"
                 rel="noopener">official gallery ↗</a>`:""}
            </div>`).join("")}</div></div>`).join("")}

      <div class="lab" style="margin-top:18px">Something else</div>
      <div class="otherrow">
        <input class="f" id="otherSet" placeholder="Any set name — e.g. Twilight Masquerade">
        <button class="btn" id="bOther">Copy request</button>
      </div>

      <div class="whynote">
        <b>Why isn't this automatic?</b>
        This app is a single file running from your own disk, so the browser blocks it from
        reading pricecharting.com, tcgcollector.com and the rest — they don't grant
        cross-origin access. Card images still load because <code>&lt;img&gt;</code> tags are
        exempt, but data isn't. So the research runs on my side, and you get the finished set.
      </div>
    </div>`;

  $("#setov").classList.add("on");
  syncScrollLock();
  $("#sx").onclick = closeSets;
  $$("#setModal [data-mv]").forEach(b => b.onclick = ()=>moveSet(b.dataset.mv, +b.dataset.d));
  $$("#setModal [data-hide]").forEach(b => b.onclick = ()=>hideSet(b.dataset.hide));
  $$("#setModal [data-show]").forEach(b => b.onclick = ()=>showSet(b.dataset.show));
  $$("#setModal [data-req]").forEach(b => b.onclick = ()=>
    copyText(`Add ${b.dataset.req} to Card Vault.`, `Request copied — paste it to me`));
  $("#bOther").onclick = ()=>{
    const v = $("#otherSet").value.trim();
    if(!v){ $("#otherSet").focus(); return; }
    copyText(`Add ${v} to Card Vault.`, "Request copied — paste it to me");
  };
  $("#otherSet").onkeydown = e => { if(e.key === "Enter") $("#bOther").click(); };
}
function closeSets(){ $("#setov").classList.remove("on"); syncScrollLock(); }

/* Freeze the page behind an open overlay so the wheel/finger scrolls the panel,
   not the binder underneath. The offset is parked in body.top and restored on close. */
let lockY = 0;
function syncScrollLock(){
  const want = ["#ov", "#setov", "#syov"].some(s => $(s) && $(s).classList.contains("on"));
  const have = document.body.classList.contains("locked");
  if(want === have) return;
  if(want){
    lockY = window.scrollY || document.documentElement.scrollTop || 0;
    document.body.style.top = (-lockY) + "px";
    document.body.classList.add("locked");
  }else{
    document.body.classList.remove("locked");
    document.body.style.top = "";
    window.scrollTo(0, lockY);
  }
}

/* ==================== stats & set tabs ==================== */
/* ---- set logo with a fallback chain, ending in a drawn crest ----
   The official expansion logos are hotlinked; if a host refuses (or is offline)
   we walk to the next candidate and finally fall back to a crest we draw here,
   so a set never renders as a bare code chip. */
window.lgoFail = function(img){
  let rest = [];
  try{ rest = JSON.parse(img.dataset.alt || "[]"); }catch(e){}
  if(rest.length){ img.dataset.alt = JSON.stringify(rest.slice(1)); img.src = rest[0]; return; }
  const box = img.closest(".logobox");   if(box)  box.classList.add("nologo");
  const host = img.closest(".stmeta,.hkicker"); if(host) host.classList.add("nologo");
  img.remove();
};
function crest(s){
  const g = "cg-"+s.id;
  return `<svg class="crest" viewBox="0 0 40 40" aria-hidden="true">
    <defs><linearGradient id="${g}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${s.accent}"/>
      <stop offset="1" stop-color="${s.accent}" stop-opacity=".42"/></linearGradient></defs>
    <rect x="7" y="3" width="26" height="34" rx="4.5" fill="url(#${g})"/>
    <path d="M7 27 L33 12 L33 20.5 L7 35.5 Z" fill="#fff" opacity=".2"/>
    <circle cx="20" cy="20" r="7.4" fill="none" stroke="#fff" stroke-opacity=".92" stroke-width="2"/>
    <path d="M12.6 20 H27.4" stroke="#fff" stroke-opacity=".92" stroke-width="2"/>
    <circle cx="20" cy="20" r="2.6" fill="#fff"/>
  </svg>`;
}
function logoBox(s, cls){
  const [first, ...rest] = s.logos;
  return `<span class="logobox">
    <img class="${cls}" src="${first}" alt="${esc(s.name)}" data-alt='${JSON.stringify(rest)}'
         referrerpolicy="no-referrer" onerror="lgoFail(this)">
    ${crest(s)}</span>`;
}

function setStats(s){
  let slots = 0, owned = 0, cards = 0;
  for(const c of s.cards){
    let any = 0;
    for(const v of c.v){ slots++; if(copies(kOf(s.id,c.n,v.id))){ owned++; any = 1; } }
    if(any) cards++;
  }
  return {slots, owned, cards, pct: slots ? owned/slots*100 : 0};
}
function drawSets(){
  const el = $("#sets"), R = 15.5, C = 2*Math.PI*R;
  el.innerHTML = visibleSets().map(s=>{
    const t = setStats(s), dash = (t.pct/100)*C;
    return `<button class="settab ${s.id===S.setId?"on":""}" data-s="${s.id}"
      style="--sa:${s.accent}" title="${esc(s.name)} — ${t.pct.toFixed(1)}% of the master set">
      <span class="ring">
        <svg viewBox="0 0 36 36" aria-hidden="true">
          <circle class="rbg" cx="18" cy="18" r="${R}"/>
          <circle class="rfg" cx="18" cy="18" r="${R}"
            stroke-dasharray="${dash.toFixed(2)} ${(C-dash).toFixed(2)}"/>
        </svg>
        <b>${t.pct < 10 ? t.pct.toFixed(1) : Math.round(t.pct)}<em>%</em></b>
      </span>
      <span class="stmeta">
        ${logoBox(s, "stlogo")}
        <span class="stname">${esc(s.name)}</span>
        <i>${t.cards}/${s.total} cards · ${s.released.slice(0,4)}</i>
      </span></button>`;
  }).join("") + `<button class="settab ghost" id="bAddSet">+ add or manage sets</button>`;
  $("#bAddSet").onclick = openSets;
  el.querySelectorAll("[data-s]").forEach(b => b.onclick = ()=>{
    if(b.dataset.s === S.setId) return;
    S.setId = b.dataset.s; selIdx = -1;
    snapshot(false); checkMilestones(true); save(); redraw();
  });
}
/* ---- number tweening ---- */
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
function tween(el, to, fmt){
  if(!el) return;
  const from = +(el.dataset.v || 0);
  el.dataset.v = to;
  if(reduced || Math.abs(to-from) < .005){ el.textContent = fmt(to); return; }
  cancelAnimationFrame(el._raf);
  const t0 = performance.now(), dur = 620;
  const step = now => {
    const p = Math.min(1, (now-t0)/dur), e = 1-Math.pow(1-p, 3);
    el.textContent = fmt(from + (to-from)*e);
    if(p < 1) el._raf = requestAnimationFrame(step);
  };
  el._raf = requestAnimationFrame(step);
}

/* ---- hero panel ---- */
function heroCard(){
  const s = curSet();
  let best = null, bestV = -1, owned = false;
  s.cards.forEach(c => c.v.forEach(v=>{
    const k = kOf(s.id,c.n,v.id), q = copies(k);
    if(!q) return;
    const per = Math.max(px(k,v,"raw")||0, px(k,v,"psa10")||0);
    if(per > bestV){ bestV = per; best = c; owned = true; }
  }));
  if(!best){
    s.cards.forEach(c=>{ const p = px(kOf(s.id,c.n,"base"), c.v[0], "raw")||0;
      if(p > bestV){ bestV = p; best = c; } });
  }
  return {card:best, owned};
}
function drawHero(){
  const s = curSet(), t = totals();
  const pctM = t.slots ? t.owned/t.slots*100 : 0, pctB = t.total ? t.base/t.total*100 : 0;

  $("#hero").style.setProperty("--sa", s.accent);
  $("#hKick").innerHTML = logoBox(s, "klogo") +
    `<span class="kname">${esc(s.name)} <span class="dot"></span> ${esc(s.series)}</span>
     <span class="dot"></span><span>released ${s.released}</span>
     <span class="dot"></span><span>prices ${s.priceDate}</span>`;
  $("#hKick").classList.remove("nologo");
  tween($("#hVal"), t.val, v => money0(v));
  $("#hSub").innerHTML = t.cps
    ? `collection value · <b>${t.cps}</b> ${t.cps===1?"copy":"copies"} across <b>${t.owned}</b> of ${t.slots} slots`
    : `collection value · nothing logged yet — hit <b>+</b> on any card below to start`;

  tween($("#hbmT"), pctM, v => v.toFixed(1)+"%");
  tween($("#hbbT"), pctB, v => v.toFixed(1)+"%");
  requestAnimationFrame(()=>{
    $("#hbm").style.width = pctM.toFixed(2)+"%";
    $("#hbb").style.width = pctB.toFixed(2)+"%";
  });
  $$("#hero .hbar .bt span").forEach((el,i)=>{
    el.textContent = i===0 ? `Master set · ${t.owned}/${t.slots} incl. variants & promos`
                           : `Base set · ${t.base}/${t.total} cards`;
  });

  const all = totalsAll(), nVis = visibleSets().length;
  $("#hPills").innerHTML = `
    <div class="hpill"><b>${t.cps}</b>total copies</div>
    <div class="hpill"><b>${t.dupes}</b>spare${t.dupes===1?"":"s"} to trade</div>
    <div class="hpill"><b>${money0(t.need)}</b>cost to finish</div>
    ${t.wl?`<div class="hpill"><b>${t.wl}</b>on the wishlist</div>`:""}
    ${nVis>1?`<div class="hpill alt"><b>${money0(all.val)}</b>all ${nVis} sets · ${all.cps} ${all.cps===1?"copy":"copies"}</div>`:""}`;

  const {card, owned} = heroCard();
  if(card){
    $("#heroR").innerHTML = `
      <div class="hglow" style="--hgc:var(--rc-${RSLUG(card.rarity)})"></div>
      <div class="hc"><img src="${card.imgLg}" alt="${esc(card.name)}"
        onerror="this.src='${card.img}';this.onerror=null">
        ${CHASE.has(card.rarity)?'<span class="foil"></span>':""}</div>
      <div class="hcap"><b>${esc(card.name)}</b>${owned?"your top card":"the set's chase card"} · #${card.n}</div>`;
  }
  $("#nWish").textContent = t.wl;
  $("#nTrade").textContent = countTrades();
}

/* ---- celebrations ---- */
function confetti(n){
  const cv = $("#confetti"); if(!cv || reduced) return;
  const ctx = cv.getContext("2d");
  cv.width = innerWidth; cv.height = innerHeight; cv.classList.add("on");
  const cols = ["#4d9bff","#a879ff","#ff86bf","#ffc247","#43d17f","#46e2d3"];
  const ps = Array.from({length:n||110}, ()=>({
    x: innerWidth*(.15+Math.random()*.7), y: -20 - Math.random()*innerHeight*.35,
    vx:(Math.random()-.5)*3.6, vy: 1.8+Math.random()*3.8,
    w: 5+Math.random()*7, h: 8+Math.random()*9,
    r: Math.random()*Math.PI, vr:(Math.random()-.5)*.26,
    c: cols[(Math.random()*cols.length)|0]
  }));
  let t = 0;
  const tick = ()=>{
    ctx.clearRect(0,0,cv.width,cv.height);
    let alive = 0;
    for(const p of ps){
      p.vy += .055; p.x += p.vx; p.y += p.vy; p.r += p.vr;
      if(p.y < cv.height + 50) alive++;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r);
      ctx.globalAlpha = Math.max(0, 1 - t/230);
      ctx.fillStyle = p.c; ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h); ctx.restore();
    }
    t++;
    if(alive && t < 250) requestAnimationFrame(tick);
    else { ctx.clearRect(0,0,cv.width,cv.height); cv.classList.remove("on"); }
  };
  requestAnimationFrame(tick);
}
function cheer(title, sub){
  const el = $("#cheer");
  el.innerHTML = `<b>${esc(title)}</b><span>${esc(sub)}</span>`;
  el.classList.add("on");
  clearTimeout(el._h); el._h = setTimeout(()=>el.classList.remove("on"), 4200);
}
function checkMilestones(silent){
  const s = curSet(), t = totals();
  S.ms = S.ms || {};
  const hits = [];
  const fire = (rawId, title, sub, big) => {
    const id = s.id + ":" + rawId;
    if(!S.ms[id]){ S.ms[id] = 1; hits.push({title, sub, big}); }
  };

  if(t.cps >= 1) fire("first", `First ${s.name} card`, "Every collection starts somewhere.", false);
  const chase = s.cards.some(c => CHASE.has(c.rarity) && cardCopies(s.id,c) > 0);
  if(chase) fire("chase", "Chase card secured", "You've pulled something from the top of the set.", true);

  [25,50,75].forEach(p=>{
    if(t.owned/t.slots*100 >= p) fire("m"+p, p+"% of the master set", `${t.owned} of ${t.slots} slots, variants and all.`, true);
  });
  if(t.base === t.total) fire("base100", "Base set complete", `All ${t.total} numbered cards of ${s.name}.`, true);
  if(t.owned === t.slots) fire("m100", "Master set complete", `All ${t.slots} slots. That is the whole thing.`, true);

  const byRar = {};
  s.cards.forEach(c=>{ (byRar[c.rarity] = byRar[c.rarity] || []).push(c); });
  for(const r in byRar){
    const n = byRar[r].length;
    if(n >= 4 && byRar[r].every(c => copies(kOf(s.id,c.n,"base")) > 0))
      fire("r:"+r, `Every ${r}`, `All ${n} ${r} card${n===1?"":"s"} in ${s.name}.`, true);
  }
  const rhSlots = [];
  s.cards.forEach(c => c.v.forEach(v => { if(REV.has(v.id)) rhSlots.push(kOf(s.id,c.n,v.id)); }));
  if(rhSlots.length && rhSlots.every(k => copies(k) > 0))
    fire("rh", "Reverse holo run complete", `All ${rhSlots.length} reverse holos in ${s.name}.`, true);

  if(!hits.length || silent) return;
  const best = hits[hits.length-1];
  cheer(best.title, best.sub);
  confetti(best.big ? 130 : 70);
}
function countTrades(){ let n=0; eachSlot(k=>{ if(copies(k)>1) n++; }); return n; }

/* ==================== binder ==================== */
function visible(){
  const s = curSet();
  let list = s.cards.slice();
  const q = filt.q.trim().toLowerCase();
  if(q) list = list.filter(c => c.name.toLowerCase().includes(q) || String(c.n)===q.replace("#",""));
  if(filt.rar) list = list.filter(c => c.rarity === filt.rar);
  if(filt.own === "owned")   list = list.filter(c => cardCopies(s.id,c) > 0);
  if(filt.own === "missing") list = list.filter(c => cardCopies(s.id,c) === 0);
  if(filt.own === "wish")    list = list.filter(c => c.v.some(v => (peek(kOf(s.id,c.n,v.id))||{}).w));
  const rawOf = c => px(kOf(s.id,c.n,"base"), c.v[0], "raw")||0;
  if(filt.sort === "val")  list.sort((a,b)=>rawOf(b)-rawOf(a));
  if(filt.sort === "name") list.sort((a,b)=>a.name.localeCompare(b.name)||a.n-b.n);
  if(filt.sort === "qty")  list.sort((a,b)=>cardCopies(s.id,b)-cardCopies(s.id,a)||a.n-b.n);
  return list;
}
function drawBinder(){
  const s = curSet();
  visList = visible();
  $("#count").textContent = visList.length + " of " + s.cards.length + " cards";
  $("#grid").style.display = S.layout === "grid" ? "" : "none";
  $("#listWrap").style.display = S.layout === "list" ? "" : "none";
  document.documentElement.style.setProperty("--tile", S.tile+"px");
  if(!visList.length){ $("#gridEmpty").style.display="block"; $("#grid").innerHTML=""; $("#listWrap").style.display="none"; return; }
  $("#gridEmpty").style.display = "none";
  S.layout === "grid" ? renderGrid(s) : renderList(s);
}
function renderGrid(s){
  $("#grid").innerHTML = visList.map((c,i)=>{
    const bk = kOf(s.id,c.n,"base"), q = cardCopies(s.id,c), bq = copies(bk);
    const vOwned = c.v.filter(v => copies(kOf(s.id,c.n,v.id))>0).length;
    const wished = c.v.some(v => (peek(kOf(s.id,c.n,v.id))||{}).w);
    const holo = CHASE.has(c.rarity);
    return `<div class="card ${q?"owned":""} ${holo?"tilt chase":""} ${i===selIdx?"sel":""}"
      data-n="${c.n}" data-i="${i}" style="--gc:var(--rc-${RSLUG(c.rarity)});animation-delay:${Math.min(i,24)*16}ms">
      <div class="thumb ${holo?"holo":""}" data-open="${c.n}">
        <span class="ph">${esc(c.name)}<br>#${c.n}</span>
        <img src="${c.img}" alt="${esc(c.name)}" loading="lazy" data-big="${c.imgLg}"
             onerror="this.style.display='none'" onload="this.parentNode.querySelector('.ph').style.display='none'">
        <span class="num">${c.n}/${s.baseTotal}</span>
        ${q?`<span class="qty">${q}</span>`:""}
        ${c.v.length>1?`<span class="vchip">${vOwned}/${c.v.length} var</span>`:""}
        <button class="star ${wished?"on":""}" data-star="${c.n}" title="Wishlist">${wished?"★":"☆"}</button>
      </div>
      <div class="meta">
        <b title="${esc(c.name)}">${esc(c.name)}</b>
        <span class="rar" style="color:var(--rc-${RSLUG(c.rarity)});background:var(--rb-${RSLUG(c.rarity)});border-color:var(--rc-${RSLUG(c.rarity)})">${c.rarity}</span>
        <div class="px"><span>Raw <b>${money(px(bk,c.v[0],"raw"))}</b></span><span>PSA 10 <b>${money(px(bk,c.v[0],"psa10"))}</b></span></div>
        <div class="steps">
          <button data-dec="${c.n}" ${bq?"":"disabled"} title="Remove a base copy">−</button>
          <button data-inc="${c.n}" title="Add a base copy">+</button>
        </div>
      </div></div>`;
  }).join("");
}
function renderList(s){
  $("#list").innerHTML = visList.map(c=>{
    const bk = kOf(s.id,c.n,"base"), q = cardCopies(s.id,c);
    const val = c.v.reduce((a,v)=>a+slotVal(kOf(s.id,c.n,v.id),v),0);
    return `<tr class="${q?"has":""}" data-n="${c.n}">
      <td class="n mini k-num">${c.n}</td>
      <td class="k-img"><img class="thumbmini" src="${c.img}" alt="" loading="lazy" onerror="this.style.visibility='hidden'"></td>
      <td class="k-name"><a href="#" data-open="${c.n}">${esc(c.name)}</a></td>
      <td class="k-rar"><span class="rar" style="color:var(--rc-${RSLUG(c.rarity)});background:var(--rb-${RSLUG(c.rarity)});border-color:var(--rc-${RSLUG(c.rarity)})">${c.rarity}</span></td>
      <td class="n mini" data-l="variants">${c.v.length}</td>
      <td class="n" data-l="raw">${money(px(bk,c.v[0],"raw"))}</td>
      <td class="n" data-l="PSA 10">${money(px(bk,c.v[0],"psa10"))}</td>
      <td class="n" data-l="copies"><b>${q||"—"}</b></td>
      <td class="n" data-l="value">${val?money(val):"—"}</td>
      <td class="k-act"><div class="steps" style="margin:0;width:78px">
        <button data-dec="${c.n}" ${copies(bk)?"":"disabled"}>−</button><button data-inc="${c.n}">+</button></div></td>
    </tr>`;
  }).join("");
}
function bump(n, d){
  const s = curSet(), k = kOf(s.id,n,"base"), e = rec(k);
  if(d > 0) e.r += d;
  else { if(e.r>0) e.r--; else if(e.p9>0) e.p9--; else if(e.p10>0) e.p10--; }
  commit();
  if(d > 0 && !reduced){
    const el = $(`#grid .card[data-n="${n}"]`);
    if(el){ el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash"); }
  }
}
function toggleWish(n){
  const s = curSet(), c = s.cards.find(x=>x.n===n), k = kOf(s.id,n,"base"), e = rec(k);
  e.w = e.w ? 0 : 1; commit();
}

/* ==================== modal ==================== */
function openCard(n){
  openN = n;
  const s = curSet(), c = s.cards.find(x=>x.n===n);
  const holo = CHASE.has(c.rarity);
  const idx = s.cards.findIndex(x=>x.n===n);
  const wished = c.v.some(v => (peek(kOf(s.id,c.n,v.id))||{}).w);
  const tot = c.v.reduce((a,v)=>a+slotVal(kOf(s.id,n,v.id),v),0);
  const anyEst = c.v.some(v=>v.est);

  const rows = (v)=>{
    const k = kOf(s.id,n,v.id), e = rec(k);
    const one = (lab, which, ck)=>{
      const p = px(k,v,which);
      return `<div class="vrow"><span class="lb">${lab}</span>
        <input class="pin" type="number" step="0.01" min="0" data-k="${k}" data-w="${which}"
               value="${p!=null?Number(p).toFixed(2):""}" placeholder="no data">
        <span class="cnt">
          <button data-k="${k}" data-f="${ck}" data-d="-1">−</button>
          <input type="number" min="0" data-k="${k}" data-q="${ck}" value="${e[ck]|0}">
          <button data-k="${k}" data-f="${ck}" data-d="1">+</button></span></div>`;
    };
    return `<div class="vblock">
      <div class="vhead"><b>${esc(v.label)}</b>
        <span><span class="vv" data-vv="${k}">${money(slotVal(k,v))}</span>
        <a href="${v.pc}" target="_blank" rel="noopener" style="font-size:11px;margin-left:9px">live ↗</a></span></div>
      ${one("Raw / ungraded","raw","r")}${one("PSA 9","psa9","p9")}${one("PSA 10","psa10","p10")}
    </div>`;
  };

  $("#modal").innerHTML = `
    <button class="mclose" id="mx" aria-label="Close">×</button>
    <div class="mimg">
      <span class="mglow" style="--gc:var(--rc-${RSLUG(c.rarity)})"></span>
      <div class="frame ${holo?"holo thumb":""}"><img src="${c.imgLg}" alt="${esc(c.name)}"
        onerror="this.src='${c.img}';this.onerror=null"></div>
      <div class="mnav">
        <button id="mprev" ${idx<=0?"disabled":""}>← prev</button>
        <button id="mwish">${wished?"★ on wishlist":"☆ wishlist"}</button>
        <button id="mnext" ${idx>=s.cards.length-1?"disabled":""}>next →</button>
      </div>
    </div>
    <div class="mbody">
      <h2>${esc(c.name)}</h2>
      <div class="sub">${esc(s.name)} · #${c.n}/${s.baseTotal}
        <span class="rar" style="color:var(--rc-${RSLUG(c.rarity)});background:var(--rb-${RSLUG(c.rarity)});border-color:var(--rc-${RSLUG(c.rarity)})">${c.rarity}</span>
        <span class="vtag">${c.v.length} variant${c.v.length===1?"":"s"}</span></div>
      ${c.v.map(rows).join("")}
      <div class="tot"><span>All variants of this card</span><span class="v" id="mtot">${money(tot)}</span></div>
      ${anyEst?`<div class="warn">One or more prices here are estimated from comparable cards — PriceCharting had no listing when this was built. Type over them if you have better numbers.</div>`:""}
      <div class="mfoot"><button class="btn" id="mzero">Clear this card</button>
        <span style="font-size:11.5px;color:var(--tx3);align-self:center">← → to move between cards · Esc to close</span></div>
    </div>`;
  $("#ov").classList.add("on");
  syncScrollLock();
  $("#mx").onclick = closeCard;
  $("#mprev").onclick = ()=>{ if(idx>0) openCard(s.cards[idx-1].n); };
  $("#mnext").onclick = ()=>{ if(idx<s.cards.length-1) openCard(s.cards[idx+1].n); };
  $("#mwish").onclick = ()=>{ toggleWish(n); openCard(n); };
  $("#mzero").onclick = ()=>{ c.v.forEach(v=>{ const e=rec(kOf(s.id,n,v.id)); e.r=e.p9=e.p10=0; }); commit(); openCard(n); };

  $$("#modal [data-f]").forEach(b => b.onclick = ()=>{
    const e = rec(b.dataset.k), f = b.dataset.f;
    e[f] = Math.max(0, (e[f]|0) + (+b.dataset.d));
    refreshModal(n); commit(false);
  });
  $$("#modal [data-q]").forEach(inp => inp.oninput = ()=>{
    const e = rec(inp.dataset.k);
    e[inp.dataset.q] = Math.max(0, parseInt(inp.value)||0);
    refreshModal(n, inp); commit(false);
  });
  $$("#modal [data-w]").forEach(inp => inp.onchange = ()=>{
    const e = rec(inp.dataset.k), v = parseFloat(inp.value);
    e.px = e.px || {};
    if(inp.value === "" || isNaN(v) || v < 0) delete e.px[inp.dataset.w];
    else e.px[inp.dataset.w] = v;
    if(!Object.keys(e.px).length) delete e.px;
    refreshModal(n); commit(false);
  });
  const fr = $("#modal .frame.holo");
  if(fr) fr.addEventListener("mousemove", ev=>{
    const r = fr.getBoundingClientRect();
    const fx = (ev.clientX-r.left)/r.width*100, fy = (ev.clientY-r.top)/r.height*100;
    fr.style.setProperty("--mx", fx.toFixed(1)+"%");
    fr.style.setProperty("--my", fy.toFixed(1)+"%");
    fr.style.setProperty("--fx", fx.toFixed(0));
  });
}
function refreshModal(n, skip){
  const s = curSet(), c = s.cards.find(x=>x.n===n);
  let tot = 0;
  c.v.forEach(v=>{
    const k = kOf(s.id,n,v.id), e = rec(k), val = slotVal(k,v); tot += val;
    const vv = $(`#modal [data-vv="${CSS.escape(k)}"]`); if(vv) vv.textContent = money(val);
    ["r","p9","p10"].forEach(f=>{
      const inp = $(`#modal [data-k="${CSS.escape(k)}"][data-q="${f}"]`);
      if(inp && inp !== skip) inp.value = e[f]|0;
    });
  });
  $("#mtot").textContent = money(tot);
}
function closeCard(){ $("#ov").classList.remove("on"); openN = null; syncScrollLock(); }

/* ==================== bulk entry ==================== */
function bulkRows(){
  const s = curSet(), out = [];
  const q = $("#bq").value.trim().toLowerCase(), rar = $("#bRar").value, vf = $("#bVar").value, of_ = $("#bOwn").value;
  eachSlot((k,v,c)=>{
    if(q && !c.name.toLowerCase().includes(q) && String(c.n)!==q.replace("#","")) return;
    if(rar && c.rarity !== rar) return;
    const inSet = v.id === "base" || REV.has(v.id);
    if(vf === "set"  && !inSet) return;          // pack pulls only — promos are real, just not in the set
    if(vf === "base" && v.id !== "base") return;
    if(vf === "rh" && !REV.has(v.id)) return;
    if(vf === "promo" && inSet) return;
    const cp = copies(k);
    if(of_ === "own" && !cp) return;
    if(of_ === "miss" && cp) return;
    out.push({k, v, c});
  });
  return out;
}
function drawBulk(){
  const rows = bulkRows();
  const promos = rows.filter(r => r.v.id !== "base" && !REV.has(r.v.id)).length;
  $("#bCount").textContent = rows.length + " slot" + (rows.length===1?"":"s") +
    (promos ? " · " + promos + " promo" + (promos===1?"":"s") : "");
  let prevN = null;
  $("#bulk").innerHTML = rows.map(({k,v,c})=>{
    const e = peek(k) || {r:0,p9:0,p10:0};
    const start = c.n !== prevN; prevN = c.n;           // first row of a card starts a group
    const promo = v.id !== "base" && !REV.has(v.id);
    return `<tr class="${copies(k)?"has ":""}${start?"gs":"cont"}">
      <td class="n mini k-num">${start ? c.n : ""}</td>
      <td class="k-name">${esc(c.name)}</td>
      <td class="k-var"><span class="vtag ${v.id==="base"?"base":promo?"promo":""}">${esc(v.label)}</span></td>
      <td class="mini k-rar">${c.rarity}</td>
      <td class="n k-raw" data-l="market">${money(px(k,v,"raw"))}</td>
      <td class="k-q" data-l="raw"><input class="qin ${e.r?"hot":""}" type="number" inputmode="numeric" min="0" data-k="${k}" data-q="r" value="${e.r||""}" placeholder="0" aria-label="${esc(c.name)} ${esc(v.label)} raw copies"></td>
      <td class="k-q" data-l="PSA 9"><input class="qin ${e.p9?"hot":""}" type="number" inputmode="numeric" min="0" data-k="${k}" data-q="p9" value="${e.p9||""}" placeholder="0" aria-label="${esc(c.name)} ${esc(v.label)} PSA 9 copies"></td>
      <td class="k-q" data-l="PSA 10"><input class="qin ${e.p10?"hot":""}" type="number" inputmode="numeric" min="0" data-k="${k}" data-q="p10" value="${e.p10||""}" placeholder="0" aria-label="${esc(c.name)} ${esc(v.label)} PSA 10 copies"></td>
      <td class="n k-val" data-sv="${k}" data-l="value">${slotVal(k,v)?money(slotVal(k,v)):"—"}</td>
    </tr>`;
  }).join("");
}

/* ==================== grading ROI ==================== */
function drawROI(){
  const s = curSet(), R = S.roi, gem = R.gem/100;
  $("#roiFee").value = R.fee; $("#roiShip").value = R.ship; $("#roiGem").value = R.gem;
  $("#roiGemV").textContent = R.gem + "%";
  $$("#roiScope button").forEach(b => b.classList.toggle("on", b.dataset.v === R.scope));

  const rows = [];
  eachSlot((k,v,c)=>{
    const raw = px(k,v,"raw"), p9 = px(k,v,"psa9"), p10 = px(k,v,"psa10");
    if(raw == null || p9 == null || p10 == null) return;
    const e = peek(k), have = e ? (e.r|0) : 0;
    if(R.scope === "own" && !have) return;
    const ev = gem*p10 + (1-gem)*p9;
    const cost = raw + (+R.fee) + (+R.ship);
    rows.push({c, v, k, raw, p9, p10, ev, cost, profit: ev-cost, roi:(ev-cost)/cost*100, have});
  });
  rows.sort((a,b)=>b.profit-a.profit);
  const shown = rows.slice(0, 80);
  $("#roiCount").textContent = rows.length ? `${rows.length} candidate${rows.length===1?"":"s"}${rows.length>80?" — top 80 shown":""}` : "";

  if(!rows.length){
    $("#roiEmpty").style.display = "block"; $("#roiWrap").style.display = "none";
    $("#roiEmpty").innerHTML = R.scope === "own"
      ? `<b>No raw copies logged yet</b>Add some cards in the Binder or Bulk entry tab, then come back — this ranks the cards you actually hold.<br><br>Or switch to <b style="display:inline">All cards</b> above to scout what's worth buying to grade.`
      : `<b>No cards with full graded data</b>Every candidate needs a raw, PSA 9 and PSA 10 price.`;
    return;
  }
  $("#roiEmpty").style.display = "none"; $("#roiWrap").style.display = "";
  const win = rows.filter(r=>r.profit>0).length;
  $("#roiSum").innerHTML = `<b>${win}</b> of ${rows.length} candidates clear their grading cost at a
    ${R.gem}% gem rate. Expected value assumes a PSA 10 ${R.gem}% of the time and a PSA 9 otherwise —
    it does not account for PSA 8 or below, so treat it as the optimistic case.`;
  $("#roi").innerHTML = shown.map(r=>`
    <tr class="${r.have?"has":""}">
      <td class="n mini k-num">${r.c.n}</td>
      <td class="k-name">${esc(r.c.name)} ${r.v.id!=="base"?`<span class="vtag">${esc(r.v.label)}</span>`:""}</td>
      <td class="n mini" data-l="have">${r.have||"—"}</td>
      <td class="n" data-l="raw">${money(r.raw)}</td>
      <td class="n mini" data-l="PSA 9">${money(r.p9)}</td>
      <td class="n mini" data-l="PSA 10">${money(r.p10)}</td>
      <td class="n" data-l="expected">${money(r.ev)}</td>
      <td class="n" data-l="all-in cost">${money(r.cost)}</td>
      <td class="n ${r.profit>0?"pos":"neg"}" data-l="profit">${r.profit>0?"+":""}${money(r.profit)}</td>
      <td class="n ${r.profit>0?"pos":"neg"}" data-l="ROI">${r.roi>0?"+":""}${r.roi.toFixed(0)}%</td>
    </tr>`).join("");
}

/* ==================== wishlist ==================== */
function drawWish(){
  const s = curSet(), rows = [];
  eachSlot((k,v,c)=>{ const e = peek(k); if(e && e.w) rows.push({k,v,c}); });
  rows.sort((a,b)=>(px(b.k,b.v,"raw")||0)-(px(a.k,a.v,"raw")||0));
  const cost = rows.filter(r=>!copies(r.k)).reduce((a,r)=>a+(px(r.k,r.v,"raw")||0),0);
  $("#wishEmpty").style.display = rows.length ? "none" : "block";
  $("#wishWrap").style.display = rows.length ? "" : "none";
  $("#wishSum").innerHTML = rows.length
    ? `<b>${rows.length}</b> card${rows.length===1?"":"s"} flagged · <b>${money(cost)}</b> to buy the ones you still need at raw market.` : "";
  $("#wish").innerHTML = rows.map(({k,v,c})=>{
    const q = copies(k);
    return `<tr class="${q?"has":""}">
      <td class="n mini k-num">${c.n}</td>
      <td class="k-img"><img class="thumbmini" src="${c.img}" alt="" loading="lazy" onerror="this.style.visibility='hidden'"></td>
      <td class="k-name"><a href="#" data-open="${c.n}">${esc(c.name)}</a> ${v.id!=="base"?`<span class="vtag">${esc(v.label)}</span>`:""}</td>
      <td class="mini k-rar">${c.rarity}</td>
      <td class="n" data-l="raw">${money(px(k,v,"raw"))}</td>
      <td class="n" data-l="PSA 10">${money(px(k,v,"psa10"))}</td>
      <td class="n" data-l="status">${q?`<span class="pos">got ${q}</span>`:"still hunting"}</td>
      <td class="k-act"><button class="btn" data-unwish="${k}">remove</button></td></tr>`;
  }).join("");
}

/* ==================== trade binder ==================== */
function drawTrade(){
  const rows = [];
  eachSlot((k,v,c)=>{
    const q = copies(k);
    if(q > 1) rows.push({k, v, c, spare:q-1, val:(q-1)*(px(k,v,"raw")||0)});
  });
  rows.sort((a,b)=>b.val-a.val);
  const tot = rows.reduce((a,r)=>a+r.val,0), n = rows.reduce((a,r)=>a+r.spare,0);
  $("#tradeEmpty").style.display = rows.length ? "none" : "block";
  $("#tradeWrap").style.display = rows.length ? "" : "none";
  $("#tradeSum").innerHTML = rows.length
    ? `<b>${n}</b> spare card${n===1?"":"s"} across ${rows.length} slot${rows.length===1?"":"s"} · <b>${money(tot)}</b> of trade stock at raw market.` : "";
  $("#trade").innerHTML = rows.map(({k,v,c,spare,val})=>`
    <tr><td class="n mini k-num">${c.n}</td>
      <td class="k-img"><img class="thumbmini" src="${c.img}" alt="" loading="lazy" onerror="this.style.visibility='hidden'"></td>
      <td class="k-name"><a href="#" data-open="${c.n}">${esc(c.name)}</a> ${v.id!=="base"?`<span class="vtag">${esc(v.label)}</span>`:""}</td>
      <td class="mini k-rar">${c.rarity}</td>
      <td class="n" data-l="have">${copies(k)}</td>
      <td class="n" data-l="spare"><b>${spare}</b></td>
      <td class="n" data-l="raw ea.">${money(px(k,v,"raw"))}</td>
      <td class="n" data-l="spare value">${money(val)}</td></tr>`).join("");
  $("#bCopyTrade").style.display = rows.length ? "" : "none";
  $("#bCopyTrade").onclick = ()=>{
    const txt = rows.map(r=>`${r.spare}x ${r.c.name} #${r.c.n}${r.v.id!=="base"?" ("+r.v.label+")":""} — ${money(px(r.k,r.v,"raw"))} ea`).join("\n");
    navigator.clipboard.writeText(`Trade list — ${curSet().name}\n\n${txt}\n\nTotal ${money(tot)} at raw market.`)
      .then(()=>toast("Trade list copied to clipboard")).catch(()=>toast("Couldn't reach the clipboard"));
  };
}

/* ==================== value history ==================== */
function histOf(sid){
  if(!S.hist || Array.isArray(S.hist)) S.hist = {};
  return (S.hist[sid || S.setId] = S.hist[sid || S.setId] || []);
}
// Returns "added" or "updated" so the caller can say which it was — a snapshot is one
// point per calendar day, so clicking the button twice in a day revises today's figure
// rather than drawing a second point. Without a word about it that reads as a dead button.
function snapshot(manual){
  const t = totals(), h = histOf();
  if(!t.cps && !manual) return null;
  const d = today(), last = h[h.length-1];
  let how = "added";
  if(last && last.d === d){ how = "updated"; last.v = t.val; last.c = t.cps; }
  else h.push({d, v:t.val, c:t.cps});
  if(h.length > 400) S.hist[S.setId] = h.slice(-400);
  return how;
}
function snapMsg(how){
  const h = histOf(), p = h[h.length-1];
  return (how === "updated" ? "Today's snapshot updated — " : "Snapshot saved — ") +
    money(p.v) + " · " + p.c + (p.c === 1 ? " copy" : " copies");
}
function drawHistory(){
  const h = histOf();
  $("#histSet").textContent = curSet().name;
  // Show whatever we have. Only the *chart* needs two points; hiding the table too meant
  // taking the first snapshot looked like nothing had happened at all.
  $("#histEmpty").style.display = h.length ? "none" : "block";
  $("#histWrap").style.display  = h.length ? "" : "none";
  $("#chartBox").style.display  = h.length < 2 ? "none" : "";
  const one = $("#histOne");
  one.style.display = h.length === 1 ? "" : "none";
  if(h.length === 1)
    one.innerHTML = `<b>One snapshot so far</b> — ${h[0].d}, ${money(h[0].v)} across ` +
      `${h[0].c} ${h[0].c===1?"copy":"copies"}. A line needs two, so the chart appears ` +
      `tomorrow. Saving again today revises this figure rather than adding a second point.`;
  $("#histTbl").innerHTML = h.slice().reverse().map((p,i,arr)=>{
    const prev = arr[i+1], d = prev ? p.v - prev.v : null;
    return `<tr><td class="k-name">${p.d}</td><td class="n" data-l="value">${money(p.v)}</td>
      <td class="n" data-l="copies">${p.c}</td>
      <td class="n ${d>0?"pos":d<0?"neg":"mini"}" data-l="change">${d==null?"—":(d>0?"+":"")+money(d)}</td></tr>`;
  }).join("");
  if(h.length < 2) return;

  const narrow = innerWidth < 700;
  const W = narrow ? 380 : 860, H = narrow ? 210 : 250;
  const P = narrow ? {t:12, r:12, b:24, l:52} : {t:16, r:18, b:28, l:78};
  const FS = narrow ? 9 : 11, FSL = narrow ? 11 : 12;
  const vs = h.map(p=>p.v);
  const vmax = Math.max(...vs), vmin = Math.min(...vs);
  // nice round ticks
  const span = (vmax - vmin) || vmax || 1;
  const rough = span / 4, mag = Math.pow(10, Math.floor(Math.log10(rough)));
  const step = [1,2,2.5,5,10].find(m => m*mag >= rough) * mag;
  const y0 = Math.max(0, Math.floor(vmin/step)*step - (vmin > step ? step : 0));
  const y1 = Math.ceil(vmax/step)*step + (vmax % step === 0 ? step : 0);
  const X = i => P.l + (h.length===1 ? 0 : i/(h.length-1)) * (W-P.l-P.r);
  const Y = v => P.t + (1 - (v-y0)/(y1-y0||1)) * (H-P.t-P.b);

  const tv = [];
  for(let v = y0; v <= y1 + 1e-9; v += step) tv.push(v);
  const line = h.map((p,i)=>`${i?"L":"M"}${X(i).toFixed(1)},${Y(p.v).toFixed(1)}`).join("");
  const area = `${line}L${X(h.length-1).toFixed(1)},${Y(y0).toFixed(1)}L${X(0).toFixed(1)},${Y(y0).toFixed(1)}Z`;
  const lastP = h[h.length-1], first = h[0];
  const chg = lastP.v - first.v;

  $("#chartTitle").textContent = "Collection value over time";
  $("#chartSub").innerHTML = `${h.length} snapshots since ${first.d} · now <b>${money(lastP.v)}</b>, ` +
    `<span class="${chg>=0?"pos":"neg"}">${chg>=0?"up":"down"} ${money(Math.abs(chg))}</span> since the first`;
  $("#chartSvg").innerHTML = `
    <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Collection value over time">
      <defs><linearGradient id="ag" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="var(--acc)" stop-opacity=".26"/>
        <stop offset="1" stop-color="var(--acc)" stop-opacity="0"/></linearGradient></defs>
      ${tv.map(v=>`<line x1="${P.l}" x2="${W-P.r}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"
          stroke="var(--grid)" stroke-width="1"/>
        <text x="${P.l-8}" y="${(Y(v)+FS*.36).toFixed(1)}" text-anchor="end" font-size="${FS}"
          fill="var(--tx3)" font-variant-numeric="tabular-nums">$${Math.round(v).toLocaleString("en-US")}</text>`).join("")}
      <path d="${area}" fill="url(#ag)"/>
      <path d="${line}" fill="none" stroke="var(--acc)" stroke-width="${narrow?2.4:2}"
            stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="${X(h.length-1).toFixed(1)}" cy="${Y(lastP.v).toFixed(1)}" r="${narrow?4:4.5}"
              fill="var(--acc)" stroke="var(--surface)" stroke-width="2"/>
      <text x="${(W-P.r)}" y="${(Y(lastP.v)-11).toFixed(1)}" text-anchor="end" font-size="${FSL}"
            font-weight="700" fill="var(--tx)">${money0(lastP.v)}</text>
      <text x="${P.l}" y="${H-5}" font-size="${FS}" fill="var(--tx3)">${first.d}</text>
      <text x="${W-P.r}" y="${H-5}" text-anchor="end" font-size="${FS}" fill="var(--tx3)">${lastP.d}</text>
      <line id="cross" x1="0" x2="0" y1="${P.t}" y2="${H-P.b}" stroke="var(--axis)" stroke-width="1" opacity="0"/>
      <circle id="dot" r="4.5" fill="var(--acc)" stroke="var(--surface)" stroke-width="2" opacity="0"/>
      <rect id="hit" x="${P.l}" y="${P.t}" width="${W-P.l-P.r}" height="${H-P.t-P.b}" fill="transparent"/>
    </svg>`;

  const svg = $("#chartSvg svg"), hit = $("#hit"), cross = $("#cross"), dot = $("#dot"), tip = $("#ctip");
  const move = ev=>{
    const r = svg.getBoundingClientRect();
    const cx0 = ev.touches ? ev.touches[0].clientX : ev.clientX;
    const sx = (cx0 - r.left) / r.width * W;
    let i = Math.round((sx - P.l)/((W-P.l-P.r)||1)*(h.length-1));
    i = Math.max(0, Math.min(h.length-1, i));
    const p = h[i], cx = X(i), cy = Y(p.v);
    cross.setAttribute("x1",cx); cross.setAttribute("x2",cx); cross.setAttribute("opacity","1");
    dot.setAttribute("cx",cx); dot.setAttribute("cy",cy); dot.setAttribute("opacity","1");
    tip.innerHTML = `<b>${money(p.v)}</b><i>${p.d} · ${p.c} copies</i>`;
    tip.classList.add("on");
    tip.style.left = Math.min(r.width - 130, Math.max(0, cx/W*r.width - 55)) + "px";
    tip.style.top  = Math.max(0, cy/H*r.height - 8) + "px";
  };
  const hide = ()=>{
    cross.setAttribute("opacity","0"); dot.setAttribute("opacity","0"); tip.classList.remove("on");
  };
  let tHide;
  const touch = ev=>{ ev.preventDefault(); clearTimeout(tHide); move(ev); };
  hit.addEventListener("mousemove", move);
  hit.addEventListener("mouseleave", hide);
  hit.addEventListener("touchstart", touch, {passive:false});
  hit.addEventListener("touchmove",  touch, {passive:false});
  // on touch there's no "leave" — hold the readout a moment, then fade it
  hit.addEventListener("touchend", ()=>{ clearTimeout(tHide); tHide = setTimeout(hide, 2600); });
}

/* ==================== export / import / print ==================== */
function dl(name, text, type){
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([text], {type}));
  a.download = name; a.click(); URL.revokeObjectURL(a.href);
}
function exportJSON(){
  dl("card-vault-backup-"+today()+".json",
     JSON.stringify({app:"cardvault", v:3, saved:new Date().toISOString(),
                     c:prune(), hist:S.hist, roi:S.roi, ms:S.ms}, null, 2),
     "application/json");
  toast("Backup downloaded");
}
function exportCSV(){
  const s = curSet(), q = v => `"${String(v==null?"":v).replace(/"/g,'""')}"`;
  const out = [["Set","Number","Name","Rarity","Variant","Raw qty","PSA 9 qty","PSA 10 qty",
                "Raw price","PSA 9 price","PSA 10 price","Total value","Wishlist","PriceCharting"].join(",")];
  eachSlot((k,v,c)=>{
    const e = peek(k) || {};
    out.push([s.name, c.n, c.name, c.rarity, v.label, e.r|0, e.p9|0, e.p10|0,
      px(k,v,"raw") ?? "", px(k,v,"psa9") ?? "", px(k,v,"psa10") ?? "",
      slotVal(k,v).toFixed(2), e.w?"yes":"", v.pc].map(q).join(","));
  });
  dl("card-vault-"+s.id.toLowerCase()+"-"+today()+".csv", out.join("\n"), "text/csv");
  toast("CSV downloaded");
}
function buildPrint(){
  const s = curSet(), miss = [];
  eachSlot((k,v,c)=>{ if(!copies(k)) miss.push({k,v,c}); });
  const t = totals();
  $("#print").innerHTML = `
    <h1>${esc(s.name)} — cards I still need</h1>
    <div class="pm">${miss.length} of ${t.slots} slots missing · ${money(t.need)} at raw market ·
      printed ${today()} · prices captured ${s.priceDate}</div>
    <table><thead><tr><th style="width:22px"></th><th style="width:38px">#</th><th>Card</th>
      <th>Variant</th><th>Rarity</th><th style="text-align:right">Raw</th><th style="text-align:right">PSA 10</th>
    </tr></thead><tbody>
    ${miss.map(({k,v,c})=>`<tr class="grp"><td><span class="bx"></span></td><td>${c.n}</td>
      <td>${esc(c.name)}</td><td>${v.id==="base"?"":esc(v.label)}</td><td>${c.rarity}</td>
      <td style="text-align:right">${money(px(k,v,"raw"))}</td>
      <td style="text-align:right">${money(px(k,v,"psa10"))}</td></tr>`).join("")}
    </tbody></table>`;
}

/* ==================== commit / redraw ==================== */
function commit(full = true){
  save(); syncSoon(); drawHero(); drawSets(); checkMilestones();
  if(!full) return;
  ({binder:drawBinder, bulk:drawBulk, roi:drawROI, wish:drawWish, trade:drawTrade, history:drawHistory}[S.view]||(()=>{}))();
}
function redraw(){ drawSets(); drawHero(); setView(S.view); drawFoot(); }
function drawFoot(){
  const s = curSet();
  $("#foot").innerHTML =
    `Prices for <b>${esc(s.name)}</b> captured ${s.priceDate} from
     <a href="${s.console}" target="_blank" rel="noopener">PriceCharting</a> (ungraded / grade 9 / PSA 10).
     Checklist from <a href="${s.tcgc}" target="_blank" rel="noopener">TCG Collector</a>,
     images from <a href="${s.limitless}" target="_blank" rel="noopener">Limitless TCG</a>.
     Every price is editable and your edits always win.<br>
     Saves automatically in this browser${storageOK?"":` — <b style="color:var(--gold)">storage looks blocked here; use Export backup</b>`}.
     Shortcuts: <kbd>←</kbd><kbd>→</kbd><kbd>↑</kbd><kbd>↓</kbd> move · <kbd>Enter</kbd> open ·
     <kbd>+</kbd>/<kbd>−</kbd> add or remove · <kbd>w</kbd> wishlist · <kbd>/</kbd> search · <kbd>Esc</kbd> close.`;
}

/* ==================== events ==================== */
function wire(){
  // nav
  $$(".tab").forEach(t => t.onclick = ()=>setView(t.dataset.v));

  // header
  $("#bTheme").onclick = ()=>{ S.theme = S.theme==="dark"?"light":"dark"; save(); applyTheme(); };
  $("#bMenu").onclick = e => { e.stopPropagation(); $("#menu").classList.toggle("open"); };
  document.addEventListener("click", ()=>$("#menu").classList.remove("open"));
  $("#mJSON").onclick = exportJSON;
  $("#mCSV").onclick  = exportCSV;
  $("#mPrint").onclick = ()=>{ buildPrint(); setTimeout(()=>window.print(), 60); };
  $("#mSnap").onclick = ()=>{ const how = snapshot(true); save(); setView("history"); toast(snapMsg(how)); };
  $("#mImport").onclick = ()=>$("#fImport").click();
  $("#mSync").onclick = ()=>{ $("#menu").classList.remove("open"); openSync(); };
  $("#mReset").onclick = ()=>{
    if(confirm("Clear every card count, price edit, wishlist flag and snapshot? Export a backup first if you want to keep it.")){
      S.c = {}; S.hist = []; save(); redraw(); toast("Collection cleared");
    }
  };
  $("#fImport").onchange = ev=>{
    const f = ev.target.files[0]; if(!f) return;
    const rd = new FileReader();
    rd.onload = ()=>{
      try{
        const j = JSON.parse(rd.result);
        if(j.c) S.c = j.c;
        else if(j.store){                                     // v1 backup
          S.c = {};
          for(const k in j.store){ const e = j.store[k];
            if(e && (e.r||e.p9||e.p10||e.price)) S.c[k+":base"] = {r:e.r|0,p9:e.p9|0,p10:e.p10|0,px:e.price||undefined}; }
        } else throw 0;
        if(j.hist) S.hist = j.hist;
        if(j.ms)   S.ms   = j.ms;
        if(j.roi)  S.roi  = Object.assign(S.roi, j.roi);
        migrate(); save(); redraw(); toast("Backup restored");
      }catch(e){ toast("That file didn't look like a Card Vault backup"); }
    };
    rd.readAsText(f); ev.target.value = "";
  };

  // binder toolbar
  $("#q").oninput     = e => { filt.q = e.target.value; selIdx = -1; drawBinder(); };
  $("#fRar").onchange = e => { filt.rar = e.target.value; drawBinder(); };
  $("#fSort").onchange= e => { filt.sort = e.target.value; drawBinder(); };
  $$("#fOwn button").forEach(b => b.onclick = ()=>{
    $$("#fOwn button").forEach(x=>x.classList.remove("on")); b.classList.add("on");
    filt.own = b.dataset.v; selIdx = -1; drawBinder();
  });
  $$("#fLay button").forEach(b => b.onclick = ()=>{
    $$("#fLay button").forEach(x=>x.classList.remove("on")); b.classList.add("on");
    S.layout = b.dataset.v; save(); drawBinder();
  });
  $("#tile").oninput = e => {
    S.tile = +e.target.value; $("#tileV").textContent = S.tile + "px";
    document.documentElement.style.setProperty("--tile", S.tile+"px"); save();
  };

  // binder delegation
  $("#binderBody").addEventListener("click", e=>{
    const s = e.target.closest("[data-star]"); if(s){ e.preventDefault(); e.stopPropagation(); toggleWish(+s.dataset.star); return; }
    const o = e.target.closest("[data-open]"); if(o){ e.preventDefault(); openCard(+o.dataset.open); return; }
    const i = e.target.closest("[data-inc]"); if(i){ bump(+i.dataset.inc, 1); return; }
    const d = e.target.closest("[data-dec]"); if(d){ bump(+d.dataset.dec, -1); return; }
  });
  // tilt + preview
  const prev = $("#prev");
  $("#grid").addEventListener("mousemove", e=>{
    const card = e.target.closest(".card"); if(!card) return;
    if(card.classList.contains("tilt")){
      const r = card.getBoundingClientRect();
      const dx = (e.clientX - r.left)/r.width - .5, dy = (e.clientY - r.top)/r.height - .5;
      card.style.setProperty("--ry", (dx*11).toFixed(2)+"deg");
      card.style.setProperty("--rx", (-dy*11).toFixed(2)+"deg");
    }
    const th = card.querySelector(".thumb");
    const r2 = th.getBoundingClientRect();
    const fx = (e.clientX-r2.left)/r2.width*100, fy = (e.clientY-r2.top)/r2.height*100;
    th.style.setProperty("--mx", fx.toFixed(1)+"%");
    th.style.setProperty("--my", fy.toFixed(1)+"%");
    th.style.setProperty("--fx", fx.toFixed(0));
    const img = card.querySelector("img[data-big]");
    if(img && window.innerWidth > 1100){
      prev.innerHTML = `<img src="${img.dataset.big}" alt="">`;
      prev.classList.add("on");
      const px_ = Math.min(e.clientX + 26, window.innerWidth - 246);
      const py = Math.min(Math.max(10, e.clientY - 160), window.innerHeight - 330);
      prev.style.left = px_+"px"; prev.style.top = py+"px";
    }
  });
  $("#grid").addEventListener("mouseleave", ()=>prev.classList.remove("on"));
  $("#grid").addEventListener("mouseout", e=>{ if(!e.relatedTarget || !e.relatedTarget.closest(".card")) prev.classList.remove("on"); });

  // bulk
  ["bq","bRar","bVar","bOwn"].forEach(id => $("#"+id)[id==="bq"?"oninput":"onchange"] = ()=>drawBulk());
  $("#bulk").addEventListener("input", e=>{
    const inp = e.target.closest("[data-q]"); if(!inp) return;
    const el = rec(inp.dataset.k);
    el[inp.dataset.q] = Math.max(0, parseInt(inp.value)||0);
    inp.classList.toggle("hot", !!el[inp.dataset.q]);
    const tr = inp.closest("tr"); tr.classList.toggle("has", copies(inp.dataset.k)>0);
    const set = curSet();
    const [,nn,vid] = inp.dataset.k.split(":");
    const v = set.cards.find(c=>c.n===+nn).v.find(x=>x.id===vid);
    const cell = tr.querySelector("[data-sv]");
    if(cell){ const sv = slotVal(inp.dataset.k, v); cell.textContent = sv?money(sv):"—"; }
    save(); drawHero(); checkMilestones();
  });

  // roi
  ["roiFee","roiShip"].forEach(id => $("#"+id).oninput = ()=>{
    S.roi.fee = +$("#roiFee").value || 0; S.roi.ship = +$("#roiShip").value || 0; save(); drawROI();
  });
  $("#roiGem").oninput = ()=>{ S.roi.gem = +$("#roiGem").value; save(); drawROI(); };
  $$("#roiScope button").forEach(b => b.onclick = ()=>{ S.roi.scope = b.dataset.v; save(); drawROI(); });

  // wishlist / trade delegation
  $("#v-wish").addEventListener("click", e=>{
    const o = e.target.closest("[data-open]"); if(o){ e.preventDefault(); openCard(+o.dataset.open); return; }
    const u = e.target.closest("[data-unwish]");
    if(u){ const el = rec(u.dataset.unwish); el.w = 0; commit(); }
  });
  $("#v-trade").addEventListener("click", e=>{
    const o = e.target.closest("[data-open]"); if(o){ e.preventDefault(); openCard(+o.dataset.open); }
  });
  $("#bSnapNow").onclick = ()=>{ const how = snapshot(true); save(); drawHistory(); toast(snapMsg(how)); };

  // modal
  $("#ov").onclick = e => { if(e.target.id === "ov") closeCard(); };
  $("#setov").onclick = e => { if(e.target.id === "setov") closeSets(); };
  $("#syov").onclick = e => { if(e.target.id === "syov") closeSync(); };

  // ripple feedback
  document.addEventListener("pointerdown", e=>{
    if(reduced) return;
    const b = e.target.closest(".btn,.tab,.seg button,.steps button,.cnt button,.mnav button,.settab");
    if(!b || b.disabled) return;
    const r = b.getBoundingClientRect(), d = Math.max(r.width, r.height) * 1.1;
    const sp = document.createElement("span");
    sp.className = "rip";
    sp.style.width = sp.style.height = d + "px";
    sp.style.left = (e.clientX - r.left - d/2) + "px";
    sp.style.top  = (e.clientY - r.top  - d/2) + "px";
    b.appendChild(sp);
    setTimeout(()=>sp.remove(), 620);
  });
  let rz;
  addEventListener("resize", ()=>{
    const c = $("#confetti"); if(c){ c.width = innerWidth; c.height = innerHeight; }
    clearTimeout(rz);
    rz = setTimeout(()=>{ if(S.view === "history") drawHistory(); }, 220);
  });

  // keyboard
  document.addEventListener("keydown", e=>{
    if(e.key === "Escape"){ closeCard(); closeSets(); closeSync(); $("#menu").classList.remove("open"); return; }
    const typing = /^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement.tagName);
    if(openN !== null){
      const s = curSet(), i = s.cards.findIndex(x=>x.n===openN);
      if(e.key === "ArrowLeft"  && i>0){ e.preventDefault(); openCard(s.cards[i-1].n); }
      if(e.key === "ArrowRight" && i<s.cards.length-1){ e.preventDefault(); openCard(s.cards[i+1].n); }
      return;
    }
    if(e.key === "/" && !typing){ e.preventDefault(); $("#q").focus(); return; }
    if(typing) return;
    if($("#setov").classList.contains("on") || $("#syov").classList.contains("on")) return;
    if(S.view !== "binder" || S.layout !== "grid" || !visList.length) return;
    const cols = Math.max(1, Math.round($("#grid").clientWidth / (S.tile + 14)));
    let ni = selIdx;
    if(e.key === "ArrowRight") ni = Math.min(visList.length-1, selIdx+1);
    else if(e.key === "ArrowLeft")  ni = Math.max(0, selIdx-1);
    else if(e.key === "ArrowDown")  ni = Math.min(visList.length-1, (selIdx<0?0:selIdx+cols));
    else if(e.key === "ArrowUp")    ni = Math.max(0, selIdx-cols);
    else if(e.key === "Enter" && selIdx>=0){ e.preventDefault(); openCard(visList[selIdx].n); return; }
    else if((e.key === "+" || e.key === "=") && selIdx>=0){ bump(visList[selIdx].n, 1); return; }
    else if((e.key === "-" || e.key === "_") && selIdx>=0){ bump(visList[selIdx].n, -1); return; }
    else if(e.key.toLowerCase() === "w" && selIdx>=0){ toggleWish(visList[selIdx].n); return; }
    else return;
    e.preventDefault();
    if(ni !== selIdx){
      selIdx = ni;
      $$("#grid .card").forEach((el,i)=>el.classList.toggle("sel", i===selIdx));
      const el = $(`#grid .card[data-i="${selIdx}"]`);
      if(el) el.scrollIntoView({block:"nearest"});
    }
  });
}

/* ==================== sync across devices ====================
   The collection is mirrored in a private GitHub gist. Each device holds its own
   token in its own browser — the token is never part of the exported backup and
   never leaves the device except as an Authorization header to api.github.com.

   Syncing is a three-step merge, not an upload: pull the gist, merge it into what
   is here, push the result. Because every slot carries an edit time, two devices
   that were both changed while apart end up with the union of the two, taking the
   newer value slot by slot. Nothing is decided by who happened to sync last. */
const SKEY = G.syncKey;
let SY = {};
try { SY = JSON.parse(localStorage.getItem(SKEY) || "{}"); } catch(e){}
if(!SY.device) SY.device = (navigator.maxTouchPoints > 1 ? "Phone" : "Desktop");
function saveSync(){ try{ localStorage.setItem(SKEY, JSON.stringify(SY)); }catch(e){} }
function syncOn(){ return !!(SY.gist && SY.token); }

function mergeSlots(a, b){
  const out = {};
  for(const k of new Set([...Object.keys(a||{}), ...Object.keys(b||{})])){
    const x = (a||{})[k], y = (b||{})[k];
    out[k] = !x ? y : !y ? x : ((y.t||0) > (x.t||0) ? y : x);
  }
  return out;
}
function mergeHist(a, b){
  const out = {};
  for(const sid of new Set([...Object.keys(a||{}), ...Object.keys(b||{})])){
    const m = {};
    for(const p of ((a||{})[sid] || [])) m[p.d] = p;
    for(const p of ((b||{})[sid] || [])) m[p.d] = p;   // a snapshot for a given day is idempotent
    out[sid] = Object.keys(m).sort().map(d => m[d]).slice(-400);
  }
  return out;
}
function syncPayload(){
  return {v:2, at:Date.now(), by:SY.device, c:S.c, hist:S.hist || {}, ms:S.ms || {},
          meta:{order:S.order || null, hidden:S.hidden || null, t:S.metaT || 0}};
}

const GAPI = "https://api.github.com/gists/";
function ghHeaders(extra){
  return Object.assign({Authorization:"Bearer " + SY.token, Accept:"application/vnd.github+json"}, extra || {});
}
function ghError(status){
  if(status === 401) return "GitHub rejected the token (401). Generate a new one with gist scope.";
  if(status === 403) return "GitHub refused the request (403) — the token may lack gist scope.";
  if(status === 404) return "That gist ID was not found (404). Check it, and that the token can see it.";
  return "GitHub returned an error (" + status + ").";
}
async function gistPull(){
  const r = await fetch(GAPI + encodeURIComponent(SY.gist), {headers: ghHeaders()});
  if(!r.ok) throw new Error(ghError(r.status));
  const j = await r.json();
  const f = j.files && (j.files["cardvault.json"] || Object.values(j.files)[0]);
  if(!f) return null;
  const text = f.truncated && f.raw_url ? await (await fetch(f.raw_url)).text() : f.content;
  if(!text) return null;
  try { return JSON.parse(text); }
  catch(e){ throw new Error("The gist does not contain readable Card Vault data."); }
}
async function gistPush(p){
  const r = await fetch(GAPI + encodeURIComponent(SY.gist), {
    method:"PATCH", headers: ghHeaders({"Content-Type":"application/json"}),
    body: JSON.stringify({files:{"cardvault.json":{content: JSON.stringify(p)}}})});
  if(!r.ok) throw new Error(ghError(r.status));
}

let syncing = false, syncQueued = false, syncTimer = null, syncMsg = "";
function setSyncMsg(m){ syncMsg = m; const el = $("#syState"); if(el) el.textContent = m; }
function syncAgo(){
  if(!SY.last) return "not yet synced";
  const s = Math.round((Date.now() - SY.last)/1000);
  if(s < 60) return "synced just now";
  if(s < 3600) return "synced " + Math.round(s/60) + " min ago";
  if(s < 86400) return "synced " + Math.round(s/3600) + "h ago";
  return "synced " + new Date(SY.last).toISOString().slice(0,10);
}
async function syncNow(quiet){
  if(!syncOn()) return false;
  // a sync already in flight: remember the request rather than dropping it, so pressing
  // "Sync now" while the background one runs still picks up the newest edits
  if(syncing){ syncQueued = true; return false; }
  syncing = true; setSyncMsg("Syncing…");
  try{
    const remote = await gistPull();
    if(remote && remote.c){
      S.c = mergeSlots(S.c, remote.c);
      S.hist = mergeHist(S.hist, remote.hist);
      S.ms = Object.assign({}, S.ms || {}, remote.ms || {});
      const rt = (remote.meta && remote.meta.t) || 0;
      if(remote.meta && rt > (S.metaT || 0)){
        if(remote.meta.order) S.order = remote.meta.order;
        if(remote.meta.hidden) S.hidden = remote.meta.hidden;
        S.metaT = rt;
      }
      baseline();            // merged-in values are not local edits; don't re-stamp them
      save();
    }
    await gistPush(syncPayload());
    SY.last = Date.now(); saveSync();
    setSyncMsg("");
    if($("#syov").classList.contains("on")) openSync();
    redraw();
    if(!quiet) toast("Synced");
    return true;
  }catch(e){
    setSyncMsg(e.message || "Sync failed");
    if(!quiet) toast(e.message || "Sync failed");
    return false;
  }finally{
    syncing = false;
    if(syncQueued){ syncQueued = false; setTimeout(() => syncNow(true), 60); }
  }
}
function syncSoon(){
  if(!syncOn()) return;
  clearTimeout(syncTimer);
  syncTimer = setTimeout(() => syncNow(true), 4000);
}

function openSync(){
  const on = syncOn();
  $("#syModal").innerHTML = `
    <button class="mclose" id="syx" aria-label="Close">×</button>
    <div class="setbody">
      <h2>Sync across devices</h2>
      <p class="vs">Keeps this collection the same on your phone and your computer, using a
        private GitHub gist as the meeting point. Both devices can be edited while apart —
        each card slot remembers when it changed, and the newer edit wins.</p>

      <div class="lab">This device</div>
      <div class="syrow">
        <input id="syDev" class="pin" value="${esc(SY.device || "")}" placeholder="Desktop">
        <span class="vs">A name so you can tell which device saved last.</span>
      </div>

      <div class="lab" style="margin-top:14px">Gist ID</div>
      <div class="syrow">
        <input id="syGist" class="pin wide" value="${esc(SY.gist || "")}" placeholder="e.g. 3f9c1a…" spellcheck="false">
        <span class="vs">The long code at the end of your gist's web address.</span>
      </div>

      <div class="lab" style="margin-top:14px">Access token</div>
      <div class="syrow">
        <input id="syTok" class="pin wide" type="password" value="${SY.token ? "••••••••••••" : ""}"
               placeholder="github_pat_…" spellcheck="false" autocomplete="off">
        <span class="vs">Needs <b>gist</b> scope and nothing else. Stored only in this browser —
          it is not included in exported backups.</span>
      </div>

      <div class="syact">
        <button class="btn pri" id="sySave">${on ? "Update and sync" : "Connect and sync"}</button>
        ${on ? `<button class="btn" id="sySync">Sync now</button>
                <button class="btn" id="syOff" style="color:var(--red)">Disconnect</button>` : ""}
      </div>
      <p class="vs" id="syState">${esc(syncMsg || (on ? syncAgo() + (SY.by ? " · last from " + SY.by : "") : ""))}</p>

      <div class="lab" style="margin-top:18px">Setting it up</div>
      <ol class="syhelp">
        <li>On <b>gist.github.com</b>, create a <b>secret</b> gist with filename
            <code>cardvault.json</code> and <code>{}</code> as the content. Copy the ID from its URL.</li>
        <li>Under GitHub <b>Settings → Developer settings → Personal access tokens →
            Tokens (classic)</b>, generate a token with <b>gist</b> ticked and nothing else.
            Fine-grained tokens cannot reach gists — it has to be a classic one.</li>
        <li>Paste both here, on each device you want kept in step.</li>
      </ol>
      <p class="vs">Your collection still lives in this browser — the gist is a copy used to
        pass changes between devices. Keep taking backups either way.</p>
    </div>`;
  $("#syov").classList.add("on"); syncScrollLock();
  $("#syx").onclick = closeSync;
  $("#sySave").onclick = () => {
    const tok = $("#syTok").value.trim();
    SY.device = $("#syDev").value.trim() || SY.device;
    SY.gist = $("#syGist").value.trim().replace(/^.*\//, "");
    if(tok && !/^•+$/.test(tok)) SY.token = tok;
    saveSync();
    if(!syncOn()){ setSyncMsg("Both a gist ID and a token are needed."); return; }
    syncNow();
  };
  if(on){
    $("#sySync").onclick = () => syncNow();
    $("#syOff").onclick = () => {
      if(!confirm("Disconnect this device from sync?\n\nYour collection stays here and the gist is left untouched — this device just stops sending and receiving changes.")) return;
      delete SY.token; delete SY.gist; saveSync(); setSyncMsg(""); openSync(); toast("Sync disconnected");
    };
  }
}
function closeSync(){ $("#syov").classList.remove("on"); syncScrollLock(); }

/* A web app manifest turns "Add to Home Screen" into a proper standalone launch with
   the right icon and name. It is built at runtime rather than shipped as a second file,
   so the app stays a single self-contained HTML document — and so start_url points at
   wherever this copy happens to live, hosted or local. */
function installManifest(){
  try{
    if(location.protocol === "file:") return;      // meaningless from a local file
    const m = {
      name: G.name, short_name: G.name,
      description: G.tagline,
      start_url: location.href.split("#")[0],
      scope: location.href.replace(/[^/]*$/, ""),
      display: "standalone", orientation: "any",
      background_color: "#070b14", theme_color: "#070b14",
      icons: [
        {src: ICONS.i192, sizes:"192x192", type:"image/png", purpose:"any"},
        {src: ICONS.i512, sizes:"512x512", type:"image/png", purpose:"any"},
        {src: ICONS.mask, sizes:"512x512", type:"image/png", purpose:"maskable"}
      ]
    };
    const l = document.createElement("link");
    l.rel = "manifest";
    l.href = URL.createObjectURL(new Blob([JSON.stringify(m)], {type:"application/manifest+json"}));
    document.head.appendChild(l);
  }catch(e){}
}

/* ==================== boot ==================== */
loadState();
baseline();
applyTheme();
installManifest();
const rars = [...new Set(DATA.sets.flatMap(s=>s.cards.map(c=>c.rarity)))];
rars.sort((a,b)=>RORDER.indexOf(a)-RORDER.indexOf(b));
const rarOpts = '<option value="">All rarities</option>' + rars.map(r=>`<option>${r}</option>`).join("");
$("#fRar").innerHTML = rarOpts; $("#bRar").innerHTML = rarOpts;
$("#tile").value = S.tile; $("#tileV").textContent = S.tile+"px";
$$("#fLay button").forEach(b=>b.classList.toggle("on", b.dataset.v===S.layout));
document.documentElement.style.setProperty("--tile", S.tile+"px");
wire();
snapshot(false);
const freshMs = !S.ms;
if(freshMs) checkMilestones(true);   // seed silently so an imported collection doesn't fire a dozen banners
save();
redraw();

/* pull anything the other device logged while this one was closed, and again whenever
   the tab comes back to the foreground */
if(syncOn()){
  setTimeout(() => syncNow(true), 600);
  document.addEventListener("visibilitychange", () => { if(!document.hidden) syncNow(true); });
}
