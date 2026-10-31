#!/usr/bin/env python3
"""Skyglass steeping: the two special steeping quests and the Epic charts' use effect that starts them. All HIDDEN.

    python3 push/skyglass_steeping.gen.py --copies <344 bundle> [--copies <bundle> ...] [--keymap <keys.json>]
        -> push/356_skyglass_steeping.json   (2 special quest creates; needs push/344's results for the Horror's id)
    python3 push/skyglass_steeping.gen.py --charts <356 bundle>
        -> push/357_skyglass_steeping_charts.json   (2 item edits; needs push/356's results for the quests' ids)

Run order: 344 (rebuilt) -> build 356 -> gates -> run 356 -> build 357 -> gates -> run 357. Neither output is committed
before its input bundle exists (L01: Forge's offline plan has no retained idmap, so the AI and quest ids are literal).

Design (RUL-2026-10-29-055; loot tables section 5 "Steeping"; RUL-2026-10-31-072 F03, F13, F32; text SKYGLASS_TEXT.md
section 2.7, read verbatim by push/skyglass_text.py):
  * Using an Epic chart (Reliquary Seal, The Last Heading; push/329 creates, hidden) consumes one copy and starts its
    own `special` quest (item effect `noncombatquest`). Special quests appear in no list and only an item starts them.
  * The 3 Core Rot are `entryItems` (F13), never `deliver_item` (which deletes the whole stack).
  * d_steep: "Steep" -> b_horror; "Take it back" -> w_back (win; refunds the chart and the 3 Rot).
  * b_horror: the Steeping Horror (344 one-off, AI key oneoff:steeping-horror), scaled to the player, full pools.
    Win -> w_taken (the tainted chart). Loss -> f_spat, a DIALOG that hands the chart back (F03: rewards on a
    fail_quest objective are never paid, theninjarpg@3314d122 libs/quest.ts ~1514-1525, ~494-522), then f_lost.
  * isolated: true (F32): an isolated defeat stays in the run at 1 HP (libs/combat/database.ts ~1324), so the
    chart-return step does not wait out a hospital stay.

Why using a chart can never destroy it when the player cannot proceed (theninjarpg@3314d122, read, not run):
  server/api/routers/item.ts ~1995-2033 refuses BEFORE any debit a second effect, a chart without preventBattleUsage /
  target SELF / method SINGLE, a granted quest that is not `special`, and an attempt already open ("You are already on
  this quest"). The debit and assignQuestToUser share one receipt transaction (~2421-2464): any refusal inside
  assignQuestToUser (quests.ts ~2604-2760: rank, availability, dates, "must be awake" because the quest has entry items,
  concurrency, and the entry charge "You need 3x Core Rot in your inventory to enter.") throws questRejected and rolls
  the whole consumption back, so the chart stays in the inventory. questRank D (every rank), levels 1-100, and special
  quests take no completion caps (libs/quest.ts ~2518-2526; QuestTypesWithMaxAttempts omits special).
  Once the quest has started, the chart and the Rot are spent: Take it back is the refund. Abandoning the run instead
  refunds nothing, and an edit to these quests restarts open attempts (libs/questRun.ts hasQuestContentChanged), so
  never edit them while players may be steeping.

Do not hand-edit the outputs.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
import skyglass_text as T  # noqa: E402
import skyglass_aikeys as K  # noqa: E402

NUM, CHARTS_NUM = 356, 357
PFX = "sg356_"
BUNDLE_329 = os.path.join(ROOT, "harvests/inbox/tnr_results_1793424666625.json")  # push/329 results
DESIGN = os.path.join(ROOT, "state/skyglass_design/design_data.json")
EXP = "art/skyglass_event_icons/exports/"
HOLD = "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH"  # scene `hold` (RUL-2026-10-30-061 item 7)
HORROR_KEY = "oneoff:steeping-horror"

# (slug, chart srcId in 329, tainted srcId in 329, design_data key of the chart, icon export, text column)
QUESTS = [
    ("reliquary", "sg329_reliquary_seal", "sg329_rotted_reliquary_seal", "chart_reliquary_seal",
     "icon-reliquary-seal.webp", 1),
    ("heading", "sg329_last_heading", "sg329_rotted_heading", "chart_last_heading", "icon-the-last-heading.webp", 2),
]
SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the chart's way closes.",
          "fleeDescription": "You break away, and the way back closes behind you."}  # text doc section 2, shared lines
# Text the doc does not give (reversible; listed in the manifest's _text_gaps for the director):
GAP_SPAT_CHOICE = "Leave the pool"
GAP_LOST = ""  # fail_quest with no description: the engine shows "Failed: <quest name>" (libs/quest.ts ~1522)


def created_329():
    out = {}
    for e in json.load(open(BUNDLE_329))["entries"]:
        if e.get("srcId") and e.get("state") == "ok" and e.get("id"):
            out[e["srcId"]] = (e["id"], e["name"])
    return out


def design_items():
    return json.load(open(DESIGN))["items"]


def subs():
    """The section 2.7 substitution table: {'<quest>': [reliquary, heading], ...}."""
    rows = T.table("### 2.7 Steeping")
    out = {}
    for r in rows:
        vals = [v.split(" (name:")[0] for v in r[1:3]]  # "(name: open question 2)" is an annotation, settled by RUL-057
        out[r[0]] = vals
    assert set(out) == {"<quest>", "<chart>", "<tainted>", "<run>"}, out
    return out


def fill(text, col, S):
    for k, v in S.items():
        text = text.replace(k, v[col - 1])
    assert "<quest>" not in text and "<chart>" not in text and "<tainted>" not in text and "<run>" not in text
    return text


def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a], text=True).strip()


def image_pack(files):
    paths = [EXP + f for f in files]
    ref = git("log", "-1", "--format=%H", "HEAD", "--", *paths)
    if not ref:
        sys.exit("icon exports not committed")
    out = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"]) != disk:
            sys.exit(f"{p}: working copy differs from {ref}")
        out[os.path.basename(p)] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    return {"ref": ref, "files": out}


def quest(slug, chart, tainted, rot, icon, col, horror, S):
    t = lambda target: fill(T.block(target), col, S)  # noqa: E731
    ch = T.choices("obj:<quest>/d_steep.description")
    assert ch == ["Steep", "Take it back"], ch
    item = lambda i, n: {"ids": [i], "number": 100, "quantity": n}  # noqa: E731
    scene = {"sceneBackground": HOLD, "sceneCharacters": []}
    objectives = [
        {"id": "d_steep", "task": "dialog", "description": t("obj:<quest>/d_steep.description"), **scene,
         "nextObjectiveId": [{"text": ch[0], "nextObjectiveId": "b_horror"},
                             {"text": ch[1], "nextObjectiveId": "w_back"}]},
        {"id": "b_horror", "task": "start_battle", "description": t("obj:<quest>/b_horror.description"), **scene,
         "opponentAIs": [{"ids": [horror], "number": 1, "quantity": 1}], "completionOutcome": "Win", "scaleGains": 1,
         "keepOriginalPools": False, "opponent_scaled_to_user": True,  # loot tables 5: "a Core Horror scaled to the player"
         "nextObjectiveId": "w_taken", "failObjectiveId": "f_spat", **SHARED},
        {"id": "w_taken", "task": "win_quest", "description": t("obj:<quest>/w_taken.description"), **scene,
         "reward_items": [item(tainted, 1)]},
        # F03: the consolation is paid on this dialog's completion, before the fail ending.
        {"id": "f_spat", "task": "dialog", "description": t("obj:<quest>/f_spat.description"), **scene,
         "reward_items": [item(chart, 1)],
         "nextObjectiveId": [{"text": GAP_SPAT_CHOICE, "nextObjectiveId": "f_lost"}]},
        {"id": "f_lost", "task": "fail_quest", "description": GAP_LOST, **scene},
        # Take it back: the chart and the 3 Core Rot paid at entry come back (F13).
        {"id": "w_back", "task": "win_quest", "description": t("obj:<quest>/w_back.description"), **scene,
         "reward_items": [item(chart, 1), item(rot, 3)]},
    ]
    name = S["<quest>"][col - 1]
    return {"entity": "quest", "slot": "create", "srcId": PFX + slug, "phase": 1, "name": name, "data": {
        "name": name, "description": t("quest:<quest>.description"),
        "successDescription": t("quest:<quest>.successDescription"),
        "image": "@img:" + icon, "questType": "special", "questRank": "D", "hidden": True,
        "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True,
        "requiredLevel": 1, "maxLevel": 100, "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None,
        "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives, "sceneBackground": HOLD, "sceneCharacters": [],
                    "entryItems": [{"ids": [rot], "number": 3}], "isolated": True, "reward": {}}}}


def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/skyglass_steeping.gen.py; do not hand-edit."}
    if extra:
        m.update(extra)
    m["items"] = items
    path = os.path.join(ROOT, f"push/{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{num}_{slug}.json: {len(items)} items")


def build_quests(bundles, keymap):
    R = K.Resolver(bundles, keymap)
    horror = R(HORROR_KEY)
    c329, D, S = created_329(), design_items(), subs()
    rot = c329["sg329_core_rot"]
    assert rot[1] == "Core Rot"
    items = []
    for slug, chart_src, tainted_src, dkey, icon, col in QUESTS:
        chart, tainted = c329[chart_src], c329[tainted_src]
        assert chart[0] == D[dkey]["id"], (dkey, chart)
        for (lid, lname), tok in ((chart, "<chart>"), (tainted, "<tainted>")):
            assert S[tok][col - 1].lower() in (lname.lower(), "the " + lname.lower()), (tok, lname)
        items.append(quest(slug, chart[0], tainted[0], rot[0], icon, col, horror, S))
    pack = image_pack([q[4] for q in QUESTS])
    write(NUM, "skyglass_steeping", (
        f"push/{NUM}, HIDDEN. The two steeping special quests (RUL-2026-10-29-055; RUL-2026-10-31-072 F03/F13/F32): "
        f"{items[0]['name']} and {items[1]['name']}. Entry 3 Core Rot (entryItems); Steep -> the Steeping Horror "
        f"({horror}, AI key {HORROR_KEY}, from {', '.join(R.bundles) or 'keymap'}), scaled; win: the tainted chart; loss: "
        "a dialog returns the chart, then the fail ending (the Rot is spent); Take it back: the chart and the 3 Rot "
        "come back. isolated: true. Nothing starts these until push/" + str(CHARTS_NUM) + " gives the Epic charts their "
        "use effect (built from this run's results bundle)."),
        items, {"dedupNames": True, "_aiKeys": R.used,
                "_text_gaps": {"obj:<quest>/f_spat.choice[0]": GAP_SPAT_CHOICE,
                               "obj:<quest>/f_lost.description": "(empty: the engine shows 'Failed: <quest name>')"},
                "imgSizes": {k: v["bytes"] for k, v in pack["files"].items()}, "imagePack": pack})


def build_charts(bundle):
    b = json.load(open(bundle))
    got = {}
    for e in b.get("entries") or []:
        if e.get("entity") == "quest" and e.get("slot") == "create" and e.get("state") == "ok" and e.get("id"):
            got[e.get("srcId")] = (e["id"], e["name"])
    for k, v in (b.get("idmap") or {}).items():
        if k.startswith(PFX) and k not in got:
            got[k] = (v, None)
    c329, S = created_329(), subs()
    m329 = {it.get("srcId"): it["data"] for it in json.load(open(os.path.join(ROOT, "push/329_skyglass_items_and_quests.json")))["items"]}
    items = []
    for slug, chart_src, _, _, _, col in QUESTS:
        if PFX + slug not in got:
            raise SystemExit(f"{PFX + slug} missing from {os.path.basename(bundle)}: is it push/{NUM}'s results?")
        qid, qname = got[PFX + slug]
        name = S["<quest>"][col - 1]
        if qname not in (None, name):
            raise SystemExit(f"{PFX + slug} is {qname!r} in the bundle, not {name!r}")
        cid, cname = c329[chart_src]
        live = m329[chart_src]
        # routers/item.ts ~1999-2008: a quest grant needs preventBattleUsage, target SELF, method SINGLE; the chart is
        # spent by destroyOnUse. All four are already so on the push/329 create; the edit sends only `effects`.
        assert live["preventBattleUsage"] and live["target"] == "SELF" and live["method"] == "SINGLE" \
            and live["destroyOnUse"] and live["itemType"] == "CONSUMABLE" and live["effects"] == [], chart_src
        eff = {"type": "noncombatquest", "questId": qid, "power": 1, "target": "INHERIT", "direction": "offence",
               "calculation": "static", "powerPerLevel": 0, "description": f"Starts {name}", "appearSfx": "",
               "disappearSfx": "", "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "",
               "disappearAnimation": ""}  # the push/274 Armory Requisition shape (verified live)
        items.append({"entity": "item", "slot": "edit", "name": f"{cname}: use to steep", "targetId": cid,
                      "data": {"effects": [eff]}})
    write(CHARTS_NUM, "skyglass_steeping_charts", (
        f"push/{CHARTS_NUM} (after push/{NUM}, from its results bundle {os.path.basename(bundle)}; literal ids, L01). "
        "The two Epic charts (hidden push/329 items) get their use effect: noncombatquest starting their steeping "
        "quest. Fetch-merge item edits carrying only `effects` (the charts' text, image and flags stay as they are). "
        "The charts stay hidden."), items)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--copies", action="append", default=[], help="push/344 results bundle (repeatable)")
    ap.add_argument("--keymap", help="JSON {AI key: literal id} overriding the bundle lookup")
    ap.add_argument("--charts", help="push/356 results bundle: write the chart edits")
    a = ap.parse_args()
    if a.charts:
        if a.copies or a.keymap:
            ap.error("--charts takes only the 356 bundle")
        return build_charts(a.charts)
    if not a.copies and not a.keymap:
        ap.error("--copies <344 bundle> (or --keymap) is required: the Steeping Horror's id comes from push/344")
    return build_quests(a.copies, a.keymap)


if __name__ == "__main__":
    main()
