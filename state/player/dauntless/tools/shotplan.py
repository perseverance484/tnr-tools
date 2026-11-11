#!/usr/bin/env python3
"""Shot planner: simulate the outcome of candidate turns before firing them (director, 2026-11-10: "a script that lets
you see the outcome of a set of moves, so you can predict enemy moves, respond with the highest value actions and plan
future combinations").

Model (engine timing rules from combat_rules.md):
  - a tag cast in round N is live from round N+1 for its duration; instant effects (damage, pierce, shield, Clear,
    Cleanse, stun AP loss, seal, Subaku's -given, Fury's recoil ground) apply at once.
  - damage = base x prod(1 + attacker +given) x prod(1 + target +taken) x prod(1 - target DR) [x 0.3 smoked];
    pierce = flat (no boosts, no DR, breaks shields); drains = flat per round on the victim's action, not absorbed.
    Target absorb heals back that share; attacker lifesteal heals its share; recoil ground returns 40% to the hitter.
  - base damage per action is calibrated per opponent from real logs (DMG tables below; scale by --scale).
Search: for each legal bundle of mine this round (policy.legal: AP, cooldowns, shared locks, range), simulate
  my turn + his predicted turn (enemy_model habit prediction, plus his top alternative), then my best follow-up next
  round + his next predicted turn. Score = HP swing (dealt - taken), +/-5000 for a kill/death, small credit for
  setup still live. Prints the top plans with predicted HP after each turn.

Usage:
  shotplan.py LOG ROUND --enemy Luka --battle B --dist 1 --ap 100 --my-hp N --en-hp N [--first] [--top 5]
  (LOG = the same "<round>|<effect text>" file policy.py reads; live tags are rebuilt from it.)
"""
import argparse
import copy
import json
import os
import re

import policy
from cd_plan import ACTIONS, LOADOUTS, load
from enemy_model import PROFILES, _predict

HERE = os.path.dirname(os.path.abspath(__file__))

