# Implementation Handoff — One Perfect Crop hidden core manifest

**Repository:** `perseverance484/tnr-tools`
**Branch:** `claude/one-perfect-crop-manifest-9wsry6` (Fable-owned implementation branch, assigned for this task)
**Base SHA:** `e35633160bdb7bb03238e30c22faf9f2b4af057c` (live `main` at session start)
**Head SHA:** the tip of this branch at handoff; FROZEN until independent review returns
**Integration target:** `main`
**Workstream / task:** `one_perfect_crop` / `build.manifest`
**Contract:** `state/prompt_one_perfect_crop.md`, governed by `state/one_perfect_crop_core_manifest_override.md` (ruling `RUL-2026-09-16-001`)
**Live requests / game writes / session credentials:** NONE. See section 6.

## 1. Objective

Build the validator-clean **hidden core manifest** for One Perfect Crop: two new AI records, their two AiProfiles and the quest, with the frozen prose/graph and combat contract implemented exactly, and with art and content-admin values deliberately left deferred.

The brief names `main @ 6e09b15bb6f3d1c90ba416d14211b533f5b4a367` as its freeze baseline. Live `main` has advanced since; this work was reconstructed from live `main` at the base SHA above, and none of the intervening commits touch the frozen sources this build reads.

## 2. Changed files

| File | Change |
|---|---|
| `push/47_one_perfect_crop_core_manifest.json` | NEW. The manifest. 5 entries, 36 objectives. |
| `push/47_one_perfect_crop_core_manifest.gen.py` | NEW. Its generator, with the handoff checklist executed as assertions. |
| `skills/building-tnr-content/scripts/validate.py` | Law 41 scoped to `includeDefaultRules: false`, as the law text reads. See section 5. |
| `skills/building-tnr-content/scripts/factory.py` | `objective()`'s first parameter renamed `task` -> `member` so a shared-schema member (`InstantWinLoseObjective`) can be built with its own `task` enum value. No behaviour change; every existing call passes it positionally. |
| `skills/building-tnr-content/12b_LAWS_coverage.md` | Law 41 coverage row corrected to match the scoped check. |
| `state/workstreams/one_perfect_crop/roadmap.json` + rendered `ROADMAP.md` / `INDEX.md` | `build.manifest` COMPLETE with evidence; `review.manifest` READY. |
| `docs/handoffs/ONE_PERFECT_CROP_CORE_MANIFEST_HANDOFF.md` | This file. |

## 3. What the manifest contains

Five creates, in build order, nothing else:

1. `ai` **Road Bandit** — `srcId: opc_ai_road_bandit`
2. `ai` **Harvest Boar** — `srcId: opc_ai_harvest_boar`
3. `aiProfile` **Road Bandit AiProfile** — `targetId: @ai:opc_ai_road_bandit`
4. `aiProfile` **Harvest Boar AiProfile** — `targetId: @ai:opc_ai_harvest_boar`
5. `quest` **One Perfect Crop** — `questType: event`, 36 objectives

Top level carries `dedupNames: true` and nothing else. No `imgSizes`, no `capture` block, no `skipPreflight`.

Nothing is transcribed by hand. Node text and choice routing are parsed out of `state/one_perfect_crop_prose_graph.md` at generation time; jutsu ids and their distance gates are resolved from pool codes through `32b_DATA_pool.json`; AI records are built by `enemy.py` from its ratified role defaults; rule objects, objective nodes and the quest entry are built by `factory.py` from `45c`/`45d`/`45g`.

### Combat contract (`state/one_perfect_crop_combat_spec.md`)

Both AI: rank `JONIN`, level `100`, `regeneration: 60`, `statsMultiplier: 1`, `poolsMultiplier: 1`, element `None`, neutral even twelve-stat ratio (all twelve at 100), `preferredGeneral1: Strength`, `preferredGeneral2: Speed`, no passive effects/tags, no avatar, no armor/items field. Road Bandit `preferredStat: Bukijutsu`, Harvest Boar `preferredStat: Taijutsu`.

Kits are the literal existing shared-pool ids, in the frozen order:

