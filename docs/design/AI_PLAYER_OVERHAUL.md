# AI player overhaul: design

Status: APPROVED by the director 2026-11-11. The build contract is
`state/prompt_ai_player_overhaul.md` (CLAUDE.md §11); this document is the design it implements.
Scope ruling: RUL-2026-11-11-148.

## 1. What the director asked for

> "An overhaul of the entire system to turn it into a fully automated AI player that trains, PvPs, does missions,
> errands, dailies, hunts, restocks items, repairs gear, swaps equipment as needed, farms content and so on."
> (director, 2026-11-11)

Earlier the same day, in the order he raised them:
- Every system has to be wired into every other. "Every time we add a new system I discover you weren't using it
  because it wasnt tied in."
- Plan on the exact live state, not a reconstruction. "Read the exact live state and feed it into the vector state
  engine … this is how you avoid errors."
- Plan for windows, not exact combos. "Guessing exact jutsu combos is futile, you want to be prepared for windows."
- Learn from real fights. "Try against real enemies and actively scan logs to understand what caused a loss." A
  library of responses grows "as we see it and successfully respond to it".
- Assume every opponent is capped, in full Kaeruun plus Subaku's mask, until his damage says otherwise.
- Never lose a turn. Never wait to heal after a fight; a Full Potion goes out at once.

## 2. Where it stands (inventory, 2026-11-11)

Code lives under `state/player/dauntless/tools/` on two branches:
- `fable/pvp-engine-harness`: the engine harness and planner2 work.
- `fable/pilot-planner-fixes` (Duet, the live pilot): its fixes for missed turns, afterburn, seat-aware timing and
  errands.

