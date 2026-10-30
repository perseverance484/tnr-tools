#!/usr/bin/env python3
"""The Haul payout re-fit for RUL-2026-10-30-060 item 4 (offline: fights do not depend on the payout).

Same rung, points and sensible-route definitions as tools/haul_payout_fit.py (sensible = the best 3-step, 1-locker,
no-cut route; every other route of 2+ steps but the timid CC is compared with it). That tool's local search could not
leave its start on the Ore Vault and kept the greedy band ahead of the ceiling, so this one searches globally with the
ruling's ceiling first:

  J = 50 * max(0, worst - 1.20) + 2 * |sensible - 7.6| + 10 * max(0, CC/sensible - 0.75)
      + GW * max(0, greedy target - greedy clear value) / 7.5            (target 21.0M, the Ore Vault 15.0M; GW 1)
      + the layout floors of haul_payout_fit.py (every step >= 0.8, locker >= 2.0 on the vault and bone, Bloom step 5
        >= step 4 + 1.5) + 0.01 * the change from the current points.

Clear rates: --results (state-merged, every legal path) overridden by every --exact file (40-seed exact runs).

  python3 haul_payout_minmax.py fit   --results R.json --exact E1.json,E2.json --layout trophy [--seed 1]
  python3 haul_payout_minmax.py table --results R.json --exact E1.json,E2.json --layout trophy --points '{"step":[..],"locker":x}'
  python3 haul_payout_minmax.py summary --results R.json --exact ... --points-file fit.json --out summary.json
"""
import json, os, random, sys

VALUE = {"hunter": {"C": 4.2, "R": 6.1, "E": 6.7, "L": 11.5}, "gatherer": {"C": 3.2, "R": 4.9, "E": 5.4, "L": 10.5}}
a = sys.argv[1:]
mode = a[0]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
d = json.load(open(opt("--results")))
EX = {}
for f in (opt("--exact", "") or "").split(","):
    if f:
        for r in json.load(open(f))["results"]:
            EX.setdefault(r["variant"], {}).update({p["path"]: p["clearPct"] for p in r["paths"]})
P = d["settings"]["params"]


def table(lay, step, locker):
    L = P["layouts"][lay]; q = L["quest"]; cut = L["points"]["cut"]
    lv = [sum(VALUE[q][t] for t in r["chests"]) + sum(VALUE[q][b["tier"]] * b["chance"] / 100 for b in r.get("bonus", [])) for r in P["ladder"][q]]
    r = next(r for r in d["results"] if r["variant"] == lay)
    rows = []
    for p in r["paths"]:
        path = p["path"]
        if not path:
            continue
        pts = sum(step[i] - (cut[i] if c == "X" else 0) + (locker if c == "L" else 0) for i, c in enumerate(path))
        k = max(i for i, x in enumerate(lv) if x <= pts + 1e-9) if lv[0] <= pts + 1e-9 else 0
        ex = path in EX.get(lay, {})
        c = EX.get(lay, {}).get(path, p["clearPct"])
        rows.append({"path": path, "ev": lv[k] * c / 100, "value": lv[k], "clear": c, "exact": ex})
    sens = [x for x in rows if len(x["path"]) == 3 and x["path"].count("L") == 1 and "X" not in x["path"]]
    S = max(x["ev"] for x in sens)
    for x in rows:
        x["pct"] = x["ev"] / S
    rows.sort(key=lambda x: -x["ev"])
    return S, rows


def stats(lay, step, locker):
    S, rows = table(lay, step, locker)
    cmp_ = [x for x in rows if len(x["path"]) >= 2 and x["path"] != "CC"]
    worst = max(cmp_, key=lambda x: x["pct"])
    cc = next((x["ev"] for x in rows if x["path"] == "CC"), 0) / S
    gl = [x for x in rows if len(x["path"]) == 5 and x["path"].count("L") >= 3]
    live = [x for x in gl if x["clear"] >= 15] or gl
    g = max(live, key=lambda x: (x["clear"], x["value"])) if live else None
    return S, rows, worst, cc, g


