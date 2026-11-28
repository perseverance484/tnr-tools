#!/usr/bin/env python3
"""Genin dungeon (Rogue Hideout, sector 1034): hidden build for a test run (director's go 2026-11-18, "Yes, build it.").

Design of record: Claude Doc "Genin dungeon: mechanics design" rev 28 (thread notes:
/mnt/project-files/.task-notes/cmsg_01HemWcQ2jhMimRupeBNzcGRBHVsUsriF9qBYGTZygQ8Vh/working-notes.md).
Director's calls: pass untradable; Rogue Sighting gate kept; required level 10; permanent; reuse the live shared marks.

    python3 push/genin_dungeon.gen.py [--bundle=<results.json> ...] [--placements=<json>]

Stages (law 17: AI jutsus/items and summon aiIds need LITERAL ids, so each stage is regenerated from the bundles
of the stages before it; their idmap gives srcId -> created id):
  660  item + jutsu   Hideout Pass, Rogue Cleave, Rogue Sweep, Rogue Rally
  661  AI            Rogue Shinobi, Rogue Marksman, Rogue Squad Leader, Rogue Shinobi Reinforcement (summon)
  662  jutsu         Rogue Reinforcements (names the summon AI)
  663  AI            Rogue Captain
  (placements)       three overworldAi.upsertPlacement calls, isActive false, made directly over the connector;
                     their ids go in state/genin_dungeon/placements.json (--placements)
  664  quest+dungeon Rogue Sighting (bound to the Rogue Shinobi placement), Rogue Hideout

Every create is hidden. Names and art are placeholders (story comes later from the director). Do not hand-edit
the outputs.
"""
import copy
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills/building-tnr-content/scripts"))
os.chdir(os.path.join(ROOT, "skills/building-tnr-content/data"))
from factory import Factory  # noqa: E402

F = Factory()
PFX = "gd_"
BUNDLES = [os.path.join(ROOT, a.split("=", 1)[1]) for a in sys.argv[1:] if a.startswith("--bundle=")]
PLACEMENTS = next((os.path.join(ROOT, a.split("=", 1)[1]) for a in sys.argv[1:] if a.startswith("--placements=")), None)
STATE = os.path.join(ROOT, "state/genin_dungeon")

# ---------------------------------------------------------------- live records reused (read 2026-11-18 ~22:56Z)
LIVE = {
    "omen_line": "gLsou07qLtM34zyepQRcS",    # Omen: Three-Plank Line (marker lifesteal on self), 3 tiles in front
    "erupt_line": "_O62ht0B7XNYzlISG1Gp5",   # Eruption: Three-Plank Line, power 90
    "omen_splash": "cJD-5e-7oZhQfvDfypyK-",  # Omen: Seven Planks (marker increaseheal), 9-tile blob 1-3 in front
    "erupt_splash": "6YkuEE7zG_y-ocGPjc5gS", # Eruption: Seven Planks, power 80
    "omen_ring": "Z9B3wJGA12Zlb5s8-MNUh",    # Omen: Cracking Ring (marker increasecooldown), radius 2 round caster
}
MARK = {"line": "lifesteal", "splash": "increaseheal", "ring": "increasecooldown"}
HIT_ANIM = "Z9j8J7ZmAjiaxH2S4nDy8"           # the eruptions' appear animation
PLACEHOLDER_IMG = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"
# KGK Rogue's live sprite (level-10 genin rogue), placeholder until the director's art lands
AVATAR = "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261018-gocAYWKP6NwO3YXFHfPV_-main-60ab311f15ee.webp"
PKG = json.load(open(os.path.join(STATE, "reward_packages_20261118.json")))["packages"]
D_MISSION = "AI7oUbJZHCX3pw1X9NKUo"           # D Rank Mission (Rogue Sighting)
D_DUNGEON = "zDG-4RdRY2-ARfXErsFpU"           # D-Rank Dungeons Level 10-30 (clear)
SECTOR, ENTRANCE = 1034, (12, 8)

notes = []


def sid(i):
    return PFX + i


def ref(kind, i):
    return f"@{kind}:{sid(i)}"


