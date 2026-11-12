"""The console's data (brief AP7 section 1), written by the brain from AP1 on so AP7 only adds a view.

    live/status.json    rewritten on every change: what the player is doing and why, what is queued, the character,
                        the fight, the relay's health, the call budget, tokens in the last hour
    live/events.jsonl   append-only, written by World.event
    live/control.json   the director's settings, versioned. The brain applies a new version at its next tick,
                        checks every change, and records each one in the event log

A setting can only narrow or steer what the gates already allow. Nothing here can put an endpoint on the allowlist,
lift a never rule or take a name off do_not_attack.md.
"""
import datetime as dt
import os

from . import config as C
from . import relay

MODES = ("hunt", "guard")                 # farm and rest arrive with AP3 and AP2
ALWAYS_ON = ("battle", "recovery", "travel", "watch", "session")   # switching these off loses turns or the character


def iso(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if t else None


# ---------------------------------------------------------------- control.json
def _number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0


def _map(value, key_ok, value_ok):
    return isinstance(value, dict) and all(key_ok(k) and value_ok(v) for k, v in value.items())


def _switches(value, world, activities):
    if not _map(value, lambda k: True, lambda v: isinstance(v, bool)):
        return "must map activity names to true or false"
    bad = [k for k in value if k not in activities]
    off = [k for k, v in value.items() if not v and k in ALWAYS_ON]
    return f"unknown activity {bad[0]}" if bad else f"{off[0]} cannot be switched off" if off else None


def _names(value, world, activities):
    if not (isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value)):
        return "must be a list of names or user ids"
    if not {x.lower() for x in world["control"]["do_not_attack"]} <= {x.lower() for x in value}:
        return "names are only ever added here; do_not_attack.md is edited to take one off"
    return None


def _rule(ok, why):
    return lambda value, world, activities: None if ok(value) else why


SETTINGS = {
    "paused": _rule(lambda v: isinstance(v, bool), "must be true or false"),
    "director_mode": _rule(lambda v: isinstance(v, bool), "must be true or false"),
    "end_session": _rule(lambda v: isinstance(v, bool), "must be true or false"),
    "mode": _rule(lambda v: v in MODES, "is not available yet (hunt or guard)"),
    "activities": _switches,
    "goal_weights": _rule(lambda v: _map(v, lambda k: k in C.goals()["weights"], _number),
                          "must map known goals to numbers of 0 or more"),
    "spend_caps": _rule(lambda v: _map(v, lambda k: k in ("daily", "reserve"), _number), "must be {daily, reserve} in ryo"),
    "do_not_attack": _names,
    "answers": _rule(lambda v: _map(v, lambda k: True, lambda a: a in ("yes", "no")),
                     "must map decision ids to yes or no"),
}
"""Every setting the director can change, and the check each change must pass. Anything else is refused."""


def _check(key, value, world, activities):
    """None when a setting is acceptable, else why not."""
    return SETTINGS[key](value, world, activities) if key in SETTINGS else "not a setting"


def apply_control(world, activities):
    """Read live/control.json and apply a new version. Every accepted change and every refused one is an event."""
    doc = relay.read(os.path.join(world.live, "control.json"))
    cur = world["control"]
    if not isinstance(doc, dict) or doc.get("version") == cur["version"]:
        return
    for key, value in doc.items():
        if key == "version":
            continue
        why = _check(key, value, world, activities)
        if why:
            world.event("error", f"setting refused: {key}: {why}", about="control")
        elif key == "answers":
            _answers(world, value)
        elif cur.get(key) != value:
            world.event("setting_changed", f"{key}: {cur.get(key)!r} -> {value!r}", setting=key)
            cur[key] = value
    cur["version"] = doc.get("version")


def _answers(world, answers):
    for d in world["decisions"]:
        a = answers.get(d.get("id"))
        if a and d.get("answer") != a:
            d["answer"] = a
            world.event("decision_answered", f"{a}: {d['text']}", id=d["id"], answer=a)