# my actions: base damage vs an average target before his DR (calibrated from 2026-11-10 logs vs Luka/Shisui:
# Fury 649-776 under +60% given & DR35 -> ~620; Rebirth 433-689; Shrapnel 442-645; Lotus 317-776; Ember 100-682;
# kunai 194-337; basic ~150), plus the tags each applies: (who, kind, value, rounds, instant?)
MINE = {
    "rebirth": (600, [("me", "given", -0.15, 2), ("me", "absorb", 0.35, 3)]),
    "shrapnel": (600, [("en", "afterburn", 0.30, 2)]),
    "lotus": (560, [("en", "buffblock", 1, 1)]),
    "fury": (620, [("en", "recoil", 0.40, 1, True)]),
    "ember": (560, [("me", "given", 0.35, 2), ("en", "taken", 0.35, 2)]),
    "danse": (420, [("en", "seal", 1, 2, True)]),
    "stormblade": (707, [("me", "reflect", 0.35, 2)], "pierce"),
    "nights": (631, [], "pierce"),                      # no heal: the record is pierce + 2-round immunity (engine 2026-11-11)
    "resonance": (450, [("en", "stun", 20, 2, True)]),
    "leech": (0, [("en", "drain", 300, 2), ("me", "absorb", 0.21, 2)]),
    "yuki": (0, [("en", "drain", 200, 2), ("en", "given", -0.25, 2)]),
    "aetherion": (350, [("en", "taken", 0.20, 2)]),
    "kunai": (280, [("en", "wound", 30, 2)]),
    "basic": (150, []),
    "subaku": (0, [("en", "given", -0.25, 1, True), ("me", "given", 0.30, 2)]),
    "overflow": (0, [("me", "given", 0.35, 2), ("me", "given", 0.35, 2)]),
    "thunders": (0, [("me", "given", 0.30, 2), ("me", "reflect", 0.35, 2)]),
    "parry": (0, [("me", "given", 0.30, 2), ("me", "parry", 0.20, 2)]),
    # Chakra Resistance (lvl 25): -30% damage taken on me for 2 rounds; his next casts lose 10 potency (consumed as he
    # casts; modelled as -10% damage given for his next turn). Replaced Parry in PvP 1 (director 2026-11-11).
    # The potency cut is instant (engine potency(): applies when isNew, consumed by his next casts), so it hits his
    # turn later THIS round when I act first, and his next turn when I act second. The -30% taken starts next round
    # like every tag, which covers his next turn whether I act first or second. Director 2026-11-11: Seal + Chakra
    # Resistance is the emergency damage nerf (his buffs blocked, his casts weakened, my damage taken -30%).
    "resist": (0, [("me", "dr", 0.30, 2), ("en", "given", -0.10, 2, True)]),
    "eclipse": (0, [("me", "given", 0.30, 2), ("me", "lifesteal", 0.35, 2)]),
    "sealnull": (0, [("en", "buffblock", 1, 1), ("me", "debuffimmune", 1, 2)]),
    "phantom": (0, [("me", "given", 0.30, 2), ("me", "dr", 0.25, 2)]),
    "shield": (0, [("me", "shield", 500, 2, True), ("me", "absorb", 0.35, 2)]),
    "severed": (0, [("en", "healcut", 0.5, 2), ("en", "taken", 0.30, 2)]),
    "smoke": (0, [("en", "given", -0.70, 1), ("me", "given", -0.70, 1), ("me", "dr", 0.25, 2)]),
    "kims": (0, [("me", "debuffimmune", 1, 1), ("me", "clearimmune", 1, 1)]),
    "pill": (0, [("me", "given", 0.15, 2), ("me", "lifesteal", 0.20, 2)]),
    "panacea": (0, [("me", "dr", 0.25, 2)]),
    "jewel": (0, [("me", "given", 0.15, 3), ("me", "dr", 0.10, 3)]),
    "disaster": (0, [("en", "taken", 0.20, 2)]),
    "clear": (0, [("en", "clear", 1, 0, True)]),
    "cleanse": (0, [("me", "cleanse", 1, 0, True)]),
    "replace": (0, []), "step": (0, []), "defstance": (0, [("me", "dr", 0.15, 1)]),
    "offstance": (0, [("me", "given", 0.15, 1)]),
}
# his actions (Luka, from 6 logged fights): base damage before my multipliers, tags applied
ENEMY = {
    "luka": {
        "resward": (650, [("me", "taken", 0.35, 2), ("me", "recoil_self", 0.40, 2)]),
        "shieldbreak": (735, [("me", "wound", 182, 2)], "pierce"),
        "dki": (650, [("en", "given", 0.40, 2), ("me", "wound", 250, 2)]),
        "absorbhit": (450, [("en", "absorb", 0.30, 2)]),
        "decree": (330, [("me", "taken", 0.20, 2)]),
        "afterburnground": (480, []),
        "draingiven": (380, [("me", "drain", 150, 2), ("en", "given", 0.30, 2)]),
        "kunai": (220, []), "basic": (180, []), "nights": (631, [], "pierce"),
        "absorbstack": (0, [("en", "given", 0.40, 2), ("en", "absorb", 0.40, 2)]),
        "middleguard": (0, [("en", "given", 0.35, 2), ("en", "dr", 0.35, 2), ("en", "debuffimmune", 1, 1)]),
        "potency": (0, [("en", "given", 0.208, 2)]),
        "pill2": (0, [("en", "given", 0.15, 2), ("en", "lifesteal", 0.20, 2)]),
        "lsdebuff": (0, [("me", "taken", 0.30, 2), ("en", "lifesteal", 0.35, 2)]),
        "lsshield": (0, [("en", "lifesteal", 0.35, 2)]),
        "vacuum": (0, [("me", "given", -0.334, 2), ("me", "taken", 0.334, 2)]),
        "afterburnme": (0, [("me", "taken", 0.15, 2)]),
        "eternaldark": (0, [("me", "given", -0.30, 2), ("en", "dr", 0.30, 2)]),
        "echo": (0, [("me", "stun", 20, 2, True), ("me", "recoil_self", 0.35, 2)]),
        "panacea": (0, [("en", "dr", 0.25, 2)]),
        "smoke": (0, [("me", "given", -0.70, 1), ("en", "given", -0.70, 1), ("en", "dr", 0.25, 2)]),
        "clear": (0, [("me", "clear", 1, 0, True)]),
        "cleanse": (0, [("en", "cleanse", 1, 0, True)]),
        "kims": (0, [("en", "debuffimmune", 1, 1), ("en", "clearimmune", 1, 1)]),
        "phantom": (0, [("en", "given", 0.30, 2), ("en", "dr", 0.25, 2)]),
        "replace": (0, []), "healitem": (0, [("en", "heal", 700, 0, True)]),
    },
}
POSITIVE = {"given+", "absorb", "lifesteal", "reflect", "parry", "dr", "shield", "debuffimmune", "clearimmune"}


