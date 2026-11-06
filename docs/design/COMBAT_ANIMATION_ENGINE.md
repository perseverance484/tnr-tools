# Combat animation engine — what the player actually sees

Status: reference (read-only source analysis). Audience: artists and content authors building custom
combat animations (first consumer: the three-act "Mother of Echoes" boss fight).

Evidence: The Ninja RPG game source at pinned commit **`3314d122`**
(`3314d122c93e036618483d18229a793ad7ad21fd`). Every source citation below is `path:line` at that
commit, relative to the game repo root. Read with `git show 3314d122:<path>`. No live requests were
made and the game was not run. Labels used:

- **[V]** verified by reading the cited code path end to end.
- **[I]** inference: follows from the code but depends on runtime/library/CDN behaviour not in the
  repo, or was not traced through every branch. Treat as a hypothesis to confirm in a preview.

---

## 0. TL;DR for animators

1. **There is no animation timeline.** The server resolves your action plus up to 4 following actions
   (AI turns) and returns **one final battle snapshot**. The client diffs it against what is on screen
   by effect `id` and starts **every** new clip at once. Nothing is sequenced, queued or staggered per
   action. [V]
2. **Appear and static start together**, on the same clock, at the same spot and size. The static loop
   is drawn **on top of** the appear clip (z 2 vs z 1). Design the appear to work *under* the loop's
   frame 0, or leave the static empty in the first frames. [V]
3. **The client never draws `disappearAnimation`.** Only the server spawns it, as a separate
   `visual` ground effect with the clip in its `appearAnimation`. [V]
4. **Appears are duplicated.** For any effect that persists (rounds ≥ 1) and carries an
   `appearAnimation`, the clip plays **twice, stacked, on the same hex** (client-side for the effect
   record + server-spawned `visual`). A ground effect landing on an *occupied* hex in its cast round
   plays it a **third** time. An instant (rounds 0) ground hit on an occupied hex plays twice. Author
   appears assuming 2–3× additive overdraw, or keep them light. Exceptions: summons (1×; `summon()`
   clears `isNew` first, `tags.ts:3190-3191`; `clone()` does not, so clones double) and the four
   damage-modifier tags (1× client-only). [V]
5. **`decrease*` tags on characters are invisible.** `decreasedamagetaken`, `decreasedamagegiven`,
   `decreasestat`, `decreasemastery`, `decreaseheal…`, `decreasepoolcost` rewrite their own `power`
   to a negative number. The client treats `power <= 0` as "depleted" and hides that effect's
   appear, static loop and static art. It also plays `appearSfx` and `disappearSfx` together.
   **A Cradle `decreasedamagetaken` static loop on the boss will never render.** Ground copies of
   these tags are not affected. [V]
6. **"1-round" effects last longer than one player turn.** A rounds:1 effect cast in round N stays
   for the rest of round N and **all of round N+1**. It is removed when round N+2 starts. A boss mark
   cast in round N is **still on screen when the boss erupts it in round N+1**, and stays through
   the rest of N+1. [V]
7. **Clips draw over fighters, portraits and HP bars.** Static *art* (`staticAssetPath`) draws under
   highlights, scenery and fighters. [V]
8. **Size and filtering:** every clip is a square **2.5 hex-heights** wide (≈1.25 hex widths),
   centred on the hex. The source is fetched as a **50 px wide** Bunny rendition and sampled with
   **linear** filtering. The frame is stretched to a square no matter its aspect. Static art is
   stretched to the hex box (2:1). [V] No mipmaps are requested in this code. [I: Pixi default]
9. **Hidden assets never render** (the battle asset query filters `hidden = false`). The default for
   new assets is `hidden = true`. [V]
10. **The first time a jutsu is used in a battle, its effects lag** by one asset-list fetch plus one
    texture fetch. During that gap, *all* effect syncing pauses while fighters and HP bars already
    show the new state. [V mechanism, I magnitude]
11. **The killing blow that ends the battle is never animated.** The canvas is torn down as soon as a
    result exists. [V]

---

## 1. Pipeline: from a performed action to pixels

### 1.1 Server: one request resolves a whole chain

