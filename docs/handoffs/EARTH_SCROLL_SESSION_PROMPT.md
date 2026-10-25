# Earth Scroll: art session prompt (round 1)

- **Brief:** `docs/design/chunin_exam_scrolls/PROJECT.md`.
- **Goal:** a new Earth Scroll item icon (Chunin Exams quest prop): the live scroll's colours and gold caps, the painted
  character replaced by a wax seal with a mountain relief. Two candidates, each in its own isolated session.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes ONE item icon: the
EARTH SCROLL, a sealed scroll candidates must carry through the Chunin Exams. Read
docs/design/chunin_exam_scrolls/PROJECT.md first.

Attach as references, with these roles:
1. SUBJECT (keep the object, colours and gold caps; NOT the character, the outline or the sparkles):
   art/item_icons/chunin_exam_scrolls/refs/ref_earth_scroll_live.webp - the live Earth Scroll: a closed hand scroll at
   45 degrees, deep green brocade ends, cream paper middle, gold rings and round gold knob finials.
2. RENDERING GOAL (match the rendering, not the colours): art/item_icons/chunin_exam_scrolls/refs/style_dragons_scroll.webp
   and style_scroll_of_bastion.webp - our approved scroll icons: bold clean dark outlines, cel shading with painterly
   texture, rich material detail, a corded tie with tassels, transparent background.

Prompt:
open square pixel-art icon of a closed sealed hand scroll lying at 45 degrees, lower left to upper right, deep forest
green brocade with a subtle darker swirl pattern, cream paper showing between gold rings, round gold knob finials on both
ends, a thick braided cord wrapped once around the middle and closed with a round dark umber-red wax seal pressed with a
relief of three mountain ridges, two short green tassels hanging from the cord, the wax seal is the brightest and most
eye-catching point, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, strong readable
silhouette, centered with a small margin, transparent background, no frame, no text.
Negative: no writing, no kanji, no letters, no runes, no symbols other than the mountain relief, no glow outline, no
yellow outline, no sparkles, no aura, no background, no asset sheet, no grid, no circular medal frame, no labels, no
multiple icons, no franchise insignia, no steel caps.

Generate two candidates, each in its own isolated generation session:
ES-1: as above.
ES-2: as above, but the scroll slightly shorter and fatter and the seal a little larger (more weight in the middle).

Square, 1024 x 1024. Return the raw images only, named raw_earth_scroll_ES-1.png and raw_earth_scroll_ES-2.png. Do not
process, crop or upload anything. Fail fast: regenerate once if any writing or character appears, the seal is missing or
not the focus, the caps turn steel, the green drifts to jade or teal, a glow outline or sparkles appear, or the scroll is
cropped or touches an edge.
~~~

## Intake (Claude Code)

1. Raw QC (no text, transparent or keyable background, whole object in frame).
2. Key if needed, trim, pad to an exact square with a small margin, export 256 x 256 lossless WebP to
   `art/item_icons/chunin_exam_scrolls/exports/icon_earth_scroll_v1.webp`.
3. Review sheet: the live icon beside each candidate, at 160 px on each rarity frame and at 45 px.
4. After the director picks, build the suggestion (one item edit of `image`, with its rationale).
