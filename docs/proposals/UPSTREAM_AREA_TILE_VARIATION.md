# Upstream PR draft: let area effects vary their clips per tile

- Upstream: `studie-tech/TheNinjaRPG`, base `main` f6619bd4c (rebase again before opening).
- Branch: `perseverance484/TheNinjaRPG` `feat/area-tile-variation` (head SHA in the handoff message; commits
  authored as perseverance484 with the Claude co-author line, like PR #2575).
- Demo GIFs (drag them into the PR description on GitHub, where the placeholders are):
  `art/jutsu_icons/forbidden_chakra_fury/animation/v9/pr_fcf_side_by_side.gif` (main),
  `pr_fcf_today_uniform.gif`, `pr_fcf_tile_variation.gif`. Built by `v9/tile_variation_demo.py` with the engine's
  own tile hash, ported to Python and checked equal on a 12 x 10 board.
- Lessons applied from PR #2575 (the maintainer added a commit to cover data-model cases we missed): the places the
  comparable `animationScale` field reaches (commit 8bd670153) were followed, except the battlefield preview, left
  out on purpose and stated; behaviours have a test that fails when the code is removed, except the audit
  snapshot's key lists, which are module-internal and untested upstream too; the description follows `AGENTS.md`.
- Review round 1 (independent agent on 1fb401660): character visuals no longer vary, loops show at once at battle
  load, the alternate is previewed and sits beside the appear animation, tile (0,0) varies, the missing tests were
  added, and the description's claims were corrected.

Title:

```
Let area effects vary their clips per tile
```

Body (copy from the next line to the end of the block):

```markdown
# Pull Request

## What

An area jutsu places the same clips on every tile it covers, and every tile starts them together, so its art reads as one tile stamped across a grid. Four optional effect settings let each tile differ:

- **`animationMirror`** – the effect's clips are mirrored on about half of its tiles.
- **`animationStagger`** (0–1000 ms) – each tile starts its clips up to this long after the effect appears.
- **`animationRipple`** (0–300 ms per hex) – each tile starts this much later per hex between it and the fighter who cast it, so the clips spread outward from the caster. Ground effects record the caster's tile (`castFrom`) when they are placed.
- **`animationAlternate`** (animation asset) – about half of the tiles play this clip in place of the appear animation, which it requires.

Ripple and stagger add up. Which tiles mirror, where each falls within the stagger and which play the alternate come from a hash of the tile's column and row (`tileVariation` in `combatEffects.ts`), so every client draws the same field and the choice does not follow rows, columns or a checkerboard. Frame timing within a clip is unchanged; a tile's delay only moves when its clips begin.

<!-- drag pr_fcf_side_by_side.gif here -->
*Top: one field clip on every tile. Bottom: the same jutsu using ripple, stagger, mirroring and an alternate clip.*

## Behaviour

- Applies to ground effects (one per tile). Effects on a character, and the appear and disappear visuals combat spawns for them, keep the artist's orientation and timing.
- Defaults (`false`, `0`, `0`, `""`) leave every tile identical, so existing content draws the same. The fields live in the effect JSON; there is no migration.
- The appear and disappear visuals that combat spawns for a ground effect keep its mirror, stagger, ripple and caster tile, as they keep `animationScale`. Only appear visuals take the alternate clip.
- Ground effects placed without a caster (battle-start items) have no caster tile and do not ripple.
- A ground effect that moves takes its new tile's orientation; its clips keep their timing.
- Effects already on the board when a battle loads show at once; only arriving effects are staggered. With reduced motion, staggered and rippling tiles start together.
- Sounds play when the effect appears; only clips are delayed.
- The alternate clip is preloaded with the battle's texture assets, previewed and picked in the effect form like the other animations, counts as an animation in content review media and asset-usage lists, is checked by the invalid-asset warning, and is inherited by jutsu reskins like the other cosmetic fields. Mirror, stagger and ripple are presentation keys for content review, like `animationScale`.
- Editors: the alternate sits beside the appear animation and the other settings beside the animation scale, in the effect form and the mass effect editor. They are battle-only fields, hidden on out-of-battle tags.
- The review battlefield preview and the jutsu animation filters work from the existing animation fields: the preview draws a single ground tile with the base clips, and the filters do not search the alternate.

## Validation

- Tests cover the schema defaults and bounds, the tile hash (stable, about half the tiles, independent of rows, columns and a checkerboard), mirroring of both clips with unchanged fit, the stagger hold and finish time, the ripple delay by hex distance and its absence without a caster tile, the caster tile recorded on a cast's ground effects, effects present at battle load, reduced motion, the alternate clip, character effects and their visuals, moved effects, ground lifecycle visuals, texture-asset hints, review media paths, the invalid-asset warning, reskin inheritance, and the effect form (field list, stagger and ripple drafts, alternate picker and preview) and mass editor.
- `make lint` passes, and TypeScript passes (`tsc --noEmit --singleThreaded`). The rendering, combat, content review, validator and layout suites pass apart from failures that also occur on `main` in the same environment (renderer context loss, overflow toolbar and avatar suites).

## Breaking changes

None.

## Vercel preview

Pull requests do **not** get a Vercel preview automatically. A collaborator with write access can comment `/tnr-create-preview` on this PR to deploy one of the current head commit. Later pushes do not refresh it — run the command again if you need an updated URL.

## License

By making this pull request, I confirm that I have the right to waive copyright and related rights to my contribution, and agree that all copyright and related rights in my contributions are waived, and I acknowledge that the Studie-Tech ApS organization has the copyright to use and modify my contribution for perpetuity.
```
