# AI player overhaul, the relay's hooks: third correction handoff, after the second re-review of b5624861

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-14, in answer to the second
re-review of `b5624861` ("request changes": one finding, R5, medium; R1 to R4 corrected; point 3 of "What
reaches the brain" acceptable once R5 is fixed).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-relay
Reviewed: b5624861c9dee3f0acdc2ce48385057fcf4eedc8
Review: docs/reviews/AI_PLAYER_HOOK_RELAY_REREVIEW2_REVIEW.md on
        chatgpt/review-ai-player-hook-relay-rereview2 @ 9c7b67ed (evidence; not merged)
Base of this correction: b5624861. Not rebased: this head is two commits on it.
Code: a2eba139
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Stands on: AP2's first part at 661f3f63 (approved), AP1 at 62e1aab1 (accepted)
Authority: RUL-2026-11-13-157, RUL-2026-11-13-156, as before
```

The diff to review is `git diff b5624861 HEAD`: one line of `player/brain/client.py`, its docstring, three
tests, and this note.

## Disposition

R5 is **confirmed and corrected**.

| The review's schedule | On `b5624861` (its output) | Now |
|---|---|---|
| A. The result of the call that was out has come. `brain next` puts down the word that the batch is over; the brain gives no answer; `brain next` again | `parsed_ended: [], loose_after_retry_and_two_rounds: {"B": 4}, reservation: [["B", 180000.0]]` | The word is read back, and the request that is made again carries it. The brain lets the batch go, the reservation is marked over, and the read after that pays it off: the day has 15,000 left |
| B. The brain has answered and the batch is cleared away; `brain next` dies before it prints the next; the result comes; `brain next` again prints the batch that was waiting, and asks nothing | `client_ended: [], brain_still_holds_completed_batch: true` | The word stays in `client.json` while the waiting batch is printed, and goes with the next request. The brain no longer holds the batch |

The report's script for B, run as it is printed, stops at its `assert h.client()["gone"] == [] and
h.client()["ended"] == []`: the word is there. On `b5624861` it runs to its end.

## What it was

`hooked.account` writes a new kind of word that a batch is over: `[id, when, token, "answered"]`. `brain next`
reads `client.json` back through a filter that keeps what is in the shape this code writes (`client._who`),
and the filter's test of such a word, `_a_word`, knew two kinds, `"back"` and `"stopped"`. So the word was
right when it was made, and went with a request made in the same `brain next`. Read from the file again it
was dropped. By then `account` had taken its batch out of `gone`, so nothing made the word a second time.

The second correction's tests all took the word from the request of the `brain next` that made it. None had
it cross a read of the file.

## What was built

- `client._a_word` knows `"answered"`.
- Both of the review's schedules are tests: `ACallThatIsOutHoldsWhatItMayCost.
  test_the_word_that_it_is_over_is_kept_until_the_brain_has_it` (A, on the spending fixture, to the read that
  pays off) and `WhatIsKeptOfABatch.
  test_the_word_that_a_batch_is_over_waits_with_a_batch_that_is_waiting_to_be_printed` (B, as the report ran
  it).
- `WhatIsKeptOfABatch.test_what_is_put_down_of_a_batch_is_read_back_as_it_was_written` writes every mark
  that goes on a batch in `gone` (`closed`, `back`) and every kind of word (`answered`, `back`, `stopped`)
  into `client.json` and reads them through `_who`. A word of another kind is still dropped.

## Did a wider assumption change?

I looked for the same thing elsewhere: something `player/hooked.py` writes into `client.json` that `_who`
does not pass.

- The marks on a batch in `gone`: `_a_batch` asks for a token and an id and keeps the rest of the entry. The
  test above holds that.
- `held`, `handed`, `hooks`, `steps`, `until`, `seen`: `_who` leaves them as they are.
- The other side: the brain takes a word of any kind (`core.evidence`); only the event it writes for the
  operator's word asks for the kind.
- The word is kept until the brain has it on every path I can find: a request the brain did not answer; a
  batch that was waiting, printed with no request; a new relay named meanwhile (`_greet` carries `ended`); a
  waiting batch given up when the run lock's lease has run out (`runlock.given_up` leaves it). It is cleared
  in one place, where the brain's answer to the request that carried it has been taken.

## The contract, and the director's word

The review accepts point 3 of "What reaches the brain" (a late result is kept, its coming is the word that
the batch is over, and what it says is not given to the brain) as a narrower contract, once R5 is corrected.
The director has approved the same, with the other open points of this line (RUL-2026-11-14-159; it is on
`fable/ai-player-hook-proof` with the preparation for the proof, not in this diff, so that this diff is the
correction and nothing else).

## Verification on the head's parent (the code commit)

Everything in this table was run on the code commit, `a2eba139`, in this cloud session. Nothing here makes a
request of the game.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 634 tests`, `OK`, three runs in a row, none skipped (`b5624861`: 631) |
| `python3 -m unittest -v player.tests.test_hook_relay` | `Ran 86 tests`, `OK` (`b5624861`: 83) |
| Planted defects, in throwaway worktrees | below |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | 30 runs, each as before: the calls in order, `brain next` after the last answer, four results at the brain, nothing left over |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the output of `184ce648`, to the byte |
| Two fuzz scripts and three simulated fights of mine, not in the repository | the output of `184ce648`, to the byte |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits b5624861..HEAD`), `git diff --check b5624861` | exit 0 each; 327 rulings on this branch |
| The report's script for schedule B (`docs/reviews/AI_PLAYER_HOOK_RELAY_REREVIEW2_REVIEW.md`, its last block) | on `b5624861` it runs to its end; here it stops at the assertion that the word is gone |

### Planted defects

Twenty-nine, one at a time, each in a throwaway worktree made from `a2eba139`, never in the repository's own
tree. The whole player suite was run for each. The worktrees were clean after the runs and are removed. Every
one fails at least one test.

They are the rows that take the corrections apart: the two for R5 (the first is the finding put back as it
was; the second lets any word through), and the twenty-seven for R1 to R4 of the second correction's note,
planted again in the code as it is now.

The other ninety-five of that note's hundred and twenty-two were not run again. They were run on `7f2d002f`
and `3a11c846`, and the code differs from `3a11c846` by the one line of `_a_word`. The tests have only been
added to.

| Planted defect | Tests that fail |
|---|---|
| R5: the word that a batch is over, by its result, is not read back | 3 fail: `test_the_word_that_a_batch_is_over_waits_with_a_batch_that_is_waiting_to_be_printed`, `test_the_word_that_it_is_over_is_kept_until_the_brain_has_it`, and 1 more |
| R5: any word is read back as word that a batch is over | 1 fails: `test_what_is_put_down_of_a_batch_is_read_back_as_it_was_written` |
| R1: a batch with a call that is out is handed in as over | 7 fail, 1 error: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 6 more |
| R1: a batch that is gone is over as soon as it was closed | 8 fail, 1 error: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 7 more |
| R1: the word that such a batch is over is never brought | 10 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, and 8 more |
| R1: such a batch is over as of now, not as of when its result came | 5 fail: `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, `test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch`, and 3 more |
| R1: a line with its result beside the late ones is still out | 13 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, and 11 more |
| R1: a line whose result is in the inbox is still out | 26 fail, 4 errors: `test_a_batch_is_closed_by_the_relay_that_holds_it_and_no_other`, `test_a_batch_is_closed_once_however_often_its_relay_comes`, and 27 more |
| R1: a line whose call did not go is out | 14 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, and 12 more |
| R1: another batch's line is taken for this batch's | 9 fail: `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 7 more |
| R1: a replaced relay that is back has ended its batch though a call of it is out | 1 fails: `test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch` |
| R1: a batch whose replaced relay came back with a call out is never over | 1 fails: `test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch` |
| R1: a batch whose relay was replaced and is not back is over when nothing of it is out | 19 fail, 3 errors: `test_a_batch_can_be_named_by_its_id`, `test_a_client_file_is_this_versions_or_no_file`, and 20 more |
| R1: what is on record of a batch that is still held goes when it is old | 1 fails: `test_what_nobody_handed_in_stays_while_its_batch_is_held_and_goes_an_hour_after` |
| R1: a call that is still out is left out of what is handed in | 9 fail: `test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 7 more |
| R2: a new relay is named without the hooks' lock | 2 fail: `test_a_new_relay_is_not_named_between_a_hooks_last_look_and_its_letting_the_call_go`, `test_each_of_them_waits_while_another_has_it` |
| R2: one who is no hook never waits for the hooks' lock | 2 fail: `test_a_new_relay_is_not_named_between_a_hooks_last_look_and_its_letting_the_call_go`, `test_each_of_them_waits_while_another_has_it` |
| R3: clearing a batch away takes the line of a call that is out | 8 fail, 1 error: `test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again`, `test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over`, and 7 more |
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

## Size

`player/brain/client.py` is 400 lines (`b5624861`: 399): the one line is in `_a_word`'s own text. Nothing else
in the player's code is changed: 6,351 lines in 32 files, the same two files over 400 lines, the same 17
functions over 12 branches. The tests are 11,857 lines (`b5624861`: 11,788).

## Known limits

Those of the second correction's note stand, unchanged.

## Live-game statement

Zero live requests in this correction. The one live request of this line is the probe's read, before the first
handoff. No gameplay action, no write, no credential.

## Open

Nothing new. The director's points are settled (RUL-2026-11-14-158, -159). What follows an approval is the
proof of the hooks on Claude Code itself, against a stand-in connector
(`docs/reviews/evidence/ai_player_hook_relay/PROOF_PLAN.md` on `fable/ai-player-hook-proof`), then AP1's live
gate on this line's head.

## Not begun

AP2's second part; the script that starts a relay; a live run; replacing a relay inside a fight; a ledger
that ends a replaced relay's batch by the record alone.
