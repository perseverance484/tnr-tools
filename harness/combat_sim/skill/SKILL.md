---
name: simulating-tnr-combat
description: Runs real The Ninja RPG (TNR) fights offline on the game's own combat code to answer "how does this fight play?" — win rates, rounds, HP left, and which enemy moves fire when and how hard — for a dungeon floor, boss, wave, hunt or quest fight, solo or in a party, before anything goes live or to explain a live result. Also replays a real battle log to check the sim. Use this skill whenever the user asks to test, sim, balance-check, tune or compare a TNR PvE fight, asks how long a fight takes or how hard a boss hits, wants a fight checked at a level or party size, or uploads a battle log to compare, even if they don't say "sim" or "harness". Zero live requests.
---

# Simulating TNR combat

The harness lives in `harness/combat_sim/` in `perseverance484/tnr-tools`. Read its README before the first run:
it lists what is modelled, what is assumed and the validation result. This skill is the procedure.

## Rules

- **Zero live requests from the sim.** Live data comes in only as connector reads you already made, saved by
  `tools/pull_live.py`. Reads only: never a live write, never an unhide, never the director's character.
- **The engine decides every number.** Do not hand-compute damage or patch engine behaviour. If the engine does
  something surprising, report it with the step log. Do not "fix" it: the game is worked within as it is, and no
  change to its code is proposed.
- **Pin the engine.** Run against `ENGINE_PIN`. If the game has moved on and the fight touches changed code, bump the
  pin in its own commit, then re-run the replay gate (below) before trusting new numbers.
- **Say the assumptions with every result:** the player build, the rotation, the dodge policy, pets on or off, the
  seed count and the round cap. A result without its build is not a result.
- **Say what is not modelled.** Player skills, titles, raid buffs, cooking, village and faction relations, clan, ANBU
  squad, loadouts and sage mode are left out, and a player spec cannot set them. A character who has any of these
  will not match the sim.
- **Whole run vs floor.** Say which one a number is: a floor's win rate, or the whole hideout cleared on every floor.

## 1. Gather the records (read-only)

With the TNR connector, read each record unfiltered (no `select`, `search` or `maxLength`):

| What | Endpoint |
|---|---|
| every enemy and every summon target | `profile.getAi {userId}` |
| each AI's profile (rules) | `ai.getAiProfile {id}` |
| each player jutsu | `jutsu.get {id}` |
| gear | `item.getUserItem {id}` (a real character's) or `item.get {id}` |
| bloodline | `bloodline.get {id}` |
| pet (its species passives change damage) | `pets.getPet {petId}` |
| damage settings | `misc.getDmgConfig` |
| shared cooldowns | `misc.getSharedCooldowns` |
| a log to replay | `combat.getBattleEntries {battleId, showBasicActions: true, userFilter: "all", limit: 200}` |

Then save them:
`python3 harness/combat_sim/tools/pull_live.py <this session's transcript .jsonl> harness/combat_sim/data/live/<YYYY-MM-DD>`

A content manifest's pending records can go in another folder with the same layout. List it after the live folder,
since later folders win. Or put a single change in the scenario's `enemyOverrides` (level, aiEdit, rules,
replacement jutsu).

## 2. Write the scenario

Copy `scenarios/genin_hideout.json`. Set:
- `_assumptions`: the build assumptions in words; they are copied into the results.
- `fights`: each fight's waves, as `aiIds` and `delayRounds`.
- `mode`: `dungeon` for a dungeon floor (waves, full restore between floors) or `quest` (all enemies at once).
- `players`: the builds.
- `variants`: the party compositions and the dodge policy for each.

Build players from a real character where one exists. That means stats, pools, masteries, gear, jutsu levels and
pets. Otherwise state the assumed build. Run at least:
- the lowest and highest level the fight is for;
- solo, and a full party where parties are allowed;
- dodge on and off, when the fight has telegraphs.

## 3. Run

```
harness/combat_sim/run.sh selftest.ts
harness/combat_sim/run.sh transition_fixture.ts
harness/combat_sim/run.sh replay.ts --scenario harness/combat_sim/scenarios/isonade_replay.json --expect-exact 11
harness/combat_sim/run.sh main.ts --scenario <scenario> --out harness/combat_sim/results/<name>.json [--seeds N] [--only "variant|variant"]
python3 harness/combat_sim/tools/merge_results.py <out.json> <part.json>...   # parts of one scenario, same code and pin
```

- **Order:** run `selftest.ts` and the replay gate first, every time the pin or the harness changes.
- **Engine export:** set `TNR_ENGINE_APP` to an export whose dependencies were installed beforehand (README,
  Setup). `run.sh` never installs; it checks the export against `ENGINE_PIN` file by file and stops on any difference.
- **Speed:** long fights cost about 5 s per fight-seed. Start with `--seeds 3` to see the shape, then 10 to 20
  seeds for numbers.

## 4. Read and report

Each fight in the output has:
- `winRate` and `roundsToWin` (median, p10, p90);
- `partyHpLeftPctWhenWon` and `playersDownWhenWon`;
- `participantSettlements` (the engine's own `calcBattleResult`) and `wonSeeds`;
- `enemyMoves`: per enemy and per move, `usesPerFight`, `usedInRunsPct`, `firstUseRound` (per fight, then median,
  p10, p90), `useRound`, `hitPartyPct`, `partyDamagePerUse` (the engine's own damage lines on the party) and
  `netPartyHpLossPerUse` (whole-step HP loss, ticks and heals included; not per-hit damage);
- the player's own move counts and `dodgeStepsPerFight`;
- `issues`.

Per variant, `wholeHideout` gives the seeds that won every floor. `tracesFirstSeed` is a readable step log of seed 1
for every variant and fight. Use it to explain *why* before giving numbers.

Report in the director's terms, short:
- win rate and rounds per variant against the design target;
- the one or two moves that decide the fight;
- what would change it.

Any retune is the director's call. It is built and shipped through the content skills, not here.

## 5. Validating against a live log

When a real fight disagrees with the sim, replay it:
1. Rebuild the player exactly (pet included) in a scenario like `isonade_replay.json`.
2. Run `replay.ts`.

`exactSeeds` counts the seeds whose whole history matches the log entry by entry (actor, action, description, every
effect line, damage to the cent), with every logged action used and the logged outcome and round. `perSeed` gives
each seed's opening cells, initiative order and first divergence.

| What you see | Likely cause |
|---|---|
| A constant damage ratio on every hit | A passive is missing. If it is the pet's, read `pets.getPet` and add the pet. If the character has skills, titles, raid buffs or sage mode, the sim cannot model them: say so. |
| Some seeds exact, others diverge early | Opening state the log doesn't record. Compare `perSeed` openings and first divergences before naming a cause. |
