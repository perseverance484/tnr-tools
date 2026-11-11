#!/usr/bin/env python3
"""Pull the newest captured full record (jutsu/item row with effects) for each PvP kit action from
harvests/inbox/*.json. Output: harness/pvp_turn/kit/records.json  {actionId: {record, source}}.
Usage: extract_kit.py [IDS...]   (default: dauntless pvp1 kit from state/player/dauntless/tools/ingest.py)"""
import glob, json, os, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "state/player/dauntless/tools"))
from ingest import IDS  # noqa: E402

def walk(x):
    if isinstance(x, dict):
        if isinstance(x.get("id"), str) and isinstance(x.get("effects"), list) and "name" in x:
            yield x
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)

def main():
    want = set(sys.argv[1:]) or {k for k in IDS if len(k) > 15} | {"yVNeLzxHSFkNpTPnlm7yQ"}
    best = {}
    for path in sorted(glob.glob(os.path.join(REPO, "harvests/inbox/*.json"))):
        try:
            doc = json.load(open(path))
        except Exception:
            continue
        for rec in walk(doc):
            if rec["id"] in want:
                key = rec.get("updatedAt") or ""
                if rec["id"] not in best or key >= best[rec["id"]][0]:
                    best[rec["id"]] = (key, rec, os.path.relpath(path, REPO))
    out = {k: {"record": v[1], "source": v[2], "updatedAt": v[0]} for k, v in sorted(best.items())}
    ov_path = os.path.join(REPO, "harness/pvp_turn/kit/live_overrides.json")
    if os.path.exists(ov_path):
        for k, ov in json.load(open(ov_path)).items():
            if k in out:
                out[k]["record"].update(ov)
                out[k]["updatedAt"] = ov["updatedAt"]
                out[k]["source"] += " + live_overrides.json"
    os.makedirs(os.path.join(REPO, "harness/pvp_turn/kit"), exist_ok=True)
    json.dump(out, open(os.path.join(REPO, "harness/pvp_turn/kit/records.json"), "w"), indent=1)
    for k in sorted(want):
        v = out.get(k)
        print(k, IDS.get(k, "?"), (v["record"]["name"], v["updatedAt"][:10]) if v else "MISSING")

if __name__ == "__main__":
    main()
