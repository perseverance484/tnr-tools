#!/usr/bin/env python3
"""Generate the Crownhold manifests from the approved design package (RUL-2026-10-25-005, -010, -011).

    python3 push/crownhold.gen.py

Source: state/crownhold/package/ (claude/silent-bastion-authoring-69za5u@6271e1f, RUL-2026-10-15-001 and
RUL-2026-10-16-*), with the fresh reads of push/269 (state/crownhold/source_check_2026-10-25.md).

push/271 = the records: The Last Directive and Extermination Order (AI jutsu), Countermand (Arakane's item), then the
20 Crownhold AIs. All HIDDEN. The quest follows as push/272 once these ids exist. Do not hand-edit the output.
"""
import hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "state/crownhold/package/state/silent_bastion_authoring")
load = lambda p: json.load(open(os.path.join(PKG, p)))

COMMANDERS = load("design/commanders.json")
PROFILES = load("compiled/ai_profiles.candidate.json")["profiles"]

DEFAULT_JUTSU_IMAGE = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"
SPRITE = {  # live crew sprites (push/249 capture), placeholders until each Crownhold avatar is drawn
    "regular": "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261019-v3-texZaFi42S3EvJZBwQ8cd-main-eded2d557ed1.webp",  # Deck Warden
    "D2.BOSS": "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261018-2OXJEXoktxJcjqMkE851g-main-e5ee91c495de.webp",     # Arsenal Keeper
    "D3.BOSS": "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261018-RBW5KsIXmTGR710D2y2Y7-main-5cda5e3df1ac.webp",     # Sealwright
    "D4.BOSS": "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261018-QY69h271Nx9uHrBeR6jwW-main-b2d624ff6f62.webp",     # The Captain
    # RUL-2026-10-28-003/-004: the D5 boss is the Crowned Captain (Arakane retired); the original crew sprite
    "D5.BOSS": "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261018-fDU9jCPZtH7YHbdQPO9RF-main-25d24b15223f.webp",
}
IMAGES = {"avatar_crownhold_arakane.webp": "art/crownhold/avatar_crownhold_arakane.webp"}
PACK_REF = "123a1b53fbf6ddebe2e624ca0ec766f9d8d4b3c0"  # the commit that carries art/crownhold

# Stat chassis. The package's ladder (RUL-2026-10-16-011) was set against the crew at statsMultiplier 3.0 (the
# Sealwright precedent); the 2026-10-21 pool pass moved the whole crew to 5. Multiplying the ladder by 5/3 keeps every
# Crownhold enemy where the director placed it relative to the crew. Pools are not scaled (the crew's pools did not
# move). PROPOSAL, tuned by the hidden calibration fight (docket B7).
STAT_SCALE = 5 / 3
EVEN_STAT = 1391299.95                      # the crew's even spread (weights for a new AI; scaleUserStats)
MASTERY = {"regular": 556519.98, "boss": 834780}  # the crew's regular / commander masteries

DESC = {  # tag descriptions shown in battle
    "finalstand": "Cannot be reduced below 1 HP", "increasedamagegiven": "Increased damage given",
    "clearprevent": "Cannot be cleared", "damage": "Deals damage", "elementalseal": "Elemental jutsu are sealed",
    "cleanseprevent": "Cannot be cleansed", "clear": "Clears all positive effects", "sealprevent": "Bloodline cannot be sealed",
}
CALC = {"increasedamagegiven": "percentage", "damage": "formula"}


def tag(e):
    t = {"type": e["type"], "power": e["power"], "rounds": e.get("rounds", 0), "target": "INHERIT", "direction": "offence",
         "calculation": e.get("calculation", CALC.get(e["type"], "static")), "powerPerLevel": 0,
         "description": DESC[e["type"]], "appearSfx": "", "disappearSfx": "", "appearAnimation": "",
         "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": ""}
    if e["type"] == "damage":
        # "Highest" is stored as "None" (validators/combat.ts IncludeStats); send what the server keeps.
        t.update({"statTypes": ["None"], "generalTypes": ["Highest"], "elements": [], "dmgModifier": 1,
                  "residualModifier": 1, "allowBloodlineDamageDecrease": True, "allowBloodlineDamageIncrease": True})
    return t


def ai_jutsu(key, src, description, battle):
    r = COMMANDERS["exclusives"][key]["record"]
    return {"entity": "jutsu", "slot": "create", "phase": 1, "name": r["name"], "srcId": src, "data": {
        "name": r["name"], "description": description, "battleDescription": battle,
        "effects": [tag(e) for e in r["effects"]], "target": r["target"], "method": r["method"], "range": r["range"],
        "cooldown": r["cooldown"], "requiredRank": "STUDENT", "requiredLevel": 1, "jutsuType": "AI", "jutsuRank": "S",
        "jutsuWeapon": "NONE", "statClassification": "None", "elementClassification": "None",
        "actionCostPerc": r["actionCostPerc"], "chakraCost": 0, "staminaCost": 0, "chakraCostReducePerLvl": 0,
        "staminaCostReducePerLvl": 0, "healthCost": 0, "healthCostReducePerLvl": 0, "extraBaseCost": 0,
        "bloodlineId": "", "villageId": "", "hidden": True, "injectableInBattle": False, "battleUsageType": "BOTH",
        "image": DEFAULT_JUTSU_IMAGE}}


