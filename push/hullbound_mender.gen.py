#!/usr/bin/env python3
"""The Hullbound Mender: Chart of the Closing Hold, a Skyglass legendary chart run (director 2026-11-09), all HIDDEN.

    python3 push/hullbound_mender.gen.py jutsu                          # write push/575 (jutsu + chart item)
    python3 push/hullbound_mender.gen.py fix --jutsu <575 bundle>       # write push/578 (edit the 2 Keel Splits 575 left blank)
    python3 push/hullbound_mender.gen.py art --jutsu <575 bundle> --uploaded <uploaded.json>   # push/579: v2 clips
    python3 push/hullbound_mender.gen.py ais --jutsu <575 bundle> --fix <578 bundle>   # write push/576, AFTER 575 and 578
    python3 push/hullbound_mender.gen.py quest --ais <576 bundle> --jutsu <575 bundle> --fix <578 bundle>   # push/577
    python3 push/hullbound_mender.gen.py check                          # offline: rule cadence and tile sets

Design of record: docs/design/SKYGLASS_MENDER_PITCH.md (approved for the Nov 13 release; renamed from Okabe). Hull tile
effects proven live on 2026-11-09 (push/539, 539b): seal, healprevent, buffprevent and increasedamagetaken 40 all land
on whoever stands on a hull tile and drop the moment they step off.

How his turn works (engine: app/src/libs/combat/ai_v2.ts, one action per pass, first rule that is ready, affordable and
true). A mark puts a 1-round marker effect on him; a payoff rule fires on that marker. The action costs keep every
promise exactly one turn away:
    payoff 35   close 34   tier mark 67   mark 66   rivet 33
    mark + payoff = 101 and tier mark + close = 101, so nothing lands on the turn it is marked;
    close + mark = 100, payoff + rivet = 68, mark + rivet = 99, tier mark + rivet = 100.
So a turn is one of: a mark and a rivet; a payoff and a rivet; a tier mark and a rivet; a close and a new mark.
The tiers no longer eat a payoff turn (the pitch's 40/60 split did; push/hullbound_mender.gen.py check shows both).

Marker effects (on him only, harmless to him): Port increaserange, Starboard fleeprevent, Planks robprevent, tier mark
increaseheal; each close adds summonprevent 25 for 100 rounds, so "closed >= k" is summonprevent >= 25k; a Splitter
break leaves decreasepoolcost 1 for 2 rounds, which puts Planks first on his next mark (Splitter and Hammerfall
alternate instead of the tiers starving the Hammerfall).

Art: every effect carries the live Skyglass danger-language strips as STAND-INS (tg_* from push/431, ERUPTION) so the
hidden test reads. The Mender's own clips (art/hullbound_mender_fx/exports, commit 8041ebb) and his avatar go up in the
browser (the MCP host cannot upload), then an art pass swaps them in with the law-18 unequip, edit, re-equip cycle.
Do not hand-edit the output.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")
NUM = {"jutsu": 575, "ais": 576, "quest": 577, "fix": 578, "art": 579}
PFX = {"jutsu": "sg575_", "ais": "sg576_"}

COLS, ROWS = 12, 10            # quest arena at level 40+ (combat battleMaps; pitch section 8)
CENTER = (5, 4)                # his post: inside the last 4x2 of safe floor
COST = {"payoff": 35, "close": 34, "tier": 67, "mark": 66, "rivet": 33}

# Live ids (verified 2026-11-09: profile.getAi reads of the three source crew; item ids from push/skyglass_new_charts and
# push/skyglass_charts.gen.py)
AVATAR = {
    "apprentice": "https://ui0arpl8sm.ufs.sh/f/lzAi8J-6y6bxAPPyL3POX.webp",   # Veteran Foundry Warden
    "caulker": "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261019-v3-texZaFi42S3EvJZBwQ8cd-main-eded2d557ed1.webp",  # Vet Deck Warden
    "pump": "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261019-v3-d6g0mOM7RBSsYI1hrUVT9-main-ae7a2d4e4029.webp",  # Vet First Blade
    "mender": "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp",  # placeholder until upload
}
POOL_JUTSU = {"Quick Strike": "FeYnH7BBw_usnc1K-TM-J", "Tide Bolt": "UnQKfwq_JoRVu10aTX6Uv"}  # live, equipped as-is
HEAVY_ARMOR = "h-V9uiuxbL7lAWkO6nZWt"   # AI Heavy Armor, as the Mother of Echoes bosses carry
ITEM = {
    "Skyglass Coffer": "THo7rfzP-S82_43aN8fs3", "Sealed Treasury": "Ma8S90Nmbi0Xvm4u4FzJh",
    "Skyglass Token": "nzCW7A-_AuYMzBs2wClnM", "Galley Stores": "D-QTnbjgTyIVc593zzdSB",
    "Core Rot": "KuqLeFB12BdB-0s5O1udk", "Lastlight Lantern": "jCJv4N3JSiihuqnK0jJ7t",
    "Shard of the Keel": "uKnlqlfyE_k1QjLuaVml_",
}
SCENE = {  # push/skyglass_hunts.gen.py SCENE (uploaded boards)
    "lower_hull": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi",
    "hold": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH",
    "reconstruction_chamber": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJRiFRQZ0udmODoNtpa0FMcwI4k2Eq7nJhyvjl",
}
CHART_ICON = "https://ui0arpl8sm.ufs.sh/f/GnbyPivtXnCa3YLP97KfO.webp"   # placeholder (the Glass Nursery chart icon)
PLACEHOLDER = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"

# Live Skyglass danger-language strips (push/431), stand-ins until the Mender's clips are uploaded.
APPEAR, VANISH = "bJy2IjRKmAVYEoXUYmXv5", "k8J4ic-KEz9ewEq1gAszr"
ERUPTION = "Z9j8J7ZmAjiaxH2S4nDy8"
TG = {
    "heavy": {"staticAssetPath": "dGCN9ZaoyXwDK9E3ZuWgU", "staticAnimation": "dL1vh_PNbZQ9m6nYwGnFa",
              "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "control": {"staticAssetPath": "M2oqurvH5jYkuCeDafnFK", "staticAnimation": "ZZ2YrtIAxfnlHAzOHXSgl",
                "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "safe": {"staticAssetPath": "-hIV18piGe0EcC0u6eN8d", "staticAnimation": "v9nA0cPU5NXxBXoONhdLH",
             "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "linger": {"staticAssetPath": "PoG_KDERWlvyj7MsKSDW2", "staticAnimation": "qlGYJizxxxdd794Jea6lB",
               "appearAnimation": APPEAR, "disappearAnimation": ""},
    "hit": {"staticAssetPath": "", "staticAnimation": "", "appearAnimation": ERUPTION, "disappearAnimation": ""},
    "none": {"staticAssetPath": "", "staticAnimation": "", "appearAnimation": "", "disappearAnimation": ""},
}

# Damage (first pass; measured and tuned on the hidden test before anything goes live, as with the Mother of Echoes).
# damage = calcHP(100)/10 * power/40 * stat advantage, linear in power (tags.ts damageCalc, powerEffect).
POWER = {"rivet": 20, "splitter": 220, "hammerfall": 310, "seal": 2000,
         "loose_rivet": 12, "apprentice_mallet": 160, "crew_splitter": 110}
PLANK_DR = 75        # Fresh Plank: 75% less damage taken (not pierce)
HULL_TAKEN = 40      # glass-grown hull: +40% damage taken (not pierce)
HULL_ROUNDS = 100
TIERS = [  # (tier, health_below, round_greater_than): marks on whichever comes first; tier 4 is the round-15 enrage
    (1, 75, 3), (2, 50, 7), (3, 25, 11), (4, None, 14)]
SEAL_ROUND = 17      # round_greater_than 17: the hold seals on round 18


# ---------------------------------------------------------------------------------------------------------------
# Tiles
# ---------------------------------------------------------------------------------------------------------------
def ring(c, r):
    return min(c, COLS - 1 - c, r, ROWS - 1 - r)


ALL = [(c, r) for c in range(COLS) for r in range(ROWS)]
BAND = {k: [t for t in ALL if ring(*t) == k - 1] for k in range(1, 5)}
PORT = [t for t in ALL if t[0] <= 5]
STARBOARD = [t for t in ALL if t[0] >= 6]
PLANKS_A = [t for t in ALL if ring(*t) >= 3 and t != CENTER]   # the 6x4 floor left after tier 3
PLANKS_B = [t for t in ALL if ring(*t) >= 4 and t != CENTER]   # the 4x2 floor left after tier 4


def coords(tiles):
    return [{"longitude": c, "latitude": r} for c, r in sorted(tiles)]


# ---------------------------------------------------------------------------------------------------------------
# Effects
# ---------------------------------------------------------------------------------------------------------------
def fx(art="none", **kw):
    e = dict(TG[art])
    e.update({"appearSfx": "", "disappearSfx": "", "powerPerLevel": 0, "direction": "offence"})
    e.update(kw)
    return e


def dmg(power, kind="damage", art="hit"):
    return fx(art, rounds=0, power=power, target="INHERIT", friendlyFire="ENEMIES", calculation="formula",
              statTypes=["None"], type=kind, description="Deals damage to target", residualModifier=1, dmgModifier=1,
              allowBloodlineDamageIncrease=True, allowBloodlineDamageDecrease=True)


def tele(art, desc):   # the omen tile: +1% out-of-combat regen to his own side only, the live telegraph carrier
    return fx(art, rounds=1, power=1, target="INHERIT", friendlyFire="FRIENDLY", calculation="percentage",
              type="increaseregeneration", description=desc)


def marker(kind, power=1, rounds=1, desc="placeholder"):
    e = fx("none", rounds=rounds, power=power, target="SELF", calculation="static", type=kind, description=desc)
    if kind == "increaserange":
        e["actionsAffected"] = []
    if kind in ("decreasepoolcost", "increasepoolcost"):
        e["direction"] = "defence"   # the server's pool-cost tags only take direction "defence" (refused live 2026-11-09)
    return e


def hull(kind, desc, art="none", power=100, calc="static"):
    return fx(art, rounds=HULL_ROUNDS, power=power, target="INHERIT", friendlyFire="ENEMIES", calculation=calc,
              type=kind, description=desc)


# ---------------------------------------------------------------------------------------------------------------
# Jutsu
# ---------------------------------------------------------------------------------------------------------------
JUTSU_BASE = {
    "extraBaseCost": 0, "bloodlineId": "", "requiredLevel": 1, "requiredRank": "STUDENT", "jutsuType": "AI",
    "image": PLACEHOLDER, "jutsuWeapon": "NONE", "statClassification": "None", "elementClassification": "None",
    "jutsuRank": "D", "staminaCost": 0.05, "chakraCost": 0.05, "staminaCostReducePerLvl": 0,
    "chakraCostReducePerLvl": 0, "healthCostReducePerLvl": 0, "healthCost": 0, "villageId": "", "hidden": True,
    "injectableInBattle": False, "battleUsageType": "BOTH",
}
JUTSU = {}   # key -> manifest data


def jutsu(key, name, desc, log, effects, cost, cooldown, tiles=None, target="GROUND", method="COORDINATES",
          selection="ALL", random_count=None, rng=0):
    d = dict(JUTSU_BASE, name=name, description=desc, battleDescription=log, effects=effects, actionCostPerc=cost,
             cooldown=cooldown, target=target, method=method, range=rng)
    if method == "COORDINATES":
        ct = {"origin": "BATTLEFIELD", "selection": selection, "coordinates": coords(tiles)}
        if random_count:
            ct["randomCount"] = random_count
        d["coordinateTargeting"] = ct
    JUTSU[key] = d


def build_jutsu():
    # The Mender's steady attack and his two telegraphed payoffs
    jutsu("rivet", "Rivet Volley", "The Hullbound Mender's steady attack: three skyglass rivets, wherever you stand.",
          "%user thumbs three skyglass rivets from his pouch and drives them into %target.",
          [dmg(POWER["rivet"])], COST["rivet"], 1, ALL, target="CHARACTER")
    jutsu("port_mark", "Keel Splitter: Port", "Marks the port half of the hold (the left six columns). It splits next turn.",
          "%user snaps a chalk line down the keel. \"Port side.\"",
          [tele("control", "Telegraph: the port half splits next turn"), marker("increaserange")],
          COST["mark"], 8, PORT)
    jutsu("starboard_mark", "Keel Splitter: Starboard",
          "Marks the starboard half of the hold (the right six columns). It splits next turn.",
          "%user snaps a chalk line down the keel. \"Starboard side.\"",
          [tele("control", "Telegraph: the starboard half splits next turn"), marker("fleeprevent", 100)],
          COST["mark"], 8, STARBOARD)
    after = marker("decreasepoolcost", 1, 2, "The Mender reaches for fresh planks")
    jutsu("port_break", "Keel Splits: Port", "Pierces everyone on the port half the chalk line marked.",
          "The deck splits along the chalk line, and the port side bursts up in splinters and glass.",
          [dmg(POWER["splitter"], "pierce"), after], COST["payoff"], 2, PORT, target="CHARACTER")
    jutsu("starboard_break", "Keel Splits: Starboard", "Pierces everyone on the starboard half the chalk line marked.",
          "The deck splits along the chalk line, and the starboard side bursts up in splinters and glass.",
          [dmg(POWER["splitter"], "pierce"), dict(after)], COST["payoff"], 2, STARBOARD, target="CHARACTER")
    plank = fx("safe", rounds=2, power=PLANK_DR, target="INHERIT", friendlyFire="ENEMIES", calculation="percentage",
               type="decreasedamagetaken", description="Fresh Plank: 75% less damage from the mallet")
    jutsu("planks_a", "Fresh Planks", "Lays three warm new planks inside the hold. Stand on one before he swings.",
          "%user lays fresh planks across the deck, warm from the saw. He lifts the mallet.",
          [plank, marker("robprevent", 100)], COST["mark"], 4, PLANKS_A, target="EMPTY_GROUND", selection="RANDOM",
          random_count=3)
    jutsu("planks_b", "Last Planks", "Lays two warm new planks on the last of the floor. Stand on one before he swings.",
          "%user lays his last two planks. He lifts the mallet.",
          [dict(plank), marker("robprevent", 100)], COST["mark"], 4, PLANKS_B, target="EMPTY_GROUND",
          selection="RANDOM", random_count=2)
    jutsu("hammerfall", "Hammerfall", "Slams the whole deck. A fresh plank takes most of it; the hull makes it worse.",
          "%user brings the mallet down on the deck, and the whole hold rings.",
          [dmg(POWER["hammerfall"])], COST["payoff"], 2, ALL, target="CHARACTER")
    # The hold closes: one omen and one close per tier
    for k in range(1, 5):
        jutsu(f"tier{k}_mark", f"The Hold Groans {['I', 'II', 'III', 'IV'][k - 1]}",
              "Seams of light open in the next band of the hold. It becomes hull next turn.",
              "The timbers groan. Seams of cold light open between the planks at the edge of the hold.",
              [tele("heavy", "Telegraph: this band becomes hull next turn"), marker("increaseheal")],
              COST["tier"], 100, BAND[k])
        close = [hull("seal", "Hull: bloodline sealed"),
                 hull("healprevent", "Hull: no healing", art="linger"),
                 hull("buffprevent", "Hull: no new buffs"),
                 hull("increasedamagetaken", "Hull: +40% damage taken", power=HULL_TAKEN, calc="percentage"),
                 marker("summonprevent", 25, 100, "The hold has closed in")]
        if k == 3:
            close.append(fx("none", rounds=100, power=10, target="SELF", calculation="percentage",
                            type="increasedamagegiven", description="The Mender works faster"))
        jutsu(f"tier{k}_close", f"The Hold Closes {['I', 'II', 'III', 'IV'][k - 1]}",
              "The marked band becomes glass-grown hull for the rest of the fight: sealed bloodline, no healing, no "
              "new buffs, +40% damage taken while you stand on it.",
              "Skyglass plates punch up through the deck and lock. The hold is smaller now.",
              close, COST["close"], 100, BAND[k])
    jutsu("seal", "The Hold Seals", "Round 18: the hold seals shut around whoever is still in it.",
          "%user sets the last rivet. \"Mind your feet.\" The hold seals shut.",
          [dmg(POWER["seal"], "pierce")], COST["payoff"], 0, ALL, target="CHARACTER")
    # The Mender's Apprentice
    jutsu("loose_rivet", "Loose Rivet", "The apprentice's steady attack.",
          "%user flings a loose rivet at %target.", [dmg(POWER["loose_rivet"])], COST["rivet"], 1, ALL,
          target="CHARACTER")
    jutsu("apprentice_mallet", "Apprentice's Mallet", "Slams the deck. A fresh plank takes most of it.",
          "%user swings a mallet too big for him into the deck.", [dmg(POWER["apprentice_mallet"])],
          COST["payoff"], 2, ALL, target="CHARACTER")
    # Bilge Crew: one side each, offset two rounds so the halves never split together
    for side, tiles, mk in (("port", PORT, marker("increaserange")), ("starboard", STARBOARD, marker("fleeprevent", 100))):
        Side = side.capitalize()
        jutsu(f"crew_{side}_mark", f"Bilge Line: {Side}", f"Marks the {side} half of the hold. It splits next turn.",
              f"%user snaps a tarred line across the bilge. \"{Side}!\"",
              [tele("control", f"Telegraph: the {side} half splits next turn"), mk], COST["mark"], 4, tiles)
        jutsu(f"crew_{side}_break", f"Bilge Split: {Side}", f"Pierces everyone on the {side} half the line marked.",
              f"The bilge boards split along the line, and the {side} side bursts.",
              [dmg(POWER["crew_splitter"], "pierce")], COST["payoff"], 2, tiles, target="CHARACTER")


# The Mender's own clips (v2, dauntless's "Looks good" 2026-11-09 17:39 UTC): 112 px one-hex strips, 24 x 50 ms, on the
# director's UploadThing (duet/moe-uploadthing state/moe_upload/uploaded.json, srcIds sg579_<key>). push/579 creates
# them as hidden ANIMATION assets and points the 575 kit at them by @scene ref.
CLIPS_V2 = ["a1_hull_omen", "a2_hull_close", "a2_hull_floor", "a3_split_omen", "a4_split_break", "a5_fresh_plank",
            "a6_hammerfall", "a7_rivet_volley", "a8_last_tier_aura"]
CLIP_NAME = {"a1_hull_omen": "omen, seams of light (loop)", "a2_hull_close": "hull closes, plates punch up",
             "a2_hull_floor": "glass-grown floor (loop)", "a3_split_omen": "chalk line (loop)",
             "a4_split_break": "the line splits", "a5_fresh_plank": "fresh plank (loop)", "a6_hammerfall": "hammerfall",
             "a7_rivet_volley": "rivet volley", "a8_last_tier_aura": "he works faster (loop)"}
HIT_CLIP = {"rivet": "a7_rivet_volley", "loose_rivet": "a7_rivet_volley", "port_break": "a4_split_break",
            "starboard_break": "a4_split_break", "crew_port_break": "a4_split_break",
            "crew_starboard_break": "a4_split_break", "hammerfall": "a6_hammerfall",
            "apprentice_mallet": "a6_hammerfall", "seal": "a6_hammerfall"}
ART_FIELDS = ("staticAssetPath", "staticAnimation", "appearAnimation", "disappearAnimation")


def apply_art(ref):
    """Swap the live stand-in strips for the Mender's clips. ref(key) -> asset id or @scene ref."""
    def put(e, static="", appear=""):
        e.update({"staticAssetPath": "", "staticAnimation": static and ref(static), "appearAnimation": appear and ref(appear),
                  "disappearAnimation": ""})
    changed = set()
    for k, d in JUTSU.items():
        before = json.dumps(d["effects"])
        for e in d["effects"]:
            t = e["type"]
            if t in ("damage", "pierce"):
                put(e, appear=HIT_CLIP[k])
            elif t == "increaseregeneration":                     # the telegraph tile
                put(e, static="a1_hull_omen" if k.startswith("tier") else "a3_split_omen")
            elif t == "decreasedamagetaken":                      # Fresh Plank
                put(e, static="a5_fresh_plank")
            elif t == "healprevent":                              # one carrier per hull tile
                put(e, static="a2_hull_floor", appear="a2_hull_close")
            elif t == "increasedamagegiven":                      # tier 3: he works faster
                put(e, static="a8_last_tier_aura")
            elif any(e.get(f) for f in ART_FIELDS):
                put(e)
        if json.dumps(d["effects"]) != before:
            changed.add(k)
    return changed


