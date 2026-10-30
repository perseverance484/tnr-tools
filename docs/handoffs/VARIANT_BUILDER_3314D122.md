# Item variant builder, unlockitemvariant.variantId, dungeon onlyOnce + contract re-pin to TheNinjaRPG@3314d122 — 2026-10-29

**Lane:** A (builder/forge, validators, generated contracts). **Rulings:** RUL-2026-10-29-047 (trophies are item variants; "the tooling re-pin to upstream"), RUL-2026-10-29-048 item 6 (Lane A started: re-pin, item variants, `unlockitemvariant.variantId`, dungeon `onlyOnce`).
**Branch:** `fable/variant-builder`, cut from `main@5ef5fbfe` and rebased onto `main@86c08838` before the push (the seven commits between are rulings and `docs/design/` only; RUL-053 makes "variant" the player-facing word, "trophy" stays internal). The frozen head is reported with the push; this file is the handoff for it.
**Game source:** `studie-tech/TheNinjaRPG@3314d122c93e036618483d18229a793ad7ad21fd` (upstream main at the start of this work; previous contract pin `2af4b320`, 499 commits earlier), read only, never executed, from a separate `git worktree` of the game clone.
**Live requests / writes:** 0 / 0. **Credentials:** none. No Skyglass variant, token, dungeon or pet manifest was written; `push/`, `docs/design/`, `docs/RULINGS.md` and `state/` (except the new ledger) are untouched. `docs/DRIFT.md` is left to the sentinel workflow.

## Contract re-pin (2af4b320 -> 3314d122)

Extraction path: `schema_extract.py <3314d122> --ctors/--entities/--constants/--procedures/--checks`, `schema_diff.py --invariants` (6 unions, 152 variants, 0 errors), `schema_diff.py diff OLD NEW --accept state/schema_adoption_ledger_3314d122.json` per file (all five exit 0). Ledger: `scripts/schema_adoption_ledger.py ... --ruling RUL-2026-10-29-047`; `--check` matches at PYTHONHASHSEED 1, 2, 3. Root 45c/45g equal skill `data/`. `fields.json` / `nested.json` re-derived by `derive_fields.mjs` / `derive_nested.mjs` (byte-identical on a second run); the dungeon contract by `derive_dungeon.mjs` (`--check` current).

Before adopting, the unchanged extractor was run at 2af4b320 and reproduced all five committed files except the date stamp. The upstream refactor (router database statements moved into `app/src/queries/*.ts`) changed no procedure Forge calls: `auth_pin_diff.mjs` 0 disagreements across 59 Forge paths, 0 reclassifications; `gameAsset.create` and `profile.getAllAiNames` gained optional nullish inputs (Forge sends none, as before). `pin_relevance.mjs` reports 26 changed surfaces; each content router's create/update/get declarations and placeholder inserts were read (placeholders now in `queries/*.ts`, unchanged).

**Breaking atoms (12, all in the ledger):**

| File | Atom | Class | Handling |
|---|---|---|---|
| 45d | `petSpecies.skillTarget` removed | upstream_field_removed | It moved onto each innate effect: `PetSpeciesEffect = AllTags.and(z.object({skillTarget}))`. New 45c `intersections` section; new `nested.json` `petSpeciesEffect` key set; both validators accept it per effect and refuse it on the species. Pet fixtures moved. |
| 45g | `enums.petSpecies.skillTarget` ENEMIES, SELF | consequence_of_removal | as above |
| 45f | `jutsu.getUserJutsuOwnership` (3 atoms) | upstream_procedure_removed | Not called by Forge or any push file. |
| 45e | 10 members of `IMG_URL_ASSISTANT_ALTERNATIVES` / `TowerDefenseUpgradeTypes` | extractor_comment_glued (new class) | The extractor glued a `// note` line onto the next list member. `strip_comments()` (string-aware) fixes it; this also stops `COPY_PRIORITY_TIERS` showing as changed (a new trailing comment upstream; DRIFT.md listed it as breaking). |
| 45g | `required_on_create.item` `furnitureData` | extractor_ref_default (new class) | `furnitureDataSchema.nullable().prefault(null)`: a named-schema field's literal default was ignored, so it was reported required. |

**Other extractor corrections:** `AvailableEffectTypes` now also excludes `increasejutsuslots` and the activity bonuses (`!isActivityBonus` in validators/ai.ts; any other unrecognised filter term is reported as unresolved). The new `itemVariant` entity target reads `ItemVariantValidator`.

