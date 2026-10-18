#!/usr/bin/env python3
"""Bloodright tree evaluator: seven-round HP-equivalent utility, in Codex's Weight unit.

Weight = (utility with the tree bonuses - utility without) / 50.5, i.e. 1 Weight = 1% of a
level-100 health pool (calcHP(100) = 5050). Mechanics are read from TheNinjaRPG@94f9d84
(app/src/libs/combat/tags.ts, potency.ts); each rule cites its source below.

Fixture (the same idea as Codex's round-total review, rebuilt here because Codex's scripts were
not pushed): the bloodline's captured kit against a mirror of itself without tree bonuses, both
level 100 with equal stats, 100 AP per round for 7 rounds, every jutsu at level JUTSU_LEVEL.
The player's cast order is the best legal priority order for that build (all orders for kits of
up to 7 jutsu, a fixed sample above that). Outgoing utility is uncapped; incoming damage is
taken against a finite pool, and healing counts only up to the health actually missing.
Pressure scales the mirror's damage (1.0 normal; the symmetric panel is 0.5 / 1.0 / 1.5).

This is a planning model, not a PvP simulator: no movement, stuns, summons or targeting.
"""
import itertools
import json
import random
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVEL_HP = 5050.0                  # calcHP(100) = 100 + 50*99 (libs/profile.ts, HP_PER_LVL=50)
BASE_HIT = LEVEL_HP / 10           # damageCalc baseline = calcHP/DMG_BASE_HITS (tags.ts)
EP_NORM = 40.0                     # DMG_EP_NORMALIZATION
WEIGHT = 50.5                      # Codex's unit: 1% of LEVEL_HP
ROUNDS = 7
AP = 100
JUTSU_LEVEL = 20                   # JUTSU_LEVEL_CAP (drizzle/constants.ts)
LEECH_CAP = 0.6                    # DAMAGE_LEECH_CAP_RATIO: lifesteal + vamp
AFTERBURN_CAP = 0.6                # afterburn: 60% of the damage it converts (tags.ts afterburn)
POTENCY_TAGS = {"damage", "increasedamagegiven", "decreasedamagegiven", "increasedamagetaken",
                "decreasedamagetaken", "afterburn", "lifesteal", "reflect", "increaseheal", "heal",
                "vamp", "absorb", "consume", "shield", "pierce", "drain", "poison"}  # potency.ts
MODIFIERS = {"increasedamagegiven", "decreasedamagegiven", "increasedamagetaken", "decreasedamagetaken"}
SAMPLE_ORDERS = 2000
TOP_PLANS = 120
TOP_PLANS_LARGE = 120
AGGREGATE = "max"                  # how a build's utility is taken over legal cast orders: max | mean


def load_kits():
    return json.loads((ROOT / "docs/design/bloodright/balance/kits_from_reference_captures.json").read_text())


@dataclass
class Row:
    type: str
    power: float
    rounds: int
    calc: str
    elements: tuple
    generals: tuple
    to_self: bool
    shield_health: float = 0.0
    shield_rounds: int = 3


@dataclass
class Jutsu:
    name: str
    ap: int
    cooldown: int
    rows: list
    classification: str
    chakra: float
    stamina: float


def jutsu_from_capture(j, classification):
    rows = []
    self_target = j.get("target") == "SELF"
    for e in j["effects"]:
        t = e.get("target", "INHERIT")
        # friendlyFire FRIENDLY puts an INHERIT effect on the caster's side whatever the jutsu
        # targets (e.g. a ground jutsu's ward: suragu Lava Wave, hyouga_yui Glacier's Will).
        to_self = t == "SELF" or (t == "INHERIT" and (self_target or e.get("friendlyFire") == "FRIENDLY"))
        rows.append(Row(type=e["type"], power=float(e.get("power", 0)) + JUTSU_LEVEL * float(e.get("powerPerLevel", 0) or 0),
                        rounds=int(e.get("rounds", 0) or 0), calc=e.get("calculation", "static"),
                        elements=tuple(e.get("elements") or ()), generals=tuple(e.get("generalTypes") or ()),
                        to_self=to_self, shield_health=float(e.get("health", 0) or 0),
                        shield_rounds=int(e.get("shieldRounds", 3) or 3)))
    return Jutsu(j["name"], int(j.get("actionCostPerc", 60)), int(j.get("cooldown", 7)), rows, classification,
                 float(j.get("chakraCost", 0) or 0), float(j.get("staminaCost", 0) or 0))


