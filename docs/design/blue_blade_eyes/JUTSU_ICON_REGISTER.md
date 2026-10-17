# Blue Blade Eyes — Jutsu Icon Identity Register

**Status:** **COLLECTION CLOSED, 2026-10-17.** dauntless reports the BBE jutsu-icon set finished. The final exports, preflight records and uploads were done outside repository tracking and are **not held here**. The rows below are the last repository-recorded state, kept as history and as the protocol's worked example; do not read them as current per-icon status.  
**Art Studio:** docs/workflows/ISOLATED_ART_GENERATION.md; director ruling RUL-2026-10-14-001.  
**Source basis:** director-provided jutsu database screenshots and approved image-generation outputs in the 2026-10-13/14 conversation. The screenshots document the names/visual meaning; they are **not** a current live capture.  
**Source bytes:** individual source identifiers, image formats, exact sizes and locally verified SHA-256 are in SOURCE_EVIDENCE.json. Those files are **not committed** in this documentation change.  
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
| **Quintessential Flake** | Distinct **six-point crystalline flake** with inward-converging chakra; no guardian armor or extra starburst competing for focus. | **NEW-METHOD REVIEW PENDING** | Existing earlier candidate(s), not locked here |
| **Arctic Frost** | One sweeping **crescent** from ice-coated Blue Blade, a single decisive cut; not three gashes or speed afterimages. | **NEW-METHOD REVIEW PENDING** | Earlier exploratory candidates; no current raw lock |
| **Blade Resonance** | Single **vertical Blue Blade** with three clean concentric chakra resonance waves; calm central axis; no large slash explosion. | **NEW-METHOD REVIEW PENDING** | Earlier exploratory candidate; no current raw lock |
| **Glacial Volley** | Strong horizontal/diagonal **fan of crystalline lances** fired in formation; discrete, directional projectiles rather than parallel slashes. | **NEW-METHOD REVIEW PENDING** | Earlier exploratory candidate; no current raw lock |

**Approval distinction:** The four marked RAW VISUAL APPROVED are director-accepted *visual subjects*, not approved compressed uploads. Do not call the other four rejected or complete without a new explicit art review. The user retains final acceptance.

## Reference selection per new icon

For an isolated generation, attach only one or two **individual** files from a trusted/available source. Recommended default: the approved Ice Shackles icon as **style/material-only**, with an optional specifically relevant Blue Blade weapon as **subject-only** when the jutsu actually needs a sword. The generator must not copy the X-chain composition. If Ice Shackles is unavailable as source bytes, provide a different personally approved individual exemplar; do not claim a URL was visually ingested.

Never attach all eight icons, a montage, the failed Icebound snowflake/three-slash attempts, or a previous jutsu generation transcript. Pass the other icons' used silhouettes as **text exclusions**, not as image-conditioning subjects.

## Durable evidence/status rules

- **RAW VISUAL APPROVED:** user accepted the raw composition; preserve original bytes/hash.
- **GIT SOURCE PINNED:** source file is committed and hash-matched at an immutable repo SHA; currently **none** of the four approved jutsu image sources meet this gate.
- **PROCESSING QC PASSED:** output, visual scale, size/format and source integrity actually checked.
- **PREFLIGHT CLEAR:** `artpreflight.py --type JUTSU_ICON --max-bytes 80000` exits with zero errors on the actual export; **not yet claimed** for any BBE jutsu icon, because no export has been run through it.
- **UPLOAD / LIVE VERIFIED:** must be supported by the operator's upload and fresh live read-back; **none** claimed.

Do not erase this history when replacing an output; use a new filename/version, document replacement approval and preserve predecessor evidence.

## Closure

Closed 2026-10-17 on dauntless's report. The repository holds the identity register, the four source hashes in SOURCE_EVIDENCE.json and the JUTSU_ICON tooling; it holds no BBE export, preflight record or upload read-back. The four remaining icons were completed by dauntless outside this register. The earlier "next studio actions" list is retired.
