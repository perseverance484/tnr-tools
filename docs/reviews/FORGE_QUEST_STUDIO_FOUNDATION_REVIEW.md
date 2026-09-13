# Quest Studio foundation — independent review

**Status:** INDEPENDENT REVIEW — APPROVE WITH REQUIRED CORRECTIONS BEFORE INTEGRATION
**Date:** 2026-09-13
**Reviewer:** Fable / Claude Code, acting as independent reviewer under `docs/workflows/FABLE_REVIEW.md`
**Reviewed branch:** `chatgpt/forge-quest-studio-foundation`
**Reviewed exact SHA:** `cda8ac76100b2fa4b5429bea27c3c8c80353e240`
**Its stated fully verified parent:** `bcb3a47e7c516b20f5a51c5aa195364d32eb6b73`
**Shared baseline compared against:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`
**Live `main` at review start:** `6848a7805d912378f7f8eb27f52c9625dd10ac54`
**Governing contract:** `state/prompt_forge_quest_studio_foundation.md` (APPROVED IMPLEMENTATION CONTRACT, ChatGPT-owned slice)
**Implementer's handoff:** `docs/handoffs/FORGE_QUEST_STUDIO_FOUNDATION_HANDOFF.md` at the reviewed SHA
**Live-game requests or writes performed by this review:** none. No credential material was used, requested or synthesised. No network request was made to any host.

## 1. Verdict

**The trust boundary is sound. The seam is the right seam. Six corrections are required before integration, and one of them is a director decision rather than an engineering fix.**

The central claim of this slice — that a Forge-authored Quest Source can reach a canonical repository compiler and come back as a structured build result without any live-game path and without weakening existing Forge safety — is **true**, and I verified the strongest part of it mechanically: `forge/src/runner/`, `forge/src/transport/`, `forge/src/storage/`, `forge/src/budget/` and `forge/src/reconcile/` are **byte-identical to the baseline**. The execution core was not touched at all. Every gate the handoff claims reproduces independently in a clean checkout.

What is not yet right is concentrated in three places: the **privilege** the browser must hold to dispatch the worker, the **confinement** of the one read the browser performs on repository-supplied data, and a set of **honesty defects in the authoring surface** where the browser tells the operator something the evidence does not support. None of them is a live-game hazard. One of them (M1) materially widens what a stolen operator token can do to `main`, and it is the finding I would fix first.

**Disposition:** `APPROVE_WITH_REQUIRED_CORRECTIONS`. Integration should wait for M1–M6.

## 2. Method and safety envelope

Per `docs/workflows/FABLE_REVIEW.md`. The target was established first (§1), authority reconstructed from `CLAUDE.md`, `docs/00_INDEX.md`, `docs/DEVELOPMENT_WORKFLOW.md`, the implementation contract and the design documents the slice is built to satisfy (§2), and every important claim was tested as an invariant with an adversarial case rather than read for plausibility (§4).

The frozen SHA was read in a detached-HEAD worktree with an in-tree `node_modules`; the branch itself was never modified, and `git status` in that worktree is clean at the end of the review. Scratch probes live under the session scratchpad, not in the repository. Every finding below was put through a refutation pass whose default was to reject it; findings that could not be reproduced were dropped, and several were downgraded when the refutation showed the consequence was smaller than first claimed. Eight invariant lenses, per-finding adversarial verification and a completeness critic produced 18 verified findings from a larger candidate set; 72 separate invariants were checked and found sound.

Two classes of claim could not be settled inside the envelope and are marked as such throughout: anything requiring a GitHub API call (so: how the remote server normalises a URL, and the CI run/job/artifact ids the handoff quotes), and anything requiring a browser or a live operator device.

## 3. Gates: every claimed result reproduces

Re-run by this review inside a clean checkout of `cda8ac76`, not taken from the handoff:

| Gate | Handoff claims | This review measured | |
|---|---|---|---|
| `cd forge && npm test` | 308 tests, 308 passed | **308 tests, 308 pass, 0 fail** | ✅ |
| `quest_compile.py --selftest` | 9 passed, 0 failed | **9 passed, 0 failed** | ✅ |
| `quest_worker_contract_test.py` | PASS, 6 boundary checks | **6 checks PASS**, exit 0 | ✅ |
| `quest_compile_integration_test.py` | Mission adapter PASS | **PASS**, exit 0 | ✅ |
| `cd forge && npm run fixtures` | regenerated = checked | **byte-identical** | ✅ |
| `cd forge && npm run build` | bundle parity PASS, ~427.2 KB | **byte-identical to the checked `forge_bundle.js`, 427.2 KB** | ✅ |
| `.github/scripts/pack_skills.py` | skillpack regenerated | **`dist/*.zip` byte-identical to checked** | ✅ |
| `doctrinemap.py` | not claimed | **exit 0**, 21 assertions, 0 errors, 0 warnings | ✅ |
| `render_doctrine.py --check` | not claimed | **exit 0**, all projections current | ✅ |
| `build_packs.py --check` | not claimed | **exit 0**, all packs and TOCs current | ✅ |
| `lawmap.py` | not claimed | **exit 0**, 93 laws, 5 pre-existing warnings | ✅ |

The four coherence gates in the last block are required by `CLAUDE.md` §8 for a change under `skills/`, were not mentioned in the handoff, and pass. Bundle reproducibility deserves particular credit: a checked-in generated artifact that rebuilds byte-for-byte from source is the property most often claimed and least often true.

One correction to the handoff's own record: the temporary write-enabled bundle-sync workflow it describes in section 6 was added and removed **twice** (`2d9fcb0`/`cab1f5b`, then `52dbf71`/`7e740a6`), not once. Having read it (`git show 52dbf71:.github/workflows/quest_studio_bundle_sync_temp.yml`), the practice was tight — it triggered only on a push touching its own file, was gated to that one branch, and did `git add -- forge_bundle.js` and nothing else — and it is absent from the review target. The disclosure is adequate in substance; the count is wrong.

## 4. Required corrections

### M1 — major, user-decision-required — Compile requires a repository-wide `Actions: write` token, which can dispatch `relay.yml` and land arbitrary content on `main`

**Invariant.** Brief §8: "All GitHub bearer traffic remains GitHub-only and separate from the TNR game session." Brief §10 item 10 asks directly whether the browser bridge "has more privilege than this design actually needs".

**What happens.** `forge/src/studio/repository.mjs:108` dispatches the worker through `Github.dispatch` (`forge/src/github.mjs:131-148`), which requires the stored PAT to hold **Actions: write**. GitHub fine-grained tokens have no per-workflow scoping, so this is repository-wide. At the reviewed SHA the repository contains five other dispatchable workflows, four of them with `contents: write` — and one of them is `relay.yml`, whose entire function is to merge an arbitrary `relay/*` branch into **`main`** (`.github/workflows/relay.yml:3-8, 25-40`). `Github.dispatch` itself validates only that the workflow name matches `/^[A-Za-z0-9._-]+$/` (`github.mjs:133`); there is no allowlist.

The consequence is a real widening. Before this slice, a stolen operator PAT (`contents: write`) could push to a branch. After it, the same stolen token can push a `relay/*` branch **and trigger the merge into `main`**. The token lives in `localStorage` on the game origin, in a page Forge does not control, which is precisely why the two-auth-path rule exists.

**Evidence.** `.github/workflows/relay.yml:1-40`; `forge/src/github.mjs:131-148`; `forge/src/studio/repository.mjs:105-118`; workflow survey of all nine workflows at the frozen SHA.

**Why this is the director's, not only Fable's.** The engineering options are known and the code can express any of them, but the choice between them is a credential-scope decision, which `CLAUDE.md` §10 reserves. The options:

- **(a) Do not grant `Actions: write`.** Trigger the worker by pushing to `studio/quest/*` and let the workflow run on `push` rather than `workflow_dispatch`. The PAT stays `contents: write`; run correlation moves from "the dispatch I just made" to "the branch and SHA I just wrote". This is the model the approved design recommended first.
- **(b) Grant it, with the risk recorded.** Keep the explicit-request correlation, and accept that the browser token can trigger any workflow in the repository.
- **(c) Grant it and reduce the blast radius** — for example require `relay.yml` to run only from a protected context, or retire it if the Studio makes it redundant.

**Do not mistake a code-side allowlist for the fix.** Adding a workflow allowlist to `Github.dispatch` is worth doing (it stops a bug in Forge from dispatching the wrong thing) but it does **not** mitigate M1, because an attacker holding the token calls the GitHub API directly and never passes through Forge's code. Only (a) or (c) changes what the token can do.

**Proposed engineering fix, whichever way the scope is ruled.** Add the allowlist at `github.mjs:133` (`if (workflow !== QUEST_STUDIO.workflow) throw`) as defence in depth, and state the required token scope in one place that the UI reads, rather than in prose (see M6b).

### M2 — major, confirmed defect — the generated-artifact confinement is bypassed by percent-encoding, and by `?` or `#` in the path

**Invariant.** Handoff §5: the Forge layer "confines generated-manifest reads to the exact request's `studio/builds/<requestId>/...` directory and rejects traversal segments/backslashes". Handoff §7 presents this as the fix for a traversal hole found during hardening.

**What happens.** `generatedArtifactPath` (`forge/src/studio/repository.mjs:51-63`) splits the tail on literal `/` and rejects empty, `.` and `..` segments and any `\`. It does not reject `%`, `?` or `#`. `Github._url` (`forge/src/github.mjs:39-41`) then interpolates the path into the API URL **unencoded** — while encoding the `ref` in the same expression — and appends its own `?ref=`. The path this guard protects comes from `result.generated.manifestPath`, read off a **mutable** request branch, which the handoff's own debt item 8 tells reviewers to treat as tamperable.

**Evidence — reproduced offline, no network.** A probe that imports the real modules with a recording `fetch` stub (`scratchpad/review-scratch/traversal_probe.mjs`):

```
REJECTED      literal dot-dot        studio/builds/<id>/../../harvests/inbox/x.json
REJECTED      backslash              studio/builds/<id>/..\..\x.json
REJECTED      empty segment          studio/builds/<id>//x.json
PASSED GUARD  percent-encoded dot-dot  → .../contents/studio/builds/<id>/%2e%2e/%2e%2e/harvests/inbox/x.json?ref=…
PASSED GUARD  percent-encoded slash    → .../contents/studio/builds/<id>/..%2f..%2fharvests/inbox/x.json?ref=…
PASSED GUARD  double-encoded dot-dot   → .../contents/studio/builds/<id>/%252e%252e/x.json?ref=…
```

Two consequences differ in how well they can be proven here:

- **The `?` and `#` forms need no server behaviour at all.** `studio/builds/<id>/a#x.json` passes the guard and produces a URL whose `?ref=` has been swallowed into the fragment and is never transmitted — so GitHub serves the file from the **default branch**, and Forge presents a file from `main` to the operator as "the generated manifest for this Studio build". `studio/builds/<id>/x?ref=main&pad=.json` injects a `ref` ahead of the adapter's own. This is a confirmed defect, verifiable with `new URL(...)` alone.
- **The percent-encoded traversal forms depend on whether the GitHub API decodes before normalising**, which this review cannot test. That half is an **unverified risk**, not a confirmed escape. It should still be closed: a browser-side confinement control must not delegate its last line of defence to a remote server's URL handling.

The blast radius is bounded — it is a read, within a repository the token already reads, and it cannot leave `api.github.com` (I checked: a path of `../../../../evil.example.com/x` still resolves to host `api.github.com`). It is nonetheless a break of a stated control in the one surface whose entire purpose is provenance.

**Note on the test.** `forge/test/github.studio.test.mjs:162-188` is named "generated manifest reads cannot escape the request build directory" but tests exactly the four literal spellings the implementation handles. It pins the code, not the invariant its name claims.

**Proposed fix.** Two independent lines, both small: (1) in `generatedArtifactPath`, add a character allowlist before the segment walk — `if (!/^[A-Za-z0-9._/-]+$/.test(path)) throw` — which removes `%`, `?`, `#` and `\` in one rule and leaves every legitimate generated path valid; (2) in `Github._url` and `Github.put`, encode per segment (`path.split("/").map(encodeURIComponent).join("/")`), which also hardens the legacy callers. Extend the test's case list with the encoded, query and fragment forms.

### M3 — major, contract–source mismatch — the build envelope carries no generated-manifest hash, so the artifact has no binding to the result that validated it

**Invariant.** The approved design requires the build result to carry a digest of the generated artifact (`docs/design/FORGE_NEXT_QUEST_STUDIO.md`; `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`), so that what the operator inspects can be proven to be what the compiler validated.

**What happens.** `quest_compile.py` records `generated.manifestPath`, `generated.entities` and `generated.enemies`, and `provenance` with `sourceSha256`, `sourceRevision` and `compilerRevision` — but **no digest of `manifest.json` itself**. Both the result and the artifact live on the same mutable request branch and can be edited independently. Nothing on the Forge side can detect that the manifest was changed after the result was written.

Today the consequence is confined: there is no promotion path into the runner (handoff debt 6), so the worst outcome is an operator reading a manifest that no longer matches its validation record. It becomes a correctness issue the moment a promotion contract exists, and a promotion contract is the next thing this seam needs.

**Proposed fix.** Add `generated.manifestSha256` in `compile_mission` where the file is written, and verify it in `QuestStudioRepository.generatedManifest` after the read. Both are a few lines, and doing it now means the promotion gate inherits the property instead of retrofitting it.

### M4 — major, confirmed defect — an edited draft shows a previous revision's build as current, with no staleness banner

**Invariant.** Handoff §5: the Forge layer "marks results from older source revisions stale rather than presenting them as current."

**What happens.** Staleness is computed only as `provenance.sourceRevision !== expectedSourceCommit` (`repository.mjs:124-135`), and `expectedSourceCommit` is `draft.sourceCommit` — the last **submitted** commit. Every edit handler clears `this.buildState` in memory, but `draft.sourceCommit` is persisted to `localStorage` and is never cleared. So: compile revision A, edit the premise, reload. `openMission` restores the edited draft, calls `refreshBuild`, matches A, computes `stale: false`, and renders the green "Mechanically valid / Live game untouched" callout with **Inspect generated manifest** enabled — for prose the operator can see on screen that was never compiled. The staleness detector answers "is this the result for the revision I last submitted?", never "is this the result for what is in the editor?".

**Evidence.** Reproduced against the real `QuestStudioWorkspace` over jsdom with storage shared across a close/reopen cycle: after editing and reopening, `buildState` is `{status: valid, stale: false}`, the "Older build result" banner is absent, and the inspect action is offered.

**Proposed fix.** Give the draft a content identity: store a digest of `missionSourceFromDraft(draft)` alongside `sourceCommit` at submit time, recompute on restore, and treat a mismatch as stale. The cruder alternative — clear `draft.sourceCommit` and `draft.lastResult` in the same handlers that already clear `buildState` — is smaller and sufficient.

### M5 — major, confirmed defect — the unratified `S` profile is offered as selectable and labelled "no combat"

**Invariant.** The safety-state contract forbids the UI implying more than the evidence supports; `mission.py`'s design intent is that an `AWAITING_RULING` profile value is a refusal, not a default.

**What happens.** In `48_DATA_mission_profiles.json`, rank `S` has **every** shape field set to the string `"AWAITING_RULING"`. Every browser gate meant to hold combat back is a numeric comparison that fails open on a non-numeric value: `Number("AWAITING_RULING")` is `NaN`, `NaN > 0` is `false`, `Number.isInteger(NaN)` is `false`. Rendered against the real profile file, `S` is **not** disabled, is labelled `S · ? nodes · no combat` — an affirmative and false claim about combat — `missionDraftProblems()` returns empty for a one-beat draft, Compile is enabled, and the readiness callout reads "Ready for repository compile".

**The repository backstop holds, and that is worth stating plainly.** A dispatched `S` mission is refused by `mission.py` with "these are rulings, not defaults", which `classify_mission_error` correctly turns into `blocked` / `decision_required`. No wrong content is produced. The defect is that the browser asserts a fact it has not established, and burns a repository round trip to discover it.

**Proposed fix.** Fail closed on any non-finite shape value: a single `shapeNum()` helper, then treat a non-numeric `battle_nodes` as "not authorable" (disable the option), render "combat unknown" rather than "no combat", and surface the unratified profile as a director decision in the readiness callout rather than as readiness.

### M6 — major, needs refinement — a loader origin-scope assertion was weakened out of scope, and the operator-facing token-scope instruction is now wrong

Two separate items, both in the "the branch changed something it did not need to" class.

**(a) The `@match` allowlist assertion.** `forge/test/release_loader.test.mjs` previously pinned the loader's `@match` set with a `deepEqual` plus a negative "no `/forge` match" assertion. The branch replaced both with presence checks, which cannot see extra entries: a loader carrying `// @match *://*/*` — injecting `forge_bundle.js`, and with it the GitHub bridge and the PAT read, into **every site the operator visits** — now passes the suite. `forge_loader_user.js` is **not in this branch's diff at all**, and I verified the original assertion still passes against the frozen loader, so nothing here required the relaxation. The one relaxation in that commit that *was* necessary is the `@x-release-pending` marker count. Nothing else in the repository constrains the `@match` set.

**(b) The token-scope instruction.** `forge/src/ui/screens.mjs:305` still tells the operator to create a "fine-grained PAT (contents: write on tnr-tools only)". After this slice, Compile additionally needs `Actions: write`. An operator following the on-screen instruction gets a failure at dispatch with no indication why.

**Proposed fix.** (a) Restore the exact-set assertion and the negative check, keeping only the marker-count relaxation. (b) Make the required scope one constant that the Settings copy renders, and update it when the M1 ruling lands — the correct text depends on which option the director takes.

## 5. Minor findings

Reported for the record; none blocks integration. Each survived a refutation pass.

| # | Finding | Where |
|---|---|---|
| m1 | The worker contract test's shell-interpolation guard only scans `run:` block scalars (the `run: \|` form) and only forbids the literal `${{ inputs.`, so a single-line `run:`, a folded `run: >`, or the `${{ github.event.inputs.* }}` spelling — which this repository already uses in `relay.yml:25` — would pass. The frozen workflow is genuinely clean; the **gate** is not a durable regression barrier | `quest_worker_contract_test.py:51-65` |
| m2 | `blocked` versus `failed` is decided by substring-matching three English phrases against `mission.py`'s human prose, with no contract on that prose and no test that provokes a real `MissionError`. A reword in a file this slice does not own silently turns a director decision into a tool defect. The selftest asserts the classifier against its own string literal | `quest_compile.py:100-113`, `:343` |
| m3 | `objective_count` is enforced as exact equality (`beats.length + 1`) by the browser and by **nothing canonical** — it appears in `mission.py` only inside a selftest fixture, and not at all in `quest_compile.py` or `validate.py`. The browser refuses drafts the repository would accept, which inverts the stated ownership. The `+ 1` mapping exists nowhere canonical either | `ui.mjs:133-136` vs `mission.py:351` |
| m4 | Draft persistence failures are swallowed (`catch { /* best effort */ }`) and the UI then reports a save | `ui.mjs:157` |
| m5 | "Build still running" is an inference from an absent file. A worker that refused the request (exit 2/3), crashed, or was cancelled by `cancel-in-progress` is indistinguishable from one mid-flight, permanently | `repository.mjs:129-131`, `ui.mjs:385,459` |
| m6 | Staleness fails open when `expectedSourceCommit` is omitted — every other unknown in that function fails closed. No shipped caller reaches it; it is a trap for the second one | `repository.mjs:124,134` |
| m7 | `put(..., { branch: undefined })` silently targets `main`: a JS default parameter fires on `undefined`, so "options passed with a bad branch" is indistinguishable from "no options". Unreachable today because `questBranch()` always produces a valid string | `github.mjs:111` |
| m8 | `meta` participates in `sourceSha256` although the contract declares it "ignored by deterministic compilation". Three sources with identical `content` and different `meta` hash differently | `quest_compile.py:64-65,226` |
| m9 | The CI zero-live-network guard AST-scans only `quest_compile.py`, not the modules it imports, and greps only two files. It is a useful tripwire, not a transitive proof | `quest_studio_ci.yml:53-79` |
| m10 | `quest_studio_ci.yml`'s path filter omits inputs the compiler actually depends on (`mission.py`, the mission profile data), so a change to canonical Mission policy does not re-run the Studio gate | `quest_studio_ci.yml:5-32` |
| m11 | The Mission integration gate asserts status but not warnings, so an art-requirements regression compiles green | `quest_compile_integration_test.py:71-86` |
| m12 | A missing compiler adapter — a tool capability gap — is returned as `blocked`, the status the contract reserves for a missing user decision. No director ruling can unblock it | `quest_compile.py:244-257` |
| m13 | 18 files on the branch have no trailing newline, including `docs/RULINGS.md`, which is an append-only ledger: the next appended ruling will concatenate onto the last line | branch-wide |

## 6. What is sound, and should be preserved

The review checked 72 invariants and found them held. The ones worth naming:

1. **The execution core is untouched.** `runner/`, `transport/`, `storage/`, `budget/`, `reconcile/` are byte-identical to `main@305a28f`. Measured, not asserted. This is the strongest possible form of "existing live-operation safety is not weakened", and it is exactly what a slice like this should be able to say.
2. **No live-game path exists anywhere in the diff.** The only occurrences of the game host in 14,585 added lines are the two guards that forbid it.
3. **Workflow inputs never reach shell syntax.** All four `run:` blocks in the worker use environment indirection; I checked each one. The trusted compiler checkout and the authored request checkout are genuinely separate, the compiler executes only from `tools/`, and request-branch content is never executed.
4. **The request boundary fails closed.** Request id, source path, branch and a 40-hex source SHA are each validated, the branch/path pair must match the id, the checked-out HEAD must equal the dispatched SHA (so a branch that advanced mid-flight is refused, exit 3), and the four Studio directories plus the source file are symlink-checked.
5. **Persistence is request-scoped.** `git add` names exactly `studio/results/<id>.build.json` and `studio/builds/<id>`, both built from the validated id, and generated artifact filenames are fixed (`manifest.json`), never derived from authored content.
6. **Evidence is persisted before failure is surfaced.** A compiler failure writes its structured envelope first and fails the run afterwards, so a failed build still produces a readable result.
7. **`liveGameTouched:false` is strictly enforced** (`!== false`), and `Compile` is separated from live execution: the Studio ships no Start control and no promotion path, deliberately.
8. **`blocked` never masquerades as `failed` by accident.** Only a typed `QuestBlocked` produces `blocked`; every other exception is `failed`. The conservative direction is the right one, and it is documented in the code.
9. **Mission policy is genuinely delegated.** The adapter calls `mission.py` with the repository's own profiles and runs canonical validation; it does not reimplement mission rules in Python or JavaScript, and the profile *values* the browser uses are read from the canonical file rather than hard-coded.
10. **The no-HTML-sink law is machine-enforced** across `forge/src` and covers the new Studio files.
11. **Legacy GitHub behaviour is preserved.** Default-`main` semantics are unchanged for every pre-existing caller, and the Studio must opt in to a branch explicitly.
12. **Generated artifacts reproduce.** The bundle, the fixtures and the skillpack zips all rebuild byte-identically, and the `RULINGS.md` entries are well formed and point at the correct canonical owners.
13. **Unsupported subtypes are honest.** Battle Pyramid, Story, Event, Raid/Boss and Daily are registry-visible and not presented as executable.

One behaviour change to an **existing** screen is worth flagging because the handoff does not mention it. The shared `h()` helper now assigns `value` as a property, which repairs `App.showExport`: on `main@305a28f` that textarea was set with `setAttribute("value", …)`, which does nothing on a `<textarea>`, so the results-bundle export has been rendering **empty**. The branch fixes it. Measured both ways against the baseline and branch helpers. The other effect — input values no longer appearing as DOM attributes — is neutral to positive (the PAT field no longer serialises its value), and nothing in the tree depends on `defaultValue` or form reset.

## 7. The two review-focus lists, answered

**Brief §10.**

| Ask | Answer |
|---|---|
| Branch/path injection in the worker | **Clean.** Validated, fails closed, id-bound. See §6 items 3–5 |
| Can request-branch code execute in the worker | **No.** Separate checkouts; compiler runs from `tools/` only |
| Can Forge accidentally write drafts to `main` | **No in practice** — every Studio path goes through `questBranch()`. One latent shape (m7) |
| Do browser rules duplicate canonical Python policy | **Yes, one does** — `objective_count` (m3), plus the S-rank gates (M5) |
| Is `blocked` vs `failed` preserved | **Structurally yes** (§6 item 8); the coupling that decides it is fragile (m2), and one capability gap is misfiled as `blocked` (m12) |
| Is provenance sufficient to reproduce a build | **Input side yes, output side no** — M3 |
| Does any new path weaken live-operation safety | **No.** §6 items 1–2, measured |

**Handoff §10.** Items 1–5 and 9 are answered above and are sound except M2. Item 6 (stale/tampered) is answered in both halves: stale is handled but incompletely (M4), tampered is not (M2, M3). Item 7 is m2/m12. Item 8 is m3. Item 10 is **M1**, and it is the finding the handoff's own question most deserved. Item 11 is verified: everything reproduces. Item 12 (the three declared npm vulnerabilities) is **not verifiable offline** and is left to a separate dependency audit, which is the right call for this slice.

## 8. Unverified, and what would settle it

- **Whether the GitHub API normalises percent-encoded traversal** in a contents path — settles the second half of M2. A single authenticated request against a scratch repository would settle it; it is outside this review's zero-network envelope.
- **The CI run, job and artifact ids** quoted in handoff §6, and the "contents read-only during the final gate" claim — settled by opening that run in the GitHub UI.
- **The three declared npm vulnerabilities** — settled by `npm audit` with network access.
- **Everything requiring a browser or a real dispatch**: an actual `workflow_dispatch` from the Forge UI, a worker refusal observed end to end, and the operator-device path. The handoff declares these as not performed and that declaration is accurate.
- **The worker cannot be rehearsed before integration**: it refuses any dispatch not from `refs/heads/main`, and it does not exist on `main` yet. First real execution will be after integration, which is an argument for landing M1–M3 before that first run rather than after.

## 9. Authority and process notes

Not defects in the code, but they belong in the record and they are cheap to fix at integration:

- **`docs/00_INDEX.md` does not route the new artifacts.** `quest_compile.py`, `quest_worker_contract_test.py` and `49_DATA_quest_studio_subtypes.json` are new repository-owned canonical artifacts with no entry in the routing index, which `CLAUDE.md` §3 makes the arbiter.
- **`studio/*` is an undeclared branch namespace.** `docs/DEVELOPMENT_WORKFLOW.md` declares `fable/*`, `chatgpt/*` and `coord/*`, and its cleanup rule names only those three. The Studio creates one branch per request and nothing deletes them.
- **`scrub.yml` has no branch filter** (`on: [push]`), so every operator source save to a `studio/quest/*` branch runs the full privacy gate. That is arguably desirable — authored content is scanned — but it is an operating cost nobody has budgeted, and it should be a deliberate choice.

## 10. Integration gate

Against `docs/workflows/FABLE_REVIEW.md` §12:

| Condition | State |
|---|---|
| Confirmed blockers closed | **No blocking findings.** M1–M6 are required corrections, not blockers |
| Required user rulings recorded or safely deferred | **No.** M1 needs a director ruling on credential scope before the seam is used with a real token |
| Required tests/gates/builds/fixtures green | **Yes**, all reproduced independently (§3) |
| Source and generated-artifact agreement adequate | **Yes** for the bundle, fixtures and skillpack; **no** for the generated manifest, which has no digest (M3) |
| No merge-blocking contradiction | **None found** |
| Implementation still points at the reviewed SHA | **Yes**, `cda8ac76` is the branch head |
| Unverified browser/live items clearly identified | **Yes**, and honestly (§8) |

**Recommendation:** correct M1–M6, then integrate. M1 needs the director first; M2, M3, M4, M5 and M6 are small, local engineering fixes that the implementer can make on the ChatGPT-owned branch and return as a new frozen SHA.

## 11. Correction loop and next step

Per `CLAUDE.md` §12 and `FABLE_REVIEW.md` §11: ChatGPT applies accepted corrections on `chatgpt/forge-quest-studio-foundation` after this review is released, re-runs the affected gates, and returns a new exact SHA. This review does not modify that branch and nothing in this pass touched it.

A narrow re-check is appropriate for the next round — M1 through M6 plus the gate set — because none of the findings alters the architecture, the trust boundary or the base relationship. The wider audit does not need repeating.

Two things this review does **not** do. It does not approve integration, which is the director's. And it does not begin the unified implementation contract that the planning review proposes; that needs its own handoff.

---

**Reviewed at:** `chatgpt/forge-quest-studio-foundation@cda8ac76100b2fa4b5429bea27c3c8c80353e240`
**Review recorded on:** `claude/forge-next-planning-v3frzi` (Fable's assigned branch for this session). This file is the only artifact it adds; the Forge Next planning package at `5e300ff7f8e3606deef411290e0f9fef770b073e` is unchanged by it.
