#!/usr/bin/env python3
"""pixelsnap_selftest.py - the exit test for pixelsnap.py.

Builds synthetic raws the way an image model paints them (pixel art enlarged by an odd factor,
shifted off the origin, softened, with stray specks), runs the tool, and asserts what it must
guarantee: the grid is found, the art pixels come back, small colour areas survive the palette,
speckles go and lines stay, refusals write nothing, output is deterministic, and the export
passes artpreflight.py --type JUTSU_ICON. Socket-free; needs Pillow only.
"""

from __future__ import annotations

import io
import json
import os
import random
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pixelsnap as ps  # noqa: E402

FAILS: list[str] = []
PALETTE = [(12, 14, 30), (30, 60, 160), (70, 130, 230), (230, 200, 90), (250, 245, 220),
           (120, 70, 40), (200, 60, 50), (60, 160, 90), (150, 90, 200), (90, 90, 100)]


def check(cond: bool, label: str) -> None:
    print(("ok    " if cond else "FAIL  ") + label)
    if not cond:
        FAILS.append(label)


def art(cells: int, seed: int) -> Image.Image:
    """Blocky pixel art: dark ground, a few big shapes, a one-pixel line, one speck."""
    rnd = random.Random(seed)
    im = Image.new("RGB", (cells, cells), PALETTE[0])
    d = ImageDraw.Draw(im)
    for _ in range(9):
        x, y = rnd.randrange(cells - 8), rnd.randrange(cells - 8)
        w, h = rnd.randrange(4, 14), rnd.randrange(4, 14)
        d.rectangle([x, y, min(cells - 1, x + w), min(cells - 1, y + h)], fill=rnd.choice(PALETTE[1:]))
    d.line([(2, cells - 4), (cells - 3, cells - 4)], fill=PALETTE[4])  # 1-px line
    return im


def model_raw(pix: Image.Image, cell: int, pad: tuple[int, int], soften: float = 0.9, specks: int = 0,
              seed: int = 1) -> Image.Image:
    """Enlarge like a model's pseudo-pixels, shift off the origin, soften, add specks."""
    big = pix.resize((pix.width * cell, pix.height * cell), Image.NEAREST)
    canvas = Image.new("RGB", (big.width + pad[0] + 9, big.height + pad[1] + 9), PALETTE[0])
    canvas.paste(big, pad)
    canvas = canvas.filter(ImageFilter.GaussianBlur(soften))
    rnd = random.Random(seed)
    dr = ImageDraw.Draw(canvas)
    for _ in range(specks):
        x, y = rnd.randrange(canvas.width - 3), rnd.randrange(canvas.height - 3)
        dr.rectangle([x, y, x + 1, y + 1], fill=(255, 255, 255))
    return canvas


