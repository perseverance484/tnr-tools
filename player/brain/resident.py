"""The resident side: the one-brain lock, and how a request file is answered with a batch file, by the resident
process (`brain run`) or by a `brain next` that finds nobody home.

Five names are called through the package (B.Brain, B.serve, B.answer, B._lock, B._await), here and in client.py:
that is where they were before the split, and where the tests take the pieces apart.
"""
import contextlib
import fcntl
import os
import time
import weakref

from .. import brain as B
from .. import config as C
from .. import relay
from ..world import World, counted
from .core import _crashed, _wire

# ---------------------------------------------------------------- the resident process and its client
_HELD = {}
"""The brain's locks this process has: {live folder: the open file}. A lock is over when its file is closed."""


def _lock(live, wait=False):
    """The one-brain lock: whoever holds it owns the world model. Returns the open file, or None."""
    os.makedirs(live, exist_ok=True)
    f = open(os.path.join(live, "brain.lock"), "w")  # noqa: SIM115 (held for the life of the holder)
    try:
        fcntl.flock(f, fcntl.LOCK_EX | (0 if wait else fcntl.LOCK_NB))
    except OSError:
        f.close()
        return None
    _HELD[os.path.realpath(live)] = weakref.ref(f)
    return f


def _home(live):
    """Does this process have the brain's lock of this live folder?"""
    f = _HELD.get(os.path.realpath(live), lambda: None)()
    return f is not None and not f.closed


def _left_save(live):
    """A save of a takeover that a brain began and left is counted (world.counted) before the brain that starts
    looks at what is on disk, and only under the brain's lock: the lock this process has already (the resident;
    a `brain next` that answers for itself), or the lock taken here for the moment when nobody has it (a brain
    made without one). When another process has the lock, a brain is home: the save is that brain's to finish,
    and nothing is counted (review of ce1be6e9)."""
    if _home(live):
        return counted(live, World._write)
    lock = B._lock(live)
    if lock is not None:
        try:
            counted(live, World._write)
        finally:
            lock.close()


def _after_crash(brain):
    """What a relay is told when the tick crashed: come back in a moment (sooner in a fight)."""
    return {"steps": [], "hold": 1.0 if brain.world.in_battle() else 3.0, "stop": None}


def _answered(brain, req):
    """The answer this very request already had, when it is made again: its `brain next` died before it had
    the answer down, and the results it carries are in the world model already (review of c0006266, finding 3:
    they were applied a second time). False for a request older than the last one answered for the same relay:
    it is dropped. None for a request that is new.

    A receipt that a brain of another protocol left answers the request too, but not with that brain's batch:
    what the request brings is in the world model already and is not taken in twice, and a batch made under
    that brain's rules is not this one's to give. The relay is told to come back in a moment."""
    done = brain.world["relay"].get("answered") or {}
    if req.get("relay") is None or req["relay"] != done.get("relay") or not isinstance(done.get("seq"), int):
        return None
    if req["seq"] < done["seq"]:
        brain.world.event("finding", f"request {req['seq']} came after request {done['seq']} of the same relay "
                                     f"was answered; it is dropped", about="relay")
        return False
    if req["seq"] > done["seq"]:
        return None
    ours = relay.ours(done) and done["batch"]
    batch = dict(ours or _after_crash(brain), id=done.get("id"))            # the batch it made then, not a new one
    batch["hold"] = round(max(0.0, batch["hold"] - (brain.world.now - done["at"])), 1)   # what is left of the wait
    return batch


REQUEST = ("protocol", "seq", "id", "relay", "held", "gone", "ended", "unprinted")
"""What every request of this version's `brain next` carries: the protocol's number, the request's number and id,
its relay, and what that relay knows of who has which batch."""


def serve(brain, live, path):
    """A request file as a running player meets it: the resident brain looking through live/inbox, or `brain
    next` answering for itself. Only a request this version's `brain next` wrote is answered: one under this
    protocol's name, with its number, and with everything such a request carries. Any other file there was left
    by an older version (or is no request at all): it is removed unanswered, and that is said. Its `brain next`
    is long gone, and what it does not say must not be read as if it had said it (review of 426a9fba, finding
    1: a request from before, with no word of who held the last batch, was answered by a brain that came home,
    and that batch was taken to be back)."""
    req = relay.read(path)
    if relay.is_request(path) and relay.ours(req) and all(k in req for k in REQUEST):
        return B.answer(brain, live, path)
    with contextlib.suppress(OSError):
        os.unlink(path)
    brain.world.event("finding", f"{os.path.basename(path)} is not a request of this version's `brain next`: "
                                 f"it is removed and not answered", about="relay")


def answer(brain, live, path):
    """Answer one request file with a batch file: the one with the request's own number and id, so an answer
    never reaches a `brain next` that asked something else. A tick that crashes still answers: the relay is told
    to come back in a moment (sooner in a fight), and the crash is written down for Duet (live/crash.log and an
    error event). The brain has undone what that tick decided, and saved the rest.

    This takes any request: a test may drive the brain with a bare one. A running player comes through
    `serve`, which lets through only what its own `brain next` wrote."""
    req = relay.read(path)
    if req is not None:
        out = _answered(brain, req)
        if out is not None and req.get("ended"):                   # nothing is run again, but word that a held
            brain.evidence(req)                                    # batch is over is never dropped unread
            brain._save()
        if out is None:
            try:
                out = dict(_wire(brain.handle(relay.unpack(req.get("results")), req.get("usage"),
                                              req.get("strays", 0), ask=req)), id=req.get("id"))
            except Exception:  # noqa: BLE001  (a relay left without a batch loses turns; a logged crash does not)
                out = _after_crash(brain)
                _crashed(brain, live)
        if out:
            relay.write(relay.batch_path(live, req["seq"], req.get("id")),
                        dict(out, protocol=relay.PROTOCOL, seq=req["seq"], relay=req.get("relay"),
                             request=req.get("id")))
    with contextlib.suppress(OSError):          # only the file that was read: never a newer request
        os.unlink(path)


def run(live=None, forever=True):
    """The resident process. Exits at once when another brain already holds the lock."""
    live = live or C.live_dir()
    lock = B._lock(live)
    if lock is None:
        return 1
    brain = B.Brain(live)
    while True:
        for path in relay.pending_requests(live):
            B.serve(brain, live, path)
        brain.watchdog()
        if not forever:
            return 0
        time.sleep(C.BRAIN_WAIT)
