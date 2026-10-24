# Celestial Dew: animations

- **Director, 2026-10-24:** "Let's do celestial dew next... I kinda think celestial dew looks good as the reverted version.
  We just need to make a cool animation for it. Crescent moon above the player, single celestial drop falls at their
  feet and splashes, disappear animation shows a celestial ward appearing. So long as the shield is active it displays a
  semi-transparent subtle celestial shield effect."
- **Icon:** our reworked ("reverted") icon comes back. It is **not live**: the live record went back to the original
  (director, 2026-10-24: "The reverted version isnt live, thats why its called reverted"); the public read of 2026-10-23
  still showed the rework. Ours (scored 10/10, "no notes; well liked"): `art/jutsu_icons/celestial_dew/refs/
  ref_cd_live_icon.webp` (the filename predates the correction), exported as `exports/icon_jutsu_celestial_dew_v1.webp`;
  the original (live): `ref_cd_original_icon.webp`. It ships in the push/240 suggestion.
- **Text:** unchanged. The live text already describes this animation (crescent moon, a single drop of starlight that
  splashes, a dome of silver light that becomes a ward).
- **Method:** the Ethereal Rebirth route. The art director paints transparent layers in the icon's style; Claude Code
  animates them by script (`build_strip.py`, Pillow), previews over the director's battle recording, and builds the
  manifests. Live-game requests/writes: 0.

## 1. The jutsu (public read 2026-10-23)

| | |
|---|---|
| Id | `2vNeMhph6A9Ld--WXa35O`; A rank, EVENT, target SELF, cooldown 7, non-elemental |
| heal | power 40, 1 round, INHERIT; appear `I9aYhT5wMB` (a generic heal), appear SFX kept |
| shield | power 90 (the chance it forms), health 600, 2 rounds, INHERIT; no animations |

## 2. How the game plays the slots (source a744c04)

| Slot | When it plays | Source |
|---|---|---|
| heal **appear** | once, at cast, on the caster | `process.ts:1559` |
| shield **appear** | once, at cast, on the caster, in the same pass as the heal's | `process.ts:1559`, `combat.ts:482` |
| shield **static** | loops from the same tick while the shield stands | `combat.ts:667` |
| shield **disappear** | once, when the shield ends: its 2 rounds run out, it is broken (`tags.ts:2291`), or it fails to form (10%: `tags.ts:2279`, then appear and disappear play together) | `process.ts:1578` |

So the director's "disappear shows a celestial ward appearing" is built as the shield's **appear** (it plays right after
the splash; a disappear would play rounds later), and the shield's **disappear** shows the ward shattering into stardust
(on expiry, on a break, and on the 10% fail, where players then see the ward try to form and shatter, matching the game's
"shield was not created" message). The static dome is there faintly from the first frame; the splash makes it flare into
full form and settle back (the Ethereal Rebirth hand-off method).

## 3. Layout and motion (`layout_guide.png`)

The 50 px effect square is centred on the tile and the round portrait reaches its top edge, so the **crescent rests on
the portrait's top rim** like a crown, horns hanging down its sides. The director's two motions (2026-10-24):
- **Ripple (proposed):** "a drop falls into the middle of the portrait, splashes and then ripples flow outward and hit
  the edges of the portrait and energize it with a celestial shield". It matches the live battle line ("falls a single
  drop of starlight that splashes across %user and spreads into a dome of soft, silver light"), and the ward becomes the
  portrait's own rim lit up, which reads at 50 px better than a faint dome around it. The splash and ripples cross the
  face briefly and see-through, like dew on glass.
- **Run:** "fall, run along the portrait curve, drop and splash at the bottom then form into a celestial ward around the
  portrait". Never crosses the face; longer travel; the text would need "splashes across %user" softened.
The art layers serve both, so the choice can be made on a moving preview.

## 4. Storyboard (ripple; 36 ms frames; all start on the same tick)

| Time | heal appear (cast) | shield appear (ward) | shield static (loop) |
|---|---|---|---|
| 0-0.45 s | the crescent blooms on the rim from a sliver, glints | - | the rim halo, very faint |
| 0.45-0.75 s | a drop swells at the crescent's lowest point | - | " |
| 0.75-0.95 s | the drop falls into the portrait's centre, accelerating | - | " |
| 0.95 s | a small crown splash at the centre; glints thrown up | - | " |
| 0.95-1.45 s | ripple rings spread outward across the portrait (see-through) | as each ring reaches the rim, the rim ignites: a ring of light runs round it | " |
| 1.45-2.2 s | the crescent rises and fades into stars | the halo flares, a faint glassy sheen washes over the portrait, then both settle to the static level | " |
| then | - | - | the ward: a soft glowing ring hugging the portrait's rim, a slow light travelling round it, a very faint sheen, two or three twinkling stars (seamless, 3.6 s) |

