# Card Vault

A Pokémon TCG collection tracker. One self-contained HTML file — no server, no account,
no install. Open it and it works.

**Live:** https://qclayton15.github.io/card-vault/

This repo exists mainly so the app can be reached from a phone. It is my own collection
tracker rather than a product, but there is nothing personal in here — the collection
itself never leaves the browser.

---

## Running it

Open `index.html`. That is the whole app: HTML, CSS, JavaScript, all nine sets of card
data and the icons are inlined into a single ~1.2 MB file. It works offline and from a
`file://` path, so you can just download it and double-click.

Your collection is saved in the browser's `localStorage`, not inside the file. That has
two consequences worth knowing:

- Opening the app from a **different location** (a new folder, or the hosted copy after
  using a local one) can look like an empty collection, because the browser treats it as
  a separate site. Nothing is lost — use **Data → Import backup…** with a JSON export.
- **Clearing your browser data wipes the collection.** Take an occasional
  **Data → Export backup (.json)**.

## What's in it

Nine sets, 1,810 cards, 3,639 individual printings:

| Set | Cards |
|---|---|
| Scarlet & Violet 151 | 207 |
| Surging Sparks | 252 |
| Prismatic Evolutions | 180 |
| Journey Together | 190 |
| Destined Rivals | 244 |
| Mega Evolution | 188 |
| Phantasmal Flames | 130 |
| Ascended Heroes | 295 |
| Perfect Order | 124 |

Six views:

- **Binder** — grid or list, search, filter by rarity / owned / missing / wishlist, sort
  by number, value, name or copies. Click a card for every printing and price.
- **Bulk entry** — one row per printing, three boxes per row: how many you own raw, in a
  PSA 9 slab, and in a PSA 10 slab. Tab between boxes; it saves as you type.
- **Grading ROI** — which cards are actually worth sending to PSA. Blends the PSA 10 and
  PSA 9 prices by a gem rate you set, then subtracts the raw card and the grading cost.
- **Wishlist** — star anything you're hunting.
- **Trades** — every slot where you hold more than one copy, so you can see your spares.
- **Value history** — a snapshot per set, saved the first time you open it each day.

Plus JSON and CSV export, a printable missing-cards checklist, dark and light themes, and
optional sync across devices through a private GitHub gist (set up from inside the app,
under **Data → Sync across devices…** — the token stays in that browser and is never
written into the gist or an export).

## How printings are labelled

The standard, non-reverse printing of a card is named by the finish it was actually
printed in — **Base** for a plain non-holo card, **Holo** where the pack card is foil.
Every Common and Uncommon is non-holo; every Rare and above is holofoil. That was checked
against pokemontcg.io's printing data for all 1,391 cards in the seven sets TCGplayer
carries, and held without exception.

Reverse Holo is always its own slot. Promos, prize-pack versions, stamped and staff
copies, and non-holo Battle Deck reprints each get their own slot too, but are hidden by
default in Bulk entry — they're real cards, just not pack pulls. Switch the Printing
filter to see them.

## Prices

Raw, PSA 9 and PSA 10 prices come from [PriceCharting](https://www.pricecharting.com/),
captured **2026-08-19**. Card names, numbers and rarities come from
[pokemontcg.io](https://pokemontcg.io/); card images from
[Limitless](https://limitlesstcg.com/).

Prices are baked in at build time, so they go stale. Every card links out to its
PriceCharting page for the current figure, and the whole set can be re-captured and
rebuilt.

## Building

`index.html` is generated, not hand-edited. The pipeline is a set of Python data modules
(one per expansion, holding the checklist, rarities, variant table and a compact price
block) which `build_data.py` turns into `cards.json`, and `build.py` inlines into the
shell along with the CSS, JavaScript and icons. Those sources live outside this repo —
this repo holds the built file only.

## Not affiliated

Unofficial fan project. Not produced by, endorsed by, or associated with The Pokémon
Company, Nintendo, Game Freak, Creatures Inc. or PriceCharting. Pokémon and all card
names and images are the property of their respective owners. Prices are a point-in-time
snapshot from a third party and are not a valuation or financial advice.
