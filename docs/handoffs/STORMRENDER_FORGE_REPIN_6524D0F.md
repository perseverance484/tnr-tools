# Contract refresh to TheNinjaRPG@6524d0f: Forge re-pin + extractor fix + skill-data adoption — 2026-10-20

**Lane:** A (code/tooling/generated contracts). **Ruling:** RUL-2026-10-20-001 ("Do B ... one big pass and put it in for review").
**Branch:** `claude/stormrender-highest-scaling-yj2nef`, built on PR #73 head `590c0d8968d21aa53713276ef2faacf2fb42b84c` (merge-base `main@383ac0f`). The `chatgpt/*` branch was not modified. The push/131 manifest is unchanged.
**Game source:** `studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb` (new), `bdec2883` (previous skill data), `94f9d84` (previous Forge pin). Read only, never executed.
**Live requests / writes:** 0 / 0. **Credentials:** none.

## Outcome

| Gate | Before | After |
| --- | --- | --- |
| `node forge/tools/check_manifest.mjs push/131_…json` | 1 problem (`elementaldamage` unknown) | **0** |
| `validate.py push/131_…json` (cwd skill `data/`) | 3 errors | **0 errors, 0 warnings** |
| `validate.py` over all 86 `push/*.json` | 81 pass / 5 fail | **83 pass / 3 fail** (90/93/94, see below) |
| `schema_diff.py diff` per file, adopted files | — | exit 0 with `--accept state/schema_adoption_ledger_6524d0fb.json` |

## Part 1 — Forge 0.8.1 (commit `31b3697` + follow-up)

- `forge/tools/derive_nested.mjs` reads `Base.omit/pick/extend` derivations (`ElementalDamageTag`), fail-closed on any other chained call. It **also no longer reads commented-out enum members as live values**: at both pins `SimpleTasks` etc. contain `// "anbu_kills",` and Forge accepted six quest tasks the server refuses (anbu_kills, tournaments_won, village_funds_earned, any_missions_completed, any_crimes_completed, students_trained). With that fix, Forge's objective set equals the skill extractor's `allObjectiveTasks` exactly (64).
- `fields.json` / `nested.json` re-derived at 6524d0f. The adopted item contract equals the live Stormrender capture's columns exactly. At 6524d0f `jutsu.update` nulls `requiredPetSpeciesId` and `quests.update` nulls `petTaskMinutes` when omitted, so the old contract would have lost data.
- `pin_relevance.mjs` (16 surfaces changed) was read surface-by-surface: limiter, procedure paths/auth, the `item.update` whole-record save, the `/forge` host and the review-desk procedures are unchanged in what Forge relies on.
- Regression tests: the captured Stormrender row + push/131 edit through `mergeForUpdate` and pre-send validation; commented-out tasks refused. Version 0.8.1, `@x-release-pending 0.8.1`; the loader keeps the released 0.8.0 pin.

## Part 2 — `schema_extract.py` blind spots fixed

Each was confirmed at both bdec2883 and 6524d0f. At bdec2883 the fixed extractor **removes nothing** relative to the committed files; it only adds what was missed and corrects values, for the reasons below.

| Blind spot | Effect in the old files |
| --- | --- |
| Line-based object parser: multi-line fields, `z\n .object({`, `...X.shape`, cross-file spreads, `Base.omit().extend()`, block-bodied helpers (`msg`, `type`) | `description`/`direction` missing on every tag (the push/131 `increasedamagetaken` errors); reward_* missing on `noncombatconsumereward` (push/97); `statTypes` missing on all tags at 6524d0f; `elementaldamage` and `noncombatconsumereward` missing |
| Spread precedence first-wins (zod is last-wins) | 45g `tag_power_max` 100 on 61 tags whose real `power` has no max (the mistake Forge `validate.mjs` documented) |
| `0` dropped (`v not in (None, False)`) | every `default: 0`, `min: 0`, `max: 0` missing |
| A nested object's keys attributed to the outer variant | `dialog.text`; inner bounds/defaults reported as the field's own |
| Fields typed by a named schema dropped | `coordinateTargeting` (all tags), `allyAIs`, `applyBuffs`/`applyDebuffs`, AI `coordinates` refused as unknown. Now resolved to the zod constant when there is one, else an opaque `{"type":"ref"}` (present, no claims) |
| `[...Name, "x"]` constant lists | `ElementNames` held `"...BasicElementName"` instead of Fire/Water/Earth/Wind/Lightning; `MaxPoolTypes` lost Health/Chakra/Stamina |
| One commented-out member dropped a whole list | `SimpleTasks` and every list spreading it |
| Helper body read as a fixed 600-char window | `enum_ref: WeaponTypes` on every stat requirement (`requiredStrength`, …) |
| 45d entity spreads and named-schema fields unresolved; `export const AiRule = z\n .object` | at 6524d0f upstream moved columns into `itemEconomySchema`, `furnitureItemSchema` and `masteryRequirementFields`: without the fix 45d lacked 7 item, 7 quest and 2 jutsu columns (auction/purchase limits, masteries, `coordinateTargeting`, `methodSize`) and `aiRule` entirely. (At bdec2883 those columns were inline, so counts there are unchanged) |
| `AvailableEffectTypes` assumed = all tags | at 6524d0f it excludes `elementaldamage` |
| 45c had no `_provenance` from the tool | now emitted (payload fingerprint as the 2026-08-30 file did by hand) |

