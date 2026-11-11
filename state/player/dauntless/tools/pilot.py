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
HOME_SECTOR = 177
CIRCUIT = [1538, 1490, 1335, 99]   # Shirohana, Tsukimori, Akasumi, Risen: where active enemies gather
ME_CARD = {"level": 100, "username": "dauntless",
           "avatar": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ2ZSxgqnMXlcRpYmJ5do0zKw4Qx6PVEtBa9b8",
           "avatarLight": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJEJNnVieLfKL5D7TAFe29bymSaPCIQ846MdzG"}
HEAL_BELOW = 0.95       # fights start at full health (playbook)
POOLS_BELOW = 0.5       # chakra / stamina floor before ramen
FULL_POTION = "IRfg2NFKKYe0ynroXI7qZ"   # user item: HP to full out of combat (ramen refills CP/SP only)
HUNT_WAIT = 4           # hunt tick ~every 7 s: about 3 calls a tick, under the connector's 30 a minute
GUARD_WAIT = 7          # world tick ~every 9 s with overhead: inside the 15 s lobby before an attack lands
POLL_GAP = 2           # seconds between his-turn polls (connector cap 30 calls/min)
PLAN_BUDGET = 4.0       # planner: median 1.2 s, worst 3.3 s on the regression set
ENT = ("*.id", "*.battleRound", "*.userId", "*.actionId", "*.appliedEffects.*.txt")

# ---------------------------------------------------------------- the calls the pilot can ask for (one place)
def call(endpoint, inp, select):
    return {"call": endpoint, "input": inp, "select": select}


def c_user():
    return call("profile.getUser", {}, ["userData.status", "userData.battleId", "userData.curHealth",
                                        "userData.maxHealth", "userData.sector", "userData.longitude",
                                        "userData.latitude", "userData.curChakra", "userData.maxChakra",
                                        "userData.curStamina", "userData.maxStamina"])


def c_sector(sector):
    return call("travel.getSectorData", {"sector": sector},
                [f"users.*.{k}" for k in ("userId", "username", "longitude", "latitude", "status", "level", "villageId",
                                          "immunityUntil", "battleId")])


def c_move(cur, dest, sector):
    return call("travel.moveInSector", {"curLongitude": cur[0], "curLatitude": cur[1], "longitude": dest[0],
                                        "latitude": dest[1], "destLongitude": dest[0], "destLatitude": dest[1],
                                        "sector": sector, "villageId": HOME_VILLAGE, **ME_CARD}, ["success", "message"])


def c_attack(t, sector):
    return call("combat.attackUser", {"userId": t["userId"], "longitude": t["longitude"], "latitude": t["latitude"],
                                      "sector": sector, "asset": "ground"}, ["success", "message", "battleId"])


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


def wait(seconds):
    """A pause inside the batch (relayed like any call: the relay needs no timers)."""
    return {"bash": f"python3 -c 'import time; time.sleep({seconds})'"}


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
        # a fast relay polls every ~2.7 s (~45 calls/min); the connector allows 30/min ("Too Many Requests"
        # mid-fight, 2026-11-11), so his-turn polls pace themselves: ~25 calls/min, ~1 s more detection lag
        return head + " | his turn", [wait(POLL_GAP)] + poll
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
def do_not_attack():
    """Names and ids from do_not_attack.md (the director's list; the 'do not snipe' table is included too)."""
    out = set()
    try:
        for line in open(os.path.join(HERE, "..", "do_not_attack.md")):
            if line.startswith("## Temporary"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if line.startswith("|") and cells and cells[0] not in ("Player", "") and not cells[0].startswith("-"):
                out.add(cells[0].lower())
                out.update(c for c in cells if c.startswith("user_"))
    except OSError:
        pass
    return out


SKIP_FOR = {"bracket": 6 * 3600, "village": 24 * 3600, "immune": 0, "move": 60, "other": 600}


def note_attack(st, res):
    """Remember why an attack was refused so the same target is not retried (bracket, ally, immunity...)."""
    a = res.get("combat.attackUser")
    if not a:
        return None
    inp, out, _ = a
    if out.get("success") or out.get("battleId"):
        st["battleId"] = out.get("battleId")
        return None
    msg = (out.get("message") or "").lower()
    kind = ("bracket" if "bracket" in msg else "village" if "village" in msg or "ally" in msg else
            "immune" if "immun" in msg else "move" if "move" in msg else "other")
    st.setdefault("skip", {})[inp.get("userId", "?")] = time.time() + (SKIP_FOR[kind] or 120)
    return f"attack refused ({kind}): {out.get('message')}"


def pick_target(st, users, me_pos):
    now = time.time()
    dna = do_not_attack()
    skip = {u: t for u, t in st.get("skip", {}).items() if t > now}
    st["skip"] = skip
    cands, why = [], {}
    for k in range(len(users.get("users.*.userId") or [])):
        t = {f: users[f"users.*.{f}"][k] for f in ("userId", "username", "longitude", "latitude", "status", "level",
                                                     "villageId", "immunityUntil", "battleId")}
        imm = t["immunityUntil"]
        immune = bool(imm) and dt.datetime.fromisoformat(str(imm).replace("Z", "+00:00")).timestamp() > now
        reason = ("me" if t["userId"] == ME else "dna" if t["userId"] in dna or (t["username"] or "").lower() in dna
                  else "battle" if t["battleId"] or t["status"] == "BATTLE" else t["status"].lower() if t["status"] != "AWAKE"
                  else "immune" if immune else "ally" if t["villageId"] == HOME_VILLAGE else "lowlvl" if (t["level"] or 0) < 90
                  else "refused" if t["userId"] in skip else None)
        if reason:
            why[reason] = why.get(reason, 0) + 1
            continue
        d = max(abs(t["longitude"] - me_pos[0]), abs(t["latitude"] - me_pos[1]))
        cands.append((d, t))
    why.pop("me", None)
    st["last_scan"] = why
    return min(cands, key=lambda x: x[0])[1] if cands else None


def world(st, user, res):
    """Rules for the awake character outside battle, in priority order. st["mode"]: guard (default), hunt, rest."""
    status, bid = user.get("userData.status"), user.get("userData.battleId")
    sector = user.get("userData.sector")
    me_pos = (user.get("userData.longitude"), user.get("userData.latitude"))
    hp, mx = user.get("userData.curHealth", 0), user.get("userData.maxHealth", 1)
    mode = st.get("mode", "guard")
    if status == "BATTLE" and bid:
        st["battleId"] = bid
        return f"BATTLE START {bid}", [c_battle(bid), c_entries(bid, 200), TICK]
    if status == "ASLEEP":
        if mode == "hunt":
            return "ASLEEP, hunt mode: waking", [call("home.toggleSleep", {}, ["success", "message"]), c_user(), TICK]
        return "ASLEEP: the worker may step away", []
    if status == "HOSPITALIZED":
        return "HOSPITALIZED: healing", [call("hospital.npcHeal", {"villageId": HOME_VILLAGE}, ["success", "message"]),
                                        c_user(), TICK]
    start = res.get("travel.startGlobalMove")
    if start and start[1].get("data.travelFinishAt"):
        st["arrive"] = dt.datetime.fromisoformat(start[1]["data.travelFinishAt"].replace("Z", "+00:00")).timestamp()
    if status not in ("AWAKE", "BATTLE", "ASLEEP", "HOSPITALIZED"):     # mid-travel: wait for the arrival time
        left = max(0.0, st["arrive"] - time.time()) if st.get("arrive") else 5.0   # unknown arrival: retry every 5 s
        return f"{status}: arriving in {left:.0f}s", ([wait(round(min(left + 0.5, 20), 1))] if left > 0 else []) + \
            [call("travel.finishGlobalMove", {}, ["success", "message"]), c_user(), TICK]
    head = f"AWAKE {mode} {hp:.0f}/{mx:.0f} HP @ {sector} {me_pos}"
    if mode == "rest":
        if sector != HOME_SECTOR:
            return head + ": going home", go(HOME_SECTOR)
        return head + ": sleeping", [call("home.toggleSleep", {}, ["success", "message"]), c_user(), TICK]
    if mode == "guard":
        return head + ": guarding", [wait(GUARD_WAIT), c_user(), TICK]
    # hunt: top up first. A heal that changed nothing is not retried for 10 min (a loop guard, not a fix)
    pools = {"hp": hp / mx,
             "cpsp": min(user.get("userData.curChakra", 1) / max(1, user.get("userData.maxChakra", 1)),
                         user.get("userData.curStamina", 1) / max(1, user.get("userData.maxStamina", 1)))}
    last = st.pop("healing", None)
    if last and pools[last[0]] <= last[1] + 1e-9:
        st.setdefault("heal_broken", {})[last[0]] = time.time() + 600
    broken = {k for k, t in st.get("heal_broken", {}).items() if t > time.time()}
    if pools["hp"] < HEAL_BELOW and "hp" not in broken:
        st["healing"] = ["hp", pools["hp"]]
        return head + ": Full Potion", [call("item.consume", {"userItemId": FULL_POTION}, ["success", "message"]),
                                       c_user(), TICK]
    if pools["cpsp"] < POOLS_BELOW and "cpsp" not in broken:
        st["healing"] = ["cpsp", pools["cpsp"]]
        return head + ": ramen", [call("village.buyFood", {"ramen": "large"}, ["success", "message"]), c_user(), TICK]
    refused = note_attack(st, res)
    scan = res.get("travel.getSectorData")
    if scan and scan[0].get("sector") == sector:
        t = pick_target(st, scan[1], me_pos)
        if t:
            moves = [] if (t["longitude"], t["latitude"]) == me_pos else [c_move(me_pos, (t["longitude"], t["latitude"]), sector)]
            return head + f": attacking {t['username']} @ {t['longitude']},{t['latitude']}", \
                moves + [c_attack(t, sector), c_user(), TICK]
        if sector in CIRCUIT or sector == HOME_SECTOR:
            nxt = CIRCUIT[(CIRCUIT.index(sector) + 1) % len(CIRCUIT)] if sector in CIRCUIT else CIRCUIT[0]
            seen = ", ".join(f"{n} {k}" for k, n in sorted(st.get("last_scan", {}).items())) or "empty"
            return head + f": nobody to fight here ({seen}){'; ' + refused if refused else ''}, next sector {nxt}", go(nxt)
    if sector not in CIRCUIT:
        return head + f": heading to the circuit ({CIRCUIT[0]})", go(CIRCUIT[0])
    batch = [wait(HUNT_WAIT), c_user(), c_sector(sector)]
    if time.time() - st.get("sensory", 0) > 31:
        st["sensory"] = time.time()
        batch.append(call("stealth.useSensory", {"sector": sector}, ["success", "message"]))
    return head + ": scanning", batch + [TICK]


def go(sector):
    return [call("travel.startGlobalMove", {"sector": sector}, ["success", "message", "data.travelFinishAt"]),
            call("travel.finishGlobalMove", {}, ["success", "message"]), c_user(), c_sector(sector), TICK]


# ---------------------------------------------------------------- tick
def tick():
    st = load_state()
    if len(sys.argv) > 2 and sys.argv[1] == "--mode":
        st["mode"] = sys.argv[2]
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
        head, batch = world(st, res["profile.getUser"][1], res)
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
