# Art request: Chakra Overflow cast animation

- **For:** the art director
- **From:** Fable / Claude Code, at dauntless's request (2026-10-23): "a new animation to go with the new chakra overflow that
  suits the icon/color theme... would really take it to the next level."
- **Companion:** the icon project `docs/design/chakra_overflow/CHAKRA_OVERFLOW_ICON_PROJECT.md` (final icon: "the rising star").
- **Source basis:** game source `studie-tech/theninjarpg` at `107d7a8` (paths below); the art spec
  `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `ANIMATION`; one public read of the current asset.
- **Status:** analysis and brief. Art direction and acceptance are the director's (CLAUDE.md section 10).
- **Live-game requests/writes:** one public read (`gameAsset.get` of the current animation), no writes.

## 1. How jutsu animations work

| Fact | Detail | Source |
|---|---|---|
| Where an animation lives | an effect's `appearAnimation`, `disappearAnimation` or `staticAnimation` names a game asset of type `ANIMATION` | effect schema; `25x` ANIMATION target |
| Sheet format | **one vertical strip**, one column, frames stacked top to bottom; **every frame square**; `frames` 1-100 | `libs/threejs/util.ts` `showAnimation` → `createActionSprite(texture, 1, frames)` |
| Timing | `speed` is **milliseconds per frame** (1-100); total length = frames × speed. Appear and disappear play **once** and vanish; static loops | `SpriteMixer.ts` (`tileDisplayDuration`); `battlefieldPreview.ts` (`frames * speed`) |
| Size in battle | drawn as a **50 px** square sprite centered on the hex (`EFFECT_ANIMATION_SIZE = 50`); the sheet is loaded at 50 px wide | `libs/threejs/combat.ts:109`, `:646` |
| Size in content lists | a 112 px canvas, from the original sheet, so frames need at least 112 px (128 recommended) | `ContentImage.tsx`; `25x` min width |
| Blending | normal alpha blending (`SpriteMaterial`, no additive mode): the strip needs **real transparency**; a dark background would show as a dark square over grass or snow biomes | `SpriteMixer.ts:49` |
| Trigger for a self buff | the jutsu's `visual` effect carries `appearAnimation` (plays on the caster's hex when cast) and `disappearAnimation` (plays where the effect ends); `process.ts` turns them into one-shot visuals | `libs/combat/process.ts:190-210, 431-455` |
| Looping aura | `staticAnimation` renders only for ground effects drawn on a hex (`combat.ts:667`, inside the hex branch), so a self buff **cannot** show a persistent aura while it lasts; the cast flash is the moment to own | `libs/threejs/combat.ts` |
| Limits | lossless WebP, **under 460,800 bytes** for the whole strip; lime chroma key for production | `25x` ANIMATION target |

## 2. What Chakra Overflow uses today

Its `visual` effect plays **`spellcast_D_large_violet`** (`QgsljoZSCOKhdQxCIGnTU`) on cast and again on expiry: a stock
FX-pack sparkle burst, **violet and pink**, 29 frames × 50 ms = 1.45 s, 128 px frames
(`docs/design/chakra_overflow/animation/current_spellcast_violet_frames.png`). It is off-palette for the new blue-and-gold
icon, and it is **shared by six other jutsu** (Starlight Veil, Celestial Empowerment, Dragon Eye Awakening, Summoning:
Reptile Zoo, Starlight Shroud, Silent Tempest). So the new animation must be a **new asset**: editing the shared one would
change all seven.

## 3. Feasibility prototype (not art)

`docs/design/chakra_overflow/animation/prototype_build.py` cuts the star and wings out of the approved icon and animates
them by script: a core flash, the emblem growing while the wings are revealed from the bottom up, a hold with rising
sparks, then a rise and fade. Result: 24 frames × 128 px, 438 KB lossless (under the ceiling), about 1.2 s at 50 ms
(`anim_chakra_overflow_proto_frames.png`, `anim_chakra_overflow_proto_preview.gif` shows it on dark, mid and bright
battle backgrounds at 128 and 50 px).

What it proves: the format, the size budget, and that the icon's star-and-wings read at 50 px in motion. What it lacks:
real motion. It is the icon zooming, and its fade turns muddy over bright ground. The wings should **sweep**, the star
should **flare**, and the chakra should **pour upward**: that is drawn animation, the art director's work.

## 4. The brief

**Concept:** the moment the user releases boundless chakra: the rising star of the icon, coming to life.

**Storyboard (about 1.2-1.4 s; 24-28 frames at 50 ms):**

| Beat | Frames (at 50 ms) | What happens |
|---|---|---|
| 1. Ignition | 1-3 | a white-hot point flashes at the center |
| 2. The star flares | 3-8 | the four-point star snaps open, its upper ray shooting up longest |
| 3. The wings rise | 6-14 | deep blue chakra sweeps up and out from beneath the star into the two wings, burning gold toward the heart; the silhouette of the icon is complete by about frame 12 |
| 4. Overflow | 12-20 | the emblem glows at full strength; gold and blue sparks stream upward past it |
| 5. Release | 20-28 | the emblem lifts slightly and dissolves upward into rising sparks (dissolve, never a gray fade) |

**Rules:**
- Matches the icon: palette (deep chakra blue to gold to white-hot), the four-point star with the long upper ray, the two
  upswept wings. The final pose should read as the icon.
- **Reads at 50 px**: bold shapes, big value contrast, few large sparks rather than many tiny ones.
- Stays inside its square: nothing clipped at the frame edges; centered on the caster's hex.
- Real transparency on every frame (delivered on lime `#00FF00` or as transparent PNG), so it works over every battle biome.
  Glow must not leave dark halos.
- No fire or flame tongues, no figure or hands, no text or runes, no spiral or ring, no franchise looks (same exclusions as the icon).
- **Disappear animation (optional):** a short reverse dissolve (about 8-10 frames, beat 5 only) played when the buff ends;
  otherwise the cast animation is reused, as today.

**Deliverables:** every frame as its own square PNG (at least 256 px; 512 preferred), numbered in order, on lime or
transparent, plus a note of intended frame time. Claude Code keys, pads, scales to 128 px, stacks the strip, checks it with
`artpreflight.py --type ANIMATION`, and previews it at 50 px over dark, mid and bright backgrounds.

**Production routes (art director's choice):**
- **A. Keyframes plus layers (recommended):** paint the key poses (beats 1, 2, 3, 4) and separate layers (star, wings,
  spark set) on lime; Claude Code tweens and composites the in-between frames by script, as the prototype does but from
  real animation layers. Consistent frames, cheapest.
- **B. Video model:** generate a short clip from the icon, then extract and clean frames. Fast, but frame-to-frame
  consistency and transparency are hard.
- **C. Frame by frame:** every frame painted. Best quality, most work.

## 5. Delivery path (once the art exists)

1. **Create the asset:** a new `ANIMATION` game asset (name for example `chakra_overflow_rising_star`, frames, speed,
   image). Forge's `gameAsset` recipe creates assets directly; suggest mode refuses creates that other records reference.
   Alternatively the director uploads it in the asset editor, as with DemonCastleFloor.
2. **Point the jutsu at it:** a suggest-mode edit of Chakra Overflow that re-sends its live effects array with only the
   `visual` effect's `appearAnimation` (and `disappearAnimation`) changed, plus `injectableInBattle` (law 20).
3. **One open suggestion per record:** push/225 (icon and text) must be resolved first, or, if push/225 has not been run
   yet, it can be rebuilt to carry the animation too, so the jutsu changes in one review.
4. The six other jutsu keep the violet animation unless the director wants them looked at separately.
