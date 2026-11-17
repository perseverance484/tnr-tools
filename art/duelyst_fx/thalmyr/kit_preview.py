#!/usr/bin/env python3
"""Thalmyr Three Tails (raid boss, AI 0EnSqDfISrmyrSLM7HgLW): Duelyst (CC0) matches for its six own jutsu.

    python3 art/duelyst_fx/thalmyr/kit_preview.py --duelyst <duelyst>/app

A 3x2 grid of real-geometry board panels, one per jutsu, each playing its proposed clip on one target (or, for the
spiral field, on a patch of ground tiles), all on one clock and looping. Proposal only: nothing is exported for
upload here. Recolours go through duelyst_fx.tint (luminance ramp, keeps the drawing).
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "jutsu_icons", "forbidden_chakra_fury", "animation"))
import duelyst_fx as D  # noqa: E402
import build_v5 as V  # noqa: E402

SEA = (0.18, 0.78, 0.86)     # reef teal
CORAL = (1.0, 0.48, 0.52)    # coral pink
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# jutsu, what it does, Duelyst sheet[:prefix], tint, fit, dy, scale, mode
KIT = [
    ("Coral Maelstrom", "damage, every enemy", "fx_f6_spiritofthewild", None, 1.0, -0.05, 3.0, "target"),
    ("Coral Undertow", "pull in + poison, every enemy", "fx_vortexswirl", SEA, 1.0, 0.0, 3.0, "target"),
    ("Brinebound Drag", "pool cost + poison, every enemy", "fx_bluewatersplash", None, 1.0, -0.05, 3.0, "target"),
    ("Abyssal Spiral Field", "ground spiral, damage", "fx_explosionblue", SEA, 0.9, -0.1, 2.0, "field"),
    ("Shellback Surge", "shield on the Three-Tails", "fx_defense:fx_forcefield_", None, 0.9, -0.1, 3.0, "target"),
    ("Reefward Bastion", "coral shield on the Three-Tails", "fx_f3_fountainofyouth", SEA, 1.0, -0.12, 3.0, "target"),
]


def load(app, name, tint, fit, dy, size):
    frs = D.place(D.frames(os.path.join(app, "resources", "fx"), name), size, fit, dy, tint)
    return frs, D.delay_ms(os.path.join(app, "data", "resources.js"), name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True)
    a = ap.parse_args()
    PW, PH = 340, 230                 # panel
    w = 104                           # hex width in a panel
    h = w / 2
    title = ImageFont.truetype(FONT, 15)
    sub = ImageFont.truetype(FONT2, 11)
    clips = []
    for name, what, sheet, tint, fit, dy, scale, mode in KIT:
        e = int(h * scale)
        frs, ms = load(a.duelyst, sheet, tint, fit, dy, 192)
        clips.append((name, what, sheet.split(":")[0].replace("fx_", ""),
                      [f.resize((e, e), Image.LANCZOS) for f in frs], ms, e, mode))
    W, H = PW * 3, PH * 2
    base = Image.new("RGBA", (W, H), (24, 30, 34, 255))
    d = ImageDraw.Draw(base)
    centres = []
    for i in range(6):
        ox, oy = (i % 3) * PW, (i // 3) * PH
        cx, cy = ox + PW / 2, oy + PH * 0.66
        centres.append((cx, cy))
        for c in range(-3, 4):
            for r in range(-3, 3):
                x = cx + c * w * 0.75
                y = cy + r * h + (h / 2 if c % 2 else 0)
                if ox - w < x < ox + PW + w and oy < y < oy + PH + h:
                    d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 26))
        d.rectangle((ox, oy, ox + PW - 1, oy + PH - 1), outline=(70, 90, 100, 255))
    # the field panel's patch: centre tile + its six neighbours (a slice of the real spiral)
    fx, fy = centres[3]
    field = [(fx, fy)] + [(fx + dx * w * 0.75, fy + dy_ * h + (h / 2 if dx % 2 else 0))
                          for dx, dy_ in ((0, -1), (0, 1), (1, -1), (1, 0), (-1, -1), (-1, 0))]
    longest = max(len(f) * ms for _, _, _, f, ms, _, _ in clips)
    cycle = longest + 700
    frames = []
    for t in range(0, cycle, 40):
        im = base.copy()
        dd = ImageDraw.Draw(im)
        for i, (name, what, src, frs, ms, e, mode) in enumerate(clips):
            ox, oy = (i % 3) * PW, (i // 3) * PH
            cx, cy = centres[i]
            spots = field if mode == "field" else [(cx, cy)]
            if mode != "field":  # stand-in figure on the target
                bw, bh = w * 0.16, h * 1.5
                dd.rounded_rectangle((cx - bw / 2, cy - bh, cx + bw / 2, cy - 3), radius=6,
                                     fill=(62, 66, 80, 255), outline=(140, 150, 170, 255))
            k = t // ms
            if k < len(frs):
                for x, y in sorted(spots, key=lambda p: p[1]):
                    im.alpha_composite(frs[k], (int(x - e / 2), int(y - e / 2)))
            dd.text((ox + 10, oy + 8), name, font=title, fill=(220, 240, 245, 255))
            dd.text((ox + 10, oy + 27), f"{what}  ·  duelyst: {src}", font=sub, fill=(150, 175, 185, 255))
        frames.append(im.convert("RGB").quantize(colors=220, method=Image.Quantize.MEDIANCUT,
                                                 dither=Image.Dither.NONE))
    out = os.path.join(HERE, "preview", "thalmyr_kit.gif")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=40, loop=0, optimize=True)
    print(out, len(frames), os.path.getsize(out))


if __name__ == "__main__":
    main()
