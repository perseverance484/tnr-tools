#!/usr/bin/env python3
"""One-call PvP turn planner (director, 2026-11-10: "I dont want you spending 30+ seconds a turn trying to sort out your
next move, you should have a planner that does that and you pick the highest value moves with a forecast for next
rounds for both you and the opponent").

Each turn: save the two connector responses into ONE file (two lines), run this, fire the printed actions in order.
  line 1: combat.getBattle {battleId} with select
          ["battle.version","battle.round","battle.activeUserId","battle.usersState.*.userId",
           "battle.usersState.*.username","battle.usersState.*.curHealth","battle.usersState.*.maxHealth",
           "battle.usersState.*.longitude","battle.usersState.*.latitude","battle.usersState.*.actionPoints"]
  line 2: combat.getBattleEntries {battleId, limit: 200} with select
          ["*.battleRound","*.userId","*.actionId","*.appliedEffects.*.txt"]
Usage: turn.py FILE --battle ID [--enemy NAME] [--loadout pvp1|pvp2] [--top 3]

What it does (no live calls, no guessing):
  - positions, HP and AP by USERNAME (never by array order), hex distance, who acts first this round, my stun;
  - my cooldowns from my own logged actions (engine actions.ts: usable when round - lastUsedRound >= cooldown) plus
    shared tag locks, written to the cd_plan state so policy.legal only offers usable bundles;
  - live/upcoming tags on both sides (cast in round N = live N+1 .. N+k), enemy resources spent (Clear, Cleanse, Smoke,
    Kim's, pierce) and his average damage per turn so far;
  - every legal bundle simulated with shotplan's engine model and scored by value_model.py (2026-11-11 rework):
    calibrated base damage (calibration.json), his reply as a weighted option set (turn / burst / setup / pierce /
    Clear / Smoke / summon, weights = smoothed logged frequencies), 0.7 expected + 0.3 worst case, then my best
    follow-up next round (x0.8) against his median turn; Cleanse / Clear / Smoke carry reserve costs; explicit guards
    only for lethal ticks, extra basic steps and pierce (no window / into absorb);
  - prints the top bundles in firing order with exact target hexes, plus the 2-round HP forecast for both sides.
"""
import argparse
import copy
import json
import os
import pickle
import re
import sys
import threading


def par_map(fn, items, n=None):
    """[fn(x) for x in items] split across n forked workers (closures work: fork copies the process). Falls back to
    serial on one core, few items, or any worker failure."""
    # opt-in: this container gives one effective core, so forking only adds overhead (measured 2026-11-11)
    n = n or int(os.environ.get("TNR_PLANNER_WORKERS", "1"))
    if n < 2 or len(items) < 4 or not hasattr(os, "fork"):
        return [fn(x) for x in items]
    kids = []
    for k in range(n):
        r, w = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(r)
            try:
                data = pickle.dumps([(i, fn(items[i])) for i in range(k, len(items), n)])
            except BaseException:  # noqa: BLE001
                data = pickle.dumps(None)
            with os.fdopen(w, "wb") as f:
                f.write(data)
            os._exit(0)
        os.close(w)
        kids.append((pid, r))
    out, ok = [None] * len(items), True
    for pid, r in kids:
        with os.fdopen(r, "rb") as f:
            part = pickle.loads(f.read() or pickle.dumps(None))
        os.waitpid(pid, 0)
        if part is None:
            ok = False
            continue
        for i, v in part:
            out[i] = v
    return out if ok else [fn(x) for x in items]


# tag kinds that apply()'s damage step or its tag guards read in the SAME round: an action that adds one of these
# with an instant start changes what later actions in its bundle see (ply2 fast path falls back to the full sim)
_READ_SRC = {"given", "lifesteal", "healcut", "recoil_self", "recoil", "buffblock"}
_READ_DST = {"taken", "dr", "shield", "healcut", "absorb", "reflect", "parry", "debuffimmune", "clearimmune"}
_AGG_KINDS = ("given", "taken", "dr", "shield", "healcut", "absorb", "lifesteal", "recoil_self", "recoil", "reflect",
              "parry", "wound", "drain")


def _contrib(tags, r):
    """Per-kind [sum, prod(1+v), prod(1-v)] of the tags live at round r (a follow-up action's own share)."""
    out = {}
    for t in tags:
        if t[2] <= r <= t[3] and t[0] in _AGG_KINDS:
            a = out.get(t[0])
            if a is None:
                out[t[0]] = [t[1], 1 + t[1], 1 - t[1]]
            else:
                a[0] += t[1]; a[1] *= 1 + t[1]; a[2] *= 1 - t[1]
    return out


def _combine(base, parts):
    out = {k: list(v) for k, v in base.items()}
    for p in parts:
        for k, v in p.items():
            a = out.get(k)
            if a is None:
                out[k] = list(v)
            else:
                a[0] += v[0]; a[1] *= v[1]; a[2] *= v[2]
    return out


def _pure_reply(sa, da, bases):
    """His pure-damage turn as arithmetic (same steps as shotplan.apply for a (base, []) spec, then run_turn):
    returns (damage to me, damage to him). sa = his aggregates, da = mine, at his reply round."""
    z = (0.0, 1.0, 1.0)
    g = lambda d, k: d.get(k, z)
    taken_self = g(sa, "wound")[0] + g(sa, "drain")[0] if bases else 0.0
    dealt = 0.0
    shield = g(da, "shield")[0]
    for base in bases:
        if not base:
            continue
        dmg = base * g(sa, "given")[1] * g(da, "taken")[1] * g(da, "dr")[2]
        if shield:
            dmg -= min(shield, dmg)
            shield = 0.0
        dmg = max(dmg, 0.0)
        heal_cut = 1 - g(da, "healcut")[0]
        dealt += dmg - dmg * min(0.9, g(da, "absorb")[0]) * heal_cut
        taken_self -= dmg * g(sa, "lifesteal")[0] * (1 - g(sa, "healcut")[0])
        taken_self += dmg * g(sa, "recoil_self")[0] + dmg * g(sa, "recoil")[0]
        taken_self += dmg * g(da, "reflect")[0] + dmg * g(da, "parry")[0]
    return dealt, taken_self


def _vec(sa, da):
    """The 13 numbers his pure-damage reply reads. sa/da = kind -> [sum, prod(1+v), prod(1-v)] for him / me."""
    z = (0.0, 1.0, 1.0)
    g = lambda d, k: d.get(k, z)
    return [g(sa, "given")[1], g(sa, "wound")[0] + g(sa, "drain")[0], g(sa, "lifesteal")[0], g(sa, "healcut")[0],
            g(sa, "recoil_self")[0] + g(sa, "recoil")[0],
            g(da, "taken")[1], g(da, "dr")[2], g(da, "shield")[0], g(da, "healcut")[0], g(da, "absorb")[0],
            g(da, "reflect")[0], g(da, "parry")[0]]


_MULT_IDX = (0, 5, 6)   # entries combined by product; the rest by sum


def _reply_vec(v, bases):
    """_pure_reply on a flat vector (same arithmetic)."""
    gm, tick, ls, hc_s, rec, tm, drp, shield, hc_d, ab, refl, par = v
    taken_self = tick if bases else 0.0
    dealt = 0.0
    for base in bases:
        if not base:
            continue
        dmg = base * gm * tm * drp
        parried = dmg * min(1.0, par)              # same order and caps as shotplan.apply
        dmg -= parried
        if shield:
            dmg -= min(shield, dmg)
            shield = 0.0
        dmg = max(dmg, 0.0)
        dealt += dmg - dmg * min(0.6, ab) * (1 - hc_d)
        taken_self -= dmg * min(0.6, ls) * (1 - hc_s)
        taken_self += dmg * rec
        taken_self += parried + dmg * min(0.6, refl)
    return dealt, taken_self


_RESERVE_CACHE = {}   # (round, cal id) -> {bundle: reserve cost}; cal is loaded once per run
_REPLY_READ = {"given", "taken", "dr", "shield", "healcut", "absorb", "lifesteal", "recoil_self", "recoil",
               "reflect", "parry", "wound", "drain", "debuffimmune", "buffblock", "clearimmune"}
_READ = {"given", "taken", "dr", "shield", "healcut", "absorb", "lifesteal", "recoil_self", "recoil", "reflect",
         "parry", "debuffimmune", "clearimmune", "buffblock"}


def _burst_g(m2, e2, R):
    """Multipliers cast this turn (live from R+1) still live in R+2: my given x his taken (ply2's burst term)."""
    g = 1.0
    for t in m2.tags:
        if t[0] == "given" and t[2] <= R + 1 and t[2] <= R + 2 <= t[3]:
            g *= 1 + t[1]
    for t in e2.tags:
        if t[0] == "taken" and t[2] <= R + 1 and t[2] <= R + 2 <= t[3]:
            g *= 1 + t[1]
    return g

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cd_plan  # noqa: E402
import shotplan  # noqa: E402
import value_model  # noqa: E402
import engine_bridge  # noqa: E402
from ingest import IDS, ME  # noqa: E402
from policy import legal  # noqa: E402
import policy  # noqa: E402

ME_NAME = "dauntless"
GRID_W, GRID_H = 13, 9

