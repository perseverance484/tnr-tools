# AI player operator preflight: first correction review

**Verdict: request changes.** B1's endpoint ceiling and B2's missing-log handling are corrected. B3's admission barrier is corrected, but process-group shutdown is not established by the implementation. B4's per-call and fresh-run evidence checks are corrected, but a failed child can still receive a passing verdict. Two medium-severity findings below block approval of this operator check; a separate detection limitation needs narrower wording or treatment.

Reviewed 2026-11-16 in `perseverance484/tnr-tools`:

- Frozen target: `fable/ai-player-hook-proof` @ `071ba1b1dcf6f28f7fadcf25b05af62d102daedd`.
- Previous target and verified merge base: `65974c0259f01afdfc8ccc20fa448af06009a0f5`.
- Scope: `git diff 65974c02 071ba1b1`, `AI_PLAYER_HOOK_PROOF_REREVIEW1_HANDOFF.md`, and the gate, preflight, stand-in, proof watchers, tests, and revised operator/evidence text on which it relies.
- Prior report: `docs/reviews/AI_PLAYER_RELAY_PREFLIGHT_REVIEW_20261114.md`, `chatgpt/review-ai-player-relay-preflight-20261114` @ `5d46d7ef`, findings B1–B4.
- Authority: RUL-2026-11-14-160 point 1; RUL-158 and RUL-159 retain the stand-in/live-gate distinction. Method: `docs/workflows/FABLE_REVIEW.md`, Engineering Auditor.
- Remote Fable head matched the frozen target at start and before publication. Observed `main`: `0626bbdeb4b46c95f400cf46682477746260366b`.
- Report branch: `chatgpt/review-ai-player-preflight-rereview1-20261116`, based on the target. Only this report is added. No implementation or Fable branch is changed.

**Zero live-game requests or writes.** No credentials used, Claude session started, or real connector launched. Neither preflight nor proof was executed against a real connector. Verification used local files, mocked sessions, the local fixture server, gate subprocesses, and inert Python processes.

## Disposition of B1–B4

| Prior finding | Disposition on 071ba1b1 |
| --- | --- |
| B1: guard mode is not a profile-only ceiling | **Closed for the gate's inspected policy.** The independent all-tool gate resolves stand-ins and accepts only own-profile reads, bounded to three. Guard mode is no longer the enforcement mechanism. |
| B2: missing stand-in log erases released-call evidence | **Original defect closed.** Logs are read independently; missing, unreadable, and malformed evidence are distinguished. Successful unmatched results and unanswered overdue releases are detected. See C3 for the narrower error-result limitation. |
| B3: byte-prefix init observer, no admission barrier, unverified shutdown | **Admission portion closed; shutdown remains open (C1).** Field-based init parsing and the closed-until-admitted gate address the original dispatch race. The new cleanup can still report success with a live descendant. |
| B4: partial/stale hook evidence or failed invocation can pass | **Partial coverage and stale-folder routes closed; failed-invocation route remains open (C2).** Per-ID evidence is materially stronger, but the status supplied to the verdict can be false. |

## C1 — Do not equate the group leader exiting with the process group ending

**Confirmed defect, medium severity; blocks approval.** `docs/reviews/evidence/ai_player_hook_relay/preflight.py:293–330`, especially lines 295 and 305–306; used by `session` at line 384.

On POSIX, `end` sends SIGTERM to the group only while the leader is alive. It then waits for **the leader**, and breaks out of the signal loop as soon as that process exits. A descendant which ignores SIGTERM therefore never receives the intended SIGKILL. If the leader already exited before `end` begins, no group signal is sent at all.

The subsequent PID checks cover only stand-ins named in readable `connected` rows. They do not establish that other descendants are gone. This matters particularly during startup failure or lost-log handling, where there can be no such row; it also applies to other session children even when the recorded stand-in has exited. `session` substitutes an empty list when the final game-log read fails, so that path cannot supply additional cleanup evidence.

**Independent reproduction using only inert local Python processes:** launch a parent in a new session/process group; it forks a child that ignores SIGTERM and sleeps. With no game-log rows, call the real `end(parent, [])`:

| Schedule | Result |
| --- | --- |
| Parent alive when `end` starts | Returns `True`; parent exits on group SIGTERM; child remains running, `/proc` state `S`. |
| Parent terminated and reaped before `end` starts | Returns `True`; child remains running, state `S`; no group signal was sent. |
| Positive control: a single ordinary sleeping process | Returns `True` and that process is terminated. |

The scratch harness killed the remaining groups in `finally`. No connector was involved. This is a demonstrated teardown/reporting defect, **not** a demonstrated escape from the endpoint gate or `--strict-mcp-config`.

**Smallest correction:** retain the known process-group identity and finish bounded group cleanup independently of the leader's status. Do not stop escalation just because `p.wait()` returned. Verify the relevant surviving descendants/group, keep the stand-in PID check as additional evidence, and return failure when shutdown cannot be established. Add real local subprocess tests for both schedules, including absent/unreadable monitoring evidence. The committed session tests replace `end` with a lambda returning true, so they cannot exercise this defect. Windows cleanup remains unverified and must not inherit a stronger claim from a POSIX fix.

