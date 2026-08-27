# Mega Evolution — Phantasmal Flames (PFL), released 2025-11-14
#
# Prices live in the PRICES block below so refresh_prices.py can rewrite
# them in place; the checklist above them never changes.
import re

# one line per card, in number order:  name|rarity code
CHECKLIST = """
Oddish|C
Gloom|C
Vileplume|R
Mega Heracross ex|D
Lotad|C
Lombre|C
Ludicolo|U
Genesect|R
Nymble|C
Lokix|U
Charmander|C
Charmeleon|C
Mega Charizard X ex|D
Moltres|R
Darumaka|C
Darmanitan|U
Reshiram|R
Oricorio ex|D
Charcadet|C
Ceruledge|U
Seel|C
Dewgong|C
Swinub|C
Piloswine|C
Mamoswine|U
Suicune|R
Piplup|C
Prinplup|C
Rotom ex|D
Yamper|C
Boltund|C
Pawmi|C
Pawmo|C
Pawmot|R
Misdreavus|C
Mismagius ex|D
Snubbull|C
Granbull|U
Cresselia|U
Meloetta|U
Mega Diancie ex|D
Mimikyu|C
Milcery|C
Alcremie|U
Zacian|R
Bramblin|C
Brambleghast|U
Paldean Tauros|U
Gligar|C
Gliscor|U
Trapinch|C
Vibrava|C
Flygon|R
Gastly|C
Haunter|U
Mega Gengar ex|D
Murkrow|C
Honchkrow|U
Sableye|C
Carvanha|C
Mega Sharpedo ex|D
Seviper|U
Absol|C
Sandile|C
Krokorok|C
Krookodile|U
Toxel|C
Toxtricity|R
Eternatus|U
Empoleon ex|D
Bronzor|C
Bronzong|U
Togedemaru|C
Duraludon|C
Archaludon|U
Jigglypuff|C
Wigglytuff|U
Aipom|C
Ambipom|R
Smeargle|C
Zigzagoon|C
Linoone|U
Buneary|C
Mega Lopunny ex|D
Battle Cage|U
Blowtorch|U
Dawn|U
Dizzying Valley|U
Firebreather|U
Grimsley's Move|U
Jumbo Ice Cream|U
Punk Helmet|U
Sacred Charm|U
Wondrous Patch|U
Ludicolo|I
Nymble|I
Dewgong|I
Piplup|I
Yamper|I
Zacian|I
Flygon|I
Paldean Wooper|I
Toxtricity|I
Togedemaru|I
Wigglytuff|I
Meowth|I
Ambipom|I
Mega Heracross ex|T
Mega Charizard X ex|T
Oricorio ex|T
Rotom ex|T
Mismagius ex|T
Mega Sharpedo ex|T
Empoleon ex|T
Mega Lopunny ex|T
Battle Cage|T
Blowtorch|T
Dawn|T
Firebreather|T
Grimsley's Move|T
Punk Helmet|T
Sacred Charm|T
Switch|T
Ignition Energy|T
Mega Charizard X ex|S
Rotom ex|S
Mega Sharpedo ex|S
Mega Lopunny ex|S
Dawn|S
Mega Charizard X ex|H
"""

