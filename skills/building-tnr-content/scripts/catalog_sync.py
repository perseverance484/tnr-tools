#!/usr/bin/env python3
"""Keep the live catalogs honest between full harvests.

The catalogs are STORAGE: a record of what exists in the game. They were wrong on 2026-08-28 not
because they were old but because nothing in them said HOW old, so they got used as current. Four
quests picked out of 47_INDEX for a capture no longer existed.

So every row carries `last_verified` and `stale_after`, and a row that disappears from a full
listing is MARKED ABSENT WITH A DATE, never deleted. Deleting loses the fact that it once existed,
which is the thing that would have stopped it being picked.

  catalog_sync.py --check                       report freshness, touch nothing
  catalog_sync.py --fold results.json           fold a capture and/or an idmap in
  catalog_sync.py --fold r.json --dir state/catalogs

Absolute dates, not relative TTLs: staleness becomes a plain date comparison a script can make.
A textual marker like "[OUTDATED]" is not a mechanism, because nothing compares it to now.
"""
import argparse, json, os, sys
from datetime import datetime, timedelta, timezone

# how long a catalog kind stays trustworthy before it must be re-verified
SHELF_LIFE_DAYS = {"quest": 7, "ai": 7, "item": 30, "jutsu": 30, "asset": 30}

# which getAllNames procedure refreshes which catalog file
PROC_TO_KIND = {
    "quests.getAllNames": "quest",
    "profile.getAllAiNames": "ai",
    "item.getAllNames": "item",
    "jutsu.getAllNames": "jutsu",
    "gameAsset.getAllNames": "asset",
}
KIND_TO_FILE = {
    "quest": "47_INDEX_quest.json", "ai": "42_INDEX_ai.json",
    "item": "41_INDEX_item.json", "jutsu": "40_INDEX_jutsu.json",
    "asset": "43_INDEX_asset.json",
}


def now():
    return datetime.now(timezone.utc)


def iso(d):
    return d.strftime("%Y-%m-%d")


def load(path):
    with open(path) as fh:
        return json.load(fh)


def ensure_stamp_cols(cat):
    """Add the stamp columns if this catalog predates them. Columnar format: cols + rows."""
    for col in ("last_verified", "absent_since"):
        if col not in cat["cols"]:
            cat["cols"].append(col)
            for r in cat["rows"]:
                r.append(None)
    return cat


def idx(cat, col):
    return cat["cols"].index(col)


def fold_names(cat, kind, rows_seen, stamp):
    """rows_seen: list of {'id':..,'name':..} from a *.getAllNames capture."""
    i_id, i_n = idx(cat, "id"), idx(cat, "n")
    i_lv, i_ab = idx(cat, "last_verified"), idx(cat, "absent_since")
    by_id = {r[i_id]: r for r in cat["rows"]}
    seen = set()
    added = renamed = revived = 0
    for row in rows_seen:
        rid, name = row.get("id"), (row.get("name") or row.get("username") or "").strip()
        if not rid:
            continue
        seen.add(rid)
        if rid in by_id:
            r = by_id[rid]
            if name and r[i_n] != name:
                r[i_n] = name
                renamed += 1
            if r[i_ab] is not None:
                r[i_ab] = None          # it is back
                revived += 1
            r[i_lv] = stamp
        else:
            new = [None] * len(cat["cols"])
            new[i_id], new[i_n], new[i_lv] = rid, name, stamp
            cat["rows"].append(new)
            added += 1
    # a full listing is authoritative about absence
    absent = 0
    for r in cat["rows"]:
        if r[i_id] not in seen and r[i_ab] is None:
            r[i_ab] = stamp
            absent += 1
    return dict(kind=kind, added=added, renamed=renamed, revived=revived,
                marked_absent=absent, seen=len(seen))


ENTITY_TO_KIND = {"quest": "quest", "ai": "ai", "item": "item",
                  "jutsu": "jutsu", "asset": "asset"}


