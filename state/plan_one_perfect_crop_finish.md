# One Perfect Crop — finish implementation plan

**Status:** execution underway; design/prose frozen, art intake partially processed, Road Bandit reuse probe staged; not yet a runnable manifest.  
**Plan owner:** ChatGPT / Content Designer.  
**Implementation owner:** Fable / Claude Code after final freeze.  
**Live-game actor:** dauntless only.  
**Current execution baseline:** `main` at/after `43523e489214a9b64fe88529b3ba68658cfe88bc`.

## Settled rulings carried into this plan

1. The route graph, prose, cast, encounter count, PASS/FAIL outcomes, delivery-before-catastrophe order, and final `MY CABBAGES!` beat are frozen.
2. Player-facing prose uses TNR scene formatting: passive narration/action in `<i>...</i>`, spoken text in quotes, dramatic beat spacing with literal `<br> <br>`, and choices quoted only when they are actually spoken.
3. F2 Road Bandit is now a dialog-gated **`start_battle`**, not `defeat_opponents`. It is an ambush and begins immediately when the player commits to the old road. This removes the previous location/sector/map-marker dependency.
4. C1 Harvest Boar remains dialog-gated **`start_battle`**.
5. Both battle losses hard-route to FAIL with no authored retry branch.
6. Balance/reward/rarity/repeatability/eligibility values that are still unresolved stay explicitly open for the content admin. Fable must not guess them into a runnable manifest.
7. Ittetsu design is accepted. The supplied 1024x1536 black-background source has been isolated locally and exported as `one_perfect_crop_ittetsu_scene.webp`, 341x512 RGBA lossless WebP, below the 450KB working ceiling. Do not redesign the character. Repo-native `artpreflight.py` remains required before production handoff.
8. The updated merchant/keeper design supplied by dauntless replaces the earlier suggestion to reuse `Forsworn Scene - Keeper`. It has been isolated locally and exported as `one_perfect_crop_waystation_keeper_scene.webp`, 341x512 RGBA lossless WebP, below the working ceiling. Treat it as the event's Waystation Keeper. Repo-native `artpreflight.py` remains required before production handoff.
9. The approved One Perfect Crop listing icon has been exported as `one_perfect_crop_quest_icon.webp`, 256x256 RGB lossless WebP, below the working ceiling. It is referenced directly by `quest.image` through `@img`; no gameAsset wrapper is needed for the listing icon.
10. `Nameless Ninja` is rejected for visual reuse as deprecated/below the current quality bar.
11. Do not edit shared live AI merely to make it fit this event.
12. Road Bandit reuse is being tested by `push/04_one_perfect_crop_bandit_ai_probe.json`, a five-read full-capture job with zero items/mutations.

## Target event shape

The event is deliberately **zero-travel**. Its authored gameplay primitives are dialog gates, two immediate `start_battle` actions, sealed FAIL wings, one hard-fail node per losing route, and one final `win_quest`.

### PASS spine

`O0 -> G1 -> G2 -> G3 -> G4 -> C1 dialog -> Harvest Boar start_battle -> delivery dialogs -> catastrophe -> win_quest`

### F1

Wrong G1 choice -> repair-success dialog -> too-late crossing dialog -> `fail_quest`.

### F2

Wrong G2 choice -> calm old-road travel dialog -> Road Bandit confrontation dialog -> **Road Bandit `start_battle`** -> false-victory dialog -> delayed levee/flood dialogs -> `fail_quest`.

Road Bandit loss -> dedicated `fail_quest`.

### F3

Wrong G3 choice -> successful-rescue dialog -> shipment-loss dialog -> `fail_quest`.

### F4

Wrong G4 choice -> perfect-catch dialog -> main-load-loss dialog -> `fail_quest`.

### C1 loss

Harvest Boar loss -> dedicated `fail_quest`.

### Engine constraints for both battles

- Each `start_battle` sits directly behind a dialog gate.
- Each has a `failObjectiveId` to a terminal FAIL route.
- No location fields are used to create gameplay travel.
- `opponentAIs` uses the current generated contract shape.
- All dialog `nextObjectiveId` values are choice arrays, including one-entry straight continuations.
- Because non-dialog actions auto-link, do not insert ungated action chains around either battle.

