# AI player overhaul: implementation brief

Status: APPROVED by the director 2026-11-11 (RUL-2026-11-11-148). This file is the build contract (CLAUDE.md §11).
Design: `docs/design/AI_PLAYER_OVERHAUL.md`. Scope ruling: RUL-2026-11-11-148.

Lane: A (code, tools, tests). Work on `fable/ai-player-*` branches and hand over each phase at an exact SHA for
independent review (`docs/workflows/IMPLEMENTATION_HANDOFF.md`).

Live play: this work produces the player, and Duet runs it. Live connector calls made while building are play under
RUL-2026-11-11-147 and follow the same rules as the player. Prefer fixtures, captures, logged fights and the offline
engine harness. A phase that needs live verification says so, and the director starts that session.

---

## 0. Read first

1. `CLAUDE.md`, `docs/00_INDEX.md`, `docs/RULINGS.md` (RUL-2026-11-09-139, -145, -146, RUL-2026-11-11-147, -148).
2. `state/prompt_playing_tnr.md` in full. Its §1 game rules, §3 never-list and §5 conduct rules are binding here.
3. `docs/design/AI_PLAYER_OVERHAUL.md` in full.
4. The current code on both branches:
   - `fable/pvp-engine-harness`: the engine harness and planner2;
   - `fable/pilot-planner-fixes`: Duet's live pilot.

   Read `state/player/dauntless/tools/` and run its tests (`tests/test_planner2.py`, `test_pilot.py`,
   `test_integration.py`, `test_nearkill.py`) before changing anything.
5. `state/player/dauntless/`: do_not_attack.md, pvp_playbook.md, pvp_rotations.md, jutsu_training.md, ryo_plan.md.
6. The skill `tnr-pvp-combat` (section 0 hard rules, 0b engine rules).

## 1. Goal

One fully automated player for the director's account. It trains, fights PvP, runs missions, errands and dailies,
hunts, farms, restocks, repairs, swaps equipment, recovers and sleeps. It decides from the exact live state, never
loses a turn, learns from every real fight, and stays inside the game rules and the director's limits.

## 2. Non-negotiables (enforced in code, with tests)

- **Official TNR connector only.** No browser play. No staff powers or staff knowledge in play (rules §6.3, §7.4).
- **Never:**
  - payments or purchases (`paypal`, `stripe`, `purchases`, `merch`);
  - `accountDeletion`;
  - other players' accounts or data beyond normal play;
  - moderation or reports;
  - deletes without a per-record yes;
  - chat, messages or posts to players;
  - Flee;
  - attacking anyone on `do_not_attack.md`;
  - sniping AngelSaber.
- **Ask first** (raise a pending decision and continue with something else):
  - premium currency (reputation);
  - leaving the clan;
  - selling rare items;
  - marriage;
  - any ryo spend above the caps.
- **No credentials.** The brain never sees connector credentials. Agents carry calls; the brain only describes them.
- **Never the director's real name**, in anything.
- **Bugs and exploits** found in play are reported and avoided, never used.

## 3. Phases

Each phase ends with a handoff at an exact SHA, its gates green, and a short findings note. Do not start a phase
before the previous one is accepted, unless the director says so.

### AP0: inventory and one base

1. **Merge into one base.** Merge `fable/pvp-engine-harness` and `fable/pilot-planner-fixes` into
   `fable/ai-player-base`. Resolve `pilot.py` by keeping Duet's battle-loop fixes (every poll a full read; plan from
   the last good read on a refusal; unpaced battle batches) and adding the harness branch's opponent-kit read before
   an attack and its kit-read retry. All existing tests pass.
2. **Allowlist.** Pull the MCP router surface (`listGameRouters`, `listRouterEndpoints`, `getEndpointSchema`), write
   `data/player_allowlist.json` (endpoint, read or action, prerequisites, cooldowns, which activity uses it), and run
   the never-list check against it. The director approves the list.
