#!/usr/bin/env python3
"""Synthetic self-test for consumer_audit.py: CLEAR, CONSUMERS and INCOMPLETE must each be reached,
and an outside holder of an RUL-010 excluded (unedited) jutsu must not block CLEAR.

    python3 harness/ghost_ship_legacy_baseline/consumer_audit_selftest.py

Builds fake census results (no game data) in a temporary root holding copies of the census
manifests, the baseline and the kit packet. Exit 0 only if every case yields its expected verdict.
"""
import glob
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("consumer_audit", os.path.join(HERE, "consumer_audit.py"))
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)
REPO = ca.ROOT


def main():
    ids, _ = ca.census_ids()
    ids = sorted(ids)
    ghost = sorted(e["aiId"] for e in json.load(open(os.path.join(REPO, ca.KIT)))["entities"])
    legacy = json.load(open(os.path.join(REPO, ca.BASELINE)))["records"][0]["targetId"]
    other = next(i for i in ids if i not in ghost)
    ghost_free = [i for i in ids if i not in ghost and i != other][0]
    excl = sorted(json.load(open(os.path.join(REPO, ca.EDIT_SCOPE)))["excluded"])[0]
    ok = True
    with tempfile.TemporaryDirectory() as root:
        for rel in [ca.BASELINE, ca.KIT, ca.EDIT_SCOPE] + [os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, ca.CENSUS_GLOB))]:
            os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
            shutil.copy(os.path.join(REPO, rel), os.path.join(root, rel))
        ca.ROOT = root

        def bundle(name, body_for):
            caps = [{"proc": "profile.getAi", "input": {"userId": u}, "persist": "full", "ok": True, "data": body_for(u)} for u in ids]
            caps = [c for c in caps if c["data"] != "SKIP"]
            rel = f"harvests/inbox/{name}.json"
            os.makedirs(os.path.join(root, "harvests/inbox"), exist_ok=True)
            json.dump({"at": "synthetic", "captures": caps}, open(os.path.join(root, rel), "w"))
            return rel

        dead = set(ids[-(len(ids) - ca.LIVE_NON_ELDER):])  # 13 stale seed ids read back null

        def base(u):
            if u in dead:
                return None
            kit = [{"jutsuId": legacy, "equipped": True}] if u in ghost else []
            return {"userId": u, "username": u, "rank": "JONIN", "jutsus": kit}

        cases = [
            ("clear", base, "CLEAR"),
            ("consumer", lambda u: {**base(u), "jutsus": [{"jutsuId": legacy, "equipped": True}]} if u == other else base(u), "CONSUMERS"),
            ("excluded jutsu held outside", lambda u: {**base(u), "jutsus": [{"jutsuId": excl, "equipped": True}]} if u == other else base(u), "CLEAR"),
            ("missing", lambda u: "SKIP" if u == other else base(u), "INCOMPLETE"),
            ("short", lambda u: None if u == other else base(u), "INCOMPLETE"),
            ("short, residual accepted", lambda u: None if u == other else base(u), "ACCEPTED_RESIDUAL", "RUL-TEST"),
            ("short with outside holder, residual accepted", lambda u: None if u == ghost_free else ({**base(u), "jutsus": [{"jutsuId": legacy, "equipped": True}]} if u == other else base(u)), "CONSUMERS", "RUL-TEST"),
            ("missing read, residual accepted", lambda u: "SKIP" if u == other else base(u), "INCOMPLETE", "RUL-TEST"),
        ]
        for name, fn, want, *acc in cases:
            got = ca.audit([bundle(name, fn)], None, acc[0] if acc else None)["verdict"]
            good = got == want
            ok &= good
            print(f"{'PASS' if good else 'FAIL'} {name}: {got} (want {want})")
    print("consumer audit selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
