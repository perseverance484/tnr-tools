# QW-0A continuation, slice A — independent review

**Verdict: CHANGES_REQUESTED.** The extractor makes substantial, reproducible corrections, but two fact-extraction defects and an evidence-provenance gap must be corrected before integration. Slice B remains queued. Overall QW-0A remains `BLOCKED_BY_SOURCE_ADOPTION`.

| Item | Exact reference |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Frozen Fable target | `fable/qw0a-extractor-fidelity-20261014@1bbc833f093c0b747e9abef741b21067ae1ed3df` |
| Main at review start / implementation merge-base | `1da18301e8e4660cedf3daa3e80893a2ac918f2b` |
| Fresh main before review publication | `83690aa7394e3253e1a3860b81bba0a0641577fe` |
| Governing continuation brief | `chatgpt/qw0a-continuation-brief-20261014@2d2390e769587bc307b83971923ba4700a63e80d`, `state/prompt_quest_workflow_qw0a_continuation_2026-10-14.md` |
| Separate approved planning source | `c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Game-source pins | `bdec2883748f029a0ecb93505adfdcbae6851fe9` and `585534d7eb21d6f0dd678d5c3eb92662f611d39b` |
| Reviewer | ChatGPT — Release Auditor, Engineering Auditor lens |
| Review branch | `chatgpt/review-qw0a-extractor-20261014`, based on the frozen target |

Live refs matched the handoff. Review used an isolated ChatGPT worktree; Fable's branch was not changed. The target has the reported 27-path implementation/evidence/package delta. The approved planning branch is still separate. Repository authority, the committed brief, prior QW-0A report/review, actual code/tests, inventory producer, pinned source and packaging automation were inspected. The global September state was read as historical orientation, not rewritten.

Main advanced during review by one sentinel commit, `83690aa`, changing only `docs/DRIFT.md` and `state/schema_sentinel.json` (signal pin `56e45fab2c87fe9d50c9beba519b616955e5c329`). There is no overlap with the implementation/review paths or adoption-policy owner. Fable remains frozen at `1bbc833`; no rebase or merge was performed. The new signal does not change the two audit pins or authorize adoption. Recheck main again before any later integration.

## Blocking findings

### QW0A-A-R1 — Omission inference accepts predicates that do not establish omission

**Confirmed defect, medium.** `skills/building-tnr-content/scripts/schema_extract.py:1046-1069`, applied to emitted fields at lines 1212-1217.

The classifier searches for an equality substring anywhere in a callback condition, and for nullable/optional methods anywhere inside the inner expression. Those checks do not prove either the callback's result for `undefined` or the enclosing schema's acceptance of that result.

These three minimal fields were inserted into `ItemValidatorRawSchema` in a scratch copy of the committed positive fixture:

| Expression | Why omission is not established |
| --- | --- |
| `z.preprocess((v) => (v !== undefined ? null : v), z.number().nullable())` | For `undefined`, the predicate is false and the callback returns `undefined`, not null. The equality regex also matches inside `!==`. |
| `z.preprocess((v) => (v === undefined && false ? null : v), z.number().nullable())` | The conjunction is false; the callback again returns `undefined`. Finding an equality substring ignores the condition as a whole. |
| `z.preprocess((v) => (v === undefined ? null : v), z.array(z.number().nullable()))` | The callback returns null, but only the array's elements are nullable. The enclosing array is not. |

**Actual CLI result:** `--entities`, `--checks` and `--gaps` all exit 0. All three fields receive `optional: true` and `_omission: "preprocess maps undefined to null and the inner schema is nullable"`. All three disappear from `required_on_create.item`. No diagnostic names these probes. The third field simultaneously has `nullable: false`, contradicting its own omission explanation. A positive control with `v === undefined` and an outer nullable number is correctly accepted.

The callback counterexamples follow directly from the supplied expressions; no game or TypeScript source was executed. This is a defect in the new inference, not a claim that the two pinned `makeCappedNullableNumber` callbacks themselves are wrong. It matters before B because B must not treat an unsupported callback as evidence that a new input is safely omissible.

**Required correction:** recognize only bounded callback forms whose complete condition and branches establish the result for omitted input. Treat an unsupported predicate conservatively and report its gap; do not set `optional: true` from a substring. Determine the inner schema's nullability/optionality at its outer level. Add CLI regressions for all three cases, required-on-create preservation, and the valid pinned positive controls. Keep this a static, bounded recognizer, not a general TypeScript evaluator.

Also correct the generated 45d reading note that currently says both flags being true necessarily means `.nullish()`: the new preprocess mechanism disproves that description. Explain the changed metadata/consumer interpretation in the report.

### QW0A-A-R2 — Named bounds and coercion still leak from nested schemas

**Confirmed defect, medium.** `schema_extract.py:647-654` and `903-910` scan the entire expression for named bounds after the outer-chain parser; line 82 likewise sets `coerce` from any nested `.coerce.` substring.

The CLI emits an outer `max: 400000` for `z.array(z.number().max(MAX_CAP)).optional()` in **both** entity extraction and a constructor field, with the positive fixture's `MAX_CAP = 400_000`. That maximum constrains a number inside the array, not the array itself. An outer-array maximum must remain absent in this example.

There is also an actual pinned-source case: `585534d7:app/src/validators/combat.ts:1754-1769`, `ItemValidatorRawSchema.craftingRequirements`. The `.max(MAX_ITEM_CRAFTING_REQUIREMENT_QUANTITY)` applies to each object's `number` field. The enclosing array has a default, optionality and nullability, but no maximum or coercion. The current 45d candidate contains:

```json
{
  "type": "array",
  "coerce": true,
  "optional": true,
  "nullable": true,
  "default": [],
  "max_ref": "MAX_ITEM_CRAFTING_REQUIREMENT_QUANTITY",
  "max": 9999
}
```

The alias is declared at `585534d7:app/drizzle/constants.ts:22`. Resolving its number does not make it an outer-array constraint. This entity leakage includes pre-existing behavior; the added constructor resolver has the same problem. It remains within A's explicit outer-chain/bound-fidelity scope and contradicts the report's completed-fidelity claim. It is not a request to migrate the consumer or add nested-field support.

**Required correction:** obtain the applicable outer calls once and use them consistently for literal/named bounds and coercion in both paths. Do not attach inner facts to their container. Add positive controls that retain actual outer bounds/coercion, a constructor and entity nested-bound negative control, and the pinned crafting-requirements case. Regenerate both-pin inventories and hashes after the fix; explain the changed facts rather than preserving the old row counts.

### QW0A-A-R3 — Complete the inventory's source and derivation provenance

**Confirmed evidence gap, medium.** `docs/reviews/qw0a_continuation/tools/build_inventory.py:303-322,413-423`.

All 25 supplied source-file hashes match the exact Git objects. However, the manifest is assembled from the classifier's `Context` index, which is not the complete set of files the extractor reads. Inspection with full pinned `app/` archives identifies these missing hashes:

| Pin | File read but absent from `source_file_sha256` |
| --- | --- |
| `bdec2883` | `app/src/libs/train.ts` |
| `bdec2883` | `app/src/validators/base.ts` (read by the retained `parse_ref_schemas` path) |
| `585534d7` | `app/src/libs/train.ts` |

The `train.ts` dependency is resolved while indexing the filtering schemas; the old-pin base helper participates in reference-shape extraction. Both matter to the claim that every read source file was recorded, even where a dependency does not alter a particular emitted payload.

The inventory also has **88 A rows, 84 B rows and 18 C rows** for derived 45g corrections with no anchor file or source-dependency links. They receive `D_DERIVED_45G`/`U_UPSTREAM` labels, which do not establish which source facts justify the changed check. Two removed nested `text` rows retain a declaration anchor but no line; the constants-count aggregate has no source file. These latter aggregate/removal cases can be explicitly represented rather than pretending each is a direct field declaration. The handoff's “every row anchored to SHA + file + declaration + line” claim is therefore too strong.

**Required correction:** gather the actual extraction read-set, including retained legacy readers, and hash it. For each derived check change, record the generator/derivation owner plus the relevant source-cited input facts (links into other inventory rows are sufficient). Add a coverage assertion for required provenance and explicitly identify metadata/aggregate cases. `unclassified: 0` must not be the only completeness check. Rebuild the inventory/report; do not manufacture a source declaration for an aggregate.

## Reproduction notes

For R1, copy `skills/building-tnr-content/data/fixtures/qw0a/positive/` to scratch. Add the three table expressions as new item fields named `negatedInput`, `constrainedInput` and `nestedNullableInput`, plus this positive control:

```typescript
validInput: z.preprocess((v) => (v === undefined ? null : v), z.number().nullable()),
```

For R2, add `nestedBoundInput: z.array(z.number().max(MAX_CAP)).optional()` to that item schema and `boundProbe` with the same expression to `DamageTag`. Run the target extractor with constructors first, then `--entities`, `--checks` and `--gaps`. Inspect the named fields and `required_on_create.item`. This uses only fixture text; it does not execute the TypeScript.

For the pinned case, extract entities from the full release-pin source and inspect `entities.item.fields.craftingRequirements`. For R3, compare the full extraction index's loaded modules plus the legacy reference reader's files to `inventory.source_file_sha256`; inspect the derived rows' anchors.

Exact observed probe fields, exits, missing-file hashes and verification results are committed in `docs/reviews/qw0a_extractor_review_evidence/verification_2026-10-14.json`. Scratch probes/candidate contracts remain outside the repository. No implementation fix was made by the reviewer.

## Verified claims and checks

| Check | Independent result |
| --- | --- |
| Target tests | exit 0; 30/30 |
| Same tests against main's extractor | exit 1; 19 failures, 9 errors, 2 guards pass |
| Inventory producer | exit 0; A 1,920 / B 2,414 / C 1,903 rows; comparison objects reproduce exactly |
| All 16 baseline/corrected extraction runs | exit 0; all structural hashes match the committed inventory |
| Repeated corrected outputs | byte-identical for identical source/provenance inputs |
| Full pinned-source confirmation | all eight corrected structural outputs and both `--gaps` diagnostic lists match |
| Unchanged adoption gates | exits, counts and output line multisets match; every corrected 45c/45d/45e candidate still fails adoption as reported |
| Existing sector/additive/bad-invariant fixtures | expected exits 1 / 0 / 1 |
| Three historical exception gates | exit 0 each; exact 56E/25W, 4E/3W, 4E/3W ledgers hold |
| Factory selftest / validator laws | exit 0; 20/20 and 4 asserted/0 failed |
| Packs, lawmap, doctrinemap, doctrine render, catalog selftest | exit 0; lawmap retains 5 existing warnings |
| Skill pack producer, twice | exit 0 twice; both ZIPs reproduce the committed hashes and stay under 2 MiB |
| Building-skill ZIP | all 91 members byte-equal to their source; 399,228 bytes |
| Python compilation | passes; bytecode outside the checkout |
| Protected paths against base | no changes to adopted contracts/root mirrors, validator/factory/gate, Forge, manifests/exceptions, state/workstreams/global projections, doctrine/rulings/laws or workflows |

The field-addition/removal inventory supports the stated absence of an unexplained field disappearance at these pins: A/B remove only the wrongly extracted nested `DialogObjective.text`. The disclosed schema-reference/inline-refine gaps remain limitations of adoption/future coverage; this review does not require turning A into a general Zod parser. The 45c sorted reference-enum representation is preserved compatibility behavior; 45e retains source order. The law-83 stamped caveat remains a later explicit preservation obligation.

Review setup qualifications: initial minimal exports omitted `libs/train.ts`, creating extra nonfatal filter-schema gaps. Rechecking with full pinned `app/` archives resolved the discrepancy without changing any audited structural hash. An initial ZIP comparator used the wrong member root; correcting it to the skill root verified all members. The producer builds themselves matched throughout. The unchanged gate's CHANGES ordering depends on set iteration, so its textual order is not asserted byte-identical. These are not additional implementation findings.

The reported Actions run IDs were not independently queried; remote-head identity and local deterministic package reproduction were checked directly. Browser/deployed-runtime behavior remains unverified. No full Forge/art/workstream suite was repeated because those implementations were unchanged.

## Correction and release instruction

Fable should address **QW0A-A-R1, R2 and R3 on its existing owned implementation branch**, retain the brief's boundaries, rebuild the relevant evidence/package and return a new frozen remote SHA. Keep original target `1bbc833` as the review reference. Account for packaging automation before announcing the freeze.

Do not integrate `1bbc833`, begin B, adopt contracts or reopen QW-1. The correction review will inspect the affected extractor paths, meaningful negative/positive controls, both-pin regenerated payloads and provenance, historical gates and package fidelity; it is not merely a document-label recheck.

After A passes independent review and accepted integration, ChatGPT issues B from fresh main. B then gets its own review/integration; only afterward does the source-adoption decision packet and separately scoped Python/Forge alignment work proceed. No policy removal allowance or broader package activation follows from this review.

**Live-game requests / writes / credentials: 0 / 0 / none.** No gameplay, reward or publication change; no global session open/close, main update or active Fable-branch write.
