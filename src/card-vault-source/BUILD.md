# Card Vault — build sources

`index.html` in the repo is **generated**. This folder is what generates it. Without
these files the app cannot be rebuilt, prices cannot be refreshed, and a new set cannot
be added — the built HTML is a one-way output.

## Rebuild

```
python3 build_data.py     # data modules -> cards.json
python3 build.py          # cards.json + app.js + style.css + shell.html -> card-vault.html
```

Both read `CV_GAME` (default `game_pokemon`), so a second game is a second profile:

```
CV_GAME=game_onepiece CV_JSON=onepiece.json python3 build_data.py
CV_GAME=game_onepiece CV_JSON=onepiece.json CV_HTML=one-piece-vault.html python3 build.py
```

`build.py` refuses to write a file whose data was built for a different game. That check
exists because a mismatched storage key would silently orphan a whole collection.

## What each file is

| File | Role |
|---|---|
| `shell.html` | page skeleton, with `__CSS__` / `__JS__` / `__DATA__` / `__TITLE__` … placeholders |
| `style.css` | all styling, dark and light |
| `app.js` | the entire app — views, storage, sync, export. Knows no card game. |
| `game_pokemon.py` | **what makes it Pokémon**: storage keys, rarity ladder, reverse-holo slot ids, image URL, naming |
| `data_*.py` | one per expansion: checklist, rarities, variant table, compact price block |
| `build_data.py` | assembles the modules into `cards.json`, with sanity assertions |
| `build.py` | inlines everything into one self-contained HTML file |
| `make_icons.py` | generates the Poké Ball icons into `icons_ball.json` (already generated) |
| `refresh_prices.py` | rewrites a module's price block from a fresh PriceCharting capture |
| `audit_printings.py` | compares our slot layout against pokemontcg.io's printing data |
| `fixture_*.py` | throwaway three-card One Piece fixture used by `test24.js` |
| `test*.js` | Playwright suite — see below |

## Tests

Need `npm install playwright`. **They hardcode `file:///home/claude/card-vault.html`** —
change that path, or run them from a folder at that location.

```
for t in 3 10 14 15 17 18 19 20 21 22 23 24; do node test$t.js; done
```

The two that matter most if you touch the build:

- `test23.js` — the storage key is still `cardvault.v2`, and an existing collection
  (counts, wishlist, price overrides, history, milestones, settings) survives intact.
- `test24.js` — a second game builds on unmodified app code, gets its own storage, and
  cannot touch the Pokémon collection.

`test20.js` covers gist sync against a fake gist; `test21.js` the printing labels;
`test22.js` the value-history tab.

## Not included

`cards.json` and `card-vault.html` are build outputs — regenerate them. `icons.json` is
the older CV-monogram icon set, superseded by `icons_ball.json`.
