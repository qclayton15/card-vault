# Scarlet & Violet — Prismatic Evolutions (SV8.5 / PRE), released 2025-01-17
# 180 cards (131 base + 49 secret). Three parallel patterns on the base set, like
# Ascended Heroes: every Common/Uncommon/Rare gets both a plain Reverse Holo and a
# Poké Ball Reverse (100 each), and the 67 Pokémon among them also get a Master Ball
# Reverse — the Trainers (#93-130) do not. Double Rares and ACE SPECs get none.
# All three route through SPECIAL, so RH is empty.
#
# Rarities: api.pokemontcg.io/v2/cards?q=set.id:sv8pt5
# Prices:   pricecharting.com/console/pokemon-prismatic-evolutions  (captured 2026-08-19)
import re

# one line per card, in number order:  name|rarity code
CHECKLIST = """
Exeggcute|C
Exeggutor|U
Pinsir|C
Budew|C
Leafeon|R
Leafeon ex|D
Cottonee|C
Whimsicott|R
Applin|C
Dipplin|U
Hydrapple ex|D
Teal Mask Ogerpon ex|D
Flareon|R
Flareon ex|D
Litleo|C
Pyroar|U
Hearthflame Mask Ogerpon ex|D
Slowpoke|C
Slowking|U
Goldeen|C
Seaking|U
Vaporeon|R
Vaporeon ex|D
Suicune|U
Glaceon|R
Glaceon ex|D
Wellspring Mask Ogerpon ex|D
Pikachu ex|D
Jolteon|R
Jolteon ex|D
Iron Hands ex|D
Iron Thorns ex|D
Espeon|R
Espeon ex|D
Duskull|C
Dusclops|C
Dusknoir|R
Spritzee|C
Aromatisse|C
Sylveon|R
Sylveon ex|D
Scream Tail|U
Flutter Mane|R
Munkidori|R
Fezandipiti|R
Iron Boulder|R
Larvitar|C
Pupitar|C
Groudon|R
Riolu|C
Lucario ex|D
Hippopotas|C
Hippowdon|C
Bloodmoon Ursaluna|R
Great Tusk|U
Sandy Shocks ex|D
Okidogi|R
Cornerstone Mask Ogerpon ex|D
Umbreon|R
Umbreon ex|D
Sneasel|C
Houndour|C
Houndoom|C
Tyranitar ex|D
Roaring Moon|R
Bronzor|C
Bronzong|U
Heatran|U
Duraludon|C
Archaludon|R
Dreepy|C
Drakloak|C
Dragapult ex|D
Eevee|C
Eevee ex|D
Snorlax ex|D
Hoothoot|C
Noctowl|R
Dunsparce|C
Dudunsparce|R
Miltank|C
Lugia ex|D
Buneary|C
Lopunny|C
Fan Rotom|C
Regigigas|U
Shaymin|U
Furfrou|C
Hawlucha|U
Noibat|C
Noivern ex|D
Terapagos ex|D
Amarys|C
Area Zero Underdepths|U
Binding Mochi|U
Black Belt's Training|C
Black Belt's Training|C
Black Belt's Training|C
Black Belt's Training|C
Briar|U
Buddy-Buddy Poffin|U
Bug Catching Set|U
Carmine|U
Ciphermaniac's Codebreaking|U
Crispin|U
Earthen Vessel|U
Explorer's Guidance|U
Festival Grounds|U
Friends in Paldea|C
Glass Trumpet|U
Haban Berry|C
Janine's Secret Art|U
Kieran|U
Lacey|U
Larry's Skill|C
Max Rod|A
Maximum Belt|A
Ogre's Mask|U
Prime Catcher|A
Professor Sada's Vitality|U
Professor Turo's Scenario|U
Professor's Research (Professor Oak)|C
Professor's Research (Professor Elm)|C
Professor's Research (Professor Rowan)|C
Professor's Research (Professor Sycamore)|C
Rescue Board|U
Roto-Stick|C
Scoop Up Cyclone|A
Sparkling Crystal|A
Techno Radar|U
Treasure Tracker|A
Amarys|T
Atticus|T
Atticus|T
Brassius|T
Eri|T
Friends in Paldea|T
Giacomo|T
Larry's Skill|T
Mela|T
Ortega|T
Raifort|T
Tyme|T
Leafeon ex|S
Teal Mask Ogerpon ex|S
Flareon ex|S
Ceruledge ex|S
Hearthflame Mask Ogerpon ex|S
Vaporeon ex|S
Glaceon ex|S
Palafin ex|S
Wellspring Mask Ogerpon ex|S
Jolteon ex|S
Iron Hands ex|S
Espeon ex|S
Sylveon ex|S
Iron Valiant ex|S
Iron Crown ex|S
Sandy Shocks ex|S
Cornerstone Mask Ogerpon ex|S
Umbreon ex|S
Roaring Moon ex|S
Pecharunt ex|S
Gholdengo ex|S
Dragapult ex|S
Raging Bolt ex|S
Eevee ex|S
Bloodmoon Ursaluna ex|S
Terapagos ex|S
Amarys|S
Crispin|S
Drayton|S
Janine's Secret Art|S
Kieran|S
Lacey|S
Iron Leaves ex|H
Teal Mask Ogerpon ex|H
Walking Wake ex|H
Pikachu ex|H
Terapagos ex|H
"""

