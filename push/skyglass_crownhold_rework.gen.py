#!/usr/bin/env python3
"""Generate push/363-365: the Crowned Captain's combat rework, the commanders' set pieces, Crownhold's heal top-ups.

    python3 push/skyglass_crownhold_rework.gen.py --jutsu           # 363: 2 jutsu creates (The Crown's Will, Recall)
    python3 push/skyglass_crownhold_rework.gen.py --ai <363 bundle> # 364: 4 AI edits (Crowned Captain + 3 commanders)
    python3 push/skyglass_crownhold_rework.gen.py --topup           # 365: Crownhold quest edit (heal top-ups)

Sources (state/skyglass_build/, provenance in its README; zero live requests):
  - crowned_captain_spec.json (SKYGLASS_BOSS_FIGHTS.md section 3): `newJutsu` (cc-crowns-will, cc-recall: the two
    records the library push/342 did not create) and `ai.record` (kit, 20 rules, stats, items, innate rows). His set
    pieces are library records (push/342 ids, law 17); cc-* resolve through 363's results bundle (idmap sg363_cc-*).
    `editedJutsu` (the Last Directive's animations) is NOT built: its text is live (push/329) and its animation
    names (cc_phase_shift, cc_last_directive) are art not yet uploaded; it joins the visual-asset push (which needs
    the Crowned Captain's kit off first, law 18).
  - crownhold_spec.json `commanders` (section 7): the Armsmaster, Replicant Zero and the Second keep their push/272
    kits and gain library set pieces; records sent as specced (<= 20 rules).
  - crownhold_spec.json `routeQuestEffects` + the harness's quest.warDivTopUp (fable/skyglass-rule-cap
    overrides/crownhold.params.rul060.json {"D4": 20, "D5": 20}; RUL-2026-10-30-060 item 3) and ccTopUp
    (RUL-2026-10-28-026 item 1: Healing full, clean +35%, War +20% with its buffs for the whole fight, alarm +15%).

Not sent on the AI edits: username and avatar (push/319 set them), hidden (stays hidden). Text of the two new jutsu is
the harness's (SKYGLASS_TEXT.md has none; it matches SKYGLASS_BOSS_FIGHTS.md section 3's battle-log lines), as push/342
did for records the text doc does not carry; animation names that are art still to upload are left empty
(`_placeholders`, via push/skyglass_library.gen.py's effect mapping).

365 re-sends Crownhold whole (quest edits do not fetch-merge): push/349's record (push/skyglass_hoard.gen.py
crownhold_edit, from push/348's bundle) with apply_topups() on top. Any LATER Crownhold edit must start from
crownhold_record() here (or call apply_topups) so the top-ups are not erased.

Do not hand-edit the output.
"""
import copy
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skyglass_wave2 as W  # noqa: E402

CC_ID = "7QofodAiUwIoM-voiA2p6"  # Crownhold D5.BOSS (state/crownhold/ids.json @ai:D5.BOSS)
BUNDLE_348 = os.path.join(W.ROOT, "harvests/inbox/tnr_results_1793459592295.json")
CC_PFX = f"sg{W.NUM['cc_jutsu']}_"
WAR_DIV_TOPUP = {"D4": 20, "D5": 20}  # RUL-2026-10-30-060 item 3 (harness overrides/crownhold.params.rul060.json)
CC_TOPUP = {"clean": 35, "alert": 15, "combat": 20}  # RUL-2026-10-28-026 item 1 (medical: givePools 100, live)
AI_SEND = ("level", "rank", "poolsMultiplier", "statsMultiplier", "regeneration", "preferredGeneral1",
           "preferredGeneral2", "primaryElement", "secondaryElement") + W.STATS6 + W.MASTERIES


def load(name, path):
    s = importlib.util.spec_from_file_location(name, os.path.join(W.ROOT, path))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ 363
