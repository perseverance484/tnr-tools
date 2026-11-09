#!/usr/bin/env python3
"""Board preview of Dragon King's Impact (adapted from the Tempest Cleave v2 preview) over the live board recording.

A stand-in LPC ninja (recoloured toward dauntless's character) casts from four columns away with the engine's spellcast
pose (7 frames over 560 ms, facing the target). The cast lands at 60%: then the ring piece plays on the 7 circle hexes
(twice stacked), the five storm slices on the target's column (once each), the gust on the caster's hex (once), and the
struck fighters are thrown back and blink red like the engine's hit reaction.

    python3 board_tempest_v2.py BOARD.gif OUT_DIR
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, "/mnt/project-files/tnr-animation/v5")
import lpc_standin as lpc

BOARD, OUT = sys.argv[1:3]
PFX = sys.argv[3] if len(sys.argv) > 3 else "anim_dragon_king_v5a_"
TAG = sys.argv[4] if len(sys.argv) > 4 else ""
STRIPS = sys.argv[5]
RATIO = 1.0
SMOULDER = "/mnt/project-files/tnr-animation/v5/out/dragon/anim_dragon_king_v6l_smoulder.webp"
VS, HEXH, PADT, PADB = 2, 64, 64, 128
src = Image.open(BOARD).convert("RGB")
W0, H0 = src.size
board = Image.new("RGB", (W0, H0 + PADT + PADB))
board.paste(src, (0, PADT))
# the grid repeats every 64 px, so the pads must copy rows in the same phase or the hexes shear at the joins
board.paste(src.crop((0, 128 - PADT, W0, 128)), (0, 0))
ph = H0 % 64; board.paste(src.crop((0, 64 + ph, W0, 64 + ph + PADB)), (0, PADT + H0))
import numpy as _np                                              # the recording darkens a little toward its edges, which
_a = _np.asarray(board).astype(float)                            # left a step at each pad join: flatten the brightness by
_m = _a[:, 100:540].mean(axis=(1, 2))                            # rows, averaged over one 64 px grid period
_pad = _np.pad(_m, 32, mode="edge"); _k = _np.ones(64) / 64
_s = _np.convolve(_pad, _k, mode="same")[32:-32]
_a *= (_m.mean() / _np.maximum(_s, 1e-6))[:, None, None]
board = Image.fromarray(_np.clip(_a, 0, 255).astype(_np.uint8))
board = board.resize((W0 * VS, board.size[1] * VS), Image.NEAREST)


def P(x, y): return x * VS, (y + PADT) * VS


def strip(name, path=None):
    path = path or os.path.join(STRIPS, name)
    meta = json.load(open(path.replace(".webp", ".json")))
    sh = Image.open(path).convert("RGBA"); c = sh.size[0]; side = int(HEXH * RATIO * VS)   # engine: square, one hex height
    return meta, [sh.crop((0, k * c, c, (k + 1) * c)).resize((side, side), Image.BILINEAR) for k in range(meta["frames"])]


CENTRE = (217, 164)
CIRCLE = [CENTRE, (217, 100), (217, 228), (118.5, 132), (118.5, 196), (315.5, 132), (315.5, 196)]
CASTER = (512.5, 196)
FOES = [CENTRE]                                                  # only the one target is struck
SLOTS_J = json.load(open(os.path.join(STRIPS, f"{PFX}slots.json")))
SL = {s["slot"]: strip(f"{PFX}{s['slot']}.webp") for s in SLOTS_J}
SL["smoulder"] = strip("", SMOULDER)
# (strip, column offset, row offset); this target sits on an even column, so (+-1, 0) is the lower neighbour
SLOTS = [(s["slot"], 0, s["row"]) for s in SLOTS_J if not s["slot"].startswith("cast_")]
CAST_SLOTS = [(s["slot"], s["row"]) for s in SLOTS_J if s["slot"].startswith("cast_")]
FIG = round(HEXH * 1.35 * VS)                                    # engine: frame size h*1.8*0.75
cast = [f.resize((FIG, FIG), Image.NEAREST) for f in lpc.frames("ninja", "spellcast", 1)]
idle_n = [f.resize((FIG, FIG), Image.NEAREST) for f in lpc.frames("ninja", "combat_idle", 1)]
idle_f = [f.resize((FIG, FIG), Image.NEAREST) for f in lpc.frames("foe", "combat_idle", 3)]


def red(im):
    r, g, b, a = im.split()
    t = Image.merge("RGBA", (r, g.point(lambda v: v * 74 // 255), b.point(lambda v: v * 58 // 255), a))   # engine tint 0xff4a3a
    return t


def put_fig(fr, im, x, y, dx=0):
    X, Y = P(x, y)
    Y -= .325 * HEXH * VS                                        # engine: frame centre 0.325 h above the hex centre
    fr.alpha_composite(im, (int(X - FIG / 2 + dx), int(Y - FIG / 2)))


def put_clip(fr, im, x, y):
    X, Y = P(x, y); s = im.size[0]
    fr.alpha_composite(im, (int(X - s / 2), int(Y - s / 2)))


STEP, LEAD, CAST, IMPACT = 10, 400, 560, 336
# trim the recording's tree column (left) and its UI bar (right): neither repeats, so both broke at the pad joins
KEEP = (96, 0, board.size[0] - 64, board.size[1])
FX_LEN = SL["c0"][0]["frames"] * SL["c0"][0]["speed"]
total = LEAD + IMPACT + FX_LEN + 1000
frames, marks = [], {}
for t in range(-LEAD, total - LEAD, STEP):
    fr = board.convert("RGBA")
    figs = []
    if 0 <= t < CAST: figs.append((CASTER, cast[min(6, t * 7 // CAST)], 0))
    else: figs.append((CASTER, idle_n[(t // 300) % len(idle_n)], 0))
    e = t - IMPACT
    for f in FOES:
        im = idle_f[(t // 300 + int(f[0])) % len(idle_f)]; dx = 0
        if 0 <= e < 380:                                         # engine: heavy hit, 380 ms, thrown back 0.32 h, blinks
            dx = -math.sin(math.pi * e / 380) * .32 * HEXH * VS
            if (e // 60) % 2 == 0: im = red(im)
        figs.append((f, im, dx))
    for (x, y), im, dx in sorted(figs, key=lambda q: q[0][1]): put_fig(fr, im, x, y, dx)
    if e >= 0:
        sp = SL["c0"][0]["speed"]; k = e // sp
        if k < SL["c0"][0]["frames"]:
            for name, dc, dr in SLOTS: put_clip(fr, SL[name][1][k], CENTRE[0] + 98.5 * dc, CENTRE[1] + 64 * dr + (32 if dc else 0))
        if k < SL["cast_c0"][0]["frames"]:
            for name, dr in CAST_SLOTS: put_clip(fr, SL[name][1][k], CASTER[0], CASTER[1] + 64 * dr)
        ms = SL["smoulder"][0]; put_clip(fr, SL["smoulder"][1][(e // ms["speed"]) % ms["frames"]], *CASTER)
        for key, kk in (("sky", 4), ("dive", 11), ("dive2", 13), ("impact", 15), ("burn", 19), ("after", 28)):
            if k == kk and key not in marks: marks[key] = len(frames)
    if t == 200: marks["windup"] = len(frames)
    frames.append(fr.convert("RGB").crop(KEEP))
for key, idx in marks.items(): frames[idx].save(os.path.join(OUT, f"dragon{TAG}_{key}.png"))
W, H = frames[0].size
for name, slow, loops in ((f"dragon_king{TAG}_board.mp4", 1, 3), (f"dragon_king{TAG}_board_slow3x.mp4", 3, 1)):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(1000 / STEP / slow),
                          "-i", "-", "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", os.path.join(OUT, name)], stdin=subprocess.PIPE)
    for _ in range(loops):
        for f in frames: p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
print("done", W, H, len(frames))
