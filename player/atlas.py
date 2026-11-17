"""The move atlas (brief, AP4 step 0): one card for every action a player can use against us or that we can use,
compiled from the catalog and measured in the game's own combat code. Generated; never edited by hand.

    python3 -m player.atlas build       make player/atlas.json again (needs the engine app, harness/pvp_turn/README.md)
    python3 -m player.atlas check       every card is of the catalog's record as it is now; with the engine, the
                                        atlas is made again and must come out the same
    python3 -m player.atlas coverage    the actions of the logged fights that have no card

A card is what the engine did when the standard caster fired that action alone on a fresh board: both at full
health and next to each other in round 1, the caster with capped stats and the endgame gear the director assumes
(full Kaeruun, Subaku's mask), the jutsu at level 25, against my own profile and gear. For every card the caster is
built again with that card for his whole kit and what the engine asks for before it lists it: its bloodline, the
elements it is of, a weapon of the kind it is cast with, the item its bloodline requires. A jutsu or item that is
for PvE only has a card that says so and is not fired.

    name, kind (jutsu | item | basic), type, rank, bloodline, weapon     from the record
    of        a mark of that record: the card is stale when the catalog's record no longer has it
    ap, cooldown, range, target, method                                  from the record
    tags      the record's effect types, in order (what it is meant to do, also where a fresh board shows nothing:
              a heal at full health, a Clear with nothing to clear)
    cost      the action points the engine asks for it
    legal     whether the engine let the standard caster fire it; else `reason`
    now       what it took off (-) or gave (+) the caster and the target at once
    effects   every effect it left on either of them: type, on, by, power, powerPerLevel, level, rounds,
              calculation, and whether it only counts from the next round (castThisRound)
    ground    every ground effect, with its tile on the standard board (caster 6,4; target 7,4)
    at        where both stand afterwards
    next      one idle round on: what ticked, and each effect's rounds left
    mine      for the actions of my own kit: cost, now, effects and ground again, fired by me as I am (my stats,
              gear and bloodline) at the standard opponent

What is not on a card yet: what Clear, Cleanse, a seal and the prevents do to each effect, and a second measure
with the caster hurt (heals). The damage is the standard matchup's; fight_bases.py rescales it for a fight.
"""
import concurrent.futures
import hashlib
import json
import os
import re
import sys

from . import config as C

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas.json")
BASICS = ("basicAttack", "basicHeal", "clear", "cleanse", "defensiveStance", "offensiveStance",
          "replacementTechnique", "meditate")
NOT_PLAYERS = ("AI", "PETS")                     # jutsu types no player casts
HELD = ("HAND", "ITEM", "THROWN")                # the slots an item is used from in a fight
PVE_ONLY = "for PvE only"
NOISE = ("visual",)                              # effects that are only pictures
LEVEL, BATCH, WORKERS = 25, 60, 4
FAULT = re.compile(r"is not a function|is undefined|Cannot find|SyntaxError")   # the engine's own code failing
EFFECT = ("type", "on", "by", "power", "powerPerLevel", "level", "rounds", "calculation", "castThisRound", "direction",
          "elements", "statTypes", "generalTypes", "poolsAffected", "x", "y")


def _tools():
    if C.TOOLS not in sys.path:
        sys.path.insert(0, C.TOOLS)
    import engine_bridge
    import value_model
    return engine_bridge, value_model


def candidates(recs):
    """[(id, kind)] of the records that can be a player's action, then the basics everyone has."""
    out = []
    for rid in sorted(recs):
        rec, kind = recs[rid]["record"], recs[rid].get("kind")
        if kind == "jutsu" and rec.get("jutsuType") not in NOT_PLAYERS:
            out.append((rid, "jutsu"))
        elif kind == "item" and rec.get("slot") in HELD and rec.get("effects"):
            out.append((rid, "item"))
    return out + [(b, "basic") for b in BASICS]


def _request(EB, VM):
    full = {"curHealth": 5050, "maxHealth": 5050, "perm": []}
    req = EB._replay_request([], C.ME, "user_atlas", dict(full), dict(full, userId="user_atlas"), (7, 4), (6, 4), 1,
                             "same", VM.load_cal())
    req["mode"], req["log"] = "cards", []
    return req


def _needs(rec, recs, gear):
    """What the standard caster must have for the engine to list this card: the card itself, the elements it is
    of, a weapon of the kind the jutsu is cast with, and the item its bloodline asks for."""
    kit = [{"record": rec, "kind": "jutsu" if "jutsuType" in rec else "item", "level": LEVEL}]
    worn = list(gear)
    if rec.get("jutsuWeapon") not in (None, "NONE"):
        held = sorted(r for r, v in recs.items() if v["record"].get("weaponType") == rec["jutsuWeapon"]
                      and v["record"].get("slot") == "HAND")
        if held:
            kit.append({"record": recs[held[0]]["record"], "kind": "item", "level": LEVEL})
    asked = (recs.get(rec.get("requiredBloodlineItemId")) or {}).get("record")
    if asked and asked.get("slot") in HELD:
        kit.append({"record": asked, "kind": "item", "level": LEVEL})
    elif asked:
        worn = [g for g in worn if g.get("slot") != asked.get("slot")] + [{"record": asked, "slot": asked.get("slot")}]
    of = [rec.get("elementClassification")] + [x for e in rec.get("effects") or [] for x in e.get("elements") or []]
    return {"kit": kit, "gear": worn, "elements": [x for x in dict.fromkeys(of) if x and x != "None"]}


