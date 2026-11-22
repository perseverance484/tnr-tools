"""HD ground hero still: one major fissure per tile with a swelling body, plasma texture flowing in its glow,
arched HD arcs above it, sparks, and lit rock plates. Used to settle the look before animating."""
import math, random, sys
sys.path.insert(0, '.')
from PIL import Image, ImageChops, ImageDraw, ImageFilter
import fxlight as L
import ground_hd as G
SS = 4


def fbm(size, seed, scales=(6, 14, 30), weights=(0.5, 0.3, 0.2)):
    random.seed(seed)
    acc = Image.new("L", size, 0)
    for s, w in zip(scales, weights):
        small = Image.effect_noise((max(2, size[0] // s), max(2, size[1] // s)), 80)
        big = small.resize(size, Image.BICUBIC)
        acc = Image.blend(acc, big, w / (w + 0.0001) if acc.getextrema() == (0, 0) else w)
    return acc.point(lambda v: max(0, min(255, int((v - 128) * 2.2 + 128))))


def hero(seed, n=168, t=0, heat=1.0, arcs=2):
    rnd = random.Random(seed)
    h = n / 2; c = n / 2; W = n * SS
    P = G.hex_pts(c, c, h)
    mids = [G.lerp(P[i], P[(i + 1) % 6], 0.5) for i in range(6)]
    pair = [(0, 3), (1, 4), (2, 5)][seed % 3]
    A, B = mids[pair[0]], mids[pair[1]]
    bend = G.lerp(G.lerp(A, B, 0.5), (c + rnd.uniform(-20, 20), c + rnd.uniform(-8, 8)), 1.0)
    main = G.angular(A, bend, rnd, 0.28) + G.angular(bend, B, rnd, 0.28)[1:]
    # a second, minor fissure branching off to another midpoint (shared crossing, so it continues next door)
    other = [k for k in range(6) if k not in pair][rnd.randrange(4)]
    j = rnd.randrange(len(main) // 3, 2 * len(main) // 3)
    minor = G.angular(mids[other], main[j], rnd, 0.32)
    core = Image.new("L", (W, W), 0); dl = ImageDraw.Draw(core)
    body = Image.new("L", (W, W), 0); db = ImageDraw.Draw(body)
    matter = Image.new("RGBA", (W, W), (0, 0, 0, 0)); dm = ImageDraw.Draw(matter)

    def widths(pts, base, ph):
        out = []
        for k in range(len(pts)):
            u = k / (len(pts) - 1)
            env = math.sin(math.pi * u)
            out.append(base * (0.45 + 0.55 * env * (0.6 + 0.4 * abs(math.sin(u * 11 + ph)))) + base * 0.35 * (1 - env))
        return out
    for pts, base, val in ((main, 5.5, 255), (minor, 3.4, 220)):
        ws = widths(pts, base, rnd.uniform(0, 6))
        poly = G.fissure_poly(pts, [w * 2.2 for w in ws])
        dm.polygon(poly, fill=(12, 5, 20, 150))               # the dark rift
        db.polygon(G.fissure_poly(pts, ws), fill=int(val * 0.5 * heat))   # molten body
        dl.line([(x * SS, y * SS) for x, y in pts], fill=int(val * heat), width=int(base * 0.2 * SS), joint="curve")
    # rock plates lifted along the rift: lit rims facing the light
    for k in range(4, len(main) - 4, 11):
        x, y = main[k]
        for sgn in (-1, 1):
            if rnd.random() < 0.4:
                continue
            r = rnd.uniform(4.5, 8)
            px_, py_ = x + rnd.uniform(-3, 3), y + sgn * rnd.uniform(6, 10)
            poly = L.rock(rnd, px_, py_, r)
            dm.polygon([(a * SS, b * SS) for a, b in poly], fill=(30, 22, 40, 170))
            rim = sorted(poly, key=lambda p: -sgn * p[1])[:3]
            dm.line([(a * SS, b * SS) for a, b in sorted(rim)], fill=(200, 150, 255, 235), width=int(1.5 * SS), joint="curve")
    # arched arcs above the rift
    for _ in range(arcs):
        i0, i1 = sorted(rnd.sample(range(len(main)), 2))
        if i1 - i0 < 15:
            i1 = min(len(main) - 1, i0 + 25)
        a, b = main[i0], main[i1]
        lift = rnd.uniform(6, 14)
        m1 = G.lerp(a, b, 0.33); m2 = G.lerp(a, b, 0.66)
        ctrl = [a, (m1[0], m1[1] - lift), (m2[0], m2[1] - lift * 0.8), b]
        path = []
        for p, q in zip(ctrl, ctrl[1:]):
            path += L.jag(p, q, 0.35, rnd, 4)[:-1]
        path.append(b)
        G.hd_bolt.__globals__  # noqa
        for i_ in range(len(path) - 1):
            tt = i_ / (len(path) - 2)
            w = 1.8 * (0.5 + 0.5 * math.sin(math.pi * tt))
            dl.line([(path[i_][0] * SS, path[i_][1] * SS), (path[i_ + 1][0] * SS, path[i_ + 1][1] * SS)],
                    fill=int(255 * heat), width=max(1, int(w * SS)))
    # sparks rising
    for _ in range(14):
        k = rnd.randrange(len(main)); x, y = main[k]
        y2 = y - rnd.uniform(4, 16); x2 = x + rnd.uniform(-5, 5)
        dl.line([(x * SS, (y - 2) * SS), (x2 * SS, y2 * SS)], fill=int(rnd.uniform(140, 255) * heat), width=max(1, int(0.5 * SS)))
    # plasma: the glow carries a flowing noise texture
    noise = fbm((W, W), seed * 7 + t)
    glow_src = ImageChops.lighter(core, body)
    tight = glow_src.filter(ImageFilter.GaussianBlur(1.6 * SS)).point(lambda v: min(255, int(v * 1.2)))
    mid = glow_src.filter(ImageFilter.GaussianBlur(5 * SS))
    mid = ImageChops.multiply(mid.point(lambda v: min(255, int(v * 2.2))), noise.point(lambda v: 90 + v * 165 // 255))
    pool = G.squashed_blur(glow_src, 13 * SS).point(lambda v: min(255, int(v * 1.6)))
    inten = ImageChops.lighter(ImageChops.lighter(core, body), ImageChops.lighter(tight, ImageChops.lighter(mid, pool)))
    inten = inten.resize((n, n), Image.LANCZOS)
    rgb = Image.merge("RGB", [inten.point([cc[i] for cc in L.STORM_LUT]) for i in range(3)])
    alpha = inten.point(lambda v: min(255, int(255 * (v / 255) ** 0.72 * 1.12)))
    light = rgb.convert("RGBA"); light.putalpha(alpha)
    out = matter.resize((n, n), Image.LANCZOS); out.alpha_composite(light)
    return out


if __name__ == "__main__":
    n = 168; h = n / 2; w = 2 * h
    tiles = [hero(s) for s in (11, 28, 40, 57)]
    W = int(5 * 0.75 * w + w); H = int(4 * h + h)
    img = Image.new("RGBA", (W, H), (52, 64, 44, 255))
    for cc in range(5):
        for r in range(4):
            x = cc * 0.75 * w + w / 2; y = r * h + h / 2 + (h / 2 if cc % 2 else 0)
            rr = random.Random(cc * 7 + r)
            fr = tiles[rr.randrange(2)]
            if rr.random() < .5: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(fr, (int(x - n / 2), int(y - n / 2)))
    img.save("/tmp/hero_patch.png")
    z = Image.new("RGBA", (n, n), (52, 64, 44, 255)); z.alpha_composite(tiles[0]); z.resize((n * 3, n * 3), Image.LANCZOS).save("/tmp/hero_tile.png")
