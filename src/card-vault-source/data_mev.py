# Mega Evolution (ME01 / MEG) — the era base set, released 2025-09-26
# 188 cards: 132 base + 56 secret (22 Illustration, 22 Ultra, 10 Special Illustration,
# 2 Mega Hyper). One reverse-holo pattern, covering every base card except the ten
# Mega Evolution ex Double Rares, plus a scatter of promo printings.
#
# Checklist: tcgwatchtower.com/pokemon/sets/mega-evolution/base-set/cards
# Prices:    pricecharting.com/console/pokemon-mega-evolution  (captured 2026-08-19)
import re

CHECKLIST = """
1|Bulbasaur|Common
2|Ivysaur|Common
3|Mega Venusaur ex|Double Rare
4|Exeggcute|Common
5|Exeggutor|Uncommon
6|Tangela|Common
7|Tangrowth|Uncommon
8|Chikorita|Common
9|Bayleef|Common
10|Meganium|Rare
11|Shuckle|Uncommon
12|Celebi|Uncommon
13|Seedot|Common
14|Nuzleaf|Common
15|Shiftry|Uncommon
16|Nincada|Common
17|Ninjask|Uncommon
18|Dhelmise|Common
19|Vulpix|Common
20|Ninetales|Uncommon
21|Numel|Common
22|Mega Camerupt ex|Double Rare
23|Litleo|Common
24|Pyroar|Uncommon
25|Volcanion|Uncommon
26|Scorbunny|Common
27|Raboot|Common
28|Cinderace|Rare
29|Sizzlipede|Common
30|Centiskorch|Uncommon
31|Chi-Yu|Uncommon
32|Mantine|Common
33|Corphish|Common
34|Kyogre|Rare
35|Snover|Common
36|Mega Abomasnow ex|Double Rare
37|Clauncher|Common
38|Clawitzer|Rare
39|Sobble|Common
40|Drizzile|Common
41|Inteleon|Uncommon
42|Snom|Common
43|Frosmoth|Uncommon
44|Eiscue|Common
45|Magnemite|Common
46|Magneton|Common
47|Magnezone|Uncommon
48|Raikou|Rare
49|Electrike|Common
50|Mega Manectric ex|Double Rare
51|Pachirisu|Common
52|Helioptile|Common
53|Heliolisk|Common
54|Abra|Common
55|Kadabra|Uncommon
56|Alakazam|Rare
57|Jynx|Common
58|Ralts|Common
59|Kirlia|Common
60|Mega Gardevoir ex|Double Rare
61|Shedinja|Uncommon
62|Spoink|Common
63|Grumpig|Uncommon
64|Xerneas|Rare
65|Greavard|Common
66|Houndstone|Uncommon
67|Gimmighoul|Common
68|Sandshrew|Common
69|Sandslash|Common
70|Onix|Common
71|Tyrogue|Common
72|Makuhita|Common
73|Hariyama|Rare
74|Lunatone|Rare
75|Solrock|Uncommon
76|Riolu|Common
77|Mega Lucario ex|Double Rare
78|Croagunk|Common
79|Toxicroak|Common
80|Marshadow|Uncommon
81|Stonjourner|Uncommon
82|Nacli|Common
83|Naclstack|Common
84|Garganacl|Uncommon
85|Crawdaunt|Uncommon
86|Mega Absol ex|Double Rare
87|Spiritomb|Uncommon
88|Yveltal|Rare
89|Nickit|Common
90|Thievul|Common
91|Shroodle|Common
92|Grafaiai|Common
93|Steelix|Rare
94|Mega Mawile ex|Double Rare
95|Dialga|Rare
96|Tinkatink|Common
97|Tinkatuff|Common
98|Tinkaton|Uncommon
99|Gholdengo|Uncommon
100|Mega Latias ex|Double Rare
101|Latios|Uncommon
102|Spearow|Common
103|Fearow|Common
104|Mega Kangaskhan ex|Double Rare
105|Delibird|Common
106|Miltank|Common
107|Buneary|Common
108|Lopunny|Common
109|Yungoos|Common
110|Gumshoos|Uncommon
111|Stufful|Common
112|Bewear|Common
113|Acerola's Mischief|Uncommon
114|Boss's Orders|Uncommon
115|Energy Switch|Common
116|Fighting Gong|Uncommon
117|Forest of Vitality|Uncommon
118|Iron Defender|Uncommon
119|Lillie's Determination|Uncommon
120|Lt. Surge's Bargain|Uncommon
121|Mega Signal|Uncommon
122|Mystery Garden|Uncommon
123|Pokémon Center Lady|Common
124|Premium Power Pro|Uncommon
125|Rare Candy|Common
126|Repel|Uncommon
127|Risky Ruins|Uncommon
128|Strange Timepiece|Uncommon
129|Surfing Beach|Uncommon
130|Switch|Common
131|Ultra Ball|Common
132|Wally's Compassion|Uncommon
133|Bulbasaur|Illustration Rare
134|Ivysaur|Illustration Rare
135|Exeggutor|Illustration Rare
136|Shuckle|Illustration Rare
137|Ninjask|Illustration Rare
138|Vulpix|Illustration Rare
139|Litleo|Illustration Rare
140|Snover|Illustration Rare
141|Clawitzer|Illustration Rare
142|Inteleon|Illustration Rare
143|Helioptile|Illustration Rare
144|Shedinja|Illustration Rare
145|Houndstone|Illustration Rare
146|Marshadow|Illustration Rare
147|Garganacl|Illustration Rare
148|Spiritomb|Illustration Rare
149|Shroodle|Illustration Rare
150|Steelix|Illustration Rare
151|Spearow|Illustration Rare
152|Delibird|Illustration Rare
153|Gumshoos|Illustration Rare
154|Stufful|Illustration Rare
155|Mega Venusaur ex|Ultra Rare
156|Mega Camerupt ex|Ultra Rare
157|Mega Abomasnow ex|Ultra Rare
158|Mega Manectric ex|Ultra Rare
159|Mega Gardevoir ex|Ultra Rare
160|Mega Lucario ex|Ultra Rare
161|Mega Absol ex|Ultra Rare
162|Mega Mawile ex|Ultra Rare
163|Mega Latias ex|Ultra Rare
164|Mega Kangaskhan ex|Ultra Rare
165|Acerola's Mischief|Ultra Rare
166|Air Balloon|Ultra Rare
167|Buddy-Buddy Poffin|Ultra Rare
168|Fighting Gong|Ultra Rare
169|Lillie's Determination|Ultra Rare
170|Lt. Surge's Bargain|Ultra Rare
171|Mega Signal|Ultra Rare
172|Mystery Garden|Ultra Rare
173|Night Stretcher|Ultra Rare
174|Premium Power Pro|Ultra Rare
175|Rare Candy|Ultra Rare
176|Wally's Compassion|Ultra Rare
177|Mega Venusaur ex|Special Illustration Rare
178|Mega Gardevoir ex|Special Illustration Rare
179|Mega Lucario ex|Special Illustration Rare
180|Mega Absol ex|Special Illustration Rare
181|Mega Latias ex|Special Illustration Rare
182|Mega Kangaskhan ex|Special Illustration Rare
183|Acerola's Mischief|Special Illustration Rare
184|Lillie's Determination|Special Illustration Rare
185|Lt. Surge's Bargain|Special Illustration Rare
186|Wally's Compassion|Special Illustration Rare
187|Mega Gardevoir ex|Mega Hyper Rare
188|Mega Lucario ex|Mega Hyper Rare
"""