def measure(ids, recs, timeout=600):
    """{id: what the engine read back} for these cards, in batches, a few engine processes at a time."""
    EB, VM = _tools()
    gear = _request(EB, VM)["him"].get("gear") or []

    def side(rid):
        rec = (recs.get(rid) or {}).get("record")
        if not rec:                                                   # a basic: nothing in his kit is needed
            return {"kit": [], "bloodline": None, "gear": gear, "elements": []}
        return dict(_needs(rec, recs, gear),
                    bloodline=EB._bloodline(rec["bloodlineId"]) if rec.get("bloodlineId") else None)

    def run(batch):
        req = _request(EB, VM)
        req["cards"] = [{"id": rid[3:], "by": "me"} if rid.startswith("me:") else {"id": rid, "side": side(rid)}
                        for rid in batch]
        return (EB._run(req, timeout) or {}).get("cards")
    # my own kit a second time, fired by me as I am at the standard opponent ("me:<id>"): the request's "me" side
    mine = ["me:" + k["record"]["id"] for k in _request(EB, VM)["me"]["kit"]] + ["me:" + b for b in BASICS]
    ids = list(ids) + [m for m in mine if m[3:] in ids]
    batches = [ids[i:i + BATCH] for i in range(0, len(ids), BATCH)]
    out, lost = {}, []
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for batch, got in zip(batches, pool.map(run, batches)):
            out.update(got or {})
            lost += [] if got else [batch]
    for batch in lost:                    # a loaded machine can lose an engine process: once more, one at a time
        got = run(batch)
        if not got:
            raise SystemExit(f"the engine gave no answer for a batch of {len(batch)} cards, twice: nothing is written")
        out.update(got)
    return out


def _effect(e):
    return {k: e[k] for k in EFFECT if e.get(k) is not None and e.get(k) != []}


def _of_record(rid, kind, rec):
    """The part of a card that is the record's own."""
    out = {"name": (rec or {}).get("name") or rid, "kind": kind, "of": mark(rec)}
    rec = rec or {}
    for key, field in (("type", "jutsuType" if kind == "jutsu" else "itemType"), ("rank", "jutsuRank"),
                       ("bloodline", "bloodlineId"), ("weapon", "jutsuWeapon"), ("ap", "actionCostPerc"),
                       ("cooldown", "cooldown"), ("range", "range"), ("target", "target"), ("method", "method")):
        if rec.get(field) not in (None, "", "NONE"):
            out[key] = rec[field]
    out["tags"] = [e.get("type") for e in rec.get("effects") or [] if e.get("type") not in NOISE]
    return out


def _read_back(m):
    """What the engine read back of a card that was fired, without the effects that are only pictures."""
    clean = lambda rows: [_effect(e) for e in rows if e["type"] not in NOISE]
    return {"now": m["now"], "effects": clean(m["effects"]), "ground": clean(m["ground"])}


def card(rid, kind, rec, m, mine=None):
    """One card: the record's own fields, then what the engine read back (m; None when it gave no answer). mine:
    the same read back with me for the caster, for the actions of my own kit."""
    out = _of_record(rid, kind, rec)
    if (rec or {}).get("battleUsageType") == "PVE":
        return dict(out, legal=False, reason=PVE_ONLY)
    if m is None:
        return dict(out, legal=False, reason="the engine gave no answer")
    out["legal"] = bool(m.get("legal"))
    if m.get("cost") is not None:
        out["cost"] = m["cost"]
    if not out["legal"]:
        return dict(out, reason=("not an action in a fight" if not m.get("listed") else m.get("reason") or "refused"))
    out.update(_read_back(m), at=m["at"],
               next={"caster": m["next"]["caster"], "target": m["next"]["target"],
                     "left": [x for x in m["next"]["left"] if x[0] not in NOISE]})
    if mine and mine.get("legal"):
        out["mine"] = dict(_read_back(mine), cost=mine.get("cost"))
    return out


def mark(rec):
    """A short mark of the record a card was made of: a card is stale when its record's mark has changed."""
    return hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:12] if rec else None


def _pin(EB):
    try:
        with open(os.path.join(os.path.dirname(EB.engine_app()), "PIN"), encoding="utf8") as f:
            return f.read().strip()
    except (OSError, TypeError):
        return None


