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
HUNT_WAIT = 8           # hunt tick ~every 10 s: 3 game calls a tick, ~18 a minute (connector cap 30)
GUARD_WAIT = 7          # world tick ~every 9 s with overhead: inside the 15 s lobby before an attack lands
POLL_GAP = 3           # seconds between his-turn polls: ~20 calls/min in a fight (connector cap 30)
PLAN_BUDGET = 4.0       # planner: median 1.2 s, worst 3.3 s on the regression set
ENT = ("*.id", "*.battleRound", "*.userId", "*.actionId", "*.appliedEffects.*.txt")

# ---------------------------------------------------------------- the calls the pilot can ask for (one place)
def call(endpoint, inp, select):
    return {"call": endpoint, "input": inp, "select": select}


def c_user():
    return call("profile.getUser", {}, ["userData.status", "userData.battleId", "userData.curHealth",
                                        "userData.maxHealth", "userData.sector", "userData.longitude",
                                        "userData.latitude", "userData.curChakra", "userData.maxChakra",
                                        "userData.curStamina", "userData.maxStamina", "userData.money",
                                        "userData.bank"])


def c_items():
    import restock
    return call("item.getUserItems", {}, restock.ITEM_SEL)


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


def c_kit(user_id):
    """His equipped jutsu, read once per opponent at battle start (opp_profile builds his bloodline profile from it)."""
    return call("jutsu.getPublicUserJutsus", {"userId": user_id}, ["*.jutsuId", "*.level", "*.equipped"])


def kit_known(user_id):
    return os.path.exists(os.path.join(HERE, "..", "..", "..", "..", "harness", "pvp_turn", "kit", "opponents",
                                       f"{user_id}.json"))


def c_act(bid, aid, x, y, v):
    return call("combat.performAction", {"battleId": bid, "actionId": aid, "longitude": x, "latitude": y,
                                         "version": v}, ["notification"])


TICK = {"bash": f"cd {HERE} && python3 pilot_safe.py"}   # pilot_safe: falls back to the last good pilot


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


def _last_call(path, tail=60_000):
    """The newest tool_use in a transcript (Claude Code writes it before the call runs)."""
    with open(path, "rb") as f:
        f.seek(max(0, os.path.getsize(path) - tail))
        lines = f.read().decode("utf8", "ignore").splitlines()
    for line in reversed(lines):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        for c in reversed((d.get("message") or {}).get("content") or [] if isinstance((d.get("message") or {}).get("content"), list) else []):
            if c.get("type") == "tool_use":
                return c
    return None


def transcript():
    """The transcript of the session running THIS tick: among recently written transcripts, the one whose newest
    call is a Bash pilot.py run. (Newest-mtime alone picked the supervisor's transcript when it wrote at the same
    moment, 2026-11-11.)"""
    if os.environ.get("TNR_TRANSCRIPT"):
        return os.environ["TNR_TRANSCRIPT"]
    files = sorted(glob.glob("/root/.claude/projects/**/*.jsonl", recursive=True), key=os.path.getmtime, reverse=True)
    now = time.time()
    for path in files[:8]:
        if now - os.path.getmtime(path) > 120:
            break
        c = _last_call(path)
        if c and c.get("name") == "Bash" and re.search(r"pilot(_safe)?\.py", (c.get("input") or {}).get("command", "")):
            return path
    return files[0] if files else None


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
                if "Too Many Requests" in text:
                    out["_rate_limited"] = (None, None, t)
                    continue
                try:
                    ep, inp = asked[c["tool_use_id"]]
                    out[ep] = (inp, json.loads(text), t)
                    if ep == "combat.performAction":
                        out.setdefault("_acts", []).append((inp, out[ep][1]))
                except ValueError:
                    pass
    return out


ITEM_IDS = {"6DnJn4x6LWWXtBu7UZybb", "TtYPd-LcXKeK3sMuhq1TP", "rsc2uO5QuffXzejfhwF_F", "yVNeLzxHSFkNpTPnlm7yQ"}


