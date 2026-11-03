#!/usr/bin/env python3
"""Skyglass uber key economy (RUL-2026-11-02-100; rates RUL-2026-11-02-099 R1-R6): the four Invitation shards,
Salvage and its exchange "The Glass Answers", and the Heartglass / The Remainder variant tokens and variants.

    python3 push/skyglass_uber_economy.gen.py
        -> push/417_skyglass_uber_economy.json         (creates, all HIDDEN: 7 items, 1 AI, 2 variants, 1 special quest)
    python3 push/skyglass_uber_economy.gen.py --link <417 bundle>
        -> push/418_skyglass_uber_economy_link.json    (3 item edits: Salvage starts the quest; the 2 tokens bound 1:1)
    python3 push/skyglass_uber_economy.gen.py --unhide <417 bundle>
        -> push/419_skyglass_uber_economy_unhide.json  (7 item edits + 1 quest edit, hidden false)
    python3 push/skyglass_uber_economy.gen.py --drops <417 bundle>
        -> push/420_skyglass_uber_shard_drops.json     (11 live quest edits re-sent whole: the shard drops)

Run order: 417 -> (bundle) build 418, 419, 420 -> gates -> run 418 -> run 419 -> run 420 -> the director's dungeon
editor rows (README). 418-420 need 417's results for literal ids (L01), so none is committed before that bundle exists.
420 must follow 419: quest rewards do not filter hidden items (theninjarpg@3314d122: no `hidden` test anywhere in the
reward path), so a drop line may never point at a hidden shard.

Design (RUL-2026-11-02-100, read with RUL-094 canon and the design doc's Invitation / Rewards sections):
  * Shards: plain tradeable items, no effect. One of each is the Mother of Echoes quest's entryItems (the fight build).
  * Salvage: untradeable CONSUMABLE. Using it starts the special quest "The Glass Answers" (item effect
    `noncombatquest`, added by 418 once the quest id exists). The use spends that one Salvage; entryItems spend 34
    more: theninjarpg@3314d122 routers/item.ts ~2400-2464 debits the used stack first, then assignQuestToUser charges
    entryItems inside the same transaction (routers/quests.ts ~2733-2830, server/utils/questEntry.ts), so 35 in all,
    and any shortfall rolls the whole use back (the Salvage stays).
  * The quest: a dialog picks one of four shards (or "Leave the glass", a refund of all 35, the steeping mis-tap
    pattern of push/356). Each shard branch is a one-round fight against one Stilled Echo, then a win that pays that
    shard. A quest with entryItems must contain a battle (validators/objectives.ts ~1024-1033); dialog choices route
    to their own branch (libs/quest.ts ~1626-1661 selectedNextObjectiveId).
  * The Stilled Echo: level 1, multipliers 1 (HP 100: enemy.py pool law), stats 10, no jutsu, includeDefaultRules
    false and one unconditional rule, end_turn (law 41; ai.md: end_turn always executes, so the AI never attacks and
    never exhausts). Not scaled to the player, scaleGains 0.
  * Tokens: the 1:1 trophy pattern (pipeline 2.10): token create with variantId null (417 phase 1), variant create
    with requiredItemId = the token (417 phase 2), token edit binding variantId (418). Untradeable. Variants have no
    hidden state, so both show on their base weapons as "Need <token>" from 417's run (the push/329 precedent).

Do not hand-edit the outputs.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("skyglass_items", os.path.join(ROOT, "push/skyglass_items.gen.py"))
IT = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(IT)

NUM, LINK, UNHIDE, DROPS = 417, 418, 419, 420
PFX = "sg417_"
PLACEHOLDER = IT.PLACEHOLDER  # engine default image (RUL-2026-10-30-059)
BLANK = "1YXbXYW2wz3GETVMb6DT6"  # Blank Scene Character (push/383-385 publish rule)
CORE_CHAMBER = "81DATu13hATfbkPuLT54E"  # scene asset reconstruction_chamber (push/339 SCENE_ASSET)
# Placeholder sprite for the Stilled Echo: the Faded crew's live sprite (push/344 part 1, Faded Deck Warden).
ECHO_AVATAR = "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261019-v3-texZaFi42S3EvJZBwQ8cd-main-eded2d557ed1.webp"
HEARTGLASS_ART = "art/skyglass_variant_skins/exports/icon-variant-heartglass.webp"

UNWRITTEN = "m0RZDUDnwQu_0BtOJgHi9"      # The Unwritten (fan): push/371 variant rows
INK_OF_THE_VOID = "wE1QeldWTjls2Cf43cFjf"  # Ink of the Void (bow): push/371 variant rows (Stargazer)
# Variant orders taken on these bases by push/329 (The Unwritten Order 1, Captain's Gunbai 2; Stargazer 1). Variants
# without a token are not captured on these two items; a taken order refuses the create cleanly (329 Roll-Call).
ORDER = {UNWRITTEN: 3, INK_OF_THE_VOID: 2}

COST, ENTRY = 35, 34  # RUL-099 R6; the used Salvage + 34 entry items
DROPS_TABLE = {  # shard -> (rate %, quests), RUL-099 R1/R3/R4 (integers: RUL-2026-10-31-087)
    "crown": (40, ["Crownhold"]),
    "tide": (25, ["The Sealed Reliquary", "The Fall", "The Rotted Reliquary", "The Burning Heading"]),
    "ledger": (15, ["The Trophy Hold", "The Bone Store", "The Snare Room", "The Overgrown Stores", "The Ore Vault",
                    "The Bloom Cellar"]),
}
# Latest committed definitions (re-sent whole; no later edit in push/ or harvests), with their verified run bundles.
SOURCES = {
    "push/383_skyglass_publish_chart_runs.json": "harvests/inbox/tnr_results_1793492872251.json",
    "push/384_skyglass_publish_haul.json": "harvests/inbox/tnr_results_1793492888772.json",
    "push/385_skyglass_publish_crownhold_hunts.json": "harvests/inbox/tnr_results_1793492929044.json",
}

# ---------------------------------------------------------------------------------------------------------------
# Text (design voice: story line in italics, then what it does; SKYGLASS_TEXT.md section 4 conventions)
# ---------------------------------------------------------------------------------------------------------------
INVITE = ("<b>Her invitation:</b> carry all four shards (Keel, Crown, Tide and Ledger) to open the way to "
          "<b>The Mother of Echoes</b>. All four are spent when the fight begins.")
GLASS = f"<b>Or:</b> use {COST} Salvage to ask the glass for any one shard."
SHARDS = [  # (key, name, story line, drop line)
    ("keel", "Shard of the Keel",
     "A splinter of the Mother Glass, shaken loose from the Core the war-ship was built around.",
     "Skyglass Wreck clear 4%"),
    ("crown", "Shard of the Crown",
     "A splinter of the Mother Glass, fallen from the broken Command Crown.",
     "Crownhold 40%"),
    ("tide", "Shard of the Tide",
     "A splinter of the Mother Glass, washed out of the echoes the Core could not hold.",
     "The Sealed Reliquary, The Fall and both Legendary chart runs 25%"),
    ("ledger", "Shard of the Ledger",
     "A splinter of the Mother Glass, entered in the stores ledger and never claimed.",
     "every Haul run 15%"),
]


def shard_desc(story, drop):
    return f"<i>{story}</i><br><br><b>Drops:</b> {drop}<br>{GLASS}<br>{INVITE}"


SALVAGE_DESC = (
    "<i>What still works aboard the wreck: brass fittings, sound timber, skyglass that holds a little light.</i><br><br>"
    "<b>Drops:</b> Skyglass Wreck clear ×5 · Faded Wreck clear ×2<br>"
    f"<b>The Glass Answers:</b> use Salvage from your inventory to trade <b>{COST} Salvage</b> (the one you use and "
    f"{ENTRY} more, carried, not stored at home) for the Invitation shard of your choice. A stilled echo brings it up; "
    "strike it once. Choose <i>Leave the glass</i> and all 35 come back. Flee or fall, and the Salvage is spent.")

TOKEN_TMPL = ("<i>{story}</i><br><br>Unlocks <b>{v}</b>, a variant of <b>{base}</b> (new look and name, same stats). "
              "You must own {base}: open it, choose <b>Variants</b>, then <b>Use {v}</b>. Once per player.")
TOKENS = [  # (key, variant/token name, base name, base id, token story, variant description, image)
    ("heartglass", "Heartglass", "The Unwritten", UNWRITTEN,
     "Cut from Sayo's own glass. Every pane still holds a face, and every face is listening.",
     "The Unwritten remade in thin panes of cyan glass, a faint face pressed behind each. When it opens, the faces "
     "turn toward your target.", "@img:icon-variant-heartglass.webp"),
    ("remainder", "The Remainder", "Ink of the Void", INK_OF_THE_VOID,
     "What the Silence did not finish drinking. It makes no sound at all.",
     "Ink of the Void gone matte black and still. It drinks the light around it, its string never glints, and dust "
     "hangs unmoving where its arrows pass.", PLACEHOLDER),
]

# RUL-2026-11-02-102: quest rewards have no once-per-player flag (validators/base.ts:20-28), so The Remainder can drop
# again after it is unlocked. Its token trades so a duplicate is worth something; Heartglass stays untradeable.
TRADEABLE_TOKENS = {"remainder"}
TRADE_NOTE = "<br>Tradeable: you only ever need one, so sell the rest."

Q_NAME = "The Glass Answers"
Q_DESC = (f"Lay {COST} Salvage on the glass floor of the Core chamber. The skyglass in it hums, and far below, in the "
          "Mother Glass, something answers.\n\n"
          "Ask for one shard of the Mother Glass. A stilled echo brings it up to you; break the echo and the shard is "
          "yours.\n\n"
          f"Costs {COST} Salvage, spent when you start. Leave the glass and all {COST} come back. Flee or fall, and "
          "the Salvage is gone.")
Q_SUCCESS = "The echo breaks, and the glass gives up what it held."
D_CHOOSE = ("You set the Salvage down on the glass floor, piece by piece. The hum rises through your feet. Far below, "
            "something is listening, and it will trade.<br><br>Which shard do you ask for?")
B_TEXT = ("An echo rises out of the floor with the shard in its hands: a deckhand, stilled mid-step, worn too thin to "
          "raise them. One blow frees it.")
W_TEXT = "The echo breaks like frost on a window. The shard drops into your palm, still warm."
W_BACK = "You gather the Salvage back up. The hum fades, and whatever was listening goes back to waiting."
F_LOST = "The echo sinks back into the glass, and the Salvage goes with it."
SHARED = {"failDescription": "The echo sinks back into the glass.",
          "drawDescription": "The echo sinks back into the glass.",
          "fleeDescription": "You step back, and the echo sinks into the glass with your Salvage."}


# ---------------------------------------------------------------------------------------------------------------
# 417: creates
# ---------------------------------------------------------------------------------------------------------------
def ref(key):
    return "@item:" + PFX + key


def items():
    out = []
    for key, name, story, drop in SHARDS:
        e = IT.create(PFX + key, name, shard_desc(story, drop), "LEGENDARY", "OTHER", True, battle="Invitation shard")
        e["data"]["destroyOnUse"] = False
        out.append(e)
    # Salvage starts a quest from the inventory: CONSUMABLE, SELF, SINGLE, preventBattleUsage (routers/item.ts
    # ~1999-2008). The noncombatquest effect is added by 418 (the quest id does not exist yet).
    out.append(IT.create(PFX + "salvage", "Salvage", SALVAGE_DESC, "COMMON", "CONSUMABLE", False, battle="Salvage"))
    for key, v, base, _bid, story, _vdesc, _img in TOKENS:
        trade = key in TRADEABLE_TOKENS
        desc = TOKEN_TMPL.format(story=story, v=v, base=base) + (TRADE_NOTE if trade else "")
        out.append(IT.create(PFX + key, v, desc, "LEGENDARY", "CONSUMABLE",
                             trade, [IT._token_effect()], battle="Variant token"))
    return out


def echo_ai():
    stat = 10
    return {"entity": "ai", "slot": "create", "phase": 2, "name": "Stilled Echo", "srcId": PFX + "stilled_echo",
            "data": {"username": "Stilled Echo", "hidden": True, "level": 1, "rank": "STUDENT",
                     "poolsMultiplier": 1, "statsMultiplier": 1, "regeneration": 0, "gender": "Unknown",
                     "preferredGeneral1": "Strength", "preferredGeneral2": "Speed", "primaryElement": None,
                     "secondaryElement": None, "isSummon": False, "avatarFacing": "left",
                     "ninjutsuMastery": stat, "genjutsuMastery": stat, "taijutsuMastery": stat,
                     "bukijutsuMastery": stat, "bloodlineMastery": stat, "sageMastery": stat,
                     "offence": stat, "defence": stat, "strength": stat, "intelligence": stat, "willpower": stat,
                     "speed": stat, "avatar": ECHO_AVATAR, "jutsus": [], "items": [], "effects": [],
                     "includeDefaultRules": False,
                     "rules": [{"conditions": [], "action": {"type": "end_turn",
                                                             "description": "stilled: it never acts"}}]}}


def variants():
    out = []
    for key, v, _base, bid, _story, vdesc, img in TOKENS:
        out.append({"entity": "itemVariant", "slot": "create", "srcId": PFX + "var_" + key, "phase": 2, "name": v,
                    "data": {"itemId": bid, "name": v, "image": img, "requiredItemId": ref(key),
                             "costType": "VARIANT_TOKEN", "cost": 1, "order": ORDER[bid], "description": vdesc,
                             "hidden": True}})
    return out


def glass_quest():
    sc = {"sceneBackground": CORE_CHAMBER, "sceneCharacters": []}
    choices = [{"text": name, "nextObjectiveId": "b_" + key} for key, name, _s, _d in SHARDS]
    choices.append({"text": "Leave the glass", "nextObjectiveId": "w_back"})
    objs = [{"id": "d_choose", "task": "dialog", "description": D_CHOOSE, **sc, "nextObjectiveId": choices}]
    for key, _name, _s, _d in SHARDS:
        objs.append({"id": "b_" + key, "task": "start_battle", "description": B_TEXT, **sc,
                     "opponentAIs": [{"ids": ["@ai:" + PFX + "stilled_echo"], "number": 1, "quantity": 1}],
                     "completionOutcome": "Win", "scaleGains": 0, "keepOriginalPools": False,
                     "opponent_scaled_to_user": False, "nextObjectiveId": "w_" + key, "failObjectiveId": "f_lost",
                     **SHARED})
        objs.append({"id": "w_" + key, "task": "win_quest", "description": W_TEXT, **sc,
                     "reward_items": [{"ids": [ref(key)], "number": 100, "quantity": 1}]})
    objs.append({"id": "w_back", "task": "win_quest", "description": W_BACK, **sc,
                 "reward_items": [{"ids": [ref("salvage")], "number": 100, "quantity": COST}]})
    objs.append({"id": "f_lost", "task": "fail_quest", "description": F_LOST, **sc})
    return {"entity": "quest", "slot": "create", "srcId": PFX + "glass_answers", "phase": 3, "name": Q_NAME, "data": {
        "name": Q_NAME, "description": Q_DESC, "successDescription": Q_SUCCESS, "image": PLACEHOLDER,
        "questType": "special", "questRank": "D", "hidden": True, "retryDelay": "none", "attemptDelay": "none",
        "consecutiveObjectives": True, "requiredLevel": 1, "maxLevel": 100, "prerequisiteQuestId": None,
        "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objs, "sceneBackground": CORE_CHAMBER, "sceneCharacters": [BLANK],
                    "entryItems": [{"ids": [ref("salvage")], "number": ENTRY}], "isolated": False, "reward": {}}}}


def image_pack():
    ref_ = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", HEARTGLASS_ART],
                                   text=True).strip()
    if not ref_:
        sys.exit(f"{HEARTGLASS_ART} is not committed")
    disk = open(os.path.join(ROOT, HEARTGLASS_ART), "rb").read()
    if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref_}:{HEARTGLASS_ART}"]) != disk:
        sys.exit(f"{HEARTGLASS_ART}: working copy differs from {ref_}")
    name = os.path.basename(HEARTGLASS_ART)
    return {"ref": ref_, "files": {name: {"path": HEARTGLASS_ART, "sha256": hashlib.sha256(disk).hexdigest(),
                                         "bytes": len(disk)}}}


def placeholders(entries):
    out = []
    for e in entries:
        d = e["data"]
        if d.get("image") == PLACEHOLDER:
            out.append(f"{e['entity']} {e['srcId']}: {d['name']} (engine default image)")
        if d.get("avatar") == ECHO_AVATAR:
            out.append(f"{e['entity']} {e['srcId']}: {d['username']} (Faded Deck Warden sprite)")
    return out


def write(num, slug, note, items_, extra=None):
    m = {"_note": note + " Generated by push/skyglass_uber_economy.gen.py; do not hand-edit."}
    if extra:
        m.update(extra)
    m["items"] = items_
    path = os.path.join(ROOT, f"push/{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{num}_{slug}.json: {len(items_)} items")


def build_create():
    entries = items() + variants() + [echo_ai()] + [glass_quest()]  # validate.py build order: item, itemVariant, ai, quest
    pack = image_pack()
    write(NUM, "skyglass_uber_economy", (
        f"push/{NUM}, all HIDDEN (RUL-2026-11-02-100). Phase 1: the four Invitation shards (tradeable, no effect; the "
        "Mother of Echoes quest takes one of each as entryItems), Salvage (untradeable; its use effect comes in "
        f"push/{LINK}), the Heartglass (untradeable) and The Remainder (tradeable, RUL-102) variant tokens (variantId null until push/{LINK}), "
        "and the Stilled Echo AI (level 1, no jutsu, one end_turn rule). Phase 2: the Heartglass variant on The "
        "Unwritten and The Remainder on Ink of the Void (variants have no hidden state: each shows as 'Need <token>' "
        f"from this run). Phase 3: the special quest {Q_NAME} ({ENTRY} Salvage entry + the used one = {COST}; pick a "
        "shard, one harmless fight, the shard; or Leave the glass for a full refund). Placeholders in _placeholders."),
        entries, {"dedupNames": True, "_placeholders": placeholders(entries),
                  "imgSizes": {k: v["bytes"] for k, v in pack["files"].items()}, "imagePack": pack})


# ---------------------------------------------------------------------------------------------------------------
# 418-420: built from 417's results bundle (literal ids, L01)
# ---------------------------------------------------------------------------------------------------------------
def created(bundle):
    b = json.load(open(bundle))
    got = {}
    for e in b.get("entries") or []:
        if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and (e.get("srcId") or "").startswith(PFX):
            got[e["srcId"]] = e["id"]
    for k, v in (b.get("idmap") or {}).items():
        if k.startswith(PFX):
            got.setdefault(k, v)
    want = {PFX + k for k, *_ in SHARDS} | {PFX + "salvage", PFX + "glass_answers", PFX + "stilled_echo"} \
        | {PFX + k for k, *_ in TOKENS} | {PFX + "var_" + k for k, *_ in TOKENS}
    missing = sorted(want - set(got))
    if missing:
        raise SystemExit(f"{os.path.basename(bundle)} is not push/{NUM}'s full results; missing {missing}")
    return got


def resolve(text, ids):
    for src, i in ids.items():
        text = text.replace(f'"@item:{src}"', json.dumps(i)).replace(f'"@ai:{src}"', json.dumps(i))
    assert "@item:" + PFX not in text and "@ai:" + PFX not in text, "unresolved 417 ref"
    return text


def build_link(bundle):
    ids = created(bundle)
    eff = {"type": "noncombatquest", "questId": ids[PFX + "glass_answers"], "power": 1, "target": "INHERIT",
           "direction": "offence", "calculation": "static", "powerPerLevel": 0, "description": f"Starts {Q_NAME}",
           "appearSfx": "", "disappearSfx": "", "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "",
           "disappearAnimation": ""}  # the push/357 shape
    out = [{"entity": "item", "slot": "edit", "name": f"Salvage: use to start {Q_NAME}", "targetId": ids[PFX + "salvage"],
            "data": {"effects": [eff]}}]
    for key, v, *_ in TOKENS:
        out.append({"entity": "item", "slot": "edit", "targetId": ids[PFX + key], "name": f"{v} (token): bind its variant",
                    "data": {"target": "SELF", "destroyOnUse": True, "preventBattleUsage": True,
                             "effects": [IT._token_effect(ids[PFX + "var_" + key])]}})
    write(LINK, "skyglass_uber_economy_link", (
        f"push/{LINK} (after push/{NUM}, from {os.path.basename(bundle)}; literal ids, L01). Salvage gets its use effect "
        f"(noncombatquest -> {Q_NAME}); Heartglass and The Remainder are bound to their own variants (pipeline 2.10 "
        "step 3). Fetch-merge item edits; every record stays hidden."), out)


def build_unhide(bundle):
    ids = created(bundle)
    out = [{"entity": "item", "slot": "edit", "targetId": ids[PFX + k], "name": f"{n}: unhide", "data": {"hidden": False}}
           for k, n, *_ in SHARDS]
    out.append({"entity": "item", "slot": "edit", "targetId": ids[PFX + "salvage"], "name": "Salvage: unhide",
                "data": {"hidden": False}})
    out += [{"entity": "item", "slot": "edit", "targetId": ids[PFX + k], "name": f"{v} (token): unhide",
             "data": {"hidden": False}} for k, v, *_ in TOKENS]
    # Quests are re-sent whole (quest.md: quest edits are full-record): 417's create with literal ids and hidden false.
    q = json.loads(resolve(json.dumps(glass_quest()["data"]), ids))
    q["hidden"] = False
    out.append({"entity": "quest", "slot": "edit", "targetId": ids[PFX + "glass_answers"], "name": f"{Q_NAME}: unhide",
                "data": q})
    write(UNHIDE, "skyglass_uber_economy_unhide", (
        f"push/{UNHIDE} (after push/{LINK}; from {os.path.basename(bundle)}; literal ids, L01): unhide the four shards, "
        f"Salvage, the two variant tokens and {Q_NAME}. The Stilled Echo AI has no hidden column (law 16b) and is "
        f"referenced only by {Q_NAME}. Run before push/{DROPS} and before the dungeon editor rows."), out)


def build_drops(bundle):
    ids = created(bundle)
    by_name, packs = {}, {}
    for f, results in SOURCES.items():
        packs[f] = json.load(open(os.path.join(ROOT, f))).get("imagePack")
        r = json.load(open(os.path.join(ROOT, results)))
        verified = {e.get("id") or e.get("targetId") for e in r.get("entries") or []
                    if e.get("state") == "ok" and e.get("verdict", "match") == "match"}
        for e in json.load(open(os.path.join(ROOT, f)))["items"]:
            if e["entity"] != "quest":
                continue
            name = e["data"]["name"]
            assert e["targetId"] in verified or any(e["targetId"] in json.dumps(x) for x in r.get("entries") or []), \
                (f, name)
            by_name[name] = (e, f)
    out, diff = [], {}
    for key, (rate, quests) in DROPS_TABLE.items():
        line = {"ids": [ids[PFX + key]], "number": rate, "quantity": 1}
        for qn in quests:
            src, f = by_name[qn]
            data = copy.deepcopy(src["data"])
            assert data["hidden"] is False, qn
            paths = []
            for o in data["content"]["objectives"]:
                if o["task"] == "win_quest":
                    ri = o.setdefault("reward_items", [])
                    assert all(ids[PFX + key] not in x["ids"] for x in ri), (qn, o["id"])
                    ri.append(dict(line))
                    paths.append(f"content.objectives[{o['id']}].reward_items += {SHARDS_BY_KEY[key]} {rate}%")
            assert paths, qn
            diff[qn] = paths
            out.append({"entity": "quest", "slot": "edit", "targetId": src["targetId"],
                        "name": f"{qn}: {SHARDS_BY_KEY[key]} {rate}% per clear", "data": data})
    assert len(out) == 11
    used = set(re.findall(r'"@img:([^"]+)"', json.dumps(out)))
    files, refs = {}, set()
    for f, pk in packs.items():  # the source manifests' own image packs, restricted to the images re-sent here
        for name in used & set((pk or {}).get("files", {})):
            files[name] = pk["files"][name]
            refs.add(pk["ref"])
    assert set(files) == used and len(refs) <= 1, (used - set(files), refs)
    extra = {"dedupNames": True, "_diff": diff}
    if files:
        extra.update({"imgSizes": {k: v["bytes"] for k, v in files.items()},
                      "imagePack": {"ref": refs.pop(), "files": files}})
    write(DROPS, "skyglass_uber_shard_drops", (
        f"push/{DROPS} (after push/{UNHIDE}; shard ids from {os.path.basename(bundle)}, L01). The shard drops (RUL-099 R1, "
        "R3, R4): each quest is re-sent WHOLE from its latest committed record (push/383, 384, 385, all VERIFIED; no later "
        "edit in push/ or harvests) with one drop line added to every win_quest ending, so each clear rolls once. "
        "Nothing else changes (_diff). These are live isolated Battle Pyramids: an edit makes any open run abandon "
        "and restart (libs/questRun.ts hasQuestContentChanged), so run it when no one is mid-run (outside the "
        "Friday-Sunday event)."), out, extra)


SHARDS_BY_KEY = {k: n for k, n, *_ in SHARDS}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--link", help="push/417 results bundle: write 418")
    ap.add_argument("--unhide", help="push/417 results bundle: write 419")
    ap.add_argument("--drops", help="push/417 results bundle: write 420")
    a = ap.parse_args()
    if a.link:
        return build_link(a.link)
    if a.unhide:
        return build_unhide(a.unhide)
    if a.drops:
        return build_drops(a.drops)
    return build_create()


if __name__ == "__main__":
    main()