def apply_bonuses(jutsu, bonuses, tree_elements):
    """potency.ts resolvePotencyTags with one static increasepotency per bonus tag: a row is boosted
    when its own elements or the jutsu's classification match the tree's elements."""
    out = []
    for r in jutsu.rows:
        add = 0.0
        if r.type in POTENCY_TAGS and r.type in bonuses:
            elems = r.elements or ("None",)
            match = any((jutsu.classification != "None" and el == jutsu.classification) or el in elems
                        for el in tree_elements)
            if match:
                add = bonuses[r.type]
        if add:
            p = max(0.0, r.power + add)
            if r.calc == "percentage":
                p = min(100.0, p)
            r = Row(**{**r.__dict__, "power": p})
        out.append(r)
    return Jutsu(jutsu.name, jutsu.ap, jutsu.cooldown, out, jutsu.classification, jutsu.chakra, jutsu.stamina)


@dataclass
class Effect:
    type: str
    power: float
    remaining: int
    created: int
    owner: int        # side that cast it
    target: int       # side it sits on
    elements: tuple
    calc: str
    orig: float = 0.0  # wound: damage dealt by the cast
    hp: float = 0.0    # shield / consume hit points


def hit(power, calc):
    if calc == "percentage":
        return LEVEL_HP * power / 100.0
    if calc == "static":
        return power * 10.0
    return BASE_HIT * power / EP_NORM                     # damageCalc 'formula', equal stats


def schedule(kit, order):
    """Fixed-priority policy: each round, cast in priority order whatever is off cooldown and fits."""
    ready = {j.name: 1 for j in kit}
    plan = []
    for rnd in range(1, ROUNDS + 1):
        ap, casts = AP, []
        for j in order:
            if ready[j.name] <= rnd and j.ap <= ap:
                casts.append(j.name)
                ap -= j.ap
                ready[j.name] = rnd + j.cooldown
        plan.append(casts)
    return plan


