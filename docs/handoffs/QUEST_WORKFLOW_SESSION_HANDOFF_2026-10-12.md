# Quest Creation Workflow Optimization — session handoff, 2026-10-12

## Current checkpoint

**QW-0A report/review integrated; source adoption remains blocked. QW-1 implemented and independently reviewed: CHANGES_REQUESTED.** Return QW-1 to Fable for the narrow correction below, then review a new frozen SHA before integration.

| Item | Exact reference |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Main verified before and after QW-1 testing | `fe4e69cbf88b49665c9ddcd6189e9ab4c833f123` |
| Approved plan and briefs | `chatgpt/quest-workflow-skyglass-retrospective-20261012@c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Approval | RUL-2026-10-12-016, at the planning SHA |
| QW-1 implementation reviewed | `fable/qw1-workstream-starter-20261012@c79c6afadeb3388d7d2823cd084405661e398f97` |
| QW-1 base / merge-base | `fe4e69cbf88b49665c9ddcd6189e9ab4c833f123` |
| Review/record owner | `chatgpt/review-qw1-workstream-starter-20261012` |
| Independent review | `docs/reviews/QW1_WORKSTREAM_STARTER_INDEPENDENT_REVIEW_2026-10-12.md` |
| Verification record | `docs/reviews/qw1_review_evidence/verification_2026-10-12.json` |

The review branch is anchored on the exact implementation snapshot. Obtain this record's containing commit with `git log -1 --format=%H -- docs/handoffs/QUEST_WORKFLOW_SESSION_HANDOFF_2026-10-12.md`. Review a future implementation by its frozen SHA, never just its branch name.

The planning branch remains separate by director instruction. Read the approved plan, brief and ruling at `c34f7de572337b0d2cfe397b9331502aa6548e27`; they are not present on the reviewed main/implementation tree.

## QW-1 findings and verified progress

**R1 — integration blocker, medium severity:** `production.hidden_run` depends only on optional `review.independent`. Marking review `SKIPPED` permits hidden-run `READY`, targeted validation and init while `build.manifest` is still `PLANNED`. Both commands returned 0 in an isolated exact-tree reproduction. A direct build dependency made both refuse with exit 1. Fable should add that edge, regenerate the golden, and cover skipped/pending/completed review with unfinished/completed builds in regression checks. Keep existing validator/status semantics.

**R2 — verification wording, low severity:** the new tests label missing/existing files “uncommitted/committed.” Actual untracked files pass the unchanged baseline and target validators. Correct the labels and handoff; do not add implicit Git operations or redesign validation. The 131 checks pass, but their split is 66 existing + 65 new, not 51 + 80.

Other verified behavior: dry-run writes nothing; JSON output matches the golden; creation changes only the new roadmap/projection and shared index; existing workstreams and global state remain byte-identical; selected refusal cases make no file changes; render check and byte compilation pass. Existing implementation helpers are unchanged. Missing-resource blocking, title-collision refusal, the golden's location and the optional default are acceptable within the brief.

`validate --all` remains exit 1 because One Perfect Crop's `launch.finalization` evidence[5] names removed `push/54_one_perfect_crop_launch_final.json`. Output and exit are byte-identical to baseline. Keep its archive/repoint decision separate; do not claim the whole repository validates or edit that workstream during QW-1 corrections.

The review does not integrate QW-1, modify Fable's branch or create a real quest workstream.

## Earlier QW-0A checkpoint retained

Main `fe4e69c` merged the QW-0A report `5fefb70b88f140c3212d0b9d94209e70be44f2bb` and independent review `e2c10ee1717d1311951bc8a7f6e621229ebf4b5f`. See `docs/reviews/QW0A_CONTRACT_ALIGNMENT_INDEPENDENT_REVIEW_2026-10-12.md` and its verification record. The former session checkpoint remains available in that review commit's version of this handoff.

The accepted outcome is `BLOCKED_BY_SOURCE_ADOPTION`, not alignment. Its continuation must address the complete extractor correction inventory and diff-gate blind spots recorded as QW-0A R1/R2. Extractor/gate repair does not authorize contract adoption. Integration of the report/review satisfied QW-1's sequence prerequisite; no new requirement to finish every QW-0 follow-up is introduced.

## Next permitted sequence

1. Fable corrects QW-1 R1/R2 within its own branch and returns a new frozen exact-SHA handoff with refreshed base/merge-base, tests and hashes.
2. ChatGPT rechecks the correction surface and generated output. Broaden review only for changed base/architecture/scope.
3. After a clean review and required director acceptance, reverify main immediately before authorized integration. Account for any advance; do not silently merge or carry approval onto an unreviewed rebase.
4. QW-0A continuation/QW-0B remain separately scoped; QW-2 through QW-5 and Quest Studio remain unstarted. Mandatory-at-scale policy and One Perfect Crop evidence disposition remain separate decisions.

## Copy/paste Fable correction handoff

```text
Repository: perseverance484/tnr-tools
Task: QW-1 narrow correction and new frozen review handoff
Owner: Fable / Claude Code; reviewer: ChatGPT

Verify remote main and your branch before editing.
Reviewed main/base: fe4e69cbf88b49665c9ddcd6189e9ab4c833f123
Reviewed branch: fable/qw1-workstream-starter-20261012
Reviewed frozen SHA: c79c6afadeb3388d7d2823cd084405661e398f97
Review branch: chatgpt/review-qw1-workstream-starter-20261012
Read docs/reviews/QW1_WORKSTREAM_STARTER_INDEPENDENT_REVIEW_2026-10-12.md
from that review branch; use its exact fetched commit as the review record.

Approved brief: state/prompt_quest_workflow_qw1_workstream_starter.md
at c34f7de572337b0d2cfe397b9331502aa6548e27.
Keep the planning branch separate. RUL-2026-10-12-016 applies.

R1: production.hidden_run must depend directly on build.manifest as
well as review.independent. Optional SKIPPED review must not bypass
an unfinished build. Regenerate the golden through the CLI. Add
regressions for unfinished/completed build and skipped/pending/
completed review; verify targeted validate and init outcomes.

R2: correct new test labels and handoff claims about committed input.
The unchanged validator checks existence, not Git commitment.
The current 131 checks comprise 66 existing + 65 new. Report fresh
counts after correction. Do not add implicit Git operations.

Run selftest, deterministic preview/golden and write rehearsal,
targeted validation, render --check and relevant regressions.
Compare validate --all with the base and report its existing One
Perfect Crop missing-evidence failure honestly; do not repair that
workstream within this task. Keep global session state untouched.

Return a new frozen SHA, base/merge-base, changed paths, regenerated
hashes, unmasked test exit codes and R1/R2 disposition. Stop for
independent exact-SHA review; do not integrate or start later work.

No gameplay/reward changes, publication, live-game requests/writes
or credentials. Rare Jewels reconciliation stays separate.
```

Do not run `session_open.py` or `session_close.py` to update the global September Forge projections for this workflow. Preserve one-writer ownership and the existing TNR authority system.
