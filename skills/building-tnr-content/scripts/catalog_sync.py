#!/usr/bin/env python3
"""Keep catalog presence and freshness honest between full harvests."""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

SHELF_LIFE_DAYS = {"quest": 7, "ai": 7, "item": 30, "jutsu": 30, "asset": 30}
PROC_TO_KIND = {
    "quests.getAllNames": "quest",
    "profile.getAllAiNames": "ai",
    "item.getAllNames": "item",
    "jutsu.getAllNames": "jutsu",
    "gameAsset.getAllNames": "asset",
}
KIND_TO_FILE = {
    "quest": "47_INDEX_quest.json",
    "ai": "42_INDEX_ai.json",
    "item": "41_INDEX_item.json",
    "jutsu": "40_INDEX_jutsu.json",
    "asset": "43_INDEX_asset.json",
}


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save(path, value):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=1, ensure_ascii=False)


def iso(value):
    return value.strftime("%Y-%m-%d")


def ensure_stamp_cols(cat):
    for col in ("last_verified", "absent_since"):
        if col not in cat["cols"]:
            cat["cols"].append(col)
            for row in cat["rows"]:
                row.append(None)
    return cat


def idx(cat, col):
    return cat["cols"].index(col)


def full_name_listing(cap):
    """Return (kind, rows) only when absence from the capture is authoritative."""
    kind = PROC_TO_KIND.get(cap.get("proc"))
    data = cap.get("data")
    if not kind or not isinstance(data, list):
        return None
    if cap.get("input"):
        return kind, None
    return kind, data


def fold_names(cat, kind, rows_seen, stamp):
    i_id, i_name = idx(cat, "id"), idx(cat, "n")
    i_verified, i_absent = idx(cat, "last_verified"), idx(cat, "absent_since")
    by_id = {row[i_id]: row for row in cat["rows"]}
    seen = set()
    added = renamed = revived = 0

    for item in rows_seen:
        record_id = item.get("id")
        name = (item.get("name") or item.get("username") or "").strip()
        if not record_id:
            continue
        seen.add(record_id)
        row = by_id.get(record_id)
        if row is None:
            row = [None] * len(cat["cols"])
            row[i_id], row[i_name], row[i_verified] = record_id, name, stamp
            cat["rows"].append(row)
            by_id[record_id] = row
            added += 1
            continue
        if name and row[i_name] != name:
            row[i_name] = name
            renamed += 1
        if row[i_absent] is not None:
            row[i_absent] = None
            revived += 1
        row[i_verified] = stamp

    marked_absent = 0
    for row in cat["rows"]:
        if row[i_id] not in seen and row[i_absent] is None:
            row[i_absent] = stamp
            marked_absent += 1

    return {
        "kind": kind,
        "added": added,
        "renamed": renamed,
        "revived": revived,
        "marked_absent": marked_absent,
        "seen": len(seen),
    }


def fold_entries(cat, kind, entries, stamp):
    i_id, i_name = idx(cat, "id"), idx(cat, "n")
    i_verified = idx(cat, "last_verified")
    by_id = {row[i_id]: row for row in cat["rows"]}
    added = confirmed = 0

    for entry in entries:
        if entry.get("entity") != kind or entry.get("state") not in (None, "ok"):
            continue
        record_id = entry.get("id")
        if not isinstance(record_id, str) or not record_id:
            continue
        row = by_id.get(record_id)
        if row is not None:
            row[i_verified] = stamp
            confirmed += 1
            continue
        row = [None] * len(cat["cols"])
        row[i_id] = record_id
        row[i_name] = (entry.get("name") or "").strip()
        row[i_verified] = stamp
        cat["rows"].append(row)
        by_id[record_id] = row
        added += 1

    return {"kind": kind, "added_from_push": added, "confirmed_from_push": confirmed}


