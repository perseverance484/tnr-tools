# 12b_LAWS_coverage.md - Enforcement matrix for the engine laws

Generated as part of the Phase 2 reconciliation (2026-08-26, source drop `TheNinjaRPG-main__3_.zip`).
One row per law in `12_TECH_engine_laws.md`. This file answers a single question: **if I forget this
law, what catches me?**

## Classes

| Class | Meaning |
|---|---|
| `validate` | `70_TOOL_validate.py` errors or warns before the manifest ever reaches the browser. Forgetting it is cheap. |
| `builder` | The push path enforces or repairs it (fetch-merge, ref substitution, null handling, id map). |
| `generated` | The law's content is now a generated file. The prose is kept for the reasoning, not the value. |
| `knowledge` | True, verified, and not mechanisable. Must be read by a human or by Claude before building. This is the expensive class. |
| `superseded` | Wrong, or overtaken by a later law. Retained so the wrong version is not independently re-derived. |

## Status column

`verified` = re-read against this source drop in the Phase 2 pass. `carried` = unchanged since it was
paid for in the field, not re-derived this pass. `corrected` = the law changed in this pass.

## Matrix
> **[CORRECTION 2026-08-28] This matrix was written against `70_TOOL_validate.py`. The skill ships
> a different, later `validate.py`, and the two do not have the same checks.** A `validate` class
> here does not guarantee the tool you are running enforces it. Nine laws were audited as claimed
> but absent; six were real gaps and are now closed, three were an artefact of grepping for law
> numbers in tools that enforce by reading a spec instead. Law 14 reached a push because of this.
> **Verify against the code, not this file.** `01_PRECEDENCE.md` gives the code precedence.


