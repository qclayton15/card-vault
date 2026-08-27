# Mega Evolution — Ascended Heroes (ME2.5 / ASC), released 2026-01-30
# 295 cards (217 base + 78 secret). Unlike the other sets, most base cards have TWO
# reverse-holo patterns — Poké Ball and Energy — while Trainers and Team Rocket's
# cards use a single Reverse Holo. All of it comes through SPECIAL rather than RH.
#
# Checklist: tcgwatchtower.com/pokemon/sets/mega-evolution/ascended-heroes/cards
# Prices:    pricecharting.com/console/pokemon-ascended-heroes  (captured 2026-08-19)
import re

CHECKLIST = """
1|Erika's Oddish|Common
2|Erika's Gloom|Uncommon
3|Erika's Vileplume ex|Double Rare
4|Erika's Bellsprout|Common
5|Erika's Weepinbell|Uncommon
6|Erika's Victreebel|Rare
7|Erika's Tangela|Common
8|Chikorita|Common
9|Bayleef|Uncommon
10|Mega Meganium ex|Double Rare
11|Wurmple|Common
12|Silcoon|Common
13|Beautifly|Uncommon
14|Cascoon|Common
15|Dustox|Uncommon
16|Budew|Common
17|Grubbin|Common
18|Team Rocket's Tarountula|Common
19|Team Rocket's Spidops|Rare
20|Charmander|Common
21|Charmeleon|Uncommon
22|Mega Charizard Y ex|Double Rare
23|Ethan's Slugma|Common
24|Ethan's Magcargo|Rare
25|Entei|Rare
26|Ethan's Ho-Oh ex|Double Rare
27|Numel|Common
28|Camerupt|Uncommon
29|Tepig|Common
30|Pignite|Uncommon
31|Mega Emboar ex|Double Rare
32|N's Darumaka|Common
33|N's Darmanitan|Uncommon
34|Salandit|Common
35|Salazzle|Uncommon
36|Scorbunny|Common
37|Raboot|Common
38|Cinderace ex|Double Rare
39|Psyduck|Common
40|Golduck|Uncommon
41|Totodile|Common
42|Croconaw|Uncommon
43|Mega Feraligatr ex|Double Rare
44|Sneasel|Common
45|Weavile|Uncommon
46|Snorunt|Common
47|Mega Froslass ex|Double Rare
48|Regice ex|Double Rare
49|N's Vanillite|Common
50|N's Vanillish|Common
51|N's Vanilluxe|Uncommon
52|Snom|Common
53|Frosmoth|Uncommon
54|Glastrier|Uncommon
55|Pikachu|Common
56|Raichu|Uncommon
57|Pikachu ex|Double Rare
58|Voltorb ex|Double Rare
59|Tynamo|Common
60|Eelektrik|Uncommon
61|Mega Eelektross ex|Double Rare
62|Stunfisk|Common
63|Helioptile|Common
64|Heliolisk|Uncommon
65|Charjabug|Common
66|Vikavolt|Uncommon
67|Tapu Koko|Rare
68|Hop's Pincurchin ex|Double Rare
69|Iono's Tadbulb|Common
70|Iono's Bellibolt ex|Double Rare
71|Iono's Wattrel|Common
72|Iono's Kilowattrel|Rare
73|Miraidon ex|Double Rare
74|Clefairy|Common
75|Clefable|Uncommon
76|Lillie's Clefairy ex|Double Rare
77|Team Rocket's Exeggcute|Common
78|Team Rocket's Exeggutor|Rare
79|Team Rocket's Mewtwo ex|Double Rare
80|Togepi|Common
81|Togetic|Common
82|Togekiss|Rare
83|Marill|Common
84|Azumarill ex|Double Rare
85|Misdreavus|Common
86|Mismagius|Rare
87|Ralts|Common
88|Kirlia|Common
89|Mega Gardevoir ex|Double Rare
90|Shuppet|Common
91|Banette|Uncommon
92|Rotom|Common
93|Swirlix|Common
94|Slurpuff|Uncommon
95|Hop's Phantump|Common
96|Hop's Trevenant|Rare
97|Team Rocket's Mimikyu|Uncommon
98|Spectrier|Rare
99|Munkidori|Rare
100|Team Rocket's Diglett|Common
101|Team Rocket's Dugtrio|Uncommon
102|Hitmontop|Common
103|Meditite|Common
104|Medicham|Common
105|Lunatone|Rare
106|Solrock|Uncommon
107|Regirock ex|Double Rare
108|Groudon|Rare
109|Cynthia's Gible|Common
110|Cynthia's Gabite|Uncommon
111|Cynthia's Garchomp ex|Double Rare
112|Riolu|Common
113|Mega Lucario ex|Double Rare
114|Stunfisk ex|Double Rare
115|Pancham|Common
116|Mega Hawlucha ex|Double Rare
117|Carbink|Uncommon
118|Rolycoly|Common
119|Carkol|Common
120|Coalossal|Rare
121|Koraidon ex|Double Rare
122|Okidogi|Rare
123|Gastly|Common
124|Haunter|Uncommon
125|Mega Gengar ex|Double Rare
126|Team Rocket's Murkrow|Common
127|Team Rocket's Honchkrow|Rare
128|Poochyena|Common
129|Mightyena|Uncommon
130|Galarian Zigzagoon|Common
131|Galarian Linoone|Common
132|Galarian Obstagoon|Uncommon
133|Cynthia's Spiritomb|Uncommon
134|Scraggy|Common
135|Mega Scrafty ex|Double Rare
136|N's Zorua|Common
137|N's Zoroark ex|Double Rare
138|Vullaby|Common
139|Mandibuzz ex|Double Rare
140|Pangoro|Uncommon
141|Hoopa|Rare
142|Fezandipiti ex|Double Rare
143|Pecharunt|Rare
144|Mawile|Uncommon
145|Registeel ex|Double Rare
146|Pawniard|Common
147|Bisharp|Common
148|Kingambit|Rare
149|Togedemaru ex|Double Rare
150|Dratini|Common
151|Dragonair|Uncommon
152|Mega Dragonite ex|Double Rare
153|Rayquaza|Rare
154|N's Reshiram|Rare
155|N's Zekrom|Rare
156|Noibat|Common
157|Noivern|Uncommon
158|Dreepy|Common
159|Drakloak|Common
160|Dragapult ex|Double Rare
161|Team Rocket's Meowth|Common
162|Team Rocket's Kangaskhan ex|Double Rare
163|Larry's Dunsparce|Common
164|Larry's Dudunsparce ex|Double Rare
165|Skitty|Common
166|Delcatty|Uncommon
167|Zangoose ex|Double Rare
168|Larry's Starly|Common
169|Larry's Staravia|Uncommon
170|Larry's Staraptor|Rare
171|Fan Rotom|Common
172|Mega Audino ex|Double Rare
173|Larry's Rufflet|Common
174|Larry's Braviary|Uncommon
175|Larry's Komala|Common
176|Drampa|Uncommon
177|Hop's Cramorant|Uncommon
178|Terapagos|Rare
179|Terapagos ex|Double Rare
180|Acerola's Mischief|Uncommon
181|Air Balloon|Uncommon
182|Anthea & Concordia|Uncommon
183|Boss's Orders|Uncommon
184|Buddy-Buddy Poffin|Common
185|Canari|Uncommon
186|Counter Gain|Common
187|Fighting Gong|Uncommon
188|Forest of Vitality|Uncommon
189|Glass Trumpet|Common
190|Iris's Fighting Spirit|Uncommon
191|Light Ball|Uncommon
192|Lillie's Determination|Uncommon
193|Mega Signal|Common
194|Mystery Garden|Uncommon
195|N's PP Up|Uncommon
196|Night Stretcher|Common
197|Nighttime Mine|Uncommon
198|Poké Pad|Common
199|Premium Power Pro|Uncommon
200|Surfer|Common
201|Team Rocket's Archer|Uncommon
202|Team Rocket's Ariana|Uncommon
203|Team Rocket's Factory|Uncommon
204|Team Rocket's Giovanni|Uncommon
205|Team Rocket's Great Ball|Uncommon
206|Team Rocket's Hypnotizer|Uncommon
207|Team Rocket's Petrel|Uncommon
208|Team Rocket's Proton|Uncommon
209|Team Rocket's Transceiver|Uncommon
210|Team Rocket's Watchtower|Uncommon
211|Thick Scale|Uncommon
212|Tool Scrapper|Common
213|Ultra Ball|Common
214|Urbain|Uncommon
215|Waitress|Common
216|Prism Energy|Uncommon
217|Team Rocket's Energy|Uncommon
218|Erika's Tangela|Illustration Rare
219|Beautifly|Illustration Rare
220|Dustox|Illustration Rare
221|Budew|Illustration Rare
222|Ethan's Magcargo|Illustration Rare
223|Numel|Illustration Rare
224|Salazzle|Illustration Rare
225|Scorbunny|Illustration Rare
226|Psyduck|Illustration Rare
227|Snorunt|Illustration Rare
228|Weavile|Illustration Rare
229|Heliolisk|Illustration Rare
230|Vikavolt|Illustration Rare
231|Iono's Wattrel|Illustration Rare
232|Marill|Illustration Rare
233|Misdreavus|Illustration Rare
234|Banette|Illustration Rare
235|Togekiss|Illustration Rare
236|Slurpuff|Illustration Rare
237|Hop's Trevenant|Illustration Rare
238|Team Rocket's Mimikyu|Illustration Rare
239|Team Rocket's Dugtrio|Illustration Rare
240|Hitmontop|Illustration Rare
241|Medicham|Illustration Rare
242|Carbink|Illustration Rare
243|Mightyena|Illustration Rare
244|Cynthia's Spiritomb|Illustration Rare
245|Galarian Obstagoon|Illustration Rare
246|Mawile|Illustration Rare
247|Dreepy|Illustration Rare
248|Drakloak|Illustration Rare
249|Larry's Staraptor|Illustration Rare
250|Fan Rotom|Illustration Rare
251|Sprigatito ex|Ultra Rare
252|Stunfisk ex|Ultra Rare
253|Mega Audino ex|Ultra Rare
254|Anthea & Concordia|Ultra Rare
255|Black Belt's Training|Ultra Rare
256|Boss's Orders|Ultra Rare
257|Canari|Ultra Rare
258|Cheren|Ultra Rare
259|Counter Gain|Ultra Rare
260|Glass Trumpet|Ultra Rare
261|Jamming Tower|Ultra Rare
262|N's PP Up|Ultra Rare
263|Team Rocket's Transceiver|Ultra Rare
264|Ultra Ball|Ultra Rare
265|Mega Froslass ex|Ultra Rare
266|Mega Eelektross ex|Ultra Rare
267|Mega Diancie ex|Ultra Rare
268|Mega Hawlucha ex|Ultra Rare
269|Mega Gengar ex|Ultra Rare
270|Mega Scrafty ex|Ultra Rare
271|Mega Dragonite ex|Ultra Rare
272|Mega Meganium ex|Special Illustration Rare
273|Mega Emboar ex|Special Illustration Rare
274|Mega Feraligatr ex|Special Illustration Rare
275|Mega Froslass ex|Special Illustration Rare
276|Pikachu ex|Special Illustration Rare
277|Pikachu ex|Special Illustration Rare
278|Mega Eelektross ex|Special Illustration Rare
279|Iono's Bellibolt ex|Special Illustration Rare
280|Lillie's Clefairy ex|Special Illustration Rare
281|Team Rocket's Mewtwo ex|Special Illustration Rare
282|Mega Diancie ex|Special Illustration Rare
283|Mega Hawlucha ex|Special Illustration Rare
284|Mega Gengar ex|Special Illustration Rare
285|Mega Scrafty ex|Special Illustration Rare
286|N's Zoroark ex|Special Illustration Rare
287|Marnie's Grimmsnarl ex|Special Illustration Rare
288|Fezandipiti ex|Special Illustration Rare
289|Steven's Metagross ex|Special Illustration Rare
290|Mega Dragonite ex|Special Illustration Rare
291|Canari|Special Illustration Rare
292|Iris's Fighting Spirit|Special Illustration Rare
293|Surfer|Special Illustration Rare
294|Mega Charizard Y ex|Mega Hyper Rare
295|Mega Dragonite ex|Mega Hyper Rare
"""

