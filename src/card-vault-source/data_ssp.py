# Scarlet & Violet — Surging Sparks (SV08 / SSP), released 2024-11-08
# 252 cards (191 base + 61 secret). One Reverse Holo pattern, but it does not line up
# with the usual "every non-ex base card" rule: ACE SPECs normally have no reverse and
# here exactly one does (Energy Search Pro #176, a real PriceCharting listing), so the
# reverses route through SPECIAL rather than RH.
#
# Rarities: api.pokemontcg.io/v2/cards?q=set.id:sv8
# Prices:   pricecharting.com/console/pokemon-surging-sparks  (captured 2026-08-19)
#
# PriceCharting also lists a Jumbo printing of #76 with no recorded sale in any grade,
# so it carries no information and is left out.
import re

# one line per card, in number order:  name|rarity code
CHECKLIST = """
Exeggcute|C
Exeggcute|C
Exeggutor|U
Durant ex|D
Scatterbug|C
Spewpa|C
Vivillon|U
Morelull|C
Shiinotic|U
Dhelmise|C
Zarude|R
Capsakid|C
Rellor|C
Rabsca|R
Wo-Chien|U
Vulpix|C
Ninetales|U
Paldean Tauros|U
Ho-Oh|U
Castform Sunny Form|C
Victini|U
Pansear|C
Simisear|C
Larvesta|C
Volcarona|C
Oricorio|C
Sizzlipede|C
Centiskorch|C
Fuecoco|C
Crocalor|C
Skeledirge|R
Charcadet|C
Charcadet|C
Armarouge|U
Ceruledge|U
Ceruledge ex|D
Scovillain ex|D
Gouging Fire|R
Paldean Tauros|U
Mantine|C
Feebas|C
Milotic ex|D
Spheal|C
Sealeo|C
Walrein|U
Shellos|C
Cryogonal|C
Black Kyurem ex|D
Bruxish|U
Quaxly|C
Quaxwell|C
Quaquaval|U
Cetoddle|C
Cetitan|C
Iron Bundle|U
Chien-Pao|R
Pikachu ex|D
Magnemite|C
Magneton|U
Magnezone|U
Rotom|C
Blitzle|C
Zebstrika|C
Stunfisk|C
Tapu Koko|R
Wattrel|C
Kilowattrel|U
Kilowattrel ex|D
Miraidon|U
Togepi|C
Togetic|C
Togekiss|R
Marill|C
Azumarill|U
Smoochum|C
Latias ex|D
Latios|U
Uxie|C
Mesprit|C
Azelf|C
Sigilyph|C
Yamask|C
Cofagrigus|R
Espurr|C
Meowstic|U
Sylveon ex|D
Dedenne|C
Xerneas|U
Oricorio|C
Sandygast|C
Palossand ex|D
Tapu Lele|R
Indeedee|U
Flittle|C
Espathra|U
Flutter Mane|U
Gimmighoul|C
Mankey|C
Primeape|C
Annihilape|U
Paldean Tauros|U
Phanpy|C
Donphan|C
Trapinch|C
Vibrava|C
Flygon ex|D
Gastrodon|R
Drilbur|C
Excadrill|C
Landorus|R
Passimian|U
Clobbopus|C
Grapploct|C
Glimmet|C
Glimmora|C
Koraidon|U
Deino|C
Zweilous|C
Hydreigon ex|D
Shroodle|C
Grafaiai|U
Alolan Diglett|C
Alolan Dugtrio|U
Skarmory|C
Registeel|U
Bronzor|C
Bronzong|C
Klefki|C
Duraludon|C
Archaludon ex|D
Gholdengo|U
Iron Crown|R
Alolan Exeggutor ex|D
Altaria|U
Dialga|R
Palkia|R
Turtonator|U
Applin|C
Flapple|U
Appletun|U
Eternatus|R
Tatsugiri ex|D
Eevee|C
Snorlax|C
Slakoth|C
Vigoroth|C
Slaking ex|D
Swablu|C
Zangoose|C
Kecleon|C
Bouffalant|C
Rufflet|C
Braviary|U
Helioptile|C
Heliolisk|C
Oranguru|C
Tandemaus|C
Maushold|U
Cyclizar ex|D
Flamigo ex|D
Terapagos|R
Amulet of Hope|A
Babiri Berry|U
Brilliant Blender|A
Call Bell|U
Chill Teaser Toy|U
Clemont's Quick Wit|U
Colbur Berry|U
Counter Gain|U
Cyrano|U
Deduction Kit|U
Dragon Elixir|U
Drasna|C
Drayton|U
Dusk Ball|U
Energy Search Pro|A
Gravity Mountain|U
Jasmine's Gaze|U
Lisia's Appeal|U
Lively Stadium|U
Meddling Memo|U
Megaton Blower|A
Miracle Headset|A
Passho Berry|U
Precious Trolley|A
Scramble Switch|A
Surfer|U
Technical Machine: Fluorite|U
Tera Orb|U
Tyme|U
Enriching Energy|A
Exeggcute|I
Vivillon|I
Shiinotic|I
Castform Sunny Form|I
Larvesta|I
Ceruledge|I
Feebas|I
Spheal|I
Bruxish|I
Cetitan|I
Stunfisk|I
Latios|I
Mesprit|I
Phanpy|I
Vibrava|I
Clobbopus|I
Alolan Dugtrio|I
Skarmory|I
Flapple|I
Appletun|I
Slakoth|I
Kecleon|I
Braviary|I
Durant ex|T
Scovillain ex|T
Milotic ex|T
Black Kyurem ex|T
Pikachu ex|T
Latias ex|T
Palossand ex|T
Flygon ex|T
Hydreigon ex|T
Archaludon ex|T
Alolan Exeggutor ex|T
Tatsugiri ex|T
Slaking ex|T
Cyclizar ex|T
Clemont's Quick Wit|T
Cyrano|T
Drasna|T
Drayton|T
Jasmine's Gaze|T
Lisia's Appeal|T
Surfer|T
Durant ex|S
Milotic ex|S
Pikachu ex|S
Latias ex|S
Hydreigon ex|S
Archaludon ex|S
Alolan Exeggutor ex|S
Clemont's Quick Wit|S
Drayton|S
Jasmine's Gaze|S
Lisia's Appeal|S
Pikachu ex|H
Alolan Exeggutor ex|H
Counter Gain|H
Gravity Mountain|H
Night Stretcher|H
Jet Energy|H
"""