Shield **disappear** (about 1 s): the halo cracks into curved shards that drift outward and fade, stardust rising.

## 5. Log

| Date | What happened |
|---|---|
| 2026-10-24 | Project opened; slots read from source; layout guide; art request and session prompt written. |
| 2026-10-24 | Director's two motions (ripple, run); ripple proposed; art layers revised to serve both. |

## 6. v1 build (2026-10-24)

Layers delivered by the art director (`art/jutsu_icons/celestial_dew/animation/raws/anim_cd_*`: crescent, drop, splash,
ripples, ward ring, glints, shards; real alpha). `art/jutsu_icons/celestial_dew/animation/build_strip.py` (Pillow; the
portrait geometry, mask, edge fade and helpers come from Ethereal Rebirth's script) builds four strips at 36 ms per
frame, 112 px frames:

| Strip | Slot | Frames | Bytes |
|---|---|---|---|
| `anim_celestial_dew_cast_v1.webp` | heal appear | 66 (2.4 s) | 207,750 |
| `anim_celestial_dew_ward_v1.webp` | shield appear | 66 | 150,784 |
| `anim_celestial_dew_loop_v1.webp` | shield static | 100 (3.6 s, seamless) | 198,578 |
| `anim_celestial_dew_break_v1.webp` | shield disappear | 30 (1.1 s) | 83,942 |

- The crescent (turned 45 degrees, 0.80 of the frame wide) rises **behind** the head like a halo, under the portrait
  mask; its upper horn stands clear at the top right. The drop (located on that horn's tip by measurement) swells, falls
  into the portrait's centre (frame 24, 0.86 s), splashes (the crown, a flash, glints thrown up), and two ripples run out
  to the rim, see-through.
- The ward ring (its band's inner edge at 0.215 of the frame, measured from the art, so it lies over the portrait's white
  rim) ignites as the ripples arrive (frame 38, 1.37 s), flares, a light runs once round it, a sheen washes the portrait,
  glints spark round it; then it fades over the loop's copy.
- The loop: the ring at 30% (still: a turning ring changed every pixel and cost 619 KB), a brighter arc travelling round
  once per loop, three stars twinkling in turn.
- The break: the ring flashes and is gone; nine curved shards spring from it, drift out, turn and fade; stardust rises.
- Preflight `--type ANIMATION`: only `soft_edges` on each (the known gap for glow). Preview `v1_over_avatar.gif` (the
  whole life of the shield), stills `v1_key_frames.png`.

## 7. v2 (2026-10-24)

Director: "Have cast and ward form both start from shield appear so they can be timed correctly. The moon is too large.
It needs to be oriented upright. The ward should not appear until the ripples hit the edge, that is how it forms. Have a
much smaller moon appear oriented directly above the player portrait like we did for the chakra overflow rising star
placement of the star. Moon appears, drop falls from it like in the icon, drop hits the portrait while the ripples flow
outward and charge the portrait edges with a celestial shield, the moon fades out."
- **One strip on the shield's appear** (`anim_celestial_dew_appear_v2.webp`, 66 frames, 239,140 bytes). The heal's appear
  is cleared in the suggestion (its generic animation would play over this one); its appear sound stays.
- **The moon:** upright as in the icon, 0.20 of the frame tall, centred 0.105 from the top (Chakra Overflow's crown star:
  0.075, about 0.24 tall), placed so its lower horn's tip is directly above the portrait's centre (located by
  measurement). Appears over frames 0-10 with a glint; fades upward once the ward has formed.
- **The drop** swells at the horn (frames 8-13) and falls straight into the centre, landing at frame 20 (0.72 s): splash,
  flash, glints thrown up.
- **The ripples** run out; the outer one reaches the rim (0.272) exactly at frame 32 (1.15 s), where the ward ring
  ignites. Nothing of the ward is drawn in this strip before then.
- **The loop** (`loop_v2`, 172,194 bytes) lowered to 18% ring + a 28% travelling arc: the game starts it on the cast's
  tick and cannot delay it, so it is faintly there before the ward forms; kept to a whisper. **The break** unchanged
  (`break_v2`, 81,778 bytes).
- Previews: `v2_over_avatar.gif`, `v2_key_frames.png`.

## 8. v3 (2026-10-24)

Director: "Have the shields loop be the ward glowing, like fading in and out, and the static animation is timed to when
the drops flow outward and power up the shield the first time. So the appear animation is the moon and drop + ripples,
timed with the static animation which is a looping glow effect. Try to make it slower, it plays way too fast."
- **appear** (`appear_v3`, 74 frames x 46 ms = 3.40 s, 132,350 bytes): the moon (in over 0.64 s, glint), the drop
  (swells 0.55-0.92 s, lands 1.38 s), the splash, the ripples (the outer one reaches the rim at frame 50, 2.30 s), sparks
  round the rim there, the moon fades. No ward drawn here.
- **loop** (`loop_v3`, 64 frames x 72 ms = 4.61 s, 206,270 bytes): the ward ring breathing. It starts dark on the appear's
  tick (so nothing of the ward shows before the ripples), rises over loop t 0.40-0.50 and peaks at t = 0.5 = 2.30 s, exactly
  when the ripples hit the rim, then fades slowly back to dark at the seam; three stars wink near each peak. One breath
  every 4.6 s; the ward is dark for about 1.8 s of each breath.
- **break** (`break_v3`, 30 frames x 46 ms = 1.38 s): the ring flashes and shatters into shards.
- Preview `v3_over_avatar.gif` (composited on real time, two breaths then the break); stills `v3_key_frames.png`.

## 9. The heal's own animation stays (2026-10-24)

Director: "Here's the heal animation. Do note that appears on the heal tag, not on the shield tag and would still play
normally. Ours is for the shield tag." The heal effect keeps its appear animation `I9aYhT5wMB` (a heart forming in a puff
of cloud; 20 frames of 128 px, `art/jutsu_icons/celestial_dew/refs/ref_cd_heal_animation_I9aYhT5wMB.webp`); it plays at
cast alongside the shield's appear. The suggestion leaves the heal effect untouched (corrects section 7, which planned to
clear it). Previews and the showcase now composite it under ours; its frame time is not on record here and is assumed
60 ms.

