# BR-036 Itojinsei — Blackwire Neutral Pewter V04 Three-Tier Art Review

**Date:** 2026-10-18. **Lead:** Image Production; supporting Art Director.
**CURRENT STATUS:** **ALL THREE BLACKWIRE NEUTRAL PEWTER V04 SEPARATE ORIGINAL TIER ARTWORKS DIRECTOR VISUALLY APPROVED** on 2026-10-18: Foundation approved in preceding review, then Hidden Art + Advanced Art approved together in reply “Approved.” All six original source/output SHA-256 files listed below retained byte-identically. **SOURCE MASTER NONZERO-SUPPORT EXACT 3/3, HIGHER-INTENSITY MASKS DELIBERATELY NONEXACT** because of the approved dark black braided-wire internal occlusion. This is artistic signoff and offline-QC, **NOT field-specific preflight or live upload readiness**. Live operations 0/0; no credentials.
**Repo/branch:** `perseverance484/tnr-tools` / `chatgpt/itojinsei-blackwire-finalization-20261018`. Previous Foundation proposal frozen at `bcfddbbe355b8188b4f1345ff1a720983e92991c`; art-lineage base `chatgpt/bee-bloodright-tier-studio-20261018@8b6edf8045b5f51331a7ac3f9c011e8907fe326d`. Do not modify Fable implementation branches.

## Identity, choice and exact original source

Director **explicitly approved the precise neutral pewter / graphite-black braided-wire V04 Foundation** following the latest Source-Geometry-Locked review. This approval of the source support and visually genuine black wires accepts a *limited internal master-brightness-mask exception*: the master black void, outer silhouette and all **nonzero support pixels** are exactly maintained, but dark wire overlays lower brightness at some illuminated source positions. The director's reply is **not** approval of still-unmade Hidden/Advanced images, and not blanket authorization to deviate from the tier silhouette or publish assets. It does **not** certify exact maxRGB/9 brightness masks.

- **Original blackwire visual identities preserved unchanged:** latest approved freehand Foundation `futuristic_blackwire_diamond_emblem.png` SHA `b060ee0f0d715e1946d165da7837c738cf05e2ef330b01fa8d2e72231fbbffeb`, earlier approved combined three-glyph source `metallic_sigils_in_electric_blue.png` SHA `8391780ec142f3f74a77082f3c6ec462d2ae7876893193a05925f9559944542b`. **These are material references, not geometry masters.**
- **Five actual jutsu images plus identity** from original `BR-036_Itojinsei.zip`, SHA `1f6ffabce148272301f3f4c5b5f90db720985ce78763e82ea3dcfccbf7218dd0`, independently SHA/CRC/image decode/manifest validated. Source is captured CDN rendition, not a newly queried live game record.
- **Exact individually saved immutable tier geometry masters** from user `Bloodright_Wave06_Production_Starter_20261018.zip`, SHA `9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`: Foundation `bb3a3e331e5913fa527049980e2738c151b85eb54ef579cd468126b10039cea2`, Hidden `97ac6df359070f885d8d5545060b788bbd8d374fdfd181c90c60976560a213fc`, Advanced `0e97566732f8ade28eedb1b18f77a666b9804f9467198f9574e3757d940cd014`. Source geometry, not generated collage, owns all tier points, arcs, crosspieces and black negative space.

**Production:** the **exact Foundation V04 material recipe was replayed without changes** on both individual Hidden and Advanced high-resolution original tier masks, using the same visually approved monochrome black braided cables over silver/neutral-pewter conductors (no vivid blue). The 1254px Foundation PNG and VP8L WebP were **copied byte-for-byte** from the user-approved V04 pilot and were hash-verified. Hidden/Advanced are **not** crops or freehand/generated icons; the final contact sheet is programmatically assembled **after** all three actual separate outputs were saved.

## Three individual icon files

