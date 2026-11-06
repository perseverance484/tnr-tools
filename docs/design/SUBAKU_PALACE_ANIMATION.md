# Subaku Palace: the domain summoning (design, assets, engine limits)

Status: design and built strips, 2026-11-05. **No manifest yet.** Jutsu `jELEiw5W3N4m2R3oJm3Pk` (player EVENT, A rank,
JONIN, level 25, 40 AP, cooldown 7, 500 chakra and 500 stamina; AOE_SPIRAL_SHOOT, target GROUND, range 4).
Mechanics are unchanged: SELF `increasedamagegiven` 30 % for 2 rounds; GROUND `decreasedamagegiven` 15 % on ENEMIES for
3 rounds.

Rulings: RUL-2026-11-05-124 (payoffs as one picture, the stage, no sickly green, premium) and RUL-2026-11-05-125
(the remake; the exact-geometry tile ships; up to 7 visual-tag lines in the jutsu details). Text of record:
`docs/design/jutsu_overhaul/EVENT_JUTSU_STORY_TEXT.md`. Shared clock and palette: `art/subaku_palace/TIMING.md`.
Centre half (sigil, gates, palace): `art/subaku_palace/gates/README.md`.

Live-game requests: 0. Game source read at theninjarpg `3314d122` and upstream main `cb755375`; never run.

## 1. What the player sees

Build target (director, 2026-11-05): 2.5-hex-height clips and LPC character avatars.

1. **Anticipation (ticks 0-6).** The domain's 60 hexes darken under a shadow veil, and the floor shows faint through
   it. At the caster's feet the burning-gold sigil kindles and spirals out (centre strip).
2. **The spread (7-16).** Ring by ring, in seven half-ring bands, the veil lifts and a current of burning gold runs
   out along the floor's gold channels. It has a white-hot head and a burning tail. The cracks flare ember a tick
   behind it. The current runs past each hex's edge into the next ring at the speed the rings land, so the light
   crosses every seam as one continuous current racing out to the rim.
3. **The gates (7-19).** Red sandstone oni gates tear out of the ground on ring 1, and the palace with its moon gate
   rises behind the caster (centre strip).
4. **The held beat (20-21).** The rim has landed. One breath of light runs through every channel of the domain at
   once (the seal), and the palace stands, white-hot for one tick.
5. **The settle (22-37).** The gates sink, the currents cool, and the frame ends on the floor's look.
6. **The 3 rounds.** A static floor of dark warm basalt flagstones with ember-glowing joints. Bold, bevelled
   currents of burnished demon gold sweep across it (director 2026-11-05: bolder and sparser, toward his original
   tile). There is one current per hex, swelling mid-hex and lit from the upper left. They join hex to hex into long
   diagonal currents 1.5 hex radii apart, with broad dark stone between. Each current throws one bold spiral curl
   into the stone. There are no corner arcs, which read as fish scale at 50 px. Every join at an edge midpoint is
   exact, so the floor reads as one surface. It lies under the fighters, with no loop.
   The caster's own hex stays empty after the cast (director 2026-11-05: it has no in-game effect either).
7. **The self-buff.** The gates and palace are the master's moment. Per the director, the sigil is symbolic and
   fades in the cast: there is no lingering buff loop and no dais.

**Light and dark boards.** The domain is a dark field (stone mean about `#30292a`), so its edge reads hard on snow and
by its gold on night boards. The rest gold is burnished (`#603a0e` to `#f0cc7c`, bevelled). The cast's burning current
(`#ffcf4a` to `#fff4c8`, white-hot head) is brighter still, and it runs along the engraved channel at each band's centre.
**Alongside other effects.** The floor is static art: it draws under fighters, highlights and every other clip, and
it carries no loop. Peak clip coverage of the arena during the cast is 43 % (mean 17 %). The largest share of any enemy's avatar
box under an opaque clip pixel is 32 %, for under one second, as the veil passes. The centre strip (v4) covers the
caster's LPC body envelope 0 % and the lower neighbour's meter rows 0 % on every frame (build-gated); its arch and
palace eave cross the caster's own meter rows (shown only on hover or selection) during ticks 15-24. Measured on the true-scale composite, both column parities.

## 2. Engine reality (what made the design)

| Fact | Source |
|---|---|
| AOE_SPIRAL_SHOOT covers spiral(caster, range) minus the caster's own hex: 60 hexes, all in one action. There is a **hole** under the caster. | `libs/combat/targeting.ts:56-58` |
| Every record of the cast starts on the same tick. A ring order must be baked into separate strips. | engine doc 0.1, 2.3 |
| There is **no per-tag delay** anywhere in the combat code. Static art is drawn from the record's first ready frame for its whole life. **The floor cannot arrive late.** | `libs/combat` at 3314d122 and cb755375: the only `delay` is the encounter round delay (`encounters.ts:14`), unrelated to tags; `scenes/combatEffects.ts:139-160` |
| A ground tag's appear plays x2 (client record + server visual). The occupant copy of a damage modifier skips applySingleEffect, so there is no third. | `libs/combat/process.ts:432-442`, `:657-739` |
| Visual tags (COORDINATES) are stamped only on their own offsets, x1, with no occupant copy, and are dropped at the first action of round N+1 (fine for one-shots). | `actions.ts:1063-1112`; `routers/combat.ts:851-860`; RUL-2026-11-02-101 |
| COORDINATES offsets are col/row. On one caster parity, odd columns sit half a row off. | `targeting.ts:59-75` |
| Visual tags are listed in the player-facing jutsu details. | `layout/ItemWithEffects.tsx:1297` |
| Static art fills the hex box (2:1) at any clip ratio. Clips are ratio x h square, 50 px rendition, linear, drawn over fighters. | `combatEffects.ts:126-150`; `sprites.ts:263-268` |

