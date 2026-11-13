"""What a batch leaves owing until it is over and has been read back (re-review of 87e497a6, H2 and H4).

Two things are kept by the batch that may change them. They are in the world model, so they are saved with the
batch and outlive a restart:

  records.spend.out   the ryo a batch's calls may cost      a profile read shows what was spent    (gates.py)
  inventory.stale     that a batch changes what I wear       a read of my items shows what is worn  (equipment.py)

A row is [the batch's id, what it owes (the ryo; nothing for the items)], with True behind them once the brain
knew, before the request at hand, that the batch is over. A batch is over when none of its calls is out or
loose in the call ledger (player/budget.py): its relay handed it in, it was never printed, or its replaced
relay came back or was confirmed stopped.

A read pays a row off only when it is known to have been made after the batch's calls:

  - the batch's own read, made behind its other calls and handed in with it; or
  - a read of a batch that was made after the brain knew the batch was over.

A read that is handed in together with the word that the batch is over was asked for before the brain knew, and
may have been made before the batch's calls. It pays nothing off, and the row waits for the next read. The
first cut dropped a row once its batch was over and any read had come: a replacement's earlier profile read was
taken for the measure of a replaced relay's purchases, and its earlier item read for the look at what that
relay's selection had equipped.
"""


OVER = [True]


def rows(kept):
    """The rows as this code keeps them, out of whatever a world model holds. The version before kept the ryo
    as these rows without the mark, and the items as True: neither says that its batch is over."""
    return [[None, None]] if kept is True else [list(r) for r in kept or []]


def open_batches(world):
    """The ids of the batches whose calls may still be made: the one that is out, and those that are loose."""
    calls = world["budget"].get("calls") or []
    out = {world["budget"].get("batch")} if any(c[2:3] == ["out"] for c in calls) else set()
    return out | {c[3] for c in calls if c[2:3] == ["loose"]}


def read(world, kept, own=True):
    """A read that can be used came in with the request at hand: the rows it does not pay off. own: it was made
    behind every other call of the batch it came with (the last batch made)."""
    last, still = world["budget"].get("batch"), open_batches(world)
    return [r for r in rows(kept) if not (r[2:] == OVER or (own and r[0] == last and last not in still))]


def settle(world, kept):
    """The request at hand has been taken in. From the next one on, a read pays off the rows whose batch is over
    now. -> the rows."""
    still = open_batches(world)
    return [r if r[0] in still else r[:2] + OVER for r in rows(kept)]
