# Skyglass art prompts: one paste-ready block per asset

- **For:** the art director (ChatGPT generates; Claude does intake afterwards)
- **Direction:** `docs/handoffs/SKYGLASS_ART_REQUEST.md` (style, palette, tier seals, variant rule, canvas per type,
  return contract). This file only carries the blocks; where it disagrees with the request, the request (and the
  rulings and spec it cites) win.
- **Scope:** every asset still NEEDS ART in `docs/design/SKYGLASS_ART_AUDIT.md` after RUL-2026-10-30-061, plus the
  seven variant-token motif versions. **Register:** `docs/design/skyglass_art/ART_REGISTER.md`.
- **References:** `skyglass_art_refs.zip`, one numbered folder per reference set; this file is also at the zip root.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (RUL-2026-10-14-001). **Live-game requests/writes:** 0.
  **Credentials:** none.

## How to use

1. Open a **fresh chat for each asset**; paste exactly one block (the text inside the fence) and nothing else.
2. Attach **only the files the block names**, from the zip folder it names, each as its own image (never a folder or sheet).
3. Generate **one candidate at a time**; approve, reject, or ask for a same-subject revision.
4. **Two wrong-subject or wrong-composition results: close the chat** and start a new one with the same block.
5. Return each **approved original unprocessed** (no crop, key, resize or screenshot), named by its code (`IC01_raw_...`).
6. Order: IC01 first in its family; **VT00 must be approved and saved as `VT00_approved.png` before VT01-VT07**.

**Release-blocking (do first if time is short):** IC01-IC07 (every new run's item and quest icon) and PT01 (the public
intro quest needs a scene character). Everything else has a working placeholder live.

## Index

| Family (audit session order) | Codes | Prompts | Zip folder(s) |
|---|---|---|---|
| 1. Chart, page and reagent icons | IC01-IC07 | 7 | `01_chart_icons`, `02_seal_icons`, `03_reagent_icons` |
| 2. Reward icons | IC08, VT00-VT07, IC09-IC12 | 13 | `02_seal_icons`, `04_reward_icons`, `05_variant_token` |
| 3. Variant skins | VS01-VS19 | 19 | `10_variant_aetherion` ... `22_variant_whispering_dawnblade` |
| 4. Jutsu icons | JI01-JI04 | 4 | `30_jutsu_icons` |
| 5. Animation raw layers | AN01-AN09 (AN09 optional) | 9 | `35_fx_layers` |
| 6. Salvager portrait | PT01 | 1 | `25_salvager_portrait` |
| 7. Crownhold avatars | AV01-AV08 | 8 | `40_crew_avatars` |
| 8. Crownhold release scenes | SC01-SC06 | 6 | `50_ship_scenes` |
| 9. Haul chests, Legendary | PC07-PC08 | 2 | attach your Epic chest image |
| 10. Quest icons | QI01 | 1 | `01_chart_icons` |
| **Total** | | **68** | |

Not prompted here: the 6 recolours Claude derives by script and the 32 finished files that only need uploading (both
listed at the end); the violet Binding blast (reuses `anim_chain_wrap_v1.webp`, RUL-2026-10-30-061 item 10); the
neutral Elemental Tool Pouch redraw (still a director call, audit D4); the 13 deferred Crownhold scenes.

---

## 1. Chart, page and reagent icons (release-blocking)

One shared chart family with the live chart icons; seals by tier (request §4). The live charts are not redrawn.

### IC01 · Tide Chart

- **Target:** Tide Chart, item `H1s2IwtZ5JqgPEoJ55IVj` · ICON (`item.image`) · Common, plain seal · lime key · priority: **release-blocking**
- **Attach folder:** `01_chart_icons/`: `chart_drowned_foundry.png` (STYLE-ONLY: the live Skyglass chart family, its dark chart paper, roller, pale cyan linework and rendering; do not copy its ship plan or layout); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC01_raw_icon-tide-chart.png`

```text
Target: Tide Chart, one square game item icon for The Ninja RPG.
References attached: 1. chart_drowned_foundry.png: STYLE-ONLY: the live Skyglass chart family, its dark chart paper, roller, pale cyan linework and rendering; do not copy its ship plan or layout. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Tide Chart: the Wayfinder's tide table, marked where the low tide opens the wreck's lower hull. A half-unrolled sheet of dark weathered chart paper on a short wooden roller, drawn in pale cyan lines: a simple coastline, the outline of a beached ship's hull, and three wavy tide bands, the lowest band marked with one small cyan cross at the hull. A small undyed dark wax dab at one corner (Common: plain seal). The same family as the attached chart, but clearly a tide table, not a ship plan. Lines and marks only, no writing or numbers.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC02 · Watch Roster

- **Target:** Watch Roster, item `yE8TwzygWZSNoZD5x97rW` · ICON (`item.image`) · Common, plain seal · lime key · priority: **release-blocking**
- **Attach folder:** `01_chart_icons/`: `chart_captains_watch.png` (STYLE-ONLY: the live Skyglass chart family, its paper, ink and rendering; do not copy its subject or layout); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC02_raw_icon-watch-roster.png`
- **Note:** Must read apart from IC06 (a torn loose ledger page tied with a cord).

```text
Target: Watch Roster, one square game item icon for The Ninja RPG.
References attached: 1. chart_captains_watch.png: STYLE-ONLY: the live Skyglass chart family, its paper, ink and rendering; do not copy its subject or layout. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Watch Roster: the Deck Warden's duty roster, with a new name at the bottom in fresh ink. A vertical paper roster scroll hanging open from a short dark wooden roller with a rope hanger; rows of short unreadable brush strokes in faded grey ink, and the last row fresh, glossy black ink still wet. A small undyed dark wax dab at the bottom edge (Common: plain seal). It reads as a list of names without a single legible character.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC03 · Reliquary Seal

- **Target:** Reliquary Seal, item `sVqDdYUJIxxRYbmKbbxo0` · ICON (`item.image`) · Epic, gold seal · lime key · priority: **release-blocking**
- **Attach folder:** `02_seal_icons/`: `anchor_reliquary.png` (MATERIAL-ONLY: dark iron, bands and rivets; do not copy its chest shape); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC03_raw_icon-reliquary-seal.png`
- **Note:** Claude recolours the wax seal to rot-green by script for the Rotted Reliquary Seal, so keep it one isolated blob. Must read apart from IC12 Countermand (an upright rectangular tablet).

```text
Target: Reliquary Seal, one square game item icon for The Ninja RPG.
References attached: 1. anchor_reliquary.png: MATERIAL-ONLY: dark iron, bands and rivets; do not copy its chest shape. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Reliquary Seal: the seal of the iron reliquary chained behind the Sealwright. A heavy round seal disc of dark storm-grey iron with a raised riveted rim, a faceted lump of pale cyan skyglass set at its heart, hanging from a short length of heavy black chain broken at its end. One small deep amber-gold wax seal is pressed onto the rim (Epic). The wax seal is the only gold on the object: one compact, separate blob that does not touch the skyglass.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (the one exception: the small amber-gold wax seal named in the subject); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC04 · The Last Heading

- **Target:** The Last Heading, item `s1mYHuKqw2YuzIzxVwU-_` · ICON (`item.image`) · Epic, gold seal · lime key · priority: **release-blocking**
- **Attach folder:** `01_chart_icons/`: `chart_drowned_foundry.png` (STYLE-ONLY: the live Skyglass chart family, its dark chart paper, roller, pale cyan linework and rendering; do not copy its ship plan or layout); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC04_raw_icon-the-last-heading.png`
- **Note:** Claude recolours the wax seal to rot-green by script for The Rotted Heading, so keep it one isolated blob.

```text
Target: The Last Heading, one square game item icon for The Ninja RPG.
References attached: 1. chart_drowned_foundry.png: STYLE-ONLY: the live Skyglass chart family, its dark chart paper, roller, pale cyan linework and rendering; do not copy its ship plan or layout. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: The Last Heading: the Wayfinder's final course, the night the ship came down. A sheet of dark chart paper, its edges scorched black and curled, a few small charred holes, crossed corner to corner by one bold pale cyan heading line that ends in an arrowhead; no other markings. One small deep amber-gold wax seal at the lower corner (Epic), the only gold on the object, separate from the cyan line. Scorched, not burning: no flames, smoke or glowing embers.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (the one exception: the small amber-gold wax seal named in the subject); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC05 · Core Rot

- **Target:** Core Rot, item `KuqLeFB12BdB-0s5O1udk` · ICON (`item.image`) · Rare; no seal (reagent) · magenta key · priority: **release-blocking**
- **Attach folder:** `03_reagent_icons/`: `anchor_skyglass_filament.png` (MATERIAL-ONLY: how a bundle of skyglass is lashed with rope; not its clean crystals or its shape); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC05_raw_icon-core-rot.png`

```text
Target: Core Rot, one square game item icon for The Ninja RPG.
References attached: 1. anchor_skyglass_filament.png: MATERIAL-ONLY: how a bundle of skyglass is lashed with rope; not its clean crystals or its shape. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Core Rot: what the Core leaves behind when it rebuilds an impression badly. One holdable, fist-sized lump: splintered dark wet ship's timber and frayed black rope with chunks of cloudy, milky skyglass caught inside, all bound tight by a few turns of wet rope finished with a knot; a faint sickly bile-green sheen on the wet surfaces. A compact closed shape, not a pile, puddle or loose chunks. No tier seal (a reagent).
Background: transparent. If transparency is not available, a true solid flat magenta chroma key (#FF00FF) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no magenta spill on the object. (Magenta, not lime: this subject carries green.)
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC06 · Ledger Page (base; = Ledger Page: The Trophy Hold)

- **Target:** Ledger Page (base; = Ledger Page: The Trophy Hold), item `JvrytTOdR1voVCoo3fckK` · ICON (`item.image`) · Legendary; no tier seal (one coloured cord for the recolours) · lime key · priority: **release-blocking**
- **Attach folder:** `01_chart_icons/`: `chart_captains_watch.png` (STYLE-ONLY: the live Skyglass chart family, its paper, ink and rendering; do not copy its subject or layout); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC06_raw_icon-ledger-page.png`
- **Note:** This base is also the Trophy Hold page. Claude recolours the cord and wax dab by script for The Bone Store and The Snare Room, so keep them one solid colour and isolated.

```text
Target: Ledger Page, one square game item icon for The Ninja RPG.
References attached: 1. chart_captains_watch.png: STYLE-ONLY: the live Skyglass chart family, its paper, ink and rendering; do not copy its subject or layout. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Ledger Page: a page torn from the Arsenal Keeper's ledger. A single sheet of yellowed off-white washi paper, creased, with a ragged torn left edge; columns of unreadable brush strokes, several short entries struck through with a line and written again beside them (every due date crossed out). The page is folded once and tied with one thin cord in a single solid deep crimson, with a small crimson wax dab where the cord is knotted. The cord and the wax dab are the only crimson on the image, compact and separate from everything else. No other seal (Legendary: the game's frame does it).
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC07 · Stores Manifest (base; = Stores Manifest: The Overgrown Stores)

- **Target:** Stores Manifest (base; = Stores Manifest: The Overgrown Stores), item `nLG6TK48xlyZ_t9R28QsY` · ICON (`item.image`) · Legendary; no tier seal (one coloured cord for the recolours) · lime key · priority: **release-blocking**
- **Attach folder:** `01_chart_icons/`: `chart_drowned_foundry.png` (STYLE-ONLY: the live Skyglass chart family, its dark chart paper, roller, pale cyan linework and rendering; do not copy its ship plan or layout); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC07_raw_icon-stores-manifest.png`
- **Note:** This base is also the Overgrown Stores page. Claude recolours the cord and wax dab by script for The Ore Vault and The Bloom Cellar. Must read apart from IC06 (a torn loose page).

```text
Target: Stores Manifest, one square game item icon for The Ninja RPG.
References attached: 1. chart_drowned_foundry.png: STYLE-ONLY: the live Skyglass chart family, its dark chart paper, roller, pale cyan linework and rendering; do not copy its ship plan or layout. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Stores Manifest: the quartermaster's manifest for the lower stores, with skyglass grown through every line. A stiff sheet of dark brown paper folded in three and half open, neat columns of unreadable brush strokes, and small faceted pale cyan skyglass crystals grown up through the paper between the lines. Tied with one thin cord in a single solid rust-orange, with a small rust-orange wax dab at the knot. The cord and the wax dab are the only orange on the image, compact and separate. No other seal (Legendary: the game's frame does it).
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 2. Reward icons

