#!/usr/bin/env python3
"""Mother of Echoes, the quality-bar batches (director's standing directive, 2026-11-05: "every boss ability animation
must look as cool as the Refraction slice-mosaic line").

    python3 art/mother_of_echoes_fx/build_fx_a6.py [--out DIR]

Batch 1 (by how often a player sees it, docs/design/MOTHER_OF_ECHOES_ART.md "Ability quality bar"):
- Refraction / Far Refraction / Facet / Lucid Refraction BREAKS: the approved Refraction line (build_fx_mosaic.py,
  director: "incredible, amazing 10/10"), sliced per column: anim_moe_rbreak_c{0..11}_a6. Every line is a full row of
  12 hexes in the spec, so one slice per column serves every row (row parity does not change a column's offset).
- the same rows' MARK arrival as one composition: light runs in from both walls along the row, meets, holds white,
  then lies still and thins to the mark's glints (SAYO_BIBLE.md 3.2: travel, lie still): anim_moe_rmark_c{0..11}_a6.
- Glass Lancet (per-hex: single target): neutral Mother Glass needle, 3 frames of flight from the upper left (the key
  light), the HELD white star for 2 frames, chips falling, 14 frames (3.1): anim_moe_lancet_a6.
Writes exports/*_a6.webp and exports/moe_fx_a6.json (or --out for a review folder). Pillow only.
"""
import argparse
import importlib.util
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("build_fx_mosaic", os.path.join(HERE, "build_fx_mosaic.py"))
MZ = importlib.util.module_from_spec(_s)
_s.loader.exec_module(MZ)
A4, A, F = MZ.A4, MZ.A, MZ.F
PAL, PRISM, WHITE, SCORE = A.PAL, MZ.PRISM, F.WHITE, F.SCORE
ROW = [(c, 1) for c in range(12)]
MG = dict(body=(214, 218, 228), lite=(250, 248, 240), edge=(91, 103, 134), deep=(24, 26, 36), chip=(255, 238, 196))
# neutral Mother Glass (QA S7: no safe-cyan; clear glass in pale steel and white, white-gold chips)


def rmark_line(cells, frames=20):
    return _rmark(cells, frames)


def _rmark(cells, frames):
    """The Refraction mark's arrival as one image: two heads of light run in from the walls along the row, meet, the
    whole line holds white (2 frames, nothing moves), then it lies still and thins, mirror glints standing on it."""
    cv = MZ.Canvas(cells)
    pts = sorted(cv.c(*k) for k in cells)
    xl, xr = pts[0][0], pts[-1][0]
    p = PAL["I"]

    def y_at(x):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / max(1, x1 - x0)
        return pts[0][1] if x < xl else pts[-1][1]

    RUN, HOLD = 7, 2
    out = []
    mid = (xl + xr) / 2
    for i in range(frames):
        f = cv.frame()
        if i < RUN:
            t = MZ.A4.ease((i + 1) / RUN)
            hl = xl - 15 + (xr - xl + 30) * t                    # one head, from the wall end
            hr = None
            for xx in range(int(xl - 15), int(xr + 16)):
                if xx > hl:
                    continue
                y = y_at(xx)
                F.px(f, xx, y - 1, p["lite"]); F.px(f, xx, y, WHITE); F.px(f, xx, y + 1, p["lite"])
                F.px(f, xx, y + 2, p["seam"])
            for hx in (hl,):
                A4.star(f, hx, y_at(hx), WHITE, 3)
                for k in range(3):
                    MZ.A4.cluster(f, hx - (6 + 4 * k), y_at(hx) - 3 + 2 * k, PRISM[k], p["seam"])
        elif i < RUN + HOLD:                                      # the hold: the whole line white, still
            for xx in range(int(xl - 16), int(xr + 17)):
                y = y_at(xx)
                for dy in (-2, -1, 0, 1, 2):
                    F.px(f, xx, y + dy, WHITE if abs(dy) < 2 else p["hot"])
                F.px(f, xx, y + 3, p["seam"])
        else:                                                    # it lies still: thins to a lit seam, glints stand on it
            u = (i - RUN - HOLD) / (frames - RUN - HOLD - 1)
            keep = max(0.0, 1 - u * 1.1)
            for xx in range(int(xl - 15), int(xr + 16)):
                y = y_at(xx)
                F.px(f, xx, y, p["hot"] if u < 0.4 else p["lite"], keep=keep)
                if u < 0.5:
                    F.px(f, xx, y - 1, p["lite"], keep=keep)
            for k, (x, _) in enumerate(pts):
                if (k + i) % 3 == 0 and u < 0.8:
                    A4.star(f, x + 6, y_at(x + 6) - 1, WHITE, 2)
        out.append(f)
    return cv, out


