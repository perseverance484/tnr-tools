# Ikazuchi Kunai: art session prompt (round 1)

- **Plan:** `docs/design/kunai_family/PROJECT.md` (research, problems, family base).
- **Goal:** a premium Ikazuchi Kunai item icon on the classic kunai silhouette (leaf blade, wrapped grip, ring pommel),
  with lightning forged into the blade. It sets the base for the five elemental kunai. Two candidates, each in its own
  isolated session.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes ONE item icon: the
IKAZUCHI KUNAI, a lightning-forged throwing kunai. It sets the shared design for a family of five elemental kunai. Read
docs/design/kunai_family/PROJECT.md first.

Attach as references, with these roles:
1. QUALITY AND FAMILY (match the rendering and the anatomy, not the colours):
   art/item_icons/kunai/refs/ref_bloodthorn_kunai_live.webp - leaf blade with a vein pattern forged into it, cord grip,
   ring pommel, transparent background. This is the quality bar.
2. SILHOUETTE (the classic kunai shape): art/item_icons/kunai/refs/ref_kunai_live.webp
3. OLD VERSION (keep only the idea, a lightning kunai; NOT its shape, background or noise):
   art/item_icons/kunai/refs/ref_ikazuchi_kunai_live.webp

Prompt:
open square pixel-art icon of a single kunai lying diagonally at 45 degrees, tip at the lower left and ring at the upper
right, a broad leaf-shaped blade with a raised centre ridge forged from blue-black storm steel, branching lightning veins
etched into the blade glowing pale electric blue and brightest at the tip, thin crackles of electricity hugging the
blade's edges only, a short steel collar, a tightly wrapped deep indigo cord grip, a round steel ring pommel with a short
loop of cord and a small pale-yellow tassel, the spark at the tip is the brightest point, bold clean dark outlines, crisp
pixel lineart, flat cel shading with painterly texture, limited palette, soft even lighting, strong readable silhouette,
centered with a small margin, transparent background, no frame, no text.
Negative: no background, no black square, no storm clouds, no lightning filling the frame, no aura, no glow disc, no
sparkles, no three-pronged kunai, no extra blades, no seal, no paper tag, no writing, no letters, no symbols, no hand, no
person, no asset sheet, no grid, no circular medal frame, no labels, no multiple icons, no franchise insignia.

Generate two candidates, each in its own isolated generation session:
IK-1: as above.
IK-2: as above, but the blade a little longer and narrower and the edge crackle even quieter (the etched veins carry
      the lightning).

Square, 1024 x 1024. Return the raw images only, named raw_ikazuchi_kunai_IK-1.png and raw_ikazuchi_kunai_IK-2.png. Do
not process, crop or upload anything. Fail fast: regenerate once if the background is not transparent, the kunai has
three prongs or twin flanges, the ring is not at the pommel, lightning fills the frame, any writing or seal appears, or
the kunai is cropped or touches an edge.
~~~

## Intake (Claude Code)

1. Raw QC (transparent, single kunai, ring pommel, no text).
2. Process with `art/item_icons/chunin_exam_scrolls/process_icon.py`, export to
   `art/item_icons/kunai/exports/icon_ikazuchi_kunai_v1.webp`; artpreflight `--type ICON`.
3. Review sheet: the live icon, each candidate and Bloodthorn Kunai side by side, on the COMMON frame at 160 px and at
   45 px.
4. After the director picks, build the suggestion (one item edit of `image`, with its rationale).
