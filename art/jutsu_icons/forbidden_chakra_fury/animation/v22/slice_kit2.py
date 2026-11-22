#!/usr/bin/env python3
"""Slice the second FCF kit sheet (kit/12_tags_whips.png, 1254 px square, black background) (2026-11-22).

Rows: 8 seal tags (4 intact, 4 burning), 16 ash scraps, 8 seal-script cracks, 8 chakra whips (two rows of 4),
6 whip-crack bursts. Tags and ash are paper (matter key: near-opaque, colour kept, so the dark brush marks stay);
the rest are light (alpha from brightness, colour un-premultiplied). Writes sprites/<kind>_<nn>.png.
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v20"))
import slice_kit as S  # noqa: E402

ROWS = [  # kind, y0, y1, cells (None = find blobs), matter
    ("tag", 10, 290, 8, True), ("ash", 292, 400, None, True), ("crack", 405, 540, 8, False),
    ("whip", 540, 765, 4, False), ("whip", 765, 995, 4, False), ("burst", 995, 1200, 6, False),
]


def main():
    im = Image.open(os.path.join(HERE, "kit", "12_tags_whips.png")).convert("RGB")
    counts = {}
    for kind, y0, y1, cells, matter in ROWS:
        band = im.crop((0, y0, im.width, y1))
        if matter:     # paper: solid where it is paper, the violet glow round it stays see-through light
            light = S.key_light(band)
            paper = S.key_matter(band).getchannel("A").point(lambda v: 0 if v < 200 else 255)
            r, g, b = band.split()
            from PIL import ImageChops as C
            lum = C.lighter(C.lighter(r, g), b).point(lambda v: 0 if v < 60 else min(255, (v - 60) * 3))
            keyed = Image.composite(Image.merge("RGBA", (r, g, b, lum)), light, lum)
        else:
            keyed = S.key_light(band)
        if cells:
            w = im.width / cells
            boxes = [(int(i * w), 0, int((i + 1) * w), band.height) for i in range(cells)]
        else:
            boxes = sorted(S.blobs(keyed.getchannel("A"), 2), key=lambda b: b[0])
        for bb in boxes:
            spr = keyed.crop(bb)
            bbox = spr.getbbox()
            if not bbox:
                continue
            spr = spr.crop(bbox)
            n = counts.get(kind, 0)
            counts[kind] = n + 1
            spr.save(os.path.join(HERE, "sprites", f"{kind}_{n:02d}.png"))
    print(counts)


if __name__ == "__main__":
    main()