class Side:
    def __init__(self, hp):
        self.hp = hp
        self.tags = []  # [kind, value, first_round, last_round]

    def live(self, kind, r):
        return [t for t in self.tags if t[0] == kind and t[2] <= r <= t[3]]

    def mult(self, kind, r):
        m = 1.0
        for t in self.live(kind, r):
            m *= 1 + t[1]
        return m

    def total(self, kind, r):
        return sum(t[1] for t in self.live(kind, r))


GROUND_DR = float(os.environ.get("TNR_GROUND_DR", "0.20"))


def ground(t):
    """A ground effect (Subaku Palace's -damage given): it holds while I stand on the marked tiles, so Cleanse does
    not remove it; moving off does, and debuff-prevent keeps it from re-applying (director 2026-11-11, 4qua R2)."""
    return len(t) > 4 and t[4] == "ground"


def off_ground(side, rows, me_id, move_ids):
    """Drop ground tags on a side (me_id = that side's user id) once it has moved after the ground was laid (rows
    oldest-first). Subaku's -given is laid by the other side on my tile; Phantom Step's -taken by the side itself
    as it lands, so only a later move takes it off."""
    if not any(ground(t) for t in side.tags):
        return
    keep = []
    for t in side.tags:
        if ground(t):
            kind = "decreasedamagegiven" if t[0] == "given" else "decreasedamagetaken"
            r0 = t[5] if len(t) > 5 else None
            laid = [i for i, (r, u, a, ts) in enumerate(rows) if (r0 is None or r == r0)
                    and any(f"marked the ground with {kind}" in (x or "") for x in (ts or []))]
            if laid and any(i > laid[-1] and u == me_id and a in move_ids for i, (r, u, a, _) in enumerate(rows)):
                continue
        keep.append(t)
    side.tags = keep


def positive(t):
    k, v = t[0], t[1]
    return (k == "given" and v > 0) or k in POSITIVE - {"given+"}


