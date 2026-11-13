"""What light reads on his turn would have cost in the live session of 2026-11-11, by that session's own figures.

    git show origin/duet/ai-player-ap1-live:state/player/dauntless/sessions/ap1_live/tokens.jsonl \\
        | python3 docs/reviews/evidence/ai_player_light_polls/tokens_recomputed.py

The file has one row per batch: the relay's context when the batch was asked for, the output tokens the batch
took, and its note. Each batch is one model request, and a request carries the relay's whole conversation.

Only the first relay's 27 batches are used: the walk to the fight and its rounds 1 to 5. After them the session
is its defects (reads that came back empty, the fight closed and opened again three times, full reads refused),
and says nothing about a fight that is read as intended.

What is counted (director 2026-11-13, RUL-2026-11-13-156: the cost is usage against the plan's limits). The
plan counts what is read again from the prompt cache at the cached rate, and less than new content (Anthropic:
code.claude.com/docs/en/costs, "Why usage climbs in a long session"; support.claude.com, "Usage limit best
practices"). Its weights are not published. The API's prices are used here, as the first of those pages points
to them. For Claude Haiku 5.5, per token and relative to fresh input:

    read from the cache               0.1
    written to the 5-minute cache     1.25    (a relay is a subagent: its cache lives five minutes)
    output                            5
    all of it times 5                 for a request whose prompt is over 100,000 tokens

So a request costs rate x (0.1 x what was in the conversation before + 1.25 x what was added since the request
before + 5 x its output). The first request of a relay is taken to read what the relay is born with from the
cache; that flatters a large relay and hardly touches a small one.

The raw count is every token of every request, added up alike. The token log keeps that sum, and the live
handoff's table and this change's first estimate were made in it.

The model. What a batch adds to the context is the growth to the next batch, as measured. Then:
  as it ran      every batch as it was: a full read behind my actions and with every poll of his turn.
  built          a batch that watched his turn adds LIGHT. The last one of a round, which showed my turn, is
                 followed by one more batch, my turn's full read: it adds what that poll added as it ran.
  one full read  the same, and the read behind my actions is a light one too (the proposal of the live handoff,
                 before RUL-2026-11-13-155 kept the state his turn starts on).
LIGHT, 2,000 tokens, is a guess: in the same session a batch with a plain read and eight log lines added about
2,600, and a batch with no read about 1,200. ACTS, 3,000, is a batch with my actions and a light read. A batch
keeps the output it had; the batch that is added takes OUT, 500, which is what the session's smallest took.

The relay. In a fight the code does not replace a relay (player/relay.py, should_rotate), so "one for the
stretch" is what would happen. The others are what replacing it in a fight would
give: past 60,000 tokens, or at the start of every round. It is born with what the session's relay had, or
with 5,000 (a relay with its own short prompt and two tools: .claude/agents/tnr-relay.md, not yet tried).

It is an estimate from one stretch of one fight against one opponent, on a relay that took 7 to 13 s a batch.
"""
import json
import sys

LIGHT, ACTS, OUT = 2000, 3000, 500
READ, WRITE, OUTPUT, STEP_AT, STEP = 0.1, 1.25, 5, 100_000, 5
ROWS = [json.loads(line) for line in sys.stdin if line.strip()][:27]
GROW = [b["context"] - a["context"] for a, b in zip(ROWS, ROWS[1:])] + [15000]


def kind(row):
    return "his" if "his turn" in row["note"] else "my" if "MY TURN" in row["note"] else "-"


def steps(i, scheme):
    """The batches that row i becomes: [(what it adds to the context, its output, has it a full read)]."""
    row, k = ROWS[i], kind(ROWS[i])
    if scheme == "as it ran" or k == "-" or (k == "my" and scheme == "built"):
        return [(GROW[i], row["out"], k != "-")]
    if k == "my":
        return [(ACTS, row["out"], False)]
    if i + 1 < len(ROWS) and kind(ROWS[i + 1]) == "my":           # the poll that showed my turn
        return [(LIGHT, OUT, False), (GROW[i], row["out"], True)]
    return [(LIGHT, row["out"], False)]


def run(birth, scheme, relay):
    """-> the plan's count, the raw count, batches, requests over the step, full reads, light reads."""
    ctx, new, rnd = birth, 0, None                                # new: what the next request adds to the cache
    plan, raw, batches, over, fulls, lights = 0.0, 0, 0, 0, 0, 0
    for i, row in enumerate(ROWS):
        if relay == "a fresh one every round" and row["round"] is not None and row["round"] != rnd:
            ctx, new, rnd = birth, 0, row["round"]
        for add, out, full in steps(i, scheme):
            if relay == "replaced past 60,000" and ctx > 60000:
                ctx, new = birth, 0
            rate = STEP if ctx > STEP_AT else 1
            plan += rate * (READ * (ctx - new) + WRITE * new + OUTPUT * out)
            raw, batches, over = raw + ctx, batches + 1, over + (rate > 1)
            fulls, lights = fulls + full, lights + (not full and kind(row) != "-")
            ctx, new = ctx + add, add
    return plan, raw, batches, over, fulls, lights


def pct(value, base):
    return "" if value == base else f"{100 * value / base - 100:+.0f}%"


print("| Relay | Born with | Reads | The plan's count | | Raw count | | Batches | of them over 100,000 | "
      "Full reads | Light reads |\n|---|---|---|---|---|---|---|---|---|---|---|")
for relay, birth in (("one for the stretch", ROWS[0]["context"]), ("one for the stretch", 5000),
                     ("replaced past 60,000", 5000), ("a fresh one every round", ROWS[0]["context"]),
                     ("a fresh one every round", 5000)):
    base = None
    for scheme in ("as it ran", "built", "one full read"):
        plan, raw, batches, over, fulls, lights = run(birth, scheme, relay)
        base = base or (plan, raw)
        print(f"| {relay} | {birth:,} | {scheme} | {plan / 1e6:.2f}M | {pct(plan, base[0])} | {raw / 1e6:.2f}M | "
              f"{pct(raw, base[1])} | {batches} | {over} | {fulls} | {lights} |")
