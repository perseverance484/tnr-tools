# AI player relay refusal: frozen review

**Verdict: request changes.** The default refusal and preservation of a running relay are sound on entry, but a waiting invocation can still print calls after permission is withdrawn. The new operator text also omits a step needed before `stopped` can acknowledge the refused relay's batch.

Reviewed 2026-11-14 in `perseverance484/tnr-tools`:

- Target: `fable/ai-player-relay-refusal` @ `9c2955bae4a1c681f7bf14de8f7ad57675cbf1d8`.
- Base and verified merge base: `071ba1b1dcf6f28f7fadcf25b05af62d102daedd` (`fable/ai-player-hook-proof`).
- Scope: `git diff 071ba1b1 9c2955ba`, handoff note, RUL-2026-11-14-161, and the unchanged client/accounting paths those changes depend on.
- Remote target and base still matched those SHAs before publication. `main` was `6dac21bbcf9740730d6f104dad26567b4740844b`.
- Report branch: `chatgpt/review-ai-player-relay-refusal-20261114`, based on the target. No implementation or Fable branch changed.

**This is not the separate re-review of the preflight correction at 071ba1b1.** Running its offline tests as a regression check here does not approve that base for use on the connected operator machine. No live gate or operator preflight was run. Zero live-game requests, writes, or credentials used; no Claude session or real connector started.

## Findings

### R1 — Recheck permission after waiting, before publishing the batch

**Confirmed defect, medium severity; blocks approval.** Target locations: `player/brain/client.py:141-145,150-172`; `player/hooked.py:221-225`.

`bare()` is called once, before `_greet` and `_exchange`. The latter can wait for a brain response; afterward `next_batch` releases the client lock and spends the batch's pacing delay. When it reacquires the lock, it checks relay ownership, pending batch identity, and lease expiry, but does not check `relay_without_hooks` again. It then marks the batch issued and prints the real calls to the hookless relay.

Offline reproduction on the frozen target:

1. Use a fresh `Rig(mode="guard", bare=False)` with a healthy AWAKE profile already saved.
2. Set `relay_without_hooks=true`; obtain the hookless relay's name/token.
3. Request its next batch. During the normal seven-second wait, after `client.json.pending` exists, set `relay_without_hooks=false` using `console.set_control`.
4. The invocation still prints `profile.getUser` and advances to a new held batch. A subsequent invocation returns `hooked.BARE`.

Deleting `control.json` or replacing it with malformed JSON during that same wait produces the same escaped batch. All three cases were reproduced using the real client/brain code, a fixture profile, and an injected sleep callback. No calls were dispatched. The positive control confirms that a *fresh invocation* refuses a previously saved protocol-10 pending batch when the setting is false, leaving the client bytes unchanged.

The rule works at invocation entry, but not at the moment the batch is printed. This contradicts the handoff's rationale that the condition is checked “where a batch is printed, every time,” and fails the requested invariant that a batch cannot still be printed when the setting is not true. The existing revocation test changes the setting **between** invocations; it does not cover revocation while one is waiting. The operator phrase “at its next `brain next`” describes that narrower behavior, but does not establish the stronger printing guarantee used in the handoff.

**Smallest correction:** retain the early check so a refused newcomer cannot replace anyone, and add a current-policy check on the final publication path after the wait and ownership checks, before changing `pending` to `held` or writing calls. Preserve superseded-relay precedence and pending/unprinted accounting. Add tests for withdrawal while awaiting the brain and during the pacing wait, including a saved pending batch, with a hooked-relay positive control. A protocol bump alone cannot fix withdrawal during a running invocation.

### R2 — The documented `stopped` recovery needs a replacement first

**Confirmed operator-documentation defect, medium severity.** Target location: `player/OPERATOR.md:136-139`; related unchanged implementation: `player/brain/client.py:309-348` (`stopped`, `_held`). The handoff and the new revocation test make the same unsupported “until the operator says stopped” claim.

When permission is withdrawn from an already named hookless relay, `bare()` returns without touching `client.json`. This deliberately preserves its `held` batch. However, `brain stopped` lists batches in `gone` or the saved ledger's `loose` rows; it does not accept the still-current relay's held batch.

Reproduction: let a hookless relay receive one batch under the explicit true setting, set false, let it receive the BARE stop line, then run the real `brain.stopped` function against that fixture directory:

| Command | Result immediately after refusal |
| --- | --- |
| `brain stopped` | Empty listing |
| `brain stopped TOKEN` | `stopped: []`, token in `not_held` |
| `brain stopped BATCH_ID` | `stopped: []`, batch ID in `not_held` |
| `brain stopped all` | `stopped: []` |

The client still held the original batch. After naming a hooked replacement, that batch moved to `gone`, and the same `stopped TOKEN` succeeded. This is safe conservative accounting, not evidence of an uncounted call or a reason to loosen `stopped`'s safeguards. The defect is that the new recovery instruction does not explain the required ordering. The nine new tests check that `held` remains but never actually perform the claimed stopped operation in this case.

**Smallest correction:** document the complete sequence: confirm the refused relay has ended, name a replacement with working hooks so the old batch becomes listable, then acknowledge the old token/batch with `stopped` and let the replacement convey that acknowledgment to the brain. If immediate acknowledgment without replacement is intended instead, that requires an explicit state/accounting change and review; do not silently mark the batch completed merely because a STOP line was printed. Add a test of the documented sequence.

## Answers to the six review questions

| Question | Conclusion |
| --- | --- |
| 1. Any hookless printing path left without true? | **Yes: R1**, when true is withdrawn after the entry check and before publication. With no permission at entry, new and current hookless relays are refused. Wrong/stale tokens either get the existing superseded response or a retry command; they do not directly print game-call batches. |
| 2. Is a running relay untouched by refusal of a newcomer? | **Yes.** The short circuit precedes `_greet`, so it cannot rename the relay, move its held batch to gone, collect results, submit a request, or replace a pending batch. I snapshotted persistent fixture-file bytes, refused an unstamped newcomer, and found them unchanged (excluding lock files); the active hooked relay then completed its batch and obtained another. Creating an inbox directory and taking the client lock are not ownership changes. |
| 3. Do replaced relays and relays losing hooks keep their old responses? | **Yes, on the reviewed paths.** `mine` requires the current token and a state without hooks. A replaced relay therefore reaches unchanged `_greet`/`hooked.back`, receives `SUPERSEDED`, and records its batch's return as before. A relay named with hooks but arriving without its stamp reaches unchanged `hooked.stop` and receives `NO_HOOKS`, even when the override is true. A stale token from the same relay still gets the prior retry line. |
| 4. Keep protocol 10? | **Yes for on-disk compatibility; the “checked at printing every time” justification needs R1 fixed.** No request/receipt/ledger shape, accounting meaning, pacing rule, or hook ownership rule changed. The new requirement is a current delivery policy that can be applied to an old protocol-10 pending batch without interpreting that batch differently. I verified refusal of such a pending batch on a fresh invocation. Changing the number does not solve the timing hole. This does not claim that an old binary already executing acquires the new check; the established update procedure still requires ending old processes. |
| 5. Do the fixture changes weaken existing tests? | **No existing assertion or tested legacy invariant was found weakened.** They opt legacy scenarios into the supported hookless mode so the tests still reach their original recovery/accounting paths. Details and limits below. The new refusal tests omit the R1/R2 cases. |
| 6. Operator subagent start and refusal text? | **Subagent instructions match RUL-161**: Agent tool, `subagent_type="tnr-relay"`, prompt `Begin.`, and preflight `--form subagent`. The refusal text correctly distinguishes a newcomer from a relay that lost hooks; its displayed prefix matches the actual BARE line, which also adds the OPERATOR reference. Clarify the newcomer scope of “no name,” since an existing refused relay retains its name, and fix the recovery sequence in R2. |

The stored setting is false by default. `bare` permits only literal JSON `true`; numeric 1, strings, other container shapes, missing files, and malformed JSON fail closed on entry. `console.SETTINGS` validates the setting as boolean when applying it, and `brain set` persists it in the usual control document. The client deliberately consults the file directly, so revocation between invocations does not wait for another brain tick. A nonempty hook stamp is the existing trusted-hook convention, not a new authentication mechanism; this delta does not redesign it.

## Fixture audit

