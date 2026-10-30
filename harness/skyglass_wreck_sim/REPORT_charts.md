# Skyglass charts, solo + companion pet: offline simulation (2026-10-28)

Branch `fable/skyglass-charts-sim` (from hunts `6652fb7c`, Wreck `ad379117` merged; Wreck pet-placement fix `c301632b` reimplemented).
Engine run at the harness pin `c86f43f4`; source checks cite `theninjarpg@2af4b320` (identical combat/AI code paths for
what is used here). Zero live requests, no credentials. Every run uses the seeded virtual clock; same-seed reruns are
identical including positions (`--repro`, checked on lowtide/L50, reliquary, fall, burning with the Captain ally).

Design player: the hunts' **L100 "average"** (JONIN caps, full Kitsune set, 9 PvE jutsu) and **L50 "lvl50"** (level budget,
Chunin kit, no gear), each with/without Kitsune; one modelled companion pet (`model.ts petFor`). Minutes = rounds x 15 s.

## Files

| File | What |
|---|---|
| `engine/charts.ts` | records (copies, hazards, ember jutsu), run sequences, `scaledRow` (engine scaling) |
| `engine/charts_main.ts` | runner; `--trace`, `--repro`, `--probe-embers`, `--sweep`, `--spec-out` |
| `engine/sim.ts` | + quest NPC allies (`allyIds`), player-loss rule, ember-aware dodge, ally marks ignored, pet placement fix |
| `engine/hunts*.ts` | adapted to the Wreck owner's consolidated `kits.ts` (`buildEndgame`/`DEFAULT_PARAMS` were removed by the merge) |
| `overrides/charts.params.json` | tuned values |
| `charts_spec.json` | 23 AI records + 3 jutsu (all pass insertAiSchema / JutsuValidator), run sequences, objective shape |
| `results/charts_*.json`, `tools/charts_tables.py` | results and the tables below |

```
TNR_SCRIPT=charts_main.ts harness/skyglass_wreck_sim/run.sh --params harness/skyglass_wreck_sim/overrides/charts.params.json \
  --runs lowtide,nightwatch --variants L50,L50kit,L100,L100noarmor --seeds 40 [--no-dodge] [--no-twist] --out results/x.json
```

## Results (40 seeds per cell)

### Common charts (opponent_scaled_to_user), 40 seeds per cell

| Run | Player | Base clear (dodge on / off) | Press-on won of reached (on / off) | Base minutes (on) |
|---|---|---|---|---:|
| lowtide | L50 | 39/40 (98%) / 40/40 (100%) | 26/39 (67%) / 22/40 (55%) | 3.3 |
| lowtide | L50kit | 40/40 (100%) / 40/40 (100%) | 40/40 (100%) / 40/40 (100%) | 2 |
| lowtide | L100 | 40/40 (100%) / 40/40 (100%) | 40/40 (100%) / 40/40 (100%) | 2 |
| lowtide | L100noarmor | 40/40 (100%) / 40/40 (100%) | 38/40 (95%) / 39/40 (98%) | 2.3 |
| nightwatch | L50 | 39/40 (98%) / 39/40 (98%) | 30/39 (77%) / 15/39 (38%) | 4.3 |
| nightwatch | L50kit | 40/40 (100%) / 40/40 (100%) | 40/40 (100%) / 40/40 (100%) | 2 |
| nightwatch | L100 | 40/40 (100%) / 40/40 (100%) | 40/40 (100%) / 40/40 (100%) | 2 |
| nightwatch | L100noarmor | 40/40 (100%) / 40/40 (100%) | 37/40 (92%) / 16/40 (40%) | 2.5 |

Per fight (dodge on): won/reached, median rounds, median HP start->end (% of base max HP)

