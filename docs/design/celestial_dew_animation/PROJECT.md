# Celestial Dew: animations

- **Director, 2026-10-24:** "Let's do celestial dew next... I kinda think celestial dew looks good as the reverted version.
  We just need to make a cool animation for it. Crescent moon above the player, single celestial drop falls at their
  feet and splashes, disappear animation shows a celestial ward appearing. So long as the shield is active it displays a
  semi-transparent subtle celestial shield effect."
- **Icon:** unchanged. The live icon is our reverted version (scored 10/10, "no notes; well liked"):
  `art/jutsu_icons/celestial_dew/refs/ref_cd_live_icon.webp`; the original: `ref_cd_original_icon.webp`.
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
