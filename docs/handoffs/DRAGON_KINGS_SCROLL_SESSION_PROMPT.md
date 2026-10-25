# Dragon King's Scroll: art session prompt (round 1)

- **Brief:** `docs/design/forbidden_pvp_scrolls/PROJECT.md`.
- **Goal:** a new Dragon King's Scroll item icon: an unrolled hanging scroll with a painted fire dragon instead of
  writing. It sets the frame the Tiger's Scroll will reuse. Two candidates, each in its own isolated session.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes ONE item icon: the
DRAGON KING'S SCROLL, a legendary hanging scroll that teaches the Forbidden jutsu Dragon King's Impact. Read
docs/design/forbidden_pvp_scrolls/PROJECT.md first.

Attach as references, with these roles:
1. SUBJECT (keep the hanging-scroll format and the dark wood rollers; NOT the writing):
   art/item_icons/forbidden_pvp_scrolls/refs/ref_dragon_kings_scroll_live.webp
2. DRAGON (take the dragon's look and colours only, not the figure or the scene):
   art/item_icons/forbidden_pvp_scrolls/refs/ref_dragon_kings_impact_jutsu.webp - a crimson and ember-orange fire dragon.
3. RENDERING GOAL (match the rendering, not the colours or shape): art/item_icons/forbidden_pvp_scrolls/refs/style_dragons_scroll.webp
   and style_demon_scroll.webp - our approved scroll icons: bold clean dark outlines, cel shading with painterly texture,
   rich material detail, transparent background.

Prompt:
open square pixel-art icon of an upright hanging scroll, fully unrolled and turned slightly to one side, dark lacquered
wood rollers with gold end caps at the top and bottom, a deep crimson silk brocade border, aged cream paper, a short
gold hanging cord at the top; painted on the paper, a crimson and gold Eastern fire dragon coiling down the length of the
scroll, scales edged in gold, flame-tipped whiskers and mane, its open maw at the bottom; the dragon's glowing ember eye
is the brightest point; crisp pixel lineart, flat cel shading, limited palette, soft even lighting, strong readable
silhouette, centered with a small margin, transparent background, no frame, no text.
Negative: no writing, no kanji, no letters, no runes, no seals with writing, no symbols, no glow outline, no sparkles,
no aura, no background, no asset sheet, no grid, no circular medal frame, no labels, no multiple icons, no franchise
insignia, no person, no blade.

Generate two candidates, each in its own isolated generation session:
DK-1: as above.
DK-2: as above, but the dragon breaks out past the paper's edge at the top and bottom (head and tail overlapping the
      border), more dynamic.

Square, 1024 x 1024. Return the raw images only, named raw_dragon_kings_scroll_DK-1.png and
raw_dragon_kings_scroll_DK-2.png. Do not process, crop or upload anything. Fail fast: regenerate once if any writing or
character appears, the dragon turns green or jade, the scroll is rolled up or lying flat, a glow outline or sparkles
appear, or the scroll is cropped or touches an edge.
~~~

## Intake (Claude Code)

1. Raw QC (no text, transparent or keyable background, whole object in frame).
2. Process with `art/item_icons/chunin_exam_scrolls/process_icon.py` (clean alpha, trim, pad square, 256 px, alpha firmed),
   export to `art/item_icons/forbidden_pvp_scrolls/exports/icon_dragon_kings_scroll_v1.webp`; artpreflight `--type ICON`.
3. Review sheet: the live icon beside each candidate, on the LEGENDARY rarity frame at 160 px and at 45 px.
4. After the director picks, build the suggestion (one item edit of `image`, with its rationale).