- `performAction` (`app/src/server/api/routers/combat.ts:597`) loops. Each iteration aligns
  round/actor (`alignBattle`, `:668`) and performs the user's action (`:702-751`, via
  `performBattleAction` → `applyEffects`, `app/src/libs/combat/actions.ts:1447`) or an AI action
  (`:752-767`).
- It **continues** while the next actor is autonomous (AI or AI-driven summon) and
  `nActions < maxActions` (`:834-841`). `maxActions` is **5**, or **1** for auto battle types or when
  any live human is on auto-combat (`:629-638`). `nActions` counts history entries
  (`:809-819`), and that includes the player's own action and "Battlefield effects expire" rows. So
  one click delivers the player's action plus **at most 4** more steps. [V]
- If the chain is longer, the client finishes it with **AI polls about 1 s apart**. A
  `setInterval(…, 1000)` calls `performAction` with no action whenever the active actor is
  AI-driven (`app/src/layout/Combat.tsx:809-866`, scenario 1 at `:835-841`). So a long round arrives
  as several snapshots, each with ≤5 steps, spaced ≥1 s plus round-trip time. [V]
- Before saving, `visual` ground effects older than the request's starting round are dropped
  (`combat.ts:857-860`). Then the version is bumped by `nActions` (`:866`). The response is
  `{ battleUpdate: maskBattle(newBattle), logEntries, result }` (`:901`, `:916-922`).
  **`battleUpdate` is the full masked battle state** (`usersState`, `usersEffects`,
  `groundEffects`, `extraState`; `app/src/libs/combat/util.ts:1929-1935`), not a diff. [V]

### 1.2 Client: replace the snapshot, diff by effect id

- `onSuccess` merges `logEntries` into the combat-log query cache first (`Combat.tsx:519-527`,
  `app/src/hooks/combat.ts:79-181`). Then it **replaces** the battle (`Combat.tsx:536-544`). Log
  rows and visuals land together. The log is not used to pace the canvas. [V]
- The scene polls the snapshot every frame and re-syncs when the battle object, its version or its
  assets change (`app/src/libs/rendering/scenes/combat.ts:280-293`). `sync` always syncs fighters
  (`:166-171`). It syncs effects **only when every id in `extraState.textureAssets` and
  `sfxAssets` has already been requested** from the asset API (`:191-199`). [V]
- Effect sync (`app/src/libs/rendering/scenes/combatEffects.ts:42-195`):
  - Records whose id is gone from `groundEffects ∪ usersEffects` are destroyed immediately, with no
    exit animation (`:44-53`).
  - Ground effects are placed on their own `(longitude, latitude)` hex (`:55-58`). User effects are
    placed on their target's **current battle-state** hex, and skipped if the target is not
    `stillInBattle` (`:59-66`).
  - Effects with no `staticAssetPath`, `staticAnimation`, `appearAnimation`, `disappearAnimation`,
    `appearSfx` or `disappearSfx` are ignored (`:76-84`).
  - A **new id** creates a record. It loads the static art (`:129-154`), the appear clip **unless
    this is the scene's initial sync** (`:155`), and the static loop (`:156`). When all of these
    settle, the record is marked `ready` (`:157-166`).
  - Clips start on the first frame after `ready`: `startedAt ??= now` (`:212`). Each frame samples
    `now - startedAt` (`:217-222`).
- `disappearAnimation` is **never** turned into a clip on the client. It only appears in the
  "has anything" check at `combatEffects.ts:80`. [V]

### 1.3 Who spawns what (per category)

