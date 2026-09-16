# Quest Studio — final narrow source-push re-review

**Reviewer role:** Independent Engineering Auditor
**Implementation owner:** ChatGPT
**Review target SHA:** `1f6a1097e33108d595ca27067a7240cf14b98ded`
(branch `chatgpt/forge-quest-studio-foundation`, "handoff: freeze Quest Studio source-push correction", 2026-09-16 18:16:03 -0500)
**Base at review time:** `origin/main`; target is **not** a descendant of main and is **40 commits behind** it.
**Planning branch referenced:** `claude/forge-next-planning-v3frzi@22f1fc43f8e316d0ec8412d5595a7cd0936f98d0`
**Governing ruling:** RUL-2026-09-16-002
**Live game touched:** none. No live TNR request or write was made at any point in this review.
**Target branch modified:** no.

---

## 1. Verdict

**CORRECTIONS_REQUIRED** — narrowly, on F1 only.

M1 is closed cleanly and the source-push model does not weaken the repository/compiler trust
boundary. The blocker is not the transport design; it is that the recorded verification evidence
for this slice does not reproduce, and the two assertions that fail to run are two of the exact
protections §8 asks to be spot-checked.

F1 is a small mechanical fix. Everything else is non-blocking.

---

## 2. Verification performed

All commands run at the frozen SHA in a clean checkout.

| Command | Result |
|---|---|
| `git cat-file -t 1f6a109…` / `git log -1` | commit present, matches the frozen handoff |
| `git merge-base --is-ancestor origin/main HEAD` | **false** — target is behind main by 40 commits |
| `npm ci` (in `forge/`) | rc=0 |
| `npm test` (node **v22.22.2**) | **311 pass / 2 fail / 2 cancelled of 315** — does **not** reproduce the recorded 315/0 |
| `python3 skills/building-tnr-content/scripts/quest_compile.py --selftest` | **9 passed / 0 failed** — matches |
| `python3 …/quest_compile_integration_test.py` | rc=0, all PASS — matches |
| `python3 …/quest_worker_contract_test.py` | rc=0, 4/4 PASS incl. "worker has no live-game path" — matches |
| `python3 …/lawmap.py` | 93 laws / 93 matrix rows / 77 citations / **0 errors, 5 warnings** — matches |
| `python3 …/doctrinemap.py` | 21 assertions, 18 referenced, 16 surfaces / **0 errors, 0 warnings** — matches |
| `node forge/build.mjs` then `git status --porcelain forge_bundle.js` | clean — **bundle reproduces byte-identically from source** |
| `git log --name-only 77042a4^..1f6a109 \| grep -E 'runner\|transport\|budget\|reconcile\|storage'` | **no matches** — untouched by this correction |

Node version note: CI pins node 24; this container has node 22.22.2. See F1 for why the
discrepancy is not dismissible as a runner artifact.

---

## 3. Disposition of M1 — **CLOSED**

The browser no longer has any Actions capability, by deletion rather than by convention.

- `Github.dispatch()` is **removed** from `forge/src/github.mjs` (−27 lines), taking with it the
  `actions/workflows/<name>/dispatches` endpoint, the `DISPATCHABLE_WORKFLOWS` allowlist, and the
  `HTTP 403; the fine-grained PAT needs Actions: write` error path.
- `QuestStudioRepository.dispatch()` and the `QUEST_STUDIO.workflow` key are **removed**;
  `submit()` now returns after the Contents `PUT` alone.
- `grep -rni dispatch forge/src forge_bundle.js` (excluding `dispatchEvent`) returns **nothing**.
  The shipped bundle carries no dispatch path either.
- Settings copy is accurate: `forge/src/ui/screens.mjs:305` —
  *"fine-grained PAT (Contents: write only on tnr-tools; do not grant Actions or Workflows)"*.
- `.github/workflows/quest_studio.yml` trigger is `push` on branches `studio/quest/**`,
  paths `studio/requests/*.quest.json`. Nothing in the compile path requires Actions or Workflows
  permission on the operator device.

Transport matches the expected shape in the brief end to end.

---

## 4. Findings by severity

### F1 — BLOCKING (Major). Two tests are structurally nested inside other tests; their assertions never execute, and the recorded 315/0 does not reproduce.