**Independent cross-check:** at 6524d0f, 45c's per-variant key sets equal Forge `nested.json` for all four union families (effects, objectives, AI conditions, AI actions). 45d's entity field sets equal Forge `fields.json` for jutsu, item, bloodline, quest and gameAsset. The two derivations share no code.

## Part 3 — the gate and the ledger

`schema_diff.py` gaps fixed: keys removed from a union variant were not atoms; 45g and 45f had **no atoms at all** (both reported "0 additions, safe to adopt" whatever changed); a newly extracted field was reported as an optional→required flip. Added `--accept LEDGER`: exit 0 only for the exact OLD/NEW sha256 pair and an **identical** breaking set, with every entry under an evidenced class. A negative control (one entry removed) fails.

`scripts/schema_adoption_ledger.py` classifies every breaking atom and re-verifies each class against both pins, without using `schema_extract.py`:

| Class | Count | Verified by |
| --- | ---: | --- |
| upstream_field_removed | 31 | Forge `derive_fields`/`derive_nested` at bdec2883 vs 6524d0f (migration-0056 stat requirements; ten tags stopped spreading `IncludeStats`; `elementalseal.elements`) |
| upstream_const_member_removed | 50 | declaration text at both pins (e.g. `StatTypes` lost `Highest`, `UserStatuses.KAGE_QUEUED`, estate home types) |
| upstream_procedure_removed | 33 | router files at both pins (kage challenges, `train.stopTraining`→`stopMasteryTraining`, …) |
| consequence_of_removal | 352 | enum/nullable/required/null-strip entries of a field or member verified above (incl. `statClassification` losing `Highest`) |
| extractor_helper_overreach | 112 | the old field's own raw expression declares no enum |
| extractor_spread_precedence | 61 | the new 45c `power` for that tag has no max |
| extractor_spread_marker | 25 | the removed value is a literal `...Name` |
| extractor_ref_resolution | 2 | `aiRule.action` old raw is a bare schema name |
| extractor_nested_key | 1 | Forge derive at bdec2883 never had `dialog.text` |

Re-run: `python3 scripts/schema_adoption_ledger.py <bdec2883> <6524d0fb> <pre-adoption 45x dir> skills/building-tnr-content/data --check state/schema_adoption_ledger_6524d0fb.json` (pre-adoption files: `git show 383ac0f:skills/building-tnr-content/data/<file>`).

## Gates (exact, all exit 0 unless stated)

- Forge (`forge/`): `npm test` 642/642; fixtures + `git diff --exit-code` clean; `npm run build` reproducible; `check_bundle_budget` raw 410,676/420,000 (97.8%), gzip 98,610/100,000 (98.6%); `check_release_pin`, `check_boundaries`, `check_imports` clean.
- Skill: `schema_diff.py --invariants` 142 variants, 0 errors; `diff … --accept` for all five files; `schema_extract.py` reproduces all five adopted files byte-for-byte; `selfcheck.py --generated data` 0 errors (factory selftest 20/20; validate.py consumes 16/16 45g blocks); `schema_adoption_ledger.py --check` matches.
- Doctrine/packs: `doctrinemap.py .` 0/0; `render_doctrine.py --check` current; `build_packs.py --check` current; `lawmap.py .` 0 errors, 5 pre-existing warnings (16d, 18, 37, 61, 69).
- `validate.py --parity` not run (pre-existing TypeError on `checks:null`, unchanged).

## Known effects, debt and open decisions

1. **push/90/93/94 validate exceptions are voided by their own terms** (they pin the old contract hashes). Nothing new was found: every error/warning they still produce is one their rulings approved, and 42 + 8 + 3 + 2 approved push/90 diagnostics (stale effect fields, farm nullability, power cap, Highest→None) no longer occur. They are released history; no new ruling was written for them.
2. **Law reconciliation needed (not done here):** law 4 lists `(damage, pierce, wound)` and says `["Highest"]` is the default for both selectors. At 6524d0f `elementaldamage` is copied into a plain `damage` tag before combat (`libs/combat/elementalDamage.ts` `resolveElementalDamage`), so the rule applies to it too, and `statTypes` `Highest` is mapped to `None`. Law 6's flat power cap of 100 is a `BaseAttributes` bound that `PowerAttributes` overrides for 61 tags. `validate.py` still applies the law-6 text (entity level, unchanged), and its `LFORM`/45g `formula_tags` stay `damage/pierce/wound`.
3. `factory.py` self-test "power over cap" now uses `weakness` (a real constructor cap); the `damage` case tested the false bound.
4. The nightly sentinel (`regen_schemas.yml`) will report drift on its first run after merge, because the extractor's output changed. That is expected; it is signal only and never adopts.
5. 45d `doc` strings can include adjacent code text (pre-existing `split_entries` comment regex; cosmetic, unchanged).
6. Root `45c`/`45g` copies updated to equal skill `data/` (the old builder reads them from `main` after merge). The old builder applies the same enum/min/max checks as validate.py; it was not run.
7. `dist/` skill packs are rebuilt by the packaging workflow after merge; not rebuilt here.

## Not done

Browser/live preview, suggestion submission, PR #73 merge, Forge release, any law/doctrine text change, any push/131 manifest change. Before push/131 runs, re-capture Stormrender: the manifest replaces the whole `effects` array from the 06:35 UTC snapshot.