def rebuild(lines, me_name, en_name, my_hp, en_hp):
    me, en = Side(my_hp), Side(en_hp)
    pat = [("damage given", "given"), ("damage taken", "taken"), ("will absorb", "absorb"), ("will steal", "lifesteal"),
           ("will reflect", "reflect"), ("will parry", "parry"), ("healing ability is decreased", "healcut")]
    ground_n = {}
    ground_dr_line = None
    for li, line in enumerate(lines):
        r, t = line.split("|", 1)
        r = int(r)
        g = re.match(rf"^({re.escape(en_name)}|{re.escape(me_name)}) marked the ground with decreasedamagegiven for the next (\d+) rounds", t)
        if g:
            ground_n[(r, g.group(1))] = (int(g.group(2)), li)
            continue
        g = re.match(rf"^({re.escape(en_name)}|{re.escape(me_name)}) marked the ground with decreasedamagetaken for the next (\d+) rounds", t)
        if g:
            # Phantom Step's ground (-damage taken for whoever stands on the landing tile, the caster): the log line
            # names no size and no follow-up line lands it, so it was never modelled. Korin R10-R11 2026-11-11: his
            # Phantom Step cut my R11 burst from ~1500 to 1146 and the planner fired for a kill he survived on 42 HP.
            # Size: GROUND_DR, the record's 10 + 0.4/level at level 25 = 20% (his other jutsu read at level 25 live).
            (me if g.group(1) == me_name else en).tags.append(["dr", GROUND_DR, r, r + int(g.group(2)), "ground", r, li])
            ground_dr_line = (r, g.group(1))
            continue
        if ground_dr_line and ground_dr_line == (r, t.split(" ", 1)[0]) and "damage taken" in t and "decreased" in t \
                and "next 1 rounds" in t:
            # the tile's own -taken landing on the caster this round (Ashutosh fight R7: "dauntless damage taken ...
            # decreased by up to 20% for the next 1 rounds"): it is the ground tag above, so it sets its size only
            who_g = me if ground_dr_line[1] == me_name else en
            if (m := re.search(r"([\d.]+)%", t)):
                for x in who_g.tags:
                    if ground(x) and x[0] == "dr" and x[5] == r:
                        x[1] = float(m.group(1)) / 100
            ground_dr_line = None
            continue
        who = me if t.startswith(me_name) else en if t.startswith(en_name) else None
        if who is None:
            continue
        other = en_name if who is me else me_name
        if (r, other) in ground_n and "damage given" in t and "decreased" in t:
            # the ground's -given lands on whoever stands on it each round it lasts: a ground tag, not a debuff
            n_g, li0 = ground_n.pop((r, other))
            v = float(m.group(1)) / 100 if (m := re.search(r"([\d.]+)%", t)) else 0.25
            who.tags.append(["given", -v, r + 1, r + n_g, "ground", r, li0])
            continue
        if "cleared of all positive" in t:
            who.tags = [x for x in who.tags if not positive(x) or ground(x)]
            continue
        if "cleared of all negative" in t:
            who.tags = [x for x in who.tags if positive(x)]
            continue
        n = int(m.group(1)) if (m := re.search(r"next (\d+) rounds?", t)) else 1
        v = float(m.group(1)) / 100 if (m := re.search(r"([\d.]+)%", t)) else 0
        for key, kind in pat:
            if key in t:
                if kind in ("given", "taken"):
                    if "decreased" in t:
                        kind, v = ("given", -v) if kind == "given" else ("dr", v)
                who.tags.append([kind, v, r + 1, r + n])
                break
        else:
            if "cannot be debuffed" in t:
                who.tags.append(["debuffimmune", 1, r + 1, r + n])
                if "cannot be cleared" in t:
                    who.tags.append(["clearimmune", 1, r + 1, r + n])
            elif "cannot be cleared" in t:
                # clear-prevent (Dr. Kim's, ANBU Member R3 2026-11-11: "cannot be cleared for the next 1 rounds" made my
                # R4 Clear fail with "resists being cleared"); the planner did not read it and wasted Clear
                who.tags.append(["clearimmune", 1, r + 1, r + n])
            elif "wound damage for" in t:
                who.tags.append(["wound", float(re.search(r"take ([\d.]+) wound", t).group(1)), r + 1, r + n])
            elif "will be drained" in t:
                who.tags.append(["drain", float(re.search(r"drained ([\d.]+)", t).group(1)), r + 1, r + n])
            elif "of damage received as afterburn" in t:
                # "X will take N% of damage received as afterburn": every hit on X adds N% more -> +N% taken
                who.tags.append(["taken", v, r + 1, r + n])
            elif "will recoil" in t:
                who.tags.append(["recoil_self", v, r + 1, r + n])
            elif "shield with" in t:
                who.tags.append(["shield", float(re.search(r"with ([\d.]+)", t).group(1)), r, r + n - 1])
    return me, en


def _agg(side, r):
    """One pass over a side's live tags at round r: kind -> [sum of values, product of (1 + value), product of
    (1 - value)] (speed pass: apply() used to rescan the tag list ~10 times per call)."""
    out = {}
    for t in side.tags:
        if t[2] <= r <= t[3]:
            a = out.get(t[0])
            if a is None:
                out[t[0]] = [t[1], 1 + t[1], 1 - t[1]]
            else:
                a[0] += t[1]; a[1] *= 1 + t[1]; a[2] *= 1 - t[1]
    return out


_Z = (0.0, 1.0, 1.0)


