# Workflow — Bloodright Tier-Icon Art Studio

**Status:** DIRECTOR-APPROVED, 2026-10-16; art-production workflow, not live-game authorization.
**Lead:** Art Director; **support:** Image Production.
**Source lineage:** 2026-10-08 tracker `chatgpt/bloodright-icon-production-tracker-20261008@c85c1ea834e24315b5688f73a65c35479b8963e6`; operational baseline `main@99e86dc549b86f1f4a5846c0e509fa6bc15b3463`.
**Decision history:** `docs/RULINGS.md`, RUL-2026-10-16-004.

Use with `docs/00_INDEX.md`, `docs/workflows/ART_PRODUCTION.md`, `docs/workflows/ISOLATED_ART_GENERATION.md`, and `skills/producing-tnr-art/SKILL.md`. The skill's live art spec and validator own *mechanical* target rules. This workflow owns the approved **Bloodright three-tier emblem visual language and production sequence**, not Bloodright tree mechanics or renderer contracts.

## 1. Bounded production scope

- Initial **29 public A/S/H bloodlines** from the pinned, director-approved roster: **19 A + 6 S + 4 H**, three icon artworks per bloodline = **87 artworks**.
- One **Foundation**, one **Hidden Art**, and one **Advanced Art** visual is shared by all nodes of its tier *within the same bloodline*. Do **not** manufacture unique artwork for each tree node.
- Membership follows the pinned Fable Bloodright roster, not an inferred current live roster. Do not add the separately hidden, deferred or excluded records without a director scope decision and source verification.
- Per-bloodline status, IDs, historical evidence, and output QC belong in `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md` and its linked records.
- Bloodright structural SVGs and showcase posters use the *separate* `docs/workflows/BLOODRIGHT_POSTERS.md`; a poster is not an individual reference image for an icon.

## 2. Universal tier silhouettes — locked

| Tier | Immutable design silhouette |
| --- | --- |
| **Foundation** | One centered **elongated outer diamond** enclosing a smaller solid/faceted **inner diamond**, with clear black negative space between them. |
| **Hidden Art** | The **nested pointed diamond**, flanked by **two balanced inward-curving crescent arcs** connected by short **horizontal crosspieces** at mid-height. |
| **Advanced Art** | The **nested pointed diamond** surrounded by a **large, sharp multi-point starburst**, with strong primary cardinal points and smaller intervening rays. |

This is a **shape system**, not an invitation to invent a different symbol for each element. The silhouette, tier-relative scale, center, symmetry, principal points, crossing structures and negative-space hierarchy remain recognizable across all bloodlines. No halo substitution, added ring, wing, weapon, character, crest, alternative runes or surrounding pictorial scene. Minor organic edge texture must never change the silhouette. The black void separating concentric forms is deliberate and should remain clean.

**Allowed per-bloodline variation:** verified palette, intrinsic material/faceting, internal texture, small controlled chakra glow and edge treatment. Derived from that bloodline's *actual existing jutsu art* and user-approved treatment card; never infer from the name or classification alone. Preserve contrast against solid black.

**Director-approved background:** **solid black / near-black, opaque**, on every Bloodright tier icon. No chroma-key lime, transparency simulation, frame/UI, text, watermark, vignette scene or decorative background. This specific Bloodright art ruling is distinct from the separately approved designed-background policy for *jutsu* icons.

## 3. Start a bloodline (Art Studio / persistent workspace)

1. Verify live repository baseline and exact tracker SHA; read current art authority, bloodline ID/rank, kit source and prior approval/QC evidence.
2. Open **2–4 exact original bloodline jutsu icons** and, when present, its identity image. Capture exact source names/IDs, provenance and visible material/palette. A screenshot, poster or kit JSON is not evidence that an unseen jutsu image was visually inspected.
3. Inspect against approved BEE and Blue Blade Eyes tier-emblem *individual* examples. Their geometry is the family reference; **their color is not** the next bloodline's prescribed color. Compare adjacent/confusable bloodlines.
4. Propose a short **treatment card**: verified imagery, palette, material, glow constraints, distinguishability, forbidden borrowed colors/forms, and reference provenance. Obtain director approval before starting Foundation.
5. Record `VISUAL DIRECTION APPROVED` separately from the state of any generated file.

