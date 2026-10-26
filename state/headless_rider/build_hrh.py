"""Headless Rider Horror!: rider AI create + quest edit adding the rider battle.

Graph change (only the tail; every other node is re-asserted verbatim from the capture):
  V0IDs (dialog, rider charges)  -> hrSqd  (was -> 66Dq0)
  hrSqd (dialog, squad arrives; text moved from 66Dq0) -> hrBat
  hrBat (start_battle vs Headless Rider) win -> 66Dq0, loss -> hrRst
  hrRst (reset_quest) -> hrSqd
  66Dq0 (win_quest) keeps its id; description becomes the closing line.
"""
import copy, json, os, sys
sys.path.insert(0, "/home/claude/tnr-tools/skills/building-tnr-content/scripts")
from factory import Factory
import enemy

CAPTURE = sys.argv[1]
OUT = sys.argv[2]
f = Factory()
pool = enemy.load_pool()

# ---------------------------------------------------------------- rider AI
LEVEL = 110
KIT = ["B20", "B27", "EF03", "EF01", "B30", "B33"]
SRC = "ai_headless_horseman"
MODE = sys.argv[3] if len(sys.argv) > 3 else "ai"  # "ai" = AI create only; else the live AI id for the quest edit
ai = enemy.build_ai({"name": "Headless Horseman", "role": "boss", "kit": KIT, "element": "Fire",
                     "avatar": "@img:headless_rider_avatar.webp", "srcId": SRC}, LEVEL, f, pool)
P = {c: pool[c] for c in KIT}
T = "CLOSEST_OPPONENT"
gate = lambda c: f.condition("distance_lower_than", value=P[c]["gate"], target=T)
use = lambda c, t=T: f.action("use_specific_jutsu", jutsuId=P[c]["id"], target=t)
ai["data"]["rules"] = [
    f.rule(action=use("B20", "SELF")),                                     # stance on cooldown
    f.rule(f.condition("health_below", value=40), gate("B30"), action=use("B30")),  # enrage stun
    f.rule(f.condition("target_has_effect", effectType="shield", threshold=0, target=T),
           gate("B33"), action=use("B33")),                                # shield denial
    f.rule(gate("B27"), action=use("B27")),
    f.rule(gate("EF03"), action=use("EF03")),
    f.rule(gate("B30"), action=use("B30")),
    f.rule(gate("B33"), action=use("B33")),
    f.rule(gate("EF01"), action=use("EF01")),
    f.rule(action=f.action("move_towards_opponent", target=T)),            # law 41 terminal
]
ai["data"]["rank"] = "ELITE JONIN"  # upstream f381b7f: only ELITE JONIN has LVL_CAP 110 and MAX stat caps
ai["data"].update(preferredStat="Ninjutsu", preferredGeneral1="Strength",
                  preferredGeneral2="Speed", gender="Male")
ai.pop("_derived")

# ---------------------------------------------------------------- quest edit
q = json.load(open(CAPTURE))
data = copy.deepcopy(q)
for k in ("createdAt", "updatedAt", "raidEndsAt", "raidCaptureDeadline", "raidGracePeriodEnd"):  # not write-validator fields (upstream f381b7f)
    data.pop(k, None)
objs = data["content"]["objectives"]
by = {o["id"]: o for o in objs}
assert data["hidden"] is True, "quest must still be hidden"

squad_text = by["66Dq0"]["description"]
v = by["V0IDs"]
v["nextObjectiveId"] = [{"text": "Continue", "nextObjectiveId": "hrSqd"}]

sqd = f.objective("dialog", id="hrSqd", description=squad_text,
                  nextObjectiveId=[{"text": "Stand with your squad and face the rider",
                                    "nextObjectiveId": "hrBat"}])
bat = f.objective("start_battle", id="hrBat",
                  description="The rider lowers his scythe and spurs the skeletal mount straight "
                              "at you. The gourd's candle flares. There is no running this time.",
                  opponentAIs=[{"ids": [MODE], "number": 1, "quantity": 1}],
                  completionOutcome="Win", nextObjectiveId="66Dq0", failObjectiveId="hrRst",
                  failDescription="The rider's laugh drops you to your knees once more.")
rst = f.objective("reset_quest", id="hrRst",
                  description="You come to on the riverbank, ears still ringing. Your squad pulls "
                              "you up. The rider is circling back.",
                  resetObjectiveId="hrSqd")
win = by["66Dq0"]
win["description"] = ("The scythe falls from the rider's grip and he wheels his mount into the "
                      "river mist, his laugh breaking apart on the wind. The curse still holds, "
                      "but tonight the Headless Rider ran from you.")

# Pre-existing defect: the three zombie fights had no failObjectiveId (re-arm loop risk).
# One shared reset sends a loss back to the trip into the ruined village (czwsz, in-flow).
zrst = f.objective("reset_quest", id="hrZRs",
                   description="The undead drag you down by sheer numbers. You break free and "
                               "fall back out of the ruined village to catch your breath.",
                   resetObjectiveId="czwsz")
for b in ("Vah2P", "jjfV9", "dKZp2"):
    by[b]["failObjectiveId"] = "hrZRs"
objs.insert(objs.index(by["BrH2S"]), zrst)

idx = objs.index(win)
objs[idx:idx] = [sqd, bat, rst]

# Hand-built: factory bounds quest.maxLevel at the pinned 100, but the live record already
# carries 110 (saved by the server), so the pin is stale; re-assert it as captured.
quest = {"entity": "quest", "slot": "edit", "name": data["name"], "targetId": data["id"], "data": data}

m = f.manifest([ai] if MODE == "ai" else [quest])
m["_note"] = (("Creates the Headless Horseman AI for Headless Rider Horror! (0lNDtE_VYJOCy8JZQI_sI): "
               "boss, level 110, ELITE JONIN, Fire, hidden, shared-pool kit B20 B27 EF03 EF01 B30 B33, "
               "custom rules (stance on cooldown, sub-40% stun, shield pierce, gated damage chain, "
               "move fallback; includeDefaultRules false). Avatar @img:headless_rider_avatar.webp from "
               "art/halloween_headless_rider/. AI only: the quest battle node is a separate edit built "
               "with this AI's live id once the results bundle lands.") if MODE == "ai" else
              ("Headless Rider Horror! quest edit: adds hrSqd dialog -> hrBat start_battle vs Headless "
               "Horseman (" + MODE + ") -> 66Dq0 win, loss -> hrRst; zombie fights fail-route to hrZRs. "
               "Whole-record re-assertion from capture tnr_results_1792954275867; stays hidden."))
if MODE == "ai":
    m["imgSizes"] = {"headless_rider_avatar.webp":
                 os.path.getsize("/home/claude/tnr-tools/art/halloween_headless_rider/headless_rider_avatar.webp")}
m = {"_note": m.pop("_note"), **m}
json.dump(m, open(OUT, "w"), indent=1, ensure_ascii=False)
print("objectives:", len(objs))
