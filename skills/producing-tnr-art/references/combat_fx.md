# Combat animations and ground tiles

Battle art on jutsu, item and AI effects: the clips that play on the board and the flat images left on tiles. Facts
are from the game source; `docs/design/COMBAT_ANIMATION_ENGINE.md` (pin `3314d122`) is the long-form analysis with
line citations, and the size rule below supersedes its fixed 2.5 (upstream `8bd670153`, re-checked at `f6a51fac5`).

## 1. The model: four slots per effect

| Slot | Field | Plays | Size |
|---|---|---|---|
| Appear | `appearAnimation` (ANIMATION asset) | once at cast | square, `tile.height x animationScale` |
| Loop | `staticAnimation` (ANIMATION) | loops while the effect lasts (rounds > 0) | same square, drawn over the appear |
| End | `disappearAnimation` (ANIMATION) | once when it ends, server-spawned as a `visual` | same square |
| Ground image | `staticAssetPath` (STATIC asset) | flat under the tile while the effect lasts | the tile box, `tile.width x tile.height` |

- `animationScale` 1-3 per effect, **one value shared by its three clips** (validator `min(1).max(3)`, default 1).
- **Where it plays is decided by targeting, not art.** A Ground/INHERIT jutsu puts every effect on every tile of its
  pattern (`actions.ts` ~1100); `target: SELF` tags play on the caster. A Ground jutsu with no SELF tag has no clip on
  the caster: carry the art on a tag that lands on the tiles (Forbidden Chakra Fury: the recoil tag).
