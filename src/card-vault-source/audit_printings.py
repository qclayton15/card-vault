"""Compare our slot layout against the printings TCGplayer actually lists.

/tmp/printings.txt holds one character per card, harvested from pokemontcg.io's
tcgplayer.prices keys — the authoritative list of which printings of a card exist:

    n normal            N normal + reverse
    h holofoil          H holofoil + reverse
    r reverse only      m normal + holofoil      A all three      0 no data

Our data modules give every card a "base" slot, plus rh, plus promos. The question
this answers is whether "base" is the right label: for a card printed only as a
holo (Vileplume PFL 3), calling the standard printing "Base" is wrong.
"""
import importlib, collections

MODULES = {"MEW": "data_mew", "SSP": "data_ssp", "PRE": "data_pre", "JTG": "data_jtg",
           "DRI": "data_dri", "MEV": "data_mev", "PFL": "data_pfl",
           "AHE": "data_ahe", "POR": "data_por"}

DECODE = {"n": ("normal",), "h": ("holo",), "r": ("rev",),
          "N": ("normal", "rev"), "H": ("holo", "rev"), "m": ("normal", "holo"),
          "A": ("normal", "holo", "rev"), "0": ()}

REV = {"rh", "ball", "energy", "play", "master", "horizonsrh", "rhcosmos", "rhplay"}

api = {}
for line in open("/tmp/printings.txt"):
    sid, total, s = line.split()
    assert len(s) == int(total), (sid, len(s), total)
    api[sid] = s

report = collections.defaultdict(list)
for sid, modname in MODULES.items():
    if sid not in api or set(api[sid]) == {"0"}:
        print("%s  — no TCGplayer data, skipped" % sid)
        continue
    m = importlib.import_module(modname)
    s = api[sid]
    for num, name, rarity, raw, p9, p10, est in m.BASE:
        have_rev = num in m.RH or any(v[0] in REV for v in m.SPECIAL.get(num, []))
        have_holo = any(v[0] == "holo" for v in m.SPECIAL.get(num, []))
        want = DECODE[s[num - 1]]
        if not want:
            report["nodata"].append((sid, num, name))
            continue
        # the standard (non-reverse) printing: is it normal, holo, or both?
        if "holo" in want and "normal" not in want and not have_holo:
            report["relabel"].append((sid, num, name, rarity))
        elif "normal" in want and "holo" in want and not have_holo:
            report["both"].append((sid, num, name, rarity))
        elif "normal" not in want and "holo" not in want:
            report["revonly"].append((sid, num, name, rarity))
        if ("rev" in want) != have_rev:
            report["missing_rev" if "rev" in want else "extra_rev"].append(
                (sid, num, name, rarity))

for key, title in [("relabel", 'base slot should read "Holo" (holofoil, no normal printing)'),
                   ("both",    'has BOTH normal and holofoil — we only carry one slot'),
                   ("revonly", 'reverse-only printing (no standard printing at all)'),
                   ("missing_rev", "API lists a reverse holo, we have no reverse slot"),
                   ("extra_rev",   "we have a reverse slot, API lists none"),
                   ("nodata",  "no TCGplayer data for this card")]:
    rows = report[key]
    print("\n%s — %d" % (title, len(rows)))
    by = collections.Counter(r[0] for r in rows)
    print("   " + (", ".join("%s:%d" % kv for kv in sorted(by.items())) or "none"))
    for r in rows[:14]:
        print("   ", " ".join(str(x) for x in r))
    if len(rows) > 14:
        print("    … %d more" % (len(rows) - 14))