# <number><variant char><raw>,<psa9>,<psa10>   blank = no sale on record
PRICES = """
1b.24,10.33,31.10 1C1.89,, 1R.70,10.97,33.21 2b.27,10.47,31.56 2C1.20,, 2R.40,10.56,59.95
3b.47,12.25,85.00 3C.96,, 3R.70,10.97,65.00 4b1.26,11.63,34.95 5b.24,10.62,32.06 5R.62,16.00,124.99
6b.21,10.40,31.33 6R.55,10.32,31.06 7b.28,10.39,49.99 7R.34,11.04,33.44 8b.99,99.51,119.00
8H21.93,45.00,119.06 8R.40,10.89,32.94 9b.49,12.99,72.05 9R.98,11.35,79.99 10b.09,10.12,30.41
10R.37,10.42,31.38 11b.70,17.98,42.00 11R1.07,24.04,113.50 12b.57,25.00,30.00 12R.71,19.00,59.00
13b4.49,24.75,75.00 14b.40,12.76,69.95 14P.99,31.00,78.47 14R.65,9.57,85.00 15b.18,10.12,30.41
15R.22,10.55,31.84 16b.15,10.15,30.51 16R.72,11.03,33.40 17b.40,13.94,55.60 17C10.07,,
17H17.99,19.99,425.69 17R.50,8.50,69.95 18b1.21,14.00,35.97 19b.65,10.90,32.98 19R.71,16.00,33.90
20b.50,10.35,31.15 20R.40,12.00,117.48 21b.26,10.36,31.19 21R.62,10.31,31.01 22b.12,10.18,30.60
22R.57,10.78,32.57 23b.13,10.22,30.74 23R.33,10.53,31.74 24b.16,10.21,30.69 24R.52,11.00,32.43
25b.20,10.25,30.83 25R.40,10.76,32.52 26b1.00,32.47,77.00 26C1.62,44.99, 26J28.38,51.00,532.87
26R.45,4.25,125.00 26S27.31,45.17,589.00 27b.99,20.00,99.99 27R1.74,19.94,52.00 28b.23,10.35,31.15
28R.99,10.75,32.48 29b1.15,28.00,31.11 30b.30,10.37,31.24 30R1.02,10.56,31.84 31b.08,10.08,30.28
31R.18,30.00,30.92 32b.34,12.69,31.15 32R.42,11.05,33.49 33b.28,10.08,30.28 33R.55,10.28,30.92
34b.28,12.16,56.00 34C3.00,, 34R.34,10.47,31.56 35b.25,10.60,31.97 35R.74,11.10,33.62
36b1.63,14.63,37.00 37b.25,10.42,31.38 37R.41,10.58,31.93 38b.12,16.95,30.41 38R.24,10.36,31.19
39b.58,10.14,48.00 39R.65,10.90,32.98 40b.45,11.12,33.72 40R1.00,11.37,34.54 41b1.63,14.50,38.68
42b.74,19.95,34.68 42R1.19,15.75,299.00 43b.15,10.14,30.46 43R.87,10.67,32.20 44b.26,11.00,33.30
44R.66,10.92,39.95 45b.36,10.46,31.51 45C3.20,, 45R.77,10.75,32.48 46b.18,10.28,30.92
46R.40,10.79,32.62 47b.11,10.15,30.51 47R.25,10.35,31.15 48b.25,10.36,45.00 48R.54,14.00,33.81
49b.10,13.50,30.46 49R.40,10.29,30.96 50b.25,18.48,56.18 50R.40,11.12,33.72 51b.23,10.35,31.15
51R.66,10.46,31.51 52b.40,10.29,30.96 52R.55,10.54,31.79 53b.35,15.03,50.68 53C2.99,,
53P.70,14.79,33.21 53R.75,11.04,92.00 54b.18,14.00,30.83 54R1.00,16.99,34.73 55b.31,15.23,59.95
55R.78,12.50,70.00 56b2.63,21.00,59.00 57b.40,10.55,45.48 57R.99,11.21,33.99 58b.16,10.22,22.19
58R.40,10.83,32.75 59b.26,10.36,39.95 59R.55,11.19,50.00 60b.53,10.86,49.99 60R.66,10.92,33.03
61b1.67,14.27,37.68 61D14.48,, 62b.24,10.39,31.29 62R.85,10.90,32.98 63b.26,10.36,31.19
63R.89,10.00,39.95 64b.30,10.12,49.99 64R.20,10.35,31.15 65b.10,10.19,49.99 65R.40,10.56,31.84
66b.25,10.37,31.24 66R.28,10.56,31.84 67b.99,11.37,34.54 67R.59,10.00,34.00 68b.20,9.38,40.99
68P.99,11.82,36.01 68R.99,9.99,32.39 69b.40,10.55,31.84 69R1.38,11.44,34.77 70b1.00,18.04,49.99
71b.25,10.33,31.10 71R.31,10.33,31.10 72b.06,10.11,30.37 72R.36,10.49,31.61 73b.08,11.00,30.60
73R.50,10.69,32.29 74b.65,12.50,129.99 74R.85,20.77,165.88 75b.16,10.12,30.41 75R.32,10.43,31.42
76b.29,10.46,31.51 76R.91,11.18,99.99 77b.31,14.66,31.38 77R1.03,11.48,149.99 78b.24,10.73,32.43
78R.75,11.04,33.44 79b.14,15.50,134.32 79R.40,10.55,80.00 80b.14,10.17,30.55 80R.75,13.00,15.00
81b.26,16.00,30.87 81R.70,10.80,32.66 82b.18,10.19,30.64 82R.25,10.71,32.34 83b.21,10.29,30.96
83R.40,10.55,31.84 84b1.38,14.00,27.50 85b.69,10.97,33.22 85R.54,10.74,32.43 86b.13,10.35,31.15
86R.17,10.29,30.96 87b1.11,10.90,32.98 87D1.20,, 87G29.96,, 87M579.02,, 87R1.16,11.55,35.14
88b.10,10.24,30.78 88R.68,10.75,32.48 89b1.12,10.71,32.34 89E.40,, 89R.40,10.61,32.02
90b.40,10.35,31.15 90R.40,10.97,33.21 91b.90,10.55,31.84 91R1.00,11.89,36.24 92b.16,10.22,30.73
92R.20,10.28,29.99 93b.25,10.35,31.15 93R.38,10.55,31.84 94b.53,10.83,32.75 94R.57,10.72,32.39
95b2.78,15.87,58.50 96b1.58,18.74,42.41 97b5.00,18.24,76.15 98b15.39,25.95,128.01
99b3.49,17.48,63.00 100b4.43,16.73,65.48 101b4.57,17.21,87.53 102b3.99,17.57,68.02
103b2.42,16.51,45.00 104b2.71,18.45,51.74 105b6.89,18.50,79.06 106b20.63,35.52,156.62
107b2.86,19.51,57.67 108b2.20,14.85,44.75 109b27.89,37.82,135.50 110b1.69,16.22,37.37
111b2.10,22.07,34.00 112b2.87,16.80,38.74 113b2.70,15.58,38.80 114b2.25,18.70,46.31
115b2.77,17.17,40.24 116b1.75,14.50,28.17 117b1.25,12.33,39.92 118b6.27,15.80,44.00
119b1.25,16.40,34.00 120b1.55,14.00,30.00 121b1.02,11.34,23.35 122b1.26,13.40,29.50
123b2.02,14.00,27.58 124b2.49,11.12,23.71 125b750.00,828.00,1912.50 126b16.87,20.22,74.01
127b20.00,24.00,86.40 128b17.13,21.51,61.83 129b23.28,29.70,88.70 130b305.00,319.07,2310.99
"""

