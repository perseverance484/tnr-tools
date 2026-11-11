# AI player overhaul: implementation brief

Status: DRAFT, awaiting the director's approval. Once approved, this file is the build contract (CLAUDE.md §11).
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
2. **Outbox and inbox.** Write the protocol and a minimal relay prompt, `player/RELAY.md`. The relay executes
   batches exactly and keeps no state. Add a watchdog for a stale outbox.
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

**Gate:** chaos and wiring tests are green, then one director-started live PvP session with zero missed turns.

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

## 5. Open decisions

From design §9. Ask before the phase that needs each one:

1. Goal weights (AP1).
2. Equipment-swap scope (AP2).
3. Spend caps (AP2).
4. PvE auto-combat scope (AP3).
5. Session windows and call share (AP1).
6. Which further modes first (AP5).
