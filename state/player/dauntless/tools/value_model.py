#!/usr/bin/env python3
"""Value model for turn.py: every weight the planner uses, derived from the engine source and our fight logs.

Replaces the old flat setup credit (+300 per x1 multiplier) and most hand-picked penalties with three mechanisms
that measure the same things directly:

1. Calibrated damage (calibration.json from calibrate.py). Each of my hits uses a base blended from the logged
   median and the prior in shotplan.MINE: base = (n*median + K*prior) / (n + K), K = 3. Pierce stays flat
   (engine process.ts: pierce runs after the damage modifiers, and its shield pass destroys shields instead of
   absorbing). The generic enemy's hit size, typical turn and burst turn come from the logs.

2. Enemy option set with experience weights. His reply is not one guess but a weighted set:
     turn    his median active turn (base units, calibrated)    burst  his 85th-percentile turn, weight 0.15
     setup   +35% given on him, +35% taken on me, one light hit (top players' set-up-then-finish pattern)
     pierce  631 flat + light hit, only while his pierce is ready; destroys my shield (engine)
     clear   strips my positive tags + light hit, only while he still holds Clear and I have live buffs
     smoke   -70% on my next round, only while he hasn't smoked
   Weights are Beta-smoothed logged frequencies (prior strength 4, priors from the 2026-11-09 top-player study),
   conditional on the situation: P(pierce | my shield up), P(Clear | I have >= 2 live buffs).
   A live summon adds its own hits to every option and keeps a pierce threat open (summons ignore his locks).
   Terminal values: kill +5000, death -6500 (a double KO is a loss).
   Score of a bundle = 0.7 x expected value + 0.3 x worst case. The 0.3 risk weight is there because a lost
   fight costs far more than HP (5 of our 8 PvP losses were one burst turn).

3. Lookahead + reserves. After his reply the planner plays my best follow-up next round (discount 0.8), so
   setup, Smoke on my own burst turn and early pierce are valued by what they do next turn, not by flat bonuses.
   Long-cooldown resources whose value lies beyond the 2-round horizon carry a reserve cost when spent, scaled
   by the fight time left:
     Cleanse  = 2 rounds x debuff_value x 0.8  (debuff_value: logged HP a live debuff package on me was worth)
     Clear    = 2 rounds x buff_value x 0.8    (buff_value: logged HP his live +given was worth)
     Smoke    = 0.7 x en_burst x 0.5           (blunts one future burst turn; about half of fights give one)
     pierce   = 0.6 x mean(500 shield, 0.7 x my hit while I'm smoked)  (what a pierce is worth in its window,
                times the chance a window turns up during its 6-round cooldown)
   reserve x min(1, rounds_left / cooldown), rounds_left = fight_len + 2 - round.

Kept as explicit guards (cheap to state, catastrophic to miss): lethal wound/drain tick without Cleanse, more than
one basic step, pierce into >= 20% absorb (director rule; absorb also heals pierce, tags.ts absorb()).
"""
import json
import os

import cd_plan
import shotplan

HERE = os.path.dirname(os.path.abspath(__file__))
K_BLEND = 3
RISK = 0.3
GAMMA = 0.8
BURST_P = 0.15
BURST_SEEN = 1.5       # his given multiplier (live or cast this round) that counts as a shown burst
BURST_SEEN_CAP = 0.8
BURST_BASE = 1100.0  # my typical two-hit burst base (Fury/Rebirth/Lotus/Shrapnel ~575 each, calibrated)
KILL, DEATH = 5000, 6500
PRIORS = {  # (prior p, strength) from the 2026-11-09 top-player study (Winta, DDXXD, Ziharkk, Gario)
    "pierce_vs_shield": (0.6, 4), "clear_vs_2buffs": (0.3, 4),
    # director 2026-11-11 (Targaryen R3->R4): a stack of 3+ buffs is what draws the Clear; prior 0.6 at strength 8
    "clear_vs_3buffs": (0.6, 8), "clear_vs_4buffs": (0.6, 8),  # logs: all 8 Clears met 3+ buffs, 7 of 8 met 4+
    "pierce": (0.15, 4), "clear": (0.15, 4),
    "smoke": (0.10, 4), "setup": (0.35, 4),
}


