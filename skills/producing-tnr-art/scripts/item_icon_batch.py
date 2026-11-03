#!/usr/bin/env python3
"""Offline item-icon wave roster and deterministic contact-sheet builder.

Only committed/user-supplied full item records are inputs. Never requests the game
or asset CDNs, never guesses item icon URLs from gameAsset art-index data.
Run from repository root. Pillow is required only by the sheet command.
"""
import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

CSV_FIELDS = ("role", "id", "name", "status", "captured_name", "item_type",
              "rarity", "slot", "image_url", "captured_at", "source_file", "snapshot_key")


def capture_timestamp_key(value):
    """Chronology key for ISO-8601 and Unix seconds/milliseconds.

    Missing timestamps sort before known timestamps. Keep the original time
    in the roster; this comparable key is only used to select provenance.
    Invalid nonempty values fail rather than silently picking a wrong source.
    """
    if value is None or value == "":
        return (0, 0.0)
    if isinstance(value, bool):
        raise ValueError(f"invalid capture timestamp: {value!r}")
    if isinstance(value, (int, float)):
        seconds = float(value)
    elif isinstance(value, str):
        value = value.strip()
        if not value:
            return (0, 0.0)
        try:
            seconds = float(value)
        except ValueError:
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"invalid capture timestamp: {value!r}") from exc
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            seconds = parsed.timestamp()
    else:
        raise ValueError(f"invalid capture timestamp: {value!r}")
    if not math.isfinite(seconds):
        raise ValueError(f"invalid capture timestamp: {value!r}")
    if abs(seconds) >= 1e11:  # Modern Unix milliseconds, not seconds.
        seconds /= 1000.0
    return (1, seconds)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def capture_records(path):
    """Yield (record, provenance) from supported *full-record* offline evidence."""
    obj = read_json(path)
    if isinstance(obj, dict) and "assets" in obj and "counts" in obj:
        raise ValueError(f"{path}: gameAsset art index is not an item-icon census")
    provenance = {"source_file": str(path), "source_sha256": digest(path)}
    if isinstance(obj, dict) and "captures" in obj:
        if obj.get("cfg") == "forge" and (
                obj.get("outcome") != "success" or obj.get("state") != "DONE"):
            raise ValueError(f"{path}: Forge bundle is not DONE/success")
        for c in obj["captures"]:
            if not isinstance(c, dict) or c.get("proc") != "item.get":
                continue
            d, inp = c.get("data"), c.get("input") or {}
            if (c.get("ok") is not True or c.get("persistOk") is False or
                    not isinstance(d, dict) or d.get("id") != inp.get("id")):
                raise ValueError(f"{path}: failed/mismatched item.get capture")
            if not all(k in d for k in ("id", "name", "image")):
                raise ValueError(f"{path}: item.get missing required full-record fields")
            yield d, {**provenance, "kind": "item.get", "captured_at": c.get("at") or obj.get("at"),
                      "snapshot_key": c.get("snapshotKey"), "bundle_has_writes": bool(obj.get("entries"))}
        return
    if isinstance(obj, dict) and "cols" in obj and "rows" in obj:
        raise ValueError(f"{path}: seed columnar name index has no item.image")
    if isinstance(obj, dict) and obj.get("collector") == "items":
        records = (obj.get("payload") or {}).get("rows")
        source_kind = "item-collector"
    elif isinstance(obj, list):
        records, source_kind = obj, "local-record-list"
    elif isinstance(obj, dict) and isinstance(obj.get("rows"), list):
        records, source_kind = obj["rows"], "local-record-list"
    else:
        raise ValueError(f"{path}: unsupported item evidence; use item.get captures or full item rows")
    if not isinstance(records, list):
        raise ValueError(f"{path}: no item records")
    for d in records:
        if not isinstance(d, dict) or not all(k in d for k in ("id", "name", "image")):
            raise ValueError(f"{path}: rows must contain exact id, name and image")
        yield d, {**provenance, "kind": source_kind,
                  "captured_at": obj.get("t") if isinstance(obj, dict) else None,
                  "snapshot_key": None, "bundle_has_writes": False}