- `visual` is an authorable tag type with no mechanics, a ground tag like barrier and summon. It is how a jutsu gets
  art with **no balance change**. Untested in our content: prove it on a hidden record first. **At most one visual
  tag per jutsu** (RUL-2026-11-16-165): every tag is listed on the jutsu's stats and database screens, and a mosaic
  of visual tags (Dragon King's Impact, about 12) made the stats unreadable. The one allowed tag is for the hero
  piece (section 3), e.g. `target: COORDINATES`, `origin: CASTER`, offset `0,0`, rounds 0.

## 2. Geometry (draw for this, not for a square tile)

- Hexes are flat and squashed 2:1: tile box `w x h` with `h = 0.5 w`.
- A clip is `h x scale` square: at 1 it is **half a tile wide**, at **2 exactly one tile wide**, at 3 it is 1.5 tile
  widths. On area jutsu every tile plays the same clip at once, so a clip wider than its tile overdraws its
  neighbours: use 2 and make the art tessellate (section 3), not 3.
- Inside a clip frame of side `S` at scale `k`, the tile is `(2S/k) x (S/k)`, centred: at k = 3 the ground image sits
  at `(2/3 S) x (1/3 S)`; below k = 2 the tile is wider than the frame. Anything meant to line up with the ground image (cracks that shimmer) must be drawn in
  that box (`scripts/fx_board.py ground-box`).
- Ground images are stretched to the 2:1 box: paint them wide, or crop to the painted footprint at its own aspect.
  Square art gets squashed. Gate them with `fx_board.py ground-check` (wide aspect, real alpha, soft edges, lossless
  WebP, byte ceiling), not `artpreflight.py --type STATIC`: the spec's STATIC target is square circle-masked map-pin
  art and refuses a wide ground image on aspect.
- Anything flat on the floor (ripples, rings, marks) is painted from straight above and squashed 2:1 by the script.
- Clips draw over fighters, portraits and HP bars; ground images draw under them. Character clips sit best with their
  visual centre about 15% above the frame centre.

## 3. Design rules (house style)

From shipped 2D grid-tactics games, mainly OpenDuelyst (a browser tactics game whose whole effects library is CC0,
`github.com/open-duelyst/duelyst`, `app/data/fx.js` and `app/resources/fx/`), and VFX timing practice. They exist
because our early clips were inconsistent and one area jutsu (FCF v4) turned into mush on the board.

1. **Hero piece once, applied piece per tile.** Duelyst gives every spell a `SpellCastFX` (one big effect at the
   cast point, 2-3 tiles) and a `SpellAppliedFX` (one to three small sprites on each target, about one tile, often
   just 8-13 frames). Here the hero is the caster's tag or the single-target tag (scale 3); the applied piece is the
   area tag (scale 2 or less, short, quiet). One focal point; never a hero-sized clip on every tile.
2. **Design for repetition.** An area tag stamps one clip on up to 60 tiles in sync (spiral range 4). Make it
   tessellate: anything that reaches a tile edge leaves through a **hex edge midpoint** along the centre-to-midpoint
   line, so neighbours join into one picture (FCF v5: one through-cut per tile chains into long slashes; six spokes
   per tile read as chain-link). Sparse per tile, mixed sizes (one big, one medium, one small mark); round bursts per
   tile always read as a pattern. A wave rippling out from the caster is impossible on one tag.
3. **Three beats, compressed.** Anticipation (dark or gathering, short), climax (the most contrast and elements, held
   2-3 frames), dissipation (dissolve, embers, smoke: never a plain alpha fade). When a hero and an area piece play
   together, give the area piece a dark lead-in while the hero gathers, so the hero visibly feeds the field.
4. **Hold frames; default 80 ms.** About 80% of Duelyst's effect sheets run at 80 ms per frame (12.5 fps), most of
   the rest at 90-160 ms. Default 70-80 ms with fewer, stronger drawings; go under 50 ms only for a deliberate smear
   or flash, a frame or two.
5. **Author for the display size.** A hex is about 39 CSS px wide on a 360 px phone board, so a scale-2 clip shows
   at about 40 px. Lines under 2 CSS px and painterly texture vanish; use bold, angular shapes (sharp reads fast and
   violent, soft reads slow), strong value contrast against the dark board, and check the board preview at phone
   size (`--shrink`).
6. **Bake layers into the strip.** Duelyst builds most effects from a few layers: a flat ground layer at the feet
   (`fxSmokeGround`, 80 x 25), a vertical layer (a strike or blast rising or falling), and a core flash, often reused
   with a tint, flip or rotation. We have one strip per slot, so composite those layers in the build script, and reuse
   one primitive (slash, crack, eruption, ring, smoke, sparks) across jutsu, tinted per element, so the game's effects
   look like one family.
7. **Budget the engine.** The loop and the ground image start at the strike, under or over the appear: give the loop
   a quiet first phase as long as the appear (it recurs each cycle as a breathing rhythm), and keep the ground image
   dark enough to read as a marked floor before the cut. Remember the appear overdraw and the end clip on occupants
   (section 5).
8. **Clear the stock clip** on other tags of the same jutsu when it would play on every tile over the new art (an
   art-only change; the director decides).

## 4. Delivery and sharpness

- Sheets: **one vertical strip, one column, square frames**, top to bottom. `frames` 1-100, `speed` 1-100 ms/frame.
  Keep strips at or under about 80 frames (mobile 4096 px texture limit). 1-2 px transparent margin top and bottom of
  each frame (linear sampling bleeds between frames).
- Lossless WebP, real transparency (normal alpha blending; a dark background shows as a box), under the
  `ANIMATION` byte ceiling in `25x_DATA_art_spec.json`. Frames at least 128 px (content lists show 112).
- **Battles fetch a 50 px-wide rendition with linear filtering** on Bunny-routed hosts (UploadThing, `utfs.io`,
  `ui0arpl8sm.ufs.sh`): the whole strip is resized to 50 px wide, so detail finer than 1/50 of a frame is lost and
  then upscaled (`processing.md` laws 79, 84). Other hosts load native. At scale 3 on desktop that is a large
  upscale: design bold shapes and glow, not hairlines. Before trusting fine detail, upload one test strip hidden and
  look at it in a real browser battle.

## 5. Gotchas that cost a live fix

1. **Appears overdraw 2-3x.** A persistent effect's appear plays from the client record and again as a server
   `visual`; on an occupied tile a third time. Keep appears light or design for the stack.
2. **A ground tag's `disappearAnimation` repeats on anyone standing in it**: every effect pass spawns it on the
   occupant (engine doc 5.3). On tiles enemies stand in, keep the end clip subtle or leave it empty.
3. **`decrease*` tags on characters are invisible** (power goes negative = "depleted": no appear, loop or ground
   art). Put the art on a visible carrier tag in the same cast.
4. **Hidden assets never render, with no error.** Create hidden (law 16b), then unhide every battle asset by edit.
5. "1-round" effects stay through the next round.
6. **Playback (game source `f6a51fac5`, `combatPlayback.ts`):** the actions in one update replay **in order, one at a
   time**. Each actor winds up (capped at about 550 ms), its strike lands, the hit holds about 120 ms, then the next
   action starts; one action is cut off after 4 s; past 8 queued actions the oldest are skipped. Everything one action
   creates starts together at its strike, appear and loop on the same clock with the loop drawn on top, so design the
   appear to read under the loop's first frames. The final action plays before the result screen (`Combat.tsx` holds
   the result), so a killing blow is animated. First use in a battle still lags one asset fetch.
7. Edits to a jutsu equipped on an AI: law 18 (unequip, edit, re-equip). Player jutsu: not needed.

## 6. Production pipeline

1. **Plan against section 3** (hero vs applied piece, tessellation, timing) before briefing the art partner.
2. **Read the record** (connector `jutsu.getAll {name}` / `jutsu.get` with `select` of the effect fields; `gameAsset.get`
   for current clips). Note targeting, method, effects, current clips and whether an AI equips it.