| Category | Client-spawned (on the effect's own record) | Server-spawned `visual` (separate ground effect, clip in `appearAnimation`) |
|---|---|---|
| **(a) Character effect, rounds ≥ 1** | appear (once, new id) + static loop + static art at the target's hex | appear `visual` at the target's **pre-action** hex when `isNew` (`process.ts:1650-1665`, coords from `:1395-1396`). Disappear `visual` when it expires (`:1670-1684`). |
| (a′) the four damage-modifier tags (`increase/decreasedamagegiven/taken`) | as (a). `decrease*` versions are hidden (§5.1) | **none**. They skip `applySingleEffect` (`process.ts:657-723`, carried forward at `:727-739`) |
| **(b) Ground effect, rounds ≥ 1** | appear + static loop + static art at its hex | appear `visual` on the same hex when `isNew` (`process.ts:432-442`). Disappear `visual` on expiry (`process.ts:300-309` in `expireGroundEffects`, or `:448-458`) |
| (b′) Ground effect, rounds 0 (instant) | **nothing**. It is dropped before the snapshot (`process.ts:445-458`) | appear `visual` **and** disappear `visual` (if set) in the same snapshot, so they play simultaneously |
| (b″) Ground effect on an occupied hex | — | plus a `fromGround` copy is pushed to the occupant (`process.ts:398-415`). On the cast round it spawns another appear `visual` at the occupant (§4.1). It spawns a disappear `visual` on every effect pass while they stand there (§5.3). |
| **(c) `visual`** | appear only (its only field). No static. Lives until the round moves on. Never replays (same id) | created by `getVisualOrSound` (`process.ts:193-220`), `rounds: 0`, new nanoid |
| **(d) damage / pierce / heal one-shots** (rounds 0, character target) | nothing (not persisted) | appear `visual` at the target. No floating numbers exist anywhere in the canvas (§1.4) |
| **(e) Summons** | appear (once) + static on the summon ground effect, at the **spawn hex** | **none**: `summon()` clears `isNew` before the appear check (`tags.ts:3190-3191` vs `process.ts:432`). Expiry disappear `visual` at the **spawn hex** (`process.ts:296-309`). Clones die with `ID_ANIMATION_SMOKE` (`process.ts:1232-1254`, non-originals only) |
| **(f) Movement / redirection** | effect clips on a character **snap** to the new hex at once. The fighter **walks** there (§2.6) | any `visual` from the moving cast sits at the **old** hex (`curTarget` = pre-action state, `process.ts:1387,1395`) |

Default art: basic attack uses `ID_ANIMATION_HIT`, basic heals use `ID_ANIMATION_HEAL`
(`actions.ts:537`, `:624`, `:654`). Clone death uses `ID_ANIMATION_SMOKE`
(`app/drizzle/constants.ts:2528-2530`). Authored jutsu damage gets **no** default hit art. [V]

### 1.4 Damage numbers

There are none on the battlefield. The only `Text` in the combat scene is the grid label
(`scenes/combat.ts:96-108`). Damage and heal show up as combat-log rows (`hooks/combat.ts:79-181`)
and as instant HP-bar changes (`primitives/statusMeter.ts:37-43`, no tween). HP bars are visible only
for the selected or hovered fighter (`combatActors.ts:288-292`). [V]

---

## 2. Timing

### 2.1 Clip duration

- `assetAnimationClip`: `frameCount = max(1, asset.frames)`, `frameDurationMs = max(1, asset.speed)`.
  The sheet is **one column, `frames` rows** (`app/src/libs/rendering/animation.ts:25-35`). Each
  frame is `sourceHeight / frames` tall (`primitives/animation.ts:22-36`). [V]
- One-shot length = `frames × speed` ms. Frame index = `floor(elapsed / speed)`, held on the last
  frame until `elapsed ≥ frames × speed`, then hidden and disposed (`animation.ts:9-22`,
  `primitives/animation.ts:78-87`, `combatEffects.ts:217-222`). At 50 ms × 20 frames that is 1.0 s.
  [V]
- Loops repeat `step % count` forever (`animation.ts:19`). [V]
- Elapsed time is the **scene clock**: the sum of frame deltas, each **capped at 100 ms**, and reset
  to 0 after a pause (`runtime.ts:79-98`, `scenes/combat.ts:272-275`). Below 10 fps, clips play
  slower than real time. In a hidden tab the clock stops and resumes where it was. [V]
- `prefers-reduced-motion`: every clip holds frame 0. One-shots still expire on schedule
  (`animation.ts:8-21`). [V]

### 2.2 Blocking and overlap

Nothing blocks. Clips do not wait for each other, for fighter movement, or for earlier actions. The
only deferral is **sound**: effect SFX are queued while any fighter is walking and flushed 50 ms after
movement stops (`combatEffects.ts:35-41`, `:202-209`). **Clips are not deferred.** So an impact clip
can play on a target that has not yet walked into a pulled position (see 2.6). [V]

### 2.3 Several actions in one update

All new records from every action in the snapshot are created in the same `sync`. Each one starts
on the first frame after **its own** assets load. In practice that is **all at once**, give or take
a texture-load difference. The combat log gets all rows at the same moment. Intermediate states inside
a chain are never drawn. Example: a character effect added and removed within the same 5-step chain
is never seen, but its server `visual`s survive and play. [V]

### 2.4 First-use lag

`extraState.textureAssets` lists animation ids from the effects currently in the battle and from the
viewer's own or revealed jutsu and items (`util.ts:1727-1745`, `:1856-1870`). Boss jutsu are added
only after first use (`revealedActions`). When the list gains an id, the asset query re-keys and
keeps the old data as placeholder (`Combat.tsx:275-299`). `requestedIds` stays stale, `known` is
false, and **effect sync is skipped** (`scenes/combat.ts:191-199`) until the fetch returns. Fighters
(`:166-171`) already update. Then the texture itself loads before `ready`. Expect the first cast of
each new animation in a battle to appear late, after the fighter and HP change. [V mechanism; the
delay is network-bound, I]

### 2.5 Static loop lifetime and round counting

- Round progression: an actor's turn ends on AP exhaustion or a 60 s timeout. The next actor follows
  `usersState` order. The round advances when every live user has had a turn
  (`actions.ts:1673-1733`, `COMBAT_SECONDS = 60` at `app/src/libs/combat/constants.ts:27`). [V]
- On each round advance, effects **not** `castThisRound` lose 1 round. `castThisRound` and `isNew`
  are then cleared (`util.ts:3035-3061`). Effects cast in the round that is ending are **not**
  decremented on that first advance. Ground effects at 0 are removed in the same step
  (`expireGroundEffects`, `util.ts:3070`, `process.ts:285-314`), and a disappear `visual` is
  spawned. [V]
- So a **rounds:1** effect cast in round N survives the N→N+1 advance (still 1). It is decremented
  to 0 at N+1→N+2. Visible span: **rest of round N + all of round N+1**. "1-round effects last the
  whole player turn" is true, and they actually last longer than that. [V]
- Character effects at 0 are dropped by the next effect pass (`process.ts:1667-1684`). If the round
  advanced in the final `alignBattle` of a request with no action after it, the 0-round effect stays
  in the snapshot. The client still draws it, because the client never checks `rounds`
  (`combatEffects.ts:42-195`). It goes away with the next action or poll tick. [I: traced for the
  common path only]
- Static loops start with the appear (§0.2) and stop when the id leaves the snapshot. Nothing fades
  out. [V]

### 2.6 Movement

Fighters walk the shortest hex path. Speed per second = `tile.width × 6 × ease`, where
`ease ∈ [0.35, 1]` (`combatActors.ts:157-162`, `:256-287`). That works out to about 0.1–0.2 s per
hex [I: arithmetic]. Effects on that fighter jump to the destination at once, because they use the
state position (`combatEffects.ts:59-66`, `:188`). Redirection (`tags.ts:2892+`) and move
(`tags.ts:2407-2445`) both just rewrite `longitude/latitude`. A pull is drawn as the target
*walking* along a path, not as a straight slide. [V]

---

## 3. Geometry and layering

### 3.1 Sizes

- Hex: `hexSize = canvasWidth / (W − 0.25·(W−1))` (`scenes/combatTerrain.ts:25-32`). Tile box =
  `hexSize × 0.5·hexSize` (flat hex, `util.ts:1010-1019`; `HEX_ASPECT_RATIO = 0.5`,
  `app/drizzle/constants.ts:956-957`). [V]
- **Clips** (appear, static loop, `visual`): a square of `tile.height × 2.5`
  (`EFFECT_ANIMATION_HEX_RATIO`, `animation.ts:75-76`, used at `combatEffects.ts:120`). That is
  1.25 hex widths. The anchor is the centre, at the tile-local point (w/2, h/2)
  (`combatEffects.ts:124`, `primitives/animation.ts:62`). Width and height are both forced to the
  same value (`primitives/animation.ts:63-64`), so **non-square frames are distorted**. There is no
  per-asset or per-effect scale or offset. [V]
- **Static art** (`staticAssetPath`): width = `tile.width`, height = `tile.height`, centred at the
  same point. It is a 2:1 box, so square art gets squashed (`combatEffects.ts:135-145`,
  `sprites.ts:72-77`). [V]
- Fighter reference (tile-local, y up): AI originals (bosses, summons) draw a `1.6h` avatar centred
  at `y = 0.9h` (`combatActors.ts:358-363`). Players draw a pin marker `1.2h` and avatar `0.8h` near
  `y = 0.9–1.0h` (`:366-383`). A clip centred at `0.5h` and spanning `−0.75h…1.75h` covers the
  whole AI avatar and extends about 0.85h **below** its feet. Aim the visual centre of character
  clips about 15% above the frame centre to sit on the body. [V geometry; I aesthetic]
- Worked example [I]: an 11-wide battle on a 400 px phone canvas gives hex 47×23.5 px and clip
  ≈59 px. On a 1000 px desktop canvas, hex is 118×59 px and clip ≈147 px. Zoom goes up to 3×
  (`scenes/combat.ts:119`, `:154`). A 50 px source is therefore shown at about 1.2×–9×.

### 3.2 Z-order (back to front)

`terrain → effects.ground (static art) → highlight outlines → grid labels → scenery → fighters
(shadow, threat halo, avatar/marker, HP/SP/CP meters) → effects.container (all clips)`
(`scenes/combat.ts:109-117`; actor internals `combatActors.ts:90`, `:106-108`). [V]

- All clips draw over every fighter, portrait, tombstone and HP bar. All static art draws under
  them. [V]
- Within one effect record: static loop (zIndex 2) over appear (zIndex 1) (`combatEffects.ts:125`).
  The barrier meter is zIndex 3 (`:174`). [V]
- Between records: **creation order** (`container.addChild` at `combatEffects.ts:91`). Roots are not
  sorted, so newer effects draw on top. Within one sync, ground effects are created before user
  effects (`:55-66`). [V]
- Fighters are y-sorted among themselves only (`combatActors.ts:294-297`). [V]
- The DOM UI (log, resource bars, action bar) sits outside the canvas and is never covered. [V]

### 3.3 Stacking on one hex or character

No cap, no offset, no merge. Every effect with art is its own record at the identical centre and
size. N effects on a boss means N loops overdrawn (`combatEffects.ts:85-128`). Tag stacking is
globally on (`BATTLE_TAG_STACKING = true`, `app/drizzle/constants.ts:1968`;
`util.ts:1352-1358`), so re-casts add new ids. Each brings another appear and another loop, out of
phase with the old one. [V]

### 3.4 Texture source, rendition and filtering

- Clip textures: `game.assets.texture(url, options.rendition ?? 50, nearest ? "nearest" :
  "linear")` (`primitives/animation.ts:11-19`). Combat effects never pass `rendition` or `nearest`
  (`combatEffects.ts:116-122`), so the result is **50 px, linear**. Static art uses the same
  defaults (`sprites.ts:50-55`, `assets.ts:31`). [V]
- `textureImageUrl` adds `?width=50` **only** for Bunny hosts (`uploadthing.b-cdn.net`,
  `tnr-storage-cdn.b-cdn.net`). Legacy `utfs.io` and `ui0arpl8sm.ufs.sh` are rewritten to Bunny
  first (`app/src/utils/image.ts:10-11`, `:22-33`, `:55-63`). Images on any other host load at
  native size. [V]
- Bunny scales the **whole strip** to 50 px wide. A 100×2000 strip with 20 frames becomes
  50×1000 (frames 50×50) [I: CDN behaviour]. Detail finer than 1/50 of the frame width is lost,
  then upscaled with linear blur.
- Sampling: `Assets.load(..., { scaleMode: "linear" })` (`assets.ts:7-16`). The renderer runs at
  `resolution: 1`, `antialias: false`, WebGL1 preferred (`runtime.ts:33-46`). The canvas is CSS-sized
  to 100% width, so high-DPI screens get a further browser upscale [I]. Mipmaps are not requested
  anywhere in this path [V]. Pixi 8.22 does not generate them by default [I]. At 50 px, minification
  is rare anyway.
- Frames are cut by exact pixel rectangles from the resized strip (`primitives/animation.ts:26-35`).
  With linear filtering, neighbouring frames can **bleed** 1 px at frame edges [I]. Keep a 1–2 px
  transparent margin at the top and bottom of every frame.
- Effect sprites are flipped twice (sprite `scale.y *= -1`, world `scale.y = -s`), so the image is
  upright as authored (`primitives/animation.ts:65`, `scenes/combat.ts:134`). [V]

---

## 4. Turn-flow walkthrough (Mother of Echoes pattern)

Assume turn order Sayo → The Silence → Feeler → player (the real order is `usersState` initiative
order, `tags.ts:3313-3319` for summons). The player clicks once per turn, and the AI chain fits in
≤5 steps. Otherwise it continues on 1 s polls (§1.1).

### Round N

1. **Player's previous click resolves; Sayo casts the mark pattern** (ground cast, rounds:1,
   `increaseregeneration` carrier, appear + static). One mark ground effect is created per pattern
   hex (`actions.ts:1063-1112`). In `applyEffects` each new mark (`isNew`):
   - spawns an appear `visual` on its hex (`process.ts:432-442`);
   - is kept, with `isNew` now false (`:445-447`);
   - if a fighter stands on it, pushes a `fromGround` copy that still has `isNew = true`
     (`process.ts:398-415`). That copy goes through `applySingleEffect` and spawns **another** appear
     `visual` at the occupant (`:1650-1665`). The log says "marked the ground with … for the next 1
     rounds" (`:391-396`).
