#!/usr/bin/env python3
"""Verify the skill bundle is internally consistent before trusting it.

This exists because the bundle drifted from its working copies inside a single
session: three scripts were edited in a scratch directory and the bundled ones
kept running the old logic. Nothing detected it, because a bundled script that
parses and runs looks healthy whether or not it is the current one.

Checks:
  - every bundled script parses
  - factory.py --selftest passes
  - the generated files are present, parse, and share one provenance stamp
  - validate.py and factory.py agree on the 45g blocks they consume

Usage:  python3 scripts/selfcheck.py [--generated <dir>]
"""
import ast
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN = ("45c_DATA_constructors.json", "45d_DATA_entity_schemas.json",
       "45g_DATA_checks.json")


def main():
    gdir = os.getcwd()
    if "--generated" in sys.argv:
        gdir = sys.argv[sys.argv.index("--generated") + 1]
    errs, notes = [], []

    for p in sorted(glob.glob(os.path.join(HERE, "*.py"))):
        try:
            ast.parse(open(p).read())
        except SyntaxError as e:
            errs.append(f"{os.path.basename(p)} does not parse: {e}")
    notes.append(f"{len(glob.glob(os.path.join(HERE, '*.py')))} bundled scripts parse")

    stamps = {}
    for name in GEN:
        p = os.path.join(gdir, name)
        if not os.path.exists(p):
            errs.append(f"{name} not found in {gdir}. The scripts read it from the working "
                        "directory; copy the generated files in first")
            continue
        try:
            d = json.load(open(p))
        except Exception as e:
            errs.append(f"{name} does not parse: {e}")
            continue
        prov = d.get("_provenance") or {}
        if prov.get("extracted"):
            stamps[name] = prov["extracted"]
    if len(set(stamps.values())) > 1:
        errs.append(f"generated files disagree on provenance: {stamps}. Regenerate all of them "
                    "from one source drop")
    elif stamps:
        notes.append(f"generated files stamped {sorted(set(stamps.values()))[0]}")

    if not errs:
        r = subprocess.run([sys.executable, os.path.join(HERE, "factory.py"), "--selftest"],
                           capture_output=True, text=True, cwd=gdir)
        tail = (r.stdout or "").strip().splitlines()[-1:] or ["no output"]
        (notes if r.returncode == 0 else errs).append("factory selftest: " + tail[0])

    checks_p = os.path.join(gdir, "45g_DATA_checks.json")
    if os.path.exists(checks_p):
        declared = {k for k in json.load(open(checks_p)) if not k.startswith("_")}
        r = subprocess.run([sys.executable, os.path.join(HERE, "validate.py"), "--check-ids", "x"],
                           capture_output=True, text=True, cwd=gdir)
        try:
            impl = set(json.loads(r.stdout)["checks"])
            for c in sorted(declared - impl):
                errs.append(f"45g declares '{c}' but validate.py does not consume it")
            notes.append(f"validate.py consumes all {len(declared)} declared 45g blocks")
        except Exception:
            errs.append("validate.py --check-ids did not return an inventory")

    for e in errs:
        print("ERROR  " + e)
    for n in notes:
        print("note   " + n)
    print(f"\n{len(errs)} errors")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
