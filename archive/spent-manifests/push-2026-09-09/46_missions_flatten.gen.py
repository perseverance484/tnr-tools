#!/usr/bin/env python3
"""
push/46_missions_flatten.gen.py

Flattens the ten Forsworn missions to a 4-node shape:
    n1 dialog (hook)  ->  n2 start_battle  ->  n3 dialog (payoff)  ->  n4 win_quest

Ruling (dauntless, this session): flatten all ten, A-ranks included.
Missions are flavor on the way to gains, not a challenge or a puzzle.

Source of truth for every top-level field and for content.reward is the live
capture harvests/inbox/tnr_results_1788136356379.json - the newest bundle that
carries all ten with full content. Nothing is transcribed.

Removes: all collect_item, move_to_location, reset_quest, all branching, and
all defeat_opponents (which require sectorType+locationType, ie forced travel).
start_battle requires no location, so the fight happens where the player stands.

Balance untouched: every node-level reward in the live records is zero, so the
whole payout already sits at content.reward and is re-asserted verbatim.

Em dashes are banned in node description and choice text. None are used here.
"""
import json
import os

CAPTURE = "harvests/inbox/tnr_results_1788136356379.json"
OUT = "push/46_missions_flatten.json"

# Top-level field set copied from the known-good whole-record quest edit
# push/34_old_ghost_prose.json. Excludes createdAt / updatedAt / village.
TOP_FIELDS = [
    "id", "name", "image", "description", "successDescription", "questRank",
    "medicalRank", "huntingRank", "gatheringRank", "requiredLevel",
    "requiredFarmingLevel", "prerequisiteQuestId", "tierLevel", "questType",
    "content", "hidden", "consecutiveObjectives", "requiredVillage",
    "requiredBloodlineId", "requiredSageModeId", "requiredSageRank",
    "maxLevel", "maxAttempts", "maxCompletes", "retryDelay", "attemptDelay",
    "endsAt", "startsAt", "raidBossMaxHealth", "raidBossCurrentHealth",
    # raidEndsAt / raidCaptureDeadline / raidGracePeriodEnd are deliberately
    # NOT re-asserted: law 72, they are not fields of the quest write
    # validator and would be dropped or rejected. They are null on all ten.
]

