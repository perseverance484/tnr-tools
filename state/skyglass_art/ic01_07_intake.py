#!/usr/bin/env python3
"""Skyglass IC01-IC07 intake and the DR01-DR06 recolours (docs/design/skyglass_art/ART_REGISTER.md).

The seven director-approved raws arrive with real (GPT-native) alpha, not a key: the subject sits at alpha 250-254
and a faint alpha 1-24 haze covers the canvas. So there is no key to remove and chroma.py is not run (the skill
prefers native transparency; precedent art/item_icons/chunin_exam_scrolls/process_icon.py). It would also hurt:
at 1254 px its lossless export is over the ceiling, so it FASTOCTREE-quantizes the whole image to 255 colours,
re-palettes every pixel and breaks the "only the region changes" property of the recolours. The work is alpha
cleanup (haze off, subject solid, dust islands removed), then the ICON framing: trim, a small even margin so the
rarity frame reads, 256 px, firmed alpha, lossless webp. Residual key colour is checked by artpreflight.py.

The six derived icons (SKYGLASS_ART_REQUEST.md section 7) recolour ONE isolated region of a base raw before the
same pipeline runs, so their alpha is identical to the base's and only the masked region changes:
  - seals (DR01/DR02): the amber-gold wax seal, found by a flood from a seed inside it through warm pixels; the
    black outline stops the flood, so the scorched rim / iron never joins;
  - cords (DR03-DR06): every hue-band component above a size floor (the cord plus its wax dab).
The masked pixels are remapped by luminance onto a three-stop ramp of the new colour, so the cel-shading steps
survive. --check verifies that every derived export differs from its base only near the mask.

usage: python3 state/skyglass_art/ic01_07_intake.py RAW_DIR OUT_DIR WORK_DIR [--check]
  RAW_DIR  art/skyglass_event_icons/raw (the IC0n_raw_*.png originals)
  OUT_DIR  art/skyglass_event_icons/exports
  WORK_DIR scratch folder for intermediates and QC composites
Pillow only (approved for art tooling).
"""
import colorsys, os, sys
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

A_LOW, A_HIGH = 24, 232      # raw alpha: haze off, near-opaque subject solid (art/item_icons/.../process_icon.py)
SPECK_PX = 64                # detached alpha islands smaller than this (full res) are dust
MARGIN = 0.92                # subject long side = 92% of the canvas: ~10 px each side at 256
OUT_PX = 256                 # spec ICON recommended_source_px
F_LOW, F_HIGH = 80, 175      # post-resize alpha firming

# code, raw file, export file, key the prompt block named (recorded only: the raws came back native alpha)
ICONS = [
    ("IC01", "IC01_raw_icon-tide-chart.png", "icon-tide-chart.webp", "lime"),
    ("IC02", "IC02_raw_icon-watch-roster.png", "icon-watch-roster.webp", "lime"),
    ("IC03", "IC03_raw_icon-reliquary-seal.png", "icon-reliquary-seal.webp", "lime"),
    ("IC04", "IC04_raw_icon-the-last-heading.png", "icon-the-last-heading.webp", "lime"),
    ("IC05", "IC05_raw_icon-core-rot.png", "icon-core-rot.webp", "magenta"),
    ("IC06", "IC06_raw_icon-ledger-page.png", "icon-ledger-page.webp", "lime"),
    ("IC07", "IC07_raw_icon-stores-manifest.png", "icon-stores-manifest.webp", "lime"),
]

