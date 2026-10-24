#!/usr/bin/env python3
"""Assemble the Ethereal Rebirth cast animation from the art director's layers (route A, the Chakra Overflow method).

    python3 art/jutsu_icons/ethereal_rebirth/animation/build_strip.py [--frames 40] [--ms 60] [--size 128]

Inputs: layers/anim_er_*.png (cut from the delivered sheet by extract_layers.py). Each painted ribbon (R1 gold, R2 blue)
is bent along a rising, widening helix around the avatar by placing thin slices of the straight painting along the path;
one drawing per ribbon moves on continuous curves for the whole run (the Chakra Overflow smoothness lesson).

The wrap rule (the game draws the sprite over the avatar, libs/threejs/combat.ts): far-side slices are dimmer and thinner
and are hidden inside the token window; near-side slices cross the token, see-through at face height. Token geometry is
Chakra Overflow's measurement: centre 0.283 of the frame from the top, radius 0.248.

Outputs: exports/anim_ethereal_rebirth_v1.webp (vertical strip of square frames, lossless), and in
docs/design/ethereal_rebirth_animation/: v1_frames.png, v1_preview.gif (128 and 50 px over dark, grass and snow with a
stand-in token). Pillow only.
"""
import argparse
import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DOCS = os.path.join(ROOT, 'docs', 'design', 'ethereal_rebirth_animation')
S = 384                                   # working size
TOKEN_CY, TOKEN_R = 0.283, 0.248
WINDOW_R = 0.96 * TOKEN_R
FACE_Y = (TOKEN_CY - 0.17, TOKEN_CY + 0.09)
CORE = (0.5, TOKEN_CY + 0.16)
THICK = 0.15                              # on-screen height of a straightened ribbon (incl. its wisps), frame fraction
SLICES = 70


# The portrait's real outer edge is its dark outline, outside the white ring. Measured by hand from brightness
# profiles of the director's battle recording (2026-10-24): centre (206, 181.6), radius 28.6 px, i.e. 0.296 of the frame
# from the top and 0.272 of the frame. The earlier mask (0.283 / 0.254) followed the white ring and stopped about
# 2.5 px short at the bottom, which is where the gold ribbon kept showing. Mask = real edge + about 1.5 px.
PORTRAIT_CY = 0.296
PORTRAIT_R = 0.287


def _behind_mask(radius=None):
    """Alpha mask for everything behind the user: 0 inside the avatar portrait and its rank star (soft 1 px edge), 255
    outside."""
    m = Image.new('L', (S * 4, S * 4), 255)
    k = S * 4
    r, cx, cy = (radius or PORTRAIT_R) * k, 0.5 * k, PORTRAIT_CY * k
    d = ImageDraw.Draw(m)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    # the rank star and its mount hang below the portrait (measured from the director's battle recording: the star
    # spans x 0.47-0.54, y 0.57-0.63 of the frame); cover x 0.5 +/- 0.07 down to y 0.67 with rounded corners
    d.rounded_rectangle([cx - 0.07 * k, (TOKEN_CY + 0.15) * k, cx + 0.07 * k, 0.67 * k], radius=0.03 * k, fill=0)
    return m.resize((S, S), Image.LANCZOS)


BEHIND_MASK = _behind_mask()


def _edge_fade(w=0.07):
    """Alpha ramp over the outer `w` of the frame on every side (the game clips the sprite at its square)."""
    ramp = [int(255 * (lambda x: x * x * (3 - 2 * x))(min(1.0, min(i, S - 1 - i) / (w * S)))) for i in range(S)]
    h = Image.new('L', (S, 1)); h.putdata(ramp)
    v = Image.new('L', (1, S)); v.putdata(ramp)
    return ImageChops.multiply(h.resize((S, S)), v.resize((S, S)))


EDGE_FADE = _edge_fade()


SET = 'v1'


def L(name):
    """v1: layers cut from the first sheet (layers/). v2: the art director's transparent raws (raws/anim_er_v2_*),
    cropped to their content."""
    if SET in ('v5', 'loop1', 'hit1') and name != 'C1_core':
        # v5: the art director's bands and sparkles in the icon's style (raws/anim_er_v5_*); variant a is the flatter one
        fn = {'R1_ribbon_gold': 'R1_band_gold_a', 'R2_ribbon_blue': 'R2_band_blue_a', 'F1_flecks': 'S1_sparkles'}[name]
        im = Image.open(os.path.join(HERE, 'raws', f'anim_er_v5_{fn}.png')).convert('RGBA')
        return im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    src = 'v1' if (SET == 'v1' or (SET in ('v3', 'v4', 'v5') and name == 'C1_core')) else 'v2'
    if src == 'v1':
        return Image.open(os.path.join(HERE, 'layers', f'anim_er_{name}.png')).convert('RGBA')
    im = Image.open(os.path.join(HERE, 'raws', f'anim_er_{src}_{name}.png')).convert('RGBA')
    return im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())


