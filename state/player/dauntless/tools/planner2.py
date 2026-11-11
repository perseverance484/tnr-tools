#!/usr/bin/env python3
"""Planner 2: a small numeric battle engine plus a tuned, feature-based score (director 2026-11-11: "the entire
planner and legality mode could be simplified and optimized ... a better format for processing information and
tuning models for decision making based on projected numeric inputs and outputs").

Same input file and FIRE line as turn.py, so the pilot can switch by path.

1. State. Each side is HP plus one flat list of numbers: for each effect kind (damage given up/down, damage taken,
   damage reduction, absorb, lifesteal, reflect, parry, shield, debuff/clear immunity, wound, drain, recoil, heal
   cut, buff block, stun, and a count of positive tags) its value at each of the next H rounds. Multipliers are
   stored as products, the rest as sums, so "what is live on round r" is one index.
2. Actions. Each kit entry (shotplan.MINE, calibrated) is compiled once into (base, pierce, [tag changes]).
   A turn applies them in order with the engine order and caps from shotplan.apply (parry before shield, reflect
   / absorb / lifesteal capped at 60%, pierce flat and shield-breaking, Clear/Cleanse instant, tags live from next
   round unless instant). tests: planner2 parity vs shotplan on every exam state.
3. Legality. Ready actions (own cooldowns + shared locks from cd_plan), range after moves, no two actions sharing a
   lock tag, cost <= AP; up to 20 AP may stay unspent (priced by the score). Clear needs a clearable positive on
   him, Cleanse a negative on me.
4. Opponent. His reply is a weighted option set read from the live state of both sides (his pierce / Clear / Smoke
   resources, my buff stack for Clear odds, his damage-given stack for burst odds, my buff block on him), each
   option played through the same engine with his observed base turn (logged hits with the live multipliers
   divided out).
5. Score of a line = W . features of the position after his reply (HP swing, my next-turn damage potential, his
   next-turn damage potential, the kill-race tempo, reserves spent, AP unspent) + kill/death terminals + hard
   guards for the coached blunders. W is tuned on the director's own turns (exam.py --planner planner2 --tune).

Usage: planner2.py FILE --battle ID [--enemy NAME] [--loadout pvp1] [--top 3] [--dump FEATURES.json]
"""
import argparse
import json
import math
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cd_plan  # noqa: E402
import shotplan  # noqa: E402
import value_model  # noqa: E402
import turn  # noqa: E402  (input parsing, targets, history helpers)
import opp_profile  # noqa: E402
import clock  # noqa: E402

ME, ME_NAME = turn.ME, turn.ME_NAME
H = 5
(GUP, GDN, TAKEN, DR, ABS, LS, REF, PAR, SHD, DIMM, CIMM, NPOS, NSTK,
 WND, DRN, RCL, HCUT, BBLK, STUN, PABS, PLS, PREF, GGRD) = range(23)
NK = 23
# PABS/PLS/PREF: bloodline passives, in neither POSK nor NEGK, so Clear/Cleanse keep them.
# GGRD: a ground -damage given (Subaku Palace) on whoever stands on it: Cleanse does not remove it, moving off does,
# and it does not land while that side is debuff-immune (director 2026-11-11, 4qua R2).
MULT = (GUP, GDN, TAKEN, DR, GGRD)
COPY = -4
POSK = (GUP, DR, ABS, LS, REF, PAR, SHD, DIMM, CIMM, NPOS, NSTK)
NEGK = (GDN, TAKEN, WND, DRN, RCL, HCUT, BBLK, STUN)
HOSTILE = {TAKEN, WND, DRN, RCL, STUN, HCUT}
KIND = {"taken": TAKEN, "dr": DR, "absorb": ABS, "lifesteal": LS, "reflect": REF, "parry": PAR, "shield": SHD,
        "debuffimmune": DIMM, "clearimmune": CIMM, "wound": WND, "drain": DRN, "recoil_self": RCL, "recoil": RCL,
        "healcut": HCUT, "buffblock": BBLK, "stun": STUN}
CLEAR, CLEANSE, HEAL = -1, -2, -3
WFILE = os.path.join(HERE, "planner2_weights.json")
# Hand-set (director 2026-11-11: "orient it in the most ideal way possible by editing weights by hand"). Units: HP.
#   swing    HP dealt minus HP taken this exchange, the base currency
#   mypot    my best next-turn damage (cooldown-aware, through the multipliers live then): worth less than HP in hand
#            because he gets a turn first to Clear / Smoke / out-heal it
#   hispot   his best next-turn damage from HIS clock (his ready jutsu then, his live stack vs my live defence):
#            weighted above mypot, because damage taken is certain once his turn comes and a lost fight is final
#   mypot2 / hispot2  multipliers still live the round after: 2-round setup and 2-round defence pay a second time
#   race     tempo: turns he needs to kill me minus turns I need to kill him (HP per turn of tempo)
#   kill / die  chance my next turn kills him / his next turn kills me, in turn order (who acts first next round)
#   reserve  Clear / Cleanse / Smoke / pierce spent outside their window; waste: per 20 AP left unspent
# 2026-11-11 rebalance towards pressure: the first set (mypot 0.6, hispot 0.75, race 120, kill 1800, die 3600) went 0-6
# live, too passive against players who heal and stack; this set won 88% vs 65% on the six hardest log-modelled
# opponents and 94% vs 88% on all of them (fightsim, both turn orders; HikuroHatake as P2 still the weak spot)
DEFAULT_W = {"swing": 1.0, "mypot": 0.9, "hispot": 0.5, "mypot2": 0.3, "hispot2": 0.35, "race": 200.0,
             "kill": 2500.0, "die": 2500.0, "reserve": 1.0, "waste": 150.0}
NF = 8


