# One Perfect Crop — launch-final scope

**Status:** ACTIVE implementation contract for `launch.finalization`  
**Director ruling date:** 2026-09-24  
**Repository work only:** yes  
**Live requests / writes authorized:** none

## Operative scope

This record preserves the director's 2026-09-24 launch-final scope. It supersedes older
One Perfect Crop launch-final assumptions only where they conflict with the decisions below.

### Art

- **2026-09-27 director clarification:** the earlier "battle AI art only" ruling applied to
  **new art production**, not to discarding scene-character art that had already been made and
  accepted. Launch-final must therefore use the existing accepted Ittetsu and Waystation Keeper
  scene assets.
- Launch-final art set:
  - Road Bandit AI avatar — repo-backed `one_perfect_crop_road_bandit_avatar.webp`.
  - Harvest Boar AI avatar — reuse the existing Wild Boar avatar; do not generate or upload a separate Harvest Boar image.
  - Ittetsu SCENE_CHARACTER — repo-backed `one_perfect_crop_ittetsu_scene.webp`, from the already-made accepted Ittetsu design.
  - Waystation Keeper SCENE_CHARACTER — repo-backed `one_perfect_crop_waystation_keeper_scene.webp`, from the already-made accepted Keeper design.
  - Market Clerk — reuse existing live gameAsset `XsLLy8awDAtaE6hXVIi_0`.
- **2026-09-26 director ruling:** reuse the existing Wild Boar avatar for Harvest Boar.
  The launch-final edit therefore sets Harvest Boar's avatar directly to
  `https://utfs.io/f/Hzww9EQvYURJmjlQbElHE4IMO5Goa7cgLxPJ0VC6lU8vbt1A`.
  This supersedes the earlier requirement for `one_perfect_crop_harvest_boar_avatar.webp`.
- Skip the Road Bandit scene character entirely; no Road Bandit SCENE_CHARACTER create or wiring.
- Do not add a Harvest Boar scene character.
- No additional scene-character generation is required; the accepted Ittetsu/Keeper assets are
  restored as launch-final inputs rather than regenerated.
- Do not generate or require Cabbage Seed art or a quest/listing icon for this launch.
- Reuse already-captured backgrounds only where the existing repository evidence requires final wiring.
- The previously reviewed 3-edit launch-final candidate at
  `70a82ad7891064ba9e4718ecca4d8cdd143fce58` is superseded by this clarification and must not be executed.

### Rewards and item creation

- No Cabbage Seed item creation.
- No Cabbage Seed item reward.
- No Ryo reward.
- No XP reward.
- No token or other standard-currency reward.
- No replacement reward package is to be designed or authored.

The surviving-seed ending prose may remain narrative flavor; it does not imply a mechanical item grant.

### Repeatability

- `maxAttempts: 100`
- `maxCompletes: 1`
- no cooldown
- leave optional `retryDelay` and `attemptDelay` fields unauthored / unset

### Eligibility

- Disregard the submitted Farming level 15 requirement.
- Author no substitute eligibility gate.

### Existing hidden core

The already-created hidden records are the launch-final edit targets:

| Record | Live hidden id |
|---|---|
| Road Bandit AI | `dKEz_VsgZjrfbtxt4ldo8` |
| Harvest Boar AI | `2-gJmijAA8lGns_thDRjz` |
| One Perfect Crop quest | `CZIZoHDAOWjxDtVaQwr6V` |

Do not rerun or recreate the hidden core. The launch-final manifest edits these three existing
hidden records and creates only the two missing hidden SCENE_CHARACTER gameAssets for Ittetsu and
the Waystation Keeper. Preserve the hidden-core graph, combat routing, AI records, and IDs except
for the explicitly approved launch-final deltas.

## Launch-final quest deltas

The quest edit must:

1. apply the queued G1/G4 prose revisions from
   `state/one_perfect_crop_launch_final_prose_patch.md`;
2. set the repeatability values above;
3. author no cooldown/delay fields and no eligibility gate;
4. preserve an empty mechanical reward package;
5. create/grant no Cabbage Seed;
6. wire the accepted Ittetsu/Waystation Keeper scene assets, existing Market Clerk, and existing
   non-generative background reuse according to the frozen prose graph;
7. keep the two new scene assets and the quest hidden; publish/unhide is a separate director-owned action.

## Safety boundary

Repository implementation, local/offline validation, and independent review are authorized.
Live requests, Forge execution, hidden execution, publish/unhide, and other live-game writes are
out of scope.
