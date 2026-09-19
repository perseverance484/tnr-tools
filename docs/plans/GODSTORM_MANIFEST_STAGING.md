# Godstorm two-pyramid manifest staging contract

Updated: 2026-09-19
Status: PARTIALLY FROZEN / NOT EXECUTABLE / ZERO LIVE REQUESTS OR WRITES
Working branch: `chatgpt/godstorm-two-pyramid-plan`

This file is the durable control sheet for assembling the eventual Forge mutation manifest for Marrow Vaults and Stormcourt. It does not itself authorize or perform a game mutation. Fable remains the normal manifest implementation owner unless the director explicitly assigns the executable payload to ChatGPT. The director alone operates the live game.

## Repository / evidence state

- Current live `main` verified at `9e1dafc3ee5c8884ce90c3530de4afba364fad24` on 2026-09-19.
- Godstorm planning branch before this staging update: `348422a92584d7d043f561b9d7c0f26f4d153dea`.
- Root graph capture: `harvests/inbox/tnr_results_1789401726302.json`.
- Related AI/art/reward capture: `harvests/inbox/tnr_results_1789402842027.json`.
- Combat-profile closure capture: `harvests/inbox/tnr_results_1789403623148.json`.
- Captures describe the September 14 live state; they are not the revised state.
- Current SCENE_BACKGROUND specification blob at main remains `688b4ed615e1cb1e11d46d4c9e35865824291033`, unchanged from the production checks used for the accepted environment exports.

## 1. Manifest-ready quest identity and graph delta

These fields are structurally approved and may be treated as frozen inputs to the eventual generator:

| Field | Marrow Vaults | Stormcourt |
| --- | --- | --- |
| Existing quest ID | `2yvE9PUQqlD8lbYNfgX-b` | `OSADdXqostbyVliCxWk6k` |
| Player-facing name | `Marrow Vaults` | `Stormcourt` |
| Quest type | preserve `battlepyramid` | preserve `battlepyramid` |
| Battles | 25 | 25 |
| Keepers | 5 | 5 |
| Successful route | full clear only | full clear only |
| Mechanical relationship | existing quest | preserve existing Marrow prerequisite |
| Cash-out | remove | remove |
| Tower identity | remove | remove |

Final revised target: 106 objectives total = 50 battles + 52 dialogs + four terminal nodes.

Remove exactly these 16 dialogs:
- Marrow: `d1_choice`, `d1_cash`, `d2_choice`, `d2_cash`, `d3_choice`, `d3_cash`, `d4_choice`, `d4_cash`.
- Stormcourt: `d6_choice`, `d6_cash`, `d7_choice`, `d7_cash`, `d8_choice`, `d8_cash`, `d9_choice`, `d9_cash`.

Reroute exactly these eight keeper success edges:
- `b1_boss -> d2_1`
- `b2_boss -> d3_1`
- `b3_boss -> d4_1`
- `b4_boss -> d5_1`
- `b6_boss -> d7_1`
- `b7_boss -> d8_1`
- `b8_boss -> d9_1`
- `b9_boss -> d10_1`

Retain:
- `b5_boss -> d5_victory -> win`
- `b10_boss -> d10_victory -> win`
- all 50 existing failure routes to `fall`
- all 18 direct opponent AI identities and their captured battle order/configuration unless later balance work explicitly changes them.

No travel node, automatic Stormcourt launch, merged tracker, new checkpoint system or new quest type is authorized.

## 2. Approved background wiring

### Marrow Vaults

Existing assets:
- M1: `7EmVo6GH5GL4YtQTDrbDR` — marrow vault 1.
- M2: `oc0cXiMrcG_6kTUwNWRkn` — marrow vault 2.
- M3: `IykL5XxwFF14BosCblZj8` — marrow vault 3.

Director-approved remap:
- `d1_1 -> M3`.
- `d5_victory -> M2`.

Other Marrow scene allocations remain as specified in Draft 2 until a later explicit change. The recovered Marrow files are legacy 500x333 sources; current art-preflight status is not claimed by this binding decision.

### Stormcourt