def note_refusals(st, res):
    """An action the game refuses ("Action not valid anymore": out of stock, locked, out of range) is banned for the
    rest of the battle, so the next plan routes around it instead of resending it until the turn times out
    (zDj54ChWY3kZogLwCkoc1 R1, 2026-11-11: Kim's refused five times, the whole turn lost)."""
    for inp, data in res.get("_acts", []):
        note = str((data or {}).get("notification", ""))
        if "has not started" in note.lower():
            # the 15 s lobby: nothing was refused for cause; the plan is simply resent once the battle starts (two
            # Luka fights, 2026-11-11: the resend rule banned Thunder's / Chakra Shield for the whole battle)
            st["sent_plan"] = None
            st.setdefault("banned", {}).pop(inp.get("battleId"), None)
            return
        if "not valid anymore" in note.lower():
            bid, aid = inp.get("battleId"), inp.get("actionId")
            ban = st.setdefault("banned", {}).setdefault(bid, [])
            if aid not in ban:
                ban.append(aid)
            st["restock_due"] = True                        # an empty item is the usual cause: restock after the fight


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
        # a loss shows as my HP at 0 before the battle closes, so a close with me alive in the last state is a win
        # (Tousen x2 and Thabiento, 2026-11-11: all three "battle closed" logs end on my killing hit)
        last = cache.get("battle") or {}
        lu = last.get("battle.usersState.*.userId") or []
        alive = ME in lu and (last.get("battle.usersState.*.curHealth") or [0] * len(lu))[lu.index(ME)] > 0
        return finish(st, bid, cache, "won" if alive else "battle closed")
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
    foe_id = users[foes[0]]
    ai = battle.get("battle.usersState.*.isAi") or []
    if not (ai and ai[foes[0]]) and not kit_known(foe_id) and cache.get("kit_asked") != foe_id:
        cache["kit_asked"] = foe_id                         # one kit read per opponent, ridden on this tick's poll
        save(cache_path, cache)
        poll = [poll[0], poll[1], c_kit(foe_id), TICK]
    active = battle["battle.activeUserId"]
    if active != ME:
        if active in users and ai and ai[users.index(active)]:
            # an AI's turn only advances when some client calls performAction during it (engine: isAITurn);
            # in PvP the human opponent's client drives his own turn
            me_x, me_y = battle["battle.usersState.*.longitude"][me_i], battle["battle.usersState.*.latitude"][me_i]
            return head + " | AI turn: nudge", [c_act(bid, "wait", me_x, me_y, v)] + poll
        # a fast relay polls every ~2.7 s (~45 calls/min); the connector allows 30/min ("Too Many Requests"
        # mid-fight, 2026-11-11), so his-turn polls pace themselves: ~25 calls/min, ~1 s more detection lag
        return head + " | his turn", [wait(POLL_GAP)] + poll
    # near a kill the python damage model runs ~300 low (ANBU Member R5, 2026-11-11): score with the exact engine
    # a plan already sent for this exact battle version that did not move the version is not resent as is: its first
    # action is banned (covers refusals whose text we did not catch)
    sent = st.get("sent_plan") or {}
    if sent.get("bid") == bid and sent.get("v") == v and sent.get("first"):
        ban = st.setdefault("banned", {}).setdefault(bid, [])
        if sent["first"] not in ban:
            ban.append(sent["first"])
    plan, how = plan_turn(bid, battle, cache["entries"], names[foes[0]], exact=hp[foes[0]] <= 2000,
                          ban=st.get("banned", {}).get(bid, []) + st.get("empty_items", []))
    if plan:
        st["sent_plan"] = {"bid": bid, "v": v, "first": plan[0]["actionId"]}
    if not plan:
        return head + f" | MY TURN, no plan ({how}): defensiveStance", \
            [c_act(bid, "defensiveStance", battle["battle.usersState.*.longitude"][me_i],
                   battle["battle.usersState.*.latitude"][me_i], v)] + poll
    acts = [c_act(bid, a["actionId"], a["longitude"], a["latitude"], v + k) for k, a in enumerate(plan)]
    return head + f" | MY TURN: {' + '.join(a['name'] for a in plan)} ({how})", acts + poll


def plan_turn(bid, battle, entries, enemy, exact=False, ban=()):
    """planner2 on a turn file built from the cache (turn.py as the fallback)."""
    path = os.path.join(LIVE, f"{bid}.turn.txt")
    rows = entries[::-1]                                    # turn.py reads newest-first, like the connector
    with open(path, "w") as f:
        f.write(json.dumps(battle) + "\n" +
                json.dumps({k: [r[i] for r in rows] for i, k in enumerate(ENT) if k != "*.id"}) + "\n")
    t0 = time.time()
    # planner2 (director 2026-11-11: "start it again with the new planner"): numeric engine, his clock and profile,
    # ~0.1-0.5 s; the old python planner stays as the fallback if it fails or overruns
    bans = ("--ban", ",".join(ban)) if ban else ()
    # which planner leads is a state switch (fights/live/pilot.json "planner": "turn" | "planner2"). Default turn.py:
    # planner2 went 0-6 live on 2026-11-11 while it plays too defensively against real players
    # 2026-11-11 Zak fight: every planner call failed live ("over budget") and the defensiveStance stand-in was
    # refused all fight. Budgets now leave room inside the 60 s turn (worst case ~22 s), and failures are reported.
    if load_state().get("planner") == "planner2":
        tries = [("planner2.py", bans, 6.0), ("turn.py", ("--no-engine", "--keep", "6", "--cash", "3") + bans, 6.0)]
    else:
        tries = ([("turn.py", ("--fast",) + bans, 9.0)] if exact else []) + \
            [("turn.py", ("--no-engine",) + bans, 6.0), ("planner2.py", bans, 6.0)]
    tries.append(("planner2.py", (), 10.0))                 # last resort: no bans, long budget
    errs = []
    for script, extra, budget in tries:
        try:
            proc = subprocess.run([sys.executable, os.path.join(HERE, script), path, "--battle", bid, "--top", "1",
                                   "--enemy", enemy, *extra], capture_output=True, text=True, timeout=budget)
            out = proc.stdout
        except subprocess.TimeoutExpired:
            errs.append(f"{script} >{budget:.0f}s")
            continue
        if "FIRE: " not in out:
            errs.append(f"{script}: " + ((proc.stderr.strip().splitlines() or out.strip().splitlines() or ["no output"])[-1])[:120])
        m = re.search(r"^FIRE: (.*)$", out, re.M)
        if m:
            return json.loads(m.group(1)), f"{time.time() - t0:.1f}s {script.split('.')[0]}" + (" engine" if "--fast" in extra else "")
    return None, "planner failed: " + " | ".join(errs)


