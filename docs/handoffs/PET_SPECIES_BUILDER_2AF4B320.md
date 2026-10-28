# Pet species builder support + contract re-pin to TheNinjaRPG@2af4b320 — 2026-10-28

**Lane:** A (builder/forge, validators, generated contracts). **Ruling:** RUL-2026-10-28-012 ("Builder route ok").
**Branch:** `fable/pet-species-builder`, cut from `main@34a2ae8f`. The frozen head is reported with the push; this file is the handoff for it.
**Game source:** `studie-tech/TheNinjaRPG@2af4b32066c39e2868efae5dba6b339278701dca`, read only, never executed. Previous contract pin `85cecaeb` (434 upstream commits earlier).
**Live requests / writes:** 0 / 0. **Credentials:** none. No Skyglass pet manifest was written; `push/`, `docs/design/` and the Skyglass `state/` files are untouched.

## What changed

**Builder (Forge 0.10.0, `@x-release-pending 0.10.0`; loader keeps the released 0.9.1 pin).**
- New manifest entity `petSpecies` and ref prefix `@petSpecies:`. Recipe: one-step `petSpecies.create` (whole record, id in `message`), `petSpecies.update {id, data}` fetch-merged over the derived field set, read-back `petSpecies.get`, names `petSpecies.getAll`. Four procedure rows (auth/limiter transcribed from the router and `trpc.ts:255-258`).
- `src/runner/pets.mjs`: `PetSpeciesValidator` refinements, isActive:false on create, `hidden` stripped (no column), and `isPetJutsuAllowed` (minus `hidden`) on any jutsu whose merged record is `jutsuType PETS`; `requiredPetSpeciesId` needs PETS.
- `lints.mjs` PET lints: a default that is a jutsu created in the same manifest (hidden, so the server refuses it), a locked default on a species create, a default locked to another literal species id, and `reward_pets` needing standard rewards / at most one per item / `preventBattleUsage:true`.
- Reconciler: a lost `petSpecies.create` is ORPHANED with `matches` evidence; only the operator's adopt binds a row (never re-sent).
- `fields.json`/`nested.json` re-derived at 2af4b320. Additions only: `petSpecies` entity; `siphon` tag; `reward_pet_experience`, `reward_level`, `reward_stats` on rewards; eleven SimpleTasks.
- `derive_fields.mjs`: finds `insertAiSchema` in `validators/aiInput.ts` (moved upstream in 8d14dbef; refuses an ambiguous declaration). `derive_nested.mjs`: task enums follow `...List` and `...Object.values(OBJ)` spreads (fail-closed on an unresolvable one); unchanged output at 85cecae.
- `pin_relevance.mjs` gained the petSpecies router/validator and `libs/pets/abilities.ts` as surfaces.

