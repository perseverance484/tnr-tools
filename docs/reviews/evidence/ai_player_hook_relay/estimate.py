"""What a relay with hooks would have cost on the live session of 2026-11-11, by the plan's count.

    git show origin/duet/ai-player-ap1-live:state/player/dauntless/sessions/ap1_live/tokens.jsonl \\
        | python3 docs/reviews/evidence/ai_player_hook_relay/estimate.py

The same stretch and the same count as the estimate for the light reads (fable/ai-player-light-polls,
docs/reviews/evidence/ai_player_light_polls/tokens_recomputed.py): the first relay's 27 batches, the walk to the
fight and its rounds 1 to 5; and per request, in fresh input tokens of Claude Haiku 5.5,

    rate x (0.1 x what was in the conversation before + 1.25 x what was added since + 5 x its output),

rate 5 for a request whose prompt is over 100,000 tokens, else 1 (RUL-2026-11-13-156: the API's price ratios,
in place of the plan's weights, which are not published).

As it ran: each batch as the log has it. Three relays: the one the session had (born with 118,190 tokens, kept
for the stretch); one born with 5,000 and kept; one born with 5,000 and replaced past 60,000, which the code
does not do inside a fight.

With hooks: the model's conversation holds a stand-in for each call and "ok" for each result. What a batch
adds, and what it takes in output, no longer depends on what is read. Both are put together from the probe
(PROBE.md), which measured single requests, not a relay's batch:

    CALL_ADD   270   added by one stand-in call and its "ok" (269 and 166 were written by the two requests
                     that followed one)
    LINE_ADD    30   one stand-in line of the next batch, as `brain next` prints it (not measured)
    NEXT_ADD   100   the `brain next` call and its last line (not measured)
    CALL_OUT   100   output for one stand-in call (97 measured)
    NEXT_OUT    60   output for the `brain next` call (not measured)
    THINK      150   thinking, once a batch (requests with thinking took 236 and 248 in all)

The log of that session does not say how many calls a batch had. A batch that watched his turn is taken to have
2 (the fight and its log), one with my actions 4, any other 3.

It is an estimate. The token log now keeps what was read from the cache and what was written to it apart, and
says which batches a relay with hooks carried: the first session gives the figure itself.
"""
import json
import sys

READ, WRITE, OUTPUT, STEP_AT, STEP = 0.1, 1.25, 5, 100_000, 5
CALL_ADD, LINE_ADD, NEXT_ADD, CALL_OUT, NEXT_OUT, THINK = 270, 30, 100, 100, 60, 150
ROWS = [json.loads(line) for line in sys.stdin if line.strip()][:27]
GROW = [b["context"] - a["context"] for a, b in zip(ROWS, ROWS[1:])] + [15000]


def calls(row):
    return 2 if "his turn" in row["note"] else 4 if "MY TURN" in row["note"] else 3


def run(birth, hooks, replace_past=None):
    """-> (the plan's count, the raw count, requests over the step, the context at the end)."""
    ctx, new, plan, raw, over = birth, 0, 0.0, 0, 0
    for i, row in enumerate(ROWS):
        if replace_past and ctx > replace_past:
            ctx, new = birth, 0
        n = calls(row)
        add = n * (CALL_ADD + LINE_ADD) + NEXT_ADD if hooks else GROW[i]
        out = n * CALL_OUT + NEXT_OUT + THINK if hooks else row["out"]
        rate = STEP if ctx > STEP_AT else 1
        plan += rate * (READ * (ctx - new) + WRITE * new + OUTPUT * out)
        raw, over = raw + ctx, over + (rate > 1)
        ctx, new = ctx + add, add
    return plan, raw, over, ctx


print("| Relay | Born with | The plan's count | a batch | against the session | Requests over 100,000 | "
      "Context at the end |\n|---|---|---|---|---|---|---|")
base = None
for name, birth, hooks, past in (("as it ran, the session's relay", ROWS[0]["context"], False, None),
                                 ("as it ran, a small relay kept for the stretch", 5000, False, None),
                                 ("as it ran, a small relay replaced past 60,000", 5000, False, 60000),
                                 ("with hooks, a small relay kept for the stretch", 5000, True, None)):
    plan, raw, over, end = run(birth, hooks, past)
    base = base or plan
    print(f"| {name} | {birth:,} | {plan / 1e6:.2f}M | {plan / len(ROWS) / 1e3:.1f}k | "
          f"{'' if plan == base else f'{100 * plan / base - 100:+.0f}%'} | {over} of {len(ROWS)} | {end:,} |")
