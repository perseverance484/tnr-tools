#!/usr/bin/env python3
"""pixelsnap.py - turn an image model's "pixel art style" raw into real pixel art.

Image models paint pseudo-pixels: blocks of uneven size, bleeding edges, off-grid placement and
palettes of thousands of colours. This tool rebuilds the picture on ONE true pixel grid with a
small fixed palette, so the 256 px export is genuine pixel art (no mixed pixel sizes).

    python3 pixelsnap.py RAW.png OUT.png [--grid auto|N] [--colors 24] [--size 256] [--denoise 5]
                         [--cell N --phase-x X --phase-y Y] [--no-clean] [--report OUT.json]
    python3 pixelsnap.py RAW.png OUT.webp ...     # .webp is written lossless

Steps (all deterministic):
  1. detect   look for the raw's pseudo-pixel cell size and phase (quarter-pixel steps) in the
              periodic peaks of its column and row edge profiles (computed in C by Pillow; no
              NumPy). Detection is advisory: generated raws usually have pseudo-pixels of about
              9-11 px (115-140 across) or no clean grid at all.
  2. grid     --grid auto aligns to the raw's own grid only when it has 48-64 cells across;
              otherwise it divides the full frame into 64 cells (no cropping).
  3. cells    lightly denoise the raw (median filter, --denoise), divide the grid extent into cells
              and give each cell the most frequent colour of its inner area, voting with a fine
              96-colour palette (cell borders, where pseudo-pixels bleed, are ignored).
  4. palette  choose the final --colors palette from the cells themselves (maximum coverage refined by
              k-means, no dithering), so small coloured areas keep their colour.
  5. clean    remove speckles: a pixel matching none of its edge neighbours takes the colour that
              holds five of its eight neighbours (--no-clean skips this).
  6. export   scale the grid up with nearest neighbour to --size (exact when --size is a
              multiple of --grid; otherwise reported as uneven) and write PNG or lossless WebP.

Defaults follow RUL-2026-10-24-002 (deep dive C1/C2): about 48-64 art pixels across, 16-24
colours. 64 is the fallback grid because 256 / 64 = 4 keeps every art pixel exactly 4x4; a raw grid
of, say, 54 gives art pixels of 4 or 5 px at 256, which the game's own downscaling hides.

The tool never judges what the picture depicts and never uploads anything. The export still goes
through artpreflight.py --type JUTSU_ICON (or jutsu_studio.py finalize) like any other icon.

Exit codes: 0 written; 1 refused (bad input or options), nothing written.
Zero network. Needs Pillow.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
from collections import Counter

from PIL import Image, ImageChops, ImageFilter

APPROVED_GRID = (48, 64)       # RUL-2026-10-24-002, C1
APPROVED_COLORS = (16, 24)     # RUL-2026-10-24-002, C2 / deep dive 6.4
MIN_CELL, MAX_CELL = 2, 64     # pseudo-pixel sizes searched, in raw pixels (quarter-pixel steps)
CONFIDENT = 1.35               # comb score at or above this counts as a detected grid
INNER = 0.25                   # fraction of each cell edge ignored when voting
VOTE_COLORS = 96               # fine palette the cells vote with, before the final palette


class Refused(Exception):
    pass


def pixels(img: Image.Image) -> list:
    """Flat pixel list on any Pillow version (getdata is deprecated from Pillow 12)."""
    f = getattr(img, "get_flattened_data", None)
    return list(f() if f else img.getdata())


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def edge_profile(img: Image.Image, axis: str) -> list[float]:
    """Mean absolute luminance step between neighbouring columns (axis='x') or rows ('y')."""
    g = img.convert("L")
    w, h = g.size
    if axis == "x":
        a, b = g.crop((1, 0, w, h)), g.crop((0, 0, w - 1, h))
        d = ImageChops.difference(a, b)
        prof = pixels(d.resize((w - 1, 1), Image.BOX))
    else:
        a, b = g.crop((0, 1, w, h)), g.crop((0, 0, w, h - 1))
        d = ImageChops.difference(a, b)
        prof = pixels(d.resize((1, h - 1), Image.BOX))
    # prof[i] is the step between pixel i and i+1, i.e. a boundary at position i+1
    return [0.0] + [float(v) for v in prof]


def comb(profile: list[float], period: float) -> tuple[float, int]:
    """Best (score, phase) for boundaries every `period` pixels (period may be fractional).
    Score = mean profile on the comb / overall mean."""
    n = len(profile)
    mean = sum(profile) / n or 1e-9
    best = (0.0, 0)
    for phase in range(int(period + 0.999)):
        pts = []
        k = 0
        while True:
            i = int(phase + k * period + 0.5)
            if i >= n:
                break
            pts.append(profile[i])
            k += 1
        if len(pts) < 4:
            continue
        s = (sum(pts) / len(pts)) / mean
        if s > best[0]:
            best = (s, phase)
    return best


def detect(img: Image.Image) -> dict:
    """Pseudo-pixel cell size (in quarter-pixel steps; model pseudo-pixels are rarely whole pixels)
    and phase, shared by both axes."""
    px, py = edge_profile(img, "x"), edge_profile(img, "y")
    scores = {}
    top_p = min(MAX_CELL, min(img.size) // 4)
    p = float(MIN_CELL)
    while p <= top_p:
        sx, fx = comb(px, p)
        sy, fy = comb(py, p)
        scores[p] = ((sx + sy) / 2, fx, fy)
        p += 0.25
    if not scores:
        return {"detected": False, "cell": None, "phase_x": 0, "phase_y": 0, "score": 0.0}
    top = max(v[0] for v in scores.values())
    # Multiples of the true period score as well as the period itself; take the smallest period
    # that is nearly as strong as the best one.
    cell = min(q for q, v in scores.items() if v[0] >= 0.9 * top)
    score, fx, fy = scores[cell]
    return {"detected": score >= CONFIDENT, "cell": cell, "phase_x": fx, "phase_y": fy,
            "score": round(score, 3)}


def extent(size: int, cell: float, phase: int) -> tuple[int, int]:
    """Start and end of the whole cells that fit on one axis."""
    n = int((size - phase) // cell)
    return phase, int(round(phase + n * cell))


def snap(raw: Image.Image, grid: int, colors: int, cell: float | None, phase_x: int, phase_y: int,
         align: bool, clean: bool, denoise: int) -> tuple[Image.Image, dict]:
    """Rebuild `raw` on a grid x grid art-pixel grid. With `align`, the grid is the raw's own
    detected grid and cells follow its pseudo-pixels; otherwise the full frame is divided evenly."""
    w, h = raw.size
    if align and cell:
        x0, x1 = extent(w, cell, phase_x)
        y0, y1 = extent(h, cell, phase_y)
    else:
        x0, x1, y0, y1 = 0, w, 0, h
    region = raw.crop((x0, y0, x1, y1))
    # A square grid over a near-square region: keep the shorter side so cells stay square.
    side = min(region.size)
    ox, oy = (region.size[0] - side) // 2, (region.size[1] - side) // 2
    region = region.crop((ox, oy, ox + side, oy + side))
    if denoise:
        region = region.filter(ImageFilter.MedianFilter(denoise))
    # Stage 1: every cell votes with a fine palette, so small coloured areas keep their colour.
    fine = region.quantize(colors=VOTE_COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    idx, fp = fine.load(), fine.getpalette()
    cells = Image.new("RGB", (grid, grid))
    o = cells.load()
    step = side / grid
    for gy in range(grid):
        for gx in range(grid):
            ax, bx = gx * step, (gx + 1) * step
            ay, by = gy * step, (gy + 1) * step
            mx, my = (bx - ax) * INNER, (by - ay) * INNER
            xs = range(int(ax + mx), max(int(ax + mx) + 1, int(bx - mx)))
            ys = range(int(ay + my), max(int(ay + my) + 1, int(by - my)))
            votes = Counter(idx[x, y] for y in ys for x in xs if x < side and y < side)
            k = min(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0]
            o[gx, gy] = tuple(fp[3 * k:3 * k + 3])
    # Stage 2: the final palette is chosen from the cells, weighted by area at the art-pixel level.
    out = cells.quantize(colors=colors, method=Image.Quantize.MAXCOVERAGE, kmeans=4, dither=Image.Dither.NONE)
    cleaned = clean_strays(out) if clean else 0
    info = {"region": [x0 + ox, y0 + oy, x0 + ox + side, y0 + oy + side],
            "aligned_to_raw_grid": bool(align and cell),
            "cleaned_pixels": cleaned}
    return out, info


def clean_strays(img: Image.Image) -> int:
    """Replace speckles: a pixel matching none of its four edge neighbours, where one colour holds at
    least five of its eight neighbours, takes that colour. Lines survive (they match an edge
    neighbour). Returns the number of pixels changed."""
    w, h = img.size
    src = img.copy().load()
    dst = img.load()
    n = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            c = src[x, y]
            if c in (src[x + 1, y], src[x - 1, y], src[x, y + 1], src[x, y - 1]):
                continue
            ring = [src[x + dx, y + dy] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy]
            m, cnt = min(Counter(ring).items(), key=lambda kv: (-kv[1], kv[0]))
            if cnt >= 5:
                dst[x, y] = m
                n += 1
    return n


def write(img: Image.Image, path: str) -> bytes:
    ext = os.path.splitext(path)[1].lower()
    rgb = img.convert("RGB")
    if ext == ".webp":
        buf = io.BytesIO()
        rgb.save(buf, "WEBP", lossless=True, quality=100, method=6, exact=True)
        data = buf.getvalue()
    elif ext == ".png":
        buf = io.BytesIO()
        rgb.save(buf, "PNG", optimize=True)
        data = buf.getvalue()
    else:
        raise Refused(f"output must be .png or .webp, not {ext or 'no extension'}")
    with open(path, "wb") as f:
        f.write(data)
    return data


def run(args: argparse.Namespace) -> dict:
    if not os.path.isfile(args.raw):
        raise Refused(f"no such file: {args.raw}")
    raw_bytes = open(args.raw, "rb").read()
    try:
        raw = Image.open(args.raw)
        raw.load()
    except Exception as e:  # noqa: BLE001 - any decode failure is a refusal
        raise Refused(f"cannot decode {args.raw}: {e}")
    if raw.mode in ("RGBA", "LA", "PA") or (raw.mode == "P" and "transparency" in raw.info):
        lo = raw.convert("RGBA").getextrema()[3][0]
        if lo < 255:
            raise Refused("raw has transparency; jutsu icons are opaque (key or flatten it first)")
    raw = raw.convert("RGB")
    if not 2 <= args.colors <= 256:
        raise Refused("--colors must be 2..256")
    if args.grid != "auto":
        try:
            args.grid = int(args.grid)
        except ValueError:
            raise Refused("--grid must be 'auto' or a number")
        if not 8 <= args.grid <= 256:
            raise Refused("--grid must be 8..256")
    if args.cell is not None:
        if not MIN_CELL <= args.cell <= min(raw.size) // 2:
            raise Refused(f"--cell must be {MIN_CELL}..{min(raw.size) // 2}")
        det = {"detected": True, "cell": args.cell, "phase_x": int(args.phase_x % args.cell),
               "phase_y": int(args.phase_y % args.cell), "score": None, "manual": True}
    else:
        det = detect(raw)
    if args.grid == "auto":
        across = None
        if det["detected"] and det["cell"]:
            across = int(min((raw.size[0] - det["phase_x"]) // det["cell"], (raw.size[1] - det["phase_y"]) // det["cell"]))
        grid = across if across and APPROVED_GRID[0] <= across <= APPROVED_GRID[1] else 64
        grid_source = "raw grid" if across and grid == across else "default 64"
    else:
        grid, grid_source = args.grid, "requested"
    if min(raw.size) < grid:
        raise Refused(f"raw is {raw.size[0]}x{raw.size[1]}, smaller than the {grid}-cell grid")
    if args.size < grid:
        raise Refused("--size must be at least the grid")
    if args.denoise and (args.denoise < 3 or args.denoise % 2 == 0):
        raise Refused("--denoise must be 0 or an odd number from 3")
    args.grid = grid
    align = grid_source == "raw grid" or (args.cell is not None)
    grid_img, info = snap(raw, grid, args.colors, det["cell"], det["phase_x"], det["phase_y"],
                          align, not args.no_clean, args.denoise)
    out = grid_img.resize((args.size, args.size), Image.NEAREST)
    data = write(out, args.out)
    used = len(set(pixels(grid_img)))
    notes = []
    if not det["detected"]:
        notes.append("no pseudo-pixel grid detected; the whole frame was resampled")
    elif not info["aligned_to_raw_grid"]:
        notes.append(f"raw grid of {det['cell']} px is outside the approved density; the whole frame was resampled to {grid}")
    if args.size % args.grid:
        notes.append(f"{args.size} is not a multiple of {args.grid}: art pixels are {args.size // args.grid} or "
                     f"{args.size // args.grid + 1} px wide (uneven)")
    if not APPROVED_GRID[0] <= args.grid <= APPROVED_GRID[1]:
        notes.append(f"grid {args.grid} is outside the approved {APPROVED_GRID[0]}-{APPROVED_GRID[1]} (RUL-2026-10-24-002)")
    if not APPROVED_COLORS[0] <= args.colors <= APPROVED_COLORS[1]:
        notes.append(f"{args.colors} colours is outside the approved {APPROVED_COLORS[0]}-{APPROVED_COLORS[1]}")
    return {
        "tool": "pixelsnap.py", "raw": args.raw, "raw_sha256": sha256_bytes(raw_bytes),
        "raw_size": list(raw.size), "detection": det, "region": info["region"],
        "aligned_to_raw_grid": info["aligned_to_raw_grid"], "grid": args.grid, "grid_source": grid_source,
        "denoise": args.denoise, "colors_requested": args.colors,
        "colors_used": used, "cleaned_pixels": info["cleaned_pixels"], "out": args.out,
        "out_size": [args.size, args.size], "out_sha256": sha256_bytes(data), "out_bytes": len(data),
        "notes": notes,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("raw")
    ap.add_argument("out")
    ap.add_argument("--grid", default="auto", help="art pixels across: auto (the raw's own grid when it is 48-64, else 64) or a number")
    ap.add_argument("--colors", type=int, default=24, help="palette size (default 24; approved 16-24)")
    ap.add_argument("--size", type=int, default=256, help="output width and height (default 256)")
    ap.add_argument("--cell", type=float, help="override the detected pseudo-pixel size (raw pixels; fractional allowed)")
    ap.add_argument("--phase-x", type=int, default=0)
    ap.add_argument("--phase-y", type=int, default=0)
    ap.add_argument("--no-clean", action="store_true", help="keep isolated single pixels")
    ap.add_argument("--denoise", type=int, default=5, help="median filter size on the raw before voting (odd, 0 = off; default 5)")
    ap.add_argument("--report", help="also write the report JSON here")
    args = ap.parse_args(argv)
    try:
        rep = run(args)
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    text = json.dumps(rep, indent=1)
    if args.report:
        with open(args.report, "w") as f:
            f.write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
