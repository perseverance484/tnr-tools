#!/usr/bin/env python3
"""
Release-specific validate.py exception for push/93 (RUL-2026-10-12-014).

    python3 push/93_ghost_ship_guardian_repair.validate_exception.py           # check (default)
    python3 push/93_ghost_ship_guardian_repair.validate_exception.py --write   # (re)write the ledger

This is push/90's gate mechanism (push/90_ghost_ship_skyglass_release.validate_exception.py), unchanged,
with a narrower scope:
- the manifest and ledger are push/93's;
- only the classes this manifest can produce are approved.

push/93 re-sends the live push/90 quests and the push/90 Sentinel edit, so its diagnostics are a subset
of the push/90 set. The one addition is the law-49 snapshot lint on the scene-character asset push/90 created.
As before, any new, changed or missing diagnostic, or any manifest or validator change, voids the exception.
"""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("p90x", os.path.join(HERE, "90_ghost_ship_skyglass_release.validate_exception.py"))
p90x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p90x)

KEEP = {"approved_shared_menu_target", "captured_selftarget_gate"}
p90x.MANIFEST = "push/93_ghost_ship_guardian_repair.json"
p90x.LEDGER = "state/ghost_ship_guardian_repair_validate_exception.json"
p90x.CLASSES = [c for c in p90x.CLASSES if c[0] in KEEP] + [
    ("stale_snapshot_scene_character",
     r"T1 law 49: objective d_sealwright sceneCharacters 'b_K8qdNI651fTsRn9tfkk' - sceneCharacters id does not resolve",
     "b_K8qdNI651fTsRn9tfkk is gs_char_sealwright, the SCENE_CHARACTER gameAsset push/90 created (run idmap). "
     "The answers snapshot predates that run. The live push/90 after-capture of both quests already carries this id."),
]
_build = p90x.build


def build() -> dict:
    doc = _build()
    doc["ruling"] = "RUL-2026-10-12-014"
    doc["scope"] = "push/93 only, at exactly this manifest SHA-256; not a doctrine change and not a precedent"
    doc["command"] = "cd skills/building-tnr-content/data && python3 ../scripts/validate.py ../../../push/93_ghost_ship_guardian_repair.json"
    return doc


p90x.build = build

if __name__ == "__main__":
    out = p90x.main()
    sys.exit(out)