| # | Class | Status | Where it is enforced / cited |
|---|---|---|---|
| 1 | knowledge | carried | Compose to update-strict standards; no mechanical check exists |
| 2 | validate | verified | `check_member` per-tag strict union against `45c` |
| 3 | knowledge | carried | Qualifier H12 (jutsu lean, item full) is not schema-visible |
| 4 | validate | carried | `check_laws` FORMULA_TAGS statTypes+generalTypes |
| 5 | validate | carried | `targetId` required on every convert/edit entry |
| 6 | validate | **corrected** | power/apReduction/threshold caps in `45c`; condition `value` has NO max |
| 7 | validate | verified | `DATE_RE` on startsAt/endsAt |
| 8 | validate | verified | `CAP_100`; bounds confirmed in `45d` quest (0-100) |
| 9 | knowledge | carried | Multiplicative stacking; doctrine, not a validator rule |
| 10 | knowledge | carried | DDT product form |
| 11 | knowledge | carried | Pierce bypass; calibration discipline |
| 12 | knowledge | carried | Ramp compounding |
| 13 | knowledge | carried | Calibration protocol |
| 14 | validate | **corrected 2026-08-28** | `check_ai_create`. Was claimed, absent, caught by builder lint L05 |
| 15 | knowledge | **corrected** | `scaleUserStats` re-read line by line; statMod precision added |
| 16 | generated | **corrected** | `USER_CAPS` now in `45e`, including the previously unrecorded `LVL_CAP` |
| 16b | validate | verified | `hidden:true` on every create; L13 |
| 16c | knowledge | carried | gameAsset hidden = listing only |
| 16d | validate | verified | AI rule shape checked against `45c` `AiRule` |
| 17 | builder | carried | Ref substitution; unresolved `@` stripped server-side |
| 18 | knowledge | carried | Unequip -> edit -> re-equip. No offline check possible |
| 19 | knowledge | carried | Item union narrower than jutsu union |
| 20 | validate | **corrected** | Guard fires only on `injectableInBattle: false`; validate now warns when the field is absent from an edit |
| 21 | generated | verified | `battleUsageType` enum in `45d` |
| 22 | generated | verified | `craftingRequirements` write shape |
| 23 | validate | verified | `consecutiveObjectives` required on create; `45d` confirms no schema default |
| 24 | knowledge | carried | `checkRewards` is a tracker tick |
| 25 | knowledge | carried | Top-level sceneBackground renders in the travel popup |
| 26 | knowledge | carried | Reset nodes and failObjectiveId |
| 27 | knowledge | carried | CYOA doctrine; design law |
| 28 | builder | carried | Per-entry `json.success` |
| 29 | builder | carried | Ids extracted from bundles by script |
| 30 | knowledge | carried | Name-collision fills; catalogs advisory |
| 31 | knowledge | carried | Law 31, generation from guide templates |
| 32 | knowledge | carried | Fresh filenames on re-upload |
| 33 | knowledge | carried | Component-based chroma keying |
| 34 | knowledge | carried | Generators paint key colour into subjects |
| 35 | validate | carried | 512KB cap; byte ledger keyed to `@img` |
| 36 | validate | **corrected 2026-08-28** | `check_entry_laws`. Was claimed and absent |
| 37 | validate | carried | `consecutiveObjectives` at data level, never in `content` |
| 38 | generated | verified | `prerequisiteQuestId` is `string`, `.nullish()`, single-valued: `45d` |
| 39 | validate | verified | Rule vocabulary fixed by `45c` `ZodAllAiConditions` / `ZodAllAiActions` |
| 40 | validate | **corrected 2026-08-28** | `check_distance_gates`, from 32b ranges |
| 41 | validate | carried | Final rule unconditional |
| 41b | knowledge | carried | Unreachability applies only below always-executable actions |
| 42 | validate | verified | `NONE` is a real member of `HUNTING_RANKS`/`GATHERING_RANKS` in `45e`; validate now warns |
| 43 | knowledge | carried | Profession experience reward fields |
| 44 | validate | carried | `number` is a COUNT on opponentAIs, a PERCENTAGE on attackers |
| 45 | validate | carried | Doubled `@ai:@ai:` prefix lint |
| 46 | validate | verified | `image: ""` nulled at write path |
| 47 | knowledge | carried | reset_quest / win_quest descriptions never display |
| 48 | validate | verified | One scene character per node |
| 49 | knowledge | carried | `sceneCharacters` resolves gameAsset ids only |
| 50 | validate | **corrected** | Three fields, three mechanisms; only avatars/icons/backgrounds stretch. `artpreflight.py` |
| 51 | knowledge | carried | Scene character canvas share |
| 52 | knowledge | carried | Node-level `image` is the sector pin |
| 53 | knowledge | carried | Logbook badge is static |
| 54 | validate | **corrected 2026-08-28** | `check_quest` law-54 block, scoped by task |
| 55 | validate | **corrected 2026-08-28** | `check_entry_laws`. Was claimed and absent |
| 56 | generated | verified | `collect_time_minutes` float, max 60: `45c` |
| 57 | knowledge | carried | Quest `updatedAt` not maintained |
| 58 | knowledge | carried | In-game editor overwrites |
| 59 | knowledge | carried | Blank-shell jutsu |
| 60 | knowledge | carried | Law 18 has an order |
| 61 | knowledge | **corrected** | `progressRound` / `refillActionPoints` re-read; confirmed against this drop |
| 62 | knowledge | carried | Stealth blocks attacking |
| 63 | knowledge | carried | Fall-through exhaustion |
| 64 | validate | **audited 2026-08-28, holds** | `check_member` vs `ZodAllAiConditions`/`ZodAllAiActions` |
| 65 | knowledge | carried | AI rules can use items |
| 66 | knowledge | carried | Usernames unique across all UserData |
| 67 | generated | **corrected** | Full six-rank `HUNTING_ITEM_DROP_CHANCES` table in `45e` |
| 68 | knowledge | carried | `reward_items` with `number: 100` |
| 69 | validate | carried | AI item `number` = dropChancePerc |
| 70 | knowledge | carried | `updateAi` syncs items by set difference |
| 71 | knowledge | carried | `updateAi` runs `scaleUserStats` on every write |
| 72 | validate | **corrected** | optional vs nullable split; `check_nulls` reads `45d` |
| 73 | validate | **corrected 2026-08-28** | `check_entry_laws`, boolean list derived from 45c and 45d |
| 74 | builder | carried | Read records are not write shapes |
| 75 | knowledge | **corrected** | `castThisRound` mechanism; now carries its source citation |
| 76 | knowledge | verified | Turn vs round; governs every `rounds` field |
| 77 | validate | **new** | Runtime-only tag class; `RUNTIME_ONLY_TAGS` |
| 78 | validate | **new** | Companion requirements: consume/vamp/wound need damage or pierce; rollsagemode item-only |
| 79 | knowledge | **new** | Delivered width is the component's `width` prop; source above it is discarded |
| 80 | knowledge | **new** | The asset editor preview is `aspect-square` and lies about non-square types |
| 81 | validate | **new** | Scene characters clip above h/w 5/3; `artpreflight.py` check `clip_bound` |
| 82 | generated | **new** | 341x512 derived from 2:3 inside maxDim 512; `25x_DATA_art_spec.json` |
| 83 | knowledge | **new** | `45e`'s `DMG_*` are defaults; live values come from the `gameSetting` table |
| 84 | knowledge | **new** | Extensionless keys on the three.js path get NO Bunny rendition; source bytes ship whole |

