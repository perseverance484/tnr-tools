# Resort in Need — Independent Employee Event Review

**Date:** 2026-10-13  
**Verdict:** **HOLD — revision required before director acceptance/publication.**  
**Repository:** `perseverance484/tnr-tools`  
**Review branch/base:** `chatgpt/review-resort-in-need-20261013` / `da3f30779259cf4a9dd82c9ecbb05bd25ff9a00d`  
**Quest:** `xG0_Jq-amzhFgcLy8BVjw` (`Resort in Need`)  
**Capture:** `harvests/inbox/tnr_results_1791902022789.json` at main `da3f30779259cf4a9dd82c9ecbb05bd25ff9a00d`, successful full `quests.get` point read at `2026-10-13T14:33:42.789Z`.  
**Game-source reference:** `studie-tech/TheNinjaRPG@922d61bbf4897014555463c4084f7ded40be2db7` (2026-10-13).  
**Role:** Content Designer; Engineering Auditor lens.  
**Boundaries:** Repository and source reads only. **Zero live-game requests, zero live-game writes, no credentials, no runtime playtest, no content modifications or publication.**

## Executive assessment

**Staff-review status:** Comprehensive review **in progress**. The earlier conversational 6/10 score is **provisional and must not be presented as the final employee rating**, since the two quest AIs and their behavior profiles have not yet been reviewed. The director requires **one consolidated review** covering quest, AI, rewards, technical correctness and prose; no topic is to be put into a separate follow-up review. A read-only AI baseline is staged in `push/99_resort_in_need_ai_review_capture.json` on main (`abb749d4e45fdbb522a72a59143b45c0374cd3ec`). Do not claim it has run until an exported results bundle proves it.

A potentially enjoyable coastal investigation begins with jellyfish exhibiting anomalous chakra abilities and escalates through a ship voyage to a giant chakra beast. The author has a coherent beginning/middle/end and the stored quest graph is structurally complete. But the released player experience would presently be at risk from two misplaced battles, the currently configured one-attempt limit (director has ruled for 100 attempts while keeping all fail routes), long stretches of travel/continuation without meaningful gameplay, and a sealing climax that is not mechanically represented. The payout is entirely unconfigured; its desired value is a **director decision**, not a defect to auto-fix.

This is an **employee-content revision**, not a Forge implementation or engine-source review.

## Verified positive findings

- Live quest is **hidden**, `questType: event`, D rank, required level 1, max level 100, `consecutiveObjectives: true`.
- Static graph traversal over ordinary `nextObjectiveId` and battle `failObjectiveId`: 32 objectives, one root (`89nzR`), all 32 reachable, no unknown edges, no directed cycles. Counts: 18 dialogs, 8 movement, 4 `defeat_opponents`, one `win_quest`, one `fail_quest`.
- Each battle carries a `failObjectiveId`; all twelve location objectives have nonempty map-marker image URLs.
- `defeat_opponents` uses a valid source schema including `sectorType: "specific"` through `complexObjectiveFields` (`app/src/validators/objectives.ts`, lines 492–509 and 563–570). An older H19 note in `references/quest.md` says otherwise; do **not** misreport this as a schema violation.
- Every dialog has an option. A single top-level `content.sceneBackground` exists; game `Logbook.tsx` lines 497–519 fall back to it when node scenes are empty. This is a **repetitive presentation**, not an empty-scene runtime defect.

## Findings (in priority order)

### RIN-01 — BLOCKER: late battles target sector 0, tile (0,0)

Captured `defeat_opponents` nodes **`0SvwH`** (third jellyfish fight) and **`nr_5q`** (boss fight) both have `sectorType: specific`, `locationType: specific`, `sector: 0`, `longitude: 0`, `latitude: 0`. The preceding voyage step **`tTOUQ`** takes players to sector 847, tile (22,9); the underwater approach **`mbLvI`** takes them to sector 919, tile (21,18). Neither fight has an overworld-placement binding.

The pinned engine resolves `specific` location from stored fields (`app/src/libs/quest.ts` lines 953–955, 1011–1023); unbound objectives require location matching (`app/src/libs/quest.ts` lines 297–342). A new map-reachability repair can snap tile coordinates to a nearby walkable tile when a suitable published map exists (lines 1630–1674), but it does not establish that sector 0 is the intended stage. There is **no player-run proof** that these battles trigger correctly. Repository law 54 specifically warns about `0,0` location nodes.