# <number><variant char><raw>,<psa9>,<psa10>   blank = no sale on record
PRICES = """
1b.07,12.00,39.59 1K1.52,9.72,71.04 1B.38,13.00,31.50 1R.27,12.00,85.00 2b.25,18.42,31.61
2K10.79,12.00,200.00 2B.48,11.35,41.59 2R.38,10.65,31.82 3b.07,12.00,100.00 3K1.53,11.99,149.99
3B.50,14.40,41.00 3R.54,11.15,33.22 4b.78,11.18,143.96 4Y43.02,, 4K3.38,22.00,87.75
4B.99,15.00,40.50 4G2713.40,,139.99 4L137.57,91.00, 4Q2.78,, 4P.40,, 4R.88,12.49,45.68
5b1.50,21.85,59.99 5C1.78,35.91,381.00 5K32.85,29.99,187.50 5B2.40,16.40,57.00 5R1.49,19.24,49.50
6V18.77,46.00,231.74 6S9.50,23.50,83.94 6b4.42,21.00,65.85 7b.12,10.29,20.00 7K1.31,10.63,58.78
7B.40,13.00,35.79 7R.16,10.17,22.76 8b.16,17.00,76.60 8K11.31,10.00,129.99 8B.64,13.00,62.50
8R.15,10.27,26.00 9b.12,4.00,30.68 9K2.85,15.50,90.61 9B1.21,14.00,38.61 9R.50,10.76,13.00
10b.40,10.46,31.27 10K2.46,17.00,87.23 10B1.00,11.49,34.99 10R.48,15.00,32.04 11b1.26,15.00,26.00
12b3.21,17.49,39.16 13b1.32,24.99,40.00 13C1.42,37.88,220.50 13K30.00,33.68,227.15
13B1.59,15.49,48.92 13R1.50,19.00,52.06 14P22.55,35.75,90.25 14b4.52,24.00,60.08 14S7.55,20.50,77.00
15b.07,3.42,39.99 15K2.22,10.08,99.77 15B.57,13.00,26.25 15R.16,9.51,43.62 16b.25,19.95,26.00
16K1.31,10.00,127.59 16B.35,8.63,58.55 16R.25,10.38,31.06 17b.99,15.40,28.92 18b.85,15.00,119.11
18K7.39,18.49,154.01 18B1.14,15.25,89.50 18R1.19,12.40,84.95 19b.40,8.10,150.00 19K3.34,19.99,166.94
19B.51,18.99,66.45 19R.62,15.00,85.51 20b.40,10.76,32.12 20K2.97,14.75,132.50 20B.84,15.25,20.00
20R.70,13.01,40.00 21b.25,14.95,46.50 21K3.20,15.43,102.26 21B.82,14.50,23.99 21R.98,6.50,100.00
22b1.59,14.93,420.44 22C1.25,34.99, 22K38.67,48.00,500.00 22B1.79,18.42,96.50 22R1.56,24.99,87.66
23P20.50,58.00,150.00 23b3.20,18.25,71.39 23S7.57,25.06,86.75 24b.50,6.00,68.10
24K12.99,19.88,154.50 24B.75,14.00,44.73 24R.99,14.45,60.00 25b1.45,19.14,117.50
25C1.95,19.99,448.25 25K25.93,34.99,239.03 25B1.34,14.25,52.00 25R1.59,17.48,50.50
26D2.70,19.79,43.62 26V17.14,55.00, 26b2.65,15.00,62.95 26S9.77,20.49,87.50 27b.99,15.25,36.43
28b2.76,30.45,122.25 29b.89,18.93,54.50 29C1.92,28.00, 29K31.50,33.00,176.74 29B1.73,17.98,54.36
29R1.41,22.00,46.13 30P19.00,42.00,130.00 30b3.91,23.55,70.00 30S9.43,24.49,76.00 31b.99,11.70,50.00
32b1.05,13.68,31.25 33b1.07,14.25,51.00 33C4.72,32.50,890.00 33K28.83,39.79,265.00
33B2.44,18.08,61.61 33R1.12,21.99,51.54 34P18.00,20.51,291.84 34b3.41,24.99,64.00
34S8.59,22.68,79.99 35b.40,10.91,32.54 35K2.76,15.00,80.74 35B1.07,16.00,42.95 35R.90,13.50,33.39
36b.40,12.48,52.98 36K2.40,13.25,92.37 36B.81,15.01,46.38 36R.89,11.35,33.77 37b.40,13.43,100.00
37K10.84,19.75,205.00 37B.64,12.00,33.30 37R.75,2.41,32.97 38b.08,16.60,49.95 38K1.00,15.34,125.00
38B.40,11.69,28.00 38R.23,10.00,31.27 39b.12,12.00,30.51 39K6.83,12.00,116.50 39B.55,10.57,12.51
39R.14,10.35,30.98 40b1.61,22.00,45.61 40C4.69,34.01,190.10 40K32.92,38.58,224.98
40B2.48,15.00,53.00 40M9.44,21.90,110.92 40R1.49,18.50,42.08 41b3.08,18.00,66.33
41S10.00,29.00,86.00 42b.25,15.00,100.00 42K8.99,10.61,127.50 42B.50,9.06,32.51 42R.21,10.00,82.50
43b.73,15.00,59.68 43K12.18,10.25,81.99 43B.75,18.00,31.26 43R.25,13.00,29.00 44b1.00,12.00,129.00
44K12.09,14.00,142.00 44B.99,14.01,40.30 44R.69,11.15,33.22 45b.39,13.41,24.95 45K6.84,11.35,254.76
45B.49,14.00,32.08 45R.17,10.58,31.61 46b.48,12.00,69.95 46K7.57,21.36,180.00 46B.47,15.00,37.00
46R.25,8.00,39.99 47b.12,10.24,95.00 47K2.41,18.56,113.46 47B.50,10.49,49.48 47R.23,17.95,31.91
48b.22,10.15,30.42 48K9.00,17.20,68.15 48B.50,13.51,39.63 48R.28,10.42,100.00 49b.50,12.23,32.63
49K10.32,15.00,185.00 49B.50,20.42,51.00 49R.25,10.50,31.57 50b.99,11.50,92.58 50K13.23,15.37,111.00
50B.88,16.89,35.73 50R.95,14.95,35.05 51S1.83,22.00,66.50 51b1.40,21.00,71.04 51J3.47,36.00,84.00
52b.05,12.75,31.14 52K1.91,14.83,92.00 52B.68,9.00,32.59 52R.15,10.23,55.00 53b.07,32.00,38.00
53K5.98,13.80,117.00 53B.68,16.01,60.29 53R1.51,12.26,36.33 54b.26,13.99,56.25 54K8.88,12.51,102.50
54B.42,12.11,31.12 54R.12,8.95,40.00 55b.08,21.35,45.11 55K6.37,7.00,133.50 55B1.00,16.79,56.04
55R.50,10.08,49.99 56b.85,22.00,32.50 57b.16,10.00,11.80 57K7.18,15.39,203.72 57B.42,17.00,39.08
57R.25,10.61,31.70 58b1.00,13.00,50.00 59b1.05,20.38,75.00 59C15.28,38.00,575.21
59K80.00,92.67,600.43 59B4.25,24.99,97.95 59R1.40,23.36,94.00 60P63.47,61.00,451.25
60b7.10,20.25,109.75 60S23.63,28.64,136.28 61b.11,13.00,30.42 61K1.99,10.07,50.00 61B.40,16.00,49.36
61R.21,10.12,30.34 62b.18,10.50,71.00 62K1.53,13.70,85.00 62B.49,13.26,38.10 62R.30,12.40,40.00
63b.41,15.00,160.00 63K10.31,22.99,165.67 63B.99,16.00,70.00 63R.13,9.19,47.75 64S1.99,17.63,68.66
64b1.55,18.48,63.00 65b.44,12.00,60.63 65K7.46,12.19,101.23 65B.38,10.17,32.75 65R.63,11.75,71.00
66b.02,10.03,30.08 66K1.06,12.15,96.02 66B.73,13.00,23.66 66R.03,10.08,38.00 67b.09,10.30,66.50
67K5.25,12.95,49.72 67B.40,10.00,36.25 67R.02,10.05,30.13 68b.10,4.14,30.38 68K1.54,17.28,129.99
68B.32,19.95,34.83 68R.13,10.30,30.85 69b.14,12.49,33.00 69K2.20,11.35,79.99 69B.36,11.50,46.71
69R.20,10.38,23.54 70b.10,8.99,25.05 70K4.99,11.83,170.00 70B.55,9.72,50.00 70R.12,10.38,31.06
71b.17,10.90,80.00 71K2.32,10.04,78.30 71B1.13,13.50,80.02 71R.56,9.09,38.00 72b.25,10.83,91.90
72K3.25,12.00,72.25 72B1.10,18.05,39.64 72R.64,7.55,44.30 73J3.72,, 73b1.62,12.73,30.00
74b1.03,23.93,53.28 74K17.39,26.78,199.19 74B2.31,20.00,56.00 74N4.58,19.99,107.86
74R1.10,19.00,61.01 75P26.04,32.00,250.00 75S12.00,26.00,117.90 75b6.00,22.75,87.50
76S4.97,27.00,164.63 76b2.45,20.62,150.00 76J5.95,20.31,58.62 77b.30,10.46,76.02
77K1.89,17.74,116.14 77B.78,12.50,18.50 77R.53,15.24,31.12 78b.24,10.98,40.00 78K8.50,21.00,127.50
78B.71,8.66,84.99 78R.69,10.61,178.00 79b.20,22.00,69.95 79K2.40,7.09,133.43 79B1.02,19.24,21.00
79R.79,11.20,119.00 80b1.31,12.99,59.17 80K19.22,14.50,69.99 80B1.42,5.10,20.50 80R1.24,11.00,100.00
81b.20,19.95,30.00 81K1.60,19.56,130.50 81B.49,19.50,40.00 81R.39,35.00,42.00 82S7.93,30.99,308.36
82b1.99,18.54,152.50 82J4.83,31.50,50.42 83b.17,28.00,30.72 83K1.35,16.50,109.99 83B.56,13.05,59.99
83R1.49,19.95,63.00 84b.25,10.23,30.64 84K8.83,13.52,77.00 84B.45,15.00,35.00 84R1.24,11.67,34.67
85b.40,10.00,55.50 85K1.95,17.00,100.94 85B.99,16.00,34.20 85R1.40,12.12,35.94 86b.40,16.95,89.03
86K1.92,12.17,110.50 86B.55,15.00,215.99 86P.14,, 86R1.78,12.70,60.00 87b.16,13.99,34.99
87K7.35,11.72,125.81 87B.86,14.40,65.50 87R.30,10.00,32.59 88b.08,10.09,30.25 88K8.87,20.00,79.99
88B.28,15.00,50.00 88R1.27,11.93,35.39 89b.12,9.41,80.00 89K1.34,15.00,121.75 89B.57,16.00,40.00
89R1.79,12.71,38.00 90b.29,10.33,30.93 90K1.53,13.05,93.73 90B.50,10.99,32.25 90R.60,5.24,44.99
91b1.35,17.27,42.00 92b1.17,14.04,34.95 93b.05,10.09,49.95 93B.40,14.00,40.00 93R.99,11.94,35.43
94b.21,9.99,30.93 94B.36,21.00,25.00 94R1.44,, 95b.21,15.99,30.98 95B.53,13.50,33.26
95R1.76,12.67,59.95 96b.10,12.00,38.00 96B.49,9.00,42.00 96R1.41,12.12,35.94 97b.12,20.00,85.00
97B.26,15.00,31.53 97R1.25,11.83,35.13 98b.18,19.49,30.34 98B.54,10.82,69.95 98R1.44,25.00,36.06
99b.03,14.00,51.00 99B.38,10.00,50.00 99R1.59,12.41,36.75 100b.25,10.27,30.76 100B.49,13.00,57.47
100R1.42,2.63,36.02 101b.55,16.00,44.00 101B.94,17.00, 101R1.76,13.79,36.83 102b.40,10.76,32.12
102B2.05,11.53,56.48 102R.35,10.77,32.16 103b.15,10.23,30.64 103B.99,12.00,35.98
103R1.35,11.84,35.13 104b.27,10.40,39.99 104B.40,10.61,32.00 104R1.31,11.52,34.24
105b.28,14.95,31.19 105B1.04,13.00,26.70 105R1.20,9.13,35.09 106b.23,42.00,59.95 106B.46,10.70,42.00
106R1.37,12.03,39.99 107b.28,10.42,23.57 107B.35,8.50,27.86 107R1.00,9.35,40.00 108b.19,10.38,31.06
108B.62,16.37,34.24 108R1.21,11.26,35.30 109b.12,15.00,30.85 109B.48,10.79,32.21 109R.17,10.26,30.72
110b.11,10.23,39.99 110B.53,9.50,50.00 110R1.26,11.81,35.05 111b.05,10.14,30.38 111B.52,7.00,33.18
111R1.30,7.99,35.51 112b.24,13.49,30.00 112B.41,11.00,31.70 112R1.37,12.09,35.85 113b.40,10.61,59.95
113B.37,11.99,85.00 113R1.19,11.82,35.09 114b.20,9.99,30.42 114B.39,10.00,55.00
114R1.59,12.00,175.00 115b.25,10.47,31.31 115B.99,14.23,94.98 115R1.49,12.27,36.36
116b1.48,13.96,50.50 116P10.14,, 117b1.91,11.75,18.05 118b.10,13.00,35.00 118B.34,10.25,40.00
118R1.40,18.00,59.95 119b.99,10.23,40.00 120b.11,8.50,61.00 120B.33,14.00,31.32 120R.18,10.26,27.00
121b.25,8.50,22.73 121B.32,10.50,40.00 121R1.21,11.97,35.51 122b.13,10.24,30.68 122B.35,10.49,23.00
122R1.80,, 123b.09,10.14,30.38 123B.29,, 123R.99,, 124b.11,10.17,30.47 124B.29,, 124R1.40,,
125b.05,10.08,30.21 125B.31,,28.99 125R1.99,, 126b.06,10.11,30.30 126B.49,13.55,19.50
126R1.20,12.08,35.81 127b.40,10.53,31.48 127B.55,12.00,60.00 127R1.07,11.79,35.00
128b1.00,12.00,21.28 129b1.00,12.70,39.99 130b.13,14.00,59.95 130B.50,14.50,69.37
130R.05,10.33,30.93 131b1.00,11.42,18.50 132b1.25,16.00,39.95 133b1.00,15.31,33.65
134b1.00,13.23,46.89 135b1.24,12.38,38.37 136b1.38,17.27,53.06 137b1.25,14.06,46.00
138b1.25,11.13,29.99 139b1.67,12.81,45.69 140b1.91,15.00,36.91 141b1.00,13.25,34.00
142b1.18,13.86,34.00 143b1.67,17.40,27.03 144b302.50,290.00,872.50 145b19.85,28.00,90.26
146b209.72,190.00,689.33 147b90.54,88.00,333.00 148b18.22,27.50,90.93 149b254.74,257.37,1022.14
150b253.51,259.36,762.50 151b40.00,42.50,170.15 152b17.00,27.00,85.30 153b196.81,190.00,660.00
154b33.34,30.10,140.75 155b298.99,290.63,1175.00 156b466.23,470.00,1525.00 157b45.00,47.95,191.86
158b32.75,32.00,109.69 159b24.45,26.24,111.28 160b15.46,24.28,83.50 161b1410.50,1394.71,5827.00
162b172.00,162.13,688.50 163b30.09,35.00,129.57 164b44.94,46.76,194.36 165b102.10,106.39,238.84
166b67.03,56.00,227.94 167b158.14,177.50,580.50 168b63.88,60.56,250.56 169b29.99,34.51,122.08
170b13.86,18.99,80.00 171b32.64,24.78,66.50 172b16.38,14.00,77.88 173b24.24,25.00,80.91
174b18.66,23.00,69.33 175b20.70,25.00,81.74 176b5.99,18.50,85.80 177b8.28,18.99,107.84
178b7.19,21.91,83.50 179b62.73,83.43,398.84 180b10.61,23.59,91.98
"""

