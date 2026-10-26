#!/usr/bin/env python3
"""Generate push/264: the Quarantined Archive and the Captain's Watch as hidden, isolated Battle Pyramids.

    python3 push/264_skyglass_hunts.gen.py

Source text: state/skyglass_hunts/hunts.py (draft content; docs/design/SKYGLASS_HUNTS_CONTENT.md). Rewards:
docs/design/SKYGLASS_LOOT_TABLES.md (RUL-2026-10-25-002/-004). The Drowned Foundry follows once the Foundry Warden
(push/262) exists, since its boss must be referenced by a literal id. Do not hand-edit the output.
"""
import hashlib, importlib.util, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("hunts", os.path.join(ROOT, "state/skyglass_hunts/hunts.py"))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)

AI = {"Core Horror": "AQi-bHJ-5tHXtxrnc0P9E", "Skyglass Sentinel": "3V_gdHYaclMB1gTyOPAbV", "Seal Charge": "wTgO-Q32caSSd0is1QIS7",
      "Sealwright": "RBW5KsIXmTGR710D2y2Y7", "Wayfinder": "v7T9_XdGMfP46em0dPuBc", "First Blade": "d6g0mOM7RBSsYI1hrUVT9",
      "The Captain": "QY69h271Nx9uHrBeR6jwW"}
ITEM = {"treasury": "Ma8S90Nmbi0Xvm4u4FzJh", "chart_archive": "cRZT41zm5vhPTQwwn8vtv", "chart_watch": "aHFNuo5RkKpDcaOBLIKiu",
        "case": "B48dTRsoLJGKBWIUbeUoG", "strongbox": "h-d58UCSuHN8EZKbLjT5R", "coffer": "THo7rfzP-S82_43aN8fs3", "inro": "ixEKlJ0MmDrX7JoMNJVhi"}
PORTRAIT = {"Sealwright": "b_K8qdNI651fTsRn9tfkk", "Oathkeeper": "6iwMYC8WTCGJTf2QIYfBz", "The Captain": "xm3F2YXkNPeLWHRAUnbmF"}
SCENE = {
    "exterior_keel_walk": "@img:scene_bg_ghost_ship_exterior_keel_walk.webp",
    "lower_hull": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi",
    "reconstruction_chamber": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJRiFRQZ0udmODoNtpa0FMcwI4k2Eq7nJhyvjl",
    "quarantined_archive": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJpo8lFZubKBAOsGCHyl3Sk0mZFrgWPUdjMJ75",
    "cache_site": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJyX6gwPukVH2MI5Lo4ehEfAXvZdcmtWqPg7rp",
    "chart_room": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJqpbYjW5dkOZgJQ8mGRcdx3SsWvPelyYFTt5V",
    "deck_b": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJcoxkatSnxBpQqGNDcTHbLmYz8uXAl3oa54ti",
    "helm": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJIp0fIvxfOewksxBoS1HQCihpL7c42Ky9uUFv",
    "command_observation_gallery": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ8ZwqPukkp45TvAnoIBa0rtCf1lbyXYjVKQ2q",
}
STEP_EXP = {"I": 1000, "II": 2000, "III": 3000, "IV": 4000, "V": 5000, "VI": 5000}
STEP_N = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
PACK_REF = "c371a8c1a8302ed23ba7287ed77cb780250dbb24"
IMAGES = {"icon-chart-quarantined-archive.webp": "art/skyglass_event_icons/exports/icon-chart-quarantined-archive.webp",
          "icon-chart-captains-watch.webp": "art/skyglass_event_icons/exports/icon-chart-captains-watch.webp",
          "scene_bg_ghost_ship_exterior_keel_walk.webp": "art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp"}


def effect(t, power, rounds, desc, calc="static"):
    return {"type": t, "power": power, "rounds": rounds, "target": "INHERIT", "direction": "defence", "calculation": calc,
            "powerPerLevel": 0, "description": desc, "appearSfx": "", "disappearSfx": "", "appearAnimation": "",
            "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": ""}


# Proposals (director to tune): the Archive alarm and the Watch terms (RUL-2026-10-24-021).
ALARM = [effect("increasedamagetaken", 20, 3, "The archive's alarm: you take 20% more damage for 3 rounds", "percentage")]
TERM = {1: [effect("elementalseal", 100, 99, "The Oathkeeper's term: your elemental jutsu are sealed")],
        2: [effect("disarm", 100, 99, "The Oathkeeper's term: you fight unarmed")],
        3: [effect("healprevent", 100, 99, "The Oathkeeper's term: no healing at the Captain's helm")]}