Two `test(...)` declarations were inserted **into the body of another test** rather than beside it.
The outer callback opens, immediately declares a second test, then continues with its own
assertions. It is syntactically valid and semantically broken: the inner test registers as a
subtest during the parent's execution, the parent does not await it, and the runner cancels it —
`test did not finish before its parent and was cancelled`.

| File | Outer test (line) | Swallowed test (line) |
|---|---|---|
| `forge/test/github.studio.test.mjs` | `"QuestStudioRepository marks an older persisted result stale"` (135) | `"QuestStudioRepository refuses build reads without an exact submitted source identity"` (137) |
| `forge/test/quest.studio.ui.test.mjs` | `"real Mission profile sentinels render as awaiting ruling and block compile"` (219) | `"editing a submitted Mission invalidates persisted build identity before reopen"` (221) |

Why this is blocking rather than cosmetic:

1. The two swallowed tests are **exact-source-identity enforcement on build reads** and
   **edited-draft stale-build invalidation** — items 3 and 8 of the spot-check list in the brief.
   Both are currently unverified by the suite that is being offered as their evidence.
2. `docs/agents/ENGINEERING_AUDITOR.md` states plainly: *do not accept an author's test count as
   proof.* The count was reconstructed and it is 311/2/2, not 315/0. Accepting a security-boundary
   slice on evidence that does not reproduce is the wrong precedent regardless of cause.
3. If CI on node 24 does report 315/0, that is worse, not better: it means a cancelled subtest is
   being counted as a pass and the gate is blind to this class of defect.

**Product code is not regressed.** `repository.mjs buildResult()` still rejects a missing or
malformed `expectedSourceCommit` (`/^[0-9a-f]{40}$/`, throws *requires the exact submitted source
commit*), and the edited-draft invalidation path is present. This is an evidence defect, not a
behaviour defect — but the evidence is what acceptance rests on.

**Correction:** move both inner `test(...)` declarations out of their parents, re-run, confirm
315/0 on the pinned node version, re-freeze. Recommend also pinning the local dev node version to
CI's 24 so this class of divergence surfaces before a freeze.

### F2 — Major (hardening, not a defect at this SHA). The compile job's own workflow definition is read from the request branch, so the entire trusted-compiler boundary rests on GitHub refusing a Contents-only token any write under `.github/workflows/`.

For `push` events, Actions resolves the workflow file **at the pushed ref**, not at `main`.
`submit()` creates the request branch with `ensureBranch(branch, main)`, so every
`studio/quest/*` branch carries a full copy of `.github/workflows/quest_studio.yml`. Anything able
to modify that file on a request branch owns the job outright — `permissions`, checkout refs,
arbitrary `run:` steps — and the trusted-main compiler checkout becomes irrelevant, because the
attacker simply does not invoke it.

The design is sound **only** because fine-grained PATs require the separate **Workflows**
permission to create or update paths under `.github/workflows/`, and RUL-2026-09-16-002 forbids
granting it. That is real and server-enforced. But it is currently an *implicit* load-bearing
assumption: nothing in the architecture doc, the ruling, or the workflow comments names it. The
day someone grants the browser PAT Workflows write to unblock an unrelated task, this boundary
collapses silently and no test fails.

**Recommendation (take with F1):**
- state it as a named invariant in `FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` and in the
  RUL-2026-09-16-002 rationale: *the browser credential must never hold Workflows write, because
  push-triggered workflows execute from the pushed ref;*
- add a first-step assertion in `quest_studio.yml` that the request branch's copy of
  `.github/workflows/quest_studio.yml` matches trusted `main`, and fail closed if it does not.
  Defence in depth against a future credential-scope mistake, at the cost of one `git diff`.

### F3 — Minor. The review branch's `docs/RULINGS.md` predates RUL-2026-09-16-001.

Numbering is **collision-free** — the renumber to `-002` landed correctly (`45f21c1`), `-001`
(One Perfect Crop) is on main, `-002` (Quest Studio) is on the branch, no duplicate id exists.
But `grep -c RUL-2026-09-16-001 docs/RULINGS.md` on the target returns **0**: the branch carries a
pre-`-001` copy of the ledger. A merge that takes the branch's file wholesale drops `-001`.
Resolve by rebasing onto current main (or a deliberate merge of the ledger) before integration, so
both entries survive. This is part of the same 40-commit base drift, not a separate problem.