# ---------------------------------------------------------------- jutsu
def jutsu_base(name, desc, battle, target, method, coords, rng, cd, ap, effects):
    return {
        "name": name, "description": desc, "battleDescription": battle, "extraBaseCost": 0, "effects": effects,
        "target": target, "range": rng, "cooldown": cd, "bloodlineId": "", "requiredLevel": 1,
        "requiredRank": "STUDENT", "jutsuType": "AI", "image": PLACEHOLDER_IMG, "jutsuWeapon": "NONE",
        "statClassification": "None", "elementClassification": "None", "jutsuRank": "D", "actionCostPerc": ap,
        "staminaCost": 0.05, "chakraCost": 0.05, "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
        "healthCostReducePerLvl": 0, "healthCost": 0, "villageId": "", "method": method,
        "coordinateTargeting": coords, "methodSize": None, "hidden": True, "battleUsageType": "BOTH",
        **{k: None for k in ("requiredBloodlineItemId", "requiredBloodlineMastery", "requiredBukijutsuMastery",
                             "requiredGenjutsuMastery", "requiredIntelligence", "requiredNinjutsuMastery",
                             "requiredSageMastery", "requiredSpeed", "requiredStrength", "requiredTaijutsuMastery",
                             "requiredWillpower")},
    }


def dmg(power):
    return {"type": "damage", "power": power, "rounds": 0, "target": "INHERIT", "appearSfx": "", "direction": "offence",
            "statTypes": ["None"], "calculation": "formula", "description": "Deals damage to target", "dmgModifier": 1,
            "disappearSfx": "", "friendlyFire": "ENEMIES", "powerPerLevel": 0, "appearAnimation": HIT_ANIM,
            "staticAnimation": "", "staticAssetPath": "", "residualModifier": 1, "disappearAnimation": "",
            "allowBloodlineDamageDecrease": True, "allowBloodlineDamageIncrease": True}


# Winded: Quench's engine-tested self weakness (lib-quench), x3 damage taken for 1 round, every general.
WINDED = {"type": "weakness", "power": 100, "rounds": 1, "target": "SELF", "appearSfx": "", "direction": "offence",
          "calculation": "static", "description": "Winded: takes triple damage for 1 round", "dmgModifier": 3,
          "disappearSfx": "", "powerPerLevel": 0, "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "",
          "disappearAnimation": "", "items": [], "jutsus": [], "elements": [],
          "statTypes": ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"],
          "generalTypes": ["Highest", "Strength", "Intelligence", "Willpower", "Speed"]}
# The live Three-Plank Line pattern, plus the caster's own hex so a CHARACTER cast is valid (library recipe:
# blasts that carry more than damage stay CHARACTER and include the caster hex, as Ship's Bell / Seal Lines).
LINE = [{"longitude": 0, "latitude": 0}, {"longitude": -1, "latitude": 0}, {"longitude": -2, "latitude": 0},
        {"longitude": -3, "latitude": 0}]

JUTSU = {
    # Captain's Cleave payoff: design ~250 on a level 10 (45% of 550 HP). Formula damage = HP(L20)/10 * power/40 *
    # advantage; power 75 gives ~197 at even stats, ~295 against a level-10's lower stats. The test run tunes it.
    "cleave": jutsu_base(
        "Rogue Cleave", "The Rogue Captain's heavy blow down the line he marked. It leaves him winded.",
        "%user brings his blade down the marked line, and the swing leaves him winded.",
        "CHARACTER", "COORDINATES", {"origin": "CASTER", "selection": "ALL", "coordinates": LINE, "randomCount": 1},
        0, 3, 100, [dmg(75), WINDED]),
    # Captain's Sweep payoff on the live Cracking Ring (radius 2): design ~110 (20%); power 35 gives ~92 even.
    "sweep": jutsu_base(
        "Rogue Sweep", "The Rogue Captain's spinning sweep across the ring he cracked.",
        "%user spins, and his blade sweeps through the cracked ring.",
        "GROUND", "AOE_SPIRAL_SHOOT", None, 2, 3, 100, [dmg(35)]),
    # Squad Leader's Rally: he hits harder for 2 rounds from the round after; a buff, so Clear removes it.
    "rally": jutsu_base(
        "Rogue Rally", "The Squad Leader rallies himself. His blows land harder for 2 rounds.",
        "%user barks a rally and squares up. His next blows will land harder.",
        "SELF", "SINGLE", None, 0, 4, 40,
        [{"type": "increasedamagegiven", "power": 20, "rounds": 2, "target": "SELF", "appearSfx": "",
          "direction": "offence", "calculation": "percentage", "description": "Rally: deals 20% more damage",
          "disappearSfx": "", "powerPerLevel": 0, "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "",
          "disappearAnimation": ""}]),
    # Reinforcements (stage 662): one Rogue Shinobi at a time; summon lock 3 (shared cooldown) and cooldown 3.
    "reinforce": jutsu_base(
        "Rogue Reinforcements", "The Rogue Captain whistles for one rogue shinobi.",
        "%user whistles, and a rogue shinobi drops in beside him.",
        "EMPTY_GROUND", "SINGLE", None, 3, 3, 30,
        [{"type": "summon", "power": 70, "rounds": 99, "target": "INHERIT", "appearSfx": "", "direction": "offence",
          "calculation": "percentage", "description": "Calls one Rogue Shinobi", "disappearSfx": "",
          "powerPerLevel": 0, "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "",
          "disappearAnimation": "", "playerControlled": False, "aiHp": 600, "aiId": ref("ai", "shinobi_summon")}]),
}


