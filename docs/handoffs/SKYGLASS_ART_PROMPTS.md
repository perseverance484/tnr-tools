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
| **Total** | | **67** | |

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

### VT01 · Captain's Command Fan

- **Target:** Captain's Command Fan, item `vltFmOTgOyqssIpNXvT37` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT01_raw_icon-variant-token-captains-command-fan.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Captain's Command Fan, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a small gunbai war fan seen face-on: a rounded paddle on a short haft with a tiny four-point star at its centre. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT02 · Rot-Bloom Reaper

- **Target:** Rot-Bloom Reaper, item `-7dQs2qwokuNSAS2c3X8Q` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT02_raw_icon-variant-token-rot-bloom-reaper.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Rot-Bloom Reaper, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a curved sickle blade with clusters of cloudy, barnacle-like skyglass along its back and a short loop of rope chain. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT03 · Warden's Forge-Fists

- **Target:** Warden's Forge-Fists, item `d96tj122ex6BnzhMDwy0s` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT03_raw_icon-variant-token-wardens-forge-fists.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Warden's Forge-Fists, a boss variant token, one square game item icon for The Ninja RPG.
References attached: 1. VT00_approved.png: SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark lines, a clenched armoured gauntlet with blunt maul-head knuckle plates. The motif fills the window and stays inside it; nothing else is added.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels; no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur; no change to the tag outside its window.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VT04 · Wayfinder's Heading

- **Target:** Wayfinder's Heading, item `giSqzJqE6YdsrnOoy1KLV` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT04_raw_icon-variant-token-wayfinders-heading.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Wayfinder's Heading, a boss variant token, one square game item icon for The Ninja RPG.
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

### VT06 · Sealwright's Seal

- **Target:** Sealwright's Seal, item `3ZR700BAWr_Pd3Eqnu1c9` · ICON (`item.image`) · Legendary; no seal · lime key · priority: **player-facing**
- **Attach folder:** `05_variant_token/`: `VT00_approved.png` (SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif)
- **Return as:** `VT06_raw_icon-variant-token-sealwrights-seal.png`
- **Note:** Starts only after VT00 is approved. Each motif must read apart from the other six at 125 px.

```text
Target: Sealwright's Seal, a boss variant token, one square game item icon for The Ninja RPG.
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

### VS01 · Gale-Watch Aetherion

- **Target:** Gale-Watch Aetherion, item variant `MXAAH-1fwPfyDJg2FnE8t` on Aetherion (`PhP5ZEF5iVa97jcumJ15c`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `10_variant_aetherion/`: `base_aetherion.png` (SUBJECT: the live Aetherion icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS01_raw_icon-variant-gale-watch-aetherion.png`
- **Note:** Shares its base with VS17 The First Blade: the two must read clearly apart at 125 px.

```text
Target: Gale-Watch Aetherion, a skin of the weapon Aetherion, one square game item icon for The Ninja RPG.
References attached: 1. base_aetherion.png: SUBJECT: the live Aetherion icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Gale-Watch Aetherion. Keep the attached Aetherion exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: a thin pale-cyan skyglass vein inlaid along the fuller; the grip rewrapped in weathered off-white sailcloth; a small four-point skyglass star set in the pommel. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (The First Blade: a long grey-blue cord bound round the grip with trailing ends, a short inlay at the blade base, brass fittings); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS02 · Tidewater Thornsilver

- **Target:** Tidewater Thornsilver, item variant `YNhKQmKUjfVIPQkGlNO41` on Thornsilver (`MQ5mJqH-5MkQdtLGSZ5nb`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `11_variant_thornsilver/`: `base_thornsilver.png` (SUBJECT: the live Thornsilver icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS02_raw_icon-variant-tidewater-thornsilver.png`
- **Note:** Shares its base with VS19 Crownbreaker: the two must read clearly apart at 125 px.

