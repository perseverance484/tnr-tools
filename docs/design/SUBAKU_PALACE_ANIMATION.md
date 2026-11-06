# Subaku Palace: the domain summoning (design, assets, engine limits)

Status: design and built strips, 2026-11-06 (final polish: light-only, the director's tile). **No manifest yet.** Jutsu `jELEiw5W3N4m2R3oJm3Pk` (player EVENT, A rank,
JONIN, level 25, 40 AP, cooldown 7, 500 chakra and 500 stamina; AOE_SPIRAL_SHOOT, target GROUND, range 4).
Mechanics are unchanged: SELF `increasedamagegiven` 30 % for 2 rounds; GROUND `decreasedamagegiven` 15 % on ENEMIES for
3 rounds.

Rulings: RUL-2026-11-05-124 (payoffs as one picture, the stage, no sickly green, premium), RUL-2026-11-05-125
(the remake; the exact-geometry tile ships; up to 7 visual-tag lines in the jutsu details), RUL-2026-11-05-127
(asset library) and RUL-2026-11-06-128 item 7 (the bloom direction approved; the arch kept). Director,
2026-11-06: light-only arrival with no spill; the resting tile to resemble his original as closely as possible. Text of record:
`docs/design/jutsu_overhaul/EVENT_JUTSU_STORY_TEXT.md`. Shared clock and palette: `art/subaku_palace/TIMING.md`.
Centre half (sigil, gates, palace): `art/subaku_palace/gates/README.md`.

Live-game requests: 0. Game source read at theninjarpg `3314d122` and upstream main `cb755375`; never run.

## 1. What the player sees

Build target (director, 2026-11-05): 2.5-hex-height clips and LPC character avatars. Arrival (director, 2026-11-06):
**light only**, with no cover and no spill.

1. **Anticipation (ticks 0-6).** The domain is there from tick 0: the director's own floor at rest, with dark basalt
   plates, red glow in the mortar and his burnished double-rail gold, unlit. At the caster's feet the burning-gold
   sigil kindles and spirals out (centre strip).
2. **The bloom (7-25).** The gold lights up outward from the caster as one wave:
   - ring 1 ignites on tick 7, and the next half-ring band every 2 ticks (ring 4 on 19);
   - in each hex a white-hot head runs out along his bands from the centre to the edges in 4 ticks (on into the
     neighbours, up to 1.5 hex radii from the centre, so the current flows from hex to hex); the band then cools over
     3 ticks (burning, then lit gold) back to his resting gold; the red mortar flares a tick behind the head;
   - only band pixels are drawn: no cover, so the fighters, their meter rows and the floor stay visible throughout;
   - ring 4's light stays inside its own hexes (no spill onto the bare board past the rim).
3. **The gates (7-19).** Red sandstone oni gates tear out of the ground on ring 1, and the palace with its moon gate
   rises behind the caster (centre strip, gates v6).
4. **The final pulse (26-32).** Every band in the domain flares together, uncut, on its core, ramping 18 /
   40 / 75 / 100 / 70 / 40 / 15 %, white-hot on tick 29 (the seal, the ground appear), with the palace's held beat on
   29-30. The bands are lit whole (QA r4: the earlier fighter cuts chopped them into dashes).
5. **The settle (31-43).** The gates sink; nothing on the floor animates after tick 32.
6. **The 3 rounds.** The director's own tile (the live DemonCastleFloor, ref a / ref c), changed only where its band
   ends missed their neighbours (section 3). It lies under the fighters, with no loop. The caster's own hex stays
   empty after the cast (director 2026-11-05: it has no in-game effect either).
7. **The self-buff.** The gates and palace are the master's moment. Per the director, the sigil is symbolic and
   fades in the cast: there is no lingering buff loop and no dais.

