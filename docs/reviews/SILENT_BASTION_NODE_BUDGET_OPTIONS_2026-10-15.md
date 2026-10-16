# Silent Bastion — objective budget options (design review)

> **DIRECTOR DECISION — 2026-10-15 (RUL-2026-10-15-001): OPTION A SELECTED.** The four full **interior** divisions / **99-node source-native candidate** is the chosen design direction. The original Outer Garrison / The Gatewarden and its puzzle are removed from this Pyramid because its **exterior must appear deserted and undefended**. Retain the other four complete divisions with 16 regular encounter slots, 4 commanders, 4 puzzles, 16–20 actual battles per winning run. **Selection is not proof:** the 99-node recovery-fight + reset bridge remains to be tested in the engine-native Phase 1 harness; no game code modifications are authorized. Earlier comparative options and the initially proposed engine enhancement are historical/rejected paths, not current recommendations.
>

**UPDATE — native reset-bridge candidates identified and stored (director follow-up):** The categorical conclusion in §4 that a game-source enhancement is the only way to preserve full division encounters below 100 is **SUPERSEDED**. A **four-division, 99-node** graph and a **five-division, 98-node** shorter graph have passed a source-mirrored **static DAG/reachability** check using existing `reset_quest` and `givePools:50` semantics. They still require **native tracker/runtime proof** before acceptance. See the new addendum at the end. No game-source changes are proposed.

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

---

## 5. Director follow-up — recovery fight + reset bridge (supersedes §4 recommendation)

**Director's insight:** Direct every division loss to a short defeat dialog and a copy of the first regular fight that sets all three pools to 50%. The recovery win should then feed the ordinary division instead of maintaining two complete lanes. The core observation is valuable: **only the first recovery battle needs `givePools:50`, not every subsequent node**.

### Why the direct 98-node proposal fails as literally drawn

The direct sketch of one normal lane (17 nodes) + defeat dialog (1) + recovery first battle (1) per division mathematically gives **`5 × 19 + 3 = 98`** and preserves all 25 unique encounter slots. However, wiring `later_battle.failObjectiveId → defeat_dialog → recovery_first_battle.nextObjectiveId → regular2` creates a **forward directed cycle** (`regular2 → fail → defeat → recovery_first → regular2`). The actual engine's `verifyQuestObjectiveFlow` in `app/src/libs/quest.ts` **includes failObjectiveId as an adjacency edge and rejects cycles** with `Cycle detected in objective chain`. An equivalent static graph check against the r2 nodes found this cycle. Plain reconnection is not a valid released quest graph.

**Crucial workaround within existing game mechanics:** Let `recovery_first_battle.nextObjectiveId` point at a **terminal `reset_quest`** that internally resets the already-visited normal path to its regular-2 dialog. The validator does **not** treat `resetObjectiveId` as a forward adjacency edge, so this is a legal graph shape *in principle*. `applyQuestResets` in `app/src/libs/quest.ts` clears the target objective and the selected forward tracker path. The normal first-fight success pointer into regular2 is preserved, so regular2 should reopen with the pools resulting from the just-won 50%-starting recovery fight.

**Two cases must not be conflated:** If the **first normal regular** loses, regular2 has never been visited; resetting to regular2 would not work. The candidate therefore creates **separate first-loss and later-loss recovery transitions**:

```text
FIRST REGULAR LOSS:
  initial REG1 loss → first-loss dialog
                    → REG1 recovery battle [givePools:50]
       recovery WIN → normal REG2 dialog directly
       recovery LOSS → reset_quest(target: first-loss dialog)
                     → recovery fight again at 50%

ANY LATER REGULAR / NONFINAL COMMANDER LOSS:
  normal REG2/3/4/boss loss → later-loss dialog
                            → REG1 recovery battle [givePools:50]
       recovery WIN → reset_quest(target: normal REG2 dialog)
                    → replay normal REG2/3/4, terminal, commander
       recovery LOSS → reset_quest(target: later-loss dialog)
                     → recovery fight again at 50%

ARAKANE LOSS: fail_quest; no checkpoint.
```

**Source-compatible graph trick:** There is no forward `nextObjectiveId` back edge at all. The only logical rewind uses `reset_quest.resetObjectiveId`, an existing native operation. No new field, game-engine patch, or impossible dynamic per-battle setting is assumed. All `start_battle` nodes have a preceding dialog, and the pre-existing Medical/Combat post-fourth-fight choice and four commander route variants remain intact.

