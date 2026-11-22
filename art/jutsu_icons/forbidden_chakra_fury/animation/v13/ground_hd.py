"""HD chakra-fracture floor for FCF v13 (2026-11-21).

Director on v12: the ground webs "look like they come from a 90s game"; wanted a high-definition modern look.
What changes from v12's floor (six even strokes):
- a fracture hierarchy: main fractures from the six edge midpoints to inner junctions, secondary fractures entering at
  the edge quarter points and joining the mains, then two levels of fine branching that stay inside the hex. Every
  edge crossing sits at a point the mirrored and the neighbouring tile share, so the web continues across tiles;
- each fracture is drawn in layers: a dark gap with a lit lip (matter), a hot core whose width and brightness vary
  along its length with breaks, a tight glow, and wide light pooling on the ground squashed 2:1 to the board;
- energy pulses run along the fractures (edge to centre, so the charge arrives from the neighbour) and short arcs
  jump between fracture points above the ground;
- drawn at 4x and reduced to the delivered size.
"""
import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import fxlight as L

SS = L.SS


def hex_pts(cx, cy, h):
    w = 2 * h
    return [(cx - w / 2, cy), (cx - w / 4, cy - h / 2), (cx + w / 4, cy - h / 2), (cx + w / 2, cy),
            (cx + w / 4, cy + h / 2), (cx - w / 4, cy + h / 2)]


def inside(p, cx, cy, h, inset=0.9):
    x, y = (p[0] - cx) / (h * inset), (p[1] - cy) / (h * inset)
    # flat-top hex of half width 1 (x) and half height 0.5 (y)
    return abs(y) <= 0.5 and abs(x) + abs(y) <= 1.0


def angular(a, b, rnd, amp=0.3, fine=0.06):
    """A fissure path: a few sharp turns, then fine grit along each straight run."""
    coarse = L.jag(a, b, amp, rnd, 3)
    out = [coarse[0]]
    for p, q in zip(coarse, coarse[1:]):
        out += L.jag(p, q, fine * 6, rnd, 3)[1:]
    return out


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def length(pts):
    return sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts, pts[1:]))


class Crack:
    __slots__ = ("pts", "w", "val", "level", "breaks")

    def __init__(self, pts, w, val, level, rnd):
        self.pts, self.w, self.val, self.level = pts, w, val, level
        # breaks: segment indices where the glowing core is interrupted (the gap stays)
        n = len(pts) - 1
        self.breaks = set()
        i = 0
        while i < n:                                  # a few longer breaks, not beads
            if rnd.random() < 0.012 * (1 + level) and level > 0:
                self.breaks.update(range(i, i + rnd.randrange(2, 5)))
                i += 5
            i += 1


