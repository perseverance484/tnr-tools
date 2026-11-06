#!/usr/bin/env python3
"""The Mother of Echoes boss entrances (art4; director feedback on the live test, 2026-11-05: "Boss intro animation
was a bit underwhelming but the aura was cool").

    python3 art/mother_of_echoes_fx/build_fx_a4.py

One signature entrance per form, on the full clip square (2.5 hex heights), anticipation -> reveal (with hold frames)
-> settle, 30 frames (1.5 s at 50 ms):
- sayo1   Heartglass light gathers, the fan of framed Heartglass blades opens behind her, a prismatic burst.
- silence the ink spreads under her and a shadow far larger than her stands up off the floor, bone wisps, then smoke.
- sayo2   the gold etch ring is traced and ignites, spokes flare, then the Remainder's black cracks creep over it.
- saint   black glass gathers in, bursts out as thorned shards with lit teal veins and bone tendrils, then falls.
Each form also has a ground piece for the visual ring around her hex (two bands, w0 / w1), timed to land on the
reveal: a Heartglass pane springing up, a shadow tendril standing up, the etch lattice igniting and cracking, a black
thorn bursting up.
Engine (docs/design/COMBAT_ANIMATION_ENGINE.md, theninjarpg@3314d122): 50 px rendition + linear stretch, so solid 2-3
px clusters and 1 px outlines; hard alpha; 1 px clear margin; the AI portrait disc (build_fx.AI_DISC) stays clear
(the clip draws above the portrait) except for the one-frame rim flash. The approved art3 auras are unchanged.
Writes exports/*_a4.webp and exports/moe_fx_a4.json. Pillow only.
"""
import importlib.util
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, file):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


A = _load("build_fx_a3", "build_fx_a3.py")
F = A.F
N = F.N
PAL, VEIN_LIT, BONE, BONE_S = A.PAL, A.VEIN_LIT, A.BONE, A.BONE_S
WHITE, SCORE, EMB_Y = F.WHITE, F.SCORE, F.EMBER_YEL
(PCX, PCY), PR = F.AI_DISC
INK = (14, 10, 24)
PRISM = ((255, 170, 170), (170, 255, 210), (190, 180, 255), (255, 236, 160))
LEN = 30
REVEAL = 9          # the frame the reveal lands on; the ring bands are timed to it
WAVE = 3            # ring band 1 trails band 0 by 150 ms


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def disc_clear(frames, flash=()):
    """Clear the portrait disc (the clip draws above it); `flash` frames keep a 1 px rim inside it."""
    out = []
    for i, f in enumerate(frames):
        m = Image.new("L", (N, N), 0)
        r = PR - (1.5 if i in flash else 0)
        ImageDraw.Draw(m).ellipse([PCX - r, PCY - r, PCX + r, PCY + r], fill=255)
        a = f.getchannel("A")
        a.paste(0, (0, 0), m)
        f.putalpha(a)
        out.append(f)
    return out


def star(f, x, y, col, s=2):
    for k in range(-s, s + 1):
        F.px(f, x + k, y, col)
        F.px(f, x, y + k, col)
    F.px(f, x, y, WHITE)


def at(r, deg, cy=PCY, cx=PCX, ry=1.0):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a) * ry


# ------------------------------------------------------------------------------------------------ Act I: Heartglass fan
def blade(f, deg, r0, r1, w, hot=False, keep_glint=None):
    """A framed Heartglass blade (kite pane) from radius r0 to r1 at angle deg."""
    p = PAL["I"]
    base_l, base_r = at(r0, deg - w), at(r0, deg + w)
    mid_l, mid_r = at((r0 + r1) * 0.55, deg - w * 0.55), at((r0 + r1) * 0.55, deg + w * 0.55)
    tip = at(r1, deg)
    n = F.frame()
    d = ImageDraw.Draw(n)
    d.polygon([base_l, mid_l, tip, mid_r, base_r], fill=(*(p["hot"] if hot else p["lite"]), 255))
    d.polygon([at(r0, deg), mid_r, tip], fill=(*p["body"], 255))
    d.line([at(r0, deg), tip], fill=(*WHITE, 255))
    F.outline_alpha(n, p["frame"])
    f.alpha_composite(n)
    if keep_glint is not None:
        g = at(r0 + (r1 - r0) * keep_glint, deg)
        star(f, g[0], g[1], p["hot"], 1)


