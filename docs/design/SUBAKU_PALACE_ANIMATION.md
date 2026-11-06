# Subaku Palace: the domain summoning (design, assets, engine limits)

Status: design and built strips, 2026-11-05. **No manifest yet.** Jutsu `jELEiw5W3N4m2R3oJm3Pk` (player EVENT, A rank,
JONIN, level 25, 40 AP, cooldown 7, 500 chakra and 500 stamina; AOE_SPIRAL_SHOOT, target GROUND, range 4).
Mechanics are unchanged: SELF `increasedamagegiven` 30 % for 2 rounds; GROUND `decreasedamagegiven` 15 % on ENEMIES for
3 rounds.

Rulings: RUL-2026-11-05-124 (payoffs as one picture, the stage, no sickly green, premium), RUL-2026-11-05-125
(the remake; the exact-geometry tile ships; up to 7 visual-tag lines in the jutsu details), RUL-2026-11-05-127
(asset library) and RUL-2026-11-06-128 item 7 (the bloom direction approved; the arch kept). Text of record:
`docs/design/jutsu_overhaul/EVENT_JUTSU_STORY_TEXT.md`. Shared clock and palette: `art/subaku_palace/TIMING.md`.
Centre half (sigil, gates, palace): `art/subaku_palace/gates/README.md`.

Live-game requests: 0. Game source read at theninjarpg `3314d122` and upstream main `cb755375`; never run.

## 1. What the player sees

Build target (director, 2026-11-05): 2.5-hex-height clips and LPC character avatars.

