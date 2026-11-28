# AI player AP1 independent review

**Verdict: REQUEST CHANGES.** The normal-path tests pass, but the frozen implementation does not yet establish the promised turn safety or shared call budget. Its missed-turn metric can report success without an action, and its wiring test can pass with production adapters disconnected. These defects must be corrected before a live session can provide a trustworthy AP1 acceptance result.

Author: ChatGPT, Engineering Auditor. Recipient: Fable. Date: 2026-11-11.

## Target and authority

| Item | Reviewed value |
|---|---|
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `fable/ai-player-ap1` |
| Frozen target | `583fe35390e4701eea50f331ae2bc10013f150c9` |
| Intended base | `40788e78d4159777a47e0b317fe13d83fa1819b3` |
| Separate ruling evidence | `fable/ai-player-rulings` at `3dcbcdfaab2ec56e35fccec982f41ec8b52977c4` |
| Main observed during review | `e6c57f288f91ef0e2cda1b0751d69df0769bda5b` |
| Review branch | `chatgpt/review-ai-player-ap1`, based on the frozen target |

The contract is `state/prompt_ai_player_overhaul.md` section 2, AP1 steps 1-7, AP7 step 1, and section 4; the architecture is `docs/design/AI_PLAYER_OVERHAUL.md` section 4. Review method: `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md` sections 7-8, `docs/agents/ENGINEERING_AUDITOR.md`, and `docs/workflows/FABLE_REVIEW.md`. The claims checked are in `docs/reviews/AI_PLAYER_AP1_HANDOFF.md`.

All file/line references below refer to the frozen target, not a subsequent correction. Reproductions used its code, logged fixtures, temporary directories, fake clocks and in-process fault injection. No live request was made.

## Reliability and efficiency assessment

The director's concern is justified by specific failure paths, but a measured runtime efficiency regression has not been established: neither a live Haiku baseline nor a comparable AP1 live measurement exists.

What the offline evidence establishes:

- The budget can schedule 32 calls within one rolling minute, despite the 30-call contract.
- The recovery path can repeatedly request reads without producing an action, even after its deadline. The resulting extra requests are real overhead without progress.
- Opponent polling can sleep 41.7 seconds in the reproduced sequence. That delay is additional to the nominal 3-6 second backoff and occurs before the next observation can start our turn clock.
- A zero missed-turn count is currently unreliable. It cannot be used as evidence that added complexity or token expenditure bought reliability.
- Production wiring is not established by the green wiring suite.

What remains unmeasured: relay tokens per actual turn/hour, end-to-end action latency, actual connector calls, and comparative live results. The 2,657 added Python lines and retained legacy tools are a complexity baseline, not by themselves proof of worse runtime efficiency. AP4 consolidation and AP6 reduction remain later phases.

The recommended response is a focused correctness pass with adversarial tests and measurable acceptance criteria, rather than another architectural layer.

## Findings

### 1 High — The shared call budget can exceed 30

**Location:** `player/budget.py:56`, `player/budget.py:81`.

**Reproduction:** Using `player.tests.support.Rig`, schedule 20 `calls.user()` steps through `Budget.pace(..., "world")`; advance the fake clock 10 seconds; call `start_fight(rig)`; supply our next-round read 10 seconds later. Each turn uses the ordinary two-action stub line. `budget.used()` is 27 after the first turn and 32 after the second, with `hold == 0`. All scheduled calls fit within one minute. Supplying an opponent-turn read two seconds later produces a 41.7-second hold.

**Refutation attempted:** The world lane independently respects its 20-call allowance. `poll_hold` reserves eight calls during opponent polling. Neither constrains consecutive urgent turns, the opening reads, or recovery: `pace` enforces the shared limit only for the world lane. The existing long-opponent-turn test does not cover this sequence.

**Consequence:** Connector refusals can occur on the very calls the reservation is supposed to protect. Long blind waits also weaken turn detection. This violates AP1 step 3; the approved exception for scheduling opponent polls does not waive the shared cap.

**Correction and acceptance:** Reconcile admission, reservations and polling deadlines across complete sequences. Keep urgent actions/recovery protected by shedding or deferring optional work beforehand. Test consecutive turns, world-to-battle transitions, recovery and refusals against a rolling-window ledger; record detection delay separately from planning time. If the requirements cannot be jointly met in a scenario, expose that constraint rather than silently exceeding the cap.

