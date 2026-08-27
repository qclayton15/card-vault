# Scarlet & Violet — Journey Together (SV09 / JTG), released 2025-03-28
# 190 cards (159 base + 31 secret). One standard Reverse Holo pattern covering
# every non-ex base card (143 of them), so RH carries the reverses and SPECIAL
# holds the promos and oddities.
#
# Rarities: api.pokemontcg.io/v2/cards?q=set.id:sv9
# Prices:   pricecharting.com/console/pokemon-journey-together  (captured 2026-08-19)
import re

# one line per card, in number order:  name|rarity code
CHECKLIST = """
Caterpie|C
Metapod|C
Butterfree|R
Paras|C
Parasect|C
Petilil|C
Lilligant|C
Maractus|U
Karrablast|C
Foongus|C
Amoonguss ex|D
Shelmet|C
Accelgor|U
Durant|C
Virizion|U
Sprigatito|C
Floragato|C
Meowscarada|R
Nymble|C
Magmar|C
Magmortar|R
Torchic|C
Combusken|U
Blaziken ex|D
Torkoal|C
N's Darumaka|C
N's Darmanitan|U
Larvesta|C
Volcarona|U
Reshiram ex|D
Volcanion ex|D
Articuno|U
Remoraid|C
Octillery|U
Lotad|C
Lombre|C
Ludicolo|R
Wingull|C
Pelipper|U
Wailmer|C
Wailord|R
Regice|U
Veluza ex|D
Alolan Geodude|C
Alolan Graveler|C
Alolan Golem|U
Iono's Voltorb|C
Iono's Electrode|U
N's Joltik|C
Togedemaru|C
Tapu Koko ex|D
Iono's Tadbulb|C
Iono's Bellibolt ex|D
Iono's Wattrel|C
Iono's Kilowattrel|R
Lillie's Clefairy ex|D
Alolan Marowak|U
Mr. Mime|C
Shuppet|C
Banette|U
Beldum|C
Metang|C
Metagross|R
N's Sigilyph|C
Oricorio|C
Lillie's Cutiefly|C
Lillie's Ribombee|R
Lillie's Comfey|C
Mimikyu ex|D
Dhelmise|C
Impidimp|C
Morgrem|C
Grimmsnarl|U
Milcery|C
Alcremie ex|D
Cubone|C
Swinub|C
Piloswine|C
Mamoswine ex|D
Larvitar|C
Pupitar|C
Regirock|R
Pancham|C
Rockruff|C
Lycanroc|R
Hop's Silicobra|C
Hop's Sandaconda|U
Toedscool|C
Toedscruel|U
Klawf|U
Koffing|C
Weezing|U
Paldean Wooper|C
Paldean Clodsire ex|D
Tyranitar|R
N's Purrloin|C
N's Zorua|C
N's Zoroark ex|D
Pangoro|U
Lokix|U
Bombirdier|C
Escavalier|U
N's Klink|C
N's Klang|C
N's Klinklang|U
Galarian Stunfisk|C
Magearna|R
Hop's Corviknight|U
Cufant|C
Copperajah|U
Hop's Zacian ex|D
Bagon|C
Shelgon|C
Salamence ex|D
Druddigon|C
N's Reshiram|R
Hop's Snorlax|R
Sentret|C
Furret|C
Dunsparce|C
Dudunsparce ex|D
Kecleon|C
Tropius|C
Audino|C
Minccino|C
Cinccino|U
Noibat|C
Noivern|R
Komala|C
Drampa|C
Skwovet|C
Greedent|U
Hop's Rookidee|C
Hop's Corvisquire|C
Hop's Wooloo|C
Hop's Dubwool|R
Cramorant|C
Hop's Cramorant|U
Lechonk|C
Oinkologne|U
Squawkabilly|C
Billy & O'Nare|C
Black Belt's Training|C
Black Belt's Training|C
Black Belt's Training|C
Brock's Scouting|U
Hop's Bag|U
Hop's Choice Band|U
Iris's Fighting Spirit|U
Levincia|U
Lillie's Pearl|U
N's Castle|U
N's PP Up|U
Postwick|U
Professor's Research (Professor Sada)|C
Redeemable Ticket|U
Ruffian|U
Super Potion|U
Spiky Energy|U
Maractus|I
Articuno|I
Wailord|I
Iono's Kilowattrel|I
Lillie's Ribombee|I
Swinub|I
Lycanroc|I
N's Reshiram|I
Furret|I
Noibat|I
Hop's Wooloo|I
Volcanion ex|T
Iono's Bellibolt ex|T
Lillie's Clefairy ex|T
Mamoswine ex|T
N's Zoroark ex|T
Hop's Zacian ex|T
Salamence ex|T
Dudunsparce ex|T
Brock's Scouting|T
Iris's Fighting Spirit|T
Ruffian|T
Volcanion ex|S
Iono's Bellibolt ex|S
Lillie's Clefairy ex|S
N's Zoroark ex|S
Hop's Zacian ex|S
Salamence ex|S
Iono's Bellibolt ex|H
N's Zoroark ex|H
Spiky Energy|H
"""