# ------------------------------------------------------------------ state
class Side:
    __slots__ = ("hp", "a")

    def __init__(self, hp, a=None):
        self.hp = hp
        if a is None:
            a = [0.0] * (NK * H)
            for k in MULT:
                a[k * H:(k + 1) * H] = [1.0] * H
        self.a = a

    def copy(self):
        return Side(self.hp, self.a[:])

    def g(self, k, o):
        return self.a[k * H + o] if 0 <= o < H else (1.0 if k in MULT else 0.0)

    def add(self, k, v, o1, o2):
        a, base = self.a, k * H
        lo, hi = max(o1, 0), min(o2, H - 1)
        if k in MULT:
            f = (1 - v) if k == DR else (1 + v)
            for o in range(lo, hi + 1):
                a[base + o] *= f
        else:
            for o in range(lo, hi + 1):
                a[base + o] += v

    def shift(self):
        """Next round: offset 1 becomes offset 0."""
        a = self.a
        for k in range(NK):
            base = k * H
            a[base:base + H - 1] = a[base + 1:base + H]
            a[base + H - 1] = a[base + H - 2] if k in (PABS, PLS, PREF) else (1.0 if k in MULT else 0.0)

    def wipe(self, kinds):
        a = self.a
        for k in kinds:
            a[k * H:(k + 1) * H] = [1.0] * H if k in MULT else [0.0] * H

    def given(self, o):
        return self.g(GUP, o) * self.g(GDN, o) * (self.g(GGRD, o) if not self.g(DIMM, o) else 1.0)

    def passives(self, absorb=0.0, lifesteal=0.0, reflect=0.0):
        for k, v in ((PABS, absorb), (PLS, lifesteal), (PREF, reflect)):
            self.a[k * H:(k + 1) * H] = [v] * H
        return self


def kind_of(kind, v):
    if kind == "given":
        return GUP if v > 0 else GDN
    return KIND.get(kind)


def add_tag(side, k, v, o1, o2):
    side.add(k, v, o1, o2)
    if k in (GUP, DR, ABS, LS, REF, PAR, SHD, DIMM, CIMM):
        side.add(NPOS, 1, o1, o2)
        if k not in (DIMM, CIMM):
            side.add(NSTK, 1, o1, o2)


def from_shotplan(s, R):
    """shotplan.Side (absolute rounds) -> Side (offsets from R)."""
    out = Side(s.hp)
    for t in s.tags:
        kind, v, first, last = t[:4]
        if shotplan.ground(t):
            out.add(GGRD, v, first - R, last - R)
            continue
        k = kind_of(kind, v)
        if k is None or last < R:
            continue
        add_tag(out, k, v, first - R, last - R)
    return out


# ------------------------------------------------------------------ actions
def compile_spec(spec, actor_is_me):
    """shotplan spec -> (base, pierce, [(on_src, kind, value, first_off, last_off)]) relative to the cast offset."""
    base, tags = spec[0], spec[1]
    pierce = len(spec) > 2 and spec[2] == "pierce"
    out = []
    for t in tags:
        who, kind, val, dur = t[0], t[1], t[2], t[3]
        instant = len(t) > 4 and t[4]
        on_src = (who == "me") == actor_is_me
        if kind == "clear":
            out.append((on_src, CLEAR, 0, 0, 0)); continue
        if kind == "cleanse":
            out.append((on_src, CLEANSE, 0, 0, 0)); continue
        if kind == "heal":
            out.append((on_src, HEAL, val, 0, 0)); continue
        if kind == "copy":
            out.append((on_src, COPY, val, 1, dur)); continue
        k = kind_of(kind, val)
        if k is None:
            continue
        o1, o2 = (0, max(dur, 1) - 1) if instant else (1, dur)
        out.append((on_src, k, val, o1, o2))
    return (base, pierce, out)


# Source details (engine process.ts / tags.ts, read 2026-11-11 for the ~1% check). The shotplan-parity test turns
# this off to compare the shared core.
SOURCE_EXACT = True


def apply(src, dst, act, o, scale=1.0):
    """One action at offset o: damage then tags (shotplan.apply order and caps). Returns (to target, to actor)."""
    base, pierce, tags = act
    base *= scale
    to_t = to_s = 0.0
    if base:
        sa, da = src.a, dst.a
        parried = 0.0
        if pierce:
            dmg = base
            dst.wipe((SHD,))
        else:
            dmg = base * src.given(o) * da[TAKEN * H + o] * da[DR * H + o]
            parried = dmg * min(1.0, da[PAR * H + o])
            dmg -= parried
        pre = max(dmg, 0.0)                               # pre-shield damage: the absorb / leech / reflect caps
        if not pierce:
            sh = da[SHD * H + o]
            if sh:
                dmg -= min(sh, dmg)
                dst.wipe((SHD,))
        dmg = max(dmg, 0.0)
        basis = pre if SOURCE_EXACT else dmg
        to_t += dmg - basis * min(0.6, da[ABS * H + o] + da[PABS * H + o]) * (1 - da[HCUT * H + o])
        to_s -= basis * min(0.6, sa[LS * H + o] + sa[PLS * H + o]) * (1 - sa[HCUT * H + o])
        back = parried + basis * min(0.6, da[REF * H + o] + da[PREF * H + o])
        rec = 0.0 if (pierce and SOURCE_EXACT) else dmg * sa[RCL * H + o]      # recoil skips pierce (tags.ts)
        if SOURCE_EXACT:
            # reflect / parry / recoil come back as damage on the attacker through HIS damage-taken modifiers
            # (process.ts calcAdjustedDamage(user, ...))
            adj = sa[TAKEN * H + o] * sa[DR * H + o]
            back *= adj
            rec *= adj
        to_s += rec + back
    for on_src, k, v, o1, o2 in tags:
        side = src if on_src else dst
        if k == CLEAR:
            if not side.g(CIMM, o):
                side.wipe(POSK)
            continue
        if k == CLEANSE:
            side.wipe(NEGK)
            continue
        if k == HEAL:
            if on_src:
                to_s -= v
            continue
        if k == COPY:
            # Shadow Dance: he copies my positive effects onto himself (from next round): my damage-given stack and
            # reductions become his
            if not src.g(BBLK, o):
                for kk in (GUP, DR, ABS, LS, REF):
                    for oo in range(o + o1, min(H, o + o2 + 1)):
                        if kk in MULT:
                            src.a[kk * H + oo] *= dst.a[kk * H + oo]
                        else:
                            src.a[kk * H + oo] += dst.a[kk * H + oo]
            continue
        if not on_src and (v < 0 or k in HOSTILE) and dst.g(DIMM, o):
            continue
        if on_src and v > 0 and k in (GUP, ABS, LS, DR, REF) and src.g(BBLK, o):
            continue
        add_tag(side, k, v, o + o1, o + o2)
    return to_t, to_s


