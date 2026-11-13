"""The relay's side: `brain next`, `brain put` and `brain stopped`. What a relay hands in, the request it makes
of the brain, the batch it is owed, and who holds which batch (live/client.json).
"""
import contextlib
import fcntl
import glob
import json
import os
import subprocess
import sys
import time

from .. import brain as B
from .. import config as C
from .. import relay
from ..budget import UPDATE
from ..world import World, counted, print_of, seen

def _transcript(state, sleep):
    """The transcript that carries this batch's token, or None. A new relay's, and one that was readable for the
    relay's last batch, is given a moment for its newest line to be written."""
    token, hint = state["token"], state.get("transcript")
    path, tries = relay.find_transcript(token, hint), 4 if hint or state.get("new") else 0
    while not path and tries:
        sleep(0.25)
        path, tries = relay.find_transcript(token, hint), tries - 1
    return path


def _collect(live, state, sleep=time.sleep):
    """The results of the batch this relay was last given: from its own transcript when one carries the batch's
    token, else the ones it handed in with `brain put` for that token. Returns (results, usage, strays, the
    transcript's path or None). Nothing of this batch is removed here: a `brain next` that dies before the
    brain has answered leaves the results where the next one finds them."""
    token, expected = state["token"], [tuple(c) for c in state.get("calls") or []]
    path = _transcript(state, sleep)
    results, usage, strays = [], {}, 0
    if path:
        try:
            results, usage, strays = relay.read_batch(path, token, expected)
        except OSError:
            path = None
    inbox = os.path.join(live, "inbox")
    for name in sorted(f for f in os.listdir(inbox) if f.startswith("put-")):
        if not name.startswith(f"put-{token}-"):
            os.unlink(os.path.join(inbox, name))                   # a result for any other batch is dropped
            continue
        row = relay.read(os.path.join(inbox, name))                # this batch's stay until the brain has them
        if row and not path:
            results.append(relay.unpack([row])[0])
    return results, usage, strays, path


def _taken(live, token):
    """The brain has this batch's results: the ones handed in with `brain put` can go."""
    for path in glob.glob(os.path.join(live, "inbox", f"put-{token}-*.json")):
        with contextlib.suppress(OSError):
            os.unlink(path)