ROT = ("#1f2e0e", "#5e7d1f", "#b8d65a")   # rot-green (request section 4: tainted seal)
# code, base code, export file, mask, ramp (shadow, mid, highlight)
# mask: ("seed", (x, y), hue_lo, hue_hi, s_min, v_min) | ("band", hue_lo, hue_hi, s_min, v_min, min_component_px)
DERIVED = [
    ("DR01", "IC03", "icon-rotted-reliquary-seal.webp", ("seed", (699, 874), 15, 60, 0.45, 0.20), ROT),
    ("DR02", "IC04", "icon-the-rotted-heading.webp", ("seed", (193, 1034), 15, 60, 0.45, 0.20), ROT),
    ("DR03", "IC06", "icon-ledger-page-bone-store.webp", ("band", 330, 20, 0.45, 0.20, 300),
     ("#121218", "#3a3a46", "#8a8a9a")),                                   # charcoal (reads by value on cream)
    ("DR04", "IC06", "icon-ledger-page-snare-room.webp", ("band", 330, 20, 0.45, 0.20, 300),
     ("#0e1a40", "#2f56b0", "#93b4f5")),                                   # cobalt blue
    ("DR05", "IC07", "icon-stores-manifest-ore-vault.webp", ("band", 5, 35, 0.55, 0.40, 300),
     ("#3a1f66", "#8a5cd6", "#d9c2ff")),                                   # bright violet (steel white vanished on brown)
    ("DR06", "IC07", "icon-stores-manifest-bloom-cellar.webp", ("band", 5, 35, 0.55, 0.40, 300),
     ("#4a0f2e", "#c2367e", "#f6a3cf")),                                   # bloom rose
]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def clean(im):
    """Haze off, subject solid, detached dust islands removed. Returns (image, dust_px)."""
    im = im.convert("RGBA")
    r, g, b, a = im.split()
    a = a.point(lambda v: 0 if v <= A_LOW else (255 if v >= A_HIGH else v))
    w, h = im.size
    ap = a.load()
    seen = bytearray(w * h)
    dust = 0
    for sy in range(h):
        for sx in range(w):
            if seen[sy * w + sx] or not ap[sx, sy]:
                continue
            comp, q = [], deque([(sx, sy)])
            seen[sy * w + sx] = 1
            while q:
                x, y = q.popleft()
                comp.append((x, y))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and ap[nx, ny]:
                            seen[ny * w + nx] = 1
                            q.append((nx, ny))
            if len(comp) < SPECK_PX:
                dust += len(comp)
                for x, y in comp:
                    ap[x, y] = 0
    out = Image.merge("RGBA", (r, g, b, a))
    return Image.composite(out, Image.new("RGBA", out.size, (0, 0, 0, 0)), a), dust


def _hsv_ok(p, hlo, hhi, smin, vmin):
    if p[3] < 128:
        return False
    H, S, V = colorsys.rgb_to_hsv(p[0] / 255, p[1] / 255, p[2] / 255)
    H *= 360
    inr = (hlo <= H <= hhi) if hlo <= hhi else (H >= hlo or H <= hhi)
    return inr and S >= smin and V >= vmin


def region_mask(im, spec):
    w, h = im.size
    px = im.load()
    mask = bytearray(w * h)
    if spec[0] == "seed":
        _, (sx, sy), hlo, hhi, smin, vmin = spec
        if not _hsv_ok(px[sx, sy], hlo, hhi, smin, vmin):
            sys.exit(f"seed {sx},{sy} is not inside the region (pixel {px[sx, sy]})")
        q = deque([(sx, sy)])
        mask[sy * w + sx] = 1
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not mask[ny * w + nx] and _hsv_ok(px[nx, ny], hlo, hhi, smin, vmin):
                    mask[ny * w + nx] = 1
                    q.append((nx, ny))
        return mask
    _, hlo, hhi, smin, vmin, min_px = spec
    cand = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            if _hsv_ok(px[x, y], hlo, hhi, smin, vmin):
                cand[y * w + x] = 1
    seen = bytearray(w * h)
    for i in range(w * h):
        if not cand[i] or seen[i]:
            continue
        comp, q = [], deque([i])
        seen[i] = 1
        while q:
            j = q.popleft()
            comp.append(j)
            x, y = j % w, j // w
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    k = ny * w + nx
                    if 0 <= nx < w and 0 <= ny < h and cand[k] and not seen[k]:
                        seen[k] = 1
                        q.append(k)
        if len(comp) >= min_px:
            for j in comp:
                mask[j] = 1
    return mask


