# Independent Review — PR #41 BBE Jutsu Icon Final Closeout

**Date:** 2026-10-17  
**Lead:** Engineering Auditor · **Supporting lens:** Art Director / Image Production (approval provenance and closure, not new art acceptance)  
**Repository:** `perseverance484/tnr-tools`  
**Review target:** PR #41, `chatgpt/bbe-final-export-closeout-20261017@e5aa3b13eb4896e93b3e85799b8f0ec2eaedeb9f` (**FROZEN**)  
**Base/merge-base:** `8c434dfeb3233dd3b3f68410c8361bc9e39ba061`  
**Main independently verified:** `9a0970002a80531078ac5e4b0f72578d3f7855f5` (three commits ahead of base; changed files do **not** overlap this PR's four documentation files)  
**PR state:** OPEN, not merged; GitHub reports mergeable at review time.  
**Verdict:** **PASS WITH NOTES — safe to integrate as a documentation-only closeout.** This is **NOT** an independent certification of unprovided binary ZIP contents or upload readiness.

## Reviewed scope

Exactly four changed files (no scripts, game content, image binaries or live manifests):

- `docs/design/blue_blade_eyes/FINAL_ART_CLOSEOUT_20261017.md` — 8/8 director acceptance, two corrected source variants, claimed local export/QC, explicit unavailable gates.
- `docs/design/blue_blade_eyes/FINAL_EXPORT_QC_20261017.json` — eight final processed WebP identities/byte hashes, source links, caps and ZIP identities.
- `docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md` — updated current 8/8 approved status, source cues and closure; Bloodright tier emblems remain outside scope.
- `docs/design/blue_blade_eyes/SOURCE_EVIDENCE.json` — all eight accepted original source identities, decoded formats, SHAs and source-ZIP fingerprint.

The previous main register represented the original conversation finish but only four directly documented raw approvals and no final export evidence. This PR repairs that historical projection without asserting that the binary originals were committed to Git.

## Independently verified documentary invariants

1. **Target and ancestry:** exact remote branch SHA equals the handoff SHA. PR #41 remains OPEN, no merge; comparing base to head yields the four files above, with no changed-path overlap against current main. No tool/code/runtime dependency introduced.
2. **Exact roster:** pinned `fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866` `docs/design/bloodright/kits/blue_blade_eyes.json` has **eight public jutsu**. The eight final QC jutsu names match that set exactly, with no duplicate or omitted name.
3. **Source/output joins:** each of eight final QC rows has a corresponding `SOURCE_EVIDENCE.json` row under the same jutsu name, and the exact source filename and SHA-256 agree for **8/8**. Source rows contain 8 unique names, output rows 8 unique names / 8 unique filenames, and each documented SHA-256 string is well formed. The `FINAL_ART_CLOSEOUT` and `JUTSU_ICON_REGISTER` distinguish the final approved **Blade Resonance** (`resonant_blue_ice_katana.png`) and **Arctic Frost** (`crescent_iceblade_arc.png`) from their rejected predecessors.
4. **Byte-limit arithmetic:** all eight reported processed sizes are **strictly below 80,000 bytes**. Independently recomputed minimum **59,408**, maximum **63,010**, sum **487,772 bytes**. The declared ZIP **497,338 bytes** leaves 9,566 bytes for archive overhead and manifest, which is plausible but cannot be independently proven without the ZIP. Declared ZIP SHA-256: `595ff010ef7b7e147ee88f36840d72fda17f216cc1c333667bd843de00d8e960`.
5. **Current technical rule:** current main's `25x_DATA_art_spec.json` `JUTSU_ICON` target applies to `jutsu.image`, permits opaque RGB via explicit optional alpha, and retains square/lossless-WebP/460,800-byte generic working specification. The BBE-specific **under 80,000 bytes** limit is stricter and is correctly expressed by `artpreflight.py --type JUTSU_ICON --max-bytes 80000`. The PR does not accidentally apply BBE's cap to BEE or other collections.
6. **Honest gates:** the final closeout, QC ledger and current register explicitly mark official `artpreflight.py` as **NOT RUN**; the source ledger identifies conversation-only originals rather than Git binary pins. They expressly do **not** equate documented file-level local checks to an official preflight PASS, Git-immutable art, operator upload, live read-back or publication. The user's prior BBE approval and the documentation update are therefore not represented as game operations.
7. **Decoded source provenance:** the three legacy `.png` filenames actually containing JPEG bytes remain labeled by **detected format**, not misdescribed as PNG pixels. Exact preserved-source checking is claimed as local author evidence, pending artifact independently being supplied.

## Notes / next conditions (not blockers for a docs-only PR)

**N1 — Image mapping is by jutsu name, not stable jutsu ID.** The eight `FINAL_EXPORT_QC_20261017.json` rows and source ledger lack `jutsu_id`. Their names independently match the historical pinned kit, but name-only mapping should **not** be used as sufficient evidence for a production `jutsu.image` update. Before Forge/content manifest construction, add or join an exact-ID source-backed binding (confirm against a current full-record capture if current/live IDs matter). The historical kit's exact IDs are:

| Jutsu | Historical jutsu ID |
| --- | --- |
| Blue Crimson | `bxIPWiqiEaCmPYfAysB5a` |
| Sapphire Command | `gIEy7THAZdXgcak5zs5U6` |
| Ice Shackles | `Aff56oo9BFTcoLLeEyOja` |
| Icebound Might | `YGBz7eIDvLwWXSVFEcK9j` |
| Glacial Volley | `Bw2OBS92Xi-4YlfErS632` |
| Blade Resonance | `TFRsEeV-VacukUUop-dtN` |
| Arctic Frost | `0tPhVC7G21Ej99YSICtJO` |
| Quintessential Flake | `dXOjSl1vNp5G5BsFrNPkh` |

**N2 — ZIP bytes were not supplied for this review.** Neither `BBE_Jutsu_Icons_Final_20261017.zip` (expected **497,338 B**, SHA above) nor `BBE_Jutsu_Approved_Originals_20261017.zip` (expected SHA `e06ff9d9d9f9dd6110f4926e574c1165fb5169774d081add5c1ffc92ba1b2b65`) is in this review's mounted files or Git tree. Thus **do not claim independent verification** of archive CRC/member bytes, original hashes/decodes, quantization re-encoding exactness, thumbnail appearances, or an official preflight result. After director supplies the consolidated approved-art ZIP, verify source ZIP fingerprints, all eight member bytes/identities, VP8L codec, 256² dimensions, RGB mode, 125/64/32 previews, and run the **actual** `artpreflight.py --type JUTSU_ICON --max-bytes 80000`. Only then advance the respective technical statuses.

**N3 — Documentation integration ≠ art publication.** PR #41 can merge as a status/evidence update independent of binary intake, without granting Forge art upload authority. Preserve versioned filenames and older rejected variants as history; no accepted image is regenerated. Use the current integrated JUTSU_ICON target, not legacy shared-ICON blocked-alpha statements from older BEE/Vaporia registers.

## Evidence/verification limits

- Independently read full frozen closeout, QC JSON, source JSON and register, plus exact pinned eight-jutsu kit and current main's art spec, current production/isolation/showcase workflows and review authority files.
- Independently checked ID/name set, per-row source SHA join, duplicate-name/file exclusion, SHA syntax, reported byte extrema/strict boundary, current art spec target and main/branch changed-path overlap. These are **source/documentary checks**, **not** actual WebP/ZIP tests.
- The author's **10/10 repo checks, ZIP CRC/reproducibility, exact source-byte hashes and image visual acceptance** are preserved as author/user claims, not silently promoted to independent rerun results.
- No GitHub Actions workflow run was returned for this frozen PR head; no full project code tests are required for the four documentation-only files.
- Browser, deployed game, upload, preflight execution on final WebPs and asset read-back were **not attempted**. Game requests/writes **0/0**; CDN requests **0**; credentials **none**.

**Next:** documentation-only integration is reasonable at frozen SHA after normal maintainer checks. Follow with the user-provided BBE originals/final ZIP, actual canonical preflight, and eventual exact-ID binding verification before any operator-authorized game uploads. For the larger bloodline jutsu-icon studio standardization, collect Vaporia closeout and all approved source/export bundles and reconcile all three families without importing Bloodright tier-emblem behavior.
