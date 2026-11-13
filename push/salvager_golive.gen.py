#!/usr/bin/env python3
"""The Salvager's Trade go-live (Friday Nov 13 release). Writes a LIVE manifest; run only on the director's release go.

    python3 push/salvager_golive.gen.py --live DIR   -> push/545_salvager_trade_golive.json

DIR holds fresh live reads taken right before the release (taken through the connector), one file per
record: quest_<id>.json (quests.get) and dungeon_<id>.json (the dungeon read). Every edited field is rebuilt from that
read, so nothing a read did not show is overwritten; the read must be taken after every other Friday step that edits
the same records (the chart go-live 538 touches the Wreck drop rows and the three new runs).

What it does (Salvager's Trade write-up, Claude Doc YNEcUm9oBvYijwTRYWYUAc; Nov 13 plan):
  1. Every win_quest node of every Skyglass run pays Wreck Salvage, inverted by depth and time (RUL-2026-11-13-148,
     retuned 17:10 UTC at the director's endgame clear times: Faded 90 s, Skyglass 10-15 min, 100 completions a day):
     Low Tide and Night Watch 1 at 25%; the crew charts, the three new runs and the six Haul runs 1; the Epic and
     tainted runs 3; Crownhold 10 (it costs a Lantern to enter). Starting numbers: re-check against measured times.
  2. Each order of The Watch Log: The Rotted Heading pays 3 salvage on claim. Later pages carry it in their own build.
  3. Both Wrecks: a salvage drop (Faded 1 at 50%, Skyglass 3 every clear), and every direct chart drop at half its
     current chance.
  4. Unhide Wreck Salvage. The four trades stay their own quest-log quests, so players choose them (director
     2026-11-13 17:03 UTC: "Keep separate so players can choose"): Wreck Sighted as prerequisite and unhidden; their
     questType is left as it is (not overworld: an NPC tap rolls at random and spends a daily roll).
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
RUNS = {  # quest id: (name, salvage per win, chance %). Every id read back by name with quests.get, Nov 9 16:35Z
    "pFQBaJxU_8RSvSi4Kir1Z": ("The Low Tide Run", 1, 25), "dnzL-bDrAEVXrKB5xariu": ("The Night Watch", 1, 25),
    "CgwAVCyZLgNQtEnqgLxxv": ("The Buried Cache", 1, 100), "UGHSuhi83C3wRtH3FD4Eu": ("The Drowned Foundry", 1, 100),
    "-bZ_ZoI6yrUJ_LKT9R5zm": ("The Quarantined Archive", 1, 100), "liljq0yVXWTSna4X6dZE1": ("The Captain's Watch", 1, 100),
    "iRMyb0WN_ip--EDbvAgLc": ("The Spoiled Hold", 1, 100), "x7ByC_5ssbpibxTB60Ag1": ("The Rotted Galley", 1, 100),
    "F2eGqpysfQ02E6pXvKqJJ": ("The Glass Nursery", 1, 100),
    "0_wTZMTqvxM-gvl_s1s7c": ("The Trophy Hold", 1, 100), "5y9wAYELSdNa8Jgim1sgD": ("The Overgrown Stores", 1, 100),
    "C1JPScsgSMcVXQUfuFgcs": ("The Ore Vault", 1, 100), "UO65dN640MgAbNBBopTVI": ("The Bloom Cellar", 1, 100),
    "vMh6SDID0XTrVJ0f1QmFD": ("The Snare Room", 1, 100), "ww_baSsbBet0mx7MK52yI": ("The Bone Store", 1, 100),
    "yZoR_dPSdg8ksO77gDH_A": ("The Sealed Reliquary", 3, 100), "H9YInJtnzKCOEMv-sNgzP": ("The Fall", 3, 100),
    "FsuXzvaqr_R25p8cEkxoK": ("The Rotted Reliquary", 3, 100), "ozDN-G6nGFXGgKuPZ04Gr": ("The Burning Heading", 3, 100),
    "fqqpkcp_L4oOsC6yyodlk": ("Crownhold", 10, 100),
}
PAGE = ("V-i3ZcAqPu0hB3G9IEzGo", "The Watch Log: The Rotted Heading", 3)
WRECKS = {"j4QEUtjbK_lbOYUPVoidk": ("Faded Skyglass Wreck", 1, 50), "RHqzYdY4EAQA9HwsBKWDS": ("Skyglass Wreck", 3, 100)}
# The charts she sells, at half their Wreck chance. The Lantern is left to its own pending rate change (Nov 13 plan).
CHARTS = {cid for k, (cid, _) in T.CH.items() if k != "lantern"}


def read(d, kind, rid):
    p = os.path.join(d, f"{kind}_{rid}.json")
    r = json.load(open(p))
    r = r.get("data", r) if isinstance(r, dict) and "data" in r and "id" not in r else r
    assert r.get("id") == rid, (p, r.get("id"))
    return r


def with_salvage(items, n, chance=100):
    assert not any(SALVAGE in i.get("ids", []) for i in items), "salvage already paid here: the read is stale or 545 ran"
    row = T.pay(SALVAGE, n)
    row["number"] = chance  # a reward row's number is its chance in percent
    return list(items) + [row]


def build(d, chart_ids):
    items = [{"entity": "item", "slot": "edit", "targetId": SALVAGE, "phase": 1, "name": "Wreck Salvage: unhide",
              "data": {"hidden": False}}]
    for qid, (name, n, chance) in RUNS.items():
        q = read(d, "quest", qid)
        assert q["name"] == name, (qid, q["name"])
        content = json.loads(json.dumps(q["content"]))
        wins = [o for o in content["objectives"] if o.get("task") == "win_quest"]
        assert wins, name
        for o in wins:
            o["reward_items"] = with_salvage(o.get("reward_items") or [], n, chance)
        odds = "" if chance == 100 else f" at {chance}%"
        items.append({"entity": "quest", "slot": "edit", "targetId": qid, "phase": 2,
                      "name": f"{name}: {n} salvage{odds} on each of {len(wins)} win(s)", "data": {"content": content}})
    pid, pname, n = PAGE
    q = read(d, "quest", pid)
    assert q["name"] == pname
    content = json.loads(json.dumps(q["content"]))
    for o in content["objectives"]:
        o["reward_items"] = with_salvage(o.get("reward_items") or [], n)
    items.append({"entity": "quest", "slot": "edit", "targetId": pid, "phase": 2,
                  "name": f"{pname}: {n} salvage per order", "data": {"content": content}})
    for did, (name, n, chance) in WRECKS.items():
        w = read(d, "dungeon", did)
        assert w["name"] == name
        rewards = json.loads(json.dumps(w["rewards"]))
        halved = 0
        for drop in rewards["drops"]:
            if drop.get("type") == "item" and drop.get("id") in chart_ids:
                drop["chance"] = max(1, round(drop["chance"] / 2, 2)); halved += 1
        assert not any(dr.get("id") == SALVAGE for dr in rewards["drops"]), "salvage already in this Wreck"
        rewards["drops"].append({"type": "item", "id": SALVAGE, "chance": chance, "quantity": n})
        odds = "" if chance == 100 else f" at {chance}%"
        items.append({"entity": "dungeon", "slot": "edit", "targetId": did, "phase": 2,
                      "name": f"{name}: {n} salvage{odds} per clear, {halved} chart drops halved", "data": {"rewards": rewards}})
    for t in T.TIERS:
        items.append({"entity": "quest", "slot": "edit", "targetId": T.IDS[t["key"]], "phase": 3,
                      "name": f"{t['name']}: quest log (player's choice), needs Wreck Sighted, unhide",
                      "data": {"prerequisiteQuestId": T.WRECK_SIGHTED, "hidden": False}})
    out = {"_note": "push/545, LIVE (Friday Nov 13 release only): salvage on every Skyglass win and Rotted Heading order, "
                    "Wreck salvage drops with direct chart drops halved, Wreck Salvage and the four trades unhidden as "
                    f"their own quest-log quests. Built from live reads in {os.path.basename(os.path.normpath(d))}. Generated by "
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