def jutsu_creates():
    L = load("skyglass_library", "push/skyglass_library.gen.py")
    L.PFX = CC_PFX
    spec = W.spec("crowned_captain_spec.json")
    placeholders, items = [], []
    for rec in spec["newJutsu"]:
        e = L.jutsu(rec["id"], rec, rec["name"], rec["description"], rec["battleDescription"], placeholders)
        assert e["data"]["cooldown"] >= L.COOLDOWN_FLOOR, rec["id"]
        items.append(e)
    recall = next(e for e in items if e["srcId"] == CC_PFX + "cc-recall")
    s = [x for x in recall["data"]["effects"] if x["type"] == "summon"]
    assert len(s) == 1 and s[0]["aiId"] == spec["recallEcho"]["id"], s  # a live Crownhold D5 regular
    return items, placeholders


# ------------------------------------------------------------------ 364
def ai_edit(where, target, rec, ids, notes, label):
    jutsus = [ids.jutsu(j, where) for j in rec["jutsus"]]
    rules = W.finish_rules([W.convert_rule(r, ids, where) for r in rec["rules"]], where, notes)
    W.check_ai(where, jutsus, rules)
    data = {k: copy.deepcopy(rec[k]) for k in AI_SEND if k in rec}
    data.update({"jutsus": jutsus, "items": [{"ids": list(it["ids"]), "number": it.get("number", 0)}
                                             for it in rec.get("items") or []],
                 "effects": copy.deepcopy(rec.get("effects") or []), "includeDefaultRules": False, "rules": rules})
    return {"entity": "ai", "slot": "edit", "targetId": target, "name": label, "data": data}


def ai_edits(bundle):
    im = W.idmap(bundle)
    extra = {}
    for k in ("cc-crowns-will", "cc-recall"):
        v = im.get(CC_PFX + k)
        if not W.NANO.match(v or ""):
            raise SystemExit(f"{os.path.basename(bundle)} has no {CC_PFX}{k}: run push/{W.NUM['cc_jutsu']} first")
        extra[k] = v
    ids = W.Ids(extra=extra)
    notes = []
    cc = W.spec("crowned_captain_spec.json")["ai"]
    assert cc["id"] == CC_ID
    out = [ai_edit("The Crowned Captain", CC_ID, cc["record"], ids, notes,
                   "The Crowned Captain: set pieces, Recall, The Crown's Will (SKYGLASS_BOSS_FIGHTS 3)")]
    for slot, c in W.spec("crownhold_spec.json")["commanders"].items():
        out.append(ai_edit(f"{slot} {c['liveUsername']}", c["id"], c["record"], ids, notes,
                           f"{c['liveUsername']}: library set pieces (SKYGLASS_BOSS_FIGHTS 7)"))
    return out, notes


# ------------------------------------------------------------------ 365
def heal(power):
    return {"type": "heal", "power": power, "rounds": 1, "target": "INHERIT", "direction": "offence",
            "calculation": "percentage", "poolsAffected": ["Health"], "powerPerLevel": 0,
            "description": "Heal top-up", "appearSfx": "", "disappearSfx": "", "appearAnimation": "",
            "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": ""}


def apply_topups(data, notes):
    """Crownhold's heal top-ups (quest starting buff `heal`, percentage of max HP, 1 round; adds to carried HP and is
    capped at max, theninjarpg@3314d122 libs/combat/tags.ts heal, validators/combat.ts questBuffTypes).

    - War route at D4 and D5 (RUL-2026-10-30-060 item 3): +20% on the division's fourth regular (b4.n.f4, b5.n.f4).
      The harness tops up at division start for its War policy; in the quest the rite route only branches off at the
      terminal puzzle, and the fourth regular is the first fight on it (where War runs died). It is also on the
      Healing route, whose commander is entered full anyway (givePools 100). PLACEMENT IS A PROPOSAL (director).
    - The Crowned Captain fight (RUL-2026-10-28-026 item 1): clean +35%, alarm +15%, War +20% with the War Rite buff
      for the whole fight (rounds 99, harness ccTopUp.warWholeFight); Healing keeps givePools 100.
    Idempotent: a node that already carries the heal is left alone."""
    objs = {o["id"]: o for o in data["content"]["objectives"]}

    def add(nid, power):
        o = objs[nid]
        assert o["task"] == "start_battle", nid
        buffs = list(o.get("applyBuffs") or [])
        if any(b["type"] == "heal" for b in buffs):
            return
        o["applyBuffs"] = [heal(power)] + buffs
        notes.append(f"{nid}: heal +{power}%")

    for div in ("D4", "D5"):
        add(f"b{div[1]}.n.f4", WAR_DIV_TOPUP[div])
    for route, power in CC_TOPUP.items():
        add(f"b5.n.boss.{route}", power)
    for b in objs["b5.n.boss.combat"]["applyBuffs"]:
        if b["type"] != "heal" and b["rounds"] != 99:
            notes.append(f"b5.n.boss.combat: War Rite {b['type']} rounds {b['rounds']} -> 99 (whole fight)")
            b["rounds"] = 99
    assert objs["b5.n.boss.medical"].get("givePools") == 100
    return data


