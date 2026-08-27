"""Throwaway three-card set, used only to prove a second game builds and gets its own
storage. Not shipped, not a real game."""
BASE = [(1, "Monkey D. Luffy", "Leader", 12.00, 40.00, 120.00, 0),
        (2, "Roronoa Zoro",    "Super Rare", 3.50, 18.00, 60.00, 0),
        (3, "Nami",            "Common",  0.20, 9.00, 25.00, 0)]
RH, RH_EST = {}, set()
SPECIAL = {1: [("alt", "Alternate Art", "alt-art", 88.00, 140.00, 410.00)],
           2: [("manga", "Manga Rare", "manga", 210.00, None, None)]}
SET = {"id":"OP01","name":"Romance Dawn","series":"One Piece","released":"2022-12-02",
       "total":3,"baseTotal":3,"code":"OP01","pcslug":"one-piece-romance-dawn",
       "tcgc":"https://onepiece.limitlesstcg.com/cards/OP01","priceDate":"2026-08-19",
       "accent":"#d4342c","logos":[]}
