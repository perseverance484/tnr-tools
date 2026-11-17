#!/usr/bin/env python3
"""Assemble the Forbidden Chakra Fury recoil clips from the art director's sources (2026-11-16).

    python3 art/jutsu_icons/forbidden_chakra_fury/animation/build_strips.py [--size PX] [--preview]

Sources (raws/, 1254 px RGBA, art director handoff raws/HANDOFF.md):
  A_fury_burst_keypose.png   recoil appear, the detonation at full strength
  B_scorched_ground_tile.png recoil ground image (staticAssetPath), one tile
  C_fade_overlay.png         recoil disappear, low arcs and sparks
  D_crackle_overlay.png      optional recoil static loop, micro-arcs

Brief: docs/handoffs/FORBIDDEN_CHAKRA_FURY_ANIMATION_ART_REQUEST.md. All four clips share animationScale 1.75, so the
tile occupies 1/1.75 of every frame: B is placed at that size inside the clip frames (crack flash) and drawn unscaled
as the ground image. Outputs (exports/): vertical strips of square frames (one column, top to bottom), lossless WebP:
  anim_fcf_burst.webp  24 frames, intended speed 42 ms
  anim_fcf_fade.webp   12 frames, 50 ms
  anim_fcf_crackle.webp 12 frames, 60 ms, loops
  ground_fcf_scorch.webp the ground image
Deterministic (fixed seeds). Numpy is used here for per-pixel masks, as the earlier animation builders do.
"""
import argparse
import math
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raws")
OUT = os.path.join(HERE, "exports")
SCALE = 1.75
WORK = 512  # working canvas per frame


def load(name, size=WORK):
    return Image.open(os.path.join(RAW, name)).convert("RGBA").resize((size, size), Image.LANCZOS)


def ground_tile(size):
    """B cropped to its painted footprint (alpha > 4%, 2% pad) so the decal fills the tile like a floor, then squared."""
    b = Image.open(os.path.join(RAW, "B_scorched_ground_tile.png")).convert("RGBA")
    x0, y0, x1, y1 = b.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    side = max(x1 - x0, y1 - y0)
    pad = int(side * 0.02)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    h = side // 2 + pad
    return b.crop((cx - h, cy - h, cx + h, cy + h)).resize((size, size), Image.LANCZOS)


def arr(im):
    return np.asarray(im, dtype=np.float32) / 255.0


def img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


