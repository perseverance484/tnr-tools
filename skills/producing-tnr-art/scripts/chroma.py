#!/usr/bin/env python3
"""Component-based chroma keying for TNR art, the pipeline standard.

Global colour-keying is retired because it cannot tell three different things
apart that all read as "key colour": the background behind the subject, the
enclosed background inside a ring or a loop, and a glow the generator painted
INTO the subject. Keying them all makes holes in the art; keying none of them
leaves a coloured halo. So this classifies connected components instead.

The four stages:
  1. Flood-fill key-ish pixels inward from the canvas borders. Everything the
     flood reaches is background, whatever shape it is.
  2. Classify what the flood did not reach. A large component (>= MIN_ENCLOSED
     px) or one touching the border is enclosed background - a ring interior,
     a gap between limbs - and goes transparent.
  3. Split the small pockets by purity. HARD key colour is openwork (lace,
     loops, holes) and goes transparent; a DILUTED blend is glow or content the
     generator painted in the key hue, and gets luminance-matched remapped
     rather than punched out.
  4. Clamp the spill left on opaque edges, normalise alpha, and quantize if the
     file is over the upload ceiling.

One consequence of stage 1 worth knowing before you blame the script: the
flood crosses DILUTED key pixels as well as pure ones, so a glow that bridges
from the subject out to the background is reached by the flood and keyed away
with it. That is not a bug to route around - a glow touching the background is
indistinguishable from spill, and it is exactly why the prompt scaffolds ban
auras, halos, light fields and discs. A glow rendered as rim light that stays
inside the silhouette survives and gets remapped.

Two generator failures this CANNOT repair, by design:
  - painted glow blocks (a solid pale disc rendered as "glow"): that is art in
    the same palette as the subject, unkeyable without eating content.
  - a subject drawn resting on a surface: nothing to key, the composite is
    wrong at the source.
In both cases regenerate. Do not process.

Usage:
  python3 chroma.py in.png out.png --target SCENE_CHARACTER [--frame full|bust]
  python3 chroma.py in.png out.png --target AI_AVATAR --qc qc.png

  --target    THE spec-driven path, and the one to use. Reads
              25x_DATA_art_spec.json and derives the key, the pad ratio, the
              export format and mode, the byte ceiling and the minimum width
              from the target's block. An export cannot then come out at the
              wrong aspect, format or size, because none of those are typed by
              hand. Targets: SCENE_CHARACTER, SCENE_BACKGROUND, AI_AVATAR,
              ICON, STATIC, ANIMATION.
  --frame     SCENE_CHARACTER only: `full` pads to 2:3, `bust` to 1:1. The
              client width-scales scene characters and never letterboxes them
              (see spec targets.SCENE_CHARACTER.render), so the aspect decides
              how TALL the figure stands: 2:3 puts a standing figure at ~90% of
              scene height, 1:1 puts a bust at 60%. Both are correct for what
              they contain. Default `full`.
  --key       override the key the spec chose. lime (#00FF00) default; magenta
              (#FF00FF) for green-conflicting subjects, e.g. foliage or jade.
  --qc        write a dark-background composite so leftover spill and chewed
              edges are visible before upload. Always pass it, and look.

  Legacy flags (--pad-2-3, --square, --max-kb) still work and still export PNG.
  They are kept for scripts that predate the spec; new work uses --target.

"""
import argparse
import json
import os
import sys
from collections import deque

SPEC_PATH = os.environ.get("TNR_ART_SPEC", "25x_DATA_art_spec.json")


def load_spec(path=None):
    path = path or SPEC_PATH
    if not os.path.exists(path):
        sys.exit(
            f"spec not found: {path}\n"
            "chroma.py derives its numbers from 25x_DATA_art_spec.json rather than carrying "
            "copies. Copy it into the working directory or set TNR_ART_SPEC."
        )
    with open(path) as fh:
        return json.load(fh)


def resolve_target(spec, target, frame="full"):
    """Turn a target name into the concrete export settings the spec dictates.

    Everything here used to be a flag the operator remembered. Reading it instead means a
    wrong aspect or a lossy keyed export is not a mistake anyone can make."""
    t = spec["targets"].get(target)
    if t is None:
        sys.exit(f"unknown target {target}; spec has {', '.join(spec['targets'])}")

    aspect = t["aspect"]
    if aspect.get("accepted"):
        chosen = aspect.get("bust" if frame == "bust" else "full_body") or aspect["accepted"][0]
    else:
        chosen = aspect.get("value")

    pad = None
    if chosen and ":" in str(chosen):
        w, h = (int(v) for v in chosen.split(":"))
        pad = (w, h)

    return {
        "target": target,
        "aspect": chosen,
        "pad": pad,
        "key": t.get("chroma_key"),
        "format": t.get("format", "webp"),
        "format_mode": t.get("format_mode", "lossless"),
        "max_kb": int(t.get("byte_ceiling_bytes", 460800) / 1024),
        "min_width": t.get("min_width_px", {}).get("value"),
        "delivered_width": t.get("delivered_width_px"),
        "max_hw": (t.get("max_aspect_h_over_w") or {}).get("value"),
    }

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: pip install pillow --break-system-packages")

