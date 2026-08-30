# SOURCE_AUDIT 2026-08-30 - repo canon vs studie-tech/TheNinjaRPG@bdec2883

Method: full source clone at bdec2883 (2026-08-29), re-extraction with the repo toolchain,
structural diff against the stamped 45x generation, targeted source reads. 32 commits since
the 2026-08-26 drop the stamped files came from.

## Extractor regression found and closed

The stamped 45c carried 10 `_recovered` hand-patches, each documenting the same two gaps in
the repo's schema_extract.py: cross-module schema refs (`attackers: idsWithNumberField` from
validators/base.ts) and file-local const enums (objectives.ts's unexported SECTOR_TYPES).
The stamped file was generator output PLUS hand recovery; the repo tool alone could not
reproduce it.

This mattered more than hygiene: the map/tutorial work added a global `SECTOR_TYPES` to
drizzle/constants.ts that name-collides with the objectives-local one. A naive regen bound
the WRONG enum - location objectives would then fail every shape check against values like
"specific" and "random". The audit caught it pre-adoption; this is exactly why --ctors runs
first and diffs before trusting.

schema_extract.py upgraded (mounted 2026-08-30): derived cross-module refs (plain, chained,
and `.refine`-wrapped, with `min_items` folded from length refines), file-local const enums
with `@file`-qualified enum_ref and local-first resolution, and a POST_DOCS table so
law-cited semantics ride the generated shape (law 44/69's HEADCOUNT-vs-DROPCHANCE doc on
idsWithNumberField.number is now generated, not hand-patched). All 10 `_recovered` blocks
retire as true generator output, and the tool now also covers the duplicate
allObjectiveSchema union the hand pass missed.

## True drift adopted (45c / 45e / 45f regenerated @bdec2883; 45d / 45g zero drift)

- constants: + `AutoCombatBattleTypes`; `MAP_RESERVED_SECTORS` is now an expression
  (sector 227 tutorial reservation) so raw is carried without a folded value;
  `QuestTypes` + `overworld` - NPC_ONLY, so the builder's hardcoded qtype enum gap is a
  T3 item (config-driven enums), not urgent.
- procedures: + `combat.toggleAutoCombat`; `combat.startArenaBattle` input grew a param.
- guards on adoption: factory --selftest 20/20, validate.py 0 errors / 0 warnings on the
  staged wedge probe, --parity 16/16 against the live acceptance bundle.

## Wedge note for Terr (quest-edit crash)

`AllObjectives` discriminators are well-formed at HEAD - every member is
`z.literal("x").prefault("x")` - and nothing on the quest-edit path constructs a
discriminatedUnion from a dynamic list. The schema content as written cannot produce
"Duplicate discriminator value undefined". Suspects: duplicate zod instances across client
chunks (literal metadata lost at a module boundary) or an intermediate build since fixed.
Deploy-window candidates 08-27/28 are the map/tutorial cluster. Worth passing on: check the
client bundle for two zod copies.

## Standing rule, restated with source in the loop

Source extraction now replaces guess-and-check for CONTRACTS: schemas, bounds, enums,
constants' compile-time defaults, the tRPC surface. It does not repeal capture-first for
LIVE STATE - law 83 stands (generated DMG_* are defaults the gameSetting table may
override), a push echo is still not a read-back, and record contents still come from
captures. Extract for what the code IS; capture for what the database HAS.

Regen cadence: the blocked regen workflow (PAT needs Workflows RW) is now the mechanism
that keeps this audit from going stale - weekly extraction lands drift the week it ships.

## Addendum (same day) - law 40 walked

Continued past the report: `ai_v2.ts` distance conditions read `target.distance`, which is
`astar.getShortestPath(origin, hex).length` on the obstacle-costed grid. Both operators are
INCLUSIVE (`>=` / `<=`) - the unrecorded precision that makes registry range + 1 exact
rather than approximately safe. Obstacle rerouting can lengthen the path beyond true hex
distance, holding gates closed through intervening bodies/barriers. Law 40 stamped VERIFIED
@bdec2883; no tool change needed - L22 and check_distance_gates already derive R+1.
