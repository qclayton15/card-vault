# Scarlet & Violet — 151 (SV3.5 / MEW), released 2023-06-23
# 207 cards (165 base + 42 secret). One standard Reverse Holo pattern covering every
# non-ex base card (153 of them), plus two one-off reverse parallels (a Cosmos reverse
# on #4 and a Play reverse on #16).
#
# Rarities: api.pokemontcg.io/v2/cards?q=set.id:sv3pt5
# Prices:   pricecharting.com/console/pokemon-scarlet-&-violet-151  (captured 2026-08-19)
#
# PriceCharting files a sealed "Poster Collection" product under #49; it is not a card
# and is excluded. Machamp #68, Marowak #105, Vaporeon #134, Mewtwo #150 and Basic
# Psychic Energy #207 were only printed as Holos, so those rows become the base slot.
import re

# one line per card, in number order:  name|rarity code
CHECKLIST = """
Bulbasaur|C
Ivysaur|U
Venusaur ex|D
Charmander|C
Charmeleon|U
Charizard ex|D
Squirtle|C
Wartortle|U
Blastoise ex|D
Caterpie|C
Metapod|C
Butterfree|U
Weedle|C
Kakuna|C
Beedrill|R
Pidgey|C
Pidgeotto|C
Pidgeot|U
Rattata|C
Raticate|U
Spearow|C
Fearow|U
Ekans|C
Arbok ex|D
Pikachu|C
Raichu|R
Sandshrew|C
Sandslash|U
Nidoran ♀|C
Nidorina|U
Nidoqueen|U
Nidoran ♂|C
Nidorino|U
Nidoking|R
Clefairy|C
Clefable|U
Vulpix|C
Ninetales ex|D
Jigglypuff|C
Wigglytuff ex|D
Zubat|C
Golbat|U
Oddish|C
Gloom|U
Vileplume|R
Paras|C
Parasect|U
Venonat|C
Venomoth|U
Diglett|C
Dugtrio|U
Meowth|C
Persian|U
Psyduck|C
Golduck|U
Mankey|C
Primeape|U
Growlithe|C
Arcanine|U
Poliwag|C
Poliwhirl|C
Poliwrath|U
Abra|C
Kadabra|U
Alakazam ex|D
Machop|C
Machoke|U
Machamp|R
Bellsprout|C
Weepinbell|C
Victreebel|U
Tentacool|C
Tentacruel|U
Geodude|C
Graveler|U
Golem ex|D
Ponyta|C
Rapidash|U
Slowpoke|C
Slowbro|U
Magnemite|C
Magneton|U
Farfetch'd|C
Doduo|C
Dodrio|R
Seel|C
Dewgong|U
Grimer|C
Muk|U
Shellder|C
Cloyster|U
Gastly|C
Haunter|U
Gengar|R
Onix|U
Drowzee|C
Hypno|U
Krabby|C
Kingler|U
Voltorb|C
Electrode|R
Exeggcute|C
Exeggutor|U
Cubone|C
Marowak|R
Hitmonlee|U
Hitmonchan|U
Lickitung|C
Koffing|C
Weezing|R
Rhyhorn|C
Rhydon|U
Chansey|R
Tangela|C
Kangaskhan ex|D
Horsea|C
Seadra|U
Goldeen|C
Seaking|U
Staryu|C
Starmie|R
Mr. Mime|R
Scyther|U
Jynx ex|D
Electabuzz|C
Magmar|C
Pinsir|U
Tauros|U
Magikarp|C
Gyarados|R
Lapras|U
Ditto|R
Eevee|C
Vaporeon|R
Jolteon|R
Flareon|R
Porygon|C
Omanyte|U
Omastar|R
Kabuto|U
Kabutops|R
Aerodactyl|R
Snorlax|U
Articuno|R
Zapdos ex|D
Moltres|R
Dratini|C
Dragonair|U
Dragonite|R
Mewtwo|R
Mew ex|D
Antique Dome Fossil|C
Antique Helix Fossil|C
Antique Old Amber|C
Big Air Balloon|U
Bill's Transfer|U
Cycling Road|U
Daisy's Help|U
Energy Sticker|U
Erika's Invitation|U
Giovanni's Charisma|U
Grabber|U
Leftovers|U
Protective Goggles|U
Rigid Band|U
Bulbasaur|I
Ivysaur|I
Charmander|I
Charmeleon|I
Squirtle|I
Wartortle|I
Caterpie|I
Pikachu|I
Nidoking|I
Psyduck|I
Poliwhirl|I
Machoke|I
Tangela|I
Mr. Mime|I
Omanyte|I
Dragonair|I
Venusaur ex|T
Charizard ex|T
Blastoise ex|T
Arbok ex|T
Ninetales ex|T
Wigglytuff ex|T
Alakazam ex|T
Golem ex|T
Kangaskhan ex|T
Jynx ex|T
Zapdos ex|T
Mew ex|T
Bill's Transfer|T
Daisy's Help|T
Erika's Invitation|T
Giovanni's Charisma|T
Venusaur ex|S
Charizard ex|S
Blastoise ex|S
Alakazam ex|S
Zapdos ex|S
Erika's Invitation|S
Giovanni's Charisma|S
Mew ex|H
Switch|H
Basic Psychic Energy|H
"""