# <number><variant char><raw>,<psa9>,<psa10>   blank = no sale on record
PRICES = """
1b.27,10.43,31.17 1R1.40,19.95,35.85 2b.29,10.45,31.21 2R1.49,5.50,36.22 3b.06,10.14,30.38
3R1.31,12.01,35.43 4b1.20,20.00,39.95 5b.18,10.34,30.92 5R1.25,7.01,35.43 6b.09,10.17,30.46
6R.99,13.00,34.13 7b.16,10.25,30.67 7R1.48,12.32,36.26 8b.23,10.45,49.99 8R.69,11.07,32.88
9b.26,10.40,31.08 9R1.50,12.32,36.26 10b.15,10.23,30.63 10R1.31,12.35,36.34 11b.44,19.95,32.21
11R.40,12.00,32.09 12b.04,10.08,30.21 12R1.21,5.00,35.67 13b.04,8.12,39.99 13R.18,10.23,30.63
14b.27,13.76,18.50 14C1.00,11.53, 14H.28,10.23,32.00 14R1.34,8.70,35.60 15b.18,10.31,30.83
15R1.35,12.08,35.59 16b.25,26.99,39.99 16R.50,17.99,67.50 17b1.00,9.38,129.99 17R1.49,21.68,72.99
18b.40,10.62,31.67 18R1.50,14.56,72.00 19b.64,73.10,88.00 19P.23,, 19R1.67,22.25,51.00
20b.33,10.31,44.99 20R1.63,14.99,36.63 21b.40,10.62,31.67 21R1.48,76.50,92.00 22b.08,10.15,30.42
22R.12,14.99,30.96 23b.23,10.28,30.75 23R1.36,12.06,68.50 24b.10,10.25,30.67 24R1.27,12.23,36.01
25b.06,10.20,30.54 25R1.40,27.00,49.99 26b.16,10.17,30.46 26R1.19,12.04,35.51 27b.06,14.95,30.17
27R1.42,12.20,35.93 28b.14,10.23,30.63 28R1.47,12.29,36.17 29b.15,34.00,67.33 29Z13.34,1.25,18.50
29X15.38,62.00,72.40 29R.44,15.47,17.63 30b.10,10.19,30.50 30R.20,10.28,30.75 31b.25,8.75,37.56
31C2.74,, 31R.45,10.70,55.31 32b.24,10.39,31.04 32R1.63,23.75,36.72 33b.25,10.31,30.84
33R1.57,7.51,36.51 34b.29,10.29,30.79 34R1.49,12.20,35.92 35b.31,9.00,31.17 35R.74,11.08,90.00
36P7.26,, 36b1.99,16.94,42.99 37b1.07,11.79,26.42 38b1.00,10.96,32.25 38H.25,5.38,39.99
38R1.50,20.15,39.99 39b.22,6.50,30.92 39R1.81,11.00,37.56 40b.31,10.17,30.46 40R1.50,12.34,36.30
41b.30,10.31,30.83 41R1.45,44.00,53.00 42b1.05,15.97,37.14 43b.30,17.00,31.25 43R.62,16.77,33.42
44b.13,10.22,30.58 44R1.00,9.99,34.84 45b.29,10.54,31.46 45R1.44,12.23,36.01 46b.16,9.99,30.63
46R1.17,11.25,39.08 47b.12,15.00,30.50 47D2.25,20.00,124.95 47R1.34,12.23,36.01 48S1.02,,68.02
48b1.00,15.09,39.27 48J2.49,66.00, 49b.15,10.39,31.04 49R1.45,8.51,35.76 50b.11,19.00,76.56
50X25.00,20.50,87.51 50R1.75,19.56,93.75 51b.22,10.22,30.58 51R.99,7.75,34.99 52b.15,10.37,31.00
52R.51,8.51,32.21 53b.27,10.37,31.00 53R1.12,9.50,29.99 54b.15,10.25,30.67 54R.29,5.50,31.04
55b.18,10.28,30.75 55R.73,14.00,31.38 56b1.00,11.93,53.26 56R1.46,9.00,59.99 57P29.87,48.00,470.00
57b3.63,20.76,101.25 58b.16,10.28,30.75 58R.25,11.50,32.25 59b.40,10.62,31.67 59P.15,,
59R.70,10.62,31.67 60b.19,10.34,30.92 60R1.40,12.08,35.59 61b.09,10.11,37.00 61R.40,10.54,31.46
62b.15,10.31,30.83 62R1.35,12.09,35.64 63b.09,10.15,30.42 63R.33,9.46,30.63 64b.12,10.20,30.54
64R1.20,20.00,34.93 65b.22,28.75,37.75 65P.13,, 65R1.25,11.26,90.00 66b.19,10.28,30.75
66R.99,11.53,34.14 67b.10,14.95,30.63 67R1.49,12.12,35.72 68b.83,19.99,34.07 69b.20,19.95,30.83
69R1.61,40.55,49.00 70b.29,25.00,54.95 70R.75,14.00,54.95 71b.23,10.36,30.96 71R1.72,15.00,37.17
72b.68,10.55,67.00 72R1.39,12.15,35.80 73b.66,11.02,32.75 73R1.49,31.54,125.00 74b.99,11.53,34.13
74P.15,25.00, 74R1.73,, 75b.80,11.53,34.13 75R1.72,32.67,37.18 76Y54.83,, 76P10.38,11.50,
76S4.47,23.99,81.58 76b4.67,16.00,46.64 77b.22,12.00,49.99 77R1.69,21.99,62.97 78b.40,85.00,102.00
78R1.60,20.00,49.99 79b.40,10.62,59.99 79R1.71,15.00,44.99 80b.39,10.62,31.67 80R1.50,4.26,36.26
81b.06,10.12,30.33 81R1.50,12.32,36.26 82b.11,10.09,30.25 82R.19,10.26,30.71 83b.20,9.15,37.72
83R1.47,43.86,53.00 84b.57,20.00,32.92 84R1.59,12.46,49.99 85b.20,10.25,30.67 85R1.53,52.20,63.00
86P26.68,50.00, 86b2.44,17.00,44.00 87b.50,14.95,32.92 87R1.76,7.26,37.09 88b.21,10.31,30.83
88R.34,13.12,39.99 89b.16,10.17,30.46 89R1.33,12.11,35.67 90b.09,10.17,30.46 90R1.11,11.94,35.22
91b.99,13.95,26.98 92b.30,11.38,61.05 92R.32,45.39,54.00 93b.25,10.46,31.25 93R1.44,9.07,36.01
94b.03,10.05,30.13 94R1.15,11.92,35.18 95b.10,10.19,30.50 95R1.38,11.97,35.30 96b.59,76.50,92.00
96R.40,5.50,23.50 97b.19,16.00,30.79 97R.40,10.56,31.00 98b.10,10.25,30.67 98R1.39,11.85,45.84
99b.12,10.14,30.38 99R1.12,22.00,60.00 100b.40,10.62,31.67 100R1.50,12.32,36.26 101b.27,10.43,31.17
101R1.53,12.35,36.34 102b.40,10.93,32.50 102R1.65,12.52,36.81 103b.19,18.99,30.67
103R.25,10.62,31.67 104b.15,10.37,31.00 104R.34,10.53,31.42 105b.25,10.39,31.04 105R.50,10.37,49.99
106b1.66,13.49,37.50 107b.40,13.99,59.50 107C1.55,,80.00 107P.15,, 107R.26,10.62,31.67
108b.05,10.09,30.25 108R.15,10.23,30.63 109b.06,10.12,30.33 109R1.30,7.46,35.43 110b.37,8.00,45.54
110R.99,11.53,130.00 111b.42,10.81,32.17 111R1.59,12.46,36.64 112b.07,10.12,30.33
112R1.13,8.50,35.05 113b.05,10.14,30.38 113R.99,10.00,34.13 114b.08,10.15,30.42 114R.99,12.01,35.43
115b.18,10.32,29.99 115R1.00,11.55,34.18 116b.21,10.33,30.88 116R.30,51.05,61.00 117b.18,10.28,30.75
117R1.49,12.31,36.22 118b.31,10.50,34.99 118R1.48,10.00,36.22 119b1.25,19.64,43.14
120b.10,10.09,30.25 120R1.45,12.56,36.88 121b.26,10.42,39.95 121R1.39,12.15,35.81
122b.15,16.52,36.00 122R.33,11.02,32.50 123b.33,9.03,31.67 123R1.60,35.29,37.38 124b.12,10.17,30.46
124R.18,10.56,31.50 125b.40,10.62,31.67 125R1.84,12.85,37.68 126b.04,10.06,30.17
126R1.31,12.03,35.47 127b.05,10.12,30.33 127R1.17,11.81,34.88 128b.19,10.37,31.00
128R1.22,23.00,35.10 129b.05,15.51,79.99 129R1.29,11.73,81.00 129S1.12,, 130V1.18,,
130S.70,11.88,42.22 130b1.04,12.75,30.05 130J2.42,13.69,152.50 131b.21,76.50,92.00
131R.30,19.99,31.29 132b.18,10.00,44.01 132R1.49,14.20,40.00 133b1.53,16.00,39.99
134b.79,11.24,33.34 134R1.88,11.16,109.99 135b.40,11.00,32.83 135R1.38,17.69,35.76
136b.65,9.65,44.50 136R.40,8.00,37.00 137b.20,10.25,30.67 137R1.76,12.72,37.35 138b.40,10.62,31.67
138R.79,9.00,33.71 139b.40,10.56,31.50 139R1.60,14.99,37.68 140b.40,10.62,31.67 140R.48,11.05,32.84
141b.40,11.00,41.00 141R1.56,9.18,76.50 142b1.47,10.84,34.14 143b.70,23.99,57.77 143W51.80,,
143P9.93,49.70,152.80 143R1.99,19.99,54.03 144b.58,26.00,87.03 144R1.99,23.05,115.00
145b.13,10.17,30.46 145R1.69,10.00,36.72 146b.11,10.29,30.79 146R1.41,29.99,35.63
147b1.04,12.75,30.02 148b.18,10.29,30.79 148R.39,10.77,32.09 149b.04,10.17,30.46
149R1.23,14.99,35.14 150b1.35,12.09,35.64 150R1.47,18.23,122.50 151b.20,10.25,30.67
151R1.17,11.84,34.96 152b.06,10.12,30.33 152R1.33,12.05,35.76 153b.12,10.17,30.46
153R.32,10.51,31.38 154b.25,11.18,31.29 154R1.17,6.50,34.88 155b.05,10.23,30.63 155R1.36,12.28,36.13
156b.10,10.23,30.63 156R1.37,12.03,35.00 157b.68,11.05,32.84 157R1.77,8.51,77.09 158b.69,11.07,32.88
158R1.78,12.76,37.43 159b1.21,13.00,36.09 160b.99,15.00,38.84 161b.31,8.71,45.00 161X.69,7.85,45.00
161P.13,, 161R1.36,12.44,36.13 162b1.01,9.14,25.03 163b.12,10.36,30.96 163R.99,11.53,34.13
164b1.79,13.50,27.11 164P6.83,, 165b.25,10.25,30.67 165R1.22,11.90,35.14 166b.21,15.00,30.88
166R1.25,15.84,35.72 167b.20,10.33,30.88 167R1.14,11.81,34.88 168b.14,10.28,30.75 168R.26,7.01,31.00
169b.25,10.25,30.67 169P.14,, 169R.25,14.95,31.04 170b.40,10.62,31.67 170R1.69,12.51,36.76
171b.10,10.23,30.63 171R.99,6.50,34.13 172b.23,10.33,30.88 172R1.20,11.88,35.05 173b.21,10.39,31.04
173R1.30,11.94,35.22 174b.15,10.28,30.75 174R1.20,11.84,34.97 175b.22,10.34,30.92
175R1.78,16.95,35.88 176b.77,8.71,23.50 176P7.11,, 176R1.93,13.09,38.35 177b.96,11.07,32.88
177A17.49,,59.88 177P.85,, 177R1.58,12.46,36.63 178b.22,10.40,31.09 178R1.40,11.94,35.22
179b.40,10.62,31.67 179R1.50,15.00,36.93 180b.40,10.62,31.67 180R1.31,12.03,35.47
181b.15,10.23,30.63 181R1.24,6.50,35.22 182b1.00,8.59,16.77 183b1.50,9.99,25.25 184b.20,10.29,30.79
184R.85,11.53,34.13 185b2.89,10.00,40.70 185P16.45,, 186b1.27,11.68,25.00 186P8.63,,
187b.15,9.99,30.63 187O110.03,66.00, 187N14.72,8.75, 187R1.30,19.99,36.18 188b.12,10.31,30.83
188R1.19,11.84,34.97 189b.21,10.33,30.88 189G25.47,,41.00 189P.24,, 189R.30,10.45,31.21
190b.12,10.39,31.04 190R1.63,14.99,36.80 191b2.65,9.05,29.86 192b8.36,16.76,105.00
193b5.18,21.65,73.00 194b4.00,17.20,74.00 195b8.63,20.20,95.75 196b2.78,15.59,47.13
197b20.26,27.98,214.14 198b9.82,25.00,135.26 199b9.89,21.39,115.18 200b2.50,18.76,65.11
201b3.00,16.40,45.50 202b2.75,15.28,48.85 203b34.44,43.88,280.00 204b12.21,24.54,146.03
205b8.54,21.14,100.00 206b4.12,16.76,53.39 207b6.35,19.27,122.38 208b9.00,27.99,117.85
209b10.36,22.06,130.41 210b4.58,15.08,50.00 211b7.19,18.40,89.00 212b13.19,31.49,218.00
213b8.89,21.25,100.00 214b4.96,16.91,99.50 215b1.39,13.00,30.01 216b1.15,17.66,52.19
217b2.56,17.34,56.00 218b2.99,15.00,50.00 219b29.99,43.56,182.24 220b5.94,19.32,67.00
221b1.99,15.25,40.50 222b3.07,19.60,60.42 223b4.71,17.80,50.00 224b1.87,16.10,41.79
225b2.63,18.85,47.50 226b2.74,19.14,54.99 227b1.28,14.00,43.31 228b1.98,19.97,48.70
229b1.80,15.21,39.51 230b2.29,13.50,31.90 231b1.18,15.06,44.98 232b1.00,14.50,31.40
233b1.99,17.29,50.17 234b4.03,19.60,54.99 235b1.47,13.00,50.00 236b29.94,34.00,108.65
237b108.75,120.00,301.25 238b288.41,285.00,895.00 239b171.50,172.50,500.00 240b34.21,42.68,120.00
241b11.54,17.64,60.00 242b26.89,33.00,127.00 243b9.19,15.09,56.00 244b7.88,16.38,46.83
245b19.37,22.44,78.94 246b25.27,23.90,99.00 247b85.87,91.59,348.50 248b10.99,21.28,85.00
249b3.46,13.17,38.95 250b10.64,17.99,71.50 251b9.94,15.00,50.44 252b4.90,10.50,34.01
"""