| Run | Player | Fights |
|---|---|---|
| lowtide | L50 | F1 40/40 r5 100->47.2; F2 40/40 r4 47.3->57.6; F3 39/40 r5 57.6->57.8; P4 26/39 r7 57.8->38.2 |
| lowtide | L50kit | F1 40/40 r3 147.1->146.4; F2 40/40 r2 147.1->146.5; F3 40/40 r3 147.1->147.1; P4 40/40 r2 147.1->147.1 |
| lowtide | L100 | F1 40/40 r3 123.8->87; F2 40/40 r2 110.8->110.7; F3 40/40 r3 123.8->123.4; P4 40/40 r2 123.8->113.1 |
| lowtide | L100noarmor | F1 40/40 r4 100->38.2; F2 40/40 r3 38.2->35.2; F3 40/40 r3 35.2->34.7; P4 38/40 r3 34.7->25.7 |
| nightwatch | L50 | F1 40/40 r5 100->47.2; F2 40/40 r4 47.3->59.3; F3 39/40 r8 59.2->53.1; P4 30/39 r10.5 53.1->35 |
| nightwatch | L50kit | F1 40/40 r3 147.1->146.4; F2 40/40 r2 147.1->146.5; F3 40/40 r3 147.1->146.1; P4 40/40 r3 147.1->147.1 |
| nightwatch | L100 | F1 40/40 r3 123.8->87; F2 40/40 r2 110.8->110.3; F3 40/40 r3 123.8->122.4; P4 40/40 r3 123.8->123.8 |
| nightwatch | L100noarmor | F1 40/40 r4 100->38.2; F2 40/40 r2.5 38.2->35.7; F3 40/40 r4 35.7->20.5; P4 37/40 r3 20.5->12 |

### Rare and tainted charts (L100, endgame), 40 seeds per cell

| Run | Player | Base clear, twist on (dodge on / off) | Base clear, twist OFF (on / off) | Press-on won of reached (on / off) | Base minutes (on) |
|---|---|---|---|---|---:|
| reliquary | L100 | 35/40 (88%) / 2/40 (5%) | 40/40 (100%) / 39/40 (98%) | 29/35 (83%) / 0/2 (0%) | 9.3 |
| reliquary | L100noarmor | 0/40 (0%) / 0/40 (0%) | - / - | 0/0 (-) / 0/0 (-) | 0 |
| fall | L100 | 36/40 (90%) / 9/40 (22%) | 40/40 (100%) / 15/40 (38%) | 21/36 (58%) / 1/9 (11%) | 5 |
| fall | L100noarmor | 0/40 (0%) / 0/40 (0%) | - / - | 0/0 (-) / 0/0 (-) | 0 |
| rotted | L100 | 20/40 (50%) / 1/40 (2%) | 28/40 (70%) / 9/40 (22%) | 7/20 (35%) / 0/1 (0%) | 5.5 |
| rotted | L100noarmor | 0/40 (0%) / 0/40 (0%) | - / - | 0/0 (-) / 0/0 (-) | 0 |
| burning | L100 | 27/40 (68%) / 2/40 (5%) | 39/40 (98%) / 0/40 (0%) | 22/27 (81%) / 0/2 (0%) | 3.8 |
| burning | L100noarmor | 0/40 (0%) / 0/40 (0%) | - / - | 0/0 (-) / 0/0 (-) | 0 |

Per fight (twist on, dodge on): won/reached, median rounds, median HP start->end (% of base max HP)