def J(lay, step, locker, cur):
    S, rows, worst, cc, g = stats(lay, step, locker)
    GT = 15.0 if lay == "vault" else 21.0
    gv = max(x["value"] for x in rows if len(x["path"]) == 5 and x["path"].count("L") >= 3 and x["clear"] >= 15) \
        if any(len(x["path"]) == 5 and x["path"].count("L") >= 3 and x["clear"] >= 15 for x in rows) else (g["value"] if g else 0)
    j = 50 * max(0, worst["pct"] - 1.20) + 2 * abs(S - 7.6) + 10 * max(0, cc - 0.75) + float(opt("--gw", "1")) * max(0, GT - gv) / 7.5
    j += sum(10 * max(0, 0.8 - s) ** 2 for s in step[1:]) + 10 * max(0, {"vault": 2.0, "bone": 2.0}.get(lay, 1.0) - locker) ** 2
    if lay == "bloom":
        j += 10 * max(0, step[3] + 1.5 - step[4]) ** 2
    j += 0.01 * (sum(abs(x - y) for x, y in zip(step, cur[0])) + abs(locker - cur[1]))
    return j


if mode == "fit":
    lay = opt("--layout"); L = P["layouts"][lay]; q = L["quest"]
    lv0 = VALUE[q][P["ladder"][q][0]["chests"][0]]
    cur = (L["points"]["step"][:], L["points"]["locker"])
    rnd = random.Random(int(opt("--seed", "1")))
    best, bj = cur, J(lay, *cur, cur)
    for it in range(int(opt("--iters", "40000"))):
        if it % 4 == 0:
            step = [round(rnd.uniform(lv0, lv0 + 2.5), 1)] + [round(rnd.uniform(0.5, 9), 1) for _ in range(4)]
            locker = round(rnd.uniform(0.5, 5), 1)
        else:
            step, locker = best[0][:], best[1]
            i = rnd.randrange(6)
            if i < 5:
                step[i] = round(max(0.3, step[i] + rnd.choice([-0.4, -0.2, -0.1, 0.1, 0.2, 0.4])), 1)
            else:
                locker = round(max(0.3, locker + rnd.choice([-0.4, -0.2, -0.1, 0.1, 0.2, 0.4])), 1)
        step[0] = max(step[0], lv0)
        j = J(lay, step, locker, cur)
        if j < bj:
            best, bj = (step, locker), j
    S, rows, worst, cc, g = stats(lay, *best)
    print(json.dumps({"layout": lay, "step": best[0], "locker": best[1], "J": round(bj, 3), "sensible": round(S, 2),
                      "worst": [worst["path"], round(worst["pct"], 3), "exact" if worst["exact"] else "merged"],
                      "ccPct": round(cc, 2), "greedy": g and [g["path"], g["clear"], g["value"]]}))
elif mode == "table":
    pts = json.loads(opt("--points"))
    S, rows, worst, cc, g = stats(opt("--layout"), pts["step"], pts["locker"])
    print(opt("--layout"), "sensible", round(S, 2))
    for x in rows[: int(opt("--top", "12"))]:
        print(f"  {x['path']:6s} EV {x['ev']:5.2f} value {x['value']:5.1f} clear {x['clear']:5.1f}% {'exact ' if x['exact'] else 'merged'} {x['pct'] * 100:5.0f}%")
elif mode == "summary":
    fit = json.load(open(opt("--points-file")))
    out = {"ruling": "RUL-2026-10-30-060 item 4", "results": os.path.basename(opt("--results")),
           "exact": [os.path.basename(f) for f in opt("--exact").split(",")], "pages": {}}
    for lay, pts in fit["pages"].items():
        S, rows, worst, cc, g = stats(lay, pts["step"], pts["locker"])
        out["pages"][lay] = {**pts, "sensible": round(S, 2), "sensibleRoute": next(x["path"] for x in rows if x["pct"] == 1.0),
                             "worst": {"route": worst["path"], "pct": round(worst["pct"] * 100, 1), "exact": worst["exact"]},
                             "ccPct": round(cc * 100, 1), "greedy": g and {"route": g["path"], "clear": g["clear"], "value": g["value"]},
                             "routesAbove100": [{"route": x["path"], "pct": round(x["pct"] * 100, 1), "clear": x["clear"],
                                                 "value": x["value"], "exact": x["exact"]}
                                                for x in rows if x["pct"] > 1.0 + 1e-9 and len(x["path"]) >= 2 and x["path"] != "CC"]}
    json.dump(out, open(opt("--out"), "w"), indent=1)
    for lay, v in out["pages"].items():
        print(lay, v["step"], v["locker"], "sensible", v["sensible"], v["sensibleRoute"], "worst", v["worst"], "greedy", v["greedy"])
