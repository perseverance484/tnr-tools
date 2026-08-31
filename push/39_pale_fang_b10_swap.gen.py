"""push/39_pale_fang_b10_swap.json - Veilstrike out, Sovereign Ascendance (B10) in.

Composed against the two live captures, not the registry:
  tnr_results_1788196013904  profile.getAi   -> the kit (5 jutsus, all equipped)
  tnr_results_1788203892632  ai.getAiProfile -> the 6-rule chain

THE FAULT, confirmed from the rule chain: rule 1 is Veilstrike with NO conditions - an
unconditional opener. Law 75 makes stealth inert on the cast round; it goes live the
following round, where law 62 blocks attacking. Rules 2-5 are all attacks, so on that round
every one of them is invalid and the chain falls through to rule 6, move_towards_opponent.
Pale Fang spends the round the +60% buff finally exists walking at you. That is the bug on
screen, and it is not a targeting error - target SELF with no distance condition is exactly
what law 40 requires.

B10 is the like-for-like: self stance, same 40 AP, no stealth, so the buff round is a
fighting round. It costs the heal 25 and two rounds of cooldown.

Both edits ride ONE entry, because rules live on the AI record (ai.md: there is no separate
profile entity to author). Literal live ids only - an unresolvable id in `jutsus` is stripped
server-side and the row still reports ok.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788196013904.json")))
PR = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788203892632.json")))
POOL = json.load(open(os.path.join(R, "32b_DATA_pool.json")))["records"]

OLD, NEW = POOL["B24"], POOL["B10"]
assert OLD["name"] == "Veilstrike" and NEW["name"] == "Sovereign Ascendance"
assert NEW["target"] == "self" and NEW["ap"] == OLD["ap"] == 40
assert not any("stealth" in e for e in NEW["effects"])

ai = AI["captures"][0]["data"]
prof = PR["captures"][0]["data"]
assert ai["username"] == "Pale Fang" and prof["userId"] == ai["userId"]
assert prof["includeDefaultRules"] is False

kit = [j["jutsuId"] for j in ai["jutsus"]]
assert OLD["id"] in kit and NEW["id"] not in kit
new_kit = [NEW["id"] if j == OLD["id"] else j for j in kit]      # same slot, same order
assert len(new_kit) == len(kit) == 5 and len(set(new_kit)) == 5

rules = json.loads(json.dumps(prof["rules"]))
hits = 0
for r in rules:
    if r.get("action", {}).get("jutsuId") == OLD["id"]:
        r["action"]["jutsuId"] = NEW["id"]
        # SELF-target jutsu take no distance gate (law 40); rule 1 correctly has none
        assert not r.get("conditions"), "a gate on a SELF jutsu - review before shipping"
        hits += 1
assert hits == 1, hits
assert rules[-1]["action"]["type"] == "move_towards_opponent" and not rules[-1].get("conditions"), \
    "law 41 / lint L24: the chain must end in an always-fireable rule"
assert OLD["id"] not in json.dumps({"kit": new_kit, "rules": rules})

items = [{"entity": "ai", "slot": "edit", "name": "Pale Fang [Veilstrike -> Sovereign Ascendance]",
          "targetId": ai["userId"],
          "data": {"jutsus": new_kit, "rules": rules, "includeDefaultRules": False}}]
after = [{"proc": "profile.getAi", "input": {"userId": ai["userId"]}},
         {"proc": "ai.getAiProfile", "input": {"id": prof["id"]}}]
man = {"items": items, "capture": {"after": after}}
open(os.path.join(R, "push/39_pale_fang_b10_swap.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/39")
print("  kit :", " -> ".join([OLD["name"], NEW["name"]]), "| slot 5 of 5, order preserved")
print("  rule: rule 1 (unconditional opener) repointed, 1 of 6 rules touched")
print("  new id", NEW["id"], "| cd", NEW["cooldown"], "| effects", NEW["effects"])
