#!/usr/bin/env python3
"""Slice the FCF keyframe sheet (keys_sheet.png, 1254 px square, black background) into aligned key poses.

Rows: flame loop x6, whip lash x5, seal tag burn x5, smoke puff x5, ground burst x5. Every key of a row is placed on
one shared canvas at one anchor so the keys stack (flame and burst: base centre; whip: thick end; tag: top centre;
smoke: centre of mass). Writes keys/<kind>_<n>.png and keys/anchors.json (anchor in canvas pixels).
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v20"))
import slice_kit as S  # noqa: E402

ROWS = [("flame", 0, 262, 6, "base"), ("whip", 266, 462, 5, "left"), ("tag", 466, 734, 5, "top"),
        ("smoke", 736, 978, 5, "mass"), ("burst", 980, 1185, 5, "base")]


def key_paper(band):
    light = S.key_light(band)
    r, g, b = band.split()
    lum = ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda v: 0 if v < 60 else min(255, (v - 60) * 3))
    return Image.composite(Image.merge("RGBA", (r, g, b, lum)), light, lum)


def anchor(a, how):
    ys, xs = np.nonzero(a > 60)
    if how == "base":
        y = ys.max()
        low = xs[ys > y - 25]
        return float(np.median(low)), float(y)
    if how == "left":
        x = xs.min()
        return float(x), float(np.median(ys[xs < x + 12]))
    if how == "top":
        y = ys.min()
        return float(np.median(xs[ys < y + 12])), float(y)
    w = a.astype(np.float64)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    return float((xx * w).sum() / w.sum()), float((yy * w).sum() / w.sum())


def main():
    im = Image.open(os.path.join(HERE, "keys_sheet.png")).convert("RGB")
    out = {}
    for kind, y0, y1, n, how in ROWS:
        cw = im.width / n
        cells = []
        for i in range(n):
            cell = im.crop((int(i * cw), y0, int((i + 1) * cw), y1))
            k = key_paper(cell) if kind == "tag" else S.key_light(cell)
            m = Image.new("L", k.size, 0)                 # drop slivers of neighbouring cells at the edges
            m.paste(255, (8, 0, k.width - 8, k.height))
            k.putalpha(ImageChops.multiply(k.getchannel("A"), m))
            cells.append((k, anchor(np.asarray(k)[..., 3], how)))
        # shared canvas: big enough for every key placed at a common anchor
        ax = max(a[0] for _, a in cells)
        ay = max(a[1] for _, a in cells)
        W = int(max(ax - a[0] + k.width for k, a in cells)) + 2
        H = int(max(ay - a[1] + k.height for k, a in cells)) + 2
        for i, (k, a) in enumerate(cells):
            c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            c.alpha_composite(k, (int(round(ax - a[0])), int(round(ay - a[1]))))
            c.save(os.path.join(HERE, "keys", f"{kind}_{i}.png"))
        out[kind] = {"anchor": [ax, ay], "size": [W, H], "keys": n}
    json.dump(out, open(os.path.join(HERE, "keys", "anchors.json"), "w"), indent=1)
    print(out)


if __name__ == "__main__":
    main()
