# Silent Bastion — complete offline authoring package: native results

**Verdict:**

- **The authoring package is complete and passes every native gate.** All 99 objectives have content. The four existing commander designs are translated into native rules. The 16 regulars are new, and all content-only blockers are documented.
- **Review correction round.** ChatGPT reviewed `16dbc5a2`; see `docs/reviews/SILENT_BASTION_AUTHORING_INDEPENDENT_REVIEW_20261016.md` on `chatgpt/review-silent-bastion-authoring-20261016@ba4fbaf5`. This revision:
  - applies RUL-2026-10-16-013, which closed F1;
  - fixes F2 (generator fail-open), F3 (validator diagnostic matching) and F4 (proofreading).
  - F5 stays a pre-manifest gate. See §7.
- **Every design and balance decision the package raised is now ruled** (RUL-2026-10-16-004 to -013). Earlier revisions applied them:
  - compiles and natively tests the approved completion caches;
  - marks the accepted values and copy;
  - records the puzzle validator exception.
- **Still open for the director:** cache names, cache and Beacon rarity, cache description wording and art.
- **Before any manifest:** fresh reads, username checks, the calibration fight and the two-phase build. Publication is not authorized. See `state/silent_bastion_authoring/decision_docket.md`.

- **Contract:** `state/prompt_silent_bastion_complete_authoring.md` at `chatgpt/silent-bastion-caches-claude-handoff-20261016@25d2b2e159d9fb9b0769db5483571e0db87991f6`.
- **Lock:** `state/silent_bastion_approved_authoring_lock.json`.
- **Graph:** `alt99_f4gate`, sha256 `c70fad7a…ee20`. The composer verifies it before building.
- **Package:** `state/silent_bastion_authoring/` (README there). **Harness:** `harness/silent_bastion_authoring/`. **Evidence:** `harness/silent_bastion_authoring/results/`.
- **Engine:** `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb`. This was upstream `main` when the run started, re-verified. The final run used a fresh clone and export.
- **Live requests/writes:** 0/0. **Credentials:** none. **Engine changes:** none. **`push/`:** untouched.

## 1. What was delivered (contract §5)

| # | Deliverable | Where |
| --- | --- | --- |
| 1 | 20-slot encounter catalog: 16 regulars + 4 commanders, source-mapped | `compiled/encounter_ledger.json` |
| 2 | 16 **new** regular profiles. Kits are drawn only from the shared pool, and commander signature jutsu are not reused. **The four pre-authored commanders are translated, not redesigned:** every rule cites its roster or profile line, with kits of 10/11/12/14 = 47 positions plus Countermand, and rule counts of 13/14/15/20 (≤20) | `design/regulars.json`, `design/commanders.json`, `compiled/ai_profiles.candidate.json` |
| 3 | All **99** objective payloads, **45** dialogs and 4 puzzles. The clues are planted in each division's first three dialogs, and the answer order varies (correct answer at position 2/3/2/1) | `design/script.json` → `compiled/quest.candidate.json`, `compiled/story_script.md` |
| 4 | Protocol ledger (exact targets), Beacon candidate and copy (charge at start, disclosed), story script | `design/protocols.json`, `design/entry_and_rewards.json` |
| 5 | Candidate stat ladder, reward economy, F3 farm math with `scaleGains` options, decision docket | `economy_and_f3.md`, `decision_docket.md` |
| 6 | Art shotlist and brief (20 avatars, 6 scenes, 5 icons). No binaries | `art_shotlist.md` |
| 7 | Deterministic composer and source extractor, each with `--check` | `tools/{compose,extract_sources,gen_regulars,gen_script}.py` |
| 8 | Validation matrix and tests | §2 |
| 9 | This report and the frozen SHA | §6 |

## 2. Gates (`harness/silent_bastion_authoring/run.sh`, final run, fresh engine clone)

