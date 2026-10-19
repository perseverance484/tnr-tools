#!/usr/bin/env python3
"""jutsu_studio.py - offline ZIP-first tooling for the Bloodline Jutsu Icon Art Studio.

Governing protocol: docs/workflows/ISOLATED_ART_GENERATION.md (P0 target lock, fail-fast
gate, studio intake s4, deterministic-only family gallery s4a, processing policy s5).
Build contract: state/prompt_jutsu_icon_p1_tooling_20261019.md (RUL-2026-10-19-005).
The art spec's JUTSU_ICON target (data/25x_DATA_art_spec.json) owns every number used
here; nothing is restated. This tool records studio and director judgements and refuses
inconsistent records. It never decides whether pixels depict the locked technique.

    python3 jutsu_studio.py doctor                                   # can this container run it canonically?
    python3 jutsu_studio.py intake PACK.zip --out WORK/intake [--roster roster.json|.csv]
    python3 jutsu_studio.py lock-check WORK/locks.json [--source-index WORK/intake/source_index.json]
    python3 jutsu_studio.py attempts WORK/attempts.json [--locks WORK/locks.json]
    python3 jutsu_studio.py compare CANDIDATE.png FAMILY1.webp ... --out WORK/compare [--label c1]
    python3 jutsu_studio.py verify-approved WORK/approved.json [--locks ..] [--attempts ..]
    python3 jutsu_studio.py finalize WORK/approved.json --out WORK/final [--label v1]
                                     [--source-index ..] [--locks ..] [--attempts ..]
    python3 jutsu_studio.py audit-gallery GALLERY.png --manifest showcase_manifest.json --exports DIR
    python3 jutsu_studio.py bench [--sizes 5,8,12]                    # socket-free timing run

intake         Safe, bounded ZIP scan (no traversal/absolute paths/symlinks/duplicates/case
               collisions/bombs, CRC checked), true-format decode, SHA-256 per member, exact
               jutsu ID/name mapping from manifest.json or --roster with an evidence level
               (never current-live), and the pinned JUTSU_ICON style exemplars.
lock-check     Target-lock completeness: identity, action, silhouette, camera/motion axis,
               secondary effect, sibling exclusions, reference roles, anatomy exception and
               a direction approval bound to the exact lock contents.
attempts       Validates the studio's generation-attempt log (restart after two wrong-subject/
               composition failures, references, anatomy) and reports failure statistics.
compare        Non-generative 125/64/32 review aid: candidate beside family files. Not a gallery.
finalize       verify-approved -> cached lossless VP8L export -> the real artpreflight.py
               --type JUTSU_ICON (canonical only when its script/spec blobs match the pins)
               -> deterministic count-adaptive showcase, audited from its written bytes ->
               closeout ZIP and flat WebP ZIP. Every stage re-hashes its inputs.
audit-gallery  VALID/INVALID for any gallery PNG against its manifest and the export bytes.

Exit codes: 0 success; 1 refused or failed (nothing claimed); 3 finished but incomplete
(MAPPING_REQUIRED rows, LOCK_INCOMPLETE, or preflight not canonically runnable).

Zero network, zero game requests, no upload capability. Needs Pillow.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath

try:
    import PIL
    from PIL import Image, ImageDraw, ImageFont, features
except ImportError:  # pragma: no cover
    print("error  Pillow is required: pip install pillow", file=sys.stderr)
    raise SystemExit(1)

TOOL_VERSION = "1.1.0"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SPEC = SCRIPT_DIR.parent / "data" / "25x_DATA_art_spec.json"
DEFAULT_PREFLIGHT = SCRIPT_DIR / "artpreflight.py"
DEFAULT_PINS = SCRIPT_DIR.parent / "data" / "preflight_pins.json"
TARGET = "JUTSU_ICON"

# ZIP intake bounds. Generous for a family pack (a few originals plus identity art),
# small enough that a hostile archive cannot exhaust the sandbox.
MAX_MEMBERS = 400
MAX_MEMBER_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024
MAX_RATIO = 200
MAX_IMAGE_PIXELS = 50_000_000
IGNORED_PREFIXES = ("__MACOSX/",)
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
SUFFIX_FORMAT = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP", ".gif": "GIF"}
FORMAT_EXT = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp", "GIF": ".gif"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)

# Showcase geometry (ISOLATED_ART_GENERATION.md s4a: equal square tiles, one caption
# band, neutral dark gutters, no frames). Fixed so a rerun is pixel-identical.
TILE, GUTTER, MARGIN, CAPTION = 350, 28, 28, 64
BG = (13, 17, 28)
TEXT = (232, 235, 242)
TEXT_DIM = (150, 160, 182)
PHONE_WIDTH = 1080
QC_SIZES = (125, 64, 32)

Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS

# Roster evidence levels. Tooling never asserts that a roster is current-live.
EVIDENCE_LEVELS = ("historical_capture", "director_roster", "current_live_unverified")

# Gate vocabulary (retrospective state table K, RUL-2026-10-19-005 D7).
GATES = ("ORIGINAL_SOURCE_VERIFIED", "DIRECTION_APPROVED", "RAW_VISUAL_APPROVED", "OUTPUT_LOCAL_QC",
         "CANONICAL_PREFLIGHT", "FAMILY_SHOWCASE_ACCEPTED", "ZIP_DELIVERED", "GIT_BINARY_PIN",
         "USER_UPLOAD_READBACK")
GATE_VALUES = {
    "ORIGINAL_SOURCE_VERIFIED": ("VERIFIED", "MAPPING_REQUIRED", "HASH_MISMATCH", "NOT_CHECKED"),
    "DIRECTION_APPROVED": ("APPROVED", "PENDING", "NOT_RECORDED"),
    "RAW_VISUAL_APPROVED": ("APPROVED", "PENDING"),
    "OUTPUT_LOCAL_QC": ("PASS", "FAIL", "NOT_RUN"),
    "CANONICAL_PREFLIGHT": ("PASS", "FAIL", "NOT_RUN", "NON_CANONICAL"),
    "FAMILY_SHOWCASE_ACCEPTED": ("ACCEPTED", "PENDING", "REJECTED", "INVALIDATED", "NOT_BUILT"),
    "ZIP_DELIVERED": ("BUILT_NOT_DELIVERED", "NOT_BUILT"),
    "GIT_BINARY_PIN": ("NOT_PERFORMED",),
    "USER_UPLOAD_READBACK": ("NOT_PERFORMED",),
}

# Target lock / attempt log vocabularies (ISOLATED_ART_GENERATION.md s2-s3).
LOCK_TEXT_FIELDS = ("action", "dominant_silhouette", "camera", "motion_axis", "secondary_effect")
REF_ROLES = ("identity-only", "style-only", "material-only", "subject")
REASON_CODES = ("wrong_target", "composition", "silhouette_conflict", "art_style_drift", "anatomy",
                "invented_symbol", "quality", "other")
RESTART_REASONS = {"wrong_target", "composition"}
OUTCOMES = ("rejected", "viable", "approved")


class StudioError(Exception):
    """A refusal. The message says exactly what failed; nothing downstream runs."""


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha256(Path(path).read_bytes())


def git_blob_sha(data: bytes) -> str:
    """The git blob id of these bytes, so a file can be compared with a pinned main blob."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def pixels_sha(img: Image.Image) -> str:
    """Encoder-independent identity of an image: size, mode and raw pixels."""
    return sha256(f"{img.width}x{img.height}:{img.mode}:".encode() + img.tobytes())


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def dump_json(obj) -> bytes:
    return (json.dumps(obj, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def atomic_write(path: Path, data: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", str(text))
    for a, b in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"')):
        text = text.replace(a, b)
    return " ".join(text.split()).casefold()


def name_key(text: str) -> str:
    """Exact comparison key: normalized, punctuation and separators dropped."""
    return re.sub(r"[^0-9a-z]+", "", normalize(text))


def file_tokens(member: str) -> list[str]:
    stem = PurePosixPath(member).stem
    tokens = [t.lower() for t in re.split(r"[^0-9A-Za-z]+", stem) if t]
    if tokens and re.fullmatch(r"v\d+", tokens[-1]):
        tokens = tokens[:-1]
    return tokens


def file_keys(members: list[str]) -> dict[str, set]:
    """Exact name keys each member file may carry: its stem minus a trailing vN, optionally minus
    a leading icon/jutsu token, optionally minus leading tokens EVERY image shares (the
    icon_<family>_ convention). A jutsu matches only when one variant equals its name exactly;
    two files matching one name stay ambiguous."""
    toks = {m: file_tokens(m) for m in members}
    shared = 0
    if len(toks) >= 2:
        lists = list(toks.values())
        while all(len(t) > shared + 1 for t in lists) and len({t[shared] for t in lists}) == 1:
            shared += 1
    out = {}
    for m, t in toks.items():
        variants = {name_key("".join(t[k:])) for k in range(0, shared + 1)}
        if len(t) > 1 and t[0] in ("icon", "jutsu"):
            variants.add(name_key("".join(t[1:])))
        out[m] = {v for v in variants if v}
    return out


def load_spec(path: Path) -> dict:
    try:
        spec = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise StudioError(f"art spec not found: {path}")
    target = (spec.get("targets") or {}).get(TARGET)
    if not isinstance(target, dict):
        raise StudioError(f"art spec {path} has no targets.{TARGET} block")
    return spec


def spec_numbers(spec: dict) -> dict:
    t = spec["targets"][TARGET]

    def val(v):
        return v.get("value") if isinstance(v, dict) else v

    rec = str(val(t.get("recommended_source_px")) or "256x256")
    w, h = (int(x) for x in rec.lower().split("x"))
    if w != h:
        raise StudioError(f"spec {TARGET}.recommended_source_px {rec} is not square")
    return {
        "size": w,
        "min_width": int(val(t.get("min_width_px")) or 0),
        "byte_ceiling": int(t.get("byte_ceiling_bytes")),
        "format": str(t.get("format")).upper(),
        "format_mode": t.get("format_mode"),
        "alpha": val(t.get("alpha")),
    }


def encoder_versions() -> dict:
    return {
        "tool": TOOL_VERSION,
        "pillow": PIL.__version__,
        "libwebp": features.version("webp") or "unknown",
        "python": "%d.%d" % sys.version_info[:2],
    }


def webp_codec(data: bytes) -> str | None:
    """'VP8L' / 'VP8 ' for a WebP file, by walking its RIFF chunks."""
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    pos = 12
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4]
        size = int.from_bytes(data[pos + 4:pos + 8], "little")
        if tag in (b"VP8L", b"VP8 "):
            return tag.decode("ascii")
        pos += 8 + size + (size & 1)
    return None


def decode(data: bytes) -> dict:
    """True-format decode. Raises StudioError for anything Pillow cannot fully load."""
    import warnings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", Image.DecompressionBombWarning)
            probe = Image.open(io.BytesIO(data))
        with probe:
            fmt, size, mode = probe.format, probe.size, probe.mode
            if size[0] * size[1] > MAX_IMAGE_PIXELS:
                raise StudioError(f"{size[0]}x{size[1]} exceeds the {MAX_IMAGE_PIXELS}-pixel bound")
            probe.load()
            has_alpha = "A" in probe.getbands() or "transparency" in probe.info
            orientation = None
            try:
                orientation = probe.getexif().get(0x0112)
            except Exception:
                orientation = None
    except StudioError:
        raise
    except Image.DecompressionBombError as exc:
        raise StudioError(f"refused as a decompression bomb: {exc}")
    except Exception as exc:
        raise StudioError(f"not a decodable image: {exc.__class__.__name__}: {exc}")
    return {"format": fmt, "width": size[0], "height": size[1], "mode": mode,
            "has_alpha": bool(has_alpha), "exif_orientation": orientation}


def load_font(size: int):
    try:
        return ImageFont.load_default(size=size), f"pillow-default-freetype-{size}"
    except (TypeError, OSError, AttributeError):
        return ImageFont.load_default(), "pillow-default-bitmap"


def text_width(draw, text: str, font) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


# ---------------------------------------------------------------------------------------------
# ZIP intake
# ---------------------------------------------------------------------------------------------


def scan_zip(data: bytes) -> tuple[list[dict], list[str], dict]:
    """Safety-check every entry and return (members, ignored, zip_info). Raise on any refusal."""
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise StudioError(f"not a readable ZIP archive: {exc}")
    infos = zf.infolist()
    if len(infos) > MAX_MEMBERS:
        raise StudioError(f"{len(infos)} entries exceeds the {MAX_MEMBERS}-entry bound")
    total = sum(i.file_size for i in infos)
    if total > MAX_TOTAL_BYTES:
        raise StudioError(f"declared expanded size {total} exceeds the {MAX_TOTAL_BYTES}-byte bound")

    problems: list[str] = []
    seen: dict[str, str] = {}
    keep: list[zipfile.ZipInfo] = []
    ignored: list[str] = []
    for info in infos:
        name = info.filename
        if "\\" in name:
            problems.append(f"{name!r}: backslash in an entry name")
            continue
        if name.startswith("/") or re.match(r"^[A-Za-z]:", name):
            problems.append(f"{name!r}: absolute path")
            continue
        parts = PurePosixPath(name).parts
        if ".." in parts:
            problems.append(f"{name!r}: path traversal")
            continue
        mode = info.external_attr >> 16
        if stat.S_ISLNK(mode):
            problems.append(f"{name!r}: symbolic link")
            continue
        if info.flag_bits & 0x1:
            problems.append(f"{name!r}: encrypted entry")
            continue
        folded = name.casefold()
        if folded in seen:
            kind = "duplicate entry" if seen[folded] == name else f"case-collides with {seen[folded]!r}"
            problems.append(f"{name!r}: {kind}")
            continue
        seen[folded] = name
        if info.is_dir():
            continue
        if info.file_size > MAX_MEMBER_BYTES:
            problems.append(f"{name!r}: {info.file_size} bytes exceeds the per-member bound")
            continue
        if info.compress_size and info.file_size / info.compress_size > MAX_RATIO:
            problems.append(f"{name!r}: compression ratio above {MAX_RATIO}:1 (possible ZIP bomb)")
            continue
        if name.startswith(IGNORED_PREFIXES) or PurePosixPath(name).name in IGNORED_NAMES:
            ignored.append(name)
            continue
        keep.append(info)
    if problems:
        raise StudioError("ZIP refused:\n  - " + "\n  - ".join(problems))

    members = []
    read_total = 0
    for info in keep:
        try:
            with zf.open(info) as handle:
                blob = handle.read(MAX_MEMBER_BYTES + 1)
        except zipfile.BadZipFile as exc:  # CRC failure surfaces here
            raise StudioError(f"ZIP refused: {info.filename!r}: {exc}")
        if len(blob) != info.file_size:
            raise StudioError(f"ZIP refused: {info.filename!r}: size {len(blob)} disagrees with header {info.file_size}")
        read_total += len(blob)
        if read_total > MAX_TOTAL_BYTES:
            raise StudioError("ZIP refused: expanded bytes exceed the bound")
        members.append({"path": info.filename, "data": blob})
    return members, ignored, {"entries": len(infos), "expanded_bytes": read_total}


def find_manifest(members: list[dict]) -> dict | None:
    hits = [m for m in members if PurePosixPath(m["path"]).name.lower() == "manifest.json"]
    if not hits:
        return None
    if len(hits) > 1:
        raise StudioError("ZIP carries more than one manifest.json: " + ", ".join(m["path"] for m in hits))
    return hits[0]


def load_roster(path: Path) -> dict:
    """Director roster: JSON {bloodline, jutsu:[{jutsu_id,name,file?}]} or CSV jutsu_id,name[,file]."""
    text = Path(path).read_text(encoding="utf-8-sig")
    if str(path).lower().endswith(".csv"):
        rows = list(csv.DictReader(io.StringIO(text)))
        if not rows or not {"jutsu_id", "name"} <= set(rows[0]):
            raise StudioError(f"roster CSV {path} needs jutsu_id,name columns")
        return {"bloodline": {}, "jutsu": [{k: (v or "").strip() for k, v in r.items()} for r in rows]}
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise StudioError(f"roster {path} is not valid JSON: {exc}")
    if isinstance(data, list):
        data = {"jutsu": data}
    return data


def check_roster(doc: dict, label: str) -> tuple[dict, list[dict]]:
    if not isinstance(doc, dict) or not isinstance(doc.get("jutsu"), list) or not doc["jutsu"]:
        raise StudioError(f"{label}: needs a non-empty 'jutsu' array")
    ids, names, rows = set(), set(), []
    for pos, row in enumerate(doc["jutsu"]):
        if not isinstance(row, dict):
            raise StudioError(f"{label}: jutsu[{pos}] is not an object")
        jid, name = row.get("jutsu_id"), row.get("name")
        if not isinstance(jid, str) or not jid.strip() or not isinstance(name, str) or not name.strip():
            raise StudioError(f"{label}: jutsu[{pos}] needs non-empty string jutsu_id and name")
        if jid in ids:
            raise StudioError(f"{label}: duplicate jutsu_id {jid}")
        if name_key(name) in names:
            raise StudioError(f"{label}: duplicate jutsu name {name!r}")
        sha = row.get("sha256")
        if sha not in (None, "") and not (isinstance(sha, str) and SHA_RE.match(sha)):
            raise StudioError(f"{label}: jutsu[{pos}] sha256 is not a 64-hex digest")
        ids.add(jid)
        names.add(name_key(name))
        rows.append(row)
    bloodline = doc.get("bloodline") if isinstance(doc.get("bloodline"), dict) else {}
    return bloodline, rows


def style_exemplars(git_ref: str | None) -> dict:
    """The pinned JUTSU_ICON exemplars, via style_refs.py beside this script."""
    try:
        sys.path.insert(0, str(SCRIPT_DIR))
        import style_refs  # type: ignore
    except Exception as exc:  # pragma: no cover - packaged together
        return {"status": "STYLE_REFERENCE_PIXELS_PENDING", "reason": f"style_refs.py unavailable: {exc}"}
    finally:
        if sys.path and sys.path[0] == str(SCRIPT_DIR):
            sys.path.pop(0)
    index_path = SCRIPT_DIR.parent / "data" / "style_refs.json"
    if not index_path.is_file():
        return {"status": "STYLE_REFERENCE_PIXELS_PENDING", "reason": "data/style_refs.json not found"}
    index = json.loads(index_path.read_text(encoding="utf-8"))
    every = style_refs.filter_refs(index, target=TARGET)
    if not every:
        return {"status": "STYLE_REFERENCE_PIXELS_PENDING", "reason": "no JUTSU_ICON exemplars are indexed"}
    pick = style_refs.select(index, TARGET)
    row = lambda r: {"key": r["key"], "name": r["name"], "family": r.get("family"), "priority": r["priority"],
                     "sha256": r["sha256"], "path": r["path"], "raw_url": style_refs.raw_url(index, r, git_ref),
                     "silhouette": r.get("silhouette"), "use_for": r["use_for"],
                     "provenance": style_refs.provenance_status(r)}
    return {
        "status": "PINNED",
        "git_ref_for_urls": git_ref or index.get("raw_url_default_ref", "main"),
        "default_selection": [row(r) for r in pick],
        "primary": [row(r) for r in every if r.get("priority") == "PRIMARY"],
        "reserved_silhouettes": [{"family": r.get("family"), "name": r["name"], "silhouette": r.get("silhouette")}
                                 for r in every],
        "rule": "STYLE/MATERIAL ONLY. Attach the actual bytes (not a URL) with at most one legacy identity icon.",
    }


def intake(zip_path: Path, out: Path, roster_path: Path | None = None, git_ref: str | None = None,
           timings: dict | None = None) -> int:
    timings = {} if timings is None else timings
    t0 = time.perf_counter()
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise StudioError(f"--out {out} is not empty; intake never mixes runs")
    data = Path(zip_path).read_bytes()
    members, ignored, zinfo = scan_zip(data)
    timings["intake_ms"] = round((time.perf_counter() - t0) * 1000, 1)

    t1 = time.perf_counter()
    issues: list[dict] = []

    def issue(level, code, message):
        issues.append({"level": level, "code": code, "message": message})

    for name in ignored:
        issue("note", "IGNORED_JUNK", f"{name} ignored (archive metadata)")

    manifest_member = find_manifest(members)
    manifest = None
    manifest_dir = ""
    if manifest_member is not None:
        try:
            manifest = json.loads(manifest_member["data"].decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise StudioError(f"{manifest_member['path']} is not valid JSON: {exc}")
        parent = str(PurePosixPath(manifest_member["path"]).parent)
        manifest_dir = "" if parent == "." else parent + "/"

    by_path = {m["path"]: m for m in members}
    index_rows = []
    for m in members:
        row = {"path": m["path"], "bytes": len(m["data"]), "sha256": sha256(m["data"]), "role": None}
        if manifest_member is not None and m["path"] == manifest_member["path"]:
            row.update(role="manifest", decoded_format="JSON")
        else:
            try:
                info = decode(m["data"])
                row.update(decoded_format=info["format"], width=info["width"], height=info["height"],
                           mode=info["mode"], has_alpha=info["has_alpha"])
                claimed = SUFFIX_FORMAT.get(PurePosixPath(m["path"]).suffix.lower())
                row["suffix_matches"] = claimed == info["format"]
                if claimed and not row["suffix_matches"]:
                    issue("note", "SUFFIX_MISMATCH", f"{m['path']} is named {claimed} but decodes as {info['format']} (kept; bytes unchanged)")
                row["role"] = "image"
            except StudioError as exc:
                if PurePosixPath(m["path"]).suffix.lower() in SUFFIX_FORMAT:
                    issue("error", "UNDECODABLE_IMAGE", f"{m['path']}: {exc}")
                    row["role"] = "undecodable"
                else:
                    row["role"] = "non_image"
                    row["decoded_format"] = "non-image"
        index_rows.append(row)
    rows_by_path = {r["path"]: r for r in index_rows}
    timings["hash_decode_ms"] = round((time.perf_counter() - t1) * 1000, 1)

    # ---- roster and mapping
    bloodline: dict = {}
    roster_rows: list[dict] = []
    roster_source = "none"
    manifest_files: dict[str, dict] = {}
    if manifest is not None:
        m_bloodline, m_rows = check_roster(manifest, manifest_member["path"])
        bloodline = dict(m_bloodline)
        roster_rows = m_rows
        roster_source = "zip_manifest"
        for r in m_rows:
            manifest_files[r["jutsu_id"]] = r
            r["_evidence_default"] = "historical_capture"
    if roster_path is not None:
        r_bloodline, r_rows = check_roster(load_roster(roster_path), str(roster_path))
        if roster_rows:
            m_by_id = {r["jutsu_id"]: r for r in roster_rows}
            r_by_id = {r["jutsu_id"]: r for r in r_rows}
            for jid in sorted(set(m_by_id) | set(r_by_id)):
                if jid not in m_by_id:
                    issue("error", "ROSTER_CONFLICT", f"roster jutsu {jid} ({r_by_id[jid]['name']}) is absent from the ZIP manifest")
                elif jid not in r_by_id:
                    issue("error", "ROSTER_CONFLICT", f"ZIP manifest jutsu {jid} ({m_by_id[jid]['name']}) is absent from the roster")
                elif name_key(m_by_id[jid]["name"]) != name_key(r_by_id[jid]["name"]):
                    issue("error", "ROSTER_CONFLICT", f"{jid}: manifest name {m_by_id[jid]['name']!r} != roster name {r_by_id[jid]['name']!r}")
        for k, v in r_bloodline.items():
            if bloodline.get(k) not in (None, "", v):
                issue("error", "ROSTER_CONFLICT", f"bloodline.{k}: manifest {bloodline.get(k)!r} != roster {v!r}")
            bloodline.setdefault(k, v)
        for r in r_rows:
            r["_evidence_default"] = "director_roster"
        roster_rows = r_rows
        roster_source = "director_roster" if roster_source == "none" else "director_roster+zip_manifest"
        for r in r_rows:
            if r.get("file"):
                manifest_files.setdefault(r["jutsu_id"], r)

    images = [r for r in index_rows if r["role"] == "image"]
    claimed: dict[str, str] = {}
    jutsu_rows = []
    by_key: dict[str, list[str]] = {}
    for path, keys in file_keys([r["path"] for r in images]).items():
        for key in keys:
            by_key.setdefault(key, []).append(path)
    for jr in roster_rows:
        jid, name = jr["jutsu_id"], jr["name"]
        evidence = jr.get("evidence_level") or jr.get("_evidence_default", "historical_capture")
        if evidence not in EVIDENCE_LEVELS:
            issue("error", "BAD_EVIDENCE_LEVEL", f"{jid} ({name}): evidence_level {evidence!r} is not one of "
                                                  f"{', '.join(EVIDENCE_LEVELS)}; tooling never records a current-live roster")
            evidence = "historical_capture"
        out_row = {"jutsu_id": jid, "name": name, "type": jr.get("type"), "evidence_level": evidence,
                   "member": None, "sha256": None, "mapping": "MAPPING_REQUIRED", "candidates": [], "issues": []}
        src = manifest_files.get(jid)
        if src and src.get("file"):
            rel = str(src["file"])
            if rel.startswith("/") or ".." in PurePosixPath(rel).parts or "\\" in rel:
                out_row["issues"].append(f"unsafe file path {rel!r}")
            else:
                member_path = manifest_dir + rel if (manifest_dir + rel) in by_path else rel
                mrow = rows_by_path.get(member_path)
                if mrow is None:
                    out_row["issues"].append(f"mapped file {rel!r} is not in the ZIP")
                    issue("error", "MISSING_MAPPED_FILE", f"{jid} ({name}): mapped file {rel!r} is not in the ZIP")
                elif mrow["role"] != "image":
                    out_row["issues"].append(f"mapped file {member_path!r} is not a decodable image")
                    issue("error", "MAPPED_FILE_NOT_IMAGE", f"{jid} ({name}): {member_path} is not a decodable image")
                elif src.get("sha256") and src["sha256"] != mrow["sha256"]:
                    out_row.update(member=member_path, sha256=mrow["sha256"], mapping="HASH_MISMATCH")
                    issue("error", "HASH_MISMATCH", f"{jid} ({name}): {member_path} sha256 {mrow['sha256']} != manifest {src['sha256']}")
                else:
                    out_row.update(member=member_path, sha256=mrow["sha256"],
                                   mapping="MANIFEST_VERIFIED" if src.get("sha256") else "MANIFEST_MAPPED")
        else:
            hits = by_key.get(name_key(name), [])
            if len(hits) == 1:
                mrow = rows_by_path[hits[0]]
                out_row.update(member=hits[0], sha256=mrow["sha256"], mapping="NAME_MATCH")
            elif len(hits) > 1:
                out_row["candidates"] = sorted(hits)
                issue("warn", "MAPPING_REQUIRED", f"{jid} ({name}): {len(hits)} files match the name exactly: {', '.join(sorted(hits))}")
            else:
                issue("warn", "MAPPING_REQUIRED", f"{jid} ({name}): no file is mapped to this jutsu")
        if out_row["member"]:
            if out_row["member"] in claimed:
                issue("error", "DOUBLE_CLAIM", f"{out_row['member']} is claimed by {claimed[out_row['member']]} and {jid}")
            claimed[out_row["member"]] = jid
            rows_by_path[out_row["member"]]["role"] = "jutsu"
            rows_by_path[out_row["member"]]["jutsu_id"] = jid
        jutsu_rows.append(out_row)

    identity = None
    ident_src = (manifest or {}).get("identity") if isinstance(manifest, dict) else None
    if isinstance(ident_src, dict) and ident_src.get("file"):
        rel = manifest_dir + str(ident_src["file"])
        if rel in rows_by_path and rows_by_path[rel]["role"] == "image":
            rows_by_path[rel]["role"] = "identity"
            identity = rel
            if ident_src.get("sha256") and ident_src["sha256"] != rows_by_path[rel]["sha256"]:
                issue("error", "HASH_MISMATCH", f"identity art {rel} sha256 disagrees with the manifest")
        else:
            issue("error", "MISSING_MAPPED_FILE", f"identity art {ident_src['file']!r} is not a decodable image in the ZIP")
    for r in index_rows:
        if r["role"] == "image":
            r["role"] = "unmapped"
            issue("warn", "UNMAPPED_ASSET", f"{r['path']} is not mapped to any jutsu (identity art? superseded? say which)")

    if not roster_rows:
        issue("warn", "ROSTER_REQUIRED", "no manifest.json and no --roster: N and every jutsu ID are unknown. "
                                          "Supply the exact roster (jutsu_id,name[,file]); never infer N from rank or file count.")

    # ---- write outputs (atomically, into a fresh directory)
    out.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".intake-", dir=str(out.parent)))
    try:
        for r in index_rows:
            if r["role"] in ("jutsu", "identity", "unmapped", "undecodable"):
                base = re.sub(r"[^A-Za-z0-9._-]+", "_", PurePosixPath(r["path"]).name)
                r["extracted_as"] = f"originals/{r['sha256'][:12]}_{base}"
                atomic_write(stage / r["extracted_as"], by_path[r["path"]]["data"])
        n_verified = bool(roster_rows) and all(j["mapping"] in ("MANIFEST_VERIFIED", "MANIFEST_MAPPED", "NAME_MATCH") for j in jutsu_rows)
        exemplars = style_exemplars(git_ref)
        source_index = {
            "schema": "tnr.jutsu-studio.source-index/1",
            "tool": encoder_versions(),
            "zip": {"filename": Path(zip_path).name, "bytes": len(data), "sha256": sha256(data), "crc_ok": True, **zinfo},
            "bloodline": {k: bloodline.get(k) for k in ("id", "name", "rank")} | {"source": roster_source},
            "roster_source": roster_source,
            "evidence_levels": sorted({j["evidence_level"] for j in jutsu_rows}),
            "evidence_note": "historical_capture and director_roster are not current-live checks",
            "n": len(roster_rows) if roster_rows else None,
            "n_status": "FROM_ROSTER" if roster_rows else "UNKNOWN_NO_ROSTER",
            "mapping_complete": n_verified,
            "identity_art": identity,
            "members": sorted(index_rows, key=lambda r: r["path"]),
            "jutsu": jutsu_rows,
            "ignored": ignored,
            "issues": issues,
            "style_exemplars": exemplars,
            "live_game_requests": 0,
            "live_game_writes": 0,
        }
        atomic_write(stage / "source_index.json", dump_json(source_index))
        atomic_write(stage / "studio_ledger.json", dump_json(initial_ledger(source_index)))
        atomic_write(stage / "approved_template.json", dump_json(approved_template(source_index)))
        atomic_write(stage / "intake_report.md", render_intake_report(source_index).encode("utf-8"))
        orient = orientation_index(index_rows, by_path)
        if orient is not None:
            atomic_write(stage / "orientation_index.png", orient)
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            out.rmdir()  # verified empty above
        os.replace(stage, out)
    except BaseException:
        import shutil
        shutil.rmtree(stage, ignore_errors=True)
        raise
    timings["total_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    print(render_intake_report(source_index))
    print(f"\nwritten: {out}/  (timings ms: {timings})")
    if any(i["level"] == "error" for i in issues):
        return 1
    return 0 if n_verified else 3


def initial_ledger(src: dict) -> dict:
    rows = []
    for j in src["jutsu"]:
        mapping = j["mapping"]
        rows.append({
            "jutsu_id": j["jutsu_id"], "name": j["name"], "legacy_member": j["member"], "legacy_sha256": j["sha256"],
            "silhouette": None, "silhouette_status": "PROPOSED_BY_STUDIO_PENDING_DIRECTOR",
            "evidence_level": j["evidence_level"],
            "mapping": mapping,
            "gates": check_gates({
                "ORIGINAL_SOURCE_VERIFIED": ("VERIFIED" if mapping in ("MANIFEST_VERIFIED", "MANIFEST_MAPPED") else
                                             "HASH_MISMATCH" if mapping == "HASH_MISMATCH" else "MAPPING_REQUIRED"),
                "DIRECTION_APPROVED": "PENDING", "RAW_VISUAL_APPROVED": "PENDING",
                "OUTPUT_LOCAL_QC": "NOT_RUN", "CANONICAL_PREFLIGHT": "NOT_RUN",
                "FAMILY_SHOWCASE_ACCEPTED": "NOT_BUILT", "ZIP_DELIVERED": "NOT_BUILT",
                "GIT_BINARY_PIN": "NOT_PERFORMED", "USER_UPLOAD_READBACK": "NOT_PERFORMED",
            }, label=j["jutsu_id"]),
        })
    return {"schema": "tnr.jutsu-studio.ledger/1", "bloodline": src["bloodline"], "n": src["n"],
            "zip_sha256": src["zip"]["sha256"], "rows": rows,
            "note": "Gates are separate and never inferred from each other. A chat approval is recorded only when the Studio writes it into approved.json. "
                    "NAME_MATCH mappings stay MAPPING_REQUIRED until the director confirms them."}


def slugify(name: str) -> str:
    s = re.sub(r"[^0-9a-z]+", "_", normalize(name).replace("'", "")).strip("_")
    return s or "jutsu"


def family_code(name: str | None) -> str:
    """Default file-name family code: word initials ('Blood-Enchanted Eyes' -> 'bee')."""
    words = [w for w in re.split(r"[^0-9a-z]+", normalize(name or "").replace("'", "")) if w]
    if len(words) >= 2:
        return "".join(w[0] for w in words)
    return (words[0][:12] if words else "family")


def approved_template(src: dict) -> dict:
    return {
        "schema": "tnr.jutsu-studio.approved/1",
        "bloodline": {"id": src["bloodline"].get("id"), "name": src["bloodline"].get("name"),
                      "family": family_code(src["bloodline"].get("name"))},
        "family_byte_cap_exclusive": None,
        "family_byte_cap_ruling": None,
        "family_acceptance": {"status": "PENDING", "evidence": "", "gallery_sha256": None,
                              "gallery_pixels_sha256": None, "members_sha256": None},
        "jutsu": [{"jutsu_id": j["jutsu_id"], "name": j["name"], "slug": slugify(j["name"]), "version": 1,
                   "raw_file": None, "raw_sha256": None,
                   "director_raw_approval": {"status": "PENDING", "evidence": ""},
                   "quantize": None, "superseded_raw_sha256": []} for j in src["jutsu"]],
        "_how_to": "Fill raw_file (path relative to this file) + raw_sha256 for each director-approved raw, set status "
                   "APPROVED with the approval evidence, then run: jutsu_studio.py finalize approved.json --out DIR. "
                   "family_byte_cap_exclusive stays null unless the director approved a stricter cap (cite the ruling). "
                   "quantize stays null unless the director approved that icon's visible palette loss. "
                   "family_acceptance ACCEPTED copies gallery.sha256, gallery.pixels_sha256 and members_sha256 from the "
                   "exact showcase_manifest.json the director accepted.",
    }


def render_intake_report(src: dict) -> str:
    bl = src["bloodline"]
    lines = [f"# Jutsu Art Studio intake - {bl.get('name') or 'UNKNOWN BLOODLINE'}", ""]
    lines.append(f"- Bloodline ID: `{bl.get('id') or 'not supplied'}`; rank: {bl.get('rank') or 'not supplied'}; roster source: {src['roster_source']}")
    lines.append(f"- N: **{src['n'] if src['n'] is not None else 'UNKNOWN'}** ({src['n_status']}); mapping complete: **{'yes' if src['mapping_complete'] else 'NO'}**")
    lines.append(f"- ZIP: `{src['zip']['filename']}` {src['zip']['bytes']} B sha256 `{src['zip']['sha256']}`; {src['zip']['entries']} entries; CRC OK")
    lines.append("")
    lines.append(f"- Roster evidence: {', '.join(src.get('evidence_levels') or ['none'])} (not a current-live check)")
    lines.append("")
    lines.append("| # | Jutsu | ID | ZIP member | Decoded | Mapping |")
    lines.append("|---|---|---|---|---|---|")
    rows_by_path = {m["path"]: m for m in src["members"]}
    for i, j in enumerate(src["jutsu"], 1):
        m = rows_by_path.get(j["member"] or "", {})
        dec = f"{m.get('decoded_format')} {m.get('width')}x{m.get('height')}" if m else "-"
        cand = f" candidates: {', '.join(j['candidates'])}" if j["candidates"] else ""
        lines.append(f"| {i} | {j['name']} | `{j['jutsu_id']}` | {j['member'] or '-'} | {dec} | {j['mapping']}{cand} |")
    if not src["jutsu"]:
        lines.append("| - | (no roster) | - | - | - | ROSTER_REQUIRED |")
    other = [m for m in src["members"] if m["role"] in ("unmapped", "identity", "undecodable")]
    if other:
        lines += ["", "Other images:"]
        for m in other:
            lines.append(f"- {m['path']} - {m['role']} ({m.get('decoded_format')} {m.get('width')}x{m.get('height')})")
    probs = [i for i in src["issues"] if i["level"] != "note"]
    if probs:
        lines += ["", "Issues:"]
        for i in probs:
            lines.append(f"- **{i['level'].upper()} {i['code']}** - {i['message']}")
    ex = src["style_exemplars"]
    lines += ["", "Style exemplars (STYLE/MATERIAL ONLY):"]
    if ex.get("status") == "PINNED":
        for r in ex["primary"]:
            flag = f" [{r['provenance']}]" if r.get("provenance") else ""
            lines.append(f"- {r['name']} ({r['family']}){flag} - reserved shape: {r['silhouette']} - {r['raw_url']}")
        taken = "; ".join(f"{r['silhouette']} ({r['family']})" for r in ex["reserved_silhouettes"])
        lines.append(f"- Shapes already owned by other families: {taken}")
    else:
        lines.append(f"- STYLE_REFERENCE_PIXELS_PENDING: {ex.get('reason')}")
    lines += ["", "Next: inspect 2-4 originals (originals/), write the family treatment card and the N-row silhouette "
                  "ledger, then the first isolated-generation brief. orientation_index.png is for the Studio only - "
                  "never attach it to a generator."]
    return "\n".join(lines) + "\n"


def orientation_index(rows: list[dict], by_path: dict) -> bytes | None:
    imgs = [r for r in rows if r["role"] in ("jutsu", "identity", "unmapped")]
    if not imgs:
        return None
    cell, label_h, cols = 160, 34, min(4, len(imgs))
    nrows = (len(imgs) + cols - 1) // cols
    head = 30
    canvas = Image.new("RGB", (cols * (cell + 12) + 12, head + nrows * (cell + label_h + 12) + 12), BG)
    draw = ImageDraw.Draw(canvas)
    font, _ = load_font(13)
    draw.text((12, 8), "STUDIO ORIENTATION ONLY - NEVER A GENERATOR REFERENCE", fill=TEXT, font=font)
    for i, r in enumerate(sorted(imgs, key=lambda r: r["path"])):
        x = 12 + (i % cols) * (cell + 12)
        y = head + (i // cols) * (cell + label_h + 12)
        with Image.open(io.BytesIO(by_path[r["path"]]["data"])) as im:
            thumb = im.convert("RGB")
            thumb.thumbnail((cell, cell), Image.LANCZOS)
        canvas.paste(thumb, (x + (cell - thumb.width) // 2, y + (cell - thumb.height) // 2))
        label = (r.get("jutsu_id") and f"{r['role']}:{r['jutsu_id'][:10]}") or r["role"]
        draw.text((x, y + cell + 2), PurePosixPath(r["path"]).name[:24], fill=TEXT, font=font)
        draw.text((x, y + cell + 17), label, fill=TEXT_DIM, font=font)
    buf = io.BytesIO()
    canvas.save(buf, "PNG", optimize=False)
    return buf.getvalue()


# ---------------------------------------------------------------------------------------------
# gate table (state table K)
# ---------------------------------------------------------------------------------------------


def check_gates(gates: dict, label: str = "icon") -> dict:
    """Refuse an unknown gate, an unknown value or an inconsistent combination. Returns gates."""
    errs = []
    if set(gates) != set(GATES):
        errs.append(f"gates must be exactly {', '.join(GATES)} (missing {sorted(set(GATES) - set(gates))}, "
                    f"unknown {sorted(set(gates) - set(GATES))})")
    for k, v in gates.items():
        if k in GATE_VALUES and v not in GATE_VALUES[k]:
            errs.append(f"{k}={v!r} is not one of {', '.join(GATE_VALUES[k])}")
    g = gates.get
    if g("CANONICAL_PREFLIGHT") in ("PASS", "FAIL", "NON_CANONICAL") and g("OUTPUT_LOCAL_QC") != "PASS":
        errs.append("CANONICAL_PREFLIGHT was run but OUTPUT_LOCAL_QC is not PASS")
    if g("OUTPUT_LOCAL_QC") in ("PASS", "FAIL") and g("RAW_VISUAL_APPROVED") != "APPROVED":
        errs.append("an export exists for a raw that is not RAW_VISUAL_APPROVED")
    if g("ZIP_DELIVERED") == "BUILT_NOT_DELIVERED" and g("OUTPUT_LOCAL_QC") != "PASS":
        errs.append("ZIP_DELIVERED is set but OUTPUT_LOCAL_QC is not PASS")
    if g("FAMILY_SHOWCASE_ACCEPTED") not in ("NOT_BUILT",) and g("OUTPUT_LOCAL_QC") != "PASS":
        errs.append("a family showcase state exists without OUTPUT_LOCAL_QC PASS")
    if errs:
        raise StudioError(f"gate table for {label} is inconsistent:\n  - " + "\n  - ".join(errs))
    return dict(gates)


def collection_gates(rows: list[dict]) -> dict:
    """The collection is only as far along as its least-advanced icon, per gate."""
    out = {}
    for k in GATES:
        vals = [r["gates"][k] for r in rows]
        order = GATE_VALUES[k]
        out[k] = vals[0] if len(set(vals)) == 1 else "MIXED: " + ", ".join(f"{v}={vals.count(v)}" for v in order if v in vals)
    return out


# ---------------------------------------------------------------------------------------------
# target locks (P0 A/B)
# ---------------------------------------------------------------------------------------------


def lock_sha(target: dict) -> str:
    """SHA-256 of a target lock without its approval block: what the director approved."""
    return sha256(canon({k: v for k, v in target.items() if k != "direction_approval"}).encode())


def load_json(path: Path, what: str, data: bytes | None = None) -> dict:
    try:
        if data is None:
            data = Path(path).read_bytes()
        return json.loads(data.decode("utf-8"))
    except FileNotFoundError:
        raise StudioError(f"{what} not found: {path}")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StudioError(f"{what} is not valid JSON: {exc}")


def check_locks(path: Path, source_index: Path | None = None, data: bytes | None = None) -> dict:
    """Return {"doc", "by_id", "incomplete": {id: [problems]}, "approved": set}. Raise on refusals.

    Refusals are records that contradict themselves or the roster; incompleteness (a missing
    field) is reported as LOCK_INCOMPLETE so a studio can fill a lock in stages."""
    doc = load_json(path, "target locks", data)
    errs: list[str] = []
    if doc.get("schema") != "tnr.jutsu-studio.locks/1":
        errs.append("schema must be 'tnr.jutsu-studio.locks/1'")
    targets = doc.get("targets")
    if not isinstance(targets, list) or not targets:
        raise StudioError("target locks problems:\n  - " + "\n  - ".join(errs + ["targets must be a non-empty array"]))
    by_id: dict[str, dict] = {}
    for pos, tg in enumerate(targets):
        if not isinstance(tg, dict) or not isinstance(tg.get("jutsu_id"), str) or not tg["jutsu_id"].strip():
            errs.append(f"targets[{pos}] needs a jutsu_id")
            continue
        if tg["jutsu_id"] in by_id:
            errs.append(f"duplicate target {tg['jutsu_id']}")
            continue
        by_id[tg["jutsu_id"]] = tg
    incomplete: dict[str, list[str]] = {}
    approved = set()
    for jid, tg in by_id.items():
        label = f"{jid} ({tg.get('name')!r})"
        miss = []
        if not isinstance(tg.get("name"), str) or not tg["name"].strip():
            miss.append("name")
        if not isinstance(tg.get("version"), int) or isinstance(tg.get("version"), bool) or tg["version"] < 1:
            miss.append("version (integer >= 1)")
        if tg.get("evidence_level") not in EVIDENCE_LEVELS:
            miss.append(f"evidence_level ({'/'.join(EVIDENCE_LEVELS)})")
        for f in LOCK_TEXT_FIELDS:
            if not isinstance(tg.get(f), str) or not tg[f].strip():
                miss.append(f)
        excl = tg.get("sibling_exclusions")
        covered = set()
        if not isinstance(excl, list):
            miss.append("sibling_exclusions")
        else:
            for e in excl:
                if not isinstance(e, dict) or not str(e.get("silhouette") or "").strip() or not e.get("jutsu_id"):
                    miss.append("sibling_exclusions entries need jutsu_id + silhouette")
                    break
                if e["jutsu_id"] == jid:
                    errs.append(f"{label}: excludes its own silhouette")
                covered.add(e["jutsu_id"])
            for other in sorted(set(by_id) - {jid} - covered):
                miss.append(f"sibling_exclusions for {other} ({by_id[other].get('name')!r})")
        refs = tg.get("references")
        if not isinstance(refs, list) or not refs:
            miss.append("references (1-2 individual images with roles)")
        else:
            if len(refs) > 2:
                errs.append(f"{label}: {len(refs)} references; a generation takes at most two individual images")
            for r in refs:
                if not isinstance(r, dict) or not SHA_RE.match(str(r.get("sha256") or "")):
                    errs.append(f"{label}: each reference needs the 64-hex sha256 of the actual attached bytes")
                    continue
                if r.get("role") not in REF_ROLES:
                    errs.append(f"{label}: reference role {r.get('role')!r} is not one of {', '.join(REF_ROLES)}")
                if r.get("kind") != "individual":
                    errs.append(f"{label}: reference {r['sha256'][:12]} must be kind 'individual'; never a sheet or collage")
        anat = tg.get("anatomy_exception")
        if anat is not None and (not isinstance(anat, dict) or not str(anat.get("scope") or "").strip()
                                 or not str(anat.get("director_evidence") or "").strip()):
            errs.append(f"{label}: anatomy_exception must be null or {{scope, director_evidence}} for this exact target")
        appr = tg.get("direction_approval") if isinstance(tg.get("direction_approval"), dict) else {}
        status = appr.get("status", "PENDING")
        if status not in ("PENDING", "APPROVED"):
            errs.append(f"{label}: direction_approval.status must be PENDING or APPROVED")
        if status == "APPROVED":
            if miss:
                errs.append(f"{label}: direction APPROVED on an incomplete lock (missing {', '.join(miss)})")
            if not str(appr.get("evidence") or "").strip():
                errs.append(f"{label}: direction APPROVED needs evidence")
            if appr.get("lock_sha256") != lock_sha(tg):
                errs.append(f"{label}: lock changed after DIRECTION_APPROVED (approved {str(appr.get('lock_sha256'))[:12]}, "
                            f"now {lock_sha(tg)[:12]}); bump version and record a fresh approval")
            else:
                approved.add(jid)
        if miss:
            incomplete[jid] = miss
    if doc.get("bloodline", {}).get("id") in (None, ""):
        errs.append("bloodline.id is required (exact bloodline identity)")
    if source_index is not None:
        src = load_json(source_index, "source index")
        roster = {j["jutsu_id"]: j for j in src.get("jutsu", [])}
        if src.get("bloodline", {}).get("id") not in (None, doc.get("bloodline", {}).get("id")):
            errs.append(f"bloodline.id {doc.get('bloodline', {}).get('id')!r} != intake {src['bloodline']['id']!r}")
        for jid, tg in by_id.items():
            if jid not in roster:
                errs.append(f"{jid}: not in the intake roster")
            elif name_key(roster[jid]["name"]) != name_key(str(tg.get("name") or "")):
                errs.append(f"{jid}: lock name {tg.get('name')!r} != roster name {roster[jid]['name']!r}")
            elif tg.get("evidence_level") in EVIDENCE_LEVELS and roster[jid].get("evidence_level") and \
                    tg["evidence_level"] != roster[jid]["evidence_level"]:
                errs.append(f"{jid}: lock evidence_level {tg['evidence_level']} != intake {roster[jid]['evidence_level']}")
        for jid in sorted(set(roster) - set(by_id)):
            incomplete.setdefault(jid, []).append("no lock for this roster jutsu")
    if errs:
        raise StudioError("target locks problems:\n  - " + "\n  - ".join(errs))
    return {"doc": doc, "by_id": by_id, "incomplete": incomplete, "approved": approved}


# ---------------------------------------------------------------------------------------------
# attempt log (P0 B, retrospective J)
# ---------------------------------------------------------------------------------------------


def check_attempts(path: Path, locks: dict | None = None, data: bytes | None = None) -> dict:
    """Validate the studio's attempt log; return per-jutsu and family statistics. Raise on refusals."""
    doc = load_json(path, "attempt log", data)
    errs: list[str] = []
    if doc.get("schema") != "tnr.jutsu-studio.attempts/1":
        errs.append("schema must be 'tnr.jutsu-studio.attempts/1'")
    rows = doc.get("attempts")
    if not isinstance(rows, list):
        raise StudioError("attempt log problems:\n  - " + "\n  - ".join(errs + ["attempts must be an array"]))
    per: dict[str, list[dict]] = {}
    rejected_shas: set = set()
    session_owner: dict[str, str] = {}
    for pos, a in enumerate(rows):
        if not isinstance(a, dict) or not isinstance(a.get("jutsu_id"), str):
            errs.append(f"attempts[{pos}] needs a jutsu_id")
            continue
        per.setdefault(a["jutsu_id"], []).append(a)
        sid = a.get("session_id")
        if isinstance(sid, str) and sid.strip():  # one jutsu per isolated conversation (P0 s1)
            owner = session_owner.setdefault(sid, a["jutsu_id"])
            if owner != a["jutsu_id"]:
                errs.append(f"session {sid!r} is used for {owner} and {a['jutsu_id']}; each isolated generation "
                            f"conversation serves exactly one jutsu")
        if a.get("outcome") == "rejected" and SHA_RE.match(str(a.get("candidate_sha256") or "")):
            rejected_shas.add(a["candidate_sha256"])
    lock_ids = locks["by_id"] if locks else None
    stats: dict[str, dict] = {}
    for jid, seq in per.items():
        label = jid
        if lock_ids is not None and jid not in lock_ids:
            errs.append(f"{label}: no target lock for this jutsu")
        counts = {f"{c}_count": 0 for c in ("wrong_target", "composition", "silhouette_conflict", "art_style_drift",
                                            "anatomy_rejection", "invented_symbol")}
        streak: dict[str, int] = {}
        approved_n, approved_sha, wait, wait_n, shown_wrong = None, None, 0.0, 0, 0
        restart_required = None
        for i, a in enumerate(seq, 1):
            al = f"{jid} attempt {a.get('attempt')}"
            if a.get("attempt") != i:
                errs.append(f"{al}: attempts must be numbered 1..n in order (expected {i})")
            sid = a.get("session_id")
            if not isinstance(sid, str) or not sid.strip():
                errs.append(f"{al}: session_id is required (one isolated conversation per id)")
                sid = ""
            out = a.get("outcome")
            if out not in OUTCOMES:
                errs.append(f"{al}: outcome must be one of {', '.join(OUTCOMES)}")
            reasons = a.get("reasons") or []
            if not isinstance(reasons, list) or any(r not in REASON_CODES for r in reasons):
                errs.append(f"{al}: reasons must be codes from {', '.join(REASON_CODES)}")
                reasons = []
            if out == "rejected" and not reasons:
                errs.append(f"{al}: a rejection needs at least one reason code")
            if out != "rejected" and reasons:
                errs.append(f"{al}: reasons are only recorded on a rejection")
            if streak.get(sid, 0) >= 2:
                errs.append(f"{al}: RESTART_REQUIRED - session {sid!r} already had two wrong-target/composition "
                            f"failures; open a clean isolated conversation with a new session_id")
            for r in reasons:
                key = "anatomy_rejection_count" if r == "anatomy" else f"{r}_count"
                if key in counts:
                    counts[key] += 1
            if out == "rejected" and RESTART_REASONS & set(reasons):
                streak[sid] = streak.get(sid, 0) + 1
            elif out in OUTCOMES:
                streak[sid] = 0
            if out == "rejected" and "wrong_target" in reasons and a.get("shown_to_director"):
                shown_wrong += 1
            refs = a.get("references") or []
            if not isinstance(refs, list) or len(refs) > 2:
                errs.append(f"{al}: at most two individual references per generation")
                refs = []
            for r in refs:
                if r in rejected_shas:
                    errs.append(f"{al}: reference {str(r)[:12]} is a rejected candidate; never condition on a failed image")
            if a.get("generator_wait_ms") is not None:
                w = a["generator_wait_ms"]
                if not isinstance(w, (int, float)) or isinstance(w, bool) or w < 0:
                    errs.append(f"{al}: generator_wait_ms must be a measured non-negative number or null")
                else:
                    wait += w
                    wait_n += 1
            if out == "approved":
                if not SHA_RE.match(str(a.get("candidate_sha256") or "")):
                    errs.append(f"{al}: an approved attempt needs candidate_sha256 of the exact approved bytes")
                if a.get("anatomy_present"):
                    exc = (lock_ids or {}).get(jid, {}).get("anatomy_exception") if lock_ids is not None else None
                    if lock_ids is None:
                        errs.append(f"{al}: approved with anatomy_present; pass --locks so the target's anatomy exception can be checked")
                    elif not exc:
                        errs.append(f"{al}: approved with anatomy_present but {jid} has no director anatomy_exception "
                                    f"(an exception for another target does not carry over)")
                if lock_ids is not None and jid in lock_ids and jid not in locks["approved"]:
                    errs.append(f"{al}: approved before the target lock was DIRECTION_APPROVED")
                approved_n, approved_sha = i, a.get("candidate_sha256")
        terminal = seq[-1] if seq else {}
        terminal_sha = terminal.get("candidate_sha256") if terminal.get("outcome") == "approved" else None
        last_sid = terminal.get("session_id")
        if streak.get(last_sid, 0) >= 2 and approved_n != len(seq):
            restart_required = last_sid
        stats[jid] = {"attempt_count": len(seq), **counts, "approved_raw_after_attempt_n": approved_n,
                      "terminal_outcome": terminal.get("outcome"), "terminal_attempt": terminal.get("attempt"),
                      "approved_candidate_sha256": terminal_sha, "last_approved_sha256": approved_sha,
                      "wrong_target_shown_to_director": shown_wrong,
                      "generator_wait_ms": wait if wait_n else None, "generator_wait_measured_n": wait_n,
                      "sessions": len({a.get("session_id") for a in seq}),
                      "restart_required_session": restart_required}
    if errs:
        raise StudioError("attempt log problems:\n  - " + "\n  - ".join(errs))
    fam = {"attempt_count": sum(s["attempt_count"] for s in stats.values()),
           "approved": sum(1 for s in stats.values() if s["approved_candidate_sha256"]),
           "first_attempt_approvals": sum(1 for s in stats.values()
                                          if s["approved_candidate_sha256"] and s["attempt_count"] == 1)}
    for k in ("wrong_target_count", "composition_count", "silhouette_conflict_count", "art_style_drift_count",
              "anatomy_rejection_count", "invented_symbol_count", "wrong_target_shown_to_director"):
        fam[k] = sum(s[k] for s in stats.values())
    measured = [s for s in stats.values() if s["generator_wait_measured_n"]]
    fam["generator_wait_ms"] = sum(s["generator_wait_ms"] for s in measured) if measured else None
    fam["generator_wait_measured_n"] = sum(s["generator_wait_measured_n"] for s in measured)
    fam["generations_per_approved_raw"] = round(fam["attempt_count"] / fam["approved"], 2) if fam["approved"] else None
    return {"doc": doc, "per_jutsu": stats, "family": fam}


# ---------------------------------------------------------------------------------------------
# approved ledger
# ---------------------------------------------------------------------------------------------


def safe_relpath(rel) -> bool:
    return (isinstance(rel, str) and bool(rel) and not rel.startswith("/") and "\\" not in rel
            and not re.match(r"^[A-Za-z]:", rel) and ".." not in PurePosixPath(rel).parts)


def verify_approved(path: Path, spec: dict, raw_root: Path | None = None,
                    source_index: Path | None = None, locks: Path | None = None,
                    attempts: Path | None = None) -> dict:
    """Return the checked plan. Raise StudioError listing every problem found."""
    path = Path(path)
    try:
        approved_bytes = path.read_bytes()  # read once: these bytes are checked and sealed
        doc = json.loads(approved_bytes.decode("utf-8"))
    except FileNotFoundError:
        raise StudioError(f"approved ledger not found: {path}")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StudioError(f"approved ledger is not valid JSON: {exc}")
    nums = spec_numbers(spec)
    root = Path(raw_root) if raw_root else path.parent
    errs: list[str] = []
    if doc.get("schema") != "tnr.jutsu-studio.approved/1":
        errs.append("schema must be 'tnr.jutsu-studio.approved/1'")
    bl = doc.get("bloodline") if isinstance(doc.get("bloodline"), dict) else {}
    family = bl.get("family")
    if not isinstance(family, str) or not SLUG_RE.match(family):
        errs.append("bloodline.family must be a lowercase slug (used in file names, e.g. 'bee')")
    if not bl.get("name"):
        errs.append("bloodline.name is required")
    cap = doc.get("family_byte_cap_exclusive")
    if cap is not None:
        if not isinstance(cap, int) or isinstance(cap, bool) or cap <= 0:
            errs.append("family_byte_cap_exclusive must be a positive integer or null")
        elif not doc.get("family_byte_cap_ruling"):
            errs.append("family_byte_cap_exclusive needs family_byte_cap_ruling: a stricter cap is a director decision, never a default")
        elif cap > nums["byte_ceiling"] + 1:
            errs.append(f"family cap {cap} is looser than the spec ceiling {nums['byte_ceiling']}; omit it")
    fam_acc = doc.get("family_acceptance") or {"status": "PENDING", "evidence": ""}
    if fam_acc.get("status") not in ("PENDING", "ACCEPTED", "REJECTED"):
        errs.append("family_acceptance.status must be PENDING, ACCEPTED or REJECTED")
    if fam_acc.get("status") == "ACCEPTED":
        if not str(fam_acc.get("evidence") or "").strip():
            errs.append("family_acceptance ACCEPTED needs evidence")
        if not SHA_RE.match(str(fam_acc.get("gallery_sha256") or "")):
            errs.append("family_acceptance ACCEPTED must name the exact gallery_sha256 the director accepted; "
                        "acceptance never transfers to a different gallery")
        if not SHA_RE.match(str(fam_acc.get("members_sha256") or "")):
            errs.append("family_acceptance ACCEPTED must name members_sha256 (from the accepted showcase manifest); "
                        "acceptance binds to the exact raw and export bytes too")
        if fam_acc.get("gallery_pixels_sha256") is not None and not SHA_RE.match(str(fam_acc["gallery_pixels_sha256"])):
            errs.append("family_acceptance gallery_pixels_sha256 must be a 64-hex digest when given")
    rows = doc.get("jutsu")
    if not isinstance(rows, list) or not rows:
        raise StudioError("approved ledger problems:\n  - " + "\n  - ".join(errs + ["jutsu must be a non-empty array"]))

    superseded = set()
    for r in rows:
        for s in (r.get("superseded_raw_sha256") or []) if isinstance(r, dict) else []:
            superseded.add(s)
    seen_id, seen_name, seen_slug, seen_raw = {}, {}, {}, {}
    plan = []
    for pos, r in enumerate(rows):
        label = f"jutsu[{pos}]"
        if not isinstance(r, dict):
            errs.append(f"{label} is not an object")
            continue
        jid, name, slug, ver = r.get("jutsu_id"), r.get("name"), r.get("slug"), r.get("version")
        label = f"{label} {name!r}"
        if not isinstance(jid, str) or not jid.strip():
            errs.append(f"{label}: jutsu_id is required")
        elif jid in seen_id:
            errs.append(f"{label}: duplicate jutsu_id {jid} (also {seen_id[jid]})")
        else:
            seen_id[jid] = label
        if not isinstance(name, str) or not name.strip():
            errs.append(f"{label}: name is required")
        elif name_key(name) in seen_name:
            errs.append(f"{label}: duplicate name")
        else:
            seen_name[name_key(name)] = label
        if not isinstance(slug, str) or not SLUG_RE.match(slug):
            errs.append(f"{label}: slug must be a lowercase slug")
        elif slug in seen_slug:
            errs.append(f"{label}: duplicate slug {slug}")
        else:
            seen_slug[slug] = label
        if not isinstance(ver, int) or isinstance(ver, bool) or ver < 1:
            errs.append(f"{label}: version must be an integer >= 1")
        appr = r.get("director_raw_approval") if isinstance(r.get("director_raw_approval"), dict) else {}
        if appr.get("status") != "APPROVED" or not str(appr.get("evidence") or "").strip():
            errs.append(f"{label}: director_raw_approval must be status APPROVED with evidence (chat approval is never assumed)")
        q = r.get("quantize")
        if q is not None:
            if not isinstance(q, dict) or q.get("method") != "MEDIANCUT":
                errs.append(f"{label}: quantize.method must be MEDIANCUT")
            elif not isinstance(q.get("colors"), int) or not 2 <= q["colors"] <= 256:
                errs.append(f"{label}: quantize.colors must be 2..256")
            elif not str(q.get("director_approved") or "").strip():
                errs.append(f"{label}: quantize needs director_approved evidence; palette loss is never automatic")
        raw_rel, raw_sha = r.get("raw_file"), r.get("raw_sha256")
        if not safe_relpath(raw_rel):
            errs.append(f"{label}: raw_file must be a relative path without '..'")
            continue
        if not isinstance(raw_sha, str) or not SHA_RE.match(raw_sha):
            errs.append(f"{label}: raw_sha256 must be a 64-hex digest")
            continue
        if raw_sha in superseded:
            errs.append(f"{label}: raw {raw_sha[:12]} is listed as superseded; a withdrawn raw cannot be a member")
        if raw_sha in seen_raw:
            errs.append(f"{label}: same raw bytes as {seen_raw[raw_sha]}")
        seen_raw[raw_sha] = label
        raw_path = root / raw_rel
        if not raw_path.is_file():
            errs.append(f"{label}: raw file not found: {raw_path}")
            continue
        blob = raw_path.read_bytes()
        if sha256(blob) != raw_sha:
            errs.append(f"{label}: raw_sha256 does not match {raw_rel} (file is {sha256(blob)})")
            continue
        try:
            info = decode(blob)
        except StudioError as exc:
            errs.append(f"{label}: {exc}")
            continue
        if info["width"] != info["height"]:
            errs.append(f"{label}: raw is {info['width']}x{info['height']}; it must be square (cropping is a Studio decision)")
        if min(info["width"], info["height"]) < nums["size"]:
            errs.append(f"{label}: raw {info['width']}px is below the {nums['size']}px export size (no upscaling)")
        if info["exif_orientation"] not in (None, 1):
            errs.append(f"{label}: raw carries EXIF orientation {info['exif_orientation']}; resolve it explicitly")
        if info["has_alpha"]:
            with Image.open(io.BytesIO(blob)) as im:
                alpha = im.convert("RGBA").getchannel("A")
                if alpha.getextrema()[0] < 255:
                    errs.append(f"{label}: raw has real transparency; this path exports designed opaque backgrounds only")
        plan.append({"jutsu_id": jid, "name": name, "slug": slug, "version": ver, "raw_path": str(raw_path),
                     "raw_file": raw_rel, "raw_sha256": raw_sha, "raw_format": info["format"],
                     "raw_size": [info["width"], info["height"]], "raw_bytes": len(blob),
                     "approval": appr, "quantize": q})

    if source_index is not None:
        src = load_json(source_index, "source index")
        sbl = src.get("bloodline") if isinstance(src.get("bloodline"), dict) else {}
        for field in ("id", "name"):  # exact bloodline identity, not only the jutsu set
            want_v = sbl.get(field)
            if want_v in (None, ""):
                continue
            got = bl.get(field)
            if got in (None, ""):
                errs.append(f"bloodline.{field} is required: the intake roster records {want_v!r}")
            elif (name_key(str(got)) != name_key(str(want_v))) if field == "name" else (got != want_v):
                errs.append(f"bloodline.{field} {got!r} != intake {want_v!r}")
        roster = {j["jutsu_id"]: j["name"] for j in src.get("jutsu", [])}
        if not roster:
            errs.append("source index has no roster; N cannot be verified")
        for jid in sorted(set(roster) - set(seen_id)):
            errs.append(f"roster jutsu {jid} ({roster[jid]}) has no approved raw: silent omission refused")
        for jid in sorted(set(seen_id) - set(roster)):
            errs.append(f"approved jutsu {jid} is not in the intake roster")
        for p in plan:
            if p["jutsu_id"] in roster and name_key(roster[p["jutsu_id"]]) != name_key(p["name"]):
                errs.append(f"{p['jutsu_id']}: approved name {p['name']!r} != roster name {roster[p['jutsu_id']]!r}")

    lock_info = attempt_info = None
    evidence: dict[str, dict] = {}
    for key, src_path in (("locks", locks), ("attempts", attempts)):
        if src_path is not None:  # read once; these exact bytes are what is checked and later sealed
            try:
                blob = Path(src_path).read_bytes()
            except OSError as exc:
                raise StudioError(f"{key} file {src_path} cannot be read: {exc}")
            evidence[key] = {"path": str(src_path), "bytes": blob, "sha256": sha256(blob)}
    if locks is not None:
        lock_info = check_locks(locks, source_index, evidence["locks"]["bytes"])
        if bl.get("id") not in (None, "") and lock_info["doc"].get("bloodline", {}).get("id") != bl.get("id"):
            errs.append(f"approved bloodline.id {bl.get('id')!r} != locks bloodline.id "
                        f"{lock_info['doc'].get('bloodline', {}).get('id')!r}")
        for p in plan:
            tg = lock_info["by_id"].get(p["jutsu_id"])
            if tg is None:
                errs.append(f"{p['jutsu_id']}: no target lock")
            elif p["jutsu_id"] not in lock_info["approved"]:
                errs.append(f"{p['jutsu_id']}: target lock is not DIRECTION_APPROVED")
            elif name_key(str(tg.get("name"))) != name_key(p["name"]):
                errs.append(f"{p['jutsu_id']}: lock name {tg.get('name')!r} != approved name {p['name']!r}")
    if attempts is not None:
        attempt_info = check_attempts(attempts, lock_info, evidence["attempts"]["bytes"])
        for p in plan:
            st = attempt_info["per_jutsu"].get(p["jutsu_id"])
            if st is None:
                errs.append(f"{p['jutsu_id']}: the attempt log has no attempt for this jutsu")
            elif st["terminal_outcome"] != "approved":
                errs.append(f"{p['jutsu_id']}: the terminal attempt ({st['terminal_attempt']}) is "
                            f"{st['terminal_outcome']}, not approved; an earlier approval does not survive a later "
                            f"attempt (record a fresh approved attempt to reaffirm it)")
            elif st["approved_candidate_sha256"] != p["raw_sha256"]:
                errs.append(f"{p['jutsu_id']}: approved raw {p['raw_sha256'][:12]} is not the candidate of the terminal "
                            f"approved attempt ({str(st['approved_candidate_sha256'])[:12]})")

    if errs:
        raise StudioError("approved ledger problems:\n  - " + "\n  - ".join(errs))
    return {"doc": doc, "family": family, "bloodline": bl, "cap": cap, "family_acceptance": fam_acc,
            "rows": plan, "approved_sha256": sha256(approved_bytes), "approved_bytes": approved_bytes,
            "approved_path": str(path),
            "source_index_checked": source_index is not None, "locks": lock_info, "attempts": attempt_info,
            "evidence": evidence}


# ---------------------------------------------------------------------------------------------
# export (cached, incremental)
# ---------------------------------------------------------------------------------------------


def transform(raw: bytes, size: int, quantize: dict | None) -> Image.Image:
    with Image.open(io.BytesIO(raw)) as im:
        img = im.convert("RGB")
    if img.size != (size, size):
        img = img.resize((size, size), Image.LANCZOS)
    if quantize:
        img = img.quantize(colors=quantize["colors"], method=Image.Quantize.MEDIANCUT,
                           dither=Image.Dither.NONE).convert("RGB")
    return img


def encode_webp(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "WEBP", lossless=True, method=6, exact=True)
    return buf.getvalue()


def export_name(family: str, row: dict) -> str:
    return f"icon_{family}_{row['slug']}_v{row['version']}.webp"


def export_all(plan: dict, spec: dict, spec_sha: str, out: Path) -> tuple[list[dict], dict]:
    """Export every approved raw. A cache hit is proven from the bytes on disk (raw sha, export sha,
    decoded export pixels == the recorded transformed pixels) without re-decoding or resizing the raw.
    Encoder determinism is probed once per run (first fresh encode is done twice)."""
    nums = spec_numbers(spec)
    versions = encoder_versions()
    exports_dir, cache_dir = out / "exports", out / "cache"
    results, stats = [], {"encoded": 0, "reused": 0, "determinism_probe": "NOT_NEEDED"}
    probe_path = cache_dir / "encoder_determinism.json"
    probe_key = sha256(canon(versions).encode())
    try:
        if json.loads(probe_path.read_text(encoding="utf-8")).get("key") == probe_key:
            stats["determinism_probe"] = "PASS_RECORDED_FOR_THESE_ENCODER_VERSIONS"
    except (OSError, ValueError):
        pass
    for row in plan["rows"]:
        name = export_name(plan["family"], row)
        options = {"size": nums["size"], "resample": "LANCZOS", "mode": "RGB", "webp": "lossless method=6 exact",
                   "quantize": row["quantize"] and {"method": "MEDIANCUT", "colors": row["quantize"]["colors"], "dither": "NONE"}}
        key = sha256(canon({"raw": row["raw_sha256"], "options": options, "spec": spec_sha, "versions": versions}).encode())
        record_path = cache_dir / (name + ".json")
        target = exports_dir / name
        record = json.loads(record_path.read_text(encoding="utf-8")) if record_path.is_file() else None
        if record is not None and record.get("key") != key:
            raise StudioError(f"{name} already exists from different inputs (raw/options/spec/encoder). Bump that jutsu's "
                              f"version instead of reusing a filename; the earlier export is preserved.")
        if record is None and target.exists():
            raise StudioError(f"{target} exists with no cache record; refusing to adopt bytes of unknown provenance")
        raw = Path(row["raw_path"]).read_bytes()
        if sha256(raw) != row["raw_sha256"]:
            raise StudioError(f"{row['raw_file']} changed after verification")
        expected_pixels = None
        if record is not None and target.is_file():
            data = target.read_bytes()
            if sha256(data) != record.get("output_sha256"):
                raise StudioError(f"{target} was modified after export (sha {sha256(data)[:12]} != recorded "
                                  f"{str(record.get('output_sha256'))[:12]}); refusing a tampered cache")
            expected_pixels = record.get("transformed_pixels_sha256")
            if expected_pixels is None:  # record from tool 1.0: prove it the slow way
                expected_pixels = pixels_sha(transform(raw, nums["size"], row["quantize"]))
            stats["reused"] += 1
        else:
            img = transform(raw, nums["size"], row["quantize"])
            expected_pixels = pixels_sha(img)
            data = encode_webp(img)
            if stats["determinism_probe"] == "NOT_NEEDED":
                stats["determinism_probe"] = "PASS" if encode_webp(img) == data else "FAIL"
                if stats["determinism_probe"] == "FAIL":
                    raise StudioError(f"{name}: the encoder is not deterministic in this environment")
                atomic_write(probe_path, dump_json({"key": probe_key, "versions": versions, "probe": name}))
            if record is not None and record.get("output_sha256") != sha256(data):
                raise StudioError(f"{name}: re-encode gives different bytes than the recorded export")
            record = {"key": key, "output": name, "output_sha256": sha256(data), "raw_sha256": row["raw_sha256"],
                      "transformed_pixels_sha256": expected_pixels,
                      "options": options, "spec_sha256": spec_sha, "versions": versions}
            atomic_write(record_path, dump_json(record))  # record first: an interrupted run re-encodes, never adopts
            atomic_write(target, data)
            stats["encoded"] += 1
        # export QC on the actual bytes
        checks, fails = {}, []
        with Image.open(io.BytesIO(data)) as back:
            back.load()
            checks["format"] = back.format
            checks["mode"] = back.mode
            checks["size"] = list(back.size)
            checks["pixels_equal_transformed"] = back.mode == "RGB" and pixels_sha(back) == expected_pixels
        checks["codec"] = webp_codec(data)
        checks["bytes"] = len(data)
        if checks["format"] != "WEBP" or checks["codec"] != "VP8L":
            fails.append(f"not a lossless VP8L WebP ({checks['format']}/{checks['codec']})")
        if checks["mode"] != "RGB" or checks["size"] != [nums["size"], nums["size"]]:
            fails.append(f"decoded {checks['mode']} {checks['size']}, expected RGB {nums['size']}x{nums['size']}")
        if not checks["pixels_equal_transformed"]:
            fails.append("decoded pixels differ from the approved transformed pixels")
        if len(data) > nums["byte_ceiling"]:
            fails.append(f"{len(data)} bytes exceeds the spec ceiling {nums['byte_ceiling']}")
        if plan["cap"] is not None and len(data) >= plan["cap"]:
            fails.append(f"{len(data)} bytes is not under the family cap {plan['cap']} (director-approved quantize is the only remedy this tool applies)")
        if sha256(Path(row["raw_path"]).read_bytes()) != row["raw_sha256"]:
            fails.append("raw bytes changed during export")
        results.append({"jutsu_id": row["jutsu_id"], "name": row["name"], "output": name, "output_sha256": sha256(data),
                        "output_bytes": len(data), "raw_sha256": row["raw_sha256"], "raw_file": row["raw_file"],
                        "raw_format": row["raw_format"], "quantize": options["quantize"], "checks": checks,
                        "transformed_pixels_sha256": expected_pixels,
                        "verdict": "PASS" if not fails else "FAIL", "failures": fails})
    return results, stats


# ---------------------------------------------------------------------------------------------
# canonical preflight (the real script, never a reimplementation)
# ---------------------------------------------------------------------------------------------


PIN_SCRIPT, PIN_SPEC = "scripts/artpreflight.py", "data/25x_DATA_art_spec.json"


def canonical_status(script: Path, spec_path: Path, pins: Path = DEFAULT_PINS) -> dict:
    """D9: canonical only when the script and spec git blobs equal the pinned main blobs."""
    rec = {"canonical": False, "pins_file": Path(pins).name, "script_blob": None, "spec_blob": None,
           "pinned_from_main": None, "reason": None}
    try:
        rec["script_blob"] = git_blob_sha(Path(script).read_bytes())
        rec["spec_blob"] = git_blob_sha(Path(spec_path).read_bytes())
    except OSError as exc:
        rec["reason"] = f"cannot read script/spec: {exc}"
        return rec
    try:
        pin = json.loads(Path(pins).read_text(encoding="utf-8"))
        want_script, want_spec = pin["blobs"][PIN_SCRIPT], pin["blobs"][PIN_SPEC]
        rec["pinned_from_main"] = pin["pinned_from_main"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        rec["reason"] = f"preflight pins unavailable ({exc.__class__.__name__}); canonical status cannot be proven"
        return rec
    bad = []
    if rec["script_blob"] != want_script:
        bad.append(f"artpreflight.py blob {rec['script_blob'][:12]} != pinned {str(want_script)[:12]}")
    if rec["spec_blob"] != want_spec:
        bad.append(f"art spec blob {rec['spec_blob'][:12]} != pinned {str(want_spec)[:12]}")
    if bad:
        rec["reason"] = "; ".join(bad)
    else:
        rec["canonical"] = True
    return rec


def run_preflight(files: list[Path], spec_path: Path, cap: int | None, script: Path = DEFAULT_PREFLIGHT,
                  pins: Path = DEFAULT_PINS) -> dict:
    script = Path(script)
    if not script.is_file():
        return {"verdict": "NOT_RUN", "reason": f"artpreflight script not found at {script}", "command": None}
    canonical = canonical_status(script, spec_path, pins)
    files = [Path(f).resolve() for f in files]
    if len({f.parent for f in files}) != 1:
        raise StudioError("preflight runs over one exports directory")
    names = [f.name for f in files]
    tail = ["--type", TARGET, "--json"] + (["--max-bytes", str(cap)] if cap is not None else [])
    cmd = [sys.executable, str(script.resolve()), *names, "--spec", str(Path(spec_path).resolve()), *tail]
    # Run inside the exports folder with bare file names so the record carries no machine paths
    # and a replay elsewhere records the identical command.
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(files[0].parent))
    shown = ["python3", script.name, *names, "--spec", Path(spec_path).name, *tail]
    record = {"command": " ".join(shown), "cwd": "exports/", "exit_code": proc.returncode,
              "stdout": proc.stdout, "stderr": proc.stderr, "script_sha256": file_sha(script),
              "spec_sha256": file_sha(spec_path), "files": [Path(f).name for f in files],
              "canonical": canonical}
    try:
        parsed = json.loads(proc.stdout)
        rows = parsed["rows"]
        errors = int(parsed["errors"])
    except Exception:
        record.update(verdict="FAIL", reason="preflight output was not the expected JSON; no pass is claimed")
        return record
    seen = {Path(r.get("file", "")).name for r in rows}
    missing = [Path(f).name for f in files if Path(f).name not in seen]
    record["errors"] = errors
    record["error_rows"] = [r for r in rows if r.get("level") == "error"]
    record["warning_rows"] = [r for r in rows if r.get("level") == "warn"]
    if missing:
        record.update(verdict="FAIL", reason=f"preflight output does not cover {missing}")
    elif proc.returncode == 0 and errors == 0 and canonical["canonical"]:
        record["verdict"] = "PASS"
    elif proc.returncode == 0 and errors == 0:
        record.update(verdict="NON_CANONICAL", reason=f"0 errors, but not the pinned canonical tool: {canonical['reason']}")
    else:
        record.update(verdict="FAIL", reason=f"exit {proc.returncode}, {errors} error(s)")
    return record


# ---------------------------------------------------------------------------------------------
# showcase
# ---------------------------------------------------------------------------------------------


def grid_rows(n: int) -> list[int]:
    """Row lengths. N <= 9 follows the established table (5 = 3+2, 8 = 4+4); N >= 10 uses
    ceil(N/4) balanced rows of at most four, longer rows first (RUL-2026-10-19-005 D5)."""
    if n < 1:
        raise StudioError("a showcase needs at least one icon")
    fixed = {1: [1], 2: [2], 3: [3], 4: [2, 2], 5: [3, 2], 6: [3, 3], 7: [4, 3], 8: [4, 4], 9: [3, 3, 3]}
    if n in fixed:
        return fixed[n]
    nrows = -(-n // 4)
    base, extra = divmod(n, nrows)
    return [base + 1] * extra + [base] * (nrows - extra)


def caption_kb(nbytes: int) -> str:
    return f"{nbytes / 1000:.1f}kB"


def fit_caption(draw, name: str, kb: str):
    for size in range(22, 13, -1):
        font, desc = load_font(size)
        if text_width(draw, f"{name}  {kb}", font) <= TILE:
            return [f"{name}  {kb}"], font, desc
    font, desc = load_font(16)
    words = name.split()
    for cut in range(len(words) - 1, 0, -1):
        first, second = " ".join(words[:cut]), " ".join(words[cut:]) + f"  {kb}"
        if text_width(draw, first, font) <= TILE and text_width(draw, second, font) <= TILE:
            return [first, second], font, desc
    raise StudioError(f"caption for {name!r} cannot fit a {TILE}px tile legibly; shorten nothing silently - ask the director")


def layout(rows: list[int]) -> tuple[int, int, list[tuple[int, int, int, int]]]:
    """Canvas size and (row, col, x, y) for each tile, row-major."""
    cols = max(rows)
    width = 2 * MARGIN + cols * TILE + (cols - 1) * GUTTER
    height = 2 * MARGIN + len(rows) * (TILE + CAPTION) + (len(rows) - 1) * GUTTER
    spots = []
    for r, count in enumerate(rows):
        row_w = count * TILE + (count - 1) * GUTTER
        x0 = (width - row_w) // 2
        y = MARGIN + r * (TILE + CAPTION + GUTTER)
        for c in range(count):
            spots.append((r + 1, c + 1, x0 + c * (TILE + GUTTER), y))
    return width, height, spots


def tile_from_export(data: bytes) -> Image.Image:
    with Image.open(io.BytesIO(data)) as im:
        return im.convert("RGB").resize((TILE, TILE), Image.LANCZOS)


def render_canvas(items: list[dict], rows: list[int]) -> tuple[Image.Image, list[dict], set]:
    """items: [{name, output_bytes, tile}] in order. Pure function of its inputs."""
    width, height, spots = layout(rows)
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    placed, fonts = [], set()
    for item, (r, c, x, y) in zip(items, spots):
        canvas.paste(item["tile"], (x, y))
        kb = caption_kb(item["output_bytes"])
        lines, font, desc = fit_caption(draw, item["name"], kb)
        fonts.add(desc)
        ty = y + TILE + 10
        for line in lines:
            if line.endswith(kb):
                head = line[: -len(kb)]
                draw.text((x, ty), head, fill=TEXT, font=font)
                draw.text((x + text_width(draw, head, font), ty), kb, fill=TEXT_DIM, font=font)
            else:
                draw.text((x, ty), line, fill=TEXT, font=font)
            ty += 24
        placed.append({"caption": f"{item['name']} {kb}", "position": {"row": r, "col": c, "x": x, "y": y}})
    return canvas, placed, fonts


def read_verified(path: Path, want_sha: str, what: str) -> bytes:
    """Read bytes and prove they are the recorded ones. Every stage calls this on its inputs."""
    try:
        data = Path(path).read_bytes()
    except OSError as exc:
        raise StudioError(f"{what} {path} cannot be read: {exc}")
    if sha256(data) != want_sha:
        raise StudioError(f"{what} {Path(path).name} is not the recorded bytes (sha {sha256(data)[:12]} != "
                          f"{str(want_sha)[:12]}); refusing to build from substituted input")
    return data


def members_commitment(icons: list[dict]) -> str:
    """Ordered commitment to the family a gallery shows: (jutsu_id, approved raw sha, export sha)."""
    return sha256(canon([[i["jutsu_id"], i["approved_raw_sha256"], i["output_sha256"]] for i in icons]).encode())


def acceptance_for(recorded: dict, gallery_sha: str, gallery_pixels: str, members_sha: str) -> dict:
    """Director family acceptance applies only to the exact family members AND gallery it names (P0 F5).

    The member commitment must match (any changed raw or export bytes invalidate, even when the
    pixels look identical). The gallery matches by file sha against the recorded file sha, or by
    decoded-pixel sha against the recorded pixel sha; the two hash domains are never mixed."""
    status = recorded.get("status", "PENDING")
    named_file, named_pixels = recorded.get("gallery_sha256"), recorded.get("gallery_pixels_sha256")
    named_members = recorded.get("members_sha256")
    gallery_match = ("file" if named_file and named_file == gallery_sha else
                     "pixels" if named_pixels and named_pixels == gallery_pixels else None)
    members_match = bool(named_members) and named_members == members_sha
    matched = gallery_match if members_match else None
    if status == "ACCEPTED":
        state = "ACCEPTED" if matched else "INVALIDATED"
    elif status == "REJECTED":
        state = "REJECTED" if matched else "PENDING"
    else:
        state = "PENDING"
    out = {"status": state, "recorded_status": status, "recorded_gallery_sha256": named_file,
           "recorded_gallery_pixels_sha256": named_pixels, "recorded_members_sha256": named_members,
           "recorded_evidence": recorded.get("evidence"), "matched_by": matched,
           "members_match": members_match, "gallery_match": gallery_match}
    if state == "INVALIDATED":
        why = []
        if not members_match:
            why.append(f"family members changed (accepted {str(named_members)[:12]}, now {members_sha[:12]})")
        if not gallery_match:
            why.append(f"gallery differs (accepted {str(named_file)[:12]})")
        out["note"] = ("acceptance no longer applies: " + "; ".join(why) +
                       ". It needs a fresh director decision on these exact members and pixels.")
    return out


def audit_gallery(gallery: bytes, manifest: dict, exports_dir: Path) -> dict:
    """VALID only if the gallery is exactly the deterministic composite of the recorded export bytes."""
    problems, notes, tiles = [], [], []
    if manifest.get("schema") != "tnr.jutsu-showcase/1":
        problems.append("manifest schema is not tnr.jutsu-showcase/1")
    icons = manifest.get("icons") or []
    rows = manifest.get("row_lengths") or []
    try:
        with Image.open(io.BytesIO(gallery)) as im:
            im.load()
            img = im.convert("RGB")
            fmt = im.format
    except Exception as exc:
        return {"verdict": "INVALID", "problems": [f"gallery is not a decodable image: {exc}"], "notes": [], "tiles": []}
    if fmt != "PNG":
        notes.append(f"gallery container is {fmt}, expected PNG")
    if not icons or sum(rows) != len(icons) or manifest.get("n") != len(icons):
        problems.append(f"manifest n/row_lengths/icons disagree (n={manifest.get('n')}, rows={rows}, icons={len(icons)})")
        return {"verdict": "INVALID", "problems": problems, "notes": notes, "tiles": []}
    layout_problems = []
    if grid_rows(len(icons)) != rows:  # D5: a final gallery must use the approved layout
        layout_problems.append(f"LAYOUT_NONCONFORMING: rows {rows}, approved rule for N={len(icons)} is "
                               f"{grid_rows(len(icons))}")
    width, height, spots = layout(rows)
    if [width, height] != list((manifest.get("geometry") or {}).get("canvas") or []) or img.size != (width, height):
        problems.append(f"canvas {img.size[0]}x{img.size[1]} != layout {width}x{height} (manifest "
                        f"{(manifest.get('geometry') or {}).get('canvas')})")
        return {"verdict": "INVALID", "problems": problems, "notes": notes, "tiles": []}
    seen_out, seen_id, items = set(), set(), []
    for icon, (r, c, x, y) in zip(icons, spots):
        where = f"row {r} col {c} ({icon.get('jutsu_name')!r})"
        if icon.get("output_filename") in seen_out or icon.get("jutsu_id") in seen_id:
            problems.append(f"{where}: duplicate tile ({icon.get('output_filename')})")
        seen_out.add(icon.get("output_filename"))
        seen_id.add(icon.get("jutsu_id"))
        pos = icon.get("position") or {}
        if (pos.get("x"), pos.get("y"), pos.get("row"), pos.get("col")) != (x, y, r, c):
            problems.append(f"{where}: manifest position {pos} != layout ({x},{y})")
        name = str(icon.get("output_filename") or "")
        if not safe_relpath(name) or "/" in name:
            problems.append(f"{where}: unsafe output filename {name!r}")
            continue
        try:
            data = read_verified(Path(exports_dir) / name, icon.get("output_sha256"), "export")
        except StudioError as exc:
            problems.append(f"{where}: {exc}")
            continue
        if len(data) != icon.get("output_bytes"):
            problems.append(f"{where}: output_bytes {icon.get('output_bytes')} != actual {len(data)}")
        want_caption = f"{icon.get('jutsu_name')} {caption_kb(len(data))}"
        if icon.get("caption") != want_caption:
            problems.append(f"{where}: caption {icon.get('caption')!r} != {want_caption!r} (bytes/1000, one decimal)")
        tile = tile_from_export(data)
        ok = img.crop((x, y, x + TILE, y + TILE)).tobytes() == tile.tobytes()
        tiles.append({"row": r, "col": c, "output_filename": name, "pixel_equal": ok})
        if not ok:
            problems.append(f"{where}: tile pixels are not the recorded export resized by LANCZOS - "
                            f"altered, replaced, recoloured or regenerated")
        items.append({"name": icon.get("jutsu_name"), "output_bytes": len(data), "tile": tile})
    if not problems:
        expected, _, _ = render_canvas(items, rows)
        if expected.tobytes() != img.tobytes():
            from PIL import ImageChops
            box = ImageChops.difference(expected, img).getbbox()
            problems.append(f"non-tile pixels (captions/background/gutters) differ from the deterministic render, "
                            f"bounding box {box}")
    if manifest.get("members_sha256") is not None and len(items) == len(icons) and \
            manifest["members_sha256"] != members_commitment(icons):
        problems.append("manifest members_sha256 does not commit to the listed jutsu/raw/export hashes")
    g = manifest.get("gallery") or {}
    if g.get("sha256") and g["sha256"] != sha256(gallery):
        notes.append("gallery file bytes differ from the manifest sha256" +
                     ("; decoded pixels are identical (re-encoded container)" if not problems else ""))
    fidelity = "FAITHFUL" if not problems else "NOT_FAITHFUL"
    all_problems = layout_problems + problems
    return {"verdict": "INVALID" if all_problems else "VALID", "problems": all_problems, "notes": notes,
            "tiles": tiles, "pixel_fidelity": fidelity,
            "layout": "NONCONFORMING" if layout_problems else "CONFORMING",
            "gallery_sha256": sha256(gallery), "gallery_pixels_sha256": pixels_sha(img)}


def build_showcase(exports: list[dict], out: Path, plan: dict, preflight: dict, label: str) -> dict:
    n = len(exports)
    rows = grid_rows(n)
    items, datas = [], {}
    for e in exports:  # P0 F: compose only the recorded export bytes
        data = read_verified(out / "exports" / e["output"], e["output_sha256"], "export")
        datas[e["output"]] = data
        items.append({"name": e["name"], "output_bytes": len(data), "tile": tile_from_export(data)})
    canvas, placed, fonts = render_canvas(items, rows)
    width, height = canvas.size
    icons = []
    for e, pl in zip(exports, placed):
        icons.append({"jutsu_id": e["jutsu_id"], "jutsu_name": e["name"], "approved_raw_sha256": e["raw_sha256"],
                      "output_filename": e["output"], "output_sha256": e["output_sha256"],
                      "output_bytes": e["output_bytes"], **pl})

    stem = f"{plan['family']}_jutsu_showcase_{label}"
    sdir = out / "showcase"
    gallery = png_bytes(canvas)
    gallery_pixels = pixels_sha(canvas)
    phone_img = canvas if width <= PHONE_WIDTH else canvas.resize((PHONE_WIDTH, round(height * PHONE_WIDTH / width)), Image.LANCZOS)
    phone = png_bytes(phone_img)
    thumbs = png_bytes(thumb_qc(exports, datas))
    manifest = {
        "schema": "tnr.jutsu-showcase/1",
        "bloodline": {"id": plan["bloodline"].get("id"), "name": plan["bloodline"].get("name"), "family": plan["family"]},
        "n": n, "row_lengths": rows, "icons": icons,
        "geometry": {"canvas": [width, height], "tile": TILE, "gutter": GUTTER, "margin": MARGIN, "caption_band": CAPTION,
                     "background": list(BG), "rows_centered": True,
                     "layout_rule": "N<=9 table; N>=10 ceil(N/4) balanced rows, longer first (RUL-2026-10-19-005 D5)"},
        "compositor": {"tool": f"jutsu_studio.py {TOOL_VERSION}", "versions": encoder_versions(),
                       "resample": "LANCZOS 256->%d" % TILE, "fonts": sorted(fonts)},
        "caption_units": "bytes/1000, one decimal (decimal kB, not KiB)",
        "gallery": {"file": f"{stem}.png", "sha256": sha256(gallery), "pixels_sha256": gallery_pixels, "bytes": len(gallery)},
        "phone_preview": {"file": f"{stem}_phone.png", "sha256": sha256(phone), "bytes": len(phone)},
        "thumbnail_qc": {"file": f"{plan['family']}_jutsu_thumbs_125_64_32_{label}.png", "sha256": sha256(thumbs), "sizes": list(QC_SIZES)},
        "members_sha256": members_commitment(icons),
        "director_family_acceptance": acceptance_for(plan["family_acceptance"], sha256(gallery), gallery_pixels,
                                                     members_commitment(icons)),
        "canonical_preflight": {k: preflight.get(k) for k in ("verdict", "command", "exit_code", "spec_sha256", "script_sha256", "reason")},
        "status_note": "A family showcase is accepted only by an explicit director decision that names this gallery's sha256; "
                       "N raw approvals are not that decision. Never a game @img asset.",
    }
    audit = audit_gallery(gallery, manifest, out / "exports")  # independent: decodes the written bytes
    if audit["verdict"] != "VALID":
        raise StudioError("showcase failed its own audit: " + "; ".join(audit["problems"]))
    manifest["tile_pixel_equality"] = {"verified_from": "written PNG bytes vs recorded export bytes",
                                       "tiles": len(audit["tiles"]), "all_equal": all(x["pixel_equal"] for x in audit["tiles"])}
    atomic_write(sdir / f"{stem}.png", gallery)
    atomic_write(sdir / f"{stem}_phone.png", phone)
    atomic_write(sdir / manifest["thumbnail_qc"]["file"], thumbs)
    atomic_write(sdir / "showcase_manifest.json", dump_json(manifest))
    return manifest


def png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=False, compress_level=6)
    return buf.getvalue()


def thumb_qc(exports: list[dict], datas: dict[str, bytes]) -> Image.Image:
    pad, label_w = 12, 44
    width = label_w + pad + len(exports) * (QC_SIZES[0] + pad)
    height = pad + sum(s + pad for s in QC_SIZES)
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    font, _ = load_font(14)
    y = pad
    for size in QC_SIZES:
        draw.text((6, y + size // 2 - 8), str(size), fill=TEXT_DIM, font=font)
        for i, e in enumerate(exports):
            with Image.open(io.BytesIO(datas[e["output"]])) as im:
                t = im.convert("RGB").resize((size, size), Image.LANCZOS)
            canvas.paste(t, (label_w + pad + i * (QC_SIZES[0] + pad), y))
        y += size + pad
    return canvas


# ---------------------------------------------------------------------------------------------
# packaging
# ---------------------------------------------------------------------------------------------


def deterministic_zip(members: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, members[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buf.getvalue()


def check_zip(data: bytes, members: dict[str, bytes]) -> None:
    zf = zipfile.ZipFile(io.BytesIO(data))
    if zf.testzip() is not None:
        raise StudioError("built archive fails its CRC test")
    names = zf.namelist()
    if sorted(names) != sorted(members) or len(set(n.casefold() for n in names)) != len(names):
        raise StudioError("built archive membership differs from the plan")
    for n in names:
        if not safe_relpath(n) or sha256(zf.read(n)) != sha256(members[n]):
            raise StudioError(f"built archive member {n} is unsafe or differs from its source")


def place_archive(path: Path, data: bytes) -> str:
    """Write once. An identical rerun is a no-op; different bytes under the same name are refused."""
    if path.exists():
        if path.read_bytes() == data:
            return "UNCHANGED"
        raise StudioError(f"{path} exists with different contents. Use a new --label; the earlier archive is preserved.")
    atomic_write(path, data)
    return "WRITTEN"


def final_ledger(plan, exports, preflight, showcase, archives, spec_sha) -> dict:
    by_id = {e["jutsu_id"]: e for e in exports}
    locks = plan.get("locks")
    rows = []
    for r in plan["rows"]:
        e = by_id[r["jutsu_id"]]
        gates = check_gates({
            "ORIGINAL_SOURCE_VERIFIED": "VERIFIED" if plan.get("source_index_checked") else "NOT_CHECKED",
            "DIRECTION_APPROVED": ("NOT_RECORDED" if locks is None else
                                   "APPROVED" if r["jutsu_id"] in locks["approved"] else "PENDING"),
            "RAW_VISUAL_APPROVED": "APPROVED",
            "OUTPUT_LOCAL_QC": e["verdict"],
            "CANONICAL_PREFLIGHT": preflight.get("verdict", "NOT_RUN"),
            "FAMILY_SHOWCASE_ACCEPTED": showcase["director_family_acceptance"]["status"] if showcase else "NOT_BUILT",
            "ZIP_DELIVERED": "BUILT_NOT_DELIVERED" if archives else "NOT_BUILT",
            "GIT_BINARY_PIN": "NOT_PERFORMED", "USER_UPLOAD_READBACK": "NOT_PERFORMED",
        }, label=r["jutsu_id"])
        rows.append({
            "jutsu_id": r["jutsu_id"], "name": r["name"], "version": r["version"],
            "raw_file": r["raw_file"], "raw_sha256": r["raw_sha256"], "raw_format": r["raw_format"],
            "output": e["output"], "output_sha256": e["output_sha256"], "output_bytes": e["output_bytes"],
            "quantize": e["quantize"], "raw_visual_approval_evidence": r["approval"].get("evidence"),
            "attempts": (plan["attempts"]["per_jutsu"].get(r["jutsu_id"]) if plan.get("attempts") else None),
            "gates": gates,
        })
    return {"schema": "tnr.jutsu-studio.ledger/2", "stage": "finalize",
            "bloodline": plan["bloodline"], "family": plan["family"], "n": len(rows),
            "family_byte_cap_exclusive": plan["cap"], "family_byte_cap_ruling": plan["doc"].get("family_byte_cap_ruling"),
            "approved_ledger_sha256": plan["approved_sha256"], "spec_sha256": spec_sha,
            "locks_sha256": plan["evidence"].get("locks", {}).get("sha256"),
            "attempts_sha256": plan["evidence"].get("attempts", {}).get("sha256"),
            "tool": encoder_versions(), "rows": rows, "collection_gates": collection_gates(rows),
            "attempt_statistics": plan["attempts"]["family"] if plan.get("attempts") else None,
            "showcase_gallery_sha256": showcase and showcase["gallery"]["sha256"],
            "family_acceptance": showcase and showcase["director_family_acceptance"],
            "live_game_requests": 0, "live_game_writes": 0}


STAGES = ("export", "preflight", "showcase", "pack")


def finalize(approved: Path, out: Path, spec_path: Path = DEFAULT_SPEC, label: str = "v1", raw_root: Path | None = None,
             source_index: Path | None = None, preflight_script: Path = DEFAULT_PREFLIGHT, stop_after: str | None = None,
             timings: dict | None = None, locks: Path | None = None, attempts: Path | None = None,
             pins: Path = DEFAULT_PINS, on_stage=None) -> dict:
    """on_stage(name) runs after each stage; the selftest uses it to substitute files between stages."""
    timings = {} if timings is None else timings
    if not SLUG_RE.match(label.replace("-", "_").replace(".", "_")):
        raise StudioError("--label must be a simple token like v1 or 2026-10-17")
    out = Path(out)
    t = time.perf_counter()
    spec = load_spec(spec_path)
    spec_sha = file_sha(spec_path)
    plan = verify_approved(approved, spec, raw_root, source_index, locks, attempts)
    timings["verify_ms"] = round((time.perf_counter() - t) * 1000, 1)

    t = time.perf_counter()
    exports, stats = export_all(plan, spec, spec_sha, out)
    timings["export_ms"] = round((time.perf_counter() - t) * 1000, 1)
    qc = {"schema": "tnr.jutsu-studio.export-qc/1", "spec_sha256": spec_sha, "label": label,
          "family_byte_cap_exclusive": plan["cap"], "exports": exports}
    atomic_write(out / "qc" / f"export_qc_{label}.json", dump_json(qc))
    result = {"exports": exports, "cache": stats, "preflight": {"verdict": "NOT_RUN"}, "showcase": None,
              "archives": {}, "timings": timings}
    if any(e["verdict"] != "PASS" for e in exports):
        bad = "; ".join(f"{e['output']}: {', '.join(e['failures'])}" for e in exports if e["verdict"] != "PASS")
        raise StudioError(f"export QC failed - nothing further is built: {bad}")
    if on_stage:
        on_stage("export")
    if stop_after == "export":
        return result

    t = time.perf_counter()
    for e in exports:
        read_verified(out / "exports" / e["output"], e["output_sha256"], "export")
    preflight = run_preflight([out / "exports" / e["output"] for e in exports], Path(spec_path), plan["cap"],
                              preflight_script, pins)
    timings["preflight_ms"] = round((time.perf_counter() - t) * 1000, 1)
    atomic_write(out / "qc" / f"preflight_{label}.json", dump_json(preflight))
    result["preflight"] = preflight
    if preflight["verdict"] == "FAIL":
        raise StudioError(f"canonical preflight FAILED ({preflight.get('reason')}); see {out}/qc/preflight_{label}.json")
    if on_stage:
        on_stage("preflight")
    if stop_after == "preflight":
        return result

    t = time.perf_counter()
    showcase = build_showcase(exports, out, plan, preflight, label)
    timings["showcase_ms"] = round((time.perf_counter() - t) * 1000, 1)
    result["showcase"] = showcase
    if on_stage:
        on_stage("showcase")
    if stop_after == "showcase":
        return result

    t = time.perf_counter()
    members: dict[str, bytes] = {}
    for r in plan["rows"]:  # re-prove every sealed input: a swap after an earlier stage is refused
        members[f"raws/raw_{r['slug']}_v{r['version']}{FORMAT_EXT.get(r['raw_format'], '.bin')}"] = \
            read_verified(Path(r["raw_path"]), r["raw_sha256"], "approved raw")
    for e in exports:
        members[f"exports/{e['output']}"] = read_verified(out / "exports" / e["output"], e["output_sha256"], "export")
    sdir = out / "showcase"
    for f in ("gallery", "phone_preview", "thumbnail_qc"):
        members[f"showcase/{showcase[f]['file']}"] = read_verified(sdir / showcase[f]["file"], showcase[f]["sha256"], "showcase file")
    members["showcase/showcase_manifest.json"] = read_verified(sdir / "showcase_manifest.json",
                                                               sha256(dump_json(showcase)), "showcase manifest")
    verdict = preflight.get("verdict", "NOT_RUN")
    dist = out / "dist"
    cname = f"{plan['family']}_jutsu_icons_closeout_{label}.zip"
    # D6: never named "upload"; the preflight verdict is in the name
    wname = f"{plan['family']}_jutsu_icons_webps_PREFLIGHT_{verdict}_{len(exports)}webp_{label}.zip"
    ledger = final_ledger(plan, exports, preflight, showcase, True, spec_sha)
    members["manifest/studio_ledger.json"] = dump_json(ledger)
    read_verified(Path(plan["approved_path"]), plan["approved_sha256"], "approved ledger")
    members["manifest/approved.json"] = plan["approved_bytes"]
    for key, ev in plan["evidence"].items():  # seal the verified bytes, and refuse if the file moved since
        read_verified(Path(ev["path"]), ev["sha256"], f"{key} record")
        members[f"manifest/{key}.json"] = ev["bytes"]
    members[f"qc/export_qc_{label}.json"] = dump_json(qc)
    members[f"qc/preflight_{label}.json"] = dump_json(preflight)
    members["SHA256SUMS"] = "".join(f"{sha256(members[n])}  {n}\n" for n in sorted(members)).encode()
    closeout = deterministic_zip(members)
    check_zip(closeout, members)
    flat_members = {e["output"]: members[f"exports/{e['output']}"] for e in exports}
    flat = deterministic_zip(flat_members)
    check_zip(flat, flat_members)
    archives = {
        "closeout": {"file": cname, "sha256": sha256(closeout), "bytes": len(closeout), "members": len(members),
                     "state": place_archive(dist / cname, closeout)},
        "webps": {"file": wname, "sha256": sha256(flat), "bytes": len(flat), "members": len(flat_members),
                  "preflight_verdict": verdict, "state": place_archive(dist / wname, flat)},
    }
    atomic_write(out / "studio_ledger.json", dump_json(ledger | {"archives": archives}))
    timings["pack_ms"] = round((time.perf_counter() - t) * 1000, 1)
    atomic_write(out / "qc" / f"timings_{label}.json", dump_json({"timings_ms": timings, "cache": stats}))
    result["archives"] = archives
    result["ledger"] = ledger
    if on_stage:
        on_stage("pack")
    return result


def print_finalize(result: dict, out: Path) -> None:
    print("| Jutsu | Export | Bytes | QC |")
    print("|---|---|---|---|")
    for e in result["exports"]:
        print(f"| {e['name']} | {e['output']} | {e['output_bytes']} ({caption_kb(e['output_bytes'])}) | {e['verdict']} |")
    p = result["preflight"]
    print(f"\ncanonical preflight: {p.get('verdict')}  {p.get('command') or p.get('reason')}")
    if p.get("verdict") in ("NOT_RUN", "NON_CANONICAL"):
        print(f"  {p.get('verdict')} is not a pass; run the pinned artpreflight.py --type JUTSU_ICON on the exports "
              f"before claiming one ({p.get('reason')}).")
    if result["showcase"]:
        s = result["showcase"]
        print(f"showcase: {s['gallery']['file']} rows {s['row_lengths']} sha256 {s['gallery']['sha256'][:12]}; "
              f"family acceptance: {s['director_family_acceptance'].get('status')}")
        if s["director_family_acceptance"].get("note"):
            print(f"  {s['director_family_acceptance']['note']}")
    for k, a in result["archives"].items():
        print(f"{k}: dist/{a['file']}  {a['bytes']} B  sha256 {a['sha256']}  ({a['state']})")
    print(f"cache: {result['cache']}  timings ms: {result['timings']}")
    print(f"output: {out}/")


# ---------------------------------------------------------------------------------------------
# compare: pre-approval review aid (P0 C) - never a gallery
# ---------------------------------------------------------------------------------------------

COMPARE_BANNER = "REVIEW AID - NOT A GALLERY - candidate first, then approved family"


def compare(candidate: Path, family: list[Path], out: Path, label: str = "c1") -> dict:
    """Candidate beside the approved family at 125/64/32 for the studio's own distinctness judgement.
    Deterministic, non-generative; the candidate bytes are only read."""
    if not SLUG_RE.match(label.replace("-", "_").replace(".", "_")):
        raise StudioError("--label must be a simple token like c1")
    if not family:
        raise StudioError("compare needs at least one approved family file")
    files = [Path(candidate)] + [Path(f) for f in family]
    blobs = []
    for f in files:
        try:
            data = f.read_bytes()
        except OSError as exc:
            raise StudioError(f"cannot read {f}: {exc}")
        decode(data)
        blobs.append(data)
    shas = [sha256(b) for b in blobs]
    if len(set(shas)) != len(shas):
        raise StudioError("compare inputs contain the same bytes twice (is the candidate already in the family list?)")
    pad, label_w, head = 12, 44, 30
    width = label_w + pad + len(files) * (QC_SIZES[0] + pad)
    height = head + pad + sum(s + pad for s in QC_SIZES)
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    font, _ = load_font(14)
    draw.text((pad, 8), COMPARE_BANNER, fill=TEXT, font=font)
    y, cells, expected = head + pad, [], {}
    for size in QC_SIZES:
        draw.text((6, y + size // 2 - 8), str(size), fill=TEXT_DIM, font=font)
        for i, data in enumerate(blobs):
            with Image.open(io.BytesIO(data)) as im:
                tile = im.convert("RGB").resize((size, size), Image.LANCZOS)
            x = label_w + pad + i * (QC_SIZES[0] + pad)
            canvas.paste(tile, (x, y))
            expected[(i, size)] = (x, y, tile)
            cells.append({"file": files[i].name, "sha256": shas[i], "role": "candidate" if i == 0 else "family",
                          "size": size, "x": x, "y": y})
        y += size + pad
    for (i, size), (x, y0, tile) in expected.items():
        if canvas.crop((x, y0, x + size, y0 + size)).tobytes() != tile.tobytes():
            raise StudioError(f"compare cell for {files[i].name} at {size}px is not its exact resize")
    for f, s in zip(files, shas):
        if file_sha(f) != s:
            raise StudioError(f"{f} changed while building the compare sheet")
    png = png_bytes(canvas)
    record = {"schema": "tnr.jutsu-studio.compare/1", "status": COMPARE_BANNER, "label": label,
              "candidate": {"file": files[0].name, "sha256": shas[0]},
              "family": [{"file": f.name, "sha256": s} for f, s in zip(files[1:], shas[1:])],
              "sizes": list(QC_SIZES), "resample": "LANCZOS", "cells": cells,
              "sheet": {"file": f"compare_{label}.png", "sha256": sha256(png)},
              "note": "Distinctness of silhouette and action is the studio's visual judgement (ISOLATED_ART_GENERATION.md "
                      "fail-fast gate 2); this sheet only puts the evidence side by side. Colour similarity is not a rejection."}
    out = Path(out)
    place_archive(out / f"compare_{label}.png", png)
    place_archive(out / f"compare_{label}.json", dump_json(record))
    return record


# ---------------------------------------------------------------------------------------------
# doctor: can this container run the canonical path?
# ---------------------------------------------------------------------------------------------


def doctor(spec_path: Path = DEFAULT_SPEC, script: Path = DEFAULT_PREFLIGHT, pins: Path = DEFAULT_PINS,
           git_ref: str | None = None) -> dict:
    checks, verdict, reason = [], None, None

    def add(name, ok, detail):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
        return ok

    add("pillow", True, f"Pillow {PIL.__version__}, libwebp {features.version('webp') or 'unknown'}")
    probe = synth_image(3, 256)
    try:
        data = encode_webp(probe)
        ok = webp_codec(data) == "VP8L"
        with Image.open(io.BytesIO(data)) as back:
            ok = ok and back.convert("RGB").tobytes() == probe.tobytes()
        add("webp_lossless", ok, "lossless VP8L round-trip" + ("" if ok else " FAILED"))
        add("encoder_determinism", encode_webp(probe) == data, "same input encodes to the same bytes")
    except Exception as exc:
        add("webp_lossless", False, f"{exc.__class__.__name__}: {exc}")
        data = None
    try:
        spec = load_spec(spec_path)
        nums = spec_numbers(spec)
        add("art_spec", True, f"{Path(spec_path).name} JUTSU_ICON size {nums['size']}, ceiling {nums['byte_ceiling']}")
    except Exception as exc:
        add("art_spec", False, str(exc))
        reason = f"art spec unusable: {exc}"
    if not add("artpreflight_present", Path(script).is_file(), str(Path(script).name)):
        reason = reason or f"artpreflight script not found at {script}"
    canon = canonical_status(script, spec_path, pins) if Path(script).is_file() and Path(spec_path).is_file() else None
    if canon is not None:
        add("canonical_pins", canon["canonical"], canon["reason"] or f"blobs match pins from main {canon['pinned_from_main']}")
    if git_ref and canon is not None:
        try:
            rels = {"script": f"skills/producing-tnr-art/{PIN_SCRIPT}", "spec": f"skills/producing-tnr-art/{PIN_SPEC}"}
            got = {k: subprocess.run(["git", "rev-parse", f"{git_ref}:{v}"], capture_output=True, text=True,
                                     cwd=str(SCRIPT_DIR), check=True).stdout.strip() for k, v in rels.items()}
            same = got["script"] == canon["script_blob"] and got["spec"] == canon["spec_blob"]
            add("git_ref_blobs", same, f"{git_ref}: script {got['script'][:12]}, spec {got['spec'][:12]}")
        except Exception as exc:
            add("git_ref_blobs", False, f"git comparison unavailable: {exc.__class__.__name__}")
    if reason is None and data is not None:
        with tempfile.TemporaryDirectory(prefix="jutsu-doctor-") as tmp:
            f = Path(tmp) / "doctor_probe_jutsu_icon.webp"
            f.write_bytes(encode_webp(synth_image(3, nums["size"])))
            rec = run_preflight([f], Path(spec_path), None, Path(script), pins)
        ran = rec.get("exit_code") is not None and rec["verdict"] in ("PASS", "NON_CANONICAL")
        add("artpreflight_probe_run", ran, f"exit {rec.get('exit_code')}, verdict {rec['verdict']}"
                                           + (f" ({rec.get('reason')})" if rec.get("reason") else ""))
        if not ran:
            reason = f"artpreflight probe did not run cleanly: {rec.get('reason') or rec.get('stderr', '')[:200]}"
    # Every failed check blocks green. canonical_pins is reported through the NON_CANONICAL verdict;
    # a git_ref_blobs check exists only when --git-ref was supplied, and then it must pass.
    failed = [c["check"] for c in checks if not c["ok"] and c["check"] != "canonical_pins"]
    if reason:
        verdict = f"NOT_RUN: {reason}"
    elif failed:
        verdict = f"NOT_READY: failed {', '.join(failed)}"
    elif canon and canon["canonical"]:
        verdict = "RUN_CAPABLE_CANONICAL"
    else:
        verdict = f"RUN_CAPABLE_NON_CANONICAL: {canon and canon['reason']}"
    return {"verdict": verdict, "checks": checks, "canonical": canon, "live_game_requests": 0}


# ---------------------------------------------------------------------------------------------
# synthetic benchmark (socket-free)
# ---------------------------------------------------------------------------------------------


def synth_image(seed: int, size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), (10 + seed * 7 % 40, 12, 30 + seed * 13 % 60))
    d = ImageDraw.Draw(img)
    for k in range(6):
        a = (seed * 37 + k * 53) % size
        b = (seed * 71 + k * 29) % size
        d.ellipse((a // 2, b // 2, a // 2 + size // 3, b // 2 + size // 4),
                  fill=((seed * 50 + k * 30) % 256, (k * 70) % 256, (seed * 90) % 256))
        d.line((0, a, size, b), fill=(240, 220 - k * 20, 200), width=max(2, size // 64))
    return img


def bench(sizes: list[int], workdir: Path | None = None) -> list[dict]:
    import shutil
    base = Path(tempfile.mkdtemp(prefix="jutsu-studio-bench-", dir=workdir))
    results = []
    try:
        for n in sizes:
            root = base / f"n{n}"
            root.mkdir()
            names = [f"Bench Technique {i + 1}" for i in range(n)]
            pack = {}
            roster = {"bloodline": {"id": f"bench{n}", "name": f"Bench {n}"}, "jutsu": []}
            for i, name in enumerate(names):
                buf = io.BytesIO()
                synth_image(i, 128).save(buf, "PNG")
                fname = f"legacy/{i:02d}.png"
                pack[fname] = buf.getvalue()
                roster["jutsu"].append({"jutsu_id": f"id{n}_{i}", "name": name, "file": fname, "sha256": sha256(buf.getvalue())})
            pack["manifest.json"] = json.dumps(roster).encode()
            (root / "pack.zip").write_bytes(deterministic_zip(pack))
            t_in = {}
            code = intake(root / "pack.zip", root / "intake", timings=t_in)
            (root / "raws").mkdir()
            appr = json.loads((root / "intake" / "approved_template.json").read_text())
            appr["bloodline"]["family"] = f"bench{n}"
            for i, row in enumerate(appr["jutsu"]):
                p = root / "raws" / f"r{i}.png"
                synth_image(i + 100, 1024).save(p, "PNG")
                row.update(raw_file=f"raws/r{i}.png", raw_sha256=file_sha(p),
                           director_raw_approval={"status": "APPROVED", "evidence": "synthetic benchmark"})
            ap_path = root / "approved.json"
            ap_path.write_bytes(dump_json(appr))
            t_full = {}
            r1 = finalize(ap_path, root / "final", label="v1", source_index=root / "intake" / "source_index.json", timings=t_full)
            # one changed icon: new raw, new version
            p = root / "raws" / "r0b.png"
            synth_image(999, 1024).save(p, "PNG")
            appr["jutsu"][0].update(raw_file="raws/r0b.png", raw_sha256=file_sha(p), version=2,
                                     superseded_raw_sha256=[appr["jutsu"][0]["raw_sha256"]])
            ap_path.write_bytes(dump_json(appr))
            t_inc = {}
            r2 = finalize(ap_path, root / "final", label="v2", source_index=root / "intake" / "source_index.json", timings=t_inc)
            results.append({"n": n, "intake_exit": code, "intake": t_in, "full": t_full, "full_cache": r1["cache"],
                            "incremental": t_inc, "incremental_cache": r2["cache"],
                            "preflight": r1["preflight"]["verdict"]})
    finally:
        shutil.rmtree(base, ignore_errors=True)
    return results


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("doctor", help="can this container run the canonical JUTSU_ICON path?")
    d.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    d.add_argument("--preflight-script", type=Path, default=DEFAULT_PREFLIGHT)
    d.add_argument("--git-ref", default=None, help="also compare script/spec blobs with this git ref (needs git)")
    p = sub.add_parser("intake", help="safe ZIP intake, mapping, report, ledger, approval template")
    p.add_argument("zip", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--roster", type=Path, help="director roster JSON or CSV (jutsu_id,name[,file][,evidence_level])")
    p.add_argument("--ref", default=None, help="git ref/SHA for style-exemplar raw URLs (default: index default, main)")
    lk = sub.add_parser("lock-check", help="target-lock completeness and approval integrity")
    lk.add_argument("locks", type=Path)
    lk.add_argument("--source-index", type=Path, default=None)
    at = sub.add_parser("attempts", help="validate the attempt log and print failure statistics")
    at.add_argument("attempts", type=Path)
    at.add_argument("--locks", type=Path, default=None)
    cp = sub.add_parser("compare", help="candidate beside the approved family at 125/64/32 (review aid)")
    cp.add_argument("candidate", type=Path)
    cp.add_argument("family", type=Path, nargs="+")
    cp.add_argument("--out", type=Path, required=True)
    cp.add_argument("--label", default="c1")
    for name in ("verify-approved", "finalize"):
        q = sub.add_parser(name)
        q.add_argument("approved", type=Path)
        q.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
        q.add_argument("--raw-root", type=Path, default=None, help="base for raw_file paths (default: approved.json's folder)")
        q.add_argument("--source-index", type=Path, default=None, help="intake source_index.json: proves N and IDs match")
        q.add_argument("--locks", type=Path, default=None, help="target locks: every raw needs a DIRECTION_APPROVED lock")
        q.add_argument("--attempts", type=Path, default=None, help="attempt log: every raw must be its last approved candidate")
        if name == "finalize":
            q.add_argument("--out", type=Path, required=True)
            q.add_argument("--label", default="v1")
            q.add_argument("--preflight-script", type=Path, default=DEFAULT_PREFLIGHT)
            q.add_argument("--stop-after", choices=STAGES[:-1])
    ag = sub.add_parser("audit-gallery", help="VALID/INVALID for a gallery PNG against its manifest and exports")
    ag.add_argument("gallery", type=Path)
    ag.add_argument("--manifest", type=Path, required=True)
    ag.add_argument("--exports", type=Path, required=True)
    b = sub.add_parser("bench", help="socket-free synthetic timing of intake/finalize/incremental rerun")
    b.add_argument("--sizes", default="5,8,12")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "doctor":
            res = doctor(args.spec, args.preflight_script, git_ref=args.git_ref)
            for c in res["checks"]:
                print(f"  {'ok  ' if c['ok'] else 'FAIL'} {c['check']}: {c['detail']}")
            print(f"doctor: {res['verdict']}")
            return 0 if res["verdict"] == "RUN_CAPABLE_CANONICAL" else 3
        if args.cmd == "intake":
            return intake(args.zip, args.out, args.roster, args.ref)
        if args.cmd == "lock-check":
            res = check_locks(args.locks, args.source_index)
            for jid, tg in res["by_id"].items():
                state = ("LOCK_INCOMPLETE: " + ", ".join(res["incomplete"][jid]) if jid in res["incomplete"] else
                         "DIRECTION_APPROVED" if jid in res["approved"] else "COMPLETE, direction PENDING")
                print(f"  {jid}  {tg.get('name')}  v{tg.get('version')}  lock {lock_sha(tg)[:12]}  {state}")
            for jid in sorted(set(res["incomplete"]) - set(res["by_id"])):
                print(f"  {jid}  LOCK_INCOMPLETE: {', '.join(res['incomplete'][jid])}")
            return 3 if res["incomplete"] else 0
        if args.cmd == "attempts":
            lock_info = check_locks(args.locks) if args.locks else None
            res = check_attempts(args.attempts, lock_info)
            for jid, s in res["per_jutsu"].items():
                flag = f"  RESTART_REQUIRED (session {s['restart_required_session']})" if s["restart_required_session"] else ""
                print(f"  {jid}: {s['attempt_count']} attempt(s), approved at {s['approved_raw_after_attempt_n']}, "
                      f"wrong_target {s['wrong_target_count']}, silhouette {s['silhouette_conflict_count']}, "
                      f"drift {s['art_style_drift_count']}, anatomy {s['anatomy_rejection_count']}{flag}")
            print(json.dumps(res["family"], indent=1))
            return 0
        if args.cmd == "compare":
            rec = compare(args.candidate, args.family, args.out, args.label)
            print(f"{rec['status']}: {args.out}/{rec['sheet']['file']} sha256 {rec['sheet']['sha256']}")
            return 0
        if args.cmd == "verify-approved":
            plan = verify_approved(args.approved, load_spec(args.spec), args.raw_root, args.source_index,
                                   args.locks, args.attempts)
            print(f"approved ledger OK: {plan['bloodline'].get('name')} ({plan['family']}), N={len(plan['rows'])}, "
                  f"cap={plan['cap'] or 'spec ceiling'}, family acceptance {plan['family_acceptance'].get('status')} "
                  f"(binds to gallery {str(plan['family_acceptance'].get('gallery_sha256'))[:12]})")
            for r in plan["rows"]:
                print(f"  {r['jutsu_id']}  {r['name']}  v{r['version']}  {r['raw_format']} {r['raw_size'][0]}x{r['raw_size'][1]}  "
                      f"{r['raw_sha256'][:12]}{'  quantize ' + str(r['quantize']['colors']) if r['quantize'] else ''}")
            return 0
        if args.cmd == "finalize":
            result = finalize(args.approved, args.out, args.spec, args.label, args.raw_root, args.source_index,
                              args.preflight_script, args.stop_after, locks=args.locks, attempts=args.attempts)
            print_finalize(result, args.out)
            return 0
        if args.cmd == "audit-gallery":
            res = audit_gallery(args.gallery.read_bytes(), load_json(args.manifest, "showcase manifest"), args.exports)
            for x in res["problems"]:
                print(f"  INVALID: {x}")
            for x in res["notes"]:
                print(f"  note: {x}")
            print(f"audit-gallery: {res['verdict']}  (pixel fidelity {res.get('pixel_fidelity', 'NOT_FAITHFUL')}, "
                  f"layout {res.get('layout', '-')})  gallery sha256 {res.get('gallery_sha256', '-')}")
            return 0 if res["verdict"] == "VALID" else 1
        if args.cmd == "bench":
            sizes = [int(s) for s in args.sizes.split(",") if s.strip()]
            res = bench(sizes)
            print("| N | intake ms | full finalize ms (export/preflight/showcase/pack) | incremental ms (export/...) | re-encoded |")
            print("|---|---|---|---|---|")
            for r in res:
                f, i = r["full"], r["incremental"]
                fmt = lambda t: f"{sum(v for k, v in t.items() if k != 'verify_ms'):.0f} ({t.get('export_ms', 0):.0f}/{t.get('preflight_ms', 0):.0f}/{t.get('showcase_ms', 0):.0f}/{t.get('pack_ms', 0):.0f})"
                print(f"| {r['n']} | {r['intake']['total_ms']:.0f} | {fmt(f)} | {fmt(i)} | {r['incremental_cache']['encoded']} of {r['n']} |")
            print(json.dumps(res, indent=1))
            return 0
    except StudioError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