3. **Map the code.** Map every current file to its future module (design §4) in
   `docs/design/AI_PLAYER_OVERHAUL.md` §2: keep, port or retire.

**Gate:** the allowlist is approved, and the base branch is green.

### AP1: brain and hands

1. **Brain.** `player/brain.py`: a resident process with the world model (`player/world.py`, persisted after every
   result), the scheduler, the arbiter (design §4.4) and the registry (`player/registry.py`).
2. **Outbox and inbox, for a Haiku relay** (design §4.7; director: "design it for Haiku and save on tokens"):
   - **The prompt.** `player/RELAY.md`, under 300 words. The loop is `brain next`, then the calls exactly as given
     (parallel, in one message), then `brain next` again. No text between calls and no decisions.
   - **Trimmed responses.** Every call has a minimal `select`. Lists are read as columns. Static data is cached in
     the brain. Before anything relies on field selects over arrays, verify they stay aligned when a field is
     missing.
   - **Fewer batches.** Back off polling during his turn with brain-side sleeps.
   - **Rotation.** Relays restart by context size (default 60k tokens), not batch count, and the brain keeps all
     state.
   - **Watchdog.** Alert on a stale outbox.
   - **Token log.** Log relay tokens per batch, per fight turn and per hour.
3. **Budget and battle lane.** `player/budget.py`: three lanes (battle, recovery, world) under 30 calls a minute
   shared, with the battle and recovery lanes never paced. The battle turn deadline: fire by T+20 s; fall back to
   the last good read at T+12 s and to the best line so far at T+15 s. Space actions 1.2 s apart. Log every turn's
   timing.
4. **Gates.** `player/gates.py` covers §2, with a test per rule.
5. **Port the core activities.** Port PvP hunt, battle and recovery from `pilot.py` as the first activities. The Full
   Potion goes in the same batch as the fight's end.
6. **Wiring test.** It fails if any module under `player/activities/` or any model or data feed is not registered and
   exercised.
7. **Chaos tests.** Cover refusals, "Too Many Requests", relay restarts mid-battle, a battle starting mid-errand,
   brain restarts, and planner timeouts.

**Gate:** chaos and wiring tests are green, then one director-started live PvP session on a Haiku relay with zero
missed turns, with its token figures recorded as the baseline for the targets.

### AP2: upkeep

Add the activities `training` (jutsu queue, energy in the village, skill tree and sensei when available), `restock`,
`repair` (near-broken only, 25%), `equipment` (loadouts per activity, weapon and thrown swaps, owned upgrades),
`bank` and `session` (start: lock; end: train intelligence, sleep at 177, PvP1 loadouts, release the lock).

**Gate:** 24 h live with the training queue never idle and no ask-first breach.

### AP3: progression

