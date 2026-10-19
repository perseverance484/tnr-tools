#!/usr/bin/env python3
"""Rebalance Bloodright trees under RUL-2026-10-18-001 with the evaluator in this folder.

Design space (RUL-2026-10-18-001):
  - four paths, Foundation -> Hidden Art -> Advanced Art, 1 BP each, intended build 3+2;
  - one tag per Foundation and Hidden Art, the same tag ascending along the path, and four
    different root tags;
  - percentage tags step +2 / +3, capstone +5, so every finished build totals 5 or 10;
  - Damage uses clean amounts (+0.2 / +0.4 / +0.6 / +0.8 / +1.2), ascending on a Damage path, and
    a build's Damage times the kit's eligible damage rows stays within 5;
  - capstones carry one or two effects; only effects the kit has native, eligible rows for;
    no Wound; Drain only as a +25 capstone effect;
  - Blue Blade Eyes keeps Lifesteal +2 -> +3 -> IDT +5 (no Damage on that path);
    Blood-Enchanted Eyes keeps Vamp on the Lifesteal capstone and Absorb only on the Guard
    (DDT) capstone, with no IDG there.

Objective, in order: the secondary choice (weakest / strongest two-node addition to each
completed path) at normal pressure and on the 0.5/1/1.5 panel, then the spread of the four
completed paths, then closeness of the tree's mean 5-BP build to the roster anchor, then fewer
node changes. Candidates are ranked with per-effect values (the bonuses are close to additive;
see evaluator notes) and the best are verified with the full simulation.

  python3 scripts/bloodright_balance/search.py <slug> [...] [--out DIR]
"""
import itertools
import json
import math
import random
import sys
from pathlib import Path as FsPath

sys.path.insert(0, str(FsPath(__file__).resolve().parent))
import evaluator as E  # noqa: E402

ROOT = E.ROOT
CURRENT = ROOT / "docs/design/bloodright/balance/round_total/proposal_trees.json"
PCT = ["increasedamagegiven", "decreasedamagegiven", "increasedamagetaken", "decreasedamagetaken", "afterburn",
       "lifesteal", "reflect", "absorb", "consume", "heal", "pierce", "poison", "vamp"]
DAMAGE_FH = [(0.2, 0.4), (0.2, 0.6), (0.4, 0.6), (0.4, 0.8), (0.2, 0.8)]
DAMAGE_CAP = [0.4, 0.6, 0.8, 1.2]
PRESSURES = (0.5, 1.0, 1.5)
SECONDARY_SCREEN = 0.90
DOUBLE_ROOTS = "--double-roots" in sys.argv   # variant: a percentage root may step +5 / +5 (total 10)
ROUND_TOTALS = (5.0, 10.0)
# Variant "round5" (proposal, 2026-10-19): a jutsu's displayed value stays round when every finished
# percentage total is a multiple of 5 (capped kit rows read 30/35/40 at level 25). Roots may total
# 5, 10 or 15 (steps 2/3, 4/6, 6/9: still rising), capstones +5 or +10, finished totals any multiple
# of 5 up to ROUND5_CAP; Pierce moves to a power ladder like Damage with its own budget.
ROUND5 = "--round5" in sys.argv or "--node5" in sys.argv
# Variant "node5": every node is +5 or +10 of one percentage effect (or a Damage / Pierce power
# step), and a path's Hidden Art may carry a different effect from its Foundation. Every build,
# partial ones included, then shows round values.
NODE5 = "--node5" in sys.argv
ROUND5_CAP = 20.0
PCT_ROOT_TOTALS = [(2.0, 3.0), (4.0, 6.0), (6.0, 9.0)]
PIERCE_FH = [(0.2, 0.4), (0.2, 0.6), (0.4, 0.6), (0.4, 0.8), (0.4, 1.2), (0.8, 1.2)]
PIERCE_CAP = [0.4, 0.8, 1.2, 1.6]
PIERCE_ROWS = {}         # slug -> eligible pierce rows, filled by search()
STRENGTH_BAND = 0.10     # mean 5-BP build within about +-10% of the Taiyo anchor before any penalty
STRENGTH_WEIGHT = float(sys.argv[sys.argv.index("--strength-weight") + 1]) if "--strength-weight" in sys.argv else 6.0
CHANGE_COST = 0.04       # a changed node (which then needs a new name) must buy a visible improvement