| Tier | Raw 1254px RGB PNG SHA256 | Lossless 256px RGB VP8L WebP SHA256 | WebP bytes | Visual status |
|---|---|---|---:|---|
| **Foundation** | `e03ea5410ce31ffe9f0a85ebcc807e2e0d8332cba1737c64d781f38b78fa3a27` | `f992a71182e7d52ee7b21d758ad0180434be244fa7483def19efa7f14ba451fc` | 34,716 | **DIRECTOR-APPROVED V04; pixels unchanged** |
| **Hidden Art** | `199c62bfca7873e02e1b04a146b02391b1f4fc74c667433f10e008e0ec0729f6` | `ab2d7e697168d4dbfa7c36656d5ee56de7b8747eb9c9631d42d51f249bd5326c` | 54,106 | **NEW PROPOSAL / DIRECTOR REVIEW PENDING** |
| **Advanced Art** | `4fbea43cb373f21494ad837effd5c5313b0812dcd692529f7ae041afce857f23` | `668da512850df13c014e485b6f1f69433b05d39e8ffd3f72eaed42a8f246ce79` | 46,816 | **NEW PROPOSAL / DIRECTOR REVIEW PENDING** |

## Source/support geometry vs intentional internal brightness exception

Each individual output decoded as actual 1254×1254 opaque RGB PNG and 256×256 lossless VP8L WebP. On all **3 × 1,572,516 pixels**, its master original `max(R,G,B)>0` support is **exactly identical** to that of the new raw image; all originally black source pixels stay black. No external star, ring, extra point, symbol, background, eye or shadow wisps were added. **Full original `maxRGB` intensity equality is NOT satisfied** because visible black braids intentionally occlude portions of reflective silver surfaces. Results measured independently:

| Threshold-mask IoU | Foundation | Hidden Art | Advanced Art |
|---|---:|---:|---:|
| `t=1` original pixel support | **1.000000** | **1.000000** | **1.000000** |
| `t=32` dark-wire shadowed details | 0.891339 | 0.930385 | 0.901422 |
| `t=128` strong highlights | 0.683481 | 0.778334 | 0.769456 |

The intended **source geometry silhouette / black negative space is exact**, but **the stricter 27/27 maxRGB threshold-mask gate would FAIL**. The original V04 Foundation intensity exception was explicitly director accepted as part of the visual artwork; the same expected internal-brightness rule is now proposed for the two new tiers. Do not call these strict-master-intensity-exact, and do not substitute the older rejected pale Tensionwire V01 to gain strict brightness equality.

## Independent production/reproducibility QC

**121 read-only independent checks passed, 0 failed** before ZIP assembly: exact ZIP/reference/master/source hashes and safe CRC; 5 jutsu+identity bytes and decoded dimensions; all three complete 1254px originals and 256px RGB VP8L WebPs; 3/3 source binary pixel support/void; measured nine brightness thresholds per tier; pixel-for-pixel VP8L decode equality to original PNG Lanczos downsize; generic `ICON` 460800-byte reference ceiling; black corners and legibility at 125/64/32; monochrome neutral palette; preceding **84 separately approved icons** ZIP SHA unaffected (`c2d4eb48d16531f3ea27a270e86f435cd438ff1a58e3e5500f06fba03e5b82bc`); byte-identical reproduction of all **six** PNG/WebP files in an independently executed clean temporary directory using the original V04 recipe.

**149 offline checks PASS, 0 FAIL including deterministic portable ZIP member/CRC, byte equality and two full SHA-identical rebuilds.** This does NOT establish any `skillTree.image` field contract/preflight acceptance. QC record `qc/BR036_Blackwire_Neutral_Pewter_V04_Independent_QC.json` and scripts are included unchanged in the portable full ZIP.

**Portable conversation files (NOT pinned Git art binaries):**

| Asset | Actual SHA-256 | Status |
|---|---|---|
| `BR036_Itojinsei_Blackwire_Neutral_Pewter_v04_Three_WebPs_REVIEW_20261018.zip` | `6de090be111dcbe92054c14effcda75b0766ea2e557527d8462cc2c094c66dba` | 3 individual WebPs; Foundation approved, other 2 proposed |
| `BR036_Itojinsei_Blackwire_Neutral_Pewter_v04_Complete_Three_Tier_Source_QC_REVIEW_20261018.zip` | `38cb4797e3ae4aedb26a8f9b19c203c1d2947ea3b5060d93875e99360a59a191` | Original jutsu + geometry ZIPs, director-accepted reference art, deterministic producers, independent auditor, 3 raw PNGs / 3 WebPs, manifest, 3 programmatically composed review/QC PNGs; original refs unchanged |
| `qc/BR036_Blackwire_Neutral_Pewter_v04_Three_Tiers_REVIEW.png` | Exact saved WebP pixels inside full pack | Non-generative director review contact, not original artwork |
| `qc/BR036_Blackwire_Neutral_Pewter_v04_125_64_32_QC.png` | Resized exact saved WebP pixels inside pack | Legibility review |

