#!/usr/bin/env python3
"""Build the offline record catalog the PvP harness reads (director, 2026-11-11: "you should have them all pulled and
plugged into the offline harness so it just reads what was used. No mid battle lookups or estimations").

Every full jutsu/item record (a dict with id, name and an effects list) captured anywhere under harvests/ is collected;
the newest copy of each id wins (updatedAt, then capture time). Curated entries in kit/records.json and the live field
refreshes in kit/live_overrides.json are laid on top when they are at least as new. No live calls.

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


def build():
    best = {}
    for path in sorted(glob.glob(os.path.join(REPO, "harvests/**/*.json"), recursive=True)):
        try:
            doc = json.load(open(path))
        except (OSError, ValueError):
            continue
        for rec in walk(doc):
            k = kind_of(rec)
            if not k:
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
