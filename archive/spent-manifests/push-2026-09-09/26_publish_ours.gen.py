"""push/26_publish_ours.json - the publish half: flips our finished missions public.

Held for the content admin's go-ahead. dauntless publishes, not Claude.

Scope: the 11 of our 31 that are still hidden AND clear the publish audit. 19 of the 31
are already public and are not touched. One White Ear is deliberately EXCLUDED - it is
questType event, and validate.py errors on three of its dialog menus (d1/d2/d3 converge,
every option leading to the same node), so it reads as a stub rather than finished work.

Each entry patches `hidden` only; the builder fetch-merges the live record, so content,
rewards and flow are untouched - the same shape as the icon swap, which landed on all 31
with a byte-identical content diff.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAP = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")

b = json.load(open(SWAP))
qs = []
for c in b["captures"]:
    if c.get("proc") != "quests.get": continue
    assert c.get("status") == 200
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    qs.append(r)
assert len(qs) == 31

# The release is the ten Forsworn missions only (dauntless). One White Ear is earmarked
# with the stubs - questType event, and d1/d2/d3 are converging dialog menus. Witness
# Detail is a bmissions-era B mission, not part of the Forsworn wave, and stays hidden.
EXCLUDE = {"One White Ear", "Witness Detail"}
hidden = [q for q in qs if q["hidden"]]
assert len(hidden) == 12, len(hidden)
pub = [q for q in hidden if q["name"] not in EXCLUDE]
assert len(pub) == 10, len(pub)

for q in pub:                        # publish gate: main sceneCharacters OR all objectives carry them
    c = q.get("content") or {}
    objs = c.get("objectives") or []
    assert objs, q["name"]
    assert (c.get("sceneCharacters") or []) or all(o.get("sceneCharacters") for o in objs), q["name"]

items = [{"entity": "quest", "slot": "edit",
          "name": "%s [publish %s]" % (q["name"], q["questRank"]),
          "targetId": q["id"], "data": {"hidden": False}}
         for q in sorted(pub, key=lambda q: (q["questRank"], q["name"]))]
after = [{"proc": "quests.get", "input": {"id": i["targetId"]}} for i in items]
man = {"items": items, "skipPreflight": True, "capture": {"after": after}}
out = os.path.join(R, "push/26_publish_ours.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out, "-", len(items), "unhides,", len(after), "read-backs")
for i in items: print("  ", i["targetId"], i["name"])