| Gate | Result |
| --- | --- |
| **G** — generators `--check` (sources, regulars, script, composer, C99 derived graphs), each with its own exit status | **all current**. Runner self-test `test_gencheck.sh`: 0 failed |
| **V** — `validate.py` on the validation-only manifest (now including both cache items) | **exit 1; 11 errors, 9 warnings; the exact lines and counts are documented (11/11).** Self-test `test_check_validate.py`: 0 failed. **Not a validate-clean result.** See §3 |
| Upstream preflight: 9 engine suites (AI v2 rules/targeting/unreachable/summon, seal/stealth, quest reset, Pyramid consequences, entry charge, run state) | **117 / 117** |
| **A** — AI (pure; real decision engine, real captured jutsu records) | **218 checks, 0 failed** (50 tests) |
| **C** — compiled content + real saves | **45 checks, 0 failed** (10 tests), including the new unbalanced-quote check (F4). Includes `scaleGains` 0 on exactly the 8 recovery battles, the approved D5 buff, and the completion caches (C1b static, C2 native) |
| **D/R/E** — frozen C99 runtime gates with **the compiled candidate quest** as the fixture | **D 543, R 7,033, E 592 checks, 0 failed** |
| **I** — recovery income on the compiled quest (new, RUL-2026-10-16-005) | **456 checks, 0 failed** (4 divisions). Compiled-runtime suite total: 41/41 tests |
| Deterministic re-run (second full `run.sh`, scratch output) | **exit 0; all 7 evidence JSON files byte-identical.** `validate_py.txt` has the same lines; only the order of two warnings changes between runs (from `validate.py` itself) |

### Contract §5 item 8 matrix → evidence

| Required | Result | Gate |
| --- | --- | --- |
| Graph: 99 nodes, 625 routes, 16–20 combats, single root, dialog-gated battles | PASS. Node by node, the compiled quest matches the locked graph, including opponents, `givePools` and reset targets | C |
| Recovery: REG1 losses and wins, recovery_later loss replays at 50% (no C1) | PASS. C1 is absent in all four divisions | D, R |
| Completion caches as ruled (RUL-2026-10-16-010) | PASS. Both cache effects pass `NonCombatConsumeRewardTag`, and both stored rows pass `ItemValidator`. Weights are 1 roll, Epic 5000 / Legendary 5000. Every Epic entry equals one whole pool recipe and every Legendary entry exactly 40% of one. The caches are untradeable and target SELF. **24 native openings** (12 per cache) through `item.consume` each granted exactly one whole compiled bundle and destroyed the cache. Which bundles were drawn is random, so it goes to `c_content.timings.json` | C1b, C2 |
| Single terminal reward | PASS. The compiled quest has quest-level `choose`, pick 1, and two cache cards; nothing on objectives. The runtime pays the completion reward once; the cache choice itself is proven on the reward-proof branch | C, R, reward proof |
| Recovery wins pay nothing (O2) | PASS. In every division a recovery win (first and later) has battle `rewardScaling` 0, pays 0 money and 0 XP, and still advances the graph; a first-pass win has `rewardScaling` 1 and pays XP. The C99 gate E8 agrees: per farm loop XP fell from 64 to 32 because only the regular win pays now | I, E |
| Carryover, Medical 100, player-side Combat and Security Alert | PASS. Every battle start is checked; effects land on the player only and are allowlisted | R, C |
| Beacon charged at start | PASS. One Beacon at `startQuest`, none on retries, never refunded | R, E |
| Arakane hard fail | PASS on all four routes | R |
| Real editor save of the compiled 99-objective quest (hidden) | PASS (128,074 bytes of content) | C |
| Commander rules save natively | PASS. All 20 profiles save through `ai.updateAiProfile` (`includeDefaultRules:false`, every rule kept). A 21-rule control is refused by the server cap | C |
| Commander behaviour follows the authored priorities | PASS. Every roster priority for Master of Arms, Replicant Zero and the Grand Marshal, and each tested Arakane rule (1–11, 17–20), fires as authored. Highlights below | A |

Commander behaviour highlights (gate A, real `performAIaction`):

- **Master of Arms.** Below 60% he opens with Sovereign Ascendance; at exactly 60% he does not. He Clears at player IDG 71 but not at 70, and uses Pierce against shields. His opener is the Tempo Fracture + Fighter's Poise combo, and Cataclysm follows Tempest Cleave's IDT. Over 8 rounds: B08+B37, B16, TC, B14, B28+B37, S07.
- **Replicant Zero.** He opens with Barrier + Hexweave and casts Split Image exactly once (the clone takes its own turns). Stolen Form answers high IDG, Bulwark comes below 65%, and Second Wind below 40% when Bulwark is on cooldown.
- **The Grand Marshal.** His sequence is Ruin, Malediction, Unraveling Strike up close or Nullifying Wave at range, Undertow anti-kite at 5, then Cataclysm on a stunned target, with Martial Law below 55%.
- **Arakane.** He opens with Apex Hunger; against a kiting player he goes Veilstep → Countermand + Solar Bow while stealthed, with no jutsu cast while stealthed. Stolen Form + Countermand runs at 60 + 40 AP and Zephyr Lance answers shields.
  - Crossbow fires when Countermand and Solar Bow are on cooldown.
  - The Last Directive fires at HP 29% but **not** at 30%.
  - Countermand's item Clear really strips the player's buffs.
