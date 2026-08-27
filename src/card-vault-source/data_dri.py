# Scarlet & Violet — Destined Rivals (SV10 / DRI), released 2025-05-30
# 244 cards (182 base + 62 secret). One standard Reverse Holo pattern covering
# every non-ex base card (165 of them), so RH carries the reverses and SPECIAL
# holds the promos and oddities.
#
# Rarities: api.pokemontcg.io/v2/cards?q=set.id:sv10
# Prices:   pricecharting.com/console/pokemon-destined-rivals  (captured 2026-08-19)
#
# PriceCharting also lists a "Premier Ball League" printing of #81 with no recorded
# sale in any grade, so it carries no information and is left out.
import re

# one line per card, in number order:  name|rarity code
CHECKLIST = """
Ethan's Pinsir|U
Yanma|C
Yanmega ex|D
Pineco|C
Shroomish|C
Breloom|C
Cynthia's Roselia|C
Cynthia's Roserade|R
Mow Rotom|C
Shaymin|U
Dwebble|C
Crustle|R
Fomantis|C
Lurantis|U
Team Rocket's Blipbug|C
Applin|C
Dipplin|C
Hydrapple|R
Team Rocket's Tarountula|C
Team Rocket's Spidops|R
Smoliv|C
Dolliv|C
Arboliva ex|D
Rellor|C
Rabsca ex|D
Teal Mask Ogerpon|U
Growlithe|C
Arcanine|U
Ponyta|C
Rapidash|U
Team Rocket's Moltres ex|D
Ethan's Cyndaquil|C
Ethan's Quilava|C
Ethan's Typhlosion|R
Ethan's Slugma|C
Ethan's Magcargo|R
Team Rocket's Houndour|C
Team Rocket's Houndoom|U
Ethan's Ho-Oh ex|D
Torchic|C
Combusken|C
Blaziken|R
Heat Rotom|C
Hearthflame Mask Ogerpon|U
Misty's Psyduck|U
Misty's Staryu|C
Misty's Starmie|U
Misty's Magikarp|C
Misty's Gyarados|R
Misty's Lapras|C
Team Rocket's Articuno|R
Cynthia's Feebas|C
Cynthia's Milotic|U
Clamperl|C
Huntail|U
Gorebyss|R
Buizel|C
Floatzel|U
Snover|C
Abomasnow|U
Wash Rotom|C
Arrokuda|C
Barraskewda|U
Cetoddle|C
Cetitan ex|D
Dondozo ex|D
Wellspring Mask Ogerpon|U
Electabuzz|C
Electivire ex|D
Team Rocket's Zapdos|R
Ethan's Pichu|C
Team Rocket's Mareep|C
Team Rocket's Flaaffy|C
Team Rocket's Ampharos|U
Electrike|C
Manectric|U
Rotom|C
Zeraora|R
Team Rocket's Drowzee|C
Team Rocket's Hypno|U
Team Rocket's Mewtwo ex|D
Team Rocket's Wobbuffet|R
Steven's Baltoy|C
Steven's Claydol|U
Team Rocket's Chingling|C
Steven's Carbink|C
Team Rocket's Mimikyu|U
Team Rocket's Dottler|C
Team Rocket's Orbeetle|U
Mankey|C
Primeape|C
Annihilape|R
Ethan's Sudowoodo|C
Team Rocket's Larvitar|C
Team Rocket's Pupitar|C
Team Rocket's Tyranitar|R
Nosepass|C
Probopass|U
Meditite|C
Medicham|U
Regirock ex|D
Cynthia's Gible|C
Cynthia's Gabite|C
Cynthia's Garchomp ex|D
Hippopotas|C
Hippowdon|U
Mudbray|C
Mudsdale|U
Arven's Toedscool|C
Arven's Toedscruel|U
Cornerstone Mask Ogerpon|U
Team Rocket's Ekans|C
Team Rocket's Arbok|U
Team Rocket's Nidoran♀|C
Team Rocket's Nidorina|C
Team Rocket's Nidoqueen|U
Team Rocket's Nidoran♂|C
Team Rocket's Nidorino|C
Team Rocket's Nidoking ex|D
Team Rocket's Zubat|C
Team Rocket's Golbat|U
Team Rocket's Crobat ex|D
Team Rocket's Grimer|C
Team Rocket's Muk|U
Team Rocket's Koffing|C
Team Rocket's Weezing|U
Team Rocket's Murkrow|U
Team Rocket's Sneasel|R
Cynthia's Spiritomb|U
Marnie's Purrloin|C
Marnie's Liepard|U
Marnie's Scraggy|C
Marnie's Scrafty|U
Marnie's Impidimp|C
Marnie's Morgrem|U
Marnie's Grimmsnarl ex|D
Marnie's Morpeko|C
Arven's Maschiff|C
Arven's Mabosstiff ex|D
Forretress|U
Skarmory|C
Steven's Skarmory|C
Steven's Beldum|C
Steven's Metang|U
Steven's Metagross ex|D
Zamazenta|R
Team Rocket's Rattata|C
Team Rocket's Raticate|C
Team Rocket's Meowth|C
Team Rocket's Persian ex|D
Kangaskhan|C
Tauros|C
Team Rocket's Porygon|C
Team Rocket's Porygon2|C
Team Rocket's Porygon-Z|U
Taillow|C
Swellow|C
Arven's Skwovet|C
Arven's Greedent|R
Squawkabilly|C
Arven's Sandwich|U
Cynthia's Power Weight|U
Emcee's Hype|C
Energy Recycler|U
Ethan's Adventure|U
Granite Cave|U
Judge|U
Sacred Ash|U
Spikemuth Gym|U
Team Rocket's Archer|U
Team Rocket's Ariana|U
Team Rocket's Bother-Bot|U
Team Rocket's Factory|U
Team Rocket's Giovanni|U
Team Rocket's Great Ball|U
Team Rocket's Petrel|U
Team Rocket's Proton|U
Team Rocket's Transceiver|U
Team Rocket's Venture Bomb|U
Team Rocket's Watchtower|U
TM Machine|U
Team Rocket's Energy|U
Yanma|I
Cynthia's Roserade|I
Shaymin|I
Crustle|I
Team Rocket's Spidops|I
Hydrapple|I
Rapidash|I
Ethan's Typhlosion|I
Team Rocket's Houndoom|I
Blaziken|I
Misty's Psyduck|I
Misty's Lapras|I
Clamperl|I
Electrike|I
Rotom|I
Team Rocket's Orbeetle|I
Team Rocket's Weezing|I
Team Rocket's Murkrow|I
Zamazenta|I
Team Rocket's Raticate|I
Team Rocket's Meowth|I
Kangaskhan|I
Arven's Greedent|I
Yanmega ex|T
Arboliva ex|T
Team Rocket's Moltres ex|T
Ethan's Ho-Oh ex|T
Cetitan ex|T
Dondozo ex|T
Electivire ex|T
Team Rocket's Mewtwo ex|T
Regirock ex|T
Cynthia's Garchomp ex|T
Team Rocket's Nidoking ex|T
Team Rocket's Crobat ex|T
Arven's Mabosstiff ex|T
Team Rocket's Persian ex|T
Emcee's Hype|T
Ethan's Adventure|T
Judge|T
Team Rocket's Archer|T
Team Rocket's Ariana|T
Team Rocket's Giovanni|T
Team Rocket's Petrel|T
Team Rocket's Proton|T
Yanmega ex|S
Team Rocket's Moltres ex|S
Ethan's Ho-Oh ex|S
Team Rocket's Mewtwo ex|S
Cynthia's Garchomp ex|S
Team Rocket's Nidoking ex|S
Team Rocket's Crobat ex|S
Arven's Mabosstiff ex|S
Ethan's Adventure|S
Team Rocket's Ariana|S
Team Rocket's Giovanni|S
Ethan's Ho-Oh ex|H
Team Rocket's Mewtwo ex|H
Cynthia's Garchomp ex|H
Team Rocket's Crobat ex|H
Jamming Tower|H
Levincia|H
"""

