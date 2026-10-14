# Silent Bastion Phase 1 — native progression results (offline)

**Status:** NATIVE OFFLINE VERIFICATION RUN. The graph's ordinary progression passes every required case on the pinned runtime. **Two engine-level findings (F1, F2) break the "dialog-gated / no premature battle" guarantee in one reachable edge path**, and one economy observation (F3) needs a director decision. Phase 1 is **not** marked verified here: that waits on ChatGPT's independent review of the frozen SHA and the director's call on F1–F3.
**Harness:** `harness/silent_bastion_phase1/` (README there). **Evidence:** `harness/silent_bastion_phase1/results/`.
**Design under test:** `state/silent_bastion_phase1_graph.json` (sha256 in `results/provenance.json`) from `chatgpt/silent-bastion-design-20261013@450c47bf88b38758477b5783569ea6ab7a0c146a`.
**Engine:** `studie-tech/TheNinjaRPG@c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd`. **Live requests/writes:** 0. **Credentials:** none.

## 1. Method

The symbolic graph was compiled 1:1 into the engine's own objective schemas (`engine/lib/graph.ts`): dialogs → `DialogObjective`, battles → `InstantStartBattleObjective` (`nextObjectiveId` = win, `failObjectiveId` = loss, `givePools`, `applyBuffs`/`applyDebuffs`), resets → `ResetQuestObjective`, terminals → `win_quest`/`fail_quest`. The quest is `battlepyramid`, `isolated:true`, `consecutiveObjectives:true`, with one entry item (fixture Beacon). Then:

- **S** — the engine's validators and graph helpers on the compiled record (pure).
- **R** — 16 complete attempts through the real routers against a throwaway local MySQL: `startQuest` → `checkRewards(choice)` (quest consequences → `initiateBattle`) → settlement via `calcBattleResult` + `combat/database.updateUser` (the upstream `quests.persistentBattle` pattern) → `fetchUpdatedUser` (reset/fail consequences). Every battle start is checked for the exact objective, opponent, start pools and quest starting effects.
- **E** — abandonment, premature input, missing Beacon, recovery freeze, pause/version change, the real `quests.update` save, performance, and the retry-loop economy.

Isolation: MySQL is `--network none` and reachable only by unix socket; all tests run in `unshare -rn` (no network interfaces). Upstream preflight (8 engine suites on Pyramid runs, entry items, isolation, retry) passed in the same environment: 73/73.

## 2. Results against the requested checks

| Requirement | Result | Evidence |
| --- | --- | --- |
| Single-root, acyclic objective progression | **PASS.** `verifyQuestObjectiveFlow` and `verifyQuestContentForSave(consecutive)` accept all 208 objectives; the runtime's own `findPredecessor` finds exactly one root, `d1.n.f1`. Negative controls: an extra root and a retry loss edge without `reset_quest` are rejected (cycle). | S |
| All battles dialog-gated | **PASS on every normal path; FAIL in the missing-Beacon path (F1).** Statically 90/90 battles have exactly one predecessor, a single-option dialog, and no battle routes into a battle. At runtime, 600 battle starts each followed an explicit dialog choice, and no battle started on page refresh after a win or loss. See F1 for the exception. | S, R, E3, E4 |
| Three terminal routes per division | **PASS.** Each of the 10 terminals (5 divisions × 2 lanes) offers Maintenance, Medical and Combat; each puzzle has 1 correct + 2 wrong options; terminals follow only regular fight 3. 3,125 successful selection paths, each 20–25 battles with exactly five commanders, all ending at `w.complete` via `d.aftermath`. Every battle kind (f1–f3, f4×2, boss×4) was fought on both lanes. | S, R |
| Medical and Combat Protocol application | **PASS (mechanics; values are placeholders).** Medical commanders start at exactly 75% HP/CP/SP of max, observed both lowering a higher carried pool and raising a lower one. Alert/Combat commanders carry exactly one player-side quest effect (Security Alert debuff / Combat buff), no other battle carries any, and the AI never receives them. | S, R |
| 50% checkpoint recovery after defeat | **PASS.** All 45 initial-lane battles were lost at least once: each routed to its own division's `d{i}.r.f1`, and the next battle started at exactly 50% of max on all three pools (77 retry entries observed). | R (L1–L9) |
| Repeated retries without broken progression | **PASS.** 83 losses in total. Two consecutive retry-entry losses in every division (L1), retry losses at f3/f4/commander, and five consecutive Division I retry losses (X1). Each `reset_quest` cleared the selected retry chain and returned to `d{i}.r.f1`; no stranded `recentlyDied`, no leftover route (e.g. a lost Medical commander followed by a Combat route started with the Combat buff and carried pools, not 75%), and the engine reported exactly one open objective after every loss. | R |
| No automatic resource recovery | **PASS.** Ordinary wins and commander transitions carry pools unchanged into the next battle. Six hours between floors restored nothing (isolated freeze). Defeat leaves 1 HP. Completion, failure and abandonment restore nothing; a new attempt starts with the depleted pools. | R, E5, E1 |
| Beacon consumed only once per attempt | **PASS.** Starting the run does not consume it; the first battle consumes exactly one (`entryPaid`); no later battle, retry or reset charges again. A new attempt after completion, failure or abandonment charges a new one. Not refunded on failure or abandonment. See F2 for starting without one. | R, E1, E4 |
| Arakane defeat ends the entire attempt | **PASS.** Lost on the initial lane under all four routes (L6–L9) and on the retry lane (A×2): `f.arakane` → `fail_quest` closes the history row uncompleted, releases isolation (AWAKE), pays nothing, refunds nothing. The closed run accepts no further progress. | R |
| Abandonment and successful completion | **PASS.** Abandon between floors closes the attempt, releases isolation, no refund/reward/recovery. Abandon during a live battle is refused by the engine ("Finish or flee"). Completion after Arakane + aftermath pays the quest reward exactly once; replaying the final claim pays nothing. | R, E1, E2 |
| No premature battles or rewards | **PASS on normal paths; FAIL in the missing-Beacon path (F1).** Out-of-order choices at the root (later dialogs, other lanes, `w.complete`) move nothing. A continuation during a live battle is rejected. After an initial loss the abandoned initial lane cannot be resumed. The quest reward appears only at completion. | E3, R |
| Performance with 208 objectives | **PASS for engine paths measured.** `QuestValidator` ≈49 ms, flow check ≈1.5 ms. `getNewTrackers` at the deepest state ≈14 ms per call. `fetchUpdatedUser` ≈54 ms. Content save ≈111 ms. Saved content 237,078 bytes; tracker 208 goals / ≈19.7 KB. A full 25-battle attempt takes ≈8 s locally. Logbook/mobile rendering was **not** tested. | S, E7, E8 timings |