# <number><variant char><raw>,<psa9>,<psa10>   blank = no sale on record
PRICES = """
1b1.22,39.60,210.00 1C2.83,16.00,42.67 1R1.51,20.00,79.32 1S43.08,32.44,253.71 2b.73,22.00,91.25
2R1.20,22.01,107.00 3b2.06,12.91,61.00 4b.76,24.49,145.74 4C3.28,22.00,131.42 4G365.00,280.00,802.00
4M44.94,62.09,232.50 4K2.76,,49.40 4R.99,27.00,116.36 5b.89,15.75,109.21 5C1.99,12.53,75.00
5R.60,14.00,120.00 6b8.29,23.19,130.00 7b1.00,18.61,80.00 7C3.00,,90.00 7E100.00,122.12,400.00
7R1.32,13.06,119.50 8b.99,27.71,118.62 8R1.00,20.00,24.99 9J2.27,65.00,179.18 9b2.99,20.82,81.90
10b.38,11.10,34.99 10R.32,16.00,170.00 11b.95,11.67,44.99 11R3.00,13.40,38.46 12b.65,11.23,32.72
12R.43,19.70,42.49 13b.27,10.44,30.97 13R.33,14.95,213.49 14b1.43,12.01,34.48 14R3.00,15.35,35.00
15b.95,11.76,23.50 15R1.66,12.89,20.50 16b.36,14.00,31.56 16Y9.20,,102.50 16R.50,13.40,163.75
17b.79,11.45,33.23 17R2.59,14.08,37.00 18b.41,10.53,44.99 18R.49,20.00,39.99 19b.17,10.44,30.97
19R.42,12.50,50.00 20b.44,15.95,39.99 20R.34,10.50,135.32 21b.33,11.39,33.07 21R2.15,13.00,227.49
22b.23,10.28,30.62 22R.25,10.00,20.00 23b.30,10.53,31.17 23R.62,14.13,187.75 24b2.06,13.65,53.95
25b.99,16.38,140.33 25C5.99,16.50,57.00 25D5.00,25.37,282.00 25T138.51,127.00,469.15
25R1.48,14.95,193.50 26b1.59,14.99,114.99 26C4.00,45.00,224.50 26R2.17,19.00,101.00
27b.25,10.44,30.97 27R.40,14.26,50.50 28b.40,10.70,27.50 28R.53,13.50,31.24 29b1.90,13.33,37.39
29R1.97,11.95,37.51 30b.21,10.44,30.97 30R.30,15.00,31.36 31b.40,12.99,20.00 31R.74,18.50,31.71
32b1.40,13.28,37.28 32R2.99,8.55,41.01 33b.40,10.70,31.56 33R.64,12.83,46.95 34b1.35,11.72,59.99
34R1.79,19.70,38.39 35b.70,11.50,140.00 35R.57,8.55,32.52 36b.35,13.50,44.99 36R.40,8.98,31.56
37b.38,10.61,31.36 37R.40,13.04,141.51 38b2.00,23.07,75.00 39b.36,19.50,120.00 39R.83,19.99,202.50
40b1.57,14.32,62.66 41b.29,10.44,30.97 41R.40,18.85,167.92 42b.25,10.44,30.97 42R.40,15.79,36.50
43b.40,14.00,39.99 43R.32,11.95,219.97 44b.31,13.20,40.00 44R.49,17.00,127.57 45b15.10,9.03,10.00
45H.77,10.05,58.72 45R.96,11.63,96.00 46b.18,10.32,30.70 46R.40,16.06,43.82 47b.25,10.42,30.93
47R.39,11.75,38.58 48b.22,10.40,130.00 48R.32,10.70,29.00 49b.55,10.72,31.60 49R.70,8.58,31.56
50b.39,14.95,31.56 50R.19,14.17,30.70 51b.52,11.03,32.30 51R.50,18.27,18.50 52b.40,13.55,76.00
52R.81,20.00,60.00 53b.40,18.00,31.56 53R.45,14.09,58.50 54b1.23,14.25,212.50 54R1.20,39.06,404.00
55b.28,10.65,31.44 55R.70,13.40,27.50 56b.15,7.01,30.58 56R.77,12.90,34.99 57b.28,10.56,31.24
57R.54,19.70,232.00 58b.48,13.50,31.87 58R.75,31.42,32.92 59b.40,34.03,39.99 59R1.17,19.51,135.04
60b.21,12.50,31.01 60R.61,21.20,49.69 61b1.01,11.77,33.93 61R2.00,13.67,146.00 62b.25,17.90,31.24
62R.40,14.27,124.96 63b.31,14.00,92.00 63C.94,29.44,159.76 63R.50,10.00,42.48 64b.69,14.01,121.00
64C.61,23.76,102.50 64R.40,15.00,116.63 65b2.23,14.80,99.00 66b.24,10.42,30.93 66R.55,11.55,45.71
67b.31,5.00,31.21 67R.40,17.99,82.16 68C1.27,8.50,700.13 68H.99,15.99,500.00 68R.98,15.00,101.26
69b.27,10.70,31.56 69R.70,11.51,255.00 70b1.37,12.15,34.79 70R2.00,16.22,280.00 71b.52,10.70,31.56
71R.37,14.00,81.30 72b.19,10.26,30.58 72R.28,12.70,39.89 73b.34,10.67,31.48 73R.35,22.00,31.56
74b.40,6.50,30.78 74R.62,9.77,110.29 75b.25,16.95,31.05 75R.40,20.25,34.99 76b1.37,15.00,43.69
77b.20,10.44,49.99 77R.40,14.14,70.84 78b.68,11.37,35.00 78R.40,13.00,39.99 79b.62,11.09,130.00
79R.68,22.50,122.88 80b.71,11.44,39.99 80R.86,15.00,108.81 81b.40,10.88,150.00 81R.61,15.77,61.01
82b.40,10.70,185.00 82R.99,15.00,41.57 83b.15,7.01,30.39 83R.43,10.50,37.82 84b.17,10.25,30.54
84R.40,10.02,36.96 85b.99,9.12,26.54 85P22.61,29.99, 85R1.48,13.00,29.99 86b.24,10.35,30.78
86R.37,10.50,123.16 87b.62,10.44,30.97 87R.30,5.00,26.00 88b.28,10.70,82.00 88R.25,14.02,208.49
89b.32,10.54,120.00 89R.41,16.00,32.95 90b.24,10.51,31.13 90R.40,11.55,249.99 91b.40,10.61,31.36
91R.32,12.59,197.49 92b.90,15.00,240.31 92R1.00,16.00,120.00 93b.89,25.00,96.97 93R1.05,23.50,118.25
94b3.04,29.31,265.00 94C28.49,99.99,1385.00 94R8.33,45.00,675.00 95b1.31,12.44,35.41
95R1.99,15.00,37.75 96b.37,10.70,31.56 96R.40,13.00,39.99 97b.99,11.75,33.89 97R1.66,12.91,76.00
98b.24,10.44,30.97 98R.40,12.00,42.00 99b.99,13.77,68.75 99R1.30,11.00,196.69 100b.15,10.21,30.47
100X8500.00,11737.47, 100W2300.00,3893.24,5049.56 100R.40,11.10,45.00 101b1.29,11.00,33.27
101R2.05,16.47,54.22 102b.21,7.01,30.70 102R.60,9.70,27.50 103b.75,11.00,32.22 103R1.53,13.92,125.00
104b.50,18.75,70.00 104R.41,25.00,43.09 105H.45,10.00,32.91 105R.82,12.45,42.50 106b1.24,11.76,40.57
106R2.00,18.99,78.12 107b1.17,15.00,49.99 107R2.98,12.00,42.37 108b.40,10.44,30.97
108R.92,10.91,182.50 109b.25,10.49,32.71 109R.40,10.51,40.00 110b.94,8.43,33.74
110R1.50,15.08,115.41 111b.25,10.47,31.05 111R.26,9.49,157.00 112b.40,10.70,31.56
112R.39,9.50,134.06 113b.65,20.34,131.25 113R1.74,40.56,100.00 114b.28,16.95,31.25
114R.49,14.00,217.50 115b1.54,11.68,27.79 116b.28,10.56,31.24 116R.40,11.00,127.05
117b.25,10.44,30.97 117R.40,13.40,31.36 118b.18,10.35,30.78 118R.50,15.00,31.56 119b1.25,12.19,34.86
119R2.20,13.40,28.42 120b.37,4.99,155.00 120R.49,12.36,31.95 121b1.40,14.99,58.16 121R.99,7.64,37.28
122b1.33,11.00,44.99 122R1.36,12.38,216.10 123b1.38,11.58,33.50 123R2.15,20.25,445.45
124b1.80,15.20,187.13 125b.75,12.75,125.00 125C.47,8.99,109.29 125R.77,7.37,14.50
126b.74,11.84,34.08 126R1.93,16.00,127.50 127b1.30,12.40,35.33 127R1.69,13.75,147.92
128b1.11,12.10,34.67 128R1.33,14.00,34.98 129b.40,8.27,147.50 129R.82,17.70,226.50
130b1.70,12.28,87.79 130R1.62,11.14,430.94 131b.88,14.00,65.01 131R2.42,15.00,28.00
132b4.57,33.00,151.19 132H1.03,20.00,128.50 132P18.12,53.20,300.00 132R2.00,47.00,52.44
133b.53,23.99,64.99 133D2.48,,121.50 133T124.99,121.14,319.86 133R.99,22.46,86.51
134H1.21,9.50,120.00 134R1.55,9.09,28.05 135b1.46,13.04,53.81 135R3.11,12.25,103.50
136b1.38,18.50,110.00 136R1.87,14.00,17.70 137b.18,22.50,38.28 137R.45,28.00,290.88
138b1.13,11.95,34.32 138R1.81,12.40,273.86 139b1.07,9.70,39.62 139R1.48,11.13,36.03
140b1.30,11.61,33.58 140R1.55,14.45,183.65 141b1.28,12.77,40.05 141R1.65,34.95,35.34
142b1.36,14.69,117.50 142R1.75,22.87,187.50 143b1.49,17.74,83.73 143R4.00,17.94,307.65
144b1.00,14.99,36.95 144R1.15,14.51,52.16 145b2.12,20.45,124.26 146b1.94,17.00,45.50
146H1.03,5.17,38.49 146R1.44,15.00,75.00 147b.65,10.70,134.00 147R.86,14.45,41.64
148b1.49,10.25,37.95 148R3.84,8.00,57.51 149b2.01,18.52,117.07 149C5.98,26.89,566.79
149R2.24,23.57,170.75 150H2.75,22.39,135.00 150R3.81,19.75,263.27 151P48.10,91.88,550.00
151U7760.18,8650.00,15504.84 151b7.81,26.74,161.17 152b.63,, 152R1.54,7.50,63.58 153b.86,11.70,33.77
153R1.19,12.10,34.67 154b.84,11.61,33.58 154R1.19,11.56,33.46 155b.48,6.45,32.72
155R1.29,19.25,47.94 156b.51,10.75,31.67 156R.58,11.12,32.49 157b.55,11.03,32.30 157R.70,11.17,32.61
158b.64,10.63,31.40 158R.79,14.00,32.65 159b.47,11.03,32.29 159R1.00,12.00,34.28 160b.84,12.00,20.00
160R.99,11.74,33.85 161b.51,11.10,32.45 161R.99,10.00,38.00 162b.74,, 162R1.00,10.50,33.73
163b.40,10.81,31.79 163R.99,11.28,24.99 164b.50,,150.00 164R1.09,11.42,19.99 165b.74,,
165R.90,12.05,34.55 166b74.99,86.00,340.31 167b44.60,60.00,295.00 168b89.00,122.64,625.65
169b60.54,91.00,490.00 170b85.55,101.59,482.80 171b56.45,76.25,395.00 172b18.16,33.89,180.55
173b80.00,101.25,558.15 174b19.05,34.90,158.42 175b61.25,87.00,474.81 176b37.76,63.51,325.00
177b20.31,36.99,218.75 178b15.40,27.06,156.83 179b13.85,25.49,160.00 180b14.89,27.15,157.95
181b43.51,47.50,264.22 182b15.00,25.19,154.51 183b39.88,50.00,231.75 184b16.80,38.17,157.50
185b7.99,24.03,88.95 186b13.13,30.06,138.43 187b8.16,26.05,104.99 188b11.30,27.11,95.00
189b6.83,20.90,106.50 190b6.67,17.85,75.00 191b5.99,25.99,148.73 192b9.70,26.33,100.00
193b31.80,44.04,210.00 194b3.60,14.42,147.44 195b3.61,14.00,115.00 196b7.61,19.24,64.90
197b5.05,17.56,66.29 198b113.58,119.29,459.92 199b363.10,399.50,1493.00 200b130.32,155.00,593.50
201b67.00,76.39,340.00 202b91.88,105.25,434.87 203b18.64,27.19,127.50 204b17.75,26.97,140.00
205L27.97,55.00,325.50 205b29.31,50.00,302.50 205J159.00,, 206b3.24,16.22,125.00
207H4.68,14.00,42.50
"""