RARITY = {"C":"Common", "U":"Uncommon", "R":"Rare", "D":"Double Rare",
          "A":"ACE SPEC Rare", "I":"Illustration Rare", "T":"Ultra Rare",
          "S":"Special Illustration Rare", "H":"Hyper Rare"}

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "R": ("rh",         "Reverse Holo",           "reverse-holo"),
    "Z": ("horizonsrh", "Horizons Reverse Holo",  "horizons-reverse-holo"),
    "X": ("horizons",   "Horizons Promo",         "horizons"),
    "C": ("cosmos",     "Cosmos Holo",            "cosmos-holo"),
    "H": ("holo",       "Holo",                   "holo"),
    "P": ("prize",      "Prize Pack",             "prize-pack"),
    "V": ("prize7",     "Prize Pack Series 7",    "prize-pack-series-7"),
    "S": ("stamped",    "Stamped Promo",          "stamped"),
    "J": ("jumbo",      "Jumbo",                  "jumbo"),
    "D": ("holiday",    "Holiday Calendar",       "holiday-calendar"),
    "Y": ("gymstamped", "Gym Stamped",            "gym-stamped"),
    "W": ("gymstamp",   "Gym Stamp",              "gym-stamp"),
    "A": ("asiagym",    "Asia Gym",               "asia-gym"),
    "G": ("greatball",  "Great Ball League",      "great-ball-league"),
    "O": ("regstaff",   "Regionals Staff",        "regional-staff"),
    "N": ("regional",   "Regional Championships", "regional"),
}
ORDER = [v[0] for v in VARIANTS.values()]

_names, _rar = {}, {}
for i, line in enumerate(CHECKLIST.strip().splitlines(), 1):
    nm, r = line.rsplit("|", 1)
    _names[i], _rar[i] = nm, RARITY[r]

_TOK = re.compile(r"^(\d+)([bRZXCHPVSJDYWAGON])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
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

assert len(BASE) == 252, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert sum(len(v) for v in SPECIAL.values()) == len(_px) - 252
_count = lambda vid: sum(1 for vs in SPECIAL.values() for t in vs if t[0] == vid)
assert _count("rh") == 166, _count("rh")

SET = {
    "id": "SSP", "name": "Surging Sparks", "series": "Scarlet & Violet",
    "released": "2024-11-08", "total": 252, "baseTotal": 191,
    "code": "SSP", "pcslug": "pokemon-surging-sparks",
    "tcgc": "https://www.tcgcollector.com/sets/11636/surging-sparks",
    "priceDate": "2026-08-19", "accent": "#f7e03d",
    "logos": [
        "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/sv08.png",
    ],
}