## Counts

| Class | Laws |
|---|---|
| validate | 33 |
| knowledge | 38 |
| generated | 6 |
| builder | 5 |
| superseded | 0 |

The `knowledge` column is the honest measure of how much of this stack still has to be *read* rather
than *checked*. Driving it down is what Phase 3 is for: a law that must be read should live next to
the workflow that needs it, not in a file that is retrieved whole.

## Open from this pass

- **File 50 retirement - RULED AND EXECUTED 2026-08-26.** Mapped claim by claim in
  `92_MAP_file50_retirement.md`, not summarised. All 16 constants it named were already generated in
  `45e`; seven claims were already laws; the pipeline shape moved to `balance.md`; the afterburn
  60% ruling moved with it; passes 2-6 cut to the repo. One claim was recorded nowhere else and is
  now **law 83**. `46b` stays closed. Original note follows for the reasoning.
- **[superseded by the above]** `50_DATA_combat_facts.md` is 200 lines and almost entirely restated
  numbers. All 11 `DMG_*` constants, `MAX_STATS_CAP`, `MAX_GENS_CAP` and `USER_CAPS` are now
  generated in `45e`. What is NOT generated is the damage formula's *shape* (the order of
  operations from `atkStats` through `advantageMod` to the residual and weakness modifiers). That
  prose belongs in `46b`; the numbers should go. Not executed this pass - it needs a ruling on
  whether `46b` reopens, and it was closed deliberately.
- **Law 40's A\\* claim** is carried, not re-verified. `PathCalculator` is constructed in
  `actions.ts` but the distance-to-gate path was not walked end to end in this pass.
- **Art laws now have a checker.** Laws 50, 81 and the spec's aspect, byte, format and soft-edge
  rules are enforced by `producing-tnr-art/scripts/artpreflight.py`, which is to art what
  `validate.py` is to manifests. Laws 79, 80 and 82 stay `knowledge` because they explain why the
  numbers are what they are; the numbers themselves are in `25x_DATA_art_spec.json`.
- **Laws 9-13** (the stacking and calibration block) are the largest `knowledge` cluster and the
  one most worth turning into a simulator assertion rather than prose.


## Added 2026-08-28

| # | Class | Status | Where it is enforced |
|---|---|---|---|
| 85 | validate | new | `check_dialog_options` |
| 86 | validate | new | `check_dialog_options`, terminal warning |
| 87 | validate | new | `check_acyclic` |
| 88 | validate | new | `check_reset_targets` |
| 89 | knowledge | new | an omission is not mechanically detectable |

