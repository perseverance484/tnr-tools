#!/usr/bin/env python3
"""push/336 Zombie Outbreak: Patient Zero AI + pyramid edit (second retry; jutsu VERIFIED by push/335): Patient Zero boss, his three signature jutsu, the Vanquisher of
the Horde badge, and full-record edits of both live quests (rewards, boss swap, text fixes).

Built from the push/330 and push/332 read-only captures:
  harvests/inbox/tnr_results_1793412572981.json (both quests, Zombie Villager)
  harvests/inbox/tnr_results_1793412740001.json (wave AIs, scene assets, items)
Run from the repo root:  python3 push/333_zombie_outbreak_build.gen.py
"""
import json, sys, copy
sys.path.insert(0, "skills/building-tnr-content/scripts")
from factory import Factory
D = "skills/building-tnr-content/data/"
f = Factory(ctors=D + "45c_DATA_constructors.json", entities=D + "45d_DATA_entity_schemas.json", checks=D + "45g_DATA_checks.json")

B1 = "harvests/inbox/tnr_results_1793412572981.json"
pool = json.load(open("32b_DATA_pool.json"))["records"]
caps = {c["input"].get("id") or c["input"].get("userId"): c["data"] for c in json.load(open(B1))["captures"]}
VOTH, ZO = caps["0U8N6218b095-TQbWlCep"], caps["QczZtQGOuODzNVA-_rnHs"]
BADGE_ID = "RAZTo1fZi988ZDuPrqVw7"           # existing live "Vanquisher of the Horde" badge (badge.getAllNames, 2026-10-30)
STAND_IN = "nqL-uL-Z_7I0iuowlpBDx"          # Zombie Villager, lvl 25, the current "Patient Zero"
LEVEL = 30                                  # above the lvl 10/15/20 waves and the lvl 25 stand-in

# ---------------------------------------------------------------- signature jutsu (3)
def dmg(p, stat):
    return f.tag("damage", power=p, powerPerLevel=0, rounds=0, statTypes=[stat],
                 generalTypes=["Strength", "Speed"], elements=[])
# Required-on-create gate fields the validator accepts as null (read from the schema, not typed).
_SCHEMA = json.load(open(D + "45d_DATA_entity_schemas.json"))["entities"]["jutsu"]["fields"]
_REQ = json.load(open(D + "45g_DATA_checks.json"))["required_on_create"]["fields"]["jutsu"]
NULLS = {k: None for k in _REQ if k.startswith("required") and _SCHEMA[k].get("nullable")}
BASE = dict(jutsuType="AI", jutsuRank="D", requiredRank="STUDENT", requiredLevel=1, actionCostPerc=60,
            target="OPPONENT", method="SINGLE", battleUsageType="BOTH", jutsuWeapon="NONE",
            chakraCost=0, staminaCost=0, healthCost=0, extraBaseCost=0, chakraCostReducePerLvl=0,
            staminaCostReducePerLvl=0, healthCostReducePerLvl=0, bloodlineId="", villageId="",
            injectableInBattle=False, hidden=True, **NULLS)
