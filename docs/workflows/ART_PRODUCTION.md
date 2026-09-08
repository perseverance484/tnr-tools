# Workflow — TNR Art Production

Use when ChatGPT is helping the user direct, generate, edit, process, review, or hand off a TNR visual asset.

This workflow coordinates ChatGPT's Art Director / Image Production roles with the repository's existing `skills/producing-tnr-art/` production authority. It does not duplicate the art spec.

## 1. Establish the target

Identify:

- asset type / client field;
- content/quest/scene/entity that needs it;
- current backlog/production status where relevant;
- required filename / `@img` contract if already established;
- whether the request is exploratory direction or production work.

Read `skills/producing-tnr-art/SKILL.md` and the exact current spec/reference files routed for that target.

## 2. Direction gate

Before spending production effort, settle enough visual direction to generate one meaningful candidate:

- subject and role;
- framing/composition;
- silhouette/readability needs;
- setting/background constraints;
- mood/lighting/material cues;
- prohibited elements;
- how the client will actually display the asset.

The user owns art direction and final acceptance. If multiple materially different directions remain viable, show the choice rather than silently deciding through generation.

## 3. Generate one asset

Generate one candidate at a time unless the user explicitly approves batching.

Follow the current prompt scaffold/house-style guidance and target restrictions.

Raw generation must avoid:

- text or labels;
- watermarks;
- UI/panels/borders/grids;
- prohibited franchise insignia/references;
- copied proprietary material;
- target-incompatible backgrounds/surfaces;
- composition that relies on processing to fix a fundamental generation error.

Treat ChatGPT-generated imagery as raw source art until the repository's production checks pass.

## 4. Raw QC

Before processing:

- run the current raw-QC mechanism required by the art skill where tooling is available;
- visually inspect composition and target suitability;
- reject wrong mode/aspect, prohibited elements, unusable key/background, painted glow blocks, inseparable surfaces, or other failures the skill marks as regeneration cases.

Do not spend processing effort trying to salvage an unprocessable generation.

## 5. Process through the repository pipeline

Use the bundled/current scripts and spec-driven target rather than rebuilding crop/key/pad/export logic by hand.

The current skill owns the exact commands, target names, numerical constraints, format rules, key behaviour, and special cases.

Always produce the target-appropriate visual QC composite required by the skill and actually inspect it.

## 6. Production preflight

Before handoff:

- run the current art preflight gate;
- verify filename / extension / dimensions / byte constraints from the current spec;
- verify the file matches the required `@img` filename exactly;
- use a fresh filename/version for a corrected asset when the repository contract requires it;
- record production metadata in the existing ledger/state mechanism when required.

A visually approved image that fails production preflight is not ready.

## 7. User acceptance

Present the processed/QC'd candidate to the user for final acceptance.

Separate:

- visual approval;
- mechanical production validity;
- in-game wiring/publishing status.

Do not call an asset "live" merely because the image file is finished.

## 8. Repository handoff

When a Fable/content task needs the asset:

- provide exact filename;
- target/type;
- acceptance status;
- preflight/QC status;
- any required `@img` reference;
- any unresolved direction or wiring decision.

Do not have ChatGPT and Fable concurrently edit the same active implementation branch to wire an asset. Follow branch ownership in `docs/DEVELOPMENT_WORKFLOW.md`.

## 9. Live-game boundary

Art production does not upload/write the live game.

The user remains the live-game actor under doctrine. A generated/processed asset is a production input, not authorization to publish it.
