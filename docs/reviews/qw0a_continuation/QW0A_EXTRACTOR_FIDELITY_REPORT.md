# QW-0A continuation, slice A — extractor fidelity report

**Slice status: `EXTRACTOR_REVIEW_READY`. Overall QW-0A status: `BLOCKED_BY_SOURCE_ADOPTION`.** This slice repairs how `schema_extract.py` reads the game source. It adopts no contract: the canonical 45x files, root mirrors, `validate.py`, `factory.py`, Forge, historical exceptions, workstreams and global state are unchanged.

| Item | Reference |
| --- | --- |
| Brief | `state/prompt_quest_workflow_qw0a_continuation_2026-10-14.md` at `chatgpt/qw0a-continuation-brief-20261014@2d2390e769587bc307b83971923ba4700a63e80d` |
| Branch / base | `fable/qw0a-extractor-fidelity-20261014` from `main@1da18301e8e4660cedf3daa3e80893a2ac918f2b` |
| Stamped source pin | `studie-tech/TheNinjaRPG@bdec2883748f029a0ecb93505adfdcbae6851fe9` |
| Release comparison pin | `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` |
| Machine-readable inventory | `docs/reviews/qw0a_continuation/QW0A_EXTRACTOR_INVENTORY.json` (untruncated) |
| Inventory producer | `docs/reviews/qw0a_continuation/tools/build_inventory.py` |
| Tests | `skills/building-tnr-content/scripts/test_schema_extract.py`, fixtures `skills/building-tnr-content/data/fixtures/qw0a/` |

Both pins were fetched from the public GitHub repository with `git fetch --depth 1 origin <sha>` and exported with `git archive`. No source was executed. No upstream HEAD was substituted for either pin. Neither pin is established as the deployed production build.

## 1. What changed in the extractor

All changes are in `skills/building-tnr-content/scripts/schema_extract.py`. The extraction is static and stdlib-only, and adds no dependency. A new `SourceIndex` reads each validator module once and records:

- its `import { … } from "@/…"` bindings, resolved through the tsconfig aliases (identical at both pins);
- its top-level `const` declarations, each with its exact extent: the first top-level `;` or the next declaration, respecting strings, comments and balanced delimiters.

On top of that index, the extractor now handles these constructs:

1. **Array spreads.** `[...A, "x"]` resolves transitively and in source order, both in constants and in validator-local lists. It also resolves inside `z.enum([...])`, including non-leading spreads such as `["None", ...MasteryNames]`. Examples: `ElementNames`, `allState`, `damageModifierTypes`, `UserStatNames`, `MaxPoolTypes`, `AvailableActionTargets`, `allObjectiveTasks`.
2. **Multi-line fields and schema heads.** 45c union-member objects are now read through the balanced parser, not the old line scanner, so a field split across lines is no longer dropped or truncated. Examples: `IncludeStats.statTypes`, `ConsumeTag.rounds`, `DiffuseTag.delayRounds`. 45d also finds `export const AiRule = z\n  .object({`.
3. **Helpers.**
   - Arrow helpers resolve from their defining module, including imported ones such as `makeCappedNullableNumber` from `validators/base.ts`.
   - Block-bodied helpers resolve too: `msg()` and `type()` (`=> { return z…; }`).
   - The helper body is its exact extent, not a 600-character window. That window is what pulled `enum_ref: "WeaponTypes"` and the next schema's text into the stamped 45d.
   - Parameter substitution replaces identifiers only. Previously `max` also replaced `.max(` and produced `.MAX_GENS_CAP(MAX_GENS_CAP)`.