## Approval and remaining source-production boundaries

**CURRENT: Foundation V04 specifically ACCEPTED. Hidden/Advanced V04 require individual director ART acceptance** of the actual two new files. Only if the director approves both is `BR-036` a completed three-icon standalone family and the existing **84/87** individually approved, byte-preserved collection eligible for a new **87/87** original WebP compilation. Explicitly record any approval before changing 84-count, and do not silently waive internal intensity differences for other families.

**OPEN, not live-upload-ready:** `skillTree.image` actual RGB opaque alpha field-specific preflight not source-verified; shared keyed `ICON` still requires alpha and `JUTSU_ICON` exception is only for `jutsu.image`. Old 21 director visually accepted but full-intensity-nonexact original-art images remain untouched. Git art original-byte pin/immutable Forge imagePack and art branch `RUL-2026-10-17-004` collision with `main` remain unresolved. **Live requests/writes/uploads 0/0/0, credentials none.**

## FINAL DIRECTOR ART ACCEPTANCE / 87-IMAGE COLLECTION — 2026-10-18

The director responded **“Approved”** after being shown the exact *new* Hidden Art and Advanced Art V04 PNG/WebP material treatment and asked whether to approve those two tiers. Together with the preceding explicit Foundation approval, **all three raw PNG and WebP icon pairs shown in the table above are now individually director-approved**. No original art bytes, color, silhouette, thread texture or internal shadow are edited as a result of approval. The earlier proposed archive's historic PENDING status is superseded only by acceptance metadata.

- **Accepted three-WebP ZIP:** `BR036_Itojinsei_Blackwire_Neutral_Pewter_v04_3_WebPs_APPROVED_20261018.zip` SHA `6de090be111dcbe92054c14effcda75b0766ea2e557527d8462cc2c094c66dba`; **byte-identical** to reviewed three-WebP ZIP.
- **Accepted full source and QC:** `BR036_Itojinsei_Blackwire_Neutral_Pewter_v04_APPROVED_Source_QC_20261018.zip` SHA `445bbceda5abe3f4273acc970790c751c07b0b6575e65e722a042e17967ffb44`, 19 old review members byte-identical; two approval-only members added.
- **All 87 original game-sized icons, 29 complete families:** `Bloodright_87_Approved_Original_WebPs_256px_20261018.zip` SHA `6de353b94244f6691d9b049f44bfac623bdbcbb9737e320625ac72c76934be19`, **5,384,275 bytes**. All former 84 director-approved images kept **byte-for-byte unchanged**. Final original art/manifest evidence: [BLOODRIGHT_87_FINAL_ART_CLOSEOUT_20261018.md](BLOODRIGHT_87_FINAL_ART_CLOSEOUT_20261018.md).
- **Current-session QC:** **1,191 independent offline assertion evaluations PASS, zero FAIL**, including exact 84 per-file earlier-original SHA comparison, Ito raw/VP8L byte SHA, full original nonzero-support master shape t1 match, expected **nonexact** internal brightness masks at t32/t128 (not mislabeled PASS as 27 strict masks), decoded lossless WebP equality, unique 29 × 3 census and full archive deterministic byte-identical rebuild. Earlier independent new-trio 149 checks also PASS.
- **Visual closure does not imply technical clearance:** old 21 source-master strict-intensity exceptions remain unchanged, and 3 Ito accepted internal black-wire brightness exceptions remain recorded; all `skillTree.image` field/preflight/Git-immutable-binary/Forge, art lineage ruling-ID collision and live game action boundaries still OPEN. **No live reads/writes, credentials none.**
