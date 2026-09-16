# One Perfect Crop — hidden core-manifest implementation brief

**Task:** `build.manifest`  
**Implementation owner:** Fable / Claude Code  
**Design/freeze owner:** ChatGPT / Content Designer  
**Independent reviewer:** ChatGPT / Engineering Auditor  
**Live-game actor:** dauntless only  
**Baseline when frozen:** `main` at `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`  
**Status:** FROZEN for hidden core-manifest implementation

## Purpose

Build a validator-clean **hidden core manifest** for One Perfect Crop now. This is deliberately not the launch-final manifest.

The director has approved temporary create-path placeholders for missing art and has deferred rewards/item economics/repeatability/eligibility. Do not fill those gaps with guesses. Implement the complete frozen quest gameplay and combat records, keep every create hidden, and leave launch-final art/admin work for a later patch.

Governing override: `state/one_perfect_crop_core_manifest_override.md`.

## Authoritative inputs

Read and implement from these sources rather than from this brief when exact prose/schema values are needed:

- `state/one_perfect_crop_core_manifest_override.md`
- `state/plan_one_perfect_crop_finish.md`
- `state/one_perfect_crop_prose_graph.md`
- `state/one_perfect_crop_bandit_resolution.md`
- `state/one_perfect_crop_combat_spec.md`
- `state/one_perfect_crop_content_admin_open.md`
- `skills/building-tnr-content/references/pipeline.md`
- `skills/building-tnr-content/references/quest.md`
- `skills/building-tnr-content/references/ai.md`
- `skills/building-tnr-content/data/32b_DATA_pool.json`
- current generated constructors/entity schemas/checks and `skills/building-tnr-content/scripts/validate.py`

If any source conflicts, follow `docs/00_INDEX.md`. The 2026-09-16 override supersedes the older finish-plan requirement that art/admin must precede *any* manifest, but only for this hidden core build.

## Manifest contents

Create exactly the core entities needed for the frozen gameplay:

1. **Road Bandit AI**
2. **Road Bandit AiProfile**
3. **Harvest Boar AI**
4. **Harvest Boar AiProfile**
5. **One Perfect Crop quest**

No new jutsu are created. Use the exact existing shared-jutsu ids from `state/one_perfect_crop_combat_spec.md`.

Do not edit any shared live AI.

## Combat contract

Implement both AI records and both AiProfiles exactly from `state/one_perfect_crop_combat_spec.md`.

Preserve in particular:

- technical rank `JONIN`
- stored level `100`
- scale-to-user ON at each quest battle objective
- None element
- neutral/even twelve-stat ratio shape
- `statsMultiplier: 1`
- `poolsMultiplier: 1`
- `regeneration: 60`
- Strength / Speed preferred generals
- armor None
- Road Bandit `preferredStat: Bukijutsu`
- Harvest Boar `preferredStat: Taijutsu`
- no passive AI effects/tags
- `includeDefaultRules: true`
- exactly the three authored priority rules per profile, in the frozen order
- no bespoke fallback/movement/anti-exhaust rules beyond the engine-appended defaults

Use generated constructors for AI rule objects. Do not hand-author remembered shapes.

## Quest contract

Implement the exact frozen prose and graph from `state/one_perfect_crop_prose_graph.md`.

Preserve:

- `questType: event`
- zero-travel event shape
- PASS spine and F1-F4 sealed failure wings
- both fights as dialog-gated `start_battle`
- Road Bandit loss -> dedicated `fail_quest`
- Harvest Boar loss -> dedicated `fail_quest`
- no authored retry route
- exactly one starting objective
- all dialog forward edges as choice arrays
- all battle success/fail edges resolved
- delivery acceptance occurs before the final cabbage catastrophe
- final `MY CABBAGES!` beat remains in the frozen prose
- one enemy per battle
- `consecutiveObjectives: true` explicitly
- every created record `hidden: true`

Do not inherit stale generic-story guidance that would replace either `start_battle` with `defeat_opponents`.

## Temporary art policy for this core build

The director explicitly accepts the current create-path placeholder wherever final art is not supplied.

Therefore:

- create **no `asset` entries**
- include **no `@img:` references**
- do not require the accepted Ittetsu / Waystation Keeper / quest-icon bytes
- do not require Road Bandit scene art, Road Bandit avatar, Harvest Boar avatar, or Cabbage Seed icon
- do not fabricate replacement asset ids or image URLs
- do not make the unfinished scene-wiring task a prerequisite for this core build
- where the current builder/game create path can validly preserve its image/scene defaults, leave those defaults untouched

If a current schema/builder path proves that a supposedly deferrable art field cannot remain valid through create defaults, stop and report that specific field as a blocker. Do not synthesize art or bypass preflight.

## Temporary admin/reward policy for this core build

The following remain unresolved and are **not** to be chosen here:

- final Ryo reward
- final XP reward
- token/other reward currencies
- Cabbage Seed rarity
- Cabbage Seed functional item type
- Cabbage Seed economic/value fields
- repeatability/max-attempt/max-complete policy
- eligibility / submitted Farming level 15 requirement

Implementation consequence:

- create **no Cabbage Seed item**
- grant **no Cabbage Seed reward** in the core manifest
- do not author final Ryo/XP/token rewards
- do not translate Farming level 15 to character `requiredLevel: 15`
- do not invent a substitute profession gate
- do not choose final repeatability
- for unresolved quest-admin fields, preserve the current create-path defaults only as temporary hidden-state placeholders
- if validator completeness requires an explicit value, use the exact value produced by the current create/default contract, not a designer-chosen substitute, and document it in the handoff as a placeholder to be replaced before launch

Objective-level reward blocks that the canonical constructors require should remain mechanically zero/empty; they are not final event rewards.

## Manifest safety

- no live request
- no Forge/API execution
- no publish/unhide operation
- every create hidden
- no `skipPreflight`
- dedup/name resolution enabled
- no unresolved `@` refs
- no item or asset entries
- no new jutsu
- no shared-record edits
- use current factories/generated contracts rather than remembered payload shapes

Choose a collision-free descriptive filename under `push/`; do not overwrite an existing manifest.

## Required gates

Before handoff:

1. run the repository manifest validator on the produced manifest;
2. require **0 errors**;
3. run any applicable factory/constructor checks needed by the current content skill;
4. inspect the manifest to confirm:
   - only the two new AI records, two AiProfiles, and quest are created;
   - no asset/item/jutsu entries exist;
   - no `@img` refs exist;
   - all creates are hidden;
   - quest graph exactly matches the frozen graph;
   - both AI/profile contracts exactly match the combat spec;
   - no publish/unhide or live request path exists.

## Handoff

Implement on a Fable-owned branch and return:

- repository + branch
- exact base SHA
- exact frozen head SHA
- manifest path
- changed files
- validator command/result
- any other gates run
- explicit list of create-path placeholder fields left for later launch finalization
- confirmation that no live request was made
- confirmation that art/admin launch-final work has not been implemented

Freeze the handed-off SHA for independent ChatGPT review.

## Not launch-final

A PASS on this core manifest means it is safe to integrate to `main` as hidden repository content. It does **not** mean One Perfect Crop is ready to publish.

Launch finalization later supplies/reviews:

- final scene characters/background wiring/avatars/icons
- Cabbage Seed item
- final rewards
- repeatability
- eligibility
- any final art replacement of placeholders
- fresh hidden-state readback
- separate user publish/unhide decision
