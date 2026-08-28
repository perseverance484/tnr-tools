#!/usr/bin/env python3
"""
enemy.py - the third quarter of a mission, built rather than decided.

A mission is a graph, its art, its enemies and its rewards. The graph and the art are
generated; the rewards come from dauntless. The enemies were the piece still assembled by hand every
time, and by hand is where three specific failures kept happening:

  - an AI written without the full stat block, which the DB fills as rank STUDENT with every
    stat 10, producing a level-100 paper doll that players hit for 15k
  - a rank below CHUNIN on a high-level enemy, which passes validation and is then silently
    gutted in combat by USER_CAPS
  - an attack rule with no distance gate, or a gate that does not match the jutsu's range, so
    the AI stands still holding a jutsu it can never reach with

None of the three is a shape error, so none is caught by a schema. All three are mechanical
consequences of documented laws, which means they belong in a generator, not in a checklist.

What is derived here and what is not:

  DERIVED from ai.md section 1.8 (ratified role defaults) - poolsMultiplier, statsMultiplier,
  kit size, armour tier, passive tag count.
  DERIVED from the engine - rank floor (USER_CAPS: CHUNIN above level 30), the distance gate
  (pool `gate`, already range+1), pool ids.
  NOT DERIVED - level. It comes from the mission profile's `enemy_level_band`, and while that
  reads AWAITING_RULING this module refuses, because level is the whole stat budget:
  `scaleUserStats` rewrites every stat as `10 + (stat/sum) * exp` where exp is a function of
  level alone. Guessing level is guessing the enemy's entire power.
  NOT DERIVED - the stat ratio. Default is uniform: twelve equal weights, which asserts
  nothing. Named archetypes exist and are flagged, because a shape is a balance opinion.

Pools are deliberately not sent. `maxHealth` and friends are overwritten with
`(100 + 50*(level-1)) * poolsMultiplier`, so the multiplier is the only real handle.
"""
from __future__ import annotations

import json
import os
import sys

AWAITING = "AWAITING_RULING"
SEARCH = [os.getcwd(), os.path.dirname(os.path.abspath(__file__)), "/mnt/project",
          "/mnt/skills/user/building-tnr-content/scripts"]

STAT_FIELDS = (
    "ninjutsuOffence", "ninjutsuDefence", "genjutsuOffence", "genjutsuDefence",
    "taijutsuOffence", "taijutsuDefence", "bukijutsuOffence", "bukijutsuDefence",
    "strength", "intelligence", "willpower", "speed",
)

# ai.md 1.8, ratified. Kit size is the count of pool codes expected, not enforced.
ROLE_DEFAULTS = {
    "standard": {"poolsMultiplier": 1, "statsMultiplier": 1, "kit_size": 5,
                 "armor": "None / AI Light", "passive_tags": 0},
    "elite":    {"poolsMultiplier": 2, "statsMultiplier": 2, "kit_size": 6,
                 "armor": "AI Light / AI Medium", "passive_tags": 1},
    "boss":     {"poolsMultiplier": 2, "statsMultiplier": 3, "kit_size": 6,
                 "armor": "AI Heavy", "passive_tags": 2},
}

# Uniform asserts nothing about the enemy's shape and is the default for that reason.
STAT_ARCHETYPES = {
    "uniform": {f: 100 for f in STAT_FIELDS},
}

REGENERATION_DEFAULT = 60  # ai.md 1.2


class EnemyError(ValueError):
    """An enemy that would have been weak, capped or inert rather than invalid."""


def _find(name: str) -> str:
    for d in SEARCH:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise EnemyError(f"cannot find {name}")


def load_pool(name: str = "32b_DATA_pool.json") -> dict:
    with open(_find(name)) as fh:
        return json.load(fh)["records"]


def rank_for_level(level: int) -> str:
    """USER_CAPS clamps stats in battle: STUDENT 20k, GENIN 60k, CHUNIN and above 450k.

    An enemy written below CHUNIN above level 30 passes every check and is then gutted at
    combat time, which reads as "the enemy is weak" rather than as a config error. So this is
    the FLOOR the level demands, and nothing may go below it.
    """
    return "CHUNIN" if level > 30 else "GENIN"


# LVL_CAP per rank, from USER_CAPS in 45e. Above GENIN every rank shares one row -
# MAX_GENS_CAP, MAX_STATS_CAP, LVL_CAP 100 - so CHUNIN, JONIN, ELITE JONIN, ELDER and NONE are
# mechanically identical and the choice between them is pure flavour.
RANK_LVL_CAP = {"STUDENT": 10, "GENIN": 30, "CHUNIN": 100, "JONIN": 100,
                "ELITE JONIN": 100, "ELDER": 100, "NONE": 100}


