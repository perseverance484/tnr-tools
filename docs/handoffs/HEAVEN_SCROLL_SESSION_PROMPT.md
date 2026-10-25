# Heaven Scroll: art session prompt (round 1)

- **Brief:** `docs/design/chunin_exam_scrolls/PROJECT.md`.
- **Goal:** the Heaven Scroll, the Earth Scroll's pair: same silhouette, gold caps and sealed cord, in the live scroll's
  navy, with a cloud relief on the seal. Two candidates, each in its own isolated session. If an Earth Scroll candidate
  is approved first, attach it as the PAIR reference so the two match.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes ONE item icon: the
HEAVEN SCROLL, the sealed scroll paired with the Earth Scroll in the Chunin Exams. Read
docs/design/chunin_exam_scrolls/PROJECT.md first.

Attach as references, with these roles:
1. SUBJECT (keep the object, colours and gold caps; NOT the character, the outline or the sparkles):
   art/item_icons/chunin_exam_scrolls/refs/ref_heaven_scroll_live.webp - the live Heaven Scroll: a closed hand scroll at
   45 degrees, deep navy brocade ends with a cloud-swirl pattern, cream paper middle, gold rings and round gold knob
   finials.
2. RENDERING GOAL (match the rendering, not the colours): art/item_icons/chunin_exam_scrolls/refs/style_dragons_scroll.webp
   and style_scroll_of_bastion.webp - our approved scroll icons: bold clean dark outlines, cel shading with painterly
   texture, rich material detail, a corded tie with tassels, transparent background.
3. PAIR (only if provided): the approved Earth Scroll icon. Match its shape, size, angle, caps, cord and seal exactly;
   only the colours and the seal's relief change.

Prompt:
open square pixel-art icon of a closed sealed hand scroll lying at 45 degrees, lower right to upper left, deep navy blue
brocade with a subtle darker cloud-swirl pattern, cream paper showing between gold rings, round gold knob finials on both
ends, a thick braided cord wrapped once around the middle and closed with a round crimson wax seal pressed with a relief
of a single curling cloud, two short navy tassels hanging from the cord, the wax seal is the brightest and most
eye-catching point, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, strong readable
silhouette, centered with a small margin, transparent background, no frame, no text.
Negative: no writing, no kanji, no letters, no runes, no symbols other than the cloud relief, no glow outline, no
yellow outline, no sparkles, no aura, no background, no asset sheet, no grid, no circular medal frame, no labels, no
multiple icons, no franchise insignia, no steel caps.

Generate two candidates, each in its own isolated generation session:
HS-1: as above.
HS-2: as above, but the scroll slightly shorter and fatter and the seal a little larger (more weight in the middle).
(If the Earth Scroll is already approved, generate only the variant that matches its proportions.)

Square, 1024 x 1024. Return the raw images only, named raw_heaven_scroll_HS-1.png and raw_heaven_scroll_HS-2.png. Do
not process, crop or upload anything. Fail fast: regenerate once if any writing or character appears, the seal is
missing or not the focus, the caps turn steel, the navy drifts to purple or bright blue, a glow outline or sparkles
appear, or the scroll is cropped or touches an edge.
~~~

## Intake (Claude Code)

1. Raw QC (no text, transparent or keyable background, whole object in frame).
2. Key if needed, trim, pad to an exact square with a small margin, export 256 x 256 lossless WebP to
   `art/item_icons/chunin_exam_scrolls/exports/icon_heaven_scroll_v1.webp`.
3. Review sheet: the live icon beside each candidate and beside the approved Earth Scroll, at 160 px on each rarity
   frame and at 45 px.
4. After the director picks, build the suggestion (one item edit of `image`, with its rationale).