## Phase A — art execution

### Processed and accepted design

- Ittetsu SCENE_CHARACTER: `one_perfect_crop_ittetsu_scene.webp` — 341x512 RGBA lossless WebP.
- Waystation Keeper SCENE_CHARACTER: `one_perfect_crop_waystation_keeper_scene.webp` — 341x512 RGBA lossless WebP.
- Quest/listing icon raw URL: `one_perfect_crop_quest_icon.webp` — 256x256 RGB lossless WebP.

The processed files are delivered together as the `one_perfect_crop_art_intake.zip` handoff. They still require the repository's final `artpreflight.py` zero-error gate before production use because the source images arrived on black rather than a generator-native chroma/alpha field and were isolated locally.

### Reuse locked for build unless dauntless changes it before final freeze

- Market Clerk scene character: `DM Mission Clerk` — gameAsset id `XsLLy8awDAtaE6hXVIi_0`.
- Farm-road / terraced-field scene family: `Forsworn Scene BG - Pass Road Dusk` — `nmrMHmz9xWojzyIV2mAR8`.
- Crossing / waystation scene family: `Forsworn Scene BG - Waystation Door` — `kmDsQUEHSub9GIX5ulO6i`.
- Old-road / ambush / flood scene family: `Forsworn Scene BG - East Road Ambush Site` — `E4VJ-IeIQMwbmGGfKc-sn`.
- Market scene family: `BustlingTownMarket` — `cYu6VwVX55m6uq1oxlWc1`.

Every dialog node must receive an explicit sceneBackground and sceneCharacters assignment. Do not create extra backgrounds merely to depict each accident; the prose carries the changing incident inside these four geographical scene families.

### Still required art

- Road Bandit SCENE_CHARACTER: `one_perfect_crop_road_bandit_scene.webp` — new, unless dauntless later approves a different current asset. `Nameless Ninja` may not be used.
- Road Bandit AI avatar: `one_perfect_crop_road_bandit_avatar.webp` if a new Road Bandit AI is required by Phase B.
- Harvest Boar AI avatar: `one_perfect_crop_harvest_boar_avatar.webp` — new square AI avatar.
- Cabbage Seed item icon: `one_perfect_crop_cabbage_seed.webp` — new square item icon.

No separate Harvest Boar SCENE_CHARACTER is required. The C1 dialog scene remains Ittetsu on the farm-road/final-approach background; prose introduces the animal immediately before battle.

## Phase B — combat-record execution

### Road Bandit reuse probe staged

`push/04_one_perfect_crop_bandit_ai_probe.json` full-captures, with no mutations:
- Bandit 1 — `sJOmHYaUnJfh9-zbNL_4b`
- Bandit Leader — `OACGO0AM5yBQkxlOs_rI_`
- Marauder — `n8EP0t5NN3zhzxXiDdZIY`
- Mercenary Ronin — `Tnkm2Xk9EthSa2z_0LfFM`
- Seichi Bandit — `UrAEVY5QvtQqKs-XB92PX`

After dauntless runs the probe, compare the exact live records against the approved combat contract. If a plausible candidate has an `aiProfileId`, full-capture `ai.getAiProfile` before declaring it compatible. Reuse only if it already satisfies the event contract closely enough without editing that shared record. Otherwise create a new generic Road Bandit AI/profile.

Approved Road Bandit contract:
- technical rank JONIN,
- scale to user ON,
- element None,
- standard/default stored stats and pools,
- no passive tags,
- no control gimmicks, shields, healing, buffs, seals, wounds, pierce, poison, or bespoke mechanics,
- kit exactly: S27 Weakening Strike (`YiRdVytsdxFzZtqkEDs5Q`), S41 Steady Strike (`fKvCGRgzGNskgFWocQCAg`), S40 Measured Strike (`kkGDat1XWUxhOQ1_T5025`),
- simple priority: approach -> Weakening Strike when available -> Steady Strike -> Measured Strike -> strongest legal fallback,
- one enemy.

### Harvest Boar

