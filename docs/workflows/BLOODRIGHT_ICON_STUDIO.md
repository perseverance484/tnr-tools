# Workflow — Bloodright Tier-Icon Art Studio

**Status:** DIRECTOR-APPROVED, 2026-10-16; **geometry-locked reskin factory and grouped review approved 2026-10-17** (RUL-2026-10-17-004 on this branch); art-production workflow, not live-game authorization.
**Lead:** Art Director; **support:** Image Production.
**Source lineage:** 2026-10-08 tracker `chatgpt/bloodright-icon-production-tracker-20261008@c85c1ea834e24315b5688f73a65c35479b8963e6`; operational baseline `main@99e86dc549b86f1f4a5846c0e509fa6bc15b3463`.
**Decision history:** `docs/RULINGS.md`, RUL-2026-10-16-004.

Use with `docs/00_INDEX.md`, `docs/workflows/ART_PRODUCTION.md`, `docs/workflows/ISOLATED_ART_GENERATION.md`, and `skills/producing-tnr-art/SKILL.md`. The skill's live art spec and validator own *mechanical* target rules. This workflow owns the approved **Bloodright three-tier emblem visual language and production sequence**, not Bloodright tree mechanics or renderer contracts.

## 1. Bounded production scope

- Initial **29 public A/S/H bloodlines** from the pinned, director-approved roster: **19 A + 6 S + 4 H**, three icon artworks per bloodline = **87 artworks**.
- One **Foundation**, one **Hidden Art**, and one **Advanced Art** visual is shared by all nodes of its tier *within the same bloodline*. Do **not** manufacture unique artwork for each tree node.
- Membership follows the pinned Fable Bloodright roster, not an inferred current live roster. Do not add the separately hidden, deferred or excluded records without a director scope decision and source verification.
- Per-bloodline status, IDs, historical evidence, and output QC belong in `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md` and its linked records.
- Bloodright structural SVGs and showcase posters use the *separate* `docs/workflows/BLOODRIGHT_POSTERS.md`; a poster is not an individual reference image for an icon.

## 2. Universal tier silhouettes — locked

| Tier | Immutable design silhouette |
| --- | --- |
| **Foundation** | One centered **elongated outer diamond** enclosing a smaller solid/faceted **inner diamond**, with clear black negative space between them. |
| **Hidden Art** | The **nested pointed diamond**, flanked by **two balanced inward-curving crescent arcs** connected by short **horizontal crosspieces** at mid-height. |
| **Advanced Art** | The **nested pointed diamond** surrounded by a **large, sharp multi-point starburst**, with strong primary cardinal points and smaller intervening rays. |

This is a **shape system**, not an invitation to invent a different symbol for each element. The silhouette, tier-relative scale, center, symmetry, principal points, crossing structures and negative-space hierarchy remain recognizable across all bloodlines. No halo substitution, added ring, wing, weapon, character, crest, alternative runes or surrounding pictorial scene. Minor organic edge texture must never change the silhouette. The black void separating concentric forms is deliberate and should remain clean.

**Allowed per-bloodline variation:** verified palette, intrinsic material/faceting, internal texture, small controlled chakra glow and edge treatment. Derived from that bloodline's *actual existing jutsu art* and user-approved treatment card; never infer from the name or classification alone. Preserve contrast against solid black.

**Director-approved background:** **solid black / near-black, opaque**, on every Bloodright tier icon. No chroma-key lime, transparency simulation, frame/UI, text, watermark, vignette scene or decorative background. **Do not redesign these emblems around rarity frames or fabricate alpha:** visual use of full-bleed opaque black is an explicit director decision. The separate jutsu-icon background approval remains in its own workflow; it is not the source of the Bloodright `skillTree.image` preflight contract.

## 3. Start a bloodline (Art Studio / persistent workspace)

