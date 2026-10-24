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


PORTRAIT_R = TOKEN_R + 0.006    # the whole portrait, white rim included, plus a hair of margin


def _behind_mask(radius=None):
    """Alpha mask for everything behind the user: 0 inside the avatar portrait and its rank star (soft 1 px edge), 255
    outside."""
    m = Image.new('L', (S * 4, S * 4), 255)
    k = S * 4
    r, cx, cy = (radius or PORTRAIT_R) * k, 0.5 * k, TOKEN_CY * k
    d = ImageDraw.Draw(m)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    # the rank star and its mount hang below the portrait (measured from the director's battle recording: the star
    # spans x 0.47-0.54, y 0.57-0.63 of the frame); cover x 0.5 +/- 0.07 down to y 0.67 with rounded corners
    d.rounded_rectangle([cx - 0.07 * k, (TOKEN_CY + 0.15) * k, cx + 0.07 * k, 0.67 * k], radius=0.03 * k, fill=0)
    return m.resize((S, S), Image.LANCZOS)


BEHIND_MASK = _behind_mask()


SET = 'v1'


def L(name):
    """v1: layers cut from the first sheet (layers/). v2: the art director's transparent raws (raws/anim_er_v2_*),
    cropped to their content."""
    src = 'v1' if (SET == 'v1' or (SET == 'v3' and name == 'C1_core')) else 'v2'
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


def lay_ribbon(strip, pts, alpha, back, front, u0=0.0, u1=1.0, depth_rule=True, front_ok=1.0):
    """Warp the straight `strip` (its part u0..u1; the strip's right end is the ribbon's head) onto the path `pts`
    (head first) as a chain of quads that share their edges, so the ribbon bends without seams."""
    n = len(pts) - 1
    sw, sh = strip.size
    hw = THICK * S / 2
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
        if depth_rule and FACE_Y[0] < my < FACE_Y[1] and math.hypot(mx - 0.5, my - TOKEN_CY) < WINDOW_R:
            wf *= 0.30                                       # near side over the face: mostly see-through
        a *= smooth(min(i, n - 1 - i), 0, 5)               # soft head and tail, never a square cut
        if a <= 0.01:
            continue
        thick = 0.7 + 0.3 * nearness
        quad = []
        for j in (i, i + 1):
            nx, ny = normals[j]
            quad.append((P[j][0] + nx * hw * thick, P[j][1] + ny * hw * thick))
        for j in (i + 1, i):
            nx, ny = normals[j]
            quad.append((P[j][0] - nx * hw * thick, P[j][1] - ny * hw * thick))
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


def build(n, size):
    gold, blue = straighten(L('R1_ribbon_gold')), straighten(L('R2_ribbon_blue'))
    # pre-shrink so warping squeezes less (no fine striping); 560 px is close to the longest on-screen path at 384 px
    gold = gold.resize((560, max(1, round(gold.height * 560 / gold.width))), Image.LANCZOS)
    blue = blue.resize((560, max(1, round(blue.height * 560 / blue.width))), Image.LANCZOS)
    core, sheet = L('C1_core'), L('F1_flecks')
    flecks = flecks_from(sheet)
    rnd = random.Random(7)
    fl = [dict(img=rnd.choice(flecks), x=0.5 + rnd.uniform(-0.34, 0.34), y=rnd.uniform(0.30, 0.82),
               start=rnd.uniform(0.35, 0.80), life=rnd.uniform(0.25, 0.4), s=rnd.uniform(0.045, 0.075)) for _ in range(16)]
    frames = []
    for f in range(n):
        t = f / (n - 1)
        back = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        top = Image.new('RGBA', (S, S), (0, 0, 0, 0))     # above the portrait mask: the seal's burst
        grow = ease(seg(t, 0.08, 0.55))
        rise = ease(seg(t, 0.15, 0.85))
        fade = 1 - ease(seg(t, 0.80, 1.0))
        if SET == 'v3':
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
        if cb > 0:
            r = S * 0.15 * ease(min(1, cb * 1.6))
            al = 1 - seg(cb, 0.55, 1.0)
            c = core.resize((max(1, int(2 * r)), max(1, int(2 * r))), Image.LANCZOS)
            c.putalpha(c.getchannel('A').point(lambda v: int(v * al)))
            top.alpha_composite(c, (int(CORE[0] * S - r), int(CORE[1] * S - r)))
        for d in fl:                                    # flecks peel off and drift up (outside the token)
            p = seg(t, d['start'], d['start'] + d['life'])
            if 0 < p < 1:
                x, y = d['x'] + 0.02 * math.sin(6 * p), d['y'] - 0.22 * p
                if in_window(x, y):
                    continue
                sz = int(d['s'] * S)
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
    ap.add_argument('--set', default='v1', choices=['v1', 'v2', 'v3'])
    a = ap.parse_args()
    global SET
    SET = a.set
    frames = build(a.frames, a.size)
    os.makedirs(os.path.join(HERE, 'exports'), exist_ok=True)
    os.makedirs(DOCS, exist_ok=True)
    strip = Image.new('RGBA', (a.size, a.size * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.paste(f, (0, a.size * i))
    out = os.path.join(HERE, 'exports', f'anim_ethereal_rebirth_{SET}.webp')
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
