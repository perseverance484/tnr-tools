"""A scenario estimate: what relays of four kinds would have cost on the live session of 2026-11-11, by the
plan's count. It is not a measurement of any of them but the first, and of that one only in part (below).

    git show origin/duet/ai-player-ap1-live:state/player/dauntless/sessions/ap1_live/tokens.jsonl \\
        | python3 docs/reviews/evidence/ai_player_hook_relay/estimate.py

The same stretch and the same count as the estimate for the light reads (fable/ai-player-light-polls,
docs/reviews/evidence/ai_player_light_polls/tokens_recomputed.py): the first relay's 27 batches, the walk to the
fight and its rounds 1 to 5; and per request, in fresh input tokens of Claude Haiku 5.5,

    rate x (0.1 x what was in the conversation before + 1.25 x what was added since + 5 x its output),

rate 5 for a request whose prompt is over 100,000 tokens, else 1 (RUL-2026-11-13-156: the API's price ratios,
in place of the plan's weights, which are not published).

What the log of that session has, and what is put in its place where it has nothing:

- A row is a batch, not a request. Its `context` is the prompt of the batch's last request, and its `in` the
  prompt tokens of all its requests. For 25 of the 27 batches the two are the same: one request. The first
  two took two requests each (`in` 233,342 and 237,730 against `context` 118,190 and 119,141). A batch's
  requests beyond the first are counted here as one more read of the conversation each (review of 184ce648:
  the first version counted every batch as one request, and left those 233,741 prompt tokens out). Every
  scenario is given the same number of requests for a batch as the session took.
- The log does not say what of a prompt was read from the cache and what was written to it. What a batch
  added to the conversation is counted as written, the rest as read.
- A relay's first request: "warm" counts the conversation it is born with as read from the cache (another
  relay of the same kind wrote it within five minutes), "cold" as written to it. The session's own relay was
  a general-purpose subagent; which it was is not in the log. Both are printed.
- "Batches over 100,000" are batches whose requests are counted at rate 5, not a count of requests.

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

No relay with hooks has carried a batch. The token log now keeps what was read from the cache and what was
written to it apart, and says which batches a relay with hooks carried: the first session gives the figure.
"""
import json
import sys

READ, WRITE, OUTPUT, STEP_AT, STEP = 0.1, 1.25, 5, 100_000, 5
CALL_ADD, LINE_ADD, NEXT_ADD, CALL_OUT, NEXT_OUT, THINK = 270, 30, 100, 100, 60, 150
ROWS = [json.loads(line) for line in sys.stdin if line.strip()][:27]
GROW = [b["context"] - a["context"] for a, b in zip(ROWS, ROWS[1:])] + [15000]


def calls(row):
    return 2 if "his turn" in row["note"] else 4 if "MY TURN" in row["note"] else 3


def run(birth, hooks, replace_past=None, cold=False):
    """-> (the plan's count, the batches counted at the higher rate, the context at the end)."""
    ctx, new, plan, over = birth, birth if cold else 0, 0.0, 0
    for i, row in enumerate(ROWS):
        if replace_past and ctx > replace_past:
            ctx, new = birth, birth if cold else 0
        n = calls(row)
        add = n * (CALL_ADD + LINE_ADD) + NEXT_ADD if hooks else GROW[i]
        out = n * CALL_OUT + NEXT_OUT + THINK if hooks else row["out"]
        again = max(1, round(row["in"] / row["context"])) - 1       # the batch's requests beyond the first
        rate = STEP if ctx > STEP_AT else 1
        plan += rate * (READ * (ctx - new) + WRITE * new + OUTPUT * out + again * READ * ctx)
        over += rate > 1
        ctx, new = ctx + add, add
    return plan, over, ctx


print("| Relay (a scenario, not a measurement) | Born with | The plan's count, born warm | born cold | "
      "against the session, warm | Batches over 100,000 | Context at the end |\n|---|---|---|---|---|---|---|")
base = None
for name, birth, hooks, past in (("as it ran, the session's relay", ROWS[0]["context"], False, None),
                                 ("as it ran, a small relay kept for the stretch", 5000, False, None),
                                 ("as it ran, a small relay replaced past 60,000", 5000, False, 60000),
                                 ("with hooks, a small relay kept for the stretch", 5000, True, None)):
    plan, over, end = run(birth, hooks, past)
    cold = run(birth, hooks, past, cold=True)[0]
    base = base or plan
    print(f"| {name} | {birth:,} | {plan / 1e6:.2f}M | {cold / 1e6:.2f}M | "
          f"{'' if plan == base else f'{100 * plan / base - 100:+.0f}%'} | {over} of {len(ROWS)} | {end:,} |")
