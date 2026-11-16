# AI player operator preflight: second correction review

**Verdict: request changes.** The original C1 schedules and C2 loop-order defect are corrected, but both findings remain open at narrower shutdown boundaries. C3 is closed. The non-POSIX refusal is sound. Two medium-severity defects below block approval of the operator check.

Reviewed 2026-11-16 in `perseverance484/tnr-tools`:

- Frozen target: `fable/ai-player-hook-proof` @ `c2efaaa266c8668a3440cb9340f98aeeea6bb3c5`.
- Correction base and verified merge base: `aa73867c53b1f7ab7a8577d0402e7195d43f0824`, the approved relay-refusal head.
- Previously reviewed preflight: `071ba1b1dcf6f28f7fadcf25b05af62d102daedd`; report `docs/reviews/AI_PLAYER_PREFLIGHT_REREVIEW1_REVIEW_20261116.md` on `chatgpt/review-ai-player-preflight-rereview1-20261116` @ `1e238719`.
- Verified the four preflight files (`preflight.py`, `preflight_gate.py`, `fake_connector.py`, `test_preflight.py`) are byte-identical between `071ba1b1` and `aa73867c`. The fast-forward base change does not conceal a different preflight implementation.
- Scope: `git diff aa73867c c2efaaa2`, the second correction handoff, affected tests and claims, and their unchanged dependencies. Authority: RUL-2026-11-14-160 point 1 and RUL-2026-11-14-161 point 3. Review method: `docs/workflows/FABLE_REVIEW.md`, Engineering Auditor.
- Remote Fable head matched the frozen target at start and before publication. Observed `main`: `0626bbdeb4b46c95f400cf46682477746260366b`.
- Report branch: `chatgpt/review-ai-player-preflight-rereview2-20261116`, based on the frozen target. Only this report is added; no implementation or Fable branch changed.

**Zero live-game requests or writes.** No credentials used, Claude session started, or real connector launched. Neither preflight nor proof was run against a real connector. The tests used temporary files, local fixture processes, and inert Python processes.

## C1 remains open: descendants observed during the wait are not remembered

**Confirmed defect, medium severity.** `docs/reviews/evidence/ai_player_hook_relay/preflight.py:343–370`, particularly the contrast between `known |= left` at line 357 and the waiting loop at lines 364–369.

The initial family scan before each signal updates `known`. Scans inside the waiting loop do not. A new descendant can therefore appear in a genuine process snapshot while its parent is still part of the session, leave the original group, and then be lost once its parent exits. The next scan can make `end()` return `True` although that child remains running.

This is **not** the handoff's disclosed limit of a detached/reparented process which was never observed while related. The reproduction explicitly observes the child in `processes()` output and verifies that `family()` includes it before its parent is gone.

Offline reproduction with real inert POSIX processes:

1. Start a parent as leader of a new session/process group. Initially it has no child.
2. Run the real `end(parent, [])`. Its first snapshot remembers the parent and it sends group SIGTERM.
3. The parent's SIGTERM handler starts a sleeping child in a separate session and waits for a local marker before exiting.
4. During the first waiting-loop scan, capture real `ps` output containing the child with `ppid=parent.pid`, `pgid=child.pid`. Verify that the child is in the session family. Release the parent and wait for it to exit before returning that snapshot to `end`.
5. That iteration sees a nonempty family and continues. The following real snapshot contains the live orphan child, now parented to PID 1, but `known` still contains only the original parent. `end` returns **True**, while the child is in state **Ss**, not a zombie.

The scratch wrapper controls the timing of real process snapshots; it does not fabricate their rows or replace the cleanup algorithm. Its `finally` block kills any remaining fixture groups. A local shutdown handler starting a child is a coverage schedule, not a claim that a recorded Claude session did this or that a connector was reached.

**Smallest correction:** update retained family membership from every snapshot, including every wait iteration, before testing for completion. Do this regardless of whether the leader has exited. Then use the retained identities for escalation and completion checks. Add a real-process test where the child appears after the initial signal scan and is observed before reparenting. The six new cleanup tests cover children present at the initial scan; they do not cover this transition.

`processes()` and `family()` otherwise handle the reviewed static snapshots appropriately: scan failure cannot become success, the original group remains discoverable after its leader exits, previously retained IDs and their descendants are traversed, and zombies are excluded from “running.” The original two C1 schedules now pass. The remaining problem is when `end` updates its retained set, not those original cases.

## C2 remains open: the final running check precedes a blocking process scan

**Confirmed defect, medium severity.** `preflight.py:425–428`, together with `end` at lines 353–360 and `processes` at lines 319–321.

The loop now checks `p.poll()` before `done`, and `session` checks it again immediately before calling `end`. That closes the previously reproduced already-exited and completion-delay cases. However, it is not a check immediately before the first signal as claimed: `end` first runs `ps`, with a timeout of up to 20 seconds. If the session exits independently during that scan, `end` never revises the saved `running=True`. It can find everything gone and return true. `session` then returns `Ended(STOPPED, ..., gone=True, running=True, code=1)`, which `verdict` accepts.

Independent offline reproduction used the actual `form`, `session`, `end`, and verdict with a real inert child:

1. Create complete, fresh three-call evidence through the existing fixture shape, with this run's nonce and the child's actual PID. Only the CLI launch is substituted with that local Python child; no Claude executable is run.
2. Keep the child alive through the loop and `session`'s final poll.
3. In the first cleanup `processes()` call, release a local marker that lets the child exit with code 1, wait for that exit, then obtain real `ps` output.
4. At the first attempted group signal the child's exit code is already 1 and its group no longer exists. The real `end` returns true and the form passes:

```json
{"the relay's hooks ran for every call": true,
 "how the session ended": "stopped after the check's calls",
 "it ended with": 1,
 "why not": null}
```