2. **The Silence and Feeler act** in the same request. The marks stay (rounds 1, `castThisRound`).
   Each extra effect pass re-runs the occupant copy (§5.3).
3. **Snapshot arrives** (one response, ≤5 steps). For every marked hex the client creates the mark
   record: client appear + static loop + static art (`combatEffects.ts:129-156`), plus the server
   appear `visual` record. **Result: appear ×2 on empty marked hexes, ×3 on occupied ones**, all
   starting together with the static loop drawn on top. Silence's and Feeler's clips start at the
   same moment. Nothing shows "Sayo first, then Silence". [V]
4. **Player's turn (round N)**. The marks are visible as static loops for the whole turn, up to the
   60 s timer.

### Round N+1

5. Round advance (inside the request after the player acts). Marks are **not** decremented because
   they were `castThisRound` (`util.ts:3044-3049`). They stay at rounds 1.
6. **Sayo casts the eruption** (ground cast, flat `pierce`, rounds 0) on the marked hexes. For each
   hex: an appear `visual` (`process.ts:432-442`). The pierce ground effect itself is **not** kept
   (`:445-458`), so it gets no client record. If the eruption tag has a `disappearAnimation`, it
   spawns **at the same time** as its appear. On occupied hexes the instant `fromGround` copy
   (`rounds: 0`, `isNew`) deals the damage and spawns a second appear `visual` at the occupant.
   **Eruption appear: ×1 on empty hexes, ×2 on occupied hexes.** [V]
