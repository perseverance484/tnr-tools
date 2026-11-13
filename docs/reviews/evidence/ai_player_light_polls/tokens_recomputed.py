"""What light reads on his turn would have cost in the live session of 2026-11-11, by that session's own figures.

    git show origin/duet/ai-player-ap1-live:state/player/dauntless/sessions/ap1_live/tokens.jsonl \\
        | python3 docs/reviews/evidence/ai_player_light_polls/tokens_recomputed.py

The file has one row per batch: the relay's context when the batch was asked for, and the batch's note. The
session's finding (docs/reviews/AI_PLAYER_AP1_LIVE_HANDOFF.md, "Tokens") is that a batch costs the relay's whole
context, since each batch is one model request and a request carries the conversation.

Only the first relay's 27 batches are used: the walk to the fight and its rounds 1 to 5. After them the session
is its defects (reads that came back empty, the fight closed and opened again three times, full reads refused),
and says nothing about a fight that is read as intended.

The model. What a batch adds to the context is the growth to the next batch, as measured. Then:
  as it ran      every batch as it was: a full read behind my actions and with every poll of his turn.
  built          a batch that watched his turn adds LIGHT. The last one of a round, which showed my turn, is
                 followed by one more batch, my turn's full read: it adds what that poll added as it ran.
  one full read  the same, and the read behind my actions is a light one too (the proposal of the live handoff,
                 before RUL-2026-11-13-155 kept the state his turn starts on).
LIGHT, 2,000 tokens, is a guess: in the same session a batch with a plain read and eight log lines added about
2,600, and a batch with no read about 1,200. ACTS, 3,000, is a batch with my actions and a light read.

The relay: one for the whole stretch, as it ran; one that is replaced when its context passes 60,000, which is
the design's rule (docs/design/AI_PLAYER_OVERHAUL.md, 4.7); or a fresh one at the start of every round. It is
born with what the session's relay had, or with 5,000 (a relay with its own short prompt and two tools).

Two ways of counting. The session's log adds up every token of every request alike: fresh input, what is
written to the prompt cache and what is read from it (player/relay.py, _usage). That is the first figure. The
second prices them as the API does: what a request adds to the conversation at 1.25 (a cache write), the rest
of it at 0.1 (a cache read). The log does not say how much of a request was read from the cache, so the second
figure assumes that all of the conversation so far was, a new relay's first request included.

It is an estimate from one stretch of one fight against one opponent, on a relay that took 7 to 13 s a batch.
"""
import json
import sys

LIGHT, ACTS = 2000, 3000
ROWS = [json.loads(line) for line in sys.stdin if line.strip()][:27]
GROW = [b["context"] - a["context"] for a, b in zip(ROWS, ROWS[1:])] + [15000]


def kind(row):
    return "his" if "his turn" in row["note"] else "my" if "MY TURN" in row["note"] else "-"


def run(birth, scheme, relay):
    """-> (tokens, the same priced as cache reads and writes, batches, full reads, light reads)."""
    ctx, total, priced, batches, fulls, lights, rnd = birth, 0, 0.0, 0, 0, 0, None
    for i, row in enumerate(ROWS):
        if relay == "a fresh one every round" and row["round"] is not None and row["round"] != rnd:
            ctx, rnd = birth, row["round"]
        k, last = kind(row), i + 1 < len(ROWS) and kind(ROWS[i + 1]) == "my"
        if scheme == "as it ran" or k == "-" or (k == "my" and scheme == "built"):
            steps = [(GROW[i], k != "-")]
        elif k == "my":
            steps = [(ACTS, False)]
        else:
            steps = [(LIGHT, False)] + ([(GROW[i], True)] if last else [])
        for add, full in steps:
            if relay == "replaced past 60,000" and ctx > 60000:
                ctx = birth
            total, batches, ctx = total + ctx, batches + 1, ctx + add
            priced += 0.1 * (ctx - add) + 1.25 * add
            fulls, lights = fulls + full, lights + (not full and k != "-")
    return total, priced, batches, fulls, lights


def pct(value, base):
    return "" if value == base else f"{100 * value / base - 100:+.0f}%"


print("| Relay | Born with | Reads | Tokens, each counted once a request | | Priced as cache reads and writes | | "
      "Batches | Full reads | Light reads |\n|---|---|---|---|---|---|---|---|---|---|")
for relay, birth in (("one for the stretch", ROWS[0]["context"]), ("one for the stretch", 5000),
                     ("replaced past 60,000", 5000), ("a fresh one every round", ROWS[0]["context"]),
                     ("a fresh one every round", 5000)):
    base = None
    for scheme in ("as it ran", "built", "one full read"):
        total, priced, batches, fulls, lights = run(birth, scheme, relay)
        base = base or (total, priced)
        print(f"| {relay} | {birth:,} | {scheme} | {total / 1e6:.2f}M | {pct(total, base[0])} | "
              f"{priced / 1e6:.2f}M | {pct(priced, base[1])} | {batches} | {fulls} | {lights} |")