# id -> (boss AI id, hook line, choice text, fight line, payoff line)
# Boss AI ids are the final-fight opponents lifted from the live records.
PLAN = {
    # ---- C rank, Unmarked tier ----
    "Sx_NfWziba6NYOEsfXrS5": (  # Chalk and Corner
        "I6bph15IwA0--iAwacxIn",
        "Fresh chalk on the corner stone. Three strokes, angled north. "
        "<br> <br> Someone is marking routes through our streets.",
        "Wait for whoever comes back.",
        "A figure crouches to add a fourth stroke and finds you already there.",
        "The marks come off with water. Whoever taught them the code is still out there.",
    ),
    "otFtGNvBFn8ZVGlda7UOH": (  # Protection
        "JBTjl1mvOWRfTPX0Igj03",
        "The noodle stand pays someone every week. It is not the village. "
        "<br> <br> The owner will not say the name out loud.",
        "Collect on their behalf.",
        "The collector arrives on schedule and reaches for the box.",
        "The stand keeps its coin this week. Next week is a different question.",
    ),
    "9kzvd414kRRXauKSXsGIq": (  # The Empty Contract
        "bCTTWqMLn_clRjR21aB2N",
        "A bounty contract on the board with the name cut out of it. "
        "<br> <br> Everything else is filled in. Rank, sector, payment.",
        "Work it anyway.",
        "You find the target exactly where the blank contract said they would be.",
        "Someone wanted this one taken without wanting it written down.",
    ),
    "ATV6Fs3XFqOf7wch99qDW": (  # The Waystation
        "JBTjl1mvOWRfTPX0Igj03",
        "The road shelter has been used. Rations, bedding, a cold fire pit. "
        "<br> <br> None of it is village issue.",
        "Hold the shelter.",
        "They come back for the cache and do not expect it to be occupied.",
        "The waystation is ours again. There are others on this road.",
    ),
    # ---- B rank, Faceless tier ----
    "s7Lnjsv-9Fvo4_YEzq-3w": (  # Nothing to Report
        "SJs7nn-cUwy-VtLt_vMwC",
        "The patrol log reads clean for six straight nights. "
        "<br> <br> The sector is not clean. You have seen it.",
        "Walk the route yourself.",
        "Halfway along the route, you learn why the log stayed empty.",
        "The log was not wrong. It was written by someone being paid to write it.",
    ),
    "ilYoJqbk--np9OSqT9lGx": (  # The Loud Way
        "2ZF5jMvECgiNBgrr4icqk",
        "They burned the granary in daylight with the doors open. "
        "<br> <br> Quiet was never the point.",
        "Go straight at them.",
        "One of them stayed behind to be seen. That was always the assignment.",
        "They wanted witnesses. Now the village has one who fought back.",
    ),
    # ---- A rank, Named ----
    "KmGPDnZnGOCvATQqA5LI8": (  # Old Ghost
        "g8l7lt-ua1ptrWvhqjrnl",
        "An old bounty contract, faded, pinned beside a fresh brief. "
        "<br> <br> Old Ghost ran an ANBU cell here once. He is back.",
        "Take the contract.",
        "He does not run. He waited for someone from the village to come.",
        "He knew every name on the wall. That is why they sent him away.",
    ),
    "WxsmoaAoV0y8vqcWYw96y_UNUSED": None,  # guard against id/AI mixup
    "WIsqHEoo4c-ToRaV5_cZj": (  # The Long Winter
        "WxsmoaAoV0y8vqcWYw96y",
        "Winter Crow has not moved camp in four months. "
        "<br> <br> She is not hiding. She is waiting for the village to get tired.",
        "End the wait.",
        "She stands up as you enter the clearing, unhurried, already reaching.",
        "She outlasted three hunters before you. She did not outlast the fourth.",
    ),
    "8ndqsf6RBZ88q3pfyZQQh": (  # The Tenth Name
        "2ZF5jMvECgiNBgrr4icqk",
        "Nine names on the Forsworn list are crossed out. "
        "<br> <br> The tenth has no crossing and no face.",
        "Hunt the tenth.",
        "The one who answers to the tenth name meets you without introducing themselves.",
        "The list is closed. Nobody is sure the tenth name was ever a person.",
    ),
    "fBQNC1wFqTPYp7reiK79T": (  # Three Rounds
        "yTHaQ_sdw-JW0C35W-Uo9",
        "Pale Fang has beaten two village hunters and let both walk home. "
        "<br> <br> He sent word that he will give a third the same courtesy.",
        "Be the third.",
        "He salutes before he moves. He means it, and it does not slow him down.",
        "He let the first two go to make sure a third would come.",
    ),
}
PLAN.pop("WxsmoaAoV0y8vqcWYw96y_UNUSED", None)


def blank_rewards(template_node):
    """Zeroed reward field set lifted from a live node, so no field is invented."""
    return {k: (list(v) if isinstance(v, list) else v)
            for k, v in template_node.items() if k.startswith("reward_")}


def load_live():
    recs = {}

    def walk(o):
        if isinstance(o, dict):
            c = o.get("content")
            if isinstance(c, dict) and isinstance(c.get("objectives"), list) \
                    and o.get("id") in PLAN:
                recs[o["id"]] = o
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(json.load(open(CAPTURE)))
    return recs