RARITY = {"C":"Common", "U":"Uncommon", "R":"Rare", "D":"Double Rare",
          "A":"ACE SPEC Rare", "I":"Illustration Rare", "T":"Ultra Rare",
          "S":"Special Illustration Rare", "H":"Hyper Rare"}

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "K": ("master",      "Master Ball Reverse",     "master-ball"),
    "B": ("ball",        "Poké Ball Reverse",       "poke-ball"),
    "R": ("rh",          "Reverse Holo",            "reverse"),
    "C": ("cosmos",      "Cosmos Holo",             "cosmos-holo"),
    "S": ("stamped",     "Stamped Promo",           "stamped"),
    "P": ("prize",       "Prize Pack",              "prize-pack"),
    "Q": ("prizecosmos", "Prize Pack Cosmos Holo",  "prize-pack-cosmos-holo"),
    "V": ("prize7",      "Prize Pack Series 7",     "prize-pack-series-7"),
    "J": ("jumbo",       "Jumbo",                   "jumbo"),
    "D": ("holiday",     "Holiday Calendar",        "holiday-calendar"),
    "Y": ("gymstamp",    "Gym Stamp",               "gym-stamp"),
    "L": ("pbl",         "Premier Ball League",     "premier-ball-league"),
    "G": ("pbljudge",    "Premier Ball League Judge","premier-ball-league-judge"),
    "N": ("pokeday",     "Pokémon Day",             "pokemon-day"),
    "M": ("pokeday25",   "Pokémon Day 2025",        "pokemon-day-2025"),
}
ORDER = [v[0] for v in VARIANTS.values()]

