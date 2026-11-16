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
  art with **no balance change**. Untested in our content: prove it on a hidden record first.

## 2. Geometry (draw for this, not for a square tile)

- Hexes are flat and squashed 2:1: tile box `w x h` with `h = 0.5 w`.
- A clip is `h x scale` square: at 1 it is **half a tile wide**; at 3 it is 1.5 tile widths. Spiral and area jutsu
  only merge into one picture at about 3; at 1.75 they read as separate columns.
- Inside a clip frame of side `S` at scale `k`, the tile is `(2S/k) x (S/k)`, centred: at k = 3 the ground image sits
  at `(2/3 S) x (1/3 S)`; below k = 2 the tile is wider than the frame. Anything meant to line up with the ground image (cracks that shimmer) must be drawn in
  that box (`scripts/fx_board.py ground-box`).
- Ground images are stretched to the 2:1 box: paint them wide, or crop to the painted footprint at its own aspect.
  Square art gets squashed.
- Anything flat on the floor (ripples, rings, marks) is painted from straight above and squashed 2:1 by the script.
- Clips draw over fighters, portraits and HP bars; ground images draw under them. Character clips sit best with their
  visual centre about 15% above the frame centre.

## 3. Delivery and sharpness

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

## 4. Gotchas that cost a live fix

1. **Appears overdraw 2-3x.** A persistent effect's appear plays from the client record and again as a server
   `visual`; on an occupied tile a third time. Keep appears light or design for the stack.
2. **A ground tag's `disappearAnimation` repeats on anyone standing in it**: every effect pass spawns it on the
   occupant (engine doc 5.3). On tiles enemies stand in, keep the end clip subtle or leave it empty.
3. **`decrease*` tags on characters are invisible** (power goes negative = "depleted": no appear, loop or ground
   art). Put the art on a visible carrier tag in the same cast.
4. **Hidden assets never render, with no error.** Create hidden (law 16b), then unhide every battle asset by edit.
5. "1-round" effects stay through the next round. No timeline: everything new in one update starts at once.
6. First use in a battle lags one asset fetch. The killing blow is never animated.
7. Edits to a jutsu equipped on an AI: law 18 (unequip, edit, re-equip). Player jutsu: not needed.

## 5. Production pipeline

1. **Read the record** (connector `jutsu.getAll {name}` / `jutsu.get` with `select` of the effect fields; `gameAsset.get`
   for current clips). Note targeting, method, effects, current clips and whether an AI equips it.
2. **Brief** in `docs/handoffs/<NAME>_ANIMATION_ART_REQUEST.md`: the record, where the art plays and why that tag
   carries it, concept, palette from the icon, per-clip beats with frames x ms, scale, deliverables, checks, and the
   live edit (art fields only). Give the director a copy-ready prompt for the art partner.
3. **Painted sources, not finished strips.** Ask for key poses or layers on a 1254 px transparent canvas (hero pose,
   ground image, overlays, flat-on floor layers). Generators cannot paint consistent frame sequences.
4. **Assemble by script** under `art/jutsu_icons/<name>/animation/` (examples: `forbidden_chakra_fury/animation/
   build_strips.py`, `chakra_overflow/animation/build_strip.py`, `art/mother_of_echoes_fx/`, Headless Rider
   `art/halloween_headless_rider/fx/fxkit.py`). Animate one drawing on continuous curves; cross-fading separate
   drawings makes shapes jump. Dissolve, never a grey fade.
5. **Board preview, always**: `python3 scripts/fx_board.py board --appear A.webp --loop L.webp --end E.webp --ground
   G.webp --scale 3 --out preview.gif` draws the real board (2:1 hexes, the spiral patch, every tile at once). A square
   tile preview lies about size: it has cost one wrong scale already.
6. **Live** (director go per job): Forge creates each asset hidden, a follow-up edit unhides them, then one full-record
   `jutsu.update` changes only the art fields and `animationScale`; read back. Fresh filenames for corrections.

## 6. What the director decides

Art direction, palette, scale, whether a stock clip is cleared, and acceptance. Never a balance change to get art onto
the board: use the existing tag or a `visual` tag.
