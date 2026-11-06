#!/usr/bin/env python3
"""An Absence: the Silence's anti-camping summon (director, 2026-11-05: "a really cool high quality explosion type
animation that splatters the ground around it ... like the Shaper fight where the balls of energy trail you and
explode into a dot ground effect").

    python3 art/mother_of_echoes_fx/build_fx_absence.py [--out DIR]

The Silence sets it on the empty hex next to the player (the omen); on its next turn it erupts into a Hush pool on its
own hex and the six around it, and is gone. Material (SAYO_BIBLE.md 2.4, 4.2): the Silence is absence: matte ink that
reflects nothing, unlit except the teal in its veins; pools keep the danger grammar's bile edge so the splatter reads
as a pool on both boards. Pieces (per-hex: the eruption is relative to the summon, so no slicing):
- avatar_moe_absence_a7.webp        AI avatar, 1:1: a small knot of ink with teal veins, low in the frame.
- anim_moe_absence_rise_a7.webp     appear on the summon: a drop of ink falls, splashes, gathers into the knot.
- anim_moe_absence_idle_a7.webp     static loop on the summon's tag: the floor round it is drawn in; the teal veins
                                    pulse faster through the loop (tension), portrait-clear.
- anim_moe_absence_burst_a7.webp    the eruption's centre clip: it inhales (ink and motes drawn in), HOLDS (the core
                                    contracts, veins white), bursts: ink thrown out across the clip, droplets, settle.
- anim_moe_absence_splat_a7.webp    the pool effect's appear on all seven hexes: ink lands as dots (led to land just
                                    after the burst) and dries into the tile.
- tile_moe_absence_dots_a7.webp     the pool tile: splattered ink dots with a bile rim and teal glints; static only
                                    (stacking rule 1: a 7-hex pool may loop, but the dots read without one).
"""
import argparse
import importlib.util
import json
import math
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("build_fx_a4", os.path.join(HERE, "build_fx_a4.py"))
A4 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(A4)
A, F = A4.A, A4.F
N = F.N
INK = (14, 10, 22)
INK_HI = (40, 36, 58)          # the only "light" on ink: a matte rim, no reflection
VEIN, VEIN_LIT = A.PAL["III"]["vein"], A.VEIN_LIT
BILE, BILE_DEEP, BILE_HOT = F.BILE, F.BILE_DEEP, F.BILE_HOT
CX, CY = 25, 27                 # the knot sits on the floor of its hex, a little below the clip centre
SPLAT_LEAD = 7                  # the splat lands this many frames after the eruption starts (the burst's payoff frame)


def knot(f, r, vein_on=1.0, squash=1.0, cx=CX, cy=CY):
    """The Absence itself: a matte ink knot, lumpy, with teal veins inside (vein_on 0..1 brightness, 2 = white-hot)."""
    n = F.frame()
    d = ImageDraw.Draw(n)
    rr = r
    d.ellipse([cx - rr, cy - rr * squash, cx + rr, cy + rr * squash], fill=(*INK, 255))
    for a, k in ((30, 0.55), (150, 0.5), (260, 0.6)):
        x, y = cx + rr * 0.7 * math.cos(math.radians(a)), cy + rr * 0.7 * squash * math.sin(math.radians(a))
        d.ellipse([x - rr * k, y - rr * k * squash, x + rr * k, y + rr * k * squash], fill=(*INK, 255))
    F.outline_alpha(n, INK_HI)
    if vein_on > 0:
        col = VEIN if vein_on < 1 else (VEIN_LIT if vein_on < 2 else (255, 255, 250))
        for a in (20, 140, 250, 320):
            x1, y1 = cx + rr * 0.8 * math.cos(math.radians(a)), cy + rr * 0.8 * squash * math.sin(math.radians(a))
            mx, my = cx + rr * 0.35 * math.cos(math.radians(a + 35)), cy + rr * 0.35 * math.sin(math.radians(a + 35))
            F.seg(n, (cx, cy), (mx, my), col)
            F.seg(n, (mx, my), (x1, y1), col)
    f.alpha_composite(n)