def flourish_sayo1():
    p = PAL["I"]
    fr = []
    for i in range(LEN):
        f = F.frame()
        if i < REVEAL:                                     # anticipation: prismatic motes spiral in, a ring tightens
            t = i / REVEAL
            for k in range(12):
                a = k * 30 + 140 * (1 - t)
                r = PR + 2 + (1 - ease(t)) * 22
                x, y = at(r, a)
                F.blob(f, x, y, PRISM[k % 4] if k % 3 else WHITE, r=1)
            F.thick_arc(f, PCX, PCY, PR + 1 + (1 - t) * 6, 0, 360, [(0, p["lite"])], 1.0)
        elif i < REVEAL + 2:                               # the flash: a Heartglass ring, hold 2 frames
            F.thick_arc(f, PCX, PCY, PR, 0, 360, [(-1, WHITE), (0, WHITE), (1, p["hot"]), (2, p["lite"]), (3, p["frame"])])
            for k in range(8):
                x, y = at(PR + 7, k * 45 + 22)
                star(f, x, y, PRISM[k % 4], 2)
        if i >= REVEAL:                                    # the fan opens behind her, from straight down outwards
            t = ease((i - REVEAL) / 6)
            fade = 1.0 if i < 22 else max(0.0, 1 - (i - 22) / 7)
            n_bl = 9
            for k in range(n_bl):
                target = 15 + k * (150 / (n_bl - 1))      # 15..165 degrees: the lower half fan (y down)
                deg = 90 + (target - 90) * t
                r1 = PR + 8 + (10 if 50 < target < 130 else 5) * t
                if fade < 1 and (k + i) % 3 == 0 and fade < 0.6:
                    continue
                if fade > 0.25:
                    glint = ((i - REVEAL - k) % 10) / 10 if i >= REVEAL + 6 else None
                    blade(f, deg, PR - 3, r1 * (0.7 + 0.3 * fade), 9, hot=(i < REVEAL + 3), keep_glint=glint)
            if REVEAL + 1 <= i <= REVEAL + 8:              # the prismatic burst: rays out of the rim
                u = (i - REVEAL - 1) / 7
                for k in range(16):
                    a = k * 22.5 + 11
                    r0 = PR + 3 + u * 16
                    col = PRISM[k % 4]
                    F.seg(f, at(r0, a), at(r0 + 4 * (1 - u) + 1, a), col)
            if i >= 20:                                    # settle into the aura: six facets orbit in
                for k in range(6):
                    x, y = at(PR + 4, k * 60 + (i - 20) * 9, ry=0.9)
                    n = F.frame()
                    ImageDraw.Draw(n).polygon([(x, y - 3), (x + 2, y), (x, y + 3), (x - 2, y)], fill=(*p["lite"], 255))
                    F.px(n, x, y, WHITE)
                    F.outline_alpha(n, p["seam"])
                    f.alpha_composite(n)
        fr.append(f)
    return disc_clear(fr, flash=(REVEAL,))


