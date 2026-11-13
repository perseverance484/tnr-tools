# AI player hook relay — independent Lane A review

**Verdict: REQUEST CHANGES.** Two high-severity defects break duplicate-call prevention and result delivery. A third, medium-severity defect deliberately discards a result when its local handoff fails. The sequential happy path works, but it does not establish the requested invariants under concurrent execution, replacement, or interruption.

Reviewed 2026-11-13. Repository: `perseverance484/tnr-tools`.

| Ref | Exact commit |
|---|---|
| Frozen target, `fable/ai-player-hook-relay` | `184ce648a0268c8e4b280f280392938b6ee371ac` |
| Approved base / verified merge-base | `661f3f63f9bd51887c402ce00f76e8e9735cb2ea` |
| `origin/main` observed at review start | `d637346156935fee457361e35a264ce786086acf` |
| Publication branch | `chatgpt/review-ai-player-hook-relay`, based on the frozen target |

Scope is `git diff 661f3f63 184ce648`, the handoff, the committed probe evidence, and the surrounding client/brain/ledger paths needed to check the seven requested invariants. Authority: RUL-2026-11-13-157, judged under RUL-2026-11-13-156; the design's sections 4.6–4.7; the approved player brief; and the review request. No implementation changes, no changes to a `fable/*` branch, no integration, no live-game requests or writes, and no live credentials/session material used. Repository access and publication only used GitHub. The probe's earlier live request was not repeated.

**H1 — High / confirmed defect: a delayed old hook deletes the current batch's duplicate-call protection.**