```text
Target: Tidewater Thornsilver, a skin of the weapon Thornsilver, one square game item icon for The Ninja RPG.
References attached: 1. base_thornsilver.png: SUBJECT: the live Thornsilver icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Tidewater Thornsilver. Keep the attached Thornsilver exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the steel darkened to a wet-dark sheen; a row of small round skyglass beads inlaid along the spine; a faint white salt crust at the guard. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (the frost-shard skin: three broken frost-point shards set in the crossguard); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS03 · Night Watch Testament

- **Target:** Night Watch Testament, item variant `mtx4YmUu-wkKGwnOPVbYS` on Night's Testament (`osJq3k77YPGoFWgof12FQ`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `12_variant_nights_testament/`: `base_nights_testament.png` (SUBJECT: the live Night's Testament icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS03_raw_icon-variant-night-watch-testament.png`

```text
Target: Night Watch Testament, a skin of the weapon Night's Testament, one square game item icon for The Ninja RPG.
References attached: 1. base_nights_testament.png: SUBJECT: the live Night's Testament icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Night Watch Testament. Keep the attached Night's Testament exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: one small pale-cyan four-point star set into the crossguard; the blackened blade unchanged, with no crystal on it. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS04 · Mast-Lightning Stormrender

- **Target:** Mast-Lightning Stormrender, item variant `_49jp25nHiH-v8ywlRdKH` on Stormrender (`cLXXf8RJv5l9B_gGsYN2a`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `13_variant_stormrender/`: `base_stormrender.png` (SUBJECT: the live Stormrender icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS04_raw_icon-variant-mast-lightning-stormrender.png`
- **Note:** Shares its base with VS16 Wayfinder's Heading: the two must read clearly apart at 125 px.

```text
Target: Mast-Lightning Stormrender, a skin of the weapon Stormrender, one square game item icon for The Ninja RPG.
References attached: 1. base_stormrender.png: SUBJECT: the live Stormrender icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Mast-Lightning Stormrender. Keep the attached Stormrender exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: a short skyglass rod set upright in the crossguard; thin cyan crackle lines on the ricasso only. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Wayfinder's Heading: a round compass rose at the crossguard and an etched route line down the fuller); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS05 · Roll-Call Oathbinder

- **Target:** Roll-Call Oathbinder, item variant `umsYP0jL3emdVFDdU6Fcd` on Oathbinder (`ttwbJ6ZA5Id-OuBludM27`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `14_variant_oathbinder/`: `base_oathbinder.png` (SUBJECT: the live Oathbinder icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS05_raw_icon-variant-roll-call-oathbinder.png`
- **Note:** Shares its base with VS14 Rot-Bloom Reaper: the two must read clearly apart at 125 px.

```text
Target: Roll-Call Oathbinder, a skin of the weapon Oathbinder, one square game item icon for The Ninja RPG.
References attached: 1. base_oathbinder.png: SUBJECT: the live Oathbinder icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Roll-Call Oathbinder. Keep the attached Oathbinder exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the chain's white prayer knots replaced by small pale-cyan skyglass beads; the black chain otherwise unchanged. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Rot-Bloom Reaper: a wet dark rope chain, milky barnacle-like skyglass on the blade back, a rot-stained haft); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS06 · Chartline Ink of the Void

- **Target:** Chartline Ink of the Void, item variant `1yWEP0r3elIzyScORfot4` on Ink of the Void (`wE1QeldWTjls2Cf43cFjf`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `15_variant_ink_of_the_void/`: `base_ink_of_the_void.png` (SUBJECT: the live Ink of the Void icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS06_raw_icon-variant-chartline-ink-of-the-void.png`

