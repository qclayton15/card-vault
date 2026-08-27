import json, os, re, importlib

# Which game this build is for. game_pokemon.py holds the identity, storage keys,
# rarity ladder and reverse-holo slot ids; a second game is a second such file.
GAMEMOD = os.environ.get("CV_GAME", "game_pokemon")
_g      = importlib.import_module(GAMEMOD)
GAME, MODULES = _g.GAME, _g.MODULES
OUT     = os.environ.get("CV_JSON", "cards.json")   # relative, so the tree is portable

PC  = "https://www.pricecharting.com/game/%s/"
# Card-image URL template, per game — {code} set code, {num} card number, {size} SM/LG.
IMG = GAME["img"]

# Which finish the standard (non-reverse) printing of a card actually has.
#
# Checked against pokemontcg.io's tcgplayer.prices keys — the authoritative list of
# printings that exist — for all 1,391 cards in the seven sets TCGplayer carries
# (Ascended Heroes and Perfect Order are too new to be listed there). The rule below
# matched every single one of them, 1,391/1,391, with no exceptions:
#
#     Common and Uncommon are printed non-holo; every higher rarity is holofoil.
#
# So a card like Vileplume PFL 3 exists as Holo + Reverse Holo and has no plain
# printing at all — calling its standard slot "Base" was simply wrong.
NONHOLO = {"Common", "Uncommon"}

# A handful of Rares were also reprinted NON-holo as a preconstructed Battle Deck
# exclusive. PriceCharting files that reprint as the plain row and the pack card as
# the "Holo" row, which is backwards from our point of view: it put the deck card in
# the base slot and the real set card in a variant. Confirmed on the listings —
# e.g. 151 #45 reads "Iron Leaves ex Battle Deck Exclusive / Non-Holo", and the eBay
# sales under 151 #132 and Phantasmal Flames #68 are titled "NON-HOLO … DECK
# EXCLUSIVE". build() swaps them back below.
DECK = ("deck", "Deck Exclusive (non-holo)")

def slug(name):
    # PriceCharting percent-encodes the apostrophe in names like "N's Darumaka"
    # (n%27s-darumaka) rather than dropping it, so park it out of the way while
    # everything else collapses to hyphens, then put it back.
    s = (name.lower()
           .replace("é","e").replace("è","e").replace("á","a").replace("í","i")
           .replace("'", "\x00").replace(".", ""))
    return re.sub(r"[^a-z0-9\x00]+", "-", s).strip("-").replace("\x00", "%27")

def build(mod):
    m = importlib.import_module(mod)
    S, code, pc = m.SET, m.SET["code"], PC % m.SET["pcslug"]
    # A set may override the URL stem for a card whose PriceCharting listing is
    # spelled differently from the card itself. Key it by number to override every
    # slot on that card, or by (number, slot id) for one printing (see data_jtg).
    over = getattr(m, "PCSLUG", {})
    # PCPATH replaces the whole URL tail for one printing, for the cases where
    # PriceCharting files a promo under a different card number entirely.
    path = getattr(m, "PCPATH", {})
    cards = []
    for num, name, rarity, raw, p9, p10, est in m.BASE:
        sl = lambda vid: over.get((num, vid)) or over.get(num) or slug(name)
        url = lambda vid, tail: pc + (path.get((num, vid)) or tail)
        holo = rarity not in NONHOLO
        extra = list(m.SPECIAL.get(num, []))

        # base slot points at PriceCharting's plain row unless we swap below
        btail = "%s-%d" % (sl("base"), num)
        hv = next((v for v in extra if v[0] == "holo"), None)
        if hv and holo:
            # the "Holo" row is the pack card; the plain row is the deck reprint
            extra[extra.index(hv)] = DECK + ("", raw, p9, p10)
            raw, p9, p10 = hv[3], hv[4], hv[5]
            btail = "%s-holo-%d" % (sl("holo"), num)
        elif hv:
            raise ValueError("%s %d: holo row on a %s" % (mod, num, rarity))

        vs = [{"id":"base","label":"Holo" if holo else "Base","raw":raw,"psa9":p9,
               "psa10":p10,"est":est,"pc":url("base", btail)}]
        if num in m.RH:
            r, a, b = m.RH[num]
            vs.append({"id":"rh","label":"Reverse Holo","raw":r,"psa9":a,"psa10":b,
                       "est":1 if num in m.RH_EST else 0,
                       "pc":url("rh", "%s-reverse-holo-%d" % (sl("rh"), num))})
        for vid, lab, suf, r, a, b in extra:
            tail = ("%s-%d" % (sl("base"), num) if vid == "deck"
                    else "%s-%s-%d" % (sl(vid), suf, num))
            vs.append({"id":vid,"label":lab,"raw":r,"psa9":a,"psa10":b,"est":0,
                       "pc":url(vid, tail)})
        cards.append({"n":num, "name":name, "rarity":rarity,
                      "img":   IMG.format(code=code, num=num, size="SM"),
                      "imgLg": IMG.format(code=code, num=num, size="LG"),
                      "v": vs})

    # sanity
    assert len(cards) == S["total"], (mod, len(cards), S["total"])
    assert [c["n"] for c in cards] == list(range(1, S["total"]+1)), mod
    # rarities that never receive a reverse-holo parallel — a game-level rule, not a
    # universal one, so it lives in the game profile alongside the rarity ladder
    dr = {c["n"] for c in cards if c["rarity"] in set(GAME.get("norev", []))}
    # slots that are a reverse-holo printing — one source of truth, in the game profile
    REV = set(GAME["rev"])

    # Sets with a single reverse pattern use RH and must cover every non-ex base card.
    # Sets with several patterns (Ascended Heroes: Ball + Energy) express them through
    # SPECIAL instead, so RH is empty there and the count check doesn't apply.
    if m.RH:
        assert not (set(m.RH) & dr), (mod, "double rares must not have reverse holos")
        assert all(1 <= n <= S["baseTotal"] for n in m.RH), (mod, "reverse holo outside base set")
        expected_rh = S["baseTotal"] - len(dr)
        assert len(m.RH) == expected_rh, (mod, len(m.RH), expected_rh)

    # Whichever route a set takes, these must always hold.
    for n, vs in m.SPECIAL.items():
        assert 1 <= n <= S["total"], (mod, "variant on a card outside the set", n)
        assert len({v[0] for v in vs}) == len(vs), (mod, "duplicate variant id on card", n)
        rev = {v[0] for v in vs} & REV
        assert not (rev and n in dr), (mod, "double rare given a reverse holo", n)
        assert not (rev and n > S["baseTotal"]), (mod, "secret given a reverse holo", n)
    for c in cards:
        assert c["v"][0]["raw"] is not None, (mod, "base card with no raw price", c["n"])
        assert len({v["id"] for v in c["v"]}) == len(c["v"]), (mod, "duplicate slot", c["n"])

    return {
        "id":S["id"], "name":S["name"], "series":S["series"], "released":S["released"],
        "total":S["total"], "baseTotal":S["baseTotal"],
        "logos": S["logos"],
        "priceDate":S["priceDate"],
        "accent":S["accent"],
        "console":"https://www.pricecharting.com/console/%s" % S["pcslug"],
        "tcgc":S["tcgc"],
        "limitless":"https://limitlesstcg.com/cards/%s" % code,
        "cards":cards,
    }

