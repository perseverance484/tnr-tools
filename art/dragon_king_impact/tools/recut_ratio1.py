#!/usr/bin/env python3
"""Re-cut Dragon King's Impact v6l for the live engine's effect size: every effect frame is drawn square, ONE hex
height tall, centred on its tile (libs/rendering/animation.ts EFFECT_ANIMATION_HEX_RATIO = 1, scenes/combatEffects.ts).
Tiles in one column sit exactly one hex height apart, so square windows of one virtual hex height (HV composite
units), stacked with no overlap, join seamlessly in game. A tile is only half a hex wide, so anything wider than HV
is softly faded at the sides.
    python3 recut_ratio1.py COMP.npz HV PREFIX OUT_DIR"""
import json, os, sys
import numpy as np
from PIL import Image
comp, HV, PFX, OUT = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
CELL = 112
EDGE = float(sys.argv[5]) if len(sys.argv) > 5 else 7.0                       # px per frame; side fade width in composite units
d = np.load(comp); U, OX, OY, MS = [float(v) for v in d["meta"]]
os.makedirs(OUT, exist_ok=True)
NM = {-3: "n3", -2: "n2", -1: "n1", 0: "c0", 1: "p1"}


def cut(A, P, j):
    T, H, W = A.shape
    y0 = (25 + HV * (j - .5) + OY) * U; x0 = (25 - HV / 2 + OX) * U; s = HV * U
    xu = (np.arange(W) + .5) / U - OX - (25 - HV / 2)              # 0..HV across the tile, composite space
    fx = np.clip(np.minimum(xu, HV - xu) / EDGE, 0, 1)
    fx = fx * fx * (3 - 2 * fx)                                    # smooth sides: the tile ends at half a hex width
    PAD = 400                                                      # the top row can start above the composite
    box = (x0, y0 + PAD, x0 + s, y0 + PAD + s)                     # exact float window: rows meet with no seam
    frames = []
    for t in range(T):
        a = np.pad(A[t].astype(np.float32) * fx[None, :], ((PAD, PAD), (0, 0)))
        p = np.pad(P[t].astype(np.float32) * fx[None, :, None], ((PAD, PAD), (0, 0), (0, 0)))
        ia = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8), "L").resize((CELL, CELL), Image.BOX, box=box)
        ip = Image.fromarray(np.clip(p * 255, 0, 255).astype(np.uint8), "RGB").resize((CELL, CELL), Image.BOX, box=box)
        Ad = np.asarray(ia, np.float32) / 255; Pd = np.asarray(ip, np.float32) / 255
        C = Pd / np.maximum(Ad[..., None], 1e-6); Ad[Ad < 2 / 255] = 0
        o = np.zeros((CELL, CELL, 4), np.uint8)
        o[..., :3] = np.clip(C * 255 + .5, 0, 255); o[..., 3] = np.clip(Ad * 255 + .5, 0, 255)
        frames.append(Image.fromarray(o, "RGBA"))
    frames[-1] = Image.new("RGBA", (CELL, CELL))
    return frames


def write(frames, name):
    strip = Image.new("RGBA", (CELL, CELL * len(frames)))
    for i, f in enumerate(frames): strip.alpha_composite(f, (0, i * CELL))
    p = os.path.join(OUT, name); strip.save(p, "WEBP", lossless=True, quality=100, method=6)
    meta = dict(file=name, kind="appear", frames=len(frames), speed=int(MS), duration_ms=len(frames) * int(MS), ratio=1,
                hv_units=HV, cell=CELL, size=list(strip.size), bytes=os.path.getsize(p))
    assert meta["size"][1] <= 4096 and meta["bytes"] <= 450 * 1024, meta
    json.dump(meta, open(p.replace(".webp", ".json"), "w"), indent=1)
    return meta


made = []
for src, pre in (("hero", ""), ("cast", "cast_")):
    A, P = d[src + "_A"], d[src + "_P"]
    m = A.astype(np.float32).max(axis=(0, 2)) > 2 / 255
    ys = np.arange(A.shape[1]) / U - OY
    top, bot = ys[m].min(), ys[m].max()
    rows = range(int(np.floor((top - 25) / HV + .5)), int(np.floor((bot - 25) / HV + .5)) + 1)
    for j in rows:
        fr = cut(A, P, j)
        if max(np.asarray(f)[..., 3].max() for f in fr) == 0: continue
        meta = write(fr, f"{PFX}{pre}{NM[j]}.webp"); made.append((pre + NM[j], j, meta["frames"], meta["bytes"]))
json.dump([dict(slot=s, row=j, frames=n, bytes=b) for s, j, n, b in made], open(os.path.join(OUT, f"{PFX}slots.json"), "w"), indent=1)
print(made)
