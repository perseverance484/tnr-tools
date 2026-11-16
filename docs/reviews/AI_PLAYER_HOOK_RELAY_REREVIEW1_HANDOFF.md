# AI player overhaul, the relay's hooks: correction handoff after the review of 184ce648

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-13, in answer to the review of
`184ce648` ("request changes": H1 and H2 high, H3 medium; a remark under check 4; a qualification of the
token estimate).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-relay
Reviewed: 184ce648a0268c8e4b280f280392938b6ee371ac
Review: docs/reviews/AI_PLAYER_HOOK_RELAY_REVIEW.md on chatgpt/review-ai-player-hook-relay @ 1f73ee12
        (evidence; not merged)
Base of this correction: 184ce648. Not rebased: this head is five commits on it.
Code: 0a281dad (b96fef81, the correction; then three small commits for what the planted defects found)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Stands on: AP2's first part at 661f3f63 (approved), AP1 at 62e1aab1 (accepted)
Authority: RUL-2026-11-13-157, RUL-2026-11-13-156, as before
```

The diff to review is `git diff 184ce648 HEAD`.

## Disposition

All three findings are **confirmed and corrected**. They are one defect seen from three sides: nothing said
when a batch of a relay with hooks is over. So the correction is one thing, a batch's life on record, and it
is best read as a whole: `player/hooked.py`, then `player/hook.py`.

| Finding | The review's case | On `184ce648` (the review's output) | Now |
|---|---|---|---|
| H1 high | relay A's hook reads `client.json` and is held up; relay B takes over and completes its first call; A's hook goes on; B's call is sent again | `claim_after: false, repeat_allowed: true, game_calls: 2` | `claim_after: True, repeat: "that call was made already, or its turn has passed", game_calls: 1` |
| H2 high, A | a call is let go; `brain next` runs before its result is in; the result comes | `batch_advanced: true, late_result_taken: false, results_at_brain: 0` | the hook in front of `brain next` waits for the call, 120 s at most, and the batch does not advance before. The result comes in that time: `results_at_brain: 1`. It does not (the review's script delivers it only after `brain next` has returned): the brain is handed an error for the call, which says it has no answer, and the result is kept in `late/` when it comes, not given to the brain (reading 1) |
| H2 high, B | call 1 done; `brain next` writes its request and dies; a brain at home answers it; call 2 is made; `brain next` again | `request_result_counts: [1, 2], retry_absorbed: [], late_result_deleted: true` | call 2 is refused (the batch was closed when the relay came to hand it in); `request_result_counts: [1, 1]`, the same rows; nothing is deleted unread |
| H3 medium | the hook cannot write the result down | `model_shown: ok, results_at_brain: 0, stopped: false` | the model is shown the result itself; `brain next` takes it from the relay's transcript: `results_at_brain: 1`. With no transcript to take it from, the brain is handed an error that says so |
| Check 4 | tool calls of one message started together | a line whose hook ran before the line in front of it was taken was refused, and the batch was cut | a line waits for the one in front of it to be taken (2 s) and to be answered (120 s) |
| Estimate, low | one request a batch; a new relay's context counted as cached; "requests" for batches | 4.84M / 2.42M / 0.41M / 0.14M | relabelled a scenario estimate, with the batch's other requests and a cold start counted: 4.96M / 2.42M / 0.41M / 0.14M warm, 5.64M / 2.43M / 0.44M / 0.14M cold |

The review's H1 script is printed in its report. I ran it on `184ce648` and got its output. It cannot run as
printed now: it holds the old hook up at `_first`, the function that swept other batches' records, which is
gone. The row above is the same schedule with the hook held up at the same moment, just after it has read
`client.json` (`AHookThatIsBehindTheTimes.test_it_takes_nothing_of_the_new_relays_and_no_call_goes_twice`).
The review's script for H2 and H3 is not in its branch; the rows are its schedules as its report gives them,
as tests of the suite (below). What each of the three findings was made of, put back into this head, fails
those tests (planted defects, below).

## What was built

### A batch on record, and who may remove it (H1)

`live/hook/` holds, for the batch with token T:

| File | Made by | Says |
|---|---|---|
| `T.seen` | the hook in front of a call | a hook has run for this batch |
| `T.<n>.json` | the tool call that takes line n, once (a hard link) | `use`: that tool call's id. Then `refused`, or `call`: the endpoint and input that went to the connector. `{"passed": true}`: nobody took the line in time, and nobody may now. `shown`: its result could not be handed in |
| `T.closed` | the hook in front of `brain next`, once | how each line had ended: answered, refused, passed, shown, or open |
| `T.results` | `brain next`, once | the rows the brain was handed |
| `late/` | the hook behind a call | results that came for a batch that was closed, or that its relay no longer held |

**No hook removes any of it**, whatever batch it is of. The sweep is gone. A hook that is behind the times can
still write, but only under the token it was asked about, and never that a call went.

What is on record of a batch is removed in one place: `hooked.consumed`, which `brain next` calls when the
brain has the batch's results. It runs under the client's lock and the hooks' lock, after `client.json` says
the batch is handed in, so no call of that batch can go any more. It removes that batch's records and its
handed-in results; it keeps the line of a call that was still out, so that a result that comes for it can be
known for what it is. Whatever any other batch has on record is left alone until it is an hour old, which is
many times longer than a hook can live (the longest timeout in the agent file is 300 s).

After its waits, the hook in front of a call reads `client.json` again and decides by that reading, under the
lock, in the same step that puts `call` on the line. A hook that read the file before its relay was replaced
is refused there.

### A batch is closed before it is handed in (H2)

The hook in front of `brain next` now does more than put the relay's id behind the command. When the command
hands in the batch its relay holds, the hook **closes** the batch first (`hooked.close`):

1. It waits for every line to end. A line that a tool call has taken is waited for, 120 s in all (`TURN`): it
   is waiting for its turn, or its call is with the connector. A line no tool call has taken is given 2 s
   (`GRACE`) and is then passed over for good.
2. Under the lock, it writes `T.closed`: how each line ended. A line whose hook was still waiting, so whose
   call has not gone, is put down as refused, and that hook refuses when it looks again.

From then on no call of the batch goes, and no result is handed in for it. `brain next` refuses to hand in a
batch of calls that was not closed (`hooked.stop`: the relay is told to stop, as when its hooks do not run).

`brain next` no longer takes whatever result files are there. It hands in what the closing says
(`hooked.handed_in`), and it keeps the rows it handed in (`T.results`) before it writes its request. Run
again, it hands in those same rows, so the brain's receipt and the request it is asked again always agree.
The receipt's deduplication is untouched.

- A line that was **answered** is handed in from its result file, as before.
- A line that was still **open** is handed in as an error: `no answer: the call went to the connector, and
  its result was not there when the batch was handed in`. The brain treats an error on an action as an
  outcome it does not know and reads again (`battle._acted`), as it does for a relay without hooks.
- A line that was refused or passed over has no row, as a call a relay without hooks did not make has none.

A result is bound to its call by the tool call's id, which the line keeps, whatever batch the relay holds by
then (`hook._made`). The review's case A failed because the result was looked for among the current batch's
lines only.

A result that comes after its batch was closed, or after its relay was replaced, is written to
`live/hook/late/T.<n>.json` and the model is shown `ok`. If it is there when the rows are first put together
(it came between the closing and `brain next`), it is taken out of `late/` and handed in with them. So what
is in `late/` is what the brain was not handed.

### A result that cannot be handed in (H3)

The hook behind a call returns `ok` in the result's place only when the result is written down: handed in, or
kept in `late/`. When that fails it returns nothing, so Claude Code shows the model the result itself and the
relay's transcript has it. The line is marked `shown` if that much can be written. `brain next` then takes the
result from the transcript by the tool call's id (`hooked._in_transcript`), the way it reads a relay without
hooks; a result that was too large for the conversation is read from the file Claude Code saved it to, as
before. If nothing at all can be written, the line stays open, the closing waits for it, and the result is
still taken from the transcript. With no transcript, the brain is handed the error above.

The same holds for a call that failed (`PostToolUseFailure`): the model sees the error in any case, and the
transcript's error block is read.

### Lines started together (check 4)

A line is taken by a tool call when its hook starts, not when its call goes. The hook of line n then waits for
line n-1: up to 2 s for a tool call to take it, up to 120 s for it to end. It goes only when line n-1 has its
answer. So four hooks started at once, in any order, make the four calls in order. A line that is refused or
passed over still cuts the batch there.

The waits are counted in looks of 50 ms, not in seconds added up. The agent file gives the two hooks that
wait the time to do it: 180 s in front of `brain next` (was 30), 300 s in front of a call (was 180). A test
holds those against `GRACE`, `TURN` and the longest pause the pacing puts in front of a call (a minute).

### The lock

`live/hook/lock` (`flock`) is held for a moment by whoever lets a call go, hands a result in, closes a batch
or clears it away. It is never held across a wait. It is what makes "closed" exact: a result is either in
before the closing and on its record, or after it and in `late/`.

### The number is 9

A batch held under 8 has no closing on record, and its lines say less. 8 was never run (`184ce648` was a
review target), but the rule in `relay.py` is to change the number when in doubt. `184ce648` is held to its
number by the test that held `661f3f63` to 7.

### The estimate

`docs/reviews/evidence/ai_player_hook_relay/estimate.py` is relabelled a scenario estimate, in its text and in
its table. A batch's requests beyond the first are now counted (one more read of the conversation each), for
every scenario alike. Each scenario is printed twice: with a relay's first request reading its birth context
from the cache, and writing it. "Requests over 100,000" is now "Batches over 100,000". The figure for a relay
with hooks is unchanged at 0.14M, 97% under the session's relay. It is still put together from single probe
requests. No relay with hooks has carried a batch.

## What changes for a relay that does as it is told

Nothing in what the game sees: `TheSameGameEitherWay` still passes (the same calls at the same moments, batch
for batch, with hooks and without). `brain next` starts 2 s later when the relay left a line of its batch out,
and up to 120 s later when a call of the batch has not come back.

## Readings of mine

These are choices I made where the review left room. Each is the director's or the reviewer's to change.

1. **A late result is kept and not given to the brain.** The review asks that outcomes in flight "remain
   deliverable across replacement and retries". Across retries they are handed in: the closing waits for
   them. A result that comes after the closing gave up on it, or after its relay was replaced, is kept in
   `late/` under its batch and call. It is not fed to the brain with a later batch: AP1's accepted rule is
   that a result belongs to its relay and its batch, and the brain already treats a replaced relay's batch
   as out until it is told otherwise. By the time a late result could be fed in, the brain has been told the
   call has no answer and has read again; what the call may have cost stays reserved until a read that is
   known to follow it (AP2, `player/owed.py`). The late result would tell it the same, out of order.
2. **A call that is out for 120 s is handed in as an error, and the relay goes on.** The alternative is to
   stop the relay. An error is what the brain already knows how to act on: it reads again.
3. **H3's "recoverable spool" is the relay's own transcript.** The review offers a spool or a state that
   prevents normal continuation. A second file of ours would fail with the first. The transcript is not
   ours to write: Claude Code keeps it, in its own folder. If the result is not there either, the brain is
   handed the error that says the call has no answer. The cost is that the result is in the model's
   conversation, once, when our folder cannot be written.
4. **A batch is closed when its relay comes to hand it in, whether or not the brain then answers.** Before,
   a batch the brain had not taken could still be finished. That was the window H2 used.
   `test_a_batch_the_brain_has_not_taken_yet_can_still_be_finished` is replaced by
   `test_a_batch_the_brain_did_not_take_stays_closed`.
5. **A call made out of order passes the earlier line over for good.** Before, it was refused and could be
   made again in order. With lines waiting for each other, a line refused for its order would have to give
   its claim back, and I did not want a record that can be undone.
6. **`GRACE` 2 s and `TURN` 120 s** are my figures.
7. **RUL-2026-11-13-157 is not edited.** Its scope names `player/hook.py` and protocol 8, as of its date.
   The design (`docs/design/AI_PLAYER_OVERHAUL.md` 4.7) and `player/OPERATOR.md` ("Hooks") say how it is now.

## Verification on the head's parent (the code commit)

Everything in this table was run on the code commit, `0a281dad`, in this cloud session. Nothing here makes a
request of the game: the suite and the scripts use the rig's stand-ins and folders of their own.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 618 tests`, `OK`, three runs in a row, none skipped (`184ce648`: 592) |
| `python3 -m unittest -v player.tests.test_hook_relay` | `Ran 70 tests`, `OK` (`184ce648`: 44) |
| A hundred and one planted defects in the code of this change, in throwaway worktrees | below |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | 30 runs, each: four calls and `brain next`, their hooks started together as five processes; the calls go in order, each after the answer before it; `brain next` after the last answer; four results at the brain; nothing left over |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the figures of `184ce648`, to the byte |
| Two fuzz scripts and three simulated fights of mine, not in the repository | the output of `184ce648`, to the byte |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits 184ce648..HEAD`), `git diff --check 184ce648` | exit 0 each; 327 rulings |
| `estimate.py`, on the session's log from `duet/ai-player-ap1-live` | exit 0; the figures in the disposition |

The same table was first run on `b96fef81`, while the planted defects ran beside it on the same machine: 616
tests, three times, and the rest as here. The test that failed once for the reviewer
(`test_a_relays_brain_next_starts_the_resident_by_itself`) passed in all six runs of the suite.

### The review's schedules, as tests

All in `player/tests/test_hook_relay.py`.

| The review's case | Test |
|---|---|
| H1: the old relay's hook is held up after reading `client.json`; the new relay's call is tried again after it goes on | `AHookThatIsBehindTheTimes.test_it_takes_nothing_of_the_new_relays_and_no_call_goes_twice` |
| H1, every hook of a replaced relay | `AHookThatIsBehindTheTimes.test_the_hooks_of_a_relay_that_was_replaced_leave_the_new_relays_batch_alone` |
| H2, A: `brain next` while a call is out | `ABatchIsClosedBeforeItIsHandedIn.test_brain_next_waits_for_a_call_that_is_with_the_connector`; the call that never comes back: `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered` |
| H2, B: as the review ran it (request written, `brain next` dies, a brain at home answers, call 2, again) | `ABatchIsClosedBeforeItIsHandedIn.test_the_second_schedule_as_the_review_ran_it` |
| H2, B with call 2 already out when `brain next` dies, and back before it is run again | `ABatchIsClosedBeforeItIsHandedIn.test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again` |
| H2: replacement while a result is in flight | `ABatchIsClosedBeforeItIsHandedIn.test_the_brain_takes_no_result_of_a_relay_that_was_replaced_and_none_is_lost` |
| H3: `relay.put` fails, for an answer and for a failed call | `AResultThatCannotBeHandedIn`, five tests |
| A batch is closed by its own relay only | `ABatchIsClosedBeforeItIsHandedIn.test_a_batch_is_closed_by_the_relay_that_holds_it_and_no_other` |
| Check 4: started together | `WhatTheHookLetsThrough.test_calls_that_are_started_together_go_in_order_whichever_hook_runs_first`; as processes, `together.py` |
| The lock | `OneAtATime.test_each_of_them_waits_while_another_has_it` |
| `184ce648` held to protocol 8 | `TheHeadsBeforeThisOne.test_what_the_first_head_with_hooks_left_is_another_versions` |

The suite's control from the review also holds: a result set that does not change survives a `brain next` that
dies before an answer (`WhatIsKeptOfABatch.test_it_goes_when_the_brain_has_the_batchs_results_and_not_before`).

### Planted defects

A hundred and one, one at a time, each in a throwaway worktree, never in the repository's own tree. The whole
player suite was run for each. The worktrees were clean after the runs and are removed. The unchanged code
passes: the runs of the suite above.

The run was made on `b96fef81`. Ninety-seven failed at least one test. Four passed every test. None of the
four showed a fault in what the code did. Each showed a rule that no test held:

| Planted defect | What the tests lacked | Now |
|---|---|---|
| H2: the log is cleared away when it is old | The test made the log old and then let a relay with hooks hand a batch in. That relay's own hook wrote to the log first | The test lets a relay without hooks take over (`0382fb13`) |
| command: another relay's `brain next` closes this relay's batch | Where another agent ran the line, the relay had already made all its calls | A test in which the other agent runs the line in the middle of the batch (`b934adf1`) |
| result: its stand-ins are counted as calls nobody asked for | Nothing: the test was there. `brain next` had stopped using `relay.read_batch`'s count and put a nought of its own in its place, so the rule stood twice and the planted defect changed the copy nothing read | `brain next` uses the count again: the one change to the code after `b96fef81` (`0a281dad`) |
| result: the result of a call that did not go is taken | No test gave the hooks behind a call something for a call the hook in front had refused. Nothing should come for one | A test for a Claude Code that runs those hooks all the same (`0a281dad`) |

The four were planted again on `0a281dad`, the whole suite for each. Each fails now: their rows below are from
that run, as is the row for the defect beside the third (a relay with hooks read as one without).

One of the hundred and one I had planted badly: "a late result that is handed in stays among the late ones"
raised an error wherever a batch was handed in, so 44 tests failed for the wrong reason. Planted as it is
meant, on `0a281dad`, it fails the one test that is for it. Its row is from that run.

In three of the hundred and one runs `test_a_relays_brain_next_starts_the_resident_by_itself` failed beside the
tests that caught the defect. It is the test that failed once for the reviewer: it starts a real process and
is tight on time, and three suites and the verification were running on four cores. It was never the only
test to fail.

The rows marked H1, H2 and H3 take the correction apart piece by piece, and name the tests that fail. The
first row is the sweep the review found, put back as it was. For the other rows the count is given.

| Planted defect | Tests that fail |
|---|---|
| H1: a hook sweeps away what other batches have on record | 3 fail: `test_it_takes_nothing_of_the_new_relays_and_no_call_goes_twice`, `test_the_brain_takes_no_result_of_a_relay_that_was_replaced_and_none_is_lost`, `test_what_nobody_handed_in_goes_when_it_is_an_hour_old` |
| H1: after its waits a hook goes by what it read before them | 2 fail: `test_a_relay_that_is_replaced_while_its_call_waits`, `test_it_takes_nothing_of_the_new_relays_and_no_call_goes_twice` |
| H1: clearing a batch away clears every batch | 5 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late`, and 2 more |
| H2: `brain next` does not wait for a call that is out | 3 fail: `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_brain_next_waits_for_a_call_that_is_with_the_connector`, `test_when_nothing_at_all_can_be_written_the_call_is_waited_for_and_then_taken_from_the_transcript` |
| H2: a batch that was not closed is handed in | 1 fails: `test_a_batch_its_hook_did_not_close_is_not_handed_in` |
| H2: a result that comes when the batch is closed is handed in for it | 2 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late` |
| H2: a result is handed in for whatever batch the relay holds now | 2 fail: `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_the_brain_takes_no_result_of_a_relay_that_was_replaced_and_none_is_lost` |
| H2: a result whose batch is over is dropped | 4 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late`, and 1 more |
| H2: a result of another batch is not known for a call's | 2 fail: `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_the_brain_takes_no_result_of_a_relay_that_was_replaced_and_none_is_lost` |
| H2: what is handed in is put together anew each time | 1 fails: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again` |
| H2: what was handed in is not kept | 2 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_it_goes_when_the_brain_has_the_batchs_results_and_not_before` |
| H2: a call that is still out is left out of what is handed in | 5 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late`, and 2 more |
| H2: a batch is closed anew each time its relay comes | 1 fails: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again` |
| H2: a line that had not gone at the closing is put down as out | 1 fails: `test_a_line_that_has_not_gone_when_the_batch_is_closed_does_not_go` |
| H2: a batch that is closed and not yet handed in still lets calls go | 6 fail: `test_a_batch_that_has_been_handed_in`, `test_a_batch_the_brain_did_not_take_stays_closed`, `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, and 3 more |
| H2: a batch the brain has still lets calls go once its records are cleared | 1 fails: `test_a_batch_that_has_been_handed_in` |
| H2: a late result that is there is not handed in | 1 fails: `test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late` |
| H2: a late result that is handed in stays among the late ones | 1 fails: `test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late` |
| H2: clearing a batch away takes the line of a call that is out | 3 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late` |
| H2: results handed in for a batch nobody handed in are dropped | 2 fail: `test_the_brain_takes_no_result_of_a_relay_that_was_replaced_and_none_is_lost`, `test_what_nobody_handed_in_goes_when_it_is_an_hour_old` |
| H2: the results of a batch stay in the inbox when the brain has them | 10 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_a_relay_without_hooks_keeps_nothing_there`, and 7 more |
| H2: what nobody handed in is kept for ever | 1 fails: `test_what_nobody_handed_in_goes_when_it_is_an_hour_old` |
| H2: the log is cleared away when it is old | 1 fails: `test_what_nobody_handed_in_goes_when_it_is_an_hour_old` |
| H2: a batch that was handed in is judged again when its relay asks again | 1 fails: `test_a_brain_next_that_died_when_the_brain_had_the_results_is_given_the_batch_when_run_again` |
| H3: the model is shown ok for a result that could not be handed in | 4 fail: `test_a_call_that_failed_and_cannot_be_handed_in`, `test_the_model_is_left_with_it_and_brain_next_takes_it_from_the_relays_transcript`, `test_when_nothing_at_all_can_be_written_the_call_is_waited_for_and_then_taken_from_the_transcript`, and 1 more |
| H3: its line does not say that the model has the result | 3 fail: `test_a_call_that_failed_and_cannot_be_handed_in`, `test_a_relays_brain_next_starts_the_resident_by_itself`, `test_the_model_is_left_with_it_and_brain_next_takes_it_from_the_relays_transcript` |
| H3: a result is not looked for in the relay's transcript | 3 fail: `test_a_call_that_failed_and_cannot_be_handed_in`, `test_the_model_is_left_with_it_and_brain_next_takes_it_from_the_relays_transcript`, `test_when_nothing_at_all_can_be_written_the_call_is_waited_for_and_then_taken_from_the_transcript` |
| H3: ok in a transcript is taken for a result | 1 fails: `test_a_result_the_model_was_shown_ok_for_is_never_taken_from_the_transcript` |
| H3: nothing is written down of a result that could not be handed in | 1 fails: `test_the_model_is_left_with_it_and_brain_next_takes_it_from_the_relays_transcript` |
| line: a line does not wait to be taken by a tool call | 3 fail |
| line: a line that was taken is not waited for | 4 fail |
| line: a line that is passed over can still be taken | 1 fails |
| line: a line goes whatever became of the one before it | 4 fail |
| line: a line can be taken twice | 5 fail |
| line: a line whose result is in counts as out | 16 fail, 4 errors |
| line: a refused line counts as out | 3 fail |
| line: a line that was passed over counts as out | 1 fails |
| line: a line whose result the model has counts as out | 2 fail |
| line: a hook that fails keeps its line | 1 fails |
| line: the wait in front of a call is not spent | 5 fail |
| line: a wait is spent again in front of every call behind it | 2 fail |
| line: nothing is on record of the hook having run | 31 fail, 14 errors |
| lock: it locks nothing | 1 fails |
| lock: a call is let go without it | 1 fails |
| lock: a result is handed in without it | 1 fails |
| lock: a batch is closed without it | 1 fails |
| lock: a batch is cleared away without it | 54 errors |
| command: any command is run | 1 fails |
| command: `brain next` may have more behind it | 1 fails |
| command: it may be run from anywhere | 1 fails |
| command: the relay's id is not put behind it | 3 fail, 55 errors |
| command: an id is passed on whatever is in it | 1 fails |
| command: a subagent is known by its session, not by itself | 13 fail |
| command: the id is not taken from the command line | 1 fails |
| command: the id stays among `brain next`'s arguments | 1 fails |
| command: another relay's `brain next` closes this relay's batch | 1 fails: `test_a_batch_is_closed_by_the_relay_that_holds_it_and_no_other` |
| batch: a relay with hooks is printed the calls themselves | 13 fail, 38 errors |
| batch: a relay without hooks is printed stand-ins | 30 fail, 2 errors |
| batch: a stand-in does not say which batch it is of | 34 fail, 16 errors |
| batch: the stand-ins are numbered from nought | 36 fail, 13 errors |
| batch: the waits are printed to a relay with hooks too | 2 fail, 1 error |
| batch: the steps are not kept for the hook | 36 fail, 16 errors |
| batch: the cutoff is not kept for the hook | 1 fails |
| batch: which kind a relay is, is not kept | 20 fail, 33 errors |
| hook: a call written out by hand is taken for a stand-in | 1 fails |
| hook: a stand-in with more beside it is taken | 1 fails |
| hook: a stand-in whose input has more in it is taken | 1 fails |
| hook: a number in any form is taken for the call's | 1 fails |
| hook: any tool is taken for the connector's | 1 fails |
| hook: a tool call with no id is let through | 1 fails |
| hook: another agent's call for this relay's batch goes | 5 fail |
| hook: a call of a batch the relay does not hold goes | 1 fails |
| hook: a call the batch has not got is looked for | 1 fails |
| hook: the run lock's cutoff is not minded | 2 fail |
| hook: a call at the cutoff goes | 2 fail |
| hook: a cutoff that cannot be read is no cutoff | 1 fails |
| hook: another version's client file is used | 1 fails |
| hook: after the waits nothing is looked at again | 4 fail |
| hook: the select is left out of the call | 1 fails, 6 errors |
| hook: a hook that fails lets the call go as it stands | 2 fail |
| hook: an input that cannot be read is let through | 1 error |
| hook: nothing is written down of what was refused | 2 fail |
| result: the model is shown the result itself | 24 fail |
| result: any tool call's result is taken for a call's | 15 fail |
| result: the result of a call that did not go is taken | 1 fails: `test_what_comes_for_a_call_the_hook_refused_is_no_result` |
| result: one that came as a dict is not understood | 1 fails |
| result: a failed call's words are read as a result | 2 fail |
| result: a result that cannot be read loses the hook its answer | 1 fails |
| result: a relay with hooks is read as one without | 12 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered`, `test_a_call_that_failed_and_cannot_be_handed_in`, and 9 more |
| result: its stand-ins are counted as calls nobody asked for | 1 fails: `test_its_transcript_is_read_for_the_tokens_and_nothing_else` |
| result: the results' times are taken for the transcript's | 1 fails |
| result: `brain put` hands a result in for the wrong call | 1 error |
| result: the results are handed in last call first | 3 fail |
| stop: a relay whose hooks never ran is printed more | 1 fails |
| stop: a relay may come with hooks one time and without the next | 1 fails |
| stop: a relay is judged at every batch, however often its hooks have run | 1 fails, 1 error |
| stop: a relay that has had no call yet is stopped | 20 fail, 33 errors |
| stop: a relay without hooks is judged as one with | 45 fail, 20 errors |
| tokens: what was read from the cache is not kept apart | 2 fail |
| tokens: the log does not say which relay carried a batch | 1 error |
| protocol: the number is still the one before | 1 fails |

