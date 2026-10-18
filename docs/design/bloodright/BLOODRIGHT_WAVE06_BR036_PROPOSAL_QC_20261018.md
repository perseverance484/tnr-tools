# Bloodright Wave 06 — BR-036 Itojinsei Tensionwire Steel v01 Proposal

> **SUPERSEDED — VISUALLY REJECTED by director on 2026-10-18.** The pale V01 three-icon set was too similar to Teno Yuki. The 151 independent checks below remain correct **only as historical mechanical checks on the rejected V01 files**; the director subsequently requested prominent black crossed wires and approved a new, **single composited three-emblem Blackwire visual source**. Canonical revision record: [BLOODRIGHT_WAVE06_BR036_BLACKWIRE_VISUAL_APPROVAL_20261018.md](BLOODRIGHT_WAVE06_BR036_BLACKWIRE_VISUAL_APPROVAL_20261018.md). Do **not** relabel these V01 raw PNG/WebPs approved, claim the Blackwire sheet passed geometry, or confuse the two source files. No revised Ito standalone production exports have been accepted yet.


**State:** Source artwork inspected; **MATERIAL TREATMENT DIRECTOR APPROVED** 2026-10-18, but **THREE SPECIFIC TIER IMAGES PROPOSED, AWAITING DIRECTOR ARTWORK ACCEPTANCE**. No in-game upload/readback or formal field-preflight.
**Lead:** Image Production · **Lens:** Art Director.
**Art branch:** `chatgpt/bloodright-wave06-art-studio-20261018`; Wave05 approved base `5512aa0e8faad6153e13122c262e5277e58c6a08`.

## Source identity and selected material

**BR-036 Itojinsei**, A-rank, 5 source-captured public bloodline jutsu; bloodline ID `j4_9ypNqYq8Ifbqf-9D2r`. Original user-supplied `BR-036_Itojinsei.zip` SHA-256 `1f6ffabce148272301f3f4c5b5f90db720985ce78763e82ea3dcfccbf7218dd0`. The ZIP contains all five jutsu CDN-delivered source images and one bloodline identity image, each verified against its declared SHA, dimensions, ZIP CRC and pinned roster. Source image inspection centered on Iron Web Entrapment, Lightning Threads, Eternal Embrace and identity; see [Wave06 intake](BLOODRIGHT_WAVE06_SOURCE_INTAKE_20261018.md).

**Approved material:** Tensionwire Steel — cool graphite/satin pewter, stretched silver micro-braided filaments within approved diamond/crescent/starburst geometry, discreet blue-white charging at original crossings. Compared against BR-033 Houkyuken Ferroflux (strong scarlet/cyan polarity), accepted Shinrai Ou Whitebolt (electric lightning fissures) and accepted Teno Yuki Winterglass (near-white translucent ice). Ito's proposed v01 is a cool bright **silver-wire metal**; adjacent frost-white resemblance at small sizes remains a visual-judgment call for the director, not a machine-certified distinction. The alternate internal darker v02 was **not selected**; it leaned toward Shinrai's blue-violet register. No jutsu source images were redrawn.

## Exact three original candidates and export QA

Source masters: the actual three director-approved 1254×1254 original Ethereal Monarch tier geometry PNGs from `Bloodright_Wave06_Production_Starter_20261018.zip` SHA `9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`. Deterministic local recipe changes material RGB hue/faceting/filament contrast *only within each original master intensity envelope*: every output pixel's `max(R,G,B)` equals source master's value. All 9 threshold masks (1,8,16,32,64,128,192,240,254) have exact 100% pixel correspondence on all 3 tiers.

| Tier | Raw original PNG SHA-256 | 256px lossless WebP SHA-256 | WebP bytes |
|---|---|---|---:|
| Foundation | `a666e06a6297f69cbea8413235409fcc50f47186224017a1ada5f099136b8ba1` | `7b9594351ea4954f06eeb58316e5fb2a3d43c47be98cb0c87550f46e894813ba` | 40,556 |
| Hidden Art | `ebcdf86cca8b3742f20a4b507cfd6be9c744c5158422c2fd2defe702932e4737` | `b8c47d84d8090f51264f500ce19401b67b241a96e5e394e248bc8a64daf06dd4` | 65,934 |
| Advanced Art | `95784b6d0696a00508d4e69722246b3c747c14f19585e7404b93f9ff86726d23` | `b6982a51eb9ad824f2e8b0b700a383142861e01de597956f2a0a36f235da83d5` | 56,044 |

