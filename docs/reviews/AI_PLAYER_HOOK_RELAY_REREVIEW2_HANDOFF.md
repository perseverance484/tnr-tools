# AI player overhaul, the relay's hooks: second correction handoff, after the re-review of ec231943

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-13, in answer to the re-review of
`ec231943` ("request changes": R1 and R2 high, R3 and R4 medium; protocol 9 and the relabelled estimate
passed).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-relay
Reviewed: ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844
Review: docs/reviews/AI_PLAYER_HOOK_RELAY_REREVIEW1_REVIEW.md on
        chatgpt/review-ai-player-hook-relay-rereview1 @ ff901d64 (evidence; not merged)
Base of this correction: ec231943. Not rebased: this head is three commits on it.
Code: 3a11c846 (7f2d002f, the correction; then one commit of tests for what the planted defects found)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Stands on: AP2's first part at 661f3f63 (approved), AP1 at 62e1aab1 (accepted)
Authority: RUL-2026-11-13-157, RUL-2026-11-13-156, as before
```

The diff to review is `git diff ec231943 HEAD`. Read `player/hooked.py` first: its opening text is the
design, and "A call that is out" is the centre of this correction.

## Disposition

All four findings are **confirmed and corrected**. The re-review keeps the closing and the saved rows; so
does this.

| Finding | The re-review's case | On `ec231943` (its output) | Now |
|---|---|---|---|
| R1 high | 180,000 ryo of the day left. A purchase of 165,000 goes and does not come back in 120 s. `brain next`; reads made while it is still out; then its result | `old_batch_still_out_or_loose: false, new_purchase: 180000` (345,000 admitted against 180,000) | The batch is handed in as gone, not held: its calls stay loose and the 180,000 stay reserved. `new_purchase: 0` through three rounds of reads. When the result comes, the next `brain next` brings the word that the batch is over as of then; the read after that pays the reservation off (the day has 15,000 left). `old_result_delivered: false` still: see "What reaches the brain" |
| R2 high | A's hook has made its last read of `client.json` under the hooks' lock; B is named; A writes `call` and allows | `old_call_allowed: true, old_call_recorded_after_replacement: true` | B is named under the same lock, so it waits until A's hook has let the call go or refused it. The call is on record before B is named: a call that is out, of a batch that is gone |
| R3 medium | A call out at the closing; the brain answers; `brain next` clears the batch away and dies; run again | `open_claim_after_retry: false, model_shown: ok, late_result_stored: false` | `open_claim_after_retry: true, late_result_stored: true`. The report's own script stops at its `assert not os.path.exists(claim)` |
| R4 medium | One `relay.put` fails; the transcript has the call and the `brain next`, and the result only after `brain next` has run | `waited: 0, brain_data: null, original_claim_retained: false` | The result is written to the hooks' own folder instead and handed in with the batch: `brain_data` is the result, and a rate limit stays a rate limit. With nothing of ours writable: `waited: 120`, the brain is told the call has no answer, the batch is not over, `original_claim_retained: true`; when the transcript has the result the next `brain next` takes it from there and the batch is over as of then |

I ran the report's R3 script on `ec231943` (it runs through: the defect) and on this code (it stops at the
assertion above). Its scripts for R1, R2 and R4 are not in its branch; the rows are its schedules as the
report gives them, as tests (below). The R2 schedule cannot be run in one thread any more: the second
`brain next` would wait for a lock that the same thread holds. The test runs it in a thread of its own and
sees it wait.

## What was built

### Closed is not over (R1)

A line of a batch is **out** when its call went to the connector (`call` is on its line) and no result of it
is on record: not in the inbox, not in `live/hook/late/` (`hooked.out`). That is all the hooks can know of
whether an operation has ended, and it is now what decides whether a batch is over.

When a relay hands a batch in and a line of it is out, `brain next` moves the batch in `client.json` from
`held` to `gone`, marked `closed`, before it asks the brain (`hooked.account`). `gone` is AP1's word for a
batch that was printed and not handed in. The brain does with it what it does with any such batch
(`core._ledger`, `budget.settle`): its calls are loose, they count in every minute, and what they may cost
and what they may change in my equipment stays owed (`owed.open_batches`). The brain's code is not touched.
The call itself is still handed in as an error that says it has no answer, so the brain reads again; but that
error no longer says anything about the batch.

Each time `brain next` comes after that, it looks at the batches that are gone and marked (`account`). When no
line of one is out any more, it puts `[id, when the last result came, token, "answered"]` among the word for
the brain (`ended`): AP1's evidence that a held batch is over, which the brain takes from every request,
also one it answers from its receipt. From the request after that one, a read pays off what the batch owed
(`owed.settle`, unchanged): the reconciliation read is known to follow the operation.

If the result never comes, the batch stays held until the operator says `brain stopped <token>`, as for any
batch that was not handed in. `brain stopped` lists it.

A replaced relay that comes back was, until now, word enough that its batch is over. With hooks its
`brain next` can come back while a call of its is out, so that is no longer enough: the batch is marked
`back` and is over when nothing of it is out (`hooked.back`, `account`). A replaced relay that has not come
back is held as before; this change does not end its batch by the record alone.

### A new relay is named under the hooks' lock (R2)

`_greet` writes the new relay into `client.json` with `live/hook/lock` held. A hook's last read of the file
and its writing `call` are under the same lock, so the two cannot interleave. The order is fixed and is in
`hooked.py`: `brain next` takes the hooks' lock while it holds the client's lock; a hook takes the hooks'
lock alone; never the other way round; never across a wait. Where no hook has ever run there is no lock
folder, and a relay is named without it: a relay with hooks cannot be on record there, because the hook in
front of its first `brain next` makes the folder.

A call that was let go before the new relay was named is a call in flight. It is out, its batch is gone, and
its result is kept when it comes. A call whose hook looks after the naming is refused, as before.

### Clearing away can be done again (R3)

`hooked.consumed` no longer goes by `T.closed`. For each line of the batch it looks at the line itself: a
line that is out stays; every other goes, with the batch's other records. The lines are looked at before
the results leave the inbox, so a line whose result was handed in is never taken for one that is out. Done a
second time it finds only the lines that are out, and leaves them.

What is on record of a batch that is held or gone never goes by age. The hour runs only for a batch that is
neither.

`hooked.handed_in` returns nothing, and writes nothing, for a batch the brain has had.

The hook behind a call returns `ok` only when the result was written down. For a tool call it does not know
(no line with that id and a `call`) it writes nothing and returns nothing: the model keeps what it was
shown.

### A result the hook cannot write down (R4)

There is no `shown` state any more. The hook behind a call tries, in order:

1. the inbox, when the batch is the one held and is not closed;
2. `live/hook/late/`, the hooks' own folder, also when the inbox cannot be written;
3. nothing: it returns nothing, the model keeps the result, and the line stays out.

A result in `late/` when its batch is handed in goes with it (it is moved to the inbox first if that can be
written). So the re-review's schedule, with one failing `relay.put`, needs no transcript.

For case 3, `brain next` looks for the results of lines that are out in the relay's own transcript, by the
tool call's id (`hooked.recover`): for two seconds when the batch is handed in (eight looks, `SPOOL`), and
once more every time it comes while the batch is gone. What it finds goes to `late/`. Found in time, it is
handed in with the batch. Found later, it is what ends the batch, and is kept. A failed call found this way
keeps what it failed with.

### Kept whoever takes over

A relay without hooks used to take away what was in the inbox for another batch. It no longer does
(`client._collect` reads its own batch's and leaves the rest); `consumed` moves them to `late/` under the
name of their line, so a line that was answered is not taken for one that is out. This was the first
correction's limit 4.

### The number is 10

`client.json` now has batches among `gone` that their own relay handed in, and marks on them. `ec231943` is
held to 9 by the test that held `184ce648` to 8.

## What reaches the brain

The re-review calls reading 1 "a narrowed delivery contract". It is, and this is the whole of it:

1. A result that is on record when its batch is handed in reaches the brain with the batch, once.
2. A call whose result is not on record then is handed in as an error that says it has no answer. Its batch
   is not over, and what it may cost stays reserved, until the result is on record or the operator's word.
3. A result that comes after its batch was handed in is kept in `late/`. That it came is what the brain is
   told (the batch is over as of then). What it says is not given to the brain.

Point 3 is the one that is not "every result reaches the brain". The alternative is to hand a late result in
with a later batch. The brain takes a result as the answer to a call of the batch it comes with, and AP1's
accepted rule is that a late result is not taken (`relay.read_batch`). I have not changed that. It is the
director's and the reviewer's to say whether point 3 is acceptable as it stands.

## Readings of mine

1. The contract above.
2. **The first correction's reading 2 is withdrawn.** A call out for 120 s is still handed in as an error and
   the relay goes on, but its batch is not over.
3. **The transcript is the last place, not the first.** The inbox, then the hooks' folder, then the
   transcript, looked in for two seconds at the hand-in and again at every `brain next`.
4. **A replaced relay's batch is not ended by the record alone.** Only its coming back or the operator's
   word ends it, as in AP1; coming back does not while a call of it is out. A ledger that ends a replaced
   relay's batch by itself is still not begun.
5. **The brain's event for a batch held this way uses AP1's words**: "it did not hand its batch in". The
   relay did, with a call out. `budget.py` is not touched; `player/OPERATOR.md` says what it means here.
6. **All of the batch's calls are held, not only the one that is out.** That is AP1's accounting for a batch
   that is not over.
7. `SPOOL` (8 looks, 0.25 s apart) is my figure.

## Verification on the head's parent (the code commit)

Everything in this table was run on the code commit, `3a11c846`, in this cloud session. Nothing here makes a
request of the game: the suite and the scripts use the rig's stand-ins and folders of their own.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 631 tests`, `OK`, three runs in a row, none skipped (`ec231943`: 618) |
| `python3 -m unittest -v player.tests.test_hook_relay` | `Ran 83 tests`, `OK` (`ec231943`: 70) |
| A hundred and twenty-two planted defects in the code of this change, in throwaway worktrees | below |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | 30 runs, each: four calls and `brain next`, their hooks started together as five processes; the calls go in order, each after the answer before it; `brain next` after the last answer; four results at the brain; nothing left over |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the output of `184ce648`, to the byte |
| Two fuzz scripts and three simulated fights of mine, not in the repository | the output of `184ce648`, to the byte |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits ec231943..HEAD`), `git diff --check ec231943` | exit 0 each; 327 rulings |
| `estimate.py`, on the session's log from `duet/ai-player-ap1-live` | exit 0; unchanged |
| The report's R3 script (`docs/reviews/AI_PLAYER_HOOK_RELAY_REREVIEW1_REVIEW.md`, its last block) | on `ec231943` it runs to its end; here it stops at `assert not os.path.exists(claim)` |

The same table was first run on `7f2d002f`, before the two tests of `3a11c846`: 630 tests, three times, and
the rest as here. The test that failed once for the first reviewer
(`test_a_relays_brain_next_starts_the_resident_by_itself`) passed in all six runs of the suite.

### The re-review's schedules, as tests

All in `player/tests/test_hook_relay.py`.

| The re-review's case | Test |
|---|---|
| R1, on the spending fixture of AP2's re-review, to the end: the result comes, the word, the read that pays off | `ACallThatIsOutHoldsWhatItMayCost.test_it` |
| R1, the result never comes: the operator's word | `ACallThatIsOutHoldsWhatItMayCost.test_the_operators_word_ends_it_when_the_result_never_comes` |
| R1, what the request says and what is kept | `ABatchIsClosedBeforeItIsHandedIn.test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over` |
| R1, a replaced relay that is back while its call is out | `ABatchIsClosedBeforeItIsHandedIn.test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch`, and with nothing out |
| R1 with the receipt: `brain next` dies after the brain answered, the result comes, run again | `ABatchIsClosedBeforeItIsHandedIn.test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again` |
| A batch is closed once, also while its call is out | `ABatchIsClosedBeforeItIsHandedIn.test_a_batch_is_closed_once_however_often_its_relay_comes` |
| R2: a new relay between the hook's last read and its writing `call` | `AHookThatIsBehindTheTimes.test_a_new_relay_is_not_named_between_a_hooks_last_look_and_its_letting_the_call_go`; the lock itself: `OneAtATime` |
| R3: cleared, died, run again; and died before clearing; the success and the failure that come after | `WhatIsKeptOfABatch.test_clearing_a_batch_away_again_keeps_the_line_of_a_call_that_is_out`, `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again` |
| R3: `ok` only for what was written down | `WhatTheBrainGets.test_a_tool_call_that_no_hook_let_through_gives_no_result`, `test_what_comes_for_a_call_the_hook_refused_is_no_result` |
| R4 as injected (one `relay.put` fails; the transcript has no result yet), a success and a rate limit | `AResultTheHookCannotWriteDown.test_when_the_inbox_cannot_be_written_it_is_kept_in_the_hooks_folder_and_handed_in_from_there`, `test_a_failed_call_keeps_what_it_failed_with` |
| R4 with nothing writable: the result in the transcript only after `brain next`, a success and a rate limit | `AResultTheHookCannotWriteDown.test_a_result_the_host_has_not_written_down_yet_is_not_given_up`, `test_a_failure_the_host_has_not_written_down_yet_keeps_what_it_failed_with` |
| R4: the two seconds, and no longer | `AResultTheHookCannotWriteDown.test_it_is_looked_for_for_a_moment_when_the_batch_is_handed_in`, `test_no_longer_than_that_and_with_no_transcript_not_at_all` |
| Results in the inbox kept whoever takes over | `WhatIsKeptOfABatch.test_results_in_the_inbox_for_a_batch_nobody_handed_in_are_kept_whoever_takes_over` |
| `ec231943` held to protocol 9 | `TheHeadsBeforeThisOne.test_what_its_correction_left_is_another_versions` |

### Planted defects

A hundred and twenty-two, one at a time, each in a throwaway worktree made from the code, never in the
repository's own tree. The whole player suite was run for each. The worktrees were clean after the runs and
are removed. The unchanged code passes: the runs of the suite above.

Forty-three are new with this correction or changed with it; the other seventy-nine are the first
correction's, planted in the code as it is now. The rows marked R1 to R4 take this correction apart piece by
piece and name tests that fail; the first row is R1 as the re-review found it. For the other rows the count
is given.

The run was made on `7f2d002f`. The container this session runs in was restarted during it, after 27. The
three defects that were in the worktrees at that moment were taken out again (the worktrees were back at
`7f2d002f`, clean), and the other 95 were run after that.

A hundred and twenty failed at least one test. Two passed every test, and both showed a rule that the tests
of this correction had stopped holding:

| Planted defect | What the tests lacked | Now |
|---|---|---|
| H2: a batch is closed anew each time its relay comes | The test that held it ran `brain next` again after the call's result had come, which this correction counts as an answer: there was nothing left to wait for either way | A test in which the relay comes again while its call is still out: it is not waited for a second time (`3a11c846`) |
| result: the result of a call that did not go is taken | Since `ok` stands only for what was written down, the hook's answer no longer tells this case from a result that could not be written | The test reads the hooks' log, which does (`3a11c846`) |

Both were planted again on `3a11c846`, the whole suite for each. Each fails now: their rows below are from
that run. `3a11c846` changes tests only.

In three of the hundred and twenty-two runs `test_a_relays_brain_next_starts_the_resident_by_itself` failed
beside the tests that caught the defect: the test that starts a real process and is tight on time, with
three suites running on four cores. It was never the only test to fail.

| Planted defect | Tests that fail |
|---|---|
| R1: a batch with a call that is out is handed in as over | 5 fail, 1 error: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 4 more |
| R1: a batch that is gone is over as soon as it was closed | 6 fail, 1 error: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 5 more |
| R1: the word that such a batch is over is never brought | 8 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, and 6 more |
| R1: such a batch is over as of now, not as of when its result came | 4 fail: `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, `test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch`, and 2 more |
| R1: a line with its result beside the late ones is still out | 11 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, and 9 more |
| R1: a line whose result is in the inbox is still out | 23 fail, 4 errors: `test_a_batch_is_closed_by_the_relay_that_holds_it_and_no_other`, `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, and 24 more |
| R1: a line whose call did not go is out | 13 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, and 11 more |
| R1: another batch's line is taken for this batch's | 8 fail: `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 6 more |
| R1: a replaced relay that is back has ended its batch though a call of it is out | 1 fails: `test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch` |
| R1: a batch whose replaced relay came back with a call out is never over | 1 fails: `test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch` |
| R1: a batch whose relay was replaced and is not back is over when nothing of it is out | 20 fail, 3 errors: `test_a_batch_can_be_named_by_its_id`, `test_a_client_file_is_this_versions_or_no_file`, and 21 more |
| R1: what is on record of a batch that is still held goes when it is old | 1 fails: `test_what_nobody_handed_in_stays_while_its_batch_is_held_and_goes_an_hour_after` |
| R1: a call that is still out is left out of what is handed in | 9 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 7 more |
| R2: a new relay is named without the hooks' lock | 2 fail: `test_a_new_relay_is_not_named_between_a_hooks_last_look_and_its_letting_the_call_go`, `test_each_of_them_waits_while_another_has_it` |
| R2: one who is no hook never waits for the hooks' lock | 2 fail: `test_a_new_relay_is_not_named_between_a_hooks_last_look_and_its_letting_the_call_go`, `test_each_of_them_waits_while_another_has_it` |
| R3: clearing a batch away takes the line of a call that is out | 6 fail, 1 error: `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 5 more |
| R3: the results leave the inbox before the lines are looked at | 12 fail: `test_a_batch_is_closed_by_the_relay_that_holds_it_and_no_other`, `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, and 10 more |
| R3: what is handed in is put together anew for a batch the brain has had | 1 fails: `test_clearing_a_batch_away_again_keeps_the_line_of_a_call_that_is_out` |
| R3: ok is shown for what was not written down | 7 fail: `test_a_result_the_host_has_not_written_down_yet_is_not_given_up`, `test_a_tool_call_that_no_hook_let_through_gives_no_result`, and 5 more |
| R3: ok is shown for a result that could not be written down | 4 fail: `test_a_result_the_host_has_not_written_down_yet_is_not_given_up`, `test_it_is_looked_for_for_a_moment_when_the_batch_is_handed_in`, and 2 more |
| R3: nothing is said of a result that could not be written down | 5 fail: `test_a_failure_the_host_has_not_written_down_yet_keeps_what_it_failed_with`, `test_a_result_the_host_has_not_written_down_yet_is_not_given_up`, and 3 more |
| R4: a result the inbox cannot take is not kept beside the late ones | 2 fail: `test_a_failed_call_keeps_what_it_failed_with`, `test_when_the_inbox_cannot_be_written_it_is_kept_in_the_hooks_folder_and_handed_in_from_there` |
| R4: the transcript is not looked in for a line that is out | 2 fail, 2 errors: `test_a_failure_the_host_has_not_written_down_yet_keeps_what_it_failed_with`, `test_a_result_the_host_has_not_written_down_yet_is_not_given_up`, and 2 more |
| R4: ok in a transcript is taken for a result | 1 fails: `test_a_result_the_model_was_shown_ok_for_is_never_taken_from_the_transcript` |
| R4: the transcript is looked in once when a batch is handed in | 2 fail: `test_it_is_looked_for_for_a_moment_when_the_batch_is_handed_in`, `test_no_longer_than_that_and_with_no_transcript_not_at_all` |
| R4: the transcript is not looked in when a batch is handed in | 3 fail: `test_it_is_looked_for_for_a_moment_when_the_batch_is_handed_in`, `test_no_longer_than_that_and_with_no_transcript_not_at_all`, and 1 more |
| R4: a line that is out is not looked for again when `brain next` comes | 2 errors: `test_a_failure_the_host_has_not_written_down_yet_keeps_what_it_failed_with`, `test_a_result_the_host_has_not_written_down_yet_is_not_given_up` |
| H1: clearing a batch away clears every batch | 11 fail, 1 error |
| H2: a result is handed in for whatever batch the relay holds now | 2 fail, 4 errors |
| H2: a late result that is there is not handed in | 5 fail |
| H2: a late result that is handed in stays beside the late ones | 3 fail |
| H2: results in the inbox for a batch nobody handed in are dropped | 4 fail, 1 error |
| H2: results in the inbox for a batch nobody handed in are kept under another name | 4 fail, 1 error |
| H2: the results of a batch stay in the inbox when the brain has them | 11 fail |
| H2: what nobody handed in is kept for ever | 1 fails |
| line: a line whose result is on record counts as out | 15 fail, 5 errors |
| line: a refused line counts as out | 3 fail |
| line: a line that was passed over counts as out | 1 fails |
| lock: a batch is cleared away without it | 1 fails |
| result: the model is shown the result itself | 28 fail |
| result: the results are handed in last call first | 3 fail |
| result: a result in the inbox for another batch is read as this batch's | 1 fails |
| protocol: the number is still the one before | 1 fails |
| H1: a hook sweeps away what other batches have on record | 7 fail |
| H1: after its waits a hook goes by what it read before them | 2 fail, 1 error |
| H2: `brain next` does not wait for a call that is out | 4 fail |
| H2: a batch that was not closed is handed in | 1 fails |
| H2: a result that comes when the batch is closed is handed in for it | 2 fail |
| H2: a result whose batch is over is dropped | 11 fail, 5 errors |
| H2: a result of another batch is not known for a call's | 7 fail, 1 error |
| H2: what is handed in is put together anew each time | 1 fails |
| H2: what was handed in is not kept | 3 fail |
| H2: a batch is closed anew each time its relay comes | 1 fails: `test_a_batch_is_closed_once_however_often_its_relay_comes` |
| H2: a line that had not gone at the closing is put down as out | 1 fails |
| H2: a batch that is closed and not yet handed in still lets calls go | 6 fail |
| H2: a batch the brain has still lets calls go once its records are cleared | 1 fails |
| H2: the log is cleared away when it is old | 1 fails |
| H2: a batch that was handed in is judged again when its relay asks again | 2 fail |
| line: a line does not wait to be taken by a tool call | 4 fail |
| line: a line that was taken is not waited for | 5 fail |
| line: a line that is passed over can still be taken | 1 fails |
| line: a line goes whatever became of the one before it | 4 fail |
| line: a line can be taken twice | 5 fail |
| line: a hook that fails keeps its line | 1 fails |
| line: the wait in front of a call is not spent | 5 fail |
| line: a wait is spent again in front of every call behind it | 2 fail |
| line: nothing is on record of the hook having run | 41 fail, 15 errors |
| lock: it locks nothing | 2 fail |
| lock: a call is let go without it | 2 fail |
| lock: a result is handed in without it | 1 fails |
| lock: a batch is closed without it | 1 fails |
| command: any command is run | 1 fails |
| command: `brain next` may have more behind it | 1 fails |
| command: it may be run from anywhere | 2 fail |
| command: the relay's id is not put behind it | 3 fail, 68 errors |
| command: an id is passed on whatever is in it | 1 fails |
| command: a subagent is known by its session, not by itself | 18 fail |
| command: the id is not taken from the command line | 1 fails |
| command: the id stays among `brain next`'s arguments | 1 fails |
| command: another relay's `brain next` closes this relay's batch | 1 fails |
| batch: a relay with hooks is printed the calls themselves | 20 fail, 44 errors |
| batch: a relay without hooks is printed stand-ins | 30 fail, 2 errors |
| batch: a stand-in does not say which batch it is of | 45 fail, 18 errors |
| batch: the stand-ins are numbered from nought | 47 fail, 15 errors |
| batch: the waits are printed to a relay with hooks too | 2 fail, 1 error |
| batch: the steps are not kept for the hook | 46 fail, 19 errors |
| batch: the cutoff is not kept for the hook | 1 fails |
| batch: which kind a relay is, is not kept | 23 fail, 43 errors |
| hook: a call written out by hand is taken for a stand-in | 2 fail |
| hook: a stand-in with more beside it is taken | 1 fails |
| hook: a stand-in whose input has more in it is taken | 1 fails |
| hook: a number in any form is taken for the call's | 1 fails |
| hook: any tool is taken for the connector's | 1 fails |
| hook: a tool call with no id is let through | 1 fails |
| hook: another agent's call for this relay's batch goes | 5 fail |
| hook: a call of a batch the relay does not hold goes | 1 fails |
| hook: a call the batch has not got is looked for | 1 fails |
| hook: the run lock's cutoff is not minded | 3 fail |
| hook: a call at the cutoff goes | 2 fail |
| hook: a cutoff that cannot be read is no cutoff | 1 fails |
| hook: another version's client file is used | 1 fails |
| hook: after the waits nothing is looked at again | 4 fail |
| hook: the select is left out of the call | 1 fails, 6 errors |
| hook: a hook that fails lets the call go as it stands | 2 fail |
| hook: an input that cannot be read is let through | 1 error |
| hook: nothing is written down of what was refused | 2 fail |
| result: any tool call's result is taken for a call's | 14 fail, 3 errors |
| result: the result of a call that did not go is taken | 1 fails: `test_what_comes_for_a_call_the_hook_refused_is_no_result` |
| result: one that came as a dict is not understood | 1 fails |
| result: a failed call's words are read as a result | 2 fail |
| result: a result that cannot be read loses the hook its answer | 1 fails |
| result: a relay with hooks is read as one without | 14 fail |
| result: its stand-ins are counted as calls nobody asked for | 1 fails |
| result: the results' times are taken for the transcript's | 1 fails |
| result: `brain put` hands a result in for the wrong call | 1 error |
| stop: a relay whose hooks never ran is printed more | 1 fails |
| stop: a relay may come with hooks one time and without the next | 1 fails |
| stop: a relay is judged at every batch, however often its hooks have run | 4 fail, 3 errors |
| stop: a relay that has had no call yet is stopped | 23 fail, 43 errors |
| stop: a relay without hooks is judged as one with | 45 fail, 20 errors |
| tokens: what was read from the cache is not kept apart | 2 fail |
| tokens: the log does not say which relay carried a batch | 1 error |