## Size

`python3 scripts/player_size.py`, on `184ce648` and now:

| | `184ce648` | Now |
|---|---|---|
| Player code | 6,027 lines in 31 files | 6,249 lines in 32 files |
| Tests | 10,993 lines | 11,464 lines |
| `player/hook.py` | 324 | 289 |
| `player/hooked.py` | | 256 |
| `player/brain/client.py` | 400 | 400 |
| `player/relay.py` | 399 | 400 |
| Files over 400 lines | `activities/battle.py`, `budget.py` | the same two |
| Functions over 60 lines | none | none |
| Functions over 12 branches | 17 | the same 17 |

The hooks' code grew by 221 lines. Most of it is the closing and what `brain next` makes of it.

## Source, generated files, and what else changed

No game source is read by this change, and no generated contract or pinned SHA moves. `player/hook.py` is
split: what is kept of a batch and what `brain next` makes of it is `player/hooked.py`. `player/brain/client.py`
calls `hooked.handed_in` and `hooked.consumed`; `_taken` is now that one call. `.claude/agents/tnr-relay.md`:
the two timeouts. `player/OPERATOR.md` ("Hooks") and the design's 4.7 say the new rules.
`docs/reviews/AI_PLAYER_HOOK_RELAY_HANDOFF.md` (the first note) is left as it was written; where it and this
note differ, this one holds.

