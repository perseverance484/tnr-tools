"""The brain: one resident process that makes every decision (design 4.1).

    python3 -m player.brain run            the resident process: answers requests, watches for a silent relay
    python3 -m player.brain next [TOKEN]   what a relay runs: hand in batch TOKEN's results, print the next batch
    python3 -m player.brain put TOKEN N    a relay whose transcript cannot be read hands in call N's result (stdin)
    python3 -m player.brain set KEY=JSON   change a setting (writes live/control.json; Duet does the same)
    python3 -m player.brain stopped TOKEN  the operator's word that a replaced relay has been stopped (or: all)
    python3 -m player.brain status         print live/status.json

One tick (Brain.handle): apply the director's settings, fold the results into the world model, let each activity
read what it understands, pick the activity with the highest priority class and score (the arbiter, design 4.4),
check its calls at the gates, pace them under the call budget, and write the batch, the status file and the world
model. The relay copies the batch to the game and comes back with `brain next`.

`brain next` starts the resident process when none is running, and answers the request itself if it has to: a relay
is never left without a batch. Every wait is spent here, in the brain, where it costs the relay nothing.

A tick that fails after the results are folded in is undone as a whole: what it learned stays, what it decided
does not, so a plan that never reached the relay is never remembered as sent. A fight's tick that fails twice
running still sends what the turn is owed (Battle.last_resort): no turn is lost to a crash.

Every request a relay's `brain next` makes carries the relay's name, the request's number and an id of its own.
The answer is kept in the world model, saved in the same write as everything the request changed, before the
request is answered: so also when the tick failed. The same request made again (its `brain next` died before it
had the answer down) gets that answer again, and nothing is applied a second time.

Who has which batch is kept by `brain next` (live/client.json), from what it printed and to whom, never from
what a relay says of itself. A batch is the request's id; it is held by the relay it was printed to until that
relay hands it in. A relay that is replaced while it holds one leaves it loose in the call ledger
(player/budget.py), until it comes back with that batch's token or the operator says it has been stopped.

What the two sides keep for each other (the client's file, a request, an answer, a batch that waits to be
printed, the receipt) carries the protocol number of the code that made it (relay.PROTOCOL). One that does not
carry this version's number is not used: an older version's file names no relay and no batch, an older brain's
answer or receipt gives no batch. The calls behind them stay in the ledger, held. A request is also put under
a name that carries the number (relay.request_path): a brain from before an update that is still running looks
for another name, takes nothing of this version's, and so changes nothing in the ledger because of it.

Where it is (the one file this was is now a package; `python3 -m player.brain` and every name are as before):
  core.py       the Brain: one tick, and what is kept of it
  resident.py   the lock; a request file answered with a batch file; the resident loop
  client.py     `brain next`, `brain put`, `brain stopped`; live/client.json
"""
import contextlib  # noqa: F401  (this and the names below: everything the module had before it was split,
import fcntl       # noqa: F401   so that whatever reaches into player.brain finds what it found there)
import glob        # noqa: F401
import json
import os
import subprocess  # noqa: F401
import sys
import time        # noqa: F401
import traceback   # noqa: F401

from .. import config as C
from .. import console, registry, relay  # noqa: F401
from ..budget import UPDATE, Budget  # noqa: F401
from ..combat import Combat  # noqa: F401
from ..gates import Gates  # noqa: F401
from ..registry import CLASSES  # noqa: F401
from ..world import RATE_LIMITED, World, counted, found, print_of, seen  # noqa: F401
from .core import BLOCK_FOR, IDLE_HOLD, QUIET, Brain, _crashed, _lead, _wire  # noqa: F401
from .resident import REQUEST, _after_crash, _answered, _lock, answer, run, serve  # noqa: F401
from .client import (LOOKS, RETRY_IN, SAVING, SUPERSEDED, _a_batch, _a_relay, _a_waiting_batch,  # noqa: F401
                     _a_word, _await, _client, _collect, _exchange, _greet, _held, _ledger_in, _named, _on_disk,
                     _owed, _sweep, _taken, _transcript, _who, next_batch, put, stopped)

B = sys.modules[__name__]  # the package as its own files call it: a function's source, run here again, finds it


def _setting(arg):
    """KEY=VALUE from the command line: the value is JSON when it parses (true, 3, {"harvest": false}), else text."""
    key, value = arg.split("=", 1)
    try:
        return key, json.loads(value)
    except ValueError:
        return key, value


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    live = C.live_dir()
    cmd = argv[0] if argv else "status"
    if cmd == "run":
        return run(live)
    if cmd == "next":
        return next_batch(live, argv[1] if len(argv) > 1 else None)
    if cmd == "put" and len(argv) == 3:
        return put(live, argv[1], argv[2], sys.stdin.read())
    if cmd == "stopped":
        return stopped(live, argv[1:], sys.stdout)
    if cmd == "set":
        print(json.dumps(console.set_control(live, **dict(_setting(a) for a in argv[1:]))))
        return 0
    if cmd == "status":
        print(json.dumps(relay.read(os.path.join(live, "status.json")), indent=1))
        return 0
    sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
    return 2
