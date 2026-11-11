"""The world model: one store for everything the player knows, saved after every result (design 4.2).

Every read updates the model, and every module reads the model rather than a raw response. The file on disk is the
whole state: a brain that restarts loads it and carries on.

Sections shared by all modules: control (the director's settings), character, map, opponents, battle (read-only
outside the battle activity), records, decisions. Each activity also has a private section (own(name)); no
activity reads another's.

The world also writes the console's event log, live/events.jsonl (brief AP7 section 1): one line per fight start
or end, activity done, purchase, error or stall, pending decision raised or answered, setting changed, and finding.
"""
import collections
import copy
import datetime as dt
import hashlib
import json
import os
import time

from . import config as C

Result = collections.namedtuple("Result", "endpoint input data error at")
"""One answered call. data: the selected response (a dict), or None. error: None, "rate_limited", or the
connector's error text."""

RATE_LIMITED = "rate_limited"

EVENT_KINDS = ("fight_start", "fight_end", "activity_done", "training_finished", "item", "repair", "error", "stall",
               "decision_raised", "decision_answered", "setting_changed", "finding")
"""The lines of live/events.jsonl (brief AP7 section 1). "finding" is the one kind the brief does not list by
name: a refused call, a late or missed turn, a suspected bug (the console's Decisions tab shows recent findings)."""

TEMPLATE = {
    "version": 1,
    "control": {                # the director's settings as last applied from live/control.json (player/console.py)
        "version": 0, "paused": False, "mode": "guard", "director_mode": False, "activities": {},
        "goal_weights": {}, "spend_caps": {}, "do_not_attack": [], "end_session": False},
    "character": {},            # the last profile read, plus read_at
    "inventory": {},            # AP2
    "training": {},             # AP2
    "timers": {},               # arrival time of a trip, and later the daily resets
    "battle": None,             # the fight in progress: the state the combat tools read (battle activity)
    "opponents": {"lost_to": {}, "skip": {}},
    "map": {"scan": None, "last_scan": {}, "sensory_at": 0},
    "records": {"results": [], "pending_result": None, "spend": {"day": "", "ryo": 0.0}, "transfers": {},
                "turns_missed": 0, "turns_unresolved": 0, "turns_unseen": 0, "last_error": None},
    "decisions": [],            # pending decisions for the director (ask-first calls)
    "budget": {"calls": []},    # [time, lane] of every call issued in the last minute
    "relay": {"seq": 0, "last_batch": [], "issued_at": 0, "expect": None, "stalled": False, "activity": None,
              "note": "", "baseline_tokens": None, "context_tokens": 0, "rotations": 0},
    "activity": {},             # private state, by activity name
}


def utc_day(now):
    return dt.datetime.fromtimestamp(now, dt.timezone.utc).strftime("%Y-%m-%d")


def parse_time(text):
    """An ISO time from the game -> epoch seconds, or None."""
    try:
        return dt.datetime.fromisoformat(str(text).replace("Z", "+00:00")).timestamp()
    except (TypeError, ValueError):
        return None


