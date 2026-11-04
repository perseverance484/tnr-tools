#!/usr/bin/env python3
"""Pass 5 (RUL-2026-11-04-113) edit rows: the eruption effect each live Mother of Echoes jutsu needs.

    python3 harness/skyglass_wreck_sim/tools/moe_eruption_rows.py <spec.json> <440 bundle> <463 bundle> > rows.json

Compares the pass-4 spec as built (dd7e33ab, what push/440 created) with the given spec and lists every jutsu whose
effects changed: live id (from push/440's results bundle), the changed effect index and its old/new fields, and the
bosses holding it (push/463's bundle) for the law 18 unequip -> edit -> re-equip. Zero live requests.
"""
import json, subprocess, sys

BUILT = "dd7e33ab9abfc96ae1630177ea1bc386729b2c8f"
spec_new = json.load(open(sys.argv[1]))
spec_old = json.loads(subprocess.check_output(["git", "show", f"{BUILT}:harness/skyglass_wreck_sim/mother_of_echoes_spec.json"]))
sid = lambda h: "sg440_" + h[4:].replace("-", "_")
ids = {}
for p in sys.argv[2:]:
    for e in json.load(open(p))["entries"]:
        if e.get("state") == "ok" and e.get("id"):
            ids[e["srcId"]] = e["id"]
old = {j["id"]: j["record"] for j in spec_old["jutsu"]}
rows = []
for j in spec_new["jutsu"]:
    o, n = old[j["id"]], j["record"]
    for i, (eo, en) in enumerate(zip(o["effects"], n["effects"])):
        if eo == en:
            continue
        diff = {k: [eo.get(k), en.get(k)] for k in sorted(set(eo) | set(en)) if eo.get(k) != en.get(k)}
        holders = [a["id"] for a in spec_new["ais"] if j["id"] in a["create"]["jutsus"]]
        rows.append({"jutsu": n["name"], "srcId": sid(j["id"]), "liveId": ids.get(sid(j["id"])), "effectIndex": i,
                     "changes": diff, "holders": [{"srcId": sid(h), "liveId": ids.get(sid(h))} for h in holders]})
missing = [r["srcId"] for r in rows if not r["liveId"]] + [h["srcId"] for r in rows for h in r["holders"] if not h["liveId"]]
json.dump({"builtFrom": BUILT, "rows": rows, "missingIds": sorted(set(missing))}, sys.stdout, indent=1)
print()
