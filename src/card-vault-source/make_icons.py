"""Generate the home-screen / tab icons and emit them as base64 data URIs.

The mark matches the one in the app header: the blue-violet-pink gradient with a CV
monogram and a narrow diagonal sheen.

Every icon is a full-bleed square. iOS masks apple-touch-icon to its own squircle, and
Android masks maskable icons, so baking in rounded corners only risks a dark halo. That
also keeps the PNGs free of an alpha channel, which lets them quantise down hard — these
are inlined into the HTML as data URIs, so bytes matter.
"""
import base64, io, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# deeper than the CSS gradient: a home-screen icon is small and needs the extra saturation
A, B, C = (42, 116, 245), (140, 78, 245), (240, 86, 160)


def lerp(c1, c2, t):
    return tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def gradient(size):
    n = 64
    g = Image.new("RGB", (n, n))
    px = g.load()
    for y in range(n):
        for x in range(n):
            t = x / (n - 1) * 0.42 + y / (n - 1) * 0.58
            px[x, y] = lerp(A, B, min(t / 0.55, 1)) if t <= 0.55 else lerp(B, C, (t - 0.55) / 0.45)
    return g.resize((size, size), Image.BICUBIC)


def sheen(size):
    """A narrow highlight band, not a wash — the old one desaturated the whole icon."""
    lay = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(lay)
    w = size * 0.13
    d.polygon([(-w, size * 0.52), (size * 0.52, -w),
               (size * 0.52 + w, -w), (-w + w, size * 0.52)], fill=64)
    return lay.filter(ImageFilter.GaussianBlur(size * 0.05))


def monogram(size, scale):
    lay = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(FONT, int(size * scale))
    b = d.textbbox((0, 0), "CV", font=f)
    d.text(((size - b[2] - b[0]) / 2, (size - b[3] - b[1]) / 2 - size * 0.015),
           "CV", font=f, fill=255)
    return lay


def icon(size, scale):
    img = gradient(size)
    img.paste(Image.new("RGB", (size, size), (255, 255, 255)), (0, 0), sheen(size))
    shadow = monogram(size, scale).filter(ImageFilter.GaussianBlur(size * 0.012))
    img.paste(Image.new("RGB", (size, size), (28, 18, 66)),
              (0, int(size * 0.012)), shadow.point(lambda v: int(v * 0.42)))
    img.paste(Image.new("RGB", (size, size), (255, 255, 255)), (0, 0), monogram(size, scale))
    return img


