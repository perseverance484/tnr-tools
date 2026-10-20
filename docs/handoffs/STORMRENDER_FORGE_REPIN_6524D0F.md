# Contract refresh to TheNinjaRPG@85cecae: Forge re-pin + extractor fix + skill-data adoption — 2026-10-20

**Lane:** A (code/tooling/generated contracts). **Ruling:** RUL-2026-10-20-001 ("Do B ... one big pass and put it in for review").
**PR:** #76. **Branch:** `claude/stormrender-highest-scaling-yj2nef`. Merge-base `383ac0f`; `main@e13bc9f` (the drift-sentinel commit) is merged in. The new frozen head is reported with the push; this file is the handoff for it.
**Review round 1:** `chatgpt/review-pr76-integration-20261020@62b81061` (`docs/reviews/PR76_INDEPENDENT_INTEGRATION_REVIEW_20261020.md`), HOLD on F1 (P1) and F2 (P2). Both are corrected below. The review branch was not modified or merged.
**Game source:** `studie-tech/TheNinjaRPG@85cecaebf4ada2e265a18a1405f63c9637443275`, the commit `main`'s drift sentinel reported and the reviewer inspected; 41 commits after the first adoption pin `6524d0fb`. TNR main was 5 commits further (`19e2010`) at the time and is not adopted. Read only, never executed. (The file name keeps "6524D0F" because other documents link it.)
**Live requests / writes:** 0 / 0. **Credentials:** none. The push/131 manifest is unchanged.

## Outcome