def apply(src_side, dst_side, spec, r, actor_is_me):
    """Apply one action: damage then tags. Returns (damage to target, damage to actor)."""
    base, tags = spec[0], spec[1]
    pierce = len(spec) > 2 and spec[2] == "pierce"
    to_tgt = to_self = 0.0
    # tick my own wound/drain on my first action is handled by the caller
    if base:
        sa, da = _agg(src_side, r), _agg(dst_side, r)
        parried = 0.0
        if pierce:
            dmg = base
            dst_side.tags = [t for t in dst_side.tags if t[0] != "shield"]
        else:
            dmg = base * sa.get("given", _Z)[1] * da.get("taken", _Z)[1]
            dmg *= da.get("dr", _Z)[2]
            # system DR already inside the calibrated base
            # engine order: parry splits the direct hit before shields (process.ts splitParriedDamage), cap 100%
            parried = dmg * min(1.0, da.get("parry", _Z)[0])
            dmg -= parried
            sh = da.get("shield", _Z)[0]
            if sh:
                used = min(sh, dmg)
                dmg -= used
                dst_side.tags = [t for t in dst_side.tags if t[0] != "shield"]
        dmg = max(dmg, 0.0)
        # engine (process.ts / damagePipeline.ts, constants.ts): parry's share went back above; reflect works on
        # what is left and returns at most 60% of it (REFLECT_CAP_RATIO), so two 35% reflects waste 10% and parry +
        # reflect do not add (20% + 35% returns 48%). Absorb and lifesteal are capped at 60% of the hit
        # (ABSORB_CAP_RATIO, DAMAGE_LEECH_CAP_RATIO). Director, 2026-11-11.
        heal_cut = 1 - da.get("healcut", _Z)[0]
        to_tgt += dmg - dmg * min(0.6, da.get("absorb", _Z)[0]) * heal_cut
        to_self -= dmg * min(0.6, sa.get("lifesteal", _Z)[0]) * (1 - sa.get("healcut", _Z)[0])
        to_self += dmg * sa.get("recoil_self", _Z)[0]
        to_self += dmg * sa.get("recoil", _Z)[0]  # standing on recoil ground
        to_self += parried + dmg * min(0.6, da.get("reflect", _Z)[0])
    for t in tags:
        who, kind, val, dur = t[0], t[1], t[2], t[3]
        instant = len(t) > 4 and t[4]
        side = src_side if who == ("me" if actor_is_me else "en") or (who == "me" and actor_is_me) else None
        side = src_side if (who == "me") == actor_is_me else dst_side
        if kind == "clear":
            if not side.live("clearimmune", r):
                # a ground -taken (Phantom Step) is cleared too here, for parity with planner2 (its tile puts it back
                # the next round; the log rebuild below keeps it)
                side.tags = [x for x in side.tags if not positive(x)]
            continue
        if kind == "cleanse":
            side.tags = [x for x in side.tags if positive(x) or ground(x)]
            continue
        if kind == "heal":
            if side is src_side:
                to_self -= val
            continue
        hostile = side is dst_side and (val < 0 or kind in ("taken", "wound", "drain", "recoil_self", "stun", "healcut", "seal"))
        if hostile and side.live("debuffimmune", r):
            continue
        if side is src_side and src_side.live("buffblock", r) and kind in ("given", "absorb", "lifesteal", "dr", "reflect") and val > 0:
            continue
        first, last = (r, r + max(dur, 1) - 1) if instant else (r + 1, r + dur)
        side.tags.append([kind, val, first, last])
    return to_tgt, to_self


def run_turn(actor, other, acts, kit, r, actor_is_me):
    dealt = taken = 0.0
    if acts:  # wound + drain tick on the first action of the turn
        taken += actor.total("wound", r) + actor.total("drain", r)
    for a in acts:
        spec = kit.get(a)
        if spec is None:
            continue
        d, s = apply(actor, other, spec, r, actor_is_me)
        dealt += d
        taken += s
    other.hp -= dealt
    actor.hp -= taken
    return dealt, taken


def enemy_options(enemy, battle, r):
    bundle, threats, ready, kit, cands = _predict(enemy, battle, r)
    alt = [a for s, a in cands if a not in bundle][:2]
    opts = [bundle]
    if alt:
        opts.append(alt)
    return opts