4. **Object spreads.** `{...A, ...B.shape, f: …}` resolves across modules, for example `...rewardFields`, `...itemEconomySchema.shape` and `...masteryRequirementFields`. JavaScript precedence applies: a later spread or field overrides an earlier one. Output field order is unchanged: own fields first, then inherited ones.
5. **Union discriminant.** The discriminant prefers the `type` literal, so an inherited `direction: type("offence")` literal cannot be taken for it.
6. **Fact fidelity.**
   - Modifiers, defaults, coercion and bounds, literal or constant-named, come from the field's outer method chain only, in both the 45c and 45d paths. A nested item schema's `.optional()`, `.max()`, `.max(CONST)`, `.prefault()` or `z.coerce` no longer leaks onto the outer field.
   - An explicit `0`, `false` or `null` default, or a `0` bound, is emitted rather than dropped.
   - Numeric literals with separators or decimals are read correctly.
   - A constant-name bound or default resolves to its number and keeps `<key>_ref`.
   - A `z.preprocess(fn, inner)` field reports the inner schema's type. Its omission behaviour is classified from the callback by a bounded recognizer (§4). Anything outside the recognized forms is a gap, never `optional: true`.
7. **Fail-closed diagnostics.**
   - An unresolved or cyclic array or object spread in these constructs is an `error`. The run exits 1, prints the named diagnostic to stderr and writes nothing to stdout, so a `>` redirect cannot capture a partial contract.
   - A source form outside these constructs that loses a field is a `gap`, listed by the new `--gaps` mode.
8. **Read-set.** Every source file the process opens goes through one reader. The new `--reads` mode prints the repository-relative read-set of the contract modes, including the retained legacy readers (`parse_ref_schemas`, `parse_unions`).

The extractor does not claim arbitrary Zod/TypeScript coverage. The `--shapes` mode (45b, which is not a repository contract) still uses the v1 line scanner. `--procedures` (45f) is structurally identical before and after at both pins.

## 2. Correction inventory

The inventory compares contract facts at field-key granularity. A whole field counts as one row when it is added or removed. It covers 45c, 45d, 45e and 45g. Each row carries an `id`, its path, before and after values, one or more classes, and an `anchor` of one of these kinds:

| Anchor kind | Content | Used for |
| --- | --- | --- |
| `source` | SHA, file, declaration, line | Ordinary rows |
| `nested_occurrence` | SHA, file, declaration, and the real line of the nested field | A field the old extractor mis-attributed to its container (`DialogObjective.text`) |
| `derived` | Producer, derivation rule, linked `inputs` (ids of the rows in the same comparison whose source-cited facts produced it) | Every 45g row |
| `aggregate` | Producer and linked `inputs` | The 45e constant count |

The producer fails (nonzero exit) unless:
- every row has a complete anchor, or linked inputs;
- every file any run read is hashed;
- the corrected extractor's `--reads` equals the read-set traced from its runs.

`unclassified: 0` is no longer the only completeness check. Classes:

| Class | Meaning |
| --- | --- |
| X1_ARRAY_SPREAD | array spread resolved (constant or `z.enum`) |
| X2_MULTILINE | multi-line field expression or schema head now parsed |
| X3_HELPER | helper inlined (block-bodied, cross-file, exact extent) |
| X4_MODULE_SPREAD | object spread resolved from another module |
| X5_SPREAD_PRECEDENCE | later spread or field wins (JS order) |
| X6_FALSY_METADATA | explicit 0 / false / null no longer dropped |
| X7_OUTER_CHAIN | nested schema facts no longer attributed to the outer field |
| X8_NUMERIC | separator/decimal literal or constant-name bound/default resolved |
| X9_OMISSION | preprocess unwrapped: inner type, omission mechanism, nullability |
| X10_ENUM_REF_LABEL | enum_ref spelling follows the declaring module |
| D_DERIVED_45G | 45g recomputed from corrected facts |
| U_UPSTREAM | real change between the pins |

A row may carry several classes, so class counts can exceed row counts. Every row in comparisons A and B is classified (`unclassified: 0`).

### A — baseline vs corrected extractor at `bdec2883`: 1,923 rows

