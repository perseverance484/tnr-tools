#!/usr/bin/env python3
"""Staff showcase: two Duelyst (CC0) hero effects fitted to existing TNR jutsu. Director 2026-11-17.

    python3 art/duelyst_fx/showcase/build_showcase.py --duelyst <duelyst>/app

- Mist Dragon Seal (fx_f2_mistdragonseal, Duelyst's ninja faction) -> Aqua Dragon Barrage (65FicNSOQQ-otNFZIoacT):
  "a relentless barrage of water dragons that crashes into the target". A red sealing circle, a blue water dragon
  bursts out roaring, talisman strips scatter.
- Phoenix Fire (fx_f2_phoenixfire) -> Phoenix Flame Strike (V_VY284CMTuqYqOOX5sa7): "conjures a blazing phoenix that
  dives into the target in a burst of fire". A spark falls, an egg of fire cracks open, a phoenix spreads its wings.
Native colours and timing (80 ms). Each source sits on a padded square canvas with one anchor row placed by the
engine's real geometry (see FEET_H / BODY_H): the dragon's seal on the body, the phoenix's fire egg on the feet. Exported at
native resolution: no resampling, so the pixel art is exactly as drawn. Proposal only; nothing uploaded.
Outputs: final/anim_<slug>_<px>.webp (strip) and preview/<slug>_discord.gif (640x360, real geometry, scale 3).
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

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
# Engine geometry (game source app/src/libs/rendering/scenes/combatEffects.ts, combatActors.ts): an effect clip is
# a square of tile.height x animationScale centred on the hex centre (tile-local y = h/2); a fighter's feet are at
# y = 0.1h (AI portrait) / 0.15h (player sprite) and its centre at 0.9h / 0.825h, y up. On screen: feet 0.4h BELOW
# the clip centre, body centre about 0.35-0.4h ABOVE it, top of the figure about 1.2h above it.
FEET_H, BODY_H, TOP_H = 0.4, -0.4, -1.2   # screen offsets from the clip centre, in tile heights (+ = down)
SCALE = 3.0

SPECS = [  # slug, sheet, jutsu name, subtitle, source anchor row, where it goes (tile heights from clip centre),
           # canvas factor, title colour, bg
    ("aqua_dragon_barrage", "fx_f2_mistdragonseal", "Aqua Dragon Barrage", "Water Style · new battle animation",
     98, BODY_H, 1.4, (206, 236, 255), (18, 26, 38)),       # the seal circle's centre -> the body
    ("phoenix_flame_strike", "fx_f2_phoenixfire", "Phoenix Flame Strike", "Fire Style · new battle animation",
     146, FEET_H, 1.5, (255, 226, 190), (32, 22, 22)),      # the fire egg's base -> the feet
]


def union_bbox(frs):
    u = None
    for f in frs:
        b = f.getbbox()
        if b:
            u = b if u is None else (min(u[0], b[0]), min(u[1], b[1]), max(u[2], b[2]), max(u[3], b[3]))
    return u


def fit(frs, anchor_row, at_h, factor):
    """Pad to a square canvas `factor` x the source and place source row `anchor_row` at `at_h` tile heights from
    the canvas centre (the canvas is the clip: SCALE tile heights). Reports any rows cut off at the top/bottom."""
    s = frs[0].width
    c = int(round(s * factor))
    u = union_bbox(frs)
    target_row = c / 2 + at_h / SCALE * c
    ox = int(round(c / 2 - (u[0] + u[2]) / 2))
    oy = int(round(target_row - anchor_row))
    cut_top, cut_bottom = max(0, -(oy + u[1])), max(0, oy + u[3] - c)
    out = []
    for f in frs:
        cv = Image.new("RGBA", (c, c), (0, 0, 0, 0))
        cv.paste(f, (ox, oy), f)
        out.append(cv)
    return out, c, (cut_top, cut_bottom)


def discord(frs, ms, out, title_txt, sub_txt, tcol, bg):
    W, H = 640, 360
    w = 190
    h = w / 2
    e = int(h * 3)
    cx, cy = W * 0.6, H * 0.62
    clip = [f.resize((e, e), Image.NEAREST if e % f.width == 0 else Image.LANCZOS) for f in frs]
    base = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(base)
    for c in range(-3, 4):
        for r in range(-3, 4):
            x = cx + c * w * 0.75
            y = cy + r * h + (h / 2 if c % 2 else 0)
            d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 26))
    d.polygon(V.hex_poly(cx, cy, w, h), fill=tuple(min(255, v + 14) for v in bg) + (255,),
              outline=(255, 255, 255, 60))
    fig = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # stand-in target figure
    fd = ImageDraw.Draw(fig)
    feet, top = cy + FEET_H * h, cy + TOP_H * h       # real fighter placement (see FEET_H/TOP_H)
    bw, head = w * 0.17, w * 0.1
    fd.ellipse((cx - w * 0.16, feet - h * 0.09, cx + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 70))
    fd.rounded_rectangle((cx - bw / 2, top + head * 1.6, cx + bw / 2, feet - 4), radius=10, fill=(62, 60, 72, 255))
    fd.ellipse((cx - head, top, cx + head, top + head * 2), fill=(62, 60, 72, 255))
    title = ImageFont.truetype(FONT, 28)
    sub = ImageFont.truetype(FONT2, 14)
    total = len(clip) * ms + 800
    shots, durs = [], []
    for t in range(0, total, 40):
        im = base.copy()
        im.alpha_composite(fig)
        k = t // ms
        if k < len(clip):
            im.alpha_composite(clip[k], (int(cx - e / 2), int(cy - e / 2)))
        dd = ImageDraw.Draw(im)
        dd.text((22, 16), title_txt, font=title, fill=tcol + (255,))
        dd.text((24, 52), sub_txt, font=sub, fill=tuple(int(v * 0.75) for v in tcol) + (255,))
        shots.append(im.convert("RGB"))
        durs.append(40)
    pal = [s.quantize(colors=220, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for s in shots]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True)
    a = ap.parse_args()
    src = os.path.join(a.duelyst, "resources", "fx")
    res = os.path.join(a.duelyst, "data", "resources.js")
    os.makedirs(os.path.join(HERE, "final"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
    for slug, sheet, name, sub, anchor, at_h, factor, tcol, bg in SPECS:
        frs = D.squared(D.frames(src, sheet))
        ms = D.delay_ms(res, sheet)
        placed, px, cut = fit(frs, anchor, at_h, factor)
        p = os.path.join(HERE, "final", f"anim_{slug}_{px}.webp")
        b = D.write_strip(placed, p, px)
        g = os.path.join(HERE, "preview", f"{slug}_discord.gif")
        discord(placed, ms, g, name, sub, tcol, bg)
        print(f"{name}: {len(placed)} frames x {ms} ms, {px}px (cut top/bottom {cut}), strip {b} B, gif {os.path.getsize(g)} B")


if __name__ == "__main__":
    main()