Skyglass Token first, then the variant-token base and its seven motifs, then the jar, the two chests and Countermand
(low priority, last).

### IC08 · Skyglass Token

- **Target:** Skyglass Token, item `nzCW7A-_AuYMzBs2wClnM` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `04_reward_icons/`: `emblem_skyglass_star.png` (SUBJECT for the stamp only: the Skyglass emblem, a four-point star in a diamond; not its colours or square layout); `anchor_skyglass_crystal.png` (MATERIAL-ONLY: skyglass, here made clouded and milky; do not copy the crystal shape)
- **Return as:** `IC08_raw_icon-skyglass-token.png`
- **Note:** Must not read like the Lion Token (a live gold token).

```text
Target: Skyglass Token, one square game item icon for The Ninja RPG.
References attached: 1. emblem_skyglass_star.png: SUBJECT for the stamp only: the Skyglass emblem, a four-point star in a diamond; not its colours or square layout. 2. anchor_skyglass_crystal.png: MATERIAL-ONLY: skyglass, here made clouded and milky; do not copy the crystal shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Skyglass Token: a token pressed from clouded skyglass and stamped with the four-point star. A thick round token of cloudy, milky pale-cyan skyglass with a faceted edge, its face stamped with the Skyglass emblem (a four-point star inside a diamond) as in the attached emblem; a little cloudiness inside and one small chip at the rim. Seen three-quarter so its thickness shows. Not a gold coin, no animal, no metal rim. No tier seal (Legendary: the game's frame does it).
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT00 · Boss variant token, BASE (not an item; the base VT01-VT07 attach)

- **Target:** Boss variant token BASE (not an item; VT01-VT07 attach it), no live id · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing (gates VT01-VT07)**
- **Attach folder:** `05_variant_token/`: `anchor_reliquary.png` (MATERIAL-ONLY: dark iron, bands and rivets; do not copy its chest shape); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `VT00_raw_icon-variant-token-base.png`
- **Note:** AFTER APPROVAL: save the approved original into `05_variant_token/` as `VT00_approved.png`. VT01-VT07 attach it; do not start them before it exists.

```text
Target: Boss variant token, BASE, one square game item icon for The Ninja RPG.
References attached: 1. anchor_reliquary.png: MATERIAL-ONLY: dark iron, bands and rivets; do not copy its chest shape. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: A boss trophy token, the shared base for seven variant tokens. An upright trophy tag of dark storm-grey iron: a tall rounded rectangle with clipped corners, thick enough to show its edge, a riveted rim, and a hole at the top threaded with a short knotted deep-indigo cord. Its face holds a recessed oval window of smooth pale-cyan skyglass, left completely blank (a motif is set into it later). Worn, weighty, hand-forged. It must not read as a round coin or a medal.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT01 · Captain's Gunbai

- **Target:** Captain's Gunbai, item `vltFmOTgOyqssIpNXvT37` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT01_raw_icon-variant-token-captains-command-fan.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Captain's Gunbai, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a small gunbai war fan seen face-on: a rounded paddle on a short haft with a tiny four-point star at its centre. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT02 · Rotbloom

- **Target:** Rotbloom, item `-7dQs2qwokuNSAS2c3X8Q` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT02_raw_icon-variant-token-rot-bloom-reaper.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Rotbloom, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a curved sickle blade with clusters of cloudy, barnacle-like skyglass along its back and a short loop of rope chain. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT03 · Forgefists

- **Target:** Forgefists, item `d96tj122ex6BnzhMDwy0s` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT03_raw_icon-variant-token-wardens-forge-fists.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Forgefists, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a clenched armoured gauntlet with blunt maul-head knuckle plates. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT04 · Wayfinder

- **Target:** Wayfinder, item `giSqzJqE6YdsrnOoy1KLV` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT04_raw_icon-variant-token-wayfinders-heading.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Wayfinder, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a compass rose with one long needle pointing up and to the right. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT05 · The First Blade

- **Target:** The First Blade, item `5rpvgpKckgmN-vXjzJpb8` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT05_raw_icon-variant-token-the-first-blade.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: The First Blade, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, an upright sword with a long cord wound round its grip, the cord ends streaming sideways as if in wind. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT06 · Sealscript

- **Target:** Sealscript, item `3ZR700BAWr_Pd3Eqnu1c9` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT06_raw_icon-variant-token-sealwrights-seal.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Sealscript, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a round seal disc ringed with fine engraved lines, a small four-point star at its centre. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT07 · Crownbreaker

- **Target:** Crownbreaker, item `pqKpEqo-x6BHTjxTRUEfD` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT07_raw_icon-variant-token-crownbreaker.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: the frost-shard token, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, three short broken frost-point shards splayed apart, a crack running between them. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC09 · The Little Horror's Jar

