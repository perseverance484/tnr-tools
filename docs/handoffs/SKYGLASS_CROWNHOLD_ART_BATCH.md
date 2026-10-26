# Art batch: Skyglass event and Crownhold (35 images)

- **Director, 2026-10-25:** "Draft up a design document for the art director to pull each prompt from and use references. Then a short compact hand off for each image in sequence and I hand you back the approved image."
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. One image per fresh session, at most two reference images (never a collage), one candidate at a time. The art director returns the RAW image; Claude Code keys, crops, exports and QCs it (`skills/producing-tnr-art`), then swaps the placeholder in game by manifest.
- **Not in this batch:** Arakane (done, `art/crownhold/avatar_crownhold_arakane.webp`); the Sealwright and Oathkeeper scene portraits (already exist). **Deferred:** the Lastlight hit animation (a vertical strip sprite sheet; its placeholder is KGK: Black Fang Lance's).
- **How a session uses this file:** it is given the link to this file and an image number. It reads that image's section, downloads the reference images from the links there, attaches them in the order given, and runs the prompt exactly as written.
- **Live-game requests/writes:** 0.

## Targets (from `25x_DATA_art_spec.json`)

| Target | Canvas to generate | Key | Delivered |
|---|---|---|---|
| ICON | 1024 x 1024 | lime (magenta when the subject is green or the brief says so) | 256 px webp |
| JUTSU_ICON | 1024 x 1024 | none: designed background allowed (RUL-2026-10-14-001) | 256 px webp |
| AI_AVATAR | 1024 x 1024 | magenta | square webp, up to 1024 px |
| SCENE_BACKGROUND | 1536 x 1024 (3:2) | none | 512 x 341 webp |

## Reference files

Every link is pinned to commit `019700fdf1521f9f9bac4ff49f442a8f141cc749`, so it never changes. A fresh session downloads the images named in its section and attaches them.

| Key | Image link |
|---|---|
| coffer | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp |
| foundry_chart | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp |
| lantern | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp |
| crown | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp |
| arakane | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp |
| arsenal | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/avatar_ghost_ship_arsenal_keeper.webp |
| bbe | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp |
| gallery | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp |
| helm | https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp |

## Sequence

| # | Image | Target | Key | References | Delivery file |
|---|---|---|---|---|---|
| 1 | Sealed Treasury | ICON | lime | coffer | `icon-sealed-treasury.webp` |
| 2 | Archive Chart Case | ICON | lime | foundry_chart, coffer | `icon-archive-chart-case.webp` |
| 3 | Chart of the Buried Cache | ICON | lime | foundry_chart | `icon-chart-buried-cache.webp` |
| 4 | Unmarked Cargo | ICON | lime | coffer | `icon-unmarked-cargo.webp` |
| 5 | Crownbreaker (badge) | ICON | magenta | arakane, crown | `icon-badge-crownbreaker.webp` |
| 6 | Lastlight (jutsu icon) | JUTSU_ICON | none | bbe, lantern | `icon-jutsu-lastlight.webp` |
| 7 | Foundry Warden (AI avatar) | AI_AVATAR | magenta | arsenal | `avatar_skyglass_foundry_warden.webp` |
| 8 | Master of Arms (commander) | AI_AVATAR | magenta | arakane | `avatar_crownhold_master_of_arms.webp` |
| 9 | Replicant Zero (commander) | AI_AVATAR | magenta | arakane | `avatar_crownhold_replicant_zero.webp` |
| 10 | The Grand Marshal (commander) | AI_AVATAR | magenta | arakane | `avatar_crownhold_the_grand_marshal.webp` |
| 11 | Crownhold Proving Proctor | AI_AVATAR | magenta | arakane | `avatar_crownhold_proving_proctor.webp` |
| 12 | Ordnance Quartermaster | AI_AVATAR | magenta | arakane | `avatar_crownhold_ordnance_quartermaster.webp` |
| 13 | Prototype Lancer Unit | AI_AVATAR | magenta | arakane | `avatar_crownhold_prototype_lancer_unit.webp` |
| 14 | Calibration Duelist | AI_AVATAR | magenta | arakane | `avatar_crownhold_calibration_duelist.webp` |
| 15 | Skyglass Archive Keeper | AI_AVATAR | magenta | arakane | `avatar_crownhold_skyglass_archive_keeper.webp` |
| 16 | Impression Containment Warden | AI_AVATAR | magenta | arakane | `avatar_crownhold_impression_containment_warden.webp` |
| 17 | Unstable Echo Subject | AI_AVATAR | magenta | arakane | `avatar_crownhold_unstable_echo_subject.webp` |
| 18 | Failed Reconstruction Prototype | AI_AVATAR | magenta | arakane | `avatar_crownhold_failed_reconstruction_prototype.webp` |
| 19 | Command Signal Adjutant | AI_AVATAR | magenta | arakane | `avatar_crownhold_command_signal_adjutant.webp` |
| 20 | High Command Staff Tactician | AI_AVATAR | magenta | arakane | `avatar_crownhold_high_command_staff_tactician.webp` |
| 21 | Honor Guard Commandant | AI_AVATAR | magenta | arakane | `avatar_crownhold_honor_guard_commandant.webp` |
| 22 | Strategist's Aide-de-Camp | AI_AVATAR | magenta | arakane | `avatar_crownhold_strategists_aide_de_camp.webp` |
| 23 | Sanctum Vanguard | AI_AVATAR | magenta | arakane | `avatar_crownhold_sanctum_vanguard.webp` |
| 24 | Directive Herald | AI_AVATAR | magenta | arakane | `avatar_crownhold_directive_herald.webp` |
| 25 | Last Watch Executor | AI_AVATAR | magenta | arakane | `avatar_crownhold_last_watch_executor.webp` |
| 26 | Order-Bearer of the Sanctum | AI_AVATAR | magenta | arakane | `avatar_crownhold_order_bearer_of_the_sanctum.webp` |
| 27 | Scene: Crownhold gate | SCENE_BACKGROUND | none | gallery, helm | `scene_bg_crownhold_gate.webp` |
| 28 | Scene: Experimental Armory | SCENE_BACKGROUND | none | gallery, helm | `scene_bg_crownhold_armory.webp` |
| 29 | Scene: Skyglass Research | SCENE_BACKGROUND | none | gallery, helm | `scene_bg_crownhold_research.webp` |
| 30 | Scene: High Command | SCENE_BACKGROUND | none | gallery, helm | `scene_bg_crownhold_high_command.webp` |
| 31 | Scene: Command Sanctum | SCENE_BACKGROUND | none | gallery, helm | `scene_bg_crownhold_sanctum.webp` |
| 32 | Scene: Signal room (aftermath) | SCENE_BACKGROUND | none | gallery, helm | `scene_bg_crownhold_signal_room.webp` |
| 33 | The Last Directive (jutsu icon) | JUTSU_ICON | none | bbe, arakane | `icon-jutsu-the-last-directive.webp` |
| 34 | Extermination Order (jutsu icon) | JUTSU_ICON | none | bbe, arakane | `icon-jutsu-extermination-order.webp` |
| 35 | Countermand (item icon) | ICON | lime | arakane, coffer | `icon-countermand.webp` |

## Prompts

### 1. Sealed Treasury

References (download and attach, in this order):

1. STYLE AND MATERIAL: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp

~~~text
Draw ONE image for The Ninja RPG: Sealed Treasury. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE AND MATERIAL. Follow each reference only for its stated role.

Subject: The Sealed Treasury: the Skyglass Project's vault strongbox, the rarest chest in the event. It must NOT look like the reference coffer with a different lid: a TALL, upright vault chest with a flat, heavy lid and short iron feet, almost a small safe. Thick blue-black iron plating with engraved silver-grey seal-script borders over blue-black wood; heavy chains wrapped once around it and locked into a large circular vault-dial seal on the front, the dial set with one big faceted pale cyan skyglass crystal. A sliver of gold coins and one jewel glint at a hairline gap under the lid. No gold trim beyond those coins.

Style: game item icon, painted digital illustration (NOT pixel art) with a crisp dark outline, matching the STYLE reference's colour grading exactly: cool blue-black wood and blue-grey iron (no warm brown wood, no grey-brown iron), engraved silver-grey detail on the metal, strong cool cyan rim light along the top and edges, ONE accent of pale cyan faceted skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark.

Return the raw image named raw_icon-sealed-treasury.png.
~~~

### 2. Archive Chart Case

References (download and attach, in this order):

1. CHART FAMILY: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp
2. STYLE AND MATERIAL: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp

~~~text
Draw ONE image for The Ninja RPG: Archive Chart Case. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. CHART FAMILY; 2. STYLE AND MATERIAL. Follow each reference only for its stated role.

Subject: The Archive Chart Case: a long cylindrical map case of dark lacquered wood with blackened iron end caps, lying at a slight angle; one end cap is open and the rolled edge of a dark chart with faint pale lines peeks out (the same chart paper as reference 1). Crossed pale paper seal strips bind the middle, with a small iron seal plate set with one faceted pale cyan skyglass bead.

Style: game item icon, painted digital illustration (NOT pixel art) with a crisp dark outline, matching the STYLE reference's colour grading exactly: cool blue-black wood and blue-grey iron (no warm brown wood, no grey-brown iron), engraved silver-grey detail on the metal, strong cool cyan rim light along the top and edges, ONE accent of pale cyan faceted skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark.

Return the raw image named raw_icon-archive-chart-case.png.
~~~

### 3. Chart of the Buried Cache

References (download and attach, in this order):

1. SHAPE, STYLE AND LAYOUT: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp

~~~text
Draw ONE image for The Ninja RPG: Chart of the Buried Cache. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SHAPE, STYLE AND LAYOUT. Follow each reference only for its stated role.

Subject: The Chart of the Buried Cache: the same half-unrolled chart as the reference, sun-faded and salt-stained, sand caught in its folds. Instead of a ship plan, the unrolled part shows a stretch of coastline in faint pale lines with three small coves, older lines faintly visible beneath newer corrections. Beneath a tiny drawn stone shrine above one cove, a single cross mark is picked out in glowing pale cyan skyglass ink; the other two coves stay plain. A frayed rope cord with one faceted pale cyan skyglass bead ties the rolled end.

Style: game item icon, painted digital illustration (NOT pixel art) with a crisp dark outline, matching the STYLE reference's colour grading exactly: cool blue-black wood and blue-grey iron (no warm brown wood, no grey-brown iron), engraved silver-grey detail on the metal, strong cool cyan rim light along the top and edges, ONE accent of pale cyan faceted skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no ship plan, no compass-rose lettering, no skull, no pirate imagery.

Return the raw image named raw_icon-chart-buried-cache.png.
~~~

### 4. Unmarked Cargo

References (download and attach, in this order):

1. STYLE AND MATERIAL: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp

~~~text
Draw ONE image for The Ninja RPG: Unmarked Cargo. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE AND MATERIAL. Follow each reference only for its stated role.

Subject: Unmarked Cargo: a plain wooden cargo crate hauled out of the Skyglass wreck, deliberately anonymous. Dark weathered planks, blackened iron corner brackets, wrapped twice in heavy iron chain held by one padlock. Every stencil and marking has been scraped off, leaving pale scratched patches. A thin line of pale cyan skyglass light leaks from one seam.

Style: game item icon, painted digital illustration (NOT pixel art) with a crisp dark outline, matching the STYLE reference's colour grading exactly: cool blue-black wood and blue-grey iron (no warm brown wood, no grey-brown iron), engraved silver-grey detail on the metal, strong cool cyan rim light along the top and edges, ONE accent of pale cyan faceted skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark. No stencil text, no shipping labels.

Return the raw image named raw_icon-unmarked-cargo.png.
~~~

### 5. Crownbreaker (badge)

References (download and attach, in this order):

1. SUBJECT: keep the crown exactly: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp
2. STYLE: icon rendering only: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp

~~~text
Draw ONE image for The Ninja RPG: Crownbreaker (badge). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: keep the crown exactly; 2. STYLE: icon rendering only. Follow each reference only for its stated role.

Subject: Crownbreaker: Supreme Commander Arakane's Command Crown at the moment it breaks. Keep the crown from the avatar exactly: the spiked blackened-gold circlet, the halo of floating skyglass blades with the seal ring at the centre, the glowing control threads. The circlet is split down the middle through the seal, the two halves pushed apart; a white-hot crack of light bursts from the broken centre; the blades scatter and tumble outward; the threads are snapped, their loose ends curling and fading. No hands, no figure.

Style: game item icon, painted digital illustration (NOT pixel art) with a crisp dark outline, matching the STYLE reference's colour grading exactly: cool blue-black wood and blue-grey iron (no warm brown wood, no grey-brown iron), engraved silver-grey detail on the metal, strong cool cyan rim light along the top and edges, ONE accent of pale cyan faceted skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no medal border, no ribbon, no magenta spill.

Return the raw image named raw_icon-badge-crownbreaker.png.
~~~

### 6. Lastlight (jutsu icon)

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp
2. MOTIF: the lantern's light: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp

~~~text
Draw ONE image for The Ninja RPG: Lastlight (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register; 2. MOTIF: the lantern's light. Follow each reference only for its stated role.

Subject: Lastlight: Crownhold's final signal turned into a weapon. One straight beam of pale cyan-white skyglass light fired from a small lantern-shaped flare at the lower left, burning diagonally through the frame; faint ember-red wounds where the beam has cut, fading at the edges.

Style: jutsu icon in the style of the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-lastlight.png.
~~~

### 7. Foundry Warden (AI avatar)

References (download and attach, in this order):

1. STYLE: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/avatar_ghost_ship_arsenal_keeper.webp

~~~text
Draw ONE image for The Ninja RPG: Foundry Warden (AI avatar). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE. Follow each reference only for its stated role.

Subject: The Foundry Warden: keeper of the drowned skyglass foundry under the wreck's keel. A broad, heavy crewman in a scorched leather smith's apron over Skyglass Project armour, soaked to the knees, seawater dripping; one hand grips a long crucible-tongs polearm, the other a dripping ladle of glowing pale cyan molten skyglass. Crystal slag crusted on his gauntlets. Accent: molten cyan.

Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_skyglass_foundry_warden.png.
~~~

### 8. Master of Arms (commander)

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Master of Arms (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Master of Arms: Division I commander. A forge-wall weapons master in heavy Skyglass armour, two drawn blades, more weapons slung across his back; calm and exacting. Accent: forge-orange. Commanders are larger and more ornate than regular officers but wear no crown.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_master_of_arms.png.
~~~

### 9. Replicant Zero (commander)

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Replicant Zero (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Replicant Zero: Division II commander. A scientist in a long lab coat rebuilding his own left hand out of light; the first successful reconstruction; calm and curious. Accent: pale violet. Commanders are larger and more ornate than regular officers but wear no crown.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_replicant_zero.png.
~~~

### 10. The Grand Marshal (commander)

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: The Grand Marshal (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: The Grand Marshal: Division III commander, called 'The Second'. A senior officer in an unadorned dark greatcoat, hands behind his back; thoughtful and severe; the deputy who could question orders. Accent: muted brass. Commanders are larger and more ornate than regular officers but wear no crown.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_the_grand_marshal.png.
~~~

### 11. Crownhold Proving Proctor

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Crownhold Proving Proctor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Crownhold Proving Proctor: Division I. An armory proctor in a faded grey drill uniform, a clipboard of stamped trial sheets in one hand, two practice blades at the hip, a whistle on a cord. Accent: drill-yellow.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_proving_proctor.png.
~~~

### 12. Ordnance Quartermaster

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Ordnance Quartermaster. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Ordnance Quartermaster: Division I. A scorched apron over an officer coat, satchels of glowing sealed explosive tags, soot-dark gloves holding a tray of tags. Accent: tag-orange.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_ordnance_quartermaster.png.
~~~

### 13. Prototype Lancer Unit

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Prototype Lancer Unit. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Prototype Lancer Unit: Division I. A half-built lightning-lance automaton fused with its test pilot, exposed capacitor coils, a serial plate reading only a stamped number shape (no legible text). Accent: electric yellow.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_prototype_lancer_unit.png.
~~~

### 14. Calibration Duelist

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Calibration Duelist. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Calibration Duelist: Division I. A duelist in a calibration harness with chakra-measuring rings on both arms and a wind-swept practice sword, apprentice insignia. Accent: wind-green.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_calibration_duelist.png.
~~~

### 15. Skyglass Archive Keeper

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Archive Keeper. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Skyglass Archive Keeper: Division II. An archivist rendered in pale blue chakra light, holding a crystal-core ledger, translucent where the reconstruction is incomplete. Accent: archive blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_skyglass_archive_keeper.png.
~~~

### 16. Impression Containment Warden

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Impression Containment Warden. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Impression Containment Warden: Division II. A sealed containment suit with a water-filled observation visor and a heavy chain of vat keys. Accent: water teal.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_impression_containment_warden.png.
~~~

### 17. Unstable Echo Subject

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Unstable Echo Subject. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Unstable Echo Subject: Division II. A failed reconstruction glitching between two overlapping silhouettes, shadow chakra leaking from the seams. Accent: shadow violet.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_unstable_echo_subject.png.
~~~

### 18. Failed Reconstruction Prototype

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Failed Reconstruction Prototype. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Failed Reconstruction Prototype: Division II. A hulking earth-bound prototype, crystal growths over a half-formed body, a reconstruction rig bolted to its back. Accent: stone ochre.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_failed_reconstruction_prototype.png.
~~~

### 19. Command Signal Adjutant

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Command Signal Adjutant. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Command Signal Adjutant: Division III. A relay headset, wind-banner semaphore flags in both hands, High Command rank stripes. Accent: signal green.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_command_signal_adjutant.png.
~~~

### 20. High Command Staff Tactician

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: High Command Staff Tactician. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: High Command Staff Tactician: Division III. A campaign map case and a quill of glowing chakra ink, the Grand Marshal's aide's cord on the shoulder. Accent: ink blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_high_command_staff_tactician.png.
~~~

### 21. Honor Guard Commandant

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Honor Guard Commandant. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Honor Guard Commandant: Division III. Ceremonial stone-plated armour and a tower shield bearing a plain circled-cross seal. Accent: polished brass.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_honor_guard_commandant.png.
~~~

### 22. Strategist's Aide-de-Camp

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Strategist's Aide-de-Camp. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Strategist's Aide-de-Camp: Division III. Sealed dispatch tubes crackling with lightning, reflective lacquered armour, an aide's sash. Accent: lightning white.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_strategists_aide_de_camp.png.
~~~

### 23. Sanctum Vanguard

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Sanctum Vanguard. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Sanctum Vanguard: Division IV. Obsidian-and-ember Sanctum armour, fire-chakra gauntlets ablaze, a short banner pole on the back. Accent: ember red.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_sanctum_vanguard.png.
~~~

### 24. Directive Herald

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Directive Herald. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Directive Herald: Division IV. Long ceremonial robes, a glowing directive scroll that is rewriting itself, lightning-lit eyes. Accent: lightning gold.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_directive_herald.png.
~~~

### 25. Last Watch Executor

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Last Watch Executor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Last Watch Executor: Division IV. A tattered night-watch cloak, twin wind glaives, a blank mask stamped with an unreadable seal. Accent: night blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_last_watch_executor.png.
~~~

### 26. Order-Bearer of the Sanctum

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Order-Bearer of the Sanctum. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Order-Bearer of the Sanctum: Division IV. Deep-water Sanctum regalia, a sealed scroll case, a blank unsigned command seal held up. Accent: deep-sea blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_order_bearer_of_the_sanctum.png.
~~~

### 27. Scene: Crownhold gate

References (download and attach, in this order):

1. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Crownhold gate. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: rendering and lighting; 2. STYLE: rendering and lighting. Follow each reference only for its stated role.

Subject: A snow-drifted parade ground before an open gate cut into a mountain wall; the gate stands open and unguarded; no banners; deep, unbroken snow; dead silence; faint cyan light deep inside the gate.

Style: game scene background, painted digital illustration matching the style references' rendering and lighting, wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette: mountain stone, military brass, Skyglass blue-white crystal light; night or dusk.

Return the raw image named raw_scene_bg_crownhold_gate.png.
~~~

### 28. Scene: Experimental Armory

References (download and attach, in this order):

1. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Experimental Armory. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: rendering and lighting; 2. STYLE: rendering and lighting. Follow each reference only for its stated role.

Subject: Lit weapon racks behind tall glass panes, a live-fire trial range, a forge wall hung with every weapon type; cold stone, brass fittings, pale skyglass lamps.

Style: game scene background, painted digital illustration matching the style references' rendering and lighting, wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette: mountain stone, military brass, Skyglass blue-white crystal light; night or dusk.

Return the raw image named raw_scene_bg_crownhold_armory.png.
~~~

### 29. Scene: Skyglass Research

References (download and attach, in this order):

1. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Skyglass Research. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: rendering and lighting; 2. STYLE: rendering and lighting. Follow each reference only for its stated role.

Subject: Archive and vat halls: crystal-core shelving, a tall skyglass lamp column, rows of glowing specimen tanks, a reconstruction theatre in the background.

Style: game scene background, painted digital illustration matching the style references' rendering and lighting, wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette: mountain stone, military brass, Skyglass blue-white crystal light; night or dusk.

Return the raw image named raw_scene_bg_crownhold_research.png.
~~~

### 30. Scene: High Command

References (download and attach, in this order):

1. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: High Command. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: rendering and lighting; 2. STYLE: rendering and lighting. Follow each reference only for its stated role.

Subject: A map room with maps of borders that no longer exist, a chattering relay board, a long war-council table set for no one.

Style: game scene background, painted digital illustration matching the style references' rendering and lighting, wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette: mountain stone, military brass, Skyglass blue-white crystal light; night or dusk.

Return the raw image named raw_scene_bg_crownhold_high_command.png.
~~~

### 31. Scene: Command Sanctum

References (download and attach, in this order):

1. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Command Sanctum. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: rendering and lighting; 2. STYLE: rendering and lighting. Follow each reference only for its stated role.

Subject: An obsidian throne room lit by ember light, a tall summit window looking out over a whole mountain range at night, an empty command seat.

Style: game scene background, painted digital illustration matching the style references' rendering and lighting, wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette: mountain stone, military brass, Skyglass blue-white crystal light; night or dusk.

Return the raw image named raw_scene_bg_crownhold_sanctum.png.
~~~

### 32. Scene: Signal room (aftermath)

References (download and attach, in this order):

1. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. STYLE: rendering and lighting: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Signal room (aftermath). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: rendering and lighting; 2. STYLE: rendering and lighting. Follow each reference only for its stated role.

Subject: A signal room far below the summit: a relay board printing a new order line by line onto a sheet of paper; the room is empty; whoever sent the order is NOT shown.

Style: game scene background, painted digital illustration matching the style references' rendering and lighting, wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette: mountain stone, military brass, Skyglass blue-white crystal light; night or dusk.

Return the raw image named raw_scene_bg_crownhold_signal_room.png.
~~~

### 33. The Last Directive (jutsu icon)

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp
2. MOTIF: the Command Crown: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: The Last Directive (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register; 2. MOTIF: the Command Crown. Follow each reference only for its stated role.

Subject: The Last Directive: a commander's final order to himself. The Command Crown's seal ring blazing white-gold above a single upright blade planted point-down, an unbreakable shield of light around it.

Style: jutsu icon in the style of the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-the-last-directive.png.
~~~

### 34. Extermination Order (jutsu icon)

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp
2. MOTIF: the Command Crown: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Extermination Order (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register; 2. MOTIF: the Command Crown. Follow each reference only for its stated role.

Subject: Extermination Order: a killing command. Seven taut cyan threads converging from the edges onto one point, where a sealed elemental sigil cracks apart.

Style: jutsu icon in the style of the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-extermination-order.png.
~~~

### 35. Countermand (item icon)

References (download and attach, in this order):

1. SUBJECT: the seal tablet at Arakane's belt: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/crownhold/avatar_crownhold_arakane.webp
2. STYLE AND MATERIAL: https://raw.githubusercontent.com/perseverance484/tnr-tools/019700fdf1521f9f9bac4ff49f442a8f141cc749/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp

~~~text
Draw ONE image for The Ninja RPG: Countermand (item icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: the seal tablet at Arakane's belt; 2. STYLE AND MATERIAL. Follow each reference only for its stated role.

Subject: Countermand: Crownhold's command seal. The rectangular gold-framed seal tablet that hangs from Arakane's belt, on a short chain, its face carved with a plain circled-cross seal glowing pale cyan.

Style: game item icon, painted digital illustration (NOT pixel art) with a crisp dark outline, matching the STYLE reference's colour grading exactly: cool blue-black wood and blue-grey iron (no warm brown wood, no grey-brown iron), engraved silver-grey detail on the metal, strong cool cyan rim light along the top and edges, ONE accent of pale cyan faceted skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark.

Return the raw image named raw_icon-countermand.png.
~~~

