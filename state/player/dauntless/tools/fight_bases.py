#!/usr/bin/env python3
"""Both kits' base damage for this matchup, from the game's own combat code (director 2026-11-11: "There's no
reason it shouldnt accurately account for these").

On a fresh board (both at full HP, adjacent, round 1) the engine assembles both fighters as the game does: stats at
the caps, his gear the endgame assumption (full Kaeruun + Subaku's mask) unless known, both bloodlines, gear passives,
elemental mastery, titles and this fight's meal / raid buffs (read live at battle start). Each damaging action of
mine and of his is fired alone; the damage is that action's base for this fight. Every permanent modifier is inside
these numbers, so planner2 then applies only the temporary effects of the live state on top (in_base).

Writes fights/live/<bid>_bases.json {"me": {name: dmg}, "him": {actionId: dmg}}. ~5 s, run beside the fight.
Usage: fight_bases.py <battleId>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clock  # noqa: E402
import engine_bridge as EB  # noqa: E402
import shotplan  # noqa: E402
import turn  # noqa: E402
import value_model  # noqa: E402
from ingest import ME  # noqa: E402

LIVE = os.path.join(HERE, "..", "fights", "live")


def mine(rows, en_id, perm, cal):
    names = [k for k, v in shotplan.MINE.items() if v[0] and k in turn.ACTION_ID]
    me = {"curHealth": 5050, "maxHealth": 5050, "perm": [e for e in perm if e.get("targetId") == ME]}
    en = {"curHealth": 5050, "maxHealth": 5050, "userId": en_id, "perm": [e for e in perm if e.get("targetId") == en_id]}
    seqs = [turn.resolve_targets((n,), (7, 4), (6, 4), set())[0] for n in names]
    req_rows = [r for r in rows if r[1] == en_id]                     # his kit and bloodline; no replay
    res = EB.replay_eval(req_rows, ME, en_id, me, en, (7, 4), (6, 4), 1, "same", cal,
                         [[(n, a, t) for n, a, t in s] for s in seqs], timeout=90, fresh=True)
    out = {}
    for n, r in zip(names, (res or {}).get("results") or []):
        if r.get("legal"):
            out[n] = 5050 - r["afterMe"]["him"]
    return out


def his(rows, en_id, perm, cal):
    acts = clock.his_actions(en_id, rows) or {}
    ids = [a for a, v in acts.items() if v[4][0]]
    return EB.his_probe(rows, en_id, ids, cal, perm=perm) if ids else {}


def main(bid):
    cache = json.load(open(os.path.join(LIVE, f"{bid}.json")))
    users = (cache.get("battle") or {}).get("battle.usersState.*.userId") or []
    en_id = next((u for u in users if u != ME), None)
    if not en_id:
        return
    rows = [(e[1], e[2], e[3], e[4]) for e in cache.get("entries") or []]
    perm = cache.get("perm_effects") or []
    cal = value_model.load_cal()
    out = {"me": mine(rows, en_id, perm, cal), "him": his(rows, en_id, perm, cal), "opp": en_id}
    json.dump(out, open(os.path.join(LIVE, f"{bid}_bases.json"), "w"))
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