| File | Classes (row counts) |
| --- | --- |
| 45c | X4 918 · X5 347 · X6 316 · X3 149 · X2 47 · X1 22 · X7 4 · X10 2 · X8 1 |
| 45d | X9 124 · X3 96 · X8 51 · X7 6 · X2 5 |
| 45e | X1 4 (`ElementNames`, `allState`, `damageModifierTypes`, `allObjectiveTasks`) |
| 45g | D 88 |

### B — baseline vs corrected extractor at `585534d7`: 2,417 rows

| File | Classes (row counts) |
| --- | --- |
| 45c | X4 1260 · X5 372 · X6 333 · X3 163 · X2 69 · X1 42 · X7 4 · X10 2 · X8 3 |
| 45d | X9 184 · X3 129 · X8 43 · X6 20 · X2 13 · X4 10 · X7 6 |
| 45e | X1 8 (adds `UserStatNames`, `MaxPoolTypes`, `AvailableActionTargets`, `TimedMasteryNames`) |
| 45g | D 84 |

### Notable corrections, with source anchors

Source-verified in each case. The anchor's line is the field or declaration in the cited pin.

- **Basic elements were missing everywhere.**
  - Before: the stamped 45c and 45e `ElementNames` contain the literal `"...BasicElementName"` instead of `Fire`, `Water`, `Wind`, `Earth` and `Lightning`. That is why `validate.py` rejects `elements: ["Fire"]`.
  - Corrected: the real members are emitted.
  - Anchors: `app/drizzle/constants.ts` `ElementNames`, at both pins.
- **`power` has no maximum on 61 tags (bdec) / 67 tags (585534d).**
  - Each tag spreads `...BaseAttributes` (`power` min −100, max 100) and then `...PowerAttributes` (`power` min 0, no max). The later spread wins.
  - The old flattening kept the first spread, which is the source of the derived 45g `tag_power_max` cap. This is the class RUL-2026-10-12-013 waived as `idg_power_cap`, and `forge/src/runner/validate.mjs` already documents it.
  - Anchors: `combat.ts` `BaseAttributes` / `PowerAttributes`.
- **Objective rewards.**
  - `...rewardFields` is declared in `validators/rewards.ts`. It now reaches all objective variants (34 at bdec), plus the `noncombatconsumereward` tag.
  - Those are exactly the `reward_*` keys in push/90's `stale_effect_fields` class.
- **Tag `description` and `direction`.** These come from `msg()` and `type()` in `BaseAttributes` and are now present. They make up the rest of `stale_effect_fields`.
- **`statTypes`.** At 585534d the 15 `IncludeStats` tags regain the multi-line field. Its members are `StatTypes` (now including `None`) plus the still-accepted input `"Highest"`.
- **Dialog objectives.** `nextObjectiveId` is an array defaulting to `[]`. The bogus `text` field (from the nested option schema) is gone. Anchor: `objectives.ts` `DialogObjective`.
- **Mastery and stat requirements (45d).**
  - Fields: `required{Strength,Speed,Intelligence,Willpower}` at both pins; `required*Offence/Defence` at bdec; `required*Mastery` at 585534d.
  - Now type `number`, `min 0`, `max` = `MAX_GENS_CAP` / `MAX_MASTERY_CAP` (with `max_ref`), and `nullable`.
  - Now `optional: true`, with `_omission: "preprocess maps undefined to null and the inner schema is nullable"`.
  - The spurious `enum_ref` is gone.
- **`craftingRequirements` (45d `item`, both pins).**
  - Source: the array's element is `z.object({ids, number: z.coerce.number().int().min(1).max(MAX_ITEM_CRAFTING_REQUIREMENT_QUANTITY)})` (`585534d7:combat.ts:1755-1769`; `bdec2883:combat.ts:1493`).
  - The stamped and baseline field carried that inner number's `coerce`, `int`, `min 1`, `max 9999` and `max_ref`.
  - Corrected: the field is an array with `default []`, `optional` and `nullable` only (X7).
