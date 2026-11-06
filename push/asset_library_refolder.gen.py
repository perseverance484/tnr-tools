#!/usr/bin/env python3
"""Asset-library re-folder (RUL-2026-11-05-127): give the live Mother of Echoes and Skyglass Boss FX assets convention
folders and names, by literal id. Zero live requests to build.

    python3 push/asset_library_refolder.gen.py --capture <push/499 results bundle>
        -> push/500_asset_library_refolder.json

Input: the read-only push/499 capture (gameAsset.getAllNames per type: id, name, image, folder). Only rows whose folder
is MotherOfEchoes or SkyglassBossFX are touched. Each edit sends {name, folder} only; the builder fetch-merges the rest
(type, frames, speed, hidden, image unchanged). Ids never change, so every jutsu, AI and quest reference stays valid.

Classification is by the asset's current name (the names our generators gave them, unique in the game). A row this
script cannot classify refuses the build (no silent "Misc" folder). Do not hand-edit the output.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = 500
OLD_FOLDERS = {"MotherOfEchoes", "SkyglassBossFX"}
TYPES = ("STATIC", "ANIMATION", "SCENE_BACKGROUND", "SCENE_CHARACTER")

F = "Skyglass - Mother of Echoes - "
FOLDERS = {
    "I": F + "Act I", "II": F + "Act II", "III": F + "Act III", "floor": F + "Floors",
    "boss": F + "Entrances and Auras", "scene": F + "Scenes", "shared": F + "Shared", "bossfx": "Skyglass - Boss FX",
}

# Keyword -> group, first match wins. Matched against the lower-cased current name.
RULES = [
    (r"\(act i\)", "I"), (r"\(act ii\)", "II"), (r"\(act iii\)", "III"),
    (r"aura|rises to fight|entrance|flourish", "boss"),
    (r"seeping pool|pool|floor|linger|mended", "floor"),
    (r"refraction|facet|lancet|lucid|likeness|listening|feeler|grasp|cradle|stillness|nothing moves|hush|silence|absence|shove", "I"),
    (r"etch|recast|worn|porter|hana|tomo|tether|sweep|mend|stilling|glass turns|glass falls quiet|glasswright", "II"),
    (r"glassfall|flood|every name|glass remembers|shatterfall|held breath|breathless|long hush|saint|remainder|quiet|good impression", "III"),
    (r"lock loop|control|glint|guard|breath draw|mark|echo strike|pull|safe pane", "shared"),
]


def die(msg):
    sys.exit(f"asset_library_refolder.gen.py: {msg}")


def rows_from(bundle):
    out = {}
    for c in bundle.get("captures") or []:
        if c.get("proc") != "gameAsset.getAllNames" or not c.get("ok"):
            continue
        typ = (c.get("input") or {}).get("type")
        data = c.get("data")
        if isinstance(data, dict):
            data = data.get("rows") or data.get("data")
        if not isinstance(data, list):
            die(f"capture for {typ} carries no row list (re-run push/499 and keep the full bundle)")
        for r in data:
            out[r["id"]] = {**r, "type": typ}
    got = {r["type"] for r in out.values()}
    if not set(TYPES) <= got | {None}:
        missing = set(TYPES) - got
        if missing:
            print(f"note: no rows captured for {sorted(missing)}", file=sys.stderr)
    return out


def classify(row):
    if row["folder"] == "SkyglassBossFX":
        return "bossfx"
    if row["type"] in ("SCENE_BACKGROUND", "SCENE_CHARACTER"):
        return "scene"
    n = row["name"].lower()
    for pat, g in RULES:
        if re.search(pat, n):
            return g
    return None


def new_name(row, group):
    n = row["name"]
    if group == "bossfx":
        return n  # already "Skyglass FX - <move>"; only the folder changes
    tail = re.sub(r"^Mother of Echoes (FX|Scene Character|Scene)\s*-\s*", "", n)
    label = {"I": "MoE I", "II": "MoE II", "III": "MoE III", "floor": "MoE Floor", "boss": "MoE Boss",
             "scene": "MoE Scene", "shared": "MoE"}[group]
    return f"{label}: {tail}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--capture", required=True, help="push/499 results bundle")
    a = ap.parse_args()
    rows = rows_from(json.load(open(a.capture)))
    mine = sorted((r for r in rows.values() if r.get("folder") in OLD_FOLDERS), key=lambda r: (r["folder"], r["name"]))
    if not mine:
        die("no MotherOfEchoes / SkyglassBossFX rows in the capture")
    taken = {r["name"] for r in rows.values()}
    items, unknown, plan = [], [], {}
    for r in mine:
        g = classify(r)
        if g is None:
            unknown.append(r["name"])
            continue
        name = new_name(r, g)
        if name != r["name"] and name in taken:
            die(f"new name {name!r} collides with an existing asset")
        taken.add(name)
        data = {"folder": FOLDERS[g]}
        if name != r["name"]:
            data["name"] = name
        items.append({"entity": "asset", "slot": "edit", "targetId": r["id"], "phase": 10,
                      "name": f"{r['name']}: folder", "data": data})
        plan.setdefault(FOLDERS[g], []).append(name)
    if unknown:
        die("unclassified assets (add a RULES entry): " + "; ".join(unknown))
    m = {"_note": (f"push/{NUM}: asset-library re-folder (RUL-2026-11-05-127). {len(items)} existing assets (folders "
                   "MotherOfEchoes, SkyglassBossFX) get convention folders and names by literal id from the push/499 "
                   "capture; each edit sends only name and folder (fetch-merge keeps type, frames, speed, hidden, "
                   "image). Ids are unchanged, so no jutsu, AI or quest reference moves. Generated by "
                   "push/asset_library_refolder.gen.py; do not hand-edit."),
         "plan": {k: sorted(v) for k, v in sorted(plan.items())}, "items": items}
    p = os.path.join(ROOT, "push", f"{NUM}_asset_library_refolder.json")
    with open(p, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{os.path.relpath(p, ROOT)}: {len(items)} edits")
    for k, v in sorted(plan.items()):
        print(f"  {k}: {len(v)}")


if __name__ == "__main__":
    main()
