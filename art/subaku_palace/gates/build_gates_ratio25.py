#!/usr/bin/env python3
"""Subaku Palace centre payoff: FALLBACK variant for the theninjarpg 3314d122 geometry (2.5 hex-height clip,
portrait marker + avatar disc). Build for main is build_gates.py (v3, 1 hex-height clip, LPC character avatars).
Director 2026-11-05: appear only (no static loop, no dais tile); the sigil fades within the cast. This script now
exports only anim_sbk_gates_rise_v2.webp (frames 36-37 are empty).

Original notes (v2) follow.

Subaku Palace: the centre payoff on the caster's hex (player EVENT jutsu jELEiw5W3N4m2R3oJm3Pk).

    python3 art/subaku_palace/gates/build_gates.py [--out DIR] [--sheet PNG]

The domain floor (art/subaku_palace/, separate owner) spreads ring by ring from the caster. The ground pattern
(AOE_SPIRAL_SHOOT, range 4) excludes the caster's own hex, so the centre rides the SELF tag (increasedamagegiven,
rounds 2). Timing and palette come from art/subaku_palace/TIMING.md (v1; ring 1 lands on tick 7, the seal pulse
peaks on tick 20). Three assets:

- anim_sbk_gates_rise_v2   appear, 38 frames x 50 ms. Ticks 0-5 the burning-gold sigil kindles at the caster's feet
                           and spirals out; tick 6 its spokes leave the hex (white-hot, one tick) along the six edge
                           midpoints where the domain's bands meet; ticks 7-12 two red sandstone gates with snarling
                           demon faces tear up out of the stone on ring 1, throwing chips; 13-19 the palace rises behind
                           the caster, two pagoda towers and a moon gate whose round door is cut round the caster's
                           pin, its gold arch tracing up to a horned crest; 20-21 the held beat on the seal pulse
                           (white-hot on 20 only, burning gold on 21, nothing moves); 22-37 the palace and the gates
                           sink back into the floor and the sigil cools to demon gold, ending on the dais's look.
- anim_sbk_master_loop_v2  static loop, 16 frames x 50 ms (0.8 s, peak on frame 0). Restrained: ember licks along the
                           caster's flanks, motes rising, a demon-gold glint at the hex's side vertices on the beat.
                           Nothing inside the pin box of this hex or the one below, nor the clan badge.
- tile_sbk_dais_v2         static art on the same SELF tag: the sigil burned into the basalt, outer and inner rings
                           and six bands to the edge midpoints, so the caster's hex is the hub the domain's bands
                           run out of rather than a bare hole (static art draws under the fighters).

Engine (docs/design/COMBAT_ANIMATION_ENGINE.md, theninjarpg@3314d122): clips are 2.5 hex heights square, fetched as
a 50 px rendition, sampled linearly, drawn over the fighters; the static loop draws over the appear from the same
clock; the four damage-modifier tags play their appear once (client only), but everything here is hard alpha, so
any extra copy of an identical frame changes nothing. Drawn on the 50 px grid (2-3 px clusters, 1 px outlines), RGB
filled under transparent pixels, exported x3 nearest (150 px frames). Build checks: nothing within 2 px of the frame
edge; every opaque pixel in the TIMING.md palette (plus the floor's basalt); white-hot on single ticks only; the
loop leaves the pin boxes clear. Pillow only.

Frame geometry (20 px per hex height): hex centred at (25, 25), vertices (5,25) (15,15) (35,15) (45,25) (35,35)
(15,35), edge midpoints (10,20) (25,15) (40,20) (40,30) (25,35) (10,30); the player's pin x 14-36, y 4-30 (avatar
disc centred (25, 15)); the hex below's pin from y 24 down; the clan badge x 37-45, y 3-11.
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
VER = "v2"

# ------------------------------------------------------------------------------------------------ timing (TIMING.md)
RING1 = 7               # band 1.0 lands
SEAL_PEAK = 20          # the seal pulse peaks on every band: the held beat lands here
LEN = 38                # the centre appear may run to 40 frames
SPOKES = RING1 - 1      # the sigil's spokes leave the caster's hex
GATE_RISE = 6           # 7-12
PALACE_AT = 13
PALACE_RISE = 6         # towers 13-18
ARCH_AT = 16            # the arch traces 16-19
HOLD = (SEAL_PEAK, SEAL_PEAK + 1)
SETTLE = SEAL_PEAK + 2  # 22
PALACE_SINK = 6         # 22-27
GATE_SINK_AT = 24
GATE_SINK = 9           # 24-32
SIGIL_COOL = 14         # 22-35
LOOP_LEN = 16

# ------------------------------------------------------------------------------------------------ palette (TIMING.md)
SHADOW = (22, 10, 9)                                                    # shadow / veil, outlines, roofs
SS_D, SS_M, SS, SS_L, SS_HI = (90, 30, 20), (122, 42, 28), (168, 67, 42), (201, 101, 61), (227, 144, 106)
G_DEEP, G_MID, G_BRI = (138, 90, 18), (196, 138, 28), (232, 180, 58)   # demon gold (at rest)
B1, B2, WHITE = (255, 207, 74), (255, 229, 138), (255, 244, 200)       # burning gold; WHITE = white-hot, one tick
E0, E1, E2, E3 = (110, 12, 8), (184, 28, 16), (255, 74, 28), (255, 150, 60)   # ember
ST_D, ST, ST_L = (31, 17, 17), (43, 28, 26), (54, 37, 33)               # basalt, sampled from the domain tile
PALETTE = {SHADOW, SS_D, SS_M, SS, SS_L, SS_HI, G_DEEP, G_MID, G_BRI, B1, B2, WHITE, E0, E1, E2, E3, ST_D, ST, ST_L}

CX, CY = 25, 25
PIN = (14, 4, 36, 30)
PIN_BELOW = (14, 24, 36, 49)
BADGE = (37, 3, 45, 11)
DISC = (25, 15)
DOOR_R = 10.5
EDGE_MID = [(10, 20), (25, 15), (40, 20), (40, 30), (25, 35), (10, 30)]
ERX, ERY = 16.0, 8.0     # the sigil's outer ring on the ground (the dais ring, r 20 in tile px, seen 2:1)


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
    """Ease out with an overshoot: the gate tears up past its rest height and settles back."""
    t = clamp01(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def outline_alpha(f, rgb=SHADOW):
    """1 px outline round every opaque cluster (4-neighbour), drawn outside it."""
    a = f.getchannel("A").load()
    w, h = f.size
    pts = [(x, y) for y in range(h) for x in range(w)
           if not a[x, y] and any(0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy]
                                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in pts:
        f.putpixel((x, y), (*rgb, 255))
    return f


def clip_below(f, y0):
    a = f.getchannel("A")
    ImageDraw.Draw(a).rectangle([0, y0, f.width, f.height], fill=0)
    f.putalpha(a)
    return f


def clear_mask(f, m):
    a = f.getchannel("A")
    a.paste(0, (0, 0), m)
    f.putalpha(a)
    return f


def box_mask(*boxes):
    m = Image.new("L", (N, N), 0)
    d = ImageDraw.Draw(m)
    for b in boxes:
        d.rectangle(b, fill=255)
    return m


def disc_mask(r):
    m = Image.new("L", (N, N), 0)
    x, y = DISC
    ImageDraw.Draw(m).ellipse([x - r, y - r, x + r, y + r], fill=255)
    return m


def door_mask():
    """The moon gate's door: the pin head and the doorway down to the ground, kept clear."""
    m = disc_mask(DOOR_R)
    x, y = DISC
    ImageDraw.Draw(m).rectangle([x - DOOR_R, y, x + DOOR_R, N], fill=255)
    return m


