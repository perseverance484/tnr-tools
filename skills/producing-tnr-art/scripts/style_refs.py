#!/usr/bin/env python3
"""style_refs.py - the durable TNR visual reference pack: verify, list, select.

Every future art session should look at the same approved live artwork before
generating anything, instead of reconstructing "TNR style" from chat memory or
prose. This script owns that corpus's integrity and its per-target selection.

    References calibrate; the spec governs.

`25x_DATA_art_spec.json` remains the authority for house-style clauses, target
numbers, aspect, delivered width, format, chroma, byte ceilings and the measured
signature. Nothing in `style_refs.json` restates any of them; the index carries
provenance, bytes, hashes and selection metadata only.

Layout, deliberately split so the skill ZIP stays small:

    art/style_refs/scene_characters/*      binary references, repo-only
    art/style_refs/scene_backgrounds/*     binary references, repo-only
    skills/producing-tnr-art/data/style_refs.json    packaged index
    skills/producing-tnr-art/scripts/style_refs.py   this file, packaged

Commands
  verify       exact-byte/dimension/format/provenance audit of the checked-in
               pack. Needs a repo checkout. Socket-free.
  list         every reference and its metadata, filtered by target/register.
  select       the deterministic small reference set for one production target.
               Works from the packaged JSON alone by emitting raw URLs, so an
               installed skill with no checkout is still useful.
  materialize  MAINTAINER ONLY. Re-downloads the reference bytes from the image
               URLs already persisted in the committed capture and rewrites the
               index. This is the only command that touches the network, and it
               fetches CDN image URLs only - never the TNR API.
  --selftest   socket-free unit tests over synthesized fixtures.

Image headers are decoded with stdlib struct/zlib like rawqc.py, so verify and
the selftest carry no Pillow dependency. `materialize` cross-checks with Pillow
when it is importable and is happy without it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys
import zlib
from pathlib import Path

SCHEMA = "tnr.style_refs"
VERSION = 1

TARGET_DIRS = {
    "SCENE_CHARACTER": "art/style_refs/scene_characters",
    "SCENE_BACKGROUND": "art/style_refs/scene_backgrounds",
}
TARGETS = tuple(TARGET_DIRS)
REGISTERS = ("NINJA", "CIVILIAN")
PRIORITIES = ("PRIMARY", "SUPPORTING")
PRIORITY_RANK = {name: i for i, name in enumerate(PRIORITIES)}
DEFAULT_LIMIT = {"SCENE_CHARACTER": 4, "SCENE_BACKGROUND": 3}

EXT_FOR_FORMAT = {"PNG": ".png", "WEBP": ".webp", "JPEG": ".jpg", "GIF": ".gif"}

# The asset CDN refuses the stock urllib User-Agent with a 403. Identify the tool
# honestly rather than impersonating a browser.
USER_AGENT = "tnr-tools/style_refs.py (reference-pack materialization)"

# The v1 pack is grounded in exactly one approved read-only capture. Pinning the
# manifest path here is what makes provenance fail-closed: neither a crafted
# index nor a --result override can point the pack at a different capture. A v2
# grounded in a different capture changes this constant deliberately.
APPROVED_CAPTURE = {
    "manifest": "push/03_tnr_art_style_reference_capture.json",
    "reads": 18,
}
APPROVED_CAPTURE_MANIFEST = APPROVED_CAPTURE["manifest"]
EXPECTED_CAPTURE_COUNT = APPROVED_CAPTURE["reads"]
EXPECTED_CAPTURE_PROC = "gameAsset.get"
HARVEST_INBOX = "harvests/inbox"


# --------------------------------------------------------------------------
# stdlib image header decoding (no Pillow; mirrors rawqc.py's approach)
# --------------------------------------------------------------------------


def decode_header(blob: bytes):
    """Return (format, width, height) from magic + header bytes, or raise."""
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        if blob[12:16] != b"IHDR":
            raise ValueError("PNG without a leading IHDR chunk")
        width, height = struct.unpack(">II", blob[16:24])
        return "PNG", width, height
    if blob[:4] == b"RIFF" and blob[8:12] == b"WEBP":
        return ("WEBP",) + _webp_size(blob)
    if blob[:2] == b"\xff\xd8":
        return ("JPEG",) + _jpeg_size(blob)
    if blob[:6] in (b"GIF87a", b"GIF89a"):
        width, height = struct.unpack("<HH", blob[6:10])
        return "GIF", width, height
    raise ValueError("unrecognised image format (not PNG/WEBP/JPEG/GIF)")


def _webp_size(blob: bytes):
    chunk = blob[12:16]
    if chunk == b"VP8X":
        width = int.from_bytes(blob[24:27], "little") + 1
        height = int.from_bytes(blob[27:30], "little") + 1
        return width, height
    if chunk == b"VP8 ":
        if blob[23:26] != b"\x9d\x01\x2a":
            raise ValueError("VP8 chunk without a keyframe start code")
        width, height = struct.unpack("<HH", blob[26:30])
        return width & 0x3FFF, height & 0x3FFF
    if chunk == b"VP8L":
        if blob[20] != 0x2F:
            raise ValueError("VP8L chunk without its signature byte")
        bits = int.from_bytes(blob[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    raise ValueError(f"unsupported WEBP chunk {chunk!r}")


def _jpeg_size(blob: bytes):
    i = 2
    end = len(blob)
    while i + 9 < end:
        if blob[i] != 0xFF:
            i += 1
            continue
        marker = blob[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        length = struct.unpack(">H", blob[i + 2 : i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height, width = struct.unpack(">HH", blob[i + 5 : i + 9])
            return width, height
        i += 2 + length
    raise ValueError("JPEG without a SOF frame header")


def png_bytes(width: int, height: int) -> bytes:
    """Minimal valid 8-bit RGB PNG. Used only by the selftest fixtures."""

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = b"".join(b"\x00" + bytes(3 * width) for _ in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


# --------------------------------------------------------------------------
# capture provenance - the shared fail-closed path for verify and materialize
# --------------------------------------------------------------------------


class ProvenanceError(Exception):
    """The pack could not be proven to come from the approved committed capture."""


def repo_relative(repo_root: Path, candidate) -> str:
    """Resolve `candidate` to a path inside repo_root, or refuse.

    `repo_root / absolute` silently discards repo_root, so an absolute or
    traversing --result would escape the repository. Refuse instead.
    """
    text = str(candidate)
    path = Path(text)
    if path.is_absolute():
        try:
            rel = path.resolve().relative_to(repo_root.resolve())
        except ValueError:
            raise ProvenanceError(
                f"{text} is outside the repository. The source result must be a committed "
                f"file under {repo_root}."
            )
        return rel.as_posix()
    if ".." in path.parts:
        raise ProvenanceError(f"{text} traverses out of the repository with '..'")
    return path.as_posix()


def find_capture_result(repo_root: Path, manifest: str) -> str:
    """The single committed successful result for `manifest`, or fail closed."""
    inbox = repo_root / HARVEST_INBOX
    if not inbox.is_dir():
        raise ProvenanceError(f"{HARVEST_INBOX}/ not found under {repo_root}")
    hits = []
    for path in sorted(inbox.glob("*.json")):
        try:
            with path.open(encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            continue
        journal = data.get("journal") or {}
        if journal.get("manifestPath") != manifest:
            continue
        if data.get("state") != "DONE" or data.get("outcome") != "success":
            continue
        hits.append(path.relative_to(repo_root).as_posix())
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise ProvenanceError(
            f"no successful committed result in {HARVEST_INBOX}/ has "
            f"journal.manifestPath == {manifest!r}"
        )
    raise ProvenanceError(
        f"{len(hits)} successful committed results claim manifest {manifest!r}: "
        f"{', '.join(hits)}. Exactly one is required; resolve the ambiguity rather "
        "than picking one."
    )


def resolve_capture_result(repo_root: Path, index: dict, override=None, approved=APPROVED_CAPTURE) -> str:
    """Repository-relative path of the result this pack must be proven against."""
    manifest = (index.get("source_capture") or {}).get("manifest")
    if manifest != approved["manifest"]:
        raise ProvenanceError(
            f"index source_capture.manifest is {manifest!r}; the approved v1 capture is "
            f"{approved['manifest']!r}"
        )
    if override is not None:
        rel = repo_relative(repo_root, override)
        if not (repo_root / rel).is_file():
            raise ProvenanceError(f"{rel} is not a file in the repository")
        return rel
    return find_capture_result(repo_root, manifest)


def load_capture_result(repo_root: Path, rel: str) -> dict:
    try:
        with (repo_root / rel).open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise ProvenanceError(f"source capture result not found: {rel}")
    except json.JSONDecodeError as exc:
        raise ProvenanceError(f"source capture result is not valid JSON: {rel}: {exc}")


def validate_capture_result(
    index: dict, result: dict, rel: str, approved=APPROVED_CAPTURE
) -> tuple[dict, list[str]]:
    """Prove `result` is the approved read-only capture for this index.

    Returns (by_id, errors). by_id maps asset id -> (capture, record). It is only
    safe to use when errors is empty.
    """
    errors: list[str] = []
    declared = index.get("source_capture") or {}

    def bad(msg: str) -> None:
        errors.append(f"{rel}: {msg}")

    if declared.get("manifest") != approved["manifest"]:
        bad(
            f"index source_capture.manifest is {declared.get('manifest')!r}; the approved "
            f"v1 capture is {approved['manifest']!r}"
        )

    if result.get("state") != "DONE":
        bad(f"result state is {result.get('state')!r}, expected 'DONE'")
    if result.get("outcome") != "success":
        bad(f"result outcome is {result.get('outcome')!r}, expected 'success'")

    journal = result.get("journal")
    if not isinstance(journal, dict):
        bad("result carries no journal; provenance cannot be established")
        return {}, errors

    if journal.get("manifestPath") != approved["manifest"]:
        bad(
            f"journal.manifestPath is {journal.get('manifestPath')!r}, expected "
            f"{approved['manifest']!r}"
        )
    if journal.get("state") not in (None, "DONE"):
        bad(f"journal.state is {journal.get('state')!r}, expected 'DONE'")

    for field, declared_key in (("jobId", "job_id"), ("manifestHash", "manifest_hash")):
        want = declared.get(declared_key)
        if want and journal.get(field) != want:
            bad(
                f"journal.{field} is {journal.get(field)!r} but the index records "
                f"{declared_key} {want!r}"
            )

    items = journal.get("items")
    if items is None:
        bad("journal carries no items array; zero mutations cannot be proven")
    elif items:
        bad(f"journal carries {len(items)} mutation item(s); this must be a read-only capture")
    if declared.get("mutations") not in (0, None):
        bad("index source_capture.mutations must be 0: this is a read-only capture")

    captures = result.get("captures")
    if not isinstance(captures, list):
        bad("result carries no captures array")
        return {}, errors

    refs_by_id: dict[str, dict] = {}
    for ref in index.get("references", []):
        asset_id = ref.get("asset_id")
        if isinstance(asset_id, str) and asset_id:
            refs_by_id[asset_id] = ref

    expected_reads = approved["reads"]
    if len(captures) != expected_reads:
        bad(
            f"expected exactly {expected_reads} captures, found {len(captures)}. "
            "An extra or missing capture makes the reference set ambiguous."
        )
    if len(refs_by_id) != expected_reads:
        bad(f"index carries {len(refs_by_id)} distinct asset ids, expected {expected_reads}")
    if declared.get("reads") not in (None, expected_reads):
        bad(f"index source_capture.reads is {declared.get('reads')!r}, expected {expected_reads}")

    by_id: dict[str, tuple[dict, dict]] = {}
    seen: dict[str, int] = {}
    for position, cap in enumerate(captures):
        label = f"capture[{position}]"
        if not isinstance(cap, dict):
            bad(f"{label} is not an object")
            continue
        if cap.get("proc") != EXPECTED_CAPTURE_PROC:
            bad(f"{label}: proc is {cap.get('proc')!r}, expected {EXPECTED_CAPTURE_PROC!r}")
            continue
        record = cap.get("data") or {}
        asset_id = record.get("id")
        if not asset_id:
            bad(f"{label}: captured record carries no id")
            continue
        if asset_id in seen:
            bad(f"{label}: duplicate capture of {asset_id} (also at capture[{seen[asset_id]}])")
            continue
        seen[asset_id] = position
        if asset_id not in refs_by_id:
            bad(
                f"{label}: captured asset {asset_id} is not in the reference index. "
                "An unexpected capture makes the reference set ambiguous."
            )
            continue

        ref = refs_by_id[asset_id]
        key = ref.get("key", asset_id)
        if cap.get("ok") is not True:
            bad(f"{key}: capture ok is {cap.get('ok')!r}, expected True")
        if cap.get("rows") != 1:
            bad(f"{key}: capture rows is {cap.get('rows')!r}, expected 1")
        if cap.get("persist") != "full":
            bad(f"{key}: capture persist is {cap.get('persist')!r}, expected 'full'")
        if cap.get("persistOk") is not True:
            bad(f"{key}: capture persistOk is {cap.get('persistOk')!r}, expected True")
        if record.get("type") != ref.get("target"):
            bad(
                f"{key}: captured type {record.get('type')!r} != index target "
                f"{ref.get('target')!r}"
            )
        if record.get("name") != ref.get("name"):
            bad(f"{key}: captured name {record.get('name')!r} != index name {ref.get('name')!r}")
        if not record.get("image"):
            bad(f"{key}: captured record carries no image URL")
        by_id[asset_id] = (cap, record)

    for asset_id, ref in sorted(refs_by_id.items()):
        if asset_id not in seen:
            bad(f"{ref.get('key', asset_id)}: expected asset {asset_id} is absent from the capture")

    return by_id, errors


def check_reference_provenance(index: dict, by_id: dict, rel: str) -> list[str]:
    """Each reference's recorded source fields must match the committed capture."""
    errors: list[str] = []
    for ref in index.get("references", []):
        key = ref.get("key", "?")
        entry = by_id.get(ref.get("asset_id"))
        if entry is None:
            continue  # already reported by validate_capture_result
        cap, record = entry
        if ref.get("source_capture") != rel:
            errors.append(
                f"{key}: source_capture is {ref.get('source_capture')!r} but provenance was "
                f"proven against {rel!r}"
            )
        if ref.get("source_image_url") != record.get("image"):
            errors.append(
                f"{key}: source_image_url does not match the captured image URL for "
                f"{ref.get('asset_id')}"
            )
        if cap.get("snapshotKey") and ref.get("source_snapshot_key") != cap.get("snapshotKey"):
            errors.append(
                f"{key}: source_snapshot_key is {ref.get('source_snapshot_key')!r}, capture "
                f"records {cap.get('snapshotKey')!r}"
            )
    return errors


