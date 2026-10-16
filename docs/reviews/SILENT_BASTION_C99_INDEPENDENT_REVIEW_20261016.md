# Silent Bastion 99-node offline-probe independent review

**Status:** REVIEW COMPLETE; **original 99-node candidate: FAIL / BLOCKED.** Three content-only revisions are sufficiently supported by committed native proof to present for director selection, but **none is approved**. No live work, implementation of production content, or publication is authorized.

## Refs / task

- Repository: `perseverance484/tnr-tools`.
- Fable frozen result: `claude/silent-bastion-budget-validation-69za5u@74eeb328f05d4258056b0a1c531619ffcf852ce3`. Branch was verified at exactly this SHA on review start; **not modified**.
- Fable base: `chatgpt/silent-bastion-node-budget-20261015@2af1ffd808f692d241b80c1d2c87e6e6d967016b` (exact merge-base per compare; three Fable commits ahead).
- Review baseline: `main@99e86dc549b86f1f4a5846c0e509fa6bc15b3463` (2026-10-16); merge to main is **not** this review's scope.
- Engine pin of tested behavior: `studie-tech/TheNinjaRPG@13d40c4c1509ecf44262aba1b5120266011ea786`. Later upstream `main@0651b039a466516a8fe24fc13b56f60dea11b7eb` (53 commits ahead) exists and is **not** the test target.
- Task: `docs/handoffs/SILENT_BASTION_CONDENSED99_NATIVE_PROOF_BRIEF.md`; source design `state/silent_bastion_condensed99_candidate.json`; Fable results `docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md`.
- Lead reviewer: Engineering Auditor; supporting lens: Content Designer. Director owns variant choice, Beacon policy, XP/ryo reward economy, and final publishing/acceptance.

## Verdict / findings

### C1 — Confirmed defect in original candidate (BLOCKING)

**Invariant:** losing a recovery battle after a later-division loss must replay that recovery at 50% HP/CP/SP, not send the player into REG2 nearly dead.

**Reproduction:** Fable `results/candidate/d_defect.json` records C1 for all four divisions. In D2 a `b2.recovery_later` fight starts with 50% HP, but its WIN edge `r2.reset_later_win` is pre-selected while the fight is still live; the reset fires before the outcome. A LOSS then exposes `d2.n.f2`, and the next normal REG2 starts at **1 HP (0.1%)**. The same observation appears for D3–D5. The candidate's gate D is green **because its expected result explicitly asserts that C1 reproduces**, not because the design satisfies the recovery contract.

**Independent source trace:** `studie-tech/TheNinjaRPG@13d40c4` `app/src/libs/quest.ts:1519–1527` pre-populates the consecutive next edge for an available, unfinished battle; `app/src/libs/objectives.ts:isQuestObjectiveAvailable` follows the selected chain without `done`; an available `reset_quest` emits its consequence in `app/src/libs/quest.ts:1379–1386`. This explains the observed reset-before-result. The bug is **not** safely acceptable; it violates the director's 50%-checkpoint rule.

### Alternatives: evidence supports all three (no director decision yet)

Fable's `derive_alternatives.py` adds a `dN.recovered` **dialog** between the recovery_later fight WIN and the reset, replacing immediate reset with an explicit player choice that cannot progress during combat. The three variants each fold only specified redundant single-option gates. Inspection of committed graph JSON against its source independently found:

| Variant | Nodes | Exactly removed per division | Effect on story/UX | Review recommendation |
| --- | ---: | --- | --- | --- |
| `alt99_f4gate` | **99** | `dN.n.f4` one-option dialog | Move the optional fourth regular's intro text into Command Terminal; keep full commander and wrong-answer approach scenes | **Preferred** |
| `alt99_alertgate` | **99** | `dN.n.boss.alert` one-option dialog | Wrong puzzle jumps to Security Alert boss; ensure all failure feedback exists in puzzle before choosing | Viable, weaker puzzle feedback |
| `alt95_bossgates` | **95** | Both `dN.n.boss.clean` and `dN.n.boss.alert` dialogs | Lose distinct Maintenance-route commander pre-battle presentations; +4 extra node budget | Viable if headroom is more important than presentation |

**Independent static structural calculation**, reading all four committed JSON graphs at the Fable frozen SHA: each has **one start at `d2.n.f1`**, no unresolved references, **no forward cycles including fail edges**, every node reachable, every battle has at least one dialog predecessor, **625 valid successful route combinations**, **16–20 battles per successful route**, exactly **four commander fights**. The original graph has four `battle.onWin → reset_quest` hazards; **all alternatives have zero**. This is an independent graph read, not a replay of Fable's MySQL harness.