The unrelated SkychainMonastery `StormCourtyard` asset `cKHhHoboreP88iH5WjDe7` is explicitly excluded and must never resolve a Godstorm binding.

Accepted new production assets:

| Logical key | Production file | Coverage | SHA-256 | Runtime gameAsset ID |
| --- | --- | --- | --- | --- |
| SC_UPPER | `bg_godstorm_stormcourt_upper_court.webp` | `d6_1` through `d9_boss` (20 dialogs) | `c0587d9fdeb8c4c75ecc6f5eaf0c08a0b783461299793c774f66f7aaab4f12b9` | PENDING |
| SC_DAIS_ACTIVE | `bg_godstorm_stormcourt_binding_dais_active.webp` | `d10_1` through `d10_boss` (5 dialogs) | `41ca12f9d21604151f754ded0df2211bed5b671dcc2dd7c954e53c5f17f36d70` | PENDING |
| SC_DAIS_RELEASED | `bg_godstorm_stormcourt_binding_dais_released.webp` | `d10_victory` | `97fc11d4ad1c24beeaffaf2e7f8a589715806dce6d17290d0fa253694fd3ef18` | PENDING |

All three are accepted compositions and locally production-exported at 1536x1024, flattened RGB, lossy WebP q85, exact 3:2, above the 512px minimum and below both current byte ceilings. Runtime IDs do not exist yet. Before gameAsset creation, place the exact binaries durably and run the repository's current `artpreflight.py` against those exact hashes.

## 3. Character-art slots

### AI avatar updates still required

These five existing Marrow AI records still have the default avatar and remain open asset slots:

| AI | Existing ID | Asset status |
| --- | --- | --- |
| Umbral Reaver | `9uDe65Qt90xnT-fM5vJZ7` | ACCEPTED / processed / wired as `ai_godstorm_marrow_umbral_reaver.webp`, SHA-256 `30693d5dc252f8ce61638a0b4c191523ef7df8461b8252ff309e21192154bfcc` |
| Hollow Lantern | `IG5Mbfi_2lpUTnUU4_XhZ` | ACCEPTED / processed / wired as `ai_godstorm_marrow_hollow_lantern.webp`, SHA-256 `50d1786fb6f5c2a2350b04dd27ec1ff8b0e1d58237e98337c0a2065e226b6055` |
| Starless Monk | `qQ6jMh8w6aiyr4pevwDh-` | ACCEPTED / processed / wired as `ai_godstorm_marrow_starless_monk.webp`, SHA-256 `877eef3b0cecc914d4e3300e21cb50c87030093c5730d4feb54b71a7e7cdc870` |
| Nightveil Sentinel | `YvinZCoMWiz0RY8ZBP5EW` | USER-SUPPLIED / processed / wired as `ai_godstorm_marrow_nightveil_sentinel.webp`, SHA-256 `d5c5a8c8a2be20700a7df16b9ac38e4b9cd6a7a2917efa5d7d815d19deebd9e2` |
| Warden of the First Dark | `oi4bHe3upEhLkI-ElJuMX` | PENDING new accepted AI_AVATAR |

Two rejected Umbral-generation attempts from the previous chat are not manifest inputs and must not be reused as TNR style references.

### Scene-character records still required

Ten keeper scene-character placements remain unresolved:
- K1 Warden of the First Dark
- K2 Keeper of Hushed Hours
- K3 The Moth Tyrant
- K4 Chained Chorister
- K5 Warden of the Half Eclipse
- K6 The Gloaming Judge
- K7 Widow of the Waning Moon
- K8 The Candlewright
- K9 Herald of the Last Dusk
- K10 Sovereign Echo of the Godstorm

A single verified blank scene-character record is also still required for the 42 non-keeper dialogs plus the intended quest-level fallback. Older candidates `Q-_3WA5kibe_8gI2CgTKl` and `1YXbXYW2wz3GETVMb6DT6` are discovery candidates only until current record/type/pixels are verified.

Do not write null IDs, planning aliases or fabricated IDs into an executable manifest.

## 4. Copy status

The structural story decisions are approved:
- one connected structure;
- Marrow below, Court above;
- Marrow clear opens access upstairs;
- no Tower branding;
- no early cash-out;
- Stormcourt ends this Godstorm release.

