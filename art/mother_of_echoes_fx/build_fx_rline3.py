#!/usr/bin/env python3
"""The Saint's Act III v2 lines (Black Refraction marks; Lucid Black Refraction, Black Facet, Black Facet Breaks payoffs):
the approved Refraction line (anim_moe_rbreak_*/rmark_*_a6, director 10/10), the same drawing and timing, recoloured
into the Remainder's material (SAYO_BIBLE.md 5.1, Act III): every colour mapped by luminance onto the obsidian / teal
vein ramp, white kept for the hold. Same per-column slices, so the line stays exact on the Saint's wall lines.

    python3 art/mother_of_echoes_fx/build_fx_rline3.py      # writes exports/anim_moe_{rbreak3,rmark3}_{l,r}{col}_a14.webp
"""
import glob
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORTS = os.path.join(HERE, "exports")
RAMP = [(8, 10, 15), (18, 23, 30), (20, 42, 51), (39, 50, 60), (47, 92, 106), (146, 182, 191), (200, 250, 255),
        (255, 255, 250)]


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def remap(img):
    px = img.load()
    cache = {}
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            k = (r, g, b)
            if k not in cache:
                L = lum(k)
                if L > 245:
                    cache[k] = RAMP[7]
                else:   # luminance 0..245 onto the ramp's first seven steps, the ramp itself rising in luminance
                    cache[k] = RAMP[min(6, int(L / 245 * 7))]
            px[x, y] = (*cache[k], a)
    return img


def main():
    n = 0
    for src in sorted(glob.glob(os.path.join(EXPORTS, "anim_moe_r*_[lr]*_a6.webp"))):
        base = os.path.basename(src)
        kind = "rbreak3" if "rbreak" in base else "rmark3"
        side_col = base.split("_")[3]
        out = os.path.join(EXPORTS, f"anim_moe_{kind}_{side_col}_a14.webp")
        remap(Image.open(src).convert("RGBA")).save(out, lossless=True, quality=100, method=6)
        n += 1
    print(n, "strips")


if __name__ == "__main__":
    main()
