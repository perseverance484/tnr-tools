#!/usr/bin/env python3
"""Forbidden Chakra Fury v9: the caster charges and releases violet chakra lightning that runs out into a field of
lightning veins joined across every hex (2026-11-20).

    TNR_DUELYST=<cache> python3 art/jutsu_icons/forbidden_chakra_fury/animation/v9/build_v9.py

Director: the tiles should be "violet streaks of chakra" like the jutsu icon (branching violet lightning, white-hot
cores), and "the center piece should be part of that animation. It should look like the user casting the jutsu. Not a
random poof of smoke."
- CASTER (visual tag, scale 3, 80 ms): the Duelyst gate pillar (fx_f2_eightgates_purpleflame, CC0) ignites around the
  user while lightning crawls over the body and arcs to the ground; at frame 10 the user releases: six bolts run from
  the body through the six edge midpoints of the caster's hex and on into the neighbours, where the field's veins
  begin. The shadow nova is gone.
- FIELD (recoil tag, scale 2, 70 ms): drawn here, in the same chunky pixel scale. Every tile carries three veins, one
  per pair of opposite edge midpoints, so each vein meets its neighbour's at the shared edge: the field reads as one
  network running out from the caster. Lead frames hold it until the caster's bolts reach the edges; then the veins
  strike from the edges inward, crackle (re-drawn every frame, the three directions flickering in turn), and fade.
Pixel scale: one drawn pixel is h/28 on the board in both clips (caster 84 px drawn x2, field 56 px drawn x3). Every
strip <= 4096 px tall.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SKILL = os.environ.get("TNR_ART_SCRIPTS", os.path.join(REPO, "skills", "producing-tnr-art", "scripts"))
sys.path.insert(0, SKILL)
import duelyst_kit as K  # noqa: E402
import fx_recipe as R  # noqa: E402

GLOW = (112, 38, 214, 120)
MID = (176, 104, 255, 255)
HOT = (238, 222, 255, 255)
DIM = (130, 70, 230, 200)
LICENSE = "CC0 1.0 - OpenDuelyst (open-duelyst/duelyst), fx_f2_eightgates_purpleflame, adapted for TNR; lightning drawn for TNR"


def jag(a, b, amp, rnd, depth=4):
    """Midpoint-displacement lightning from a to b (end points fixed)."""
    pts = [a, b]
    for d in range(depth):
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            dx, dy = q[0] - p[0], q[1] - p[1]
            ln = math.hypot(dx, dy) or 1
            off = rnd.uniform(-1, 1) * amp * ln / (1.6 ** d) / 2
            out += [(mx - dy / ln * off, my + dx / ln * off), q]
        pts = out
    return [(round(x), round(y)) for x, y in pts]


def draw_bolt(layer, pts, heat, branches=0, rnd=None, upto=1.0):
    """heat 2: white core; 1: violet; 0: dim. upto: fraction of the path drawn (a bolt growing)."""
    n = max(2, int(len(pts) * upto))
    pts = pts[:n]
    d = ImageDraw.Draw(layer)
    d.line(pts, fill=GLOW, width=3)
    d.line(pts, fill={2: HOT, 1: MID, 0: DIM}[heat], width=1)
    for _ in range(branches):
        i = rnd.randrange(1, len(pts) - 1)
        p = pts[i]
        ang = rnd.uniform(0, 2 * math.pi)
        ln = rnd.uniform(3, 7)
        q = (p[0] + math.cos(ang) * ln, p[1] + math.sin(ang) * ln * 0.6)
        br = jag(p, q, 0.5, rnd, 2)
        d.line(br, fill=GLOW, width=2)
        d.line(br, fill=MID if heat else DIM, width=1)


def hex_mids(cx, cy, hw, hh):
    """Edge midpoints of a flat-top hex (half width hw, half height hh), as opposite pairs."""
    top, bot = (cx, cy - hh), (cx, cy + hh)
    ul, lr = (cx - 0.75 * hw, cy - hh / 2), (cx + 0.75 * hw, cy + hh / 2)
    ur, ll = (cx + 0.75 * hw, cy - hh / 2), (cx - 0.75 * hw, cy + hh / 2)
    return [(top, bot), (ul, lr), (ur, ll)]


# ------------------------------------------------------------------------------------------------- field
FL, FX, F_MS, F_LEAD = 56, 3, 70, 12


def field_frames():
    rnd = random.Random(9)
    pairs = hex_mids(FL / 2, FL / 2, FL / 2, FL / 4)
    out = [Image.new("RGBA", (FL, FL), (0, 0, 0, 0)) for _ in range(F_LEAD)]
    plan = [  # (grow, heat, which pairs lit, branches): all three strike, then two at a time, flickering
        (0.5, 2, (0, 1, 2), 0), (1.0, 2, (0, 1, 2), 2), (1, 2, (0, 2), 3), (1, 1, (1,), 2), (1, 2, (1, 2), 3),
        (1, 1, (0,), 2), (1, 2, (0, 1), 2), (1, 1, (2,), 2), (1, 0, (1, 2), 1), (1, 0, (0,), 1),
        (1, 0, (2,), 0), (0, 0, (), 0)]
    for grow, heat, lit, br in plan:
        im = Image.new("RGBA", (FL, FL), (0, 0, 0, 0))
        for k in lit:
            a, b = pairs[k]
            if grow < 1:   # strike from both edges toward the middle
                m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                for e in (a, b):
                    draw_bolt(im, jag(e, m, 0.7, rnd), heat, 0, rnd, upto=grow * 2)
            else:
                draw_bolt(im, jag(a, b, 0.7, rnd), heat, br, rnd)
        out.append(im)
    return [f.resize((FL * FX, FL * FX), Image.NEAREST) for f in out]


# ------------------------------------------------------------------------------------------------ caster
CL, CX, C_MS, RELEASE = 84, 2, 80, 10
H = CL / 3                       # tile height in drawn px (clip = 3 tile heights)
CENTRE = CL / 2
BODY = (CENTRE, CENTRE - 0.4 * H)
FEET_Y = CENTRE + 0.4 * H


def pillar(side):
    src = K.squared(K.frames("fx_f2_eightgates_purpleflame"))
    top, base = 3, 169                       # union bbox rows of the pillar
    h = side / 3
    k = 1.7 * h / (base - top)
    s = int(round(src[0].width * k))
    feet = side / 2 + 0.4 * h
    frames = []
    for f in src:
        c = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        c.alpha_composite(f.resize((s, s), Image.LANCZOS), (int(side / 2 - s / 2), int(feet - base * k)))
        frames.append(c)
    return frames


def caster_frames():
    rnd = random.Random(5)
    side = CL * CX
    pil = pillar(side)
    seq = list(range(1, 11)) + list(range(23, 31))       # ignite + roar, then the collapse under the release
    mids = [p for pair in hex_mids(CENTRE, CENTRE, H, H / 2) for p in pair]
    n = RELEASE + 10
    out = []
    for t in range(n):
        lt = Image.new("RGBA", (CL, CL), (0, 0, 0, 0))
        if t < RELEASE:                                   # charge: arcs crawl over the body, then reach the ground
            for _ in range(1 + t // 3):
                a = (BODY[0] + rnd.uniform(-5, 5), BODY[1] + rnd.uniform(-12, 10))
                b = (BODY[0] + rnd.uniform(-7, 7), BODY[1] + rnd.uniform(-12, 12))
                draw_bolt(lt, jag(a, b, 0.6, rnd, 3), 2 if t > 6 else 1)
            if t >= 6:
                g = (BODY[0] + rnd.choice((-1, 1)) * rnd.uniform(6, 12), FEET_Y + rnd.uniform(-1, 2))
                draw_bolt(lt, jag((BODY[0], BODY[1] + 6), g, 0.5, rnd, 3), 1)
        else:                                             # release: six bolts to the hex edges, then flicker out
            k = t - RELEASE
            heat = 2 if k < 4 else (1 if k < 7 else 0)
            grow = min(1.0, 0.5 + 0.5 * k)
            lit = mids if k < 5 else rnd.sample(mids, max(0, 6 - k))
            for m in lit:                                 # body -> the edge midpoint -> on toward the neighbour
                far = (CENTRE + 1.6 * (m[0] - CENTRE), CENTRE + 1.6 * (m[1] - CENTRE))
                path = jag((BODY[0], BODY[1] + 4), m, 0.35, rnd) + jag(m, far, 0.6, rnd, 3)[1:]
                draw_bolt(lt, path, heat, 2 if k < 6 else 0, rnd, upto=grow)
            if k < 2:
                ImageDraw.Draw(lt).ellipse((BODY[0] - 5 + k, BODY[1] - 5 + k, BODY[0] + 5 - k, BODY[1] + 5 - k),
                                           fill=HOT if k == 0 else MID)
        c = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        if t < len(seq):
            c.alpha_composite(pil[seq[t]])
        c.alpha_composite(lt.resize((side, side), Image.NEAREST))
        out.append(c)
    return out


def main():
    out = HERE
    clips = []
    for cid, role, scale, ms, frs, effect in (
            ("caster", "caster", 3, C_MS, caster_frames(), "visual"),
            ("field", "field", 2, F_MS, field_frames(), "recoil")):
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(out, f"anim_fcf_v9_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, {px} px ({px * len(frs)} px tall), {b} bytes")
        clips.append(({"id": cid, "role": role, "scale": scale, "ms": ms, "effect": effect}, frs))
    g = os.path.join(out, "preview_fcf_v9_board.gif")
    R.board(clips, g, title="Forbidden Chakra Fury v9", shrink=1.0)
    print(f"board: {g}")


if __name__ == "__main__":
    main()