1. **Anticipation (ticks 0-6).** The domain lies as bare stone: every band hex is covered whole by its own floor with
   no gold at all (the director's arrival, 2026-11-05/06). Only 1.4 % of the floor's gold pixels show at tick 0, at
   the jagged hex edges. At the caster's feet the burning-gold sigil kindles and spirals out (centre strip).
2. **The bloom (7-30).** The gold blooms outward from the caster as one wave:
   - ring 1 ignites on tick 7, and the next half-ring band every 2 ticks (ring 4 on 19);
   - in each hex a white-hot head runs out along the rails from the centre to the edges over 8 ticks, with a stepped
     burning trail and the red cracks flaring a tick behind it;
   - each ring ignites when the previous ring's head is halfway out, so the blooms overlap into one continuous front;
   - where the head has passed, the cover is gone: the real tile (and any fighter or meter row) shows, with only the
     lit rails drawn over it, and the trail fades out;
   - the last head reaches the rim on tick 27.
3. **The gates (7-19).** Red sandstone oni gates tear out of the ground on ring 1, and the palace with its moon gate
   rises behind the caster (centre strip, gates v6).
4. **The held beat (28-30).** The rim has formed. Every rail face in the domain burns solid at once, the channels
   white-hot on tick 29 (the seal, the ground appear), and the palace's held beat lands on 29-30.
5. **The settle (31-43).** The gates sink; nothing on the floor animates after tick 30.
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
it carries no loop. **The cover has no fighter keep-out** (director, 2026-11-05: "I don't care if the animation covers
the fighter for a moment"). A fighter in the domain is hidden by its hex's stone (and, above the hex top, by the
next hex's) from tick 0 until the bloom reaches it. Nothing lingers: the cover opens where the head passes, and only
the lit rails remain for the 3-tick trail. Measured with the independent reviewer's renderer (`qa_render.py`, actual
sprite and meter alpha), on both column parities with identical numbers:
- frames with an enemy's body more than 25 % covered: ring 1 16-19 (0.8-0.95 s), ring 2 21 (LPC), AI originals on rings 2-3 24-26, and
  ring 4 29 (1.45 s, the maximum: its head stands in the outer neighbour, whose bloom passes last);
- meter rows follow the same pass, 19-28 frames.
The centre strip's
sigil ring (ticks 4-23) crosses the lower neighbour's meter rows, up to 16 % of them (QA r3: a real ground ring,
hidden only behind the legs); its gates, palace and shards never do. The caster's own
meter rows are crossed by the centre strip's moon-gate arch and nothing else: on ticks 24-33 in v6 (the roof wings now
sit below the rows), up to 33 % of the rows by the build's rectangle (the reviewer's renderer measured 40 % on v4; to
re-measure on v6). The director accepted this on 2026-11-05 ("keep the arch") on the understanding that those rows show
only on hover or selection. That holds for other viewers only: the casting player always sees their own rows
(theninjarpg cb755375 `combat.ts:420` passes the viewer's userId as `selectedId`; `combatActors.ts:516-520`).

## 2. Engine reality (what made the design)

| Fact | Source |
|---|---|
| AOE_SPIRAL_SHOOT covers spiral(caster, range) minus the caster's own hex: 60 hexes, all in one action. There is a **hole** under the caster. | `libs/combat/targeting.ts:56-58` |
| One snapshot creates every record of the cast, so a ring order must be baked into separate strips (their clips still start when their own images are ready; see below). | engine doc 0.1, 2.3 |
| There is **no per-tag delay** anywhere in the combat code. Static art is drawn from the record's first ready frame for its whole life. **The floor cannot arrive late.** | `libs/combat` at 3314d122 and cb755375: the only `delay` is the encounter round delay (`encounters.ts:14`), unrelated to tags; `scenes/combatEffects.ts:139-160` |
| A ground tag's appear plays x2 (client record + server visual). The occupant copy of a damage modifier skips applySingleEffect, so there is no third. | `libs/combat/process.ts:432-442`, `:657-739` |
| Visual tags (COORDINATES) are stamped only on their own offsets, x1, with no occupant copy, and are dropped at the first action of round N+1 (fine for one-shots). | `actions.ts:1063-1112`; `routers/combat.ts:851-860`; RUL-2026-11-02-101 |
| COORDINATES offsets are col/row. On one caster parity, odd columns sit half a row off. | `targeting.ts:59-75` |
| Visual tags are listed in the player-facing jutsu details. | `layout/ItemWithEffects.tsx:1297` |
| Static art fills the hex box (2:1) at any clip ratio. Clips are ratio x h square, 50 px rendition (no rendition is passed for effect clips), linear, drawn over fighters. | `combatEffects.ts:122-150`; `primitives/animation.ts:16`; `sprites.ts:263-268` |
| A ground tag carries ONE `staticAssetPath`; there is no per-hex variant. | `validators/combat.ts:121`; `combatEffects.ts:135` |
| Each record's clip starts when its own images are ready, so records of one cast can start a few ticks apart. | QA B4; `combatEffects.ts:118-160` |

**What follows.**
- The floor is present from tick 0. The arrival is drawn by the band clips covering it (the director's idea): each
  band hex starts as its own floor with no gold, and the gold blooms outward and uncovers the real tile as it passes.
- **The hand-off is exact by construction.** Behind the trail the clip is transparent, so what shows is the tile
  itself. The cover's stone is built from the tile's own on-screen render (the floor without gold), exactly centred.
  At tick 0 the cover hides 98.6 % of the gold pixels; the rest show at the jagged hex edges of the 50 px clip.
  (`exports/subaku_domain_v1.json`, `handoff_check`.)
- **Direction inside a hex.** All hexes in one tag show identical pixels, so a strip cannot know which edge its
  current enters by. Each hex blooms from its own centre. The ring timing (4 ticks a ring, 8 ticks a bloom) chains
  them into one outward front. A current entering from the caster's side would need ring x direction groups, about
  40 tags against the 7 allowed.
- **Load order (QA B4).** Each record's clip starts when its own images are ready. Every band strip is
  self-contained: it lights only its own hex and depends on no neighbour.
  - **Tile late, clips on time:** the cover is opaque stone, so a late tile is hidden while the hex is still covered.
    Only a hex whose bloom has already passed would show bare board until the tile arrives.
  - **Clips late, tile on time** (simulated with the reviewer's renderer, every band strip 4 ticks late): the finished
    floor shows for those 4 ticks, then the stone cover pops on (a whole-frame mean change of 6.6) and the bloom
    plays in full, 4 ticks late. If only some strips are late, only their rings flash the finished floor first.
  - Sizes: the floor tile is 128 px (the spec minimum), about 15 KB. The band strips are about 3 KB each. Size alone
    does not set the load order, so neither case can be ruled out.
- **A unique painted swirl across the domain is not possible.** Every hex in one tag shows identical pixels.
- **Tile variants are not possible either** (one `staticAssetPath` per ground tag). They would mean splitting the
  enemy-weakening ground effect into 2-3 COORDINATES copies:
  - mechanically identical, but more effect lines;
  - the 4 parity-only rim hexes would lose the debuff.
  - So the floor is one tile, and the repeat is broken inside it: the woven lattice (two directions), per-pixel grain,
    16 stones per hex in 7 tones, and tapered joints.

**Parity error (every caster column).**
- Whole bands ignite on their ring's tick, 3 + 4 d. A half band holds ring d on one parity and ring d + 1 on the
  other. It ignites exactly between them, at 5 + 4 d: 100 ms late on one parity and 100 ms early on the other.
- On both parities, 40 of the 56 band hexes ignite exactly on their ring; the other 16 within 100 ms.
- 4 rim hexes per parity are in the domain on one parity only, so they carry no band tag. They are the top four rim
  hexes on an even column and the bottom four on an odd one.
- **Accepted:** these hexes show the finished tile from tick 0, with the final pulse on 28-30. A neighbour's clip cannot
  extend to cover them, because the same strip would then also paint past the rim onto the bare board on every
  other side.

## 3. Assets (built; artpreflight 0 errors / 0 warnings)

Asset library (RUL-2026-11-05-127): every upload goes in the folder **`Jutsu - Subaku Palace`**, named
`Subaku Palace: <part>`.

| File | Library name | Type | Frames x ms | Slot (proposed) |
|---|---|---|---|---|
| `exports/tile_sbk_domain_v3.webp` (128 px) | `Subaku Palace: domain floor` | STATIC | 1 | ground `decreasedamagegiven`: `staticAssetPath` (replaces DemonCastleFloor `zEvI0yd_As_FzNyrr5Iq4`) |
| `exports/anim_sbk_seal_v1.webp` | `Subaku Palace: domain seal` | ANIMATION | 36 x 50 | ground `decreasedamagegiven`: `appearAnimation` (replaces the library clip `c4FqDZWFZOdWn86o6nPL7`); `appearSfx` blank |
| `exports/anim_sbk_wave_b0_v1.webp` | `Subaku Palace: ring 1 wave` | ANIMATION | 36 x 50 | visual tag b0: COORDINATES, origin CASTER, offsets in `subaku_domain_v1.json`, power 2, rounds 1, `appearAnimation` |
| `exports/anim_sbk_wave_b1_v1.webp` | `Subaku Palace: ring 1.5 wave` | ANIMATION | 36 x 50 | visual tag b1 (as b0) |
| `exports/anim_sbk_wave_b2_v1.webp` | `Subaku Palace: ring 2 wave` | ANIMATION | 36 x 50 | visual tag b2 |
| `exports/anim_sbk_wave_b3_v1.webp` | `Subaku Palace: ring 2.5 wave` | ANIMATION | 36 x 50 | visual tag b3 |
| `exports/anim_sbk_wave_b4_v1.webp` | `Subaku Palace: ring 3 wave` | ANIMATION | 36 x 50 | visual tag b4 |
| `exports/anim_sbk_wave_b5_v1.webp` | `Subaku Palace: ring 3.5 wave` | ANIMATION | 36 x 50 | visual tag b5 |
| `exports/anim_sbk_wave_b6_v1.webp` | `Subaku Palace: ring 4 wave` | ANIMATION | 36 x 50 | visual tag b6 |
| `gates/exports/anim_sbk_gates_rise_v6.webp` (centre half; v2, v4 and v5 superseded after QA) | `Subaku Palace: gates rise` | ANIMATION | 44 x 50 | SELF `increasedamagegiven`: `appearAnimation`; `appearSfx` Earth `XBlRonNjvwAZx1_HFpHdM` |

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
