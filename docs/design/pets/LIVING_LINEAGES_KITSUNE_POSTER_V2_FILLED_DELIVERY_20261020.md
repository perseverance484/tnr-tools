# Living Lineages — Kitsune V2 source-filled concept poster delivery

**Date:** 2026-10-20. **Owner:** ChatGPT Art Director/Image Production workdesk.  
**State:** **V2 STRUCTURE DIRECTOR-APPROVED; 19 EXACT-ORIGIN SOURCE IMAGES INSERTED; FILLED POSTER AWAITS FINAL DIRECTOR VISUAL ACCEPTANCE.**  
**This is a visual proof of concept, not game-generator behavior evidence or a production-asset export.**

## Approved narrative and fixed layout

User decision: **“Structure approved. Insert images.”** This accepts the reference-first **V2** composition previously shown as the 2048×1980 structural preview (the older V1 template is retained as historical accepted layout). The V2 flow is:

1. One **juvenile species reference** (shown only once) → **Player selects Palette / Characteristic / Aura** → **four separately generated, explicitly labeled EXAMPLE Rank 1 companions** (Ember, Moonlit, Jade, Obsidian), each with its actual catalogue choices printed.
2. Four independent **Rank 1 Companion → Rank 2 Scout → Rank 3 Tracker** progressions, with the proposed inheritance rule **own previous image**, not species base or another player's image.
3. One **Ember Rank 1–9** evolution example: **Growth R1–4**, then **Metamorphosis/developed forms R5–9**; milestones **Rank 5 Hunter, Rank 7 Sentinel, Rank 9 Sovereign**. Rank 10 outside scope.

The V2 template retains all textual and layout geometry; replacing art-placeholder child nodes with source-derived image placements changed **no visible headings, cards, labels, stage rows or spatial coordinates**. Only nonvisual SVG metadata/accessibility text and art layers changed.

## Finished composition and available conversation artifacts

| Delivered file | Verified SHA-256 | Bytes | Purpose |
| --- | --- | ---: | --- |
| `TNR_Living_Lineages_Kitsune_Concept_Flow_Structural_V2_20261020.svg` | `af59059ec42d6c4768a8eea70e315b897f43a58f2a5f20e95c7dba34ebaf0969` | 39040 | Exact director-approved V2 structural input; no animal source images embedded. |
| `TNR_Living_Lineages_Kitsune_Poster_V2_FILLED_20261020.svg` | `09c59f759ed3c7a33c408cba39232feff6eddeb02546fe7f2fc2478496d6cb00` | 9103938 | **Self-contained editable SVG** with 19 unique source-derived PNGs embedded once in `defs`, reused by 26 `use` placements. |
| `TNR_Living_Lineages_Kitsune_Poster_V2_FILLED_Preview_20261020.png` | `acf5b9454352fb9601495065edbd7109012be78e545a00695e394c57d5505058` | 1266398 | CairoSVG rasterization of the populated SVG, **2048×1980 pixels**. |
| `TNR_Living_Lineages_Kitsune_Poster_V2_FILLED_Sources_20261020.zip` | `347dc2d10b6a5335b3e0b0411e01abebf16ad6911c101586b98f787c93e9b01c` | 22009228 | **46 entry** source archive: 19 original JPEGs + 19 presentation PNG cutouts + self-contained SVG + PNG preview + exact V2 structure/layout map + manifest + README + reproducibility Python script/instructions. |
| `TNR_Living_Lineages_Kitsune_Poster_V2_FILLED_Manifest_20261020.json` | Manifest is also inside ZIP, with 19 original and presentation-derivative hashes and **26 slot-to-source bindings** | — | Exact provenance and repeat-source record. |

**Distribution:** These are **conversation artifacts** available with this workdesk, **not committed raster or SVG binary assets to the repository**. The branch stores direction, the V2 geometric slot map, approval status and source hashes; source originals are preserved in the ZIP. Do not invent Git paths to binaries that were not committed. Production policy keeps finished presentation binaries out of Git.

## Source fidelity / non-generative composition

Each unique source is a **real original image submitted in this project**, not a generated reconstruction or a cropped thumbnail from the old reference poster. The original 19 JPEG byte strings have been hashed and read back individually from the ZIP. Source upload filenames misleadingly ended `.png` despite actual JPEG/RGB data.

The poster **only** applies a deterministic presentation-layer external black-background cutout: threshold connected near-black boundary pixels (`max(R,G,B) ≤ 16`), 3px edge softening, original-content crop, transparent padding, 512×512 RGBA LANCZOS preview resample. There is **no art repainting or generative step**. All **19 original full-resolution JPEGs** remain immutable separately in ZIP. Every repeated use of an asset ID shares the **same exact encoded cutout** through `defs`/`use` in the editable SVG. The appearance of silhouette highlights and effects is from the saved originals.

