# One Perfect Crop partial-failure repair — Fable handoff

**Status:** READY FOR FABLE IMPLEMENTATION  
**Repository:** `perseverance484/tnr-tools`  
**Planning base:** `main@9630ad574a20c45f1b5f2124956fb2efc2f09b29`  
**Live policy:** ZERO LIVE REQUESTS / ZERO LIVE WRITES  
**Publish/unhide:** not authorized

## Incident

The user-run push/54 job is a confirmed partial failure. The durable diagnostic is:

`docs/reviews/ONE_PERFECT_CROP_LAUNCH_FINAL_PARTIAL_FAILURE.md`

Result bundle:

`harvests/inbox/tnr_results_1790603583693.json`

Do not rerun push/54.

## Split implementation

Fable must return **two independent frozen implementation SHAs**.

### A — minimal content repair

Contract:

`state/prompt_one_perfect_crop_launch_asset_repair.md`

Create a dedicated Fable branch. Produce only the two-asset in-place repair manifest/generator
and repository safety bookkeeping required to keep the spent push/54 out of the active picker.
No AI writes and no quest write. Full after-capture: both gameAssets plus the quest.

### B — validator hardening

Contract:

`state/prompt_asset_folder_regex_hardening.md`

Create a separate Fable Lane A branch. Close the Python + Forge offline gap for the
gameAsset.folder server regex. The invalid spaced folder must fail before transport; the valid
alphanumeric folder must pass.

Do not combine A and B into one implementation branch.

## Review/execution ordering

1. Fable freezes A and B independently and returns both exact SHAs.
2. ChatGPT independently reviews both.
3. The repair candidate is also run through the hardened validators offline.
4. Only after both reviews PASS may the director execute the two-asset repair while hidden.
5. Return the complete repair Forge result/full two-asset + quest after-captures.
6. Closeout review comes before any publish/unhide decision.

Repository access is not live-game authorization. Fable performs no live diagnostic, repair,
retry, publish, or unhide.
