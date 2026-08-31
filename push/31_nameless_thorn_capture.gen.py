"""push/31_nameless_thorn_capture.json - reads the quest for the prose pass.

"The Nameless mission" is read as **The Nameless Thorn**, qn36dRZfTnru7oSgjDElO - the only
Nameless record in the quest table, questType `story`, and it matches the `NamelessThorn`
asset folder (8 assets). It has never been captured, so its prose cannot be worked on yet.

Old Ghost needs no read - its full record is already in tnr_results_1788135094828.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = os.path.join(R, "harvests/inbox/tnr_results_1788110429856.json")
for c in json.load(open(NAMES))["captures"]:
    if c.get("proc") == "quests.getAllNames":
        rows = c["data"]["data"] if isinstance(c["data"], dict) else c["data"]
hit = [r for r in rows if r["name"] == "The Nameless Thorn"]
assert len(hit) == 1, hit
man = {"capture": {"before": [{"proc": "quests.get", "input": {"id": hit[0]["id"]}}]}, "items": []}
open(os.path.join(R, "push/31_nameless_thorn_capture.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/31 - reads", hit[0]["name"], hit[0]["id"], "(questType %s)" % hit[0]["questType"])