def jutsu_entry(key, phase):
    data = copy.deepcopy(JUTSU[key])
    effs = data.pop("effects")
    try:
        F._effects("jutsu", effs)
    except Exception as err:  # noqa: BLE001
        if "generalTypes" not in str(err):
            raise
        notes.append(f"{key}: formula damage with statTypes [None] and no generalTypes, as the live eruptions")
    e = F.entry("jutsu", "create", name=data["name"], srcId=sid(key), data=data)
    e["data"]["effects"] = effs
    e["phase"] = phase
    return e


# ---------------------------------------------------------------- item
PASS = {
    "itemType": "OTHER", "slot": "NONE", "cooldown": 0, "weaponType": "NONE", "target": "SELF", "method": "SINGLE",
    "cost": 1, "repsCost": 0, "seichiSilverCost": 0, "stackSize": 999, "destroyOnUse": False, "range": 0,
    "chakraCost": 0, "staminaCost": 0, "healthCost": 0, "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
    "healthCostReducePerLvl": 0, "actionCostPerc": 60, "battleDescription": "Hideout Pass", "canStack": True,
    "maxImbueNumber": 1, "maxDurability": 100, "inShop": False, "isEventItem": False, "hidden": True, "maxEquips": 1,
    "preventBattleUsage": True, "requiredLevel": 1, "xpToLevel": 1000, "parentItemId": None, "requiredStrength": None,
    "requiredSpeed": None, "requiredIntelligence": None, "requiredWillpower": None, "canBeCrafted": False,
    "canBeImbued": False, "canBeHunted": False, "canBeGathered": False, "canBeTraded": False, "isFarmSeed": False,
    "farmGrowTimeSeconds": 0, "farmYieldItemId": None, "farmMinLevel": 1, "farmPlantExperience": 0,
    "farmHarvestExperience": 0, "farmSellValue": 0, "farmExtractSeedItemId": None, "farmExtractSeedCount": 0,
    "isFarmFertilizer": False, "farmTimeReductionSeconds": 0, "farmFertilizerExperience": 0, "craftingExperience": 0,
    "crystalTargetTypes": None, "bloodlineId": None, "battleUsageType": "BOTH", "effects": [],
    "name": "Hideout Pass", "rarity": "COMMON", "image": PLACEHOLDER_IMG,
    "description": ("<i>Taken from a rogue in sector 1034. It gets you into their hideout.</i><br><br>"
                    "<b>Rogue Hideout</b> · Sector 1034 · Genin, level 10 and up<br>"
                    "Each player spends 1 pass when a run starts. Retries are free. Can't be traded."),
}

# ---------------------------------------------------------------- AI
# Live genin AIs store flat stats at budget/12 + 10 for their level (Shaman Knight L15 4,968.33, Mini-Momo L20
# 8,718.33). Combat stats are reweighted server-side; masteries are kept as sent on a new AI, so they carry the level.
FLAT = {14: 4343.33, 16: 5635.0, 20: 8718.33}
STATS = ["strength", "speed", "intelligence", "willpower", "offence", "defence", "ninjutsuMastery",
         "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery"]


def cond(type_, **kw):
    return F.condition(type_, description="", **kw)


def act(type_, **kw):
    return F.action(type_, **kw)


def use(j, target="SELF", note=""):
    jid = LIVE.get(j) or (j if j == "basicAttack" else ref("jutsu", j))
    return act("use_specific_jutsu", description=note, jutsuId=jid, target=target)


def has(marker):
    return cond("has_effect", effectType=MARK[marker], threshold=1)


def near(lo, hi):
    return cond("player_within_range", minRange=lo, maxRange=hi)


MOVE = {"conditions": [cond("distance_higher_than", value=1, target="CLOSEST_OPPONENT")],
        "action": act("move_towards_opponent", description="close in", target="CLOSEST_OPPONENT")}
