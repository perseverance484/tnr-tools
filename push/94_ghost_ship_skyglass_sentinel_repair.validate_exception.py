#!/usr/bin/env python3
"""
Release-specific validate.py exception for push/94 (RUL-2026-10-12-015).

    python3 push/94_ghost_ship_skyglass_sentinel_repair.validate_exception.py           # check (default)
    python3 push/94_ghost_ship_skyglass_sentinel_repair.validate_exception.py --write   # (re)write the ledger

This is the push/93 gate with push/94's manifest, ledger and ruling. The approved classes are the same:
shared menu targets, the captured self-target gate, and the stale-snapshot scene character.
Any change voids the exception.
"""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("p93x", os.path.join(HERE, "93_ghost_ship_guardian_repair.validate_exception.py"))
p93x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p93x)
p90x = p93x.p90x

p90x.MANIFEST = "push/94_ghost_ship_skyglass_sentinel_repair.json"
p90x.LEDGER = "state/ghost_ship_skyglass_sentinel_repair_validate_exception.json"
_build = p93x.build


def build() -> dict:
    doc = _build()
    doc["ruling"] = "RUL-2026-10-12-015"
    doc["scope"] = "push/94 only, at exactly this manifest SHA-256; not a doctrine change and not a precedent"
    doc["command"] = "cd skills/building-tnr-content/data && python3 ../scripts/validate.py ../../../push/94_ghost_ship_skyglass_sentinel_repair.json"
    return doc


p90x.build = build

if __name__ == "__main__":
    sys.exit(p90x.main())
