"""push/42_boss_self_target_fix.json - fixes the SELF-target mismatch on the A-rank bosses.

THE PATTERN, from the four captured rule chains:

  Faceless Shadow  rule 0  Hushed Hours (SELF)          action target SELF            <- correct
  Winter Crow      rule 0  Surging Overflow (SELF)      action target RANDOM_OPPONENT <- broken
  Old Ghost        rule 0  Apex Hunger (SELF)           action target RANDOM_OPPONENT <- broken
  Old Ghost        rule 5  Second Wind (SELF)           action target RANDOM_OPPONENT <- broken
  Pale Fang        rule 0  Sovereign Ascendance (SELF)  action target RANDOM_OPPONENT <- broken

Faceless Shadow is the control: the one boss whose self-buff rule was authored with
target SELF is the one that was built correctly, and the other three all carry the same
copy-paste of RANDOM_OPPONENT onto a jutsu that cannot be aimed at an opponent.

Every OTHER_USER jutsu in all four chains is already correct - right target, and a
distance gate at range + 1 per law 40. Nothing else is touched. Faceless Shadow gets no
entry at all.

Rules ride on the AI record (ai.md), so this is three `ai` edits carrying the full rules
array with one field changed per broken rule.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITS = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788208842873.json")))
CHAINS = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788208954502.json")))

ai_by_profile = {}
for c in KITS["captures"]:
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    ai_by_profile[r["aiProfileId"]] = r

items, report = [], []
for c in CHAINS["captures"]:
    prof = c["data"]
    if isinstance(prof, dict) and "data" in prof: prof = prof["data"]
    if isinstance(prof, list): prof = prof[0]
    ai = ai_by_profile[prof["id"]]
    kit = {j["jutsuId"]: j["jutsu"] for j in ai["jutsus"]}
    rules = json.loads(json.dumps(prof["rules"]))
    fixed = []
    for i, rule in enumerate(rules):
        a = rule["action"]
        jid = a.get("jutsuId")
        if not jid: continue
        ju = kit.get(jid)
        assert ju, "%s rule %d fires a jutsu not in the kit" % (ai["username"], i)
        if ju["target"] == "SELF" and a.get("target") != "SELF":
            a["target"] = "SELF"
            assert not rule.get("conditions"), "law 40: a SELF action must carry no distance gate"
            fixed.append((i, ju["name"]))
    if not fixed:
        report.append((ai["username"], "no change - already correct"))
        continue
    # nothing but the target moved
    before = json.loads(json.dumps(prof["rules"]))
    for i, _ in fixed: before[i]["action"]["target"] = "SELF"
    assert json.dumps(before) == json.dumps(rules)
    assert rules[-1]["action"]["type"] in ("move_towards_opponent", "use_highest_power_action")
    items.append({"entity": "ai", "slot": "edit",
                  "name": "%s [SELF target fix]" % ai["username"],
                  "targetId": ai["userId"],
                  "data": {"rules": rules, "includeDefaultRules": prof["includeDefaultRules"]}})
    report.append((ai["username"], ", ".join("rule %d %s" % f for f in fixed)))

assert len(items) == 3, len(items)
assert not any(i["name"].startswith("Faceless Shadow") for i in items)
after = [{"proc": "ai.getAiProfile", "input": {"id": p}}
         for p, a in ai_by_profile.items() if any(i["targetId"] == a["userId"] for i in items)]
man = {"items": items, "capture": {"after": after}}
open(os.path.join(R, "push/42_boss_self_target_fix.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/42 -", len(items), "AI edits,", len(after), "read-backs")
for n, w in report: print("   %-16s %s" % (n, w))