BASIC = {"conditions": [], "action": use("basicAttack", "CLOSEST_OPPONENT", "basic attack")}
END = {"conditions": [], "action": act("end_turn", description="unconditional tail (law 41)")}


def marker_kit(mark, omen, erupt, reach):
    """The library recipe: payoff on top, mark when a player is in reach, hold still while marked."""
    return [
        {"conditions": [has(mark)], "action": use(erupt, note="payoff of the mark")},
        {"conditions": [near(1, reach)], "action": use(omen, note="mark")},
        {"conditions": [has(mark)], "action": act("end_turn", description="hold still while the mark is up")},
    ]


SHINOBI_RULES = marker_kit("line", "omen_line", "erupt_line", 3) + [MOVE, BASIC, END]
MARKSMAN_RULES = marker_kit("splash", "omen_splash", "erupt_splash", 3) + [
    {"conditions": [cond("distance_higher_than", value=3, target="CLOSEST_OPPONENT")],
     "action": act("move_towards_opponent", description="close to splash range", target="CLOSEST_OPPONENT")}, BASIC, END]
LEADER_RULES = [
    {"conditions": [cond("distance_lower_than", value=4, target="CLOSEST_OPPONENT")],
     "action": use("rally", note="Rally (lands next round, 2 rounds, clearable)")},
    MOVE, BASIC, END]
CAPTAIN_RULES = [
    {"conditions": [has("line")], "action": use("cleave", note="Cleave payoff (+ Winded on self)")},
    {"conditions": [has("ring")], "action": use("sweep", note="Sweep payoff")},
    {"conditions": [cond("health_below", value=50), cond("does_not_have_summon")],
     "action": use("reinforce", "EMPTY_GROUND_CLOSEST_TO_SELF", "Reinforcements under half health, one at a time")},
    {"conditions": [near(1, 1)], "action": use("omen_ring", note="mark Sweep when a player is adjacent")},
    {"conditions": [has("ring")], "action": act("end_turn", description="hold still while the ring is marked")},
    {"conditions": [near(1, 3)], "action": use("omen_line", note="mark Cleave when a player is within 3")},
    {"conditions": [has("line")], "action": act("end_turn", description="hold still while the line is marked")},
    MOVE, BASIC, END]

STUN_IMMUNE = {"type": "stunprevent", "power": 100, "rounds": 100, "target": "INHERIT", "appearSfx": "",
               "direction": "offence", "calculation": "percentage", "description": "Prevents being stunned",
               "disappearSfx": "", "powerPerLevel": 0, "appearAnimation": "", "staticAnimation": "",
               "staticAssetPath": "", "disappearAnimation": ""}  # shape as live Unkei no Kami


def ai(key, username, level, pools, jutsus, rules, drop=None, summon=False, effects=()):
    data = {"username": username, "avatar": AVATAR, "avatarFacing": "left", "gender": "Unknown", "level": level,
            "rank": "GENIN", "regeneration": 60, "isSummon": summon, "hidden": True, "inArena": False,
            "includeDefaultRules": False, "poolsMultiplier": pools, "statsMultiplier": 1,
            "preferredGeneral1": "Strength", "preferredGeneral2": "Speed", "primaryElement": None,
            "secondaryElement": None, "bloodlineMastery": 10, "sageMastery": 10,
            "effects": list(effects), "jutsus": jutsus,
            "items": [{"ids": [ref("item", "pass")], "number": drop}] if drop else [], "rules": rules}
    for s in STATS:
        data[s] = FLAT[level]
    assert len(rules) <= 20 and rules[-2] is BASIC and rules[-1] is END
    return data


AIS = {
    "shinobi": ai("shinobi", "Rogue Shinobi", 14, 1, [LIVE["omen_line"], LIVE["erupt_line"]], SHINOBI_RULES, 25),
    "marksman": ai("marksman", "Rogue Marksman", 14, 1, [LIVE["omen_splash"], LIVE["erupt_splash"]], MARKSMAN_RULES, 25),
    "leader": ai("leader", "Rogue Squad Leader", 16, 2, [ref("jutsu", "rally")], LEADER_RULES, 50),
    "shinobi_summon": ai("shinobi_summon", "Rogue Shinobi Reinforcement", 14, 1,
                         [LIVE["omen_line"], LIVE["erupt_line"]], SHINOBI_RULES, None, summon=True),
    "captain": ai("captain", "Rogue Captain", 20, 3,
                  [LIVE["omen_line"], ref("jutsu", "cleave"), LIVE["omen_ring"], ref("jutsu", "sweep"),
                   ref("jutsu", "reinforce")], CAPTAIN_RULES, None, effects=[STUN_IMMUNE]),
}


