# The Crowned Captain: solo boss fight, offline tuning (2026-10-28)

The Crowned Captain is Crownhold's last fight (D5.BOSS, live id `7QofodAiUwIoM-voiA2p6`). This report tunes him for one
average endgame player and exports a build spec.

- **Engine:** the game's combat engine at `c86f43f4`, in memory, with the live damage settings.
- **Requests:** zero live requests and no credentials.
- **Spec:** `crowned_captain_spec.json`.
- **Raw results:** `results/crowned_captain_tuned.json` (60 seeds with dodging, 60 without).
- **Sample traces:** `results/crowned_captain_trace_seed3.txt` and `..._seed5.txt`.
- **Script:** `engine/crowned_captain.ts`.
- **Inputs:** `data/crowned_captain_inputs.json`, built by `tools/build_crowned_captain_inputs.py`.

Nothing here is pushed or authorised for the live game. The spec carries placeholder ids `cc-*` for the 10 new jutsu.

## Current tuning: HP doubled (director, 2026-10-28)

The director doubled his HP (pools 2.5 to 5, 25,250 HP) so that phase 1 lasts. The Recall echo is unchanged.

**What was retuned, and why:**
- **Unavoidable damage down:** damage rows go from +100% and +75% to a single **+50%** row.
- **Set pieces more often:** Crownfall's cooldown goes from 4 to **3** and Command Absolute's from 8 to **6**. Each set
  piece is a full boss turn that a dodger takes no damage from. A player who ignores the marks gets hit more often.
- **Set-piece damage is unchanged:** Crownfall 180, Command Absolute 130 plus stun and seal, Shardstorm 180.
- The rules and the rest of the kit are unchanged.

| 60 seeds per mode | Dodging on | Dodging off (marks ignored) |
|---|---:|---:|
| Win rate | **93.3%** (56/60) | **5%** (3/60) |
| Rounds to win, median [p10-p90] | **23 [23-23]** (range 21-25) | 22 |
| Player HP left at a win, median / p10 | **22.8% / 8%** (2 wins at almost 0%) | ~0% |
| Losses by phase (1 / 2 / 3) | 0 / 3 / 1 | 2 / 47 / 8 |
| **Phase lengths**, median: phase 1 (100-60%) / phase 2 (60-30%) / phase 3 to the kill | **7 / 10 / 6 rounds** (phase 2 starts r7, phase 3 r17) | 7 / 10 / - (most die in phase 2) |
| The Last Directive cast | 95% | 18% |
| Idle turns: boss / player | 3.8% / 0% | 0% / 0% |
| Dodge moves per fight; moves refused onto a mark | 4.6; 2.0 | - |
| Set pieces that landed with no mark the turn before | 0 | 0 |

The fight now has one mode: 48 of 56 wins take exactly 23 rounds. The two-mode split of the first tuning is gone.

**Set pieces per fight** (marked / landed / hit; damage per hit is HP actually lost):

| Set piece | Dodging on | Dodging off |
|---|---|---|
| Crownfall | 2.1 / 2.1 / 0 | 2.1 / 2.1 / 1.2 (59%), 1,612 per hit |
| Command Absolute | 1.9 / 1.0 / 0 | 1.3 / 1.3 / 1.3 (100%), 1,077 per hit, plus stun and seal |
| Shardstorm | 0.9 opener / 3.0 volleys / 0 | 0.2 / 0.5 / 0.1 (few reach phase 3) |
| Recall | 1.1 casts | 1.2 casts |

**Damage to the player by source:**

| Dodging on | | Dodging off | |
|---|---:|---|---:|
| Extermination Order | 35.1% | Crownfall | 33.3% |
| echo | 19.7% | Command Absolute | 22.6% |
| Devouring Grasp | 17.6% | Extermination Order | 15.4% |
| Scorching Rend | 13.4% | echo | 9.6% |
| Cursed Thread Weave | 6.5% | Scorching Rend | 6.6% |
| Final Command | 4.5% | Devouring Grasp, Cursed Thread Weave, Final Command, Keelbind, Solar Bow, Ruin Refrain, Shardstorm | 12.5% together |
| Keelbind, Solar Bow, Ruin Refrain | 3.1% together | | |