def set_control(live, **changes):
    """Write a new version of live/control.json with these settings changed (the CLI, and Duet's copy step)."""
    path = os.path.join(live, "control.json")
    doc = relay.read(path) or {"version": 0}
    for k, v in changes.items():
        if isinstance(v, dict) and isinstance(doc.get(k), dict):
            doc[k] = {**doc[k], **v}
        else:
            doc[k] = v
    doc["version"] = int(doc.get("version") or 0) + 1
    relay.write(path, doc)
    return doc


# ---------------------------------------------------------------- status.json
def _battle(world):
    b = world["battle"]
    if not b:
        return None
    turn = b.get("turn") or {}
    return {"id": b["bid"], "opponent": b.get("enemy"), "round": b.get("round"), "seat": b.get("seat"),
            "my_hp": b.get("my_hp"), "his_hp": b.get("his_hp"),
            "his_windows": None,          # his damage curve and tool windows: the planner states them from AP4 on
            "pick": b.get("pick"), "turn_started": iso(turn.get("T")), "fired": iso(turn.get("fired_at"))}


def write_status(world, budget, activity, why, queue):
    """Rewrite live/status.json. queue: [(name, why, eta in seconds), ...], the next activities in line."""
    me, now, r = world.me, world.now, world["relay"]
    silent = max(0.0, now - r["issued_at"] - r["expect"]) if r.get("expect") is not None else 0.0
    relay.write(os.path.join(world.live, "status.json"), {
        "schema": 1, "at": iso(now), "account": C.ACCOUNT,
        "mode": world["control"]["mode"], "paused": world["control"]["paused"],
        "director_mode": world["control"]["director_mode"], "control_version": world["control"]["version"],
        "activity": {"name": activity, "why": why},
        "queue": [{"name": n, "why": w, "eta_s": e} for n, w, e in queue[:5]],
        "character": {"status": me.get("status"), "hp": me.get("curHealth"), "max_hp": me.get("maxHealth"),
                      "chakra": me.get("curChakra"), "max_chakra": me.get("maxChakra"),
                      "stamina": me.get("curStamina"), "max_stamina": me.get("maxStamina"),
                      "sector": me.get("sector"), "x": me.get("longitude"), "y": me.get("latitude"),
                      "money": me.get("money"), "bank": me.get("bank"), "energy": me.get("curEnergy"),
                      "read_at": iso(me.get("read_at"))},
        "battle": _battle(world),
        "relay": {"healthy": not r.get("stalled"), "silent_s": round(silent, 1),
                  "last_batch_at": iso(r.get("issued_at")), "context_tokens": r.get("context_tokens"),
                  "rotations": r.get("rotations", 0)},
        "budget": {"limit": C.CALL_LIMIT, "last_minute": budget.used(now),
                   **{lane: budget.used(now, lane) for lane in ("battle", "recovery", "world")},
                   # calls held for relays that were replaced with a batch in hand (`brain stopped` ends a hold)
                   "held": [{"relay": token, "calls": n, "since": iso(since)} for token, n, since in budget.loose()]},
        "tokens": relay.tokens_summary(world.live, now),
        "decisions_pending": [{"id": d["id"], "text": d["text"]} for d in world["decisions"] if not d.get("answer")],
        "fights_today": _today(world), "turns_missed": world["records"].get("turns_missed", 0),
        "turns_unresolved": world["records"].get("turns_unresolved", 0),
        "turns_unseen": world["records"].get("turns_unseen", 0),
        "spent_today": world.spent_today(), "last_error": world["records"].get("last_error")})


def _today(world):
    day = dt.datetime.fromtimestamp(world.now, dt.timezone.utc).date()
    res = [r for r in world["records"]["results"]
           if len(r) > 2 and dt.datetime.fromtimestamp(r[2], dt.timezone.utc).date() == day]
    return {"won": sum(1 for r in res if r[1] == "won"), "lost": sum(1 for r in res if r[1] == "lost")}
