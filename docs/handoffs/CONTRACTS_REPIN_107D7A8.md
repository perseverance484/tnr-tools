# Tooling re-pin to TheNinjaRPG@107d7a8: contracts, Forge 0.8.2, validator — 2026-10-22

**Lane:** A (code/tooling/generated contracts). **Ruling:** RUL-2026-10-22-005.
**Repository:** `perseverance484/tnr-tools`. **Branch:** `fable/contracts-107d7a8`.
**Base:** `main@68cd487`. **Head:** the commit that adds this file (reported with the push; frozen for review).
**Integration target:** `main`.
**Game source:** `studie-tech/TheNinjaRPG@107d7a86894f806a4c9cec89effef5992118a0ed` (origin/main, 2026-10-22).
Old pin: `85cecaebf4ada2e265a18a1405f63c9637443275`. Both checked out read-only (`git worktree`), never executed.
**Live requests / writes:** 0 / 0. **Credentials:** none.

## Objective

Bring the tooling up to the current game source: adopt the regenerated skill contracts (45c–45g) under a
reviewed ledger, re-pin Forge's derived contracts, and make `validate.py` enforce the new rules (level cap 110,
Elite Jonin milestone quests). `siphon` needed no validator code (tag shapes come from 45c).

## What changed upstream (85cecae → 107d7a8, as it affects the tooling)

- **`siphon` effect** (`SiphonTag = ConsumeTag.extend({ rounds min 1 })`, `validators/combat.ts`): in `AllTags`,
  `PotencyTagTypes`, `OBJECTIVE_TAG_TYPES`, `POST_DAMAGE_MODIFIER_TYPES`, `SHARED_COOLDOWN_TAGS`.
- **Level cap 110:** jutsu/item `requiredLevel` and quest `requiredLevel`/`maxLevel` are `.max(MAX_PLAYER_LEVEL)`
  (110; quest fields also `.int()`). `MAX_EXPERIENCE_LEVEL` = 100.
- **Milestone rewards:** `milestoneRewardFields` (`reward_level` 0 or 101–110, `reward_stats` 0–`MAX_STATS_CAP`) join
  every reward key set, plus a QuestValidator superRefine (`validators/objectives.ts` ~998–1043).
- **`insertAiSchema` moved** from `drizzle/schema.ts` to the new `validators/aiInput.ts` (commit 8d14dbe); contents
  unchanged.
- Four new procedures (`kageDefense.request/dismissInstantDefense`, `misc.refresh/verifyCaptcha`), new
  `PetArtProviders` members. `MAX_STATS_CAP` 1.5M, `MAX_GENS_CAP` 600k (Elite Jonin only).

## Changes

| Commit | Files | Behaviour |
|---|---|---|
| `05311a8` | `forge/tools/derive_fields.mjs`, `forge/tools/pin_relevance.mjs`, `scripts/schema_adoption_ledger.py`, skill `data/45c–45g`, `state/schema_adoption_ledger_107d7a8.json`, `docs/RULINGS.md` | derive_fields finds `insertAiSchema` in `drizzle/schema.ts` or `validators/aiInput.ts` (exactly one must declare it; both is refused); pin_relevance watches `aiInput.ts`; the ledger tool gains class `upstream_cap_raised` and an optional `--ruling`; contracts regenerated and adopted |
| `5a0a333` | `forge/src/runner/fields.json`, `nested.json`, `forge/tools/derive_nested.mjs`, `forge/build.mjs`, `forge/src/main.mjs`, `forge/package.json`, `forge_loader_user.js`, `forge_bundle.js`, two test files | Forge 0.8.2 at the new pin; loader keeps released `@version 0.8.1` + `@require` and adds `@x-release-pending 0.8.2` |
| `e134721` | `skills/building-tnr-content/scripts/validate.py`, `scripts/test_validate_107d7a8.py` | `check_bounds` (45d min/max/int on top-level numbers), law 8 caps read from 45d, `check_milestone` |
| `283fe2c` | `references/jutsu.md`, `packs/jutsu-build.md`, `_toc/jutsu.json` | `%jutsu` is never substituted; empty `battleDescription` is accepted (fallback), missing 400s |

### The ledger (`state/schema_adoption_ledger_107d7a8.json`)

Four breaking atoms, all 45g `cap_100` removals, class **`upstream_cap_raised`**:
`item.requiredLevel`, `jutsu.requiredLevel`, `quest.requiredLevel`, `quest.maxLevel`. Each is verified from the entity
validator's own field declaration at both pins (`field_expr`, independent of `schema_extract.py`): `.max(100)` at
85cecae, `.max(NAME)` at 107d7a8 with `NAME` declared as an integer literal > 100 (`MAX_PLAYER_LEVEL = 110`). The
fields stay capped; 45d now carries `max: 110` with `max_ref: MAX_PLAYER_LEVEL`. Everything else is additive.

### Forge contract delta

- `fields.json`: entity field sets unchanged for all six entities (jutsu, item, bloodline, quest, gameAsset, ai);
  only `pin` and the AI `source` (`app/src/validators/aiInput.ts:11`) change.
- `nested.json`: `siphon` (same keys as `consume`), `reward_level`/`reward_stats` in every reward key set; 84 validator
  files searched (was 81). Expanded surface: 86 → 87 effect types, 176 → 177 slots, 62 distinct sets (unchanged).