KEYS = {
    "lime":     {"channel": 1, "name": "lime",     "rgb": (0, 255, 0)},
    "magenta":  {"channel": None, "name": "magenta", "rgb": (255, 0, 255)},
}
MIN_ENCLOSED = 1200      # px; at or above this an unreached component is background
SPILL_CLAMP = 15         # how far a key-hued edge pixel is pulled back
ALPHA_FLOOR = 8          # below this, alpha is snapped to 0 so edges do not fringe


def is_keyish(px, key):
    r, g, b = px[0], px[1], px[2]
    if key == "lime":
        return g > 100 and g > r + 40 and g > b + 40
    return r > 100 and b > 100 and g < r - 40 and g < b - 40


def is_hard_key(px, key):
    r, g, b = px[0], px[1], px[2]
    if key == "lime":
        return g > 180 and r < 100 and b < 100
    return r > 180 and b > 180 and g < 100


def flood_from_borders(px, w, h, key):
    """Stage 1. Returns a bytearray mask: 1 where the flood reached."""
    mask = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_keyish(px[x, y], key):
                q.append((x, y))
                mask[y * w + x] = 1
    for y in range(h):
        for x in (0, w - 1):
            if is_keyish(px[x, y], key):
                q.append((x, y))
                mask[y * w + x] = 1
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not mask[ny * w + nx]:
                if is_keyish(px[nx, ny], key):
                    mask[ny * w + nx] = 1
                    q.append((nx, ny))
    return mask


def components(px, w, h, key, reached):
    """Stage 2/3. Key-ish pixels the flood did not reach, grouped."""
    seen = bytearray(w * h)
    out = []
    for sy in range(h):
        for sx in range(w):
            i = sy * w + sx
            if seen[i] or reached[i] or not is_keyish(px[sx, sy], key):
                continue
            comp, q, touches = [], deque([(sx, sy)]), False
            seen[i] = 1
            while q:
                x, y = q.popleft()
                comp.append((x, y))
                if x in (0, w - 1) or y in (0, h - 1):
                    touches = True
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    j = ny * w + nx
                    if 0 <= nx < w and 0 <= ny < h and not seen[j]:
                        if is_keyish(px[nx, ny], key):
                            seen[j] = 1
                            q.append((nx, ny))
            out.append((comp, touches))
    return out


def luma(px):
    return 0.299 * px[0] + 0.587 * px[1] + 0.114 * px[2]


def process(path_in, path_out, key="lime", pad=None, max_kb=450, qc=None,
            fmt="png", fmt_mode="lossless", min_width=None, max_hw=None):
    img = Image.open(path_in).convert("RGBA")
    w, h = img.size
    px = img.load()
    log = {"size": (w, h), "key": key}

    reached = flood_from_borders(px, w, h, key)
    log["background_px"] = sum(reached)

    comps = components(px, w, h, key, reached)
    enclosed = holes = remapped = 0
    for comp, touches in comps:
        if len(comp) >= MIN_ENCLOSED or touches:
            for x, y in comp:
                reached[y * w + x] = 1
            enclosed += len(comp)
            continue
        for x, y in comp:
            if is_hard_key(px[x, y], key):
                reached[y * w + x] = 1
                holes += 1
            else:
                L = luma(px[x, y])
                px[x, y] = (int(L * 0.88), int(L * 0.94), int(L), px[x, y][3])
                remapped += 1
    log["enclosed_px"], log["hole_px"], log["remapped_px"] = enclosed, holes, remapped

    # apply alpha, then clamp spill on what survives
    for y in range(h):
        for x in range(w):
            if reached[y * w + x]:
                px[x, y] = (0, 0, 0, 0)
                continue
            r, g, b, a = px[x, y]
            if key == "lime" and g > r + SPILL_CLAMP and g > b + SPILL_CLAMP:
                g = max(r, b) + SPILL_CLAMP
            elif key == "magenta" and r > g + SPILL_CLAMP and b > g + SPILL_CLAMP:
                m = g + SPILL_CLAMP
                r, b = min(r, m), min(b, m)
            if a < ALPHA_FLOOR:
                a = 0
            px[x, y] = (r, g, b, a)

    img = img.crop(img.getbbox() or (0, 0, w, h))
    if pad:
        img = pad_to_ratio(img, pad)
    log["out_size"] = img.size

    # Refuse rather than ship an undersized export. Padding fixes an aspect; nothing fixes
    # a source that was never big enough, and a silent nearest-neighbour upscale would hide
    # a generation fault behind a file that passes every other check.
    if min_width and img.size[0] < min_width:
        log["UNDER_MIN_WIDTH"] = f"{img.size[0]}px against a {min_width}px minimum"

    if max_hw and img.size[1] / img.size[0] > max_hw + 1e-6:
        log["OVER_CLIP_BOUND"] = f"h/w {img.size[1] / img.size[0]:.3f} exceeds {max_hw:.3f}"

    kb = _export(img, path_out, fmt, fmt_mode)
    log["format"] = f"{fmt} {fmt_mode}"
    if kb > max_kb:
        img = img.quantize(colors=255, method=Image.FASTOCTREE).convert("RGBA")
        kb = _export(img, path_out, fmt, fmt_mode)
        log["quantized"] = True
    log["kb"] = kb
    if kb > max_kb:
        log["OVER_BUDGET"] = True

    if qc:
        bg = Image.new("RGBA", img.size, (18, 18, 22, 255))
        bg.alpha_composite(img)
        bg.convert("RGB").save(qc)
        log["qc"] = qc
    return log