def run_turn(actor, other, acts, o, cap_a, cap_o, scale=1.0):
    dealt = taken = 0.0
    if acts:
        taken += actor.g(WND, o) + actor.g(DRN, o)
    for act in acts:
        d, s = apply(actor, other, act, o, scale)
        dealt += d
        taken += s
    other.hp = min(cap_o, other.hp - dealt)
    actor.hp = min(cap_a, actor.hp - taken)
    return dealt, taken


# ------------------------------------------------------------------ legality
def legal_bundles(st, R, ap, d0, loadout, me0, en0):
    """Every bundle of ready actions with cost in [ap-20, ap], range checked after moves, no shared-lock pairs."""
    A = cd_plan.ACTIONS
    ready = [n for n in loadout if n in A and n in shotplan.MINE and cd_plan.ready_round(st, n) <= R]
    if not any(en0.g(k, 0) for k in (ABS, LS, REF, PAR, SHD, DR)) and en0.given(0) <= 1.0001 or en0.g(CIMM, 0):
        ready = [n for n in ready if n != "clear"]          # nothing clearable, or clear-immune
    if not (me0.g(TAKEN, 0) > 1.0001 or me0.g(GDN, 0) < 0.9999 or me0.g(WND, 0) or me0.g(DRN, 0) or me0.g(RCL, 0)
            or me0.g(HCUT, 0) or me0.g(TAKEN, 1) > 1.0001 or me0.g(WND, 1) or me0.g(DRN, 1)):
        ready = [n for n in ready if n != "cleanse"]        # nothing to cleanse
    if d0 > 1:
        ready.append("step")
    ready.sort(key=lambda n: -A[n][0])
    tags = {n: cd_plan.tags_of(n) if n != "step" else set() for n in ready}
    out = []

    def rec(i, cost, chosen, locks, steps):
        if cost >= ap - 20 and chosen:
            out.append(tuple(chosen))
        for j in range(i, len(ready)):
            n = ready[j]
            c = A[n][0]
            if cost + c > ap or (tags[n] & locks):
                continue
            if n == "step":
                if steps >= 2:
                    continue
                rec(j, cost + c, chosen + [n], locks, steps + 1)   # steps may repeat
                continue
            rec(j + 1, cost + c, chosen + [n], locks | tags[n], steps)

    rec(0, 0, [], set(), 0)
    ok = []
    for b in out:
        moves = sum(cd_plan.MOVES.get(x, 0) for x in b)
        d = max(1, d0 - moves)
        if any(cd_plan.RANGE.get(x, 0) and cd_plan.RANGE[x] < d for x in b):
            continue
        if "step" in b and d0 - sum(cd_plan.MOVES.get(x, 0) for x in b if x != "step") <= 1:
            continue                                         # a step that isn't needed
        ok.append(b)
    return ok


# ------------------------------------------------------------------ opponent
def his_options(cal, ctx, m, e, r):
    """[(weight, [kit names])] for his reply at offset r, read from the live state of both sides."""
    if ctx["afk"]:
        return [(1.0, [])]
    sm = value_model.smoothed
    opts = []
    npos, stack = m.g(NPOS, r), m.g(NSTK, r)
    if ctx["pierce_ready"]:
        p = sm(cal, "pierce_vs_shield") if m.g(SHD, r) else sm(cal, "pierce")
        if ctx["pierce_shown"] and m.g(SHD, r):
            p = max(p, 0.85)
        opts.append((p, ["pierce", "light"]))
    if ctx["clear_held"] and npos >= 1 and not m.g(CIMM, r):
        p = (value_model.clear_risk_4(cal) if stack >= 4 else sm(cal, "clear_vs_3buffs") if stack >= 3 else
             sm(cal, "clear_vs_2buffs") if npos >= 2 else sm(cal, "clear"))
        opts.append((p, ["clear", "light"]))
    if not ctx["smoke_spent"]:
        opts.append((sm(cal, "smoke"), ["smoke", "light"]))
    blocked = e.g(BBLK, r) > 0
    opts.append((sm(cal, "setup") * (0.4 if blocked else 1.0), ["debuff", "light"] if blocked else ["buff", "debuff", "light"]))
    # his 85th-percentile turn at its base rate; his live stack is NOT added to the weight: the engine already
    # multiplies every option by his damage-given and my damage-taken, so a stacked opponent's turn is a burst at
    # its real size (weighting it up again double counted: ANBU R3 / Hikuro R5 read as deaths the director survived)
    opts.append((value_model.BURST_P * (0.35 if blocked else 1.0), ["burst"]))
    opts.append((max(0.05, 1.0 - sum(w for w, _ in opts)), ["turn"]))
    real = ctx.get("his_real")
    if real:
        # his clock: his best real lines on his next turn (from his ready actions, scored from his side) take the
        # weight of the generic pierce / setup / burst / turn options; Clear (state-dependent) and Smoke (an item,
        # not in the public kit) keep their measured odds
        keep = [(w, o) for w, o in opts if o[0] in ("clear", "smoke")]
        if keep and keep[0][1][0] == "clear" and ctx.get("his_real_clear"):
            keep = [(keep[0][0], ctx["his_real_clear"])] + keep[1:]
        rest = max(0.05, 1.0 - sum(w for w, _ in keep))
        opts = keep + [(rest * w, list(b)) for w, b in real]
        tot = sum(w for w, _ in opts)
        return [(w / tot, o) for w, o in opts]
    if ctx["summon"]:
        opts = [(w, o + ["summon"]) for w, o in opts]
    clear_w = sum(w for w, a in opts if "clear" in a)
    rest = sum(w for w, a in opts if "clear" not in a)
    if clear_w and rest:
        clear_w = min(clear_w, 0.95)
        return [(w if "clear" in a else w * (1 - clear_w) / rest, a) for w, a in opts]
    tot = sum(w for w, _ in opts)
    return [(w / tot, a) for w, a in opts]


# ------------------------------------------------------------------ evaluation
def ttk(hp, rate):
    return min(8.0, hp / max(50.0, rate))


def sig(x):
    return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, x))))


