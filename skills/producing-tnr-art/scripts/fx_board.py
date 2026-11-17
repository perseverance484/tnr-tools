#!/usr/bin/env python3
"""Combat FX helpers: preview clips on the game's real board, split/join strips, place art in the tile box.

    python3 fx_board.py board --appear A.webp [--loop L.webp] [--end E.webp] [--ground G.webp] [--scale 3]
                              [--ms 42,60,50] [--pattern spiral|all|one] [--bg BG.webp] --out preview.gif
    python3 fx_board.py ground-box --scale 3 --size 128      # where the tile sits inside a clip frame
    python3 fx_board.py ground-check G.webp                   # gate for a battle ground image (staticAssetPath)
    python3 fx_board.py strip-info A.webp                     # frames, frame size, bytes vs the ANIMATION ceiling
    python3 fx_board.py --selftest

Geometry is the Pixi renderer's (theninjarpg combatEffects.ts / animation.ts, checked at f6a51fac5): flat hexes in
a 2:1 box (HEX_ASPECT_RATIO 0.5, stacking 0.25), clips square at tile.height x animationScale centred on the tile,
the ground image (staticAssetPath) stretched to the tile box; appear and loop start on one clock with the loop
drawn on top; every tile one action hits starts together (actions themselves replay one after another). Board layout follows art/halloween_headless_rider/fx/fxkit.py. Pillow only; no network.
"""
import argparse
import math
import os
import sys
import tempfile

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artpreflight import webp_mode  # noqa: E402  the one RIFF codec reader (VP8L vs 'VP8 ', VP8X-aware)

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
    """Engine order (combatEffects.ts): at the strike the ground image, the appear (zIndex 1) and the loop (zIndex 2,
    drawn ON TOP) all start on one clock; the loop keeps cycling while the effect lasts; the end clip plays when it
    ends. Frames are sampled from shared elapsed time, so appear/loop occlusion shows exactly as in battle."""
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
    a_ms, l_ms, e_ms = ms
    lasting = max(len(fa) * a_ms, len(fl) * l_ms * hold_loops if fl else 0, 600 if gt is not None else 0)
    end_ms = len(fe) * e_ms
    total = lasting + end_ms + 400
    # Sample at every instant any clip changes frame on the shared clock (not a fixed tick, which can skip frames
    # of fast clips entirely). GIF viewers clamp delays under 20 ms, so a faster clip is shown frame-complete but
    # slowed; that is reported, never hidden by dropping frames.
    marks = {0, lasting, total}
    if fa:
        marks.update(range(0, min(len(fa) * a_ms, lasting), a_ms))
        marks.add(min(len(fa) * a_ms, lasting))  # the appear's expiry is an event too
    if fl:
        marks.update(range(0, lasting, l_ms))
    if fe:
        marks.update(range(lasting, lasting + end_ms, e_ms))
    marks.add(lasting + end_ms)
    times = sorted(m for m in marks if m < total)
    frames, durs = [], []
    for k, t_ms in enumerate(times):
        nxt = times[k + 1] if k + 1 < len(times) else total
        c = base.copy()
        live = t_ms < lasting
        if gt is not None and live:
            for t in hit:
                c.alpha_composite(gt, (int(t[2] - w / 2), int(t[3] - h / 2)))
        layers = []
        if live and fa and t_ms < len(fa) * a_ms:
            layers.append(fa[t_ms // a_ms])                      # appear, zIndex 1
        if live and fl:
            layers.append(fl[(t_ms // l_ms) % len(fl)])          # loop, zIndex 2, over the appear
        if not live and fe and t_ms - lasting < end_ms:
            layers.append(fe[(t_ms - lasting) // e_ms])          # end clip, server visual
        for fr in layers:
            for t in hit:
                c.alpha_composite(fr, (int(t[2] - eff / 2), int(t[3] - eff / 2)))
        ImageDraw.Draw(c).text((6, 4), f"animationScale {scale}  t={t_ms}ms", fill=(255, 255, 255, 220))
        c = c.convert("RGB")
        if shrink != 1.0:
            c = c.resize((int(c.width * shrink), int(c.height * shrink)), Image.LANCZOS)
        frames.append(c)
        durs.append(nxt - t_ms)
    real = total - times[0]
    # GIF delays are whole centiseconds and viewers clamp under 20 ms. Quantize on the CUMULATIVE clock (error
    # diffusion) so rounding does not accumulate, never below 20 ms, then measure the encoded file itself.
    q, acc, done = [], 0, 0
    for d_ms in durs:
        acc += d_ms
        step = max(20, int(round((acc - done) / 10.0)) * 10)
        q.append(step)
        done += step
    durs = q
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True)
    enc = Image.open(out)
    enc_d = []
    for i in range(getattr(enc, "n_frames", 1)):
        enc.seek(i)
        enc_d.append(enc.info.get("duration", 0))
    shown = sum(enc_d)
    starts, acc = [], 0
    for d_ms in enc_d:
        starts.append(acc)
        acc += d_ms
    drift = max(abs(a - (b - times[0])) for a, b in zip(starts, times))  # encoded vs game start of each frame
    under = sum(1 for k, t_ms in enumerate(times) if (times[k + 1] if k + 1 < len(times) else total) - t_ms < 20)
    if shown != real or drift:
        word = "slower" if shown > real else "faster" if shown < real else "same total"
        print(f"note: encoded GIF {shown} ms for {real} ms of game time ({shown / real:.2f}x, {word}); frames start up "
              f"to {drift} ms off their game time ({under} interval(s) under the 20 ms floor, delays in 10 ms steps); "
              f"every frame is still shown")
    board.last_timing = {"game_ms": real, "gif_ms": shown, "max_drift_ms": drift, "under_floor": under}
    return out, len(frames), len(hit)


def ground_check(path, max_bytes=BYTE_CEILING):
    """Gate for a battle ground image (effect.staticAssetPath). The renderer stretches it to the 2:1 tile box, so it
    must be wide, transparent at the edges and real alpha; there is no spec target for it (STATIC is map-pin art)."""
    errors, warns = [], []
    im = Image.open(path)
    mode = webp_mode(path)
    if im.format != "WEBP":
        errors.append(f"format {im.format}: export lossless WebP")
    elif mode != "lossless":
        errors.append(f"WebP codec {mode or 'unreadable'}: export lossless (VP8L)")
    im = im.convert("RGBA")
    W, H = im.size
    ar = W / H
    if not 1.4 <= ar <= 2.6:
        errors.append(f"aspect {ar:.2f}: the tile box is 2:1 (allowed 1.4-2.6); square art is squashed flat")
    if W < 128:
        errors.append(f"width {W}px: at least 128")
    a = im.getchannel("A")
    lo, hi = a.getextrema()
    if lo == 255:
        errors.append("no transparency: a ground image needs real alpha")
    border = [a.getpixel((x, 0)) for x in range(W)] + [a.getpixel((x, H - 1)) for x in range(W)] + \
             [a.getpixel((0, y)) for y in range(H)] + [a.getpixel((W - 1, y)) for y in range(H)]
    if max(border) > 40:
        warns.append(f"edge alpha up to {max(border)}: feather the edges so tiles blend on any ground")
    b = os.path.getsize(path)
    if b >= max_bytes:
        errors.append(f"{b} bytes: over the {max_bytes} ceiling")
    return {"file": path, "size": [W, H], "aspect": round(ar, 2), "bytes": b, "errors": errors, "warnings": warns}


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
        assert n == 10 and hits > 7, (n, hits)  # 8 appear frames, ground alone after expiry, post-effect
        # occlusion: a red appear under a blue loop must show blue at t=0, as the engine draws the loop on top
        red, blue = os.path.join(td, "r.webp"), os.path.join(td, "u.webp")
        save_strip([Image.new("RGBA", (32, 32), (255, 0, 0, 255))] * 4, red, 32)
        save_strip([Image.new("RGBA", (32, 32), (0, 0, 255, 255))] * 4, blue, 32)
        out, n, hits = board(os.path.join(td, "o.gif"), appear=red, loop=blue, scale=3, pattern="one")
        g0 = Image.open(out).convert("RGB")
        tiles, w, h, _ = hex_board()
        cx, cy = pattern_tiles(tiles, w, h, "one")[0][2:]
        px = g0.getpixel((int(cx), int(cy)))
        assert px[2] > 150 and px[0] < 100, px
        rb = os.path.join(td, "rb.webp")
        save_strip([Image.new("RGBA", (32, 32), (255, 0, 0, 255)), Image.new("RGBA", (32, 32), (0, 0, 255, 255))], rb, 32)
        out, n, _ = board(os.path.join(td, "f.gif"), loop=rb, scale=3, pattern="one", ms=(42, 20, 50))
        gif = Image.open(out)
        seen = set()
        for i in range(n):
            gif.seek(i)
            p = gif.convert("RGB").getpixel((int(cx), int(cy)))
            seen.add("r" if p[0] > 150 else "b" if p[2] > 150 else "-")
        assert {"r", "b"} <= seen, seen
        # appear expiry: one 100 ms red appear over a 600 ms ground must leave the tile after 100 ms
        one = os.path.join(td, "one.webp")
        save_strip([Image.new("RGBA", (32, 32), (255, 0, 0, 255))], one, 32)
        out, n, _ = board(os.path.join(td, "x.gif"), appear=one, ground=g, scale=3, pattern="one", ms=(100, 60, 50))
        gif, t_acc, red_ms = Image.open(out), 0, 0
        for i in range(n):
            gif.seek(i)
            if gif.convert("RGB").getpixel((int(cx), int(cy)))[0] > 150:
                red_ms += gif.info["duration"]
        assert red_ms == 100, red_ms
        # merged schedules: 21/20 ms clips are each over the floor but their merged events are not; must be reported
        a4, l4 = os.path.join(td, "a4.webp"), os.path.join(td, "l4.webp")
        save_strip([Image.new("RGBA", (32, 32), (255, 0, 0, 255))] * 4, a4, 32)
        save_strip([Image.new("RGBA", (32, 32), (0, 0, 255, 128))] * 4, l4, 32)
        board(os.path.join(td, "m.gif"), appear=a4, loop=l4, scale=3, pattern="one", ms=(21, 20, 50))
        tm = board.last_timing
        assert tm["under_floor"] > 0 and (tm["gif_ms"] != tm["game_ms"] or tm["max_drift_ms"] > 0), tm
        # 10 ms quantization: four 29 ms appear frames must not be truncated (cumulative rounding keeps the clip near
        # 116 ms) and the report must come from the encoded file
        a29 = os.path.join(td, "a29.webp")
        save_strip([Image.new("RGBA", (32, 32), (255, 0, 0, 255))] * 4, a29, 32)
        out, n, _ = board(os.path.join(td, "q.gif"), appear=a29, scale=3, pattern="one", ms=(29, 60, 50))
        enc, red_ms, total_ms = Image.open(out), 0, 0
        for i in range(n):
            enc.seek(i)
            total_ms += enc.info["duration"]
            if enc.convert("RGB").getpixel((int(cx), int(cy)))[0] > 150:
                red_ms += enc.info["duration"]
        assert abs(red_ms - 116) <= 5, red_ms
        assert board.last_timing["gif_ms"] == total_ms, (board.last_timing, total_ms)
        assert board.last_timing["max_drift_ms"] <= 5, board.last_timing
        gc = ground_check(g)
        assert not gc["errors"], gc
        lossy = os.path.join(td, "lossy.webp")
        im = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((20, 10, 236, 118), fill=(90, 40, 140, 255))
        im.save(lossy, "WEBP", lossless=False, quality=35)
        assert any("codec" in e for e in ground_check(lossy)["errors"]), ground_check(lossy)
        sq = os.path.join(td, "sq.webp")
        Image.new("RGBA", (128, 128), (90, 40, 140, 255)).save(sq, "WEBP", lossless=True)
        assert any("aspect" in e for e in ground_check(sq)["errors"])
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
    gc = sub.add_parser("ground-check")
    gc.add_argument("path")
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
    elif a.cmd == "ground-check":
        r = ground_check(a.path)
        for e in r["errors"]:
            print("error  ", e)
        for wn in r["warnings"]:
            print("warning", wn)
        print(f"{r['file']}: {r['size'][0]}x{r['size'][1]}, aspect {r['aspect']}, {r['bytes']} bytes; "
              f"{len(r['errors'])} error(s), {len(r['warnings'])} warning(s)")
        return 1 if r["errors"] else 0
    else:
        print(strip_info(a.path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