def simulate(kits, plans, pressure, start_hp=(LEVEL_HP, LEVEL_HP)):
    """Two sides. Returns side-0 utility: damage out - net health lost (healing only up to missing)."""
    effects = []
    hp = list(start_hp)
    out = [0.0, 0.0]
    taken = [0.0, 0.0]
    scale = (1.0, pressure)
    byname = [{j.name: j for j in kits[0]}, {j.name: j for j in kits[1]}]

    def active(e, rnd):
        return e.remaining > 0 and e.created < rnd

    def heal(side, amount):
        gain = max(0.0, min(amount, LEVEL_HP - hp[side]))
        hp[side] += gain

    def damage(src, dst, amount, rnd, kind="damage", elements=("None",), leech=0.0):
        """kind: 'damage' (modifiers, shields, afterburn), 'pierce' (modifiers only: tags.ts
        afterburn skips pierce; adjustDamageGiven/Taken do not), 'true' (drain, poison, wound ticks)."""
        if amount <= 0:
            return 0.0
        amount *= scale[src]
        piercing = kind != "damage"
        if kind != "true":
            mod = 0.0
            for e in effects:
                if not active(e, rnd) or e.type not in MODIFIERS:
                    continue
                if e.elements and not any(x in elements for x in e.elements):
                    continue                                   # getEfficiencyRatio: modifier elements
                if e.type == "increasedamagegiven" and e.target == src:
                    mod += e.power
                elif e.type == "decreasedamagegiven" and e.target == src:
                    mod -= e.power
                elif e.type == "increasedamagetaken" and e.target == dst:
                    mod += e.power
                elif e.type == "decreasedamagetaken" and e.target == dst:
                    mod -= e.power
            amount *= max(0.0, 1 + mod / 100.0)
        dealt = amount
        # shields and consume shields on the defender soak first (tags.ts shield / consume)
        for e in effects:
            if piercing:
                break
            if e.target == dst and e.type in ("shield", "consumeshield") and e.remaining > 0 and e.hp > 0 and amount > 0:
                soak = min(e.hp, amount)
                e.hp -= soak
                amount -= soak
        hp[dst] -= amount
        out[src] += dealt
        taken[dst] += amount
        extra = 0.0
        if not piercing:
            ab = 0.0
            for e in effects:
                if active(e, rnd) and e.type == "afterburn" and e.target == dst:
                    ab += dealt * e.power / 100.0
            extra += min(ab, AFTERBURN_CAP * dealt)
        refl = sum(dealt * e.power / 100.0 for e in effects if active(e, rnd) and e.type == "reflect" and e.target == dst)
        absb = sum(dealt * e.power / 100.0 for e in effects if active(e, rnd) and e.type == "absorb" and e.target == dst)
        ls = sum(e.power / 100.0 for e in effects if active(e, rnd) and e.type == "lifesteal" and e.target == src)
        cons = sum(e.power / 100.0 for e in effects if active(e, rnd) and e.type == "consume" and e.owner == src)
        if extra:
            hp[dst] -= extra; out[src] += extra; taken[dst] += extra
        if refl:
            hp[src] -= refl; out[dst] += refl; taken[src] += refl
        if absb:
            heal(dst, absb)
        heal(src, dealt * min(LEECH_CAP, ls + leech))
        if cons:
            effects.append(Effect("consumeshield", 0, 3, rnd, src, src, (), "static", hp=min(1.0, cons) * dealt))
        return dealt

    for rnd in range(1, ROUNDS + 1):
        for side in (0, 1):
            for name in plans[side][rnd - 1]:
                j = byname[side][name]
                vamp = sum(r.power / 100.0 for r in j.rows if r.type == "vamp")
                dealt_by_cast = 0.0
                for r in j.rows:
                    dst = side if r.to_self else 1 - side
                    if r.type in ("damage", "pierce"):
                        dealt_by_cast += damage(side, dst, hit(r.power, r.calc), rnd, r.type,
                                                r.elements or ("None",), vamp)
                    elif r.type == "heal" and r.rounds == 0:
                        heal(dst, LEVEL_HP * r.power / 100.0 if r.calc == "percentage" else r.power * 10.0)
                for r in j.rows:
                    dst = side if r.to_self else 1 - side
                    if r.rounds <= 0 or r.type in ("damage", "pierce"):
                        continue
                    e = Effect(r.type, r.power, r.rounds, rnd, side, dst, r.elements, r.calc)
                    if r.type == "wound":
                        e.orig = dealt_by_cast
                    if r.type == "shield":
                        e.hp = r.shield_health * min(1.0, r.power / 100.0)   # expected value of the chance roll
                    effects.append(e)
            # damage over time and pool effects owned by this side, ticking on its turn
            for e in effects:
                if not active(e, rnd) or e.owner != side:
                    continue
                if e.type == "wound" and e.orig > 0:
                    damage(side, e.target, e.orig * e.power / 100.0 / scale[side], rnd, "true")
                elif e.type == "drain":
                    amt = LEVEL_HP * e.power / 100.0 if e.calc == "percentage" else e.power   # tags.ts drain
                    damage(side, e.target, amt / scale[side], rnd, "true")
                elif e.type == "heal":
                    heal(e.target, LEVEL_HP * e.power / 100.0 if e.calc == "percentage" else e.power * 10.0)
                elif e.type == "poison":
                    spent = sum(byname[1 - side][n].chakra + byname[1 - side][n].stamina for n in plans[1 - side][rnd - 1])
                    damage(side, e.target, spent * e.power / 100.0 / scale[side], rnd, "true")
        for e in effects:
            if e.created < rnd:
                e.remaining -= 1
    return out[0] - (LEVEL_HP - hp[0]), out[0], LEVEL_HP - hp[0]