# --------------------------------------------------------------------------
# index loading / path resolution
# --------------------------------------------------------------------------

SCRIPT = Path(__file__).resolve()
SKILL_ROOT = SCRIPT.parents[1]


def default_index_path() -> Path:
    """Works identically from the repo tree and from an installed skill ZIP."""
    packaged = SKILL_ROOT / "data" / "style_refs.json"
    if packaged.exists():
        return packaged
    return Path.cwd() / "style_refs.json"


def default_repo_root() -> Path:
    guess = SCRIPT.parents[3]
    if (guess / "art" / "style_refs").is_dir():
        return guess
    return Path.cwd()


def load_index(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"style_refs: index not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"style_refs: index is not valid JSON: {path}: {exc}")


def raw_url(index: dict, ref: dict, git_ref: str | None = None) -> str:
    template = index.get("raw_url_template") or (
        "https://raw.githubusercontent.com/perseverance484/tnr-tools/{ref}/{path}"
    )
    return template.format(
        ref=git_ref or index.get("raw_url_default_ref", "main"), path=ref["path"]
    )


# --------------------------------------------------------------------------
# verify
# --------------------------------------------------------------------------


def verify(
    index: dict,
    repo_root: Path,
    check_bytes: bool = True,
    check_provenance: bool = True,
    result_override=None,
    approved=APPROVED_CAPTURE,
) -> list[str]:
    """Return a list of human-readable errors. Empty list means the pack is sound.

    Byte-level integrity alone is not enough: a pack can hash perfectly and still
    be severed from the approved capture. When check_provenance is on, the same
    fail-closed result validation materialize uses runs here too, and every
    reference's recorded source fields are cross-checked against that committed
    result rather than trusted.
    """
    errors: list[str] = []

    def bad(msg: str) -> None:
        errors.append(msg)

    if index.get("schema") != SCHEMA:
        bad(f"schema must be {SCHEMA!r}, found {index.get('schema')!r}")
    if index.get("version") != VERSION:
        bad(f"version must be {VERSION}, found {index.get('version')!r}")

    capture = index.get("source_capture")
    if not isinstance(capture, dict):
        bad("source_capture block is missing")
        check_provenance = False
    else:
        for field in ("manifest", "result", "job_id"):
            if not capture.get(field):
                bad(f"source_capture.{field} is missing")

    refs = index.get("references")
    if not isinstance(refs, list) or not refs:
        bad("references must be a non-empty array")
        return errors

    banned = {
        str(entry.get("name", "")).strip().lower()
        for entry in index.get("excluded", [])
        if isinstance(entry, dict)
    }

    seen_keys: dict[str, int] = {}
    seen_ids: dict[str, str] = {}
    seen_paths: dict[str, str] = {}

    for position, ref in enumerate(refs):
        if not isinstance(ref, dict):
            bad(f"references[{position}] is not an object")
            continue
        key = ref.get("key")
        label = key or f"references[{position}]"

        for field in (
            "key",
            "name",
            "asset_id",
            "target",
            "priority",
            "order",
            "path",
            "source_image_url",
            "source_capture",
            "sha256",
            "width",
            "height",
            "format",
            "use_for",
        ):
            if ref.get(field) in (None, ""):
                bad(f"{label}: required field {field!r} is missing")

        if not isinstance(key, str) or not key:
            continue
        if key in seen_keys:
            bad(f"{label}: duplicate reference key (also at index {seen_keys[key]})")
        seen_keys[key] = position

        asset_id = ref.get("asset_id")
        if isinstance(asset_id, str) and asset_id:
            if asset_id in seen_ids:
                bad(f"{label}: duplicate gameAsset id {asset_id} (also on {seen_ids[asset_id]})")
            seen_ids[asset_id] = key

        target = ref.get("target")
        if target not in TARGETS:
            bad(f"{label}: unsupported target {target!r}; v1 supports {', '.join(TARGETS)}")
            target = None

        if ref.get("priority") not in PRIORITIES:
            bad(f"{label}: priority must be one of {', '.join(PRIORITIES)}")
        if not isinstance(ref.get("order"), int):
            bad(f"{label}: order must be an integer")

        register = ref.get("register")
        if target == "SCENE_CHARACTER":
            if register not in REGISTERS:
                bad(f"{label}: scene-character register must be one of {', '.join(REGISTERS)}")
        elif register not in (None, ""):
            bad(f"{label}: register is only meaningful for SCENE_CHARACTER")

        if str(ref.get("name", "")).strip().lower() in banned:
            bad(f"{label}: {ref['name']!r} is on the excluded list and must not be a positive reference")

        rel = ref.get("path")
        if isinstance(rel, str) and rel:
            if rel.startswith("/") or (len(rel) > 1 and rel[1] == ":") or ".." in Path(rel).parts:
                bad(f"{label}: path must be a repository-relative path without '..': {rel!r}")
                rel = None
            elif rel in seen_paths:
                bad(f"{label}: duplicate local path {rel} (also on {seen_paths[rel]})")
            else:
                seen_paths[rel] = key
            if rel and target and not rel.startswith(TARGET_DIRS[target] + "/"):
                bad(f"{label}: {target} reference must live under {TARGET_DIRS[target]}/, found {rel}")
        else:
            rel = None

        if rel and check_bytes:
            local = repo_root / rel
            if not local.is_file():
                bad(f"{label}: reference file is missing: {rel}")
                continue
            blob = local.read_bytes()
            digest = hashlib.sha256(blob).hexdigest()
            if digest != ref.get("sha256"):
                bad(f"{label}: sha256 mismatch for {rel}: index {ref.get('sha256')}, file {digest}")
            if "bytes" in ref and ref["bytes"] != len(blob):
                bad(f"{label}: byte count mismatch for {rel}: index {ref['bytes']}, file {len(blob)}")
            try:
                fmt, width, height = decode_header(blob)
            except (ValueError, struct.error, IndexError) as exc:
                bad(f"{label}: cannot decode {rel}: {exc}")
                continue
            if fmt != ref.get("format"):
                bad(f"{label}: format mismatch for {rel}: index {ref.get('format')}, file {fmt}")
            if (width, height) != (ref.get("width"), ref.get("height")):
                bad(
                    f"{label}: dimension mismatch for {rel}: index "
                    f"{ref.get('width')}x{ref.get('height')}, file {width}x{height}"
                )
            expected_ext = EXT_FOR_FORMAT.get(fmt)
            if expected_ext and not rel.lower().endswith(expected_ext):
                bad(f"{label}: {rel} is decoded {fmt} but does not carry {expected_ext}")

    if check_provenance:
        try:
            rel = resolve_capture_result(repo_root, index, result_override, approved)
            result = load_capture_result(repo_root, rel)
        except ProvenanceError as exc:
            bad(f"provenance: {exc}")
        else:
            if result_override is None and index["source_capture"].get("result") != rel:
                bad(
                    f"provenance: index records result "
                    f"{index['source_capture'].get('result')!r} but the single successful "
                    f"committed result for {approved['manifest']} is {rel!r}"
                )
            by_id, capture_errors = validate_capture_result(index, result, rel, approved)
            for err in capture_errors:
                bad(f"provenance: {err}")
            if not capture_errors:
                for err in check_reference_provenance(index, by_id, rel):
                    bad(f"provenance: {err}")

    required = index.get("required")
    if not isinstance(required, dict) or not required:
        bad("required block is missing: verify cannot prove the v1 corpus is complete")
    else:
        for target, keys in sorted(required.items()):
            if target not in TARGETS:
                bad(f"required.{target}: unsupported target")
                continue
            for key in keys:
                if key not in seen_keys:
                    bad(f"required {target} reference {key!r} is absent from the pack")

    return errors


# --------------------------------------------------------------------------
# list / select
# --------------------------------------------------------------------------


def sort_key(ref: dict):
    return (PRIORITY_RANK.get(ref.get("priority"), len(PRIORITIES)), ref.get("order", 0), ref.get("key", ""))


def filter_refs(index: dict, target=None, register=None, tags=None, keys=None) -> list[dict]:
    out = []
    wanted_tags = {t.strip().lower() for t in (tags or []) if t.strip()}
    wanted_keys = {k.strip() for k in (keys or []) if k.strip()}
    for ref in index.get("references", []):
        if target and ref.get("target") != target:
            continue
        if register and ref.get("register") != register:
            continue
        if wanted_keys and ref.get("key") not in wanted_keys:
            continue
        if wanted_tags:
            have = {str(t).lower() for t in ref.get("tags", [])}
            if not (wanted_tags & have):
                continue
        out.append(ref)
    out.sort(key=sort_key)
    return out


def select(index: dict, target: str, register=None, tags=None, keys=None, limit=None) -> list[dict]:
    chosen = filter_refs(index, target=target, register=register, tags=tags, keys=keys)
    if limit is None:
        limit = DEFAULT_LIMIT.get(target, 4)
    if limit > 0:
        chosen = chosen[:limit]
    return chosen


def describe(ref: dict) -> str:
    bits = [ref.get("priority", "")]
    if ref.get("register"):
        bits.append(ref["register"])
    tags = ", ".join(str(t) for t in ref.get("tags", []))
    if tags:
        bits.append(tags)
    return " / ".join(b for b in bits if b)


def print_list(index: dict, refs: list[dict]) -> None:
    if not refs:
        print("(no references matched)")
        return
    for ref in refs:
        print(f"{ref['key']}  -  {ref['name']}")
        print(f"    {ref['target']}  {describe(ref)}")
        print(f"    {ref['width']}x{ref['height']} {ref['format']}  {ref.get('bytes', '?')} bytes")
        print(f"    path   {ref['path']}")
        print(f"    asset  {ref['asset_id']}")
        print(f"    use    {ref['use_for']}")
        if ref.get("do_not_use_for"):
            print(f"    LIMIT  {ref['do_not_use_for']}")
        print()


def print_select(index: dict, refs: list[dict], target: str, register, git_ref) -> None:
    header = f"TNR visual references - {target}"
    if register:
        header += f" / {register}"
    print(header)
    print("=" * len(header))
    print()
    print("References calibrate; 25x_DATA_art_spec.json governs.")
    print("Read the spec target + house_style FIRST, then open each image below and look at it.")
    print("Use the individual images as references, never a collage. Start a clean generation")
    print("context for a new asset class so a previous asset cannot contaminate this one.")
    print()
    if not refs:
        print("NO REFERENCES MATCHED - do not invent a substitute; widen the filter or")
        print("proceed from the art spec alone and say so.")
        return
    for position, ref in enumerate(refs, 1):
        print(f"{position}. {ref['name']}  [{describe(ref)}]")
        print(f"   path : {ref['path']}")
        print(f"   raw  : {raw_url(index, ref, git_ref)}")
        print(f"   size : {ref['width']}x{ref['height']} {ref['format']}")
        print(f"   note : {ref['use_for']}")
        if ref.get("do_not_use_for"):
            print(f"   LIMIT: {ref['do_not_use_for']}")
        print()
    print("Inspect every image above before composing the prompt. A URL in a prompt is not")
    print("evidence that a generator ingested the pixels.")


# --------------------------------------------------------------------------
# materialize (maintainer path - the only networked command)
# --------------------------------------------------------------------------


def materialize(index_path: Path, repo_root: Path, result_path: Path | None) -> int:
    import urllib.request

    index = load_index(index_path)

    # Prove the source capture BEFORE any download. Nothing is fetched or written
    # until the result is shown to be the single successful committed read-only
    # capture for the approved manifest, with all 18 expected full-body records.
    try:
        capture_rel = resolve_capture_result(repo_root, index, result_path)
        result = load_capture_result(repo_root, capture_rel)
    except ProvenanceError as exc:
        raise SystemExit(f"materialize: provenance: {exc}")

    by_id, capture_errors = validate_capture_result(index, result, capture_rel)
    if capture_errors:
        print(
            f"materialize: refusing to materialize from {capture_rel}: "
            f"{len(capture_errors)} provenance error(s)",
            file=sys.stderr,
        )
        for err in capture_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"provenance OK: {capture_rel} ({len(by_id)} approved captures)\n")

    changed = 0
    for ref in index["references"]:
        asset_id = ref["asset_id"]
        cap, data = by_id[asset_id]
        url = data["image"]

        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            blob = response.read()
        if not blob:
            raise SystemExit(f"materialize: {ref['key']}: empty download from {url}")
        fmt, width, height = decode_header(blob)
        try:
            from PIL import Image  # optional cross-check only
            import io

            with Image.open(io.BytesIO(blob)) as im:
                if im.format != fmt or im.size != (width, height):
                    raise SystemExit(
                        f"materialize: {ref['key']}: Pillow reads {im.format} {im.size}, "
                        f"header reads {fmt} {width}x{height}"
                    )
        except ImportError:
            pass

        ext = EXT_FOR_FORMAT.get(fmt)
        if not ext:
            raise SystemExit(f"materialize: {ref['key']}: unsupported decoded format {fmt}")
        rel = f"{TARGET_DIRS[ref['target']]}/{ref['key']}{ext}"
        out = repo_root / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(blob)  # exact downloaded bytes, no transcode

        ref.update(
            {
                "path": rel,
                "source_image_url": url,
                "source_capture": capture_rel,
                "source_snapshot_key": cap.get("snapshotKey"),
                "sha256": hashlib.sha256(blob).hexdigest(),
                "bytes": len(blob),
                "width": width,
                "height": height,
                "format": fmt,
            }
        )
        changed += 1
        print(f"{ref['key']:<26} {fmt:<5} {width}x{height:<6} {len(blob):>7} bytes  {rel}")

    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(ref["bytes"] for ref in index["references"])
    print(f"\n{changed} references materialized, {total} bytes total, index rewritten: {index_path}")
    return 0


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------


