#!/usr/bin/env python3
"""Fury of The White Tiger (QXE9J0fnu1t-DAGTGbaCX): caster + target from Duelyst (CC0). Director 2026-11-17.

    python3 art/duelyst_fx/showcase/build_white_tiger.py --duelyst <duelyst>/app

Battle text: "Waves of green and blue energy flow from %user's body as %user opens the first seven Inner Gates ...
a massive tiger-shaped shockwave of wind crashing into %target".
- CASTER appear (increasedamagegiven, SELF): Duelyst fx_f2_eightgates_teallotus, a ring of eight lotus pads (the
  gates), a white flash, a chakra column, a lotus bloom. Frames 1-33 minus four from the column's hold, 70 ms; pads
  anchored on the feet. Cast only (RUL-2026-11-17-166: no lingering loop on buffs; the buff's current stock loop
  iBl5_M2fonkk8yiBLQgwU would be cleared).
- TARGET appear (damage): Duelyst fx_f2_saberspineseal, a sealing circle, the tiger bursts out roaring, talisman
  strips, embers. 80 ms, seal centre on the body, behind a blank lead so it strikes once the gates have opened.
- Both recoloured with one gradient: warm hues h -> 200 - 0.6 h (red -> blue, orange -> teal, yellow -> jade), so
  the fire becomes "green and blue energy" and the tiger a jade wind tiger. Lightness and saturation kept.
Geometry as build_showcase.py. Outputs: final/anim_white_tiger_{gates,tiger}_<px>.webp, preview/white_tiger_discord.gif.
"""
import argparse
import colorsys
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "jutsu_icons", "forbidden_chakra_fury", "animation"))
import duelyst_fx as D  # noqa: E402
import build_v5 as V  # noqa: E402
from build_showcase import FEET_H, BODY_H, TOP_H, SCALE, fit, FONT, FONT2  # noqa: E402

GATES_MS, TIGER_MS = 70, 80
DROP = {14, 17, 20, 23}          # column-hold frames removed
LEAD_GATE_FRAMES = 11            # the tiger strikes once the column has risen (gates frame ~11)


def chakra(im):
    """Warm hues (reds through yellow-greens, h <= 90 or >= 330) -> 200 - 0.6 h: blue, teal, jade."""
    px = im.convert("RGBA")
    data = []
    for r, g, b, a in (px.get_flattened_data() if hasattr(px, "get_flattened_data") else px.getdata()):
        if a:
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            hd = h * 360
            if hd >= 330:
                hd -= 360
            if hd <= 90 and s > 0.12:
                nr, ng, nb = colorsys.hls_to_rgb(((200 - 0.6 * hd) % 360) / 360, l, s)
                r, g, b = int(nr * 255), int(ng * 255), int(nb * 255)
        data.append((r, g, b, a))
    out = Image.new("RGBA", px.size)
    out.putdata(data)
    return out


def build(app):
    src = os.path.join(app, "resources", "fx")
    gates = [chakra(f) for i, f in enumerate(D.squared(D.frames(src, "fx_f2_eightgates_teallotus")))
             if 1 <= i <= 33 and i not in DROP]
    gates, gpx, gcut = fit(gates, 160, FEET_H, 1.3)
    tiger = [chakra(f) for f in D.squared(D.frames(src, "fx_f2_saberspineseal"))][:30]
    tiger, tpx, tcut = fit(tiger, 97, BODY_H, 1.4)
    lead = round(LEAD_GATE_FRAMES * GATES_MS / TIGER_MS)
    tiger = [Image.new("RGBA", (tpx, tpx), (0, 0, 0, 0))] * lead + tiger
    return gates, gpx, tiger, tpx, (gcut, tcut), lead


def preview(gates, tiger, out):
    W, H = 720, 380
    w = 150
    h = w / 2
    e = int(h * SCALE)
    caster = (W * 0.24, H * 0.68)
    tgt = (caster[0] + 3 * w * 0.75, caster[1] - h / 2)
    G = [f.resize((e, e), Image.LANCZOS) for f in gates]
    T = [f.resize((e, e), Image.LANCZOS) for f in tiger]
    base = Image.new("RGBA", (W, H), (16, 26, 28, 255))
    d = ImageDraw.Draw(base)
    for c in range(-2, 7):
        for r in range(-3, 4):
            x = caster[0] + c * w * 0.75
            y = caster[1] + r * h + (h / 2 if c % 2 else 0)
            d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 24))
    figs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(figs)
    for cx, cy in (caster, tgt):
        feet, top = cy + FEET_H * h, cy + TOP_H * h
        bw, head = w * 0.17, w * 0.1
        fd.ellipse((cx - w * 0.16, feet - h * 0.09, cx + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 70))
        fd.rounded_rectangle((cx - bw / 2, top + head * 1.6, cx + bw / 2, feet - 4), radius=8, fill=(58, 66, 70, 255))
        fd.ellipse((cx - head, top, cx + head, top + head * 2), fill=(58, 66, 70, 255))
    title = ImageFont.truetype(FONT, 26)
    sub = ImageFont.truetype(FONT2, 13)
    small = ImageFont.truetype(FONT2, 12)
    total = max(len(G) * GATES_MS, len(T) * TIGER_MS) + 700
    shots = []
    for t in range(0, total, 35):
        im = base.copy()
        im.alpha_composite(figs)
        if t < len(G) * GATES_MS:
            im.alpha_composite(G[t // GATES_MS], (int(caster[0] - e / 2), int(caster[1] - e / 2)))
        if t < len(T) * TIGER_MS:
            im.alpha_composite(T[t // TIGER_MS], (int(tgt[0] - e / 2), int(tgt[1] - e / 2)))
        dd = ImageDraw.Draw(im)
        dd.text((20, 14), "Fury of The White Tiger", font=title, fill=(200, 250, 236, 255))
        dd.text((22, 48), "Forbidden · Seven Inner Gates · new battle animation", font=sub, fill=(150, 200, 190, 255))
        dd.text((caster[0] - 22, caster[1] + h * 0.78), "caster", font=small, fill=(170, 200, 195, 255))
        dd.text((tgt[0] - 20, tgt[1] + h * 0.78), "target", font=small, fill=(170, 200, 195, 255))
        shots.append(im.convert("RGB").quantize(colors=220, method=Image.Quantize.MEDIANCUT,
                                                dither=Image.Dither.NONE))
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=35, loop=0, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True)
    a = ap.parse_args()
    gates, gpx, tiger, tpx, cuts, lead = build(a.duelyst)
    fin = os.path.join(HERE, "final")
    for name, frs, px, ms in (("anim_white_tiger_gates", gates, gpx, GATES_MS),
                              ("anim_white_tiger_tiger", tiger, tpx, TIGER_MS)):
        p = os.path.join(fin, f"{name}_{px}.webp")
        b = D.write_strip(frs, p, px)
        print(f"{os.path.basename(p)}: {len(frs)} frames x {ms} ms, {b} bytes")
    print("rows cut (gates, tiger):", cuts, " tiger lead:", lead)
    g = os.path.join(HERE, "preview", "white_tiger_discord.gif")
    preview(gates, tiger, g)
    print(g, os.path.getsize(g))


if __name__ == "__main__":
    main()
