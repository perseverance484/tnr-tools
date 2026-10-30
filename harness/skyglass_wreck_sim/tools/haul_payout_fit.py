#!/usr/bin/env python3
"""The Haul payout fit (RUL-2026-10-29-044): choose each page's haul points so that, with guaranteed chests,

  - the sensible run (best 3-step, 1-locker path) averages about the old S-rank payout (7.5M),
  - no path (2+ steps, other than the timid CC) has an EV more than ~20% above it,
  - the timid run (CC) pays clearly less,
  - a full greedy clear (5 steps, 3+ lockers) is worth about 3x the old payout (--greedy lo,hi; RUL-2026-10-29-045).

Clear rates come from a results file (--exhaustive or --paths); fights do not depend on the payout, so the fit is offline.
The ladder (chest bundles) and the step-4 cut penalty are fixed; the fit searches step points and locker points.

  python3 haul_payout_fit.py results.json [--params haul_spec.json] [--layouts trophy,bone] [--iters 20000] [--seed 1] [--exact exact.json] [--out fit.json]
"""
import json
import random
import sys

VALUE = {"hunter": {"C": 4.2, "R": 6.1, "E": 6.7, "L": 11.5}, "gatherer": {"C": 3.2, "R": 4.9, "E": 5.4, "L": 10.5}}
OLD = 7.5

args = sys.argv[1:]
src = args[0]
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
iters = int(opt("--iters", "20000"))
# greedy clear value band, x the old payout (RUL-2026-10-29-044: 2-2.5x; -045: ~3x)
GW = float(opt("--gw", "0.5"))
CAPW = float(opt("--capw", "40"))
GLO, GHI = (float(x) for x in opt("--greedy", "2.8,3.2").split(","))
rnd = random.Random(int(opt("--seed", "1")))
d = json.load(open(src))
P = json.load(open(opt("--params")))["params"] if opt("--params") else d["settings"]["params"]  # --params: a haul_spec.json (current params)
only = opt("--layouts")


def ladder_values(q):
    return [sum(VALUE[q][t] for t in r["chests"]) + sum(VALUE[q][b["tier"]] * b["chance"] / 100 for b in r.get("bonus", [])) for r in P["ladder"][q]]


def rung_value(q, pts, lv):
    k = 0
    for i, v in enumerate(lv):
        if v <= pts + 1e-9:
            k = i
    return lv[k]


def points(path, step, locker, cut):
    return sum(step[i] - (cut[i] if c == "X" else 0) + (locker if c == "L" else 0) for i, c in enumerate(path))


def evaluate(paths, q, lv, step, locker, cut):
    ev = {}
    for p in paths:
        val = rung_value(q, points(p["path"], step, locker, cut), lv) if p["path"] else 0
        ev[p["path"]] = (val * p["clearPct"] / 100, val, p["clearPct"])
    sens = [k for k in ev if len(k) == 3 and k.count("L") == 1 and "X" not in k]
    S = max(ev[k][0] for k in sens) if sens else 0
    greedy = [k for k in ev if len(k) == 5 and k.count("L") >= 3]
    return ev, S, greedy


# Layout identity floors: a locker is always worth clearly more than a crate; the Ore Vault's and the Bone Store's
# lockers are rich; the Bloom Cellar's last step is the steep one.
MIN_LOCKER = {"vault": 2.0, "bone": 2.0}


def loss(paths, q, lv, step, locker, cut, layout=""):
    ev, S, greedy = evaluate(paths, q, lv, step, locker, cut)
    if S <= 0:
        return 1e9
    L = 4 * (S - OLD) ** 2
    for k, (e, v, c) in ev.items():
        if len(k) >= 2 and k != "CC":
            L += CAPW * max(0, e / S - 1.2) ** 2
    if "CC" in ev:
        L += 20 * max(0, ev["CC"][0] / S - 0.75) ** 2
    live = [k for k in greedy if ev[k][2] >= 15] or greedy
    if live:
        gv = max(ev[k][1] for k in live)
        L += GW * (max(0, GLO * OLD - gv) ** 2 + max(0, gv - GHI * OLD) ** 2)
    # haul points should grow with depth: every step adds something
    L += sum(10 * max(0, 0.8 - s) ** 2 for s in step[1:])
    L += 10 * max(0, MIN_LOCKER.get(layout, 1.0) - locker) ** 2
    if layout == "bloom":
        L += 10 * max(0, step[3] + 1.5 - step[4]) ** 2
    return L


# --exact file: exact per-seed clear rates override the state-merged ones for the paths it has
EX = {}
if opt("--exact"):
    for r in json.load(open(opt("--exact")))["results"]:
        EX[r["variant"]] = {p["path"]: p["clearPct"] for p in r["paths"]}

out = {}
for r in d["results"]:
    v = r["variant"]
    if "+" in v or (only and v not in only.split(",")):
        continue
    lay = P["layouts"][v]
    q = lay["quest"]
    lv = ladder_values(q)
    cut = lay["points"]["cut"]
    paths = [dict(p, clearPct=EX.get(v, {}).get(p["path"], p["clearPct"])) for p in r["paths"]]
    best = (lay["points"]["step"][:], lay["points"]["locker"])
    bl = loss(paths, q, lv, best[0], best[1], cut, v)
    for it in range(iters):
        if it % 4 == 0:  # random restart near the current best
            step = [round(max(0.3, s + rnd.uniform(-1.0, 1.0)), 1) for s in best[0]]
            locker = round(max(0.3, best[1] + rnd.uniform(-1.0, 1.0)), 1)
        else:
            step = best[0][:]
            i = rnd.randrange(6)
            if i < 5:
                step[i] = round(max(0.3, step[i] + rnd.choice([-0.3, -0.2, -0.1, 0.1, 0.2, 0.3])), 1)
                locker = best[1]
            else:
                locker = round(max(0.3, best[1] + rnd.choice([-0.3, -0.2, -0.1, 0.1, 0.2, 0.3])), 1)
        step[0] = max(step[0], lv[0])  # one crate pays the lowest rung
        lo = loss(paths, q, lv, step, locker, cut, v)
        if lo < bl:
            best, bl = (step, locker), lo
    ev, S, greedy = evaluate(paths, q, lv, best[0], best[1], cut)
    top = sorted(((e, k) for k, (e, _, _) in ev.items() if len(k) >= 2), reverse=True)[:5]
    g = max(((ev[k][2], ev[k][1], k) for k in greedy), default=None)  # the greedy path most likely to clear: (clear %, value, path)
    out[v] = {"step": best[0], "locker": best[1], "cut": cut, "loss": round(bl, 3), "sensible": round(S, 2),
              "cc": round(ev.get("CC", (0,))[0], 2), "top": [(k, round(e, 2), round(e / S, 2)) for e, k in top],
              "greedyBestValue": g}
    print(v, json.dumps(out[v]))
json.dump(out, open(opt("--out", "/dev/null"), "w"), indent=1)
