# BR-015 Blue Blade Eyes — Source-Grounded Pale Frostblade Azure V04 Foundation Pilot

**Status:** DIRECTOR PALETTE CORRECTION RECEIVED (2026-10-18) / **ONE NEW FOUNDATION V04 ART CANDIDATE PROPOSED, NOT YET VISUALLY APPROVED**. Historically director-approved Midnight Blade Alloy V03 Foundation image preserved byte-exact. Hidden/Advanced V03 unapproved and paused. No live game requests/writes, uploads or credentials.

**Lead:** Image Production · **Supporting lens:** Art Director.
**Repository:** `perseverance484/tnr-tools` · **art branch:** `chatgpt/bbe-pale-blue-source-correction-20261018` · **exact parent:** `chatgpt/bbe-midnight-alloy-trio-20261018@c016a4d8230666e3fd265379023ce6a03546e598`. Current main separately checked `fd7e194afab71a5712b83d16397feffdf704e9d2`. Art lineage not merged.
**Canonical sources:** `docs/workflows/BLOODRIGHT_ICON_STUDIO.md`; `docs/design/bloodright/BBE_MIDNIGHT_ALLOY_V03_TRIO_REVIEW_QC_20261018.md`; `docs/design/bloodright/BBE_TIER_EMBLEM_FAILURE_DIAGNOSIS_20261018.md`; `docs/design/bloodright/BBE_ICON_OUTPUT_QC_20261008.json`; `skills/producing-tnr-art/data/25x_DATA_art_spec.json` (target field-specific gate still unresolved).

## Operator's corrective art direction

After the Foundation V03 was specifically visually accepted and matching Hidden/Advanced V03 files proposed, the operator supplied **actual current BBE bloodline/jutsu art** and stated **“BBE is more of a pale blue, like baby blue or ice. These are the current BBE bloodline images.”** This specifically corrects the former **dark Midnight Blade Alloy** family palette's visual mismatch; earlier assumption that other ice families required making BBE dark gunmetal/ultramarine was overcorrected.

The director's first V03 Foundation approval is not silently erased or rewritten: its specific source SHA remains accepted as previously viewed, but **its continuation as the preferred BBE family treatment is ON HOLD pending this palette correction**. V03 Hidden/Advanced have never been director-approved, must not be auto-promoted or used in the final 87-image pack, and are superseded **as pending design candidates**, not erased binary evidence. The new V04 is **one proposed replacement Foundation** only. No new V04 artwork is accepted until explicit user confirmation.

## Actual uploaded reference art intake

**Operator archive:** `BR-015_Blue_Blade_Eyes.zip`; **actual SHA-256** `97f463fe08e421bd67de53a45abc079be643b5e7b2bba6a05caf03c433be7309`, 545,892 bytes, ZIP CRC clean. `manifest.json` contains **8 exact bloodline jutsu images + one bloodline identity JPG**, plus recorded CDN/capture provenance. All nine actual 256×256 RGB pixels, MIME, member byte counts and SHA-256s independently verified against manifest. All eight jutsu names/IDs matched the pinned `docs/design/bloodright/kits/blue_blade_eyes.json`:

- Icebound Might `YGBz7eIDvLwWXSVFEcK9j`
- Glacial Volley `Bw2OBS92Xi-4YlfErS632`
- Ice Shackles `Aff56oo9BFTcoLLeEyOja`
- Blade Resonance `TFRsEeV-VacukUUop-dtN`
- Blue Crimson `bxIPWiqiEaCmPYfAysB5a`
- Quintessential Flake `dXOjSl1vNp5G5BsFrNPkh`
- Sapphire Command `gIEy7THAZdXgcak5zs5U6`
- Arctic Frost `0tPhVC7G21Ej99YSICtJO`

**Actual material inspection:** Icebound Might, Glacial Volley, Blade Resonance and other individual current images are predominantly **high-key icy pale blue, cyan crystal/ice edges, blue-white blade-light with cold cobalt/dark-navy depth**. Identity contains blue eyes and a centered ice-blade motif. Unlike the earlier wrong freehand attempts, there is **no** requirement to import a new eye/pupil shape into the universal tier geometry. The original jutsu imagery favors **icebound blade energy**, not dark steel as the dominant material.

**Evidence boundary:** the ZIP's CDN-served images match the archived manifest; no current game API was queried and there is no claim of original uploader byte-identity. The source has **no authority to alter the fixed Bloodright three-tier shapes**.

## Source-grounded art treatment — Frostblade Azure V04 (PROPOSED)

**Direction:** light baby-blue / sky-ice aura with blade-sharp cyan-white faceted ridges and restrained sapphire depth, not dark alloy. Maintain BBE's actual source palette without merely duplicating the other two Ice bloodlines: **Hyouga Yui** uses intensely saturated cobalt fractured blue ice, while **Teno Yuki** uses near-white silver/opal frost. BBE's proposed middle register emphasizes `pale bright blue` and sharp iceblade light. The comparison is a qualitative art proposal, not a mathematical style-acceptance gate.

