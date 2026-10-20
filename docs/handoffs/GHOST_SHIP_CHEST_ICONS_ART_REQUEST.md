# Art request: Ghost Ship chest icons (12)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-20)
- **Status:** APPROVED as written by dauntless, 2026-10-20 (RUL-2026-10-20-002): the family motifs,
  tier ladder, Ornate gold accent and Mystery treatment below. The rendered style is still locked
  by the director's visual approval of icons 1 and 2.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one asset per generation session).
  Spec authority: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `ICON`.
- **Live-game requests/writes:** 0. Nothing here uploads anything.

## 1. Why

Ten of these chests are the rewards of the Ghost Ship (Hunt) and Ghost Ship (Gather) quests: each
quest gives its own Common, Rare, Epic and Legendary tier plus Ornate and Mystery. The Rusted pair is
not a quest reward, but uses the same old icons and is included so the set stays consistent. The
quests got the Ghost Ship / Skyglass art update (`art/ghost_ship_skyglass/`); the chests did not, and
still use the older pixel-art icons. Two further problems:

- **Hunter's and Gatherer's chests are indistinguishable.** At every tier the two share the exact same
  image file, so a player cannot tell them apart in the inventory, although one holds creature
  materials and the other herbs and ores.
- **Mystery Chest** carries a painted red question mark, and **Ornate Chest** is drawn open with
  treasure spilling out. Both break the icon rules (no symbols or text, no open lids or spilled
  contents).

The Mystery Chest can also roll the **Skyglass Reliquary**, which is already in the new style. The new
chests must read as the same family as the Reliquary without looking like it.

## 2. Targets

| # | Item | Holds | Delivery filename |
|---|---|---|---|
| 1 | Common Hunter's Chest | Common hunting materials | `icon-gs-chest-hunter-common.webp` |
| 2 | Common Gatherer's Chest | Common gathering materials | `icon-gs-chest-gatherer-common.webp` |
| 3 | Rare Hunter's Chest | Rare hunting materials | `icon-gs-chest-hunter-rare.webp` |
| 4 | Rare Gatherer's Chest | Rare gathering materials | `icon-gs-chest-gatherer-rare.webp` |
| 5 | Epic Hunter's Chest | Epic hunting materials | `icon-gs-chest-hunter-epic.webp` |
| 6 | Epic Gatherer's Chest | Epic gathering materials | `icon-gs-chest-gatherer-epic.webp` |
| 7 | Legendary Hunter's Chest | Legendary hunting materials | `icon-gs-chest-hunter-legendary.webp` |
| 8 | Legendary Gatherer's Chest | Legendary gathering materials | `icon-gs-chest-gatherer-legendary.webp` |
| 9 | Rusted Hunter's Chest | Furs, pelts, shells, antlers; small chance of Rare Jewels | `icon-gs-chest-hunter-rusted.webp` |
| 10 | Rusted Gatherer's Chest | Herbs, ores, Mosswolf Tuft; small chance of Rare Jewels | `icon-gs-chest-gatherer-rusted.webp` |
| 11 | Ornate Chest | Imperial Gold, Unobtanium, Rare Jewels, Lion Token | `icon-gs-chest-ornate.webp` |
| 12 | Mystery Chest | The Common to Legendary Hunter's and Gatherer's chests, Ornate, Mystery itself and the Skyglass Reliquary (not the Rusted pair) | `icon-gs-chest-mystery.webp` |

Ids and current icon URLs are in the 2026-10-20 public read and are added by script when the release
manifest is built; they are not needed to draw.

## 3. Style lock (from the approved Ghost Ship set)

Taken from the director-approved icons in `art/ghost_ship_skyglass/` (crown, crystal, filament,
katana, reliquary, serum):

- near-black iron and dark wood, low overall value; blackened iron banding with rivets;
- **one accent: pale cyan skyglass crystal**, faceted, with a soft inner glow;
- engraved four-point star rune motif on metal (sparingly);
- painted rendering with a crisp dark outline, soft cool rim light, no hard cast shadow;
- 3/4 view at eye level, the same camera as the Reliquary; transparent background.

**References per session (pass the actual image bytes, individually, never a collage):**
1. `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`: **style/material only**.
2. After approval, icon 1 (and from icon 3 on, the approved twin of the same family): **style and
   family motif only**.

Do not pass the old pixel-art chest icons; they would pull the generator back to the old style.

## 4. Design proposal (director to approve)

**Silhouette.** A classic domed-lid chest, like the current icons. This keeps tiers recognisable and
separates the set from the Reliquary, which is a flat-lidded box with a central vertical crystal clasp.

**Family motif** (must read at 125 px):