- **`AiRule` at 585534d.** The entity is now present, with its new `id` and `group` fields. The baseline dropped the whole entity because of the multi-line head.

## 3. Real upstream changes (C — corrected `bdec2883` vs corrected `585534d7`): 1,903 rows

These rows are the contract delta that a future adoption decision has to weigh. They are not adopted here.

| Area | Change |
| --- | --- |
| 45c, 11 variants added | `AllTags`: `decreaseaggro`, `decreasemastery`, `decreasepotency`, `diffuse`, `increaseaggro`, `increasemastery`, `increasepotency`. AI conditions: `player_within_range`, `summon_within_range`. Objectives: `bloodline_collection` in both objective unions. |
| 45c, fields removed | `statTypes` and `generalTypes` on `{in,de}crease damage {given,taken}` (the 4 tags keep `elements`); `elementalseal.elements` |
| 45c, enums | `target` adds `COORDINATES` on tags; AI action `target` adds `COORDINATE` and its enum_ref becomes `AvailableActionTargets`; `poolsAffected` uses `MaxPoolTypes`; new objective/potency members |
| 45d `item` / `jutsu` | 8 `required*Offence/Defence` removed and 6 `required*Mastery` added on each (migration 0056). `item` adds the farm fields, `requiredSkillId` and the `itemEconomySchema` fields. `jutsu` adds `bloodlineReskinId`, `elementClassification`, `reskinParentJutsuId`, `requiredSkillId`. |
| 45d `quest` / `aiRule` | `quest` adds 6 mastery requirements and `requiredFarmingLevel`; `aiRule` adds `id` and `group` |
| 45e | 168 constants added, 9 removed, 30 values changed. 892 `order` index shifts are metadata only, caused by inserted declarations. |

The comparison classes are labelled `U_UPSTREAM`. Telling breaking from additive rows is the job of the gate in slice B.

## 4. Omission, nullability and defaults

`optional` means the key may be omitted. `nullable` means an explicit `null` is accepted. A `default` means omission falls back to that value. Nullable is not omissible.

Omission is inferred only from one bounded callback form: `(v) => (A1 || A2 … ? null : v)`.
- Every atom must be an exact equality of the parameter with `undefined`, `null` or `""` (`===` or loose `==`, either operand order).
- The condition may not contain negation, `&&`, parentheses or any other operand.
- `v == null` and `v == undefined` are true for `undefined`; strict `v === null` and `v === ""` are not.
- The inner schema's acceptance is read from its outer chain only.

| Callback / inner schema | Where | Result |
| --- | --- | --- |
| maps `undefined` to `null`; inner outer-chain `.nullable()`/`.nullish()` | `makeCappedNullableNumber` (`base.ts:10-14` at 585534d; `combat.ts:1276` at bdec); `nullableInteger` (`itemEconomy.ts:4-8`, loose `== null`) | `optional: true`, `nullable: true`, `_omission` names the mechanism |
| rewrites only `""`, passes `undefined` through; inner `.nullish()` | `requiredSageRank` (`objectives.ts`) | `optional: true` |
| maps `undefined` to `null`, but only a nested element is nullable | review probe `nestedNullableInput` | `optional: false`, stays in `required_on_create` |
| passes `undefined` through; inner not optional | fixture `strictCapped` (strict `=== null` only) | `optional: false` |
| `!==`, `&&`, or any form outside the above | review probes `negatedInput`, `constrainedInput` | `optional` as declared (`false`), stays in `required_on_create`, `G_PREPROCESS_UNCLASSIFIED` gap |

At both pins, every preprocess field matches a recognized positive form, so the pinned payloads are unchanged by this tightening.

45d's `_contract.reading` note no longer says that `optional` plus `nullable` means `.nullish()`. It now says:
- both flags mean omission and null are both accepted;
- the mechanism is `.nullish()` or a classified preprocess named in `_omission`;
- facts describe the field's outer schema.