For generation, only pass **one or two individual images** selected for that one target, each explicitly labeled `silhouette-only`, `material/style-only` or `target identity`. Do not send a contact sheet or the full image collection to an isolated generator. The original image bytes must actually be attached/accessible; a link, image hash or prose-only recollection is insufficient. Current-chat re-encoded copies are usable for *visual orientation*, **not** assumed equivalent to the previously approved raw originals.

## 4. One-icon production loop

The persistent **Art Studio** coordinates; a **fresh isolated generation conversation** owns each single tier image.

1. **Foundation first:** strict universal diamond geometry, approved material/palette, opaque black. Generate **one** square candidate; director accepts or rejects. On acceptance preserve exact raw bytes and checksum; lock palette/material treatment.
2. **Hidden Art second:** fresh conversation, Foundation supplies **material/style only**; the universal Hidden Art geometry is fixed. Generate one candidate, obtain director acceptance, preserve raw bytes.
3. **Advanced Art third:** fresh conversation, Foundation/Hidden Art supplies **style/material only**; universal sharp starburst is fixed. One candidate, director acceptance, preserve raw bytes.
4. On repeated wrong-form outputs, stop and restart the isolated conversation instead of layering more old images. No image sheet is a substitute for three independent individually approved originals.
5. Inspect a *studio-made comparison sheet* only **after** the three originals exist, for director/QC review. Do not regenerate the sheet as a replacement for individual images.

Every generation brief states: the tier and exact bloodline ID; approved reference roles; one dominant immutable silhouette; material treatment; solid black opaque background; centered square composition; negative-space/edge contrast; exclusions and prior confusion risks; **one image only**; no processing, repository guessing or game writes. Design at actual thumbnail legibility, not full-resolution ornamentation.

## 5. Production and evidence gates

Track these separately; passing one does not imply the next:

- **VISUAL APPROVED:** director accepted the *specific* raw original, with documented bloodline/tier and SHA-256.
- **RAW INTAKE VERIFIED:** actual source bytes accessible, decoded format/mode/dimensions and SHA-256 recorded; source immutable/pinned when repository storage is authorized.
- **FAMILY QC:** display checks at **125 / 64 / 32 px** for silhouette recognition, black negative space, no tier confusion, consistency of palette/material, neighboring-bloodline contrast. The 125px number follows the current generic ICON reference, **not yet an independently verified future Bloodright UI display contract**.
- **EXPORT QC:** use actual current `25x_DATA_art_spec.json` target and appropriate processing scripts. Historical BEE/BBE output used opaque RGB **256×256 lossless WebP**; verify container codec, dimensions, bytes, pixel preservation, black corners, exact `@img` filename, fresh versioned filename and packaging integrity. Record output SHA-256, size, paths and command.
- **PREFLIGHT:** invoke the real repository validator and record **all errors**. The current shared `ICON` target still assumes **lime chroma-key / RGBA**; director-approved opaque Bloodright RGB exports fail the generic **alpha** rule. Treat this as **PREFLIGHT-BLOCKED / field-contract resolution pending**, not a silent waiver or green preflight. Do not manufacture transparency, alter validation/spec code, or declare the file upload-ready merely because visual/byte/codec checks passed.
- **WIRING/PUBLISH:** separate future action only after user-approved client-field/spec resolution, source preservation and explicit operator authorization. Repository work alone authorizes **zero live-game requests/writes**.

Do not assume `item.image`, `jutsu.image`, and `bloodline.image` faithfully describe the *future Bloodright tier-skill icon field*; Fable must verify its actual consumer before a delivery/write contract is set. Any code/spec/preflight fix is **Lane A, Fable-owned** and independently reviewed, not an art-studio workaround.

## 6. Progress accounting and next gate

2026-10-08 tracker evidence: **BEE 3/3 and Blue Blade Eyes 3/3** director-approved and historically processed to WebP (**6/87**). Their accepted output hashes appear in the two `*_ICON_OUTPUT_QC_20261008.json` records. Neither accepted raw binaries nor final WebPs were pinned in the tracker branch; do not mistake screenshots or user re-uploads for byte-identical production originals.

**Next: Ethereal Monarch.** Its jutsu art was historically visually confirmed **teal/cyan**, but the six original images are not pinned in this production branch. Reacquire **2–4 exact individual jutsu originals** and verify material before proposing/confirming its treatment card, then generate Foundation in a fresh single-image conversation. **Taiyo Kami** follows after inspecting its actual jutsu icons.

**No raw art generated, no processing run, no game requests or game writes by adopting this workflow.**
