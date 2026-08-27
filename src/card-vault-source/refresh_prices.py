"""Rewrite every set module's PRICES block from a fresh PriceCharting capture.

Input is the compact stream produced in the browser (see card-vault-adding-a-set.md):

    <SETID> <number><variantChar><raw>,<psa9>,<psa10> ...      prices in cents

Only slots the module already tracks are updated. A slot the capture is missing keeps
its previous value and is reported rather than silently blanked; a slot the capture has
that the module doesn't track is reported too, so new printings get noticed.

    python3 refresh_prices.py /tmp/fresh/fresh.txt /tmp/fresh/corrections.txt --apply
"""
import importlib, re, sys, datetime

MODS = {"MEW":"data_mew", "SSP":"data_ssp", "PRE":"data_pre", "JTG":"data_jtg",
        "DRI":"data_dri", "MEV":"data_mev", "PFL":"data_pfl", "AHE":"data_ahe",
        "POR":"data_por"}
TOK = re.compile(r"^(\d*)([A-Za-z])(\d*),(\d*),(\d*)$")


def cents(s):
    return None if s == "" else int(s) / 100.0


def read_stream(path):
    """{set id: {(number, char): (raw, psa9, psa10)}} — first value wins on duplicates."""
    out, dups = {}, []
    for line in open(path).read().split("\n"):
        parts = line.split()
        if not parts:
            continue
        sid, last = parts[0], None
        px = out.setdefault(sid, {})
        for tok in parts[1:]:
            m = TOK.match(tok)
            if not m:
                raise ValueError("bad token %r in %s" % (tok, sid))
            num = int(m.group(1)) if m.group(1) else last
            last = num
            key = (num, m.group(2))
            val = tuple(cents(m.group(i)) for i in (3, 4, 5))
            if key in px:
                dups.append("%s %d%s" % (sid, num, m.group(2)))
                # a sealed product or an unpriced promo can collide with a real card;
                # never let a row with no sales overwrite one that has them
                if not (px[key][0] is None and val[0] is not None):
                    continue
            px[key] = val
    return out, dups


def read_corrections(path):
    fixes = {}
    for line in open(path).read().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        head, val = line.split("=", 1)
        sid, key = head.split()
        m = re.match(r"^(\d+)([A-Za-z])$", key)
        num, ch = int(m.group(1)), m.group(2)
        if val == "DROP":
            fixes[(sid, num, ch)] = None
        else:
            fixes[(sid, num, ch)] = tuple(cents(x) for x in val.split(","))
    return fixes


def money(x):
    if x is None:
        return ""
    s = "%.2f" % x
    return s[1:] if s.startswith("0.") else s


def current_tokens(src):
    """(number, char) keys in the module's existing PRICES block, in order."""
    body = src.split('PRICES = """', 1)[1].split('"""', 1)[0]
    keys = []
    for tok in body.split():
        m = re.match(r"^(\d+)([A-Za-z])", tok)
        keys.append((int(m.group(1)), m.group(2)))
    return keys


def rewrite(sid, mod, fresh, report):
    path = "/home/claude/%s.py" % mod
    src = open(path).read()
    keys = current_tokens(src)
    old = importlib.import_module(mod)
    oldpx = {}
    body = src.split('PRICES = """', 1)[1].split('"""', 1)[0]
    for tok in body.split():
        m = re.match(r"^(\d+)([A-Za-z])(\d*\.?\d*),(\d*\.?\d*),(\d*\.?\d*)$", tok)
        f = lambda g: float(g) if g else None
        oldpx[(int(m.group(1)), m.group(2))] = (f(m.group(3)), f(m.group(4)), f(m.group(5)))

    toks, missing, moved = [], [], []
    for k in keys:
        new = fresh.get(k)
        if new is None:
            missing.append("%d%s" % k)
            new = oldpx[k]
        else:
            o = oldpx[k]
            if o[0] is not None and new[0] is not None and o[0] != new[0]:
                moved.append((new[0] - o[0], o[0], new[0], k))
        toks.append("%d%s%s,%s,%s" % (k[0], k[1], money(new[0]), money(new[1]), money(new[2])))

    extra = sorted(set(fresh) - set(keys))
    report[sid] = {"missing": missing, "extra": extra, "moved": moved, "slots": len(keys)}

    lines, cur = [], []
    for t in toks:
        if sum(len(x) + 1 for x in cur) + len(t) > 100:
            lines.append(" ".join(cur)); cur = []
        cur.append(t)
    if cur:
        lines.append(" ".join(cur))

    head, rest = src.split('PRICES = """', 1)
    _, tail = rest.split('"""', 1)
    src = head + 'PRICES = """\n' + "\n".join(lines) + '\n"""' + tail
    today = datetime.date.today().isoformat()
    src = re.sub(r'"priceDate": "[\d-]+"', '"priceDate": "%s"' % today, src)
    src = re.sub(r'"priceDate":"[\d-]+"', '"priceDate":"%s"' % today, src)
    src = re.sub(r'\(captured \d{4}-\d\d-\d\d\)', '(captured %s)' % today, src)
    return path, src


def main():
    stream, corr_path = sys.argv[1], sys.argv[2]
    apply = "--apply" in sys.argv
    fresh, dups = read_stream(stream)
    fixes = read_corrections(corr_path)
    for (sid, num, ch), val in fixes.items():
        if val is None:
            fresh[sid].pop((num, ch), None)
        else:
            fresh[sid][(num, ch)] = val
    if dups:
        print("duplicate rows in capture (first kept):", ", ".join(dups))

    report, out = {}, {}
    for sid, mod in MODS.items():
        path, src = rewrite(sid, mod, fresh[sid], report)
        out[path] = src

    print("\n%-5s %6s %8s %8s %8s" % ("set", "slots", "missing", "new", "moved"))
    for sid in MODS:
        r = report[sid]
        print("%-5s %6d %8d %8d %8d" % (sid, r["slots"], len(r["missing"]), len(r["extra"]), len(r["moved"])))
        if r["missing"]:
            print("      missing:", ", ".join(r["missing"][:12]), "..." if len(r["missing"]) > 12 else "")
        if r["extra"]:
            print("      untracked rows in capture:", ", ".join("%d%s" % k for k in r["extra"][:12]))

    allmoved = [(sid, m) for sid in MODS for m in report[sid]["moved"]]
    allmoved.sort(key=lambda t: -abs(t[1][0]))
    print("\nbiggest raw-price moves:")
    for sid, (d, o, n, k) in allmoved[:15]:
        print("  %-4s #%-4d %-2s  $%8.2f -> $%8.2f  %+8.2f" % (sid, k[0], k[1], o, n, d))

    if apply:
        for path, src in out.items():
            open(path, "w").write(src)
        print("\napplied to %d modules" % len(out))
    else:
        print("\ndry run — pass --apply to write")


main()
