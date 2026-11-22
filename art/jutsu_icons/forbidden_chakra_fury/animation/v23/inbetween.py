#!/usr/bin/env python3
"""Bake the FCF key poses into smooth sequences by optical-flow inbetweening (prototype: OpenCV + NumPy).

For each pair of keys, dense flow is solved both ways on the alpha-weighted brightness; each inbetween warps key A
forward and key B backward by the fraction t and cross-dissolves them, with t eased so the motion settles into each
key. Writes seq/<kind>_<nnn>.png (same canvas and anchor as keys/), seq/index.json.
"""
import json
import os

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = {"flame": 10, "whip": 8, "tag": 8, "smoke": 10, "burst": 8}
CYCLIC = {"flame"}


def load(kind, i):
    return np.asarray(Image.open(os.path.join(HERE, "keys", f"{kind}_{i}.png")).convert("RGBA")).astype(np.float32) / 255


def gray(x):
    return np.clip(x[..., :3].max(2) * x[..., 3] * 255, 0, 255).astype(np.uint8)


def flows(a, b):
    ga, gb = gray(a), gray(b)
    p = dict(pyr_scale=0.5, levels=5, winsize=31, iterations=6, poly_n=7, poly_sigma=1.5, flags=0)
    return cv2.calcOpticalFlowFarneback(ga, gb, None, **p), cv2.calcOpticalFlowFarneback(gb, ga, None, **p)


def inbetween(a, b, fab, fba, t):
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    s = t * t * (3 - 2 * t)                      # ease the dissolve so each key holds its shape longest
    wa = cv2.remap(a, xx - fab[..., 0] * t, yy - fab[..., 1] * t, cv2.INTER_LINEAR)
    wb = cv2.remap(b, xx - fba[..., 0] * (1 - t), yy - fba[..., 1] * (1 - t), cv2.INTER_LINEAR)
    return wa * (1 - s) + wb * s


def main():
    os.makedirs(os.path.join(HERE, "seq"), exist_ok=True)
    meta = json.load(open(os.path.join(HERE, "keys", "anchors.json")))
    index = {}
    for kind, steps in STEPS.items():
        n = meta[kind]["keys"]
        keys = [load(kind, i) for i in range(n)]
        pairs = list(range(n if kind in CYCLIC else n - 1))
        out = []
        for i in pairs:
            a, b = keys[i], keys[(i + 1) % n]
            fab, fba = flows(a, b)
            for s in range(steps):
                out.append(inbetween(a, b, fab, fba, s / steps))
        if kind not in CYCLIC:
            out.append(keys[-1])
        for j, f in enumerate(out):
            Image.fromarray(np.clip(f * 255, 0, 255).astype(np.uint8), "RGBA").save(
                os.path.join(HERE, "seq", f"{kind}_{j:03d}.png"))
        index[kind] = {"frames": len(out), "cyclic": kind in CYCLIC, **meta[kind]}
        print(kind, len(out))
    json.dump(index, open(os.path.join(HERE, "seq", "index.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
