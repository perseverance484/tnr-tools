# Tempest Cleave — premium caster-cleave refinement plan

**Status:** Director-approved visual *strategy*; design/production plan only. No round-2 raw accepted; no image generated or uploaded by this plan.
**Date:** 2026-10-24
**Repository baseline:** `main@44dcad9338c7a5be9df545168fe820b93b40388e`
**Target:** `jutsu.image` — Tempest Cleave, `Ul83iTziN__Z0i_UOzZTK` (EVENT, A rank; no bloodline)
**Leads:** ChatGPT / Art Director + Image Production for original raw; Fable / Claude Code for raw intake, pixel snapping, 45px/112px previews, export/preflight, record updates. Director owns all final art decisions.
**Live game:** 0 requests, 0 writes. No credentials.

## Decision and source boundaries

This is a **target-specific departure** from the abstract-only / no-figure round-1 directions in `PILOT.md`, `TEMPEST_CLEAVE_PILOT_SESSION_PROMPT.md`, and active `RUL-2026-10-24-002`. The director selected the original fox-masked storm caster as the new foundation, approved the more literal, storm-powered *cleave* read, liked the caster/slash candidate, and endorsed the proposed quality-refinement strategy. It is **not** a project-wide rescission of the provisional abstract-emblem ruling; Fable should reconcile the pilot's operative per-target guidance after the director accepts an updated candidate. Do not silently blend the two incompatible "no figure" and "keep masked caster" briefs.

Historical, committed `PILOT.md` describes an outward AOE ring and a storm of razor wind. The visual moment selected for the current icon is the **storm being released as a cleaving air slash** by the mask-wearing shinobi, without altering the jutsu's actual effects or battle text.

**Subject/composition reference:** user-selected `1000019223.png` from the art conversation, **1536×1536, RGB, actually JPEG-encoded**, 559,366 bytes, SHA-256 `db11fae3921e46e0a15c9863b038da4cf1731915e83b678d89ce4c93c41100d5`. The attachment is *not pinned as source bytes in this repository*. Before an isolated refinement generation, reattach the original, individual image; do not use a screenshot, contact sheet or textual filename alone and claim reference conditioning. Intake must identify **true decoder format**, not `.png` extension. The new raw's real format and its source hash are to be recorded separately.

**Reference budget:** use only the selected source as SUBJECT / COMPOSITION lock. Optionally add **one** approved TNR icon as STYLE ONLY after actual inspection, without copying its subject, hue or motion. Do not attach the abandoned abstract storm trials, the blade-ring/shuriken failure, or any collage.

## Creative lock — preserve before changing

Keep the selected candidate's identity: recognizable white fox-like **generic** mask, midnight/charcoal layered shinobi armor, braced casting stance and extended forward hand; upper-frame swirling slate/blue-white storm; singular large slash descending diagonally **upper left → lower right**. The mask and storm must belong to one action. No sword, opponent, new figure, clan/series symbol, headband, scenery vignette, seal/rune or UI.

The image has a strong existing action line and colour identity. Preserve its general camera, diagonal motion, mask construction, and dark navy/blue-white palette. Preserve the dramatic **front-plane** cleave, but do not preserve its beam-like geometry or excessive white fill merely for pixel-for-pixel similarity.

The selected reference contains tiny burgundy/maroon mask marks. Keep the *mask identity*, including restrained markings if needed; do not introduce red/orange to the storm, slash or environment. This mask-only exception and the now-visible figure are local differences from round-1 no-red/no-figure restrictions, to record when the pilot brief is reconciled.

## Stage 0 — archive / baseline gate (Fable intake)

1. Preserve the exact selected user-upload bytes and SHA; mark current status **visual reference, not accepted export**.
2. Record decoder/MIME mismatch (filename says PNG, bytes decode JPEG); do not quietly relabel the original as a lossless PNG.
3. Build a deterministic baseline comparison at 45px (normal and blurred grayscale), 32px, 64px, 125px, and 112px badge mockup. Use this to measure *improvement*, not to process a new raw.
4. Verify which implementation of `pixelsnap.py` is available. At baseline it is **not present on main**; the pilot points to Fable's `fable/pixel-art-snap` branch. Do not invent a canonical processing command or claim a pass until the actual tool/ref and run are recorded.

## Stage 1 — composition and action (ONE exploratory raw)

**Priority 1: turn beam into a cleave.** Retain the same upper-left-to-lower-right attack trajectory, but reshape the thick even white streak into one **sharpened curved cutting front** with a thin almost-white edge, cooler compressed blue body and a broken charcoal/slate wake. A visible leading edge and taper should announce a *cut through air*, never a lightsaber, generic laser, lightning bolt, water wave, claw set, crescent moon or metal weapon. Preserve a single primary slash; subsidiary wind ribs trail it, not multiple coequal attacks.

**Priority 2: give the caster readable scale.** Bring the figure *approximately* 25–35% optically closer versus source without turning it into a portrait. Increase the mask's screen occupancy to support a distinct pale fox-mask silhouette at 45px; keep the forward arm readable, the torso dark, and the mask clear of the slash. The lower legs may be simplified or partially out of frame. Only one complete, anatomically plausible pair of hands. The figure supports the cleave rather than eclipsing it.

**Priority 3: link cause to effect.** Make the storm bands funnel toward the casting arm, then join the slash through one unmistakable compact wind-transfer ribbon. Tone down or remove repeated wrist-loop decorations, especially the off-hand circle, which presently implies a second competing technique. Keep the storm canopy in the upper portion and lower the brightness of its stripes.