```text
Target: Chartline Ink of the Void, a skin of the weapon Ink of the Void, one square game item icon for The Ninja RPG.
References attached: 1. base_ink_of_the_void.png: SUBJECT: the live Ink of the Void icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Chartline Ink of the Void. Keep the attached Ink of the Void exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: fine cyan skyglass chart lines and one small compass mark inlaid along both limbs. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS07 · The Unwritten Order

- **Target:** The Unwritten Order, item variant `3NH-VreJl9TcqqIYiztn_` on The Unwritten (`m0RZDUDnwQu_0BtOJgHi9`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `16_variant_the_unwritten/`: `base_the_unwritten.png` (SUBJECT: the live The Unwritten icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS07_raw_icon-variant-the-unwritten-order.png`
- **Note:** Shares its base with VS13 Captain's Command Fan: the two must read clearly apart at 125 px.

```text
Target: The Unwritten Order, a skin of the weapon The Unwritten, one square game item icon for The Ninja RPG.
References attached: 1. base_the_unwritten.png: SUBJECT: the live The Unwritten icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: The Unwritten Order. Keep the attached The Unwritten exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the fan's leaves become pale paper written with faint unreadable brush strokes, one line left blank; the outer edge sealed with drops of cyan skyglass wax. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Captain's Command Fan: a rounded black-lacquered gunbai war-fan paddle with a skyglass star at its centre); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS08 · Keelstone Embrace

- **Target:** Keelstone Embrace, item variant `xFyTBqje5M1_68EqRRoBu` on Gaea's Embrace (`-LzgdTM1yTjlezOyjd-6H`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `17_variant_gaeas_embrace/`: `base_gaeas_embrace.png` (SUBJECT: the live Gaea's Embrace icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS08_raw_icon-variant-keelstone-embrace.png`

```text
Target: Keelstone Embrace, a skin of the weapon Gaea's Embrace, one square game item icon for The Ninja RPG.
References attached: 1. base_gaeas_embrace.png: SUBJECT: the live Gaea's Embrace icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Keelstone Embrace. Keep the attached Gaea's Embrace exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the plated shaft kept; the orange tip crystal recoloured pale skyglass cyan; two dark iron bands added on the shaft. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS09 · Drill-Count Bracers

- **Target:** Drill-Count Bracers, item variant `_tdmHvPnvlnIMLpRnk9GC` on Warden's Bracers (`qTzWEb6tFBv8dl15ztqDO`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `18_variant_wardens_bracers/`: `base_wardens_bracers.png` (SUBJECT: the live Warden's Bracers icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS09_raw_icon-variant-drill-count-bracers.png`
- **Note:** Shares its base with VS15 Warden's Forge-Fists: the two must read clearly apart at 125 px.

```text
Target: Drill-Count Bracers, a skin of the weapon Warden's Bracers, one square game item icon for The Ninja RPG.
References attached: 1. base_wardens_bracers.png: SUBJECT: the live Warden's Bracers icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Drill-Count Bracers. Keep the attached Warden's Bracers exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: a row of tally notches cut across the knuckles, each set with a tiny cyan skyglass stud; any glyph on the plates becomes plain lacquered metal. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Warden's Forge-Fists: soot-black forged iron, blunt maul-head knuckle plates, seams of cooled skyglass); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS10 · Lastlight Dawnblade

- **Target:** Lastlight Dawnblade, item variant `m7Xqe9cD1oB_2vCj1Zvu5` on Eclipsed Dawnblade (`MbPhG5El3UYjS5Bk2K3Bl`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `19_variant_eclipsed_dawnblade/`: `base_eclipsed_dawnblade.png` (SUBJECT: the live Eclipsed Dawnblade icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS10_raw_icon-variant-lastlight-dawnblade.png`
- **Note:** Must also read apart from VS18 Sealwright's Seal (a different Dawnblade with engraved lines and a pommel seal disc).