_names, _rar = {}, {}
for i, line in enumerate(CHECKLIST.strip().splitlines(), 1):
    nm, r = line.rsplit("|", 1)
    _names[i], _rar[i] = nm, RARITY[r]

_TOK = re.compile(r"^(\d+)([bKBRCSPQVJDYLGNM])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
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

BASE, RH, RH_EST, SPECIAL = [], {}, set(), {}
for num in sorted(_names):
    BASE.append((num, _names[num], _rar[num]) + _px.get((num, "b"), (None, None, None)) + (0,))
for (num, v), px in sorted(_px.items()):
    if v == "b":
        continue
    vid, label, suf = VARIANTS[v]
    SPECIAL.setdefault(num, []).append((vid, label, suf) + px)
for num in SPECIAL:
    SPECIAL[num].sort(key=lambda t: ORDER.index(t[0]))

# PriceCharting files these two promos without the "ex" the base card carries
PCSLUG = {(51, "stamped"): "lucario", (64, "stamped"): "tyranitar"}

assert len(BASE) == 180, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert sum(len(v) for v in SPECIAL.values()) == len(_px) - 180
_count = lambda vid: sum(1 for vs in SPECIAL.values() for t in vs if t[0] == vid)
assert (_count("rh"), _count("ball"), _count("master")) == (100, 100, 67)

SET = {
    "id": "PRE", "name": "Prismatic Evolutions", "series": "Scarlet & Violet",
    "released": "2025-01-17", "total": 180, "baseTotal": 131,
    "code": "PRE", "pcslug": "pokemon-prismatic-evolutions",
    "tcgc": "https://www.tcgcollector.com/sets/11641/prismatic-evolutions",
    "priceDate": "2026-08-19", "accent": "#7c6cf5",
    "logos": [
        "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/sv08pt5.png",
    ],
}