class Planner:
    def __init__(self, me0, en0, R, ctx, cal, my_kit, his_kit, st, en_acted, caps, base_turn, clockd=None):
        self.me0, self.en0, self.R, self.ctx, self.cal = me0, en0, R, ctx, cal
        self.my_kit, self.his_kit, self.st, self.en_acted, self.caps = my_kit, his_kit, st, en_acted, caps
        self.base_turn = base_turn
        self.hr = 1 if en_acted else 0                 # his reply offset
        self.hn = 2 if en_acted else 1                 # his next turn offset (after my next turn)
        dmg = [(n, cd_plan.ACTIONS[n][0], my_kit[n]) for n in st["loadout"]
               if n in my_kit and my_kit[n][0] > 0 and n in cd_plan.ACTIONS and n not in ("basic",)]
        self.combos = []                               # damage bundles <= 100 AP for my next-turn potential

        def rec(i, cost, names, nonp, pier):
            if names:
                self.combos.append((frozenset(names), nonp, pier))
            for j in range(i, len(dmg)):
                n, c, act = dmg[j]
                if cost + c <= 100:
                    rec(j + 1, cost + c, names + [n], nonp + (0 if act[1] else act[0]), pier + (act[0] if act[1] else 0))
        rec(0, 0, [], 0.0, 0.0)
        pierce = [n for n, _, act in dmg if act[1]]
        self.combos = [c for c in self.combos if sum(1 for n in c[0] if n in pierce) <= 1]
        self.ready_next = {n for n in st["loadout"] if n in cd_plan.ACTIONS and cd_plan.ready_round(st, n) <= R + 1}
        self.res = value_model.reserves(cal)
        self.pot_cache = {}
        self.clockd = clockd or {}                     # his real kit: candidates, next-turn damage lines, scale
        self.his_cache = {}

    def my_potential(self, b, m, e):
        """Best damage I can deal next turn (offset 1) with what is ready then, through the live multipliers."""
        o = 1
        mult = m.given(o) * e.g(TAKEN, o) * e.g(DR, o) * (1 - min(1.0, e.g(PAR, o)))
        ab = 1 - min(0.6, e.g(ABS, o) + e.g(PABS, o)) * (1 - e.g(HCUT, o))
        locked = set(b)
        key = (frozenset(locked), round(mult, 3))
        best = self.pot_cache.get(key)
        if best is None:
            best = (0.0, 0.0)
            for names, nonp, pier in self.combos:
                if names & locked or not names <= self.ready_next:
                    continue
                v = nonp * mult + pier
                if v > best[0] + best[1]:
                    best = (nonp * mult, pier)
            self.pot_cache[key] = best
        hit, pier = best
        hit = max(0.0, hit - e.g(SHD, o))
        reflected = hit * min(0.6, e.g(REF, o) + e.g(PREF, o)) + (hit / max(1e-6, 1 - min(1.0, e.g(PAR, o))) - hit if e.g(PAR, o) else 0)
        return (hit + pier) * ab + e.g(WND, o) + e.g(DRN, o), reflected

    def his_base(self, used):
        """His raw next-turn damage: with his kit, the best line from what is ready on his next turn minus what his
        reply just used (his cooldowns decide when his burst can come); else his observed / prior base turn."""
        lines = self.clockd.get("next_lines")
        if not lines:
            return self.base_turn
        key = frozenset(used)
        v = self.his_cache.get(key)
        if v is None:
            v = max((d for names, d in lines if not (names & key)), default=0.0) * self.clockd["scale"]
            v = self.his_cache[key] = max(v, 150.0)
        return v

    def his_potential(self, m, e, used=()):
        o = self.hn
        stun = (100 - min(40, e.g(STUN, o))) / 100
        hit = self.his_base(used) * e.given(o) * m.g(TAKEN, o) * m.g(DR, o) * stun
        par = min(1.0, m.g(PAR, o))
        parried = hit * par
        hit = max(0.0, hit - parried - m.g(SHD, o))
        reflected = parried + hit * min(0.6, m.g(REF, o) + m.g(PREF, o))
        hit = hit * (1 - min(0.6, m.g(ABS, o) + m.g(PABS, o)) * (1 - m.g(HCUT, o)))
        return hit + m.g(WND, 1) + m.g(DRN, 1), reflected

    def features(self, b, m, e, used=()):
        my_hp0, en_hp0 = self.me0.hp, self.en0.hp
        swing = (en_hp0 - e.hp) - (my_hp0 - m.hp)
        mine, refl_on_me = self.my_potential(b, m, e)
        his, refl_on_him = self.his_potential(m, e, used)
        mine_net, his_net = mine + refl_on_him, his + refl_on_me
        race = ttk(m.hp, his_net) - ttk(e.hp, mine_net)
        # lethal reads, in turn order: who acts first next round decides whose kill lands (his burst runs ~20% over
        # his line, my estimate is a best line so it is not padded)
        p_kill = sig((mine_net - e.hp) / 250.0)
        p_die = sig((1.2 * his_net - m.hp) / 250.0)
        if self.en_acted:          # he acts first in a round: his next turn comes before mine
            p_kill *= 1 - p_die
        else:
            p_die *= 1 - p_kill
        # the round after: multipliers still live then (2-round buffs / debuffs / reductions pay twice), on a
        # generic burst for me and his base turn for him
        o2, h2 = 2, self.hn + 1
        mine2 = value_model.BURST_BASE * (m.given(o2) * e.g(TAKEN, o2) * e.g(DR, o2) - 1)
        his2 = self.base_turn * (e.given(h2) * m.g(TAKEN, h2) * m.g(DR, h2) * (1 - min(0.6, m.g(ABS, h2))) - 1)
        return [swing, mine_net, -his_net, race, mine2, -his2, p_kill, -p_die]

    def line(self, b):
        """Expected features and terminal value of bundle b over his weighted replies."""
        cm, ce = self.caps
        acts = [self.my_kit[x] for x in b if x in self.my_kit]
        m0, e0 = self.me0.copy(), self.en0.copy()
        if "cleanse" in b:
            m0.wipe(NEGK)
        if any(x in ("phantom", "replace", "step") for x in b):
            m0.wipe((GGRD,))                            # moves fire first: off his ground
        run_turn(m0, e0, acts, 0, cm, ce)
        if e0.hp <= 0:
            return [(self.en0.hp - e0.hp) - (self.me0.hp - m0.hp)] + [0] * (NF - 1), value_model.KILL, self.en0.hp, [(1.0, ["-"])], 1.0
        feats = [0.0] * NF
        term = dmg = 0.0
        opts = self.replies(m0, e0)
        outs = []
        for w, names in opts:
            m, e = m0.copy(), e0.copy()
            real = names and names[0] in self.clockd.get("ids", ())
            stun = 1.0 if real else (100 - min(40, e.g(STUN, self.hr))) / 100
            run_turn(e, m, [self.his_kit[n] for n in names if n in self.his_kit], self.hr, ce, cm, stun)
            dmg += w * (self.en0.hp - e.hp)
            if m.hp <= 0 or e.hp <= 0:
                t = value_model.KILL if e.hp <= 0 < m.hp else -value_model.DEATH
                term += w * t
                f = [(self.en0.hp - e.hp) - (self.me0.hp - m.hp)] + [0] * (NF - 1)
            else:
                f = self.features(b, m, e, names)
            outs.append((w, names, f))
            for i in range(NF):
                feats[i] += w * f[i]
        return feats, term, dmg, outs, 0.0

    def his_score(self, hb, m0, e0):
        """His line from his side on the board he faces: damage now, minus what bounces back, plus what it does to
        his next hit and to mine (his setup up, my setup stripped / smoked / blocked)."""
        ho = self.hr
        m, e = m0.copy(), e0.copy()
        d, t = run_turn(e, m, [self.his_kit[x] for x in hb], ho, 1e9, 1e9)
        o = ho + 1
        his_gain = self.base_turn * (e.given(o) * m.g(TAKEN, o) * m.g(DR, o) - e0.given(o) * m0.g(TAKEN, o) * m0.g(DR, o))
        my_drop = value_model.BURST_BASE * (m0.given(1) * e0.g(TAKEN, 1) * e0.g(DR, 1) - m.given(1) * e.g(TAKEN, 1) * e.g(DR, 1))
        return d - t + 0.7 * his_gain + 0.6 * my_drop

    def his_habit(self, hb):
        """His logged habits for this line (opponents.py), 0 without a model."""
        h = self.clockd.get("habit")
        if not h:
            return 0.0
        return h(hb, self.clockd.get("hr_abs", self.R), self.clockd.get("his_prev"), self.clockd.get("his_n", 0) == 0)

    def replies(self, m0, e0):
        """His reply options on this board. With his kit: his candidate lines re-scored against the position my
        bundle leaves (so my Seal / Clear / stun / Smoke change what he does), top 4 by softmax, plus Smoke (an item
        outside the public kit) at its measured odds. Without a kit: the generic option set."""
        cands = self.clockd.get("cands")
        if not cands or self.ctx["afk"]:
            return his_options(self.cal, self.ctx, m0, e0, self.hr)
        ap = 100 - (20 if e0.g(STUN, self.hr) else 0)
        scored = [(self.his_score(hb, m0, e0) + self.his_habit(hb), list(hb)) for hb, cost in cands if cost <= ap]
        out = clock.soft(scored)
        if not self.ctx["smoke_spent"] and not self.clockd.get("smoke_in_kit"):
            ps = value_model.smoothed(self.cal, "smoke")
            out = [(w * (1 - ps), b) for w, b in out] + [(ps, ["smoke", "light"])]
        return out

    def extras(self, b, ap):
        """Reserve cost, AP unspent (in 20s) and hard guards for the coached blunders."""
        rc = value_model.reserve_cost(b, self.cal, self.R)[0]
        for x in b:
            if x in ("stormblade", "nights") and not self.ctx["pierce_window"]:
                rc += self.res[x]
        cost = sum(cd_plan.ACTIONS[x][0] for x in b)
        guard, why = 0.0, []
        if "basicheal" in b and self.me0.hp > 0.6 * self.caps[0]:
            guard -= 450; why.append("basic heal above 60% HP")
        if "smoke" in b and self.en0.g(DIMM, 0):
            guard -= 800; why.append("smoke into his debuff immunity (smokes only me)")
        if any(x in ("stormblade", "nights") for x in b) and self.en0.g(ABS, 0) >= 0.2:
            guard -= self.en0.g(ABS, 0) * 631
        return rc, (ap - cost) / 20.0, guard, why