### 2 High — Rejected or undelivered plans suppress deadline recovery

**Location:** `player/activities/battle.py:98`, `:111`, `:141`; `player/brain.py:185`.

**Reproduction:** Start the logged fixture. Return `{"notification":"Action not valid anymore"}` for both issued actions, followed by a rate-limited battle read. Continue returning rate-limited reads at T+12, T+15, T+20 and T+60. Every subsequent batch contains reads only; no replacement action is emitted. Generic action errors followed by unreadable reads produce the same result.

A second reproduction injects a one-time exception in `_compose`, after battle planning has set `fired_at` but before a batch is returned. `answer` sends only the next-tick instruction. A subsequent failed read still produces no deadline fallback because the resident state says the unsent plan fired.

**Refutation attempted:** A fresh battle read after the game refusal does produce another plan. An action-level 429 clears `fired_at` and also recovers. The defect is the combination of other refusals or undelivered plans with missing usable reads. Existing tests manually clear state or provide the fresh read that avoids it.

**Consequence:** A turn can pass without further action despite the T+12/T+15/T+20 safeguards. Returning a batch after a crash is not sufficient recovery.

**Correction and acceptance:** Distinguish planned, issued, confirmed and uncertain actions. Do not preserve an unsent plan as fired after a failed tick. Reconcile ambiguous delivery by battle version, without blindly duplicating actions. Add combined refusal/read-failure and post-plan crash tests that check an action path and its timing, not merely the presence of a response.

### 3 High — The timeout fallback repeats a known-invalid action

**Location:** `player/activities/battle.py:339`.

**Reproduction:** Make planning return no line; the brain emits `defensiveStance`. Return `Action not valid anymore` for that action and advance to T+15 with the unchanged battle read. The output again contains `defensiveStance`, although it is in `state["banned"]`. Expired-budget replanning continues down the same fallback.

**Refutation attempted:** The ban is correctly recorded and passed to the planner. The unconditional emergency fallback ignores it. The planner timeout test establishes that the planner returns, not that the fallback can be accepted by the game.

**Consequence:** The recovery loop can spend the remaining turn repeatedly attempting an action already known to be invalid. It also does not implement the brief's best-line-so-far behavior.

**Correction and acceptance:** Retain a legal best-so-far or validated emergency line and honor refusals in every fallback. Test an expired planner budget after rejection of the first fallback, without relying on a successful fresh planner run.

### 4 High — Results are not bound to the issuing relay and batch

**Location:** `player/relay.py:63`, `:102`; `player/brain.py:246`.

**Reproduction:** Write a synthetic transcript with a `profile.getUser` tool use at time 90 and its result at time 110. `read_results(path, 100)` accepts it, although the call predates the batch cutoff. A battle profile from that result opens the old battle.

Separately, provide a Claude transcript directory containing only an unrelated transcript with no `brain next` call. `find_transcript` returns that file anyway. Running `next_batch` in-process consumes its profile, opens battle `FOREIGN`, emits reads for it, and does not emit `ECHO`.

**Refutation attempted:** Transcript tool-result IDs are matched to tool-use IDs, and result timestamps are checked. Neither binds the result to the expected batch. `client.json` records expected calls, but collection does not enforce them. A readable unrelated file is treated as a readable relay transcript.

**Consequence:** Late or unrelated responses can change battle state and subsequent actions. It also prevents the documented fallback from activating when ownership is unknown.

**Correction and acceptance:** Establish relay identity and explicit batch/call correlation; reject stale or unrelated results and fall back when ownership cannot be established. Test delayed results, replacement relays, unrelated newest transcripts and duplicate deliveries.

### 5 Medium — Unknown spending is treated as zero

**Location:** `player/gates.py:154`; `player/calls.py:116` (`ramen`).

**Reproduction:** Set today's recorded spending to exactly `DAILY_CAP` and supply an awake profile with low chakra. The next batch contains `village.buyFood` with no pending decision. `K.ramen()` supplies `ryo=None`; the gate converts it to zero. The same call with a positive cost correctly returns `ask`. With a zero configured daily allowance, the unknown-cost call still passes.

