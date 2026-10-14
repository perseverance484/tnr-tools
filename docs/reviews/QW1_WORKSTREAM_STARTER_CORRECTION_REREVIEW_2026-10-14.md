# QW-1 correction — independent re-review, 2026-10-14 UTC

**Verdict: PASS for the frozen corrected implementation. R1 and R2 are closed.** No new integration blocker was found in the agreed correction surface. Recommend director acceptance and authorized integration after a fresh-main check. This review does not perform or authorize that integration.

ChatGPT reviewed as Release Auditor with Engineering Auditor lens. Fable remains the implementation owner. The earlier `CHANGES_REQUESTED` verdict still describes its original `c79c6af` target; this PASS applies to `1b14f99` below.

## Exact references and scope

| Item | Verified reference |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Frozen correction | `fable/qw1-workstream-starter-20261012@1b14f9974912e8cf0d00dc9ca3ad1b34ca7e10b9` |
| Direct parent / previously reviewed implementation | `c79c6afadeb3388d7d2823cd084405661e398f97` |
| Unchanged base / merge-base | `fe4e69cbf88b49665c9ddcd6189e9ab4c833f123` |
| Main verified during re-review | `057acddb986b50e486ccf550fac00b68fff51490` |
| Prior independent review | `8d91512d98165a031f8e04859e8d45c862320080` |
| Approved planning SHA | `c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Review branch | `chatgpt/review-qw1-corrections-20261014` |
| Evidence | `docs/reviews/qw1_review_evidence/verification_2026-10-14.json` |

Authority remains the approved QW-1 brief and RUL-2026-10-12-016 at the separate planning SHA, plus the existing repository role/review/implementation workflows. The prior review permitted a narrow correction recheck when the scope and base relationship remained valid; both conditions hold.

The correction is four files, +63/-5; the full branch is the same four paths, +1132/-1. The implementation script changes only `_selftest_new`; the rest of the module's AST is identical to `c79c6af`, including all runtime CLI and validation paths. The template and golden each gain one direct dependency; documentation gains two explanatory bullets. The supplied three SHA-256 values match.

Main has 16 commits since the original base, affecting captures/results, crafting-cache art/manifests, and the source-drift sentinel. Its changes do not overlap the implementation paths, `state/workstreams/`, the template's existing resource files, or the applicable authority/review workflows. No main advance is treated as contract adoption or live-game authority.

## R1 — CLOSED

`production.hidden_run.depends_on` now contains both `build.manifest` and `review.independent`. The regenerated golden has the same edge. The multi-variant rehearsal also adds `build.manifest_variant_b` to the hidden run's dependencies, and the documentation tells coordinators to preserve every build edge when splitting variants.

Independent CLI probes used a disposable archive of the exact frozen tree. The original failing recipe was reproduced without changing the other initial task states. Additional cases used explicitly synthetic existing evidence files to exercise status/dependency mechanics, not real content acceptance or Git commitment.

| Fixture state | Targeted validate | CLI init | Result |
| --- | --- | --- | --- |
| Build `PLANNED`, review `SKIPPED`, hidden run `READY` | 1 | 1 | Names unfinished `build.manifest (PLANNED)`; original bypass closed |
| Build `COMPLETE`, review `PLANNED`, hidden run `READY` | 1 | 1 | Names unfinished `review.independent (PLANNED)` |
| Build `COMPLETE`, review `SKIPPED`, hidden run `READY` | 0 | 0 | Init packet includes build as completed upstream evidence |
| Build `COMPLETE`, review `COMPLETE`, hidden run `READY` | 0 | 0 | Init packet includes build as completed upstream evidence |
| Primary build complete, variant B `PLANNED` and explicitly required, review skipped | 1 | 1 | Names unfinished variant B |

The unchanged meanings of `SKIPPED` and `SUPERSEDED` are retained. The fix expresses the prerequisite in the coordination graph, as requested.

Negative control: substitute only the old `c79c6af` template in a disposable tree and run the corrected selftest. It exits 1 with **five R1 checks failing**, plus the expected golden-mismatch check. This proves the added checks detect the original defect rather than passing regardless of the new edge.

## R2 — CLOSED

The new test labels now correctly describe missing/existing source files and existing repository-path evidence. The sandbox test names its actual path restriction. The new workflow paragraph explicitly says that validation checks safe repository-relative existence, accepts untracked files, and leaves commitment as a handoff/review obligation. Baseline labels are preserved, and no Git operation or validator change was added.

The independently counted selftest total is **142 = 66 baseline + 65 original QW-1 + 11 correction checks**. This matches the corrected handoff. Commitment, approval and semantic truth of evidence remain workflow responsibilities; a green validator is not proof of them.

## Verification and main compatibility

- Exact target `--selftest`: exit 0, 142 passing checks, 0 failures.
- Exact target `render --check`: exit 0. `py_compile` passes with bytecode outside the checkout. `git diff --check` passes.
- Two independent `new example_quest --title "Example Quest" --type quest --json` previews are byte-identical, equal the committed golden, and change no file in the archived tree.
- Isolated `new review_fixture --write --json`: exit 0, stdout equals written JSON, targeted validation and render check exit 0, and blocked design init exits 1.
- Creation adds only the new `roadmap.json` and `ROADMAP.md` and changes only the shared `INDEX.md`. All other files, including One Perfect Crop and global session state, remain byte-identical.
- Runtime module AST is unchanged except `_selftest_new`; no validator/init/new semantics were modified to obtain the result.
- `git merge-tree --write-tree --name-only 057acddb986b50e486ccf550fac00b68fff51490 1b14f9974912e8cf0d00dc9ca3ad1b34ca7e10b9` exits 0 without conflicts and yields tree `e04219ce5476bd18804840b4e42b58eb2e8ee658`. Its delta from current main is exactly the four approved implementation paths.
- In a disposable archive of that merge tree, selftest again exits 0 with 142 checks and render check exits 0. The gate run changes no archived files. No merge commit or branch ref was created for this simulation.

**Existing all-workstreams validation debt remains:** `validate --all` exits 1 for One Perfect Crop's `launch.finalization` evidence[5], which names absent `push/54_one_perfect_crop_launch_final.json`. Exit, stdout and stderr match across the baseline script, current main and simulated integration tree; the exact target reports the same failure. This is separate historical evidence disposition, not a QW-1 regression. No repository-wide all-green claim is made, and this review introduces no general validation bypass.

The first review's accepted limitations remain: local `--write` is not transactional and the existing piped `next` may emit BrokenPipeError. They are outside this correction. Unrelated art, doctrine, law, pack and Forge gates were not rerun because their sources are unaffected. No browser/Android/live-game checks are applicable to this offline CLI correction. Scratch probes and synthetic workstream state are not committed.

## Integration handoff

1. Obtain director acceptance and explicit integration authority. The approved brief ends at a frozen review handoff, and the Release Auditor role has audit/recommendation authority rather than merge authority by default.
2. Immediately before integration, reverify main and confirm Fable still points to `1b14f9974912e8cf0d00dc9ca3ad1b34ca7e10b9`. This review's merge rehearsal is against main `057acddb986b50e486ccf550fac00b68fff51490`; if main advances, inspect the new delta and repeat the affected compatibility gates. A changed implementation SHA needs a delta review.
3. Integrate the exact reviewed implementation through the normal authorized Lane A process. Preserve the original review/evidence, this correction review/evidence and the updated session handoff. The ChatGPT review branch contains only those documentation changes over the frozen target. Keep the planning branch separate.
4. Confirm post-integration selftest, golden/projection consistency and unchanged scope. Report the known One Perfect Crop failure explicitly rather than hiding its exit code or repairing it inside this package.
5. Stop at the QW-1 integration checkpoint. QW-0A continuation and QW-0B need separately bounded work; QW-2 through QW-5 and Quest Studio are not automatic follow-ons. Mandatory-workstream policy and One Perfect Crop evidence disposition remain separate decisions.

QW-0A remains `BLOCKED_BY_SOURCE_ADOPTION`; its earlier report/review integration satisfied QW-1's sequence prerequisite. No global September Forge projection, real quest workstream, reward, gameplay or publication record was changed. Rare Jewels reconciliation remains separate. Live-game requests/writes: 0/0; credentials: none.