def fold_entries(cat, kind, entries, stamp):
    """A push results `entries` array is the only typed record of what we just created. The
    `idmap` is NOT usable here: it mixes jutsu, item, asset and quest ids with no entity field,
    and folding it blindly put 697 rows into two catalogs at once on the first test run."""
    i_id, i_n = idx(cat, "id"), idx(cat, "n")
    i_lv = idx(cat, "last_verified")
    have = {r[i_id] for r in cat["rows"]}
    added = confirmed = 0
    for e in entries:
        if ENTITY_TO_KIND.get(e.get("entity")) != kind:
            continue
        if e.get("state") not in (None, "ok"):
            continue                      # a failed entry created nothing
        rid = e.get("id")
        if not isinstance(rid, str) or not rid:
            continue
        name = (e.get("name") or "").strip()
        if rid in have:
            for r in cat["rows"]:
                if r[i_id] == rid:
                    r[i_lv] = stamp
                    confirmed += 1
                    break
        else:
            new = [None] * len(cat["cols"])
            new[i_id], new[i_n], new[i_lv] = rid, name, stamp
            cat["rows"].append(new)
            have.add(rid)
            added += 1
    return dict(kind=kind, added_from_push=added, confirmed_from_push=confirmed)


def freshness(cat, kind, today):
    i_lv, i_ab = idx(cat, "last_verified"), idx(cat, "absent_since")
    shelf = SHELF_LIFE_DAYS.get(kind, 30)
    never = stale = absent = fresh = 0
    oldest = None
    for r in cat["rows"]:
        if r[i_ab] is not None:
            absent += 1
            continue
        lv = r[i_lv]
        if not lv:
            never += 1
            continue
        d = datetime.strptime(lv, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        oldest = d if oldest is None or d < oldest else oldest
        if (today - d).days > shelf:
            stale += 1
        else:
            fresh += 1
    return dict(kind=kind, rows=len(cat["rows"]), fresh=fresh, stale=stale,
                never_verified=never, absent=absent, shelf_days=shelf,
                stale_after=iso(oldest + timedelta(days=shelf)) if oldest else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="state/catalogs")
    ap.add_argument("--fold", help="a results or capture bundle to fold in")
    ap.add_argument("--check", action="store_true", help="report freshness only")
    a = ap.parse_args()
    today, stamp = now(), iso(now())

    if a.check or not a.fold:
        bad = 0
        for kind, fn in KIND_TO_FILE.items():
            p = os.path.join(a.dir, fn)
            if not os.path.exists(p):
                print(f"MISSING  {fn}: no catalog. Capture before trusting any lookup.")
                bad += 1
                continue
            f = freshness(ensure_stamp_cols(load(p)), kind, today)
            flag = "STALE " if (f["stale"] or f["never_verified"]) else "ok    "
            print(f"{flag} {fn:26} {f['rows']:5} rows | fresh {f['fresh']:5} "
                  f"stale {f['stale']:5} unverified {f['never_verified']:5} "
                  f"absent {f['absent']:4} | shelf {f['shelf_days']}d")
            bad += 1 if (f["stale"] or f["never_verified"]) else 0
        print("\nEvery lookup against a STALE catalog needs a capture first." if bad
              else "\nAll catalogs within shelf life.")
        return 1 if bad else 0

    bundle = load(a.fold)
    reports = []
    for cap in bundle.get("captures", []) or []:
        kind = PROC_TO_KIND.get(cap.get("proc"))
        data = cap.get("data")
        if not kind or not isinstance(data, list):
            continue
        p = os.path.join(a.dir, KIND_TO_FILE[kind])
        if not os.path.exists(p):
            print(f"skip {kind}: {p} not present")
            continue
        cat = ensure_stamp_cols(load(p))
        rep = fold_names(cat, kind, data, stamp)
        json.dump(cat, open(p, "w"), indent=1, ensure_ascii=False)
        reports.append(rep)

    entries = bundle.get("entries") or []
    if entries:
        for kind in sorted({ENTITY_TO_KIND[e["entity"]] for e in entries
                            if e.get("entity") in ENTITY_TO_KIND}):
            p = os.path.join(a.dir, KIND_TO_FILE[kind])
            if not os.path.exists(p):
                continue
            cat = ensure_stamp_cols(load(p))
            rep = fold_entries(cat, kind, entries, stamp)
            if rep["added_from_push"] or rep["confirmed_from_push"]:
                json.dump(cat, open(p, "w"), indent=1, ensure_ascii=False)
                reports.append(rep)

    if not reports:
        print("nothing foldable: no *.getAllNames capture and no typed entries")
        return 1
    for r in reports:
        print("  " + json.dumps(r))
    print(f"\nfolded at {stamp}. Rows absent from a full listing were marked, not deleted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