# ------------------------------------------------------------------------------------------------ the Silence: the shadow stands up
def shadow_shape(f, rise, vein_on, scale=1.0):
    """A hooded shadow far larger than her portrait, standing up behind it from the floor: `rise` 0 (flat) .. 1."""
    hy = PCY - 3 + (1 - rise) * 30                         # head centre
    hr = (PR + 7) * scale
    n = F.frame()
    d = ImageDraw.Draw(n)
    d.ellipse([PCX - hr, hy - hr * 1.1, PCX + hr, hy + hr], fill=(*INK, 255))
    sh = hy + hr * 0.6                                     # shoulders spread to the frame edge, down to the floor
    hem = []                                               # a robe that flares to a ragged hem on the floor
    for k in range(13):
        x = PCX - hr - 8 + k * (2 * hr + 16) / 12
        hem.append((x, 47 - (3 if k % 2 else 0) - 2 * abs(math.sin(k * 1.7))))
    d.polygon([(PCX - hr + 1, sh), (PCX + hr - 1, sh), *reversed(hem)], fill=(*INK, 255))
    for k in (-1, 1):                                      # ragged sleeves reaching out
        d.polygon([(PCX + k * (hr - 2), sh), (PCX + k * (hr + 9), sh + 9), (PCX + k * (hr + 5), sh + 11),
                   (PCX + k * (hr + 8), sh + 15), (PCX + k * (hr - 1), sh + 12)], fill=(*INK, 255))
    d.polygon([(PCX - 4, hy - hr * 1.1 - 4 * rise), (PCX + 4, hy - hr * 1.1 - 4 * rise), (PCX, hy - hr)],
              fill=(*INK, 255))                            # the hood's point
    F.outline_alpha(n, PAL["III"]["lite"])
    if vein_on:                                            # teal crack veins in the shadow
        for k, (a, L) in enumerate(((200, 9), (-20, 9), (150, 7), (30, 7), (110, 12), (70, 12))):
            x0, y0 = PCX + (hr - 1) * math.cos(math.radians(a)), hy + (hr - 1) * math.sin(math.radians(a))
            x1, y1 = x0 + L * math.cos(math.radians(a + 25)), y0 + L * math.sin(math.radians(a + 25))
            F.seg(n, (x0, y0), (x1, y1), VEIN_LIT if vein_on > 1 else PAL["III"]["vein"])
    f.alpha_composite(n)
    return hy


def tendril(f, x0, y0, ang, L, curl, col, w=1, ph=0.0):
    x, y = x0, y0
    for s in range(int(L)):
        a = math.radians(ang + curl * s / max(1, L) * 90 + 12 * math.sin(ph + s * 0.5))
        x, y = x + math.cos(a), y + math.sin(a)
        F.blob(f, x, y, col, r=w if s < L * 0.5 else 1)
    return x, y


def flourish_silence():
    fr = []
    for i in range(LEN):
        f = F.frame()
        t = i / LEN
        pool = ease(min(1, i / 8)) * (1 if i < 23 else max(0, 1 - (i - 23) / 7))
        if pool > 0.05:                                    # the ink spreads on the floor under her
            n = F.frame()
            rx, ry = 6 + 18 * pool, 2 + 4 * pool
            ImageDraw.Draw(n).ellipse([PCX - rx, 42 - ry, PCX + rx, 42 + ry], fill=(*INK, 255))
            for k in range(5):
                a = k * 72 + 20
                F.seg(n, (PCX, 42), (PCX + rx * 0.9 * math.cos(math.radians(a)), 42 + ry * 0.9 * math.sin(math.radians(a))),
                      PAL["III"]["vein"])
            F.outline_alpha(n, PAL["III"]["frame"])
            f.alpha_composite(n)
        if REVEAL - 2 <= i < 23:                           # the shadow stands up, holds, its veins flare
            rise = ease((i - REVEAL + 2) / 7)
            hy = shadow_shape(f, rise, 2 if REVEAL + 5 <= i <= REVEAL + 7 else (1 if rise > 0.6 else 0))
            if rise > 0.5:                                  # bone wisps off the shoulders
                for side in (-1, 1):
                    for k in range(2):
                        tendril(f, PCX + side * (PR + 7), hy + 8 + k * 6, 90 - side * (80 + k * 25), 9 + k * 3,
                                -side * 0.8, BONE if k == 0 else BONE_S, ph=i * 0.6)
        if i >= 20:                                        # it comes apart as smoke rising past her
            u = (i - 20) / 9
            for k in range(10):
                x = PCX + (k - 4.5) * 4.6 + 2 * math.sin(i * 0.7 + k)
                y = 46 - u * 40 - (k % 3) * 4
                if 0 < y < 49:
                    F.blob(f, x, y, PAL["III"]["smoke"] if k % 2 else INK, r=2 if u < 0.5 else 1)
        fr.append(f)
    return disc_clear(fr, flash=(REVEAL + 6,))


