#!/usr/bin/env python3
"""Subaku Palace: the centre payoff on the caster's hex (player EVENT jutsu jELEiw5W3N4m2R3oJm3Pk).

    python3 art/subaku_palace/gates/build_gates.py [--out DIR] [--sheet PNG]

SHIPPING BUILD. Target geometry (art/subaku_palace/TIMING.md v5, director 2026-11-05): effect clips 2.5 hex heights
square (the ratio-1 change 338126cb is to be reverted upstream), players drawn as LPC character avatars. The ratio-1
note build is build_gates_ratio1.py.

One asset, the appear on the SELF tag (increasedamagegiven): anim_sbk_gates_rise_v6, 44 frames x 50 ms. No static
loop, no dais (director: the sigil is symbolic and fades within the cast).

- 0-5    the sigil burns into the ground round the caster's feet: a spark, two arcs sweeping round to close a
         bevelled ring 30 x 8 px (0-0.4 h above the hex bottom), then ember cracks and a swell.
- 6      its bands flash white-hot to the hex's edge midpoints and run past them: the energy leaves the hex.
- 7-9    ring 1 ignites: two red sandstone oni gates tear up in three heaves (25 %, 60 %, 100 %), 2 px sandstone
         shards knocked off each top and falling; the ring draws in to 18 x 8 px to stay whole between them. Flared roofs with upturned eaves, a horn-crested lintel, a two-tone snarling face
         (10 x 11) with burning eyes.
- 14-20  as the bloom spreads, the palace rises behind them: two three-tier pagoda towers and roof wings.
- 21-23  the sigil cools to demon gold; out from 24.
- 22-26  the solid demon-gold moon-gate arch traces up round the caster as the bloom reaches the rim.
- 29-30  the held beat on the floor's final pulse. Ridges, arch, eyes white-hot on 29 only; nothing moves.
- 31-41  the palace sinks (31-36); the gates sink into the floor (33-41).
- 42-43  empty: nothing lingers.

Frame geometry (50 px frame = 2.5 h, so h = 20 px): hex box x 5-45, y 15-35, centre (25, 25), edge midpoints
(10,20) (25,15) (40,20) (40,30) (25,35) (10,30). The LPC caster (combatActors.ts 604-618 at cb755375): 1.35 h frame
centred 0.825 h above the hex bottom; a typical body, mapped by LPC rows, spans x 20-29 (head) / 18-31 (arms), y 5
(headgear) to 31 (feet at y 30.3). Keep-clear zones, gated at 0 % on every frame:
- ENVELOPE  the caster's body: nothing is drawn over it (the sigil and palace pass behind it).
- METERS    the lower neighbour's HP/SP/CP rows, which fall inside this clip at 0.2-0.6 h above this hex's bottom
            (x 15-34, y 23-31), for everything but the sigil. The sigil ring (QA r3) is masked only by ENVELOPE;
            its cover of these rows is reported in the JSON.
The caster's own meters (x 15-34, y 3-11) are reported, not gated: the moon-gate arch's top crosses them on ticks
24-33 (director, 2026-11-05: keep the arch). They are ALWAYS visible to the casting player: combat.ts:420 passes the
viewer's own userId as selectedId, and combatActors.ts:516-520 shows a fighter's meters when it is selected or
hovered. Other viewers see them only on hover or selection.

Mirror-symmetric about x -> 49 - x (the clip centre lies between pixels 24 and 25). Drawn on the 50 px grid, hard
alpha, 1 px outlines, RGB filled under transparent pixels, exported x3 nearest. Build checks: 2 px edge margin, TIMING.md
palette, white-hot on ticks 6 and 29 only, the two keep-clear zones, the last two frames empty. Pillow only.
"""
import argparse
import json
import math
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORTS = os.path.join(HERE, "exports")
N = 50
SCALE = 3
MS = 50
MAX_BYTES = 460800
SAFE_EDGE = 2
VER = "v6"