Tier: the callback and inner-schema text are **source-verified**. That Zod passes an absent key's `undefined` through the preprocess callback is **inferred** from Zod semantics, because the source was not executed.

## 5. Gate evidence (unchanged `schema_diff.py`)

Each candidate was compared against the stamped `skills/building-tnr-content/data/45{c,d,e}`. A nonzero adoption diff here is expected evidence, not a test failure.

| Pin | Extractor | invariants | 45c | 45d | 45e |
| --- | --- | --- | --- | --- | --- |
| bdec2883 | baseline | 0 (128) | 0 | 0 | 0 |
| bdec2883 | corrected | 0 (128) | **1** (20 breaking) | **1** (25) | **1** (5) |
| 585534d7 | baseline | 0 (139) | 1 (219) | 1 (42) | 1 (45) |
| 585534d7 | corrected | 0 (139) | 1 (76) | 1 (38) | 1 (46) |

The corrected extractor's breaks at `bdec2883` all remove facts the stamped files never should have contained:

| File | Breaking changes |
| --- | --- |
| 45c | 20 removals of the fake `...BasicElementName` member |
| 45d | 25 type changes, from `preprocess` to the inner type |
| 45e | 5 unexpanded spread literals: `...BasicElementName`, `...publicState`, `...privateState`, `...damageReductionTypes`, `...damageBoostTypes` |

Any adoption therefore needs a reviewed removal path even at the stamped pin. The adoption decision packet takes that up. The gate still has the review's R2 blind spots (non-enum union fields, union field types, nullability) until slice B, so the full-payload inventory above, not the atom gate, is the complete record. Full gate output is in the inventory's `gates[].output`.

## 6. Reproduction and hashes

```
git -C <scratch>/tnr fetch --depth 1 origin <pin>; git -C <scratch>/tnr archive <pin> | tar -x -C <src@pin>
python3 skills/building-tnr-content/scripts/schema_extract.py <src@pin> --ctors      # constructors first
python3 skills/building-tnr-content/scripts/schema_extract.py <src@pin> --entities
python3 skills/building-tnr-content/scripts/schema_extract.py <src@pin> --constants
python3 skills/building-tnr-content/scripts/schema_extract.py <src@pin> --checks
python3 skills/building-tnr-content/scripts/schema_extract.py <src@pin> --gaps
git show 1da18301e8e4660cedf3daa3e80893a2ac918f2b:skills/building-tnr-content/scripts/schema_extract.py > <scratch>/baseline.py
python3 docs/reviews/qw0a_continuation/tools/build_inventory.py \
  --old-src <src@bdec2883> --old-sha bdec2883748f029a0ecb93505adfdcbae6851fe9 \
  --new-src <src@585534d7> --new-sha 585534d7eb21d6f0dd678d5c3eb92662f611d39b \
  --baseline <scratch>/baseline.py --corrected skills/building-tnr-content/scripts/schema_extract.py \
  --stamped skills/building-tnr-content/data --scratch <scratch>/candidates --out <inventory.json>
```

All 16 extraction runs exited 0. Repeating every corrected run with identical inputs gave byte-identical output (`repeat_runs`, all `identical: true`).

- The full-file hash includes `_provenance`, which carries the run date, the source-path label and 16-hex source hashes, so it varies by run date.
- The structural hash drops only `_provenance` and sorts keys; list order is preserved.
- `source_file_sha256` holds the sha256 of every file any extraction run opened under the source tree. The read-set is captured by running each extractor under a Python `open` audit hook (`runs[].source_reads`), so the baseline extractor and the legacy readers are covered too.
- At `bdec2883` the read-set is 13 files and includes `libs/train.ts` and `validators/base.ts`. At `585534d7` it is 15 files and adds `itemEconomy.ts` and `mastery.ts`.
- `source_read_coverage` asserts that every read file is hashed and that the corrected extractor's `--reads` equals its traced read-set.

Structural sha256 prefixes (full values are in the inventory):