# ------------------------------------------------------------------------------------------------ Act II: the etch ring ignites, then cracks
def flourish_sayo2():
    p = PAL["II"]
    fr = []
    R = PR + 3
    cracks = [(30, 1), (150, -1), (250, 1), (330, -1), (90, 1)]
    for i in range(LEN):
        f = F.frame()
        if i < REVEAL:                                     # traced: the arc grows round her, a hot spark at its head
            sweep = 360 * ease((i + 1) / REVEAL)
            F.thick_arc(f, PCX, PCY, R, -90, -90 + sweep, [(-1, SCORE), (0, F.ETCH_MID), (1, F.ETCH_DIM), (2, SCORE)])
            hx, hy = at(R, -90 + sweep)
            star(f, hx, hy, F.ETCH_HOT, 2)
        else:
            hot = REVEAL <= i < REVEAL + 3
            crack_t = ease((i - REVEAL - 3) / 9) if i >= REVEAL + 3 else 0
            gold = F.ETCH_HOT if hot else (F.ETCH_MID if crack_t < 0.6 else F.ETCH_DIM)
            F.thick_arc(f, PCX, PCY, R, 0, 360, [(-1, SCORE), (0, gold), (1, gold), (2, gold if hot else F.ETCH_DIM),
                                                 (3, SCORE)])
            if i < REVEAL + 10:                            # six etched spokes flare out to the frame edge
                u = ease((i - REVEAL) / 4)
                for k in range(6):
                    a = k * 60 + 30
                    r1 = R + 3 + 18 * u
                    c = F.ETCH_HOT if i < REVEAL + 4 else F.ETCH_MID
                    F.seg(f, at(R + 2, a), at(r1, a), SCORE)
                    F.seg(f, at(R + 2, a, cy=PCY - 1), at(r1, a, cy=PCY - 1), c, keep=1.0 if i < REVEAL + 7 else 0.5)
                    if i < REVEAL + 3:
                        x, y = at(r1, a)
                        star(f, x, y, F.ETCH_HOT, 1)
            if crack_t > 0:                                # the Remainder's black cracks creep over the gold
                for k, (a, sgn) in enumerate(cracks):
                    L = crack_t * (12 + 3 * (k % 2))
                    x, y = at(R, a)
                    pts = [(x, y)]
                    for s in range(int(L)):
                        ang = math.radians(a + sgn * (40 + 25 * math.sin(s * 1.3 + k)))
                        x, y = x + math.cos(ang), y + math.sin(ang)
                        pts.append((x, y))
                    for j, q in enumerate(pts):
                        F.blob(f, q[0], q[1], p["vein"], r=2 if j < len(pts) * 0.6 else 1)
                    if len(pts) > 4:
                        F.blob(f, pts[-1][0], pts[-1][1] - 2, p["smoke"], r=2)
                    for q in pts[::4]:
                        F.px(f, q[0] + 1, q[1] - 1, F.ETCH_HOT if crack_t < 0.5 else F.ETCH_DIM)
            if i >= 23:                                    # the smoke lifts off
                for k in range(5):
                    x, y = at(R + 4 + (i - 23) * 1.2, k * 72 + 10)
                    F.blob(f, x, y - (i - 23), p["smoke"], r=1)
        fr.append(f)
    return disc_clear(fr, flash=(REVEAL,))


# ------------------------------------------------------------------------------------------------ Act III: black glass bursts
def thorn(f, x0, y0, deg, L, w, lit):
    tip = (x0 + L * math.cos(math.radians(deg)), y0 + L * math.sin(math.radians(deg)))
    l = (x0 + w * math.cos(math.radians(deg - 90)), y0 + w * math.sin(math.radians(deg - 90)))
    r = (x0 + w * math.cos(math.radians(deg + 90)), y0 + w * math.sin(math.radians(deg + 90)))
    notch = (x0 + L * 0.45 * math.cos(math.radians(deg - 14)) + w * 0.6 * math.cos(math.radians(deg - 90)),
             y0 + L * 0.45 * math.sin(math.radians(deg - 14)) + w * 0.6 * math.sin(math.radians(deg - 90)))
    n = F.frame()
    d = ImageDraw.Draw(n)
    d.polygon([l, notch, tip, r], fill=(20, 20, 30, 255))
    d.line([(x0, y0), tip], fill=(*(VEIN_LIT if lit else PAL["III"]["vein"]), 255))
    d.line([l, notch, tip], fill=(*PAL["III"]["vein"], 255))
    F.outline_alpha(n, VEIN_LIT if lit else PAL["III"]["frame"])
    f.alpha_composite(n)


