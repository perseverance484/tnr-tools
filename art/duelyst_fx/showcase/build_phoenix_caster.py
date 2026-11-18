#!/usr/bin/env python3
"""Phoenix Flame Strike (V_VY284CMTuqYqOOX5sa7), full choreography. Director 2026-11-17: "show the phoenix forming
from flames that swirl around the caster and fly off".

    python3 art/duelyst_fx/showcase/build_phoenix_caster.py --duelyst <duelyst>/app

Effects: damage on the target (rounds 0) + increasedamagegiven on the caster (SELF, 2 rounds, empty art slots), so
both sides get art with no new tags and no mechanics change. Every clip of one action starts together, and a clip
stays on its own hex, so the flight is told by timing: the phoenix climbs out of the top of the caster's clip, and
the target's clip is held back until then and opens with the fireball diving in from above.
- CASTER appear (buff effect), 18 frames x 70 ms: fire-tinted swirl (Duelyst fx_f1_inmolation 2-7) round the legs;
  it flares up (inmolation 14-16) while the phoenix fades in out of it (fx_f2_phoenixfire 19); wings fold then open
  (phoenixfire 20-21); a launch flash (phoenixfire 24); the phoenix climbs and leaves the frame (22, 23, 25, 26).
- CASTER loop (2 rounds): inmolation 3-14, the swirl keeps circling (seamless with the appear's opening).
- CASTER end: inmolation 15-22, the swirl flares and scatters.
- TARGET appear (damage effect): phoenixfire 8-37 (dive, egg, burst, phoenix, embers) behind a blank lead as long as
  the caster's launch, 80 ms; replaces the earlier showcase strip (fresh _b name).
All CC0 (OpenDuelyst). Geometry: clip = SCALE tile heights centred on the hex centre; feet 0.4 tile heights below.
Outputs: final/anim_phoenix_caster_{appear,loop,end}_<px>.webp, final/anim_phoenix_flame_strike_225_b.webp,
preview/phoenix_full_discord.gif.
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "jutsu_icons", "forbidden_chakra_fury", "animation"))
import duelyst_fx as D  # noqa: E402
import build_v5 as V  # noqa: E402
from build_showcase import FEET_H, TOP_H, SCALE, fit, FONT, FONT2  # noqa: E402

FIRE = (1.0, 0.42, 0.10)
C = 270                      # caster canvas (native pixels); one tile height = C / SCALE = 90 px
TH = C / SCALE
CX, CY = C // 2, C // 2
FEET = CY + FEET_H * TH      # 171
BODY = CY - 0.4 * TH         # 99
APPEAR_MS, LOOP_MS, END_MS, TARGET_MS = 70, 80, 80, 80


def alpha(im, k):
    out = im.copy()
    out.putalpha(out.getchannel("A").point(lambda v: int(v * k)))
    return out


def stamp(canvas, im, cx, cy):
    canvas.alpha_composite(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))))


def build(app):
    src = os.path.join(app, "resources", "fx")
    inmo = [D.tint(f, FIRE).resize((140, 140), Image.NEAREST) for f in D.squared(D.frames(src, "fx_f1_inmolation"))]
    phx = D.squared(D.frames(src, "fx_f2_phoenixfire"))           # 150 px
    swirl_y = FEET - 0.45 * TH                                      # swirl centre round the shins/thighs
    phx_y = BODY - 10                                               # phoenix forms over the body
    blank = lambda: Image.new("RGBA", (C, C), (0, 0, 0, 0))         # noqa: E731
    appear = []
    for i in range(2, 8):                                           # swirl gathers
        f = blank(); stamp(f, inmo[i], CX, swirl_y); appear.append(f)
    for k, i in enumerate((14, 15, 16)):                            # flare up, phoenix fades in
        f = blank(); stamp(f, inmo[i], CX, swirl_y - 8 * k)
        stamp(f, alpha(phx[19], (0.25, 0.55, 0.85)[k]), CX, phx_y); appear.append(f)
    for i in (20, 21):                                              # wings fold, open
        f = blank(); stamp(f, alpha(inmo[18], 0.6), CX, swirl_y); stamp(f, phx[i], CX, phx_y); appear.append(f)
    f = blank(); stamp(f, phx[24], CX, phx_y); appear.append(f)     # launch flash
    rise = [10, 28, 56, 96, 150, 215]
    for k, i in enumerate((22, 23, 25, 26, 22, 23)):                # climbs out of the frame
        f = blank()
        if k < 3:
            stamp(f, alpha(inmo[19 + k], 0.7 - 0.2 * k), CX, swirl_y)   # embers left behind
        p = phx[i] if k < 4 else ImageEnhance.Brightness(phx[i]).enhance(1.15)
        stamp(f, p, CX, phx_y - rise[k]); appear.append(f)
    launch_ms = len(appear) * APPEAR_MS - 2 * APPEAR_MS             # the phoenix is gone two frames before the end
    loop = []
    for i in range(3, 15):
        f = blank(); stamp(f, inmo[i], CX, swirl_y); loop.append(f)
    end = []
    for i in range(15, 23):
        f = blank(); stamp(f, inmo[i], CX, swirl_y); end.append(f)
    # target: dive onwards, anchored as build_showcase.py (fire egg's base on the feet), behind a blank lead
    tframes, tpx, _ = fit(phx, 146, FEET_H, 1.5)
    lead = round(launch_ms / TARGET_MS)
    target = [Image.new("RGBA", (tpx, tpx), (0, 0, 0, 0))] * lead + tframes[8:]
    return appear, loop, end, target, tpx, lead


def preview(appear, loop, end, target, out):
    W, H = 720, 380
    w = 150
    h = w / 2
    e = int(h * SCALE)
    caster = (W * 0.24, H * 0.68)
    tgt = (caster[0] + 3 * w * 0.75, caster[1] - h / 2)
    rs = lambda frs: [f.resize((e, e), Image.LANCZOS) for f in frs]  # noqa: E731
    A, L, E, T = rs(appear), rs(loop), rs(end), rs(target)
    base = Image.new("RGBA", (W, H), (30, 20, 20, 255))
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
        fd.rounded_rectangle((cx - bw / 2, top + head * 1.6, cx + bw / 2, feet - 4), radius=8, fill=(66, 58, 62, 255))
        fd.ellipse((cx - head, top, cx + head, top + head * 2), fill=(66, 58, 62, 255))
    title = ImageFont.truetype(FONT, 26)
    sub = ImageFont.truetype(FONT2, 13)
    small = ImageFont.truetype(FONT2, 12)
    strike_end = max(len(A) * APPEAR_MS, len(T) * TARGET_MS)
    loop_until = strike_end + 2200          # the buff's two rounds, shortened for the preview
    total = loop_until + len(E) * END_MS + 600
    shots = []
    for t in range(0, total, 35):
        im = base.copy()
        im.alpha_composite(figs)
        put = lambda fr, p: im.alpha_composite(fr, (int(p[0] - e / 2), int(p[1] - e / 2)))  # noqa: E731
        if t < loop_until:
            put(L[(t // LOOP_MS) % len(L)], caster)   # the loop runs from the strike, under the appear
        elif t < loop_until + len(E) * END_MS:
            put(E[(t - loop_until) // END_MS], caster)
        if t < len(A) * APPEAR_MS:
            put(A[t // APPEAR_MS], caster)
        if t < len(T) * TARGET_MS:
            put(T[t // TARGET_MS], tgt)
        dd = ImageDraw.Draw(im)
        dd.text((20, 14), "Phoenix Flame Strike", font=title, fill=(255, 226, 190, 255))
        dd.text((22, 48), "Fire Style · new battle animation", font=sub, fill=(200, 170, 140, 255))
        dd.text((caster[0] - 22, caster[1] + h * 0.78), "caster", font=small, fill=(200, 180, 170, 255))
        dd.text((tgt[0] - 20, tgt[1] + h * 0.78), "target", font=small, fill=(200, 180, 170, 255))
        if t >= loop_until:
            dd.text((W - 200, H - 24), "buff ends (2 rounds later)", font=small, fill=(200, 170, 140, 255))
        shots.append(im.convert("RGB").quantize(colors=220, method=Image.Quantize.MEDIANCUT,
                                                dither=Image.Dither.NONE))
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=35, loop=0, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True)
    a = ap.parse_args()
    appear, loop, end, target, tpx, lead = build(a.duelyst)
    fin = os.path.join(HERE, "final")
    for old in ("anim_phoenix_caster_appear_234.webp", "anim_phoenix_caster_loop_315.webp",
                "anim_phoenix_caster_end_315.webp", "anim_phoenix_flame_strike_225.webp"):
        p = os.path.join(fin, old)
        if os.path.exists(p):
            os.remove(p)
    for name, frs, px, ms in (("anim_phoenix_caster_appear", appear, C, APPEAR_MS),
                              ("anim_phoenix_caster_loop", loop, C, LOOP_MS),
                              ("anim_phoenix_caster_end", end, C, END_MS),
                              ("anim_phoenix_flame_strike", target, tpx, TARGET_MS)):
        suffix = "_b" if name == "anim_phoenix_flame_strike" else ""
        p = os.path.join(fin, f"{name}_{px}{suffix}.webp")
        b = D.write_strip(frs, p, px)
        print(f"{os.path.basename(p)}: {len(frs)} frames x {ms} ms, {b} bytes")
    print(f"target lead: {lead} blank frames")
    g = os.path.join(HERE, "preview", "phoenix_full_discord.gif")
    preview(appear, loop, end, target, g)
    print(g, os.path.getsize(g))


if __name__ == "__main__":
    main()
