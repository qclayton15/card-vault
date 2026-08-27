# Mega Evolution — Perfect Order (ME03 / POR), released 2026-03-27
# num, name, rarity, raw, psa9, psa10, estimated
#
# Prices live in the PRICES block below so refresh_prices.py can rewrite
# them in place; the checklist above them never changes.
import re

# one line per card, in number order:  name|rarity code
CHECKLIST = """
Spinarak|C
Ariados|C
Shaymin|U
Snivy|C
Servine|C
Serperior|R
Scatterbug|C
Spewpa|C
Vivillon|U
Rowlet|C
Dartrix|C
Decidueye ex|D
Fletchinder|C
Talonflame|U
Salandit|C
Salazzle ex|D
Turtonator|U
Seel|C
Dewgong|R
Staryu|C
Mega Starmie ex|D
Lapras ex|D
Amaura|C
Aurorus|R
Volcanion|U
Shinx|C
Luxio|U
Luxray|R
Dedenne|C
Clefairy|C
Mega Clefable ex|D
Mawile|C
Espurr|C
Meowstic|U
Spritzee|C
Aromatisse|U
Nosepass|C
Probopass|C
Hippopotas|C
Hippowdon|U
Landorus|R
Binacle|C
Barbaracle|U
Tyrunt|C
Tyrantrum|R
Hawlucha|C
Mega Zygarde ex|D
Gastly|C
Haunter|C
Gengar|R
Skorupi|C
Drapion|U
Yveltal ex|D
Chien-Pao|R
Mega Skarmory ex|D
Honedge|C
Doublade|C
Aegislash|U
Klefki|C
Rattata|C
Raticate|U
Meowth ex|D
Snorlax|C
Bunnelby|C
Diggersby|U
Fletchling|C
Furfrou|C
Antique Jaw Fossil|C
Antique Sail Fossil|C
Core Memory|U
Crushing Hammer|C
Energy Search|C
Energy Swatter|U
Hole-Digging Shovel|C
Jacinthe|U
Judge|U
Lumiose City|U
Lumiose Galette|U
Naveen|U
Poké Ball|C
Poké Pad|U
Pokémon Catcher|C
Potion|C
Rosa's Encouragement|U
Tarragon|U
Growing Grass Energy|R
Rocky Fighting Energy|R
Telepathic Psychic Energy|R
Spewpa|I
Rowlet|I
Talonflame|I
Aurorus|I
Dedenne|I
Clefairy|I
Espurr|I
Probopass|I
Drapion|I
Doublade|I
Raticate|I
Decidueye ex|T
Salazzle ex|T
Mega Starmie ex|T
Mega Clefable ex|T
Mega Zygarde ex|T
Yveltal ex|T
Mega Skarmory ex|T
Meowth ex|T
Energy Recycler|T
Forest of Vitality|T
Jacinthe|T
Lumiose City|T
Naveen|T
Poké Pad|T
Rosa's Encouragement|T
Sacred Ash|T
Tarragon|T
Wondrous Patch|T
Mega Starmie ex|S
Mega Clefable ex|S
Mega Zygarde ex|S
Meowth ex|S
Jacinthe|S
Rosa's Encouragement|S
Mega Zygarde ex|M
"""

