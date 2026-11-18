#!/usr/bin/env python3
"""Re-cut combat strips so frame_px x frames <= 4096 (2026-11-17).

Battle clips are one-column strips loaded as one WebGL texture (assetAnimationClip, columns 1). Off-Bunny hosts
(the director's own UploadThing, bbenpyo9uu.ufs.sh) skip the game's 50 px rendition and load native, and combat
effects have no MAX_TEXTURE_SIZE guard (character sheets do). Phones commonly cap textures at 4096 px, so a taller
strip draws as a black box. Each frame is resampled (LANCZOS) to the largest size that fits; frame count and timing
are unchanged.

    python3 art/duelyst_fx/recut_4096.py
"""
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LIMIT = 4096
JOBS = [  # source, output stem
    ('rengoku/final/anim_rengoku_strike_tight_300_b.webp', 'rengoku/final/anim_rengoku_strike_tight_{px}_c.webp'),
    ('rengoku/final/anim_rengoku_smoulder_tight_300_b.webp', 'rengoku/final/anim_rengoku_smoulder_tight_{px}_c.webp'),
    ('showcase/final/anim_white_tiger_gates_234.webp', 'showcase/final/anim_white_tiger_gates_{px}.webp'),
    ('showcase/final/anim_white_tiger_tiger_252.webp', 'showcase/final/anim_white_tiger_tiger_{px}.webp'),
]
for src, out in JOBS:
    im = Image.open(os.path.join(HERE, src)).convert('RGBA')
    w, h = im.size
    n = h // w
    assert w * n == h, src
    px = LIMIT // n
    px -= px % 2
    sheet = Image.new('RGBA', (px, px * n), (0, 0, 0, 0))
    for i in range(n):
        sheet.paste(im.crop((0, i * w, w, (i + 1) * w)).resize((px, px), Image.LANCZOS), (0, i * px))
    p = os.path.join(HERE, out.format(px=px))
    sheet.save(p, 'WEBP', lossless=True, method=6)
    print(f'{os.path.relpath(p, HERE)}: {n} frames x {px} px = {px * n} px tall, {os.path.getsize(p)} bytes')
