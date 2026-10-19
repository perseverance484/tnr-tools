# BR-036 Itojinsei — Blackwire Neutral Pewter V04, Source-Geometry-Locked Foundation Pilot

**Date:** 2026-10-18 · **Lead:** Image Production · **Supporting lens:** Art Director.
**Status:** NEW **FOUNDATION V04 PROPOSED — NOT DIRECTOR APPROVED**. Latest refined Freehand Foundation `futuristic_blackwire_diamond_emblem.png` was director **VISUALLY APPROVED** in conversation but is not assumed to match the universal geometry. The newly generated Hidden/Advanced freehand candidates are **NOT GEOMETRY-APPROVED OR FILE-ACCEPTED**. The existing 84/87 approved individual icons remain unchanged.
**Repository:** `perseverance484/tnr-tools`; `chatgpt/itojinsei-blackwire-finalization-20261018`; previous head `d5c7dc3e070bfbd73106b7aca04be5307bb262df`; art-lineage base `8b6edf8045b5f51331a7ac3f9c011e8907fe326d`. Read-only main confirmed `fd7e194afab71a5712b83d16397feffdf704e9d2`.

## Director feedback / family disambiguation

The operator said **“That's good. Approved”** about a new dark braided blackwire Foundation render, then two separately freehand-generated Hidden and Advanced images were made without respecting master geometry. Follow-up: **“Good but geometry drifted. Use proper workflow. Also I dont think the blue is necessary or part of the theme for shadow weaver, is it?”**

**This is BR-036 Itojinsei, not BR-063 Shadow Weaver.** The Shadow Weaver family has a separate director-approved `Ebony Silk V03` dark/gray material and **does not require blue**; see `BLOODRIGHT_WAVE04_BR063_EBONY_SILK_APPROVED_QC_20261017.json`. Itojinsei's source family includes **Lightning Threads** with sparse blue electrical highlights but these are **not mandatory to its black braided-wire identity**. To honor the desire for a darker, closer-to-refined-foundation look, the new **single** Itojinsei Foundation pilot uses silver/neutral pewter and black tension braids, **no vivid sapphire or electric-blue glow**, and contrasts with Ebony Silk's smokelike texture through solid metal facets and crossing black wires.

## Source bytes / exact shape owner

- Latest **director-accepted freehand Foundation VISUAL**: `futuristic_blackwire_diamond_emblem.png` **SHA-256 `b060ee0f0d715e1946d165da7837c738cf05e2ef330b01fa8d2e72231fbbffeb`** (1254×1254 RGB), unchanged. Its color/material/chisel texture informs V04; its hand-generated silhouette is *not* the shape authority.
- Earlier approved 3-emblem Blackwire visual composite `metallic_sigils_in_electric_blue.png` SHA-256 **`8391780ec142f3f74a77082f3c6ec462d2ae7876893193a05925f9559944542b`**, unchanged.
- Five original Itojinsei jutsu images plus identity reference ZIP `BR-036_Itojinsei.zip` SHA-256 **`1f6ffabce148272301f3f4c5b5f90db720985ce78763e82ea3dcfccbf7218dd0`**.
- **Actual approved Foundation original geometry master:** `geometry_masters/Ethereal_Monarch_Foundation_TEAL_1254.png` SHA-256 **`bb3a3e331e5913fa527049980e2738c151b85eb54ef579cd468126b10039cea2`**, extracted byte-exact from operator starter ZIP SHA **`9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`**.

The V04 production script is deterministic, uses the actual 1254px geometry master as an authoritative **pixel-activity mask**, and treats the latest approved picture as **material reference only**. All added black/silver braided wire overlays are clipped to precisely the old illuminated source positions. No new symbol, wing, crescent, spike, star point, external sparkles, UI or freehand shape is added. No three-icon generated source contact sheet used. This **Foundation-only** stop-and-review is required because earlier generator attempts kept drifting.

## Source/output identity and honest geometry verdict