| Run | Player | Fights |
|---|---|---|
| reliquary | L100 | F1 40/40 r4 123.8->112.3; F2 35/40 r11 123.8->108.7; F3 35/35 r10 123.8->111.8; F4 35/35 r10 123.8->71.6; P5 29/35 r8 95.4->39 |
| reliquary | L100noarmor | F1 37/40 r6 100->49.6; F2 0/37 rNone -; F3 0/0 rNone -; F4 0/0 rNone -; P5 0/0 rNone - |
| fall | L100 | F1 40/40 r6 123.8->102.5; F2 39/40 r7 123.8->81.5; F3 36/39 r7 105.3->70.6; P4 21/36 r9 94.3->30.7 |
| fall | L100noarmor | F1 13/40 r7 100->33.2; F2 0/13 rNone -; F3 0/0 rNone -; P4 0/0 rNone - |
| rotted | L100 | F1 29/40 r11 86.6->39.6; F2 20/29 r12 63.4->37.6; P3 7/20 r9 61.4->25.5 |
| rotted | L100noarmor | F1 0/40 rNone -; F2 0/0 rNone -; P3 0/0 rNone - |
| burning | L100 | F1 35/40 r8 86.6->34.9; F2 27/35 r5 58.7->32.7; F3 27/27 r3 56.5->50.3; P4 22/27 r3 74->67.7 |
| burning | L100noarmor | F1 0/40 rNone -; F2 0/0 rNone -; F3 0/0 rNone -; P4 0/0 rNone - |

### Steeping (Steeping Horror scaled to the player), 40 seeds

| Player | Win (dodge on / off) | Rounds (on) | HP start->end median (on) |
|---|---|---|---|
| L100 | 31/40 (78%) / 0/40 (0%) | 9 | 123.8->34.5 |
| L100noarmor | 0/40 (0%) / 0/40 (0%) | None | 100->None |

### Twist hazards (twist on, dodge on / off, L100)

