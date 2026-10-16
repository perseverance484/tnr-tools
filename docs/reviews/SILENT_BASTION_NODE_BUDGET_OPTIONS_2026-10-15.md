# Silent Bastion — objective budget options (design review)

**Status:** OPTIONS / INDEPENDENT DESIGN ANALYSIS — no new gameplay ruling, quest manifest, engine change, or publication authorization. Goal: evaluate a director-stated **90–100 objective budget** without flattening the five-division, protocol/puzzle, and checkpoint identity of Ghost Ship: The Last Directive. The director suggested possibly cutting the first division (**The Gatewarden / Outer Garrison**) because it is underpowered and dull; that was a **possibility, not an approved cut**.

**Repository locks inspected 2026-10-15:** `perseverance484/tnr-tools main@43ce6b2d22736cd90e3de52e66f620570e67888f`, authoring plan `chatgpt/silent-bastion-content-execution-plan-20261014@c9f30ee7c6dfb444ac28851d1fd4c8dd8f46f4d1`, Phase 1 native proof `claude/silent-bastion-phase1-validation-9628h6@33be3cd2fe504d508ade2ab04d15e45f4c752ed3`, game `studie-tech/TheNinjaRPG@13d40c4c1509ecf44262aba1b5120266011ea786`. Phase 1 tested the graph at upstream `c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd` and is **not automatically certified against newer source**.