def make_roster(wave_path, capture_paths):
    wave = read_json(wave_path)
    if not isinstance(wave, dict) or not isinstance(wave.get("items"), list):
        raise ValueError("Wave must contain an items array")
    all_items = [(x, "candidate") for x in wave["items"]]
    all_items += [(x, "context") for x in wave.get("context", [])]
    if any(not isinstance(x, dict) or not isinstance(x.get("id"), str) or
           not isinstance(x.get("name"), str) for x, _ in all_items):
        raise ValueError("Wave entries require exact id and name")
    ids = [x["id"] for x, _ in all_items]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate wave item id")
    found = {}
    for path in capture_paths:
        for d, src in capture_records(path):
            if d["id"] in ids:
                found.setdefault(d["id"], []).append((d, src))
    rows = []
    for entry, role in all_items:
        hits = found.get(entry["id"], [])
        pairs = {(d["name"], d["image"]) for d, _ in hits}
        if not hits:
            status, chosen = "CAPTURE_MISSING", None
        elif len(pairs) > 1:
            status, chosen = "CONFLICT", None
        elif next(iter(pairs))[0] != entry["name"]:
            status, chosen = "NAME_MISMATCH", None
        elif not next(iter(pairs))[1]:
            status, chosen = "IMAGE_MISSING", None
        else:
            status = "CAPTURED" if all(s["kind"] == "item.get" for _, s in hits) else "LOCAL_RECORD"
            chosen = max(hits, key=lambda h: (
                capture_timestamp_key(h[1].get("captured_at")), h[1]["source_file"]))
        d, src = chosen if chosen else ({}, {})
        rows.append({
            "role": role, "id": entry["id"], "name": entry["name"],
            "status": status, "captured_name": d.get("name"),
            "item_type": d.get("itemType"), "rarity": d.get("rarity"),
            "slot": d.get("slot"), "hidden": d.get("hidden"),
            "image_url": d.get("image"), "captured_at": src.get("captured_at"),
            "source_file": src.get("source_file"), "source_sha256": src.get("source_sha256"),
            "snapshot_key": src.get("snapshot_key"), "bundle_has_writes": src.get("bundle_has_writes"),
            "evidence_kind": src.get("kind"), "matching_captures": len(hits),
            "notes": entry.get("notes", ""),
        })
    return {"schema": "tnr.item-icon-roster.v1", "wave": wave["wave"], "family": wave["family"],
            "wave_source": str(wave_path), "wave_sha256": digest(wave_path),
            "captures": [str(p) for p in capture_paths], "rows": rows}