| Slot ID | Exact original SHA-256 |
| --- | --- |
| `SPECIES_REF` | `8b32ed6bb9ba4ea919fb18812fbdece4a845c49ec6a3c85a45610ec022c59dc9` |
| `A_R01` | `b49354012e173291b415383cf4aca91942d921297041e232d9ef3dd057058470` |
| `A_R02` | `d2c030e448dc023336e67c6eb4dc61ba4f5aeafc16982c0429b45821f9cca977` |
| `A_R03` | `55c2ec175c02229a89f4a80cbc92bc555f5f03a5a473ade63f33e01cb881fd28` |
| `A_R04` | `b28a7cd75499bf768000c474f4296a24edfa908c3b12b4abb85ecbcfcabe903f` |
| `A_R05` | `434b736f5e7188ac7be2eac92824f599de61cf2eec3a3c0d9ca03b65dad10034` |
| `A_R06` | `db2ebeb7562e1b0e8a1f431ecc0c55a93c33122d352f3553c862c6bac7aed8d3` |
| `A_R07` | `147e8f9cea6b2f1bd467f0dcba76546365d2832cf38ef02420b74f320edb5dd4` |
| `A_R08` | `c2858de46ace5bf1f5391741cc370af7ea6c91c0f47b1b59b06cd9774c774817` |
| `A_R09` | `b69899a1072ede47dd19b2219bb50d0e92131c58b4b3d154e6603b510e8e23ba` |
| `B_R01` | `f42524d1be91e8e92dee9ae4bd2140374907431c2ee431621f36cf84dc5619b1` |
| `B_R02` | `b31168d0de30371e8df214f43bf7532e908949d5b3cc1ea161974a154e746172` |
| `B_R03` | `b0868310f64f17be067f8352001b2f2105db707770fbc0c4ae0c5467dcae058b` |
| `C_R01` | `c240b7f610e4d8c50281b99eb7512e89867d749e4229e80804e0b2652af2b378` |
| `C_R02` | `cdc25cc257054c0fbe030ee1683f88f4ae0b6486933d6dd124de1b8d8e60ab4c` |
| `C_R03` | `dc67a0a1549c5af25c3e41f5b3311a69fdd2b26a2971b663009b37728e5e4c2f` |
| `D_R01` | `440ba5c866f74a21ba0d46654e3b2f6b7cc21fb1dd1c7dcdb69db2be11d6849b` |
| `D_R02` | `70c541d0b0a3e6167f60bf5b5c5edf77a18983223dd2976ac3ad9f997db8278b` |
| `D_R03` | `20ce9623607b6e1aef6e143003b88162036605b0bb7c7bd77b8af79ab1a27602` |

## Resolved missing Obsidian individual originals

Director later supplied **two standalone images** after the earlier single `1000018915.png` two-fox composite:
- **D_R02 Scout:** `1000018916.png` = original JPEG RGB 1536×1475, SHA-256 `70c541d0b0a3e6167f60bf5b5c5edf77a18983223dd2976ac3ad9f997db8278b`, shown as a yearling with two distinct tails.
- **D_R03 Tracker:** `1000018917.png` = original JPEG RGB 1536×1536, SHA-256 `20ce9623607b6e1aef6e143003b88162036605b0bb7c7bd77b8af79ab1a27602`, shown in a lower agile pose with three tails.

Both originals are used **directly** as distinct source inputs for their respective V2 poster slots; the old paired composite is **NOT** used. The prior composite-only limitation in the historic intake record is resolved, and no split/crop from that earlier composite was necessary.

## Verified local delivery checks

- Exactly **19 unique original source SHA-256** matches, 19 original images decode JPEG/RGB, true dimensions recorded and full source bytes preserved.
- Exactly **19 embedded source-derived PNG images**, each with a unique art ID and alpha channel, each reused only by SVG `use`.
- Exactly **26** placed SVG art nodes, every slot maps 1:1 to a V2 slot-map entry and source hash; one **SPECIES_REF** display, four player outputs, four × three lineage displays, nine Ember ranks.
- No image-generation compositing; XML reparses, SVG renders to PNG at **2048×1980** with CairoSVG; original artwork is never reconstructed.
- ZIP CRC and all 19 original/19 cutout hashes verified by readback; inclusion of script and full original structural layout supports independent reproduction.
- No live-game requests, player image attempts, credentials, asset uploads, production preflight or publication.

## Acceptance distinctions / remaining gates

**Layout:** DIRECTOR-APPROVED V2 structure.  
**Poster placement:** DIRECTOR-AUTHORIZED; **DONE for all 26 positions**; Obsidian standalone sources resolved.  
**Original artwork:** The previously explicitly approved group is species base and four Rank 1 founders (**5 originals**). The eight Ember R2–9, four Moonlit/Jade R2–3 and two standalone Obsidian R2–3 illustrations are **selected for the filled poster** but their independent visual-batch approvals/actual model image-to-image chaining were never source-proven; do not rewrite historical source status as `APPROVED` without a director decision.  
**Whole populated poster:** **PENDING DIRECTOR VISUAL REVIEW** of the actual filled SVG/PNG.  
**Game upload readiness:** **NOT CLAIMED**: original sources are opaque JPEG; 512px derivatives are poster-only and have not passed the TNR art pipeline or engine/client validation.

**Next step:** Show filled preview, obtain the director's final poster acceptance or specific refinements, preserve source/derivative hashes. The actual proposed reference + player choice + rank-conditioning product still requires Fable's future reviewed implementation and is not proven to be present in the live game.