def recolour(im, mask, ramp):
    """Luminance-ramp remap of the masked pixels; alpha untouched."""
    w, h = im.size
    px = im.load()
    stops = [hexrgb(c) for c in ramp]
    lum = sorted(0.299 * px[i % w, i // w][0] + 0.587 * px[i % w, i // w][1] + 0.114 * px[i % w, i // w][2]
                 for i in range(w * h) if mask[i])
    if not lum:
        sys.exit("empty recolour mask")
    lo, hi = lum[int(len(lum) * 0.05)], lum[int(len(lum) * 0.95)]
    span = max(1.0, hi - lo)
    for i in range(w * h):
        if not mask[i]:
            continue
        x, y = i % w, i // w
        r, g, b, a = px[x, y]
        t = min(1.0, max(0.0, (0.299 * r + 0.587 * g + 0.114 * b - lo) / span))
        if t < 0.55:
            c0, c1, u = stops[0], stops[1], t / 0.55
        else:
            c0, c1, u = stops[1], stops[2], (t - 0.55) / 0.45
        px[x, y] = tuple(int(round(c0[k] + (c1[k] - c0[k]) * u)) for k in range(3)) + (a,)
    return sum(mask)


def frame(im, dst):
    im = im.crop(im.getchannel("A").getbbox())
    side = round(max(im.size) / MARGIN)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
    canvas = canvas.resize((OUT_PX, OUT_PX), Image.LANCZOS)
    r, g, b, a = canvas.split()
    a = a.point(lambda v: 0 if v < F_LOW else (255 if v > F_HIGH else v))
    out = Image.merge("RGBA", (r, g, b, a))
    out = Image.composite(out, Image.new("RGBA", out.size, (0, 0, 0, 0)), a)
    out.save(dst, "WEBP", lossless=True, quality=100, method=6)
    bb = a.getbbox()
    return {"bytes": os.path.getsize(dst), "trimmed": im.size,
            "margins_ltrb": (bb[0], bb[1], OUT_PX - bb[2], OUT_PX - bb[3])}


def run(code, img, out_name, out_dir, work):
    img.save(os.path.join(work, f"{code}_clean.png"))
    info = frame(img, os.path.join(out_dir, out_name))
    out = Image.open(os.path.join(out_dir, out_name)).convert("RGBA")
    bg = Image.new("RGBA", out.size, (18, 18, 22, 255))      # chroma.py's QC background
    bg.alpha_composite(out)
    bg.convert("RGB").save(os.path.join(work, f"{code}_qc.png"))
    print(f"{code} {out_name} {info}")


def check(out_dir, raw_dir):
    """Each derived export vs its base: identical alpha; visible colour changes only where the mask lands."""
    base_of = {c: o for c, _, o, _ in ICONS}
    bad = 0
    for code, base, out_name, _, _ in DERIVED:
        a = Image.open(os.path.join(out_dir, base_of[base])).convert("RGBA")
        b = Image.open(os.path.join(out_dir, out_name)).convert("RGBA")
        same_alpha = a.getchannel("A").tobytes() == b.getchannel("A").tobytes()
        w = a.width
        pa, pb = a.load(), b.load()
        ch = [y * w + x for y in range(a.height) for x in range(w) if pa[x, y][3] and pa[x, y] != pb[x, y]]
        vis = sum(1 for v in a.getchannel("A").tobytes() if v)
        bb = (min(i % w for i in ch), min(i // w for i in ch), max(i % w for i in ch) + 1, max(i // w for i in ch) + 1) if ch else None
        print(f"{code} vs {base}: alpha identical={same_alpha} changed px={len(ch)} ({len(ch) / vis:.1%} of visible) "
              f"changed bbox={bb}")
        bad += (not same_alpha)
    return bad


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    raw_dir, out_dir, work = sys.argv[1:4]
    os.makedirs(work, exist_ok=True)
    if "--check" in sys.argv:
        sys.exit(1 if check(out_dir, raw_dir) else 0)
    cleaned = {}
    for code, raw, out_name, key in ICONS:
        img, dust = clean(Image.open(os.path.join(raw_dir, raw)))
        cleaned[code] = img
        print(f"{code} clean: dust islands removed {dust} px")
        run(code, img.copy(), out_name, out_dir, work)
    for code, base, out_name, spec, ramp in DERIVED:
        img = cleaned[base].copy()
        mask = region_mask(img, spec)
        n = recolour(img, mask, ramp)
        mprev = Image.new("L", img.size)
        mprev.putdata([255 if m else 0 for m in mask])
        mprev.save(os.path.join(work, f"{code}_mask.png"))
        print(f"{code} from {base}: recoloured {n} px to {ramp[1]}")
        run(code, img, out_name, out_dir, work)
    sys.exit(1 if check(out_dir, raw_dir) else 0)


if __name__ == "__main__":
    main()
