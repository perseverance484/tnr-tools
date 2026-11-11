#!/usr/bin/env python3
"""Offline end-to-end test of pilot.py: a fake transcript holding one poll batch (AngelSaber R3, a logged state) must
produce the planner's pick as actions + the next poll + the tick, in one batch. No live calls.
Run: python3 tests/test_pilot.py"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "angelsaber_r3.txt")
BID = "TESTPILOT"


def fake_transcript(path, battle, entries):
    now = dt.datetime.now(dt.timezone.utc)
    rows = []
    for k, (ep, inp, data) in enumerate((("combat.getBattle", {"battleId": BID}, battle),
                                         ("combat.getBattleEntries", {"battleId": BID, "limit": 200}, entries))):
        ts = (now + dt.timedelta(seconds=k)).isoformat().replace("+00:00", "Z")
        rows.append({"timestamp": ts, "message": {"content": [{"type": "tool_use", "id": f"u{k}",
                     "name": "mcp__Tnr__callEndpoint", "input": {"endpointName": ep, "input": inp}}]}})
        rows.append({"timestamp": ts, "message": {"content": [{"type": "tool_result", "tool_use_id": f"u{k}",
                     "content": [{"type": "text", "text": json.dumps(data)}]}]}})
    with open(path, "w") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")


def main():
    battle, ents = [json.loads(l) for l in open(FIX).read().splitlines() if l.strip()]
    n = len(ents["*.battleRound"])
    ents["*.id"] = [f"e{n - i}" for i in range(n)]
    with tempfile.TemporaryDirectory() as d:
        tp = os.path.join(d, "t.jsonl")
        fake_transcript(tp, battle, ents)
        out = subprocess.run([sys.executable, os.path.join(HERE, "pilot.py")], capture_output=True, text=True,
                             env=dict(os.environ, TNR_TRANSCRIPT=tp, TNR_PILOT_LIVE=os.path.join(d, "live"))).stdout.splitlines()
    want = subprocess.run([sys.executable, os.path.join(HERE, "planner2.py"), FIX, "--battle", BID + "_ref", "--top", "1"], capture_output=True, text=True).stdout
    want_ids = [a["actionId"] for a in json.loads(want.split("FIRE: ", 1)[1].splitlines()[0])]
    batch = [json.loads(l) for l in out[1:]]
    acts = [b["input"]["actionId"] for b in batch if b.get("call") == "combat.performAction"]
    vers = [b["input"]["version"] for b in batch if b.get("call") == "combat.performAction"]
    print(out[0])
    assert "MY TURN" in out[0], out
    assert acts == want_ids, (acts, want_ids)
    assert vers == list(range(battle["battle.version"], battle["battle.version"] + len(acts))), vers
    tail = [b.get("call") or "bash" for b in batch[len(acts):]]
    # an opponent with no saved kit gets one kit read riding on the poll (opp_profile)
    assert tail in (["combat.getBattle", "combat.getBattleEntries", "bash"],
                    ["combat.getBattle", "combat.getBattleEntries", "jutsu.getPublicUserJutsus", "bash"]), tail
    print("ok: pilot batch = planner pick + poll + tick")


def test_restock():
    """A due restock reads items first; with Kim's empty and Smoke at home it buys Kim's and takes Smoke out."""
    head, b = run_world([user()], "hunt", {"restock": {"next": 0, "pass": 0, "active": False}})
    assert "restock: reading items" in head and b[0]["call"] == "item.getUserItems", (head, b[:1])
    items = {"*.id": ["u1", "u2"], "*.itemId": ["6DnJn4x6LWWXtBu7UZybb", "TtYPd-LcXKeK3sMuhq1TP"],
             "*.quantity": [0, 5], "*.equipped": ["NONE", "NONE"], "*.storedAtHome": [False, True]}
    u = user()
    u[2]["userData.money"], u[2]["userData.bank"] = 3_000_000, 0
    head, b = run_world([u, ("item.getUserItems", {}, items)], "hunt",
                        {"restock": {"next": 0, "pass": 1, "active": True}})
    calls = [x.get("call") for x in b]
    assert "item.buy" in calls and "home.toggleStoreItem" in calls, (head, calls)
    print("ok: restock (read, buy from the shop, take out of home storage)")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------- world rules (hunt / guard / rest)
def run_world(results, mode, state=None):
    """results: [(endpoint, input, data)] as one batch; returns (status line, batch)."""
    with tempfile.TemporaryDirectory() as d:
        live = os.path.join(d, "live")
        os.makedirs(live)
        # restock is tested on its own below; keep it off the world-rule cases unless the state asks for it
        json.dump(dict({"restock": {"next": 4e9, "pass": 0, "active": False}}, **(state or {}), mode=mode),
                  open(os.path.join(live, "pilot.json"), "w"))
        now = dt.datetime.now(dt.timezone.utc)
        rows = []
        for k, (ep, inp, data) in enumerate(results):
            ts = (now + dt.timedelta(seconds=k + 1)).isoformat().replace("+00:00", "Z")
            rows.append({"timestamp": ts, "message": {"content": [{"type": "tool_use", "id": f"w{k}",
                         "name": "mcp__Tnr__callEndpoint", "input": {"endpointName": ep, "input": inp}}]}})
            rows.append({"timestamp": ts, "message": {"content": [{"type": "tool_result", "tool_use_id": f"w{k}",
                         "content": [{"type": "text", "text": json.dumps(data)}]}]}})
        tp = os.path.join(d, "t.jsonl")
        open(tp, "w").write("\n".join(json.dumps(r) for r in rows) + "\n")
        out = subprocess.run([sys.executable, os.path.join(HERE, "pilot.py")], capture_output=True, text=True,
                             env=dict(os.environ, TNR_TRANSCRIPT=tp, TNR_PILOT_LIVE=live)).stdout.splitlines()
    return out[0], [json.loads(l) for l in out[1:]]


def user(status="AWAKE", hp=5050, sector=1538, pos=(10, 10), bid=None):
    return ("profile.getUser", {}, {"userData.status": status, "userData.battleId": bid, "userData.curHealth": hp,
                                    "userData.maxHealth": 5050, "userData.sector": sector,
                                    "userData.longitude": pos[0], "userData.latitude": pos[1]})


def sector(rows, sec=1538):
    keys = ("userId", "username", "longitude", "latitude", "status", "level", "villageId", "immunityUntil", "battleId")
    return ("travel.getSectorData", {"sector": sec}, {f"users.*.{k}": [r[i] for r in rows] for i, k in enumerate(keys)})


def test_world():
    me = ("user_37qazcrgUPldBPI65bb25DQiCjz", "dauntless", 10, 10, "AWAKE", 100, "9FZf8b9E7tZJZTaChmhHB", None, None)
    shisui = ("user_2SAAMvwqsbjyS2Qd8A2pB0Gzn4W", "Shisui", 11, 10, "AWAKE", 100, "x", None, None)      # do-not-attack
    friend = ("u_f", "Villager", 10, 11, "AWAKE", 100, "9FZf8b9E7tZJZTaChmhHB", None, None)              # own village
    immune = ("u_i", "Fresh", 10, 12, "AWAKE", 100, "y", "2099-01-01T00:00:00Z", None)
    low = ("u_l", "Genin", 10, 10, "AWAKE", 20, "y", None, None)
    prey = ("u_p", "Prey", 13, 14, "AWAKE", 100, "y", None, None)
    head, b = run_world([user(), sector([me, shisui, friend, immune, low, prey])], "hunt")
    assert "attacking Prey" in head, head
    assert [x.get("call") for x in b][:2] == ["travel.moveInSector", "combat.attackUser"], b
    assert b[0]["input"]["longitude"] == 13 and b[1]["input"]["userId"] == "u_p", b
    head, b = run_world([user(), sector([me, shisui, friend])], "hunt")
    assert "next sector 1490" in head and b[0]["input"] == {"sector": 1490}, (head, b)
    head, b = run_world([user(status="ASLEEP", sector=177)], "hunt")
    assert "waking" in head and b[0]["call"] == "home.toggleSleep", head
    head, b = run_world([user(status="ASLEEP", sector=177)], "guard")
    assert b == [], (head, b)
    head, b = run_world([user(hp=2000)], "hunt")
    assert b[0]["call"] == "item.consume", head
    head, b = run_world([user(hp=2000)], "hunt", {"healing": ["hp", 2000 / 5050]})    # potion did nothing
    assert b[0].get("call") != "item.consume", (head, b)
    head, b = run_world([user(status="BATTLE", bid="B1")], "hunt")
    assert b[0]["call"] == "combat.getBattle" and b[1]["input"]["limit"] == 200, head
    head, b = run_world([user(sector=1538)], "rest")
    assert "going home" in head, head
    refused = ("combat.attackUser", {"userId": "u_p"}, {"success": False, "message": "Cannot attack Prey — different combat bracket (7 vs 5)"})
    head, b = run_world([refused, user(), sector([me, prey])], "hunt")
    assert "attacking" not in head and "bracket" in head, head
    # rate limit: a refused call in the batch -> pause and resend the same game calls
    last = [{"call": "combat.getBattle", "input": {"battleId": "B1"}, "select": []}, {"bash": "x"}]
    head, b = run_world([("combat.getBattle", {"battleId": "B1"}, "Error POSTing to endpoint: Too Many Requests")], "hunt",
                        {"last_batch": last, "battleId": "B1"})
    assert head.startswith("RATE LIMITED") and b[0] == last[0] and "pilot_safe.py" in b[-1]["bash"], (head, b)
    print("ok: world rules (target filters, circuit, wake, rest, heal, battle start, refusal memory, rate-limit backoff)")


def test_restock():
    """A due restock reads items first; with Kim's empty and Smoke at home it buys Kim's and takes Smoke out."""
    head, b = run_world([user()], "hunt", {"restock": {"next": 0, "pass": 0, "active": False}})
    assert "restock: reading items" in head and b[0]["call"] == "item.getUserItems", (head, b[:1])
    items = {"*.id": ["u1", "u2"], "*.itemId": ["6DnJn4x6LWWXtBu7UZybb", "TtYPd-LcXKeK3sMuhq1TP"],
             "*.quantity": [0, 5], "*.equipped": ["NONE", "NONE"], "*.storedAtHome": [False, True]}
    u = user()
    u[2]["userData.money"], u[2]["userData.bank"] = 3_000_000, 0
    head, b = run_world([u, ("item.getUserItems", {}, items)], "hunt",
                        {"restock": {"next": 0, "pass": 1, "active": True}})
    calls = [x.get("call") for x in b]
    assert "item.buy" in calls and "home.toggleStoreItem" in calls, (head, calls)
    print("ok: restock (read, buy from the shop, take out of home storage)")


if __name__ == "__main__":
    test_world()
    test_restock()
    # every test passed: this pilot.py becomes the fallback pilot_safe.py runs if a later edit breaks
    import shutil
    good = os.path.join(HERE, "pilot_good.py")
    os.makedirs(os.path.dirname(good), exist_ok=True)
    shutil.copy(os.path.join(HERE, "pilot.py"), good)
    print("ok: saved as the last good pilot")
