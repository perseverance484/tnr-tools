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
harness/skyglass_wreck_sim/run.sh --probe-check --variants average

# Player-strength check: one player vs The Captain, solo, plain QUEST battle (60 seeds):
TNR_SCRIPT=calibrate.ts harness/skyglass_wreck_sim/run.sh --seeds 60 \
    --out harness/skyglass_wreck_sim/results/calibration_solo_captain.json

# Mechanics probes (movement / summon / ground AOE / barrier / clone jutsu on an AI enemy):
TNR_SCRIPT=probe_mechanics.ts harness/skyglass_wreck_sim/run.sh --seeds 3 --rounds 6 \
    --out harness/skyglass_wreck_sim/results/probe_mechanics.json
python3 harness/skyglass_wreck_sim/tools/probe_summary.py harness/skyglass_wreck_sim/results/probe_mechanics.json

# Telegraphed-boss probes (ground marks, self markers, COORDINATES patterns, grid/spawns, summoning an AI record):
TNR_SCRIPT=probe_telegraph.ts harness/skyglass_wreck_sim/run.sh --out harness/skyglass_wreck_sim/results/probe_telegraph.json

# Crownhold bosses on the shared set-piece library (engine/cclib.ts, engine/library.ts; REPORT_crowned_captain.md).
# The Crowned Captain solo, dodge on/off, writes his build spec:
TNR_SCRIPT=crowned_captain.ts harness/skyglass_wreck_sim/run.sh --seeds 60 \
    --out $PWD/harness/skyglass_wreck_sim/results/crowned_captain_tuned.json \
    --write-spec $PWD/harness/skyglass_wreck_sim/crowned_captain_spec.json
# The three division commanders solo, and the whole isolated pyramid with pools carried (route policies):
TNR_SCRIPT=crownhold.ts harness/skyglass_wreck_sim/run.sh --solo 60 \
    --out $PWD/harness/skyglass_wreck_sim/results/crownhold_commanders_solo.json \
    --write-spec $PWD/harness/skyglass_wreck_sim/crownhold_spec.json
TNR_SCRIPT=crownhold.ts harness/skyglass_wreck_sim/run.sh --chain 20 --policies clean,alert,healing,war \
    --out $PWD/harness/skyglass_wreck_sim/results/crownhold_chain.json

# Boss-fight mechanic probes (two-marker chain, weakness window, ring/bell, Chain Hook, barriers):
TNR_SCRIPT=probe_boss.ts harness/skyglass_wreck_sim/run.sh --out harness/skyglass_wreck_sim/results/probe_boss.json

# Build the designed dungeon-copy kits (engine/kits.ts) into an override + build_spec.json section:
TNR_SCRIPT=build_kits.ts harness/skyglass_wreck_sim/run.sh \
    --params harness/skyglass_wreck_sim/overrides/kits_endgame.params.json
harness/skyglass_wreck_sim/run.sh --override harness/skyglass_wreck_sim/overrides/kits_endgame.json \
    --variants average --runs 60 --out harness/skyglass_wreck_sim/results/kits_endgame.json
#   add --no-dodge to switch off the auto-player's dodge of marked hexes
# Level 40-60 version (level-50 copies, lighter kits; the lvl50/lvl40/lvl60 player tiers):
TNR_SCRIPT=build_kits.ts harness/skyglass_wreck_sim/run.sh --version lvl50 \
    --params harness/skyglass_wreck_sim/overrides/kits_lvl50.params.json
harness/skyglass_wreck_sim/run.sh --override harness/skyglass_wreck_sim/overrides/kits_lvl50.json \
    --variants lvl50 --runs 60 --out harness/skyglass_wreck_sim/results/kits_lvl50.json

