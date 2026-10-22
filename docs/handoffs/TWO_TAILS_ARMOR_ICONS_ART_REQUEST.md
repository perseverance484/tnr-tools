# Art request: Two Tails armor icons (5)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-22)
- **Progress:** 1 Shozoku director-approved 2026-10-22 (`art/two_tails_armor/raws/raw_two_tails_shozoku_v1.png`); it locks the rendering and palette for pieces 2 to 5.
- **Status:** direction approved (RUL-2026-10-22-001: icons only, match the Kitsune set, offensive
  nekomata theme). Per-piece silhouettes below are proposals; the director's visual approval of each raw
  locks it, and icon 1 locks the rendered style.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one asset per generation session).
  Spec: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `ICON` (item icon, alpha required).
- **Source:** push/204 capture, `harvests/inbox/tnr_results_1792629744565.json` (2026-10-22).
- **Live-game requests/writes:** 0. The Kitsune icons were downloaded from the game's image CDN as
  references (approved); nothing is uploaded here.

## 1. Why

The Two Tails set is LEGENDARY, but its icons do not read as a family the way the RARE Kitsune set does.
The director wants Two Tails to match the Kitsune set's look while reading as a more offensive set: every
Two Tails piece boosts the wearer's damage.

## 2. Targets

| # | Item | Id | Slot | Effects (live) | Delivery filename |
|---|---|---|---|---|---|
| 1 | Two Tails Shozoku | `t88B9dtM-Wly3NZ_6f6NZ` | chest | damage given +15%, stats +20%, max pools | `icon-two-tails-shozoku.webp` |
| 2 | Two Tails Zukin | `qcIb0edEpXfLaOiERicCE` | head | damage given +15%, absorb, stats +15% | `icon-two-tails-zukin.webp` |
| 3 | Two Tails Tekkou | `rFrYeO7r4fsIn8PrU2xd8` | hands | damage given +15%, max pools, stats +20% | `icon-two-tails-tekkou.webp` |
| 4 | Two Tails Tabi | `4voAt9Cg1z7X0Wg3YKQ_m` | legs (leg wraps) | damage given +15%, lower pool costs, stats +15% | `icon-two-tails-tabi.webp` |
| 5 | Two Tails Jaki-Tabi | `vW7pgjvMnJMbg2aFzWwZo` | feet (split-toe boots) | damage given +15%, stats +20%, shorter cleanse/clear cooldowns | `icon-two-tails-jaki-tabi.webp` |

## 3. Style lock: the Kitsune set

References (repo-pinned, 250x250 RGBA WebP, downloaded 2026-10-22): `art/two_tails_armor/refs/kitsune_*.webp`
(mask, armor, gauntlets, belt, pants, pants_f, tabi_shoes).

What the Kitsune icons share, and Two Tails keeps:
- **Rendering:** painted, cel-shaded game-item art with a crisp dark outline, soft shading, bright rim
  highlights on metal. Not hard pixel art and not photoreal.
- **Construction:** lacquered armor plates over layered cloth, gold-trimmed edges, gold fittings, a
  sculpted gold animal-head emblem as the centerpiece clasp, braided cords and tassels.
- **Presentation:** one piece, centered, three-quarter view, filling about 80% of the canvas with a small
  margin, on a transparent background (no scene, no shadow on the ground).

What changes for Two Tails (the offensive nekomata theme):

| | Kitsune | Two Tails |
|---|---|---|
| Spirit | fox (kitsune), trickster | two-tailed cat spirit (nekomata), predator |
| Plates | white lacquer | **black lacquer** |
| Cloth | deep violet | **deep crimson** |
| Markings | red and blue fox face strokes | **crimson claw-slash strokes with a thin gold edge** |
| Emblem | gold fox head | **gold nekomata head with bared fangs, its two tails curling around it** |
| Cords | red braid and tassels | **black-and-gold braid, crimson tassels** |
| Edges | smooth, rounded | **sharper, angled plate edges; claw or fang points where the piece allows** |

**Avoid** (franchise association, RUL-2026-10-22-001): blue fire or blue flame of any kind, ghost-fire, a
flaming cat. No fire at all on these icons. Also no text, kanji, glyphs, symbols beyond the sculpted emblem,
frames, UI, characters or body parts (pieces are shown empty, as the Kitsune set is).

## 4. Pieces (proposal)

Each piece mirrors its Kitsune counterpart's silhouette so the sets pair up, then adds the offensive detail.

| # | Piece | Silhouette and offensive detail | Kitsune counterpart |
|---|---|---|---|
| 1 | Shozoku (chest) | a chest guard with black lacquer plates and layered crimson cloth; angular pauldrons with short claw-point edges; crimson claw-slash markings across the chest; gold nekomata emblem at the sash; two crimson sash tails hanging from the waist like twin tails | Kitsune Armor |
| 2 | Zukin (head) | a black ninja hood with cat-ear points, a black lacquer nekomata half-mask over the lower face with a fanged jaw edge, crimson slash markings, gold trim, a crimson tassel at the side | Kitsune Mask |
| 3 | Tekkou (hands) | a single armored gauntlet like the Kitsune one: black lacquer forearm plate, crimson cloth, gold nekomata emblem at the wrist, and three short curved claw blades over the knuckles | Kitsune Gauntlets |
| 4 | Tabi (legs) | a pair of leg guards like the Kitsune pants: crimson wrapped cloth, black lacquer greaves with angled edges and claw-slash markings, gold knee caps, two crimson streamers at the hip like twin tails | Kitsune Pants |
| 5 | Jaki-Tabi (feet) | a pair of split-toe boots like the Kitsune tabi-shoes: black lacquer shin plates, crimson cloth, gold trim, short claw points at each toe cap | Kitsune Tabi-Shoes |

Distinction rules: only the Shozoku and Tabi carry the twin-tail streamers; only the Tekkou has knuckle
blades; the emblem appears on the Shozoku and Tekkou only (as on the Kitsune armor and gauntlets).

## 5. Spec values (`targets.ICON`)

| Field | Value |
|---|---|
| aspect | 1:1 (tolerance 2%) |
| recommended source | 256x256 (minimum 160 px wide) |
| delivered / displayed width | 125 px / 160 px |
| format | WebP, lossless |
| byte ceiling | 460,800 bytes |
| alpha | required (item icon): native transparency preferred; otherwise a true flat lime `#00FF00` key over the whole canvas |
| padding | transparent margin so the rarity frame reads |

## 6. Process

1. **Shozoku first** (it carries the emblem, plates, cloth and markings). One image per session; the
   director approves it, and it locks the rendering and palette for the other four.
2. Pieces 2 to 5, each with the matching Kitsune icon plus the approved Shozoku as references (style and
   construction only, never their silhouettes).
3. Two wrong-subject results in one session: close it and start clean.
4. **Raw QC:** one piece, empty (no body), black lacquer and crimson cloth, gold nekomata details, no fire
   or blue flame, background truly transparent or flat lime, the piece clearly the same family as Kitsune.
5. **Intake (Fable):** key or keep native alpha, clamp spill, pad to square, lossless WebP, check edges on a
   dark composite, `artpreflight.py --type ICON`, then one suggest-mode ticket (one suggestion per piece,
   icon only).

## 7. Delivery

Return each approved original under its exact filename (section 2); a correction gets a fresh name (`_b`,
`_c`). Include a ledger row per file: filename, type `ICON`, pixel size, bytes.