**Retune path at pools 5** (40 seeds per mode; on = win %, rounds, HP left; off = win %):

| Damage rows | CF cd | CA cd | Set pieces CF / CA / SS | On | Off |
|---:|---:|---:|---|---|---:|
| 1.75 (old) | 4 | 8 | 180 / 130 / 180 | 0% (dies in phase 2) | 0% |
| 1 | 4 | 8 | same | 0% | 0% |
| 0.5 | 4 | 8 | same | 45%, 25, 0% | 5% |
| 0 | 4 | 8 | same | 55%, 25, 12% | 5% |
| 0 | 4 | 5 | same | 32.5%, 25, 11% | 5% |
| 0 | 3 | 5 | same | 100%, 23, 38% | 5% |
| 0.25 | 3 | 5 | same | 100%, 23, 30% | 5% |
| 0.5 | 3 | 5 | same | 90%, 23, 23% | 0% |
| **0.5** | **3** | **6** | **same** | **92.5%, 23, 23% (tuned; 60 seeds: 93.3%)** | **5%** |

**What is still not as designed:**
- **The fight is 23 rounds, not 12-15.** The director accepted a longer fight with this change.
- **Phase 2 is the longest, at 10 rounds.** In it, Extermination Order and the echo deal most of the damage a dodger
  takes, and all 3 phase-2 losses happen there.
- **Phase 1 now lasts 7 rounds.** Crownfall fires about twice, but Final Command, Keelbind and Ruin Refrain still deal
  under 7% of the damage. They sit below Crownfall and Cursed Thread Weave in the rule order, and Crownfall now holds
  every third turn.
- **His damage still sits above the ladder,** at x1.5 rows x1.6 from The Crown's Will (x2.4), plus the Directive.

Everything below this section is the first tuning (pools 2.5), kept for the record. Its engine facts, probe answers and
open decisions still stand.

---

## First tuning (pools 2.5, superseded)

### Headline (first tuning, 60 seeds per mode)

| | Dodging on | Dodging off (marks ignored) |
|---|---:|---:|
| Win rate | **93.3%** (56/60) | **1.7%** (1/60) |
| Rounds to win, median [p10-p90] | **15 [13-16]** | 16 (one win) |
| Player HP left at a win, median / p10 | **39.3% / 30.8%** | 2% |
| Where losses happen (phase 1 / 2 / 3) | 0 / 4 / 0 | 3 / 9 / 47 |
| Boss reaches phase 2 / phase 3 (median round) | r4 / r9 | r4 / r8.5 |
| The Last Directive cast | 93.3% of fights | 80% |
| Idle turns: boss / player | 0% / 0% | 0% / 0% |
| Dodge moves per fight; moves refused onto a mark | 4.9; 1.0 | - |
| Set pieces that landed with no mark the turn before | 0 | 0 |

**The win distribution has two modes.** The fight is nearly deterministic; only the spawn tile and the 10% random
barriers vary.

| Branch (dodging on) | Wins | Phase 3 starts | Rounds | Player HP left (median) | What happens |
|---|---:|---|---:|---:|---|
| Fast | 24 | round 7 | 13 | 87% | The player's single-target jutsu stay on him through phase 2. |
| Slow | 32 | round 10 | 16 | 32% | The echo stands closest, so the auto-player spends 2-3 turns on it while Extermination Order and Scorching Rend land. |

- The 4 losses are all slow-branch, in phase 2.
- The median of 39% HP sits between the two modes.
- A real player who "focuses him" plays the fast branch. One who fights every echo plays the slow branch.

### Set pieces: how often each fires and hits

Per fight, averaged. "Hit" means the player stood on a pattern hex when it landed. Damage per hit is the HP actually
lost, so it is capped by the HP left.