# <number><variant char><raw>,<psa9>,<psa10>   blank = no sale on record
PRICES = """
1b.14,10.32,31.15 1R1.49,11.99,39.00 2b.12,10.29,31.05 2R.44,10.63,32.24 3b.14,10.21,30.76
3R1.39,11.85,36.64 4b.15,10.31,31.10 4R.74,11.04,33.73 5b.10,10.16,30.57 5R1.40,11.87,36.69 6b.69,,
6C.70,10.56,32.01 6H30.00,46.54,292.75 6P9.78,, 6R.99,10.53,31.91 7b.05,10.09,30.33
7R1.29,11.72,36.16 8b.24,10.32,31.15 8R.70,10.93,33.34 9b.44,10.63,32.25 9R.45,2.80,32.15
10b1.33,11.77,36.36 10R.39,10.52,31.86 11b.19,10.23,30.81 11R.25,10.33,31.19 12b1.00,12.26,26.00
13b.20,10.25,30.91 13R1.50,10.00,37.17 14b.40,10.53,31.91 14R.55,18.99,125.00 15b.21,10.29,31.05
15R.56,10.75,32.68 16b1.36,11.25,34.49 17b.10,10.13,30.48 17R.50,10.56,32.01 18b.19,10.32,31.15
18R.60,10.73,32.63 19b.45,10.60,32.15 19R1.60,, 20b.15,10.21,30.76 20R.76,11.15,30.00
21b1.49,12.20,36.51 22b1.20,13.66,22.50 23b.40,10.53,31.91 23R.55,10.73,32.63 24b3.33,27.49,78.97
24R.74,11.33,34.78 25b.14,10.19,30.67 25R.40,10.53,31.91 26b.76,10.39,31.38 26R1.67,11.99,40.00
27b.20,10.27,30.96 27R.52,10.69,32.48 28b1.34,11.98,37.07 28P21.80,25.12,285.00 28R1.21,11.39,34.97
29b.39,10.45,31.62 29R1.69,12.25,38.08 30b.40,8.50,31.91 30R1.49,4.00,89.88 31b1.00,8.50,57.50
32b.20,10.27,30.96 32R1.48,11.97,37.07 33b.71,11.31,34.68 33R1.49,11.91,36.83 34b.13,10.17,30.62
34R1.52,12.03,37.27 35b.21,10.31,31.10 35R.48,10.35,30.00 36b.21,10.36,31.29 36R.32,10.72,70.00
37b.12,10.13,30.48 37R.50,10.53,31.91 38b.19,10.13,30.48 38R.41,10.56,32.01 39b.15,10.20,30.72
39R.40,10.00,32.72 40b.08,10.11,30.38 40R.48,10.53,31.91 41b.25,, 41C.11,10.20,30.72 41R.40,,
42b.16,10.21,30.76 42R1.20,11.60,35.74 43b.25,10.28,31.00 43R.31,10.43,31.53 44b.32,10.40,31.43
44R.26,10.00,31.24 45b1.81,, 45C1.58,11.29,34.63 45R.71,,113.00 46b.22,10.29,31.05
46R.51,10.68,125.00 47b1.10,11.98,30.43 47S15.80,, 48b.25,10.33,31.19 48R1.59,12.12,37.60
49b.54,10.45,31.62 49R1.03,16.15,78.00 50b1.99,99.00,254.00 50D123.54,128.92,807.00
50G105.50,145.50,1405.07 50J14.82,240.00, 50R2.04,33.89,350.00 50S12.99,, 51b.16,10.21,30.76
51R1.49,11.99,25.00 52b.11,10.16,30.57 52R1.39,11.76,36.31 53b1.12,11.45,32.00 54b.31,10.41,31.48
54R.40,, 55b1.67,11.47,41.50 55S13.27,, 56b.16,10.08,30.29 56R1.10,10.75,32.68 57b.56,10.75,32.68
57R.81,11.32,34.73 58b.35,10.41,31.48 58R.72,10.76,47.00 59b.10,10.13,30.48 59R1.42,11.89,36.79
60b.16,10.25,30.91 60R.58,10.77,32.77 61b.25,10.33,31.19 61R1.00,11.33,34.78 62b2.25,20.49,43.00
62S25.50,, 63b.64,10.88,33.15 63R1.25,12.16,37.74 64b.14,10.12,30.43 64R1.17,11.56,35.59
65b.15,10.20,30.72 65R1.25,11.67,35.97 66b.06,10.08,30.29 66R1.30,11.73,36.21 67b.25,10.15,30.53
67R.41,10.93,33.34 68b.66,11.32,34.73 68R1.18,11.71,36.12 69b.37,10.53,31.91 69R.55,10.93,33.34
70b.14,10.19,30.67 70R.33,10.53,31.91 71b.85,10.43,31.53 71R1.32,11.76,36.31 72b.29,10.44,31.58
72R1.54,11.93,50.07 73b.27,10.40,31.43 73R1.44,11.92,36.88 74b.12,10.16,30.57 74R1.54,12.06,37.35
75b.25,10.33,31.19 75R.34,10.00,31.91 76b.53,10.79,32.82 76E335.00,, 76M35.61,, 76R.95,11.25,34.49
77b.39,10.51,31.82 77R.99,11.32,34.73 78b.16,10.32,31.15 78R.76,10.53,31.91 79b.28,10.39,31.39
79R.31,10.53,31.91 80b.23,10.33,31.19 80R.55,10.53,31.91 81b1.00,11.43,35.11 81R.97,13.48,30.00
82b.11,10.19,30.67 82R.92,11.16,34.15 83b.20,10.27,30.96 83R.90,11.32,34.73 84b.40,10.53,31.91
84R.99,11.49,35.35 85b.40,10.53,31.91 85R.33,10.53,31.91 86b.32,, 86C.68,10.84,33.01
86R.92,10.53,31.91 87b1.87,10.00, 87C.99,11.32,34.73 87R.72,10.89,33.20 88b1.69,, 88C.99,10.00,34.73
88R1.29,11.77,36.35 88S1.79,, 89b2.26,15.31,64.91 90b5.10,21.01,83.50 91b2.95,21.00,53.95
92b3.75,30.88,90.06 93b5.12,21.20,91.50 94b21.29,32.00,163.75 95b4.40,13.75,60.00
96b1.40,14.50,38.95 97b1.86,15.00,48.84 98b2.99,31.00,64.81 99b3.00,24.73,74.51 100b3.10,16.20,40.50
101b2.26,25.00,46.76 102b6.50,27.17,77.41 103b6.45,22.41,58.00 104b6.00,33.00,80.31
105b5.97,28.18,109.50 106b4.99,26.96,71.50 107b14.00,31.47,114.29 108b2.69,13.67,16.00
109b4.94,19.50,36.01 110b2.97,22.00,56.50 111b3.06,13.44,46.00 112b2.51,17.40,40.50
113b10.20,13.00,68.47 114b5.00,24.13,84.50 115b2.00,12.67,38.00 116b2.04,4.50,37.48
117b3.25,12.36,46.43 118b39.07,71.00,172.00 119b55.89,59.48,153.35 120b57.66,74.00,195.32
121b129.46,154.00,331.00 122b24.71,27.50,121.88 123b45.49,67.50,228.44 124b130.81,145.00,560.00
"""

