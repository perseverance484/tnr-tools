#!/usr/bin/env python3
"""Run the whole Bloodright planning pipeline.

  python3 scripts/bloodright/build_all.py          # regenerate dossiers, normalize+render trees, matrix
  python3 scripts/bloodright/build_all.py --check  # fail if any committed output is stale or any tree invalid

Exit codes: 0 ok, 1 invalid tree(s), 2 stale output(s).
"""
from __future__ import annotations

import argparse
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bloodright_lib as L  # noqa: E402

TREES_DIR = os.path.join(L.DESIGN_DIR, "trees")


def run(args: list[str]) -> int:
    print("$ " + " ".join(os.path.relpath(a, L.REPO_ROOT) if os.path.isabs(a) else a for a in args))
    return subprocess.call([sys.executable] + args, cwd=L.REPO_ROOT)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    flag = ["--check"] if args.check else []
    rc = 0
    rc = max(rc, run([os.path.join(HERE, "audit_kits.py")] + flag))
    trees = sorted(p for p in glob.glob(os.path.join(TREES_DIR, "*.json")) if not p.endswith(".validation.json"))
    if trees:
        rc = max(rc, run([os.path.join(HERE, "validate_tree.py")] + trees + (flag if args.check else ["--write"])))
        rc = max(rc, run([os.path.join(HERE, "render_tree.py")] + trees + flag))
    else:
        print("no trees under docs/design/bloodright/trees")
    rc = max(rc, run([os.path.join(HERE, "balance_matrix.py")] + flag))
    rc = max(rc, run([os.path.join(HERE, "roster_ledger.py")] + flag))
    rc = max(rc, run([os.path.join(HERE, "classification_table.py")] + flag))
    print("build_all:", "OK" if rc == 0 else f"exit {rc}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
