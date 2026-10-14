# Silent Bastion — Phase 1 structural graph and native-proof handoff

**Status:** STATIC DESIGN GRAPH PASSED; NATIVE RUNTIME / ENGINE-VALIDATOR PROOF PENDING. Do not call Phase 1 complete or the event release-ready.
**Lead:** ChatGPT Content Designer, supporting Engineering Auditor; **native implementation/tests:** Fable / Claude Code, owning a separate `fable/*` branch. **Director:** dauntless owns progression acceptance, combat buffs, rewards, publishing and every live-game action.
**Live requests/writes:** 0. **Credentials:** none. **Publication:** none.
**Repository:** `perseverance484/tnr-tools`; graph at `state/silent_bastion_phase1_graph.json` (introduced `5212b8c25d9195e5f8691d06da75e660685839ac`); original release plan `state/silent_bastion_release_plan.md`.
**Planning refs:** `main@1da18301e8e4660cedf3daa3e80893a2ac918f2b`, `chatgpt/silent-bastion-design-20261013@876b58cc9046b6c2528869d97c7038335f299f4e` before graph commit; merge-base `057acddb986b50e486ccf550fac00b68fff51490`.
**Pinned game:** `studie-tech/TheNinjaRPG@c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd`.
**Authority routing:** `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/workflows/CONTENT_WORKSTREAM.md` (on main), `docs/DEVELOPMENT_WORKFLOW.md`, `skills/building-tnr-content/references/{quest,ai,balance,item}.md`.

## 1. Exact candidate flow

One new isolated `battlepyramid` quest, five divisions and 25 distinct encounter slots (four regular plus commander per division). Every fight has a directly preceding dialog, and every terminal is after regular fight 3. Correct Maintenance bypasses regular fight 4; incorrect Maintenance also bypasses it but adds a temporary boss-only Security Alert. Medical and Combat each require regular fight 4 and then use distinct commander battle nodes with their respective battle-start values/effects. The win/aftermath is single and only after Arakane.

**Critical new workaround, awaiting native proof:** each division has two structurally separate lanes:

- `n` (first entry): start first regular battle **without** `givePools`, preserving carried pools. Any loss except final Arakane switches, by that battle's **fail edge**, into the `r` lane's first dialog.
- `r` (after a division loss): its **first regular battle only** carries `givePools=50`. Later battles in that retry lane preserve carry except Medical's commander battle `givePools=75`. A new loss from the retry lane goes to a single division-specific `reset_quest` pointing back to the retry first dialog. This is the ONLY graph cycle and is expressed via `resetObjectiveId`, deliberately excluded from the ordinary objective-edge DAG. No extra entry item should be spent.
- Success against any commander variant (initial or retry) joins the **next** division's ordinary `n` lane, *not* its retry lane. Arakane loss on either lane goes to the shared `fail_quest` terminal.

Why duplication is needed: a `start_battle` author's `givePools` is an unconditional battle-start percentage; there is no proved native predicate meaning “only after a prior loss”. A single shared initial battle would either always reset players to 50% or never do so. The retry lane makes prior defeat explicit in the selected graph path. No engine patch is assumed.

**Notation:** `d3.n.f1` = first-battle gate in division 3, initial lane; `b3.r.f1` = first regular fight on the division 3 retry lane with 50% starting pools; `b5.n.boss.medical` = Arakane on Medical route, with 75% starting pools. All 208 nodes/links are in the JSON; it is **symbolic and not a game payload**.

## 2. Static design-graph QA — performed

A source-shaped independent adjacency check of the committed symbolic graph yielded:

| Check | Result |
| --- | --- |
| Distinct nodes | **208**: 111 dialogs, 90 battle objectives, 5 resets, 1 win, 1 fail |
| Unique directed root | **1** — `d1.n.f1` |
| Reachability | **208/208** (success + fail edges; reset targets are not graph edges) |
| Non-reset graph | **acyclic** |
| Battle gating | **90/90** directly preceded by exactly one dialog |
| Unique encounter identities | **25** (five divisions × [regular 1–4, boss]) |
| Retry 50% effects | **5** (only `b1.r.f1` through `b5.r.f1`) |
| Medical 75% effects | **10** (initial + retry commander Medical variants) |
| Boss-only symbolic effects | **20** (10 Security Alerts, 10 Combat Protocol buffs) |
| All-success branch selection combinations | **3,125** (five terminal outcomes per division, including the two wrong puzzle answers) |
| Successful path length | **20–25** battles; exactly **five** commanders on every path |
| Win-node/reward location | Exactly **one** `win`; no per-floor rewards in symbolic data |