def pad_to_ratio(img, ratio):
    """Pad transparent to an exact aspect. The subject keeps its share of the
    canvas, which is what determines apparent size in the client: a small
    subject needs headroom or it gets scaled to human height."""
    tw, th = ratio
    w, h = img.size
    target_h = max(h, int(round(w * th / tw)))
    target_w = max(w, int(round(target_h * tw / th)))
    out = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    out.paste(img, ((target_w - w) // 2, target_h - h))
    return out


def _export(img, path, fmt, mode):
    """Write in the format the spec names.

    webp lossless for keyed art: lossy rings around the hard edges this style is built from,
    and the ringing survives the CDN downsample that everything else forgives. webp lossy at
    q85 for backgrounds, which carry no alpha and no keyed edge.
    """
    fmt = (fmt or "png").lower()
    if fmt == "webp":
        if mode == "lossy_q85":
            img.convert("RGB").save(path, "WEBP", lossless=False, quality=85, method=6)
        else:
            img.save(path, "WEBP", lossless=True, quality=100, method=6)
    elif fmt in ("jpg", "jpeg"):
        img.convert("RGB").save(path, "JPEG", quality=90, optimize=True)
    else:
        img.save(path, "PNG", optimize=True)
    return _kb(path)


def _kb(p):
    import os
    return round(os.path.getsize(p) / 1024, 1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--target", help="spec target: SCENE_CHARACTER, AI_AVATAR, ICON, ...")
    ap.add_argument("--frame", choices=["full", "bust"], default="full")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--key", choices=sorted(KEYS), default=None)
    ap.add_argument("--pad-2-3", action="store_true")
    ap.add_argument("--square", action="store_true")
    ap.add_argument("--max-kb", type=int, default=None)
    ap.add_argument("--qc")
    a = ap.parse_args()

    if a.target:
        cfg = resolve_target(load_spec(a.spec), a.target, a.frame)
        key = a.key or cfg["key"] or "lime"
        pad = cfg["pad"]
        max_kb = a.max_kb or cfg["max_kb"]
        fmt, fmt_mode = cfg["format"], cfg["format_mode"]
        min_width, max_hw = cfg["min_width"], cfg["max_hw"]
        want_ext = "." + fmt
        if not a.dst.lower().endswith(want_ext):
            sys.exit(
                f"target {a.target} exports {fmt}, but the output filename is {a.dst}.\n"
                "The @img reference resolves by exact filename, so the extension is part of "
                "the contract and this script will not quietly rename it."
            )
    else:
        key = a.key or "lime"
        pad = (2, 3) if a.pad_2_3 else (1, 1) if a.square else None
        max_kb = a.max_kb or 450
        fmt, fmt_mode = "png", "lossless"
        min_width = max_hw = None

    report = process(a.src, a.dst, key, pad, max_kb, a.qc, fmt, fmt_mode, min_width, max_hw)
    if a.target:
        report["target"] = a.target + (f" ({a.frame})" if a.target == "SCENE_CHARACTER" else "")
        report["aspect"] = resolve_target(load_spec(a.spec), a.target, a.frame)["aspect"]
    for k, v in report.items():
        print(f"{k}: {v}")

    fatal = [k for k in ("OVER_BUDGET", "UNDER_MIN_WIDTH", "OVER_CLIP_BOUND") if k in report]
    if fatal:
        print("\nFAILED: " + ", ".join(fatal))
        sys.exit(1)
