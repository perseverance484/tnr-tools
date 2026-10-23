# Brief — Forge dungeon recipe (Lane A)

**Status:** APPROVED FOR IMPLEMENTATION (RUL-2026-10-23-006). This brief is the build contract.
**Date:** 2026-10-23
**Owner:** Fable / Claude Code, on `fable/forge-dungeon-recipe`. Independent review: ChatGPT, against a frozen SHA (`docs/DEVELOPMENT_WORKFLOW.md`, `docs/workflows/IMPLEMENTATION_HANDOFF.md`).
**Repository base:** `perseverance484/tnr-tools@a69e52b5b9046a469f00278e0ff131c8c33348df`
**Game source pin:** `studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed` (2026-10-22). Read the source; do not run it.
**Serves:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` (the Skyglass Wreck dungeon).

## 1. Problem

The game now has a staff-authored `dungeon` entity (`app/src/validators/dungeon.ts`, `app/src/server/api/routers/dungeon.ts`). Forge knows nine entities and no dungeon; the generated contracts (45c–45g, `fields.json`, `nested.json`) carry dungeon constants and procedure names only, no content schema. Without a recipe the dungeon can only be built by hand in the in-game editor, with no manifest, no validation, no journal and no read-back.

## 2. Source facts at the pin (verify again before relying on them)

- `dungeon.save` is `protectedProcedure.use(ratelimitMiddleware)`, input `saveDungeonSchema = {id?: string, content: dungeonContentSchema}`. Omitting `id` creates (`nanoid()`); with `id` it upserts the whole `content`. It returns `{success: true, message: "Dungeon saved.", id}` — the id is in `id`, not in `message`. Refusals are `errorResponse(...)` (success:false): role, missing entrance asset, missing AI or reward, cache drop that is not a weighted cache, reward bounds.
- Save copies each `package` drop's catalog snapshot server-side; a client-sent `package` payload is ignored.
- `dungeon.getAll` is a protected query returning every definition row `{id, content, updatedAt}` for content staff, `[]` otherwise. There is no per-id get.
- `dungeonContentSchema`: `name` (trim, 1–100), `description` (≤2000, default ""), `structureAssetId`, `structureScale` (`mapLocationFields`), `sector` (int, `MAP_SECTOR_ID_MIN`–`MAP_SECTOR_ID_MAX`), `longitude` (int, 0–`SECTOR_WIDTH-1`), `latitude` (int, 0–`SECTOR_HEIGHT-1`), `expiresAt` (coerced date, nullable), `hidden` (default true), `background` (`COMBAT_BIOMES`, default "default"), `tiers` (1–`DUNGEON_MAX_TIERS` tiers of exactly `DUNGEON_FLOORS_PER_TIER` floors), `rewards {money, experience, tokens, prestige, drops}`.
- Floor: `kind` ∈ floor / mini-boss / boss; `waves` 1–`DUNGEON_MAX_WAVES`, each `{aiIds (1–DUNGEON_MAX_MOBS), delayRounds (0–ENCOUNTER_MAX_WAVE_DELAY_ROUNDS, default 0)}`. Refinement: the last floor of the last tier is `boss`, the last floor of every other tier is `mini-boss`, the rest are `floor`; every floor's first wave has `delayRounds` 0.
- Drop: `type` ∈ item / jutsu / cache / package, `id`, `chance` 1–100, `quantity` int 1–`DUNGEON_MAX_REWARD_QUANTITY` (default 1), jutsu quantity must be 1; at most `DUNGEON_MAX_DROPS`.
- Reward bounds (`libs/dungeonRewards.ts` `dungeonRewardError`): scalar totals ≤ `DUNGEON_MAX_REWARD_AMOUNT`; worst-case granted items ≤ `DUNGEON_MAX_GRANTED_ITEMS` per member.

## 3. Scope

1. **Scoped contract.** `forge/tools/derive_dungeon.mjs` derives `forge/src/dungeon/contract.json` from a checkout at the exact pin, refusing any other HEAD or a dirty source file, with `--check` comparing bytes. Mirror `tools/derive_bloodright.mjs`. It records: the two procedures with `kind`, `auth`, `mcp`, and `limited` true when the procedure is public **or composes `ratelimitMiddleware`**; the content, floor, wave and drop key sets; enums (floor kinds, drop types, `COMBAT_BIOMES`); every numeric bound above and the map bounds; source file SHA-256s. It does not refresh any other contract.
2. **Validator.** `forge/src/dungeon/validate.mjs`, pure and socket-free: unknown keys at every level, types and bounds, the tier/floor-kind and first-wave refinements, jutsu quantity, worst-case reward bounds (direct drops only; package snapshots are server-side and are reported as "checked at save"), refs left as refs. A **create must carry `hidden: true`** (law 16b). Hook it into `Validator.problems` / `knownFields` the way Bloodright is.
3. **Recipe and runner.** A `dungeon` entity: one-step create through `dungeon.save {content}` taking the id from the response's `id` field; update through `dungeon.save {id, content}` with content = live content ∪ asserted top-level keys; get and names through `dungeon.getAll`, projected to the matching row's `content` (generalising the existing `skillTree.getAllFolders` list-get); verify diffs asserted keys against that content. Add the two paths to `PROCEDURES` from the contract; add `dungeon` to `ENTITIES`. Suggest mode must refuse it (the review desk has no dungeon entity type).
4. **Refs.** `@ai:` in wave `aiIds`, `@item:` / `@jutsu:` in drop ids, `@asset:` in `structureAssetId` resolve through the existing ref machinery and order the plan.
5. **Repository validator.** `validate.py --strict` accepts dungeon entries through a bridge to the Node validator (`bloodright_bridge.py` pattern, `forge/tools/validate_dungeon.mjs`), never through 45d.
6. **Tests.** Contract `--check`; validator accept/refuse cases for every rule above; runner create → verify, update (merge) → verify, resume after a lost create response, dedupNames through `getAll`, refusal paths, suggest-mode refusal, fake-game support; `check_manifest.mjs` on a fixture manifest.
7. **Budget.** Measure with `tools/check_bundle_budget.mjs`. Raise the ratchet only with the measurement and reason recorded in that file.

## 4. Out of scope

Reward-package recipe (`rewardPackages.*`; follow-up, same pattern); lobby/run/claim procedures; re-pinning `fields.json`, `nested.json` or 45c–45g; any engine change; any live request; the Skyglass Wreck content manifest itself (Lane B, after review).

## 5. Gates

`npm test` and `npm run build` in `forge/`; `node tools/derive_dungeon.mjs <checkout> --check`; `node tools/check_bundle_budget.mjs`; `node forge/tools/check_manifest.mjs` and `validate.py --strict` on the fixture manifest; `doctrinemap.py` and `render_doctrine.py --check` if skills or doctrine text change. No gate is piped in a way that hides its exit code.

## 6. Handoff

Per `docs/workflows/IMPLEMENTATION_HANDOFF.md`: exact base and head SHAs, changed files, gate commands and results, source pin, known debt, live checks not performed (all), and what has not begun. Freeze the SHA until review returns.
