# Blue Blade Eyes — Jutsu Icon Identity Register

**Status:** **6/8 RAW VISUAL APPROVED; 2/8 REWORK REQUIRED.** The director expressly rejected the current **Arctic Frost** and **Blade Resonance** compositions as insufficiently fitting their jutsu and the BBE family, correcting earlier over-optimistic status entries. All eight *historical draft exports* are 256x256 opaque lossless WebP below 80,000 bytes, but the eight-icon bundle is **NOT an approved final art pack**; current shared ICON alpha preflight remains blocked and no live upload occurred.  
**Art Studio:** docs/workflows/ISOLATED_ART_GENERATION.md; director ruling RUL-2026-10-14-001.  
**Source basis:** director-provided jutsu database screenshots and approved image-generation outputs in the 2026-10-13/14 conversation. The screenshots document the names/visual meaning; they are **not** a current live capture.  
**Source bytes:** individual source identifiers, image formats, exact sizes and locally verified SHA-256 are in SOURCE_EVIDENCE.json. Those files are **not committed** in this documentation change.  
**Separate workstream:** the older BBE Foundation/Hidden Art/Advanced Art *Bloodright emblem* work at chatgpt/bloodright-icon-production-tracker-20261008 is **not part of this eight-jutsu icon set**. Do not edit or re-approve the existing BBE bloodline artwork here.

## Collection-wide visual lock

- **Palette:** frosted icy white, pale cyan, pale glacial-blue crystalline chakra; deep sapphire only for focused contrast and silhouette gaps.
- **Material:** semi-translucent faceted ice, white-fracture highlights, selective pixel-detailed edges, luminous sapphire interiors, restrained frost haze.
- **Composition:** one dominant technique-specific silhouette, one supporting effect, clear direction/negative space, high contrast at small sizes; the family shares **rendering and palette, not layouts**.
- **Ninja/chakra:** express the actual technique (speed afterimages, precision cutting, binding, resonance, protection, aimed volleys); no obligatory circular seal or eye emblem.
- **Background:** jutsu images **fill their entire square**, with **no rarity backdrop behind them** and **no transparency requirement**. Use a full-bleed, opaque, deliberately painted icy/sapphire atmosphere; no reserved margin for a rarity plate, no alpha-keying and no artificial transparent corners. This is the director's visual/client requirement; the shared ICON preflight's alpha mismatch remains unresolved (see protocol).
- **Avoid:** actors/portraits, mandatory symmetrical mandalas, portal-summoned weapons, duplicate subject motifs, overlapping main silhouettes, extra unrelated ornaments, text, frames/grids, franchise insignia.
- **Production:** square lossless WebP, current spec's output dimensions, **<80,000 bytes** for BBE exports, visual comparison at 125/64/32px; exact @img filename and honest mechanical preflight verdict.
- The accepted source art is **visually locked**. An assistant may not replace/reinterpret it during processing without renewed director authorization.

## Eight-image distinction ledger

| Jutsu | Unique thumbnail silhouette and action | Status | Primary source |
| --- | --- | --- | --- |
| **Blue Crimson** | **Z-shaped** discontinuous, extremely fast icy chakra movement; sharply broken displacement/strike trails, **no portals** and no multiple summoned swords. | **RAW VISUAL APPROVED** | icy_teleportation_slash_emblem.png |
| **Sapphire Command** | **///** three well-separated, forceful diagonal crystalline cuts; deliberate precision, not Blue Crimson's motion blur. | **RAW VISUAL APPROVED** | glacial_crystal_claw_slashes.png |
| **Ice Shackles** | **X** massive frozen chains closing around a small central binding seal; unmistakable restraint, not a snowflake. | **RAW VISUAL APPROVED** | a_high_detail_fantasy_sci_fi_icy_magic_emblem_scen.png |
| **Icebound Might** | **Broad guardian armor**: towering crystalline shoulder plates, heavy protective gauntlets and intense chakra chest core; **no actor inside**. | **RAW VISUAL APPROVED** | 1000018410.png (actual bytes JPEG) |
| **Quintessential Flake** | Distinct **six-point crystalline flake** with inward-converging chakra; no guardian armor or extra starburst competing for focus. | **RAW VISUAL APPROVED** (2026-10-14) | 1000018420.png (attachment decodes as JPEG; generation-original source pending) |
| **Arctic Frost** | One sweeping **crescent** from ice-coated Blue Blade, a single decisive cut; not three gashes or speed afterimages. | **REWORK REQUIRED — NOT APPROVED** (director correction, 2026-10-14) | 1000018419.png (rejected visual candidate; historical draft, not approved export) |
| **Blade Resonance** | Single **vertical Blue Blade** with three clean concentric chakra resonance waves; calm central axis; no large slash explosion. | **REWORK REQUIRED — NOT APPROVED** (director correction, 2026-10-14) | 1000018418.png (rejected visual candidate; historical draft, not approved export) |
| **Glacial Volley** | Strong horizontal/diagonal **fan of crystalline lances** fired in formation; discrete, directional projectiles rather than parallel slashes. | **RAW VISUAL APPROVED** (2026-10-14) | 1000018412.png (user attachment; JPEG content; original isolated-session export pending) |