def fill_under(img):
    """RGB under every transparent pixel copied from the nearest drawn pixel (BFS), so linear filtering never pulls
    in a dark fringe. Alpha is untouched."""
    w, h = img.size
    p = img.load()
    seen = [[p[x, y][3] > 0 for x in range(w)] for y in range(h)]
    frontier = [(x, y) for y in range(h) for x in range(w) if seen[y][x]]
    while frontier:
        nxt = []
        for x, y in frontier:
            r, g, b, _ = p[x, y]
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx]:
                    seen[ny][nx] = True
                    p[nx, ny] = (r, g, b, 0)
                    nxt.append((nx, ny))
        frontier = nxt
    return img


def strip(frames):
    out = []
    for f in frames:
        g = f.copy()
        a = g.getchannel("A")
        ImageDraw.Draw(a).rectangle([0, 0, N - 1, N - 1], outline=0)    # 1 px clear margin (frame-edge bleed)
        g.putalpha(a)
        out.append(fill_under(g))
    s = Image.new("RGBA", (N, N * len(out)))
    for i, f in enumerate(out):
        s.paste(f, (0, i * N))
    return s.resize((N * SCALE, N * len(out) * SCALE), Image.NEAREST)


# ------------------------------------------------------------------------------------------------ checks
def edge_check(name, frames):
    for i, f in enumerate(frames):
        bb = f.getchannel("A").getbbox()
        if bb and (bb[0] < SAFE_EDGE or bb[1] < SAFE_EDGE or bb[2] > N - SAFE_EDGE or bb[3] > N - SAFE_EDGE):
            raise SystemExit(f"{name}: frame {i} reaches within {SAFE_EDGE} px of the clip edge {bb} (it would clip)")
    return frames


