# Fable implementation brief — gameAsset folder-regex validator hardening

**Status:** READY / FROZEN BRIEF  
**Lane:** A — validator/tooling hardening  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Base:** `main@9630ad574a20c45f1b5f2124956fb2efc2f09b29`  
**Live-game policy:** ZERO LIVE REQUESTS / ZERO LIVE WRITES  
**Incident:** `docs/reviews/ONE_PERFECT_CROP_LAUNCH_FINAL_PARTIAL_FAILURE.md`

## Objective

Close the offline-validation gap that allowed:

`gameAsset.folder = "One Perfect Crop"`

to pass both repository `validate.py` and Forge pre-send validation even though the server
validator rejects it with:

`/^[a-zA-Z0-9]*$/`

The fix must make the invalid value fail offline **before any mutation can be sent**, while
`"OnePerfectCrop"` passes.

## Required branch

Create a fresh Fable-owned Lane A branch from the verified base. Do not mix this tooling change
into the content-repair branch.

Suggested name:

`claude/gameasset-folder-regex-hardening-20260928`

Return an exact frozen SHA for independent review.

## Evidence/source contract

The generated repository schema already records the server rule at:

`skills/building-tnr-content/data/45d_DATA_entity_schemas.json`
→ `entities.gameAsset.fields.folder.raw`

as:

`z.string().regex(/^[a-zA-Z0-9]*$/, "Folder name can only contain letters and numbers").optional()`

Forge's current `fields.json` only carries top-level key membership from the pinned source and
therefore loses this constraint.

Do not invent a contradictory second policy. The enforcement should be derived from the
generated/pinned validator evidence already owned by the repository. If Forge needs additional
derived constraint metadata, extend its source derivation deterministically and pin/test that
output. If the implementation uses a targeted constraint adapter rather than a general regex
engine, it must still name its source/provenance and fail closed on drift.

## Python validator requirement

`skills/building-tnr-content/scripts/validate.py` must reject a manifest asset entry whose
asserted `folder` violates the generated gameAsset folder regex.

Required witnesses:

- `folder: "One Perfect Crop"` → error / nonzero exit;
- `folder: "OnePerfectCrop"` → accepted by this check;
- an asset edit without `folder` remains valid;
- unrelated entities/fields are unchanged.

Prefer consuming the generated entity schema rather than hardcoding the regex independently.

## Forge pre-send requirement

Forge's `Validator.problems("asset", ...)` / offline `check_manifest.mjs` path must reject the
same invalid folder value before transport.

Required witnesses:

- invalid folder appears in `check_manifest.mjs` pre-send problems;
- valid folder produces no folder-format problem;
- a runner test proves no `gameAsset.create` or `gameAsset.update` call is sent for a manifest
  rejected on folder format;
- existing key-surface and nested validation behavior remains unchanged.

The browser-side validation must derive from the pinned game validator contract, or from a
deterministic generated artifact derived from that pin. Do not silently make Forge depend on the
stale 45d field set for top-level membership where `fields.json` intentionally owns newer pinned
keys.

## Regression against the incident

Add an offline regression fixture/test shaped like the failed push/54 asset:

```json
{
  "entity": "asset",
  "slot": "edit",
  "targetId": "qFJk06nwwy0B9o2qZ1oZE",
  "data": {
    "name": "OnePerfectCrop Scene - Ittetsu",
    "type": "SCENE_CHARACTER",
    "image": "https://example.invalid/existing.webp",
    "folder": "One Perfect Crop",
    "frames": 1,
    "speed": 1,
    "hidden": true,
    "onInitialBattleField": false,
    "licenseDetails": "TNR"
  }
}
```

It must fail in both offline validators specifically because of `folder`, not because of an
unrelated fixture error. The corrected `OnePerfectCrop` twin must pass the folder check.

## Scope control

This is validator hardening, not a game-content rewrite.

Do not:

- alter push/54 historical result semantics;
- perform any live request/write;
- change the server source pin unless independently justified;
- broaden Forge to enforce arbitrary regex/raw-Zod text without tests and a deterministic source
  contract;
- refactor unrelated validator surfaces.

If implementation reveals other unenforced server regexes, report them as follow-up findings
rather than expanding this task without approval.

## Required gates

At minimum:

- focused Python validator tests;
- focused Forge Validator/check_manifest/runner tests;
- full Forge suite;
- any derivation reproducibility/drift test affected by new generated metadata;
- existing validator parity/selfcheck gates relevant to touched files;
- repository scrub;
- no live requests/writes.

Run the **new repair manifest** from
`state/prompt_one_perfect_crop_launch_asset_repair.md` through the hardened validators as an
offline acceptance fixture once that repair branch has a frozen candidate. This cross-branch
check may be performed in a temporary review checkout; do not merge implementation branches
together merely to run it.

## Handoff

Return:

- repository;
- hardening branch;
- base;
- frozen hardening SHA;
- changed files/generated artifacts;
- focused + full test counts;
- derivation/parity results;
- proof invalid `"One Perfect Crop"` is refused offline;
- proof valid `"OnePerfectCrop"` is accepted by the folder check;
- confirmation no live requests/writes;
- any follow-up regex gaps discovered but left out of scope.

Independent review is required before any further live repair write.
