#!/usr/bin/env python3
"""v7i: the approved v6l Dragon King's Impact, whole and uncut, shrunk uniformly to fit one hex. v6l was drawn for a
2.5-hex square; this takes the same 80-unit square and draws it in one hex (40% size), on the caster (afterburn) and
the target (damage). Only the canvas edges get a short soft fade so nothing ends in a hard line.
    python3 recut_fit.py COMP.npz PREFIX OUT_DIR"""
import json, os, sys
import numpy as np
from PIL import Image
comp, PFX, OUT = sys.argv[1:4]
CELL = 112
S, CX, CY = 80.0, 25.0, 0.0                       # one square for both strips, so the caster and target match in scale
d = np.load(comp); U, OX, OY, MS = [float(v) for v in d["meta"]]
os.makedirs(OUT, exist_ok=True)
ss = lambda v: (lambda c: c * c * (3 - 2 * c))(np.clip(v, 0, 1))


def cut(src):
    A_all, P_all = d[src + "_A"], d[src + "_P"]
    T, H, W = A_all.shape
    xu = (np.arange(W) + .5) / U - OX; yu = (np.arange(H) + .5) / U - OY
    F = (ss((yu + 40) / 5) * ss((44 - yu) / 4))[:, None] * (ss((xu + 10) / 6) * ss((60 - xu) / 6))[None, :]
    xl, y0 = CX - S / 2, CY - S / 2
    PAD = 800
    box = ((xl + OX) * U + PAD, (y0 + OY) * U + PAD, (xl + S + OX) * U + PAD, (y0 + S + OY) * U + PAD)
    out = []
    for t in range(T):
        a = np.pad(A_all[t].astype(np.float32) * F, PAD)
        p = np.pad(P_all[t].astype(np.float32) * F[..., None], ((PAD, PAD), (PAD, PAD), (0, 0)))
        ia = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8), "L").resize((CELL, CELL), Image.BOX, box=box)
        ip = Image.fromarray(np.clip(p * 255, 0, 255).astype(np.uint8), "RGB").resize((CELL, CELL), Image.BOX, box=box)
        Ad = np.asarray(ia, np.float32) / 255; Pd = np.asarray(ip, np.float32) / 255
        C = Pd / np.maximum(Ad[..., None], 1e-6); Ad[Ad < 2 / 255] = 0
        o = np.zeros((CELL, CELL, 4), np.uint8)
        o[..., :3] = np.clip(C * 255 + .5, 0, 255); o[..., 3] = np.clip(Ad * 255 + .5, 0, 255)
        out.append(Image.fromarray(o, "RGBA"))
    out[-1] = Image.new("RGBA", (CELL, CELL))
    return out


made = []
for src, slot in (("hero", "c0"), ("cast", "cast_c0")):
    fr = cut(src)
    name = f"{PFX}{slot}.webp"; p = os.path.join(OUT, name)
    strip = Image.new("RGBA", (CELL, CELL * len(fr)))
    for i, f in enumerate(fr): strip.alpha_composite(f, (0, i * CELL))
    strip.save(p, "WEBP", lossless=True, quality=100, method=6)
    meta = dict(file=name, kind="appear", frames=len(fr), speed=int(MS), duration_ms=len(fr) * int(MS), ratio=1,
                window_units=S, centre=[CX, CY], cell=CELL, size=list(strip.size), bytes=os.path.getsize(p))
    assert meta["bytes"] <= 450 * 1024, meta
    json.dump(meta, open(p.replace(".webp", ".json"), "w"), indent=1)
    made.append(dict(slot=slot, row=0, frames=len(fr), bytes=meta["bytes"]))
json.dump(made, open(os.path.join(OUT, f"{PFX}slots.json"), "w"), indent=1)
print(made)
