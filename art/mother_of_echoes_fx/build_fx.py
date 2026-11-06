#!/usr/bin/env python3
"""The Mother of Echoes battle FX built in code (pixel art, Pillow only).

    python3 art/mother_of_echoes_fx/build_fx.py

Writes art/mother_of_echoes_fx/exports/ (fresh filenames, law 32) and exports/moe_fx_v1.json (frames, speed, use,
bytes, the spec art names each file serves). Asset list and sources: docs/design/MOTHER_OF_ECHOES_ART.md.

Renderer facts (theninjarpg@3314d122, pixi; read-only):
- libs/rendering/scenes/combatEffects.ts: every effect on a hex draws its ANIMATION clips (appear one-shot, static
  loop) as ONE square sprite of size tile.height * EFFECT_ANIMATION_HEX_RATIO, centred on the hex, in the effects
  container drawn after the actors (over the characters). EFFECT_ANIMATION_HEX_RATIO = 2.5 (libs/rendering/animation.ts).
  A staticAssetPath is a still sprite stretched to tile.width x tile.height on the `ground` layer, under the actors.
- Hexes are FLAT with height = width * HEX_ASPECT_RATIO (0.5) (libs/combat/util.ts getBattleGrid, drizzle/constants.ts).
  So in a 50 px animation frame (= 2.5 hex heights) the hex is 40 x 20 px, centred at (25, 25), vertices
  (5,25) (15,15) (35,15) (45,25) (35,35) (15,35); the 50 px STATIC tile maps onto the hex's bounding box.
- ANIMATION assets are vertical strips, gameAsset.speed = ms per frame (libs/rendering/animation.ts assetAnimationClip).
- Fighter art (libs/rendering/scenes/combatActors.ts combatActorParts, h = hex height, Y up from the hex's top edge):
  player marker h*1.2 tall and h wide centred at 0.9h, avatar disc h*0.8 at h, clan badge at x 0.9w, y 1.4h;
  status bars at y h + w/3. AI avatars are h*1.6 discs at 0.9h. In frame px (20 px per h): the player's pin spans
  x 15-35, y 5-29, the hex below's pin x 15-35 from y 25 down. Looping effects keep clear of those (director,
  2026-10-28: "mindful of player portraits"); one-shot hits are unrestricted.

House method (art/skyglass_boss_fx/animate.py, animate_an.py): drawn on the 50 px grid, stepped alpha, RGB under
transparent pixels filled from the nearest drawn pixel (the GPU filters linearly), every loop peaks on frame 0 and
shares the 0.8 s beat (16 x 50 ms), delivered enlarged x3 by nearest neighbour (150 px frames, the ANIMATION target's
112 px and STATIC's 128 px minimum widths in 25x_DATA_art_spec.json). Fades use an ordered dither, not partial alpha,
so the soft-edge share stays under the spec ceiling. No NumPy (CLAUDE.md section 9).

Palette families (docs/design/SKYGLASS_BOSS_ANIMATIONS.md readability rules): heavy ember, control violet, lingering
bile, safe cyan are taken. The Etching is a new threat (a delayed hit you must remember), so it gets its own shape and
its own family: a LATTICE of straight scored lines (no ring, chain, pool or star) in warm white and pale gold. Its
Recast replays the same lattice before the glass rises, so the hit is recognisably the mark coming due.
"""
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
EXPORTS = os.path.join(HERE, 'exports')
N = 50              # drawn grid (frame px)
MS = 50             # ms per frame (gameAsset.speed)
BEAT = 16           # 16 x 50 ms = 0.8 s shared pulse
SCALE = 3           # delivered 150 px frames
MAX_BYTES = 460800  # spec byte ceiling (ANIMATION and STATIC)
VERSION = 'v1'

# ------------------------------------------------------------------------------------------------ geometry (frame px)
C = (25.0, 25.0)
HEX = [(5, 25), (15, 15), (35, 15), (45, 25), (35, 35), (15, 35)]
# the three lattice axes run through opposite edge midpoints, so they continue straight into every neighbour
ENDS = {'T': (25, 15), 'B': (25, 35), 'UL': (10, 20), 'LL': (10, 30), 'UR': (40, 20), 'LR': (40, 30)}
SIDE = ('UL', 'LL', 'UR', 'LR')     # the junctions no portrait covers
# STATIC tile coordinates: the 50 px square is stretched onto the hex's bounding box
T_HEX = [(0, 25), (12.5, 0), (37.5, 0), (50, 25), (37.5, 50), (12.5, 50)]
T_ENDS = {'T': (25, 0), 'B': (25, 50), 'UL': (6.25, 12.5), 'LL': (6.25, 37.5), 'UR': (43.75, 12.5), 'LR': (43.75, 37.5)}

# ------------------------------------------------------------------------------------------------ palettes
INK = (14, 12, 18)
ETCH_DARK = (58, 44, 30)
SCORE = (24, 16, 10)         # the scored groove: near-black brown, the contrast on a light board
ETCH_DIM = (150, 118, 64)
ETCH_MID = (222, 184, 104)
ETCH_HOT = (255, 238, 196)
WHITE = (255, 255, 250)
GLASS_L = (236, 242, 250)
GLASS_M = (160, 176, 204)
GLASS_D = (58, 64, 88)
CYAN = (152, 214, 232)
CYAN_D = (52, 110, 138)
BONE = (228, 222, 206)
BONE_S = (168, 160, 146)
BONE_D = (44, 40, 48)
DUST = (206, 210, 222)

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def frame():
    return Image.new('RGBA', (N, N), (0, 0, 0, 0))


def px(f, x, y, rgb, keep=1.0):
    """Plot one pixel; keep < 1 drops it by an ordered dither (a fade with no partial alpha)."""
    x, y = int(round(x)), int(round(y))
    if not (0 <= x < f.width and 0 <= y < f.height):
        return
    if keep < 1.0 and BAYER[y % 4][x % 4] >= keep * 16:
        return
    f.putpixel((x, y), (*rgb, 255))


def seg(f, a, b, rgb, keep=1.0, step=0.25):
    n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
    for k in range(n + 1):
        t = k / n
        px(f, a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, rgb, keep)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def poly_mask(points, size=N):
    m = Image.new('L', (size, size), 0)
    ImageDraw.Draw(m).polygon(points, fill=255)
    return m


def clip(f, mask):
    out = frame() if f.size == (N, N) else Image.new('RGBA', f.size, (0, 0, 0, 0))
    out.paste(f, (0, 0), mask)
    return out


def portrait_mask():
    """Pixels a looping effect must leave clear: this hex's player pin, avatar, bars and clan badge, and the hex
    below's pin (its portrait rises onto this hex). Neighbours to the sides sit outside the frame's hex."""
    m = Image.new('L', (N, N), 0)
    d = ImageDraw.Draw(m)
    for dy in (0, 20):
        d.rectangle([14, 4 + dy, 36, 30 + dy], fill=255)      # marker pin, avatar disc
        d.rectangle([14, 0 + dy, 36, 4 + dy], fill=255)       # status bars
        d.rectangle([37, 3 + dy, 45, 11 + dy], fill=255)      # clan badge
    return m


PORTRAIT = None


def mind_portrait(frames):
    global PORTRAIT
    PORTRAIT = PORTRAIT or portrait_mask()
    out = []
    for f in frames:
        g = f.copy()
        a = g.getchannel('A')
        a.paste(0, (0, 0), PORTRAIT)
        g.putalpha(a)
        out.append(g)
    return out


def fill_under(img):
    """RGB under every transparent pixel copied from the nearest drawn pixel (BFS), so linear filtering never pulls
    in a dark fringe. Alpha is untouched."""
    w, h = img.size
    p = img.load()
    seen = [[p[x, y][3] > 0 for x in range(w)] for y in range(h)]
    frontier = [(x, y) for y in range(h) for x in range(w) if seen[y][x]]
    if not frontier:
        return img
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


def strip(frames, margin=True):
    out = []
    for f in frames:
        g = f.copy()
        if margin:
            a = g.getchannel('A')
            d = ImageDraw.Draw(a)
            d.rectangle([0, 0, N - 1, N - 1], outline=0)
            g.putalpha(a)
        out.append(fill_under(g))
    s = Image.new('RGBA', (N, N * len(out)))
    for i, f in enumerate(out):
        s.paste(f, (0, i * N))
    return s.resize((s.width * SCALE, s.height * SCALE), Image.NEAREST)


def pulse(i, period=BEAT):
    return 0.5 + 0.5 * math.cos(2 * math.pi * i / period)


# ------------------------------------------------------------------------------------------------ tg_etch: tile + glint
def etch_lines(img, ends, centre, widths=(4, 2, 1), cols=None, scale=1.0):
    """The etched lattice: three axes through opposite edge midpoints. Bright at the centre, dimmer toward the edge
    (low contrast at the edge, bright in the core); each spoke ends exactly on an edge midpoint, where the
    neighbour's spoke continues it, so a field reads as one scored sheet with no hex seams."""
    d = ImageDraw.Draw(img)
    cols = cols or [(ETCH_DARK, ETCH_DIM, ETCH_MID), (ETCH_DARK, ETCH_MID, ETCH_HOT)]
    outer, inner = cols
    w_out, w_mid, w_core = (max(1, round(w * scale)) for w in widths)
    for e in ends.values():
        d.line([centre, e], fill=(*outer[0], 255), width=w_out)
    for e in ends.values():
        m = lerp(centre, e, 0.5)
        d.line([m, e], fill=(*outer[1], 255), width=w_mid)
        d.line([centre, m], fill=(*inner[1], 255), width=w_mid)
    for e in ends.values():
        m = lerp(centre, e, 0.55)
        d.line([centre, m], fill=(*inner[2], 255), width=w_core)


def build_etch_tile():
    """Drawn in tile space, which the game stretches 2:1 onto the hex box, so line widths are compensated: the
    vertical axis is drawn about half as wide as the diagonals and every spoke lands about equally thick on screen.
    v2 (director, 2026-11-03: "reads faint on a light board"): each spoke is a deep near-black scored groove with a
    bright gold-white cut inside it, so it holds on snow and on dark floors alike, and the region carries a darker
    smoked haze. Still a lattice (no ring, chain, pool or star), still gold and white."""
    t = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    # v3 (art QA): the v2 1 px Bayer haze became a screen door after the 50 px CDN rendition and pixi's linear
    # stretch; the region is now tinted by sparse solid 2x2 score chips set between the spokes instead.
    for x, y in ((12, 15), (38, 15), (12, 35), (38, 35), (18, 6), (32, 6), (18, 44), (32, 44), (5, 25), (45, 25)):
        for dx in (0, 1):
            for dy in (0, 1):
                px(t, x + dx, y + dy, ETCH_DARK)
    d = ImageDraw.Draw(t)
    diag = {k: e for k, e in T_ENDS.items() if k not in ('T', 'B')}
    vert = {k: T_ENDS[k] for k in ('T', 'B')}
    bold = [(SCORE, ETCH_MID, ETCH_HOT), (SCORE, ETCH_HOT, WHITE)]
    etch_lines(t, diag, (25, 25), widths=(6, 3, 1), cols=bold)
    etch_lines(t, vert, (25, 25), widths=(3, 2, 1), cols=bold)
    # the cut's origin: a hard-edged nick of white in a dark socket at the centre
    d.rectangle([22, 20, 28, 30], fill=(*SCORE, 255))
    d.rectangle([24, 22, 26, 28], fill=(*ETCH_HOT, 255))
    d.line([(25, 23), (25, 27)], fill=(*WHITE, 255))
    t = clip(t, poly_mask(T_HEX))
    s = fill_under(t)
    return s.resize((N * SCALE, N * SCALE), Image.NEAREST)


def build_etch_glint():
    """Loop over the tile: a scribe-spark runs out along each spoke on the beat, and the four side junctions (where
    this hex's lattice meets its neighbours') twinkle together across the whole field. Portrait-clear."""
    fr = []
    for i in range(BEAT):
        f = frame()
        p = pulse(i)
        # visible side runs of the four side spokes brighten with the pulse
        for k in SIDE:
            e = ENDS[k]
            a = lerp(C, e, 0.62)
            seg(f, a, e, ETCH_HOT if p > 0.8 else ETCH_MID, keep=1.0 if p > 0.5 else 0.5)
            seg(f, (a[0], a[1] + 1), (e[0], e[1] + 1), ETCH_DARK, keep=1.0 if p > 0.5 else 0.5)
        # the scribe spark: out along every spoke over the first half beat
        if i < 8:
            t = (i + 1) / 8
            for e in ENDS.values():
                x, y = lerp(C, e, t)
                px(f, x, y, WHITE)
                bx, by = lerp(C, e, max(0.0, t - 0.12))
                px(f, bx, by, ETCH_HOT)
        # junction twinkle: a four-point glint, largest on the beat
        r = 4 if i == 0 else 3 if i in (1, 15) else 2 if i in (2, 14) else 1 if i in (3, 13) else 0
        for k in SIDE:
            x, y = ENDS[k]
            if r:
                px(f, x, y, WHITE)
                for s in range(1, r + 1):
                    col = WHITE if s == 1 else ETCH_HOT
                    for dx, dy in ((s, 0), (-s, 0), (0, s), (0, -s)):
                        px(f, x + dx, y + dy, col)
        fr.append(f)
    # not clipped to the hex: a junction lies on the shared edge, and both neighbours draw the same glint there
    return mind_portrait(fr)


