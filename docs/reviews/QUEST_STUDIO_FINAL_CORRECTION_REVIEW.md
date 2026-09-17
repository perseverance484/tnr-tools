# Quest Studio — final correction re-review

**Reviewer role:** Independent Engineering Auditor
**Implementation owner:** ChatGPT
**Review target SHA:** `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`
(branch `chatgpt/forge-quest-studio-foundation`, "handoff: freeze final Quest Studio correction")
**Prior target:** `1f6a1097e33108d595ca27067a7240cf14b98ded`
**Prior review:** `claude/quest-studio-source-push-review@10658b817b51a77efcc18470ef8ef9b9e89e1dbe`
**Correction handoff:** `docs/handoffs/FORGE_QUEST_STUDIO_FINAL_CORRECTION_HANDOFF.md`
**Live game touched:** none. No live TNR request or write was made.
**ChatGPT branch modified:** no.

---

## 1. Verdict

**APPROVE_WITH_NONBLOCKING_FOLLOWUP**

F1, F2 and F5 are all closed. F1's closure was independently reproduced on a *different* Node
version from CI's, which is the specific thing that had to be proven — the prior discrepancy is
genuinely gone, not masked by runner behaviour. No prior finding regressed. Quest Studio is
accepted for integration planning.

Four non-blocking follow-ups (N1–N4) are recorded below. None gates integration planning; N1 and
N2 should be picked up during unified Forge implementation.

---

## 2. Correction scope

The diff from the prior target is surgical — 8 files, no `forge/src` change at all:

```
.github/workflows/quest_studio.yml                        +59
docs/RULINGS.md                                            1 line
docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md  1 line
docs/handoffs/FORGE_QUEST_STUDIO_FINAL_CORRECTION_HANDOFF.md  +125 (new)
forge/test/github.studio.test.mjs                          3
forge/test/quest.studio.ui.test.mjs                        3
skills/…/quest_worker_contract_test.py                     +4
dist/building-tnr-content.zip                              (regenerated)
```

`git diff --name-only 1f6a109 HEAD -- forge/src` is **empty**. Every browser-side protection is
therefore unchanged by construction, not merely by assertion.

---

## 3. Verification performed

All commands run in a clean checkout at the frozen SHA, **Node v22.22.2** (CI pins 24.20.0 —
version divergence is deliberate here, see F1).

| Command | Result |
|---|---|
| `npm ci` | rc=0 |
| `npm test` | **315 tests / 315 pass / 0 fail / 0 cancelled / 0 skipped** |
| `npm run fixtures` | rc=0 |
| `git diff --exit-code -- forge/test/fixtures/envelope` | **clean** |
| `npm run build` → `git status --porcelain forge_bundle.js` | **clean — bundle rebuilds without drift** (429.8 KB) |
| `npm audit --omit=dev --audit-level=high` | **found 0 vulnerabilities** |
| `quest_worker_contract_test.py` | rc=0 — *Quest Studio source-push trust boundary pinned* |
| `quest_compile.py --selftest` | **9 passed / 0 failed** |
| `quest_compile_integration_test.py` | rc=0, all PASS |
| `doctrinemap.py` | 21 assertions, 18 referenced, 16 surfaces — **0 err / 0 warn** |
| `render_doctrine.py --check` | **all projections current (exit 0)** |
| `build_packs.py --check` | **all packs and TOCs current (exit 0)** |
| `lawmap.py .` | 93 laws / 93 matrix rows / 77 citations across 38 files — **0 errors, 5 warnings** (pre-existing) |
| `git merge-base --is-ancestor origin/main HEAD` | false — **40 commits behind main** (known debt) |

Note on dependency debt: `npm audit --omit=dev` reports **zero** production vulnerabilities at this
SHA. Whatever advisories remain are dev-only. No Quest Studio exploit path identified; not treated
as a blocker, per instruction.

---

## 4. Disposition of prior findings

### F1 — **CLOSED**, independently reproduced

Both tests are now top-level declarations. The fix is a pure reordering: each swallowed test was
lifted out of its parent's body and placed before it, with the parent's `test(...)` header moved
down to sit directly on its own body. No assertions were changed, weakened or deleted — I diffed
the bodies, not just the counts.

Executed and observed passing by name in my own run:

```
ok 166 - QuestStudioRepository refuses build reads without an exact submitted source identity
ok 167 - QuestStudioRepository marks an older persisted result stale
ok 186 - editing a submitted Mission invalidates persisted build identity before reopen
ok 187 - real Mission profile sentinels render as awaiting ruling and block compile
```

