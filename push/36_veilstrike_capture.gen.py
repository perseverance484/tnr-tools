"""push/36_veilstrike_capture.json - reads the live Veilstrike record.

The pool registry (32b B24) is a 2026-08-26 snapshot generated from
32_REGISTRY_shared_ai_pool.md, not a live read, so it cannot settle what the record says
today. This reads it.
"""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pool = json.load(open(os.path.join(R, "32b_DATA_pool.json")))
rec = pool["records"]["B24"]
assert rec["name"] == "Veilstrike"
man = {"capture": {"before": [{"proc": "jutsu.get", "input": {"id": rec["id"]}}]}, "items": []}
open(os.path.join(R, "push/36_veilstrike_capture.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/36 - reads Veilstrike", rec["id"])
print("registry says: target", rec["target"], "| range", rec["range"], "| gate", rec["gate"],
      "| ap", rec["ap"], "| cooldown", rec["cooldown"])
print("effects:", rec["effects"])
