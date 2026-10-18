# Bloodright Wave 06 — BR-040 Kyuko-sei Collapsed Amber V03 Proposal

**Status:** Four-family wave ART MATERIAL DIRECTION APPROVED; **BR-040 three specific images newly PRODUCED/PROPOSED, not yet director artwork-approved**. Last Wave06 bloodline. No field-specific `skillTree.image` preflight / Forge / game operations.
**Date:** 2026-10-18 · **Roles:** Image Production lead; Art Director supporting.
**Repository lineage:** `perseverance484/tnr-tools`, `chatgpt/bloodright-wave06-art-studio-20261018`; Wave05 art parent `5512aa0e8faad6153e13122c262e5277e58c6a08` (not integrated with main).

## Pinned original art and visual direction

**BR-040 Kyuko-sei**, A-rank, Dust, bloodline ID `Y10fxyLR39IBJ3ICkAdEp`. User-supplied `BR-040_Kyuko_sei.zip` SHA-256 **`9495e293e976a1b3bcc507972360363180516d5729b4f279c8b3e9dff68d466c`**. Verified actual five CDN-served jutsu images + identity against manifest SHA-256/dimensions/IDs, safe ZIP paths and CRC. Original image identity is captured CDN rendition, not proven original uploader bytes and not a new game capture.

**Individual jutsu images visually inspected:** Temporal Erosion `g3wqcN_BzdSprujUBN84p`; Singularity `7GGmPc5Sbp3JSeHGYgaJV`; Ethereal Particle Storm `IKv0cRCVTFpFCCEbAbuA7`; Abysmal End `IBzUgEsvppitn8MILT4tV`, plus bloodline identity `Y10fxyLR39IBJ3ICkAdEp`. Source imagery predominantly shows bright bronze/ochre-grained dust, charged compacted sandstone and gravitational concentration with sparing pale ivory energy. Distinct from Aerathiel's bright blue/seafoam/ivory microdust, and from Tenohira Musei's dual blue/orange split.

**Approved material direction:** **Collapsed Amber**, derived from actual original references. V03 is **weathered antique ochre/amber bronze over ashen sandstone with mineral speckling**, rather than luminous explosion orange or soft pale peach. Two private internal color tests V01/V02 and a lower-intensity V04 exploration were **NOT presented and are NOT approved**. V03 is the first candidate presented for director review, selected to preserve **exact full-master pixel intensities** rather than V04's nonexact altered brightness. Do not substitute an internal exploration for v03.

## Geometry and production evidence

**Universal tier geometry** from the operator-approved `Bloodright_Wave06_Production_Starter_20261018.zip`, SHA-256 `9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`. The script applies new material-color patterns only **inside each approved 1254px individual tier master** with every output pixel's `max(R,G,B)` equal to the source master, including **nine exact threshold masks per tier (1/8/16/32/64/128/192/240/254)**. Foundation remains outer+inner diamond, Hidden Art paired crescents, Advanced Art exact multipoint starburst, all opaque solid black/no new outer geometry. Decorative glow is entirely bounded by original master pixels; never generated from the source contact sheet.

| Tier | Independently saved 1254px RGB PNG SHA-256 | Separate 256px VP8L RGB lossless WebP SHA-256 | WebP bytes | Full geometry |
|---|---|---|---:|---|
| Foundation | `1c2a73378c0d398fda578567577e1b012623610cd8bec4d83070e120edd09931` | `5cf8ee55f96ce65c11a40386561f05384d6df5fe9b541740fc1b727244dd9399` | 41,788 | EXACT |
| Hidden Art | `4ae6f75f9b72e271d4ad183240ae4bc1a6d1fa725d138c4a56e1d0041549122a` | `590cb461845edd9f70311af7f18869f51297a0d4006833a9e0e1cd490dbc7de3` | 67,624 | EXACT |
| Advanced Art | `9b94281ffca74e8a0936e10da4205934a52811d265591cc1ee34dc060d251e05` | `7785787d66e63fffa2b970f4c7626a58cb1f29c1ca6156dcc5a11917eb08f0cf` | 57,950 | EXACT |

