#!/usr/bin/env python3
"""Derive the numbers that used to be worked out by hand.

Everything here was a source of arithmetic error at some point. The stat model
in particular was misunderstood for months: absolute stat values are NOT
writable, level fixes the budget, and the twelve numbers in a payload are
ratio weights. This encodes the real formulas from `app/src/libs/profile.ts`
so nobody derives them again.

Usage
  python3 tnr_calc.py ai --level 45 --hp 4200 --role skirmisher
  python3 tnr_calc.py ai --level 60 --hp 5400 --role support --show-block
  python3 tnr_calc.py kit --codes B37,S06,S07,S27,S02 [--pool 32b_DATA_pool.json]
  python3 tnr_calc.py reward --rank B
  python3 tnr_calc.py levels 30 45 60 75

All formulas are source-derived; see the SOURCE notes on each function.
"""
import json, os, sys

# ------------------------------------------------------------------ source

HP_PER_LVL = SP_PER_LVL = CP_PER_LVL = 50          # drizzle/constants.ts
MAX_STATS_CAP, MAX_GENS_CAP = 450000, 200000       # drizzle/constants.ts
USER_CAPS = {"STUDENT": 20000, "GENIN": 60000, "CHUNIN": MAX_STATS_CAP,
             "JONIN": MAX_STATS_CAP, "ELITE JONIN": MAX_STATS_CAP,
             "ELDER": MAX_STATS_CAP, "NONE": MAX_STATS_CAP}

STAT_FIELDS = ["ninjutsuOffence", "ninjutsuDefence", "genjutsuOffence", "genjutsuDefence",
               "taijutsuOffence", "taijutsuDefence", "bukijutsuOffence", "bukijutsuDefence",
               "strength", "intelligence", "willpower", "speed"]


def calc_level_requirements(level):
    """SOURCE libs/profile.ts. factor is 950 above level 80, else 500."""
    total = 0
    for i in range(1, level + 1):
        f = 950 if i > 80 else 500
        total += f + (i - 1) * f
    return total


def stat_budget(level):
    """SOURCE scaleUserStats: exp = calcLevelRequirements(level) - 500."""
    return calc_level_requirements(level) - 500


def pool_base(level):
    """SOURCE calcHP/calcSP/calcCP: 100 + 50*(level-1). All three pools share it."""
    return 100 + HP_PER_LVL * (level - 1)


def pools_multiplier_for(level, target_hp):
    """The only lever that moves pools. Schema bounds 1 to 50."""
    return round(target_hp / pool_base(level), 2)


def scale(weights, level, stats_multiplier=1):
    """Reproduce scaleUserStats exactly: each stat becomes its share of the budget."""
    total = sum(weights.values())
    exp = stat_budget(level)
    return {k: (10 + int(v / total * exp * 100) / 100) * stats_multiplier
            for k, v in weights.items()}


# ------------------------------------------------------------------- roles

ROLES = {
    # ratio weights, not numbers. Shape of the enemy, not its size.
    "skirmisher": dict(taijutsuOffence=40, bukijutsuOffence=34, speed=22, strength=20,
                       taijutsuDefence=24, bukijutsuDefence=24, ninjutsuDefence=22,
                       genjutsuDefence=22, willpower=12, intelligence=8,
                       ninjutsuOffence=1, genjutsuOffence=1),
    "bruiser": dict(taijutsuOffence=46, bukijutsuOffence=30, strength=30, speed=12,
                    taijutsuDefence=32, bukijutsuDefence=30, ninjutsuDefence=26,
                    genjutsuDefence=26, willpower=18, intelligence=6,
                    ninjutsuOffence=1, genjutsuOffence=1),
    "support": dict(taijutsuOffence=30, bukijutsuOffence=26, speed=18, strength=16,
                    taijutsuDefence=30, bukijutsuDefence=28, ninjutsuDefence=28,
                    genjutsuDefence=28, willpower=24, intelligence=20,
                    ninjutsuOffence=1, genjutsuOffence=1),
    "caster": dict(ninjutsuOffence=44, genjutsuOffence=28, intelligence=26, willpower=22,
                   ninjutsuDefence=28, genjutsuDefence=28, taijutsuDefence=20,
                   bukijutsuDefence=20, speed=16, strength=8,
                   taijutsuOffence=1, bukijutsuOffence=1),
}


def ai_block(level, target_hp, role, rank="CHUNIN", stats_multiplier=1):
    if role not in ROLES:
        raise SystemExit(f"role must be one of: {', '.join(ROLES)}")
    weights = {k: ROLES[role].get(k, 1) for k in STAT_FIELDS}
    produced = scale(weights, level, stats_multiplier)
    cap = USER_CAPS.get(rank, MAX_STATS_CAP)
    clamped = {k: v for k, v in produced.items() if v > cap}
    return {
        "level": level,
        "rank": rank,
        "poolsMultiplier": pools_multiplier_for(level, target_hp),
        "statsMultiplier": stats_multiplier,
        "weights": weights,
        "produced": {k: round(v) for k, v in produced.items()},
        "pools": {"base": pool_base(level), "after_multiplier": round(pool_base(level) * pools_multiplier_for(level, target_hp))},
        "budget": stat_budget(level),
        "cap": cap,
        "clamped_by_rank": {k: round(v) for k, v in clamped.items()},
    }


# ---------------------------------------------------------------- rewards