7. **The marks do not disappear here.** They are still at rounds 1 and keep looping **underneath**
   the eruption, because the eruption `visual` records are newer and draw on top. They stay through
   the rest of round N+1, including the player's N+1 turn. [V]
8. **Damage feedback**: no numbers. HP bars change instantly if visible. The log gets rows like
   "X takes N damage". [V]

### Round N+2

9. On the N+1→N+2 advance, marks go 1→0 and `expireGroundEffects` removes them. If they have
   `disappearAnimation`, a `visual` is spawned per hex (`process.ts:300-309`). The client destroys
   the mark record at once (`combatEffects.ts:49-53`), so the loop cuts out on whatever frame it was
   on. The disappear `visual` then plays once. [V]

**Design consequence.** To make the mark vanish *at* the eruption, do not rely on rounds:1. The
engine offers no "consume the mark" hook for that. Options: accept the overlap (make the eruption
read clearly over the loop), or author the mark as rounds:0 (not viable: a rounds:0 ground effect is
dropped on cast and never loops), or accept a one-round linger. This is a content decision. It is not
settled here.

### 4.1 Character-target cast whose pattern includes empty hexes

In the user-effect branch an effect is pushed only when a valid occupant exists (`actions.ts:1125-1159`,
gated `target && …` at `:1141`). Empty pattern hexes get **no effect and no animation**. The
exceptions are tags with `target: "SELF"`, which go to the caster, and barrier-damage tags, which hit
a barrier on that hex (`:1168-1208`). [V]