**Refutation attempted:** The gate correctly blocks spending already above the cap and correctly checks supplied positive costs. The live builder omits the cost, so these successful tests do not cover the boundary.

**Consequence:** A purchase can exceed the director's allowance or reserve without prior approval. AP2's future spend-cap decisions do not remove AP1's obligation to enforce the caps it currently uses.

**Correction and acceptance:** Obtain a cost or conservative bound before screening. Treat an unknown price as unknown, not free. Test both the daily allowance and reserve immediately at their boundaries.

### 6 Medium — Midnight-crossing temporary holds expire early

**Location:** `player/gates.py:61`.

**Reproduction:** In a temporary do-not-attack file, add `- 2026-11-11 23:50-00:20 UTC: Luka and 4qua. Leave them be.` Evaluate at `2026-11-11T23:55:00+00:00`. The parsed protected set is empty, and `Gates.check` permits attacks on both names.

**Refutation attempted:** Ordinary same-day holds work. The accepted syntax has start and end times, but the start is discarded and the end always uses the starting date. If crossing midnight is unsupported, the line should be rejected conservatively instead of interpreted as expired.

**Correction and acceptance:** Handle the rollover or require an explicit end date and fail closed on ambiguous input. Add tests before, during and after a midnight boundary.

### 7 Medium — Missed-turn accounting can hide missed turns

**Location:** `player/activities/battle.py:362`, `:371`; `player/budget.py:89`.

**Reproduction:** Start the fixture, remove current-round entries belonging to us, and deliver no successful action result. Advance 60 seconds to an opponent next-round read with a higher version. The logged row says `acted: true`; `turns_missed` remains zero. In a second case, jump directly to our next round: the old turn is replaced without any `turns.jsonl` row, again leaving zero misses.

**Refutation attempted:** The implementation checks our log entries, but also treats a fired timestamp plus any later version as proof of our action. `_close` even supplies a synthetic version increment. `turn_open` does not close an unrecorded previous round before replacing it.

**Consequence:** The headline zero-missed-turn acceptance metric can give a false success signal. It cannot reliably gate the live trial.

**Correction and acceptance:** Close each observed turn, including skipped observations and fight termination. Distinguish confirmed action, confirmed miss and unresolved evidence. Test empty/incomplete logs, unrelated version advancement, direct round jumps and relay loss.

### 8 Medium — Wiring tests can pass with production adapters disconnected

**Location:** `player/tests/test_wiring.py:23`, `:75`; `player/tests/support.py` (`StubCombat`).

**Reproduction:** Patch `Combat.plan_turn` to return `(None, "unwired")` and `Combat.save_kit` to return `False`, then run the complete `player.tests.test_wiring` suite. All five tests pass. `Rig` substitutes `StubCombat` overrides, which supply the evidence being asserted.

**Refutation attempted:** Activity module discovery does detect an unregistered activity. The model/feed check compares a manually written evidence list to the manually maintained registry; it does not inventory all production dependencies or exercise these production adapters. Background command strings prove scheduling, not that resulting data is consumed. The design's specifically named `meal_factor.py`, `validate.py --write-scales` and `engine_fit.py --write` feeds also lack independent inventory coverage here.

**Correction and acceptance:** Keep stubs for unit tests, but exercise the production adapter boundary with controlled subprocess/file dependencies. Test that removing a real producer or consumer fails wiring. Inventory model/feed ownership independently of the registry being checked; make later-phase deferrals explicit rather than silently omitting dependencies.

### 9 Medium — Console events report purchases before approval or success

**Location:** `player/activities/recovery.py:55`, `:57`, `:68`.

**Reproduction:** Put recorded spending above the daily cap and request ramen recovery. The gates drop the purchase and raise a pending decision; the output contains no `village.buyFood`. Nevertheless, `events.jsonl` contains `ramen bought`. Potion events are likewise emitted while constructing a plan, before screening and game confirmation.

**Refutation attempted:** The gate behaves correctly in this case. The event remains an affirmative purchase record even though the action was never sent; it is not labelled an intention.

**Consequence:** AP7's history can misstate resource use and successful recovery, undermining the director's ability to manage the player.