# ------------------------------------------------------------------------------------------------ timing (TIMING.md v5)
RING1 = 7               # ring 1 ignites; the gates heave up 7-9
SEAL_PEAK = 29          # the floor's final pulse peaks (white-hot channels)
LEN = 44
SPOKES = RING1 - 1
SIG_COOL_AT = 21        # the sigil cools 21-23 and is out from 24 (QA; director: it fades within the cast)
PALACE_AT = 14          # the palace rises 14-20 as the bloom spreads
PALACE_RISE = 7
ARCH_AT = 22            # the moon-gate arch traces up 22-26, as the bloom reaches the rim
HOLD = (SEAL_PEAK, SEAL_PEAK + 1)     # 29-30
SETTLE = SEAL_PEAK + 2  # 31
PALACE_SINK = 6         # 31-36
GATE_SINK_AT = 33
GATE_SINK = 9           # 33-41; 42-43 empty

# ------------------------------------------------------------------------------------------------ palette (TIMING.md v5)
SHADOW = (22, 10, 9)
SS_D, SS_M, SS, SS_L, SS_HI = (90, 30, 20), (122, 42, 28), (168, 67, 42), (201, 101, 61), (227, 144, 106)
G_DEEP, G_MID, G_BRI = (138, 90, 18), (196, 138, 28), (232, 180, 58)
B1, B2, WHITE = (255, 207, 74), (255, 229, 138), (255, 244, 200)
E0, E1, E2, E3 = (110, 12, 8), (184, 28, 16), (255, 74, 28), (255, 150, 60)
ST, ST_L = (44, 40, 40), (60, 54, 53)                     # basalt (TIMING.md v5: #2c2828, #3c3635)
PALETTE = {SHADOW, SS_D, SS_M, SS, SS_L, SS_HI, G_DEEP, G_MID, G_BRI, B1, B2, WHITE, E0, E1, E2, E3, ST, ST_L}

CX, CY = 24.5, 25.0
EDGE_MID = [(10, 20), (25, 15), (40, 20), (40, 30), (25, 35), (10, 30)]


def mirror_x(x):
    return 49 - x


# ------------------------------------------------------------------------------------------------ keep-clear zones
def envelope_mask():
    m = Image.new("L", (N, N), 0)
    d = ImageDraw.Draw(m)
    d.rectangle([22, 5, 27, 7], fill=255)        # crown / headgear
    d.rectangle([20, 8, 29, 17], fill=255)       # head
    d.rectangle([18, 17, 31, 27], fill=255)      # shoulders, arms, torso
    d.rectangle([20, 27, 29, 31], fill=255)      # legs to the feet
    return m


def lower_meters_mask():
    m = Image.new("L", (N, N), 0)
    ImageDraw.Draw(m).rectangle([15, 23, 34, 31], fill=255)
    return m


def own_meters_mask():
    m = Image.new("L", (N, N), 0)
    ImageDraw.Draw(m).rectangle([15, 3, 34, 11], fill=255)
    return m


ENV = envelope_mask()
METERS = lower_meters_mask()
KEEP = Image.new("L", (N, N), 0)
KEEP.paste(255, (0, 0), ENV)
KEEP.paste(255, (0, 0), METERS)


# ------------------------------------------------------------------------------------------------ primitives
def frame():
    return Image.new("RGBA", (N, N), (0, 0, 0, 0))


def px(f, x, y, col):
    x, y = int(round(x)), int(round(y))
    if 0 <= x < f.width and 0 <= y < f.height:
        f.putpixel((x, y), (*col, 255))


def clamp01(t):
    return max(0.0, min(1.0, t))


def ease_out(t):
    return 1 - (1 - clamp01(t)) ** 3


def ease_in(t):
    return clamp01(t) ** 2


