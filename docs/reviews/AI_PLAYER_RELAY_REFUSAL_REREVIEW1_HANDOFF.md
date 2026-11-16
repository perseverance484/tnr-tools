# AI player, the refusal of a relay without hooks: correction handoff, after the review of 9c2955ba

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-14, in answer to the review of
`9c2955ba` ("request changes": R1 and R2, both medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-relay-refusal
Reviewed: 9c2955bae4a1c681f7bf14de8f7ad57675cbf1d8
Review: docs/reviews/AI_PLAYER_RELAY_REFUSAL_REVIEW_20261114.md on
        chatgpt/review-ai-player-relay-refusal-20261114 @ 64f7d87a (evidence; not merged)
Base of this correction: 9c2955ba. Not rebased: this head is three commits on it.
Code: 6f8fa44d (R1, R2), fcb0929c (a test that raced)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Stands on: fable/ai-player-hook-proof @ 071ba1b1 (its re-review is separate, and still out)
Authority: RUL-2026-11-14-161
```

The diff to review is `git diff 9c2955ba HEAD`: one line of `player/brain/client.py`, a paragraph of
`player/hooked.py`'s text, six tests, the operator's guide, one test's last lines, and this note.

## Disposition

Both findings are **confirmed and corrected**. The first note's reason for leaving the protocol number alone
("asked where a batch is printed, every time") was not true of the code it described. It is now.

| | What the review found | Now |
|---|---|---|
| R1 | The director's word was looked for when `brain next` began and not again. Taken back while that `brain next` waited, the batch was printed all the same | It is asked for again where the batch is printed, after the wait. The relay is printed the STOP line and nothing else |
| R2 | The guide said the batch of a relay turned away after it was let in "is held until you say `stopped`". `stopped` does not take the batch of the relay on record | The guide has the order that works. `stopped` is as it was. A test runs the order, and the review's four commands before it |

## R1: what it was, and what was built

`next_batch` asks the brain, takes its answer, lets go of the client's lock, spends the wait in front of the
batch, takes the lock again, and prints. `hooked.bare` stood before all of that. Between the two the director
can say `relay_without_hooks=false`, or the file can go or be broken, and the batch was then printed to the
relay with its calls, marked as the one it holds.

The line that looks at who the relay is, after the wait, now asks for the word too:

```python
        if state.get("relay") != me or hooked.bare(live, state, token, hooks):   # (asked again: the wait is over)
            out.write((SUPERSEDED if state.get("relay") != me else hooked.BARE) + "\n")   # the batch stays
```

- **A relay that took over comes first**, as it did: one that was replaced while it waited is told so.
- **Turned away there**, the relay keeps its name and is printed nothing. Nothing is put down as held. The
  batch stays in `client.json` as made and not had (`pending`), exactly as it does for a relay that was
  replaced while it waited.
- **The batch is not lost.** The relay with hooks that takes over is printed it, by the path that was there
  for a replaced relay's batch (`_owed`); if it has waited too long by then, the brain is asked afresh, as
  before.
- **A relay with hooks is not asked.** `bare` returns at once for one whose `brain next` came through its
  hook.
- The early look stays where it was, so a newcomer without hooks still replaces nobody.

The other two things `next_batch` can print after the wait are a line to come back with, and nothing else:
when the batch that is owed is no longer the one this call waited for, and when the run lock's lease no longer
reaches the batch's last call.

`player/brain/client.py` is 400 lines, as it was.

## R2: what it was, and what was built

`brain stopped` is the operator's word for a batch whose relay will make no more calls. Its own text says it
is "never the batch the running relay holds". A relay that is turned away after it was let in is still the
relay on record: `bare` changes nothing, on purpose. So the word could not be said of its batch, by its
token, by the batch's id, or by `all`, until a relay with hooks had taken over and the batch had gone to
`gone`. The guide and the first note both said otherwise, and no test tried it.

I have not loosened `stopped`: taking the running relay's batch on the strength of a STOP line would mark
calls as over that nothing shows to be. The guide now says, under "When that word is taken back":

1. see that the relay has ended;
2. start a relay with hooks, which takes over; the old batch is then listed by `brain stopped`;
3. say `stopped TOKEN` with the old relay's token;
4. the new relay's next `brain next` tells the brain.

It also says what R1 makes true: the relay is printed no more calls from that moment, "not at its next
`brain next`, and not by one that is waiting for its batch"; and, for the review's sixth answer, that it is
the newcomer that is given no name, where one that was let in keeps its own.

## The tests

Six, in `test_hook_relay.ARelayWithoutHooksIsTurnedAway` (15 now):

| Test | What it holds |
|---|---|
| `test_the_word_taken_back_while_it_waits_is_taken_back_for_the_batch_it_waits_for` | The review's schedule, six ways: the word unsaid, the file gone, the file broken, each while `brain next` waits for the brain's answer and while it spends the batch's wait. The STOP line; nothing held; the batch still made; the next `brain next` the same, with nothing changed |
| `test_the_batch_it_waited_for_goes_to_the_relay_with_hooks_that_takes_over` | That batch, by its id, printed to the relay with hooks as a stand-in, made, and answered |
| `test_with_the_word_standing_through_the_wait_it_is_printed_its_batch` | The other side: nothing changed for a relay the director lets play |
| `test_a_relay_with_hooks_is_printed_its_batch_whatever_becomes_of_the_word_while_it_waits` | The review's positive control |
| `test_one_that_was_replaced_while_it_waited_is_told_so_and_not_the_new_line` | The relay that took over comes first |
| `test_its_batch_is_let_go_by_the_operators_word_once_a_relay_with_hooks_has_taken_over` | R2: the review's four commands, which take nothing; then the guide's order, to the brain letting the batch's calls go |

On `9c2955ba` the first of them prints `profile.getUser` where it expects the STOP line.

## A test that looked a moment too soon (fcb0929c)

The review's first run of the suite had one failure, in
`TheCommandLine.test_a_relays_brain_next_starts_the_resident_by_itself`, at its last assertion, and none on a
rerun. It is not this change's: the test fails **3 runs of 40 here, on this branch and on 071ba1b1 alike**.

It ends the resident brain, waits until the process is gone from the process list, and takes the brain's lock
at once. It finds a process by its command line in `/proc`. A process that is ending is without its command
line a moment before it lets go of its files, so now and then the test looked in between. It waits for the
lock now, five seconds at most. What it asserts is what it asserted: the lock is free again. **80 runs, none
failed.**

I had reported "three runs in a row" of the suite at every handoff of this line. They were true runs; the
suite was nonetheless one that failed about one run in fourteen. It is a commit of its own, to be judged by
itself.

## Verification on the code head (fcb0929c)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 651 tests`, `OK`, three runs in a row, none skipped (`9c2955ba`: 645) |
| `python3 -m unittest -v player.tests.test_hook_relay` | `Ran 101 tests`, `OK` (95) |
| The test that raced, alone, 80 times | 80 passed |
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 30 tests`, `OK` |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | 30 runs, each as before |
| `python3 -m player.tests.test_walk 200 300` | the output of `184ce648`, to the byte |
| Two fuzz scripts and three simulated fights of mine, not in the repository | the output of `184ce648`, to the byte |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits 9c2955ba..HEAD`), `git diff --check 9c2955ba` | exit 0 each; 331 rulings |

