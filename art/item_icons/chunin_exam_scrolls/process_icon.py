#!/usr/bin/env python3
"""Process a Chunin Exam scroll raw into its item icon: clean alpha, trim, pad square with a margin, 256 px lossless.

    python3 process_icon.py <raw.png> <out.webp>
"""
import sys
from PIL import Image
raw, out = sys.argv[1:3]
im = Image.open(raw).convert('RGBA')
r, g, b, a = im.split()
a = a.point(lambda v: 0 if v <= 24 else (255 if v >= 232 else v))   # stray near-zero alpha off, near-opaque subject solid
im = Image.merge('RGBA', (r, g, b, a))
im = im.crop(a.getbbox())
side = round(max(im.size) / 0.95)                                     # ~2.5% margin each side so the rarity frame reads
canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
canvas.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
canvas = canvas.resize((256, 256), Image.LANCZOS)
r, g, b, a = canvas.split()                                          # resampling softens the edge; firm it up
canvas = Image.merge('RGBA', (r, g, b, a.point(lambda v: 0 if v < 80 else (255 if v > 175 else v))))
canvas.save(out, 'WEBP', lossless=True, quality=100, method=6)
print(out, canvas.size, 'trimmed', im.size)
