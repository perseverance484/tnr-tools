# Art request: Skyglass event item icons (11)

- **For:** the director and the isolated image-generation sessions
- **From:** Fable / Claude Code, 2026-10-24. Director: "Let's make art for them now before we make them actually."
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`: one icon per fresh session, at most two individual reference
  images (never a collage), one candidate at a time. Spec: `25x_DATA_art_spec.json` target `ICON`.
- **Gate:** push/254 (the item creates) is on HOLD until these icons are approved; it will be regenerated with the real
  images instead of placeholders.
- **Live-game requests/writes:** 0.

## Targets

| # | Item | Delivery file | Key | References to attach |
|---|---|---|---|---|
| 1 | Skyglass Coffer | `icon-skyglass-coffer.webp` | lime | Reliquary (style only) |
| 2 | Katon Tool Pouch | `icon-tool-pouch-katon.webp` | lime | Shinobi Tool Pouch (subject) + Katon Kunai (subject detail) |
| 3 | Ikazuchi Tool Pouch | `icon-tool-pouch-ikazuchi.webp` | lime | approved #2 (style) + Ikazuchi Kunai (subject detail) |
| 4 | Wave Tool Pouch | `icon-tool-pouch-wave.webp` | lime | approved #2 (style) |
| 5 | Stonefall Tool Pouch | `icon-tool-pouch-stonefall.webp` | lime | approved #2 (style) |
| 6 | Zephyrfang Tool Pouch | `icon-tool-pouch-zephyrfang.webp` | **magenta** (green accent) | approved #2 (style) |
| 7 | Chart of the Drowned Foundry (map of the wreck: keel and lower decks) | `icon-chart-drowned-foundry.webp` | lime | Reliquary (style only) |
| 8 | Chart of the Quarantined Archive (map of the wreck: sealed chamber amidships) | `icon-chart-quarantined-archive.webp` | lime | approved #7 (style) |
| 9 | Chart of the Captain's Watch (map of the wreck: upper command decks) | `icon-chart-captains-watch.webp` | lime | approved #7 (style) |
| 12 | Chart of the Buried Cache (route chart of a shore cove; added 2026-10-25) | `icon-chart-buried-cache.webp` | lime | approved #7 (style) |
| 10 | Lastlight Lantern | `icon-skyglass-signal-beacon.webp` | lime | Reliquary (style only) |
| 11 | Armory Requisition | `icon-armory-requisition.webp` | lime | Reliquary (style only) |

Reference files: `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`,
`art/crafting_caches/icon-shinobi-tool-pouch.webp`, `art/item_icons/kunai/refs/ref_katon_kunai_live.webp`,
`art/item_icons/kunai/refs/ref_ikazuchi_kunai_live.webp`.

## Order

1. **#1 Coffer, #2 Katon pouch, #7 Foundry chart** first; each locks its family. Director approves each before its family
   continues.
2. Then the other pouches (with #2 attached), the other charts (with #7), the Lastlight Lantern and the Requisition.

## Family rules

- **Skyglass family (Coffer, Charts, Lastlight Lantern, Requisition):** near-black iron and dark wood or dark paper, blackened iron
  banding with rivets, ONE accent of pale cyan faceted skyglass with a soft inner glow, a crisp dark outline, soft cool rim
  light, 3/4 view at eye level, no cast shadow. The Coffer must NOT look like the Reliquary (that is a flat-lidded box with
  a central vertical crystal clasp, now retired).
- **Tool Pouch family:** the Shinobi Tool Pouch's shape (dark leather hip pouch, flap and buckle, three kunai ring-handles
  standing out of the top). The three kunai become that element's kunai; the buckle and stitching pick up the element colour
  as the one accent. Everything else stays identical across the five so they read as a set; only the element changes.

## Copy-ready session prompts

Every prompt is self-contained. Paste it into a new session with the listed references.

### 1. Skyglass Coffer
~~~text
Draw ONE game item icon for The Ninja RPG: the Skyglass Coffer, a seal-locked salvage coffer from a wrecked shinobi
sky-warship. Generate exactly one image. Do not crop, key or process it.

Reference attached: the Skyglass Reliquary icon. STYLE AND MATERIAL ONLY: match its rendering, palette, outline and
lighting. Do NOT copy its shape: no flat lid, no central vertical crystal clasp.

Subject: a small, squat, closed coffer with a gently rounded lid, wider than it is tall. Blackened iron corner caps and two
riveted bands over dark wood. On the front, a round iron seal plate holding a single faceted pale cyan skyglass disc, and
faint pale seal-script lines running along the bands. Closed, nothing spilling out.

Style: game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of
pale cyan faceted skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening,
strong readable silhouette at 125 px, centered, single object, small even margin on every side. Square 1024 x 1024, on a
true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no symbols other than the seal-script lines, no labels, no UI, no frame, no watermark, no
open lid, no contents, no loose items, no table or surface, no shadow on the background, no glow halo or light disc, no
gold, no question mark, no second object.

Return the raw image named raw_icon_skyglass_coffer.png.
~~~

### 2. Katon Tool Pouch (locks the pouch family)
~~~text
Draw ONE game item icon for The Ninja RPG: the Katon Tool Pouch, a fire-specialist's armory pouch. Generate exactly one
image. Do not crop, key or process it.

References attached:
1. Shinobi Tool Pouch icon. SUBJECT AND STYLE: keep this pouch exactly (dark leather hip pouch, front flap, buckle,
   rivets, three kunai ring-handles standing out of the top) and its rendering.
2. Katon Kunai icon. SUBJECT DETAIL ONLY: the three kunai in the pouch become this kunai (dark blade with an ember-orange
   edge and a red-orange core in the ring).

Subject: the same pouch, with the three Katon kunai handles standing out of the top. The buckle becomes dark iron and the
stitching along the flap glows faintly ember orange: ember orange is the one accent.

Style: match reference 1's rendering exactly, crisp dark outline, flat cel shading, camera at eye level, 3/4 view, strong
readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat
lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no fire effects or flames around it, no glow halo, no loose kunai, no other items, no table
or surface, no shadow on the background, no UI, no frame, no watermark.

Return the raw image named raw_icon_tool_pouch_katon.png.
~~~

### 3-6. The other pouches
Attach the approved Katon pouch (style and shape: keep it identical) plus, for Ikazuchi only, the Ikazuchi Kunai icon
(subject detail). Paste the Katon prompt with these substitutions:

| # | Name | Kunai and accent line (replaces the Katon description) | Background |
|---|---|---|---|
| 3 | Ikazuchi Tool Pouch | three Ikazuchi kunai (dark blade, crackling pale blue-white lightning core in the ring); stitching glows electric blue-white | lime |
| 4 | Wave Tool Pouch | three Wave kunai (dark blade with a deep sea-blue edge and a water-blue core in the ring); stitching glows deep sea blue | lime |
| 5 | Stonefall Tool Pouch | three Stonefall kunai (heavy dark blade with an amber-brown stone edge and an amber core in the ring); stitching glows warm amber | lime |
| 6 | Zephyrfang Tool Pouch | three Zephyrfang kunai (slim dark blade with a pale wind-green edge and a pale green core in the ring); stitching glows pale wind green | **magenta #FF00FF** (and "no magenta spill" in the negative) |

Raw names: `raw_icon_tool_pouch_<element>.png`. "No lightning / water / rocks / wind effects around it" goes in each
negative.

### 7. Chart of the Drowned Foundry (locks the chart family)

**Concept (RUL-2026-10-24-026):** the Charts are maps of the wreck itself. The ship's layout is always shifting, but now
and then a chart of its interior turns up. Every chart is the same half-unrolled sheet showing a side-on plan of the ship
(hull outline, decks, bulkheads) drawn in faint pale lines that have been redrawn over older lines, with ONE section
picked out in glowing skyglass ink: the keel and lower decks (Foundry), a sealed chamber amidships (Archive) or the upper
command decks (Captain's Watch). At 125 px the glowing section's position, bottom, middle or top, tells them apart.

Attach `ref_style_skyglass_reliquary.png`.
~~~text
Draw ONE game item icon for The Ninja RPG: the Chart of the Drowned Foundry, a chart of the interior of a wrecked shinobi sky-warship whose layout keeps shifting. Generate exactly one image. Do not crop, key or process it.

Reference attached: the Skyglass Reliquary icon. STYLE AND MATERIAL ONLY: match its rendering, palette, outline and lighting. Do not copy its shape.

Subject: a rolled parchment chart, half unrolled at an angle, dark water-stained paper. On the unrolled part, a side-on cutaway plan of a sailing warship: the hull outline, stacked decks, bulkheads and masts drawn in faint pale lines, with older lines showing faintly beneath newer ones as if the plan had been redrawn many times. The KEEL AND LOWEST DECKS are picked out in glowing pale cyan skyglass ink. A blackened iron chart ring holds the rolled end, stamped with a small anvil-and-gear seal and set with one small faceted pale cyan skyglass bead. A few water drips at the torn lower edge.

Style: game item icon, painted digital illustration with a crisp dark outline, dark parchment and blackened iron, one accent of pale cyan skyglass ink and skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no numbers, no labels or legends, no compass-rose lettering, no coastline or land map, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no quill, no bottle, no second object.

Return the raw image named raw_icon_chart_drowned_foundry.png.
~~~

### 8. Chart of the Quarantined Archive
Attach the approved Foundry chart (processed).
~~~text
Draw ONE game item icon for The Ninja RPG: the Chart of the Quarantined Archive, a chart of the interior of a wrecked shinobi sky-warship whose layout keeps shifting. Generate exactly one image. Do not crop, key or process it.

Reference attached: Chart of the Drowned Foundry icon. SHAPE, STYLE AND LAYOUT: keep the same half-unrolled chart, the same side-on ship plan with redrawn faint pale lines, the same camera and rendering. Only the highlighted section and the binding change.

Subject: the same chart, clean and dry, not waterlogged. On the ship plan, a single SEALED CHAMBER AMIDSHIPS, in the middle of the hull, is picked out in glowing pale cyan skyglass ink and boxed in by a drawn seal border; the keel is NOT highlighted. Instead of a plain iron ring, crossed pale paper seal strips bind the rolled end, and where they cross sits a small blackened iron seal plate set with one faceted pale cyan skyglass bead.

Style: game item icon, painted digital illustration with a crisp dark outline, dark parchment and blackened iron, one accent of pale cyan skyglass ink and skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no numbers, no labels or legends, no compass-rose lettering, no coastline or land map, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no quill, no bottle, no writing on the seal strips, no water drips, no second object.

Return the raw image named raw_icon_chart_quarantined_archive.png.
~~~

### 9. Chart of the Captain's Watch
Attach the approved Foundry chart (processed).
~~~text
Draw ONE game item icon for The Ninja RPG: the Chart of the Captain's Watch, the captain's own chart of a wrecked shinobi sky-warship whose layout keeps shifting. Generate exactly one image. Do not crop, key or process it.

Reference attached: Chart of the Drowned Foundry icon. SHAPE, STYLE AND LAYOUT: keep the same half-unrolled chart, the same side-on ship plan with redrawn faint pale lines, the same camera and rendering. Only the highlighted section and the binding change.

Subject: the same chart, clean and dry. On the ship plan, the UPPER COMMAND DECKS, the raised stern decks and the helm at the top of the hull, are picked out in glowing pale cyan skyglass ink; the keel is NOT highlighted. The rolled end is held by a heavier blackened iron captain's chart ring with a small crown-shaped crest (no letters) and a larger faceted pale cyan skyglass bead. A slim dark iron spyglass lies across the unrolled part.

Style: game item icon, painted digital illustration with a crisp dark outline, dark parchment and blackened iron, one accent of pale cyan skyglass ink and skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no numbers, no labels or legends, no compass-rose lettering, no coastline or land map, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no quill, no bottle, no gold or brass, no water drips.

Return the raw image named raw_icon_chart_captains_watch.png.
~~~

### 12. Chart of the Buried Cache (added 2026-10-25, RUL-2026-10-25-012)
Attach the approved Foundry chart (processed). The one chart that maps the shore, not the ship.
~~~text
Draw ONE game item icon for The Ninja RPG: the Chart of the Buried Cache, an old salt-stained route chart from a wrecked shinobi sky-warship, marking a cache its crew buried on the shore. Generate exactly one image. Do not crop, key or process it.

Reference attached: Chart of the Drowned Foundry icon. SHAPE, STYLE AND LAYOUT: keep the same half-unrolled chart, the same camera and rendering. The drawing on it and the binding change.

Subject: the same chart, sun-faded and salt-stained, sand caught in its folds. Instead of a ship plan, the unrolled part shows a stretch of coastline in faint pale lines with three small coves, older lines faintly visible beneath newer corrections. Beneath a tiny drawn stone shrine above one cove, a single cross mark is picked out in glowing pale cyan skyglass ink; the other two coves stay plain. A frayed rope cord with one faceted pale cyan skyglass bead ties the rolled end, and a small iron shovel blade tag hangs from the cord.

Style: game item icon, painted digital illustration with a crisp dark outline, faded parchment and blackened iron, one accent of pale cyan skyglass ink and skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no numbers, no labels or legends, no compass-rose lettering, no ship plan, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no quill, no bottle, no skull, no pirate imagery, no second object.

Return the raw image named raw_icon_chart_buried_cache.png.
~~~

### 10. Lastlight Lantern
~~~text
Draw ONE game item icon for The Ninja RPG: the Lastlight Lantern, a hand-held signal lamp still tuned to a hidden
fortress. Generate exactly one image. Do not crop, key or process it.

Reference attached: the Skyglass Reliquary icon. STYLE AND MATERIAL ONLY: match its rendering, palette, outline and
lighting. Do not copy its shape.

Subject: a compact hand-held beacon lamp with a blackened iron cage frame, a carry ring on top and a short iron base. Inside
the cage, a single tall faceted pale cyan skyglass crystal glows softly, the brightest part of the icon. Thin pale
seal-script lines on the iron base.

Style: game item icon, painted digital illustration with a crisp dark outline, near-black iron, one accent of pale cyan
skyglass with a soft inner glow kept inside the cage, soft cool rim light, camera at eye level, 3/4 view, strong readable
silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green
chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no light beam, no rays, no glow halo or light disc outside the cage, no flame, no candle, no
table or surface, no shadow on the background, no UI, no frame, no watermark, no second object.

Return the raw image named raw_icon_skyglass_signal_beacon.png.
~~~

### 11. Armory Requisition
~~~text
Draw ONE game item icon for The Ninja RPG: the Armory Requisition, an iron requisition tag a quartermaster exchanges for
one tool pouch. Generate exactly one image. Do not crop, key or process it.

Reference attached: the Skyglass Reliquary icon. STYLE AND MATERIAL ONLY: match its rendering, palette, outline and
lighting. Do not copy its shape.

Subject: a rectangular blackened iron tag with clipped corners and riveted edges, hanging from a short dark cord, stamped
with a crossed-kunai emblem (no letters) and set with one small faceted pale cyan skyglass bead below the emblem.

Style: game item icon, painted digital illustration with a crisp dark outline, near-black iron, one accent of pale cyan
skyglass with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, strong readable silhouette at 125 px,
centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background
(#00FF00) covering the entire canvas, not transparent, not checkerboard.

Negative: no text, no letters, no numbers, no paper, no scroll, no coins, no loose kunai, no table or surface, no shadow on
the background, no glow halo, no UI, no frame, no watermark, no second object.

Return the raw image named raw_icon_armory_requisition.png.
~~~

## Intake (Claude Code)

Raw QC; key (`chroma.py --target ICON`, `--key magenta` for #6); pad to square with margin; lossless WebP at 256 px into
`art/skyglass_event_icons/exports/`; review sheet at 125 px on each rarity frame; then regenerate push/254 with the real
images (`imagePack`) and stage the Requisition with its Special quest.
