#!/usr/bin/env python3
"""Dump the full-resolution v6l composite (alpha + premultiplied rgb, in frame units) for every frame, so it can be
re-cut for the engine's live effect size (1 hex height per square frame) instead of v6l's 2.5.
    python3 dump_v6l_composite.py OUT.npz"""
import os, sys
import numpy as np
V5 = "/mnt/project-files/tnr-animation/v5"
sys.path.insert(0, V5); os.chdir(V5)
import build_dragon_v6l as L
from build_dragon_v6l import cel, btc, U, OX, OY

def comp(self):
    if self.soft_base:
        rgb = 1 - np.exp(-1.35 * self.energy())
        A = rgb.max(2); Pm = rgb.copy()
        if self.extra is not None and self.extra.max() > 0:
            Pc, Ac = cel(np.clip(self.extra, 0, 1))
            Pm = Pc + Pm * (1 - Ac[..., None]); A = Ac + A * (1 - Ac)
    else:
        rgb = (1 - np.exp(-1.35 * self.energy())) ** 1.8
        if self.extra is not None: rgb = 1 - (1 - rgb) * (1 - np.clip(self.extra, 0, 1))
        Pm, A = cel(rgb)
    ia = np.asarray(self.ink.filter(btc.ImageFilter.GaussianBlur(self.ink_soft * U)), float) / 255 * .92
    Pm = Pm + self.ink_rgb * ia[..., None] * (1 - A[..., None]); A = A + ia * (1 - A)
    if self.over is not None:
        Po, ao = self.over
        Pm = Po + Pm * (1 - ao[..., None]); A = ao + A * (1 - ao)
    if self.paint is not None:
        Lp = np.clip(self.paint, 0, 1)
        la = np.clip(self.paint_a, 0, 1) if getattr(self, "paint_a", None) is not None else Lp.max(2)
        Pm = Lp + Pm * (1 - la[..., None]); A = la + A * (1 - la)
    ys = np.arange(self.H) / U - OY
    fy = np.clip(np.minimum(ys - self.top, self.bot - ys) / 6, 0, 1) ** 1.3   # keep v6l's top/bottom fade, drop its 50-unit side clip
    A = A * fy[:, None]; Pm = Pm * fy[:, None, None]
    return {"A": A, "Pm": Pm}

L.PCel.slices = comp
out = {}
for name, fn, n in (("hero", L.hero, L.bdk.N), ("cast", L.launcher, 19)):
    As, Ps = [], []
    for i in range(n):
        c = fn(i).slices(); As.append(c["A"].astype(np.float16)); Ps.append(c["Pm"].astype(np.float16))
        print(name, i, c["A"].shape, flush=True)
    out[name + "_A"] = np.stack(As); out[name + "_P"] = np.stack(Ps)
out["meta"] = np.array([U, OX, OY, L.bdk.MS])
np.savez_compressed(sys.argv[1], **out)
print("saved", sys.argv[1])
