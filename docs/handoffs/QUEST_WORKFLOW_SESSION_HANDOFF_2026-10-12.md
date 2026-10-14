# Quest Creation Workflow Optimization — session handoff

Updated 2026-10-14 UTC after independent correction re-review of QW-0A extractor slice A.

## Current checkpoint

**QW-1 is INTEGRATED and independently verified at main `1da18301e8e4660cedf3daa3e80893a2ac918f2b`.** R1 and R2 are closed. The director's accepted integration checkpoint is recorded; no further QW-1 correction or merge is pending at this SHA.

QW-0A's investigative report/review remains integrated with outcome `BLOCKED_BY_SOURCE_ADOPTION`. **Extractor slice A correction at frozen Fable `091dc95a6a8533f53b26bf46af15c6f6cd77f448` has verdict CHANGES_REQUESTED.** QW0A-A-R2 and R3 are closed. R1 remains open: rejected preprocessing still inherits inner optional/default facts that incorrectly remove required inputs. Diff-gate slice B waits for A's accepted review/integration. No continuation implementation has been integrated.

| Item | Exact reference |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Verified QW-1 integration / slice A base | `1da18301e8e4660cedf3daa3e80893a2ac918f2b` |
| Current main at slice A correction review close | `f083ddecfd400431ae2160d814546dab30f54f15` |
| First merge parent / pre-merge main | `057acddb986b50e486ccf550fac00b68fff51490` |
| Second merge parent / integrated review record | `6c4af7f8d568c9789b92e83f413cefb83c29f131` |
| Reviewed implementation | `fable/qw1-workstream-starter-20261012@1b14f9974912e8cf0d00dc9ca3ad1b34ca7e10b9` |
| Previous implementation | `c79c6afadeb3388d7d2823cd084405661e398f97` |
| Implementation base / merge-base | `fe4e69cbf88b49665c9ddcd6189e9ab4c833f123` |
| Original independent review | `8d91512d98165a031f8e04859e8d45c862320080` |
| Separate approved planning source | `chatgpt/quest-workflow-skyglass-retrospective-20261012@c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Approval | RUL-2026-10-12-016; director acceptance/integration authorization reported for 2026-10-14 |
| Checkpoint record branch | `chatgpt/qw1-integration-checkpoint-20261014` |
| QW-1 checkpoint record SHA | `7a9578d42dfff0e0cbb61c6430c84f3bc30436eb` |
| Current brief/sequence branch | `chatgpt/qw0a-continuation-brief-20261014` |
| Continuation implementation contract | `state/prompt_quest_workflow_qw0a_continuation_2026-10-14.md` |
| Committed continuation brief SHA | `2d2390e769587bc307b83971923ba4700a63e80d` |
| Frozen slice A correction | `fable/qw0a-extractor-fidelity-20261014@091dc95a6a8533f53b26bf46af15c6f6cd77f448` |
| Previous target / direct parent | `1bbc833f093c0b747e9abef741b21067ae1ed3df` |
| Previous independent review | `3f64e065e5f79ab0ce1daad42d9fcbadc2e75d0a` |
| Current review record branch | `chatgpt/review-qw0a-extractor-corrections-20261014` |

The brief branch builds on the QW-1 checkpoint record. This correction review branch anchors to frozen `091dc95` and carries forward the original slice-A review/evidence and QW-1 integration evidence blob-identically. Read the continuation brief with `git show 2d2390e769587bc307b83971923ba4700a63e80d:state/prompt_quest_workflow_qw0a_continuation_2026-10-14.md`; it need not be present in the implementation checkout. Main, Fable, brief and planning refs were reverified. The planning branch remains separate.

Main now includes the signal-only sentinel commit `83690aa` and the unrelated isolated-art/BBE documentation merge `f083dde`. The art-specific ruling changes no extractor or adoption policy. There is no slice-A path overlap. Preserve these main changes; neither replaces either audit pin. The frozen implementation was not rebased.

## QW-0A slice A correction review checkpoint

Current review: `docs/reviews/QW0A_EXTRACTOR_FIDELITY_CORRECTION_REREVIEW_2026-10-14.md`. Evidence: `docs/reviews/qw0a_extractor_review_evidence/correction_verification_2026-10-14.json`. Original review/evidence remain under their original paths, recording the prior target and three findings.

- **QW0A-A-R1 — OPEN:** the original predicate/nested-nullability cases now pass, but a recognized callback that maps undefined to null still inherits `.optional()` or `.default(7)`/`.prefault(7)` from a nonnullable inner number. All three required inputs disappear from `required_on_create` with no gap. The classifier's `False` result is ignored. Conversely, pass-through default/prefault positive cases are incorrectly classified as rejected, so a blanket removal would regress valid fallbacks. Make classification, emitted facts and derived checks agree.
- **QW0A-A-R2 — CLOSED:** nested bounds/coercion no longer leak in constructor/entity fixtures or the two pinned `item.craftingRequirements` fields; real outer controls pass.
- **QW0A-A-R3 — CLOSED:** the 13/15-file read sets reproduce and match exact Git hashes; legacy reads are covered, derived rows link to source anchors, and provenance fault probes are detected.

Independent verification reproduces 43 passing author tests; six failures against `1bbc833`; 20 failures/20 errors against the base extractor; all 16 extraction hashes/read sets; all 6,243 inventory rows; and repeatability. Historical gates, coherence gates, deterministic skill packages and protected scope pass. The reviewer added scratch-only omission probes, including valid pass-through controls. Full pinned source was read, never executed.

Fable's next action is a focused R1 correction on its existing branch, followed by regenerated evidence/package, affected/required gates and a new frozen remote head. Closed R2/R3 need no new implementation unless affected. Do not integrate `091dc95` or begin B. ChatGPT independently re-reviews before the concrete acceptance/integration step. QW-1 stays closed; source adoption stays separate.

## Independent integration verification

At the QW-1 checkpoint, live main, Fable, review and planning refs matched the reported integration. The integration has exactly the expected two parents. Its tree matches a clean merge of those parents. The approved planning commit is not an ancestor of integration and its branch remains separate. These are the retained QW-1 verification results; current main is recorded above.

All four implementation blobs on main match reviewed `1b14f99`: `scripts/content_workstream.py`, both files in `scripts/workstream_templates/`, and `docs/workflows/CONTENT_WORKSTREAM.md`. The other five integrated paths are the review/evidence files and this handoff. Original review/evidence blobs still match `8d91512`; its older handoff was superseded by the accepted correction checkpoint.

Independently rerun on the actual integration tree:

- `content_workstream.py --selftest`: exit 0, **142 passing / 0 failing** checks.
- `render --check`: exit 0.
- Example preview with `--json`: exit 0, byte-identical to the committed golden, SHA-256 `ef222f782f762e5194c101fa6cfa6e6041851c96eab46ccdd810210dd7de97d8`.
- Python byte compilation: passes, with bytecode outside the checkout.
- `validate --all`: exit 1 for the unchanged One Perfect Crop evidence-pointer failure; stdout/stderr and exit are byte-identical to the pre-merge main script.

No `state/workstreams/` change or real workstream was integrated. The three global surfaces `state/digest.json`, `state/active-context.md`, and `state/status.json` are blob-identical before/after the merge. This audit changed no implementation or existing workstream.

Fable also reports passing pack/law/doctrine gates, with the existing five law warnings. Those unrelated gates were not repeated in this checkpoint audit. The commit graph establishes the intended merge and ancestry; the reported non-force push method is author-attested.

Machine-readable evidence: `docs/reviews/qw1_review_evidence/integration_verification_2026-10-14.json`.

## Review history and remaining limits

R1 was fixed by making hidden execution depend directly on build and review, including every explicitly split build variant. The original bypass now refuses validation/init; legitimate positive cases include build evidence. R2 corrected new test labels and documentation: path existence is checked, Git commitment is a handoff/review obligation. Runtime validator/status semantics are unchanged.

The original and correction reports remain at:

- `docs/reviews/QW1_WORKSTREAM_STARTER_INDEPENDENT_REVIEW_2026-10-12.md`
- `docs/reviews/QW1_WORKSTREAM_STARTER_CORRECTION_REREVIEW_2026-10-14.md`

The starter is optional and now available on main. The known nontransactional local `--write` and existing piped-`next` BrokenPipeError remain disclosed limitations.

One Perfect Crop's `launch.finalization` evidence[5] still names removed `push/54_one_perfect_crop_launch_final.json`. Its archival/repoint disposition remains a separate task. Do not claim repository-wide validation is green or introduce a general bypass.

## Orchestration and remaining implementation sequence

The user asked ChatGPT to plan and direct the remaining implementation, issue Claude instructions, and independently review code. Brief authorship is therefore settled: ChatGPT owns the brief and review/integration instructions; Fable owns implementation. The new continuation brief is an orchestrator-issued engineering assignment within QW-0A, not a new director ruling or adoption-policy change. Routine details inside that boundary need no separate authorship decision.

Use `state/prompt_quest_workflow_qw0a_continuation_2026-10-14.md` for the executable A/B contract. It incorporates R1/R2 from `docs/reviews/QW0A_CONTRACT_ALIGNMENT_INDEPENDENT_REVIEW_2026-10-12.md`: full source-cited inventories at both pins, union field existence/type coverage, nullability tightening, and preserved refusal of genuinely required new inputs. Main `fe4e69c` already integrated report `5fefb70b88f140c3212d0b9d94209e70be44f2bb` and review `e2c10ee1717d1311951bc8a7f6e621229ebf4b5f`.

| Sequence / status | Deliverable and next gate |
| --- | --- |
| QW-1 — CLOSED | Keep the integrated starter and its review evidence. No further implementation or integration is pending. |
| QW-0A A — CHANGES_REQUESTED | R2/R3 closed. Correct the remaining R1 omission/default contradiction on Fable's existing branch; regenerate evidence/package and return a frozen SHA. Re-review precedes accepted integration. |
| QW-0A B — QUEUED AFTER A | Harden the existing diff gate, reproduce R2 failures and preserve positive/negative controls. Separate branch, frozen review and integration. |
| QW-0A adoption decision — AFTER A/B EVIDENCE | ChatGPT prepares the exact prospective delta and policy decision packet. User decides any change to D-adopt-gate/source selection; no automatic removal allowance. |
| QW-0A alignment — CONDITIONAL | Once adoption requirements are satisfied, separately brief canonical contracts plus Python/Forge parity and compatibility tests at the chosen pin. Only this outcome can establish alignment. |
| QW-0B — SEPARATE, NOT STARTED | Verify the current Forge version mismatch; issue a narrow version-source/build/release brief. Do not fold a version release into A/B. |
| QW-0 follow-ups — SEPARATE, NOT STARTED | Crafting-relation readback needs its own source/registry scope; spent-manifest archive and historical audit need their own evidence-preserving boundary. OPC pointer disposition belongs here or in an explicitly selected standalone repair. |
| QW-3 — PLANNED, NOT ACTIVATED | Next wider package in the approved delivery order: honest name/capture coverage, preflight, readback statuses and offline surgical recovery proposals. Scope against existing Forge/capture owners before activation. |
| QW-2 — PLANNED AFTER QW-3 | Deterministic quest blueprint/variant compilation through existing compiler/validator authority, preserving IDs and approved values. Independent schema/graph/authoring acceptance. |
| QW-4 — PLANNED | Separate small combat-evidence, art-provenance and factual-presentation slices; each has its own evidence and acceptance. |
| QW-5 — LATER, GATED | Existing Quest Studio/Forge Next prerequisites, source reconciliation and user decisions remain binding. No second compiler/runner/task authority. |

For every activated slice: Fable implementation → frozen exact-SHA ChatGPT review → correction if needed → applicable acceptance/integration authorization → fresh-main check → bounded post-integration verification and durable handoff. ChatGPT issues the next concrete instruction rather than leaving sequencing to the implementer. QW-2 through QW-5 are planned here, not automatically started.

The schema-sentinel automation is signal-only. Skill packaging can add generated commits to an implementation branch; freeze the actual remote head after accounting for them. Tooling repairs do not adopt generated contracts or remove the historical push/90/93/94 exceptions.

Open user decisions remain separate: D-adopt-gate removal policy; mandatory-at-scale workstreams; OPC push/54 pointer disposition; and Rare Jewels canonical/live reconciliation. No actual quest workstream, global September projection update, live-game action, reward change or publication is part of this assignment.

## Copy/paste next-session handoff

```text
Resume Quest Creation Workflow Optimization in perseverance484/tnr-tools.
Lead: Release Auditor; supporting lens: Engineering Auditor.

