#!/usr/bin/env python3
"""The director's AP test fight 2 critique as planner guards (critique.py), one check per point, then both planners
on a logged turn with the guards wired in. Socket-free; run: python3 tests/test_critique.py"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)

import cd_plan  # noqa: E402
import critique as K  # noqa: E402
import ingest  # noqa: E402
import shotplan  # noqa: E402
import turn  # noqa: E402

ME, HIM = "me_id", "him_id"


def ctx(**over):
    """A context: round 6, I act first, everything in PvP 1 ready, full AP, healthy, nothing on the board, his
    Clear spent last round (so one rule is checked at a time; the Clear rule's checks pass rows=[])."""
    st = {"loadout": list(cd_plan.LOADOUTS["pvp1"]), "used": over.pop("used", [])}
    kw = dict(R=6, en_acted=False, st=st, ap=100, my_hp=5000, my_max=5050, me_pos=(6, 4), ground=[], me_id=ME,
              rows=[(5, HIM, "clear", [])], en_id=HIM, clear_safe=False, nuke_hit=0)
    kw.update(over)
    return K.context(**kw)


def palace(centre):
    """My Subaku Palace's ground: every hex within 4 of the centre but the centre (AOE_SPIRAL_SHOOT)."""
    return [{"type": "decreasedamagegiven", "creatorId": ME, "longitude": x, "latitude": y, "rounds": 3,
             "createdRound": 5}
            for x in range(13) for y in range(9) if 0 < K._dist((x, y), centre) <= 4]


def check(name, cond, detail=""):
    if not cond:
        raise SystemExit(f"FAIL: {name} {detail}")
    print(f"  ok  {name}")


# ---- Limit Breaker is a planner action now (it was never in a table, so it could not be picked)
check("Limit Breaker in every table and in PvP 1",
      cd_plan.ACTIONS["limitbreaker"][:3] == (40, 7, "increasepotency") and "limitbreaker" in shotplan.MINE
      and ingest.IDS["P7dDcC102RhwBTTgA4HU_"] == "limitbreaker" and "limitbreaker" in cd_plan.LOADOUTS["pvp1"]
      and "limitbreaker" in cd_plan.LOADOUTS["pvp1_parry"] and "limitbreaker" in turn.ORDER)

# ---- 1. "Phantom stepping off the center of Subaku Palace ... increased their damage"
g = palace((6, 4))
check("the Palace's centre is the hole in its footprint", K.subaku_centres(g, ME) == {(6, 4)})
check("a Palace near the edge still has its centre", K.subaku_centres(palace((1, 1)), ME) == {(1, 1)})
check("his Palace is not mine", K.subaku_centres([dict(t, creatorId=HIM) for t in g], ME) == set())
c = ctx(ground=g)
for mv in ("phantom", "replace", "step"):
    p, why = K.guards([mv, "nights"], c)
    check(f"{mv} off my Palace's centre pays", p <= -K.OFF_CENTRE and "centre of my Subaku Palace" in why[0], why)
check("staying on the centre pays nothing", K.guards(["shield", "panacea"], c)[0] == 0)
check("moving when I am not on the centre pays nothing", K.guards(["phantom"], ctx(ground=g, me_pos=(6, 6)))[0] == 0)
check("no Palace up: moving pays nothing", K.guards(["phantom"], ctx())[0] == 0)

# ---- 2. "Using all buffs while enemy had clear and you did not have clear prevention active"
three = ["overflow", "eclipse", "pill"]                       # his R3, the turn DDXXD cleared
p, why = K.guards(three, ctx(rows=[]))
check("three buffs into his ready Clear pay for each", p == -3 * K.BUFF_INTO_CLEAR, why)
check("one buff is not 'all buffs'", K.guards(["overflow", "nights"], ctx(rows=[]))[0] == 0)
check("clear prevention live over his turn: no guard", K.guards(three, ctx(rows=[], clear_safe=True))[0] == 0)
check("Dr. Kim's now covers him when he acted first", K.guards(["kims"] + three[:2], ctx(rows=[], en_acted=True))[0] == 0)
check("Dr. Kim's now does not cover his turn later this round",
      K.guards(["kims"] + three[:2], ctx(rows=[], en_acted=False))[0] == -2 * K.BUFF_INTO_CLEAR)
cleared = [(2, HIM, "clear", [])]
check("his Clear on cooldown: no guard", K.guards(three, ctx(R=6, rows=cleared))[0] == 0)
check("his Clear back after 10 rounds", K.guards(three, ctx(R=12, rows=cleared))[0] < 0)
check("an afk enemy clears nothing", K.guards(three, ctx(rows=[], afk=True))[0] == 0)

# ---- 3. "Not using limit Breaker ... Not using aetherion during burst round"
SET = [[5, "overflow"]]                                      # a setup last round: this is the burst round
p, why = K.guards(["fury", "jewel", "pill"], ctx(used=SET))
check("a 60 AP hit with neither pump pays", p == -K.BURST_UNPUMPED and "Limit Breaker or Aetherion" in why[0], why)
check("Limit Breaker in the burst: no guard", K.guards(["limitbreaker", "fury"], ctx(used=SET))[0] == 0)
check("Aetherion in the burst: no guard", K.guards(["fury", "aetherion"], ctx(used=SET))[0] == 0)
lb_cd = SET + [[3, "limitbreaker"], [5, "aetherion"]]
check("both on cooldown: no guard", K.guards(["fury", "jewel", "pill"], ctx(used=lb_cd))[0] == 0)
check("no room for either: a second hit and a pill leave 20 AP", K.guards(["fury", "kunai", "pill"], ctx(used=SET))[0] == 0)
check("a move kept for range is not counted as room", K.guards(["phantom", "fury"], ctx(used=SET))[0] == 0)
check("not a burst: no guard", K.guards(["shield", "panacea", "jewel"], ctx(used=SET))[0] == 0)
check("no setup last round: not the burst round", K.guards(["fury", "jewel", "pill"], ctx())[0] == 0)

# ---- 4. "Didnt try to use Danse Macabre or Chakra Resistance to prevent getting nuked"
nuke = ctx(my_hp=2400, nuke_hit=1500)
p, why = K.guards(["shield", "jewel"], nuke)
check("a nuke on his clock and no seal halves with a shield", p == -0.5 * K.NUKE_NO_SEAL, why)
check("a nuke on his clock, no seal, no cover", K.guards(["nights", "pill"], nuke)[0] < -K.NUKE_NO_SEAL + 1)
check("Chakra Resistance answers it", K.guards(["resist", "nights"], nuke)[0] == 0)
check("Danse Macabre answers it", K.guards(["danse", "kunai"], nuke)[0] >= -K.BURST_UNPUMPED)
check("both on cooldown: no guard", K.guards(["nights", "pill"], ctx(my_hp=2400, nuke_hit=1500,
                                                                     used=[[5, "resist"], [5, "danse"]]))[0] == 0)
check("a small hit is no nuke", K.guards(["nights", "pill"], ctx(my_hp=5000, nuke_hit=900))[0] == 0)
rows = [(4, HIM, "x", ["dauntless takes 862.68 damage", "dauntless takes 606.00 afterburn damage"]),
        (4, HIM, "y", ["dauntless takes 351.42 damage"]), (3, HIM, "z", ["dauntless takes 400.00 damage"])]
check("his hardest turn is read from the log", abs(K.observed_peak(rows, HIM, "dauntless") - 1820.1) < 0.01)

# ---- 5. "Using buff prevent at the end of the fight with a pill and offensive stance while better damage and
#         defense options are available"
late = ctx(my_hp=1500)
p, why = K.guards(["pill", "lotus", "offstance"], late)            # his R8
check("late pill and stance pay for each", p <= -2 * K.LATE_FILLER and "late pill+offstance" in why[-1], why)
check("not late: the guard is off", K.guards(["pill", "lotus", "offstance"], ctx(my_hp=4000))[0] > -2 * K.LATE_FILLER)
spent = [[R, n] for R in (5,) for n in K.BETTER_LATE]
check("nothing better ready: no guard", K.guards(["pill", "lotus", "offstance"], ctx(my_hp=1500, used=spent))[0] == 0)

# ---- both planners run with the guards on a logged turn (ANBU Member R3, a battle id that starts with a dash)
for script in ("turn.py", "planner2.py"):
    extra = ["--no-engine"] if script == "turn.py" else []
    out = subprocess.run([sys.executable, os.path.join(TOOLS, script), os.path.join(HERE, "anbu_r3.txt"),
                          "--battle=-CH613DKHOF7stgVwrDNR", "--top=3", "--enemy=ANBU Member", *extra],
                         capture_output=True, text=True, timeout=600, cwd=TOOLS,
                         env=dict(os.environ, TNR_CRITIQUE="1"))
    check(f"{script} plans with the guards on (TNR_CRITIQUE=1)", out.returncode == 0 and "FIRE:" in out.stdout,
          out.stdout[-800:] + out.stderr[-800:])
check("off by default in the planners", K.live_guards(three, ctx(rows=[]))[0] == 0 or K.LIVE)

# ---- the replay review on fight 2 (reconstructed from the operator's decode: no positions, see the file's note)
import json  # noqa: E402
raw = json.load(open(os.path.join(HERE, "ap_fight2_ddxxd.json")))
rows = list(zip(raw["*.battleRound"], raw["*.userId"], raw["*.actionId"], raw["*.appliedEffects.*.txt"]))
found = K.review_fight(rows, ingest.ME, "user_ddxxd_reconstructed")
txt = " | ".join(f"R{f['round']} {f['text']}" for f in found)
check("R7: Phantom Step while my Subaku Palace was up", any(f["round"] == 7 and "Subaku Palace" in f["text"]
                                                            for f in found), txt)
check("R3: three buffs into his ready Clear", any(f["round"] == 3 and "ready Clear" in f["text"] for f in found), txt)
check("a burst round without Limit Breaker", any("without Limit Breaker" in f["text"] for f in found), txt)
check("R8: the burst round without Aetherion", any(f["round"] == 8 and "Aetherion" in f["text"] for f in found), txt)
check("before his nukes: no Danse Macabre or Chakra Resistance",
      {f["round"] for f in found if "Danse Macabre" in f["text"]} == {7, 8}, txt)
check("R8: late pill and offensive stance", any(f["round"] == 8 and "late pill+offstance" in f["text"]
                                                for f in found), txt)
check("nothing flagged on turns he did not fault", {f["round"] for f in found} <= {3, 4, 7, 8}, txt)
check("Limit Breaker is no error in a fight it was not in",
      not any("Limit Breaker" in f["text"] and "Aetherion" not in f["text"]
              for f in K.review_fight(rows, ingest.ME, "user_ddxxd_reconstructed", limit_breaker=False)))
print("ok: the fight 2 critique is a replay review and, switched on, planner terms")
