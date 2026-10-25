# Tiger's Scroll: art session prompt (round 1)

- **Brief:** `docs/design/forbidden_pvp_scrolls/PROJECT.md`.
- **Goal:** the Tiger's Scroll, the Dragon King's Scroll's pair: the same unrolled hanging scroll, with a painted white
  tiger instead of the dragon. If a Dragon King's Scroll candidate is approved first, attach it as the PAIR reference so
  the frames match exactly. Two candidates, each in its own isolated session.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes ONE item icon: the
TIGER'S SCROLL, a legendary hanging scroll that teaches the Forbidden jutsu Fury of The White Tiger (seven inner gates
opened, a tiger-shaped shockwave). It is the pair of the Dragon King's Scroll. Read
docs/design/forbidden_pvp_scrolls/PROJECT.md first.

Attach as references, with these roles:
1. SUBJECT (keep the hanging-scroll format and the white tiger; NOT the flat rendering or the blue ring pattern):
   art/item_icons/forbidden_pvp_scrolls/refs/ref_tigers_scroll_live.webp
2. RENDERING GOAL (match the rendering, not the colours or shape): art/item_icons/forbidden_pvp_scrolls/refs/style_dragons_scroll.webp
   and style_demon_scroll.webp - our approved scroll icons: bold clean dark outlines, cel shading with painterly texture,
   rich material detail, transparent background.
3. PAIR (only if provided): the approved Dragon King's Scroll icon. Match its frame exactly (rollers, caps, border,
   cord, angle, proportions); only the creature and the colours change.

Prompt:
open square pixel-art icon of an upright hanging scroll, fully unrolled and turned slightly to one side, dark lacquered
wood rollers with silver end caps at the top and bottom, a deep navy silk brocade border, pale cream paper, a short
silver hanging cord at the top; painted on the paper, a white tiger leaping downward toward the viewer, white fur with
bold black stripes, ice-blue shading, claws out, mouth open in a roar, swirling pale blue and green wind streaks trailing
from its body; the tiger's ice-blue eyes are the brightest point; crisp pixel lineart, flat cel shading, limited palette,
soft even lighting, strong readable silhouette, centered with a small margin, transparent background, no frame, no text.
Negative: no writing, no kanji, no letters, no runes, no seals with writing, no symbols, no glow outline, no sparkles,
no aura, no background, no asset sheet, no grid, no circular medal frame, no labels, no multiple icons, no franchise
insignia, no person, no orange tiger.

Generate two candidates, each in its own isolated generation session:
TS-1: as above.
TS-2: as above, but the tiger breaks out past the paper's edge (head and forepaws overlapping the border), more dynamic.
(If the Dragon King's Scroll is already approved, generate only the variant that matches it.)

Square, 1024 x 1024. Return the raw images only, named raw_tigers_scroll_TS-1.png and raw_tigers_scroll_TS-2.png. Do not
process, crop or upload anything. Fail fast: regenerate once if any writing or character appears, the tiger turns orange,
the scroll is rolled up or lying flat, a glow outline or sparkles appear, or the scroll is cropped or touches an edge.
~~~

## Intake (Claude Code)

1. Raw QC (no text, transparent or keyable background, whole object in frame).
2. Process with `art/item_icons/chunin_exam_scrolls/process_icon.py`, export to
   `art/item_icons/forbidden_pvp_scrolls/exports/icon_tigers_scroll_v1.webp`; artpreflight `--type ICON`.
3. Review sheet: live icon, each candidate and the approved Dragon King's Scroll side by side, on the LEGENDARY frame at
   160 px and at 45 px.
4. After the director picks (and picks the description), build the suggestion: one item edit of `image` and
   `description`, with its rationale.