# ------------------------------------------------------------------------------------------------ moe_recast
def blade(f, base, h, w, flash=False):
    """A thin blade of glass rising point-up from `base`: light left face, mid right face, dark outline, gold edge."""
    bx, by = base
    if h < 1:
        return
    for yy in range(int(h) + 1):
        y = by - yy
        half = w * (1 - yy / max(1, h)) / 2
        x0, x1 = bx - half, bx + half
        for x in range(int(math.floor(x0)), int(math.ceil(x1)) + 1):
            if x < x0 - 0.5 or x > x1 + 0.5:
                continue
            col = GLASS_L if x <= bx else GLASS_M
            if flash:
                col = WHITE
            px(f, x, y, col)
        px(f, math.floor(x0) - 1, y, GLASS_D)
        px(f, math.ceil(x1) + 1, y, ETCH_MID if not flash else ETCH_HOT)
    px(f, bx, by - h - 1, GLASS_D)


def build_recast():
    """The Recast: the etched lattice flashes back into view (the mark coming due), glass blades rise along it, peak
    white, and shatter into falling splinters while the lattice cools. 12 frames, one-shot (0.6 s)."""
    sites = [(C, 18, 5)] + [(lerp(C, e, 0.55), 11 if k in SIDE else 8, 3) for k, e in ENDS.items()]
    sites = [((round(p[0]), round(p[1]) + 1), h, w) for p, h, w in sites]
    rise = {1: 0.25, 2: 0.6, 3: 0.9, 4: 1.0}
    frags = []
    for (bx, by), h, w in sites:
        for k in range(4):
            ang = -math.pi / 2 + (k - 1.5) * 0.7 + (0.25 if bx > 25 else -0.25 if bx < 25 else 0)
            sp = 1.6 + 0.35 * k
            frags.append((bx, by - h * (0.35 + 0.18 * k), math.cos(ang) * sp, math.sin(ang) * sp, k % 2))
    fr = []
    for i in range(12):
        f = frame()
        lat = frame()
        if i <= 1:
            etch_lines(lat, ENDS, C, widths=(3, 2, 1), cols=[(ETCH_DARK, ETCH_HOT, WHITE), (ETCH_DARK, WHITE, WHITE)])
        elif i <= 7:
            etch_lines(lat, ENDS, C, widths=(3, 2, 1))
        elif i <= 9:
            for e in ENDS.values():
                seg(lat, C, e, ETCH_DIM, keep=0.5 if i == 8 else 0.25)
        f.alpha_composite(clip(lat, poly_mask(HEX)))
        if i in rise:
            for (bx, by), h, w in sorted(sites, key=lambda s: s[0][1]):
                blade(f, (bx, by), h * rise[i], w, flash=(i == 4))
        if i >= 5:
            t = i - 4
            keep = 1.0 if t < 4 else 0.5 if t < 6 else 0.25
            for x0, y0, vx, vy, light in frags:
                x, y = x0 + vx * t, y0 + vy * t + 0.42 * t * t
                col = (GLASS_L if light else ETCH_MID) if t < 4 else GLASS_M
                px(f, x, y, col, keep)
                px(f, x + (1 if vx >= 0 else -1), y, GLASS_D if t > 2 else col, keep)
        if i == 4:  # the peak: a white rim flash round the hex edge
            for a, b in zip(HEX, HEX[1:] + HEX[:1]):
                seg(f, a, b, WHITE, keep=0.75)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ moe_guard_open

# ------------------------------------------------------------------------------------------------ moe_quiet
def ellipse(f, cx, cy, rx, ry, rgb, n=48, keep=1.0):
    for k in range(n):
        a = 2 * math.pi * k / n
        px(f, cx + math.cos(a) * rx, cy + math.sin(a) * ry, rgb, keep)