| Piece | What it does | State |
|---|---|---|
| `pilot.py` + `pilot_safe.py` | One "tick" script. It reads the last tool results, decides, and prints the next batch of connector calls. A relay agent copies each batch into the TNR connector. | Works. It has grown to ~1,500 lines mixing battle, world, upkeep and errands. Relays run out of context after ~200 batches and must be relaunched. |
| `planner2.py` | The PvP turn planner. Per-round state arrays (5 rounds), legal 100-AP bundles, his reply set from his cooldown clock plus habits, a hedge on his hardest hit, a two-exchange lookahead, damage curves (built, off). | Within 1% of the engine on 80% of positions when fed the exact live state. |
| `turn.py`, `shotplan.py`, `value_model.py` | The first planner and its text-log rebuild of state. | Fallback only, but planner2 still imports from them. |
| `engine_bridge.py`, harness `replay_sim.ts` | Runs the pinned game source offline: replay, eval, state, probe, scripted reply. | Solid; it is the ground truth for the numbers. |
| `fight_bases.py` | Both kits' damage for a matchup, from the engine (caps, gear, bloodlines, masteries, meals). | Live. |
| `opponents.py`, `opp_profile.py`, `opponent_kit.py` | Opponent models from all logs; bloodline profile; kits and weapon imbues. | His exact next bundle is unpredictable (~6–10% on fights the model hasn't seen); his windows are not. |
| `postmortem.py`, `solutions.py`, `tune_real.py` | Per-fight review against his actual next turn; a solution library; tuning against real opponents. | Live, young. |
| `fightsim.py`, `exam.py`, `validate.py`, `engine_check.py` | Simulated fights and accuracy checks. | The sim flatters us: its bots are weaker than real players. |
| `restock.py` | Items, repair, jutsu and energy training. | Works. Duet added a village trip for stat training. |
| Errands, dailies, missions, farming | Duet's Hyorin errands only. | Mostly missing. |

### What went wrong, and what the design must prevent

| Failure (2026-11-11) | Cause | Design answer |
|---|---|---|
| Jutsu training silently stopped; opponent models unused | New systems were added beside the loop, not into it | Activity registry + a wiring test that fails if any module is unregistered (§4.3, §8) |
| Missed turns (4qua R2, R4) | Director-window timer restarted per action; extra reads; pacing on the turn's read | Battle is a hard real-time lane with its own call budget and deadlines (§4.6) |
| Plans on wrong numbers | State rebuilt from log text | Exact live effect list every turn; engine bases per fight (§5.1) |
| Planning against a generic opponent | Kit read raced the first turn and was not retried | Opponent dossier is ready before the first action, and retried (§5.3) |
| Third-partied at 3,211 HP | Full Potion queued behind a read cycle | Post-fight recovery runs in the same batch as the fight's end (§4.6) |
| Relays forget, stall and need relaunching | The "brain" lives in a script re-run each tick; the relay is an LLM with a context limit | The brain becomes a resident process; relays become a thin, replaceable executor (§4.1) |
| Wins and losses mislabelled | Result inferred from status alone | Result from the fight log's own HP accounting (§5.4) |
| Sim said "better" when it wasn't | Bots are weaker than real players | Real-fight replay scoring is the gate; the sim is only a smoke test (§6) |

### File map (AP0, 2026-11-11)

Every tracked file under `state/player/dauntless/tools/` on the merged base `fable/ai-player-base` (53 files), and
where it goes. The import graph behind it was read from the code, not from the docstrings.

- **keep:** the file stays a module of its own. It moves under the player package and is listed in the registry
  (§4.3) as a model, a data feed or an evaluation.
- **port:** its logic moves into the new module named. The old file is deleted once the port's tests pass.
- **retire:** deleted. Where other modules still import names from it, those names move first.

**The loop**

| File | Lines | Verdict | Goes to (§4) | Phase | Notes |
|---|---|---|---|---|---|
| `pilot.py` | 1,017 | port | `brain.py`: `tick`, the state file, the transcript reader (it becomes the results inbox, §4.7). `world.py`: everything in `fights/live/pilot.json`. `budget.py`: `budget`. `gates.py`: `do_not_attack`, the refusal bans. `activities/battle.py`: `battle_tick`, `plan_turn`, `finish`, `log_says_lost`, director mode. `activities/pvp_hunt.py`: `world` in hunt and guard mode, `pick_target`, `note_attack`. `activities/recovery.py`: Full Potion, ramen, hospital. `activities/restock.py`, `repair.py`, `training.py`: `restock_tick` and the village training trip. `activities/session.py`: rest, sleep, wake. `activities/errands.py`: `errand_tick`. The `harvest_*` pair becomes the harvest feed. | AP1 (battle, hunt, recovery), AP2 (upkeep, session), AP3 (errands) | The design said ~1,500 lines; it is 1,017. Between them the pilot, `restock.py` and `harvest.py` can send 32 endpoints (`data/player_allowlist.json`, status `in_use`). |
| `pilot_safe.py` | 21 | retire | - | AP1 | A resident brain that reloads its world model replaces the "last good copy" fallback. `pilot_good.py` is its untracked output, written by `tests/test_pilot.py`. |
| `pilot_watch.py` | 20 | retire | the brain's status log and the outbox watchdog (§4.1) | AP1 | |
| `restock.py` | 243 | port | `activities/restock.py` (`plan`, the item table, auction caps), `activities/repair.py` (the 25% rule), `activities/training.py` (`training_plan`), `gates.py` (reserve, daily cap) | AP2 | It also writes `fights/live/equipped.json` (the thrown weapon the planners read) and swaps in the backup thrown weapon: both become world-model state for `activities/equipment.py`. |
| `harvest.py` | 110 | keep | data feed `harvest`, scheduled in the scouting class (§4.4) | AP1 | Reads other players' battle histories and logs. Its scope is a question for the director (handoff, open decisions). Writes `fights/observed/`, which is untracked. |
| `hunt_plan.py` | 88 | port | `activities/hunting.py` (the opening turn of a hunt) | AP3 | Run by hand today; nothing imports it. |
| `add_record.py` | 14 | port | the brain's static catalogue cache (§4.7) | AP1 | Adds a `jutsu.get` or `item.get` record to `harness/pvp_turn/kit/records.json`. |

**Combat: decision**

| File | Lines | Verdict | Goes to | Phase | Notes |
|---|---|---|---|---|---|
| `planner2.py` | 1,395 | keep | combat engine: the one planner (§5.2) | AP4 | It still imports 6 names from `cd_plan`, 5 from `clock`, 2 from `fightsim`, 4 from `shotplan`, 13 from `turn` and 11 from `value_model`. Those move in before the three old files go. |
| `turn.py` | 1,253 | retire, after a port | its still-used names go to planner2 or a combat helper; `load_input` stays as the text rebuild for old logs, labelled reconstructed (brief AP4.2) | AP4 | **Not a dead fallback.** In the repository `pilot.py` leads with `turn.py`; a runtime file that is not tracked (`fights/live/planner_choice`) can put planner2 first, with `turn.py` second. Duet's six planner commits of 2026-11-11 (near-kill margin, barriers, scoring, afterburn and mitigation-aware setup, seat-aware timing, hold Clear, kunai priced by fight closeness) changed 402 lines here and 32 in planner2. `tests/test_nearkill.py` tests `turn.py`. Before it goes, each of those rules is rebuilt in planner2 or shown by `tune_real` not to matter. |
| `shotplan.py` | 434 | retire, after a port | `MINE` (my kit card), `ground`, `off_ground`, `rebuild` go to a combat helper | AP4 | `tests/test_planner2.py` uses it as the parity reference; the engine takes that role. |
| `value_model.py` | 237 | retire, after a port | `calibrate_kit`, `generic_kit`, `load_cal`, `reserves`, `clear_risk_4` and the constants go to planner2 | AP4 | |
| `cd_plan.py` | 163 | port | the kit tables (`ACTIONS`, `LOADOUTS`, `MOVES`, `RANGE`, `LOCKS`) go to a combat helper; per-battle cooldown state goes to the world model's battle state | AP4 | 10 modules import it. Its command-line planner goes. |
| `clock.py` | 192 | keep | combat engine: his cooldown clock, the reply set and his windows (§5.2) | AP4 | |
| `solutions.py`, and its data `solutions.json` | 413 | keep | combat engine: the solution library (§5.2), merged after every fight on the brain (§5.4) | AP4 | |
| `battle_plan.py` | 203 | retire | - | AP1 | Nothing imports it; planner2's lookahead replaced it. |
| `policy.py`, `state_rules.py`, `enemy_model.py`, and their data: `rules_config.json`, `policy_weights.json`, `train_log.jsonl` | 488, 203, 203 | retire | - | AP4 | The first learned policy (2026-11-10). It is reached only through `turn.py` and `shotplan.py` (`policy.legal`, `enemy_model._predict`), so it goes with them. |
| `ingest.py`, `ids.py` | 100, 3 | retire, after a port | `IDS` and `ME` (my action ids and user id) go to the combat helper | AP4 | 13 modules import `ingest`, 12 of them only for those two names. The rest of it pre-trains `policy.py`. |
| `postfight.py`, `calibrate.py`, and their data `calibration.json` | 179, 204 | retire | `postmortem.py` is the per-fight review (§5.4) | AP4 | `calibration.json` is still read through `value_model.load_cal` and `engine_bridge.py`; it goes when the per-fight engine bases cover what it holds. |
| `replay.py` | 32 | retire | - | AP4 | Replays a fight through `turn.py`; `postmortem.py` and `tune_real.py` do this against the engine. |

**Combat: engine, opponents, evaluation**

| File | Lines | Verdict | Goes to | Phase | Notes |
|---|---|---|---|---|---|
| `engine_bridge.py` | 425 | keep | combat engine: the offline engine (ground truth) | - | With `harness/pvp_turn/` (the engine harness, its record catalogue and its tools), which stays where it is. |
| `fight_bases.py` | 66 | keep | combat engine: per-fight bases (§5.1) | AP1 | Started by the pilot beside each fight. |
| `engine_fit.py` | 128 | keep | evaluation; writes `fights/engine_bases.json` | AP4 | Run by hand today. Registered as a data feed, or folded into `fight_bases.py`. |
| `meal_factor.py` | 64 | retire | `fight_bases.py` already carries meal and raid buffs (§5.1) | AP4 | **Not wired today:** planner2 reads `fights/live/<battle>_meal.json`, and nothing runs the script that writes it. The integration test only checks that the reader's name appears in planner2's source text. |
| `opponents.py` | 337 | keep | model `opponents` (§5.3), rebuilt after every fight | AP1 | |
| `opp_profile.py` | 140 | keep | opponent dossier: bloodline and rank (§5.3) | AP1 | |
| `opponent_kit.py` | 98 | keep | opponent dossier: kit, weapons and imbues (§5.3) | AP1 | The read before the attack and its retry are on the base (this merge). |
| `fit_gear.py` | 104 | port | opponent dossier: "capped, full Kaeruun plus Subaku's mask, until his damage says otherwise" (§5.3) | AP4 | Run by hand today; nothing imports it. |
| `postmortem.py` | 218 | keep | learning: per-fight review (§5.4), scheduled by the brain between fights | AP4 | |
| `tune_real.py` | 51 | keep | evaluation: the real-fight gate (§6) | AP4 | |
| `engine_check.py` | 194 | keep | evaluation: the accuracy gate (§6) | AP4 | |
| `validate.py` | 244 | keep | evaluation: simulator against the logs; writes `fights/opp_scale.json` | AP4 | The scales are written by hand today (`--write-scales`); as a data feed they run after each fight, or go if the dossier replaces them. |
| `exam.py` | 201 | keep | evaluation; `hp_track` moves to `activities/battle.py` for the result from the log's HP accounting (§5.4) | AP1 for `hp_track` | |
| `fightsim.py` | 289 | keep | smoke test only (§6); planner2's lookahead uses its `Fight` class | AP4 | |

**Tests and fixtures**

| File | Lines | Verdict | Goes to | Phase | Notes |
|---|---|---|---|---|---|
| `tests/test_pilot.py` | 320 | port | the chaos tests and the per-activity tests (brief AP1.7) | AP1 | It writes `pilot_good.py` and `fights/observed/harvest.json` into the tree when run; the ported tests write to a temporary folder only. |
| `tests/test_integration.py` | 86 | port | the wiring test, driven by the registry (brief AP1.6) | AP1 | Seven of its checks read source text for a name instead of exercising the system. The wiring test exercises each one. |
| `tests/test_planner2.py` | 57 | keep, then port | parity against the engine instead of `shotplan.py` | AP4 | |
| `tests/test_nearkill.py` | 72 | port | the same rules, tested on planner2 | AP4 | See `turn.py`. |
| `tests/*.txt` (7 fixtures) | 2 each | keep | fixtures from logged fights (brief §4) | - | One of them (`ziharkk_r2_live.txt`) carries the live effect list. |

Three things the map turned up that the later phases must carry:
1. `turn.py` is the planner Duet has been fixing, so AP4 is a port of rules, not a deletion.
2. Three feeds run by hand or not at all (`meal_factor.py`, `validate.py --write-scales`, `engine_fit.py --write`):
   the registry in AP1 lists each as a data feed with an owner, or the file goes.
3. The connector pads nothing: a field that is missing from one element of a list is dropped from that field's
   column (`pilot.py`, the ground-list comment, and `opponent_kit.save_kit`, which refuses misaligned columns). So
   field selects over lists do **not** stay aligned (§4.7), and AP1 reads lists by columns only where every element
   carries the field, with a length check.

## 3. Principles

1. **One brain, many hands.** All decisions are made in one resident process with one world model. Agents only
   carry calls to the connector and back.
2. **Exact state or say so.** Plan from the game's own live state. Reconstruct only when no live state exists, and
   mark the result as reconstructed.
3. **Windows over guesses.** Model what each side *can* do, round by round (damage curves, tool windows), and
   hedge. Do not predict exact bundles.
4. **Everything registered, everything tested.** An activity or model that is not in the registry does not exist. A
   test fails if one is missing.
5. **Real fights are the judge.** Changes to combat logic are scored on logged real fights, replayed in the engine
   against what the opponent actually did next.
6. **Safety in code, not prose.** The never-list, ask-first gates and do-not-attack list are enforced by the runtime
   and covered by tests.

## 4. Architecture

```
            ┌──────────────────────────── brain (resident process) ────────────────────────────┐
            │  world model ── scheduler ── arbiter ── activities (registry) ── combat engine   │
            │       ▲              │            │              │                    │          │
            │       │         timers/resets   utility       call plans          planner2+     │
            │   results        energy, cds    + gates      (per activity)       lookahead     │
            │       │                                          │                               │
            │   outbox ◄──────────── call budget (30/min shared; lanes) ◄──────────────┘       │
            └───────┬──────────────────────────────────────────────▲──────────────────────────┘
                    │ batches (JSON)                               │ results (JSON)
               ┌────▼─────┐                                   ┌────┴─────┐
               │  relay   │ ── TNR connector (official) ──►   │  relay   │   (Duet-scheduled, replaceable)
               └──────────┘                                   └──────────┘
```

### 4.1 Brain and hands

- **Brain:** a long-running Python process (`player/brain.py`). It owns the world model, scheduler, arbiter,
  activities and combat engine.
- **The outbox and inbox are the contract.** The brain exposes a batch outbox and a results inbox: files under
  `state/player/<account>/live/`, or a local socket with the same messages.
- **Relays:** the TNR connector can only be called by an agent. A relay agent loops: take the batch, execute it
  exactly, return the results. Relays hold no state and make no decisions, so any relay can replace any other
  without loss.
  - Duet schedules relays and restarts them.
  - A watchdog notices a stale outbox (no pickup in 10 s) and alerts.
- **Credentials:** the brain never holds connector credentials (CLAUDE.md §6). It only produces call
  descriptions.
- **Restart safety:** if the brain restarts, it reloads the world model from disk and resumes. It is idempotent per
  battle version.

### 4.2 World model (`player/world.py`)

One typed store, persisted after every result:
- **Character:** HP, chakra, stamina, energy, money, bank, location, status, stats, ranks.
- **Inventory and gear:** with durability; equipped loadouts.
- **Jutsu and training queue.**
- **Timers:** jutsu training, energy, missions, errands and their daily caps, dailies resets, shared cooldowns,
  hospital, stealth, sensory.
- **Battle:** the live effect list, positions, AP, version, seat; his kit and imbues.
- **Opponents:** models, dossiers, cooldown of when we lost to whom.
- **Map knowledge:** sectors and who has been seen where and when.
- **Records:** the session log, findings and the result history.

Every read updates the model, and every module reads the model rather than raw responses.

### 4.3 Activities (`player/activities/*.py`) and the registry

Each activity is a class with the same five methods:
- `available(world)`
- `value(world)` (expected gain per minute, in a common currency, §4.4)
- `plan(world)` (a call plan with checkpoints)
- `on_result(world, result)`
- `done(world)`

`player/registry.py` lists them all, and the wiring test checks that every module under `activities/` is
registered and has tests.

| Activity | Notes |
|---|---|
| `pvp_hunt` | Scan, sensory, stealth, travel, approach, attack (bracket rules, do-not-attack, lost-to cooldown, no AngelSaber snipes). Third-party finishes. |
| `pvp_ranked`, `tournament`, `war`, `bounty`, `shrine` | Phase 3+, each after its playbook exists. |
| `missions` | villageMission and quests: accept, travel, complete, claim. PvE fights use auto-combat where the game offers it (director: auto-combat only against AI), otherwise the PvE policy. |
| `errands`, `dailies` | Daily caps and reset times from the world model; Duet's Hyorin errands become the first errand route. |
| `hunting` | The hunting profession cycle. |
| `farming` | The farming profession, raids and farmable content the account can reach. |
| `training` | Jutsu training queue (lowest level first, targets), energy to intelligence or willpower in the village, sensei and skill-tree points when available. |
| `restock` | Item shop, inventory, home storage, auction (≤ price caps); ryo only, never premium currency. |
| `repair` | Repair only when an item is near broken (director: worn is fine, broken is not; threshold 25%). |
| `equipment` | Loadouts per activity (PvP, PvE farm, profession). Swap the thrown weapon or weapons when the kit says so. Equip upgrades the account already owns. |
| `recovery` | Full Potion at the end of any fight, in the same batch; hospital; ramen for chakra and stamina. |
| `bank` | Keep money banked above a reserve. |
| `session` | Start: claim the run lock. End: train intelligence, sleep at home sector 177, PvP1 loadouts, release the lock. |

### 4.4 Arbiter

A utility arbiter picks the next activity:
- **Score:** `value × urgency × readiness`, with hard preemption by priority class:
  1. **Battle** (a fight in progress always wins).
  2. **Safety:** HP below threshold, hospital, being hunted.
  3. **Deadlines:** a timer about to expire, a daily resetting.
  4. **Upkeep:** training queue empty, items low, gear near broken.
  5. **Goals:** PvP, missions, farming.
  6. **Scouting.**
- **Common currency for value:** progress points per minute, with weights set in `player/goals.json` that the
  director edits, e.g. "PvP kills matter most this week".
- **Interleaving:** short upkeep tasks run during travel waits.

### 4.5 Gates (safety in code)

`player/gates.py` checks every call against:
- the endpoint allowlist (`data/player_allowlist.json`, from `state/prompt_playing_tnr.md` §4.2);
- the never-list (payments, account deletion, other players' data, moderation, deletes without a per-record yes,
  chat or messages);
- the ask-first list: premium currency (reputation), leaving the clan, selling rare items, marriage, and any spend
  above caps;
- `do_not_attack.md`;
- no Flee.

An ask-first action becomes a **pending decision**: the brain notifies the director and carries on with something
else. A refused call is logged as a finding, never retried around.

### 4.6 Call budget and battle lane

- **Budget:** 30 calls a minute is shared by the account, and no call is scheduled past it: a 31st would only be
  refused. The three lanes (**battle**, **recovery**, **world**) decide who gives way first.
  - A turn's actions and recovery calls may use the whole minute.
  - No read takes the room of a turn's actions (5 calls).
  - The reads that only watch a fight (his turn's polls, the poll behind my actions) and the world lane (at most
    20 a minute) leave room for a turn and the read behind it (8 calls). For that reserve alone, a fight is never
    left unread for more than 12 s.
  - When the minute is full all the same, the call waits. A wait in front of an action or a recovery call, or a
    blind wait over 12 s, is logged as a finding. (AP1 review, finding 1: read as "never paced", the battle
    lane could pass the limit.)
- **A battle turn has a deadline.** From turn start the brain must fire by T+20 s. If the exact read is not back by
  T+12 s, it plans from the last good read. If the planner is not done by T+15 s, it fires the best line so far.
  Every turn records its timing and how long the fight went unread before the turn was seen. Any turn within
  20 s of the limit is a finding.
- **A turn knows what happened to its actions** (sent, answered, accepted by the game).
  - A plan that came back refused, or never reached the game, is replaced while the turn is still open.
  - With no line from the planner, the turn's best line so far goes; failing that Defensive Stance, then End
    Turn. An action the game has refused is never sent again.
  - A turn closes as **acted**, **missed** or **unresolved**, from the game's answers and the battle log only.
    Unresolved turns are counted apart from missed ones and are never counted as played.
- **Actions:** sent with a 1.2 s gap (director: not all at once).
- **Fight end:** the end-of-fight batch carries recovery first (Full Potion), then the reads.

### 4.7 Built for the smallest model (director 2026-11-11: "run by an incredibly efficient model … design it for
Haiku and save on tokens")

Every decision is code in the brain, so the only model in the loop is the relay, and the relay needs no judgment: it
copies calls. The design targets **Claude Haiku as the relay**, and keeps the larger models out of the loop
entirely.

- **The relay contract is mechanical.**
  - One short system prompt (under 300 words, `player/RELAY.md`) and one loop: run `brain next`, make the calls it
    prints exactly, run `brain next` again.
  - No reasoning, no summaries, no text between calls. Parallel tool calls in one message per batch.
  - Anything that needs judgment never reaches the relay. It becomes a pending decision for the director (or a Duet
    message), raised by the brain.
- **Tokens in are what the relay pays for, so every response is trimmed at the source.**
  - Every call carries a `select` of only the fields the brain uses.
  - Lists are read as columns, e.g. the ground list (~8× smaller).
  - The effect list is read with a field select once AP0 confirms that selects on arrays stay aligned when a field is
    missing. Until then, it's read whole only on my turn.
  - Static data (catalog, kits, maps) is cached in the brain and never re-read through the relay.
- **Fewer, fuller batches.**
  - Polling backs off on the opponent's turn (long sleeps inside the brain's own wait, not repeated reads).
  - Upkeep is grouped into one batch per pass.
  - The brain's waits are Bash sleeps, which cost almost nothing.
