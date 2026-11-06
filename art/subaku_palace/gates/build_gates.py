#!/usr/bin/env python3
"""Subaku Palace: the centre payoff on the caster's hex (player EVENT jutsu jELEiw5W3N4m2R3oJm3Pk).

    python3 art/subaku_palace/gates/build_gates.py [--out DIR] [--sheet PNG]

One asset, the appear on the SELF tag (increasedamagegiven): anim_sbk_gates_rise_v3, 38 frames x 50 ms. Director
2026-11-05: the sigil is symbolic and fades within the cast; no dais tile, no lingering buff loop. Timing from
art/subaku_palace/TIMING.md (ring 1 lands on tick 7, the seal pulse peaks on tick 20).

- 0-5    the burning-gold sigil kindles round the caster's feet and spirals out along the ground.
- 6      its bands flash white-hot and run out of the frame (the energy leaves the hex, the tick before ring 1).
- 7-12   two red sandstone gates, each crowned with a snarling oni face, tear up out of the stone on either side of
         the caster, throwing chips.
- 13-19  pagoda roofs stack up on both gates (gold ridges, upturned tips, finials): the two gate-towers flanking the
         caster are the demon palace's front.
- 20-21  the held beat on the seal peak: nothing moves; ridges, finials and the oni eyes white-hot on 20 only.
- 22-37  the roofs fold down, the gates sink back into the floor shedding embers, the sigil cools to demon gold and
         goes out. The last frames are empty: nothing lingers.

Engine geometry (theninjarpg origin/main cb755375; see README.md for file:lines): the clip is ONE hex height square
(EFFECT_ANIMATION_HEX_RATIO = 1), centred on the hex, fetched as a 50 px rendition, sampled linearly, drawn OVER the
fighters and their meters. On the 50 px frame: the hex's flat top edge is y 0, its bottom edge y 50, and the frame spans
the middle half of the hex width. The caster is an LPC character avatar 1.35 h tall centred at 0.825 h: its feet sit
at about y 38 and a typical body covers x 10-40 from above the frame down to y 40. Everything here stays out of that
column except the ground sigil's front arc below the feet. Players without a character appearance still get the old
marker (x 0-50, y up to 35); that coverage is reported, not gated.

Drawn on the 50 px grid (2-3 px clusters, 1 px outlines), RGB filled under transparent pixels, exported x3 nearest
(150 px frames). Build checks: nothing within 2 px of the frame edge; every opaque pixel in the TIMING.md palette;
white-hot on ticks 6 and 20 only; the LPC head/torso core (x 14-36) never covered, the whole envelope at most 12%; the last two frames empty.
Pillow only.
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
VER = "v3"
MAX_BODY_COVER = 0.12   # the whole envelope: the gates stand in front of the arms' outer edges
MAX_CORE_COVER = 0.0    # head, torso and legs (x 14-36): never covered

# ------------------------------------------------------------------------------------------------ timing (TIMING.md)
RING1 = 7
SEAL_PEAK = 20
LEN = 38
SPOKES = RING1 - 1
GATE_RISE = 6           # 7-12
ROOF_AT = 13            # tiers 13-19
HOLD = (SEAL_PEAK, SEAL_PEAK + 1)
SETTLE = SEAL_PEAK + 2  # 22
ROOF_FOLD = 5           # 22-26
GATE_SINK_AT = 25
GATE_SINK = 8           # 25-32
SIGIL_COOL = 12         # 22-33, out by 34

# ------------------------------------------------------------------------------------------------ palette (TIMING.md)
SHADOW = (22, 10, 9)
SS_D, SS_M, SS, SS_L, SS_HI = (90, 30, 20), (122, 42, 28), (168, 67, 42), (201, 101, 61), (227, 144, 106)
G_DEEP, G_MID, G_BRI = (138, 90, 18), (196, 138, 28), (232, 180, 58)
B1, B2, WHITE = (255, 207, 74), (255, 229, 138), (255, 244, 200)
E0, E1, E2, E3 = (110, 12, 8), (184, 28, 16), (255, 74, 28), (255, 150, 60)
ST, ST_L = (43, 28, 26), (54, 37, 33)                                   # basalt, from the domain tile
PALETTE = {SHADOW, SS_D, SS_M, SS, SS_L, SS_HI, G_DEEP, G_MID, G_BRI, B1, B2, WHITE, E0, E1, E2, E3, ST, ST_L}

# ------------------------------------------------------------------------------------------------ geometry (1 hex height)
FEET = (25, 38)                 # LPC foot contact: groundY 0.234 h
SIG_C = (25, 40)                # the sigil centres just in front of the feet
SIG_RX, SIG_RY = 21.0, 6.0
GATE_BASE = 45                  # the gates stand on the ground plane level with the sigil's front
GATES = (4, 39)                 # slab x 4-10 and 39-45 (outlines at 3/11 and 38/46)


def lpc_body_mask():
    """Envelope of a typical LPC character (front, combat idle) on this frame: LPC px (x 18-46, y 10-62) mapped by
    clip = 25 + (u - 32) * 1.055, 8.75 + (v - 32) * 1.055. Head and shoulders run off the top of the frame."""
    m = Image.new("L", (N, N), 0)
    d = ImageDraw.Draw(m)
    d.rectangle([14, 0, 36, 8], fill=255)        # head / neck (headgear widens this above the frame)
    d.rectangle([10, 8, 40, 30], fill=255)       # shoulders, arms, torso
    d.rectangle([14, 30, 36, 40], fill=255)      # legs to the feet
    return m


def legacy_marker_mask():
    """Players without a character appearance: the location marker, h wide, centred 0.9 h, 1.2 h tall."""
    m = Image.new("L", (N, N), 0)
    ImageDraw.Draw(m).ellipse([0, -12, 50, 35], fill=255)
    return m


def lpc_core_mask():
    m = Image.new("L", (N, N), 0)
    ImageDraw.Draw(m).rectangle([14, 0, 36, 37], fill=255)
    return m


BODY = lpc_body_mask()
CORE = lpc_core_mask()


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


def pixels(f):
    return f.get_flattened_data() if hasattr(f, "get_flattened_data") else f.getdata()


def fill_under(img):
    """RGB under every transparent pixel copied from the nearest drawn pixel (BFS): linear filtering never pulls in
    a dark fringe. Alpha is untouched."""
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
        ImageDraw.Draw(a).rectangle([0, 0, N - 1, N - 1], outline=0)
        g.putalpha(a)
        out.append(fill_under(g) if g.getchannel("A").getbbox() else g)
    s = Image.new("RGBA", (N, N * len(out)))
    for i, f in enumerate(out):
        s.paste(f, (0, i * N))
    return s.resize((N * SCALE, N * len(out) * SCALE), Image.NEAREST)


# ------------------------------------------------------------------------------------------------ checks
def edge_check(frames):
    for i, f in enumerate(frames):
        bb = f.getchannel("A").getbbox()
        if bb and (bb[0] < SAFE_EDGE or bb[1] < SAFE_EDGE or bb[2] > N - SAFE_EDGE or bb[3] > N - SAFE_EDGE):
            raise SystemExit(f"frame {i} reaches within {SAFE_EDGE} px of the clip edge {bb} (it would clip)")


def palette_check(frames):
    for i, f in enumerate(frames):
        for p in pixels(f):
            if p[3] and p[3] != 255:
                raise SystemExit(f"frame {i} has soft alpha {p[3]} (hard alpha only)")
            if p[3] and p[:3] not in PALETTE:
                raise SystemExit(f"frame {i} colour {p[:3]} is not in the TIMING.md palette")


def white_check(frames, allowed):
    hot = [i for i, f in enumerate(frames) if any(p[3] and p[:3] == WHITE for p in pixels(f))]
    if set(hot) - set(allowed):
        raise SystemExit(f"white-hot on frames {hot}, allowed only {sorted(allowed)}")


def coverage(frames, mask):
    m = mask.load()
    cells = [(x, y) for y in range(N) for x in range(N) if m[x, y]]
    return [round(sum(1 for x, y in cells if f.getpixel((x, y))[3]) / len(cells), 3) for f in frames]


# ------------------------------------------------------------------------------------------------ the sigil
def ell(r, deg):
    a = math.radians(deg)
    return SIG_C[0] + SIG_RX * r * math.cos(a), SIG_C[1] + SIG_RY * r * math.sin(a)


def sigil_temp(i):
    if i in (SPOKES, HOLD[0]):
        return 2
    if i < SETTLE:
        return 1
    return 1 - clamp01((i - SETTLE) / SIGIL_COOL)


# the bands leave toward the hex's bottom edge midpoint and its two lower side edges (the other three exits lie
# behind the caster or outside the frame)
SPOKE_DIRS = (90, 160, 20)


def spoke_pts(deg, start, end, n=10):
    out = []
    for s in range(n + 1):
        u = start + (end - start) * s / n
        out.append((SIG_C[0] + SIG_RX * u * math.cos(math.radians(deg)),
                    SIG_C[1] + SIG_RY * u * math.sin(math.radians(deg)) * (1.1 if deg == 90 else 1.0)))
    return out


def sigil(i):
    f = frame()
    temp = sigil_temp(i)
    if temp <= 0:
        return f
    hot = temp >= 2
    top = WHITE if hot else (B2 if temp >= 1 else (G_BRI if temp > 0.6 else (G_MID if temp > 0.3 else G_DEEP)))
    bot = B1 if hot else (G_BRI if temp >= 1 else (G_MID if temp > 0.6 else G_DEEP))
    if i == 0:                                           # the spark at the caster's feet
        for dx, dy, c in ((0, 2, B2), (1, 2, B2), (-1, 2, B1), (2, 2, B1), (0, 3, B1)):
            px(f, FEET[0] + dx, FEET[1] + dy, c)
        return clear_mask(f, BODY)
    reach = clamp01(i / (SPOKES - 1)) if i < SPOKES else 1.0
    for ph in (0, 180):                                  # two arms spiral out from under the feet
        pts = []
        for k in range(73):
            u = k / 72
            if u > reach:
                break
            pts.append(ell(0.18 + 0.82 * u, ph + 400 * u))
        for k, (x, y) in enumerate(pts):
            px(f, x, y, top if k % 3 else bot)
        if i < SPOKES and pts:
            hx, hy = pts[-1]
            px(f, hx, hy, B2)
            px(f, hx + 1, hy, B2)
    if i >= SPOKES - 2:                                  # the outer ring closes, bevelled
        for d in range(0, 360, 3):
            x, y = ell(1.0, d)
            px(f, x, y - 0.5, top)
            px(f, x, y + 0.5, bot)
        for d in range(0, 360, 7):
            x, y = ell(0.55, d)
            px(f, x, y, bot)
    if i >= SPOKES:                                      # three bands out toward the hex edges
        for deg in SPOKE_DIRS:
            for x, y in spoke_pts(deg, 1.0, 1.08):
                px(f, x, y, top if (i <= SPOKES + 1 or temp < 1) else bot)
    if i in (SPOKES, SPOKES + 1):                        # the energy leaves the hex: out to the frame edge, then gone
        for deg in SPOKE_DIRS:
            for x, y in spoke_pts(deg, 1.0 if i == SPOKES else 1.05, 1.12 if deg == 90 else 1.18, 12):
                if SAFE_EDGE <= x <= N - SAFE_EDGE - 1 and y <= N - SAFE_EDGE - 1:
                    px(f, x, y, WHITE if i == SPOKES else B2)
    if SPOKES < i < SETTLE and i not in HOLD:            # pulses race round the ring's front
        u = ((i - SPOKES) * 0.13) % 1.0
        for ph in (20, 160):
            x, y = ell(1.0, ph + (140 * u if ph == 20 else -140 * u))
            px(f, x, y, B2)
            px(f, x + 1, y, B2)
    if i >= SPOKES:                                      # ember light in the cracks between the rings
        for deg in (35, 145, 75, 110):
            x, y = ell(0.78, deg)
            px(f, x, y, E2 if temp >= 1 else E1)
    return clear_mask(f, BODY)                           # the sigil lies on the ground: the caster stands over it


# ------------------------------------------------------------------------------------------------ the gates
# One gate, 8 x 26, front view, lit from the top left. A snarling oni face crowns a carved door.
# .=clear L/l/s/m/d sandstone hi..dark  o=shadow  E=eyes  T=throat  F=fangs  G/K gold  R/r ember
GATE_MAP = [
    "K.....K",   # horn tips
    "GK...KG",   # horns
    "LLLLLLs",   # cap
    "loolood",   # brows: a hard V
    "lEoloEd",   # burning eyes
    "llEmEld",   # slanting in under the brows
    "llmomld",   # snout
    "lFoooFd",   # maw, upper fangs
    "loTTTod",   # ember throat
    "lFoooFd",   # lower fangs
    "KGGGGGK",   # demon-gold collar
    "lssssss",
    "lmmRmmd",
    "lmGrGmd",
    "lmmRmmd",
    "lmmrmmd",
    "lmmRmmd",
    "lmGrGmd",
    "lmmRmmd",
    "lmmrmmd",
    "lmmRmmd",
    "lmGrGmd",
    "lmmRmmd",
    "lmmrmmd",
    "lssssss",
    "ddddddd",
]
GW, GH = 7, len(GATE_MAP)


def gate_sprite(eyes, throat, flip):
    g = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
    col = {"H": B1, "G": G_BRI, "K": G_MID, "L": SS_HI, "l": SS_L, "s": SS, "m": SS_M, "d": SS_D, "o": SHADOW,
           "E": eyes, "T": throat, "F": B2, "R": E1, "r": E0}
    for y, row in enumerate(GATE_MAP):
        for x, ch in enumerate(row):
            if ch != ".":
                g.putpixel((x, y), (*col[ch], 255))
    if flip:                                             # mirror the carving, keep the light from the top left
        g = g.transpose(Image.FLIP_LEFT_RIGHT)
        for y in range(3, GH - 1):
            for x, (a, b) in ((0, (SS_D, SS_L)), (GW - 1, (SS_L, SS_D))):
                if g.getpixel((x, y))[:3] == a:
                    g.putpixel((x, y), (*b, 255))
    return g


def gate_colours(i):
    if i == HOLD[0]:
        return WHITE, E3
    if i == HOLD[1] or RING1 <= i < RING1 + 2:
        return B2, E3
    if i < SETTLE:
        return B1, E2
    return (G_BRI, E2) if i < GATE_SINK_AT + 3 else (G_MID, E1)


def gate_rise(i):
    t = i - RING1
    if t < 0:
        return 0.0
    if i >= GATE_SINK_AT:
        return 1 - ease_in((i - GATE_SINK_AT + 1) / GATE_SINK)
    return ease_back((t + 1) / GATE_RISE)


# the pagoda tiers that crown each gate: (roof row y relative to the gate top, outer overhang, inner overhang,
# body half-height above it). Roofs reach out over the hex, away from the caster.
TIERS = ((-1, 1, 1, 3), (-5, 1, 0, 3), (-9, 0, -1, 2))


def tower_tiers(gx, flip, up, ridge, tip):
    """Roofs stacked on one gate. up 0..1 raises them tier by tier."""
    f = frame()
    d = ImageDraw.Draw(f)
    top = GATE_BASE - GH
    shown = up * len(TIERS)
    below = top                                                       # the top of whatever this tier stands on
    for k, (ry, outer, inner, _) in enumerate(TIERS):
        if shown <= k:
            break
        lift = round((1 - clamp01(shown - k)) * 3)
        y = top + ry + lift
        lo, hi = (gx - outer, gx + GW - 1 + inner) if not flip else (gx - inner, gx + GW - 1 + outer)
        body_l, body_r = gx + 1 + k, gx + GW - 2 - k
        if below - 1 >= y + 1:                                        # the tier's wall, down to the roof below
            d.rectangle([body_l, y + 1, body_r, below - 1], fill=(*SS_D, 255))
            d.line([body_l, y + 1, body_l, below - 1], fill=(*SS_M, 255))
        below = y - 1
        d.rectangle([lo, y - 1, hi, y], fill=(*SHADOW, 255))          # the roof
        d.line([lo + 1, y - 1, hi - 1, y - 1], fill=(*ridge, 255))   # its gold ridge
        out_x = lo if not flip else hi
        d.point([(out_x, y - 2)], fill=(*tip, 255))                   # the upturned outer tip
        d.point([(hi if not flip else lo, y - 2)], fill=(*ridge, 255))
        if k == 0:                                                    # an ember window under the first roof
            d.point([(gx + 3, y + 2)], fill=(*E2, 255))
    if shown >= len(TIERS):
        fy = top + TIERS[-1][0] + 0 - 3
        d.point([(gx + 3, fy), (gx + 3, fy - 1)], fill=(*tip, 255))            # the finial
    return f


def tier_colours(i):
    if i == HOLD[0]:
        return WHITE, WHITE
    if i == HOLD[1]:
        return B2, B2
    if i < SETTLE:
        return G_BRI, B1
    return G_MID, G_BRI


def tiers_up(i):
    if i < ROOF_AT:
        return 0.0
    if i >= SETTLE:
        return 1 - clamp01((i - SETTLE + 1) / ROOF_FOLD)
    return clamp01((i - ROOF_AT + 1) / 6)


def gates_layer(i):
    f = frame()
    up = gate_rise(i)
    if up <= 0:
        return f
    eyes, throat = gate_colours(i)
    ridge, tip = tier_colours(i)
    tu = tiers_up(i)
    for gx, flip in ((GATES[0], False), (GATES[1], True)):
        n = frame()
        n.alpha_composite(gate_sprite(eyes, throat, flip))  # placed below
        n = frame()
        g = frame()
        g.alpha_composite(gate_sprite(eyes, throat, flip), (gx, GATE_BASE - GH))
        if tu > 0:
            g.alpha_composite(tower_tiers(gx, flip, tu, ridge, tip))
        sink = round((1 - up) * (GH + 12))
        n.alpha_composite(g, (0, sink))
        clip_below(n, GATE_BASE)
        outline_alpha(n)
        clip_below(n, GATE_BASE + 1)
        f.alpha_composite(n)
    return f


def torn_ground(i):
    f = frame()
    t = i - RING1
    if t < 0 or i > GATE_SINK_AT + GATE_SINK + 1:
        return f
    glow = t < GATE_RISE + 2 or i >= GATE_SINK_AT
    for gx in GATES:
        for k, x in enumerate(range(gx - 1, gx + GW + 1)):
            px(f, x, GATE_BASE, ST_L if k % 3 else ST)
            px(f, x, GATE_BASE + 1, SHADOW)
            if glow and k % 2 == 1:
                px(f, x, GATE_BASE, E2 if (t < 3 or i >= GATE_SINK_AT) else E1)
    return f


def chips(i):
    """Basalt and sandstone chips thrown outward by the tear (2 x 2, outlined), kept off the caster."""
    f = frame()
    t = i - RING1
    if not 0 <= t < 8:
        return f
    rnd = random.Random(3)
    for gx, away in ((GATES[0], -1), (GATES[1], 1)):
        for k in range(3):
            vx = away * rnd.uniform(0.3, 1.0)
            vy = rnd.uniform(-3.6, -2.4)
            x = gx + GW / 2 + rnd.uniform(-3, 2) + vx * t
            y = GATE_BASE - 2 + vy * t + 0.6 * t * t
            if not (SAFE_EDGE + 1 <= x <= N - SAFE_EDGE - 3 and SAFE_EDGE + 1 <= y < GATE_BASE - 1):
                continue
            if BODY.getpixel((int(x), int(y))) or BODY.getpixel((min(N - 1, int(x) + 1), int(y))):
                continue
            n = frame()
            c = SS_L if k % 2 else ST_L
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                px(n, x + dx, y + dy, c)
            px(n, x, y, SS_HI if k % 2 else ST_L)
            outline_alpha(n)
            f.alpha_composite(n)
    return f


def embers(i):
    f = frame()
    if i < GATE_SINK_AT - 1:
        return f
    rnd = random.Random(7)
    for k in range(9):
        x0 = rnd.choice((rnd.uniform(3, 10), rnd.uniform(40, 47)))
        y0 = rnd.uniform(36, 44)
        start = GATE_SINK_AT - 1 + rnd.randint(0, 7)
        t = i - start
        if 0 <= t < 6 and i < LEN - 2:
            x, y = x0 + (1 if (t + k) % 4 < 2 else 0), y0 - t * 2
            if y >= SAFE_EDGE + 1 and not BODY.getpixel((int(x), int(y))):
                px(f, x, y, (E3, E2, E2, E1, E0, E0)[t])
    return f


# ------------------------------------------------------------------------------------------------ assets
def rise():
    fr = []
    for i in range(LEN):
        f = frame()
        f.alpha_composite(sigil(i))
        f.alpha_composite(torn_ground(i))
        f.alpha_composite(gates_layer(i))
        f.alpha_composite(chips(i))
        f.alpha_composite(embers(i))
        fr.append(f)
    return fr


def build():
    r = rise()
    edge_check(r)
    palette_check(r)
    white_check(r, {SPOKES, HOLD[0]})
    if any(f.getchannel("A").getbbox() for f in r[-2:]):
        raise SystemExit("the last two frames must be empty: nothing lingers after the appear")
    body = coverage(r, BODY)
    if max(body) > MAX_BODY_COVER:
        raise SystemExit(f"the LPC body envelope is {max(body):.1%} covered on frame {body.index(max(body))}")
    core = coverage(r, CORE)
    if max(core) > MAX_CORE_COVER:
        raise SystemExit(f"the LPC head/torso core is {max(core):.1%} covered on frame {core.index(max(core))}")
    return r, body, core, coverage(r, legacy_marker_mask())


def export(out_dir, sheet=None):
    os.makedirs(out_dir, exist_ok=True)
    r, body, core, legacy = build()
    name = f"anim_sbk_gates_rise_{VER}.webp"
    p = os.path.join(out_dir, name)
    strip(r).save(p, lossless=True, quality=100, method=6)
    size = os.path.getsize(p)
    assert size < MAX_BYTES, size
    row = {"file": f"art/subaku_palace/gates/exports/{name}", "type": "ANIMATION", "frames": len(r), "speed": MS,
           "bytes": size, "slot": "appearAnimation on the SELF increasedamagegiven effect (no staticAnimation, "
           "no staticAssetPath)",
           "clip": "1 hex height (EFFECT_ANIMATION_HEX_RATIO = 1, theninjarpg cb755375)",
           "lpc_body_cover_max": max(body), "lpc_core_cover_max": max(core), "legacy_marker_cover_max": max(legacy)}
    with open(os.path.join(out_dir, f"sbk_gates_{VER}.json"), "w") as fh:
        json.dump({"source": "art/subaku_palace/gates/build_gates.py", "timing": "art/subaku_palace/TIMING.md v1",
                   "ring1": RING1, "seal_peak": SEAL_PEAK, "assets": [row]}, fh, indent=1)
        fh.write("\n")
    print(row["file"], len(r), size, "lpc body cover max", max(body), "core", max(core), "legacy marker cover max", max(legacy))
    if sheet:
        raw_sheet(r, sheet)


def raw_sheet(r, path):
    """Every frame at x4 on a mid-grey board with the LPC body envelope and the feet outlined."""
    Z, cols = 4, 10
    rows = (len(r) + cols - 1) // cols
    s = Image.new("RGBA", (cols * N * Z, rows * (N * Z + 12) + 4), (70, 70, 78, 255))
    d = ImageDraw.Draw(s)
    edge = BODY.filter(__import__("PIL.ImageFilter", fromlist=["FIND_EDGES"]).FIND_EDGES).load()
    for j, f in enumerate(r):
        x, y = (j % cols) * N * Z, (j // cols) * (N * Z + 12)
        d.text((x + 3, y), f"f{j}", fill=(240, 230, 200))
        y += 12
        for yy in range(N):
            for xx in range(N):
                if edge[xx, yy]:
                    d.rectangle([x + xx * Z, y + yy * Z, x + xx * Z + Z - 1, y + yy * Z + Z - 1], fill=(90, 120, 150))
        d.line([x + (FEET[0] - 3) * Z, y + FEET[1] * Z, x + (FEET[0] + 3) * Z, y + FEET[1] * Z], fill=(150, 200, 230))
        s.alpha_composite(f.resize((N * Z, N * Z), Image.NEAREST), (x, y))
    s.convert("RGB").save(path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=EXPORTS)
    ap.add_argument("--sheet")
    a = ap.parse_args()
    export(a.out, a.sheet)