def palette_check(name, frames):
    for i, f in enumerate(frames):
        for p in (f.get_flattened_data() if hasattr(f, 'get_flattened_data') else f.getdata()):
            if p[3] and p[3] != 255:
                raise SystemExit(f"{name}: frame {i} has soft alpha {p[3]} (hard alpha only)")
            if p[3] and p[:3] not in PALETTE:
                raise SystemExit(f"{name}: frame {i} colour {p[:3]} is not in the TIMING.md palette")
    return frames


def white_check(name, frames, allowed):
    hot = [i for i, f in enumerate(frames) if any(p[3] and p[:3] == WHITE for p in (f.get_flattened_data() if hasattr(f, 'get_flattened_data') else f.getdata()))]
    if set(hot) - set(allowed):
        raise SystemExit(f"{name}: white-hot on frames {hot}, allowed only {sorted(allowed)}")
    return frames


def portrait_check(name, frames, keep_clear):
    m = keep_clear.load()
    for i, f in enumerate(frames):
        a = f.getchannel("A").load()
        if any(a[x, y] and m[x, y] for y in range(N) for x in range(N)):
            raise SystemExit(f"{name}: frame {i} draws inside a pin box")
    return frames


def portrait_coverage(frames):
    """Share of the avatar disc (r 8) each frame covers: the caster must stay readable."""
    m = disc_mask(8).load()
    disc = [(x, y) for y in range(N) for x in range(N) if m[x, y]]
    return [round(sum(1 for x, y in disc if f.getpixel((x, y))[3]) / len(disc), 3) for f in frames]


# ------------------------------------------------------------------------------------------------ the sigil
def ell(r, deg):
    a = math.radians(deg)
    return CX + ERX * r * math.cos(a), CY + ERY * r * math.sin(a)


def ring_pts(r, step=3):
    return [ell(r, d) for d in range(0, 360, step)]


def arm_pts(phase, reach=1.0, steps=72):
    out = []
    for k in range(steps + 1):
        u = k / steps
        if u > reach:
            break
        out.append(ell(0.15 + 0.85 * u, phase + 400 * u))
    return out


def spoke_pts(k, reach=1.0, start=0.0):
    """Points from the outer ring out along the edge-midpoint direction; reach 1 = the hex edge, >1 beyond it."""
    ex, ey = EDGE_MID[k]
    sx, sy = ell(1.0, math.degrees(math.atan2((ey - CY) / ERY, (ex - CX) / ERX)))
    dx, dy = ex - sx, ey - sy
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    span = max(L, 3.0)                       # the bands run at least 3 px from the ring to the edge
    n = 8
    return [(sx + ux * span * u, sy + uy * span * u) for u in (s / n * reach for s in range(n + 1)) if u >= start]


def sigil_temp(i):
    """0 dark .. 1 burning .. 2 white-hot (the spokes' tick and the hold's first tick)."""
    if i in (SPOKES, HOLD[0]):
        return 2
    if i < SETTLE:
        return 1
    return 1 - clamp01((i - SETTLE) / SIGIL_COOL)