| Set piece | Dodging on: marked / landed / hit | Dodging off: marked / landed / hit | Damage per hit (dodging off) |
|---|---|---|---:|
| Crownfall (phase 1) | 1.0 / 1.0 / 0 | 1.0 / 1.0 / 0.6 (60% of landings) | 2,750 |
| Command Absolute (phase 2) | 1.0 / 0.9 / 0 | 0.9 / 0.9 / 0.9 (100%) | 1,787, plus a 2-round stun and seal |
| Shardstorm (phase 3; landings are volleys) | 0.9 opener / 4.6 volleys / 0 | 0.8 / 1.7 / 0.7 (42%) | 709 (most victims already low) |
| Recall | 1.0 cast; the echo deals 25% of all damage the player takes | 0.9 | - |

### Damage to the player by source (share of all damage taken)

| Dodging on | | Dodging off | |
|---|---:|---|---:|
| Extermination Order | 34.0% | Command Absolute | 27.7% |
| Scorching Rend | 27.1% | Crownfall | 27.4% |
| echo (Sanctum Vanguard) | 24.9% | Extermination Order | 13.2% |
| Final Command | 5.0% | Scorching Rend | 9.8% |
| Devouring Grasp, Ruin Refrain, Cursed Thread Weave, Solar Bow, Keelbind | 9% together | echo / Shardstorm | 9.6% / 8.6% |

## The setup

**The player** is the harness's `average` tier:
- level-100 JONIN with capped stats, so 6,250 HP with the set;
- the full Kitsune set, worn through the item path;
- the 9 level-25 PvE jutsu (Fire/Wind);
- driven by the harness rotation (`playerRules`), with full pools.

**The battle** is a plain QUEST battle, because Crownhold's `start_battle` objectives call `initiateBattle(..., "QUEST")`.
- The grid is **12 x 10** (`getDefaultBattleSizes("QUEST", 100)`).
- The isolated battlepyramid flag does not change the battle type or the grid.
- Random initial barriers are on.

**The dodge rule** is a declared test input, run through the engine's own Move, Replacement Technique and Cleanse
actions:
1. At each action step, if the player stands on a live danger mark (`tg_heavy` or `tg_control` ground visual), they
   step to the nearest unmarked free hex:
   - Replacement Technique when that hex is 2 or more steps away, within 5, and the technique is ready;
   - otherwise one Move step.
   If rooted, they use the basic Cleanse first. In 60 runs that never came up.
2. They never end a move on a marked hex. An auto-combat move onto one is replaced by ending the turn.

## The boss record (first-tuning values; the current values are in the section above and in the spec)

| Field | Value | Note |
|---|---|---|
| poolsMultiplier | **2.5** (12,625 HP) | push/272 had 3.5 |
| statsMultiplier | 5.83 (unchanged) | Inert in battle; see engine fact 1 |
| Innate damage rows | **+100% and +75%** (x3.5), plus sealprevent | |
| The Crown's Will (opener) | +60% damage given and +25% stats | Total x5.6 before the Directive's +30% |
| Throne | (9,4) | He walks there on his first turn and never moves again (reached in 100% of runs) |

**Kit (22 jutsu):**
- Arakane's kit minus Rapid Fire (live: Shuriken Storm), Braced Strike and Surging Overflow. Live names differ from the
  package names:

  | Package name | Live name |
  |---|---|
  | Hexweave | Cursed Thread Weave |
  | Zephyr Lance | Wind Spear |
  | Apex Hunger | Oni's Hunger |
  | Worldbreaker Chorus | Great Bell Toll |

- Ruin Refrain replaces Worldbreaker Chorus.
- Plus Final Command and Keelbind, from the old Crowned Captain kit (push/249 capture).
- The Last Directive, Extermination Order and the Countermand item are kept, along with Solar Bow and Crossbow.
- Oni's Hunger is replaced by **The Crown's Will**, a Crownhold-only copy with the same effects. It carries
  `cc_crown_aura` and the opening log line.
- Plus 9 new set-piece and Recall records.

**Set pieces:**

