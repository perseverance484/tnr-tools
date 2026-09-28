# Fable implementation brief — One Perfect Crop launch-final asset repair

**Status:** READY / FROZEN BRIEF  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Base:** `main@9630ad574a20c45f1b5f2124956fb2efc2f09b29`  
**Live-game policy:** ZERO LIVE REQUESTS / ZERO LIVE WRITES during implementation and review  
**Diagnostic source:** `docs/reviews/ONE_PERFECT_CROP_LAUNCH_FINAL_PARTIAL_FAILURE.md`

## Objective

Prepare the smallest safe repair for the two hidden gameAsset placeholder rows created by the
failed push/54 run. Repair them **in place**; do not create replacement assets, rerun push/54,
rewrite the AI records, or rewrite the quest unless new committed evidence proves the stored
scene ids are wrong.

## Required branch

Create a fresh Fable-owned implementation branch from the verified base. Do not implement on a
ChatGPT branch.

Suggested name:

`claude/opc-launch-final-asset-repair-20260928`

Return an exact frozen SHA for independent review.

## Inputs to verify before implementation

Read at minimum:

- `harvests/inbox/tnr_results_1790603583693.json`
- `push/54_one_perfect_crop_launch_final.json`
- `docs/reviews/ONE_PERFECT_CROP_LAUNCH_FINAL_PARTIAL_FAILURE.md`
- `docs/reviews/ONE_PERFECT_CROP_LAUNCH_FINAL_R2_REVIEW.md`
- `state/one_perfect_crop_launch_final_art.md`
- `state/workstreams/one_perfect_crop/roadmap.json`
- current entity schema / Forge manifest contracts for `asset` edits and full captures.

Fail closed if the bundle does not reproduce:

- manifest hash `0b942400`;
- Ittetsu placeholder id `qFJk06nwwy0B9o2qZ1oZE`;
- Keeper placeholder id `qiFtWf9G91kt4spFRA1VF`;
- Ittetsu uploaded URL
  `https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJqpGORkWdkOZgJQ8mGRcdx3SsWvPelyYFTt5V`;
- Keeper uploaded URL
  `https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJHM8ObaQvYURJhgs76VZtf9wxpMa13Cq0iOnr`.

## Deliverables

Create a new repair manifest and deterministic generator, using the next safe push number
available at implementation time. If `55` remains free, prefer:

- `push/55_one_perfect_crop_launch_final_asset_repair.json`
- `push/55_one_perfect_crop_launch_final_asset_repair.gen.py`

The manifest must contain **exactly two write items**, both `asset` / `edit`:

### Ittetsu

Target: `qFJk06nwwy0B9o2qZ1oZE`

Assert the intended record:

- `name: "OnePerfectCrop Scene - Ittetsu"`
- `type: "SCENE_CHARACTER"`
- `image: "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJqpGORkWdkOZgJQ8mGRcdx3SsWvPelyYFTt5V"`
- `folder: "OnePerfectCrop"`
- `frames: 1`
- `speed: 1`
- `hidden: true`
- `onInitialBattleField: false`
- `licenseDetails: "TNR"`

### Waystation Keeper

Target: `qiFtWf9G91kt4spFRA1VF`

Assert the intended record:

- `name: "OnePerfectCrop Scene - Waystation Keeper"`
- `type: "SCENE_CHARACTER"`
- `image: "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJHM8ObaQvYURJhgs76VZtf9wxpMa13Cq0iOnr"`
- `folder: "OnePerfectCrop"`
- `frames: 1`
- `speed: 1`
- `hidden: true`
- `onInitialBattleField: false`
- `licenseDetails: "TNR"`

Do not use `@img`; the exact intended image bytes were already uploaded by push/54 and their
URLs are persisted in the committed result bundle.

Do not create new `srcId` dependencies. The repair is target-id based.

## Capture contract

Full after-capture is mandatory for exactly:

1. `gameAsset.get` Ittetsu placeholder id;
2. `gameAsset.get` Keeper placeholder id;
3. `quests.get` One Perfect Crop quest id `CZIZoHDAOWjxDtVaQwr6V`.

Use `persist: "full"` on all three.

The quest is capture-only in this repair. There must be no quest item in the write list.

## Forbidden writes

The generator must assert absence of:

- AI write items;
- quest write items;
- create items of any entity;
- `@img` references / imagePack uploads;
- item/jutsu/bloodline writes;
- publish/unhide operations;
- any target other than the two placeholder gameAsset ids.

No live request is authorized during implementation or review.

## Spent-manifest safety

Push/54 is an executed write manifest and the diagnostic explicitly says **do not rerun it**.
Before integration, remove it from the active Forge picker surface by archiving the JSON under
the repository's normal spent-manifest convention, while preserving its exact bytes and result
provenance. Do not rewrite its historical content. If existing guard/tooling needs a find-through
archive path, preserve that behavior rather than weakening a guard.

This is repository safety bookkeeping, not a live action.

## Generator requirements

The generator must derive/verify its constants against the committed result bundle and historical
push/54 evidence rather than trusting chat text alone. At minimum it should fail closed on:

- wrong result-bundle manifest hash;
- wrong two placeholder ids;
- wrong already-uploaded URLs;
- wrong intended names/type/folder;
- any extra write item;
- any quest/AI write;
- any create;
- any image upload reference.

Provide `--check` generator exactness.

## Required gates

Run the normal manifest gates plus repair-specific assertions:

- generator `--check`;
- `validate.py`: zero errors;
- `node forge/tools/check_manifest.mjs`: zero pre-send problems;
- focused generator/manifest tests proving exactly two edits and three full captures;
- workstream validate/render checks for any roadmap change;
- repository scrub.

The repair must also be tested against the separately hardened folder-regex validators from
`state/prompt_asset_folder_regex_hardening.md` before it is eligible for live execution.
Do not perform the live repair from Fable.

## Workstream/state update

Record the push/54 partial failure and transition `launch.finalization` away from the obsolete
"waiting for initial hidden execution" state. The repaired task remains blocked/review-gated
until:

1. repair implementation is independently reviewed;
2. validator hardening is independently reviewed;
3. the director performs the repair run while hidden;
4. the returned two-asset + quest full readback passes closeout.

Publishing/unhide remains separate and user-owned.

## Handoff

Return:

- repository;
- repair branch;
- base;
- frozen repair SHA;
- repair manifest path + manifest hash;
- exact two target ids;
- tests/gates;
- confirmation of 0 live requests/writes;
- explicit statement that push/54 was not rerun;
- any deviation from this brief.

Do not bundle the separate validator implementation into this repair branch.
