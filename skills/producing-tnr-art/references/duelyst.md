# Battle animations from the Duelyst library

OpenDuelyst (a browser tactics game whose source and art were released CC0 1.0 in 2020) is the house library for
battle animations: about 208 effect sheets and 696 animated units, bold pixel art drawn for a tactics board, close
to TNR's board in scale and camera. Since 2026-11-16 most clips are composed from it by script (Rengoku Rō, Fury of
The White Tiger, Reefward Bastion, Phoenix Flame Strike, FCF v6) rather than painted. `combat_fx.md` owns the engine
facts and house rules; this file is how to use the library within them.

## 1. Setup

- `scripts/duelyst_kit.py fetch` once per machine: a sparse checkout of `open-duelyst/duelyst` at the pinned commit
  into `$TNR_DUELYST` (default `~/.cache/tnr-duelyst`, about 70 MB, outside the repository). The repository holds
  only `data/duelyst_catalog.json`; `catalog` regenerates it, only when the pin changes.
- Effects live in `app/resources/fx`, units in `app/resources/units`; timing per animation comes from the source
  (mostly 80 ms; some 40 ms bursts; slow idles up to 1 s; `"msFrom": "default"` marks the 32 with none).
- Songhai (`f2_`) is the ninja faction: gates, lotus, seals, smoke, wind. Abyssian (`f4_`) is shadow and void,
  Vetruvian (`f3_`) sand and water, Lyonar (`f1_`) holy light, Magmar (`f5_`) earth and beasts, Vanar (`f6_`) ice.

## 2. Find

- `find --kind fx --hue teal --shape tall`, `find --kind fx terms...`, `find --kind unit --action attack <name>`.
  Each row gives `sheet:prefix`, frames, ms, native px, hue and shape; a sheet with several animations needs the
  exact prefix.
- `sheet <refs...> --out c.gif` plays the candidates side by side, each through once; look at it before choosing.
- **Judge by eye, at board size.** Names lie: `spiritofthewild` is a wave of foam that reads as a flock of gulls at
  board size (rejected for Coral Maelstrom). A piece that reads as one shape at 40 CSS px beats a detailed one.
- Good fits so far: `fx_f4_obliterate` (prison of flame -> Rengoku Rō), `fx_f2_eightgates_teallotus` and
  `_purpleflame` (gate opening -> White Tiger, FCF v6), `fx_f2_saberspineseal` (seal and tiger), `fx_f3_fountainofyouth`
  (reef barrier), `fx_f2_phoenixfire` with `fx_f1_inmolation`'s flames (Phoenix Flame Strike),
  `fx_f2_mistdragonseal` (Aqua Dragon Barrage), `fx_tornadoswirl`, `fx_explosionblue` geysers
  (tile-sized, for areas).

## 3. Compose with a recipe

`scripts/fx_recipe.py build <recipe.json>` turns a recipe into one strip per clip, a real-board preview GIF and
`recipe.lock.json` (file, frames, speed, px, bytes, sha256, `licenseDetails`, rows cut) for the upload job. The
schema is in the script's docstring; `fx_recipe.py example` prints the White Tiger recipe, and
`data/fx_recipes/` holds the shipped ones. `--selftest` rebuilds White Tiger and checks it pixel for pixel against
the strips that went live.

```json
{"id": "tiger", "role": "target", "effect": "damage", "scale": 3, "ms": 80, "lead": 10,
 "layers": [{"sheet": "fx_f2_saberspineseal", "frames": "0-29",
             "recolour": [{"op": "gradient", "lo": 330, "hi": 90, "a": 200, "b": -0.6}],
             "anchor": {"row": 97, "at": "body"}, "factor": 1.4}]}
```

- **One clip = one asset.** `role` is where it plays (caster, target, field), `slot` which effect field (appear,
  loop, end), `effect` notes which tag carries it.
