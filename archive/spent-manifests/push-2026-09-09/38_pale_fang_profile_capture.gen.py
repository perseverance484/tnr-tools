"""push/38_pale_fang_profile_capture.json - reads Pale Fang's aiProfile rule chain.

push/36 got the character record, which carries only `aiProfileId`, not the rules. My
manifest should have read both; it did not, so this is the missing half.

Doing the kit swap without the rules first would leave a rule naming a jutsu the AI no
longer owns. The engine falls through an unexecutable rule (law 41b) rather than crashing,
so it would not be fatal - but Pale Fang would quietly lose a rule slot, which is the same
class of silent failure as the one being fixed.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = json.load(open(os.path.join(R, "harvests/inbox/tnr_results_1788196013904.json")))
ai = b["captures"][0]["data"]
pid = ai["aiProfileId"]
assert pid, "Pale Fang has no aiProfileId"
man = {"capture": {"before": [{"proc": "ai.getAiProfile", "input": {"id": pid}}]}, "items": []}
open(os.path.join(R, "push/38_pale_fang_profile_capture.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/38 - reads aiProfile", pid)