| Set piece | Telegraph | Detonation | Pattern |
|---|---|---|---|
| Crownfall | 100 AP, cd 4; `tg_heavy` | 100 AP, damage 180; `cc_crownfall` | A fan of 5 rays (36 hexes) from the throne |
| Command Absolute | 100 AP, cd 8; `tg_control` over the hall, `tg_safe` on 3 stars, `cc_phase_shift` | 100 AP, damage 130 + stun (60 AP, 2r; `dt_control`) + seal 2r, log "Kneel."; `cc_command_absolute` | Stars at (7,1) (5,4) (8,8), each 4 hexes from the throne, so the player keeps jutsu range on a star |
| Shardstorm | Opener 60 AP | Three volleys, 60 AP each, damage 180; each also marks the next pattern; `cc_shardstorm` | Rotation by marker |
| Recall | - | 60 AP, cd 8, `cc_recall`; summons Sanctum Vanguard (D5.REG1, `pshn-LkaC5vIgI6EOv68I`) beside the throne | Echo: 2,500 HP, 70% stats, 3 rounds |

- **Shardstorm patterns:** each pattern marks one colour of the hex 3-colouring, a third of the hall. A clear hex is
  always adjacent. Why a third, not two thirds: fact 5.
- **Recall:** the condition is `does_not_have_summon` plus the cooldown.

**Rules (34, in order):**

| Rules | What they do |
|---|---|
| 0 | Walk to the throne |
| 1-5 | The detonations, each keyed `has_effect` on its own 1-round marker |
| 6-11 | **Phase 3** (under 30%): The Last Directive, then Purging Stance on afterburn or poison (fact 6), then Shardstorm, then Extermination Order, then end turn |
| 12-19 | **Phase 2** (under 60%): Command Absolute, Recall, Stolen Form, Extermination Order, Scorching Rend, Devouring Grasp, Countermand, then end turn. The end turn keeps phase-1 moves out |
| 20-33 | **Phase 1**: The Crown's Will (round 1), Arakane's Veilstep/Countermand/Purging/Wind Spear rules, Crownfall, Cursed Thread Weave, Final Command, Keelbind, Ruin Refrain, Scorching Rend, Devouring Grasp, Solar Bow, end turn |

The Last Directive gets a cosmetic edit only:
- its battle log becomes the design's "\"Preserve command.\" The crown blazes.";
- the finalstand row gets `cc_last_directive` and `cc_phase_shift`.

Its effects are unchanged: finalstand, clearprevent, +30% damage given, 5 rounds (director: no clear strips it).

**Validation:** every new record and the edited Last Directive pass `JutsuValidator`. Every rule passes `AiRule`. The AI
record passes `insertAiSchema`, including `maxPoolsMultiplier`.

## Tuning path (dodging on / off; earlier rows ran on earlier code, see the engine facts)

| Step | Seeds | Pools | Damage rows | Set pieces CF / CA / SS | Echo HP / power / cd | On: win, rounds, HP | Off: win |
|---|---:|---:|---:|---|---|---|---:|
| First pass, stars far, 2-round marks | 20 | 3 | 1 | 90 / 60 / 70 | 6,000 / 100 / 2 | 0% (stalls in phase 2) | 0% |
| Stars moved into range | 20 | 3 | 1 | 90 / 60 / 70 | 6,000 / 100 / 2 | 80%, 20, 32% | 0% |
| Echo cheaper | 20 | 2.5 | 0.5 | 150 / 110 / 130 | 2,500 / 70 / 5 | 85%, 18, 61% | 65% |
| Set pieces up | 20 | 2.5 | 0.5 | 200 / 150 / 170 | 2,500 / 70 / 6 | 95%, 12*, 79% | 5% |
| Final Stand fix (Purging Stance), 60-AP volleys | 20 | 2.5 | 1 | 200 / 150 / 170 | 2,500 / 70 / 6 | 85%, 16, 68% | 5% |
| One-third Shardstorm, CA cd 8 | 20 | 2.25 | 1.5 | 200 / 150 / 200 | 1,500 / 70 / 8 | 90%, 16, 43% | 5% |
| Echo beside the throne | 20 | 2.25 | 2 | 200 / 150 / 200 | 2,500 / 70 / 8 | 90%, 15, 26% | 5% |
| | 40 | 2.25 | 2.5 | 150 / 110 / 150 | same | 52.5%, 13, 86% | 5% |
| **Tuned** | 60 | **2.5** | **1.75** | **180 / 130 / 180** | **2,500 / 70 / 8** | **93.3%, 15, 39%** | **1.7%** |