```text
Target: Lastlight Dawnblade, a skin of the weapon Eclipsed Dawnblade, one square game item icon for The Ninja RPG.
References attached: 1. base_eclipsed_dawnblade.png: SUBJECT: the live Eclipsed Dawnblade icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Lastlight Dawnblade. Keep the attached Eclipsed Dawnblade exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: a small lantern-shaped skyglass core set at the base of the blade, its soft cyan light contained inside it, not spilling out. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS11 · Skysail Whisper

- **Target:** Skysail Whisper, item variant `kD6g1o5qJo3K9r1HeHtiH` on Zephyr's Whisper (`CBp4scJi9XzMKRqxpshwT`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `20_variant_zephyrs_whisper/`: `base_zephyrs_whisper.png` (SUBJECT: the live Zephyr's Whisper icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS11_raw_icon-variant-skysail-whisper.png`

```text
Target: Skysail Whisper, a skin of the weapon Zephyr's Whisper, one square game item icon for The Ninja RPG.
References attached: 1. base_zephyrs_whisper.png: SUBJECT: the live Zephyr's Whisper icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Skysail Whisper. Keep the attached Zephyr's Whisper exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the fans' embedded crystal recoloured pale skyglass cyan; thin rigging cords strung between the ribs. If the base's wind swirl is kept, keep it compact, inside the margin and not touching the background. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS12 · Hullbreaker Frostbite

- **Target:** Hullbreaker Frostbite, item variant `Iew4QFXyfWLPlPoMgeDrz` on Yuki's Frostbite (`Z-JdppXvrSokRymXavpOw`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `21_variant_yukis_frostbite/`: `base_yukis_frostbite.png` (SUBJECT: the live Yuki's Frostbite icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS12_raw_icon-variant-hullbreaker-frostbite.png`

```text
Target: Hullbreaker Frostbite, a skin of the weapon Yuki's Frostbite, one square game item icon for The Ninja RPG.
References attached: 1. base_yukis_frostbite.png: SUBJECT: the live Yuki's Frostbite icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Hullbreaker Frostbite. Keep the attached Yuki's Frostbite exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the haft replaced by dark ship's timber with iron rings; a skyglass inlay set into the cheek of the axe head, not the edge. The head keeps its frost colouring, but without the cloud of blue fire around it: the axe silhouette must read, with glow only as a thin edge light. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS13 · Captain's Command Fan

- **Target:** Captain's Command Fan, item variant `Deo6Y7dNzaPhOAiWK-4I3` on The Unwritten (`m0RZDUDnwQu_0BtOJgHi9`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `16_variant_the_unwritten/`: `base_the_unwritten.png` (SUBJECT: the live The Unwritten icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS13_raw_icon-variant-captains-command-fan.png`
- **Note:** Shares its base with VS07 The Unwritten Order: the two must read clearly apart at 125 px.

```text
Target: Captain's Command Fan, a skin of the weapon The Unwritten, one square game item icon for The Ninja RPG.
References attached: 1. base_the_unwritten.png: SUBJECT: the live The Unwritten icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Captain's Command Fan. Keep the attached The Unwritten exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the folding fan becomes a gunbai war fan in the same footprint, angle and size: a rounded black-lacquered paddle with an iron rim on a short haft (the base's pommel and hanging cord kept), a four-point star inlaid in pale cyan skyglass at the centre, faint cyan cracks along the rim. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (The Unwritten Order: the folding fan kept, pale paper leaves with faint strokes and cyan wax on the edge); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS14 · Rot-Bloom Reaper

- **Target:** Rot-Bloom Reaper, item variant `dkkdXbwWFOGSw1nemyK7K` on Oathbinder (`ttwbJ6ZA5Id-OuBludM27`) · ICON (item-variant image) · no tier seal · magenta key · priority: **player-facing**
- **Attach folder:** `14_variant_oathbinder/`: `base_oathbinder.png` (SUBJECT: the live Oathbinder icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS14_raw_icon-variant-rot-bloom-reaper.png`
- **Note:** Shares its base with VS05 Roll-Call Oathbinder: the two must read clearly apart at 125 px.