1. Verify live repository baseline and exact tracker SHA; read current art authority, bloodline ID/rank, kit source and prior approval/QC evidence.
2. **Open the director-supplied bloodline reference ZIP** (or the matching inner ZIP from an outer multi-bloodline bundle), inspect/archive safely and verify names, IDs and manifest-image byte hashes where available. Then open **2–4 exact original bloodline jutsu images** and, when present, its identity image. Capture exact source names/IDs, provenance and visible material/palette. A screenshot, poster or kit JSON is not evidence that an unseen jutsu image was visually inspected. **These are thematic references, never instructions to remake the jutsu artwork.**
3. Inspect against approved BEE and Blue Blade Eyes tier-emblem *individual* examples. Their geometry is the family reference; **their color is not** the next bloodline's prescribed color. Compare adjacent/confusable bloodlines.
4. Propose a short **treatment card**: verified imagery, palette, material, glow constraints, distinguishability, forbidden borrowed colors/forms, and reference provenance. Obtain director approval before starting Foundation.
5. Record `VISUAL DIRECTION APPROVED` separately from the state of any generated file.

For generation, only pass **one or two individual images** selected for that one target, each explicitly labeled `silhouette-only`, `material/style-only` or `target identity`. Do not send a contact sheet or the full image collection to an isolated generator. The original image bytes must actually be attached/accessible; a link, image hash or prose-only recollection is insufficient. Current-chat re-encoded copies are usable for *visual orientation*, **not** assumed equivalent to the previously approved raw originals.

## 4. Approved geometry-locked reskin factory — three icons, one bloodline session

**Director approved 2026-10-17:** For Bloodright tier emblems **only**, replace the former *fresh image-generation conversation for each tier* requirement with **one clean reskin production session for each bloodline's matched three-icon set**. The separate bloodline **jutsu-icon rework** workflow still uses its own per-technique isolated-generation rules. Do not treat an existing-jutsu source ZIP as a request to redraw each jutsu.

**Preferred path: fixed-geometry masters and masked appearance treatments.** The Art Studio selects the three exact, approved, high-resolution **Foundation / Hidden Art / Advanced Art** originals as source/mask masters, verifies real bytes and hashes, and locks their geometry. The approved Ethereal Monarch individual raw PNGs are currently available as candidate family/template material, with hash evidence in `docs/design/bloodright/ETHEREAL_MONARCH_ICON_OUTPUT_QC_20261017.json`. They are **not Git-pinned binaries** and are not yet evidence of a reproducible processor. A separate tool/code pass must pin the approved actual master bytes before declaring deterministic regeneration possible.

For each bloodline:

1. **Treatment card:** Use its inspected jutsu references to choose actual palette, edge glow, interior material, and distinctions from nearby bloodlines. Approval can cover a *wave of 4–6* treatment cards; absent reference pixels require intake, not guessed materials.
2. **Single theme recipe:** Apply the **same approved appearance recipe** to all three geometry masters. Retain each tier's outer bounds, centroid, pointed diamond/crescents/starburst, crossing positions and black negative space. Color and material variation can be substantial **inside the fixed geometry** (crystal, heat fissures, shadow, polished metal, etc.); a color-only recolor is not universally sufficient.
3. **One dedicated session, three separate images:** Prefer a deterministic/shape-masked image processing pass when it yields premium results. For themes needing generative detailing, use **one new isolated production conversation for that bloodline** with the actual tier silhouette reference(s) and one or two relevant *individual* thematic images at a time. Produce/return **three individually saved, square tier images**; no generated sheet or contact montage as the artwork itself. If any output alters its fixed geometry, reject/restencil it rather than accepting a creative new sigil.
4. **QC sheet and batch review:** After the three source files exist, compose a **non-generative contact sheet from the exact saved pixels**. Group roughly **4–6 bloodlines per review wave** (rows = bloodlines, columns = the three tier images). Director accepts/rejects **each bloodline's trio**; keep already approved rows immutable and revise only rejected sets.
5. **Delivery:** Preserve accepted raw bytes, make three separate versioned lossless WebPs, compare at 125/64/32, verify hashes and ZIP contents and update the tracker. Fable can ingest the verified three-icon package in parallel with separate hidden structural Forge import preparation. The art studio performs **zero game reads/writes**.

