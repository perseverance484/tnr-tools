#!/usr/bin/env python3
"""An offline dry run of the player brain: no game call is made.

A brain with the live defaults (pvp_turns off, stealth down) plays a scripted stretch of a day on a temporary
folder, with the real do-not-attack list, and is handed answers in the shapes the game gives. It starts in shadow
(the default) and checks that nothing would go out, then plays in read_only, the dry run that can move: in shadow no
read comes back, so the brain asks for the same first read again and again. Here the script stands in for the game
and answers the reads; every action is held in live/shadow.jsonl. The upkeep activities (restock, repair, training,
equipment, bank) are switched off: their reads are not scripted. Each step prints what it chose and what would go
out, then the script checks the director's rules against what it saw. Exit 0 when every check holds.

    python3 scripts/player_dry_run.py [--keep]     # --keep leaves the temporary folder and prints its path
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from player import config as C                      # noqa: E402
from player.brain import Brain                      # noqa: E402
from player.combat import Combat                    # noqa: E402
from player.gates import Gates                      # noqa: E402
from player.world import Result                     # noqa: E402

DNA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state", "player", "dauntless",
                   "do_not_attack.md")
T0 = 1_795_510_800.0        # 2026-11-23 09:00 UTC (inside the Aurora_Dusk and Momochi windows)
ROW = ("userId", "username", "longitude", "latitude", "status", "level", "villageId", "immunityUntil", "battleId")


def res(endpoint, data=None, inp=None):
    return Result(endpoint, inp or {}, data, None, None)


def user(status="AWAKE", hp=5050, sector=1538, pos=(10, 10), bid=None, chakra=100, **more):
    d = {"userData.status": status, "userData.battleId": bid, "userData.curHealth": hp, "userData.maxHealth": 5050,
         "userData.sector": sector, "userData.longitude": pos[0], "userData.latitude": pos[1],
         "userData.curChakra": chakra, "userData.maxChakra": 100, "userData.curStamina": 100,
         "userData.maxStamina": 100, "userData.money": 150_000, "userData.bank": 50_000_000, "userData.curEnergy": 0,
         "userData.dailyErrands": 30}
    d.update({f"userData.{k}": v for k, v in more.items()})
    return res("profile.getUser", d)


def scan(rows, sector=1538):
    return res("travel.getSectorData", {f"users.*.{k}": [r[i] for r in rows] for i, k in enumerate(ROW)},
               {"sector": sector})


class Run:
    def __init__(self, live):
        self.live, self.t = live, T0
        fights = os.path.join(live, "fights")
        self.brain = Brain(live, clock=lambda: self.t, combat=Combat(fights, spawn=False), gates=Gates(dna_path=DNA))
        self.brain.world["control"].update(mode="hunt", relay_without_hooks=True)
        self.brain.world["control"]["activities"].update(
            {a: False for a in ("restock", "repair", "training", "equipment", "bank")})
        self.seen, self.fails = [], []

    def tick(self, label, *results, dt=1.0):
        self.t += dt
        out = self.brain.handle([r._replace(at=self.t) for r in results])
        sent = [s["call"] for s in out["steps"] if "call" in s]
        self.seen.append((label, out))
        print(f"\n[{label}] {out['activity']}: {out['note']}")
        print(f"   goes out: {sent or 'nothing'}")
        held = self.held()
        if held and held[-1]["at"] == self.t:
            print(f"   held:     {[h['call'] for h in held[-1]['held']]}")
        return out

    def held(self):
        try:
            with open(os.path.join(self.live, "shadow.jsonl"), encoding="utf8") as f:
                return [json.loads(line) for line in f]
        except OSError:
            return []

    def check(self, ok, what):
        print(f"   {'ok  ' if ok else 'FAIL'} {what}")
        if not ok:
            self.fails.append(what)


def main():
    live = tempfile.mkdtemp(prefix="player-dry-run-")
    r = Run(live)
    w = r.brain.world
    print(f"dry run in {live}: run={w['control']['run']}, pvp_turns={w['control']['pvp_turns']}")
    r.check(w["control"]["run"] == "shadow" and w["control"]["pvp_turns"] is False, "starts in shadow, hands off PvP")

    out = r.tick("awake at home (shadow)", user(sector=C.HOME_SECTOR))
    r.check(not any("call" in s for s in out["steps"]), "shadow: nothing goes out")
    w["control"]["run"] = "read_only"
    print("\n-- read_only from here: reads go out (the script answers them), actions are held")
    r.tick("the reads asked again", user(sector=C.HOME_SECTOR), dt=300)
    r.tick("streak and interest read", res("activityStreak.getUserStreaks", {"streaks": [{"configId": "s1",
            "canClaim": True}]}), res("bank.getPendingInterest", {"amount": 4200}), user(sector=C.HOME_SECTOR))
    r.tick("claims answered", res("activityStreak.claimStreakDay", {"success": True},
            {"configId": "s1", "payCatchUp": False, "reset": False}), res("bank.claimInterest", {"success": True}),
           user(sector=C.HOME_SECTOR, dailyErrands=2))
    claims = [h for row in r.held() for h in row["held"] if h["call"] == "activityStreak.claimStreakDay"]
    r.check(bool(claims) and all(h["input"]["payCatchUp"] is False for h in claims), "streak claimed, never paid")
    errand = [row for row in r.held() if row["activity"] == "errands"]
    r.check(bool(errand), "errands behind the spread: an errand is planned")

    rows = [("user_keoshi", "Keoshi", 3, 3, "AWAKE", 100, "v", None, None),
            ("user_aurora", "Aurora_Dusk", 4, 4, "AWAKE", 100, "v", None, None),
            ("user_low", "Ninety", 5, 5, "AWAKE", 90, "v", None, None),
            ("user_t", "Target", 12, 12, "AWAKE", 100, "v", None, None)]
    w["opponents"]["lost_to"].clear()
    r.tick("on the circuit", user(dailyErrands=30))
    out = r.tick("scan: friends, a protected player, a 90, a 100; HP short", user(hp=4000, dailyErrands=30), scan(rows))
    r.check(out["activity"] == "recovery" and "combat.attackUser" not in str(r.held()),
            "short HP: it heals first, no attack is planned")
    r.tick("healed", user(dailyErrands=30), dt=30)
    out = r.tick("scan again at full", user(dailyErrands=30), scan(rows), dt=10)
    attacks = [h["input"] for row in r.held() for h in row["held"] if h["call"] == "combat.attackUser"]
    r.check(bool(attacks) and {a.get("userId") for a in attacks} == {"user_t"},
            "the only one attacked is the level 100 (not Keoshi, Aurora_Dusk or the 90)")

    out = r.tick("in a fight against a person", user("BATTLE", bid="B1", dailyErrands=30))
    battle, ents = recorded_fight()
    out = r.tick("his fight (a recorded state: round 3 against a person)", res("combat.getBattle", battle,
                 {"battleId": "B1"}), res("combat.getBattleEntries", ents, {"battleId": "B1", "limit": 8}))
    acts = [h for row in r.held() for h in row["held"] if h["call"] == "combat.performAction"]
    r.check(not acts, "a fight against a person: no turn is played")
    r.check(any(e.get("kind") == "ping" for e in _events(live)) or "hands off" in out["note"],
            "the director is pinged once for his fight")
    reads = {e for e, v in r.brain.gates.endpoints.items() if v.get("kind") == "read"}
    sent = [s["call"] for _, o in r.seen for s in o["steps"] if "call" in s and s["call"] not in reads]
    r.check(not sent, f"not one action went out in the whole run {sent or ''}")
    sectors = [h["input"].get("sector") for row in r.held() for h in row["held"] if "sector" in h["input"]]
    r.check(210 not in sectors, "sector 210 never visited")

    print(f"\n{len(r.held())} batches held in shadow.jsonl; {len(r.fails)} check(s) failed")
    if "--keep" in sys.argv:
        print(f"kept: {live}")
    else:
        shutil.rmtree(live, ignore_errors=True)
    return 1 if r.fails else 0


def recorded_fight():
    """A logged fight state (the pvp tools' tests/angelsaber_r3.txt): my turn, round 3, against a person."""
    with open(os.path.join(C.TOOLS, "tests", "angelsaber_r3.txt"),
              encoding="utf8") as f:
        battle, ents = [json.loads(line) for line in f.read().splitlines() if line.strip()]
    n = len(ents["*.battleRound"])
    ents["*.id"] = [f"e{n - i}" for i in range(n)]
    return battle, ents


def _events(live):
    try:
        with open(os.path.join(live, "events.jsonl"), encoding="utf8") as f:
            return [json.loads(line) for line in f]
    except OSError:
        return []


if __name__ == "__main__":
    sys.exit(main())
