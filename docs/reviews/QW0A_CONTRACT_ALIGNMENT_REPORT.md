# QW-0A — source-contract and validator alignment: mismatch report

**Verdict: `BLOCKED_BY_SOURCE_ADOPTION`.** No generated contract, validator, factory or Forge file was changed. The canonical validator is **not** fixed by this pass, and the three SHA-scoped Ghost Ship exception gates stay in force unchanged.

**Brief:** `state/prompt_quest_workflow_qw0_contract_alignment.md` (approved by RUL-2026-10-12-016 on `chatgpt/quest-workflow-skyglass-retrospective-20261012@c34f7de572337b0d2cfe397b9331502aa6548e27`).
**Branch:** `fable/qw0a-contract-alignment-20261012`, base `main@4de2668bb947368113683b5cb97e197abc87df27`.
**Live game:** 0 requests, 0 writes. No credentials and no CDN contact. GitHub was read only to fetch the public upstream source.

## 1. Outcome in one paragraph

The mechanical adoption gate fails closed for every candidate pin. Against the stamped files (all extracted at `bdec2883`), it exits 1 on 45c, 45d and 45e at the release pin `585534d7`, the sentinel `6e4429d6` and the current upstream HEAD `f8c04d02`. The failures have two causes:

- **Genuine source removals.** Migration 0056 removed the offence/defence stat columns. Some tags also lost fields.
- **Extractor blind spots.** `schema_extract.py` cannot read the newer source idioms, so it reports members and fields as removed when the source still has them.

Neither cause can be cleared inside this slice:

- Adopting a genuine removal is exactly what D-adopt-gate forbids, and the doctrine has no approved path for a reviewed removal.
- Adopting the fresh extraction anyway would make things worse. As a scratch counterfactual, `validate.py` on push/90 against the fresh `585534d` contracts gives **143 errors / 17 warnings**, up from 56 / 25. Most of the new errors are false rejections of valid AI targets.

The pass also found, and test-proved, four pre-existing defects in the current tooling (§6).

## 2. Source-selection ledger

| Revision | Role | Commit date | Suitable for a bounded correction? |
|---|---|---|---|
| `bdec2883748f029a0ecb93505adfdcbae6851fe9` | Stamped source of 45c/45d/45e/45f/45g | 2026-08-29 | Baseline only. The current extractor reproduces all three gated files atom for atom (§3). |
| `585534d7eb21d6f0dd678d5c3eb92662f611d39b` | Release-tested pin for Ghost Ship (push/90/93/94, Stage 2 harness) | 2026-10-11 | **Chosen candidate.** It is the only pin with release evidence behind it. Gate fails (§3). |
| `6e4429d65f466b0df9fca3f9917b6dd427df7573` | Sentinel signal (`state/schema_sentinel.json`, `docs/DRIFT.md`) | 2026-10-12 | Signal only. It is not an adoption instruction, and the gate fails. |
| `f8c04d029ea58007bf2947dbddb94c446e15dbb5` | Upstream `main` HEAD, verified by `git ls-remote` during this pass | 2026-10-12 | Unverified for content. Its 45c and 45d atoms are identical to `585534d`. 45e additionally removes `TOWN` from `SECTOR_TYPES`, `ALLIANCE_VILLAGE_TYPES` and `FACTION_VILLAGE_TYPES`, and removes `warIds` from `privateState` (faction-raids work). |

**Deployment status:** none of these revisions is established as the deployed production build. Forge's field tables `forge/src/runner/fields.json` and `nested.json` carry a fourth pin, `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`. This pass did not reconcile that pin (§6.4).

## 3. Mechanical gate results (exact)

Commands run in scratch, with `$X = skills/building-tnr-content/scripts` and `$D = skills/building-tnr-content/data`:

