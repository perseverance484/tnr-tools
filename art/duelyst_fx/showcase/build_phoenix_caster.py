#!/usr/bin/env python3
"""Phoenix Flame Strike (V_VY284CMTuqYqOOX5sa7), full choreography. Director 2026-11-17: "show the phoenix forming
from flames that swirl around the caster and fly off".

    python3 art/duelyst_fx/showcase/build_phoenix_caster.py --duelyst <duelyst>/app

Effects: damage on the target (rounds 0) + increasedamagegiven on the caster (SELF, 2 rounds, empty art slots), so
both sides get art with no new tags and no mechanics change. Every clip of one action starts together, and a clip
stays on its own hex, so the flight is told by timing: the phoenix climbs out of the top of the caster's clip, and
the target's clip is held back until then and opens with the fireball diving in from above.
- CASTER appear (buff effect), about 19 frames x 70 ms (empty tail trimmed). The swirl (Duelyst fx_f1_inmolation, remapped by luminance onto
  a colour ramp sampled from the phoenix's own frames, so it is the same fire) coils up from the shins and tightens
  on the chest while embers spiral in; it flares (inmolation 14-15) over the start of Duelyst's drawn birth
  (fx_f2_phoenixfire 15-19: the fireball bursts with the phoenix inside), wings fold and open (20-21), a launch
  flash (24), and the phoenix climbs out of the frame (22, 23, 25, 26) over the birth's dying embers (27-31).
- No loop or end clip on the buff (director: "There's so many buffs in tnr it would be a mess if they all stayed"):
  the flames show during the cast only; the buff itself stays invisible like other TNR buffs.
- TARGET appear (damage effect): phoenixfire 8-37 (dive, egg, burst, phoenix, embers) behind a blank lead as long as
  the caster's launch, 80 ms; replaces the earlier showcase strip (fresh _b name).
All CC0 (OpenDuelyst). Geometry: clip = SCALE tile heights centred on the hex centre; feet 0.4 tile heights below.
Outputs: final/anim_phoenix_caster_appear_<px>.webp, final/anim_phoenix_flame_strike_225_b.webp,
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
APPEAR_MS, TARGET_MS = 70, 80


def alpha(im, k):
    out = im.copy()
    out.putalpha(out.getchannel("A").point(lambda v: int(v * k)))
    return out


def stamp(canvas, im, cx, cy):
    canvas.alpha_composite(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))))


def ramp_from(frames, bins=256):
    """A luminance -> colour lookup sampled from frames (the phoenix's own fire), dark to light."""
    import numpy as np
    pix = []
    for f in frames:
        a = np.asarray(f.convert("RGBA")).reshape(-1, 4)
        pix.append(a[a[:, 3] > 200][:, :3])
    pix = np.concatenate(pix).astype(np.float32)
    lum = pix @ np.array([0.299, 0.587, 0.114], np.float32)
    order = np.argsort(lum)
    pix, lum = pix[order], lum[order]
    lut = np.zeros((bins, 3), np.float32)
    edges = np.linspace(0, len(lum), bins + 1).astype(int)
    for i in range(bins):
        seg = pix[edges[i]:max(edges[i] + 1, edges[i + 1])]
        lut[i] = seg.mean(0)
    return lut


def remap(im, lut):
    """Recolour by luminance rank onto `lut`, keeping alpha: the swirl becomes the phoenix's fire."""
    import numpy as np
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    lum = a[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
    idx = np.clip((lum / 255 * (len(lut) - 1)).astype(int), 0, len(lut) - 1)
    out = a.copy()
    out[..., :3] = lut[idx]
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def sparks(canvas, centre, n, t, radius, seed=3):
    """Embers spiralling inward to `centre` (t 0 -> 1), drawn in phoenix colours."""
    import math
    import random
    rnd = random.Random(seed)
    d = ImageDraw.Draw(canvas)
    cols = [(255, 214, 90, 255), (255, 150, 40, 255), (230, 70, 30, 255)]
    for i in range(n):
        a0 = rnd.uniform(0, 2 * math.pi)
        r = radius * (1 - t) * rnd.uniform(0.6, 1.0)
        a = a0 + t * 2.4
        x, y = centre[0] + math.cos(a) * r, centre[1] + math.sin(a) * r * 0.55
        sz = 2 + (i % 2)
        d.rectangle((x, y, x + sz, y + sz), fill=cols[i % 3])


def build(app):
    src = os.path.join(app, "resources", "fx")
    phx = D.squared(D.frames(src, "fx_f2_phoenixfire"))           # 150 px
    lut = ramp_from(phx[20:27])
    inmo = [remap(f, lut).resize((140, 140), Image.NEAREST) for f in D.squared(D.frames(src, "fx_f1_inmolation"))]
    swirl_y0 = FEET - 0.45 * TH                                     # starts round the shins
    phx_y = BODY - 10                                               # the phoenix is born over the chest
    blank = lambda: Image.new("RGBA", (C, C), (0, 0, 0, 0))         # noqa: E731
    shrink = lambda im, k: im.resize((max(1, int(im.width * k)),) * 2, Image.NEAREST)  # noqa: E731
    appear = []
    # 1. the swirl coils up the body and tightens (6 frames)
    for k, i in enumerate(range(2, 8)):
        u = k / 5
        f = blank()
        stamp(f, shrink(inmo[i], 1.0 - 0.25 * u), CX, swirl_y0 + (phx_y + 18 - swirl_y0) * u)
        if k >= 2:
            sparks(f, (CX, phx_y + 10), 10, (k - 2) / 4, 70)
        appear.append(f)
    # 2. it flares into a fireball (2 frames), the drawn birth begins underneath
    for k, i in enumerate((14, 15)):
        f = blank()
        stamp(f, alpha(shrink(phx[15 + k], 0.85), 0.5 + 0.4 * k), CX, phx_y + 6)
        stamp(f, shrink(inmo[i], 0.72), CX, phx_y + 18)
        sparks(f, (CX, phx_y + 10), 10, 0.85 + 0.15 * k, 70)
        appear.append(f)
    # 3. the phoenix bursts out of the fireball (Duelyst's own frames 16-19), wings fold and open (20-21)
    for i in (16, 17, 18, 19, 20, 21):
        f = blank()
        stamp(f, shrink(phx[i], 0.85 if i < 20 else 0.9), CX, phx_y + (6 if i < 20 else 0))
        appear.append(f)
    # 4. launch flash, then it climbs out of the frame leaving embers
    f = blank(); stamp(f, shrink(phx[24], 0.9), CX, phx_y); appear.append(f)
    rise = [12, 32, 62, 104, 160, 225]
    for k, i in enumerate((22, 23, 25, 26, 22, 23)):
        f = blank()
        if k < 3:
            stamp(f, alpha(shrink(phx[27 + 2 * k], 0.85), 0.8 - 0.25 * k), CX, phx_y + 6)
        p = phx[i] if k < 4 else ImageEnhance.Brightness(phx[i]).enhance(1.15)
        stamp(f, shrink(p, 0.9), CX, phx_y - rise[k]); appear.append(f)
    while appear and appear[-1].getbbox() is None:                 # the phoenix has left: drop empty tail
        appear.pop()
    launch_ms = len(appear) * APPEAR_MS
    tframes, tpx, _ = fit(phx, 146, FEET_H, 1.5)
    lead = round(launch_ms / TARGET_MS)
    target = [Image.new("RGBA", (tpx, tpx), (0, 0, 0, 0))] * lead + tframes[8:]
    return appear, target, tpx, lead


def preview(appear, target, out):
    W, H = 720, 380
    w = 150
    h = w / 2
    e = int(h * SCALE)
    caster = (W * 0.24, H * 0.68)
    tgt = (caster[0] + 3 * w * 0.75, caster[1] - h / 2)
    rs = lambda frs: [f.resize((e, e), Image.LANCZOS) for f in frs]  # noqa: E731
    A, T = rs(appear), rs(target)
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
    total = max(len(A) * APPEAR_MS, len(T) * TARGET_MS) + 700
    shots = []
    for t in range(0, total, 35):
        im = base.copy()
        im.alpha_composite(figs)
        put = lambda fr, p: im.alpha_composite(fr, (int(p[0] - e / 2), int(p[1] - e / 2)))  # noqa: E731
        if t < len(A) * APPEAR_MS:
            put(A[t // APPEAR_MS], caster)
        if t < len(T) * TARGET_MS:
            put(T[t // TARGET_MS], tgt)
        dd = ImageDraw.Draw(im)
        dd.text((20, 14), "Phoenix Flame Strike", font=title, fill=(255, 226, 190, 255))
        dd.text((22, 48), "Fire Style · new battle animation", font=sub, fill=(200, 170, 140, 255))
        dd.text((caster[0] - 22, caster[1] + h * 0.78), "caster", font=small, fill=(200, 180, 170, 255))
        dd.text((tgt[0] - 20, tgt[1] + h * 0.78), "target", font=small, fill=(200, 180, 170, 255))
        shots.append(im.convert("RGB").quantize(colors=220, method=Image.Quantize.MEDIANCUT,
                                                dither=Image.Dither.NONE))
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=35, loop=0, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True)
    a = ap.parse_args()
    appear, target, tpx, lead = build(a.duelyst)
    fin = os.path.join(HERE, "final")
    for old in ("anim_phoenix_caster_appear_234.webp", "anim_phoenix_caster_loop_315.webp",
                "anim_phoenix_caster_end_315.webp", "anim_phoenix_flame_strike_225.webp",
                "anim_phoenix_caster_loop_270.webp", "anim_phoenix_caster_end_270.webp"):
        p = os.path.join(fin, old)
        if os.path.exists(p):
            os.remove(p)
    for name, frs, px, ms in (("anim_phoenix_caster_appear", appear, C, APPEAR_MS),
                              ("anim_phoenix_flame_strike", target, tpx, TARGET_MS)):
        suffix = "_b" if name == "anim_phoenix_flame_strike" else ""
        p = os.path.join(fin, f"{name}_{px}{suffix}.webp")
        b = D.write_strip(frs, p, px)
        print(f"{os.path.basename(p)}: {len(frs)} frames x {ms} ms, {b} bytes")
    print(f"target lead: {lead} blank frames")
    g = os.path.join(HERE, "preview", "phoenix_full_discord.gif")
    preview(appear, target, g)
    print(g, os.path.getsize(g))


if __name__ == "__main__":
    main()