def eligible_tags(ev):
    """Effect types with at least one native row the tree's bonus reaches (potency.ts matching)."""
    out = {}
    for j in ev.base_kit:
        for r in j.rows:
            if r.type not in E.POTENCY_TAGS or r.type == "wound":
                continue
            elems = r.elements or ("None",)
            if any((j.classification != "None" and el == j.classification) or el in elems for el in ev.elements):
                out[r.type] = out.get(r.type, 0) + 1
    return out


def damage_ceiling(rows):
    """Largest clean per-row Damage total whose sum over eligible rows stays within 5."""
    if not rows:
        return 0.0
    return math.floor(round(5.0 / rows / 0.2, 6)) * 0.2


class TreePath:
    __slots__ = ("root", "f", "h", "cap", "htag")

    def __init__(self, root, f, h, cap, htag=None):
        self.root, self.f, self.h, self.cap = root, f, h, dict(cap)
        self.htag = htag or root

    def nodes(self):
        return [{self.root: self.f}, {self.htag: self.h}, dict(self.cap)]

    def key(self):
        return (self.root, self.f, self.htag, self.h, tuple(sorted(self.cap.items())))


def path_options(tags, slug):
    """Every legal path for this kit, before the cross-path checks."""
    roots = [t for t in tags if t in PCT or t == "damage"]
    caps = []
    if ROUND5:
        singles = ([(t, a) for t in tags if t in PCT and t != "pierce" for a in (5.0, 10.0)]
                   + [("damage", d) for d in DAMAGE_CAP if "damage" in tags]
                   + [("pierce", d) for d in PIERCE_CAP if "pierce" in tags])
    else:
        singles = [(t, 5.0) for t in tags if t in PCT] + [("damage", d) for d in DAMAGE_CAP if "damage" in tags]
    if "drain" in tags:
        singles.append(("drain", 25.0))
    for a in singles:
        caps.append({a[0]: a[1]})
    for a, b in itertools.combinations(singles, 2):
        if a[0] != b[0]:
            caps.append({a[0]: a[1], b[0]: b[1]})
    out = []
    if NODE5:
        pct = [t for t in tags if t in PCT and t != "pierce"]
        for root in roots:
            if root in ("damage", "pierce"):
                fhs = [(root, f, root, h) for f, h in (DAMAGE_FH if root == "damage" else PIERCE_FH)]
            else:
                fhs = [(root, f, ht, h) for f in (5.0, 10.0) for ht in pct for h in (5.0, 10.0)
                       if ht != root or h >= f]
            for rt, f, ht, h in fhs:
                for cap in caps:
                    if rt in ("damage", "pierce") and rt in cap and cap[rt] <= h:
                        continue
                    out.append(TreePath(rt, f, h, cap, ht))
        return [p for p in out if keystone_ok(slug, p)]
    for root in roots:
        if ROUND5:
            fhs = DAMAGE_FH if root == "damage" else PIERCE_FH if root == "pierce" else PCT_ROOT_TOTALS
        else:
            fhs = DAMAGE_FH if root == "damage" else ([(2.0, 3.0), (5.0, 5.0)] if DOUBLE_ROOTS else [(2.0, 3.0)])
        for f, h in fhs:
            for cap in caps:
                if root in ("damage", "pierce") and root in cap and cap[root] <= h:
                    continue          # ascending along a Damage / Pierce path
                out.append(TreePath(root, f, h, cap))
    return [p for p in out if keystone_ok(slug, p)]


