# PR #76 — independent integration review (2026-10-20)

**Lead:** Engineering Auditor; supporting lens: Release Auditor  
**Verdict:** **HOLD / REQUEST CORRECTION before integration to `main`**. Do not merge the review branch as an implementation branch.

| Field | Verified target |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| PR | [#76](https://github.com/perseverance484/tnr-tools/pull/76) |
| Implementation branch | `claude/stormrender-highest-scaling-yj2nef` |
| Frozen implementation head | `564531ff83b95f719c1c3c5ec1d4b3bf2b09de92` |
| Review-time `main` | `e13bc9fa085b37bd84ab7736256da8d1ad2a4a99` (automated upstream-drift sentinel) |
| Merge-base | `383ac0f45bc47004a4a8915f4c724c79b35798f3` |
| Adopted TNR pin | `studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb` |
| Later TNR source inspected | `85cecaebf4ada2e265a18a1405f63c9637443275` (41 commits after the pin; already reported by `main`'s sentinel); TNR main was `19e2010f9cd3f9be26fff96cca0bf6dece322f11` (46 ahead) |
| Reviewer safety | GitHub-source reads only; **0 live-game requests, 0 writes, no credentials** |

## F1 — P1 source/contract mismatch: a Forge quest edit can turn off public map locations

**Confirmed implementation behaviour against source after the adopted pin. Deployment of that later source to the production game was not tested. This is a merge/release blocker because the failure is a silent content change if/when the newer server code is deployed.**

- At TNR `85cecae`, `app/drizzle/schema.ts` adds `quest.publicLocations`, and `app/src/validators/objectives.ts` adds `publicLocations: z.boolean().prefault(false)` to `QuestValidatorRawSchema`. It also spreads `mapLocationFields` into `baseObjectiveFields` from the new `app/src/validators/mapLocation.ts`.
- At the frozen PR head, `forge/src/runner/fields.json` is still pinned to `6524d0f`. Its 37 quest write fields **do not contain `publicLocations`**. `skills/building-tnr-content/data/45d_DATA_entity_schemas.json` has the same omission.
- In `forge/src/runner/recipes.mjs:76-83`, `mergeForUpdate` copies live + asserted data *only for known fields*. In `forge/src/runner/validate.mjs:120-134`, the known-field set comes from that pinned file. Reconstructing the exact filter with `live.publicLocations = true` and an unrelated quest name edit produces **no `publicLocations` key** in the outgoing payload.
- At TNR `85cecae`, `app/src/server/api/routers/quests.ts:846-853` parses update data through `QuestValidator`. Its normal update path sets `{...input.data, updatedAt}` (`~1046-1049`), and its presentation-only update explicitly writes `quest.publicLocations = input.data.publicLocations` (`~1030-1044`). The missing boolean is defaulted to **false**. Thus a subsequent ordinary Forge edit of a quest with public locations enabled can disable them without the operator requesting it.
- The same drift makes new objective fields (`structureAssetId`, `locationName`, `locationDescription`, `structureScale`) unknown to the pinned Forge nested validator. `forge/tools/derive_nested.mjs:26-41` does not read new `mapLocation.ts`; an updated extraction must handle that source import/spread rather than silently omit the keys.

**Correction:** Fable should incorporate the newer source contracts (at least the commit introducing these fields, preferably the currently confirmed source pin), update both Forge derivations and skill contracts through the existing audited adoption/ledger procedure, and add a socket-free fetch-merge regression: `publicLocations:true` on a fetched live quest must remain true through an unrelated edit; all four authorized location/objective fields must be recognized. Pin the exact source SHA and re-run the full Forge + skill/schema gates. Do not assume game deployment from GitHub; no production experiment is required for this correction.

## F2 — P2 confirmed adoption-gate blind spot: variant field type changes are not breaking atoms

`skills/building-tnr-content/scripts/schema_diff.py:73-105` emits `("variant-field", union.variant, field)` for 45c union keys and `enum-member` atoms for inline enum values, **but no type/requiredness atoms for union variant fields**. `ftype` atoms exist only for 45d entity fields. `BREAK_ON_REMOVE` and `--accept` therefore never see a type-only change in a tag's existing field; `--invariants` checks discriminators and enum resolution, not this type.

**Counterexample from the code's atom walk:** Change `unions.AllTags.damage.fields.power.type` from `"number"` to `"string"` without changing the field name or enum. The 45c atom sets remain identical, so `schema_diff.py diff OLD NEW` reports zero breaking changes and needs no ledger. This contradicts the tool's declared type-change fail-closed guarantee and `docs/DOCTRINE.md` D-adopt-gate. This gap predates the PR's extension to `variant-field` atoms; it becomes material in a broad extractor/gate adoption.

**Correction:** Add union-variant field type and optional-to-required transition atoms, fail closed on removals/type flips, and test a synthetic 45c type mutation both without and with an exact-hash, evidenced acceptance ledger. If this alters the current ledger's breaking set, regenerate and independently verify it rather than adding a waiver. This is a gate-hardening request, not a claim that the current adopted source actually contains an unreviewed type flip.

## What held up

- The Stormrender correction remains one `mode:"suggest"` item with `effects[0].statTypes:["None"]`, `generalTypes:["Highest"]`, unchanged second effect, and no new balance number. At adopted TNR pin `ElementalDamageTag` is derived from `DamageTag`, and the `statTypes` validator normalizes authored `Highest` to `None`.
- Forge's derived `nested.json` now includes `elementaldamage`; the PR's socket-free capture-based regression asserts preservation of the other Stormrender fields through `mergeForUpdate` and pre-send validation.
- PR-head [Forge GitHub Actions run 39457047439](https://github.com/perseverance484/tnr-tools/actions/runs/39457047439) is **green**: tests, bundle reproducibility, release-pin/boundary/import/size gates passed. Forge 0.8.1 is correctly staged behind loader `@version 0.8.0` with `@x-release-pending 0.8.1`.
- `45c` and `45g` root copies have the same Git blob IDs as their skill-data counterparts in the PR file listing.
- The author's handoff reports `validate.py` and `check_manifest.mjs` zero errors for push/131, `npm test` 642/642, and all five `schema_diff --accept`/schema-ledger/selfcheck gates. **Those Python gates were not independently executed by this reviewer**; the checkout was available by GitHub connector rather than a runnable local clone.

## Non-blocking tracked discrepancies / cautions

- `docs/reviews/STORMRENDER_HIGHEST_SCALING_MANIFEST_GATE_20261020.md` and the manifest's `_note` still say the old Forge pin blocks `elementaldamage`, even though the replacement branch clears that particular gate. Mark the preliminary report superseded or amended with the new result; do not remove the important **fresh Stormrender recapture before execution** instruction.
- Law 4's formula-tag set excludes `elementaldamage` although runtime resolves it to `damage`. Law 6's universal 100-power claim and `validate.py`'s explicit 100 check conflict with `PowerAttributes` overrides in the inspected source. The handoff already flags these as separate law-reconciliation work; they are **not** silently accepted as correct by this review.
- PR's 1-commit main divergence is the automated drift-sentinel update, not an implementation conflict. Re-check and synchronize `main` after corrections. Keep push/131 in operator-controlled draft/suggestion workflow; merging code does not approve a live run or publication.

## Evidence and verification boundaries

Review method: read exact GitHub files/patches and frozen generated contracts; compare the adopted pin with newer upstream commits; trace the fetch-merge, validator, and quest-update source paths; reconstruct a minimal known-fields-filter input/output; inspect official CI status. No local npm/python tests, no browser test, no game-source execution, no live game fetch/mutation. Reviewed SHA remained unchanged when checked after inspection.

**Next:** Fable owns corrections on its branch and returns a new frozen head SHA; independent re-review checks F1/F2 and related generated contracts, regression tests, source pin, and 0-error required gates. Neither this review report branch nor the unreviewed future branch head is a merge recommendation.