This is the load-bearing evidence. My prior run at `1f6a109` gave **311/2/2 on Node 22**; the same
tree on Node 24 CI reported 315/0. That divergence was exactly what made the old number
untrustworthy. At `5ba636d` I get **315/315/0 on Node 22**, and CI reports 315/315/0 on Node 24.
The two runners now agree, and they agree on the number that includes both formerly cancelled
subtests running. The discrepancy is eliminated at the source, not hidden by runner behaviour.

### F2 — **CLOSED** as requested hardening

**Invariant stated in both durable surfaces.** `RUL-2026-09-16-002` and
`FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` now each carry it explicitly, with the correct
reasoning: push-triggered workflow definitions resolve from the pushed request ref, so Workflows
write on the browser credential would let it replace the worker definition on a request branch and
collapse the trusted-main compiler boundary. Both name it as an invariant rather than describing it
in passing.

**Worker check verified in the specified order.** Read directly from
`.github/workflows/quest_studio.yml`:

1. `Checkout trusted compiler` — `ref: main`, `path: tools`, `persist-credentials: false` ✓
2. `Resolve trusted compiler revision` — `git -C tools rev-parse HEAD` ✓
3. `Checkout pushed worker definition` — `ref: ${{ github.sha }}`, `path: request-definition`,
   `persist-credentials: false` ✓
4. `Verify worker definition matches trusted main` —
   `cmp --silent request-definition/.github/workflows/quest_studio.yml tools/.github/workflows/quest_studio.yml` ✓
5. fails closed, `exit 2`, under `set -euo pipefail` ✓ — a missing file on the pushed ref also fails
   `cmp`, so absence fails closed too
6. only then `Validate push identity` → `Checkout authored request source` → `Validate request
   content` → `Compile Quest Source` ✓

**Framing is correct and I do not overclaim it.** The comparison lives inside the workflow
definition that is itself resolved from the pushed ref, so a credential that already holds Workflows
write can delete the check along with everything else. It is not a substitute for the credential
invariant and the handoff, the ruling and the architecture doc all say so. What it *does* buy is
real: it catches accidental worker drift — most plausibly a request branch created from an older
`main` before a `quest_studio.yml` update — which is an operational failure mode that would
otherwise run stale worker logic silently. Meaningful defence in depth, correctly scoped.

`quest_worker_contract_test.py` pins the step name and the exact `cmp` invocation. See N1 for the
one gap in that pinning.

### F5 — **CLOSED**

Verified against the persistence path:

- `Persist build result to request branch` now carries
  `if: ${{ always() && steps.identity.outcome == 'success' }}` ✓
- if `build-result.json` is missing, the step synthesizes a structured envelope with
  `errors[0].code = "compiler_no_result"` ✓