# Trace one floor action by action (absolute override path; TNR_DODGE=0 turns dodging off):
TNR_SCRIPT=trace_floor.ts harness/skyglass_wreck_sim/run.sh 1 "$PWD/harness/skyglass_wreck_sim/overrides/director_layout.json" average 1
```

Options: `--variants a,b` (player tiers, below), `--runs N`, `--seed S` (first seed), `--max-wipes N`
(retries before a run is abandoned; default 3), `--max-rounds N` per floor battle (default 150),
`--floors i,j`, `--no-barriers`, `--override file.json`, `--out file.json`,
`--dmg-config live|default|file.json` (default `live`, see below).
`--no-dodge` turns off the harness dodge (below).

**Dodging (harness auto-player, not engine behaviour).** At a player's turn, if they stand on a hex an
enemy marked `tg_heavy` / `tg_control`, or in a `tg_linger` pool, or an arena-wide mark is up (`tg_safe`
stars exist) and they are not on a star, they walk (engine basic Move, one hex per action, at most 3) to
the nearest free acceptable hex. While marks are up, their "close in" move becomes a one-hex step that
never enters a marked hex, and an explicit end of turn keeps the engine's appended backup rules from
walking them back in. Counts (threatened / dodged / failed: rooted or stunned, no free hex in reach)
are in each variant's `dodge` block.

**Determinism.** Each run seeds Math.random (combat rolls, spawn redraw) and, separately, the id entropy the engine
draws from crypto.getRandomValues through nanoid (`seedEntropy`), so a seed reproduces a run even with clones or
summons on the field. `--probe-check` verifies it.

**Kits (`engine/kits.ts`, `engine/kitlib.ts`, `engine/build_kits.ts`).** The dungeon copies (ids `dg-*`,
placeholders), their dungeon-only jutsu and priority rules are built in code from captured shape donors
and checked against the live `JutsuValidator`, `AiRule` and `insertAiSchema` while building. Tuning
knobs live in a params JSON (pools, +100% damage rows, move powers). The override also carries
`signatures` (rule indices per AI); `main.ts` reports per enemy `signatureFiredPct` (appearances in
which a signature rule fired) and `idleTurnsAfterRound2Pct` (turns from the enemy's 3rd round in its
wave with nothing but move / end turn).

**Damage settings.** Every simulated battle carries `battle.extraState.dmgConfig`, which
`process.ts` reads before its code defaults. The harness default is the LIVE config in
`data/dmg_config_live.json` (`misc.getDmgConfig`, read in game by the director on 2026-10-28:
`curve 2, gen_weight 1, advantage_min 0`; code defaults are `1.6, 2, 0.01`). `--dmg-config default`
reproduces the first (2026-10-26) report, which ran on code defaults.

Env: `TNR_ENGINE_SRC` (default `/home/claude/studie-tech/theninjarpg`, never modified),
`TNR_ENGINE_PIN` (default `c86f43f4e7ad468bc3673018423edca9fc48a1b1`, origin/main on 2026-10-26),
`TNR_ENGINE_WORK` (export dir, default `$TMPDIR/tnr_skyglass_wreck_sim`, outside the repo),
`TNR_DEPENDENCIES_APP` (reuse an install with byte-identical `bun.lock`/`package.json`; otherwise
`bun install --frozen-lockfile --ignore-scripts` runs once against the npm registry).

Outputs also give, per enemy, `ruleFireDist`: for each authored rule, how many appearances fired it never /
exactly once / more than once.

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
- player gear: the Kitsune armour set from the push/204 capture `harvests/inbox/tnr_results_1792629744565.json`
  (Mask HEAD, Armor CHEST, Gauntlets HAND, Belt WAIST, Pants LEGS, Tabi-Shoes FEET; Pants-F is an identical
  alternate LEGS piece). Worn as real equipped item rows, so `processUsersForBattle` realises their effects
  (fromType `armor`) and folds the percentage damage modifiers into the engine's pre-battle gear pools.
- summon templates: any summon effect's `aiId` must be a captured AI; the harness pre-seeds the engine's own
  `summonTemplateCache` with those rows, so summons run without a database.

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

Defined in `engine/model.ts` (`PLAYER_VARIANTS`), driven by the engine's auto-combat with a declared
rotation profile (`playerRules`: self-buffs when ready, each attack jutsu when off cooldown and in range,
close in, basic attack). Ids contain `user_`, so `ai_v2` treats them as players.

- **`average`** (director 2026-10-28, the endgame party member): level-100 JONIN, stats at the JONIN caps
  (offence/defence 1.3M, generals 400k; masteries an even split of the 4.2M total, they only gate jutsu),
  the full Kitsune armour set, Fire/Wind elements, 9 PvE-usable jutsu at the Jonin level cap 25
  (`ENDGAME_PLAYER_KIT`: Chakra Overflow, Typhon Burst, Tempestual Fury, Burning Coil, Gale Force Blast,
  Scorching Sun Strike, Wind Style: Sky Dragon, Phoenix Flame Strike, Stunning Jab). Elite Jonin's
  level 30 cap applies only to ELITE JONIN-rank jutsu, so it does not apply.
- **`noarmor`**: `average` without the Kitsune set (reference).
- Earlier ladder kept for reference (8-jutsu non-elemental kit): `baseline`, `cap`, and `geared`/`strong`/`elite`,
  whose gear knobs now enter as one synthetic ARMOR row (`gearMode: "armor"`, the engine's gear pools;
  `"innate"` reproduces the first report's bloodline-type tags, which the engine skips for damage effects
  that disallow bloodline modifiers).
- Level 40-60 version: `lvl40`, `lvl50`, `lvl60` (CHUNIN, level budget, Chunin kit); enemy `level` overrides.

Variant fields (override `players`): `level`, `rank`, `statBudget`, `stats`, `poolsMultiplier`,
`damageGivenPct`, `damageTakenReductionPct`, `gearMode`, `gearItemIds`, `elements`, `jutsuIds`, `jutsuLevel`, `rules`.