**Light and dark boards.** The domain is his dark basalt field, so its edge reads hard on snow and by its gold on night
boards. At rest the bands are his own burnished gold, unchanged (`SBK_REST_SCALE` 1.0). The bloom is clearly brighter:
a white-hot head (`#fff4c8`) and a burning trail (`#ffe58a`, `#ffcf4a`).
**Alongside other effects.** The floor is static art: it draws under fighters, highlights and every other clip, and
it carries no loop. The clips draw only on the bands, about 2 px wide on the 50 px clip. Measured with the independent
reviewer's renderer (`qa_render.py`, actual sprite and meter alpha), both column parities:
- every LPC enemy body is at most 23 % covered, on no frame over 25 %; the wide AI avatar beside the caster is at
  most 33 %, on 6 frames, as heads pass (the bands are thicker now, at his width);
- meter rows: LPC at most 23 %; the AI avatars' higher rows at most 41 %, on 5-6 frames;
- during the final pulse no body is more than 13 % covered and no LPC meter row more than 23 %;
- frame to frame, the largest whole-arena change is 3.4 (mean absolute, 0-255, light board).
The centre strip's
sigil ring (ticks 4-23) crosses the lower neighbour's meter rows, up to 16 % of them (QA r3: a real ground ring,
hidden only behind the legs); its gates, palace and shards never do. The caster's own
meter rows are crossed by the centre strip's moon-gate arch and nothing else (38 % on the reviewer's renderer, ticks
24-33). The director accepted this on 2026-11-05 ("keep the arch"; RUL-2026-11-06-128). The casting player always
sees their own rows (theninjarpg cb755375 `combat.ts:420` passes the viewer's userId as `selectedId`;
`combatActors.ts:516-520`).

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
- The floor is present from tick 0, so the arrival is light, not reveal: the director's tile rests unlit and the
  bloom races along its bands. There is no cover, so there is no hand-off, nothing hides a fighter, and the untagged
  rim hexes simply rest like their neighbours.
- **Direction inside a hex.** All hexes in one tag show identical pixels, so a strip cannot know which edge its
  current enters by. Each hex lights from its own centre; the light runs on into the neighbours, and the ring timing
  (4 ticks a ring, 4 ticks centre to edge) chains it into one outward front. A current entering only from the
  caster's side would need ring x direction groups, about 40 tags against the 7 allowed.
- **Load order (QA B4).** Each record's clip starts when its own images are ready. Every band strip is
  self-contained. A late strip only lights its rings late; a late tile leaves the bare board under the light until
  it arrives. Nothing pops: the light draws on the floor, never over a cover.
- **A unique painted swirl across the domain is not possible.** Every hex in one tag shows identical pixels.
- **Tile variants are not possible either** (one `staticAssetPath` per ground tag). They would mean splitting the
  enemy-weakening ground effect into 2-3 COORDINATES copies:
  - mechanically identical, but more effect lines;
  - the 4 parity-only rim hexes would lose the debuff.

**Parity error (every caster column).**
- Whole bands ignite on their ring's tick, 3 + 4 d. A half band holds ring d on one parity and ring d + 1 on the
  other. It ignites exactly between them, at 5 + 4 d: 100 ms late on one parity and 100 ms early on the other.
- On both parities, 40 of the 56 band hexes ignite exactly on their ring; the other 16 within 100 ms.
- 4 rim hexes per parity are in the domain on one parity only, so they carry no band tag. They are the top four rim
  hexes on an even column and the bottom four on an odd one.
- **Ruled (director 2026-11-06): light-only, no spill.** These hexes rest like their neighbours and flare in the
  final pulse (26-32). Extending ring 4's light into them would also paint lit bands onto the bare board past the rim
  on every other side; a strip cannot tell the two apart.

## 3. Assets (built; artpreflight 0 errors / 0 warnings)

Asset library (RUL-2026-11-05-127, folder name per RUL-2026-11-06-130: `^[a-zA-Z0-9]*$`): every upload goes in the folder
**`JutsuSubakuPalace`**, named
`Subaku Palace: <part>`.