\* Rounds of 12 before the Final Stand fix were the boss dying through the Last Directive (fact 6).

## Engine facts found or re-verified (each checked in source and/or by run)

**Stats and records:**

1. **statsMultiplier does nothing above about 4.7 for a JONIN AI.**
   - `initiateBattle` caps every participant with `capUserStats(rank)`: offence/defence 1.3M, generals 400k.
   - The push/272 boss (live readback 1,622,255.8 each) fights with exactly the player's stats.
   - Only pools and damage rows tune him.
   - Rank ELITE JONIN would lift the cap. That is a director call; not used.

2. **`increasepoolcost` needs `rounds >= 2` in the live schema** (`validators/combat.ts` IncreasePoolCostTag), so the
   probe's 1-round marker cannot be stored.
   - A 2-round marker overlaps the next set piece's.
   - Each set piece therefore carries its own harmless 1-round self effect as its marker:

     | Set piece | Marker |
     |---|---|
     | Crownfall | `fleeprevent` |
     | Command Absolute | `robprevent` |
     | Shardstorm volleys | `onehitkillprevent`, `increaseaggro`, `decreaseaggro` |

   - None of these is cleansable (not in `isNegativeUserEffect`).
   - The player's basic Clear could strip a marker and cancel a set piece; the auto-player never uses Clear.

**Geometry and patterns:**

3. **The battle grid is FLAT with odd columns offset** (`getBattleGrid`).
   - `engine/probe_telegraph.ts` measured its rings on a default (POINTY) honeycomb grid. Its "row parity" rule is
     really column parity on the battle grid.
   - All patterns here are BATTLEFIELD-origin, absolute, so parity does not matter.
   - One jutsu can carry several patterns: per-tag `target: "COORDINATES"` with its own `coordinateTargeting`, plus a
     SELF tag (`util.ts` getActionAffectedTiles, `actions.ts` insertAction). This is how one telegraph lays `tg_heavy`
     on the danger hexes and `tg_safe` on the safe ones.

4. **Marks must be 1-round visuals.**
   - A 1-round ground visual stays through the next round, which covers the detonation turn.
   - A 2-round visual stays a whole round after the hit and reads as a new warning.
   - Visuals never play a `disappearAnimation`: `expireGroundEffects` drops expired visuals before that branch. So
     `dt_heavy` is unused (spec, `animations`).

5. **Turn order can put him before the player in a round.**
   - When it does, last volley's mark is still on the floor beside the new one.
   - With two-thirds patterns the two marks covered every hex, and a careful player had nowhere to stand. That caused 7
     of 9 losses in one 20-seed batch.
   - One-third patterns fix it, because a hex of the third colour is always adjacent.

**Damage and the Last Directive:**

6. **Final Stand does not stop damage-over-time.**
   - `process.ts` applies afterburn, poison and drain ticks outside `calcAdjustedDamage` and `applyFinalStandDamage`.
   - Each damage component (damage, residual, wound) is floored separately against the HP before the hit, so their sum
     can still kill.
   - The player's Tempestual Fury afterburn killed him under the Last Directive in 2 of 60 runs.
   - The fix in rules: under 30% he uses Purging Stance on afterburn or poison before Shardstorm. After that there were
     no early kills in 60 runs.
   - The engine issue itself is worth an upstream report: Final Stand is meant to be a floor.

**Targeting:**

7. **Command Absolute's detonation is an OTHER_USER cast over the pattern.**
   - That makes stun and seal real user effects. A ground stun would only stun while the player stands on the hex.
   - The engine accepts the cast only if some unit stands in the pattern. The echo counts, and friendlyFire ENEMIES spares
     it.
   - If the player is on a star and no echo is up, the cast is refused, so the "Kneel." log and animation do not play, and
     he takes his next rule. That is why landings are 0.9 per fight with dodging, not 1.0.

8. **Initial barriers punch holes in GROUND telegraphs.** A barrier hex gets no mark, while the OTHER_USER Kneel still
   covers it if the barrier is destroyed. Rare; noted.

## Probes asked for in the brief and by the coordinator