def ease_back(t, s=1.7):
    t = clamp01(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def outline_alpha(f, rgb=SHADOW):
    a = f.getchannel("A").load()
    pts = [(x, y) for y in range(N) for x in range(N)
           if not a[x, y] and any(0 <= x + dx < N and 0 <= y + dy < N and a[x + dx, y + dy]
                                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in pts:
        f.putpixel((x, y), (*rgb, 255))
    return f


def clip_below(f, y0):
    a = f.getchannel("A")
    ImageDraw.Draw(a).rectangle([0, y0, N, N], fill=0)
    f.putalpha(a)
    return f


def clear_mask(f, m):
    a = f.getchannel("A")
    a.paste(0, (0, 0), m)
    f.putalpha(a)
    return f


def mirrored(f):
    """f plus its mirror about the clip centre."""
    g = f.copy()
    g.alpha_composite(f.transpose(Image.FLIP_LEFT_RIGHT))
    return g


def shifted(f, dy):
    if not dy:
        return f
    g = frame()
    g.alpha_composite(f, (0, dy))
    return g


def pixels(f):
    return f.get_flattened_data() if hasattr(f, "get_flattened_data") else f.getdata()


def fill_under(img):
    p = img.load()
    seen = [[p[x, y][3] > 0 for x in range(N)] for y in range(N)]
    frontier = [(x, y) for y in range(N) for x in range(N) if seen[y][x]]
    while frontier:
        nxt = []
        for x, y in frontier:
            r, g, b, _ = p[x, y]
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < N and 0 <= ny < N and not seen[ny][nx]:
                    seen[ny][nx] = True
                    p[nx, ny] = (r, g, b, 0)
                    nxt.append((nx, ny))
        frontier = nxt
    return img


def strip(frames):
    s = Image.new("RGBA", (N, N * len(frames)))
    for i, f in enumerate(frames):
        g = f.copy()
        a = g.getchannel("A")
        ImageDraw.Draw(a).rectangle([0, 0, N - 1, N - 1], outline=0)
        g.putalpha(a)
        s.paste(fill_under(g) if a.getbbox() else g, (0, i * N))
    return s.resize((N * SCALE, N * len(frames) * SCALE), Image.NEAREST)


# ------------------------------------------------------------------------------------------------ checks
def coverage(frames, mask):
    m = mask.load()
    cells = [(x, y) for y in range(N) for x in range(N) if m[x, y]]
    return [round(sum(1 for x, y in cells if f.getpixel((x, y))[3]) / len(cells), 3) for f in frames]


def check(frames):
    for i, f in enumerate(frames):
        bb = f.getchannel("A").getbbox()
        if bb and (bb[0] < SAFE_EDGE or bb[1] < SAFE_EDGE or bb[2] > N - SAFE_EDGE or bb[3] > N - SAFE_EDGE):
            raise SystemExit(f"frame {i} reaches within {SAFE_EDGE} px of the clip edge {bb}")
        for p in pixels(f):
            if p[3] and p[3] != 255:
                raise SystemExit(f"frame {i} has soft alpha {p[3]}")
            if p[3] and p[:3] not in PALETTE:
                raise SystemExit(f"frame {i} colour {p[:3]} is not in the TIMING.md palette")
    hot = [i for i, f in enumerate(frames) if any(p[3] and p[:3] == WHITE for p in pixels(f))]
    if set(hot) - {SPOKES, HOLD[0]}:
        raise SystemExit(f"white-hot on frames {hot}, allowed only {SPOKES} and {HOLD[0]}")
    if any(f.getchannel("A").getbbox() for f in frames[-2:]):
        raise SystemExit("the last two frames must be empty")
    c = coverage(frames, ENV)
    if max(c) > 0:
        raise SystemExit(f"the caster's LPC envelope is {max(c):.1%} covered on frame {c.index(max(c))}")
    c = coverage(rise(with_sigil=False), METERS)                # gates, palace, chips: never on the lower meters
    if max(c) > 0:
        raise SystemExit(f"the lower neighbour's meters are {max(c):.1%} covered on frame {c.index(max(c))}")


# ------------------------------------------------------------------------------------------------ the sigil
# A ring burned into the ground round the caster's feet, 30 x 8 px (x 10-39, y 27-35; 0-0.4 h above the hex bottom),
# drawn in to 18 x 8 (x 16-33) by the gates' heaves so it stays whole between them.
# Only the stretch of its back arc behind the legs is hidden (the LPC envelope). Once the gates stand, their slabs
# cover the ring's two ends, so it reads as a ring between them. QA 2026-11-06 (r3): the sigil may pass under the
# lower neighbour's meter rows; everything else stays gated off them (reported in the JSON).
SIG_C = (CX, 31.0)
SIG_RX, SIG_RY = 15.0, 4.0
SIG_RX_TIGHT = 9.0                   # from tick 9 the ring has drawn in between the standing gates (x 16-33)


def sig_rx(i):
    """30 px wide while it builds (0-7), drawn in by the gates' heaves (8: 12 px half-width, 9 on: 9)."""
    return SIG_RX if i <= RING1 else (12.0 if i == RING1 + 1 else SIG_RX_TIGHT)


_RX = [SIG_RX]                       # the half-width for the frame being drawn (set in sigil())
SIG_OUT = SIG_COOL_AT + 3            # gone from tick 24: the sigil fades within the cast
SPOKE_EDGES = [(10, 30), (40, 30), (25, 35), (10, 20), (40, 20)]   # the top midpoint lies behind the head


def ell(r, deg):
    a = math.radians(deg)
    return SIG_C[0] + _RX[0] * r * math.cos(a), SIG_C[1] + SIG_RY * r * math.sin(a)


def sigil_cols(i):
    """(lit edge, body) for tick i, or None once it is out."""
    if i == SPOKES:
        return WHITE, B1
    if i < SIG_COOL_AT:
        return (B2, G_BRI) if i >= 3 else (B1, G_MID)
    k = i - SIG_COOL_AT                                 # 21, 22, 23: burning gold cools to demon gold; out at 24
    return ((G_BRI, G_MID), (G_MID, G_DEEP), (G_DEEP, G_DEEP))[k] if k < 3 else None


def spoke_pts(edge, start, end, n=10):
    ex, ey = edge
    sx, sy = ell(1.0, math.degrees(math.atan2((ey - SIG_C[1]) / SIG_RY, (ex - SIG_C[0]) / _RX[0])))
    return [(sx + (ex - sx) * (start + (end - start) * s / n), sy + (ey - sy) * (start + (end - start) * s / n))
            for s in range(n + 1)]


def sigil(i):
    """0: a spark in front of the feet. 1-4: two burning arcs sweep round from the front and meet behind the caster,
    doubling to a bevelled band. 5: the inner ring and the ember cracks light, the band swells. 6: the bands flash
    white-hot out to the hex's edge midpoints and past them. Then a steady ring with pulses running out along the
    bands, white-hot on the seal peak, cooling 22-24, out at 25."""
    f = frame()
    _RX[0] = sig_rx(i)
    cols = sigil_cols(i)
    if cols is None:
        return f
    top, body = cols
    if i == 0:
        for dx, c in ((0, B2), (-1, B2), (1, B1), (-2, B1), (2, G_MID)):
            px(f, SIG_C[0] + dx, SIG_C[1] + SIG_RY, c)
        return clear_mask(f, ENV)
    sweep = 180 * clamp01(i / 4)                        # degrees each way from the front (90 deg = front centre)
    for d in range(0, 361, 2):
        off = min(abs(d - 90), 360 - abs(d - 90))
        if off > sweep:
            continue
        x, y = ell(1.0, d)
        px(f, x, y - 0.5, top)
        px(f, x, y + 0.5, body)
        if i >= 4:                                      # the band thickens outward as it closes
            ox, oy = math.cos(math.radians(d)), math.sin(math.radians(d))
            px(f, x + (1 if ox > 0.5 else -1 if ox < -0.5 else 0), y + (1 if oy > 0.5 else 0), body)
    if i in (1, 2, 3):                                  # the arcs' heads
        for d in (90 - sweep, 90 + sweep):
            x, y = ell(1.0, d)
            px(f, x, y, B2)
    if i >= 5:                                          # ember cracks in the band's front
        for d in (35, 145, 70, 110):
            x, y = ell(1.0, d)
            px(f, x, y + 0.5, E2 if i < SIG_COOL_AT else E1)
    if i == 5:                                          # the swell before the release
        for d in range(0, 360, 4):
            x, y = ell(1.06, d)
            px(f, x, y, B1)
    if i >= SPOKES:                                     # the bands out to the edge midpoints
        for e in SPOKE_EDGES:
            for x, y in spoke_pts(e, 0.0, 1.0):
                px(f, x, y, top if i <= SPOKES + 1 else body)
    if i in (SPOKES, SPOKES + 1):                       # and past them: the energy leaves the hex
        for e in SPOKE_EDGES:
            for x, y in spoke_pts(e, 1.0 if i == SPOKES else 1.25, 1.6, 8):
                if SAFE_EDGE <= x <= N - SAFE_EDGE - 1 and SAFE_EDGE <= y <= N - SAFE_EDGE - 1:
                    px(f, x, y, WHITE if i == SPOKES else B2)
    if SPOKES + 1 < i < SIG_COOL_AT:                    # pulses run out along the bands
        for e in SPOKE_EDGES:
            pts = spoke_pts(e, 0.0, 1.0)
            x, y = pts[((i - SPOKES) * 2) % len(pts)]
            px(f, x, y, B2)
    return clear_mask(f, ENV)


# ------------------------------------------------------------------------------------------------ the gates
# The LEFT gate, 13 x 28, drawn at x 3-15 (slab x 4-13); the right gate is its mirror. Lit from the top left.
# Y ridge (gold, white-hot on the hold)  K/G demon gold  o shadow  L/l face plate (two-tone light)  W eyes
# F fangs  T throat  d/s/m sandstone dark..mid  R/r ember studs
GATE_MAP = [
    "Y..K....K...Y",   # upturned eave tips and the crest's horn tips
    "Y...G..G....Y",   # the horns curl in to the lintel
    "YYYYYYYYYYYYY",   # roof ridge
    "ooooooooooooo",   # the flared roof
    ".ooooooooooo.",
    ".KGGGGGGGGK..",   # lintel
    ".LLLLLLLLLL..",   # the oni face: a light plate with dark carving
    ".LoLLLLLLoL..",   # brows, a hard V
    ".LLoLLLLoLL..",
    ".LLLooooLLL..",
    ".LWWoLLoWWL..",   # burning eyes
    ".lLWolloWLl..",
    ".lllloollll..",   # nostrils
    ".lFooooooFl..",   # maw, upper fangs
    ".loTTTTTTol..",   # ember throat
    ".lFooooooFl..",   # lower fangs
    ".dlllllllld..",   # jaw
    ".KGGGGGGGGK..",   # collar
    ".smmmRRmmms..",   # the carved door
    ".smGmrrmGms..",
    ".smmmRRmmms..",
    ".smmmrrmmms..",
    ".smGmRRmGms..",
    ".smmmrrmmms..",
    ".smmmRRmmms..",
    ".smGmrrmGms..",
    ".ssssssssss..",
    ".dddddddddd..",
]
GW, GH = 13, len(GATE_MAP)
GATE_X = 3
GATE_BASE = 45                      # the lip of torn stone


def gate_sprite(eyes, ridge, throat):
    g = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    col = {"Y": ridge, "K": G_MID, "G": G_BRI, "o": SHADOW, "L": SS_HI, "l": SS_L, "W": eyes, "F": G_BRI,
           "T": throat, "d": SS_D, "s": SS, "m": SS_M, "R": E1, "r": E0}
    for y, row in enumerate(GATE_MAP):
        for x, ch in enumerate(row):
            if ch != ".":
                g.putpixel((x, y), (*col[ch], 255))
    return g


def gate_colours(i):
    if i == HOLD[0]:
        return WHITE, WHITE, E3
    if i == HOLD[1] or RING1 <= i < RING1 + 2:
        return B2, B2, E3
    if i < SETTLE:
        return B2, G_BRI, E2
    return (B1, G_BRI, E2) if i < GATE_SINK_AT + 3 else (G_BRI, G_MID, E1)


RISE_STAGES = (0.25, 0.6, 1.0)      # ring 1: the gates tear free in three heaves, chips flying


def gate_up(i):
    if i < RING1:
        return 0.0
    if i >= GATE_SINK_AT:
        return 1 - ease_in((i - GATE_SINK_AT + 1) / GATE_SINK)
    t = i - RING1
    return RISE_STAGES[t] if t < len(RISE_STAGES) else 1.0


def gates_layer(i):
    up = gate_up(i)
    if up <= 0:
        return frame()
    eyes, ridge, throat = gate_colours(i)
    n = frame()
    n.alpha_composite(gate_sprite(eyes, ridge, throat), (GATE_X, GATE_BASE - GH + round((1 - up) * (GH + 2))))
    clip_below(n, GATE_BASE)
    outline_alpha(n)
    clip_below(n, GATE_BASE)
    return clear_mask(mirrored(n), KEEP)


def torn_ground(i):
    """A lip of broken basalt at each gate's foot while it stands (no ember dashes)."""
    f = frame()
    if gate_up(i) <= 0:
        return f
    for k, x in enumerate(range(GATE_X, GATE_X + 12)):
        px(f, x, GATE_BASE, ST_L if k % 3 else ST)
        px(f, x, GATE_BASE + 1, SHADOW)
    return mirrored(f)


def chips(i):
    """Sandstone shards (2 x 1 px, no outline) knocked off each gate's top as it heaves up (7, 8, 9): a short hop,
    then they fall past the gate's flank within 4 ticks."""
    f = frame()
    rnd = random.Random(3)
    for k in range(6):
        born = k % 3
        vx = rnd.uniform(-0.8, -0.2)                    # outward, drawn before any skip: each shard keeps its path
        vy = rnd.uniform(-1.6, -0.8)
        x0 = rnd.uniform(4, 9)
        tt = i - RING1 - born
        if not 0 <= tt < 5:
            continue
        top = GATE_BASE - GH * RISE_STAGES[born]
        x = x0 + vx * tt
        y = top - 2 + vy * tt + 1.4 * tt * tt
        now_top = GATE_BASE - GH * gate_up(i)
        if x < SAFE_EDGE or y < SAFE_EDGE or y > GATE_BASE - 1:
            continue
        if y >= now_top - 1 and x >= GATE_X + 1:        # in front of the gate's face: skip (it reads as a hole)
            continue
        c1, c2 = (SS_HI, SS_L) if k % 2 else (SS_L, SS)
        px(f, x, y, c1)
        px(f, x + 1, y, c2)
    return clear_mask(mirrored(f), KEEP)


# ------------------------------------------------------------------------------------------------ the palace
# the left tower over the gate's slab (x 4-13): (roof row y, roof x0, x1, body x0, x1), bottom tier first
TIERS = ((16, 4, 13, 6, 11), (11, 5, 12, 7, 10), (6, 6, 11, 8, 9))
WALL = (12, 13, 22)                 # left x, roof-wing ridge y, base y (the wall runs to its mirror)
ARCH_C = (CX, 19.0)
ARCH_RX, ARCH_RY = 10.5, 15.0       # apex y 4; the arch springs from the wall's base at y 22


def in_arch(x, y, grow=0.0):
    return ((x - ARCH_C[0]) / (ARCH_RX + grow)) ** 2 + ((y - ARCH_C[1]) / (ARCH_RY + grow)) ** 2 <= 1.0


def palace_left(ridge, tip, window):
    """The left half of the palace front (mirrored by the caller): a three-tier tower behind the gate, the wall
    with its eave out to the centre."""
    f = frame()
    d = ImageDraw.Draw(f)
    wl, ey, wb = WALL
    d.rectangle([wl, ey + 3, 25, wb], fill=(*SS_D, 255))               # the wall
    for y in range(ey + 6, wb, 4):
        d.line([wl + 1, y, 25, y], fill=(*SS_M, 255))                  # lacquer courses
    d.rectangle([wl - 2, ey, 25, ey + 2], fill=(*SHADOW, 255))         # the roof wing, running into the arch
    for k, (ry, r0, r1, b0, b1) in enumerate(TIERS):                  # the tower, bottom tier first
        nxt = TIERS[k - 1][0] - 1 if k else 21
        d.rectangle([b0, ry + 2, b1, nxt], fill=(*SS_D, 255))
        d.line([b0, ry + 2, b0, nxt], fill=(*SS_M, 255))
        d.rectangle([r0, ry, r1, ry + 1], fill=(*SHADOW, 255))
    # the door of the moon gate
    m = Image.new("L", (N, N), 0)
    mp = m.load()
    for y in range(N):
        for x in range(N):
            if in_arch(x, y) and y <= WALL[2]:
                mp[x, y] = 255
    f = clear_mask(f, m)
    outline_alpha(f)
    f = clear_mask(f, m)
    d = ImageDraw.Draw(f)
    for k, (ry, r0, r1, b0, b1) in enumerate(TIERS):                  # gold ridges, upturned tips, windows
        d.line([r0 + 1, ry, r1 - 1, ry], fill=(*ridge, 255))
        d.point([(r0, ry - 1), (r1, ry - 1)], fill=(*tip, 255))
        d.point([(8, ry + 3), (9, ry + 3)], fill=(*window, 255))
    d.point([(8, TIERS[-1][0] - 2), (9, TIERS[-1][0] - 2), (8, TIERS[-1][0] - 3)], fill=(*tip, 255))   # finial
    d.line([wl - 1, WALL[1], 25, WALL[1]], fill=(*ridge, 255))         # the wing's ridge
    d.line([wl - 1, WALL[1] + 2, 25, WALL[1] + 2], fill=(*G_DEEP, 255))  # its gilded eave line
    d.point([(wl - 2, WALL[1] - 1), (wl - 3, WALL[1] - 2)], fill=(*tip, 255))
    return clear_mask(f, m)


def arch_layer(progress, outer, inner):
    """The moon gate's arch: a solid two-tone demon-gold band (2 px), traced up from the wall's base to the apex."""
    f = frame()
    if progress <= 0:
        return f
    lim = WALL[2] - (WALL[2] - 3) * clamp01(progress)     # trace from the base (y 22) up to the apex
    for y in range(N):
        for x in range(N):
            if y > WALL[2] or y < lim:
                continue
            if in_arch(x, y, 1.6) and not in_arch(x, y, 0.0):
                px(f, x, y, outer)
            elif in_arch(x, y, 0.0) and not in_arch(x, y, -1.0):
                px(f, x, y, inner)
    return f


def palace_colours(i):
    if i == HOLD[0]:
        return WHITE, WHITE, E3, B2, WHITE
    if i == HOLD[1]:
        return B2, B2, E3, G_BRI, B2
    if i < SETTLE:
        return G_BRI, B1, E2, G_MID, B1
    return G_MID, G_BRI, E1, G_DEEP, G_MID


def palace_layer(i):
    if i < PALACE_AT:
        return frame()
    up = ease_out((i - PALACE_AT + 1) / PALACE_RISE)
    if i >= SETTLE:
        up = 1 - ease_in((i - SETTLE + 1) / PALACE_SINK)
    if up <= 0:
        return frame()
    ridge, tip, window, arch_out, arch_in = palace_colours(i)
    f = mirrored(palace_left(ridge, tip, window))
    f.alpha_composite(arch_layer(clamp01((i - ARCH_AT + 1) / 5) if i < SETTLE else 1.0, arch_out, arch_in))
    f = shifted(f, round((1 - up) * 24))
    clip_below(f, WALL[2] + 1)
    return clear_mask(f, KEEP)


# ------------------------------------------------------------------------------------------------ assets
def rise(with_sigil=True):
    fr = []
    for i in range(LEN):
        f = frame()
        if with_sigil:
            f.alpha_composite(sigil(i))
        f.alpha_composite(palace_layer(i))
        f.alpha_composite(torn_ground(i))
        f.alpha_composite(gates_layer(i))
        f.alpha_composite(chips(i))
        fr.append(clear_mask(f, ENV) if with_sigil else clear_mask(f, KEEP))
    return fr


def export(out_dir, sheet=None):
    os.makedirs(out_dir, exist_ok=True)
    r = rise()
    check(r)
    own = coverage(r, own_meters_mask())
    lower = coverage(r, METERS)                                 # the sigil alone (QA r3)
    name = f"anim_sbk_gates_rise_{VER}.webp"
    p = os.path.join(out_dir, name)
    strip(r).save(p, lossless=True, quality=100, method=6)
    size = os.path.getsize(p)
    assert size < MAX_BYTES, size
    row = {"file": f"art/subaku_palace/gates/exports/{name}", "type": "ANIMATION", "frames": len(r), "speed": MS,
           "bytes": size,
           "slot": "appearAnimation on the SELF increasedamagegiven effect; no staticAnimation, no staticAssetPath",
           "geometry": "clip 2.5 hex heights (EFFECT_ANIMATION_HEX_RATIO 2.5); caster an LPC character avatar",
           "lpc_envelope_cover_max": 0.0,
           "lower_neighbour_meters_cover_max_sigil_only": max(lower),
           "lower_neighbour_meters_cover_frames": [k for k, v in enumerate(lower) if v],
           "own_meters_cover_max": max(own), "own_meters_cover_frames": [k for k, v in enumerate(own) if v]}
    with open(os.path.join(out_dir, f"sbk_gates_{VER}.json"), "w") as fh:
        json.dump({"source": "art/subaku_palace/gates/build_gates.py", "timing": "art/subaku_palace/TIMING.md v5",
                   "ring1": RING1, "seal_peak": SEAL_PEAK, "assets": [row]}, fh, indent=1)
        fh.write("\n")
    print(row["file"], len(r), size, "own meters cover max", max(own), "lower meters (sigil) max", max(lower),
          [k for k, v in enumerate(lower) if v])
    if sheet:
        raw_sheet(r, sheet)


def raw_sheet(r, path):
    """Every frame x4 on mid-grey, the envelope (blue) and the lower neighbour's meters (red) outlined."""
    from PIL import ImageFilter
    Z, cols = 4, 10
    rows = (len(r) + cols - 1) // cols
    s = Image.new("RGBA", (cols * N * Z, rows * (N * Z + 12)), (70, 70, 78, 255))
    d = ImageDraw.Draw(s)
    edges = [(ENV.filter(ImageFilter.FIND_EDGES).load(), (90, 130, 170)),
             (METERS.filter(ImageFilter.FIND_EDGES).load(), (170, 80, 80))]
    for j, f in enumerate(r):
        x, y = (j % cols) * N * Z, (j // cols) * (N * Z + 12)
        d.text((x + 3, y), f"f{j}", fill=(240, 230, 200))
        y += 12
        for e, c in edges:
            for yy in range(N):
                for xx in range(N):
                    if e[xx, yy]:
                        d.rectangle([x + xx * Z, y + yy * Z, x + xx * Z + Z - 1, y + yy * Z + Z - 1], fill=c)
        s.alpha_composite(f.resize((N * Z, N * Z), Image.NEAREST), (x, y))
    s.convert("RGB").save(path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=EXPORTS)
    ap.add_argument("--sheet")
    a = ap.parse_args()
    export(a.out, a.sheet)