@contextlib.contextmanager
def _client(live):
    """The lock on live/client.json: who the relay is, and the batch it is owed. One `brain next` at a time reads
    it, talks to the brain and writes it back, so a relay that takes over and one that is still waiting cannot
    each write over the other (AP1 re-review, finding 3)."""
    with open(os.path.join(live, "client.lock"), "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


SUPERSEDED = "STOP superseded: another relay has taken over"
RETRY_IN = 5.0            # s before a relay asks again when the brain gave no answer


def _who(client):
    """client.json as this code may use it. A file that does not carry this version's protocol number is read
    as no file at all: no relay, no batch waiting, nothing held or gone. So an older version's file never has a
    batch printed that this version's brain did not pace (review of 60a28a84: an older waiting batch had every
    field of a current one, and was printed past the budget), and its relay is told to stop. Within a file of
    this protocol, what is not in the shape this code writes is dropped. Nothing dropped here is taken for its
    opposite: a batch that the file says nothing of is, to the brain, not on record, and is held."""
    state = relay.read(client)
    if not relay.ours(state):
        state = {}                                                 # another version's file: none of it is read
    state["protocol"] = relay.PROTOCOL
    if not _a_relay(state):
        for k in ("relay", "token", "seq"):                        # no relay is known by such a file: the next
            state.pop(k, None)                                     # `brain next` with no token starts one afresh
    state["calls"] = state["calls"] if isinstance(state.get("calls"), list) else []
    state["pending"] = state.get("pending") if _a_waiting_batch(state.get("pending")) else None
    state["held"] = state.get("held") if _a_batch(state.get("held")) else None
    state["gone"] = [g for g in state.get("gone") or [] if _a_batch(g)]
    state["ended"] = [e for e in state.get("ended") or [] if _a_word(e)]
    state["unprinted"] = [u for u in state.get("unprinted") or [] if isinstance(u, str)]
    return state


def _a_relay(state):
    """The relay that is running, as client.json names it: its name, its token, its last request's number."""
    return (isinstance(state.get("relay"), str) and isinstance(state.get("token"), str)
            and isinstance(state.get("seq"), int) and not isinstance(state.get("seq"), bool))


def _a_batch(g):
    """A printed batch, as client.json keeps it under held and gone: its relay's token and its id."""
    return isinstance(g, dict) and isinstance(g.get("token"), str) and isinstance(g.get("id"), str)


def _a_waiting_batch(p):
    """A batch this version's brain made that is waiting to be printed, as client.json keeps it under pending."""
    return (relay.ours(p) and isinstance(p.get("id"), str) and isinstance(p.get("seq"), int)
            and isinstance(p.get("steps"), list) and isinstance(p.get("ready_at"), (int, float)) and "stop" in p)


def _a_word(e):
    """Word that a batch is over, as client.json keeps it under ended: [the batch, when, whose, how]."""
    return (isinstance(e, list) and len(e) == 4 and isinstance(e[0], (str, int)) and not isinstance(e[0], bool)
            and isinstance(e[1], (int, float)) and e[3] in ("back", "stopped"))


def next_batch(live=None, token=None, out=sys.stdout, sleep=time.sleep):
    """`brain next [token]`: hand in the results, wait for the batch (answering it here if no brain is running),
    spend the brain-side wait, print the batch.

    Without a token the relay is new: it is given a name and one line to run, and nothing is taken from it yet.
    With the token of the batch it was last given, it hands that batch in. Any other token is a relay that has
    been replaced (it is told to stop) or a `brain next` run twice (it is given the current line again).

    A batch the brain has made is kept in client.json until a relay has it. The brain-side wait is spent with
    the lock released, so a replacement can take over meanwhile; whoever owns the relay when the wait is over
    gets the batch, and a relay that was replaced during it is told to stop and prints no call.

    client.json says who has what: held is the batch printed to the relay that is running, from the moment it
    is printed until the brain has taken its results; gone are the batches that were held by relays replaced
    since; ended is the evidence, not yet given to the brain, that one of those is over."""
    live = live or C.live_dir()
    os.makedirs(os.path.join(live, "inbox"), exist_ok=True)
    client = os.path.join(live, "client.json")
    with _client(live):
        state = _who(client)
        said = _greet(client, state, token)
        if said:
            out.write(said + "\n")
            return 0
        me, (pending, hold) = state["relay"], _exchange(live, client, state, sleep)
    if pending is None:                                            # the brain gave no answer: nothing has moved,
        sleep(hold)                                                # and the relay asks the same thing again
        out.write(relay.next_line(token) + "\n")
        return 0
    wait = hold if hold is not None else pending["ready_at"] - time.time()
    if wait > 0:
        sleep(wait)
    with _client(live):
        state = _who(client)
        if state.get("relay") != me:
            out.write(SUPERSEDED + "\n")                           # the batch stays for the relay that took over
        elif (state.get("pending") or {}).get("id") != pending["id"]:
            # the batch this call waited for is not the one that is owed any more: another call of this relay
            # has it, or it grew too old and the brain was asked afresh. Print nothing of it; come back.
            out.write(relay.next_line(state["token"]) + "\n")
        else:
            token = f"{me}-{pending['seq']}"
            calls = [[x["call"], x["input"]] for x in pending["steps"] if "call" in x]
            state.update(seq=pending["seq"], token=token, issued_at=time.time(), pending=None, calls=calls,
                         held={"token": token, "id": pending["id"]} if calls else None)   # printed: this relay's
            relay.write(client, state)
            out.write("\n".join(relay.lines(pending["steps"], pending["stop"], token,
                                            echo=not state.get("transcript"))) + "\n")
    return 0


def _greet(client, state, token):
    """What to say to a `brain next` that hands nothing in: a new relay gets its name and its first line, a
    replaced one is told to stop, a second call for the same batch gets the current line. None for a relay that
    is handing in the batch it was last given.

    A new relay replaces the one that was running. A batch that one still holds (it was printed to it, and the
    brain has not had its results) is gone with it. When a replaced relay comes back with the very token of a
    batch that is gone, that batch is over: that is noted (ended) for the brain. No other token proves anything:
    a relay that asked and was replaced before its batch was printed held nothing (review of 442a6311, finding
    2: such a relay's token carried the number of a batch another relay held, and released it)."""
    if token is None:
        gone = (state.get("gone") or []) + ([state["held"]] if state.get("held") else [])
        state = {"protocol": relay.PROTOCOL, "relay": os.urandom(3).hex(), "seq": state.get("seq", 0),
                 "calls": [], "transcript": None, "new": True, "pending": state.get("pending"), "held": None,
                 "gone": gone, "ended": state.get("ended") or [], "unprinted": state.get("unprinted") or []}
        state["token"] = f"{state['relay']}-{state['seq']}"
        relay.write(client, state)
        return relay.next_line(state["token"])
    if token != state.get("token"):
        if token.split("-")[0] == state.get("relay"):
            return relay.next_line(state["token"])
        was = next((g for g in state.get("gone") or [] if g["token"] == token), None)
        if was:
            state["gone"].remove(was)
            state["ended"] = (state.get("ended") or []) + [[was["id"], time.time(), token, "back"]]
            relay.write(client, state)
        return SUPERSEDED
    return None


def _exchange(live, client, state, sleep):
    """Hand this relay's results to the brain and get the next batch, unless a batch is already waiting for a
    relay. The batch is written into client.json before anything else happens to it. Returns (the batch, the
    brain-side wait still to spend, or None for one that was already waiting); or (None, a wait) when the brain
    gave no answer: then nothing is marked as handed in, and no evidence is dropped."""
    results, usage, strays, path = _collect(live, state, sleep)
    if state.get("handed") == state["token"]:                      # this batch's results have gone in already
        results, usage, strays = [], {}, 0
    pending, hold = _owed(state), None
    if pending is None:
        seq, rid = state["seq"] + 1, os.urandom(4).hex()
        _sweep(live)
        req = relay.request_path(live, seq, rid)
        ask = {"protocol": relay.PROTOCOL, "seq": seq, "id": rid, "relay": state["relay"],
               "results": relay.pack(results), "usage": usage, "strays": strays, "at": time.time(),
               "clock": "transcript" if path else "ours", "held": state.get("held"), "gone": state["gone"],
               "ended": state["ended"], "unprinted": state["unprinted"]}
        # On record before it is asked: whatever the brain makes of this request has not been printed. If this
        # `brain next` dies now, the next one can say so, and the brain need not hold that batch for anyone.
        state["unprinted"] = state["unprinted"] + [rid]
        relay.write(client, state)
        relay.write(req, ask)
        batch = B._await(live, seq, rid, req, sleep)
        if batch is None:
            return None, RETRY_IN
        hold = batch["hold"]
        pending = {"protocol": batch["protocol"], "id": batch.get("id") or rid, "seq": seq,
                   "steps": batch["steps"], "stop": batch["stop"], "ready_at": time.time() + hold}
        state.update(held=None, ended=[], unprinted=[])            # the brain has them, saved beside its answer
    state.update(pending=pending, transcript=path, new=False, handed=state["token"])
    relay.write(client, state)
    _taken(live, state["token"])                                   # and only now are they no longer needed here
    return pending, hold


def _sweep(live):
    """Called with the client's lock held, when no `brain next` is waiting on the brain: a request or a batch
    file that is there now was left by one that died, of this version or any other. Such a request is not
    answered late, and such a batch is never printed."""
    for path in glob.glob(os.path.join(live, "inbox", "*req-*.json")) + glob.glob(os.path.join(live, "outbox", "batch-*.json")):
        with contextlib.suppress(OSError):
            os.unlink(path)


def _owed(state):
    """A batch the brain made that no relay has had yet (its relay was replaced while it waited), unless it has
    waited too long to be worth sending: then the brain is asked afresh, under the next number. A batch is known
    by its own id, so a call that is still waiting on the old one cannot publish it in the new one's place
    (review of 0d10b7c6, finding 3)."""
    pending = state.get("pending")
    if pending and time.time() - pending["ready_at"] > C.STALE_OUTBOX:
        state["seq"] = max(state.get("seq", 0), pending["seq"])    # its number is not used again
        state["unprinted"] = state["unprinted"] + [pending["id"]]  # it was not printed, and now never will be
        state["pending"] = None
        return None
    return pending


def _await(live, seq, rid, req, sleep, limit=90.0):
    """The answer to this request, from a brain of this protocol: an answer that any other brain wrote is
    removed and not taken. When no brain holds the lock, this process answers and then starts one.

    A brain from before the update that is still running holds the lock and does not see the request (it is
    under this protocol's name). Then nothing is answered until that brain is ended; from that moment the lock
    is free and the request is answered here. When the request is gone and no answer has come (a brain dropped
    it), there is nothing to do but wait: that is waited out like any other wait, and a brain is started once."""
    t0, mine, started = time.time(), relay.batch_path(live, seq, rid), False
    while time.time() - t0 < limit:
        batch = relay.read(mine)
        if batch is not None:
            os.unlink(mine)
            if relay.ours(batch) and batch.get("request") == rid:
                return batch                                       # the answer to this very request
        lock = B._lock(live)
        if lock is not None:                                       # nobody is home: answer here, then start a brain
            try:
                asked = os.path.exists(req)
                if asked:
                    B.serve(B.Brain(live), live, req)
            finally:
                lock.close()
            if not started and os.environ.get("TNR_PLAYER_NO_DAEMON") != "1":
                subprocess.Popen([sys.executable, "-m", "player.brain", "run"], cwd=C.ROOT, start_new_session=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                started = True
            if asked:
                continue                                           # its answer is written: read it
        sleep(C.BRAIN_WAIT)
    return None


def stopped(live, names, out=sys.stdout):
    """`brain stopped TOKEN ...`, or `brain stopped all`: the operator's word that a relay which did not hand
    its batch in has been stopped and will make no call from now on. The brain was holding that batch against
    the minute; it now counts those calls from this moment, so they leave a minute from now.

    The word covers the batches that are held at the moment it is said, each by its id, and is kept that way:
    it is never read again as "whatever is held by then" (review of efa79808, finding 1). `all` is every held
    batch: those of the relays replaced so far, those the ledger holds for a relay that is not on record, and,
    after an update, the minute that is held for the relays from before it (Budget.taken_over).
    It is never the batch of the relay that is running, and never one that goes loose later. A batch can also
    be named by its id, as the listing shows it: an older version's batch has a number for one, and is named
    by that number (review of 426a9fba, finding 2: the number typed did not match the number kept). With no
    name: the batches that are held, and nothing is changed.

    Say it only of relays that are known to be stopped: this is the one statement the ledger takes on trust."""
    client = os.path.join(live, "client.json")
    with _client(live):
        state, now = _who(client), time.time()
        held = _held(live, state)
        said = {b: t for b, t in held.items()
                if b != SAVING and ("all" in names or t in names or str(b) in names)}
        if said:
            state["gone"] = [g for g in state["gone"] if g["id"] not in said]
            state["ended"] = state["ended"] + [[b, now, t, "stopped"] for b, t in said.items()]
            relay.write(client, state)
    known = {str(b) for b in held if b != SAVING} | {t for t in held.values() if t}
    out.write(json.dumps({"stopped": [_named(b, held) for b in said], "all": "all" in names,
                          "not_held": [n for n in names if n != "all" and n not in known],
                          "still_held": [_named(b, held) for b in held if b not in said]}) + "\n")
    return 0


SAVING = "a takeover that is being saved"       # in place of a name: no word is taken, the listing says ask again
LOOKS = (40, 0.05)        # how often `brain stopped` looks again while a takeover is being saved, and the s between


def _named(batch, held):
    """A held batch as the listing shows it."""
    if batch == SAVING:
        return "the relays from before the update (a brain is saving the takeover: say it again in a moment)"
    if str(batch).startswith(UPDATE):
        return f"the relays from before the update ({batch})"
    return held[batch] or f"batch {batch}"


def _held(live, state):
    """Every batch that is held now, by its id, with the token of the relay that has it (None when that is not
    on record): those the client's file says went with a replaced relay, and those the brain's saved ledger
    holds, whoever has them. Never the batch of the relay that is running: that one is out, not loose."""
    held = {g["id"]: g["token"] for g in state["gone"]}
    ledger, takeover = _on_disk(live, os.path.join(live, "world.json"))
    for c in (ledger if isinstance(ledger, dict) else {}).get("calls") or []:
        if c[2:3] == ["loose"] and len(c) > 3 and c[3] is not None:
            held.setdefault(c[3], c[5] if len(c) > 5 else None)
    if takeover:
        held.setdefault(takeover, None)
    return held


def _on_disk(live, path):
    """(the saved ledger, what the world model on disk is to the operator's word): None for a ledger of this
    version's or no file; the name of the hold for another version's ledger that no brain has saved yet (the
    brain that takes it over holds a minute's calls under this very id, so the word can name it now); or SAVING.

    SAVING: a brain has begun to save the takeover and has not finished (World.save). The count and the file
    do not belong together then, and no word is taken (review of e4a267cd: word said between the writes was
    kept under the name of a takeover that did not exist yet, and let a later one go). It is looked at again
    for a moment. If it stays so and nobody is home, the brain that began it is gone: its save is counted
    here, under the brain's lock, and the file has a new name. If a brain is home, it is that brain's to end."""
    for _ in range(LOOKS[0]):
        raw, written, count, saving = seen(path)
        ledger = _ledger_in(raw)
        if raw is None or relay.ours(ledger):
            return ledger, None
        if not saving:
            return ledger, UPDATE + print_of(raw, written, count)
        time.sleep(LOOKS[1])
    lock = B._lock(live)
    if lock is None:
        return ledger, SAVING
    try:
        counted(live, World._write)
    finally:
        lock.close()
    raw, written, count, _ = seen(path)
    return _ledger_in(raw), None if raw is None else UPDATE + print_of(raw, written, count)


def _ledger_in(raw):
    """The call ledger in a world model file's bytes, or None."""
    try:
        world = json.loads(raw)
    except (TypeError, ValueError):
        return None
    return world.get("budget") if isinstance(world, dict) else None


def put(live, token, index, text):
    """`brain put TOKEN N`, with the result on standard input: call N (from 1) of batch TOKEN, from a relay whose
    transcript cannot be read. A result for any batch but the one in progress is dropped."""
    state = _who(os.path.join(live, "client.json"))
    calls = state["calls"]
    if token != state.get("token") or not str(index).isdigit() or not 1 <= int(index) <= len(calls):
        return 1
    ep, inp = calls[int(index) - 1]
    relay.write(os.path.join(live, "inbox", f"put-{token}-{int(index):03d}.json"),
                list(relay.from_text(ep, inp, text.strip(), time.time())))
    return 0
