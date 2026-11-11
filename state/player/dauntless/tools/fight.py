#!/usr/bin/env python3
"""Scripted live-PvP turn (director 2026-11-11: missed turns in three straight fights; 10 s per turn; "AI driven
approach with scripted tool calls"; auto-combat is for fights against the game's AI only).

A turn is three steps and no deliberation:
  1. ONE parallel read (both calls in one message):
       combat.getBattle {battleId}  select: battle.version, battle.round, battle.activeUserId,
         battle.usersState.*.userId|username|curHealth|maxHealth|longitude|latitude|actionPoints
       combat.getBattleEntries {battleId, limit: 8 (first poll of a battle: 200)}
         select: *.id, *.battleRound, *.userId, *.actionId, *.appliedEffects.*.txt
  2. `python3 fight.py` with NO arguments. It reads both results straight from the session transcript (Claude Code
     writes each tool result there before the next call runs: ~40 ms), merges new log entries into a per-battle
     cache by entry id (the cache keeps the log after the battle is deleted), and plans:
       his turn: full planner + engine re-score, stored as the DEFAULT for my next turn (off the clock);
       my turn: fast planner (python only) inside --budget (3.5 s); over budget, or past ~36 s into my turn, it
       prints the stored default instead.
  3. Fire the printed performAction inputs back to back, versions already filled in. Re-poll only to verify.
`--stdin` takes the merged JSON on stdin instead (offline tests).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
CACHE_DIR = os.path.join(HERE, "..", "fights", "live")
# my turn: python planner only, shortlist sized by the regression study; the engine checks ran on his turn
MY_TURN_FLAGS = ("--no-engine",)
ENT_KEYS = ("*.id", "*.battleRound", "*.userId", "*.actionId", "*.appliedEffects.*.txt")


def cache_path(bid):
    return os.path.join(CACHE_DIR, f"{bid}.json")


def default_path(bid):
    return os.path.join(CACHE_DIR, f"{bid}.default.json")


def load_default(bid):
    try:
        d = json.load(open(default_path(bid)))
        return d.get("plan"), d.get("for")
    except (OSError, ValueError):
        return None, None


def load_cache(bid):
    try:
        return json.load(open(cache_path(bid)))
    except (OSError, ValueError):
        return {"battleId": bid, "entries": [], "default": None, "default_for": None}


def save_cache(c):
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = cache_path(c["battleId"]) + ".tmp"
    json.dump(c, open(tmp, "w"), indent=0)
    os.replace(tmp, cache_path(c["battleId"]))


def merge(cache, inp):
    """Add new entries (newest-first in the input) to the cache (kept oldest-first), by entry id."""
    if "*.id" not in inp:
        return 0
    seen = {e[0] for e in cache["entries"]}
    new = [list(x) for x in zip(*(inp.get(k, []) for k in ENT_KEYS)) if x[0] not in seen]
    cache["entries"].extend(new[::-1])
    return len(new)


def battle_part(inp):
    return {k: v for k, v in inp.items() if k.startswith("battle.")}


def turn_file(battle, entries, path):
    rows = entries[::-1]   # turn.py wants newest-first, like the connector
    ents = {k: [r[i] for r in rows] for i, k in enumerate(ENT_KEYS) if k != "*.id"}
    with open(path, "w") as f:
        f.write(json.dumps(battle) + "\n" + json.dumps(ents) + "\n")


def run_turn(path, bid, enemy, budget, extra=()):
    cmd = [sys.executable, os.path.join(HERE, "turn.py"), path, "--battle", bid, "--top", "1", *extra]
    if enemy:
        cmd += ["--enemy", enemy]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=budget).stdout
    except subprocess.TimeoutExpired:
        return None, "planner over budget"
    m = re.search(r"^FIRE: (.*)$", out, re.M)
    if not m:
        tail = [l for l in out.splitlines() if l.strip()][-2:]
        return None, "no FIRE line: " + " | ".join(tail)
    return json.loads(m.group(1)), ""


def transcript_path():
    """The live session transcript (Claude Code writes every tool result here before the next call runs)."""
    p = os.environ.get("TNR_TRANSCRIPT")
    if p:
        return p
    import glob
    files = glob.glob("/root/.claude/projects/*/*.jsonl")
    return max(files, key=os.path.getmtime) if files else None


def from_transcript(tail=400_000):
    """Newest combat.getBattle and combat.getBattleEntries results (and the battleId asked for), read straight from
    the transcript: the turn never retypes a read (director 2026-11-11: 10 s per turn, scripted tool calls)."""
    path = transcript_path()
    if not path:
        return None, None
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(max(0, size - tail))
        lines = f.read().decode("utf8", "ignore").splitlines()
    asked, got = {}, {}
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
                ep = (c.get("input") or {}).get("endpointName")
                if ep in ("combat.getBattle", "combat.getBattleEntries"):
                    asked[c["id"]] = (ep, ((c.get("input") or {}).get("input") or {}).get("battleId"))
            elif c.get("type") == "tool_result" and c.get("tool_use_id") in asked:
                body = c.get("content")
                text = body if isinstance(body, str) else "".join(x.get("text", "") for x in body or [] if isinstance(x, dict))
                try:
                    got[asked[c["tool_use_id"]][0]] = (asked[c["tool_use_id"]][1], json.loads(text))
                except ValueError:
                    pass
    if "combat.getBattle" not in got:
        return None, None
    bid, battle = got["combat.getBattle"]
    inp = dict(battle)
    e = got.get("combat.getBattleEntries")
    if e and e[0] == bid:
        inp.update(e[1])
    return bid, inp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("battle", nargs="?", help="default: the battle of the newest getBattle read in the transcript")
    ap.add_argument("--enemy")
    ap.add_argument("--budget", type=float, default=3.5)
    ap.add_argument("--stdin", action="store_true", help="read the merged JSON from stdin instead of the transcript")
    ap.add_argument("--preplan", help=argparse.SUPPRESS)
    ap.add_argument("--key", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.preplan:   # detached worker started by a his-turn poll
        plan, _ = run_turn(a.preplan, a.battle, a.enemy or None, 60)
        if plan:
            tmp = default_path(a.battle) + ".tmp"
            json.dump({"plan": plan, "for": json.loads(a.key)}, open(tmp, "w"))
            os.replace(tmp, default_path(a.battle))
        try:
            os.unlink(os.path.join(CACHE_DIR, f"{a.battle}.pre.lock"))
        except OSError:
            pass
        return
    t0 = time.time()
    if a.stdin:
        inp = json.loads(sys.stdin.read())
    else:
        bid, inp = from_transcript()
        if inp is None:
            sys.exit("no combat.getBattle result in the transcript yet")
        a.battle = a.battle or bid
    if not a.battle:
        sys.exit("battle id needed")
    c = load_cache(a.battle)
    n_new = merge(c, inp)
    battle = battle_part(inp) or c.get("battle")
    if not battle:
        sys.exit("no battle state in input or cache")
    c["battle"] = battle
    us = battle["battle.usersState.*.userId"]
    names = battle["battle.usersState.*.username"]
    hp = battle["battle.usersState.*.curHealth"]
    me_i = us.index(ME)
    en_i = next((i for i in range(len(us)) if i != me_i and hp[i] > 0), None)
    enemy = a.enemy or (names[en_i] if en_i is not None else None)
    R, v = battle["battle.round"], battle["battle.version"]
    mine = battle["battle.activeUserId"] == ME
    # turn clock: the battle exposes no timer we read, so time the turn from the first poll that saw it
    tk = [R, battle["battle.activeUserId"]]
    if c.get("turn_key") != tk:
        c["turn_key"], c["turn_seen"] = tk, t0
    elapsed = t0 - c["turn_seen"]
    status = (f"R{R} v{v} {'MY TURN' if mine else 'his turn'} {elapsed:.0f}s | me {hp[me_i]:.0f}"
              + (f" | {enemy} {hp[en_i]:.0f}" if en_i is not None else " | no living enemy") + f" | +{n_new} entries")
    save_cache(c)
    if en_i is None:
        print(status); return
    path = os.path.join(CACHE_DIR, f"{a.battle}.turn.txt")
    if not mine:
        # his turn: return at once (the poll loop's speed IS my turn-detection lag) and pre-plan the default for my
        # next turn in a detached process, full planner + engine re-score, off the clock
        b = dict(battle)
        b["battle.activeUserId"] = ME
        aps = list(b["battle.usersState.*.actionPoints"]); aps[me_i] = 100
        b["battle.usersState.*.actionPoints"] = aps
        pre = os.path.join(CACHE_DIR, f"{a.battle}.pre.txt")
        turn_file(b, c["entries"], pre)
        key = [R, len(c["entries"])]
        lock = os.path.join(CACHE_DIR, f"{a.battle}.pre.lock")
        busy = os.path.exists(lock) and time.time() - os.path.getmtime(lock) < 45
        if load_default(a.battle)[1] != key and not busy:
            open(lock, "w").close()
            subprocess.Popen([sys.executable, os.path.abspath(__file__), a.battle, "--preplan", pre,
                              "--enemy", enemy or "", "--key", json.dumps(key)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        d = load_default(a.battle)[0]
        print(status + " | default: " + (" + ".join(x["name"] for x in d) if d else "none yet"))
        return
    turn_file(battle, c["entries"], path)
    # hard deadline: past 30 s into my turn there is no time to plan; fire the default (60 s turn timer)
    left = min(a.budget, 38 - elapsed) - (time.time() - t0)
    plan, err = (run_turn(path, a.battle, enemy, left, MY_TURN_FLAGS) if left >= 1.5
                 else (None, f"{elapsed:.0f}s into my turn"))
    src = "fresh"
    if not plan:
        plan, src = load_default(a.battle)[0], f"DEFAULT ({err})"
    print(status + f" | plan {src} ({time.time() - t0:.1f}s)")
    if not plan:
        print("NO PLAN: fire defensiveStance + best 60 manually"); return
    print(f"FIRE v{v}: " + " + ".join(x["name"] for x in plan))
    for k, x in enumerate(plan):
        print(json.dumps({"battleId": a.battle, "actionId": x["actionId"], "longitude": x["longitude"],
                          "latitude": x["latitude"], "version": v + k}))


if __name__ == "__main__":
    main()
