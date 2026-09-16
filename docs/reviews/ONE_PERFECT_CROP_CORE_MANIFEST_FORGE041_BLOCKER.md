# One Perfect Crop core manifest — Forge 0.4.1 blocker

**Status:** BLOCKING — supersedes the earlier PASS for `af0efc6cb7657ea8bf95f6aae414ea2ff5391a2f` for production/Forge use.  
**Observed surface:** Forge 0.4.1 manifest selection, before job creation or mutation.  
**Prior reviewed SHA:** `af0efc6cb7657ea8bf95f6aae414ea2ff5391a2f`  
**Current main when source-checked:** `a45b576428d21bd7f24889a4965cf626d8dbf18a`  
**Reviewer:** ChatGPT / Engineering Auditor

## Behavior-proven failure

Selecting `push/47_one_perfect_crop_core_manifest.json` in Forge 0.4.1 was refused with:

`item 2: aiProfile cannot be created directly; create an ai with rules`

`item 3: aiProfile cannot be created directly; create an ai with rules`

Forge refused the manifest during parse/plan. No live mutation was issued by this attempt.

## Source confirmation

Current Forge is version 0.4.1 (`forge/package.json`). `forge/src/runner/manifest.mjs` explicitly treats `aiProfile` as a recognized manifest entity but rejects `op === "create"` for it with the exact observed message. `forge/src/runner/recipes.mjs` documents `aiProfile` as update-only.

The supported create path is an `ai` create whose `data` carries `rules` and `includeDefaultRules`. `forge/src/runner/runner.mjs` excludes those routing keys from `profile.updateAi`, then, after the AI fill succeeds, runs its rules phase for `ai` items that carry `data.rules`. That phase reads/toggles the AI profile as necessary and calls `ai.updateAiProfile`; read-back separately verifies the profile rules and `includeDefaultRules`.

## Root cause

The implementation and prior review relied on the retired `builder_bundle.js` manifest convention in which standalone `aiProfile` items were routable. That convention is incompatible with the current Forge 0.4.1 manifest contract. The repository manifest validator also failed to catch the mismatch, so its green result was insufficient evidence of Forge compatibility.

## Required correction

The corrected core manifest must contain exactly three create items:

1. Road Bandit `ai` create, preserving the existing AI record fields and exact three authored rules plus `includeDefaultRules: true` in the AI item's `data`.
2. Harvest Boar `ai` create, preserving the existing AI record fields and exact three authored rules plus `includeDefaultRules: true` in the AI item's `data`.
3. One Perfect Crop `quest` create, unchanged except for any deterministic regeneration caused by the corrected generator.

Remove both standalone `aiProfile` create items. Do not change the approved combat values, rule order, shared-jutsu ids, graph/prose, placeholder policy, rewards/admin deferral, hidden-first policy, or live-game boundary.

The generator assertions and local validation/tooling must be updated so this exact Forge 0.4.1 incompatibility is caught before handoff. The corrected candidate requires a new exact-SHA Fable handoff and a new independent review before user execution.

## Prior review status

`docs/reviews/ONE_PERFECT_CROP_CORE_MANIFEST_REVIEW.md` remains historical evidence of what was reviewed, but its PASS is superseded for execution by this behavior-proven blocker. A corrected candidate must not inherit that PASS.