# ---------------------------------------------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------------------------------------------
def has(kind, threshold=1):
    return {"type": "has_effect", "effectType": kind, "threshold": threshold, "description": "Has effect"}


def health_below(v):
    return {"type": "health_below", "value": v, "description": "Health below given percentage"}


def round_gt(v):
    return {"type": "round_greater_than", "value": v, "description": "Current round is higher than specified value"}


def round_lt(v):
    return {"type": "round_lower_than", "value": v, "description": "Current round is lower than specified value"}


def dist_gt(v):
    return {"type": "distance_higher_than", "value": v, "target": "CLOSEST_OPPONENT",
            "description": "Distance higher than given value"}


def dist_lt(v):
    return {"type": "distance_lower_than", "value": v, "target": "CLOSEST_OPPONENT",
            "description": "Distance lower than or equal given value"}


def use(jid, conds=(), target="SELF"):
    return {"conditions": list(conds), "action": {"type": "use_specific_jutsu", "jutsuId": jid, "target": target,
                                                  "description": "Select specific jutsu"}}


def move_to(c, r, conds=()):
    return {"conditions": list(conds), "action": {"type": "move_towards_opponent", "target": "COORDINATE",
                                                  "coordinates": {"longitude": c, "latitude": r},
                                                  "description": "Take his post"}}