def countermand():
    r = COMMANDERS["exclusives"]["X:COUNTERMAND"]["record"]
    base = json.load(open(os.path.join(ROOT, "archive/spent-manifests/push-2026-10-25/260_skyglass_items_create.json")))
    data = dict(next(it for it in base["items"] if it["srcId"] == "chart_foundry")["data"])
    data.update({
        "name": "Countermand", "itemType": "OTHER", "slot": "ITEM", "rarity": "LEGENDARY",
        "description": ("The command seal of Crownhold. The Crowned Captain presses it against an afterimage's "
                        "pattern to strip away anything it was not ordered to carry."),
        "battleDescription": "%user raises the Countermand. Every borrowed strength on %target is revoked.",
        "effects": [tag(e) for e in r["effects"]], "target": r["target"], "method": r["method"], "range": r["range"],
        "cooldown": r["cooldown"], "actionCostPerc": r["actionCostPerc"], "destroyOnUse": False, "inShop": False,
        "hidden": True, "battleUsageType": "PVE", "preventBattleUsage": False, "canBeTraded": False,
        "canStack": False, "stackSize": 1, "image": DEFAULT_JUTSU_IMAGE,
    })
    return {"entity": "item", "slot": "create", "phase": 1, "name": "Countermand", "srcId": "countermand", "data": data}


DESCRIPTIONS = {
    "Select specific jutsu": None,
}
ACTION_DESC = {"use_specific_jutsu": "Select specific jutsu", "use_specific_item": "Select specific item",
               "move_towards_opponent": "Move towards opponent", "end_turn": "End turn"}
COND_DESC = {"distance_lower_than": "Distance lower than or equal given value",
             "distance_higher_than": "Distance higher than or equal given value",
             "health_below": "Health below given percentage", "round_lower_than": "Current round is lower than specified value",
             "specific_round": "Specific round", "has_effect": "Has effect", "target_has_effect": "Target has effect"}
# Literal ids of the push/271 creates (law 17: an AI's jutsu and item arrays must carry literal ids; refs are stripped).
IDS_FILE = os.path.join(ROOT, "state/crownhold/ids.json")
IDS = json.load(open(IDS_FILE)) if os.path.exists(IDS_FILE) else {}


SOURCES = load("sources/source_records.json")
SELF_TARGETED = {v["id"] for v in SOURCES["jutsu"].values() if v["record"].get("target") in ("SELF", "EMPTY_GROUND")}


def rule(r):
    a = {k: (IDS.get(v, v) if isinstance(v, str) else v) for k, v in r["action"].items()}
    a["description"] = ACTION_DESC[a["type"]]
    self_cast = a["type"] == "use_specific_jutsu" and r["action"].get("jutsuId") in SELF_TARGETED
    conds = []
    for c in r["conditions"]:
        c = dict(c)
        if self_cast and c["type"] == "distance_lower_than":
            # A distance condition measures from the rule's own target, which is the caster on a self-cast (always 0).
            # "An enemy within N" is what the package meant; same fix as push/251.
            c = {"type": "player_within_range", "minRange": 0, "maxRange": c["value"],
                 "description": "An enemy player is within the inclusive hex range"}
        else:
            c["description"] = COND_DESC[c["type"]]
        conds.append(c)
    return {"action": a, "conditions": conds}


def ai(p):
    r, boss = p["record"], p["slot"].endswith("BOSS")
    g1, g2 = r["generals"]
    data = {
        "username": RENAME.get(p["name"], p["name"]), "hidden": True, "level": r["level"], "rank": r["rank"],
        "poolsMultiplier": r["poolsMultiplier"], "statsMultiplier": round(r["statsMultiplier"] * STAT_SCALE, 2),
        "regeneration": r["regeneration"], "gender": "Unknown", "preferredGeneral1": g1, "preferredGeneral2": g2,
        "primaryElement": None, "secondaryElement": None, "isSummon": False, "avatarFacing": "left",
        **{m: MASTERY["boss" if boss else "regular"] for m in
           ("ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery")},
        "bloodlineMastery": 10, "sageMastery": 10,
        **{s: EVEN_STAT for s in ("offence", "defence", "strength", "intelligence", "willpower", "speed")},
        "avatar": SPRITE.get(p["slot"], SPRITE["regular"]),
        "jutsus": [IDS.get(j, j) for j in r["jutsus"]],
        "items": [{**it, "ids": [IDS.get(i, i) for i in it["ids"]]} for it in r["items"]], "effects": [tag(e) for e in r["effects"]],
        "includeDefaultRules": p["aiProfile"]["includeDefaultRules"],
        "rules": [rule(x) for x in p["aiProfile"]["rules"]],
    }
    return {"entity": "ai", "slot": "create", "phase": 1, "name": RENAME.get(p["name"], p["name"]), "srcId": "crownhold_" + p["slot"].lower(),
            "data": data}