def flourish_saint():
    fr = []
    dirs = [k * 30 + 15 for k in range(12)]
    for i in range(LEN):
        f = F.frame()
        if i < REVEAL:                                     # black glass gathers in, the floor darkens
            t = ease(i / (REVEAL - 1))
            for k, a in enumerate(dirs):
                r = PR + 3 + (1 - t) * (16 + 4 * (k % 3))
                x, y = at(r, a + 25 * (1 - t))
                thorn(f, x, y, a + 180, 4, 1.5, k % 4 == 0)
            n = F.frame()
            ImageDraw.Draw(n).ellipse([PCX - 6 - 12 * t, 42 - 2 - 3 * t, PCX + 6 + 12 * t, 42 + 2 + 3 * t], fill=(*INK, 255))
            f.alpha_composite(n)
        elif i < REVEAL + 2:                               # the flash: a lit teal rim, hold 2 frames
            F.thick_arc(f, PCX, PCY, PR, 0, 360, [(-1, VEIN_LIT), (0, WHITE), (1, VEIN_LIT), (2, PAL["III"]["vein"]),
                                                   (3, (20, 20, 30))])
        if i >= REVEAL:                                    # the burst: thorns out, then they fall
            u = ease((i - REVEAL) / 5)
            g = max(0, i - REVEAL - 8)
            for k, a in enumerate(dirs):
                if i > 24 and (k + i) % 2:
                    continue
                r0 = PR + 1 + u * (5 + 3 * (k % 2))
                x0, y0 = at(r0, a)
                y0 += 0.12 * g * g
                L = (7 + 3 * (k % 3)) * (1 if g == 0 else max(0.4, 1 - g / 14))
                thorn(f, x0, y0, a, L, 2.5, i < REVEAL + 6 and k % 2 == 0)
            if REVEAL + 1 <= i < 25:                       # bone tendrils whip out and curl back
                u2 = (i - REVEAL - 1) / (24 - REVEAL)
                L = 14 * math.sin(math.pi * min(1, u2 * 1.3))
                for k, a in enumerate((200, 340, 120, 60, 160)):
                    x0, y0 = at(PR + 1, a)
                    tendril(f, x0, y0, a, max(2, L + 2 * (k % 2)), 0.9 if k % 2 else -0.9, BONE if k < 3 else BONE_S,
                            ph=i * 0.5 + k)
            if i >= 18:                                    # teal motes drift up where the shards were
                for k in range(6):
                    x, y = at(PR + 6 + k % 3, k * 60 + 30)
                    F.px(f, x, y - (i - 18) * 1.2, VEIN_LIT)
        fr.append(f)
    return disc_clear(fr, flash=(REVEAL,))


# ------------------------------------------------------------------------------------------------ the ring pieces (ground)
PIECE_LEN = 20


