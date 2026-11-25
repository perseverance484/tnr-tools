#!/usr/bin/env python3
"""
push/622_gobblefather_core.gen.py

Builds push/622_gobblefather_jutsu.json and push/623_gobblefather_ai_quest.json, the HIDDEN build of the
Thanksgiving 2026 event "The Gobblefather" (staff sheet:
state/gobblefather/event_sheet.txt).

    jutsu  12 boss signatures (AI-only, hidden)
    ai     7  enemies (3 supports from the shared pool, 4 bosses)
    quest  1  The Gobblefather (questType event, 3 boss fights + 1 guard fight)

Deliberately absent (follow-up jobs, each needs art or a director ruling):
  - scene/character assets and @scene refs (art pass, producing-tnr-art)
  - jutsu icons (placeholder default image) and FX animations
  - reward items (Golden Feathered Ring, Gobblefather's Cane), badge
    "Family Business", title "The Tax Evader"
  - launch block: dates, maxAttempts/maxCompletes, unhide list

Every balance number below is a PLACEHOLDER (see PLACEHOLDERS) until the
director rules. Payloads are constructed by factory.py / enemy.py, never typed.

Run from the repository root:
    python3 push/622_gobblefather_core.gen.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "building-tnr-content")
sys.path.insert(0, os.path.join(SKILL, "scripts"))

from factory import Factory            # noqa: E402
from enemy import build_ai, load_pool  # noqa: E402

OUT_J = os.path.join(ROOT, "push", "622_gobblefather_jutsu.json")
OUT_A = os.path.join(ROOT, "push", "623_gobblefather_ai_quest.json")
IDS = {}  # jutsu srcId -> literal live id (law 17), filled from 622's results bundle
CTORS = os.path.join(ROOT, "45c_DATA_constructors.json")
ENTS = os.path.join(SKILL, "data", "45d_DATA_entity_schemas.json")
CHECKS = os.path.join(ROOT, "45g_DATA_checks.json")
POOL = os.path.join(ROOT, "32b_DATA_pool.json")

P = "gf622"  # srcId prefix
DEFAULT_ICON = ("https://uploadthing.b-cdn.net/f/"
                "630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp")
STATS4 = ["Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"]

START, END = "2026-11-26", "2026-12-03"  # RUL: Thanksgiving + one week
ENEMY_LEVEL = 75          # PLACEHOLDER: sheet quest level
SCALED_TO_USER = True     # PLACEHOLDER: same setting as One Perfect Crop

PLACEHOLDERS = [
    "Enemy level 75 on every AI, opponent_scaled_to_user true on every fight",
    "Pools/stats multipliers: supports 1/1, bosses 2/3 (role default), Gobblefather pools 3",
    "Every jutsu power, duration and cooldown (listed per jutsu in the summary)",
    "Quest gates: requiredLevel 75, questRank S (from the sheet)",
    "Quest rewards from the sheet: 18,000 exp, 15,000 ryo, 600 prestige, 500 tokens, 600 clan points",
    "Lost guard/boss fights 1-3 retry from the dialog before the fight; only the Gobblefather loss fails the quest",
]


# ------------------------------------------------------------------ effects

def fx(f, t, power, rounds=None, target="INHERIT", **kw):
    vals = {"power": power, "target": target}
    if rounds is not None:
        vals["rounds"] = rounds
    if t == "damage":
        vals.update(calculation="formula", statTypes=["Highest"],
                    generalTypes=["Highest"], elements=[])
    if t == "decreasestat":
        vals.update(direction="offence", statTypes=STATS4, generalTypes=["Speed"])
    vals.update(kw)
    return f.tag(t, **vals)


def jutsu(f, key, name, desc, battle, target, method, rng, cd, ap, rank, effects):
    return f.entry("jutsu", "create", name=name, srcId=f"{P}_j_{key}", data={
        "name": name, "description": desc, "battleDescription": battle,
        "jutsuType": "AI", "jutsuRank": rank, "requiredRank": "STUDENT",
        "requiredLevel": 1, "jutsuWeapon": "NONE", "target": target,
        "method": method, "range": rng, "cooldown": cd, "actionCostPerc": ap,
        "healthCost": 0, "chakraCost": 0, "staminaCost": 0, "extraBaseCost": 0,
        "healthCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
        "staminaCostReducePerLvl": 0, "battleUsageType": "PVE",
        "elementClassification": "None", "statClassification": "Highest",
        "effects": effects, "hidden": True, "injectableInBattle": False,
        "bloodlineId": "", "villageId": "", "image": DEFAULT_ICON,
        "requiredBloodlineItemId": None,
        "requiredStrength": None, "requiredSpeed": None,
        "requiredIntelligence": None, "requiredWillpower": None,
        **{f"required{m}Mastery": None for m in ("Bloodline", "Bukijutsu", "Genjutsu",
                                                  "Ninjutsu", "Sage", "Taijutsu")},
    })


def build_jutsu(f):
    O, S, ALL, ONE = "OPPONENT", "SELF", "ALL", "SINGLE"
    J = {}

    def add(key, *a):
        J[key] = jutsu(f, key, *a)

    # Tony Drumstick
    add("clobber", "Drumstick Release: Concrete Clobber",
        "Tony hardens an oversized drumstick into stone and swings it like a debt he means to collect.",
        "%user swings a stone-hard drumstick into %target. \"Nothing personal.\"",
        O, ONE, 2, 4, 60, "A",
        [fx(f, "damage", 65), fx(f, "stun", 100, 1, apReduction=20)])
    add("barrage", "Feather Barrage: Collection Notice",
        "A spray of razor feathers, each one a reminder that payment is overdue.",
        "%user flings a storm of sharpened feathers. Every one of them is a collection notice.",
        O, ALL, 5, 5, 60, "B",
        [fx(f, "damage", 40), fx(f, "afterburn", 20, 2)])
    add("family_business", "Family Business",
        "Tony squares his shoulders. With his brother at his back, he hits like two turkeys.",
        "%user cracks his knuckles. \"Family business.\"",
        S, ONE, 0, 5, 40, "A",
        [fx(f, "increasedamagegiven", 30, 3)])
    # Vinny Drumstick
    add("wing_guard", "Wing Guard: Protection Payment",
        "Vinny folds his wings into a guard. Protection was always part of the deal.",
        "%user raises his wings. \"Protection's included. You pay for it later.\"",
        S, ONE, 0, 5, 40, "A",
        [fx(f, "decreasedamagetaken", 35, 2)])
    add("counter", "Back-Alley Counter",
        "Vinny waits for the swing, then sends it back the way it came.",
        "%user settles into a back-alley stance. Hit him and it comes back to you.",
        S, ONE, 0, 6, 40, "A",
        [fx(f, "reflect", 30, 2)])
    add("beatdown", "Double Drumstick Beatdown",
        "The brothers' oldest routine: one holds, one swings, and nobody walks away straight.",
        "%user calls \"Tony, now!\" and the Drumstick Brothers bring the beatdown down on %target.",
        O, ONE, 3, 7, 60, "S",
        [fx(f, "damage", 75), fx(f, "stun", 100, 1, apReduction=20)])
    # Don Giblet
    add("feather_tax", "Feather Tax: Mandatory Collection",
        "A sealing technique that draws chakra out of the debtor and banks it as protection.",
        "%user adjusts his spectacles. \"Your chakra has been repossessed.\"",
        O, ONE, 5, 6, 60, "S",
        [fx(f, "damage", 35), fx(f, "drain", 20, 2, poolsAffected=["Chakra"]),
         fx(f, "absorb", 25, 2, target="SELF")])
    add("interest", "Compound Interest",
        "A Debt Mark inked onto the target. It compounds every round it is left unpaid.",
        "%user marks %target in his ledger. \"Interest has already been applied.\"",
        O, ONE, 5, 2, 60, "A",
        [fx(f, "damage", 25), fx(f, "increasedamagetaken", 15, 4)])
    add("collection_day", "Collection Day",
        "Every Debt Mark comes due at once.",
        "%user closes his ledger. \"Collection Day.\" Every unpaid debt on %target comes due.",
        O, ONE, 5, 6, 60, "S",
        [fx(f, "damage", 80)])
    # The Gobblefather
    add("drumsticks", "Thanksgiving Massacre: Flying Drumsticks",
        "Chakra-forged drumsticks rain down from the chandeliers.",
        "%user slams the banquet table in half. \"NOW IT'S PERSONAL!\" Enormous chakra drumsticks rain down on %target.",
        O, ONE, 5, 4, 60, "S",
        [fx(f, "damage", 60), fx(f, "afterburn", 15, 2)])
    add("final_feast", "The Final Feast",
        "The stolen harvest's chakra, packed into a golden corn sphere and detonated.",
        "%user hurls a blazing golden corn sphere. \"This Thanksgiving, nobody eats until the Family eats.\"",
        O, ALL, 5, 8, 60, "S",
        [fx(f, "damage", 85)])
    add("omerta", "Omertà: Code of Feathers",
        "The Code of Feathers. A cornered Don hits back harder than he is hit.",
        "%user rises to his full height. \"THE FAMILY IS POWER!\"",
        S, ONE, 0, 10, 40, "S",
        [fx(f, "decreasedamagetaken", 30, 99), fx(f, "reflect", 25, 99)])
    return J


# ----------------------------------------------------------------------- AI

def gate_rule(f, j, *extra):
    """Exact gate = range + 1 for SINGLE opponent jutsu; ALL and SELF ungated."""
    d = j["data"]
    conds = list(extra)
    if d["target"] != "SELF" and d["method"] == "SINGLE":
        conds.append(f.condition("distance_lower_than", value=d["range"] + 1))
    return f.rule(*conds, action=f.action(
        "use_specific_jutsu", jutsuId=IDS[j["srcId"]],
        target="SELF" if d["target"] == "SELF" else "RANDOM_OPPONENT"))


def pool_rule(f, pool, code, *extra):
    r = pool[code]
    conds = list(extra)
    if r.get("gate") is not None:
        conds.append(f.condition("distance_lower_than", value=r["gate"]))
    return f.rule(*conds, action=f.action(
        "use_specific_jutsu", jutsuId=r["id"],
        target="RANDOM_OPPONENT" if r.get("gate") is not None else "SELF"))


def enemy(f, pool, name, key, role, kit, stat, gens, element="None", rank=None):
    e = build_ai({"name": name, "srcId": f"{P}_ai_{key}", "role": role,
                  "kit": kit, "element": element, "rank": rank,
                  "stat_archetype": "uniform"}, ENEMY_LEVEL, f, pool)
    e.pop("_derived", None)
    d = e["data"]
    # The live AI record moved to the mastery stat model (see push/561 Driftline): enemy.py still
    # emits the retired 8 offence/defence fields and preferredStat, which Forge refuses as unknown
    # keys. Re-express the same uniform ratio in the current fields; the preferred school leans
    # its mastery. Stats are ratio weights (law 15), so only the shape matters.
    for k in ("ninjutsuOffence", "ninjutsuDefence", "genjutsuOffence", "genjutsuDefence",
              "taijutsuOffence", "taijutsuDefence", "bukijutsuOffence", "bukijutsuDefence"):
        d.pop(k)
    for school in ("ninjutsu", "genjutsu", "taijutsu", "bukijutsu"):
        d[school + "Mastery"] = 300 if school == stat.lower() else 150
    d.update(bloodlineMastery=10, sageMastery=10, offence=100, defence=100)
    d["preferredGeneral1"], d["preferredGeneral2"] = gens
    d["gender"] = "Male"
    # enemy.py leaves a self stance's rule on the action's default RANDOM_OPPONENT target; a rule
    # firing a SELF jutsu must target SELF (event.md step 4), so the chain is rebuilt here.
    d["rules"], _ = f.rules(*[pool_rule(f, pool, c) for c in kit],
                            f.rule(action=f.action("move_towards_opponent", target="RANDOM_OPPONENT")))
    return e


def build_ai_entries(f, pool, J):
    H = lambda v: f.condition("health_below", value=v)  # noqa: E731
    move = f.rule(action=f.action("move_towards_opponent", target="RANDOM_OPPONENT"))
    out = []

    # Supports: pool kits, enemy.py's own gated chain (law 41 move fallback).
    out.append(enemy(f, pool, "Feathered Enforcer", "enforcer", "standard",
                     ["S02", "S27", "B37"], "Taijutsu", ("Strength", "Speed")))
    out.append(enemy(f, pool, "Corn Collector", "collector", "standard",
                     ["S06", "S28", "B38"], "Bukijutsu", ("Speed", "Intelligence")))
    out.append(enemy(f, pool, "Feathered Accountant", "accountant", "standard",
                     ["S33", "S04", "B39"], "Genjutsu", ("Intelligence", "Willpower")))

    def boss(name, key, sig, pool_kit, stat, gens, rules, pools=None):
        e = enemy(f, pool, name, key, "boss", pool_kit, stat, gens, rank="JONIN")
        d = e["data"]
        d["jutsus"] = [IDS[J[k]["srcId"]] for k in sig] + d["jutsus"]
        d["rules"], warn = f.rules(*rules, move)
        d["includeDefaultRules"] = False
        if pools:
            d["poolsMultiplier"] = pools
        out.append(e)

    boss("Tony Drumstick", "tony", ["clobber", "barrage", "family_business"],
         ["S42"], "Taijutsu", ("Strength", "Speed"), [
             gate_rule(f, J["family_business"]),
             gate_rule(f, J["clobber"]),
             gate_rule(f, J["barrage"]),
             pool_rule(f, pool, "S42"),
         ])
    boss("Vinny Drumstick", "vinny", ["wing_guard", "counter", "beatdown"],
         ["S41"], "Taijutsu", ("Strength", "Willpower"), [
             gate_rule(f, J["wing_guard"], H(60)),
             gate_rule(f, J["beatdown"]),
             gate_rule(f, J["counter"]),
             pool_rule(f, pool, "S41"),
         ])
    boss("Don Giblet", "giblet",
         ["interest", "collection_day", "feather_tax"],
         ["S34", "S28"], "Genjutsu", ("Intelligence", "Willpower"), [
             pool_rule(f, pool, "S34", H(50)),                      # Emergency Audit
             gate_rule(f, J["collection_day"], f.condition(
                 "target_has_effect", effectType="increasedamagetaken",
                 threshold=15, target="CLOSEST_OPPONENT")),
             gate_rule(f, J["interest"]),
             gate_rule(f, J["feather_tax"]),
             pool_rule(f, pool, "S28"),                             # Golden Avalanche (slow)
         ])
    boss("The Gobblefather", "gobblefather",
         ["drumsticks", "final_feast", "omerta"],
         ["B23", "A3", "S27", "S42"], "Ninjutsu", ("Strength", "Willpower"), [
             gate_rule(f, J["omerta"], H(35)),                      # phase 3
             gate_rule(f, J["final_feast"], H(35)),
             gate_rule(f, J["drumsticks"], H(70)),                  # phase 2
             pool_rule(f, pool, "A3", H(70)),                       # Gravy Release (area)
             pool_rule(f, pool, "B23"),                             # Family Protection
             pool_rule(f, pool, "S27"),                             # An Offer (weaken), phase 1
             pool_rule(f, pool, "S42"),
         ], pools=3)
    return out


# -------------------------------------------------------------------- quest

def nar(stage, *lines):
    body = " <br>\n".join(lines)
    return f"<i> {stage} </i> <br> <br>\n{body}" if lines else f"<i> {stage} </i>"


# id -> (kind, payload). Dialog choices are (text, target).
GRAPH = [
    ("o1", "dialog", nar("Golden fields stretch along the Harvest Plains Trade Road. Goah Way crouches beside an empty merchant wagon, turning a black feather in his fingers.",
        '"Something strange is happening along the trade routes. Merchants are disappearing, harvests are being stolen, and apparently someone has introduced a Feather Tax. Find out who\'s behind it."'),
        [("I'll investigate the missing caravans.", "o2"),
         ("A Feather Tax? Seriously?", "o1a")]),
    ("o1a", "dialog", nar("Goah lets the feather drift to the ground.",
        '"I\'ve encountered many strange things in Seichi. A criminal organization of turkeys is certainly new."'),
        [("Then I'll go meet them.", "o2")]),
    ("o2", "dialog", nar("Further down the road, scattered corn and black feathers trail past overturned crates. A nervous merchant waves you over before you can ask."),
        [("Are you all right?", "o3")]),
    ("o3", "dialog", nar("Merchant Hachiro wrings his hands beside an empty cart.",
        '"They took everything! Corn, pumpkins, potatoes! One of them even took my lunch. They said the Family always eats first!"',
        '"Two big turkeys in black suits. They set up a tollgate past the bend."'),
        [("Show me where.", "o4")]),
    ("o4", "dialog", nar("A checkpoint built from stolen caravan crates blocks the road. A painted sign demands the Feather Tax. Behind it stand two enormous turkeys in matching black suits: Tony and Vinny Drumstick."),
        [("Step up to the tollgate.", "o5")]),
    ("o5", "dialog", nar("Tony taps an oversized drumstick against his palm. Vinny straightens his gold rings.",
        'Tony: "You wanna pass? You gotta pay. Pay the Feather Tax or become part of the pavement."',
        'Vinny: "Tony, be polite. We\'re conducting business."'),
        [("I'm not paying your ridiculous tax.", "b6"),
         ("Who exactly runs this operation?", "o5a")]),
    ("o5a", "dialog", nar("Vinny steps forward, smiling without warmth.",
        '"You don\'t ask questions about the Family. The Family asks questions about you."',
        'Tony: "Right. Sorry. PLEASE pay the Feather Tax."'),
        [("Still not paying.", "b6")]),
    ("b6", "battle", ["tony", "vinny"], "o6", "r6"),
    ("r6", "reset", "o5", "<i> You stagger back down the road, feathers in your hair. The tollgate still stands. </i>"),
    ("o6", "dialog", nar("The tollgate collapses in a heap of splintered crates. Tony lies flat on the road.",
        'Tony: "Tell the boss... we tried..."',
        'Vinny: "You just had to hit him with the drumstick, didn\'t you? Fine. Everything goes to Don Giblet at the Golden Silo."'),
        [("Then that's where I'm going.", "o7")]),
    ("o7", "dialog", nar("The Golden Silo towers over the plains, its storerooms stacked with stolen crates and barrels of corn. Feathered Enforcers and Corn Collectors guard the doors."),
        [("Clear the guards.", "b8")]),
    ("b8", "battle", ["enforcer", "enforcer", "collector", "collector"], "o9", "r8"),
    ("r8", "reset", "o7", "<i> The guards drive you back out of the Golden Silo. The stolen harvest stays locked inside. </i>"),
    ("o9", "dialog", nar("Behind the warehouse office door, a turkey in a burgundy waistcoat adjusts his spectacles over an open ledger: Don Giblet.",
        '"You\'ve caused considerable financial damage to our organization. Naturally, you\'ll be paying for it."'),
        [("Your operation is finished.", "b10"),
         ("Return the stolen supplies.", "o9b"),
         ("Can I negotiate a payment plan?", "o9a")]),
    ("o9a", "dialog", nar("Don Giblet does not look up from his ledger.",
        '"Certainly. Your first payment is due immediately. Your second was due yesterday."'),
        [("Then let's settle the account.", "b10")]),
    ("o9b", "dialog", nar("Don Giblet turns a page.",
        '"According to my records, you owe the Family a considerable amount of corn. Interest has already been applied."'),
        [("I don't owe you anything.", "b10")]),
    ("b10", "battle", ["giblet", "accountant", "accountant"], "o10", "r10"),
    ("r10", "reset", "o9", "<i> Debt Marks burn on your skin as you retreat from the Golden Silo. Don Giblet makes a note in his ledger. </i>"),
    ("o10", "dialog", nar("Don Giblet slumps over his desk, spectacles askew.",
        '"Impossible... My calculations were perfect... Who... who is going to balance the books?"',
        "His ledger lies open: the location of the Feathered Estate, and a grand feast planned for Thanksgiving."),
        [("Take the ledger.", "o11")]),
    ("o11", "dialog", nar("Beyond the cornfields, a mansion rises behind golden fences and stone turkey statues. A sign at the gate reads: PRIVATE PROPERTY. FAMILY ONLY."),
        [("Walk through the gate.", "o12")]),
    ("o12", "dialog", nar("Beneath red curtains and a portrait of an enormous turkey, the Gobblefather sits in a high-backed chair. A tiny chicken dozes on his lap.",
        '"You defeated my boys. You ruined my business. And now you\'ve come to my home. Tell me... what exactly do you want?"'),
        [("Return the harvest and end the Feather Tax.", "o12b"),
         ("Your criminal empire ends today.", "b13"),
         ("I came for Thanksgiving dinner.", "o12a")]),
    ("o12a", "dialog", nar("The Gobblefather's feathers bristle.",
        '"Dinner? DINNER? You walk into my home, insult my Family, and expect a seat at my table?"'),
        [("I'll take that as a no.", "b13")]),
    ("o12b", "dialog", nar("The Gobblefather strokes the tiny chicken and sighs.",
        '"You come to me on the day of my daughter\'s hatching... and you ask me to return my corn? Disrespectful."'),
        [("The harvest goes back to the villages.", "b13")]),
    ("b13", "battle", ["gobblefather", "enforcer", "enforcer"], "o14", "x"),
    ("o14", "dialog", nar("The Gobblefather falls backward into his enormous chair. His golden ring slips from his wing. He looks toward the tiny chicken on his desk.",
        '"Take care of the business..."',
        "He closes his eyes. After a moment, the chicken lets out a quiet cluck. The Gobblefather opens one eye.",
        '"...And don\'t forget the corn."'),
        [("Return the harvest to the villages.", "o15")]),
    ("o15", "dialog", nar("Back on the Harvest Plains Trade Road, wagons roll freely again. Goah Way watches the merchants pass.",
        '"The stolen harvest has been returned, and the merchants can travel safely again. I suppose Thanksgiving is saved. Though I never imagined I\'d witness an organized criminal empire run entirely by turkeys."'),
        [("At least everyone can enjoy their feast.", "o16"),
         ("I wonder who takes over the Family now.", "o15a")]),
    ("o15a", "dialog", nar("Goah glances back toward the distant estate.", '"I\'d rather not find out."'),
        [("Fair enough.", "o16")]),
    ("o16", "dialog", nar("The Harvest Plains return to normal. The Feather Tax is abolished, the stolen food is distributed among the villages, and Thanksgiving preparations resume throughout Seichi. The Feathered Family's reign has ended."),
        [("Happy Thanksgiving.", "win")]),
    ("win", "win", "The Feathered Family has fallen. The harvest is home and the Feather Tax is abolished."),
    ("x", "fail", "\"You should've taken the deal. Now the Family owns the harvest, the roads, and everything that comes through them. Happy Thanksgiving.\""),
]

QUEST_DESC = ("A criminal organization known as the Feathered Family has seized control of the Harvest Plains, "
              "stealing Thanksgiving supplies and imposing a ridiculous Feather Tax on Seichi's merchants. "
              "Investigate the missing caravans, defeat the syndicate's enforcers, and confront the mysterious "
              "Gobblefather before he claims the entire harvest.")
QUEST_SUCCESS = ("The Feathered Family's criminal empire has collapsed. The stolen harvests have been recovered, "
                 "the Feather Tax has been abolished, and Thanksgiving celebrations can continue throughout Seichi. "
                 "The Gobblefather's reign has ended, but somewhere among the scattered feathers, a familiar voice "
                 "mutters that the Family never forgets.")


def build_objectives(f):
    objs = []
    for node in GRAPH:
        nid, kind = node[0], node[1]
        if kind == "dialog":
            objs.append(f.objective(
                "dialog", id=nid, description=node[2],
                nextObjectiveId=[{"text": t, "nextObjectiveId": n} for t, n in node[3]],
                attackers=[], attackers_scaled_to_user=False))
        elif kind == "battle":
            counts = {}
            for k in node[2]:
                counts[k] = counts.get(k, 0) + 1
            objs.append(f.objective(
                "start_battle", id=nid,
                opponentAIs=[{"ids": [f"@ai:{P}_ai_{k}"], "number": n, "quantity": 1}
                             for k, n in counts.items()],
                opponent_scaled_to_user=SCALED_TO_USER, keepOriginalPools=False,
                completionOutcome="Win", nextObjectiveId=node[3],
                failObjectiveId=node[4]))
        elif kind == "reset":
            objs.append(f.objective("reset_quest", id=nid, resetObjectiveId=node[2],
                                    description=node[3]))
        elif kind in ("win", "fail"):
            objs.append(f.objective("InstantWinLoseObjective", id=nid,
                                    task=f"{kind}_quest", successDescription=node[2],
                                    description=node[2]))
    return objs


def build_quest(f, objectives):
    q = _quest(f, objectives)
    # RUL: unlimited tries. Upstream QUEST_LIMIT_UNLIMITED is -1 and the live quests.update schema
    # takes minimum -1 (connector read 2026-11-25); the pinned 45d still says min 0, so the
    # factory cannot construct it. Set after construction; the pin needs a re-extract (Lane A).
    q["data"]["maxAttempts"] = -1
    # Fields the live quests.update schema requires that the pinned 45d predates (connector read
    # 2026-11-25), at the values the live Skyglass records carry (push/611/612 read-backs).
    d = q["data"]
    # teamMaxPlayers / raidMaxPlayers are left to the server default: Forge's pinned schema does
    # not know them yet and the first refused jutsu.update showed that JSON-schema "required" lists
    # defaulted fields too (animationScale was absent and not reported).
    d.update(publicLocations=False, teamEnabled=False)
    c = d["content"]
    c.update(isolated=False, entryItems=[], rewardMode="all", rewardPickCount=1)
    for k, v in (("reward_hunter_items", False), ("reward_hunter_items_ids", []),
                 ("reward_gathering_items", False), ("reward_gathering_items_ids", []),
                 ("reward_seichi_silver", 0)):
        c["reward"].setdefault(k, v)
    for o in c["objectives"]:
        o.setdefault("reward_hunter_items", False)
        o.setdefault("reward_gathering_items", False)
        if o["task"] == "start_battle":
            o.setdefault("applyBuffs", [])
            o.setdefault("applyDebuffs", [])
    return q


def _quest(f, objectives):
    return f.entry("quest", "create", name="The Gobblefather", srcId=f"{P}_quest", data={
        "name": "The Gobblefather",
        "questType": "event",
        "questRank": "S",
        "requiredLevel": 75,
        "consecutiveObjectives": True,
        "hidden": True,
        "description": QUEST_DESC,
        "successDescription": QUEST_SUCCESS,
        "startsAt": START, "endsAt": END,
        "maxAttempts": 100,  # overwritten to -1 below
        "maxCompletes": 1,
        "tierLevel": None,
        "petTaskMinutes": None,
        **{f"required{m}Mastery": None for m in ("Bloodline", "Bukijutsu", "Genjutsu",
                                                  "Ninjutsu", "Sage", "Taijutsu")},
        "content": {
            "objectives": objectives,
            "reward": {
                "reward_exp": 18000,
                "reward_money": 15000,
                "reward_prestige": 600,
                "reward_tokens": 500,
                "reward_clanpoints": 600,
            },
            "sceneBackground": "",
            "sceneCharacters": [],
        },
    })


# ----------------------------------------------------------------- checks

def verify(man):
    items = man["items"]
    assert all(i["data"].get("hidden") is True for i in items)
    srcs = {i["srcId"] for i in items}
    blob = json.dumps(man, ensure_ascii=False)
    import re
    for ref in re.findall(r"@(?:ai|jutsu):([A-Za-z0-9_]+)", blob):
        assert ref in srcs, f"dangling ref {ref}"
    q = items[-1]["data"]
    objs = q["content"]["objectives"]
    ids = [o["id"] for o in objs]
    assert len(ids) == len(set(ids))
    edges = []
    for o in objs:
        n = o.get("nextObjectiveId")
        if isinstance(n, list):
            targets = [c["nextObjectiveId"] for c in n]
            assert len(targets) == len(set(targets)), f"{o['id']}: choices share a target"
            edges += targets
        elif n:
            edges.append(n)
        if o.get("failObjectiveId"):
            edges.append(o["failObjectiveId"])
        if o["task"] == "dialog":
            for d in ("—", "–"):
                assert d not in o["description"] and all(d not in c["text"] for c in n), o["id"]
    assert not set(edges) - set(ids), set(edges) - set(ids)
    starts = [i for i in ids if i not in edges]
    assert starts == ["o1"], starts
    by = {o["id"]: o for o in objs}
    for o in objs:
        if o["task"] == "start_battle":
            gates = [p for p in objs if isinstance(p.get("nextObjectiveId"), list)
                     and any(c["nextObjectiveId"] == o["id"] for c in p["nextObjectiveId"])]
            assert gates and all(g["task"] == "dialog" for g in gates), o["id"]
            assert o["failObjectiveId"]
        if o["task"] == "reset_quest":
            assert by[o["resetObjectiveId"]]["task"] == "dialog"
    for i in items:
        if i["entity"] == "ai":
            d = i["data"]
            ids_ok = set(d["jutsus"])
            for r in d["rules"]:
                j = r["action"].get("jutsuId")
                assert j is None or j in ids_ok, (i["name"], j)
            assert d["rules"][-1]["action"]["type"] == "move_towards_opponent"


# Live contract drift (connector read 2026-11-25, jutsu.update schema): upstream's mastery rework
# removed statClassification "Highest" (now None|Ninjutsu|Genjutsu|Taijutsu|Bukijutsu) and the
# effects' statTypes, and added animationScale on every effect. The pinned 45c/45d predate it
# (sentinel drift since 2026-11-22), so the factory still builds the old shape. Re-expressed here
# to match the live pool records (S42: statClassification None, no statTypes, animationScale set).
# The first 622 run created Concrete Clobber's row (Xiv4MSyDT2fy56Rs4LBpr) and was refused on the
# update, so that item is now an update of the row it made rather than a second create.
CLOBBER_ID = "Xiv4MSyDT2fy56Rs4LBpr"


def livefix_jutsu(entry):
    d = entry["data"]
    d["statClassification"] = "None"
    for e in d["effects"]:
        e.pop("statTypes", None)
        e.setdefault("animationScale", 1)
    if entry["srcId"] == f"{P}_j_clobber":
        entry["slot"] = "edit"
        entry["targetId"] = CLOBBER_ID
    return entry


def write(path, man):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    kinds = {}
    for i in man["items"]:
        kinds[i["entity"]] = kinds.get(i["entity"], 0) + 1
    print(f"{path}: {kinds}")


def main():
    """No args: push/622 (jutsu creates).
    --ids <622 results bundle>: push/623 (AI + quest) with literal jutsu ids.
    --dry: 623 with stand-in ids to /tmp, for validate.py only (never pushed)."""
    args = sys.argv[1:]
    f = Factory(ctors=CTORS, entities=ENTS, checks=CHECKS)
    pool = load_pool(POOL)
    J = build_jutsu(f)
    if not args:
        man = f.manifest(list(J.values()))
        man["items"] = [livefix_jutsu(i) for i in man["items"]]
        write(OUT_J, {
            "_note": "push/622: The Gobblefather (Thanksgiving 2026) step 1 of 2, 12 AI jutsu, HIDDEN. "
                     "Keep the results bundle: push/623 (AI + quest) is built from it with --ids. "
                     "Generated by push/622_gobblefather_core.gen.py; do not hand-edit.",
            "_placeholders": PLACEHOLDERS, "dedupNames": True, "items": man["items"]})
        return
    if args[0] == "--ids":
        im = dict(json.load(open(args[1])).get("idmap") or {})
        im.setdefault(f"{P}_j_clobber", CLOBBER_ID)
        missing = [j["srcId"] for j in J.values() if j["srcId"] not in im]
        if missing:
            raise SystemExit(f"bundle has no id for {missing}: run push/622 first")
        IDS.update({j["srcId"]: im[j["srcId"]] for j in J.values()})
        out = OUT_A
    elif args[0] == "--dry":
        IDS.update({j["srcId"]: "DRY" + format(n, "018d") for n, j in enumerate(J.values())})
        out = "/tmp/623_gobblefather_ai_quest.dry.json"
    else:
        raise SystemExit(main.__doc__)
    ais = build_ai_entries(f, pool, J)
    quest = build_quest(f, build_objectives(f))
    # A quest created through quests.create starts as "mission"; updating it to "event" makes
    # the server assign it to every active player of the rank (TheNinjaRPG quests.ts update,
    # "Assign a quest that just became an event"), hidden or not. So the quest is a clone of a
    # hidden staff event quest (Driftline Hand Test (staff), JTdR6SSYLs62S-3l6O26J), made over the
    # connector, and this job edits that clone in place: its type never changes.
    if "--quest-id" in args:
        qid = args[args.index("--quest-id") + 1]
        quest["slot"] = "edit"
        quest["targetId"] = qid
    man = {
        "_note": "push/623: The Gobblefather step 2 of 2, 7 AI + quest, HIDDEN, literal jutsu ids from push/622. "
                 "Generated by push/622_gobblefather_core.gen.py --ids; do not hand-edit.",
        "_placeholders": PLACEHOLDERS, "dedupNames": True,
        "items": f.manifest(ais + [quest])["items"],
    }
    verify(man)
    write(out, man)
    if out == OUT_A:
        # validate.py still carries law 14's preferredStat; the game removed the field and Forge
        # refuses it. Ledgered under RUL-2026-10-25-009, exactly as push/262/272/344.
        import hashlib
        led = os.path.join(ROOT, "state", "validate_exceptions", "623_gobblefather_ai_quest.json")
        with open(led, "w", encoding="utf-8") as fh:
            json.dump({
                "manifest": "push/623_gobblefather_ai_quest.json",
                "ruling": "RUL-2026-10-25-009",
                "reason": "validate.py law 14 / L05 demands preferredStat on an AI create; the game's AI "
                          "schema no longer has preferredStat (removed upstream) and Forge refuses the key as unknown",
                "sha256": hashlib.sha256(open(out, "rb").read()).hexdigest(),
                "accepted": [f"ERROR  [ai:{i['name']}]: law 14: AI create missing required field "
                             f"'preferredStat' (builder lint L05 rejects this)"
                             for i in man["items"] if i["entity"] == "ai"],
            }, fh, indent=1)
            fh.write("\n")
        print(led)


if __name__ == "__main__":
    main()
