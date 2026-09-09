#!/usr/bin/env python3
"""Build the name lookup layer from canonical seed catalogs plus inbox deltas."""

from __future__ import annotations

import argparse
import datetime
import json
import re
from pathlib import Path

RAW = "https://raw.githubusercontent.com/perseverance484/tnr-tools/main"
SEEDS = {
    "jutsu": "40_INDEX_jutsu.json",
    "item": "41_INDEX_item.json",
    "ai": "42_INDEX_ai.json",
    "asset": "43_INDEX_asset.json",
    "quest": "47_INDEX_quest.json",
}
CAPTURE_ENTITY = {
    "jutsu.getAllNames": "jutsu",
    "item.getAllNames": "item",
    "quests.getAllNames": "quest",
    "gameAsset.getAllNames": "asset",
    "profile.getAllAiNames": "ai",
}


def load(path: Path):
    return json.loads(path.read_text())


def seed_rows(path: Path) -> tuple[list[list], str | None]:
    data = load(path)
    fresh = data.get("_freshness") or {}
    stamp = (
        fresh.get("generated")
        or fresh.get("date")
        or fresh.get("harvested")
        or fresh.get("newest_record")
        or data.get("generated")
    )
    if stamp and "unknown" in str(stamp):
        stamp = "seed catalog (pre-answers)"

    cols = [str(col).lower() for col in data.get("cols") or []]
    try:
        id_idx = cols.index("id")
        name_idx = next(cols.index(name) for name in ("name", "username", "n") if name in cols)
    except (ValueError, StopIteration) as exc:
        raise ValueError(f"{path}: seed catalog needs id and name columns") from exc
    hidden_idx = next((cols.index(name) for name in ("hidden", "hid") if name in cols), None)

    rows = []
    for row in data.get("rows") or []:
        hidden = row[hidden_idx] if hidden_idx is not None and hidden_idx < len(row) else None
        rows.append([row[id_idx], row[name_idx], bool(hidden) if hidden is not None else None])
    return rows, stamp


def bundle_time(path: Path) -> str | None:
    match = re.search(r"tnr_results_(\d+)", path.name)
    if not match:
        return None
    when = datetime.datetime.fromtimestamp(int(match.group(1)) / 1000, datetime.timezone.utc)
    return when.strftime("%Y-%m-%d %H:%MZ")


def inbox_rows(repo: Path) -> dict[str, dict]:
    latest = {}
    for path in sorted((repo / "harvests" / "inbox").glob("tnr_results_*.json")):
        try:
            bundle = load(path)
        except (OSError, json.JSONDecodeError):
            continue
        for capture in bundle.get("captures") or []:
            entity = CAPTURE_ENTITY.get(str(capture.get("proc") or ""))
            if not entity:
                continue
            rows = capture.get("rows")
            if not isinstance(rows, list):
                rows = capture.get("data")
            if not isinstance(rows, list):
                continue
            normalized = [
                [row.get("id") or row.get("userId"), row.get("name") or row.get("username"), row.get("hidden")]
                for row in rows
                if isinstance(row, dict)
            ]
            normalized = [row for row in normalized if row[0] and row[1]]
            if normalized:
                latest[entity] = {
                    "rows": normalized,
                    "source": path.relative_to(repo).as_posix(),
                    "captured": bundle_time(path) or "unknown",
                }
    return latest


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, separators=(",", ":")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--out", default="answers")
    args = parser.parse_args()

    repo = Path(args.repo)
    out = repo / args.out
    out.mkdir(parents=True, exist_ok=True)
    hot = inbox_rows(repo)
    hot_out = {
        "note": (
            "Recently harvested records NOT yet in the seed catalogs: newest inbox capture per entity, "
            "minus rows the seed already holds. A name here is live even though names_<entity>.json lacks it."
        ),
        "entities": {},
    }
    index = [
        "# answers/INDEX.md - the lookup layer",
        "",
        "Two fetches answer any name/id lookup: this INDEX, then the entity file",
        "(plus hot.json when its delta column below is non-zero). Rows are",
        "`[id, name, hidden]`; `hidden: null` means the source did not carry the",
        "flag. `generated` stamps are DERIVED from sources, so regeneration is",
        "idempotent. Raw CDN caches ~5 min; fresher than that takes a capture.",
        "",
        "| entity | rows | source stamp | hot delta (newer, uncataloged) | fetch |",
        "|---|---|---|---|---|",
    ]

    wrote = 0
    for entity, filename in SEEDS.items():
        source = repo / "harvests" / "seed" / filename
        if not source.exists():
            index.append(f"| {entity} | - | none committed | - | - |")
            continue

        rows, stamp = seed_rows(source)
        rows.sort(key=lambda row: (row[1] or "").lower())
        known_ids = {row[0] for row in rows}
        captured = hot.get(entity)
        delta = []
        if captured:
            delta = sorted(
                (row for row in captured["rows"] if row[0] not in known_ids),
                key=lambda row: (row[1] or "").lower(),
            )
            if delta:
                hot_out["entities"][entity] = {
                    "source_bundle": captured["source"],
                    "captured": captured["captured"],
                    "row_delta": len(delta),
                    "rows": delta,
                }

        output_name = f"names_{entity}.json"
        write_json(
            out / output_name,
            {
                "generated": stamp or "unknown",
                "entity": entity,
                "source": source.relative_to(repo).as_posix(),
                "source_stamp": stamp,
                "count": len(rows),
                "hot_delta": len(delta),
                "hot_hint": (
                    f"{len(delta)} newer record(s) live but uncataloged - fetch answers/hot.json"
                    if delta
                    else None
                ),
                "rows": rows,
            },
        )
        index.append(
            f"| {entity} | {len(rows)} | {stamp or 'unknown'} | {len(delta)} | "
            f"{RAW}/answers/{output_name} |"
        )
        wrote += 1

    write_json(out / "hot.json", hot_out)
    index += [
        "",
        f"Hot shard (delta rows + capture stamps): {RAW}/answers/hot.json",
        "",
        "Other fetchable canon:",
        f"- Engine laws (full numbered text): {RAW}/docs/ENGINE_LAWS.md",
        f"- Doctrine (single source): {RAW}/docs/DOCTRINE.md",
        "",
        "Skill zips (download, not fetch): /dist/ on the repo page.",
        "",
        "A capture beats any file here (precedence). Retention: see",
        "docs/COMPACTION_RUNBOOK.md - manual-only, seed is the audit floor.",
    ]
    (out / "INDEX.md").write_text("\n".join(index) + "\n")

    delta_count = sum(row["row_delta"] for row in hot_out["entities"].values())
    print(f"answers: {wrote} entity files + hot.json ({delta_count} delta rows) + INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