**Pilot completed and director visually approved 2026-10-17:** `BR-075 Taiyo Kami` and `BR-029 Godstorm Eclipse`. The director supplied both exact source-art ZIPs; all five Taiyo + twelve Godstorm original jutsu reference images and two identity images were verified from the packs. The six independently saved tier-emblem raw PNGs are visually accepted. The corresponding six 256×256 lossless RGB WebPs passed offline file/pixel/byte/ZIP checks; evidence is `docs/design/bloodright/BLOODRIGHT_FACTORY_PILOT_QC_20261017.json`. **This is not proof of a deterministic geometry processor or `skillTree.image` formal preflight.** Continue with 4–6 new bloodlines per approval wave.

**The canonical geometric lock is not a sheet:** source masks/individual reference files are authoritative; a batch preview is only a QC aid. This factory protocol is a *specific Bloodright three-tier exception* to the broader one-image-per-isolated-generation default.

## 5. Production and evidence gates

Track these separately; passing one does not imply the next:

- **VISUAL APPROVED:** director accepted the *specific* raw original, with documented bloodline/tier and SHA-256.
- **RAW INTAKE VERIFIED:** actual source bytes accessible, decoded format/mode/dimensions and SHA-256 recorded; source immutable/pinned when repository storage is authorized.
- **FAMILY QC:** display checks at **125 / 64 / 32 px** for silhouette recognition, black negative space, no tier confusion, consistency of palette/material, neighboring-bloodline contrast. The 125px number follows the current generic ICON reference, **not yet an independently verified future Bloodright UI display contract**.
- **EXPORT QC:** use actual current `25x_DATA_art_spec.json` target and appropriate processing scripts. Historical BEE/BBE output used opaque RGB **256×256 lossless WebP**; verify container codec, dimensions, bytes, pixel preservation, black corners, exact `@img` filename, fresh versioned filename and packaging integrity. Record output SHA-256, size, paths and command.
- **PREFLIGHT:** invoke the real repository validator and record **all errors**. The current shared `ICON` target still assumes **lime chroma-key / RGBA**; director-approved opaque Bloodright RGB exports fail the generic **alpha** rule. Treat this as **PREFLIGHT-BLOCKED / field-contract resolution pending**, not a silent waiver or green preflight. Do not manufacture transparency, alter validation/spec code, or declare the file upload-ready merely because visual/byte/codec checks passed.
- **WIRING/PUBLISH:** separate future action only after user-approved client-field/spec resolution, source preservation and explicit operator authorization. Repository work alone authorizes **zero live-game requests/writes**.

Do not assume `item.image`, `jutsu.image`, and `bloodline.image` faithfully describe the *future Bloodright tier-skill icon field*; Fable must verify its actual consumer before a delivery/write contract is set. Any code/spec/preflight fix is **Lane A, Fable-owned** and independently reviewed, not an art-studio workaround.

## 6. Progress accounting and next gate

2026-10-08 tracker evidence: **BEE 3/3 and Blue Blade Eyes 3/3** director-approved and historically processed to WebP (**6/87**). Their accepted output hashes appear in the two `*_ICON_OUTPUT_QC_20261008.json` records. Neither accepted raw binaries nor final WebPs were pinned in the tracker branch; do not mistake screenshots or user re-uploads for byte-identical production originals.

**Current production register (2026-10-17):** BEE, Blue Blade Eyes and Ethereal Monarch were previously approved (9 icons). The director then approved **Taiyo Kami and Godstorm Eclipse's two complete 3-icon pilot families** (six further originals) and local RGB 256×256 lossless export/QC is complete. **15/87 tier emblems visually approved and file-QC exported; 24 families / 72 emblems remaining**. See `ICON_PRODUCTION_TRACKER.md`, `ETHEREAL_MONARCH_ICON_OUTPUT_QC_20261017.json` and `BLOODRIGHT_FACTORY_PILOT_QC_20261017.json`. Approved files are conversation deliverables until pinned at immutable repository SHAs.

**Next:** begin the first post-pilot **4–6-family wave** with new operator-supplied art reference ZIPs; do not regenerate Taiyo/Godstorm or the earlier three accepted families. **24 remaining sets / 72 images**. Machine geometry-master processor implementation, field-verified mechanical `skillTree.image` preflight, immutable binary pins and Forge import validation remain separately required. No live-game requests or writes are authorized.