Add the activities `missions` (villageMission, quests), `errands` (Duet's Hyorin route first), `dailies`, `hunting`,
`farming`, and PvE combat (auto-combat where the game offers it, otherwise planner2 in PvE mode). Each activity gets
a playbook page (`state/prompt_playing_tnr.md` §4.4) before it goes live.

**Gate:** the daily routine completes unattended for 3 days.

### AP4: combat consolidation

**0. The move atlas comes first** (director, 2026-11-11: "model every known pvp jutsu that can be used against us
and also our own jutsu … we know exactly which clocks and weights move on the ttk when every jutsu is cast").

- **What:** `player/atlas.json`, one card for every action a player can use against us or that we can use:
  - normal, bloodline and special jutsu;
  - weapons, with learned imbues;
  - combat consumables;
  - the basics.

  That's about 1,600 of the catalog's 2,985 records; AI-only and pet records are excluded.
- **Each card holds:**
  - AP cost, cooldown, shared-cooldown locks, range, target, elements;
  - each effect as an exact state change: which planner arrays and rounds it touches, by how much, whether it acts
    this round or next, and what Clear, Cleanse, seals and prevents do to it;
  - its damage on a fresh board, measured in the engine at the standard assumption (capped stats, full Kaeruun +
    Subaku's mask, level 25 jutsu unless known), with how each stat and the level scale it.
- **Generated, not written by hand.** A generator compiles the cards from the catalog and the engine. Cards are
  never edited by hand.
- **Refreshed:** when the catalog changes, the atlas is regenerated and diffed, and a changed card is a finding.
- **The state machine applies cards.** When the live state shows a cast (his or mine), the brain applies that card's
  exact changes to the round arrays. The damage curves, tool windows and race update from it, so every clock and
  weight that moves on the time-to-kill is the card's, not an estimate.
- **Per fight:** `fight_bases.py` rescales the damage on the cards in both kits to the actual matchup.
- **Replaces** the hand-written kit specs (`shotplan.MINE`, `clock.compile_record`, the generic kit), which AP6 then
  deletes.
- **Clean inputs for opponent models.** Every fight's archive stores his turns as atlas card ids, with the exact
  live state of each round (HP, the live arrays, his ready cards per his clock, seat).
  - **Purpose:** his behaviour models train on exactly what he could do and what he faced, not on log text.
  - **Prediction:** stays weak until the data grows (director, 2026-11-11: "you won't be able to guess correctly
    without more data … but this way the inputs are clean").
  - **Re-checks:** held-out accuracy (exact turn, type of turn, his damage in the round) is re-measured monthly. A
    prediction term weighs in the planner only while it beats the base rate on held-out fights. Until then the
    planner plans on windows and the hedge.
- **Gate:**
  - every action in every logged fight resolves to a card;
  - one card applied alone matches the engine within 1% on damage and on every effect's value and timing, over a
    sample of at least 200 cards that includes every effect type;
  - no hand-written spec is still used in a live fight.

1. **One planner.** planner2 only. turn.py, shotplan.py and value_model.py become helpers or are deleted.
2. **Live state everywhere.** `from_live` is the only state path in a live fight; the text rebuild remains for old
   logs only and is labelled as reconstructed.
3. **Windows.** Turn the damage curves and tool windows on if `tune_real` passes (design §6).
4. **Learning on the brain.** Post-mortems, the solution library and opponent dossiers run on the brain, between
   fights.
5. **Accuracy.** Close the remaining engine gaps until `engine_check` (live-shaped) is ≥ 95% of bundles within 1%.

**Gate:** design §6.

### AP5: further modes

Ranked, tournament, war, bounty and shrine, each with its playbook, gates and tests; then the weekly report and the
findings pipeline.

### AP6: the simplest version that meets every standard

Director, 2026-11-11: "construct the most simplistic version of the ai player code that still fulfills all
standards … reduce overengineering and needless complexity". AP0–AP5 find out what the player needs. AP6 keeps
only that, and proves nothing was lost.

**1. Freeze the standard first (the contract).** Before deleting anything, build `player/contract/`, which records
what "fulfils all standards" means as runnable checks:
- **Safety:** every gate test from §2. These must give identical outcomes, with no tolerance.
- **Robustness:** every chaos test from AP1. Identical outcomes.
- **Decisions:** a corpus of at least 300 recorded situations:
  - battle turns from `fights/live_states/`;
  - world states from the brain's log: upkeep, missions, errands, travel, recovery.

  For each one, store the current decision and its score (engine exchange against his actual next turn for battle
  turns; the arbiter's choice and its outcome for world states).
- **Combat quality:** `engine_check` (live-shaped, ≥ 95% within 1%) and `tune_real` on the last 20 real fights,
  with a bootstrap confidence interval so "no worse" means outside noise.
- **Live KPIs** from AP5's weekly report, as the baseline:
  - missed turns (0);
  - training idle minutes;
  - dailies completed;
  - PvP win rate;
  - relay tokens per hour and per fight.

**2. Ablate, then delete.** For every component (module, model, feature, flag, fallback, cache, config knob):
1. Remove it.
2. Run the contract.
3. Keep it only if a safety or robustness check fails, a decision check gets worse outside noise, or a KPI would
   suffer (say which).

Record the verdict for each component in `docs/design/AI_PLAYER_OVERHAUL.md` §10 (component, the check that keeps
it, or "deleted"). Expect large cuts: features added on a hunch, models that never moved a decision, duplicate state
paths, simulator-only code, flags left off.

**3. Rewrite what survives, as plainly as possible.**
- **Plain code:** plain functions and data tables before classes and frameworks. One battle state machine with
  explicit states. Activities as rows in a table (preconditions, value, call template) wherever their logic allows,
  and code only where it doesn't.
- **One way to do each thing:** one state path (live), one planner, one call budget, one config file. Delete every
  alternative.
- **No dead flags:** a setting stays only if a test shows it changes a decision the live player makes. Everything
  else becomes a constant or is deleted. Nothing is left switched off.
- **No speculative generality:** no plug-in hooks, abstract bases or options that nothing uses today.

**4. Complexity budget, enforced by a CI check (`player/contract/budget.py`):**

| Measure | Budget |
|---|---|
| Total player code, excluding tests and the engine harness | ≤ 50% of the AP5 total, and an absolute cap set from the AP5 measurement |
| Largest file | ≤ 400 lines |
| Largest function | ≤ 60 lines |
| Branching (cyclomatic complexity) per function | ≤ 12 |
| Config knobs | ≤ 15, each with a test proving it matters |
| Third-party dependencies | none beyond the standard library, Pillow and the engine harness |
| Imports of retired modules (turn.py, shotplan.py, value_model.py, fightsim.py, ...) | 0 |

A budget is changed only by the director, in a ruling.

**5. Readability check.**
- `player/README.md` explains the whole player in at most 2 pages: the loop, the battle state machine, the activity
  table, the planner, the gates.
- An independent reviewer (ChatGPT, under `docs/workflows/FABLE_REVIEW.md`) must be able to trace one battle turn
  and one errand from read to call using only that README and the code, and reports anything they could not follow
  as a finding.

**6. Swap-over.**
- **Parallel run:** the simplified player runs live beside the AP5 baseline's numbers for 48 h, on the same Haiku
  relay design.
- **Swap-over gate:** every contract check passes, every budget is met, and no live KPI is worse than the baseline
  outside noise. Then the old code is deleted from the branch, not just left unused.

**Gate:** all of step 6, the component verdict table complete, and the director's sign-off.

## 4. Engineering rules

- **Narrow modules.** One activity per file, and no activity reaching into another's state. Shared state goes
  through the world model.
- **Exact state first.** Any reconstruction is labelled. Never hand-tune a number the engine can measure.
- **Combat changes are scored on real fights** (`tune_real.py`, last 20 fights): no change ships that lowers the
  mean exchange or the best-of-set rate. The simulator is a smoke test only.
- **Tests are socket-free and use fixtures** from logged fights (`fights/`, `fights/live_states/`).
- **Keep the director informed through Duet:** fight start, fight end with turning point, pending decisions, stalls,
  daily summary.
- **Handoffs** list exact SHAs, gates run, live checks not performed, and open decisions (CLAUDE.md §11).
- **Keep complexity visible from AP1 on.** Each handoff reports the player's line count, its largest file and
  function, its config knobs and anything added that is switched off. A feature that ships switched off has a named
  date to be switched on or deleted. AP6 cuts what is left; it should not have to undo habits.

## 5. Open decisions

From design §9. Ask before the phase that needs each one:

1. Goal weights (AP1).
2. Equipment-swap scope (AP2).
3. Spend caps (AP2).
4. PvE auto-combat scope (AP3).
5. Session windows and call share (AP1).
6. Which further modes first (AP5).
7. The AP6 absolute size cap, set from the AP5 measurement (AP6).