FIXTURE_APPROVED = {"manifest": APPROVED_CAPTURE["manifest"], "reads": 3}


def _fixture_result(index: dict, rel: str) -> dict:
    """A well-formed read-only capture result matching the fixture index."""
    captures = []
    for position, ref in enumerate(index["references"]):
        captures.append(
            {
                "phase": "after",
                "proc": EXPECTED_CAPTURE_PROC,
                "input": {"id": ref["asset_id"]},
                "ok": True,
                "rows": 1,
                "error": None,
                "persist": "full",
                "snapshotKey": ref["source_snapshot_key"],
                "persistOk": True,
                "data": {
                    "id": ref["asset_id"],
                    "name": ref["name"],
                    "type": ref["target"],
                    "image": ref["source_image_url"],
                },
            }
        )
    return {
        "state": "DONE",
        "outcome": "success",
        "journal": {
            "v": 1,
            "jobId": index["source_capture"]["job_id"],
            "manifestPath": index["source_capture"]["manifest"],
            "manifestHash": index["source_capture"]["manifest_hash"],
            "state": "DONE",
            "items": [],
        },
        "captures": captures,
    }


def _write_result(repo: Path, rel: str, result: dict) -> None:
    target = repo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result), encoding="utf-8")


def _fixture(tmp: Path):
    """A three-reference pack plus its committed capture. Returns (index, repo_root)."""
    repo = tmp / "repo"
    for target_dir in TARGET_DIRS.values():
        (repo / target_dir).mkdir(parents=True, exist_ok=True)

    def write(target, key, width, height):
        rel = f"{TARGET_DIRS[target]}/{key}.png"
        blob = png_bytes(width, height)
        (repo / rel).write_bytes(blob)
        return rel, blob

    rel_a, blob_a = write("SCENE_CHARACTER", "anchor", 8, 8)
    rel_b, blob_b = write("SCENE_CHARACTER", "second", 6, 9)
    rel_c, blob_c = write("SCENE_BACKGROUND", "yard", 12, 8)

    def entry(key, name, asset, target, register, priority, order, rel, blob, tags):
        return {
            "key": key,
            "name": name,
            "asset_id": asset,
            "target": target,
            "register": register,
            "tags": tags,
            "priority": priority,
            "order": order,
            "path": rel,
            "source_image_url": f"https://example.invalid/{key}",
            "source_capture": "harvests/inbox/fixture_result.json",
            "source_snapshot_key": f"fix-job::after::{order}",
            "sha256": hashlib.sha256(blob).hexdigest(),
            "bytes": len(blob),
            "width": decode_header(blob)[1],
            "height": decode_header(blob)[2],
            "format": "PNG",
            "use_for": "fixture",
        }

    index = {
        "schema": SCHEMA,
        "version": VERSION,
        "source_capture": {
            "manifest": FIXTURE_APPROVED["manifest"],
            "result": "harvests/inbox/fixture_result.json",
            "job_id": "fix-job",
            "manifest_hash": "fixhash",
            "reads": 3,
            "mutations": 0,
        },
        "excluded": [{"name": "Nameless Ninja", "reason": "deprecated"}],
        "required": {"SCENE_CHARACTER": ["anchor", "second"], "SCENE_BACKGROUND": ["yard"]},
        "references": [
            entry("anchor", "Anchor", "id-a", "SCENE_CHARACTER", "NINJA", "PRIMARY", 10, rel_a, blob_a, ["bust"]),
            entry("second", "Second", "id-b", "SCENE_CHARACTER", "NINJA", "SUPPORTING", 20, rel_b, blob_b, ["full-body"]),
            entry("yard", "Yard", "id-c", "SCENE_BACKGROUND", None, "PRIMARY", 10, rel_c, blob_c, ["yard"]),
        ],
    }
    _write_result(repo, index["source_capture"]["result"], _fixture_result(index, index["source_capture"]["result"]))
    return index, repo


