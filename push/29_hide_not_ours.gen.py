"""push/29_hide_not_ours.json - hides the missions outside our set.

Built from the full mission census (tnr_results_1788136356379), not from names.

The census returned 61 missions: 30 ours, 31 not. Of those 31, five are ALREADY hidden
and are left alone entirely - one empty "New Quest -" shell, and four S-rank records
carrying 49 objectives each (Hungry Torii, Thread Hunt, Shrine Ash, Hag Lullaby, all
2026-07-03). Those four are somebody's substantial work in progress, already out of
sight; there is no reason to write to them.

That leaves 26 public missions, every one of them a 1-or-2 objective stub from 2024 or
mid-2025. Those are the hide list.

Each entry patches `hidden` only and the builder fetch-merges the live record, so content
is preserved for the upgrade-or-retire pass later.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(R, "harvests/inbox/tnr_results_1788136356379.json")
SWAP = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")

rows = [r for c in json.load(open(CENSUS))["captures"] for r in c["data"]["data"]]
assert len(rows) == 61 and len({r["id"] for r in rows}) == 61

ours = set()
for c in json.load(open(SWAP))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    ours.add(r["id"])
assert len(ours) == 31

other = [r for r in rows if r["id"] not in ours]
assert len(other) == 31, len(other)
targets = [r for r in other if not r["hidden"]]
assert len(targets) == 26, len(targets)
assert all(len((r.get("content") or {}).get("objectives") or []) <= 2 for r in targets), \
    "a target with more than 2 objectives is not a stub - stop and review"
assert not (ours & {r["id"] for r in targets})

items = [{"entity": "quest", "slot": "edit",
          "name": "%s [hide %s]" % (r["name"].strip(), r["questRank"]),
          "targetId": r["id"], "data": {"hidden": True}}
         for r in sorted(targets, key=lambda r: (r["questRank"], r["name"]))]
after = [{"proc": "quests.get", "input": {"id": i["targetId"]}} for i in items]
# skipPreflight: partial quest edit, same builder qBad gap as the icon swap and the publish
man = {"items": items, "skipPreflight": True, "capture": {"after": after}}
out = os.path.join(R, "push/29_hide_not_ours.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out, "-", len(items), "hides,", len(after), "read-backs")
print("left alone (already hidden):")
for r in other:
    if r["hidden"]:
        print("   %-28s %s  %d objectives" % (r["name"][:28], r["questRank"],
              len((r.get("content") or {}).get("objectives") or [])))