**Correction and acceptance:** Separate requested/issued/confirmed outcomes. Emit purchase/use events only on appropriate confirmation, and test gate refusal, transport error and game refusal.

### 10 Medium — The opening archive loses information

**Location:** `player/activities/battle.py:254`, `:284`.

**Reproduction:** Start the logged fixture and inspect the first `B1.full.jsonl.gz` row. Its `seat` is null although the resulting world state identifies seat 2. Poll the same round/side again: the archive still contains only the original null-seat row. Supplying a ground record with an `id` also demonstrates that the archive holds its compacted form, without that field.

**Refutation attempted:** The full users-effect list is preserved, including fields the planner ignores. The seat is determined after archiving, and duplicate suppression prevents a later poll from correcting it. Ground is taken from the compact world representation, not the original supplied record.

**Consequence:** The archive does not fully support the handoff's claim that each round's full state, ground and seat are retained so they need not be captured again.

**Correction and acceptance:** Determine the seat before finalizing the archive and retain available raw state separately from planner projections. Clearly distinguish unavailable fields from empty fields. Test the first archived row, not only later rounds.

### 11 Medium — The ECHO instruction lacks safe result encoding

**Location:** `player/RELAY.md:25`.

**Reproduction:** Substitute JSON containing `"You don't have that item"` into the prescribed `python3 -m player.brain put N 'RESULT'` command. Literal substitution fails shell parsing with `No closing quotation`.

**Refutation attempted:** The simple JSON `put` test works. An experienced relay could supply correct shell escaping, but the mechanical contract neither specifies that transformation nor tests it. This is a contract defect; no claim is made about how a live model would repair the command.

**Correction and acceptance:** Define safe stdin/file/encoded transport that does not interpolate raw result text into shell syntax. Test apostrophes, quotes and multiline results, and state the necessary result-dependent sequencing in the relay prompt.

## AP1 claim assessment

| Brief requirement | Assessment |
|---|---|
| 1 Resident brain, persisted state, scheduler, arbiter, registry | Present; failed-tick state and delivery reconciliation need correction (2). |
| 2 Small-model relay, selects, waits, rotation, watchdog, token log | Normal path present; identity/correlation and fallback contract need correction (4, 11). Prompt is 262 words. |
| 3 Budget and turn deadlines | Not met in the reproduced cases (1, 2, 3, 7). |
| 4 Gates with rule coverage | Central screening works, but spending and temporary holds are incomplete (5, 6). Twenty-six passing gate tests are not proof of all section 2 invariants. |
| 5 Core activity port | Ordinary battle parity and recovery composition verified; exceptional action paths remain defective (2, 3). |
| 6 Wiring | Existing suite is green but can miss production disconnection (8). |
| 7 Chaos | Named scenarios exist and pass, but combinations and post-plan failure boundaries remain uncovered (2, 3, 7). |
| AP7 step 1 data from AP1 | Files exist; outcome events can be false (9), and the missed-turn metric is unreliable (7). |
| Updated full-state archive requirement | Full users effects preserved; opening seat and raw ground preservation need correction (10). |

`SameAsThePilot` really compares endpoints, inputs, selects and waits for its three ordinary states: our turn with the real planner, the opponent's turn, and an AI turn. It is useful evidence, but not parity coverage for refusal, timeout, closing-battle or restart behavior.

## Handoff deviations

| Deviation | Review disposition |
|---|---|
| 1 Context-growth rotation | Settled by RUL-2026-11-11-151. Code matches: 60,000 growth or 150,000 absolute; never during battle. Do not reopen. |
| 2 Scheduled opponent polling | Legitimate distinction from urgent action pacing, but the implementation does not establish the combined cap/deadline guarantees (1). |
| 3 Ordered calls in one message | Normal parity test preserves order and waits. Actual relay execution remains unverified; ECHO additionally needs result-dependent sequencing (11). |
| 4 T+12 fallback | Works on its tested path; fails after certain refusals or an unsent plan marked fired (2). |
| 5 Four supporting activities | Consistent with the pilot's core loop; no independent scope defect found. |
| 6 Harvest enabled | Settled by RUL-2026-11-11-151. Runtime behavior matches; the study-only gate remains. Do not reopen. |
| 7 Initial pilot handover | Potion id and skip/loss memory handover tested; the wider AP2 work remains explicitly deferred. |
| 8 Time-based result matching | Unsafe as implemented (4). |
| 9 Log-derived turning point | A disclosed log heuristic; do not describe it as an engine-based causal postmortem. No separate blocker established. |
| 10 Additional finding event | Reasonable; event truthfulness still needs correction (9). |
| 11 Default goal-weight numbers | Disclosed defaults; multiple-goal arbitration is tested synthetically, not demonstrated as an AP1 live improvement. |
| 12 Unknown empty items | Disclosed lack of inventory knowledge; its recovery path must not deadlock or repeat a known-invalid fallback (2, 3). |