## 10. v4: the ring no longer clips at the top (2026-10-24)

Director: "The animations circle seems to clip at the top when the ward forms". The portrait reaches to 0.024 of the
frame top, so the ring round it (band outer edge 0.278) and its glow ran past the frame edge and under the 7% edge fade.
Now: the band's inner edge at 0.19 (outer about 0.246, top about 0.05), over the portrait's white rim; the edge fade
narrowed to 2.5% for Celestial Dew; the ring's outer glow softened (alpha^1.5). The ripples end at the band's middle
(0.22). Strips `*_v4`: appear 105,974 bytes, loop 161,768, break 75,622. Shipped to the existing assets by push/243.

## 11. v5: a natural hand-off (2026-10-24)

Director: "Make its fade in and out look more natural. The appear animation can brighten it earlier and faster so then it
appears to hold longer when the breathe effect reaches its full effect as the appear animation fades, like they're doing
a handoff. Then the breathe animation does the rest."
- The **appear** draws its own copy of the ring: it flashes up as the ripples touch the rim (frames 48-51, about 2.3 s),
  holds at full for 12 frames, then fades over 10 (to about 3.3 s).
- The **loop** (now 64 frames x 90 ms = 5.76 s per breath) rises gently underneath from phase 0.38 and peaks in the middle
  of that fade (phase 0.535, about 3.1 s), then fades softly (a half cosine) back to dark at the seam; stars wink round its
  peak.
- Seen together (measured): dark until 2.2 s; a quick rise to about 0.95 by 2.4 s; a hold near 0.96 to 3.3 s; a soft fade to
  dark by 5.6 s; then the loop breathes on its own (a gentle rise, a long fade).
- Strips `*_v5`: appear 176,282 bytes, loop 162,408, break 75,622 (unchanged art). push/243 now ships v5.

## 12. v6: the portrait's real geometry, from the pinned source (2026-10-24)

Director: "The dimensions of our animation dont line up with the portrait. Need to get the exact dimensions correct, not
estimate from screenshots. Find the information in the pinned source code." (recording:
`battle_recording_2026-10-24b.mp4`).

**What the source says** (a744c04, `libs/threejs/combat.ts`, `libs/combat/util.ts`, `drizzle/constants.ts`):
- the effect is a unit sprite scaled to `EFFECT_ANIMATION_SIZE` = 50 world units, centred at (w/2, h/2) of its tile
  (`drawCombatEffect`); the user's avatar is a circle-masked sprite 0.8 h square at (w/2, 1.0 h); the white marker
  0.9 h x 1.1 h at (w/2, 0.9 h); the star h/2.5 at (w/2, 0.4 h); the health bar at h + w/3 (`createUserSprite`); both
  groups sit at the tile origin (-x, -y) (`combat.ts:731`, `:1067`);