| Family | Brand on the front panel, in skyglass light | Wrap |
|---|---|---|
| Hunter's | three parallel claw gouges | a leather strap with a bone or fang clasp |
| Gatherer's | a single leaf | a coiled rope binding, a small sprig tucked under it |

**Tier ladder** (same camera and size at every tier; escalation by material, ornament and crystal):

| Tier | Treatment |
|---|---|
| Rusted | pitted, corroded iron, flaking bands, cracked dull crystal, no glow |
| Common | plain blackened iron bands, one small crystal clasp, no glow |
| Rare | reinforced bands with steel rivets, brighter crystal clasp, faint glow along the lid seam |
| Epic | silver-trimmed bands, a larger faceted crystal, the family brand glowing |
| Legendary | silver filigree, a small skyglass crystal cluster crowning the lid, the brightest glow (still rim light, never a halo) |

**Ornate Chest.** The grandest chest in the set, closed: heavy silver filigree and several inset
skyglass gems. Proposal: allow **aged gold** as a second accent, because its loot is Imperial Gold;
otherwise it stays skyglass-only.

**Mystery Chest.** Closed and sealed: crossed chains and a heavy lock, with skyglass mist curling from
the lid seam. **No question mark**, since symbols and lettering are out. If the director wants a
"?" kept, that is an explicit exception.

## 5. Spec values (`targets.ICON`)

| Field | Value |
|---|---|
| aspect | 1:1, tolerance 2% (the game stretches icons; non-square distorts) |
| recommended source | 256x256 (minimum 160 px wide) |
| delivered / displayed width | 125 px / 160 px |
| format | WebP, lossless |
| byte ceiling | 460,800 bytes |
| padding | transparent margin so the rarity frame behind the icon still reads |
| background | native transparency preferred; otherwise lime `#00FF00` key (skyglass is cyan, so lime is safe) |

## 6. Prompts

**Shared style clause (proposal; icon 1 locks it):**
`game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object`

**Shared negative:**
`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Subject lines** (one per session; append the style clause, then the background clause):

| # | Subject |
|---|---|
| 1 | a closed domed-lid chest of plain blackened iron bands on dark wood, one small skyglass crystal clasp, a leather strap with a bone fang clasp, three parallel claw gouges branded on the front panel |
| 2 | a closed domed-lid chest of plain blackened iron bands on dark wood, one small skyglass crystal clasp, a coiled rope binding with a small sprig tucked under it, a single leaf branded on the front panel |
| 3-8 | as 1 or 2, with the tier treatment from section 4 |
| 9-10 | as 1 or 2, with the Rusted treatment |
| 11 | a closed, grand domed-lid treasure chest with heavy silver filigree and several inset skyglass gems, aged gold trim |
| 12 | a closed domed-lid chest bound by crossed iron chains and a heavy lock, faint skyglass mist curling from the lid seam |

**Background clause:** `transparent background` where the generator supports it; otherwise
`on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`.

## 7. Process

1. **Icon 1 (Common Hunter's) first.** One image per session. Show it to the director and wait for
   approval: it locks the style clause and the Hunter's motif.
2. **Icon 2 (Common Gatherer's)** with icon 1 as a reference. Director approval locks the Gatherer's
   motif and confirms the twins read differently at 125 px.
3. Then the Rare, Epic, Legendary and Rusted pairs, then Ornate, then Mystery. Each session gets the
   Reliquary plus the approved icon of the same family, nothing else.
4. Two wrong-subject results in one session: close it and start clean (protocol section 3).
5. **Raw QC before processing:** square, one complete closed chest, no text or symbols beyond the
   brand, no halo or glow disc, not sitting on a surface, background truly flat or transparent.
6. **Processing at intake:** key or keep native alpha, clamp spill, pad to square, lossless WebP,
   check edges on a dark composite, then `artpreflight.py --type ICON`.

## 8. Delivery and next step

- Return each approved original to the studio with its filename exactly as in section 2. A
  correction gets a fresh name (`_b`, `_c`).
- Include a ledger row per file: filename, type `ICON`, pixel size, bytes.
- After intake and preflight, the twelve icons go to the review desk as one Forge suggest-mode
  ticket (category VISUAL, title "Update icon", one rationale per chest).

## 9. Director decisions

Approved as written on 2026-10-20 (items 1 to 4). Item 5 stays open.

1. Family motifs: claw gouges + leather and fang for Hunter's, leaf + rope and sprig for Gatherer's.
2. The tier ladder in section 4.
3. Aged gold as a second accent on the Ornate Chest.
4. Mystery Chest without a question mark.
5. Separate, not part of this request: all twelve chests are rarity COMMON, including the
   "Legendary" ones. Rarity is a director call.
