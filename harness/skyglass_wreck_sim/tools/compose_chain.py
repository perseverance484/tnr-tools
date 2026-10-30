#!/usr/bin/env python3
"""Compose Crownhold route chains offline from per-fight tables (engine/crownhold.ts --table).

A fight at full pools gives a sample of (outcome, HP cost). The composed chain assumes a fight's HP cost does not
depend on the HP the player brings (the player loses when the cost reaches the HP carried). This is a tuning
surrogate only: the reported route numbers come from real chains (crownhold.ts --chain), which carry every pool.

  compose_chain.py TABLE.json [TABLE.json ...] [--boss-scale D3=0.8,D4=0.7] [--reg-scale D4.REG4=0.5]
                  [--war-restore 30] [--n 4000] [--json]
Later tables override earlier ones per (fight, variant).
"""
import json
import random
import statistics as st
import sys

ROUTES = {
    "clean": (3, "none", False),
    "alert": (3, "alarm", False),
    "healing": (4, "none", True),
    "war": (4, "war", False),
}


def load(paths):
    rows = {}
    for p in paths:
        d = json.load(open(p))
        for r in d.get("table", []):
            if r["hp"] < 1:
                continue
            rows[(r["fight"], r["variant"])] = [(x["outcome"] == "won", 100 - x["endHp"], x["rounds"]) for x in r["runs"]]
    return rows


def compose(rows, n=4000, scale=None, seed=7, reg_scale=None, war_restore=0.0):
    scale = scale or {}
    reg_scale = reg_scale or {}
    rnd = random.Random(seed)
    out = {}
    for route, (nreg, var, heal) in ROUTES.items():
        clears = 0
        losses = {}
        entry = {d: [] for d in ["D2", "D3", "D4", "D5"]}
        bwin = {d: [0, 0] for d in entry}
        for _ in range(n):
            hp = 100.0
            lost = None
            for d in ["D2", "D3", "D4", "D5"]:
                for r in range(1, nreg + 1):
                    won, cost, _ = rnd.choice(rows[(f"{d}.REG{r}", "none")])
                    cost *= reg_scale.get(f"{d}.REG{r}", 1.0)
                    if not won or cost >= hp:
                        lost = f"{d}.REG{r}"
                        break
                    hp -= cost
                if lost:
                    break
                if heal:
                    hp = 100.0
                elif route == "war" and war_restore:
                    hp = min(100.0, hp + war_restore)
                entry[d].append(hp)
                key = (f"{d}.BOSS", var) if (f"{d}.BOSS", var) in rows else (f"{d}.BOSS", "none")
                won, cost, _ = rnd.choice(rows[key])
                cost *= scale.get(d, 1.0)
                bwin[d][1] += 1
                if not won or cost >= hp:
                    lost = f"{d}.BOSS"
                    break
                bwin[d][0] += 1
                hp -= cost
            if lost:
                losses[lost] = losses.get(lost, 0) + 1
            else:
                clears += 1
        out[route] = {
            "clearPct": round(100 * clears / n, 1),
            "lossesAt": dict(sorted(losses.items(), key=lambda kv: -kv[1])),
            "bossEntryHpMedian": {d: (round(st.median(v), 1) if v else None) for d, v in entry.items()},
            "bossWinPctOfReached": {d: (round(100 * w / t, 1) if t else None) for d, (w, t) in bwin.items()},
        }
    return out


def fight_table(rows):
    t = {}
    for (f, v), xs in sorted(rows.items()):
        wins = [c for w, c, _ in xs if w]
        t[f"{f}/{v}"] = {
            "n": len(xs), "winPct": round(100 * len(wins) / len(xs), 1),
            "costMedian": round(st.median(wins), 1) if wins else None,
            "costP90": round(sorted(wins)[int(0.9 * (len(wins) - 1))], 1) if wins else None,
            "roundsMedian": st.median([r for _, _, r in xs]),
        }
    return t


if __name__ == "__main__":
    args = sys.argv[1:]
    paths = [a for a in args if a.endswith(".json")]
    scale = {}
    if "--boss-scale" in args:
        for kv in args[args.index("--boss-scale") + 1].split(","):
            k, v = kv.split("=")
            scale[k] = float(v)
    n = int(args[args.index("--n") + 1]) if "--n" in args else 4000
    reg_scale = {}
    if "--reg-scale" in args:
        for kv in args[args.index("--reg-scale") + 1].split(","):
            k, v = kv.split("=")
            reg_scale[k] = float(v)
    war_restore = float(args[args.index("--war-restore") + 1]) if "--war-restore" in args else 0.0
    rows = load(paths)
    res = {"fights": fight_table(rows), "routes": compose(rows, n, scale, reg_scale=reg_scale, war_restore=war_restore)}
    if "--json" in args:
        print(json.dumps(res, indent=1))
    else:
        for k, v in res["fights"].items():
            print(f"{k:22s} win {v['winPct']:5.1f}  cost med {v['costMedian']}  p90 {v['costP90']}  rounds {v['roundsMedian']}")
        for k, v in res["routes"].items():
            print(f"{k:8s} clear {v['clearPct']:5.1f}%  entry {v['bossEntryHpMedian']}  bossWin {v['bossWinPctOfReached']}  losses {v['lossesAt']}")
