# Ghost Ship chest icons — Art Studio register

**Session:** PERSISTENT ART STUDIO, not image generation  
**Lead:** Art Director · **Supporting lens:** Image Production  
**Status:** 2/12 director-approved visuals; Rare Hunter candidate 1 visual revision requested; 0/12 production-ready exports  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Base:** `main@4e8346ba71e4f72d3b14a81bd1ec2a5e92b921bc` (2026-10-20)  
**Canonical approved brief:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md`  
**Director approval:** `docs/RULINGS.md#rul-2026-10-20-002--ghost-ship-chest-icons-art-direction-approved-as-written`  
**Workflow:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Mechanical authority:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json` → `targets.ICON`  
**No game contact:** 0 live-game requests, 0 live-game writes; no credentials, game uploads or publishing.

## Current gates

- Gate 01 — Common Hunter's Chest: **DIRECTOR APPROVED**, original supplied in studio conversation as `1000018925.png`. Visual Ghost Ship rendered-style lock and Hunter's claw/leather/fang family motif lock **established**. Mechanical background/alpha QC unresolved (source decoded JPEG on black matte).
- Gate 02 — Common Gatherer's Chest: **DIRECTOR APPROVED**, isolated prompt retrospectively recorded in `COMMON_GATHERER_CHEST_ISOLATED_BRIEF_20261020.md`, original supplied in studio conversation as `1000018926.png`. Gatherer's leaf/rope/sprig family motif **established**. Compared both conversation-supplied images side-by-side after Lanczos reduction to **125 px**: family identities **VISUALLY DISTINCT** (fang/claws versus rope/sprig/leaf). Mechanical background/alpha QC unresolved (source decoded JPEG on black matte).
- Gate 03 — Rare Hunter's Chest: **REVISION REQUESTED / NOT APPROVED**. Initial candidate received and visually reviewed at 125 px beside approved Common Hunter, including a grayscale comparison. The director observed that it looks virtually identical to Common except for blue lighting; the tier escalation does not yet read. Request a **same-subject revision in the existing isolated generation session**, not a wrong-subject restart. The original generation brief remains `RARE_HUNTER_CHEST_ISOLATED_BRIEF_20261020.md`. Two individually attached refs remain Reliquary + approved Common Hunter only.
- Gates 04–10: **BLOCKED** pending preceding approved illustrations; in each case attach Reliquary and one approved icon from that same family only. Gates 11–12 (Ornate and Mystery) are also **BLOCKED**; neither has a same-family predecessor, so the canonical 'same family' second-reference instruction is undefined for these two; confirm applicable reference handling with director when reached. Never invent a reference or attach a collage.
- Collection handoff: **BLOCKED** until 12/12 original image approvals, raw QC, native-alpha/key processing, lossless 256×256 WebP exports, dark-composite checks, and `artpreflight.py --type ICON` output. The director retains final acceptance.

## Approved reference and style gate

- **Reference source:** `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp` at base main SHA; Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`. Image bytes visually inspected during initialization; 3/4 dark riveted box, dark wood and near-black iron, cyan faceted crystal, cool edges. **Style/material ONLY**, never a flat-lid or subject/silhouette template.
- **Attach actual reference bytes**, not a textual path, URL, thumbnail, collage or rejected image. Session 01 uses this reference **alone**.
- Approved subject and palette remain in the canonical handoff. Chest lids are **closed and domed**; no legacy pixel-art chest references; Hunter's claw brand/leather/fang versus Gatherer's leaf/rope/sprig must remain readable at 125 px.
- The shared prompt clause calls for a crystal with a soft inner glow while the Common treatment says “no glow.” Preserve both approved phrases in their respective source clauses; for Common QC distinguish crystal material brightness from extra cast glow, lit seams/brands, auras or halos. If a candidate makes the distinction ambiguous, director visual approval settles its acceptance — the studio must not silently rewrite the tier ladder.

## Rare Hunter's Chest — candidate 1 feedback (2026-10-20)