# ---------------------------------------------------------------- the quest (push/273)
SCRIPT = load("design/script.json")
PROTOCOLS = load("design/protocols.json")
GRAPH = json.load(open(os.path.join(ROOT, "state/crownhold/package/harness/silent_bastion_condensed99/graphs/alt99_f4gate.json")))
UFS = "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ"
SCENE = {  # placeholders from the Skyglass set until Crownhold's six scenes are drawn (package art_shotlist.md)
    2: UFS + "TdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH",   # hold          -> Experimental Armory
    3: UFS + "RiFRQZ0udmODoNtpa0FMcwI4k2Eq7nJhyvjl",   # reconstruction -> Skyglass Research
    4: UFS + "8ZwqPukkp45TvAnoIBa0rtCf1lbyXYjVKQ2q",   # gallery       -> High Command
    5: UFS + "Ip0fIvxfOewksxBoS1HQCihpL7c42Ky9uUFv",   # helm          -> Command Sanctum
}
ITEM = {"lantern": "jCJv4N3JSiihuqnK0jJ7t", "coffer": "THo7rfzP-S82_43aN8fs3", "treasury": "Ma8S90Nmbi0Xvm4u4FzJh"}
LASTLIGHT_JUTSU = "0F-68bxOXW_LkJnXV0lwT"
CROWN_FRAGMENT = "ayiRmSjWs05lMPyL3G-1d"  # Fragment of the Skyglass Crown
HONOR_TOKENS = 1000  # Crownhold's Honor: PROPOSAL, the director sets the amount (RUL-2026-10-25-002)
# Director 2026-10-26 (RUL-2026-10-26-003): short ninja-world names. USERNAME = the live AI name (a "Crown " prefix on
# the one-word titles, because usernames are unique across all users, players included: engine law 66). PROSE = how the
# quest text names them (no prefix). Replicant Zero and Supreme Commander Arakane keep their names.
USERNAME = {
    "Master of Arms": "Crown Armsmaster", "Bastion Proving Proctor": "Crown Trialmaster",
    "Ordnance Quartermaster": "Crown Tagwright", "Prototype Lancer Unit": "Crown Lancer",
    "Calibration Duelist": "Crown Duelist", "Skyglass Archive Keeper": "Crown Archivist",
    "Impression Containment Warden": "Crown Binder", "Unstable Echo Subject": "Crown Echo",
    "Failed Reconstruction Prototype": "Crown Stonebound", "The Grand Marshal": "The Second",
    "Command Signal Adjutant": "Crown Signaller", "High Command Staff Tactician": "Crown Tactician",
    "Honor Guard Commandant": "Honor Guard", "Strategist's Aide-de-Camp": "Crown Runner",
    "Sanctum Vanguard": "Crown Vanguard", "Directive Herald": "Crown Herald",
    "Last Watch Executor": "Last Watch", "Order-Bearer of the Sanctum": "Crown Sealbearer",
}
RENAME = USERNAME
PROSE = [  # longest first
    ("Bastion Proving Proctor", "Trialmaster"), ("Crownhold Proving Proctor", "Trialmaster"), ("Proving Proctor", "Trialmaster"),
    ("Failed Reconstruction Prototype", "Stonebound"), ("Impression Containment Warden", "Binder"),
    ("High Command Staff Tactician", "Tactician"), ("Order-Bearer of the Sanctum", "Sealbearer"),
    ("Strategist's Aide-de-Camp", "Runner"), ("Command Signal Adjutant", "Signaller"),
    ("Skyglass Archive Keeper", "Archivist"), ("Ordnance Quartermaster", "Tagwright"),
    ("Prototype Lancer Unit", "Lancer"), ("Unstable Echo Subject", "Echo"), ("Honor Guard Commandant", "Honor Guard"),
    ("Calibration Duelist", "Duelist"), ("Last Watch Executor", "Last Watch"), ("Sanctum Vanguard", "Vanguard"),
    ("Directive Herald", "Herald"), ("Master of Arms", "Armsmaster"), ("The Grand Marshal", "The Second"),
    ("the Grand Marshal", "the Second"), ("Grand Marshal", "Second"), ("Order-Bearer", "Sealbearer"),
    ("Aide-de-Camp", "Runner"), ("Quartermaster", "Tagwright"),
    # RUL-2026-10-26-004: Edo command shrines, not terminals (node ids such as d2.n.terminal are ids, not prose)
    ("Military Command Terminal", "command shrine"), ("command terminal", "command shrine"),
    ("The terminal", "The shrine"), ("the terminal", "the shrine"),
    # RUL-2026-10-26-005: Edo vocabulary for the quest's mechanics (same effects, same routes)
    ("under Security Alert", "with the alarm raised"), ("Security Alert", "Alarm Raised"),
    ("to claim protocol access", "to earn passage"), ("Medical Protocol", "Healing Rite"), ("Combat Protocol", "War Rite"),
]
LABEL = {  # option labels after PROSE (the wrong-answer beats repeat these)
    "Maintenance Passage: enter the disable sequence": "Hidden passage: quiet the racks",
    "Protocol access: face the Duelist": "Proper passage: face the Duelist",
    "Coolant, then Charge, then Seal": "Douse, then Drain, then Seal",
    "Charge, then Coolant, then Seal": "Drain, then Douse, then Seal",
    "Seal, then Coolant, then Charge": "Seal, then Douse, then Drain",
    "Maintenance Passage: identify the original": "Hidden stair: name the original",
    "Protocol access: face the Stonebound": "Proper passage: face the Stonebound",
    "Subject A": "Jar A", "Subject B": "Jar B", "Subject C": "Jar C",
    "Maintenance Passage: present an authorised order": "Service corridor: present a sealed order",
    "Protocol access: face the Runner": "Proper passage: face the Runner",
    "Maintenance Passage: name the directive in force": "Hidden channel: name the directive in force",
    "Protocol access: face the Sealbearer": "Proper passage: face the Sealbearer",
}
FAIL_ID = "f_lost"

QUEST_DESCRIPTION = (
    "Carried out of the wreck, the Lastlight Lantern burns toward a mountain the maps call empty. Crownhold, the fortress "
    "that built the Skyglass Project and gave its crew their last order, has not answered a call in a generation. Its "
    "gates stand open. Nothing guards them.\n\n"
    "Starting the expedition spends one Lastlight Lantern. Lose any fight and the expedition ends; the Lantern is not "
    "refunded.\n\nIf you still have a reward to choose from an earlier expedition, claim it before you set out: an "
    "expedition cannot be completed while an earlier reward choice is waiting.")
QUEST_SUCCESS = "The Crowned Captain has fallen and his Command Crown lies broken. Choose your reward."
BOSS_NAME = "The Crowned Captain"  # username: the legacy Ghost Ship boss keeps "Crowned Captain" (law 66)
# RUL-2026-10-28-004: the Supreme Commander is the Crowned Captain (applied after PROSE; sentence starts capitalised)
BOSS_PROSE = [("Supreme Commander Arakane", "the Crowned Captain"), ("the Supreme Commander", "the Crowned Captain"),
              ("The Supreme Commander", "The Crowned Captain")]