def selftest() -> int:
    import copy
    import tempfile

    failures: list[str] = []

    def want(condition: bool, label: str) -> None:
        print(("  ok   " if condition else "  FAIL ") + label)
        if not condition:
            failures.append(label)

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        base, repo = _fixture(tmp)

        def check(index, override=None):
            return verify(index, repo, result_override=override, approved=FIXTURE_APPROVED)

        print("parsing and a clean pack")
        want(check(base) == [], "a well-formed pack verifies with zero errors")
        fmt, width, height = decode_header(png_bytes(13, 7))
        want((fmt, width, height) == ("PNG", 13, 7), "stdlib PNG header decode returns format and size")

        print("\nhash and dimension tampering")
        bad = copy.deepcopy(base)
        bad["references"][0]["sha256"] = "0" * 64
        errs = check(bad)
        want(any("sha256 mismatch" in e for e in errs), "a wrong sha256 is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["width"] = 999
        errs = check(bad)
        want(any("dimension mismatch" in e for e in errs), "wrong indexed dimensions are rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["format"] = "WEBP"
        errs = check(bad)
        want(any("format mismatch" in e for e in errs), "a wrong decoded format is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["bytes"] = 1
        want(any("byte count mismatch" in e for e in check(bad)), "a wrong byte count is rejected")

        print("\nstructural rejection")
        bad = copy.deepcopy(base)
        bad["references"][1]["key"] = "anchor"
        want(any("duplicate reference key" in e for e in check(bad)), "duplicate keys are rejected")

        bad = copy.deepcopy(base)
        bad["references"][1]["asset_id"] = "id-a"
        want(any("duplicate gameAsset id" in e for e in check(bad)), "duplicate asset ids are rejected")

        bad = copy.deepcopy(base)
        bad["references"].pop(0)
        want(any("required" in e and "anchor" in e for e in check(bad)), "a missing required reference is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["path"] = TARGET_DIRS["SCENE_CHARACTER"] + "/gone.png"
        want(any("is missing" in e for e in check(bad)), "a missing local file is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["target"] = "AI_AVATAR"
        want(any("unsupported target" in e for e in check(bad)), "an unsupported target is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["register"] = "SAMURAI"
        want(any("register must be" in e for e in check(bad)), "an unsupported register is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["path"] = "/etc/passwd.png"
        want(any("repository-relative" in e for e in check(bad)), "an absolute path is rejected")

        bad = copy.deepcopy(base)
        bad["references"][2]["path"] = base["references"][0]["path"]
        want(any("must live under" in e for e in check(bad)), "a reference filed under the wrong target dir is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["name"] = "Nameless Ninja"
        want(any("excluded list" in e for e in check(bad)), "an excluded/deprecated asset is rejected")

        bad = copy.deepcopy(base)
        bad["version"] = 99
        want(any("version must be" in e for e in check(bad)), "a wrong schema version is rejected")

        bad = copy.deepcopy(base)
        bad["source_capture"]["mutations"] = 3
        want(any("read-only capture" in e for e in check(bad)), "a capture claiming mutations is rejected")

        print("\nprovenance - the source capture must prove itself")
        rel = base["source_capture"]["result"]
        good = _fixture_result(base, rel)

        def with_result(mutate, index=None):
            """Rewrite the committed result, verify, then restore it."""
            import copy as _copy

            broken = _copy.deepcopy(good)
            mutate(broken)
            _write_result(repo, rel, broken)
            try:
                return check(index if index is not None else base)
            finally:
                _write_result(repo, rel, good)

        def with_result_override(mutate):
            """Same, but name the file explicitly through --result."""
            import copy as _copy

            broken = _copy.deepcopy(good)
            mutate(broken)
            _write_result(repo, rel, broken)
            try:
                return check(base, override=Path(rel))
            finally:
                _write_result(repo, rel, good)

        def wrong_manifest(r):
            r["journal"]["manifestPath"] = "push/99_something_else.json"

        want(any("journal.manifestPath" in e for e in with_result(wrong_manifest)),
             "a result whose journal names a different manifest is rejected")
        # The default resolver skips a non-DONE/non-success result entirely, so the
        # normal path fails closed as "nothing suitable". The explicit --result
        # override names the file directly and must still be refused on its state:
        # the override may never weaken the approved-capture contract.
        want(any("no successful committed result" in e for e in
                 with_result(lambda r: r.__setitem__("state", "PAUSED"))),
             "the default path fails closed when the only candidate is not DONE")
        want(any("result state is" in e for e in
                 with_result_override(lambda r: r.__setitem__("state", "PAUSED"))),
             "a non-DONE result named by --result is still rejected")
        want(any("no successful committed result" in e for e in
                 with_result(lambda r: r.__setitem__("outcome", "error"))),
             "the default path fails closed when the only candidate did not succeed")
        want(any("result outcome is" in e for e in
                 with_result_override(lambda r: r.__setitem__("outcome", "error"))),
             "a non-success result named by --result is still rejected")
        want(any("mutation item" in e for e in
                 with_result(lambda r: r["journal"].__setitem__("items", [{"proc": "gameAsset.create"}]))),
             "a result carrying journal mutation items is rejected")
        want(any("journal.jobId" in e for e in
                 with_result(lambda r: r["journal"].__setitem__("jobId", "someone-elses-job"))),
             "a jobId disagreeing with the indexed provenance is rejected")
        want(any("journal.manifestHash" in e for e in
                 with_result(lambda r: r["journal"].__setitem__("manifestHash", "deadbeef"))),
             "a manifest hash disagreeing with the indexed provenance is rejected")
        want(any("absent from the capture" in e for e in with_result(lambda r: r["captures"].pop(0))),
             "a missing expected capture is rejected")

        def duplicate(r):
            import copy as _copy
            r["captures"][1] = _copy.deepcopy(r["captures"][0])

        errs = with_result(duplicate)
        want(any("duplicate capture" in e for e in errs), "a duplicated expected capture is rejected")

        def extra(r):
            import copy as _copy
            stray = _copy.deepcopy(r["captures"][0])
            stray["data"]["id"] = "not-in-the-index"
            r["captures"].append(stray)

        errs = with_result(extra)
        want(any("ambiguous" in e for e in errs),
             "an unexpected extra capture is rejected as ambiguous")
        want(any("persist is" in e for e in
                 with_result(lambda r: r["captures"][0].__setitem__("persist", "summary"))),
             "a capture that is not persist:full is rejected")
        want(any("persistOk is" in e for e in
                 with_result(lambda r: r["captures"][0].__setitem__("persistOk", False))),
             "a capture whose body failed to persist is rejected")
        want(any("ok is" in e for e in
                 with_result(lambda r: r["captures"][0].__setitem__("ok", False))),
             "a failed capture is rejected")
        want(any("rows is" in e for e in
                 with_result(lambda r: r["captures"][0].__setitem__("rows", 0))),
             "a capture returning no row is rejected")
        want(any("captured name" in e for e in
                 with_result(lambda r: r["captures"][0]["data"].__setitem__("name", "Someone Else"))),
             "a capture whose record name disagrees with the index is rejected")
        want(any("captured type" in e for e in
                 with_result(lambda r: r["captures"][0]["data"].__setitem__("type", "SCENE_BACKGROUND"))),
             "a capture whose record type disagrees with the index is rejected")
        want(any("image URL" in e or "source_image_url" in e for e in
                 with_result(lambda r: r["captures"][0]["data"].__setitem__("image", ""))),
             "a capture carrying no image URL is rejected")
        want(any("source_image_url" in e for e in
                 with_result(lambda r: r["captures"][0]["data"].__setitem__(
                     "image", "https://example.invalid/somewhere-else"))),
             "a reference whose recorded source URL is not the captured one is rejected")

        bad = copy.deepcopy(base)
        bad["source_capture"]["manifest"] = "push/99_not_approved.json"
        want(any("approved v1 capture" in e for e in check(bad)),
             "an index pointing at a manifest that is not the approved capture is rejected")

        bad = copy.deepcopy(base)
        bad["source_capture"]["result"] = "harvests/inbox/some_other_result.json"
        want(any("single successful committed result" in e for e in check(bad)),
             "an index whose recorded result is not the resolved one is rejected")

        bad = copy.deepcopy(base)
        bad["references"][0]["source_snapshot_key"] = "fix-job::after::99"
        want(any("source_snapshot_key" in e for e in check(bad)),
             "a reference whose snapshot key disagrees with the capture is rejected")

        outside = tmp / "outside_result.json"
        outside.write_text(json.dumps(good), encoding="utf-8")
        want(any("outside the repository" in e for e in check(base, override=outside)),
             "an absolute --result outside the repository is refused")
        want(any("traverses out of the repository" in e for e in
                 check(base, override=Path("../escape.json"))),
             "a traversing --result is refused")
        want(check(base, override=Path(rel)) == [],
             "a repository-relative --result naming the approved result is accepted")

        strays = repo / HARVEST_INBOX / "second_success.json"
        strays.write_text(json.dumps(good), encoding="utf-8")
        want(any("Exactly one is required" in e for e in check(base)),
             "two successful results for the same manifest fail closed as ambiguous")
        strays.unlink()
        want(check(base) == [], "removing the ambiguity restores a clean verify")

        missing = repo / HARVEST_INBOX / "fixture_result.json"
        moved = missing.read_bytes()
        missing.unlink()
        want(any("no successful committed result" in e for e in check(base)),
             "no matching committed result fails closed")
        missing.write_bytes(moved)

        print("\nselection")
        chars = select(base, "SCENE_CHARACTER")
        want([r["key"] for r in chars] == ["anchor", "second"], "PRIMARY sorts ahead of SUPPORTING")
        want(select(base, "SCENE_CHARACTER") == select(base, "SCENE_CHARACTER"), "selection is stable across calls")
        shuffled = copy.deepcopy(base)
        shuffled["references"] = list(reversed(shuffled["references"]))
        want(
            [r["key"] for r in select(shuffled, "SCENE_CHARACTER")] == ["anchor", "second"],
            "selection order is independent of index order",
        )
        want([r["key"] for r in select(base, "SCENE_BACKGROUND")] == ["yard"], "background selection ignores characters")
        want(len(select(base, "SCENE_CHARACTER", limit=1)) == 1, "--limit truncates deterministically")
        want([r["key"] for r in select(base, "SCENE_CHARACTER", tags=["full-body"])] == ["second"], "tag filtering works")
        want(select(base, "SCENE_CHARACTER", register="CIVILIAN") == [], "an empty register selects nothing rather than substituting")
        want(
            raw_url(base, base["references"][0], "abc123").endswith("abc123/" + base["references"][0]["path"]),
            "raw URLs are emitted for checkout-free callers",
        )

    print()
    if failures:
        print(f"{len(failures)} FAILED")
        for label in failures:
            print(f"  - {label}")
        return 1
    print("style_refs selftest: all checks passed")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true", help="run socket-free unit tests and exit")
    parser.add_argument("--index", type=Path, help="path to style_refs.json")
    sub = parser.add_subparsers(dest="command")

    p_verify = sub.add_parser("verify", help="audit the checked-in pack (needs a repo checkout)")
    p_verify.add_argument("--repo-root", type=Path, default=None)
    p_verify.add_argument(
        "--result",
        type=Path,
        default=None,
        help="committed result to prove provenance against; must resolve inside the repository. "
        "Default: the single successful committed result for the approved manifest.",
    )

    p_list = sub.add_parser("list", help="list references and metadata")
    p_list.add_argument("--target", choices=TARGETS)
    p_list.add_argument("--register", choices=REGISTERS)
    p_list.add_argument("--tag", action="append", default=[])
    p_list.add_argument("--json", action="store_true")

    p_select = sub.add_parser("select", help="pick the deterministic reference set for one target")
    p_select.add_argument("--target", choices=TARGETS, required=True)
    p_select.add_argument("--register", choices=REGISTERS)
    p_select.add_argument("--tag", action="append", default=[])
    p_select.add_argument("--key", action="append", default=[])
    p_select.add_argument("--limit", type=int, default=None)
    p_select.add_argument("--ref", default=None, help="git ref for emitted raw URLs (default: main)")
    p_select.add_argument("--json", action="store_true")

    p_mat = sub.add_parser("materialize", help="MAINTAINER: re-download bytes from captured image URLs")
    p_mat.add_argument("--repo-root", type=Path, default=None)
    p_mat.add_argument(
        "--result",
        type=Path,
        default=None,
        help="committed result to materialize from; must resolve inside the repository and "
        "still pass every provenance invariant.",
    )

    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.command:
        parser.print_help()
        return 2

    index_path = args.index or default_index_path()

    if args.command == "materialize":
        return materialize(index_path, args.repo_root or default_repo_root(), args.result)

    index = load_index(index_path)

    if args.command == "verify":
        repo_root = args.repo_root or default_repo_root()
        errors = verify(index, repo_root, result_override=args.result)
        if errors:
            print(f"style_refs verify: {len(errors)} error(s) against {repo_root}", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1
        total = sum(ref.get("bytes", 0) for ref in index["references"])
        counts = {}
        for ref in index["references"]:
            counts[ref["target"]] = counts.get(ref["target"], 0) + 1
        summary = ", ".join(f"{n} {t}" for t, n in sorted(counts.items()))
        print(f"style_refs verify: OK - {len(index['references'])} references ({summary}), {total} bytes")
        print(f"  manifest:   {APPROVED_CAPTURE_MANIFEST}")
        print(f"  capture:    {index['source_capture']['result']}")
        print(f"  provenance: {EXPECTED_CAPTURE_COUNT}/{EXPECTED_CAPTURE_COUNT} approved captures proven, 0 mutations")
        return 0

    if args.command == "list":
        refs = filter_refs(index, target=args.target, register=args.register, tags=args.tag)
        if args.json:
            json.dump(refs, sys.stdout, indent=2, ensure_ascii=False)
            print()
        else:
            print_list(index, refs)
        return 0

    if args.command == "select":
        refs = select(
            index,
            target=args.target,
            register=args.register,
            tags=args.tag,
            keys=args.key,
            limit=args.limit,
        )
        if args.json:
            payload = {
                "target": args.target,
                "register": args.register,
                "authority": index.get("authority_note"),
                "references": [
                    {
                        "key": r["key"],
                        "name": r["name"],
                        "path": r["path"],
                        "raw_url": raw_url(index, r, args.ref),
                        "width": r["width"],
                        "height": r["height"],
                        "format": r["format"],
                        "priority": r["priority"],
                        "register": r.get("register"),
                        "tags": r.get("tags", []),
                        "use_for": r["use_for"],
                        "do_not_use_for": r.get("do_not_use_for"),
                    }
                    for r in refs
                ],
            }
            json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
            print()
        else:
            print_select(index, refs, args.target, args.register, args.ref)
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