- **Rotation by size, not count.** Relays restart when their context passes a token threshold (default 60k), not
  after a batch count. The brain is resident, so a restart loses nothing.
- **Results flow:**
  - Today the brain reads results out of the relay's transcript.
  - The relay protocol keeps that (no tokens spent echoing results). Every relay gets a name on its first
    `brain next`, and every batch ends with `brain next <token>`. The brain reads only the transcript that
    carries that token, only the calls made for that batch, and matches each to a call the batch asked for.
  - One fallback: when no transcript carries the token, the batch asks for each result in turn with
    `brain put <token> <n>`, the result on standard input.
- **Measured.** Tokens per hour and per fight are a KPI in the weekly report. The targets, set in AP1 from the first
  measurements, are a fixed cap per fight turn and per hour of world activity.
- **Larger models:**
  - Fable (or Duet's main model) is used only for building, reviewing post-mortems on request, and the weekly report.
  - None of them sits in the live loop.

## 5. Combat

### 5.1 State

The live effect list (`combat.getBattle` usersEffects) is read on every battle poll and feeds planner2's arrays
through one mapper, `from_live`, built on the source rules:
- the rounds countdown;
- immediate effects (shields);
- seals lifting only bloodline passives;
- wound from the original damage;
- drain from max HP;
- afterburn as its own effect.

Ground zones come from the ground list. Per-fight engine bases (`fight_bases.py`) carry every permanent modifier, so
the arrays hold only temporary effects. Every live state is archived per round.

### 5.1b Move atlas

There is one generated card for every action usable in PvP: about 1,600 jutsu, weapons, consumables and basics.
Each card is compiled from the catalog and measured in the engine:
- costs, cooldowns, locks, range, elements;
- each effect as an exact change to the round arrays, with its timing and how Clear, Cleanse and seals treat it;
- damage at the standard assumption, rescaled per fight.

The state machine applies a card when the live state shows that cast. Every clock and weight that moves on the
time-to-kill then comes from the card, and nothing is estimated. It replaces the hand-written kit specs.

What stays uncertain is only *which* card he picks next. That is why the planner works in windows and hedges
(§5.2). The archive stores every fight as card ids plus the exact live state of each round, so his behaviour models
learn from clean inputs as the data grows. Prediction counts in the planner only while it beats the base rate on
held-out fights.

### 5.2 Decision

- **One planner (planner2).** turn.py, shotplan.py and value_model.py are retired into helpers or deleted once
  nothing imports them.
- **Windows:** both sides' damage curves over the next 3 turns on their cooldown clocks, through the live
  multipliers, DR, absorb and shields, plus each side's tool windows (Clear, Cleanse, Smoke, Kim's, prevents, Seal).
  A move is valued by how it bends the curves, and the race is who reaches the other's HP first, in turn order.