**Independent offline validation: 171/171 PASS / zero FAIL** after normalizing the manifest's `jpg` format spelling to Pillow's decoded `JPEG`. Checks included all 5+1 originals' byte SHA and ID, approved master SHA/full per-pixel maxRGB and 27 brightness-threshold masks, three PNG+VP8L lossless 256px raw/WebP decoded pixel equality to intentional Lanczos resized source, strict WebP byte/corner/thumbnail tests at **125/64/32 px**, neighboring director-approved Aerathiel exact raw/WebP binary invariance (six SHA checks), full **six-file deterministic producer replay** from portable original starter ZIP, and all delivered ZIP CRC/member hash checks. [External QC artifact](#portable-artifacts). **No actual field-specific `artpreflight.py` successful run can be inferred** from the offline proof.

## Portable artifacts (exact conversation file bytes; NOT immutable Git art pins)

| Artifact | SHA-256 | Status |
|---|---|---|
| `BR-040_Kyuko_sei_Collapsed_Amber_v03_Proposed_Production_Pack_20261018.zip` (exact reference ZIP, exact original geometry ZIP, source recipe, individual 3 PNG+3 WebP, QC evidence and previews) | `2f470f1e3bb353e5b812781fd3d63f7f66c2ec96bdd9545e17cd4e929e0f4aa6` | Proposal, self-contained/replayable |
| `BR-040_Kyuko_sei_Collapsed_Amber_v03_3_WebPs_PROPOSED_20261018.zip` | `3e7f60376bee29d852daadef9ebafdd035642c94802d863f26c78655aace9e03` | Proposal |
| `BR-040_Kyuko_sei_Collapsed_Amber_Three_Tiers_PROPOSED_HIRES_v03_20261018.png` (programmatic resized raw-PNG showcase) | `05a2e0d6505e185a78ccb7b4bf5ffd503acc6441d5d433b2c9168eab9e56a750` | Review preview, NOT one composite raw |
| `Kyuko_sei_V03_vs_Aerathiel_Tenohira_Comparison.png` (actual accepted/proposed 256px WebP pixels) | `e5f4c8e72463e9f01018c5c1417202b6fdca03b88725d08f2921f3457b8a668a` | Visual contrast check |
| `BR-040_Kyuko_sei_Collapsed_Amber_v03_Offline_QC_20261018.json` | `5db1e3a6a2a2a57b51028fecb54e2225106bc71b55eee4b59cf42902b7279af2` | 171 check ledger |
| `wave06_produce_kyuko_v03.py` | `31cb2df2a5eb4b4d8b6eab665305aca9db0b64a2895b0ee99f819e7232066ea3` | Portable raw/VP8L source recipe |

**Independent originals inside full pack:** `raw_1254/br040_kyuko_sei_{foundation,hidden_art,advanced_art}_collapsed_amber_v03.png` and `webp256/br040_kyuko_sei_{foundation,hidden_art,advanced_art}_collapsed_amber_v03.webp`, six file hashes as table above. Preview sheets are programmatically composed **after** each individual file was saved; no generated collage/source reinterpretation.

## Approval and technical boundaries

**Now:** ask the director to accept/revise the three **specific V03 output images**. If approved, keep all six exact approved hashes immutable; do not regenerate a falsely 'approved' approximation. Only a director response to these images increases Wave06 visual-art totals.

**Status before this approval:** **28/29 families / 84/87 tier designs visually approved**, including a BR-036 Itojinsei Blackwire three-icon depiction in one accepted composite; **27/29 families / 81/87 icons** have individually saved accepted source PNG+WebP pairs. BR-040 is still PROPOSED, so no count increase yet.

**Remaining blockers notwithstanding future artwork signoff:** BR-036 approved Blackwire sheet still requires individually accepted, exact-master-geometry/byte-QC source and separate exports; 12 previous visually accepted Wave04/05 emblems failed strict original master geometry, retained as accepted visually only; `skillTree.image` actual field-specific opaque-alpha mechanics unverified; Git binary source pins/immutable Forge imagePack and art-lineage RUL-ID collision with newer `main` unaddressed. **0 live-game requests/writes; no credentials.**
