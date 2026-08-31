"""push/36_pale_fang_capture.json - reads Pale Fang before touching its kit.

Replacing Veilstrike is two edits, not one: the jutsu comes off Pale Fang's kit, AND the
aiProfile rule that names it by id has to change with it, or the rule points at a jutsu the
AI no longer owns. Neither can be written from the registry snapshot - the live kit and the
live rule chain have never been captured.

Reads Pale Fang and the live Veilstrike record (to confirm the effect list the diagnosis
rests on is still what the 2026-08-26 registry says).
"""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(R, "answers/names_ai.json")).read()
m = re.search(r'\["([A-Za-z0-9_-]{18,24})","Pale Fang"', s)
assert m, "Pale Fang not in the AI name index"
pale = m.group(1)
veil = json.load(open(os.path.join(R, "32b_DATA_pool.json")))["records"]["B24"]["id"]
man = {"capture": {"before": [
    {"proc": "profile.getAi", "input": {"userId": pale}},
    {"proc": "jutsu.get", "input": {"id": veil}},
]}, "items": []}
open(os.path.join(R, "push/36_pale_fang_capture.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/36 - Pale Fang", pale, "+ Veilstrike", veil)
