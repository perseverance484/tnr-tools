#!/usr/bin/env python3
"""Forbidden Chakra Fury v6: v5's tessellating field fed by a Duelyst forbidden-gate pillar on the caster (2026-11-18).

    TNR_DUELYST=<cache> python3 art/jutsu_icons/forbidden_chakra_fury/animation/build_v6_duelyst.py [--board] [--final]

Director: "Can we build a forbidden chakra fury animation using those scripts?" (the Duelyst kit). Same structure and
rulings as v5 (art on the recoil tag; ONE caster visual tag; no tag mosaic):
- CASTER (visual tag appear, scale 3): OpenDuelyst fx_f2_eightgates_purpleflame (CC0), the Songhai gate-opening
  pillar, anchored to the caster's feet: it ignites (source frames 1-4), roars (5-8), and as it collapses (23-30)
  v5's caster detonation plays over it: chakra drawn into the body, then six drive-cracks run to the hex edges.
- FIELD (recoil appear/static/disappear + ground image, scale 2): v5's crack network unchanged, delayed by LEAD ticks
  so it starts cutting when the drive-cracks reach the caster's hex edges. Duelyst stays off the field on purpose:
  a stamped Duelyst piece on 60 tiles turns into a field of identical clusters (the FCF shadowcreep trial); the
  field must tessellate, which v5's spokes do.
- The static loop starts at t=0 (engine), so its quiet stretch is lengthened by the same delay.
One 42 ms clock for caster and field (the pillar's 80 ms frames are held two ticks). Every strip is <= 4096 px tall
(native hosting: phones draw taller strips black), so sizes come from frame counts.
"""
import argparse
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "skills", "producing-tnr-art", "scripts"))
import build_v5 as V  # noqa: E402
import build_strips as B  # noqa: E402

try:
    import duelyst_kit as K  # skill branch fable/duelyst-kit, or main once merged
except ImportError:  # main before the kit merges: the older module has the same readers
    sys.path.insert(0, os.path.join(REPO, "art", "duelyst_fx"))
    import duelyst_fx as K  # noqa: E402

N = V.N
TICK = 42
LEAD = 12                     # field delay, ticks: v5's caster frame f plays at tick LEAD + f
PILLAR = list(range(1, 9)) + list(range(23, 31))   # ignite + roar, then the collapse; each held 2 ticks
FEET_H = 0.4                  # fighter feet sit 0.4 tile-heights below the clip centre (combatActors geometry)
PILLAR_H = 1.85               # pillar height in tile heights: the clip ends 1.9 h above the feet (figure ~1.6 h)
LICENSE = "CC0 1.0 - OpenDuelyst (open-duelyst/duelyst), fx_f2_eightgates_purpleflame, adapted for TNR"


def pillar_frames(n=N):
    """The Duelyst pillar on an n x n caster canvas (clip side = 3 tile heights), its base on the caster's feet."""
    src = K.squared(K.frames("fx_f2_eightgates_purpleflame"))
    boxes = [f.getbbox() for f in src if f.getbbox()]
    top = min(b[1] for b in boxes)
    base = max(b[3] for b in boxes)
    h = n / V.CASTER_SCALE
    k = PILLAR_H * h / (base - top)
    side = int(round(src[0].width * k))
    feet_y = n / 2 + FEET_H * h
    out = []
    for f in src:
        g = f.resize((side, side), Image.LANCZOS)
        c = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        c.alpha_composite(g, (int(n / 2 - side / 2), int(feet_y - base * k)))
        out.append(c)
    return out


