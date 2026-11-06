#!/usr/bin/env python3
"""Mother of Echoes, S9: the Flood and the enrage as lattice-periodic paintings (coordinator option b, 2026-11-05).

    python3 art/mother_of_echoes_fx/build_fx_field.py --spec SPEC --out DIR [--which flood,enrage]

Both are near-whole-arena fields. The picture is ONE painting over the hall whose content repeats every 2 columns and 3
rows (a lattice vector both ways), so a hex's slice depends only on (col mod 2, row mod 3), its wave band and whether a
missed hex borders it; identical slices are collapsed by content hash (visually invisible sharing, director's rule).
The wave is a per-band lead of empty frames (SAYO_BIBLE.md 3.4: "waves sweep across the field so the fall reads as one
ceiling"): the Flood rolls out from the hall's middle, the enrage sweeps the hall column-band by column-band.
Masked to the hexes the cast hits: nothing draws over a safe hex.

The unit animation (Act III, the Remainder; SAYO_BIBLE.md 5.1):
- Flood ("every pane in the hall lit at once except three places"): 0-3 the hall's veins kindle teal under the panes;
  4-6 HOLD white-teal (identical); 7-11 thorned black shards stand up out of every pane seam over a void bloom; 12-16
  they break, chunks thrown and falling; 17-23 it settles to frozen teal cracks and dissolves onto the Act III floor.
- Enrage ("every pane answers: the corrupted burst rolls across the hall"): the same hall, corrupted: black cracks race
  through the panes first, the hold is a void-violet flash, the shards are taller and the bloom wider; settles the same.
Pillow only.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import math
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("build_fx_paint", os.path.join(HERE, "build_fx_paint.py"))
P = importlib.util.module_from_spec(_s)
_s.loader.exec_module(P)
MZ, A4, F = P.MZ, P.A4, P.F
R3, WHITE, SCORE = P.R3, P.WHITE, P.SCORE
BOARD = [(c, r) for c in range(12) for r in range(10)]
PX, PY = 60, 60                     # the pattern's period: 2 columns, 3 rows (both lattice vectors)
LEAD = 2                            # frames between wave bands


def unit_tile(seed):
    """One period of the hall's pane pattern: lozenge seams (u = x - 2y, v = x + 2y, period 60) and teal veins
    (random walks wrapped on the period). Returns per-pixel classes for a PX x PY tile."""
    rnd = random.Random(seed)
    seam, vein = set(), set()
    for y in range(PY):
        for x in range(PX):
            u, v = (x - 2 * y) % 60, (x + 2 * y) % 60
            if min(u, 60 - u) < 1.5 or min(v, 60 - v) < 1.5:
                seam.add((x, y))
    for _ in range(3):
        x, y, a = rnd.uniform(0, PX), rnd.uniform(0, PY), rnd.uniform(0, math.pi)
        for _s in range(90):
            x += math.cos(a); y += 0.5 * math.sin(a); a += rnd.uniform(-0.4, 0.4)
            vein.add((int(x) % PX, int(y) % PY))
    shards = [(rnd.uniform(0, PX), rnd.uniform(0, PY), rnd.randint(11, 19), rnd.choice((3, 3, 4)), rnd.uniform(-0.3, 0.3))
              for _ in range(9)]                              # bigger, so they read over the floor (coordinator, lift)
    return seam, vein, shards


def unit_frames(cv, rm, kind, seed=5, frames=24):
    seam, vein, shards = unit_tile(seed)
    pts = [(x, y) for y in range(cv.h) for x in range(cv.w) if rm.getpixel((x, y))]
    cls = {p: ((p[0] % PX, p[1] % PY) in seam, (p[0] % PX, p[1] % PY) in vein) for p in pts}
    # the shards at every period translate inside the canvas
    allsh = []
    for oy in range(-PY, cv.h + PY, PY):
        for ox in range(-PX, cv.w + PX, PX):
            for (sx, sy, h, w, tilt) in shards:
                x, y = ox + sx, oy + sy
                if 0 <= x < cv.w and 0 <= y < cv.h and rm.getpixel((int(x), int(y))):
                    allsh.append((x, y, h * (1.35 if kind == "enrage" else 1.0), w, tilt))
    out = []
    corrupt = kind == "enrage"
    for i in range(frames):
        f = cv.frame()
        px = f.load()
        if i < 4:                                            # anticipation: the veins kindle (enrage: black cracks first)
            g = (i + 1) / 4
            for p, (s_, v_) in cls.items():
                if v_:
                    px[p] = (*((R3["deep"] if corrupt and i < 2 else R3["vdim"]) if g < 0.6 else R3["vlit"]), 255)
                elif s_ and F.BAYER[p[1] % 4][p[0] % 4] < g * 16:
                    px[p] = (*(R3["deep"] if corrupt else R3["frame"]), 255)
        elif i == 4:                                         # the wave's white crest: this band's front arriving
            for p, (s_, v_) in cls.items():              # lines only: no flat pale fill (it tore under skew, QA S4)
                if v_ or s_:
                    px[p] = (*WHITE, 255)
        elif i < 7:                                          # HOLD: two identical frames
            for p, (s_, v_) in cls.items():
                if v_ or s_:
                    px[p] = (*(R3["hot"] if v_ else (R3["vdim"] if not corrupt else R3["void"])), 255)
                elif corrupt and F.BAYER[p[1] % 4][p[0] % 4] < 2:     # a sparse void tint, low contrast (QA S4)
                    px[p] = (*R3["void"], 255)
        elif i < 12:                                         # shards stand up out of the seams over the void bloom
            v = i - 6
            for p, (s_, v_) in cls.items():
                if F.BAYER[p[1] % 4][p[0] % 4] < (0.35 + (0.15 if corrupt else 0)) * 16:
                    px[p] = (*R3["void"], 255)
                elif v_:
                    px[p] = (*R3["vlit"], 255)
            n = cv.frame()
            d = ImageDraw.Draw(n)
            for (x, y, h, w, tilt) in allsh:
                hh = h * min(1.0, v / 2.5)
                tip = (x + tilt * hh, y - hh)
                d.polygon([(x - w, y), (x + w, y), tip], fill=(*R3["body"], 255))
                d.polygon([(x - w, y), (x - w * 0.2, y), tip], fill=(*R3["lit"], 255))          # the lit face
                d.line([(x - w + 0.5, y - 1), tip], fill=(*(R3["hot"] if v < 4 else R3["vlit"]), 255), width=1)
                d.line([(x + w, y), tip], fill=(*R3["vlit"], 255))
                P.F.px(n, *tip, WHITE)
            F.outline_alpha(n, R3["deep"])
            f.alpha_composite(n)
        elif i < 17:                                         # they break: chunks thrown and falling
            u = i - 11
            for p, (s_, v_) in cls.items():
                if F.BAYER[p[1] % 4][p[0] % 4] < (0.3 - 0.05 * u) * 16:
                    px[p] = (*R3["void"], 255)
            for k, (x, y, h, w, tilt) in enumerate(allsh):
                for j in range(2):
                    cx = x + (j * 2 - 1) * (1 + 1.2 * u) + tilt * h
                    cy = y - h * (0.4 + 0.3 * j) - 1.8 * u + 0.5 * u * u
                    if cy < y + 4 and (u < 4 or (k + j) % 2):
                        P.cluster(f, cx, cy, R3["body"] if j else R3["lit"], R3["deep"])
        else:                                                # settle: frozen teal cracks dissolve onto the floor
            keep = 1.0 - (i - 16) / (frames - 17)
            for p, (s_, v_) in cls.items():
                if v_ and F.BAYER[p[1] % 4][p[0] % 4] < keep * 16:
                    px[p] = (*(R3["vlit"] if i < 19 else R3["vdim"]), 255)
                elif s_ and F.BAYER[p[1] % 4][p[0] % 4] < keep * 0.4 * 16:
                    px[p] = (*R3["frame"], 255)
        out.append(P.masked(f, rm))
    return out


def bands(kind, cells):
    if kind == "enrage":
        return {k: k[0] // 3 for k in cells}                 # 4 column bands, left to right
    return {k: min(3, int(4 * max(abs(k[0] - 5.5) / 6, abs(k[1] - 4.5) / 5))) for k in cells}   # out from the middle


def strip_bytes(frames):
    b = io.BytesIO()
    F.strip(frames).save(b, "WEBP", lossless=True, quality=100, method=6)
    return b.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--which", default="flood,enrage")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    spec = json.load(open(a.spec))
    names = {"flood": "The Names Flood In", "enrage": "The Glass Remembers"}
    rows = []
    for kind in a.which.split(","):
        # a spec id (e.g. moe-saint-flood-rime) paints that record; its region is <field>_<spec id> in the gen
        byid = {j["id"]: j for j in spec["jutsu"]}
        if kind in byid:
            rec, region, field = byid[kind]["record"], None, ("flood" if "flood" in kind else "enrage")
            region = f"{field}_{kind.split('-')[-1]}"          # moe-saint-flood-rime -> flood_rime (the gen's region)
        else:
            rec = next(j["record"] for j in spec["jutsu"] if j["record"]["name"] == names[kind])
            region, field = kind, kind
        cells = [(c["longitude"], c["latitude"]) for c in rec["coordinateTargeting"]["coordinates"]]
        cv = MZ.Canvas(BOARD)
        sub = MZ.Canvas(BOARD)
        sub.cells = list(cells)
        rm = P.region_mask(sub)
        fr = unit_frames(cv, rm, field)
        sl = cv.slices(fr)
        bd = bands(field, cells)
        uniq = {}
        for k in sorted(cells):
            strip = [F.frame() for _ in range(bd[k] * LEAD)] + sl[k]
            data = strip_bytes(strip)
            h = hashlib.sha1(data).hexdigest()[:10]
            if h not in uniq:
                fn = f"anim_moe_{region.replace('moe-saint-', '')}_s{len(uniq):02d}_a14.webp"
                open(os.path.join(a.out, fn), "wb").write(data)
                uniq[h] = fn
            rows.append({"file": uniq[h], "region": region, "col": k[0], "row": k[1], "frames": len(strip), "band": bd[k]})
        print(kind, len(cells), "hexes ->", len(uniq), "unique strips")
    json.dump({"slices": rows}, open(os.path.join(a.out, f"moe_fx_field_{a.which.replace(',', '_')}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