```
python3 $X/schema_extract.py <src@pin> --ctors|--entities|--constants|--checks|--procedures > x_<pin>/<mode>.json
python3 $X/schema_diff.py --invariants x_<pin>/ctors.json --constants x_<pin>/constants.json
python3 $X/schema_diff.py diff $D/45c_DATA_constructors.json   x_<pin>/ctors.json
python3 $X/schema_diff.py diff $D/45d_DATA_entity_schemas.json x_<pin>/entities.json
python3 $X/schema_diff.py diff $D/45e_DATA_constants.json      x_<pin>/constants.json
```

| Check | bdec2883 (reproduction) | 585534d | 6e4429d | f8c04d0 |
|---|---|---|---|---|
| `--invariants` | 0 (128 variants) | 0 (139) | 0 (139) | 0 (139) |
| diff 45c | **0** (0 additions) | **1** (219 breaking) | 1 (219) | 1 (219) |
| diff 45d | **0** (0 additions) | **1** (42 breaking) | 1 (42) | 1 (42) |
| diff 45e | **0** (0 additions) | **1** (45 breaking) | 1 (47) | 1 (47) |

- Extraction is deterministic. Re-running `--ctors`, `--entities` and `--constants` at `585534d` gave byte-identical output:
  - ctors `afa6468da32cd779…`
  - entities `242bbdd02eb99d6c…`
  - constants `f67b62717d940b9b…`
- The full gate output at `585534d` is in `docs/reviews/qw0a_evidence/gate_585534d_45{c,d,e}.txt`. The tool truncates at 60 rows; the untruncated atom sets are in `docs/reviews/qw0a_evidence/atoms_bdec2883_to_585534d.txt`.

## 4. Classification of every breaking change at 585534d

Tier key, following `docs/00_INDEX.md`:

- **SV** — source-verified at `585534d`. File and line are cited, under `app/src/validators/` unless stated.
- **TP** — test-proven by a command in this report.

### 4.1 Extractor blind spots: the source still accepts what the diff calls removed

| ID | Diff atoms | Source idiom the extractor misreads | Tier |
|---|---|---|---|
| E1 | 15 tags × `statTypes` members (absorb, afterburn, damage, decreasestat, increasestat, lifesteal, pierce, recoil, redirection, reflect, rob, timecompression, timedilation, wound, plus the 4 damage-given/taken tags in G1) | `IncludeStats.statTypes` is now a **multi-line** expression, `z\n.array(z\n.enum([...StatTypes, "Highest"]).transform(Highest→None))` (`combat.ts:137-143`). The extractor drops the field entirely. | SV, TP (fresh 45c: `damage` has no `statTypes`) |
| E2 | `AllTags.{de,in}creasemaxpools.poolsAffected` Health/Chakra/Stamina | `MaxPoolTypes = [...PoolTypes, "Energy"]` (`drizzle/constants.ts:436`) is emitted as the literal `"...PoolTypes"` plus `"Energy"`. The real set is a superset. | SV |
| E3 | 9 AI action variants × `target`, all 9 `AvailableTargets` members | `AvailableActionTargets = [...AvailableTargets, "COORDINATE"]` (`ai.ts:147`) is emitted as `["COORDINATE"]` (45e) and `"...AvailableTargets"`, `"COORDINATE"` (45c). The real set is a superset. | SV, TP (§5: 71 false rejections) |
| E4 | 45d `aiRule.action`, `aiRule.conditions`, entity dropped | `export const AiRule = z\n  .object({` is multi-line (`ai.ts:264`). `SCHEMA_RE` needs `z.object({` on one line. | SV |
| E5 | 45d `item`/`jutsu` `required{Strength,Speed,Intelligence,Willpower}` type `preprocess` lost | `makeCappedNullableNumber` moved to `validators/base.ts:10`. The helper resolver only looks in the same file, so type and nullability are lost. | SV, TP (§5: 16 false "not nullable" errors) |
| E6 | 45e `UserStatNames` 12 members | `UserStatNames = [...CombatStatNames, ...MasteryNames]` (`drizzle/constants.ts:746`) is emitted as two literal spread strings. | SV |

