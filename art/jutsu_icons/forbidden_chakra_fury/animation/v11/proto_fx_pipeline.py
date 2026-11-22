import math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, "/home/claude/tnr-tools/art/jutsu_icons/forbidden_chakra_fury/animation/v11")
import build_v11 as V
S = 4                         # supersample
N = 168                       # delivered px (scale 3 clip)
W = N * S
RAMP = [(0, (120, 40, 230)), (0.35, (140, 60, 250)), (0.6, (190, 110, 255)), (0.82, (232, 190, 255)), (0.95, (250, 240, 255)), (1, (255, 255, 255))]

def ramp(v):
    for (a, ca), (b, cb) in zip(RAMP, RAMP[1:]):
        if v <= b:
            t = (v - a) / (b - a)
            return tuple(int(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))
    return RAMP[-1][1]
LUT = [ramp(i / 255) for i in range(256)]

def tapered(d, pts, w0, w1, val):
    n = len(pts)
    for i, (p, q) in enumerate(zip(pts, pts[1:])):
        w = w0 + (w1 - w0) * i / max(1, n - 2)
        d.line([p, q], fill=val, width=max(1, int(w)))
        d.ellipse((q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2), fill=val)

def frame(seed=4):
    rnd = random.Random(seed)
    core = Image.new("L", (W, W), 0)
    d = ImageDraw.Draw(core)
    g = (W / 2, W / 2)
    top = (W / 2 - 26 * 2 * S, 0)
    path = V.jag(top, g, 0.42, rnd, 6)
    tapered(d, path, 1.5 * S, 4 * S, 255)                      # thin at the sky, thick at impact
    for _ in range(5):                                        # tapered branches
        i = rnd.randrange(3, len(path) - 3)
        p = path[i]; a = rnd.uniform(-2.4, -0.6) if rnd.random() < .5 else rnd.uniform(0.6, 2.4)
        q = (p[0] + math.cos(a) * 30 * S, p[1] + abs(math.sin(a)) * 22 * S)
        tapered(d, V.jag(p, q, 0.6, rnd, 4), 3 * S, 0.5 * S, 200)
    for _ in range(6):                                        # ground arcs, flattened
        a = rnd.uniform(0, 2 * math.pi)
        q = (g[0] + math.cos(a) * 38 * S, g[1] + math.sin(a) * 19 * S)
        tapered(d, V.jag(g, q, 0.6, rnd, 4), 4 * S, 0.5 * S, 170)
    d.ellipse((g[0] - 9 * S, g[1] - 4.5 * S, g[0] + 9 * S, g[1] + 4.5 * S), fill=255)   # impact flash
    # bloom: intensity = core + stacked blurs; then gradient map, alpha from intensity
    inten = core
    for r, k in ((2, 0.75), (7, 0.5), (18, 0.35)):
        b = core.filter(ImageFilter.GaussianBlur(r * S)).point(lambda v, k=k: min(255, int(v * k * 2.2)))
        inten = ImageChops.lighter(inten, b)
    inten = inten.resize((N, N), Image.LANCZOS)
    rgb = Image.merge("RGB", [inten.point([c[i] for c in LUT]) for i in range(3)])
    alpha = inten.point(lambda v: min(255, int(255 * (v / 255) ** 0.8 * 1.1)))
    out = rgb.convert("RGBA"); out.putalpha(alpha)
    return out

def show(fx, old):
    tiles = []
    for bg in ((52, 64, 44), (150, 140, 110), (18, 18, 26)):
        for im in (old, fx):
            c = Image.new("RGBA", (N, N), bg + (255,)); c.alpha_composite(im); tiles.append(c)
    sheet = Image.new("RGBA", (N * 2 + 6, N * 3 + 12), (0, 0, 0, 255))
    for i, t in enumerate(tiles):
        sheet.alpha_composite(t, ((i % 2) * (N + 6), (i // 2) * (N + 6)))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.LANCZOS).save("/tmp/proto_compare.png")

c = V.clips()
old = c["storm_b"][0][8 + 3]          # current seeker, strike beat
show(frame(), old)