A separate selected-link **model simulation** of the committed JSON (not the live engine) traversed initial-loss cases at first regular, third regular, fourth regular, division IV commander, and division V regular encounters; every case entered its own division's retry lane and found `givePools=50` on its next first regular fight. Losing to Arakane instead reached `f.arakane`. A second loss inside the retry lane passed through `r1.retry`, cleared its selected path and re-entered `d1.r.f1` with 50% at the next first battle. These checks are **not** equivalent to source-runtime tests.

## 3. Source evidence (read-only, pinned)

- `app/src/libs/quest.ts:2168–2305`: `verifyQuestObjectiveFlow` counts success and fail edges, requires one root, acyclic graph, and full reachability; `resetObjectiveId` is not a normal traversal edge.
- `app/src/libs/objectives.ts:51–66,148–182`: predecessor and active-path selection use the authored links and per-player `selectedNextObjectiveId`.
- `app/src/libs/quest.ts:1188–1243,1460–1529`: authored `start_battle` conveys pools/effects, losses select `failObjectiveId`, and recently-died handling may affect first/repeat retries.
- `app/src/server/api/routers/quests.ts:4037–4086`: a `reset_quest` clears the reset target's selected-chain goals rather than being an ordinary link.
- `app/src/validators/objectives.ts:408–424`: `givePools` supports 0–100; `applyBuffs`/`applyDebuffs` use the supported starting-tag allowlists. Empty `givePools` preserves carry.
- `app/src/validators/combat.ts:1098–1169`: starting effects require duration and allowlist membership. In particular, `clearprevent` is **NOT** currently among allowed player starting buffs, so the advertised Arakane Combat Protocol **cannot** be implemented as drafted.
- `app/src/libs/questRun.ts` and `app/src/server/api/routers/combat.ts`: isolated-run and `entryPaid` item payment are persisted game constructs, still needing full checkpoint regression tests.

## 4. Fable's mandatory next native-proof packet

On a Fable-owned branch, load the pinned game source, current quest schema/contracts and the design JSON (don't work on the active `chatgpt/*` branch). Construct an **offline, schema-correct fixture** (not a live write, not production manifest), run `QuestValidator` and `verifyQuestObjectiveFlow`, and test using the actual `getNewTrackers` / quest consequence / combat initiation paths. Resolve any gaps by reporting them for director judgment rather than changing gameplay semantics silently.

**Required cases:**
1. First entry: Beacon consumed **once when first battle starts**, `entryPaid` persists through both lanes/retries, the player cannot leave isolation and secretly recover.
2. All four per-division terminal outcomes: Maintenance correct and each wrong choice bypass fight4 (wrong => boss Security Alert only); Medical and Combat both fight4, apply **player** pool set-to75 or approved player combat buff **only on their corresponding boss battle**.
3. Every initial-lane loss in divisions 1–5 (including div1–4 commanders) enters the **same division's** recovery lane and starts its first regular battle at exactly 50%, without resetting healthy first entries or transitions from a defeated commander.
4. Every retry-lane regular/boss loss (except Arakane) repeatedly clears and re-enters its own retry corridor; **two consecutive losses** must not strand on `recentlyDied`, repeat the wrong boss/terminal route, or break the single selected path.
5. Defeat to Arakane hard-fails and ends the entire attempt; abandonment releases isolation; neither refunds the Beacon. The success ending can pay rewards **only once**, after five commander wins.
6. No auto-fired adjacent battle, accidental reward, free healing, wrong/extra enemy or multiple active `start_battle` objectives. Verify carried HP/CP/SP across ordinary victories and division transitions.
7. Timing/UX/performance with **208 objectives / 90 authored battles**, including hidden-run pause/version changes and mobile Logbook navigability. Exceeding current limits is a blocker, not permission to split the approved single Pyramid into five quests.
8. Zero network/live-game requests. Mock production state locally and document test fixtures, exact source SHA, test commands, results and any unresolved engine gaps.

**Exit gate:** Phase 1 becomes *verified* only with source-native tests + validated schema-correct fixture, reviewed against the approved design; Fable freezes a handoff SHA and ChatGPT independently reviews that SHA. Report any architecture defect before progressing to AI/rewards.

## 5. Explicitly deferred, not implied approvals

The director-approved **two regular enemy archetypes per division** belongs to Phase 3 (10 identities across 20 encounters), not this graph's combat records. The Grand Marshal's 12-move candidate, all exact boss stats, the temporary Protocol values and Security Alert strength, item drop/economy, art and story dialogue remain separate. The latest Discord Protocol list and the roster differ, and `clearprevent` on a player boss-start is currently unsupported. No speculative effects or rewards should be treated as finalized by this artifact.

**Administrative:** At the appropriate integration boundary, Fable should use `scripts/content_workstream.py` to initialize/validate/render the `silent_bastion` multi-session roadmap from `docs/workflows/CONTENT_WORKSTREAM.md` rather than hand-edit generated projections. Reconcile the shared main branch first; project `active-context`/`status` are generated and remain untouched.
