# Silent Bastion condensed 99-node candidate — native offline results

**Verdict: FAIL as specified.** One recovery transition in the director-selected 99-objective graph does not behave as the brief requires on the pinned engine. The defect is the same in all four divisions. Everything else in the brief passes. Three **content-only** remediation graphs (no engine change, within budget) were derived and pass every gate, including the defect probe. They are **options for director acceptance**. None is selected, and four-division content authoring has **not** continued.

- **Brief:** `docs/handoffs/SILENT_BASTION_CONDENSED99_NATIVE_PROOF_BRIEF.md` at `chatgpt/silent-bastion-node-budget-20261015@2af1ffd808f692d241b80c1d2c87e6e6d967016b`.
- **Design under test:** `state/silent_bastion_condensed99_candidate.json` (99 objectives).
- **Harness:** `harness/silent_bastion_condensed99/` (README there). **Evidence:** `harness/silent_bastion_condensed99/results/<variant>/`, provenance in `results/provenance.json`.
- **Engine:** `studie-tech/TheNinjaRPG@13d40c4c1509ecf44262aba1b5120266011ea786`. That was upstream `main` when the run started, the same as "last inspection" in the brief. It is 139 commits after the Phase 1 pin `c82dc7f8`.
- **Isolation:** live-game requests **0**, writes **0**, credentials **none**, engine modifications **0**.

## 1. Method

The method is the same as Phase 1 (`docs/reviews/SILENT_BASTION_PHASE1_NATIVE_RESULTS.md` §1):

- **Compile.** The symbolic graph is compiled 1:1 into the engine's own objective schemas (battlepyramid, `isolated`, `consecutiveObjectives`, one entry item). The Phase 1 compiler `harness/silent_bastion_phase1/engine/lib/graph.ts` received only the mapping changes the brief allows: a `TNR_GRAPH` selector and `resetTarget` → `resetObjectiveId`. `startPoolsPercent` was already mapped to `givePools`. The Phase 1 static gate still passes at its own pin (33/33).
- **Drive.** Every step goes through the real routers against a throwaway socket-only MySQL: `startQuest` → `checkRewards` (quest consequences → `initiateBattle`) → upstream settlement pattern (`calcBattleResult` + `combat/database.updateUser`) → `fetchUpdatedUser` (reset and fail consequences).
- **Read the path from the graph.** `engine/lib/run99.ts` reads the path from the graph and checks every battle start, win, loss and reset. It also checks that the completed objectives of earlier divisions survive every later reset.

Gates:

- **S** — engine validators and graph helpers, pure.
- **D** — the recovery_later loss transition, isolated per division.
- **R** — 18 complete attempts.
- **E** — edge cases.

Upstream preflight: 10 engine suites (Pyramid runs, entry items and the new entry charge, isolation, retry, `questReset`) passed **79/79** in the same environment.

## 2. The defect (C1)

**Minimal reproduction** (gate D, every division; `results/candidate/d_defect.json`):

1. Win `b2.n.f1`, then lose `b2.n.f2`. The run lands on `d2.lost_later` at 1 HP. Correct.
2. Choose `b2.recovery_later`. The fight starts at 50%. Correct. But in the same request the tracker already loses `d2.lost_later`, `b2.recovery_later` and `r2.reset_later_win`: the reset to `d2.n.f2` has **already fired**. While the fight runs, the engine's active objective is `d2.n.f2`.
3. Lose the recovery fight. The active objective stays `d2.n.f2`, and the player has 1 HP. `retryBattle` is refused.
4. Choose `b2.n.f2`. It is accepted, and REG2 starts at **1 HP (0.1%)**.

The same result occurs in D3 (REG4 loss, Combat route), D4 (Security Alert commander loss) and D5 (REG3 loss).

**Consequences:**

