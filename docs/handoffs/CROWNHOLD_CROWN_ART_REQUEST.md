# Art request: Arakane's Command Crown (Arakane avatar, Crownbreaker badge)

- **Director, 2026-10-25:** "Crownbreaker. And now Arakane needs a cool Crown, and the badge is that Crown breaking. So he
  needs a better Crown than the captain. Its how they control the other afterimages" (RUL-2026-10-25-011).
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`: one image per fresh session, at most two individual
  reference images, one candidate at a time. Avatar first: it locks the crown's design; the badge then attaches it.
- **Live-game requests/writes:** 0.

## The crown (design lock)

The Crowned Captain's Skyglass Crown (`art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp`) is a jagged
cyan-crystal half-crown on an iron band with a small seal disc. Arakane's must clearly outrank it and say "command":

- a closed circlet of **blackened gold** (not the Captain's iron), engraved with seal-script;
- a **halo of seven Skyglass blades floating above the band**, evenly spaced, not touching it;
- at the front a large faceted **Skyglass prism core** carrying the pale circled-cross seal, burning white at the centre;
- **thin glowing threads** running from each floating blade down and away out of frame: the control lines to the
  afterimages he commands;
- palette: blackened gold, pale cyan Skyglass, white-hot core. One accent colour family, as the Skyglass sets use.

## 1. Supreme Commander Arakane (AI avatar)

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session draws ONE AI avatar:
Supreme Commander Arakane, master of the Crownhold fortress. Generate exactly ONE candidate. Do not process, crop, key or
upload anything.

Attach two references, with these roles:
1. STYLE (match rendering, outline, palette handling and pose energy; NOT the character): avatar_ghost_ship_crowned_captain_b.webp.
2. THE LESSER CROWN (do NOT copy; Arakane's crown must clearly outrank it): icon_ghost_ship_skyglass_crown.webp.

Concept: the commander who issued the last directive. Tall, composed, ruthlessly calm; a dignified older warlord in
layered black-and-gold command armour and a long dark mantle, one gauntleted hand raised palm-down as if giving an order.
He wears the COMMAND CROWN: a closed circlet of blackened gold engraved with seal-script; above it a halo of seven pale
cyan Skyglass blades float evenly spaced, not touching the band; at the front a large faceted Skyglass prism core with a
pale circled-cross seal burning white at its centre; thin glowing cyan threads run from each floating blade down and
away past his shoulders and out of frame, like puppet strings. A command seal tablet (Countermand) hangs at his belt.

Prompt:
single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style
reference, limited palette of black armour, blackened gold, pale cyan skyglass and one white-hot core accent, a
commanding warlord with a floating halo crown of seven skyglass blades above a gold circlet and glowing control threads
trailing from the blades, front three-quarter view, whole figure and crown inside the frame with a clear margin, on a
true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no
second character, no copy of the reference crown's shape, no realistic or painterly rendering, no blur, no gradient
background, no sheet, no grid.

Rules: square, 1024 x 1024. Fail fast and regenerate once if the background is not flat magenta, anything touches an
edge, the crown is not clearly grander than the reference crown, the floating blades or the threads are missing, or the
rendering drifts from the style reference.

Return the raw image only, named raw_avatar_crownhold_arakane.png.
~~~

## 2. Crownbreaker (badge icon)

Run after #1 is approved.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session draws ONE badge icon:
Crownbreaker, earned by breaking Supreme Commander Arakane's Command Crown. Generate exactly ONE candidate. Do not
process, crop, key or upload anything.

Attach two references, with these roles:
1. SUBJECT (keep the crown's design exactly): the approved Arakane avatar. Keep the blackened-gold circlet with
   seal-script, the halo of seven floating skyglass blades, the faceted prism core with the circled-cross seal, and the
   glowing control threads.
2. STYLE (icon rendering and framing only): icon_ghost_ship_skyglass_crown.webp.

Concept: the Command Crown at the moment it breaks. The circlet is split down the middle through the prism core, the two
halves pushed apart; a white-hot crack of light bursts from the shattered core; the floating blades are scattered and
tumbling outward; the control threads are snapped, their loose ends curling and fading. No hands, no figure.

Prompt:
single game badge icon, the shattered command crown alone, crisp pixel art with clean dark outlines and flat cel shading
matching the style reference, limited palette of blackened gold, pale cyan skyglass and one white-hot burst of light at
the broken core, centred and symmetrical with a clear margin on every side, readable at 64 pixels, on a true solid flat
magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no UI, no watermark, no frame or medal border, no ribbon, no character, no hands, no
scenery, no shadow on the magenta, no magenta spill, no blur, no gradient background, no sheet, no grid.

Rules: square, 1024 x 1024. Fail fast and regenerate once if the background is not flat magenta, anything touches an
edge, the crown no longer matches the avatar's crown, or it does not read as broken at small size.

Return the raw image only, named raw_badge_crownbreaker.png.
~~~

## Intake (Claude Code)

Key magenta with `chroma.py`; avatar to the AI avatar target, badge to the ICON target (`25x_DATA_art_spec.json`);
review sheet against the Crowned Captain and his crown.