def lancet():
    """Neutral Mother Glass: flick, pierce, steady. A glint at the wall side (2 frames), the needle flies 3 frames from
    the upper left with two fading ghosts, the white star HOLDS 2 frames on the target's body, chips fall. 14 frames."""
    out = []
    tip = (26, 18)                                               # the fighter's body in the clip (portrait centre)
    start = (9, 8)
    L = 20

    def needle(f, hx, hy, keep=1.0, col=MG["body"]):
        ang = math.atan2(hy - start[1], hx - start[0])
        ln = max(4.0, min(L, math.hypot(hx - start[0], hy - start[1])))
        tx, ty = hx - ln * math.cos(ang), hy - ln * math.sin(ang)
        nx, ny = -math.sin(ang), math.cos(ang)
        n = F.frame()
        d = ImageDraw.Draw(n)
        d.polygon([(hx, hy), (tx + 2 * nx, ty + 2 * ny), (tx - 2 * nx, ty - 2 * ny)], fill=(*col, 255))
        d.line([(hx, hy), (tx + 1 * nx, ty + 1 * ny)], fill=(*MG["lite"], 255))
        d.line([(hx, hy), (tx - 1.5 * nx, ty - 1.5 * ny)], fill=(*WHITE, 255))
        F.outline_alpha(n, MG["deep"])
        if keep < 1:
            a = n.getchannel("A").point(lambda v: v)
            for y in range(N := n.height):
                for x in range(n.width):
                    if a.getpixel((x, y)) and F.BAYER[y % 4][x % 4] >= keep * 16:
                        n.putpixel((x, y), (0, 0, 0, 0))
        f.alpha_composite(n)

    for i in range(14):
        f = F.frame()
        if i < 2:                                                # anticipation: the wall glints
            A4.star(f, start[0] + 2, start[1] + 2, WHITE, 2 + i)
        elif i < 5:                                              # flight
            t = (i - 1) / 3
            hx, hy = start[0] + (tip[0] - start[0]) * t, start[1] + (tip[1] - start[1]) * t
            for g, keep in ((2, 0.35), (1, 0.6)):
                tg = max(0.05, t - g * 0.18)
                needle(f, start[0] + (tip[0] - start[0]) * tg, start[1] + (tip[1] - start[1]) * tg, keep, MG["lite"])
            needle(f, hx, hy)
        elif i < 7:                                              # the held star: nothing moves
            n = F.frame()
            for k in range(-9, 10):
                w = 2 if abs(k) < 3 else 1
                for j in range(-w + 1, w):
                    F.px(n, tip[0] + k, tip[1] + j, WHITE)
                    F.px(n, tip[0] + j, tip[1] + k, WHITE)
            for k in range(-4, 5):
                F.px(n, tip[0] + k, tip[1] + k, MG["lite"]); F.px(n, tip[0] + k, tip[1] - k, MG["lite"])
            F.outline_alpha(n, MG["edge"])
            f.alpha_composite(n)
        else:                                                    # chips fall: steady
            v = i - 7
            for k, (dx, dy) in enumerate(((-5, -3), (4, -4), (7, 0), (-6, 2), (2, -6), (-2, 4))):
                if v > 4 and k % 2:
                    continue
                A4.cluster(f, tip[0] + dx * (1 + 0.2 * v), tip[1] + dy + 0.35 * v * v,
                           MG["chip"] if k % 2 else MG["body"], MG["deep"])
        out.append(f)
    return A4.edge_check("lancet", out)