| Run | Fight | Hazard marks / blasts per fight | Blast hit % (on / off) | Hazard died median round (on) |
|---|---|---|---|---|
| reliquary | 2nd echo: Sealwright + Lingering Echo (Pour Line | 2.8 / 1.1 | 4.4 / 89.2 | 11 |
| reliquary | 3rd echo: Skyglass Sentinel + Lingering Echo (Po | 4.5 / 2 | 1.4 / 76.2 | 10 |
| reliquary | last echo: First Blade + Lingering Echo (Pour +  | 4.2 / 2.5 | 3.5 / 78.3 | 9 |
| rotted | last pair: Skyglass Sentinel + First Blade + Lin | 2.5 / 1.6 | 8.7 / 100 | 11 |
| fall | burning deck: Deck Warden + Seal Charge + embers | 0 / 0 | None / None | 4 |
| fall | gun deck: Arsenal Keeper + Deck Warden + embers | 0 / 0 | None / None | 3 |
| fall | the break: Core Horror + embers | 0 / 0 | None / None | 3 |
| burning | the break: Core Horror + embers | 0 / 0 | None / None | 3 |
| burning | gun deck with the Captain: Arsenal Keeper + Deck | 0 / 0 | None / None | 3 |
| burning | PRESS ON (proposed): First Blade on the burning  | 0 / 0 | None / None | 2 |

Ember metric note: "embers N hits" in the console counts every HP loss on the player's own steps in a Burning Deck
fight (it also catches Keelbind's drain); the ember behaviour itself is proven by the probe below.

## Reading against the targets

| Run | Target | Result (L100 Kitsune, dodge on unless noted) |
|---|---|---|
| Low Tide / Night Watch base | 85-90%, ~5 min | L50: 98% / 98%, 3.3 / 4.3 min. L100 (both builds) and L50+Kitsune: 100%, ~2 min |
| Commons press-on | ~60% | L50: 67% / 77% of reached. L100: 95-100% |
| Sealed Reliquary | 80% / press-on 55% | 88% / 83% (9.3 min) |
| The Fall | 80% / 55% | 90% / 58% |
| Rotted Reliquary | ~55% | 50% (press-on Replicant Zero 35%) |
| Burning Heading | ~55% | 68% (press-on 81%) |
| Steeping | ~75% | 78% |

- **Twists matter.** Ignoring the twist (dodge off) collapses every rare: Reliquary 88% -> 5%, Fall 90 -> 22%, Rotted
  50 -> 2.5%, Burning 68 -> 5%. With the hazards removed the same runs read 100/100/70/98% (dodge on) and 98/38/22/0%
  (dodge off): the Lingering Echo is what makes the Reliquary punish non-dodgers (97.5% -> 5%), and its blasts hit
  76-100% with dodge off against 1-9% with dodge on.
- **Without Kitsune every rare, tainted and steeping run is 0/40** (the same wall as the hunts: the set's +1,200 max HP
  is re-applied at every fight start, about +24% per fight, so "no refill" is soft for Kitsune wearers only).
- **Commons barely respond to dodging** (L50 99% either way): their only set piece is Tide Line (damage only, no push
  row in the library) and the press-on Wayfinder's scatter; dodge off mainly lowers the press-on rate (Night Watch L50
  77% -> 38%).
- Remaining misses are press-on/one-knob items: Reliquary press-on (Oathkeeper copy) is steep in its stats
  (pools 2 rows 2: 97%; 2.5/2: 83%; 3/3: 0% at 20 seeds); Burning Heading is 13 points easy (raise the afterburn or
  the Core Horror there); Rotted's Replicant Zero press-on is 35%.

## Tuned / new records (placeholder ids; `charts_spec.json` has kits, rules, stats)

- **Common-chart crew copies `chart-c-*` (7):** Deck Warden, Seal Charge, Arsenal Keeper, Skyglass Sentinel (pools 1.5,
  1 row), Wayfinder, First Blade (1.5, 1 row), Oathkeeper. Same kit/rules as the live record, `statsMultiplier 1`,
  pools 1 unless noted, plus one +100% damage-taken row and -50% damage given. Scaled to the player in battle.
- **Rare copies `chart-r-*` (7):** Foundry Warden 1.2/1 row, Sealwright 1/1, Sentinel 2/1, First Blade 1.2/1,
  Core Horror 2/2, The Captain 2/2, Oathkeeper 2.5/2. The hunt records are tuned as one boss from full HP
  (e.g. Sealwright + Echo at hunt stats cost 83% and ran 20 rounds), so a 4-boss carried-HP gauntlet needs lighter copies.
- **Tainted pair copies `chart-t-*` (4):** Foundry Warden, Sealwright, Sentinel, First Blade, all pools 1, no rows.
- **Lingering Echo** x3 (`chart-lingering-echo-2/3/4`, the Reliquary twist): Deck Warden statline, pools 2, 1 row, immobile;
  holds the fallen bosses' **library** pairs only (Pour Line = Omen/Eruption: Lines; + Script Lines = Seal Lines;
  + Tide Line = Rows A). Each pair marks on scheduled odd rounds (`specific_round`) and blasts next turn; it fades at
  round 10 (no rule matches, the engine's give-up path removes it, `ai_v2.ts` "exhausted and has to give up"). Median
  death round 9-11 = it lingers the whole fight. **No new jutsu.**
- **Burning Deck** (`chart-burning-deck`, The Fall twist): Seal Charge statline, pools 3 (10,650 HP), immobile; lays
  **Spreading Fire I/II/III** (3 new jutsu: GROUND, COORDINATES rows 0-2 / 3-4 / 5-6, `drain` 5% max HP + `tg_ember`
  visual, 10 rounds, 40 AP) at rounds 1/4/7, safe ground shrinking to the bottom rows (the gangway).
- **Steeping Horror** (`chart-steeping-horror`): Core Horror kit/rules, no drop, pools 3.76 (18,988 HP), 3 rows, scaled.
- Replicant Zero (press-on): push/272 record with a solo edit pools 1.5, 1 row (`stats` in params; a copy, since the live
  record is Crownhold's D3 boss).
- Tainted twists: Rotted elementalseal 2 rounds every fight + entry 70%; Burning afterburn 60% for 4 rounds every fight +
  entry 70%. Rotted's last pair carries the Lingering Echo with Pour Line only (both pairs = 25-35% clear).
- RUL-2026-10-28-021 item 3 applied in the harness (Crown Stonebound's Erupting Ground damage rows ENEMIES only).

## Proposed press-on rooms (flag: undefined in the design)

| Run | Proposed room | Records |
|---|---|---|
| Low Tide Run | the chart room: a scaled Wayfinder | `chart-c-wayfinder` |
| Night Watch (Second Watch) | First Blade alone (the Seal Charge pair made it ~40%) | `chart-c-first-blade` |
| Sealed Reliquary | **the Oathkeeper** (a live crew record exists: `0PZU_FvlbM3ErYGlD5r56`; shared kit `dg-oathkeeper`) | `chart-r-oathkeeper` |
| The Fall | The Captain at the helm | `chart-r-the-captain` |
| Rotted Reliquary | Replicant Zero (ruled) | push/272 D3.BOSS, solo edit |
| Burning Heading | First Blade on the burning deck, Captain still beside you, embers | live First Blade + Burning Deck |

## Engine checks (source at theninjarpg@2af4b320; RUL-2026-10-28-022 model)

a. **Routing works; rewards are collected when objectives are done.** `getReward` pays every objective that is
   `done && !collected` (`libs/quest.ts:497-540`) whether or not the quest is resolved; non-resolved advances are claimed
   too (`commitQuestObjectiveRewards`, `routers/quests.ts:4009`). The quest reward pays only when `isQuestComplete`
   (`libs/quest.ts:480-495`), which for consecutive quests walks `selectedNextObjectiveId` to a done objective with no
   next (`libs/objectives.ts:110-142`); `win_quest` is instantly done (`libs/quest.ts:1514-1515`). In a "choose" quest the
   completion reward becomes a frozen pick offer (`libs/quest.ts:487-490`, `rewardMode`/`rewardPickCount`,
   `validators/rewards.ts:151-159`). So under RUL-022: put no Skyglass rewards on battle objectives; put the ladder exp,
   Treasury chance and profession drops on each `win_quest` ending; the pick is the quest reward.
b. **Press-on fall-back works.** A lost battle with `failObjectiveId` sets `selectedNextObjectiveId = failObjectiveId`
   and marks the battle objective done (`libs/quest.ts:1814-1845`). Routing it to the `win_quest` ending at the current
   step completes the quest (path ends on a done win_quest), so the player gets that ending's objective rewards **and**
   the completion pick. Caveat: because the lost battle objective is "done", any rewards authored on it pay as well -
   keep battle objectives reward-free.
c. **Steeping refund works, and entry items are paid again on every new run.** Lose -> `failObjectiveId` -> a
   `win_quest` ending carrying `reward_items: [the chart]` pays the item and ends the quest (as a): the 3 Core Rot stay
   spent. Entry items are checked and paid when a run starts; a fresh or restarted attempt pays again, only re-entering a
   still-open paid attempt keeps its receipt (`routers/quests.ts:3286-3299`). A retry therefore costs the chart + 3 Rot
   again. Note the refund ending counts as a completion (relevant to `maxCompletes`/achievement counting); a dialog step
   with `reward_items` followed by `fail_quest` is the alternative if that matters (objective rewards are claimed on
   non-resolved advances, quests.ts:4009ff).
d. **Yes, the cap counts everything.** Every run start increments `previousAttempts` (fresh insert = 1, restart +1:
   `routers/quests.ts:3663, 3684, 3703, 3720`), whatever the previous run's outcome; `isAvailableUserQuests` blocks a start
   once `previousAttempts >= maxAttempts` for `battlepyramid` (in `QuestTypesWithMaxAttempts`, `drizzle/constants.ts:1097`;
   check `libs/quest.ts:2484-2488`, enforced at start `routers/quests.ts:3226`), and `maxAttempts` is capped at 100
   (`validators/objectives.ts:906`). So failed runs and steeping retries all count if steeping is a Pyramid quest.
   Steeping needs no isolation, so it can be a non-capped type; `maxCompletes` (<= 100, line 907) also caps lifetime
   completions when `retryDelay` is "none" (`libs/quest.ts:2479-2483`).

**Also found in source:** `givePools` replaces the player's pools with % of effective max at battle start
(`routers/combat.ts:3291-3302`), so the 70% entry must sit on the **first** fight objective only; on a later one it would
refill or drain the carried pools. Allies: `allyAIs` go left of the targets and are never scaled
(`routers/combat.ts:2741, 2786, 3088`); the player's battle is lost when the player is out even if the ally fights on
(`libs/combat/util.ts:1972-1977`).

## Ember (`drain`) ground, proven (`--probe-embers`, `results/charts_probe_embers.json`)

- The cast does no damage (the Burning Deck's own step never changes player HP).
- A player standing on an ember is hit on its **next action**: standing still from round 1 loses 5% max HP (252) once
  per round from round 2; a player who walks off on its turn pays one tick per step it starts on an ember; a player who
  walks onto a laid band pays nothing until its next action there.
- `drain` is in `SHARED_COOLDOWN_TAGS` (`drizzle/constants.ts:265-286`): one band locks the others for 3 rounds, so bands
  are laid 3 rounds apart (a band every round is not possible with one caster). The tag's `rounds` max is 10.

## Can't be built as designed / closest alternative

1. **The commons cannot serve L50 and L100 alike.** `opponent_scaled_to_user` sets the target to the player's level and
   gives it `statsMultiplier x 0.5 x` the level budget (`libs/profile.ts:307-357`; `SCALED_AI_STAT_BUDGET_SHARE = 0.5`, `drizzle/constants.ts:1298`; applied at `routers/combat.ts:3088-3091`),
   capped at rank caps. An L100 endgame player sits at the JONIN caps (above the budget), an L50 player on the budget,
   and the Kitsune set adds +1,200 HP per fight (+47% of an L50 pool). So L50 needs `statsMultiplier 1` plus softening
   rows to reach 85-90%, which leaves L100 (and L50+Kitsune) at 100% in 2 minutes. Tuned for the L50 player; director
   call whether endgame players should find the commons trivial or the commons split by level.
2. **Schema floor:** `insertAiSchema` rejects `statsMultiplier < 1` and `poolsMultiplier < 1`, so softening uses innate
   +damage-taken / -damage-given rows (the easy-Wreck copies already use the first).
3. **The live hunt records cannot be reused for the rares or commons** without changing the hunts (stats are per
   record), so 18 stat-only copies are proposed (no new jutsu).
4. **Spreading fire:** the Burning Deck is a battle target; the auto-player usually kills it by round 3-4 (median), so
   in practice band I (sometimes II) lands. Killing the fire source is a legitimate counterplay, but if the fire should
   always reach the gangway, give the Deck heavy innate damage reduction (it then burns out on its own after band III).
5. **Tide Line** stays damage only (no push row in the library).
6. **Lingering Echo fade** uses the engine give-up path (battle log "is exhausted and has to give up"); a custom fade
   line needs a 1-round self-kill jutsu instead.

## Merge notes for the other lanes

- The Wreck merge removed `buildEndgame`/`DEFAULT_PARAMS` from `kits.ts`; hunts code here is adapted (rules only), and
  the consolidated shared rules change the hunts' fights (a 4-seed smoke run: Watch Captain 1/4). The hunts owner should
  re-run on the merged kits.
- `sim.ts` here adds allies, the player-loss rule, ember dodge and friendly-mark filtering; all are no-ops for fights
  without allies or ember tiles.

## Not done

No live requests, no browser, no push. Runs use the harness player model (no weapon, no cleanse use, CLOSEST_OPPONENT
targeting, which also hits hazards). Titles, rewards and objective manifests are not built.
