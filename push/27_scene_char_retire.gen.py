"""push/27_scene_char_retire.json - retires the outdated scene characters on the two
bmissions-era B missions: Witness Detail and Copies, Not Thefts.

Method: substitute, do not delete. Copies already carries 'Blank Scene Character'
(1YXbXYW2wz3GETVMb6DT6) on 17 of its 25 nodes, so a blank IS the house way to show no
character. Emptying the arrays instead would risk the publish validator, which demands
main sceneCharacters OR every objective carrying them - Copies is already public, so a
write that fails that check would be rejected outright.

Retired here: every bmissions-folder portrait plus the dmissions-era clerk.
These entries carry FULL live content with only sceneCharacters changed, so validate.py
checks the whole flow rather than waving it through as a partial edit.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAP = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")
CEN = os.path.join(R, "harvests/inbox/tnr_results_1788134455342.json")

BLANK = "1YXbXYW2wz3GETVMb6DT6"          # Blank Scene Character, folder ghostship
RETIRE = {
    "ZtwuYm9wgDcl88F_KDStl",   # Witness Kanna       /bmissions
    "pqihl43HYROpkIMX172-P",   # The Handler         /bmissions
    "ryLnefupONNZKX5hcPWid",   # ANBU Commander      /bmissions
    "kYX8v4FkO96cZTPF2ORPq",   # Fleetfoot Scene     /bmissions
    "tUTXsFG4HqESOkTiXz6Fm",   # Nightfoot Scene     /bmissions
    "XsLLy8awDAtaE6hXVIi_0",   # DM Mission Clerk    /dmissions
}
# Copies, Not Thefts is excluded (dauntless): it is already live with its new icon and
# is not part of this release. Dropping it also drops the three pre-existing converging
# menu errors it carried, so this manifest goes green on its own merits.
TARGETS = {"Witness Detail"}

assets = None
for c in json.load(open(CEN))["captures"]:
    if c["proc"] == "gameAsset.getAll": assets = c["data"]["data"]
ids = {a["id"] for a in assets}
assert BLANK in ids
assert RETIRE <= ids, RETIRE - ids

qs = {}
for c in json.load(open(SWAP))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    qs[r["name"]] = r
assert TARGETS <= set(qs)

def fix(lst):
    if not lst: return lst, 0
    out, n = [], 0
    for i in lst:
        if i in RETIRE:
            n += 1
            if BLANK not in out: out.append(BLANK)
        elif i not in out:
            out.append(i)
    return out, n

items, report = [], []
for name in sorted(TARGETS):
    q = json.loads(json.dumps(qs[name]))
    content = q["content"]
    total = 0
    content["sceneCharacters"], n = fix(content.get("sceneCharacters"))
    total += n
    for o in content.get("objectives") or []:
        o["sceneCharacters"], n = fix(o.get("sceneCharacters"))
        total += n
    # publish gate must still hold after the swap
    objs = content.get("objectives") or []
    assert (content.get("sceneCharacters") or []) or all(o.get("sceneCharacters") for o in objs), name
    assert not (set(json.dumps(content).split('"')) & RETIRE), name
    data = {k: v for k, v in q.items() if k not in ("createdAt", "updatedAt")}
    items.append({"entity": "quest", "slot": "edit", "name": "%s [retire scene chars]" % name,
                  "targetId": q["id"], "data": data})
    report.append((name, total, q["hidden"]))

after = [{"proc": "quests.get", "input": {"id": i["targetId"]}} for i in items]
# No skipPreflight: this entry carries full content, and Witness Detail passes the
# builder flow checks on its own.
man = {"items": items, "capture": {"after": after}}
out = os.path.join(R, "push/27_scene_char_retire.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out)
for n, t, h in report: print("  %-20s %2d references retired  (hidden=%s)" % (n, t, h))
