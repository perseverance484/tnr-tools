# Godstorm / Tower of Endless Night — final readiness audit

Date: 2026-09-14
Lead lens: Release Auditor
Supporting lenses: Content Designer, Art Director
Base live-repo SHA: `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`
Live-operation status: READ-ONLY AUDIT ONLY. ChatGPT performed no live game writes.

## Verdict

**HOLD / RED for final certification.**

The three battlepyramids are structurally coherent and their opponent records / AI profiles resolve, but the current live content is not final-ready because reward integrity is broken, one quest violates current repeatable-reward doctrine, the final boss carries a major uncalibrated multiplicative damage spike, and visual coverage is incomplete.

This is not a recommendation to take the live quests down automatically. The operator owns that decision. It is a release-certification hold: do not call the current package final until the blockers below are resolved and read back.

## Evidence set

Read-only capture chain:

1. `push/23_godstorm_tower_root_capture.json`
   - result: `harvests/inbox/tnr_results_1789401726302.json`
   - three full `quests.get` records
2. `push/24_godstorm_tower_related_capture.json`
   - result: `harvests/inbox/tnr_results_1789402842027.json`
   - 23 full `profile.getAi` records, reward/item point reads, candidate game assets
3. `push/25_godstorm_tower_combat_closure.json`
   - result: `harvests/inbox/tnr_results_1789403623148.json`
   - 23 full `ai.getAiProfile` records + direct AI Heavy Armor read
   - `DONE / success`, zero mutation entries, all 24 captures resolved

Canonical mechanics reviewed:
- `skills/building-tnr-content/references/quest.md`
- `skills/building-tnr-content/references/ai.md`
- `skills/building-tnr-content/references/balance.md`
- `skills/producing-tnr-art/SKILL.md`
- `skills/producing-tnr-art/data/25x_DATA_art_spec.json`

## Scope

Quest roots:
- `2yvE9PUQqlD8lbYNfgX-b` — The Tower of Endless Night: The Marrow Vaults
- `OSADdXqostbyVliCxWk6k` — The Tower of Endless Night: The Stormcourt
- `VjT93rkmWlWlrdG6Pp46e` — The Tower of Endless Night: Dawnless Crown

All three are S-rank `battlepyramid`, required level 70, max level 100. Stormcourt requires Marrow Vaults; Dawnless Crown requires Stormcourt.

## PASS — objective graph / battle sequencing

The captured graphs contain **75 `start_battle` nodes** total: five battles per floor across fifteen floors.

The engine requires every `start_battle` to sit directly behind a dialog gate. The graph supplies exactly:
- 60 straight `Advance` dialog choices into normal battle nodes; and
- 15 `Face the keeper` dialog choices into keeper/boss battle nodes.

All 75 captured battle nodes carry `failObjectiveId`, routing losses to the shared `fall` fail node. The sampled and terminal paths use battle -> dialog -> battle sequencing rather than consecutive un-gated battles. Cash-out choices route through reward-bearing dialog nodes and then the `win_quest` terminator. Final victories likewise route through a payoff dialog before `win_quest`.

**Structural verdict: PASS.** The known battlepyramid co-activation/skip failure mode is not present in the captured graphs.

## PASS — AI/profile closure

Phase 2 resolved the 23 unique opponent AI records used by the three quests. Phase 3 resolved all 23 associated AiProfile records. No profile point-read returned zero rows.

The profiles contain ordered range-gated rules, combo actions, movement fallbacks, and `includeDefaultRules:true`. The high-risk keeper/final-boss profiles have real rule bodies rather than empty/default-only profiles.

The full equipped jutsu bodies were embedded in `profile.getAi`, so separate jutsu point reads were not necessary for closure.

**Record-resolution verdict: PASS.** This does not by itself certify difficulty.

## BLOCKER 1 — guaranteed keystone reward references do not resolve

Marrow Vaults final victory promises and references an Eclipse Keystone:
- reward item id `1VkKByaLQNDjJUEqiNeic`
- `number:100`, `quantity:1` (guaranteed one if the reference is valid)

Stormcourt final victory promises and references an Aegis Keystone:
- reward item id `PPlOpN27RkT0Aw-m9Cfg3`
- `number:100`, `quantity:1`

Phase-2 live `item.get` point reads returned `rows:0`, `data:null` for **both IDs**.

