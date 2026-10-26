# Skyglass Wreck dungeon simulator (offline, engine-driven)

Runs the Skyglass Wreck's real fights through The Ninja RPG's own combat engine, in memory,
to time a 3-player clear against the 60-minute dungeon limit (`DUNGEON_RUN_SECONDS = 3600`)
and to tune enemies and waves before anything is pushed. Zero live requests, no credentials:
the engine is a `git archive` export of a local game clone, run in a socket-denied child
(`harness/ghost_ship_final/tools/offline_exec.py`: `unshare -rn` plus seccomp).

Results and findings: `REPORT.md`. Raw results: `results/*.json`.

## Run

Requirements: git, Python 3, Bun 1.4.x, a local game clone containing the pinned commit,
`unshare` (or `TNR_NETWORK_ISOLATION=seccomp`).

```bash
# Baseline (captured live state), all player tiers, 30 seeded runs each:
harness/skyglass_wreck_sim/run.sh --runs 30 --out harness/skyglass_wreck_sim/results/baseline.json

# A candidate design from an override file, selected player tiers:
harness/skyglass_wreck_sim/run.sh --override harness/skyglass_wreck_sim/overrides/candidate_compact.json \
    --variants geared,strong --runs 30 --out harness/skyglass_wreck_sim/results/candidate_compact.json

# Quick look at one floor (0-based), no retries:
harness/skyglass_wreck_sim/run.sh --floors 4 --variants strong --runs 5 --max-wipes 0

# Prove the rule probe changes nothing and runs are seed-deterministic:
harness/skyglass_wreck_sim/run.sh --probe-check --variants geared
```

Options: `--variants a,b` (player tiers, below), `--runs N`, `--seed S` (first seed), `--max-wipes N`
(retries before a run is abandoned; default 3), `--max-rounds N` per floor battle (default 150),
`--floors i,j`, `--no-barriers`, `--override file.json`, `--out file.json`.

Env: `TNR_ENGINE_SRC` (default `/home/claude/studie-tech/theninjarpg`, never modified),
`TNR_ENGINE_PIN` (default `c86f43f4e7ad468bc3673018423edca9fc48a1b1`, origin/main on 2026-10-26),
`TNR_ENGINE_WORK` (export dir, default `$TMPDIR/tnr_skyglass_wreck_sim`, outside the repo),
`TNR_DEPENDENCIES_APP` (reuse an install with byte-identical `bun.lock`/`package.json`; otherwise
`bun install --frozen-lockfile --ignore-scripts` runs once against the npm registry).

Speed: about 5-10 s of CPU per floor battle for tiers that survive; a 30-run baseline of a strong
tier takes 30-60 min on 2 cores. Candidate designs with 1-2 waves per floor are several times faster.

## What it does

`tools/build_baseline.py` resolves the dungeon and enemies from committed evidence into
`data/baseline.json` (`--check` verifies it is current):

- dungeon: `archive/spent-manifests/push-2026-10-25/263_skyglass_wreck_dungeon.json`
- AI rows (stats, pools, innate effects, jutsu rows with full jutsu records, items) and AI profiles:
  push/249 roster capture `harvests/inbox/tnr_results_1792900120886.json`
- push/250 Sentinel rules: the LIVE readback in `tnr_results_1792900236721.json` (verdict drift: the
  server added `effect: "damage"` to the fallback rule)
- push/251 crew kits/rules (verified match): manifest payload; Oathkeeper's added Weakening Strike row
  uses the record captured on Sealwright
- push/252 boss pools (verified match): replayed in-engine through the server's `scaleEditedAi`
- player jutsu: newest captured copy across `harvests/` and `answers/`

`engine/` (copied into the export and run with Bun):