# <number><variant char><raw>,<psa9>,<psa10>   blank = no sale on record
PRICES = """
1b.22,10.26,30.79 1R.65,11.02,33.07 2b.14,10.22,30.66 2R.67,8.43,220.00 3P2.10,, 3b1.00,15.00,39.99
4b.15,10.18,30.53 4R.32,11.27,31.14 5b.40,10.58,31.75 5R.42,10.58,31.75 6b.18,10.48,31.45
6R.25,10.36,31.10 7b.43,10.50,31.23 7R1.33,11.04,33.11 8b.99,11.23,33.68 8Q.20,, 8P.16,10.31,30.92
8R.99,10.64,31.93 9b.28,10.20,30.61 9R.40,10.58,31.75 10b.99,11.82,14.00 10P.24,,40.00
10R1.49,12.55,35.00 11b.40,10.58,31.75 11R.99,19.95,33.46 12b.40,13.50,31.75 12P.82,,
12R.40,10.58,31.75 13b.40,10.58,74.99 13R.40,10.83,32.50 14b.71,10.22,59.95 14R.99,10.73,32.19
15b.20,10.29,30.88 15R.35,10.34,31.01 16b.40,10.73,59.99 16R1.32,11.44,34.34 17b.52,10.22,30.66
17R.70,10.58,31.75 18b.99,11.44,34.34 18C4.25,, 18R.64,11.14,33.42 19b.40,10.58,49.99
19R.40,25.00,31.75 20b.24,12.00,149.99 20H.40,10.80,32.41 20Q.20,, 20P.25,, 20R.99,10.96,32.89
21b1.27,11.44,59.95 21R1.38,14.89,33.42 22b.40,10.58,31.75 22R.59,10.86,24.50 23b1.50,17.00,29.58
24b.23,10.23,30.70 24R.28,10.41,31.23 25b.99,16.85,25.75 26b.40,10.58,31.75 26R.65,11.18,33.55
27b.99,15.50,31.31 27R1.25,11.94,35.83 28b.74,10.41,31.23 28R1.55,13.40,75.00 29b.65,19.95,59.99
29R.68,10.99,32.98 30b.50,15.55,59.95 30R1.19,20.00,69.99 31b1.21,20.47,47.62 31S2.23,14.26,106.80
32b.41,15.95,75.00 32R1.00,16.08,152.50 33b.63,19.86,144.97 33P.19,, 33R.99,15.48,50.43
34b.95,22.24,175.00 34H.90,13.00,49.00 34P.24,, 34R1.13,11.50,111.00 34T118.18,117.50,422.53
34S11.96,123.88,385.00 35b.21,10.22,30.66 35R.73,29.95,32.32 36b.33,9.58,41.00 36C.35,, 36P.18,,
36R.40,10.73,32.19 37b.25,10.22,30.66 37R.50,11.08,33.24 38b.60,11.63,67.12 38R.99,11.59,34.78
39P6.43,, 39b1.33,17.97,36.37 40b.74,19.95,33.55 40R.99,11.17,33.50 41b.22,10.34,31.01
41R.84,19.99,59.95 42b1.06,18.02,50.00 42C9.87,54.43, 42R.99,10.50,33.99 43b.40,10.32,30.96
43R.47,13.00,79.99 44b.17,10.32,30.96 44R.43,10.74,32.24 45b.93,33.07,216.23 45R1.35,21.46,271.40
46b.32,19.49,149.99 46R.50,10.73,120.00 47b.51,16.00,95.53 47R1.43,11.25,33.77 48b1.26,25.88,87.69
48R.94,28.99,71.86 49b1.78,28.00,222.03 49H1.04,24.52,129.64 49R.99,23.81,250.00
49T157.49,161.40,532.50 49S16.38,65.00,389.22 50b.50,12.00,44.86 50R1.29,20.25,57.23
51b1.79,20.00,108.62 51C3.19,, 51H1.35,17.85,95.13 51R.99,11.50,74.99 51S31.73,32.91,95.77
52b.49,10.58,31.75 52R.84,11.15,33.46 53b.22,12.00,94.95 53R1.14,20.00,34.34 54b.23,10.29,30.88
54R.50,10.58,31.75 55b.27,10.36,31.10 55R.40,10.58,74.99 56b.39,7.50,31.75 56R.50,10.99,32.98
57b.30,26.99,67.50 57R.92,17.50,31.66 58b.55,10.58,59.95 58R.60,11.75,35.26 59b.25,15.18,31.31
59R1.76,12.57,37.71 60b.26,16.00,30.88 60R.44,11.02,33.07 61b.21,10.41,31.23 61R.42,19.99,54.99
62b.30,10.31,30.92 62R.20,10.58,31.75 63b.18,10.26,30.79 63R.61,10.69,32.06 64b.08,10.03,30.09
64R.21,10.29,30.88 65b1.45,14.40,25.23 66b1.49,15.00,34.95 67b.40,10.42,31.27 67R.70,11.02,33.07
68b.16,19.00,30.79 68R.29,10.00,32.19 69b1.02,17.73,41.50 70b1.50,19.23,108.48 70C1.40,,
70G46.97,59.18,138.19 70M19.31,27.98,104.03 70R1.35,26.79,89.99 70S69.88,44.00,120.00
71b.55,19.50,77.99 71R1.00,20.00,68.32 72b.50,10.25,30.74 72R1.32,11.20,33.59 73b.25,10.22,52.56
73R.89,3.40,35.00 74b.22,17.50,59.95 74R1.08,11.20,33.59 75b.18,10.31,30.92 75R.40,12.00,31.75
76b.20,10.16,30.48 76R.65,10.95,32.85 77b.10,10.23,30.70 77R.70,10.58,31.75 78b.66,14.00,70.00
78Q3.50,, 78R.74,11.08,33.24 79b.22,9.36,31.10 79R.50,10.87,33.64 80b.37,11.74,91.25
80R.73,11.06,33.20 81b2.13,20.27,76.00 81P29.28,, 82b1.33,17.00,63.00 82R.99,11.50,106.67 83b.19,10.41,31.23
83R.32,10.48,31.45 84b.27,10.17,30.53 84R.70,10.66,31.97 85b.19,10.26,30.79 85R.90,10.99,32.98
86b.15,10.04,40.00 86R.40,10.31,30.92 87b.99,35.92,70.00 87F139.99,117.82,341.48
87E16.80,24.99,293.47 87R1.48,19.94,221.30 88b.10,10.15,30.44 88R.40,10.58,31.75 89b.29,10.35,31.05
89R.40,10.58,31.75 90b.40,9.01,32.98 90R.85,13.00,32.98 91b.11,10.22,30.66 91R.64,16.50,32.41
92b.75,15.00,49.99 92R.40,14.99,99.99 93b.25,10.38,59.95 93R.50,65.25,78.00 94b.40,28.40,199.03
94R.70,10.67,105.99 95b.25,10.50,97.50 95R.73,12.40,33.07 96b.80,27.00,206.50 96C1.63,70.00,
96H1.05,20.00,184.99 96K34.00,39.31,143.36 96R1.71,29.98,277.89 96T133.11,127.51,422.00
96S13.48,112.86,396.98 97b.10,9.75,44.99 97R.66,10.01,32.32 98b.31,10.58,59.99 98R.50,10.86,32.58
99b.22,10.32,30.96 99R.24,10.58,31.75 100b.31,19.95,31.10 100R.70,10.80,32.41 101b1.35,10.91,22.50
102b.41,19.99,71.00 102C1.73,4.99,74.10 102R.99,11.44,34.34 103b.34,14.75,79.99 103C1.68,7.18,87.34
103P.42,, 103R1.19,13.49,47.33 104P20.65,23.01, 104b1.76,10.95,39.99 105b.15,10.19,30.57
105R.40,10.58,31.75 106b.31,10.23,30.70 106R.79,12.50,31.75 107b.15,10.16,30.48 107R.65,10.41,31.23
108b.21,10.36,31.10 108R.40,13.50,31.75 109b.06,10.15,30.44 109R.19,10.29,30.88 110b.20,10.12,30.35
110R.84,10.58,31.75 111b.51,10.38,31.14 111R.40,10.66,31.97 112b.23,10.36,31.10 112R.75,14.50,32.15
113b.33,9.00,54.99 113R.98,11.09,33.29 114b.40,10.58,31.75 114R.69,10.58,170.38 115b.25,10.36,31.10
115R.94,12.99,39.00 116b.50,10.73,32.19 116R.88,10.73,32.19 117b1.62,12.40,37.24
117R1.69,12.46,37.41 118b.40,15.00,31.75 118R.97,11.44,34.34 119P6.24,, 119b1.48,15.99,38.03
120b.18,13.23,30.92 120R.40,11.02,33.07 121b.39,9.20,31.75 121R.89,11.36,34.08 122P7.14,,
122b1.08,19.12,29.51 123b.17,10.25,99.99 123R.40,10.58,31.75 124b.38,12.97,31.75
124R1.06,11.11,33.33 125b.23,6.77,70.00 125R.40,10.64,77.00 126b.63,12.77,74.99 126R.99,11.63,34.91
127b.69,7.10,70.00 127R.92,7.13,34.65 128b.99,15.00,53.50 128R.52,11.18,33.55 129b.40,10.51,31.53
129R.60,10.87,32.63 130b.20,20.00,59.95 130R.50,19.99,32.19 131b.14,24.98,44.95 131R.40,29.95,31.75
132b.37,10.36,42.95 132R.72,10.61,31.84 133b.32,10.42,59.95 133R.95,11.39,34.16 134b.40,10.58,31.75
134R.70,11.02,33.07 135b.36,10.32,44.95 135R.99,10.98,32.93 136b1.50,13.00,34.50 137b.94,11.02,46.95
137R1.77,12.75,47.93 138b.41,15.08,31.10 138R.65,10.58,99.00 139P3.23,, 139b1.40,14.00,47.00
140b.24,10.36,31.10 140R.49,10.82,32.45 141b.27,10.15,30.44 141R.40,10.00,31.75 142b.24,10.36,31.10
142R.25,19.99,31.23 143b.33,10.34,31.01 143R.34,10.50,31.49 144b.32,10.47,31.40 144R.40,10.58,31.75
145b1.89,15.58,39.99 146b.57,11.25,50.00 146R.99,11.28,34.16 147b.15,10.22,30.66
147R.40,10.00,149.99 148b.22,12.00,30.66 148R.50,5.50,31.40 149b.49,20.53,89.00 149C1.33,28.74,99.00
149R.92,16.00,75.46 150b1.49,15.50,51.14 151b.85,9.00,30.88 151R.55,29.97,33.72 152b.55,10.80,32.41
152R.62,10.36,31.10 153b.40,26.39,57.75 153R.73,66.00,79.00 154b.46,10.76,32.28 154R.88,10.66,31.97
155b.40,10.58,31.75 155R.98,51.00,61.00 156b.60,10.88,32.63 156R1.17,11.94,35.82 157b.22,10.26,30.79
157R.67,10.73,32.19 158b.20,10.19,24.99 158R.25,10.73,32.19 159b.40,7.00,31.14 159C2.00,,
159R.45,10.66,31.97 160b.19,10.16,30.48 160R.21,11.90,75.00 161b.10,10.15,30.44 161R.15,10.22,30.66
162b.40,10.55,31.66 162P.17,, 162R.72,10.58,31.75 163b.10,10.15,30.44 163R.18,10.31,30.92
164b.99,11.81,35.43 164R.99,11.36,34.07 165b.33,10.55,31.67 165Q.11,,170.00 165P.13,10.19,30.57
165R.71,11.72,33.15 166b.11,10.09,30.26 166R.16,10.36,31.10 167b.16,10.28,30.83 167W277.02,,
167R.50,10.58,31.75 168b.71,10.89,32.67 168R.99,11.17,33.50 169b.34,10.23,30.70 169R.70,10.73,32.19
170b.40,10.55,31.66 170P.22,, 170R.60,11.40,34.20 171b.44,10.64,31.93 171P.25,10.32,30.96
171R.79,11.06,33.20 172b.26,10.35,59.95 172R.40,10.90,32.72 173b.85,11.24,33.72 173X1.18,11.71,35.13
173R.99,11.44,34.34 174b.61,111.00,133.00 174C.77,,54.97 174P.19,10.26,30.79 174O700.64,,
174N39.66,, 174R.74,9.36,32.72 175b.37,7.50,31.36 175R.90,16.00,31.75 176b.94,11.49,34.47 176P.65,,
176R1.22,11.78,35.35 177b.56,10.95,32.85 177P.24,10.32,30.96 177R.79,10.63,31.88
178b1.21,11.84,35.52 178P.32,10.50,31.49 178R1.94,12.83,38.51 179b.25,15.99,20.75 179R.50,6.50,32.63
180b1.00,11.50,59.95 180R1.17,11.27,33.81 181b.18,10.51,31.53 181R.40,10.48,31.45
182b.50,19.95,31.75 182P.30,, 182R1.62,12.36,37.09 183b3.88,16.90,77.50 184b13.89,22.40,148.75
185b11.44,20.26,125.00 186b2.94,16.45,75.32 187b6.18,22.00,80.50 188b4.50,20.00,71.35
189b9.40,23.40,152.50 190b26.99,39.00,324.32 191b15.99,23.35,165.00 192b10.56,20.75,163.75
193b60.93,75.00,400.00 194b34.55,45.00,324.40 195b4.97,19.83,97.00 196b3.89,19.01,68.46
197b3.80,19.50,82.87 198b4.00,17.74,97.85 199b8.79,23.75,125.05 200b8.88,20.88,114.98
201b4.99,19.45,109.20 202b6.77,20.00,111.00 203b27.28,39.60,250.00 204b11.55,24.50,160.64
205b4.03,17.16,50.00 206b1.59,20.29,34.96 207b2.50,18.60,33.00 208b6.46,24.50,74.01
208S11.01,27.47,99.00 209b5.00,20.00,65.05 210b1.75,13.72,36.16 211b1.76,16.24,38.95
212b2.33,18.52,50.00 213b20.70,39.66,124.74 214b1.99,18.43,43.87 215b4.99,20.30,65.71
216b4.13,21.00,60.00 217b3.50,20.30,49.99 218b1.82,17.77,40.97 219b4.45,21.65,52.50
220b2.80,18.00,42.00 221b3.72,16.45,48.50 222b2.61,14.25,31.95 223b3.45,14.00,46.62
224b4.51,18.63,40.76 225b6.23,19.13,54.77 226b10.00,13.05,36.41 227b3.99,13.65,43.37
228b19.95,27.51,70.76 229b88.44,92.23,307.98 229S65.14,80.00,367.50 230b152.50,160.25,385.00
231b518.40,517.00,1111.78 232b222.74,227.99,485.68 233b100.00,107.50,287.99 234b60.00,75.00,155.88
235b25.46,28.00,88.00 236b36.00,44.49,152.25 237b20.99,26.35,60.00 238b27.34,35.00,95.04
239b23.95,33.41,86.06 240b58.00,66.33,189.00 241b29.99,30.94,90.00 242b16.49,24.25,64.99
243b8.94,19.00,53.66 244b8.50,18.58,41.01
"""