### Two complete static candidates committed

| Candidate | Objectives | Unique fights | Actual successful fights | Preserves |
| --- | ---: | ---: | ---: | --- |
| **Four full divisions** | **99** | **20** (16 regular + 4 commanders) | 16–20 | All four remaining full division sequences, four puzzles, three terminal routes, all Medical100/Combat/Alert choices, original retry-50 intent, Arakane end-fail |
| **Five shorter divisions** | **98** | **15** (10 regular + 5 commanders) | 10–15 | All five commander identities/puzzles/protocols, but only **REG1 mandatory + REG4 optional** per division, terminal after REG1 |

- `state/silent_bastion_condensed99_candidate.json`: Four divisions **Experimental Armory through Command Sanctum**, with the user-suggested optional cut of The Gatewarden / Outer Garrison; per division **17 original single-lane + 7 additional recovery/reset nodes = 24**; four divisions `4×24+3=99`. **Breakdown:** 45 dialogs, 40 battles, 12 resets, 1 win, 1 fail. Full four-regular fight pacing preserved in every remaining division.
- `state/silent_bastion_condensed98_fivediv_candidate.json`: Five divisions each shortened from four regulars to **two** (REG1 mandatory, REG4 optional), one clean boss-approach dialog removed per division (puzzle directly gates the clean boss), with the same **7 recovery/reset nodes** per division: `5×(17−4−1+7)+3=98`. **Breakdown:** 41 dialogs, 40 battles, 15 resets, 1 win, 1 fail. Five commanders retained.

**Checked now (not native-tested):** Both structural files have exactly one root, all references resolve, every node is reachable, no direct forward cycles including fail edges, correct intended per-division and overall counts. A source-equivalent local tracker reset walk also reached the expected active dialog after (a) first recovery loss, (b) later recovery win, (c) later recovery loss, and (d) first recovery win followed by later recovery win. This proves the *design is not disqualified* by the old cycle objection, not that game UI/router traversal is safe. These symbols are **not executable game records**.

### Native proof gate before deciding

Ask Fable to **compile these exact symbolic candidates** using `harness/silent_bastion_phase1/engine/lib/graph.ts` (adjust the compiler only as needed to support `resetTarget` and `startPoolsPercent`, not production game source) and run `QuestValidator`, `verifyQuestObjectiveFlow`, real `startQuest/checkRewards`, battle settlement, `applyQuestResets` and tracker recomputation. Required cases:

1. Initial REG1 loss → recovery at 50%; recovery loss repeated twice → recovery again at50%; recovery win → REG2 (or terminal in five-division variant), without wrong previous quest completion.
2. Loss at every later regular and each clean/alert/Medical/Combat boss route → re-fight REG1 at50 → **win→reset** clears only current division's selected REG2+ chain → valid re-entry; repeated losses do not strand tracker.
3. Medical boss restores full pools (RUL-2026-10-14-001), Combat effects are **player-side**, wrong Maintenance debuff is player-side, and no extra buff on fourth regular.
4. Ordinary division transitions **carry pools**, 50% pool set only on recovery battle after defeat, and no auto-refill on a normal win.
5. Beacon consumed once on first initiated battle, never on checkpoint recovery. Arakane loss ends whole run. No duplicated final reward, no skipped normal battles through browser/UI, no reward from reset transitions. Assess retry XP/ryo farming (F3).
6. Refresh/reconnect, missing Beacon F1/F2, old saved tracker/edited quest behavior, duplicate incoming predecessor, objective ordering, and visible Logbook/mobile navigation under the current pinned engine.
7. Rerun reproducible tests on **current source** and independent second run, record exact SHA and source drift.

**Decision is not made:** Whether to cut Gatewarden, shorten regular waves, or preserve all five bosses via some other authored compromise remains entirely the director's choice. **Recommendation updated:** Prototype the **99-node / four-full-division** candidate first because it preserves the four remaining divisions' combat depth and uses no game-code change, then separately compare it with the **98-node / five-shorter-division** choice. Both are **CANDIDATE, NOT APPROVED, NOT ENGINE-NATIVE-VERIFIED.**

**Live requests/writes:** 0; no credentials or game source modification. All changes are to this ChatGPT-owned review branch.