def run(args: list[str]) -> tuple[int, dict | None, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = ps.main(args)
    rep = json.loads(out.getvalue()) if rc == 0 else None
    return rc, rep, err.getvalue()


def dist(a, b) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def main() -> int:
    tmp = tempfile.mkdtemp(prefix="pixelsnap_selftest_")
    p = lambda name: os.path.join(tmp, name)  # noqa: E731

    # 1. Grid recovery: 50 art pixels across, painted at 24 px each, shifted by (7, 11).
    src = art(50, seed=3)
    raw = model_raw(src, 24, (7, 11), specks=0)
    raw.save(p("raw50.png"))
    det = ps.detect(raw)
    check(det["detected"] and det["cell"] == 24, f"detects the 24 px pseudo-pixel (got {det['cell']}, score {det['score']})")
    check(det["phase_x"] == 7 and det["phase_y"] == 11, f"finds the (7, 11) offset (got {det['phase_x']}, {det['phase_y']})")
    rc, rep, _ = run([p("raw50.png"), p("out50.png"), "--denoise", "0", "--no-clean"])
    check(rc == 0 and rep["grid"] == 50 and rep["grid_source"] == "raw grid" and rep["aligned_to_raw_grid"],
          f"auto grid aligns to the raw's own 50-cell grid (got {rep and rep['grid']})")
    out = Image.open(p("out50.png")).convert("RGB").resize((50, 50), Image.NEAREST)
    a, b = list(src.getdata()), list(out.getdata())
    match = sum(1 for x, y in zip(a, b) if dist(x, y) < 40) / len(a)
    check(match >= 0.97, f"art pixels come back (match {match:.3f}, need 0.97)")
    check(any("not a multiple" in n for n in rep["notes"]), "uneven 256/50 scaling is reported")

    # 2. Palette size and exact 4x4 art pixels on the 64 grid.
    src64 = art(64, seed=5)
    model_raw(src64, 19, (3, 5)).save(p("raw64.png"))
    rc, rep, _ = run([p("raw64.png"), p("out64.webp"), "--colors", "16"])
    img = Image.open(p("out64.webp")).convert("RGB")
    check(rc == 0 and rep["grid"] == 64 and img.size == (256, 256), "64-cell raw -> 256 px lossless WebP")
    check(len(set(img.getdata())) <= 16, f"palette within --colors 16 (used {len(set(img.getdata()))})")
    blocks_ok = all(len({img.getpixel((x * 4 + i, y * 4 + j)) for i in range(4) for j in range(4)}) == 1
                    for y in range(64) for x in range(64))
    check(blocks_ok, "every art pixel is an exact 4x4 block (no mixels)")

    # 3. A small coloured area keeps its colour against a dominant hue.
    small = Image.new("RGB", (64, 64), (40, 90, 200))
    ImageDraw.Draw(small).rectangle([28, 28, 33, 33], fill=(130, 80, 40))
    for i in range(0, 64, 3):
        ImageDraw.Draw(small).line([(0, i), (63, i)], fill=(60 + i, 120, 220))
    ImageDraw.Draw(small).rectangle([28, 28, 33, 33], fill=(130, 80, 40))
    model_raw(small, 16, (2, 2)).save(p("rawsmall.png"))
    rc, rep, _ = run([p("rawsmall.png"), p("outsmall.png"), "--colors", "16"])
    o = Image.open(p("outsmall.png")).convert("RGB")
    centre = o.getpixel((124, 124))
    check(rc == 0 and dist(centre, (130, 80, 40)) < 45, f"small brown area survives the palette (got {centre})")

    # 4. Speckles go, a one-pixel line stays. The speck uses a palette colour, so only cleaning can remove it.
    spk = src.copy()
    spk.putpixel((25, 25), PALETTE[4])
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                spk.putpixel((25 + dx, 25 + dy), PALETTE[1])
    model_raw(spk, 24, (7, 11)).save(p("rawspeck.png"))
    rc, rep, _ = run([p("rawspeck.png"), p("outspeck.png"), "--denoise", "0"])
    o = Image.open(p("outspeck.png")).convert("RGB").resize((50, 50), Image.NEAREST)
    check(dist(o.getpixel((25, 25)), PALETTE[1]) < 40, "a lone speck is cleaned away")
    line = [o.getpixel((x, 46)) for x in range(5, 45)]
    check(sum(1 for c in line if dist(c, PALETTE[4]) < 50) >= 36, "the one-pixel line survives cleaning")
    check(rep["cleaned_pixels"] >= 1, "cleaned pixels are counted in the report")

    # 5. No grid: a smooth painterly raw falls back to the whole frame and 64 cells.
    rnd = random.Random(2)
    seedimg = Image.new("RGB", (12, 12))
    seedimg.putdata([tuple(rnd.randrange(256) for _ in range(3)) for _ in range(144)])
    seedimg.resize((900, 900), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3)).save(p("rawpaint.png"))
    rc, rep, _ = run([p("rawpaint.png"), p("outpaint.png")])
    check(rc == 0 and not rep["detection"]["detected"] and rep["grid"] == 64 and not rep["aligned_to_raw_grid"]
          and rep["region"] == [0, 0, 900, 900], "painterly raw: no grid, full frame, 64-cell fallback")
    check(any("no pseudo-pixel grid" in n for n in rep["notes"]), "missing grid is reported")

    # 5b. A raw grid outside 48-64 is not used for alignment: the full frame is resampled, uncropped.
    model_raw(art(30, seed=8), 30, (5, 5)).save(p("raw30.png"))
    rc, rep, _ = run([p("raw30.png"), p("out30.png")])
    w30 = Image.open(p("raw30.png")).size
    check(rc == 0 and rep["grid"] == 64 and not rep["aligned_to_raw_grid"] and rep["region"][2] - rep["region"][0] == min(w30),
          "a 30-cell raw grid is reported but not cropped to; 64-cell full-frame resample")

    # 6. Manual cell override.
    rc, rep, _ = run([p("raw50.png"), p("outman.png"), "--cell", "24", "--phase-x", "7", "--phase-y", "11", "--grid", "50"])
    check(rc == 0 and rep["detection"].get("manual") and rep["grid"] == 50, "--cell/--phase override is honoured")

    # 7. Refusals write nothing.
    Image.new("RGBA", (300, 300), (0, 0, 0, 0)).save(p("alpha.png"))
    cases = [
        ([p("alpha.png"), p("r1.png")], p("r1.png"), "transparent raw"),
        ([p("raw50.png"), p("r2.jpg")], p("r2.jpg"), "unsupported output extension"),
        ([p("raw50.png"), p("r3.png"), "--denoise", "4"], p("r3.png"), "even --denoise"),
        ([p("raw50.png"), p("r4.png"), "--colors", "1"], p("r4.png"), "--colors 1"),
        ([p("raw50.png"), p("r5.png"), "--grid", "abc"], p("r5.png"), "--grid abc"),
        ([p("missing.png"), p("r6.png")], p("r6.png"), "missing raw"),
    ]
    Image.new("RGB", (20, 20)).save(p("tiny.png"))
    cases.append(([p("tiny.png"), p("r7.png"), "--grid", "64"], p("r7.png"), "raw smaller than the grid"))
    for args, outp, label in cases:
        rc, _, err = run(args)
        check(rc == 1 and "REFUSED" in err and not os.path.exists(outp), f"refuses {label} and writes nothing")

    # 8. Deterministic.
    run([p("raw64.png"), p("d1.webp")])
    run([p("raw64.png"), p("d2.webp")])
    check(open(p("d1.webp"), "rb").read() == open(p("d2.webp"), "rb").read(), "same raw and options -> identical bytes")

    # 9. The export passes the real preflight.
    data_dir = os.path.join(os.path.dirname(HERE), "data")
    pre = subprocess.run([sys.executable, os.path.join(HERE, "artpreflight.py"), "--type", "JUTSU_ICON", p("out64.webp")],
                         cwd=data_dir, capture_output=True, text=True)
    check(pre.returncode == 0 and "0 errors" in pre.stdout, "export passes artpreflight.py --type JUTSU_ICON")

    print(f"\n{'PASS' if not FAILS else 'FAIL'}: {len(FAILS)} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
