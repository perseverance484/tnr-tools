#!/usr/bin/env python3
"""Slice the director's FCF sprite kit (kit/*.png, black backgrounds) into separate keyed sprites (2026-11-22).

    python3 .../v20/slice_kit.py

Light sprites (glow, lightning, flame, smoke, seal): alpha = brightest channel, colour un-premultiplied, so the glow
keeps its hue over any ground. Matter sprites (debris): near-opaque mask, colour kept. Items are found as connected
blobs of a dilated mask (Pillow only), so pieces with gaps (spark clusters, dashed rings) stay one sprite.
Writes sprites/<kind>_<nn>.png and sprites_contact.png.
"""
import os

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
KIT, OUT = os.path.join(HERE, "kit"), os.path.join(HERE, "sprites")
SHEETS = {  # file, kind, dilation px (at 1/4 scale), matter
    "01_seal_parts.png": ("seal", 1, False), "02_seal_shards.png": ("shard", 2, False),
    "03_lightning_bolts.png": ("bolt", 2, False), "04_lightning_forks.png": ("fork", 3, False),
    "05_sparks.png": ("spark", 4, False), "06_chakra_flame_tongues.png": ("flame", 3, False),
    "07_smoke_puffs.png": ("smoke", 4, False), "08_chakra_motes.png": ("mote", 3, False),
    "09_flashes.png": ("flash", 6, False), "10_shockwave_rings.png": ("ring", 5, False),
    "11_debris.png": ("debris", 3, True),
}


def key_light(im):
    r, g, b = im.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    a = m.point(lambda v: 0 if v < 8 else min(255, int((v - 8) * 1.06)))
    # un-premultiply: scale colour so its brightest channel is 255 where there is any alpha
    k = m.point(lambda v: 0 if v < 8 else min(255, int(255 * 255 / max(v, 1)) // 255 * 0 + v))
    out = Image.merge("RGBA", (r, g, b, a))
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            R, G, B, A = px[x, y]
            if A:
                s = 255 / max(R, G, B, 1)
                px[x, y] = (min(255, int(R * s)), min(255, int(G * s)), min(255, int(B * s)), A)
    return out


def key_matter(im):
    r, g, b = im.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    a = m.point(lambda v: 0 if v < 6 else min(255, (v - 6) * 14))
    return Image.merge("RGBA", (r, g, b, a))


def blobs(alpha, dil):
    small = alpha.resize((alpha.width // 4, alpha.height // 4), Image.BILINEAR).point(lambda v: 255 if v > 24 else 0)
    for _ in range(dil):
        small = small.filter(ImageFilter.MaxFilter(3))
    lab = small.copy()
    boxes = []
    px = lab.load()
    w, h = lab.size
    n = 0
    for y in range(h):
        for x in range(w):
            if px[x, y] == 255:
                n += 1
                ImageDraw.floodfill(lab, (x, y), 100)
                bb = lab.point(lambda v: 255 if v == 100 else 0).getbbox()
                ImageDraw.floodfill(lab, (x, y), 1)
                if bb and (bb[2] - bb[0]) * (bb[3] - bb[1]) > 6:
                    boxes.append(tuple(c * 4 for c in bb))
    return boxes


def main():
    os.makedirs(OUT, exist_ok=True)
    tiles = []
    for fn, (kind, dil, matter) in SHEETS.items():
        im = Image.open(os.path.join(KIT, fn)).convert("RGB")
        keyed = key_matter(im) if matter else key_light(im)
        if kind == "seal":          # the rings' glows touch: fixed cells (outer, runes, inner, star, 8 spokes)
            xs = [0, 445, 895, 1165, 1536]
            boxes = [(xs[i], 40, xs[i + 1], 540) for i in range(4)]
            sx = [0, 190, 375, 585, 775, 935, 1110, 1310, 1536]
            boxes += [(sx[i], 560, sx[i + 1], 920) for i in range(8)]
        elif kind == "bolt":          # one bolt per row: split at the darkest horizontal bands
            a = keyed.getchannel("A")
            rows = [sum(a.crop((0, y, a.width, y + 1)).getdata()) for y in range(a.height)]
            step = a.height / 8
            cuts = [0] + [min(range(int(step * k - step * 0.3), int(step * k + step * 0.3)), key=lambda y: rows[y])
                          for k in range(1, 8)] + [a.height]
            boxes = [(0, cuts[k], a.width, cuts[k + 1]) for k in range(8)]
        else:
            boxes = sorted(blobs(keyed.getchannel("A"), dil), key=lambda b: (b[1] // 120, b[0]))
        for i, bb in enumerate(boxes):
            pad = 6
            bb = (max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad))
            spr = keyed.crop(bb)
            spr = spr.crop(spr.getbbox() or (0, 0, 1, 1))
            spr.save(os.path.join(OUT, f"{kind}_{i:02d}.png"))
            tiles.append((f"{kind}_{i:02d}", spr))
        print(f"{kind}: {len(boxes)}")
    cell = 96
    cols = 16
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell, rows * cell), (40, 48, 40, 255))
    d = ImageDraw.Draw(sheet)
    for i, (name, spr) in enumerate(tiles):
        s = spr.copy()
        s.thumbnail((cell - 6, cell - 16))
        x, y = (i % cols) * cell, (i // cols) * cell
        sheet.alpha_composite(s, (x + (cell - s.width) // 2, y + 12 + (cell - 16 - s.height) // 2))
        d.text((x + 2, y + 1), name, fill=(255, 255, 255, 200))
    sheet.save(os.path.join(HERE, "sprites_contact.png"))


if __name__ == "__main__":
    main()