def load_cal():
    try:
        return json.load(open(os.path.join(HERE, "calibration.json")))
    except (OSError, ValueError):
        return {"my_base": {}, "en_hit": 500, "en_turn": 600, "en_burst": 1300, "opportunities": {},
                "debuff_value": 300, "buff_value": 450, "fight_len": 7}


def clear_risk_4(cal):
    """P(he Clears this turn | my 4+ buff stack, his Clear held). Per-turn hazard among opponents who do Clear:
    every logged Clear of a 4+ stack came on his 1st-3rd chance (7 Clears in 12 chances, calibrate.py
    clear_wait_4buffs); the raw 7/26 is diluted by AFK / short fights where he never got to it. Director
    2026-11-11: a big stack "basically forces the enemy's Clear". Beta-smoothed with prior 0.6 at strength 8."""
    w = cal.get("clear_wait_4buffs")
    if not w:
        return smoothed(cal, "clear_vs_4buffs")
    return (len(w) + 0.6 * 8) / (sum(w) + 8)


def smoothed(cal, key):
    hit, n = cal.get("opportunities", {}).get(key, [0, 0])
    p0, k = PRIORS[key]
    return (hit + p0 * k) / (n + k)


def calibrate_kit(cal):
    """Blend logged medians into shotplan.MINE base damage (in place). Returns {name: (old, new, n)}."""
    changes = {}
    for name, rec in cal.get("my_base", {}).items():
        spec = shotplan.MINE.get(name)
        if not spec or len(spec) > 2 and spec[2] == "pierce":
            continue
        n, med = rec["n"], rec["median"]
        new = (n * med + K_BLEND * spec[0]) / (n + K_BLEND)
        changes[name] = (spec[0], round(new), n)
        shotplan.MINE[name] = (new,) + tuple(spec[1:])
    return changes


def generic_kit(cal, reach_scale=1.0):
    hit = cal.get("en_hit", 500) * reach_scale
    return {
        "turn": (cal.get("en_turn_norm", 800) * reach_scale, []),
        "burst": (cal.get("en_burst_norm", 1500) * reach_scale, []),
        "summon": (450.0, []),  # Korin's Jade 2026-11-11: pierce 379 + 152 + basic 65 into +35% taken -> ~450 base
        "hit": (hit, []), "light": (hit * 0.6, []),
        "pierce": (631.0, [], "pierce"),
        "clear": (0, [("me", "clear", 1, 0, True)]),
        "smoke": (0, [("me", "given", -0.70, 1), ("en", "given", -0.70, 1), ("en", "dr", 0.25, 2)]),
        "buff": (0, [("en", "given", 0.35, 2)]),
        "debuff": (0, [("me", "taken", 0.35, 2)]),
        "basic": (150, []), "hit2": (hit, []),
    }


