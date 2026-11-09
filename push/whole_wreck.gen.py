#!/usr/bin/env python3
"""The Whole Wreck: hidden staff walk-through of the Skyglass event (Nov 9 2026, dauntless's go).
One non-isolated battlepyramid quest (no entry item, no edit lock, never bulk-assigned like an event).
She explains each piece, hands over its real items, and offers each boss as players face it, or Move on.
Every fight: any result moves on, full pools at start, no hospital. Mother of Echoes acts 2-3 carry HP;
a loss in any act ends the three acts. Writes push/583_the_whole_wreck.json (run from the repository root)."""
import json, os

BEACH = "rX78pJPETsUL2JrsSvGHn"          # Wreck Sighted's shore
SALVAGER = ["Xugt7415D3-tepLfxpwM5"]      # her scene character (Wreck Sighted)
LOWTIDE_BG = "dFwyPzyhUZQjDBXpJRUDJ"      # Low Tide Run breach
WRECK_BG = "yufttCkG-KsefHKuz9Q2a"        # Low Tide Run hold
DRIFT_BG = "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJIp0fIvxfOewksxBoS1HQCihpL7c42Ky9uUFv"
MENDER_BG = "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJRiFRQZ0udmODoNtpa0FMcwI4k2Eq7nJhyvjl"
CROWN_BG = "yoq9zYoprHZnM1EDc3ZTk"        # Crownhold floor 5
MOE_BG = "81DATu13hATfbkPuLT54E"          # Mother of Echoes hall
IMAGE = "https://ui0arpl8sm.ufs.sh/f/G7m7lRtuN6-aC2n2QyP3b.png"  # Wreck Sighted icon

IT = dict(tide="H1s2IwtZ5JqgPEoJ55IVj", salvage="mW6_ZGtGcCSuXGPhn-H4o",
          cache="nbLC37UzBamthKXvZsgQB", foundry="pY-0O5Gs2n89pf0kYb5J2", archive="cRZT41zm5vhPTQwwn8vtv",
          watch="aHFNuo5RkKpDcaOBLIKiu", seal="sVqDdYUJIxxRYbmKbbxo0", heading="s1mYHuKqw2YuzIzxVwU-_",
          closing="oQcPHpr0sqmWHfaJPR4T_", lantern="jCJv4N3JSiihuqnK0jJ7t",
          keel="uKnlqlfyE_k1QjLuaVml_", crown="4UNvgWIDGD9QpNVtLr1aM", tidesh="KHGZAfQFosLQJ29AN2ymC",
          ledger="cGrmhfe88ACBvFk2XqvSu")
AI = dict(lt_warden="3qlQV9EAnTZldvyhv3YnM", lt_seal="lY1qD7dPuxs1rhCFFDitU",
          warden="texZaFi42S3EvJZBwQ8cd", sealch="wTgO-Q32caSSd0is1QIS7", sentinel="3V_gdHYaclMB1gTyOPAbV",
          blade="d6g0mOM7RBSsYI1hrUVT9", oath="0PZU_FvlbM3ErYGlD5r56", wayf="v7T9_XdGMfP46em0dPuBc",
          horror="AQi-bHJ-5tHXtxrnc0P9E", captain="QY69h271Nx9uHrBeR6jwW", sealwright="RBW5KsIXmTGR710D2y2Y7",
          dl_captain="xTfDUSDalduRg43MlcCbO", mender="6_c1fpF8YXIjoaLX0mIRT", crowned="7QofodAiUwIoM-voiA2p6",
          moe1a="fJLcH1mpB1XHHGtNWwvzD", moe1b="IhNR-W1FElTsrWw1KfuQ9", moe2="H3pNj2qUWpMpVRINiH6Vn",
          moe3="k0hgSrghl_KcYs9ATVDJT")

def opp(*pairs):
    return [{"ids": [AI[k]], "number": n, "quantity": 1} for k, n in pairs]

def items(*pairs):
    return [{"ids": [IT[k]], "number": 100, "quantity": q} for k, q in pairs]