LOST_TO_HOURS = 6      # a player who just beat me is not attacked again for this long (2026-11-11: Luka, three in a row)


def finish(st, bid, cache, why):
    """Battle over: keep its log for the post-fight tools (the game deletes it), back to the world loop."""
    if why == "lost":
        foes = [u for u in (cache.get("battle") or {}).get("battle.usersState.*.userId") or [] if u != ME]
        for u in foes:
            st.setdefault("lost_to", {})[u] = time.time() + LOST_TO_HOURS * 3600
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
                  else "refused" if t["userId"] in skip
                  else "beat me" if st.get("lost_to", {}).get(t["userId"], 0) > now else None)
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
        left = max(left, 3.0)          # past the arrival time but not arrived yet: pause between retries
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
        return head + ": Full Potion", [call("item.consume", {"userItemId": st.get("full_potion_uid", FULL_POTION)},
                                             ["success", "message"]),
                                       c_user(), TICK]
    if pools["cpsp"] < POOLS_BELOW and "cpsp" not in broken:
        st["healing"] = ["cpsp", pools["cpsp"]]
        return head + ": ramen", [call("village.buyFood", {"ramen": "large"}, ["success", "message"]), c_user(), TICK]
    rs = restock_tick(st, user, res)
    if rs:
        return head + rs[0], rs[1]
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
            return head + f": nobody to fight here ({seen}){'; ' + refused if refused else ''}, next sector {nxt}", \
                go(nxt)[:-1] + harvest_calls(st) + [TICK]
    if sector not in CIRCUIT:
        return head + f": heading to the circuit ({CIRCUIT[0]})", go(CIRCUIT[0])
    batch = [wait(HUNT_WAIT), c_user(), c_sector(sector)]
    if time.time() - st.get("sensory", 0) > 31:
        st["sensory"] = time.time()
        batch.append(call("stealth.useSensory", {"sector": sector}, ["success", "message"]))
    return head + ": scanning" + (f" [logs: {st['harvest']}]" if st.get("harvest") else ""), \
        batch + harvest_calls(st) + [TICK]


def restock_tick(st, user, res):
    """Restock passes between fights (restock.py plans; this sends): read items -> act -> read again, until nothing
    is missing or 4 passes; then every 15 min, or right after a fight where the game refused an item."""
    import restock
    rs = st.setdefault("restock", {"next": 0, "pass": 0, "active": False})
    if rs.get("active"):
        items = res.get("item.getUserItems")
        if not items:
            if rs["pass"] >= 4:
                rs.update(active=False, next=time.time() + restock.EVERY)
                return None
            rs["pass"] += 1
            return ": restock: reading items", [c_items(), c_user(), TICK]
        lst = res.get("auction.getAuctionListings")
        listings = dict(lst[1], _item=rs.get("q")) if lst and lst[1] else None
        calls, notes, q = restock.plan(st, items[1], user, _restock_records(), listings, HOME_VILLAGE,
                                       st.get("full_potion_uid", FULL_POTION))
        rs["pass"] += 1
        batch = [call(*c) for c in calls]
        if q:
            rs["q"] = q[0]
            batch.append(call("auction.getAuctionListings", {"itemName": q[1], "limit": 20, "listingType": "AUCTION"},
                              restock.AUCTION_SEL))
        rs["last"] = notes
        if batch and rs["pass"] < 4:
            return ": restock: " + "; ".join(notes), batch + [c_items(), c_user(), TICK]
        rs.update(active=False, next=time.time() + restock.EVERY)
        rs["pass"] = 0
        return None
    if time.time() >= rs.get("next", 0) or st.pop("restock_due", False):
        rs.update(active=True, q=None)
        rs["pass"] = 0
        return ": restock: reading items", [c_items(), c_user(), TICK]
    return None


