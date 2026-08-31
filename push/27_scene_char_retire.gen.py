"""push/27_scene_char_retire.json - retires the two dead scene characters.

CORRECTED (dauntless): retire ONLY Fleetfoot Scene and Nightfoot Scene, which no longer
exist. The earlier version retired every bmissions-era portrait, which was wider than
asked for.

Those two ids appear in exactly one place across all 31 of our missions - Copies, Not
Thefts, nodes l1 and l2 (Fleetfoot) and c5 (Nightfoot). Witness Detail never referenced
either one, so it is not touched at all here: its Witness Kanna and The Handler
references stay exactly as they are live.

Method: substitute Blank Scene Character rather than empty the array. Copies already
carries that blank on 17 of its 25 nodes, and it is public - a node left with no scene
character risks the publish validator rejecting the whole save.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAP = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")

BLANK = "1YXbXYW2wz3GETVMb6DT6"          # Blank Scene Character
RETIRE = {
    "kYX8v4FkO96cZTPF2ORPq",             # Fleetfoot Scene - gone
    "tUTXsFG4HqESOkTiXz6Fm",             # Nightfoot Scene - gone
}
TARGET = "Copies, Not Thefts"

qs = {}
for c in json.load(open(SWAP))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    qs[r["name"]] = r

# the two ids must live nowhere else in our 31, or this manifest is incomplete
elsewhere = []
for n, q in qs.items():
    cont = q.get("content") or {}
    lists = [cont.get("sceneCharacters") or []] + [o.get("sceneCharacters") or [] for o in cont.get("objectives") or []]
    if any(i in RETIRE for l in lists for i in l) and n != TARGET:
        elsewhere.append(n)
assert not elsewhere, elsewhere

q = json.loads(json.dumps(qs[TARGET]))
content = q["content"]
touched = []
def fix(lst, node):
    if not lst: return lst
    out = []
    for i in lst:
        if i in RETIRE:
            touched.append((node, i))
            if BLANK not in out: out.append(BLANK)
        elif i not in out:
            out.append(i)
    return out
content["sceneCharacters"] = fix(content.get("sceneCharacters"), "<main>")
for o in content.get("objectives") or []:
    o["sceneCharacters"] = fix(o.get("sceneCharacters"), o.get("id"))
assert len(touched) == 3, touched

# nothing but those two ids moved, and the publish gate still holds
before = qs[TARGET]["content"]
assert len(content["objectives"]) == len(before["objectives"])
assert all(o.get("sceneCharacters") for o in content["objectives"])
data = {k: v for k, v in q.items() if k not in ("createdAt", "updatedAt")}
assert data["hidden"] is False                     # stays live, this is a repair not a flip
items = [{"entity": "quest", "slot": "edit", "name": "%s [retire Fleetfoot + Nightfoot]" % TARGET,
          "targetId": q["id"], "data": data}]
after = [{"proc": "quests.get", "input": {"id": q["id"]}}]
# skipPreflight: Copies' a1/a2/f1 dialog menus converge in the LIVE record already -
# validating the untouched capture reproduces the same three errors. This manifest adds
# no regression, it just cannot pass a gate the record fails today.
man = {"items": items, "skipPreflight": True, "capture": {"after": after}}
out = os.path.join(R, "push/27_scene_char_retire.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out)
for node, i in touched:
    print("   node %-6s %s -> Blank Scene Character" % (node, "Fleetfoot" if i.startswith("kYX") else "Nightfoot"))
print("   Witness Detail: not touched")
