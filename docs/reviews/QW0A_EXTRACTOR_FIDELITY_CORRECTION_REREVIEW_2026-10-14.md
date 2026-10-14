# QW-0A continuation, slice A — correction re-review

**Verdict: CHANGES_REQUESTED. QW0A-A-R2 and R3 are closed; QW0A-A-R1 remains open.** The original regression cases now pass. A remaining error in applying the omission classifier still labels some required inputs as safely omissible. Correct this before A integration or slice B. Overall QW-0A remains `BLOCKED_BY_SOURCE_ADOPTION`.

| Item | Exact reference |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Frozen correction target | `fable/qw0a-extractor-fidelity-20261014@091dc95a6a8533f53b26bf46af15c6f6cd77f448` |
| Direct parent / previous target | `1bbc833f093c0b747e9abef741b21067ae1ed3df` |
| Implementation base / merge-base with main | `1da18301e8e4660cedf3daa3e80893a2ac918f2b` |
| Fresh main at re-review | `f083ddecfd400431ae2160d814546dab30f54f15` |
| Previous independent review | `chatgpt/review-qw0a-extractor-20261014@3f64e065e5f79ab0ce1daad42d9fcbadc2e75d0a` |
| Governing continuation brief | `chatgpt/qw0a-continuation-brief-20261014@2d2390e769587bc307b83971923ba4700a63e80d`, `state/prompt_quest_workflow_qw0a_continuation_2026-10-14.md` |
| Separate approved planning source | `c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Game-source pins | `bdec2883748f029a0ecb93505adfdcbae6851fe9`, `585534d7eb21d6f0dd678d5c3eb92662f611d39b` |
| Reviewer | ChatGPT — Release Auditor, Engineering Auditor lens |
| Review branch | `chatgpt/review-qw0a-extractor-corrections-20261014`, based on the frozen correction |

Remote target, direct parent, merge-base, brief and planning refs were verified. The correction changes the reported ten paths. Review used an isolated ChatGPT worktree and full pinned source archives. No Fable branch, adopted contract or game source was modified.

Main has advanced beyond the handoff's `83690aa` through merge `f083dde` of isolated art-generation/BBE icon documentation. The new ruling is art-specific and changes no extractor, adoption policy or slice-A path. The earlier sentinel changes only `docs/DRIFT.md` and `state/schema_sentinel.json`. Preserve both unrelated changes; they do not replace the two audit pins. Recheck main before any eventual integration.

## Disposition

| Finding | Result |
| --- | --- |
| QW0A-A-R1 — omission inference | **PARTIALLY FIXED / OPEN.** The original unsafe-predicate and nested-nullability probes pass. The bounded classifier's rejection is not applied to emitted optional/default facts, and its pass-through classification overlooks defaults. See below. |
| QW0A-A-R2 — nested bounds/coercion | **CLOSED.** Both constructor/entity negative cases and outer-bound/coercion positive cases pass. At both source pins, `item.craftingRequirements` now has no leaked coercion, integer restriction or numeric bounds. |
| QW0A-A-R3 — provenance | **CLOSED.** Actual reads are traced and hashed, including legacy readers. All 28 source hashes match pinned Git objects; derived/aggregate links reach source anchors. Coverage checks detect missing anchors, missing/dangling inputs and read-set failures. |

## Remaining blocker: QW0A-A-R1 — rejected omission is still emitted as safe

**Confirmed defect, medium.** At target `091dc95`, see `skills/building-tnr-content/scripts/schema_extract.py:1109-1118` (classification), `1256-1268` (application), and `1537-1538` (derived required inputs).

`parse_expr2` unwraps a preprocessor and initially copies the inner schema's facts. `extract_entity` then handles `omit is True` and `omit is None`, but does nothing for **`omit is False`**. Consequently, facts copied from the inner schema can contradict the classifier's known result for an omitted outer input.

Three additional fields in a scratch copy of the committed positive fixture reproduce the problem:

```typescript
rejectedOptionalInput: z.preprocess((v) => (v === undefined ? null : v), z.number().optional()),
rejectedDefaultInput: z.preprocess((v) => (v === undefined ? null : v), z.number().default(7)),
rejectedPrefaultInput: z.preprocess((v) => (v === undefined ? null : v), z.number().prefault(7)),
```

For each field, the recognized callback maps omitted `undefined` to `null`. The inner schemas are nonnullable. Their optional/default behavior applies to `undefined`, which this callback replaces. The classifier returns `False` with the explanation “preprocess maps undefined to null but the inner schema is not nullable.”

| Field | Actual emitted facts | Actual 45g result |
| --- | --- | --- |
| `rejectedOptionalInput` | `optional: true`, `nullable: false`, no omission explanation | Absent from `required_on_create.item` |
| `rejectedDefaultInput` | `optional: false`, `nullable: false`, `default: 7` | Absent from `required_on_create.item` because `default` is present |
| `rejectedPrefaultInput` | `optional: false`, `nullable: false`, `default: 7` | Absent from `required_on_create.item` because `default` is present |

All CLI modes (`--ctors`, `--entities`, `--checks`, `--gaps`) exit 0. None of these fields receives a gap diagnostic. This is the same required-input safety boundary as R1, now in the connection between classification and contract emission. It is not an additional pinned-source discrepancy: the two audited pins continue to use the recognized positive forms.

There is a related positive-control requirement. For callbacks that pass `undefined` through, simple inner `.default(7)` and `.prefault(7)` do provide omission fallbacks:

```typescript
acceptedDefaultInput: z.preprocess((v) => (v === "" ? null : v), z.number().default(7)),
acceptedPrefaultInput: z.preprocess((v) => (v === "" ? null : v), z.number().prefault(7)),
```

The current classifier also returns `False` for these, because it checks only `optional`/`nullish`, although emitted default facts correctly keep them out of `required_on_create`. Therefore, blindly applying every existing `False` result by deleting defaults would create a regression. The callback outcome, inner-schema acceptance and emitted omission facts must agree. Simple pass-through `.optional()` and undefined-to-null with `.nullable()` remain valid positive controls and were also checked.

This review reasons from the exact callback text, existing contract meanings and the extractor's own classification/output. No TypeScript, game runtime or Zod runtime was executed. The release-pin behavior is not being newly inferred from these synthetic cases.

### Required correction and acceptance

Keep the correction within the extractor/tests/fixtures/report/package boundary on Fable's current branch:

1. Make the recognized omission result authoritative for the **outer field's** emitted facts. A copied inner `optional` or `default` must not advertise safe omission when preprocessing prevents that behavior.
2. Account for supported default/prefault behavior when classifying the callback outcome. Preserve actual pass-through fallbacks and the existing pinned positive forms. Keep unsupported semantics explicit and conservative; do not expand this into a general Zod evaluator.
3. Add CLI regressions for all three rejected cases above: no false omission acceptance in 45d, all three present in `required_on_create.item`, and consistent classification/diagnostics. Add the two pass-through default controls so a blanket removal cannot pass. Retain the original R1/R2 cases.
4. Keep contract emission and the derived checks consistent. A change only to `required_on_create` that leaves 45d falsely advertising an omission fallback is insufficient for slice B. Use the existing contract meanings; disclose any proposed format/consumer extension before relying on it, as required by the brief.
5. Regenerate both-pin evidence and deterministic skill packaging. Report whether the pinned structural outputs change; do not presume they do. Show the added negative cases fail against `091dc95` for the intended reason. Re-run affected and required gates, then return the actual frozen remote head after automation settles.

R2 and R3 do not need new implementation work unless this correction changes their relevant code/evidence. Review will focus on the omission result and downstream facts while checking that the closed findings, pins, provenance and protected boundaries remain intact.

## Independent verification

| Check | Result |
| --- | --- |
| Target regression suite | exit 0; 43/43 |
| Same suite against `1bbc833` | exit 1; exactly six failures |
| Same suite against main-base extractor | exit 1; 20 failures, 20 errors, three passes |
| New reviewer omission probes | all CLI modes exit 0; three required inputs are still incorrectly excluded; four positive controls recorded |
| Inventory producer | exit 0; A 1,923 / B 2,417 / C 1,903 rows; comparison objects exactly match committed inventory |
| Extraction runs / repeatability | all 16 runs exit 0 and match structural hashes/read sets; all eight repeated corrected runs byte-identical for identical inputs |
| Source provenance | 13 old-pin and 15 release-pin hashes match Git objects; trace, `--reads`, committed coverage and reproduced coverage agree |
| Provenance links | every derived/aggregate row reaches a source anchor; five targeted missing-provenance probes are detected |
| Pinned `craftingRequirements` | both arrays retain `default: []`, optionality/nullability, and no nested bounds/coercion |
| Unchanged candidate gates | all 16 gate results reproduce, comparing exits and output line multisets; corrected adoption diffs still refuse as expected |
| Existing sector/additive/bad-invariant fixtures | expected exits 1 / 0 / 1; stamped invariants exit 0 |
| Historical exception gates | exit 0 each; 56E/25W, 4E/3W, 4E/3W ledgers hold |
| Factory / validator laws | exit 0; 20/20 and 4 asserted / 0 failed |
| Packs, lawmap, doctrinemap, doctrine render, catalog | exit 0; lawmap retains five existing warnings |
| Deterministic skill packs | two builds reproduce both committed ZIPs; content ZIP 401,513 bytes, all 91 members match source; both below 2 MiB |
| Compilation / protected paths | three Python files compile outside the tree; full branch delta stays within A's allowlist |

Full-file hashes depend on provenance date/source label; structural comparisons exclude only `_provenance`. Existing gate change-line ordering is not deterministic, so byte-order equality is not claimed. Full source read sets and all comparison objects reproduce independently. The author's Actions run IDs were not queried; the actual remote freeze and deterministic local package results were checked.

Reviewer setup note: an initial attempt to redirect the pack producer's output outside its repository root failed at its relative-path logging assertion after one scratch ZIP. Running the unchanged producer at its normal paths in the isolated ChatGPT worktree reproduced both ZIPs twice and left tracked content unchanged. This is not a product finding or a suppressed gate failure.

Machine evidence: `docs/reviews/qw0a_extractor_review_evidence/correction_verification_2026-10-14.json`. Prior independent review/evidence and the QW-1 integration evidence are carried forward blob-identically; the session handoff is updated. The reviewer changed documentation/evidence only.

## Release direction

Do not integrate `091dc95` or begin B. Fable applies the bounded R1 correction and returns a new frozen SHA. ChatGPT re-reviews, then prepares the concrete A integration for applicable acceptance/authorization with a fresh-main check. After accepted A integration, ChatGPT activates B from fresh main using the committed brief's existing gate-hardening matrix. B has its own review/integration before the adoption decision packet.

QW-1 remains closed. Planning remains separate. No new source-adoption policy, removal allowance, Forge version release or broader work package is activated.

**Live-game requests / writes / credentials: 0 / 0 / none.** No gameplay, reward, publication, global session projection or main update.