def dialog(i, scene, text, choices, portrait=None):
    return {"id": i, "task": "dialog", "description": text, "sceneBackground": SCENE[scene],
            "sceneCharacters": [PORTRAIT[portrait]] if portrait else [],
            "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}


def battle(i, scene, text, foes, nxt, retry, debuffs=None):
    counts = {}
    for f in foes: counts[f] = counts.get(f, 0) + 1
    o = {"id": i, "task": "start_battle", "description": text, "sceneBackground": SCENE[scene], "sceneCharacters": [],
         "opponentAIs": [{"ids": [AI[f]], "number": n, "quantity": 1} for f, n in counts.items()],
         "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False, "opponent_scaled_to_user": False,
         "nextObjectiveId": nxt, "failObjectiveId": "r_" + i,
         "failDescription": "You are driven back. Catch your breath and try again.",
         "drawDescription": "Neither side gives way. Try again.", "fleeDescription": "You fall back. Try again."}
    if debuffs: o["applyDebuffs"] = debuffs
    reset = {"id": "r_" + i, "task": "reset_quest", "description": "You were beaten back. The fight waits for you.",
             "sceneBackground": SCENE[scene], "sceneCharacters": [], "resetObjectiveId": retry}
    return [o, reset]


def win(i, scene, text, step):
    return {"id": i, "task": "win_quest", "description": text, "sceneBackground": SCENE[scene], "sceneCharacters": [],
            "reward_exp": STEP_EXP[step], "reward_items": [{"ids": [ITEM["treasury"]], "number": STEP_N[step], "quantity": 1}]}


def archive():
    objs, prev = [], {}
    nodes = H.ARCHIVE["nodes"]
    for (i, task, scene, src, text, edges, extra) in nodes:
        for _, tgt in edges: prev.setdefault(tgt, i)
    for (i, task, scene, src, text, edges, extra) in nodes:
        portrait = None  # Sealwright scene character pending push/140
        if task == "dialog":
            # A menu may not send two options to one node (validate.py): each wrong answer gets its own short beat
            # that leads on to the shared alarm.
            seen, out = {}, []
            for t, tgt in edges:
                seen[tgt] = seen.get(tgt, 0) + 1
            k = 0
            for t, tgt in edges:
                if seen[tgt] > 1:
                    k += 1
                    beat = f"{i}_wrong{k}"
                    objs.append(dialog(beat, scene, f"You choose: {t}. The seal flares red and the archive's alarm begins to toll.",
                                       [("Brace yourself", tgt)]))
                    out.append((t, beat))
                else:
                    out.append((t, tgt))
            objs.append(dialog(i, scene, text, out, portrait))
        elif task == "start_battle":
            objs += battle(i, scene, text, extra["fight"], edges[0][1], prev[i], ALARM if i.startswith("b_alarm") else None)
        elif task == "win_quest":
            objs.append(win(i, scene, text, extra["step"]))
    return objs


def watch():
    o = []
    land = H.WATCH["nodes"][0]
    o.append(dialog("d_landing", "cache_site", land[4], [("Board the boat", "d_term1")], "Oathkeeper"))
    T1 = H.WATCH["nodes"][1][4]
    T2 = "On deck the First Blade waits in the uniform of a dead era, twin cleavers forming from the gale. 'Finally. Something new.' The Oathkeeper speaks from the rail: 'Meet him with empty hands.'"
    T3 = H.WATCH["nodes"][6][4]
    fights = {1: ("chart_room", "Wayfinder", "The Wayfinder redraws the room around you.", "Your seal-work goes quiet. The Wayfinder waits."),
              2: ("deck_b", "First Blade", "The First Blade steps forward.", "You set your weapons down. The First Blade grins."),
              3: ("helm", "The Captain", "The Captain steps down from the command dais.", "The Oathkeeper seals the helm against healing. The Captain draws.")}
    intro = {1: (T1, "Oathkeeper"), 2: (T2, "Oathkeeper"), 3: (T3, "The Captain")}

    def term_node(n, c):  # the term offer for fight n with c terms accepted so far
        return f"d_term{n}" if n == 1 else f"d_term{n}_{c}"

    def after(n, c):
        if n < 3: return term_node(n + 1, c)
        return "d_gallery_" + ("IV" if c == 0 else "VI" if c == 3 else "V")

    for n in (1, 2, 3):
        scene, foe, fight_text, accept_text = fights[n]
        for c in ([0] if n == 1 else range(n)):
            t = term_node(n, c)
            text, portrait = intro[n]
            o.append(dialog(t, scene, text, [("Accept the term", f"d{n}t_{c}"), ("Refuse and fight", f"d{n}_{c}")], portrait))
            o.append(dialog(f"d{n}_{c}", scene, "You refuse the term. " + fight_text, [("Fight", f"b{n}_{c}")]))
            o.append(dialog(f"d{n}t_{c}", scene, accept_text, [("Fight", f"b{n}t_{c}")]))
            o += battle(f"b{n}_{c}", scene, fight_text, [foe], after(n, c), f"d{n}_{c}")
            o += battle(f"b{n}t_{c}", scene, fight_text + " You fight under the Oathkeeper's term.", [foe], after(n, c + 1), f"d{n}t_{c}", TERM[n])
    gal = H.WATCH["nodes"][8][4]
    for step in ("IV", "V", "VI"):
        o.append(dialog("d_gallery_" + step, "command_observation_gallery", gal, [("Claim the watch's stores", "w_" + step)]))
    for (i, task, scene, src, text, edges, extra) in H.WATCH["nodes"][9:]:
        o.append(win(i, scene, text, extra["step"]))
    return o


def quest(src, name, desc, success, chart, image, objectives, reward, rank):
    return {"entity": "quest", "slot": "create", "name": name, "srcId": src, "data": {
        "name": name, "description": desc, "image": image, "questType": "battlepyramid", "questRank": rank,
        "successDescription": success, "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True, "requiredLevel": 1, "maxLevel": 100,
        "maxAttempts": 100, "maxCompletes": 100, "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None,
        "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives, "sceneBackground": "", "sceneCharacters": [],
                    "entryItems": [{"ids": [chart], "number": 1}], "isolated": True,
                    "rewardMode": "choose", "rewardPickCount": 1, "reward": reward}}}


