# Bloodline Jutsu Icon Family Showcase — deterministic QC/presentation

**Status:** ACTIVE specialised presentation workflow (RUL-2026-10-17-020; D4 under RUL-2026-10-19-005). The operative acceptance and exact-pixel rules are **`docs/workflows/ISOLATED_ART_GENERATION.md` §4a (P0 F, RUL-2026-10-19-003)**; this document routes their *mechanical application*, not a new art or acceptance rule. P1 Option B implementation is `skills/producing-tnr-art/scripts/jutsu_studio.py` (PR #66); its current code and art spec govern executable details.
**Scope:** `jutsu.image` technique-replacement family reviews. Not a fixed Bloodright tier-emblem showcase, in-game `@img` asset, game upload or publication.

## Input and provenance

Verify the exact **N/N** current jutsu ID/name roster, **N/N separately director-approved raw bytes** (originals preserved) and **N/N matching processed WebP bytes**. Compare source/export SHA-256s, actual decoder/VP8L/dimensions, withdrawn versions and current preflight evidence in the Art Studio ledger. Do not invent missing members, substitute a historical name-only ID mapping, use a prior superseded raw, or treat a ZIP manifest as a live capture.

An incomplete collection may be shown only as a clearly **DRAFT** internal review aid under the P0 rule. **The P1 CLI intentionally refuses incomplete N/N finalization** (partial DRAFT composition is unimplemented Option C); never present a partial image as accepted final evidence.

## Layout / compositor (D5)

The compositor uses equal square presentation tiles, neutral gutters and a consistent text-caption band with **exact names and actual exported bytes/1000 in decimal kB to one decimal**. Only recorded resampling of the exact export pixels is permitted; do not regenerate, retouch or replace accepted icon art. The game WebPs are unmodified by presentation resizing. The count-to-row decision (RUL-2026-10-19-005 D5) is:

| N | Row lengths |
| --- | --- |
| 1–3 | one row of N |
| 4 | 2+2 |
| 5 | **3+2 centered** |
| 6 | 3+3 |
| 7 | 4+3 centered |
| 8 | **4+4** |
| 9 | 3+3+3 |
| N ≥ 10 | `ceil(N/4)` balanced rows, each ≤4, longer rows first (10=**4+3+3**, 11=**4+4+3**, 12=4+4+4, 13=**4+3+3+3**) |

The `grid_rows()` function in `jutsu_studio.py` implements that table (it is **not** a CLI subcommand); `audit-gallery` refuses nonconforming layouts as **INVALID** even when it separately reports their source pixels `FAITHFUL`. Historical BEE 8-tile 1536×854 and Vaporia 5-tile 1156×854 canvases are **examples**, not mandatory output sizes. Do not force five icons into an eight-icon sheet.

## Mechanical output and external audit

Use `jutsu_studio.py finalize APPROVED.json --out DIR [--label v1] [--source-index PATH] [--locks PATH] [--attempts PATH]` only after N/N approvals. It produces a deterministic full-resolution PNG, phone preview, 125/64/32 family QC composite and `showcase/showcase_manifest.json` alongside exact exported WebPs. The tool verifies the written PNG's **decoded tile pixels** against verified exported WebP resizes and checks captions, row positions, gutters, layout and the gallery's members commitment.

~~~sh
python3 skills/producing-tnr-art/scripts/jutsu_studio.py audit-gallery WORK/final/showcase/<fam>_jutsu_showcase_v1.png --manifest WORK/final/showcase/showcase_manifest.json --exports WORK/final/exports
~~~

`audit-gallery` returns `VALID` or `INVALID` relative to the **supplied manifest and exact export bytes**. It reports `pixel_fidelity` and `layout` separately for archival diagnosis. A `VALID` audit is **not** independent proof of a director approval, valid source-history mapping, canonical preflight, game binding or upload. Pin the approved manifest and output hashes; a generatively reconstructed sheet is **INVALID** under P0 even if it resembles approved art.

The companion manifest schema `tnr.jutsu-showcase/1` records: bloodline ID/name, N, ordered jutsu IDs/names, raw/export SHA-256s, export bytes, tile positions, row layout, compositor/resampling/font versions, gallery file + pixel SHAs, mobile/thumbnail QC files, `members_sha256`, separate preflight verdict and director family acceptance state. Output dimensions and file-size captions are derived from actual exports, not guessed raw sizes.

## Exact director acceptance and closeout

After the director accepts the **specific actual gallery**, copy **`gallery.sha256`**, optionally **`gallery.pixels_sha256`**, and **`members_sha256`** from that exact `showcase_manifest.json` into `approved.json.family_acceptance`, with the director's evidence and `status: ACCEPTED`. Re-run `finalize` with a **fresh label** so its write-once archive names do not collide. The tool accepts the prior decision only when the member commitment matches **and** the gallery file SHA or decoded-pixel SHA matches within the same hash domain. Any source raw **or export byte change** invalidates prior family acceptance even if the gallery pixels are visually unchanged.

An Art Studio may close with `FAMILY_SHOWCASE_ACCEPTED: PENDING`; that does not override missing preflight or upload gates. `CANONICAL_PREFLIGHT` is separately PASS/NOT_RUN/NON_CANONICAL/FAIL and is only canonical when `artpreflight.py` and the art spec match `data/preflight_pins.json` (D9). For D6 the flat WebP ZIP name is `<fam>_jutsu_icons_webps_PREFLIGHT_<VERDICT>_<N>webp_<label>.zip`, never an “upload” ZIP. No version of the gallery, thumbnail QC or full closeout ZIP is a game `@img` file. Live operations remain exclusively the user's.