def chase(conds=()):
    return {"conditions": list(conds), "action": {"type": "move_towards_opponent", "target": "CLOSEST_OPPONENT",
                                                  "description": "Move towards opponent"}}


END = {"conditions": [], "action": {"type": "end_turn", "description": "End turn"}}
CLOSED = "summonprevent"     # 25 per closed tier


def mender_rules(J):
    rules = [use(J["seal"], [round_gt(SEAL_ROUND)]),
             move_to(*CENTER, [round_lt(2)]),
             # payoffs (35): whatever was marked last turn
             use(J["port_break"], [has("increaserange")]),
             use(J["starboard_break"], [has("fleeprevent")]),
             use(J["hammerfall"], [has("robprevent")])]
    # closes (34): the newest marked tier, gated on how many have closed
    for k in (4, 3, 2, 1):
        conds = [has("increaseheal")] + ([has(CLOSED, 25 * (k - 1))] if k > 1 else [])
        rules.append(use(J[f"tier{k}_close"], conds))
    # tier marks (67): health or round, whichever comes first, in order
    for k, hb, rg in TIERS:
        gate = [has(CLOSED, 25 * (k - 1))] if k > 1 else []
        if hb is not None:
            rules.append(use(J[f"tier{k}_mark"], gate + [health_below(hb)]))
        rules.append(use(J[f"tier{k}_mark"], gate + [round_gt(rg)]))
    # marks (66): planks right after a split, then the Splitter (Starboard from round 5), then planks
    rules += [use(J["planks_b"], [has("decreasepoolcost"), has(CLOSED, 100)]),
              use(J["planks_a"], [has("decreasepoolcost")]),
              use(J["starboard_mark"], [round_gt(4)]),
              use(J["port_mark"]),
              use(J["planks_b"], [has(CLOSED, 100)]),
              use(J["planks_a"]),
              use(J["rivet"]),      # 33, once a turn
              END]
    return rules