# firing order inside a turn: reposition, strip/lock, defensive locks, buffs, damage, fillers, kite step last
ORDER = ["cleanse", "phantom", "replace", "step", "clear", "sealnull", "kims", "smoke", "ember", "overflow", "thunders",
         "parry", "eclipse", "pill", "jewel", "subaku", "severed", "disaster", "shield", "panacea", "lotus", "danse",
         "shrapnel", "fury", "rebirth", "resonance", "leech", "yuki", "stormblade", "nights", "aetherion", "kunai",
         "basic", "basicheal", "defstance", "offstance", "stepback"]
SELF_T = {"overflow", "thunders", "parry", "eclipse", "shield", "pill", "jewel", "panacea", "kims", "defstance",
          "offstance", "basicheal", "cleanse"}
AOE = {"fury", "shrapnel"}
BUFFS = {"overflow", "thunders", "parry", "eclipse", "pill", "jewel", "ember", "phantom"}
ACTION_ID = {v: k for k, v in IDS.items()}
GROUND_EXIT = {"phantom", "replace", "step"}
# Near-kill rules (director 2026-11-11 after Korin R11, "Make all three"): the quick forecast ran ~25% hot there (his
# Phantom Step ground was not modelled) and the planner fired for a kill he survived on 42 HP.
# KILL_MARGIN: a python-forecast kill counts as sure only with this much overkill (forecast x (1 - margin) >= his HP);
# below that it is a chance, blended with the line where he lives, so bundles that add damage win a close kill.
# ENGINE_MARGIN: the same for the engine re-score, which was ~3.6% off on that turn. NEAR_KILL_HP: at or below this
# HP the engine re-score runs even in --fast (live) mode and its numbers replace the quick estimate.
KILL_MARGIN = float(os.environ.get("TNR_KILL_MARGIN", "0.12"))
ENGINE_MARGIN = float(os.environ.get("TNR_ENGINE_MARGIN", "0.05"))
NEAR_KILL_HP = float(os.environ.get("TNR_NEAR_KILL_HP", "2000"))
# Fillers and moves (director 2026-11-11, Ashutosh fight: "Its using basic attack and the stances an awful lot when I
# see those as situational"; "it used replacement technique when it was already in range along with a basic attack").
# FILLER_COST: each basic attack / stance pays this, so it is picked only when it clearly wins or nothing else fits
# the AP. MOVE_COST: a Replacement that buys no range (for anything but a basic) and no clear line past a barrier.
FILLER_COST = float(os.environ.get("TNR_FILLER_COST", "60"))
MOVE_COST = float(os.environ.get("TNR_MOVE_COST", "200"))
FILLERS = ("basic", "defstance", "offstance")
BARRIERS = []        # live barriers: (x, y, hp, absorb share, creatorId), set by main() from the ground list
HOSTILE = set()      # tiles under his harmful ground (Subaku Palace's -given, recoil, +taken...), set by main()
HOSTILE_KINDS = {"decreasedamagegiven", "increasedamagetaken", "recoil", "stun", "damage", "poison", "seal",
                 "decreaseheal", "drain", "wound", "afterburn"}


def barrier_between(a, b):
    """[hp, absorb] of the barriers on a shortest path from a to b (the engine's getBarriersBetween walks one shortest
    path; any shortest path counts here, the cautious read), or None for a clear line. My own barriers do not block."""
    hit = [x for x in BARRIERS if x[4] != ME and (x[0], x[1]) not in (a,) and dist(a, (x[0], x[1])) +
           dist((x[0], x[1]), b) == dist(a, b)]
    if not hit:
        return None
    keep = 1.0
    for x in hit:
        keep *= 1 - x[3]
    return [sum(x[2] for x in hit), 1 - keep]


def _guard(m, R, at=None):
    """My damage cuts cast by this turn (live from R+1) still live at round `at` (default R+2): the share of his
    turn there they stop (director 2026-11-11: Panacea's second round went uncounted, so Defensive Stance looked as
    good). The caller picks `at` = his first reply the simulation has NOT already played (Luka fight 2026-11-11: the
    credit was read at the reply ply2 had already simulated with the cut in place, so it was counted twice)."""
    at = R + 2 if at is None else at
    k = 1.0
    for t in m.tags:
        if t[0] == "dr" and t[2] <= R + 1 and t[2] <= at <= t[3]:
            k *= 1 - t[1]
    return 1 - k


def _guard_val(m, e, R, at, m0, turn, p_clear=0.0):
    """What my new cuts are worth on his next unsimulated turn: his TYPICAL turn (not his best burst) x the
    multipliers he will hit with there (his damage-given stack, my damage-taken), so a cut is worth more against a
    stacked opponent (director 2026-11-11, Luka R1: "you didn't put up any damage reduction vs his dmg inc")."""
    g = _guard(m, R, at) - _guard(m0, R, at)
    if g <= 0:
        return 0.0
    return value_model.GAMMA * turn * e.mult("given", at) * m.mult("taken", at) * g * (1 - p_clear)


def _mit(e, at, afb=None, cap=None):
    """His side of my next hit at round `at`: the share of it that sticks after his damage cuts and his absorb heal,
    plus my afterburn on him (engine process.ts: afterburn is a share of the same hit added outside the absorb, so
    an afterburn as big as his absorb cancels it; director 2026-11-11 Luka: "1 afterburn stack would've canceled it
    out totally"). afb overrides the afterburn share; cap counts only afterburn cast by that round."""
    k, ab, hc, aft = 1.0, 0.0, 0.0, 0.0
    for t in e.tags:
        if t[2] <= at <= t[3]:
            if t[0] == "dr":
                k *= 1 - t[1]
            elif t[0] == "absorb":
                ab += t[1]
            elif t[0] == "healcut":
                hc += t[1]
            elif t[0] == "afterburn" and (cap is None or t[2] <= cap):
                aft += t[1]
    if afb is not None:
        aft = afb
    return k * (1 + min(0.6, aft) - min(0.6, ab) * max(0.0, 1 - hc))


def _mult_by(side, kind, at, cap):
    m = 1.0
    for t in side.tags:
        if t[0] == kind and t[2] <= cap and t[2] <= at <= t[3]:
            m *= 1 + t[1]
    return m


def _off_val(m, e, R, at, base, m0=None, e0=None, p_clear=0.0):
    """What my damage multipliers (my given, his taken, my afterburn on him) cast by R+1 and live at my next
    unsimulated attack `at` add to a typical hit, AFTER his cuts and absorb there (director 2026-11-11, Luka R1:
    four damage stacks into his absorb were worth far less than they were scored). Baseline: m0/e0's stack (stage 1)
    or a plain hit into his defences (ply2)."""
    cap = R + 1
    g_me = _mult_by(m, "given", at, cap)
    if p_clear:
        # his held Clear before my payoff wipes my buffs (Luka R3, 2026-11-11) but not my debuffs on him: the
        # afterburn / damage-taken I put on him survive it, my damage-given stacks do not
        g_neg = 1.0
        for t in m.tags:
            if t[0] == "given" and t[1] < 0 and t[2] <= cap and t[2] <= at <= t[3]:
                g_neg *= 1 + t[1]
        g_me = (1 - p_clear) * g_me + p_clear * g_neg
    v1 = g_me * _mult_by(e, "taken", at, cap) * _mit(e, at, cap=cap)
    if m0 is not None:
        k0 = _mit(e, at, afb=sum(t[1] for t in e0.tags if t[0] == "afterburn" and t[2] <= at <= t[3]))
        v0 = m0.mult("given", at) * e0.mult("taken", at) * k0
    else:
        v0 = _mit(e, at, afb=0.0)
    return value_model.GAMMA * base * max(0.0, v1 - v0)


def kill_chance(dealt, hp, margin):
    """Chance a forecast kill is real: 1 when dealt x (1 - margin) >= hp, 0.5 at dealt == hp, 0 below."""
    if dealt < hp or hp <= 0:
        return 0.0 if hp > 0 else 1.0
    sure = hp / (1 - margin)
    return 1.0 if dealt >= sure else 0.5 + 0.5 * (dealt - hp) / (sure - hp)


def _equipped_thrown():
    """The thrown weapon equipped now (fights/live/equipped.json, written by the pilot's restock pass): the planners'
    "kunai" action fires it. Bloodthorn adds a wound; an elemental/plain kunai is damage only."""
    try:
        eq = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fights", "live",
                                          "equipped.json")))
    except (OSError, ValueError):
        return
    tid = eq.get("THROWN")
    if not tid or tid == ACTION_ID.get("kunai"):
        return
    ACTION_ID["kunai"] = tid
    IDS[tid] = "kunai"
    try:
        rec = engine_bridge._records().get(tid, {}).get("record", {})
        p = sum((e.get("power") or 0) + (e.get("powerPerLevel") or 0) * 25 for e in rec.get("effects", [])
                if e.get("type") in ("damage", "elementaldamage"))
        if p:
            shotplan.MINE["kunai"] = (p * 13.3, [])
    except Exception:  # noqa: BLE001
        pass
MOVE_IDS = {k for k, v in IDS.items() if v in GROUND_EXIT}
ACTION_ID.update({"kunai": "yVNeLzxHSFkNpTPnlm7yQ", "basicheal": "basicHeal", "step": "move", "stepback": "move"})