CROWN = ("Above his white mask the Command Crown sits like frost: pale skyglass grown in jagged points around one tall "
         "central blade threaded through a small ring of light, the same crystal that splinters from his armour. Every officer you passed on the way up, and "
         "every hand aboard the Skyglass ship, answered to that crown. You have been breaking its hold all the way up "
         "the mountain.")
OVERRIDE = {  # whole-node text, Edo pass (RUL-2026-10-26-005); the package text keeps the original mechanics
    "d2.n.f1": (
        "The road ends at a gate cut into the mountain. No sentry calls out, no banner hangs, and snow has drifted unbroken "
        "across the parade ground. Whatever lived here left long ago.\n\nInside, the castle armoury is lit.\n\nLong racks "
        "of spears and blades line the walls, each rack bound in paper seals that still hum with chakra. A wooden placard by "
        "the first rack reads: \"NEVER SEAL A RACK WHILE ITS CHAKRA STILL BURNS.\" Somewhere ahead a signal bell rings, and a "
        "figure in a faded grey drill wrap steps out of the lantern light: the Trialmaster, bokken raised, as though you were "
        "late for a trial that began decades ago.\n\n\"Candidate. Your trial number?\" Its eyes burn with pale chakra."),
    "d2.n.f2": (
        "The Trialmaster unravels into drifting chakra, and the bell falls silent. That was no ghost. It answered like a man "
        "reading from a memory.\n\nPast the trial range, an ordnance store stands open. A ledger lies on the counter in a "
        "careful hand: \"Douse the tags first, always, or they flash.\" Behind it, the Tagwright looks up from a tray of "
        "paper explosive tags already smouldering at their edges.\n\n\"Live tags are not for candidates,\" it says, and "
        "fans three of them between its fingers."),
    "d2.n.f3": (
        "The armoury narrows into a stone spear gallery. A lean spearman waits at its end beside a thrusting post scorched "
        "black by lightning, his forearms wrapped in old burn cloth. Someone has scratched a reminder for the night watch into "
        "the post: \"Seal comes last.\"\n\nLightning crawls along his spearhead. He lowers it and lunges."),
    "d2.n.terminal": (
        "Beyond the gallery, a command shrine glows in a wall niche, and beyond that the armoury's heart: a sealed door marked "
        "ARMSMASTER.\n\nThe shrine offers two ways through. A hidden passage runs behind the sealed weapon racks, but its "
        "lock asks how to quiet the racks' seals. Or you can ask for passage the proper way, and the duty officer, the "
        "Duelist, is already striding toward you to test your right to it with a blade."),
    "d2.n.puzzle": (
        "Behind the shrine, the passage lock holds three bell-cords (DOUSE, DRAIN, SEAL) and asks for the order that safely "
        "quiets the racks. A wrong order will not stop you getting through, but the armoury will know you are there.\n\n"
        "Which order do you pull?"),
    "d2.n.boss.clean": (
        "The racks go quiet one by one, and the passage lets you out behind the sealed door before anyone has noticed you."
        "\n\nThe Armsmaster turns from a forge wall hung with every weapon the Skyglass Project ever tested. \"Clean work,\" "
        "he says. \"Now show me whether you can fight as well as you can read.\" He takes down his war-axe without looking."),
    "d2.n.boss.alert": (
        "The racks spit sparks and a great bell hammers through the armoury. You reach the sealed door with the whole floor "
        "awake behind you.\n\nThe Armsmaster is already armed. \"An intruder who wakes the racks,\" he says, \"fights tired "
        "and expected. Raise the alarm.\" Every lantern in the hall flares red."),
    "d2.n.protocol": (
        "The Duelist kneels, its blade broken, and the shrine grants you passage. Two rites wake before the Armsmaster's door."
        "\n\nThe Healing Rite will wash you in the armoury's restorative mist: you enter the fight fully recovered. The War "
        "Rite will instead brace you against his Sovereign Fetters, so his stuns will not hold you."),
    "d3.n.f1": (
        "Beyond the armoury's back stair, the air turns cold and blue. The Skyglass Research Division is an archive hall: tall "
        "shelves of paper-tagged boxes, each holding a skyglass crystal with a faint, sleeping light.\n\nThe Archivist looks "
        "up from a ledger and frowns at you. \"You are not on the register,\" it says, as if that were the stranger thing. "
        "\"Understand what you are walking through. An impression repeats. An original hesitates.\"\n\nIt closes the "
        "ledger, and it does not hesitate."),
    "d3.n.f2": (
        "The Archivist unravels into the shelves. The register it carried lists names (Skyglass researchers, smiths, "
        "officers), each with a date and the word RECALLED.\n\nThe sealing-jar halls beyond are lit by a single tall "
        "skyglass lantern. The Binder stands beneath it, deep-hooded, a great iron sealing key in its hand. You notice the "
        "lantern throws the Binder's shadow across the floor, and the Binder notices you noticing.\n\n\"Impressions never "
        "cast a shadow under the skyglass lantern,\" it says. \"You do. Hold still to be sealed.\""),
    "d3.n.f3": (
        "In the last jar hall, a shinobi steps out of the dark, his outline wavering at the edges as if it cannot decide where "
        "to stop. The tag on his sash reads IX. His voice seems to come from a half-step behind him.\n\n\"They kept trying,"
        "\" he says. \"Every one of us carries his scar: the burn from Replicant Zero's first failed recall. Every one of us "
        "but the copies. I am not a copy. I am not finished.\"\n\nHe lunges with his sai."),
    "d3.n.terminal": (
        "A command shrine stands at the sliding door of the recall chamber. The plaque beside the door reads REPLICANT ZERO, "
        "and beneath it, smaller: THE FIRST TO RETURN.\n\nThe shrine offers the back stair behind the sealing jars, locked "
        "until you name the one original among three recalled shinobi. Or ask for passage the proper way, and face the "
        "chamber's last guardian: the Stonebound, the one they kept."),
    "d3.n.puzzle": (
        "Three recalled shinobi sleep in sealed jars under the skyglass lantern, their shapes showing through the paper "
        "seals. The lock asks which one is the original.\n\nJar A: casts a shadow and bears the old burn scar.\nJar B: casts "
        "no shadow and bears the old burn scar.\nJar C: casts a shadow and bears no scar.\n\nA wrong answer will still open "
        "the stair, but the chamber will be waiting for you."),
    "d3.n.boss.clean": (
        "The stair lets you into the recall chamber from the gallery behind the shoji. On the tatami below, a tall medic in a "
        "high-collared coat turns his own left hand in the lantern light, a small ball of violet healing chakra resting above "
        "his palm.\n\n\"Jar A,\" says Replicant Zero, without turning. \"Correct. I was the first one they brought back, you "
        "know. My body died in that jar. I did not.\" He looks at you, interested. \"Let us see what you are made of. I would "
        "like a copy.\""),
    "d3.n.boss.alert": (
        "The jar seals burst with a crack and the chamber floods with cold blue light. Every seal frame in the room turns "
        "toward you.\n\n\"Wrong one,\" says Replicant Zero, closing his hand around a ball of violet chakra. \"The chamber's "
        "wards are already waking. I was the first one they brought back. My body died in that jar. I did not.\" He smiles. "
        "\"Neither will you leave.\""),
    "d3.n.protocol": (
        "The Stonebound collapses into crystal dust, and the chamber's rites wake.\n\nThe Healing Rite will lay you on the "
        "recall table: you enter the fight fully recovered. The War Rite will instead surge your chakra, increasing the damage "
        "you deal for the opening rounds."),
    "d4.n.f1": (
        "Above the research division, Crownhold becomes a war headquarters. Maps of borders that no longer exist cover the "
        "walls of High Command. Signal bells still ring down the corridors.\n\nThe Signaller turns from a board of bell-cords, "
        "war fan raised. \"Orders arrive by this room or they do not arrive,\" it says. \"And only orders countersigned by "
        "the Second carry two seals. Remember that, intruder. You will not live to use it.\""),
    "d4.n.f2": (
        "The planning hall is set for a war council no one will attend. At the head of the table, the Tactician corrects a "
        "campaign map with a brush of glowing chakra ink.\n\n\"Form matters,\" it says without looking up. \"The Supreme "
        "Commander's seal is always placed to the left of the Second's. Always. An order that gets that wrong was written by "
        "someone who never stood in this room.\" It sets down the brush and draws its jitte."),
    "d4.n.terminal": (
        "Outside the office of the Second, the only officer the Supreme Commander allowed to question him, a command shrine "
        "waits.\n\nThe service corridor to his office opens only for a properly sealed order. Or ask for passage through the "
        "front: the Runner, last courier of the Second, stands at the door with sealed dispatch tubes crackling on its back."),
    "d4.n.puzzle": (
        "The shrine holds three orders. Only one will open the service corridor.\n\nOrder A: two seals; the Supreme "
        "Commander's seal on the right; dated before the Silence.\nOrder B: two seals; the Supreme Commander's seal on the "
        "left; dated before the Silence.\nOrder C: two seals; the Supreme Commander's seal on the left; dated after the "
        "Silence.\n\nA forged order will still open the corridor, but it will be recorded."),
    "d4.n.boss.alert": (
        "A forged order is still an order, and High Command records it. Every bell in the building rings your position as you "
        "step into the Second's office.\n\n\"A forgery,\" says the Second, and sounds almost disappointed. \"I questioned "
        "his orders for thirty years. I never forged one.\" He draws his blade, and the room's wards turn against you."),
    "d4.n.protocol": (
        "The Runner falls, and its sealed dispatches burn away into the shrine, which wakes two rites.\n\nThe Healing Rite "
        "will open the officers' infirmary to you: you enter the fight fully recovered. The War Rite will instead ward your "
        "techniques, so the Second's seals will not hold you."),
    "d5.n.f1": (
        "The last stair climbs into the summit of the mountain. The Command Sanctum is dark obsidian and ember light, and its "
        "Vanguard stands across the gate.\n\n\"State your directive,\" says the Vanguard. \"No? Then hear the Sanctum's: "
        "when two orders disagree, the Sanctum obeys the one that protects the Command.\" Ember light runs along its iron "
        "fire-hook."),
    "d5.n.terminal": (
        "The outer ring of the Sanctum holds Crownhold's last command shrine. Past it is the door of the Crowned "
        "Captain.\n\nThe drainage channel around the ring will open for whoever can name the directive currently in force. "
        "Or ask for passage the proper way, and face the Sealbearer, who guards the door with a sealed scroll case and a "
        "blank, unsigned command seal."),
    "d5.n.puzzle": (
        "Three directives are posted on the shrine. Only one is in force.\n\nDirective 1 (older, signed by the Supreme "
        "Commander): \"Hold the Sanctum doors.\"\nDirective 2 (newer, unsigned): \"Open the doors to the intruder.\"\n"
        "Directive 3 (newest, signed by the Supreme Commander): \"Seal the outer ring. Let the intruder reach me.\"\n\nA "
        "wrong answer still opens the channel, but the ring will be roused."),
    "d5.n.protocol": (
        "The Sealbearer falls, and its blank command seal shatters on the floor. The shrine wakes the Sanctum's last two rites."
        "\n\nThe Healing Rite will restore you in the Sanctum's reliquary: you enter the final fight fully recovered. The War "
        "Rite is the Sanctum's last field directive: for the opening rounds, nothing the Crowned Captain does can weaken you."),
    "d.aftermath": (  # RUL-2026-10-28-004: the crown is the root; breaking it frees every afterimage, ship and castle
        "The Crowned Captain falls to one knee. The Command Crown cracks through its central blade, and its points "
        "break away and shatter on the stone. All through the mountain, something lets go. Then he is only "
        "chakra, settling over the floor of the throne room like ash.\n\nThe signal bells stop. Down every stair you "
        "climbed, the officers who still stood lower their blades and fade, released at last. Far away on the shore, the "
        "Skyglass wreck goes quiet: its crew were his echoes too.\n\nShards of the broken crown lie scattered across "
        "the throne room floor, still faintly cold with skyglass light. On the wall behind the throne, his last directive is "
        "carved in his own hand: PRESERVE COMMAND. PRESERVE THE CREW. HOLD UNTIL THE MISSION IS DONE. Beneath it, where the "
        "mission should be written, the stone is blank."),
}
# RUL-2026-10-28-005: the Crowned Captain never sailed. He commands the afterimages from afar; the one players beat
# aboard the Ghost Ship was one of his echoes, which is why they look alike.
ECHO_LINE = '"I defeated you once!"'
ECHO_BEAT = {
    "d5.n.boss.clean": ("The Crowned Captain tilts his head. The points of his crown catch the light like frost.<br><br>"
                        "\"You defeated a voice I lent to a ship,\" he says. \"I control... many echoes.\"<br><br>"
                        "He draws his blade."),
    "d5.n.boss.alert": ("Behind the white mask, something like a smile. Every crystal on his armour flares at once.<br><br>"
                        "\"You defeated a voice I lent to a ship,\" he says. \"I control... many echoes.\"<br><br>"
                        "Every ward in the Sanctum flares."),
}
PROTOCOL_INTRO = ("The rite takes hold, and the Sanctum door opens on the throne room. The Crowned Captain waits there, "
                  "masked in white, skyglass splintering from his armour, his Command Crown grown in pale jagged points "
                  "around one tall blade. Every officer you passed on the way up, and every hand aboard the Skyglass ship, "
                  "answered to that crown.<br><br>You know that mask. You have fought it before.")