### F4 — Minor, accepted as designed. TOCTOU between the remote-head check and the push, closed by fast-forward refusal.

`Persist build result` does `ls-remote` for the request branch head, compares it to `SOURCE_SHA`,
then `git push origin HEAD:$REQUEST_BRANCH`. A newer revision landing inside that window would
make the push a non-fast-forward, and it is rejected — **fails closed**, no `--force` anywhere.
Three independent layers protect stale publication: `concurrency` with `cancel-in-progress` keyed
per request branch, the explicit head-equality check, and non-fast-forward refusal.
No action. Recorded so that a future "add `--force` to fix flaky pushes" is recognised on sight as
a boundary break rather than a convenience.

### F5 — Minor. `Persist build result` has no `if: always()`.

Structured failures are handled correctly: the boundary path (`boundary_rc=2`) and a nonzero
compiler rc both write a result envelope, persist it, and only then surface the failure in the
final step. The single uncovered case is `test -f "$TMP_RESULT"` failing — the compiler produced
no result file at all — which hard-exits the Compile step and skips persistence entirely. Forge
then sees nothing and must fall back to poll timeout. Low consequence, worth a follow-up so that
every terminal state leaves evidence on the request branch.

---

## 5. Previously closed findings — no regression detected

Spot-checked against the frozen tree; all preserved.

| Protection | Status at target |
|---|---|
| Artifact path hardening | `generatedArtifactPath()` rejects prefix escape, empty/`.`/`..` segments, `\`, `%?#`, non-`.json` |
| `generated.manifestSha256` binding | enforced `/^[0-9a-f]{64}$/`, digest recomputed over fetched text and compared before use |
| Edited-draft stale-build invalidation | present in product code — **but its test is swallowed, see F1** |
| Unresolved profile fail-closed | `quest_compile --selftest`: *mission unresolved ruling classifies as blocker* PASS |
| Worker request identity on failures | integration test: *failed envelopes preserve the validated worker request id* PASS |
| Mission profile-shape enforcement | integration test: *repository adapter blocks Mission profile-shape mismatches* PASS |
| Visible manifest inspection | ui test 186 *generated manifest inspection is visible inside the Studio shell* PASS |
| DOM sink hardening | `createElement`/CSSOM only; suite's no-socket and error-banner tests pass |
| Release-loader assertions | `release_loader.test.mjs` rc=0 |
| Zero-live compiler boundary | `quest_worker_contract_test.py` *worker has no live-game path* PASS; `validateBuildResult` refuses `liveGameTouched !== false` |

No previously accepted finding was regressed by the source-push correction. The correction commit
`77042a4` touched `.github/workflows/quest_studio.yml` **only**; the browser-side removal landed
earlier in `f7e007b`. `runner`, `transport`, `budget`, `storage` and `reconcile` are untouched
across `77042a4^..1f6a109`.

---

## 6. Worker boundary — attacked and held

Recorded so the next reviewer does not have to re-derive it.

- **Recursion.** Generated commits write `studio/results/<id>.build.json` and
  `studio/builds/<id>/**`. Neither matches the `paths:` filter `studio/requests/*.quest.json`, so a
  build commit cannot re-trigger the compiler. Holds.
- **Unrelated writes.** Any other path on the request branch is outside the filter and triggers
  nothing. Holds.
- **Branch-shape attack.** `studio/quest/**` admits `studio/quest/a/b`; stripping the prefix yields
  request id `a/b`, which fails `^[a-z0-9][a-z0-9._-]{2,63}$` because `/` is not in the charset.
  Exit 2. Holds.
- **Path traversal.** The same charset excludes `/`, and the first character must be alphanumeric,
  so no `..` segment is constructible in `studio/requests/<id>.quest.json`. An id such as `a..b`
  yields a literal filename, not a traversal. Holds.