# The spec's lines are 9 hexes from a wall (SAYO_BIBLE.md 3.2): "L" rows are columns 0-8 from the left wall, "R" rows
# columns 3-11 from the right wall. The R composition is the L one drawn on columns 3-11 and mirrored about the row's
# middle (column c <-> 14 - c keeps every column's parity, so the odd-column drop still lines up).
ROWS = {"L": [(c, 1) for c in range(0, 9)], "R": [(c, 1) for c in range(3, 12)]}


def mirrored(frames):
    return [f.transpose(Image.FLIP_LEFT_RIGHT) for f in frames]


def line_slices(kind, build):
    out = {}
    for side, cells in ROWS.items():
        cv, fr = build(cells)
        if side == "R":
            fr = mirrored(fr)
        for (col, _row), sl in sorted(cv.slices(fr).items()):
            out[(side, col)] = sl
    return out


def assets():
    out = []
    for (side, col), sl in sorted(line_slices("break", lambda c: MZ.refraction_line(c, mirrored=True)).items()):
        out.append((f"anim_moe_rbreak_{side.lower()}{col}_a6.webp", sl, f"Refraction Breaks, {side} row, column {col}"))
    for (side, col), sl in sorted(line_slices("mark", rmark_line).items()):
        out.append((f"anim_moe_rmark_{side.lower()}{col}_a6.webp", sl, f"Refraction mark arrival, {side} row, column {col}"))
    out.append(("anim_moe_lancet_a6.webp", lancet(), "Glass Lancet: needle, held star, chips (neutral Mother Glass)"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=F.EXPORTS)
    a = ap.parse_args()
    rows = []
    for name, frames, note in assets():
        p = os.path.join(a.out, name)
        F.strip(frames).save(p, lossless=True, quality=100, method=6)
        rows.append({"file": f"art/mother_of_echoes_fx/exports/{name}", "type": "ANIMATION", "frames": len(frames),
                     "speed": F.MS, "bytes": os.path.getsize(p), "note": note})
    with open(os.path.join(a.out, "moe_fx_a6.json"), "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/build_fx_a6.py", "assets": rows}, fh, indent=1)
        fh.write("\n")
    print(len(rows), "FX")


if __name__ == "__main__":
    main()


# ------------------------------------------------------------------------------------------------ batch 2 (per-hex)
ASH = ((58, 52, 56), (128, 118, 112), (186, 178, 168))
LANTERN = (232, 170, 84)
INK2 = (14, 12, 18)


def doorward_sweep():
    """The Gate Porter's sweep (SAYO_BIBLE.md 3.6, the Worn: ash, one lantern-amber accent; never ember, violet or a
    pool colour): the bar draws back (2 frames), sweeps through the target in a wide flat arc (3 frames), HOLDS on
    contact (2 frames), ash chips scatter, the arc's trail fades. 14 frames."""
    out = []
    cx, cy = 25, 20
    for i in range(14):
        f = F.frame()
        if i < 2:                                                # wind-up: the bar's end at the right, a lantern glint
            A4.cluster(f, 41 - i, 14 + i, LANTERN, ASH[0])
        elif i < 5:                                              # the sweep: a flat arc right to left through the target
            t = (i - 1) / 3
            a1 = -40 + 220 * t
            n = F.frame()
            for w, col in ((5, ASH[1]), (2, ASH[2])):
                F.thick_arc(n, cx, cy, 18, max(-40, a1 - 80), a1, [(k - 2, col) for k in range(w)], ry_scale=0.62)
            F.outline_alpha(n, ASH[0])
            f.alpha_composite(n)
            x, y = cx + 18 * math.cos(math.radians(a1)), cy + 18 * 0.62 * math.sin(math.radians(a1))
            A4.cluster(f, x, y, LANTERN, ASH[0])
        elif i < 7:                                              # the held contact: the arc stops, the bar's end on them
            n = F.frame()
            F.thick_arc(n, cx, cy, 18, 40, 180, [(-2, ASH[1]), (-1, ASH[2]), (0, ASH[2]), (1, ASH[1]), (2, ASH[1])], ry_scale=0.62)
            F.outline_alpha(n, ASH[0])
            f.alpha_composite(n)
            A4.star(f, cx - 6, cy + 4, (255, 255, 250), 3)
        else:                                                    # ash chips scatter and fall; the trail fades
            v = i - 7
            if v < 3:
                F.thick_arc(f, cx, cy, 18, 60 + 25 * v, 180, [(0, ASH[1]), (1, ASH[1])], ry_scale=0.62)
            for k, (dx, dy) in enumerate(((-9, -2), (-4, -5), (3, -4), (-12, 2), (6, 1))):
                if v > 4 and k % 2:
                    continue
                A4.cluster(f, cx - 2 + dx * (1 + 0.12 * v), cy + 2 + dy + 0.3 * v * v, ASH[2] if k % 2 else ASH[1], ASH[0])
        out.append(f)
    return A4.edge_check("doorward sweep", out)


