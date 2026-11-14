# AI player hook relay — independent third re-review

**Verdict: APPROVED for the reviewed code. R5 is closed. No blocking finding remains in this correction.** Completion evidence now survives client reloads until a request carrying it is acknowledged. The previously approved lifecycle changes are preserved.

Reviewed 2026-11-14, repository `perseverance484/tnr-tools`, Lane A.

| Ref | Commit |
|---|---|
| Frozen target, `fable/ai-player-hook-relay` | `51fac81d712b65936dba14bf340ac957975da3e4` |
| Code commit | `a2eba13900ccb9e2607f4bfab33cb3c84b98e979` |
| Base / verified merge-base | `b5624861c9dee3f0acdc2ce48385057fcf4eedc8` |
| `main` observed during review | `589214c89d341b90575ab51f7ada097c1ab9ce14` |
| Report branch, based on the frozen target | `chatgpt/review-ai-player-hook-relay-rereview3` |

Scope: `git diff b5624861 51fac81d`. The diff is exactly the `_a_word` predicate and its docstring, three tests, and the third correction handoff. The previous report at `9c7b67ed` is evidence only and was not merged. This is a focused correction review; no wider assumption or lifecycle implementation changed.

Zero live requests, no game-source execution, no credentials, no implementation edits, and no changes to `fable/*`.

## 1. R5: completion evidence survives until acknowledgement