**Authority and precedence:** `docs/00_INDEX.md`, `docs/RULINGS.md` (on Fable's Phase 1 branch, including RUL-2026-10-14-001), `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `state/silent_bastion_design.md`, `state/silent_bastion_release_plan.md`, `state/silent_bastion_phase1_graph.json` (r2), `docs/reviews/SILENT_BASTION_PHASE1_NATIVE_RESULTS.md`, `skills/building-tnr-content/references/quest.md` §3.7, game `app/src/libs/quest.ts` (`applyQuestResets`), `app/src/validators/objectives.ts` (ResetQuest and InstantStartBattle schemas), and `app/src/libs/objectives.ts` (consecutive path semantics).

## 1. Precisely where 178 nodes come from

The **r2 symbolic graph** contains **91 dialogs + 80 battle objectives + 5 reset_quest + 1 win + 1 fail = 178**. Each division is exactly **35 nodes**:

| Per division | Dialogs | Battle nodes | Reset | Total |
| --- | ---: | ---: | ---: | ---: |
| Initial lane (`.n.`) | 9 | 8 | 0 | 17 |
| Retry lane (`.r.`) | 9 | 8 | 0 | 17 |
| Shared `rN.retry` | 0 | 0 | 1 | 1 |
| **Total per division** | **18** | **16** | **1** | **35** |

Global aftermath + completion + final failure add **3** nodes: `5×35 + 3 = 178`.

**Only 25 distinct opponent encounter slots exist** (five commanders + 20 regulars). The 80 battle nodes are route/initial-versus-retry variants, not 80 distinct fights. The expanded graph exists to enforce player-facing **same-division 50% pool resets**, **Medical full heal (`givePools:100`)**, **player-side Combat buffs**, **clean/alert puzzle outcomes**, and each battle having a real dialog predecessor. The native harness passed ordinary r2 paths, including 20–25 fights per run, and verified retries on the pinned engine, while separately recording engine findings F1–F5.

The **90–100 budget is director-imposed here**, not a known universal game write-schema hard cap; Phase 1 successfully validated/saved the 178-node hidden fixture offline. The node target is still binding as a design constraint for future authoring.

## 2. Options with exact static node arithmetic

| Option | Node count | Encounters / clear-shortcut minimum | What changes | Evidence status |
| --- | ---: | --- | --- | --- |
| Keep r2 | **178** | 25 / 20 | Existing director-approved game shape; over budget | Native-tested at Phase 1 pin |
| Cut Outer Garrison only | **143** | 20 / 16 | Lose The Gatewarden division, one boss, four regulars, one puzzle/terminal | Direct subtraction, **not** retested |
| Keep five divisions; puzzle dialog routes directly to clean/alert boss, eliminating separate one-option boss approach dialogs | **158** | 25 / 20 | Saves **4 dialogs/division** (2 per lane); preserves effects and fights but shortens approach narrative | Source-compatible design idea, **not** native-tested |
| Cut Outer Garrison + direct puzzle→boss (on remaining four divisions) | **127** | 20 / 16 | Still over budget and loses an entire division | Arithmetic only |
| **Five divisions, single authored progression lane + five reset nodes and a native 50%-after-loss reset mechanism** | **93** | **25 / 20** | Removes redundant second lane (17 nodes/division) while maintaining 50% reset, Medical100, all bosses and choices | **Requires separate game-code capability, NOT available today** |
| Above, also drop one-option clean/alert boss approach dialogs | **83** | 25 / 20 | Additional 2 dialogs/division removed; puzzle itself directly gates boss | Requires same engine capability; not tested |
| Four divisions, single lane, keep boss approaches, native reset capability | **75** | 20 / 16 | Cut Gatewarden; no longer 5-division arc | Requires engine capability |
| **Native-only drastic condensation:** cut Gatewarden; reduce each remaining division to 2 regular encounters (first mandatory, second optional), puzzle at earlier terminal; direct puzzle→boss | **95** | **12 / 8** | Preserves 4 commanders, all 4 puzzles and protocols, 50% retry topology; loses 13 of 25 normal-route fights and the introductory boss | **Design candidate only; native retest mandatory** |

**Native-only 95 budget detail:** each surviving division is `35 – 8` (drop two regular fight/dialog pairs from both lanes) `– 4` (delete separate clean/alert approach dialogs on both lanes) `= 23` nodes. Four divisions `4×23 + 3 = 95`. The terminal now appears after the **first regular**, and the **second regular** is optional via Maintenance; that is a substantial pacing/rule rewrite, not a cosmetic deletion.

**Proposed 93 budget detail:** each division retains the **original 9 dialogs + 8 battle nodes** in one lane, plus **one reset node**: `9+8+1=18`. Five divisions `5×18=90`; global aftermath/win/fail `+3` → **93 nodes** (46 dialogs, 40 battle nodes, 5 resets, win and fail). Preserves all 25 enemy slots, all five puzzle themes, both Protocol choices and all boss variants. The first-battle Beacon rule and pool carry must also survive implementation.

## 3. Technical obstacle: cannot just merge the two lanes

**The current game schema does not give `reset_quest` an HP/CP/SP set-percent field.** In current `app/src/validators/objectives.ts`, `ResetQuestObjective` has `resetObjectiveId` and rewards, while `givePools` is a **battle-start** field. `applyQuestResets` in `app/src/libs/quest.ts` removes the target and its selected tracker path but does **not** restore pools. Ordinary defeat leaves the user at minimum 1 HP.

**Further, naïvely merging the initial and retry branches after their different first-fight nodes is not a proven native workaround.** A shared later `start_battle` has **one static `failObjectiveId`**. The r2 initial lane redirects its first loss to a distinct retry entry, whereas the retry lane's repeated losses require `reset_quest` to clear that already visited path. If an initial-lane loss reaches a reset pointed at an **as-yet-unvisited** retry entry, the current `applyQuestResets` logic cannot simply infer and create the missing route. Blind lane merging risks stalled trackers, infinite progress loops, or 50% recovery never firing. No claim of source-native 93/83 is made.

## 4. Recommended path: preserve the five-division Pyramid via a scoped reset enhancement

**Recommendation to director:** Do **not** remove The Gatewarden solely to hit the node cap. The first division may separately merit pacing/combat improvements, but eliminating it only saves 35 nodes (still 143); the majority of the bloat is **duplicate authoring for retry**.

Have the game implementation owner examine an **isolated, narrowly scoped** capability to set the three player pools to **50% only when `reset_quest` is entered from a non-final battle loss** in an isolated `battlepyramid`. Possible contracts include an optional `resetPoolsPercent` property on `reset_quest`, or a quest-level `battlepyramid` checkpoint-pool setting, with exactly scoped runtime application and generated contract updates. These are **engineering alternatives, not invented existing fields**.

**One-lane intended semantics:** any loss on fights 1–24 → that division's `reset_quest` → clear its selected path → restore HP/CP/SP to 50% → re-open that division's first regular dialog; normal wins/division transitions leave pools unchanged; Medical Protocol still fully restores pools on the boss **only** when chosen; Arakane loss still hard-fails. This should make a five-division, 25-encounter **93-node** Pyramid possible without deleting the core gameplay. **Not guaranteed until separately reviewed, implemented and native-tested.**

Prove source/contract and 93-node fixture against the *actual* engine build SHA; require correct loss and reset across all four boss variants and both normal/repeat attempts, no accidental restoration after an ordinary win or before first fight, Beacon charged once, no rewards for reset, no duplicate commander battle, and hard-fail Arakane. Rerun Phase 1 F1/F2 missing-Beacon and F3 retry farming checks alongside the correction the director already expects. Preserve F4/F5 disclosure: hidden game quest data and final text are currently retrievable via public API, so "story spoiler impossible" is not an enforceable game guarantee.

**Fallback without a game-code change:** the 95-node option is mathematically possible as a proposal, but it cuts the gameplay to 12 full-route fights and 4 commanders, sharply reducing the resource-attrition identity. The director must explicitly authorize that scale reduction before a graph revision.

## Decision requested

Is a small **game-source reset-pool enhancement** acceptable to preserve the **93-node / five-division / 25-encounter** experience? If not, the director may choose a shorter four-division Pyramid, understanding that simply removing floor one alone is insufficient.

**Live game requests/writes:** 0. **No code, manifests, or live data changed.** This analysis has no authority to alter director-approved lore, combat balance, protocols, rewards, or the branch assigned to Fable.