## Size

`python3 scripts/player_size.py`, on `ec231943` and now:

| | `ec231943` | Now |
|---|---|---|
| Player code | 6,249 lines in 32 files | 6,350 lines in 32 files |
| Tests | 11,464 lines | 11,788 lines |
| `player/hook.py` | 289 | 286 |
| `player/hooked.py` | 256 | 361 |
| `player/brain/client.py` | 400 | 399 |
| `player/relay.py` | 400 | 400 |
| Files over 400 lines | `activities/battle.py`, `budget.py` | the same two |
| Functions over 60 lines | none | none |
| Functions over 12 branches | 17 | the same 17 |

## Source, generated files, and what else changed

No game source is read by this change, and no generated contract or pinned SHA moves. Changed:
`player/hooked.py`, `player/hook.py`, `player/brain/client.py` (`_collect`, `_greet`, `_exchange`),
`player/relay.py` (the number), `player/tests/test_hook_relay.py`, `player/OPERATOR.md` ("Hooks"), the
design's 4.7. `player/budget.py`, `player/owed.py` and `player/brain/core.py` are not changed. The earlier
notes are left as they were written; where they and this note differ, this one holds.

## Known limits

1. **Claude Code's hook engine has still not run these hooks**, as the re-review says: hooks declared in an
   agent file, real timeouts and failures, the order in which the transcript is written, Duet's machine.
