#!/usr/bin/env python3
"""Turn search results into the rebalance overlay and its review sheet.

  python3 scripts/bloodright_balance/apply.py <search-output-dir>

Writes:
  docs/design/bloodright/balance/scorer_v1/trees.json   node bonuses per bloodline (the overlay
      scripts/bloodright_from_naming.py applies over the naming-pass CSV), plus scores and the
      nodes whose effects changed (their names need a naming review)
  docs/design/bloodright/balance/scorer_v1/REVIEW.md    cumulative build totals per tree

Each new path is placed on the current branch that starts with the same effect when there is one,
so a node name stays with the effect it was written for.
"""
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "docs/design/bloodright/balance/round_total/proposal_trees.json"
OUT = ROOT / "docs/design/bloodright/balance/scorer_v1"
LABEL = {"damage": "Damage", "increasedamagegiven": "IDG", "decreasedamagegiven": "DDG", "increasedamagetaken": "IDT",
         "decreasedamagetaken": "DDT", "afterburn": "Afterburn", "lifesteal": "Lifesteal", "reflect": "Reflect",
         "absorb": "Absorb", "consume": "Consume", "heal": "Heal", "pierce": "Pierce", "poison": "Poison",
         "vamp": "Vamp", "drain": "Drain"}


def num(v):
    return int(v) if float(v).is_integer() else round(v, 2)


def fmt(bonus):
    parts = []
    for t in sorted(bonus, key=lambda t: (t != "damage", LABEL.get(t, t))):
        v = bonus[t]
        parts.append(f"+{num(v)} {LABEL.get(t, t)}" if t in ("damage", "drain") else f"+{num(v)}% {LABEL.get(t, t)}")
    return ", ".join(parts) or "none"


def place(cur_tree, new_paths):
    """Map each new path to a branch p1..p4, preferring the branch with the same root effect."""
    by_branch = {}
    for n in cur_tree["nodes"]:
        by_branch.setdefault(n["branch"], {})[n["tier"]] = n
    cur_roots = {b: next(iter(d[1]["bonuses"])) for b, d in by_branch.items()}
    best = None
    for perm in itertools.permutations(sorted(by_branch)):
        same = sum(cur_roots[b] == p["root"] for b, p in zip(perm, new_paths))
        if best is None or same > best[0]:
            best = (same, perm)
    return dict(zip(best[1], new_paths)), by_branch


def main(src):
    src = Path(src)
    current = json.loads(CURRENT.read_text())
    overlay, review = {}, []
    review.append("# Bloodright rebalance (scorer v1)\n")
    review.append("Cumulative Bloodright bonuses per build, prerequisites included (RUL-2026-10-18-001 "
                  "presentation). Weight = seven-round HP-equivalent value / 50.5 (1 = 1% of a level-100 "
                  "health pool), scored by `scripts/bloodright_balance/` against a mirror of the kit.\n")
    for slug in sorted(current):
        f = src / f"{slug}.json"
        r = json.loads(f.read_text())
        name = current[slug]["bloodline"]["name"]
        if "infeasible" in r:
            overlay[slug] = {"status": "unchanged: " + r["infeasible"], "eligible": r["eligible"]}
            review.append(f"\n## {name}\n\nUnchanged. {r['infeasible'].capitalize()} "
                          f"(eligible: {', '.join(sorted(LABEL.get(t, t) for t in r['eligible'] if t in LABEL))}). "
                          "Needs its element decided first.\n")
            continue
        placed, by_branch = place(current[slug], r["paths"])
        nodes, renamed = {}, []
        for b in sorted(placed):
            p = placed[b]
            new = [{p["root"]: p["f"]}, {p["root"]: p["h"]}, p["cap"]]
            for tier, bonus in enumerate(new, 1):
                nid = f"{b}_t{tier}"
                nodes[nid] = {k: num(v) for k, v in bonus.items()}
                old = by_branch[b][tier]["bonuses"]
                if set(old) != set(bonus):
                    renamed.append({"id": nid, "name": by_branch[b][tier]["name"], "was": fmt(old), "now": fmt(bonus)})
        info = r["info"]
        overlay[slug] = {
            "status": "rebalanced",
            "nodes": nodes,
            "rename_needed": renamed,
            "scores": {k: info[k] for k in ("secondary_normal", "secondary_panel", "three_spread", "mean5")},
            "before": {k: r["current_info"][k] for k in ("secondary_normal", "secondary_panel", "three_spread", "mean5")},
        }
        # review sheet: four completed paths and twelve 5-BP builds, cumulative
        def total(ids):
            t = {}
            for i in ids:
                for k, v in nodes[i].items():
                    t[k] = round(t.get(k, 0) + v, 4)
            return t
        names = {n["id"]: n["name"] for n in current[slug]["nodes"]}
        review.append(f"\n## {name}\n")
        review.append(f"Paths within {info['three_spread']*100:.0f}% of each other; weakest add-on "
                      f"{min(info['secondary_normal'], info['secondary_panel'])*100:.0f}% of the strongest; "
                      f"average full build {info['mean5']:.2f} Weight (before: {r['current_info']['mean5']:.2f}).\n")
        review.append("| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |\n|---|---|---|---|---|")
        for b in sorted(placed):
            ids = [f"{b}_t1", f"{b}_t2", f"{b}_t3"]
            cells = [f"{names[i]}: {fmt(nodes[i])}" for i in ids]
            review.append(f"| {b} | {cells[0]} | {cells[1]} | {cells[2]} | {fmt(total(ids))} |")
        review.append("\n5-BP builds (completed path + another path's Foundation and Hidden Art):\n")
        for a in sorted(placed):
            for c in sorted(placed):
                if a != c:
                    review.append(f"- {a} + {c}: {fmt(total([f'{a}_t1', f'{a}_t2', f'{a}_t3', f'{c}_t1', f'{c}_t2']))}")
        if renamed:
            review.append("\nNodes whose effects changed (names need review):\n")
            for x in renamed:
                review.append(f"- {x['id']} {x['name']}: {x['was']} -> {x['now']}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "trees.json").write_text(json.dumps(overlay, indent=1, ensure_ascii=False) + "\n")
    (OUT / "REVIEW.md").write_text("\n".join(review) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}/trees.json and REVIEW.md")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