**What follows.**
- The floor is present from tick 0, so "summoned" is drawn by clips: a veil per hex that lifts with its ring, plus the
  current.
- A unique painted swirl across the domain is not possible. Every hex in one tag shows identical pixels, so a
  non-repeating picture would need one tag per hex (56-60). The parity shift also tears exact slices.
- The field is therefore one lattice-periodic surface (the tile), and the spread is carried by 7 timing groups. The
  clips sample the same periodic field past their own hex, so their light lands on exactly the floor's pixels on
  either parity.

**Parity error (every caster column).**
- Bands use each offset's mean hex distance over the two parities.
- On both parities, 40 of the 56 band hexes land exactly on their true ring, and 16 land half a ring early or late
  (about 75 ms).
- 4 rim hexes per parity are in the domain on one parity only, so they carry no band tag. They are the top four rim
  hexes on an even column and the bottom four on an odd one. They get no veil and only the seal breath.

## 3. Assets (built, `art/subaku_palace/exports/`, artpreflight 0 errors / 0 warnings)

| Asset | Type | Frames x ms | Slot (proposed) |
|---|---|---|---|
| `tile_sbk_domain_v3.webp` (150 px) | STATIC | 1 | ground `decreasedamagegiven`: `staticAssetPath` (replaces DemonCastleFloor `zEvI0yd_As_FzNyrr5Iq4`) |
| `anim_sbk_seal_v1.webp` | ANIMATION | 32 x 50 | ground `decreasedamagegiven`: `appearAnimation` (replaces the library clip `c4FqDZWFZOdWn86o6nPL7`) |
| `anim_sbk_wave_b0_v1` … `b6_v1.webp` | ANIMATION | 32 x 50 each | 7 new visual tags: COORDINATES, origin CASTER, the offsets in `subaku_domain_v1.json`, power 2, rounds 1, `appearAnimation` |
| `gates/exports/anim_sbk_gates_rise_v4.webp` (centre half; v2 superseded after QA) | ANIMATION | 38 x 50 | SELF `increasedamagegiven`: `appearAnimation` |

Builders (Pillow only): `floor.py` (the periodic field and the tile), `build_domain.py` (strips and offsets),
`preview.py` (the true-scale composite). It imports the Mother of Echoes `qa_preview.py` read-only. Exploration patterns
(palace lattice, swirl, streams; the superseded thin 'flow' is in git history at 5f2c6a07) are in `tile_v2.py`. The director's four reference tiles are in `refs/`. Ref a
(`677f13a9`) is taken as the live DemonCastleFloor because it is the only one that fills the 2:1 box. No hash is
captured for the live asset, and fetching it would be a live request. Provenance and preflight: `_provenance/`.

**Sound (director 2026-11-05).** Remove the ground tag's `appearSfx` Heal (`4iG_WpgEmPGUzHn8z129r`). It plays
once per new record, about 120 times per cast. Put Earth (`XBlRonNjvwAZx1_HFpHdM`) as `appearSfx` on band tag b0 only
(ring 1: 4 records on the same tick).

## 4. Mechanics: unchanged (director 2026-11-05)

No mechanic change. The caster's hole stays empty after the cast. Enemies standing in the palace deal 15 % less for
3 rounds; the master deals 30 % more for 2.

## 5. Ratio-1 note (338126cb; the director expects it reverted)

At `EFFECT_ANIMATION_HEX_RATIO = 1` a clip is h x h: it covers the hex's central rectangle and never the wing triangles
where columns meet. Lit currents break at every column seam, a veil would draw dark boxes, and painted slices cannot
tile. The static floor still fills the hex. `SBK_RATIO=1 python3 build_domain.py` builds strips for that geometry: no
veil, currents faded at the clip sides. The gates agent's `anim_sbk_gates_rise_v3` (`gates/build_gates_ratio1.py`) is the ratio-1 centre.

## 6. Previews (true scale: 132 x 66 hex, 165 px clip, 50 px rendition, linear; LPC stand-in, labelled)

Contact sheets in `docs/design/subaku_palace/`. The GIFs (arena 12 x 10 and close-up, light and dark, even and odd
caster columns) are regenerated by `preview.py [--odd]`. The board is the real battle still tiled by its own hex
period. The dark board is the harness's night grade.

## 7. Raw art

None is needed: the tile and strips are delivered at the 50 px rendition, where the programmatic finish holds.
An optional painted finish for the stone and the gold is in `docs/handoffs/SUBAKU_PALACE_FLOOR_ART_REQUEST.md`.
