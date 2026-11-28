# AI player hook relay — independent first re-review

**Verdict: REQUEST CHANGES.** The original stale-hook sweep is removed, and closure plus a saved result snapshot fixes the original changing-request reproduction. The combined lifecycle still has four confirmed defects: a timeout releases financial exposure while a mutation is in flight; replacement can race the final admission check; repeated cleanup loses an outstanding call's identity; and transcript fallback can be acknowledged before its result exists in the transcript.

Reviewed 2026-11-13, repository `perseverance484/tnr-tools`.

| Ref | Commit |
|---|---|
| Frozen target, `fable/ai-player-hook-relay` | `ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844` |
| Code commit | `0a281dad` |
| Previous reviewed head / verified merge-base | `184ce648a0268c8e4b280f280392938b6ee371ac` |
| `main` observed during this re-review | `c56ff81ca53311c974b5ea8c65060d8347e9a8f9` |
| Report branch, based on the frozen target | `chatgpt/review-ai-player-hook-relay-rereview1` |

Scope: `git diff 184ce648 ec231943`. Read in the requested order: `player/hooked.py`, `player/hook.py`, `player/brain/client.py` (including `_collect` and `_taken`), then `player/tests/test_hook_relay.py`; afterward the correction handoff and surrounding receipt, budget, spending, and equipment code. The previous report on `chatgpt/review-ai-player-hook-relay@1f73ee12` is evidence only and was not merged. Authority remains RUL-2026-11-13-157, RUL-2026-11-13-156, the approved player brief/design and this review request.

Zero live-game requests or writes; no live credentials/session material; no game-source execution. All calls below are fixture calls in temporary rehearsal folders. No implementation changes and no modifications to `fable/*` branches.

**R1 — High: a timed-out mutation is treated as a completed batch, so a read made before the mutation finishes can release its spending reservation.**