- `model.ts` builds DB-shaped `CombatQueryUser` rows for enemies and players and applies overrides.
- `sim.ts` assembles each floor exactly as `initiateBattle` does for a dungeon (`capUserStats` on every
  participant, `processUsersForBattle` for the opening slice, `prepareEncounterWaves` for later waves,
  `extraState.encounter`/`extraState.dungeon`, pool-effect base adjust, `refreshMasteries`, aggressor,
  10% random initial barriers, the initiating player acts first) and then loops like
  `combat.performAction`: `advanceEncounterWave` -> `alignBattle` -> `performAIaction` ->
  `alignBattle` -> `advanceEncounterWave` -> `dungeonBattleOutcome`.
- `main.ts` plays whole runs as `routers/dungeon.ts` does (one battle per floor; waves share the
  floor's battle; a won floor restores everyone; a wipe revives everyone and returns the party to the
  tier's first floor) and aggregates.

`tools/apply_probe.py` adds one observation-only callback to the export's `ai_v2.ts` so the harness
can record which profile rule produced each action. `--probe-check` asserts identical outcomes with
the callback removed, and that the same seed reproduces the same run.

## Outputs (`--out`)

Per player tier: outcomes, wipes, total rounds, wall-clock minutes at 10/15/20 s per player turn with
AI turns at 0 s (server-side) and 1.5 s (animation allowance), plus 30 s per floor battle for the
lobby ready-up; per floor; per wave (`F<floor>W<wave>`): rounds median/min/max/p90, clears, wipes,
party HP lost %, pools left, damage share by enemy ("threats"), and per enemy in that wave: rule
fire counts (authored index, `engine-fallback` for the engine's appended backup/end-turn rules),
rules that never fired, actions used, damage dealt/taken/healed, effects applied, idle-or-move share,
when it died. Per player: actions, damage dealt/taken/healed, lowest HP %, downs.

## Override file (candidate designs)

All keys optional; the captured live state is the default for anything not named.

```json
{
  "name": "candidate", "note": "free text",
  "floors": [ { "kind": "floor", "waves": [ { "aiIds": ["Deck Warden", "Core Horror"], "delayRounds": 0 } ] } ],
  "enemies": {
    "Crowned Captain": { "hpScale": 0.5 },
    "Deck Warden": {
      "aiEdit": { "poolsMultiplier": 2 },
      "statScale": 0.8,
      "effects": [],
      "jutsuIds": ["UnQKfwq_JoRVu10aTX6Uv", "V3WrfQ3pB-eCq2hojsxWe"],
      "jutsuLevel": 1,
      "rules": [ { "conditions": [], "action": { "type": "use_highest_power_action", "effect": "damage", "target": "RANDOM_OPPONENT", "description": "" } } ],
      "includeDefaultRules": true
    }
  },
  "newEnemies": { "deckhand": { "base": "Deck Warden", "username": "Deckhand", "hpScale": 0.5 } },
  "jutsu": { "<new id>": { "...full jutsu record...": "" } },
  "players": { "mytier": { "stats": { "offence": 1300000, "defence": 1300000, "generals": 400000 },
                           "poolsMultiplier": 2, "damageGivenPct": 50, "damageTakenReductionPct": 30 } }
}
```

Enemies are named by AI id or username. `aiEdit` is replayed through `scaleEditedAi` like a Forge
AI edit (pools follow `poolsMultiplier`, stored pools clamp at 65,535). `hpScale` and `statScale` are
design knobs applied to the battle row (HP may exceed the stored-column cap in memory, as battles allow;
to ship it, it must be expressible as a real record). Floors: the engine fixes five floors per tier;
`DUNGEON_MAX_WAVES` is 5 per floor. Player tiers named in `players` that are not built in start from
`cap`.

## Player tiers

Defined in `engine/model.ts` (`PLAYER_VARIANTS`); all level-100 JONIN, same eight-jutsu kit at
level 25, driven by the engine's auto-combat with a declared rotation profile (`playerRules`):
`baseline` (the brief's even-spread level budget, no gear), `cap` (JONIN caps, no gear), `geared`,
`strong`, `elite` (gear stand-ins as innate battle tags plus a pools multiplier). Which tier is the
"average party" is a director decision; see `REPORT.md`.
