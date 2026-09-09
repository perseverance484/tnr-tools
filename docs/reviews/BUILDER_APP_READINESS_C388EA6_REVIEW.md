# Builder app production-readiness review — c388ea6

## Target

- Repository: `perseverance484/tnr-tools`
- Implementation branch observed: `claude/builder-app-production-readiness-kelsib`
- Exact reviewed remote head: `c388ea65e0783f4e8ad0670949f23dfc420b205f`
- Prior implementation base: `4062268f433ffd4d1f9b7b1e2678367ecad9119c`
- Current shared baseline observed: `main` @ `4a506dff0af7dd499c8b580af4f0c14fdfc48c1c`
- Readiness contract: `state/prompt_builder_app_readiness.md` @ `b8f9dbf533dd51c119eb8d530e9c2fe3506e43b4`
- Mode: full relevant readiness audit, zero live-game requests.

The branch head moved once after Fable's handoff documentation: `5998db2...` was followed by the automatic skillpack rebuild `c388ea65...`. The latter changes only the two packaged skill zip artifacts. This review therefore targets the actual current remote head `c388ea65...`, not the stale branch position implied by the handoff message.

## Verdict

**CHANGES REQUIRED.**

The core Forge hardening is materially improved and the previously open F4 mutation-ambiguity defect is closed in the inspected source. However, two release blockers remain: one confirmed false-green path in repository verification and one incomplete current-upstream relevance proof.

No live-game request, game write, session cookie, or live credential was used in this review.

## Finding 1 — HIGH — Forge `SKIPPED` / pending writes can still make `harvest.py verify` exit 0

**Classification:** confirmed defect / production verification integrity.

### Invariant

A Forge result bundle may pass the repository verification gate only when every write is actually verified. A manually skipped orphan is explicitly unverified: the server row may exist and is deliberately left unresolved.

### Evidence

Forge's own state model gets this right:

- `Journal.jobOutcome()` returns `unverified` if any item is `SKIPPED` or otherwise unresolved.
- `Runner.skip()` allows `ORPHANED -> SKIPPED`.
- the UI warns that skipping leaves any server row in place and shows a finished job with skipped items as **UNVERIFIED**.
- `harvestEntry()` maps a `SKIPPED` item to results-bundle `state: "skipped"`.

But `skills/building-tnr-content/scripts/harvest.py::cmd_verify()` treats every non-`ok` state other than `error`/`failed` as a harmless `SKIP`, increments no failure counter, and may return exit 0. Therefore a Forge job can be `DONE` + `outcome: unverified` because the operator skipped an ambiguous orphan, while the repository verification command reports `verified` if the remaining entries match.

The committed harvest regression suite covers match, drift, unread, and failure, but does not cover a skipped orphan or pending Forge write.

### Practical consequence

An ambiguous create can leave a live placeholder/orphan behind. The Forge UI correctly refuses to call that verified, but the repository gate can later call the same bundle verified. That is exactly the kind of cross-surface false-success signal the readiness pass was meant to eliminate and can mislead later recovery, cleanup, or duplicate-create reasoning.

### Smallest robust correction

Preserve legacy builder semantics, but fail closed for Forge bundles. For example:

- identify Forge bundles by `cfg == "forge"`, `forgeState`, or another explicit Forge marker;
- for Forge, treat `skipped` and `pending` write entries as **UNVERIFIED** and make `verify` exit 1; and/or require a Forge top-level `outcome == "success"` before exit 0;
- add an end-to-end regression that creates an ambiguous/orphaned item, calls the real `skip()` path, exports the bundle, runs the real `harvest.py verify`, and asserts exit 1 plus an UNVERIFIED result;
- also cover manual export of a still-pending/open Forge write so that it cannot pass the gate.

Do not weaken Forge's own `jobOutcome()` semantics to match `harvest.py`; Forge is correct here.

## Finding 2 — BLOCKER — source-relevance proof is stale against the actual current game `main`

**Classification:** unverified contract/source risk; acceptance-gate blocker, not yet a demonstrated code defect.

### Evidence

The handoff proves the pinned source `345d18ac...` against the TNR Tools sentinel commit `e02f8159...` and calls that current upstream.

At review time, the actual public game repository is:

- `studie-tech/TheNinjaRPG` default branch: `main`
- current `main` head: `62af1b3405b10183b31f838c9a5f131d790460f1`

