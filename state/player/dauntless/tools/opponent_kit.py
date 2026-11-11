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


def save_kit(user_id, d, name=""):
    """Save his equipped kit from a jutsu.getPublicUserJutsus response; returns (path, kit, catalog gaps)."""
    ids, lv, eq = d["*.jutsuId"], d.get("*.level") or [25] * len(d["*.jutsuId"]), d["*.equipped"]
    if not (len(ids) == len(lv) == len(eq)):
        raise ValueError(f"misaligned select arrays ({len(ids)}/{len(lv)}/{len(eq)}); re-read without truncation")
    kit = [(j, int(l or 1)) for j, l, e in zip(ids, lv, eq) if e]
    cat = EB._records()
    out = {"userId": user_id, "name": name, "savedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "jutsu": [j for j, _ in kit], "jutsuLevels": {j: l for j, l in kit}, "items": []}
    path = os.path.join(EB.HARNESS, "kit", "opponents", f"{user_id}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    old = EB.opponent_kit(user_id) or {}
    for k in ("imbues", "weapons", "items", "gear", "bloodlineId"):        # learned in fights: never dropped
        if old.get(k) and not out.get(k):
            out[k] = old[k]
    json.dump(out, open(path, "w"), indent=1)
    return path, kit, [j for j, _ in kit if j not in cat]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("user_id")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--name", default="")
    a = ap.parse_args()
    d = json.load(open(a.file)) if a.file else json.load(sys.stdin)
    try:
        path, kit, gaps = save_kit(a.user_id, d, a.name)
    except ValueError as e:
        sys.exit(str(e))
    cat = EB._records()
    print(f"saved {len(kit)} equipped jutsu for {a.name or a.user_id}:",
          ", ".join(f"{cat[j]['record']['name']} L{l}" if j in cat else f"{j} L{l}" for j, l in kit))
    if gaps:
        print("CATALOG GAP:", ",".join(gaps))


if __name__ == "__main__":
    main()


IMBUE_KEYS = ("type", "power", "powerPerLevel", "level", "calculation", "direction", "elements", "statTypes",
              "generalTypes", "poolsAffected")


def learn_weapons(user_id, effects):
    """Weapons can be imbued with extra effects that no record shows (director 2026-11-11): when his weapon lands, the
    live effect list shows what it applied. Effects he cast this round from a weapon (actionId = the weapon's item
    id), of a type the weapon's record does not carry, are saved to his kit as that weapon's imbue; every weapon he
    swings is remembered (up to 2 equipped). Returns the weapon ids that taught something new."""
    recs = EB._records()
    kit = EB.opponent_kit(user_id) or {"userId": user_id, "jutsu": [], "jutsuLevels": {}}
    imbues, weapons = kit.setdefault("imbues", {}), kit.setdefault("weapons", [])
    new = []
    for e in effects or []:
        aid = e.get("actionId")
        rec = (recs.get(aid) or {}).get("record") or {}
        if e.get("creatorId") != user_id or not e.get("castThisRound") or rec.get("itemType") != "WEAPON":
            continue
        if aid not in weapons:
            weapons.append(aid); new.append(aid)
        if e.get("type") in {x.get("type") for x in rec.get("effects", [])}:
            continue
        spec = {k: e.get(k) for k in IMBUE_KEYS if e.get(k) is not None}
        spec["rounds"] = int(e.get("rounds") or 0)
        spec["target"] = "SELF" if e.get("targetId") == user_id else "INHERIT"
        have = imbues.setdefault(aid, [])
        if not any(h.get("type") == spec["type"] and h.get("target") == spec["target"] for h in have):
            have.append(spec); new.append(aid)
    if new:
        path = os.path.join(EB.HARNESS, "kit", "opponents", f"{user_id}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump(kit, open(path, "w"), indent=1)
    return new
