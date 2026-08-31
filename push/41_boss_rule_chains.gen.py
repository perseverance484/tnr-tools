"""push/41_boss_rule_chains.json - reads all four A-rank boss rule chains.

Profile ids come from the push/40 bundle, so no id is guessed.

What this settles: every one of the four bosses carries at least one SELF-target jutsu
(Hushed Hours, Surging Overflow, Second Wind, Apex Hunger, Sovereign Ascendance). If each
is fired by a rule whose action target is an opponent - as Pale Fang's rule 0 already is -
that is the pattern behind "action no longer possible" and it is one fix repeated four times.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788208842873.json")))
reads, seen = [], []
for c in B["captures"]:
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    pid = r.get("aiProfileId")
    assert pid, "%s has no aiProfileId" % r.get("username")
    reads.append({"proc": "ai.getAiProfile", "input": {"id": pid}})
    seen.append((r["username"], pid))
assert len(reads) == 4
man = {"capture": {"before": reads}, "items": []}
open(os.path.join(R, "push/41_boss_rule_chains.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/41 -", len(reads), "reads, 0 mutations")
for n, p in seen: print("  ", n, p)