## C2 — Complete call evidence must not conceal an already-failed child

**Confirmed defect, medium severity; blocks approval.** `preflight.py:368–375`, with `verdict` at lines 208–215 and `form` at lines 388–413.

The loop tests `done(gate, hooks, game)` before `p.poll()`. Whenever `done` is true, the `elif` containing the exit check is skipped, including during the 0.2-second completion delay. The loop can consequently assign `STOPPED` to a process that already exited by itself, including exit 1. Cleanup checks that the process ended but does not correct the terminal reason. `verdict` accepts that supplied reason and passes the form.

**Independent reproduction:** run the actual `form`, `session`, completion predicate, and verdict with fresh per-run files containing valid admission, three matching gate/came/answered/pre/post IDs, and four Bash-hook rows. Replace the child with a stub whose `poll()` already returns 1; stub cleanup as successful to isolate terminal-status handling. The form returns:

```json
{"the relay's hooks ran for every call": true,
 "how the session ended": "stopped after the check's calls",
 "why not": null}
```

The same happens with an already-exited code-0 child. All logs are created for this invocation, with its fresh nonce; stale files are not involved. The counterexample preserves the complete call evidence, so it does not dispute that those hooks ran. It disputes the stronger, explicit passing contract: **stopped by the check after its calls**, rather than an invocation that failed or ended independently. A failed CLI session must not silently become an approved operator preflight.

**Smallest correction:** observe and preserve independent child exit before selecting intentional-stop success, including during the completion delay. Carry the observed exit/termination result into the verdict rather than constructing a success label solely from logs. Continue to distinguish an intentional harness termination from an arbitrary nonzero child exit; blindly requiring exit 0 would reject the intended termination path. Add a loop/form test combining complete evidence with child exit 1, plus the existing incomplete-evidence and intentional-stop controls. The current failed-child loop test never satisfies `done`, while the verdict test injects a failure label directly; neither tests the combination above.

## C3 — An error result does not prove that a call was refused before dispatch

**Confirmed detection/claim limitation, low severity; not an additional approval blocker.** `preflight.py:181–204`, especially line 199; the general “a call was answered, and not by the stand-in” claims in the handoff and `PROOF.md`.

`astray` skips a gate-admitted call indefinitely when its tool result has `is_error: true`, even if there is no matching stand-in row. Its docstring reasons that such a call was refused downstream and “never went.” That is not established by the error flag: a server can receive a call and return an error too.

I launched only the local stand-in with a fresh nonce/log, verified one normal call's IDs, then set its control to `unseen: true` and `fail: ["profile.getUser"]`. It received the next request and answered with `isError: true` without logging that call. Passing that result to the real `astray` yielded no alarm even well beyond `LATE`. The committed test explicitly expects the same blanket exemption.

This does **not** bypass the gate's three-read bound, and the missing call evidence still prevents that run from satisfying the final verdict. However, the immediate unmatched-answer detector is narrower than the prose suggests and cannot certify that erroring calls never reached a connector. Either classify these as ambiguous/unmatched unless separate evidence establishes pre-dispatch refusal, or explicitly narrow the claims and diagnostic behavior. A permission refusal and a dispatched server error need separate tests if different handling is intended.

## Checks that hold

### Gate and admission

`prepare` supplies an independent `SessionStart` marker and `PreToolUse` matcher `.*` through `--settings`; the latter has `onFailure: block`. The hook emits a denial or no permission decision, never an allow that overrides another guard. Its first decision requires a nonempty admitted session ID equal to the incoming session ID. Before that, Bash, Agent/Task, and connector calls all take the refusal path. The inventory-only session is never given an `admitted` file and also receives `--tools ""`.

After admission, the Bash regex uses a full match for the specified `python3 -m player.brain next` command, optional batch token, and optional exact repository `cd`. Extra shell commands, flags, newlines, and other tools are rejected. Agent/Task permits one start of the named relay from the main agent in subagent form; the same gate log serializes that decision and the connector-call count. The gate does not enforce every optional Agent parameter or the prompt wording, but those do not expand its tool/endpoint allowance under the stated inherited-hook model.

For connector calls, `stands_for` resolves a stand-in using the current protocol-compatible held batch, matching token and valid integer call index; otherwise it inspects the requested endpoint/input directly. It accepts only `profile.getUser` with empty/omitted input. The hospital, travel, and battle fixtures correctly demonstrate that the brain may request more while this gate refuses it. An independent run of eight concurrent real gate processes admitted exactly three requests and denied five; no endpoint was dispatched by that test.