Locations: [`player/hooked.py:204–219`](https://github.com/perseverance484/tnr-tools/blob/ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844/player/hooked.py#L204), especially the synthetic `NO_ANSWER` result; `player/brain/client.py:221–225`; existing consumers `brain/core.py:_ledger`, `budget.py:settle`, and `owed.py:open_batches/read/settle`.

An open call becomes an ordinary error row after the closing wait. The request still identifies its batch as `held`, so `_ledger` settles that batch as returned. `Budget.settle` removes its `out` markers, and `owed.settle` marks its spending reservation as belonging to an ended batch. A subsequent profile read can now clear that reservation. Nothing canceled or completed the outstanding connector operation.

The handoff's reading 1 says a later read is known to follow the outstanding call and that a late result would tell the brain the same thing. That does not hold when the mutation itself is still pending, rather than just its reply being delayed.

Reproduced with the real hooks/client/brain and the existing AP2 spending fixture:

1. Start with 49,820,000 ryo already spent, 180,000 remaining under the daily cap, and 400,000 in pocket. The brain plans 180,000 of purchases.
2. Allow the first `item.buy`, costing 165,000, and keep it in flight. Do not commit its game-side effect or return its result yet.
3. Run `brain next`. After the 120-second wait it submits `NO_ANSWER`; the old batch is no longer `out` or `loose`. Its 180,000 reservation has the ended marker `[batch, 180000, true]`.
4. Execute the next reads against the still-unchanged profile and stock, then hand them in. The brain plans another 180,000 of purchases, although the original 165,000 operation is still outstanding.
5. Return the old success. It is stored in `late/` and not applied to the brain.

```json
{"pending_purchase":165000,"old_batch_still_out_or_loose":false,"new_purchase":180000,"remaining_daily_allowance":180000,"old_result_delivered":false}
```

The admitted exposure is 345,000 against 180,000 remaining. If both sets complete, spending reaches 50,165,000. The fixture changes no admission or spending code; it supplies the delayed connector operation and intervening reads. A server guarantee that every operation has finished before this timeout could change the conclusion, but no such guarantee or cancellation/completion evidence is implemented or supplied.

Correction: distinguish **closed to new admissions** from **all admitted operations completed**. Keep unresolved mutation exposure and equipment invalidation until completion/cancellation is established, or a reconciliation read is known to follow completion. A synthetic error must not by itself retire that exposure. Preserve receipt idempotence; do not replay an old raw response into the next batch as an expedient fix. Readings 1 and 2 cannot be approved together as implemented.

**R2 — High: replacement does not participate in the lock protecting the final admission check.**

Locations: [`player/hook.py:171–175`](https://github.com/perseverance484/tnr-tools/blob/ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844/player/hook.py#L171) and [`player/brain/client.py:187–195`](https://github.com/perseverance484/tnr-tools/blob/ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844/player/brain/client.py#L187).

The final `holding()` read and writing `call` are protected by `hook/lock`, but naming a replacement in `_greet` only holds `client.lock`. Those operations can run concurrently. Re-reading under a lock is insufficient when the writer uses a different lock.

Reproduction: let A take its first line and reach the final `holding()` read inside `hook/lock`. After the file has been read, start B through real `brain next` with no token; it writes the new relay identity without waiting for `hook/lock`. Resume A with the reading it just obtained. A writes `call` and returns `allow` after B has been named.

```json
{"current_relay":"replacement","old_call_allowed":true,"old_call_recorded_after_replacement":true,"replacement_named":true}
```

This is not the unavoidable interval between an already-granted permission and the host dispatching it. Even the code's own admission record is created after replacement. The new stale-reading test pauses at the *initial* read; its final read observes B and denies. It misses a replacement between the final read and the admission write.

Correction: coordinate replacement and final admission using the same synchronization/ownership transition, with a documented lock order. Test replacement specifically after the final read and before writing `call`. Keep the distinction between newly admitted calls and calls already in flight when the replacement is named.

**R3 — Medium: cleanup is not idempotent; a post-answer retry deletes the identity of a call still in flight, then its real result is replaced by `ok` without storage.**

Locations: [`player/hooked.py:223–256`](https://github.com/perseverance484/tnr-tools/blob/ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844/player/hooked.py#L223), `client.py:238–240`, and `hook.py:197–199,258–267`.

`consumed` derives the set of open calls from `T.closed`. Its first invocation preserves those calls' `T.n.json` files but deletes `T.closed` itself. If the same token is consumed again, there is no closure record, the open set becomes empty, and the preserved call files are deleted. `_exchange` calls `_taken` again when resuming a pending answer, including when `handed == token`.

Reproduction:

1. Allow a call, keep its result outstanding, and let the batch close with that call `open` after the wait.
2. Let the brain answer and let `_taken` complete. Crash the client immediately afterward, before it prints the pending batch. At this point the pending answer and `handed` marker are saved; the open call's identity is correctly retained.
3. Retry the same `brain next`. It consumes the old token again and deletes the retained identity.
4. Deliver the original successful result. `_made` now returns `None`. `run("post")` still returns `updatedToolOutput: ok`; no inbox or late-result file is written.

```json
{"advanced":true,"open_claim_after_first_cleanup":true,"open_claim_after_retry":false,"model_shown":[{"type":"text","text":"ok"}],"late_result_stored":false,"puts":[]}
```

This happens immediately, not after the one-hour retention policy. The checked-in post-answer crash test uses a completed call, so there is no open record to lose.

Correction: make acknowledgement/cleanup safely repeatable, with durable unresolved-call identity that survives repeated consumption. Avoid rebuilding an empty closure/snapshot merely because an acknowledged token's files were cleaned. Also only suppress a successful tool output when its result was actually accepted or retained; `end is None` is not evidence of storage. Test crashes both before and after cleanup with an open call, and the eventual success/failure callback.

**R4 — Medium: `shown` is treated as finished before the transcript spool necessarily contains the result.**

Locations: [`player/hook.py:220–224`](https://github.com/perseverance484/tnr-tools/blob/ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844/player/hook.py#L220), and `player/hooked.py:109–117,192–219`.

On a failed result-file write, `_shown` marks the line before the post hook returns. `ended` treats `shown` as terminal, so a concurrent Bash hook can close immediately. `handed_in` looks once for the tool-use ID in the transcript, substitutes `NO_ANSWER` if it is not there, and freezes that row. `_transcript` waits for a transcript containing the `brain next` token, not for the missing result block. That token may already exist because the calls and `brain next` were emitted in the same message.

Reproduced by giving the transcript the stand-in and final Bash tool-use blocks, injecting one `relay.put` failure, and delaying the host's result append until after `brain next`. The hook correctly returns no output replacement. Nevertheless the brain immediately receives `NO_ANSWER`, and consumption deletes the call identity. The original response then appears in the transcript but has no delivery/recovery path.

```json
{"waited":0,"advanced":true,"brain_data":null,"original_claim_retained":false,"result_now_in_transcript":true}
```

The same schedule with `PostToolUseFailure` and `Too Many Requests` delivers generic `NO_ANSWER` instead of `rate_limited`, losing the failure classification. This is a confirmed local schedule; the actual Claude Code transcript-flush ordering remains unverified. The fallback tests pre-populate the complete transcript before starting `next`, and so do not cover it.

Correction: distinguish “left visible for the host to record” from “durably recoverable from the transcript.” Do not acknowledge/delete a `shown` outcome until its matching result block is available, or retain an explicit unresolved recovery state and identity for later collection. Use a bounded recovery policy without declaring a still-pending spool write permanently consumed. A transcript can be the fallback store, but the current one-shot lookup does not make it a reliable spool.

**Disposition of the requested checks and the handoff's readings.**

| Area | Assessment |
|---|---|
| H1: stale hooks, cleanup, repeated calls | The original `_first` sweep is gone, and its exact first-read/replacement scenario now preserves B's claims and refuses the repeat. Atomic claim creation prevents ordinary duplicates. No cross-batch deletion by a hook was found. The broader replaced-relay admission claim still fails R2; cleanup still loses required identity in R3. |
| H2: early `next`, crashes, immutable retries, replacement | `T.closed` blocks further admissions, and `T.results` makes unacknowledged retries carry the same rows. The original before-answer crash/resident-answer/late-call scenario is fixed. Early `next` waits successfully for normally returning calls. These improvements do not settle outstanding operations safely (R1), make cleanup repeatable (R3), or ensure fallback results are available (R4). |
| H3: durable acceptance before `ok` | A raised persistence error now leaves the response visible; both success and failure recover when the transcript already contains the result. R3 still produces `ok` without storage for an actually admitted call. R4 loses delivery/classification without suppressing the response. |
| Parallel calls; 2 s / 120 s; 180 s / 300 s | Thirty runs of the committed five-process test passed. Claims made before waiting allow reversed startup order within the grace interval. Closure shares one 2-second missing-line budget and one 120-second open-line budget across the batch; each predecessor wait has its own budget. Nominal closure waits fit 180 s; 2 + 120 + up to 60 s of pacing fits 300 s. Actual durations also include scheduling/I/O/lock delay. Busy startup or long batches can still be cut, as disclosed. None of those numerical bounds establishes that a connector mutation has completed. |
| Reading 1: keep late results, do not apply them as the next batch | Keeping batch identity and avoiding stale replay into the current world model is appropriate. Treating an archive as sufficient acknowledgement/reconciliation is not: R1 disproves the stated reservation rationale, and R3 can lose the archive entry altogether. A replaced relay's results are also not guaranteed retained when its replacement is unhooked, as known limit 4 explicitly admits. This is a narrowed delivery contract, not an unqualified correction of “every result reaches the brain.” |
| Reading 2: hand in an error after 120 s and continue | Rejected as implemented by R1. A bounded wait can be reasonable, but a wait expiring is neither a completed operation nor a confirmed cancellation. Continuing other safe work must preserve unresolved exposure. |
| Reading 3: use the transcript as the spool | Reasonable storage choice only with verified availability and recovery semantics. Not sound as implemented; R4. Actual host behavior remains unverified. |
| Readings 4–7 | Closing before the request, even if the brain does not answer, is sound. Irrevocable missing-line decisions are a conservative ordering policy with a startup/liveness tradeoff. The 2/120-second choices do not authorize dropping unresolved effects. Leaving the historical RUL-157 entry unchanged while documenting the new design is appropriate. |
| Protocol 9 / predecessor 8 | Correctly bumped. The full suite actually runs `184ce648` as a predecessor, as well as `661f3f63`; no skips. Old pending/client/receipt state is not accepted as a current batch. This migration guard does not fix the within-version lifecycle findings. |
| Relabeled estimate | Accepted as a scenario estimate under the recorded proxy weights. Extra requests and warm/cold birth assumptions are now explicit and counted. Reproduced warm `4.96M / 2.42M / 0.41M / 0.14M`, cold `5.64M / 2.43M / 0.44M / 0.14M`. The additional-read count is inferred from `in/context`, all scenarios reuse it, and per-call growth/output and 5,000-token birth remain modeled. The table no longer presents the 27 batches as 27 observed requests. It is not measured hook-relay savings or independent evidence of subscription billing weights. |

The agent-file hook engine, real timeout/failure enforcement, actual transcript flush order and Duet's runtime remain unverified. This workspace has no `claude` executable. The new subprocess probe tests the local lifecycle under concurrency, not Claude Code's scheduler, front-matter registration, or `onFailure: block`. No live probe was attempted. The previous assessment of the narrow Bash grammar and explicit permission `allow` is unchanged, subject to the lifecycle defects above.

**Verification on the frozen target.**

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 618 tests passed, no skips, 60.206 seconds; includes the 70 hook tests and both predecessor versions. |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | All 30 runs passed: four calls in order, followed by closure, four results delivered; 0.58–0.67 s from first allowance to closing. |
| `python3 -W ignore::ResourceWarning /workspace/scratch/review_hook_rereview1.py` | Five deterministic adversarial reproductions passed their assertions: R1, R2, R3, R4 success and R4 failure. |
| `python3 docs/reviews/evidence/ai_player_hook_relay/estimate.py < /workspace/scratch/ap1-tokens.jsonl` | Reproduced the revised table. Input extracted from `112aadbd:state/player/dauntless/sessions/ap1_live/tokens.jsonl`. |
| `python3 scripts/player_allowlist.py check` and `report --check` | Passed; 93 endpoints, zero never-list violations; report current. |
| `python3 scripts/rulings_index.py --check` | Passed; 327 rulings, index current. |
| `git diff --check 184ce648 ec231943` | Passed. |
| Review-artifact guards: `git diff --cached --check`, `python3 scripts/check_no_real_name.py`, `python3 scripts/check_large_files.py` | Passed; zero prohibited-name hits and zero unallowed large files. |

The scratch harness is outside the repository and is not committed. It uses `Hooks` and `TwoRelays` from the checked-in tests, real client/brain/receipt logic, and mocked clocks/connector data. R1 does not patch the budget, gates or spending code. R2 inserts replacement after the final file read without replacing any admission decision. R3 raises only after the actual `_taken` has run. R4 injects a transient result-write failure and varies when the host transcript contains the result. These schedules were reproduced against this SHA, not carried over from the previous report.

For a compact reproduction of R3 from the repository root:

```python
import os
from unittest import mock
from player import hooked
from player.brain import client
from player.tests.test_hook_relay import Hooks, OK

h = Hooks()
h.start()
try:
    token, lines = h.first_batch()
    inp, real = h.sent(lines[0])
    original = client._taken
    class Died(Exception):
        pass
    def cleanup_then_die(*args):
        original(*args)
        raise Died()
    try:
        with mock.patch.object(client, "_taken", cleanup_then_die):
            h.next(token)
    except Died:
        pass
    claim = hooked.on_record(h.r.dir, token, "1.json")
    assert os.path.exists(claim)
    h.next(token)
    assert not os.path.exists(claim)  # Defect: still-out call identity disappeared.
    assert h.comes(inp, real) == OK
    assert not os.path.exists(hooked.late(h.r.dir, token, 1))
finally:
    h.doCleanups()
```

Next step: Fable corrects these transitions on its own branch and returns a new frozen SHA. Re-review admission/replacement synchronization, unresolved-operation accounting, repeatable acknowledgement/cleanup, receipt replay and fallback spooling together. Preserve the successful closure/snapshot fixes. No merge, live run, light-polls decision, or new implementation work is authorized by this report.