# <number><variant><raw>,<psa9>,<psa10>. b base, R Reverse Holo, Y Reverse Play, H Holo,
# C Cosmos Holo, P Prize Pack, Q Prize Pack Cosmos Holo, S Stamped, A Stamped Asia,
# G EB Games, M GameStop, I International Championship. Empty field = no sales data.
PRICES = """
1b.70,17.00,78.95 1R1.18,10.87,99.99 1Y,, 2b.80,11.50,34.48 2R.99,10.15,125.00 3b1.40,16.48,36.00
3P8.36,, 4b.05,10.07,30.23 4R.40,10.70,32.27 5b.10,10.07,30.23 5R.71,7.80,80.00 6b.24,19.00,85.00
6R.40,10.50,81.00 7b.06,10.08,30.27 7R.42,10.59,31.90 8b.40,19.74,31.49 8R.70,8.50,65.00
9b.40,10.56,31.81 9R.74,11.20,89.00 10b2.49,28.00,92.25 10H1.00,11.73,49.00 10R.99,13.30,57.00
11b.23,10.56,31.81 11R.50,14.00,53.75 12b.85,11.22,180.00 12R.89,16.50,37.66 13b.10,10.21,30.68
13I,, 13R.23,10.32,24.76 14b.21,10.30,30.95 14R.40,10.56,31.81 15b.18,10.25,26.00 15R.41,10.35,31.13
16b.08,10.13,30.41 16R.30,10.63,32.04 17b.14,10.35,31.13 17R.75,10.83,32.67 18b.16,10.21,30.68
18R.40,14.95,31.81 19b.55,10.56,31.81 19R.55,10.50,35.30 20b.40,11.43,74.98 20R1.04,15.15,72.50
21b.17,10.24,30.77 21R.40,7.50,31.81 22b.99,10.52,27.81 22P2.51,13.73,41.99 23b.06,10.14,30.45
23R.43,14.00,30.91 24b.13,10.18,30.59 24R.40,10.56,31.81 25b.08,10.14,30.45 25R.40,10.56,45.50
26b.10,10.14,30.45 26R.40,10.56,24.77 27b.21,10.35,31.13 27R.55,10.56,31.81 28b.99,9.52,45.01
28P.13,10.21,30.68 28R.40,10.82,32.62 29b.16,10.35,31.13 29R.50,10.28,30.91 30b.10,10.14,30.45
30R.40,10.62,31.99 31b.30,10.13,30.41 31R.56,9.00,23.50 32b.20,10.35,40.00 32R.86,10.93,32.99
33b.18,10.31,31.00 33R.40,20.00,31.81 34b.94,11.00,43.00 34C1.38,29.99, 34R.80,9.57,34.48
35b.25,10.28,30.91 35R.60,10.99,33.17 36b1.09,13.98,29.27 37b.23,10.28,40.00 37R.40,8.56,41.69
38b.16,8.62,27.00 38C1.82,, 38R.35,10.50,31.58 39b.25,26.99,30.77 39R.50,10.56,31.81
40b.32,10.28,30.91 40R.61,10.86,32.76 41b.10,10.13,30.41 41R.56,11.50,31.58 42b.27,10.42,31.36
42R.87,10.84,32.72 43b.40,10.39,31.27 43R.38,10.52,22.00 44b.08,10.14,40.00 44R.25,10.35,31.13
45b.14,10.07,30.23 45R.28,10.70,32.26 46b.25,10.35,31.13 46R.99,9.61,34.48 47b.15,10.18,30.59
47R.50,10.56,31.81 48b.87,10.38,52.00 48C1.02,11.37,230.00 48R.50,9.50,32.26 49b.25,10.38,31.22
49R.40,12.99,31.81 50b1.27,12.89,27.27 50P2.95,,62.00 51b.10,10.20,30.63 51R.70,15.99,36.00
52b1.13,10.99,79.99 52R.74,10.82,32.63 53b.28,10.41,40.00 53R.40,10.56,31.81 54b.55,10.77,129.99
54R.75,15.70,58.57 55b.79,11.39,34.48 55R.99,10.50,87.49 56b.72,13.50,126.42 56R.75,14.99,107.14
57b.18,10.49,99.99 57R.25,10.51,167.50 58b.67,11.57,44.40 58C.56,, 58R.87,9.54,31.81
59b.37,16.63,115.50 59C.66,, 59R.50,13.50,31.81 60b1.25,14.09,30.00 60P6.63,19.39,60.20
61b.08,10.18,30.59 61R.40,10.56,31.81 62b.25,10.35,31.13 62R.83,14.00,68.00 63b.06,10.08,30.27
63R.31,10.56,31.81 64b6.18,22.50,156.27 64H.91,9.09,32.49 64R.70,10.00,32.04 64S6.53,,109.99
64A45.12,73.52,234.10 65b.50,10.37,49.99 65R.40,10.56,31.81 66b.13,10.11,30.36 66R.38,10.42,31.36
67b.37,10.15,30.50 67R.40,10.56,31.81 68b.45,14.77,71.30 68R1.05,11.89,268.80 69b.10,10.14,30.45
69R.59,10.70,37.00 70b.20,10.32,31.04 70R.40,12.00,32.13 71b.28,10.28,30.91 71R.56,9.99,32.54
72b.25,9.60,31.13 72R.40,10.42,31.36 73H.27,10.44,31.40 73P.18,10.27,30.86 73R.85,11.20,33.85
74b.60,11.34,33.30 74P.20,10.31,31.00 74R.40,10.56,31.81 75b.53,14.95,32.40 75P.19,10.35,260.00
75R.56,10.56,31.81 76b.40,14.73,49.55 76C.51,,202.19 76R.38,19.99,32.99 77b1.09,13.55,36.18
78b.20,10.27,30.86 78R.25,11.08,43.95 79b.02,10.08,30.27 79R.28,10.45,61.00 80b.11,10.14,30.45
80R.20,10.30,30.95 81b.05,10.07,30.23 81R.32,8.56,31.09 82b.16,10.35,31.13 82R.20,10.35,31.13
83b.18,10.23,30.72 83R.39,10.55,30.84 84b.22,10.28,30.91 84R.50,11.05,33.40 85b.18,10.14,30.45
85R.25,10.51,31.63 86b1.49,15.00,34.83 86P5.72,, 87b.40,9.50,43.25 87R.25,10.52,46.25 87S8.81,,
88b.99,12.00,25.75 88G17.03,50.00, 88M19.99,22.10,600.00 88R.40,14.50,49.81 88S4.05,18.38,
89b.10,10.10,30.32 89R.22,7.00,31.13 90b.09,10.14,40.00 90R.40,10.70,32.26 91b.13,10.21,30.68
91R.32,10.50,31.45 92b.17,10.20,30.63 92R.40,10.41,31.31 93b1.49,13.68,28.52 93C1.52,,
93R.40,14.50,41.00 94b1.41,11.68,33.00 94P12.04,, 95b.98,12.43,32.50 95R.29,10.56,31.81
96b.21,10.30,29.99 96R.55,10.41,31.31 97b.22,10.30,30.95 97R.39,9.50,31.77 98b.25,10.30,30.95
98R.56,10.56,31.81 99b.16,10.15,30.50 99R.45,10.63,32.04 100b1.52,13.86,33.00 101b.46,10.38,36.00
101P5.02,45.28,505.00 101R.40,13.18,43.76 102b.05,10.11,40.00 102R.40,14.95,22.50
103b.20,10.28,30.91 103R.83,8.75,51.00 104b1.92,17.00,35.00 104P8.07,,153.51 105b.40,10.35,31.13
105R.30,19.95,41.00 106b.25,10.44,31.40 106R.99,10.99,33.17 107b.40,10.56,31.81 107R.87,11.39,40.00
108b.13,10.18,40.00 108R.40,10.32,31.04 109b.20,14.95,30.45 109R.40,27.00,31.58 110b.18,10.25,30.82
110R.40,11.75,32.22 111b.30,10.42,31.36 111R.70,10.99,29.00 112b.17,10.24,30.77 112R.25,9.50,38.00
113b.20,10.35,64.95 113R.30,19.00,32.26 114b.48,10.56,31.81 114Q1.24,11.59,35.11 114R.35,10.61,31.95
115b.21,10.28,30.91 115R.30,10.44,31.40 116b.27,10.38,31.22 116P.19,10.27,30.86 116R.50,10.49,31.58
117b.59,11.03,33.30 117P.14,10.21,30.68 117Q.15,10.21,30.68 117R1.30,11.84,35.93 118b.21,10.31,31.00
118P.11,, 118Q.08,, 118R.40,8.52,31.81 119b1.24,43.00,52.00 119P.90,, 119R1.79,13.00,47.00
120b.19,10.32,31.04 120R.50,10.00,31.49 121b.17,10.28,30.91 121P.10,, 121R.40,10.56,31.81
122b.13,10.18,30.59 122P.10,, 122Q.12,, 122R.56,10.01,22.50 123b.29,10.45,31.45 123R.55,8.05,23.00
124b.50,10.70,32.26 124P.17,10.24,30.77 124Q.18,, 124R.36,9.39,31.63 125b.50,10.70,32.26
125R.38,9.72,15.50 126b.13,10.28,30.91 126R.25,8.50,31.13 127b.40,10.79,32.54 127P.24,10.35,31.13
127R1.00,11.50,44.90 128b.15,10.27,30.86 128R.32,11.00,31.45 129b.67,10.94,33.03 129R.81,14.00,33.67
130b.19,10.27,30.86 130R.40,9.82,32.04 131b.62,11.03,33.31 131R.99,9.37,34.48 132b1.16,11.63,35.25
132Q.49,, 132R.70,10.93,32.99 133b21.66,30.00,118.70 133S23.24,40.00,735.00 134b19.99,27.73,95.77
135b5.97,20.44,59.99 136b7.01,19.63,75.25 137b4.38,19.12,40.50 138b18.15,27.50,90.50
139b5.03,19.96,56.40 140b2.90,19.52,39.01 141b2.73,15.02,41.68 142b2.75,15.00,41.03
143b3.95,18.74,46.50 144b3.01,18.78,44.50 145b2.99,15.20,45.35 146b14.20,23.30,91.00
147b1.99,13.55,37.08 148b3.03,18.65,44.68 149b2.48,15.24,39.39 150b8.45,21.61,70.00
151b4.61,20.00,54.99 152b3.47,16.97,51.50 153b4.10,16.00,55.00 154b7.22,20.30,54.00
155b11.88,25.58,75.00 156b2.01,15.50,39.10 157b2.49,17.75,41.00 158b2.77,15.55,39.11
159b5.18,20.51,45.99 160b12.99,26.07,83.25 161b5.37,18.49,45.00 162b2.73,21.00,40.31
163b4.99,19.60,52.00 164b5.13,20.99,47.40 165b2.45,15.50,40.47 166b2.40,10.96,38.18
167b4.99,14.00,31.76 168b2.37,11.56,29.11 169b20.25,23.56,56.98 170b1.80,14.00,43.13
171b1.81,12.40,33.00 172b1.74,11.39,25.16 173b4.48,12.00,20.03 174b2.70,9.39,25.50
175b3.99,12.92,32.42 176b3.29,14.00,29.65 177b146.06,143.35,241.17 178b172.70,167.83,383.50
179b194.97,191.25,395.00 180b54.77,63.00,136.50 181b80.20,74.00,213.50 182b52.89,56.69,146.91
183b32.50,27.36,86.69 184b59.84,59.53,144.25 185b18.00,23.25,85.08 186b19.27,33.00,58.65
187b202.71,182.70,595.67 188b241.03,215.29,732.00
"""