RARITY = {"C":"Common", "U":"Uncommon", "R":"Rare", "D":"Double Rare",
          "I":"Illustration Rare", "T":"Ultra Rare",
          "S":"Special Illustration Rare", "H":"Hyper Rare"}

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "R": ("rh",        "Reverse Holo",             "reverse-holo"),
    "K": ("rhcosmos",  "Reverse Holo Cosmos",      "reverse-holo-cosmos"),
    "Y": ("rhplay",    "Reverse Holo Play",        "reverse-holo-play"),
    "C": ("cosmos",    "Cosmos Holo",              "cosmos-holo"),
    "H": ("holo",      "Holo",                     "holo"),
    "P": ("prize",     "Prize Pack",               "prize-pack"),
    "S": ("stamped",   "Stamped Promo",            "stamped"),
    "G": ("ebgames",   "EB Games",                 "eb-games"),
    "M": ("gamestop",  "GameStop Promo",           "gamestop"),
    "E": ("pokecenter","Pokemon Center",           "pokemon-center"),
    "J": ("jumbo",     "Jumbo",                    "jumbo"),
    "D": ("holiday",   "Holiday Calendar",         "holiday-calendar"),
    "T": ("together",  "Pokémon Together",         "pokemon-together"),
    "X": ("cosprof",   "Cosmos Professor Program", "cosmos-professor-program"),
    "W": ("professor", "Professor Program",        "professor-program"),
    "U": ("ultraball", "Ultra Ball League",        "ultra-ball-league"),
    "L": ("metal",     "Metal",                    "metal"),
}
ORDER = [v[0] for v in VARIANTS.values()]