def ai_entry(key, phase):
    d = copy.deepcopy(AIS[key])
    return {"entity": "ai", "slot": "create", "srcId": sid(key), "name": d["username"], "phase": phase, "data": d}


# ---------------------------------------------------------------- quest + dungeon (stage 664)
def placements():
    if PLACEMENTS and os.path.exists(PLACEMENTS):
        return json.load(open(PLACEMENTS))["placements"]
    return {}


def package(pid, attach_id):
    p = PKG[pid]
    return {"id": attach_id, "packageId": pid, "name": p["name"], "description": p["description"],
            "rewards": copy.deepcopy(p["rewards"])}


def quest_entry(phase):
    pl = placements().get("shinobi", "@placement:shinobi")
    objectives = [
        {"id": "o_sight", "task": "defeat_opponents",
         "description": "Rogue shinobi have been sighted in sector 1034. Find one and beat it.",
         "successDescription": "The rogue drops a pass marked with the hideout's sign.",
         "sceneBackground": "", "sceneCharacters": [], "overworldPlacementId": pl,
         "opponentAIs": [{"ids": [ref("ai", "shinobi")], "number": 1}],
         # a placement-bound objective resolves off the placement, never these coordinates (quest.ts
         # isObjectiveLocationSatisfied); mid-sector values only keep law 54 quiet
         "sectorType": "specific", "locationType": "specific", "sector": SECTOR, "longitude": 12, "latitude": 12,
         "completionOutcome": "Win", "nextObjectiveId": "w_done", "failObjectiveId": "f_lost",
         "failDescription": "The rogue beats you back.", "drawDescription": "The rogue slips away.",
         "fleeDescription": "You break off the fight."},
        {"id": "f_lost", "task": "fail_quest",
         "description": "The rogue got the better of you. Take Rogue Sighting again when you are ready.",
         "sceneBackground": "", "sceneCharacters": []},
        {"id": "w_done", "task": "win_quest",
         "description": "The pass gets you into the Rogue Hideout. More rogues in sector 1034 carry them.",
         "sceneBackground": "", "sceneCharacters": [],
         "reward_items": [{"ids": [ref("item", "pass")], "number": 100, "quantity": 1}],
         "reward_packages": [package(D_MISSION, "gd664_rogue_sighting_d_mission")]},
    ]
    data = {
        "name": "Rogue Sighting", "image": PLACEHOLDER_IMG, "questType": "mastery", "questRank": "D",
        "description": ("Rogue shinobi have set up camp in sector 1034. Beat one and take its Hideout Pass.<br><br>"
                        "<i>Genin, levels 10 to 30. Unlocks the Rogue Hideout.</i>"),
        "successDescription": "You can now enter the Rogue Hideout in sector 1034. Each run costs one Hideout Pass.",
        "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
        "requiredLevel": 10, "maxLevel": 30, "maxAttempts": 100, "maxCompletes": 1, "prerequisiteQuestId": None,
        "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives, "sceneBackground": "", "sceneCharacters": [], "entryItems": [],
                    "isolated": False, "reward": {}},
    }
    return {"entity": "quest", "slot": "create", "srcId": sid("quest"), "name": data["name"], "phase": phase,
            "data": data}


def wave(*keys):
    return {"aiIds": [ref("ai", k) for k in keys], "delayRounds": 0}


def floor(kind, *waves):
    return {"kind": kind, "waves": list(waves)}


S, M, L = "shinobi", "marksman", "leader"
TIER = [
    floor("floor", wave(S, S, S), wave(S, S, M)),
    floor("floor", wave(M, M, S), wave(L, S, S)),
    floor("floor", wave(S, S, M), wave(M, M, S), wave(L, M)),
    floor("floor", wave(L, S, S), wave(L, M, M), wave(S, S, S)),
    floor("boss", wave("captain")),
]


