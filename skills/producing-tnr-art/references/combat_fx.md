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
- Clips draw over fighters, portraits and HP bars; ground images draw under them.
- **Where the fighter stands inside a clip** (game source `combatActors.ts`, `combatEffects.ts`): the clip square and
  the ground image are centred on the hex centre; a fighter's feet are 0.1-0.15 tile heights above the hex's bottom
  edge. In clip terms, with `h` the tile height: **feet 0.4 h below the clip centre, body centre about 0.4 h above
  it, head about 1.2 h above it.** At scale 3 the clip spans 1.5 h above and below its centre, so art can rise at
  most 1.9 h above the feet before the square crops it (FCF v6's pillar). A ring "on the feet" sits 0.4 h below the
  centre, not at it (Rengoku Rō's first previews put the figure wrong and the ring had to move). `fx_recipe.py`
  anchors layers with these names (`feet`, `body`, `top`) and its board preview draws stand-in fighters to match.

## 3. Design rules (house style)

These hold however the clip is made; `references/duelyst.md` is how most clips are made now.

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
9. **One visual tag, one caster clip.** At most one `visual` tag per jutsu (RUL-2026-11-16-165), and one clip per
   cast on the caster: two SELF tags with appears play on top of each other (White Tiger kept the gates on the buff
   and cleared the afterburn's clip).
10. **Buffs are cast-only** (RUL-2026-11-17-166): no lingering `staticAnimation` on a buff or self tag; "there's so
    many buffs in TNR it would be a mess if they all stayed". Play the art once at cast and clear any stock loop.
11. **Tell travel with timing, not movement.** A clip stays on its own hex, and every clip of one action starts at
    the strike. A projectile or creature "flies" when the caster's clip ends in a launch and the target's clip opens
    with blank lead frames that cover the flight (White Tiger's tiger waits 10 x 80 ms for the gates to open;
    Phoenix Flame Strike's target strip waits 17 frames while the bird leaves the caster).

## 4. Delivery and sharpness

- Sheets: **one vertical strip, one column, square frames**, top to bottom. `frames` 1-100, `speed` 1-100 ms/frame.
  1-2 px transparent margin top and bottom of each frame helps where linear sampling bleeds between frames.
- Lossless WebP, real transparency (normal alpha blending; a dark background shows as a box), under the
  `ANIMATION` byte ceiling in `25x_DATA_art_spec.json`.
- **The host decides what the battle loads** (`src/utils/image.ts`, `assets.ts`):

| Host | Battle loads | Consequence |
|---|---|---|
| Bunny-routed (`utfs.io`, `ui0arpl8sm.ufs.sh`, the legacy Forge image-pack route) | the strip resized to **50 px wide**, linear filtering | detail finer than 1/50 of a frame is lost, then upscaled: bold shapes and glow, not hairlines (`processing.md` laws 79, 84) |
| The director's own UploadThing (`bbenpyo9uu.ufs.sh`) and any other host | the strip **at native size** | sharp at any size, but see the height rule |

- **Height rule: frame px x frames <= 4096.** A battle clip is one WebGL texture (one column) and combat effects have
  no texture-size guard; phones cap textures at about 4096 px, so a taller native strip draws as a **black box**
  (Rengoku Rō's 300 px strips, 6900 and 10500 px tall, on the review desk 2026-11-17; fixed by re-cutting to 178 and
  116 px, push/630). Desktops allow 16384, so a desktop check does not catch it. `fx_recipe.py` and
  `duelyst_kit.py strip` size every strip to fit and refuse one that does not; apply it to Bunny-hosted art too, in
  case it is moved to a native host later.
- Size from frame count: 4096 // frames (29 frames -> 140 px, 40 -> 102). A clip at scale 3 shows about 111 CSS px
  tall at desktop 1x (37 px tiles), so 100-140 px source is enough; content lists show 112 px. Trim frames before
  shrinking pixels when a clip runs long.
- Before trusting fine detail, upload one test strip hidden and look at it in a real browser battle, on a phone.

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

1. **Read the record** (connector `jutsu.get` with `select` of the effect fields; `gameAsset.get` for current clips).
   Note targeting, method, every effect tag and its current clips, the battle text, and whether an AI equips it. Save
   the read under `state/<slug>/`.
2. **Plan against section 3:** which tag carries the hero piece (caster or single target, scale 3), which carries
   the applied piece (area tag, scale 2, tessellating), what is cleared (stock clips, buff loops), how the timing tells
   the story across clips.
3. **Build from the library first** (`references/duelyst.md`): `duelyst_kit.py find`/`sheet` to pick pieces by eye,
   then a recipe for `fx_recipe.py build` (strips, board preview, lock file). A custom script that imports the kit is
   for what a recipe cannot say (Phoenix Flame Strike's drawn birth frames, FCF v6's pillar over our own field).
4. **Paint only when nothing fits** (ground images, tessellating area fields, a subject the library lacks). Brief in
   `docs/handoffs/<NAME>_ANIMATION_ART_REQUEST.md` with a copy-ready prompt for the art partner; ask for key poses or
   layers on a 1254 px transparent canvas, never frame sheets, and assemble by script under
   `art/jutsu_icons/<name>/animation/` (examples: `forbidden_chakra_fury/animation/build_v5.py`,
   `art/mother_of_echoes_fx/`). Animate one drawing on continuous curves; dissolve, never a grey fade.
5. **Board preview, always**, at true scale with fighters where the engine puts them: `fx_recipe.py build` writes one;
   for finished strips use `fx_board.py board --appear A.webp --loop L.webp --end E.webp --ground G.webp --scale 3`.
   Show the director the preview (a Discord-ready GIF for staff review when asked) and wait for approval.
6. **Upload job** (`building-tnr-content` push pattern, e.g. push/627-629): hidden asset creates from the lock file
   (filename, frames, speed, `licenseDetails`), an unhide by literal id from the results bundle, then the jutsu edit:
   art fields and `animationScale` only, the full effects array re-sent, as a suggestion ticket (category ANIMATION)
   or a direct edit on the director's go. Law 18 when an AI equips it. Fresh filenames for corrections.

## 7. What the director decides

Art direction (including which library piece and recolour), palette, scale, whether a stock clip is cleared, and
acceptance. Never a balance change to get art onto the board: use the existing tag or the one `visual` tag.
