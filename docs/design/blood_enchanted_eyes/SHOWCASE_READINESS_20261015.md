# Blood-Enchanted Eyes — Eight-Jutsu Showcase Readiness

**Status:** **SHOWCASE STALE — NEW ART REVIEW OPEN (7/8 CURRENT RAW APPROVALS)** (2026-10-15). No final showcase approval or current eight-icon export pack. The earlier verified deterministic showcase is a historical snapshot only.  
**Workstation:** `chatgpt/bee-jutsu-art-studio-20261014`.  
**Workflow owner:** `docs/workflows/JUTSU_ICON_SHOWCASE.md`.  
**Reference layout:** director-provided 2 x 4 BBE screenshot `1000018422.png` (layout only; source is JPEG despite extension, 1536 x 854). See workflow for exact hash and framing rules.  
**No live requests or writes. No production upload.**

**Roster-size scope:** this preparation document is **BEE-specific**. Blood-Enchanted Eyes happens to have **eight** jutsu in the pinned historical roster, so its showcase uses the BBE-style **4 + 4** layout. **Do not generalize that count, grid, or 1536 x 854 canvas to other bloodlines.** Many A-rank bloodlines have five jutsu; S-rank rosters vary. Future bloodline studios determine N from their own verified jutsu roster and follow the adaptive procedure in `docs/workflows/JUTSU_ICON_SHOWCASE.md` (e.g. **3 + 2 centered** for five, pending director acceptance).

## Intended final presentation

For BEE's verified eight-jutsu roster specifically, a landscape **1536 x 854** contact sheet of exactly **eight** currently accepted BEE jutsu icons, **four square tiles per row**, on a plain dark navy/charcoal background. Each icon gets one label directly below: `<Approved jutsu name> <actual WebP size in decimal kB to one decimal>`. No title banner, decorative border, rarity card, guessed bytes, weapons/character embellishments, or image-generation changes to existing art.

**Frozen row-major display order**, following the BEE historical jutsu roster rather than the order the artworks happened to be generated:

| Position | Jutsu | Current raw approval at preparation | Accepted source (SHA-256 prefix) |
| --- | --- | --- | --- |
| R1C1 | Ring of Spilled Blood | APPROVED | `1000018474.png` (`a686b372`) |
| R1C2 | Crimson Tithe | APPROVED | `1000018475.png` (`eeae4826`) |
| R1C3 | Sanguine Plague | **CURRENT RAW APPROVED — chakra skull** | `crimson_shadow_skull_vortex.png` (`8f115286`); old `1000018488.png` superseded |
| R1C4 | Reaper's Embrace | APPROVED — scythe | `1000018481.png` (`0b972708`) |
| R2C1 | Unholy Enhancement | **REWORK UNDER DISCUSSION — NOT CURRENTLY APPROVED** | Old `1000018491.png` withdrew due Ring similarity; pulsing shadow-chakra vein network PROPOSED only |
| R2C2 | Crimson Impact | APPROVED | `1000018482.png` (`85617e35`) |
| R2C3 | Hemocure | APPROVED — vitality bubble | `1000018489.png` (`bdb157eb`) |
| R2C4 | Thousand Strike | APPROVED — needle storm | `1000018487.png` (`6a6fead5`) |

**Historical decision now fulfilled by accepted `1000018491.png`:** director disliked Unholy Enhancement's previous upward power eruption because of confusion with Crimson Impact; current replacement target is savage, broken radiating waves with intentional broad shadow wavefronts, **not** lumps/debris, smooth vitality-bubble arcs or an explosion. The latest rework `1000018490.png` (conversation JPEG RGB 1536 x 1536, 426,476 bytes, SHA-256 `27069f2d73dfaa76332dae0f953d2e6c113b6c3f492324f231559b0337e422bf`) received critical director feedback on its shadow anatomy; **not approved**, not a style reference. This attachment's received-byte metadata is recorded here as review evidence; the actual binary is conversation-bound, not Git-pinned.

## Latest director collection review (2026-10-15) — revokes showcase readiness

- Skull replacing the old Sanguine shadow front: raw RGB PNG `crimson_shadow_skull_vortex.png`, 1254×1254, 1,893,042 bytes, SHA-256 `8f115286d8cd7fdaecfd018a4cf6f5349307a5bf90d9036001d0c8db33f97b7f`. Director explicitly approved the skull; no current 256px processed WebP yet.
- Unholy Enhancement previous raw approval `1000018491.png` withdrawn on family comparison because it resembles Ring of Spilled Blood; a dense but **bold, simple network of pulsing crimson-black shadow-chakra veins** is being explored as an alternative. Avoid upward/low-central eruption (Crimson Impact), rings/vortex (Ring), small filaments and literal anatomical blood vessels.
- The previous deterministic showcase `bee_jutsu_icon_showcase_v1.png`, accompanying `SHOWCASE_QC_20261015.json`, 125/64/32 QC preview, and archived WebPs are **accurate historical snapshots of the prior eight** but **STALE, NOT FINAL, NOT DELIVERABLE** after the artwork changes. All original file/export hashes remain evidence. Regenerate new current Sanguine/Unholy exports and repeat family QC/showcase only after eight current approvals.
- Never represent the previous source-derived size captions as current after new exports; no new showcase output/file size is established.

