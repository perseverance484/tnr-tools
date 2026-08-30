#!/usr/bin/env python3
"""
artpreflight.py - acceptance check for processed TNR art, against 25x_DATA_art_spec.json.

Art had no equivalent of validate.py: nothing checked an asset before handover, so aspect,
byte and filename faults were caught by eye or by a player. This closes that.

    python3 artpreflight.py <dir-or-file>... [--spec 25x_DATA_art_spec.json]
                                             [--manifest manifest.json]
                                             [--type SCENE_CHARACTER]
                                             [--json]

Type is inferred from the filename when not given (see TYPE_HINTS). Every file must resolve
to a target in the spec or it is an error, because an unclassified asset is one that nobody
checked.

Exit code is the error count, so it drops into a pipeline the same way validate.py does.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("error  Pillow is required: pip install pillow --break-system-packages")
    sys.exit(1)


# --------------------------------------------------------------------------- spec

DEFAULT_SPEC = "25x_DATA_art_spec.json"


def load_spec(path: str) -> dict:
    if not os.path.exists(path):
        raise SystemExit(f"error  spec not found: {path}")
    with open(path) as fh:
        return json.load(fh)


# Filename -> target. Ordered; first match wins. Kept deliberately dumb: an explicit
# --type always beats inference, and an un-inferable name is an error, not a guess.
TYPE_HINTS = [
    (re.compile(r"(scene[_-]?char|_char\b|portrait|_sc_)", re.I), "SCENE_CHARACTER"),
    # `_scene_` is deliberately NOT a background hint: it matches `boss_scene_char` too,
    # and the ambiguity guard would then refuse every correctly-named scene character.
    (re.compile(r"(scene[_-]?bg|background|_bg\b|_bg_|^bg_)", re.I), "SCENE_BACKGROUND"),
    (re.compile(r"(avatar|_ai_|sprite)", re.I), "AI_AVATAR"),
    (re.compile(r"(icon|_item_|_jutsu_|^img_)", re.I), "ICON"),
    (re.compile(r"(pin|_static_|marker)", re.I), "STATIC"),
    (re.compile(r"(anim|_frames?\d|sheet)", re.I), "ANIMATION"),
]


def infer_type(filename: str) -> str | None:
    """
    Refuses to guess when a filename matches more than one target.

    First-match-wins looked fine until `bad_portrait_avatar.webp` classified as a scene
    character because "portrait" is checked before "avatar". An ambiguous name is exactly
    the case where a silent wrong answer is worse than an error.
    """
    base = os.path.basename(filename)
    hits = {target for pattern, target in TYPE_HINTS if pattern.search(base)}
    if len(hits) == 1:
        return hits.pop()
    return None


def webp_mode(path: str) -> str | None:
    """
    'lossless', 'lossy' or None, read from the RIFF chunk layout.

    A plain lossless file is RIFF/WEBP/VP8L and a plain lossy one is RIFF/WEBP/'VP8 '.
    Anything carrying alpha or metadata is wrapped in an extended VP8X container and the
    real codec chunk sits further in, which is what the first version of this check missed:
    it saw VP8X, assumed lossless, and passed a lossy export of every keyed asset.
    """
    with open(path, "rb") as fh:
        data = fh.read(4096)
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    fourcc = data[12:16]
    if fourcc == b"VP8L":
        return "lossless"
    if fourcc == b"VP8 ":
        return "lossy"
    if fourcc != b"VP8X":
        return None
    # Extended container: walk chunks from byte 12 until a codec chunk turns up.
    pos = 12
    while pos + 8 <= len(data):
        cid = data[pos : pos + 4]
        size = int.from_bytes(data[pos + 4 : pos + 8], "little")
        if cid == b"VP8L":
            return "lossless"
        if cid == b"VP8 ":
            return "lossy"
        pos += 8 + size + (size & 1)
    return None


def parse_ratio(text: str) -> float:
    """'2:3' -> 0.6667 (width/height)."""
    w, h = text.split(":")
    return float(w) / float(h)


# --------------------------------------------------------------------------- checks

class Report:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, level: str, path: str, check: str, message: str) -> None:
        self.rows.append(
            {"level": level, "file": os.path.basename(path), "check": check, "message": message}
        )

    def error(self, path: str, check: str, message: str) -> None:
        self.add("error", path, check, message)

    def warn(self, path: str, check: str, message: str) -> None:
        self.add("warn", path, check, message)

    def note(self, path: str, check: str, message: str) -> None:
        self.add("note", path, check, message)

    @property
    def errors(self) -> int:
        return sum(1 for r in self.rows if r["level"] == "error")

    @property
    def warnings(self) -> int:
        return sum(1 for r in self.rows if r["level"] == "warn")


def soft_edge_share(img: Image.Image) -> float | None:
    """
    Share of pixels with a partial alpha, over the pixels that carry any alpha at all.

    Keyed pixel art has hard edges: a high partial-alpha share means either the key ate a
    gradient or the export was resampled after keying. Returns None for an opaque image.
    """
    if img.mode != "RGBA":
        return None
    alpha = img.getchannel("A")
    hist = alpha.histogram()
    opaque = hist[255]
    partial = sum(hist[8:250])
    visible = opaque + partial + sum(hist[250:255]) + sum(hist[1:8])
    if visible == 0:
        return None
    return partial / visible


def check_file(path: str, target: str, spec: dict, report: Report, img_refs: set[str] | None) -> None:
    t = spec["targets"].get(target)
    if t is None:
        report.error(path, "type", f"no spec target named {target}")
        return

    try:
        img = Image.open(path)
        img.load()
    except Exception as exc:  # noqa: BLE001
        report.error(path, "open", f"cannot open: {exc}")
        return

    w, h = img.size
    ratio = w / h
    size_bytes = os.path.getsize(path)
    ext = os.path.splitext(path)[1].lower().lstrip(".")

    # ---- aspect  (law 50: only avatars/icons/backgrounds stretch)
    aspect = t["aspect"]
    tol = aspect.get("tolerance", 0.01)
    accepted = aspect.get("accepted")
    if accepted:
        hits = [a for a in accepted if abs(ratio - parse_ratio(a)) <= tol]
        # A full-body scene character is a BAND, not a point: the ratified exemplars run
        # 0.594-0.696 and a single tolerance around 2:3 rejects three of them.
        lo_hi = aspect.get("full_body_band")
        if not hits and lo_hi and lo_hi[0] <= ratio <= lo_hi[1]:
            hits = [f"full-body band {lo_hi[0]}-{lo_hi[1]}"]
        if not hits:
            report.error(
                path,
                "aspect",
                f"{w}x{h} is {ratio:.4f}; spec accepts {' or '.join(accepted)} "
                f"({', '.join(f'{parse_ratio(a):.4f}' for a in accepted)}) within {tol}",
            )
        else:
            report.note(path, "aspect", f"{w}x{h} matches {hits[0]}")
    elif aspect.get("value") == "per_frame_1:1":
        report.note(path, "aspect", "per-frame check needs --frames; sheet ratio not checked")
    elif aspect.get("value"):
        want = parse_ratio(aspect["value"])
        if abs(ratio - want) > tol:
            report.error(
                path,
                "aspect",
                f"{w}x{h} is {ratio:.4f}; spec requires {aspect['value']} ({want:.4f}) within {tol}",
            )
        else:
            report.note(path, "aspect", f"{w}x{h} matches {aspect['value']}")

    # ---- clipping bound (scene characters only)  # law 81
    bound = t.get("max_aspect_h_over_w")
    if bound:
        hw = h / w
        if hw > bound["value"]:
            report.error(
                path,
                "clip_bound",
                f"h/w {hw:.3f} exceeds {bound['value']:.3f} ({bound['value_label']}); "
                f"the client clips the top",
            )

    # ---- dimensions
    min_w = t.get("min_width_px", {}).get("value")
    if min_w and w < min_w:
        report.error(path, "min_width", f"{w}px is under the {min_w}px minimum")

    delivered = t.get("delivered_width_px")
    if delivered and w > delivered * 4:
        report.warn(
            path,
            "oversize",
            f"{w}px against a delivered width of {delivered}px; the CDN discards the excess "
            f"and it costs upload bytes only",
        )

    # ---- bytes
    ceiling = t.get("byte_ceiling_bytes")
    hard = spec["upload"]["hard_cap_bytes"]
    if size_bytes > hard:
        report.error(
            path, "bytes", f"{size_bytes / 1024:.1f}KB exceeds the {hard / 1024:.0f}KB presign hard cap"
        )
    elif ceiling and size_bytes > ceiling:
        report.error(
            path,
            "bytes",
            f"{size_bytes / 1024:.1f}KB exceeds the {ceiling / 1024:.0f}KB working ceiling",
        )

    # ---- format
    want_fmt = t.get("format")
    if want_fmt and ext != want_fmt:
        report.error(path, "format", f"extension .{ext}; spec requires .{want_fmt}")
    if ext == "webp" and t.get("format_mode") == "lossless":
        mode = webp_mode(path)
        if mode is None:
            report.error(path, "format_mode", "not a readable RIFF/WEBP container")
        elif mode != "lossless":
            report.error(
                path,
                "format_mode",
                f"{mode} webp; spec requires lossless for keyed art (lossy rings the hard edges)",
            )

    # ---- alpha
    if t.get("chroma_key") is not None and img.mode != "RGBA":
        report.error(path, "alpha", f"mode {img.mode}; a keyed asset must carry an alpha channel")
    if t.get("chroma_key") is None and img.mode == "RGBA":
        report.warn(path, "alpha", "carries alpha; backgrounds should be flattened")

    # ---- soft edges
    share = soft_edge_share(img)
    max_share = spec["house_style"]["measured_signature"]["soft_edge_share_max"]
    if share is not None:
        if share > max_share:
            report.error(
                path,
                "soft_edges",
                f"{share:.1%} partial-alpha pixels against a {max_share:.0%} ceiling; "
                f"the key ate a gradient or the file was resampled after keying",
            )
        else:
            report.note(path, "soft_edges", f"{share:.1%}")

    # ---- residual key colour
    if t.get("chroma_key"):
        residual = residual_key(img, spec["chroma"]["keys"])
        if residual:
            name, count = residual
            report.error(
                path, "spill", f"{count} pixels still near the {name} key; raise the spill clamp"
            )

    # ---- filename contract
    if img_refs is not None:
        if os.path.basename(path) not in img_refs:
            report.error(
                path,
                "img_ref",
                "no @img reference in the manifest matches this filename exactly",
            )


def residual_key(img: Image.Image, keys: dict) -> tuple[str, int] | None:
    """Count visible pixels still sitting near a key colour. Any is a fault."""
    if img.mode != "RGBA":
        rgba = img.convert("RGBA")
    else:
        rgba = img
    small = rgba.resize((min(rgba.width, 256), min(rgba.height, 256)))
    px = small.load()
    targets = {}
    for name, hexval in keys.items():
        h = hexval.lstrip("#")
        targets[name] = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    counts = {name: 0 for name in targets}
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, a = px[x, y]
            if a < 32:
                continue
            for name, (tr, tg, tb) in targets.items():
                if abs(r - tr) < 40 and abs(g - tg) < 40 and abs(b - tb) < 40:
                    counts[name] += 1
    for name, count in counts.items():
        if count > 0:
            return name, count
    return None


# --------------------------------------------------------------------------- library audit

INDEX_TYPE_MAP = {"SCENE_CHARACTER": "SCENE_CHARACTER", "SCENE_BACKGROUND": "SCENE_BACKGROUND",
                  "STATIC": "STATIC", "ANIMATION": "ANIMATION"}


def audit_index(index_path: str, spec: dict) -> dict:
    """
    Audit the LIVE library against the spec, from an art_index harvest.

    The per-file checks above need the bytes; this needs only dimensions, size and format,
    which is what the mirror already collects. It exists because the defects that actually
    reach players are population-scale - a hundred assets in the wrong format, one image
    doing the work of fourteen NPCs - and no per-file check will ever see them.
    """
    with open(index_path) as fh:
        index = json.load(fh)
    assets = index["assets"]
    out = {"total": len(assets), "buckets": {}}

    def bucket(name):
        return out["buckets"].setdefault(name, [])

    # one image, many records
    by_url = {}
    for a in assets:
        by_url.setdefault(a["url"], []).append(a)
    for url, rows in by_url.items():
        if len(rows) < 2:
            continue
        named = [r for r in rows if (r.get("name") or "").strip().lstrip("/").lower() != "placeholder"]
        junk = len(rows) - len(named)
        bucket("shared_image").append({
            "records": len(rows), "named_content": len(named), "placeholder_records": junk,
            "px": f"{rows[0]['w']}x{rows[0]['h']}", "kb": rows[0]["kb"],
            "examples": [r["name"] for r in named[:5]],
        })

    for a in assets:
        target = INDEX_TYPE_MAP.get(a.get("type"))
        t = spec["targets"].get(target) if target else None
        if not t or not a.get("w"):
            continue
        ratio = a["w"] / a["h"]
        aspect = t["aspect"]
        tol = aspect.get("tolerance", 0.01)
        accepted = aspect.get("accepted") or ([aspect["value"]] if aspect.get("value") else [])
        band = aspect.get("full_body_band")
        ok = any(abs(ratio - parse_ratio(x)) <= tol for x in accepted if ":" in str(x))
        if not ok and band and band[0] <= ratio <= band[1]:
            ok = True
        if accepted and not ok:
            bucket("wrong_aspect").append(
                {"name": a["name"], "type": a["type"], "px": f"{a['w']}x{a['h']}", "aspect": round(ratio, 3)}
            )
        cb = t.get("max_aspect_h_over_w")
        if cb and a["h"] / a["w"] > cb["value"]:
            bucket("clipped").append(
                {"name": a["name"], "px": f"{a['w']}x{a['h']}",
                 "top_clipped": round((a["h"] / a["w"]) / cb["value"] - 1, 3)}
            )
        mw = t.get("min_width_px", {}).get("value")
        if mw and a["w"] < mw:
            bucket("under_min_width").append({"name": a["name"], "type": a["type"], "w": a["w"], "min": mw})
        if a.get("format") and a["format"] != "image/" + t.get("format", "webp"):
            bucket("wrong_format").append({"name": a["name"], "type": a["type"], "format": a["format"], "kb": a["kb"]})
        if a["kb"] > spec["upload"]["working_ceiling_bytes"] / 1024:
            bucket("over_working_ceiling").append({"name": a["name"], "kb": a["kb"]})
        if a["kb"] < 3:
            bucket("sub_3kb").append({"name": a["name"], "type": a["type"], "px": f"{a['w']}x{a['h']}", "kb": a["kb"]})
    return out


def render_audit(out: dict) -> str:
    lines = [f"LIBRARY AUDIT  {out['total']} records", ""]
    order = ["shared_image", "wrong_aspect", "clipped", "under_min_width",
             "wrong_format", "over_working_ceiling", "sub_3kb"]
    for name in order:
        rows = out["buckets"].get(name, [])
        lines.append(f"{name}  ({len(rows)})")
        for r in rows[:12]:
            lines.append("    " + json.dumps(r))
        if len(rows) > 12:
            lines.append(f"    ... {len(rows) - 12} more")
        lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- manifest

def manifest_img_refs(path: str) -> set[str]:
    with open(path) as fh:
        raw = fh.read()
    return set(re.findall(r"@img:([A-Za-z0-9_.\-]+)", raw))


# --------------------------------------------------------------------------- main

def collect(paths: list[str]) -> list[str]:
    out: list[str] = []
    exts = {".png", ".webp", ".jpg", ".jpeg"}
    for p in paths:
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if os.path.splitext(name)[1].lower() in exts:
                    out.append(os.path.join(p, name))
        else:
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--index", default=None, help="audit a live art_index harvest instead of files")
    ap.add_argument("--spec", default=DEFAULT_SPEC)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--type", default=None, help="force a target for every file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    spec = load_spec(args.spec)

    if args.index:
        out = audit_index(args.index, spec)
        if args.json:
            print(json.dumps(out, indent=1))
        else:
            print(render_audit(out))
        return 0

    refs = manifest_img_refs(args.manifest) if args.manifest else None
    report = Report()

    files = collect(args.paths)
    if not files:
        print("error  no image files found")
        return 1

    for path in files:
        target = args.type or infer_type(path)
        if target is None:
            report.error(
                path,
                "type",
                "cannot infer a target from the filename; pass --type or rename to the convention",
            )
            continue
        check_file(path, target, spec, report, refs)

    if args.json:
        print(json.dumps({"rows": report.rows, "errors": report.errors}, indent=1))
    else:
        for row in report.rows:
            if row["level"] == "note":
                continue
            print(f"{row['level']:6} {row['file']}  [{row['check']}] {row['message']}")
        print(f"\n{report.errors} errors, {report.warnings} warnings, {len(files)} files")

    return report.errors


if __name__ == "__main__":
    sys.exit(main())
