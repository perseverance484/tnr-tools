#!/usr/bin/env python3
"""Duelyst (OpenDuelyst, CC0) effect sheets -> TNR battle strips.

    python3 art/duelyst_fx/duelyst_fx.py gallery --src <duelyst>/app/resources/fx --res <duelyst>/app/data/resources.js
    python3 art/duelyst_fx/duelyst_fx.py strip NAME --src .. --size 192 [--fit 0.9] [--dy 0] [--tint 0.72,0.42,1.0] out.webp

Source: github.com/open-duelyst/duelyst, released CC0 1.0 after the game closed (2020). Sheets are cocos2d plists
(format 2): each frame has a `frame` rect in the atlas (`rotated` = stored 90 degrees clockwise), and a
`sourceColorRect` placing the trimmed pixels inside `sourceSize`. We rebuild each full frame, pad it to a square
(TNR frames are square, one-column vertical strips), and scale it with NEAREST so the pixel art stays crisp.
Timing comes from `frameDelay` in resources.js (most are 0.08 s).
"""
import argparse
import os
import plistlib
import re

from PIL import Image, ImageDraw, ImageOps

NUM = re.compile(r"(\d+)")


def rect(s):
    a = [int(float(x)) for x in re.findall(r"-?\d+\.?\d*", s)]
    return a[0], a[1], a[2], a[3]


def size(s):
    a = [int(float(x)) for x in re.findall(r"-?\d+\.?\d*", s)]
    return a[0], a[1]


def natural(k):
    return [int(t) if t.isdigit() else t for t in NUM.split(k)]


def split(name):
    """`sheet` or `sheet:prefix` (one sheet can hold several animations, e.g. fx_shadowcreep idle and spawn)."""
    sheet, _, prefix = name.partition(":")
    return sheet, prefix


def sequences(src, sheet):
    d = plistlib.load(open(os.path.join(src, sheet + ".plist"), "rb"))
    out = {}
    for k in d["frames"]:
        pre = NUM.split(k)[0] if not k[0].isdigit() else ""
        pre = re.sub(r"\d+\.png$", "", k)
        out[pre] = out.get(pre, 0) + 1
    return out


def frames(src, name):
    """Full-size RGBA frames of one sheet (or one `sheet:prefix` animation), in order."""
    name, prefix = split(name)
    d = plistlib.load(open(os.path.join(src, name + ".plist"), "rb"))
    atlas = Image.open(os.path.join(src, name + ".png")).convert("RGBA")
    if not prefix and len(sequences(src, name)) > 1:
        raise SystemExit(f"{name} holds several animations, pick one as {name}:<prefix>: {sequences(src, name)}")
    out = []
    for k in sorted(d["frames"], key=natural):
        if prefix and not k.startswith(prefix):
            continue
        v = d["frames"][k]
        x, y, w, h = rect(v["frame"])
        if v.get("rotated"):
            piece = atlas.crop((x, y, x + h, y + w)).rotate(90, expand=True)
        else:
            piece = atlas.crop((x, y, x + w, y + h))
        sw, sh = size(v["sourceSize"])
        cx, cy, cw, ch = rect(v["sourceColorRect"])
        full = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        full.paste(piece, (cx, cy))
        out.append(full)
    return out


def delay_ms(res_js, name, default=80):
    """frameDelay for the resource whose plist is `name` (resources.js entries: plist: RSX.x / path strings)."""
    if not res_js or not os.path.exists(res_js):
        return default
    sheet, prefix = split(name)
    s = open(res_js).read()
    i = s.find(f"framePrefix: '{prefix}'") if prefix else s.find(f"{sheet}.plist")
    if i < 0:
        return default
    m = re.search(r"frameDelay:\s*([0-9.]+)", s[i:i + 600])
    return int(round(float(m.group(1)) * 1000)) if m else default


