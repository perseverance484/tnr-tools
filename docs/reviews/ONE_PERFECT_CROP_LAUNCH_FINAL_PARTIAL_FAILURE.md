# One Perfect Crop launch-final — hidden-run partial failure diagnosis

**Status:** CONFIRMED PARTIAL FAILURE / DO NOT RERUN PUSH/54  
**Observed main:** `9630ad574a20c45f1b5f2124956fb2efc2f09b29`  
**Result bundle:** `harvests/inbox/tnr_results_1790603583693.json`  
**Executed manifest:** `push/54_one_perfect_crop_launch_final.json`  
**Manifest hash:** `0b942400`  
**Forge:** 0.5.0  
**Live requests / writes by this diagnostic:** 0 / 0

## What succeeded

The result bundle records VERIFIED/match for:

- Road Bandit AI avatar edit — `dKEz_VsgZjrfbtxt4ldo8`
- Harvest Boar AI avatar edit — `2-gJmijAA8lGns_thDRjz`
- One Perfect Crop quest closeout edit — `CZIZoHDAOWjxDtVaQwr6V`

The quest readback is structurally the reviewed graph/admin/prose payload.

## What failed

Forge created two hidden gameAsset placeholders, then their update phase was rejected:

- Ittetsu — `qFJk06nwwy0B9o2qZ1oZE`
- Waystation Keeper — `qiFtWf9G91kt4spFRA1VF`

Both failures are server validation failures on `data.folder`:

```text
/^[a-zA-Z0-9]*$/
Folder name can only contain letters and numbers
```

The reviewed manifest authored `folder: "One Perfect Crop"`; the valid repair value is
`folder: "OnePerfectCrop"`.

## Quest consequence

The quest update resolved and stored the two newly-created placeholder ids before the asset
update phases failed. The live quest therefore references:

- Ittetsu placeholder `qFJk06nwwy0B9o2qZ1oZE` in 22 dialogs
- Keeper placeholder `qiFtWf9G91kt4spFRA1VF` in 3 dialogs

The quest is structurally VERIFIED but presentation-incomplete until those two exact placeholder
rows are repaired in place. A quest rewrite is not needed if the asset ids remain the same.

## Exact uploaded image URLs

The run's persisted idmap records the already-uploaded exact files:

- Ittetsu:
  `https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJqpGORkWdkOZgJQ8mGRcdx3SsWvPelyYFTt5V`
- Waystation Keeper:
  `https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJHM8ObaQvYURJhgs76VZtf9wxpMa13Cq0iOnr`

The repair must reuse these URLs directly. Do not upload the images again.

## Repair contract

Repair exactly the two existing placeholder ids in place as SCENE_CHARACTER assets.

Intended assertions for each asset:

- original intended name from push/54;
- `type: "SCENE_CHARACTER"`;
- exact existing uploaded image URL from this result bundle;
- `folder: "OnePerfectCrop"`;
- `frames: 1`;
- `speed: 1`;
- `hidden: true`;
- `onInitialBattleField: false`;
- `licenseDetails: "TNR"`.

No AI writes. No quest write unless new repository evidence proves the stored ids are no longer
the intended ids. Full after-capture must include both `gameAsset.get` records and the quest.

Do not rerun push/54.

## Tooling defect

The generated `45d_DATA_entity_schemas.json` already preserves the server's folder regex in
`gameAsset.fields.folder.raw`, but the repository Python validator and Forge's pre-send
validator currently validate field presence/key surfaces without enforcing this regex. That gap
allowed push/54 to pass offline gates and fail only after a placeholder had been created.

Validator hardening is a separate Lane A change. It must make an invalid asset folder such as
`"One Perfect Crop"` fail offline before any mutation, while `"OnePerfectCrop"` passes.
The implementation should derive/reuse the generated or pinned validator contract rather than
introducing an unrelated hand-maintained regex if avoidable.
