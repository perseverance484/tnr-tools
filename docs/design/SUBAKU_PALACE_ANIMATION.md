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

1. **Anticipation (ticks 0-6).** The domain lies as empty dark stone. Each band hex is covered by its own floor with
   the gold rails engraved but unlit (the director's arrival, 2026-11-05). At the caster's feet the burning-gold
   sigil kindles and spirals out (centre strip).
2. **The spread (7-19).** Ring by ring, in seven half-ring bands, the gold forms in each hex: from the hex centre
   outward over three ticks, a white-hot head runs along the rails with a burning trail, and the cracks flare ember
   behind it. On the fourth tick the hex shows the finished floor, and an ordered dissolve over three ticks hands it
   to the real tile underneath. The bands land 1-2 ticks apart, so the gold steps outward ring by ring.
3. **The gates (7-19).** Red sandstone oni gates tear out of the ground on ring 1, and the palace with its moon gate
   rises behind the caster (centre strip).
4. **The held beat (19-21).** The rim has formed. Every rail face in the domain burns solid at once, the channels
   white-hot on tick 20 (the seal), and the palace stands.
5. **The settle (22-37).** The gates sink, the currents cool, and the frame ends on the floor's look.
6. **The 3 rounds.** A static floor in the director's reference style (refs a-d). Dark basalt flagstones with a
   fine grain and their own tones, faint red light in the mortar, and whole joints glowing ember that taper out at the
   stone corners. Over them runs a woven lattice of crisp double-rail demon gold: one gentle S current per hex, from
   the lower-left to the upper-right edge midpoint, weaving over two large arcs (M1-M3 and M0-M4). Hex to hex the
   currents run at 150 deg and the arcs chain at 60 deg across them, so the gold reads as one woven surface, not
   parallel stripes. It has no curls. Every band leaves its hex at an edge midpoint with the same width and a
   symmetric profile, so every join is exact. It lies under the fighters, with no loop.
   The caster's own hex stays empty after the cast (director 2026-11-05: it has no in-game effect either).
7. **The self-buff.** The gates and palace are the master's moment. Per the director, the sigil is symbolic and
   fades in the cast: there is no lingering buff loop and no dais.

**Light and dark boards.** The domain is a dark field (stone mean about `#30292a`), so its edge reads hard on snow and
by its gold on night boards. The rails are burnished demon gold (`#764a12` to `#fadc96`) with a
recessed groove (`#46280a`) between them. The cast's burning current (`#ffcf4a` to `#fff4c8`) runs in that groove.
**Alongside other effects.** The floor is static art: it draws under fighters, highlights and every other clip, and
it carries no loop. Clips keep out of every fighter and every meter row (`keepout()` in `build_domain.py`):
- the hex's own fighter: the centre column, +-0.35 h from the hex bottom up, and +-0.55 h from 1.25 h up (its
  meters; LPC hudTop 1.5 h, AI originals 1.99 h);
- the lower hex's fighter head and meters: +-0.55 h, 0.15-1.0 h;
- the diagonal neighbours: |x| >= 1 h, from 0.7 h up.

On the true-scale composite, both column parities, measured with the independent reviewer's renderer
(`qa_render.py`, actual sprite and meter alpha): every enemy's body is covered at most 15 % on any frame, and its
meters at most 11 %; no frame exceeds 25 % for any enemy. The floor clips cover the caster 0 %. The caster's own
meter rows (shown only on hover or selection) are covered up to 40 % on ticks 19-21, by the centre strip (v4) and
nothing else. Its arch and palace eave cross them during ticks 15-24, an exception the director accepted on
2026-11-05 ("keep the arch").
In the keep-out zone the real tile shows through from tick 0: a column of formed gold at each hex centre, where
the bloom starts anyway.

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
| Static art fills the hex box (2:1) at any clip ratio. Clips are ratio x h square, 50 px rendition (no rendition is passed for effect clips), linear, drawn over fighters. | `combatEffects.ts:122-150`; `primitives/animation.ts:16`; `sprites.ts:263-268` |
| A ground tag carries ONE `staticAssetPath`; there is no per-hex variant. | `validators/combat.ts:121`; `combatEffects.ts:135` |
| Each record's clip starts when its own images are ready, so records of one cast can start a few ticks apart. | QA B4; `combatEffects.ts:118-160` |

