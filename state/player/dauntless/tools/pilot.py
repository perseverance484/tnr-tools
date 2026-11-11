#!/usr/bin/env python3
"""pilot.py: the single entry point that pilots dauntless while awake (director rulings, 2026-11-11).

Contract:
- The worker pilots whenever the character is awake, and may step away only while it rests.
- Every tick is exactly ONE relayed batch: whatever `pilot.py` printed last time. That is the game calls, in order,
  ending with `pilot.py` itself.
- `pilot.py` reads the results of that batch straight from the session transcript, so the worker never retypes or
  interprets game data. It keeps one state file, decides, and prints the next batch.

So the worker does no game reasoning on the clock: it relays. A turn costs one model round trip, and its actions go
in the same batch as the poll that follows them.

Output format: a status line, then one JSON object per line, relayed in order:
  {"call": endpointName, "input": {...}, "select": [...]}   -> mcp__Tnr__callEndpoint
  {"bash": "..."}                                          -> Bash (always the final pilot tick)
  {"wait": seconds}                                        -> background sleep, then relay the rest on wake
  (no lines)                                               -> nothing to do: asleep, the worker may step away

Modes come from the game, not from memory: profile.getUser status (AWAKE / BATTLE / HOSPITALIZED / ASLEEP) and
combat.getBattle. Adding behaviour = adding a rule to `world()`; battle play is turn.py (the verified planner).
"""
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = os.environ.get("TNR_PILOT_LIVE") or os.path.join(HERE, "..", "fights", "live")   # gitignored runtime
FIGHTS = os.path.join(HERE, "..", "fights")
STATE = os.path.join(LIVE, "pilot.json")
ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
HOME_VILLAGE = "9FZf8b9E7tZJZTaChmhHB"
GUARD_WAIT = 7          # world tick ~every 9 s with overhead: inside the 15 s lobby before an attack lands
PLAN_BUDGET = 4.0       # planner: median 1.2 s, worst 3.3 s on the regression set
ENT = ("*.id", "*.battleRound", "*.userId", "*.actionId", "*.appliedEffects.*.txt")

# ---------------------------------------------------------------- the calls the pilot can ask for (one place)
def call(endpoint, inp, select):
    return {"call": endpoint, "input": inp, "select": select}


def c_user():
    return call("profile.getUser", {}, ["userData.status", "userData.battleId", "userData.curHealth",
                                        "userData.maxHealth", "userData.sector"])


def c_battle(bid):
    return call("combat.getBattle", {"battleId": bid},
                ["battle.version", "battle.round", "battle.activeUserId"] +
                [f"battle.usersState.*.{k}" for k in ("userId", "username", "curHealth", "maxHealth", "longitude",
                                                      "latitude", "actionPoints", "isAi")])


def c_entries(bid, n):
    return call("combat.getBattleEntries", {"battleId": bid, "limit": n}, list(ENT))


def c_act(bid, aid, x, y, v):
    return call("combat.performAction", {"battleId": bid, "actionId": aid, "longitude": x, "latitude": y,
                                         "version": v}, ["notification"])


TICK = {"bash": f"cd {HERE} && python3 pilot.py"}


# ---------------------------------------------------------------- state + transcript
def load_state():
    try:
        return json.load(open(STATE))
    except (OSError, ValueError):
        return {}


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{os.getpid()}"
    json.dump(obj, open(tmp, "w"))
    os.replace(tmp, path)


def transcript():
    """The transcript of whichever session is relaying right now: the most recently written one (a dedicated pilot
    agent writes under <session>/subagents/)."""
    files = glob.glob("/root/.claude/projects/**/*.jsonl", recursive=True)
    return os.environ.get("TNR_TRANSCRIPT") or (max(files, key=os.path.getmtime) if files else None)


