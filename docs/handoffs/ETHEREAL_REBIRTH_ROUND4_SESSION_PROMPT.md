# Ethereal Rebirth: art session prompt (round 4, wider and more aggressive ribbons)

> **PAUSED (2026-10-24, RUL-2026-10-24-007):** Ethereal Rebirth is a Forbidden jutsu, so its icon is to be redrawn with
> the Forbidden Master (`docs/design/characters/FORBIDDEN_MASTER.md`) once the model sheet is approved. Do not run this
> prompt unless the director says otherwise.

- **Director, 2026-10-24:** "I think i want to make the icons energy ribbons wider and more aggressive like the
  animations. Its like the player is emitting energy waves that absorb damage."
- **Base:** the approved final icon (`art/jutsu_icons/ethereal_rebirth/candidates/round3/raw_ethereal_rebirth_final.png`,
  exported as `exports/icon_jutsu_ethereal_rebirth_v1.webp`). Text (approved, unchanged): `docs/design/icon_overhaul/
  ethereal_rebirth/TEXT_V2.md`. Its battle line still fits: "Ribbons of pale soul-light pour out of them and spin around
  their body before one lashes out" (RUL-2026-10-24-004).
- **Scope:** the ribbons only. The warrior and everything else stay.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes round 4 of the
Ethereal Rebirth jutsu icon: the approved icon with its energy ribbons redrawn wider and more aggressive, to match the
jutsu's cast animation.

Attach as references, with these roles:
1. SUBJECT (keep as close as possible): art/jutsu_icons/ethereal_rebirth/candidates/round3/raw_ethereal_rebirth_final.png
2. RIBBON STYLE (match the bands' width and energy): art/jutsu_icons/ethereal_rebirth/animation/raws/ref_anim_v5_peak.png
   (three frames of the cast animation; the dark circle is where the player's portrait sits) and the band layers
   art/jutsu_icons/ethereal_rebirth/animation/raws/anim_er_v5_R1_band_gold_a.png and anim_er_v5_R2_band_blue_a.png.

The idea: the warrior is EMITTING waves of soul-light that absorb damage. The ribbons are no longer thin streamers drifting
around him; they are broad, powerful bands surging out of him and sweeping round him as a guarding storm of light.

Change only the ribbons:
1. WIDER: about twice their current width, broad flat bands like the animation's (a translucent pale wash inside with
   lighter streaks along it, a crisp near-white line on each long edge, a soft glow outside: warm amber for gold, deep blue
   for blue). They must still read as bands, not blobs, at 45 px.
2. MORE AGGRESSIVE: they burst outward from the chest core and sweep round the body in fast, tight, sharply curving arcs,
   like shockwaves of light; tips taper into long whip points that snap and curl; a sense of speed along each band.
   Fewer, stronger bands: about four to five in all (gold and blue), not many thin ones.
3. PROTECTIVE: the bands wrap round the warrior as a guard, mostly BEHIND and AROUND the silhouette. Where a band crosses
   in front of the body it turns see-through. The face, the chest core and the two hands are never covered.
4. Keep the gold band whipping out of the frame at the upper right (the lash at the enemy; the one thing allowed to cross
   the frame edge).

Keep everything else exactly as in the final icon: the pose, the face, the gold eyes, the white hair, the navy armour and
its rim light, the crimson scarf and sash, the seal rings at the hands, the cracked white-gold chest core (still the
single brightest point), the few small four-point sparkles, the dark navy background, the crop and margins. Palette:
gold pale cream #fef383 to white with amber glow #e27d1b; blue icy #9aa4d2 to #75dcff with deep-blue glow #286aec.
Non-elemental: soul-light only, no fire, water or lightning. Premium TNR pixel art as drawn (no pixel conversion);
square, opaque, full-bleed; no text or symbols.

Generate three candidates, each in its own isolated generation session. Return the raw images only, named
raw_ethereal_rebirth_R4-1.png, raw_ethereal_rebirth_R4-2.png and raw_ethereal_rebirth_R4-3.png. Do not process, crop or
upload anything. Fail fast: regenerate once if the warrior changed (pose, face, colours), if a band covers the face, core
or hands, or if the bands turned into a busy tangle that loses the figure at thumbnail size.
~~~

## Intake (Claude Code)

1. Raws to `art/jutsu_icons/ethereal_rebirth/candidates/round4/`.
2. Gate sheet (`docs/design/icon_overhaul/gate_sheet.py`) with the final icon as the reference row; check the 45 px read
   (figure still clear inside the bands), the face/core/hands kept clear, and the bands against the animation's.
3. On approval: export 256 px lossless WebP as `exports/icon_jutsu_ethereal_rebirth_v2.webp`, run
   `artpreflight.py --type JUTSU_ICON`, and rebuild push/236 with it (one suggestion: icon, text, cast animation, loop).