# <number><variant char><raw>,<psa9>,<psa10>   blank = no sale on record
PRICES = """
1b.20,10.34,18.73 1R1.10,10.59,31.72 2b.59,10.34,30.99 2R1.10,12.07,35.99 3b1.17,5.00,99.99
3R.99,11.59,34.61 4b.14,10.27,30.78 4R.40,10.94,32.72 5b.26,10.49,31.42 5R.40,10.74,32.16
6b.09,10.10,30.30 6R.40,10.59,31.72 7b.47,10.48,31.38 7R.55,11.10,33.19 8b.20,8.51,30.65
8R.27,10.42,31.21 9b.40,10.59,59.99 9R.38,10.74,32.16 10b.09,10.12,30.35 10R.38,10.74,32.16
11b.66,15.38,56.90 12b.05,10.04,30.13 12R.30,10.51,31.47 13b.12,10.21,30.60 13R.25,10.37,31.08
14b.25,10.25,30.73 14R.22,10.45,31.29 15b.34,10.49,31.42 15R.65,10.59,31.73 16b.60,10.46,31.34
16R.76,13.99,22.79 17b.33,10.45,31.29 17R.60,7.50,33.66 18b1.09,10.00,34.27 18C10.41,,
18R.99,11.80,35.22 19b.05,10.12,30.35 19R.40,10.59,31.73 20b.25,10.09,16.25 20R.33,13.00,25.00
21b.28,9.51,46.99 21R.50,10.98,32.84 22b.32,40.00,59.99 22R1.50,12.17,36.30 23b.24,10.21,30.60
23R.40,10.74,32.16 24b1.99,12.76,45.00 24J4.36,12.97,120.00 25b.25,10.27,30.78 25R.30,10.59,31.73
26b.20,10.39,31.12 26R.65,11.22,33.54 27b.50,10.58,59.99 27P.28,, 27R.89,11.41,34.10
28b.20,10.19,54.99 28R.50,10.59,31.73 29b.10,10.15,30.43 29R.40,10.49,31.42 30S.99,25.00,51.54
30b1.05,11.43,46.00 30J1.64,12.56,162.50 31b1.48,12.99,40.00 32b.99,8.50,67.69 32D.99,11.87,155.48
32R.90,13.40,33.32 33b.26,10.52,31.51 33R.40,10.68,31.98 34b.17,10.37,31.08 34R.40,10.59,31.73
35b.32,10.30,30.86 35R.81,5.00,31.72 36b.19,10.22,30.65 36R.40,10.91,32.63 37b.58,13.93,33.15
37R1.00,11.32,33.84 38b.20,10.19,30.56 38R.35,10.74,30.00 39b.08,10.16,30.47 39R.26,10.50,31.47
40b.20,10.31,30.91 40R.61,10.00,35.00 41b.92,28.00,152.50 41C1.77,32.25,338.33 41R.73,11.08,41.00
42b.35,10.59,31.73 42R.51,10.65,31.90 43b1.35,13.00,38.99 44b.21,10.36,31.04 44R.40,10.79,31.72
45b.33,10.40,31.16 45R.40,7.50,31.72 46b.38,14.95,31.64 46R.74,15.00,34.27 47b.49,10.48,31.38
47A.45,, 47R.89,14.20,40.54 48b.49,10.45,31.29 48R.79,11.47,34.27 49b.25,10.28,30.82
49R.37,10.74,32.16 50b.19,10.27,30.78 50R.25,10.46,31.34 51b1.23,11.50,31.00 52b.21,12.02,42.89
52C.38,, 52R.46,10.68,31.98 53P1.21,, 53b1.32,17.66,35.25 54b.25,10.53,31.55 54R.66,10.59,56.00
55b.39,21.94,31.00 55H.42,16.00,31.72 55P.13,, 55R.86,11.31,33.79 56V4.33,, 56b2.03,9.22,43.61
57b.40,10.37,31.08 57R.99,22.48,32.16 58b.51,10.43,31.25 58R.43,5.50,31.72 59b.24,10.36,31.04
59R.63,10.51,31.47 60b.36,16.00,31.21 60R.94,11.16,33.36 61b.25,10.40,31.16 61R.33,10.74,32.16
62b.25,10.33,30.95 62R.27,10.40,31.16 63b.51,13.81,53.50 63R.99,12.07,35.99 64b.16,10.30,30.86
64R.30,10.45,31.29 65b.16,10.30,30.86 65R.40,10.59,31.73 66b.25,10.37,49.99 66R1.72,33.00,37.12
67b1.06,16.99,38.68 67Q.12,, 67P.13,,105.60 67R1.25,11.47,46.50 68b.21,10.31,49.99
68R.40,10.59,31.72 69J4.00,45.00, 69X4.54,, 69S4.04,10.00,156.19 69b1.99,19.95,101.75
70b.22,10.36,31.04 70R.38,10.74,32.16 71b.05,10.10,30.30 71R.40,10.52,31.51 72b.12,10.18,30.52
72R.50,10.39,31.12 73b.25,10.28,21.75 73R.40,10.59,31.72 74b.66,10.92,32.67 74R.84,10.59,31.73
75S1.69,17.99,59.99 75b1.59,14.92,34.31 76b.50,44.99,152.50 76R.92,65.00,121.33 77b.24,10.33,30.95
77R.65,10.79,32.29 78b.12,10.21,30.60 78R.34,10.49,31.42 79P1.08,11.99, 79b1.11,14.48,40.04
80b.25,10.61,31.77 80R.65,9.37,32.80 81b.32,10.37,31.08 81R.27,5.68,31.16 82b.25,5.50,35.00
82R.50,10.62,31.81 83b.25,10.37,31.08 83R.40,10.59,31.72 84b.20,5.00,30.86 84R.29,12.40,31.29
85b.50,11.61,23.61 85C.85,, 85R.70,11.08,33.15 86b.27,10.31,30.91 86R.28,10.28,30.82
87b.38,10.59,31.73 87R.75,11.11,33.24 88b.17,10.30,30.86 88R.66,11.10,33.19 89b.35,10.59,31.73
89R.41,10.64,31.85 90b.06,10.13,30.39 90R.25,10.51,31.47 91b.24,10.45,31.29 91R.40,10.59,46.07
92b.45,10.50,31.47 92R.80,11.19,33.45 93b.25,10.34,30.99 93R.99,11.47,34.27 94b1.34,15.00,44.43
95b.99,12.50,110.00 95C15.99,,275.00 95P.39,, 95R1.38,12.25,46.03 96b.27,10.52,31.51
96R.40,10.59,31.72 97b.50,10.59,31.72 97R.82,20.00,30.00 98P3.64,, 98b2.00,12.71,67.50
99b.24,16.95,30.65 99R.31,10.59,31.72 100b.38,10.27,30.78 100R.50,11.14,33.32 101b.18,10.36,31.04
101R.40,10.39,31.12 102b.04,10.37,31.08 102R.33,10.59,31.73 103b.18,10.37,31.08 103R.40,10.43,31.25
104b.20,10.24,30.69 104R.32,12.50,235.00 105b.35,14.95,31.68 105R.50,11.07,33.10 106b.19,10.30,30.86
106R.33,11.01,32.93 107b.47,10.71,32.07 107R.68,19.79,32.03 108b.35,10.52,31.51 108R.75,10.92,32.67
109b.10,10.15,30.43 109R.26,10.42,31.21 110b.23,10.42,31.21 110R.42,10.61,31.77 111P1.32,,
111b1.20,16.41,35.12 112b.20,10.36,31.04 112R.42,10.62,31.81 113b.21,10.34,30.99 113R.40,6.68,32.80
114J1.05,21.50,117.16 114S1.62,21.44,67.00 114b1.35,13.81,53.00 115b.28,10.34,30.99
115R.72,11.17,33.41 116b1.04,12.18,36.96 116Q.15,, 116P.18,, 116R.82,14.13,70.00
117b1.25,19.99,122.81 117C59.99,,525.19 117G64.99,83.00,419.79 117M27.85,41.51,575.00 117Q5.53,,
117P1.44,, 117R1.40,19.36,184.06 118b.14,10.25,30.73 118R.41,10.94,32.72 119b.24,10.45,31.29
119R.69,11.47,34.27 120b2.34,13.48,40.09 120R2.22,13.02,38.75 121b1.43,10.64,30.00
122b.21,10.30,30.86 122R.74,11.10,33.19 123b.20,10.22,30.65 123R.40,19.95,31.73 124b.25,10.34,30.99
124R.53,19.00,31.72 125b1.15,11.71,34.96 125R1.47,12.18,25.00 126b.40,10.59,31.72
126R.99,11.25,33.62 127b.69,11.03,32.97 127R.55,11.03,32.97 128b.46,12.50, 128H.19,10.28,30.82
128R.51,24.95,32.16 129b.23,10.36,31.04 129R.40,7.50,31.73 130b.25,10.37,31.08 130R.40,11.90,31.73
131b.13,10.30,30.86 131R.40,8.50,31.51 132b.26,10.45,31.29 132R.47,11.11,33.24 133b.24,10.37,31.08
133R.34,9.34,31.73 134b.20,10.30,30.86 134R.50,10.74,32.22 135b.40,15.48,50.00 135C.67,,25.00
135R.50,5.50,32.80 136b.44,18.75,114.25 136C.29,22.99,40.00 136P.10,, 136R1.06,11.67,33.06
136S8.71,21.50,85.00 137b.19,10.30,30.86 137R.32,10.83,32.41 138b.21,10.33,30.95 138R.40,10.59,31.72
139b.40,10.49,31.42 139R.71,11.44,34.18 140b.38,10.59,31.72 140R.99,11.47,34.27 141b.22,10.24,30.69
141R.29,9.75,31.47 142b.12,10.22,30.65 142R.27,19.79,31.16 143b.34,10.51,31.47 143R.79,10.00,33.45
144b.40,10.64,31.85 144R.49,10.85,32.46 145b.28,10.59,31.72 145R.92,11.10,33.19 146b.61,10.98,32.85
146P.13,, 146R.99,11.35,33.92 147b.20,10.52,31.51 147P.14,, 147R.34,10.59,31.72 148b.40,10.59,31.72
148W2.99,14.44,36.75 148P.19,, 148R.40,10.37,31.08 149b.22,14.00,30.78 149Y,, 149P.12,, 149N61.30,,
149R.36,19.74,31.72 149U84.01,, 150b.16,10.22,30.65 150Z25.00,, 150W.10,10.16,30.47 150P.14,,
150R.43,10.59,31.72 151b.55,14.43,55.88 151C.99,,32.99 151Q.18,, 151P.20,, 151R.40,14.65,31.73
152b.33,10.49,31.42 152P.15,, 152R.99,14.50,47.22 153b.41,25.00,95.00 153Q.20,42.00,127.50 153P.24,,
153R.99,42.25,100.00 154b.20,10.37,31.08 154Q.20,, 154P.23,, 154R.75,10.59,31.72 155b1.06,,
155R.50,10.76,32.20 156b.51,11.00,32.89 156R.79,11.41,34.10 157b.40,10.59,31.72 157R.90,11.44,34.19
158b.40,10.50,31.47 158R.72,11.07,33.10 159b.50,10.74,32.16 159R1.59,12.30,36.68
160b2.79,15.14,53.50 161b21.75,42.93,267.50 162b14.72,28.00,179.22 163b5.32,21.00,68.85
164b5.50,20.00,79.50 165b3.21,16.99,75.00 166b3.74,19.95,73.55 167b17.00,28.62,191.98
167S20.15,30.00,223.24 168b8.12,22.13,132.00 169b5.99,20.55,102.57 170b6.11,19.08,80.75
171b1.89,15.00,41.33 172b2.25,14.33,40.00 173b8.00,20.41,62.33 174b1.79,17.00,37.73
175b4.89,15.00,44.00 176b3.45,17.23,53.00 177b2.51,17.95,56.00 178b2.00,14.73,40.00
179b2.14,19.93,75.00 180b2.25,13.25,44.90 181b1.42,11.08,42.01 182b20.00,26.00,98.40
183b34.52,36.59,109.14 184b96.25,116.70,400.00 185b42.63,51.00,149.00 186b28.24,33.53,130.90
187b56.44,61.33,260.00 188b14.69,24.09,97.47 189b14.66,19.99,80.84 190b4.35,17.16,59.99
"""