# ---------------------------------------------------------------- hex helpers (odd-q, same as hx.py)
def cube(c, r):
    x = c
    z = r - (c - (c & 1)) // 2
    return x, -x - z, z


def dist(a, b):
    a, b = cube(*a), cube(*b)
    return max(abs(a[i] - b[i]) for i in range(3))


def hexes():
    return [(x, y) for x in range(GRID_W) for y in range(GRID_H)]


def neighbours(p):
    return [h for h in hexes() if dist(h, p) == 1]


# ---------------------------------------------------------------- input
def load_input(path):
    lines = [l for l in open(path).read().splitlines() if l.strip()]
    battle = json.loads(lines[0])
    ents = json.loads(lines[1]) if len(lines) > 1 else {}
    us = {k.split(".")[-1]: v for k, v in battle.items() if k.startswith("battle.usersState")}
    people = []
    for i, uid in enumerate(us["userId"]):
        people.append({k: us[k][i] for k in us})
    for p in people:                  # permanent effects read at battle start (bloodline, gear, titles, meals)
        p["perm"] = [e for e in battle.get("battle.permEffects") or [] if e.get("targetId") == p["userId"]]
    me = next(p for p in people if p["userId"] == ME)
    others = [p for p in people if p["userId"] != ME and p["curHealth"] > 0]
    rows = []
    if ents:
        effs = ents.get("*.appliedEffects.*.txt", [])
        rows = list(zip(ents["*.battleRound"], ents["*.userId"], ents["*.actionId"], effs))[::-1]  # oldest first
    return battle, me, others, rows


def my_history(rows):
    used = []
    for r, u, a, _ in rows:
        if u == ME and a in IDS:
            n = IDS[a]
            if n in ("step",):
                continue
            used.append([r, n])
    return used


def enemy_resources(rows, en_id, rnd):
    spent = {}
    pierce_last = None
    turns, dmg = 0, 0.0
    by_round = {}
    for r, u, a, t in rows:
        if u != en_id:
            continue
        txt = " ".join(t or [])
        if a == "clear":
            spent["clear"] = r
        elif a == "cleanse":
            spent["cleanse"] = r
        if "Elite Smoke" in txt or ("damage given [all damage] is decreased by up to 70%" in txt and ME_NAME in txt):
            spent["smoke"] = r
        if "cannot be cleared" in txt:
            spent["kims"] = r
        if "pierced" in txt or a in ("osJq3k77YPGoFWgof12FQ", "G6MRbppaDZ2a5Wr0GIjH8") or "immunity to buff prevention" in txt:
            pierce_last = r
        for m in re.finditer(rf"{ME_NAME} takes ([\d.]+) (?:damage|afterburn damage|wound damage)", txt):
            by_round[r] = by_round.get(r, 0) + float(m.group(1))
    if by_round:
        turns = len(by_round)
        dmg = sum(by_round.values()) / turns
    return spent, pierce_last, dmg


# ---------------------------------------------------------------- planning
def generic_enemy(avg):
    base = max(500.0, avg or 900.0) / 2  # two hits per turn
    return {"hit": (base, []), "hit2": (base, []), "basic": (150, [])}


def place_phantom(me_pos, en_pos, need, occupied):
    """Phantom/Replacement landing hex: within 5 of me, at distance == need from him if possible, else closest."""
    best = None
    for h in hexes():
        if h in occupied or dist(h, me_pos) > 5 or h == en_pos or h == me_pos:
            continue
        d = dist(h, en_pos)
        # in range first, off his harmful floor (director 2026-11-11, ANBU Member's Subaku Palace), then a clear line
        # past his barriers (Ashutosh R6), then the range wanted, then the shortest hop
        key = ((d - need + 10) if d > need else 0, h in HOSTILE, barrier_between(h, en_pos) is not None, abs(d - need),
               dist(h, me_pos))
        if best is None or key < best[0]:
            best = (key, h)
    return best[1] if best else me_pos


def place_away(me_pos, en_pos, occupied):
    """Disengage landing hex (move fired last): off his harmful floor, then as far from him as a 5-hex hop goes."""
    best = None
    for h in hexes():
        if h in occupied or dist(h, me_pos) > 5 or h == en_pos or h == me_pos:
            continue
        key = (h in HOSTILE, -min(dist(h, en_pos), 6), dist(h, me_pos))
        if best is None or key < best[0]:
            best = (key, h)
    return best[1] if best else me_pos


def moves_last(bundle, d0):
    """Phantom Step / Replacement while already engaged (director 2026-11-11: "It is a gap closer initiation tool or a
    disengagement tool... attack then move out of range"): when every targeted action already reaches from where I
    stand, the move fires last and disengages. Only when something needs the range does it fire first."""
    if not any(x in ("phantom", "replace") for x in bundle):
        return False
    reach = [cd_plan.RANGE[x] for x in bundle if cd_plan.RANGE.get(x, 0)]
    # attack, then move out: a bundle with nothing to fire at him keeps the old placement (replays 2026-11-11: a bare
    # buff + Phantom disengage, Ashutosh R3, scored 588 below Panacea + Rebirth)
    return bool(reach) and min(reach) >= d0


def step_toward(p, goal, occupied, away=False):
    cands = [h for h in neighbours(p) if h not in occupied]
    if not cands:
        return p
    return (max if away else min)(cands, key=lambda h: (dist(h, goal), h))


def resolve_targets(bundle, me_pos, en_pos, occupied):
    """Turn a bundle into ordered (action, actionId, (x, y)) steps with real hexes; moves first, kite step last."""
    last = moves_last(bundle, dist(me_pos, en_pos))
    seq = sorted(bundle, key=lambda a: (last and a in ("phantom", "replace"), ORDER.index(a) if a in ORDER else 50))
    ranged = [cd_plan.RANGE.get(a, 0) for a in seq if cd_plan.RANGE.get(a, 0)]
    # range 4 does not stop his jutsu (most are range 4), so with nothing to reach just stay where I am
    need = min(ranged) if ranged else max(1, dist(me_pos, en_pos))
    pos = me_pos
    out = []
    for a in seq:
        if a in ("phantom", "replace") and last:
            pos = place_away(pos, en_pos, occupied)
            tgt = pos
        elif a in ("phantom", "replace"):
            pos = place_phantom(pos, en_pos, need, occupied)
            tgt = pos
        elif a == "step":
            pos = step_toward(pos, en_pos, occupied)
            tgt = pos
        elif a == "stepback":
            pos = step_toward(pos, en_pos, occupied, away=True)
            tgt = pos
        elif a in SELF_T:
            tgt = pos
        else:
            tgt = en_pos
        out.append((a, ACTION_ID.get(a, a), tgt))
    return out, pos


def _prod(xs):
    p = 1.0
    for x in xs:
        p *= x
    return p


def penalties(bundle, ctx, cal):
    """Explicit guards only; everything else is priced by value_model (enemy options, lookahead, reserves)."""
    p, why = 0.0, []
    # hard rule (2026-11-11): every Chakra Shield cast while the enemy's pierce could be ready got pierced
    # (Ziharkk R2, Korin R4, Slyrak R2, Hikuro R1 rematch): never shield into a possible pierce
    if "shield" in bundle and ctx["pierce_ready"]:
        p -= 3000; why.append("Shield into a possibly-ready pierce (hard rule: 4/4 pierced)")
    steps = bundle.count("step")
    if steps > 1:
        p -= 60 * (steps - 1); why.append(f"{steps} basic steps (use Phantom/Replacement)")
    pierce = [x for x in bundle if x in ("nights", "stormblade")]
    if pierce and not ctx["pierce_window"]:
        c = value_model.reserves(cal)[pierce[0]]
        p -= c; why.append(f"pierce spent with no smoke/shield/DR window (-{c:.0f})")
    # director: absorb applies after damage processing and heals back pierce too (tags.ts absorb()); avoid if possible
    if pierce and ctx["en_absorb"] >= 0.2:
        c = ctx["en_absorb"] * 631
        p -= c; why.append(f"pierce into his {ctx['en_absorb']:.0%} absorb (-{c:.0f}, Clear it first)")
    # director 2026-11-11 (ANBU Member R3: Panacea + Basic Heal at 3404/5050 HP instead of a smoke-proof pierce): a
    # heal far from danger buys nothing; above 60% HP a Basic Heal is worth a fraction of its 600
    if "basicheal" in bundle and ctx["my_hp"] > 0.6 * ctx.get("my_max", 5050):
        p -= 450; why.append("Basic Heal above 60% HP (-450)")
    fill = [x for x in bundle if x in FILLERS]
    if fill and FILLER_COST:
        p -= FILLER_COST * len(fill); why.append(f"filler {'+'.join(fill)} (-{FILLER_COST * len(fill):.0f})")
    if "replace" in bundle and "d0" in ctx:
        reach = [cd_plan.RANGE[x] for x in bundle if cd_plan.RANGE.get(x) and x != "basic"]
        if not ((reach and ctx["d0"] > min(reach)) or ctx.get("line_blocked")):
            p -= MOVE_COST; why.append(f"Replacement buys no range or clear line (-{MOVE_COST:.0f})")
    if ctx["tick"] >= ctx["my_hp"] - 50 and "cleanse" not in bundle:
        p -= 6000; why.append(f"wound/drain tick {ctx['tick']:.0f} kills me: Cleanse FIRST")
    return p, why