QW-1 is integrated and independently verified.
Integration: main@1da18301e8e4660cedf3daa3e80893a2ac918f2b
Current main at correction review close: f083ddecfd400431ae2160d814546dab30f54f15
  (sentinel plus unrelated art-documentation merge; no slice-A path overlap)
Reviewed implementation: 1b14f9974912e8cf0d00dc9ca3ad1b34ca7e10b9
Integrated review: 6c4af7f8d568c9789b92e83f413cefb83c29f131
Checkpoint record: chatgpt/qw1-integration-checkpoint-20261014
  @ 7a9578d42dfff0e0cbb61c6430c84f3bc30436eb
Current brief branch: chatgpt/qw0a-continuation-brief-20261014
  @ 2d2390e769587bc307b83971923ba4700a63e80d
Brief: state/prompt_quest_workflow_qw0a_continuation_2026-10-14.md
Review record branch: chatgpt/review-qw0a-extractor-corrections-20261014

Verify current remote refs; read the existing authority/role files,
this handoff, the QW-1 correction review and integration evidence.
Do not repeat the completed QW-1 implementation or integration.

The approved planning branch remains separate at:
c34f7de572337b0d2cfe397b9331502aa6548e27
Read the plan/briefs and RUL-2026-10-12-016 at that SHA.