def build_quiet():
    """The Quiet: a ring of ink-black stillness closes on the target, a bone-white hush flares at the centre, and the
    dust around it stops in the air. 12 frames, one-shot."""
    cx, cy = 25, 22
    motes = [(cx + math.cos(a) * r, cy + math.sin(a) * r * 0.7) for a, r in
             ((0.3, 11), (1.2, 13), (2.0, 10), (2.9, 12), (3.7, 11), (4.6, 13), (5.4, 10), (6.0, 14))]
    fr = []
    for i in range(12):
        f = frame()
        if i <= 5:
            t = i / 5
            rx, ry = 21 - 17 * t, 13 - 10 * t
            for d in (0, 1, 2):
                ellipse(f, cx, cy, rx + d * 0.6, ry + d * 0.4, INK, n=64)
            ellipse(f, cx, cy, max(1, rx - 1), max(1, ry - 0.8), BONE_S if i < 5 else BONE, n=40, keep=0.6)
        if i in (5, 6, 7):
            r = {5: 4, 6: 6, 7: 3}[i]
            for s in range(-r, r + 1):
                px(f, cx + s, cy, BONE if abs(s) < r else BONE_S)
                px(f, cx, cy + s * 0.7, BONE if abs(s) < r else BONE_S)
            for s in range(-r // 2, r // 2 + 1):
                px(f, cx + s, cy + s * 0.7, BONE_S)
                px(f, cx + s, cy - s * 0.7, BONE_S)
            ellipse(f, cx, cy, r + 2, (r + 2) * 0.6, INK, n=40)
        if i >= 6:
            keep = 1.0 if i < 9 else 0.5 if i < 11 else 0.25
            for mx, my in motes:
                px(f, mx, my, DUST, keep)
                px(f, mx, my + 1, BONE_D, keep)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ moe_lancet

# ------------------------------------------------------------------------------------------------ moe_feeler

# ------------------------------------------------------------------------------------------------ moe_lull

# ------------------------------------------------------------------------------------------------ figures
VIOLET = (96, 66, 150)
VIOLET_D = (44, 30, 72)
AI_DISC = ((25, 17), 16.5)   # an AI avatar: h * 1.6 across at 0.9 h (combatActorParts), in frame px


def figure_mask():
    """A plain standing shinobi silhouette (hood, shoulders, arms at the sides, two legs) on the 50 px grid, feet
    on the hex centre's front edge: about 1.1 hex heights tall, the height of a fighter's marker."""
    m = Image.new('L', (N, N), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([22, 9, 28, 16], fill=255)                                  # hooded head
    d.polygon([(21, 13), (25, 7), (29, 13)], fill=255)                    # hood peak
    d.polygon([(20, 17), (30, 17), (31, 27), (19, 27)], fill=255)        # torso
    d.polygon([(18, 18), (20, 17), (20, 26), (18, 25)], fill=255)        # left arm
    d.polygon([(30, 17), (32, 18), (32, 25), (30, 26)], fill=255)        # right arm
    d.rectangle([21, 27, 24, 34], fill=255)                               # legs
    d.rectangle([26, 27, 29, 34], fill=255)
    return m


FIG = None


def fig_pixels():
    global FIG
    if FIG is None:
        m = figure_mask().load()
        inside = {(x, y) for y in range(N) for x in range(N) if m[x, y]}
        edge = {(x, y) for (x, y) in inside if any((x + dx, y + dy) not in inside
                                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
        FIG = (inside, edge)
    return FIG


# ------------------------------------------------------------------------------------------------ moe_stillness

# ------------------------------------------------------------------------------------------------ moe_breathless
def build_breathless():
    """Breathless Pull: the air is drawn out of the hex. Pale breath-streaks run in from the rim, gather above the
    fighter and stream away upward (toward the one who breathed in; a hex sprite cannot aim at her, so the pull
    reads as up and away), then a small deep-violet lock closes at the feet (the stun) and the dust stops. Plays
    only on hit hexes; the three dry tiles, Where the Three Refused, keep their tg_safe art and never show it.
    12 frames, one-shot."""
    starts = [(6, 25), (44, 25), (12, 33), (38, 33), (12, 17), (38, 17), (25, 36), (19, 36), (31, 36)]
    apex = (25, 4)
    fr = []
    for i in range(12):
        f = frame()
        if i <= 8:
            for k, (sx, sy) in enumerate(starts):
                for j in range(5):                         # a dashed streak: five beads moving along a curve
                    t = (i / 8) * 1.25 - j * 0.07 - (k % 3) * 0.04
                    if not 0 <= t <= 1:
                        continue
                    cx, cy = 25 + (sx - 25) * 0.3, 14
                    x = (1 - t) ** 2 * sx + 2 * (1 - t) * t * cx + t * t * apex[0]
                    y = (1 - t) ** 2 * sy + 2 * (1 - t) * t * cy + t * t * apex[1]
                    kp = 1.0 if j < 3 else 0.5
                    px(f, x, y, WHITE if j == 0 else DUST if j < 3 else GLASS_M, kp)
                    px(f, x + 1, y, CYAN if j < 2 else GLASS_M, kp)      # two pixels wide, cold-edged
                    px(f, x, y + 1, GLASS_D, kp)                        # dark under-edge: reads on a light board
                    px(f, x + 1, y + 1, GLASS_D, kp)
        if 4 <= i <= 8:                                    # the drawn breath leaves at the top
            for k in range(3):
                px(f, 24 + k, 3 - (i - 4) * 0.5, DUST, 0.75)
        if i >= 6:                                         # the lock at the feet
            r = {6: 9, 7: 7, 8: 6}.get(i, 6)
            keep = 1.0 if i < 10 else 0.5
            ellipse(f, 25, 32, r, r * 0.4, VIOLET, n=40, keep=keep)
            ellipse(f, 25, 32.6, r, r * 0.4, VIOLET_D, n=40, keep=keep)
            if i == 6:
                ellipse(f, 25, 32, r + 2, (r + 2) * 0.4, WHITE, n=40, keep=0.5)
        if i >= 7:
            for mx, my in ((15, 20), (36, 18), (19, 9), (32, 27), (13, 28)):
                px(f, mx, my, DUST, 1.0 if i < 10 else 0.5)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ moe_lucid
def build_lucid():
    """Lucid, on Sayo alone: a slow ring of cold skyglass facets turns round her portrait, white on the beat, with
    a cold glint along the lower rim. Two beats (1.6 s); an eighth of a turn per loop so it is seamless. Keeps her
    (AI-sized) portrait clear. Distinct from the Crowned Captain's frost crown: no crown points, no full ring of
    crystal, eight separate facets and open sky between them."""
    period = BEAT * 2
    (pcx, pcy), pr = AI_DISC
    fr = []
    for i in range(period):
        f = frame()
        hot = i in (0, 1, 16, 17)
        for k in range(8):
            ang = 2 * math.pi * (k / 8 + i / (period * 8))
            x, y = round(25 + math.cos(ang) * 21), round(18 + math.sin(ang) * 17)
            for dx, dy, col in ((0, -2, WHITE if hot else CYAN), (-1, -1, GLASS_L), (0, -1, WHITE if hot else GLASS_L),
                                (1, -1, CYAN), (-1, 0, GLASS_L), (0, 0, CYAN), (1, 0, CYAN_D), (0, 1, CYAN_D)):
                px(f, x + dx, y + dy, col)
            for dx, dy in ((0, -3), (-2, -1), (2, -1), (-2, 0), (2, 0), (-1, 1), (1, 1), (0, 2)):
                px(f, x + dx, y + dy, GLASS_D)
        for k in range(-7, 8):                             # the cold rim under her, brightest on the beat
            px(f, 25 + k * 1.6, 36 - abs(k) * 0.25, WHITE if hot and abs(k) < 3 else CYAN, 1.0 if abs(k) < 5 else 0.5)
        fr.append(f)
    mask = Image.new('L', (N, N), 0)
    ImageDraw.Draw(mask).ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], fill=255)
    out = []
    for f in fr:
        a = f.getchannel('A')
        a.paste(0, (0, 0), mask)
        f.putalpha(a)
        out.append(f)
    return out


# ------------------------------------------------------------------------------------------------ moe_likeness

# ------------------------------------------------------------------------------------------------ moe_worn

# ------------------------------------------------------------------------------------------------ moe_cradle
def build_cradle():
    """Cradle (while a feeler lives, the Silence holds Sayo: 90% less damage taken). A static loop on Sayo: pale
    feelers of the Silence rise from the floor beneath her and wind up around her in a braided ring, two lifting
    their tips over her shoulders, over an ink hold that throbs violet on the shared 0.8 s beat. Everything stays
    outside her AI-sized portrait, so she reads clearly as held and the player looks for the feeler to kill.
    16 frames, one beat."""
    (pcx, pcy), pr = AI_DISC
    fr = []

    def outside(x, y):
        return math.hypot(x - pcx, y - pcy) > pr + 0.6

    for i in range(BEAT):
        f = frame()
        p = pulse(i)
        ph = 2 * math.pi * i / BEAT
        # the ink hold: a dark band round the lower two thirds of her portrait, violet on the beat
        for deg in range(150, 391, 2):
            r = math.radians(deg)
            for dr, col, keep in ((1.0, VIOLET if p > 0.55 else VIOLET_D, 1.0), (2.0, INK, 0.75), (3.0, VIOLET_D, 0.25 + 0.5 * p)):
                px(f, pcx + (pr + dr) * math.cos(r), pcy + (pr + dr) * math.sin(r), col, keep)
        # four feelers braid round her: each starts on the floor under her and winds up one side
        for side in (-1, 1):
            for k, off in enumerate((0.0, math.pi)):
                pts = []
                for t in range(0, 61):
                    u = t / 60
                    deg = 90 + side * (u * 128)                      # from straight under her up past the shoulder
                    rr = pr + 3.0 + 1.6 * math.sin(u * 11 + off + ph * (1 if k else -1))
                    if u < 0.12:                                     # the root rises out of the floor
                        rr += (0.12 - u) * 12
                    r = math.radians(deg)
                    pts.append((pcx + rr * math.cos(r), pcy + rr * math.sin(r), u))
                tx, ty, _ = pts[-1]                                  # the tip lifts and hooks over the shoulder
                for j in range(1, 6):
                    a2 = math.radians(j * 30)
                    pts.append((tx - side * 1.4 * math.sin(a2), ty - 1.6 * j * 0.5 - 0.6 * p, 1.0))
                for x, y, u in pts:
                    th = 1.1 * (1 - u) + 0.35
                    for o in (-1, 0, 1):
                        if abs(o) <= th and outside(x + o * 0.0, y + o):
                            px(f, x, y + o, BONE if o <= 0 else BONE_S)
                    if outside(x, y + th + 1):
                        px(f, x, y + th + 1, BONE_D)
        for mx, my in ((5, 6), (45, 9), (3, 44), (47, 46)):
            px(f, mx, my, DUST, 1.0 if (i // 4) % 2 == 0 else 0.5)
        fr.append(f)
    return fr

# ------------------------------------------------------------------------------------------------ moe_flood (signature)




# ------------------------------------------------------------------------------------------------ v2 polish (art QA)
# The CDN delivers every strip at 50 px wide (theninjarpg@3314d122 primitives/animation.ts rendition 50) and pixi
# stretches it ~3.3x with LINEAR filtering (combatEffects.ts never passes nearest): 1 px dithers turn to haze, so the
# v2 builders below use solid clusters of 2-3 px, 1 px dark outlines, and fade by shrinking or dropping whole
# clusters instead of ordered dithering.
ORE = (196, 92, 40)          # ember (the heavy-damage family)
ORE_HOT = (255, 196, 120)


def blob(f, x, y, rgb, r=1):
    """A solid square cluster (2r x 2r px, r=1 -> 2x2)."""
    for dx in range(-r + 1, r + 1):
        for dy in range(-r + 1, r + 1):
            px(f, x + dx, y + dy, rgb)


def outline_alpha(f, rgb):
    """1 px dark outline round every opaque pixel cluster (4-neighbour), drawn under the cluster."""
    a = f.getchannel('A').load()
    pts = [(x, y) for y in range(f.height) for x in range(f.width)
           if not a[x, y] and any(0 <= x + dx < f.width and 0 <= y + dy < f.height and a[x + dx, y + dy]
                                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in pts:
        f.putpixel((x, y), (*rgb, 255))
    return f


def thick_arc(f, cx, cy, r, a0, a1, layers, ry_scale=1.0):
    """An arc from a0 to a1 (degrees) drawn as concentric 1 px rings, layers = [(dr, rgb), ...]."""
    for dr, col in layers:
        rr = r + dr
        n = max(8, int(abs(a1 - a0) / 360 * 2 * math.pi * rr * 3))
        for k in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * k / n)
            px(f, cx + rr * math.cos(a), cy + rr * math.sin(a) * ry_scale, col)


def build_guard_open():
    """Weakness after a Recast, on SAYO (Recast's weakness targets SELF: her guard opens, x3 damage taken). A bold
    ring of etched gold glass round her portrait, cracked into six plates; on the 0.8 s beat the plates push outward
    and flare white along their cut, so the gaps open: punish now. Etching gold/white with near-black score lines
    (the Etching family, so it reads as the mark's payoff, distinct from Lucid's cyan facets). Off her face: every
    pixel sits outside her AI-sized portrait. 16 frames, one beat."""
    (pcx, pcy), pr = AI_DISC
    plates = [(-150, -95), (-85, -30), (-20, 35), (45, 100), (110, 165), (175, 210)]
    fr = []
    for i in range(BEAT):
        f = frame()
        p = pulse(i)
        push = 1.5 * p
        for a0, a1 in plates:
            mid = math.radians((a0 + a1) / 2)
            ox, oy = math.cos(mid) * push, math.sin(mid) * push
            hot = p > 0.7
            thick_arc(f, pcx + ox, pcy + oy, pr + 1.5, a0, a1,
                      [(0.0, SCORE), (1.0, ETCH_HOT if hot else ETCH_MID), (2.0, WHITE if hot else ETCH_HOT),
                       (3.0, ETCH_MID), (4.0, SCORE)])
            # a crack spike off the plate's outer edge
            r0 = pr + 1.5 + 4
            for s in range(3):
                x = pcx + ox + (r0 + s) * math.cos(mid)
                y = pcy + oy + (r0 + s) * math.sin(mid)
                px(f, x, y, ETCH_HOT if hot and s < 2 else SCORE)
        if p > 0.85:  # the beat: white sparks leap from the opened gaps
            for a0, _ in plates:
                g = math.radians(a0 - 2.5)
                for s in (6.5, 8.0):
                    blob(f, pcx + (pr + s) * math.cos(g), pcy + (pr + s) * math.sin(g), WHITE)
        fr.append(f)
    mask = Image.new('L', (N, N), 0)
    ImageDraw.Draw(mask).ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], fill=255)
    out = []
    for f in fr:
        a = f.getchannel('A')
        a.paste(0, (0, 0), mask)
        f.putalpha(a)
        out.append(f)
    return out


def build_lancet():
    """Glass Lancet: a thick skyglass needle with a dark outline streaks in from the upper left (4 frames), strikes
    in a white impact star held 2 frames, then splinters into solid 2 px chips. 11 frames."""
    a, b = (3.0, 2.0), (25.0, 21.0)
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    chips = [(math.cos(t) * s, math.sin(t) * s) for t, s in ((3.5, 2.0), (4.3, 2.3), (5.0, 1.8), (5.7, 2.2), (0.5, 1.7), (2.5, 1.9))]
    fr = []
    for i in range(11):
        f = frame()
        if i <= 3:
            tip = lerp(a, b, (i + 1) / 4)
            n = frame()
            for k in range(11):                                   # body, 3 px wide
                x, y = tip[0] - ux * k, tip[1] - uy * k
                for o in (-1, 0, 1):
                    col = WHITE if (o == 0 and k < 6) else GLASS_L if o <= 0 else CYAN
                    px(n, x - uy * o, y + ux * o, col)
            outline_alpha(n, GLASS_D)
            f.alpha_composite(n)
            for k in range(3):                                    # short cyan trail, solid
                blob(f, tip[0] - ux * (13 + 3 * k), tip[1] - uy * (13 + 3 * k), CYAN if k < 2 else CYAN_D)
        if i in (4, 5, 6):                                        # impact star, held
            r = {4: 9, 5: 8, 6: 5}[i]
            n = frame()
            for s in range(-r, r + 1):
                for o in (0, 1) if abs(s) < r - 1 else (0,):
                    px(n, b[0] + s, b[1] + o, WHITE if abs(s) < r - 2 else CYAN)
                    px(n, b[0] + o, b[1] + s * 0.8, WHITE if abs(s) < r - 2 else CYAN)
            for s in range(-(r // 2), r // 2 + 1):
                px(n, b[0] + s, b[1] + s, GLASS_L)
                px(n, b[0] + s, b[1] - s, GLASS_L)
            outline_alpha(n, GLASS_D)
            f.alpha_composite(n)
        if i >= 6:
            t = i - 5
            for k, (vx, vy) in enumerate(chips):
                if t > 4 and k % 2:
                    continue                                       # fade by dropping whole chips
                x, y = b[0] + vx * t * 1.4, b[1] + vy * t * 1.4 + 0.3 * t * t
                blob(f, x, y, GLASS_L if t < 3 else CYAN)
                px(f, x + 1, y + 1, GLASS_D)
        fr.append(f)
    return fr


def build_lull():
    """The Glass Falls Quiet: the breath between cycles on Sayo (fleeprevent, SELF, 2 rounds). Sixteen 2x2 motes of
    pale glass dust drift down at her sides, each with a dark under-pixel, and two faint 2 px dust curtains hang at
    the frame's edges. Clear of her AI-sized portrait. Two beats (1.6 s), loops seamlessly."""
    period = BEAT * 2
    motes = [(4, 0), (7, 11), (10, 22), (5, 5), (8, 27), (11, 15), (3, 19), (9, 8),
             (46, 3), (43, 19), (40, 9), (45, 27), (42, 14), (47, 23), (39, 1), (44, 30)]
    (pcx, pcy), pr = AI_DISC
    fr = []
    for i in range(period):
        f = frame()
        for x0 in (2, 48):                                        # dust curtains: short solid dashes falling
            for k in range(4):
                y = (i * 1.5 + k * 12) % 44
                for yy in range(3):
                    px(f, x0, y + yy, GLASS_M)
                    px(f, x0 + (1 if x0 < 25 else -1), y + yy, DUST)
        for x0, t0 in motes:
            k = (i + t0) % period
            y = 2 + k * 1.3
            x = x0 + (1 if (k // 8) % 2 else 0)
            if math.hypot(x - pcx, y - pcy) <= pr + 2:
                continue
            blob(f, x, y, DUST)
            px(f, x, y + 1, GLASS_D)
            px(f, x + 1, y + 1, GLASS_D)
        fr.append(f)
    return fr


def build_stillness():
    """Nothing Moves (the control mark comes due as a stun): a solid ring of ink closes in from the hex rim over the
    stunned fighter, its inner edge a crisp 1 px deep violet, and the dust stops in 2x2 motes; then the ring lets go
    by thinning, never dithering. 12 frames, one-shot."""
    motes = [(14, 12), (35, 10), (11, 22), (39, 20), (18, 30), (33, 31), (25, 6), (29, 18), (20, 19)]
    cx, cy, RX, RY = 25, 22, 22, 14
    fr = []
    for i in range(12):
        f = frame()
        if i <= 10:
            close = min(1.0, (i + 1) / 6)
            release = 0.0 if i < 8 else (i - 7) / 3.5
            inner = 1.0 - 0.66 * close + 0.6 * release
            outer = 1.0 - 0.25 * release
            for y in range(N):
                for x in range(N):
                    r = math.hypot((x - cx) / RX, (y - cy) / RY)
                    if inner <= r <= outer:
                        px(f, x, y, INK if r > inner + 0.06 else VIOLET)
                    elif outer < r <= outer + 0.05:
                        px(f, x, y, VIOLET_D)
        if i >= 3:
            for k, (mx, my) in enumerate(motes):
                if i >= 10 and k % 2:
                    continue
                blob(f, mx, my, WHITE if i in (5, 6) else DUST)
        fr.append(f)
    return fr


def build_likeness():
    """Your Likeness (summon flourish): the summoned avatar is already on screen, so this frames it. A ring of
    silvered glass closes round its portrait, flashes white, cracks, and bursts outward into solid 2-3 px shards.
    14 frames, one-shot."""
    (pcx, pcy), pr = AI_DISC
    shards = [(a, 1.6 + 0.4 * (k % 3)) for k, a in enumerate(range(0, 360, 30))]
    fr = []
    for i in range(14):
        f = frame()
        if i <= 5:
            r = pr + 9 - 7 * min(1.0, i / 4)
            thick_arc(f, pcx, pcy, r, 0, 360, [(0.0, GLASS_D), (1.0, WHITE if i == 5 else GLASS_L), (2.0, GLASS_M), (3.0, GLASS_D)])
            if i >= 4:                                             # cracks run across the ring
                for a in range(15, 360, 60):
                    g = math.radians(a)
                    for s in range(5):
                        px(f, pcx + (r - 1 + s) * math.cos(g), pcy + (r - 1 + s) * math.sin(g), GLASS_D)
        if i >= 6:
            t = i - 5
            for k, (a, sp) in enumerate(shards):
                if t > 6 and k % 2:
                    continue
                g = math.radians(a + 8 * t)
                rr = pr + 2 + sp * t * 1.6
                x, y = pcx + rr * math.cos(g), pcy + rr * math.sin(g) + 0.25 * t * t
                n = frame()
                blob(n, x, y, GLASS_L if k % 3 else WHITE)
                px(n, x + 1, y - 1, CYAN)
                outline_alpha(n, GLASS_D)
                f.alpha_composite(n)
        fr.append(f)
    mask = Image.new('L', (N, N), 0)
    ImageDraw.Draw(mask).ellipse([pcx - pr + 3, pcy - pr + 3, pcx + pr - 3, pcy + pr - 3], fill=255)
    out = []
    for f in fr:
        a = f.getchannel('A')
        a.paste(0, (0, 0), mask)
        f.putalpha(a)
        out.append(f)
    return out


def build_worn():
    """The Worn (summon flourish): an upwell of grey-brown ash out of the glass round the summoned avatar's feet:
    solid 2x2 clumps boil up from the floor ring and rise along its sides, thinning as they climb. 14 frames."""
    (pcx, pcy), pr = AI_DISC
    ASH, ASH_D, ASH_L = (128, 118, 112), (58, 52, 56), (186, 178, 168)
    rng = [((k * 37) % 23 - 11, (k * 53) % 7, (k * 29) % 5) for k in range(26)]
    fr = []
    for i in range(14):
        f = frame()
        if i <= 6:                                                 # the floor ring the ash breaks through
            rx = 8 + i * 2
            n = frame()
            ellipse(n, 25, 37, rx, rx * 0.32, ASH_L if i < 3 else ASH, n=200)
            ellipse(n, 25, 37.8, rx, rx * 0.32, ASH_D, n=200)
            ellipse(n, 25, 38.6, rx, rx * 0.32, ASH_D, n=200)
            f.alpha_composite(n)
        for k, (xo, d0, sp) in enumerate(rng):
            t = i - d0 * 0.6
            if t < 0:
                continue
            y = 38 - t * (1.6 + sp * 0.3)
            side = -1 if xo < 0 else 1
            x = 25 + xo * 1.5 + side * max(0, (34 - y)) * 0.45
            if y < 4 or (i > 10 and k % 2):
                continue
            if math.hypot(x - pcx, y - pcy) < pr - 2:
                x = pcx + side * (pr + 1)                           # keep the face clear: rise along the sides
            col = ASH_L if t < 3 else ASH if t < 7 else ASH_D
            n2 = frame()
            blob(n2, x, y, col, r=2 if t < 5 else 1)
            outline_alpha(n2, ASH_D)
            f.alpha_composite(n2)
        fr.append(f)
    return fr


def build_feeler():
    """The Listening (summon flourish): an ink ripple spreads at the summoned feeler's root and pale bone wisps curl
    up beside it and drop away. Frames the avatar instead of drawing a second feeler. 14 frames, one-shot."""
    fr = []
    for i in range(14):
        f = frame()
        if i <= 9:                                                 # ink ripples
            for j, d in enumerate((0, 3)):
                t = i - d
                if 0 <= t <= 6:
                    rx = 5 + t * 2.4
                    ellipse(f, 25, 37, rx, rx * 0.33, INK, n=200)
                    ellipse(f, 25, 37.8, rx, rx * 0.33, VIOLET if t < 4 else INK, n=200)
                    ellipse(f, 25, 38.6, rx, rx * 0.33, INK, n=200)
        for side in (-1, 1):                                       # two wisps either side
            for w, x0 in enumerate((14, 9)):
                t = i - 2 - w * 2
                if t < 0 or t > 10:
                    continue
                h = min(14, t * 2.5)
                for s in range(int(h)):
                    y = 37 - s
                    x = 25 + side * (x0 + 2 * math.sin(s / 3 + t * 0.4))
                    if t > 7 and s < (t - 7) * 4:
                        continue                                   # it drops away from the root up
                    px(f, x, y, BONE)
                    px(f, x + side, y, BONE_S)
                    px(f, x - side, y, BONE_D)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ moe_flood
# Not built (art QA, 2026-11-04): the director's ME28 faces could not hold up at the 50 px CDN rendition (v1 drawn at
# 150 px lost two-thirds of its detail; 50 px rebuilds read as blank tiles and stacked into columns across a field).
# The Names Flood In keeps the reuse-live Eruption strip (Z9j8J7ZmAjiaxH2S4nDy8, the doc's P1 source).


# ------------------------------------------------------------------------------------------------ moe_flood (mask)
MASK_KEYS = os.path.join(ROOT, 'art', 'mother_of_echoes', 'raw', 'fx_flood_mask_keys.png')   # director, 3 keyframes


def mask_keys():
    """The director's three lime-keyed keyframes (whole, cracked, burst), each cropped and fitted to the 50 px grid
    at 38 px tall with hard alpha, colours kept flat (the source is already 5 flat colours)."""
    src = Image.open(MASK_KEYS).convert('RGBA')
    px_ = src.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px_[x, y]
            if g > 170 and r < 110 and b < 110:
                px_[x, y] = (0, 0, 0, 0)
    w3 = src.width // 3
    out = []
    for k in range(3):
        part = src.crop((k * w3, 0, (k + 1) * w3, src.height))
        part = part.crop(part.getbbox())
        h = 38 if k < 2 else 44
        part = part.resize((max(1, round(part.width * h / part.height)), h), Image.BOX)
        a = part.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
        part.putalpha(a)
        out.append(part)
    return out


def build_flood_mask():
    """The Names Flood In (heavy payoff): one great glass mask rises out of the hex, holds, its eyes snap open as
    ember cracks split it with a white flash, then it bursts into chunky shards that fly apart. 14 frames, one-shot.
    The director's keyframes are drawn for the 50 px delivery (bold outline, 5 flat colours)."""
    whole, cracked, burst = mask_keys()
    fr = []

    def put(img, scale=1.0, dy=0, flash=False):
        f = frame()
        im = img
        if scale != 1.0:
            im = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.NEAREST)
        if flash:  # whiten the fill, keep the dark outline so the silhouette holds
            im = im.copy()
            q = im.load()
            for y in range(im.height):
                for x in range(im.width):
                    r, g, b, al = q[x, y]
                    if al and r + g + b > 150:
                        q[x, y] = (min(255, r + (255 - r) * 3 // 5), min(255, g + (255 - g) * 3 // 5),
                                   min(255, b + (255 - b) * 3 // 5), al)
        f.alpha_composite(im, ((N - im.width) // 2, (N - im.height) // 2 + 2 + dy))
        return f

    for sc, dy in ((0.55, 8), (0.8, 4), (1.0, 0)):      # rises and swells out of the floor
        fr.append(put(whole, sc, dy))
    fr += [put(whole), put(whole)]                     # holds: the calm before
    fr.append(put(cracked, flash=True))                # the eyes open, white flash
    fr += [put(cracked), put(cracked)]                 # cracks burn
    fr.append(put(burst, 0.9, flash=True))             # it bursts
    for sc in (1.0, 1.08, 1.14):                       # shards fly apart
        fr.append(put(burst, sc))
    shards = put(burst, 1.18)                          # last frame: shards only, the star gone
    a = shards.getchannel('A').load()
    p_ = shards.load()
    for y in range(N):
        for x in range(N):
            r, g, b, al = p_[x, y]
            if al and r - b > 30:                       # drop the ember star and its cream core
                p_[x, y] = (0, 0, 0, 0)
    fr.append(shards)
    fr.append(frame())
    return fr


# ================================================================================================================
# Custom set (director, 2026-11-05: "we're borrowing a lot of animations from elsewhere in the event instead of
# making our own"). Every Mother of Echoes slot that borrowed a live Skyglass/library strip gets its own, drawn in
# Sayo's glass look but keeping the event's danger GRAMMAR (docs/design/SKYGLASS_BOSS_ANIMATIONS.md readability
# rules): heavy = ember ring with cracks, control = violet links in a ring, linger = bile seep, safe = cyan
# four-point star in a diamond; shape carries the meaning, colour confirms it. Here the ring is cracked glass, the
# links are faceted violet glass, the seep wells through crazed glass, the safe diamond is a cut glass pane.
# All on the 50 px grid in solid clusters (the CDN 50 px rendition + pixi's linear stretch), 1 px dark outlines.
# ================================================================================================================
EMBER_D = (92, 30, 18)
EMBER_DEEP = (34, 14, 14)
EMBER_RED = (214, 58, 26)
EMBER_YEL = (255, 206, 84)
BILE = (150, 186, 40)
BILE_HOT = (214, 238, 104)
BILE_D = (52, 70, 14)
BILE_DEEP = (22, 30, 10)
VIOLET_L = (176, 140, 232)
VIOLET_M = (128, 92, 196)
CYAN_L = (206, 244, 252)
ASH = (128, 118, 112)
ASH_D = (58, 52, 56)
ASH_L = (186, 178, 168)
TC = (25, 25)          # tile-space centre (the 50 px STATIC is stretched to the hex box, 2:1)
GC, GRX, GRY = (25, 25), 19.0, 9.5     # the hex's ground ellipse in animation-frame px


def disc_mask(cx, cy, r, ry=None):
    m = Image.new('L', (N, N), 0)
    ry = r if ry is None else ry
    ImageDraw.Draw(m).ellipse([cx - r, cy - ry, cx + r, cy + ry], fill=255)
    return m


def tile_out(t):
    """Tile export: RGB filled under transparency, delivered x3 nearest (150 px), like tile_moe_etch."""
    return fill_under(t).resize((N * SCALE, N * SCALE), Image.NEAREST)


def jag(cx, cy, r0, r1, a, wob, steps=7):
    """A jagged crack polyline from radius r0 to r1 along angle a (degrees), deterministic zig-zag."""
    pts = []
    for k in range(steps + 1):
        t = k / steps
        r = r0 + (r1 - r0) * t
        g = math.radians(a + (wob if k % 2 else -wob) * (0.3 + t))
        pts.append((cx + r * math.cos(g), cy + r * math.sin(g)))
    return pts


# ------------------------------------------------------------------------------------------------ heavy (tile + loop)
HEAVY_CRACKS = (15, 82, 150, 214, 286, 340)


def build_tile_heavy():
    """Heavy: the Skyglass heavy silhouette (a bright ember ring round a near-black ground, thin jagged cracks) cut
    as glass: the ring is a ten-sided band of red-to-yellow facets split by dark seams, white sheen on its upper-left
    plates, and four thin jagged cracks with white-hot cores run from the rim to a small smouldering core."""
    t = frame()
    d = ImageDraw.Draw(t)
    poly = lambda r, rot=18: [(25 + r * math.cos(math.radians(k * 36 + rot)), 25 + r * math.sin(math.radians(k * 36 + rot))) for k in range(10)]
    d.polygon(poly(24.6), fill=(*SCORE, 255))
    d.polygon(poly(23.2), fill=(*EMBER_RED, 255))
    d.polygon(poly(21.2), fill=(*EMBER_YEL, 255))
    d.polygon(poly(19.6), fill=(*EMBER_RED, 255))
    d.polygon(poly(18), fill=(*SCORE, 255))
    d.polygon(poly(17), fill=(*EMBER_DEEP, 255))
    for k in range(10):                                          # facet seams
        g = math.radians(k * 36 + 18)
        d.line([(25 + 17.5 * math.cos(g), 25 + 17.5 * math.sin(g)), (25 + 24 * math.cos(g), 25 + 24 * math.sin(g))], fill=(*SCORE, 255), width=1)
    for k in (5, 6):                                             # sheen on the upper-left plates
        g = math.radians(k * 36 + 36)
        blob(t, 25 + 21.5 * math.cos(g), 25 + 21.5 * math.sin(g), WHITE)
    for a, wob in ((30, 16), (128, 13), (212, 17), (300, 14)):    # four thin jagged cracks
        pts = jag(25, 25, 4.5, 18, a, wob, steps=5)
        d.line(pts, fill=(*EMBER_RED, 255), width=2)
        d.line(pts[1:4], fill=(*EMBER_YEL, 255), width=1)
    d.ellipse([20, 20, 30, 30], fill=(*SCORE, 255))
    d.ellipse([21.5, 21.5, 28.5, 28.5], fill=(*EMBER_RED, 255))
    d.ellipse([23, 23, 27, 27], fill=(*EMBER_YEL, 255))
    d.rectangle([24, 24, 26, 26], fill=(*WHITE, 255))
    return tile_out(t)


def side_mask():
    """Loops sit over the actors: keep them to the hex's left and right ends (the portrait-clear junctions)."""
    m = Image.new('L', (N, N), 255)
    return m


def build_heavy_glint():
    """Heavy loop: ember flares run along the ring at the hex's left and right ends and embers lift off them, the
    whole field pulsing on the shared 0.8 s beat. Portrait-clear."""
    fr = []
    for i in range(BEAT):
        f = frame()
        p = pulse(i)
        hot = p > 0.6
        for side in (-1, 1):
            for k in range(7):                                  # the ring's end arc, thick
                a = math.radians((180 if side < 0 else 0) + (k - 3) * 9)
                x, y = GC[0] + (GRX - 1) * math.cos(a), GC[1] + (GRY - 0.5) * math.sin(a)
                blob(f, x, y, ORE_HOT if hot else ORE)
                px(f, x, y + 1.5, EMBER_D)
            for k, (dx, h0) in enumerate(((2, 0), (5, 5), (0, 9))):   # embers lifting
                y = GC[1] - 2 - ((i + h0) % BEAT) * 0.9
                x = GC[0] + side * (GRX - 3 + dx * 0.6)
                if y > 5:
                    blob(f, x, y, ORE_HOT if (i + h0) % BEAT < 6 else ORE, r=1)
        if i == 0:
            for side in (-1, 1):
                blob(f, GC[0] + side * (GRX - 1), GC[1], WHITE, r=2)
        fr.append(f)
    return mind_portrait(fr)


# ------------------------------------------------------------------------------------------------ control (hush)
def build_tile_control():
    """Control/lock: the Skyglass control silhouette (a bright violet chain ring) as fourteen faceted violet glass
    links, alternating solid and open, round an ink ground with a closed glass eye (the hush) at the centre."""
    t = frame()
    d = ImageDraw.Draw(t)
    d.ellipse([0.5, 0.5, 49.5, 49.5], fill=(*INK, 255))
    d.ellipse([12, 12, 38, 38], fill=(*VIOLET_D, 255))
    n = 14
    for k in range(n):
        g = math.radians(k * 360 / n)
        cx, cy = 25 + 19.2 * math.cos(g), 25 + 19.2 * math.sin(g)
        tang = g + math.pi / 2
        ux, uy, vx, vy = math.cos(tang), math.sin(tang), math.cos(g), math.sin(g)
        L, W = (4.6, 3.2) if k % 2 == 0 else (4.6, 2.0)
        corners = [(cx + ux * L + vx * W, cy + uy * L + vy * W), (cx - ux * L + vx * W, cy - uy * L + vy * W),
                   (cx - ux * L - vx * W, cy - uy * L - vy * W), (cx + ux * L - vx * W, cy + uy * L - vy * W)]
        d.polygon(corners, fill=(*VIOLET_L, 255), outline=(*INK, 255))
        inner = [(cx + (x - cx) * 0.5, cy + (y - cy) * 0.5) for x, y in corners]
        d.polygon(inner, fill=(*(INK if k % 2 == 0 else VIOLET_M), 255))
    for k in range(0, n, 2):                                     # glass glints on the solid links, upper-left lit
        g = math.radians(k * 360 / n)
        if math.cos(g) + math.sin(g) < 0:
            blob(t, 25 + 20.5 * math.cos(g), 25 + 20.5 * math.sin(g), WHITE, r=1)
    # the closed eye
    d.polygon([(13, 25), (19, 19), (31, 19), (37, 25), (31, 31), (19, 31)], fill=(*VIOLET_M, 255), outline=(*INK, 255))
    d.polygon([(16, 25), (20, 21.5), (30, 21.5), (34, 25), (30, 28.5), (20, 28.5)], fill=(*VIOLET_L, 255))
    d.line([(14, 25), (36, 25)], fill=(*INK, 255), width=3)
    for x in (18, 22, 26, 30, 33):
        d.line([(x, 27), (x - 1, 30)], fill=(*INK, 255), width=1)
    return tile_out(clip(t, disc_mask(25, 25, 24.8)))


def build_control_glint():
    """Control loop: a violet glint runs round the links and the link ends tighten on the beat at the hex's sides.
    Portrait-clear."""
    fr = []
    for i in range(BEAT):
        f = frame()
        p = pulse(i)
        for side in (-1, 1):
            for k in range(3):
                a = math.radians((180 if side < 0 else 0) + (k - 1) * 14)
                x, y = GC[0] + (GRX - 1.5 - p) * math.cos(a), GC[1] + (GRY - 1) * math.sin(a)
                blob(f, x, y, VIOLET_L if p > 0.6 else VIOLET_M)
                px(f, x + side, y, INK)
        k = i % BEAT                                            # the travelling glint
        a = math.radians(180 + k * (360 / BEAT))
        x, y = GC[0] + (GRX - 1) * math.cos(a), GC[1] + (GRY - 0.5) * math.sin(a)
        blob(f, x, y, WHITE)
        fr.append(f)
    return mind_portrait(fr)


# ------------------------------------------------------------------------------------------------ linger
def build_tile_linger():
    """Lingering: the Skyglass seep silhouette (an irregular bile blotch with dark gaps) as bile welling up through
    crazed glass: overlapping lumps, a web of bright cracks, bubbles."""
    t = frame()
    d = ImageDraw.Draw(t)
    lumps = [(25, 25, 15), (14, 18, 8), (36, 17, 8), (39, 31, 8), (13, 33, 8), (25, 39, 8), (25, 10, 7), (8, 25, 6), (42, 24, 6)]
    for x, y, r in lumps:
        d.ellipse([x - r - 1.5, y - r - 1.5, x + r + 1.5, y + r + 1.5], fill=(*BILE_DEEP, 255))
    for x, y, r in lumps:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(96, 124, 26, 255))
    for x, y, r in lumps[:6]:
        d.ellipse([x - r * 0.55, y - r * 0.55, x + r * 0.55, y + r * 0.55], fill=(*BILE_DEEP, 255))
    for a in (20, 80, 140, 200, 260, 320):
        pts = jag(25, 25, 2, 21, a, 13, steps=6)
        d.line(pts, fill=(*BILE, 255), width=2)
        d.line(pts[:3], fill=(*BILE_HOT, 255), width=1)
    for x, y in ((17, 18), (33, 15), (37, 32), (17, 34), (26, 26), (9, 24), (41, 22), (25, 40)):
        blob(t, x, y, BILE_HOT)
        px(t, x - 1, y - 1, WHITE)
    return tile_out(clip(t, disc_mask(25, 25, 24.5)))


def build_linger_glint():
    """Linger loop: bubbles swell and pop at the pool's left and right ends; 1.2 s (24 frames). Portrait-clear."""
    fr = []
    for i in range(24):
        f = frame()
        for side, ph in ((-1, 0), (1, 12)):
            t = (i + ph) % 24
            x = GC[0] + side * (GRX - 4)
            y = GC[1] + 1
            if t < 10:
                r = 1 + t // 4
                n = frame()
                ellipse(n, x, y - t * 0.3, r + 0.5, r * 0.8 + 0.5, BILE, n=40)
                blob(n, x - 1, y - t * 0.3 - r * 0.5, BILE_HOT)
                outline_alpha(n, BILE_DEEP)
                f.alpha_composite(n)
            elif t < 13:
                for dx, dy in ((-2, -2), (2, -2), (0, -4)):
                    blob(f, x + dx * (t - 9), y - 3 + dy * (t - 9) * 0.6, BILE_HOT)
        fr.append(f)
    return mind_portrait(fr)


# ------------------------------------------------------------------------------------------------ safe
def build_tile_safe():
    """Safe: a cut-glass diamond pane in Skyglass cyan with a white four-point star rising from its centre: the
    Skyglass safe silhouette, the most inviting thing on the board."""
    t = frame()
    d = ImageDraw.Draw(t)
    dia = [(25, 1), (49, 25), (25, 49), (1, 25)]
    d.polygon(dia, fill=(*GLASS_D, 255))
    d.polygon([(25, 4), (46, 25), (25, 46), (4, 25)], fill=(*CYAN_D, 255))
    d.polygon([(25, 7), (43, 25), (25, 43), (7, 25)], fill=(*CYAN, 255))
    # facets: light upper-left faces, mid lower-right
    d.polygon([(25, 7), (7, 25), (25, 25)], fill=(*CYAN_L, 255))
    d.polygon([(25, 43), (43, 25), (25, 25)], fill=(*CYAN_D, 255))
    d.polygon([(25, 12), (38, 25), (25, 38), (12, 25)], fill=(*CYAN_D, 255))
    d.polygon([(25, 14), (36, 25), (25, 36), (14, 25)], fill=(*CYAN, 255))
    # the star
    star = [(25, 9), (28, 22), (41, 25), (28, 28), (25, 41), (22, 28), (9, 25), (22, 22)]
    d.polygon(star, fill=(*GLASS_D, 255))
    star_in = [(25, 11), (27.2, 22.8), (39, 25), (27.2, 27.2), (25, 39), (22.8, 27.2), (11, 25), (22.8, 22.8)]
    d.polygon(star_in, fill=(*WHITE, 255))
    d.line([(25, 12), (25, 38)], fill=(*CYAN_L, 255))
    d.rectangle([24, 24, 26, 26], fill=(*WHITE, 255))
    return tile_out(t)


def build_safe_glint():
    """Safe loop: calm light rising at the diamond's left and right points and a soft star twinkle there, 1.6 s
    (32 frames). Portrait-clear."""
    fr = []
    for i in range(32):
        f = frame()
        for side, ph in ((-1, 0), (1, 16)):
            t = (i + ph) % 32
            x = GC[0] + side * (GRX - 2)
            for k in range(3):
                y = GC[1] - ((t + k * 10) % 32) * 0.7
                if y > 6:
                    blob(f, x + (k - 1) * 2 * side, y, CYAN_L if k == 1 else CYAN)
            r = 3 if t == 0 else 2 if t in (1, 31) else 1 if t in (2, 30) else 0
            if r:
                for s in range(1, r + 1):
                    for dx, dy in ((s, 0), (-s, 0), (0, s), (0, -s)):
                        px(f, x + dx, GC[1] + dy, WHITE)
                px(f, x, GC[1], WHITE)
        fr.append(f)
    return mind_portrait(fr)


# ------------------------------------------------------------------------------------------------ mark appear / vanish
def ground_ring(f, rx, ry, layers, cx=25, cy=25, a0=0, a1=360):
    for dr, col in layers:
        n = max(16, int(abs(a1 - a0) / 360 * 2 * math.pi * max(rx, ry) * 3))
        for k in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * k / n)
            px(f, cx + (rx + dr) * math.cos(a), cy + (ry + dr * 0.5) * math.sin(a), col)


def build_heavy_appear():
    """Heavy mark arrives: a white-hot ring slams down a little wider than the hex and contracts onto the mark's rim,
    then ember sparks kick up off the rim and fall back (the tile under it holds the mark). 10 frames, one-shot."""
    fr = []
    sparks = [(k * 45 + 20, 1.0 + 0.3 * (k % 3)) for k in range(8)]
    for i in range(10):
        f = frame()
        if i <= 3:
            s = {0: 1.35, 1: 1.18, 2: 1.05, 3: 1.0}[i]
            rx, ry = (GRX - 1) * s, (GRY - 0.5) * s
            ground_ring(f, rx, ry, [(0, WHITE), (1, EMBER_YEL), (-1, EMBER_YEL), (2, EMBER_RED), (-2, EMBER_RED)] if i < 3
                        else [(0, EMBER_YEL), (1, EMBER_RED), (-1, EMBER_RED)])
        if 3 <= i <= 9:
            t = i - 2
            for k, (a, sp) in enumerate(sparks):
                if t > 5 and k % 2:
                    continue
                g = math.radians(a)
                x0, y0 = 25 + (GRX - 1) * math.cos(g), 25 + (GRY - 0.5) * math.sin(g)
                x, y = x0 + math.cos(g) * t * 0.9, y0 - sp * t * 2.4 + 0.45 * t * t
                n = frame()
                blob(n, x, y, WHITE if t < 2 else EMBER_YEL if t < 4 else EMBER_RED)
                outline_alpha(n, SCORE)
                f.alpha_composite(n)
        fr.append(f)
    return fr


def build_heavy_vanish():
    """Heavy mark clears (spawned as its own visual when the mark expires): the ring gives one last dull glow, cracks
    apart into ember chips and they rise as ash. 8 frames."""
    fr = []
    for i in range(8):
        f = frame()
        if i <= 1:
            ground_ring(f, GRX - 1, GRY - 0.5, [(0, EMBER_RED), (1, EMBER_D)])
        if i >= 1:
            t = i - 1
            for k in range(10):
                if t > 3 and k % 2:
                    continue
                g = math.radians(k * 36 + 10)
                x, y = 25 + (GRX - 1) * math.cos(g), 25 + (GRY - 0.5) * math.sin(g) - t * 2.2
                n = frame()
                blob(n, x, y, EMBER_RED if t < 2 else ASH_L if t < 4 else ASH)
                outline_alpha(n, ASH_D)
                f.alpha_composite(n)
        fr.append(f)
    return fr


def build_control_appear():
    """Control mark arrives: violet glass links whip round the ring from the left and snap shut with an ink flash.
    9 frames, one-shot."""
    fr = []
    for i in range(9):
        f = frame()
        if i <= 4:
            span = 72 * (i + 1)
            for k in range(0, span, 24):
                a = math.radians(180 + k)
                x, y = 25 + (GRX - 1) * math.cos(a), 25 + (GRY - 0.5) * math.sin(a)
                n = frame()
                blob(n, x, y, VIOLET_L if k > span - 30 else VIOLET_M)
                px(n, x + 1, y, VIOLET)
                outline_alpha(n, INK)
                f.alpha_composite(n)
        if 5 <= i <= 6:
            ground_ring(f, GRX - 2, GRY - 1, [(0, WHITE if i == 5 else VIOLET_L), (1, VIOLET_M), (-1, VIOLET_M), (2, INK), (-2, INK)])
        if 7 <= i <= 8:
            ground_ring(f, GRX - 2, GRY - 1, [(0, VIOLET_M), (1, INK)])
        fr.append(f)
    return fr


def build_control_vanish():
    """Control mark clears: the links unclasp and drop as ink. 8 frames."""
    fr = []
    for i in range(8):
        f = frame()
        for k in range(10):
            if i > 3 and k % 2:
                continue
            a = math.radians(k * 36)
            x = 25 + (GRX - 1 + i * 0.8) * math.cos(a)
            y = 25 + (GRY - 0.5 + i * 0.3) * math.sin(a) + i * 0.8
            blob(f, x, y, VIOLET_M if i < 3 else VIOLET if i < 6 else VIOLET_D)
        fr.append(f)
    return fr


def build_safe_appear():
    """Safe mark arrives: a cyan beam rises from the hex, the star opens out of it white, the diamond rim draws.
    10 frames, one-shot."""
    fr = []
    dia = [(25, 25 - GRY + 0.5), (25 + GRX - 1, 25), (25, 25 + GRY - 0.5), (25 - GRX + 1, 25)]
    for i in range(10):
        f = frame()
        if i <= 4:
            h = 6 + i * 6
            for y in range(int(25 - h), 26):
                px(f, 24, y, CYAN_L)
                px(f, 25, y, WHITE)
                px(f, 26, y, CYAN)
        if 2 <= i <= 7:
            r = min(7, 2 + (i - 2) * 2)
            n = frame()
            for s in range(-r, r + 1):
                px(n, 25 + s, 25 - 8, WHITE if abs(s) < r - 1 else CYAN)
                px(n, 25, 25 - 8 + s, WHITE if abs(s) < r - 1 else CYAN)
            outline_alpha(n, CYAN_D)
            f.alpha_composite(n)
        if i >= 3:
            for a, b in zip(dia, dia[1:] + dia[:1]):
                seg(f, a, b, WHITE if i in (3, 4) else CYAN, keep=1.0 if i < 9 else 0.5)
        fr.append(f)
    return fr


def build_safe_vanish():
    """Safe mark clears: the star lifts away and the diamond rim dims out. 8 frames."""
    fr = []
    dia = [(25, 25 - GRY + 0.5), (25 + GRX - 1, 25), (25, 25 + GRY - 0.5), (25 - GRX + 1, 25)]
    for i in range(8):
        f = frame()
        if i < 6:
            y = 17 - i * 2.5
            r = 4 - i // 2
            for s in range(-r, r + 1):
                px(f, 25 + s, y, CYAN_L)
                px(f, 25, y + s, CYAN_L)
            blob(f, 25, y, WHITE)
        if i < 5:
            for a, b in zip(dia, dia[1:] + dia[:1]):
                seg(f, a, b, CYAN if i < 3 else CYAN_D)
        fr.append(f)
    return fr


def build_etch_appear():
    """Etching mark arrives: a white scribe spark cuts the lattice out from the centre along its six spokes, the cut
    flares gold, then settles (the tile holds the mark). 9 frames, one-shot."""
    fr = []
    for i in range(9):
        f = frame()
        t = min(1.0, (i + 1) / 5)
        for e in ENDS.values():
            b = lerp(C, e, t)
            seg(f, C, b, ETCH_HOT if i < 5 else ETCH_MID)
            seg(f, (C[0], C[1] + 1), (b[0], b[1] + 1), SCORE)
            if i < 5:
                blob(f, b[0], b[1], WHITE)
        if i in (5, 6):
            for e in ENDS.values():
                seg(f, C, e, WHITE)
            blob(f, 25, 25, WHITE, r=2)
        if i >= 7:
            fr.append(clip(f, poly_mask(HEX)))
            continue
        fr.append(clip(f, poly_mask(HEX)) if i >= 5 else f)
    return fr


def build_etch_vanish():
    """Etching mark clears: the lattice cools from gold to dark score and fades, spoke by spoke. 8 frames."""
    fr = []
    for i in range(8):
        f = frame()
        for k, e in enumerate(ENDS.values()):
            if k < i - 1:
                continue
            seg(f, C, e, ETCH_MID if i < 3 else ETCH_DIM if i < 6 else ETCH_DARK)
        fr.append(clip(f, poly_mask(HEX)))
    return fr


def build_linger_appear():
    """Lingering pool arrives (as the Skyglass seep erupting into its pool): the glass cracks, a bile splash heaves
    up out of the centre in fat outlined globs and slaps back down across the pool. 10 frames."""
    fr = []
    globs = [(-9, 2.2, 3), (9, 2.2, 3), (-4, 3.2, 2), (4, 3.0, 2), (0, 3.8, 3), (-14, 1.4, 2), (14, 1.4, 2)]
    for i in range(10):
        f = frame()
        if i <= 2:
            for a in (20, 80, 140, 200, 260, 320):
                g = math.radians(a)
                r = (i + 1) / 3
                seg(f, (25, 25), (25 + (GRX - 2) * r * math.cos(g), 25 + (GRY - 1) * r * math.sin(g)), BILE_HOT)
        if 2 <= i <= 9:
            t = i - 1
            for k, (dx, up, r) in enumerate(globs):
                if t > 6 and k % 2:
                    continue
                x = 25 + dx * min(1.0, t / 3)
                y = 25 - up * t * 2.2 + 0.75 * t * t
                if y > 27:
                    y = 27
                n = frame()
                ImageDraw.Draw(n).ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=(*BILE, 255))
                blob(n, x - r * 0.4, y - r * 0.4, BILE_HOT)
                outline_alpha(n, BILE_DEEP)
                f.alpha_composite(n)
        fr.append(f)
    return fr


def shard_poly(f, cx, cy, h, w, tilt=0.0, hot=False, outline=True):
    """A glass shard, point up: light left face, mid right face, ember (or white) edge, dark outline."""
    n = frame()
    d = ImageDraw.Draw(n)
    tip = (cx + tilt * h, cy - h)
    left, right = (cx - w / 2, cy), (cx + w / 2, cy)
    mid = (cx + tilt * h * 0.5, cy - h * 0.15)
    d.polygon([left, tip, mid], fill=(*(WHITE if hot else GLASS_L), 255))
    d.polygon([mid, tip, right], fill=(*(ORE_HOT if hot else GLASS_M), 255))
    d.line([tip, right], fill=(*ORE_HOT, 255))
    if outline:
        outline_alpha(n, SCORE)
    f.alpha_composite(n)


def burst_chunks(f, cx, cy, t, n=8, sp=2.2, cols=(GLASS_L, ORE_HOT, GLASS_M), grav=0.35, drop=0):
    for k in range(n):
        if drop and t > drop and k % 2:
            continue
        a = math.radians(-160 + k * (140 / max(1, n - 1)))
        s = sp * (0.8 + 0.25 * (k % 3))
        x, y = cx + math.cos(a) * s * t * 1.4, cy + math.sin(a) * s * t + grav * t * t
        m = frame()
        blob(m, x, y, cols[k % len(cols)], r=1 if t > 3 else 2 if k % 2 == 0 else 1)
        outline_alpha(m, SCORE)
        f.alpha_composite(m)


def build_refraction_blast():
    """Refraction Breaks (heavy payoff): the line of light across the hex flares white, then shatters, a column of
    ember-hearted glass shards bursts up out of it and rains back as chunks. Tall, fast, loud. 12 frames."""
    fr = []
    for i in range(12):
        f = frame()
        if i <= 1:                                             # the light line flares across the hex
            for o, col in ((0, WHITE), (-1, CYAN_L), (1, CYAN_L), (2, CYAN_D)):
                seg(f, (6, 25 + o), (44, 25 + o), col)
            if i == 1:
                blob(f, 25, 25, WHITE, r=3)
        if i == 2:                                              # white flash, the line breaks
            ground_ring(f, GRX - 2, GRY - 1, [(0, WHITE), (1, ORE_HOT), (-1, WHITE), (2, ORE)])
            for x in range(8, 43, 5):
                blob(f, x, 25, WHITE)
        if 2 <= i <= 6:                                        # the shard column
            g = {2: 0.4, 3: 0.85, 4: 1.0, 5: 0.9, 6: 0.6}[i]
            for dx, h, w, tilt in ((-9, 13, 5, -0.25), (9, 12, 5, 0.25), (-4, 20, 6, -0.08), (4, 19, 6, 0.1), (0, 25, 7, 0.0)):
                shard_poly(f, 25 + dx, 27, h * g, w, tilt, hot=(i == 3))
            if i >= 3:
                for x in (18, 25, 32):
                    blob(f, x, 27, ORE_HOT, r=2)
        if i >= 6:
            burst_chunks(f, 25, 12, i - 5, n=9, sp=2.4, drop=4)
            ground_ring(f, GRX - 2 + (i - 6), GRY - 1 + (i - 6) * 0.5, [(0, ORE if i < 9 else EMBER_D)])
        fr.append(f)
    return fr


def big_pane(f, cx, tip_y, h, w, hot=False):
    """A tall pane of glass falling point-first: lit left face, mid right face, white leading edge, dark outline."""
    n = frame()
    d = ImageDraw.Draw(n)
    top = tip_y - h
    d.polygon([(cx - w / 2, top), (cx, top), (cx, tip_y)], fill=(*(WHITE if hot else GLASS_L), 255))
    d.polygon([(cx, top), (cx + w / 2, top), (cx, tip_y)], fill=(*(GLASS_L if hot else GLASS_M), 255))
    d.line([(cx - w / 2, top), (cx, tip_y)], fill=(*WHITE, 255))
    d.line([(cx - w / 2 + 2, top + 3), (cx + 1, top + h * 0.6)], fill=(*GLASS_D, 255))
    outline_alpha(n, SCORE)
    f.alpha_composite(n)


def ember_column(f, cx, base, h, w):
    """The heavy detonation's column (dt_heavy's grammar): ember shards bursting up, white at the core."""
    for dx, hh, ww, tilt in ((-w * 0.45, h * 0.55, w * 0.35, -0.3), (w * 0.45, h * 0.6, w * 0.35, 0.3),
                             (-w * 0.2, h * 0.85, w * 0.4, -0.1), (w * 0.2, h * 0.8, w * 0.4, 0.12), (0, h, w * 0.5, 0)):
        n = frame()
        d = ImageDraw.Draw(n)
        tip = (cx + dx + tilt * hh, base - hh)
        d.polygon([(cx + dx - ww / 2, base), tip, (cx + dx + ww / 2, base)], fill=(*EMBER_RED, 255))
        d.polygon([(cx + dx - ww / 4, base), (tip[0], tip[1] + hh * 0.3), (cx + dx + ww / 4, base)], fill=(*EMBER_YEL, 255))
        outline_alpha(n, EMBER_DEEP)
        f.alpha_composite(n)
    blob(f, cx, base - 3, WHITE, r=2)


def thick_tendril(f, pts, base_w=3.0, col=BONE, side=BONE_S):
    n = frame()
    L = len(pts)
    for s, (x, y) in enumerate(pts):
        w = max(1.0, base_w * (1 - s / max(1, L)) + 0.6)
        for o in range(-int(w), int(w) + 1):
            if abs(o) <= w:
                px(n, x + o, y, col if o <= 0 else side)
    outline_alpha(n, BONE_D)
    f.alpha_composite(n)


def build_glassfall():
    """Glassfall pane (lethal heavy payoff): anticipation, the pane's shadow darkens the hex; a tall pane falls
    point-first; impact frame white; an ember column bursts up through the shattering glass; chunks rain and the
    scorch settles. 13 frames (0.65 s)."""
    fr = []
    for i in range(13):
        f = frame()
        if i <= 3:                                             # shadow grows, pane falls
            r = 4 + i * 2.5
            ImageDraw.Draw(f).ellipse([25 - r * 1.4, 26 - r * 0.45, 25 + r * 1.4, 26 + r * 0.45], fill=(*EMBER_DEEP, 255))
            big_pane(f, 25, -6 + i * 10.5, 26, 14)
        if i == 4:                                             # impact: the whole hex flashes white
            big_pane(f, 25, 27, 20, 14, hot=True)
            ground_ring(f, GRX - 1, GRY - 0.5, [(0, WHITE), (1, WHITE), (-1, EMBER_YEL), (2, EMBER_YEL)])
        if 5 <= i <= 8:
            g = {5: 0.7, 6: 1.0, 7: 0.85, 8: 0.5}[i]
            ember_column(f, 25, 28, 26 * g, 16)
            ground_ring(f, GRX - 1, GRY - 0.5, [(0, EMBER_YEL if i < 7 else EMBER_RED), (1, EMBER_RED)])
        if i >= 6:
            burst_chunks(f, 25, 14, i - 5, n=10, sp=2.8, drop=5)
        if i >= 9:
            ground_ring(f, GRX - 2, GRY - 1, [(0, EMBER_D)])
        fr.append(f)
    return fr


def build_shatterfall():
    """Shatterfall Gives Way (Act III, lethal, a field of hexes): the ceiling-pane gives way. Anticipation: cracks
    spider across a dark shadow; one broad pane crashes edge-first; white impact; a broad ember eruption tears up
    through it; glass rains and the floor smoulders. Compact per hex so a field reads as one collapse. 15 frames."""
    fr = []
    for i in range(15):
        f = frame()
        if i <= 4:
            r = 6 + i * 2.5
            ImageDraw.Draw(f).ellipse([25 - r * 1.3, 26 - r * 0.42, 25 + r * 1.3, 26 + r * 0.42], fill=(*EMBER_DEEP, 255))
            if i >= 2:                                           # the falling slab, edge-first
                y = -20 + (i - 2) * 16
                n = frame()
                d = ImageDraw.Draw(n)
                d.polygon([(13, y), (37, y - 3), (35, y + 8), (15, y + 11)], fill=(*GLASS_L, 255))
                d.polygon([(25, y - 1.5), (37, y - 3), (35, y + 8), (25, y + 9.5)], fill=(*GLASS_M, 255))
                d.line([(13, y), (37, y - 3)], fill=(*WHITE, 255))
                d.line([(19, y + 1), (23, y + 9)], fill=(*GLASS_D, 255))
                d.line([(29, y - 1), (31, y + 8)], fill=(*GLASS_D, 255))
                outline_alpha(n, SCORE)
                f.alpha_composite(n)
        if i == 5:
            n = frame()
            ImageDraw.Draw(n).ellipse([25 - 21, 25 - 10, 25 + 21, 25 + 10], fill=(*WHITE, 255))
            ImageDraw.Draw(n).ellipse([25 - 17, 25 - 8, 25 + 17, 25 + 8], fill=(*EMBER_YEL, 255))
            outline_alpha(n, EMBER_RED)
            f.alpha_composite(n)
        if 6 <= i <= 10:
            g = {6: 0.75, 7: 1.0, 8: 0.95, 9: 0.7, 10: 0.4}[i]
            ember_column(f, 18, 28, 20 * g, 12)
            ember_column(f, 32, 28, 22 * g, 12)
            ember_column(f, 25, 30, 30 * g, 16)
        if i >= 7:
            burst_chunks(f, 25, 10, i - 6, n=12, sp=3.0, drop=5)
        if i >= 9:
            ground_ring(f, GRX - 2, GRY - 1, [(0, EMBER_RED if i < 12 else EMBER_D), (1, EMBER_D)])
        fr.append(f)
    return fr


def build_enrage():
    """The Glass Remembers (the late backstop, field-wide): every hex grows a crown of outlined glass spikes that
    heat from white to ember and close inward, then a white-hot ember column erupts from the centre. 13 frames."""
    fr = []
    spikes = [(k * 45, 7 + (k % 2) * 3) for k in range(8)]
    for i in range(13):
        f = frame()
        if i <= 6:
            g = min(1.0, (i + 1) / 4)
            pull = 0 if i < 4 else (i - 3) * 0.12
            for a, h in sorted(spikes, key=lambda s: math.sin(math.radians(s[0]))):
                r = math.radians(a)
                bx = 25 + (GRX - 4) * (1 - pull) * math.cos(r)
                by = 25 + (GRY - 2) * (1 - pull) * math.sin(r) + 2
                shard_poly(f, bx, by, h * g, 5, -math.cos(r) * 0.4, hot=(i in (3, 4)))
            ground_ring(f, GRX - 3, GRY - 1.5, [(0, EMBER_YEL if i >= 3 else EMBER_RED), (1, EMBER_D)])
        if i == 6:
            blob(f, 25, 22, WHITE, r=4)
        if 7 <= i <= 10:
            g = {7: 0.8, 8: 1.0, 9: 0.8, 10: 0.45}[i]
            ember_column(f, 25, 29, 28 * g, 18)
        if i >= 8:
            burst_chunks(f, 25, 14, i - 7, n=10, sp=2.6, drop=3)
        fr.append(f)
    return fr


def build_grasp():
    """Grasp (the Feeler's strike: pierce + root): anticipation, an ink ripple opens under the target; three thick
    bone feelers whip up and curl over it; the clench (white flash, violet hold, held two frames); they sink back
    into the ink. 12 frames."""
    fr = []
    roots = [(-13, 36), (13, 36), (0, 38)]
    for i in range(12):
        f = frame()
        if i <= 10:
            r = min(1.0, (i + 1) / 3) if i < 8 else (11 - i) / 3
            n = frame()
            ImageDraw.Draw(n).ellipse([25 - 17 * r, 36 - 5 * r, 25 + 17 * r, 36 + 5 * r], fill=(*INK, 255))
            ImageDraw.Draw(n).ellipse([25 - 13 * r, 36 - 3.5 * r, 25 + 13 * r, 36 + 3.5 * r], fill=(*VIOLET_D, 255))
            f.alpha_composite(n)
        if 1 <= i <= 10:
            g = min(1.0, i / 3) if i <= 7 else (10 - i) / 3
            for k, (rx, ry) in enumerate(roots):
                h = 25 * g
                pts = []
                steps = max(2, int(h))
                for s in range(steps + 1):
                    u = s / steps
                    curl = (1 if rx < 0 else -1 if rx > 0 else 0.4) * (u ** 2.2) * (13 if i >= 3 else 6)
                    pts.append((25 + rx * (1 - u * 0.5) + curl, ry - s))
                thick_tendril(f, pts, base_w=2.2 if k < 2 else 1.6)
        if i in (4, 5):                                         # the clench, held
            n = frame()
            for side in (-1, 1):                                # the hold: violet glints where the tips lock, off the face
                blob(n, 25 + side * 9, 12, VIOLET_L, r=2)
                blob(n, 25 + side * 9, 12, WHITE)
            blob(n, 25, 4, WHITE, r=2 if i == 4 else 1)
            outline_alpha(n, INK)
            f.alpha_composite(n)
        fr.append(f)
    return fr


def build_echo_strike():
    """The echoes' strikes (Your Own Strike, Doorward Sweep, Cadet's Tether): anticipation glint; a broad crescent
    of dark silvered glass sweeps through the target; impact held white for two frames; the crescent breaks into
    falling shards and ash. 11 frames."""
    cx, cy, R = 30, 30, 20
    fr = []
    for i in range(11):
        f = frame()
        if i == 0:
            blob(f, 9, 12, WHITE, r=2)
            px(f, 6, 12, CYAN); px(f, 12, 12, CYAN); px(f, 9, 9, CYAN); px(f, 9, 15, CYAN)
        if 1 <= i <= 3:
            a1 = {1: 200, 2: 250, 3: 300}[i]
            n = frame()
            for a in range(160, a1 + 1, 2):
                g = math.radians(a)
                th = 4.5 * math.sin(math.pi * (a - 160) / max(20, a1 - 160))
                for o in range(0, int(th) + 1):
                    col = GLASS_L if o == 0 else GLASS_M if o < th - 1 else GLASS_D
                    px(n, cx + (R - o) * math.cos(g), cy + (R - o) * math.sin(g) * 0.8, col)
            g = math.radians(a1)
            blob(n, cx + R * math.cos(g), cy + R * math.sin(g) * 0.8, WHITE, r=2)
            outline_alpha(n, SCORE)
            f.alpha_composite(n)
        if i in (4, 5):
            n = frame()
            for a in range(160, 301, 2):
                g = math.radians(a)
                th = 4.5 * math.sin(math.pi * (a - 160) / 140)
                for o in range(0, int(th) + 1):
                    px(n, cx + (R - o) * math.cos(g), cy + (R - o) * math.sin(g) * 0.8, WHITE if i == 4 else GLASS_L)
            outline_alpha(n, GLASS_D)
            f.alpha_composite(n)
            blob(f, 25, 22, WHITE, r=3 if i == 4 else 2)
        if i >= 6:
            t = i - 5
            for k, a in enumerate(range(175, 300, 18)):
                if t > 3 and k % 2:
                    continue
                g = math.radians(a)
                x0, y0 = cx + (R - 2) * math.cos(g), cy + (R - 2) * math.sin(g) * 0.8
                x, y = x0 + math.cos(g) * t * 1.6, y0 + math.sin(g) * t * 1.2 + 0.35 * t * t
                n = frame()
                blob(n, x, y, GLASS_L if k % 2 else ASH_L, r=2 if t < 3 else 1)
                outline_alpha(n, SCORE)
                f.alpha_composite(n)
        fr.append(f)
    return fr


def build_pull():
    """Pull (Breathless Pull, Cadet's Tether): six ink tendrils with bone hooks lash in from the frame's edge, catch
    at the target's centre and yank tight into a violet knot that pulses and closes. 10 frames."""
    dirs = [k * 60 + 30 for k in range(6)]
    fr = []
    for i in range(10):
        f = frame()
        if i <= 5:
            reach = min(1.0, (i + 1) / 4)
            for a in dirs:
                g = math.radians(a)
                p0 = (25 + 23 * math.cos(g), 25 + 21 * math.sin(g))
                p1 = (25 + 23 * (1 - reach * 0.85) * math.cos(g), 25 + 21 * (1 - reach * 0.85) * math.sin(g))
                if i >= 4:
                    p0 = lerp(p0, p1, (i - 3) * 0.4)
                n = frame()
                for o in (-1, 0, 1):
                    seg(n, (p0[0], p0[1] + o), (p1[0], p1[1] + o), VIOLET_M if o < 1 else VIOLET)
                blob(n, p1[0], p1[1], BONE, r=2)
                outline_alpha(n, INK)
                f.alpha_composite(n)
        if 4 <= i <= 9:
            r = {4: 4, 5: 7, 6: 6, 7: 5, 8: 3, 9: 2}[i]
            n = frame()
            ImageDraw.Draw(n).ellipse([25 - r, 25 - r * 0.8, 25 + r, 25 + r * 0.8], fill=(*(VIOLET_L if i in (5, 6) else VIOLET_M), 255))
            if i in (5, 6):
                blob(n, 25, 25, WHITE, r=2)
            outline_alpha(n, INK)
            f.alpha_composite(n)
        fr.append(f)
    return fr


def build_shove():
    """Push (Doorward Sweep): a white impact at the target's centre, then a thick shock-arc of ash and dark glass
    blasts outward both ways, throwing chunks, and thins out. 10 frames."""
    fr = []
    for i in range(10):
        f = frame()
        if i <= 1:
            n = frame()
            ImageDraw.Draw(n).ellipse([25 - 7 + i * 2, 22 - 5 + i, 25 + 7 - i * 2, 22 + 5 - i], fill=(*WHITE, 255))
            outline_alpha(n, ASH_D)
            f.alpha_composite(n)
        if 1 <= i <= 7:
            r = 6 + (i - 1) * 3
            th = 4 if i < 4 else 3 if i < 6 else 2
            n = frame()
            for a in range(-60, 61, 3):
                g = math.radians(a)
                for side in (-1, 1):
                    for o in range(th):
                        x = 25 + side * (r - o) * math.cos(g)
                        y = 24 + (r - o) * 0.6 * math.sin(g)
                        px(n, x, y, ASH_L if o == 0 else ASH)
            outline_alpha(n, ASH_D)
            f.alpha_composite(n)
        if i >= 3:
            t = i - 2
            for side in (-1, 1):
                for k, (dy, sp) in enumerate(((-5, 1.0), (0, 1.3), (5, 0.9))):
                    if t > 4 and k != 1:
                        continue
                    n = frame()
                    blob(n, 25 + side * (8 + t * 3.2 * sp), 24 + dy + 0.3 * t * t, GLASS_L if k == 1 else ASH_L, r=2 if t < 3 else 1)
                    outline_alpha(n, SCORE)
                    f.alpha_composite(n)
        fr.append(f)
    return fr


def build_mend():
    """Worn Mending (heal on a Worn ally): a warm bone ring blooms at its feet, eight motes of warm light spiral up
    its sides and gather above its head into a soft four-point glint that blooms and fades. Warm bone-gold, not cyan
    (cyan means safe). 13 frames."""
    MEND = (240, 220, 160)
    MEND_D = (150, 126, 80)
    fr = []
    for i in range(13):
        f = frame()
        if i <= 5:
            r = 6 + i * 2.6
            ground_ring(f, r, r * 0.32, [(0, MEND if i < 4 else MEND_D), (1, MEND_D)], cy=36)
        for k in range(8):
            t = i - (k % 4) * 0.8
            if t < 0 or t > 8:
                continue
            side = -1 if k % 2 else 1
            y = 36 - t * 3.4
            x = 25 + side * (15 - t * 0.9) + side * math.sin(t * 0.9 + k) * 1.5
            n = frame()
            blob(n, x, y, WHITE if t < 2 else MEND, r=2 if t < 5 else 1)
            outline_alpha(n, MEND_D)
            f.alpha_composite(n)
        if 7 <= i <= 12:
            r = {7: 2, 8: 4, 9: 6, 10: 5, 11: 3, 12: 1}[i]
            n = frame()
            for s in range(1, r + 1):
                for ddx, ddy in ((s, 0), (-s, 0), (0, s), (0, -s)):
                    px(n, 25 + ddx, 4 + 1 + ddy * 0.8, WHITE if s <= max(1, r // 2) else MEND)
            blob(n, 25, 5, WHITE)
            outline_alpha(n, MEND_D)
            f.alpha_composite(n)
        fr.append(f)
    return fr


CUSTOM = (
    # (file, builder, kind, use, serves, note)
    ('tile_moe_heavy_v1.webp', build_tile_heavy, 'STATIC', 'staticAssetPath', ['tg_heavy'],
     'Heavy mark (Sayo): smoked-glass disc ringed by ember-edged glass facets, six ember cracks to a white-hot core'),
    ('anim_moe_heavy_glint_v1.webp', build_heavy_glint, 'ANIMATION', 'static', ['tg_heavy'],
     'Heavy loop: ember flares and lifting embers at the ring\'s ends on the 0.8 s beat (portrait-clear)'),
    ('anim_moe_heavy_appear_v1.webp', build_heavy_appear, 'ANIMATION', 'appear', ['tg_heavy'],
     'Heavy mark arrives: ember-edged glass shards drop onto the ring, it rings white, cracks run in'),
    ('tile_moe_control_v1.webp', build_tile_control, 'STATIC', 'staticAssetPath', ['tg_control'],
     'Control/lock mark (Sayo): a ring of faceted violet glass links on ink, a closed glass eye (the hush) at the centre'),
    ('anim_moe_control_glint_v1.webp', build_control_glint, 'ANIMATION', 'static', ['tg_control'],
     'Control loop: the links tighten on the beat at the ring\'s ends; a white glint runs round (portrait-clear)'),
    ('anim_moe_control_appear_v1.webp', build_control_appear, 'ANIMATION', 'appear', ['tg_control', 'moe_lull_visual'],
     'Control mark arrives: violet glass links whip round and snap shut with an ink flash'),
    ('tile_moe_linger_v1.webp', build_tile_linger, 'STATIC', 'staticAssetPath', ['tg_linger', 'moe_hush_floor'],
     'Lingering pool (Sayo): a crazed glass pane with bile seeping up through its cracks'),
    ('anim_moe_linger_glint_v1.webp', build_linger_glint, 'ANIMATION', 'static', ['tg_linger', 'moe_hush_floor'],
     'Linger loop: bile bubbles swell and pop at the pool\'s ends, 1.2 s (portrait-clear)'),
    ('anim_moe_linger_appear_v1.webp', build_linger_appear, 'ANIMATION', 'appear', ['tg_linger', 'moe_hush_floor'],
     'Lingering pool arrives: the glass crazes and bile wells up through the cracks'),
    ('tile_moe_safe_v1.webp', build_tile_safe, 'STATIC', 'staticAssetPath', ['tg_safe'],
     'Safe hex (Sayo): a cut-glass cyan diamond pane with a white four-point star'),
    ('anim_moe_safe_glint_v1.webp', build_safe_glint, 'ANIMATION', 'static', ['tg_safe'],
     'Safe loop: calm light rising at the diamond\'s points, a soft star twinkle, 1.6 s (portrait-clear)'),
    ('anim_moe_safe_appear_v1.webp', build_safe_appear, 'ANIMATION', 'appear', ['tg_safe'],
     'Safe hex arrives: a cyan beam rises, the star opens white, the diamond rim draws'),
    ('anim_moe_etch_appear_v1.webp', build_etch_appear, 'ANIMATION', 'appear', ['tg_etch'],
     'Etching arrives: a white scribe spark cuts the lattice out from the centre, the cut flares gold'),
    ('anim_moe_refraction_blast_v1.webp', build_refraction_blast, 'ANIMATION', 'appear', ['moe_refraction'],
     'Refraction Breaks: the line of light flares and shatters; an ember-hearted glass column bursts up and rains back'),
    ('anim_moe_glassfall_v1.webp', build_glassfall, 'ANIMATION', 'appear', ['moe_glassfall'],
     'Glassfall pane: a pane falls point-first, white-hot ember impact, shatters into chunks'),
    ('anim_moe_shatterfall_v1.webp', build_shatterfall, 'ANIMATION', 'appear', ['moe_shatterfall'],
     'Shatterfall Gives Way: two broad panes crash down, the hex erupts white-hot, a ring shock runs out'),
    ('anim_moe_enrage_v1.webp', build_enrage, 'ANIMATION', 'appear', ['moe_enrage'],
     'The Glass Remembers: a crown of ember-hearted glass spikes closes in and bursts white on every hex'),
    ('anim_moe_grasp_v1.webp', build_grasp, 'ANIMATION', 'appear', ['moe_grasp'],
     'Grasp: bone feelers whip up out of an ink ripple and clench over the target'),
    ('anim_moe_echo_strike_v1.webp', build_echo_strike, 'ANIMATION', 'appear', ['moe_echo_strike'],
     'The echoes\' strikes (Your Own Strike, Doorward Sweep, Cadet\'s Tether): a slash of silvered glass, ash and chips'),
    ('anim_moe_pull_v1.webp', build_pull, 'ANIMATION', 'appear', ['moe_pull'],
     'Pull (Breathless Pull, Cadet\'s Tether): ink streaks rush in to the target and lock in a violet knot'),
    ('anim_moe_shove_v1.webp', build_shove, 'ANIMATION', 'appear', ['moe_shove'],
     'Push (Doorward Sweep): an arc of ash and dark glass bursts outward from the target'),
    ('anim_moe_mend_v1.webp', build_mend, 'ANIMATION', 'appear', ['moe_mend'],
     'Worn Mending: warm bone light motes rise and gather into a soft glint over the mended summon'),
)


def export_custom(save):
    for name, fn, kind, use, serves, note in CUSTOM:
        out = fn()
        if kind == 'STATIC':
            save(name, out, 1, use, serves, note, kind='STATIC')
        else:
            save(name, strip(out), len(out), use, serves, note)


def export():
    os.makedirs(EXPORTS, exist_ok=True)
    rows = []

    def save(name, img, frames, use, serves, note, kind='ANIMATION'):
        p = os.path.join(EXPORTS, name)
        img.save(p, lossless=True, quality=100, method=6)
        size = os.path.getsize(p)
        assert size < MAX_BYTES, (name, size)
        rows.append({'file': f'art/mother_of_echoes_fx/exports/{name}', 'type': kind, 'frames': frames,
                     'speed': MS if kind == 'ANIMATION' else None, 'duration_ms': frames * MS if kind == 'ANIMATION' else None,
                     'frame_px': N * SCALE, 'drawn_grid_px': N, 'bytes': size, 'use': use, 'serves': serves, 'note': note})
        print(f'{name}: {kind} {frames} frame(s), {size} bytes')

    save('tile_moe_etch_v3.webp', build_etch_tile(), 1, 'staticAssetPath', ['tg_etch'],
         'The Etching mark, STATIC still under the characters, stretched to the hex box; the lattice joins seamlessly '
         'across a field', kind='STATIC')
    g = build_etch_glint()
    save('anim_moe_etch_glint_v1.webp', strip(g), len(g), 'staticAnimation', ['tg_etch'],
         'Etching loop over the tile: scribe sparks run out along the lattice and the side junctions twinkle on the '
         '0.8 s beat (portrait-clear)')
    for name, fn, use, serves, note, loop in (
            ('anim_moe_recast_v1.webp', build_recast, 'appear', ['moe_recast'],
             'Recast: the etched lattice flashes back and glass blades rise along it, then shatter (the Etching comes due)', False),
            ('anim_moe_guard_open_v2.webp', build_guard_open, 'static', ['moe_guard_open'],
             'Guard open (Recast weakness, on Sayo): a cracked ring of etched gold glass round her portrait; the plates push '
             'out and flare white on the beat (portrait-clear loop)', True),
            ('anim_moe_quiet_v1.webp', build_quiet, 'appear', ['moe_quiet'],
             'The Quiet: an ink ring closes on the target, a bone-white hush, the dust stops', False),
            ('anim_moe_lancet_v2.webp', build_lancet, 'appear', ['moe_lancet'],
             'Glass Lancet: a thick outlined skyglass needle streaks in, white impact star held 2 frames, splinters', False),
            ('anim_moe_feeler_v2.webp', build_feeler, 'appear', ['moe_feeler'],
             'The Listening (summon flourish): ink ripples at the root, bone wisps curl up beside the summoned feeler', False),
            ('anim_moe_lull_v3.webp', build_lull, 'static', ['moe_lull'],
             'The Glass Falls Quiet: 2x2 glass dust and two dust curtains drifting down beside Sayo; staticAnimation of the jutsu\'s fleeprevent '
             '(SELF, 2 rounds), moved off the visual the server drops (RUL-2026-11-02-101); clears an AI portrait', True),
            ('anim_moe_still_dark_v2.webp', build_stillness, 'appear', ['moe_stillness'],
             'Nothing Moves: a solid ink ring closes in from the rim, a crisp violet edge, the dust stops', False),
            ('anim_moe_breath_draw_v1.webp', build_breathless, 'appear', ['moe_breathless'],
             'Breathless Pull: breath drawn out of the hex, up and away; a violet lock closes at the feet', False),
            ('anim_moe_cradle_v2.webp', build_cradle, 'static', ['moe_cradle'],
             'Cradle: pale feelers rise at Sayo\'s sides and cup beneath her, an ink hold throbbing violet on the beat; '
             'staticAnimation of the decreasedamagetaken effect (while a feeler lives she takes 90% less); AI portrait clear', True),
            ('anim_moe_lucid_aura_v1.webp', build_lucid, 'static', ['moe_lucid'],
             'Lucid: eight cold skyglass facets circling Sayo, white on the beat (AI portrait clear)', True),
            ('anim_moe_likeness_ring_v2.webp', build_likeness, 'appear', ['moe_likeness'],
             'Your Likeness (summon flourish): a silvered-glass ring closes on the summon, cracks and bursts into shards', False),
            ('anim_moe_worn_ash_v2.webp', build_worn, 'appear', ['moe_worn'],
             'The Worn (summon flourish): grey-brown ash wells up out of the glass round the summon', False)):
        fr = fn()
        save(name, strip(fr), len(fr), use, serves, note)
    fm = build_flood_mask()
    save('anim_moe_flood_mask_v1.webp', strip(fm), len(fm), 'appear', ['moe_flood'],
         'The Names Flood In: one great glass mask rises, its eyes snap open as ember cracks split it, then it bursts '
         'into chunky shards (director keyframes ME28b, drawn for the 50 px delivery)')
    export_custom(save)
    meta = {'source': 'art/mother_of_echoes_fx/build_fx.py (pixel art in code)',
            'renderer': 'theninjarpg@3314d122 libs/rendering/scenes/combatEffects.ts (pixi): one square sprite per hex, '
                        'tile.height * 2.5; staticAssetPath stretched to the hex box under the actors',
            'layout': 'vertical strip, one square frame per row', 'speed_unit': 'ms per frame (gameAsset.speed)',
            'assets': rows}
    with open(os.path.join(EXPORTS, 'moe_fx_v1.json'), 'w') as fh:
        json.dump(meta, fh, indent=1)
        fh.write('\n')


if __name__ == '__main__':
    export()