| Output | bdec baseline | bdec corrected | 585534d baseline | 585534d corrected |
| --- | --- | --- | --- | --- |
| 45c | `69926b4bc29568b5` | `831211ba1f5862f4` | `bd84d9d28e5a3715` | `8e9b23884b35edfb` |
| 45d | `559db15dfb52355b` | `262586aa87dd38b6` | `36bfd06a5ce52cbf` | `75f3e5e28ac8338e` |
| 45e | `011e7cdcb83d5c5f` | `33382fb866f2cfeb` | `bbe688d76daa9e9c` | `4be17246a66de0e7` |
| 45g | `464fa47e135c0e0e` | `217f29c340963017` | `69752eb811f1a9f0` | `ce33c5dafef2723f` |

The baseline output at `bdec2883` is structurally identical to the stamped 45c, 45d and 45g. Stamped 45e differs only by one hand-added key, `_contract.runtime_override_caveat` (the law 83 DMG_* note), which the extractor never emits. An adoption must preserve it deliberately.

## 7. Tests

`python3 skills/building-tnr-content/scripts/test_schema_extract.py` exits 0, with 43/43 passing. The tests cover:

- spreads: constant, transitive, two-spread, combat module, enum-by-ref, validator-local, non-leading inline;
- multi-line field, chain and schema head; nested-item leak; strings containing braces and commas;
- spread precedence: later spread wins, spread over an own field, cross-module spread;
- helpers: `type()`/`msg()`, discriminant, cross-file helper on multi-line and single-line heads, nullable-not-omissible, constant default;
- omission inference (correction pass): negated predicate, constrained conjunction and nested-only nullability stay required and in `required_on_create`; the strict-undefined, loose-null and pass-through pinned forms stay omissible;
- nested facts (correction pass): nested bound and coercion not attached to the container in both paths; real outer bounds and coercion kept; the `craftingRequirements` shape;
- falsy metadata: 0, false, null;
- refusals: unresolved and cyclic array and object spreads exit 1 with empty stdout; gaps are reported but not fatal;
- determinism.

The same tests against the `main@1da1830` extractor (`SCHEMA_EXTRACT=<baseline>`) exit 1 with 20 failures and 20 errors (`tests_baseline_main_1da1830.txt`). Each failure shows the intended defect: literal `...X` members, missing fields, `type: coerce`, leaked `text`, `min -100 / max 100` precedence, dropped `false`/`0`/`null`, `item` absent because of the multi-line head, the unresolved cross-file helper, and exit 0 on unresolved or cyclic spreads.

The three baseline passes are:
- the two guards (discriminant selection, determinism);
- `test_constructor_nested_bound_not_outer`. The old 45c path never resolved constant-named bounds, so that particular leak was introduced in `1bbc833`, not inherited.

Against the previously reviewed `1bbc833` extractor, the tests exit 1 with exactly the 6 new negative tests failing (`tests_previous_1bbc833.txt`): the three omission probes, the entity and constructor nested-bound probes, and `craftingRequirements`.

## 8. Residual gaps and consumer notes

1. **Gaps at 585534d (`--gaps`, non-fatal; none at bdec):**
   - `coordinateTargeting: coordinateTargetingSchema.nullish()` in `BaseAttributes` (all tags), `JutsuValidatorRawSchema` and `ItemValidatorRawSchema`.
   - `coordinates: aiCoordinatesSchema.optional()` in `actionTargetSettings` (9 AI actions).
   - `allyAIs: allyAIsField` in `InstantStartBattleObjective` / `DefeatOpponents`.

   These schema-reference fields are not inlined and stay absent from 45c/45d, as before. Consequence: a validator built on these contracts would still reject them as unknown fields.