_names, _rar = {}, {}
for i, line in enumerate(CHECKLIST.strip().splitlines(), 1):
    nm, r = line.rsplit("|", 1)
    _names[i], _rar[i] = nm, RARITY[r]

_TOK = re.compile(r"^(\d+)([bRKYCHPSGMEJDTXWUL])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
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

# Five cards were only ever printed as Holos, so PriceCharting has no plain row for
# them — promote the Holo so the base slot has a price.
_promoted = []
for num in list(_names):
    if (num, "b") not in _px and (num, "H") in _px:
        _px[(num, "b")] = _px.pop((num, "H"))
        _promoted.append(num)

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

# PriceCharting files #207 without the "Basic"
PCSLUG = {207: "psychic-energy"}

assert len(BASE) == 207, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert len(RH) == 153, len(RH)
assert _promoted == [68, 105, 134, 150, 207], _promoted

SET = {
    "id": "MEW", "name": "Scarlet & Violet 151", "series": "Scarlet & Violet",
    "released": "2023-06-23", "total": 207, "baseTotal": 165,
    "code": "MEW", "pcslug": "pokemon-scarlet-&-violet-151",
    "tcgc": "https://www.tcgcollector.com/sets/11584/scarlet-and-violet-151",
    "priceDate": "2026-08-19", "accent": "#4f7ef0",
    "logos": [
        "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/sv03pt5.png",
    ],
}