**Additions:** 45c +130 (seven tags: six activity bonuses and `increasejutsuslots`; `unlockitemvariant.variantId`; the intersection); 45d +`itemVariant`; 45e +33; 45f +123 (discord, forum, territoryWar, `item.getVariantNames`, ...); 45g +13. `fields.json`: +`itemVariant`, `petSpecies` -`skillTarget`, `ai` -`avatar3d` (userData column dropped upstream, d45cd0c8; 189 -> 188 keys). `nested.json`: +7 tags, `variantId`, `petSpeciesEffect` (198 slots, 66 sets). Dungeon contract: pin 107d7a86 -> 3314d122, `dropFields` +`onlyOnce`, derived `dropFlags`; bounds and defaults unchanged.

**Effect on existing `push/*.json`:** none. No committed manifest uses a species, `skillTarget`, `avatar3d`, `unlockitemvariant`, a new tag or dungeon drops. Measured, not inferred (below).

## What changed

**Forge 0.12.0 (`@x-release-pending 0.12.0`; the loader keeps the released 0.11.0 `@version` and `@require` pin `36c5201b`).**
- `src/runner/variants.mjs` (new): entity `itemVariant`, ref prefix `@variant:`. Recipe: one mutation `item.upsertItemVariant {itemId, variant}` creates (no `variant.id`) and replaces the whole record (with it). Reads: `item.getItemVariants {itemId}` (protected, no limiter) for merge, read-back and reconciliation, through a recipe `read` hook (`Runner._get`), never cached. Two procedure rows.
- Create: pre-create read of the item's variants. The 7-variant cap and a taken order fail the item before any send. The ids are recorded on the journal item (`variantSnapshot`). After the send (which answers no id), a second read binds the single new row at the planned order holding the asserted keys. Any other result is ORPHANED with candidates and pauses. A failed read leaves the item SENT, and `resume()` reconciles it to ORPHANED. Only the operator's adopt binds a row; nothing is re-sent.
- Edit: fetch-merge over the live row; a stored null `description`/`battleDescription` is omitted (z.string().optional() refuses null).
- Pre-send bounds: name 1-191 trimmed, image `@img` or URL <= 512, cost int 0..2^31-1, order 1..7, descriptions strings, `requiredItemId` only on VARIANT_TOKEN, `furnitureData` object/null, `itemId` required on every variant entry, `id` refused.
- Lint "VARIANT":
  - refuses a token item that is not CONSUMABLE / SELF / SINGLE / destroyOnUse / preventBattleUsage;
  - refuses a bad `variantId` and two creates at one `(itemId, order)`;
  - refuses a variant created with `requiredItemId` naming a same-manifest token whose `unlockitemvariant` already names a variant (the server accepts only null before the variant has an id);
  - warns on a purchasable cost type and on a token variant without `requiredItemId`.
- `unlockitemvariant.variantId` is in the nested key set; `@variant:` refs resolve at send time like every ref.
- Dungeon: `onlyOnce` must be a boolean. `derive_dungeon.mjs` reads `src/queries/dungeon.ts` (the entrance-asset lookup moved there) and asserts the onlyOnce identity `(type, id)` and the per-player, per-dungeon history.
- Pets: species effects take `skillTarget` (from `nested.json`, fail closed without it).
- Tools: `auth_pin_diff.mjs` covers petSpecies/badge/title; `pin_relevance.mjs` gains `validators/item.ts` and nine `src/queries/*.ts` surfaces.

**Skill.**
- `schema_extract.py`: `strip_comments`, the named-schema default, `intersections`, the `itemVariant` target, `AvailableEffectTypes`.
- `schema_diff.py`: intersection atoms (removal breaking). Ledger: classes `extractor_comment_glued` and `extractor_ref_default`, each re-checked against source, plus a string-aware declaration read.
- `validate.py` + new `variant_checks.py`:
  - itemVariant keys, required, enums and bounds; the token rules; `variantId`;
  - the same-manifest token-binding rule and `(itemId, order)` twins;
  - visibility warnings;
  - where the 3314d122 tags may live (activity bonuses: bloodline or ARMOR/ACCESSORY/KEYSTONE/CRYSTAL items only; `increasejutsuslots` on token-like consumables, at most `MAX_EXTRA_JUTSU_SLOTS`);
  - species effect `skillTarget` (and L09 does not flag it); `@variant` refs; build order.
- `references/pipeline.md` §2.10 (labelled source-verified, NOT behaviour-proven); packs re-rendered (hash stamps).

## Gates (exact)

