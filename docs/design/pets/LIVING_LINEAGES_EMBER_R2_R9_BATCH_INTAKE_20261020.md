# Ember Kitsune Rank 2–9 — eight-image source intake

**Status:** EIGHT ORIGINALS RECEIVED, mechanically decoded, **BATCH DIRECTOR APPROVAL PENDING**.  
**Date:** 2026-10-20. **Art goal:** visual proof-of-concept only, under RUL-2026-10-20-005 fast-batch exception. **Live requests/writes:** 0. **Credentials:** none.  
**Lead:** Art Director; source/format checks: Image Production.  
**Workdesk initial state:** `chatgpt/living-lineages-kitsune-workdesk-20261020@6b3bbf8f0664b9b2254dc12f55ab546e63604123`. Batch was authorized and entirely ungenerated in the tracker at this head.

## Proven source intake vs unproven generation behavior

The director supplied **eight visually distinct Ember Kitsune images** in a single message (“Here's ember”), apparently in rank order. **Rank assignment follows displayed upload order**, not the numerically unordered uploaded filenames; no separate generation session log or author-produced manifest accompanied the files. All eight originals were decoded from user-supplied files under `/mnt/data` and source SHA-256s calculated from their actual bytes; every one is **1536 × 1536 RGB JPEG**, opaque black background, with an original file display name ending in `.png`. None is yet a transparent production export.

**Verified input R1:** `kitsune_ember_rank1_approved_source_20261020.jpg`, SHA-256 `b49354012e173291b415383cf4aca91942d921297041e232d9ef3dd057058470`, 1536 × 1536 JPEG RGB, already director-approved. This input remains the separate reference of record and is included unchanged with eight outputs in the intake archive.

| Asset | Rank name | User-uploaded filename | Source SHA-256 | Original bytes | Concept tails | Expected immediate parent |
| --- | --- | --- | --- | ---: | ---: | --- |
| `A_R02` | Scout | `1000018905.png` | `d2c030e448dc023336e67c6eb4dc61ba4f5aeafc16982c0429b45821f9cca977` | 323473 | 2 | `A_R01` |
| `A_R03` | Tracker | `1000018904.png` | `55c2ec175c02229a89f4a80cbc92bc555f5f03a5a473ade63f33e01cb881fd28` | 351104 | 3 | `A_R02` |
| `A_R04` | Guardian | `1000018903.png` | `b28a7cd75499bf768000c474f4296a24edfa908c3b12b4abb85ecbcfcabe903f` | 412097 | 3 | `A_R03` |
| `A_R05` | Hunter | `1000018907.png` | `434b736f5e7188ac7be2eac92824f599de61cf2eec3a3c0d9ca03b65dad10034` | 479787 | 4 | `A_R04` |
| `A_R06` | Warden | `1000018908.png` | `db2ebeb7562e1b0e8a1f431ecc0c55a93c33122d352f3553c862c6bac7aed8d3` | 541546 | 5 | `A_R05` |
| `A_R07` | Sentinel | `1000018906.png` | `147e8f9cea6b2f1bd467f0dcba76546365d2832cf38ef02420b74f320edb5dd4` | 557927 | 6 | `A_R06` |
| `A_R08` | Mythic | `1000018909.png` | `c2858de46ace5bf1f5391741cc370af7ea6c91c0f47b1b59b06cd9774c774817` | 593643 | 7 | `A_R07` |
| `A_R09` | Sovereign | `1000018910.png` | `b69899a1072ede47dd19b2219bb50d0e92131c58b4b3d154e6603b510e8e23ba` | 640913 | 8 | `A_R08` |


**Lineage evidence limitation:** The **intended** dependency is R1→R2→R3→R4→R5→R6→R7→R8→R9, and the rank-to-parent mapping is recorded. Actual *generator-side ingestion of each prior output* is **NOT VERIFIED** by the images or order alone, so `used_parent_sha256` remains null in the ledger. Expected parent candidate SHA-256 is recorded separately from approved-parent SHA-256. Do not claim source-proven chained inference from visual similarity.

## Minimal batch-level visual review

- **Visual species/identity:** Eight one-headed quadrupedal foxes with connected native paws, pointed ears, russet/charcoal/amber fur, pale-tipped features and light Wind curls. Ember is consistently recognizable, while fur and poses change organically.
- **Growth:** R2 reads as a leggier yearling; R3 is lower and athletic with a larger tail display; R4 looks more adult and fur-developed.
- **Metamorphosis:** Hunter (R5) introduces stronger angular shoulder fur and richer tail/body mass; Sentinel (R7) stands more erect and imposing; Sovereign (R9) develops an ornate apex fur crest and tail fan. **Caveat:** Later ranks read partly as elaborations of the same fox body design (larger fan/glowing fur), not three unmistakably different anatomical species forms. This is an art-direction tradeoff for the director, **not an automatic rejection under the explicit relaxed-QC instruction**.
- **Tail targets:** Concept curve R2–9 = `2,3,3,4,5,6,7,8`; overlapping late-rank tail fans prevent independently confirming every tail root in a lightweight visual check. Do not record exact anatomical counts as source-proven.
- **Images:** All eight decode without errors, square/full body. No scene, labels or UI embedded. Images have prominent luminous **orange fur streaks increasingly reminiscent of fire**, although pale Wind wisps remain visible. Whether this drift is acceptable is the director's decision; the user explicitly authorized natural variation.
- **QC boundary:** One 3×3 deterministic quicklook places original R1 and eight candidate images at 436px in source order, with rank labels outside each image. It does **not** rebuild or alter the accepted 1536×1024 structural sheet. No raw-to-alpha conversion, preflight or live upload performed.

## Byte-verified portable intake

- **ZIP:** `TNR_Living_Lineages_Ember_R2_R9_Source_Intake_20261020.zip` — exact JPEG bytes for R1–R9 in `images/`, `batch_manifest.json`, short README and deterministic 3×3 preview. **ZIP SHA-256:** `ddb1f6d5ea7fa85585269e27ae1359abe385330a87f25225488cc969841b2a78`; **size:** 6,617,842 bytes; **12 ZIP entries**. Manifest verifies all eight output hashes and their normalized `.jpg` extension; original `.png` filenames are retained as source metadata.
- **Preview:** `TNR_Living_Lineages_Ember_R1_R9_Batch_Review_20261020.png` — SHA-256 `fd14682c43349698619747add6ffee12961af451d4b0f16ee790e23b335fc81b`; source-faithful Pillow LANCZOS preview, **1428×1632** PNG. Preview ≠ the original files.
- These are **conversation artifacts**, not Git-pinned artwork; repository documents contain only hashes, provenance, and presentation contracts.
- The approved structural SVG, layout map and all previously accepted images remain unchanged.

## Next director gate

**Single decision:** Accept **Ember R2–R9 as the complete exploratory illustration batch for the sheet**, or request a specific correction? The workdesk must not set `director_visual_approval=APPROVED` or count these as 8 new approved images without the director's explicit decision. **Before approval: 5/19 approved.** Upon approval: 13/19 approved, with six Moonlit/Jade/Obsidian R2–3 images remaining. Acceptance would be visual-only; JPEG sources and alpha/preflight remain production-unready.

**Source-of-truth:** `LIVING_LINEAGES_KITSUNE_SLOTS_20261020.json` for individual candidate hashes/status; this intake describes the batch and any incompleteness. **Do not claim game-generator behavior proved**, and do not silently override RUL-2026-10-20-005's permission for artistic drift.
