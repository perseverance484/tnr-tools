"""push/45_mission_ai_self_target_fix.json - the remaining SELF-target mismatches.

Full audit of all 15 mission AI rule chains against their kits found FOUR remaining, in
four records:

  Unmarked Shadow  rule 4  Warrior's Poise      RANDOM_OPPONENT -> SELF
  Unmarked Blade   rule 4  Minor Overflow       RANDOM_OPPONENT -> SELF
  Unmarked Stray   rule 4  Fighter's Poise      RANDOM_OPPONENT -> SELF
  Faceless Blade   rule 0  Compression Barrier  RANDOM_OPPONENT -> SELF

The other eleven are clean, including Faceless Stray, which carries three SELF jutsu and
targets all three correctly. So the defect is not systemic to the tooling or to every
record - it is a handful of records where the wrong target was carried across.

No rule anywhere fires a jutsu missing from its own kit, so there is no second class of
break hiding behind this one.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITS = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788235198666.json")))
CHAINS = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788235395095.json")))

ai_by_profile = {}
for c in KITS["captures"]:
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    ai_by_profile[r["aiProfileId"]] = r

items, report = [], []
for c in CHAINS["captures"]:
    assert c.get("status") == 200
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
        assert ju, "%s rule %d fires a jutsu not in its kit" % (ai["username"], i)
        if ju["target"] == "SELF" and a.get("target") != "SELF":
            assert not rule.get("conditions"), "law 40: SELF action must carry no distance gate"
            a["target"] = "SELF"
            fixed.append((i, ju["name"]))
    if not fixed: continue
    expect = json.loads(json.dumps(prof["rules"]))
    for i, _ in fixed: expect[i]["action"]["target"] = "SELF"
    assert json.dumps(expect) == json.dumps(rules)          # only the target moved
    assert rules[-1]["action"]["type"] in ("move_towards_opponent", "use_highest_power_action")
    items.append({"entity": "ai", "slot": "edit",
                  "name": "%s [SELF target fix]" % ai["username"],
                  "targetId": ai["userId"],
                  "data": {"rules": rules, "includeDefaultRules": prof["includeDefaultRules"]}})
    report.append((ai["username"], fixed))

assert len(items) == 4, len(items)
after = [{"proc": "ai.getAiProfile", "input": {"id": p}}
         for p, a in ai_by_profile.items() if any(i["targetId"] == a["userId"] for i in items)]
assert len(after) == 4
man = {"items": items, "capture": {"after": after}}
open(os.path.join(R, "push/45_mission_ai_self_target_fix.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/45 -", len(items), "AI edits,", len(after), "read-backs")
for n, f in report: print("   %-18s %s" % (n, ", ".join("rule %d %s" % x for x in f)))
