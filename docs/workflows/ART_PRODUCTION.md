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

## 1b. Visual reference bootstrap

Where the repository carries visual references for the target, inspecting them is a **required**
bootstrap step, not an optional aid. It is what makes a fresh art conversation start from the same
approved artwork as the last one instead of from prose and memory.

1. Identify the target/type and register.
2. Read the current `25x_DATA_art_spec.json` target block and `house_style`. **References
   calibrate; the spec governs** - the reference pack does not replace `spec.house_style` and owns
   no style clause or number.
3. Run `skills/producing-tnr-art/scripts/style_refs.py select` for the target.
4. Open and visually inspect each selected **individual** image before composing anything.

Constraints that come with it:

- Use the selected individual images, never a collage or contact sheet.
- Placing a raw URL in a prompt is not evidence that an image generator ingested those pixels. If
  the surface cannot take image references, inspect the images yourself and ground the art
  direction in what you actually see.
- Begin a new asset class in a clean generation context carrying only its own references, so a
  previous unrelated generation cannot displace the subject.
- Honour any `do_not_use_for` limitation recorded against a reference.

`style_refs.py verify --repo-root .` audits the pack's bytes, dimensions, format and provenance and
should be green before a session relies on it. `style_refs.py bundle --check` proves the committed
operator transfer bundle under `art/style_ref_bundles/` still matches the pack.

## 1c. Generation gate — repository-ready is not generation-ready

A workstream task marked `READY` has its durable inputs committed. That is all it says. Whether
**this** conversation can generate correctly depends on runtime facts the repository cannot hold:
whether the selected reference pixels were actually rendered here and looked at, whether the
generation surface holds them as image inputs, and whether the context is clean of another asset
class. The workstream initializer prints those as `SESSION GATES / ACTION READINESS`
(`docs/workflows/CONTENT_WORKSTREAM.md` section 4b); an unproven gate means the action is forbidden.

### Reference modes

Exactly one applies, declared by the session from what it actually did. The definitions live in
`skills/producing-tnr-art/SKILL.md`; in brief:

| Mode | What is true | What the session must say |
|---|---|---|
| `ATTACHED` | the selected individual reference images are real rendered image attachments / input images in this generation conversation | preferred for ChatGPT production generation when selected references exist |
| `ASSISTANT_GROUNDED` | the assistant visually inspected the selected pixels, but the generation surface cannot receive them as image inputs | the canonical text contract is used, grounded by that inspection; the generator received no reference images; no reference-image conditioning is claimed |
| `NOT_HYDRATED` | only metadata, paths, URLs or unrendered bytes/base64 are available | image generation is forbidden until hydration occurs |

Uploading the transfer ZIP (`art/style_ref_bundles/tnr_style_reference_pack.zip`), quoting a raw
URL, reading a hash, fetching base64 that is never rendered, or building a collage hydrates
nothing. The bundle exists so an operator can download the exact bytes once to a phone, extract
them once, and later attach the individual images a preflight names. `ASSISTANT_GROUNDED` is
allowed only when the pixels were genuinely inspected through a real rendered-image path and the
generator cannot take image inputs; it is not a fallback for skipping hydration.

### Required order for ChatGPT production generation

1. initialize the workstream task and read its session gates;
2. render the deterministic generation-preflight packet
   (`skills/producing-tnr-art/scripts/generation_preflight.py prepare`) for the exact
   target/register/frame/subject, pinned to the verified commit;
3. hydrate and visually inspect each selected individual reference, and say what was seen; where
   file access permits, hash-check the attached bytes against `style_refs.json`, otherwise say that
   hash equivalence is unverified rather than assuming it;
4. declare the reference mode — prefer `ATTACHED`;
5. establish a clean generation context carrying only this asset class and its references;
6. settle enough user-owned art direction for one meaningful candidate; surface the packet's
   `direction_review_required` items and any open decisions rather than settling them;
7. immediately before the image-generation call, stage the canonical generation contract from the
   packet in the conversation — the exact target/scaffold/subject/negative fields, verbatim;
8. generate exactly one candidate;
9. classify the returned image as a **PROVISIONAL RAW CANDIDATE**;
10. raw-QC it (section 4) before any processing.

The repository cannot add a binary or file argument to ChatGPT's image-generation surface, and it
cannot prove what internal prompt representation the product used. It can prove what contract was
staged (the packet and its hash) and which references were present in the conversation. Do not
claim more than that.

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

The returned image is a **PROVISIONAL RAW CANDIDATE**: not accepted, not production-ready, not an
implied asset. It proceeds only through section 4. Treat ChatGPT-generated imagery as raw source
art until the repository's production checks pass.

## 4. Raw QC

Immediately after generation and before any processing:

- run the current raw-QC mechanism required by the art skill where tooling is available;
- visually inspect composition and target suitability against the staged contract;
- a wrong visual register (photoreal, cinematic, soft-painterly, anime), scenery or a surface behind a keyed character target, wrong aspect/mode, prohibited insignia, wrong framing/camera, unusable key/background, painted glow blocks, inseparable surfaces, or any other failure the skill marks as a regeneration case is a **REJECT**: state it in one line and do not process.

Only a raw-QC pass proceeds to chroma/processing, dark-composite QC and art preflight. Final
acceptance remains the user's (section 7). Do not spend processing effort trying to salvage an
unprocessable generation.

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
