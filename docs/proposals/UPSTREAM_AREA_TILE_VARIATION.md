# Upstream PR draft: let area effects vary their clips per tile

- Upstream: `studie-tech/TheNinjaRPG`, base `main` 7fc8789d2.
- Branch: `perseverance484/TheNinjaRPG` `feat/area-tile-variation` (commit SHA in the handoff message; one commit,
  authored as perseverance484 with the Claude co-author line, like PR #2575).
- Demo GIFs (drag them into the PR description on GitHub, where the placeholders are):
  `art/jutsu_icons/forbidden_chakra_fury/animation/v9/pr_fcf_side_by_side.gif` (main),
  `pr_fcf_today_uniform.gif`, `pr_fcf_tile_variation.gif`. Built by `v9/tile_variation_demo.py` with the engine's
  own tile hash, ported to Python and checked equal on a 12 x 10 board.
- Lessons applied from PR #2575 (the maintainer added a commit to cover data-model cases we missed): every place
  the comparable `animationScale` field reaches was followed (commit 8bd670153 touched 16 files), each behaviour has
  a test that fails when it is removed, and the description follows `AGENTS.md` (timeless, no chronology).

Title:

```
Let area effects vary their clips per tile
```

Body (copy from the next line to the end of the block):

```markdown
# Pull Request

## What

An area jutsu puts the same clips on every tile it covers, all starting together, so its art reads as one tile stamped across a grid. Three optional effect settings let each tile differ:

- **`animationMirror`** – the effect's clips are mirrored on about half of its tiles.
- **`animationStagger`** (0–1000 ms) – each tile starts its clips up to this long after the effect appears.
- **`animationAlternate`** (animation asset) – about half of the tiles play this clip instead of the appear animation.

Which tiles mirror, how late each starts and which play the alternate come from a hash of the tile's column and row (`tileVariation` in `combatEffects.ts`), so every client draws the same field and the choice never repeats in stripes or a checkerboard. Timing inside a tile is unchanged, so a clip's own lead frames still line up with the caster's clip.

<!-- drag pr_fcf_side_by_side.gif here -->
*Top: an area jutsu today, the same field clip on every tile. Bottom: the same art with `animationMirror`, a 300 ms `animationStagger` and an alternate vein clip that meets the same tile edges.*

## Behaviour

- Applies to ground effects (one per tile). Effects attached to a character keep the artist's orientation and timing.
- Defaults (`false`, `0`, `""`) draw exactly as before, so existing content is unchanged. The fields live in the effect JSON; there is no migration.
- The appear and disappear visuals that combat spawns for an effect keep its mirror and stagger, as they keep `animationScale`. Only appear visuals take the alternate clip.
- A ground effect that moves takes its new tile's orientation; its clips keep their timing.
- With reduced motion, staggered tiles start together.
- The alternate clip is preloaded with the battle's texture assets, counts as an animation in content review media and asset-usage lists, is checked by the invalid-asset warning, and is inherited by jutsu reskins like the other cosmetic fields. Mirror and stagger are presentation keys for content review, like `animationScale`.
- Editors: the three fields sit next to the other animation fields in the effect form and the mass effect editor; the alternate uses the animation asset picker. They are battle-only fields, hidden on out-of-battle tags.
- The review battlefield preview draws a single ground tile, so it shows the base clips.

## Validation

- New and updated tests cover the schema defaults and bounds, the tile hash (stable, about half the tiles, no simple pattern), mirroring of both clips with unchanged fit, the stagger hold and finish time, reduced motion, the alternate clip, character effects, moved effects, lifecycle visuals, texture-asset hints, reskin inheritance and the editor field list.
- `make lint` and `make typecheck` pass. The rendering, combat, content review, validator and layout suites pass apart from failures that also occur on `main` in the same environment (renderer context loss, overflow toolbar and avatar suites).

## Breaking changes

None.

## Vercel preview

Pull requests do **not** get a Vercel preview automatically. A collaborator with write access can comment `/tnr-create-preview` on this PR to deploy one of the current head commit. Later pushes do not refresh it — run the command again if you need an updated URL.

## License

By making this pull request, I confirm that I have the right to waive copyright and related rights to my contribution, and agree that all copyright and related rights in my contributions are waived, and I acknowledge that the Studie-Tech ApS organization has the copyright to use and modify my contribution for perpetuity.
```
