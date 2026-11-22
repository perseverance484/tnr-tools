# Upstream PR draft: let area effects vary per tile, and let one visual cover the area

- Upstream: `studie-tech/TheNinjaRPG`, base `main` 3176d8585 (rebase again before opening).
- Branch: `perseverance484/TheNinjaRPG` `feat/area-tile-variation`, head 736679f66 (two commits, authored as
  perseverance484 with the Claude co-author line, like PR #2575).
- Demo (drag into the PR description on GitHub, where the placeholder is):
  `art/jutsu_icons/forbidden_chakra_fury/animation/v24/pr_fcf_before_after.mp4` (or the `.gif` beside it, 6.8 MB).
  Built by `v24/compare_pr.py` from FCF v23 cut two ways: `v24/cut_today.py` (a 3x caster clip and tile clips, 128 px
  x 32-frame strips) and `v24/cut_full.py` (the whole move as one 14x visual on the user, a 7 x 7 grid sheet of 320 px
  cells). Playback uses the engine's tile hash ported to Python (`v10/board_v10.py`).
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
Let area effects vary per tile, and let one visual cover the area
```

Body (copy from the next line to the end of the block):

```markdown
# Pull Request

## What

An area jutsu's ground effects place the same clips on every tile they cover, and every tile starts them together, so the art reads as one tile stamped across a grid. Nothing can be drawn across the area as a whole either: a clip is at most three tile heights, and an effect sheet is a single column of frames, so a strip within the common 4096 px texture limit holds about 32 frames of 128 px.

Four optional effect settings let each tile's ground-effect clips differ:

- **`animationMirror`** – the effect's clips are mirrored on about half of its tiles.
- **`animationStagger`** (0–1000 ms) – each tile starts its clips up to this long after the effect appears.
- **`animationRipple`** (0–300 ms per hex) – each tile starts this much later per hex between it and the fighter who cast it, so the clips spread outward from the caster. Ground effects record the caster's tile (`castFrom`) when they are placed.
- **`animationAlternate`** (animation asset) – about half of the tiles play this clip in place of the appear animation. Validation requires an appear animation whenever an alternate is set, for every effect list (the shared effect rule, quest starting effects and raid damage-threshold effects).

Ripple and stagger add up, and variation adds at most 2 s of delay to a tile (`MAX_TILE_DELAY_MS`); texture loading can hold a tile back further. A one-shot clip whose effect leaves the battle before the clip has finished, such as a visual replaced by the next action, still plays to its end and is then cleaned up, including when the effect leaves while its textures are loading; looping and static art leave with the effect. Which tiles mirror, where each falls within the stagger and which play the alternate come from a hash of the tile's column and row (`tileVariation` in `combatEffects.ts`), so every client draws the same field and the choice does not follow rows, columns or a checkerboard. Frame timing within a clip is unchanged; a tile's delay only moves when its clips begin.

Two further changes let one clip cover the whole area:

- **A visual on the user can be up to 15x** (`animationScale`, `MAX_SELF_VISUAL_SCALE`). A `visual` tag with target `SELF` plays once, on the caster's tile, so it can be drawn as one picture of the whole move; a range-4 area needs about 13x. Every other tag, and a visual on any other target, keeps the 3x limit, since it repeats on every tile; validation names the field otherwise, for every effect list.
- **Effect sheets can be grids.** A sheet of square frames may be a grid read row by row as well as a vertical strip. The layout is measured from the image (`sheetLayout`): a grid of N columns (at least three) is `ceil(frames / N) / N` times as tall as it is wide, and a sheet that fits no grid is read as a strip. The content list preview reads grids the same way.

<!-- drag pr_fcf_before_after.mp4 here -->
*One move cut three ways, on one clock. Top: every tile playing the same clip at once beside a 3x clip on the caster. Middle: the same clips with mirroring, alternate clips, stagger and ripple. Bottom: the whole move as a single 14x visual on the caster, drawn from a 7 x 7 grid sheet of 320 px frames at 30 ms each.*

## Behaviour

- Applies to ground effects (one per tile). Effects on a character, and the appear and disappear visuals combat spawns for them, keep the artist's orientation and timing.
- Combat spawns an appear visual for each arriving effect, and the visual names the effect it announces (`arrivalFor`). The renderer skips the arrival clip and sound of an announced effect for as long as that effect stays in the battle, so a lasting effect's arrival plays once, through its visual, including when its fighter is downed by the hit and later returns. The visual stands alone, so the arrival still shows when its effect is removed or depleted in the same action or lands on a fighter who falls. An effect nothing announces plays its own arrival. On an occupied tile, the copy forwarded onto the fighter spawns no visual of its own.
- The new settings at their defaults (`false`, `0`, `0`, `""`) change nothing: every tile plays the same clips at the same moment. The fields live in the effect JSON; there is no migration.
- Existing content sees three differences. A one-shot visual that the next action removes plays to its end. A lasting ground or character effect plays its appear clip and sound once, through combat's visual. A ground effect on an occupied tile shows its appear visual once, and a lasting one plays no disappear clip or sound on the fighter each round.
- A departing effect that is finishing its clips does not take the pointer, so hover reaches a live effect on the same tile.
- An effect still in the battle but not shown, such as one on a fighter at 0 HP, keeps its clips for when it returns; an id that returns while its earlier clips are finishing starts fresh.
- The appear and disappear visuals that combat spawns for a ground effect keep its mirror, stagger, ripple and caster tile, as they keep `animationScale`; a lasting ground effect's loops and static art use the same settings. Only appear clips take the alternate.
- Only ground effects a fighter places with an action record a caster tile; battle-start items and passive enemy-skill effects do not ripple. A ground effect's disappear visual ripples from where its caster stood when it was cast.
- A ground effect that moves takes its new tile's orientation; its clips keep their timing.
- When any effect of a cast has a projectile, none of that cast's impact clips add stagger or ripple (they still mirror and alternate): impacts land when the flights do, and the flights already spread by distance. Flights are neither mirrored nor delayed.
- A departing effect's ground art (decal or static image) hides at once; a SURFACE-style clip keeps playing on the ground layer until it finishes.
- Effects already on the board when a battle loads show at once; only arriving effects are staggered. With reduced motion, staggered and rippling tiles start together.
- Variation adds no delay to sounds; they keep their existing timing, including the queueing used while fighters move.
- The alternate clip is preloaded with the battle's texture assets, has the asset picker and preview in the effect form like the other animations, can be cleared with "None" in the mass effect editor, counts as an animation in content review media and asset-usage lists, is checked by the invalid-asset warning, and is inherited by jutsu reskins like the other cosmetic fields. Mirror, stagger and ripple are presentation keys for content review, like `animationScale`.
- Editors: in the effect form the alternate sits beside the appear animation and the other settings beside the animation scale; the mass effect editor shows them as selectable columns in the order chosen. Both editors share one rule for fields a tag never uses (`hiddenEffectFields`): out-of-battle tags drop the battle fields, and activity bonuses and jutsu-slot grants keep only their power and description. The form hides those fields and the mass editor shows them as not applicable.
- The review battlefield preview plays the variation settings across the area from the caster's tile, draws the alternate (and preloads it), and keeps its cycle open for the longest clip plus the farthest tile's delay. The jutsu animation filters do not search the alternate.
- The asset editor describes both sheet layouts when an animation is uploaded.
- Existing sheets keep their layout: a strip measures as one column. Only a strip whose frames are at least nine times as wide as they are tall could read as a grid (N columns match frames about N² times as wide), which is why a grid needs three columns.
- A grid sheet, like a strip, must fit the device's texture size and costs its full decoded area in texture memory (a 2240 px grid is about 20 MB).

## Validation

- Tests cover the schema defaults and bounds, the tile hash (stable, about half the tiles, independent of rows, columns and a checkerboard), mirroring of both clips with unchanged fit, the stagger hold and finish time, the ripple delay by hex distance and its absence without a caster tile, the caster tile recorded on a cast's ground effects, effects present at battle load, reduced motion, the alternate clip and its appear-animation requirement (shared validation, quest starting effects, raid threshold create and update, and the renderer guard), a departed effect's waiting clip playing to its end (on the clip layer and, for SURFACE style, on the ground layer), a projectile cast landing its impacts without delay (including another effect of the same cast), an announced arrival playing once across a downed fighter's return, the review preview carrying variation across an area and timing it, a one-shot clip whose effect leaves while its texture loads, a departing effect with no one-shot being dropped once loaded, a hidden effect keeping its clips until its fighter returns, an id returning while its clips finish (shown or on a downed fighter) starting fresh, character effects and their visuals, appear visuals linked to the effect they announce (lasting and instant, ground and character, a target that survives or falls), an announced effect playing one arrival clip and sound, the arrival surviving its effect's removal or zero power, an unannounced effect playing its own arrival, hover passing over a departing effect, a lasting and an instant ground effect on an occupied tile and a lasting debuff on a surviving fighter each playing one arrival clip and sound through combat processing and the renderer, a ground hit on an occupied tile showing once, forwarded copies of a lasting ground effect spawning no disappear visual, moved effects, ground lifecycle visuals, texture-asset hints, review media paths, the invalid-asset warning, reskin inheritance, the effect form (field lists including out-of-battle tags, stagger and ripple drafts blocking Save, the alternate's picker trigger and preview query) and the mass editor (alternate choices, clearing with None, not-applicable cells on out-of-battle effects and activity bonuses). They also cover a visual on the user above 3x (accepted for target `SELF` up to the cap, rejected on other targets, for other tags and on quest starting effects), the sheet layout (strips, grids, a rounded rendition, the closest of two near grids, sheets that fit no grid, a strip of wide frames), the content list preview cropping a grid across a row boundary, raid threshold create and update with a large visual on the user and on every tile and clip textures (a strip cut down the sheet, a grid cut row by row), and the review preview keeping a visual on the user at its size.
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
- Review round 5 (independent agent on b16b2d1f5): changes requested (P2: a lasting effect on a fighter downed by
  the same action lost its arrival). Applied in ffabfd233: lasting character arrivals are collected during the
  action and spawned as visuals after consequences when the fighter fell or fled (test for survive/fall, confirmed
  to fail without the fix).
- Review round 6 (independent agent on ffabfd233): PASS, one P3 (helper split a doc comment from its type).
  Applied in 2511e336c. Ready for the director's review.
- Director's independent review (on 2511e336c): changes requested (barrier broken in its own action and zero-power
  lasting effects lost their arrival; departing clip stole hover). Applied in 88c6edd91: reverted "combat skips
  visuals for lasting effects" and the fallen-target fallback; combat spawns arrival visuals as main does, each
  linked to its effect (arrivalFor), and the renderer skips an announced effect's own arrival. Departing records
  skip hit testing. Cap described as added delay.
- Review round 7 (independent agent on 88c6edd91): PASS, wording P3s in the body fixed (leftover clause, timeless
  phrasing). No code change; ready for the director's review.
- 2026-11-21: demo GIFs regenerated from FCF v10 with ripple (v10/board_v10.py); caption matches.
- Rebased on main 3176d8585 (258 upstream commits: projectiles, ground styles, animation offset, sound origins,
  item fortify, preview footprint); second commit added (self visual up to 15x, grid sheets). Review round 8
  (independent agent on 2a70fe0a0): changes requested, two P2s (departing SURFACE clip hidden with its ground
  container; tile delay doubled up on projectile impacts) and two P3s (scale label, two relative phrases). Applied in
  75c7e506f with tests confirmed to fail without the fixes.
- Review round 9 (independent agent on 75c7e506f): PASS, one P3 left as written (a projectile cast's own-tile impact
  skips stagger and ripple though nothing flew; the description says "a cast with a projectile"). Ready for the
  director's review.
- Director's independent review (on 75c7e506f): changes requested, four P2s (projectile timing per effect rather than
  per cast; announcements lasting one snapshot; first-within-tolerance grid choice; preview dropping the variation
  settings) and four P3s (ContentImage grid test, raid router scale test, SURFACE decal assertion, upload form text),
  plus wording. Applied in 736679f66, each new test confirmed to fail without its fix.