def squared(frs):
    """Pad every frame to a common square (keeps the sheet's own centre, which Duelyst anchors on the tile/unit)."""
    w = max(f.width for f in frs)
    h = max(f.height for f in frs)
    s = max(w, h)
    out = []
    for f in frs:
        c = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        c.paste(f, ((s - f.width) // 2, (s - f.height) // 2))
        out.append(c)
    return out


def tint(im, rgb, amount=1.0):
    """Recolour by luminance into a ramp dark->rgb->white (keeps the drawing, swaps the palette)."""
    r, g, b, a = im.split()
    lum = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))
    lo = tuple(int(255 * c * 0.25) for c in rgb)
    mid = tuple(int(255 * c) for c in rgb)
    col = ImageOps.colorize(lum, black=lo, mid=mid, white=(250, 244, 255), midpoint=110)
    if amount < 1:
        col = Image.blend(Image.merge("RGB", (r, g, b)), col, amount)
    out = col.convert("RGBA")
    out.putalpha(a)
    return out


def place(frs, size_px, fit=1.0, dy=0.0, tint_rgb=None):
    """Square TNR frames of `size_px`: the art scaled (NEAREST, integer steps when it can) to `fit` of the frame,
    shifted by dy (fraction of the frame, + = down)."""
    sq = squared(frs)
    s = sq[0].width
    target = max(1, int(size_px * fit))
    out = []
    for f in sq:
        if tint_rgb:
            f = tint(f, tint_rgb)
        g = f.resize((target, target), Image.NEAREST if target >= s else Image.LANCZOS)
        c = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
        c.alpha_composite(g, ((size_px - target) // 2, (size_px - target) // 2 + int(dy * size_px)))
        out.append(c)
    return out


def write_strip(frs, path, size_px):
    sheet = Image.new("RGBA", (size_px, size_px * len(frs)), (0, 0, 0, 0))
    for i, f in enumerate(frs):
        sheet.paste(f, (0, i * size_px))
    sheet.save(path, "WEBP", lossless=True, method=6)
    return os.path.getsize(path)


def gallery(src, res_js, names, out, cell=150, cols=5):
    clips = []
    for n in names:
        frs = squared(frames(src, n))
        clips.append((n.split(":")[-1] or n, [f.resize((cell, cell), Image.NEAREST if f.width <= cell else Image.LANCZOS) for f in frs],
                      delay_ms(res_js, n)))
    rows = (len(clips) + cols - 1) // cols
    total = 2400
    step = 40
    W, H = cols * cell, rows * (cell + 14)
    out_frames = []
    for t in range(0, total, step):
        im = Image.new("RGB", (W, H), (34, 36, 32))
        d = ImageDraw.Draw(im)
        for i, (n, frs, ms) in enumerate(clips):
            x, y = (i % cols) * cell, (i // cols) * (cell + 14)
            k = (t // ms) % (len(frs) + 6)  # a short gap between plays
            if k < len(frs):
                im.paste(frs[k], (x, y + 14), frs[k])
            d.text((x + 3, y + 1), n.replace("fx_", "")[:24], fill=(220, 220, 220))
        out_frames.append(im)
    out_frames[0].save(out, save_all=True, append_images=out_frames[1:], duration=step, loop=0, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    g = sp.add_parser("gallery")
    g.add_argument("--src", required=True)
    g.add_argument("--res")
    g.add_argument("--out", default="gallery.gif")
    g.add_argument("names", nargs="+")
    s = sp.add_parser("strip")
    s.add_argument("name")
    s.add_argument("out")
    s.add_argument("--src", required=True)
    s.add_argument("--size", type=int, default=192)
    s.add_argument("--fit", type=float, default=1.0)
    s.add_argument("--dy", type=float, default=0.0)
    s.add_argument("--tint")
    a = ap.parse_args()
    if a.cmd == "gallery":
        gallery(a.src, a.res, a.names, a.out)
        print(a.out)
    else:
        rgb = tuple(float(x) for x in a.tint.split(",")) if a.tint else None
        frs = place(frames(a.src, a.name), a.size, a.fit, a.dy, rgb)
        print(a.out, len(frs), "frames", write_strip(frs, a.out, a.size), "bytes")


if __name__ == "__main__":
    main()
