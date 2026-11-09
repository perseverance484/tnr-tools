#!/usr/bin/env python3
"""The Salvager's Trade go-live (Friday Nov 13 release). Writes a LIVE manifest; run only on the director's release go.

    python3 push/salvager_golive.gen.py --live DIR   -> push/545_salvager_trade_golive.json

DIR holds fresh live reads taken right before the release (taken through the connector), one file per
record: quest_<id>.json (quests.get) and dungeon_<id>.json (the dungeon read). Every edited field is rebuilt from that
read, so nothing a read did not show is overwritten; the read must be taken after every other Friday step that edits
the same records (the chart go-live 538 touches the Wreck drop rows and the three new runs).

What it does (Salvager's Trade write-up, Claude Doc YNEcUm9oBvYijwTRYWYUAc; Nov 13 plan):
  1. Every win_quest node of every Skyglass run pays Wreck Salvage (number 100): Low Tide and Night Watch 1; the crew
     charts, the three new runs and the six Haul runs 2; the Epic and tainted runs and Crownhold 3.
  2. Each order of The Watch Log: The Rotted Heading pays 3 salvage on claim. Later pages carry it in their own build.
  3. Both Wrecks: a 100% salvage drop (Faded 3, Skyglass 5), and every direct chart drop at half its current chance.
  4. Unhide Wreck Salvage. The four trades become questType overworld with Wreck Sighted as prerequisite and are
     unhidden (folds push/543 in).
Not here: her NPC placement (overworldAi.upsertPlacement isActive true, a direct connector call), the husk and her AI
(profile.updateAi hidden false, by connector: Forge's MCP host cannot save AI records), the Fire and Wreck Sighted
(push/510), The Driftline runs (the early-game thread's own build pays salvage). Do not hand-edit the output.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
import salvager_trade as T  # noqa: E402  (push/salvager_trade.gen.py is imported through a shim below)

SALVAGE = T.SALVAGE
RUNS = {  # quest id: (name, salvage per win)
    "pFQBaJxU_8RSvSi4Kir1Z": ("The Low Tide Run", 1), "dnzL-bDrAEVXrKB5xariu": ("The Night Watch", 1),
    "CgwAVCyZLgNQtEnqgLxxv": ("The Buried Cache", 2), "tpLUAnYVCTyrsdZ5sOssM": ("The Drowned Foundry", 2),
    "-bZ_ZoI6yrUJ_LKT9R5zm": ("The Quarantined Archive", 2), "iUnQO8Fek3yJ-tL4Djv99": ("The Captain's Watch", 2),
    "iQ5tqJaUKSvqbOybqVVDy": ("The Spoiled Hold", 2), "ww_baSsbBet0mx7MK52yI": ("The Rotted Galley", 2),
    "F2eGqpysfQ02E6pXvKqJJ": ("The Glass Nursery", 2),
    "0_wTZMTqvxM-gvl_s1s7c": ("The Trophy Hold", 2), "5y9wAYELSdNa8Jgim1sgD": ("The Overgrown Stores", 2),
    "C1JPScsgSMcVXQUfuFgcs": ("The Ore Vault", 2), "UGHSuhi83C3wRtH3FD4Eu": ("The Bloom Cellar", 2),
    "VjT93rkmWlWlrdG6Pp46e": ("The Snare Room", 2), "vMh6SDID0XTrVJ0f1QmFD": ("The Bone Store", 2),
    "yZoR_dPSdg8ksO77gDH_A": ("The Sealed Reliquary", 3), "H9YInJtnzKCOEMv-sNgzP": ("The Fall", 3),
    "FsuXzvaqr_R25p8cEkxoK": ("The Rotted Reliquary", 3), "ozDN-G6nGFXGgKuPZ04Gr": ("The Burning Heading", 3),
    "fqqpkcp_L4oOsC6yyodlk": ("Crownhold", 3),
}
PAGE = ("V-i3ZcAqPu0hB3G9IEzGo", "The Watch Log: The Rotted Heading", 3)
WRECKS = {"j4QEUtjbK_lbOYUPVoidk": ("Faded Skyglass Wreck", 3), "RHqzYdY4EAQA9HwsBKWDS": ("Skyglass Wreck", 5)}
# The charts she sells, at half their Wreck chance. The Lantern is left to its own pending rate change (Nov 13 plan).
CHARTS = {cid for k, (cid, _) in T.CH.items() if k != "lantern"}


def read(d, kind, rid):
    p = os.path.join(d, f"{kind}_{rid}.json")
    r = json.load(open(p))
    r = r.get("data", r) if isinstance(r, dict) and "data" in r and "id" not in r else r
    assert r.get("id") == rid, (p, r.get("id"))
    return r


def with_salvage(items, n):
    assert not any(SALVAGE in i.get("ids", []) for i in items), "salvage already paid here: the read is stale or 545 ran"
    return list(items) + [T.pay(SALVAGE, n)]


def build(d, chart_ids):
    items = [{"entity": "item", "slot": "edit", "targetId": SALVAGE, "phase": 1, "name": "Wreck Salvage: unhide",
              "data": {"hidden": False}}]
    for qid, (name, n) in RUNS.items():
        q = read(d, "quest", qid)
        assert q["name"] == name, (qid, q["name"])
        content = json.loads(json.dumps(q["content"]))
        wins = [o for o in content["objectives"] if o.get("task") == "win_quest"]
        assert wins, name
        for o in wins:
            o["reward_items"] = with_salvage(o.get("reward_items") or [], n)
        items.append({"entity": "quest", "slot": "edit", "targetId": qid, "phase": 2,
                      "name": f"{name}: {n} salvage on each of {len(wins)} win(s)", "data": {"content": content}})
    pid, pname, n = PAGE
    q = read(d, "quest", pid)
    assert q["name"] == pname
    content = json.loads(json.dumps(q["content"]))
    for o in content["objectives"]:
        o["reward_items"] = with_salvage(o.get("reward_items") or [], n)
    items.append({"entity": "quest", "slot": "edit", "targetId": pid, "phase": 2,
                  "name": f"{pname}: {n} salvage per order", "data": {"content": content}})
    for did, (name, n) in WRECKS.items():
        w = read(d, "dungeon", did)
        assert w["name"] == name
        rewards = json.loads(json.dumps(w["rewards"]))
        halved = 0
        for drop in rewards["drops"]:
            if drop.get("type") == "item" and drop.get("id") in chart_ids:
                drop["chance"] = max(1, round(drop["chance"] / 2, 2)); halved += 1
        assert not any(dr.get("id") == SALVAGE for dr in rewards["drops"]), "salvage already in this Wreck"
        rewards["drops"].append({"type": "item", "id": SALVAGE, "chance": 100, "quantity": n})
        items.append({"entity": "dungeon", "slot": "edit", "targetId": did, "phase": 2,
                      "name": f"{name}: {n} salvage per clear, {halved} chart drops halved", "data": {"rewards": rewards}})
    for t in T.TIERS:
        items.append({"entity": "quest", "slot": "edit", "targetId": T.IDS[t["key"]], "phase": 3,
                      "name": f"{t['name']}: overworld, needs Wreck Sighted, unhide",
                      "data": {"questType": "overworld", "prerequisiteQuestId": T.WRECK_SIGHTED, "hidden": False}})
    out = {"_note": "push/545, LIVE (Friday Nov 13 release only): salvage on every Skyglass win and Rotted Heading order, "
                    "Wreck salvage drops with direct chart drops halved, Wreck Salvage and the four trades unhidden as "
                    f"overworld quests. Built from live reads in {os.path.basename(os.path.normpath(d))}. Generated by "
                    "push/salvager_golive.gen.py; do not hand-edit.", "items": items}
    path = os.path.join(ROOT, "push/545_salvager_trade_golive.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(path, ROOT), len(items))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", required=True)
    ap.add_argument("--chart", action="append", default=[], help="extra chart item ids to halve in the Wrecks")
    a = ap.parse_args()
    build(a.live, CHARTS | set(a.chart))