## Corrected showcase and invalid first montage — evidence (2026-10-15)

The first image-generated red contact sheet `crimson_infernal_skill_gallery.png` was **invalid**: it reinterpreted Sanguine Plague and Unholy Enhancement, drew the *shelved* Sanguine source `1000018478.png` instead of the approved `1000018488.png`, and captioned **source JPEG KiB sizes**, not verified final processed WebP decimal kB. It was not an exact-asset presentation and is superseded. Never count it as a family review deliverable.

The corrected `bee_jutsu_icon_showcase_v1.png` (1536×854) was assembled **deterministically** from decoded bytes of each of eight genuine current 256px RGB VP8L lossless WebP exports. It uses the registered 4×2 roster order above with **correct Sanguine `1000018488.png`** and **newly accepted Unholy `1000018491.png`**. No icon was regenerated, repainted, warped or cropped; only downscaled to the exact required WebP size and uniformly resized for the contact sheet. Each caption is generated from its **actual output WebP byte count / 1000**.

**HISTORICAL, NO LONGER CURRENT output evidence:** `SHOWCASE_QC_20261015.json` includes every source/export SHA-256, 256px WebP byte counts, layout, corrected image SHA, archive integrity, and distinct delivery/preflight statuses. Current downloadable artifacts are conversation-backed, not Git binary-backed. The director's **whole-family acceptance is still pending**, as is the shared ICON opaque-alpha preflight resolution.

## Final showcase gate — current facts

| Gate | Current state | Needed |
| --- | --- | --- |
| Raw visual approvals | **7/8 CURRENT** | New Sanguine skull approved; Unholy vein design pending. Earlier 8/8 was a historical checkpoint |
| Exact accepted originals | **8/8 SHA MATCHES** on locally accessible user attachments | JPEG RGB 1536px originals (despite .png extensions), conversation-held; binary files not Git-pinned |
| Current final 256px exports | **6/8 unchanged verified**, 2 need replacement | Old Sanguine corruption-front and Unholy-wave exports are retired; processing needed for new skull and future Unholy |
| Historical processed file | Old Ring `icon_bee_ring_of_spilled_blood_v1.webp` remains historical REJECTED | Corrected current Ring is `icon_bee_ring_of_spilled_blood_v2.webp` (80,484 bytes) |
| Small-size family comparison | **Assistant inspected all eight actual processed files at 125/64/32px** | `bee_jutsu_icon_qc_125_64_32.png`; director final whole-family comparison pending |
| Shared ICON alpha preflight | **NOT RUN / KNOWN BLOCKER** for intentionally opaque jutsu artwork | Current generic ICON alpha rule contradicts approved opaque jutsu background; no preflight PASS claim |
| Labeled showcase + manifest | **PREVIOUS SHOWCASE STALE** | Valid historical exact-source snapshot; rebuild after new Sanguine and Unholy, with new WebP-derived captions |
| Whole-set director signoff | **PENDING** | Present corrected exact-source showcase and request final set-level feedback/acceptance |
| Previous processed bundle / live | Historical eight-file ZIP passed CRC/hash checks but is now STALE; **NO LIVE ACTION** | Never deliver the old candidate package with superseded Sanguine/Unholy images |

The old BBE reference montage is an example of **showcase presentation only**. Its pictured icon art and reported file sizes are not BEE inputs or evidence that BBE had eight final accepted files; its own closeout documents an unfinished revision. Never borrow the blue crystalline rendering for the red BEE family.

## Final workstation closure action

**HISTORICAL closeout checklist from prior 8/8 checkpoint** (superseded by the latest director rework):

1. **COMPLETED:** verified 8/8 current director raw approvals and individual original source hashes; old rejected/shelved versions excluded.
2. **COMPLETED FOR TECHNICAL CHECKS:** eight 256px RGB lossless WebPs pass format, byte-limit, image-decoding, pixel-binding, and assistant 125/64/32 preview checks. **Preflight NOT RUN** due known alpha contract mismatch.
3. **COMPLETED:** composed faithful image and companion manifest deterministically from the eight exact WebPs; captions from actual decimal WebP kB.
4. **PENDING:** show corrected set for explicit **director showcase-level acceptance**; rebuild if needed.
5. **PENDING FAMILY SIGNOFF / FOLLOW-UP:** preserve final director verdict, evidence/hash metadata and opaque ICON alpha-preflight limitation; keep ZIP separate from upload readiness. Showcase acceptance is not live publication.

**Ownership boundary:** Art Studio may design/review/produce the composite from accepted data; any new generalized showcase builder/script or validator change is separate Lane A implementation, normally Fable-owned and independently reviewed.
