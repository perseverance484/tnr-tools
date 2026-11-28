#!/usr/bin/env python3
"""Job 645, HIDDEN: Isonade's warnings never overlap or lapse, and the fight is harder (the director, Nov 18).

The director's calls (2026-11-18): "Fix it" (a new warning replaced a pending one in the hidden test, and one of the
three triple-damage windows was lost), then "About 40% HP" for what a good level 100 player should end a clean run on.

Root cause (live battle of the Nov 18 test, engine 3314d122): a stun cut Isonade's AP to 80, so churn 10 + land 90
did not fit, the AI fell through to the next mark rule, and the new warning replaced the pending one. Time
compression (+10 AP per jutsu) does the same. A latent second case: after the bite, a Black Water mark fitted beside
a bitten slam, so two warnings stood at once and the bitten slam's lapsed.

What changes (harness: harness/isonade.ts in /mnt/project-files/tnr/isonade_build, params isonade_v2):
  - Isonade carries an innate stunprevent (power 100, 99 rounds), as Sayo and the kite do.
  - Slam I/II/III and Black Water land cost 70 AP (was 90): a land fits even under time compression.
  - Omen: Black Water I/II/III cost 50 AP (was 40): never beside a slam land or a bitten slam, never landed
    the turn it is marked.
  - Slam III, Bitten no longer marks the next rows: after the bite the slams run A, B, C, then a free turn, where
    a Black Water mark can come without overlapping a slam warning.
  - The third Black Water is marked below 33% health (was 25%), so the boss lives to its third window.
  - Harder: slams power 560 (was 140), Black Water 640 (was 170), brine drain 12% (was 8%), bitten brine lasts
    3 rounds (was 4), Isonade's pools x8.4 (was x5.6, so about 42,400 HP at level 100).
Descriptions that named the old numbers are updated. Animations, targeting and every other field are the live
records' own (captures in state/stolen_stores_captures/isonade_live_2026-11-18, read 2026-11-18 ~19:55Z).

Law 18: phase 10 takes the 11 edited jutsu off Isonade, phase 20 edits them, phase 30 puts the full kit back with
the new pools and stunprevent, phase 40 edits the rule threshold.

Run: python3 push/645_isonade_warnings_tuning.gen.py -> push/645_isonade_warnings_tuning.json. Do not hand-edit.
"""
import copy
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state", "stolen_stores_captures", "isonade_live_2026-11-18")
OUT = os.path.join(ROOT, "push", "645_isonade_warnings_tuning.json")

ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
PROFILE = "3xrmVKb3oAZDQ7YzpGh-S"
KIT = ["5HnvskWG20YUlJciX8gvA", "5tqEkTPERX3lkyon_LOKp", "6w0MWbsSIB2j02MADv1nK", "7wxzJedprikQuUr7nSDrS",
       "8cKI86O81cXAMaFS9qqOo", "9QsiAey2OR8hB3UTNhRGh", "EMD7BPKzoOhGB-aOb_Rf2", "gUO8uQLCC5AjvfOuETYlN",
       "hcqL90RPenl24EY73YJr4", "Kaebmb1nzNi3sMadz0W12", "nngO-MnDwNRUEDdrPw6sI", "Qo04-DUTH_cSbnLmPhLEy",
       "SbfiGJPGdjVmLZcAWQrKl", "SWTtkWhjBsHKAu-OI-CQj", "VCaNcj9kGc8kaFk6rQdpR", "XY3PFkXuY_bHQGmg33hz1",
       "yFClnbV7Yr4WpvmcrDEMi"]  # live profile.getAi 2026-11-18
SLAM = ["5tqEkTPERX3lkyon_LOKp", "8cKI86O81cXAMaFS9qqOo", "XY3PFkXuY_bHQGmg33hz1"]
BITTEN = ["5HnvskWG20YUlJciX8gvA", "7wxzJedprikQuUr7nSDrS", "gUO8uQLCC5AjvfOuETYlN"]
BW_LAND = "VCaNcj9kGc8kaFk6rQdpR"
BW_OMEN = ["yFClnbV7Yr4WpvmcrDEMi", "EMD7BPKzoOhGB-aOb_Rf2", "nngO-MnDwNRUEDdrPw6sI"]
BITE = "9QsiAey2OR8hB3UTNhRGh"

LAND_AP, BW_OMEN_AP = 70, 50
SLAM_POWER, BW_POWER, BRINE_PCT, BITTEN_ROUNDS = 560, 640, 12, 3
POOLS_MULT, BW3_AT = 8.4, 33
STUN_PREVENT = {
    "type": "stunprevent", "power": 100, "rounds": 99, "target": "INHERIT", "appearSfx": "", "direction": "offence",
    "calculation": "percentage", "description": "Prevents being stunned", "disappearSfx": "", "powerPerLevel": 0,
    "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": "",
}
# Top-level fields a jutsu edit sends besides effects (Forge fetch-merges the rest from live).
SEND = ["description", "actionCostPerc", "effects"]


