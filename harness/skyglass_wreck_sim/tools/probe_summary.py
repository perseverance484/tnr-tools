#!/usr/bin/env python3
"""Condense results/probe_mechanics.json into per-scenario findings (seed 1 timeline + all-seed counts).

Usage: probe_summary.py results/probe_mechanics.json
"""
import json
import sys

d = json.load(open(sys.argv[1]))
print("sources:", json.dumps(d["sources"], indent=1))
for p in d["probes"]:
    print(f"\n### {p['key']}: {p['question']}")
    print(f"jutsu {p['jutsu']['name']} target={p['jutsu']['target']} method={p['jutsu']['method']} range={p['jutsu']['range']} cd={p['jutsu']['cooldown']} effects={p['jutsu']['effects']}")
    print(f"casts per seed: {p['castsPerSeed']}")
    for run in p["runs"][:1]:
        print(f"seed {run['seed']}: outcome {run['outcome']} after {run['rounds']} rounds; player starts {run['playerStart']}")
        pos = {"player": run["playerStart"]}
        for l in run["log"]:
            if l["actor"] == "player" or l["actor"].startswith("probe") or l["actor"].startswith(("summon", "unit")):
                pos[l["actor"]] = l["to"]
            interesting = l["action"] not in ("move", "wait") or l["hp"] or l.get("newUnits")
            if l["actor"].startswith(("summon", "unit")):
                interesting = True
            if not interesting:
                continue
            ground = [g for g in (l.get("ground") or []) if g["type"] not in ("visual",)]
            cells = sorted({(g["x"], g["y"], g["type"], g.get("rounds")) for g in ground})
            pl = pos.get("player")
            on = [c for c in cells if pl and (c[0], c[1]) == tuple(pl)]
            extra = ""
            if l.get("newUnits"):
                extra += " NEW " + ", ".join(f"{n['label']}@({n['x']},{n['y']}) hp {n['hp']}" for n in l["newUnits"])
            if l["newEffects"]:
                extra += " fx " + ",".join(l["newEffects"])
            if cells:
                extra += f" ground[{len(cells)} cells: {sorted({c[2] for c in cells})} rounds {sorted({c[3] for c in cells})}; player@{pl} on-cell={bool(on)}]"
            print(f"  r{l['round']} {l['actor']:<24} {str(l['action'])[:30]:<30} rule {l['rule']}/{l['authored']} {l['from']}->{l['to']} hp {l['hp']}{extra}")