These are dangling guaranteed reward references in live quest content. Do not infer successful grant behavior from the quest payload. The item records must be created/restored or the quest reward references must be corrected, then read back.

## BLOCKER 2 — Endless Night Chest has an empty live loot table

Item `HLycjzUcVwKZenBWpd0V-` — `Endless Night Chest` — resolves live, but its `noncombatconsumereward` effect is currently empty:
- description explicitly says the loot table is pending Content Admin;
- reward item/jutsu/bloodline/badge arrays are empty;
- currency / token / prestige / experience reward values are zero.

Therefore the pyramid's chase-container reward is not functionally complete.

Important semantic correction: in quest `reward_items`, `number` is **drop chance percent**, not quantity. `quantity` is the amount granted. Current final-floor chest chances are therefore:
- Marrow Vaults: 5% chance of one chest;
- Stormcourt: 10% chance of one chest;
- Dawnless Crown: 15% chance of one chest.

Earlier shorthand treating these numbers as chest quantities was incorrect and is superseded by this audit.

## BLOCKER 3 — Marrow Vaults is an immediate repeatable currency fountain

Marrow Vaults is captured with:
- `retryDelay: "none"`
- `maxCompletes: 100`
- `maxAttempts: 100`

Its first-vault cash-out already pays:
- 25,000 ryo
- 25 event tokens
- 10 prestige
- 1% chance of one Endless Night Chest

and ends in `win_quest`.

The current balance doctrine explicitly states that a record with `retryDelay:"none"` and `maxCompletes > 1` must not pay currency/rare rewards; otherwise it is a farm fountain. Stormcourt and Dawnless Crown use `retryDelay:"daily"`, making Marrow Vaults the outlier.

At minimum, the operator must choose one of the two coherent models before final certification:
1. make Marrow Vaults daily/capped like Towers 2-3; or
2. intentionally keep it repeatable and redesign its reward class to the uncapped/material-only doctrine.

No balance value is changed by this review; the choice belongs to the operator.

## BALANCE HOLD — risk/reward curve

Each tower has five reward exits: four voluntary cash-outs plus the final victory. Within each tower, event tokens and prestige are flat while ryo and chest chance increase with depth:

- Marrow: 25 tokens / 10 prestige at each exit; ryo and chest chance rise by floor.
- Stormcourt: 150 tokens / 60 prestige at each exit; ryo and chest chance rise by floor.
- Dawnless: 275 tokens / 110 prestige at each exit; ryo and chest chance rise by floor.

This makes the event-currency-per-risk incentive strongly favor the earliest cash-out; deeper climbing is bought primarily with higher ryo and higher chest probability. That may be intentional, but it needs explicit operator sign-off because the fiction repeatedly frames deeper climbing as increasing accumulated winnings.

## BALANCE HOLD — stat-cap compression

All opponents are ELITE JONIN, so the CHUNIN+ combat stat cap is 450,000.

The captured level-90 base enemies already carry raw specialty offence/defence fields around 486k, and later keepers rise far above that. Those specialty fields therefore enter the battle cap from the opening tier onward. General stats continue increasing longer, and pools rise from roughly 9.1k toward 11.9k, but the authored raw specialty-stat ladder is partially compressed by the combat cap.

Practical consequence: late-floor difficulty is driven more by pools, kits, passives, control, armor and AI rules than the impressive raw offence/defence numbers suggest. A live calibration fight is required for a final difficulty claim.

## HIGH-RISK BALANCE FINDING — The Endless Night

The final boss `psxanDcHJH0v_MDH5YhyH` has a qualitatively different multiplier stack from the rest of the tower.

Persistent passives include:
- +100% Shadow damage given, 100 rounds
- +100% Shadow damage given, 100 rounds
- +50% Shadow damage given, 100 rounds
- 100% stun prevention, 100 rounds

Current damage doctrine says same-type percentage rows multiply. The three persistent Shadow rows therefore form a **x6.0 passive Shadow damage multiplier** before temporary buffs.

Its explicit AI profile can also cast `The Gathering Night`, +60% Shadow damage for six rounds. When that buff is active alongside the persistent rows, the applicable row-product is **x9.6** before other applicable modifiers. The boss also owns other temporary damage buffs; exact overlap depends on range, cooldown and fight state and is not assumed here.

The boss additionally has `AI Heavy Armor` equipped, live-verified with:
- 20% decreased damage taken for 100 rounds; and
- +30% Highest stat for 100 rounds.