### 4.2 Per-effect `COORDINATES` mosaic

A tag with `target: "COORDINATES"` takes the **ground** branch even inside a character cast
(`actions.ts:1067-1071`). It is stamped on each tile in **its own** resolved tile set,
`effectTiles[tagIndex]` (`:1063-1065`), whether or not the tile is occupied (`:1096-1112`). So each
tag's art draws only on that tag's hexes. A mosaic works. Each piece is a normal ground effect, so
the duplication rules apply: rounds ≥1 pieces show appear ×2 (×3 if occupied) plus their loop.
Rounds 0 pieces show appear ×1 (×2 if occupied), and their disappear fires at the same time. Each
piece is its own record, so pieces painted in one cast start within a texture-load of each other.
They are not frame-locked. [V; frame-locking I]

---

## 5. Constraints and gotchas

### 5.1 Invisible effects (`power <= 0` = "depleted")

The client hides a record whose `power` is defined and `<= 0` (`combatEffects.ts:183-187`, `:215`).
It also plays `disappearSfx` right away (`:184-185`). These handlers set
`effect.power = -Math.abs(effect.power)` on the persisted user effect, at cast:

- `decreaseStats` (`tags.ts:847`)
- `decreaseMastery` (`:892`)
- `decreaseDamageGiven` (`:977`; also `process.ts:692`)
- `decreaseDamageTaken` (`:1062`; also `process.ts:710`)
- `decreaseHealGiven` (`:1173`)
- `decreasepoolcost` (`:1816`)

