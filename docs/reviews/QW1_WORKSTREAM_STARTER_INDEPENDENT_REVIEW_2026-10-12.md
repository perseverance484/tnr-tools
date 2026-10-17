# QW-1 workstream starter — independent review, 2026-10-12

**Verdict: CHANGES_REQUESTED.** One confirmed template dependency defect blocks integration. The implementation otherwise stays within the approved optional scaffold scope. Correct the verification wording in the same narrow correction pass.

Reviewer: ChatGPT, Release Auditor with Engineering Auditor lens. Implementation remains Fable-owned. No implementation fix, integration, game operation or reward change was performed by this review.

## Exact target and authority

| Item | Verified reference |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Main / merge-base | `fe4e69cbf88b49665c9ddcd6189e9ab4c833f123` |
| Frozen implementation | `fable/qw1-workstream-starter-20261012@c79c6afadeb3388d7d2823cd084405661e398f97` |
| Approved planning source | `chatgpt/quest-workflow-skyglass-retrospective-20261012@c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Brief | `state/prompt_quest_workflow_qw1_workstream_starter.md` at the planning SHA |
| Plan / ruling | `docs/design/QUEST_CREATION_WORKFLOW_IMPROVEMENT_PLAN_2026-10-12.md`, QW-1; RUL-2026-10-12-016 at the planning SHA |
| Review branch | `chatgpt/review-qw1-workstream-starter-20261012`, anchored on the exact frozen implementation |
| Verification record | `docs/reviews/qw1_review_evidence/verification_2026-10-12.json` |

Remote main, implementation and planning refs matched these values at initialization and after testing. The delta is four files, +1074/-1. The three supplied SHA-256 values match. The planning branch stays separate; the plan, brief and ruling were read at their exact planning SHA, not assumed to exist on main.

Main `fe4e69c` integrates the QW-0A report and independent review. This satisfies the QW-1 sequencing prerequisite. QW-0A remains `BLOCKED_BY_SOURCE_ADOPTION`; integration of that investigative outcome is not contract alignment or adoption, and does not require every QW-0 follow-up to finish before QW-1.

## R1 — Optional review can bypass the unfinished manifest build

**Confirmed defect; medium severity; integration blocker.**

Location: `scripts/workstream_templates/multisession_v1.json`, `production.hidden_run.depends_on` at line 179, together with the explicitly optional `review.independent` at lines 163–170. The golden example contains the same graph.

The hidden-run task depends only on independent review. Under the unchanged validator, `SKIPPED` satisfies a dependency and does not require that skipped task's own dependencies to be settled. Skipping optional review therefore removes the only effective build prerequisite. It also removes the build from the hidden-run init packet's direct upstream outputs.

Reproduction against the frozen CLI in a disposable archive of its tracked tree:

1. Create `review_fixture` using `new --write`.
2. Leave `build.manifest` `PLANNED` and all other prerequisite tasks at their initial statuses.
3. Set `review.independent` to `SKIPPED` and record the reason that this fixture scope does not require independent review.
4. Set `production.hidden_run` to `READY`.
5. Run targeted `validate` and `init review_fixture --task production.hidden_run`.

**Actual:** both exit 0. The init packet presents an executable hidden operator run although the build is unfinished and has no manifest evidence. Nothing was run against the game. This is a misleading readiness result in the new coordination graph, not an automatic game execution vulnerability.

**Expected:** hidden execution remains dependent on the completed build whether optional review is required, pending or skipped. The brief requires realistic stage dependencies and rejection of false `READY` claims while preserving existing validation semantics.

**Smallest correction:** make `production.hidden_run` depend directly on both `build.manifest` and `review.independent`; regenerate the golden through the CLI. Do not change `validate`, `init` or the meaning of `SKIPPED`. Adding the direct build edge only to the disposable fixture made both commands exit 1 with `depends on unfinished build.manifest (PLANNED)`.

Add focused regression coverage: skipped review plus unfinished build must refuse validation/init; a properly evidenced completed build with review still pending must refuse; completed build plus legitimately skipped or completed review must permit initialization. Preserve existing dependency rewiring when splitting tasks or adding variants.

Reproduction recipe (writes only the temporary archive):

```bash
review_tree=$(mktemp -d)
git archive c79c6afadeb3388d7d2823cd084405661e398f97 | tar -x -C "$review_tree"
python3 "$review_tree/scripts/content_workstream.py" new review_fixture --title 'Review Fixture' --type quest --write
python3 - "$review_tree" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1]) / 'state/workstreams/review_fixture/roadmap.json'
r = json.loads(p.read_text())
tasks = {t['id']: t for t in r['tasks']}
tasks['review.independent']['status'] = 'SKIPPED'
tasks['review.independent']['resume_note'] = 'Independent review is not required for this fixture scope.'
tasks['production.hidden_run']['status'] = 'READY'
p.write_text(json.dumps(r, indent=2) + '\n')
PY
python3 "$review_tree/scripts/content_workstream.py" validate state/workstreams/review_fixture/roadmap.json
python3 "$review_tree/scripts/content_workstream.py" init review_fixture --task production.hidden_run
```

## R2 — Verification claims overstate what is checked

**Stale test/report wording; low severity; correction requested with R1.** This is not a newly introduced validator regression and does not authorize Git-aware validation.

At `scripts/content_workstream.py` lines 1366–1370, the test calls a nonexistent path an “uncommitted” source and a newly written temporary file “committed.” No Git repository/commit is created by that test. Line 1381 similarly calls existing path evidence committed evidence.

Independent control: create an actual untracked repository-relative source, clear the design blocker, add the path to required resources, and mark the task `READY`. `git ls-files` returns no tracked path, but both validation and init exit 0. The baseline validator also accepts the same fixture. The existing code checks path safety and existence; commitment remains a workflow obligation verified during handoff/review.

Correct the new test labels and handoff to distinguish **missing versus existing repository-relative files** from **uncommitted versus committed sources**. Keep the requirement to commit durable sources, but do not claim the unchanged validator proves commitment or approval. Preserve the socket-free/no-implicit-Git boundary.

The total of **131 passing checks** is correct. Independently counted breakdown: **66 existing + 65 new**, not 51 + 80. Correct the handoff count. The seven author-reported mutation checks were not independently rerun; this review used independent CLI and dependency probes instead.

## Findings that do not require redesign

| Review question | Assessment |
| --- | --- |
| Stage set and initial statuses | Appropriate coordination stages; all start `PLANNED`/`BLOCKED`, with empty evidence. No fabricated approvals or gameplay values. R1 is the required dependency correction. |
| Missing template task pointer | Dropping a missing required-resource pointer while naming it in a blocker and setting the task `BLOCKED` follows the brief and preserves the existing validator. Top-level shared-resource omissions produce warnings; they are not automatically per-task blockers. |
| Title collision strictness | Reasonable for the existing case-insensitive slug/title lookup. Preventing ambiguity needs no director decision. |
| Golden under `scripts/` | Appropriate adjacent test fixture, outside real `state/workstreams/`. No relocation needed. |
| Optional workstreams | Correct approved default. Whether to make them mandatory at scale remains a separate policy decision. |
| Nontransactional `--write` | Disclosed local recovery limitation, not a blocker for this bounded pass. It performs no game or Git operation. Do not describe partial render failure as an atomic no-write refusal. |
| Existing `next \| head` BrokenPipeError | Outside the changed code; not a QW-1 blocker. |

## Independently verified evidence

- `python3 scripts/content_workstream.py --selftest`: exit 0, 131 checks, no failures. Baseline selftest: exit 0, 66 checks.
- `python3 scripts/content_workstream.py render --check`: exit 0; existing projections current.
- `validate --all`: exit 1 with the One Perfect Crop missing `push/54_one_perfect_crop_launch_final.json` evidence pointer. Exit, stdout and stderr are byte-identical to baseline. This is documented pre-existing debt, not a new QW-1 regression; no global all-green claim is made.
- AST comparison: all pre-existing function/class definitions except the intentionally extended `main` and `selftest` are unchanged. Existing validation/render/init helpers were not relaxed.
- Disposable tracked-tree CLI rehearsal: preview writes no files and JSON equals the golden; `--write --json` stdout equals the written roadmap; targeted validation and render check exit 0; initial blocked design init exits 1.
- Creation adds only the new `roadmap.json` and `ROADMAP.md` and changes only the shared `INDEX.md`. Every other archived file, including One Perfect Crop and the three global session surfaces, remains byte-identical.
- Duplicate slug/title, traversal, unsafe title and invalid type refuse with expected exit 1/2 and no file changes.
- The independent R1 bypass and direct-edge control reproduce as described; the R2 untracked-source control passes the baseline and target validators.
- `py_compile` passes, with bytecode written outside the reviewed tree. The reviewed checkout was clean before adding these review records.

The author's art/coherence gates were not rerun: no art, doctrine, law, pack or Forge source changes in this delta require them. Browser/Android/live-game validation is inapplicable to this offline CLI change. Scratch probe scripts and temporary workstreams are not committed.

## Next permitted sequence

1. Fable applies R1 and the R2 evidence-wording corrections on its own implementation branch. Preserve the approved scope and planning-branch separation.
2. Fable regenerates the golden, runs the relevant positive/negative gates, compares existing-workstream validation with the current base, and returns a new frozen SHA plus exact base/merge-base, changed files, hashes and unmasked exit codes.
3. ChatGPT independently reviews the new exact SHA. A narrow recheck is sufficient if changes stay within R1/R2 and the base/architecture assumptions still hold.
4. After a clean review and required director acceptance, reverify main immediately before authorized integration. If main has advanced, assess its delta and rerun affected checks; do not carry this verdict onto an unreviewed rebased commit.
5. Keep One Perfect Crop's historical evidence pointer as a separate disposition/archival decision. Do not repair an existing workstream in the QW-1 correction. QW-0A continuation/QW-0B need their own bounded scope; QW-2 through QW-5 and Quest Studio do not start automatically.

No global September Forge projection was updated. Rare Jewels remains a separate canonical/live reconciliation issue; no rewards, gameplay, publication, credentials or live-game requests/writes are involved.