# <number><variant><raw>,<psa9>,<psa10>   variant: b base, B Ball, E Energy,
# R Reverse Holo, C Cosmos Holo, P Prize Pack, J Jumbo. Empty price = no sales data.
PRICES = """
1B.13,10.18,30.61 1b1.07,11.45,35.02 1E.77,10.84,32.91 2B.13,10.19,30.66 2b.64,10.95,33.29
2E.28,10.39,31.36 3b1.04,15.50,110.62 4B.10,10.20,30.70 4b.70,11.36,34.70 4E.75,11.00,33.47
5B.12,10.12,30.42 5b.40,10.54,31.88 5E1.79,12.43,38.40 6B.20,10.27,30.94 6b.70,10.95,33.29
6E.62,10.85,32.96 7B.20,10.14,30.47 7b.40,12.83,53.44 7C.42,, 7E.26,10.76,32.63 8B.71,10.84,32.91
8b1.29,15.50,26.00 8C.93,, 8E.52,14.00,31.46 9B.62,11.29,34.46 9b.16,13.17,30.70 9E.91,11.15,33.99
10b1.85,9.49,31.00 11B.55,8.99,32.96 11b.19,19.85,60.03 11E.82,10.34,31.17 12B.62,10.84,32.91
12b.12,10.22,30.75 12E.24,14.00,31.18 13B.50,10.11,30.38 13b.14,10.46,31.60 13E.85,11.19,34.13
14B.20,10.54,31.88 14b.20,10.24,30.85 14E1.49,12.08,37.18 15B.59,10.15,30.52 15b.12,10.11,30.38
15E1.58,12.17,37.51 16B.56,10.54,31.88 16b.14,10.22,30.75 16E.45,10.73,32.54 17B.27,10.37,31.27
17b.33,10.15,30.52 17E1.49,12.02,37.00 18b.41,10.57,31.97 18E1.79,12.22,37.70 18R.53,10.75,32.58
19b.30,10.41,31.41 19E.25,10.31,31.08 19R.82,10.81,32.82 20B.93,32.98,360.00 20b1.25,17.00,127.50
20C2.13,14.33,174.62 20E1.78,300.00,693.50 21B.62,29.95,33.76 21b.40,18.50,31.88 21E1.69,11.00,29.00
22b7.00,33.50,100.00 22P62.23,, 23B.03,10.05,30.19 23b.32,20.00,122.50 23E.33,10.46,31.60
24B.11,10.15,30.52 24b.79,11.07,33.71 24E.55,10.96,33.33 25B.25,22.50,32.91 25b.79,11.36,34.70
25E.70,11.42,34.93 26b.98,12.28,48.68 27B.58,10.61,32.11 27b.10,10.33,31.13 27E1.52,12.02,37.00
28B.51,10.69,32.39 28b.05,10.14,30.47 28E1.13,11.34,34.65 29B.27,10.81,32.82 29b.62,13.50,49.81
29C.99,, 29E1.51,12.05,37.09 30B.40,10.54,31.88 30b.11,10.15,28.00 30E1.74,12.41,38.36
31b1.14,46.00,55.00 32B.18,10.26,30.89 32b.71,10.35,31.22 32E1.71,12.25,37.80 33B.16,10.22,30.75
33b.40,10.35,31.22 33E1.75,12.39,38.27 34B.40,10.50,31.74 34b.08,10.11,30.38 34E.24,10.54,31.88
35B.05,10.14,30.47 35b.09,10.09,30.33 35E1.75,12.43,38.41 36B.55,10.75,32.58 36b.42,10.68,32.35
36E1.49,11.90,36.57 37B.25,10.39,31.36 37b.09,10.14,30.47 37E1.29,11.90,36.57 38b1.65,14.00,37.00
39B1.00,39.52,195.00 39b1.00,36.00,90.34 39E1.49,34.99,141.85 40B.89,19.99,34.65 40b.32,12.00,46.52
40E.70,11.13,33.90 41B.40,10.66,32.30 41b.25,23.00,56.07 41C1.16,, 41E.41,30.00,33.05
42B.52,10.80,32.77 42b.71,11.34,34.65 42E1.63,12.20,37.61 43b1.80,19.50,50.00 44B.23,10.31,31.08
44b.15,10.11,30.38 44E1.49,12.02,37.00 45B.31,10.39,31.36 45b.14,10.05,30.19 45E1.60,12.17,37.51
46B.99,11.03,33.57 46b.26,10.46,31.60 46E.39,10.72,32.49 47b2.63,16.40,85.00 48b.96,14.73,34.51
49B.28,10.39,31.36 49b.55,10.33,31.13 49E1.60,12.20,37.61 50B.11,10.15,30.52 50b.70,10.62,32.16
50E1.79,12.56,38.88 51B.11,10.08,30.28 51b.53,10.31,31.08 51E1.68,12.28,37.89 52B.73,10.98,33.38
52b.55,10.95,33.29 52E1.42,11.93,36.67 53B.23,10.31,31.08 53b.15,14.00,30.71 53E1.59,12.35,38.13
54B.40,10.54,31.88 54b.25,10.27,30.94 54E1.60,12.17,37.51 55B1.44,21.72,67.21 55b1.25,17.00,174.00
55E1.39,28.02,251.90 56B1.10,11.23,34.27 56b.71,14.00,33.52 56E1.99,12.70,39.35 57b5.06,27.66,101.20
58b1.94,12.75,39.53 59B.39,10.34,31.17 59b.29,10.46,31.60 59E1.17,11.87,36.48 60B.22,10.96,33.34
60b.40,10.54,31.88 60E1.87,12.49,38.65 61b1.79,12.37,89.98 62B.29,10.20,30.70 62b.18,10.24,30.85
62E1.42,11.93,36.66 63B.14,10.23,30.80 63b.20,10.16,30.56 63E1.72,12.33,38.08 64B.10,10.14,30.47
64b.17,10.05,30.19 64E1.49,12.02,36.99 65B.32,10.54,31.88 65b.10,10.14,30.47 65E.35,10.37,31.27
66B.17,10.23,30.80 66b.02,10.04,30.14 66E1.69,12.16,37.46 67B.18,10.46,31.60 67b.15,10.20,30.70
67E.45,10.92,33.19 68b1.36,11.86,90.00 69B.12,10.22,30.75 69b.80,11.34,34.65 69E1.79,12.43,38.41
70b.99,12.50,34.00 71B.32,10.38,31.32 71b.99,11.65,35.73 71E1.69,12.26,37.84 72B.12,10.24,30.85
72b.99,10.54,31.88 72E.40,10.54,66.00 73b.98,11.49,36.88 74B.81,11.21,34.18 74b.27,10.39,31.36
74E.54,13.50,32.72 75B.81,11.06,33.66 75b.28,10.12,30.42 75E1.50,12.07,37.19 76b1.60,15.00,26.00
77b.25,10.34,31.17 77E1.37,, 77R1.67,, 78b1.00,12.00,34.70 78E1.83,, 78R1.62,12.37,
79b2.08,36.00,137.50 80B.70,10.95,33.29 80b.12,10.20,30.70 80E1.65,14.00,37.84 81B.70,10.95,33.29
81b.26,10.37,31.27 81E1.30,11.76,36.11 82B1.00,11.36,34.70 82b1.00,11.36,34.69 82E.87,11.52,35.26
83B.52,10.70,32.44 83b.24,10.75,32.58 83E1.48,12.01,36.95 84b1.02,19.50,67.00 85B.78,10.75,32.58
85b.54,10.75,32.58 85E1.55,12.10,37.28 86B.49,10.49,31.69 86b.55,11.09,31.00 86E.84,10.95,31.00
87B.75,11.02,33.52 87b.16,10.22,30.75 87E1.49,11.68,35.83 88B.55,10.75,32.58 88b.15,10.22,30.75
88E.99,11.23,34.27 89b1.38,11.87,28.00 90B.68,10.45,31.55 90b.21,10.18,30.61 90E1.56,12.13,37.38
91B.40,10.99,33.43 91b.07,10.07,30.23 91E1.61,12.36,38.17 92B.55,10.79,32.72 92b.40,10.49,31.69
92E1.49,12.02,36.99 93B.80,10.95,33.29 93b.15,10.20,30.70 93E.26,10.34,31.17 94B.99,10.95,33.29
94b.25,10.58,32.02 94E1.64,12.24,37.75 95B.20,10.24,30.85 95b.73,10.95,33.29 95E1.45,12.15,37.47
96B.24,10.30,31.03 96b.85,11.22,34.22 96E.37,10.90,33.10 97b.99,18.51,60.31 97E2.00,25.00,39.39
97R1.99,17.50,60.82 98B1.25,11.34,34.65 98b.87,11.70,35.87 98E.70,10.54,31.88 99B.87,10.95,33.28
99b1.19,11.17,34.04 99E.79,11.36,34.70 100b.07,16.00,33.00 100E.99,11.34,34.65 100R1.23,11.99,35.60
101b.49,10.84,51.00 101E1.86,12.52,38.75 101R1.25,11.67,35.78 102B.11,10.37,31.27
102b.20,10.56,31.92 102E1.50,12.02,37.01 103B.30,10.14,30.47 103b.23,10.28,30.99
103E1.49,12.02,37.01 104B.37,10.50,31.74 104b.10,10.14,30.47 104E1.27,11.91,36.62
105B.24,10.33,31.13 105b.91,10.54,31.88 105E.40,11.02,33.52 106B.20,10.27,30.94 106b.20,10.27,30.94
106E1.59,12.20,37.60 107b1.17,12.02,64.00 108B.45,10.61,32.11 108b.77,19.50,36.67
108E.70,11.36,34.69 109B.15,10.20,30.70 109b.45,10.95,33.29 109E.62,11.07,33.71 110B.20,10.27,30.94
110b.55,11.29,34.46 110E1.91,12.59,38.98 111b1.77,12.02,36.99 112B.20,10.35,31.22
112b.14,14.00,30.66 112E1.36,11.84,36.00 113b1.42,11.51,43.26 114b1.49,12.02,60.00
115B.13,10.57,31.97 115b.14,10.18,30.61 115E1.20,11.83,36.34 116b1.71,12.52,43.50 116J9.49,,
117B.10,10.68,32.35 117b.19,10.26,30.89 117E1.55,12.10,37.28 118B.21,10.26,30.89 118b.06,10.07,30.23
118E.29,10.37,31.27 119B.23,10.34,31.17 119b.03,10.04,30.14 119E1.14,11.54,35.36 120B.27,10.41,31.41
120b.12,10.20,30.70 120E1.67,12.43,38.40 121b1.75,14.00,28.00 122B.23,10.31,31.08
122b.40,10.54,31.88 122E.33,10.45,26.00 123B.44,11.02,33.52 123b.29,12.00,89.78 123C1.90,11.25,
123E.50,14.00,33.43 124B.40,10.99,33.43 124b.28,10.42,31.46 124E1.79,12.46,38.50
125b3.49,28.56,68.00 126b.29,12.99,32.11 126E2.15,12.93,40.16 126R1.78,12.68,39.30
127b.70,10.95,33.29 127E.24,10.26,30.89 127R1.36,12.02,37.00 128B.74,10.84,32.91 128b.42,10.69,32.39
128E1.49,13.40,37.47 129B.67,11.10,33.80 129b.20,10.14,30.47 129E1.69,12.37,38.22
130B.70,10.64,32.21 130b.25,10.34,31.17 130E1.49,12.02,37.00 131B.80,10.85,32.96 131b.12,10.26,30.89
131E.40,10.43,31.50 132B.70,10.68,32.35 132b.40,10.54,31.88 132E1.61,12.20,37.61 133B.07,10.09,30.33
133b.67,10.34,31.17 133E1.66,12.22,37.70 134B.77,10.95,33.29 134b.21,10.27,30.94
134E1.49,12.09,37.23 135b1.96,8.99,46.00 136B.15,10.19,30.66 136b1.15,11.34,34.65
136E1.49,12.32,38.03 137b1.80,5.38,49.99 138B.15,10.33,31.13 138b.06,10.09,30.33
138E1.31,11.76,36.10 139b.95,10.00,34.70 140B.22,10.41,31.41 140b.07,10.18,30.61
140E1.73,12.29,37.94 141B.19,10.20,30.70 141b.70,11.30,34.51 141E.58,11.13,33.90
142b2.94,14.07,44.08 143B.15,10.26,30.89 143b.51,10.99,33.43 143E1.29,11.75,36.06
144B.69,11.34,34.65 144b.23,10.28,30.99 144E1.50,12.04,37.04 145b1.44,11.93,36.67
146B.34,10.71,32.44 146b.08,10.11,30.38 146E.25,10.27,50.00 147B.26,10.22,30.75 147b.10,10.22,30.75
147E1.49,12.02,36.99 148B.15,10.27,30.94 148b.55,10.96,33.33 148E.26,10.66,32.30
149b1.15,11.87,28.00 150B.55,19.99,34.70 150b.72,11.70,35.87 150E1.53,12.10,37.28 151B.81,8.99,35.02
151b.35,13.00,48.21 151E1.76,12.39,38.26 152b4.97,83.00,83.62 153B1.58,7.52,38.07
153b1.59,34.00,236.57 153E2.96,14.50,44.04 154B.26,10.39,31.36 154b.86,13.50,56.99
154E1.63,10.66,100.00 155B.34,10.46,31.60 155b1.49,22.00,67.05 155E.90,11.22,34.22
156B.12,10.54,31.88 156b.22,30.00,31.03 156E1.86,12.43,135.00 157B.55,10.41,31.41
157b.10,10.27,30.94 157E1.59,12.16,37.47 158B.32,10.14,30.47 158b.40,10.31,31.08
158E1.58,12.14,37.43 159B.32,29.95,31.88 159b.70,10.95,33.29 159E1.50,12.03,37.05
160b1.76,1.29,76.00 161b.69,16.50,33.29 161E1.92,12.63,39.11 161R1.58,12.14,63.50
162b1.18,11.72,35.96 163B.12,10.18,30.61 163b.40,10.54,31.88 163E1.45,12.10,37.28
164b1.27,12.29,64.00 165B.63,11.11,33.85 165b.31,14.82,31.50 165E1.84,12.49,38.65
166B.38,10.95,33.29 166b.23,10.34,31.17 166E1.25,12.17,37.51 167b.86,11.29,34.46 168B.02,10.03,30.09
168b.79,10.72,32.49 168E1.69,12.33,38.08 169B.04,10.07,30.23 169b.16,10.47,31.64
169E1.75,12.37,38.23 170B.17,10.22,30.75 170b.76,10.91,33.14 170E1.79,12.24,37.75
171B.20,10.27,30.94 171b.25,1.75,31.17 171E1.17,11.82,36.30 172b1.67,17.50,38.66 173B.09,10.14,30.47
173b.30,10.54,31.88 173E.40,10.37,31.27 174B.20,10.27,30.94 174b.11,19.00,30.70 174E.40,10.72,32.49
175B.19,10.26,30.89 175b.25,11.10,105.75 175C.47,, 175E1.79,12.42,38.42 176B.18,10.24,30.85
176b.15,10.07,30.23 176E1.54,12.33,38.08 177B.10,10.09,30.33 177b.07,10.34,31.17
177E1.49,12.02,37.01 178B.28,10.34,31.17 178b.24,10.33,31.13 178E.40,10.75,32.58
179b1.00,11.36,32.58 180b.32,10.37,31.27 180R1.54,12.09,37.23 181b.62,10.87,33.01
181R1.99,12.70,39.35 182b.37,10.47,31.64 182R1.59,12.21,37.65 183b.88,11.25,34.32
183R2.04,12.77,39.57 184b1.06,11.42,34.93 184R1.73,12.39,38.26 185b1.35,10.96,33.33
185R1.70,12.32,38.04 186b.25,10.20,30.70 186R1.62,12.18,37.56 187b.34,10.46,31.60
187R1.78,12.41,38.37 188b.74,11.03,33.57 188R1.72,12.29,37.94 189b.29,10.35,31.22
189R1.69,12.31,37.98 190b.20,10.27,30.94 190R1.61,12.25,37.79 191b.62,10.89,33.10
191R1.79,12.43,38.41 192b1.34,11.82,36.29 192R2.31,12.63,39.11 193b.39,10.38,31.31
193R1.51,12.46,38.49 194b.26,10.43,31.50 194R1.55,12.10,37.28 195b.40,10.65,32.26
195R1.91,15.00,38.97 196b1.34,11.30,34.51 196R1.49,12.02,37.00 197b.67,10.92,33.20
197R1.79,12.43,38.41 198b.86,15.00,51.07 198R1.84,6.63,40.80 199b.40,10.53,31.83
199R1.66,12.27,37.84 200b.20,10.27,30.94 200R1.83,12.48,38.60 201b.40,10.54,31.88
201R1.49,12.02,36.99 202b.55,10.96,33.33 202R1.69,12.20,37.60 203b.42,10.75,32.58
203R1.59,12.29,37.94 204b.70,11.00,33.47 204R1.78,12.40,38.31 205b.25,10.30,31.03
205R1.72,12.42,38.36 206b.40,10.85,32.96 206R1.57,12.16,37.46 207b1.06,11.63,35.63
207R2.02,12.74,39.48 208b.27,10.37,31.27 208R1.74,12.29,37.94 209b.28,10.98,33.38
209R1.70,12.43,38.41 210b.59,10.80,32.77 210R1.84,12.44,38.45 211b.32,10.43,31.50
211R1.69,12.29,37.94 212b.30,10.33,31.13 212R1.75,12.37,38.22 213b.82,10.41,31.41
213R1.69,12.29,37.94 214b.13,10.18,30.61 214R1.57,12.13,37.37 215b.40,10.54,31.88
215R1.89,12.56,38.88 216b.29,10.52,31.78 216R1.69,12.27,37.84 217b.66,10.96,33.33
217R1.79,12.43,38.41 218b18.89,35.00,124.76 219b7.48,25.53,100.00 220b2.78,20.00,73.75
221b8.79,15.43,62.00 222b7.18,30.18,79.38 223b6.13,22.00,89.50 224b3.06,23.50,67.83
225b8.50,26.25,76.88 226b71.88,104.00,329.50 227b5.99,20.60,75.00 228b4.63,28.00,79.56
229b2.64,20.60,51.56 230b2.72,19.15,64.85 231b9.33,22.78,61.85 232b12.37,24.45,106.64
233b5.00,21.50,79.50 234b9.45,22.50,95.00 235b6.22,17.31,73.00 236b8.25,18.44,67.00
237b4.37,20.60,80.80 238b22.76,35.63,161.88 239b9.99,24.26,94.00 240b6.25,23.35,90.75
241b6.00,19.75,73.05 242b5.99,15.73,67.97 243b8.18,27.50,100.65 244b10.48,24.25,92.19
245b3.08,16.50,61.00 246b6.58,23.28,95.53 247b8.43,21.40,67.04 248b5.95,15.29,67.33
249b4.99,16.50,72.76 250b3.41,18.81,58.73 251b2.85,19.00,68.74 252b1.00,18.40,32.69
253b2.35,22.00,68.10 254b1.73,20.00,55.61 255b1.60,17.20,57.50 256b6.19,44.94,109.17
257b3.37,20.23,73.50 258b1.25,15.25,46.00 259b.99,11.34,69.00 260b1.25,11.44,49.99
261b1.89,13.40,92.73 262b2.99,22.27,116.29 263b1.62,13.61,58.50 264b6.18,15.00,44.84
265b9.50,23.55,81.00 266b4.72,20.50,76.00 267b8.19,22.50,72.46 268b4.90,22.24,85.75
269b59.99,62.79,231.03 270b4.88,20.00,76.14 271b38.96,51.14,165.00 272b82.41,86.51,205.88
273b52.89,74.00,162.60 274b132.69,198.00,302.27 275b71.00,77.90,226.54 276b968.48,942.00,2282.13
277b352.94,349.01,978.50 278b38.69,37.00,117.57 279b59.75,63.25,151.50 280b165.51,198.00,372.82
281b341.09,355.00,701.74 282b51.39,55.00,158.40 283b53.24,58.00,163.95 284b1027.16,957.91,2175.00
285b55.50,64.00,193.59 286b151.25,155.00,362.75 287b65.58,60.00,161.76 288b55.13,74.00,163.65
289b91.27,90.00,331.45 290b649.68,710.00,1260.00 291b36.59,37.50,125.73 292b32.23,39.01,161.00
293b21.50,34.32,133.99 294b391.00,425.00,2188.44 295b238.20,241.71,1173.09
"""

