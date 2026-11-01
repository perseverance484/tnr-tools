import json, sys, collections
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/zombie_sim/pyramid_runs.json"))
runs = d["runs"]
G = collections.defaultdict(list)
for r in runs:
    G[(r["mode"], r["kit"], r["band"], r["level"])].append(r)
print(f"{'mode':16} {'kit':6} {'band':4} {'lvl':>3} | clear | where runs end (stage:count) | boss 1st-try win | avg boss rounds | player HP left after W1/W2/W3")
for k in sorted(G, key=lambda k: (k[0], k[1], -k[2], k[3])):
    rs = G[k]
    clear = sum(r["cleared"] for r in rs)
    ends = collections.Counter()
    boss1 = []; bossR = []; hpLeft = collections.defaultdict(list); timeouts = 0; deaths = 0
    for r in rs:
        last = r["stages"][-1]
        if not r["cleared"]:
            ends[last["stage"]] += 1
        for s in r["stages"]:
            for a in s["attempts"]:
                if a["winner"] == "none": timeouts += 1
                if a["winner"] == "boss": deaths += 1
            won = [a for a in s["attempts"] if a["winner"] == "player"]
            if won and s["stage"] != "Boss":
                a = won[0]; hpLeft[s["stage"]].append(round(100 * a["end"]["hp"] / a["end"]["maxHp"]))
            if s["stage"] == "Boss":
                boss1.append(s["attempts"][0]["winner"] == "player")
                bossR += [a["rounds"] for a in s["attempts"]]
    hp = " / ".join(f"{sum(v)//len(v)}%" if (v := hpLeft[w]) else "-" for w in ("Wave 1", "Wave 2", "Wave 3"))
    b1 = f"{sum(boss1)}/{len(boss1)}" if boss1 else "-"
    br = f"{sum(bossR)/len(bossR):.0f}" if bossR else "-"
    print(f"{k[0]:16} {k[1]:6} {k[2]:<4} {k[3]:>3} | {clear}/{len(rs)} | {dict(ends) or '-'} | {b1} | {br} | {hp} | timeouts {timeouts} deaths {deaths}")
