#!/usr/bin/env python3
"""Subaku Palace resting floor, 'classic': the director's own tile (ref c, the hi-res live DemonCastleFloor), with its
bands redrawn on its own stone so every band end meets its neighbour (director 2026-11-06: "make it resemble the old
hex as much as possible").

    python3 classic.py          # .cache/classic_1024.png and a join report (build_domain.py exports the tile)

Canvas: the game stretches the tile canvas corner to corner into the 2:1 hex box, so ref c is cropped to its hex
bounds and resampled square. Coordinates as floor.py: regular flat-top hex, circumradius 1, y down; corner k at 60 k
deg; edge k runs from corner k to corner k + 1; u is the fraction along it.

Join rule: across edge k a neighbour shows its edge k + 3, so a band leaving edge k at u with outward direction d
needs a band leaving edge k + 3 at 1 - u with outward direction d + 180. Measured on ref c, 11 of its band ends have
no partner (only the L / bottom-left arc and the S / bracket pairs come close). The layout below keeps his five
elements and moves only their ends:
- S band: leaves the upper-left edge horizontally (his) at u 0.24 (his 0.30); its lower end comes down to the bottom
  edge at 0.15, heading down (his ran out through the lower-right edge near the bottom corner);
- top-left L: his: vertical from the top edge at 0.20 (his 0.216), a chamfered corner, horizontal to the upper-left
  midpoint (his 0.48);
- top-right arc: his, round the top-right corner from the top edge at 0.85 to the upper-right midpoint;
- bottom-left arc: his sweep up from the bottom edge at 0.80 (his 0.81), now ending at the lower-left midpoint (his
  ran on to the left corner);
- right bracket: his chamfered bracket, attached to the lower-right edge at the midpoint and at 0.76 (his straddled
  the right corner).
Pairs: L top / bottom-left arc (0.20 / 0.80, vertical); L left / bracket (0.50 / 0.50, horizontal); S left / bracket
(0.24 / 0.76, horizontal); S bottom / top-right arc (0.15 / 0.85, vertical); bottom-left arc / top-right arc (the
midpoints, square to the edges). Every end is exact in position and direction.
Profile: his band total width (0.105 radius) as a symmetric double rail (two rails, a dark groove between), because
his wide-plus-narrow pair cannot keep its narrow rail on a consistent side across a seam. The rails are textured with
his own burnished gold (sampled from the straight arm of his L); the stone, mortar glow and dark rim are his pixels,
cloned in where an old band no longer runs.
"""
import math
import os
import sys

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, 'refs', 'ref_domain_tile_c_1254.png')
N = 1024
SQ3 = math.sqrt(3)
H = SQ3 / 2
C = [(math.cos(math.radians(60 * k)), math.sin(math.radians(60 * k))) for k in range(6)]
PX = 2.0 / N                      # hex units per canvas pixel (x); y is the same after the square resample (H / (N/2))

RAIL = 0.058                      # one rail's width (QA r4: thickened toward his visible width at 50 px)
GROOVE = 0.012
HALF = RAIL + GROOVE / 2          # band half-width: 0.064
OUTLINE = 0.008
CAP = 0.30                        # his segment caps: a dark joint across the band every 0.30 of arc length
LIGHT = (-0.6, -0.8)              # his bevel light, from the upper left
BLEED = 0.06                      # content past the hex edge (the neighbours' continuation), so no seam opens
RIM = 0.035                       # his dark rim is removed: the last 0.035 in from each edge repeats the inner pixels


def edge_point(k, u):
    (x1, y1), (x2, y2) = C[k], C[(k + 1) % 6]
    return x1 + (x2 - x1) * u, y1 + (y2 - y1) * u


def to_px(x, y):
    return (x + 1) / 2 * N, (y / H + 1) / 2 * N


def to_hex(px, py):
    return (px + 0.5) / N * 2 - 1, ((py + 0.5) / N * 2 - 1) * H


