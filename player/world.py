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
    "budget": {"calls": [], "batch": None},     # the call ledger (player/budget.py); batch: the id of the one out
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


COUNT = "takeovers.json"


def generation(live):
    """(count, saving) from live/takeovers.json. count: how many ledgers of another version the brains of this
    live folder have taken over and saved as their own, or begun to save and left. saving: a brain is saving
    one now, or one began to and has not finished. (0, False) when the file is not there or cannot be read."""
    try:
        with open(os.path.join(live, COUNT), encoding="utf8") as f:
            kept = json.load(f)
        n = kept["count"]
    except (OSError, ValueError, KeyError, TypeError):
        return 0, False
    return (n if type(n) is int and n > 0 else 0), kept.get("saving") is True


def takeovers(live):
    """The count alone."""
    return generation(live)[0]


def counted(live, write):
    """An unfinished save of a takeover is counted and closed: (count + 1, not saving). The brain that began it
    is gone, and what is on disk now is a takeover of its own, under a name nobody has spoken of. `write`:
    World._write, or what a test puts in its place.

    Only for the one who has the brain's lock (player/brain: a brain that starts, and `brain stopped` with
    nobody home). Whoever only reads a live folder leaves the count alone: a brain that is saving has the
    lock, and its save is its own to finish (review of ce1be6e9: every World that was made counted, so one made
    by a reader between a living brain's writes closed that brain's save, a word was taken for the name of that
    moment, and the brain then finished on the count it had read before)."""
    n, saving = generation(live)
    if saving:
        write(os.path.join(live, COUNT), {"count": n + 1, "saving": False})


def seen(path):
    """A world model file and the count, read so that they belong together: (bytes, the time the file was
    written, count, saving). bytes is None when there is no file. The count is read before and after the file,
    and the file again when it changed in between: a save that ran across the read is not half seen."""
    live = os.path.dirname(path)
    for _ in range(8):
        before = generation(live)
        try:
            with open(path, "rb") as f:
                raw, written = f.read(), os.fstat(f.fileno()).st_mtime_ns
        except OSError:
            raw, written = None, None
        if generation(live) == before:
            break
    return raw, written, before[0], before[1]


def found(path):
    """A short print of a world model file exactly as it stands on disk, readable or not, as the takeover it
    would be; None when there is no file. Whoever reads the same file gets the same print: `brain stopped`
    and the brain name by it the hold that is put on a ledger taken over from another version
    (player/budget.py), from before any brain has it until one has saved it.

    The print is of the file's bytes, of the time it was last written, and of the number of takeovers saved
    here so far. The first save of a taken-over ledger raises that number (World.save), so a file that turns
    up later is another takeover under another name, whatever its bytes and whatever its time: word that was
    said of the first names nothing in the second (second review of c412de4d: an empty file was
    `update-da39a3ee` every time, and a word that `brain next` had kept through a crash let go the hold of a
    later one). The time is there for a file that is written again before any brain has saved it: that is not
    the file the operator spoke of.

    While a takeover is being saved the count and the file do not belong together yet, and the print of that
    moment is nobody's: `brain stopped` asks `seen` and speaks of no name then (review of e4a267cd)."""
    raw, written, count, _ = seen(path)
    return None if raw is None else print_of(raw, written, count)


def print_of(raw, written, count):
    return hashlib.sha1(raw + b"\0%d\0%d" % (written, count)).hexdigest()[:8]