FAIL_TEXT = "You fall, and Crownhold does not let you up. You wake outside the gate in the snow, and the Lantern has gone dark."
WIN_TEXT = "Crownhold falls silent behind you. The crown that held its officers and the Skyglass crew is broken."


def prose(t):
    for a, b in (("the Silent Bastion", "Crownhold"), ("The Silent Bastion", "Crownhold"), ("Silent Bastion", "Crownhold"),
                 ("the Bastion's", "Crownhold's"), ("The Bastion's", "Crownhold's"), ("the Bastion", "Crownhold"),
                 ("The Bastion", "Crownhold"), ("Bastion", "Crownhold")):
        t = t.replace(a, b)
    for a, b in PROSE + BOSS_PROSE:
        t = t.replace(a, b)
    return re.sub(r'(^|[.!?]"? |\n)the Crowned Captain', lambda m: m.group(1) + "The Crowned Captain", t)


def qtag(t, kind):
    calc = {"stunprevent": "percentage", "increasedamagegiven": "percentage", "increasedamagetaken": "percentage"}
    return {"type": t["type"], "power": t["power"], "rounds": t["rounds"], "target": "INHERIT", "direction": "offence",
            "calculation": t.get("calculation", calc.get(t["type"], "static")), "powerPerLevel": 0,
            "description": {"buff": "War Rite", "debuff": "Alarm Raised"}[kind], "appearSfx": "",
            "disappearSfx": "", "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": ""}