PIERCE_IDS = {"osJq3k77YPGoFWgof12FQ", "G6MRbppaDZ2a5Wr0GIjH8"}


def observed_turns(rows, en_id, en_name, me_side, en_side):
    """His base damage per turn: each logged direct hit on me divided by the multipliers live at that round (his given
    x my taken x my reductions), summed per turn. Pierce is flat and skipped. Clears drop tags from the rebuild, so a
    turn right after a Clear reads slightly high (an overestimate is the safe side)."""
    per_turn = {}
    for r, u, a, ts in rows:
        if u != en_id or a in PIERCE_IDS:
            continue
        for t in ts or []:
            m = re.match(rf"^{re.escape(ME_NAME)} takes ([\d.]+) damage$", t.strip())
            if not m:
                continue
            mult = en_side.mult("given", r) * me_side.mult("taken", r)
            for tag in me_side.live("dr", r):
                mult *= 1 - tag[1]
            per_turn[r] = per_turn.get(r, 0.0) + float(m.group(1)) / max(0.15, mult)
    return [v for v in per_turn.values() if v >= 100]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--battle", required=True)
    ap.add_argument("--enemy"); ap.add_argument("--loadout", default="pvp1"); ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--no-engine", action="store_true", help="skip the exact engine re-score (harness/pvp_turn)")
    ap.add_argument("--fast", action="store_true", help="my-turn mode: engine legality in parallel, no engine re-score, shortlist 10+4")
    ap.add_argument("--keep", type=int, default=0); ap.add_argument("--cash", type=int, default=4)
    ap.add_argument("--ban", default="", help="action ids or short names the game refused this battle")
    a = ap.parse_args()
    battle, me, others, rows = load_input(a.file)
    if not others:
        print("no living enemy"); return
    summoned = {m.group(1) for _, _, _, ts in rows for t in (ts or []) if (m := re.search(r"^\s*(\S+) was summoned", t))}
    players = [p for p in others if p["username"].strip() not in summoned] or others
    en = players[0] if not a.enemy else next((p for p in others if p["username"].lower() == a.enemy.lower()), others[0])
    R = battle["battle.round"]
    my_turn = battle["battle.activeUserId"] == ME
    en_acted = any(r == R and u == en["userId"] for r, u, _, _ in rows)
    me_pos, en_pos = (me["longitude"], me["latitude"]), (en["longitude"], en["latitude"])
    d0 = dist(me_pos, en_pos)
    BARRIERS[:] = [(g["longitude"], g["latitude"], float(g.get("curHealth") or 0), float(g.get("absorbPercentage") or 0) / 100,
                    g.get("creatorId")) for g in battle.get("battle.groundEffects") or []
                   if g.get("type") == "barrier" and float(g.get("curHealth") or 0) > 0]
    occupied = {(p["longitude"], p["latitude"]) for p in others} | {(x[0], x[1]) for x in BARRIERS}
    HOSTILE.clear()
    HOSTILE.update((g["longitude"], g["latitude"]) for g in battle.get("battle.groundEffects") or []
                   if g.get("type") in HOSTILE_KINDS and g.get("creatorId") == en["userId"])

    # cooldown state from my own log
    st = {"loadout": list(cd_plan.LOADOUTS[a.loadout]) + ["basicheal"], "used": my_history(rows)}
    _ban = {x for x in a.ban.split(",") if x}
    _ban |= {IDS.get(x, x) for x in _ban}
    st["loadout"] = [n for n in st["loadout"] if n not in _ban and ACTION_ID.get(n) not in _ban]
    cd_plan.ACTIONS.setdefault("basicheal", (60, 5, None, "heal 600 instant"))
    shotplan.MINE.setdefault("basicheal", (0, [("me", "heal", 600, 0, True)]))
    cd_plan.save(a.battle, st)

    lines = [f"{r}|{t.strip()}" for r, u, _, ts in rows for t in (ts or [])]
    me0, en0 = shotplan.rebuild(lines, ME_NAME, en["username"], me["curHealth"], en["curHealth"])
    shotplan.off_ground(me0, rows, ME, MOVE_IDS)
    shotplan.off_ground(en0, rows, en["userId"], MOVE_IDS)
    _gm = (engine_bridge.opponent_kit(en["userId"]) or {}).get("gearMods") or {}
    _his_gear_dr = float(_gm.get("drTakenFromGear", 15))   # measured, else the endgame assumption (Kaeruun + Fortify III)
    # a stun costs AP in the 2 rounds AFTER the one it was cast in. The engine (turn.ts calcApReduction ->
    # getActiveTargetEffects) skips effects with castThisRound, so his stun earlier THIS round costs nothing now:
    # DDX R5 and Warlord40 R2 (2026-11-11) both had the full 100 AP after a same-round stun, and the planner's
    # 80 AP left 20 unspent (DDX R5: Phantom+kunai+Defensive Stance planned, Chakra Pill tacked on after).
    stunned = any("dauntless is stunned" in l and R - 2 <= int(l.split("|")[0]) < R for l in lines) \
        or bool(me0.live("stun", R))
    # the stun's size is in the log ("stunned [-10 AP]"; arena 2026-11-11: a -10 stun was planned as -20, 10 AP lost)
    stun_amt = max([int(m.group(1)) for l in lines if (m := re.search(r"dauntless is stunned \[-(\d+) AP\]", l))
                    and R - 2 <= int(l.split("|")[0]) < R] or [20])
    ap_now = min(int(me["actionPoints"]) if my_turn else 100, 100 - stun_amt if stunned else 100)
    spent, pierce_last, avg = enemy_resources(rows, en["userId"], R)
    known = en["username"].lower() in shotplan.ENEMY
    ekit = shotplan.ENEMY.get(en["username"].lower()) or generic_enemy(avg)

    def tags(side, r):
        # a list, not a set: two identical tags (Chakra Overflow's double +35%) both count and both show
        return sorted(f"{t[0]}{'' if t[0] in ('stun',) else f' {t[1]:g}'} (to R{t[3]})" for t in side.tags
                      if t[2] <= r <= t[3])

    ctx = {
        "pierce_ready": pierce_last is None or R - pierce_last >= 3,
        "clear_held": "clear" not in spent,
        "me_immune_now": bool(me0.live("debuffimmune", R)),
        "me_debuffed": any(t[2] <= R + 1 and t[3] >= R and (t[0] in ("taken", "wound", "drain", "recoil_self")
                           or (t[0] == "given" and t[1] < 0)) for t in me0.tags),
        "en_buffed": any(t[3] >= R and shotplan.positive(t) for t in en0.tags),
        "my_next_burst": True,
        "my_hp": me["curHealth"],
        "d0": d0,
        "line_blocked": barrier_between(me_pos, en_pos) is not None,
        "my_max": me.get("maxHealth", 5050),
        "afk": (lambda t: len(t) >= 1 and sum(1 for a in t if a == "wait") * 2 >= len(t))(
            [a for r, u, a, _ in rows if u == en["userId"] and (a == "wait" or a not in ("move",))]
            and [a for r, u, a, _ in rows if u == en["userId"]]),
        # director 2026-11-11: pierce is best when his DR is at or near max (engine DMG_REDUCTION_CAP = 90%), not
        # into 30-45%. Window = his effective in-combat DR >= 55%, a live shield, me smoked, or a pierce kill.
        # his gear DR adds to the 50% system DR (engine pre-battle stage): effective DR vs a bare target =
        # 1 - (50 - gearDR)/50 * prod(1 - tag DR). Director's R4 Stormblade vs TearsOfAngel: gear 17 + tag 35 -> 57%.
        "pierce_window": bool(me0.mult("given", R) < 0.6 or en0.live("shield", R)
                              or 1 - (50 - _his_gear_dr) / 50 * _prod(1 - t[1] for t in en0.live("dr", R)) >= 0.55
                              or en["curHealth"] <= 720),
        "en_absorb": en0.total("absorb", R),
        "tick": me0.total("wound", R) + me0.total("drain", R),
    }

    print(f"R{R} v{battle['battle.version']} | {'MY TURN' if my_turn else 'his turn'} | "
          f"{'he acted first this round' if en_acted else 'I act first this round'}"
          f" | seat: player {2 if en_acted else 1}")
    print(f"me {ME_NAME} {me['curHealth']:.0f} HP @ {me_pos}  AP {ap_now}{f' (STUNNED -{stun_amt})' if stunned else ''}")
    print(f"him {en['username']} {en['curHealth']:.0f} HP @ {en_pos}  dist {d0}  avg dmg/turn {avg:.0f}")
    print(f"my tags now: {', '.join(tags(me0, R)) or '-'} | next: {', '.join(tags(me0, R + 1)) or '-'}")
    print(f"his tags now: {', '.join(tags(en0, R)) or '-'} | next: {', '.join(tags(en0, R + 1)) or '-'}")
    print(f"enemy {'AFK (timing out)' if ctx['afk'] else 'active'}; his spent: {spent or '-'}; pierce {'READY' if ctx['pierce_ready'] else f'used R{pierce_last}'}; "
          f"Clear {'HELD' if ctx['clear_held'] else 'spent'}")
    print("value model: calibrated kit + weighted enemy options + 1-round lookahead (value_model.py)")
    waiting = sorted((cd_plan.ready_round(st, n), n) for n in st["loadout"] if n in cd_plan.ACTIONS
                     and cd_plan.ready_round(st, n) > R)
    print("on cooldown: " + ", ".join(f"{n}->R{r}" for r, n in waiting))
    if not my_turn:
        print("not my turn: poll again in <=15 s")
        return

    bundles = legal(st, R, ap_now, bool(en0.live("debuffimmune", R)),
                    set(), st["loadout"], d0)
    # engine replay (harness/pvp_turn/engine/replay_sim.ts): legality, AP and costs from the engine's own state
    # --fast (live-turn mode): the engine's legality list runs in a thread while python scores stage 1, and is
    # applied to the stage-1 list afterwards; the slower engine re-score of the shortlist is skipped
    eng_box = {}
    def _eng_list():
        eng_box["eng"] = engine_bridge.replay_list(rows, ME, en["userId"], me, en, me_pos, en_pos, R,
                                                   "next" if en_acted else "same", value_model.load_cal())
    eng_thread = None
    if a.no_engine:
        eng = None
    elif a.fast:
        eng_thread = threading.Thread(target=_eng_list, daemon=True)
        eng_thread.start()
        eng = None
    else:
        _eng_list()
        eng = eng_box["eng"]

    def make_eng_ok(eng):
        cost_by_id = {x["id"]: x["cost"] for x in eng["available"]}
        ap_eng = eng["ap"]
        def eng_ok(bb):
            tot = 0
            for x in bb:
                aid = ACTION_ID.get(x, x)
                if aid == "move":
                    tot += 10
                    continue
                if aid not in cost_by_id:
                    return False
                tot += cost_by_id[aid]
            return tot <= ap_eng
        return eng_ok, ap_eng
    if eng:
        cost_by_id = {x["id"]: x["cost"] for x in eng["available"]}
        ap_eng = eng["ap"]
        def eng_ok(bb):
            tot = 0
            for x in bb:
                aid = ACTION_ID.get(x, x)
                if aid == "move":
                    tot += 10
                    continue
                if aid not in cost_by_id:
                    return False
                tot += cost_by_id[aid]
            return tot <= ap_eng
        bundles = [bb for bb in bundles if eng_ok(bb)]
        ap_now = ap_eng
        print(f"engine replay: AP {ap_eng}, {len(eng['available'])} actions available"
              + (f", replay issues {len(eng['replayIssues'])}" if eng.get("replayIssues") else ""))
    gm = (engine_bridge.opponent_kit(en["userId"]) or {}).get("gearMods")
    print("his gear: " + (f"MEASURED given +{gm['incDamageGivenFromGear']:g}, DR {gm['drTakenFromGear']:g} (fit_gear.py)" if gm
                          else "endgame assumption (run fit_gear.py on his turn once hits exist both ways)"))
    src = engine_bridge.his_kit_source(en["userId"])
    print("his kit: " + ("REAL (saved before the fight, opponent_kit.py)" if src == "real"
                         else "ESTIMATED: no pre-fight kit saved, unseen moves use the calibrated stand-in"))
    miss = engine_bridge.missing_records(rows, ME)
    if miss:
        print("CATALOG GAP (not in kit/catalog.json; refresh harvests after the fight, no mid-fight lookups):",
              ",".join(miss))
    if not bundles:
        print("no legal bundle (check AP/cooldowns)"); return
    # kite-back variants: one spare step moves me back out after ranged actions
    extra = []
    for b in bundles:
        cost = sum(cd_plan.ACTIONS[x][0] for x in b if x in cd_plan.ACTIONS)
        if "step" in b and ap_now - cost >= 10 and "basic" not in b:
            extra.append(tuple(b) + ("stepback",))
    cd_plan.ACTIONS.setdefault("stepback", (10, 0, None, "kite step"))
    shotplan.MINE.setdefault("stepback", (0, []))
    bundles = list(bundles) + extra
    cal = value_model.load_cal()
    value_model.calibrate_kit(cal)
    ctx["smoke_spent"] = "smoke" in spent
    ctx["en_given"] = en0.mult("given", R + 1 if en_acted else R)
    # live enemy summon (e.g. Korin's Jade): acts on its own cooldowns, so his pierce lock doesn't cover it
    sm = [(r, m.group(1), int(m.group(2))) for r, u, _, ts in rows if u == en["userId"] for t in (ts or [])
          if (m := re.search(r"^\s*(\S+) was summoned for (\d+) rounds", t))]
    ctx["summon"] = False
    if sm:
        r0, sname, n = sm[-1]
        names = {p["username"].strip(): p["curHealth"] for p in others}
        if sname in names:  # live summons appear in usersState; dead ones drop out (others keeps HP > 0 only)
            alive = names[sname] > 0
        else:  # snapshot without it: no death message exists, so use damage taken (Jade died at ~2650)
            took = sum(float(m.group(1)) for r, u, _, ts in rows if r >= r0 for t in (ts or [])
                       if (m := re.match(rf"\s*{re.escape(sname)} takes ([\d.]+) damage", t)))
            alive = took < 2000
        ctx["summon"] = alive and r0 + n - 1 >= R
    ctx["pierce_shown"] = pierce_last is not None  # he carries a pierce: shield-vs-pierce odds go up
    ctx["pierce_ready_own"] = ctx["pierce_ready"]
    if ctx["summon"]:
        ctx["pierce_ready"] = True
    # no blanket ban while he is debuff-immune: shotplan drops each hostile tag on an immune target and keeps the
    # damage, and buff-block (Seal / Lotus) still lands (live: director's R2 Seal vs immune TearsOfAngel, 2026-11-11)
    blocked = set()
    profile = known and en["username"].lower() in shotplan.PROFILES
    hr = R + 1 if en_acted else R          # his reply round
    hr2 = hr + 1                            # his reply after my follow-up
    maxhp_me, maxhp_en = me.get("maxHealth", 5050), en.get("maxHealth", 5050)

    # Opponent model (director 2026-11-11: "gauge their active state vs our own"). His threat = his BASE turn x the
    # multipliers live when he acts (his damage-given stack, my damage-taken debuffs, my reductions), which the
    # simulation applies. The base comes from HIS logged hits with the multipliers live at each hit divided out,
    # blended with the prior while samples are few, so a stacked opponent reads as a burst at its real size.
    obs = observed_turns(rows, en["userId"], en["username"], me0, en0)
    def kit_for(dend):
        reach = max(0.4, 1 - 0.1 * max(0, dend - 4))  # each hex beyond 4 costs him 10 AP of his turn
        k = value_model.generic_kit(cal, reach)
        if obs:
            n, prior_t, prior_b = len(obs), k["turn"][0], k["burst"][0]
            med = sorted(obs)[n // 2] * reach
            k["turn"] = ((n * med + prior_t) / (n + 1), [])
            k["burst"] = ((n * max(max(obs) * reach, med * 1.6) + prior_b) / (n + 1), [])
        if known:
            k.update(ekit)
        return k

    # Clear vs his NEXT stack (DDX R3, 2026-11-11): my Clear has a 10-round cooldown, so it is one shot per fight.
    # Spent on his small R3 stack (+65% given), it was gone when he cast +115% in R4 and hit 1854 in R5. Holding it
    # is worth what Clearing his biggest reachable stack would save: his base turn x the +given he can cast in one
    # turn (his kit's buffs ready in the next 3 rounds) x how often he has stacked so far. That replaces the flat
    # Clear reserve when larger, and only for a Clear spent now.
    clear_wait, clear_wait_note = 0.0, ""
    if cd_plan.ready_round(st, "clear") <= R and not ctx["afk"]:
        try:
            import clock
            hacts = clock.his_actions(en["userId"], rows)
        except Exception:  # noqa: BLE001
            hacts = None
        if hacts:
            def _buffs(bb):
                return sum(t[2] for x in bb for t in hacts[x][4][1] if t[0] == "en" and t[1] == "given" and t[2] > 0)
            peak = max((_buffs(bb) for rr in (hr, hr + 1, hr + 2)
                        for bb in clock.bundles(hacts, clock.ready_at(hacts, en["userId"], rows, rr))), default=0.0)
            cur = sum(t[1] for t in en0.tags if t[0] == "given" and t[1] > 0 and t[2] <= hr <= t[3])
            his_rounds = sorted({r for r, u, _, _ in rows if u == en["userId"]})
            stacked = sum(1 for rr in his_rounds if _buffs([a for r, u, a, _ in rows
                                                            if u == en["userId"] and r == rr and a in hacts]) >= 0.3)
            p_build = 0.8 * (stacked + 1) / (len(his_rounds) + 2)
            if peak > cur:
                flat = value_model.reserve_cost(("clear",), cal, R)[0]
                wait = p_build * kit_for(d0)["turn"][0] * peak
                clear_wait = max(0.0, wait - flat)
                clear_wait_note = (f"Clear wait: his stack now +{cur:.0%}, he can cast +{peak:.0%} in one turn "
                                   f"(p {p_build:.2f}) -> hold value {wait:.0f} vs flat {flat:.0f}")
    if clear_wait_note:
        print(clear_wait_note)

    # kunai cost real ryo: price the throw by how close the fight is (value_model.kunai_cost). My turn = what I have
    # taken off him per round so far, blended with a 1100 prior; his turn = his modelled base turn at this distance.
    done = max(0.0, maxhp_en - en0.hp)
    my_turn = (done + 1100 * 2) / (max(0, R - 1) + 2)
    # his turn: the larger of his modelled base turn and what he has actually averaged (Arashii R6 averaged 1807 with
    # me on 704: a race, not the "sure win" the 544 base turn read)
    value_model.KUNAI_COST, kwhy = value_model.kunai_cost(me0.hp, en0.hp, my_turn,
                                                          max(kit_for(d0)["turn"][0], avg or 0), ctx["afk"])
    print(f"kunai: {kwhy} -> cost {value_model.KUNAI_COST}")

    def my_reserve(b, rnd):
        rc, why = value_model.reserve_cost(b, cal, rnd)
        if rnd == R and clear_wait and "clear" in b:
            rc += clear_wait
            why = why + [f"Clear wait -{clear_wait:.0f}"]
        return rc, why

    def his_options(m, r, b=()):
        c = ctx
        if ctx["summon"] and any(x in AOE for x in b):  # AoE clears summons (Fury one-shot Jade for 2646, 2026-11-11)
            c = dict(ctx, summon=False, pierce_ready=ctx["pierce_ready_own"])
        # Seal of Nullification / Lotus cast now block his buffs in his next-round turn (director's R2 Seal vs
        # TearsOfAngel: his R3 self-buff "cannot be buffed"); his burst and setup lean on those buffs
        if r > R and any(x in ("sealnull", "lotus") for x in b):
            c = dict(c, en_buffblocked=True)
        opts = value_model.enemy_options(cal, c, m, r, ctx["afk"])
        if profile:
            pred = shotplan.enemy_options(en["username"].lower(), a.battle, r)
            opts = [(w * 0.5, o) for w, o in opts] + [(0.5 / len(pred), o) for o in pred]
        return opts

    def ply1(b, h, kit):
        m, e = value_model.copy_side(me0), value_model.copy_side(en0)
        if "cleanse" in b:  # Cleanse fired first removes wound/drain before they tick (ground effects stay)
            m.tags = [x for x in m.tags if shotplan.positive(x) or shotplan.ground(x)]
        # moving off his ground ends its -damage given: before my hits when the move fires first (gap close), after
        # them when it fires last (disengage), and only if the landing tile is off his floor
        mv = any(x in GROUND_EXIT for x in b)
        last = mv and moves_last(b, d0)
        off = mv and (not HOSTILE or resolve_targets(b, me_pos, en_pos, occupied)[1] not in HOSTILE)
        if off and not last:
            m.tags = [x for x in m.tags if not shotplan.ground(x)]
        bar = kit.get("_barrier")
        shotplan.MY_BARRIER = list(bar) if bar else None
        try:
            d, t = shotplan.run_turn(m, e, list(b), shotplan.MINE, R, True)
        finally:
            shotplan.MY_BARRIER = None
        if off and last:
            m.tags = [x for x in m.tags if not shotplan.ground(x)]
        m.hp = min(m.hp, maxhp_me)
        log = [("me", R, b, d, t, m.hp, e.hp)]
        p_kill = 1.0
        if e.hp <= 0 < m.hp:
            dealt = en0.hp - e.hp
            p_kill = kill_chance(dealt, en0.hp, KILL_MARGIN)
            if p_kill < 1.0:          # a close kill: he may live on what the forecast overshoots by
                sc_kill = value_model.score(m, e, me["curHealth"], en["curHealth"])
                e.hp = max(1.0, en0.hp - dealt * (1 - KILL_MARGIN))
                log[0] = ("me", R, b, d, t, m.hp, e.hp)
        m._his = tuple(h)
        if e.hp > 0:
            d2, t2 = shotplan.run_turn(e, m, h, kit, hr, False)
            m.hp = min(m.hp, maxhp_me); e.hp = min(e.hp, maxhp_en)
            log.append(("him", hr, h, d2, t2, m.hp, e.hp))
        if e.hp <= 0 < m.hp and len(log) > 1:
            # he died on his own turn (my reflect / recoil): too unsure for the kill bonus, so he is kept alive on
            # 1 HP and the lookahead plays on. Scoring it as a dead end left such a line BELOW the lines where he
            # lives and gets finished next turn (Korin R10 replay, 2026-11-11: Nights + Basic Heal dropped to #25)
            e.hp = 1.0
            log[-1] = log[-1][:6] + (e.hp,)
        sc = value_model.score(m, e, me["curHealth"], en["curHealth"])
        if p_kill < 1.0:
            sc = p_kill * sc_kill + (1 - p_kill) * sc
            e.p_kill = p_kill        # the lookahead and setup credit only count for the share where he lives
        return m, e, sc, log

    def ply2(m, e, b, dend, kit):
        """My best follow-up next round (after cooldowns from b) and his expected reply to it."""
        if m.hp <= 0 or e.hp <= 0:
            return 0.0, None
        st2 = {"loadout": st["loadout"], "used": st["used"] + [[R, x] for x in b if x not in ("step", "stepback")]}
        best = (-1e9, None)
        # his Clear, still held after his ply-1 reply, can land in his hr2 reply before my payoff round: the setup
        # and guard credits only count for the share where it does not (the ply-2 reply itself is his plain turn)
        p_clr = 0.0
        if ctx["clear_held"] and not ctx["afk"] and "clear" not in getattr(m, "_his", ()):
            p_clr = sum(w for w, o in value_model.enemy_options(cal, ctx, m, hr2, False) if "clear" in o)
        r1 = R + 1
        # Speed pass (director 2026-11-11: 10 s per turn): same arithmetic as simulating every follow-up from
        # scratch, two shortcuts. (1) Within round R+1 my actions do not see each other unless one changes R+1
        # state (Clear/Cleanse, a shield broken, an instant tag the damage step reads), because new tags only turn
        # on from R+2: each action is applied ONCE to the start state and bundles are summed. Bundles holding an
        # interacting action take the full sequential path. (2) His reply depends only on the tags live in his
        # round (+ the summon flag) and on the multipliers the burst term reads, so it is cached on exactly those.
        acts = {}
        for x in st["loadout"] + ["step", "stepback"]:
            spec = shotplan.MINE.get(x)
            if spec is None:
                acts[x] = (0.0, 0.0, [], [], False)
                continue
            m1, e1 = value_model.copy_side(m), value_model.copy_side(e)
            d, s = shotplan.apply(m1, e1, spec, r1, True)
            nm, ne = len(m.tags), len(e.tags)
            # an instant tag interacts only if a later action of mine reads it: on me (the actor) the damage step
            # reads given/lifesteal/healcut/recoil and the buff-block guard; on him, taken/dr/shield/absorb/healcut/
            # reflect/parry and the debuff/clear guards
            inter = (x in ("clear", "cleanse") or m1.tags[:nm] != m.tags or e1.tags[:ne] != e.tags
                     or any(t[2] <= r1 and t[0] in _READ_SRC for t in m1.tags[nm:])
                     or any(t[2] <= r1 and t[0] in _READ_DST for t in e1.tags[ne:]))
            acts[x] = (d, s, m1.tags[nm:], e1.tags[ne:], inter)
        tick = m.total("wound", r1) + m.total("drain", r1)
        on_ground = any(shotplan.ground(t) for t in m.tags)
        reply_cache = {}
        tagless = all(not (kit.get(x) or (0, []))[1] and len(kit.get(x) or (0, [])) == 2 for x in ("turn", "summon"))
        if tagless:
            # Arithmetic fast path, exact: for a follow-up with no interacting action, my turn is the sum of each
            # action's effect on the start state; his pure-damage reply depends only on WHICH tagging actions the
            # follow-up holds (each adds fixed tags), so it is cached on that set; the burst term only reads
            # tags that started by R+1, which no non-interacting follow-up adds, so it is one number per call.
            base_g = _off_val(m, e, R, R + 2, value_model.BURST_BASE, p_clear=p_clr)
            base_d = _guard_val(m, e, R, hr2 + 1, me0, kit["turn"][0], p_clr)
            tagging = {x: bool(v[2] or v[3]) for x, v in acts.items()}
            aoe_b = any(x in AOE for x in b)
            summon_on = bool(ctx.get("summon"))
            rk = _RESERVE_CACHE.setdefault((r1, id(cal)), {})
            base_m = {k: list(v) for k, v in shotplan._agg(m, hr2).items()}
            base_e = {k: list(v) for k, v in shotplan._agg(e, hr2).items()}
            base_v = _vec(base_e, base_m)
            cvec = {}
            for x, v in acts.items():
                cm, ce = _contrib(v[2], hr2), _contrib(v[3], hr2)
                cvec[x] = _vec(ce, cm) if (cm or ce) else None
            reply_bases = {False: [kit["turn"][0]], True: [kit["turn"][0], (kit.get("summon") or (0, []))[0]]}
        for b2 in legal(st2, r1, 100, bool(e.live("debuffimmune", r1)), blocked, st["loadout"], dend):
            if tagless and not any(x not in acts or acts[x][4] for x in b2):
                dealt, taken = 0.0, tick if b2 else 0.0
                for x in b2:
                    av = acts[x]
                    dealt += av[0]
                    taken += av[1]
                mh = min(m.hp - taken, maxhp_me)
                eh = e.hp - dealt
                pk = kill_chance(dealt, e.hp, KILL_MARGIN) if eh <= 0 else 0.0
                if eh > 0:
                    alive = summon_on and not aoe_b and not any(x in AOE for x in b2)
                    tk = (alive,) + tuple(x for x in b2 if tagging[x])
                    hit = reply_cache.get(tk)
                    if hit is None:
                        vv = list(base_v)
                        for x in b2:
                            cv = cvec[x]
                            if cv is not None:
                                for i in range(12):
                                    if i in _MULT_IDX:
                                        vv[i] *= cv[i]
                                    else:
                                        vv[i] += cv[i]
                        hit = reply_cache[tk] = _reply_vec(vv, reply_bases[alive])
                    mh -= hit[0]
                    eh -= hit[1]
                rc = rk.get(b2)
                if rc is None:
                    rc = rk[b2] = value_model.reserve_cost(b2, cal, r1)[0]
                v = (e.hp - eh) - (m.hp - mh) - rc
                if pk:                  # only my own hits count as a kill, with the margin (no reflect / recoil deaths)
                    v += pk * value_model.KILL
                if mh <= 0:
                    v -= value_model.DEATH
                if eh > 0 and mh > 0:
                    v += base_g + base_d
                if v > best[0]:
                    best = (v, b2)
                continue
            if any(x not in acts or acts[x][4] for x in b2) or (on_ground and any(x in GROUND_EXIT for x in b2)):
                m2, e2 = value_model.copy_side(m), value_model.copy_side(e)
                if "cleanse" in b2:
                    m2.tags = [x for x in m2.tags if shotplan.positive(x) or shotplan.ground(x)]
                if any(x in GROUND_EXIT for x in b2):
                    m2.tags = [x for x in m2.tags if not shotplan.ground(x)]
                shotplan.run_turn(m2, e2, list(b2), shotplan.MINE, r1, True)
            else:
                m2, e2 = shotplan.Side(m.hp), shotplan.Side(e.hp)
                m2.tags, e2.tags = list(m.tags), list(e.tags)
                dealt, taken = 0.0, tick if b2 else 0.0
                for x in b2:
                    d, s, tm, te, _ = acts[x]
                    dealt += d
                    taken += s
                    m2.tags += tm
                    e2.tags += te
                e2.hp -= dealt
                m2.hp -= taken
            m2.hp = min(m2.hp, maxhp_me)
            eh_mine = e2.hp
            gtags = None
            if e2.hp > 0:
                alive = bool(ctx.get("summon") and not any(x in AOE for x in tuple(b) + tuple(b2)))
                if tagless:
                    # his modelled turn is pure damage: it only reads the tags its damage step reads, and only
                    # removes my shield, so the burst term is taken before it and the cache key is minimal
                    gtags = _off_val(m2, e2, R, R + 2, value_model.BURST_BASE, p_clear=p_clr)
                    key = (alive, tuple(sorted(tuple(t) for t in m2.tags if t[0] in _REPLY_READ and t[2] <= hr2 <= t[3])),
                           tuple(sorted(tuple(t) for t in e2.tags if t[0] in _REPLY_READ and t[2] <= hr2 <= t[3])))
                else:
                    key = (alive, tuple(sorted(tuple(t) for t in m2.tags if t[2] <= hr2 <= t[3] or (t[0] == "given" and t[2] <= r1 <= R + 2 <= t[3]))),
                           tuple(sorted(tuple(t) for t in e2.tags if t[2] <= hr2 <= t[3] or (t[0] == "taken" and t[2] <= r1 <= R + 2 <= t[3]))))
                hit = reply_cache.get(key)
                if hit is None:
                    pm, pe = m2.hp, e2.hp
                    shotplan.run_turn(e2, m2, ["turn"] + (["summon"] if alive else []), kit, hr2, False)
                    if not tagless:
                        gtags = _off_val(m2, e2, R, R + 2, value_model.BURST_BASE, p_clear=p_clr)
                    reply_cache[key] = (pm - m2.hp, pe - e2.hp, gtags)
                else:
                    m2.hp -= hit[0]
                    e2.hp -= hit[1]
                    if not tagless:
                        gtags = hit[2]
            v = value_model.score(m2, e2, m.hp, e.hp) - value_model.reserve_cost(b2, cal, r1)[0]
            if e2.hp <= 0:              # only my own hits count as a kill, with the margin (no reflect / recoil deaths)
                v -= value_model.KILL * (1.0 if eh_mine > 0 else 1 - kill_chance(e.hp - eh_mine, e.hp, KILL_MARGIN))
            # buffs/debuffs still live in R+2 pay off again on my next burst (director's smoke -> setup -> burst
            # line, Zaruza/Hikuro 2026-11-11); the 1-round lookahead alone undervalued 2-round setups
            if e2.hp > 0 and m2.hp > 0:
                # only multipliers cast THIS turn (live from R+1) count; ply2's own setup must not chain
                # setup credit after his cuts/absorb at my next attack, and my new cuts against his NEXT unplayed
                # turn (hr2 + 1; hr2 itself was just simulated with them in place) at his typical size
                v += gtags if gtags is not None else _off_val(m2, e2, R, R + 2, value_model.BURST_BASE, p_clear=p_clr)
                v += _guard_val(m2, e2, R, hr2 + 1, me0, kit["turn"][0], p_clr)
            if v > best[0]:
                best = (v, b2)
        return best

    # stage 1: one ply for every bundle (expected + worst over his option set); stage 2: lookahead on the best 25
    stage = []

    def setup_est(m, e, kit):
        """Stage-1 setup estimate so 2-round setups survive pruning (they score ~0 on one ply): my multipliers live
        at my next attack after his cuts/absorb there, and my new cuts against his next unplayed turn (hr + 1)."""
        return (_off_val(m, e, R, R + 1, value_model.BURST_BASE, me0, en0)
                + _guard_val(m, e, R, hr + 1, me0, kit["turn"][0]))
    for b in bundles:
        seq, end = resolve_targets(b, me_pos, en_pos, occupied)
        dend = dist(end, en_pos)
        kit = kit_for(dend)
        kit["_barrier"] = barrier_between(end, en_pos) if BARRIERS else None
        pen, why = penalties(b, ctx, cal)
        rc, rwhy = my_reserve(b, R)
        kc = value_model.KUNAI_COST if "kunai" in b else 0
        outs = []
        # his options are judged on MY STACK AFTER this bundle (Clear risk grows with what I just stacked; it used
        # to read the pre-bundle stack, so Overflow+Thunders into a held Clear looked safe)
        m_after, e_after = value_model.copy_side(me0), value_model.copy_side(en0)
        shotplan.run_turn(m_after, e_after, list(b), shotplan.MINE, R, True)
        for w, h in his_options(m_after, hr, b):
            m, e, sc, log = ply1(b, h, kit)
            kill = e.hp <= 0
            # the kunai's ryo is paid even on a kill (unlike cooldown reserves): a kill line without it wins
            outs.append((w, sc + (-kc if kill else pen - rc), m, e, log, kill))
        # stage-1 setup estimate so 2-round setups survive pruning (they score ~0 on one ply): what my multipliers
        # live next round add to a typical burst, discounted like the lookahead
        outs = [(w, v + (0 if kill else (1 - getattr(e, "p_kill", 0.0)) * setup_est(m, e, kit)), m, e, log, kill)
                for w, v, m, e, log, kill in outs]
        ev = sum(w * v for w, v, *_ in outs)
        worst = min(outs, key=lambda o: o[1])
        stage.append(((1 - value_model.RISK) * ev + value_model.RISK * worst[1], b, outs, worst, dend, kit,
                      [] if worst[5] else why + rwhy))
    stage.sort(key=lambda x: -x[0])
    if eng_thread is not None:
        eng_thread.join(10)
        eng = eng_box.get("eng")
        if eng:
            ok, ap_eng = make_eng_ok(eng)
            stage = [x for x in stage if ok(x[1])]
            print(f"engine replay (parallel): AP {ap_eng}, {len(eng['available'])} actions available")
            if not stage:
                print("no legal bundle (engine)"); return
        else:
            print("engine replay unavailable: python legality only")
    if os.environ.get("TNR_STAGE_DEBUG"):
        keys = os.environ["TNR_STAGE_DEBUG"].split(",")
        for i, (s1, b, outs, worst, *_r) in enumerate(stage):
            if i < 3 or any(k in b for k in keys):
                print(f"stage1 #{i + 1} {s1:+.0f} {'+'.join(b)} | " + " ".join(
                    f"{w:.2f}:{v:+.0f}" for w, v, *_x in outs))
    # cash-in guarantee (director 2026-11-11, Targaryen R3): with a big stack live, setup_est makes "one more buff"
    # outscore paying the stack out, and the payoff attacks were pruned before the lookahead ever saw them. The 6
    # bundles with the most immediate expected damage to him always reach stage 2.
    def _dealt(o):
        return sum(w * (en["curHealth"] - e.hp) for w, v, m, e, log, kill in o)
    nk, nc = (a.keep, a.cash) if a.keep else ((10, 4) if a.fast else (25, 6))
    keep = stage[:nk]
    for extra in sorted(stage[nk:], key=lambda x: -_dealt(x[2]))[:nc]:
        keep.append(extra)
    def stage2_vals(item):
        s1, b, outs, worst, dend, kit, why = item
        vals = []
        for w, v, m, e, log, kill in outs:
            live = 1 - getattr(e, "p_kill", 0.0)
            if not kill:
                v -= live * setup_est(m, e, kit)
            f, b2 = ply2(m, e, b, dend, kit)
            vals.append((w, v + live * value_model.GAMMA * f, b2))
        return vals
    # the lookahead is ~90% of the planner's time: split across CPU cores by fork (same result, order kept)
    all_vals = par_map(stage2_vals, keep)
    results = []
    for (s1, b, outs, worst, dend, kit, why), vals in zip(keep, all_vals):
        ev = sum(w * v for w, v, _ in vals)
        wv = min(vals, key=lambda x: x[1])
        total = (1 - value_model.RISK) * ev + value_model.RISK * wv[1]
        follow = max(vals, key=lambda x: x[0])[2]
        log = list(worst[4]) + ([("me", R + 1, follow, 0, 0, 0, 0)] if follow else [])
        results.append((total, b, log, why, vals, outs))
        if os.environ.get("TNR_STAGE_DEBUG") and any(k in b for k in os.environ["TNR_STAGE_DEBUG"].split(",")):
            print(f"stage2 {total:+.0f} {'+'.join(b)} | " + " ".join(
                f"{w:.2f}:{v:+.0f}({'+'.join(b2 or ())})" for w, v, b2 in vals))
    results.sort(key=lambda x: -x[0])
    # desperation (director 2026-11-11, ANBU Member R5: Cleanse at 419 HP when every line died anyway): if even the
    # best line scores as my death, rank by expected damage to him; the best chance is the kill or near-kill
    if results and results[0][0] < -value_model.DEATH * 0.6:
        def _dmg(r):
            return sum(w * (en["curHealth"] - e.hp) for w, v, m, e, log, kill in r[5])
        results.sort(key=lambda r: -_dmg(r))
        print("DESPERATION: every line loses; ranked by damage to him")
    # exact re-score of the best 6 by engine replay: my bundle, then his typical and best reply from his real kit
    engine_note = "engine: legality only (--fast)" if a.fast and eng else "engine: off"
    near = en["curHealth"] <= NEAR_KILL_HP
    if not a.no_engine and (not a.fast or near) and eng:
        top = results[:6]
        if near:
            # near a kill the engine judges the bundles that hit hardest too, even if python ranked them low
            for r_ in sorted(results[6:], key=lambda r_: -sum(w * (en["curHealth"] - e.hp) for w, v, m, e, l, k in r_[5]))[:4]:
                top.append(r_)
        # one-shot answers (Cleanse / Smoke / Clear) are judged by the engine even if the python shortlist pruned them
        for key in ("cleanse", "smoke", "clear"):
            if any(key in r[1] for r in top):
                continue
            extra = next((r for r in results[6:] if key in r[1]), None)
            if extra is None:  # not in the lookahead set: take the best stage-1 bundle with it (no lookahead term)
                st1 = next((x for x in stage if key in x[1]), None)
                if st1:
                    extra = (st1[0], st1[1], [], st1[6], [], [])
            if extra:
                top.append(extra)
        seqs = [resolve_targets(bb, me_pos, en_pos, occupied)[0] for _, bb, *_ in top]
        # the engine stops at 0 HP, so near a kill he gets extra HP for the check and the overkill is read back:
        # a kill counts as sure only with ENGINE_MARGIN to spare (Korin R11: engine 1188 = exactly his HP, real 1146)
        bump = max(0.0, min(3000.0, float(en.get("maxHealth", 5050)) - en["curHealth"])) if near else 0.0
        en_q = dict(en, curHealth=en["curHealth"] + bump)
        res = engine_bridge.replay_eval(rows, ME, en["userId"], me, en_q, me_pos, en_pos, R,
                                        "next" if en_acted else "same", cal,
                                        [[(n, aid, t) for n, aid, t in sq] for sq in seqs])
        if res and res.get("results") and bump:
            for er in res["results"]:
                for nm in ("afterMe", "typical", "best"):
                    if er.get(nm) and "him" in er[nm]:
                        er[nm]["him"] -= bump
                am = er.get("afterMe")
                if am:
                    er["p_kill"] = kill_chance(en["curHealth"] - am["him"], en["curHealth"], ENGINE_MARGIN)
        if res and res.get("results"):
            engine_note = "engine: replay (every logged action replayed on the TNR engine)" + (
                f"; near-kill check, margin {ENGINE_MARGIN:.0%}" if near else "")
            rescored = []
            for (total, bb, log, why, vals, outs), er in zip(top, res["results"]):
                if not er.get("legal"):
                    rescored.append((-1e9, bb, log, [f"engine: illegal ({er.get('reason')})"], vals, outs))
                    continue
                pen, pwhy = penalties(bb, ctx, cal)
                rc, rwhy = my_reserve(bb, R)
                f = sum(w * (v - v1) for (w, v, _), (_, v1, *_r) in zip(vals, outs))  # python lookahead part
                def sc_of(x):
                    em, ee = shotplan.Side(x["me"]), shotplan.Side(x["him"])
                    # he died on his own reply (reflect / recoil): the HP counts, the kill bonus does not
                    return value_model.score(em, ee, me["curHealth"], en["curHealth"]) - (value_model.KILL if x["him"] <= 0 else 0)
                pk = er.get("p_kill", 1.0 if er["afterMe"]["him"] <= 0 else 0.0)
                t_kill = value_model.score(shotplan.Side(er["afterMe"]["me"]), shotplan.Side(0), me["curHealth"], en["curHealth"])
                if pk >= 1.0:
                    t2 = t_kill - (value_model.KUNAI_COST if "kunai" in bb else 0)
                else:
                    # he lives (or may): his reply as the engine played it, from what the margin leaves him
                    left = max(1.0, en["curHealth"] - (en["curHealth"] - er["afterMe"]["him"]) * (1 - ENGINE_MARGIN)) \
                        if pk > 0 else None
                    typ = er.get("typical") or {"me": er["afterMe"]["me"], "him": er["afterMe"]["him"]}
                    best = er.get("best") or typ
                    if left is not None:      # a kill line in the check: his reply from the HP the margin leaves
                        typ = dict(typ, him=max(1.0, left - (er["afterMe"]["him"] - typ["him"])))
                        best = dict(best, him=max(1.0, left - (er["afterMe"]["him"] - best["him"])))
                    t2 = (1 - value_model.RISK) * sc_of(typ) + value_model.RISK * sc_of(best) + pen - rc + value_model.GAMMA * f
                    if pk > 0:
                        t2 = pk * (t_kill - (value_model.KUNAI_COST if "kunai" in bb else 0)) + (1 - pk) * t2
                eng_log = [("me", R, bb, 0, 0, er["afterMe"]["me"], er["afterMe"]["him"])]
                for nm in ("typical", "best"):
                    if er.get(nm):
                        eng_log.append(("him", hr, [nm] + [x[:6] for x in er[nm]["actions"]], 0, 0, er[nm]["me"], er[nm]["him"]))
                rescored.append((t2, bb, eng_log + [l for l in log if l[0] == "me" and l[1] == R + 1], why, vals, outs))
            # engine-scored candidates rank ahead of python-only ones (different, less exact scale)
            results = sorted(rescored, key=lambda x: -x[0]) + [r for r in results if r not in top]
        else:
            engine_note = "engine: eval unavailable, python sim used"
    print(engine_note)
    print(f"{len(bundles)} legal bundles. TOP {a.top}:")
    for i, (sc, b, log, why, *_r) in enumerate(results[:a.top], 1):
        seq, end = resolve_targets(b, me_pos, en_pos, occupied)
        fire = " -> ".join(f"{x}@{t[0]},{t[1]}" for x, _, t in seq)
        fc = " | ".join(f"{w} R{r} {'+'.join(x)}: me {mh:.0f} / him {eh:.0f}" if w == "him" or r == R else
                        f"then me R{r} {'+'.join(x)}" for w, r, x, _, _, mh, eh in log)
        print(f"{i}. {sc:+6.0f}  {fire}  (ends @{end}, dist {dist(end, en_pos)})")
        print(f"     forecast: {fc}" + (f"  [penalty: {'; '.join(why)}]" if why else ""))
    best = results[0][1]
    seq, _ = resolve_targets(best, me_pos, en_pos, occupied)
    policy.legal_save()
    print("FIRE:", json.dumps([{"actionId": aid, "longitude": t[0], "latitude": t[1], "name": n} for n, aid, t in seq]))


_equipped_thrown()

if __name__ == "__main__":
    main()