def uri(img, colors):
    q = img.quantize(colors=colors, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    b = io.BytesIO()
    q.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode(), len(b.getvalue())


out, report = {}, []
#  name    px   monogram scale   palette
spec = [("apple", 180, 0.40, 128),   # iOS home screen
        ("i192",  192, 0.40, 128),   # Android launcher / install prompt
        ("i512",  512, 0.40, 128),   # store-quality "any"
        ("mask",  512, 0.28,  96),   # maskable: monogram inside the safe 80%
        ("fav",    64, 0.42,  64)]   # browser tab
for name, size, scale, colors in spec:
    img = icon(size, scale)
    u, n = uri(img, colors)
    out[name] = u
    img.save("/home/claude/icon_%s.png" % name)
    report.append("%-6s %3dpx  %6.1f KB png  %6.1f KB base64" % (name, size, n / 1024, len(u) / 1024))

json.dump(out, open("/home/claude/icons.json", "w"))
print("\n".join(report))
print("total inlined: %.1f KB" % (sum(len(v) for v in out.values()) / 1024))


# ---------------------------------------------------------------- ball variant
# An original Poké Ball mark drawn in the app's palette, not a copy of anyone's
# artwork: the upper half carries the same blue-violet-pink gradient as the CV mark,
# which keeps it recognisably this app rather than a facsimile of an official icon.
BG = (13, 20, 36)          # the app's dark background, so it sits on any tab colour
RA, RB = (255, 91, 71), (240, 86, 160)     # the app's ember and rose accents


def warm(size):
    """Ember-to-rose sweep for the ball's upper half — the app's own accents, but warm
    enough that the silhouette still reads as a ball at 16px."""
    n = 64
    g = Image.new("RGB", (n, n))
    px = g.load()
    for y in range(n):
        for x in range(n):
            px[x, y] = lerp(RA, RB, x / (n - 1) * 0.55 + y / (n - 1) * 0.45)
    return g.resize((size, size), Image.BICUBIC)

def ball(size, inset):
    img = Image.new("RGB", (size, size), BG)
    s = int(size * 4)                       # supersample, then downscale for clean edges
    big = Image.new("RGBA", (s, s), BG + (255,))
    d = ImageDraw.Draw(big)
    pad = int(s * inset)
    box = [pad, pad, s - pad - 1, s - pad - 1]
    r = (box[2] - box[0]) / 2
    cx = cy = (box[0] + box[2]) / 2

    top = warm(s).convert("RGBA")           # gradient only inside the upper half
    m = Image.new("L", (s, s), 0)
    md = ImageDraw.Draw(m)
    md.ellipse(box, fill=255)
    md.rectangle([0, int(cy), s, s], fill=0)
    big.paste(top, (0, 0), m)

    lower = Image.new("L", (s, s), 0)
    ld = ImageDraw.Draw(lower)
    ld.ellipse(box, fill=255)
    ld.rectangle([0, 0, s, int(cy)], fill=0)
    big.paste(Image.new("RGB", (s, s), (245, 247, 252)), (0, 0), lower)

    band = int(r * 0.18)
    d.rectangle([cx - r, cy - band / 2, cx + r, cy + band / 2], fill=BG + (255,))
    ring = int(r * 0.34)
    d.ellipse([cx - ring, cy - ring, cx + ring, cy + ring], fill=BG + (255,))
    d.ellipse([cx - ring * 0.66, cy - ring * 0.66, cx + ring * 0.66, cy + ring * 0.66],
              fill=(245, 247, 252, 255))
    edge = Image.new("L", (s, s), 0)
    ImageDraw.Draw(edge).ellipse(box, outline=255, width=int(r * 0.045))
    big.paste(Image.new("RGB", (s, s), (255, 255, 255)), (0, 0), edge.point(lambda v: v // 4))

    return big.convert("RGB").resize((size, size), Image.LANCZOS)


out2, rep2 = {}, []
for name, size, ins, colors in [("apple", 180, .10, 128), ("i192", 192, .10, 128),
                                ("i512", 512, .10, 128), ("mask", 512, .19, 96),
                                ("fav", 64, .04, 64)]:
    img = ball(size, ins)
    u, n = uri(img, colors)
    out2[name] = u
    img.save("/home/claude/ball_%s.png" % name)
    rep2.append("%-6s %3dpx  %6.1f KB base64" % (name, size, len(u) / 1024))
json.dump(out2, open("/home/claude/icons_ball.json", "w"))
print("\nball variant:")
print("\n".join(rep2))
print("total inlined: %.1f KB" % (sum(len(v) for v in out2.values()) / 1024))

# side-by-side sheet at real sizes
sheet = Image.new("RGB", (760, 380), (245, 247, 251))
dd = ImageDraw.Draw(sheet)
f = ImageFont.truetype(FONT, 15); fs = ImageFont.truetype(FONT, 11)
dd.text((28, 22), "A — CV monogram", font=f, fill=(20, 28, 44))
dd.text((28, 202), "B — Poke Ball", font=f, fill=(20, 28, 44))
for row, src in ((0, "icon"), (1, "ball")):
    x = 40
    for px in (120, 64, 44, 32, 16):
        im = Image.open("/home/claude/%s_i512.png" % src).resize((px, px), Image.LANCZOS)
        y = 52 + row * 180 + (120 - px)
        sheet.paste(im, (x, y))
        dd.text((x, 52 + row * 180 + 126), "%dpx" % px, font=fs, fill=(110, 122, 140))
        x += px + 30
sheet.save("/home/claude/icon-compare.png")
print("\nwrote icon-compare.png")
