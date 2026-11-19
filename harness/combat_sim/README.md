# combat_sim: real TNR fights, offline

One reusable harness for "how does this fight play?". It runs fights on the game's own combat code, pinned to a
commit (`ENGINE_PIN`), in a socket-denied child process. It makes zero live requests and changes nothing live.

It takes:
- **records**: AI rows, AI profiles, jutsu, items, user items, bloodlines, pets, damage settings and shared
  cooldowns, as the connector returns them (`data/live/<date>/`). It can also take a manifest's records dropped into
  another folder with the same layout, plus design knobs in the scenario (`enemyOverrides`: level, aiEdit, rules,
  a replacement jutsu record).
- **players**: a spec with level, rank, stats (or the level's stat budget), pools, masteries, elements, preferred
  generals, bloodline, jutsu with levels, gear, pets and auto-combat rules (default: `rotationRules` in
  `engine/model.ts`). Any other spec field is refused.

It reports, per variant and fight:
- win rate and rounds to win (median, p10, p90);
- party HP left and how many players went down;
- the engine's own settlement (`calcBattleResult`) per player, and which seeds won;
- for every enemy move (definitions below): `usesPerFight`, `usedInRunsPct`, `firstUseRound`, `useRound`,
  `hitPartyPct`, `partyDamagePerUse` and `netPartyHpLossPerUse`;
- the player's own move counts and dodge steps, plus a step-by-step trace of seed 1 for every variant and fight;
- the invocation, the scenario's sha256, the harness code hash (`engine/*.ts`), the engine pin, the scenario's
  `_assumptions` and each player's full build, `notModelled` list included.

### Enemy move metrics

| Field | Meaning |
|---|---|
| `usesPerFight` | mean uses per fight |
| `usedInRunsPct` | share of fights in which the move was used at least once |
| `firstUseRound` | per fight, the round of its first use; median, p10, p90 over the fights that used it |
| `useRound` | median, p10, p90 over every use |
| `hitPartyPct` | share of uses whose own effect lines damaged a party member |
| `partyDamagePerUse` | the engine's own "X takes N damage" lines on party members in the move's action effects, summed per use (0 when it hit nobody). Later ticks and expiry are not counted here. |
| `netPartyHpLossPerUse` | party HP lost over the whole step (expiry, ticks and heals included), over the uses that lost any. It is not per-hit damage. |

### Whole hideout vs floors

Each floor is its own fight with a full restore. `winRate` is per floor. `wholeHideout.seedIndicesClearingEveryFloor`
counts the seed indices whose run was won on every floor (each floor's run is an independent draw, so this is an
empirical joint, not a single continuous run); `productOfFloorWinRatesPct` is the product of the floor rates.

## How it stays faithful

- **Assembly** follows `initiateBattle`: capUserStats, then `processUsersForBattle` (opening slice: players plus
  wave 1, with a shared summon cache and the pet preload), then `prepareEncounterWaves`. After that come the dungeon
  extra state, auto-combat, `syncPoolAdjustments`, `refreshMasteries`, the aggressor flag, starting barriers, and
  initiative order. The live `dmgConfig` and `sharedCooldowns` go into `extraState` the way the insert stores them.
- **Spawns**: `processUsersForBattle` places every fighter itself. Its `randomInt` (node:crypto) is the one
  engine import the harness replaces: `engine/entropy_plugin.ts` rewrites that single import line in
  `src/server/api/routers/combat.ts` at load time to `engine/entropy.ts`, which draws from the run's seed. Nothing
  else in the engine is rewritten, and pets and their ground passives are placed by the engine. A scenario's
  `placements` feed that same draw (the planned cell's index); a cell that is not a free spawn cell is refused.
- **Turns** follow `performAction`:
  1. advanceEncounterWave
  2. alignBattle (pre-action; it runs the sage transition itself)
  3. the action
  4. dungeon lastActionRound
  5. alignBattle (post-action)
  6. advanceEncounterWave
  7. `calcBattleResult` per player, from the pinned settlement code. A fight is won when some player's result is
     Won, lost when every player has settled without a win, stalled at the round cap.
- **History**: each step records the router's history entry: its description (" It is now X's turn." included) and
  its applied effects in router order: pre-action expiry, the action, post-action expiry, orphaned summons.
  `engine/transition_fixture.ts` checks that a Curse paid at a round transition lands in the entry and the HP delta.
- **Actors**: AI and summons act through `performAIaction`. Players act through the auto-combat path with their
  profile rules. The replay instead forces a logged player's actions through
  `availableUserActions` → `performBattleAction`, the human path.
- **Randomness**: `Math.random`, `crypto.getRandomValues`, nanoid's pool, node:crypto `randomInt` (through the
  entropy plugin) and the clock are seeded per run. The same seed gives the same fight.
- **Dodge policy** (`policy.dodge`): a player standing on an enemy telegraph steps to the nearest unmarked hex
  first, as a person reading the floor would. Without `dangerAnimations` it counts any enemy-created ground effect
  that has an animation. It stands in for a human and is a declared test input; switch it off to see an inattentive
  player.

## Validation: the Isonade log (Nov 18, battle MUH-bMM1A-0_o-CkIehGg)

`scenarios/isonade_replay.json` rebuilds the director's character from live reads taken the same evening:
stats, pools, masteries, gear, jutsu levels (they match the log's buff percentages) and the active pet. It then
forces every logged action at the logged tile.

A seed is **exact** only when all of these hold (`engine/replay_check.ts`, one predicate for the count, the gate and
the saved example):
- the sim's history has as many entries as the log, and entry k matches log entry k on round, actor, actionId,
  description and the complete ordered list of effect lines;
- actors map one-to-one (the player's id is the logged id);
- every damage line matches the log to the cent;
- every logged player action was used, none was refused, and no player turn timed out unforced;
- the engine settles the fight Won in round 12, as logged.

`tests/replay_check.test.ts` holds the false positives the predicate must reject: altered damage, a deleted AI
damage line, an extra AI action, a missing player wait, an extra entry, a round-99 loss, a wrong outcome or round,
swapped actors, and unconsumed, refused or idle player turns.

Across 20 seeds (`results/isonade_replay.json`):
- **11 are exact** (seeds 1, 4, 9, 10, 11, 12, 13, 14, 15, 17, 20): all 87 history entries match, every damage line
  matches to the cent, and the engine settles the fight Won in round 12.
- **9 are not.** Each first differs at entry 3, where the log has Isonade's It Rises and the sim has a move; the sim
  then loses in round 7.

Every seed opens on the same cells (dauntless D4, Little Horror C4, Isonade I2). What differs is the initiative
order. All 11 exact seeds share the turn cycle dauntless → Isonade → Little Horror (whoever starts); all 9 others
share dauntless → Little Horror → Isonade. That is what the per-seed records show. Why that order changes Isonade's
first choice is not established. Per-seed opening cells, initiative order and first divergence are in the results.

The first attempt left the pet out, and every hit came out at exactly 0.833 of the log. That was Little Horror's
species passive: +20% damage given for its owner and -10% damage given for enemies. Pets are now modelled; leave one
out and damage is off by its passives.

Gate: `run.sh replay.ts --scenario harness/combat_sim/scenarios/isonade_replay.json --expect-exact 11`
(a minimum count of exact seeds).

## Use

```
harness/combat_sim/tools/pull_live.py <session transcript .jsonl> harness/combat_sim/data/live/<date>
harness/combat_sim/run.sh selftest.ts
harness/combat_sim/run.sh transition_fixture.ts
harness/combat_sim/run.sh replay.ts --scenario harness/combat_sim/scenarios/isonade_replay.json --out harness/combat_sim/results/isonade_replay.json --expect-exact 11
harness/combat_sim/run.sh main.ts --scenario harness/combat_sim/scenarios/genin_hideout.json --out harness/combat_sim/results/genin_hideout.json
harness/combat_sim/run.sh main.ts --scenario ... --seeds 5 --only "L15 solo|L15 solo, no dodging" --out part1.json   # "|" separates names
python3 harness/combat_sim/tools/merge_results.py results/x.json part1.json part2.json ...   # same scenario, code and pin only
python3 -m unittest discover -s harness/combat_sim/tests
bun test harness/combat_sim/tests/replay_check.test.ts
```

### pull_live.py

`pull_live.py` reads the answers the connector already gave in a session, so it makes no new request. It keeps
only unfiltered answers: a call made with `select`, `search` or `maxLength` is skipped. To refresh inputs, read the
records with the connector without filters, then run it.

Records it needs:
- `profile.getAi` for every AI and every summon target;
- `ai.getAiProfile` for each AI's profile;
- `jutsu.get` for player jutsu;
- `item.getUserItem` or `item.get` for gear;
- `bloodline.get`;
- `pets.getPet`;
- `misc.getDmgConfig` and `misc.getSharedCooldowns`;
- `combat.getBattleEntries` with `showBasicActions` for a replay.

### Setup (once, outside the harness)

`run.sh` never installs anything. Provision the engine export yourself, from a machine allowed to fetch packages:

```
git -C <game clone> archive <ENGINE_PIN> app | tar -x -C <dir>
cd <dir>/app && bun install --frozen-lockfile --ignore-scripts
```

Then pass `TNR_ENGINE_APP=<dir>/app`. Without `TNR_ENGINE_APP`, `run.sh` exports the pin from the local clone
(`TNR_ENGINE_SRC`, default `/root/work/game`) into `TNR_ENGINE_WORK` and stops with exit 3, because that export has
no `node_modules`.

### run.sh

- The pin is always the committed `ENGINE_PIN`. A `TNR_ENGINE_PIN` that differs stops the run (exit 2).
- Before every run, `tools/verify_export.py` checks the export's source file by file against `git ls-tree <pin> app`
  in the clone (blob hashes and the exact file set, outside `node_modules`). A changed, missing or extra file stops the
  run (exit 2). `tests/test_run_sh.py` covers these refusals and the missing-dependency stop.
- The engine runs in a child with sockets denied (`harness/ghost_ship_final/tools/offline_exec.py`).

### What it writes locally

- `run.sh`: an export under `TNR_ENGINE_WORK` (when `TNR_ENGINE_APP` is unset), and a per-run copy of `engine/*.ts`
  inside the export (`tnr_combat_sim_<pid>/`, removed on exit).
- `pull_live.py`: record files under the folder you name; every id is checked against `[A-Za-z0-9_-]+` and every
  path must stay inside that folder.
- `main.ts` / `replay.ts`: the `--out` file.

## Limits (say them with every result)

- **Player builds are assumptions** unless they come from a real character. The genin scenario's `_assumptions`
  state its builds; they are copied into the results.
- **Not modelled for players: skills, titles, raid buffs, cooking, village and faction relations, clan, ANBU squad,
  loadouts and sage mode.** The player row leaves them empty and a spec cannot set them. Pet skills are passed to the
  engine as `pets.getPet` returns them. A real character with any of these will not match the sim, and a replay of
  their log will show it.
- **The default rotation is a simple priority list, not a person.** It does not plan setup rounds, focus fire or
  kite beyond the dodge step.
- **A player's real starting tile and their pet's are unknown** unless a scenario gives `placements`. Otherwise the
  engine draws spawns from its spawn list with the run's seed.
- **The dungeon's one-hour deadline is not modelled.** The 3-round inactivity rule is, through `lastActionRound`.