- `provenance.sourceRevision` = `SOURCE_SHA` and `provenance.compilerRevision` = `COMPILER_SHA`
  (newly threaded into the step's env for exactly this) ✓
- `liveGameTouched: false` ✓
- persisted first, surfaced after — `Surface compiler failure` is a separate later step under the
  same condition ✓
- `RC="${COMPILE_RC:-4}"` — a missing `compile_rc` defaults to nonzero ✓
- persistence still `git add --` scoped to `studio/results/<id>.build.json` and
  `studio/builds/<id>` only ✓

**Invalid request identity cannot write results.** This is the specific risk the `always()` change
could have introduced, and it does not. The gate is `steps.identity.outcome == 'success'`, not bare
`always()`. If `Validate push identity` fails or never runs — malformed branch, bad request id,
non-40-hex SHA, or a worker-definition mismatch upstream of it — `outcome` is not `success`,
persistence is skipped, and nothing is written anywhere. The request-scoped paths are only ever
derived from an already-validated `REQUEST_ID`.

---

## 5. Regression check — none found

| Protection | Status |
|---|---|
| M1 source-push / Contents-only browser credential | intact — `forge/src` untouched since prior target |
| No browser `workflow_dispatch` path | `grep -rni dispatch forge/src forge_bundle.js` (minus `dispatchEvent`) → **empty** |
| Exact `sourceCommit` correlation | intact — `repository.mjs` unchanged; test 166 now actually proves it |
| Stale-result detection | intact — test 167 passes |
| Artifact-path confinement | intact — `generatedArtifactPath()` unchanged |
| `manifestSha256` binding | intact |
| Unresolved Mission profile fail-closed | `quest_compile --selftest` PASS |
| Failed-envelope request identity | integration test PASS |
| Mission profile-shape enforcement | integration test PASS; test 187 now actually executes |
| Generated manifest inspection | ui suite PASS |
| DOM sink hardening | suite PASS incl. no-socket and error-banner tests |
| Zero-live compiler boundary | contract test *worker has no live-game path* PASS; `validateBuildResult` still refuses `liveGameTouched !== false` |
| Source branch stale-head refusal | `[[ "$REMOTE_SHA" == "$SOURCE_SHA" ]]` present, exit 5 |
| Non-fast-forward stale-push refusal | intact |
| No `--force` | `grep -- "--force\|push -f\|+refs"` on the workflow → **empty** |
| No Forge runner/transport/budget/storage/reconcile change | `git diff --name-only … -- forge/src` → **empty** |

---

## 6. Non-blocking follow-ups

### N1 — the worker-definition check's *position* is pinned only by presence, not by order.

`quest_worker_contract_test.py` has a `require_order` chain, but it covers only:

```
Validate push identity → Checkout authored request source → Validate request content → Compile Quest Source
```

`Verify worker definition matches trusted main` is asserted present but is **not** in that chain.
A future edit could move the `cmp` step to after compilation and every gate would still pass, which
silently converts a pre-execution boundary check into a post-hoc one. One-line fix: prepend
`"name: Verify worker definition matches trusted main"` to the existing `require_order` list.

### N2 — stale request branches will fail closed with no evidence on the branch, and need a documented recovery.

`submit()` calls `ensureBranch(branch, main)`, which creates the branch once and never rebases it.
A request branch created before a `quest_studio.yml` update on `main` therefore carries the old
worker definition. On the next Compile the `cmp` fails, exit 2 — and because that happens *before*
`Validate push identity`, persistence is correctly skipped and **nothing lands on the request
branch**. Forge polls, finds no new result, and surfaces only a timeout with no structured cause.

The ordering is right — writing request-scoped paths before identity validation is exactly what
§3 of the brief asks us to prevent — so this is a deliberate tradeoff, not a defect. But the
operator-visible symptom is indistinguishable from a hung build. Recommend documenting the recovery
(delete and recreate the request branch after any `quest_studio.yml` change reaches `main`), and
considering whether Forge should surface workflow-run conclusion alongside result polling so a
fail-closed refusal is legible rather than silent.

### N3 — cosmetic: persist step assumes `request/` exists.

With `always()`, if `Checkout authored request source` fails after identity succeeded, the persist
step runs and `git -C request ls-remote` errors on a missing directory, producing a confusing
message rather than a clear one. No correctness impact — nothing can be written without a checkout
either way.

### N4 — carried: base drift and ledger reconciliation (prior F3).

Target is 40 commits behind `origin/main`; `grep -c RUL-2026-09-16-001 docs/RULINGS.md` on the
target returns **0**. Numbering remains collision-free. This stays an integration requirement.

---

## 7. Remaining integration requirements

Confirmed as requirements, not blockers for this slice:

1. **Base drift reconciled before integration**, deliberately rather than by blind merge.
2. **Both `RUL-2026-09-16-001` and `RUL-2026-09-16-002` must survive** that reconciliation.
3. **One repository-only end-to-end `studio/quest/*` rehearsal** after the reviewed seam exists on
   `main`, verifying: trigger fires on a source push; worker-definition equality passes; compiler
   SHA recorded in `provenance.compilerRevision`; artifacts land request-scoped only; a second
   source push supersedes the first; stale-build refusal fires when forced. **Zero live-game
   contact.**
4. N1 and N2 folded into unified Forge implementation.

---

## 8. Summary for the director

The corrections are clean and narrow. Nothing in Forge's source changed — only two test
declarations moved, the worker gained a fail-closed pre-flight, and the credential invariant got
written down in the two places that outlive this conversation.

The number that mattered is now true. Last time the handoff claimed 315/0 and my machine said
311/2/2; the two swallowed tests are the ones guarding exact source identity and edited-draft
invalidation, so that gap sat directly on the protections being signed off. This time I get 315/315
on a different Node version than CI, and both tests appear by name in the passing list. That is the
claim verified rather than repeated.

The workflow-definition check is honest about what it is. It cannot stop a credential that already
holds Workflows write — the check would go down with everything else — and the docs say so plainly
instead of overselling it. What it does stop is the realistic case: a request branch carrying a
stale worker definition and compiling under old rules without anyone noticing.

Two things to pick up later, neither urgent. The contract test pins that the check exists but not
that it runs first, so it could drift downstream unnoticed. And when the check does fire on a stale
branch, the operator sees a silent timeout rather than a reason — worth making legible before this
is in daily use.

Accepted for integration planning.
