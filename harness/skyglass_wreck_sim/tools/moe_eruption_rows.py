#!/usr/bin/env python3
"""Pass 5 (RUL-2026-11-04-113) / pass 6 edit rows: every change each live Mother of Echoes jutsu needs vs the built spec.

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
newJutsu = []  # pass 6: records the built spec does not have (e.g. the follow-the-player marks) are creates, not edits
for j in spec_new["jutsu"]:
    if j["id"] not in old:
        newJutsu.append({"jutsu": j["record"]["name"], "srcId": sid(j["id"])})
        continue
    o, n = old[j["id"]], j["record"]
    holders = [a["id"] for a in spec_new["ais"] if j["id"] in a["create"]["jutsus"]]
    hold = [{"srcId": sid(h), "liveId": ids.get(sid(h))} for h in holders]
    # Pass 6: record-level fields (target CHARACTER for the Act II Recasts, patterns, cooldowns) and effects appended
    # or removed (the eruption debuff, the Lancet ramp) are edits too; zip() alone dropped them.
    top = {k: [o.get(k), n.get(k)] for k in sorted(set(o) | set(n)) if k != "effects" and o.get(k) != n.get(k)}
    if top:
        rows.append({"jutsu": n["name"], "srcId": sid(j["id"]), "liveId": ids.get(sid(j["id"])), "effectIndex": None, "changes": top, "holders": hold})
    eo_all, en_all = o["effects"], n["effects"]
    for i in range(max(len(eo_all), len(en_all))):
        eo = eo_all[i] if i < len(eo_all) else None
        en = en_all[i] if i < len(en_all) else None
        if eo == en:
            continue
        if eo is None or en is None:
            diff = {"added" if eo is None else "removed": en if eo is None else eo}
        else:
            diff = {k: [eo.get(k), en.get(k)] for k in sorted(set(eo) | set(en)) if eo.get(k) != en.get(k)}
        rows.append({"jutsu": n["name"], "srcId": sid(j["id"]), "liveId": ids.get(sid(j["id"])), "effectIndex": i, "changes": diff, "holders": hold})
missing = [r["srcId"] for r in rows if not r["liveId"]] + [h["srcId"] for r in rows for h in r["holders"] if not h["liveId"]]
json.dump({"builtFrom": BUILT, "rows": rows, "newJutsu": newJutsu, "missingIds": sorted(set(missing))}, sys.stdout, indent=1)
print()