- Road Bandit — S27 `YiRdVytsdxFzZtqkEDs5Q`, S41 `fKvCGRgzGNskgFWocQCAg`, S40 `kkGDat1XWUxhOQ1_T5025`
- Harvest Boar — S27 `YiRdVytsdxFzZtqkEDs5Q`, S42 `4TM6iS8P0qgNHsFpALFhg`, S41 `fKvCGRgzGNskgFWocQCAg`

Each AiProfile carries `includeDefaultRules: true` and exactly three authored rules in the frozen order, each a `distance_lower_than` gate at `6` (pool range 5 + 1, law 40) into `use_specific_jutsu`. No movement, highest-power or anti-exhaust rule is authored: the engine-appended default tail owns those cases, per the director ruling in the combat spec.

Behaviour lives only on the AiProfile entries, not duplicated onto the AI entries, so the two cannot drift. The builder's `ai` phase saves the record, then its `aiProfile` phase resolves `@ai:<srcId>` -> `profile.getAi` -> `ai.toggleAiProfile` -> `ai.updateAiProfile`.

### Quest contract (`state/one_perfect_crop_prose_graph.md`)

36 objectives, in the frozen order, one start (`opc_o0`), acyclic, no dangling edge. All 27 frozen description blocks and every choice line are byte-verbatim from the frozen file. `consecutiveObjectives: true` at data level and absent from `content` (laws 23, 37). Zero-travel: no node carries `sectorType`, `locationType`, `sector`, `longitude` or `latitude`.

PASS spine `opc_o0 -> opc_g1 -> opc_g2 -> opc_g3 -> opc_g4 -> opc_c1 -> Harvest Boar -> opc_d1..opc_d5 -> opc_win`, with sealed F1-F4 wings and six `fail_quest` terminals (four wings plus one per battle loss). No failure branch rejoins the PASS spine.

Both encounters are dialog-gated `start_battle` (never `defeat_opponents`), one enemy each, `opponent_scaled_to_user: true`, `completionOutcome: "Win"`, `keepOriginalPools: false`. Road Bandit loss hard-routes to `opc_f2_battle_fail`, Harvest Boar loss to `opc_c1_fail`; both are `fail_quest`. No `reset_quest` node and no `resetObjectiveId` exists anywhere: there is no authored retry route.

Delivery acceptance (`opc_d2`, "Shipment accepted") precedes the catastrophe (`opc_d4`, "MY CABBAGES!"), which precedes `opc_win`. Every dialog forward link is a choice array, including single-entry continuations. No em or en dash appears in any player-facing text.

## 4. Deferred: create-path defaults and placeholders

Everything below is a deliberate hole, per the 2026-09-16 override. **None of it is accepted content.** Launch finalization must fill or explicitly accept each one before any publish/unhide decision.

| Field / area | State in this manifest | Owner |
|---|---|---|
| Quest `description` | `null` (schema-nullable; the create-path "unset"). No listing blurb is invented. | launch finalization / user |
| Quest `image` (listing icon) | key absent; the create path keeps its own default. No `@img`. | `art.icons` |
| `content.sceneBackground` / `sceneCharacters` and every node's scene fields | constructor defaults (`""` / `[]`). No background or character id is authored, because the scene family's characters are assets this build may not create; half-wiring it would be art work in a build that defers art. | `art.scene_characters`, `art.backgrounds` |
| Node `image` | constructor default `""`. Dialog nodes draw no map pin (laws 52, 53). | `art.icons` |
| AI avatars | no `avatar` key on either AI. | `art.combat_avatars` |
| Equipped armor | no `items`/armor field; a fresh AI owns nothing, which is the spec's `None`. Armor is an editor-side equip, not a payload field. | launch finalization |
| `content.reward` | `{}`. No Ryo, XP, tokens or item grant. | `admin.balance_and_eligibility` |
| Objective-level reward blocks | absent. The generated objective contract (`45c` `AllObjectives`) carries no reward fields, so nothing mechanical is authored and nothing is guessed. Live records carry a 27-key zero block written by the in-game editor; that shape is not part of the write validator. | `admin.balance_and_eligibility` |
| Cabbage Seed item and its reward grant | absent entirely. The frozen graph's `guaranteed reward item: Cabbage Seed x1` is deferred by override clause 4. | `admin.balance_and_eligibility` |
| `maxAttempts`, `maxCompletes`, `retryDelay`, `attemptDelay` | keys absent; create-path defaults stand. No repeatability policy is chosen. | `admin.balance_and_eligibility` |
| `requiredLevel`, `maxLevel`, `questRank`, `requiredVillage`, `prerequisiteQuestId`, `medicalRank`, `huntingRank`, `gatheringRank` | keys absent. In particular the submitted `Farming level 15` requirement is NOT translated to character `requiredLevel: 15` and no substitute gate is invented. | `admin.balance_and_eligibility` |
| `startsAt`, `endsAt`, `tierLevel` | `null` (schema-required, nullable). No launch window is chosen. | launch finalization |

