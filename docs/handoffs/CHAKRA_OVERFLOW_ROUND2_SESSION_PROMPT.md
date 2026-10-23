# Chakra Overflow: round 2 session prompt (boundless chakra)

- **Basis:** the draft 1 review and the director's concept correction (2026-10-23; RUL-2026-10-23-002 amendment):
  `docs/design/chakra_overflow/DRAFT1_REVIEW.md`, brief section 6.
- **Zip for the session:** `chakra_overflow_round2.zip` (contents listed in the prompt).
- **Intake:** raws to `art/jutsu_icons/chakra_overflow/candidates/`, then `preview_in_context.py` against draft 1 and the
  current icon.

## Paste into a new art-director session

~~~text
You are the art director for The Ninja RPG. This session runs ROUND 2 of the Chakra Overflow icon project, the most
scrutinized piece of art we will make.

Attached (chakra_overflow_round2.zip):
- CHAKRA_OVERFLOW_ICON_PROJECT.md: the project brief (usage data, where the icon appears, acceptance criteria;
  section 9 is the director's concept correction). Read it first.
- DRAFT1_REVIEW.md: the review of the director's first draft. Section 3 says what failed, section 5 how to fix it,
  section 6 is the round-2 brief you will run.
- raw_chakra_overflow_draft1.png: the director's first draft. For YOUR understanding only (what to keep, what to
  drop). NEVER attach it to a generation.
- draft1_in_context.png and draft1_grayscale_neighbors.png: the draft in the in-game battle bar, and in grayscale
  beside the icons it was confused with (it matched the Ethereal Rebirth flame pillar).
- icon_bee_unholy_enhancement_v2.webp and icon_jutsu_celestial_dew_v1.webp: rendering references only (finish,
  contrast, rim light, luminous core). Never copy their compositions.

Why it matters: Chakra Overflow is the most-used jutsu in the game (107,720 battle uses, 6.6% of all jutsu use).
Nearly every player opens with it, so its icon is the most-seen icon in the game.

The concept (director, 2026-10-23): BOUNDLESS CHAKRA. "An item doesn't need to overflow, the chakra we're depicting
is what's overflowing. You're activating this flow of energy by using the technique." There is no vessel, orb,
container or object: the chakra itself is the subject, flowing without limit.

Keep from draft 1: gold as the brightest value in the frame, and its rising central spike (the upward energy).
Drop from draft 1: flame tongues, the blue flame wings on each side, the bonfire fanning from the bottom edge, and
art that fills the frame edge to edge. Drawn as fire, it read as a fire-element jutsu (Chakra Overflow has no
element), at 32 px it looked like a fleur-de-lis, and its flames covered the corners where the game draws badges.

How to show boundless chakra:
1. Energy, not flame: luminous currents, light rays, smooth flowing streams, a crackling plasma edge, sparks rising.
2. One compact white-hot source just above the center; the chakra surges outward and upward from it without end.
3. Color as intensity: calm deep chakra blue at the outer reaches, hotter toward the source, turning gold and then
   white-hot at the heart. One energy rising in power, not two fires side by side. Deep blue, not cyan or ice blue.
4. Upward weight: the flow is strongest and longest upward, so the whole emblem points up (the power-up sign).
5. Endless but bounded: the streams thin and fade into the dark before they reach the edges, so the flow feels
   limitless while the emblem stays one clear shape.

Non-negotiables:
- Reads as "POWER UP" at 32 px with no label, and as one shape in grayscale.
- Emblem inside the central 80%, dark navy-to-black space on every side, BOTH bottom corners empty and dark (the game
  draws 28 px level and count badges there), nothing touching any edge.
- House rendering: detailed pixel-art finish, crisp edges, strong rim light, luminous core, high contrast, full-bleed
  dark background (opaque). Far fewer fractal wisps than draft 1.
- Exclusions: no flames or fire of any kind; no orb, sphere, vessel or object; no body, figure, face, hands, or aura
  outline of a person; no text, kanji, runes, seals, mandalas or eye emblems; no frame or UI; no franchise looks
  (Eight Gates, Rasengan, Super Saiyan aura); no spiral, vortex or ring; no crescent, dragon, droplet, or pillar rising
  from broken stone.

Run these briefs, ONE per isolated generation session, exactly one square candidate each (2 generations per brief,
6 raws in total):
- R2-a CHAKRA NOVA: the source bursts outward in every direction as luminous streams, the upward ones longest,
  forming a crown-shaped starburst.
- R2-b RISING TORRENT: a wide surge of chakra currents rushes upward from the source and converges into one sharp
  upward arrowhead, sparks streaming off its point.
- R2-c POWER FLARE: a tall teardrop flare of crackling chakra energy with a white-hot heart and an electric rim,
  shedding rising streams from its tip. An energy flare, not a flame, and no figure inside it.

For each generation use the full brief from DRAFT1_REVIEW.md section 6 plus that variant's line.

Fail-fast every raw before returning it: reject anything that reads as fire or flame tongues, contains an object or
figure, has a spiral, or touches an edge or the bottom corners, and regenerate it once. Look at each raw at 32 px
before accepting it.

Return every raw unprocessed (no crop, upscale or retouch), named raw_chakra_overflow_R2-a1.png, R2-a2, R2-b1 and so
on, each with one line on how it reads at 32 px. Do not pick a winner: the director shortlists after the in-game
preview.

Live-game requests/writes: 0. No credentials. Do not upload anything.
~~~