def the_quiet():
    """The Quiet (the Saint): ink lids close over the target like an eye shutting (3 frames), HELD shut (2 frames, one
    teal seam), open again (2 frames) and leave frozen dust settling. Clear of the portrait except the held beat."""
    out = []
    cx, cy, rx, ry = 25, 18, 15, 10
    for i in range(13):
        f = F.frame()
        if i < 2:                                                # anticipation: the lids gather at the rim
            F.thick_arc(f, cx, cy, rx + 2, 200, 340, [(0, INK2), (1, INK2)], ry_scale=ry / rx)
            F.thick_arc(f, cx, cy, rx + 2, 20, 160, [(0, INK2), (1, INK2)], ry_scale=ry / rx)
        elif i < 7:
            close = A4.ease((i - 1) / 3) if i < 5 else 1.0
            n = F.frame()
            d = ImageDraw.Draw(n)
            gap = (1 - close) * ry
            d.chord([cx - rx, cy - ry - 2, cx + rx, cy - gap + ry * 0.3], 180, 360, fill=(*INK2, 255))
            d.chord([cx - rx, cy + gap - ry * 0.3, cx + rx, cy + ry + 2], 0, 180, fill=(*INK2, 255))
            F.outline_alpha(n, (70, 84, 98))
            f.alpha_composite(n)
            if i >= 5:                                           # held shut: one teal seam, nothing moves
                F.seg(f, (cx - rx + 2, cy), (cx + rx - 2, cy), (146, 182, 191))
        elif i < 9:                                              # they open
            open_ = (i - 6) / 3
            F.thick_arc(f, cx, cy, rx + 1 + 2 * open_, 200, 340, [(0, INK2), (1, INK2)], ry_scale=ry / rx)
            F.thick_arc(f, cx, cy, rx + 1 + 2 * open_, 20, 160, [(0, INK2), (1, INK2)], ry_scale=ry / rx)
        else:                                                    # frozen dust settles
            v = i - 9
            for k, (dx, dy) in enumerate(((-12, -3), (11, -2), (-8, 6), (9, 7))):
                A4.cluster(f, cx + dx, cy + dy + v, (206, 210, 222), INK2)
        out.append(f)
    return A4.edge_check("the quiet", out)


# ------------------------------------------------------------------------------------------------ batch 4: follow marks, Act III heavy tune
EMB, EMB_Y = F.EMBER_RED, F.EMBER_YEL


VEIN_DIM, VEIN_LITB = (47, 92, 106), (146, 182, 191)   # SAYO_BIBLE.md 5.1: the variant's dim and lit veins (not #60d6ec)
OBS, OBS_L = (18, 23, 30), (39, 50, 60)