QW-1: 142 selftests pass; render/golden/compile checks pass.
validate --all retains only the recorded One Perfect Crop push/54
evidence-pointer failure, unchanged from pre-merge main.

Slice A was delivered on fable/qw0a-extractor-fidelity-20261014.
Reviewed frozen correction: 091dc95a6a8533f53b26bf46af15c6f6cd77f448
Previous target/direct parent: 1bbc833f093c0b747e9abef741b21067ae1ed3df
Previous review: 3f64e065e5f79ab0ce1daad42d9fcbadc2e75d0a
Verdict: CHANGES_REQUESTED; not integrated. R2/R3 CLOSED; R1 OPEN.
Read docs/reviews/QW0A_EXTRACTOR_FIDELITY_CORRECTION_REREVIEW_2026-10-14.md.
Fable corrects R1 on its owned branch: do not inherit safe omission from
inner optional/default facts when preprocessing makes omission fail.
Preserve valid pass-through defaults/prefaults and pinned positive forms.
The review includes exact probes and required acceptance checks.
Preserve both exact source pins and all protected paths in the brief.
Return a new frozen remote head after evidence/package regeneration and
affected/required verification. ChatGPT re-reviews before integration.
Keep schema_diff.py unchanged in A; no contract adoption.

B (gate hardening) follows A's accepted review/integration on a new branch.
Then ChatGPT prepares the concrete adoption decision packet and later
alignment brief. QW-0A remains BLOCKED_BY_SOURCE_ADOPTION throughout A/B.
No new director policy ruling or source adoption is recorded here.

Keep One Perfect Crop pointer repair and Rare Jewels reconciliation
separate. Do not automatically start QW-0B, QW-2 through QW-5,
Quest Studio or an actual quest workstream.

Fable owns implementation; ChatGPT independently reviews frozen SHAs.
Preserve one-writer branches and the global September Forge projections.
No gameplay/reward changes, publication, live requests/writes or credentials.
```