**Required correction:** bind these battles to the intended quest sectors/tiles, aligned with the story and prior movement objective, then source-check and playtest the progression. Do not try to “fix” the engine or replace `specific` with `random` as a shortcut.

### RIN-02 — DIRECTOR-RULED: preserve fail branches; raise maxAttempts to 100

**Captured live state:** `maxAttempts: 1`, `maxCompletes: 1`, `retryDelay: "none"`, `attemptDelay: "none"`. The four multi-option dialogs (`89nzR`, `l5Miv`, `8YT8K`, `TLuVn`) each include a voluntary `fail_quest` branch to `jF6G_`; every battle loss also routes there. The pinned source enforces attempt and completion caps on event quests (`app/src/libs/quest.ts` lines 2030–2042).

**Director decision, 2026-10-13:** Keep **every existing `fail_quest` node and all existing player-choice and battle-failure routes**. Change only `maxAttempts: 1 → 100`, preserve `maxCompletes: 1`, and leave `retryDelay` and `attemptDelay` unchanged. Do **not** remove refusal choices, add `reset_quest` retry routes, or change the intended failure consequences.

**Player consequence:** Up to 100 lifetime quest attempts, with at most one successful completion. Each failed or deliberately abandoned run can be started again, subject to the 100-attempt ceiling. This is not an unlimited retry policy.

**Implementation boundary:** Design decision only; Fable prepares/validates any in-place edit from a fresh full capture, and the director alone initiates the live-game update. The captured quest still holds `maxAttempts: 1` until the operator applies the change.

### RIN-03 — DIRECTOR DECISION: zero configured quest rewards

`content.reward` contains all zero/empty reward fields, and all 32 objective-level rewards are zero/empty. No authored quest EXP, money, items, tokens, jutsu or progression reward is captured. This says nothing about possible separate AI combat drops, which were not audited.

For a currently one-attempt, director-ruled 100-attempt / one-completion event with 8 travel steps and 4 battles, this is a poor reward-to-effort proposition unless zero payout is explicitly the event's purpose. The separate *The Crown in the Surf* design draft (`docs/design/JELLYFISH_COAST_QUEST.md`) expressly specifies no rewards, but it is a distinct candidate and does **not** authorize applying that rule here.

**Consolidated staff-review requirement:** the employee should either propose an appropriate reward package or explicitly justify why the event is meant to be rewardless. Assess that proposal together with quest and AI revisions, not as a separate later review. The director still owns the approved reward types, values and rarity; the reviewer does not select those figures.

### RIN-04 — MEDIUM: high travel and narration overhead for D-rank onboarding

Graph composition: 18 dialog nodes, 8 location movement nodes and 4 battles. The harbor charter uses multiple mandatory “Continue” conversations; ship repairs require a detour to Akasumi sector 1334 and back; roughly a week passes entirely through dialogue with no elapsed-time mechanic. `Ecyo6` claims to move to the marina but is at the same sector 847, tile (11,12) as the prior battle `0e35I`, so the player can already satisfy it. `zZkf5` says “Collect Shipwrights tools” but is only `move_to_location`, without collection or delivery state. Another objective says “Head to 22,9” instead of using in-world language.

**Recommendation:** compress repeated conversations, cut or give a concrete purpose to the repair detour, and make travel objectives describe clear destinations. If tools actually matter, use `collect_item`/`deliver_item` with an approved item; otherwise just call it “Visit the shipwright” rather than pretending to award physical tools.

### RIN-05 — MEDIUM: sealing climax is narrated, not earned

At `TLuVn` the player concludes “You know you can’t beat this thing. You must seal it away,” selects special underwater breathing equipment that has never been acquired or established, and follows `mbLvI` into an ordinary `defeat_opponents` boss at `nr_5q`. The following `MMv29` simply announces that the beast was sealed. Nothing in the graph demonstrates or rewards an actual sealing action.

**Recommendation:** foreshadow the sealing method, obtain or prepare it in the quest, and make the final encounter's objective logically support the announced outcome. This can remain a simple battle followed by a grounded seal activation, without new jutsu or complex mechanics if the director prefers.

