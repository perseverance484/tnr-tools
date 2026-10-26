# Art request: Chakra Overflow animation, crown layout layers

- **For:** the art director
- **From:** Fable / Claude Code, at dauntless's request (2026-10-23)
- **Why:** the director's battle recording showed the cast animation playing *over* the character. The game draws an
  animation as a square centered on the tile (`libs/threejs/combat.ts`, `EFFECT_ANIMATION_SIZE`), and the character's round
  token sits in the upper half of that square, so the frame's top edge is level with the top of the token. The director
  chose the **crown layout**: the character is kept clear inside the blue-and-gold wings, and the star sits **on top of the
  head**, where the glint flares and winks out. "I like it on top of the head. We'll have to clean up the icon to match."
- **Now:** a working version is built by script from the round-A layers, with a soft circular window cut out of the wings
  (`docs/design/chakra_overflow/animation/crown_in_battle_preview.gif`). The cut-out leaves the wings looking cropped. This
  request is for **clean layers drawn for this layout**, so the wings frame the character on purpose.
- **Not in scope:** the jutsu icon stays as approved; the animation is drawn for the battlefield, the icon for the bar.
- **Live-game requests/writes:** 0.

## 1. Layout (frame fractions, 0 = top-left, 1 = bottom-right)

`docs/design/chakra_overflow/animation/crown_layout_guide.png` shows it at 1254 px:

| Zone | Where | Rule |
|---|---|---|
| Character window (red circle) | center (0.50, 0.283), radius 0.24 | **completely empty**: the character's token shows here |
| Star (gold box) | center (0.50, 0.075); box x 0.38-0.62, y 0.00-0.20 | the star sits on top of the head; it may overlap the very top of the window slightly, never the face |
| Wings | either side of the window and below it, meeting in a V at about (0.50, 0.88) | wing tips rise beside the head (to about y 0.05-0.15), the wings sweep around the window like hands cupping it |
| Safe area (blue) | x 0.06-0.94, y 0.04-0.96 | nothing outside it except the star's top ray |

## 2. Deliverables

Each 1254 x 1254, transparent (or flat lime `#00FF00`), centered exactly like the guide, same palette and finish as the
approved icon and the round-A layers:

- **C1 WINGS (crown):** the two blue-to-gold wings, redrawn to wrap **around** the empty character window: inner edges
  following the circle with a clean glowing rim, tips rising beside the head, base V below. No art inside the window.
- **C2 STAR (crown):** the four-point star, drawn **for its small size**: about 0.24 of the frame tall, bolder and simpler
  than L1 (thicker rays, a hot white core, crisp gold edges) so it reads at the 50 px battle size. Long upper ray, as in
  the icon.
- **C3 PEAK (optional):** a composed reference frame of C1 + C2 at full glow, for checking the look.

The flash (L3) and sparks (L4) from round A are reused; the dissolve and the glint are scripted.

## 3. Checks before returning

- Lay each layer over the guide: nothing inside the red circle; the star inside the gold box; everything inside the blue area.
- View C1 + C2 together at 64 px: the wings must read as framing a center, and the star as a star.
- No fire or flame tongues, no figure, no text or runes, no spiral or ring, no franchise looks.

## 4. Intake (Claude Code)

`art/jutsu_icons/chakra_overflow/animation/raws/anim_co_C1_wings_crown.png`, `anim_co_C2_star_crown.png` (and C3);
`build_strip.py` switches to them (the scripted window then becomes unnecessary), rebuilds the strip, re-previews it over the
battle recording, and push/226 (asset create) and push/225 (jutsu suggestion) follow.

## 5. Delivered and placed (2026-10-23)

C1 (wings), C2 (star) and C3 (peak reference) delivered as 1254 px transparent PNGs. The wings' drawn window sits lower and a
little smaller than the guide (centered about 0.40 of the frame instead of 0.283), and the star is drawn lower (center 0.176)
and slightly larger, so `build_strip.py` places the layers rather than using them as-is: wings scaled 1.10 and raised 30 px,
the placement that best clears the character inside the frame (16% of the token area still under the wings' inner rim,
which reads as a frame around the token); star scaled to 0.24 of the frame and centered at 0.075. Placement comparison over
the battle recording: `docs/design/chakra_overflow/animation/crown_art_placement_options.png`. A soft fade where the wings
cross the token is one switch away (`CROWN_FADE`). New strip: 48 frames at 54 ms (2.6 s), 344,630 bytes; in-battle preview
`crown_in_battle_preview.gif`.
