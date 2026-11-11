#!/usr/bin/env python3
"""Damage factors from meal / raid buffs in one battle (director 2026-11-11: "The last little bit of variance is
probably meal buffs from food").

The game adds each fighter's meal and raid buffs to the battle at the start as permanent stat boosts (combat.ts,
processUsersForBattle: raidBuffs -> increasestat effects with timedBuffExpiresAt). No log line shows them; the pilot
reads them once per battle from combat.getBattle (pilot.perm_effects). Stat boosts reach damage through the stat
formula, so the factor comes from the engine itself: the same hit fired on a fresh board with and without the buffs.
  me   my hits on him: my offence buffs and his defence buffs
  him  his hits on me: his offence buffs and my defence buffs (the same formula with the roles swapped)
Writes fights/live/<bid>_meal.json {"me": f, "him": f}; planner2 multiplies the matching damage by them.

Usage: meal_factor.py <battleId>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_bridge as EB  # noqa: E402
import turn  # noqa: E402
import value_model  # noqa: E402
from ingest import ME  # noqa: E402

LIVE = os.path.join(HERE, "..", "fights", "live")
PROBE = "fury"


def timed(effects, uid, direction):
    """uid's meal / raid buffs that act on the given side of the formula (offence or defence)."""
    return [e for e in effects if e.get("targetId") == uid and e.get("timedBuffExpiresAt")
            and e.get("direction") in (direction, "both", None)]


def dealt(me_perm, him_perm, cal):
    me = {"curHealth": 5050, "maxHealth": 5050, "perm": me_perm}
    en = {"curHealth": 5050, "maxHealth": 5050, "perm": him_perm, "userId": "him"}
    seq = turn.resolve_targets((PROBE,), (7, 4), (6, 4), set())[0]
    r = EB.replay_eval([], ME, "him", me, en, (7, 4), (6, 4), 1, "same", cal, [[(n, a, t) for n, a, t in seq]],
                       timeout=60)
    res = (r or {}).get("results") or [{}]
    return 5050 - res[0]["afterMe"]["him"] if res[0].get("legal") else None


def main(bid):
    cache = json.load(open(os.path.join(LIVE, f"{bid}.json")))
    effs = cache.get("perm_effects") or []
    users = (cache.get("battle") or {}).get("battle.usersState.*.userId") or []
    foe = next((u for u in users if u != ME), None)
    out = {"me": 1.0, "him": 1.0}
    if foe and any(e.get("timedBuffExpiresAt") for e in effs):
        cal = value_model.load_cal()
        base = dealt([], [], cal)
        mine = dealt(timed(effs, ME, "offence"), timed(effs, foe, "defence"), cal)
        his = dealt(timed(effs, foe, "offence"), timed(effs, ME, "defence"), cal)   # roles swapped, same formula
        if base:
            out = {"me": round((mine or base) / base, 4), "him": round((his or base) / base, 4)}
    json.dump(out, open(os.path.join(LIVE, f"{bid}_meal.json"), "w"))
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