### Planted defects

Six, each in a throwaway worktree of the code head, the whole suite run on each. Every one fails a test.

| Planted defect | Tests that fail |
|---|---|
| The word is not asked for again when the batch is printed | 2: `test_the_word_taken_back_while_it_waits_is_taken_back_for_the_batch_it_waits_for`, and the batch's going to the relay that takes over |
| Turned away there, the batch it waited for is dropped | the same 2 |
| One that was replaced while it waited is told the new line | 3, among them `test_one_that_was_replaced_while_it_waited_is_told_so_and_not_the_new_line` |
| A relay with hooks is asked for the word when its batch is printed | 4, among them `test_a_relay_with_hooks_is_printed_its_batch_whatever_becomes_of_the_word_while_it_waits` |
| Turned away there, the batch is put down as the one it holds | `test_the_word_taken_back_while_it_waits_is_taken_back_for_the_batch_it_waits_for` |
| The word is asked for again, and only of a relay that is new | 2 |

R2 changed no code, so there is nothing of it to plant; its test fails on `9c2955ba`'s guide only in the
sense that it runs what that guide did not say.

## Size

The player's code is 6,379 lines in 32 files (`9c2955ba`: 6,373): the six are text in `player/hooked.py`,
which is 387 lines. `player/brain/client.py` is 400. The same two files are over 400 lines, the same 17
functions over 12 branches. The tests are 12,176 lines (12,044).

## Not done, and why

- **No run under Claude Code for R1.** The schedule needs the word taken back inside one `brain next`'s wait.
  The tests do that with the real client and brain and a clock they move; a session would add a model that
  is told to stop, which the first note's runs already show.
- **No event when a relay is turned away**, as the first note says. The STOP line is what says so.
- **The protocol number stays 10**, as the review concludes it can once R1 is closed.

## Live-game statement

Zero live requests. Nothing here started a session of Claude Code. No gameplay action, no write, no
credential.

## Not begun

Running the check on the operator's machine. AP1's live gate, which waits for the re-review of 071ba1b1, for
this review, and for the check.
