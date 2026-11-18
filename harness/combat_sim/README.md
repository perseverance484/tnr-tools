# combat_sim: real TNR fights, offline

One reusable harness for "how does this fight play?". It runs fights on the game's own combat code, pinned to a
commit (`ENGINE_PIN`), in a socket-denied child process. It makes zero live requests and changes nothing live.

It takes:
- **records**: AI rows, AI profiles, jutsu, items, user items, bloodlines, pets, damage settings and shared
  cooldowns, as the connector returns them (`data/live/<date>/`). It can also take a manifest's records dropped into
  another folder with the same layout, plus design knobs in the scenario (`enemyOverrides`: level, aiEdit, rules,
  a replacement jutsu record).
- **players**: a spec with level, rank, stats (or the level's stat budget), pools, masteries, elements, bloodline,
  jutsu with levels, gear, pets and auto-combat rules (default: `rotationRules` in `engine/model.ts`).

It reports, per variant and fight:
- win rate and rounds to win (median, p10, p90);
- party HP left and how many players went down;
- for every enemy move: how often it fired per fight, its first and typical round, how often it hit the party, and
  the damage when it did;
- the player's own move counts and dodge steps, plus a step-by-step log of the first seed.

## How it stays faithful

- **Assembly** follows `initiateBattle`: capUserStats, then `processUsersForBattle` (opening slice: players plus
  wave 1, with a shared summon cache and the pet preload), then `prepareEncounterWaves`. After that come the dungeon
  extra state, auto-combat, `syncPoolAdjustments`, `refreshMasteries`, the aggressor flag, starting barriers, and
  initiative order. The live `dmgConfig` and `sharedCooldowns` go into `extraState` the way the insert stores them.
- **Turns** follow `performAction`:
  1. advanceEncounterWave
  2. alignBattle (plus the sage transition)
  3. the action
  4. dungeon lastActionRound
  5. alignBattle
  6. advanceEncounterWave
  7. outcome: `dungeonBattleOutcome` for floors.
- **Actors**: AI and summons act through `performAIaction`. Players act through the auto-combat path with their
  profile rules. The replay instead forces a logged player's actions through
  `availableUserActions` → `performBattleAction`, the human path.
- **Randomness**: `Math.random`, `crypto.getRandomValues`, nanoid's pool and the clock are seeded per run. The same
  seed gives the same fight.
- **Dodge policy** (`policy.dodge`): a player standing on an enemy telegraph steps to the nearest unmarked hex
  first, as a person reading the floor would. Without `dangerAnimations` it counts any enemy-created ground effect
  that has an animation. It stands in for a human and is a declared test input; switch it off to see an inattentive
  player.

## Validation: the Isonade log (Nov 18, battle MUH-bMM1A-0_o-CkIehGg)

`scenarios/isonade_replay.json` rebuilds the director's character from live reads taken the same evening:
stats, pools, masteries, gear, jutsu levels (they match the log's buff percentages) and the active pet. It then
forces every logged action at the logged tile.

Across 20 seeds:
- **11 reproduce the log exactly.** All 21 logged hits match to the cent, both recoil hits match, every Isonade
  and Grasping Arm action matches in order, and the fight is won in round 12.
- **The other 9 diverge for one reason.** The pet's starting tile isn't in the log. When it starts elsewhere,
  Undertow pulls the director's character 2 hexes instead of 3, so the logged moves no longer line up.

The first attempt left the pet out, and every hit came out at exactly 0.833 of the log. That was Little Horror's
species passive: +20% damage given for its owner and -10% damage given for enemies. Pets are now modelled; leave one
out and damage is off by its passives.

Gate: `run.sh replay.ts --scenario scenarios/isonade_replay.json --expect-exact 10`.

## Use

```
harness/combat_sim/tools/pull_live.py <session transcript .jsonl> harness/combat_sim/data/live/<date>
TNR_ENGINE_APP=<existing export>/app harness/combat_sim/run.sh selftest.ts
harness/combat_sim/run.sh replay.ts --scenario harness/combat_sim/scenarios/isonade_replay.json --expect-exact 10
harness/combat_sim/run.sh main.ts --scenario harness/combat_sim/scenarios/genin_hideout.json --out harness/combat_sim/results/genin_hideout.json
harness/combat_sim/run.sh main.ts --scenario ... --seeds 5 --only "L15 solo"
python3 -m unittest discover -s harness/combat_sim/tests
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

### run.sh

Without `TNR_ENGINE_APP`, `run.sh` exports the pin from a local game clone (`TNR_ENGINE_SRC`, default
`/root/work/game`) with `git archive`. It then runs `bun install --frozen-lockfile --ignore-scripts` once.

## Limits (say them with every result)

- **Player builds are assumptions** unless they come from a real character. The genin scenario uses the engine's
  own player stat scale (the level's whole stat budget, spread evenly), level pools, masteries at 10, no gear and
  no pets.
- **The default rotation is a simple priority list, not a person.** It does not plan setup rounds, focus fire or
  kite beyond the dodge step.
- **A player's real starting tile and their pet's are unknown.** Spawns are drawn from the engine's spawn list with
  the run's seed.
- **The dungeon's one-hour deadline is not modelled.** The 3-round inactivity rule is, through `lastActionRound`.