def dot(f, x, y, r, rim=True, ry=None):
    n = F.frame()
    ry = r * 0.6 if ry is None else ry
    ImageDraw.Draw(n).ellipse([x - r, y - ry, x + r, y + ry], fill=(*INK, 255))
    F.outline_alpha(n, BILE if rim else INK_HI)
    f.alpha_composite(n)


def avatar():
    """1:1 AI avatar: the knot drawn on a 64 px grid and scaled up hard-edged, transparent ground."""
    f = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    g = F.frame()
    knot(g, 11, 1.0, 1.0, 25, 28)
    for k, a in enumerate((200, 250, 300, 340)):                 # wisps drawn toward it
        x, y = 25 + 17 * math.cos(math.radians(a)), 28 + 15 * math.sin(math.radians(a))
        A4.cluster(g, x, y, INK if k % 2 else VEIN, INK_HI)
    f.alpha_composite(g.resize((64, 64), Image.NEAREST))
    return f.resize((1152, 1152), Image.NEAREST)


def rise():
    """A drop of ink falls onto the hex, splashes flat, and gathers back up into the knot; the veins light last."""
    out = []
    for i in range(14):
        f = F.frame()
        if i < 4:                                                 # the drop falls
            y = 8 + i * 5
            dot(f, CX, y, 2.5, rim=False)
        elif i < 7:                                               # it splashes flat
            u = (i - 3) / 3
            n = F.frame()
            ImageDraw.Draw(n).ellipse([CX - 4 - 9 * u, CY + 3 - 2 * u, CX + 4 + 9 * u, CY + 3 + 2 * u], fill=(*INK, 255))
            F.outline_alpha(n, INK_HI)
            f.alpha_composite(n)
            for k in range(4):
                A4.cluster(f, CX + (k - 1.5) * (6 + 4 * u), CY - 1 - 3 * u + (k % 2) * 2, INK, INK_HI)
        else:                                                     # it gathers into the knot; veins light, held
            u = A4.ease((i - 6) / 4)
            knot(f, 3 + 5 * u, 0 if i < 10 else (1.5 if i in (11, 12) else 1.0), 0.6 + 0.4 * u)
        out.append(f)
    return A4.edge_check("absence rise", out)


def idle():
    """32-frame loop (1.6 s): the floor round it is drawn in toward the knot; vein pulses come faster each beat
    (period 10, 8, 6, 4, 4 frames): it is about to go off. Clear of the knot itself (the avatar shows it)."""
    out = []
    beats = [0, 10, 18, 24, 28]
    for i in range(32):
        f = F.frame()
        since = min(i - b for b in beats if b <= i)
        lit = since < 2
        for k in range(8):                                       # ink motes drawn in, on a ring at the hex rim
            a = math.radians(k * 45 + i * 4)
            r = 19 - ((i * 1.5 + k * 5) % 12)
            x, y = CX + r * math.cos(a), CY + 4 + r * 0.5 * math.sin(a)
            A4.cluster(f, x, y, VEIN_LIT if (lit and k % 2 == 0) else INK, INK_HI)
        if lit:                                                  # the floor pulse: a thin ink ring tightens on the beat
            F.ground_ring(f, 15 - since * 3, 7 - since * 1.5, [(0, VEIN), (1, INK)], cx=CX, cy=CY + 4)
        out.append(f)
    return A4.edge_check("absence idle", out)


FROST = (150, 160, 174)
FROST_D = (70, 84, 98)


def frost_bit(f, x, y):
    A4.cluster(f, x, y, FROST, INK)