def apprentice_rules(J):
    return [use(J["apprentice_mallet"], [has("robprevent")]),
            use(J["tier1_close"], [has("increaseheal")]),
            use(J["tier1_mark"], [round_gt(2)]),
            use(J["planks_a"]),
            use(J["loose_rivet"]),
            END]


def crew_rules(J, side, delay):
    mk = "increaserange" if side == "port" else "fleeprevent"
    return [use(J[f"crew_{side}_break"], [has(mk)]),
            use(J[f"crew_{side}_mark"], [round_gt(delay)] if delay else []),
            use(POOL_JUTSU["Tide Bolt"], [dist_lt(6)], target="CLOSEST_OPPONENT"),
            use(POOL_JUTSU["Quick Strike"], [dist_lt(4)], target="CLOSEST_OPPONENT"),
            chase([dist_gt(2)]),
            END]


# ---------------------------------------------------------------------------------------------------------------
# AIs
# ---------------------------------------------------------------------------------------------------------------
STAT = 1391299.95   # the Mother of Echoes stat block (push/463)
MASTERY = 834780


def reuse_ids():
    """--reuse key=id,...: AIs a failed run already created blank; finish them by id instead of creating twins."""
    if "--reuse" not in sys.argv: return {}
    return dict(kv.split("=", 1) for kv in sys.argv[sys.argv.index("--reuse") + 1].split(","))