def enemy_options(cal, ctx, me_side, r, afk):
    """[(weight, [actions])] for the generic enemy reply in round r."""
    if afk:
        return [(1.0, [])]
    opts = []
    # his Clear strips every positive of mine that exists when he acts, live or cast this round (engine tags.ts
    # removeEffects has no castThisRound filter). Acting first (player 1), my new buffs start next round but his
    # Clear later this round still takes them, so they count: t[2] <= r + 1, not t[2] <= r.
    clearable = lambda t: shotplan.positive(t) and t[2] <= r + 1 and t[3] >= r  # noqa: E731
    my_pos = sum(1 for t in me_side.tags if clearable(t))
    if ctx["pierce_ready"]:
        p = smoothed(cal, "pierce_vs_shield") if me_side.live("shield", r) else smoothed(cal, "pierce")
        if ctx.get("pierce_shown") and me_side.live("shield", r):
            p = max(p, 0.85)  # every logged shield cast into a SHOWN, ready pierce was broken (Ziharkk, Korin)
        opts.append((p, ["pierce", "light"]))
    stack = sum(1 for t in me_side.tags if clearable(t) and t[0] not in ("clearimmune", "debuffimmune"))
    if ctx["clear_held"] and my_pos >= 1 and not me_side.live("clearimmune", r):
        p = (clear_risk_4(cal) if stack >= 4 else smoothed(cal, "clear_vs_3buffs") if stack >= 3 else
             smoothed(cal, "clear_vs_2buffs") if my_pos >= 2 else smoothed(cal, "clear"))
        opts.append((p, ["clear", "light"]))
    if not ctx.get("smoke_spent"):
        opts.append((smoothed(cal, "smoke"), ["smoke", "light"]))
    blocked = ctx.get("en_buffblocked")   # my Seal / Lotus: he cannot buff this turn
    opts.append((smoothed(cal, "setup") * (0.4 if blocked else 1.0), ["debuff", "light"] if blocked else ["buff", "debuff", "light"]))
    # a stacked +given on him is the burst tell (Hikuro R7, Warlord40 R3): scale the burst weight with his live
    # damage-given multiplier, capped at 0.6
    g = ctx.get("en_given", 1.0)
    # a stack he has ALREADY cast is a known fact, not a guess (DDX R4, 2026-11-11: he acted first and queued
    # +15/+30/+35/+35 given; acting second I could see it all, yet the 0.6 burst cap shared with his absolute Clear
    # hazard left the burst at 0.22 and the planner raced ember+thunders into an 1854 hit). From BURST_SEEN up, the
    # burst is an absolute hazard like his Clear, capped at BURST_SEEN_CAP.
    seen = g >= BURST_SEEN and not blocked
    opts.append((min(BURST_SEEN_CAP if seen else 0.6, BURST_P * g ** 3) * (0.35 if blocked else 1.0),
                 ["burst"] + (["seen"] if seen else [])))  # his 85th-percentile turn: 15% of active turns by definition
    rest = max(0.05, 1.0 - sum(w for w, _ in opts))
    opts.append((rest, ["turn"]))
    if ctx.get("summon"):  # a live summon acts on its own cooldowns (and can pierce: Jade broke my shield R5)
        opts = [(w, o + ["summon"]) for w, o in opts]
    # his Clear is an absolute probability (measured hazard): the other options share what is left, instead of
    # normalising everything together and diluting the Clear (0.59 used to come out ~0.42)
    absolute = lambda a: "clear" in a or "seen" in a  # noqa: E731
    abs_w = sum(w for w, a in opts if absolute(a))
    rest_tot = sum(w for w, a in opts if not absolute(a))
    if abs_w and rest_tot:
        k = min(1.0, 0.95 / abs_w)
        opts = [(w * k if absolute(a) else w * (1 - min(abs_w, 0.95)) / rest_tot, a) for w, a in opts]
        return [(w, [x for x in a if x != "seen"]) for w, a in opts]
    tot = sum(w for w, _ in opts)
    return [(w / tot, a) for w, a in opts]


def score(me, en, my0, en0):
    """HP swing plus terminal values. Death outweighs a kill: the Korin double KO (2026-11-11) was scored a loss."""
    s = (en0 - en.hp) - (my0 - me.hp)
    if en.hp <= 0:
        s += KILL
    if me.hp <= 0:
        s -= DEATH
    return s


def reserves(cal):
    smoked_hit = 0.3 * 580  # my median non-pierce hit while smoked (x0.3)
    return {
        "cleanse": 2 * cal.get("debuff_value", 300) * 0.8,
        "clear": 2 * cal.get("buff_value", 450) * 0.8,
        "smoke": 0.7 * cal.get("en_burst", 1300) * 0.5,
        "stormblade": 0.6 * (500 + (631 - smoked_hit)) / 2,
        "nights": 0.6 * (500 + (631 - smoked_hit)) / 2,
    }


def reserve_cost(bundle, cal, rnd):
    res = reserves(cal)
    left = max(0, cal.get("fight_len", 7) + 2 - rnd)
    cost, why = 0.0, []
    for a in bundle:
        if a in res and a not in ("stormblade", "nights"):  # pierce is priced by turn.penalties (window rule)
            cd = cd_plan.ACTIONS.get(a, (0, 6))[1] or 6
            c = res[a] * min(1.0, left / cd)
            cost += c
            why.append(f"{a} reserve -{c:.0f}")
    return cost, why


def copy_side(s):
    n = shotplan.Side(s.hp)
    n.tags = [list(t) for t in s.tags]
    return n
