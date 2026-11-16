#!/usr/bin/env python3
"""Combat FX helpers: preview clips on the game's real board, split/join strips, place art in the tile box.

    python3 fx_board.py board --appear A.webp [--loop L.webp] [--end E.webp] [--ground G.webp] [--scale 3]
                              [--ms 42,60,50] [--pattern spiral|all|one] [--bg BG.webp] --out preview.gif
    python3 fx_board.py ground-box --scale 3 --size 128      # where the tile sits inside a clip frame
    python3 fx_board.py strip-info A.webp                     # frames, frame size, bytes vs the ANIMATION ceiling
    python3 fx_board.py --selftest

Geometry is the Pixi renderer's (theninjarpg combatEffects.ts / animation.ts, checked at f6a51fac5): flat hexes in
a 2:1 box (HEX_ASPECT_RATIO 0.5, stacking 0.25), clips square at tile.height x animationScale centred on the tile,
the ground image (staticAssetPath) stretched to the tile box, every hit tile starting at the same instant (no
timeline). Board layout follows art/halloween_headless_rider/fx/fxkit.py. Pillow only; no network.
"""
import argparse
import math
import os
import sys
import tempfile

from PIL import Image, ImageDraw

HEX_ASPECT = 0.5
STACK = 0.25
BYTE_CEILING = 460_800  # ANIMATION target; the authority is 25x_DATA_art_spec.json


def strip_frames(path):
    s = Image.open(path).convert("RGBA")
    n = max(1, s.height // s.width)
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)) for i in range(n)]


def save_strip(frames, path, size=128):
    s = Image.new("RGBA", (size, size * len(frames)))
    for i, f in enumerate(frames):
        s.paste(f.convert("RGBA").resize((size, size), Image.LANCZOS), (0, i * size))
    s.save(path, "WEBP", lossless=True, method=6)
    return os.path.getsize(path)


def ground_box(scale, size):
    """(x, y, w, h) of the tile inside a size x size clip frame at animationScale `scale`."""
    h = size / scale
    w = 2 * h
    return (size - w) / 2, (size - h) / 2, w, h


def hex_board(width_css=360, cols=12, rows=7, px=2):
    hexsize = width_css / (cols - STACK * (cols - 1))
    w, h = hexsize * px, hexsize * HEX_ASPECT * px
    tiles = []
    for c in range(cols):
        for r in range(rows):
            x = c * w * (1 - STACK) + w / 2
            y = r * h + h / 2 + (h / 2 if c % 2 else 0)
            tiles.append((c, r, x, y))
    return tiles, w, h, (int(width_css * px), int((rows + 0.5) * h))


