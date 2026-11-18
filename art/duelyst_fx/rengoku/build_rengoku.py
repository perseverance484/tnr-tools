#!/usr/bin/env python3
"""Rengoku Ro (fKQxOwBqZs8PXvpdGlbPg) art from Duelyst's fx_f4_obliterate (CC0). Director 2026-11-16.

    python3 art/duelyst_fx/rengoku/build_rengoku.py --duelyst <duelyst>/app [--final]

Jutsu: SINGLE / OPPONENT, range 4. Effects: damage (rounds 0) + afterburn (rounds 2). Art only, no mechanics:
- damage appear  = the obliterate story: ring of ghost-flame rises (the prison), implodes, dome detonation, smoke.
- afterburn loop = a quiet lead-in as long as the strike (the loop starts at the strike), then a dim re-flare of the
  ring (frames 5-11, ping-pong): "the phantom fire keeps smouldering" for its 2 rounds.
- damage disappear: cleared (the stock wind clip would replay on top).
Variants for the director: native 80 ms; tight (ring hold trimmed, 70 ms); hellfire tint.
Source frames are 300 px pixel art. The engine centres a clip on the hex centre while fighters stand 0.4 tile heights
lower (their feet near the front of the hex), so frames shift down slightly to put the ring on the feet. Files carry
a _b suffix: the first build (2026-11-16) anchored the ring on the hex centre, which floats it at shin height.
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "jutsu_icons", "forbidden_chakra_fury", "animation"))
import duelyst_fx as D  # noqa: E402
import build_v5 as V  # noqa: E402

NAME = "fx_f4_obliterate"
SHIFT = 0.035          # ring onto the target's feet: fighters stand 0.4 tile heights below the clip centre
                       # (combatActors.ts feet y=0.1-0.15h vs combatEffects.ts clip centre y=h/2); at scale 3
                       # that is +0.133 of the frame, and the source ring already sits ~0.1 low
SCALE = 3.0            # 1.5 hexes: the ring encircles the target's tile
TIGHT_DROP = {8, 10, 12, 24, 26}   # ring hold and tail frames removed in the tight cut


def base_frames(app):
    frs = D.squared(D.frames(os.path.join(app, "resources", "fx"), NAME))
    out = []
    for f in frs:
        c = Image.new("RGBA", f.size, (0, 0, 0, 0))
        c.alpha_composite(f, (0, int(SHIFT * f.height)))
        out.append(c)
    return out


def hellfire(frs):
    return [D.tint(f, (1.0, 0.36, 0.12)) for f in frs]


def smoulder(frs, strike_ms_total, ms=70, alpha=0.55):
    """The afterburn loop. The engine starts it at the strike (over the appear), so each cycle opens with a quiet
    lead-in as long as the strike, then the ring re-flares (fade in, flicker, fade out): the phantom fire smouldering
    between strikes for its 2 rounds."""
    lead = max(1, round(strike_ms_total / ms))
    ring = frs[5:12]
    seq = ring + ring[-2:0:-1]
    env = [0.25, 0.6] + [1.0] * (len(seq) - 4) + [0.6, 0.25]
    blank = Image.new("RGBA", frs[0].size, (0, 0, 0, 0))
    out = [blank] * lead
    for f, k in zip(seq, env):
        g = f.copy()
        g.putalpha(g.getchannel("A").point(lambda v, k=k: int(v * alpha * k)))
        out.append(ImageEnhance.Brightness(g).enhance(0.85))
    return out


def fit(frs, size):
    s = frs[0].width
    return [f.resize((size, size), Image.NEAREST if size % s == 0 else Image.LANCZOS) for f in frs]


def preview(variants, out, px=2, shrink=0.8):
    """Three targets side by side on the real board, each playing its variant's appear, then its smoulder loop for
    two 'rounds' (about 2.4 s), all on one clock. A stand-in figure on each target."""
    cols, rows, STACK, width_css = 12, 6, 0.25, 360
    hs = width_css / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(width_css * px), int((rows + 0.5) * h)
    pos = lambda c, r: (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))  # noqa: E731
    base = Image.new("RGBA", (W, H), (38, 40, 36, 255))
    d = ImageDraw.Draw(base)
    for c in range(cols):
        for r in range(rows):
            x, y = pos(c, r)
            d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 34))
    e = int(h * SCALE)
    spots = [(2, 3), (6, 3), (10, 3)]
    vs = []
    for (label, app_frs, ams, loop_frs, lms), spot in zip(variants, spots):
        vs.append((pos(*spot), label, fit(app_frs, e), ams, fit(loop_frs, e), lms))
    total = max(len(a) * ams for _, _, a, ams, _, _ in vs) + 2400 + 300
    frames = []
    for t in range(0, total, 20):
        im = base.copy()
        dd = ImageDraw.Draw(im)
        for (x, y), label, a, ams, lp, lms in vs:
            feet = y + 0.4 * h  # real placement: feet 0.4 tile heights below the clip centre
            dd.rounded_rectangle((x - w * 0.13, feet - h * 1.6, x + w * 0.13, feet), radius=6,
                                 fill=(70, 66, 84, 255), outline=(150, 140, 170, 255))
            dd.text((x - w * 0.55, y + h * 1.2), label, fill=(235, 235, 235, 255))
            end = len(a) * ams
            if t < end:
                im.alpha_composite(a[t // ams], (int(x - e / 2), int(y - e / 2)))
            if t < end + 2400:  # the afterburn loop runs from the strike for its rounds
                im.alpha_composite(lp[(t // lms) % len(lp)], (int(x - e / 2), int(y - e / 2)))
        dd.text((6, 4), f"Rengoku Ro x{SCALE}  t={t}ms", fill=(255, 255, 255, 220))
        im = im.convert("RGB").resize((int(W * shrink), int(H * shrink)), Image.LANCZOS)
        frames.append(im)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=20, loop=0, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True)
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--size", type=int, default=300)
    a = ap.parse_args()
    frs = base_frames(a.duelyst)
    tight = [f for i, f in enumerate(frs) if i not in TIGHT_DROP]
    hf = hellfire(tight)
    sm_native = smoulder(frs, len(frs) * 80)
    sm_tight = smoulder(frs, len(tight) * 70)
    sm_hell = smoulder(hellfire(frs), len(hf) * 70)
    variants = [("native 80ms", frs, 80, sm_native, 70),
                ("tight 70ms", tight, 70, sm_tight, 70),
                ("hellfire", hf, 70, sm_hell, 70)]
    os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
    preview(variants, os.path.join(HERE, "preview", "rengoku_board.gif"))
    outdir = os.path.join(HERE, "final" if a.final else "exports")
    os.makedirs(outdir, exist_ok=True)
    for tag, app_frs, loop_frs in (("native", frs, sm_native), ("tight", tight, sm_tight), ("hellfire", hf, sm_hell)):
        for kind, seq in (("strike", app_frs), ("smoulder", loop_frs)):
            p = os.path.join(outdir, f"anim_rengoku_{kind}_{tag}_{a.size}_b.webp")
            b = D.write_strip(fit(seq, a.size), p, a.size)
            print(f"{os.path.basename(p)}: {len(seq)} frames, {b} bytes")


if __name__ == "__main__":
    main()