- Surface review (`pin_relevance.mjs`, 16 changed surfaces read): no router, limiter or procedure-kind change Forge
  relies on; no update path strips or rejects a field Forge writes. `trpc.ts` adds an `x-tnr-anonymous` header path
  Forge never sends. tRPC 11.18 → 11.19, zod 4.4 → 4.6; superjson 2.2.6 and uploadthing 7.7.4 unchanged.
  `globalNotFound` still set.

## Verification (exact commands, all from repo root unless noted)

**Reproduction before adoption**
- `schema_extract.py <85cecae> --ctors|--entities|--constants|--procedures|--checks` reproduces all five committed
  45x files exactly except the `"extracted"` date line.
- `node forge/tools/derive_fields.mjs <85cecae>` reproduces the committed `fields.json` (sorted-key compare).

**Skill contracts**
- `schema_diff.py diff <pre> <new> --accept state/schema_adoption_ledger_107d7a8.json`: exit 0 for all five (45c 98
  additions, 45d 0, 45e 8, 45f 12, 45g 4 breaking all accepted).
- `PYTHONHASHSEED={1,2,3} python3 scripts/schema_adoption_ledger.py <85cecae> <107d7a8> <pre> skills/building-tnr-content/data --check state/schema_adoption_ledger_107d7a8.json --ruling RUL-2026-10-22-005`: matches.
- `schema_diff.py --invariants data/45c_DATA_constructors.json --constants data/45e_DATA_constants.json` (cwd skill):
  143 variants, 0 errors (pre-adoption: 142, 0).
- `selfcheck.py --generated data` (cwd skill): 0 errors.
- `python3 -m unittest scripts/test_schema_diff.py`: 9/9.

**Validator**
- `python3 -m unittest scripts/test_validate_107d7a8.py`: 6/6.
- `validate.py` over every `push/*.json` (110 files, cwd skill `data/`): output byte-identical before and after both the
  contract adoption and the validator change (105 pass, 5 fail, the same five).

**Forge (`forge/`, after `npm ci`)**
- `npm test`: 618 pass, 14 fail. The 14 fail identically on `main@68cd487` (pre-existing, listed below).
- `npm run build`: `forge_bundle.js` 403.1 KB; a second build is byte-identical (sha256 check).
- `npm run fixtures`: exit 0, no diff.
- `check_bundle_budget`: raw 412,820/420,000 (98.3%), gzip 98,692/100,000 (98.7%).
- `check_boundaries`: 0 violations (generated-contract pin 107d7a8). `check_imports`: 0. `check_release_pin`: ok.
- `pin_relevance.mjs <85cecae> <107d7a8>`: exit 1 by design (16 surfaces changed); each was read (above).

**Doctrine / packs / laws**
- `build_packs.py --check`: current (after `--write`). `doctrinemap.py .`: 0/0. `render_doctrine.py --check`: current.
- `lawmap.py .`: 0 errors, 5 warnings (pre-existing, unchanged).

## Pre-existing Forge test failures (fail identically on main@68cd487)

offline package check (committed packages complete); validate.py --strict routes collections to the offline check;
old per-floor cash-outs via unreachable node; F4 reordering storage; F4 opening dialogue reachable; wrong art of
exactly the right size; wording check on carried prose; failed run supplying Marrow Vaults; deterministic render
refuses unmaterialised art; R2 observations coalesce; R3 rooted cycle through a failure link; ordinary sentence
opener not a stale name; `presentation.golden.test.mjs`; compatibility: staged manifests pass pre-send validation.
Mostly the presentation/collection-package suites. Not investigated in this pass.

## Known debt, deviations and open items

1. **Law reconciliation (not done, by ruling):** law 4 (stat-less formula damage is flat and level-scaled in current
   source, `libs/combat/tags.ts` damageCalc/powerEffect, not "trillions"), law 6 (the 100 power cap is per tag), and
   now **law 8** (`maxLevel` caps at 110, not 100). The validator follows the generated bound; the law text is stale.
2. **The 85cecae ledger's `--check`** would now differ by one line: the `classes` table lists every class, including
   the new `upstream_cap_raised` (count 0 there). Not re-run (needs a bdec2883 checkout).
3. **Bloodright contract** (`forge/tools/derive_bloodright.mjs`, own pin 94f9d84) is not re-derived. `PotencyTagTypes`
   now has `siphon` between `consume` and `shield`; re-deriving it will break `test/bloodright.test.mjs`
   (`CONTRACT.tags.slice(-7)`).
4. **Not modelled:** siphon/consume share one conversion budget and `SHIELD_MAX_HEALTH` (`registerShieldConversion`);
   no lint warns when both are authored. Dungeon drop types (`cache`, `package`, `quantity`) are outside the tooling's
   entities. New `check_bounds`/`check_milestone` are not in `check_ids()` (builder parity inventory).
5. `forge/package-lock.json` still says 0.7.0 (pre-existing).

## Not performed

No browser, live, session or game-execution checks. The game source was read, never run. No live manifest was run.

## Not begun

Law 4/6/8 reconciliation; Bloodright re-derivation; any milestone-quest or siphon content; the AoE `friendlyFire`
lint suggested in the 2026-10-22 analysis.