RARITY = {"C":"Common", "U":"Uncommon", "R":"Rare", "D":"Double Rare",
          "I":"Illustration Rare", "T":"Ultra Rare",
          "S":"Special Illustration Rare", "H":"Hyper Rare"}

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "R": ("rh",          "Reverse Holo",           "reverse-holo"),
    "P": ("prize",       "Prize Pack",             "prize-pack"),
    "Q": ("prizecosmos", "Prize Pack Cosmos Holo", "prize-pack-cosmos-holo"),
    "X": ("prizecosmo",  "Prize Pack Cosmo Holo",  "prize-pack-cosmo-holo"),
    "C": ("cosmos",      "Cosmos Holo",            "cosmos-holo"),
    "H": ("holo",        "Holo",                   "holo"),
    "S": ("stamped",     "Stamped Promo",          "stamped"),
    "T": ("staff",       "Staff Promo",            "staff"),
    "G": ("ebgames",     "EB Games",               "eb-games"),
    "M": ("gamestop",    "GameStop Promo",         "gamestop"),
    "F": ("prestaff",    "Prerelease Staff",       "prerelease-staff"),
    "E": ("prerelease",  "Prerelease",             "prerelease"),
    "K": ("pokecenter",  "Pokemon Center",         "pokemon-center"),
    "W": ("professor",   "Professor Program",      "professor-program"),
    "O": ("regstaff",    "Regionals Staff",        "regional-staff"),
    "N": ("regional",    "Regional Championships", "regional"),
}
ORDER = ["rh"] + [v[0] for v in VARIANTS.values() if v[0] != "rh"]

_names, _rar = {}, {}
for i, line in enumerate(CHECKLIST.strip().splitlines(), 1):
    nm, r = line.rsplit("|", 1)
    _names[i], _rar[i] = nm, RARITY[r]

_TOK = re.compile(r"^(\d+)([bRPQXCHSTGMFEKWON])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
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
    if v == "R":
        RH[num] = px
        continue
    vid, label, suf = VARIANTS[v]
    SPECIAL.setdefault(num, []).append((vid, label, suf) + px)
for num in SPECIAL:
    SPECIAL[num].sort(key=lambda t: ORDER.index(t[0]))

assert len(BASE) == 244, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert len(RH) == 165, len(RH)

SET = {
    "id": "DRI", "name": "Destined Rivals", "series": "Scarlet & Violet",
    "released": "2025-05-30", "total": 244, "baseTotal": 182,
    "code": "DRI", "pcslug": "pokemon-destined-rivals",
    "tcgc": "https://www.tcgcollector.com/sets/11650/destined-rivals",
    "priceDate": "2026-08-19", "accent": "#d9a520",
    "logos": [
        "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/sv10.png",
    ],
}