- **Anchor every layer** to the fighter (`combat_fx.md` section 2): pick the source row that should touch the feet
  (a ground ring, a pool, a pillar's base) or the body (a strike, a seal), and name it. Duelyst sheets sit low in
  their frames, centred on the unit's tile; never trust the frame centre.
- **`factor`** sets how much of the clip the art fills: the clip side is `factor` x the source frame. 1.2-1.5 for a
  scale-3 hero piece. The build reports rows cut where art leaves the square: a little off the top of a column is
  fine, a cut ring is not.
- **Trim and pace** with `frames`, `drop` (remove held frames: White Tiger dropped four from the column's hold),
  `reverse`, `hold` (show a source frame for several clip frames) and `start`. One clip has one clock (`ms`); keep
  the source timing unless the replay length matters (the replay cuts one action at 4 s).
- **Layer** pieces in one clip: later layers resample onto the first layer's canvas and can start later (a flash on
  top of a column, a ground ring under a strike).
- **Size** is automatic: native, an optional whole-number `upscale` for small sprites, then the 4096 px height rule
  (`combat_fx.md` section 4). Long clips come out smaller; trim frames before accepting a small size.

## 4. Recolour

| Op | Does | Use |
|---|---|---|
| `gradient` | hues in a range mapped linearly, `(a + b h) mod 360`, lightness and saturation kept | a whole element change with the drawing's own ramp: fire -> blue, teal, jade for White Tiger (`330-90`, `200 - 0.6 h`) |
| `hue_swap` | hues in a range moved to one hue | one part only: Reefward's gold ring -> coral (`330-100` -> 352) while the water stayed blue |
| `tint` | the luminance ramp recoloured dark -> colour -> white | flat, single-colour pieces (smoke, sparks) |

Duelyst palettes are faction-coded; a recolour is usually needed so a piece matches the jutsu's element and icon.
Recolour before scaling (the build does). For a ramp borrowed from another sheet (Phoenix's swirl matched to the
bird's own palette) write a custom script (section 6).

## 5. Areas, the caster and the target

- **Hero pieces and single targets** are where the library shines: scale 3, one per cast.
- **Area tags stamp one clip on up to 60 tiles in sync.** A Duelyst piece made for one unit, repeated on every tile,
  turns into a field of identical clusters (the FCF `shadowcreep` trial). For fields use a tile-sized piece that
  reads as texture (`explosionblue` geysers, recoloured) or our own tessellating art (FCF v5's crack field), with the
  library piece as the hero on the caster feeding it (FCF v6). Preview the field on all 60 tiles before deciding.
- **Caster plus target:** the caster's clip tells the wind-up and launch; the target's clip opens with `lead` blank
  frames for the travel, then lands (`combat_fx.md` rule 11). Check both together on the board preview.
- **Buffs:** cast-only, no loop (RUL-2026-11-17-166).

## 6. When a recipe is not enough

Write a per-jutsu script under `art/duelyst_fx/<slug>/` that imports `duelyst_kit` (and `fx_recipe` helpers) for:
drawn frames between library pieces (Phoenix Flame Strike's swirl coiling into the bird, `art/duelyst_fx/showcase/
build_phoenix_caster.py`), a palette borrowed from another sheet, a library piece layered over our own art (FCF v6,
`art/jutsu_icons/forbidden_chakra_fury/animation/build_v6_duelyst.py`), or a ring hold cut and re-timed (Rengoku Rō,
`art/duelyst_fx/rengoku/build_rengoku.py`). Keep the same geometry names and the 4096 px rule, and make a board
preview the same way.

## 7. Provenance and units

- `licenseDetails`: "CC0 1.0 - OpenDuelyst (open-duelyst/duelyst), <sheet> [/ <sheet>], adapted for TNR" (the lock
  file writes it). CC0 needs no credit; we credit anyway, and staff threads say "adapted from OpenDuelyst's effects
  library (CC0, free to use)".
- Unit sprites (idle, run, attack, hit, death, cast) could become AI sprite sheets through the in-game Sprite Studio
  library (`spriteAnimation.create`, no credits). That is an art-direction change for AI characters and needs the
  director's call and its own sheet-layout check; it is not part of this pipeline.