def ai(key, name, avatar, pools, stats_mult, effects, jutsus, rules, items=()):
    rid = reuse_ids().get(key)
    head = {"entity": "ai", "slot": "edit", "targetId": rid} if rid else {"entity": "ai", "slot": "create"}
    assert pools >= 1, "poolsMultiplier must be >= 1"
    return {**head, "srcId": PFX["ais"] + key, "phase": 1, "name": name, "data": {
        "avatarFacing": "left", "bloodlineMastery": 10, "bukijutsuMastery": MASTERY, "defence": STAT,
        "gender": "Unknown", "genjutsuMastery": MASTERY, "hidden": True, "includeDefaultRules": False,
        "intelligence": STAT, "isSummon": False, "level": 100, "ninjutsuMastery": MASTERY, "offence": STAT,
        "poolsMultiplier": pools, "preferredGeneral1": "Strength", "preferredGeneral2": "Willpower",
        "primaryElement": None, "rank": "JONIN", "regeneration": 60, "sageMastery": 10, "secondaryElement": None,
        "speed": STAT, "statsMultiplier": stats_mult, "strength": STAT, "taijutsuMastery": MASTERY,
        "username": name, "willpower": STAT, "effects": effects, "jutsus": list(dict.fromkeys(jutsus)),
        "items": list(items), "rules": rules, "avatar": avatar, "inArena": False}}


def innate(kind, power, desc, target="INHERIT", calc="percentage"):
    return fx("none", rounds=100, power=power, target=target, calculation=calc, type=kind, description=desc)


def build_ais(J):
    mender_kit = ["seal", "port_break", "starboard_break", "hammerfall"] + [f"tier{k}_{x}" for k in range(1, 5)
                                                                          for x in ("close", "mark")] + \
        ["planks_b", "planks_a", "starboard_mark", "port_mark", "rivet"]
    steady = [innate("stunprevent", 100, "Nothing knocks the Mender off his work"),
              innate("onehitkillprevent", 100, "placeholder", target="SELF", calc="static")]
    return [
        # poolsMultiplier must be >= 1 (profile.updateAi refused 0.8 on 2026-11-09), so at level 100 every AI has at
        # least 5,050 HP; the planned 4,040 and 2,525 are kept as effective HP with innate damage taken (+25%, +100%).
        ai("apprentice", "The Mender's Apprentice", AVATAR["apprentice"], 1, 5.83,
           list(steady) + [innate("increasedamagetaken", 25, "Green hands: takes 25% more damage")],
           [J[k] for k in ("apprentice_mallet", "tier1_close", "tier1_mark", "planks_a", "loose_rivet")],
           apprentice_rules(J)),
        ai("caulker", "Bilge Caulker", AVATAR["caulker"], 1, 5,
           [innate("increasedamagetaken", 100, "Bilge crew, no armour: takes double damage")],
           [J["crew_port_break"], J["crew_port_mark"], POOL_JUTSU["Tide Bolt"], POOL_JUTSU["Quick Strike"]],
           crew_rules(J, "port", 0)),
        ai("pump", "Bilge Pump Hand", AVATAR["pump"], 1, 5,
           [innate("increasedamagetaken", 100, "Bilge crew, no armour: takes double damage")],
           [J["crew_starboard_break"], J["crew_starboard_mark"], POOL_JUTSU["Tide Bolt"], POOL_JUTSU["Quick Strike"]],
           crew_rules(J, "starboard", 2)),
        ai("mender", "The Hullbound Mender", AVATAR["mender"], 3.2, 5.83, list(steady),
           [J[k] for k in mender_kit], mender_rules(J), items=[HEAVY_ARMOR]),
    ]