Create a new Harvest Boar AI/profile:
- technical rank JONIN,
- scale to user ON,
- element None,
- default/even stored stats, pools, regeneration and armor,
- no passive tags or special charge mechanic,
- kit exactly: S27 Weakening Strike (`YiRdVytsdxFzZtqkEDs5Q`), S42 Forceful Strike (`4TM6iS8P0qgNHsFpALFhg`), S41 Steady Strike (`fKvCGRgzGNskgFWocQCAg`),
- simple priority: approach -> Weakening Strike when available -> Forceful Strike -> Steady Strike -> strongest legal fallback,
- one enemy.

No new jutsu are created.

## Phase C — content-admin open packet

These values are intentionally **not** decided by implementation. They may be filled only by the content admin. Until they are supplied, the final manifest must remain non-runnable/incomplete rather than inventing defaults.

Open fields:
- event reward Ryo,
- event reward XP,
- event reward tokens/other standard currencies if used,
- Cabbage Seed rarity,
- Cabbage Seed required economic/value fields,
- Cabbage Seed functional item type if the item contract requires a semantic choice,
- event repeatability / once policy,
- exact eligibility rule.

The submitted requirement says `Farming level 15`. Current generated quest vocabulary does not establish a native farming progression gate. Do **not** translate it to character `minLevel: 15`. Content admin must explicitly select a supported substitute or remove the mechanical gate.

## Phase D — final freeze contract

Once Phase B capture review and the Phase C admin fields are resolved, freeze `state/prompt_one_perfect_crop.md`. It must carry:
- exact normalized prose for every node,
- exact node IDs and graph,
- both dialog-gated `start_battle` nodes and hard-fail battle routes,
- exact Road Bandit reuse ID or new AI/profile specification,
- new Harvest Boar AI/profile specification,
- exact reused scene asset IDs,
- exact new `@img:<filename>` contracts,
- complete scene wiring,
- Cabbage Seed item definition,
- content-admin values copied exactly,
- every create hidden,
- no publishing operation,
- stale-reference warning: do not inherit the old event note that generic story battles must use `defeat_opponents` or a mission-style 12–14-node shape.

## Phase E — Fable manifest implementation

Fable builds from the frozen brief using current factory/generated contracts.

Dependency order:
`jutsu -> assets -> items -> ai -> aiProfile -> quest`

For this event the jutsu phase is empty.

Required properties:
- dedup/name resolution enabled,
- every created entity `hidden: true`,
- no publishing/unhide operation,
- exact `@img` filenames,
- no shared-record edits unless separately approved,
- no authored retry route after battle loss,
- exactly one quest start and all choice/fail edges resolve,
- `validate.py` 0 errors before handoff.

Fable returns an exact frozen SHA plus validation/build evidence. No live request.

## Phase F — independent ChatGPT audit

Audit the exact frozen candidate for:
- PASS/FAIL reachability and sealed failure wings,
- no wrong branch rejoining PASS,
- G4 overlearning trap preserved,
- both battles dialog-shielded `start_battle`,
- hard loss routing,
- normalized prose markup,
- explicit delivery acceptance before `MY CABBAGES!`,
- no Ittetsu incompetence,
- one enemy per battle,
- JONIN + scale-to-user fidelity,
- exact approved micro-kits,
- no new jutsu,
- explicit scene wiring,
- exact asset filenames/IDs,
- content-admin values copied exactly,
- all creates hidden,
- validator green.

## Phase G — user production execution and readback

Only dauntless crosses the production boundary:
1. load the reviewed manifest in Forge,
2. inspect preflight and image resolution,
3. confirm mutations deliberately,
4. run,
5. export/commit result,
6. fresh full readback/capture of created records,
7. compare readback to frozen contract.

A green push echo is not readback. Publishing/unhiding is a separate content-admin/dauntless action after acceptance.

## Immediate next gate

Run `push/04_one_perfect_crop_bandit_ai_probe.json`. Forge should show **5 full captures, 0 items, 0 mutations**. While that read-only probe is pending, missing art can be produced one asset at a time in a clean art-generation context using the captured live TNR references.