def save_roster(roster, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "roster.json").write_text(
        json.dumps(roster, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (out_dir / "roster.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(roster["rows"])


def make_sheet(roster_path, image_map_path, out_path):
    """Use only local exact image bytes; missing art is a labelled draft tile."""
    from PIL import Image, ImageDraw, ImageFont

    roster, mapping = read_json(roster_path), read_json(image_map_path)
    if roster.get("schema") != "tnr.item-icon-roster.v1" or not isinstance(mapping, dict):
        raise ValueError("Expect roster.v1 and {item_id: local_image_path} map")
    rows = roster["rows"]
    sizes = (256, 125, 64, 32)
    offsets = (255, 540, 730, 860)
    w, row_h, top = 980, 328, 82
    im = Image.new("RGB", (w, top + row_h * len(rows) + 22), (18, 23, 30))
    draw = ImageDraw.Draw(im)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    def font(n, bold=False):
        try:
            return ImageFont.truetype(bold_path if bold else font_path, n)
        except OSError:
            return ImageFont.load_default()
    draw.text((18, 12), f"{roster['wave']} — captured item icons", font=font(24, True), fill=(240, 245, 250))
    draw.text((18, 47), "Offline proofing only · NEAREST scaling · not a game-ready export", font=font(13),
              fill=(165, 182, 195))
    audit = []
    for i, r in enumerate(rows):
        y = top + row_h * i
        draw.line((18, y, w-18, y), fill=(62, 73, 85), width=1)
        draw.text((18, y+15), r["name"], font=font(16, True), fill=(235, 240, 246))
        draw.text((18, y+45), r["id"], font=font(11), fill=(158, 174, 188))
        draw.text((18, y+68), r["role"].upper(), font=font(12), fill=(170, 216, 222))
        draw.text((18, y+92), r["status"], font=font(12), fill=(224, 185, 139))
        entry = mapping.get(r["id"])
        local = entry.get("path") if isinstance(entry, dict) else entry
        expected = entry.get("sha256") if isinstance(entry, dict) else None
        status, sha = "MISSING", None
        art = None
        if isinstance(local, str):
            p = Path(local)
            if p.is_file():
                sha = digest(p)
                if expected and expected != sha:
                    status = "HASH_MISMATCH"
                else:
                    try:
                        with Image.open(p) as raw:
                            raw.load()
                            art = raw.convert("RGBA")
                        status = "PRESENT"
                    except (OSError, ValueError):
                        status = "DECODE_FAILED"
        for sz, x in zip(sizes, offsets):
            draw.text((x, y+12), f"{sz}px", font=font(12), fill=(161, 179, 196))
            cell = Image.new("RGBA", (sz, sz), (35, 41, 49, 255))
            if art is not None:
                # No crop, no recolour, no interpolation; original file is untouched.
                preview = art.copy()
                preview.thumbnail((sz, sz), Image.Resampling.NEAREST)
                cell.alpha_composite(preview, ((sz-preview.width)//2, (sz-preview.height)//2))
            else:
                ImageDraw.Draw(cell).text((8, max(8, sz//2-8)), "NO FILE", font=font(11),
                                          fill=(210, 135, 135))
            im.paste(cell.convert("RGB"), (x, y+38))
        draw.text((18, y+285), f"Image: {status}", font=font(12),
                  fill=(150, 216, 176) if status == "PRESENT" else (235, 140, 140))
        audit.append({"id": r["id"], "status": status, "local_file": local, "sha256": sha})
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "PNG", optimize=True)
    summary = {"schema": "tnr.item-icon-sheet.v1", "wave": roster["wave"],
               "status": "ASSEMBLED_FOR_REVIEW" if all(a["status"] == "PRESENT" for a in audit) else "DRAFT_INCOMPLETE",
               "sheet": str(out), "sheet_sha256": digest(out),
               "sizes": list(sizes), "resampling": "Pillow NEAREST",
               "source_roster_sha256": digest(roster_path), "images": audit}
    out.with_suffix(".json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    rp = sub.add_parser("roster", help="Filter offline item.get captures against a named wave")
    rp.add_argument("--wave", required=True)
    rp.add_argument("--capture", action="append", default=[],
                    help="Repeat for each captured-results bundle or full-item JSON; omit for intake draft")
    rp.add_argument("--out", required=True, help="Output directory for roster.json / roster.csv")
    rp.add_argument("--require-complete", action="store_true",
                    help="Exit 2 if any candidate item is not captured")
    sp = sub.add_parser("sheet", help="Compose a draft contact sheet from local image bytes")
    sp.add_argument("--roster", required=True)
    sp.add_argument("--image-map", required=True,
                    help='JSON of {item_id: "local/path.webp"} or {"path": ..., "sha256": ...}')
    sp.add_argument("--out", required=True, help="PNG contact sheet; .json audit emitted beside it")
    args = ap.parse_args(argv)
    if args.command == "roster":
        roster = make_roster(args.wave, args.capture)
        save_roster(roster, args.out)
        statuses = {s: sum(r["status"] == s for r in roster["rows"]) for s in
                    sorted(set(r["status"] for r in roster["rows"]))}
        print(json.dumps({"wave": roster["wave"], "rows": len(roster["rows"]), "statuses": statuses}))
        if args.require_complete and any(r["role"] == "candidate" and r["status"] != "CAPTURED"
                                         for r in roster["rows"]):
            return 2
    else:
        summary = make_sheet(args.roster, args.image_map, args.out)
        print(json.dumps({"status": summary["status"], "sheet": summary["sheet"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
