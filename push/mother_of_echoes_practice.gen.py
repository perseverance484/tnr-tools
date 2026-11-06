#!/usr/bin/env python3
"""The Mother of Echoes practice fight (push/469): a HIDDEN copy of the uber's battle pyramid for the director to
playtest. Zero live requests.

    python3 push/mother_of_echoes_practice.gen.py --bundles <440, 461-464 bundles> --economy <417 bundle>
        -> push/469_mother_of_echoes_practice.json

Same three battles against the same live boss AIs as the real quest (push/464), so every tuning or art edit to those
records (push/466) shows here too. Differences from the real quest: no entry items (no shards needed); the real rewards stay (ryo, exp, both variant-token rolls and the pick) so the director's tester
can check the reward screen (director, 2026-11-04: "Put the rewards on it for my tester, no requirements just
hidden"). Its own name, and it stays hidden for good (never published): hidden is the only gate on free rewards. The director asked to reuse
an existing quest (Faded Ghostwatch, push/393), but 393 never ran (RUL-2026-10-31-090), so there is no record to
swap; this is a fresh create. Built by importing push/mother_of_echoes.gen.py's quest_data (one source for the
fight); do not hand-edit the output.
"""
import argparse
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("moe", os.path.join(ROOT, "push", "mother_of_echoes.gen.py"))
moe = importlib.util.module_from_spec(_s)
_s.loader.exec_module(moe)

NUM = 469
NAME = "The Mother of Echoes (Practice)"
DESC = ("Test fight for The Mother of Echoes. The same three battles against the same enemies and the same rewards, "
        "with no shards needed. Health, chakra and stamina carry between battles with no refills, as in the real "
        "fight.")


def practice_data(b, ids, econ, scenes=None):
    """The practice quest record: the real quest_data (scenes: 466 asset ids, or None for the placeholder chamber)
    with no entry items, practice wording, the real rewards, hidden. Used for the 469 create and later edits."""
    d = moe.quest_data(b, ids, econ, scenes)
    d.update({"name": NAME, "description": DESC, "hidden": True})
    c = d["content"]
    c["entryItems"] = []  # no shards: the director's tester enters freely; the real rewards stay (hidden quest)
    for o in c["objectives"]:
        if o["task"] == "fail_quest":
            o["description"] = "Practice over. Try again whenever you like."
        for k in ("failDescription", "drawDescription", "fleeDescription"):
            if k in o:
                o[k] = "Practice over."
        if o["id"] == "d_intro1":
            o["description"] = "<i>Test run.</i> No shards are needed.<br><br>" + o["description"]
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--bundles", nargs="*", default=[], help="results bundles of 440 and 461-464")
    ap.add_argument("--economy", help="push/417 results bundle")
    a = ap.parse_args()
    b = moe.Build(moe.load_spec())
    ids = moe.created(a.bundles, moe.PFX)
    econ = moe.created([a.economy] if a.economy else [], moe.ECON)
    moe.need(econ, [moe.ECON + k for k in ("keel", "crown", "tide", "ledger", *moe.TOKEN_PCT)], "--economy")
    moe.need(ids, [moe.sid(t) for t in b.bosses], "practice")
    d = practice_data(b, ids, econ)
    m = {"_note": (f"push/{NUM}: the HIDDEN Mother of Echoes practice fight (director, 2026-11-04). Same battles and "
                   "boss AIs as push/464 (literal ids, law 17), no entry items, the real rewards, never published (hidden is the only gate). Generated "
                   "by push/mother_of_echoes_practice.gen.py; do not hand-edit."),
         "items": [{"entity": "quest", "slot": "create", "srcId": "sg469_practice", "phase": 1, "name": NAME,
                    "data": d}]}
    p = os.path.join(ROOT, "push", f"{NUM}_mother_of_echoes_practice.json")
    with open(p, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