def sigil(i):
    """The burning-gold sigil: a spark at the caster's feet, two arms spiral out, the outer ring closes, the spokes
    leave the hex on tick 6, pulses race outward while the palace stands, it cools to the dais's demon gold."""
    f = frame()
    temp = sigil_temp(i)
    if temp <= 0:
        return f
    hot = temp >= 2
    top = WHITE if hot else (B2 if temp >= 1 else (G_BRI if temp > 0.55 else (G_MID if temp > 0.25 else G_DEEP)))
    bot = B1 if hot else (G_BRI if temp >= 1 else (G_MID if temp > 0.55 else G_DEEP))
    if i == 0:                                                 # the spark at the caster's feet (front of the pin)
        for dx, dy, c in ((0, 2, B2), (1, 2, B2), (-1, 2, B1), (2, 2, B1), (0, 3, B1)):
            px(f, CX + dx, CY + dy, c)
        return mask_sigil(f)
    reach = clamp01(i / (SPOKES - 1)) if i < SPOKES else 1.0
    for ph in (0, 180):
        for k, (x, y) in enumerate(arm_pts(ph, reach)):
            px(f, x, y, top if k % 3 else bot)
        if i < SPOKES:                                          # the arms' heads
            hx, hy = arm_pts(ph, reach)[-1]
            px(f, hx, hy, B2)
            px(f, hx + 1, hy, B2)
    if i >= SPOKES - 2:                                         # the outer ring closes, bevelled (lit top, deep under)
        for x, y in ring_pts(1.0):
            px(f, x, y - 0.5, top)
            px(f, x, y + 0.5, bot)
        for x, y in ring_pts(0.55, 6):
            px(f, x, y, bot)
    if i >= SPOKES:                                             # the six bands out to the edge midpoints
        for k in range(6):
            for x, y in spoke_pts(k, 1.0):
                px(f, x, y, top if (i <= SPOKES + 1 or temp < 1) else bot)
    if i in (SPOKES, SPOKES + 1):                               # the energy leaves the hex: past the edge, then gone
        for k in range(6):
            for x, y in spoke_pts(k, 1.9, start=1.0 if i == SPOKES else 1.45):
                px(f, x, y, WHITE if i == SPOKES else B2)
    if SPOKES < i < SETTLE and i not in HOLD:                  # pulses race outward along the arms and spokes
        u = ((i - SPOKES) * 0.2) % 1.0
        for ph in (0, 180):
            x, y = ell(0.15 + 0.85 * u, ph + 400 * u)
            px(f, x, y, B2)
            px(f, x + 1, y, B2)
        for k in range(6):
            pts = spoke_pts(k)
            x, y = pts[(i - SPOKES) % len(pts)]
            px(f, x, y, B2)
    if i >= SPOKES:                                             # ember light in the cracks between the rings
        for deg in (30, 110, 200, 290):
            x, y = ell(0.78, deg)
            px(f, x, y, E2 if temp >= 1 else E1)
    return mask_sigil(f)


def mask_sigil(f):
    """The sigil lies on the ground: its back arc passes behind the caster's portrait."""
    return clear_mask(f, disc_mask(9.5))


def embers(i):
    """Embers lifting off the floor as the gates sink and the sigil cools."""
    f = frame()
    if i < GATE_SINK_AT:
        return f
    rnd = random.Random(7)
    for k in range(10):
        x0 = rnd.choice((rnd.uniform(5, 14), rnd.uniform(36, 45), rnd.uniform(8, 42)))
        y0 = rnd.uniform(38, 45) if k < 6 else rnd.uniform(28, 34)
        start = GATE_SINK_AT + rnd.randint(0, 8)
        t = i - start
        if 0 <= t < 7:
            x, y = x0 + (1 if (t + k) % 4 < 2 else 0), y0 - t * 1.5
            if SAFE_EDGE + 1 <= y and not (PIN[0] <= x <= PIN[2] and PIN[1] <= y <= PIN[3]):
                px(f, x, y, (E3, E2, E2, E1, E1, E0, E0)[t])
    return f


# ------------------------------------------------------------------------------------------------ the gates
# One gate, 12 x 20 (slab x 1-10, horns overhang x 0 and 11), facing the viewer, lit from the top left.
# .=clear H=burning gold G=demon gold K=deep gold L/l/s/m/d=sandstone hi..dark o=shadow E=eyes T=throat R/r=ember
GATE_MAP = [
    "H..........H",
    "GK........KG",
    ".KLLLLLLLLK.",
    ".ddllllllddl"[:12],
    ".lEddlldEdl.",
    ".llEEmmEEll.",
    ".llmoommlll.",
    ".loGooooGol.",
    ".loKoTToKol.",
    ".looGooGool.",
    ".llsKssKsll.",
    ".KGGGGGGGGK.",
    ".lsssssssss.",
    ".lmGmmRmGmd.",
    ".lmmmmrmmmd.",
    ".lmmmmRmmmd.",
    ".lmGmmrmGmd.",
    ".lmmmmRmmmd.",
    ".lmmmmrmmmd.",
    ".sssssssssd.",
]
GW, GH = 12, len(GATE_MAP)
GATE_BASE = 45
GATES = (3, 35)                    # left edge of each map (slab x 4-13 and 36-45)


def gate_sprite(eyes_col, throat_col, flip):
    g = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    col = {"H": B1, "G": G_BRI, "K": G_MID, "L": SS_HI, "l": SS_L, "s": SS, "m": SS_M, "d": SS_D, "o": SHADOW,
           "E": eyes_col, "T": throat_col, "R": E1, "r": E0}
    for y, row in enumerate(GATE_MAP):
        row = row.ljust(GW, ".")
        for x, ch in enumerate(row):
            if ch != ".":
                g.putpixel((x, y), (*col[ch], 255))
    if flip:
        g = g.transpose(Image.FLIP_LEFT_RIGHT)
        # keep the light from the top left: relight the slab's outer columns after the flip
        for y in range(3, GH):
            if g.getpixel((1, y))[:3] in (SS_D, SS):
                g.putpixel((1, y), (*SS_L, 255))
            if g.getpixel((10, y))[:3] in (SS_L, SS):
                g.putpixel((10, y), (*SS_D, 255) if y >= 12 else (*SS, 255))
    return g


