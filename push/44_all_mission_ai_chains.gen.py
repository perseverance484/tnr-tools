"""push/44_all_mission_ai_chains.json - the rule chains for all 15 mission AIs.

Profile ids taken from the push/43 bundle. Kits are clean: 15/15 read 200, every kit entry
equipped, so law 18's severed-link cause is out across the whole set and the only remaining
candidate is the rule/jutsu target mismatch.

12 of the 15 carry at least one SELF-target jutsu, so up to 12 records can hold the defect:

  Faceless Stray   Veilstep, Minor Overflow, Fighter's Poise   (three)
  Old Ghost        Second Wind, Apex Hunger                    (already fixed)
  Winter Crow      Surging Overflow                            (already fixed)
  Pale Fang        Sovereign Ascendance                        (already fixed)
  Faceless Shadow  Hushed Hours                                (was correct)
  Unmarked Shadow  Warrior's Poise
  Unmarked Blade   Minor Overflow
  Unmarked Stray   Fighter's Poise
  Faceless Blade   Compression Barrier
  KX: Iron Aberration / KGK Rogue  Sharpened Focus
  KGK Obelisk      Obelisk Overload

All 15 are read, not just the 12, so the three jutsu-less records are covered by the same
snapshot.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788235198666.json")))
seen, reads = [], []
for c in B["captures"]:
    assert c.get("status") == 200
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    pid = r.get("aiProfileId")
    assert pid, "%s has no aiProfileId" % r.get("username")
    reads.append({"proc": "ai.getAiProfile", "input": {"id": pid}})
    seen.append(r["username"])
assert len(reads) == 15 and len({json.dumps(x) for x in reads}) == 15
man = {"capture": {"before": reads}, "items": []}
open(os.path.join(R, "push/44_all_mission_ai_chains.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/44 -", len(reads), "reads, 0 mutations")