**Approval distinction:** **Six** entries are director RAW VISUAL APPROVED; **Arctic Frost and Blade Resonance are NOT APPROVED**. Previous studio approval labels were explicitly corrected by the director. Technical compression success on their old drafts does not change artistic status or make the eight-pack ready. The user retains final acceptance.

## Director rework correction — 2026-10-14

Director clarifies that **Arctic Frost** and **Blade Resonance** **were not approved**: both insufficiently communicate their individual jutsu and feel out of place in the family. Do not reinterpret "looks good" / "took some doing" in older conversation turns as operative approval after this explicit correction. Previous processed drafts are retained only for traceability; **no regeneration or image replacement is authorized in the Art Studio**. Use new isolated generation sessions after deciding clearer concepts, then seek explicit individual approvals.

This correction does **not** withdraw raw visual approval from Blue Crimson, Sapphire Command, Ice Shackles, Icebound Might, Glacial Volley or Quintessential Flake.

## Eight-icon processing pass — 2026-10-14

All eight previous candidate source attachments were processed to **256x256 RGB opaque full-bleed lossless WebP**, using Pillow LANCZOS resizing and 256-color MEDIANCUT without dithering. Full RGB at 256px exceeded 80,000 bytes; this color reduction keeps all eight under the director's stricter cap while retaining dimensions. Source and export hashes, precise bytes, codec checks, verified ZIP metadata and source flags: [PROCESSING_QC_20261014.json](PROCESSING_QC_20261014.json).

The studio visually inspected the eight-icon family at **256/125/64/32px**, but the director has since **rejected Arctic Frost and Blade Resonance on visual/jutsu-fit grounds**. Their previous exports are historical drafts **excluded from any final delivery**. The other six remain visually approved and processed-export acceptance remains pending. The generic ICON artpreflight alpha contract remains incompatible with this director-approved opaque-background presentation and was **not invoked** in this pass. Do not represent mechanical preflight as passed. This repository change commits only documentation and evidence, not binary images.

## Reference selection per new icon

For an isolated generation, attach only one or two **individual** files from a trusted/available source. Recommended default: the approved Ice Shackles icon as **style/material-only**, with an optional specifically relevant Blue Blade weapon as **subject-only** when the jutsu actually needs a sword. The generator must not copy the X-chain composition. If Ice Shackles is unavailable as source bytes, provide a different personally approved individual exemplar; do not claim a URL was visually ingested.

Never attach all eight icons, a montage, the failed Icebound snowflake/three-slash attempts, or a previous jutsu generation transcript. Pass the other icons' used silhouettes as **text exclusions**, not as image-conditioning subjects.

## Durable evidence/status rules

- **RAW VISUAL APPROVED:** user accepted the raw composition; preserve original bytes/hash.
- **GIT SOURCE PINNED:** source file is committed and hash-matched at an immutable repo SHA; currently **none** of the six approved (or two rejected historical) images meet this gate.
- **PROCESSING QC PASSED:** output, visual scale, size/format and source integrity actually checked.
- **PREFLIGHT CLEAR:** the correct current repository tool exits with zero errors; **not claimed** for opaque BBE jutsu icons.
- **UPLOAD / LIVE VERIFIED:** must be supported by the operator's upload and fresh live read-back; **none** claimed.

Do not erase this history when replacing an output; use a new filename/version, document replacement approval and preserve predecessor evidence.

## Next studio actions

1. Preserve the six accepted source images and the two rejected drafts as separately labeled historical evidence; source and processed binaries remain conversation files, not Git-tracked binaries.
2. **Redesign Arctic Frost and Blade Resonance in isolated per-jutsu generation sessions, one at a time.** The studio should revisit the connection between actual jutsu actions, correct Blue Blade weapon curvature, palette and distinctive silhouette. No new design is approved by this status correction.
3. **Do not deliver the existing eight-icon ZIP as final.** It contains the two rejected drafts. After replacement and new explicit director visual approval, process only the accepted sources; recheck 125/64/32px family distinction, size/format and exact source hashes. The shared-ICON preflight alpha mismatch remains unresolved and cannot be reported as a green canonical preflight.
4. Request separate Fable Lane A implementation of **jutsu-specific opaque-background contract/preflight handling** before claiming mechanically clean upload packages.
5. Keep any actual game upload, content changes, and publication under dauntless's separate authority.