Its kit also includes guaranteed/strong control and denial: stun+seal (`Sovereign Fetters`), buff+heal prevention (`Law of No Dawn`), wound pressure, clear, pierce, and all-target attacks. It is also stun-immune.

This may be an intended pinnacle wall, but it is not defensible to call it balanced from static records alone. The repository's own calibration doctrine requires a declared dummy loadout and live anchor fights. Final-boss tuning remains **AMBER/HOLD pending operator-approved calibration**.

## VISUAL HOLD — current live coverage

The three quest listing/hero images are non-default, but scene coverage is incomplete.

### Marrow Vaults
Three live scene backgrounds exist:
- `7EmVo6GH5GL4YtQTDrbDR` — `marrow vault 1`
- `oc0cXiMrcG_6kTUwNWRkn` — `marrow vault 2`
- `IykL5XxwFF14BosCblZj8` — `marrow vault 3`

They are wired only into a small set of Vault-1 dialogs/cashout nodes. Captured Vaults 2-5 use empty `sceneBackground` fields.

### Stormcourt
A live candidate background exists:
- `cKHhHoboreP88iH5WjDe7` — `StormCourtyard`

It is **not referenced anywhere in the captured Stormcourt quest graph**. Captured Stormcourt dialog nodes use empty `sceneBackground` fields.

### Dawnless Crown
Captured Dawnless dialog nodes use empty `sceneBackground` fields throughout the inspected floor chain, including the final throne sequence. The same direct dialog `image` is reused heavily instead.

### AI avatars
Nine of the 23 captured enemy records still use the engine default avatar rather than bespoke character art. The most important production priorities are the final/keeper identities and the four base enemy archetypes; final acceptance and exact visual direction remain operator-owned.

## Proposed visual-production priority

Do not batch-generate. Follow the art skill one asset at a time with QC.

Priority A — final boss identity:
- The Endless Night avatar (currently default)
- Warden of the Severed Dawn avatar (currently default)
- final Dawnless throne background

Priority B — missing tower environment language:
- Stormcourt core background set (at minimum court / tribunal / eye-of-storm finale)
- Dawnless per-floor progression (surgery-cathedral / casket machinery / wire loom / severed-dawn keeper hall / black-sun throne)
- Marrow Vaults wiring completion, deciding whether the existing three plates intentionally recur or whether two additional plates are warranted

Priority C — remaining default-avatar archetypes/keepers:
- Umbral Reaver
- Hollow Lantern
- Starless Monk
- Nightveil Sentinel
- Warden of the First Dark
- The Twinned Reliquary
- The Loomwright

Before generation, use the current art spec/reference-pack workflow and generate the shot list from the captured quest graph rather than treating this hand audit as the production manifest.

## Readiness matrix

| Area | Verdict | Reason |
|---|---|---|
| Capture closure | PASS | 3 read-only phases complete; phase 3 all point reads resolved |
| Quest graph / battle sequencing | PASS | 75 battles, 75 fail routes, 60 normal + 15 keeper dialog gates |
| AI record/profile integrity | PASS | 23 AI + 23 AiProfiles resolve |
| Reward reference integrity | BLOCK | 2 guaranteed keystone IDs resolve to zero live rows |
| Chest reward | BLOCK | live loot table empty |
| Repeatability/economy safety | BLOCK | Marrow `retryDelay:none` pays ryo/tokens/prestige/chase chance |
| Static balance plausibility | AMBER | cap compression + final boss multiplier/control spike |
| Calibrated combat balance | UNVERIFIED | no declared-loadout live calibration evidence |
| Visual coverage | BLOCK for final-polish bar | sparse Marrow wiring; Storm/Dawnless backgrounds absent; default AI avatars remain |
| Final acceptance | HOLD | operator decisions + corrective writes/readback + playtest still required |

## Safest closeout sequence

1. Operator rules Marrow repeatability model and reward curve.
2. Operator defines/approves the two keystone records or replacement IDs and the Endless Night Chest loot table.
3. Fable/normal implementation owner authors the corrective mutation manifest(s) from those decisions.
4. Operator runs the protected live write; capture postflight/read-back.
5. ChatGPT independently reviews exact post-write SHA/capture.
6. In parallel, produce visual assets one at a time under the current art spec, then hand approved files/wiring to the normal implementation owner.
7. Run declared-loadout combat calibration, especially the final boss.
8. Final operator acceptance/publishing decision.
