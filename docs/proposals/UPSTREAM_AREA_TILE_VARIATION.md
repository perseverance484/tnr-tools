# Upstream PR draft: let area effects vary their clips per tile

- Upstream: `studie-tech/TheNinjaRPG`, base `main` a69344979 (rebase again before opening).
- Branch: `perseverance484/TheNinjaRPG` `feat/area-tile-variation`, head b16b2d1f5 (one commit, authored as
  perseverance484 with the Claude co-author line, like PR #2575).
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
  added, and the description's claims were corrected. Round 2 (80647dc26, with ripple): PASS with three P3s, all
  applied in 656e24ce0 (2 s delay cap with a test, the caster-tile wording, the disappear-ripple clause).

Title:

```
Let area effects vary their clips per tile
```

Body (copy from the next line to the end of the block):

```markdown
# Pull Request

## What

An area jutsu's ground effects place the same clips on every tile they cover, and every tile starts them together, so the art reads as one tile stamped across a grid. Four optional effect settings let each tile's ground-effect clips differ:

- **`animationMirror`** – the effect's clips are mirrored on about half of its tiles.
- **`animationStagger`** (0–1000 ms) – each tile starts its clips up to this long after the effect appears.
- **`animationRipple`** (0–300 ms per hex) – each tile starts this much later per hex between it and the fighter who cast it, so the clips spread outward from the caster. Ground effects record the caster's tile (`castFrom`) when they are placed.
- **`animationAlternate`** (animation asset) – about half of the tiles play this clip in place of the appear animation. Validation requires an appear animation whenever an alternate is set, for every effect list (the shared effect rule, quest starting effects and raid damage-threshold effects).

Ripple and stagger add up, and a tile waits at most 2 s (`MAX_TILE_DELAY_MS`), which bounds how long an area takes to fill. A one-shot clip whose effect leaves the battle before the clip has finished, such as a visual replaced by the next action, still plays to its end and is then cleaned up, including when the effect leaves while its textures are loading; looping and static art leave with the effect. Which tiles mirror, where each falls within the stagger and which play the alternate come from a hash of the tile's column and row (`tileVariation` in `combatEffects.ts`), so every client draws the same field and the choice does not follow rows, columns or a checkerboard. Frame timing within a clip is unchanged; a tile's delay only moves when its clips begin.

<!-- drag pr_fcf_side_by_side.gif here -->
*Top: one field clip on every tile. Bottom: the same jutsu using ripple, stagger, mirroring and an alternate clip.* <!-- caption must match the GIF regenerated with ripple -->

## Behaviour

- Applies to ground effects (one per tile). Effects on a character, and the appear and disappear visuals combat spawns for them, keep the artist's orientation and timing.
- Each arrival has one owner. Combat spawns an appear visual only for an effect that ends the round it lands; a lasting effect stays in the battle and the renderer plays its appear clip and sound from it, once. On an occupied tile, the copy forwarded onto the fighter spawns no visual of its own.
- The new settings at their defaults (`false`, `0`, `0`, `""`) change nothing: every tile plays the same clips at the same moment. The fields live in the effect JSON; there is no migration.
- Existing content sees three differences. A one-shot visual that the next action removes plays to its end. A lasting ground or character effect plays its appear clip and sound once, where combat's spawned visual used to play them a second time over the effect's own. A ground effect on an occupied tile shows its appear visual once, and a lasting one plays no disappear clip or sound on the fighter each round.
- An effect still in the battle but not shown, such as one on a fighter at 0 HP, keeps its clips for when it returns; an id that returns while its earlier clips are finishing starts fresh.
- The appear and disappear visuals that combat spawns for a ground effect keep its mirror, stagger, ripple and caster tile, as they keep `animationScale`; a lasting ground effect's own arrival uses the same settings. Only appear clips take the alternate.
- Only ground effects a fighter places with an action record a caster tile; battle-start items and passive enemy-skill effects do not ripple. A ground effect's disappear visual ripples from where its caster stood when it was cast.
- A ground effect that moves takes its new tile's orientation; its clips keep their timing.
- Effects already on the board when a battle loads show at once; only arriving effects are staggered. With reduced motion, staggered and rippling tiles start together.
- Variation adds no delay to sounds; they keep their existing timing, including the queueing used while fighters move.
- The alternate clip is preloaded with the battle's texture assets, has the asset picker and preview in the effect form like the other animations, can be cleared with "None" in the mass effect editor, counts as an animation in content review media and asset-usage lists, is checked by the invalid-asset warning, and is inherited by jutsu reskins like the other cosmetic fields. Mirror, stagger and ripple are presentation keys for content review, like `animationScale`.
- Editors: in the effect form the alternate sits beside the appear animation and the other settings beside the animation scale; the mass effect editor shows them as selectable columns in the order chosen. Both editors share one rule for fields a tag never uses (`hiddenEffectFields`): out-of-battle tags drop the battle fields, and activity bonuses and jutsu-slot grants keep only their power and description. The form hides those fields and the mass editor shows them as not applicable.
- The review battlefield preview and the jutsu animation filters work from the existing animation fields: the preview draws a single ground tile with the base clips, and the filters do not search the alternate.

## Validation

- Tests cover the schema defaults and bounds, the tile hash (stable, about half the tiles, independent of rows, columns and a checkerboard), mirroring of both clips with unchanged fit, the stagger hold and finish time, the ripple delay by hex distance and its absence without a caster tile, the caster tile recorded on a cast's ground effects, effects present at battle load, reduced motion, the alternate clip and its appear-animation requirement (shared validation, quest starting effects, raid threshold create and update, and the renderer guard), a departed effect's waiting clip playing to its end, a one-shot clip whose effect leaves while its texture loads, a departing effect with no one-shot being dropped once loaded, a hidden effect keeping its clips until its fighter returns, an id returning while its clips finish (shown or on a downed fighter) starting fresh, character effects and their visuals, lasting ground and character effects owning their arrival, a lasting and an instant ground effect on an occupied tile each playing one arrival clip and sound through combat processing and the renderer, a ground hit on an occupied tile showing once, forwarded copies of a lasting ground effect spawning no disappear visual, moved effects, ground lifecycle visuals, texture-asset hints, review media paths, the invalid-asset warning, reskin inheritance, the effect form (field lists including out-of-battle tags, stagger and ripple drafts blocking Save, the alternate's picker trigger and preview query) and the mass editor (alternate choices, clearing with None, not-applicable cells on out-of-battle effects and activity bonuses).
- `make lint` passes with only warnings already on `main`, and TypeScript passes (`tsc --noEmit --singleThreaded`). The rendering, combat, content review, validator and layout suites pass apart from failures that also occur on `main` in the same environment; which of the overflow-toolbar, avatar, element-icon and renderer context-loss tests fail varies by environment. SQL-backed tests were skipped without a database.

## Breaking changes

None.

## Vercel preview

Pull requests do **not** get a Vercel preview automatically. A collaborator with write access can comment `/tnr-create-preview` on this PR to deploy one of the current head commit. Later pushes do not refresh it — run the command again if you need an updated URL.

## License

By making this pull request, I confirm that I have the right to waive copyright and related rights to my contribution, and agree that all copyright and related rights in my contributions are waived, and I acknowledge that the Studie-Tech ApS organization has the copyright to use and modify my contribution for perpetuity.
```
- Director's independent review (on 656e24ce0): changes requested, no P0/P1. Applied in 019323a36: forwarded ground
  copies no longer spawn character visuals (occupied tile shows once; lasting effects spawn no per-round disappear
  clip); departed effects finish their one-shot clips before cleanup; shared validation requires an appear
  animation for an alternate and the renderer ignores an alternate without one; both editors share
  `hiddenEffectFields` (now also reskin-slot and jutsu-slot grants; mass editor shows N/A); the mass editor can
  clear the alternate with None; description corrected. The GIF must be regenerated with ripple before opening.
- Review round 3 (independent agent on 019323a36): changes requested. Applied in ea28e4ccb: effects hidden but
  still in the battle keep their loops; a returning id while its record finishes rebuilds fresh (tests for both,
  each confirmed to fail without its fix); description now lists the two behaviour changes for existing content.
- Review round 4 (independent agent on ea28e4ccb): PASS with two P3s. Applied in 334f56cad: a returning id is
  rebuilt in sync's first loop, so it also starts fresh when it returns on a downed fighter (new test, confirmed to
  fail on ea28e4ccb); timeless wording and the validation list fixed. Ready for the director's review.
- Director's independent review (on 334f56cad): changes requested, no P0/P1. Applied in b16b2d1f5: one owner per
  arrival (combat spawns an appear visual only for effects that end the round they land; lasting ground and character
  effects play their own; process-plus-renderer test); departure during texture load keeps one-shots and drops the
  rest once loaded (deferred-texture tests); the alternate rule is shared with quest starting effects and raid
  threshold create/update (input-boundary tests); activity bonuses and jutsu-slot grants use the shared
  hiddenEffectFields rule (mass-editor test); cap comment, test name and description corrected.