The exact Draft 2 quest descriptions, all 52 dialog descriptions, battle labels/outcome wording and exact local-binding finale prose remain **editorial draft unless separately accepted**. Therefore the eventual executable quest-update payload must not be declared frozen merely because the graph and art map are ready.

Current authored source: `docs/plans/GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md`.

## 5. Reward fields intentionally open

The manifest must not invent values for:
- Marrow full-clear reward package;
- Stormcourt full-clear reward package;
- repeat period / completion count / attempt policy;
- chest use, omission or replacement;
- any new drop channel.

The shared `Endless Night Chest` `HLycjzUcVwKZenBWpd0V-` is Tower-branded and cannot be silently reused/renamed. Content Admin/director decision remains required.

## 6. Other unresolved implementation gates

Before the mutation manifest can be frozen:
- resolve three new Stormcourt gameAsset IDs after asset creation;
- resolve five Marrow avatar image URLs after accepted production/upload;
- resolve ten keeper SCENE_CHARACTER IDs and one blank SCENE_CHARACTER ID;
- accept/freeze exact player-facing copy;
- settle the two reward packages and cadence;
- verify any external hub/menu/entry records that expose old Tower naming;
- define protected handling for active trackers referencing the 16 removed dialogs;
- preserve historical successful completions unless the director separately authorizes migration;
- rerun current source/contract checks and graph validation at implementation time;
- perform retained-AI functional/balance QA before release readiness;
- rerun actual repository art preflight on every new binary;
- independently review the frozen implementation SHA before live application.

## 7. Asset intake procedure from this point

For every new art file received by this chat:
1. identify its intended logical slot and source/acceptance status;
2. process it against the current target contract;
3. inspect delivered-size output;
4. record exact production filename, dimensions, format, byte size and SHA-256;
5. run repository art preflight when a checkout/runtime is available;
6. never invent a runtime ID;
7. once the operator/Fable creates the game asset, replace the slot's PENDING runtime ID with the read-back ID;
8. only then permit the quest manifest to reference that asset.

Raw generated candidates, rejected images and review composites are never manifest dependencies.

## 8. Current readiness snapshot

| Surface | State |
| --- | --- |
| Two-quest release scope | FROZEN |
| Graph deletion/reroute plan | FROZEN, implementation validation pending |
| Marrow background remap | APPROVED |
| Stormcourt environment compositions | 3/3 APPROVED |
| Stormcourt environment production exports | 3/3 COMPLETE LOCALLY |
| Stormcourt runtime background IDs | 0/3, PENDING |
| Marrow missing AI avatars | 4/5 supplied, processed and manifest-wired; Warden of the First Dark pending |
| Keeper scene characters | 0/10 resolved runtime IDs |
| Blank scene character | PENDING |
| Exact player-facing copy | NOT FROZEN |
| Rewards/cadence/chest | OPEN |
| Executable mutation manifest | NOT YET CREATED |
| Live requests/writes in this staging pass | ZERO |

The next safe manifest progress comes from asset intake: each accepted avatar/portrait can be processed and its exact production metadata added immediately while the copy/reward decisions remain independent.


## 9. AI rule-safety closure and current executable-scope manifest

A current-source audit was completed on 2026-09-19 against `studie-tech/TheNinjaRPG@a670c9aaa741157dc66eacc949600ff2db0b48cd` using the full September 14 AI and AI-profile captures. Durable review: `docs/reviews/REVIEW_2026-09-19_godstorm_ai_rule_safety.md`.

Result:
- all 18 retained profiles resolve;
- every specific/combo jutsu reference is equipped;
- every SELF jutsu is action-targeted SELF;
- every OTHER_USER jutsu used by a specific/combo rule is action-targeted RANDOM_OPPONENT;
- every specific/combo offensive rule is guarded at or inside the minimum range of the action(s) it can select;
- all 18 profiles carried one unsafe authored pattern: an unconditional `use_highest_power_action(effect=damage, target=RANDOM_OPPONENT)` fallback.