def inside(x, y, eps=0.0):
    return abs(y) <= H + eps and SQ3 * abs(x) + abs(y) <= SQ3 + eps


def load_canvas():
    im = Image.open(REF).convert('RGBA')
    a = im.getchannel('A')
    ys = [y for y in range(im.height) if any(a.getpixel((x, y)) > 128 for x in range(300, 950, 8))]
    xs = [x for x in range(im.width) if a.getpixel((x, im.height // 2)) > 128]
    return im.crop((xs[0], ys[0], xs[-1] + 1, ys[-1] + 1)).resize((N, N), Image.LANCZOS)


def is_gold(p):
    r, g, b, a = p
    return a > 200 and ((r > 80 and g > 45 and r > b + 40 and g > b + 10) or (r > 200 and g > 165 and r > b + 25))


# ------------------------------------------------------------------ the layout (polylines in hex units)
def cubic(p0, p1, p2, p3, n=120):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def line(p, q, n=40):
    return [(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n + 1)]


def path_ext(pts, ext=0.08):
    """Extend both ends straight on past the edge (so the rails run into the bleed and over the seam)."""
    (x0, y0), (x1, y1) = pts[0], pts[1]
    d = math.hypot(x0 - x1, y0 - y1)
    a = (x0 + (x0 - x1) / d * ext, y0 + (y0 - y1) / d * ext)
    (x0, y0), (x1, y1) = pts[-1], pts[-2]
    d = math.hypot(x0 - x1, y0 - y1)
    b = (x0 + (x0 - x1) / d * ext, y0 + (y0 - y1) / d * ext)
    return [a] + pts + [b]


def dir_vec(deg):
    return math.cos(math.radians(deg)), math.sin(math.radians(deg))


def layout():
    P = {}
    # S: upper-left edge (e3) at 0.24, travelling right (0 deg); bottom edge (e1) at 0.15, travelling down (90 deg)
    s0, s1 = edge_point(3, 0.24), edge_point(1, 0.15)
    m = (-0.02, 0.18)                                   # the diagonal run through the middle, at 50 deg
    t = dir_vec(50)
    P['S'] = cubic(s0, (s0[0] + 0.45, s0[1]), (m[0] - t[0] * 0.30, m[1] - t[1] * 0.30), m) + \
        cubic(m, (m[0] + t[0] * 0.30, m[1] + t[1] * 0.30), (s1[0], s1[1] - 0.22), s1)[1:]
    # L: top edge (e4) at 0.20 straight down, chamfer, left to M3 (e3 at 0.50)
    l0, l1 = edge_point(4, 0.20), edge_point(3, 0.50)
    ch = 0.10
    P['L'] = line(l0, (l0[0], l1[1] - ch)) + line((l0[0], l1[1] - ch), (l0[0] - ch, l1[1]))[1:] + \
        line((l0[0] - ch, l1[1]), l1)[1:]
    # top-right arc: top edge (e4) at 0.85 heading down -> M5 (e5 at 0.50) leaving at 330 deg
    t0, t1 = edge_point(4, 0.85), edge_point(5, 0.50)
    o = dir_vec(330)
    P['TR'] = cubic(t0, (t0[0], t0[1] + 0.32), (t1[0] - o[0] * 0.32, t1[1] - o[1] * 0.32), t1)
    # bottom-left arc: bottom edge (e1) at 0.80 heading up -> M2 (e2 at 0.50) leaving at 150 deg
    b0, b1 = edge_point(1, 0.80), edge_point(2, 0.50)
    o = dir_vec(150)
    P['BL'] = cubic(b0, (b0[0], b0[1] - 0.45), (b1[0] - o[0] * 0.40, b1[1] - o[1] * 0.40), b1)
    # bracket: lower-right edge (e0) at 0.50 and 0.76, both horizontal; a chamfered "[" between them
    k0, k1 = edge_point(0, 0.50), edge_point(0, 0.76)
    xl = 0.40                                         # his bracket: a deep '[' with crisp 45 deg corners
    c2 = 0.045
    P['BR'] = line(k0, (xl + c2, k0[1])) + line((xl + c2, k0[1]), (xl, k0[1] + c2))[1:] + \
        line((xl, k0[1] + c2), (xl, k1[1] - c2))[1:] + line((xl, k1[1] - c2), (xl + c2, k1[1]))[1:] + \
        line((xl + c2, k1[1]), k1)[1:]
    return {k: path_ext(v) for k, v in P.items()}


def ends():
    """(edge, u, outward direction deg) for every band end, for the join check."""
    return [(3, 0.24, 180), (1, 0.15, 90), (4, 0.20, 270), (3, 0.50, 180), (4, 0.85, 270), (5, 0.50, 330),
            (1, 0.80, 90), (2, 0.50, 150), (0, 0.50, 0), (0, 0.76, 0)]


def check_joins():
    E = ends()
    bad = []
    for k, u, d in E:
        if not any(k2 == (k + 3) % 6 and abs(u2 - (1 - u)) < 1e-9 and (d2 - d - 180) % 360 == 0 for k2, u2, d2 in E):
            bad.append((k, u, d))
    return bad


# ------------------------------------------------------------------ rendering
def dist_field(paths):
    """Per canvas pixel: (distance to the nearest band centreline, arc length there, side sign, path name)."""
    segs = []
    for name, pts in paths.items():
        acc = 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            segs.append((x0, y0, x1, y1, L, acc, name))
            acc += L
    # bucket segments on a coarse grid for speed
    G = 24
    grid = {}
    for s in segs:
        x0, y0, x1, y1 = s[:4]
        r = HALF + OUTLINE + 0.04
        for gx in range(int((min(x0, x1) - r + 1.2) * G / 2.4), int((max(x0, x1) + r + 1.2) * G / 2.4) + 1):
            for gy in range(int((min(y0, y1) - r + 1.2) * G / 2.4), int((max(y0, y1) + r + 1.2) * G / 2.4) + 1):
                grid.setdefault((gx, gy), []).append(s)
    return segs, grid, G


def nearest(grid, G, x, y):
    best = None
    for s in grid.get((int((x + 1.2) * G / 2.4), int((y + 1.2) * G / 2.4)), ()):
        x0, y0, x1, y1, L, acc, name = s
        dx, dy = x1 - x0, y1 - y0
        t = max(0.0, min(1.0, ((x - x0) * dx + (y - y0) * dy) / (L * L))) if L else 0.0
        px, py = x0 + dx * t, y0 + dy * t
        d = math.hypot(x - px, y - py)
        if best is None or d < best[0]:
            side = (dx * (y - y0) - dy * (x - x0))
            best = (d, acc + t * L, 1 if side >= 0 else -1, name, (dx / L, dy / L) if L else (1, 0))
    return best


def gold_texture(can):
    """His burnished gold: the wide rail of his L's straight vertical arm, as a (across, along) strip."""
    px = can.load()
    # the arm runs down from the top edge at canvas x ~ 0.343-0.374 N; take its brightest 30 px wide core, rows 2-17 %
    x0 = int(0.343 * N)
    w = int(0.032 * N)
    y0, y1 = int(0.02 * N), int(0.17 * N)
    tex = Image.new('RGB', (w, y1 - y0))
    tp = tex.load()
    for y in range(y0, y1):
        for x in range(w):
            r, g, b, a = px[x0 + x, y]
            tp[x, y - y0] = (r, g, b)
    return tex


TRANSFORMS = [(math.pi, 1), (math.pi / 3, 1), (-math.pi / 3, 1), (2 * math.pi / 3, 1), (-2 * math.pi / 3, 1),
              (0.0, -1), (math.pi, -1), (math.pi / 3, -1), (-math.pi / 3, -1)]   # (rotation, mirror-x)


def _tf(x, y, rot, mir):
    x = x * mir
    c, s = math.cos(rot), math.sin(rot)
    return c * x - s * y, s * x + c * y


def clone_stone(can, gold_m, new_band):
    """Fill the old bands with his own stone from a rotated / mirrored copy of the tile (the hex's symmetries keep every
    point inside the hex). Each connected hole takes the one transform that lands most of it on stone; a dark mortar
    line is drawn round each fill, so it reads as a plate edge."""
    src = can.load()
    gm, nb = gold_m.load(), new_band.load()
    hole = Image.new('L', (N, N), 0)
    hp = hole.load()
    for y in range(N):
        for x in range(N):
            if gm[x, y] and not nb[x, y]:
                hp[x, y] = 255
    # connected components (4-neighbour)
    seen = set()
    comps = []
    for y in range(N):
        for x in range(N):
            if hp[x, y] and (x, y) not in seen:
                comp = [(x, y)]
                seen.add((x, y))
                i = 0
                while i < len(comp):
                    cx, cy = comp[i]
                    i += 1
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        sx, sy = cx + dx, cy + dy
                        if 0 <= sx < N and 0 <= sy < N and hp[sx, sy] and (sx, sy) not in seen:
                            seen.add((sx, sy))
                            comp.append((sx, sy))
                comps.append(comp)

    filled_now = set()

    def source(x, y, tf):
        hx, hy = to_hex(x, y)
        tx, ty = _tf(hx, hy, *tf)
        X, Y = to_px(tx, ty)
        X, Y = int(X), int(Y)
        if 0 <= X < N and 0 <= Y < N and not gm[X, Y] and src[X, Y][3] > 200 and inside(tx, ty, -0.02):
            return src[X, Y]
        return None
    out = can.copy()
    dst = out.load()
    left = []
    for comp in comps:
        sample = comp[::max(1, len(comp) // 400)]
        ranked = sorted(TRANSFORMS, key=lambda tf: -sum(1 for p in sample if source(*p, tf)))
        for x, y in comp:
            for tf in ranked:
                v = source(x, y, tf)
                if v:
                    dst[x, y] = v
                    filled_now.add((x, y))
                    break
            else:
                left.append((x, y))
    # fallback (e.g. at the hex centre, where every symmetry lands on a band): grow the filled stone inward
    todo = set(left)
    while todo:
        done = []
        for x, y in todo:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2)):
                sx, sy = x + dx, y + dy
                if 0 <= sx < N and 0 <= sy < N and (sx, sy) not in todo and (not gm[sx, sy] or not hp[sx, sy]
                                                                             or (sx, sy) in filled_now):
                    if gm[sx, sy] and hp[sx, sy] and (sx, sy) not in filled_now:
                        continue
                    if nb[sx, sy]:
                        continue
                    dst[x, y] = dst[sx, sy]
                    done.append((x, y))
                    break
        if not done:
            break
        for p in done:
            todo.discard(p)
            filled_now.add(p)
    # mortar line round each fill
    edge = hole.filter(ImageFilter.MaxFilter(3))
    ep = edge.load()
    for y in range(N):
        for x in range(N):
            if ep[x, y] and not hp[x, y] and not nb[x, y]:
                r, g, b, a = dst[x, y]
                dst[x, y] = (int(r * 0.35) + 10, int(g * 0.3), int(b * 0.3), a)
    return out


def build(gold_scale=1.0):
    can = load_canvas()
    src = can.load()
    gm = Image.new('L', (N, N), 0)
    gmp = gm.load()
    for y in range(N):
        for x in range(N):
            if is_gold(src[x, y]):
                gmp[x, y] = 255
    gm = gm.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(19))
    # (closed, then grown 9 px: the old bands with their dark outlines and cast shadows)
    paths = layout()
    segs, grid, G = dist_field(paths)
    tex = gold_texture(can)
    tw, th = tex.size
    tp = tex.load()
    band = Image.new('L', (N, N), 0)
    core = Image.new('L', (N, N), 0)          # the band itself (no shadow): the stone fill skips only this
    rail = Image.new('L', (N, N), 0)
    chan = Image.new('L', (N, N), 0)
    info = {}
    bp, rp, cp, corep = band.load(), rail.load(), chan.load(), core.load()
    for y in range(N):
        for x in range(N):
            hx, hy = to_hex(x, y)
            if not inside(hx, hy, 0.05):
                continue
            nb = nearest(grid, G, hx, hy)
            if nb is None:
                continue
            d, s, side, name, tvec = nb
            if d <= HALF + OUTLINE + 0.022:
                bp[x, y] = 255
                info[(x, y)] = nb
                if d <= HALF + OUTLINE:
                    corep[x, y] = 255
    out = clone_stone(can, gm, core)
    op = out.load()
    for (x, y), (d, s, side, name, tvec) in info.items():
        r, g, b, a = op[x, y]
        if d > HALF + OUTLINE:                           # the cast shadow round the band
            f = 0.45 + 0.55 * (d - HALF - OUTLINE) / 0.022
            op[x, y] = (int(r * f), int(g * f), int(b * f), a)
            continue
        if d > HALF:                                      # the dark bevel outline
            op[x, y] = (28, 16, 8, a)
            continue
        ph = s % CAP
        if ph < 0.010:                                    # his segment cap: a dark joint across the band
            op[x, y] = (30, 17, 8, a)
            rp[x, y] = 255
            continue
        if d < GROOVE / 2:                                # the groove between the rails
            op[x, y] = (34, 20, 10, a)
            cp[x, y] = 255
            continue
        # a rail: across 0 (groove side) .. 1 (outer edge); mirror so both rails share the profile; his strip
        # runs dark-bright-dark across, so map across to the strip's columns and arc length to its rows
        across = (d - GROOVE / 2) / RAIL
        tx = min(tw - 1, int(across * (tw - 1)))
        ty = int((s / (PX * 1.0)) * 0.9) % (2 * th)
        ty = ty if ty < th else 2 * th - 1 - ty              # mirror-repeat along the band
        cr, cg, cb = tp[tx, ty]
        k = gold_scale
        # his bevel: the rail's outer edge catches the light where it faces the upper left, falls dark where it
        # faces away; its inner edge (by the groove) sits a step darker; the joint behind each cap catches light
        nx, ny = -tvec[1] * side, tvec[0] * side
        lit = nx * LIGHT[0] + ny * LIGHT[1]
        if across > 0.72:
            k *= 1.0 + 0.32 * lit if lit > 0 else 1.0 + 0.40 * lit
        elif across < 0.18:
            k *= 0.78
        if 0.010 <= ph < 0.019:
            k *= 1.3
        op[x, y] = (min(255, int(cr * k)), min(255, int(cg * k)), min(255, int(cb * k)), a)
        rp[x, y] = 255
    crack = Image.new('L', (N, N), 0)
    kp = crack.load()
    for y in range(N):
        for x in range(N):
            r, g, b, a = op[x, y]
            if a > 200 and r > 70 and r > 1.8 * g and r > 1.8 * b and not rp[x, y]:
                kp[x, y] = 255                       # his red mortar glow
    # QA r5: his red veins must survive the 50 px rendition (ref a reads red-veined; RUL-125 names the red cracks).
    # Widen each glowing joint to ~16 source px (0.8 px at 50) along the dark mortar it sits in, in his red
    # (ref a mean #7f0302), with a hotter core, never over a band or its outline.
    grow = crack.filter(ImageFilter.MaxFilter(17))
    gp_ = grow.load()
    core_m = crack.filter(ImageFilter.MaxFilter(7)).load()
    for y in range(N):
        for x in range(N):
            if not gp_[x, y] or rp[x, y] or bp[x, y]:
                continue
            r, g, b, a = op[x, y]
            if r + g + b > 150 and not kp[x, y]:      # stone face, not mortar: leave it
                continue
            op[x, y] = (172, 14, 6, a) if core_m[x, y] else (132, 6, 3, a)
            kp[x, y] = 255
    return can, out, rail, chan, crack


def edge_dist(x, y):
    """Distance to the hex boundary and the nearest edge's inward normal (regular flat-top hex)."""
    best = None
    for k in range(6):
        a = math.radians(60 * k + 30)
        nx, ny = math.cos(a), math.sin(a)                 # outward normal of edge k
        d = H - (x * nx + y * ny)
        if best is None or d < best[0]:
            best = (d, -nx, -ny)
    return best


def finalize(out):
    """Bleed and rim (QA r4 B1): every pixel within BLEED past the hex edge takes the content of the neighbouring hex
    (the same tile, so it is the exact continuation); his dark rim is replaced by repeating the pixels RIM in from
    each edge, so bands run unbroken across the seam; alpha is 255 throughout."""
    import floor as FL
    src = out.load()
    fin = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    fp = fin.load()
    for py in range(N):
        for px in range(N):
            x, y = to_hex(px, py)
            if not inside(x, y, BLEED):
                continue
            lx, ly = FL.reduce(x, y)
            d, nx, ny = edge_dist(lx, ly)
            if d < RIM:
                lx, ly = lx + nx * (RIM - d), ly + ny * (RIM - d)
            X, Y = to_px(lx, ly)
            r, g, b, _ = src[min(N - 1, max(0, int(X))), min(N - 1, max(0, int(Y)))]
            fp[px, py] = (r, g, b, 255)
    return fin


def tile(size=128, gold_scale=1.0, colours=96):
    """The export: the finished canvas reduced to the delivery size (box filter), alpha 255 inside the bleed, and
    reduced to a palette (lossless WebP stores <= 256 colours as a palette, so the floor loads small)."""
    _, out, rail, chan, crack = build(gold_scale)
    fin = finalize(out)
    small = fin.convert('RGBa').resize((size, size), Image.BOX).convert('RGBA')
    a = small.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    q = small.convert('RGB').quantize(colors=colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    small = q.convert('RGB').convert('RGBA')
    small.putalpha(a)
    return small, fin, rail, chan, crack


def crossings(rail_m, inset=0.03):
    gm = rail_m.load()
    res = {}
    for k in range(6):
        (x1, y1), (x2, y2) = C[k], C[(k + 1) % 6]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        nl = math.hypot(mx, my)
        nx, ny = -mx / nl, -my / nl
        runs, cur = [], None
        S = 1200
        for i in range(S + 1):
            u = i / S
            X, Y = to_px(x1 + (x2 - x1) * u + nx * inset, y1 + (y2 - y1) * u + ny * inset)
            g = gm[min(N - 1, int(X)), min(N - 1, int(Y))]
            if g and cur is None:
                cur = u
            if not g and cur is not None:
                runs.append([cur, u])
                cur = None
        merged = []
        for r in runs:
            if merged and r[0] - merged[-1][1] < 0.04:
                merged[-1][1] = r[1]
            else:
                merged.append(r)
        res[k] = [(round((a + b) / 2, 3), round(b - a, 3)) for a, b in merged if b - a > 0.01]
    return res


if __name__ == '__main__':
    print('join check (layout):', check_joins() or 'all ends paired')
    can, out, rail, chan, crack = build()
    cache = os.path.join(HERE, '.cache')                 # build intermediates, not delivered
    os.makedirs(cache, exist_ok=True)
    finalize(out).save(os.path.join(cache, 'classic_1024.png'))
    print('rail crossings (centre, width) per edge:', crossings(rail))