### 4.2 Genuine source changes: the gate is right to stop

| ID | Diff atoms | Source evidence | Tier |
|---|---|---|---|
| G1 | `AllTags.{in,de}crease damage{given,taken}`: `statTypes` and `generalTypes` removed; `elements` added | The four tags no longer spread `...IncludeStats`. They declare `elements` only (`combat.ts:239-260`). | SV |
| G2 | `AllTags.elementalseal.elements` removed | `ElementalSealTag` has no `elements` and now seals "all elemental 60 AP jutsu" (`combat.ts:858-863`; at bdec2883 it had `elements ... prefault(["Fire"])`). | SV |
| G3 | 45d `item`/`jutsu`: 16 fields `required{Ninjutsu,Genjutsu,Taijutsu,Bukijutsu}{Offence,Defence}` removed; 6 `required*Mastery` added | Migration 0056 unified combat stats. The validators declare `required*Mastery: makeCappedNullableNumber(MAX_MASTERY_CAP)` (`combat.ts:1540-1549`). | SV |
| G4 | 45e `StatNames`: 8 offence/defence members → `["offence","defence"]`. `StatTypes` "Highest" → "None". `privateState`/`publicState` member churn. | `libs/combat/constants.ts:48,94,134`; `drizzle/constants.ts:390`. The `Highest` → `None` change is softened at the write boundary: `IncludeStats` still accepts `"Highest"` and stores `"None"`. | SV |

### 4.3 Gate-labelling quirk

| ID | Diff atoms | Finding | Tier |
|---|---|---|---|
| Q1 | 45d `now-required` × 24 (farm*, isFarm*, required*Mastery) | These fields do **not** exist in the stamped 45d. `cmd_diff` labels every new field whose `optional` is `False` as "optional → required". The fields carry `.prefault(...)`, so the server lets the key be omitted. The fail-closed outcome is conservative. The label is wrong. | SV, TP |

## 5. Counterfactual: what a naive adoption would do to the canonical validator

Scratch only; nothing was adopted.

```
cd skills/building-tnr-content/data
python3 ../scripts/validate.py ../../../push/90_ghost_ship_skyglass_release.json                        # stamped
python3 ../scripts/validate.py ../../../push/90_ghost_ship_skyglass_release.json \
  --ctors x_585534d/ctors.json --entities x_585534d/entities.json --checks x_585534d/checks.json        # fresh
```

| Contracts | Exit | Result | Change |
|---|---|---|---|
| Stamped (`bdec2883`) | 1 | 56 errors, 25 warnings | Exactly the RUL-2026-10-12-013 ledger |
| Fresh (`585534d`) | 1 | **143 errors, 17 warnings** | See below |

How the fresh run differs from the stamped run:

- **+71 errors from E3:** valid `RANDOM_OPPONENT`, `CLOSEST_OPPONENT` and `SELF` action targets are rejected.
- **+16 errors from E5:** `required{Strength,…}: null` is reported as "not nullable". The server accepts it, and the stamped run correctly notes it as accepted.
- **2 errors change shape:** `statTypes='None' not in enum` becomes `unknown field 'statTypes'` (E1).
- **−8 warnings:** the farm-nullability warnings resolve, because the farm fields now exist.
- **Unchanged:** the 42 stale-effect-field errors, because the extractor also misses `direction: type(...)`, `description: msg(...)` and the cross-module `...rewardFields` spread (`combat.ts:63,67,818-823`).

**Conclusion (TP):** the fresh extraction is less faithful to `585534d` than the stamped file is to `bdec2883`. Adopting it would corrupt the validator, so the gate's refusal is correct.

## 6. Pre-existing defects found (current main, independent of any pin)