def keystone_ok(slug, p):
    if slug == "blue_blade_eyes":
        if p.root == "lifesteal" and (p.htag != "lifesteal" or set(p.cap) != {"increasedamagetaken"}
                                      or (not NODE5 and p.cap != {"increasedamagetaken": 5.0})):
            return False
        if p.root != "lifesteal" and "increasedamagetaken" in p.cap and p.cap.get("increasedamagetaken"):
            return True
    if slug == "blood_enchanted_eyes":
        if p.root == "lifesteal" and "vamp" not in p.cap:
            return False
        if p.root != "lifesteal" and "vamp" in p.cap:
            return False
        if "absorb" in p.cap and p.root != "decreasedamagetaken":
            return False
        if p.root == "decreasedamagetaken" and ("absorb" not in p.cap or "increasedamagegiven" in p.cap):
            return False
        if p.root == "absorb":
            return False
    return True


def tree_ok(slug, paths, dmg_rows):
    if len({p.root for p in paths}) != 4:
        return False
    # distinctive capstones (RUL-2026-10-18-001): no two alike, no effect on more than two
    caps = [tuple(sorted(p.cap)) for p in paths]
    if len(set(caps)) != 4:
        return False
    use = {}
    for c in caps:
        for t in c:
            use[t] = use.get(t, 0) + 1
    if any(n > (3 if t == "damage" else 2) for t, n in use.items()):   # Taiyo puts Damage on three
        return False
    if slug == "blue_blade_eyes" and not any(p.root == "lifesteal" for p in paths):
        return False
    if slug == "blood_enchanted_eyes" and not ({"lifesteal", "decreasedamagetaken"} <= {p.root for p in paths}):
        return False
    # finished builds: every percentage tag totals 5 or 10 (RUL-2026-10-18-001)
    three, five = builds_of(paths)
    for b in list(three.values()) + list(five.values()):
        for t, v in b.items():
            if ROUND5:
                if t in PCT and t != "pierce" and (abs(v / 5 - round(v / 5)) > 1e-9 or v > ROUND5_CAP):
                    return False
            elif t in PCT and v not in ROUND_TOTALS:
                return False
    # every finished build is its own package: four distinct completed paths, twelve distinct 5-BP builds
    keys3 = {tuple(sorted(b.items())) for b in three.values()}
    keys5 = {tuple(sorted(b.items())) for b in five.values()}
    if len(keys3) != 4 or len(keys5) != 12:
        return False
    budgets = [("damage", dmg_rows)]
    if ROUND5:
        budgets.append(("pierce", PIERCE_ROWS.get(slug, 0)))
    return all(max_allocation(paths, t) <= damage_ceiling(rows) + 1e-9 for t, rows in budgets)


def max_allocation(paths, tag):
    """Largest total of a flat-power tag over every legal allocation: one capstone at most,
    prerequisites, 5 BP."""
    fh = [(p.nodes()[0].get(tag, 0), p.nodes()[1].get(tag, 0)) for p in paths]
    best = 0.0
    for i, p in enumerate(paths):            # with path i's capstone
        own = sum(n.get(tag, 0) for n in p.nodes())
        others = sorted((a + b for j, (a, b) in enumerate(fh) if j != i), reverse=True)
        singles = sorted((a for j, (a, _) in enumerate(fh) if j != i), reverse=True)
        best = max(best, own + max(others[0], singles[0] + singles[1] if len(singles) > 1 else 0))
    pair = sorted((a + b for a, b in fh), reverse=True)
    best = max(best, pair[0] + pair[1] + max(a for a, _ in fh))
    return best


def totals(node_lists):
    t = {}
    for n in node_lists:
        for k, v in n.items():
            t[k] = round(t.get(k, 0) + v, 4)
    return t


def builds_of(paths):
    three = {i: totals(paths[i].nodes()) for i in range(4)}
    five = {(i, j): totals(paths[i].nodes() + paths[j].nodes()[:2]) for i in range(4) for j in range(4) if i != j}
    return three, five