_W = None


def load_weights():
    """DEFAULT_W, then planner2_weights.json, then TNR_W (a JSON object, for weight experiments in the simulator)."""
    global _W
    if _W is None:
        w = dict(DEFAULT_W)
        try:
            w.update(json.load(open(WFILE)))
        except (OSError, ValueError):
            pass
        if os.environ.get("TNR_W"):
            w.update(json.loads(os.environ["TNR_W"]))
        _W = w
    return _W


def total(W, feats, term, rc, waste, guard):
    return (W["swing"] * feats[0] + W["mypot"] * feats[1] + W["hispot"] * feats[2] + W["race"] * feats[3]
            + W["mypot2"] * feats[4] + W["hispot2"] * feats[5] + W["kill"] * feats[6] + W["die"] * feats[7] + term - W["reserve"] * rc - W["waste"] * waste + guard)


# ------------------------------------------------------------------ main
def build(a):
    battle, me, others, rows = turn.load_input(a.file)
    if not others:
        return None, "no living enemy"
    en = others[0] if not a.enemy else next((p for p in others if p["username"].lower() == a.enemy.lower()), others[0])
    R = battle["battle.round"]
    my_turn = battle["battle.activeUserId"] == ME
    en_acted = any(r == R and u == en["userId"] for r, u, _, _ in rows)
    me_pos, en_pos = (me["longitude"], me["latitude"]), (en["longitude"], en["latitude"])
    d0 = turn.dist(me_pos, en_pos)
    st = {"loadout": list(cd_plan.LOADOUTS[a.loadout]) + ["basicheal"], "used": turn.my_history(rows)}
    cd_plan.ACTIONS.setdefault("basicheal", (60, 5, None, "heal 600 instant"))
    shotplan.MINE.setdefault("basicheal", (0, [("me", "heal", 600, 0, True)]))
    lines = [f"{r}|{t.strip()}" for r, u, _, ts in rows for t in (ts or [])]
    sme, sen = shotplan.rebuild(lines, ME_NAME, en["username"], me["curHealth"], en["curHealth"])
    stun_lines = [(int(l.split("|")[0]), int(m.group(1)) if (m := re.search(r"\[-(\d+) AP\]", l)) else 20)
                  for l in lines if "dauntless is stunned" in l]
    stun = max([s for r0, s in stun_lines if r0 + 2 >= R and (r0 < R or en_acted)] or [0])
    ap = min(int(me["actionPoints"]) if my_turn else 100, 100 - stun)
    spent, pierce_last, avg = turn.enemy_resources(rows, en["userId"], R)
    cal = value_model.load_cal()
    value_model.calibrate_kit(cal)
    gm = (turn.engine_bridge.opponent_kit(en["userId"]) or {}).get("gearMods") or {}
    gear_dr = float(gm.get("drTakenFromGear", 15))
    afk_acts = [x for r, u, x, _ in rows if u == en["userId"]]
    sm = [(r, m.group(1), int(m.group(2))) for r, u, _, ts in rows if u == en["userId"] for t in (ts or [])
          if (m := re.search(r"^\s*(\S+) was summoned for (\d+) rounds", t))]
    summon = False
    if sm:
        r0, sname, n = sm[-1]
        names = {p["username"].strip(): p["curHealth"] for p in others}
        summon = (names.get(sname, 0) > 0) and r0 + n - 1 >= R
    ctx = {
        "pierce_ready": pierce_last is None or R - pierce_last >= 3 or summon,
        "pierce_shown": pierce_last is not None,
        "clear_held": "clear" not in spent,
        "smoke_spent": "smoke" in spent,
        "afk": bool(afk_acts) and sum(1 for x in afk_acts if x == "wait") * 2 >= len(afk_acts),
        "summon": summon,
        "pierce_window": bool(sme.mult("given", R) < 0.6 or sen.live("shield", R)
                              or 1 - (50 - gear_dr) / 50 * turn._prod(1 - t[1] for t in sen.live("dr", R)) >= 0.55
                              or en["curHealth"] <= 720),
    }
    shotplan.off_ground(sme, rows, ME, turn.MOVE_IDS)
    me0, en0 = from_shotplan(sme, R), from_shotplan(sen, R)
    reach = max(0.4, 1 - 0.1 * max(0, d0 - 4))
    his_kit_raw = value_model.generic_kit(cal, reach)
    # his profile (opp_profile: kit read at battle start -> bloodline -> rank, boost and elements): the prior turn
    # gets his bloodline damage boost; his observed hits already include it
    prof = opp_profile.profile(en["userId"], rows)
    gmul = opp_profile.given_mult(prof)
    mine_prof = opp_profile.own_profile()
    en0.passives(**prof.get("passives", {}))
    me0.passives(**mine_prof.get("passives", {}))
    for k in ("turn", "burst", "hit", "light", "hit2"):
        v = his_kit_raw[k]
        his_kit_raw[k] = (v[0] * gmul,) + tuple(v[1:])
    obs = turn.observed_turns(rows, en["userId"], en["username"], sme, sen)
    if obs:
        n, med = len(obs), sorted(obs)[len(obs) // 2] * reach
        his_kit_raw["turn"] = ((n * med + his_kit_raw["turn"][0]) / (n + 1), [])
        his_kit_raw["burst"] = ((n * max(max(obs) * reach, med * 1.6) + his_kit_raw["burst"][0]) / (n + 1), [])
    his_kit = {k: compile_spec(v, False) for k, v in his_kit_raw.items()}
    # his clock (clock.py): his real kit, what is ready on his reply turn and the turn after, his best lines
    # his kit: the saved equipped kit + what he used in this fight + everything his model saw in other fights
    # (opponents.py over every log), and his habits from those logs (director 2026-11-11: "you weren't using
    # accurate opponent models")
    import opponents as OM
    model = OM.load().get(en["userId"])
    acts = clock.his_actions(en["userId"], rows)
    if model:
        macts = OM.acts_for(model)
        acts = dict(macts, **(acts or {}))
    habit = OM.habit_fn(model) if model else None
    his_turns = OM.turns_of(rows, en["userId"])
    clock_info, clockd = None, {}
    ctx["copier"] = bool(acts) and any(t[1] == "copy" for v in acts.values() for t in v[4][1])
    if acts and not ctx["afk"]:
        scale = gmul / max(1.0, opp_profile.given_mult(mine_prof))
        clockd, clock_info = make_clock(acts, rows, en["userId"], R, en_acted, me0, en0, ctx, cal, his_kit,
                                        his_kit_raw["turn"][0], scale, habit=habit,
                                        his_prev=his_turns[-1][1] if his_turns else None, his_n=len(his_turns))
        clock_info["model"] = (f"{len(model.get('fights', []))} logged fights, {len(model.get('bundles', []))} turns"
                               if model else "no logged fights")
    my_kit = make_my_kit(prof)
    caps = (me.get("maxHealth", 5050), en.get("maxHealth", 5050))
    P = Planner(me0, en0, R, ctx, cal, my_kit, his_kit, st, en_acted, caps, his_kit_raw["turn"][0], clockd)
    # solution-library key: this position plus what his last turn did (solutions.py)
    try:
        import opponents as OM
        import solutions
        his = OM.turns_of(rows, en["userId"])
        last = list(his[-1][1]) if his else []
        P.book_key = solutions.situation_key(P, ctx, st, R, last, clock.acts_from_ids(last))
    except Exception:  # noqa: BLE001  (the library is an aid; planning never depends on it)
        P.book_key = None
    info = dict(battle=battle, me=me, en=en, R=R, my_turn=my_turn, en_acted=en_acted, me_pos=me_pos, en_pos=en_pos,
                d0=d0, ap=ap, stun=stun, others=others, st=st, sme=sme, sen=sen, prof=prof, gmul=gmul, clock=clock_info, rows=rows)
    return P, info


_ENGINE_BASES = None


def engine_bases():
    """Base damage of each of my actions as the game's own combat code computes it (engine_fit.py --write: each
    action fired alone on the pinned engine, no tags; 2026-11-11). Used in place of the log-calibrated bases."""
    global _ENGINE_BASES
    if _ENGINE_BASES is None:
        try:
            _ENGINE_BASES = json.load(open(os.path.join(HERE, "..", "fights", "engine_bases.json")))
        except (OSError, ValueError):
            _ENGINE_BASES = {}
    return _ENGINE_BASES


def make_my_kit(prof):
    """My kit compiled (bases from the engine where measured), with his bloodline DR applied to my jutsu of the
    matching element."""
    idx = opp_profile._index()
    my_kit = {}
    eb = engine_bases()
    for k, v in shotplan.MINE.items():
        if k in eb and v[0]:
            v = (eb[k],) + tuple(v[1:])
        els = (idx.get(turn.ACTION_ID.get(k, ""), ["", []])[1]) or ["None"]
        f = opp_profile.dr_vs(prof, els)
        my_kit[k] = compile_spec(((v[0] * f,) + tuple(v[1:])) if f != 1.0 and not (len(v) > 2 and v[2] == "pierce") else v, True)
    my_kit["step"] = my_kit["stepback"] = (0, False, [])
    cd_plan.ACTIONS.setdefault("step", (10, 0, None, ""))
    return my_kit


def make_clock(acts, rows, en_id, R, en_acted, me0, en0, ctx, cal, his_kit, base_turn, scale, habit=None,
               his_prev=None, his_n=0):
    """His clock for planner2: his kit compiled into his_kit (in place), his candidate reply lines (his 12 best on
    this board, plus his best Clear line and best pure-damage line; re-scored per bundle of mine later) and his
    next-turn damage lines (what is ready then). Returns (clockd, printable info)."""
    hr_abs, hn_abs = (R + 1, R + 2) if en_acted else (R, R + 1)
    for aid, (nm, cost, cd, locks, spec) in acts.items():
        if aid not in his_kit:
            his_kit[aid] = compile_spec(spec, False)
    ready = clock.ready_at(acts, en_id, rows, hr_abs)
    ready_next = clock.ready_at(acts, en_id, rows, hn_abs)
    all_lines = [(hb, sum(acts[x][1] for x in hb)) for hb in clock.bundles(acts, ready, 100)]
    clockd = {"ids": set(acts), "scale": scale, "smoke_in_kit": any("Smoke" in acts[x][0] for x in acts),
              "habit": habit, "his_prev": his_prev, "his_n": his_n, "hr_abs": hr_abs,
              "next_lines": [(frozenset(hb), sum(acts[x][4][0] for x in hb)) for hb in clock.bundles(acts, ready_next, 100)]}
    tmp = Planner(me0, en0, R, ctx, cal, {}, his_kit, {"loadout": [], "used": []}, en_acted, (5050, 5050), base_turn, clockd)
    sc = sorted(((tmp.his_score(hb, me0, en0) + tmp.his_habit(hb), hb, c) for hb, c in all_lines), key=lambda x: -x[0])
    keep = sc[:12]
    for pick in (next((x for x in sc if "clear" in x[1]), None),
                 max(sc, key=lambda x: sum(acts[a][4][0] for a in x[1]), default=None)):
        if pick and pick not in keep:
            keep.append(pick)
    clockd["cands"] = [(hb, c) for _, hb, c in keep]
    lines0 = clock.soft([(s_, list(hb)) for s_, hb, _ in keep])
    nxt = max((d for _, d in clockd["next_lines"]), default=0.0) * scale
    info = dict(ready=[acts[x][0] for x in ready], ready_next=[acts[x][0] for x in ready_next],
                lines=[(w, [acts[x][0] for x in b]) for w, b in lines0], next_dmg=nxt)
    return clockd, info


BOOK_W = float(os.environ.get("TNR_BOOK_W", "450"))     # HP-equivalent bonus x confidence for the solved answer to this position (solutions.json)


def rank(P, bundles, ap, W):
    res = []
    book = None
    key = getattr(P, "book_key", None)
    if key and not os.environ.get("TNR_NO_BOOK"):
        import solutions
        book = solutions.lookup(key, getattr(P, "book_path", None) or solutions.LIVE)
    for b in bundles:
        feats, term, dmg, outs, _ = P.line(b)
        rc, waste, guard, why = P.extras(b, ap)
        if book and book[1] > 0.2 and tuple(sorted(b)) == tuple(sorted(book[0])):
            guard += BOOK_W * book[1]
            why = why + [f"library answer (confidence {book[1]:.0%})"]
        res.append((total(W, feats, term, rc, waste, guard), b, feats, term, rc, waste, guard, why, dmg, outs))
    res.sort(key=lambda x: -x[0])
    if res and res[0][0] < -0.6 * value_model.DEATH:
        res.sort(key=lambda x: -x[8])
        print("DESPERATION: every line loses; ranked by damage to him")
    return res


def rollout_rerank(P, info, res, n, budget, k=4):
    """Decision-time playouts (director 2026-11-11: "it's like having extra processing power"): the top k bundles,
    plus the best Cleanse / Clear line when it is not among them, are each played to the end of the fight n times
    against his model (opponents.py habits + kit; else his saved kit), common seeds; the best mean outcome is fired.
    Replaying the Ziharkk loss, playouts found Cleanse + Thunder's on R2 where the one-turn score ranked it 18th."""
    t0 = time.time()
    try:
        import fightsim
        import opponents as OM
        import solutions
        en_id = info["en"]["userId"]
        m = OM.load().get(en_id)
        acts = OM.acts_for(m) if m else clock.his_actions(en_id, info["rows"])
        if not acts:
            return res
        habit = OM.habit_fn(m) if m else None
        f = fightsim.Fight(acts, info["prof"], not info["en_acted"], seed=7, habit=habit)
        f.me, f.en = P.me0.copy(), P.en0.copy()
        f.rows = [(r, u if u == ME else fightsim.EN_ID, x, None) for r, u, x, _ in info["rows"]]
        f.used = [list(x) for x in info["st"]["used"]]
        f.loadout = list(info["st"]["loadout"])
        f.R = info["R"]
        his = OM.turns_of(info["rows"], en_id)
        f.his_prev, f.his_turns = (his[-1][1] if his else None), len(his)
        cands = [r for r in res[:k]]
        for key in ("cleanse", "clear"):
            if not any(key in r[1] for r in cands):
                extra = next((r for r in res[k:40] if key in r[1]), None)
                if extra:
                    cands.append(extra)
        scored = []
        for r in cands:
            vals = []
            for s in range(n):
                if time.time() - t0 > budget:
                    break
                vals.append(solutions.rollout(f, r[1], 4242 + s))
            if not vals:
                break
            scored.append((sum(vals) / len(vals), r))
        if len(scored) < 2:
            return res
        scored.sort(key=lambda x: (-x[0], -x[1][0]))
        print("playouts: " + " | ".join(f"{'+'.join(r[1])} {v:+.2f}" for v, r in scored)
              + f" ({time.time() - t0:.1f}s)")
        best = scored[0][1]
        return [best] + [r for r in res if r is not best]
    except Exception as e:  # noqa: BLE001  (playouts are an aid; the one-turn ranking stands without them)
        print("playouts skipped:", e)
        return res


def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("file"); ap_.add_argument("--battle", required=True)
    ap_.add_argument("--enemy"); ap_.add_argument("--loadout", default="pvp1"); ap_.add_argument("--top", type=int, default=3)
    ap_.add_argument("--dump")
    ap_.add_argument("--ban", default="", help="action ids or short names the game refused this battle")
    for f in ("--no-engine", "--fast"):
        ap_.add_argument(f, action="store_true")      # accepted for pilot compatibility; planner2 is engine-free
    ap_.add_argument("--keep", type=int, default=0); ap_.add_argument("--cash", type=int, default=0)
    ap_.add_argument("--rollouts", type=int, default=0, help="play the top candidates out to the end N times each")
    ap_.add_argument("--rollout-budget", type=float, default=4.5)
    a = ap_.parse_args()
    t0 = time.time()
    P, info = build(a)
    if P is None:
        print(info); return
    R, me, en = info["R"], info["me"], info["en"]
    print(f"R{R} v{info['battle']['battle.version']} | {'MY TURN' if info['my_turn'] else 'his turn'} | "
          f"{'he acted first this round' if info['en_acted'] else 'I act first this round'}")
    print(f"me {me['curHealth']:.0f} HP AP {info['ap']}{' (STUNNED -%d)' % info['stun'] if info['stun'] else ''}"
          f" | him {en['username']} {en['curHealth']:.0f} HP | dist {info['d0']} | his base turn {P.base_turn:.0f}")
    print(f"me next: given x{P.me0.given(1):.2f} taken x{P.me0.g(TAKEN, 1):.2f} dr x{P.me0.g(DR, 1):.2f} | "
          f"him next: given x{P.en0.given(1):.2f} taken x{P.en0.g(TAKEN, 1):.2f} dr x{P.en0.g(DR, 1):.2f}")
    pr = info["prof"]
    print(f"his profile ({pr.get('source')}): {pr.get('bloodline', '?')} rank {pr.get('rank', '?')} | boost +{pr.get('given', (0,))[0]:.0%} "
          f"on {'/'.join(pr.get('given', (0, []))[1]) or '-'} (x{info['gmul']:.2f} on his hits) | DR {pr.get('dr', (0,))[0]:.0%} "
          f"vs {'/'.join(pr.get('dr', (0, []))[1]) or '-'} | his elements {'/'.join(pr.get('elements', [])) or '?'}")
    ck = info["clock"]
    if ck:
        print(f"his clock: ready on his turn: {', '.join(ck['ready'])}")
        print(f"           ready the turn after: {', '.join(ck['ready_next'])} (his best line then {ck['next_dmg']:.0f} before multipliers)")
        print("           his likely lines: " + " | ".join(f"{w:.0%} {'+'.join(b)}" for w, b in ck["lines"]))
        print(f"           his model: {ck.get('model', '-')}")
    else:
        print("his clock: no saved kit (generic stand-in)")
    if not info["my_turn"]:
        print("not my turn: poll again in <=15 s"); return
    banned = {x for x in a.ban.split(",") if x}
    banned |= {turn.IDS.get(x, x) for x in banned}
    if banned:
        info["st"]["loadout"] = [n for n in info["st"]["loadout"] if n not in banned and turn.ACTION_ID.get(n) not in banned]
        print("banned this battle (refused by the game):", ", ".join(sorted(banned)))
    bundles = legal_bundles(info["st"], R, info["ap"], info["d0"], info["st"]["loadout"], P.me0, P.en0)
    if not bundles:
        print("no legal bundle (check AP/cooldowns)"); return
    W = load_weights()
    res = rank(P, bundles, info["ap"], W)
    if a.rollouts:
        res = rollout_rerank(P, info, res, a.rollouts, a.rollout_budget - (time.time() - t0))
    if a.dump:
        json.dump({"bundles": [{"b": list(r[1]), "f": r[2], "term": r[3], "rc": r[4], "waste": r[5], "guard": r[6],
                                "dmg": r[8]} for r in res]}, open(a.dump, "w"))
    occupied = {(p["longitude"], p["latitude"]) for p in info["others"]}
    print(f"planner2: {len(bundles)} legal bundles in {time.time() - t0:.2f}s. TOP {a.top}:")
    for i, r in enumerate(res[:a.top], 1):
        seq, end = turn.resolve_targets(r[1], info["me_pos"], info["en_pos"], occupied)
        fire = " -> ".join(f"{x}@{t[0]},{t[1]}" for x, _, t in seq)
        f = r[2]
        print(f"{i}. {r[0]:+6.0f}  {fire}  [swing {f[0]:+.0f} mine {f[1]:.0f} his {-f[2]:.0f} race {f[3]:+.2f} kill {f[6]:.0%} die {-f[7]:.0%} "
              f"term {r[3]:+.0f} reserve {r[4]:.0f} unspent {r[5] * 20:.0f}{' GUARD ' + '; '.join(r[7]) if r[7] else ''}]")
    seq, _ = turn.resolve_targets(res[0][1], info["me_pos"], info["en_pos"], occupied)
    print("FIRE:", json.dumps([{"actionId": aid, "longitude": t[0], "latitude": t[1], "name": n} for n, aid, t in seq]))


if __name__ == "__main__":
    main()