def build():
    """The atlas, made from the catalog and the engine: {"_meta": ..., "cards": {id: card}}."""
    EB, _ = _tools()
    if not EB.engine_app():
        raise SystemExit("no engine app on this machine: harness/pvp_turn/README.md, \"Engine version\"")
    recs = EB._records()
    ids = candidates(recs)
    got = measure([rid for rid, _ in ids if (recs.get(rid) or {}).get("record", {}).get("battleUsageType") != "PVE"],
                  recs)
    broken = sorted(rid for rid, m in got.items() if FAULT.search(str(m.get("reason") or "")))
    if broken:                              # not a card's own refusal: the engine's code did not load or run
        raise SystemExit(f"the engine failed on {len(broken)} card(s) ({got[broken[0]]['reason'][:90]}): nothing is "
                         "written")
    cards = {rid: card(rid, kind, (recs.get(rid) or {}).get("record"), got.get(rid), got.get("me:" + rid))
             for rid, kind in ids}
    legal = [c for c in cards.values() if c["legal"]]
    meta = {"engine": _pin(EB), "catalog_records": len(recs), "level": LEVEL,
            "board": {"caster": [6, 4], "target": [7, 4], "health": 5050},
            "cards": len(cards), "legal": len(legal), "mine": sum(1 for c in cards.values() if "mine" in c),
            "effect_types": sorted({e["type"] for c in legal for e in c["effects"] + c["ground"]})}
    return {"_meta": meta, "cards": cards}


def write(atlas, path=PATH):
    """One card a line, in id order, so that a changed card is one changed line."""
    with open(path, "w", encoding="utf8") as f:
        f.write('{"_meta": ' + json.dumps(atlas["_meta"], sort_keys=True) + ',\n"cards": {\n')
        rows = [json.dumps(rid) + ": " + json.dumps(c, sort_keys=True, ensure_ascii=False)
                for rid, c in sorted(atlas["cards"].items())]
        f.write(",\n".join(rows) + "\n}}\n")


def load(path=PATH):
    with open(path, encoding="utf8") as f:
        return json.load(f)


def stale(kept, recs):
    """What the catalog has that the atlas was not made of: {"changed": ids whose record is not the one the card
    was made of, "new": records that would be cards and have none, "gone": cards whose record is no more}. Other
    records come and go with every harvest and do not touch the atlas."""
    cards, now = kept["cards"], dict(candidates(recs))
    return {"changed": sorted(r for r in now if r in cards and cards[r].get("of") != mark((recs.get(r) or {}).get("record"))),
            "new": sorted(r for r in now if r not in cards), "gone": sorted(r for r in cards if r not in now)}


def check():
    """([what is wrong with the committed atlas], a note). Without the engine: only whether its cards are of the
    catalog's records as they are now."""
    EB, _ = _tools()
    kept = load()
    wrong = [f"{len(ids)} card(s) {what}: {', '.join(ids[:8])}" for what, ids in (
        ("are of a record that has changed", stale(kept, EB._records())["changed"]),
        ("are missing for records the catalog has", stale(kept, EB._records())["new"]),
        ("are of records the catalog no longer has", stale(kept, EB._records())["gone"])) if ids]
    if not EB.engine_app():
        return wrong, "no engine app here: not made again"
    if kept["_meta"]["engine"] != _pin(EB):
        wrong.append(f"made with the engine at {kept['_meta']['engine']}, this one is at {_pin(EB)}")
    fresh = build()
    changed = sorted(rid for rid in set(kept["cards"]) | set(fresh["cards"])
                     if kept["cards"].get(rid) != fresh["cards"].get(rid))
    if changed:
        wrong.append(f"{len(changed)} card(s) come out differently: {', '.join(changed[:8])}")
    return wrong, f"made again: {len(fresh['cards'])} cards"


def coverage(atlas=None):
    """{action id: how many logged fights use it} for the actions of the logged fights that have no legal card.
    My own and other players' actions; an AI's are not a player's."""
    EB, _ = _tools()
    import opponents
    cards = (atlas or load())["cards"]
    missing = {}
    for bid, _path, rows, _meta in opponents.load_logs():
        used = {a for _, u, a, _ in rows if isinstance(u, str) and u.startswith("user_") and a not in ("wait", "move")}
        for a in used:
            if not (cards.get(a) or {}).get("legal"):
                missing[a] = missing.get(a, 0) + 1
    return missing


def main(argv=None):
    cmd = (argv or sys.argv[1:] or ["check"])[0]
    if cmd == "build":
        atlas = build()
        write(atlas)
        print(json.dumps({k: v for k, v in atlas["_meta"].items() if k != "effect_types"}))
        return 0
    if cmd == "check":
        wrong, note = check()
        print("\n".join(wrong) or f"the atlas is current ({note})")
        return 1 if wrong else 0
    if cmd == "coverage":
        missing = coverage()
        print(json.dumps({"without_a_card": len(missing), "actions": dict(sorted(missing.items(), key=lambda x: -x[1]))},
                         indent=1))
        return 1 if missing else 0
    sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