```text
Target: Rot-Bloom Reaper, a skin of the weapon Oathbinder, one square game item icon for The Ninja RPG.
References attached: 1. base_oathbinder.png: SUBJECT: the live Oathbinder icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Rot-Bloom Reaper. Keep the attached Oathbinder exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the chain becomes wet dark rope; clusters of cloudy, milky skyglass grow like barnacles along the back of the blade; the haft dark and rot-stained with a faint bile-green tinge. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Roll-Call Oathbinder: the black chain kept with neat cyan beads in place of its prayer knots); do not use that design.
Background: transparent. If transparency is not available, a true solid flat magenta chroma key (#FF00FF) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no magenta spill on the object. (Magenta, not lime: this subject carries green.)
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS15 · Warden's Forge-Fists

- **Target:** Warden's Forge-Fists, item variant `3DtT9myjmYY5xNY5mv7Ew` on Warden's Bracers (`qTzWEb6tFBv8dl15ztqDO`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `18_variant_wardens_bracers/`: `base_wardens_bracers.png` (SUBJECT: the live Warden's Bracers icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS15_raw_icon-variant-wardens-forge-fists.png`
- **Note:** Shares its base with VS09 Drill-Count Bracers: the two must read clearly apart at 125 px.

```text
Target: Warden's Forge-Fists, a skin of the weapon Warden's Bracers, one square game item icon for The Ninja RPG.
References attached: 1. base_wardens_bracers.png: SUBJECT: the live Warden's Bracers icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Warden's Forge-Fists. Keep the attached Warden's Bracers exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the pair reforged in soot-black iron with blunt maul-head knuckle plates and thin seams of cooled pale-cyan skyglass between the plates; any glyph on the plates removed. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Drill-Count Bracers: the base metal kept, a row of tally notches with tiny cyan studs); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS16 · Wayfinder's Heading

- **Target:** Wayfinder's Heading, item variant `hkcF8F8RZa71dcLu8im8G` on Stormrender (`cLXXf8RJv5l9B_gGsYN2a`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `13_variant_stormrender/`: `base_stormrender.png` (SUBJECT: the live Stormrender icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS16_raw_icon-variant-wayfinders-heading.png`
- **Note:** Shares its base with VS04 Mast-Lightning Stormrender: the two must read clearly apart at 125 px.

```text
Target: Wayfinder's Heading, a skin of the weapon Stormrender, one square game item icon for The Ninja RPG.
References attached: 1. base_stormrender.png: SUBJECT: the live Stormrender icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Wayfinder's Heading. Keep the attached Stormrender exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: a small round compass rose inlaid in cyan skyglass at the crossguard; a fine etched route line running down the fuller. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Mast-Lightning Stormrender: a short skyglass rod upright in the crossguard and cyan crackle on the ricasso); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS17 · The First Blade

- **Target:** The First Blade, item variant `m_CYA2H9XDF_TbMiii8PE` on Aetherion (`PhP5ZEF5iVa97jcumJ15c`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `10_variant_aetherion/`: `base_aetherion.png` (SUBJECT: the live Aetherion icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS17_raw_icon-variant-the-first-blade.png`
- **Note:** Shares its base with VS01 Gale-Watch Aetherion: the two must read clearly apart at 125 px.

```text
Target: The First Blade, a skin of the weapon Aetherion, one square game item icon for The Ninja RPG.
References attached: 1. base_aetherion.png: SUBJECT: the live Aetherion icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: The First Blade. Keep the attached Aetherion exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the grip bound in a long grey-blue cord whose ends trail out as if in wind; a short skyglass inlay at the base of the blade; dull brass on the guard and pommel fittings (brass, not gold). Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Gale-Watch Aetherion: a cyan vein down the fuller, an off-white sailcloth grip, a small star pommel); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS18 · Sealwright's Seal

- **Target:** Sealwright's Seal, item variant `trSVpt_E_BqOJS1geL_Sn` on Whispering Dawnblade (`mqCCZGSfXUNL02B4H6C9R`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `22_variant_whispering_dawnblade/`: `base_whispering_dawnblade.png` (SUBJECT: the live Whispering Dawnblade icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS18_raw_icon-variant-sealwrights-seal.png`
- **Note:** The base is Whispering Dawnblade, not Eclipsed Dawnblade (RUL-2026-10-30-060 item 8). Must read apart from VS10 Lastlight Dawnblade.