- **No unit gave up** from exhaustion in any multi-round loop.

## 3. Findings

**AR1 — Arakane's ultimate can fire on an expired Final Stand (engine behaviour). Resolved: cooldown 4 approved, RUL-2026-10-16-004.**

- **Mechanism.** `routers/combat.ts` calls `alignBattle`, which lowers effect rounds to 0 without pruning them, and then `performAIaction`. `has_effect` sums raw power without `isEffectActive`. Authored rule 2 therefore passes at the first decision after Final Stand reaches 0 rounds.
- **Reproduction.** At the first-drafted cooldown 2, rule 2 fires in round 12 with Final Stand at 0 rounds (`AR.finalPhaseDecisions`).
- **Probe.** Cooldowns 2–7 were tested from start distances 4, 7 and 9:
  - cooldowns 2, 3, 5 and 6 can each cast on the expired round;
  - **cooldown 4** kept every cast inside an active Final Stand, with two casts per window;
  - cooldown 7 also stayed clean, but with one cast.
- **Decision.** Cooldown **4** is approved and compiled. The director accepts the residual risk for sequences the probe didn't cover; no engine change is requested.

**SRC1 — Veilstep's captured record (stealth 1r, cooldown 5) differs from the pool registry and the design prose (2r, cooldown 6).** The Arakane stealth branch works natively with the 1-round record. Resolved: the record is used as-is (RUL-2026-10-16-007); a fresh capture before the manifest still applies if it differs.

**TC1 not reproduced:** Tempest Cleave (`AOE_CIRCLE_SPAWN`, `friendlyFire: ALL`) never hit Master of Arms at path distance 2–5, so no extra gate was added.

**VAL1 — `validate.py` lint L18 is stale against `0651b039`.** It forbids `clear` on items, but `ItemValidator` accepts it and gate A shows the item Clear working in combat. This is tooling, Lane A, and is not changed here.

**VAL2 — `validate.py`'s tag schemas predate Weighted Cache.** `skills/building-tnr-content/data/46_DATA_tag_schemas.json` was extracted 2026-07-10. It reports `rewardMode` and `weightedCache` as unknown fields on `noncombatconsumereward`. At `0651b039` the engine's own schema accepts both, and gate C opens the caches natively. Lane A tooling; not changed here.

**Caught and fixed by validate.py this round:** both cache items now carry item `target: "SELF"` (lint L18); the factory default was `CHARACTER`. Tradability uses the engine column `canBeTraded`.

**`validate.py`'s 11 remaining errors, all documented in `tools/check_validate.py`:**

- 2 are the two-phase build requirement: Arakane's exclusive jutsu need literal IDs.
- 4 are the locked puzzle topology: both wrong answers share the Security Alert node. The validator exception is granted (RUL-2026-10-16-012).
- 1 is VAL1.
- 4 are VAL2.
- The 2 unresolved-cache-ref warnings are gone now that the caches are compiled.

**F3 — resolved with O2 (RUL-2026-10-16-005).** The 8 recovery battles carry `scaleGains: 0`. Gate C checks the value survives `QuestValidator` on exactly those battles. Gate I (§2) shows natively that a recovery win still settles and advances, with `rewardScaling` 0 and no money or experience, while a first-pass win pays.

**RC1 — accepted with copy (RUL-2026-10-16-009).** The quest description tells the player to claim an earlier reward before setting out. The reward-proof branch is unchanged.

**D5 — Debuff Prevent 100 / 3r (RUL-2026-10-16-008).** The director delegated the pick. Option A was chosen because it is native-proven and fits the Sanctum's fiction, while leaving the endgame threat intact. The D5 dialog and battle text now describe it.

**Earlier findings at this pin:** F4/F5 text exposure is accepted (RUL-2026-10-16-012); B1 (Beacon at start) was approved earlier. C1 is absent from the selected graph.

**Notes on the brief's assumptions:**

- The Grand Marshal's stacked DDG had fully expired by round 8 in the passive-player loop (`GM.playerDDGStackAfter8` is empty). The kit, double DDG included, is now ratified (RUL-2026-10-16-006).
- The Division IV puzzle and the Order-Bearer's blank seal foreshadow the unknown issuer without naming it (docket item 12).

## 4. Fixture limits and what was not tested