**What follows.**
- The floor is present from tick 0. The arrival is drawn by the band clips covering it (the director's idea):
  - each band hex starts as its own floor with the gold engraved but unlit;
  - the gold forms outward from the hex centre;
  - the clip ends on the floor's look and dissolves to the real tile.
- **The hand-off is as close as a 50 px clip allows, not pixel-exact.** A clip spans 2.5 h in 50 px, so the hex is
  40 x 20 clip px. The tile spans the hex in 50 x 50 px. They are different samplings of the same floor.
  - The clip's formed frame is built from the tile's own on-screen render, exactly centred.
  - Against the tile on screen, over the covered area, the mean absolute difference is 16.3 per channel (0-255),
    and 17 % of pixels differ by more than 32. That is the resolution floor: the tile's look reduced to 50 px and
    scaled back measures 17.6. A 100 px clip would allow 8.8, but the engine fixes 50.
  - The 3-tick ordered dissolve swaps the coarse clip for the sharp tile pixel by pixel, rather than all at once.
  - The positions are integer at both parities, so the numbers are the same at both. The build records them in
    `exports/subaku_domain_v1.json` (`handoff_check`).
- **Load-order tolerance (QA B4).** Every band strip is self-contained: it lights only its own hex, and nothing
  depends on a neighbour's timing.
  - If a strip loads late, its hexes first show the finished tile, then the cover pops on and the gold forms.
  - The pop is the difference between the tile and the cover's first frame: a mean of 21.9, with 19 % of pixels off
    by more than 32. It is mostly the gold going dark: the cover keeps the rails' shape, engraved in near-black
    bronze, as the frame closest to the tile.
  - The floor tile is 128 px, the spec minimum, 15 KB, so it loads first.
- **A unique painted swirl across the domain is not possible.** Every hex in one tag shows identical pixels.
- **Tile variants are not possible either** (one `staticAssetPath` per ground tag). They would mean splitting the
  enemy-weakening ground effect into 2-3 COORDINATES copies:
  - mechanically identical, but more effect lines;
  - the 4 parity-only rim hexes would lose the debuff.
  - So the floor is one tile, and the repeat is broken inside it: the woven lattice (two directions), per-pixel grain,
    16 stones per hex in 7 tones, and tapered joints.

**Parity error (every caster column).**
- Whole bands land on their ring's tick, 4 + 3 d. A half band holds ring d on one parity and ring d + 1 on the other.
  It lands at 3 d + 5, rounded toward the earlier ring: 50 ms late on one parity and 100 ms early on the other.
- On both parities, 40 of the 56 band hexes land exactly on their ring. The other 16 land within 100 ms (QA S5).
- 4 rim hexes per parity are in the domain on one parity only, so they carry no band tag. They are the top four rim
  hexes on an even column and the bottom four on an odd one.
- **Accepted:** these hexes show the finished tile from tick 0, with the seal beat on 19-21. A neighbour's clip cannot
  extend to cover them, because the same strip would then also paint past the rim onto the bare board on every
  other side.

## 3. Assets (built; artpreflight 0 errors / 0 warnings)

Asset library (RUL-2026-11-05-127): every upload goes in the folder **`Jutsu - Subaku Palace`**, named
`Subaku Palace: <part>`.

| File | Library name | Type | Frames x ms | Slot (proposed) |
|---|---|---|---|---|
| `exports/tile_sbk_domain_v3.webp` (128 px) | `Subaku Palace: domain floor` | STATIC | 1 | ground `decreasedamagegiven`: `staticAssetPath` (replaces DemonCastleFloor `zEvI0yd_As_FzNyrr5Iq4`) |
| `exports/anim_sbk_seal_v1.webp` | `Subaku Palace: domain seal` | ANIMATION | 32 x 50 | ground `decreasedamagegiven`: `appearAnimation` (replaces the library clip `c4FqDZWFZOdWn86o6nPL7`); `appearSfx` blank |
| `exports/anim_sbk_wave_b0_v1.webp` | `Subaku Palace: ring 1 wave` | ANIMATION | 32 x 50 | visual tag b0: COORDINATES, origin CASTER, offsets in `subaku_domain_v1.json`, power 2, rounds 1, `appearAnimation` |
| `exports/anim_sbk_wave_b1_v1.webp` | `Subaku Palace: ring 1.5 wave` | ANIMATION | 32 x 50 | visual tag b1 (as b0) |
| `exports/anim_sbk_wave_b2_v1.webp` | `Subaku Palace: ring 2 wave` | ANIMATION | 32 x 50 | visual tag b2 |
| `exports/anim_sbk_wave_b3_v1.webp` | `Subaku Palace: ring 2.5 wave` | ANIMATION | 32 x 50 | visual tag b3 |
| `exports/anim_sbk_wave_b4_v1.webp` | `Subaku Palace: ring 3 wave` | ANIMATION | 32 x 50 | visual tag b4 |
| `exports/anim_sbk_wave_b5_v1.webp` | `Subaku Palace: ring 3.5 wave` | ANIMATION | 32 x 50 | visual tag b5 |
| `exports/anim_sbk_wave_b6_v1.webp` | `Subaku Palace: ring 4 wave` | ANIMATION | 32 x 50 | visual tag b6 |
| `gates/exports/anim_sbk_gates_rise_v4.webp` (centre half; v2 superseded after QA) | `Subaku Palace: gates rise` | ANIMATION | 38 x 50 | SELF `increasedamagegiven`: `appearAnimation`; `appearSfx` Earth `XBlRonNjvwAZx1_HFpHdM` |

The SELF `increasedamagegiven` effect's `staticAssetPath` and `staticAnimation` are **cleared** (no dais, no loop).
The 7 band tags carry no sound and no static slots.

Builders (Pillow only): `floor.py` (the periodic field and the tile), `build_domain.py` (strips and offsets),
`preview.py` (the true-scale composite). It imports the Mother of Echoes `qa_preview.py` read-only. Exploration patterns
(palace lattice, swirl, streams; the superseded 'flow' and 'bold flow' floors are in git history at 5f2c6a07 and be8646d1) are in `tile_v2.py`. The director's four reference tiles are in `refs/`. Ref a
(`677f13a9`) is taken as the live DemonCastleFloor because it is the only one that fills the 2:1 box. No hash is
captured for the live asset, and fetching it would be a live request. Provenance and preflight: `_provenance/`.

**Sound.**
- Remove the ground tag's `appearSfx` Heal (`4iG_WpgEmPGUzHn8z129r`). It plays once per new record, about 120 times
  per cast.
- One Earth (`XBlRonNjvwAZx1_HFpHdM`) goes on the SELF `increasedamagegiven` effect's `appearSfx`: 1 record, so it
  plays once.
- This follows the director's "one Earth sound" (2026-11-05). On band tag b0 it would play 4 times (QA S6).

## 4. Mechanics: unchanged (director 2026-11-05)

No mechanic change. The caster's hole stays empty after the cast. Enemies standing in the palace deal 15 % less for
3 rounds; the master deals 30 % more for 2.

## 5. Ratio-1 note (338126cb; the director expects it reverted)

At `EFFECT_ANIMATION_HEX_RATIO = 1` a clip is h x h: it covers the hex's central rectangle and never the wing triangles
where columns meet. Lit currents break at every column seam, a veil would draw dark boxes, and painted slices cannot
tile. The static floor still fills the hex. The ratio-1 strip build is kept in git history at 5f2c6a07. It is not
maintained. The gates agent's `anim_sbk_gates_rise_v3` (`gates/build_gates_ratio1.py`) is the ratio-1 centre.

## 6. Previews (true scale: 132 x 66 hex, 165 px clip, 50 px rendition, linear; LPC stand-in, labelled)

Contact sheets in `docs/design/subaku_palace/`, with the independent reviewer's renderer run on this build (`qa_render_paths_patched.py`: only its asset/output paths and the gates strip name changed) and its stats (`qa_reviewer_render_*.json`, including the load-skew simulation). The GIFs (arena 12 x 10 and close-up, light and dark, even and odd
caster columns) are regenerated by `preview.py [--odd]`. The board is the real battle still tiled by its own hex
period. The dark board is the harness's night grade.

## 7. Raw art

None is needed: the tile and strips are delivered at the 50 px rendition, where the programmatic finish holds.
An optional painted finish for the stone and the gold is in `docs/handoffs/SUBAKU_PALACE_FLOOR_ART_REQUEST.md`.