Quest `successDescription` is the one piece of completion prose the frozen graph supplies, reused verbatim rather than paraphrased into a second line; it is also the `opc_win` node's `successDescription`.

## 5. Deliberate tooling change: law 41

`validate.py` rejected any rule chain whose final rule was conditional. `docs/ENGINE_LAWS.md` law 41 is scoped: *"With `includeDefaultRules: false` the final rule must be unconditional."* With the flag true the engine appends its own catch-all tail (highest-power legal action, then movement) after the authored chain, and that tail is the terminator. The builder's own preflight (`rulesBad()` in `builder_bundle.js`) carries no terminal check at all, so the container was stricter than both the law and the browser.

The combat spec requires exactly three gated rules with `includeDefaultRules: true` and forbids an authored fallback, and the brief forbids `skipPreflight`, so this was the only path to 0 errors that does not break the frozen contract. The check is now skipped only when the entry's `includeDefaultRules` is exactly `true`. The dead-rule check (an unconditional terminal rule *above* the end) stays unconditional, because it is true either way. `12b_LAWS_coverage.md` row 41 records the correction.

`--parity` still reports the same 16 checks on both sides: the check inventory is unchanged, only its scope.

## 6. Verification — exact commands and results

Run from the repository root unless noted.

```
python3 scripts/content_workstream.py init one_perfect_crop --task build.manifest
  -> packet printed; task READY, dependency build.final_freeze COMPLETE

python3 push/47_one_perfect_crop_core_manifest.gen.py
  -> push/47_one_perfect_crop_core_manifest.json: 5 entries, 36 objectives
     (the generator's own verify() assertions all pass or it does not write)

python3 skills/building-tnr-content/scripts/validate.py \
    push/47_one_perfect_crop_core_manifest.json \
    --ctors 45c_DATA_constructors.json \
    --entities skills/building-tnr-content/data/45d_DATA_entity_schemas.json \
    --checks 45g_DATA_checks.json \
    --lints skills/building-tnr-content/data/45h_DATA_lints.json \
    --pool 32b_DATA_pool.json
  -> 0 errors, 2 warnings   (exit 0)
     warn [ai:Road Bandit]  kit is all 60 AP actions and no 40 AP stance
     warn [ai:Harvest Boar] kit is all 60 AP actions and no 40 AP stance
     plus 4 notes: quest description / startsAt / endsAt / tierLevel explicit null is ACCEPTED

python3 skills/building-tnr-content/scripts/validate.py \
    --parity harvests/inbox/tnr_results_1789189076617.json  (builder v4.32 inventory)
  -> builder and validator implement the same 16 checks; 0 errors, 0 warnings (exit 0)

python3 skills/building-tnr-content/scripts/validate.py --laws
  -> laws 9, 10, 11, 12: 4 asserted, 0 failed (exit 0)

python3 ../scripts/factory.py --selftest   (cwd skills/building-tnr-content/data)
  -> 20/20 passed (exit 0)

python3 skills/building-tnr-content/scripts/selfcheck.py \
    --generated skills/building-tnr-content/data
  -> 29 bundled scripts parse; source git:studie-tech/TheNinjaRPG@bdec2883;
     factory selftest 20/20; validate.py consumes 16/16 declared 45g blocks; 0 errors (exit 0)

python3 skills/building-tnr-content/scripts/lawmap.py
  -> 93 laws, 93 matrix rows, 77 citations across 35 files; 0 errors, 5 warnings (exit 0)
     the same 5 pre-existing warnings the board already records (laws 16d, 18, 37, 61, 69)

python3 skills/building-tnr-content/scripts/doctrinemap.py
  -> 21 assertions, 18 referenced, 16 surfaces; 0 errors, 0 warnings (exit 0)

python3 skills/building-tnr-content/scripts/render_doctrine.py --check
  -> all projections current (exit 0)

python3 skills/building-tnr-content/scripts/build_packs.py --check
  -> all packs and TOCs current (exit 0)

python3 scripts/content_workstream.py validate --all   /   render --all
  -> see the commit that updates the roadmap
```