def over(dst, src):
    """Alpha-composite float RGBA arrays (straight alpha)."""
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    oa = sa + da * (1 - sa)
    rgb = np.where(oa > 0, (src[..., :3] * sa + dst[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6), 0)
    return np.concatenate([rgb, oa], axis=-1)


def transform(im, scale=1.0, rot=0.0, dy=0.0):
    w = im.width
    s = im.resize((max(1, int(w * scale)),) * 2, Image.LANCZOS).rotate(rot, Image.BICUBIC)
    c = Image.new("RGBA", (w, w))
    c.alpha_composite(s, ((w - s.width) // 2, int((w - s.height) // 2 + dy)))
    return c


def radial(n, r0, soft):
    y, x = np.mgrid[0:n, 0:n]
    r = np.hypot(x - n / 2, y - n / 2) / (n / 2)
    return np.clip((r0 - r) / soft + 0.5, 0, 1), r, np.arctan2(y - n / 2, x - n / 2)


def noise(n, seed, blur=6):
    rng = np.random.default_rng(seed)
    a = Image.fromarray((rng.random((n, n)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(a, dtype=np.float32)
    return (a - a.min()) / max(1e-6, a.max() - a.min())


def bright_points(a, k, seed, thr=0.75):
    """k bright pixels of a (luminance x alpha), for motes and embers."""
    lum = a[..., :3].mean(-1) * a[..., 3]
    ys, xs = np.nonzero(lum > thr)
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(xs), size=min(k, len(xs)), replace=False)
    return xs[idx], ys[idx], rng


def dots(n, pts, colour, radius):
    """Soft round motes at pts [(x, y, alpha)]."""
    c = np.zeros((n, n, 4), np.float32)
    y, x = np.mgrid[0:n, 0:n]
    for px, py, al in pts:
        if al <= 0:
            continue
        x0, x1, y0, y1 = int(px - radius * 3), int(px + radius * 3), int(py - radius * 3), int(py + radius * 3)
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(n, x1), min(n, y1)
        if x0 >= x1 or y0 >= y1:
            continue
        d = np.hypot(x[y0:y1, x0:x1] - px, y[y0:y1, x0:x1] - py)
        a = np.clip(1 - d / radius, 0, 1) ** 1.5 * al
        blob = np.zeros((y1 - y0, x1 - x0, 4), np.float32)
        blob[..., :3] = colour
        blob[..., 3] = a
        c[y0:y1, x0:x1] = over(c[y0:y1, x0:x1], blob)
    return c


VIOLET = np.array([0.77, 0.55, 1.0], np.float32)
CORE = np.array([0.96, 0.92, 1.0], np.float32)


def build_burst():
    A = load("A_fury_burst_keypose.png")
    Aa = arr(A)
    n = WORK
    # crack flash: B's veins (bright violet pixels) at tile size inside the 1.75x frame
    tile = int(n / SCALE)
    B = ground_tile(tile)
    Bc = Image.new("RGBA", (n, n))
    Bc.alpha_composite(B, ((n - tile) // 2, (n - tile) // 2))
    Ba = arr(Bc)
    vein = np.clip((Ba[..., :3].max(-1) - 0.55) / 0.3, 0, 1) * Ba[..., 3]
    veins = np.concatenate([np.broadcast_to(VIOLET * 0.6 + CORE * 0.4, vein.shape + (3,)), vein[..., None]], -1)
    mx, my, rng = bright_points(Aa, 46, 7)
    ang = rng.random(len(mx)) * 2 * math.pi
    er = noise(n, 11, 5)
    frames = []
    for f in range(24):
        c = np.zeros((n, n, 4), np.float32)
        if f < 3:  # draw-in: motes rush to the centre, a small core grows
            t = (f + 1) / 3
            pts = []
            for i in range(len(mx)):
                sx, sy = n / 2 + math.cos(ang[i]) * n * 0.48, n / 2 + math.sin(ang[i]) * n * 0.48
                px, py = sx + (n / 2 - sx) * (0.35 + 0.6 * t) ** 1.4, sy + (n / 2 - sy) * (0.35 + 0.6 * t) ** 1.4
                pts.append((px, py, 0.9))
            c = over(c, dots(n, pts, VIOLET * 0.8 + CORE * 0.2, 9))
            c = over(c, dots(n, [(n / 2, n / 2, 1.0)], CORE, 14 + 26 * t))
        elif f < 14:  # detonation and the lash
            t = (f - 3) / 10
            s = 0.32 + 0.68 * min(1, (f - 3) / 4) ** 0.6  # hard expansion over frames 4-7
            rot = (f - 3) * 1.6
            fr = arr(transform(A, s, rot))
            reveal, r, th = radial(n, 0.25 + 1.1 * min(1, (f - 3) / 4), 0.18)
            flick = 0.75 + 0.25 * np.sin(th * 6 + f * 2.3) * (r > 0.25)
            fr[..., 3] *= reveal * np.clip(flick, 0, 1)
            if f <= 5:  # white flash on detonation
                fl = 1 - (f - 3) / 3
                fr[..., :3] = fr[..., :3] * (1 - fl * 0.5) + CORE * fl * 0.5
            if f >= 11:  # cracks begin to flare
                v = veins.copy()
                v[..., 3] *= (f - 10) / 4
                c = over(c, v)
            c = over(c, fr)
        else:  # scorch flare then ember dissolve
            t = (f - 14) / 9
            fr = arr(transform(A, 1.0 + 0.04 * t, 17.6 + (f - 14) * 0.8, -6 * t))
            thr = t ** 1.1
            fr[..., 3] *= np.clip((er - thr) / 0.12, 0, 1)
            v = veins.copy()
            v[..., 3] *= max(0.0, 1 - max(0, f - 18) / 5)
            c = over(c, v)
            c = over(c, fr)
            ex, ey, rg = bright_points(Aa, 26, 100 + f)
            pts = [(x, y - 40 * t * (1 + (i % 3)), 0.85 * (1 - t)) for i, (x, y) in enumerate(zip(ex, ey))]
            c = over(c, dots(n, pts, VIOLET, 6))
        frames.append(img(c))
    return frames


def components(a, thr=0.15):
    """Label connected bright regions (simple flood fill) for per-arc flicker."""
    mask = a[..., 3] > thr
    lab = np.zeros(mask.shape, np.int32)
    cur = 0
    for y0, x0 in zip(*np.nonzero(mask)):
        if lab[y0, x0]:
            continue
        cur += 1
        stack = [(y0, x0)]
        lab[y0, x0] = cur
        while stack:
            y, x = stack.pop()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < mask.shape[0] and 0 <= xx < mask.shape[1] and mask[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = cur
                        stack.append((yy, xx))
    return lab, cur


def build_fade():
    C = arr(load("C_fade_overlay.png", 256))
    lab, k = components(C)
    rng = np.random.default_rng(21)
    phase = rng.random(k + 1) * 6
    frames = []
    for f in range(12):
        t = f / 11
        on = np.ones(k + 1)
        for i in range(1, k + 1):  # 2-3 snaps per arc, then out
            on[i] = (0.55 + 0.45 * math.sin(phase[i] + f * 2.1)) * (1 - t ** 1.6)
        c = C.copy()
        c[..., 3] *= np.where(lab > 0, on[lab], 1 - t)
        up = int(-14 * t)
        c = np.roll(c, up, axis=0) if f > 6 else c
        frames.append(img(c).resize((WORK, WORK), Image.LANCZOS))
    return frames


def build_crackle():
    D = arr(load("D_crackle_overlay.png", 256))
    lab, k = components(D, 0.1)
    rng = np.random.default_rng(31)
    off = rng.integers(0, 12, k + 1)
    frames = []
    for f in range(12):
        c = D.copy()
        vis = np.zeros(k + 1)
        for i in range(1, k + 1):
            p = (f + off[i]) % 12
            vis[i] = [1, 0.7, 0, 0, 0.9, 0.4, 0, 0, 0, 1, 0.5, 0][p]  # seamless 12-frame cycle, uneven brightness
        c[..., 3] *= np.where(lab > 0, vis[lab], 0)
        frames.append(img(c).resize((WORK, WORK), Image.LANCZOS))
    return frames


def strip(frames, size, path):
    s = Image.new("RGBA", (size, size * len(frames)))
    for i, fr in enumerate(frames):
        s.paste(fr.resize((size, size), Image.LANCZOS), (0, i * size))
    s.save(path, "WEBP", lossless=True, method=6)
    return os.path.getsize(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--board", action="store_true", help="game-geometry board preview (fxkit), after the strips")
    ap.add_argument("--v2", action="store_true", help="floor-ripple version (director 2026-11-16) at scale 3")
    ap.add_argument("--v3", action="store_true", help="painted floor ripple (E1/E2) and the light end clip")
    ap.add_argument("--final", action="store_true", help="export the upload set (192 px, fresh names) to final/")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.v2:
        return main_v2(a.size)
    if a.v3:
        return main_v3(a.size)
    if a.final:
        return export_final(a.size if a.size != 128 else 192)
    clips = {"burst": (build_burst(), 42), "fade": (build_fade(), 50), "crackle": (build_crackle(), 60)}
    for name, (frames, ms) in clips.items():
        p = os.path.join(OUT, f"anim_fcf_{name}.webp")
        b = strip(frames, a.size, p)
        print(f"{p}: {len(frames)} frames x {a.size}px, {ms} ms, {b} bytes{'  OVER 460800' if b > 460800 else ''}")
    g = os.path.join(OUT, "ground_fcf_scorch.webp")
    ground_tile_aspect(256).save(
        g, "WEBP", lossless=True, method=6)
    print(f"{g}: 256px, {os.path.getsize(g)} bytes")
    if a.preview:
        preview(clips)
    if a.board:
        board_preview()


def preview(clips):
    """Battle-like preview: a 7-tile spiral patch on dark, mid and bright ground; tile 64 px, clips at 1.75x."""
    T = 64
    S = int(T * SCALE)
    grounds = [(38, 36, 44), (86, 112, 66), (214, 200, 160)]
    B = ground_tile(T)
    burst, fade, crack = clips["burst"][0], clips["fade"][0], clips["crackle"][0]
    hexes = [(0, 0), (1, 0), (-1, 0), (0.5, 0.75), (-0.5, 0.75), (0.5, -0.75), (-0.5, -0.75)]
    W, H = T * 5, T * 4
    seq = [("burst", i) for i in range(24)] + [("hold", i) for i in range(24)] + [("fade", i) for i in range(12)] + [("empty", 0)] * 6
    out = []
    for kind, i in seq:
        row = Image.new("RGBA", (W * 3, H))
        for gi, gc in enumerate(grounds):
            panel = Image.new("RGBA", (W, H), gc + (255,))
            cx, cy = W // 2, H // 2
            for hx, hy in hexes:
                x, y = int(cx + hx * T), int(cy + hy * T)
                if kind in ("hold", "fade") or (kind == "burst" and i >= 14):
                    panel.alpha_composite(B, (x - T // 2, y - T // 2))
            for hx, hy in hexes:
                x, y = int(cx + hx * T), int(cy + hy * T)
                fr = {"burst": burst[i] if kind == "burst" else None, "hold": crack[i % 12], "fade": fade[i] if kind == "fade" else None}.get(kind)
                if fr is not None:
                    panel.alpha_composite(fr.resize((S, S), Image.LANCZOS), (x - S // 2, y - S // 2))
            row.paste(panel, (gi * W, 0))
        out.append(row.convert("RGB"))
    durs = [42] * 24 + [60] * 24 + [50] * 12 + [80] * 6
    p = os.path.join(HERE, "preview", "fcf_preview.gif")
    out[0].save(p, save_all=True, append_images=out[1:], duration=durs, loop=0)
    sheet = Image.new("RGB", (W * 3, H * 4))
    for k, idx in enumerate([2, 6, 16, 40]):
        sheet.paste(out[idx], (0, k * H))
    sheet.save(os.path.join(HERE, "preview", "fcf_preview_frames.png"))
    print(p)



def board_preview(scales=(1.75, 3.0), bgs=None, out_name="fcf_board"):
    """Game-geometry preview via the Headless Rider fxkit board: flat hexes squashed 2:1 (HEX_ASPECT 0.5), the
    AOE spiral patch, and the Pixi renderer's sizes (combatEffects.ts): clip = tile.height x animationScale, ground
    image = one tile, width x height. Plays burst -> ground + crackle -> fade on every hit tile at the same instant."""
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "halloween_headless_rider", "fx"))
    import fxkit  # noqa: E402
    art = os.path.join(HERE, "..", "..", "..", "halloween_headless_rider")
    bgs = bgs or [os.path.join(art, "headless_rider_horror_01_background.webp"),
                  os.path.join(art, "headless_rider_horror_02_village_dawn.webp")]
    tiles, w, h, (W, H), _ = fxkit.hex_board(scale=2)
    centre = tiles[len(tiles) // 2 + 2]
    hit = fxkit.spiral_tiles(tiles, (centre[2], centre[3]), 2, w, h)
    g = ground_tile_aspect()
    gt = g.resize((int(w), int(h)), Image.LANCZOS)
    burst = strip_frames(os.path.join(OUT, "anim_fcf_burst.webp"))
    crack = strip_frames(os.path.join(OUT, "anim_fcf_crackle.webp"))
    fade = strip_frames(os.path.join(OUT, "anim_fcf_fade.webp"))
    timeline = [("burst", i, 42) for i in range(24)] + [("hold", i, 60) for i in range(30)] + \
               [("fade", i, 50) for i in range(12)] + [("empty", 0, 400)]
    panels = []
    for bg in bgs:
        base = Image.open(bg).convert("RGBA").resize((W, int(W * 2 / 3)), Image.LANCZOS)
        base = base.crop((0, (base.height - H) // 2, W, (base.height - H) // 2 + H))
        base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
        from PIL import ImageDraw
        d = ImageDraw.Draw(base)
        for t in tiles:
            d.polygon(fxkit._hex_poly(t[2], t[3], w, h), outline=(255, 255, 255, 40))
        for sc in scales:
            eff = int(h * sc)
            seq = []
            fb, fc, ff = ([f.resize((eff, eff), Image.LANCZOS) for f in fr] for fr in (burst, crack, fade))
            for kind, i, ms in timeline:
                c = base.copy()
                if kind == "hold" or kind == "fade" or (kind == "burst" and i >= 14):
                    for t in hit:
                        c.alpha_composite(gt, (int(t[2] - w / 2), int(t[3] - h / 2)))
                for t in hit:
                    fr = fb[i] if kind == "burst" else fc[i % 12] if kind == "hold" else ff[i] if kind == "fade" else None
                    if fr is not None:
                        c.alpha_composite(fr, (int(t[2] - eff / 2), int(t[3] - eff / 2)))
                ImageDraw.Draw(c).text((8, 6), f"animationScale {sc}", fill=(255, 255, 255, 230))
                seq.append(c)
            panels.append(seq)
    cols = len(scales)
    frames = []
    for k in range(len(timeline)):
        sheet = Image.new("RGB", (W * cols, H * len(bgs)))
        for pi, seq in enumerate(panels):
            sheet.paste(seq[k].convert("RGB"), ((pi % cols) * W, (pi // cols) * H))
        frames.append(sheet)
    p = os.path.join(HERE, "preview", f"{out_name}.gif")
    frames[0].save(p, save_all=True, append_images=frames[1:], duration=[t[2] for t in timeline], loop=0, optimize=True)
    stills = Image.new("RGB", (W * cols, H * len(bgs) * 3))
    for r, k in enumerate([8, 34, 58]):
        stills.paste(frames[k], (0, r * H * len(bgs)))
    stills.save(os.path.join(HERE, "preview", f"{out_name}_stills.png"))
    print(p, os.path.getsize(p))


def strip_frames(path):
    s = Image.open(path).convert("RGBA")
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)) for i in range(s.height // s.width)]


def ground_tile_aspect(width=256):
    """B cropped to its painted footprint keeping its own aspect (the renderer stretches the ground image to the
    tile's width x height, and tiles are squashed 2:1)."""
    b = Image.open(os.path.join(RAW, "B_scorched_ground_tile.png")).convert("RGBA")
    x0, y0, x1, y1 = b.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    pw, ph = int((x1 - x0) * 0.02), int((y1 - y0) * 0.02)
    c = b.crop((x0 - pw, y0 - ph, x1 + pw, y1 + ph))
    return c.resize((width, max(1, round(width * c.height / c.width))), Image.LANCZOS)




# ------------------------------------------------------------------------------------------- v2: floor ripple
# Director 2026-11-16: "lines of violent purple chakra rippling across the floor and exploding, then the cracks remain
# and shimmer". Frame geometry at animationScale 3 (combatEffects.ts): clip side S = 3 x tile.height; the ground image
# is drawn at tile.width x tile.height = (2/3 S) x (1/3 S), centred (HEX_ASPECT 0.5). Everything on the floor is drawn
# top-down and squashed 2:1 so it lies flat on the board.
V2_SCALE = 3.0


def floor_box(n):
    gw, gh = int(n * 2 / 3), int(n / 3)
    return (n - gw) // 2, (n - gh) // 2, gw, gh


def ground_in_frame(n):
    """The ground image placed exactly where the renderer draws it, inside an n x n clip frame at scale 3."""
    x, y, gw, gh = floor_box(n)
    c = Image.new("RGBA", (n, n))
    c.alpha_composite(ground_tile_aspect(512).resize((gw, gh), Image.LANCZOS), (x, y))
    return arr(c)


def vein_mask(a):
    return np.clip((a[..., :3].max(-1) - 0.55) / 0.3, 0, 1) * a[..., 3]


def bolt(rng, length, steps=7, rough=0.22):
    """Jagged polyline from (0,0) along +x by midpoint displacement; returns [(x, y)]."""
    pts = [(0.0, 0.0), (length, 0.0)]
    amp = length * rough
    for _ in range(steps):
        new = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            new += [((x0 + x1) / 2, (y0 + y1) / 2 + rng.uniform(-amp, amp)), (x1, y1)]
        pts = new
        amp *= 0.55
    return pts


def ripple_lines(n, seed=5, count=9):
    """A web of jagged lines radiating from the centre (top-down space, radius up to ~0.5 n), with forks.
    Returns list of polylines with per-point distance from centre (for the travelling ripple)."""
    rng = np.random.default_rng(seed)
    lines = []
    for i in range(count):
        a = (i + rng.uniform(-0.3, 0.3)) / count * 2 * math.pi
        L = n * rng.uniform(0.40, 0.50)
        pts = bolt(rng, L)
        ca, sa = math.cos(a), math.sin(a)
        poly = [(n / 2 + x * ca - y * sa, n / 2 + x * sa + y * ca) for x, y in pts]
        lines.append(poly)
        for _ in range(rng.integers(1, 3)):  # forks
            k = rng.integers(len(poly) // 3, len(poly) * 3 // 4)
            fa = a + rng.choice([-1, 1]) * rng.uniform(0.35, 0.8)
            fp = bolt(rng, L * rng.uniform(0.25, 0.45), steps=6)
            bx, by = poly[k]
            lines.append([(bx + x * math.cos(fa) - y * math.sin(fa), by + x * math.sin(fa) + y * math.cos(fa)) for x, y in fp])
    return lines


def draw_ripple(n, lines, head, tail, ss=3):
    """Lines lit between radius tail..head (top-down), white-hot at the head, violet behind, then squashed 2:1."""
    from PIL import ImageDraw
    N = n * ss
    core = Image.new("L", (N, N))
    hot = Image.new("L", (N, N))
    dc, dh = ImageDraw.Draw(core), ImageDraw.Draw(hot)
    c0 = n / 2
    for poly in lines:
        for (x0, y0), (x1, y1) in zip(poly, poly[1:]):
            r = math.hypot((x0 + x1) / 2 - c0, (y0 + y1) / 2 - c0)
            if r > head or r < tail:
                continue
            seg = [(x0 * ss, y0 * ss), (x1 * ss, y1 * ss)]
            k = 1 - min(1, (head - r) / max(1, head - tail))  # 1 at the head
            dc.line(seg, fill=int(190 + 65 * k), width=int(ss * (5 + 5 * k)))
            if head - r < n * 0.09:
                dh.line(seg, fill=255, width=int(ss * 4.5))
    core = core.resize((n, n), Image.LANCZOS)
    hot = hot.resize((n, n), Image.LANCZOS)
    glow = core.filter(ImageFilter.GaussianBlur(9))
    c, h_, g = (np.asarray(x, np.float32) / 255 for x in (core, hot, glow))
    rgb = np.zeros((n, n, 3), np.float32) + VIOLET * 0.9
    rgb = rgb * (1 - h_[..., None]) + CORE * h_[..., None]
    alpha = np.clip(np.maximum(c, g * 1.6), 0, 1)
    rgb = np.where(c[..., None] > 0.05, rgb * 0.7 + CORE * 0.3 * c[..., None], np.array([0.55, 0.25, 0.95]))
    out = np.concatenate([rgb, alpha[..., None]], -1)
    sq = img(out).resize((n, n // 2), Image.LANCZOS)  # lie flat: squash 2:1 about the centre
    flat = Image.new("RGBA", (n, n))
    flat.alpha_composite(sq, (0, n // 4))
    return arr(flat)


def build_v2():
    n = WORK
    A = load("A_fury_burst_keypose.png")
    G = ground_in_frame(n)
    V = vein_mask(G)
    veins_rgb = np.concatenate([np.broadcast_to(VIOLET * 0.55 + CORE * 0.45, V.shape + (3,)), V[..., None]], -1)
    lines = ripple_lines(n)
    er = noise(n, 41, 5)
    R = n * 0.5
    burst = []
    for f in range(28):
        c = np.zeros((n, n, 4), np.float32)
        if f < 12:  # ripple outward, two waves
            t = (f + 1) / 12
            head = R * (t ** 0.8)
            c = over(c, draw_ripple(n, lines, head, max(0, head - R * 0.55)))
            if f >= 6:  # second, brighter wave chasing the first
                t2 = (f - 5) / 7
                c = over(c, draw_ripple(n, lines, R * t2 ** 0.9, max(0, R * t2 ** 0.9 - R * 0.25)))
        elif f < 20:  # the floor explodes: lines flash, the painted burst erupts upward, flattened at the base
            t = (f - 12) / 7
            lines_lit = draw_ripple(n, lines, R, 0)
            lines_lit[..., 3] *= 1 - t * 0.8
            c = over(c, lines_lit)
            v = veins_rgb.copy()
            v[..., 3] *= min(1, t * 2)
            c = over(c, v)
            s = 0.45 + 0.75 * min(1, t * 1.6) ** 0.6
            ex = transform(A, s, (f - 12) * 2.0, -n * 0.10 * t)
            exa = arr(ex.resize((n, int(n * 0.82)), Image.LANCZOS).crop((0, 0, n, int(n * 0.82))).resize((n, n)))
            exa = arr(transform(img(exa), 1.0, 0, 0))
            exa[..., 3] *= np.clip((er - t ** 1.3 + 0.15) / 0.15, 0, 1)
            if f <= 13:
                exa[..., :3] = exa[..., :3] * 0.5 + CORE * 0.5
            c = over(c, exa)
        else:  # settle: the explosion becomes embers, the lines cool into the cracks
            t = (f - 20) / 7
            v = veins_rgb.copy()
            v[..., 3] *= 1 - 0.35 * t
            c = over(c, v)
            ex, ey, rg = bright_points(arr(A), 22, 300 + f)
            pts = [(x, y * 0.8 - 60 * t * (1 + i % 3), 0.85 * (1 - t)) for i, (x, y) in enumerate(zip(ex, ey))]
            c = over(c, dots(n, pts, VIOLET, 6))
        burst.append(img(c))
    # shimmer loop: light travels along the cracks (aligned to the ground image), 16 frames
    yy, xx = np.mgrid[0:n, 0:n]
    shimmer = []
    nz = noise(n, 51, 3)
    for f in range(16):
        ph = f / 16 * 2 * math.pi
        wave = 0.5 + 0.5 * np.sin((xx * 0.035 + yy * 0.06) - ph * 2 + nz * 5)
        glint = np.clip((wave - 0.72) / 0.28, 0, 1) ** 1.5
        a = V * glint
        rgb = np.broadcast_to(CORE * 0.75 + VIOLET * 0.25, a.shape + (3,))
        shimmer.append(img(np.concatenate([rgb, a[..., None]], -1)))
    # fade: the cracks themselves dim out (the ground image vanishes when the effect ends), last sparks rise
    Cs = arr(load("C_fade_overlay.png"))
    fade = []
    for f in range(12):
        t = f / 11
        g = G.copy()
        flick = 1 - t ** 1.2
        g[..., 3] *= flick
        vv = veins_rgb.copy()
        vv[..., 3] *= flick * (0.6 + 0.4 * math.sin(f * 2.7))
        cs = Cs.copy()
        cs[..., 3] *= (1 - t) * (0.5 + 0.5 * math.sin(f * 1.9 + 1))
        fade.append(img(over(over(g, vv), cs)))
    return burst, shimmer, fade


def main_v2(size=128):
    burst, shimmer, fade = build_v2()
    for name, frames, ms in (("burst_v2", burst, 42), ("shimmer_v2", shimmer, 70), ("fade_v2", fade, 50)):
        p = os.path.join(OUT, f"anim_fcf_{name}.webp")
        b = strip(frames, size, p)
        print(f"{p}: {len(frames)} frames x {size}px, {ms} ms, {b} bytes{'  OVER 460800' if b > 460800 else ''}")
    board_preview_v2()


def board_preview_v2(out_name="fcf_board_v2"):
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "halloween_headless_rider", "fx"))
    import fxkit  # noqa: E402
    art = os.path.join(HERE, "..", "..", "..", "halloween_headless_rider")
    bg = os.path.join(art, "headless_rider_horror_01_background.webp")
    tiles, w, h, (W, H), _ = fxkit.hex_board(scale=2)
    centre = tiles[len(tiles) // 2 + 2]
    hit = fxkit.spiral_tiles(tiles, (centre[2], centre[3]), 2, w, h)
    gt = ground_tile_aspect(512).resize((int(w), int(h)), Image.LANCZOS)
    eff = int(h * V2_SCALE)
    fb, fs, ff = ([f.resize((eff, eff), Image.LANCZOS) for f in strip_frames(os.path.join(OUT, f"anim_fcf_{k}.webp"))]
                  for k in ("burst_v2", "shimmer_v2", "fade_v2"))
    base = Image.open(bg).convert("RGBA").resize((W, int(W * 2 / 3)), Image.LANCZOS)
    base = base.crop((0, (base.height - H) // 2, W, (base.height - H) // 2 + H))
    base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    d = ImageDraw.Draw(base)
    for t in tiles:
        d.polygon(fxkit._hex_poly(t[2], t[3], w, h), outline=(255, 255, 255, 40))
    tl = [("burst", i, 42) for i in range(28)] + [("hold", i, 70) for i in range(32)] + [("fade", i, 50) for i in range(12)] + [("empty", 0, 400)]
    frames = []
    for kind, i, ms in tl:
        c = base.copy()
        if kind == "hold" or (kind == "burst" and i >= 16):
            for t in hit:
                c.alpha_composite(gt, (int(t[2] - w / 2), int(t[3] - h / 2)))
        fr = fb[i] if kind == "burst" else fs[i % 16] if kind == "hold" else ff[i] if kind == "fade" else None
        if fr is not None:
            for t in hit:
                c.alpha_composite(fr, (int(t[2] - eff / 2), int(t[3] - eff / 2)))
        c = c.convert("RGB")
        frames.append(c.resize((c.width * 2 // 3, c.height * 2 // 3), Image.LANCZOS))
    p = os.path.join(HERE, "preview", f"{out_name}.gif")
    frames[0].save(p, save_all=True, append_images=frames[1:], duration=[t[2] for t in tl], loop=0, optimize=True)
    st = Image.new("RGB", (frames[0].width, frames[0].height * 5))
    for r, k in enumerate([5, 11, 15, 22, 45]):
        st.paste(frames[k], (0, r * frames[0].height))
    st.save(os.path.join(HERE, "preview", f"{out_name}_stills.png"))
    print(p, os.path.getsize(p))



# ------------------------------------------------------------------------------------------- v3: painted ripple
# Director 2026-11-16: painted floor ripple (art request section 7, raws E1/E2) replaces the scripted lines; "Sharper is
# fine. Let's do this animation." The end clip is kept light (vein flicker and sparks, no ground plate): a ground
# tag's disappearAnimation repeats on anyone standing in it (combat_fx.md gotcha 2).
def painted_ripple(n, layer, head, hot=0.09, tail_fade=0.55):
    """Reveal a painted top-down web out to radius `head` (fraction of n), white-hot at the head, then squash 2:1."""
    L = arr(Image.open(os.path.join(RAW, layer)).convert("RGBA").resize((n, n), Image.LANCZOS))
    _, r, _ = radial(n, 1, 1)
    r = r * 0.5  # radius as a fraction of n
    vis = np.clip((head - r) / 0.02 + 0.5, 0, 1)
    band = np.clip(1 - (head - r) / hot, 0, 1) * (r <= head)
    behind = 1 - tail_fade * np.clip((head - r - hot) / 0.35, 0, 1)
    out = L.copy()
    out[..., :3] = out[..., :3] * (1 - band[..., None] * 0.85) + CORE * band[..., None] * 0.85
    out[..., 3] = out[..., 3] * vis * np.maximum(behind, band)
    sq = img(out).resize((n, n // 2), Image.LANCZOS)
    flat = Image.new("RGBA", (n, n))
    flat.alpha_composite(sq, (0, n // 4))
    return arr(flat)


def build_v3():
    n = WORK
    A = load("A_fury_burst_keypose.png")
    G = ground_in_frame(n)
    V = vein_mask(G)
    veins_rgb = np.concatenate([np.broadcast_to(VIOLET * 0.55 + CORE * 0.45, V.shape + (3,)), V[..., None]], -1)
    er = noise(n, 41, 5)
    reach = 0.47
    burst = []
    for f in range(28):
        c = np.zeros((n, n, 4), np.float32)
        if f < 12:  # E1 races out; E2 chases from frame 6
            t = (f + 1) / 12
            c = over(c, painted_ripple(n, "E1_Ripple_Web.png", reach * t ** 0.8))
            if f >= 6:
                t2 = (f - 5) / 7
                c = over(c, painted_ripple(n, "E2_Second_Wave.png", reach * t2 ** 0.9, hot=0.12, tail_fade=0.75))
        elif f < 20:  # the floor erupts: webs flash out, the painted burst rises, cracks flare in
            t = (f - 12) / 7
            w1 = painted_ripple(n, "E1_Ripple_Web.png", reach, tail_fade=0.0)
            w2 = painted_ripple(n, "E2_Second_Wave.png", reach, tail_fade=0.0)
            for w in (w1, w2):
                w[..., 3] *= max(0.0, 1 - t * 1.3)
                c = over(c, w)
            v = veins_rgb.copy()
            v[..., 3] *= min(1, t * 2)
            c = over(c, v)
            s = 0.45 + 0.75 * min(1, t * 1.6) ** 0.6
            ex = arr(transform(A, s, (f - 12) * 2.0, -n * 0.10 * t))
            ex[..., 3] *= np.clip((er - t ** 1.3 + 0.15) / 0.15, 0, 1)
            if f <= 13:
                ex[..., :3] = ex[..., :3] * 0.5 + CORE * 0.5
            c = over(c, ex)
        else:  # settle into the cracks, embers rise
            t = (f - 20) / 7
            v = veins_rgb.copy()
            v[..., 3] *= 1 - 0.35 * t
            c = over(c, v)
            ex_, ey, _ = bright_points(arr(A), 22, 300 + f)
            pts = [(x, y * 0.8 - 60 * t * (1 + i % 3), 0.85 * (1 - t)) for i, (x, y) in enumerate(zip(ex_, ey))]
            c = over(c, dots(n, pts, VIOLET, 6))
        burst.append(img(c))
    # light end clip: vein flicker and the C sparks only (no ground plate; repeats on occupants)
    Cs = arr(load("C_fade_overlay.png"))
    fade = []
    for f in range(10):
        t = f / 9
        vv = veins_rgb.copy()
        vv[..., 3] *= (1 - t) * (0.45 + 0.35 * math.sin(f * 2.7))
        cs = Cs.copy()
        cs[..., 3] *= (1 - t) * (0.5 + 0.5 * math.sin(f * 1.9 + 1))
        fade.append(img(over(vv, cs)))
    return burst, fade


def main_v3(size=128):
    burst, fade = build_v3()
    for name, frames, ms in (("burst_v3", burst, 42), ("fade_v3", fade, 50)):
        p = os.path.join(OUT, f"anim_fcf_{name}.webp")
        b = strip(frames, size, p)
        print(f"{p}: {len(frames)} frames x {size}px, {ms} ms, {b} bytes{'  OVER 460800' if b > 460800 else ''}")



def export_final(size=192):
    """Final upload set (director 2026-11-16: own host, native resolution). Fresh filenames; 2 px clear margin at the
    top and bottom of every frame (linear sampling bleeds between frames)."""
    burst, fade = build_v3()
    _, shimmer, _ = build_v2()
    fin = os.path.join(HERE, "final")
    os.makedirs(fin, exist_ok=True)

    def margin(frames):
        out = []
        for f in frames:
            f = f.resize((size, size), Image.LANCZOS)
            a = np.asarray(f).copy()
            a[:2, :, 3] = 0
            a[-2:, :, 3] = 0
            out.append(Image.fromarray(a, "RGBA"))
        return out

    rows = []
    for name, frames, ms in (("fcf_burst_v3", burst, 42), ("fcf_shimmer_v3", shimmer, 70), ("fcf_fade_v3", fade, 50)):
        p = os.path.join(fin, f"anim_{name}_{size}.webp")
        b = strip(margin(frames), size, p)
        rows.append((os.path.basename(p), len(frames), ms, b))
    g = os.path.join(fin, "ground_fcf_scorch_v3.webp")
    ground_tile_aspect(384).save(g, "WEBP", lossless=True, method=6)
    rows.append((os.path.basename(g), 1, 0, os.path.getsize(g)))
    for r in rows:
        print("%s: %d frames, %d ms, %d bytes" % r)


if __name__ == "__main__":
    main()