- **Target:** The Little Horror's Jar, no live id yet · ICON (`item.image`) · Legendary; no seal · magenta key · priority: **player-facing**
- **Attach folder:** `04_reward_icons/`: `anchor_skyglass_serum.png` (MATERIAL-ONLY: how glass, stopper and binding are rendered; do not copy its vial shape); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC09_raw_icon-little-horrors-jar.png`

```text
Target: The Little Horror's Jar, one square game item icon for The Ninja RPG.
References attached: 1. anchor_skyglass_serum.png: MATERIAL-ONLY: how glass, stopper and binding are rendered; do not copy its vial shape. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: The Little Horror's Jar: the ship's mascot, sealed in a jar; the Core tried to remember it, and this is what came back. A small squat jar of thick clear old glass with a wooden stopper bound down with rope, a blank paper seal tag pasted across the stopper. Inside, a small round rot-and-skyglass creature: a dark wet blob body with bile-green mottling, a few cloudy skyglass crystals on its back, two lit cyan eyes and a wide grin with one tooth too many, pressed against the glass with one small paw. Oddly cute, not gory. No tier seal (Legendary: the game's frame does it).
Background: transparent. If transparency is not available, a true solid flat magenta chroma key (#FF00FF) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no magenta spill on the object. (Magenta, not lime: this subject carries green.)
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC10 · Galley Stores

- **Target:** Galley Stores, item `D-QTnbjgTyIVc593zzdSB` · ICON (`item.image`) · Rare, cyan seal · lime key · priority: **player-facing**
- **Attach folder:** `04_reward_icons/`: `unmarked_cargo.png` (STYLE-ONLY: the live Skyglass cargo family, its wood, rope, iron and rendering; do not copy its shape); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC10_raw_icon-galley-stores.png`

```text
Target: Galley Stores, one square game item icon for The Ninja RPG.
References attached: 1. unmarked_cargo.png: STYLE-ONLY: the live Skyglass cargo family, its wood, rope, iron and rendering; do not copy its shape. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Galley Stores: the galley still stocks a larder for a crew that does not eat. A straw rice bale (tawara) bound with rope rings, with a small wooden tag lashed to it, the tag branded with the Skyglass emblem (a four-point star in a diamond) in pale cyan; one small pale skyglass-cyan wax seal pressed on the tag's cord (Rare: cyan seal).
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC11 · Crown's Hoard

- **Target:** Crown's Hoard, no live id yet · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `04_reward_icons/`: `sealed_treasury.png` (STYLE-ONLY: the live Skyglass chest family, its lacquer, iron bands and rendering; do not copy its shape); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `IC11_raw_icon-crowns-hoard.png`
- **Note:** The prompt never says "crown" (it draws crowns, RUL-2026-10-26-003). Must read apart from the live Sealed Treasury and Skyglass Coffer.

```text
Target: a castle treasury chest (the Hoard), one square game item icon for The Ninja RPG.
References attached: 1. sealed_treasury.png: STYLE-ONLY: the live Skyglass chest family, its lacquer, iron bands and rendering; do not copy its shape. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: A mountain castle's own treasury, gathered beneath the throne. A large, heavy treasure chest of black lacquer bound with wide storm-grey iron bands and studs, broader and taller than a coffer; the lid slightly open on a thin glint of dull silver coins and one pale cyan skyglass token; a small sealed ceramic jar roped to the lid; the Skyglass emblem (a four-point star in a diamond) in pale cyan on the iron lock plate. No tier seal (Legendary: the game's frame does it).
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### IC12 · Countermand

- **Target:** Countermand, item `W3lOjQhhIPUYPkIZmiNum` · ICON (`item.image`) · AI-held; no seal · lime key · priority: **low (AI-held; players see it only in battle)**
- **Attach folder:** `02_seal_icons/`: `emblem_skyglass_star.png` (SUBJECT for the mark only: the Skyglass emblem, a four-point star in a diamond; not its colours, size or square layout); `anchor_reliquary.png` (MATERIAL-ONLY: dark iron, bands and rivets; do not copy its chest shape)
- **Return as:** `IC12_raw_icon-countermand.png`
- **Note:** Must read apart from IC03 Reliquary Seal (a round iron disc on a broken chain).

```text
Target: Countermand, one square game item icon for The Ninja RPG.
References attached: 1. emblem_skyglass_star.png: SUBJECT for the mark only: the Skyglass emblem, a four-point star in a diamond; not its colours, size or square layout. 2. anchor_reliquary.png: MATERIAL-ONLY: dark iron, bands and rivets; do not copy its chest shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Countermand: the castle's command seal. An upright rectangular command tablet of black lacquered wood framed in dull iron, hanging from a short dark cord, its face carved with the Skyglass emblem (a four-point star in a diamond) inlaid in pale cyan skyglass. No gold frame. No tier seal (an AI-held item).
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 3. Variant skins (19)

One weapon per chat with its live icon as SUBJECT. Do the Skyglass set (VS01-VS12) first, then the boss set
(VS13-VS19) beside it, so the six shared bases can be compared at 125 px: Aetherion VS01/VS17, Thornsilver VS02/VS19,
Stormrender VS04/VS16, Oathbinder VS05/VS14, The Unwritten VS07/VS13, Warden's Bracers VS09/VS15. Art lines:
`SKYGLASS_TEXT.md` §5. No tier seal on any variant.

### VS01 · Windward

- **Target:** Windward, item variant `MXAAH-1fwPfyDJg2FnE8t` on Aetherion (`PhP5ZEF5iVa97jcumJ15c`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `10_variant_aetherion/`: `base_aetherion.png` (SUBJECT: the live Aetherion icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS01_raw_icon-variant-gale-watch-aetherion.png`
- **Note:** Shares its base with VS17 The First Blade: the two must read clearly apart at 125 px.

```text
Target: Windward, a skin of the weapon Aetherion, one square game item icon for The Ninja RPG.
References attached: 1. base_aetherion.png: SUBJECT: the live Aetherion icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Windward. Keep the attached Aetherion's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the blue fire of the blade recoloured storm-white with pale grey edges (wind, not flame); the grip rewrapped in weathered off-white sailcloth; a cluster of three faceted skyglass shards growing from the guard; a small four-point skyglass star in the pommel. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (The First Blade: a long grey-blue cord bound round the grip with trailing ends, a short inlay at the blade base, brass fittings); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS02 · Riptide

- **Target:** Riptide, item variant `YNhKQmKUjfVIPQkGlNO41` on Thornsilver (`MQ5mJqH-5MkQdtLGSZ5nb`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `11_variant_thornsilver/`: `base_thornsilver.png` (SUBJECT: the live Thornsilver icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS02_raw_icon-variant-tidewater-thornsilver.png`
- **Note:** Shares its base with VS19 Crownbreaker: the two must read clearly apart at 125 px.

```text
Target: Riptide, a skin of the weapon Thornsilver, one square game item icon for The Ninja RPG.
References attached: 1. base_thornsilver.png: SUBJECT: the live Thornsilver icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Riptide. Keep the attached Thornsilver's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the steel recoloured deep sea-green, wet and dark; a crust of white salt and small grey barnacles climbing the first third of the blade from the guard; a row of round skyglass beads along the spine. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (the frost-shard skin: three broken frost-point shards set in the crossguard); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS03 · Nightreaver

- **Target:** Nightreaver, item variant `mtx4YmUu-wkKGwnOPVbYS` on Night's Testament (`osJq3k77YPGoFWgof12FQ`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `12_variant_nights_testament/`: `base_nights_testament.png` (SUBJECT: the live Night's Testament icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS03_raw_icon-variant-night-watch-testament.png`

```text
Target: Nightreaver, a skin of the weapon Night's Testament, one square game item icon for The Ninja RPG.
References attached: 1. base_nights_testament.png: SUBJECT: the live Night's Testament icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Nightreaver. Keep the attached Night's Testament's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the round guard rebuilt as a small iron ship's wheel with short spokes; a tiny iron ship's lantern with a pale-cyan skyglass flame hanging from the pommel on a short cord; a broad moon-silver band along the cutting edge of the black blade; one four-point skyglass star at the centre of the wheel. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS04 · Thunderwake

- **Target:** Thunderwake, item variant `_49jp25nHiH-v8ywlRdKH` on Stormrender (`cLXXf8RJv5l9B_gGsYN2a`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `13_variant_stormrender/`: `base_stormrender.png` (SUBJECT: the live Stormrender icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS04_raw_icon-variant-mast-lightning-stormrender.png`
- **Note:** Shares its base with VS16 Wayfinder: the two must read clearly apart at 125 px.

```text
Target: Thunderwake, a skin of the weapon Stormrender, one square game item icon for The Ninja RPG.
References attached: 1. base_stormrender.png: SUBJECT: the live Stormrender icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Thunderwake. Keep the attached Stormrender's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the lightning recoloured from violet to pale cyan-white; the crossguard replaced by a short broken mast spar lashed with rope, a skyglass rod set upright in it; thin cyan crackle lines on the ricasso. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Wayfinder: a round compass rose at the crossguard and an etched route line down the fuller); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS05 · Anchorline

- **Target:** Anchorline, item variant `umsYP0jL3emdVFDdU6Fcd` on Oathbinder (`ttwbJ6ZA5Id-OuBludM27`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `14_variant_oathbinder/`: `base_oathbinder.png` (SUBJECT: the live Oathbinder icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS05_raw_icon-variant-roll-call-oathbinder.png`
- **Note:** Shares its base with VS14 Rotbloom: the two must read clearly apart at 125 px.

```text
Target: Anchorline, a skin of the weapon Oathbinder, one square game item icon for The Ninja RPG.
References attached: 1. base_oathbinder.png: SUBJECT: the live Oathbinder icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Anchorline. Keep the attached Oathbinder's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the chain recoloured weathered iron with rust-orange patches; the spiked ball replaced by a small ship's anchor of dark iron; the white prayer knots replaced by pale-cyan skyglass beads. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Rotbloom: a wet dark rope chain, milky barnacle-like skyglass on the blade back, a rot-stained haft); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS06 · Starfall

- **Target:** Starfall, item variant `1yWEP0r3elIzyScORfot4` on Ink of the Void (`wE1QeldWTjls2Cf43cFjf`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `15_variant_ink_of_the_void/`: `base_ink_of_the_void.png` (SUBJECT: the live Ink of the Void icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS06_raw_icon-variant-chartline-ink-of-the-void.png`

```text
Target: Starfall, a skin of the weapon Ink of the Void, one square game item icon for The Ninja RPG.
References attached: 1. base_ink_of_the_void.png: SUBJECT: the live Ink of the Void icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Starfall. Keep the attached Ink of the Void's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: both limbs recoloured old parchment-white, inlaid with fine cyan skyglass chart lines and one small compass mark; the bowstring becomes tarred rigging rope; a small brass compass charm hanging from the grip. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS07 · The Unwritten Order

- **Target:** The Unwritten Order, item variant `3NH-VreJl9TcqqIYiztn_` on The Unwritten (`m0RZDUDnwQu_0BtOJgHi9`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `16_variant_the_unwritten/`: `base_the_unwritten.png` (SUBJECT: the live The Unwritten icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS07_raw_icon-variant-the-unwritten-order.png`
- **Note:** Shares its base with VS13 Captain's Gunbai: the two must read clearly apart at 125 px.

```text
Target: The Unwritten Order, a skin of the weapon The Unwritten, one square game item icon for The Ninja RPG.
References attached: 1. base_the_unwritten.png: SUBJECT: the live The Unwritten icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: The Unwritten Order. Keep the attached The Unwritten's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the black fan leaves become pale cream paper written with faint unreadable brush strokes, one line left blank, so the fan reads light instead of dark; the outer edge sealed with drops of cyan skyglass wax; the skull charm replaced by a round skyglass seal. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Captain's Gunbai: a rounded black-lacquered gunbai war-fan paddle with a skyglass star at its centre); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS08 · Keelstone

- **Target:** Keelstone, item variant `xFyTBqje5M1_68EqRRoBu` on Gaea's Embrace (`-LzgdTM1yTjlezOyjd-6H`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `17_variant_gaeas_embrace/`: `base_gaeas_embrace.png` (SUBJECT: the live Gaea's Embrace icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS08_raw_icon-variant-keelstone-embrace.png`

```text
Target: Keelstone, a skin of the weapon Gaea's Embrace, one square game item icon for The Ninja RPG.
References attached: 1. base_gaeas_embrace.png: SUBJECT: the live Gaea's Embrace icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Keelstone. Keep the attached Gaea's Embrace's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the shaft becomes dark ship's keel timber with two iron bands and a few grey barnacles; the orange tip crystal recoloured pale skyglass cyan; a heavy iron mooring ring hanging below the head. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS09 · Skyglass Kote

- **Target:** Skyglass Kote, item variant `_tdmHvPnvlnIMLpRnk9GC` on Warden's Bracers (`qTzWEb6tFBv8dl15ztqDO`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `18_variant_wardens_bracers/`: `base_wardens_bracers.png` (SUBJECT: the live Warden's Bracers icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS09_raw_icon-variant-drill-count-bracers.png`
- **Note:** Shares its base with VS15 Forgefists: the two must read clearly apart at 125 px.

```text
Target: Skyglass Kote, a skin of the weapon Warden's Bracers, one square game item icon for The Ninja RPG.
References attached: 1. base_wardens_bracers.png: SUBJECT: the live Warden's Bracers icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Skyglass Kote. Keep the attached Warden's Bracers's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the whole pair made of raw skyglass crystal, faceted, unpolished and gleaming, pale cyan brightening to near-white at the facet edges, with darker cyan depths inside; the plates keep their shapes but read as cut crystal, with rough natural facets and a few jagged crystal points along the cuff edges that change the outline; the straps become thin dark-iron bands binding the crystal; the glyph removed. Skyglass family mark: a short torn deep-indigo pennant knotted at one cuff, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. These are crystal armour, not a blade (director 2026-10-31, RUL-2026-10-31-082); the Skyglass Katana stays the only crystal blade.
It must read clearly apart from its sibling skin on the same base (Forgefists: soot-black forged iron, blunt maul-head knuckle plates, seams of cooled skyglass); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS10 · Lastlight Duskblade

- **Target:** Lastlight Duskblade, item variant `m7Xqe9cD1oB_2vCj1Zvu5` on Eclipsed Dawnblade (`MbPhG5El3UYjS5Bk2K3Bl`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `19_variant_eclipsed_dawnblade/`: `base_eclipsed_dawnblade.png` (SUBJECT: the live Eclipsed Dawnblade icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS10_raw_icon-variant-lastlight-dawnblade.png`
- **Note:** Must also read apart from VS18 Sealscript (a different Dawnblade with engraved lines and a pommel seal disc).

```text
Target: Lastlight Duskblade, a skin of the weapon Eclipsed Dawnblade, one square game item icon for The Ninja RPG.
References attached: 1. base_eclipsed_dawnblade.png: SUBJECT: the live Eclipsed Dawnblade icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Lastlight Duskblade. Keep the attached Eclipsed Dawnblade's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the blade recoloured night-blue steel with a pale edge; a small iron lantern cage set at the base of the blade holding a skyglass core, its soft cyan light contained inside it; the white grip rewrapped in deep indigo. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS11 · Skysail

- **Target:** Skysail, item variant `kD6g1o5qJo3K9r1HeHtiH` on Zephyr's Whisper (`CBp4scJi9XzMKRqxpshwT`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `20_variant_zephyrs_whisper/`: `base_zephyrs_whisper.png` (SUBJECT: the live Zephyr's Whisper icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS11_raw_icon-variant-skysail-whisper.png`

```text
Target: Skysail, a skin of the weapon Zephyr's Whisper, one square game item icon for The Ninja RPG.
References attached: 1. base_zephyrs_whisper.png: SUBJECT: the live Zephyr's Whisper icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Skysail. Keep the attached Zephyr's Whisper's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the fan paper becomes patched off-white sailcloth with visible stitching; the red tassels replaced by deep-indigo cord; thin rigging cords strung between the ribs; the embedded crystal recoloured pale skyglass cyan; if the wind swirl is kept, recolour it storm-grey and keep it compact, inside the margin. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS12 · Hullbreaker

- **Target:** Hullbreaker, item variant `Iew4QFXyfWLPlPoMgeDrz` on Yuki's Frostbite (`Z-JdppXvrSokRymXavpOw`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `21_variant_yukis_frostbite/`: `base_yukis_frostbite.png` (SUBJECT: the live Yuki's Frostbite icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS12_raw_icon-variant-hullbreaker-frostbite.png`

```text
Target: Hullbreaker, a skin of the weapon Yuki's Frostbite, one square game item icon for The Ninja RPG.
References attached: 1. base_yukis_frostbite.png: SUBJECT: the live Yuki's Frostbite icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Hullbreaker. Keep the attached Yuki's Frostbite's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the haft replaced by dark ship's timber with iron rings; a skyglass inlay set into the cheek of the axe head, not the edge. The head keeps its frost colouring, but without the cloud of blue fire around it: the axe silhouette must read, with glow only as a thin edge light. Skyglass family mark: a short torn deep-indigo pennant knotted at the guard, its ends trailing back. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS13 · Captain's Gunbai

- **Target:** Captain's Gunbai, item variant `Deo6Y7dNzaPhOAiWK-4I3` on The Unwritten (`m0RZDUDnwQu_0BtOJgHi9`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `16_variant_the_unwritten/`: `base_the_unwritten.png` (SUBJECT: the live The Unwritten icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS13_raw_icon-variant-captains-command-fan.png`
- **Note:** Shares its base with VS07 The Unwritten Order: the two must read clearly apart at 125 px.

```text
Target: Captain's Gunbai, a skin of the weapon The Unwritten, one square game item icon for The Ninja RPG.
References attached: 1. base_the_unwritten.png: SUBJECT: the live The Unwritten icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Captain's Gunbai. Keep the attached The Unwritten's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the folding fan becomes a gunbai war fan in the same footprint, angle and size: a rounded black-lacquered paddle with a thick iron rim on a short haft (the base's pommel and hanging cord kept), a large four-point star inlaid in pale cyan skyglass filling the centre, faint cyan cracks along the rim. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (The Unwritten Order: the folding fan kept, pale paper leaves with faint strokes and cyan wax on the edge); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS14 · Rotbloom

- **Target:** Rotbloom, item variant `dkkdXbwWFOGSw1nemyK7K` on Oathbinder (`ttwbJ6ZA5Id-OuBludM27`) · ICON (item-variant image) · no tier seal · magenta key · priority: **player-facing**
- **Attach folder:** `14_variant_oathbinder/`: `base_oathbinder.png` (SUBJECT: the live Oathbinder icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS14_raw_icon-variant-rot-bloom-reaper.png`
- **Note:** Shares its base with VS05 Anchorline: the two must read clearly apart at 125 px.

```text
Target: Rotbloom, a skin of the weapon Oathbinder, one square game item icon for The Ninja RPG.
References attached: 1. base_oathbinder.png: SUBJECT: the live Oathbinder icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Rotbloom. Keep the attached Oathbinder's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the chain becomes wet dark rope; clusters of cloudy, milky skyglass grow like barnacles along the back of the blade; the whole weapon stained a sickly bile-green, so it reads green at a glance; ragged strands of rot hanging from the blade. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Anchorline: the black chain kept with neat cyan beads in place of its prayer knots); do not use that design.
Background: transparent. If transparency is not available, a true solid flat magenta chroma key (#FF00FF) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no magenta spill on the object. (Magenta, not lime: this subject carries green.)
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS15 · Forgefists

- **Target:** Forgefists, item variant `3DtT9myjmYY5xNY5mv7Ew` on Warden's Bracers (`qTzWEb6tFBv8dl15ztqDO`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `18_variant_wardens_bracers/`: `base_wardens_bracers.png` (SUBJECT: the live Warden's Bracers icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS15_raw_icon-variant-wardens-forge-fists.png`
- **Note:** Shares its base with VS09 Skyglass Kote: the two must read clearly apart at 125 px.

```text
Target: Forgefists, a skin of the weapon Warden's Bracers, one square game item icon for The Ninja RPG.
References attached: 1. base_wardens_bracers.png: SUBJECT: the live Warden's Bracers icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Forgefists. Keep the attached Warden's Bracers's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the pair reforged in soot-black iron with blunt, oversized maul-head knuckle plates that change the outline; thin seams of cooled pale-cyan skyglass between the plates; any glyph on the plates removed. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Skyglass Kote: the base metal kept, a row of tally notches with tiny cyan studs); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS16 · Wayfinder

- **Target:** Wayfinder, item variant `hkcF8F8RZa71dcLu8im8G` on Stormrender (`cLXXf8RJv5l9B_gGsYN2a`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `13_variant_stormrender/`: `base_stormrender.png` (SUBJECT: the live Stormrender icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS16_raw_icon-variant-wayfinders-heading.png`
- **Note:** Shares its base with VS04 Thunderwake: the two must read clearly apart at 125 px.

```text
Target: Wayfinder, a skin of the weapon Stormrender, one square game item icon for The Ninja RPG.
References attached: 1. base_stormrender.png: SUBJECT: the live Stormrender icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Wayfinder. Keep the attached Stormrender's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the lightning recoloured storm-grey with a single white core line; a large round compass rose of dark iron and cyan skyglass mounted as the crossguard, wider than the blade; a fine etched route line running down the fuller. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Thunderwake: a short skyglass rod upright in the crossguard and cyan crackle on the ricasso); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS17 · The First Blade

- **Target:** The First Blade, item variant `m_CYA2H9XDF_TbMiii8PE` on Aetherion (`PhP5ZEF5iVa97jcumJ15c`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `10_variant_aetherion/`: `base_aetherion.png` (SUBJECT: the live Aetherion icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS17_raw_icon-variant-the-first-blade.png`
- **Note:** Shares its base with VS01 Windward: the two must read clearly apart at 125 px.

```text
Target: The First Blade, a skin of the weapon Aetherion, one square game item icon for The Ninja RPG.
References attached: 1. base_aetherion.png: SUBJECT: the live Aetherion icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: The First Blade. Keep the attached Aetherion's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the blue fire of the blade burned down to dark smoke-grey with one bright pale-cyan line along the edge; the grip bound in a long grey-blue cord whose ends trail out as if in wind; dull brass on the guard and pommel fittings (brass, not gold). Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Windward: a cyan vein down the fuller, an off-white sailcloth grip, a small star pommel); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS18 · Sealscript

- **Target:** Sealscript, item variant `trSVpt_E_BqOJS1geL_Sn` on Whispering Dawnblade (`mqCCZGSfXUNL02B4H6C9R`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `22_variant_whispering_dawnblade/`: `base_whispering_dawnblade.png` (SUBJECT: the live Whispering Dawnblade icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS18_raw_icon-variant-sealwrights-seal.png`
- **Note:** The base is Whispering Dawnblade, not Eclipsed Dawnblade (RUL-2026-10-30-060 item 8). Must read apart from VS10 Lastlight Duskblade.

```text
Target: Sealscript, a skin of the weapon Whispering Dawnblade, one square game item icon for The Ninja RPG.
References attached: 1. base_whispering_dawnblade.png: SUBJECT: the live Whispering Dawnblade icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Sealscript. Keep the attached Whispering Dawnblade's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the blade's rose-gold glow recoloured pale cyan-white; fine dark engraved lines like brushed seal script along the whole blade (decorative strokes only, no legible characters); a large round skyglass seal disc at the pommel; two blank paper seal strips hanging from the guard. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS19 · Crownbreaker

- **Target:** Crownbreaker, item variant `dt6BWKCOfuB3mPLl14-CF` on Thornsilver (`MQ5mJqH-5MkQdtLGSZ5nb`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `11_variant_thornsilver/`: `base_thornsilver.png` (SUBJECT: the live Thornsilver icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS19_raw_icon-variant-crownbreaker.png`
- **Note:** Shares its base with VS02 Riptide: the two must read clearly apart at 125 px.

```text
Target: Frost-Shard Thornsilver, a skin of the weapon Thornsilver, one square game item icon for The Ninja RPG.
References attached: 1. base_thornsilver.png: SUBJECT: the live Thornsilver icon; keep its core form, proportions and angle so the weapon is recognisable; its colours and details change as the Subject says. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Frost-Shard Thornsilver. Keep the attached Thornsilver's core form, proportions and angle so it is recognisably the same weapon, then restyle it boldly so it reads as a new skin, not the base, at 125 px: the blade recoloured frost-white; three long broken frost-point shards of pale skyglass jutting from the crossguard, wider than the blade so they change the outline; the blade itself with no crystal along the edge. Add a thin pale-cyan edge light along the whole outline. Skyglass appears as inlay, shards and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Riptide: wet-dark steel, a row of skyglass beads on the spine, salt crust at the guard); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Thumbnail test: shrunk to 125 px beside the base, this must read as a different skin at a glance, by colour and outline, not only by small details.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 4. Jutsu icons

Player-facing first (Lastlight, Little Maw), then the two AI-only icons. JUTSU_ICON: designed dark background, no key.

### JI01 · Lastlight

- **Target:** Lastlight, jutsu `0F-68bxOXW_LkJnXV0lwT` · JUTSU_ICON (`jutsu.image`) · designed background, no key · priority: **player-facing (the Crownhold pick jutsu)**
- **Attach folder:** `30_jutsu_icons/`: `jutsu_style_bbe_sapphire_command.png` (STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition); `motif_lantern.png` (SUBJECT motif only: the Lastlight Lantern's skyglass core, used for the beam's small source flare; do not draw the whole lantern)
- **Return as:** `JI01_raw_icon-jutsu-lastlight.png`
- **Note:** Must read apart from JI04 Extermination Order (a curved crimson slash running the other diagonal).

```text
Target: Lastlight, one square jutsu icon for The Ninja RPG. Jutsu id 0F-68bxOXW_LkJnXV0lwT.
References attached: 1. jutsu_style_bbe_sapphire_command.png: STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition. 2. motif_lantern.png: SUBJECT motif only: the Lastlight Lantern's skyglass core, used for the beam's small source flare; do not draw the whole lantern. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, laid out like the attached jutsu-icon exemplar: one bold technique filling the square on a designed dark background, the same framing, rendering and detail density. Crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur, no bloom. Readable at 125 px. Square 1024 x 1024.
Action: Lastlight: the castle's final signal turned into a weapon, a skyglass beam that burns through a line of enemies and leaves wounds that resist healing (line shot, length 5; damage, wound, heal cut).
Dominant silhouette: one straight, hard-edged beam of pale cyan-white skyglass light fired from a small lantern-core flare at the lower left, crossing the whole frame to the upper right.
Camera and motion: side-on; the beam runs lower-left to upper-right, the source flare nearest the viewer.
Secondary effect: small ember-red cut marks scattered along the beam's path, fading at the edges (the wound).
Palette: night ink #08080d and deep indigo #1e2d46 behind; the technique in its own colours as named.
Background: a designed opaque dark background (deep indigo night into near-black #08080d), part of the image. No chroma key, no transparency, no checkerboard.
Avoid: no text, letters, kanji, runes, spell circles or floating ornamental symbols; no character, face, body, hands or fingers; no frame, border, UI or watermark; no second technique; no gold; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### JI02 · Little Maw

- **Target:** Little Maw, no live id yet · JUTSU_ICON (`jutsu.image`) · designed background, no key · priority: **player-facing (the Little Horror pet's signature)**
- **Attach folder:** `30_jutsu_icons/`: `jutsu_style_bbe_sapphire_command.png` (STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition); `motif_fx_maw.png` (SUBJECT motif only: the Core Horror's maw of black water and teeth, to be drawn much smaller, rounder and cuter)
- **Return as:** `JI02_raw_icon-jutsu-little-maw.png`
- **Note:** No live jutsu id yet (it ships with the Little Horror's kit).

```text
Target: Little Maw, one square jutsu icon for The Ninja RPG.
References attached: 1. jutsu_style_bbe_sapphire_command.png: STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition. 2. motif_fx_maw.png: SUBJECT motif only: the Core Horror's maw of black water and teeth, to be drawn much smaller, rounder and cuter. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, laid out like the attached jutsu-icon exemplar: one bold technique filling the square on a designed dark background, the same framing, rendering and detail density. Crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur, no bloom. Readable at 125 px. Square 1024 x 1024.
Action: Little Maw: the Little Horror's signature bite; damage, and the target takes more damage for a round.
Dominant silhouette: a small round maw of black seawater rising from below, ringed with crooked pale teeth, one tooth too many, a few chips of cloudy skyglass in the gums, snapping shut; small and oddly cute, not gory.
Camera and motion: front-on at eye level, the maw centred and closing toward the viewer.
Secondary effect: a little splash ring and a few droplets thrown up around it.
Palette: night ink #08080d and deep indigo #1e2d46 behind; the technique in its own colours as named.
Background: a designed opaque dark background (deep indigo night into near-black #08080d), part of the image. No chroma key, no transparency, no checkerboard.
Avoid: no text, letters, kanji, runes, spell circles or floating ornamental symbols; no character, face, body, hands or fingers; no frame, border, UI or watermark; no second technique; no gold; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### JI03 · The Last Directive

- **Target:** The Last Directive, jutsu `GHFMU_DDKvBBp5BEuTeah` · JUTSU_ICON (`jutsu.image`) · designed background, no key · priority: **low (AI-only: the Crowned Captain)**
- **Attach folder:** `30_jutsu_icons/`: `jutsu_style_bbe_sapphire_command.png` (STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition); `motif_fx_frost_ring.png` (SUBJECT motif only: the ring of frost-point skyglass shards; not its layout)
- **Return as:** `JI03_raw_icon-jutsu-the-last-directive.png`
- **Note:** AI-only; the RUL-2026-10-30-061 'default image' rule covers the library jutsu, while the audit keeps this one as low priority.

```text
Target: The Last Directive, one square jutsu icon for The Ninja RPG. Jutsu id GHFMU_DDKvBBp5BEuTeah.
References attached: 1. jutsu_style_bbe_sapphire_command.png: STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition. 2. motif_fx_frost_ring.png: SUBJECT motif only: the ring of frost-point skyglass shards; not its layout. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, laid out like the attached jutsu-icon exemplar: one bold technique filling the square on a designed dark background, the same framing, rendering and detail density. Crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur, no bloom. Readable at 125 px. Square 1024 x 1024.
Action: The Last Directive: the commander's final order to himself; he cannot fall for five rounds and hits harder.
Dominant silhouette: one katana planted point-down, upright in the centre, ringed by tall frost-point skyglass shards blazing white-cyan in a circle around it.
Camera and motion: front-on at eye level, perfectly upright and symmetrical: an unbreakable stand.
Secondary effect: hard white-cyan edge light flaring off every shard.
Palette: night ink #08080d and deep indigo #1e2d46 behind; the technique in its own colours as named.
Background: a designed opaque dark background (deep indigo night into near-black #08080d), part of the image. No chroma key, no transparency, no checkerboard.
Avoid: no text, letters, kanji, runes, spell circles or floating ornamental symbols; no character, face, body, hands or fingers; no frame, border, UI or watermark; no second technique; no gold; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### JI04 · Extermination Order

- **Target:** Extermination Order, jutsu `EqZsaqser8c2-KpVCaXk_` · JUTSU_ICON (`jutsu.image`) · designed background, no key · priority: **low (AI-only: the Crowned Captain)**
- **Attach folder:** `30_jutsu_icons/`: `jutsu_style_bbe_sapphire_command.png` (STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition); `motif_fx_crimson_strike.png` (SUBJECT motif only: the crimson slash and its shards; not its layout)
- **Return as:** `JI04_raw_icon-jutsu-extermination-order.png`
- **Note:** Must read apart from JI01 Lastlight (a straight cyan beam running the other diagonal).

```text
Target: Extermination Order, one square jutsu icon for The Ninja RPG. Jutsu id EqZsaqser8c2-KpVCaXk_.
References attached: 1. jutsu_style_bbe_sapphire_command.png: STYLE-ONLY: the approved jutsu-icon register, its layout, background, rendering and detail density; do not copy its blue blades or composition. 2. motif_fx_crimson_strike.png: SUBJECT motif only: the crimson slash and its shards; not its layout. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, laid out like the attached jutsu-icon exemplar: one bold technique filling the square on a designed dark background, the same framing, rendering and detail density. Crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur, no bloom. Readable at 125 px. Square 1024 x 1024.
Action: Extermination Order: a killing command; damage, an elemental seal and a block on cleansing.
Dominant silhouette: one heavy curved crimson slash cutting down through a blank paper sealing tag, the tag splitting in two with its ink border cracking.
Camera and motion: the slash runs from upper left to lower right, the tag centred and facing the viewer.
Secondary effect: crimson shards flying off along the cut.
Palette: night ink #08080d and deep indigo #1e2d46 behind; the technique in its own colours as named.
Background: a designed opaque dark background (deep indigo night into near-black #08080d), part of the image. No chroma key, no transparency, no checkerboard.
Avoid: no text, letters, kanji, runes, spell circles or floating ornamental symbols; no character, face, body, hands or fingers; no frame, border, UI or watermark; no second technique; no gold; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 5. Animation raw layers

Raw-layer style of `docs/handoffs/PATIENT_ZERO_ANIMATIONS_ART_SESSION_PROMPT.md`: one element per 1254 px canvas,
alpha or magenta, never lime. Palette families from `SKYGLASS_BOSS_ANIMATIONS.md` (heavy = ember, control = violet,
lingering = bile, safe = skyglass cyan). The violet Binding blast reuses `anim_chain_wrap_v1.webp` (no prompt). AN09 is
optional.

### AN01 · cp_command: Ward of Command banner

- **Target:** cp_command: Ward of Command banner · ANIMATION (aura loop on the Captain) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release (every Captain fight uses it)**
- **Attach folder:** `35_fx_layers/`: `fx_ships_bell.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN01_raw_fx_command_banner.png`
- **Note:** Hold the Line / Unbroken Command: the banner snaps in the wind behind the Captain (`SKYGLASS_BOSS_ANIMATIONS.md`). Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: cp_command: Ward of Command banner.
References attached: 1. fx_ships_bell.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette: deep indigo #111b2e #1e2d46 #2f445e, night ink #08080d, storm-grey iron #5c6474, one pale skyglass-cyan accent #98c1cc.
Subject: one tall, narrow nobori command banner of deep indigo cloth on a black lacquered pole with a plain iron finial, the cloth snapping hard to one side in a strong wind, its hem torn, the Skyglass emblem (a four-point star in a diamond) in pale cyan at its centre.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN02 · cc_phase_shift: shockwave flourish

- **Target:** cc_phase_shift: shockwave flourish · ANIMATION (cast flourish) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release**
- **Attach folder:** `35_fx_layers/`: `fx_frost_ring.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN02_raw_fx_phase_shift.png`
- **Note:** The Crowned Captain at 60% and 30%; Claude recolours it by script for the Captain's Last Stand and Ruin Refrain's pulse. The flourish plays over his existing sprite, so it draws no crown. Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: cc_phase_shift: shockwave flourish.
References attached: 1. fx_frost_ring.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette (safe / skyglass): skyglass cyan #98c1cc brightening to near-white, deep indigo #1e2d46 shadow.
Subject: a flat shockwave ring of pale white-cyan light seen slightly from above, with frost-point skyglass shards flung outward along it; the centre empty.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN03 · cp_gunwale: Raise the Gunwale barrier

- **Target:** cp_gunwale: Raise the Gunwale barrier · gameAsset STATIC or ANIMATION (barrier sprite) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release**
- **Attach folder:** `35_fx_layers/`: `fx_broadside.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN03_raw_fx_gunwale_barrier.png`
- **Note:** The Captain's phase-2 barrier; the Sentinel's Shell Wall shares this sprite (RUL-2026-10-30-061 item 10). Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: cp_gunwale: Raise the Gunwale barrier.
References attached: 1. fx_broadside.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette: dark ship timber #413335 #624c49, storm-grey iron #5c6474 #86858a, rope #4c444c, off-white paper tags, one pale skyglass-cyan accent #98c1cc.
Subject: a short curved wall of stacked dark ship's timbers lashed with rope and bound with iron bands, blank paper seal tags pasted across the planks, seen front-on at eye level.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN04 · ch_enrage: The Core Rebuilds aura

- **Target:** ch_enrage: The Core Rebuilds aura · ANIMATION (aura loop on the Core Horror) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release**
- **Attach folder:** `35_fx_layers/`: `fx_bile_seep.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN04_raw_fx_core_enrage.png`
- **Note:** Plays on the Core Horror under 50%. Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: ch_enrage: The Core Rebuilds aura.
References attached: 1. fx_bile_seep.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette (lingering / bile): bile green #3d4a12 #6b8f1e #a8c23a, highlight #d8e86a, rot black #120c10; a few cloudy skyglass flecks #98c1cc.
Subject: a loose ring of bile-green rot drips and droplets with a few cloudy skyglass flecks, dripping downward; the centre left completely empty so the boss's sprite shows through.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN05 · cc_hexweave: Hexweave hit

- **Target:** cc_hexweave: Hexweave hit · ANIMATION (hit) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release**
- **Attach folder:** `35_fx_layers/`: `fx_binding_seal.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN05_raw_fx_hexweave.png`
- **Note:** Must read apart from the reused violet blast (anim_chain_wrap: chains spiralling) and the binding seal (a chain ring with a star). Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: cc_hexweave: Hexweave hit.
References attached: 1. fx_binding_seal.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette (control / lock): violet into ink, from #2a1640 through #6b3fa0 to a pale violet highlight; ink black #08080d.
Subject: a tangled, irregular snarl of violet ink cords wrapping tightly around nothing, like a net cinched shut, loose cord ends whipping out on one side, ink droplets flicking off; asymmetric and organic, NOT a star, NOT a hexagram, NOT a lattice or any regular geometric figure; cords only, no symbols.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN06 · Spreading Fire ember tile

- **Target:** Spreading Fire ember tile · gameAsset STATIC or ANIMATION loop (drain tile) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release**
- **Attach folder:** `35_fx_layers/`: `fx_ember_eruption.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN06_raw_fx_spreading_fire_embers.png`
- **Note:** The Fall's ember bands (rounds 1, 4 and 7). Must not read as the heavy mark (a cracked ember ring that resolves next turn). Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: Spreading Fire ember tile.
References attached: 1. fx_ember_eruption.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette (heavy / ember): ember red #c3141b into orange and white-hot, char black #120c10.
Subject: a flat patch of smouldering deck planks seen from above: planks charred black with glowing ember cracks along the grain, a few small low tongues of flame and drifting sparks; no ring shape and no crater.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN07 · ch_bile_spit: glob in flight

- **Target:** ch_bile_spit: glob in flight · ANIMATION (cast/hit, layer 1 of 2) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release**
- **Attach folder:** `35_fx_layers/`: `fx_bile_seep.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN07_raw_fx_bile_glob.png`
- **Note:** The Core Horror's plain attack, with AN08. Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: ch_bile_spit: glob in flight.
References attached: 1. fx_bile_seep.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette (lingering / bile): bile green #3d4a12 #6b8f1e #a8c23a, highlight #d8e86a, rot black #120c10; a few cloudy skyglass flecks #98c1cc.
Subject: one wet glob of bile in flight: a teardrop with a trailing tail, dark core, bile-green body, a few glossy highlight pixels and two or three cloudy skyglass flecks.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN08 · ch_bile_spit: splash

- **Target:** ch_bile_spit: splash · ANIMATION (cast/hit, layer 2 of 2) · 1254 x 1254 raw layer, magenta key or alpha · priority: **release**
- **Attach folder:** `35_fx_layers/`: `fx_bile_seep.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN08_raw_fx_bile_splash.png`
- **Note:** Pairs with AN07; attach the approved AN07 instead of the FX reference only if the director wants a closer match (still one or two images). Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: ch_bile_spit: splash.
References attached: 1. fx_bile_seep.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette (lingering / bile): bile green #3d4a12 #6b8f1e #a8c23a, highlight #d8e86a, rot black #120c10; a few cloudy skyglass flecks #98c1cc.
Subject: a flat ragged bile splash seen slightly from above, irregular arms and a few detached droplets.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AN09 · ch_undertow: water-drag streak (OPTIONAL)

- **Target:** ch_undertow: water-drag streak (OPTIONAL) · ANIMATION (hit) · 1254 x 1254 raw layer, magenta key or alpha · priority: **optional: only if the Undertow move survives the harness (still a PROBE)**
- **Attach folder:** `35_fx_layers/`: `fx_maw.png` (STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject)
- **Return as:** `AN09_raw_fx_undertow.png`
- **Note:** Generate only if the director confirms Undertow ships. Claude keys it and builds the strip (50 px frames) with `art/skyglass_boss_fx/boss_fx.py`.

```text
Target: one raw animation layer for The Ninja RPG's Skyglass boss fights: ch_undertow: water-drag streak.
References attached: 1. fx_maw.png: STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art in the rendering of the attached Skyglass boss-FX key art: crisp pixel rendering, dark one-pixel outlines, flat cel steps, limited palette, no airbrush, no bloom. Glow is edge light only, never a painted disc, panel or halo.
Canvas: 1254 x 1254, ONE element centred with a clear margin, nothing else on the canvas.
Palette: black water #08080d #10131a, deep sea teal-grey #2f445e, white-grey foam, a few cloudy skyglass flecks #98c1cc.
Subject: a horizontal streak of dark seawater dragging hard toward one side, a curling foam crest at its leading edge and a few trailing tendrils of water.
Background: native transparency (real alpha, no grey or tinted backing, no dark fringe, no checkerboard). If transparency is not available, a MAGENTA key only (#FF00FF), flat, covering the whole canvas and every enclosed gap. Never lime.
Avoid: no text, runes, glyphs, spell circles or symbols (the Skyglass emblem only where the subject names it); no character, face, body or hands; no scenery, floor or cast shadow; no second element; no franchise insignia.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 6. Salvager portrait (release-blocking)

### PT01 · The salvager (Wreck Sighted)

- **Target:** The salvager (Wreck Sighted), no live id yet · SCENE_CHARACTER (`sceneCharacters[]`), 2:3 full body · lime key · priority: **release-blocking** (the intro quest is public and cannot ship without a scene character)
- **Attach folder:** `25_salvager_portrait/`: `civilian_keeper.png` (STYLE-ONLY: the civilian register and grounded proportions; a different person, do not copy her robe, colours or pose); `sealwright_portrait.png` (STYLE-ONLY: the Skyglass pixel rendering, darkness and line weight; not the character)
- **Return as:** `PT01_raw_scene_char_skyglass_salvager.png`
- **Note:** Prompt hint from `SKYGLASS_TEXT.md` §1 via the audit (B).

```text
Target: the salvager, one full-body dialog portrait for The Ninja RPG's Wreck Sighted quest.
References attached: 1. civilian_keeper.png: STYLE-ONLY: the civilian register and grounded proportions; a different person, do not copy her robe, colours or pose. 2. sealwright_portrait.png: STYLE-ONLY: the Skyglass pixel rendering, darkness and line weight; not the character. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy pixel art matching the Skyglass crew's portraits: crisp pixel lineart, flat cel shading in two or three steps, limited dark palette, soft even lighting; no airbrush, bloom or painterly gradients. Camera at eye level, flat three-quarter view, no low angle, no foreshortening. Single figure, full body, head to feet visible with a clear margin, on a 2:3 portrait canvas, 1024 x 1536. Grounded adult proportions, not chibi, no anime-scaled eyes.
Subject: a coast salvager, a grounded adult woman, soaked and salt-stained, pushing a wet chart into the viewer's hands. Edo-era working clothes: a tenugui tied over her hair, a short indigo work jacket with the sleeves rolled and tied back with a cord, dark tapered trousers, straw waraji over tabi, a coil of wet rope at her hip. She holds a rolled, dripping chart out in front of her in both hands at chest height, arms within her silhouette; urgent, tired, wide awake. A civilian, not a ninja: no weapon, no armour, no mask. The only accent is the chart's pale skyglass-cyan lines.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the entire canvas, not a checkerboard, no shadow on the key, no lime spill on her.
Avoid: no text, letters or symbols; no headband, forehead protector, clan or village symbol; no weapon or armour; no aura, halo or glow; no scenery, floor or furniture, nothing resting on a surface; no second character; no gold; no blur, no smooth painterly rendering.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 7. Crownhold avatars (8)

From `SKYGLASS_CROWNHOLD_ART_BATCH.md` #12, #13, #21-#26, re-checked against the Edo pass: no terminals, tanks or
crowns; chakra-impression ninjas (RUL-2026-10-26-001); command shrines and the one Skyglass seal (RUL-2026-10-26-004);
Edo props (RUL-2026-10-26-005). Each note says what changed from the batch. Start with AV01 and judge the rest against it.

### AV01 · Tagwright

- **Target:** Tagwright (live username Crown Tagwright), AI `1syezT0axWVQVgeOGN-LH` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV01_raw_avatar_crownhold_ordnance_quartermaster.png`
- **Note:** Delivery file `avatar_crownhold_ordnance_quartermaster.webp`. Head kept distinct from the other officers (bible §6.2). Batch #12 had him holding a lacquered tray; changed to a ready stance (bible §6.0: weapon drawn). If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Tagwright, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Tagwright: a soot-stained short work haori and a tenugui headwrap knotted at the back; bandoliers of blank paper explosive tags across the chest; a fan of paper tags held ready in one soot-dark gloved hand, a kunai in the other. Accent: tag-orange.
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AV02 · Lancer

- **Target:** Lancer (live username Crown Lancer), AI `e5ye0RlN0fManSKdD_k-o` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV02_raw_avatar_crownhold_prototype_lancer_unit.png`
- **Note:** Delivery file `avatar_crownhold_prototype_lancer_unit.webp`. Head kept distinct from the other officers (bible §6.2). If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Lancer, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Lancer: a lean spear specialist in light laced plates and a close-fitting hood, a long cross-bladed yari with a thin edge of lightning chakra along its blade, burn-scarred forearms wrapped in cloth. Accent: electric yellow.
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AV03 · Honor Guard

- **Target:** Honor Guard (live username Honor Guard), AI `1orTQQ0Q9XhBvwlSZuzj5` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV03_raw_avatar_crownhold_honor_guard_commandant.png`
- **Note:** Delivery file `avatar_crownhold_honor_guard_commandant.webp`. Head kept distinct from the other officers (bible §6.2). Batch #21 held the naginata upright beside him; changed to battle-ready (bible §6.0). If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Honor Guard, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Honor Guard: a tall guard in plain stone-grey laced armour and a plain jingasa hat, a naginata held level and ready. Accent: polished iron.
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AV04 · Runner

- **Target:** Runner (live username Crown Runner), AI `-U_-iIwhGodkqdvc4GPa6` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV04_raw_avatar_crownhold_strategists_aide_de_camp.png`
- **Note:** Delivery file `avatar_crownhold_strategists_aide_de_camp.webp`. Head kept distinct from the other officers (bible §6.2). Batch #22 put the lightning on the scroll tubes; chakra sits on a blade edge only (bible §6.4). If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Runner, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Runner: a swift courier-shinobi in light lacquered plates and an aide's sash, a low straw kasa tied under the chin, sealed scroll dispatch tubes strapped across the back, a short ninjato drawn with a thin edge of lightning chakra. Accent: lightning white.
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AV05 · Vanguard

- **Target:** Vanguard (live username Crown Vanguard), AI `pshn-LkaC5vIgI6EOv68I` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV05_raw_avatar_crownhold_sanctum_vanguard.png`
- **Note:** Delivery file `avatar_crownhold_sanctum_vanguard.webp`. Head kept distinct from the other officers (bible §6.2). If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Vanguard, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Vanguard: a front-line shinobi in obsidian-black laced plates and a plain dark kabuto with a menpo, fire chakra running along the edge of his katana, a short banner pole with a plain dark pennant on the back. Accent: ember red.
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AV06 · Herald

- **Target:** Herald (live username Crown Herald), AI `Q6QjSoH6d1SabfQOLb12-` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV06_raw_avatar_crownhold_directive_herald.png`
- **Note:** Delivery file `avatar_crownhold_directive_herald.webp`. Head kept distinct from the other officers (bible §6.2). Batch #24's 'lightning gold' accent is now pale lightning yellow (no gold, bible §4.2); the glowing marks are plain ink. If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Herald, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Herald: a long dark ceremonial kimono and a deep cowl hood falling over the shoulders, an unrolled scroll of orders in one hand marked with unreadable brush strokes, a short sword drawn in the other, lightning-lit eyes. Accent: pale lightning yellow (a chakra colour, not gold metal).
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AV07 · Last Watch

- **Target:** Last Watch (live username Last Watch), AI `qQn9h2FY3GUUqgaFIRAuf` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV07_raw_avatar_crownhold_last_watch_executor.png`
- **Note:** Delivery file `avatar_crownhold_last_watch_executor.webp`. Head kept distinct from the other officers (bible §6.2). Batch #25's 'mask stamped with an unreadable seal' is now a blank mask (the Skyglass emblem is the only mark allowed). If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Last Watch, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Last Watch: a tattered night-watch cloak with its hood pulled low over a plain blank lacquer mask with no marks, twin kusarigama with wind chakra along the blades. Accent: night blue.
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### AV08 · Sealbearer

- **Target:** Sealbearer (live username Crown Sealbearer), AI `09gLgh9sCtshISC0dvpka` · AI_AVATAR (`userData.avatar`) · magenta key · priority: **release** (a borrowed crew sprite is live meanwhile)
- **Attach folder:** `40_crew_avatars/`: `crew_style_deck_warden.png` (STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text)
- **Return as:** `AV08_raw_avatar_crownhold_order_bearer_of_the_sanctum.png`
- **Note:** Delivery file `avatar_crownhold_order_bearer_of_the_sanctum.webp`. Head kept distinct from the other officers (bible §6.2). The tablet carries the Skyglass emblem (RUL-2026-10-26-004), not a blank or circled-cross seal. If the Deck Warden's hood and spear start repeating, attach `fallback_style_seal_charge.png` instead (bible §9).

```text
Target: Sealbearer, one AI battle avatar for The Ninja RPG's haunted mountain castle.
References attached: 1. crew_style_deck_warden.png: STYLE-ONLY: the original crew's look, its rendering, palette, outline weight, outfit language and proportions; this is a different person, whose head, gear and weapon are described by the text. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja, premium pixel art matching the original Skyglass crew: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Colour: near-black and deep indigo cloth; skyglass cyan along the weapon's edge and in the eyes; the officer's own accent used as small as the crew's cyan; brass on only one or two small fittings; rope only at the belt. Build and pose: lean, tall and agile, in a battle-ready stance with the weapon drawn; the sash tail and torn hems trail with movement. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette.
Costume: the crew's four marks: a hood or hat (as the subject names), a cloth mask over nose and mouth with eyes lit by pale chakra, an indigo sash with a hanging tail, and cloth-wrapped shins over closed tabi boots; dark layered kimono and plain lacquered plates where the subject asks for armour. Solid gloved hands with five fingers. Period weapons only.
He is a solid shinobi recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of the accent colour at the cloth's torn edges. Any chakra is a compact flame-like glow along a weapon's edge, or a small ball of chakra held above an open gloved palm; the hand is drawn normally. Square 1024 x 1024.
Subject: Sealbearer: deep-blue Sanctum wraps and a wide, shallow sandogasa hat with a short dark cloth veil at the back, a sealed scroll case on the back, a command seal tablet held up in one hand carved with the Skyglass emblem (a four-point star in a diamond), a wakizashi drawn in the other. Accent: deep-sea blue.
Background: a true solid flat magenta chroma key (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no floor, no cast shadow on the key, no magenta spill on the figure.
Avoid: no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold, no filigree, no tassels, no crown, no ornate parade armour, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no sheet, no grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 8. Crownhold release scenes (6)

The six release scenes of RUL-2026-10-30-061 item 9 (batch #27, #28, #34, #37, #38, #45), re-grounded in Edo craft.
The other 13 batch scenes are deferred.

### SC01 · Crownhold gate

- **Target:** Crownhold gate (batch #27) · SCENE_BACKGROUND (`sceneBackground`), 3:2 · no key · priority: **release** (borrowed ship scenes are live meanwhile)
- **Attach folder:** `50_ship_scenes/`: `colour_scene_observation_gallery.png` (STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout); `pixel_style_captain_portrait.png` (STYLE-ONLY: the pixel rendering only; not the character)
- **Return as:** `SC01_raw_scene_bg_crownhold_gate.png`
- **Note:** Delivery file `scene_bg_crownhold_gate.webp`. Used by the fail node ('you wake outside the gate in the snow') and the opening.

```text
Target: Castle gate, one scene background for The Ninja RPG's haunted mountain castle.
References attached: 1. colour_scene_observation_gallery.png: STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout. 2. pixel_style_captain_portrait.png: STYLE-ONLY: the pixel rendering only; not the character. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy, PREMIUM PIXEL ART game scene background in the same pixel rendering as the pixel-style reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), colour and light as the colour reference: night, deep indigo and storm-grey, cold blue fill, skyglass-cyan lanterns as the focal light, wet stone or polished floors. The castle is an Edo mountain castle: stone walls, heavy timber, tatami, shoji, iron fittings, paper and skyglass lanterns. Camera at eye level. Wide 3:2 landscape, 1536 x 1024. Keep the lower-left and lower-right thirds calm and readable: dialog portraits stand there.
Subject: the gate of a mountain castle at night: a snow-drifted parade ground before a heavy timber gate with iron studs, cut into a high stone wall; the gate stands open and unguarded, no banners; deep, unbroken snow; faint skyglass-cyan light deep inside the gateway.
Background: none; this is the full scene, edge to edge. No chroma key, no frame.
Avoid: no people, characters, creatures or silhouettes; no text, letters, kanji, signs or readable writing (maps, scrolls and boards show only lines and unreadable strokes); no screens, terminals, switches, cables, glass tanks or vats, laboratory gear, machines or guns; no crowns; no gold or filigree; no UI, frame, watermark, collage or grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### SC02 · Armory proving hall (Experimental Armory)

- **Target:** Armory proving hall (Experimental Armory) (batch #28) · SCENE_BACKGROUND (`sceneBackground`), 3:2 · no key · priority: **release** (borrowed ship scenes are live meanwhile)
- **Attach folder:** `50_ship_scenes/`: `colour_scene_observation_gallery.png` (STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout); `pixel_style_captain_portrait.png` (STYLE-ONLY: the pixel rendering only; not the character)
- **Return as:** `SC02_raw_scene_bg_crownhold_proving_hall.png`
- **Note:** Delivery file `scene_bg_crownhold_proving_hall.webp`. Division I opening (the Trialmaster). Batch #28's racks 'behind glass', live-fire range and brass placard are re-grounded per RUL-2026-10-26-005.

```text
Target: Armory proving hall (Experimental Armory), one scene background for The Ninja RPG's haunted mountain castle.
References attached: 1. colour_scene_observation_gallery.png: STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout. 2. pixel_style_captain_portrait.png: STYLE-ONLY: the pixel rendering only; not the character. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy, PREMIUM PIXEL ART game scene background in the same pixel rendering as the pixel-style reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), colour and light as the colour reference: night, deep indigo and storm-grey, cold blue fill, skyglass-cyan lanterns as the focal light, wet stone or polished floors. The castle is an Edo mountain castle: stone walls, heavy timber, tatami, shoji, iron fittings, paper and skyglass lanterns. Camera at eye level. Wide 3:2 landscape, 1536 x 1024. Keep the lower-left and lower-right thirds calm and readable: dialog portraits stand there.
Subject: inside the castle armoury: long wooden racks of yari and katana along cold stone walls, each rack bound with paper seal tags that glow faintly cyan; a blank wooden placard on a post by the first rack; a sand trial yard with straw practice targets beyond; skyglass lanterns on iron hooks.
Background: none; this is the full scene, edge to edge. No chroma key, no frame.
Avoid: no people, characters, creatures or silhouettes; no text, letters, kanji, signs or readable writing (maps, scrolls and boards show only lines and unreadable strokes); no screens, terminals, switches, cables, glass tanks or vats, laboratory gear, machines or guns; no crowns; no gold or filigree; no UI, frame, watermark, collage or grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### SC03 · Sealing-jar halls (Skyglass Research)

- **Target:** Sealing-jar halls (Skyglass Research) (batch #34) · SCENE_BACKGROUND (`sceneBackground`), 3:2 · no key · priority: **release** (borrowed ship scenes are live meanwhile)
- **Attach folder:** `50_ship_scenes/`: `colour_scene_observation_gallery.png` (STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout); `pixel_style_captain_portrait.png` (STYLE-ONLY: the pixel rendering only; not the character)
- **Return as:** `SC03_raw_scene_bg_crownhold_vat_halls.png`
- **Note:** Delivery file `scene_bg_crownhold_vat_halls.webp`. The Binder and the Echo. Batch #34's 'glowing specimen tanks' are sealing jars (RUL-2026-10-26-005).

```text
Target: Sealing-jar halls (Skyglass Research), one scene background for The Ninja RPG's haunted mountain castle.
References attached: 1. colour_scene_observation_gallery.png: STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout. 2. pixel_style_captain_portrait.png: STYLE-ONLY: the pixel rendering only; not the character. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy, PREMIUM PIXEL ART game scene background in the same pixel rendering as the pixel-style reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), colour and light as the colour reference: night, deep indigo and storm-grey, cold blue fill, skyglass-cyan lanterns as the focal light, wet stone or polished floors. The castle is an Edo mountain castle: stone walls, heavy timber, tatami, shoji, iron fittings, paper and skyglass lanterns. Camera at eye level. Wide 3:2 landscape, 1536 x 1024. Keep the lower-left and lower-right thirds calm and readable: dialog portraits stand there.
Subject: a long hall of tall glazed ceramic sealing jars standing in rows, each wrapped in paper seal tags and rope, lit by one tall skyglass lantern on a wooden post; heavy iron sealing keys hanging on wall hooks; one jar cracked and dark.
Background: none; this is the full scene, edge to edge. No chroma key, no frame.
Avoid: no people, characters, creatures or silhouettes; no text, letters, kanji, signs or readable writing (maps, scrolls and boards show only lines and unreadable strokes); no screens, terminals, switches, cables, glass tanks or vats, laboratory gear, machines or guns; no crowns; no gold or filigree; no UI, frame, watermark, collage or grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### SC04 · High Command signal room

- **Target:** High Command signal room (batch #37) · SCENE_BACKGROUND (`sceneBackground`), 3:2 · no key · priority: **release** (borrowed ship scenes are live meanwhile)
- **Attach folder:** `50_ship_scenes/`: `colour_scene_observation_gallery.png` (STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout); `pixel_style_captain_portrait.png` (STYLE-ONLY: the pixel rendering only; not the character)
- **Return as:** `SC04_raw_scene_bg_crownhold_signal_room.png`
- **Note:** Delivery file `scene_bg_crownhold_signal_room.webp`. Division III opening (the Signaller) and the aftermath; whoever sends the order is never shown. Batch #37's relay board, switches and self-printing paper are bell-cords (RUL-2026-10-26-005).

```text
Target: High Command signal room, one scene background for The Ninja RPG's haunted mountain castle.
References attached: 1. colour_scene_observation_gallery.png: STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout. 2. pixel_style_captain_portrait.png: STYLE-ONLY: the pixel rendering only; not the character. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy, PREMIUM PIXEL ART game scene background in the same pixel rendering as the pixel-style reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), colour and light as the colour reference: night, deep indigo and storm-grey, cold blue fill, skyglass-cyan lanterns as the focal light, wet stone or polished floors. The castle is an Edo mountain castle: stone walls, heavy timber, tatami, shoji, iron fittings, paper and skyglass lanterns. Camera at eye level. Wide 3:2 landscape, 1536 x 1024. Keep the lower-left and lower-right thirds calm and readable: dialog portraits stand there.
Subject: a signal room of the castle's high command: a wall of bell-cords running up to a row of small bronze signal bells, a taiko signal drum on a stand, campaign maps of borders that no longer exist pinned to the walls (lines only), paper lanterns; empty of people.
Background: none; this is the full scene, edge to edge. No chroma key, no frame.
Avoid: no people, characters, creatures or silhouettes; no text, letters, kanji, signs or readable writing (maps, scrolls and boards show only lines and unreadable strokes); no screens, terminals, switches, cables, glass tanks or vats, laboratory gear, machines or guns; no crowns; no gold or filigree; no UI, frame, watermark, collage or grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### SC05 · Planning hall

- **Target:** Planning hall (batch #38) · SCENE_BACKGROUND (`sceneBackground`), 3:2 · no key · priority: **release** (borrowed ship scenes are live meanwhile)
- **Attach folder:** `50_ship_scenes/`: `colour_scene_observation_gallery.png` (STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout); `pixel_style_captain_portrait.png` (STYLE-ONLY: the pixel rendering only; not the character)
- **Return as:** `SC05_raw_scene_bg_crownhold_planning_hall.png`
- **Note:** Delivery file `scene_bg_crownhold_planning_hall.webp`. The Tactician. Chairs from batch #38 are zabuton (Edo).

```text
Target: Planning hall, one scene background for The Ninja RPG's haunted mountain castle.
References attached: 1. colour_scene_observation_gallery.png: STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout. 2. pixel_style_captain_portrait.png: STYLE-ONLY: the pixel rendering only; not the character. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy, PREMIUM PIXEL ART game scene background in the same pixel rendering as the pixel-style reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), colour and light as the colour reference: night, deep indigo and storm-grey, cold blue fill, skyglass-cyan lanterns as the focal light, wet stone or polished floors. The castle is an Edo mountain castle: stone walls, heavy timber, tatami, shoji, iron fittings, paper and skyglass lanterns. Camera at eye level. Wide 3:2 landscape, 1536 x 1024. Keep the lower-left and lower-right thirds calm and readable: dialog portraits stand there.
Subject: a war-council hall set for a council no one will attend: a long low table spread with campaign maps (lines only), empty zabuton cushions along both sides, a brush resting on an inkstone of glowing skyglass-cyan chakra ink.
Background: none; this is the full scene, edge to edge. No chroma key, no frame.
Avoid: no people, characters, creatures or silhouettes; no text, letters, kanji, signs or readable writing (maps, scrolls and boards show only lines and unreadable strokes); no screens, terminals, switches, cables, glass tanks or vats, laboratory gear, machines or guns; no crowns; no gold or filigree; no UI, frame, watermark, collage or grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### SC06 · Throne room (Command Sanctum)

- **Target:** Throne room (Command Sanctum) (batch #45) · SCENE_BACKGROUND (`sceneBackground`), 3:2 · no key · priority: **release** (borrowed ship scenes are live meanwhile)
- **Attach folder:** `50_ship_scenes/`: `colour_scene_observation_gallery.png` (STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout); `pixel_style_captain_portrait.png` (STYLE-ONLY: the pixel rendering only; not the character)
- **Return as:** `SC06_raw_scene_bg_crownhold_throne_room.png`
- **Note:** Delivery file `scene_bg_crownhold_throne_room.webp`. The Crowned Captain's fight. Batch #45's cyan threads from the floor are removed (RUL-2026-10-26-001 item 4) and Arakane is retired; the carved order stays unreadable (no text).

```text
Target: Throne room (Command Sanctum), one scene background for The Ninja RPG's haunted mountain castle.
References attached: 1. colour_scene_observation_gallery.png: STYLE-ONLY: colour and lighting of the approved ship scenes; do not copy its room or layout. 2. pixel_style_captain_portrait.png: STYLE-ONLY: the pixel rendering only; not the character. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy, PREMIUM PIXEL ART game scene background in the same pixel rendering as the pixel-style reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), colour and light as the colour reference: night, deep indigo and storm-grey, cold blue fill, skyglass-cyan lanterns as the focal light, wet stone or polished floors. The castle is an Edo mountain castle: stone walls, heavy timber, tatami, shoji, iron fittings, paper and skyglass lanterns. Camera at eye level. Wide 3:2 landscape, 1536 x 1024. Keep the lower-left and lower-right thirds calm and readable: dialog portraits stand there.
Subject: the summit hall of the keep: dark obsidian-black stone lit by ember braziers, a tall window over a moonlit mountain range, an empty raised command seat; on the wall behind the seat, a stone panel cut with rows of unreadable carved grooves, its lowest band left blank, smooth stone.
Background: none; this is the full scene, edge to edge. No chroma key, no frame.
Avoid: no people, characters, creatures or silhouettes; no text, letters, kanji, signs or readable writing (maps, scrolls and boards show only lines and unreadable strokes); no screens, terminals, switches, cables, glass tanks or vats, laboratory gear, machines or guns; no crowns; no gold or filigree; no UI, frame, watermark, collage or grid.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

---

## 9. Haul chests, Legendary (2)

The Common, Rare and Epic chests (PC01-PC06) are done (art register). Generate these two from the approved Epic chests.

### PC07 · Keeper's Reserve

- **Target:** Keeper's Reserve (Legendary Haul chest, new hidden item from push/370) · ICON (`item.image`) · Legendary; no tier seal · magenta key · priority: **push/370 follow-up**
- **Attach folder:** none in the zip; attach your approved Epic Hunter chest image (the silver one with the glowing seams; saved in the repo as `art/skyglass_event_icons/raw/PC05_raw_icon-epic-hunters-chest.png`) as SUBJECT: keep its chest shape, angle, proportions and hunter motif
- **Return as:** `PC07_raw_icon-legendary-hunters-chest.png`
- **Note:** The top of the tier ladder (iron → bronze → silver → this). It must read as the richest of the four at 125 px without any gold.

```text
Target: Keeper's Reserve, one square game item icon for The Ninja RPG, the Legendary tier of a four-tier chest set (Bundle, Pack, Strongbox, Reserve).
References attached: 1. the Prize Strongbox (the Epic hunting chest): SUBJECT: keep its exact chest shape, angle, proportions, plank layout and hunter motif; only the materials step up. Follow the reference only for that role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Keeper's Reserve. The same chest as the attached Epic chest, raised one tier: the iron bands and corner plates become dark blackened steel edged with thin bright skyglass crystal inlay along every band; a cluster of three faceted pale-cyan skyglass crystals grows up through the lid beside the strap, breaking the chest's outline; the cyan light seams between the planks are brighter and run around all sides; the skyglass emblem clasp is larger, set in a crystal mount. Keep the hunter's motif: the dark stitched leather strap, the big curved horn hanging from the clasp (now tipped with a skyglass point) and the three claw marks on the front, glowing cyan. No gold or yellow metal anywhere: the tier reads by crystal and light, not by gold.
Background: transparent. If transparency is not available, a true solid flat magenta chroma key (#FF00FF) covering the whole canvas and every enclosed gap; not a checkerboard, not black, no gradient, no shadow on the key, no magenta spill on the object. (Magenta, not lime: the gatherer chest carries green leaves.)
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed is the Skyglass emblem, a four-point star in a diamond, as on the attached chest's clasp); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is thin seams of cyan light only); no gold, no yellow metal, no filigree, no jewels other than skyglass; no second object; no hands or people; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### PC08 · Quartermaster's Reserve

- **Target:** Quartermaster's Reserve (Legendary Haul chest, new hidden item from push/370) · ICON (`item.image`) · Legendary; no tier seal · magenta key · priority: **push/370 follow-up**
- **Attach folder:** none in the zip; attach your approved Epic Gatherer chest image (the silver one with the glowing seams; saved in the repo as `art/skyglass_event_icons/raw/PC06_raw_icon-epic-gatherers-chest.png`) as SUBJECT: keep its chest shape, angle, proportions and gatherer motif
- **Return as:** `PC08_raw_icon-legendary-gatherers-chest.png`
- **Note:** The top of the tier ladder (iron → bronze → silver → this). It must read as the richest of the four at 125 px without any gold.

```text
Target: Quartermaster's Reserve, one square game item icon for The Ninja RPG, the Legendary tier of a four-tier chest set (Bundle, Pack, Strongbox, Reserve).
References attached: 1. the Overgrown Strongbox (the Epic gathering chest): SUBJECT: keep its exact chest shape, angle, proportions, plank layout and gatherer motif; only the materials step up. Follow the reference only for that role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Quartermaster's Reserve. The same chest as the attached Epic chest, raised one tier: the iron bands and corner plates become dark blackened steel edged with thin bright skyglass crystal inlay along every band; a cluster of three faceted pale-cyan skyglass crystals grows up through the lid beside the strap, breaking the chest's outline; the cyan light seams between the planks are brighter and run around all sides; the skyglass emblem clasp is larger, set in a crystal mount. Keep the gatherer's motif: the pale grey rope with its cyan thread, the sprig of green leaves and white berries at the clasp (now fuller, with a small skyglass bud among the leaves) and the leaf carved on the front, glowing cyan. No gold or yellow metal anywhere: the tier reads by crystal and light, not by gold.
Background: transparent. If transparency is not available, a true solid flat magenta chroma key (#FF00FF) covering the whole canvas and every enclosed gap; not a checkerboard, not black, no gradient, no shadow on the key, no magenta spill on the object. (Magenta, not lime: the gatherer chest carries green leaves.)
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed is the Skyglass emblem, a four-point star in a diamond, as on the attached chest's clasp); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is thin seams of cyan light only); no gold, no yellow metal, no filigree, no jewels other than skyglass; no second object; no hands or people; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

## 10. Quest icons (1)

### QI01 · The Watch Log (weekly page)

- **Target:** the weekly page quest "The Watch Log: First Page" and every later page, push/490 · ICON (`quest.image`; the
  quest listing and the profile dashboard card render it square, like an item icon) · lime key · priority: before the
  page is published (it ships with the placeholder until then)
- **Attach folder:** `01_chart_icons/`: `chart_captains_watch.png` (STYLE-ONLY: the live Skyglass chart family, its paper,
  ink and rendering; do not copy its subject or layout); `anchor_skyglass_crystal.png` (STYLE-ONLY: the pixel rendering
  and the skyglass cyan of the approved Skyglass icons; do not copy the crystal)
- **Return as:** `QI01_raw_icon-watch-log-page.png`
- **Note:** Must read apart from IC02 (Watch Roster, a rolled duty roster) and IC06 (a torn loose ledger page tied with a
  cord): this is one flat page held down by a stone.

```text
Target: The Watch Log, one square game quest icon for The Ninja RPG.
References attached: 1. chart_captains_watch.png: STYLE-ONLY: the live Skyglass chart family, its paper, ink and rendering; do not copy its subject or layout. 2. anchor_skyglass_crystal.png: STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, seen from slightly above, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: a single page from a ship's watch log, dried by a fire: one sheet of dark weathered paper with salt-stained, slightly curled edges, held flat at one corner by a smooth grey beach stone. On the page, five short horizontal brush strokes in dark ink, one under the other like a list of orders, and a small pale cyan tick mark beside the top stroke. Lines and marks only, no writing or numbers.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap; not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols; no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object besides the stone; no roller, no cord, no scroll rod; no hands or people; no screens, machines or modern objects; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

## Claude derives these by script (no prompt)

From the approved bases, by a hue shift confined to one isolated region (request §7). If a returned base makes the
region hard to isolate, Claude says so at intake rather than forcing it.

| Code | Item (live id) | From | Change |
|---|---|---|---|
| DR01 | Rotted Reliquary Seal (`2sGi5SZXh2UutHmM-mIMD`) | approved IC03 | the amber-gold wax seal recoloured rot-green (Legendary, tainted); nothing else changes |
| DR02 | The Rotted Heading (`U2yJbBM6_N1xBBf0ez96F`) | approved IC04 | the amber-gold wax seal recoloured rot-green; nothing else changes |
| DR03 | Ledger Page: The Bone Store (`uu6ETQimuBJ69jwr76IIi`) | approved IC06 | the crimson tie cord and wax dab recoloured, one colour per page |
| DR04 | Ledger Page: The Snare Room (`6QgcnW0v6gZeHY474BjR0`) | approved IC06 | the same, a third colour |
| DR05 | Stores Manifest: The Ore Vault (`9j4IErGW1gmZ-5FNjZMEQ`) | approved IC07 | the rust-orange tie cord and wax dab recoloured, one colour per page |
| DR06 | Stores Manifest: The Bloom Cellar (`7Sz2ttMScKH8b10XYS12I`) | approved IC07 | the same, a third colour |

## Already in repo, upload only (no prompt)

From the audit's uploads list (32 files). The director runs the builder; Claude builds the manifests.

| Code | Asset | Type | Repo file | Route | Live id |
|---|---|---|---|---|---|
| UP01 | Sealed Treasury | ICON | `art/skyglass_event_icons/exports/icon-sealed-treasury.webp` | push/275 | `Ma8S90Nmbi0Xvm4u4FzJh` |
| UP02 | Archive Chart Case | ICON | `art/skyglass_event_icons/exports/icon-archive-chart-case.webp` | push/275 | `B48dTRsoLJGKBWIUbeUoG` |
| UP03 | Chart of the Buried Cache | ICON | `art/skyglass_event_icons/exports/icon-chart-buried-cache.webp` | push/275; check its seal is cyan (now Rare) before the swap; also the Buried Cache quest image | `nbLC37UzBamthKXvZsgQB` |
| UP04 | Unmarked Cargo | ICON | `art/skyglass_event_icons/exports/icon-unmarked-cargo.webp` | push/275 | `KzITKJ5BUQRz5QuYWw-0B` |
| UP05 | Crownbreaker badge v2 | ICON (badge) | `art/crownhold/icon-badge-crownbreaker-v2.webp` | push/340 creates the badge with it | `7kJGzBnfO14eKRs7_7c_f` |
| UP06 | Foundry Warden avatar | AI_AVATAR | `art/skyglass_event_icons/avatars/avatar_skyglass_foundry_warden.webp` | RUL-2026-10-30-061 item 8 | - |
| UP07 | Crown Armsmaster avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_master_of_arms.webp` | avatar-edit manifest (not yet built) | `-GKFYAZUg1eF-3VnZhDjx` |
| UP08 | Replicant Zero avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_replicant_zero.webp` | avatar-edit manifest (not yet built) | `vjEFUJ9mb1zNTuQf4lfXv` |
| UP09 | The Second avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_the_grand_marshal.webp` | avatar-edit manifest (not yet built) | `ZsfRoyJ55Zsay5bHNLMPv` |
| UP10 | Crown Trialmaster avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_proving_proctor.webp` | avatar-edit manifest (not yet built) | `1iJF8VBietrfvxJd_ZhFS` |
| UP11 | Crown Duelist avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_calibration_duelist.webp` | avatar-edit manifest (not yet built) | `B41DtMALbOTpL82thkBZu` |
| UP12 | Crown Archivist avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_skyglass_archive_keeper.webp` | avatar-edit manifest (not yet built) | `LZiunyinw9ScK3mh9HiR2` |
| UP13 | Crown Binder avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_impression_containment_warden.webp` | avatar-edit manifest (not yet built) | `N3E3C6MGgVYql2pTvpuGf` |
| UP14 | Crown Echo avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_unstable_echo_subject.webp` | avatar-edit manifest (not yet built) | `0LON_CwaUuXj4EYL7BtxS` |
| UP15 | Crown Stonebound avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_failed_reconstruction_prototype.webp` | avatar-edit manifest (not yet built) | `jqxu13kNHhfNY-NF68Ftb` |
| UP16 | Crown Signaller avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_command_signal_adjutant.webp` | avatar-edit manifest (not yet built) | `IJNhy83uB5Lc3sqn6Iqcr` |
| UP17 | Crown Tactician avatar | AI_AVATAR | `art/crownhold/avatar_crownhold_high_command_staff_tactician.webp` | avatar-edit manifest (not yet built) | `5U0WgIrowP6HdP5DrrxBS` |
| UP18 | anim_maw_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_maw_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP19 | anim_maw_field_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_maw_field_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP20 | anim_quench_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_quench_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP21 | anim_command_absolute_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_command_absolute_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP22 | anim_command_absolute_field_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_command_absolute_field_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP23 | anim_crownfall_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_crownfall_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP24 | anim_broadside_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_broadside_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP25 | anim_broadside_field_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_broadside_field_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP26 | anim_ships_bell_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_ships_bell_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP27 | anim_crimson_strike_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_crimson_strike_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP28 | anim_chain_wrap_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_chain_wrap_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP29 | anim_recall_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_recall_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP30 | anim_crown_aura_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_crown_aura_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP31 | anim_rot_claw_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_rot_claw_v1.webp` | create hidden, Proving Ground test-play, unhide | - |
| UP32 | anim_exposed_v1 | ANIMATION | `art/skyglass_boss_fx/exports/anim_exposed_v1.webp` | create hidden, Proving Ground test-play, unhide | - |

Also reused, not uploaded twice: the Little Maw animation is `anim_maw_v1.webp`; the Last Directive blaze is
`anim_crown_aura_v1.webp`; the violet Binding blast is `anim_chain_wrap_v1.webp`; the Shell Wall uses AN03.