def resolve_rank(level: int, requested: str | None) -> str:
    """Allow rank to be RAISED for story, never lowered below what the level can carry.

    A deserter line wants its top rungs reading JONIN rather than CHUNIN, and that costs
    nothing: the caps row is identical. What is not free is the other direction - writing a
    level-25 dropout as STUDENT caps it at 20k stats and level 10, which is the same silent
    gutting the derived rank exists to prevent. So flavour up is free and flavour down refuses.
    """
    floor = rank_for_level(level)
    if not requested:
        return floor
    requested = str(requested).upper()
    if requested not in RANK_LVL_CAP:
        raise EnemyError(f"rank {requested!r} not one of {', '.join(RANK_LVL_CAP)}")
    if RANK_LVL_CAP[requested] < level:
        raise EnemyError(
            f"rank {requested} caps level at {RANK_LVL_CAP[requested]}, but this enemy is "
            f"level {level}. It would pass every check and be gutted at combat time. "
            f"Floor for this level is {floor}."
        )
    return requested


def resolve_kit(codes, pool: dict) -> list:
    kit = []
    for code in codes:
        if code not in pool:
            raise EnemyError(f"pool code {code!r} does not exist (32b_DATA_pool.json)")
        kit.append(dict(pool[code], code=code))
    return kit


def build_rules(kit: list, factory) -> list:
    """One gated attack rule per kit entry, then a move fallback.

    The gate is the pool's own `gate` value, which is already range+1. Computing it here from
    `range` would be a second implementation of the same arithmetic and a place for the two to
    disagree. The move fallback is last: without it an AI whose every gate fails does nothing
    at all, which looks identical to a severed equip link in the logs.
    """
    rules = []
    for j in kit:
        # A self/ground-targeted stance carries `range: null` and `gate: null` in the pool.
        # Gating it on distance is not merely redundant: the stance would then only fire while
        # an opponent happened to be inside the gate, which is a behaviour change nobody asked
        # for. Ungated, it fires when the AI has the AP for it. validate.py flags the gated
        # form, and this is the construction-side fix for it.
        if j.get("gate") is None:
            rules.append(factory.rule(
                action=factory.action("use_specific_jutsu", jutsuId=j["id"]),
            ))
            continue
        rules.append(factory.rule(
            factory.condition("distance_lower_than", value=j["gate"]),
            action=factory.action("use_specific_jutsu", jutsuId=j["id"]),
        ))
    rules.append(factory.rule(action=factory.action("move_towards_opponent")))
    return rules


def build_ai(entry: dict, level, factory, pool: dict) -> dict:
    name = entry.get("name")
    if not name:
        raise EnemyError("roster entry has no name")
    if level == AWAITING or level is None:
        raise EnemyError(
            f"{name}: enemy level is unresolved. It comes from the profile's "
            f"enemy_level_band, which is still {AWAITING}. Level fixes the entire stat "
            f"budget, so there is no safe default."
        )
    level = int(level)
    if not 1 <= level <= 200:
        raise EnemyError(f"{name}: level {level} outside the server range 1-200")

    role = entry.get("role", "standard")
    if role not in ROLE_DEFAULTS:
        raise EnemyError(f"{name}: role {role!r} not one of {', '.join(ROLE_DEFAULTS)}")
    defaults = ROLE_DEFAULTS[role]

    archetype = entry.get("stat_archetype", "uniform")
    if archetype not in STAT_ARCHETYPES:
        raise EnemyError(f"{name}: stat archetype {archetype!r} is not defined")

    codes = entry.get("kit") or []
    if not codes:
        raise EnemyError(
            f"{name}: no kit. Per-event jutsu minting is retired; kits come from the shared "
            f"pool by code (32_REGISTRY_shared_ai_pool.md)."
        )
    kit = resolve_kit(codes, pool)

    data = {
        "username": name,
        "level": level,
        "rank": resolve_rank(level, entry.get("rank")),
        "regeneration": REGENERATION_DEFAULT,
        "poolsMultiplier": defaults["poolsMultiplier"],
        "statsMultiplier": defaults["statsMultiplier"],
        "isSummon": False,
        # Standing rule, every entity: content ships hidden and publishing is a separate,
        # human step. Where the column does not exist the builder strips the key harmlessly.
        "hidden": True,
        "primaryElement": entry.get("element") or "",
        "secondaryElement": "",
        # Literal ids, never @jutsu refs: an unresolvable ref in the jutsus array is stripped
        # server-side without an error and the AI stands there unarmed.
        "jutsus": [j["id"] for j in kit],
        "rules": build_rules(kit, factory),
        "includeDefaultRules": False,
        **STAT_ARCHETYPES[archetype],
    }
    if entry.get("avatar"):
        data["avatar"] = entry["avatar"]

    # AP economy (32b _meta, laws 61-63): a round is 100 AP, attacks cost 60 and stances 40.
    # A kit of nothing but attacks cannot fund a full round and the AI stalls itself. Reported
    # rather than refused, because a deliberately short fight can justify it.
    warnings = []
    if kit and all(j.get("ap", 60) >= 60 for j in kit):
        warnings.append(
            f"{name}: kit is all {kit[0].get('ap', 60)} AP actions with no 40 AP stance; "
            f"a round is 100 AP, so the AI will exhaust itself (laws 61-63)"
        )

    return {
        "name": name,
        "entity": "ai",
        "slot": "create",
        "srcId": entry.get("srcId") or "ai_" + "".join(
            ch.lower() if ch.isalnum() else "_" for ch in name).strip("_"),
        "data": data,
        "_derived": {"role": role, "armor_tier": defaults["armor"],
                     "passive_tags_expected": defaults["passive_tags"],
                     "kit_size_expected": defaults["kit_size"],
                     "kit_codes": [j["code"] for j in kit],
                     "rank_reason": f"level {level} floor {rank_for_level(level)} (USER_CAPS); written {resolve_rank(level, entry.get('rank'))}",
                     "warnings": warnings},
    }