Plus a 74-assertion independent audit of the produced JSON, written against the brief's checklist rather than against the generator, covering entry inventory, hidden-on-create, ref resolution, the full combat contract against the combat-spec text, and the full quest graph. All passed. Its assertions are reproduced in the generator's `verify()` so they re-run on every regeneration.

### The two warnings

`kit is all 60 AP actions and no 40 AP stance` on both AI. This is the ruled-on shape, not an oversight: the combat spec fixes the kits at three 60 AP pool attacks and states the consequence explicitly, resolving it through `includeDefaultRules: true` rather than a bespoke exhaustion branch. Changing it would mean minting a stance jutsu, which the brief forbids.

## 7. Source and provenance

- Game source behind every generated contract used here: `git:studie-tech/TheNinjaRPG@bdec2883` (2026-08-29). `45c` extracted 2026-08-30; `45d`, `45e`, `45g` extracted 2026-09-09. Root and skill copies of `45c`/`45g` are byte-identical (md5 checked).
- No generated contract was regenerated, re-extracted or adopted in this task; all were consumed as stamped.
- Shared-jutsu ids and their gates come from `32b_DATA_pool.json`, which the bandit-resolution document independently verifies against the same four records.
- No capture or results bundle was produced. `harvests/inbox/tnr_results_1789189076617.json` was read only to supply the builder's check inventory for `--parity`.
- The manifest is deterministically reproducible: re-running the generator on an unchanged repository rewrites byte-identical JSON.

## 8. Known debt, deviations and things to attack

1. **`factory.rules()` is still unscoped for law 41.** The opt-in assembly helper refuses a chain whose last rule is conditional, with no `includeDefaultRules` context to consult. This build does not use it (rules are assembled with `factory.rule()` directly), so it was left alone rather than widened mid-task. It should be scoped the same way, or given the flag, in its own change.
2. **Node reward blocks are absent** where live records carry a 27-key zero block. The generated objective contract has no reward fields, so this follows the contract; if the reviewer reads the absence as a risk at push time, the fix is a zero block copied from a live capture, not authored values.
3. **Quest `description: null`** is a real hole in a player-facing record. It is deliberate (no frozen listing prose exists and inventing it is user-owned), but it is the single most likely thing a reviewer will want changed.
4. **`aiProfile` entries carry inert `name` and `hidden` keys.** The builder's aiProfile path sends only `rules` and `includeDefaultRules`, so both are dropped; they are present so the entries satisfy the create laws 16b and 36 like every other create. An alternative reading is that aiProfile entries should be exempt from those laws in `validate.py`; that would be a tooling change and was not made.
5. **The manifest has never been run**, so nothing here is read-back evidence. A green validator is not a live record.
6. **`opc_*` logical ids are used verbatim as engine objective ids**, which the frozen graph permits; none exceeds the id length used elsewhere in live content, but that was checked by construction, not against a live record.

## 9. Open user decisions

Every row in section 4 marked `admin.balance_and_eligibility`, plus final art acceptance, final listing copy, repeatability, eligibility, and the publish/unhide decision itself. `state/one_perfect_crop_content_admin_open.md` remains the authoritative list; nothing in it was resolved here.

## 10. Live-game statement

- No live request of any kind was made. Nothing in this task contacted `theninja-rpg.com`.
- No game write was made. The manifest is a file; only dauntless's tap can run it.
- No live session cookie, credential or token was obtained, requested, synthesised or exposed.
- No browser check, Forge run, preflight-panel check or hidden-state read-back was performed. Every result in section 6 is container-side.
- Every create is `hidden: true` and the manifest contains no publish, unhide or `hidden: false` path.

## 11. Not begun

- `review.manifest` — the independent ChatGPT audit of this exact SHA.
- `production.run_and_readback` — dauntless's Forge run and the fresh read-back.
- `launch.finalization` — final art, Cabbage Seed item, rewards, repeatability, eligibility, listing copy, scene wiring, and the separate publish decision.
- No art was produced, processed or QC'd. No `artpreflight.py` run was made.