# variant char -> (slot id, label, PriceCharting slug suffix)
VARIANTS = {
    "B": ("ball",   "Ball Reverse Holo",   "ball"),
    "E": ("energy", "Energy Reverse Holo", "energy"),
    "R": ("rh",     "Reverse Holo",        "reverse-holo"),
    "C": ("cosmos", "Cosmos Holo",         "cosmos-holo"),
    "P": ("prize",  "Prize Pack",          "prize-pack"),
    "J": ("jumbo",  "Jumbo",               "jumbo"),
}

_names, _rar = {}, {}
for line in CHECKLIST.strip().splitlines():
    n, nm, r = line.split("|")
    _names[int(n)] = nm
    _rar[int(n)] = r

_TOK = re.compile(r"^(\d+)([bBERCPJ])(\d*\.\d{2})?,(\d*\.\d{2})?,(\d*\.\d{2})?$")
_px = {}
for tok in PRICES.split():
    m = _TOK.match(tok)
    if not m:
        raise ValueError("bad price token: %r" % tok)
    num, v = int(m.group(1)), m.group(2)
    f = lambda g: float(g) if g else None
    _px.setdefault((num, v), (f(m.group(3)), f(m.group(4)), f(m.group(5))))

BASE, RH, RH_EST, SPECIAL = [], {}, set(), {}
for num in sorted(_names):
    raw, p9, p10 = _px.get((num, "b"), (None, None, None))
    BASE.append((num, _names[num], _rar[num], raw, p9, p10, 0))