- **His replies:** his ready lines, weighted by habits and in-fight memory, with a hedge (35%) on his hardest hit.
  Exact-bundle prediction is not a goal.
- **Lookahead:** two exchanges (mine, his, mine, his) over the top 20 candidates, inside the turn deadline.
- **Solution library:** situation key (HP bands, live multipliers, flags, his last turn's signature) to responses
  proven in the engine against real opponents' actual next turns, weighted by evidence.
- **Seat rules:** player 1 vs player 2, same-round stun, castThisRound (Duet's fixes).

### 5.3 Opponent dossier

Ready before the first action of a fight. When we attack, it's read before the attack; when we're attacked, the
first battle poll reads it, retried until saved. It holds:
- his kit, with weapons and imbues learned from what his weapons apply;
- his bloodline and rank;
- his windows from past logs (when he bursts, how often he Clears first);
- the lost-to cooldown;
- the default assumption: capped, full Kaeruun plus Subaku's mask, until his damage says otherwise.

### 5.4 After every fight

1. Result from the log's HP accounting (not status alone).
2. Archive the live states and log.
3. Post-mortem (low priority, paused during fights): his read, planner vs engine vs log damage, and choice regret
   against his actual next turn.
4. Merge into the solution library.
5. Update the opponent models.
6. Report to the director: result, key turns, turning point.

### 5.5 PvE combat

AI fights (missions, hunts, raids) use auto-combat where the game offers it. Otherwise they use planner2 in PvE mode:
the same state and windows, the opponent being the AI's scripted kit, and no hedge on behaviour it does not have.

## 6. Learning and evaluation

| Check | Gate |
|---|---|
| `engine_check` (live-shaped) | ≥ 95% of bundles within 1% of the engine, damage dealt and self HP |
| `tune_real` (real fights, picks answered by his actual next turn) | A combat change ships only if it does not lower the mean exchange or the best-of-set rate on the last 20 real fights |
| Wiring test | Every activity, model and data feed is registered and exercised |
| Chaos tests | Refusals, rate limits, timeouts, relay restarts, battle starting mid-errand, Full Potion at fight end, deadline fallback |
| Live KPIs (weekly report) | PvP win rate, turns missed (target 0), training queue idle minutes (target 0), dailies completed, money and stats over time, relay tokens per hour and per fight, findings |

The fight simulator stays as a smoke test, not a gate.

## 7. Operations (Duet)

- Duet runs the relays and the brain, restarts them, and sends alerts:
  - fight start;
  - fight end with result and turning point;
  - pending decisions;
  - stalls;
  - a daily summary.
- **Run lock:** claimed as `player` for each session and heartbeated by the brain.
- **Scheduled jobs:** nightly `tune_real` on the day's fights (between fights only), a weekly report and harvesting
  of public battle histories.
- **The director's play:** when the director plays in the browser, the brain pauses world activities. Director mode
  remains for fights, with the window counted once from turn start.

## 8. Phases

| Phase | Delivers | Exit gate |
|---|---|---|
| AP0 | Inventory: MCP router surface (live list 2026-11-11: 83 routers), allowlist draft, current tools mapped to modules, merge of `fable/pvp-engine-harness` and `fable/pilot-planner-fixes` into one base | Allowlist approved; one green base branch |
| AP1 | Brain and hands: world model, outbox/inbox, Haiku relay (§4.7), trimmed selects, budget lanes, battle deadline, gates, registry + wiring test; PvP and recovery ported from pilot.py | Chaos tests green; one live PvP session on a Haiku relay with zero missed turns and the token figures recorded |
| AP2 | Upkeep activities: training, restock, repair, equipment, bank, session start and end | 24 h live with training never idle and no ask-first breach |
| AP3 | Progression activities: missions, errands, dailies, hunting, farming, PvE combat | Daily routine completes unattended for 3 days |
| AP4 | Combat consolidation: the move atlas (§5.1b) first, then one planner, curves on if `tune_real` passes, library and post-mortems on the brain, retire turn.py | Atlas coverage and accuracy gates; engine-check and real-fight gates (§6) |
| AP5 | Further modes: ranked, tournament, war, bounty, shrine; weekly report and findings pipeline | Each mode's playbook and test before it goes live |
| AP6 | The simplest implementation of every required behavior: freeze the gates and a 300-situation decision corpus; simplify logic inside functions and across state flows; remove unnecessary steps, duplication, state and indirection; delete proven redundancy. See the brief's AP6 and RUL-2026-11-12-153 | Contract green, budget met, reviewed simplification record and readability, 48 h live parity, director sign-off |
| AP7 | The director's console: status, events and settings files (written from AP1 on), a phone-first Dashboard with Now, Today, Decisions, Settings, Health and Trends tabs, settings flowing back to the brain through the gates, short push notifications | Director can follow, approve, pause and re-weight from his phone; changes live within 2 min; a week with no missing events |

## 9. Decisions for the director

1. **Goals and weights:** what the account should progress first. This seeds `player/goals.json`.
   Decided: RUL-2026-11-11-149 item 5.
2. **Equipment swapping:** the PvP brief says not to change loadouts or gear unless told to. This overhaul asks for
   swaps "as needed". Confirm the scope: loadouts per activity, weapon swaps, and equipping upgrades already owned.
   Buying gear stays under the spend caps.
   Decided: RUL-2026-11-11-150 (a PvP 2 loadout for the matchups the standard build loses) and
   RUL-2026-11-11-152 item 4 (PvP 2 is the experimental build; PvP 1 stays unchanged).
3. **Spend caps:** the daily ryo cap and reserve (today 3M/day, 500k reserve); auction price caps.
   Decided: RUL-2026-11-11-152 item 3 (a spend over 50M ryo is asked first; the 500k reserve stays).
4. **PvE auto-combat:** confirm auto-combat for every AI fight, or only for missions and errands.
5. **Session windows:** when the brain may run, and its share of the 30 calls a minute while you play.
   Decided: RUL-2026-11-11-149 item 6.
6. **Which further modes to enable first:** ranked, tournament, war, bounty, shrine.

## 10. AP6 simplification record

Filled in during AP6: record the required behavior, unnecessary complexity, simpler implementation and evidence
that behavior is preserved. Cover functions inside retained modules and flows spanning modules. Outcomes may
be rewritten, consolidated, removed as redundant, or retained with a reason that the code is already clear.

The objective is simpler logic and fewer unnecessary moving parts. A function count or line reduction alone
does not establish success. Keep useful boundaries, prefer clear direct code, and explain the before/after
improvement. The governing process and unchanged numerical budgets are in `state/prompt_ai_player_overhaul.md`,
AP6 (clarification: RUL-2026-11-12-153).

| Function, component or flow | Required behavior | Unnecessary complexity | Change and why it is simpler | Preservation evidence |
|---|---|---|---|---|