1. **The stamped 45c and 45e reject the five basic elements (TP).** `ElementNames` is emitted with the literal member `"...BasicElementName"`, and Fire, Water, Wind, Earth and Lightning are missing.
   - A probe item with `damage.elements=["Fire"]` gives `ERROR … damage.elements='Fire' not in enum (...BasicElementName, Boil, …)`. The same probe with `["Ice"]` gives no elements error.
   - Probe manifests: scratch `probe_el_{Fire,Ice}.json`. Each is the first push/90 item with one `damage` effect substituted.
   - Forge's `nested.json` checks key sets only, so Forge accepts the same payload. That is a Python/Forge disagreement.
2. **The adoption gate does not see union-field removals without enums (TP).** Deleting the non-enum field `AllTags.damage.power` from a copy of the stamped 45c and running `schema_diff.py diff` reports "no breaking changes … (exit 0)". `atoms()` only records enum members for union fields.
   - D-adopt-gate's statement that the gate "fail-closes on … field removals" therefore holds for 45d entities but **not** for 45c tag/objective/action fields.
   - The G1 and G2 removals happen to be caught only because those fields carried enums.
3. **Q1 mislabels new fields as tightened (TP):** see §4.3.
4. **The validator and Forge read different source pins (observed).**
   - Python 45c/45d/45g are at `bdec2883`.
   - Forge `fields.json` and `nested.json` are at `345d18ac`.
   - push/90's own checks used `585534d`.
   - Forge `check_manifest.mjs` exits 0 on push/90, push/93 and push/94, while `validate.py` exits 1 on all three. Parity cannot be claimed until one pin is adopted on both surfaces.
5. **Garbled `raw` in stamped 45d (observed).** Stamped 45d `item.requiredStrength.raw` runs past the helper into `JutsuValidatorRawSchema` and carries a spurious `enum_ref: "WeaponTypes"`. This was not traced further.

## 7. push/90 historical diagnostics: disposition by class

The approved ledger `state/ghost_ship_skyglass_release_validate_exception.json` was not modified, and its gate still holds (§8).

| Ledger class | Errors | Warnings | Classification | Would the pinned contract clear it? |
|---|---:|---:|---|---|
| `stale_effect_fields` | 42 | 0 | Genuine source mismatch: stale catalog | Not with the current extractor (blind spots: `type()`, `msg()`, cross-module spread) |
| `stattypes_none_enum` | 2 | 0 | Genuine source change (G4) plus E1 | No. A raw regen gives "unknown field" instead |
| `consume_companion_rule` | 1 | 0 | Validator law rule (45g `companion_required`, law-owned) is stale against `SuperRefineEffects` (`rounds === 0`) | No. Needs law reconciliation, not regen |
| `idg_power_cap` | 6 | 0 | Deliberate compatibility rule (45g `tag_power_max`, `_class: law`); no server bound | No. Law/lint owner decision |
| `preferredstat_l05` | 1 | 0 | Validator law rule (`AI_CREATE_REQUIRED`, law 14) is stale after migration 0056; Forge is already corrected | No. Law reconciliation plus 45h parity |
| `approved_shared_menu_target` | 4 | 0 | Intended director waiver (content) | Not a contract issue |
| `law60_build_order` | 0 | 9 | Deliberate compatibility rule | Not a contract issue |
| `stale_farm_nullability` | 0 | 8 | Stale catalog | Yes: resolves under fresh 45d (§5) |
| `captured_selftarget_gate` | 0 | 8 | Captured-content waiver | Not a contract issue |

## 8. Gates and tests run (exact; exit codes not masked)

All commands were run on `main@4de2668`. This branch adds only this report and its evidence files.