Hidden pause and version change (E6): hiding the quest pauses continuation without losing the checkpoint; unhiding resumes at the same objective. An edited quest blocks the old run, which can still be abandoned.

## 3. Findings for director / engineering decision

**F1 — Missing-Beacon window bypasses dialog gates and fight order (engine; blocks the guarantee as stated).**
If the first battle fails to start, the following dialogs remain completable. In the engine-native probe (E4b), with no Beacon held, eight dialog steps were accepted without any fight, including the Division I terminal choice and the first two Division II dialogs. Once a Beacon was added, page refreshes alone started seven battles in a row with no dialog step, in this order: `b1.n.f1, b1.n.f2, b1.n.f3, b1.n.boss.combat, b1.n.f4.combat, b2.n.f1, b2.n.f2`. The **commander was fought before regular fight 4**. No battle was skipped (completion still requires every battle on the path), and no reward was gained.
Cause at the pin:
1. `app/src/libs/quest.ts:1349–1356`: for `task:"any"`, a pending `start_battle` gets `selectedNextObjectiveId = nextObjectiveId` before it is won.
2. `app/src/libs/objectives.ts:148` (`isQuestObjectiveAvailable`) follows `selectedNextObjectiveId` without requiring `done`, so the next dialog becomes available.
3. `quest.ts:1240` queues a combat for every available pending battle, and `app/src/server/api/routers/quests.ts:4058` starts the first one in array order. That is why the boss precedes f4: the graph lists boss nodes before f4 nodes.

In normal play, the guard at `quests.ts:1268` ("Must be awake…") rejects continuation while a battle is live. That guard is why the gap only opens when a battle fails to start. The Beacon is the reachable trigger (F2). Other `initiateBattle` failures (races) could open the same window; those were not exercised.
Options, all needing a decision: (a) an upstream engine change, e.g. do not preset `selectedNextObjectiveId` on an unfinished `start_battle`, or require the predecessor to be done; (b) an engine-side Beacon check at `startQuest` for entry-item Pyramids, which closes the reachable trigger only; (c) a content-only mitigation: reorder objectives so each `f4` precedes its commander. That fixes the order symptom but **not** the dialog bypass. Not applied: the graph is ChatGPT's design artifact.

**F2 — `startQuest` admits the run without the entry item (engine behaviour).** Isolation begins, and the first battle is refused with the notification "You do not have the required entry items in your inventory". `checkRewards` still returns `success:true`. This is the reachable trigger for F1 and a UX gap.

**F3 — Retry loops repeat ordinary battle income (economy; user-owned).** Deliberately losing a Division I–IV commander resets the division. The already-won regular fights are then re-won, and each win pays normal battle settlement ryo/XP. In E9 every loop (3 regular wins + 1 commander loss) paid ryo and 96 XP, all on one Beacon. The quest reward is unaffected. Whether this is acceptable, capped, or offset (e.g. `scaleGains` on retry-lane battles) is a balance decision.

**Confirmed source facts (no new decision; already open in the design):**
- `clearprevent` is not in `questBuffTypes`. The advertised Arakane Combat Protocol is rejected by `InstantStartBattleObjective` and by `QuestValidator` (S). The D5 combat route here uses a labelled stand-in.
- A **visible** save needs `sceneCharacters` (quest-level or on every objective); a hidden save of the same record succeeds (E7).
- Abandonment is refused mid-battle by design of the engine.
- The editor save calls the Discord content hook. In the test it refused the placeholder webhook URL; no network exists in the namespace.

## 4. Not tested / limits

- No combat was simulated: outcomes and end pools are imposed on the snapshot (upstream test pattern). Encounter difficulty, AI rules, starting-effect magnitudes and Security Alert strength are out of scope.
- Placeholder effects (`PLACEHOLDER_EFFECTS`) are not proposals.
- Logbook/mobile UI navigability with 208 objectives, browser/client behaviour, hidden-content publication, and real Pusher delivery were not exercised.
- Concurrency/race windows beyond the upstream preflight suites were not added.
- Only one entry-item path was tested (single stack).