def splash(f, cx, cy, r, lobes, rot, squash=0.6, seed=0):
    """A jagged ink splash: a body with pointed lobes, outlined matte (no gloss), teal cracks inside."""
    rnd = random.Random(seed)
    pts = []
    for k in range(lobes * 2):
        a = math.radians(rot + k * 180 / lobes)
        rr = r * (1.0 if k % 2 == 0 else 0.45) * rnd.uniform(0.85, 1.1)
        pts.append((cx + rr * math.cos(a), cy + rr * squash * math.sin(a)))
    n = F.frame()
    ImageDraw.Draw(n).polygon(pts, fill=(*INK, 255))
    F.outline_alpha(n, (206, 210, 222))          # frost on the edge: the ink reads against ink floors and dark boards
    F.outline_alpha(n, INK)
    f.alpha_composite(n)


def burst():
    """The eruption, one picture in the centre clip (the column stagger stops exact slicing for a summon-relative cast,
    so the whole explosion lives in the clip centred on the Absence and reaches into its neighbours; the ring pieces
    carry the splatter beyond). Inhale (6 frames: frost and ink stream in, the knot swells, veins brighten) -> HOLD
    (2 frames: a ring of frost frozen mid-air round a white-veined knot; nothing moves) -> one white-teal frame ->
    burst (ink thrown out in pointed petals, frost shattering outward, teal cracks running across the floor) ->
    settle (the ink drops to a stain, frost drifts down). 22 frames."""
    rnd = random.Random(5)
    shards = [(rnd.uniform(0, 360), rnd.uniform(0.75, 1.0)) for _ in range(12)]
    out = []
    for i in range(22):
        f = F.frame()
        if i < 6:                                                # inhale
            u = A4.ease((i + 1) / 6)
            for k in range(12):
                a = math.radians(k * 30 + 15 + 20 * u)
                r = 21 - 13 * u
                (frost_bit if k % 2 else (lambda f_, x_, y_: A4.cluster(f_, x_, y_, INK, INK_HI)))(
                    f, CX + r * math.cos(a), CY + r * 0.6 * math.sin(a))
            F.ground_ring(f, 12 - 4 * u, 6 - 2 * u, [(0, INK), (1, INK)], cx=CX, cy=CY + 3)
            knot(f, 6 + 3 * u, 1.0 + 0.6 * u)
        elif i < 8:                                              # the hold: frost frozen mid-air, stillness
            for k in range(10):
                a = math.radians(k * 36)
                frost_bit(f, CX + 11 * math.cos(a), CY + 7 * math.sin(a) - 2)
            knot(f, 6, 2.0)
        elif i == 8:                                             # the impact frame
            F.ground_ring(f, 7, 4, [(0, VEIN_LIT), (1, (255, 255, 250)), (2, VEIN_LIT), (3, INK)], cx=CX, cy=CY)
            knot(f, 4, 2.0)
        else:                                                    # the burst and its settle
            v = i - 9
            t = A4.ease((v + 1) / 4)
            if v < 3:                                            # the frost shock runs out (value, not colour)
                F.ground_ring(f, 9 + 5 * v, 5 + 3 * v, [(0, (206, 210, 222)), (1, (255, 255, 250)), (2, INK)], cx=CX, cy=CY + 1)
            if v < 8:                                            # teal cracks run out across the floor
                for k in range(6):
                    a = math.radians(k * 60 + 30)
                    L = 6 + 14 * min(1, v / 3)
                    p0 = (CX, CY + 2)
                    p1 = (CX + L * math.cos(a), CY + 2 + L * 0.5 * math.sin(a))
                    F.seg(f, p0, p1, VEIN_LIT if v < 3 else VEIN)
            if v < 7:                                            # the ink petals
                splash(f, CX, CY - (2 if v < 3 else 0) + 0.4 * max(0, v - 3) ** 2, 6 + 11 * t, 7, 10 + v * 3,
                       0.62, seed=v)
                if v < 4:
                    splash(f, CX, CY, 4 + 4 * t, 5, 40, 0.62, seed=11)
            else:                                                # settled: a stain, the last ink beading
                w = 1 - (v - 7) / 6
                if w > 0:
                    n = F.frame()
                    ImageDraw.Draw(n).ellipse([CX - 12 * w - 3, CY - 4 * w, CX + 12 * w + 3, CY + 4 * w + 1], fill=(*INK, 255))
                    F.outline_alpha(n, INK_HI)
                    f.alpha_composite(n)
            for a, sp in shards:                                 # frost shattering outward, then drifting down
                r = (5 + 15 * sp) * t
                x = CX + r * math.cos(math.radians(a))
                y = CY + r * 0.6 * math.sin(math.radians(a)) - 7 * math.sin(math.pi * min(1, v / 7)) + 0.15 * v * v
                if v < 11 and 5 <= x <= 45 and 5 <= y <= 45:
                    frost_bit(f, x, y)
        out.append(f)
    return A4.edge_check("absence burst", out)