**Any appear, static loop or static art attached to these tags on a character never shows.** The
server appear `visual` still plays, once, for the types that pass through `applySingleEffect`. Damage
modifiers get no `visual` (§1.3), so `decreasedamagetaken` and `decreasedamagegiven` show
**nothing at all**. Shields and barriers whose power drains to 0 hide the same way. Workaround: put
the boss's loop on a different, visible carrier tag (one whose power stays positive) in the same
cast. [V]

### 5.2 Hidden assets and missing art

- Battle asset fetch: `fetchGameAssets(... hidden = false ...)` (`app/src/queries/misc.ts:28-36`,
  called from `routers/misc.ts:101-106`). `hidden` defaults to **true** (`app/drizzle/schema.ts:171`).
  A hidden asset is not in `assets`, so `addClip` returns silently (`combatEffects.ts:113-114`).
  There is no error and no placeholder. [V]
- Failed texture loads are logged and the record still becomes ready without that clip
  (`combatEffects.ts:157-163`). [V]

### 5.3 Ground effects with `disappearAnimation` spam it on occupants

A ground effect's `fromGround` copy has `fromGround: true`. So
`(isEffectActive && !fromGround) || visual` is false, and the `else if (disappearAnimation…)` branch
runs (`process.ts:1667-1684`). The result: **every effect pass while someone stands on a lingering
pool or mark spawns that tag's disappear clip on them.** Effect passes run on every action. Only author
`disappearAnimation` on ground tags that nobody can stand on, or accept repeated "pops". The copy's
coordinates come from the occupant (`:1395-1396`). [V code path; repetition rate per action I]

### 5.4 Row/column 0 drop disappear `visual`s for character effects