**(3) Can a ground effect grant `injectjutsus` to whoever ends a move on it? No** (`results/probe_ground_inject.json`).
- The test: a boss jutsu laid an `injectjutsus` ground effect (3 rounds), with friendlyFire ENEMIES and with ALL. The
  player moved onto it and stood there.
- Result: no persistent effect, and the jutsu never appeared in their actions.
- A ground `increasedamagetaken` tile behaves the same way.
- Why: ground effects reach a unit only transiently while each action resolves. `applyEffects` gives them rounds 1, and
  they are "not forwarded to the next round". `handleInjectedJutsus` reads the persistent effects, so the grant never
  shows.

Two related answers came out of the same probe:
- **Preloaded: yes.** `initiateBattle` loads every `injectableInBattle` jutsu into `extraState.jutsus`
  (`routers/combat.ts` ~2321). The harness does the same.
- **One-use: yes, when the inject is cast directly on the unit.** With OTHER_USER and SINGLE, the jutsu appeared at once
  and was used once. With cooldown 20 against a 3-round grant, it did not come back.

So heal or buff tiles must be ordinary ground effects, such as heal or increasedamagegiven, which the engine applies
while the unit stands there. A granted action must be cast on the unit.

**Dropped by the director:**
- (4) can a clear remove finalstand;
- (2) the Crown Shard weakness window.

The Crown Shard is cut. Shardstorm's safe hexes are plain. The Last Directive is a 5-round survival test.

The source answer to (4), found before the drop: no.
- `clear` checks `clearprevent` first (`tags.ts` clear).
- `finalstand` is not in `isPositiveUserEffect`, so a clear would never remove it anyway.

## What does not work as designed, and open decisions

- **Phase 1, the duelist, is short.**
  - The player's opening burst takes him from 100% to 60% in about 3 turns.
  - So Crownfall fires once and Final Command, Keelbind and Ruin Refrain barely act: 9% of the damage taken together.
  - Making the duel phase longer needs more HP, which pushes the fight past 15 rounds. The Directive alone adds 6. The
    alternative is a different phase threshold. **Director's call.**
- **His HP sits below the push/272 ladder.**
  - Pools are 2.5 against 3.5, because the 5-round Directive plus 12-15 rounds forces it.
  - His damage is above the ladder (x5.6), so "above the ladder" holds for damage, not health.
- **Two modes, not one average**, as shown above. The slow branch is the "hard" fight (32% HP left, all 4 losses). The
  fast branch is comfortable (87% HP left).
- **Recall, then Command Absolute.**
  - Command Absolute's cooldown is 8, so it comes once per phase 2.
  - Each pass costs him two full turns (mark, Kneel) in which he does not attack.
  - Shorter cooldowns made phase 2 a stall (the first pass: 0% wins).
- **Countermand (clear) on the player** removes the player's jutsu buffs. The Kitsune effects stay: `fromType` armor is a
  persistent source (`tags.ts` persistentEffectSourceTypes).
- **Kit cooldowns are untouched.** No `cooldowns` override is used, so the shared live records (Final Command and so on)
  need no copies.
- **Every set-piece number assumes the live damage settings** (`data/dmg_config_live.json`).

## Reproduce

```bash
python3 harness/skyglass_wreck_sim/tools/build_crowned_captain_inputs.py --check
H=$PWD/harness/skyglass_wreck_sim
TNR_SCRIPT=crowned_captain.ts harness/skyglass_wreck_sim/run.sh --seeds 60 \
  --out $H/results/crowned_captain_tuned.json --write-spec $H/crowned_captain_spec.json \
  --probe-inject --probe-out $H/results/probe_ground_inject.json
# one fight, action by action (both dodge modes):
TNR_SCRIPT=crowned_captain.ts harness/skyglass_wreck_sim/run.sh --trace 5 --seeds 0
# a tuning variant (absolute path; any DEFAULTS key):
TNR_SCRIPT=crowned_captain.ts harness/skyglass_wreck_sim/run.sh --params /abs/variant.json --seeds 40
```

- 60 seeds per mode take about 1 minute.
- `--params` and `--write-spec` paths must be absolute, because run.sh resolves only `--out`/`--override`.