def straighten(strip, win=41):
    """The painted ribbons wave along their length; bent along a curve that wave reads as a braided rope. Shift each
    column so the ribbon's (smoothed) alpha centre line is straight, then crop to the content."""
    w, h = strip.size
    a = strip.getchannel('A').load()
    cy = []
    for x in range(w):
        tot = sum(a[x, y] for y in range(h))
        cy.append(sum(y * a[x, y] for y in range(h)) / tot if tot > 200 else None)
    known = [(x, c) for x, c in enumerate(cy) if c is not None]
    for x in range(w):                                  # fill gaps with the nearest known centre
        if cy[x] is None:
            cy[x] = min(known, key=lambda k: abs(k[0] - x))[1]
    sm = [sum(cy[max(0, x - win // 2):x + win // 2 + 1]) / len(cy[max(0, x - win // 2):x + win // 2 + 1]) for x in range(w)]
    out = Image.new('RGBA', (w, h * 2), (0, 0, 0, 0))
    for x in range(w):
        col = strip.crop((x, 0, x + 1, h))
        out.paste(col, (x, int(h - sm[x])))
    return out.crop(out.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox())


def ease(t):
    return t * t * (3 - 2 * t)


def seg(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


def in_window(x, y):
    return math.hypot(x - 0.5, y - TOKEN_CY) < WINDOW_R


def lighter(dst, src):
    """Light-like merge: per-channel maximum of colour and alpha (overlapping slices do not stack into seams)."""
    return Image.merge('RGBA', [ImageChops.lighter(a, b) for a, b in zip(dst.split(), src.split())])


def helix(phase, yc, a, b, length, pitch, n):
    pts = []
    for i in range(n + 1):
        u = i / n
        th = phase - u * length
        pts.append((0.5 + a * math.cos(th), yc + b * math.sin(th) + pitch * u, math.sin(th)))
    return pts


def _solve(A, B):
    """Gaussian elimination for the 8x8 perspective system."""
    n = len(B)
    M = [row[:] + [B[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[c][c]:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def perspective_coeffs(dst, src):
    """Coefficients for Image.transform(PERSPECTIVE): maps output points `dst` to input points `src`."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return _solve(A, B)


def smooth(v, a, b):
    return ease(seg(v, a, b))


def lay_ribbon(strip, pts, alpha, back, front, u0=0.0, u1=1.0, depth_rule=True, front_ok=1.0, face=True, twist=None,
               thick_k=1.0, no_face=False):
    """Warp the straight `strip` (its part u0..u1; the strip's right end is the ribbon's head) onto the path `pts`
    (head first) as a chain of quads that share their edges, so the ribbon bends without seams.

    `twist(u)` (v5) gives the band's roll angle along its length: the band narrows as cos(angle) goes to 0 (seen edge-on,
    it brightens to a pale line) and its back face (cos < 0) is drawn darker."""
    n = len(pts) - 1
    sw, sh = strip.size
    hw = THICK * S / 2 * thick_k
    roll = [twist(j / n) for j in range(n + 1)] if twist else None
    P = [(x * S, y * S) for x, y, _ in pts]
    D = [d for _, _, d in pts]
    normals = []
    for i in range(n + 1):
        ax, ay = P[max(0, i - 1)]
        bx, by = P[min(n, i + 1)]
        tx, ty = bx - ax, by - ay
        ln = math.hypot(tx, ty) or 1.0
        normals.append((-ty / ln, tx / ln))
    for i in range(n):
        mx, my = (P[i][0] + P[i + 1][0]) / 2 / S, (P[i][1] + P[i + 1][1]) / 2 / S
        depth = (D[i] + D[i + 1]) / 2 if depth_rule else 1.0
        nearness = smooth(depth, -0.25, 0.25)              # 0 far side, 1 near side, a soft crossover
        a = alpha * (0.55 + 0.45 * nearness)
        wf = nearness * front_ok if depth_rule else 1.0     # share drawn in front of the token; the rest goes behind
        if face and depth_rule and FACE_Y[0] < my < FACE_Y[1] and math.hypot(mx - 0.5, my - TOKEN_CY) < WINDOW_R:
            wf *= 0.30                                       # near side over the face: mostly see-through
        if no_face:
            # never in front of the face: over the upper portrait the band slides behind (under the mask), with a soft
            # change-over in height and at the rim, so it fades round the face instead of being cut
            above = 1 - smooth(my, PORTRAIT_CY - 0.01, PORTRAIT_CY + 0.07)
            inside = 1 - smooth(math.hypot(mx - 0.5, my - PORTRAIT_CY), PORTRAIT_R - 0.03, PORTRAIT_R + 0.04)
            wf *= 1 - above * inside
        a *= smooth(min(i, n - 1 - i), 0, 5)               # soft head and tail, never a square cut
        if a <= 0.01:
            continue
        thick = 0.7 + 0.3 * nearness
        tw = [1.0, 1.0]
        edge, backface = 0.0, False
        if roll:
            c0, c1 = math.cos(roll[i]), math.cos(roll[i + 1])
            tw = [max(0.16, abs(c0)), max(0.16, abs(c1))]
            edge = 1 - min(1.0, (abs(c0) + abs(c1)) / 2 / 0.45)    # 1 when edge-on
            backface = (c0 + c1) < 0
        quad = []
        for j, k in ((i, 0), (i + 1, 1)):
            nx, ny = normals[j]
            quad.append((P[j][0] + nx * hw * thick * tw[k], P[j][1] + ny * hw * thick * tw[k]))
        for j, k in ((i + 1, 1), (i, 0)):
            nx, ny = normals[j]
            quad.append((P[j][0] - nx * hw * thick * tw[k], P[j][1] - ny * hw * thick * tw[k]))
        # head first along the path; the strip's head is its right end
        sx_i = (u1 - (u1 - u0) * i / n) * (sw - 1)
        sx_j = (u1 - (u1 - u0) * (i + 1) / n) * (sw - 1)
        src = [(sx_i, 0), (sx_j, 0), (sx_j, sh - 1), (sx_i, sh - 1)]
        xs, ys = [q[0] for q in quad], [q[1] for q in quad]
        x0, y0 = int(math.floor(min(xs))) - 1, int(math.floor(min(ys))) - 1
        x1, y1 = int(math.ceil(max(xs))) + 1, int(math.ceil(max(ys))) + 1
        bw, bh = x1 - x0, y1 - y0
        if bw <= 0 or bh <= 0:
            continue
        local = [(qx - x0, qy - y0) for qx, qy in quad]
        try:
            co = perspective_coeffs(local, src)
        except ZeroDivisionError:
            continue
        piece = strip.transform((bw, bh), Image.PERSPECTIVE, co, Image.BILINEAR)
        if roll and (edge > 0.02 or backface):
            pa = piece.getchannel('A')
            rgb = piece.convert('RGB')
            if backface:                                     # the far face of the silk: a shade deeper
                rgb = Image.blend(rgb, ImageChops.multiply(rgb, Image.new('RGB', rgb.size, (185, 185, 185))), 0.5)
            if edge > 0.02:                                  # edge-on: folds to a bright, near-white line
                rgb = Image.blend(rgb, Image.new('RGB', rgb.size, (255, 252, 240)), 0.55 * edge)
                pa = pa.point(lambda v, e=edge: min(255, int(v * (1 + 0.6 * e))))
            piece = rgb.convert('RGBA')
            piece.putalpha(pa)
        mask = Image.new('L', (bw * 2, bh * 2), 0)
        ImageDraw.Draw(mask).polygon([(qx * 2, qy * 2) for qx, qy in local], fill=255)
        mask = mask.resize((bw, bh), Image.LANCZOS)
        base = ImageChops.multiply(piece.getchannel('A'), mask)
        for layer, share in ((front, wf), (back, 1 - wf)):
            if share * a <= 0.01:
                continue
            p2 = piece.copy()
            p2.putalpha(base.point(lambda v, k=a * share: int(v * k)))
            tile = Image.new('RGBA', layer.size, (0, 0, 0, 0))
            tile.paste(p2, (x0, y0))
            layer.paste(lighter(layer, tile))


LASH_T = 0.55                  # when the gold ribbon's head leaves the spin
SPIN_RATE = 2 * math.pi * 1.5  # radians of spin per unit time
TH_DEPART = 0.35               # helix angle at departure: front right, moving up and to the right


def spin_ribbons_v3(t, grow, rise, fade, gold, blue, back, front):
    """v3 motion: the spin runs the other way, and the gold ribbon's head peels off the spin at LASH_T and flies out of
    the frame along the departure tangent, its body following the same path (one continuous drawing, no second ribbon)."""
    if grow <= 0 or fade <= 0:
        return
    yc = 0.62 - 0.40 * rise
    a_r = 0.30 + 0.10 * grow
    b_r, pitch = 0.12, 0.28 * grow
    length = 0.5 + 3.0 * grow
    qd = SPIN_RATE * LASH_T
    front_ok = ease(seg(t, 0.45, 0.60))
    u0 = 1 - min(1.0, 0.25 + 0.75 * grow)

    def helix_pt(th, u):
        return (0.5 + a_r * math.cos(th), yc + b_r * math.sin(th) + pitch * u, math.sin(th))

    # departure point and direction (direction of motion for decreasing th, bent a little to the right)
    dx, dy = math.sin(TH_DEPART), -math.cos(TH_DEPART)
    dx, dy = dx + 0.35, dy
    ln = math.hypot(dx, dy)
    dx, dy = dx / ln, dy / ln
    for k, strip in enumerate((gold, blue)):
        phase0 = TH_DEPART + qd + k * math.pi
        qh = SPIN_RATE * t
        pts = []
        for i in range(SLICES + 1):
            u = i / SLICES
            q = qh - u * length
            if k == 0 and q > qd:
                px, py, _ = helix_pt(phase0 - qd, (qh - qd) / length)
                dist = (q - qd) * a_r * 1.15
                bend = 0.10 * dist * dist                 # the lash curls up as it flies (a whip, not a stick)
                pts.append((px + dx * dist + 0.25 * bend, py + dy * dist - bend, 1.0))
            else:
                pts.append(helix_pt(phase0 - q, u))
        al = 0.97 * fade
        if k == 0:
            al *= 1 - ease(seg(t, 0.82, 0.95))       # gone once it has left the frame
        lay_ribbon(strip, pts, al, back, front, u0=u0, u1=1.0, front_ok=front_ok)


def spin_ribbons_v4(t, grow, rise, fade, gold, blue, back, front):
    """v4 (director, 2026-10-24): the whole spin is centred on the portrait. Both ribbons start on the far side, behind
    the avatar, and orbit the portrait (axis through its centre), coming round in front; front passes draw over the
    portrait, back passes are hidden by the portrait mask (applied to the behind layer only). The spin rises from below
    the portrait's centre to above it. The gold ribbon leaves the orbit on the front right and lashes out of frame."""
    if grow <= 0 or fade <= 0:
        return
    pcy = PORTRAIT_CY
    yc = pcy + 0.12 - 0.22 * rise            # the orbit crosses the portrait's middle, rising from chest to brow
    a_r = 0.36 + 0.04 * grow                 # orbit wider than the portrait (radius 0.287) on both sides
    b_r, pitch = 0.14, 0.08 * grow
    length = 0.5 + 3.0 * grow
    td = 0.58                                 # gold departs at this time, on the front right (helix angle 0.35)
    th0 = {0: 0.35 + SPIN_RATE * td - 2 * math.pi}   # starts on the far right, behind the avatar
    th0[1] = th0[0] - 1.2                            # blue starts further round, also behind
    u0 = 1 - min(1.0, 0.25 + 0.75 * grow)

    def pt(th, u, dy=0.0):
        return (0.5 + a_r * math.cos(th), yc + dy + b_r * math.sin(th) + pitch * u, math.sin(th))

    dx, dy = math.sin(TH_DEPART) + 0.35, -math.cos(TH_DEPART)
    ln = math.hypot(dx, dy)
    dx, dy = dx / ln, dy / ln
    for k, strip in enumerate((gold, blue)):
        off = 0.0 if k == 0 else 0.05            # blue a little lower, so the two ribbons stack, not overlap
        thh = th0[k] - SPIN_RATE * t             # head angle; the spin runs towards decreasing angle
        pts = []
        for i in range(SLICES + 1):
            u = i / SLICES
            if k == 0 and t > td:
                # arc travelled since departure, measured in angle; the body behind it is still on the orbit
                gone = SPIN_RATE * (t - td) - u * length
                if gone > 0:
                    hx, hy, _ = pt(TH_DEPART, 0)
                    dist = gone * a_r * 1.15
                    bend = 0.10 * dist * dist
                    pts.append((hx + dx * dist + 0.25 * bend, hy + dy * dist - bend, 1.0))
                    continue
                pts.append(pt(TH_DEPART - gone, u))
            else:
                pts.append(pt(thh + u * length, u, off))
        al = 0.97 * fade
        if k == 0:
            al *= 1 - ease(seg(t, 0.85, 0.97))
        lay_ribbon(strip, pts, al, back, front, u0=u0, u1=1.0, front_ok=1.0, face=False)


# Timing (fluidity pass, director 2026-10-24: "very smooth ... transition from one to the next smoothly"). Both strips run
# at MS per frame; the game starts them on the same tick (combat.ts adds the appear and static animations in one pass),
# so cast frame f lines up with loop frame f. The loop phase at cast time t is t * HANDOFF_K.
MS, CAST_N, LOOP_N = 36, 66, 100
HANDOFF_K = (CAST_N - 1) / LOOP_N
# The loop's two bands (shared with the cast's hand-off): strip, lift, tilt, alpha, phase. Orbit: LOOP_A, LOOP_B radii.
LOOP_BANDS = [('gold_a', 0.07, -0.12, 0.60, 0.0), ('blue_a', -0.02, 0.15, 0.55, math.pi)]
LOOP_A, LOOP_B, LOOP_LEN, LOOP_THICK = 0.40, 0.15, 2.2, 0.85
HAND_T0, HAND_T1 = 0.60, 0.90   # the cast's blue band eases onto the loop's blue orbit over this part of the cast


def loop_angle(k, tl):
    return LOOP_BANDS[k][4] - 2 * math.pi * tl


def _blue_cast_angle(t, ph):
    """Head angle of the cast's blue band: spins at SPIN_RATE, then eases down to the loop's rate over HAND_T0..T1
    (integrated, so the slow-down has no jolt)."""
    w_l = 2 * math.pi * HANDOFF_K
    steps = 200
    acc, prev = 0.0, SPIN_RATE
    for i in range(1, steps + 1):
        s_ = t * i / steps
        w = SPIN_RATE + (w_l - SPIN_RATE) * ease(seg(s_, HAND_T0, HAND_T1))
        acc += (prev + w) / 2 * (t / steps)
        prev = w
    return ph - acc


def _blue_phase():
    """The cast's blue phase, chosen (within half a turn of the v5 design's) so that it arrives exactly on the loop's
    blue band when the hand-off ends."""
    ph0 = 0.35 + SPIN_RATE * 0.58 - 2 * math.pi - 1.2
    d = loop_angle(1, HAND_T1 * HANDOFF_K) - _blue_cast_angle(HAND_T1, ph0)
    d = (d + math.pi) % (2 * math.pi) - math.pi
    return ph0 + d


BLUE_PH = _blue_phase()


# v5 bands, as in the icon: three gold, three blue. Each: strip, height of its orbit above (-) or below (+) the portrait
# centre, tilt of its orbit plane (radians, + raises the right side), horizontal radius add-on, start angle offset, a
# delay before it pours out, length and thickness factors, alpha. Band 0 is the gold one that whips out to the upper right.
V5_BANDS = [
    dict(s='gold_a', lift=0.06, tilt=0.00, ar=0.00, ph=0.0, delay=0.00, ln=1.00, th=1.45, al=0.95),  # lash
    dict(s='blue_a', lift=-0.03, tilt=0.00, ar=0.00, ph=-1.2, delay=0.00, ln=1.00, th=1.45, al=0.95),
    dict(s='gold_b', lift=-0.13, tilt=-0.30, ar=-0.03, ph=2.3, delay=0.06, ln=0.70, th=1.15, al=0.85),  # crescent over the head
    dict(s='blue_b', lift=-0.17, tilt=0.30, ar=0.03, ph=0.9, delay=0.10, ln=0.75, th=1.15, al=0.85),    # loop behind the shoulders
    dict(s='gold_b', lift=0.13, tilt=-0.18, ar=0.07, ph=3.9, delay=0.12, ln=0.80, th=1.10, al=0.85),    # long low sweep
    dict(s='blue_b', lift=0.09, tilt=0.40, ar=0.04, ph=5.0, delay=0.16, ln=0.70, th=1.00, al=0.80),     # across the legs
]


def spin_ribbons_v5(t, grow, rise, fade, strips, back, front):
    """v5 (director, 2026-10-24: "Draw the ribbons as they appear in the icon. Exactly."; then: "there are more ribbons
    in the icon"): the icon's six translucent bands, three gold and three blue, on tilted orbits round the portrait at
    different heights (the v4 orbit centred on the portrait). Front passes never cross the face (upper half of the
    portrait); there the band goes behind and the portrait mask hides it. Band 0 (gold) whips out to the upper right.
    Each band rolls along its length (twist), narrowing to a bright edge where it turns."""
    if fade <= 0:
        return
    pcy = PORTRAIT_CY
    yc = pcy + 0.04 - 0.10 * rise
    td = 0.58
    base0 = 0.35 + SPIN_RATE * td - 2 * math.pi
    dx, dy = math.sin(TH_DEPART) + 0.35, -math.cos(TH_DEPART)
    ln = math.hypot(dx, dy)
    dx, dy = dx / ln, dy / ln
    for k, b in enumerate(V5_BANDS):
        g = ease(seg(t, 0.08 + b['delay'], 0.55 + b['delay']))
        if g <= 0:
            continue
        a_r = 0.36 + 0.04 * g + b['ar']
        b_r, pitch = 0.17, 0.05 * g
        length = (0.5 + 2.8 * g) * b['ln'] if k < 2 else 1.0 + 2.3 * g * b['ln']   # the added bands never start as scraps
        u0 = 1 - min(1.0, 0.25 + 0.75 * g)
        cy0 = yc + b['lift']
        tilt = b['tilt']
        thick = b['th']
        twist_off = 0.4 + k * 1.3 + 2.5 * t
        thh = base0 + b['ph'] - SPIN_RATE * t
        e = 0.0
        if k == 1:
            # the hand-off: the blue band slows and settles onto the loop's blue orbit, then fades over it
            e = ease(seg(t, HAND_T0, HAND_T1))
            tl = t * HANDOFF_K
            lerp = lambda a, c: a + (c - a) * e
            a_r, b_r, pitch = lerp(a_r, LOOP_A), lerp(b_r, LOOP_B), lerp(pitch, 0.0)
            length, thick = lerp(length, LOOP_LEN), lerp(thick, LOOP_THICK)
            cy0, tilt = lerp(cy0, PORTRAIT_CY + LOOP_BANDS[1][1]), lerp(tilt, LOOP_BANDS[1][2])
            u0 = lerp(u0, 0.0)
            twist_off = lerp(twist_off, 0.4 + 1.3 + 2 * math.pi * tl)
            thh = _blue_cast_angle(t, BLUE_PH)
        ct, st = math.cos(tilt), math.sin(tilt)

        def pt(th, u, cy0=cy0, a_r=a_r, b_r=b_r, pitch=pitch, ct=ct, st=st):
            x, y = a_r * math.cos(th), b_r * math.sin(th) + pitch * u
            return (0.5 + x * ct + y * st, cy0 - x * st + y * ct, math.sin(th))

        pts = []
        for i in range(SLICES + 1):
            u = i / SLICES
            if k == 0 and t > td:
                gone = SPIN_RATE * (t - td) - u * length
                if gone > 0:
                    hx, hy, _ = pt(TH_DEPART, 0)
                    dist = gone * a_r * 1.15
                    bend = 0.10 * dist * dist
                    pts.append((hx + dx * dist + 0.25 * bend, hy + dy * dist - bend, 1.0))
                    continue
                pts.append(pt(TH_DEPART - gone, 0))
            else:
                pts.append(pt(thh + u * length, u))
        al = b['al'] * (smooth(g, 0.0, 0.35) if k < 2 else smooth(g, 0.15, 0.50))   # fade in as it pours out, never a loose blob
        if k != 1:
            al *= fade
        if k == 1:
            # matched to the loop's blue band (which sits under it) by HAND_T1; then it fades, leaving the loop
            al = (al + (LOOP_BANDS[1][3] - al) * e) * (1 - ease(seg(t, HAND_T1, 1.0)))
        elif k == 0:
            al *= 1 - ease(seg(t, 0.85, 0.97))
        else:
            # gone before the final front pass (director, 2026-10-24: a gold band came round over the portrait as the
            # animation ended, "lets cut that out")
            al *= 1 - ease(seg(t, 0.74, 0.86))
        twist = (lambda u, o=twist_off: o + 2 * math.pi * 0.75 * u)
        # each band on its own layers, then laid over the others normally: a per-channel max between a gold and a
        # blue band turns their overlap pink
        bb = Image.new('RGBA', back.size, (0, 0, 0, 0))
        ff = Image.new('RGBA', front.size, (0, 0, 0, 0))
        lay_ribbon(strips[b['s']], pts, al, bb, ff, u0=u0, u1=1.0, front_ok=1.0, face=False, twist=twist,
                   thick_k=thick, no_face=True)
        back.alpha_composite(bb)
        front.alpha_composite(ff)


def flecks_from(sheet):
    """Split the fleck sheet into separate sprites (connected alpha blobs, found on a reduced copy)."""
    small = sheet.getchannel('A').resize((sheet.width // 4, sheet.height // 4)).point(lambda v: 255 if v > 40 else 0)
    w, h = small.size
    px = small.load()
    seen = set()
    boxes = []
    for y in range(h):
        for x in range(w):
            if px[x, y] and (x, y) not in seen:
                stack, xs, ys = [(x, y)], [], []
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    xs.append(cx)
                    ys.append(cy)
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                if len(xs) > 3:
                    boxes.append((min(xs) * 4 - 4, min(ys) * 4 - 4, max(xs) * 4 + 8, max(ys) * 4 + 8))
    return [sheet.crop(b) for b in boxes]


C2_R, C3_R = 0.24, 0.30        # frame-fraction radius of the full 1254 px canvas for the glow+rays and the cracks


def burst_v6(top, cb, c2, c3):
    """The icon's starburst (director, 2026-10-24; art director's C2/C3 layers): the cracks spread out from the
    portrait's centre (a soft radial wipe), the white-hot glow and its rays flare over them, then both fade. Drawn on the
    unmasked top layer, centred on the portrait. cb runs 0..1 over the first 0.45 of the cast."""
    cx, cy = 0.5 * S, PORTRAIT_CY * S
    # cracks: revealed outward over cb 0.05..0.45, fade over 0.65..1
    reveal = ease(seg(cb, 0.05, 0.45))
    al3 = 1 - ease(seg(cb, 0.60, 0.85))
    if reveal > 0 and al3 > 0:
        d = int(2 * C3_R * S)
        im = c3.resize((d, d), Image.LANCZOS)
        m = Image.new('L', (d * 2, d * 2), 0)
        rr = d * reveal * 1.05
        ImageDraw.Draw(m).ellipse([d - rr, d - rr, d + rr, d + rr], fill=255)
        m = m.resize((d, d), Image.LANCZOS).filter(ImageFilter.GaussianBlur(d * 0.04))
        a = ImageChops.multiply(im.getchannel('A'), m).point(lambda v: int(min(255, v * 1.25) * al3))
        im.putalpha(a)
        top.alpha_composite(im, (int(cx - d / 2), int(cy - d / 2)))
    # glow and rays: flare up over cb 0..0.25 (growing from half size), hold, fade over 0.55..1
    g = ease(seg(cb, 0.0, 0.25))
    al2 = g * (1 - ease(seg(cb, 0.45, 0.75)))
    if al2 > 0:
        d = max(2, int(2 * C2_R * S * (0.5 + 0.5 * g)))
        im = c2.resize((d, d), Image.LANCZOS)
        # the rays are hair-thin at this size: lift their alpha so they still read
        im.putalpha(im.getchannel('A').point(lambda v: int(min(255, v * 1.6) * al2)))
        top.alpha_composite(im, (int(cx - d / 2), int(cy - d / 2)))


def build_loop(n, size):
    """loop1 (director, 2026-10-24): the absorb effect's staticAnimation, which the game loops for as long as the
    absorb is active (libs/threejs/combat.ts: showAnimation(playInfinite) for effect.staticAnimation). A subtler version
    of the cast animation: one gold and one blue band, thinner and fainter, on a slow steady orbit round the portrait,
    and a few sparkles twinkling. It starts at the same moment as the cast animation and runs under it, so it stays
    quiet. Seamless: the bands make exactly one orbit per loop and every other motion repeats with the same period."""
    def band(name):
        im = straighten(L(name))
        return im.resize((560, max(1, round(im.height * 560 / im.width))), Image.LANCZOS)
    gold, blue = band('R1_ribbon_gold'), band('R2_ribbon_blue')
    flecks = flecks_from(L('F1_flecks'))
    rnd = random.Random(11)
    sp = []
    for i in range(6):
        ang = 2 * math.pi * i / 6 + rnd.uniform(-0.3, 0.3)
        rr = rnd.uniform(0.36, 0.44)
        sp.append(dict(img=flecks[(2 * i + 1) % len(flecks)], x=0.5 + rr * math.cos(ang),
                       y=PORTRAIT_CY + 0.05 + rr * 0.95 * math.sin(ang), ph=i / 6, s=rnd.uniform(0.05, 0.07)))
    a_r, b_r, length = LOOP_A, LOOP_B, LOOP_LEN
    strips = {'gold_a': gold, 'blue_a': blue}
    frames = []
    for f in range(n):
        t = f / n                                          # 0 .. 1, frame n would equal frame 0
        back = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        for k, (sname, lift, tilt, al, _ph) in enumerate(LOOP_BANDS):
            strip = strips[sname]
            ct, st = math.cos(tilt), math.sin(tilt)
            cy0 = PORTRAIT_CY + lift
            thh = loop_angle(k, t)                         # one full orbit per loop
            pts = []
            for i in range(SLICES + 1):
                u = i / SLICES
                th = thh + u * length
                x, y = a_r * math.cos(th), b_r * math.sin(th)
                pts.append((0.5 + x * ct + y * st, cy0 - x * st + y * ct, math.sin(th)))
            # the twist travels along the band once per loop, so it repeats exactly
            twist = (lambda u, k=k: 0.4 + k * 1.3 + 2 * math.pi * 0.75 * u + 2 * math.pi * t)
            bb = Image.new('RGBA', (S, S), (0, 0, 0, 0))
            ff = Image.new('RGBA', (S, S), (0, 0, 0, 0))
            lay_ribbon(strip, pts, al, bb, ff, u0=0.0, u1=1.0, front_ok=1.0, face=False, twist=twist,
                       thick_k=LOOP_THICK, no_face=True)
            back.alpha_composite(bb)
            front.alpha_composite(ff)
        for d in sp:                                       # each sparkle twinkles once per loop, staggered
            p = (t + d['ph']) % 1.0
            if p < 0.4:
                q = math.sin(math.pi * p / 0.4)
                sz = max(2, int(d['s'] * S * (0.4 + 0.6 * q)))
                im = d['img'].resize((sz, max(1, int(sz * d['img'].height / d['img'].width))), Image.LANCZOS)
                im.putalpha(im.getchannel('A').point(lambda v, q=q: int(v * 0.8 * q)))
                back.alpha_composite(im, (int(d['x'] * S - im.width / 2), int(d['y'] * S - im.height / 2)))

        def glowed(layer):
            g = layer.filter(ImageFilter.GaussianBlur(S * 0.008))
            g.putalpha(g.getchannel('A').point(lambda v: int(v * 0.4)))
            return Image.alpha_composite(g, layer)
        back = glowed(back)
        back.putalpha(ImageChops.multiply(back.getchannel('A'), BEHIND_MASK))
        out = Image.alpha_composite(back, glowed(front))
        out.putalpha(ImageChops.multiply(out.getchannel('A'), EDGE_FADE))
        frames.append(out.resize((size, size), Image.LANCZOS))
    return frames


HIT_N = CAST_N                   # the hit plays on the enemy's tile, started on the same tick as the cast
HIT_IMPACT = 44                  # frame of impact (1.58 s), just after the cast's gold lash leaves the caster's frame


def build_hit(n, size):
    """hit1 (director, 2026-10-24: "an impact beam of spiraling ribbons hitting their portrait... corkscrew from the top,
    timed to the lash"): the damage effect's appearAnimation, played once over the ENEMY's portrait (process.ts:1559,
    combat.ts:646). The game starts it on the same tick as the cast (one drawCombatEffects pass), so frames line up:
    gathering sparkles while the cast plays, then the gold and blue bands, wound round each other into one corkscrew,
    drive down from the top of the frame into the portrait as the cast's lash leaves the caster; on impact a flash, two
    rings of ribbon light blast outward round the portrait, and the two ribbons spring apart and curl round it (behind
    passes under the portrait mask) before fading. Each ribbon is one drawing moving along one continuous route."""
    def band(name):
        im = straighten(L(name))
        return im.resize((560, max(1, round(im.height * 560 / im.width))), Image.LANCZOS)
    gold, blue = band('R1_ribbon_gold'), band('R2_ribbon_blue')
    flecks = flecks_from(L('F1_flecks'))
    c2 = Image.open(os.path.join(HERE, 'raws', 'anim_er_v6_C2_glow_rays.png')).convert('RGBA')
    fi = HIT_IMPACT
    ix, iy = 0.5, PORTRAIT_CY + 0.03                      # impact point: the portrait's centre
    sx, sy = 0.58, -0.04                                  # the corkscrew enters from the top, a touch right of centre
    ax_len = math.hypot(ix - sx, iy - sy)
    adx, ady = (ix - sx) / ax_len, (iy - sy) / ax_len     # axis direction (down)
    nx_, ny_ = -ady, adx                                  # its normal
    R_MAX, TURNS, RIB_LEN = 0.075, 2.5, 1.05               # helix radius, turns along the ribbon, ribbon length (route units)
    ALPHA_K = 3.2                                         # route units -> spiral angle after impact
    rnd = random.Random(5)
    sp = [dict(img=flecks[i % len(flecks)], ang=2 * math.pi * i / 7 + rnd.uniform(-0.25, 0.25),
               s=rnd.uniform(0.05, 0.075), ph=rnd.uniform(0, 1)) for i in range(7)]

    def route(k, sig, spin, post=False):
        """Point (x, y, depth) at route distance sig for ribbon k: down the corkscrew axis, then out on a spiral."""
        if sig <= ax_len:
            r = R_MAX * smooth(ax_len - sig, 0.0, 0.12)   # the braid narrows to the impact point
            ph = 2 * math.pi * TURNS * sig / RIB_LEN + spin + k * math.pi
            off = r * math.cos(ph)
            dep = math.sin(ph)
            if post:
                dep = max(dep, 0.3)                       # the braid still pouring in stays in front of the portrait
            return (sx + adx * sig + nx_ * off, sy + ady * sig + ny_ * off, dep)
        al = (sig - ax_len) * ALPHA_K
        d = 1 if k == 0 else -1
        th = math.pi / 2 + d * al
        rr = min(0.40, 0.03 + 0.16 * al)
        return (ix + rr * math.cos(th), iy + rr * 0.45 * math.sin(th), math.sin(th))

    def dist(f):
        """Distance the ribbons' heads have travelled along the route at frame f (accelerating in, easing out)."""
        f0 = fi - 11
        if f < f0:
            return -1.0
        if f <= fi:
            q = (f - f0) / (fi - f0)
            return ax_len * q ** 1.6                      # accelerates into the hit
        q = (f - fi) / (n - 1 - fi)
        return ax_len + 1.35 * (1 - (1 - q) ** 2.2)       # springs out, then slows

    frames = []
    for f in range(n):
        back = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        beam_b = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        beam_f = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        top = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        # 1. sparkles gather round the portrait while the cast plays, then scatter on impact
        for d in sp:
            if f < fi:
                p = seg(f, 14, fi)
                rr = 0.44 - 0.12 * ease(p)
                a = smooth(p, 0.0, 0.3) * (0.55 + 0.45 * math.sin(math.pi * ((p * 2 + d['ph']) % 1.0)))
                sc = 0.7
            else:
                p = seg(f, fi, fi + 16)
                rr = 0.32 + 0.20 * ease(p)
                a = 1 - ease(p)
                sc = 1.0 - 0.4 * p
            if a <= 0.02:
                continue
            x, y = 0.5 + rr * math.cos(d['ang']), PORTRAIT_CY + 0.04 + rr * 0.95 * math.sin(d['ang'])
            sz = max(2, int(d['s'] * S * sc))
            im = d['img'].resize((sz, max(1, int(sz * d['img'].height / d['img'].width))), Image.LANCZOS)
            im.putalpha(im.getchannel('A').point(lambda v, a=a: int(v * a)))
            back.alpha_composite(im, (int(x * S - im.width / 2), int(y * S - im.height / 2)))
        # 2. the corkscrew and its unravelling: one route per ribbon
        D = dist(f)
        if D > 0:
            spin = 2 * math.pi * 0.35 * f                 # the braid drills as it comes
            al = 0.97 * (1 - ease(seg(f, fi + 10, n - 3)))
            for k, strip in enumerate((gold, blue)):
                lo = max(0.0, D - RIB_LEN)
                pts = [route(k, D - (D - lo) * i / SLICES, spin, D > ax_len) for i in range(SLICES + 1)]
                u0 = 0.0                                  # the whole band along the braid (its whip tip leads)
                if D <= ax_len:                           # still in the corkscrew: in front of the portrait
                    bb, ff = beam_b, beam_f
                else:
                    bb, ff = back, front
                tb = Image.new('RGBA', (S, S), (0, 0, 0, 0))
                tf = Image.new('RGBA', (S, S), (0, 0, 0, 0))
                twist = (lambda u, k=k, f=f: 0.4 + 1.3 * k + 2 * math.pi * 0.75 * u + 0.25 * f)
                lay_ribbon(strip, pts, al, tb, tf, u0=u0, u1=1.0, front_ok=1.0, face=False, twist=twist,
                           thick_k=1.15 if D <= ax_len + 0.15 else 0.9)
                if D <= ax_len:
                    # in the braid the two ribbons pass round each other; neither goes behind the portrait yet
                    ff.alpha_composite(tb)
                    ff.alpha_composite(tf)
                else:
                    bb.alpha_composite(tb)
                    ff.alpha_composite(tf)
        # 3. two rings of ribbon light blast outward round the portrait (gold, then blue)
        for k, (strip, f0) in enumerate(((gold, fi), (blue, fi + 3))):
            p = seg(f, f0, f0 + 13)
            if 0 < p < 1:
                a_r = 0.10 + 0.36 * ease(p)
                pts = []
                for i in range(SLICES + 1):
                    th = -math.pi / 2 + 2 * math.pi * i / SLICES   # the seam sits behind the portrait
                    pts.append((ix + a_r * math.cos(th), iy + a_r * 0.42 * math.sin(th), math.sin(th)))
                tb = Image.new('RGBA', (S, S), (0, 0, 0, 0))
                tf = Image.new('RGBA', (S, S), (0, 0, 0, 0))
                lay_ribbon(strip, pts, 0.9 * (1 - ease(p)), tb, tf, front_ok=1.0, face=False,
                           thick_k=0.75 - 0.45 * p, no_face=True)
                back.alpha_composite(tb)
                front.alpha_composite(tf)
        # 4. the flash at the point of impact
        g = ease(seg(f, fi - 1, fi + 2))
        al2 = g * (1 - ease(seg(f, fi + 2, fi + 10)))
        if al2 > 0:
            d = max(2, int(2 * 0.27 * S * (0.6 + 0.4 * g)))
            im = c2.resize((d, d), Image.LANCZOS)
            im.putalpha(im.getchannel('A').point(lambda v: int(min(255, v * 1.6) * al2)))
            top.alpha_composite(im, (int(ix * S - d / 2), int(iy * S - d / 2)))

        def glowed(layer):
            gl = layer.filter(ImageFilter.GaussianBlur(S * 0.010))
            gl.putalpha(gl.getchannel('A').point(lambda v: int(v * 0.5)))
            return Image.alpha_composite(gl, layer)
        back = glowed(back)
        back.putalpha(ImageChops.multiply(back.getchannel('A'), BEHIND_MASK))
        out = Image.alpha_composite(back, glowed(front))
        out = Image.alpha_composite(out, glowed(beam_b))
        out = Image.alpha_composite(out, glowed(beam_f))
        out = Image.alpha_composite(out, glowed(top))
        out.putalpha(ImageChops.multiply(out.getchannel('A'), EDGE_FADE))
        frames.append(out.resize((size, size), Image.LANCZOS))
    return frames


def build(n, size):
    if SET == 'hit1':
        return build_hit(n, size)
    if SET == 'loop1':
        return build_loop(n, size)
    gold, blue = straighten(L('R1_ribbon_gold')), straighten(L('R2_ribbon_blue'))
    # pre-shrink so warping squeezes less (no fine striping); 560 px is close to the longest on-screen path at 384 px
    gold = gold.resize((560, max(1, round(gold.height * 560 / gold.width))), Image.LANCZOS)
    blue = blue.resize((560, max(1, round(blue.height * 560 / blue.width))), Image.LANCZOS)
    v5_strips = {'gold_a': gold, 'blue_a': blue}
    if SET == 'v5':
        for key, fn in (('gold_b', 'R1_band_gold_b'), ('blue_b', 'R2_band_blue_b')):
            im = Image.open(os.path.join(HERE, 'raws', f'anim_er_v5_{fn}.png')).convert('RGBA')
            im = straighten(im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()))
            v5_strips[key] = im.resize((560, max(1, round(im.height * 560 / im.width))), Image.LANCZOS)
    core, sheet = L('C1_core'), L('F1_flecks')
    c2 = c3 = None
    if SET == 'v5':
        c2 = Image.open(os.path.join(HERE, 'raws', 'anim_er_v6_C2_glow_rays.png')).convert('RGBA')
        c3 = Image.open(os.path.join(HERE, 'raws', 'anim_er_v6_C3_cracks.png')).convert('RGBA')
    flecks = flecks_from(sheet)
    rnd = random.Random(7)
    fl = [dict(img=rnd.choice(flecks), x=0.5 + rnd.uniform(-0.34, 0.34), y=rnd.uniform(0.30, 0.82),
               start=rnd.uniform(0.35, 0.80), life=rnd.uniform(0.25, 0.4), s=rnd.uniform(0.045, 0.075)) for _ in range(16)]
    if SET == 'v5':
        # the icon's sparkles: scattered round the user, each twinkling once (grow, glint, shrink) with a slight drift up
        fl = []
        for i in range(12):
            ang = 2 * math.pi * i / 12 + rnd.uniform(-0.2, 0.2)
            rr = rnd.uniform(0.34, 0.44)
            fl.append(dict(img=flecks[i % len(flecks)], x=0.5 + rr * math.cos(ang),
                           y=PORTRAIT_CY + 0.05 + rr * 0.95 * math.sin(ang), start=rnd.uniform(0.22, 0.70),
                           life=rnd.uniform(0.22, 0.32), s=rnd.uniform(0.075, 0.11)))
    frames = []
    for f in range(n):
        t = f / (n - 1)
        back = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        top = Image.new('RGBA', (S, S), (0, 0, 0, 0))     # above the portrait mask: the seal's burst
        grow = ease(seg(t, 0.08, 0.55))
        rise = ease(seg(t, 0.15, 0.85))
        fade = 1 - ease(seg(t, 0.80, 1.0))
        if SET == 'v5':
            spin_ribbons_v5(t, grow, rise, fade, v5_strips, back, front)
        elif SET == 'v4':
            spin_ribbons_v4(t, grow, rise, fade, gold, blue, back, front)
        elif SET == 'v3':
            spin_ribbons_v3(t, grow, rise, fade, gold, blue, back, front)
        else:
            if grow > 0 and fade > 0:
                yc = 0.62 - 0.40 * rise
                spin = 2 * math.pi * 1.5 * t
                for k, strip in enumerate((gold, blue)):
                    length = 0.5 + 3.0 * grow
                    pts = helix(spin + k * math.pi, yc, 0.30 + 0.10 * grow, 0.12, length, 0.28 * grow, SLICES)
                    # opening: everything goes behind the token until the spin has risen (director, 2026-10-24: the
                    # blue ribbon at the start appeared over the player's icon)
                    lay_ribbon(strip, pts, 0.97 * fade, back, front, u0=1 - min(1.0, 0.25 + 0.75 * grow), u1=1.0,
                               front_ok=ease(seg(t, 0.45, 0.60)))
            lash = seg(t, 0.55, 0.80)                       # the gold ribbon lashes out of frame towards the enemy
            if 0 < lash < 1:
                head = lash * 1.5
                pts = []
                for i in range(31):
                    s_ = head - 0.55 * i / 30
                    if s_ < 0:
                        break
                    pts.append((0.60 + 0.58 * s_, 0.33 - 0.30 * s_ + 0.04 * math.sin(4 * s_), 1.0))
                if len(pts) > 3:
                    lay_ribbon(gold, pts, 0.97 * (1 - seg(lash, 0.75, 1.0)), back, front, 0.35, 1.0, depth_rule=False)
        cb = seg(t, 0.0, 0.45)                          # the seal breaking at the chest
        if SET == 'v5' and cb > 0:
            burst_v6(top, cb, c2, c3)
        elif cb > 0:
            r = S * 0.15 * ease(min(1, cb * 1.6))
            al = 1 - seg(cb, 0.55, 1.0)
            c = core.resize((max(1, int(2 * r)), max(1, int(2 * r))), Image.LANCZOS)
            c.putalpha(c.getchannel('A').point(lambda v: int(v * al)))
            ccx, ccy = (0.5, PORTRAIT_CY) if SET in ('v4', 'v5') else CORE
            top.alpha_composite(c, (int(ccx * S - r), int(ccy * S - r)))
        for d in fl:                                    # flecks peel off and drift up (outside the token)
            p = seg(t, d['start'], d['start'] + d['life'])
            if 0 < p < 1:
                if SET == 'v5':
                    x, y = d['x'], d['y'] - 0.06 * p
                    sz = max(2, int(d['s'] * S * (0.4 + 0.6 * math.sin(math.pi * p))))
                else:
                    x, y = d['x'] + 0.02 * math.sin(6 * p), d['y'] - 0.22 * p
                    sz = int(d['s'] * S)
                if in_window(x, y) or not (0.03 < x < 0.97 and 0.03 < y < 0.97):
                    continue
                im = d['img'].resize((sz, max(1, int(sz * d['img'].height / d['img'].width))), Image.LANCZOS)
                a = math.sin(math.pi * p)
                im.putalpha(im.getchannel('A').point(lambda v, a=a: int(v * a)))
                back.alpha_composite(im, (int(x * S - im.width / 2), int(y * S - im.height / 2)))  # never over the portrait
        # behind layer: hidden by the whole portrait (rim and rank star), its glow included, so nothing that goes
        # behind the user ever shows over them; the front layer (the near side of the wrap) is not masked
        def glowed(layer):
            g = layer.filter(ImageFilter.GaussianBlur(S * 0.010))
            g.putalpha(g.getchannel('A').point(lambda v: int(v * 0.5)))
            return Image.alpha_composite(g, layer)
        back = glowed(back)
        back.putalpha(ImageChops.multiply(back.getchannel('A'), BEHIND_MASK))
        out = Image.alpha_composite(back, glowed(front))
        tglow = top.filter(ImageFilter.GaussianBlur(S * 0.010))
        tglow.putalpha(tglow.getchannel('A').point(lambda v: int(v * 0.5)))
        out = Image.alpha_composite(out, Image.alpha_composite(tglow, top))  # the burst sits on top, unmasked
        if SET == 'v5':
            out.putalpha(ImageChops.multiply(out.getchannel('A'), EDGE_FADE))   # the whip fades out, no hard cut at the edge
        frames.append(out.resize((size, size), Image.LANCZOS))
    return frames


def stand_in_token(size):
    t = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    cx, cy, r = size * 0.5, size * TOKEN_CY, size * TOKEN_R
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 78, 96, 255), outline=(240, 240, 240, 255), width=max(1, size // 64))
    d.ellipse([cx - r * 0.32, cy - r * 0.55, cx + r * 0.32, cy + r * 0.05], fill=(200, 170, 150, 255))
    d.chord([cx - r * 0.8, cy + r * 0.05, cx + r * 0.8, cy + r * 1.4], 180, 360, fill=(40, 60, 110, 255))
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', type=int, default=40)
    ap.add_argument('--ms', type=int, default=60)
    ap.add_argument('--size', type=int, default=128)
    ap.add_argument('--set', default='v1', choices=['v1', 'v2', 'v3', 'v4', 'v5', 'loop1', 'hit1'])
    a = ap.parse_args()
    global SET
    SET = a.set
    if SET == 'v5':
        assert (a.frames, a.ms) == (CAST_N, MS), f'v5 hands off to the loop: use --frames {CAST_N} --ms {MS}'
    if SET == 'hit1':
        assert (a.frames, a.ms) == (HIT_N, MS), f'the hit is timed to the cast: use --frames {HIT_N} --ms {MS}'
    if SET == 'loop1':
        assert (a.frames, a.ms) == (LOOP_N, MS), f'the loop pairs with v5: use --frames {LOOP_N} --ms {MS}'
    frames = build(a.frames, a.size)
    os.makedirs(os.path.join(HERE, 'exports'), exist_ok=True)
    os.makedirs(DOCS, exist_ok=True)
    strip = Image.new('RGBA', (a.size, a.size * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.paste(f, (0, a.size * i))
    out = os.path.join(HERE, 'exports', f'anim_ethereal_rebirth_{SET}.webp')
    if SET in ('v5', 'loop1', 'hit1'):
        # clear alpha under 4/255 (invisible glow tails): about 8% smaller, room under the byte ceiling
        strip.putalpha(strip.getchannel('A').point(lambda v: 0 if v < 4 else v))
    strip.save(out, lossless=True, method=6)
    cols = 10
    sheet = Image.new('RGB', (a.size * cols, a.size * math.ceil(len(frames) / cols)), (18, 22, 34))
    for i, f in enumerate(frames):
        cell = Image.new('RGBA', (a.size, a.size), (18, 22, 34, 255))
        cell.alpha_composite(stand_in_token(a.size))
        cell.alpha_composite(f)
        sheet.paste(cell.convert('RGB'), ((i % cols) * a.size, (i // cols) * a.size))
    sheet.save(os.path.join(DOCS, f'{SET}_frames.png'))
    bgs = [(18, 22, 34), (74, 104, 60), (205, 210, 214)]
    gif = []
    for f in frames:
        canvas = Image.new('RGB', (3 * 150 + 3 * 70, 160), (30, 32, 38))
        for i, bg in enumerate(bgs):
            tile = Image.new('RGBA', (128, 128), bg + (255,))
            tile.alpha_composite(stand_in_token(128))
            tile.alpha_composite(f.resize((128, 128), Image.LANCZOS))
            canvas.paste(tile.convert('RGB'), (10 + i * 150, 16))
            small = Image.new('RGBA', (50, 50), bg + (255,))
            small.alpha_composite(stand_in_token(50))
            small.alpha_composite(f.resize((50, 50), Image.LANCZOS))
            canvas.paste(small.convert('RGB'), (460 + i * 70, 55))
        gif.append(canvas)
    gif[0].save(os.path.join(DOCS, f'{SET}_preview.gif'), save_all=True, append_images=gif[1:], duration=a.ms, loop=0)
    print(f'{len(frames)} frames of {a.size} px, {os.path.getsize(out)} bytes (ceiling 460800), speed {a.ms} ms = '
          f'{len(frames) * a.ms / 1000:.1f} s')


if __name__ == '__main__':
    main()