Locations on the frozen target: [`player/hook.py:92–105`](https://github.com/perseverance484/tnr-tools/blob/184ce648a0268c8e4b280f280392938b6ee371ac/player/hook.py#L92), and `release` at lines 230–241.

`release` reads `client.json`, then calls `_first` using that snapshot, before checking ownership. `_first` deletes every other batch's hook files. It is not synchronized with client replacement or other hooks. The atomic hard link in `_mine` only prevents duplicates while its claim file remains present.

Deterministic reproduction against the real hook and client code, using the existing socket-free `Hooks` fixture:

1. Relay A holds its first batch. Pause its first `pre` after `holding` returns, immediately before `_first`.
2. Relay B replaces A, obtains a batch through the real `brain next`, and completes its first call. B's claim file exists.
3. Resume A. Its `_first(A-token)` deletes B's claim and `.seen` files. A is eventually denied by the final ownership check, but that does not undo the deletion.
4. Repeat B's already-completed first stand-in. B's hook allows it again. The mock connector records two identical calls.

Observed output:

```json
{"old_refused":"that batch is another relay's","claim_before":true,"claim_after":false,"repeat_allowed":true,"game_calls":2}
```

This is a violation of the no-repeat invariant, not merely a refused stale call. The reproduction uses `profile.getUser`; the deleted claim is the same mechanism protecting purchases, actions, and every other endpoint. A repeated mutation would have only one planned call/reservation behind it. The second `_may` does not repair this: it checks ownership, token and cutoff, not whether another process removed the current batch's claims.

Smallest robust correction: stop allowing an individual hook with an old snapshot to delete other batches' live claims. Coordinate claim lifetime/cleanup with client generation changes under a shared synchronization rule, or retain per-batch claims until cleanup can prove no live hook needs them. Rechecking once before an unlocked deletion is insufficient. Add a deterministic replacement/interleaving test that attempts the current call again after the stale hook resumes.

**H2 — High / confirmed defect: `brain next` can close a batch while its hooks are still producing results; receipt replay then loses late results too.**

Locations: [`player/brain/client.py:31–59`](https://github.com/perseverance484/tnr-tools/blob/184ce648a0268c8e4b280f280392938b6ee371ac/player/brain/client.py#L31), `_exchange` at lines 208–240; [`player/hook.py:248–270`](https://github.com/perseverance484/tnr-tools/blob/184ce648a0268c8e4b280f280392938b6ee371ac/player/hook.py#L248). The agent instructions at `.claude/agents/tnr-relay.md:42–47` put connector calls and the final Bash `brain next` in one message.

There is no batch-completion barrier between these tools. The Bash hook validates and stamps a command immediately. `_collect` takes whatever files exist at that instant; `_exchange` can then mark the batch handed in and advance the token. `answered` only searches the *current* token's claims. An allowed old call's later result is therefore rejected, even though its tool-use ID was recorded correctly.

Reproduction A:

1. Obtain the first batch and run its real `pre` to `allow`, without delivering its connector result yet.
2. Run the final `brain next` for that token. It returns a new batch.
3. Deliver the original successful result to `answered`.

```json
{"batch_advanced":true,"late_result_taken":false,"results_at_brain":0}
```

The `.seen` marker is already present, so the missing-hook check does not stop this. The client lock serializes `brain next` processes with each other; hooks do not participate in it. The checked-in tests execute each complete pre/call/post sequence before running `next`, so their same-game comparison does not exercise this schedule. Actual Claude Code scheduling on Duet's machine remains unverified; the implementation failure for the schedule explicitly raised in this review is locally confirmed.

Reproduction B covers a `brain next` that dies **before the brain answers**:

1. Obtain a four-call batch and complete call 1.
2. Let `_exchange` persist its request, containing only result 1. Raise at entry to `brain._await`, simulating the client dying before an answer.
3. Have the resident brain serve that persisted request normally. It saves a receipt for that relay/sequence.
4. Complete call 2. The hook permits this because the client still has no `handed` marker. Its result file exists.
5. Retry `brain next`. The new request contains both results. `resident._answered` reuses the prior receipt for the same relay/sequence and does not absorb result 2. `_taken` nevertheless deletes result 2 with the other files.

```json
{"request_result_counts":[1,2],"retry_absorbed":[],"late_result_deleted":true,"late_endpoint":"travel.getSectorData"}
```

Receipt deduplication is doing its existing job: it avoids applying result 1 twice. The new asynchronous producer violates its assumption that a retry's result set is unchanged. Do not remove that deduplication to fix this.

Smallest robust correction: define and persist a closed batch/result snapshot before submitting it to the brain, coordinate it with hook admission and in-flight calls, and acknowledge/delete only results actually consumed. Bind result identity durably to batch/call rather than finding it only through the current client token. In-flight outcomes must remain deliverable across replacement and retries; an unresolved call must not silently become a completed batch. Test both schedules above, plus replacement while a result is in flight. A prompt instruction alone does not enforce the requested contract.

**H3 — Medium / confirmed defect, disclosed in the handoff: a failed post-hook handoff still replaces the only result with `ok`.**

Location: [`player/hook.py:294–302`](https://github.com/perseverance484/tnr-tools/blob/184ce648a0268c8e4b280f280392938b6ee371ac/player/hook.py#L294).

After an allowed call, make `relay.put` raise `OSError` once. `run("post", ...)` catches the write failure, logs it if possible, and unconditionally returns `updatedToolOutput: ok`. Restore storage and run the next batch. The result is absent, the relay is not stopped, and the brain continues. Hooked transcripts are intentionally excluded as a result source, and the transcript now contains only `ok` anyway.

```json
{"model_shown":[{"type":"text","text":"ok"}],"results_at_brain":0,"batch_advanced":true,"stopped":false}
```

This is the handoff's known limit 8, reproduced rather than treated as accepted. It fails the request that every result reach the brain exactly once, including failure paths. A connector mutation may have succeeded; a diagnostic log about failed delivery is not its result or a durable recovery mechanism.

Smallest robust correction: only suppress a result after durable acceptance; provide a recoverable result spool or explicit failed-delivery state that prevents normal continuation until the outcome is preserved/reconciled. Cover successful responses and `PostToolUseFailure`. If loss on this path is intentionally accepted, it needs an explicit exception to the requested contract and an operator recovery procedure. No such exception was supplied for this review.

**Coverage of the seven requested checks.**

| Check | Assessment |
|---|---|
| 1. Only the next authorized call; repeats, stale calls, identity, replacement, lease, failed hooks | Sequential validation rejects malformed stand-ins, wrong batches/agents, handed-in batches, duplicate claims, missing predecessors, and calls at/after a finite cutoff. It rechecks after waits. Python exceptions in `pre` return `deny`. H1 breaks duplicate prevention under replacement. Host enforcement of process failure/timeout is unverified; see below. |
| 2. Results once, correct call, failures, oversized results, interrupted `next` | Normal correlation by tool-use ID and batch index works; the tested string/text-block/content-wrapper forms, error strings, rate limits and saved-output paths work. H2 and H3 prevent an exactly-once approval. A control with an unchanged result set survives a client death before an answer: one result is delivered on retry and deleted only afterward. |
| 3. Unhooked behavior and immutable relay kind; hooks never ran | Unhooked formatting/collection remains equivalent apart from protocol and added usage fields. A current token with a changed/missing hook identity stops; adding hooks to an existing unhooked relay stops. The first nonempty hooked batch with no `.seen` mark stops before more calls are printed. Starting without a token creates a new relay, rather than changing an existing relay's kind. |
| 4. Waits and simultaneous tool starts | Sequential calls spend their assigned waits once, including the 1.2-second action gap. `_turn` waits up to 30 seconds for a predecessor result **only if its claim already exists**; a predecessor whose hook has not claimed yet causes immediate refusal. Thus concurrent startup can truncate a legitimate batch depending on scheduling, and long predecessor waits/results can also exceed the 30-second budget. Refusal preserves order but does not establish reliable parallel progress. H2 additionally covers the final Bash call running early. |
| 5. `allow` and Bash command check | The hook explicitly grants permission to the rewritten brain call and to the permitted `brain next`; it does not defer approval to the normal prompt. That is consistent with the stated play-session interpretation of RUL-157, conditional on fixing admission/lifecycle defects. The anchored command pattern rejects shell suffixes, extra flags, substitutions, `put`, `set`, and `stopped`; stamped IDs are constrained. A bare command assumes the documented repository-root working directory. The agent's two-tool list is also part of the boundary: `_stand_in` itself matches a `callEndpoint` suffix, not an exact server identity. |
| 6. Protocol 8 and old state | Correctly bumped from 7. The predecessor-package test actually executes base `661f3f63`, including old pending/receipt state. Old client state cannot print an old batch as current; old-token relays stop; old requests/receipts/ledger holds keep the established migration rules. This does not solve H2's within-version changing result snapshot. |
| 7. Token estimate and log fields | `in` remains total prompt tokens; `cached` and `written` are its components, not extra input to add again. Fresh input is `in - cached - written`. `hooks` identifies the collection mode. Existing rows may lack the new components; unavailable usage is not a measured zero. The table reproduces, but its exact ratios remain modeled, not measured plan savings; qualifications below. |

**Token-estimate qualification — low severity / needs refinement.**

The committed script reproduces `4.84M / 2.42M / 0.41M / 0.14M` and a hooked end context of `29,600` on `112aadbd`'s log. The probe supports replacing a large successful result with a small stub, which is the principal saving. It does not measure a real hook relay's per-batch request count or birth context.

At `estimate.py:52–61`, each row is modeled as one request using its final `context`, ignoring the row's total `in`. The first two source rows actually have `in/context` of `233342/118190` and `237730/119141`: 233,741 additional prompt tokens across those two rows are omitted from the input model. Consequently “27 of 27 requests” is a modeled batch count, not the actual observed request count. The script also initializes/resets `new=0`, treating a newly born relay's whole initial context as cached. That warm-cache assumption needs labeling or cold-start accounting. The final 15,000-token growth, 5,000-token birth size and per-batch call counts are assumptions, as the script partly documents.

Keep the table labeled as a scenario estimate and fix or explain the request-count and cache-birth assumptions before using the ratios as acceptance evidence. The actual subscription weights are unpublished according to RUL-156; this review checked the committed calculation under those stated proxy weights, not independently verified provider billing. The new log fields are useful and in scope; they permit a better calculation once real hook-relay request data exists. No conclusion here requires reopening the separate light-polls branch.

**Runtime limits of the evidence.**

The committed probe on Claude Code 2.1.323 establishes one successful MCP input substitution and output replacement from project settings. It does not establish agent-front-matter hook registration, `PostToolUseFailure` behavior, oversized-output behavior, concurrent dispatch, or `onFailure: block` under process failure/timeout. The agent-file tests inspect strings and execute the shell commands; they do not run the Claude Code hook engine. This workspace has no `claude` executable, and no live probe was attempted. Those claims remain unverified, not failed tests or proven runtime defects. A local fake connector/runtime probe would be appropriate after the code corrections, without spending a live-game request.

Normal pre-hook exceptions fail closed in Python. For a process that cannot start, exits abnormally, or times out, safety depends on the host honoring `onFailure: block`. A dropped post hook additionally threatens result delivery. The design's claim that the relay carries neither payload should remain qualified for failure/timeout paths until that behavior is tested.

**Verification.** All game behavior was provided by local fixtures/stubs and temporary rehearsal folders.

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | First run: 592 tests, one failure in unchanged `test_a_relays_brain_next_starts_the_resident_by_itself`, at the assertion that the terminated daemon's lock is free. Full rerun: all 592 passed, no skips (59.506 seconds). |
| `python3 -W ignore::ResourceWarning -m unittest player.tests.test_brain_package.TheCommandLine.test_a_relays_brain_next_starts_the_resident_by_itself` | 1 passed on isolated rerun. The initial shutdown race is not attributed to this diff. |
| `python3 -W ignore::ResourceWarning -m unittest player.tests.test_hook_relay` | 44 passed, including the real protocol-7 predecessor test; no skips. |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 passed; existing ResourceWarnings. |
| `python3 -m player.tests.test_walk 200 300` | 200 walks of 300 steps; 5,481 calls, zero walks with a problem. |
| `python3 scripts/player_allowlist.py check` | Passed; 93 endpoints, zero never-list violations. |
| `python3 scripts/player_allowlist.py report --check` | Passed; checked-in report current. |
| `python3 scripts/rulings_index.py --check` | Passed; 327 rulings, index current. |
| `git diff --check 661f3f63 184ce648` | Passed. |
| Review-artifact guards: `git diff --cached --check`, `python3 scripts/check_no_real_name.py`, `python3 scripts/check_large_files.py` | Passed; zero prohibited-name hits and zero unallowed large files. |
| `git show 112aadbd:state/player/dauntless/sessions/ap1_live/tokens.jsonl` piped to the committed `estimate.py` | Reproduced the published table; arithmetic qualifications above. |
| `python3 -W ignore::ResourceWarning /workspace/scratch/review_hook_relay.py` | Five deterministic checks: H1, both H2 schedules, H3, and successful unchanged-snapshot retry. All observed outcomes asserted. Scratch script is outside the repository and not committed. |

The adversarial checks use the existing `player.tests.test_hook_relay.Hooks` fixture, real `brain.next_batch`, hook admission and result code, and real `brain.serve`. The mocked seam in H1 only schedules replacement just before the stale `_first`; no admission check or file operation is replaced. H2's crash seam raises before `_await` starts; the saved request is subsequently served normally. H3 injects a single result-persistence error. They do not depend on game source or a network endpoint.

To reproduce H1 compactly from the repository root:

```python
from unittest import mock
from player import hook
from player.tests.test_hook_relay import Hooks, OK

h = Hooks()
h.start()
try:
    old_token, old_lines = h.first_batch()
    first, current = hook._first, {}
    def interleave(live, token):
        with mock.patch.object(hook, "_first", first):
            current["token"], current["lines"] = h.first_batch(agent="replacement")
            assert h.call(current["lines"][0], agent="replacement") == OK
        first(live, token)
    with mock.patch.object(hook, "_first", interleave):
        assert "another relay" in h.call(old_lines[0])
    assert h.call(current["lines"][0], agent="replacement") == OK
    assert len(h.game) == 2  # Expected invariant: the second call is refused.
finally:
    h.doCleanups()
```

**Next permitted step:** Fable corrects the lifecycle/claim defects on its own branch, adds adversarial tests, and returns a new frozen SHA. Re-review should cover hook admission, cleanup, result acknowledgement, receipt replay, and parallel dispatch together; H1/H2 cross those boundaries. This report is not authorization to merge, run the player live, or change the held light-polls work.