def gate_colours(i):
    if i == HOLD[0]:
        return WHITE, E3
    if i == HOLD[1] or RING1 <= i < RING1 + 2:
        return B2, E3
    if i < SETTLE:
        return B1, E2
    return (G_BRI, E2) if i < GATE_SINK_AT + 3 else (G_MID, E1)


def gate_layer(i):
    f = frame()
    t = i - RING1
    if t < 0:
        return f
    up = ease_back((t + 1) / GATE_RISE)
    if i >= GATE_SINK_AT:
        up = 1 - ease_in((i - GATE_SINK_AT) / GATE_SINK)
    if up <= 0:
        return f
    eyes, throat = gate_colours(i)
    for gx, flip in ((GATES[0], False), (GATES[1], True)):
        n = frame()
        n.alpha_composite(gate_sprite(eyes, throat, flip), (gx, GATE_BASE - round(up * GH)))
        clip_below(n, GATE_BASE)
        outline_alpha(n)
        clip_below(n, GATE_BASE)
        f.alpha_composite(n)
    return f


def torn_ground(i):
    """The torn earth at each gate's foot: a lip of broken basalt with ember light in the tear."""
    f = frame()
    t = i - RING1
    if t < 0 or i > GATE_SINK_AT + GATE_SINK + 2:
        return f
    glow = t < GATE_RISE + 2 or GATE_SINK_AT <= i
    for gx in GATES:
        for k, x in enumerate(range(gx, gx + GW)):
            px(f, x, GATE_BASE, ST_L if k % 3 else ST)
            px(f, x, GATE_BASE + 1, SHADOW)
            if glow and k % 2 == 0:
                px(f, x, GATE_BASE, E2 if (t < 3 or i >= GATE_SINK_AT) else E1)
    return f


def chips(i):
    """Basalt and sandstone chips thrown up by the tear (2 x 2, outlined): an arc up and back down."""
    f = frame()
    t = i - RING1
    if not 0 <= t < 9:
        return f
    rnd = random.Random(3)
    for gx, face in ((GATES[0], -1), (GATES[1], 1)):
        for k in range(4):
            vx = rnd.uniform(-1.2, 1.2) + face * 0.5
            vy = rnd.uniform(-4.0, -2.6)
            x = gx + GW / 2 + rnd.uniform(-5, 4) + vx * t
            y = GATE_BASE - 2 + vy * t + 0.55 * t * t
            if not (SAFE_EDGE + 1 <= x <= N - SAFE_EDGE - 3 and SAFE_EDGE + 1 <= y < GATE_BASE - 1):
                continue
            if PIN[0] - 1 <= x <= PIN[2] and PIN[1] <= y <= PIN[3]:
                continue
            n = frame()
            c = SS_L if k % 2 else ST_L
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                px(n, x + dx, y + dy, c)
            px(n, x, y, SS_HI if k % 2 else ST_L)
            outline_alpha(n)
            f.alpha_composite(n)
    return f


# ------------------------------------------------------------------------------------------------ the palace
PALACE_BASE = 31
TOWERS = (10, 40)
# tower tiers: (roof top y, roof half width, body top y, body half width); the body runs to the next roof
TIERS = ((4, 4, 6, 2), (10, 5, 12, 3), (17, 6, 19, 4))


def palace_sprite(ridge, ridge_tip, window):
    """The demon palace at rest: a lacquered wall with a moon gate, two three-tier pagoda towers. Sandstone-dark
    walls lit on the left, shadow roofs with demon-gold ridges and upturned tips, ember windows."""
    f = frame()
    d = ImageDraw.Draw(f)
    d.rectangle([8, 8, 42, PALACE_BASE - 1], fill=(*SS_D, 255))                  # the wall
    d.line([8, 8, 8, PALACE_BASE - 1], fill=(*SS_M, 255))
    for y in (14, 20, 26):
        d.line([9, y, 41, y], fill=(*SHADOW, 255))
    d.rectangle([5, 6, 45, 7], fill=(*SHADOW, 255))                               # the wall's eave
    for tx in TOWERS:
        for k, (ry, rw, by, bw) in enumerate(TIERS):
            nxt = TIERS[k + 1][0] if k + 1 < len(TIERS) else PALACE_BASE
            d.rectangle([tx - bw, by, tx + bw, nxt - 1], fill=(*SS_D, 255))      # body
            d.line([tx - bw, by, tx - bw, nxt - 1], fill=(*SS_M, 255))
            d.rectangle([tx - rw, ry, tx + rw, ry + 1], fill=(*SHADOW, 255))     # roof
            d.line([tx - rw + 1, ry + 2, tx + rw - 1, ry + 2], fill=(*SHADOW, 255))
        d.point([(tx, 8), (tx - 1, 14), (tx + 1, 14), (tx - 2, 22), (tx + 2, 22)], fill=(*window, 255))
    f = clear_mask(f, door_mask())
    outline_alpha(f)
    f = clear_mask(f, door_mask())
    d = ImageDraw.Draw(f)
    for tx in TOWERS:                                                             # gold ridges, upturned tips, finial
        for ry, rw, _, _ in TIERS:
            d.line([tx - rw + 1, ry, tx + rw - 1, ry], fill=(*ridge, 255))
            d.point([(tx - rw, ry - 1), (tx + rw, ry - 1)], fill=(*ridge_tip, 255))
        d.point([(tx, 3)], fill=(*ridge_tip, 255))
    for x in range(6, 45):
        if f.getpixel((x, 6))[3]:
            d.point([(x, 6)], fill=(*ridge, 255))
    f = clear_mask(f, door_mask())
    return f