def network(seed, cx, cy, h):
    rnd = random.Random(seed)
    P = hex_pts(cx, cy, h)
    edges = [(P[i], P[(i + 1) % 6]) for i in range(6)]
    mids = [lerp(a, b, 0.5) for a, b in edges]
    quarters = [lerp(a, b, t) for a, b in edges for t in (0.22, 0.78)]
    # level 0: fractures run THROUGH the tile, midpoint to midpoint, each midpoint used once, so across the field
    # they join into long winding fracture lines instead of a star per tile
    pairings = [((0, 3), (1, 2), (4, 5)), ((1, 4), (2, 3), (5, 0)), ((2, 5), (0, 1), (3, 4))]
    cracks = []
    for a, b in pairings[seed % 3]:
        A, B = mids[a], mids[b]
        mid = lerp(A, B, 0.5)
        bend = lerp(mid, (cx, cy), rnd.uniform(-0.25, 0.35))    # bow away from (or toward) the centre a little
        path = angular(A, bend, rnd, 0.3) + angular(bend, B, rnd, 0.3)[1:]
        cracks.append(Crack(path, 4.2, 255, 0, rnd))
    mains = list(cracks)
    for _ in range(4):                                        # level 1: secondary fractures between the mains
        a, b = rnd.sample(mains, 2)
        pa = a.pts[rnd.randrange(len(a.pts) // 3, len(a.pts) - 2)]
        pb = b.pts[rnd.randrange(len(b.pts) // 3, len(b.pts) - 2)]
        if math.hypot(pa[0] - pb[0], pa[1] - pb[1]) < 0.9 * h:
            cracks.append(Crack(angular(pa, pb, rnd, 0.35), 2.4, 215, 1, rnd))
    for level, (count, ln, w, val) in enumerate(((8, 0.18, 0.9, 160), (8, 0.09, 0.5, 115)), start=2):
        parents = [c for c in cracks if c.level == level - 2 or c.level == level - 1]
        for _ in range(count):                                # levels 2-3: fine branching, kept inside the hex
            par = rnd.choice(parents)
            i = rnd.randrange(1, len(par.pts) - 1)
            p, q = par.pts[i - 1], par.pts[i]
            tang = math.atan2(q[1] - p[1], q[0] - p[0])
            a = tang + rnd.choice((-1, 1)) * rnd.uniform(0.3, 0.8)
            L_ = ln * h * 2 * rnd.uniform(0.6, 1.3)
            end = (q[0] + math.cos(a) * L_, q[1] + math.sin(a) * L_ * 0.55)
            path = angular(q, end, rnd, 0.35, 0.08)
            cut = next((k for k, pt in enumerate(path) if not inside(pt, cx, cy, h)), len(path))
            if cut >= 3:
                cracks.append(Crack(path[:cut], w, val, level, rnd))
    return cracks


def squashed_blur(img, r):
    """Blur wider than tall: light pooling on the 2:1 board."""
    w, h = img.size
    small = img.resize((w, h // 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(r))
    return small.resize((w, h), Image.BILINEAR)


def fissure_poly(pts, widths):
    left, right = [], []
    for k, p in enumerate(pts):
        a = pts[max(0, k - 1)]
        b = pts[min(len(pts) - 1, k + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[k] / 2
        left.append(((p[0] + nx * w) * SS, (p[1] + ny * w) * SS))
        right.append(((p[0] - nx * w) * SS, (p[1] - ny * w) * SS))
    return left + right[::-1]


def draw_core(dl, crack, heat, grow, rnd, flicker):
    """A fracture's light as a true fissure: a filled shape that swells and pinches along its length (full width at the
    tile edges, where it continues into the neighbour), with a white-hot filament inside. Branches taper to points."""
    pts = crack.pts
    n = max(2, int(round(len(pts) * grow)))
    pts = pts[:n]
    total = max(1, len(crack.pts) - 1)
    ph = (crack.val * 0.37) % 6.28
    widths = []
    for k in range(len(pts)):
        t = k / total
        if crack.level < 2:
            swell = 0.55 + 0.45 * abs(math.sin(t * 9.0 + ph)) * math.sin(math.pi * t) + 0.25 * (1 - math.sin(math.pi * t))
        else:
            swell = (1 - t) ** 1.2
        widths.append(max(0.3, crack.w * swell))
    v = int(min(255, crack.val * heat * 0.7))
    dl.polygon(fissure_poly(pts, widths), fill=v)
    fil = [(p[0] * SS, p[1] * SS) for p in pts]
    dl.line(fil, fill=int(min(255, crack.val * heat)), width=max(1, int(min(widths) * 0.0 + crack.w * 0.28 * SS)),
            joint="curve")


def pulses(dl, cracks, phase, heat):
    """Bright packets running along the main and secondary fractures, edge to centre."""
    for k, c in enumerate(cracks):
        if c.level > 1:
            continue
        pts = c.pts
        u = (phase * (1.4 if c.level else 1.0) + k * 0.37) % 1.0
        i = int(u * (len(pts) - 1))
        for j in range(max(0, i - 4), min(len(pts) - 1, i + 1)):
            fade = 1 - (i - j) / 5
            p, q = pts[j], pts[j + 1]
            dl.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=int(255 * heat * fade),
                    width=int((c.w + 1.2) * SS))


def arcs(dl, cracks, rnd, heat, n=3):
    """Short arcs jumping between nearby fracture points, lifted a little off the ground."""
    pool = [p for c in cracks if c.level <= 1 for p in c.pts[::3]]
    for _ in range(n):
        a = rnd.choice(pool)
        near = [p for p in pool if 6 < math.hypot(p[0] - a[0], p[1] - a[1]) < 22]
        if not near:
            continue
        b = rnd.choice(near)
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - rnd.uniform(3, 8))
        path = L.jag(a, mid, 0.5, rnd, 3) + L.jag(mid, b, 0.5, rnd, 3)[1:]
        dl.line([(x * SS, y * SS) for x, y in path], fill=int(240 * heat), width=max(1, int(0.8 * SS)))


def floor_frame(n, cracks, cx, cy, h, heat, grow, phase, rnd, arc_n=0, veil=0.0):
    W = n * SS
    core = Image.new("L", (W, W), 0)
    dl = ImageDraw.Draw(core)
    gap = Image.new("L", (W, W), 0)
    dg = ImageDraw.Draw(gap)
    if veil:
        ImageDraw.Draw(core).polygon([(x * SS, y * SS) for x, y in hex_pts(cx, cy, h)], fill=int(255 * veil))
    for c in cracks:
        g = grow if c.level == 0 else max(0.0, (grow - 0.25 * c.level) / (1 - 0.25 * c.level))
        if g <= 0:
            continue
        m = max(2, int(round(len(c.pts) * g)))
        dg.line([(x * SS, y * SS) for x, y in c.pts[:m]], fill=255, width=max(1, int((c.w + 0.8) * SS)))
        draw_core(dl, c, heat, g, rnd, flicker=1.0)
    if phase is not None and heat > 0.2:
        pulses(dl, cracks, phase, heat)
    if arc_n:
        arcs(dl, cracks, rnd, heat, arc_n)
    # matter: the dark gap with a faint lit lip
    gap_soft = gap.filter(ImageFilter.GaussianBlur(0.8 * SS))
    dark = Image.new("RGBA", (W, W), (10, 4, 18, 0))
    dark.putalpha(gap_soft.point(lambda v: int(v * 0.5 * min(1, 0.4 + grow))))
    # light: core + tight glow + wide pooling on the ground
    tight = core.filter(ImageFilter.GaussianBlur(1.8 * SS)).point(lambda v: min(255, int(v * 1.9)))
    mid = core.filter(ImageFilter.GaussianBlur(5 * SS)).point(lambda v: min(255, int(v * 1.5)))
    pool = squashed_blur(core, 12 * SS).point(lambda v: min(255, int(v * 1.5)))
    inten = ImageChops.lighter(ImageChops.lighter(core, tight), ImageChops.lighter(mid, pool))
    inten = inten.resize((n, n), Image.LANCZOS)
    rgb = Image.merge("RGB", [inten.point([c[i] for c in L.STORM_LUT]) for i in range(3)])
    alpha = inten.point(lambda v: min(255, int(255 * (v / 255) ** 0.75 * 1.1)))
    light = rgb.convert("RGBA")
    light.putalpha(alpha)
    out = dark.resize((n, n), Image.LANCZOS)
    out.alpha_composite(light)
    return out


def floor_frames(seed, n=168):
    h = n / 2
    c = n / 2
    cracks = network(seed, c, c, h)
    rnd = random.Random(seed + 9)
    plan = [  # (veil, grow, heat, pulse phase, arcs)
        (0.12, 0.0, 0.0, None, 0), (0.05, 0.15, 1.0, None, 0), (0.0, 0.45, 1.0, None, 0), (0.0, 0.75, 1.0, None, 1),
        (0.0, 1.0, 1.0, 0.0, 2), (0.0, 1.0, 0.95, 0.18, 3), (0.0, 1.0, 0.85, 0.36, 2), (0.0, 1.0, 0.9, 0.54, 3),
        (0.0, 1.0, 0.78, 0.72, 2), (0.0, 1.0, 0.7, 0.9, 1), (0.0, 1.0, 0.6, 0.08, 1), (0.0, 1.0, 0.5, 0.26, 0),
        (0.0, 1.0, 0.4, None, 0), (0.0, 1.0, 0.3, None, 0), (0.0, 1.0, 0.18, None, 0), (0.0, 1.0, 0.08, None, 0)]
    return [floor_frame(n, cracks, c, c, h, heat, grow, ph, rnd, an, veil) for veil, grow, heat, ph, an in plan]


# ------------------------------------------------------------------------------------- HD ground lightning
def hd_bolt(dl, a, b, rnd, w=2.2, val=255, flat=0.5, branches=4, depth_amp=0.32):
    """A modern lightning arc along the ground: a jagged main channel that tapers, a second thinner strand that
    wanders off and rejoins it, and branches that fork twice, each fading and thinning toward its tip."""
    def channel(p, q, amp, d=6):
        pts = L.jag(p, q, amp, rnd, d)
        return [(x, p[1] + (y - p[1]) * 1.0) for x, y in pts]

    def tapered(pts, w0, w1, v0, v1):
        n = len(pts)
        for i, (p, q) in enumerate(zip(pts, pts[1:])):
            t = i / max(1, n - 2)
            ww = w0 + (w1 - w0) * t
            dl.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=int(v0 + (v1 - v0) * t),
                    width=max(1, int(ww * SS)))

    main = channel(a, b, depth_amp)
    # flatten onto the ground plane around the arc's own baseline
    cy = (a[1] + b[1]) / 2
    main = [(x, cy + (y - cy) * flat) if i not in (0, len(main) - 1) else (x, y) for i, (x, y) in enumerate(main)]
    mid_w = w
    tapered(main[: len(main) // 2 + 1], w * 0.7, mid_w, val * 0.85, val)
    tapered(main[len(main) // 2:], mid_w, w * 0.5, val, val * 0.8)
    # second strand
    i0, i1 = sorted(rnd.sample(range(4, len(main) - 4), 2))
    if i1 - i0 > 6:
        strand = channel(main[i0], main[i1], 0.5, 4)
        tapered(strand, w * 0.35, w * 0.35, val * 0.7, val * 0.7)
    for _ in range(branches):
        i = rnd.randrange(3, len(main) - 3)
        p, q = main[i - 1], main[i]
        tang = math.atan2(q[1] - p[1], q[0] - p[0])
        ang = tang + rnd.choice((-1, 1)) * rnd.uniform(0.35, 0.9)
        ln = math.hypot(b[0] - a[0], b[1] - a[1]) * rnd.uniform(0.2, 0.4)
        end = (q[0] + math.cos(ang) * ln, q[1] + math.sin(ang) * ln * flat)
        br = L.jag(q, end, 0.45, rnd, 5)
        tapered(br, w * 0.55, 0.2, val * 0.8, val * 0.15)
        k = rnd.randrange(len(br) // 3, len(br) - 2)
        p2, q2 = br[k - 1], br[k]
        t2 = math.atan2(q2[1] - p2[1], q2[0] - p2[0]) + rnd.choice((-1, 1)) * rnd.uniform(0.4, 0.9)
        end2 = (q2[0] + math.cos(t2) * ln * 0.45, q2[1] + math.sin(t2) * ln * 0.45 * flat)
        tapered(L.jag(q2, end2, 0.5, rnd, 4), w * 0.3, 0.15, val * 0.6, val * 0.1)


def ground_storm_frame(n, cracks, cx, cy, h, heat, arcs_spec, fissure_heat, veil=0.0):
    """arcs_spec: list of (a, b, seed, w) arcs to draw this frame."""
    W = n * SS
    core = Image.new("L", (W, W), 0)
    dl = ImageDraw.Draw(core)
    if veil:
        dl.polygon([(x * SS, y * SS) for x, y in hex_pts(cx, cy, h)], fill=int(255 * veil))
    # dim fissures: wide soft body, no white
    fis = Image.new("L", (W, W), 0)
    df = ImageDraw.Draw(fis)
    for c in cracks:
        if c.level <= 1 and fissure_heat > 0:
            df.line([(x * SS, y * SS) for x, y in c.pts], fill=int(150 * fissure_heat), width=int(c.w * 0.6 * SS),
                    joint="curve")
    for a, b, seed, w in arcs_spec:
        hd_bolt(dl, a, b, random.Random(seed), w=w, val=255 * heat)
    tight = core.filter(ImageFilter.GaussianBlur(1.2 * SS)).point(lambda v: min(255, int(v * 1.7)))
    mid = core.filter(ImageFilter.GaussianBlur(4 * SS)).point(lambda v: min(255, int(v * 1.2)))
    pool = squashed_blur(ImageChops.lighter(core, fis), 12 * SS).point(lambda v: min(255, int(v * 1.6)))
    fsoft = fis.filter(ImageFilter.GaussianBlur(1.5 * SS))
    inten = ImageChops.lighter(ImageChops.lighter(core, tight), ImageChops.lighter(mid, ImageChops.lighter(pool, fsoft)))
    inten = inten.resize((n, n), Image.LANCZOS)
    rgb = Image.merge("RGB", [inten.point([c[i] for c in L.STORM_LUT]) for i in range(3)])
    alpha = inten.point(lambda v: min(255, int(255 * (v / 255) ** 0.75 * 1.1)))
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def ground_storm_frames(seed, n=168):
    h = n / 2
    c = n / 2
    cracks = network(seed, c, c, h)
    rnd = random.Random(seed * 3 + 1)

    def rand_pt():
        while True:
            p = (c + rnd.uniform(-0.85, 0.85) * h, c + rnd.uniform(-0.42, 0.42) * h)
            if inside(p, c, c, h, 0.88):
                return p

    def new_arc(w):
        a = rand_pt()
        for _ in range(30):
            b = rand_pt()
            if 0.55 * h < math.hypot(b[0] - a[0], (b[1] - a[1]) * 2) < 1.4 * h:
                break
        return [a, b, rnd.randrange(1 << 30), w]

    live = []
    plan = [  # (veil, heat, new arcs this frame, fissure heat)
        (0.12, 0, 0, 0.0), (0.05, 1.0, 2, 0.3), (0, 1.0, 2, 0.6), (0, 1.0, 1, 0.8), (0, 0.95, 2, 0.9), (0, 0.9, 1, 0.9),
        (0, 0.95, 2, 0.85), (0, 0.85, 1, 0.8), (0, 0.85, 2, 0.75), (0, 0.75, 1, 0.65), (0, 0.65, 1, 0.55),
        (0, 0.55, 1, 0.45), (0, 0.45, 0, 0.35), (0, 0.35, 0, 0.25), (0, 0.2, 0, 0.15), (0, 0.0, 0, 0.06)]
    out = []
    for veil, heat, k, fh in plan:
        live = [a for a in live if a[4] > 0]
        for _ in range(k):
            live.append(new_arc(rnd.uniform(1.6, 2.6)) + [2])
        spec = []
        for arc in live:
            spec.append((arc[0], arc[1], arc[2] + arc[4], arc[3] * (0.75 if arc[4] == 1 else 1.0)))
            arc[4] -= 1
        out.append(ground_storm_frame(n, cracks, c, c, h, heat, spec, fh, veil))
    return out
