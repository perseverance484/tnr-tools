# One Perfect Crop — launch-final scope

**Status:** ACTIVE implementation contract for `launch.finalization`  
**Director ruling date:** 2026-09-24  
**Repository work only:** yes  
**Live requests / writes authorized:** none

## Operative scope

This record preserves the director's 2026-09-24 launch-final scope. It supersedes older
One Perfect Crop launch-final assumptions only where they conflict with the decisions below.

### Art

- Launch-final accepted art is **battle AI art only**:
  - Road Bandit AI avatar — `one_perfect_crop_road_bandit_avatar.webp`
  - Harvest Boar AI avatar — `one_perfect_crop_harvest_boar_avatar.webp`
- Skip the Road Bandit scene character entirely.
- Scene-character work is nonblocking for launch finalization.
- Do not generate or require Cabbage Seed art.
- Do not restore older Ittetsu, Waystation Keeper, quest-icon, Road Bandit scene-character,
  or Cabbage Seed asset requirements as launch blockers.
- Reuse already-captured backgrounds/scene assets only where the existing repository evidence
  requires final wiring and no new art generation is needed.

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

Do not rerun or recreate the hidden core. The launch-final manifest is an EDIT/CLOSEOUT manifest
against these ids. Preserve the hidden-core graph, combat routing, AI records, and IDs except for
the explicitly approved launch-final deltas.

## Launch-final quest deltas

The quest edit must:

1. apply the queued G1/G4 prose revisions from
   `state/one_perfect_crop_launch_final_prose_patch.md`;
2. set the repeatability values above;
3. author no cooldown/delay fields and no eligibility gate;
4. preserve an empty mechanical reward package;
5. create/grant no Cabbage Seed;
6. wire only existing non-generative background/scene reuse that remains required by the
   frozen prose graph;
7. remain hidden; publish/unhide is a separate director-owned action.

## Safety boundary

Repository implementation, local/offline validation, and independent review are authorized.
Live requests, Forge execution, hidden execution, publish/unhide, and other live-game writes are
out of scope.