def build_roster(roster: list, level, factory, pool: dict | None = None) -> list:
    pool = pool if pool is not None else load_pool()
    return [build_ai(e, level, factory, pool) for e in roster]


# --------------------------------------------------------------------------- selftest

ROSTER = [
    {"name": "Test Thug", "role": "standard", "kit": ["S01", "S02"], "element": "Fire"},
    {"name": "Test Captain", "role": "boss", "kit": ["S01", "A1"], "srcId": "cap"},
]


def selftest() -> int:
    for d in SEARCH:
        if os.path.isdir(d) and d not in sys.path:
            sys.path.insert(0, d)
    from factory import Factory

    f = Factory()
    pool = load_pool()
    checks, failures = [], []

    def want(cond, label):
        checks.append(label)
        if not cond:
            failures.append(label)

    try:
        build_roster(ROSTER, AWAITING, f, pool)
        want(False, "an unresolved level refuses rather than defaulting")
    except EnemyError as err:
        want("stat budget" in str(err), "an unresolved level refuses rather than defaulting")

    out = build_roster(ROSTER, 45, f, pool)
    thug, cap = out[0], out[1]

    want(thug["data"]["rank"] == "CHUNIN", "level 45 forces CHUNIN so USER_CAPS does not gut it")
    want(build_ai({"name": "x", "kit": ["S01"]}, 12, f, pool)["data"]["rank"] == "GENIN",
         "level 12 stays GENIN")
    want(cap["data"]["statsMultiplier"] == 3 and cap["data"]["poolsMultiplier"] == 2,
         "boss multipliers come from the ratified role table")
    want(thug["data"]["statsMultiplier"] == 1, "standard role is not boosted")
    want(all(f_ in thug["data"] for f_ in STAT_FIELDS), "all twelve stat fields present")
    want(all(thug["data"][f_] >= 10 for f_ in STAT_FIELDS), "every stat clears the min of 10")
    want("maxHealth" not in thug["data"] and "curChakra" not in thug["data"],
         "pools not sent; they are overwritten from poolsMultiplier")

    rules = thug["data"]["rules"]
    want(len(rules) == 3, "one rule per kit jutsu plus a move fallback")
    want(rules[-1]["action"]["type"] == "move_towards_opponent", "move fallback is last")
    gates = [r["conditions"][0]["value"] for r in rules[:-1]]
    want(gates == [pool["S01"]["gate"], pool["S02"]["gate"]],
         "every attack rule carries the pool's own gate, not a recomputed one")
    want(all(r["conditions"][0]["value"] == pool[c]["range"] + 1
             for r, c in zip(rules[:-1], ["S01", "S02"])), "gate equals jutsu range plus one")

    want(thug["data"]["jutsus"] == [pool["S01"]["id"], pool["S02"]["id"]],
         "kit resolves to literal ids, never @jutsu refs")
    want(cap["srcId"] == "cap" and thug["srcId"] == "ai_test_thug", "srcIds usable and slugged")
    want(thug["data"]["hidden"] is True, "every AI ships hidden")
    want(any("100 AP" in w for w in thug["_derived"]["warnings"]),
         "an all-attack kit raises the AP-economy warning rather than shipping silently")

    try:
        build_ai({"name": "y", "kit": ["NOPE"]}, 20, f, pool)
        want(False, "an unknown pool code refuses")
    except EnemyError:
        want(True, "an unknown pool code refuses")

    try:
        build_ai({"name": "z"}, 20, f, pool)
        want(False, "a kitless enemy refuses rather than shipping unarmed")
    except EnemyError:
        want(True, "a kitless enemy refuses rather than shipping unarmed")

    for label in failures:
        print(f"  FAIL  {label}")
    print(f"\n{len(checks) - len(failures)} passed, {len(failures)} failed")
    return len(failures)


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
