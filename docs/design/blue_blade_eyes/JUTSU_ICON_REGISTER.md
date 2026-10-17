# Blue Blade Eyes — Jutsu Icon Identity Register

**Status:** **COLLECTION CLOSED — 8/8 DIRECTOR VISUALLY APPROVED, 2026-10-17.** Exact final source files and opaque 256×256 lossless WebP exports have been verified and delivered as a conversation ZIP; eight encoded outputs and corresponding SHA-256/byte/codec evidence are recorded in FINAL_EXPORT_QC_20261017.json. This Git branch records the evidence only, **not the image binaries**. Canonical artpreflight.py was not executed in this container, and no live-game upload or read-back was performed by this workstream.  
**Art Studio:** docs/workflows/ISOLATED_ART_GENERATION.md; director ruling RUL-2026-10-14-001.  
**Source basis:** director-provided jutsu database screenshots and approved image-generation outputs in the 2026-10-13/14 conversation. The screenshots document the names/visual meaning; they are **not** a current live capture.  
**Source bytes:** eight director-approved source identities, decoded formats, exact dimensions and SHA-256 values are in SOURCE_EVIDENCE.json. The source backup and processed ZIPs are conversation deliverables, **not committed Git binaries**.  
**Separate workstream:** the older BBE Foundation/Hidden Art/Advanced Art *Bloodright emblem* work at chatgpt/bloodright-icon-production-tracker-20261008 is **not part of this eight-jutsu icon set**. Do not edit or re-approve the existing BBE bloodline artwork here.

## Collection-wide visual lock

- **Palette:** frosted icy white, pale cyan, pale glacial-blue crystalline chakra; deep sapphire only for focused contrast and silhouette gaps.
- **Material:** semi-translucent faceted ice, white-fracture highlights, selective pixel-detailed edges, luminous sapphire interiors, restrained frost haze.
- **Composition:** one dominant technique-specific silhouette, one supporting effect, clear direction/negative space, high contrast at small sizes; the family shares **rendering and palette, not layouts**.
- **Ninja/chakra:** express the actual technique (speed afterimages, precision cutting, binding, resonance, protection, aimed volleys); no obligatory circular seal or eye emblem.
- **Background:** full-bleed designed icy/sapphire atmosphere for jutsu icons; **opaque presentation approved, transparency not required**. Do not fake transparency. Preflight against the spec's JUTSU_ICON target, which accepts opaque RGB (see protocol §5).
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
| **Quintessential Flake** | Distinct **six-point crystalline flake** with inward-converging chakra; no guardian armor or extra starburst competing for focus. | **RAW VISUAL APPROVED** | 1000018420.png (decoded JPEG; exact SHA in SOURCE_EVIDENCE.json) |
| **Arctic Frost** | One sweeping **crescent** from ice-coated Blue Blade, a single decisive cut; not three gashes or speed afterimages. | **RAW VISUAL APPROVED — replacement** (director explicit) | crescent_iceblade_arc.png (final higher-contrast revision, not the old washed-out image) |
| **Blade Resonance** | Single **vertical Blue Blade** with three clean concentric chakra resonance waves; calm central axis; no large slash explosion. | **RAW VISUAL APPROVED — replacement** | resonant_blue_ice_katana.png (final approved replacement, not earlier rejected sword) |
| **Glacial Volley** | Strong horizontal/diagonal **fan of crystalline lances** fired in formation; discrete, directional projectiles rather than parallel slashes. | **RAW VISUAL APPROVED** | 1000018412.png (decoded JPEG; exact SHA in SOURCE_EVIDENCE.json) |

**Approval distinction:** All eight specific visual sources are director-approved, including revised Blade Resonance and Arctic Frost. The eight processed outputs were checked for size, codec, reproduction, and 125/64/32px distinguishability, but **formal artpreflight and external live-game upload/read-back are separate gates**. Do not confuse source, export, preflight, and live publication states.

## Reference selection per new icon

For an isolated generation, attach only one or two **individual** files from a trusted/available source. Recommended default: the approved Ice Shackles icon as **style/material-only**, with an optional specifically relevant Blue Blade weapon as **subject-only** when the jutsu actually needs a sword. The generator must not copy the X-chain composition. If Ice Shackles is unavailable as source bytes, provide a different personally approved individual exemplar; do not claim a URL was visually ingested.

Never attach all eight icons, a montage, the failed Icebound snowflake/three-slash attempts, or a previous jutsu generation transcript. Pass the other icons' used silhouettes as **text exclusions**, not as image-conditioning subjects.

## Durable evidence/status rules

- **RAW VISUAL APPROVED:** user accepted the raw composition; preserve original bytes/hash.
- **GIT SOURCE PINNED:** a source file is committed and hash-matched at an immutable repo SHA; **none of these eight originals are committed**. Exact source hashes and conversation archives are recorded for portable verification.
- **PROCESSING QC PASSED:** output, visual scale, size/format and source integrity actually checked.
- **PREFLIGHT CLEAR:** `artpreflight.py --type JUTSU_ICON --max-bytes 80000` exits with zero errors on the actual export; **not claimed here**, because the official script was not run in this runtime. Main's JUTSU_ICON spec accepts opaque RGB, and equivalent file-level constraints were independently checked.
- **UPLOAD / LIVE VERIFIED:** must be supported by the operator's upload and fresh live read-back; **none** claimed.

Do not erase this history when replacing an output; use a new filename/version, document replacement approval and preserve predecessor evidence.

## Closure

Closed 2026-10-17 with **eight visual approvals and a complete portable 8-file export**. The final binary ZIP is `BBE_Jutsu_Icons_Final_20261017.zip` (SHA-256 `595ff010ef7b7e147ee88f36840d72fda17f216cc1c333667bd843de00d8e960`) and the approved source backup is `BBE_Jutsu_Approved_Originals_20261017.zip` (SHA-256 `e06ff9d9d9f9dd6110f4926e574c1165fb5169774d081add5c1ffc92ba1b2b65`). Both are **conversation artifacts, not Git blobs**. Exact byte and source/output verification: FINAL_EXPORT_QC_20261017.json; durable closeout: FINAL_ART_CLOSEOUT_20261017.md. Official `artpreflight.py` execution and any live upload/read-back are **not represented as completed** by this session.