ARCH_R = 11.3


def arch(progress, col, col_hi):
    """The moon gate's arch: a demon-gold ring round the door, traced up from both jambs to the crest."""
    f = frame()
    x0, y0 = DISC
    if progress <= 0:
        return f
    for yy in range(y0, PALACE_BASE):                                   # the jambs
        for xx in (14, 36):
            px(f, xx, yy, col if yy % 3 else G_DEEP)
    sweep = 90 * clamp01(progress)
    deg = 0.0
    while deg <= sweep:
        for base, s in ((180, 1), (360, -1)):
            a = math.radians(base + s * deg)
            px(f, x0 + ARCH_R * math.cos(a), y0 + ARCH_R * math.sin(a), col_hi if int(deg) % 18 < 9 else col)
        deg += 3
    return f


def crest(eye, horn):
    """The horned oni crest on the arch's keystone, over the caster's head."""
    f = frame()
    for x, y, c in ((23, 3, horn), (27, 3, horn), (23, 4, G_MID), (24, 4, G_BRI), (25, 4, eye), (26, 4, G_BRI),
                    (27, 4, G_MID), (24, 5, G_DEEP), (25, 5, G_MID), (26, 5, G_DEEP)):
        px(f, x, y, c)
    return f


def palace_colours(i):
    if i == HOLD[0]:
        return WHITE, WHITE, E3
    if i == HOLD[1]:
        return B2, WHITE if False else B2, E3
    if i < SETTLE:
        return G_BRI, B1, E2
    return G_MID, G_BRI, E1


def palace_layer(i):
    f = frame()
    if i < PALACE_AT:
        return f
    up = ease_out((i - PALACE_AT + 1) / PALACE_RISE)
    if i >= SETTLE:
        up = 1 - ease_in((i - SETTLE + 1) / PALACE_SINK)
    if up <= 0:
        return f
    ridge, tip, window = palace_colours(i)
    off = round((1 - up) * 28)
    f.alpha_composite(palace_sprite(ridge, tip, window), (0, off))
    clip_below(f, PALACE_BASE)
    if i >= ARCH_AT:                                                     # the arch and crest stand with the palace
        prog = clamp01((i - ARCH_AT + 1) / 4)
        a = arch(prog, G_MID if i < SETTLE else G_DEEP, ridge)
        if off:
            a2 = frame()
            a2.alpha_composite(a, (0, off))
            a = clip_below(a2, PALACE_BASE)
        f.alpha_composite(a)
        if prog >= 1:
            c = crest(window if i not in HOLD else (WHITE if i == HOLD[0] else B2), tip)
            if off:
                c2 = frame()
                c2.alpha_composite(c, (0, off))
                c = clip_below(c2, PALACE_BASE)
            f.alpha_composite(c)
    return clear_mask(f, door_mask())          # after the offset: nothing slides through the door onto the caster


# ------------------------------------------------------------------------------------------------ assets
def rise():
    fr = []
    for i in range(LEN):
        f = frame()
        f.alpha_composite(sigil(i))
        f.alpha_composite(palace_layer(i))
        f.alpha_composite(torn_ground(i))
        f.alpha_composite(gate_layer(i))
        f.alpha_composite(chips(i))
        f.alpha_composite(embers(i))
        fr.append(f)
    return fr


LOOP_CLEAR = None