Bright-sample RGB means from the *exact saved 256px Foundation WebPs*, calculated over pixels with max channel >=100:
- New V04 BBE: **(111,173,202)**
- Approved Hyouga Yui: **(34,97,202)**
- Approved Teno Yuki: **(186,194,202)**
- Approved Shinrai Ou: **(124,134,202)**

The varying red/green-channel balance documents the intended middle pale-blue/cyan register, but the director retains the final visual distinction decision.

## One independently saved candidate, exact geometry

**Original fixed-master source:** `Ethereal_Monarch_Foundation_TEAL_1254.png` SHA-256 `bb3a3e331e5913fa527049980e2738c151b85eb54ef579cd468126b10039cea2`, in operator-supplied starter ZIP SHA-256 `9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`. The 2026-10-18 director-approved Midnight V03 Foundation source (SHA-256 `6a15c3f0548a36dd3f381d88bdeacdeb26ca49c09d82199326c7f0897488c042`) supplied in-geometry facet glint detail only. V03 remains exact and unchanged, as independently verified by SHA and WebP pixels.

**Method:** separate deterministic 1254px PNG material remap. For every pixel, `max(R,G,B)_V04 == max(R,G,B)_original master` exactly. Original black negative space entirely unchanged; no invented outer effects, eye glyphs, frames, character art, labels, or newly lit pixels. No freehand image generation or generated collage was used. One 256px lossless VP8L export created via Pillow Lanczos. **No Hidden or Advanced V04 images produced.**

| Proposed file | Actual SHA-256 | Size | Status |
|---|---|---:|---|
| `br015_bbe_foundation_frostblade_azure_v04_1254.png` | `a31f1bc80e7dcddb4261877b857bfdf78c2d68b802b01b9fd876b494cf1d458b` | 1,197,931 B | RGB 1254×1254 PNG, **PROPOSED** |
| `br015_bbe_foundation_frostblade_azure_v04_256.webp` | `5c9a74ec58a60bc24d8db8fe14e0f7d74952eb9b2613a356e3ba3e414b2f5e66` | 43,076 B | RGB 256×256 VP8L lossless, **PROPOSED** |

**Independent read-only offline QC: 80/80 checks PASS, zero FAIL**, including supplied original BBE ZIP SHA/CRC and nine image hashes/dimensions/captured byte counts; pinned kit ID/name joins; exact starter and source-master SHA; byte-exact earlier approved V03 original PNG & WebP preservation; new raw/export dimensions/mode/hash/bytes; **all 1,572,516 Foundation maxRGB pixels identical**; 9/9 brightness thresholds (1,8,16,32,64,128,192,240,254) exact; black source void and corner checks; VP8L decoded pixel equality to intentional Lanczos raw downsample; reference 460800-byte ICON ceiling; legibility at 125/64/32; and neighbor sample color comparisons. Visual legibility and distinction require director acceptance, not just these checks.

## Portable artifact / review

- `BR015_BBE_Frostblade_Azure_V04_Foundation_PROPOSED_20261018.zip`: SHA-256 **`e339ae86274156c1d9e44bdff9329b8a15f392c45e5944d82a56c593ffcc59e0`**, 12,273,021 bytes, 13 archive entries, all members readback/CRC/byte-identity PASS. Two independent deterministic ZIP rebuilds reproduced exact archive SHA.
- Includes exact BBE original reference ZIP, original three-master starter ZIP, exact preserved old V03 Foundation PNG/WebP, new separately saved V04 Foundation 1254px PNG/256px WebP, Python producer and independent validator sources, evidence/manifest, 125/64/32 QA and image-source neighbor visual comparison programmatically composed from the exact stored individual images.
- Actual 80-check JSON: `qc/BR015_Frostblade_Azure_Foundation_V04_OFFLINE_QC.json`. Review PNG: `qc/BR015_Frostblade_Azure_V04_Source_Neighbor_Comparison.png`. QA panel: `qc/BR015_Frostblade_Azure_V04_125_64_32_QC.png`. All are evidence of proposed new material, not pre-approved source replacements.

## Next gate and safety

**Decision needed:** Director chooses whether to **replace the formerly accepted Midnight Alloy V03 Foundation's palette** with new source-grounded Frostblade Azure V04 Foundation. Do not interpret the user's supplied source references as image-level approval of this newly generated V04. Once that acceptance is explicit, apply the exact new V04 recipe independently to original Hidden and Advanced geometry masters, perform all strict geometry+codec QC, and seek separate art acceptance for the two results. The old V03 trio remains historically recorded and the two proposed V03 tiers remain unapproved.

**Actual live Bloodright field mechanics still unverified:** repo shared `ICON` target's keyed-alpha rule applies to item/bloodline.image, `JUTSU_ICON` optional alpha to jutsu.image only; the targeted `skillTree.image` opaque RGB preflight/renderer path is not proven. Formal artpreflight not run for that field; no upload-ready claims. Previously approved 78 original standalone assets and any prior geometry exceptions unchanged. **Zero live requests/writes, zero credentials, zero publication.**
