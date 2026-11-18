#!/usr/bin/env python3
"""Reefward Bastion (sDDqtnvOBcphnR8vKH1T5) appear clip from Duelyst fx_f3_fountainofyouth (CC0). Director 2026-11-17.

    python3 art/duelyst_fx/thalmyr/build_reefward.py --duelyst <duelyst>/app

Jutsu: ALL / ALLY, shield 4 rounds on the Three-Tails ("coral pillars surge from the flooded ground and weave into a
protective reef barrier"). The source clip: a pool forms, a ring rises with spouts, a water dome blooms, a twisting
column shoots up, ribbons swirl away (23 frames, 80 ms, 80 px).
Changes: the gold ring and sparks are recoloured coral (hue-selective: only warm, saturated pixels move; the water
keeps its blue); the art sits on a 96 px canvas lifted so the pool lands just below the frame centre (the target's
feet; the column tip loses its top 8 px); exported 3x NEAREST (288 px) so the pixels stay crisp. Outputs:
  final/anim_reefward_bastion_288.webp   (upload strip, 23 x 80 ms)
  preview/reefward_bastion.gif           (real-geometry single-target preview, scale 3)
"""
import argparse
import colorsys
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "jutsu_icons", "forbidden_chakra_fury", "animation"))
import duelyst_fx as D  # noqa: E402
import build_v5 as V  # noqa: E402

NAME = "fx_f3_fountainofyouth"
CANVAS = 96
POOL_Y = 70        # pool centre line in the 80 px source
POOL_AT = 62       # where it lands on the 96 px canvas
UP = 3             # export scale (NEAREST)
CORAL_HUE = 352 / 360
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def coralize(im):
    """Move warm, saturated pixels (the gold ring, sparks) to coral; leave blues and whites alone."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32) / 255
    rgb = a[..., :3]
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    hue = np.zeros_like(mx)
    d = np.maximum(mx - mn, 1e-6)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    warm = ((hue <= 100) | (hue >= 330)) & (sat > 0.2) & (a[..., 3] > 0)  # reds to lime: the gold ring and its highlight (85 deg)
    out = a.copy()
    ys, xs = np.nonzero(warm)
    for y, x in zip(ys, xs):
        h, l, s = colorsys.rgb_to_hls(*rgb[y, x])
        nr, ng, nb = colorsys.hls_to_rgb(CORAL_HUE, min(1.0, l * 1.05), min(1.0, s * 0.95))
        out[y, x, :3] = (nr, ng, nb)
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def build(app):
    frs = D.squared(D.frames(os.path.join(app, "resources", "fx"), NAME))
    s = frs[0].width
    out = []
    for f in frs:
        c = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
        c.alpha_composite(coralize(f), ((CANVAS - s) // 2, POOL_AT - POOL_Y))
        out.append(c.resize((CANVAS * UP, CANVAS * UP), Image.NEAREST))
    return out, D.delay_ms(os.path.join(app, "data", "resources.js"), NAME)


def preview(frs, ms, out):
    W, H = 640, 360
    w = 190
    h = w / 2
    e = int(h * 3)
    cx, cy = W * 0.6, H * 0.72
    clip = [f.resize((e, e), Image.LANCZOS) for f in frs]
    base = Image.new("RGBA", (W, H), (22, 30, 36, 255))
    d = ImageDraw.Draw(base)
    for c in range(-3, 4):
        for r in range(-3, 4):
            x = cx + c * w * 0.75
            y = cy + r * h + (h / 2 if c % 2 else 0)
            d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 28))
    d.polygon(V.hex_poly(cx, cy, w, h), fill=(30, 44, 52, 255), outline=(120, 210, 230, 70))
    fig = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # stand-in for the Three-Tails: a low, broad shell
    fd = ImageDraw.Draw(fig)
    fd.ellipse((cx - w * 0.30, cy - h * 0.95, cx + w * 0.30, cy + h * 0.05), fill=(52, 62, 72, 255))
    fd.ellipse((cx - w * 0.30, cy - h * 0.12, cx + w * 0.30, cy + h * 0.12), fill=(0, 0, 0, 60))
    title = ImageFont.truetype(FONT, 28)
    sub = ImageFont.truetype(FONT2, 14)
    total = len(clip) * ms + 700
    frames = []
    for t in range(0, total, 40):
        im = base.copy()
        im.alpha_composite(fig)
        k = t // ms
        if k < len(clip):
            im.alpha_composite(clip[k], (int(cx - e / 2), int(cy - e / 2)))
        dd = ImageDraw.Draw(im)
        dd.text((22, 16), "Reefward Bastion", font=title, fill=(214, 244, 250, 255))
        dd.text((24, 52), "Thalmyr Three Tails · new battle animation", font=sub, fill=(150, 196, 210, 255))
        frames.append(im.convert("RGB").quantize(colors=200, method=Image.Quantize.MEDIANCUT,
                                                 dither=Image.Dither.NONE))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=40, loop=0, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True)
    a = ap.parse_args()
    frs, ms = build(a.duelyst)
    os.makedirs(os.path.join(HERE, "final"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
    p = os.path.join(HERE, "final", f"anim_reefward_bastion_{CANVAS * UP}.webp")
    b = D.write_strip(frs, p, CANVAS * UP)
    print(f"{os.path.basename(p)}: {len(frs)} frames x {ms} ms, {b} bytes")
    g = os.path.join(HERE, "preview", "reefward_bastion.gif")
    preview(frs, ms, g)
    print(g, os.path.getsize(g))


if __name__ == "__main__":
    main()