RARITY = {"C":"Common", "U":"Uncommon", "R":"Rare", "D":"Double Rare",
          "I":"Illustration Rare", "T":"Ultra Rare",
          "S":"Special Illustration Rare", "H":"Hyper Rare"}

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "R": ("rh",          "Reverse Holo",           "reverse-holo"),
    "C": ("cosmos",      "Cosmos Holo",            "cosmos-holo"),
    "J": ("jumbo",       "Jumbo",                  "jumbo"),
    "P": ("prize",       "Prize Pack",             "prize-pack"),
    "S": ("stamped",     "Stamped Promo",          "stamped"),
    "D": ("holiday",     "Holiday Calendar",       "holiday-calendar"),
    "A": ("cosmosprize", "Cosmos Holo Prize Pack", "cosmos-holo-prize-pack"),
    "H": ("holo",        "Holo",                   "holo"),
    "V": ("prize7",      "Prize Pack Series 7",    "prize-pack-series-7"),
    "Q": ("prizecosmos", "Prize Pack Cosmos Holo", "prize-pack-cosmos-holo"),
    "X": ("jumbostamp",  "Jumbo Stamped",          "jumbo-stamped"),
    "G": ("ebgames",     "EB Games",               "eb-games"),
    "M": ("gamestop",    "GameStop Promo",         "gamestop"),
    "W": ("prizecosmo",  "Prize Pack Cosmo Holo",  "prize-pack-cosmo-holo"),
    "Y": ("gym",         "Gym Promo",              "gym"),
    "N": ("regional",    "Regional Championships", "regional-championships"),
    "U": ("ultraball",   "Ultra Ball League",      "ultra-ball-league"),
    "Z": ("gymstamp",    "Gym Stamp",              "gym-stamp"),
}
ORDER = ["rh"] + [v[0] for v in VARIANTS.values() if v[0] != "rh"]

