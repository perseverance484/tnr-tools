#!/usr/bin/env python3
"""Tables for the Mother of Echoes tuning runs (engine/moe.ts --out); shards of one cell are merged.

    python3 harness/skyglass_wreck_sim/tools/moe_tables.py harness/skyglass_wreck_sim/results/moe_final_*.json

A cell is "model:policy" plus the kill order when it is not the default (Sayo first). Per act: entered / won, median
rounds, deaths' causes, set-piece lands per fight / hits on the player / unmarked blasts, idle boss turns, specials.
"""
import json
import statistics
import sys
from collections import Counter, defaultdict


def main(paths):
    cells = defaultdict(list)
    for p in paths:
        doc = json.load(open(p))
        for name, c in doc["cells"].items():
            label = name + ("" if doc.get("kill", "sayo") == "sayo" else f" ({doc['kill']} first)")
            cells[label].extend(c["runs"])
    print("| Cell | Runs | Full clear | Act I won/entered (median rounds) | Act II | Act III | Unmarked blasts |")
    print("|---|---|---|---|---|---|---|")
    detail = []
    for label, runs in cells.items():
        n = len(runs)
        fc = sum(1 for r in runs if r["cleared"])
        row = [label, str(n), f"{fc} ({round(100 * fc / n, 1)}%)"]
        unm = 0
        for a in (1, 2, 3):
            acts = [x for r in runs for x in r["acts"] if x["act"] == a]
            if not acts:
                row.append("-")
                continue
            won = sum(1 for x in acts if x["outcome"] == "won")
            row.append(f"{won}/{len(acts)} ({statistics.median(x['rounds'] for x in acts)})")
            unm += sum(x["unmarkedTotal"] for x in acts)
            deaths = Counter(x["deathCause"] or "?" for x in acts if x["outcome"] == "lost")
            stalled = sum(1 for x in acts if x["outcome"] == "stalled")
            sets = defaultdict(lambda: Counter())
            for x in acts:
                for k, s in x["sets"].items():
                    sets[k].update({kk: vv for kk, vv in s.items()})
            specials = Counter()
            idle, turns = Counter(), Counter()
            for x in acts:
                specials.update(x["specials"])
                idle.update(x["bossIdle"])
                turns.update(x["bossTurns"])
            kf = Counter((x["killFirst"] or "").replace("moe-ai-", "") for x in acts if x["killFirst"])
            setTxt = "; ".join(f"{k} {round(s['land'] / len(acts), 1)}/{int(s['hit'])}/{int(s['unmarked'])}" for k, s in sets.items()) or "-"
            idleTxt = ", ".join(f"{k.replace('moe-ai-', '')} {idle[k]}/{turns[k]}" for k in turns)
            specTxt = ", ".join(f"{k} {v}" for k, v in sorted(specials.items()))
            dTxt = "; ".join(f"{k} {v}" for k, v in deaths.most_common(4)) or "-"
            detail.append(f"| {label} | {a} | {dTxt} | {stalled} | {setTxt} | {idleTxt} | {specTxt} | {', '.join(f'{k} {v}' for k, v in kf.items()) or '-'} |")
        row.append(str(unm))
        print("| " + " | ".join(row) + " |")
    print()
    print("| Cell | Act | Deaths (top 4) | Stalled | Set pieces: lands per fight / hits on player / unmarked | Idle boss turns / turns | Specials (total casts) | Killed first |")
    print("|---|---|---|---|---|---|---|---|")
    for line in detail:
        print(line)


if __name__ == "__main__":
    main(sys.argv[1:])
