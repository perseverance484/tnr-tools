# Skyglass Wreck map structure: art session prompts (round 1, three concepts)

- **Design:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` (RUL-2026-10-23-003, RUL-2026-10-24-008).
- **Goal:** the world-map structure sprite for the Skyglass Wreck dungeon entrance. Three competing concepts, each in its
  own fresh, isolated session (`docs/workflows/ISOLATED_ART_GENERATION.md`). The director picks one.
- **Live-game requests/writes:** 0. Credentials: none.

## How the game draws it (why the prompts say what they say)

- A dungeon entrance is a `mapAsset` of category "structure", drawn as a camera-facing billboard on the flat hex map
  (`app/src/libs/threejs/mapLocations.ts`, `syncMapLocationSprites`). Height = hex height x renderScale x entrance scale;
  width follows the image's aspect ratio. Uploads are resized to 512 px on the longest side.
- The sprite's anchor is `center (0.5, 0.15)`: the point 15% up from the bottom edge sits on the tile centre. So the
  structure's ground/waterline belongs about 15% above the bottom, with only a little foreground (surf, rocks) below it.
- Live structures (the Wyrmspire mountains, the stone arch shrine) are compact painted objects in a front three-quarter
  view, read at roughly 60-100 px on screen, over a light-blue sea. No sky, no scene, no night backdrop.

## References (two per session, the same two for all three)

1. **SUBJECT - the ship itself:** `art/ghost_ship_skyglass/quest_icon_ghost_ship_skyglass.webp`. Keep the ship's design:
   dark weathered timber hull with iron bands, torn slate-blue sails and hanging banners carrying the pale circled-cross
   seal sigil, the small lit cabin windows, and the faceted white-blue Skyglass Core crystal mounted under the keel in
   iron rings. Drop its black background.
2. **CAMERA / SCALE - a live map structure:** the director's own screenshot of an in-game structure on the world map
   (the Wyrmspire Mountain Range sprite or the stone arch shrine). Match its viewing angle, compactness and how it sits on
   the sea. Do not copy its subject, palette or rendering.

Background is flat magenta, not lime: the ship's seal-light is cyan-white and a green key would bleed into it.

## Concept 1 - Beached wreck

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session draws ONE world-map
structure sprite: the entrance to the Skyglass Wreck dungeon. Generate exactly ONE candidate. Do not process, crop, key
or upload anything.

Attach two references, with these roles:
1. SUBJECT (keep the ship's design, NOT its pose or background): quest_icon_ghost_ship_skyglass.webp. Keep the dark
   weathered timber hull with iron bands, the torn slate-blue sails and long hanging banners with the pale circled-cross
   seal sigil, the small lit cabin windows, and the faceted white-blue Skyglass Core crystal held under the keel in iron
   rings.
2. CAMERA / SCALE (match the viewing angle and compactness only): the in-game map structure screenshot. Do not copy its
   subject, colours or rendering.

Concept: the ghost ship has fallen out of the sky and lies BEACHED on a small sand-and-black-rock spit at the edge of the
sea. The hull is heeled over about 20 degrees, one mast snapped, sails torn and slack, banners trailing in the sand. The
keel has split and the Skyglass Core is half-buried in the sand beside the hull, cracked, still glowing pale cyan-white,
with faint seal-script lines glowing along the hull planks. A few crates and iron rings spilled on the sand. Shallow surf
foam laps the spit on the sea side.

Prompt:
single game world-map structure sprite, a wrecked shinobi sky-warship beached on a small sand and dark rock spit, crisp
pixel art with clean dark outlines and flat cel shading matching the ship reference, limited palette of weathered dark
timber, iron grey, slate-blue cloth, pale sand, and one accent of glowing cyan-white seal-light, neutral even daylight
(not night), front three-quarter view from slightly above, compact readable silhouette that still reads as a ship at
80 pixels tall, the whole object centred with a clear margin on every side, the sand spit's waterline about 15 percent
above the bottom edge with only a little surf and rock below it, on a true solid flat magenta chroma key background
(#FF00FF) covering the entire canvas, not transparent, not checkerboard, no shadow cast onto the magenta.
Negative: no text, no UI, no watermark, no labels, no sky, no moon, no clouds, no horizon, no scenery behind the object,
no large ocean area, no night lighting, no fog wash, no magenta spill on the object, no pirate skull flag, no cannons, no
modern ship, no people, no second ship, no blur, no painterly smear, no gradient background, no asset sheet, no grid,
no extra symbols or kanji beyond the circled-cross seal.

Rules: square, 1024 x 1024. Fail fast and regenerate once if the background is not flat magenta, the object touches an
edge, the rendering drifts from the ship reference (realistic or painterly), the Skyglass Core is missing, or the ship
no longer reads as a ship at small size.

Return the raw image only, named raw_skyglass_wreck_structure_beached.png.
~~~

## Concept 2 - Hovering ghost ship

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session draws ONE world-map
structure sprite: the entrance to the Skyglass Wreck dungeon. Generate exactly ONE candidate. Do not process, crop, key
or upload anything.

Attach two references, with these roles:
1. SUBJECT (keep the ship's design and its floating pose, NOT its background): quest_icon_ghost_ship_skyglass.webp. Keep
   the dark weathered timber hull with iron bands, the torn slate-blue sails and long hanging banners with the pale
   circled-cross seal sigil, the small lit cabin windows, and the faceted white-blue Skyglass Core crystal held under
   the keel in iron rings.
2. CAMERA / SCALE (match the viewing angle and compactness only): the in-game map structure screenshot. Do not copy its
   subject, colours or rendering.

Concept: the ghost ship still HOVERS, low, just above a small cluster of dark sea rocks. It sits level but listing
slightly, sails torn, banners hanging straight down. The Skyglass Core under the keel glows pale cyan-white, and a thin
column of faint seal-light runs from the core down to a glowing ring of seal-script on the rocks below. Small chunks of
rock and broken timber float in the air between the keel and the rocks. The gap between keel and rocks is short: the
ship stays close to the ground so the sprite stays compact.

Prompt:
single game world-map structure sprite, a derelict shinobi sky-warship hovering low above a small cluster of dark sea
rocks, a glowing faceted crystal core under the keel, crisp pixel art with clean dark outlines and flat cel shading
matching the ship reference, limited palette of weathered dark timber, iron grey, slate-blue cloth, dark wet rock, and
one accent of glowing cyan-white seal-light, neutral even daylight (not night), front three-quarter view from slightly
above, compact readable silhouette that still reads as a floating ship at 80 pixels tall, the whole object centred with
a clear margin on every side, the rocks' waterline about 15 percent above the bottom edge with only a little surf below
it, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not
checkerboard, no shadow cast onto the magenta.
Negative: no text, no UI, no watermark, no labels, no sky, no moon, no clouds, no horizon, no scenery behind the object,
no large ocean area, no night lighting, no fog wash, no large glow halo, no light rays filling the canvas, no magenta
spill on the object, no pirate skull flag, no cannons, no modern ship, no people, no second ship, no blur, no painterly
smear, no gradient background, no asset sheet, no grid, no extra symbols or kanji beyond the circled-cross seal.

Rules: square, 1024 x 1024. Fail fast and regenerate once if the background is not flat magenta, the object touches an
edge, the rendering drifts from the ship reference (realistic or painterly), the Skyglass Core is missing, the ship
floats so high it leaves a large empty gap, or the ship no longer reads as a ship at small size.

Return the raw image only, named raw_skyglass_wreck_structure_hovering.png.
~~~

## Concept 3 - Run aground, rising

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session draws ONE world-map
structure sprite: the entrance to the Skyglass Wreck dungeon. Generate exactly ONE candidate. Do not process, crop, key
or upload anything.

Attach two references, with these roles:
1. SUBJECT (keep the ship's design, NOT its pose or background): quest_icon_ghost_ship_skyglass.webp. Keep the dark
   weathered timber hull with iron bands, the torn slate-blue sails and long hanging banners with the pale circled-cross
   seal sigil, the small lit cabin windows, and the faceted white-blue Skyglass Core crystal held under the keel in iron
   rings.
2. CAMERA / SCALE (match the viewing angle and compactness only): the in-game map structure screenshot. Do not copy its
   subject, colours or rendering.

Concept: the ghost ship has RUN AGROUND but is trying to rise again. Its bow is wedged between dark sea rocks at the
waterline; the stern has lifted off the water and tilts upward about 15 degrees. The Skyglass Core under the keel flares
pale cyan-white, cracked but alive. Iron chains and heavy ropes from the bow are snagged on the rocks and pulled taut,
holding the ship down. Loose planks, rope ends and small stones drift upward around the lifting stern. Sails torn,
banners streaming upward.

Prompt:
single game world-map structure sprite, a shinobi sky-warship run aground with its bow wedged in dark sea rocks and its
stern lifting off the water, taut chains anchoring the bow to the rocks, a glowing cracked crystal core under the keel,
debris drifting upward, crisp pixel art with clean dark outlines and flat cel shading matching the ship reference,
limited palette of weathered dark timber, iron grey, slate-blue cloth, dark wet rock, and one accent of glowing
cyan-white seal-light, neutral even daylight (not night), front three-quarter view from slightly above, compact readable
silhouette that still reads as a ship at 80 pixels tall, the whole object centred with a clear margin on every side, the
rocks' waterline about 15 percent above the bottom edge with only a little surf below it, on a true solid flat magenta
chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no shadow cast onto the
magenta.
Negative: no text, no UI, no watermark, no labels, no sky, no moon, no clouds, no horizon, no scenery behind the object,
no large ocean area, no night lighting, no fog wash, no large glow halo, no magenta spill on the object, no pirate skull
flag, no cannons, no modern ship, no people, no second ship, no blur, no painterly smear, no gradient background, no
asset sheet, no grid, no extra symbols or kanji beyond the circled-cross seal.

Rules: square, 1024 x 1024. Fail fast and regenerate once if the background is not flat magenta, the object touches an
edge, the rendering drifts from the ship reference (realistic or painterly), the Skyglass Core or the chains are missing,
or the ship no longer reads as a ship at small size.

Return the raw image only, named raw_skyglass_wreck_structure_rising.png.
~~~

## Intake (Claude Code)

1. Raw QC each image: flat magenta, nothing touching an edge, ship design matches the subject reference, Core visible.
2. Key the magenta, clean edges and spill, trim to the object with a small margin, keeping the waterline at about 15%
   above the bottom; export transparent PNG at 512 px on the longest side to
   `art/ghost_ship_skyglass/structure/structure_skyglass_wreck_<concept>_v1.png`.
3. Review sheet: the three side by side, each also composited on a light-blue hex sea at 60, 80 and 100 px tall.
4. There is no map-structure target in `25x_DATA_art_spec.json` yet; intake follows this file until one exists.
