# Bloodright: Fable design output to ChatGPT posters

This is a guide for the later **ChatGPT art session**, not a change to Fable's active planning assignment. Fable is already running against its approved planning brief. Do not interrupt it, edit its branch, or require it to restart for this document.

## What Fable is already required to save

The existing `state/prompt_bloodright_planning.md` requires committed outputs under `docs/design/bloodright/`: an approved roster, kit dossiers, structured tree JSON, readable Markdown, deterministic SVGs, complete build examples, validation results, cross-bloodline balance analysis and an engine-gap register. Fable must finish with its exact repository, branch, base and head commit SHAs and completed/blocked entries.

Those committed files are the durable handoff. A chat summary or a temporary file path is not the handoff. Fable does not need to generate themed artwork or add a new poster-pack format while its current session is in progress.

## Start the later ChatGPT session

Supply Fable's final repository/branch/head SHA, the bloodline to start with, and the approved Taiyo Kami poster as a visual reference if it is not otherwise accessible. A new session needs access to that repository or an exported copy of the committed files. Do not assume access to the previous chat's attachments.

Read the actual final files at the supplied **immutable Fable head SHA**, including the governing design brief and validation results. Discover the output filenames Fable actually used; its brief did not prescribe a per-bloodline directory naming scheme. Match bloodlines by stable record ID, not approximate names. Taiyo Kami remains the reference; the other 43 approved IDs form the generation queue.

Keep Fable's design branch frozen. Any poster preparation or text corrections made by ChatGPT belong in a separate `chatgpt/*` art branch or separate deliverables. Do not replace Fable's analysis as a side effect of creating artwork.

## Assemble one bloodline's generation inputs

| Input | Purpose |
|---|---|
| Tree JSON at Fable's head SHA | Exact node names, tiers, costs, effect tags, static values, selectors, recipients and prerequisites |
| Corresponding SVG | Legible layout, all connections, full skill text and tier hierarchy |
| Kit dossier, builds and validation | Confirm scope, repeated matching rows, totals, real limitations and completed versus blocked work |
| Bloodline image/icon | The bloodline's visual identity; use a captured public source or a supplied image |
| This guide plus the approved style image | Consistent art direction and presentation conventions |

`poster_assets.json` supplies the captured public icon URLs for the 43 approved remaining bloodlines and Taiyo Kami. These are **image references only**, taken from the existing 2026-10-01 capture. Their availability and contents have not been freshly fetched. Retrieve and inspect the exact image before generation. If unavailable, flag that reference and request the image when needed; do not invent a successful download or substitute a similarly named bloodline.

If a packet is otherwise complete, the later ChatGPT session can prepare a compact `poster-brief.md` and render the SVG to a reference PNG locally. This is presentation preparation, not a reason to send Fable back through its planning work. No new numeric values, branches or mechanics may be invented to fill a poster.

## Exact data and presentation

The structured tree, SVG and final effect tables must agree. If they disagree, resolve the discrepancy from the final design/evidence before rendering that entry; do not silently blend versions. A complete proposed design can be shown as **Experimental design** without pretending the user has approved its balance or that the engine supports it live. A recorded blocker is not a completed tree.

Preserve each tree's actual node count and topology; do not force every bloodline into Taiyo Kami's four-column arrangement. Show the 4 BP budget, 1 BP once-only cost, prerequisite arrows and no-more-than-one-Advanced-Art rule. Keep all tier labels. Show full effect names, numeric values and the eligibility scope. Internal node IDs remain useful for checks but must not appear as skill numbers on cards.

Use a single shared target-role legend with matching text/icon colors. Teal identifies self buffs, rose enemy debuffs and amber direct damage; label additional recipient roles explicitly if a kit needs them. Do not repeat Self Buff/Enemy Debuff/Damage role labels on every card. Afterburn is an enemy debuff that makes damage dealt cause additional Afterburn damage during its existing duration, not a standalone damage instance. Infer recipients from the actual rows, not just the tag name.

Retain the static examples where relevant:

- `Static bonuses: a 35% tag with +5% becomes 40%.`
- `A 40 EP jutsu with +5 Damage becomes 45EP.`

Do not restore the removed supported-tag/scope-preservation footer notes, old 20/30 SP budgets, numeric skill labels or superseded Taiyo Kami values. Solar Cataclysm has Damage only; the moved Increase Damage Given bonus belongs to Eternal Noon in the current reference.

## Shared art direction

Use the approved hybrid direction: evocative bloodline-themed hero art, selective glow and a restrained decorative frame around calm dark cards. Keep clear hierarchy, generous spacing, legible text and obvious forks. Flashy, not gaudy; neither a dense ornament wall nor a sterile diagram. Change the central subject, environmental motifs and accents to suit each bloodline. Do not copy Taiyo Kami's fox or fire into unrelated bloodlines.

The supplied bloodline icon controls identity details. Any distinctive counts or anatomy, such as weapon tines and eyes, must match the selected reference. Treat a visual reference as styling/identity evidence, never as authority for old numbers or mechanics. If the exact style poster cannot be recovered, say so and use this written direction or ask for it when exact matching matters.

## Generate, check and record

1. Render and inspect the deterministic SVG, then use it and the inspected bloodline image with image generation.
2. Compare the generated poster against the canonical tree: every name, tag, value, recipient color, cost, prerequisite, arrow, tier and footer. Recheck Afterburn and repeated effects. Fix mistakes before marking it complete.
3. Record a small generation log keyed by bloodline ID: Fable head SHA, actual source paths, tree/SVG content hashes, image reference, final prompt, output filename or persistent asset reference, QA result and any remaining issue.
4. Track completed, queued and blocked posters so another session can resume without regenerating finished ones. Create this index from Fable's actual final outputs; do not claim all 43 are ready just because the roster is approved.

Keep reproducible text/specifications in the repository and the generated poster PNGs in persistent deliverable storage. A `sandbox:` link or temporary workspace filename alone is not durable storage. Do not commit rendered poster binaries as routine repository content. Existing repository art rules govern any later game-upload assets; these showcase posters do not themselves authorize game changes.

## Minimal new-session request

> Generate Bloodright posters from Fable's completed planning handoff in `perseverance484/tnr-tools` at commit `<FABLE_FINAL_HEAD_SHA>`. Start with `<BLOODLINE_NAME>`. Read the final tree JSON, SVG, kit notes and validation; use the approved Taiyo Kami visual style and the matching bloodline image. Preserve the design exactly and keep a generation log so we can continue through the roster.

Replace the placeholders with Fable's actual final SHA and the chosen name. This guide's own commit is not Fable's final design commit.