## Verification and size

All commands below were run at the frozen target. Tests were local and made no game requests.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 138 tests, OK |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK |
| `python3 scripts/player_allowlist.py check` | Exit 0; 93 endpoints; never-list clean |
| `python3 scripts/player_allowlist.py report --check` | Exit 0; report current |
| `python3 scripts/player_size.py` | Figures below match handoff |
| From `state/player/dauntless/tools`: `python3 tests/test_planner2.py` | Exit 0; 4,000/4,000 parity cases |
| Same directory: `python3 tests/test_pilot.py` | Exit 0 |
| Same directory: `python3 tests/test_integration.py` | Exit 0 |
| Same directory: `python3 tests/test_nearkill.py` | Exit 0 |

The first catalog-test run lacked the committed `harvests/inbox/tnr_results_1794368544997.json` in the sparse checkout. Including it and rerunning produced 46 OK. That setup failure is not an implementation finding. Legacy test outputs were moved outside the checkout.

| Measure | Verified |
|---|---|
| Player Python code excluding tests | 2,657 lines in 19 files |
| Tests | 1,914 lines |
| Largest file | `activities/battle.py`, 389 lines |
| Largest function | `combat.py:plan_turn`, 38 lines |
| Configuration constants | 47 |
| Control settings | 9, plus the carried planner-choice switch |
| Functions above 12 branches | 10, listed below |

Branch counts match the handoff: `battle._absorb` 17, `battle._tick` 16, `battle.plan` 16, `battle._my_turn` 13, `combat.plan_turn` 16, `calls.ground_cols` 15, `gates.do_not_attack` 15, `brain._compose` 14, `relay.read_results` 14, and `relay.find_transcript` 13. These are disclosed AP6 debt, not independent AP1 budget violations.

Primary, recovery and rider calls pass through `_compose` gate screening. Tested controls cannot add forbidden endpoints or remove permanent do-not-attack names. The one-brain lock, normal in-process fallback, simple `put` path, rotation behavior and ordinary same-batch potion composition pass their tests. The pilot's tools have no changes against the intended base.

## Requested Fable response

Review this report before broadening AP1 or starting AP2. For each numbered finding, return **confirmed**, **refuted with frozen-SHA evidence**, or **needs clarification**, together with the smallest proposed correction and a regression test that would fail on this target. Existing green test counts are not a refutation of an independent failing case.

Prioritize the coupled runtime failures first: budget/admission, action delivery state, fallback legality, result ownership and trustworthy missed-turn accounting. Then address the remaining gate, wiring, archive, console and relay-contract defects. Avoid expanding the architecture unless a reproduced failure requires it.

For a later correction handoff, provide an exact frozen SHA, the new adversarial tests, the original required checks, updated size figures and a finding-by-finding disposition. Keep the ten AP6 complexity items visible; do not turn this pass into AP4/AP6 consolidation.

Once the offline defects are closed, the director-started live gate should measure actual calls per rolling minute, observation-to-action latency, unresolved deliveries, confirmed missed turns, and relay tokens per batch/turn/hour. Compare equivalent workloads before claiming an efficiency improvement. Uncertain turn outcomes must be visible rather than counted as successful turns. The live trial remains the director's action and is not authorized by this report.

## Repository and live boundary

During the independent audit, no tracked file changed and no `fable/*` branch was modified. This subsequent, user-requested report adds only this Markdown file on the separate `chatgpt/review-ai-player-ap1` branch. It contains no implementation fixes. Zero live-game requests were made throughout the audit and report preparation. No live relay, browser or gameplay session was run.