def quest():
    obj = SCRIPT["objectives"]
    nodes = [n for n in GRAPH["nodes"] if n.get("lane") != "recovery" and n["kind"] != "reset"]
    keep = {n["id"] for n in nodes}
    div_of = lambda nid: int(nid[1]) if nid[1].isdigit() else 5
    out = []

    def scene(nid):
        return SCENE[div_of(nid)] if nid[1].isdigit() else SCENE[5]

    def text(nid):
        if nid in OVERRIDE: return prose(OVERRIDE[nid])
        t = prose(obj[nid]["text"])
        if nid == "d5.n.boss.clean":  # the Ghost Ship's last order was his (story bible, Ghost Ship lore carried forward)
            t = t.replace("I gave them that.", "I gave them that, and I gave my ship the same order: preserve command, preserve "
                          "the crew, hold until the mission is done.")
        if nid in ("d5.n.boss.clean", "d5.n.boss.alert"):
            t = t.replace(" He turns.", " " + CROWN + "\n\nHe turns.").replace(" He turns from the window.", " " + CROWN + "\n\nHe turns from the window.")
        return t

    for n in nodes:
        nid = n["id"]
        if n["kind"] == "dialog":
            o = obj[nid]
            if "choices" in n:
                opts = o.get("options", {})
                choices, seen = [], {}
                for c in n["choices"]:
                    seen[c["to"]] = seen.get(c["to"], 0) + 1
                k = 0
                for c in n["choices"]:
                    label = prose(opts.get(c["label"]) or opts.get(c["to"]) or c["label"])
                    label = LABEL.get(label, label)
                    if seen[c["to"]] > 1:  # a menu may not send two options to one node: each wrong answer gets a beat
                        k += 1
                        beat = f"{nid}.wrong{k}"
                        out.append({"id": beat, "task": "dialog", "description": f"You choose: {label}. Somewhere in the walls a ward wakes and turns toward you.",
                                    "sceneBackground": scene(nid), "sceneCharacters": [], "nextObjectiveId": [{"text": "Go on", "nextObjectiveId": c["to"]}]})
                        choices.append({"text": label, "nextObjectiveId": beat})
                    elif nid == "d5.n.protocol":  # the rite route meets him too: intro, the line, his answer, then the fight
                        intro, reply = f"{nid}.{c['to']}.intro", f"{nid}.{c['to']}.echoes"
                        out.append({"id": intro, "task": "dialog", "description": PROTOCOL_INTRO, "sceneBackground": scene(nid),
                                    "sceneCharacters": [], "nextObjectiveId": [{"text": ECHO_LINE, "nextObjectiveId": reply}]})
                        out.append({"id": reply, "task": "dialog", "description": ECHO_BEAT["d5.n.boss.clean"], "sceneBackground": scene(nid),
                                    "sceneCharacters": [], "nextObjectiveId": [{"text": "Fight", "nextObjectiveId": c["to"]}]})
                        choices.append({"text": label, "nextObjectiveId": intro})
                    else:
                        choices.append({"text": label, "nextObjectiveId": c["to"]})
            else:
                nxt = n["next"]
                label = "Fight" if nxt.startswith("b") else ("Leave Crownhold" if nxt.startswith("w") else "Continue")
                choices = [{"text": label, "nextObjectiveId": nxt}]
                if nid in ECHO_BEAT:  # RUL-2026-10-28-005: the player recognises him; he answers, then the fight
                    beat = nid + ".echoes"
                    out.append({"id": beat, "task": "dialog", "description": ECHO_BEAT[nid], "sceneBackground": scene(nid),
                                "sceneCharacters": [], "nextObjectiveId": [{"text": "Fight", "nextObjectiveId": nxt}]})
                    choices = [{"text": ECHO_LINE, "nextObjectiveId": beat}]
            out.append({"id": nid, "task": "dialog", "description": text(nid).replace("\n\n", "<br><br>").replace("\n", "<br>"), "sceneBackground": scene(nid),
                        "sceneCharacters": [], "nextObjectiveId": choices})
        elif n["kind"] == "battle":
            slot = n["encounterSlot"]
            ref = IDS.get("@ai:" + slot, "@ai:crownhold_" + slot.lower())
            lose = "f.arakane" if n["onLoss"] == "f.arakane" else FAIL_ID
            b = {"id": nid, "task": "start_battle", "description": prose(obj[nid]["text"]), "sceneBackground": scene(nid),
                 "sceneCharacters": [], "opponentAIs": [{"ids": [ref], "number": 1, "quantity": 1}],
                 "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False, "opponent_scaled_to_user": False,
                 "nextObjectiveId": n["onWin"], "failObjectiveId": lose, "failDescription": "You are defeated.",
                 "drawDescription": "The fight stalls and the moment is lost.",
                 "fleeDescription": "You break away, and Crownhold closes behind you."}
            if n.get("startPoolsPercent") == 100: b["givePools"] = 100
            eff = n.get("startEffect", "")
            if eff.startswith("SECURITY_ALERT"):
                b["applyDebuffs"] = [qtag(PROTOCOLS["securityAlert"]["effect"]["tag"], "debuff")]
            elif eff.startswith("COMBAT_PROTOCOL"):
                d = eff.split("_")[2]
                b["applyBuffs"] = [qtag(PROTOCOLS["combat"][d]["effect"]["tag"], "buff")]
            out.append(b)
        elif n["kind"] == "win":
            out.append({"id": nid, "task": "win_quest", "description": WIN_TEXT, "sceneBackground": SCENE[5], "sceneCharacters": [],
                        "reward_exp": 5000, "reward_items": [{"ids": [ITEM["treasury"]], "number": 6, "quantity": 1}]})
        elif n["kind"] == "fail":
            out.append({"id": nid, "task": "fail_quest", "description": prose(obj[nid]["text"]), "sceneBackground": SCENE[5], "sceneCharacters": []})
    out.append({"id": FAIL_ID, "task": "fail_quest", "description": FAIL_TEXT, "sceneBackground": SCENE[2], "sceneCharacters": []})
    # RUL-2026-10-28-003: a guaranteed pick of one Fragment of the Skyglass Crown for players farming it
    reward = {"reward_items": [{"ids": [ITEM["coffer"]], "number": 100, "quantity": 2},
                               {"ids": [CROWN_FRAGMENT], "number": 100, "quantity": 1}], "reward_tokens": HONOR_TOKENS,
              "reward_jutsus": [LASTLIGHT_JUTSU]}
    if "badge:crownbreaker" in IDS: reward["reward_badges"] = [IDS["badge:crownbreaker"]]
    return {"entity": "quest", "slot": "create", "srcId": "crownhold", "name": "Crownhold", "data": {
        "name": "Crownhold", "description": QUEST_DESCRIPTION, "image": SPRITE["D5.BOSS"],
        "questType": "battlepyramid", "questRank": "S", "successDescription": QUEST_SUCCESS, "retryDelay": "none",
        "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True, "requiredLevel": 1, "maxLevel": 100,
        "maxAttempts": 100, "maxCompletes": 100, "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None,
        "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": out, "sceneBackground": "", "sceneCharacters": [],
                    "entryItems": [{"ids": [ITEM["lantern"]], "number": 1}], "isolated": True,
                    "rewardMode": "choose", "rewardPickCount": 1, "reward": reward}}}