- `support.Rig(..., bare=True)` is an intentional test default, **not** the production default. It writes the control override and marks it already applied at version 0 in the fixture world. `ARelayWithoutHooksIsTurnedAway.start` explicitly constructs `Rig(..., bare=False)`, so its new default-refusal cases do not inherit that permission.
- `support.bare(live)` writes only the version-0 override. I checked the caller contexts: the copied historical fixtures contain no control document; callers needing pause or other versioned settings subsequently write those settings as before. No held/gone/pending/receipt/ledger record is erased or rewritten by this helper.
- `support.and_bare(settings)` retains the supplied version and all other fields while adding the override. The five changed complete-file writes still apply their original mode/pause changes; they do not reset those controls.
- The edit inside `test_rereview9.OLD_ASLEEP` supplies the override immediately before launching the new code. Without it, the newly introduced refusal would prevent the upgrade test from reaching its original replacement path. Version 0 matches the old fixture world's already-applied control version, so it does not create a new setting event in the old process. The old process must still return exactly `SUPERSEDED`, new relays must still receive no calls during the takeover hold, and the 30-call hold assertions remain.
- An AST comparison of every changed test file found **zero removed or changed assertion expressions**; the nine new hook-relay tests add 32. This supplements, rather than replaces, inspection of the altered setups. Duplicate imports added inside `OLD_RESIDENT` are harmless.
- Limitation for future tests: `Rig.new_brain()` assigns the fixture's `self.bare` to the world after loading it, so that helper is not evidence for persistence of this setting across a restart. Test that new behavior using the production `Brain` and explicit control files, rather than assuming a default Rig models it. No existing test asserted persistence of this newly introduced field.

The small `proof.py` delta enables the override only for `--hooks none` unless `--no-word` is supplied. It does not change the preflight's agent-hook mode. The added historical-proof annotation correctly explains that the prior hookless runs predate this refusal. No proof session was rerun for this review.

## Verification and limitations

All tests ran against the exact target except the explicitly labeled base control. The player suite uses local fixtures and temporary live directories; the preflight test module uses a stand-in process, not Claude or the real connector.

| Check | Result |
| --- | --- |
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | Initial run: 645 tests, one failure in `TheCommandLine.test_a_relays_brain_next_starts_the_resident_by_itself`, final lock-release assertion at line 141; no skips. Full rerun: **645 tests, OK**, 65.097 s, no skips. |
| Focused rerun of that test on target | 1 test, OK, 1.339 s |
| Same focused test on base 071ba1b1 | 1 test, OK, 1.389 s |
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | 30 tests, OK, 10.293 s; regression evidence only, not the base's separate review |
| `python3 -W ignore::ResourceWarning /workspace/scratch/review_refusal.py` | All assertions passed: three in-flight withdrawal reproductions, stopped-command failure and replacement control, saved protocol-10 pending refusal, and byte-preserving newcomer refusal with continued hooked play |
| AST assertion comparison, base to target | Zero removed/changed assertions in changed test files; 32 added |
| `git diff --check 071ba1b1 HEAD` | Exit 0 |
| `python3 scripts/rulings_index.py --check` | Exit 0; 331 rulings, current index |

The initial process test failure occurred after the test could no longer find its daemon in `/proc` but before it could reacquire the lock. The production resident/lock implementation and the test's process-disappearance/lock assertions are unchanged in this delta. The focused passes do not prove its cause; it is recorded as intermittent verification evidence, not a confirmed refusal regression.

The scratch script is not committed, per `docs/workflows/FABLE_REVIEW.md`. SHA-256: `90d2cca5cb5abca3fe08764923b905a4f8e8aa976d8102f9db060c23a78a6e6d`. It uses the actual `next_batch` path through the existing offline hook-test fixture, injects only the clock/sleep and local settings changes, and calls no model/connector. The key R1 schedule is reproducible from the target root with:

```python
from player.tests.test_hook_relay import ARelayWithoutHooksIsTurnedAway
from player.tests.support import user
t = ARelayWithoutHooksIsTurnedAway()
try:
    t.start(mode="guard")
    t.r.world.absorb([user()._replace(at=t.r.t)])
    t.r.world.save()
    t.says(relay_without_hooks=True)
    token = t.next(hooked=False)[0]
    original_sleep = t.sleep
    def withdraw(seconds):
        if seconds > 1 and t.client().get("pending"):
            t.says(relay_without_hooks=False)
        original_sleep(seconds)
    t.sleep = withdraw
    print(t.next(token, hooked=False)[1])  # includes profile.getUser
finally:
    t.doCleanups()
```

## Next step

Fable should fix the final publication check and the operator recovery sequence on its own branch, add the missing failure-path tests, and return a new frozen SHA. A focused re-review can cover those changes plus their pending/held accounting interactions; wider changes to protocol or ownership would require a wider check. The separate review of 071ba1b1 and the operator's stand-in preflight remain prerequisites to the director's live gate.