- the camera is orthographic over the canvas width (`Combat.tsx:1038`), so a world unit is a CSS pixel; the grid is 12
  columns (`getBattleDimensions`), `hexsize = width / (12 - 0.25 x 11)` (`drawCombatBackground`,
  `HEX_STACKING_DISPLACEMENT` = 0.25) and the tile height `h = hexsize x HEX_ASPECT_RATIO (0.5)` = width / 18.5.
- So in the effect square: avatar centre at 0.5 - h/100 from the top, radius 0.4 h / 50; star centre 0.5 + h/500.
  **The effect is a fixed 50 px while h grows with the canvas**, so the portrait's place in the square depends on the
  screen width: no single strip lines up on every screen (true of every effect animation in the game).

**The error:** every earlier preview placed the effect square on a recording by assuming the portrait's proportions in
it (inherited from Chakra Overflow), never measuring them. That assumption (portrait centre 0.296, outline radius 0.272)
was wrong for the director's screen; the real avatar there is centre 0.339, radius 0.130.

**Reference screen:** the director's phone. Measured from the v5 ring in the new recording, the effect square is 184.1
recording px across at (219.3, 132.1); the source model then gives h = 16.1 (a canvas about 298 CSS px wide) from the
avatar's centre and predicts its radius as 0.129, matching the measured 0.130. The white marker disc (its art is not in
source) measures centre 0.325, radius 0.163; the health bar sits at 0.124.

**v6** (`build_strip.py`: `H_REF` = 16.1 and the formulas above): the ward band starts just outside the white disc and is
centred on it; the drop falls into the avatar's centre; the ripples run from there to the band; the moon (0.11 tall) sits
above the health bar; splash, glints, sparks and shards scaled to the real portrait. Strips `*_v6`: appear 121,684 bytes,
loop 133,558, break 50,282. Checked composited onto the recording at the game's placement: `v6_on_your_recording.png`.
Previews and the showcase now use the new recording (`battle_still_2026-10-24b.png`) at that placement.

**Also affected:** the Ethereal Rebirth animations (cast, loop, hit) were built on the same assumed portrait; they need
the same correction.

## 13. v7, and other screens (2026-10-24)

Director: "It also brightens too suddenly with the appear animation, slow it down a lot." The appear's copy of the ward
now rises over 18 frames (0.83 s) from just before the ripples reach the rim, holds 10, fades over 14; the appear is 92
frames (4.2 s); the loop is 64 x 100 ms = 6.4 s, peaking (about 3.9 s) in the middle of that fade. Seen together: dark
until 2.2 s, about 0.7 by 2.75 s, full by 3.0 s, held to about 4.3 s, a soft fade to dark by 6.3 s.

Director: "Will our celestial dew draw properly for everyone's screens? It needs to fit everyone's appropriately." From
the source formulas (section 12), the avatar in the 50 px effect square:

| Canvas width (CSS px) | h | Avatar centre (from top) | Avatar radius |
|---|---|---|---|
| 298 (the director's phone) | 16.1 | 0.34 | 0.13 |
| 375 (typical phone) | 20.3 | 0.30 | 0.16 |
| 430 (large phone) | 23.2 | 0.27 | 0.19 |
| 676 (the widest the layout's main column renders, `Welcome.tsx` comment) | 36.5 | 0.13 | 0.29 |

One strip is drawn at a fixed 50 px for every screen, so it can match the portrait at one canvas width only; this is true
of every effect animation in the game. Options are set out to the director (a game-side change that scales effects with
the tile; or tuning for a target width and making the design tolerant; or anchoring to the tile instead of the portrait).

## 14. Upstream request (2026-10-24)

The director opened a pull request on `studie-tech/theninjarpg` (from a fork, through the GitHub website) changing the
two `showAnimation` calls in `drawCombatEffect` from `scale: EFFECT_ANIMATION_SIZE` to `scale: h * 2.5`
(`REQUEST_scale_effect_animations.md`, `scale_effect_animations.patch`, against main `2af4b32`). Not visible to this
session (the repository is not attached). If it merges, the effect square becomes 2.5 tile heights on every screen and
the portrait sits at a fixed place in it (avatar centre 0.3 from the top, radius 0.16, the h = 20 layout); Celestial Dew
and Ethereal Rebirth are then rebuilt to that one layout and fit every screen. Until then, v7 (tuned to the director's
phone) ships.
