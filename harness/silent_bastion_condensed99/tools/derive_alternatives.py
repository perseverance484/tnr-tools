#!/usr/bin/env python3
"""Derive content-only alternatives to the condensed 99-node candidate (FAIL remediation options).

The candidate routes each `bN.recovery_later` WIN edge straight into a `reset_quest`. At the pinned
engine a pending battle's string `nextObjectiveId` is pre-selected while the fight is live, so that
reset fires the moment the recovery fight starts (see docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md,
finding C1). Every option below inserts one dialog `dN.recovered` between the recovery WIN and the
reset (+4 objectives) and differs only in which existing dialog gate it folds to stay within budget:

  alt99_f4gate     terminal "Protocol access" routes straight to bN.n.f4    (-4: dN.n.f4)          = 99
  alt99_alertgate  wrong puzzle answers route straight to bN.n.boss.alert  (-4: dN.n.boss.alert)  = 99
  alt95_bossgates  puzzle answers route straight to both commander battles (-8: boss.clean/alert) = 95

Every battle keeps a dialog predecessor (the terminal / puzzle dialog, as the protocol dialog already
does for Medical/Combat). Nothing else changes. These are OPTIONS for director acceptance, not design.

  python3 tools/derive_alternatives.py          # write graphs/*.json
  python3 tools/derive_alternatives.py --check  # verify committed graphs are current
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../.."))
SRC = "state/silent_bastion_condensed99_candidate.json"
DIVS = (2, 3, 4, 5)

def add_recovered(nodes):
    out = []
    for n in nodes:
        if n["id"].endswith(".recovery_later"):
            d = n["division"]
            n = {**n, "onWin": f"d{d}.recovered"}
            out.append(n)
            out.append({"id": f"d{d}.recovered", "kind": "dialog", "next": f"r{d}.reset_later_win", "division": d,
                        "lane": "recovery", "purpose": "Recovery fight won; confirm before rewinding to regular 2 (dialog-gated reset)."})
            continue
        out.append(n)
    return out

def fold(nodes, gates):
    """Remove the single-next dialog gates in `gates` and point their predecessors at the battle."""
    by = {n["id"]: n for n in nodes}
    repl = {g: by[g]["next"] for g in gates}
    out = []
    for n in nodes:
        if n["id"] in repl:
            continue
        n = copy.deepcopy(n)
        for c in n.get("choices", []):
            c["to"] = repl.get(c["to"], c["to"])
        if n.get("next") in repl:
            n["next"] = repl[n["next"]]
        out.append(n)
    return out

VARIANTS = {
    "alt99_f4gate": lambda d: [f"d{d}.n.f4"],
    "alt99_alertgate": lambda d: [f"d{d}.n.boss.alert"],
    "alt95_bossgates": lambda d: [f"d{d}.n.boss.alert", f"d{d}.n.boss.clean"],
}

def derive(src):
    res = {}
    for name, gates in VARIANTS.items():
        nodes = fold(add_recovered(copy.deepcopy(src["nodes"])), [g for d in DIVS for g in gates(d)])
        kinds = {}
        for n in nodes:
            kinds[n["kind"]] = kinds.get(n["kind"], 0) + 1
        g = {k: v for k, v in src.items() if k != "nodes"}
        g.update({
            "kind": "NON_EXECUTABLE_REMEDIATION_OPTION",
            "variant": name,
            "derivedFrom": SRC,
            "derivation": "harness/silent_bastion_condensed99/tools/derive_alternatives.py",
            "directorApproval": "NOT_SELECTED; option for director acceptance",
            "runtimeProof": "see docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md",
            "counts": {"total": len(nodes), "dialogs": kinds.get("dialog", 0), "battles": kinds.get("battle", 0),
                       "resets": kinds.get("reset", 0), "win": kinds.get("win", 0), "fail": kinds.get("fail", 0),
                       "uniqueEncounterSlots": len({n["encounterSlot"] for n in nodes if n["kind"] == "battle"})},
            "foldedDialogGates": [g for d in DIVS for g in gates(d)],
            "addedDialogs": [f"d{d}.recovered" for d in DIVS],
            "nodes": nodes,
        })
        g.pop("graphCheck", None)
        res[name] = g
    return res

def main():
    src = json.load(open(os.path.join(REPO, SRC)))
    check = "--check" in sys.argv
    bad = 0
    for name, g in derive(src).items():
        path = os.path.join(HERE, "..", "graphs", f"{name}.json")
        text = json.dumps(g, indent=1) + "\n"
        if check:
            cur = open(path).read() if os.path.exists(path) else None
            print(f"{name}: {'current' if cur == text else 'STALE'} ({g['counts']['total']} nodes)")
            bad |= cur != text
        else:
            open(path, "w").write(text)
            print(f"wrote graphs/{name}.json ({g['counts']['total']} nodes: {g['counts']})")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