# ---------------------------------------------------------------------------------------------------------------
# Chart item and quest
# ---------------------------------------------------------------------------------------------------------------
CHART = "Chart of the Closing Hold"
QUEST = "The Closing Hold"
PICK = [("Skyglass Coffer", 2), ("Sealed Treasury", 1), ("Skyglass Token", 2), ("Galley Stores", 3)]
ENDING = [("Lastlight Lantern", 30), ("Core Rot", 40), ("Shard of the Keel", 50), ("Sealed Treasury", 6)]
EXP = 5000   # ladder step VI
FOOTER = ("<i>Spent when the run starts. No refills between fights; once inside, you leave by winning, falling or "
          "abandoning. Claim any waiting reward first.</i>")
ITEM_BASE = {
    "itemType": "OTHER", "slot": "NONE", "cooldown": 0, "weaponType": "NONE", "target": "SELF", "method": "SINGLE",
    "cost": 1, "repsCost": 0, "seichiSilverCost": 0, "stackSize": 999, "destroyOnUse": False, "range": 0,
    "chakraCost": 0, "staminaCost": 0, "healthCost": 0, "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
    "healthCostReducePerLvl": 0, "actionCostPerc": 60, "battleDescription": "Treasure chest", "canStack": True,
    "maxImbueNumber": 1, "maxDurability": 100, "inShop": False, "isEventItem": False, "hidden": True, "maxEquips": 1,
    "preventBattleUsage": True, "requiredLevel": 1, "xpToLevel": 1000, "parentItemId": None, "requiredStrength": None,
    "requiredSpeed": None, "requiredIntelligence": None, "requiredWillpower": None, "canBeCrafted": False,
    "canBeImbued": False, "canBeHunted": False, "canBeGathered": False, "canBeTraded": True, "isFarmSeed": False,
    "farmGrowTimeSeconds": 0, "farmYieldItemId": None, "farmMinLevel": 1, "farmPlantExperience": 0,
    "farmHarvestExperience": 0, "farmSellValue": 0, "farmExtractSeedItemId": None, "farmExtractSeedCount": 0,
    "isFarmFertilizer": False, "farmTimeReductionSeconds": 0, "farmFertilizerExperience": 0, "craftingExperience": 0,
    "crystalTargetTypes": None, "bloodlineId": None, "battleUsageType": "BOTH", "effects": [],
}  # push/536's chart create (tradeable, unusable in battle, hidden on create)


def chart_card():
    drops = " · ".join(f"{n} {p}%" for n, p in ENDING)
    picks = " · ".join(n + (f" ×{q}" if q > 1 else "") for n, q in PICK)
    return ("<i>A carpenter's plan of the lower hold, redrawn so many times the paper is more chalk than ink. Every "
            "wall on it has been moved inward.</i><br><br><b>The Closing Hold</b> · Battle Arena · level 40 and up<br>"
            "Difficulty: ★★★★☆<br><b>Chance drops:</b> " + drops + "<br><b>Choose two:</b> " + picks + "<br>" + FOOTER)


def chart_entry():
    data = dict(ITEM_BASE, name=CHART, description=chart_card(), rarity="LEGENDARY", image=CHART_ICON)
    return {"entity": "item", "slot": "create", "srcId": PFX["jutsu"] + "chart", "phase": 1, "name": CHART,
            "data": data}


SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the hold closes over it.",
          "fleeDescription": "You break away, and the hold closes behind you."}


def dialog(i, scene, desc, choice, nxt):
    return {"id": i, "task": "dialog", "description": desc, "sceneBackground": SCENE[scene], "sceneCharacters": [],
            "nextObjectiveId": [{"text": choice, "nextObjectiveId": nxt}]}


def battle(i, scene, desc, ai_ids, nxt):
    return {"id": i, "task": "start_battle", "description": desc, "sceneBackground": SCENE[scene],
            "sceneCharacters": [], "opponentAIs": [{"ids": [a], "number": 1, "quantity": 1} for a in ai_ids],
            "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False,
            "opponent_scaled_to_user": False, "nextObjectiveId": nxt, "failObjectiveId": "f_lost", **SHARED}