def items_reward(*entries, **scalars):
    r = {"reward_items": [{"ids": [i], "number": 100, "quantity": q} for i, q in entries]}
    r.update(scalars)
    return r


def main():
    items = [
        quest("hunt_archive", "The Quarantined Archive", H.ARCHIVE["premise"],
              "The archive's last seal is broken and its records are yours.", ITEM["chart_archive"],
              "@img:icon-chart-quarantined-archive.webp", archive(),
              items_reward((ITEM["case"], 1), (ITEM["strongbox"], 1), reward_exp=15000), "A"),
        quest("hunt_watch", "The Captain's Watch", H.WATCH["premise"],
              "You kept the Captain's watch and claimed its stores.", ITEM["chart_watch"],
              "@img:icon-chart-captains-watch.webp", watch(),
              items_reward((ITEM["coffer"], 1), (ITEM["inro"], 3), reward_money=50000), "A"),
    ]
    files = {}
    for name, path in IMAGES.items():
        b = open(os.path.join(ROOT, path), "rb").read()
        files[name] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    m = {"_note": ("Skyglass treasure hunts, step 1 (push/264): the Quarantined Archive and the Captain's Watch as HIDDEN, isolated "
                   "Battle Pyramids (director 2026-10-25: hidden push of everything). Entry: their Chart (consumed at start). Every "
                   "battle sits behind its own dialog and loses to a reset that returns to that dialog; the Watch carries the count "
                   "of accepted terms in its node ids so a retry keeps the same terms. Endings pay the exp ladder and the Sealed "
                   "Treasury at 1% per step; completion is pick 1 (Archive: Chart Case / Sage's Strongbox / 15,000 exp; Watch: "
                   "Skyglass Coffer / 50,000 ryo / Medicine Inro x3). PROPOSALS for the director: the exp and ryo pick amounts, "
                   "questRank A, no level gate, the alarm debuff (20% more damage taken, 3 rounds) and the three terms (whole-fight "
                   "elemental seal, disarm, heal prevent). maxAttempts/maxCompletes 100 (the engine cap). Portraits use the "
                   "Sealwright/Oathkeeper/Captain scene characters (Sealwright and Oathkeeper images wait on push/140). Generated "
                   "by push/264_skyglass_hunts.gen.py; do not hand-edit."),
         "dedupNames": True, "imgSizes": {k: v["bytes"] for k, v in files.items()},
         "imagePack": {"ref": PACK_REF, "files": files}, "items": items}
    json.dump(m, open(os.path.join(ROOT, "push/264_skyglass_hunts_create.json"), "w"), indent=1)
    for it in items: print(it["name"], len(it["data"]["content"]["objectives"]), "objectives")


if __name__ == "__main__":
    main()