def d(id, text, choices, bg=BEACH, chars=SALVAGER, give=None):
    o = {"id": id, "task": "dialog", "description": text, "sceneBackground": bg, "sceneCharacters": list(chars),
         "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}
    if give:
        o["reward_items"] = give
    return o

def b(id, text, opponents, nxt, bg, fail=None, outcome="Any", refill=True, scaled=False):
    o = {"id": id, "task": "start_battle", "description": text, "sceneBackground": bg, "sceneCharacters": [],
         "opponentAIs": opponents, "completionOutcome": outcome, "scaleGains": 1, "keepOriginalPools": True,
         "opponent_scaled_to_user": scaled, "nextObjectiveId": nxt, "failObjectiveId": fail or nxt,
         "failDescription": "The fight goes against you. She pulls you clear, and the walk-through goes on.",
         "drawDescription": "The fight stalls. She pulls you clear, and the walk-through goes on.",
         "fleeDescription": "You break away. She pulls you clear, and the walk-through goes on."}
    if refill:
        o["givePools"] = 100
    return o

I = lambda s: "<i>" + s + "</i><br><br>"
O = []
# 1. Wreck Sighted
O.append(d("d_s1", I("The salvager sits by her fire on the shore of 210, a rolled chart across her knees.") +
    "\"So you want the whole wreck, start to finish. Every Friday at 6 PM Central, a new hull surfaces and "
    "Wreck Sighted goes up on the Wake Island board. That quest is the kickoff: it sends people to the wreck, "
    "hands them this week's Watch Log and their first chart, and the wrecks stay open until Monday at 6 PM.\"<br>"
    "She holds out the chart. \"A Tide Chart. It opens the Low Tide Run. Want to meet the crew it sends you into?\"",
    [("Show me the Low Tide crew", "b_s1"), ("Move on", "d_s2")], give=items(("tide", 1))))
O.append(b("b_s1", "A Deck Warden and his Seal Charge step out of the breach, the first fight of the Low Tide Run.",
    opp(("lt_warden", 1), ("lt_seal", 1)), "d_s2", LOWTIDE_BG, scaled=True))
# 2. The Watch Log
O.append(d("d_s2", I("She taps a page pinned under a stone by the fire.") +
    "\"The Watch Log. Each page opens with a short story hook, then five challenges with their rewards, then the rules. "
    "There are two pages a week, one for levels 30 to 80 and one for 81 and up, and players pick theirs in Wreck Sighted. "
    "The pages hide on Wednesday, and Friday brings new ones. Nothing to do here, just know where they come from.\"",
    [("Got it", "d_s3")]))
# 3. Her shore at 210
O.append(d("d_s3", I("She drops a heavy sack at your feet. It clinks.") +
    "\"Wreck Salvage. Players earn it in the wrecks and the chart runs, and spend it with me. I trade a deck chart for 4, "
    "a hold chart for 10, a sealed chart for 20, and the Lastlight Lantern for 30, once a week. My trades and my shore jobs "
    "come to people at random, on their daily NPC rolls, so nobody farms me dry. Here's 30, go try a trade.\"",
    [("Continue", "d_s4")], give=items(("salvage", 30))))
# 4. The Wrecks
O.append(d("d_s4", I("She points at the two hulls on the reef, one grey with age, one glittering.") +
    "\"Those are the Wrecks. The Faded Wreck is for 30 and up, the full Skyglass Wreck for 80 and up. Both are party "
    "dungeons for three, and both drop salvage and charts. The full Wreck is five decks: Deck Wardens and a Seal Charge, "
    "the Sentinel and the First Blade, the Oathkeeper and the Wayfinder, the Core Horror, then the Captain and his "
    "Sealwright. They're tuned for three, so going in alone, expect to lose.\"",
    [("Take the decks one at a time", "b_w1"), ("Jump to the top deck", "d_w5"), ("Move on", "d_s5")]))
O.append(b("b_w1", "Two Deck Wardens and a Seal Charge hold the first deck.",
    opp(("warden", 2), ("sealch", 1)), "d_w2", WRECK_BG))
O.append(d("d_w2", I("Glass crunches under your feet on the way down.") + "\"The second deck. The Sentinel and the First Blade.\"",
    [("Next deck", "b_w2"), ("Leave the Wreck", "d_s5")], bg=WRECK_BG, chars=[]))
O.append(b("b_w2", "The Skyglass Sentinel and the First Blade turn as one.",
    opp(("sentinel", 1), ("blade", 1)), "d_w3", WRECK_BG))
O.append(d("d_w3", I("The third deck is quiet in the way a held breath is quiet.") + "\"The Oathkeeper and the Wayfinder.\"",
    [("Next deck", "b_w3"), ("Leave the Wreck", "d_s5")], bg=WRECK_BG, chars=[]))
O.append(b("b_w3", "The Oathkeeper raises his hand, and the Wayfinder marks your way out before you take it.",
    opp(("oath", 1), ("wayf", 1)), "d_w4", WRECK_BG))
O.append(d("d_w4", I("Something in the fourth deck is breathing through the walls.") + "\"The Core Horror. Don't stand still.\"",
    [("Next deck", "b_w4"), ("Leave the Wreck", "d_s5")], bg=WRECK_BG, chars=[]))
O.append(b("b_w4", "The Core Horror pulls itself out of the hull.", opp(("horror", 1)), "d_w5", WRECK_BG))
O.append(d("d_w5", I("The top deck. Three Deck Wardens stand watch, and behind them a masked figure waits at the helm.") +
    "\"The last deck comes in two waves: three Deck Wardens first, then the Captain and the Sealwright.\"",
    [("Face the Deck Wardens", "b_w5a"), ("Leave the Wreck", "d_s5")], bg=WRECK_BG, chars=[]))
O.append(b("b_w5a", "Three Deck Wardens close ranks around the helm.", opp(("warden", 3)), "d_w5b", WRECK_BG))
O.append(d("d_w5b", I("The Captain steps down from the helm, and the Sealwright walks at his side.") +
    "\"There he is. This is the fight the whole Wreck builds to.\"",
    [("Face the Captain", "b_w5b"), ("Leave the Wreck", "d_s5")], bg=WRECK_BG, chars=[]))
O.append(b("b_w5b", "The Captain and the Sealwright.", opp(("captain", 1), ("sealwright", 1)), "d_s5", WRECK_BG))
# 5. Charts and runs
O.append(d("d_s5", I("Back at the fire, she fans out six charts like a hand of cards.") +
    "\"Charts are the solo side. Each one opens a Battle Pyramid run and is spent when the run starts. HP carries from "
    "fight to fight, a loss ends the run, and runs pay salvage and better charts back. Every run plays a little differently: "
    "terms you bargain for, the riddle door, the push-your-luck Haul, the run backwards, and the tainted route once a chart "
    "is steeped in Core Rot. Here's one of each deep chart, so you can play them later.\"",
    [("Continue", "d_s6")], give=items(("cache", 1), ("foundry", 1), ("archive", 1), ("watch", 1), ("seal", 1), ("heading", 1))))
# 6. The Driftline
O.append(d("d_s6", I("She nods down the beach, where the tide runs out farther than it should.") +
    "\"The Driftline. That's the 30 to 80 band's own story: its own runs and its own bosses, so newer players have a road "
    "of their own. At the end of it waits the Driftline Captain.\"",
    [("Fight the Driftline Captain", "b_s6"), ("Move on", "d_s7")]))
O.append(b("b_s6", "The Driftline Captain takes the helm of the broken stern.", opp(("dl_captain", 1)), "d_s7", DRIFT_BG, scaled=True))
# 7. The Hullbound Mender
O.append(d("d_s7", I("She hands you a chart that smells of pitch and wet timber.") +
    "\"The Hullbound Mender. His hold shrinks while you fight: he lays hull tiles, drops planks and splits the keel, and "
    "the walls keep coming in. His chart only drops in the Wreck, it's never sold. That's the Chart of the Closing Hold.\"",
    [("Fight him", "b_s7"), ("Move on", "d_s8")], give=items(("closing", 1))))
O.append(b("b_s7", "The Hullbound Mender sets down his mallet and picks up another.", opp(("mender", 1)), "d_s8", MENDER_BG))
# 8. Crownhold
O.append(d("d_s8", I("She sets a small lantern in your hands. Its light does not flicker in the wind.") +
    "\"The Lastlight Lantern. It opens Crownhold, the climb up the mountain: rites, allies and alarms, decided by how you "
    "climb. Players get the Lantern from my weekly trade or, rarely, from the Wreck. At the top sits the Crowned Captain.\"",
    [("Fight the Crowned Captain", "b_s8"), ("Move on", "d_s9")], give=items(("lantern", 1))))
O.append(b("b_s8", "The Crowned Captain turns from the window, his Command Crown pale as frost.", opp(("crowned", 1)), "d_s9", CROWN_BG))
# 9. Mother of Echoes
O.append(d("d_s9", I("She lays four shards on a cloth, and they ring faintly against each other.") +
    "\"The four shards. Keel from the Wreck and the Mender's hold, Crown from Crownhold, Tide from the Epic chart runs, "
    "Ledger from the Haul. Together they open the Mother of Echoes: three acts, one continuous fight, HP carried from act "
    "to act, and losing any act ends it.\"",
    [("Fight all three acts", "b_m1"), ("Move on", "d_s10")], give=items(("keel", 1), ("crown", 1), ("tidesh", 1), ("ledger", 1))))
O.append(b("b_m1", "Act one. The Mother Glass is singing.", opp(("moe1a", 1), ("moe1b", 1)), "d_m2", MOE_BG,
    fail="d_m_lost", outcome="Win"))
O.append(d("d_m2", I("The deep goes quiet, but the glass does not.") +
    "\"Act two. You keep the HP you have.\"", [("Hold your ground", "b_m2"), ("Step back out", "d_s10")], bg=MOE_BG, chars=[]))
O.append(b("b_m2", "Act two. She has started to remember you.", opp(("moe2", 1)), "d_m3", MOE_BG,
    fail="d_m_lost", outcome="Win", refill=False))
O.append(d("d_m3", I("Every pane in the hall turns toward you.") +
    "\"Act three. The Silence has stopped holding back.\"", [("Do not hold still", "b_m3"), ("Step back out", "d_s10")],
    bg=MOE_BG, chars=[]))
O.append(b("b_m3", "Act three. The Silence.", opp(("moe3", 1)), "d_s10", MOE_BG,
    fail="d_m_lost", outcome="Win", refill=False))
O.append(d("d_m_lost", I("The glass throws you back onto the sand.") +
    "\"In a real run, that's the end of it. Here, we just keep walking.\"", [("Continue", "d_s10")]))
# 10. Back at her fire
O.append(d("d_s10", I("The fire has burned low. Out on the reef, the glass is already growing back.") +
    "\"That's the whole wreck. Every week the glass grows back and a new hull surfaces on Friday, with a new page of the "
    "story. Everything I gave you is real, so play the full runs whenever you like.\"",
    [("Thank her", "w_done")]))
O.append({"id": "w_done", "task": "win_quest", "description": "You walked the whole wreck, start to finish.",
          "sceneBackground": BEACH, "sceneCharacters": []})

quest = {
    "name": "The Whole Wreck",
    "description": "Staff walk-through of the Skyglass event. The salvager explains every piece in order, hands over "
                   "the real items, and offers each boss as players face it, or a way to move on. Nothing is required.",
    "image": IMAGE, "questType": "battlepyramid", "questRank": "D",
    "successDescription": "You walked the whole wreck, start to finish.",
    "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
    "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,
    "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
    "startsAt": None, "endsAt": None,
    "content": {"objectives": O, "sceneBackground": BEACH, "sceneCharacters": [], "isolated": False,
                "reward": {}},
}
man = {"_note": "push/583, The Whole Wreck, HIDDEN staff walk-through (one non-isolated battlepyramid quest, D rank, no entry "
                "item). dauntless's go Nov 9 2026 4:55 PM CT. Generated by push/whole_wreck.gen.py; do not hand-edit.",
       "items": [{"entity": "quest", "slot": "create", "srcId": "ww_quest", "name": "The Whole Wreck", "data": quest}]}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "583_the_whole_wreck.json")
json.dump(man, open(out, "w"), indent=1, ensure_ascii=False)
print(out, len(O), "objectives")
