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
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    clips = {"burst": (build_burst(), 42), "fade": (build_fade(), 50), "crackle": (build_crackle(), 60)}
    for name, (frames, ms) in clips.items():
        p = os.path.join(OUT, f"anim_fcf_{name}.webp")
        b = strip(frames, a.size, p)
        print(f"{p}: {len(frames)} frames x {a.size}px, {ms} ms, {b} bytes{'  OVER 460800' if b > 460800 else ''}")
    g = os.path.join(OUT, "ground_fcf_scorch.webp")
    ground_tile(256).save(
        g, "WEBP", lossless=True, method=6)
    print(f"{g}: 256px, {os.path.getsize(g)} bytes")
    if a.preview:
        preview(clips)


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


if __name__ == "__main__":
    main()
