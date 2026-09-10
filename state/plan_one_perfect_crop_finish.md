# One Perfect Crop — finish implementation plan

**Status:** design-complete enough to finish; not yet a runnable implementation brief.  
**Plan owner:** ChatGPT / Content Designer.  
**Implementation owner:** Fable / Claude Code after final freeze.  
**Live-game actor:** dauntless only.  
**Base:** `main` at `cfa3fb71ce70858d2ed740945421a3671ca2215d`.

## Settled rulings carried into this plan

1. The route graph, prose, cast, encounter count, PASS/FAIL outcomes, delivery-before-catastrophe order, and final `MY CABBAGES!` beat are frozen.
2. Player-facing prose uses TNR scene formatting: passive narration/action in `<i>...</i>`, spoken text in quotes, dramatic beat spacing with literal `<br> <br>`, and choices quoted only when they are actually spoken.
3. F2 Road Bandit is now a dialog-gated **`start_battle`**, not `defeat_opponents`. It is an ambush and begins immediately when the player commits to the old road. This removes the previous location/sector/map-marker dependency.
4. C1 Harvest Boar remains dialog-gated **`start_battle`**.
5. Both battle losses hard-route to FAIL with no authored retry branch.
6. Balance/reward/rarity/repeatability/eligibility values that are still unresolved stay explicitly open for the content admin. Fable must not guess them into a runnable manifest.
7. Ittetsu art is produced and accepted as the character design. The shared source is 1024x1536 RGB with an opaque black background; it still needs a production-safe transparent/chroma source or equivalent isolation before the standard SCENE_CHARACTER processing/QC pipeline. Do not redesign the character.
8. The One Perfect Crop quest/listing icon is approved in current TNR pixel style; it still needs standard processing/QC and a final filename contract.
9. `Nameless Ninja` is rejected for visual reuse as deprecated/below the current quality bar.
10. Do not edit shared live AI merely to make it fit this event.

## Target event shape

The event is now deliberately **zero-travel**. Its authored gameplay primitives are dialog gates, two immediate `start_battle` actions, sealed FAIL wings, one hard-fail node per losing route, and one final `win_quest`.

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

## Remaining work, in dependency order

### Phase A — finish art intake and reuse decisions

**Already designed/approved**
- One Perfect Crop listing icon — approved art, needs pipeline processing/QC and final filename.
- Ittetsu SCENE_CHARACTER — approved design, needs isolation to legal alpha/chroma, then raw QC/process/dark-composite QC/preflight.

**Reuse, subject to final visual acceptance/current record identity**
- Waystation Keeper: prefer current `Forsworn Scene - Keeper` (`AM0saNTIIl1FPgc5pAzxc`) over minting a new generic civilian.
- Market Clerk: `DM Mission Clerk` (`XsLLy8awDAtaE6hXVIi_0`).
- Destination market: `BustlingTownMarket` (`cYu6VwVX55m6uq1oxlWc1`).
- Rural/background coverage: review the captured current Forsworn backgrounds first, especially Pass Road Dusk, Waystation Door, East Road Ambush Site, and Canal Frontage. Reuse only if the actual visual fits One Perfect Crop's rural-farming tone; otherwise generate the minimum new set.

**Still needs new art unless a later approved reuse appears**
- Road Bandit SCENE_CHARACTER. `Nameless Ninja` is rejected; do not fall back to it.
- Harvest Boar AI avatar.
- Cabbage Seed item icon.

**Scene-background goal**
Keep the set minimal. The likely maximum is four scene families:
1. farm road / damaged cart / terraced fields,
2. crossing / waystation,
3. old levee / ambush / flood route,
4. market.
A reused background may cover a family if visually appropriate; every dialog node still receives an explicit background and scene-character assignment.

**Art gates**
Use `skills/producing-tnr-art/` exactly: one asset at a time; `rawqc.py`; target processing via `chroma.py` when applicable; dark composite inspection; `artpreflight.py` zero errors; record exact final filename/dimensions/KB. Corrected assets get fresh filenames.

### Phase B — resolve combat records

#### Road Bandit
First perform a fresh full capture of the strongest existing generic bandit AI candidates from the current AI catalog. Reuse only if a live AI already satisfies the approved event combat contract closely enough without editing a shared record.

Approved combat contract:
- technical rank JONIN,
- scale to user ON,
- element None,
- standard/default stored stats and pools,
- no passive tags,
- no control gimmicks, shields, healing, buffs, seals, wounds, pierce, poison, or bespoke mechanics,
- three-move micro-kit: Weakening Strike + Steady Strike + Measured Strike,
- simple priority: approach -> Weakening Strike when available -> Steady Strike -> Measured Strike -> strongest legal fallback,
- one enemy.

If no current reusable AI matches, create a new generic Road Bandit AI/profile. Do not mutate an existing shared enemy.