RARITY = {"C":"Common", "R":"Rare", "D":"Double Rare", "U":"Uncommon", "I":"Illustration Rare", "T":"Ultra Rare", "S":"Special Illustration Rare", "H":"Hyper Rare"}

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "R": ("rh",           "Reverse Holo",            "reverse-holo"),
    "C": ("cosmos",       "Cosmos Holo",             "cosmos-holo"),
    "H": ("stamped",      "Stamped Promo",           "stamped"),
    "P": ("holo",         "Holo",                    "holo"),
    "S": ("gamestop",     "GameStop Promo",          "gamestop"),
    "J": ("ebgames",      "EB Games Promo",          "eb-games"),
    "D": ("prize",        "Prize Pack",              "prize-pack"),
    "G": ("regional",     "Regional Championships",  "regional-championships"),
    "M": ("regionalstaff", "Regionals Staff",         "regional-championships-staff"),
    "E": ("prizecosmos",  "Prize Pack Cosmos",       "prize-pack-cosmos"),
}
ORDER = [v[0] for v in VARIANTS.values()]

# prices carried over from a previous capture rather than a fresh sale
EST = {45}
RH_EST = {80}

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

assert len(BASE) == 130, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert len(_names) == 130

SET = {
    "id":"PFL", "name":"Phantasmal Flames", "series":"Mega Evolution",
    "released":"2025-11-14", "total":130, "baseTotal":94,
    "code":"PFL", "pcslug":"pokemon-phantasmal-flames",
    "tcgc":"https://www.tcgcollector.com/sets/11669/phantasmal-flames",
    "priceDate":"2026-08-19", "accent":"#ff6a45",
    "logos":[
      "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/me02.png",   # official Pokemon CDN wordmark
      "https://archives.bulbagarden.net/media/upload/thumb/f/fa/ME2_Logo_EN.png/640px-ME2_Logo_EN.png",
      "https://archives.bulbagarden.net/media/upload/f/fa/ME2_Logo_EN.png",
      "https://archives.bulbagarden.net/media/upload/thumb/7/7f/SetSymbolPhantasmal_Flames.png/120px-SetSymbolPhantasmal_Flames.png",
    ],
}
