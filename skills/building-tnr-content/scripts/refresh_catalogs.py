#!/usr/bin/env python3
"""Regenerate trimmed working catalogs from harvester dumps.

Point this at a folder of `tnr_h1_*.json` harvests. It picks the newest dump
for each entity and writes the compact `4x_DATA_*_catalog.json` files used for
lookup, dedup, reference, and balance work.

  python3 refresh_catalogs.py /mnt/user-data/uploads /mnt/user-data/outputs

Full raw harvests remain the source record; these catalogs intentionally drop
cosmetics, timestamps, and reconstructible fields.
"""
import glob
import json
import os
import sys
from collections import Counter


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

    ic = []
    for i in I.values():
        ic.append({
            "id": i["id"], "n": i["name"].strip(), "type": i.get("itemType"),
            "rar": i.get("rarity"), "slot": i.get("slot"), "cost": i.get("cost"),
            "hid": bool(i.get("hidden")), "ap": i.get("actionCostPerc"),
            "eff": [x for x in (eff(e) for e in i.get("effects") or []) if x],
        })
    ic.sort(key=lambda x: x["n"].lower())

    ac = []
    for a in A.values():
        img = a.get("image") or ""
        ac.append({
            "id": a["id"], "n": (a.get("name") or "").strip(), "type": a.get("type"),
            "folder": a.get("folder"), "art": bool(img) and PH not in img,
            "url": img,
        })
    ac.sort(key=lambda x: (x["type"] or "", x["n"].lower()))

    used = {}
    for q in Q.values():
        for o in (q.get("content") or {}).get("objectives") or []:
            for oa in (o.get("opponentAIs") or []) + (o.get("attackers") or []):
                for x in oa.get("ids", []):
                    used.setdefault(x, []).append(q["name"].strip())

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