def heavy_tile_iii_b():
    """Act III heavy mark (QA B5): ember-rimmed obsidian, dim veins with a lit 1 px core, an ember core. No fill near
    safe cyan anywhere; the ember rim (2 px + a hot inner line) is what reads on dark floors."""
    t = F.frame()
    d = ImageDraw.Draw(t)
    d.polygon(A.poly10(25.0), fill=(*EMB, 255))
    d.polygon(A.poly10(23.6), fill=(*EMB_Y, 255))
    d.polygon(A.poly10(22.6), fill=(*SCORE, 255))
    d.polygon(A.poly10(21.6), fill=(*OBS_L, 255))
    d.polygon(A.poly10(19.4), fill=(*OBS, 255))
    for k in range(10):                                          # thorns on the rim, dark
        g = math.radians(k * 36)
        d.polygon([(25 + 21 * math.cos(g - 0.08), 25 + 21 * math.sin(g - 0.08)), (25 + 24 * math.cos(g), 25 + 24 * math.sin(g)),
                   (25 + 21 * math.cos(g + 0.08), 25 + 21 * math.sin(g + 0.08))], fill=(*OBS_L, 255))
    for a_, wob in ((30, 16), (128, 13), (212, 17), (300, 14)):
        pts = F.jag(25, 25, 4.5, 18, a_, wob, steps=5)
        d.line(pts, fill=(*VEIN_DIM, 255), width=2)
        d.line(pts[1:4], fill=(*VEIN_LITB, 255), width=1)
    d.ellipse([20, 20, 30, 30], fill=(*SCORE, 255))
    d.ellipse([21.5, 21.5, 28.5, 28.5], fill=(*EMB, 255))
    d.ellipse([23, 23, 27, 27], fill=(*EMB_Y, 255))
    m = Image.new("L", (50, 50), 0)
    ImageDraw.Draw(m).polygon(A.poly10(25.0), fill=255)
    out = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    out.paste(t, (0, 0), m)
    return F.tile_out(out)


def heavy_appear_iii_b(ring_inner=None):
    """Act III heavy arrival (QA S4, B5): 3 anticipation frames (the rim heats where it will land, nothing else
    moves), then it arrives DARK: an obsidian ring with a dim vein inner edge and the ember rim, contracting; ember
    chips fall (never rise), all inside the clip."""
    INKc = (14, 10, 22)
    inner = ring_inner or VEIN_DIM
    fr = []
    for i in range(13):
        f = F.frame()
        if i < 3:
            F.ground_ring(f, F.GRX - 1, F.GRY - 0.5, [(0, EMB if i < 2 else EMB_Y)])
        elif i <= 6:
            s_ = {3: 1.08, 4: 1.05, 5: 1.02, 6: 1.0}[i]
            F.ground_ring(f, (F.GRX - 1) * s_, (F.GRY - 0.5) * s_, [(-1, inner), (0, INKc if ring_inner is None else SCORE), (1, EMB_Y), (2, EMB)])
        else:
            t = i - 6
            for k in range(8):
                if t > 4 and k % 2:
                    continue
                g = math.radians(k * 45 + 20)
                x0, y0 = 25 + (F.GRX - 3) * math.cos(g), 25 + (F.GRY - 1.5) * math.sin(g)
                A4.cluster(f, x0 + math.cos(g) * t * 0.4, y0 + 0.25 * t * t, EMB_Y if t < 3 else EMB, SCORE)
        fr.append(f)
    return A4.edge_check("heavy appear iii", fr)


def close_in(act):
    """The follow mark (The Silence Turns / The Glass Turns, SAYO_BIBLE.md 3.7): the floor goes still before it
    breaks. Ink (III) or black cracks (II) run in from the hex's corners and close on it (5 frames), HOLD while the
    ember rim heats (2 frames), then the act's heavy mark arrives. Same strip on all seven hexes: drawn symmetric, so
    the ring reads as the floor closing on the player whatever their column."""
    p = A.PAL["II" if act == "ii" else "III"]
    line = (14, 10, 22) if act == "iii" else p["vein"]
    fr = []
    for i in range(7):
        f = F.frame()
        t = min(1.0, (i + 1) / 5)
        for k in range(6):
            a = math.radians(k * 60)
            x0, y0 = 25 + 17 * math.cos(a), 25 + 8.5 * math.sin(a)
            x1, y1 = x0 + (25 - x0) * t * 0.8, y0 + (25 - y0) * t * 0.8
            n = F.frame()
            ImageDraw.Draw(n).line([(x0, y0), (x1, y1)], fill=(*line, 255), width=2)
            F.outline_alpha(n, (70, 84, 98) if act == "iii" else SCORE)
            f.alpha_composite(n)
        if i >= 5:                                               # the hold: the rim heats, nothing moves
            F.ground_ring(f, F.GRX - 1, F.GRY - 0.5, [(0, EMB), (1, EMB_Y)])
        fr.append(f)
    tail = heavy_appear_iii_b() if act == "iii" else heavy_appear_iii_b(ring_inner=A.PAL["II"]["hot"])
    return A4.edge_check(f"close_in {act}", fr + tail)