Current game source does not range-filter `availableUserActions` against the profile-supplied target coordinate. If movement is checked but cannot produce a usable move/path, that unconditional fallback can select a damage action beyond its range and `performBattleAction` can reject/throw. The staged correction preserves every other rule and adds the engine-native adjacent guard `distance_lower_than <= 2` on RANDOM_OPPONENT to that one fallback in each profile. A second programmatic target/range pass over the corrected rule sets reports zero remaining issues in this audit class.

The complete **currently safe executable scope** is checked in at `push/48_godstorm_current_manifest.json`:
- 3 hidden SCENE_BACKGROUND creates using the three accepted production files and exact `imgSizes`;
- 4 existing Marrow `ai` edits wiring Umbral Reaver, Hollow Lantern, Starless Monk and Nightveil Sentinel avatars by exact `@img` filename;
- 18 existing `aiProfile` edits applying only the bounded fallback correction;
- 25 items total;
- no quest mutation yet.

“Currently safe executable scope” is deliberate. The quest graph delta is structurally frozen, but applying it while leaving old Tower/cash-out prose or inventing copy/reward/scene-character fields would create an incoherent intermediate quest. The quest edit remains withheld until the unresolved copy, reward/cadence/chest and scene-character slots are frozen. This is not permission to run item 48 against production; the director remains the only live-game operator.

For the next manifest revision, accepted avatar/scene-character assets should be added to the same generator/pack and quest edits should be emitted only when every required player-facing field is settled. Do not remove the 18 profile corrections when later revisions supersede item 48.


### First three Marrow avatar intake (2026-09-19)

The director supplied and accepted the first three missing Marrow avatar masters in order: Umbral Reaver, Hollow Lantern, Starless Monk. Each 1536x1536 lime-key PNG was processed through the current component-key logic, cropped to the visible subject, transparently padded back to exact 1:1, and exported as lossless WebP. Dark-background QC composites were inspected; no disqualifying green field or silhouette damage was observed.

| AI | Production file | Output px | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Umbral Reaver | `ai_godstorm_marrow_umbral_reaver.webp` | 1492x1492 | 161,650 | `30693d5dc252f8ce61638a0b4c191523ef7df8461b8252ff309e21192154bfcc` |
| Hollow Lantern | `ai_godstorm_marrow_hollow_lantern.webp` | 1476x1476 | 196,056 | `50d1786fb6f5c2a2350b04dd27ec1ff8b0e1d58237e98337c0a2065e226b6055` |
| Starless Monk | `ai_godstorm_marrow_starless_monk.webp` | 1477x1477 | 207,410 | `877eef3b0cecc914d4e3300e21cb50c87030093c5730d4feb54b71a7e7cdc870` |

All three are square, carry alpha, exceed the 320px AI_AVATAR minimum and are below the 460,800-byte working ceiling. They are wired into `push/48_godstorm_current_manifest.json` as existing-AI edits to `data.avatar`; no runtime ID is needed for an AI avatar image because Forge uploads the file and resolves `@img:<filename>` directly to the avatar URL. The remaining missing Marrow AI avatar slots are Nightveil Sentinel and Warden of the First Dark.


### Nightveil Sentinel avatar intake (2026-09-19)

The director supplied the fourth missing Marrow avatar master for Nightveil Sentinel. The 1536x1536 lime-key source was processed through the same component-key path as the first three, cropped to the visible subject, transparently padded to exact 1:1 and exported as lossless WebP. The dark-background QC composite was inspected and showed a clean silhouette with no remaining lime field or obvious keyed holes.

| AI | Production file | Output px | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Nightveil Sentinel | `ai_godstorm_marrow_nightveil_sentinel.webp` | 1429x1429 | 115,618 | `d5c5a8c8a2be20700a7df16b9ac38e4b9cd6a7a2917efa5d7d815d19deebd9e2` |

The export is square, carries alpha, exceeds the 320px AI_AVATAR minimum and is below the 460,800-byte working ceiling. It is wired into `push/48_godstorm_current_manifest.json` as an existing-AI edit to `YvinZCoMWiz0RY8ZBP5EW.data.avatar` using the exact `@img` filename. The only remaining missing Marrow AI avatar slot is Warden of the First Dark.