[`player/brain/client.py:113`](https://github.com/perseverance484/tnr-tools/blob/51fac81d712b65936dba14bf340ac957975da3e4/player/brain/client.py#L113) now accepts `"answered"` alongside `"back"` and `"stopped"`. It preserves the existing record-shape checks and still rejects an unknown completion kind. This fixes the precise producer/reader mismatch: `hooked.account` creates the record, `_who` retains it, and the brain's existing evidence consumer accepts it.

I reran both prior schedules against the native fixed validator, without the validator override used as a control in the previous review. I also exercised replacement, both lease-expiry paths, and receipt replay:

| Schedule | Observed result |
|---|---|
| A: late result arrives; completion request receives no answer; retry | The saved `answered` row survives `_who`, appears in the retried request, and releases the old batch's four loose calls. The original 180,000 reservation no longer remains held through later reads. The new checked-in spending test also verifies the actual 165,000 spend and the subsequent reconciliation, leaving 15,000 of the allowance. |
| B: brain answers; cleanup finishes; client dies before printing; late result arrives; retry reuses pending answer | No new brain request is made while the pending batch is printed. The completion row remains in `client.json` through that print and reaches the brain with the next request. The old batch is then no longer loose. |
| A new relay is named while the completion request is unanswered | `_greet` carries the pending completion word into the replacement's state. The replacement's request delivers it and clears the old hold. |
| A new relay is named while completion evidence waits with a pending answer | Naming and printing preserve the word without prematurely clearing it. A returning superseded relay also leaves it intact. The replacement's next request delivers it. |
| Pending batch's lease has expired before `_exchange` | `_owed` gives up the pending batch, preserves `ended`, and carries both the completion word and the abandoned batch's `unprinted` ID in the new request. The old completed batch's hold is released. |
| Lease expires during the wait before printing | The second `_who` retains the word. `given_up` removes the expired pending batch without printing its calls and preserves completion evidence. The following request delivers the word and the abandoned batch's identity. |
| Brain consumes completion, then client dies before recording the answer | The row remains available for retry. Receipt replay accepts the same completion evidence safely, and the client clears it after receiving the answer. The completed batch does not become loose again. |

The code agrees with these results: replacement explicitly carries `ended`; printing does not clear it; `runlock.given_up` changes only the pending batch, sequence and `unprinted`; and `_exchange` clears `ended` after receiving the brain's answer to the request that carried it. Reusing an already pending answer skips that clearing operation. The existing client lock serializes these client-state changes. The receipt path separately accepts completion evidence even when it reuses an earlier answer.

Within the supported current-protocol file lifecycle, I found no remaining path that discards this word before acknowledgement. This conclusion does not extend to deletion/corruption of the client file or a protocol replacement; those retain their separate conservative takeover semantics.

## 2. Other fields written by `hooked.py`

I inspected every mutation of client state in `hooked.py` against `_who` and its validators, beyond the new test's two collections.

| Producer | Client-state change | Reader behavior |
|---|---|---|
| `stop` | `seen = True` | Preserved by `_who`. |
| `account` | `held = None`; append the held batch to `gone` with `closed = True` | `None` remains `None`; `_a_batch` validates the string token/id and preserves the entire dictionary, including the marker. |
| `account` | Remove completed entry from `gone`; append `[id, timestamp, token, "answered"]` | Now accepted by `_a_word` and preserved exactly. |
| `back` with an outstanding call | `back = True` on the existing `gone` entry | Extra dictionary fields are preserved by `_a_batch`. |
| `back` with no outstanding call | Remove entry from `gone`; append completion kind `"back"` | Already accepted and preserved. |

There is no other client-state writer in `hooked.py`. Hook-related fields owned by the client (`hooks`, `handed`, `steps`, `until`, and the valid held/pending batch records) also survive `_who` in the shapes that this code writes. Their intentional replacement when a new relay is named is not a filtering loss.

`WhatIsKeptOfABatch.test_what_is_put_down_of_a_batch_is_read_back_as_it_was_written` covers the two `gone` markers, all three completion kinds, and rejection of an unknown kind. It passes. No second producer/reader mismatch was found.

## 3. Previously approved behavior is preserved

Verified byte-for-byte unchanged from `b5624861`: `player/hooked.py`, `player/hook.py`, `player/relay.py`, `player/budget.py`, `player/owed.py`, `player/brain/core.py`, `player/brain/resident.py`, `player/runlock.py`, and `.claude/agents/tnr-relay.md`.

Thus closure, immutable saved result rows, unresolved-call exposure, repeatable cleanup, synchronized replacement, result suppression only after storage, and inbox/folder/transcript fallback retain the implementation reviewed last time. The full suite reruns their regression cases. Protocol remains 10; this fix makes its existing completion record readable rather than changing its meaning.

The narrower late-result contract remains acceptable: retain the payload with its original batch, deliver durable completion evidence, and reconcile current state through eligible subsequent reads. R5 no longer prevents that evidence from surviving retries. I also read RUL-2026-11-14-158 and -159 on the separate proof branch (`fable/ai-player-hook-proof`, observed at `2c3c1bc90a544d700aedb2f10973079e2dfefd68`); point 3 and automatic permission for the brain's admitted calls are now explicit director decisions there. Those rulings were not merged into this frozen target or this report branch.

## Verification and remaining limits

| Check on the frozen target | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 634 tests passed, no skips, 61.097 s; includes 86 hook tests and the predecessor-version cases. |
| `python3 -W ignore::ResourceWarning /workspace/scratch/review_hook_rereview3.py` | All seven schedules above passed. The first two reuse the previous scratch reproductions with success expectations and no validator patch; the other five exercise the additional transitions. |
| Exact diff / merge-base / unchanged-file checks; `git diff --check b5624861 51fac81d` | Passed; only the three declared files changed. |
| `python3 scripts/rulings_index.py --check` | Passed: 327 rulings; index current on this target. |
| Report guards: `git diff --cached --check`, `python3 scripts/check_no_real_name.py`, `python3 scripts/check_large_files.py` | Passed: zero prohibited-name hits and zero unallowed large files. |

The scratch harness is outside the repository and is not committed. It uses temporary rehearsal folders, the checked-in hook/spending fixtures and the real client, brain and ledger. It injects no-answer/crash schedules and gives temporary pending batches cutoff times to exercise lease expiry. It neither contacts the connector nor invokes a live run-lock operation. The old helper's output label `validator_control: true` denotes its success expectation in this run; no validator substitution is installed.

The author's repeated suites, mutation campaign, fuzz scripts and separate process probe were not rerun as independent campaigns for this one-line correction. The full suite and the targeted schedules above are the fresh verification reported here.

Actual Claude Code agent-file hook registration, timeout/failure enforcement, transcript ordering and Duet's runtime remain outside this code review's proof. The next step is the already directed local proof against a stand-in connector. This approval does not claim that proof or the subsequent AP1 live gate has passed. No merge, local hook-engine proof or live run was performed in this review.
