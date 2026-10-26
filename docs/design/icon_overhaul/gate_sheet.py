#!/usr/bin/env python3
"""Gate sheet for one icon round: each candidate as players see it, beside the references.

    python3 docs/design/icon_overhaul/gate_sheet.py OUT.png "ref:LABEL=PATH" ... LABEL=PATH [LABEL=PATH ...]

Arguments starting with "ref:" are reference rows (drawn first, label dimmed); the rest are candidates.

Per row: the 256 px icon; the 45 px phone size and its blurred grey silhouette (both enlarged 2x with nearest neighbour, so
the sheet shows the real phone pixels); 32 px; a 112 px tile with the level badge (bottom-left); and the 45 px icon in a
mobile battle bar between kept icons. The first rows are the references (older version, live icon).
Sizes from the game source: 45 px mobile bar, 112 px default tile, rounded corners, 28 px badge (deep dive section 3).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
KEPT = ["art/jutsu_icons/scroll_jutsu/exports/icon_jutsu_blazing_fang_strike_v1.webp",
        "art/jutsu_icons/scroll_jutsu/exports/icon_jutsu_celestial_dew_v1.webp",
        "art/style_refs/jutsu_icons/bee/icon_bee_ring_of_spilled_blood_v2.webp",
        "art/jutsu_icons/crystal_essence/exports/icon_crystal_essence_crystal_sphere_v1.webp",
        "art/style_refs/jutsu_icons/bee/icon_bee_crimson_tithe_v1.webp",
        "art/jutsu_icons/crystal_essence/exports/icon_crystal_essence_prism_v1.webp"]
BG, PANEL, FG, DIM = (24, 26, 32), (15, 23, 42), (235, 235, 240), (160, 163, 172)


def font(s, b=False):
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
    except OSError:
        return ImageFont.load_default()


def square(path):
    im = Image.open(path).convert('RGB')
    s = min(im.size)
    return im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width - s) // 2 + s, (im.height - s) // 2 + s))


def at(im, px):
    return im.resize((px, px), Image.LANCZOS)


def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = Image.new('RGB', im.size, PANEL)
    out.paste(im, (0, 0), m)
    return out


def tile112(im):
    t = rounded(at(im, 112), 12)
    d = ImageDraw.Draw(t)
    d.rounded_rectangle((0, 0, 111, 111), 12, outline=(148, 163, 184), width=2)
    d.ellipse((2, 82, 30, 110), fill=(30, 41, 59), outline=(148, 163, 184))
    d.text((16, 96), "5", font=font(14, True), fill=FG, anchor='mm')
    return t


def bar(im):
    icons = [square(os.path.join(ROOT, p)) for p in KEPT]
    seq = icons[:3] + [im] + icons[3:]
    b = Image.new('RGB', (len(seq) * 49 + 4, 53), PANEL)
    for i, x in enumerate(seq):
        b.paste(rounded(at(x, 45), 6), (4 + i * 49, 4))
    return b


def main(out, refs, cands, title):
    rows = [(l, os.path.join(ROOT, p)) for l, p in refs] + cands
    nref = len(refs)
    RH = 256 + 40
    W = 256 + 3 * 100 + 50 + 130 + 7 * 49 + 80
    sheet = Image.new('RGB', (W, 60 + RH * len(rows)), BG)
    d = ImageDraw.Draw(sheet)
    d.text((16, 16), title, font=font(24, True), fill=FG)
    for i, (label, path) in enumerate(rows):
        y = 60 + i * RH
        im = square(path)
        d.text((16, y), label, font=font(17, True), fill=DIM if i < nref else FG)
        x = 16
        sheet.paste(at(im, 256), (x, y + 26)); x += 256 + 20
        s45 = at(im, 45)
        sheet.paste(s45.resize((90, 90), Image.NEAREST), (x, y + 26))
        d.text((x, y + 120), "45 px", font=font(13), fill=DIM)
        sil = ImageOps.grayscale(s45).filter(ImageFilter.GaussianBlur(1.6)).convert('RGB')
        sheet.paste(sil.resize((90, 90), Image.NEAREST), (x + 100, y + 26))
        d.text((x + 100, y + 120), "silhouette", font=font(13), fill=DIM)
        sheet.paste(at(im, 32).resize((64, 64), Image.NEAREST), (x + 200, y + 26))
        d.text((x + 200, y + 96), "32 px", font=font(13), fill=DIM)
        sheet.paste(tile112(im), (x, y + 150))
        d.text((x + 120, y + 240), "112 px tile, badge", font=font(13), fill=DIM)
        x += 300
        sheet.paste(bar(im), (x, y + 26))
        d.text((x, y + 84), "mobile bar (45 px), 4th icon", font=font(13), fill=DIM)
    sheet.save(out, optimize=True)
    print(out, sheet.size)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = sys.argv[2:]
    title = "Gate sheet"
    if args and args[0].startswith("title:"):
        title = args.pop(0)[6:]
    refs = [tuple(a[4:].split('=', 1)) for a in args if a.startswith("ref:")]
    cands = [tuple(a.split('=', 1)) for a in args if not a.startswith("ref:")]
    main(sys.argv[1], refs, cands, title)