class Scorer:
    def __init__(self, ev):
        self.ev = ev
        self.single = {}
        self.exact = {}

    def tag_value(self, tag, amount, pressure):
        k = (tag, round(amount, 4), pressure)
        if k not in self.single:
            self.single[k] = self.ev.weight({tag: amount}, pressure)
        return self.single[k]

    def additive(self, bonus, pressure):
        return sum(self.tag_value(t, a, pressure) for t, a in bonus.items())

    def full(self, bonus, pressure):
        k = (tuple(sorted(bonus.items())), pressure)
        if k not in self.exact:
            self.exact[k] = self.ev.weight(bonus, pressure)
        return self.exact[k]


def evaluate(paths, value, anchor, current_keys):
    three, five = builds_of(paths)
    res = {}
    for pr in PRESSURES:
        t = {i: value(b, pr) for i, b in three.items()}
        f = {k: value(b, pr) for k, b in five.items()}
        sec = []
        for i in range(4):
            adds = [f[(i, j)] - t[i] for j in range(4) if j != i]
            hi = max(adds)
            sec.append(min(adds) / hi if hi > 1e-9 else 0.0)
        res[pr] = (t, f, min(sec))
    sec_n = res[1.0][2]
    sec_p = min(_panel_secondary(res))
    t1 = res[1.0][0]
    spread = min(t1.values()) / max(t1.values()) if max(t1.values()) > 0 else 0.0
    mean5 = sum(res[1.0][1].values()) / 12
    dev = abs(math.log(max(mean5, 1e-6) / anchor))
    changes = sum(1 for i, p in enumerate(paths) for a, b in zip(p.nodes(), current_keys[i]) if a != b)
    floor = min(sec_n, sec_p)
    score = (3.0 * min(floor, SECONDARY_SCREEN) + 2.0 * min(spread, SECONDARY_SCREEN)
             + 0.3 * (floor + spread) - STRENGTH_WEIGHT * max(0.0, dev - STRENGTH_BAND) - CHANGE_COST * changes)
    return score, {"secondary_normal": sec_n, "secondary_panel": sec_p, "three_spread": spread, "mean5": mean5,
                   "three": t1, "five": res[1.0][1], "changes": changes}


def _panel_secondary(res):
    """Secondary choice on the panel average of the three pressures."""
    t = {i: sum(res[pr][0][i] for pr in PRESSURES) / len(PRESSURES) for i in range(4)}
    f = {k: sum(res[pr][1][k] for pr in PRESSURES) / len(PRESSURES) for k in res[1.0][1]}
    out = []
    for i in range(4):
        adds = [f[(i, j)] - t[i] for j in range(4) if j != i]
        hi = max(adds)
        out.append(min(adds) / hi if hi > 1e-9 else 0.0)
    return out


def current_paths(tree):
    ids = E.builds(tree)
    by = {n["id"]: n["bonuses"] for n in tree["nodes"]}
    out = []
    for p in sorted(ids):
        f, h, a = (dict((k, float(v)) for k, v in by[i].items()) for i in ids[p])
        (root, fv), = f.items()
        out.append(TreePath(root, fv, h[root], a))
    return out