def freshness(cat, kind, today):
    i_verified, i_absent = idx(cat, "last_verified"), idx(cat, "absent_since")
    shelf = SHELF_LIFE_DAYS.get(kind, 30)
    counts = {"fresh": 0, "stale": 0, "never_verified": 0, "absent": 0}
    oldest = None

    for row in cat["rows"]:
        if row[i_absent] is not None:
            counts["absent"] += 1
            continue
        verified = row[i_verified]
        if not verified:
            counts["never_verified"] += 1
            continue
        date = datetime.strptime(verified, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        oldest = date if oldest is None or date < oldest else oldest
        counts["stale" if (today - date).days > shelf else "fresh"] += 1

    return {
        "kind": kind,
        "rows": len(cat["rows"]),
        **counts,
        "shelf_days": shelf,
        "stale_after": iso(oldest + timedelta(days=shelf)) if oldest else None,
    }


def catalog_path(directory, kind):
    return os.path.join(directory, KIND_TO_FILE[kind])


def check_catalogs(directory, today):
    bad = 0
    for kind, filename in KIND_TO_FILE.items():
        path = catalog_path(directory, kind)
        if not os.path.exists(path):
            print(f"MISSING  {filename}: no catalog. Capture before trusting any lookup.")
            bad += 1
            continue
        report = freshness(ensure_stamp_cols(load(path)), kind, today)
        stale = report["stale"] or report["never_verified"]
        print(
            f"{'STALE ' if stale else 'ok    '} {filename:26} {report['rows']:5} rows | "
            f"fresh {report['fresh']:5} stale {report['stale']:5} "
            f"unverified {report['never_verified']:5} absent {report['absent']:4} | "
            f"shelf {report['shelf_days']}d"
        )
        bad += int(bool(stale))
    print("\nEvery lookup against a STALE catalog needs a capture first." if bad else "\nAll catalogs within shelf life.")
    return 1 if bad else 0


def fold_bundle(directory, bundle, stamp):
    reports = []
    for cap in bundle.get("captures") or []:
        listing = full_name_listing(cap)
        if listing is None:
            continue
        kind, rows_seen = listing
        if rows_seen is None:
            print(f"skip {kind}: filtered {cap.get('proc')} input is not authoritative for absence")
            continue
        path = catalog_path(directory, kind)
        if not os.path.exists(path):
            print(f"skip {kind}: {path} not present")
            continue
        cat = ensure_stamp_cols(load(path))
        reports.append(fold_names(cat, kind, rows_seen, stamp))
        save(path, cat)

    entries = bundle.get("entries") or []
    kinds = sorted({entry.get("entity") for entry in entries if entry.get("entity") in KIND_TO_FILE})
    for kind in kinds:
        path = catalog_path(directory, kind)
        if not os.path.exists(path):
            continue
        cat = ensure_stamp_cols(load(path))
        report = fold_entries(cat, kind, entries, stamp)
        if report["added_from_push"] or report["confirmed_from_push"]:
            save(path, cat)
            reports.append(report)

    if not reports:
        print("nothing foldable: no unfiltered *.getAllNames capture and no typed entries")
        return 1
    for report in reports:
        print("  " + json.dumps(report))
    print(f"\nfolded at {stamp}. Rows absent from a full listing were marked, not deleted.")
    return 0


def selftest():
    filtered = {
        "proc": "gameAsset.getAllNames",
        "input": {"type": "STATIC"},
        "data": [{"id": "a", "name": "A"}],
    }
    assert full_name_listing(filtered) == ("asset", None)

    full = {"proc": "gameAsset.getAllNames", "data": [{"id": "a", "name": "A"}]}
    kind, rows_seen = full_name_listing(full)
    cat = ensure_stamp_cols({"cols": ["id", "n"], "rows": [["a", "Old"], ["b", "B"]]})
    report = fold_names(cat, kind, rows_seen, "2026-09-09")
    assert report == {"kind": "asset", "added": 0, "renamed": 1, "revived": 0, "marked_absent": 1, "seen": 1}
    assert cat["rows"][1][idx(cat, "absent_since")] == "2026-09-09"
    print("catalog_sync selftest OK")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="state/catalogs")
    parser.add_argument("--fold", help="results or capture bundle to fold in")
    parser.add_argument("--check", action="store_true", help="report freshness only")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    today = datetime.now(timezone.utc)
    stamp = iso(today)
    if args.check or not args.fold:
        return check_catalogs(args.dir, today)
    return fold_bundle(args.dir, load(args.fold), stamp)


if __name__ == "__main__":
    raise SystemExit(main())