## Known limits

1. **Claude Code's hook engine has still not run these hooks.** As the review lists: hooks declared in an
   agent file, `PostToolUseFailure`, a result too large for the conversation, tool calls started together,
   `onFailure: block`. `together.py` (above) runs the hook commands as separate processes started together,
   against a stand-in for the connector. It shows that the hooks keep order and close a batch under real
   concurrency. It does not show how Claude Code schedules them, or that it runs them.
2. **A hook that is killed** (its timeout, the machine) with a line in its hand leaves the line open. The
   closing waits its 120 s for it and puts it down as refused if its call had not gone, as out if it had.
   If the hook was killed between writing `call` and returning, the call did not go and the brain is told it
   has no answer: an outcome it does not know, which is the truth as far as the record goes.
3. **Started together, a line gives up 120 s after its hook starts**, and the closing 120 s after it starts.
   A batch whose own pauses (the pacing under the call limit) add up to more than that is cut there when
   Claude Code starts its tool calls together. Run one after another, it is not: each hook then starts when
   the call before it is back.
4. **A relay without hooks that replaces one with hooks** drops the results that one had handed in, as it
   drops any result handed in for another batch (AP1). When the replacement has hooks they are kept in
   `late/`.
5. **Nothing reads `late/`.** It is for the operator. A result there is the outcome of a call the brain
   counts as unknown.
6. **The line of a call that is out is kept for an hour.** A result that comes later than that is not known
   for a call's, and is not kept.
7. **The token estimate is an estimate.** See its text.
8. Of the first note's limits: 5 is restated here (3) with other figures; 8 was H3 and is corrected; 9 now
   also means `flock`; the others stand.

## Live-game statement

Zero live requests in this correction. The one live request of this line is the probe's read, before the first
handoff. No gameplay action, no write, no credential.

## Open

For the director, unchanged from the first note: whether the hook's "allow" is acceptable; `effort: low` on
the relay; whether the light-polls branch is dropped; AP1's live gate and the head it runs on; whether the line
goes to `main`; the first run on Duet's machine. New: readings 1 and 2 above.

For a later session, with the director's word: the review's local probe of the real hook engine with a fake
connector. It needs a `claude` that can run an agent here; I have not tried whether this session's can.

## Not begun

AP2's second part; the script that starts a relay; a live run; replacing a relay inside a fight; a ledger that
knows a replaced relay with hooks is stopped.