**Skill.**
- `schema_extract.py`: `petSpecies` entity target; `X.shape.key` field references (aiRules/includeDefaultRules were silently dropped); `z.array(...)` fields take bounds and optional/nullable/coerce from the OUTER chain (also corrects `item.craftingRequirements`, which had carried its element's `.min(1).max(...)`, `coerce`, `int`); inline `.superRefine((...` recorded as `<inline>` (petSpecies, aiRule); `...Object.values(OBJ)` list members; `validators/pets.ts` local enums (PET_AI_*).
- 45c/45d/45e/45f/45g regenerated and adopted (root 45c/45g copies equal skill data/). Ledger `state/schema_adoption_ledger_2af4b320.json`: 5 breaking atoms, all verified — 1 `upstream_const_member_removed` (ACTIVE_VOTING_SITES lost `bbogd`), 4 `upstream_bound_changed` (45g cap_100: item/jutsu `requiredLevel`, quest `requiredLevel`/`maxLevel` now `.max(MAX_PLAYER_LEVEL)` = 110).
- `schema_adoption_ledger.py`: new class `upstream_bound_changed` (bound read from the field declaration at both pins, named constant resolved at the new pin) and an optional `--ruling`.
- `validate.py` + new `pet_checks.py`: petSpecies keys/required/enums/lengths/refinements/pet AI allowlists (from 45d/45g/45e), the isPetJutsuAllowed mirror, species-default rules, reward_pets/reward_pet_experience rules, `@petSpecies` refs, slot-aware build order (species create before jutsu, species edit after).
- `references/pipeline.md` §2.8 (labelled source-verified, not behaviour-proven); packs/TOCs re-rendered (hash stamps only).

**reward_pet_experience / reward_pets (task item 3):** both are on item `noncombatconsumereward` in 45c and Forge `nested.json`. `reward_pet_experience` is also on quest rewards and every objective. `reward_pets` is **not** a quest reward at source (`QuestReward`/`ObjectiveReward` lack it): a quest grants a pet by rewarding the item.

## Gates (exact)

- `node --test` via `npm test` (forge/): 734 tests, 724 pass, 0 fail, 10 skipped (after the budget raise below). Base `34a2ae8f`: 721 / 712 / 0 / 9. `test/pets.test.mjs` 13/13; its source-comparison test runs with `TNR_GAME_CHECKOUT=<2af4b320 checkout>` (passed) and is skipped otherwise.
- `npm run build` twice: byte-identical. `npm run fixtures` then `git diff --exit-code`: clean.
- `check_boundaries` 0 violations (pin 2af4b320), `check_imports` 0, `check_release_pin` ok.
- `check_bundle_budget` exit 0: raw 444,780 / 446,000, gzip 107,068 / 108,000 (base 435,145 / 105,126). Raised from 436,000 / 105,500 by the director (RUL-2026-10-28-014).
- `node tools/check_manifest.mjs` on every `push/*.json`: identical per-file results to base (6 refuse at both). Fixtures: 4 good pass, 4 bad refused.
- `validate.py` (cwd skill data/) on every `push/*.json`: identical exit codes and error/warning counts to base (116/121 pass; 229, 319, 90, 93, 94 fail at both). `validate.py --strict` on the fixtures: 4 good exit 0, 4 bad exit 1.
- `schema_extract.py <2af4b320> --ctors/--entities/--constants/--procedures/--checks`: byte-identical to the adopted files. Run at 85cecae, the patched extractor changes nothing in the committed files except: the new petSpecies entity and its 45g entries (only additions; `null_strip_exempt` gains `artDirection`, `preferredDamageElement`), PET_AI_* in 45e, `aiRule.superRefine` `[]` -> `["<inline>"]`, and the `item.craftingRequirements` bound/flag correction.
- `schema_diff.py --invariants`: 143 variants, 0 errors. `schema_diff.py diff OLD NEW --accept state/schema_adoption_ledger_2af4b320.json`: exit 0 for all five.
- `schema_adoption_ledger.py ... --check ... --ruling RUL-2026-10-28-012`: matches at PYTHONHASHSEED 1, 2, 3.
- 45d fields equal Forge `fields.json` for all six content entities; 45c key sets equal `nested.json` for tags, objectives (by task), AI conditions and actions.
- `python3 -m unittest scripts/test_pet_species.py` 7/7; `scripts/test_schema_diff.py` 9/9; `selfcheck.py --generated data` 0 errors; `factory.py --selftest` 20/20.
- `doctrinemap.py .` 0/0; `render_doctrine.py --check` current; `build_packs.py --check` current (after `--write`); `lawmap.py .` 0 errors, 5 pre-existing warnings.
- Not run: `validate.py --parity` (pre-existing TypeError on `checks:null`).

## Known debt, deviations, open decisions

1. **Bundle budget: resolved.** The director raised it to 446,000 / 108,000 (RUL-2026-10-28-014).
2. **Interpretation to confirm:** species have no `hidden` column; this branch treats `isActive:false` on create as the species' hidden-on-create and refuses `isActive:true` on create. Activation stays a publishing act.
3. **Build order needs a publish between steps 2 and 3.** The server refuses hidden defaults, and every jutsu create ships hidden, so the species-defaults edit can only run after the director publishes the signature jutsu. Both gates refuse the one-manifest form.
4. **Law reconciliation flagged, not done:** law 8's cap of 100 on `maxLevel` (validate.py `CAP_100`) is stale at source (`MAX_PLAYER_LEVEL` 110); `requiredLevel` likewise. validate.py still applies the law text.
5. Forge refuses ANY edit of a live PETS jutsu that already fails isPetJutsuAllowed. Forge does not mirror the pet AI action/effect allowlists (server refuses those before writing; validate.py checks them).
6. 45c `reward_pets` still shows the element's `min 1 / max 191` (the outer-bound fix was applied to 45d entity fields only); validate.py enforces the real cap of 1 from 45e.
7. The 85cecae ledger is kept as history; its `--check` no longer reproduces under the updated tool (new class list).
8. `isPetJutsuAllowed`'s effect list and link/mastery keys are hand-held in `pets.mjs` and `pet_checks.py` (they live in `libs/`, not a validator); the checkout-gated Forge test compares them with source.

## Not done / not begun

- No browser, live or session checks; the old builder (`builder_bundle.js`) was not extended or run; no Forge release.
- No Skyglass species/jutsu/jar manifests, no live species or PETS jutsu catalogue capture, no answers/ catalogue for species, no `petSpecies.get` full-persistence capture path.