Init is parsed as JSON fields rather than a byte prefix. Admission requires the exact server/tool inventory, a nonempty session ID, this run's single connected nonce row, and a matching gate-start marker. The admitted file is atomically replaced. Missing admission evidence reaches the startup deadline without opening the gate. This fixes the original observer-only design under Claude Code's documented/assumed hook execution semantics. I did not independently run Claude Code to verify `onFailure` handling, hook registration, or strict MCP isolation on an installed real connector; the committed stand-in captures are evidence for the tested CLI/environment, not a new connected-machine experiment.

### Evidence, isolation, and stand-in

The ordinary preflight no longer runs `proof.py`. Only `--try` imports its agent-definition helpers; that mode forces the overall result to fail as evidence of agent-file registration. The default environment retains the terminal's variables but replaces the live/fights/output paths and disables the resident daemon; `--bare-env` uses the explicit allowlist. Sessions start in the repository root with the generated local stdio MCP configuration and `--strict-mcp-config`.

Fresh output directories refuse existing contents, closing the stale-log pass. The verdict requires exactly three distinct admitted IDs, consistent session/relay form, exactly one successful pre and post per call, matching stand-in came/answered IDs, and the expected hook coverage. Partial posts, another session's rows, duplicate IDs, fewer calls, failed stand-in answers, and an explicitly failed terminal status do not pass. C2 concerns how that status is produced, not these ID checks.

The nonce tool, `_meta["claudecode/toolUseId"]`, and connected PID are actually produced by the local server. An independent stdio exchange verified the nonce-named inventory and matching call IDs/PID. The server contains no network forwarding and remains intentionally permissive about endpoint names: it is not the firewall. A nonce tool is useful run-identification evidence, not an independent authentication proof against an adversarial server.

The login-shell check detects the tested `TNR_PLAYER_LIVE` override and refuses on a mismatch or launch/timeout error. As the source admits, it probes a shell like the session's, not that exact session shell; Windows skips it. I did not test the operator's real shell, startup files, environment, or trust state. This distinction must remain explicit.

### Proof watchers and documentation

`proof.py` now expressly excludes machines with the real connector and removes the `--own-env` path. It still runs the normal player's requested calls and has after-dispatch watchers, not this gate. I extracted and executed the actual nested watcher bodies offline: a released call with a missing game log stopped the fake process after just over two simulated seconds; an unreadable log stopped immediately; spaced unexpected init and malformed init stopped immediately; missing init stopped after 45.05 simulated seconds. This independently verifies the B2/B3 fixes there without starting proof or Claude.

`player/OPERATOR.md` now requires a reviewed preflight head and distinguishes the terminal check from a Claude session. `PROOF.md` and the handoff correctly withdraw the guard-mode safety argument and disclose the untested operator environment, real connector, agent-file-hook success, and Windows path. Their endpoint-ceiling and admission descriptions match the inspected gate. Their group-ending and “stopped by the check” claims need C1/C2 corrected; their unmatched-answer language needs C3's qualification. Nothing in this review demonstrates that the real connector was reached or authorizes a live gate.

## Verification

| Command/check on the frozen target | Result |
| --- | --- |
| `python3 -m unittest -v docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | **30 tests, OK**, 10.310 s. No Claude or real connector. |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | Exit 0; local fixture server only. |
| `PYTHONPATH=. python3 /workspace/scratch/preflight_rereview_checks.py` | **6 checks, OK**, 0.146 s. Includes assertions reproducing C1/C2/C3, cleanup control, concurrent gate bound, nonce/ID/PID exchange, and both actual proof watcher bodies. “OK” means the stated observed behaviors reproduced, not that the target is defect-free. |
| `git diff --check 65974c02 071ba1b1` | Passed. |
| `git diff 65974c02 071ba1b1 -- player .claude` | Only `player/OPERATOR.md`; ordinary player code, tests, and relay agent unchanged. No duplicate player-suite run was needed for this harness-only correction. |
| Publication checks: staged whitespace, `check_no_real_name.py --commits 65974c02..HEAD`, `check_large_files.py`, `rulings_index.py --check` | Passed: 0 name hits, 0 disallowed large files, 330 rulings and current index. File scans cover populated sparse-checkout files, including the report, not absent files. |

Scratch tests are outside the repository and not committed. Source SHA-256: `e5122683c6c73113b4cbb2ad6de8ce2427482049aee87742166cebb78d0f4fd6`. They do not launch a Claude executable. C1 uses real isolated POSIX groups; C2 uses mocked session/process boundaries with the real form/loop/verdict; C3 and metadata checks use only the local stand-in. Historical model-run counts and the author's planted-defect counts were inspected as reported evidence, not independently rerun.

## Next step

Fable should correct C1 and C2, resolve C3's overstatement or ambiguous-error handling, add the missing combined failure-path tests, and return a new frozen SHA. Re-review can remain focused on cleanup, terminal status, error-result detection, and their affected claims/tests. B1 and the corrected admission/per-ID mechanisms need not be redesigned. The previously approved relay-refusal correction is separate; it does not clear these preflight defects. This head is not yet approved for the operator's connected-machine check.
