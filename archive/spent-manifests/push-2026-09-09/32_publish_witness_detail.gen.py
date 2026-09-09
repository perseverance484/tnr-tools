"""push/32_publish_witness_detail.json - finalizes the release of Witness Detail.

Held back from the Forsworn release as a bmissions-era B mission; dauntless now rules it
ships. Patches `hidden` only, with a read-back.

Publish gate checked against the live record before building: content.sceneCharacters is
non-empty (Witness Kanna), so the "must have scene characters" rejection cannot fire. Its
Fleetfoot/Nightfoot problem never applied - those ids were only ever in Copies.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAP = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")
for c in json.load(open(SWAP))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    if r["name"] == "Witness Detail": q = r
assert q["hidden"] is True and q["questRank"] == "B"
content = q["content"]
objs = content.get("objectives") or []
assert (content.get("sceneCharacters") or []) or all(o.get("sceneCharacters") for o in objs)
dead = {"kYX8v4FkO96cZTPF2ORPq", "tUTXsFG4HqESOkTiXz6Fm"}
allsc = set(content.get("sceneCharacters") or [])
for o in objs: allsc |= set(o.get("sceneCharacters") or [])
assert not (allsc & dead), allsc & dead
man = {"items": [{"entity": "quest", "slot": "edit", "name": "Witness Detail [publish B]",
                  "targetId": q["id"], "data": {"hidden": False}}],
       "skipPreflight": True,
       "capture": {"after": [{"proc": "quests.get", "input": {"id": q["id"]}}]}}
open(os.path.join(R, "push/32_publish_witness_detail.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/32 - 1 unhide,", len(objs), "objectives, scene chars:", sorted(allsc))
