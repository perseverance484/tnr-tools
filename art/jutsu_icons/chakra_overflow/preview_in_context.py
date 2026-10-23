#!/usr/bin/env python3
"""Show Chakra Overflow candidates the way players see them (theninjarpg 107d7a8).

    python3 art/jutsu_icons/chakra_overflow/preview_in_context.py OUT.png CAND [CAND ...]

Sizes come from the battle screen source, not guesses:
  - default action grid: tiles at least 7rem (112 px) wide, labels shown, rounded-xl corners, 2 px border
    (combat/page.tsx:101-105, CombatActions.tsx:315, ContentImage.tsx:103,128);
  - small-actions mode: grid-cols-7 on mobile (about 45 px tiles on a 360 px screen) and grid-cols-9 on desktop
    (about 70 px), gap-1 (combat/page.tsx:102);
  - jutsu lists draw a 28 px level badge on the bottom-left corner and a count badge bottom-right
    (CombatActions.tsx:330-339), so those corners must not carry the emblem.
Rows per candidate: in a mobile battle bar between approved icons, in a desktop bar, a 112 px tile with a level
badge, a 32 px chip, and a silhouette test (grayscale, blurred) that shows whether the shape survives without color.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
NEIGHBORS = sorted(glob.glob(os.path.join(ROOT, 'art/jutsu_icons/starter/exports/*.webp')))[:3] + \
    sorted(glob.glob(os.path.join(ROOT, 'art/jutsu_icons/scroll_jutsu/exports/*.webp')))[:3]
BG = (15, 23, 42)       # slate-900 panel
BORDER = (148, 163, 184)


def tile(im, px, label=None, badge=None):
    radius = max(3, round(px * 12 / 112))   # rounded-xl is 0.75rem at a 112 px tile
    t = im.convert('RGB').resize((px, px), Image.LANCZOS)
    mask = Image.new('L', (px, px), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, px - 1, px - 1], radius, fill=255)
    out = Image.new('RGB', (px, px + (16 if label else 0)), BG)
    out.paste(t, (0, 0), mask)
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([0, 0, px - 1, px - 1], radius, outline=BORDER, width=2)
    if badge:
        r = 14
        d.ellipse([0, px - 2 * r, 2 * r, px], fill=(203, 213, 225), outline=(220, 38, 38), width=2)
        d.text((r - 4, px - r - 6), badge, fill=(0, 0, 0))
    if label:
        d.text((2, px + 2), label, fill=(226, 232, 240))
    return out


def bar(cand, px, n=7):
    icons = [Image.open(p) for p in NEIGHBORS][: n - 1]
    icons.insert(len(icons) // 2, cand)
    w = n * px + (n - 1) * 4
    out = Image.new('RGB', (w + 8, px + 8), BG)
    for i, im in enumerate(icons):
        out.paste(tile(im, px), (4 + i * (px + 4), 4))
    return out


def silhouette(cand, px=64):
    g = ImageOps.grayscale(cand.convert('RGB')).resize((px, px), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5))
    return ImageOps.autocontrast(g).convert('RGB')


def main(out_path, cands):
    rows = []
    for p in cands:
        c = Image.open(p)
        parts = [bar(c, 45), bar(c, 70, 9), tile(c, 112, 'Chakra Overflow', '25'), tile(c, 32), silhouette(c)]
        h = max(x.height for x in parts) + 22
        row = Image.new('RGB', (sum(x.width for x in parts) + 12 * len(parts) + 8, h), (30, 30, 34))
        ImageDraw.Draw(row).text((6, 2), os.path.basename(p), fill=(250, 250, 250))
        x = 6
        for part in parts:
            row.paste(part, (x, 18)); x += part.width + 12
        rows.append(row)
    sheet = Image.new('RGB', (max(r.width for r in rows), sum(r.height for r in rows)), (30, 30, 34))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height
    sheet.save(out_path)
    print(out_path, sheet.size, f'{len(cands)} candidate(s)')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2:])