This is an ordinary asynchronous-exit interval around a blocking subprocess call, not a requirement to eliminate an infinitesimal poll/signal race. The child was running when cleanup was entered, but had ended by itself before any termination signal could be delivered. The evidence still proves the three fixture calls' hook coverage; it does not satisfy the explicit requirement that the check stopped a running session.

**Smallest correction:** establish and return the termination observation at the signaling boundary inside cleanup, after the potentially blocking preparation/scan. Propagate an independently observed exit to `session`/`Ended` rather than preserving the earlier `running` flag. Add this scan-time-exit case through the actual cleanup and verdict. Preserve the distinction between intentional termination and arbitrary failure; simply requiring exit 0 would be wrong for the intended SIGTERM path. Existing tests replace `end`, so their additional polls cannot exercise this interval.

## C3 closed: a recorded pre-hook refusal is different from an error result

`astray` now fails an admitted call with an unmatched error result unless the relay's log contains a nonempty refusal from the **pre** hook for that exact tool-use ID. Missing hooks, a passing pre hook, a post-hook refusal, and another call's refusal do not qualify. Successful unmatched answers still fail, and no-result/no-row calls retain the deadline.

This exemption is sound within the existing trusted hook-log and unique tool-use-ID model. I inspected `player/hook.py:243–255`: a pre-hook refusal is logged on the same path that returns `permissionDecision: deny`; it is evidence from before dispatch rather than an inference from a server's error. A supplemental check ran that real hook, verified its denial and matching log row, then confirmed that only that ID was exempted; another ID's error and successful result both triggered the appropriate unmatched-call alarm. The committed stand-in test independently demonstrates that an actual unlogged server error now fails.

No stronger assumption about hostile log editing, reused tool-use IDs, or a CLI ignoring hook denials is introduced by this review. Those are outside the preflight's established model. A refused call also does not supply the complete came/answered/pre/post evidence needed for a passing verdict.

## Platform, tests, and revised claims

- **Non-POSIX start refusal is sound.** `main` rejects before creating the run folder, self-testing the connector, probing the shell, or launching a session. The offline test checks exit 2, `started: false`, and no subprocess launches. Windows cleanup and shell-skip branches are removed. Linux was tested; macOS remains explicitly untested.
- **The 41 tests pass.** The added real-process cases close the original C1 schedules, cover an initially discoverable detached child and a logged stand-in PID, and test unobservable/unkillable cases and graceful termination. The form tests close the original C2 loop-order defect, including exits during the completion delay; the inventory-only session now requires independent exit 0. The two remaining schedules above cross boundaries those tests do not exercise.
- **Fixture restoration is improved.** The loop tests restore the recorded original time, Popen, run, and end functions rather than a previous nested setup's substitutes. Real cleanup tests are no longer relying on an accidental leftover end stub.
- **B1, admission, and per-ID mechanisms are unchanged.** `preflight_gate.py`, `fake_connector.py`, and `proof.py` are unchanged from `aa73867c`; ordinary player code and `.claude` files are unchanged. The approved refusal remains part of the base. No repeat full-player-suite run was necessary for this correction.
- **Documentation:** the operator's instruction to report either an unmatched answer or an ambiguous error now matches C3, and the Windows refusal matches the code. The unconditional whole-family-gone and running-when-stopped claims in the preflight text, `PROOF.md`, and handoff still need the C1/C2 corrections. `PROOF.md` also says **39 tests**, while this head actually has **41**; update that stale count when correcting the findings. It is not an approval blocker by itself.
- **Limits:** the disclosed never-observed detached/reparented descendant limit remains distinct from the observed-but-forgotten C1 defect. The operator's own environment, connected-machine strict MCP behavior, actual agent-file-hook success, and macOS were not exercised here. The committed `preflight3/a` and `j` outputs support the reported stand-in outcomes; they do not rule out these additional schedules or constitute a live authorization.

## Verification

| Command/check on c2efaaa2 | Result |
| --- | --- |
| `python3 -m unittest -v docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | **41 tests, OK**, 18.090 s; no skips. Real local fixture/process tests included; no Claude session. |
| `PYTHONPATH=. python3 /workspace/scratch/preflight_rereview2_checks.py` | **3 checks, OK**, 0.221 s: actual pre-refusal exemption and two assertions reproducing the remaining C1/C2 defects. “OK” confirms those observed behaviors, not approval of the target. |
| `git diff --exit-code 071ba1b1 aa73867c --` the four preflight files | Passed: byte-identical across the base change. |
| `git diff --check aa73867c c2efaaa2` | Passed. |
| `git diff --name-only aa73867c c2efaaa2 -- player .claude` | Only `player/OPERATOR.md`. |
| Publication checks: staged whitespace, `check_no_real_name.py --commits aa73867c..HEAD`, `check_large_files.py`, `rulings_index.py --check` | Passed: 0 name hits, 0 disallowed large files, 331 rulings and current index. File scans cover populated sparse-checkout files, including this report, not absent files. |

Scratch source is outside the repository and not published, per review workflow. SHA-256: `8c89fa8abe303c0c21499b93afad0a192486266d4b0348f3b92948f553742aac`. The two process reproductions synchronize genuine inert child exits and genuine system snapshots; no live/game transport is present. All fixture children are terminated in cleanup. Author-reported model sessions and planted-defect runs were not rerun.

## Next step

Fable should retain descendants seen in every shutdown scan, move the terminal-state observation to the actual signaling boundary, add these two failure-path tests, and return a new frozen SHA. C3, the non-POSIX refusal, the approved relay-refusal base, and unchanged gate/admission/per-ID logic do not need redesign. This head is not yet approved for the operator's connected-machine check or cleared as the combined reviewed head for the live gate.