3. **Brief** in `docs/handoffs/<NAME>_ANIMATION_ART_REQUEST.md`: the record, where the art plays and why that tag
   carries it, concept, palette from the icon, per-clip beats with frames x ms, scale, deliverables, checks, and the
   live edit (art fields only). Give the director a copy-ready prompt for the art partner.
4. **Painted sources, not finished strips.** Ask for key poses or layers on a 1254 px transparent canvas (hero pose,
   ground image, overlays, flat-on floor layers). Generators cannot paint consistent frame sequences.
5. **Assemble by script** under `art/jutsu_icons/<name>/animation/` (examples: `forbidden_chakra_fury/animation/
   build_strips.py`, `chakra_overflow/animation/build_strip.py`, `art/mother_of_echoes_fx/`, Headless Rider
   `art/halloween_headless_rider/fx/fxkit.py`). Animate one drawing on continuous curves; cross-fading separate
   drawings makes shapes jump. Dissolve, never a grey fade.
6. **Board preview, always**: `python3 scripts/fx_board.py board --appear A.webp --loop L.webp --end E.webp --ground
   G.webp --scale 3 --out preview.gif` draws the real board (2:1 hexes, the spiral patch, every tile at once) with the
   appear and loop composited on one clock, loop on top, as the engine does. A square tile preview lies about size: it
   has cost one wrong scale already. Gate ground images with `fx_board.py ground-check G.webp`.
7. **Live** (director go per job): Forge creates each asset hidden, a follow-up edit unhides them, then one full-record
   `jutsu.update` changes only the art fields and `animationScale`; read back. Fresh filenames for corrections.

## 7. What the director decides

Art direction, palette, scale, whether a stock clip is cleared, and acceptance. Never a balance change to get art onto
the board: use the existing tag or a `visual` tag.

## 7. Duelyst library (CC0)

OpenDuelyst (a browser tactics game whose source and art were released CC0 1.0 in 2020) is our stock library:
about 208 effect sheets and 696 animated units (idle, run, attack, hit, death, breathing, cast), bold pixel art.
Timing is per animation from the source (mostly 80 ms; some 40 ms bursts, slower idles up to 1 s); a sequence with no
source timing is marked `"msFrom": "default"` (80 ms). `scripts/duelyst_kit.py` reads it from a cache outside the repository (`$TNR_DUELYST`, default
`~/.cache/tnr-duelyst`, pinned commit); the repository holds only `data/duelyst_catalog.json`.

1. `duelyst_kit.py fetch` once per machine, then `catalog` only if the pin changes.
2. **Find:** `find --kind fx --hue teal --shape tall`, `find --kind unit --action attack serpent`, or name terms;
   `sheet ... --out c.gif` plays the matches side by side, each through once. A `sheet:prefix` name must be an
   exact animation prefix (`find` prints them). Judge by eye: names lie (`spiritofthewild` is a wave of
   foam that reads as a flock of gulls at board size; the director rejected it for Coral Maelstrom).
3. **Fit:** build a per-jutsu script (precedent: `art/duelyst_fx/rengoku/build_rengoku.py`,
   `art/duelyst_fx/thalmyr/build_reefward.py`) that imports the kit: anchor the art to the target's feet (Duelyst
   sheets sit low in their frame), recolour (`tint` for a whole ramp, `hue_swap` for one part: the gold ring of
   `fountainofyouth` became coral while the water stayed blue), trim or reorder frames, keep the source timing
   unless the replay length matters (Rengoku's ring hold was cut to 1.6 s), and export whole-step NEAREST.
   **Frame size x frames must stay at or under 4096 px**: art on a native host (the director's UploadThing) loads
   full size, and phones draw a taller strip as a black box (Rengoku Rō's 300 px strips, 2026-11-17). `strip` and
   `write_strip` refuse taller strips and print the largest size that fits.
4. **Preview** on the real board at true scale before anything is uploaded; check a dark lead-in for loops that
   start with the strike (section 4).
5. **Provenance:** `licenseDetails` names "CC0 1.0 - OpenDuelyst (open-duelyst/duelyst), <sheet>, adapted for TNR".

Area tags still follow the repetition rule: a Duelyst piece made for one unit, stamped on every tile of a spiral,
turns into a field of identical clusters (FCF trial with `shadowcreep`). Hero pieces and per-target clips are where
the library shines; area fields use tile-sized pieces (`explosionblue` geysers) or our own tessellating art.
Units' body animations can become AI sprite sheets through the Sprite Studio library (`spriteAnimation.create`,
no credits); that path needs its own sheet-layout check before use.