**Priority 4: reduce noise.** Delete random black floating chunks and repeat highlights in favour of a few planned torn-air gaps along the slash. Abstract away the village, torii and fire. Background remains dark, two-tone storm field, not a new scene.

**Framing:** one square full-bleed opaque icon. Eye-line/mask and initiating hand in the safe upper/central area. The dramatic slash may crop *deliberately* at the leading/trailing outer edges as in the approved foundation, but its meaning must remain legible when the 112px tile's two lower-corner badges obscure the corners. Do not let mask, casting gesture or other essential information touch the occlusion zones. This intentional attack crop is another target-specific reconciliation against the old abstract prompt's blanket "nothing touches edges".

**Stage 1 director gate:** does it read as **masked shinobi channels storm → devastating razor-wind cleave** at 45px? Does it preserve the selected candidate's identity? If yes, freeze the macro composition and move to stage 2. If no, correct geometry, not texture.

## Stage 2 — value and palette pass (ONE controlled same-subject revision)

- Establish a three-level hierarchy: (1) sharpest white cutting *edge* / primary attack, (2) pale mask and blue-grey wind body, (3) nearly black armor/background; keep the brightest saturation/white coverage **narrow**, not a giant uniform wedge.
- Keep one dominant illumination event at the cleave; streaked light reflected on the forward hand, sleeve plate rims, and mask is subordinate, **not another glow source**. The storm canopy must remain visibly darker than the cleave.
- Separate materials: ceramic mask (hard pale planes), layered armor (dark interrupted planes), compressed cutting air (ribbon/wake with clean empty gaps), lightning (very sparse electric branches).
- Primary hues: charcoal/navy, steel-slate, cool blue-grey, icy-white, occasional pale electric blue/cyan. No teal/green, pink, orange fire, broad warm accent, or red energy. Tiny existing mask markings alone may remain.
- Re-test greyscale 45px and 32px at this stage. A stranger must identify *wind slash* rather than beam/water; caster must still be nameable as a masked ninja.

## Stage 3 — premium pixel-art finish (ONE controlled same-subject revision)

- Use the approved TNR jutsu-icon **retro 32-bit** rendering target: coherent pixel clusters, hard stepped contours, controlled cel-shaded planes, no blur, painted gradients, bloom, fake pixel noise, micro-speckling, fine hairlines or random dithering.
- Design around approximately **48–64 effective art pixels across** for eventual deterministic `pixelsnap.py` processing, with a disciplined **16–24 colour** final target as governed by the pilot. Image generation alone does **not** prove a clean single grid or this colour count.
- Favor distinctive *clusters* over intricate pattern on armor. Make the mask eye slits and horn/ear silhouette survive at thumbnail size. Preserve slightly asymmetric storm arcs.
- Avoid fake sharpening/upscaling; the production snap must not be used to repair a failed macro shape. Compare candidate **raw and snapped** before promotion.
- No character anatomy errors, decorative runes, ornamental frame, lens flare or unrelated environmental props.

## Fail-fast and approval gates

**Reject before requesting approval** when any candidate resembles shuriken/saw/portal, beam/laser, glossy water effect, a mass of lightning without wind, has rotational symmetry, loses the mask, breaks finger/arm anatomy, makes the vortex brighter than the slash, buries the caster, or adds a busy village/scenery. Review at true 45px, not only the large render. After two wrong-subject/composition failures, restart a fresh isolated generation per `ISOLATED_ART_GENERATION.md` using only the selected reference and tight original target lock.

**Director visual acceptance** is separate from mechanical readiness. After director chooses the raw:
- Fable intake: preserve true raw source bytes and hash, raw-QC and output metadata.
- Fable gates: 45px recognition, grayscale/blur silhouette, 32/64/125px, 112px badge, side by side with original/selected candidate and kept icons; note family distinction from BEE's Ring of Spilled Blood and other cool-colour wind effects.
- Fable processes using the actual reviewed/pinned `pixelsnap.py` and current TNR art spec, with **no chroma key** for opaque jutsu icons. Produce a fresh versioned square lossless WebP according to `JUTSU_ICON` spec; run `artpreflight.py --type JUTSU_ICON` and any stricter workstream cap when explicitly established. The current jutsu-icon spec recommends a 256×256 output and accepts an opaque background. Never call the raw upload-ready merely because it looks good.
- Fable updates `PILOT.md` / the relevant canonical director decision record after director acceptance; maintain clear distinction between local figure exception and the wider abstract-emblem ruling.
- Only the director authorizes final acceptance and any live-game action. No game requests/writes, credentials, uploads, manifests or publication in this plan.

## Proposed output convention

Each isolated image generation produces exactly **one** untouched raw, for example `raw_tempest_cleave_caster_cleave_R2-01.<actual-source-extension>`. Do not mislabel JPEG bytes as PNG. Stage-1 rejection is logged; stages 2–3 use fresh filenames and retain the preceding stage for A/B comparison. Proposed Fable intake folder: `art/jutsu_icons/tempest_cleave/candidates/caster_cleave_refinement/`.

**Next action:** reattach the selected exact source in an isolated single-candidate image-edit generation, implement Stage 1 only; do not jump straight to palette/detail until the director accepts the new slash geometry and caster prominence.