VARIANTS = {
    "Y": ("play",     "Reverse Play",          "reverse-play"),
    "H": ("holo",     "Holo",                  "holo"),
    "C": ("cosmos",   "Cosmos Holo",           "cosmos-holo"),
    "P": ("prize",    "Prize Pack",            "prize-pack"),
    "Q": ("prizecos", "Prize Pack Cosmos",     "prize-pack-cosmos-holo"),
    "S": ("stamped",  "Stamped Promo",         "stamped"),
    "A": ("asia",     "Stamped Asia Promo",    "stamped-asia-promo"),
    "G": ("ebgames",  "EB Games Promo",        "eb-games"),
    "M": ("gamestop", "GameStop Promo",        "gamestop"),
    "I": ("intl",     "International Champs",  "international-championship"),
}
_ORDER = ["play", "holo", "cosmos", "prize", "prizecos", "stamped", "asia",
          "ebgames", "gamestop", "intl"]

_names, _rar = {}, {}
for line in CHECKLIST.strip().splitlines():
    n, nm, r = line.split("|")
    _names[int(n)] = nm
    _rar[int(n)] = r

_TOK = re.compile(r"^(\d+)([bRYHCPQSAGMI])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
_px = {}
for tok in PRICES.split():
    m = _TOK.match(tok)
    if not m:
        raise ValueError("bad price token: %r" % tok)
    f = lambda g: float(g) if g else None
    _px.setdefault((int(m.group(1)), m.group(2)),
                   (f(m.group(3)), f(m.group(4)), f(m.group(5))))

# Hariyama #73 was only ever printed as a Holo — promote it so the base slot has a price.
for num in _names:
    if (num, "b") not in _px and (num, "H") in _px:
        _px[(num, "b")] = _px.pop((num, "H"))

BASE, RH, RH_EST, SPECIAL = [], {}, set(), {}
for num in sorted(_names):
    raw, p9, p10 = _px.get((num, "b"), (None, None, None))
    BASE.append((num, _names[num], _rar[num], raw, p9, p10, 0))
for (num, v), px in sorted(_px.items()):
    if v == "b":
        continue
    if v == "R":
        RH[num] = px
    else:
        vid, label, suf = VARIANTS[v]
        SPECIAL.setdefault(num, []).append((vid, label, suf) + px)
for num in SPECIAL:
    SPECIAL[num].sort(key=lambda t: _ORDER.index(t[0]))

assert len(BASE) == 188, len(BASE)
assert all(b[3] is not None for b in BASE), [b[0] for b in BASE if b[3] is None]

# PriceCharting lists these two only under its "prize-pack-cosmo-holo" misspelling
PCPATH = {
    (114, "prizecos"): "boss%27s-orders-ghetsis-prize-pack-cosmo-holo-114",
    (117, "prizecos"): "forest-of-vitality-prize-pack-cosmo-holo-117",
}

SET = {
    "id": "MEV", "name": "Mega Evolution", "series": "Mega Evolution",
    "released": "2025-09-26", "total": 188, "baseTotal": 132,
    "code": "MEG", "pcslug": "pokemon-mega-evolution",
    "tcgc": "https://www.tcgcollector.com/sets/11618/mega-evolution",
    "priceDate": "2026-08-19", "accent": "#f0568f",
    "logos": [
        "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/me01.png",
        "https://archives.bulbagarden.net/media/upload/thumb/8/85/ME1_Logo_EN.png/640px-ME1_Logo_EN.png",
        "https://archives.bulbagarden.net/media/upload/8/85/ME1_Logo_EN.png",
    ],
}