def quest_entry(A, chart_id):
    objs = [
        dialog("d_hatch", "lower_hull", "The lower hatch opens on a hold that is still being built. Somewhere below, a "
               "mallet is working, steady as a heartbeat, and the walls are a little closer every time it lands.",
               "Climb down", "b_apprentice"),
        battle("b_apprentice", "lower_hull", "The Mender's Apprentice looks up from his planks. \"You're standing where "
               "the wall goes.\"", [A["apprentice"]], "d_narrow"),
        dialog("d_narrow", "hold", "The hold is narrower than it was a minute ago. Two bilge hands are snapping tarred "
               "lines across the boards, and wherever a line lands, the deck splits.", "Cross the bilge", "b_crew"),
        battle("b_crew", "hold", "The Bilge Caulker and the Pump Hand call their sides.", [A["caulker"], A["pump"]],
               "d_keel"),
        dialog("d_keel", "reconstruction_chamber", "The keel room. A broad, stooped shipwright sets down a plank and "
               "turns around, a skyglass mallet on his shoulder. \"Mind your feet. The hull's coming in.\"",
               "Face the Hullbound Mender", "b_mender"),
        battle("b_mender", "reconstruction_chamber", "The Hullbound Mender lifts his mallet, and the hold begins to "
               "close.", [A["mender"]], "w_done"),
        {"id": "w_done", "task": "win_quest", "description": "The Mender lowers his mallet. \"...Leave it open. Just "
         "this once.\" The walls stop moving, and the hold's stores are yours.",
         "sceneBackground": SCENE["reconstruction_chamber"], "sceneCharacters": [], "reward_exp": EXP,
         "reward_items": [{"ids": [ITEM[n]], "number": p, "quantity": 1} for n, p in ENDING]},
        {"id": "f_lost", "task": "fail_quest", "description": "The hold closes over you, and the Mender goes back to "
         "his planks.", "sceneBackground": SCENE["lower_hull"], "sceneCharacters": []},
    ]
    reward = {"reward_items": [{"ids": [ITEM[n]], "number": 100, "quantity": q} for n, q in PICK]}
    return {"entity": "quest", "slot": "create", "srcId": "sg577_quest", "name": QUEST, "data": {
        "name": QUEST, "description": "Down in the lower hold, the ship's master carpenter is still mending. He mends "
        "the hold shut around anything that does not belong in it.\n\nClaim any reward choice still waiting from an "
        "earlier run before you set out.", "image": CHART_ICON, "questType": "battlepyramid", "questRank": "S",
        "successDescription": "You left the Hullbound Mender's hold before it closed.", "retryDelay": "none",
        "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True, "requiredLevel": 40, "maxLevel": 100,
        "maxAttempts": 100, "maxCompletes": 100, "prerequisiteQuestId": None, "tierLevel": None,
        "requiredVillage": None, "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objs, "sceneBackground": "", "sceneCharacters": [],
                    "entryItems": [{"ids": [chart_id], "number": 1}], "isolated": True, "rewardMode": "choose",
                    "rewardPickCount": 2, "reward": reward}}}


# ---------------------------------------------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------------------------------------------
def check_static():
    assert len(ALL) == 120 and [len(BAND[k]) for k in range(1, 5)] == [40, 32, 24, 16]
    assert len(PORT) == len(STARBOARD) == 60 and len(PLANKS_A) == 23 and len(PLANKS_B) == 7
    assert ring(*CENTER) == 4
    c = COST
    assert c["mark"] + c["payoff"] > 100 and c["tier"] + c["close"] > 100          # nothing lands the turn it is marked
    assert c["close"] + c["mark"] <= 100 and c["payoff"] + c["rivet"] <= 100
    assert c["mark"] + c["rivet"] <= 100 and c["tier"] + c["rivet"] <= 100
    assert c["payoff"] + c["tier"] > 100 and c["tier"] + c["mark"] > 100           # one new promise per turn
    for v in list(ITEM.values()) + list(POOL_JUTSU.values()) + [HEAVY_ARMOR]:
        assert NANO.match(v), v
    for d in JUTSU.values():
        n = len(d.get("coordinateTargeting", {}).get("coordinates", []))
        assert n <= 400 and len(d["name"]) <= 40, d["name"]
        for t in (d["description"], d["battleDescription"]):
            assert "—" not in t and "–" not in t, d["name"]


def check_graph(objs):
    by = {o["id"]: o for o in objs}
    seen, todo = set(), [objs[0]["id"]]
    while todo:
        i = todo.pop()
        if i in seen:
            continue
        seen.add(i)
        o = by[i]
        nxt = o.get("nextObjectiveId")
        nxts = [x["nextObjectiveId"] for x in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])
        if o.get("failObjectiveId"):
            nxts.append(o["failObjectiveId"])
        for n in nxts:
            assert n in by, (i, n)
            todo.append(n)
    assert seen == set(by)
    for o in objs:
        assert "—" not in o["description"] and "–" not in o["description"], o["id"]


FIX_KEYS = ("port_break", "starboard_break")   # failed in 575 (pool-cost direction); finished by 578 edits


def ids_from_bundle(path, prefix, keys, fix=None):
    b = json.load(open(path))
    out = {}
    for e in b["entries"]:
        src = e.get("srcId") or ""
        if src.startswith(prefix):
            k = src[len(prefix):]
            if e["state"] != "ok" and fix is not None and k in FIX_KEYS:
                continue
            assert e["state"] == "ok" and NANO.match(e["id"]), (src, e.get("state"))
            out[k] = e["id"]
    if fix is not None:   # the 578 edit bundle: same ids, now saved with the fixed effects
        idmap = b["idmap"]
        for e in json.load(open(fix))["entries"]:
            k = (e.get("srcId") or "")[len("sg578_"):]
            if k in FIX_KEYS:
                assert e["state"] == "ok" and e["id"] == idmap[prefix + k], (k, e.get("state"))
                out[k] = e["id"]
    missing = set(keys) - set(out)
    assert not missing, missing
    return out


def fix_arg():
    return sys.argv[sys.argv.index("--fix") + 1] if "--fix" in sys.argv else None


