# Forge content-contract re-pin to TheNinjaRPG@6524d0f (Stormrender unblock) — 2026-10-20

**Lane:** A (code/tooling). **Branch:** `claude/stormrender-highest-scaling-yj2nef`, built on PR #73 head
`590c0d8968d21aa53713276ef2faacf2fb42b84c` (merge-base `main@383ac0f`). The `chatgpt/*` branch was not modified.
**Live requests / writes:** 0 / 0. **Credentials:** none. **Game source:** read only, never executed.

## What changed

| File | Change |
| --- | --- |
| `forge/tools/derive_nested.mjs` | Reads `const X = Base.omit({..}).pick({..}).extend({..})` derivations (upstream `ElementalDamageTag = DamageTag.omit({ elements: true }).extend(...)`). Fail-closed: any other chained call, an omit/pick of a key the base lacks, or a derived union member that does not redeclare its own discriminator is a hard error. Default pin 6524d0f. |
| `forge/tools/derive_fields.mjs` | Default pin 6524d0f only. |
| `forge/src/runner/nested.json`, `fields.json` | Re-derived at 6524d0f by the tools above (not hand-edited). |
| `forge/test/*` | Pinned counts/digest moved with the contract; new regression test (below). |
| `forge/build.mjs`, `forge_bundle.js` | Banner pin; rebuilt. |
| `forge/package.json`, `forge/src/main.mjs`, `forge_loader_user.js` | 0.8.1, loader keeps released 0.8.0 pin with `@x-release-pending 0.8.1` (two-stage release). |

Scoped Bloodright contract (`forge/src/bloodright/contract.json`) and the review-desk contract (`2aed7e4`) are **unchanged**.

## Adoption evidence

- **Extractor fidelity:** with the patched tools, `derive_nested.mjs` and `derive_fields.mjs` at 94f9d84 reproduce the committed files **byte-for-byte**; at 6524d0f the default-pin output equals the adopted files byte-for-byte.
- **Structural diff (nested), purely additive:** new effect types `elementaldamage` (DamageTag keys minus `elements`) and `noncombatquest`; `reward_titles` on every objective and `objectiveReward`; `reward_pets`/`reward_titles` on `noncombatconsumereward`. No key or discriminator removed.
- **Structural diff (fields):** jutsu `+methodSize, +requiredPetSpeciesId`; item `+methodSize`; quest `+petTaskMinutes`; ai `+npcTitle` and pet/title columns, `-customTitle` (upstream rename `customTitle`→`npcTitle`, column renamed in `schema.ts`; Forge's review contract already used `npcTitle`).
- **Live corroboration:** the operator capture `tnr_results_1792478135730.json` Stormrender row's column set equals the 6524d0f item contract exactly (minus server-owned `id/createdAt/updatedAt`; `craftingRequirements` is relation-only, as before). At 94f9d84 the live `methodSize` column was outside the contract.
- **`pin_relevance.mjs`:** 16 declared surfaces changed; each was read (independent audit). Limiter, procedure paths/auth, `item.update` whole-record save, `/forge` host (`globalNotFound`, proxy catch-all) and the review-desk procedures are unchanged in what Forge relies on. No server transform rewrites `effects` in the item update path. Two findings make the re-pin **necessary**, not optional: at 6524d0f `jutsu.update` nulls `requiredPetSpeciesId` and `quests.update` nulls `petTaskMinutes` when the field is omitted, and the 94f9d84 contract omitted both. Non-Forge tooling note: `pin_relevance.mjs` does not watch the contentReview router/libs that suggest mode depends on (unchanged since 2aed7e4 here).

## Regression test

`forge/test/adversarial.test.mjs` — *re-pin 6524d0f: an item edit keeps an elementaldamage effect and adds statTypes None / generalTypes Highest*. Socket-free replay of the captured live Stormrender row through `mergeForUpdate` with push/131's data: pre-send validation passes on the edit and the merged payload; every contract column (incl. `methodSize`) survives; `effects[0]` differs from live only by `statTypes:["None"]` + `generalTypes:["Highest"]`; `effects[1]` unchanged; `elements` and a typo are still refused on `elementaldamage`; ordinary `damage` with `Highest` selectors still passes. The staged-manifest compatibility test now covers push/131 too.

## Gates (exact commands, all from `forge/`)

| Command | Result |
| --- | --- |
| `npm test` | 641 pass / 0 fail |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures/{envelope,screens}` | clean |
| `npm run build` + `git diff --exit-code -- ../forge_bundle.js` | reproducible |
| `node tools/check_bundle_budget.mjs` | raw 410,815 / 420,000 (97.8%); gzip 98,652 / 100,000 (98.7%) |
| `node tools/check_release_pin.mjs` / CI release-pin step | ok / clean |
| `node tools/check_boundaries.mjs`, `node tools/check_imports.mjs` | 0 violations each |
| `node tools/check_manifest.mjs ../push/131_stormrender_highest_scaling_suggestion.json` | **0 pre-send problems (exit 0)**; was 1 at 94f9d84 |

## NOT resolved: `validate.py` (skill 45c/45d/45e/45g) — needs a decision

`cd skills/building-tnr-content/data && python3 ../scripts/validate.py ../../../push/131_stormrender_highest_scaling_suggestion.json` → **exit 1, 3 errors**:
1. `effects[0]: 'elementaldamage' is not a member of AllTags` (45c at bdec2883 predates the tag);
2–3. `effects[1]: increasedamagetaken: unknown field 'direction'` / `'description'` (same stale-effect-field class RUL-2026-10-12-013 already evidenced).

Governed regeneration was attempted and **fails the D-adopt-gate**, so nothing was adopted:
- `schema_extract.py` at bdec2883 reproduces all five committed 45c/d/e/f/g bodies exactly (extractor is faithful at its recorded drop).
- At 6524d0f: `schema_diff.py --invariants` → 0 errors; `diff` → 45c **exit 1**, 45d **exit 1**, 45e **exit 1**, 45f/45g exit 0.
- The removals mix **genuine upstream changes** (migration-0056 per-type stats; `StatTypes.Highest`; `UserStatuses.KAGE_QUEUED`; estate home types; `customTitle`) with **extractor blind spots** (the `aiRule` entity disappears; a literal `"...BasicElementName"` spread is emitted as an enum member; `noncombatconsumereward` drops out of `AvailableEffectTypes`/`tag_power_max` although it still exists upstream).
- `schema_diff.py` does not parse the 45g format (it reported "0 additions" on a file with dozens of changes), so its 45g exit 0 is not evidence.

Options: (a) a push/131-specific validate exception under the RUL-2026-10-12-013 mechanism (3 diagnostics, 2 classes); (b) a separate Lane A task to fix the extractor blind spots and adopt 45c/d/e/g at 6524d0f with a ruling on the genuine removals. Either is dauntless's call; this handoff takes neither.

## Not done / not begun

Browser/live preview, suggestion submission, PR #73 merge, release (post-merge `release_pin.yml`), any skill `data/` regeneration, any change to the push/131 manifest. Before running push/131, the operator must re-capture Stormrender: the manifest replaces the whole `effects` array from the 06:35 UTC snapshot.