| Gate | Result |
|---|---|
| `npm test` (forge/) | 770 tests, 757 pass, **1 fail**, 12 skipped. The failure is `gates.test.mjs` "the checked bundle is inside its raw and gzip budget". Base `5ef5fbfe`: 756 / 745 / 0 / 11. |
| `TNR_GAME_CHECKOUT=<3314d122> node --test test/catalog test/pets test/variants test/dungeon test/dungeon.review test/dungeon.rereview` | 110 / 110 |
| `npm run build` twice | byte-identical, sha256 `98c9e41e2b4ed67b02ca31f617cca262b3e4bc20638fa0249d96141cd5f69676` |
| `npm run fixtures` then `git diff --exit-code` | clean (real `node_modules` copy) |
| `check_boundaries` / `check_imports` / `check_release_pin` | 0 violations (pin 3314d122) / 0 / ok |
| **`check_bundle_budget`** | **exit 1: raw 461,813 / 455,000 (101.5%), gzip 110,989 / 109,500 (101.4%)** |
| `derive_dungeon.mjs <3314d122> --check`; `derive_fields`/`derive_nested` at the pin | current; byte-identical to the committed files |
| `check_manifest.mjs` and `validate.py` (cwd skill `data/`) on all 120 `push/*.json` | per-file exit codes, full `check_manifest` output and full `validate.py` output identical to base; `validate.py --strict` exit codes identical (14 fail at both, pre-existing) |
| New fixtures (`test/fixtures/variants/`, `dungeon/onlyonce_manifest.json`) | 2 good + the onlyOnce one pass both gates; `variant_bad.json` refused by both |
| `python3 -m unittest scripts/test_pet_species.py scripts/test_schema_diff.py scripts/test_catalog_checks.py scripts/test_variant_checks.py` | 34 OK |
| `selfcheck.py --generated .` (data/) / `factory.py --selftest` | 0 errors / 20/20 |
| `doctrinemap.py .` / `render_doctrine.py --check` / `build_packs.py --check` (after `--write`) | 0/0 / current / current |
| `lawmap.py .` | 93 laws, 0 errors, 5 pre-existing warnings (16d, 18, 37, 61, 69) |

Mutation checks (reverted): binding a row without the asserted-key match fails "a row at the planned order that does not hold the plan"; sending a null description fails the recipe test; removing the token-binding lint fails the lint and parity tests.

## Bundle budget: over, not raised (the director's decision)

- Base 450,662 / 108,381 -> 461,813 / 110,989 (+11,151 raw / +2,608 gzip).
  - Data: +845 raw (`fields.json` +244, `nested.json` +469, dungeon contract +132).
  - Code, after comment stripping: `variants.mjs` +3.5 KB, `runner.mjs` +2.1 KB, `lints.mjs` +2.0 KB, `reconciler.mjs` +1.3 KB, the rest about +1.1 KB.
- **Smallest raise that passes: raw 461,813 / gzip 110,989** (zero headroom). Any later change would need another step. **466,000 / 112,000** would leave about 4.2 KB / 1.0 KB.
- No trim inside the feature closes a 6.8 KB raw gap. Dropping the VARIANT lints saves about 2 KB and moves those refusals to the server, where the variant create is refused before writing but a token create is not. Dropping the pre-create read would leave no way to find the new id.

## Known debt, deviations, open decisions

1. **Bundle budget** (above): the director's decision.
2. **Decision: variants have no hidden state.** A variant appears in its base item's Variants list for every owner from the moment it is created. A token variant shows as "Need <token name>": the name comes from `item.getAllNames`, which lists hidden items too. Any other cost type can be bought at once. The tooling warns but does not choose; the create order and timing are the publishing step.
3. **Decision: the shared Skyglass Token (RUL-048, `variantId: null`) also unlocks any older VARIANT_TOKEN variant without `requiredItemId`, for a player who owns that variant's item** (`consumeVariantToken`, routers/item.ts:1498-1510). Accept, or audit the live token variants first.
4. **1:1 trophies need two manifests:**
   - a token create (`variantId: null`) and the variant create (`requiredItemId: @item:<token>`);
   - then a token edit with a literal `targetId` setting `variantId` (an `@variant` ref from the idmap, or the literal id).

   Both gates refuse the one-manifest form that names the variant before it exists. Until the edit lands, the token can unlock any other token variant without a required item.
