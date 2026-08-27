"""The Pokémon build of Card Vault.

Everything in this file is what makes the app *about Pokémon* rather than about
trading cards in general: the storage keys, the naming, the rarity ladder, and
which slot ids count as a reverse-holo parallel. The app code itself knows none
of it — it reads all of this out of DATA.game at runtime.

To add a second game, copy this file, change the values, point it at that game's
data modules, and build. Nothing in app.js, style.css or shell.html should need
to know which game it is running.
"""

# ---------------------------------------------------------------- identity
GAME = {
    "id":      "pokemon",
    "name":    "Card Vault",
    "tagline": "Pokémon TCG collection tracker",
    "title":   "Card Vault — Pokémon Collection Tracker",
    "desc":    "Track your Pokémon TCG collection by set, with raw, PSA 9 and PSA 10 prices.",

    # ------------------------------------------------------------ storage
    # DO NOT CHANGE THESE for a build that is already in use. The collection lives
    # in the browser under this key; renaming it orphans every card the user has
    # logged. A second game MUST use different keys so the two never collide.
    "key":     "cardvault.v2",
    "syncKey": "cardvault.sync",

    # ------------------------------------------------------------ vocabulary
    # Rarity ladder, lowest to highest. Drives the rarity filter order and sorting;
    # anything not listed here sorts to the front, so keep it complete.
    "rarities": ["Common", "Uncommon", "Rare", "Double Rare", "ACE SPEC Rare",
                 "Illustration Rare", "Ultra Rare", "Special Illustration Rare",
                 "Hyper Rare", "Mega Hyper Rare"],

    # The rarities worth calling a set's chase card.
    "chase": ["Illustration Rare", "Ultra Rare", "Special Illustration Rare",
              "Hyper Rare", "Mega Hyper Rare"],

    # Slot ids that are a reverse-holo parallel rather than a promo. Most sets have
    # one pattern; Ascended Heroes has two (Poké Ball and Energy) plus a plain
    # Reverse Holo on Trainers; Prismatic Evolutions stacks plain / Poké Ball /
    # Master Ball; the Mega Evolution base set adds a rare Reverse Play parallel.
    # These count as part of the set in the Bulk-entry filter; everything else is
    # treated as a promo and hidden by default.
    "rev": ["rh", "ball", "energy", "play", "master",
            "horizonsrh", "rhcosmos", "rhplay"],

    # Rarities that never receive a reverse-holo parallel. Used by the build's sanity
    # checks; a game without this rule simply omits the key.
    "norev": ["Double Rare"],

    # Card-image URL template. {code} is the set code, {num} the card number
    # (zero-padded to three), {size} SM or LG. Limitless mirrors the TPCi art.
    "img": "https://limitlesstcg.nyc3.cdn.digitaloceanspaces.com/tpci/"
           "{code}/{code}_{num:03d}_R_EN_{size}.png",

    # Where the "add a set" panel tells the user new sets come from.
    "source": "tcg.pokemon.com",
}

# ---------------------------------------------------------------- data modules
MODULES = ["data_mew", "data_ssp", "data_pre", "data_jtg", "data_dri", "data_mev",
           "data_pfl", "data_ahe", "data_por"]