2. **Inline refine.** `AiRule` carries an inline `.superRefine((rule, ctx) => …)` (`ai.ts:264`). 45d's `superRefine` lists named functions only, so the rule ("COORDINATE target requires coordinates"; minRange ≤ maxRange) is not represented.
3. **Existing 45c format kept:**
   - A field with an `enum_ref` carries a sorted, de-duplicated `enum`; source order lives in 45e.
   - An `enum_ref` is omitted when the list sits in a module 45e does not fold in (for example `rewards.ts`). The inline `enum` still carries its members.
4. **Consumer-visible facts (not adopted).** If adopted later:
   - 45d gains `_omission` and `default_ref` keys, and its `_contract.reading` note changes (§4).
   - Preprocess fields report their inner `type`.
   - 45g `required_on_create` drops omissible preprocess fields.
   - `tag_power_max` loses the tags whose effective `power` has no max.
   - Consumers ignore unknown underscore keys. A validator or Forge parity change is the later alignment slice's job.
5. **Fail-closed CLI.** The scheduled `regen_schemas.yml` sentinel redirects stdout. A future upstream drop containing an unresolved supported spread would now fail that job rather than record a corrupted candidate. The corrected extractor exits 0 for `--ctors/--entities/--constants` at `6e4429d6` and `f8c04d02` (checked as a risk note only; these are not inventory pins).
6. **Not addressed here (slice B and later):**
   - `schema_diff.py` blind spots (R2).
   - Python vs Forge source-pin divergence.
   - Law-owned validator rules (law 14 `preferredStat`, `companion_required`).
   - The D-adopt-gate removal-adoption decision.

## 9. Correction pass (review `3f64e065`, CHANGES_REQUESTED on `1bbc833`)

### QW0A-A-R1 — FIXED

**Change.** `preprocess_omission` is now a bounded recognizer (§4). Unsupported predicates produce a `G_PREPROCESS_UNCLASSIFIED` gap and leave `optional` as declared. The inner schema's nullability and optionality are read from its outer chain. An omission that is proven rejected is classified as such and is not reported as a gap. The 45d reading note is corrected.

**Evidence.**
- The review's three probes are in `ItemValidatorRawSchema` of the positive fixture, together with the positive controls: strict-undefined, loose-null (`nullableInteger` form) and pass-through (`requiredSageRank` form).
- Tests: `OmissionInference`, 7 cases, including `required_on_create` preservation.
- Pinned payloads are unchanged by this fix, because every pinned callback is a recognized positive form.

### QW0A-A-R2 — FIXED

**Change.**
- `coerce` comes from the outer expression (`z.coerce.…` at its start).
- Constant-named bounds come from outer-chain calls only, in both `parse_expr2` (45d) and `SourceIndex.resolve_numbers` (45c and 45d).
- Constant-named defaults come from an outer `prefault`/`default` call only.

**Evidence.**
- Tests: `NestedFacts`, 6 cases. Entity and constructor nested-bound negatives; outer bound and outer coercion positives; the `craftingRequirements` shape mirrored from the release pin.
- Inventory: `craftingRequirements` loses `coerce`, `int`, `min`, `max` and `max_ref` at both pins (A and B, +3 rows each).
- Regenerated structural hashes: only 45d changed (§6). 45c, 45e and 45g are structurally identical to the `1bbc833` run.

### QW0A-A-R3 — FIXED

**Change.**
- The extractor reads every source file through `_read()` and exposes the read-set with `--reads`.
- The inventory traces each run's actual opens with an audit hook and hashes all of them. `train.ts` and `bdec2883:base.ts` are now included.
- Every row carries an `id`. Each 45g row is `derived`, with its producer, derivation rule and linked input row ids. The 45e count is `aggregate`, with linked inputs. The dialog `text` removals are `nested_occurrence` anchors with their real line.
- The producer asserts provenance coverage and exits nonzero on any gap (`provenance problems: 0` for this run).

**Evidence.** Inventory keys `source_read_coverage` and `comparisons.*.rows[].anchor`. Producer output: `unclassified: 0`, `provenance problems: 0`, exit 0.

**Live requests / writes / credentials: 0 / 0 / none.**