class World:
    def __init__(self, live=None, clock=time.time):
        self.live = live or C.live_dir()
        self.path = os.path.join(self.live, "world.json")
        self.clock = clock
        self.d = copy.deepcopy(TEMPLATE)            # making a World writes nothing: the count is the brain's
        self.found = found(self.path)               # the file as it was on disk (None on a first start),
        self.found_at = os.path.getmtime(self.path) if self.found else None   # and when it was last written
        self.taken_over = False                     # the brain's to set: that file was another version's ledger
        self.load()

    # ------------------------------------------------------------ disk
    def load(self):
        try:
            with open(self.path, encoding="utf8") as f:
                saved = json.load(f)
        except (OSError, ValueError):
            return False
        if not isinstance(saved, dict):
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
        if not self.taken_over:
            return self._write(self.path, self.d)
        # A takeover is put on disk in three writes, and until the third the file it took over can be spoken of
        # by no name (once the second is done, its hold is in the saved ledger and is spoken of as that row).
        #   1. the count's file says "saving". A brain that ends after this leaves the old file there: the
        #      next brain counts the save that was left (counted), and takes the file over under a new name.
        #      The other order, the world model first, would leave a saved takeover uncounted and its name free
        #      for the next file of the same bytes.
        #   2. the world model.
        #   3. the count is raised and "saving" is over. The count is read again for it: if anything counted
        #      since the first write (nothing can while this brain has its lock; a brain a script made has
        #      none), this save does not end on a number that was passed (review of ce1be6e9).
        # Before this version there were two writes: the count raised, then the world model. Between them the
        # file on disk and the raised count made the name of a takeover that did not exist yet; `brain stopped`
        # could write word of it down, and a later takeover of the same bytes had that name (review of
        # e4a267cd). A save that fails leaves this brain to do all three again.
        count = os.path.join(self.live, COUNT)
        self._write(count, {"count": takeovers(self.live), "saving": True})
        self._write(self.path, self.d)
        self._write(count, {"count": takeovers(self.live) + 1, "saving": False})
        self.taken_over = False

    @staticmethod
    def _write(path, obj):
        tmp = f"{path}.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf8") as f:
            json.dump(obj, f, separators=(",", ":"))
        os.replace(tmp, path)

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

    PROFILE_NUMBERS = ("curHealth", "maxHealth", "curChakra", "maxChakra", "curStamina", "maxStamina", "sector",
                       "longitude", "latitude", "curEnergy")

    @classmethod
    def _unfit(cls, new):
        """The first field of a profile read that is not of the kind every module takes it for, or None: the
        status is text, the battle id text or nothing, my health two numbers, every other pool and my position a
        number or nothing, pocket and bank an amount or nothing."""
        def number(v):
            return isinstance(v, (int, float)) and not isinstance(v, bool)

        def amount(v):
            try:
                return not isinstance(v, bool) and float(v) == float(v)
            except (TypeError, ValueError):
                return False
        if not isinstance(new["status"], str):
            return "status"
        if not (new.get("battleId") is None or isinstance(new["battleId"], str)):
            return "battleId"
        return next((k for k in cls.PROFILE_NUMBERS
                     if not (number(new.get(k)) or new.get(k) is None and k not in ("curHealth", "maxHealth"))),
                    next((k for k in ("money", "bank") if not (new.get(k) is None or amount(new[k]))), None))

    def _profile(self, r):
        new = {k.split(".", 1)[1]: v for k, v in r.data.items() if k.startswith("userData.")}
        if "status" not in new:
            return
        unfit = self._unfit(new)
        if unfit:                                   # the last good profile stands; nothing is built on this one
            self.event("finding", f"a profile read cannot be used ({unfit}): {json.dumps(new.get(unfit))[:80]}",
                       about="selects")
            return
        old = self.me
        # what was spent: a fall in pocket plus bank between two reads (measured, never estimated). The day is
        # the brain's own clock's: a result's time is the transcript's, and a wrong one would start the day anew.
        if old.get("money") is not None and new.get("money") is not None:
            before = float(old.get("money") or 0) + float(old.get("bank") or 0)
            after = float(new.get("money") or 0) + float(new.get("bank") or 0)
            spend = self.d["records"]["spend"]
            if spend.get("day") != utc_day(self.now):
                spend.update(day=utc_day(self.now), ryo=0.0)
            if after < before:
                spend["ryo"] = spend.get("ryo", 0.0) + (before - after)
        new["read_at"] = self.now
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
