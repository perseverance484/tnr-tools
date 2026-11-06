import json, sys, glob, statistics, collections
# usage: moe_confirm_summary.py TAG [DIR]  -> per-cell summary of the 30-run confirmation
tag = sys.argv[1]
D = sys.argv[2] if len(sys.argv) > 2 else "results/pass6_wip/upstream/"
CLOCK = ("Glass Remembers", "own turn")
def med(x): return statistics.median(x) if x else None
for f in sorted(glob.glob(D + tag + "_*.json")):
    d = json.load(open(f)); kill = d.get("kill", "sayo")
    for cn, c in d["cells"].items():
        runs = c["runs"]; n = len(runs)
        clears = sum(1 for r in runs if r["cleared"])
        rec = [0, 0]; hold = [0, 0]; unw = 0; ubd = 0; sit = []; stage = collections.defaultdict(lambda: [[], []])
        loss = collections.Counter(); lossAct = collections.Counter(); ohko = 0; s7 = [0, 0]; une = 0
        for r in runs:
            for a in r["acts"]:
                s = a.get("sets", {})
                if a["act"] == 2 and "Recast" in s: rec[0] += s["Recast"]["mark"]; rec[1] += s["Recast"]["land"]
                if a["act"] == 3 and "Hold Still" in s: hold[0] += s["Hold Still"]["mark"]; hold[1] += s["Hold Still"]["land"]
                g = a.get("paneOnSafe") or {}; s7[0] += g.get("n", 0); s7[1] += g.get("hitPlayer", 0); une += (a.get("recastUnetched") or {}).get("n", 0)
                unw += a.get("unwarned", 0) or 0; ubd += a.get("unmarkedButDrawn", 0) or 0
                if a["act"] == 1 and a.get("maxSafeSit") is not None: sit.append(a["maxSafeSit"])
                st = a.get("stage")
                if st and st["turns"]: stage[a["act"]][0].append(med(st["hazards"])); stage[a["act"]][1].append(100 * st["moved"] / st["turns"])
                dc = a.get("deathCause")
                if dc:
                    k = "clock" if any(w in dc for w in CLOCK) else "filler" if any(w in dc for w in ("Lancet","Strike","Sweep","Tether","Quiet","Attack")) else "reading"
                    loss[k] += 1; lossAct[(a["act"], dc.split(": ", 1)[-1])] += 1
                    if a.get("maxHit", {}).get("dmg", 0) >= 0.99 * a.get("maxHp", 6250) and a["maxHit"]["by"] == dc: ohko += 1
        stg = {k: (round(med(v[0]) or 0), round(med(v[1]) or 0)) for k, v in sorted(stage.items())}
        print(f"{cn} ({kill}): clear {clears}/{n} | Recast marks/lands {rec[0]}/{rec[1]} | HoldStill marks/lands {hold[0]}/{hold[1]} | unwarned {unw} (drawn {ubd}) | camp A1 max/med {max(sit) if sit else '-'}/{med(sit)} | stage {stg} | losses {dict(loss)} | full-HP one-shots {ohko} | S7 pane-on-safe {s7[0]} (on player {s7[1]}) | unetched Recasts {une}")
        print("   deaths:", dict(lossAct.most_common(6)))
