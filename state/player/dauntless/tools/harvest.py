"""Battle-log harvester (director 2026-11-11: "Pull every log you can, model as many opponents as possible").

The game keeps finished battles' action logs (combat.getBattleEntries works on any battle id, verified on a fight
from the day before) and lists any player's battles (combat.getBattleHistory {userId}: battle id, type, winner =
attackedId, loser = defenderId). The pilot spends spare call budget between fights on this crawl:
  users  : seeds (everyone in my own logs, the ranked top list) and every player met in a harvested PvP battle
  battles: PvP battles of those users, newest first; each log saved once to fights/observed/<battleId>.json with
           both players' ids, names and the winner, for opponents.py to model both sides.
Pure planning here (next calls + ingest of their results); pilot.py sends the calls under its rate budget.
"""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OBS = os.path.join(HERE, "..", "fights", "observed")
STATE = os.path.join(OBS, "harvest.json")
PVP = ["COMBAT", "RANKED_PVP", "RANKED_SPARRING", "SPARRING", "TOURNAMENT", "KAGE_PVP", "CLAN_CHALLENGE"]
HIST_SEL = ["data.*.battleId", "data.*.battleType", "data.*.attackedId", "data.*.defenderId",
            "data.*.attacker.username", "data.*.defender.username", "data.*.createdAt"]
ENT_SEL = ["*.id", "*.battleRound", "*.userId", "*.actionId", "*.appliedEffects.*.txt"]
USER_EVERY = 6 * 3600          # re-crawl a player's history after this long
MAX_BATTLES_PER_USER = 30


def load():
    try:
        return json.load(open(STATE))
    except (OSError, ValueError):
        return {"users": {}, "battles": {}, "seeded": False}


def save(h):
    os.makedirs(OBS, exist_ok=True)
    json.dump(h, open(STATE, "w"))


def seed(h, user_ids):
    for u in user_ids:
        if u and u.startswith("user_"):
            h["users"].setdefault(u, {"crawled": 0})
    h["seeded"] = True


def next_calls(h, n=1):
    """Up to n calls: a pending battle log first (they age out of nobody's history), else the stalest player."""
    out = []
    pending = [b for b, v in h["battles"].items() if not v.get("fetched")]
    pending.sort(key=lambda b: h["battles"][b].get("createdAt") or "", reverse=True)
    # at most one call per endpoint per batch: the pilot reads the newest result of each endpoint per tick
    for b in pending[:1]:
        out.append(("combat.getBattleEntries", {"battleId": b, "limit": 400}, ENT_SEL))
    if len(out) < n:
        now = time.time()
        stale = sorted((v.get("crawled", 0), u) for u, v in h["users"].items() if now - v.get("crawled", 0) > USER_EVERY)
        for _, u in stale[:1]:
            out.append(("combat.getBattleHistory", {"userId": u, "limit": MAX_BATTLES_PER_USER, "combatTypes": PVP},
                        HIST_SEL))
    return out


def ingest(h, endpoint, inp, data):
    """Fold one result in. Returns a short note or None."""
    if not isinstance(data, dict):
        return None
    if endpoint == "combat.getBattleHistory":
        u = inp.get("userId")
        if u in h["users"]:
            h["users"][u]["crawled"] = time.time()
        ids = data.get("data.*.battleId") or []
        g = lambda k, i: (data.get(f"data.*.{k}") or [None] * len(ids))[i]
        new = 0
        for i, b in enumerate(ids):
            a, d = g("attackedId", i), g("defenderId", i)
            if not (a or "").startswith("user_") or not (d or "").startswith("user_"):
                continue
            if b not in h["battles"]:
                h["battles"][b] = {"type": g("battleType", i), "winner": a, "loser": d, "createdAt": g("createdAt", i),
                                   "names": {a: g("attacker.username", i), d: g("defender.username", i)}}
                new += 1
            for x in (a, d):
                h["users"].setdefault(x, {"crawled": 0})
        return f"history {u}: {new} new battles"
    if endpoint == "combat.getBattleEntries":
        b = inp.get("battleId")
        meta = h["battles"].get(b)
        if meta is None or not data.get("*.battleRound"):
            if meta is not None:
                meta["fetched"] = True               # empty log: nothing to keep, don't ask again
            return None
        meta["fetched"] = True
        os.makedirs(OBS, exist_ok=True)
        json.dump(dict(data, _meta=dict(meta, battleId=b)), open(os.path.join(OBS, f"{b}.json"), "w"))
        return f"log {b}: {len(data['*.battleRound'])} entries"
    return None


def stats(h):
    got = sum(1 for v in h["battles"].values() if v.get("fetched"))
    return f"{len(h['users'])} players, {got}/{len(h['battles'])} battle logs"