5. **Assumed:** the live game runs 3314d122 or later. `requiredItemId`, `variantId` and `onlyOnce` do not exist before it.
6. onlyOnce history counts only receipts written after the field existed. A new dungeon has no earlier receipts, so this does not matter for the Wreck.
7. Forge does not mirror the new tags' placement rules (`validate.py` does). The server refuses them only at an item or jutsu UPDATE, after the placeholder exists.
8. Hand-held values, each compared with source by the checkout-gated test: `MAX_VARIANTS` (7) and the two column limits. Forge does not check the `costType` enum or the `furnitureData` shape: zod refuses both before writing; `validate.py` checks the enum.
9. Variant descriptions go through `sanitizeVariantText`, so markup may read back as drift. `validate.py` warns.
10. Not re-run: the 2af4b320 and 85cecae ledgers' `--check` under the updated ledger tool.

## Not done / not begun

- No browser, live or session checks; no Forge release; the old builder (`builder_bundle.js`) was not extended.
- No Skyglass variant, token, Little Horror jar or Wreck manifests; no variant capture manifest; no answers/ catalogue of live variants.
- `docs/DRIFT.md`, `docs/RULINGS.md` and `state/` (digest/board) not edited.


## Budget: resolved

The director raised the budget to **466,000 / 112,000** (RUL-2026-10-29-054). After the raise:
- `check_bundle_budget` exits 0, at raw 461,813 / 466,000 and gzip 110,989 / 112,000.
- The bundle is byte-unchanged.

## Review round 1 (ChatGPT on `81295b8b`: no P0/P1, three P2)

All three accepted. Each has a test that fails on `81295b8b` and passes after the fix.

| Finding | Fix | Test |
|---|---|---|
| **F1** A token create could omit `target`. `item.create`'s placeholder holds `target: "CHARACTER"` (queries/item.ts `insertItemForCreate`), the fetch-merge kept it, and the update failed. | **Both gates:** a create of an item carrying `unlockitemvariant` or `increasejutsuslots` must state `target: "SELF"`, `destroyOnUse: true` and `preventBattleUsage: true`. Each is refused if stated otherwise, on edits too. `method` and `itemType` may be omitted on a create: the placeholder holds `method` SINGLE (schema default) and `item.create` takes the type, CONSUMABLE when omitted. **Forge:** `lints.mjs` "VARIANT". **Python:** `variant_checks.py`, `PLACEHOLDER_OK`. | Forge "review F1" (each of the three keys removed from the token fixture is refused; omitting method/itemType or an edit's target is accepted). Python `test_r1_f1_token_create_states_target`. |
| **F2** Forge accepted invalid placements of the 3314d122 tags; Python and the game refused them, the game only at the update after the placeholder existed. | **Forge preflight (lint "VARIANT"), at parity with `variant_checks.py`:** activity bonuses are refused on jutsu, species and non-gear items; slot grants are refused off items; token requirements apply as F1. The six-name list `ACTIVITY_BONUSES` and `MAX_JUTSU_SLOTS` (2) live in `variants.mjs`, compared with combat.ts/constants.ts by the checkout-gated test. **Both gates:** an item create without `itemType` counts as CONSUMABLE (what Forge creates), so it cannot carry an activity bonus; Python had let it through. | Forge "review F2/F3" (consumable / untyped create / jutsu / species refused, ARMOR accepted) and the gated source test. Python `test_r1_f2_omitted_item_type_is_consumable_on_create`. |
| **F3** Python counted an omitted `power` as 0, so three slot grants passed; the game prefaults each to 1. | **Python:** sums with the extracted 45c default (`AllTags.increasejutsuslots.power.default` = 1; `check_effects_placement` now gets the constructors). **Forge:** `power ?? 1`, the prefault the gated test reads at source. Both report the total. | Python `test_r1_f3_slot_power_defaults_before_summing` (three defaulted grants refused, two accepted). Forge "review F2/F3" (three defaulted grants refused as 3, two accepted). |

Not changed: L18 (`noncombatconsumereward`) still checks only a stated `target`, the same shape as F1 for reward items. It is pre-existing, outside these findings, and changing it could move `push/*.json` results.

### Gates (round 1, exact)