def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/hullbound_mender.gen.py; do not hand-edit.", "dedupNames": True}
    m.update(extra or {})
    m["items"] = items
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(path, ROOT), len(items), "items")


def main():
    build_jutsu()
    check_static()
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "check":
        print("tiles and costs OK;", len(JUTSU), "jutsu")
        return
    if mode == "jutsu":
        items = [{"entity": "jutsu", "slot": "create", "srcId": PFX["jutsu"] + k, "phase": 1, "name": d["name"],
                  "data": d} for k, d in JUTSU.items()] + [chart_entry()]
        write(NUM["jutsu"], "hullbound_mender_jutsu",
              "push/575, HIDDEN: the Hullbound Mender's kit (Chart of the Closing Hold, director 2026-11-09, Nov 13 "
              "release): the Mender's Rivet Volley, Keel Splitter (Port/Starboard marks and breaks), Fresh/Last Planks "
              "and Hammerfall, four hold tiers (omen and close: seal, healprevent, buffprevent, +40% damage taken), "
              "The Hold Seals (round 18); the Apprentice's Loose Rivet and Mallet; the Bilge Crew's lines; and the "
              "chart item (Legendary, placeholder icon). Art fields carry live Skyglass stand-ins until the Mender's "
              "clips are uploaded in the browser.", items)
        return
    if mode == "fix":
        idmap = json.load(open(sys.argv[sys.argv.index("--jutsu") + 1]))["idmap"]
        items = [{"entity": "jutsu", "slot": "edit", "targetId": idmap[PFX["jutsu"] + k], "srcId": "sg578_" + k,
                  "phase": 1, "name": JUTSU[k]["name"], "data": JUTSU[k]} for k in FIX_KEYS]
        write(NUM["fix"], "hullbound_mender_keel_fix",
              "push/578, HIDDEN: finishes the two Keel Splits that 575 created blank (the pool-cost marker needed "
              "direction defence). Edits by id; no AI equips them yet, so no equip link to sever.", items)
        return
    if mode == "art":
        idmap = json.load(open(sys.argv[sys.argv.index("--jutsu") + 1]))["idmap"]
        urls = json.load(open(sys.argv[sys.argv.index("--uploaded") + 1]))["files"]
        assets = [{"entity": "asset", "slot": "create", "phase": 1, "srcId": "sg579_" + c,
                   "name": "Hullbound Mender - " + CLIP_NAME[c],
                   "data": {"name": "Hullbound Mender - " + CLIP_NAME[c], "type": "ANIMATION",
                            "image": urls["sg579_" + c]["url"], "folder": "HullboundMender", "frames": 24, "speed": 50,
                            "hidden": True, "onInitialBattleField": False, "licenseDetails": "TNR"}}
                  for c in CLIPS_V2]
        changed = apply_art(lambda c: "@scene:sg579_" + c)
        edits = [{"entity": "jutsu", "slot": "edit", "targetId": idmap[PFX["jutsu"] + k], "srcId": "sg579j_" + k,
                  "phase": 2, "name": JUTSU[k]["name"], "data": JUTSU[k]} for k in JUTSU if k in changed]
        write(NUM["art"], "hullbound_mender_art",
              "push/579, HIDDEN: the Mender's v2 clips (approved 2026-11-09 17:39 UTC) as 9 hidden ANIMATION assets "
              "(images already on the director's UploadThing), then the 575 kit edited by id to use them in place of "
              "the live Skyglass stand-ins. No AI equips these jutsu yet (576 runs after), so no equip link to sever.",
              assets + edits)
        return
    if mode == "ais":
        J = ids_from_bundle(sys.argv[sys.argv.index("--jutsu") + 1], PFX["jutsu"], JUTSU, fix_arg())
        items = build_ais(J)
        write(NUM["ais"], "hullbound_mender_ais",
              "push/576, HIDDEN: the four AIs (fresh creates, equipped once; law 18 applies to any later jutsu edit): "
              "The Mender's Apprentice (Veteran Foundry Warden art, 5,050 HP, +25% damage taken = 4,040 effective), Bilge "
              "Caulker and Bilge Pump Hand (Deck Warden and First Blade art, 5,050 HP, +100% taken = 2,525 effective, live Quick Strike and Tide Bolt), The Hullbound Mender "
              "(16,160 HP, AI Heavy Armor, stun immune, placeholder avatar). Jutsu by literal id from push/575's "
              "bundle.", items, {"_jutsu_ids": J})
        return
    if mode == "quest":
        J = ids_from_bundle(sys.argv[sys.argv.index("--jutsu") + 1], PFX["jutsu"], list(JUTSU) + ["chart"], fix_arg())
        A = ids_from_bundle(sys.argv[sys.argv.index("--ais") + 1], PFX["ais"],
                            ["apprentice", "caulker", "pump", "mender"])
        q = quest_entry(A, J["chart"])
        check_graph(q["data"]["content"]["objectives"])
        write(NUM["quest"], "hullbound_mender_quest",
              "push/577, HIDDEN: The Closing Hold, the isolated Battle Pyramid entered with the Chart of the Closing "
              "Hold (spent at start; level 40+ for the 12x10 arena; carried pools, a lost fight fails the run): the "
              "Apprentice, the Bilge Crew, the Hullbound Mender; pick 2 of Coffer x2 / Sealed Treasury / Token x2 / "
              "Galley Stores x3; Lantern 30%, Core Rot 40%, Shard of the Keel 50%, Sealed Treasury 6%, 5,000 exp. "
              "Chart drop rows wait for the Friday go-live.", [q], {"_ai_ids": A, "_chart_id": J["chart"]})
        return
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