def master_loop():
    """The 2-round self-buff: ember licks along the caster's flanks (outside the pin), motes rising, a demon-gold
    glint at the hex's side vertices on the beat. Peak on frame 0."""
    fr = []
    for i in range(LOOP_LEN):
        f = frame()
        beat = 1 - i / LOOP_LEN
        for side, x0 in ((-1, 13), (1, 37)):                    # a flame lick hugging each flank, 2 px wide
            top = 22 - round(6 * beat) - (2 if i == 0 else 0)          # tallest on the beat
            for y in range(top, 30):
                u = (y - top) / max(1, 29 - top)                       # 0 at the tip, 1 at the foot
                wob = 1 if ((y + i * (2 if side < 0 else 3)) % 6) < 3 else 0
                x = x0 + side * wob
                c = E3 if u > 0.75 else (E2 if u > 0.4 else (E1 if u > 0.15 else E0))
                if i == 0 and u > 0.55:
                    c = B1
                px(f, x, y, c)
                if u > 0.35:
                    px(f, x + side, y, E1 if u < 0.75 else E2)
        for k, (x0, ph) in enumerate(((10, 0), (40, 6), (8, 11), (42, 3))):
            u = ((i + ph) % LOOP_LEN) / LOOP_LEN
            y = 34 - u * 24
            x = x0 + (1 if (i + k) % 6 < 3 else 0)
            px(f, x, y, E3 if u < 0.3 else (E2 if u < 0.6 else (E1 if u < 0.85 else E0)))
        if i <= 2:
            for vx, s in ((6, 1), (44, -1)):
                px(f, vx, 25, (B2, G_BRI, G_MID)[i])
                px(f, vx + s, 25, (G_BRI, G_MID, G_DEEP)[i])
                if i == 0:
                    px(f, vx, 24, G_MID)
        fr.append(clear_mask(f, box_mask(PIN, PIN_BELOW, BADGE)))
    return fr


def dais_tile():
    """The caster's hex: the sigil burned into the basalt. A square tile the engine stretches onto the hex box
    (2:1), so the rings are round here and match the appear's ground ellipse (outer r 20, inner r 11 = 0.55);
    six bands run to the edge midpoints, where the domain's bands meet. Transparent outside the hex."""
    T = N
    c = T / 2
    rnd = random.Random(11)
    f = Image.new("RGBA", (T, T), (*ST, 255))
    pts = [(x * 10 + rnd.randint(-3, 3) + 5, y * 10 + rnd.randint(-3, 3) + 5) for y in range(5) for x in range(5)]
    for y in range(T):                                                  # basalt flags, dark seams, ember in some
        for x in range(T):
            ds = sorted(((x - a) ** 2 + (y - b) ** 2, k) for k, (a, b) in enumerate(pts))
            (d0, k0), (d1, k1) = ds[0], ds[1]
            if math.sqrt(d1) - math.sqrt(d0) < 1.2:
                f.putpixel((x, y), (*(E1 if (k0 + k1) % 5 == 0 else SHADOW), 255))
            else:
                f.putpixel((x, y), (*(ST_L if y < pts[k0][1] - 1 else (ST if k0 % 2 else ST_D)), 255))

    def band(points, w):
        """A bevelled gold band: lit top edge, body, deep lower edge, shadow under it."""
        for x, y in points:
            for dy in range(-w - 1, w + 2):
                if abs(dy) == w + 1:
                    if f.getpixel((int(x) % T, min(T - 1, max(0, int(y + dy)))))[:3] not in (G_BRI, G_MID, G_DEEP):
                        px(f, x, y + dy, SHADOW)
        for x, y in points:
            for dy in range(-w, w + 1):
                px(f, x, y + dy, B1 if dy < 0 else (G_BRI if dy == 0 else G_DEEP))

    for k in range(6):
        a = math.radians(-90 + 60 * k)
        ex, ey = c + (T / 2) * math.cos(a) * 0.866, c + (T / 2) * math.sin(a) * 0.866 / 0.866 * 1.0
        mx, my = [(c, 0), (43.75, 12.5), (43.75, 37.5), (c, T), (6.25, 37.5), (6.25, 12.5)][k]
        sx, sy = c + 20 * (mx - c) / math.hypot(mx - c, my - c), c + 20 * (my - c) / math.hypot(mx - c, my - c)
        n = 16
        band([(sx + (mx - sx) * s / n, sy + (my - sy) * s / n) for s in range(n + 1)], 1)
    band([(c + 20 * math.cos(math.radians(d)), c + 20 * math.sin(math.radians(d))) for d in range(0, 360, 2)], 1)
    band([(c + 11 * math.cos(math.radians(d)), c + 11 * math.sin(math.radians(d))) for d in range(0, 360, 3)], 0)
    for ph in (0, 180):                                                 # the spiral arms, burned in
        for k in range(80):
            u = k / 80
            r = 20 * (0.15 + 0.85 * u)
            if 12.5 < r < 18.5 or r < 9.5:
                d = math.radians(ph + 400 * u)
                px(f, c + r * math.cos(d), c + r * math.sin(d), G_DEEP if k % 3 else G_MID)
    for d in (30, 110, 200, 290):
        px(f, c + 15.6 * math.cos(math.radians(d)), c + 15.6 * math.sin(math.radians(d)), E2)
    m = Image.new("L", (T, T), 0)
    ImageDraw.Draw(m).polygon([(0, c), (T / 4, 0), (3 * T / 4, 0), (T, c), (3 * T / 4, T), (T / 4, T)], fill=255)
    f.putalpha(m)
    return f