def write(num, slug, note, items):
    files = {}
    used = json.dumps(items)
    for name, path in IMAGES.items():
        if "@img:" + name in used:
            b = open(os.path.join(ROOT, path), "rb").read()
            files[name] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    m = {"_note": note, "dedupNames": True}
    if files:
        m.update({"imgSizes": {k: v["bytes"] for k, v in files.items()}, "imagePack": {"ref": PACK_REF, "files": files}})
    m["items"] = items
    json.dump(m, open(os.path.join(ROOT, f"push/{num}_{slug}.json"), "w"), indent=1)
    print(num, len(items), "items")


def main():
    # push/271 and push/272 have run and are archived; set REGEN_271=1 / REGEN_272=1 only to reproduce them.
    if os.environ.get("REGEN_271"): write(271, "crownhold_exclusives", (
        "Crownhold exclusives (push/271), all HIDDEN (RUL-2026-10-25-005; package RUL-2026-10-15-001 / -10-16-*): The Last "
        "Directive and Extermination Order (Arakane's AI jutsu; values approved RUL-2026-10-16-004/-011/-013) and "
        "Countermand (his OTHER item: Clear 100, 40 AP, range 5, cooldown 6, PVE; RUL-2026-10-16-011). They must exist "
        "before the 20 Crownhold AIs (push/272), which equip them by literal id (law 17). Placeholder icons. Generated by "
        "push/crownhold.gen.py; do not hand-edit."), [
        ai_jutsu("X:LAST_DIRECTIVE", "last_directive",
                 ("The Crowned Captain's final order to himself. For five rounds he cannot fall, strikes harder, and nothing he "
                  "carries can be stripped away."),
                 "%user speaks the Last Directive. The Command Crown blazes and refuses to let him fall."),
        ai_jutsu("X:EXTERMINATION_ORDER", "extermination_order",
                 ("Given only while the Last Directive holds. A single killing order that seals the target's elements "
                  "and keeps them from cleansing it."),
                 "%user issues the Extermination Order. Every thread of the Crown pulls toward %target."),
        countermand()])
    if os.environ.get("REGEN_272") and all(k in IDS for k in ("@jutsu:last_directive", "@jutsu:extermination_order", "@item:countermand")):
        write(272, "crownhold_ais", (
            "Crownhold AIs (push/272), all HIDDEN: the 20 enemies exactly as the package's kits and rule sets "
            "(includeDefaultRules false, end_turn last); Arakane equips push/271's records by literal id. Changes from the "
            "package: current AI schema (combat stats + masteries; no preferredStat, removed by migration 0056); the "
            "crew chassis (even stats, masteries 556,519.98 regulars / 834,780 commanders); the package's stat ladder x5/3 "
            "to keep its place against the crew after the 2026-10-21 pool pass (PROPOSAL; the calibration fight tunes it); "
            "pools as approved; self-cast distance gates rewritten as 'enemy within N'. Kits keep Shuriken Storm at its "
            "new strength (director 2026-10-25: 'Let them use it'). Avatars: Arakane's own; the other 19 borrow crew "
            "sprites until drawn. Generated by push/crownhold.gen.py; do not hand-edit."),
            [ai(p) for p in PROFILES])
    if os.environ.get("REGEN_276"): write(276, "crownhold_ai_rename", (
        "Crownhold AI renames (push/276), RUL-2026-10-26-003: username-only direct edits on the 18 hidden Crownhold AIs "
        "(Replicant Zero and Supreme Commander Arakane keep their names). Forge fetch-merges and re-sends each AI's live "
        "kit (jutsus, items), so nothing else changes; updateAi rescales stats on every write (law 71, expected). If a "
        "name is refused as taken (law 66), report it; the fix is a new name, not a retry. Generated by "
        "push/crownhold.gen.py; do not hand-edit."),
        [{"entity": "ai", "slot": "edit", "name": USERNAME[p["name"]], "targetId": IDS["@ai:" + p["slot"]],
          "data": {"username": USERNAME[p["name"]]}} for p in PROFILES if p["name"] in USERNAME])
    # Director 2026-10-28: one large update. 273 and 276 are assembled into push/319 by push/skyglass_update.gen.py.
    q = quest()
    out = os.path.join(ROOT, "state/crownhold/quest.preview.json")
    json.dump(q, open(out, "w"), indent=1)
    print("quest preview:", len(q["data"]["content"]["objectives"]), "objectives ->", os.path.relpath(out, ROOT))
    if os.environ.get("REGEN_273") and all("@ai:" + p["slot"] in IDS for p in PROFILES):
        badge = "badge:crownbreaker" in IDS
        write(273, "crownhold_quest", (
            "Crownhold (push/273), HIDDEN isolated Battle Pyramid (RUL-2026-10-25-005/-010/-011; package alt99_f4gate without "
            "its recovery lane). Entry: Lastlight Lantern. Four divisions, 16 to 20 fights; a lost fight ends the run "
            "(Arakane's loss keeps its own text). Puzzles, Alarm Raised (+10% damage taken 2r), Healing Rite (givePools 100) or "
            "War Rite before each commander; Edo wording RUL-2026-10-26-005. Ending: ladder VI (5,000 exp, Sealed Treasury 6%). Pick 1: Skyglass "
            "Coffer x2 / Crownhold's Honor (1,000 village tokens, PROPOSAL) / " + ("Crownbreaker badge / " if badge else "")
            + "Lastlight jutsu. Enemies by literal push/272 ids. Scenes borrow the Skyglass set. Generated by "
            "push/crownhold.gen.py; do not hand-edit."), [q])
        if not badge:
            print("273 written WITHOUT the Crownbreaker badge: add its id to state/crownhold/ids.json and regenerate")


if __name__ == "__main__":
    main()
