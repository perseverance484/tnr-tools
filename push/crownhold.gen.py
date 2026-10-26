#!/usr/bin/env python3
"""Generate the Crownhold manifests from the approved design package (RUL-2026-10-25-005, -010, -011).

    python3 push/crownhold.gen.py

Source: state/crownhold/package/ (claude/silent-bastion-authoring-69za5u@6271e1f, RUL-2026-10-15-001 and
RUL-2026-10-16-*), with the fresh reads of push/269 (state/crownhold/source_check_2026-10-25.md).

push/271 = the records: The Last Directive and Extermination Order (AI jutsu), Countermand (Arakane's item), then the
20 Crownhold AIs. All HIDDEN. The quest follows as push/272 once these ids exist. Do not hand-edit the output.
"""
import hashlib, json, os

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
    "D5.BOSS": "@img:avatar_crownhold_arakane.webp",                                                            # drawn 2026-10-25
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
        "description": ("The command seal of Crownhold. Supreme Commander Arakane presses it against an afterimage's "
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
HONOR_TOKENS = 1000  # Crownhold's Honor: PROPOSAL, the director sets the amount (RUL-2026-10-25-002)
RENAME = {"Bastion Proving Proctor": "Crownhold Proving Proctor"}
FAIL_ID = "f_lost"

QUEST_DESCRIPTION = (
    "The Lastlight Lantern burns toward a mountain the maps call empty. Crownhold, the fortress that issued the Skyglass "
    "Project's last directive, has not answered a call in a generation. Its gates stand open. Nothing guards them.\n\n"
    "Starting the expedition spends one Lastlight Lantern. Lose any fight and the expedition ends; the Lantern is not "
    "refunded.\n\nIf you still have a reward to choose from an earlier expedition, claim it before you set out: an "
    "expedition cannot be completed while an earlier reward choice is waiting.")
QUEST_SUCCESS = "Supreme Commander Arakane has fallen and his Command Crown lies broken. Choose your reward."
CROWN = ("Above his brow the Command Crown turns slowly: seven blades of Skyglass hanging in the air around a gold "
         "circlet, and from every blade a thread of light running down through the floor, out to every officer you "
         "passed on the way up. You have been cutting those threads all the way up the mountain.")
OVERRIDE = {
    "d.aftermath": (
        "Supreme Commander Arakane falls to one knee. The Command Crown cracks through its prism core, and the floating "
        "blades drop and shatter on the stone. All through the mountain, the threads of light go slack. Then he is only "
        "light, settling over the floor of the throne room like ash.\n\nFor a moment Crownhold is silent in a new way. "
        "The relay lines stop. The lamps dim.\n\nThen, in the signal room far below, the relay board wakes. A new order "
        "prints itself, line by line, onto the Supreme Commander's own paper. It is dated today. It bears no seal you have "
        "seen anywhere in Crownhold. It is addressed to the Ghost Ship.\n\nThe crown is broken. Something else is still "
        "giving orders."),
}
FAIL_TEXT = "You fall, and Crownhold does not let you up. You wake outside the gate in the snow, and the Lantern has gone dark."
WIN_TEXT = "Crownhold falls silent behind you. Whatever still gives its orders, it no longer has a crown to give them through."


def prose(t):
    for a, b in (("the Silent Bastion", "Crownhold"), ("The Silent Bastion", "Crownhold"), ("Silent Bastion", "Crownhold"),
                 ("the Bastion's", "Crownhold's"), ("The Bastion's", "Crownhold's"), ("the Bastion", "Crownhold"),
                 ("The Bastion", "Crownhold"), ("Bastion", "Crownhold")):
        t = t.replace(a, b)
    for a, b in RENAME.items():
        t = t.replace(a, b)
    return t


def qtag(t, kind):
    calc = {"stunprevent": "percentage", "increasedamagegiven": "percentage", "increasedamagetaken": "percentage"}
    return {"type": t["type"], "power": t["power"], "rounds": t["rounds"], "target": "INHERIT", "direction": "offence",
            "calculation": t.get("calculation", calc.get(t["type"], "static")), "powerPerLevel": 0,
            "description": {"buff": "Combat Protocol", "debuff": "Security Alert"}[kind], "appearSfx": "",
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
        if nid in OVERRIDE: return OVERRIDE[nid]
        t = prose(obj[nid]["text"])
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
                    label = opts.get(c["label"]) or opts.get(c["to"]) or c["label"]
                    if seen[c["to"]] > 1:  # a menu may not send two options to one node: each wrong answer gets a beat
                        k += 1
                        beat = f"{nid}.wrong{k}"
                        out.append({"id": beat, "task": "dialog", "description": f"You choose: {label}. Somewhere in the walls a ward wakes and turns toward you.",
                                    "sceneBackground": scene(nid), "sceneCharacters": [], "nextObjectiveId": [{"text": "Go on", "nextObjectiveId": c["to"]}]})
                        choices.append({"text": label, "nextObjectiveId": beat})
                    else:
                        choices.append({"text": label, "nextObjectiveId": c["to"]})
            else:
                nxt = n["next"]
                label = "Fight" if nxt.startswith("b") else ("Leave Crownhold" if nxt.startswith("w") else "Continue")
                choices = [{"text": label, "nextObjectiveId": nxt}]
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
    reward = {"reward_items": [{"ids": [ITEM["coffer"]], "number": 100, "quantity": 2}], "reward_tokens": HONOR_TOKENS,
              "reward_jutsus": [LASTLIGHT_JUTSU]}
    if "badge:crownbreaker" in IDS: reward["reward_badges"] = [IDS["badge:crownbreaker"]]
    return {"entity": "quest", "slot": "create", "srcId": "crownhold", "name": "Crownhold", "data": {
        "name": "Crownhold", "description": QUEST_DESCRIPTION, "image": "@img:avatar_crownhold_arakane.webp",
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
    write(271, "crownhold_exclusives", (
        "Crownhold exclusives (push/271), all HIDDEN (RUL-2026-10-25-005; package RUL-2026-10-15-001 / -10-16-*): The Last "
        "Directive and Extermination Order (Arakane's AI jutsu; values approved RUL-2026-10-16-004/-011/-013) and "
        "Countermand (his OTHER item: Clear 100, 40 AP, range 5, cooldown 6, PVE; RUL-2026-10-16-011). They must exist "
        "before the 20 Crownhold AIs (push/272), which equip them by literal id (law 17). Placeholder icons. Generated by "
        "push/crownhold.gen.py; do not hand-edit."), [
        ai_jutsu("X:LAST_DIRECTIVE", "last_directive",
                 ("Arakane's final order to himself. For five rounds he cannot fall, strikes harder, and nothing he "
                  "carries can be stripped away."),
                 "%user speaks the Last Directive. The Command Crown blazes and refuses to let him fall."),
        ai_jutsu("X:EXTERMINATION_ORDER", "extermination_order",
                 ("Given only while the Last Directive holds. A single killing order that seals the target's elements "
                  "and keeps them from cleansing it."),
                 "%user issues the Extermination Order. Every thread of the Crown pulls toward %target."),
        countermand()])
    if all(k in IDS for k in ("@jutsu:last_directive", "@jutsu:extermination_order", "@item:countermand")):
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
    else:
        print("272 waits for push/271's ids in state/crownhold/ids.json")
    q = quest()
    out = os.path.join(ROOT, "state/crownhold/quest.preview.json")
    json.dump(q, open(out, "w"), indent=1)
    print("quest preview:", len(q["data"]["content"]["objectives"]), "objectives ->", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
