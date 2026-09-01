"""push/43_all_mission_ai_audit.json - reads every AI used by our 31 missions.

The SELF-target mismatch turned out to be four rules across three of the four A-rank
bosses, with Faceless Shadow as the correctly-authored control. dauntless reports the same
symptom across the mission AIs generally, so this audits all of them rather than chasing
reports one at a time.

15 distinct opponent ids, extracted from the opponentAIs arrays of our 31 quests. Four are
already captured (the A-rank set) but are re-read so the whole audit is one snapshot.

This is the kit half. aiProfileId only comes back from these reads, so the rule chains need
a second manifest - same two-step as the A-rank audit.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SW = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")
qs = []
for c in json.load(open(SW))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    qs.append(r)
assert len(qs) == 31
ids = set()
for q in qs:
    for o in (q.get("content") or {}).get("objectives") or []:
        for grp in (o.get("opponentAIs") or []):
            ids.update(grp.get("ids") or [])
assert len(ids) == 15, len(ids)
reads = [{"proc": "profile.getAi", "input": {"userId": i}} for i in sorted(ids)]
man = {"capture": {"before": reads}, "items": []}
open(os.path.join(R, "push/43_all_mission_ai_audit.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/43 -", len(reads), "reads, 0 mutations")
