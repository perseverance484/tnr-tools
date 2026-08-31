"""push/40_a_rank_boss_audit.json - reads every A-rank boss and its rule chain.

"Action no longer possible" needs the kit AND the rules side by side for each boss: the
check is whether a rule fires a jutsu whose own `target` disagrees with the rule action's
`target`. Pale Fang is already one confirmed instance - rule 1 fires Veilstrike, a SELF
jutsu, with action target RANDOM_OPPONENT.

Note ai.md's diagnostic order: a severed equip link (law 18, jutsu edited while equipped)
produces the SAME log signature as an inert rule. The getAi read carries `equipped` per kit
entry, so both hypotheses are testable from this one bundle.

AI ids extracted from the opponentAIs arrays of our own A-rank quests, never transcribed.
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
ids = {}
for q in qs:
    if q["questRank"] != "A": continue
    for o in (q.get("content") or {}).get("objectives") or []:
        for grp in (o.get("opponentAIs") or []):
            for i in (grp.get("ids") or []):
                ids.setdefault(i, set()).add(q["name"])
assert ids, "no A-rank opponents found"
reads = []
for i in sorted(ids):
    reads.append({"proc": "profile.getAi", "input": {"userId": i}})
man = {"capture": {"before": reads}, "items": []}
open(os.path.join(R, "push/40_a_rank_boss_audit.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/40 -", len(reads), "reads, 0 mutations")
for i in sorted(ids): print("  ", i, "|", ", ".join(sorted(ids[i])))
print()
print("NOTE: aiProfileId is only known after these land, so the rule chains need a second")
print("manifest. Not folding a guess into this one.")
