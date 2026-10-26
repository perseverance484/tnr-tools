# Ethereal Rebirth: art session prompt (round 3, polish)

- **Base:** round 2's R2-2, the director's pick
  (`art/jutsu_icons/ethereal_rebirth/candidates/round2/raw_ethereal_rebirth_r2_2.png`). Review: `docs/design/icon_overhaul/
  ethereal_rebirth/ROUND2_REVIEW.md`. Text (approved): `ethereal_rebirth/TEXT_V2.md`.
- **Scope:** polish only. Three changes; nothing else moves.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes the polish round of
the Ethereal Rebirth jutsu icon. Read docs/design/icon_overhaul/ethereal_rebirth/ROUND2_REVIEW.md first.

Attach the director's pick as the SUBJECT reference and keep it as close as possible:
art/jutsu_icons/ethereal_rebirth/candidates/round2/raw_ethereal_rebirth_r2_2.png

Make exactly these three changes and nothing else:
1. ZOOM OUT about 5%: the left hand, the right hand and the hair must clear the frame edges with a small dark margin;
   keep the knees-up crop and the figure's size otherwise.
2. HALVE THE FLECKS: remove about half of the loose flecks of light, mostly from the four corners; keep a few close to the
   body, peeling off it into the ribbons.
3. The ribbon crossing the legs: a little MORE SEE-THROUGH, so the legs show through it more clearly.

Keep everything else exactly as in R2-2: the pose, the face, the gold eyes, the white hair, the navy armour and its rim
light, the crimson scarf and sash, the seal rings at the hands, the cracked white-gold chest core (still the brightest
point), the gold and blue-white soul-light ribbons, the gold ribbon whipping out of the frame at the upper right (it is
the one thing allowed to cross the frame edge), the dark navy background. Non-elemental: no fire, water or lightning.
Premium TNR pixel art as drawn; square, opaque, full-bleed; no text or symbols.

Generate two candidates, each in its own isolated generation session. Return the raw images only, named
raw_ethereal_rebirth_R3-1.png and raw_ethereal_rebirth_R3-2.png. Do not process, crop or upload anything. Fail fast:
regenerate once if anything other than the three changes moved (pose, face, colours, ribbon layout).
~~~

## Intake (Claude Code)

1. Raws to `art/jutsu_icons/ethereal_rebirth/candidates/round3/`.
2. Gate sheet with R2-2 as a reference row; check the edges (left, right, top strips), the flecks in the badge corners and
   the 45 px read against R2-2.
3. On approval: export 256 px lossless WebP to `art/jutsu_icons/ethereal_rebirth/exports/`, run
   `artpreflight.py --type JUTSU_ICON`, and hold it for the suggestion with the approved text and the cast animation.