def pattern_tiles(tiles, w, h, pattern):
    centre = tiles[len(tiles) // 2 + 2]
    if pattern == "all":
        return tiles
    if pattern == "one":
        return [centre]
    out = []
    for t in tiles:  # spiral patch: tiles within 2 hex steps (approximate in board space)
        if math.hypot((t[2] - centre[2]) / (w * 0.75), (t[3] - centre[3]) / h) <= 2.25:
            out.append(t)
    return out


def hex_poly(x, y, w, h):
    return [(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y), (x + w / 4, y + h / 2),
            (x - w / 4, y + h / 2)]


def board(out, appear=None, loop=None, end=None, ground=None, scale=1.0, ms=(42, 60, 50), pattern="spiral",
          bg=None, hold_loops=2, shrink=1.0):
    tiles, w, h, (W, H) = hex_board()
    hit = pattern_tiles(tiles, w, h, pattern)
    if bg:
        base = Image.open(bg).convert("RGBA").resize((W, int(W * 2 / 3)), Image.LANCZOS)
        base = base.crop((0, (base.height - H) // 2, W, (base.height - H) // 2 + H))
        base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    else:
        base = Image.new("RGBA", (W, H), (44, 46, 40, 255))
    d = ImageDraw.Draw(base)
    for t in tiles:
        d.polygon(hex_poly(t[2], t[3], w, h), outline=(255, 255, 255, 40))
    eff = max(1, int(h * scale))
    fa, fl, fe = ([f.resize((eff, eff), Image.LANCZOS) for f in strip_frames(p)] if p else [] for p in (appear, loop, end))
    gt = Image.open(ground).convert("RGBA").resize((int(w), int(h)), Image.LANCZOS) if ground else None
    tl = [("a", i, ms[0]) for i in range(len(fa))]
    tl += [("l", i, ms[1]) for i in range(len(fl) * hold_loops)] if fl else [("l", 0, 600)] if gt else []
    tl += [("e", i, ms[2]) for i in range(len(fe))] + [("x", 0, 400)]
    frames = []
    for kind, i, _ in tl:
        c = base.copy()
        if gt is not None and kind in ("a", "l"):  # the ground image shows from the cast while the effect lasts
            for t in hit:
                c.alpha_composite(gt, (int(t[2] - w / 2), int(t[3] - h / 2)))
        fr = fa[i] if kind == "a" else fl[i % len(fl)] if kind == "l" and fl else fe[i] if kind == "e" else None
        if fr is not None:
            for t in hit:
                c.alpha_composite(fr, (int(t[2] - eff / 2), int(t[3] - eff / 2)))
        ImageDraw.Draw(c).text((6, 4), f"animationScale {scale}", fill=(255, 255, 255, 220))
        c = c.convert("RGB")
        if shrink != 1.0:
            c = c.resize((int(c.width * shrink), int(c.height * shrink)), Image.LANCZOS)
        frames.append(c)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=[t[2] for t in tl], loop=0, optimize=True)
    return out, len(frames), len(hit)


def strip_info(path):
    fr = strip_frames(path)
    b = os.path.getsize(path)
    return {"frames": len(fr), "frame_px": fr[0].width, "bytes": b, "under_ceiling": b < BYTE_CEILING,
            "has_alpha": any(f.getchannel("A").getextrema()[0] < 255 for f in fr)}


def selftest():
    with tempfile.TemporaryDirectory() as td:
        frames = []
        for i in range(8):
            f = Image.new("RGBA", (64, 64))
            ImageDraw.Draw(f).ellipse((32 - 4 * i, 32 - 4 * i, 32 + 4 * i, 32 + 4 * i), outline=(180, 90, 255, 255), width=3)
            frames.append(f)
        a = os.path.join(td, "a.webp")
        save_strip(frames, a, 64)
        info = strip_info(a)
        assert info["frames"] == 8 and info["frame_px"] == 64 and info["has_alpha"], info
        g = os.path.join(td, "g.webp")
        Image.new("RGBA", (128, 64), (90, 40, 140, 200)).save(g, "WEBP", lossless=True)
        out, n, hits = board(os.path.join(td, "b.gif"), appear=a, ground=g, scale=3, pattern="spiral")
        assert n == 8 + 1 + 1 and hits > 7, (n, hits)
        x, y, w, h = ground_box(3, 120)
        assert (round(w), round(h), round(x), round(y)) == (80, 40, 20, 40)
    print("SELFTEST PASS")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("board")
    for k in ("appear", "loop", "end", "ground", "bg"):
        b.add_argument(f"--{k}")
    b.add_argument("--scale", type=float, default=1.0)
    b.add_argument("--ms", default="42,60,50", help="appear,loop,end ms per frame")
    b.add_argument("--pattern", default="spiral", choices=["spiral", "all", "one"])
    b.add_argument("--shrink", type=float, default=1.0, help="scale the GIF down for phones (e.g. 0.66)")
    b.add_argument("--out", required=True)
    g = sub.add_parser("ground-box")
    g.add_argument("--scale", type=float, required=True)
    g.add_argument("--size", type=int, default=128)
    s = sub.add_parser("strip-info")
    s.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "board":
        if not 1 <= a.scale <= 3:
            ap.error("animationScale is 1 to 3")
        ms = tuple(int(x) for x in a.ms.split(","))
        out, n, hits = board(a.out, a.appear, a.loop, a.end, a.ground, a.scale, ms, a.pattern, a.bg, shrink=a.shrink)
        print(f"{out}: {n} frames, {hits} tiles, scale {a.scale}, {os.path.getsize(out)} bytes")
    elif a.cmd == "ground-box":
        x, y, w, h = ground_box(a.scale, a.size)
        print(f"tile box in a {a.size}px frame at scale {a.scale}: x={x:.1f} y={y:.1f} w={w:.1f} h={h:.1f}")
    else:
        print(strip_info(a.path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
