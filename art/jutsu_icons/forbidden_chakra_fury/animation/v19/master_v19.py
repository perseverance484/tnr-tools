#!/usr/bin/env python3
"""FCF v19 MASTER: built from the director's painted art, in board space (2026-11-22).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v19/master_v19.py

Usable from the painted set (raws/): the three seals, the two bolts and the aftermath smoke. Not used: the three
auras (each has a person-shaped hole, and the game's fighter sprite cannot be located or matched - learned on White
Tiger), and the column (its opaque core would bury the fighter).
Shot: the forbidden seal ignites under the user (dim -> blazing), the area darkens; at the release the seal cracks
with an inverted impact frame and the painted bolts lash out to the whole area over ~260 ms, each with its own
shoot / land / afterglow / restrike / die; chakra smoke rises from the broken seal as it ends.
Black backgrounds are turned into alpha by brightness (glow keeps its colour). Writes master_fcf_v19.gif.
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v18"))
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import master_v18 as M  # noqa: E402
import board_v10 as BV  # noqa: E402

W, H, TW, TH, SRC = M.W, M.H, M.TW, M.TH, M.SRC
STEP = 25


def key_black(path):
    """Black background -> alpha. alpha = brightest channel; colour un-premultiplied so the glow keeps its hue."""
    im = Image.open(path).convert("RGB")
    r, g, b = im.split()
    a = ImageChops.lighter(ImageChops.lighter(r, g), b)
    a = a.point(lambda v: 0 if v < 10 else min(255, int((v - 10) * 1.08)))
    def un(c):
        return Image.merge("L", [Image.eval(c, lambda v: v)]) if False else c
    rgba = Image.merge("RGBA", (r, g, b, a))
    px = rgba.load()
    w, h = rgba.size
    out = Image.new("RGBA", (w, h))
    po = out.load()
    for y in range(h):
        for x in range(w):
            R, G, B, A = px[x, y]
            if A:
                k = 255 / max(R, G, B, 1)
                po[x, y] = (min(255, int(R * k)), min(255, int(G * k)), min(255, int(B * k)), A)
    return out.crop(out.getbbox())


def fit(im, w, h):
    return im.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS)


def alpha_mul(im, k):
    if k >= 1:
        return im
    out = im.copy()
    out.putalpha(im.getchannel("A").point(lambda v: int(v * max(0.0, k))))
    return out


def main(seed=21):
    rnd = random.Random(seed)
    cache = os.path.join(HERE, "keyed")
    os.makedirs(cache, exist_ok=True)
    art = {}
    for n in ("seal_dim", "seal_blazing", "seal_cracking", "bolt_a", "bolt_b", "aftermath_smoke"):
        p = os.path.join(cache, n + ".png")
        if not os.path.exists(p):
            key_black(os.path.join(HERE, "raws", n + ".png")).save(p)
        art[n] = Image.open(p)
    cx, cy = M.CX, M.CY + 0.4 * TH                    # seal on the ground under the user
    sw = TW * 2.6                                       # the seal spans the user's hex and reaches into the ring
    seals = {k: fit(v, sw, sw * v.height / v.width) for k, v in art.items() if k.startswith("seal")}
    smoke = fit(art["aftermath_smoke"], TW * 3.4, TW * 3.4 * art["aftermath_smoke"].height / art["aftermath_smoke"].width)
    # bolts: aimed at area tiles spread over the circle (8 sectors guaranteed), launched over 260 ms
    tiles = [k for k in M.AREA if BV.dist(k, M.CASTER) >= 3]
    rnd.shuffle(tiles)
    chosen = []
    for sec in range(8):
        for k in tiles:
            x, y = M.TILES[k]
            a = math.atan2(y - SRC[1], x - SRC[0])
            if int(((a + math.pi / 8) % (2 * math.pi)) // (math.pi / 4)) == sec and k not in chosen:
                chosen.append(k)
                break
    for k in tiles:
        if len(chosen) >= 16:
            break
        if k not in chosen:
            chosen.append(k)
    bolts = []
    for k in chosen:
        x, y = M.TILES[k]
        src = art["bolt_a" if rnd.random() < 0.5 else "bolt_b"]
        L_ = math.hypot(x - SRC[0], y - SRC[1]) * 1.12          # streak a little past the tile
        th = TH * rnd.uniform(1.6, 2.2)
        img = fit(src, L_, th)
        if rnd.random() < 0.5:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        ang = -math.degrees(math.atan2(y - SRC[1], x - SRC[0]))
        bolts.append((rnd.uniform(0, 260), img, ang, rnd.random() < 0.5))
    shots = []
    for t in range(-350, 900, STEP):
        night = max(0.0, min(1.0, (t + 350) / 200)) * (1.0 if t < 600 else max(0, 1 - (t - 600) / 250))
        base = _board(night, invert=0 <= t < STEP)
        # the seal: dim and growing, blazing at the release, cracking just after, fading out
        if t < -120:
            s, k, grow = seals["seal_dim"], (t + 350) / 230, 0.6 + 0.4 * (t + 350) / 230
        elif t < 75:
            s, k, grow = seals["seal_blazing"], 1.0, 1.0
        elif t < 500:
            s, k, grow = seals["seal_cracking"], 1.0 if t < 300 else 1 - (t - 300) / 200, 1.0
        else:
            s = None
        if s is not None:
            g = fit(s, s.width * grow, s.height * grow)
            if 0 <= t < 75:
                g = alpha_mul(g, 1.0)
            base.alpha_composite(alpha_mul(g, k), (int(cx - g.width / 2), int(cy - g.height / 2)))
        for launch, img, ang, two in bolts:
            ph = t - launch
            if ph < 0:
                continue
            i = int(ph // 50)
            beats = ["shoot", "land", "glow", "dark", "re", "die"] if two else ["shoot", "land", "glow", "die"]
            if i >= len(beats):
                continue
            beat = beats[i]
            g = img
            if beat == "shoot":                      # revealed from the user outward, on twos
                frac = 0.5 if ph % 50 < 25 else 0.85
                mask = Image.new("L", img.size, 0)
                edge = int(img.width * frac)
                ImageDraw.Draw(mask).rectangle((0, 0, edge, img.height), fill=255)
                mask = mask.filter(ImageFilter.GaussianBlur(max(2, img.width * 0.06)))   # a soft leading edge
                g = img.copy()
                g.putalpha(ImageChops.multiply(img.getchannel("A"), mask))
            g = alpha_mul(g, {"shoot": 1.0, "land": 1.0, "glow": 0.55, "dark": 0.18, "re": 0.95, "die": 0.25}[beat])
            if beat == "land":                        # the impact frame of each bolt: brighter, a hair thicker
                g = g.resize((g.width, int(g.height * 1.15)), Image.LANCZOS)
            r = g.rotate(ang, Image.BICUBIC, expand=True)
            # the bolt's left end (its start) sits on the body: offset the rotated image from its centre
            L_ = img.width
            mx = SRC[0] + math.cos(math.radians(-ang)) * L_ / 2
            my = SRC[1] + math.sin(math.radians(-ang)) * L_ / 2
            base.alpha_composite(r, (int(mx - r.width / 2), int(my - r.height / 2)))
        if t >= 300:                                  # chakra smoke off the broken seal
            u = (t - 300) / 600
            k = min(1.0, u * 3) * (1 - u)
            g = alpha_mul(smoke, k * 0.9)
            base.alpha_composite(g, (int(cx - g.width / 2), int(cy - g.height * 0.82 - u * TH * 0.6)))
        shots.append(base.convert("RGB"))
    shots[0].save(os.path.join(HERE, "master_fcf_v19.gif"), save_all=True, append_images=shots[1:], duration=STEP,
                  loop=0, optimize=True)
    picks = [-250, -40, 25, 100, 200, 450]
    times = list(range(-350, 900, STEP))
    sheet = Image.new("RGB", (W, H * len(picks)))
    for i, x in enumerate(picks):
        sheet.paste(shots[next(j for j, tt in enumerate(times) if tt >= x)], (0, i * H))
    sheet.save(os.path.join(HERE, "master_stills_v19.png"))


def _board(night, invert=False):
    base = Image.new("RGBA", (W, H), (52, 64, 44, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in M.TILES.values():
        d.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                   (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], outline=(255, 255, 255, 30))
    for k, col in (((8, 3), (96, 58, 52, 255)), ((2, 5), (96, 58, 52, 255)), ((6, 7), (96, 58, 52, 255)),
                   (M.CASTER, (52, 50, 66, 255))):
        x, y = M.TILES[k]
        feet, top = y + 0.4 * TH, y - 1.2 * TH
        d.ellipse((x - TW * 0.16, feet - TH * 0.09, x + TW * 0.16, feet + TH * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((x - TW * 0.085, top + TW * 0.16, x + TW * 0.085, feet - 3), radius=6, fill=col)
        d.ellipse((x - TW * 0.1, top, x + TW * 0.1, top + TW * 0.2), fill=col)
    if night:
        m = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(m)
        for k in M.AREA + [M.CASTER]:
            x, y = M.TILES[k]
            md.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                        (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(8))
        dark = Image.new("RGBA", (W, H), (6, 2, 14, 0))
        dark.putalpha(m.point(lambda v: int(v * night * (0.92 if invert else 0.62))))
        base.alpha_composite(dark)
    return base


if __name__ == "__main__":
    main()
