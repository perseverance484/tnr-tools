# AI player operator preflight: third correction review

**Verdict: approved for the reviewed preflight corrections. C1 and C2 are closed.** No new blocking finding was found. C3, the non-POSIX refusal, and the previously accepted gate/admission/per-ID mechanisms remain accepted. This clears the code-review gate for this frozen preflight; it does not substitute for a successful operator-machine check or establish live-session performance.

Reviewed 2026-11-16 in `perseverance484/tnr-tools`:

- Frozen target: `fable/ai-player-hook-proof` @ `e6686d39735a6065dd53afa7c402725878cfed60`.
- Previous target, correction base, and verified merge base: `c2efaaa266c8668a3440cb9340f98aeeea6bb3c5`.
- Prior report: `docs/reviews/AI_PLAYER_PREFLIGHT_REREVIEW2_REVIEW_20261116.md` on `chatgpt/review-ai-player-preflight-rereview2-20261116` @ `eefb063e`, C1 and C2 still open.
- Scope: `git diff c2efaaa2 e6686d39`, the third correction handoff, shutdown/family/termination paths, tests, and revised claims. Authority: RUL-2026-11-14-160 point 1 and RUL-2026-11-14-161 point 3. Method: `docs/workflows/FABLE_REVIEW.md`, Engineering Auditor.
- Remote Fable head matched the frozen target at start and before publication. Observed `main`: `28fc1e70721e5632f30327026b2175c00892ac12`.
- Report branch: `chatgpt/review-ai-player-preflight-rereview3-20261116`, anchored to the frozen target. Only this report is added; no implementation or Fable branch changed.

**Zero live-game requests or writes.** No credentials used, Claude session launched, or real connector started. Neither preflight nor proof was run against a real connector. Tests used temporary files, the local fixture server, intercepted signal calls, and inert local Python processes.

## C1 — Closed: every shutdown snapshot updates the retained family

`docs/reviews/evidence/ai_player_hook_relay/preflight.py:375–395` now uses one scan/remember/signal/wait loop for each signal phase. Every successful snapshot contributes `left` to `known` before any completion decision. Thus a descendant observed during a wait remains discoverable by its own PID after it changes group or loses its parent.

The group is signalled once per phase, independently of whether its leader has exited. Newly observed members receive the current phase's signal immediately. `told` avoids repeatedly signalling the same members within that phase and resets for SIGKILL escalation. An unsuccessful scan returns `gone=False`; unsuccessful termination cannot produce success while the process remains in the observed family. Success requires both a finished leader and an empty running family. Zombies are appropriately treated as exited, not as processes able to continue making calls.

I reran the previous review's independent real-process schedule with corrected assertions: the leader initially has no child; its SIGTERM handler starts a child in a separate session; a genuine wait-loop snapshot observes that child while related; the parent exits before the next snapshot. The real `end` now returns `(True, True)` only after the child is terminated. The final process snapshot showed the child as a zombie, rather than the running `Ss` state observed on the previous target.

The committed version deliberately makes that child ignore SIGTERM, so it tests retention through escalation rather than succeeding merely because the first request happened to end it. A separate committed test confirms that a newly observed cooperative child is asked to end immediately, without waiting for the SIGKILL phase. The earlier leader-alive, leader-already-exited, detached-child, recorded-stand-in, failed-signal, failed-scan, and graceful-termination cases also pass.

I found no path in the reviewed loop that declares a retained, still-running session member gone while it remains represented in the system's process table. The disclosed limit remains: a descendant which detaches and is reparented without ever being observed as related cannot be discovered by ancestry polling alone. That is distinct from the observed-but-forgotten defect, now fixed. The recorded stand-in PID supplies an additional explicit root for that process. The scan interval is 0.1 seconds **plus the process scan's execution time**, not a hard 10 Hz guarantee.

## C2 — Closed: cleanup supplies the observation at the signalling step

`end` captures `running` after its first process scan and family calculation, immediately before its completion/signal decisions. No blocking subprocess call remains between that observation and the first signal. `session` no longer keeps its own earlier flag: it uses the returned `(gone, running)`, translates a proposed `STOPPED` into `BY_ITSELF` when cleanup found the leader already exited, and constructs `Ended` from that result. The verdict still requires intentional-stop status, a running leader at that step, and successful cleanup.

The independent reproduction runs the actual form/session/end/verdict with complete fresh call evidence and a real inert child in place of Claude. The child exits with code 1 while the first cleanup scan is being obtained. On this target, no group signal is attempted after that completed exit; the form returns false, reports `the session ended by itself`, records exit 1, and gives the corresponding failure reason. On the previous target this same schedule passed as `STOPPED`.