def fresh_results(since, tail=400_000):
    """{endpoint: (input, data, time)}: the newest result per endpoint written after `since` (epoch s), i.e. this batch.
    Claude Code writes each tool result to the transcript before the next call in a batch runs."""
    path = transcript()
    if not path:
        return {}
    with open(path, "rb") as f:
        f.seek(max(0, os.path.getsize(path) - tail))
        lines = f.read().decode("utf8", "ignore").splitlines()
    asked, out = {}, {}
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        content = (d.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for c in content:
            if c.get("type") == "tool_use" and c.get("name", "").endswith("callEndpoint"):
                asked[c["id"]] = ((c.get("input") or {}).get("endpointName"), (c.get("input") or {}).get("input") or {})
            elif c.get("type") == "tool_result" and c.get("tool_use_id") in asked:
                t = dt.datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")).timestamp()
                if t <= since:
                    continue
                body = c.get("content")
                text = body if isinstance(body, str) else "".join(x.get("text", "") for x in body or [] if isinstance(x, dict))
                try:
                    ep, inp = asked[c["tool_use_id"]]
                    out[ep] = (inp, json.loads(text), t)
                except ValueError:
                    pass
    return out


# ---------------------------------------------------------------- battle
def battle_tick(st, bid, battle, entries):
    cache_path = os.path.join(LIVE, f"{bid}.json")
    try:
        cache = json.load(open(cache_path))
    except (OSError, ValueError):
        cache = {"entries": []}
    if entries and "*.id" in entries:
        seen = {e[0] for e in cache["entries"]}
        new = [list(x) for x in zip(*(entries.get(k, []) for k in ENT)) if x[0] not in seen]
        cache["entries"] += new[::-1]                      # cache is oldest-first
    users = battle.get("battle.usersState.*.userId") or []
    if ME not in users:                                     # battle gone (finished battles are deleted)
        return finish(st, bid, cache, "battle closed")
    cache["battle"] = battle
    save(cache_path, cache)
    hp = battle["battle.usersState.*.curHealth"]
    me_i = users.index(ME)
    foes = [i for i in range(len(users)) if i != me_i and hp[i] > 0]
    if hp[me_i] <= 0 or not foes:
        return finish(st, bid, cache, "won" if hp[me_i] > 0 else "lost")
    R, v = battle["battle.round"], battle["battle.version"]
    names = battle["battle.usersState.*.username"]
    head = f"BATTLE R{R} v{v} | me {hp[me_i]:.0f} | {names[foes[0]]} {hp[foes[0]]:.0f}"
    poll = [c_battle(bid), c_entries(bid, 8), TICK]
    active = battle["battle.activeUserId"]
    if active != ME:
        ai = battle.get("battle.usersState.*.isAi") or []
        if active in users and ai and ai[users.index(active)]:
            # an AI's turn only advances when some client calls performAction during it (engine: isAITurn);
            # in PvP the human opponent's client drives his own turn
            me_x, me_y = battle["battle.usersState.*.longitude"][me_i], battle["battle.usersState.*.latitude"][me_i]
            return head + " | AI turn: nudge", [c_act(bid, "wait", me_x, me_y, v)] + poll
        return head + " | his turn", poll
    plan, how = plan_turn(bid, battle, cache["entries"], names[foes[0]])
    if not plan:
        return head + f" | MY TURN, no plan ({how}): defensiveStance", \
            [c_act(bid, "defensiveStance", battle["battle.usersState.*.longitude"][me_i],
                   battle["battle.usersState.*.latitude"][me_i], v)] + poll
    acts = [c_act(bid, a["actionId"], a["longitude"], a["latitude"], v + k) for k, a in enumerate(plan)]
    return head + f" | MY TURN: {' + '.join(a['name'] for a in plan)} ({how})", acts + poll


def plan_turn(bid, battle, entries, enemy):
    """turn.py (the verified planner, python only on the clock) on a turn file built from the cache."""
    path = os.path.join(LIVE, f"{bid}.turn.txt")
    rows = entries[::-1]                                    # turn.py reads newest-first, like the connector
    with open(path, "w") as f:
        f.write(json.dumps(battle) + "\n" +
                json.dumps({k: [r[i] for r in rows] for i, k in enumerate(ENT) if k != "*.id"}) + "\n")
    t0 = time.time()
    for extra, budget in (((), PLAN_BUDGET), (("--keep", "6", "--cash", "3"), 2.0)):
        try:
            out = subprocess.run([sys.executable, os.path.join(HERE, "turn.py"), path, "--battle", bid, "--top", "1",
                                  "--enemy", enemy, "--no-engine", *extra],
                                 capture_output=True, text=True, timeout=budget).stdout
        except subprocess.TimeoutExpired:
            continue
        m = re.search(r"^FIRE: (.*)$", out, re.M)
        if m:
            return json.loads(m.group(1)), f"{time.time() - t0:.1f}s" + (" short list" if extra else "")
    return None, "planner over budget"


def finish(st, bid, cache, why):
    """Battle over: keep its log for the post-fight tools (the game deletes it), back to the world loop."""
    rows = cache.get("entries", [])[::-1]
    if rows:
        save(os.path.join(FIGHTS, f"{bid}_entries.json"), {k: [r[i] for r in rows] for i, k in enumerate(ENT)})
    st.pop("battleId", None)
    return f"BATTLE OVER ({why}): log saved fights/{bid}_entries.json", [c_user(), TICK]


# ---------------------------------------------------------------- world
def world(st, user):
    """Rules for the awake character outside battle, in priority order. Hunting rules plug in here."""
    status, bid = user.get("userData.status"), user.get("userData.battleId")
    if status == "BATTLE" and bid:
        st["battleId"] = bid
        return f"BATTLE START {bid}", [c_battle(bid), c_entries(bid, 200), TICK]
    if status == "ASLEEP":
        return "ASLEEP: the worker may step away", []
    if status == "HOSPITALIZED":
        return "HOSPITALIZED: healing", [call("hospital.npcHeal", {"villageId": HOME_VILLAGE}, ["success", "message"]),
                                        c_user(), TICK]
    hp, mx = user.get("userData.curHealth", 0), user.get("userData.maxHealth", 1)
    return f"AWAKE {hp:.0f}/{mx:.0f} HP, sector {user.get('userData.sector')}: guarding", \
        [{"wait": GUARD_WAIT}, c_user(), TICK]


# ---------------------------------------------------------------- tick
def tick():
    st = load_state()
    started = time.time()
    res = fresh_results(st.get("last_tick", 0))
    bid = st.get("battleId")
    tb = res.get("combat.getBattle", (0, 0, 0))[2]
    tu = res.get("profile.getUser", (0, 0, 0))[2]
    if tb and tb >= tu:
        inp, battle, _ = res["combat.getBattle"]
        bid = inp.get("battleId") or bid
        e = res.get("combat.getBattleEntries")
        head, batch = battle_tick(st, bid, battle or {}, e[1] if e and e[0].get("battleId") == bid else None)
        if "BATTLE OVER" not in head:
            st["battleId"] = bid
    elif tu:
        head, batch = world(st, res["profile.getUser"][1])
    elif bid:
        head, batch = f"resume battle {bid}", [c_battle(bid), c_entries(bid, 8), TICK]
    else:
        head, batch = "start", [c_user(), TICK]
    st["last_tick"] = started
    save(STATE, st)
    print(head)
    for b in batch:
        print(json.dumps(b, separators=(",", ":")))


if __name__ == "__main__":
    tick()