- A lost recovery fight after a later defeat does not replay at 50%. The run continues to REG2 with the player's 1 HP.
- `rN.reset_later_loss` (4 objectives) is unreachable.
- A **won** recovery fight produces the intended state (REG2 with the fight's end pools), but only by coincidence: the outcome is ignored.

**Native contract that causes it (pinned source):**

1. `app/src/libs/quest.ts:1519–1527` — on a task `any` pass, an available, unfinished objective with a string `nextObjectiveId` gets `selectedNextObjectiveId = nextObjectiveId`. A pending `start_battle` therefore points at its WIN target while the fight is live.
2. `app/src/libs/objectives.ts` `isQuestObjectiveAvailable` follows `selectedNextObjectiveId` from the root without requiring `done`, so the WIN target becomes available.
3. `quest.ts:1379–1386` — an available `reset_quest` emits its reset consequence immediately. `applyQuestResets` (`quest.ts:799–827`) then removes `dN.n.f2` and its selected chain, which includes the live recovery battle.

A battle's **loss** edge is set only when the battle is lost (`quest.ts:1704–1710`). That is why `recovery_first` (WIN → dialog, LOSS → reset) and Phase 1's loss-edge resets behave correctly, and why only the four `recovery_later` WIN edges are affected.

**Static lint** (gate S, `battleWinEdgesIntoReset`): `b2..b5.recovery_later → rN.reset_later_win` are the only battle WIN edges that target a `reset_quest`.

**Logbook:** the client's active objective is `getActiveObjective`. During any fight `canProgress` is false (`app/src/layout/Logbook.tsx:467–471`, `:787–788`), so no dialog buttons render while the recovery fight runs. After it, the candidate shows `d2.n.f2` even when the recovery was lost.

## 3. Results against the brief (candidate)

| Requirement | Candidate | Evidence |
| --- | --- | --- |
| Validators: `QuestValidator`, `verifyQuestObjectiveFlow`, `verifyQuestContentForSave`, single root, reachability, no cycles, real save | **PASS.** 99 objectives (45 dialogs, 40 battles, 12 resets, win, fail). `findPredecessor` finds one root, `d2.n.f1`. Back edges exist only as `resetObjectiveId`; a direct recovery→`d2.n.f2` edge is rejected as a cycle (negative control). The real `quests.update` saves the hidden record (110,450 bytes). | S, E6 |
| Every battle has a dialog predecessor | **PASS.** 40/40, including the post-fourth-fight protocol choice. No battle routes into a battle. | S |
| Structure | **PASS.** 4 terminals after REG3; puzzle with 1 correct and 2 wrong answers; protocol only after the fourth fight; 20 encounter slots, no Gatewarden. 625 successful selection paths of 16–20 battles, each with four commanders and one ending. | S |
| Initial REG1 loss; two consecutive recovery_first losses; recovery win → REG2 | **PASS** in every division (L1, M1, M2). | R |
| Defeat at REG2/3/4 and on each clean/alert/Medical/Combat commander; recovery win → REG2 via `reset_quest` | **PASS for the win path** (L2–L4, B×4, M1, M2): the run lands on `dN.n.f2` with the recovery fight's end pools. As §2 shows, this happens because the reset fired at the fight's start. | R |
| Recovery_later **loss** → replay at 50% (`reset_later_loss`) | **FAIL (C1)** in all four divisions. | D |
| Repeated failures without stale progress or a wrong division reset; earlier divisions never reset | **PASS** for every exercised transition. Earlier divisions' completed objectives were checked after every segment of every division. | R (M1: 6 segments in D2, 4 in D4) |
| Effective pools | **PASS** except C1. 56/56 recovery fights started at exactly 50%. Recovery win → REG2 starts with the actual end-of-fight pools, not another 50% set. Wins and division transitions carry pools. Medical sets 100% only when selected (healing a depleted carry was observed). A lost Medical commander followed by a Combat route carries the depleted pools with the buff. Quest effects land on the player only. | R |
| 16–20 battles; one commander victory per division; no duplicate boss start; correct opponents; no premature terminal or reward | **PASS.** 625 static paths of 16–20 battles; each runtime clean run played 18 (mixed routes), the all-Medical run 20. One commander win per division; opponent slot checked at all 483 battle starts; reward only at completion. | S, R, E7 |
| Beacon once; Arakane defeat closes the attempt; replay pays once | **PASS** with a contract change (**B1**, §5). Arakane defeat on all four routes (and after a D5 recovery) closes the attempt uncompleted, releases isolation, pays and refunds nothing. Completion pays exactly once; a replayed claim pays nothing. A new attempt restarts at the root and charges a new Beacon. | R, E2 |
| Pause, version edit and resume at recovery checkpoints | **PASS.** Hiding the quest at `d2.lost_later` refuses the recovery; unhiding resumes it at 50%. No regeneration over six idle hours. An edit after a reset blocks the old run, which can still be abandoned. Abandonment is refused mid-recovery-fight and accepted at the post-recovery checkpoint without refund. | E3, E5 |
| Out-of-order input | **PASS.** Probes at the root, after a REG1 loss, and during live recovery fights move nothing. Taking REG2 during a live recovery fight is rejected. | E4 |
| Performance | `getNewTrackers` ≈6 ms per call at the deepest state (99 goals, ≈10 KB tracker); full 20-battle run ≈5 s locally. | E7 timings |

**Totals:** R = 18 attempts, 483 battle starts, 60 losses. Assertion counts (candidate): S 30, D 538, R 6,817, E 592, all passing. Gate D's candidate checks assert that C1 **reproduces**.

## 4. Content-only remediation options (for director acceptance)

C1 is avoided without engine change when the recovery_later WIN edge leads to a **dialog**, and that dialog's only option is the reset. While the fight is live, the engine may pre-select the dialog, but a dialog needs an explicit choice. The choice is refused during the fight, and only the WIN path offers it. Each option adds `dN.recovered` (+4 objectives) and folds one existing single-option dialog gate per division into the dialog before it, so the battle is still dialog-gated. The protocol dialog already gates the Medical and Combat commanders this way. All other content, encounters, puzzles, commanders, protocols and values are unchanged. The graphs are generated by `harness/silent_bastion_condensed99/tools/derive_alternatives.py`, which `run.sh` runs with `--check`.

| Option | Objectives | Folded gate (per division) | Player-facing cost |
| --- | --- | --- | --- |
| **`alt99_f4gate`** (recommended) | 99 | `dN.n.f4` — the terminal's "Protocol access" choice starts the fourth fight directly | The fourth enemy's intro text must live in the terminal dialog. No outcome feedback is lost. |
| `alt99_alertgate` | 99 | `dN.n.boss.alert` — wrong puzzle answers start the Security Alert commander fight directly | No separate "alarm raised" beat after a wrong answer. The penalty must be signalled by the puzzle text or option labels. |
| `alt95_bossgates` | 95 | `dN.n.boss.clean` and `dN.n.boss.alert` | No commander intro beat on the Maintenance route; 5 objectives of headroom. |

Each option passes S, D, R and E (§6). Gate D shows, in all four divisions:

- the recovery fight stays the active objective while it runs;
- a recovery loss rewinds to `dN.lost_later`;
- the next fight is the recovery fight again at 50%.

Gate R adds consecutive recovery_later losses (two in L3; up to two per segment in M1). All recovery fights were both won and lost in every division.

**Rejected as alternatives:**

- Adding `dN.recovered` without a fold costs 103 objectives, which is over budget.
- Merging the two recovery templates fails: after a REG1 loss, `dN.n.f2` is not on the selected chain, so a reset to it removes nothing and the run stalls.
- Pointing the recovery WIN edge straight at `dN.n.f2` is rejected as a cycle.
- Resetting to `bN.n.f1` or `dN.n.f1` restarts REG1 with the carried 1 HP, not 50%, and a `bN.n.f1` target also auto-starts the fight without a dialog.

**Option 0, accept C1 unchanged**, is possible, but it breaks the brief's "loss … must return to … 50%" for recovery fights after a later defeat. It is listed for completeness, not recommended.

## 5. Other findings

- **B1 — entry is charged at the start at this pin (engine change since Phase 1).** Upstream `dc07be41` ("Check and consume Battle Pyramid entry items when a run starts") debits the Beacon inside `startQuest`; the first battle sees the `entryPaid` receipt. The brief and RUL-2026-10-15-001 say "charged at the first initiated fight". The observed behaviour is still exactly once per attempt, never refunded, including when the run is abandoned before any fight. The **director must re-confirm** whether this wording is acceptable or how the player-facing text should describe it.
- **F1 / F2 — closed at this pin.** `startQuest` without a Beacon is refused ("You need 1× … to enter"): no isolation, no attempt row, and crafted dialog choices change nothing. The reachable trigger of F1 no longer exists. The underlying pre-selection that F1 relied on is the same mechanism as C1 and is still present.
- **F3 — retry-loop income (economy, user-owned).** Each loop of "REG2 win + REG3 loss + recovery win" paid ordinary battle ryo and 64 XP on one Beacon (E8). This is unchanged in kind from Phase 1.
- **F4 / F5 — dialog text exposure, unchanged.** The aftermath text is returned by `quests.get` to a logged-out caller and by `profile.getUser` at run start. `hidden: true` does not hide it from `quests.get` or `quests.getAll({hidden:true})`.
- **Arakane Combat Protocol:** `clearprevent` is still not in `questBuffTypes`, so the D5 stand-in remains (the director's decision is still open).
- **Integration: ruling ID collision.** This branch's `docs/RULINGS.md:1098` has `RUL-2026-10-14-001` (Medical full heal / protocol after the fourth fight). `main@43ce6b2`'s `docs/RULINGS.md:1098` has the same ID for an unrelated art ruling. Flagged for explicit reconciliation at integration; not changed here.

## 6. Runs, provenance, reproducibility

```bash
harness/silent_bastion_condensed99/run.sh            # preflight + S, D, R, E on all four variants
```

Run 1 (committed evidence): `run.sh: preflight=0 derive=0 bun=0 evidence=0 -> exit 0`. Upstream preflight 79/79; `derive_alternatives.py --check` current.

| Variant | Objectives | Graph sha256 | S | D | R | E | Saved bytes (E6) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate` | 99 | `52dac9af…b2a6` | 30/0 | 538/0 (C1 reproduced 4/4) | 6,817/0 | 592/0 | 110,450 |
| `alt99_f4gate` | 99 | `c70fad7a…ee20` | 30/0 | 543/0 (C1 absent 4/4) | 7,033/0 | 592/0 | 110,510 |
| `alt99_alertgate` | 99 | `81216f93…acea` | 30/0 | 543/0 (C1 absent 4/4) | 7,144/0 | 604/0 | 110,414 |
| `alt95_bossgates` | 95 | `8204cddb…57fd` | 30/0 | 525/0 (C1 absent 4/4) | 7,087/0 | 601/0 | 106,398 |

(checks / failed). R on each option: 18 attempts, 504 battle starts, 81 losses, 77 recovery starts at exactly 50%, both recovery fights won **and** lost in every division.

DETERMINISM_PLACEHOLDER

Input SHA-256 values (graphs, brief, harness files, engine sources `quest.ts`, `objectives.ts`, `validators/objectives.ts`, `routers/quests.ts`, `utils/questEntry.ts`, `bun.lock`) are in `results/provenance.json`. Evidence JSON is deterministic: sorted keys, and passing checks keep names only. Timings and raw ryo are only in `*.timings.json`.

## 7. Not tested / limits

- No combat was simulated. Outcomes and end pools are imposed with the upstream settlement pattern. Encounter balance, AI rules, starting-effect magnitudes and Security Alert strength are out of scope; placeholder effects are not proposals.
- The Logbook was assessed from source only. Browser, mobile and Pusher delivery were not exercised.
- No concurrency or race windows were added beyond the upstream preflight suites.
- **Not begun:** authoring plan update, objective texts, deserted-exterior staging drafts, manifests under `push/`, publication. These wait on the director's choice in §4 (and B1/F3/F5 as applicable).