_names, _rar = {}, {}
for i, line in enumerate(CHECKLIST.strip().splitlines(), 1):
    nm, r = line.rsplit("|", 1)
    _names[i], _rar[i] = nm, RARITY[r]

_TOK = re.compile(r"^(\d+)([bRCJPSDAHVQXGMWYNUZ])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
_px = {}
for tok in PRICES.split():
    m = _TOK.match(tok)
    if not m:
        raise ValueError("bad price token: %r" % tok)
    f = lambda g: float(g) if g else None
    key = (int(m.group(1)), m.group(2))
    if key in _px:
        raise ValueError("duplicate price token: %r" % tok)
    _px[key] = (f(m.group(3)), f(m.group(4)), f(m.group(5)))

# rows with no sale on any of the three grades carry no information — drop them
_px = {k: v for k, v in _px.items() if any(x is not None for x in v)}

BASE, RH, RH_EST, SPECIAL = [], {}, set(), {}
for num in sorted(_names):
    BASE.append((num, _names[num], _rar[num]) + _px.get((num, "b"), (None, None, None)) + (0,))
for (num, v), px in sorted(_px.items()):
    if v == "b":
        continue
    if v == "R":
        RH[num] = px
        continue
    vid, label, suf = VARIANTS[v]
    SPECIAL.setdefault(num, []).append((vid, label, suf) + px)
for num in SPECIAL:
    SPECIAL[num].sort(key=lambda t: ORDER.index(t[0]))

# Where PriceCharting's listing is spelled differently from the card, keep the correct
# name on screen and put PriceCharting's stem in the link:
#   190 is filed as "Spike Energy"
#   142 keeps the ampersand instead of collapsing it to a hyphen
#   69's two promo printings drop the "ex" the base card carries
PCSLUG = {
    190: "spike-energy",
    142: "billy-&-o%27nare",
    (69, "jumbostamp"): "mimikyu",
    (69, "stamped"): "mimikyu",
}

assert len(BASE) == 190, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert len(RH) == 143, len(RH)

SET = {
    "id": "JTG", "name": "Journey Together", "series": "Scarlet & Violet",
    "released": "2025-03-28", "total": 190, "baseTotal": 159,
    "code": "JTG", "pcslug": "pokemon-journey-together",
    "tcgc": "https://www.tcgcollector.com/sets/11645/journey-together",
    "priceDate": "2026-08-19", "accent": "#1cb0d8",
    "logos": [
        "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/sv09.png",
    ],
}