def piece(which):
    """One hex of the visual ring around her hex: lands on its frame 0, 20 frames."""
    fr = []
    cx, base = 25, 34
    for i in range(PIECE_LEN):
        f = F.frame()
        u = ease(i / 4)
        late = max(0, i - 10) / 9
        if which == "sayo1":                               # a Heartglass pane springs up and breaks into prism light
            if i < 12:
                h = 4 + 16 * u
                A.shard(f, cx, base, h, 9, 0.0, "I", hot=i < 2)
                if i in (3, 4, 5):
                    star(f, cx, base - h - 1, WHITE, 2)
            else:
                for k in range(8):
                    a = math.radians(k * 45 + 20)
                    r = 3 + (i - 12) * 2
                    F.blob(f, cx + r * math.cos(a), base - 10 + r * math.sin(a) + late * 4, PRISM[k % 4] if k % 2 else PAL["I"]["lite"], r=1)
        elif which == "silence":                           # the ink pools, a shadow tendril stands up, sinks to smoke
            pool = min(1, i / 3) * (1 if i < 15 else max(0, 1 - (i - 15) / 4))
            if pool:
                n = F.frame()
                ImageDraw.Draw(n).ellipse([cx - 9 * pool, base - 3 * pool, cx + 9 * pool, base + 3 * pool], fill=(*INK, 255))
                F.outline_alpha(n, PAL["III"]["frame"])
                f.alpha_composite(n)
            if 1 <= i < 15:
                H = 22 * ease((i - 1) / 5) * (1 if i < 11 else max(0.2, 1 - (i - 11) / 4))
                for s in range(int(H)):
                    x = cx + 2.5 * math.sin(s * 0.35 + i * 0.5) * (s / max(1, H))
                    F.blob(f, x, base - s, INK, r=2 if s < H * 0.7 else 1)
                    if s % 5 == 2:
                        F.px(f, x, base - s, PAL["III"]["vein"])
                if H > 6:
                    tx = cx + 2.5 * math.sin(H * 0.35 + i * 0.5)
                    tendril(f, tx, base - H, -90, 6, 0.8, BONE, ph=i)
            if i >= 11:
                for k in range(4):
                    F.blob(f, cx - 6 + k * 4, base - 6 - (i - 11) * 2 - k % 2 * 3, PAL["III"]["smoke"], r=1)
        elif which == "sayo2":                             # the etch lattice ignites, then black cracks cross it
            heat = F.ETCH_HOT if i < 4 else (F.ETCH_MID if i < 10 else F.ETCH_DIM)
            L = min(1, i / 3) * 12
            for a in (0, 60, 120):
                for sgn in (1, -1):
                    x1 = cx + sgn * L * math.cos(math.radians(a))
                    y1 = base - 6 + sgn * L * math.sin(math.radians(a)) * 0.6
                    F.seg(f, (cx, base - 5), (x1, y1 + 1), SCORE)
                    if i < 16 or (i + a) % 2:
                        F.seg(f, (cx, base - 6), (x1, y1), heat)
            if i < 3:
                star(f, cx, base - 6, WHITE, 3)
            if i >= 5:
                c = ease((i - 5) / 6)
                x, y = cx - 10, base - 9
                for s in range(int(20 * c)):
                    x, y = x + 1, y + 0.6 * math.sin(s * 1.4)
                    F.blob(f, x, y, PAL["II"]["vein"], r=1)
                if i >= 12:
                    F.blob(f, cx + 2, base - 10 - (i - 12), PAL["II"]["smoke"], r=2)
        else:                                              # saint: a black thorn bursts up, bone wisp, shards fall
            if i < 13:
                h = 4 + 18 * u
                thorn(f, cx, base, -90, h, 4, i < 6)
                if 2 <= i < 12:
                    tendril(f, cx + 3, base - h * 0.6, -40, 4 + i * 0.6, 0.9, BONE, ph=i)
            else:
                for k in range(6):
                    x = cx - 7 + k * 3
                    y = base - 16 + (i - 13) ** 2 * 0.35 + k % 2 * 3
                    thorn(f, x, y, 90 + (k - 2.5) * 12, 3, 1.2, False)
            if i < 3:
                F.thick_arc(f, cx, base, 6 + i * 2, 0, 360, [(0, VEIN_LIT)], 0.4)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ set pieces for the frequent moves
# Director (2026-11-05, live test): "I didn't see any of the cool set pieces we talked about in Act I. Can we make the
# ones she fires off frequently like that since players see them the most." Each is a per-hex piece; the generator
# lays one visual COORDINATES tag per band over the cast's own tiles, band k leading by k * SET_LEAD frames, and blanks
# the effect's own appear (so overdraw drops from 2-3x to 1x per hex).
SET_LEAD = 2        # 100 ms per band: six bands sweep a 12-hex line in 0.5 s
SET_BANDS = 6


def beam_piece():
    """Act I mark arrival: a beam of Heartglass light runs through the hex (white core, cyan sides, prism fringe, a
    mirror glint), then the Act I heavy mark lands."""
    p = PAL["I"]
    out = []
    for i in range(3):
        f = F.frame()
        y = 25
        half = (0.5 + 0.5 * i) * 25
        for dx in range(-int(half), int(half) + 1):
            x = 25 + dx
            F.px(f, x, y - 2, PRISM[(dx + i) % 4])
            F.px(f, x, y - 1, p["lite"])
            F.px(f, x, y, WHITE)
            F.px(f, x, y + 1, p["lite"])
            F.px(f, x, y + 2, PRISM[(dx + i + 2) % 4], keep=0.6)
        if i == 1:
            star(f, 25, 25, WHITE, 4)
        out.append(f)
    tail = A.appear_heavy("I")
    for j, g in enumerate(tail):
        if j < 2:
            g = g.copy()
            F.seg(g, (0, 25), (49, 25), p["lite"], keep=0.5 if j == 0 else 0.25)
        out.append(g)
    return out