| Command | Result |
|---|---|
| `python3 push/90_ghost_ship_skyglass_release.validate_exception.py` | exit 0: EXCEPTION HOLDS, 56 errors / 25 warnings at sha256 `6b72054282be…804b0c7` |
| `python3 push/93_ghost_ship_guardian_repair.validate_exception.py` | exit 0: HOLDS, 4 errors / 3 warnings at `840a80fc…2753` |
| `python3 push/94_ghost_ship_skyglass_sentinel_repair.validate_exception.py` | exit 0: HOLDS, 4 errors / 3 warnings at `a31a5884…1988` |
| `node forge/tools/check_manifest.mjs push/{90,93,94}_*.json` | exit 0 ×3 |
| `node --test forge/test/post0056.test.mjs` | exit 0, 3/3 |
| `npm test` (forge, after `npm ci`) | exit 0, 526/526 |
| `python3 factory.py --selftest` (cwd skill `data/`) | exit 0, 20/20 |
| `python3 validate.py --laws` | exit 0, 4 asserted, 0 failed |
| `schema_diff.py diff fixtures/schema_old_sector.json fixtures/schema_new_sector.json` | exit 1 (negative control, expected) |
| `schema_diff.py diff fixtures/schema_old_add.json fixtures/schema_new_add.json` | exit 0 (positive control) |
| `schema_diff.py --invariants fixtures/schema_bad_invariants.json` | exit 1 (negative control, expected) |
| `schema_diff.py --invariants 45c --constants 45e` (stamped) | exit 0 |
| `build_packs.py --check` | exit 0 |
| `lawmap.py .` | exit 0: 0 errors, 5 pre-existing warnings |
| `doctrinemap.py .` | exit 0: 0 errors, 0 warnings |
| `render_doctrine.py --check` | exit 0 |

Notes:

- The first `npm test` run in this container reported 11 failures. They came from the shallow clone: `presentation.*` tests could not read blob `10fb25704dff`. After `git fetch --unshallow`, the suite was 526/526. This is environment-only and involved no code change.
- Brief negative tests "old fields rejected when source proves removal" and "unsupported effect rejected" were **not added**. They presuppose an adopted pinned contract, and none was adopted.

## 9. Smallest viable follow-ups, in order

Each needs its own bounded brief and review.

1. **QW-0A.1, extractor fidelity (Lane A, no adoption).** Teach `schema_extract.py` six things:
   - array-constant spreads `[...X, "lit"]`, both in constants and inside `z.enum([...])`;
   - multi-line field expressions;
   - multi-line `z\n.object(` schema heads;
   - cross-file helper resolution (`validators/base.ts`);
   - the `msg()`/`type()` helpers;
   - cross-module object spreads (`...rewardFields`).

   Acceptance: a fresh extraction at `bdec2883`, diffed against the stamped files, shows only the §6.1 element correction. A fresh extraction at `585534d` leaves only the G1–G4 atoms breaking.
2. **QW-0A.2, gate tightening (Lane A).**
   - Record union-field atoms so §6.2 is caught.
   - Label `now-required` only for fields that existed before.
   - Both changes make the gate stricter, not looser. Add fixtures for each.
3. **Director decision (required before any adoption).** D-adopt-gate has no approved path for a *deliberate, reviewed* removal. G1–G4 and the §6.1 correction are all removals, so as the doctrine stands the stamped contracts can never follow upstream again. Options:
   - (a) A doctrine change that permits adoption against an atom-enumerated, SHA-scoped removal ledger, reviewed like the release exceptions. The gate still fails closed on anything not enumerated.
   - (b) Keep the absolute gate, and accept a permanent `bdec2883` contract plus per-release exceptions.

   Choosing (a) is a change to `docs/DOCTRINE.md` D-adopt-gate through its owner, not something this slice can do.
4. **After 1–3, pinned adoption at the chosen SHA.** Then:
   - add the regression fixtures named in the brief;
   - update validator and Forge parity;
   - run the law reconciliation for law 14 `preferredStat`, `companion_required` and `tag_power_max` through the RULINGS-recorded reconciliation sequence.

## 10. Not begun

QW-0B (Forge version constant), crafting-relation capture, spent-manifest archive/audit, QW-1 and QW-2 through QW-5, Quest Studio integration, any game change, live reads/writes and publication. `state/active-context.md` and `state/status.json` were read and not modified. No historical exception ledger, manifest or gate was touched.