def score(me, en, my0, en0):
    s = (en0 - en.hp) - (my0 - me.hp)
    if en.hp <= 0:
        s += 5000
    if me.hp <= 0:
        s -= 5000
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log"); ap.add_argument("round", type=int)
    ap.add_argument("--enemy", required=True); ap.add_argument("--battle", required=True)
    ap.add_argument("--dist", type=int, default=1); ap.add_argument("--ap", type=int, default=100)
    ap.add_argument("--my-hp", type=float, required=True); ap.add_argument("--en-hp", type=float, required=True)
    ap.add_argument("--first", action="store_true"); ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    lines = [l.strip() for l in open(a.log) if "|" in l]
    opp = a.enemy.lower()
    ekit = ENEMY.get(opp, ENEMY["luka"])
    mykit = {k: ((v[0] * a.scale,) + v[1:]) for k, v in MINE.items()}
    st = load(a.battle)
    me0, en0 = rebuild(lines, "dauntless", a.enemy, a.my_hp, a.en_hp)
    R = a.round
    ap_now = a.ap - (20 if me0.live("stun", R) else 0)
    bundles = policy.legal(st, R, ap_now, bool(en0.live("debuffimmune", R)), set(), st["loadout"], a.dist)
    his_now = enemy_options(opp, a.battle, R) if opp in PROFILES else [["basic"]]
    his_next = enemy_options(opp, a.battle, R + 1) if opp in PROFILES else [["basic"]]
    results = []
    for b in bundles:
        worst = None
        for h in his_now:
            me, en = copy.deepcopy(me0), copy.deepcopy(en0)
            log = []
            if a.first:
                d, t = run_turn(me, en, list(b), mykit, R, True); log.append(("me", R, b, d, t, me.hp, en.hp))
                if en.hp > 0:
                    d, t = run_turn(en, me, h, ekit, R, False); log.append(("him", R, h, d, t, me.hp, en.hp))
            else:
                d, t = run_turn(me, en, list(b), mykit, R, True); log.append(("me", R, b, d, t, me.hp, en.hp))
                if en.hp > 0:
                    d, t = run_turn(en, me, his_next[0], ekit, R + 1, False); log.append(("him", R + 1, his_next[0], d, t, me.hp, en.hp))
            # greedy follow-up next round: best single high-value bundle among simple options (ignores cooldown detail)
            if me.hp > 0 and en.hp > 0:
                best_f = None
                for f in (("rebirth", "kunai", "pill"), ("fury", "parry"), ("stormblade", "thunders"), ("nights", "ember"),
                          ("leech", "jewel", "pill"), ("ember", "overflow"), ("clear", "sealnull"), ("cleanse", "shield")):
                    if not all(x in st["loadout"] for x in f) or any(x in b for x in f):
                        continue
                    m2, e2 = copy.deepcopy(me), copy.deepcopy(en)
                    run_turn(m2, e2, list(f), mykit, R + 1, True)
                    v = (en.hp - e2.hp) - (me.hp - m2.hp) + (5000 if e2.hp <= 0 else 0)
                    if best_f is None or v > best_f[0]:
                        best_f = (v, f)
                follow = best_f
            else:
                follow = None
            sc = score(me, en, a.my_hp, a.en_hp) + (0.5 * follow[0] if follow else 0)
            if worst is None or sc < worst[0]:
                worst = (sc, log, follow, h)
        results.append((worst[0], b, worst))
    results.sort(key=lambda t: -t[0])
    print(f"round {R}: {len(bundles)} legal bundles, me {a.my_hp:.0f} / him {a.en_hp:.0f}, AP {ap_now}; "
          f"his likely now {his_now}, next {his_next[0]}")
    for sc, b, (s, log, follow, h) in results[:a.top]:
        steps = "; ".join(f"{w} R{r} {'+'.join(x)}: dealt {d:.0f} self {t:+.0f} -> me {mh:.0f}/him {eh:.0f}"
                          for w, r, x, d, t, mh, eh in log)
        fu = f" | then {'+'.join(follow[1])} ({follow[0]:+.0f})" if follow else ""
        print(f"{sc:+7.0f}  {'+'.join(b):32s} vs his {'+'.join(h)} :: {steps}{fu}")


if __name__ == "__main__":
    main()
