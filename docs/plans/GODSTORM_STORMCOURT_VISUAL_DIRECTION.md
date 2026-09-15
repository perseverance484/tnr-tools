# Godstorm: Stormcourt visual direction

2026-09-15 | Source inspection complete; direction and production allocation proposed, not approved art

## Result

Stormcourt should be the exposed upper court of the same dark-stone structure shown in the Marrow backgrounds. Keep the masonry, arched openings, aged brass, chains and violet energy; replace the enclosed vault ceiling with a rain-exposed central court and restrained storm light. No SkychainMonastery artwork or earlier infographic illustration is a reference.

## Evidence and scope

Verified repository refs for this review:
- main: `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`.
- planning branch: `chatgpt/godstorm-two-pyramid-plan@c7055bc56683fc00abcd5ceb6a2fb41459c0589e`.
- recovery branch: `chatgpt/godstorm-art-recovery@1bca57eeb0c1836a49334dc2f49196a5a3db24c7`.

Authority: `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, the Art Director role, `docs/workflows/ART_PRODUCTION.md`, the current art skill/specification, and `GODSTORM_ART_REUSE_DECISIONS.md` AR-001. RUL-2026-09-15-003 owns the approved connected-setting decision history; RUL-2026-09-15-004 records the exclusion. Operational state projections still describe older Forsworn work and do not certify Godstorm completion.

The previously delivered `godstorm_source_art.zip` was extracted locally, with safe-path/ZIP-integrity checks and SHA-256 verification of every indexed image. All 19 files fully decoded through Pillow. ZIP SHA-256: `57c331ab29d79bdde795e0b4fd08ac3eeeae9e656fa1b71295aeab0ca54295a1`. These are September 15 downloads of URLs captured on September 14, not proven original generation masters.

Individually opened and visually inspected for this direction: all three Marrow backgrounds, all nine retained Stormcourt avatars, and the Stormcourt quest listing image (13 original files). The rejected StormCourtyard was not visually opened or used as a reference in this pass. Its archived bytes were included only in the archive-integrity check. The comparison sheet is composed from unchanged source images; it is not a proposed gameplay background and must not be sent to a generator as a collage reference.

The archive `index.json` supplies exact entity IDs, snapshot keys, capture pointers, URLs and hashes. Machine-readable local review evidence is supplied with the review package; source-image paths below are relative to `art/godstorm_sources/capture-2026-09-14/` on the recovery branch.

## Pixel observations

| Source | Visible evidence | Consequence |
| --- | --- | --- |
| marrow vault 1 | Block masonry, tall arches, iron restraints/chains, aged-brass circular mechanisms and floor inlay, small violet lamps | Primary architectural/material reference for the Court |
| marrow vault 2 | A heavy part-open arched door, iron details and violet light beyond | Threshold reference; suitable candidate for the end of the Vaults, subject to acceptance |
| marrow vault 3 | Camera looks down a descending stairwell into the lower chambers | Entry/descent candidate, not an image of ascending into Stormcourt |
| Gloaming Judge | Black/violet robes, warm metal edging, geometric metalwork, heavy ceremonial gavel | Continue the same metals and formal architecture; do not introduce a different building tradition |
| Widow of the Waning Moon | Near-black clothing and cold pale blades | Cold edge highlights can remain a character accent, not a new environment palette |
| Candlewright | Dark garments with localized warm wax/flame accents | Allow sparse candle niches; do not make the whole Court amber-lit |
| Herald of the Last Dusk | Dark purple wraps, brass horn and trim | Repeats the black/violet/brass family |
| Sovereign Echo | Dark plated armor, brass trim, violet cloth and white-violet lightning at the helm | Binding dais should carry localized violet electrical activity and restrained bright highlights |
| Four Ascendant guardians | Dark armored silhouettes, purple fabric/edges, one localized cyan lantern | Background stays quieter and slightly more readable than the figures; no cyan redesign of the full Court |
| Stormcourt listing image | Violet electrical motif and warm metallic trim; also a framed tower/key-door emblem | Palette corroboration only. Do not copy its frame, keyhole doors or tower-as-logo into scene art |

These observations establish continuity, not final acceptance of every source file or identity detail.

## Proposed Court design

Architecture: retain Marrow's stone block scale, arches, heavy piers and metal fittings. The outer circulation remains sheltered; the central court is open to weather. A recessed stair opening makes the route from the Vaults readable without drawing a separate travel scene. Use the lower ritual hall's ring/inlay geometry as the basis for restrained conductors at the finale.

Palette: charcoal stone, blackened iron, subdued brass, deep violet cloth/energy and cold grey wet surfaces. Violet is the primary supernatural accent. Small candlelight and character-specific ice/cyan highlights remain local. Avoid a field of saturated purple, broad bloom, an enormous vortex or a black-sun/eclipse focal point associated with the removed finale.

Lighting: increase environmental readability above the Vaults through overcast light, rain-dark stone and small wet reflections. Keep defined shadow shapes and a limited palette. Do not reproduce the lowest-exposure portions of the source images merely to say the brightness matches.

Composition: eye-level view from just beyond the stair opening, looking toward the Court's raised far side. Put the significant architecture/dais to the center-right. Keep the lower-left figure area simple and free of bright runes, candles, rails or focal objects that a portrait would cover. No people, creatures, humanoid statues or built-in boss figure in the background.

Rendering: retain crisp pixel-edge decisions and restrained cel/painterly depth at the final scene size. Not smooth cinematic concept art, photographic stone, a generic giant cathedral, or a new ornamental palace. Existing art establishes the architecture; no external franchise is a reference.

## Recommended output allocation

This is an art-direction proposal, not a generated production shotlist, accepted commission count or wiring manifest. No new IDs have been assigned. All Court bindings remain unresolved under AR-001 until replacement files and records are accepted.

| Proposed output | Job | Draft scene coverage | Count |
| --- | --- | --- | ---: |
| Upper Court | New master environment: entry, circulation and keeper approaches. Include a restrained raised tribunal platform, peripheral candle recesses and cold sheltered stone, without making a separate setting for each keeper | d6_1 through d9_boss, five pre-battle dialogs in each group | 20 |
| Binding Dais — active | Second master/composition using the same structure/materials, focused on the binding instruments, ring inlay and active electrical pressure. Empty space for the separate Echo portrait | d10_1, d10_2, d10_3, d10_4, d10_boss | 5 |
| Binding Dais — released | Derivative of the accepted active master: same camera and structure; electrical activity extinguished, ordinary rain retained, no invented destruction | d10_victory | 1 |

Total proposal: **two new master backgrounds plus one derived state, covering 26 dialogs**. The derived state is a delivered image requiring its own QC, not a free implicit engine effect. It is contingent on accepting the draft binding-breaking ending. Do not generate all three before the first master's direction is reviewed.

The smaller one-master option remains possible, but it provides no distinct final-keeper setting. The two-master recommendation makes the encounter's change of place readable without adding one painting per keeper. Existing source artwork supplies the reference/design basis, not completed Stormcourt scenery.

## Marrow mapping correction proposed after pixel inspection

The current editorial draft assigns M3 to the final Vaults-to-Court handoff. Its viewpoint actually looks down the stairs, so that assignment should not be presented as visually verified.

Propose M3 for the initial descent (`d1_1`) and M2's part-open threshold for `d5_victory`, with the Court ascent established in the text and next quest's opening. M1 remains the core ritual-hall plate. This changes two proposed scene bindings, not any game record or source artwork. No flip, repaint or misleading crop is needed. Final visual/storyboard acceptance is still required.

This change would replace one previously retained M1 binding at d1_1; distinguish it from the 47 currently missing background fields. It does not change the 52-dialog structure or the number of background source files.

## Technical observations and target contract

The current specification at main requires SCENE_BACKGROUND aspect 3:2, delivered width 512, minimum width 512, lossily encoded WebP q85 and working ceiling 460800 bytes. Recommended source sizes include 1536x1024. Background composition reserves the lower-left area for the character, whose wrapper is 40% of scene width. Source: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target SCENE_BACKGROUND. Read the spec again when producing the deliverables; this brief does not replace it.

The three recovered Marrow plates are 500x333, just below the current minimum width. Do not classify them as newly production-validated or silently upscale them to claim improved detail. This is a minor legacy resolution gap, not a reason to redraw all three automatically. Their reuse or a source-original recovery remains a separate acceptance choice.

Exposure diagnostics were measured on original bytes using Pillow RGB-to-L conversion with coefficients 0.2126, 0.7152, 0.0722 and integer output:

| Plate | Median luminance, 0–255 | Pixels below 20 |
| --- | ---: | ---: |
| M1 | 10 | 72.48% |
| M2 | 4 | 91.79% |
| M3 | 6 | 85.28% |

The spec's exposure guidance flags medians below 8 or over 90% of pixels below 20. These diagnostics make M2/M3 readability a review item; they are not a claimed repository-preflight run. Keep the references' materials and color relationships while making new Court midtones visible. No brightness correction was applied to any original in this pass.

The inspected Court avatars are transparent PNGs at 256 pixels high. Their identity/palette is useful, but source size, target ratio and pixel quality need separate checks before avatar or scene-character delivery. No new portrait conversion was performed here.

## Next production gate and safety boundary

Review this direction and two-master/one-variant allocation. The first candidate should be the Upper Court alone. Before generation: run the current art reference selection, inspect the selected individual references, scope the generation context to the accepted Godstorm images, and use the current background scaffold/target. Do not include the rejected image, recovery overview containing it, or the earlier infographic illustrations. Mechanical reference-pack provenance and production QC remain required, not implied by this inspection.

After generation: raw QC, appropriate export, native delivered-size review and separate actor-overlay check; then user acceptance. The binding and released variants follow only after the first result establishes the rendering/material standard.

This pass performed repository reads, ZIP/hash checks, full image decoding, actual individual-source inspection, source comparison assembly and local proposed-coverage assertions (26 unique Court dialog IDs). No production artwork was generated or altered, no live-game request was made, and no capture/mutation/asset upload was run. Direct Git access failed DNS; a local clone and repository session guards/art preflight were not run. Repository evidence was read through the authorized connector. Documentation belongs on the ChatGPT planning branch; Fable's implementation branch and main remain untouched.