RARITY = {"C":"Common", "U":"Uncommon", "R":"Rare", "D":"Double Rare", "I":"Illustration Rare", "T":"Ultra Rare", "S":"Special Illustration Rare", "M":"Mega Hyper Rare"}

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "R": ("rh",           "Reverse Holo",            "reverse-holo"),
    "C": ("holo",         "Holo",                    "holo"),
    "H": ("prestaff",     "Prerelease Staff",        "prerelease-staff"),
    "P": ("stamped",      "Stamped Promo",           "stamped"),
    "S": ("prize",        "Prize Pack",              "prize-pack"),
    "J": ("cosmos",       "Cosmos Holo",             "cosmos-holo"),
    "D": ("gamestop",     "GameStop Promo",          "gamestop"),
    "G": ("ebgames",      "EB Games Stamped",        "eb-games-stamped"),
    "M": ("regional",     "Regional Championships",  "regional"),
    "E": ("regionalstaff", "Regionals Staff",         "regional-staff"),
}
ORDER = [v[0] for v in VARIANTS.values()]

# prices carried over from a previous capture rather than a fresh sale
EST = set()
RH_EST = set()

_names, _rar = {}, {}
for i, line in enumerate(CHECKLIST.strip().splitlines(), 1):
    nm, r = line.rsplit("|", 1)
    _names[i], _rar[i] = nm, RARITY[r]

_TOK = re.compile(r"^(\d+)([bCDEGHJMPRS])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
_px = {}
for t in PRICES.split():
    mt = _TOK.match(t)
    if not mt:
        raise ValueError("bad price token: %r" % t)
    f = lambda g: float(g) if g else None
    key = (int(mt.group(1)), mt.group(2))
    if key in _px:
        raise ValueError("duplicate price token: %r" % t)
    _px[key] = (f(mt.group(3)), f(mt.group(4)), f(mt.group(5)))

BASE, RH, SPECIAL = [], {}, {}
for num in sorted(_names):
    BASE.append((num, _names[num], _rar[num])
                + _px.get((num, "b"), (None, None, None)) + (1 if num in EST else 0,))
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

assert len(BASE) == 124, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert len(_names) == 124

# PriceCharting files Serperior's two promos under #64 rather than #6
PCPATH = {
    (6, "prestaff"): "serperior-prerelease-staff-64",
    (6, "stamped"):  "serperior-stamped-64",
}

SET = {
    "id":"POR", "name":"Perfect Order", "series":"Mega Evolution",
    "released":"2026-03-27", "total":124, "baseTotal":88,
    "code":"POR", "pcslug":"pokemon-perfect-order",
    "tcgc":"https://www.tcgcollector.com/sets/11685/perfect-order",
    "priceDate":"2026-08-19", "accent":"#22c08d",
    "logos":[
      "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/me03.png",   # official Pokemon CDN wordmark
      "https://archives.bulbagarden.net/media/upload/thumb/a/ae/ME3_Logo_EN.png/640px-ME3_Logo_EN.png",
      "https://archives.bulbagarden.net/media/upload/a/ae/ME3_Logo_EN.png",
      "https://archives.bulbagarden.net/media/upload/thumb/0/09/SetSymbolPerfect_Order.png/120px-SetSymbolPerfect_Order.png",
    ],
}
