#!/usr/bin/env python3
"""Negative self-test for build_baseline.py: each tampered push/86 copy must be detected.

    python3 harness/ghost_ship_legacy_baseline/selftest.py

Copies the inputs into a temporary root, mutates the push/86 capture, and requires build() to
report an error for every probe (and none for the unmodified copy). Exit 0 only if all hold.
"""
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("build_baseline", os.path.join(HERE, "build_baseline.py"))
bb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb)
REPO = bb.ROOT
CAP = bb.PUSH86


def kit_rows(doc, jid):
    for c in doc["captures"]:
        if c.get("proc") == "profile.getAi":
            for uj in c["data"]["jutsus"]:
                if uj["jutsuId"] == jid:
                    yield uj["jutsu"]


def first_only(doc, jid, fn):
    fn(next(kit_rows(doc, jid)))


def every(doc, jid, fn):
    for r in kit_rows(doc, jid):
        fn(r)


def drop(doc, jid):
    for c in doc["captures"]:
        if c.get("proc") == "profile.getAi":
            c["data"]["jutsus"] = [uj for uj in c["data"]["jutsus"] if uj["jutsuId"] != jid]


PROBES = [
    ("unmodified copy", None, False),
    ("one copy cooldown+1", lambda d: first_only(d, "T3glZGcSd-jS8G-NB43GR", lambda r: r.__setitem__("cooldown", r["cooldown"] + 1)), True),
    ("all copies effect power+5", lambda d: every(d, "MG9ZujAV8lK7--YxThVbQ", lambda r: r["effects"][0].__setitem__("power", r["effects"][0]["power"] + 5)), True),
    ("added column non-null", lambda d: every(d, "nCQETf-HNnbRec1OSY2-R", lambda r: r.__setitem__("requiredSageMastery", 10)), True),
    ("presentation drift", lambda d: every(d, "X2P22h8ApDmTZHjWpNO87", lambda r: r.__setitem__("name", "Renamed")), True),
    ("record missing", lambda d: drop(d, "wMcoazoyXaEXViSCn5weF"), True),
]


def main():
    base = json.load(open(os.path.join(REPO, CAP), encoding="utf-8"))
    ok = True
    with tempfile.TemporaryDirectory() as root:
        for rel in (bb.PACKET, json.load(open(os.path.join(REPO, bb.PACKET)))["source"]["capture"]):
            os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
            shutil.copy(os.path.join(REPO, rel), os.path.join(root, rel))
        os.makedirs(os.path.dirname(os.path.join(root, CAP)), exist_ok=True)
        bb.ROOT = root
        for label, mutate, expect in PROBES:
            doc = json.loads(json.dumps(base))
            if mutate:
                mutate(doc)
            json.dump(doc, open(os.path.join(root, CAP), "w", encoding="utf-8"))
            _, errors = bb.build()
            hit = bool(errors)
            good = hit == expect
            ok &= good
            print(f"{'PASS' if good else 'FAIL'} {label}: {'detected' if hit else 'clean'}")
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