- **SHA/path confusion.** Checkout is by `github.sha`, then re-verified:
  `git -C request rev-parse HEAD` must equal `SOURCE_SHA` or the boundary step fails. `SOURCE_SHA`
  itself is regex-pinned to 40 hex. Holds.
- **Symlink escape.** `request/studio`, `.../requests`, `.../results`, `.../builds` and the source
  file itself are each refused if `-L`. Holds.
- **Trusted-code separation.** Compiler is checked out from `ref: main` into `tools/` with
  `persist-credentials: false` and invoked as `python3 tools/skills/.../quest_compile.py`. Nothing
  under `request/` is ever executed. Compiler revision is measured (`git -C tools rev-parse HEAD`)
  and recorded in `provenance.compilerRevision`. Holds — subject to F2.
- **Persistence confinement.** `git add --` is scoped to exactly the two request-scoped paths;
  push target is the request branch. No trusted-main write path exists. Holds.
- **Retry semantics.** `submit()` injects a fresh `meta.repositoryBuildRequestId` on every Compile,
  so recompiling visually unchanged content still produces a distinct blob, a distinct commit and a
  distinct `sourceCommit`. This is the correct fix for the identical-content no-op case, and
  `sourceCommit` remains the exact identity Forge polls against. Holds.

---

## 7. Residual integration debt vs. actual blockers

**Blocker (one):** F1.

**Integration debt — not blockers, but must be recorded as requirements before Forge Next work:**

1. **No end-to-end `studio/quest/*` source-push build has ever executed**, because trusted `main`
   does not yet contain the Quest Studio compiler seam. The static and integration evidence is
   sufficient to accept *this slice* — the worker contract test pins the trust boundary
   mechanically, the compiler selftest and integration test exercise the compile path, and the
   transport is small and fully readable. It is **not** sufficient to declare the transport proven.
   **Requirement:** once the seam is on `main`, run one repository-only rehearsal against a
   throwaway request id and verify: trigger fires, compiler revision recorded, result and build
   artifacts land on the request branch only, a second push supersedes the first, and the stale
   branch-head refusal fires when forced. No live game contact.
2. **Base drift.** 40 commits behind main, including the ledger gap in F3. Rebase before integration.
3. F2's invariant + CI assertion.
4. F5's `if: always()`.

---

## 8. Recommended planning reconciliation — specified, not applied

`claude/forge-next-planning-v3frzi@22f1fc43f8e316d0ec8412d5595a7cd0936f98d0` should **not** be
reconciled yet. The brief gates that work on a clean review, and the accepted Quest Studio SHA is
going to move when F1 is fixed. Reconciling now would immediately restale the pointer it is meant
to fix.

When the corrected Quest Studio SHA is frozen, the reconciliation should:

- replace stale references to the previous Quest Studio review target with the newly accepted SHA;
- state the transport as **source-push**, and the browser credential scope as **Contents: write
  only**, citing RUL-2026-09-16-002;
- remove any statement that the Quest Studio review has not yet happened, replacing it with a
  pointer to this review and its disposition;
- carry F2's invariant forward into the unified implementation contract, since it constrains
  credential provisioning for every future Studio;
- carry §7's rehearsal requirement forward as an integration gate;
- preserve the approved ForgeCore architecture unchanged and reopen no settled director decision.

Forge Next implementation should not begin until the corrected Quest Studio SHA and the reconciled
planning SHA are both frozen and returned to the director.

---

## 9. Summary for the director

The credential decision worked. M1 is gone by deletion, not by promise — the Actions endpoint no
longer exists anywhere in Forge or its bundle, and the operator PAT can now be Contents-only. The
worker boundary held under every attack tried: recursion, branch shape, traversal, SHA confusion,
symlinks, stale publication.

One thing needs fixing before acceptance, and it is fifteen minutes of work: two tests were pasted
inside other tests, so they never run, and the "315 passed" figure on the handoff does not
reproduce here. The code those tests cover is fine — the tests are not. Given this is a security
boundary, the number should be true before it is signed.

One thing is worth adding while it is open: the whole trusted-compiler design depends on GitHub
refusing a Contents-only token any write to `.github/workflows/`. That is true today and nobody has
written it down. It should be an invariant in the architecture doc and a check in the workflow,
because the failure mode is silent.