```text
Target: Sealwright's Seal, a skin of the weapon Whispering Dawnblade, one square game item icon for The Ninja RPG.
References attached: 1. base_whispering_dawnblade.png: SUBJECT: the live Whispering Dawnblade icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Sealwright's Seal. Keep the attached Whispering Dawnblade exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: fine dark engraved lines like brushed seal script running along the whole blade (decorative strokes only, no legible characters); a round skyglass seal disc at the pommel. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
Generate ONE image. Do not crop, key, resize or otherwise process it.
```

### VS19 · Crownbreaker

- **Target:** Crownbreaker, item variant `dt6BWKCOfuB3mPLl14-CF` on Thornsilver (`MQ5mJqH-5MkQdtLGSZ5nb`) · ICON (item-variant image) · no tier seal · lime key · priority: **player-facing**
- **Attach folder:** `11_variant_thornsilver/`: `base_thornsilver.png` (SUBJECT: the live Thornsilver icon; keep its silhouette, proportions, blade treatment, colours and angle); `material_skyglass_crystal.png` (MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape)
- **Return as:** `VS19_raw_icon-variant-crownbreaker.png`
- **Note:** Shares its base with VS02 Tidewater Thornsilver: the two must read clearly apart at 125 px.

```text
Target: Frost-Shard Thornsilver, a skin of the weapon Thornsilver, one square game item icon for The Ninja RPG.
References attached: 1. base_thornsilver.png: SUBJECT: the live Thornsilver icon; keep its silhouette, proportions, blade treatment, colours and angle. 2. material_skyglass_crystal.png: MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape. Follow each reference only for its stated role.
Style: Edo-era Japanese fantasy ninja pixel art, matching the Skyglass crew and their item icons: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly gradients; not chunky low-res pixel art, not smooth illustration. Palette: blue-black lacquered wood, storm-grey iron, weathered leather and rope, deep indigo cloth, and one pale skyglass-cyan accent (#98c1cc brightening to near-white). Skyglass is a faceted crystal object or inlay, never a glowing field.
Framing: one object, three-quarter view at eye level, centred, a small even margin on every side, a strong silhouette that reads at 125 px. Square 1024 x 1024.
Subject: Frost-Shard Thornsilver. Keep the attached Thornsilver exactly: the same silhouette, proportions, angle, colours and blade or body treatment. Change only this: the crossguard set with three short broken frost-point shards of pale skyglass; the blade exactly as the base, with no crystal added along the edge. Skyglass appears only as inlay and accents. The Skyglass Katana is the only all-crystal blade: no blade turns to crystal, and this must not read as a crystal sword.
It must read clearly apart from its sibling skin on the same base (Tidewater Thornsilver: wet-dark steel, a row of skyglass beads on the spine, salt crust at the guard); do not use that design.
Background: transparent. If transparency is not available, a true solid flat lime-green chroma key (#00FF00) covering the whole canvas and every enclosed gap (inside loops, handles, rings and chain links); not a checkerboard, no gradient, no shadow on the key, no lime spill on the object.
Avoid: no text, letters, numbers, kanji, runes or symbols (the only mark allowed anywhere is the Skyglass emblem, a four-point star in a diamond or circle, and only where the subject names it); no frame, border, medal ring, UI or watermark; no table, surface, ground or cast shadow; no glow halo, aura, light disc or light field (glow is a thin edge light only); no gold, no filigree, no jewels (dull brass fittings only where the subject says brass); no second object; no hands or people; no screens, glass tanks, machines or modern objects; no headband, clan or village symbol; no photorealism, no blur.
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
Subject: a tight woven knot of violet ink cords crossing over one another into a small hexagonal lattice, ink droplets flicking off its edges; cords only, no symbols.
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
