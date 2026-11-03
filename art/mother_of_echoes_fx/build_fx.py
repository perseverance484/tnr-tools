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
SKY = os.path.join(ROOT, 'art', 'skyglass_boss_fx', 'exports')
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
    vertical axis is drawn half as wide as the diagonals and every spoke lands about equally thick on screen. A
    sparse ordered-dither haze (denser at the centre, thin at the edge) tints the marked region without a fill
    boundary, so neighbouring tiles cannot show a seam."""
    t = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    hz = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    for y in range(N):
        for x in range(N):
            r = math.hypot((x - 25) / 25, (y - 25) / 25)
            px(hz, x, y, ETCH_DIM if r < 0.55 else ETCH_DARK, keep=0.25 if r < 0.55 else 0.125)
    t.alpha_composite(hz)
    d = ImageDraw.Draw(t)
    diag = {k: e for k, e in T_ENDS.items() if k not in ('T', 'B')}
    vert = {k: T_ENDS[k] for k in ('T', 'B')}
    etch_lines(t, diag, (25, 25), widths=(4, 2, 1))
    etch_lines(t, vert, (25, 25), widths=(2, 1, 1))
    # the cut's origin: a small hard-edged nick of white at the centre
    d.rectangle([23, 21, 27, 29], fill=(*ETCH_DARK, 255))
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
def build_guard_open():
    """Weakness after a Recast: four splinters of the shattered glass circle the hex rim, catching gold light on the
    beat. Portrait-clear loop (they pass behind the portraits at the front and back); a quarter turn per beat, so
    the loop is seamless."""
    fr = []
    for i in range(BEAT):
        f = frame()
        hot = i in (0, 1)
        for k in range(4):
            ang = 2 * math.pi * (k / 4 + i / (BEAT * 4)) + 0.4
            x, y = round(25 + math.cos(ang) * 19), round(25 + math.sin(ang) * 9.5)
            shard = [(0, -3, ETCH_HOT if hot else GLASS_L), (-1, -2, GLASS_L), (0, -2, WHITE if hot else GLASS_L),
                     (1, -2, GLASS_M), (-1, -1, GLASS_L), (0, -1, GLASS_L), (1, -1, GLASS_M), (-1, 0, GLASS_L),
                     (0, 0, GLASS_M), (1, 0, GLASS_M), (0, 1, GLASS_M)]
            for dx, dy, col in shard:
                px(f, x + dx, y + dy, col)
            for dx, dy in ((0, -4), (-2, -2), (2, -2), (-2, -1), (2, -1), (-2, 0), (2, 0), (-1, 1), (1, 1), (0, 2)):
                px(f, x + dx, y + dy, GLASS_D)
            if hot:
                px(f, x + 3, y - 3, ETCH_HOT)
                px(f, x - 3, y - 4, ETCH_MID)
        fr.append(f)
    return mind_portrait(fr)


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
def build_lancet():
    """Glass Lancet: a needle of skyglass streaks in from the upper left, strikes, and splinters. 10 frames."""
    a, b = (4.0, 3.0), (25.0, 20.0)
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    rng = [(math.cos(t) * s, math.sin(t) * s) for t, s in ((3.6, 1.8), (4.2, 2.2), (4.9, 1.6), (5.6, 2.0), (0.4, 1.5), (2.6, 1.7))]
    fr = []
    for i in range(10):
        f = frame()
        if i <= 3:
            tip = lerp(a, b, (i + 1) / 4)
            for k in range(1, 7):  # trail
                px(f, tip[0] - ux * (k + 7), tip[1] - uy * (k + 7), CYAN_D if k > 3 else CYAN, keep=1.0 if k < 4 else 0.5)
            for k in range(8):  # the needle: white core, cyan edge, dark under-edge
                x, y = tip[0] - ux * k, tip[1] - uy * k
                px(f, x, y, WHITE if k < 5 else GLASS_L)
                px(f, x - uy, y + ux, CYAN)
                px(f, x + uy, y - ux, CYAN_D if k > 1 else CYAN)
        if i == 4:
            for s in range(-4, 5):
                px(f, b[0] + s, b[1], WHITE if abs(s) < 3 else CYAN)
                px(f, b[0], b[1] + s * 0.75, WHITE if abs(s) < 3 else CYAN)
            ellipse(f, b[0], b[1], 6, 4, CYAN, n=16)
        if i >= 5:
            t = i - 4
            keep = 1.0 if t < 3 else 0.5 if t < 5 else 0.25
            for vx, vy in rng:
                x, y = b[0] + vx * t * 1.3, b[1] + vy * t * 1.3 + 0.3 * t * t
                px(f, x, y, GLASS_L if t < 3 else CYAN, keep)
                px(f, x + 1, y + 1, CYAN_D, keep)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ moe_feeler
def build_feeler():
    """The Listening: a pale feeler of the Silence rises from the floor, curls its tip as if listening, and the dust
    around it stops. 14 frames, one-shot (the summon appears where it stands)."""
    base = (25, 34)
    lengths = [0, 5, 10, 15, 20, 24, 27, 28, 28, 28, 28, 28, 28, 28]
    motes = [(16, 14), (34, 12), (14, 24), (37, 22), (20, 8), (31, 27)]
    fr = []
    for i in range(14):
        f = frame()
        if i <= 4:  # the floor gives: an ink ripple at the root
            r = 3 + i * 1.5
            ellipse(f, base[0], base[1] + 1, r, r * 0.35, INK, n=36, keep=1.0 if i < 3 else 0.5)
        Lh = lengths[i]
        keep = 1.0 if i < 11 else 0.5 if i < 13 else 0.25
        if Lh:
            pts = []
            n = max(2, Lh)
            for k in range(n + 1):
                s = k / n
                x = base[0] + 3.2 * math.sin(s * 3.6 + i * 0.25) * s
                y = base[1] - Lh * s
                pts.append((x, y, s))
            # curl the tip toward the listener's right
            if Lh >= 24:
                tx, ty, _ = pts[-1]
                for k, (cx, cy) in enumerate(((tx + 1, ty - 1), (tx + 2, ty), (tx + 2, ty + 1), (tx + 1, ty + 2))):
                    pts.append((cx, cy, 1.0))
            for x, y, s in pts:
                th = 2.4 * (1 - s) + 0.6
                for o in range(-int(th) - 1, int(th) + 2):
                    if abs(o) <= th:
                        col = BONE if o <= 0 else BONE_S
                        px(f, x + o, y, col, keep)
                    elif abs(o) <= th + 1:
                        px(f, x + o, y, BONE_D, keep)
            for s_knot in (0.3, 0.55, 0.78):
                for x, y, s in pts:
                    if abs(s - s_knot) < 0.5 / max(2, Lh) + 0.02:
                        px(f, x, y, BONE_D, keep)
                        px(f, x + 1, y, BONE_D, keep)
                        break
        if i >= 7:
            for mx, my in motes:
                px(f, mx, my, DUST, keep)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ moe_lull
def build_lull():
    """The Glass Falls Quiet: the breath between cycles. A few motes of pale glass dust drift down at the hex's
    sides and settle. Two beats (1.6 s), portrait-clear, deliberately quiet."""
    period = BEAT * 2
    motes = [(8, 0), (12, 11), (39, 5), (43, 19), (10, 22), (41, 27)]
    fr = []
    for i in range(period):
        f = frame()
        for x0, t0 in motes:
            k = (i - t0) % period
            y = 12 + k * 0.7
            x = x0 + (1 if (k // 6) % 2 else 0)
            keep = 1.0 if k < 18 else 0.5 if k < 26 else 0.25
            px(f, x, y, DUST, keep)
        fr.append(f)
    return mind_portrait(fr)


# ------------------------------------------------------------------------------------------------ re-exports
REEXPORTS = {
    # new file: (source strip in art/skyglass_boss_fx/exports, spec art names served, use, note)
    'anim_moe_stillness_v1.webp': ('anim_chain_wrap_v1.webp', ['moe_stillness'], 'appear',
                                   'Nothing Moves: the violet lock (dt_control family) on the stunned hex; pairs with tg_control'),
    'anim_moe_breathless_v1.webp': ('anim_command_absolute_v1.webp', ['moe_breathless'], 'appear',
                                    'Breathless Pull: chains lock and the seal stamps (violet control family); pairs with tg_control'),
    'anim_moe_lucid_v1.webp': ('anim_crown_aura_v1.webp', ['moe_lucid'], 'static',
                               'Lucid: a ring of skyglass shards circling Sayo (buff loop; keeps the portrait clear)'),
    'anim_moe_echo_rise_v1.webp': ('anim_recall_v1.webp', ['moe_likeness', 'moe_worn'], 'appear',
                                   'Your Likeness and the Worn: an echo pulled up out of the glass (summon flourish)'),
}


def harden(img):
    """Partial alpha (the boss_fx strips' 130 step) becomes full-alpha pixels kept by an ordered dither in proportion
    to their alpha, as animate_an.py does for its fades: the soft-edge share then passes the spec ceiling and the
    look at 50 px is unchanged. Works on the 50 px grid, before the x3 delivery scale."""
    g = img.copy()
    p = g.load()
    for y in range(g.height):
        for x in range(g.width):
            r, gg, b, a = p[x, y]
            if 0 < a < 255:
                p[x, y] = (r, gg, b, 255 if BAYER[y % 4][x % 4] < a / 255 * 16 else 0)
    return g


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

    save('tile_moe_etch_v1.webp', build_etch_tile(), 1, 'staticAssetPath', ['tg_etch'],
         'The Etching mark, STATIC still under the characters, stretched to the hex box; the lattice joins seamlessly '
         'across a field', kind='STATIC')
    g = build_etch_glint()
    save('anim_moe_etch_glint_v1.webp', strip(g), len(g), 'staticAnimation', ['tg_etch'],
         'Etching loop over the tile: scribe sparks run out along the lattice and the side junctions twinkle on the '
         '0.8 s beat (portrait-clear)')
    for name, fn, use, serves, note, loop in (
            ('anim_moe_recast_v1.webp', build_recast, 'appear', ['moe_recast'],
             'Recast: the etched lattice flashes back and glass blades rise along it, then shatter (the Etching comes due)', False),
            ('anim_moe_guard_open_v1.webp', build_guard_open, 'static', ['moe_guard_open'],
             'Guard open (the Recast weakness): splinters circle the hex rim, gold on the beat (portrait-clear loop)', True),
            ('anim_moe_quiet_v1.webp', build_quiet, 'appear', ['moe_quiet'],
             'The Quiet: an ink ring closes on the target, a bone-white hush, the dust stops', False),
            ('anim_moe_lancet_v1.webp', build_lancet, 'appear', ['moe_lancet'],
             'Glass Lancet: a skyglass needle streaks in and splinters', False),
            ('anim_moe_feeler_v1.webp', build_feeler, 'appear', ['moe_feeler'],
             'The Listening: a pale feeler rises and curls its tip (summon flourish)', False),
            ('anim_moe_lull_v1.webp', build_lull, 'static', ['moe_lull'],
             'The Glass Falls Quiet: glass dust drifting down at the hex sides (portrait-clear loop)', True)):
        fr = fn()
        save(name, strip(fr), len(fr), use, serves, note)
    for name, (src, serves, use, note) in REEXPORTS.items():
        s = Image.open(os.path.join(SKY, src)).convert('RGBA')
        frames = s.height // s.width
        assert s.width == N and s.height == N * frames, (src, s.size)
        save(name, harden(s).resize((s.width * SCALE, s.height * SCALE), Image.NEAREST), frames, use, serves,
             f'{note}. Re-export x{SCALE} (nearest) of art/skyglass_boss_fx/exports/{src} (boss_fx.py, director key '
             f'art 2026-10-28), its 130 alpha step turned into an ordered dither (spec soft-edge ceiling); not live '
             f'before this.')
    meta = {'source': 'art/mother_of_echoes_fx/build_fx.py (pixel art in code; re-exports of art/skyglass_boss_fx strips)',
            'renderer': 'theninjarpg@3314d122 libs/rendering/scenes/combatEffects.ts (pixi): one square sprite per hex, '
                        'tile.height * 2.5; staticAssetPath stretched to the hex box under the actors',
            'layout': 'vertical strip, one square frame per row', 'speed_unit': 'ms per frame (gameAsset.speed)',
            'assets': rows}
    with open(os.path.join(EXPORTS, 'moe_fx_v1.json'), 'w') as fh:
        json.dump(meta, fh, indent=1)
        fh.write('\n')


if __name__ == '__main__':
    export()