- Gate A drives the real AI decision engine against a passive player. It simulates no damage race, no player AI and no difficulty. Balance needs the calibration protocol and director acceptance.
- On this grid an adjacent target reads below path length 2, so behaviour scenarios use distance ≥3. Gate A3 also covers distance 2 for Tempest Cleave.
- Runtime gates impose battle outcomes with the upstream settlement pattern. The completion reward in D/R/E is the harness sentinel; the cache choice is proven on the reward-proof branch.
- Jutsu records come from committed operator captures (2026-08 to 2026-10); the weapons come from the upstream seed. **None of these is a fresh live readback.**
- Not done: a live manifest, art, browser or Android checks, hidden write or readback, username-collision checks, fresh reads of the cache ingredients (2026-10-13 census capture), and the coherence gates for `skills/` or doctrine (no such files changed).

## 5. Reproduce

```bash
harness/silent_bastion_authoring/run.sh      # needs git, bun 1.4.x, python3, unshare, docker; clones the pinned engine
python3 state/silent_bastion_authoring/tools/compose.py --check
```

Provenance is in `results/provenance.json`: the engine pin, `bun.lock`, the SHA-256 of 12 engine source files, and the SHA-256 of every package, harness, lock, graph, contract and design-source file.

## 6. Handoff

- **Repository:** `perseverance484/tnr-tools`
- **Branch:** `claude/silent-bastion-authoring-69za5u` (Fable-owned, sole writer)
- **Base:** `25d2b2e159d9fb9b0769db5483571e0db87991f6`. The merge-base with `main@99e86dc` is reported at handoff.
- **Frozen head:** the commit that adds this revision. The SHA is in the handoff message. It supersedes the reviewed head `16dbc5a2976a463be1f9506e007f10bd0814e85d` (and before it `01643c80` and `d648c62a`). Since `16dbc5a2`, the only changes are the review corrections in §7.
- **Companion proof:** `claude/recipe-cache-native-proof-69za5u@b133d73286df9e48ba1015b21dd694c69c9ea090`. It is independent, not merged here, and pending its own review.
- **Next:** ChatGPT independent audit of the frozen SHA. After that, the director works through `decision_docket.md`.

## 7. Independent review corrections (`16dbc5a2` → this head)

| Finding | Disposition | Change | Evidence |
| --- | --- | --- | --- |
| **F1** Extermination Order fields and the two weapons were still candidates | **Closed by RUL-2026-10-16-013**; metadata applied. Combat values unchanged. | Entry copied verbatim from the review branch into `docs/RULINGS.md`. In `design/commanders.json`: Extermination Order status APPROVED (60 AP, r5, single, 80 dmg, Elemental Seal 100/2r, Cleanse Prevent 100/2r, CD 4, active Final Stand only); effect notes `approval` instead of `candidate`, including The Last Directive's IDG 30 (already RUL-011); Arakane `itemsStatus` (Countermand, Solar Bow HAND_1, Crossbow HAND_2 approved, fresh captures required). Arakane profile and docket updated. | `compiled/ai_profiles.candidate.json` and `compiled/cache_items.candidate.json` are byte-identical to `16dbc5a2`. The quest and validation manifest differ only in the 9 F4 texts (plus the quest status string). Gate A 218/0 |
| **F2** generator runner fail-open | **Fixed.** | `tools/gencheck.sh`: every check runs, and each check's own nonzero exit or `STALE` fails the gate. `run.sh` uses it after running `tools/test_gencheck.sh` (first/middle/last failure and STALE cases, plus later checks still running). | Self-test 0 failed. Real-command reproduction: first generator pointed at a missing engine. Old grouping `GEN_STATUS=0`; new runner status 1, with the failing command named |
| **F3** validator matching used a set | **Fixed.** | `tools/check_validate.py` compares a `Counter` of verbatim ERROR lines (no truncation), the summary error count (11) and warning count (9), and exit status 1. Logic is in a pure `judge()`; `tools/test_check_validate.py` runs first in `run.sh`. | Self-test 0 failed (duplicate, missing, reworded, new, summary mismatch, warning change, exit 0, killed, crash all fail). Real run 11/11 |
| **F4** missing quote; defeat text said pools were already at half | **Fixed in `tools/gen_script.py`.** | `d3.n.boss.alert` now ends `"Neither will you leave."`: the closing quote had been swallowed by Python's triple-quote parsing. In all 8 `dN.lost_first/later` dialogs the pool clause now reads "your next trial begins with your pools at half"; story, choices and graph are unchanged. | Gate C: no objective text or option label has an unbalanced double quote |
| **F5** full AI loadout and combat integration | **Open pre-manifest gate** (docket item 9a) | Not built here, by the review's scoping. The release stays BLOCKED. | — |