| Gate | Result |
|---|---|
| `npm test` (forge/) | 773 tests, 760 pass, 0 fail, 13 skipped |
| Source-gated, `TNR_GAME_CHECKOUT=<3314d122>` (catalog, pets, variants, dungeon x3) | 113 / 113 |
| `npm run build` twice | byte-identical, sha256 `e259f57cb8b790ccc2f745daedbf87c69d2b10f41e3c9a8ad020f08c9f6ace96` |
| `npm run fixtures` then `git status` | clean |
| `check_boundaries` / `check_imports` / `check_release_pin` | 0 / 0 / ok |
| `derive_dungeon.mjs --check` | current |
| `check_bundle_budget` | exit 0: **raw 463,070 / 466,000 (99.4%), gzip 111,355 / 112,000 (99.4%)**, +1,257 / +366 over `81295b8b` |
| `check_manifest.mjs` and `validate.py` on all 120 `push/*.json` vs `81295b8b` | outputs and exit codes identical; `--strict` exit codes identical (14 fail at both) |
| Python unit tests (pet_species, schema_diff, catalog_checks, variant_checks) | 37 OK |
| `selfcheck --generated` / `factory --selftest` | 0 errors / 20/20 |
| `doctrinemap` / `render_doctrine --check` / `build_packs --check` | 0/0 / current / current |
| `lawmap` | 0 errors, 5 pre-existing warnings |

Contracts, ledger, `fields.json`, `nested.json`, the dungeon contract and the loader are unchanged. Live requests / writes: 0 / 0.

## Review round 2 (ChatGPT on `6956bf66`: F1-F3 verified; one P2 and the L18 advice)

Branch fast-forwarded to the bot's `da94470b` (skillpack dist rebuild) first. Each fix has a test that fails on `da94470b` and passes after it.

| Item | Fix | Test |
|---|---|---|
| **1 (P2)** Forge added a string slot power to the running total (`"1"` + `"1"` = `"011"`, refused); `validate.py` skipped non-numbers (accepted `"abc"`). | Commit `005181ac`. **Both gates** coerce like the pinned `z.coerce.number().int().min(1).prefault(1)`. An omitted power is 1 (Python reads the 45c default); a given one goes through JavaScript `Number()` (Python: `_zod_number`). A power that is NaN, not an integer, or below 1 is refused per effect, and only valid powers count toward the cap. **Known difference:** Python refuses some strings `Number()` accepts (hex such as `"0x1"`, `"Infinity"`). It is stricter, never looser. | Forge "review round 2 (1)" and Python `test_r2_slot_power_coerced_like_zod`: 1 + `"1"` and `"1"` + `"1"` accepted; `"1"` + `"1"` + 1 refused as 3; `"abc"`, -1 and 1.5 refused. |
| **2 (advice)** L18 (`noncombatconsumereward`) checked only a stated `target`. | Separate commit `67903359`. **Forge:** a create with `target` omitted now fails L18 (the placeholder holds `CHARACTER`); an edit may still omit it, because it merges the live value. **Python:** unchanged, because `validate.py`'s L18 already refused an omitted target (on edits too, stricter). The six reward-item entries in `push/*.json` all state `SELF` (97 x3 creates; 132, 133, 319 edits); outputs unchanged. | Forge "review round 2 (2)": omitted and CHARACTER refused on a create, SELF accepted, an edit without target accepted; `validate.py --strict` refuses the omitted-target create. |
| **3** The distributed skill ZIP must carry the corrected validators. | `dist/` is built by the skillpack workflow on push. The frozen head is the bot's dist commit on top of these commits, checked against the tree (reported with the push). | n/a |

### Gates (round 2, exact)

| Gate | Result |
|---|---|
| `npm test` (forge/) | 775 tests, 762 pass, 0 fail, 13 skipped |
| Source-gated, `TNR_GAME_CHECKOUT=<3314d122>` (catalog, pets, variants, dungeon x3) | 115 / 115 |
| `npm run build` twice | byte-identical, sha256 `871026de765db3e022d26c609e4d9307186d1d37e3dc1af075fc2a15c7c818d4`; the committed bundle equals a fresh build |
| `npm run fixtures` then `git status` | clean |
| `check_boundaries` / `check_imports` / `check_release_pin` | 0 / 0 / ok |
| `derive_dungeon.mjs --check` | current |
| `check_bundle_budget` | exit 0: **raw 463,369 / 466,000 (99.4%), gzip 111,448 / 112,000 (99.5%)** |
| `check_manifest.mjs` and `validate.py` on all 120 `push/*.json` vs `da94470b` | outputs and exit codes identical; `--strict` exit codes identical (14 fail at both) |
| Python unit tests (pet_species, schema_diff, catalog_checks, variant_checks) | 38 OK |
| `selfcheck --generated` / `factory --selftest` | 0 errors / 20/20 |
| `doctrinemap` / `render_doctrine --check` / `build_packs --check` | 0/0 / current / current |
| `lawmap` | 0 errors, 5 pre-existing warnings |

Live requests / writes: 0 / 0.