def _restock_records():
    import engine_bridge
    import restock
    recs = engine_bridge._records()
    ids = list(restock.TRACK) + [x for x in [load_state().get("full_potion_item")] if x]
    return {i: recs[i]["record"] for i in ids if i in recs}


def harvest_calls(st, n=2):
    """Spare-budget battle-log crawl between fights (harvest.py): at most n reads, only with headroom in the window."""
    import harvest
    recent = [t for t in st.get("calls", []) if t > time.time() - 60]
    if len(recent) > CALL_BUDGET - 8:           # leave room: a fight can start on any tick
        return []
    h = harvest.load()
    if not h.get("seeded"):
        import opponents
        harvest.seed(h, [u for _, _, rows, _ in opponents.load_logs() for _, u, _, _ in rows])
        harvest.save(h)
    return [call(*c) for c in harvest.next_calls(h, n)]


def harvest_ingest(st, res):
    """Fold harvested results in (my own battle's entries are not in the crawl list, so they are ignored)."""
    got = [(ep, res[ep]) for ep in ("combat.getBattleHistory", "combat.getBattleEntries") if ep in res]
    if not got:
        return
    import harvest
    h = harvest.load()
    notes = [harvest.ingest(h, ep, r[0], r[1]) for ep, r in got]
    if any(notes):
        harvest.save(h)
        st["harvest"] = harvest.stats(h)


def go(sector):
    return [call("travel.startGlobalMove", {"sector": sector}, ["success", "message", "data.travelFinishAt"]),
            call("travel.finishGlobalMove", {}, ["success", "message"]), c_user(), c_sector(sector), TICK]



CALL_BUDGET = 22        # reads per rolling 60 s; actions skip the pacing (connector cap 30 for the whole account)


def budget(st, batch):
    """Pace the batch so this pilot never exceeds CALL_BUDGET game calls in any rolling minute: the batch's existing
    in-batch pauses count, and one pause is added in front when the window is full. Every call the pilot issues is
    recorded with the time it will run (2026-11-11: back-offs alone could not clear a rolling window)."""
    now = time.time()
    hist = [t for t in st.get("calls", []) if t > now - 60]
    out, t, added = [], now, 0.0
    for b in batch:
        if "bash" in b and "time.sleep(" in b["bash"]:
            t += float(re.search(r"sleep\(([\d.]+)\)", b["bash"]).group(1))
            out.append(b)
            continue
        if "call" in b:
            recent = [x for x in hist if x > t - 60]
            # my turn's actions never wait: they use the headroom between the budget and the connector's 30 (a 21 s
            # pause landed on my turn in the Eladriel fight, 2026-11-11); only reads are paced
            if b["call"] != "combat.performAction" and len(recent) >= CALL_BUDGET:
                gap = recent[len(recent) - CALL_BUDGET] + 60.5 - t
                out.append(wait(round(gap, 1)))
                t += gap
                added += gap
            hist.append(t + 0.4)
            t += 0.4
        out.append(b)
    st["calls"] = hist[-60:]
    st["budget_wait"] = round(added, 1)
    return out

# ---------------------------------------------------------------- tick
def tick():
    st = load_state()
    if len(sys.argv) > 2 and sys.argv[1] == "--mode":
        st["mode"] = sys.argv[2]
    started = time.time()
    res = fresh_results(st.get("last_tick", 0))
    note_refusals(st, res)
    harvest_ingest(st, res)
    if "jutsu.getPublicUserJutsus" in res:
        inp, data, _ = res["jutsu.getPublicUserJutsus"]
        try:
            import opponent_kit
            opponent_kit.save_kit(inp["userId"], data or {})
        except Exception:  # noqa: BLE001  (a bad kit read must never stop the pilot; the planner uses its stand-in)
            pass
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
    if "_rate_limited" in res and st.get("last_batch"):
        # the connector refused part of the batch: resend the same calls (actions already applied fail harmlessly on
        # the battle version) once the call budget below has room
        head, batch = "RATE LIMITED: resending under the budget", [b for b in st["last_batch"] if "call" in b] + [TICK]
    else:
        st["last_batch"] = batch
    batch = budget(st, batch)
    st["last_tick"] = started
    save(STATE, st)
    print(head + (f" (paced {st['budget_wait']}s)" if st.get("budget_wait") else ""))
    for b in batch:
        print(json.dumps(b, separators=(",", ":")))


if __name__ == "__main__":
    tick()