def crownhold_record(notes):
    H = load("skyglass_hoard", "push/skyglass_hoard.gen.py")
    e = H.crownhold_edit(BUNDLE_348)  # = push/349 as run (Crownhold live, hidden)
    e["data"] = apply_topups(e["data"], notes)
    e["name"] = "Crownhold: heal top-ups (War route D4/D5, Crowned Captain route heals)"
    return e


# ------------------------------------------------------------------ main
def main():
    args = sys.argv[1:]
    if "--ai" in args:
        bundle = args[args.index("--ai") + 1]
        items, notes = ai_edits(bundle)
        n = W.NUM["cc_ai"]
        m = {"_note": (f"push/{n}, built from push/{W.NUM['cc_jutsu']}'s bundle {os.path.basename(bundle)} (literal "
                       "ids, law 17): the Crowned Captain's combat rework (crowned_captain_spec.json: Crownfall, "
                       "Command Absolute, Shardstorm, Recall, The Crown's Will; 20 rules) and the three Crownhold "
                       "commanders' library set pieces (crownhold_spec.json), from "
                       f"{W.build_dir_note()}. 4 AI edits, records stay hidden; no jutsu is edited. Run with or after "
                       f"push/{W.NUM['topup']} (the chain was tuned with the heal top-ups). Generated by "
                       "push/skyglass_crownhold_rework.gen.py --ai; do not hand-edit."),
             "_rule_notes": notes, "items": items}
        return W.write(os.path.join(W.OUT, f"{n}_crownhold_captain_rework.json"), m)
    if "--topup" in args:
        notes = []
        n = W.NUM["topup"]
        m = {"_note": (f"push/{n}: Crownhold (hidden) re-sent whole = push/349's record + heal top-ups: War route "
                       "+20% at D4 and D5 (RUL-2026-10-30-060 item 3; placed on the fourth regular, a proposal) and the "
                       "Crowned Captain's route heals (RUL-2026-10-28-026 item 1). Generated by "
                       "push/skyglass_crownhold_rework.gen.py --topup; do not hand-edit."),
             "_changes": notes, "items": [crownhold_record(notes)]}
        return W.write(os.path.join(W.OUT, f"{n}_crownhold_heal_topups.json"), m)
    if args and args != ["--jutsu"]:
        raise SystemExit(__doc__)
    items, placeholders = jutsu_creates()
    n = W.NUM["cc_jutsu"]
    m = {"_note": (f"push/{n}: the Crowned Captain's two new AI jutsu, HIDDEN: The Crown's Will (his phase aura; "
                   "replaces Oni's Hunger) and Recall (summons the Sanctum Vanguard echo, 70% / 2,500 HP), from "
                   f"{W.build_dir_note()}/crowned_captain_spec.json newJutsu. Keep the results bundle: push/"
                   f"{W.NUM['cc_ai']} is built from it (--ai). Generated by push/skyglass_crownhold_rework.gen.py; do "
                   "not hand-edit."),
         "dedupNames": True, "_placeholders": placeholders, "items": items}
    W.write(os.path.join(W.OUT, f"{n}_crownhold_captain_jutsu.json"), m)


if __name__ == "__main__":
    main()