| Artifact | SHA-256 | Size | Status |
|---|---|---:|---|
| 1254×1254 RGB `br036_itojinsei_foundation_blackwire_pewter_v04_1254.png` | **`e03ea5410ce31ffe9f0a85ebcc807e2e0d8332cba1737c64d781f38b78fa3a27`** | **1,124,803 B** | **Proposed only** |
| 256×256 RGB VP8L lossless `br036_itojinsei_foundation_blackwire_pewter_v04_256.webp` | **`f992a71182e7d52ee7b21d758ad0180434be244fa7483def19efa7f14ba451fc`** | **34,716 B** | **Proposed only** |

**Independent offline audit 44/44 PASS / 0 FAIL**, including exact original ZIP/source/approved-picture SHA and CRC, original master image SHA, 84 prior approved WebPs unchanged, raw PNG dimensions/RGB, WebP 256² VP8L/lossless pixel equality to intentional Lanczos resized raw, black corners, source support/negative space **perfect binary correspondence**, 125/64/32 view, bounded neutral color channel differences (max 15), deterministic independent recipe replay. No formal `skillTree.image` field-specific preflight.

**Crucial internal brightness exception — do not mislabel strict:** The user previously favored **Option B**, with genuinely dark braided cables. **The new V04 outer-source pixel footprint at threshold 1 is EXACT (IoU = 1.000000)**, including all black negative spaces, but black wires intentionally darken existing illuminated source-master pixels. Higher internal luminosity-threshold masks therefore differ: `t8=0.979883, t16=0.963957, t32=0.891339, t64=0.765904, t128=0.683481, t192=0.573580, t240=0.156056, t254=0.178220`. Full per-pixel `maxRGB` equality is **FAIL/NOT CLAIMED**. This is a proposed **director-owned internal wire-occlusion exception** to the stricter master-intensity factory, NOT an error-free strict geometry result. The conventional diamond geometry/negative-space source support is unchanged. The user must specifically accept these modified V04 image pixels (and acknowledge that tradeoff) before repeating the treatment on Hidden and Advanced.

## Portable proof and review

- **Complete source/master/reference/producer/independent QC package:** `BR036_Itojinsei_Blackwire_Neutral_Pewter_v04_Foundation_PROPOSED_Source_QC_20261018.zip`, **SHA-256 `e9a37b691244f5cae34085171a6e1f287129f6dbd29adf4632e0ae9536d1efcf`**, 13,174,730 bytes. Contains immutable latest director-approved visual source, earlier three-emblem source, jutsu source ZIP, immutable original master ZIP, deterministic Python producer, independent geometry/codec replay auditor, one separate Foundation raw PNG, one VP8L WebP, 125/64/32 QC and a comparison assembled programmatically from individual actual saved image pixels. 13 members, CRC/member byte-integrity PASS, double-build exactly reproducible.
- **WebP-only review ZIP:** `BR036_Itojinsei_Blackwire_Neutral_Pewter_v04_Foundation_WebP_PROPOSED_20261018.zip`, SHA **`c9192167f05f46d27d2680ebf6ddb5f46a5e97365cea771e735c4091ef30f01f`** (one 256px file, 34,941 bytes).
- **Review:** `qc/BR036_Itojinsei_Blackwire_Neutral_Pewter_v04_Review.png` shows latest accepted visual reference vs exact geometry master vs new actual 256px neutral-source version vs separate accepted BR-063 Shadow Weaver Ebony Silk Foundation. `qc/BR036_Itojinsei_Blackwire_v04_125_64_32_QC.png` confirms readability tests.

## Next user-controlled decision and remaining technical gates

**Director chooses whether this specific V04 Foundation sufficiently preserves approved Blackwire visual/material while keeping the correct universal diamond/black void, and whether dark-cable internal brightness exception is acceptable.** If yes, produce **two separately saved raw 1254px Hidden Art/Advanced Art** sources from their exact individual SHA-verified masters using the chosen same treatment, run shape/brightness loss tests independently, and request separate visual approval. **No new individual BR-036 icon was marked accepted** and the 84/87 collection remains frozen.

`skillTree.image` opaque RGB field-specific client/validator acceptance remains **NOT VERIFIED**; generic `ICON` keyed alpha does not give permission to upload, and JUTSU_ICON optional-alpha applies only to `jutsu.image`. Prior 21 historical visually approved but strict-intensity-nonexact items remain untouched. No binary art pinned in Git, no Forge imagePack, no ruling-ID conflict reconciliation, no game uploads/live reads/writes; credentials none.