class World:
    def __init__(self, live=None, clock=time.time):
        self.live = live or C.live_dir()
        self.path = os.path.join(self.live, "world.json")
        self.clock = clock
        self.d = copy.deepcopy(TEMPLATE)
        self.load()

    # ------------------------------------------------------------ disk
    def load(self):
        try:
            with open(self.path, encoding="utf8") as f:
                saved = json.load(f)
        except (OSError, ValueError):
            return False
        for k, v in saved.items():
            if k in TEMPLATE:                       # an unknown section is dropped, never guessed at
                if isinstance(TEMPLATE[k], dict) and isinstance(v, dict):
                    self.d[k] = {**copy.deepcopy(TEMPLATE[k]), **v}
                else:
                    self.d[k] = v
        return True

    def save(self):
        os.makedirs(self.live, exist_ok=True)
        tmp = f"{self.path}.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf8") as f:
            json.dump(self.d, f, separators=(",", ":"))
        os.replace(tmp, self.path)

    def _append(self, name, row):
        os.makedirs(self.live, exist_ok=True)
        with open(os.path.join(self.live, name), "a", encoding="utf8") as f:
            f.write(json.dumps(row, separators=(",", ":")) + "\n")

    # ------------------------------------------------------------ sections
    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        if key not in TEMPLATE:
            raise KeyError(f"{key} is not a section of the world model")
        self.d[key] = value

    def own(self, activity):
        """An activity's private state."""
        return self.d["activity"].setdefault(activity, {})

    @property
    def now(self):
        return self.clock()

    # ------------------------------------------------------------ the character
    @property
    def me(self):
        return self.d["character"]

    def status(self):
        return self.me.get("status")

    def in_battle(self):
        return bool(self.d["battle"])

    def position(self):
        return (self.me.get("longitude"), self.me.get("latitude"))

    def pools(self):
        """{"hp": ratio, "cpsp": the lower of chakra and stamina, as a ratio}."""
        m = self.me
        return {"hp": (m.get("curHealth") or 0) / max(1.0, m.get("maxHealth") or 1),
                "cpsp": min((m.get("curChakra") or 1) / max(1.0, m.get("maxChakra") or 1),
                            (m.get("curStamina") or 1) / max(1.0, m.get("maxStamina") or 1))}

    # ------------------------------------------------------------ results
    def absorb(self, results):
        """Fold the reads every module shares into the model: my profile, and a trip's arrival time."""
        for r in results:
            if r.error or not isinstance(r.data, dict):
                continue
            if r.endpoint == "profile.getUser":
                self._profile(r)
            elif r.endpoint == "travel.startGlobalMove" and r.data.get("data.travelFinishAt"):
                t = parse_time(r.data["data.travelFinishAt"])
                if t:
                    self.d["timers"]["arrive"] = t

    def _profile(self, r):
        new = {k.split(".", 1)[1]: v for k, v in r.data.items() if k.startswith("userData.")}
        if "status" not in new:
            return
        old = self.me
        # what was spent: a fall in pocket plus bank between two reads (measured, never estimated)
        if old.get("money") is not None and new.get("money") is not None:
            before = float(old.get("money") or 0) + float(old.get("bank") or 0)
            after = float(new.get("money") or 0) + float(new.get("bank") or 0)
            spend = self.d["records"]["spend"]
            if spend.get("day") != utc_day(r.at):
                spend.update(day=utc_day(r.at), ryo=0.0)
            if after < before:
                spend["ryo"] = spend.get("ryo", 0.0) + (before - after)
        new["read_at"] = r.at
        self.d["character"] = new

    def spent_today(self):
        spend = self.d["records"]["spend"]
        return spend.get("ryo", 0.0) if spend.get("day") == utc_day(self.now) else 0.0

    # ------------------------------------------------------------ the console's event log
    def event(self, kind, text, **fields):
        """One line in live/events.jsonl. kind is one of EVENT_KINDS."""
        if kind not in EVENT_KINDS:
            raise ValueError(f"{kind} is not an event kind")
        at = dt.datetime.fromtimestamp(self.now, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self._append("events.jsonl", {"at": at, "kind": kind, "text": text[:400], **fields})
        if kind in ("error", "stall", "finding"):
            self.d["records"]["last_error"] = {"at": at, "kind": kind, "text": text[:200]}

    def decide(self, key, text, step=None):
        """Raise a pending decision for the director once. Returns True when it is new."""
        if any(d["key"] == key and not d.get("answer") for d in self.d["decisions"]):
            return False
        did = hashlib.sha1(key.encode("utf8")).hexdigest()[:8]
        self.d["decisions"].append({"id": did, "key": key, "text": text, "raised": round(self.now, 1), "answer": None,
                                    "call": {k: step[k] for k in ("call", "input")} if step else None})
        self.d["decisions"] = self.d["decisions"][-50:]
        self.event("decision_raised", text, id=did)
        return True

    def answered(self, key):
        """The director's answer to a decision ("yes" / "no"), or None while it is pending or was never raised."""
        for d in self.d["decisions"]:
            if d["key"] == key and d.get("answer"):
                return d["answer"]
        return None