That head is newer than the sentinel SHA used by Fable. The readiness brief required current-source relevance, not merely relevance to the most recent TNR Tools sentinel snapshot.

A reviewer spot-check of three high-risk surfaces shows no change between `e02f8159...` and `62af1b34...`:

- `app/src/server/api/trpc.ts` has the same blob SHA `0bc47578...`;
- `app/src/server/api/routers/profile.ts` has the same blob SHA `d3a5f047...`;
- `app/src/validators/objectives.ts` has the same blob SHA `d2a4c184...`.

That is encouraging, but it is not a substitute for the task's own full declared-surface + generated-contract relevance gate.

### Practical consequence

Without rerunning the relevance proof against the actual game head, independent review cannot establish that Forge's procedure, validator, nested-key, rate-limit, host-page, and dependency assumptions still describe production. This is a release-evidence failure even if the newer commits turn out to be unrelated.

### Smallest robust correction

Immediately before the new handoff:

1. resolve the actual `studie-tech/TheNinjaRPG/main` head and record its exact SHA;
2. run `tools/pin_relevance.mjs` from `345d18ac...` to that exact head;
3. regenerate/compare `fields.json` and `nested.json` through their producers;
4. inspect every changed declared Forge surface rather than accepting a nonzero result mechanically;
5. update the notes/handoff with the exact current head and verdict.

If game `main` advances again before the frozen handoff, repeat the check. Do not move the original Forge pin merely because upstream is newer; move it only if the evidence requires it.

## Verified improvements that held under inspection

- **F4 mutation ambiguity:** `decodeElement()` now validates per-index error elements through the strict audited tRPC-error predicate; malformed mutation elements throw through `decodeResponse(..., {mutation:true})` and preserve `SENT` ambiguity for reconciliation.
- **Honest terminal semantics:** unread/drift verification remains `CONFIRMED` at phase `verify`; jobs become `INCOMPLETE`, not green success, and resume can only re-read. `readBack:false` is refused for manifests containing writes.
- **Pool-code safety:** resolution/stuck-code checks occur during manifest parsing, before a job opens or irreversible work begins.
- **Name collision safety:** `dedupNames` is enforced before creates through the reader/budget path and read failure pauses rather than silently bypassing the check.
- **Nested unknown-key safety:** generated nested key sets are wired for the supported effect, quest, and AI-rule structures and fail closed when the derived nested contract is absent.
- **Release pin design:** the staged workflow pins `forge_bundle.js` to the actual main commit SHA and syncs the Forge loader version when the bundle changes. The current branch-floating loader is explicitly marked unpinned until release.
- **UI result semantics:** Forge visibly distinguishes success, failure, and unverified completion; skipping an orphan explicitly states that the server row, if any, remains.

These verified improvements do not override the two blockers above.

## Handoff / workflow refinement

The current Fable branch was assigned by the Claude environment rather than using the requested legacy `builder-app` branch, and an automatic skillpack workflow advanced the branch after the handoff commit. Neither is by itself a correctness defect, but the correction handoff must wait for all auto-commits to settle and then report the final exact remote head. Review must target that SHA, not an earlier authored commit.

Because this pass changed a skill script, a generated skillpack auto-commit is expected after the correction as well. Account for it before declaring the branch frozen.

## User-owned / integration sequencing

Do **not** ask dauntless to install or run Forge yet.

`state/staged_workflows/release_pin.yml` must be installed at `.github/workflows/release_pin.yml` **before** the eventual main integration that changes `forge_bundle.js`, so that integration itself triggers the immutable pin. Installing it after the Forge bundle merge would not retroactively pin that already-landed bundle unless another qualifying bundle change triggered the workflow.

The two existing-manifest findings in Fable's handoff are content decisions, not reasons to weaken Forge validation. They can remain refused until dauntless chooses whether to edit/retire those manifests.

## Tests / execution

This review inspected the exact remote source, tests, handoff, staged workflow, and current public game-source refs. It did not independently execute Fable's npm/build/fixture suite in a local checkout. Fable reports 199/199 tests and deterministic generated artifacts; those claims should be rerun in the correction handoff. The surviving harvest defect is demonstrated directly by the committed control flow and the missing skipped/pending regression.

## Next permitted step

Fable should make only the two blocker corrections above plus the necessary regression tests/handoff updates, rerun the full readiness gates, let generated auto-commits settle, and return the final exact remote SHA. A narrow re-review is appropriate if no wider architecture or assumptions change.