The committed test also includes the matching positive control: the same evidence with a child which remains alive until signalled passes and records `-SIGTERM`. The existing tests cover exit 0 and exit 1 before completion or during its brief delay, and require successful independent exit 0 for the inventory-only session. Intentional termination is correctly not constrained to exit 0; the committed Claude stand-in captures record 143.

This addresses the blocking scan-time race identified by the review. It does not claim an atomic operating-system transaction spanning a liveness poll and signal delivery. The remaining instruction-level asynchronous-exit interval is the explicitly accepted boundary from the prior review, not the former potentially seconds-long scan interval.

## Family protection — Sound for the process-table model used here

`family` starts its exclusion set with PIDs 0 and 1, then walks this program's ancestry in the supplied process table. It subtracts those identities both from the initial leader/known seeds and from each expansion. Therefore a protected PID supplied through a bad connected-log row is neither returned as a target nor used as an ancestry root to collect unrelated descendants. A protected PID cannot re-enter merely through a matching group number.

Supplemental synthetic-table checks cover this process, its parent and grandparent, PID 1, PID 0, and combinations of those as log-derived seeds. They also check group-based re-entry and that an explicitly named ordinary child remains eligible. A separate test runs `end` with those bad log PIDs and intercepted signals: only the actual fixture session's process group receives SIGTERM; no protected PID or sibling receives an individual signal. No real ancestor was signalled during testing.

The direct group signal is rooted in the trusted `Popen` PID of a session launched with `start_new_session=True`, not in a log-provided group number. That invariant is important to the protection. This is a guard against sweeping up this program, its ancestors, and their unrelated descendants from erroneous log seeds; it is not authentication of every arbitrary PID in a tampered log. It relies on the system's process table for the ancestry information, as the rest of cleanup does. Within that stated model, I found no missing seed or expansion path around the exclusion.

## Claims, unchanged surfaces, and limits

- `PROOF.md` now gives the correct **44-test** count and describes the remembered descendants and signalling-time observation. Its explicit never-observed detached-descendant limitation matches the implementation. The preflight text and handoff agree on the same boundaries.
- `preflight_gate.py`, `fake_connector.py`, `proof.py`, player code, `.claude`, and `player/OPERATOR.md` are unchanged in this correction. The prior C3 closure and non-POSIX startup refusal remain applicable. The approved hook-relay and relay-refusal implementations are still part of this head; no separate player behavior change is introduced here.
- The new tests exercise the previous actual failures through real local processes. The switch from a boolean cleanup result to `(gone, running)` is reflected in the older assertions and the loop's cleanup stub. No previous failure condition was found weakened by that adaptation.
- The committed `preflight4` outputs still distinguish diagnostic `--try` success from agent-file registration: supplied-hook forms pass individually but the overall agent-file claim remains false; the untrusted-folder run fails. Those are author-run stand-in captures, not newly run Claude sessions from this review.
- The operator's own environment, a machine with the real connector, successful registration of the agent file's own hooks, and macOS remain unverified here. Windows remains refused. Strict MCP configuration and the CLI's hook semantics remain the prevention assumptions established in the earlier reviews; these cleanup changes do not prove a new transport-isolation guarantee.

## Verification

| Command/check on e6686d39 | Result |
| --- | --- |
| `python3 -m unittest -v docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | **44 tests, OK**, 20.855 s; no skips. Includes real local process and stand-in cases. |
| `PYTHONPATH=. python3 /workspace/scratch/preflight_rereview3_checks.py` | **5 checks, OK**, 1.247 s: both previous independent shutdown reproductions with corrected expectations, deep ancestor exclusion, intercepted signal-target verification, and the actual pre-hook-refusal exemption control. |
| `git diff --check c2efaaa2 e6686d39` | Passed. |
| Unchanged-surface comparisons | No changes to the gate, fake connector, proof harness, player code, agent files, or repository review/authority instructions. No duplicate full-player-suite run was necessary for this correction. |
| Publication checks: staged whitespace, `check_no_real_name.py --commits c2efaaa2..HEAD`, `check_large_files.py`, `rulings_index.py --check` | Passed: 0 name hits, 0 disallowed large files, 331 rulings and current index. File scans cover populated sparse-checkout files, including this report, not absent files. |

Scratch source is outside the repository and not published, per the review workflow. SHA-256: `be4300eba4411cd77e963066c83c502e39dacd379fef580b235aa9981593a3c5`. The C1/C2 checks adapt the prior independent reproductions rather than relying only on the newly committed tests. Fixture processes are cleaned up; the ancestor checks never signal real system ancestors. Author-reported model-session and planted-defect runs were not independently repeated.

## Next step

No further correction is requested for C1 or C2. This frozen head has passed the code review required before the operator-machine preflight. The operator must still run the normal subagent preflight from the trusted repository folder and obtain exit 0 with the agent file's own hooks before beginning live play. A `--try` result does not meet that requirement. No operator-machine check or live hunt was started by this review.
