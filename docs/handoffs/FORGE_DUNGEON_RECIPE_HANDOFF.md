# Forge dungeon recipe — implementation handoff (Lane A)

```text
Repository: perseverance484/tnr-tools
Branch: fable/forge-dungeon-recipe
Base: 991a58c80cae9737a447e61c2c615f5cd970078e
Head: aef88c3e3bb99c7dac465f5e35b5e13e20c253b3 (FROZEN until review returns)
Integration target: main @ 991a58c80cae9737a447e61c2c615f5cd970078e
Brief: state/prompt_forge_dungeon_recipe.md (RUL-2026-10-23-006); budget RUL-2026-10-23-007
Reviewer: ChatGPT (independent)
```

## Objective

Let Forge build, validate, journal and read back the game's `dungeon` definitions, so the Skyglass Wreck (docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md) can ship as a manifest instead of being built by hand in the editor.

## Changed

- `forge/tools/derive_dungeon.mjs` (new): derives `forge/src/dungeon/contract.json` from `studie-tech/theninjarpg@107d7a86`, refusing another HEAD or a dirty source file; `--check` compares bytes. Constants are evaluated arithmetically from `constants.ts`, and every pattern fails closed (including asserted presence of each refinement the validator mirrors).
- `forge/src/dungeon/contract.json` (generated) and `forge/src/dungeon/validate.mjs` (new): content, floor, wave, drop and reward key sets; floor-kind and first-wave refinements; bounds; direct-drop reward bounds; `hidden:true` on create; literal `structureAssetId` (it is a `mapAsset`, not a `gameAsset`); refusal of a sent `package` payload; `dungeonRow` projection.
- `forge/src/runner/recipes.mjs`: `dungeon` recipe (one-step create through `dungeon.save {content}`, id from the response's `id`, update `{id, content}`, get and names through `dungeon.getAll`); `recipeRows`, `updateInput` helpers.
- `forge/src/runner/runner.mjs`: `readCreatedId` for creates that return the id outside `message`; update input via the recipe; dedup rows via `recipeRows`.
- `forge/src/budget/reader.mjs`: `dungeon.getAll` as a no-input list; get-by-id projects the matching row.
- `forge/src/reconcile/reconciler.mjs`: list rows via `recipeRows`; a one-step create adopts the single new row only when it matches every asserted key, then goes to verify.
- `forge/src/runner/validate.mjs`, `manifest.mjs`, `transport/procedures.mjs`: dispatch, entity list, the two contract procedures; `MAX_DUNGEON_WRITES = 30`.
- `skills/building-tnr-content/scripts/validate.py` + `dungeon_bridge.py`, `forge/tools/validate_dungeon.mjs`: `validate.py --strict` routes dungeon entries to the same Node validator.
- Tests: `forge/test/dungeon.test.mjs` (22), `fakegame.mjs` dungeon routes, procedure-table invariants in `auth.test.mjs` / `transport.client.test.mjs`.
- Release staging: `forge/package.json` 0.9.0, `@x-release-pending 0.9.0` in `forge_loader_user.js`, rebuilt `forge_bundle.js`, budget 435,000 / 105,000 in `check_bundle_budget.mjs`, `dist/building-tnr-content.zip` rebuilt, `docs/BUILDER_APP_NOTES.md` section "Dungeon definitions (0.9.0)".

## Not begun / out of scope

Reward-package recipe; dungeon lobby/act/claim; re-pinning `fields.json`, `nested.json` or 45c–45g; release promotion (`pin_release.py`) after merge; the Skyglass Wreck content manifest (Lane B, after review).

## Verification (Node 24.22.1, full-history clone)

- `npm test` in `forge/` with `TNR_GAME_CHECKOUT` at the pin — 667 tests, 667 pass, 0 fail (base `581dae1` was 644/644). Without the checkout the one `--check` test is skipped.
- `node tools/derive_dungeon.mjs <checkout@107d7a86> --check` — "dungeon contract current".
- `npm run build` then `git diff --quiet -- forge_bundle.js` — committed bundle matches a fresh build.
- `node tools/check_bundle_budget.mjs` — raw 425,490 / 435,000 (97.8%), gzip 102,323 / 105,000 (97.5%); base was 412,173 / 98,680.
- `node forge/tools/check_release_pin.mjs` — exit 0.
- `check_manifest.mjs` and `validate.py --strict` on a fixture dungeon manifest — accept the valid one, refuse a broken one (inside `dungeon.test.mjs`).
- `doctrinemap.py` 0 errors / 0 warnings; `render_doctrine.py --check` exit 0; `build_packs.py --check` exit 0; `lawmap.py` 0 errors, 5 pre-existing warnings (16d, 18, 37, 61, 69).
- `pack_skills.py` — `dist/building-tnr-content.zip` sha256 `9f013af4…a8b2`, identical to the skillpack workflow's build.
- GitHub Actions on `aef88c3`: forge success, skillpack success, scrub success.

## Source / provenance

- Game source: `studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed`; per-file SHA-256s in `contract.json._meta.sources`. Read, never run.
- `dungeon.ts`, the router and `dungeonRewards.ts` are unchanged between the pin and upstream `a18f719d` (2026-10-23).
- Generated: `contract.json` (rebuilt by the tool), `forge_bundle.js` (rebuilt), skill zip (rebuilt). Nothing else regenerated.

## Risk / debt — attack these

1. **The composed limiter.** `dungeon.save` is the first mutation with `limited:true`; the invariant tests were changed to name it as the single exception. The budget still meters reads only; the 30-write manifest cap is the guard. Check that no code path treats `limited` as implying "query".
2. **Lost-create adoption.** One-step adoption trusts "exactly one new row since the snapshot, matching every asserted key". Bloodright requires operator binding in the same situation; this does not. Is the asymmetry justified for dungeons (no placeholder, name-dedup available)?
3. **Whole-content replace.** Every edit re-sends the full live content from `dungeon.getAll`. Server-side defaults returned by the read (for example `package` snapshots on drops) are re-sent; the server ignores `package` and re-copies it. A live definition that no longer parses at the pin would be re-sent as read.
4. **Dates.** `expiresAt` comes back as a Date and is re-sent as one; diff uses `eqLoose`, which compares instants.
5. **Bounds the client cannot check:** package contents in the reward bounds, existence of referenced rows, weighted-cache drops. Left to the server's save; reported as refusals.
6. `forge/package-lock.json` still says 0.7.0 (stale before this change; not touched).

## Live-game statement

Zero live requests, zero game writes, no credentials or session material. No browser or live-session checks were performed; `dungeon.getAll` behaviour for non-staff accounts and the real save response are taken from source, not observed.
