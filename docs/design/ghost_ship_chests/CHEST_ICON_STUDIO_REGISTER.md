# Ghost Ship chest icons — Art Studio register

**Session:** PERSISTENT ART STUDIO, not image generation  
**Lead:** Art Director · **Supporting lens:** Image Production  
**Status:** INITIALIZED; icon 01 isolated brief READY; 0/12 raw approvals; 0/12 processed exports  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Base:** `main@4e8346ba71e4f72d3b14a81bd1ec2a5e92b921bc` (2026-10-20)  
**Canonical approved brief:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md`  
**Director approval:** `docs/RULINGS.md#rul-2026-10-20-002--ghost-ship-chest-icons-art-direction-approved-as-written`  
**Workflow:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Mechanical authority:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json` → `targets.ICON`  
**No game contact:** 0 live-game requests, 0 live-game writes; no credentials, game uploads or publishing.

## Current gates

- Gate 01 — Common Hunter's Chest: isolated brief `COMMON_HUNTER_CHEST_ISOLATED_BRIEF_20261020.md` prepared. Original not generated/received. Director visual approval **PENDING**. This approval will lock the rendered style and Hunter's motif.
- Gate 02 — Common Gatherer's Chest: **BLOCKED** by gate 01. Use Reliquary + approved icon 01 as the only two individually attached images; require director approval and 125px Hunter/Gatherer differentiation.
- Gates 03–12: **BLOCKED** until the required predecessor approvals; proceed in the exact order listed below. Every isolated conversation generates one asset and receives the Reliquary plus the approved same-family reference, at most two individual image attachments. For Ornate and Mystery, use the explicitly approved applicable reference strategy without introducing extra images.
- Collection handoff: **BLOCKED** until 12/12 original image approvals, raw QC, native-alpha/key processing, lossless 256×256 WebP exports, dark-composite checks, and `artpreflight.py --type ICON` output. The director retains final acceptance.

## Approved reference and style gate

- **Reference source:** `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp` at base main SHA; Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`. Image bytes visually inspected during initialization; 3/4 dark riveted box, dark wood and near-black iron, cyan faceted crystal, cool edges. **Style/material ONLY**, never a flat-lid or subject/silhouette template.
- **Attach actual reference bytes**, not a textual path, URL, thumbnail, collage or rejected image. Session 01 uses this reference **alone**.
- Approved subject and palette remain in the canonical handoff. Chest lids are **closed and domed**; no legacy pixel-art chest references; Hunter's claw brand/leather/fang versus Gatherer's leaf/rope/sprig must remain readable at 125 px.
- The shared prompt clause calls for a crystal with a soft inner glow while the Common treatment says “no glow.” Preserve both approved phrases in their respective source clauses; for Common QC distinguish crystal material brightness from extra cast glow, lit seams/brands, auras or halos. If a candidate makes the distinction ambiguous, director visual approval settles its acceptance — the studio must not silently rewrite the tier ladder.

## Production ledger

`—` means not yet produced or measured; **PENDING** is not an approval, QC pass or preflight result. Store actual original image identity, MIME/format and SHA-256 in an intake entry when received; processed export SHA-256 and byte count are distinct from raw identity.

| # | Target | Exact delivery filename | Type | Raw approved | Export px | Export bytes | Raw SHA-256 | Preflight |
|---|---|---|---|---|---|---|---|---|
| 01 | Common Hunter's Chest | `icon-gs-chest-hunter-common.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 02 | Common Gatherer's Chest | `icon-gs-chest-gatherer-common.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 03 | Rare Hunter's Chest | `icon-gs-chest-hunter-rare.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 04 | Rare Gatherer's Chest | `icon-gs-chest-gatherer-rare.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 05 | Epic Hunter's Chest | `icon-gs-chest-hunter-epic.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 06 | Epic Gatherer's Chest | `icon-gs-chest-gatherer-epic.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 07 | Legendary Hunter's Chest | `icon-gs-chest-hunter-legendary.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 08 | Legendary Gatherer's Chest | `icon-gs-chest-gatherer-legendary.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 09 | Rusted Hunter's Chest | `icon-gs-chest-hunter-rusted.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 10 | Rusted Gatherer's Chest | `icon-gs-chest-gatherer-rusted.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 11 | Ornate Chest | `icon-gs-chest-ornate.webp` | ICON | PENDING | — | — | — | NOT_RUN |
| 12 | Mystery Chest | `icon-gs-chest-mystery.webp` | ICON | PENDING | — | — | — | NOT_RUN |

## Intake checklist, per approved original

1. Require original source bytes from its **own** isolated generation conversation, evidence of director approval, intended item name and expected output filename. Inspect actual decoder format, pixel dimensions, alpha, completeness, closed lid, no text or bad composition, and raw SHA-256; do not trust an extension.
2. Reject wrong-subject, multiple-object, open-lid, table/shadow, halo/disc or unusable background artwork instead of trying to fix it with processing; two wrong-subject attempts in one isolated conversation mean close and restart clean.
3. Preserve original. Keep genuinely native alpha, or key true flat lime `#00FF00` using the repository pipeline; clamp spill and pad transparently to **exact square** with margin (rarity frame still visible).
4. Export **lossless WebP**, recommended **256×256**, at least **160px** wide, with byte count **below 460,800**. No lossy fallback silently substituted.
5. Actually inspect the dark-background composite and compare relevant sibling icons at **125/64/32px** (the Hunter/Gatherer twin gate requires **125px**).
6. Run canonical `skills/producing-tnr-art/scripts/artpreflight.py <path> --type ICON`, preserve the full output, and record export dimensions, actual bytes, SHA-256, QC/preflight verdict and filename exactly. A correction uses a **fresh `_b` / `_c` name**, never overwritten bytes under the same output name.
7. Package 12 processed WebPs, ledger, hashes and preflight evidence only after all production gates pass. Incomplete packs must be clearly marked partial / draft.

## Downstream, not authorized in this studio

Fable / Claude Code, after the director accepts the completed set: commit binaries under `art/`, pin an `imagePack`, and prepare exactly one Forge **suggest-mode** ticket (`VISUAL`, title `Update icon`, one rationale per chest). No writes to game. All twelve chests' item rarity (`COMMON` including “Legendary” named chests) remains a **separate director decision**, not a change request in this workstream.

## History

- 2026-10-20: initialized from fresh `main@4e8346ba71e4f72d3b14a81bd1ec2a5e92b921bc`; targeted canonical art brief, ruling, isolation workflow, skill/spec and original Reliquary style reference inspected. No raw generations received; no preflight run; no uploads/publishing.