All three raw originals are actual independently saved **1254px RGB PNG**. All three processed files are separate **256px opaque RGB VP8L lossless WebPs**. Actual decoded WebPs exactly match intentionally Lanczos-resized raw PNGs. Opaque solid-black corners, 125/64/32px visibility, generic ICON 460800-byte reference ceiling, master/roster ZIP hashes, and every earlier approved BR033 source PNG/WebP binary SHA passed. No synthetic alpha or new geometries introduced.

**Independent offline audit: 151 assertions PASS, zero FAIL**, including original-source IDs and six image SHA/CRC/dimensions, three original tier geometry SHA/shape/maxRGB + 27 mask checks, VP8L decoded equality, 125/64/32 previews, source-to-approved BR033 byte preservation, generated comparisons, ZIP membership and per-file byte identity. The included portable Python production recipe was replayed against the packaged original ZIPs and reproduced all **three PNG + three WebP SHA-256 files exactly** on the current runtime. Source provenance is captured CDN-served rendition, not uploader-original bytes.

## Portable proposed artifacts (conversation attachments, NOT immutable Git binary pins)

| Artifact | SHA-256 |
|---|---|
| `BR-036_Itojinsei_Tensionwire_v01_Proposed_Production_Pack_20261018.zip` (source pack, starter/master, replayable recipe, separate PNG/WebPs, QC/preview) | `432edeae44fea1b487e5bd8d9215318440e90110ce9d0268a09c1fbbcfd7f7d7` |
| `BR-036_Itojinsei_Tensionwire_v01_3_WebPs_PROPOSED_20261018.zip` | `bdd02c7d85269bbd06cbe1ea1e752aa232fd8bc576b9fd9c28e87b192a5ebcef` |
| `BR-036_Itojinsei_Tensionwire_Three_Tiers_PROPOSED_v01_20261018.png` (programmatically composed from the **exact separate saved WebP pixels**) | `b5c3bfc65357cd090b7b25a088dfaeae2495bc937f7d8978685265865b716572` |
| `BR-036_Itojinsei_125_64_32_QC_PROPOSED_v01_20261018.png` | `749eb4c03ef3700d70735bb8e1158f72f59db22f9c0d43efc2d2ac088d3ad667` |
| `BR-036_Itojinsei_vs_Houkyuken_Shinrai_Teno_20261018.png` (independent comparator, actual accepted WebP pixels) | `26e247269b7b73370209aeffa6905b7353a2435f9db68e19a665f2a9a893f1bf` |

## Acceptance and outstanding gates

- **BR-033 Houkyuken:** Accepted v02 original trio locked 3/3 and corresponding 3 WebP bytes unchanged. Approved full archive `BR-033_Houkyuken_Ferroflux_v02_Approved_Production_Pack_20261018.zip` SHA `7489f63df227a009ab097c6502302529899c2c0c617aadbf2a34c5abefcbdcb7`; approved three-WebP package SHA `a9a3d858a3c147f6abd39dcdf2dd1576bc1da7314bd427720f853d056c6f8409`. Acceptance record: [BR033 QC](BLOODRIGHT_WAVE06_BR033_PROPOSAL_QC_20261018.md). No approved pixel modified.
- **BR-036 Itojinsei:** Director has approved its Tensionwire material *direction*, NOT any particular raw icon yet. The next step is inspection/visual approval of the linked three-tier v01 review image. Preserve exact raw/export SHA if accepted. If rejected, revise this one family only; do not overwrite the approved BR033 files.
- **Overall visual approval:** **26/29 bloodlines, 78/87 emblems**; **three families/nine emblems** remain, counting this proposed/unapproved Ito trio.
- **Technical gates still OPEN:** `skillTree.image` actual field acceptance and opaque RGB alpha semantics are not verified. Generic `ICON` still expects alpha; no field-specific `artpreflight.py` successful run can be claimed; this ZIP is **NOT upload-ready**. Git binary pin/immutable Forge imagePack/structural five-BP tree integration, 12 previously approved but strict-master-NONEXACT images, and art-branch ruling-ID collision with main remain separate. Production QC is not operator authorization.
- **Live-game requests/writes:** **0/0**. **Credentials:** none.