| Gate | Before | After |
| --- | --- | --- |
| `node forge/tools/check_manifest.mjs push/131_…json` | 1 problem (`elementaldamage` unknown) | **0** |
| `validate.py push/131_…json` (cwd skill `data/`) | 3 errors | **0 errors, 0 warnings** |
| `validate.py` over all 86 `push/*.json` | 81 pass / 5 fail | **83 pass / 3 fail** (90/93/94, below) |
| `schema_diff.py diff OLD NEW` (OLD = `main`'s files) | — | exit 0 for all five with `--accept state/schema_adoption_ledger_85cecae.json` |

## Review corrections

**F1 (P1), `quest.publicLocations` lost on Forge quest edits.** Forge `fields.json`/`nested.json` and all skill contracts are re-derived at 85cecae.
- `quest.publicLocations` (`z.boolean().prefault(false)`) is now in the quest write set, so `mergeForUpdate` re-sends the live value.
- Every objective gains `structureAssetId`, `locationName`, `locationDescription` and `structureScale` (`mapLocationFields`, from the new `validators/mapLocation.ts`).
- `derive_nested.mjs` now searches every validator file, so a new module is found rather than failing. A name declared in more than one file is refused, not guessed.
- Regression tests (`forge/test/adversarial.test.mjs`):
  - `publicLocations: true` survives an unrelated edit, and an asserted `false` still wins;
  - all four location keys are accepted on objectives and a typo is refused.
- `pin_relevance.mjs` 6524d0f→85cecae: 7 surfaces changed. The two router diffs were read.
  - `quests.update` now refuses a missing structure asset (loudly) and writes `publicLocations` on its presentation-only path.
  - `jutsu.getAll` changed its `hideAi` filter.
  - Nothing else changes what Forge relies on.
- Item contract unchanged: it still equals the live Stormrender capture's columns.

**F2 (P2), type-only changes inside 45c union-variant fields were invisible.**
- `schema_diff.py` now emits `vfield-type` and `vfield-required` atoms. A union-variant field changing type, losing its type, or becoming required (no `optional`, no `default`) is breaking.
- The breaking-set computation is one shared function (`schema_diff.classify`), used by both the gate and the ledger tool, and is deterministic across `PYTHONHASHSEED`.
- New `scripts/test_schema_diff.py` (9 tests) covers:
  - the reviewer's `power: number → string` mutation failing without a ledger, and passing only with an exact-hash, evidenced, identical ledger;
  - the ledger refusing an unevidenced class, a stale entry, a missing entry or a different NEW file;
  - a dropped type, optional→required, an additive new required field, and 45g/45f removals.
  - The tests fail against the previous `schema_diff.py`.
- The stronger gate changed the breaking set. The ledger was regenerated (not waived) and is re-verified below. It surfaced:
  - 29 genuine upstream changes: every objective `task` lost its `.prefault()`, so it is now required;
  - 2 more extractor corrections.

**Non-blocking items:**
- The preliminary `docs/reviews/STORMRENDER_HIGHEST_SCALING_MANIFEST_GATE_20261020.md` now carries an amendment: the blocker is resolved, and the fresh-recapture instruction is kept.
- The manifest `_note` is unchanged; its "do not run until both offline gates pass" condition is now met.

## Forge 0.8.1

- `derive_nested.mjs`:
  - reads `Base.omit/pick/extend` (`ElementalDamageTag`);
  - ignores commented-out enum members (six quest tasks the server refuses had been accepted);
  - searches all validator files (`_meta.files` lists the core ones plus a `searched` count; listing all 87 would cost ~4 KB of bundle).
- At 6524d0f the old pin's `jutsu.update`/`quests.update` would null `requiredPetSpeciesId`/`petTaskMinutes`. The 85cecae contract carries both.
- Stormrender regression test: the captured row plus the push/131 edit through `mergeForUpdate` and pre-send validation.
- Version 0.8.1 with `@x-release-pending 0.8.1`; the loader keeps the released 0.8.0 pin.

## `schema_extract.py` blind spots (fixed)

Balanced, cross-file, last-wins object parsing. This covers:
- multi-line fields and `z\n .object({`;
- `...X.shape` and cross-file spreads;
- `Base.omit().extend()` derivations;
- block-bodied helpers (`msg`, `type`);
- zero values (`default/min/max: 0` were dropped as falsy);
- fields typed by a named schema (resolved, or emitted as opaque `{"type":"ref"}` instead of dropped);
- constant lists built with `[...Name]`, and lists with a commented-out member;
- the helper body read as a fixed 600-character window (the `WeaponTypes` enum on stat requirements);
- 45d entity spreads and `AiRule`;
- the `AvailableEffectTypes` filter;
- 45c `_provenance`.

At bdec2883 the fixed extractor removes nothing from the committed files. At 85cecae:
- 45c per-variant key sets equal Forge `nested.json` for all four union families;
- 45d entity fields equal Forge `fields.json` (jutsu, item, bloodline, quest, gameAsset);
- the two derivations share no code.

## The ledger (`state/schema_adoption_ledger_85cecae.json`, `main` → 85cecae)

`scripts/schema_adoption_ledger.py` re-verifies every breaking atom against both pins without `schema_extract.py`. It reads the pins from each checkout's `git rev-parse HEAD`. Any atom it cannot verify blocks adoption.

| Class | Count | Verified by |
| --- | ---: | --- |
| upstream_field_removed | 31 | Forge `derive_fields`/`derive_nested` at both pins |
| upstream_const_member_removed | 50 | declaration text at both pins |
| upstream_procedure_removed | 33 | router files at both pins |
| upstream_default_removed | 29 | the variant schema's own field declaration at both pins (`task: z.literal(x).prefault(x)` → `z.literal(x)`) |
| consequence_of_removal | 352 | belongs to a field or member verified above |
| extractor_helper_overreach | 112 | the old field's raw expression declares no enum |
| extractor_spread_precedence | 61 | the new 45c `power` for that tag has no max |
| extractor_spread_marker | 25 | the removed value is a literal `...Name` |
| extractor_nested_key | 2 | inner key of `z.array(z.object(...))`: `dialog.text`, and `nextObjectiveId` typed "string" |
| extractor_ref_resolution | 2 | `aiRule.action` old raw is a bare schema name |
| extractor_type_fragment | 1 | `consume.rounds` typed "coerce"; the declaration is `z.coerce.number()` at both pins |

The superseded `state/schema_adoption_ledger_6524d0fb.json` is removed. It described an intermediate step that never reached `main`.

To re-run (pre-adoption files from `git show 383ac0f:skills/building-tnr-content/data/<file>`):
```
python3 scripts/schema_adoption_ledger.py <bdec2883 checkout> <85cecae checkout> <pre-adoption dir> skills/building-tnr-content/data --check state/schema_adoption_ledger_85cecae.json
```

## Gates (exact, all exit 0 unless stated)

- **Forge (`forge/`):**
  - `npm test` 644/644; fixtures plus `git diff --exit-code` clean; `npm run build` reproducible.
  - `check_bundle_budget`: raw 412,173/420,000 (98.1%), gzip 98,680/100,000 (98.7%).
  - `check_release_pin`, `check_boundaries`, `check_imports` clean.
  - Stormrender `check_manifest` 0.
- **Skill:**
  - `schema_diff.py --invariants`: 142 variants, 0 errors.
  - `diff … --accept` passes for all five files.
  - `schema_extract.py` reproduces all five adopted files byte-for-byte.
  - `selfcheck.py --generated data`: 0 errors (factory 20/20; 16/16 45g blocks).
  - `schema_adoption_ledger.py --check` matches (PYTHONHASHSEED 1, 2, 3).
  - `python3 -m unittest scripts/test_schema_diff.py`: 9/9.
- **Doctrine/packs:** `doctrinemap.py .` 0/0; `render_doctrine.py --check` current; `build_packs.py --check` current; `lawmap.py .` 0 errors, 5 pre-existing warnings.
- **Not run:** `validate.py --parity`, because of a pre-existing TypeError on `checks:null` (unchanged).

## Known effects, debt and open decisions

1. **push/90/93/94 validate exceptions are voided by their own terms.** They pin the old contract hashes. Every error and warning they still produce is one their rulings approved; none are new.
2. **Law reconciliation needed (not done here):**
   - Law 4 lists `(damage, pierce, wound)` and gives `["Highest"]` as the default for both selectors. `elementaldamage` becomes plain `damage` before combat, and `statTypes` `Highest` is mapped to `None`.
   - Law 6's flat power cap of 100 is a `BaseAttributes` bound that `PowerAttributes` overrides for 61 tags.
   - `validate.py` still applies the law text as written.
3. `factory.py` self-test "power over cap" now uses `weakness`, a real constructor cap.
4. **The nightly sentinel will report drift on its first run after merge**, because the extractor's output changed and TNR main has moved past 85cecae. That is a signal only; it never adopts.
5. Root `45c`/`45g` copies equal skill `data/`. The old builder applies the same enum/min/max checks as validate.py; it was not run.
6. `dist/` skill packs are rebuilt by the packaging workflow.

## Not done

- No browser, live or session checks; no suggestion submitted; no PR merge or Forge release; no law or doctrine text changes.
- **Before push/131 runs, re-capture Stormrender:** the manifest replaces the whole `effects` array from the 06:35 UTC snapshot.