def build_objectives(rec, boss, hook, choice, fight, payoff):
    c = rec["content"]
    bg = c.get("sceneBackground", "")
    chars = list(c.get("sceneCharacters", []))
    objs = rec["content"]["objectives"]
    dlg_t = next(o for o in objs if o["task"] == "dialog")
    win_t = next(o for o in objs if o["task"] == "win_quest")
    battle_src = next(o for o in objs
                      if o["task"] in ("defeat_opponents", "start_battle"))
    r_dlg = blank_rewards(dlg_t)
    r_win = blank_rewards(win_t)

    n1 = dict(r_dlg)
    n1.update({
        "id": "f1", "task": "dialog", "image": "", "description": hook,
        "successDescription": "",
        "nextObjectiveId": [{"text": choice, "nextObjectiveId": "f2"}],
        "sceneBackground": bg, "sceneCharacters": chars,
        "attackers": [], "attackers_scaled_to_user": True,
        "attackers_scale_gains": 1, "attackers_max_per_battle": 1,
    })

    n2 = dict(r_dlg)
    for k in ("attackers", "attackers_scaled_to_user",
              "attackers_scale_gains", "attackers_max_per_battle"):
        n2.pop(k, None)
    n2.update({
        "id": "f2", "task": "start_battle", "image": "",
        "description": fight,
        "successDescription": "Target down.",
        "opponentAIs": [{"ids": [boss], "number": 1, "quantity": 1}],
        "opponent_scaled_to_user": True,
        "completionOutcome": "Win",
        # Self-edge f2 -> f2 closes a cycle and the builder's q.fill flow
        # validator rejects it. Loss routes through a reset_quest hop instead,
        # so a defeat just puts the player back at the fight. Off the happy
        # path, so the win route is still four taps.
        "failObjectiveId": "rs_f2",
        "failDescription": battle_src.get(
            "failDescription", "You failed to defeat the opponent"),
        "fleeDescription": battle_src.get(
            "fleeDescription", "You fled from the opponent"),
        "drawDescription": battle_src.get(
            "drawDescription", "The battle ended in a draw"),
        "nextObjectiveId": "f3",
        "sceneBackground": bg, "sceneCharacters": chars,
    })

    n3 = dict(r_dlg)
    n3.update({
        "id": "f3", "task": "dialog", "image": "", "description": payoff,
        "successDescription": "",
        "nextObjectiveId": [{"text": "File the report.",
                             "nextObjectiveId": "f_win"}],
        "sceneBackground": bg, "sceneCharacters": chars,
        "attackers": [], "attackers_scaled_to_user": True,
        "attackers_scale_gains": 1, "attackers_max_per_battle": 1,
    })

    n4 = dict(r_win)
    n4.update({
        "id": "f_win", "task": "win_quest",
        "description": "Contract closed.",
        "successDescription": "Mission complete.",
        "sceneBackground": bg, "sceneCharacters": chars,
    })

    # Off-path retry hop. Only reached on a loss.
    rs = dict(r_win)
    rs.update({
        "id": "rs_f2", "task": "reset_quest",
        "description": "Go again.",
        "successDescription": "",
        "resetObjectiveId": "f2",
        "sceneBackground": bg, "sceneCharacters": chars,
    })
    return [n1, n2, n3, n4, rs]


def main():
    live = load_live()
    missing = [q for q in PLAN if q not in live]
    if missing:
        raise SystemExit("live record missing for: %s" % missing)

    items = []
    order = ["Sx_NfWziba6NYOEsfXrS5", "otFtGNvBFn8ZVGlda7UOH",
             "9kzvd414kRRXauKSXsGIq", "ATV6Fs3XFqOf7wch99qDW",
             "s7Lnjsv-9Fvo4_YEzq-3w", "ilYoJqbk--np9OSqT9lGx",
             "KmGPDnZnGOCvATQqA5LI8", "WIsqHEoo4c-ToRaV5_cZj",
             "8ndqsf6RBZ88q3pfyZQQh", "fBQNC1wFqTPYp7reiK79T"]
    for qid in order:
        rec = live[qid]
        boss, hook, choice, fight, payoff = PLAN[qid]
        data = {}
        for f in TOP_FIELDS:
            if f in rec:
                data[f] = rec[f]
        content = dict(rec["content"])
        content["objectives"] = build_objectives(
            rec, boss, hook, choice, fight, payoff)
        data["content"] = content
        data["consecutiveObjectives"] = True   # law 23: always explicit
        items.append({
            "entity": "quest",
            "slot": "edit",
            "name": "%s [flatten 4-node]" % rec["name"],
            "targetId": qid,
            "data": data,
        })

    manifest = {
        "version": 1,
        "note": "Flatten the ten Forsworn missions to dialog / start_battle / "
                "dialog / win_quest. Zero forced travel. Balance untouched: "
                "content.reward re-asserted verbatim, all node rewards were "
                "already zero.",
        "dedupNames": True,
        "items": items,
    }
    os.makedirs("push", exist_ok=True)
    json.dump(manifest, open(OUT, "w"), indent=1)
    print("wrote %s: %d quest edits" % (OUT, len(items)))
    for it in items:
        o = it["data"]["content"]["objectives"]
        print("  %-30s %d nodes  %s" % (
            it["data"]["name"][:30], len(o),
            " -> ".join(n["task"] for n in o)))


if __name__ == "__main__":
    main()