SPLAT_LEAD = 9


def splat():
    """The splatter on each of the seven hexes (one strip for all: drawn symmetric, so the column stagger cannot break
    it), led to land on the burst: ink drops fall in, splash into a small star-shaped stain with radial streaks, frost
    flecks settle on it, it holds, then gives way to the floor tile under it."""
    out = [F.frame() for _ in range(SPLAT_LEAD)]
    for i in range(10):
        f = F.frame()
        if i < 2:
            for k in range(5):
                A4.cluster(f, 25 + (k - 2) * 6, 17 + 4 * i + (k % 2) * 2, INK, INK_HI)
        elif i < 8:
            u = A4.ease((i - 1) / 3)
            splash(f, 25, 25, 5 + 7 * u, 6, 15, 0.5, seed=3)
            for k in range(6):                                   # radial streaks
                a = math.radians(k * 60)
                p0 = (25 + (6 + 5 * u) * math.cos(a), 25 + (3 + 2.5 * u) * math.sin(a))
                p1 = (25 + (9 + 9 * u) * math.cos(a), 25 + (4.5 + 4.5 * u) * math.sin(a))
                n = F.frame()
                ImageDraw.Draw(n).line([p0, p1], fill=(*INK, 255), width=2)
                F.outline_alpha(n, (206, 210, 222))
                f.alpha_composite(n)
            if i >= 4:
                for x, y in ((20, 23), (31, 26), (26, 29)):
                    frost_bit(f, x, y)
        else:
            for x, y in ((20, 23), (31, 26), (26, 29)):
                frost_bit(f, x, y + (i - 7))
        out.append(f)
    return A4.edge_check("absence splat", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=F.EXPORTS)
    ap.add_argument("--avatar-out", default=os.path.join(F.ROOT, "art", "mother_of_echoes", "exports"))
    a = ap.parse_args()
    rows = []
    for name, frames, note in (("anim_moe_absence_rise_a7.webp", rise(), "An Absence arrives (summon appear)"),
                               ("anim_moe_absence_idle_a7.webp", idle(), "An Absence waits (summon loop, tightening)"),
                               ("anim_moe_absence_burst_a9.webp", burst(), "An Absence erupts: one painted burst in the centre clip"),
                               ("anim_moe_absence_splat_a9.webp", splat(), "An Absence: the splatter on the seven hexes (symmetric)")):
        p = os.path.join(a.out, name)
        F.strip(frames).save(p, lossless=True, quality=100, method=6)
        rows.append({"file": f"art/mother_of_echoes_fx/exports/{name}", "type": "ANIMATION", "frames": len(frames),
                     "speed": F.MS, "bytes": os.path.getsize(p), "note": note})
    p = os.path.join(a.avatar_out, "avatar_moe_absence_a7.webp")
    avatar().save(p, lossless=True, quality=100, method=6)
    with open(os.path.join(a.out, "moe_fx_absence.json"), "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/build_fx_absence.py", "assets": rows,
                   "avatar": "art/mother_of_echoes/exports/avatar_moe_absence_a7.webp", "splat_lead": SPLAT_LEAD}, fh, indent=1)
        fh.write("\n")
    print(len(rows), "FX + avatar")


if __name__ == "__main__":
    main()