**Art-side laws 35, 50 and 81 audited and confirmed enforced.** `artpreflight.py` checks bytes
against `upload.hard_cap_bytes` plus a per-target working ceiling, clipping against
`max_aspect_h_over_w`, and the `@img` filename contract via `img_refs`. Selftest 38/38. It
enforces by reading `25x_DATA_art_spec.json` rather than citing law numbers, which follows the
stack's own "laws cite, never restate" rule but makes coverage unauditable by grep. Adding a
`# law NN` comment beside each check would make this matrix mechanically verifiable at no
behavioural cost.

## Phase 3 - code-based laws (opened 2026-08-30, mounted)

"Verify against the code, not this file" is now a command: `python3 scripts/lawmap.py <repo-root>`
cross-checks ENGINE_LAWS text, this matrix, and `law NN` citations across both skills' scripts and
`builder_bundle.js`. Baseline this pass: 93 laws, 93 rows, 70 citations, 0 errors. Parity now runs
against production evidence directly: `validate.py --parity <inbox results bundle>` reads the
bundle's own `checks` inventory (proven 2026-08-30 against the acceptance bundle, 16/16).

Audit deltas this pass:
- validate.py and artpreflight.py annotated at their enforcing sites (`# law NN`), closing 12 of 16
  grep-blind rows. Miscitation fixed: the distance-gate message cited law 39, is law 40.
- ENGINE_LAWS structural rot repaired: the 2026-08-28 quest-flow section landed INSIDE section 16
  as a duplicate `## 12`; renumbered `## 17` and re-seated. Heading only - law text untouched.
- Laws 18 and 61: cited by validate.py but classed knowledge. Reclass to validate(partial)
  PROPOSED (18's kit-side check exists in check_pool_kit; live equip state stays unknowable).
- Laws 16d, 37, 69: matrix claims validate; no enforcing site found by this audit. Annotate the
  real site or reclass. OPEN.
- stack.py audits the retired project-knowledge layout and mis-flags repo runtime files.
  Law-numbering audit now lives in lawmap.py. Retire or re-point: OPEN.
- 10_LAWS_core.md exists only in project knowledge; under repo canon it needs a repo home
  (⇪ File it to docs/ next project session). OPEN.

Conversion tranches, knowledge -> code, smallest risk first:
- **T1 validator warnings** (no builder change, parity untouched): law 3 item-full vs jutsu-lean
  cosmetics; law 49 sceneCharacters resolve against answers/names_asset; laws 30/66 offline
  name-collision warn against the answers name files.
- **T2 executable doctrine**: laws 9-13 as calc.py selftest assertions - each law a failing test
  the moment the tool stops embodying it.
- **T3 builder v4.28 + 45g + parity**: promote T1 warnings to errors on both sides; annotate the
  builder lints (L05, L22...) so lawmap can read that surface too.
- **Stays knowledge**: rendering/editor/runtime semantics (25, 47, 51-53, 57-60, 62-63, 65, 70-71,
  75-76, 79-80, 83-84, 89).

Rulings OPEN for dauntless: T1 scope; warnings-ship-validator-first y/n; 18/61 and 16d/37/69
reclasses; stack.py retirement; 10_LAWS_core relocation.

## Source audit 2026-08-30 (docs/SOURCE_AUDIT_2026-08-30.md)

45c/45e/45f regenerated @bdec2883 with the upgraded extractor; 45d/45g zero drift. Laws
44/69's headcount-vs-dropchance doc now rides the GENERATED 45c (POST_DOCS in
schema_extract.py). Law 40's A* range+1 claim remains carried, not walked, this pass.
Laws 85-88's flow validator unchanged in the window. Builder qtype enum lacks new
NPC-only `overworld` - folds into T3 config-driven enums.