### RIN-06 — MEDIUM: completion presentation is abrupt and malformed

`MMv29` resolves the beast, then `td-XJ` sends players back to shore and `VXw0X` is a silent `win_quest` transition. The wildlife team never appears in a final interactive dialogue. Both top-level `successDescription` and the win-node version use inconsistent/unclosed quotation marks. `app/src/layout/Logbook.tsx` lines 919–928 show a resolved quest can show the top-level success description. Repository law 47 confirms win-node text is not itself a story dialogue.

**Recommendation:** add a short visible report-back conversation with the wildlife team immediately before `win_quest`; normalize the top-level completion text.

### RIN-07 — POLISH: draft-level grammar, vague objectives, repetitive visuals

Example text to proofread:
- “jutsu’s” → “jutsu”; “something similar to” + “resembling” is redundant.
- “Boat’s make me seasick” → “Boats make me seasick.”
- “Sound's like work” → “Sounds like work.”
- “Dawn special underwater breathing gear” → “Don special underwater breathing gear.”
- “As you make your down further” → “As you make your way farther.”
- “beachline” → “shoreline”; inconsistent offshore/town/harbor capitalization and dialogue quotation styles.

Seven location/fight objectives have empty descriptions: `0e35I`, `Ecyo6`, `igQ-i`, `0SvwH`, `mbLvI`, `nr_5q`, `td-XJ`. Several choices include leading/trailing whitespace. Dialog uses `parseHtml`; embedded raw newlines are not reliable paragraph breaks. All 32 per-node scene backgrounds and characters are empty; fallback to the one top-level background is source-confirmed, so there is no missing-scene error, but beach/harbor/ship/open-sea/underwater scene changes would improve presentation.

### RIN-08 — UNVERIFIED: four battle difficulties cannot be certified from a quest-only capture

Battle opponent counts are **2**, **3**, **2**, **1** in four consecutive fights; the first three use `1WAgDucRwcwGZ_yQ9r0uN`, final boss uses `msKodzIJSH2J_BO-1FCIN`. Each uses `opponent_scaled_to_user: true`. In the quest's `opponentAIs`, `number` means simultaneous combatant headcount, not successive waves. Neither AI id is in the repository's seed/name census consulted during this review; absence from a stale catalog is not proof of a missing live AI.

A level-1 eligible D-rank event with 2/3 opponents may be disproportionately punishing, but actual strength **cannot be judged without those AI records, kits, scaling and a test run**. A read-only `quests.get` + both `profile.getAi` baseline is now staged under `push/99_resort_in_need_ai_review_capture.json` on main. Capture both live AIs first; derive any `ai.getAiProfile` IDs strictly from their returned `aiProfileId` values, then review priority/range/default fallbacks, combat stats, equipped jutsu/items, drops and the quest's scaled multiplayer encounters. Do not reuse stats from a different jellyfish candidate.

## Final review disposition and operator gates

**Not approved for publication.** Correct the two battle coordinates and verify quest progression; apply the director-ruled `maxAttempts: 100` while preserving `maxCompletes: 1`, the four optional `fail_quest` choices, and existing battle-loss routes. Staff-facing requested changes focus on battle coordinates and proofreading; the separate pacing/sealing/presentation observations are optional design feedback, not mandatory redesign requirements. Include the employee's reward proposal (or explicit zero-reward rationale) and our AI assessment in the **same final staff review**; no part of the submission is delegated to a separate review. Reward amounts remain director-owned. Following any full-record quest edit, recapture the current live record before additional changes because editor saves and quest updates can overwrite unrelated fields (ENGINE_LAWS 58).

The event currently remains hidden. This review does not authorize unhide, quest update, item/AI edits, schema adoption or gameplay changes. Fable retains ordinary content-manifest implementation ownership; the director retains reward, rarity, balance, acceptance and live-operation authority.

**Evidence limitations:** full successful capture of exactly one quest only; no corresponding AI/profile reads yet; the staged read-only `push/99` capture has not yet been operator-run. No CDN/art byte checks or in-game playthrough. No `validate.py` run on the new capture manifest in this ChatGPT environment; manual safety assertions confirm `items: []`, three full point reads and no `after` calls. Static graph checks were performed in-memory on the 32 captured objectives. Hold the employee score until both AI records and any live AiProfiles are reviewed.