def dungeon_entry(phase):
    data = {
        "name": "Rogue Hideout",
        "description": ("Rogue shinobi have dug in at sector 1034. Five floors down, their Captain waits.<br><br>"
                        "Genin, level 10 and up. Parties of 1 to 3. Each player spends 1 Hideout Pass when the run "
                        "starts. Every big hit is marked a turn ahead: step out of the red."),
        "requirements": {"requiredLevel": 10, "prerequisiteQuestId": ref("quest", "quest"),
                         "requiredItemId": ref("item", "pass"), "requiredItemQuantity": 1,
                         "maxAttempts": None, "maxCompletes": None, "attemptDelay": "none", "retryDelay": "none"},
        "structureAssetId": "", "structureScale": 1, "sector": SECTOR, "longitude": ENTRANCE[0],
        "latitude": ENTRANCE[1], "expiresAt": None, "hidden": True, "background": "default", "tiers": [TIER],
        "rewards": {"money": 0, "experience": 0, "tokens": 0, "prestige": 0, "drops": [
            {"type": "package", "id": D_DUNGEON, "chance": 100, "quantity": 1},
            {"type": "item", "id": ref("item", "pass"), "chance": 15, "quantity": 1}]},
    }
    return {"entity": "dungeon", "slot": "create", "srcId": sid("dungeon"), "name": data["name"], "phase": phase,
            "data": data}


items = [
    {"entity": "item", "slot": "create", "srcId": sid("pass"), "name": PASS["name"], "phase": 660, "data": PASS},
    jutsu_entry("cleave", 660), jutsu_entry("sweep", 660), jutsu_entry("rally", 660),
    ai_entry("shinobi", 661), ai_entry("marksman", 661), ai_entry("leader", 661), ai_entry("shinobi_summon", 661),
    jutsu_entry("reinforce", 662),
    ai_entry("captain", 663),
    quest_entry(664), dungeon_entry(664),
]

# every ref must be created earlier in the sequence (or inside the same manifest, for 664's quest ref)
made, problems = set(), []
for it in items:
    for kind, r in re.findall(r'"@(jutsu|ai|item|quest):([^"]+)"', json.dumps(it["data"])):
        if r not in made:
            problems.append(f"{it['srcId']} needs {r} before it")
    made.add(it["srcId"])
assert not problems, problems

idmap = {}
for b in BUNDLES:
    idmap.update(json.load(open(b)).get("idmap") or {})


def resolve(o, keep=()):
    if isinstance(o, dict):
        return {k: resolve(v, keep) for k, v in o.items()}
    if isinstance(o, list):
        return [resolve(v, keep) for v in o]
    if isinstance(o, str):
        m = re.fullmatch(r"@(jutsu|ai|item|quest):(.+)", o)
        if m and m.group(2) in idmap and m.group(1) not in keep:
            return idmap[m.group(2)]
    return o


STAGES = {
    660: "the Hideout Pass item and three new jutsu (Rogue Cleave, Rogue Sweep, Rogue Rally)",
    661: "Rogue Shinobi, Rogue Marksman, Rogue Squad Leader and the summoned Rogue Shinobi Reinforcement",
    662: "Rogue Reinforcements (names the summoned AI)",
    663: "the Rogue Captain",
    664: "the Rogue Sighting quest (bound to the inactive Rogue Shinobi placement) and the Rogue Hideout dungeon",
}
NAMES = {660: "660_genin_dungeon_pass_jutsu", 661: "661_genin_dungeon_rogues", 662: "662_genin_dungeon_reinforcements",
         663: "663_genin_dungeon_captain", 664: "664_genin_dungeon_quest_dungeon"}
for phase, what in STAGES.items():
    st = [resolve(it) for it in items if it["phase"] == phase]
    blob = json.dumps(st)
    open_refs = sorted(set(re.findall(r'"(@(?:jutsu|ai|item):[^"]+)"', blob)) | set(re.findall(r'"(@placement:[^"]+)"', blob)))
    # within 664 the quest is made first, so the dungeon's @quest ref resolves in-run (forge dungeon refs allow it)
    man = {
        "_note": (f"push/{phase}: genin dungeon (Rogue Hideout) hidden build, {what}. Generated by "
                  "push/genin_dungeon.gen.py; do not hand-edit. Director's go 2026-11-18 ('Yes, build it.') covers a "
                  "HIDDEN build for a test run only: every create hidden, placements inactive, nothing unhidden. "
                  "Names and art are placeholders. "
                  + (f"NOT READY: {len(open_refs)} refs wait on earlier stages." if open_refs else "Refs resolved.")),
        "dedupNames": True,
        "items": st,
    }
    out = os.path.join(ROOT, "push", f"{NAMES[phase]}.json")
    with open(out, "w") as fh:
        json.dump(man, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote push/{NAMES[phase]}.json: {len(st)} items; open refs {len(open_refs)} {open_refs[:4]}")
for n in sorted(set(notes)):
    print("  note:", n)
