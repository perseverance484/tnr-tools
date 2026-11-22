#!/usr/bin/env python3
"""Forbidden Chakra Fury v10: built for the area tile variation engine feature (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v10/build_v10.py

Director: "we could make a much higher quality animation ... using mirror, stagger and alternate", plus ripple. The
tiles are "violet streaks of chakra" like the icon; the centre piece is the user casting the jutsu; the v7 explosion on
the character was the part he liked.

Clips (one drawn pixel is h/28 on the board in every clip, so the pieces share one pixel scale):
- CASTER (visual tag, scale 3, 80 ms): the Duelyst gate pillar ignites around the user while chakra lightning crawls
  over the body (charge, frames 0-6). At frame 7 the user releases: the v7 shadow-nova burst (fx_f4_shadownova, CC0,
  trimmed to fit 4096 px) with six bolts running out through the hex edges toward the neighbours.
- STRIKE A / B (damage tag, scale 3, 70 ms; B is the animationAlternate): each in four beats after a lead that waits
  for the release. A, the sky strike: sparks gather on the ground (anticipation), a white-hot bolt falls from above
  with an impact flash (strike), ground arcs flicker across the hex (crackle), embers drift up and die (decay). B, the
  ground eruption: violet cracks open across the hex, chakra streaks shoot up out of them, the cracks crackle, embers.
- GLOW (recoil tag, scale 2, 70 ms): a violet chakra stain that swells under the strikes and fades with them.

Engine settings the preview simulates (combatEffects.tileVariation, ported in tile_variation.py):
  strikes: animationMirror on, animationAlternate = strike B, animationStagger 120, animationRipple 90
  glow:    animationMirror on, animationStagger 120, animationRipple 90
A tile four hexes out waits at most 480 ms, inside the 0.6-0.8 s budget that keeps a cast readable in replay.
Every strip <= 4096 px tall.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
V9 = os.path.join(HERE, "..", "v9")
sys.path.insert(0, V9)
import build_v9 as V  # noqa: E402  (jag, draw_bolt, hex_mids, pillar; also puts the skill scripts on the path)
import duelyst_kit as K  # noqa: E402

GLOW, MID, HOT, DIM = V.GLOW, V.MID, V.HOT, V.DIM
EMBER = (206, 150, 255, 255)
LICENSE = ("CC0 1.0 - OpenDuelyst (open-duelyst/duelyst): fx_f2_eightgates_purpleflame, fx_f4_shadownova, adapted "
           "for TNR; lightning, strikes and glow drawn for TNR")

C_MS, S_MS, G_MS = 80, 70, 70
RELEASE = 7                           # caster frame the jutsu leaves the hands
LEAD = 7                              # strike/glow frames held empty so the area starts as the release lands
SL, SX = 84, 2                        # strike/caster: 84 drawn px x2 = 168 px, scale 3 (one drawn px = h/28)
GL, GX = 56, 3                        # glow: 56 drawn px x3 = 168 px, scale 2
SH = SL / 3                           # tile height in drawn px at scale 3
SC = SL / 2                           # clip centre = the hex centre (ground point)


def blank(n=SL):
    return Image.new("RGBA", (n, n), (0, 0, 0, 0))


def flat(cx, cy, r, ang):
    """A point on the ground ellipse (the board is squashed 2:1)."""
    return (cx + math.cos(ang) * r, cy + math.sin(ang) * r * 0.5)


def ground_arc(layer, rnd, heat, reach, branches=1):
    a = rnd.uniform(0, 2 * math.pi)
    p = flat(SC, SC, rnd.uniform(0, 3), a)
    q = flat(SC, SC, reach * rnd.uniform(0.7, 1.0), a + rnd.uniform(-0.4, 0.4))
    V.draw_bolt(layer, V.jag(p, q, 0.6, rnd, 3), heat, branches, rnd)


def flash(layer, r, fill):
    ImageDraw.Draw(layer).ellipse((SC - r, SC - r / 2, SC + r, SC + r / 2), fill=fill)


def embers(layer, rnd, t, n, seed_pts):
    d = ImageDraw.Draw(layer)
    for i in range(n):
        x, y = seed_pts[i % len(seed_pts)]
        a = max(0, 255 - t * 50)
        d.point((round(x + rnd.uniform(-1, 1)), round(y - t * 1.5 - i % 3)), fill=EMBER[:3] + (a,))


def decay_frames(rnd, pts, scorch):
    out = []
    for t in range(5):
        im = blank()
        if scorch:
            r = 9 - t
            ImageDraw.Draw(im).ellipse((SC - r, SC - r / 2, SC + r, SC + r / 2), outline=GLOW[:3] + (110 - 22 * t,))
        if t < 2:
            ground_arc(im, rnd, 0, 8, 0)
        embers(im, rnd, t, 8, pts)
        out.append(im)
    return out


def strike_sky(seed=31):
    rnd = random.Random(seed)
    out = []
    for t in range(3):                                     # anticipation: sparks pull in to the strike point
        im = blank()
        d = ImageDraw.Draw(im)
        for k in range(8):
            x, y = flat(SC, SC, 12 - 4 * t, k * math.pi / 4 + t * 0.4)
            d.point((round(x), round(y)), fill=MID if t < 2 else HOT)
        flash(im, 2 + t, GLOW)
        out.append(im)
    top = (SC + rnd.uniform(-6, 6), 0)
    path = V.jag(top, (SC, SC), 0.45, rnd, 5)
    im = blank()                                           # leader
    V.draw_bolt(im, path, 1, 0, rnd)
    out.append(im)
    for t in range(2):                                     # strike: white-hot bolt, impact flash, ground arcs
        im = blank()
        flash(im, 9 - 3 * t, GLOW)
        bolt = V.jag(top, (SC, SC), 0.45, rnd, 5)
        V.draw_bolt(im, [(x + 1, y) for x, y in bolt], 1, 0, rnd)   # a second strand thickens the strike
        V.draw_bolt(im, bolt, 2, 3, rnd)
        flash(im, 4 - t, HOT)
        for _ in range(3):
            ground_arc(im, rnd, 2, 12)
        out.append(im)
    for t in range(5):                                     # crackle: the bolt flickers out, arcs run the ground
        im = blank()
        if t in (0, 2):
            V.draw_bolt(im, V.jag(top, (SC, SC), 0.45, rnd, 5), 1, 1, rnd)
        for _ in range(3 - t // 2):
            ground_arc(im, rnd, 1 if t < 3 else 0, 13)
        out.append(im)
    out += decay_frames(rnd, [flat(SC, SC, rnd.uniform(0, 9), rnd.uniform(0, 6.3)) for _ in range(8)], True)
    return out


def strike_ground(seed=47):
    rnd = random.Random(seed)
    angs = [i * 2 * math.pi / 5 + rnd.uniform(-0.3, 0.3) for i in range(5)]
    cracks = [V.jag((SC, SC), flat(SC, SC, rnd.uniform(10, 13), a), 0.5, rnd, 3) for a in angs]
    vents = [c[len(c) * 2 // 3] for c in cracks]
    out = []
    for t in range(3):                                     # anticipation: the cracks open outward
        im = blank()
        for c in cracks:
            V.draw_bolt(im, c, 1 if t < 2 else 2, 0, rnd, upto=(t + 1) / 3)
        out.append(im)
    for t in range(3):                                     # strike: streaks shoot up out of the vents
        im = blank()
        flash(im, 6 + 2 * t, GLOW)
        for c in cracks:
            V.draw_bolt(im, c, 2, 0, rnd)
        for i, (x, y) in enumerate(vents):
            hgt = SH * (0.55 + 0.25 * ((i * 7) % 3)) * min(1.0, 0.45 + 0.35 * t)
            V.draw_bolt(im, V.jag((x, y), (x + rnd.uniform(-3, 3), y - hgt), 0.35, rnd, 3), 2 if t else 1,
                        1 if t else 0, rnd)
        out.append(im)
    for t in range(5):                                     # crackle: cracks and stubs of the streaks flicker
        im = blank()
        for k, c in enumerate(cracks):
            if (k + t) % 2 == 0 or t < 2:
                V.draw_bolt(im, c, 1 if t < 3 else 0, 0, rnd)
        for i, (x, y) in enumerate(vents):
            if (i + t) % 3 == 0:
                V.draw_bolt(im, V.jag((x, y), (x, y - SH * 0.3), 0.4, rnd, 2), 1 if t < 3 else 0, 0, rnd)
        out.append(im)
    out += decay_frames(rnd, vents, True)
    return out


def glow_frames():
    """A faint chakra stain under the strikes: an uneven violet scatter that swells with the strike and fades.
    Drawn on the 56 px scale-2 grid; kept low and broken up so the area never reads as a grid of pads."""
    import random as _r
    rnd = _r.Random(13)
    c = GL / 2
    pts = []
    while len(pts) < 70:
        x, y = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
        if x * x + y * y <= 1:
            pts.append((x, y, rnd.random()))
    alphas = [30, 70, 110, 130, 115, 125, 100, 80, 60, 42, 26, 14, 6, 0]
    out = []
    for i, a in enumerate(alphas):
        im = blank(GL)
        d = ImageDraw.Draw(im)
        r = min(GL / 2 - 6, 8 + 3 * i)
        d.ellipse((c - r * 0.5, c - r * 0.25, c + r * 0.5, c + r * 0.25), fill=(150, 80, 240, a // 3))
        for x, y, w in pts:
            if w < 0.35 + 0.05 * (i % 3):
                d.point((round(c + x * r), round(c + y * r * 0.5)), fill=(186, 120, 255, int(a * (0.5 + w))))
        out.append(im)
    return out


def caster_frames():
    """v9's charge, an earlier release, then the v7 shadow-nova burst over the body with the six bolts."""
    rnd = random.Random(5)
    side = SL * SX
    pil = V.pillar(side)
    seq = list(range(1, 8)) + list(range(23, 31))
    nova_src = K.squared(K.frames("fx_f4_shadownova"))
    nova_idx = list(range(0, 12)) + [13, 15]   # the last frames turn red, off palette
    # v7 anchor: shadow nova row 98 on the body (0.4 h above the clip centre), factor 1 against the 196 px sheet.
    k = side / nova_src[0].width
    nova = []
    for i in nova_idx:
        f = nova_src[i].resize((side, side), Image.LANCZOS)
        oy = int(round(side / 2 - 0.4 * side / 3 - 98 * k))
        cv = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        cv.paste(f, (0, oy), f)
        nova.append(cv)
    body = (SC, SC - 0.4 * SH)
    feet_y = SC + 0.4 * SH
    mids = [p for pair in V.hex_mids(SC, SC, SH, SH / 2) for p in pair]
    n = RELEASE + len(nova)
    assert n * side <= 4096, n
    out = []
    for t in range(n):
        lt = blank()
        if t < RELEASE:
            for _ in range(1 + t // 2):
                a = (body[0] + rnd.uniform(-5, 5), body[1] + rnd.uniform(-12, 10))
                b = (body[0] + rnd.uniform(-7, 7), body[1] + rnd.uniform(-12, 12))
                V.draw_bolt(lt, V.jag(a, b, 0.6, rnd, 3), 2 if t > 4 else 1)
            if t >= 4:
                g = (body[0] + rnd.choice((-1, 1)) * rnd.uniform(6, 12), feet_y + rnd.uniform(-1, 2))
                V.draw_bolt(lt, V.jag((body[0], body[1] + 6), g, 0.5, rnd, 3), 1)
        else:
            j = t - RELEASE
            if j < 8:
                heat = 2 if j < 3 else (1 if j < 6 else 0)
                lit = mids if j < 4 else rnd.sample(mids, max(0, 6 - j))
                for m in lit:
                    far = (SC + 1.6 * (m[0] - SC), SC + 1.6 * (m[1] - SC))
                    path = V.jag((body[0], body[1] + 4), m, 0.35, rnd) + V.jag(m, far, 0.6, rnd, 3)[1:]
                    V.draw_bolt(lt, path, heat, 2 if j < 5 else 0, rnd, upto=min(1.0, 0.5 + 0.5 * j))
        c = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        if t < len(seq):
            c.alpha_composite(pil[seq[t]])
        if t >= RELEASE:
            c.alpha_composite(nova[t - RELEASE])
        c.alpha_composite(lt.resize((side, side), Image.NEAREST))
        out.append(c)
    return out


def lead(frs, n, size):
    return [Image.new("RGBA", (size, size), (0, 0, 0, 0)) for _ in range(n)] + frs


def clips():
    up = lambda frs, s, x: [f.resize((s * x, s * x), Image.NEAREST) for f in frs]  # noqa: E731
    return {
        "caster": (caster_frames(), C_MS, 3),
        "strike_a": (lead(up(strike_sky(), SL, SX), LEAD, SL * SX), S_MS, 3),
        "strike_b": (lead(up(strike_ground(), SL, SX), LEAD, SL * SX), S_MS, 3),
        "glow": (lead(up(glow_frames(), GL, GX), LEAD, GL * GX), G_MS, 2),
    }


def main():
    for cid, (frs, ms, scale) in clips().items():
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(HERE, f"anim_fcf_v10_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px "
              f"({px * len(frs)} px tall), {b} bytes")


if __name__ == "__main__":
    main()