def assets():
    r = rise()
    edge_check("rise", r)
    palette_check("rise", r)
    white_check("rise", r, {SPOKES, HOLD[0]})
    lp = master_loop()
    edge_check("loop", lp)
    palette_check("loop", lp)
    white_check("loop", lp, set())
    portrait_check("loop", lp, box_mask(PIN, PIN_BELOW, BADGE))
    cov = portrait_coverage(r)
    if max(cov) > 0.08:
        raise SystemExit(f"rise: the caster's avatar disc is {max(cov):.0%} covered on frame {cov.index(max(cov))}")
    return [
        (f"anim_sbk_gates_rise_{VER}.webp", r,
         f"appear on the SELF tag: sigil kindles 0-5, spokes leave the hex {SPOKES}, gates tear up on ring 1 ({RING1}), "
         f"palace {PALACE_AT}-19, held beat {HOLD[0]}-{HOLD[1]} on the seal peak, settle {SETTLE}-{LEN - 1}",
         {"avatar_disc_cover_max": max(cov)}),
        (f"anim_sbk_master_loop_{VER}.webp", lp, "static loop on the SELF tag (2 rounds): flank ember licks, motes, "
         "vertex glints on the beat; pin boxes and clan badge clear", {}),
    ]


def export(out_dir, sheet=None):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for name, frames, note, extra in assets()[:1]:
        assert len(frames) <= 80
        p = os.path.join(out_dir, name)
        strip(frames).save(p, lossless=True, quality=100, method=6)
        size = os.path.getsize(p)
        assert size < MAX_BYTES, (name, size)
        rows.append({"file": f"art/subaku_palace/gates/exports/{name}", "type": "ANIMATION", "frames": len(frames),
                     "speed": MS, "bytes": size, "note": note, **extra})
    with open(os.path.join(out_dir, f"sbk_gates_ratio25_{VER}.json"), "w") as fh:
        json.dump({"source": "art/subaku_palace/gates/build_gates.py", "timing": "art/subaku_palace/TIMING.md v1",
                   "ring1": RING1, "seal_peak": SEAL_PEAK, "assets": rows}, fh, indent=1)
        fh.write("\n")
    for r in rows:
        print(r["file"], r["frames"], r["bytes"])
    if sheet:
        raw_sheet(sheet)


def raw_sheet(path):
    """Every frame of both strips at x4 on a mid-grey board with the pin box outlined (authoring check)."""
    r, lp = rise(), master_loop()
    Z = 4
    cols = 10
    rows_r = (len(r) + cols - 1) // cols
    rows_l = (len(lp) + cols - 1) // cols
    s = Image.new("RGBA", (cols * N * Z, (rows_r + rows_l) * (N * Z + 12) + 4), (70, 70, 78, 255))
    d = ImageDraw.Draw(s)
    for j, (f, lab) in enumerate([(f, f"rise f{i}") for i, f in enumerate(r)] + [(f, f"loop f{i}") for i, f in enumerate(lp)]):
        row = j // cols if j < len(r) else rows_r + (j - len(r)) // cols
        col = j % cols if j < len(r) else (j - len(r)) % cols
        x, y = col * N * Z, row * (N * Z + 12)
        d.text((x + 3, y), lab, fill=(240, 230, 200))
        g = f.resize((N * Z, N * Z), Image.NEAREST)
        y += 12
        d.rectangle([x + PIN[0] * Z, y + PIN[1] * Z, x + PIN[2] * Z + Z - 1, y + PIN[3] * Z + Z - 1], outline=(90, 150, 200))
        d.ellipse([x + (DISC[0] - 8) * Z, y + (DISC[1] - 8) * Z, x + (DISC[0] + 8) * Z, y + (DISC[1] + 8) * Z], outline=(150, 200, 230))
        s.alpha_composite(g, (x, y))
    s.convert("RGB").save(path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=EXPORTS)
    ap.add_argument("--sheet", help="also write a raw x4 contact sheet of every frame here")
    a = ap.parse_args()
    export(a.out, a.sheet)