def build_caster(n=N):
    pil = pillar_frames(n)
    det = V.build_caster(n)                      # v5: frames 0-3 gather, 4+ detonate and drive-cracks
    ticks = max(2 * len(PILLAR), LEAD + len(det))
    frames = []
    for t in range(ticks):
        c = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        if t // 2 < len(PILLAR):
            c.alpha_composite(pil[PILLAR[t // 2]])
        if 0 <= t - LEAD < len(det):
            c.alpha_composite(det[t - LEAD])
        frames.append(c)
    return frames


def build_field(n=N):
    blank = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    return [blank] * LEAD + V.build_field_appear(n)


def size_for(frames, cap=4096):
    px = cap // len(frames)
    return px - px % 2


def board(clips, out, cols=12, rows=10, caster=(5, 5), radius=4, px=2, shrink=0.75):
    """v5's real-board preview with the corrected stand-in figure (feet 0.4 h below the clip centre, ~1.6 h tall)
    and the v6 clocks."""
    width_css, STACK = 360, 0.25
    hs = width_css / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(width_css * px), int((rows + 0.5) * h)
    tiles = {(c, r): (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
             for c in range(cols) for r in range(rows)}
    field = sorted([k for k in tiles if k != caster and V.hex_dist(k, caster) <= radius], key=lambda k: tiles[k][1])
    base = Image.new("RGBA", (W, H), (38, 40, 36, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in tiles.values():
        d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 34))
    fe, ce = int(h * V.FIELD_SCALE), int(h * V.CASTER_SCALE)
    rs = lambda fr, s: [f.resize((s, s), Image.LANCZOS) for f in fr]  # noqa: E731
    fa, fl, fend, ca = rs(clips["field"], fe), rs(clips["loop"], fe), rs(clips["end"], fe), rs(clips["caster"], ce)
    g = clips["ground"].resize((int(w), int(h)), Image.LANCZOS)
    l_ms, e_ms = V.MS["loop"], V.MS["end"]
    lasting = len(fl) * l_ms * 2
    total = lasting + len(fend) * e_ms + 500
    marks = set(range(0, len(fa) * TICK + 1, TICK)) | set(range(0, len(ca) * TICK + 1, TICK)) | \
        set(range(0, lasting, l_ms)) | set(range(lasting, lasting + len(fend) * e_ms + 1, e_ms)) | {total}
    times = sorted(m for m in marks if m <= total)
    cx, cy = tiles[caster]
    frames, durs = [], []
    for i, t in enumerate(times[:-1]):
        im = base.copy()
        live = t < lasting
        if live and t >= (LEAD + 8) * TICK:     # the scar shows once the field has cut (v5 flash frame 8)
            for k in field:
                x, y = tiles[k]
                im.alpha_composite(g, (int(x - w / 2), int(y - h / 2)))
        ImageDraw.Draw(im).rounded_rectangle((cx - w * 0.12, cy - 1.2 * h, cx + w * 0.12, cy + FEET_H * h),
                                             radius=6, fill=(70, 66, 84, 255), outline=(150, 140, 170, 255))
        layers = []
        if live and t < len(fa) * TICK:
            layers.append(fa[t // TICK])
        if live:
            layers.append(fl[(t // l_ms) % len(fl)])
        if not live and t - lasting < len(fend) * e_ms:
            layers.append(fend[(t - lasting) // e_ms])
        for fr in layers:
            for k in field:
                x, y = tiles[k]
                im.alpha_composite(fr, (int(x - fe / 2), int(y - fe / 2)))
        if t < len(ca) * TICK:
            im.alpha_composite(ca[t // TICK], (int(cx - ce / 2), int(cy - ce / 2)))
        ImageDraw.Draw(im).text((6, 4), f"FCF v6  Duelyst gate pillar + v5 field  t={t}ms  {len(field)} tiles",
                                fill=(255, 255, 255, 220))
        im = im.convert("RGB")
        frames.append(im.resize((int(W * shrink), int(H * shrink)), Image.LANCZOS))
        durs.append(times[i + 1] - t)
    q, acc, done = [], 0, 0
    for dm in durs:
        acc += dm
        step = max(20, int(round((acc - done) / 10.0)) * 10)
        q.append(step)
        done += step
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=q, loop=0, optimize=True)
    return len(field), len(frames)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", action="store_true")
    ap.add_argument("--final", action="store_true", help="write the upload set to final/ (fresh v6 names)")
    a = ap.parse_args()
    quiet = 15 + math.ceil(LEAD * TICK / V.MS["loop"])
    clips = {"caster": build_caster(), "field": build_field(), "loop": V.build_field_loop(frames=32 + quiet - 15,
             quiet=quiet), "end": V.build_field_end(), "ground": V.build_field_ground()}
    outdir = os.path.join(HERE, "final" if a.final else "exports")
    os.makedirs(outdir, exist_ok=True)
    names = {"caster": ("anim_fcf_caster_v6", True, TICK), "field": ("anim_fcf_field_v6", True, TICK),
             "loop": ("anim_fcf_glint_v6", False, V.MS["loop"]), "end": ("anim_fcf_drain_v6", False, V.MS["end"])}
    rt = {}
    for key, (stem, pal, ms) in names.items():
        size = min(192, size_for(clips[key]))
        p = os.path.join(outdir, f"{stem}_{size}.webp")
        b = B.strip(V.margin(clips[key], size), size, p, palette=pal)
        assert size * len(clips[key]) <= 4096
        print(f"{os.path.basename(p)}: {len(clips[key])} frames x {ms} ms, {size} px "
              f"({size * len(clips[key])} px tall), {b} bytes")
        rt[key] = [f.resize((size, size), Image.LANCZOS) for f in clips[key]]
    g = os.path.join(outdir, "ground_fcf_scar_v6.webp")
    clips["ground"].resize((384, 192), Image.LANCZOS).save(g, "WEBP", lossless=True, method=6)
    print(f"{os.path.basename(g)}: 384x192, {os.path.getsize(g)} bytes")
    if a.board:
        prev = os.path.join(HERE, "preview")
        os.makedirs(prev, exist_ok=True)
        rt["ground"] = clips["ground"].resize((384, 192), Image.LANCZOS)
        nt, nf = board(rt, os.path.join(prev, "fcf_board_v6.gif"))
        print(f"board: {nt} field tiles, {nf} frames -> preview/fcf_board_v6.gif")


if __name__ == "__main__":
    main()
