"""push/30_repair_freedoms_scouting.json - repairs collateral loss from the hide wave.

Writing `hidden:true` to Freedom's Scouting Party round-tripped the whole record through
the builder's fetch-merge, and the server normalized its sparse legacy fields to schema
defaults. Almost all of that was harmless (null -> 0, null -> [], null -> "NONE"), but
three real values were lost:

  objectives[0].opponent_name    "Forbidden Sorcerer" -> null
  objectives[0].attackers_chance  0 -> null
  objectives[1].attackers_chance  0 -> null

This restores those three from the pre-hide census. Base is the CURRENT post-hide record,
so the normalization stands and only the lost values are put back - it stays hidden.

None of the other 25 hides lost anything; a full value->null scan across all 26 found
these three and nothing else.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(R, "harvests/inbox/tnr_results_1788136356379.json")
POST = os.path.join(R, "harvests/inbox/tnr_results_1788136975366.json")
NAME = "Freedom's Scouting Party"

pre = {r["name"].strip(): r for c in json.load(open(PRE))["captures"] for r in c["data"]["data"]}
post = {}
for c in json.load(open(POST))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    post[r["name"].strip()] = r
a, b = pre[NAME], json.loads(json.dumps(post[NAME]))
assert a["id"] == b["id"] and b["hidden"] is True

RESTORE = [(0, "opponent_name"), (0, "attackers_chance"), (1, "attackers_chance")]
done = []
for idx, field in RESTORE:
    want = a["content"]["objectives"][idx][field]
    assert b["content"]["objectives"][idx].get(field) is None, (idx, field)
    assert a["content"]["objectives"][idx]["id"] == b["content"]["objectives"][idx]["id"]
    b["content"]["objectives"][idx][field] = want
    done.append((b["content"]["objectives"][idx]["id"], field, want))

data = {k: v for k, v in b.items() if k not in ("createdAt", "updatedAt", "village")}
assert data["hidden"] is True
items = [{"entity": "quest", "slot": "edit", "name": "%s [restore lost fields]" % NAME,
          "targetId": b["id"], "data": data}]
man = {"items": items, "skipPreflight": True,
       "capture": {"after": [{"proc": "quests.get", "input": {"id": b["id"]}}]}}
out = os.path.join(R, "push/30_repair_freedoms_scouting.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out)
for n, f, v in done: print("   %s.%s <- %s" % (n, f, json.dumps(v)))
