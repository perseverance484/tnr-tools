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

## 3. Layout (`layout_guide.png`)

The 50 px effect square is centred on the tile and the round portrait reaches its top edge, so there is no room above
the portrait: the **crescent rests on the portrait's top rim** like a crown, horns hanging down its sides. The feet are
directly below the portrait, so a straight fall crosses the face. Two options (director's choice):
- **A (proposed):** the drop forms at the crescent's right horn and **runs down the outside curve of the coming ward** to
  the feet, tracing the shape the ward will take; it never crosses the face.
- **B:** a straight fall from the crescent through the centre, in front of the portrait (fast, about 3 frames over the
  face).

## 4. Storyboard (36 ms frames; all start on the same tick)

| Time | heal appear (cast) | shield appear (ward) | shield static (loop) |
|---|---|---|---|
| 0-0.5 s | the crescent blooms on the rim from a sliver, glints | - | the dome, very faint |
| 0.5-0.8 s | a drop swells at the horn's tip | - | " |
| 0.8-1.2 s | the drop falls (A or B), a faint trail | - | " |
| 1.2 s | the splash at the feet: a low crown splash, ripple rings, glints | a front of light sweeps up the dome from the splash | " |
| 1.2-2.0 s | the crescent rises and fades into stars | the dome flares, then settles to the static level | " |
| then | - | - | a subtle dome: bright rim, clear centre, a slow shimmer band, a few twinkling stars (seamless, 3.6 s) |

Shield **disappear** (about 1 s): cracks run down the dome from the top, curved shards fall and fade, stardust drifts up.

## 5. Log

| Date | What happened |
|---|---|
| 2026-10-24 | Project opened; slots read from source; layout guide; art request and session prompt written. |