class Evaluator:
    def __init__(self, slug, kits=None, jutsu_names=None):
        kits = kits or load_kits()
        k = kits[slug]
        self.slug = slug
        self.elements = tuple(k["elements"])
        cls = self.elements[0] if len(self.elements) == 1 and self.elements[0] != "None" else "None"
        caps = [j for j in k["jutsu"] if not jutsu_names or j["name"] in jutsu_names]
        self.base_kit = [jutsu_from_capture(j, cls) for j in caps]
        n = len(self.base_kit)
        if n <= 7:
            self.orders = list(itertools.permutations(range(n)))
        else:
            rng = random.Random(1729)
            seen = set()
            while len(seen) < SAMPLE_ORDERS:
                p = list(range(n)); rng.shuffle(p); seen.add(tuple(p))
            self.orders = sorted(seen)
        self._plans = {}
        self.mirror_order = None
        self._base = {}

    def plan(self, kit, order):
        key = (tuple(j.ap for j in kit), order)
        if key not in self._plans:
            self._plans[key] = schedule(kit, [kit[i] for i in order])
        return self._plans[key]

    def mirror(self):
        """The opponent: the base kit, playing its own best order at normal pressure."""
        if self.mirror_order is None:
            best = None
            for o in self.orders:
                p = self.plan(self.base_kit, o)
                u = simulate([self.base_kit, self.base_kit], [p, p], 1.0)[0]
                if best is None or u > best[0]:
                    best = (u, o)
            self.mirror_order = best[1]
        return self.plan(self.base_kit, self.mirror_order)

    def utility(self, bonuses, pressure=1.0):
        kit = [apply_bonuses(j, bonuses, self.elements) for j in self.base_kit] if bonuses else self.base_kit
        mplan = self.mirror()
        us = [simulate([kit, self.base_kit], [p, mplan], pressure)[0] for p in self.candidate_plans()]
        return max(us) if AGGREGATE == "max" else sum(us) / len(us)

    def candidate_plans(self, k=None):
        """Bonuses never change AP or cooldowns, so the legal schedules are fixed per kit. Keep the
        distinct ones, best first by base utility, and the top TOP_PLANS of those (checked against
        the full set by scripts/bloodright_balance/check_plans.py)."""
        if getattr(self, "_cands", None) is None:
            mplan = self.mirror()
            seen, ranked = set(), []
            for o in self.orders:
                p = self.plan(self.base_kit, o)
                key = json.dumps(p)
                if key in seen:
                    continue
                seen.add(key)
                ranked.append((simulate([self.base_kit, self.base_kit], [p, mplan], 1.0)[0], key, p))
            ranked.sort(key=lambda t: (-t[0], t[1]))
            self._all_plans = [p for *_, p in ranked]
            limit = TOP_PLANS if len(self.base_kit) <= 7 else TOP_PLANS_LARGE
            self._cands = self._all_plans[:limit]
        return self._cands

    def weight(self, bonuses, pressure=1.0):
        if pressure not in self._base:
            self._base[pressure] = self.utility({}, pressure)
        return (self.utility(bonuses, pressure) - self._base[pressure]) / WEIGHT


def total_bonuses(tree, node_ids):
    tot = {}
    for n in tree["nodes"]:
        if n["id"] in node_ids:
            for t, v in n["bonuses"].items():
                tot[t] = round(tot.get(t, 0) + v, 4)
    return tot


def builds(tree):
    """Paths p1..p4 as [F, H, A] ids; 3-BP completions and the 12 ordered 5-BP builds."""
    paths = {}
    for n in tree["nodes"]:
        paths.setdefault(n["branch"], {})[n["tier"]] = n["id"]
    paths = {p: [d[1], d[2], d[3]] for p, d in sorted(paths.items())}
    return paths


def score_tree(tree, ev, pressures=(1.0,)):
    paths = builds(tree)
    res = {"three": {}, "five": {}, "secondary": {}}
    for pr in pressures:
        three = {p: ev.weight(total_bonuses(tree, ids), pr) for p, ids in paths.items()}
        five = {}
        for p, q in itertools.permutations(paths, 2):
            five[(p, q)] = ev.weight(total_bonuses(tree, paths[p] + paths[q][:2]), pr)
        sec = {}
        for p in paths:
            adds = {q: five[(p, q)] - three[p] for q in paths if q != p}
            hi = max(adds.values())
            sec[p] = (min(adds.values()) / hi) if hi > 0 else 0.0
        res["three"][pr], res["five"][pr], res["secondary"][pr] = three, five, sec
    return res


def summary(tree, ev, pressures=(1.0,)):
    r = score_tree(tree, ev, pressures)
    three = r["three"][1.0]; five = r["five"][1.0]; sec = r["secondary"][1.0]
    return {"three": (min(three.values()), max(three.values())), "five": (min(five.values()), max(five.values())),
            "secondary_floor": min(sec.values()), "detail": r}


if __name__ == "__main__":
    import sys
    trees = json.loads((ROOT / "docs/design/bloodright/balance/round_total/proposal_trees.json").read_text())
    kits = load_kits()
    for slug in (sys.argv[1:] or trees):
        ev = Evaluator(slug, kits)
        s = summary(trees[slug], ev)
        print(f"{slug:28} 3BP {s['three'][0]:5.2f}-{s['three'][1]:5.2f}  5BP {s['five'][0]:5.2f}-{s['five'][1]:5.2f}  sec {s['secondary_floor']*100:5.1f}%")