def stillness_piece():
    """The Silence's lock: an ink ring closes in on the hex with teal veins and bone barbs, then snaps shut."""
    out = []
    for i in range(12):
        f = F.frame()
        if i < 7:
            r = 21 - i * 2.6
            F.ground_ring(f, r, r * 0.55, [(0, INK), (1, INK), (2, PAL["III"]["vein"] if i % 2 else INK)])
            for k in range(6):
                a = math.radians(k * 60 + i * 8)
                x, y = 25 + r * math.cos(a), 25 + r * 0.55 * math.sin(a)
                F.seg(f, (x, y), (x - 3 * math.cos(a), y - 1.6 * math.sin(a)), BONE)
        elif i < 9:
            F.ground_ring(f, 3, 2, [(0, VEIN_LIT), (1, WHITE), (2, PAL["III"]["vein"]), (3, INK)])
        else:
            for k in range(6):
                a = math.radians(k * 60 + 30)
                rr = 4 + (i - 9) * 3
                F.blob(f, 25 + rr * math.cos(a), 25 + rr * 0.55 * math.sin(a), PAL["III"]["smoke"] if k % 2 else INK, r=1)
        out.append(f)
    return out


def close_in_appear():
    """The Silence Turns (heavy, the Remainder): ink tendrils reach in from the hex's six corners and close on the
    centre, then the Act III heavy mark lands. Works as the mark's arrival now and ahead of an eruption later."""
    out = []
    for i in range(5):
        f = F.frame()
        t = (i + 1) / 5
        for k in range(6):
            a = math.radians(k * 60)
            x0, y0 = 25 + 22 * math.cos(a), 25 + 12 * math.sin(a)
            x1, y1 = x0 + (25 - x0) * t * 0.85, y0 + (25 - y0) * t * 0.85
            F.seg(f, (x0, y0), (x1, y1), INK)
            F.seg(f, (x0, y0 + 1), (x1, y1 + 1), INK)
            F.px(f, x1, y1, PAL["III"]["vein"] if i < 4 else VEIN_LIT)
        out.append(f)
    return out + A.appear_heavy("III")


def close_in_core():
    """The Silence Turns' centre (TARGET origin): a ring of dark the size of the clip closes on the target's hex with
    bone wisps, then bursts black with lit teal veins."""
    out = []
    for i in range(14):
        f = F.frame()
        if i < 8:
            r = 24 - i * 2.6
            F.ground_ring(f, r, r * 0.6, [(0, INK), (1, INK), (2, INK), (3, PAL["III"]["vein"])])
            for k in range(8):
                a = k * 45 + i * 6
                x, y = 25 + r * math.cos(math.radians(a)), 25 + r * 0.6 * math.sin(math.radians(a))
                tendril(f, x, y, a + 180, 4, 0.6, BONE if k % 2 else BONE_S, ph=i + k)
        elif i < 10:
            F.ground_ring(f, 5, 3, [(0, WHITE), (1, VEIN_LIT), (2, INK), (3, INK)])
        else:
            u = (i - 10) / 3
            for k in range(8):
                a = math.radians(k * 45 + 22)
                rr = 4 + u * 12
                thorn(f, 25 + rr * math.cos(a), 25 + rr * 0.6 * math.sin(a) - u * 4, -90 + (k - 3.5) * 14, 5 - 2 * u, 1.5,
                      k % 2 == 0)
        out.append(f)
    return out


def pool_dark_appear():
    """A dark pool (the Silence, Act III) arrives: ink wells up from a crack at the centre and spreads, teal veins
    running out through it."""
    out = []
    for i in range(9):
        f = F.frame()
        t = ease((i + 1) / 7)
        n = F.frame()
        ImageDraw.Draw(n).ellipse([25 - 17 * t, 25 - 8 * t, 25 + 17 * t, 25 + 8 * t], fill=(*INK, 255))
        for k in range(6):
            a = math.radians(k * 60 + 15)
            F.seg(n, (25, 25), (25 + 15 * t * math.cos(a), 25 + 7 * t * math.sin(a)),
                  VEIN_LIT if i in (3, 4) else PAL["III"]["vein"])
        F.outline_alpha(n, PAL["III"]["frame"])
        f.alpha_composite(n)
        if i < 4:
            F.blob(f, 25, 25 - 2 - i * 2, PAL["III"]["smoke"], r=2)
        out.append(f)
    return out