# Icons reuse existing live jutsu art (answers/jutsu_art.json) until bespoke icons exist.
ICON = {"bite": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJeclb3VyV3OvUJQExAi0bGoIZDF74LqSnHRdp",   # Rotting Bite
        "claws": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJgtyil1cU9cpECTimBdjaqbNn7vQsxGR1wLk4",  # Rending Slash
        "bile": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ28cjbUnMXlcRpYmJ5do0zKw4Qx6PVEtBa9b8"}   # Toxic Pool
SIGS = [
 ("pz_bite", "Patient Zero: Infected Bite", 2, 4, "Taijutsu", ICON["bite"],
  "Patient Zero lunges and sinks rotten teeth deep into flesh, leaving a wound that refuses to close.",
  "%user lunges and sinks rotten teeth into %target!",
  [dmg(60, "Taijutsu"), f.tag("wound", power=15, powerPerLevel=0, rounds=2, generalTypes=["Highest"])]),
 ("pz_claws", "Patient Zero: Festering Claws", 2, 3, "Taijutsu", ICON["claws"],
  "Grave-black nails rake across the target and seed an infection that leaves them easier to hurt.",
  "%user rakes festering claws across %target!",
  [dmg(45, "Taijutsu"), f.tag("increasedamagetaken", power=15, powerPerLevel=0, rounds=2)]),
 ("pz_bile", "Patient Zero: Plague Bile", 4, 5, "Ninjutsu", ICON["bile"],
  "A gout of virulent zombie bile that burns on contact and fouls any attempt to heal.",
  "%user retches a stream of plague bile at %target!",
  [dmg(40, "Ninjutsu"), f.tag("poison", power=20, powerPerLevel=0, rounds=2, poolsAffected=["Health"]),
   f.tag("decreaseheal", power=30, powerPerLevel=0, rounds=2)]),
]
items, ranges = [], {}
for src, name, rng, cd, stat, img, desc, bdesc, eff in SIGS:
    e = f.entry("jutsu", "create", name=name, srcId=src, data=dict(BASE, name=name, description=desc,
        battleDescription=bdesc, range=rng, cooldown=cd, statClassification=stat, effects=eff, image=img))
    ranges[src] = rng   # created and VERIFIED by push/335; not re-sent

# ---------------------------------------------------------------- Patient Zero
LIVE = {"pz_bite": "HrNA9mD5WW2uaCdkq7Iao", "pz_claws": "ydcbW8BIAKyYxHpnz7SDw", "pz_bile": "2lWcedG9Dw528HGO4eI6R"}  # push/335 VERIFIED, tnr_results_1793413958294
ranges = {LIVE[k]: v for k, v in ranges.items()}
for code in ("S43", "B28"):
    ranges[pool[code]["id"]] = pool[code]["range"]
P = lambda c: pool[c]["id"]
J = lambda s: LIVE[s]
gate = lambda jid: f.condition("distance_lower_than", value=ranges[jid] + 1, target="CLOSEST_OPPONENT")
use = lambda jid, tgt="CLOSEST_OPPONENT": f.action("use_specific_jutsu", jutsuId=jid, target=tgt)
rules, _ = f.rules(
  f.rule(action=use(P("B19"), "SELF")),                                                  # Warrior's Poise, cd 5
  f.rule(f.condition("health_below", value=40), gate(P("B28")), action=use(P("B28"))),   # enrage: Recoil Slam
  f.rule(gate(J("pz_bite")), action=use(J("pz_bite"))),
  f.rule(gate(J("pz_claws")), action=use(J("pz_claws"))),
  f.rule(gate(P("S43")), action=use(P("S43"))),                                          # Heavy Cut: his sword
  f.rule(gate(J("pz_bile")), action=use(J("pz_bile"))),
  f.rule(action=f.action("move_towards_opponent", target="CLOSEST_OPPONENT")),
  ranges=ranges)
items.append({"entity": "ai", "slot": "create", "phase": 1, "name": "Patient Zero", "srcId": "pz_boss", "data": {
  "username": "Patient Zero", "level": LEVEL, "rank": "CHUNIN", "gender": "Male", "regeneration": 60,
  "poolsMultiplier": 2, "statsMultiplier": 3, "isSummon": False, "hidden": True,
  "preferredGeneral1": "Strength", "preferredGeneral2": "Speed",
  "primaryElement": "", "secondaryElement": "",
  "avatar": "@img:patient_zero_avatar.webp",   # art/halloween_zombie_outbreak, AI_AVATAR preflight 0/0
  "jutsus": [P("B19"), J("pz_bite"), J("pz_claws"), P("S43"), J("pz_bile"), P("B28")],
  "rules": rules, "includeDefaultRules": False,
  # post-0056 columns, as RATIO weights (scaleUserStats rewrites totals from level): bruiser shape
  "offence": 130, "defence": 110,
  "taijutsuMastery": 160, "bukijutsuMastery": 130, "ninjutsuMastery": 90, "genjutsuMastery": 40,
  "bloodlineMastery": 10, "sageMastery": 10,
  "strength": 120, "speed": 110, "intelligence": 60, "willpower": 90}})

# ---------------------------------------------------------------- quest edits (full live record)
DROP = ("id", "createdAt", "updatedAt", "raidStartedAt", "raidEndsAt", "raidCaptureDeadline", "raidGracePeriodEnd")
def full(q):
    out = {k: copy.deepcopy(v) for k, v in q.items() if k not in DROP}
    for k in ("huntingRank", "gatheringRank", "medicalRank"):   # law 42: NONE is inert, omit
        if out.get(k) == "NONE": out.pop(k)
    return out
def fix(s, pairs):
    for a, b in pairs: s = s.replace(a, b)
    return s
def text_pass(obj, pairs):
    if isinstance(obj, dict): return {k: text_pass(v, pairs) for k, v in obj.items()}
    if isinstance(obj, list): return [text_pass(v, pairs) for v in obj]
    return fix(obj, pairs) if isinstance(obj, str) else obj

v = full(VOTH)
v = text_pass(v, [("waves the zombies", "waves of zombies"), ("his hoard", "his horde")])
for o in v["content"]["objectives"]:
    for slot in o.get("opponentAIs") or []:
        slot["ids"] = ["@ai:pz_boss" if i == STAND_IN else i for i in slot["ids"]]
v["content"]["reward"].update({          # PLACEHOLDER amounts: checklist names only the badge and exp
    "reward_badges": [BADGE_ID], "reward_exp": 500, "reward_money": 200000,
    "reward_tokens": 1000, "reward_prestige": 1000, "reward_clanpoints": 1000})
items.append({"entity": "quest", "slot": "edit", "phase": 2, "targetId": VOTH["id"],
  "name": "Vanquish the Horde: Patient Zero boss, rewards + badge, typo fixes", "data": v})

import hashlib, os
ART_REF = "c12f0216e88d3e16a4b1b73f08fa76812a60933d"   # commit that added the avatar bytes
AVATAR_NAME = "patient_zero_avatar.webp"
AVATAR_PATH = "art/halloween_zombie_outbreak/patient_zero_avatar.webp"
AVATAR_BYTES = os.path.getsize(AVATAR_PATH)
AVATAR_SHA = hashlib.sha256(open(AVATAR_PATH, "rb").read()).hexdigest()
man = {"_note": "push/336 second retry. push/335 (tnr_results_1793413958294) VERIFIED the three Patient Zero jutsu (HrNA9mD5WW2uaCdkq7Iao, ydcbW8BIAKyYxHpnz7SDw, 2lWcedG9Dw528HGO4eI6R); its AI create was refused pre-send for pre-migration-0056 stat keys (preferredStat, per-school offence/defence), which blocked the pyramid edit. This creates the hidden level-30 CHUNIN Patient Zero with post-0056 keys (offence/defence/masteries as ratio weights) and literal jutsu ids, then re-sends Vanquish the Horde as a full record: Patient Zero replaces the Zombie Villager stand-in in both boss fights, rewards plus the existing badge RAZTo1fZi988ZDuPrqVw7, typo fixes. Quest stays hidden. Generated by push/336_patient_zero_and_pyramid.gen.py; do not hand-edit. PLACEHOLDERS: pyramid ryo/tokens/prestige/clan points.",
       "dedupNames": True,
       "imgSizes": {AVATAR_NAME: AVATAR_BYTES},
       "imagePack": {"ref": ART_REF, "files": {AVATAR_NAME: {"path": AVATAR_PATH, "sha256": AVATAR_SHA, "bytes": AVATAR_BYTES}}},
       "_placeholders": ["pyramid reward amounts"],
       "items": items}
json.dump(man, open("push/336_patient_zero_and_pyramid.json", "w"), indent=1, ensure_ascii=False)
print(len(items), "entries")
