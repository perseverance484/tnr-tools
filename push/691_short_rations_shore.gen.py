"""push/691: rebuild Short Rations (Gqbnq2LVtIVBlLYlAnam1, HIDDEN) so its fights are the
shore crew from push/690. Director, Nov 20 16:35Z: 'Switch Short Rations'.

Each fight is a defeat_opponents objective bound to one shore placement (one win per step).
A dialog sits between the three Deckhand steps because all three Deckhands share one AI:
without a stop between them, one win could close every Deckhand step in the same pass.
Same reward (3 Wreck Salvage, 1000 exp), level 30-100, id unchanged. Prints the full
quests.update payload (whole record, read back first) to stdout."""
import json, sys

SALVAGER = "goagM4WhKWtnVb8oP5euM"
DECK = ["N142XR4hbrfHaIEE7Z-BL", "v329QMIIE8NCr5ScXwQrj", "1hQvqkHGhNw-XhBRQxREv"]
MATE = "W8WZoQ1q7T8-5nnosdDPm"
DECK_AI, MATE_AI = "mm3C1bhpSuturfXR1hyPS", "Ys9d_kNoBoVaAsFfh6_DN"
SALVAGE = "mW6_ZGtGcCSuXGPhn-H4o"
BEACH = "https://ui0arpl8sm.ufs.sh/f/QfsAnXSp9QG0AuwbQywCW.webp"

REWARD0 = {"reward_exp": 0, "reward_rank": "NONE", "reward_items": [], "reward_money": 0,
  "reward_badges": [], "reward_jutsus": [], "reward_titles": [], "reward_tokens": 0,
  "reward_prestige": 0, "reward_anbupoints": 0, "reward_bloodlines": [], "reward_clanpoints": 0,
  "reward_reputation": 0, "reward_sage_modes": [], "reward_war_damage": 0, "reward_skillpoints": 0,
  "reward_war_healing": 0, "reward_hunter_items": False, "reward_seichi_silver": 0,
  "reward_gathering_items": False, "reward_hunter_items_ids": [], "reward_hunting_experience": 0,
  "reward_medical_experience": 0, "reward_village_membership": "NONE",
  "reward_crafting_experience": 0, "reward_gathering_items_ids": [],
  "reward_gathering_experience": 0, "reward_sage_mastery_experience": 0}
LOC = {"locationName": "", "locationDescription": "", "structureAssetId": "", "structureScale": 1,
       "successDescription": ""}

def dialog(oid, text, choice, nxt, bg=BEACH, chars=None, placement=None):
    o = {"id": oid, "task": "dialog", "image": "", "attackers": [], "description": text,
         "nextObjectiveId": [{"text": choice, "nextObjectiveId": nxt}],
         "sceneBackground": bg, "sceneCharacters": chars or [],
         "attackers_scale_gains": 1, "attackers_max_per_battle": 1,
         "attackers_scaled_to_user": False, **LOC, **REWARD0}
    if placement: o["overworldPlacementId"] = placement
    return o

def fight(oid, placement, ai, text, nxt):
    return {"id": oid, "task": "defeat_opponents", "overworldPlacementId": placement,
            "opponentAIs": [{"ids": [ai], "number": 1}], "allyAIs": [],
            "description": text, "nextObjectiveId": nxt, "failObjectiveId": "f_lost",
            "opponent_scaled_to_user": True, "completionOutcome": "Win", "scaleGains": 1,
            "keepOriginalPools": False, "givePools": 100, "applyBuffs": [], "applyDebuffs": [],
            "failDescription": "You are defeated.",
            "fleeDescription": "You break away, and the tide closes behind you.",
            "drawDescription": "The fight stalls, and the tide takes the way back.",
            "sceneBackground": BEACH, "sceneCharacters": [], **LOC, **REWARD0}

def end(oid, task, text, **reward):
    return {"id": oid, "task": task, "description": text, "sceneBackground": BEACH,
            "sceneCharacters": [], **LOC, **{**REWARD0, **reward}}

objectives = [
  dialog("d_ask", "\"Their galley's bare, so they've come ashore to fill it, from my crates. "
         "Thin them out and I'll pay you.\" Down the shore, a deckhand is prising the lid off one "
         "of her crates.", "Cut him off", "b1", bg="rX78pJPETsUL2JrsSvGHn",
         chars=["Xugt7415D3-tepLfxpwM5"], placement=SALVAGER),
  fight("b1", DECK[0], DECK_AI, "The deckhand nearest her fire drops the lid and turns to you, "
        "the way he'd turn to an order.", "d_d2"),
  dialog("d_d2", "A second deckhand is further down the sand, filling a sack with her dried fish "
         "for the galley.", "Take the sack", "b2"),
  fight("b2", DECK[1], DECK_AI, "He knots the sack shut and comes at you with it.", "d_d3"),
  dialog("d_d3", "The third is near the water's edge, rolling one of her casks toward the hull.",
         "Stop the cask", "b3"),
  fight("b3", DECK[2], DECK_AI, "He lets the cask roll and comes up the sand at you.", "d_mate"),
  dialog("d_mate", "At the north end of the shore the Galley Mate is ticking off what the crew "
         "brought in. He doesn't look up.", "Take the list off him", "b4"),
  fight("b4", MATE, MATE_AI, "The Mate closes his list and calls the galley to order.", "w_done"),
  end("w_done", "win_quest", "Her crates stay on her sand, and their galley stays empty, for "
      "today. You bring back what they were hauling.", reward_exp=1000,
      reward_items=[{"ids": [SALVAGE], "number": 100, "quantity": 3}]),
  end("f_lost", "fail_quest", "The crew carry on past you, arms full for the galley. The tide "
      "will turn again tomorrow."),
]

live = json.load(open(sys.argv[1]))  # full quests.get read, saved before the edit
# Read-only, runtime or inert fields the quest write validator drops (law 72) or flags (law 42).
DROP = {"id", "createdAt", "updatedAt", "teamMaxPlayers", "raidMaxPlayers", "raidStartedAt",
        "raidEndsAt", "raidCaptureDeadline", "raidGracePeriodEnd", "huntingRank",
        "gatheringRank", "medicalRank"}
data = {k: v for k, v in live.items() if k not in DROP}
data["description"] = (
  "The Wreck's galley is bare, so its crew have come ashore to fill it, and they're filling it "
  "from the Salvager's crates. Thin them out: 3 Foraging Deckhands and their Galley Mate, for 3 "
  "Wreck Salvage.<br><br><i>Ask the Salvager at her fire on the beach below the Wreck (sector "
  "210). The crew wander the shore, and the quest marks the one you're after. Enemies match your "
  "level. You start each fight at full health, chakra and stamina. Lose one and the job ends.</i>")
data["content"] = {**live["content"], "objectives": objectives}
assert data["hidden"] is True and data["questType"] == "overworld"
json.dump({"id": live["id"], "data": data}, sys.stdout, ensure_ascii=False)
