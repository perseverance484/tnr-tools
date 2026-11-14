#!/usr/bin/env python3
"""The Salvager's Trade go-live (Friday Nov 13 release). Writes a LIVE manifest; run only on the director's release go.

    python3 push/salvager_golive.gen.py --live DIR   -> push/545_salvager_trade_golive.json

DIR holds fresh live reads taken right before the release (taken through the connector), one file per
record: quest_<id>.json (quests.get), dungeon_<id>.json (the dungeon read) and item_B48dTRsoLJGKBWIUbeUoG.json
(item.get of the Archive Chart Case). Every edited field is rebuilt from that
read, so nothing a read did not show is overwritten; the read must be taken after every other Friday step that edits
the same records (the chart go-live 538 touches the Wreck drop rows and the three new runs).

What it does (Salvager's Trade write-up, Claude Doc YNEcUm9oBvYijwTRYWYUAc; Nov 13 plan):
  1. Every win_quest node of every Skyglass run pays Wreck Salvage, inverted by depth and time (RUL-2026-11-13-148,
     retuned 17:10 UTC at the director's endgame clear times: Faded 90 s, Skyglass 10-15 min, 100 completions a day):
     Low Tide and Night Watch 1 at 25%; the crew charts, the three new runs and the six Haul runs 1; the Epic and
     tainted runs 3; Crownhold 10 (it costs a Lantern to enter). Starting numbers: re-check against measured times.
  2. Each order of The Watch Log: The Rotted Heading pays 3 salvage on claim. Later pages carry it in their own build.
  3. Both Wrecks: a salvage drop (Faded 1 at 25%, Skyglass 3 every clear), and every direct chart drop at half its
     current chance.
  5. The Lantern trade sells once per record (retryDelay none, maxCompletes 1); the Friday routine creates a fresh copy
     each week and hides the last (director 2026-11-13: "1 lantern per", since the game week turns Sunday 6 PM).
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
RUNS = {  # quest id: (name, salvage per win, chance %). Ladder by entry-chart rarity, director 2026-11-13 21:25Z
    # "1 in 4, 1, 3, 5 and haul pages change to epic rarity": common 1 at 25%, rare 1, epic 3, legendary 5, Crownhold 10. Every id read back by name with quests.get, Nov 9 16:35Z
    "pFQBaJxU_8RSvSi4Kir1Z": ("The Low Tide Run", 1, 25), "dnzL-bDrAEVXrKB5xariu": ("The Night Watch", 1, 25),
    "CgwAVCyZLgNQtEnqgLxxv": ("The Buried Cache", 1, 100), "UGHSuhi83C3wRtH3FD4Eu": ("The Drowned Foundry", 1, 100),
    "-bZ_ZoI6yrUJ_LKT9R5zm": ("The Quarantined Archive", 1, 100), "liljq0yVXWTSna4X6dZE1": ("The Captain's Watch", 1, 100),
    "iRMyb0WN_ip--EDbvAgLc": ("The Spoiled Hold", 1, 100), "x7ByC_5ssbpibxTB60Ag1": ("The Rotted Galley", 1, 25),
    "F2eGqpysfQ02E6pXvKqJJ": ("The Glass Nursery", 3, 100),
    "0_wTZMTqvxM-gvl_s1s7c": ("The Trophy Hold", 3, 100), "5y9wAYELSdNa8Jgim1sgD": ("The Overgrown Stores", 3, 100),
    "C1JPScsgSMcVXQUfuFgcs": ("The Ore Vault", 3, 100), "UO65dN640MgAbNBBopTVI": ("The Bloom Cellar", 3, 100),
    "vMh6SDID0XTrVJ0f1QmFD": ("The Snare Room", 3, 100), "ww_baSsbBet0mx7MK52yI": ("The Bone Store", 3, 100),
    "yZoR_dPSdg8ksO77gDH_A": ("The Sealed Reliquary", 3, 100), "H9YInJtnzKCOEMv-sNgzP": ("The Fall", 3, 100),
    "FsuXzvaqr_R25p8cEkxoK": ("The Rotted Reliquary", 5, 100), "ozDN-G6nGFXGgKuPZ04Gr": ("The Burning Heading", 5, 100),
    "fqqpkcp_L4oOsC6yyodlk": ("Crownhold", 10, 100),
    "pCFFWT8ZNDMfXCrvR-0hk": ("The Drowned Cradle", 5, 100),  # director Nov 13 20:10Z "Yes, 3" (unhidden by 599)
}
# Director 2026-11-13 21:25Z: the six Haul pages move from legendary to epic (they pay the epic 3 above).
HAUL_PAGES = {"JvrytTOdR1voVCoo3fckK": "Ledger Page: The Trophy Hold", "nLG6TK48xlyZ_t9R28QsY": "Stores Manifest: The Overgrown Stores",
              "9j4IErGW1gmZ-5FNjZMEQ": "Stores Manifest: The Ore Vault", "7Sz2ttMScKH8b10XYS12I": "Stores Manifest: The Bloom Cellar",
              "6QgcnW0v6gZeHY474BjR0": "Ledger Page: The Snare Room", "uu6ETQimuBJ69jwr76IIi": "Ledger Page: The Bone Store"}
# The two chart runs already pay salvage (2 each, push D1a/early-game build); the ladder resets them. Split Hold's chart
# is common (1 at 25%), Broken Stern's is rare (1).
RESET = {"ktVUByCZUfREmWYsvPtzQ": ("The Split Hold", 1, 25), "BDUY4nScGzYiZoHGkmkxP": ("The Broken Stern", 1, 100)}
# Chart loop fix (director 2026-11-13 21:40Z, "If archive is in remove it, and we can add chart cases to watch log rewards
# and archive rewards"): no end-of-run choice offers a chart or an Archive Chart Case, except the Quarantined Archive,
# which keeps the case; the case no longer holds the Archive's own chart; four drops trimmed. Salvage and trade prices
# unchanged. Chain growth after the fix 0.44 (every chart chain ends; Archive self-return ~0.19 per run).
CASE = "B48dTRsoLJGKBWIUbeUoG"
ARCHIVE = "-bZ_ZoI6yrUJ_LKT9R5zm"
CHART_ITEMS = {cid for cid, _ in T.CH.values()} | set(HAUL_PAGES) | {
    "I09yVwwnSQK8YE2vkdl1l",  # Chart of the Split Hold
    "KR5-rVmqtAWeMzpE52aE7",  # Chart of the Broken Stern
    "oQcPHpr0sqmWHfaJPR4T_",  # Chart of the Drowned Cradle
    "2sGi5SZXh2UutHmM-mIMD",  # Rotted Reliquary Seal (read back by name Nov 13 21:50Z)
    "U2yJbBM6_N1xBBf0ez96F",  # The Rotted Heading (read back by name Nov 13 21:50Z)
}
TRIMS = {  # quest id: {item id: {live chance: new chance}} on every win node; a chance not in the map fails the build
    ARCHIVE: {"sVqDdYUJIxxRYbmKbbxo0": {25: 15}},                                          # Reliquary Seal
    "liljq0yVXWTSna4X6dZE1": {"s1mYHuKqw2YuzIzxVwU-_": {25: 10, 45: 20}},                  # Captain's Watch: Last Heading
    "iRMyb0WN_ip--EDbvAgLc": {"U2yJbBM6_N1xBBf0ez96F": {10: 5}, "2sGi5SZXh2UutHmM-mIMD": {10: 5}},  # Spoiled Hold
    "fqqpkcp_L4oOsC6yyodlk": {"sVqDdYUJIxxRYbmKbbxo0": {25: 10}, "s1mYHuKqw2YuzIzxVwU-_": {25: 10}},  # Crownhold
}
# Director Nov 13: the "Driftline" name is scrapped everywhere players see it. The three bosses are renamed by the
# Driftline hidden build (DL1); their names inside the two chart runs' text are swapped here, on the same fresh read.
RENAMES = [("Driftline Wayfinder", "Shoal Wayfinder"), ("Driftline Core Horror", "Shoal Core Horror"),
           ("Driftline Captain", "Stern Captain")]


def renamed(text):
    for a, b in RENAMES:
        text = text.replace(a, b)
    return text


CASE_DESC = ('<i>A sealed chart case from the Quarantined Archive, holding one chart of the wreck\'s shifting decks.</i><br><br>'
             '<b>Each roll:</b><br><span style="color:#9ca3af">\u25c6</span> <b>Common 55%</b> \u00b7 Chart of the Drowned Foundry<br>'
             '<span style="color:#3b82f6">\u25c6</span> <b>Rare 35%</b> \u00b7 Chart of the Captain\'s Watch<br>'
             '<span style="color:#f59e0b">\u25c6</span> <b>Legendary 7%</b> \u00b7 Reliquary Seal or The Last Heading <i>(3.5% each)</i><br>'
             '<span style="color:#ef4444">\u25c6</span> <b>Forbidden 3%</b> \u00b7 Lastlight Lantern')
CASE_TIERS = [("Common", ["pY-0O5Gs2n89pf0kYb5J2"], 5500), ("Rare", ["aHFNuo5RkKpDcaOBLIKiu"], 3500),
              ("Legendary", ["sVqDdYUJIxxRYbmKbbxo0", "s1mYHuKqw2YuzIzxVwU-_"], 700), ("Forbidden", ["jCJv4N3JSiihuqnK0jJ7t"], 300)]


def chain_fix(qid, name, content):
    """Strip chart picks from the end-of-run choice and apply drop trims. Returns a short note for the item name."""
    notes = []
    rw = content.get("reward") or {}
    rows = rw.get("reward_items") or []
    keep_case = qid == ARCHIVE
    drop = lambda r: any(i in CHART_ITEMS or (i == CASE and not keep_case) for i in r.get("ids", []))
    kept = [r for r in rows if not drop(r)]
    if len(kept) != len(rows):
        if content.get("rewardMode") == "choose":
            assert len(kept) >= int(content.get("rewardPickCount") or 1), (name, "too few choices left")
        rw["reward_items"] = kept
        notes.append(f"{len(rows) - len(kept)} chart pick(s) removed")
    if keep_case:
        assert any(CASE in r.get("ids", []) for r in kept), "Archive no longer offers the case: read is stale"
    for iid, m in TRIMS.get(qid, {}).items():
        hit = 0
        for o in content["objectives"]:
            if o.get("task") != "win_quest":
                continue
            for r in o.get("reward_items") or []:
                if iid in r.get("ids", []):
                    assert r["number"] in m, (name, iid, r["number"], "chance not as read Nov 13 21:50Z")
                    r["number"] = m[r["number"]]; hit += 1
        assert hit, (name, iid, "trim found nothing")
        notes.append(f"{iid[:5]} trimmed x{hit}")
    return ", ".join(notes)


def case_edit(d):
    it = read(d, "item", CASE)
    assert it["name"] == "Archive Chart Case"
    effects = json.loads(json.dumps(it["effects"]))
    wc = [e for e in effects if e.get("weightedCache")]
    assert len(wc) == 1
    tiers = [{"name": n, "entries": [{"items": [{"itemId": i, "quantity": 1}]} for i in ids], "probability": p}
             for n, ids, p in CASE_TIERS]
    assert sum(t["probability"] for t in tiers) == 10000
    wc[0]["weightedCache"]["tiers"] = tiers
    return {"entity": "item", "slot": "edit", "targetId": CASE, "phase": 1,
            "name": "Archive Chart Case: Archive chart removed (Foundry 55, Watch 35, Seal/Heading 7, Lantern 3)",
            "data": {"description": CASE_DESC, "effects": effects}}


PAGE = ("V-i3ZcAqPu0hB3G9IEzGo", "The Watch Log: The Rotted Heading", 3)
WRECKS = {"j4QEUtjbK_lbOYUPVoidk": ("Faded Skyglass Wreck", 1, 25), "RHqzYdY4EAQA9HwsBKWDS": ("Skyglass Wreck", 3, 100)}
# The charts she sells, at half their Wreck chance. The Lantern is left to its own pending rate change (Nov 13 plan).
CHARTS = {cid for k, (cid, _) in T.CH.items() if k != "lantern"}
# Charts first added to the Wrecks by 538 (Nov 13) already carry their final rates (Faded: Rotted Galley 10%; Skyglass:
# Spoiled 6, Rotted Galley 5, Nursery 3), so they are not halved again.
NEW_538 = {T.CH[k][0] for k in ("spoiled", "galley", "nursery")}
# Chart of the Closing Hold (the Mender's entry, 599): 5% on every ending of The Spoiled Hold (director's Mender source,
# relayed Nov 13 19:58Z; the Skyglass Wreck's 2% row is 538 --closing-hold-drops).
CLOSING = "oQcPHpr0sqmWHfaJPR4T_"
SPOILED_HOLD = "iRMyb0WN_ip--EDbvAgLc"


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
            if qid == SPOILED_HOLD:
                assert not any(CLOSING in i.get("ids", []) for i in o["reward_items"]), "Drowned Cradle chart already here"
                row = T.pay(CLOSING, 1); row["number"] = 5
                o["reward_items"].append(row)
        fix = chain_fix(qid, name, content)
        odds = "" if chance == 100 else f" at {chance}%"
        items.append({"entity": "quest", "slot": "edit", "targetId": qid, "phase": 2,
                      "name": f"{name}: {n} salvage{odds} on each of {len(wins)} win(s)" + (f"; {fix}" if fix else ""),
                      "data": {"content": content}})
    items.append(case_edit(d))
    for iid, iname in HAUL_PAGES.items():
        items.append({"entity": "item", "slot": "edit", "targetId": iid, "phase": 1,
                      "name": f"{iname}: rarity EPIC (was LEGENDARY)", "data": {"rarity": "EPIC"}})
    for qid, (name, n, chance) in RESET.items():
        q = read(d, "quest", qid)
        assert q["name"] == name, (qid, q["name"])
        content = json.loads(renamed(json.dumps(q["content"], ensure_ascii=False)))
        assert "Driftline" not in json.dumps(content), (name, "Driftline still named in content")
        top = {k: renamed(q[k]) for k in ("description", "successDescription") if q.get(k) and renamed(q[k]) != q[k]}
        assert not any("Driftline" in v for v in top.values()), (name, "Driftline still named")
        wins = [o for o in content["objectives"] if o.get("task") == "win_quest"]
        assert wins, name
        for o in wins:
            rows = [i for i in (o.get("reward_items") or []) if SALVAGE in i.get("ids", [])]
            assert len(rows) == 1, (name, o["id"], rows)
            rows[0]["quantity"] = n
            rows[0]["number"] = chance
        fix = chain_fix(qid, name, content)
        odds = "" if chance == 100 else f" at {chance}%"
        items.append({"entity": "quest", "slot": "edit", "targetId": qid, "phase": 2,
                      "name": f"{name}: salvage reset to {n}{odds} on each of {len(wins)} win(s)" + (f"; {fix}" if fix else "")
                              + "; Shoal/Stern boss names",
                      "data": dict(top, content=content)})
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
            if drop.get("type") == "item" and drop.get("id") in chart_ids and drop.get("id") not in NEW_538:
                drop["chance"] = max(1, round(drop["chance"] / 2, 2)); halved += 1
        assert not any(dr.get("id") == SALVAGE for dr in rewards["drops"]), "salvage already in this Wreck"
        rewards["drops"].append({"type": "item", "id": SALVAGE, "chance": chance, "quantity": n})
        odds = "" if chance == 100 else f" at {chance}%"
        items.append({"entity": "dungeon", "slot": "edit", "targetId": did, "phase": 2,
                      "name": f"{name}: {n} salvage{odds} per clear, {halved} chart drops halved", "data": {"rewards": rewards}})
    for t in T.TIERS:
        # name: the Nov 13 clones were made as "<name> - copy" (quests.clone); the release edit sets the real name.
        # questRank D: the Administration Building lists event quests only at the player's letter ranks (Genin D-C,
        # Chunin D-B; queries/quests.ts fetchQuestDiscoveryCandidates ranks filter), so D leaves only the level gates
        # (director Nov 13 20:10Z "No rank gates, just level gates").
        # No key quest (director Nov 13 20:12Z: "they dont need a key as the cost gates them, availability to all is fine").
        data = {"name": t["name"], "prerequisiteQuestId": None, "hidden": False, "questRank": "D"}
        extra = ""
        if t["key"] == "lantern":
            # One Lantern per weekend (director 2026-11-13 "1 lantern per"): the game week turns over Sunday 6 PM,
            # mid-event, so a weekly limit would sell two. This record sells once, ever; each Friday a fresh copy
            # replaces it (queue job 595, from Nov 20) and the old one is hidden.
            data.update({"retryDelay": "none", "maxCompletes": 1})
            extra = ", once per record (re-issued each Friday)"
        items.append({"entity": "quest", "slot": "edit", "targetId": T.IDS[t["key"]], "phase": 3,
                      "name": f"{t['name']}: quest log (player's choice), no key, rank D, unhide{extra}",
                      "data": data})
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