#### Harvest Boar
Create a new Harvest Boar AI/profile:
- technical rank JONIN,
- scale to user ON,
- element None,
- default/even stored stats, pools, regeneration, armor,
- no passive tags or special charge mechanic,
- three-move micro-kit: Weakening Strike + Forceful Strike + Steady Strike,
- simple priority: approach -> Weakening Strike when available -> Forceful Strike -> Steady Strike -> strongest legal fallback,
- one enemy.

No new jutsu are required. Resolve the already-approved shared jutsu IDs through current generated data/factory machinery rather than hard-coding remembered codes.

### Phase C — content-admin decision packet

Do not block design/art/AI preparation on these, but do block the final runnable manifest.

Content admin must supply or approve every unresolved value required by the generated item/quest contracts, including at minimum:
- event reward Ryo,
- event reward XP,
- event reward tokens/other standard currencies if used,
- Cabbage Seed item rarity,
- Cabbage Seed economic/value fields required by its chosen item type,
- event repeatability / once policy,
- exact eligibility rule.

The submitted sheet says `Farming level 15`, but the current quest reference exposes gathering/hunting/crafting/medical counters and no repository search currently establishes a native `farming` quest gate. Do **not** silently convert this to character `minLevel: 15`. Resolve the intended gate with the content admin against current generated contracts/source; if no native farming gate exists, record the approved substitute or remove the mechanical gate explicitly.

Also settle the Cabbage Seed's functional item type (flavor/material/other supported type) if the generated item contract requires a semantic choice beyond numeric tuning.

### Phase D — freeze final implementation brief

Once Phases A-C are complete, create `state/prompt_one_perfect_crop.md` as the concise Fable contract. It must include:
- exact normalized prose for every node,
- exact node IDs and graph,
- the F2 `start_battle` ruling,
- both hard-fail battle routes,
- exact AI/AI profile IDs or create specs,
- exact reused asset IDs,
- exact new `@img:<filename>` contracts,
- scene background + scene character wiring for every dialog node,
- Cabbage Seed item definition,
- content-admin reward/repeatability/eligibility values,
- hidden/publishing constraints,
- explicit stale-reference warning: do not inherit the old event note that generic story battles must use `defeat_opponents` or a 12-14-node mission shape.

This brief is the implementation contract; do not use chat memory as a substitute.

### Phase E — Fable manifest implementation

Fable builds on its own implementation branch / normal Lane B content path using the current factory and generated contracts.

Build dependency order remains:
`jutsu -> assets -> items -> ai -> aiProfile -> quest`

For One Perfect Crop the jutsu phase is empty.

Required implementation properties:
- dedup/name resolution enabled,
- every created entity `hidden: true`,
- no publishing/unhide operation in the creation manifest,
- asset `@img` filenames exact,
- no shared-record edits unless the frozen brief explicitly names an approved edit,
- no authored retry route after battle loss,
- quest graph has exactly one start and all choice/fail edges resolve,
- validate with `validate.py` and require 0 errors before handoff.

Fable returns an exact frozen SHA plus validation/build evidence. No live request.

### Phase F — independent ChatGPT content audit

Audit the exact frozen candidate for:
- PASS/FAIL reachability and sealed failure wings,
- no wrong branch rejoining PASS,
- G4 overlearning trap preserved,
- F2 and C1 both correctly dialog-shielded `start_battle`,
- hard loss routing,
- normalized TNR prose markup (`<i>`, quotes, `<br> <br>`),
- `MY CABBAGES!` appears only after explicit accepted-delivery confirmation,
- no Ittetsu incompetence introduced by implementation edits,
- one enemy per battle,
- JONIN + scale-to-user fidelity,
- approved micro-kits only,
- no new jutsu,
- complete explicit scene wiring,
- art filenames/asset IDs match approved outputs,
- content-admin values copied exactly,
- all creates hidden,
- validator green.

### Phase G — user production execution and readback

Only dauntless crosses the production boundary:
1. load the reviewed manifest in Forge,
2. inspect preflight and image resolution,
3. confirm mutation set deliberately,
4. run,
5. export/commit result,
6. perform fresh full readback/capture of created records,
7. compare readback to the frozen contract.

A green push echo is not sufficient evidence. Publishing/unhiding remains a separate content-admin/dauntless action after readback acceptance.

## Recommended immediate sequence

1. Process/isolate the already-made Ittetsu art; do not regenerate the design.
2. Process the approved listing icon.
3. Visually decide the three reuse assets and captured background candidates.
4. Generate/process Road Bandit, Harvest Boar avatar, Cabbage Seed icon, and only the backgrounds still missing after reuse.
5. Full-capture Road Bandit AI candidates and decide reuse-vs-new.
6. Hand the compact unresolved balance/reward/eligibility packet to the content admin.
7. Freeze `state/prompt_one_perfect_crop.md`.
8. Fable builds and validates.
9. ChatGPT audits exact SHA.
10. dauntless runs and readbacks; publishing remains separate.