def search(slug, tree, anchor, kits=None, restarts=None, seed=7, verify=40):
    restarts = restarts or (20 if NODE5 else 60)
    ev = E.Evaluator(slug, kits)
    tags = eligible_tags(ev)
    dmg_rows = tags.get("damage", 0)
    PIERCE_ROWS[slug] = tags.get("pierce", 0)
    opts = path_options(tags, slug)
    scorer = Scorer(ev)
    cur = current_paths(tree)
    cur_nodes = [p.nodes() for p in cur]
    rng = random.Random(seed)
    add = scorer.additive

    def ok(paths):
        return tree_ok(slug, paths, dmg_rows)

    if len({p.root for p in opts}) < 4:
        return {"slug": slug, "eligible": tags, "infeasible": "fewer than four eligible root effects for four distinct paths",
                "current_info": _jsonable(evaluate(cur, scorer.full, anchor, cur_nodes)[1])}
    pool = {}
    starts = [cur] if ok(cur) else []
    tries = 0
    while len(starts) < restarts and tries < 200000:
        tries += 1
        cand = rng.sample(opts, 4)
        if ok(cand):
            starts.append(cand)
    for start in starts:
        paths = list(start)
        best, _ = evaluate(paths, add, anchor, cur_nodes)
        improved = True
        while improved:
            improved = False
            for i in rng.sample(range(4), 4):
                for o in opts:
                    trial = paths[:i] + [o] + paths[i + 1:]
                    if not ok(trial):
                        continue
                    s, _ = evaluate(trial, add, anchor, cur_nodes)
                    if s > best + 1e-9:
                        best, paths, improved = s, trial, True
        pool[tuple(p.key() for p in paths)] = (best, paths)
    ranked = sorted(pool.values(), key=lambda t: -t[0])[:verify]
    verified = []
    for _, paths in ranked:
        s, info = evaluate(paths, scorer.full, anchor, cur_nodes)
        verified.append((s, paths, info))
    verified.sort(key=lambda t: -t[0])
    s, paths, info = verified[0]
    cs, cinfo = evaluate(cur, scorer.full, anchor, cur_nodes)
    return {"slug": slug, "eligible": tags, "damage_ceiling": damage_ceiling(dmg_rows), "score": s,
            "paths": [{"root": p.root, "f": p.f, "htag": p.htag, "h": p.h, "cap": p.cap} for p in paths], "info": _jsonable(info),
            "current_score": cs, "current_ok": ok(cur), "current_info": _jsonable(cinfo)}


def _jsonable(info):
    if info is None:
        return None
    out = dict(info)
    out["three"] = {f"p{i + 1}": round(v, 3) for i, v in info["three"].items()}
    out["five"] = {f"p{i + 1}+p{j + 1}": round(v, 3) for (i, j), v in info["five"].items()}
    for k in ("secondary_normal", "secondary_panel", "three_spread", "mean5"):
        out[k] = round(info[k], 4)
    return out


def anchor_value(trees, kits):
    """Roster anchor: the accepted Taiyo exemplar's mean 5-BP build under this evaluator."""
    ev = E.Evaluator("taiyo_kami", kits)
    sc = Scorer(ev)
    paths = current_paths(trees["taiyo_kami"])
    _, five = builds_of(paths)
    return sum(sc.full(b, 1.0) for b in five.values()) / 12


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_dir = FsPath(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else None
    if out_dir:
        args = [a for a in args if a != str(out_dir)]
    for flag in ("--strength-weight", "--target"):
        if flag in sys.argv:
            val = sys.argv[sys.argv.index(flag) + 1]
            args = [a for a in args if a != val]
    trees = json.loads(CURRENT.read_text())
    kits = E.load_kits()
    # --target W: pull every tree toward an absolute mean 5-BP Weight (a rule set's roster level)
    # instead of the pre-rebalance Taiyo exemplar.
    anchor = float(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else anchor_value(trees, kits)
    print(f"anchor (Taiyo mean 5-BP, normal pressure): {anchor:.3f}")
    for slug in args or trees:
        r = search(slug, trees[slug], anchor, kits)
        r["anchor"] = anchor
        if "infeasible" in r:
            print(f"{slug:28} INFEASIBLE: {r['infeasible']} (eligible: {sorted(r['eligible'])})")
            if out_dir:
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / f"{slug}.json").write_text(json.dumps(r, indent=1) + "\n")
            continue
        i, c = r["info"], r["current_info"]
        print(f"{slug:28} now sec {c['secondary_normal']*100:5.1f}/{c['secondary_panel']*100:5.1f} spread {c['three_spread']*100:5.1f} mean5 {c['mean5']:.2f}"
              f"  ->  sec {i['secondary_normal']*100:5.1f}/{i['secondary_panel']*100:5.1f} spread {i['three_spread']*100:5.1f} mean5 {i['mean5']:.2f} changes {i['changes']}")
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{slug}.json").write_text(json.dumps(r, indent=1) + "\n")