2. **A call that was let go and never answers, in any form**, holds its batch until the operator's word. That
   includes a call the host did not make after the hook allowed it, unless the transcript says so.
3. **What the transcript says of a tool call is taken for its outcome**, as it is for a relay without hooks.
   An interrupted call has a block there too.
4. **Only the running relay's transcript is looked in.** A line of a replaced relay that is out is resolved
   by its hook's result, or by the operator's word.
5. **While a batch is held this way the brain plays on fewer calls a minute**: each of the batch's calls
   takes a place in every minute.
6. **The line of a call stays an hour after its batch is over**, beside its result in `late/`.
7. Of the first correction's limits: 3 (the 120 s and the 2 s) and 7 (the estimate) stand; 4 is corrected; 1,
   2, 5 and 6 are restated here. The first note's limits stand as that correction left them.

## Live-game statement

Zero live requests in this correction. The one live request of this line is the probe's read, before the first
handoff. No gameplay action, no write, no credential.

## Open

For the director, unchanged: whether the hook's "allow" is acceptable; `effort: low` on the relay; whether
the light-polls branch is dropped; AP1's live gate and the head it runs on; whether the line goes to `main`;
the first run on Duet's machine. From this note: "What reaches the brain", point 3.

For a later session, with the director's word: a local probe of the real hook engine with a fake connector.

## Not begun

AP2's second part; the script that starts a relay; a live run; replacing a relay inside a fight; a ledger
that ends a replaced relay's batch by the record alone.