# Every expansion with an official gallery on tcg.pokemon.com/en-us/all-galleries/,
# newest first. Logo codes and slugs read straight from that page — see
# claude/card-vault-set-logos.md. Sets already built into the app are filtered out below.
CDN = "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/%s.png"
GALLERY = "https://tcg.pokemon.com/en-us/galleries/%s/"
CATALOG = [
    # name,                    series,             code,      slug,                   note
    ("Pitch Black",            "Mega Evolution",   "me05",    "pitch-black",           "newest set"),
    ("Chaos Rising",           "Mega Evolution",   "me04",    "chaos-rising",          ""),
    ("Perfect Order",          "Mega Evolution",   "me03",    "perfect-order",         ""),
    ("Ascended Heroes",        "Mega Evolution",   "me02pt5", "ascended-heroes",       "special set"),
    ("Phantasmal Flames",      "Mega Evolution",   "me02",    "phantasmal-flames",     ""),
    ("Mega Evolution",         "Mega Evolution",   "me01",    "mega-evolution",        "started the era"),
    ("Black Bolt & White Flare","Scarlet & Violet","sv10pt5", "black-white",           "two sets in one"),
    ("Destined Rivals",        "Scarlet & Violet", "sv10",    "destined-rivals",       ""),
    ("Journey Together",       "Scarlet & Violet", "sv09",    "journey-together",      ""),
    ("Prismatic Evolutions",   "Scarlet & Violet", "sv08pt5", "prismatic-evolutions",  "Eevee special set"),
    ("Surging Sparks",         "Scarlet & Violet", "sv08",    "surging-sparks",        "Pikachu ex chase"),
    ("Stellar Crown",          "Scarlet & Violet", "sv07",    "stellar-crown",         ""),
    ("Shrouded Fable",         "Scarlet & Violet", "sv06pt5", "shrouded-fable",        "special set"),
    ("Twilight Masquerade",    "Scarlet & Violet", "sv06",    "twilight-masquerade",   ""),
    ("Temporal Forces",        "Scarlet & Violet", "sv05",    "temporal-forces",       ""),
    ("Paldean Fates",          "Scarlet & Violet", "sv04pt5", "paldean-fates",         "special set"),
    ("Paradox Rift",           "Scarlet & Violet", "sv04",    "paradox-rift",          ""),
    ("Scarlet & Violet 151",   "Scarlet & Violet", "sv03pt5", "151",                   "the original 151"),
    ("Obsidian Flames",        "Scarlet & Violet", "sv03",    "obsidian-flames",       ""),
    ("Paldea Evolved",         "Scarlet & Violet", "sv02",    "paldea-evolved",        ""),
    ("Scarlet & Violet",       "Scarlet & Violet", "sv01",    "scarlet-violet",        "era base set"),
]

sets = [build(m) for m in MODULES]
have = {s["name"] for s in sets}
catalog = [{"name":n, "series":se, "logo":CDN % c, "gallery":GALLERY % sl, "note":no}
           for n, se, c, sl, no in CATALOG if n not in have]

json.dump({"game":GAME, "sets":sets, "catalog":catalog}, open(OUT, "w"),
          separators=(",",":"))

for s in sets:
    slots = sum(len(c["v"]) for c in s["cards"])
    rar = {}
    for c in s["cards"]: rar[c["rarity"]] = rar.get(c["rarity"],0)+1
    print("%-16s %3d cards  %3d slots   %s" % (s["name"], len(s["cards"]), slots,
          ", ".join("%s:%d" % (k,v) for k,v in sorted(rar.items()))))
print("total slots:", sum(sum(len(c["v"]) for c in s["cards"]) for s in sets))
