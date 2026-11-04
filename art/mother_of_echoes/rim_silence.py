#!/usr/bin/env python3
"""The Silence rim-light proposal (art QA 2026-11-04: the pure-black silhouette vanishes on dark boards). Adds a pale
violet/bone rim just inside the silhouette and a faint violet inner glow behind it; alpha is untouched (hard).
    python3 art/mother_of_echoes/rim_silence.py   -> art/mother_of_echoes/exports/avatar_moe_silence_rim.webp
Pillow only. The original avatar_moe_silence.webp stays the wired default until the director approves."""
import os
from PIL import Image, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'exports', 'avatar_moe_silence.webp')
OUT = os.path.join(HERE, 'exports', 'avatar_moe_silence_rim.webp')
RIM, GLOW = (214, 198, 240), (120, 98, 160)

im = Image.open(SRC).convert('RGBA')
a = im.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
k = 23                                       # ~2 px at the in-battle size (1181 px source shown at ~106 px)
inner = a.filter(ImageFilter.MinFilter(k))
rim = ImageChops.subtract(a, inner)
glow = ImageChops.subtract(inner, inner.filter(ImageFilter.MinFilter(k + 8)))
rgb = im.convert('RGB')
out = im.copy()
out.paste(Image.blend(rgb, Image.new('RGB', im.size, GLOW), 0.45), (0, 0), glow)
out.paste(Image.blend(rgb, Image.new('RGB', im.size, RIM), 0.85), (0, 0), rim)
out.putalpha(a)
out.save(OUT, 'WEBP', lossless=True)
print(OUT)
