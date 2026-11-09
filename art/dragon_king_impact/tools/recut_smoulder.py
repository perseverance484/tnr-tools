"""Re-cut the v6l smoulder loop (built at clip ratio 2.5) for hex size 1 at the same scale as the v7b tall pillar
(hv32: 32 composite units per hex row = a 72 px window of the 112 px 2.5 frame), centred on the tile."""
import json, sys, numpy as np
from PIL import Image
SRC = '/mnt/project-files/tnr-animation/v5/out/dragon/anim_dragon_king_v6l_smoulder.webp'
OUT = sys.argv[1]
W, F, S, CELL, EDGE = 112, 24, 112 * 32 / 50, 112, 5
im = np.asarray(Image.open(SRC).convert('RGBA')).astype(np.float32).reshape(F, W, W, 4)
x0 = y0 = (W - S) / 2
frames = []
for t in range(F):
    fr = Image.fromarray(im[t].astype(np.uint8), 'RGBA')
    # premultiplied resize to avoid dark fringes
    p = im[t].copy(); p[..., :3] *= p[..., 3:4] / 255
    rgb = Image.fromarray(np.clip(p, 0, 255).astype(np.uint8), 'RGBA').resize((CELL, CELL), Image.LANCZOS, box=(x0, y0, x0 + S, y0 + S))
    q = np.asarray(rgb).astype(np.float32)
    a = q[..., 3:4]
    q[..., :3] = np.where(a > 0, q[..., :3] * 255 / np.maximum(a, 1), 0)
    e = np.minimum(np.arange(CELL), np.arange(CELL)[::-1]).astype(np.float32) / (EDGE * CELL / S)
    e = np.clip(e, 0, 1); e = e * e * (3 - 2 * e)
    q[..., 3] *= e[None, :] * e[:, None]
    frames.append(np.clip(q, 0, 255).astype(np.uint8))
strip = Image.fromarray(np.concatenate(frames, 0), 'RGBA')
strip.save(OUT, 'WEBP', lossless=True, method=6)
import os
meta = {"file": os.path.basename(OUT), "kind": "loop", "frames": F, "speed": 80, "duration_ms": F * 80, "ratio": 1,
        "hv_units": 32.0, "cell": CELL, "size": list(strip.size), "bytes": os.path.getsize(OUT)}
json.dump(meta, open(OUT[:-5] + '.json', 'w'), indent=1); print(meta)
