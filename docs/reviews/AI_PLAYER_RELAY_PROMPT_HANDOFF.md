# AI player, the relay: the one-message rule, and a reader that counted calls twice. Handoff for review

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-14, after the third re-review approved
the hook relay at `51fac81d` and the proof of its hooks on Claude Code itself was run.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-relay
Base: 51fac81d712b65936dba14bf340ac957975da3e4 (approved: chatgpt/review-ai-player-hook-relay-rereview3 @ b8e9b027)
Code: 995625fe (the prompt), f4d042d0 (the reader)
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Authority: RUL-2026-11-14-160, point 2 (the prompt). The reader's fix is the implementer's, found by the proof.
Evidence: docs/reviews/evidence/ai_player_hook_relay/PROOF.md on fable/ai-player-hook-proof (its head is in
          the handoff message), "After the director's word"
```

The diff to review is `git diff 51fac81d HEAD`: two changes in two commits, each with its tests, and this
note. Nothing of the hooks' code (`player/hook.py`, `player/hooked.py`, `player/brain/`) is touched.

RUL-2026-11-14-160 is on `fable/ai-player-hook-proof` with RUL-158 and -159, not in this diff, so that this
diff is the two changes and nothing else.

## 1. The next `brain next` goes in the message of the batch's calls (995625fe)

**What the proof found.** The relay's prompt said "Do every line, in order, as tool calls in ONE message" and
that the last line is the next `brain next`. Under Claude Code 2.1.325, Haiku did that in 6 sessions of 26.
In the other 20 it sent the batch's calls, waited for their results, and then sent `brain next` in a message
of its own. Both are correct. The second is one more request a batch, which reads the whole conversation
again: 5,320 to 5,515 by the plan's count against 4,212 to 4,425.

**The director's word.** RUL-2026-11-14-160, point 2: the rule goes into the prompt before the live gate,
through review.

**What was changed.** One sentence of step 2 of `player/RELAY.md`, and of `.claude/agents/tnr-relay.md`, whose
body is that prompt (a test holds them equal):

```text
-   The last line is always the next `brain next`. Run it exactly as printed.
+   The last line is always the next `brain next`. Run it exactly as printed, in that same message: never wait
+   for the results of the calls first.
```

- It is in the step, not a line under Rules, so that the section on a batch with `put` lines, which follows
  and says "one line at a time, not in one message", reads as the exception.
- The prompt is 312 words. Its bound in `test_relay.py` and in `docs/design/AI_PLAYER_OVERHAUL.md` section 4.7
  was "under 300"; it is "under 320". Thirteen words for a fifth of a batch's cost.
- `test_the_next_brain_next_goes_in_the_message_of_the_batchs_calls` holds the sentence in the step, and that
  the `put` section still says what it said.

**Measured, with the files as committed** (against the stand-in connector; no request of the game):

| Relay | Sessions that wrote every batch in one message | A line copied wrong |
|---|---|---|
| With hooks, the session's main agent | 16 of 16 (runs 10a to 10f, 11a to 11j) | none |
| With hooks, a subagent | 7 of 7 (13a to 13c, 13e to 13h) | none |
| Printed `put` lines (no hooks, no transcript) | still one line at a time, call then `put`: 3 of 3 (10g to 10i), as before the change (9b to 9d) | |
| No hooks, results read in its transcript | the rule changed nothing: `brain next` in a message of its own in every batch but one, old wording and new (runs 12) | |

A batch of a relay with hooks, by the brain's token log: 3,890 to 4,100 as a main agent, 3,500 to 3,630 as a
subagent.

**Is `brain next` in the same message safe?** It is what the hooks were built for and what the first three
reviews judged: the hook before `brain next` closes the batch, and waits for every line that was taken. Under
this Claude Code the tool calls of one message are run one after another, so that hook has never anything to
wait for: `brain next` starts when the last call has its result.

## 2. Only the messages of a transcript are read (f4d042d0)

**What the proof found.** In a relay run without hooks, every batch had as many "calls the batch did not ask
for" as it had calls: seven findings in eight batches (run 9a), and the call budget charged for each. With a
debug file, Claude Code 2.1.325 keeps beside each message of a transcript a copy of what it sent the API, in
rows of type `api-request-blob`, tool calls and all, under the same ids. `relay._blocks` took the parts of any
row that had a `message`, so `_span` saw every call twice, matched the first to what the batch asked for, and
counted the second as a stray.

**What it did not touch.** A relay with hooks: its results come through its hooks, and its strays are not
counted (`read_batch(..., hooked=True)`). Its token figures were right: a copy has no `usage`. So nothing the
three reviews judged, and nothing the proof measured of a relay with hooks, rests on it.

**What was changed.** `relay._blocks` gives the parts of a row only when the row is a message of the
conversation: its `type` is `assistant` or `user`, or it has none (the suite's transcripts). One line, and its
comment. `player/relay.py` is still 400 lines.

`test_only_the_messages_of_a_transcript_are_read` writes a transcript as that Claude Code wrote it and asks
for the batch: on `51fac81d` it reports two strays, here none.

**Under Claude Code itself, after the fix:** no such finding in 13 sessions without hooks (11k, 12a to 12l).

**Why it is here and not left for later.** It is the fallback's reader, and the fallback is what a session
gets when its hooks do not run. I would not hand over a line with a known wrong count in it. It is a commit of
its own, so it can be judged, or left out, by itself.

## Verification on the code head (f4d042d0)

Run in this cloud session. Nothing here makes a request of the game.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 636 tests`, `OK`, three runs in a row, none skipped (`51fac81d`: 634) |
| `python3 -m unittest -v player.tests.test_hook_relay` | `Ran 86 tests`, `OK`, as before |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | 30 runs, each as before |
| `python3 -m player.tests.test_walk 200 300` | the output of `184ce648`, to the byte |
| Two fuzz scripts and three simulated fights of mine, not in the repository | the output of `184ce648`, to the byte |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py`, `git diff --check 51fac81d` | exit 0 each; 327 rulings on this branch |

### Planted defects

Seven, each in a throwaway worktree of this head, the whole suite run on each. Every one fails a test.

| Planted defect | Tests that fail |
|---|---|
| The rule is taken out of the prompt and the agent file | `test_the_next_brain_next_goes_in_the_message_of_the_batchs_calls` |
| The rule is in the prompt and not in the agent file | `test_the_relay_agent_is_that_prompt_with_two_tools_and_nothing_else` |
| The rule says "in that same message" and not that the results are not waited for | `test_the_next_brain_next_goes_in_the_message_of_the_batchs_calls` |
| The `put` section no longer says "not in one message" | the same |
| The reader takes a tool call from any row again | `test_only_the_messages_of_a_transcript_are_read` |
| The reader takes the model's rows and not the results' | the same |
| The reader drops a row that has no type | 17 tests |

## Size

The player's code is 6,351 lines in 32 files, as at `51fac81d`: `player/relay.py` is 400 lines, the same two
files are over 400, the same 17 functions over 12 branches. The tests are 11,899 lines (`51fac81d`: 11,857).

## What the proof found that is not changed here

They are in `PROOF.md`; none is in this diff.

- **A relay without hooks is not reliable on this Claude Code.** It stopped itself in 7 sessions of 17, with
  the old wording and the new alike: it made one call of a batch of five and went on, or it read the calls it
  was carrying and refused one. No relay with hooks stopped itself in 58. The brain still falls back to it
  when no hook runs. Whether it should refuse to instead is a decision, not a correction, and it is put to the
  director.
- **`omitClaudeMd: true` is honoured for a subagent and not for a main agent.** A main-agent relay has
  `CLAUDE.md` in front of it and is born with 7,900 tokens; a subagent with 4,090.
- **The `put` fallback's command is not passed by a permission rule**; Claude Code asks each time.
- **A hook that dies with a line in its hand costs a two-minute wait**, as built.

## Known limits

Those of the third correction's note stand. The measurements are against the stand-in's game, which does not
fight: batches of one to five reads and moves.

## Live-game statement

Zero live requests. The one live request of this line is the probe's read, before the first handoff. No
gameplay action, no write, no credential.

## Open

For the director, in the handoff message: how the live relay is started (a subagent is the cheaper one, and
the one that reads nothing but its prompt); and whether the brain should refuse to play through a relay
without hooks.

## Not begun

AP1's live gate (the director's to start, after this review and the check on the operator's machine); AP2's
second part; the script that starts a relay; replacing a relay inside a fight; a ledger that ends a replaced
relay's batch by the record alone.
