#!/usr/bin/env python3
"""Build the offline record catalog the PvP harness reads (director, 2026-11-11: "you should have them all pulled and
plugged into the offline harness so it just reads what was used. No mid battle lookups or estimations").

Every full jutsu/item record (a dict with id, name and an effects list) captured anywhere under harvests/ is collected;
the newest copy of each id wins (updatedAt, then capture time). Curated entries in kit/records.json and the live field
refreshes in kit/live_overrides.json are laid on top when they are at least as new. Then every kit/live_jutsu_*.jsonl
patch (connector reads of the engine fields: effects, target, range, cooldown, method, AP cost, weapon, usage type,
jutsu type, bloodline) replaces those fields when its updatedAt is newer; cosmetic effect keys (sfx, animations,
description) are carried over from the old copy of the same effect type, else "". No live calls.

Hidden records are left out (director 2026-11-11, RUL-2026-11-11-149: "Do not use hidden records, treat them like
they are actually hidden"): a jutsu, item or bloodline whose newest copy says hidden never reaches the catalog,
whichever capture or patch it came from. The player meets such a record only as a log line in a fight.

Output: harness/pvp_turn/kit/catalog.json  {id: {"record": {...}, "kind": "jutsu"|"item", "source": path, "updatedAt"}}
(gitignored: derived from committed harvests, rebuild with this script).
Usage: build_catalog.py [--check ID ...]   (--check prints which of the given ids are in the catalog)
"""
import glob
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
KIT = os.path.join(REPO, "harness/pvp_turn/kit")
OUT = os.path.join(KIT, "catalog.json")


def walk(x):
    if isinstance(x, dict):
        if isinstance(x.get("id"), str) and isinstance(x.get("effects"), list) and "name" in x:
            yield x
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)


def kind_of(rec):
    if "itemType" in rec:
        return "item"
    if "jutsuType" in rec:
        return "jutsu"
    return None


def is_bloodline(rec):
    return ("jutsuType" not in rec and "itemType" not in rec and "aiProfile" not in rec
            and ("regenIncrease" in rec or not rec.get("village"))
            and rec.get("rank") in ("D", "C", "B", "A", "S", "H"))


def build(repo=None, kit=None):
    """Build kit/catalog.json and kit/bloodlines.json; returns the catalog. repo / kit default to this repository
    (the tests point them at a temporary tree)."""
    REPO, KIT = repo or globals()["REPO"], kit or globals()["KIT"]
    OUT = os.path.join(KIT, "catalog.json")
    best = {}
    bls = {}
    for path in sorted(glob.glob(os.path.join(REPO, "harvests/**/*.json"), recursive=True)):
        try:
            doc = json.load(open(path))
        except (OSError, ValueError):
            continue
        for rec in walk(doc):
            k = kind_of(rec)
            if not k:
                if is_bloodline(rec) and (rec.get("updatedAt") or "") >= (bls.get(rec["id"], {}).get("updatedAt") or ""):
                    bls[rec["id"]] = rec
                continue
            key = (rec.get("updatedAt") or "", path)
            if rec["id"] not in best or key >= best[rec["id"]][0]:
                best[rec["id"]] = (key, rec, k, os.path.relpath(path, REPO))
    out = {i: {"record": r, "kind": k, "source": src, "updatedAt": key[0]} for i, (key, r, k, src) in best.items()}
    rp = os.path.join(KIT, "records.json")
    if os.path.exists(rp):
        for i, v in json.load(open(rp)).items():
            if i.startswith("_"):
                continue
            cur = out.get(i)
            if cur is None or (v.get("updatedAt") or "") >= cur["updatedAt"]:
                out[i] = {"record": v["record"], "kind": kind_of(v["record"]) or "jutsu",
                          "source": "kit/records.json (" + v.get("source", "?") + ")", "updatedAt": v.get("updatedAt") or ""}
    op = os.path.join(KIT, "live_overrides.json")
    if os.path.exists(op):
        for i, ov in json.load(open(op)).items():
            if i in out and not i.startswith("_") and ov.get("updatedAt", "") >= out[i]["updatedAt"]:
                out[i]["record"] = dict(out[i]["record"], **ov)
                out[i]["updatedAt"] = ov["updatedAt"]
                out[i]["source"] += " + live_overrides.json"
    COSMETIC = ("appearSfx", "disappearSfx", "appearAnimation", "staticAnimation", "staticAssetPath",
                "disappearAnimation", "description")
    for pp in sorted(glob.glob(os.path.join(KIT, "live_jutsu_*.jsonl"))):
        for line in open(pp):
            if not line.strip():
                continue
            patch = json.loads(line)
            cur = out.get(patch["id"])
            if cur and patch["updatedAt"] <= cur["updatedAt"]:
                continue
            old = dict(cur["record"]) if cur else {"id": patch["id"]}
            old_fx = list(old.get("effects", []))
            fx = []
            for e in patch["effects"]:
                prev = next((o for o in old_fx if o.get("type") == e["type"]), None)
                if prev is not None:
                    old_fx.remove(prev)
                fx.append({**{k: (prev or {}).get(k, "") for k in COSMETIC}, **e})
            rec = {**old, **{k: v for k, v in patch.items() if k != "effects"}, "effects": fx}
            out[patch["id"]] = {"record": rec, "kind": "jutsu", "updatedAt": patch["updatedAt"],
                                "source": os.path.relpath(pp, REPO) + " (connector read)"}
    for pp in sorted(glob.glob(os.path.join(KIT, "live_bloodlines_*.jsonl"))):
        for line in open(pp):
            if line.strip():
                b = json.loads(line)
                if (b.get("updatedAt") or "") >= (bls.get(b["id"], {}).get("updatedAt") or ""):
                    bls[b["id"]] = b
    # hidden records never reach the player: checked last, on the newest copy, so no capture or patch can add one
    n_all, n_bl = len(out), len(bls)
    out = {i: v for i, v in out.items() if not v["record"].get("hidden")}
    bls = {i: b for i, b in bls.items() if not b.get("hidden")}
    print(f"hidden, left out: {n_all - len(out)} jutsu and items, {n_bl - len(bls)} bloodlines")
    json.dump(bls, open(os.path.join(KIT, "bloodlines.json"), "w"), separators=(",", ":"))
    print(f"bloodlines: {len(bls)} -> harness/pvp_turn/kit/bloodlines.json")
    json.dump(out, open(OUT, "w"), separators=(",", ":"))
    n_j = sum(v["kind"] == "jutsu" for v in out.values())
    print(f"catalog: {len(out)} records ({n_j} jutsu, {len(out) - n_j} items) -> {os.path.relpath(OUT, REPO)}")
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--check":
        cat = json.load(open(OUT))
        for i in sys.argv[2:]:
            v = cat.get(i)
            print(i, (v["record"]["name"], v["updatedAt"][:10]) if v else "MISSING")
    else:
        build()