**Native evidence inspected:** for `alt99_f4gate`, `results/alt99_f4gate/d_defect.json` verifies all D2–D5 recovery_later loss attempts keep the recovery battle active during combat, rewind to `dN.lost_later` after loss, and restart at **50%**. `r_runtime.json`: **7,033 checks, 0 failed**; `s_static.json`: **30 checks, 0 failed**; `e_edges.json`: **592 checks, 0 failed**. `bun_test.log`: **52 pass, 0 fail**. Fable reports deterministic second runs with all 16 core evidence files byte-identical. Equivalent committed per-variant evidence for `alt99_alertgate` and `alt95_bossgates` was inspected for defect-gate assertions.

**Scope limit:** We **did not independently execute** the Bun/MySQL/native runtime harness in this review environment. The reviewed evidence and pinned source support the findings, but not a claim of separately reproduced native database runs. Fable's fixtures impose battle outcomes and end pools via the upstream settlement test pattern; **AI battle actions and balance were not simulated**. Logbook was source-inspected, not browser/mobile tested.

### B1 — Source-verified entry timing change (USER DECISION REQUIRED)

The current tested engine debits the required Beacon **when the player starts the Pyramid run via `startQuest`**, not on the first initiated battle. At `app/src/server/api/routers/quests.ts:2899–2925,3047–3108` the entry charges are gathered and paid inside the run-start transaction via `payQuestEntryAtStart`; `app/src/server/utils/questEntry.ts` provides the guarded item debit and persisted `entryPaid` receipt. No-Beacon attempts are now refused before isolation, closing the old reachable F1/F2 window. Replays/abandonments do **not** refund the Beacon; retrying a division does **not** spend a second one.

This contradicts the prior *first battle only* director-approved description, but is not an authoring defect. **Recommend accepting the current native timing** rather than workaround semantics that bypass entry control. The UI/NPC copy must explicitly warn before the user commits: `Starting the expedition consumes one Skyglass Signal Beacon. Abandonment and failure do not refund it; division retries require no extra Beacon.` No final wording is adopted until director approval.

### Further deferred user decisions and integration risks

- **F3 retry income:** the native probe found repeatable ordinary battle XP/ryo from successive checkpoint loops with one Beacon; this may be material economically. Decide later whether to accept or suppress/scale replay gains (`scaleGains` must be source-tested on proposed routes). Do not quietly set a zero multiplier.
- **F4/F5 secrecy:** quest text, including the aftermath twist, is observable in public `quests.get` even on `hidden:true`. Intended narrative order is valid, but **cannot** be guaranteed against API data-mining. No game-code fix authorized.
- **D5 Combat Protocol:** `clearprevent` remains unsupported in the authored `questBuffTypes` list for battle-start player buffs; Fable used a **labelled stand-in**, not an accepted substitute.
- **Rulings ID collision:** `RUL-2026-10-14-001` is Medical100/protocol placement in Fable's design branch but an unrelated jutsu-art ruling on the later `main`. This is a **merge-blocking records conflict** to reconcile in the canonical decision history without dropping either decision.
- **Provenance and source drift:** current game main is 53 commits beyond the pinned runtime; rerun targeted authoring-integrated tests against an explicitly resolved target before release-readiness.
- The selected **deserted exterior / four interior divisions** ruling (`RUL-2026-10-15-001`) remains in force. The Gatewarden stays removed. None of the content-only graphs changes the approved four commanders, puzzles, rewards design ownership or entry lore.

## Next permitted step

1. **Director chooses** `alt99_f4gate` (review-preferred), `alt99_alertgate`, or `alt95_bossgates`; **do not accept C1**.
2. **Director accepts or rejects B1** run-start Beacon consumption. If accepted, update operative design, precise entry-copy and stale handoff fields. If rejected, an alternative content/entry contract will need separate feasibility proof (no game changes assumed).
3. Fable creates a **new or reassigned Fable-owned authoring branch** from the accepted frozen graph/approved plan and commits the selected graph as the **canonical symbolic source**, then regenerates/reruns native checks and carries on with four-division content authoring. The current candidate is BROKEN and must **not** be used by the one-shot authoring generator. Do not modify this Fable frozen handoff during the decision pause.
4. Keep F3, D5 unsupported tag, and final balances/rewards/art as explicit director approval gates before final production. Resolve rulings-ID collision when integrating with current main.

**Verification performed:** exact-ref/source check, full report/brief read, graph-by-graph delta inspection, independent DAG/reachability and 625-path structural enumeration, source-code trace of C1 and B1, direct review of committed S/D/R/E outcome files, report/provenance and Bun summaries. **Not run:** native Bun/MySQL/docker tests, live-game requests, game writes or browser. **Credentials:** none. **Game source modifications:** none.
