#!/usr/bin/env python3
"""Save an opponent's real equipped jutsu kit BEFORE the fight, so the engine planner plays his actual moves instead of
a calibrated stand-in (director, 2026-11-11: "No mid battle lookups or estimations").

Input (FILE or stdin): the response of
  jutsu.getPublicUserJutsus {userId} with select ["*.jutsuId", "*.level", "*.equipped"]
Writes harness/pvp_turn/kit/opponents/<userId>.json {userId, name, savedAt, jutsu: [ids], jutsuLevels: {id: level}}
and reports any equipped jutsu missing from kit/catalog.json (a catalog gap to fill from harvests, not mid-fight).
Items are not public (item.getPublicUserItems: "You can only view your own items"); items he uses still resolve from
the catalog by their logged action id.
Usage: opponent_kit.py USER_ID [--name NAME] [FILE]
When I am the one attacked, run it once at the start of round 1 (one kit read, no per-move lookups).
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_bridge as EB  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("user_id")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--name", default="")
    a = ap.parse_args()
    d = json.load(open(a.file)) if a.file else json.load(sys.stdin)
    ids, lv, eq = d["*.jutsuId"], d.get("*.level") or [25] * len(d["*.jutsuId"]), d["*.equipped"]
    if not (len(ids) == len(lv) == len(eq)):
        sys.exit(f"misaligned select arrays ({len(ids)}/{len(lv)}/{len(eq)}); re-read without truncation")
    kit = [(j, int(l or 1)) for j, l, e in zip(ids, lv, eq) if e]
    cat = EB._records()
    out = {"userId": a.user_id, "name": a.name, "savedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "jutsu": [j for j, _ in kit], "jutsuLevels": {j: l for j, l in kit}, "items": []}
    path = os.path.join(EB.HARNESS, "kit", "opponents", f"{a.user_id}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), indent=1)
    gaps = [j for j, _ in kit if j not in cat]
    print(f"saved {len(kit)} equipped jutsu for {a.name or a.user_id}:",
          ", ".join(f"{cat[j]['record']['name']} L{l}" if j in cat else f"{j} L{l}" for j, l in kit))
    if gaps:
        print("CATALOG GAP:", ",".join(gaps))


if __name__ == "__main__":
    main()
