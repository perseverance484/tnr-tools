# AI player hook relay — independent second re-review

**Verdict: REQUEST CHANGES — one medium-severity recovery defect.** The four prior reproductions are corrected. The new completion handoff loses its `answered` evidence when `client.json` is reloaded, leaving a completed batch held in the brain until operator intervention. This affects both an unanswered request and reuse of a pending answer.

Reviewed 2026-11-14, repository `perseverance484/tnr-tools`, Lane A.

| Ref | Commit |
|---|---|
| Frozen target, `fable/ai-player-hook-relay` | `b5624861c9dee3f0acdc2ce48385057fcf4eedc8` |
| Code commit | `3a11c846` |
| Base / verified merge-base | `ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844` |
| `main` observed during review | `1db7b6aa6b5632742edc007e5b94378eb92d0346` |
| Report branch, based on the frozen target | `chatgpt/review-ai-player-hook-relay-rereview2` |

Scope: `git diff ec231943 b5624861`. Read in the requested order: `player/hooked.py`, including its opening design; `player/hook.py`; `player/brain/client.py`, including `_collect`, `_greet`, `_exchange`, `_taken`; then `player/tests/test_hook_relay.py`. Reviewed the second correction handoff, changed design/operator documentation, and the unchanged ledger, receipt, spending and equipment consumers together. The previous report at `ff901d64` is evidence only and was not merged.

Authority: the review request, RUL-2026-11-13-157 and -156, `state/prompt_ai_player_overhaul.md`, and `docs/design/AI_PLAYER_OVERHAUL.md`. Zero live requests, no game-source execution, no credentials, no implementation edits, and no changes to `fable/*`.

## R5 — Medium: the client discards the new completion evidence on reload

Locations at the frozen target:

- [`player/hooked.py:294`](https://github.com/perseverance484/tnr-tools/blob/b5624861c9dee3f0acdc2ce48385057fcf4eedc8/player/hooked.py#L294): `account` removes the completed batch from `gone` and appends `[id, at, token, "answered"]` to `ended`.
- [`player/brain/client.py:91`](https://github.com/perseverance484/tnr-tools/blob/b5624861c9dee3f0acdc2ce48385057fcf4eedc8/player/brain/client.py#L91) and [`:113`](https://github.com/perseverance484/tnr-tools/blob/b5624861c9dee3f0acdc2ce48385057fcf4eedc8/player/brain/client.py#L113): `_who` filters `ended` through `_a_word`, which accepts only `"back"` and `"stopped"`.
- [`player/brain/client.py:214`](https://github.com/perseverance484/tnr-tools/blob/b5624861c9dee3f0acdc2ce48385057fcf4eedc8/player/brain/client.py#L214), `:228–239`, and `:152–169`: completion evidence is saved before asking the brain, or while reusing an already pending answer; subsequent client reads discard it.

The new record is valid when produced and sent directly to the brain. It is invalid according to the client that must keep it across requests. Because `account` has already removed its batch from `gone`, another scan does not reconstruct the evidence. Keeping the late result file is insufficient: `account` scans only marked entries still in `gone`.

**Schedule A: no answer to the completion request.** Reproduced with the real client/brain and the checked-in AP2 spending fixture:

1. The brain plans 180,000 ryo of purchases. Admit the first 165,000 purchase and keep its result outstanding.
2. Close and hand in the batch after the wait. Its four calls become loose and its 180,000 reservation correctly stays open.
3. Deliver the late result. On the next `brain next`, `account` removes the batch from `gone` and saves an `answered` row. Make `_await` return `None`, without letting the brain consume the request.
4. Retry. `_who` silently drops the row; `_sweep` removes the unanswered request that carried it. The new request has neither the batch in `gone` nor its completion in `ended`.
5. Continue through two rounds of reads. The brain still holds all four calls and the original reservation. The result remains stored, but the completion is never sent again.

Output, with generated batch identifiers normalized:

```json
{"saved_ended":[["B",1800000124.7998838,"T","answered"]],"parsed_ended":[],"late_result_kept":true,"loose_after_retry_and_two_rounds":{"B":4},"reservation":[["B",180000.0]],"client_gone":[]}
```

The same omission applies if the client dies after saving this evidence and before the brain reads it. A brain that has already consumed and saved the evidence is a different case; its ledger is not made loose again by this finding.

**Schedule B: retry of an already saved answer.** This does not require the brain to fail:

1. Hand in a batch with a call out. Let the brain answer, let `_taken` finish, then stop the client before it prints the pending batch.
2. Deliver the old call's late result.
3. Retry the old `brain next`. `account` creates the completion row, but `_owed` supplies the pending answer, so no request sends the row to the brain.
4. `_exchange` saves it; the second `_who` in `next_batch` discards it before printing the pending batch and writing the client file again.
5. Hand in the new batch. The old batch remains loose, although its result is stored and the client has no outstanding entry for it.

```json
{"retry_reused_pending":true,"client_ended":[],"client_gone":[],"brain_still_holds_completed_batch":true,"result_retained":true}
```

**Consequence.** This is conservative loss of progress, not premature release or an observed overspend. It permanently consumes minute capacity and keeps spending reservations; the analogous equipment batch remains unresolved to the brain. Repeated occurrences can exhaust available capacity. `brain stopped` can still recover the batch from the brain's ledger, so the severity is medium. The automatic recovery promised by the handoff does not work under these schedules.

**Correction.** Make the producer and client validator agree on the new completion kind. Keep completion evidence durable until the brain acknowledges it, including while an existing pending batch is reused. Add a serialization/reload test and both schedules above. In an isolated scratch control, admitting `answered` through the existing validator was the only behavior changed: both schedules then delivered completion and released the old batch's hold. No repository implementation was changed for that control.

The suite's new receipt test has the result arrive before the retry constructs its completion row and sends it directly to the brain. The cleanup tests have the result arrive after the pending batch has been printed. Neither exercises a completion row crossing the client reload in the two schedules above.

## Disposition of the requested checks

| Check | Assessment |
|---|---|
| R1: unresolved operation and exposure | The original premature-release reproduction is corrected. `out` distinguishes a claimed line from an admitted call and requires a result in the inbox or hooks' folder before considering that call answered. `account` moves an unresolved held batch to marked `gone`; the unchanged brain keeps its minute slots, spending reservation and equipment invalidation. Reads while it remains unresolved do not retire the reservation. The spending fixture passes three rounds with no second purchase. Completion normally releases the hold and only a subsequent eligible read reconciles it. R5 blocks reliable delivery of that completion. |
| R1: a replaced relay comes back with a call out | Corrected: `back` marks the entry rather than declaring it over. The replacement keeps the old batch loose until its result arrives or the operator supplies the word. Admission and replacement synchronization make this inspection meaningful: an old hook cannot admit a new call after the replacement was named. A replaced relay that never comes back remains held, as explicitly scoped. |
| R2: last read, admission and replacement | Corrected. `_greet` names the replacement under the same `hook/lock` used for the hook's final ownership read and `call` write. The exact final-read schedule now makes replacement wait. The admitted call is recorded before replacement and is then accounted as in flight. Client operations take `client.lock` before `hook/lock`; hooks take only `hook/lock`. No reverse acquisition or wait loop holding `hook/lock` was found. For a supported hooked relay the initial Bash hook creates the hook folder before naming; `make=False` preserves the plain-relay path. |
| R3: acknowledgement and cleanup | The original repeated-cleanup loss is corrected. Cleanup determines unresolved lines from their own records and result presence, before removing inbox results. Repeated cleanup preserves a call still out. `handed_in` does not reconstruct a consumed snapshot when `handed == token`. Both before/after-cleanup crash tests and eventual success/failure callbacks pass. R5 is a remaining completion-acknowledgement defect, rather than a recurrence of the lost call identity. |
| R3: `ok` only after storage | Corrected for the reviewed success and failure paths. Post success returns `ok` only when `answered` reports a successful write. An unknown or refused call yields no replacement. An inbox failure falls back to `late/`; failure of both stores leaves the original response visible. PostToolUseFailure preserves the error and stores its normalized outcome where possible. No reproduced `ok` without a stored outcome remains. |
| R4: inbox, hooks' folder, transcript | The original failure is corrected. A failed inbox write can be recovered from the hooks' folder with the batch. If both writes fail, there is no terminal `shown` marker: the line remains out. `recover` checks the transcript by the admitted call's tool-use ID, makes a bounded initial lookup, and retries on later requests. It writes a recovered outcome before `out` can declare completion. A late transcript append no longer destroys the unresolved identity. Success and rate-limit cases pass. R5 can still lose the subsequent completion word. |
| Immutable result snapshot and receipt replay | The saved `T.results` rows remain unchanged on retry; new late content is not added to a request the brain may already have answered. The receipt consumer can take completion evidence without applying old result content twice. That consumer works when it receives the evidence; R5 loses it earlier, in the client. |
| Concurrent dispatch and waits | Thirty runs of the five-process probe passed. The 2 s claim grace and 120 s outstanding-call wait remain; the Bash and connector pre-hook timeouts remain 180 s and 300 s. The new transcript lookup occurs inside `brain next`, after its Bash hook returns: up to eight 0.25 s sleeps, with an initial look as well. No hook lock is held over these waits. Scheduling, I/O and lock contention are additional elapsed time. A timeout no longer means that the operation completed. |
| Protocol 10 and predecessor 9 | Correct bump. The full suite runs the actual `ec231943` predecessor, alongside `184ce648` and `661f3f63`, with no skips. Old client/pending/receipt state does not become a current executable batch; old exposure remains subject to the existing takeover rules. R5 is a within-version record-validation mismatch, not a missing protocol bump. |
| Plain relay and kind | The plain-relay game-equivalence and fixed-kind tests pass. Collection now leaves another batch's inbox results until cleanup can retain them in the hooks' folder where applicable. This is the intended preservation change, not a switch of relay kind. |

## Judgment on “What reaches the brain,” point 3

**Acceptable as an explicitly narrower recovery contract, once R5 is fixed.** I do not require a late payload to be applied as a result of the next batch. Keeping its original batch identity, retaining its content, and sending durable completion evidence lets the existing reservation and read-back machinery reconcile without introducing stale state into a new batch. The normal spending case demonstrates the required order: unresolved hold, recorded result, completion evidence, then a read eligible to pay off the reservation.

This is not delivery of every raw result to the brain. A late success will not produce the ordinary success-side activity processing, and a late `rate_limited` payload is archived rather than delivered as a new rate-limit signal. Current state must be obtained again; event history can retain the earlier `NO_ANSWER`. The handoff now states that tradeoff explicitly. Its known limit concerning a replaced relay's transcript also remains: automatic fallback reads the running relay's transcript, so a replaced relay's unrecorded outcome can require the operator's word. These are constraints of the contract, not evidence that the result was applied exactly once to the world model.

The result must remain associated with its admitted call, unresolved exposure must remain held, and completion must survive every retry until acknowledged. Point 3 is sound in principle on those terms; R5 means this frozen implementation does not yet fulfill them. This review judgment is not a merge or live-run authorization.

## Verification and limits

| Check on the frozen target | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 631 tests passed, no skips, 60.565 s; includes 83 hook tests and the three predecessor versions. |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | All 30 runs passed: four calls in order, closure after their answers, four results delivered, no leftovers. First allowance to closing: 0.59–0.65 s. |
| `python3 -W ignore::ResourceWarning /workspace/scratch/review_hook_rereview2.py` | Two adversarial schedules reproduce R5. Both isolated validator controls deliver completion and release the old hold. |
| `python3 scripts/player_allowlist.py check` and `report --check` | Passed: 93 endpoints, zero never-list violations; report current. |
| `python3 scripts/rulings_index.py --check` | Passed: 327 rulings; index current. |
| `git diff --check ec231943 b5624861` | Passed. |
| Report guards: `git diff --cached --check`, `python3 scripts/check_no_real_name.py`, `python3 scripts/check_large_files.py` | Passed: zero prohibited-name hits and zero unallowed large files. |

Scratch probes use the checked-in `Hooks` and AP2 spending fixtures, temporary folders, mocked clocks, and the real client, brain, ledger and receipt code. They make no connector requests. Only `_await` returning no answer or an exception immediately after the real `_taken` introduces the failure schedules; the validator is modified only in the separately labeled in-process controls. The scratch harness is outside the repository and is not committed.

Compact reproduction of schedule B, from the repository root:

```python
from unittest import mock
from player.brain import client
from player.tests.test_hook_relay import Hooks, OK

h = Hooks()
h.start()
try:
    token, lines = h.first_batch()
    batch = h.client()["held"]
    inp, real = h.sent(lines[0])
    taken = client._taken

    class Died(Exception):
        pass

    def cleared_then_die(*args):
        taken(*args)
        raise Died()

    try:
        with mock.patch.object(client, "_taken", cleared_then_die):
            h.next(token)
    except Died:
        pass
    assert h.client()["pending"] and batch["id"] in h.loose()
    assert h.comes(inp, real) == OK
    new, lines, _ = h.next(token)  # Reuses pending; completion vanishes on reload.
    assert h.client()["gone"] == [] and h.client()["ended"] == []
    h.does(lines)
    h.next(new)
    assert batch["id"] in h.loose()  # Defect: completed batch still held.
finally:
    h.doCleanups()
```

Actual Claude Code agent-file hook registration, timeout/failure enforcement, transcript flush order and Duet's environment remain unverified. There is no `claude` executable in this workspace. The process probe verifies local concurrency, not the host hook engine. No live probe was attempted. The prior estimate assessment is unchanged; the estimate and token fields are outside this correction's code diff. The author's mutation-testing claims were read, not independently rerun.

Next step: Fable corrects the completion-record round trip on its own branch and returns a new frozen SHA with both retry schedules covered. Preserve the closure, immutable snapshot, unresolved-call accounting, synchronized replacement and fallback-storage fixes. No merge or live run was performed.