def setpieces():
    beam, brk = beam_piece(), A.burst("I")
    etch, recast = F.build_etch_appear(), A.recast_a3()
    still = stillness_piece()
    out = []
    for k in range(SET_BANDS):
        out.append((f"anim_moe_beam_w{k}_a4.webp", A.delayed(beam, k * SET_LEAD), f"Act I mark: light runs in, band {k}"))
        out.append((f"anim_moe_break_w{k}_a4.webp", A.delayed(brk, k * SET_LEAD), f"Refraction Breaks wave, band {k}"))
        out.append((f"anim_moe_etch_w{k}_a4.webp", A.delayed(etch, k * SET_LEAD), f"Etching scored in sequence, band {k}"))
        out.append((f"anim_moe_recast_w{k}_a4.webp", A.delayed(recast, k * SET_LEAD), f"Recast region breaks, band {k}"))
    for k in range(4):
        out.append((f"anim_moe_still_w{k}_a4.webp", A.delayed(still, k * SET_LEAD), f"Stillness closes in, band {k}"))
    out.append(("anim_moe_close_in_a4.webp", close_in_appear(), "The Silence Turns: dark closes in on each hex"))
    out.append(("anim_moe_close_in_core_a4.webp", A.delayed(close_in_core(), 3), "The Silence Turns: the target's hex"))
    out.append(("anim_moe_pool_dark_appear_a4.webp", pool_dark_appear(), "Dark pool spreads (the Silence, Act III)"))
    return out


def assets():
    out = []
    for which, fn, note in (("sayo1", flourish_sayo1, "Heartglass light gathers, the fan opens, prismatic burst"),
                            ("silence", flourish_silence, "the ink spreads and her shadow stands up off the floor"),
                            ("sayo2", flourish_sayo2, "the gold etch ring ignites, black cracks creep in"),
                            ("saint", flourish_saint, "black glass bursts as thorns with lit teal veins and bone tendrils")):
        out.append((f"anim_moe_entrance_{which}_a4.webp", fn(), f"Entrance ({which}): {note}"))
        p = piece(which)
        for k in range(2):
            out.append((f"anim_moe_entrance_ring_{which}_w{k}_a4.webp", A.delayed(p, REVEAL + k * WAVE),
                        f"Entrance ring ({which}) band {k} (lead {REVEAL + k * WAVE})"))
    return out


def export(out_dir=None, drafts=False):
    """The entrances go to exports/ (moe_fx_a4.json). --drafts writes the frequent-move set pieces to --out instead:
    they wait for docs/design/SAYO_BIBLE.md (coordinator, 2026-11-05) before they are finalised and wired."""
    rows = []
    for name, frames, note in (setpieces() if drafts else assets()):
        assert len(frames) <= 80, (name, len(frames))
        p = os.path.join(out_dir or F.EXPORTS, name)
        F.strip(frames).save(p, lossless=True, quality=100, method=6)
        size = os.path.getsize(p)
        assert size < F.MAX_BYTES, (name, size)
        rows.append({"file": f"art/mother_of_echoes_fx/exports/{name}", "type": "ANIMATION", "frames": len(frames),
                     "speed": F.MS, "bytes": size, "note": note})
    if drafts:
        print(f"{len(rows)} draft set pieces -> {out_dir}")
        return
    with open(os.path.join(F.EXPORTS, "moe_fx_a4.json"), "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/build_fx_a4.py", "assets": rows}, fh, indent=1)
        fh.write("\n")
    print(f"{len(rows)} FX")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts", action="store_true", help="write the draft set pieces (not the entrances)")
    ap.add_argument("--out", help="output folder for --drafts")
    a = ap.parse_args()
    if a.drafts and not a.out:
        raise SystemExit("--drafts needs --out (drafts never land in exports/)")
    export(a.out, a.drafts)