The disappear `visual` for user effects is gated on `longitude && latitude` being truthy
(`process.ts:1670-1674`). A character standing in **column 0 or row 0** gets no disappear clip. The
appear path checks `!== undefined` (`:1653-1654`) and is not affected. [V]

### 5.5 Frame and size limits

- `frames` 1–100, `speed` 1–100 ms/frame (`app/src/validators/asset.ts:8-9`; DB `tinyint`,
  `schema.ts:169-170`). The maximum one-shot is 10 s. 50 ms × N frames gives N/20 s. [V]
- Strip height at the 50 px rendition is about `50 × frames` px (square frames). 100 frames is
  5000 px. That is above `MAX_TEXTURE_SIZE = 4096` on some mobile GPUs, and WebGL1 is preferred
  (`runtime.ts:36`). Keep strips ≤ about 80 frames (≤4096 px) [I: device-dependent].
- Everything outside the 2.5h square is cut off, because the sprite is the frame. Art that needs to
  reach beyond one hex ring (2.5h ≈ 1.25 hex widths) cannot. Splash larger areas as per-hex pieces
  (§4.2). [V]
- The battlefield canvas clips at its edges, so edge-hex clips are cropped. [I]

### 5.6 Performance

There is no sprite cap. Each clip is one sprite with per-frame texture views over one shared decoded
source (`primitives/animation.ts:6-46`). Idle decoded textures are kept up to 16 MB / 64 entries
(`assets.ts:5-20`, `leaseCache.ts:58-90`). A 7-hex mark with appear×2 and loop is about 21 sprites.
That is cheap [I]. Async load time per new id is the real cost (§2.4).

### 5.7 Desync sources (summary)

| Symptom | Cause |
|---|---|
| Clip plays before the target finishes walking | clips are never deferred; only SFX are (§2.2) |
| Impact at the old hex after a pull | server `visual` uses the pre-action position (§1.3 f) |
| Static loop jumps ahead of the fighter | effect records use state position (§2.6) |
| All of round N's AI actions flash at once | single snapshot per ≤5 steps (§2.3) |
| First cast of a jutsu appears late | asset-list refetch gate (§2.4) |
| Mark still visible during eruption | rounds:1 lifetime (§2.5, §4) |
| Appear looks brighter or doubled | client + server appear (§0.4) |
| Loop cuts mid-frame on expiry | record destroyed with no fade (§1.2) |
| Battle-ending blow not animated | scene disabled when `result` is set (`Combat.tsx:1038`, `app/src/hooks/game-scene.ts:16,26`) |
| Reloading mid-fight shows no appears | initial sync skips appears (`combatEffects.ts:155`, `scenes/combat.ts:198`) |
| Summon loop stays behind when summon moves | summon effect anchored at spawn hex (`process.ts:364-374`) |
| Clone/summon death | clones: smoke `visual`. Summons are `isOriginal` (`tags.ts:3233-3237`): no smoke, a tombstone instead (`combatActors.ts:182-183`, `:400`) |
| Initial battlefield rocks | 10% of empty hexes get a `barrier` with static art at start (`routers/combat.ts:3019-3050`). Marks on those hexes overdraw them |

---

## 6. Assumption check (as supplied)

| Assumption | Verdict |
|---|---|
| Appear and static start together | **Confirmed.** Same `startedAt`. Static draws **over** the appear (z 2 > 1). |
| 1-round effects last the whole player turn | **Confirmed, and they last longer:** the rest of the cast round plus all of the next round. |
| The client never plays disappearAnimation; the server spawns it as a separate visual | **Confirmed.** Caveats: none for the four damage modifiers, none in column/row 0 for character effects, and it repeats on occupants of ground effects (§5.3, §5.4). |
| Ground-mark appear plays twice | **Confirmed, and worse:** ×2 on empty hexes, ×3 on occupied hexes. Character effects with rounds ≥1 also double. Instant ground hits ×1, or ×2 if occupied. |
| All clips draw over fighters and HP bars | **Confirmed** for clips. `staticAssetPath` art is **under** fighters, scenery and highlights. |
| Linear filtering, 50 px rendition | **Confirmed** for Bunny-hosted images. Other hosts load at native size. Clips are forced square; static art is stretched to 2:1. |