**The resting tile** (`classic.py`; the director's ref c, the hi-res live floor, cropped to its hex and resampled to
the corner-to-corner canvas the game stretches):
- Join rule: across edge k a neighbour shows its edge k + 3, so a band leaving edge k at u with outward direction d
  needs one leaving edge k + 3 at 1 - u with outward direction d + 180. Measured on his tile, 11 of its band ends have
  no partner (only the L / bottom-left arc and the S / bracket pairs come close). That is why the live floor reads as
  repeated hooks.
- Kept: his five elements, his stone and mortar glow, his burnished gold texture (sampled from his L), his band width
  (thickened to 0.128 so it reads at his visible width at 50 px), his bevel (lit from the upper left) and his
  segment caps (a dark joint every 0.30 along each band).
- Changed, only to make every end meet:
  - the S band leaves the upper-left edge horizontally as his does (u 0.24, his 0.30); its lower end comes down to
    the bottom edge at 0.15 (his ran out through the lower-right edge near the bottom corner);
  - the top-left L: his, its ends at 0.20 (his 0.216) and the upper-left midpoint (his 0.483);
  - the top-right arc: his, from the top edge at 0.85 to the upper-right midpoint;
  - the bottom-left arc: his sweep up from the bottom edge at 0.80 (his 0.81), now ending at the lower-left midpoint
    (his ran on to the left corner);
  - the right bracket: his chamfered bracket, attached to the lower-right edge at the midpoint and at 0.76, with his crisp 45-degree corners (his
    straddled the right corner);
  - the profile: a symmetric double rail (two rails, a dark groove) at his total width, because his wide-plus-narrow
    pair cannot keep its narrow rail on a consistent side across a seam;
  - where an old band no longer runs, his stone is filled in from a rotated or mirrored copy of his own tile (one
    symmetry per hole, with a mortar line round it).
- Pairs, all exact in position and direction: L top / bottom-left arc (0.20 / 0.80); L left / bracket (0.50 / 0.50);
  S left / bracket (0.24 / 0.76); S bottom / top-right arc (0.15 / 0.85); bottom-left arc / top-right arc (the
  midpoints). `python3 classic.py` prints the join check.
- Bleed (QA r4 B1): the tile carries 0.06 radius of the neighbouring hexes' own content past its edge, his dark rim
  is replaced by the inner pixels so bands run unbroken across the seam, and alpha is 255. No pale seam shows on snow
  at 50 px.
- Delivered as a 96-colour lossless palette WebP, 128 px, about 10 KB (QA r4 S3; the band strips are about 1.4 KB).
- Side by side (hi-res, 1x true scale, 3x, the 50 px rendition, and tiled at true scale on snow):
  `docs/design/subaku_palace/tile_original_vs_new.png`.

| File | Library name | Type | Frames x ms | Slot (proposed) |
|---|---|---|---|---|
| `exports/tile_sbk_domain_v4.webp` (128 px palette, about 10 KB, `classic.py`) | `Subaku Palace: domain floor` | STATIC | 1 | ground `decreasedamagegiven`: `staticAssetPath` (replaces DemonCastleFloor `zEvI0yd_As_FzNyrr5Iq4`) |
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

Builders (Pillow only): `classic.py` (the resting tile and its band masks), `build_domain.py` (strips and offsets;
`SBK_VARIANT=cover` builds the reference cover variant into `reference/cover_variant_DO_NOT_UPLOAD/` (never upload) from `floor.py`'s 'rails' tile),
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

Contact sheets in `docs/design/subaku_palace/`, with the independent reviewer's renderer run on this build (`qa_render_paths_patched.py`: only its asset/output paths and the gates strip name changed) and its stats (`qa_reviewer_render_*.json`, the clips-late case is moot without a cover). The GIFs (arena 12 x 10 and close-up, light and dark, even and odd
caster columns) are regenerated by `preview.py [--odd]`. The board is the real battle still tiled by its own hex
period. The dark board is the harness's night grade.

## 7. Raw art

None is needed: the resting tile is the director's own art (ref c), with its bands redrawn only to join. The earlier
optional painted-finish request (`docs/handoffs/SUBAKU_PALACE_FLOOR_ART_REQUEST.md`) applied to the procedural floor
and is superseded.
