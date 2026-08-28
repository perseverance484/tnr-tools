#!/usr/bin/env python3
"""Regenerate the 4x_INDEX files (and repo-bound full catalogs) from harvester dumps.

2026-08-26: project knowledge carries INDEXES only (columnar: cols + rows arrays,
id/name/routing fields, _freshness stamp with newest createdAt). Full catalogs go
to the tnr-tools repo. This script now emits both; keep createdAt in every index.

Point it at a folder of tnr_h1_*.json harvests; it picks the newest of each
kind and writes trimmed catalogs sized to live in project knowledge.

  python3 refresh_catalogs.py /mnt/user-data/uploads /mnt/user-data/outputs

Trim philosophy: keep every field used for lookup, dedup, reference or
balance work. Drop cosmetics, timestamps, and anything reconstructible.
Full dumps stay on GitHub; these are the working copies.
"""
import json, os, re, sys, glob
from collections import Counter



INDEX_SPEC = {
    "jutsu":  ("40_INDEX_jutsu.json",  ["id", "n", "rank", "type", "hid", "createdAt"]),
    "items":  ("41_INDEX_item.json",   ["id", "n", "type", "rar", "slot", "hid", "createdAt"]),
    "ais":    ("42_INDEX_ai.json",     ["id", "n", "lvl", "rank", "summon", "arena", "createdAt"]),
    "assets": ("43_INDEX_asset.json",  ["id", "n", "type", "folder", "hid", "createdAt"]),
    "quests": ("47_INDEX_quest.json",  ["id", "n", "type", "rank", "lvl", "vil", "hid", "createdAt"]),
}
INDEX_CONTRACT = ("INDEX ONLY, columnar: cols names the fields, each row is an array in that order. "
    "For id/name lookup, dedup and tier routing. Full catalogs live in the tnr-tools repo; the live "
    "game is queried via the builder capture block. Absence here proves nothing about the live game: "
    "anything created after newest_record is invisible.")


def emit_index(kind, rows, out_dir):
    name, keep = INDEX_SPEC[kind]
    slim = [[r.get(k) for k in keep] for r in rows]
    newest = max((str(r.get("createdAt") or "")[:10] for r in rows), default="unknown")
    with open(os.path.join(out_dir, name), "w") as fh:
        json.dump({"_freshness": {"row_count": len(rows), "newest_record": newest or "unknown",
                                  "contract": INDEX_CONTRACT},
                   "cols": keep, "rows": slim}, fh, separators=(",", ":"))
    return name


def newest(folder, kind):
    fs = glob.glob(os.path.join(folder, f"tnr_h1_{kind}_*.json"))
    if not fs:
        return None
    return sorted(fs)[-1]


def rows(path):
    if not path:
        return []
    with open(path) as fh:
        return json.load(fh)["payload"]["rows"]


def eff(e):
    """Compact one effect row to 'type power/rounds'."""
    t = e.get("type")
    if t == "visual":
        return None
    p, r = e.get("power"), e.get("rounds")
    s = t
    if p not in (None, 0):
        s += f" {p}"
    if r:
        s += f"/{r}r"
    return s