def cap(i):
    with open(os.path.join(CAP, f"{i}.json")) as f:
        return json.load(f)


def one(effects, t):
    hits = [e for e in effects if e["type"] == t]
    assert len(hits) == 1, (t, len(hits))
    return hits[0]


def jutsu_item(rec, phase, name):
    return {"entity": "jutsu", "slot": "edit", "targetId": rec["id"], "phase": phase, "name": name,
            "data": {k: rec[k] for k in SEND}}


def main():
    items = []
    edited = SLAM + BITTEN + [BW_LAND] + BW_OMEN + [BITE]
    assert set(edited) <= set(KIT)
    items.append({"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10,
                  "name": "Isonade: edited jutsu off (law 18)", "data": {"jutsus": [j for j in KIT if j not in edited]}})

    for i, jid in enumerate(SLAM):
        r = cap(jid)
        assert r["actionCostPerc"] == 90 and one(r["effects"], "damage")["power"] == 140
        r["actionCostPerc"] = LAND_AP
        one(r["effects"], "damage")["power"] = SLAM_POWER
        one(r["effects"], "drain")["power"] = BRINE_PCT
        items.append(jutsu_item(r, 20, f"{r['name']}: 70 AP, harder slam and brine"))

    for i, jid in enumerate(BITTEN):
        r = cap(jid)
        fx = r["effects"]
        one(fx, "damage")["power"] = SLAM_POWER
        drain = one(fx, "drain")
        drain["power"], drain["rounds"] = BRINE_PCT, BITTEN_ROUNDS
        brine = [e for e in fx if e["type"] == "visual" and e["target"] == "INHERIT"]
        assert len(brine) == 1 and brine[0]["rounds"] == 4
        brine[0]["rounds"] = BITTEN_ROUNDS
        if i < 2:
            r["description"] = (f"After the bite: the arms slam and rise again at once (the next rows go red), and the "
                                f"brine lasts {BITTEN_ROUNDS} rounds.")
            name = f"{r['name']}: harder slam and brine, brine {BITTEN_ROUNDS} rounds"
        else:
            # The last of three: no next mark (red rows visual, slam-A marker, chain marker).
            before = len(fx)
            r["effects"] = [e for e in fx if not (e["type"] == "visual" and e["target"] == "COORDINATES")
                            and e["type"] not in ("increasecooldown", "increaseheal")]
            assert before - len(r["effects"]) == 3, before - len(r["effects"])
            r["description"] = (f"After the bite: the third slam in a row. The arms come down and stay down, and the "
                                f"brine lasts {BITTEN_ROUNDS} rounds.")
            name = f"{r['name']}: ends the run of three, harder slam and brine"
        items.append(jutsu_item(r, 20, name))

    r = cap(BW_LAND)
    assert r["actionCostPerc"] == 90 and one(r["effects"], "damage")["power"] == 170
    r["actionCostPerc"] = LAND_AP
    one(r["effects"], "damage")["power"] = BW_POWER
    items.append(jutsu_item(r, 20, "Isonade Black Water: 70 AP, harder"))

    for jid in BW_OMEN:
        r = cap(jid)
        assert r["actionCostPerc"] == 40
        r["actionCostPerc"] = BW_OMEN_AP
        items.append(jutsu_item(r, 20, f"{r['name']}: 50 AP"))

    r = cap(BITE)
    r["description"] = "Once, at half health: Isonade tears off a piece of the hull. From now on it slams three turns running."
    items.append(jutsu_item(r, 20, "Bite of the Ship: description"))

    items.append({"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30,
                  "name": "Isonade: kit back (law 18), pools x8.4, cannot be stunned",
                  "data": {"jutsus": KIT, "poolsMultiplier": POOLS_MULT, "effects": [STUN_PREVENT]}})

    prof = cap(PROFILE)
    rules = copy.deepcopy(prof["rules"])
    bw3 = [r for r in rules if r["action"].get("jutsuId") == BW_OMEN[2]]
    assert len(bw3) == 1 and bw3[0]["conditions"][0]["value"] == 25
    bw3[0]["conditions"][0]["value"] = BW3_AT
    assert len(rules) == 20
    items.append({"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40,
                  "name": f"Isonade: third Black Water below {BW3_AT}% health",
                  "data": {"rules": rules, "includeDefaultRules": prof["includeDefaultRules"]}})

    m = {"_note": ("push/645, HIDDEN: Isonade's warnings never overlap or lapse (stunprevent, land 70 AP, Black Water "
                   "omens 50 AP, the bitten run ends on Slam III, third Black Water below 33%) and the fight is harder "
                   "(slam 560, Black Water 640, brine 12%, bitten brine 3 rounds, pools x8.4). Law 18 in phases 10/30. "
                   "Generated by push/645_isonade_warnings_tuning.gen.py from live captures; do not hand-edit."),
         "items": items}
    with open(OUT, "w") as f:
        json.dump(m, f, separators=(",", ":"))
    print(f"wrote {OUT}: {len(items)} items, {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