for (num, v), (raw, p9, p10) in sorted(_px.items()):
    if v == "b":
        continue
    vid, label, suf = VARIANTS[v]
    SPECIAL.setdefault(num, []).append((vid, label, suf, raw, p9, p10))
for num in SPECIAL:
    SPECIAL[num].sort(key=lambda t: ["ball", "energy", "rh", "cosmos", "prize", "jumbo"].index(t[0]))

assert len(BASE) == 295, len(BASE)
assert all(b[3] is not None for b in BASE), "every base card needs a raw price"
assert sum(len(v) for v in SPECIAL.values()) == len(_px) - 295

SET = {
    "id": "AHE", "name": "Ascended Heroes", "series": "Mega Evolution",
    "released": "2026-01-30", "total": 295, "baseTotal": 217,
    "code": "ASC", "pcslug": "pokemon-ascended-heroes",
    "tcgc": "https://www.tcgcollector.com/sets/11680/ascended-heroes",
    "priceDate": "2026-08-19", "accent": "#a06cf0",
    "logos": [
        "https://d1i787aglh9bmb.cloudfront.net/assets/img/global/logos/en-us/me02pt5.png",
        "https://archives.bulbagarden.net/media/upload/thumb/b/b9/ME2.5_Logo_EN.png/640px-ME2.5_Logo_EN.png",
        "https://archives.bulbagarden.net/media/upload/b/b9/ME2.5_Logo_EN.png",
        "https://archives.bulbagarden.net/media/upload/thumb/0/0e/SetSymbolAscended_Heroes.png/120px-SetSymbolAscended_Heroes.png",
    ],
}