- **Source attachment:** `1000018927.png`; actual decoder format JPEG (RGB, **opaque black matte**), 1536×1536, 372094 bytes, SHA-256 `dfdce5512e8f4d826519fd13550723297bcde17e881356b354cb958b07e416ce`. Candidate evidence only; **not** an approved raw, production asset, or Git-pinned binary.
- **Director feedback:** “Kinda looks identical to common other than the blue tinge.” Accordingly, **visual acceptance is withheld**; do not advance to Rare Gatherer's as if Rare Hunter were approved.
- **Independent 125-px comparison:** Common and candidate share practically the same domed lid, two curved iron bands, leather/fang geometry, dark corner rivet blocks, diamond gem housing and front claw placement. Their 125-px grayscale silhouettes/material structure remain extremely similar. The most visible change is extra saturated cyan seam lines; this reads as a lighting pass rather than the approved material/tier evolution.
- **Revision target (art-direction proposal, not a new tier rule):** emphasize *mechanically distinct* Rare reinforced ironwork visible without color: **layered/stepped steel reinforcement bands over the two arch hoops**, **substantial riveted shoulder/corner armor plates**, and a **visibly stronger faceted clasp housing**. Keep claws/leather/fang readable and the same camera/size. Retain **only a faint lid-seam** cyan glow; avoid multiple neon-blue stripes. No silver trim, glowing brand, filigree, crystal cluster, gold, or chains (reserved to higher/special tiers). Judge against Common at **125 px and grayscale** before asking for approval.
- **Protocol classification:** correct subject with inadequate tier readability, *not* a wrong-subject strike. Same isolated session may revise. Production background issue remains (opaque JPEG/black rather than native alpha or approved lime key).

## Production ledger

`—` means not yet produced or measured; **PENDING** is not an approval, QC pass or preflight result. Store actual original image identity, MIME/format and SHA-256 in an intake entry when received; processed export SHA-256 and byte count are distinct from raw identity.

| # | Target | Exact delivery filename | Type | Raw approved | Export px | Export bytes | Raw SHA-256 | Preflight |
|---|---|---|---|---|---|---|---|---|
| 01 | Common Hunter's Chest | `icon-gs-chest-hunter-common.webp` | ICON | APPROVED | — | — | `b341d9e939d7a5cb182ac8576ab97777b36cfea607a3e4d6768052554ea3e4f3` | NOT_RUN |
| 02 | Common Gatherer's Chest | `icon-gs-chest-gatherer-common.webp` | ICON | APPROVED | — | — | `acb6f618cdbc3b5414a3bfbfaabc682b9e03403141fe0d8b7b8c0a4a5356381a` | NOT_RUN |
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

## Uploaded-original intake evidence (2026-10-20)

The two conversation-delivered originals have filenames ending in `.png` but **decode as JPEG** (`RGB`, no alpha), each 1536×1536 with an opaque black background. The hashes below describe **the exact bytes supplied to this studio**, not Git-pinned original generators, finished WebP files, or production QC.

| Target | Studio intake filename | Decoded format | Pixels | Raw bytes | Raw SHA-256 | 125-px visual gate | Mechanical alpha/key gate |
|---|---|---|---|---:|---|---|---|
| Common Hunter's | `1000018925.png` | JPEG (RGB, opaque) | 1536×1536 | 333824 | `b341d9e939d7a5cb182ac8576ab97777b36cfea607a3e4d6768052554ea3e4f3` | PASS (paired) | **BLOCKED**: black matte, no native alpha/lime key |
| Common Gatherer's | `1000018926.png` | JPEG (RGB, opaque) | 1536×1536 | 364006 | `acb6f618cdbc3b5414a3bfbfaabc682b9e03403141fe0d8b7b8c0a4a5356381a` | PASS (paired) | **BLOCKED**: black matte, no native alpha/lime key |

**Important:** Director approval is visual acceptance only. The approved images are suitable as visual reference attachments for subsequent generation, but **neither is a valid production input for the prescribed native-alpha/lime-key pipeline yet**. Re-acquire transparent/flat-lime originals or explicitly approve and verify a separate safe background-matting repair; keying pure black indiscriminately risks eating near-black wood/outline. Never claim clean alpha, finished WebPs, successful preflight or upload readiness from this evidence. The background issue need not stop generation of later tiers; communicate the issue promptly and require transparency/flat lime on new outputs.

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

- 2026-10-20: Rare Hunter candidate 1 returned; director withheld approval due to insufficient structural tier differentiation. 125-px + grayscale comparison corroborated. Candidate raw metadata logged; same-subject revision requested, generation remains isolated.

- 2026-10-20: initialized from fresh `main@4e8346ba71e4f72d3b14a81bd1ec2a5e92b921bc`; targeted canonical art brief, ruling, isolation workflow, skill/spec and original Reliquary style reference inspected. No raw generations received at initialization; no preflight run; no uploads/publishing.
- 2026-10-20: director visually approved Common Hunter and Common Gatherer from conversation attachments. Studio decoded, hashed, inspected and verified 125-px family differentiation. Discovered that attached `.png` filenames actually contain opaque JPEG black-matte images; native-alpha/lime background mechanical gate is blocked for both. Rare Hunter brief prepared, no image generation or preflight run in studio.