REWARDS = {  # derived from the shipped set, 2026-08-26
    "D": dict(exp=173, money=1100, tokens=100, prestige=14, clanpoints=100),
    "C": dict(exp=450, money=15000, tokens=100, prestige=100, clanpoints=100),
    "B": dict(exp=670, money=25000, tokens=150, prestige=150, clanpoints=150),
    "A": dict(exp=1000, money=35000, tokens=300, prestige=300, clanpoints=300),
}
REWARD_NOTES = {
    "D": "the new set's scale. The legacy 222/10,000 band is retired.",
    "C": "13 of 17 live C missions pay this. Unratified for the new format.",
    "B": "matched to Copies, Not Thefts. Ratified 2026-08-26.",
    "A": "two live bands exist, 1000/35,000 and 800/30,000. Unratified.",
}


# -------------------------------------------------------------------- kit

def kit_report(codes, pool_path):
    if not os.path.exists(pool_path):
        raise SystemExit(f"pool file not found: {pool_path}")
    pool = json.load(open(pool_path))["records"]
    out, ap = [], []
    for c in codes:
        r = pool.get(c)
        if not r:
            raise SystemExit(f"unknown pool code: {c}")
        r = dict(r, code=c)
        out.append(r)
        ap.append(r["ap"])
    stances = [r for r in out if r["ap"] == 40]
    print(f"{len(out)} records, {len(stances)} stance(s) at 40 AP, {len(out)-len(stances)} action(s) at 60 AP")
    print()
    print("%-6s %-22s %-7s %-6s %-5s %s" % ("code", "name", "target", "gate", "AP", "id"))
    for r in out:
        print("%-6s %-22s %-7s %-6s %-5s %s" % (
            r["code"], r["name"][:22], r["target"], r["gate"] if r["gate"] else "-", r["ap"], r["id"]))
    print()
    print("ids for the jutsus array:")
    print(json.dumps([r["id"] for r in out]))
    print()
    if not stances:
        print("WARNING: no 40 AP stance. A round is 100 AP, so an all-attack kit exhausts itself (laws 61 to 63).")
    if len(out) > 6:
        print(f"WARNING: {len(out)} records. Role kit sizes are 5 standard, 5 to 6 elite or boss.")
    print("gates above are range+1 (law 39). Use them verbatim in distance_lower_than conditions.")


# -------------------------------------------------------------------- cli

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    args = sys.argv[2:]

    def opt(name, default=None, cast=str):
        if name in args:
            return cast(args[args.index(name) + 1])
        return default

    if cmd == "ai":
        level = opt("--level", None, int)
        hp = opt("--hp", None, int)
        role = opt("--role", "skirmisher")
        rank = opt("--rank", "CHUNIN")
        sm = opt("--stats-multiplier", 1, float)
        if not level or not hp:
            raise SystemExit("need --level and --hp")
        b = ai_block(level, hp, role, rank, sm)
        print(f"level {level}, {role}, rank {rank}")
        print(f"  stat budget       {b['budget']:,}   (fixed by level, not negotiable)")
        print(f"  pools             {b['pools']['base']:,} base -> {b['pools']['after_multiplier']:,} "
              f"with poolsMultiplier {b['poolsMultiplier']}")
        print(f"  rank stat cap     {b['cap']:,}")
        if b["clamped_by_rank"]:
            print(f"  !! CLAMPED at rank {rank}: {b['clamped_by_rank']}")
            print(f"     raise the rank, or these are silently cut in combat")
        print()
        print("  %-20s %-10s %s" % ("field", "weight", "produced"))
        for k in STAT_FIELDS:
            print("  %-20s %-10s %s" % (k, b["weights"][k], f"{b['produced'][k]:,}"))
        if "--show-block" in args:
            payload = {k: b["weights"][k] for k in STAT_FIELDS}
            payload.update(level=level, rank=rank, poolsMultiplier=b["poolsMultiplier"],
                           statsMultiplier=sm, regeneration=60)
            print()
            print("payload block (weights go in as-is; the server rescales them):")
            print(json.dumps(payload, indent=1))

    elif cmd == "kit":
        codes = [c.strip().upper() for c in opt("--codes", "").split(",") if c.strip()]
        if not codes:
            raise SystemExit("need --codes B37,S06,...")
        kit_report(codes, opt("--pool", "32b_DATA_pool.json"))

    elif cmd == "reward":
        rank = opt("--rank", "B").upper()
        r = REWARDS.get(rank)
        if not r:
            raise SystemExit(f"rank must be one of: {', '.join(REWARDS)}")
        print(f"{rank} rank: " + "  ".join(f"{k} {v:,}" for k, v in r.items()))
        print(f"note: {REWARD_NOTES[rank]}")
        print()
        print("inline on the win_quest node, and zero content.reward explicitly, or a live")
        print("record's existing quest-level reward pays a second time through fetch-merge.")

    elif cmd == "levels":
        print("%-7s %-14s %-10s %s" % ("level", "stat budget", "pool base", "hp at multiplier 1.5 / 2 / 3"))
        for lv in [int(a) for a in args if a.isdigit()]:
            p = pool_base(lv)
            print("%-7s %-14s %-10s %s" % (lv, f"{stat_budget(lv):,}", f"{p:,}",
                                           " / ".join(f"{round(p*m):,}" for m in (1.5, 2, 3))))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