def build(folder, out):
    PH = "630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"
    J = {j["id"]: j for j in rows(newest(folder, "jutsu"))}
    I = {i["id"]: i for i in rows(newest(folder, "items"))}
    A = {a["id"]: a for a in rows(newest(folder, "assets"))}
    Q = {q["id"]: q for q in rows(newest(folder, "quests"))}
    deepf = newest(folder, "aiDeep")
    D = {r["userId"]: r for r in rows(deepf) if "username" in r} if deepf else {}
    V = {v["id"]: v["name"] for v in rows(newest(folder, "villages"))}

    # ---- jutsu ----
    jc = []
    for j in J.values():
        jc.append({
            "id": j["id"], "n": j["name"].strip(), "rank": j.get("jutsuRank"),
            "type": j.get("jutsuType"), "hid": bool(j.get("hidden")),
            "tgt": j.get("target"), "rng": j.get("range"), "cd": j.get("cooldown"),
            "ap": j.get("actionCostPerc"), "el": j.get("elements") or [],
            "eff": [x for x in (eff(e) for e in j.get("effects") or []) if x],
        })
    jc.sort(key=lambda x: x["n"].lower())

    # ---- items ----
    ic = []
    for i in I.values():
        ic.append({
            "id": i["id"], "n": i["name"].strip(), "type": i.get("itemType"),
            "rar": i.get("rarity"), "slot": i.get("slot"), "cost": i.get("cost"),
            "hid": bool(i.get("hidden")), "ap": i.get("actionCostPerc"),
            "eff": [x for x in (eff(e) for e in i.get("effects") or []) if x],
        })
    ic.sort(key=lambda x: x["n"].lower())

    # ---- assets ----
    ac = []
    for a in A.values():
        img = a.get("image") or ""
        ac.append({
            "id": a["id"], "n": (a.get("name") or "").strip(), "type": a.get("type"),
            "folder": a.get("folder"), "art": bool(img) and PH not in img,
            "url": img,
        })
    ac.sort(key=lambda x: (x["type"] or "", x["n"].lower()))

    # ---- quest references, so AI usage is known without re-deriving ----
    used = {}
    for q in Q.values():
        for o in (q.get("content") or {}).get("objectives") or []:
            for oa in (o.get("opponentAIs") or []) + (o.get("attackers") or []):
                for x in oa.get("ids", []):
                    used.setdefault(x, []).append(q["name"].strip())

    # ---- AI ----
    aic = []
    for uid, r in D.items():
        kit = [{"id": x["jutsuId"], "n": J.get(x["jutsuId"], {}).get("name", "?").strip()}
               for x in (r.get("jutsus") or [])]
        items = [{"id": x.get("itemId"),
                  "n": I.get(x.get("itemId"), {}).get("name", "?"),
                  "rar": I.get(x.get("itemId"), {}).get("rarity"),
                  "drop": x.get("dropChancePerc")}
                 for x in (r.get("items") or [])]
        aic.append({
            "id": uid, "n": r["username"].strip(), "lvl": r.get("level"),
            "rank": r.get("rank"), "el": [e for e in (r.get("primaryElement"), r.get("secondaryElement")) if e],
            "summon": bool(r.get("isSummon")), "arena": bool(r.get("inArena")),
            "shrine": bool(r.get("inShrines")),
            "hp": r.get("maxHealth"),
            "nin": int(r.get("ninjutsuOffence") or 0), "tai": int(r.get("taijutsuOffence") or 0),
            "spd": int(r.get("speed") or 0),
            "kit": kit, "items": items,
            "usedBy": sorted(set(used.get(uid, [])))[:4],
        })
    aic.sort(key=lambda x: (x["lvl"] or 0, x["n"].lower()))

    # ---- quests ----
    qc = []
    for q in Q.values():
        c = q.get("content") or {}
        obs = c.get("objectives") or []
        rew = c.get("reward") or {}
        locs = [{"id": o["id"], "s": o.get("sector"), "x": o.get("longitude"), "y": o.get("latitude")}
                for o in obs if o.get("sector") is not None]
        foes = sorted({x for o in obs
                       for oa in (o.get("opponentAIs") or []) + (o.get("attackers") or [])
                       for x in oa.get("ids", [])})
        qc.append({
            "id": q["id"], "n": q["name"].strip(), "type": q.get("questType"),
            "rank": q.get("questRank"), "lvl": [q.get("requiredLevel"), q.get("maxLevel")],
            "vil": V.get(q.get("requiredVillage")), "hid": bool(q.get("hidden")),
            "prereq": q.get("prerequisiteQuestId"),
            "nodes": len(obs), "tasks": dict(Counter(o["task"] for o in obs)),
            "foes": foes, "locs": locs,
            "rew": {k.replace("reward_", ""): v for k, v in rew.items()
                    if v not in (0, [], "NONE", None, False)},
        })
    qc.sort(key=lambda x: (x["type"] or "", x["n"].lower()))

    files = {
        "40_DATA_jutsu_catalog.json": jc,
        "41_DATA_item_catalog.json": ic,
        "42_DATA_ai_catalog.json": aic,
        "43_DATA_asset_catalog.json": ac,
        "47_DATA_quest_catalog.json": qc,
    }
    for name, data in files.items():
        p = os.path.join(out, name)
        with open(p, "w") as fh:
            json.dump(data, fh, separators=(",", ":"))
        print(f"{name:34} {len(data):5} records  {os.path.getsize(p)//1024:5} KB")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads"
    out = sys.argv[2] if len(sys.argv) > 2 else "/mnt/user-data/outputs"
    build(folder, out)
