#!/usr/bin/env python3
"""RUL-2026-10-14-001 transform of state/silent_bastion_phase1_graph.json (r1 -> r2).

Per lane (n, r) of every division:
- the two route-specific fourth fights (f4.medical / f4.combat) and their gate dialogs become ONE
  fourth fight `b{d}.{lane}.f4` gated by `d{d}.{lane}.f4`;
- the fourth fight's win goes to a protocol dialog `d{d}.{lane}.protocol` whose options route
  directly to the Medical and Combat commander battle nodes (same commander);
- the per-protocol commander gate dialogs (boss.medical / boss.combat) are removed: the protocol
  dialog is their gate;
- Medical commander battles set pools to 100% (full heal) instead of 75%.
Node order puts the fourth fight before the commander battles. Maintenance is unchanged.

  python3 harness/silent_bastion_phase1/tools/restructure_protocol_choice.py [--check]
"""
import json, os, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
PATH = os.path.join(REPO, "state/silent_bastion_phase1_graph.json")


def transform(g: dict) -> dict:
    if g.get("revision") == "r2":
        return g
    old = {n["id"]: n for n in g["nodes"]}
    out = []
    for n in g["nodes"]:
        i = n["id"]
        parts = i.split(".")
        protocol_boss = len(parts) == 4 and parts[2] == "boss" and parts[3] in ("medical", "combat")
        if (len(parts) >= 3 and parts[2] == "f4") or protocol_boss:
            continue  # fourth fights, Medical/Combat gates and battles are re-emitted below
        if n["kind"] == "dialog" and i.endswith(".terminal"):
            d, lane = n["division"], n["lane"]
            out.append({**n, "choices": [
                {"label": "Maintenance Passage", "to": f"d{d}.{lane}.puzzle"},
                {"label": "Protocol access (fight the fourth enemy)", "to": f"d{d}.{lane}.f4"},
            ]})
            continue
        out.append(n)
        if n["kind"] == "battle" and parts[2] == "boss" and parts[3] == "alert":
            d, lane = int(parts[0][1:]), parts[1]
            src4 = old[f"b{d}.{lane}.f4.medical"]
            med, com = old[f"b{d}.{lane}.boss.medical"], old[f"b{d}.{lane}.boss.combat"]
            out += [
                {"id": f"d{d}.{lane}.f4", "kind": "dialog", "next": f"b{d}.{lane}.f4", "division": d, "lane": lane, "regular": 4},
                {"id": f"b{d}.{lane}.f4", "kind": "battle", "encounterSlot": src4["encounterSlot"],
                 "onWin": f"d{d}.{lane}.protocol", "onLoss": src4["onLoss"]},
                {"id": f"d{d}.{lane}.protocol", "kind": "dialog", "division": d, "lane": lane,
                 "commander": old[f"d{d}.{lane}.boss.medical"]["commander"],
                 "choices": [{"label": "Medical Protocol", "to": med["id"]}, {"label": "Combat Protocol", "to": com["id"]}]},
                {**med, "startPoolsPercent": 100},
                com,
            ]
    g = {**g, "revision": "r2", "nodes": out}
    g["status"] = "PHASE_1_R2_DIRECTOR_RESTRUCTURE_NATIVE_TESTED_OFFLINE"
    g["specialFields"] = {
        **g["specialFields"],
        "startPoolsPercent": "Symbolic stand-in for start_battle.givePools; only retry first fight=50 and Medical commander=100 (full heal)",
    }
    g["revisionNote"] = ("r2 per RUL-2026-10-14-001: one fourth fight per lane; the protocol is chosen by the dialog after it, "
                         "which routes directly to the Medical (givePools 100) or Combat commander battle node.")
    return g


def main() -> int:
    src = json.load(open(PATH))
    new = transform(src)
    text = json.dumps(new, indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        ok = src.get("revision") == "r2" and json.dumps(transform(src)) == json.dumps(src)
        print("graph r2 current" if ok else "graph not r2"); return 0 if ok else 1
    open(PATH, "w").write(text)
    print(f"wrote r2: {len(new['nodes'])} nodes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
