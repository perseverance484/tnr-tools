# Skyglass Wreck dungeon simulator (offline, engine-driven)

Runs the Skyglass Wreck's real fights through The Ninja RPG's own combat engine, in memory,
to time a 3-player clear against the 60-minute dungeon limit (`DUNGEON_RUN_SECONDS = 3600`)
and to tune enemies and waves before anything is pushed. Zero live requests, no credentials:
the engine is a `git archive` export of a local game clone, run in a socket-denied child
(`harness/ghost_ship_final/tools/offline_exec.py`: `unshare -rn` plus seccomp).

Results and findings: `REPORT.md` (its first section, the 2026-10-30 final pass, is current). Raw results: `results/*.json`.

**Rule cap and law-40 gates (2026-10-31, `fable/skyglass-rule-cap`; REPORT.md first section).** Every runner fails a battle
or a spec with an AI over the server's 20-rule cap (`engine/rulecap.ts`; `--allow-over-cap` only to reproduce pre-trim
rule sets) and sets every `distance_lower_than` on a rule casting a shared-pool jutsu to range + 1 (`engine/gates.ts`,
from `32b_DATA_pool.json`; `--old-gates` for the previous gates). Outputs carry `ruleCap` and `gates` blocks. Tables:
`python3 tools/rulecap_tables.py`, `python3 tools/rulecap_haul.py label=file,...`.

**Final pass (`results/final_*.json`, tables: `python3 tools/final_tables.py`).** Every runner (`main.ts`, `hunts_main.ts`,
`charts_main.ts`, `haul_main.ts`, `crownhold.ts`) takes:
- `--audit-fallback /abs/out.json`: a static per-enemy, per-phase audit of fallback rules (RUL-2026-10-29-046);
- `--no-fallback-fix`: rebuilds the pre-fix rules.

Each runner also writes a `fallbackGuard` block (set pieces cast without their marker) into its output.
`tools/economy_inputs.py` and `tools/economy.py` turn the measured clear rates and run lengths into a 12-hour weekend
economy. The Haul has no steeping (RUL-2026-10-29-056); the steeped-page commands below are historical.

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
# Chain-tuned (RUL-2026-10-28-013): the player brings one modelled pet (--no-pet to drop it) and reads each telegraph
# with probability --read (report 4 uses 0.85). The whole pyramid per route policy, pools carried:
TNR_SCRIPT=crownhold.ts harness/skyglass_wreck_sim/run.sh --read 0.85 --chain 16 --policies clean,alert,healing,war \
    --out $PWD/harness/skyglass_wreck_sim/results/crownhold_chain.json
# Per-fight tables at full pools (fast), then an offline chain estimate from them (tuning surrogate only):
TNR_SCRIPT=crownhold.ts harness/skyglass_wreck_sim/run.sh --read 0.85 --table all --hps 1 --variants none,alarm,war \
    --seeds 20 --shard 0/2 --out /abs/table_0.json   # and --shard 1/2 in a second process
python3 harness/skyglass_wreck_sim/tools/compose_chain.py /abs/table_0.json /abs/table_1.json [--reg-scale ...] [--war-restore N]

# Boss-fight mechanic probes (two-marker chain, weakness window, ring/bell, Chain Hook, barriers):
TNR_SCRIPT=probe_boss.ts harness/skyglass_wreck_sim/run.sh --out harness/skyglass_wreck_sim/results/probe_boss.json

# Shared set-piece library (engine/library.ts) -> library_spec.json, and its marker / minor-mark probes:
TNR_SCRIPT=build_library.ts harness/skyglass_wreck_sim/run.sh
TNR_SCRIPT=probe_library.ts harness/skyglass_wreck_sim/run.sh --out harness/skyglass_wreck_sim/results/probe_library.json
# Rule audit for one enemy: why each authored rule did or did not fire (read-only hook before each AI decision):
TNR_SCRIPT=audit_rules.ts harness/skyglass_wreck_sim/run.sh --override harness/skyglass_wreck_sim/overrides/kits_endgame.json \
    --floor 4 --enemy "The Captain" --runs 30 --pets --together "Steady the Helm|Raise the Gunwale|Omen:" \
    --out harness/skyglass_wreck_sim/results/audit_captain_endgame.json
#   --phase-hp N (default 50) splits each appearance into phase 1 / phase 2 at his first decision below N% health:
#   medians, p90, his health at that decision, and per-appearance rows (`perAppearance`). --together "a|b|c" checks that
#   rules whose notes contain a, b and c first fire in the same round (the Captain's transition turn).
#   actionsByPhase counts every action the enemy took, by name, in each phase.
# Delayed GROUND damage probe (elementaldamage, damage over rounds, poison/wound/afterburn/drain):
TNR_SCRIPT=probe_ground.ts harness/skyglass_wreck_sim/run.sh --out harness/skyglass_wreck_sim/results/probe_ground.json

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
`--no-dodge` turns off the harness dodge (below). `--pets` gives each player one modelled companion (below).

**Pets (`--pets`, `model.ts petFor`).** No pet record exists in the committed captures, so each player brings a
modelled mid-rank companion: pet rank = half the owner's maximum (JONIN owner: rank 5, level 30; CHUNIN owner: rank 3,
level 15), stats at half the caps of the matching character rank, species COMMON / ASSAULT, no jutsu, the engine's
default pet rules. They enter through the engine's own pet path (`processUsersForBattle` `petPreload`), and the
harness re-seats each beside its owner's redrawn spawn cell.

**Dodging (harness auto-player, not engine behaviour).** At a player's turn, if they stand on a hex an
enemy marked `tg_heavy` / `tg_control`, or in a `tg_linger` pool, or an arena-wide mark is up (`tg_safe`
stars exist) and they are not on a star, they walk (engine basic Move, one hex per action, at most 3) to
the nearest free acceptable hex. While marks are up, their "close in" move becomes a one-hex step that
never enters a marked hex, and an explicit end of turn keeps the engine's appended backup rules from
walking them back in. Counts (threatened / dodged / failed: rooted or stunned, no free hex in reach)
are in each variant's `dodge` block.

**Determinism.** Each run seeds Math.random (combat rolls, spawn redraw) and, separately, the id entropy the engine
draws from crypto.getRandomValues through nanoid (`seedEntropy`), so a seed reproduces a run even with clones or
summons on the field. The wall clock is virtual (`seedClock` / `tickClock`: a fixed epoch per run, +1 s per action),
because the engine's 60 s round timer otherwise made outcomes depend on machine load. Pets' engine-drawn cells are
cleared before they are re-seated (the engine draws spawn cells with unseeded node:crypto). `--probe-check` runs each
seed twice plus once with the rule probe removed and compares actions, HP changes and positions.

**Kits (`engine/kits.ts`, `engine/kitlib.ts`, `engine/build_kits.ts`).** The dungeon copies (ids `dg-*`,
placeholders), their dungeon-only jutsu and priority rules are built in code from captured shape donors
and checked against the live `JutsuValidator`, `AiRule` and `insertAiSchema` while building. Tuning
knobs live in a params JSON (pools, +100% damage rows, move powers). The override also carries
`signatures` (rule indices per AI); `main.ts` reports per enemy `signatureFiredPct` (appearances in
which a signature rule fired) and `idleTurnsAfterRound2Pct` (turns from the enemy's 3rd round in its
wave with nothing but move / end turn).

**The Captain's phases (RUL-2026-10-28-031 / -032).** Phase 1 (above 50%) is a duel. His first turn below 50% is the
transition: Steady the Helm (`lib-steady-the-helm`, 20 AP: cleanse, 40% decreasedamagetaken and 40% absorb for 2 rounds,
clearprevent), Raise the Gunwale (20 AP) and the first deck mark (40 AP) in one turn; 80 AP so that it also fits under a
20-AP player stun, which cleanse cannot lift. Battle Trance follows in the AP after a later mark. His last rule is the basic attack by name (`use_specific_jutsu` with the engine's
`basicAttack` action id), not `use_highest_power_action`, which cast Broadside unmarked in phase 1. Check it with
`audit_rules.ts --together` (above) and its `actionsByPhase` tally; findings in `REPORT.md` reports 4d and 4e.

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

## The Haul (S-rank profession charts)

`engine/haul.ts` (params, hazards, fights per state, quest state-graph generator), `engine/haul_main.ts` (runner),
`tools/haul_payout_fit.py` (payout fit), `tools/haul_tables.py` (tables). Quest graphs: `haul_spec.json`. Results:
`results/haul_*.json` (settings and params embedded). Rulings: RUL-2026-10-29-037, -038, -044.

**Payout (RUL-2026-10-29-044).** Chests are guaranteed. Each choice adds haul points (millions of chest value): a crate
the step's points, a locker the step's points + the page's locker points, a cut the step's points minus the cut penalty
(a step-4 cut drops to Common: -2). A run pays the profession ladder's highest rung its points reach:

- Hunter: C 4.2 / R 6.1 / C+C 8.4 / C+R 10.3 / R+R 12.2 / C+L 15.7 / R+L 17.6 / C+R+L 21.8 / L+L 23.0 / C+L+L 27.2
- Gatherer: C 3.2 / R 4.9 / C+R 8.1 / R+R 9.8 / L 10.5 / C+L 13.7 / R+L 15.4 / C+R+L 18.6 / L+L 21.0 / C+L+L 24.2

Points are order-free, so the quest state is (step, alertness 0..3, pending cut, points): every quest is a few dozen
dialog choices, one battle per (state, crate|locker), and one ending per rung reached (all 30 quests 57-83 objectives).
Steeped pages pay the same rungs one tier higher with a 40% bonus chest each (Picked clean: one tier lower, each at 60%).
The step and locker points were fitted (`haul_payout_fit.py`) to the simulated clear rates: sensible run about 7.5M,
no route more than ~20% above it, timid clearly less, a greedy clear worth ~3x the old S-rank payout (RUL-2026-10-29-045).

**Results (exact per-seed runs, 40 seeds, L100 Kitsune + pet; "clear % / EV M", dodge on, dodge off in brackets).**
Round 2 (RUL-2026-10-29-045): Snare Room extra guard on the step-2 locker only, its crate snares at steps 2-4 and
hazards x1; Ore Vault one guard fewer at steps 4-5; top rungs raised so a greedy clear pays ~3x; cut-through hazards:
drain (hunters) / elementalseal (gatherers) on the next fight.

| Page | Timid CC | Sensible CLC | Best 3-step 1-locker | Greedy (most likely 5-step, 3+ L route) | Deep crates CCCCC | Best named route (vs sensible) |
|---|---|---|---|---|---|---|
| trophy | 100% / 4.2 (off 97.5% / 4.1) | 87.5% / 7.3 (off 67.5% / 5.7) | CLC 87.5% / 7.3 | LCLLC 37.5% (off 0%), clear pays 21.8, EV 8.2, 6 min | 70% / 8.5 (off 47.5% / 5.8) | CCCCC 70% / 8.5 (116%) |
| bone | 100% / 4.2 (off 100% / 4.2) | 85% / 7.1 (off 62.5% / 5.2) | LCC 87.5% / 7.3 | LLLCC 22.5% (off 0%), clear pays 21.8, EV 4.9, 6.3 min | 50% / 6.1 (off 25% / 3.0) | LCL 85% / 8.8 (119%) |
| snare | 100% / 6.1 (off 95% / 5.8) | 70% / 7.2 (off 32.5% / 3.4) | CCL 82.5% / 8.5 | LCXLL 35% (off 0%), clear pays 21.8, EV 7.6, 5.8 min | 20% / 2.4 (off 15% / 1.8) | LCL 80% / 9.8 (115%) |
| overgrown | 90% / 4.4 (off 97.5% / 4.8) | 92.5% / 7.5 (off 95% / 7.7) | CLC 92.5% / 7.5 | LLLCC 37.5% (off 27.5%), clear pays 21.0, EV 7.9, 6.5 min | 37.5% / 5.8 (off 47.5% / 7.3) | LLLCC 37.5% / 7.9 (105%) |
| vault | 97.5% / 4.8 (off 95% / 4.7) | 70% / 7.3 (off 67.5% / 7.1) | LCC 72.5% / 7.6 | CLLLC 32.5% (off 10%), clear pays 15.4, EV 5.0, 6.8 min | 80% / 7.8 (off 85% / 8.3) | CCXL 87.5% / 9.2 (121%) |
| bloom | 90% / 4.4 (off 92.5% / 4.5) | 90% / 7.3 (off 87.5% / 7.1) | CLC 90% / 7.3 | LLLCC 32.5% (off 17.5%), clear pays 21.0, EV 6.8, 6.5 min | 30% / 4.6 (off 25% / 3.9) | CLL 97.5% / 7.9 (108%) |

| Page | Points: crate by step | Locker + | Cut - (step 4) | Lockers at | Cuts at | Objectives: base / rot / flood / alarmed / picked (choice-battle-ending) |
|---|---|---|---|---|---|---|
| trophy | 4.2 / 0.9 / 1.3 / 3 / 5.4 | 2.4 | 2 | 1,2,3,4,5 | 3,4 | 76 (22-44-10) / 76 / 76 / 77 / 76 |
| bone | 4.2 / 0.9 / 1.3 / 1.2 / 7.3 | 2.5 | 2 | 1,2,3 | 3,4 | 57 (21-27-9) / 57 / 57 / 77 / 57 |
| snare | 5.2 / 0.9 / 1.5 / 1.2 / 3.5 | 3.3 | 2 | 1,2,3,4,5 | 2,3,4 | 83 (24-48-11) / 83 / 83 / 83 / 83 |
| overgrown | 3.7 / 1.4 / 1.9 / 2.5 / 8.6 | 1.1 | 2 | 1,2,3,4,5 | 3,4 | 76 (22-44-10) / 76 / 76 / 77 / 76 |
| vault | 4.5 / 1.9 / 2.2 / 0.6 / 0.6 | 1.9 | 2 | 1,2,3,4,5 | 3,4 | 75 (22-44-9) / 75 / 75 / 77 / 75 |
| bloom | 4.1 / 0.9 / 1.9 / 4.2 / 5.7 | 1.4 | 2 | 1,2,3,4,5 | 3,4 | 75 (22-44-9) / 75 / 75 / 76 / 75 |

Steeping (best route EV of the steeped page / the base page, dodge on; weights 30/25/25/20): Rot-soaked 1.44-1.75x,
Flooded hold (rooted 3 rounds on hunter pages, 2 on gatherer pages) 0.78-1.41x, Alarmed 1.54-1.75x, Picked clean
0.40-0.59x; the roll: trophy 1.37x, bone 1.23x, snare 1.36x, overgrown 1.15x, vault 1.12x, bloom 1.17x.

```bash
# Every legal path of every base page, state-merged (40 particles per state):
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --exhaustive --variants base --seeds 40 --out results/haul_base_dodge.json
# The 24 steeped pages (layout+modifier):
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --exhaustive --variants mods --seeds 24 --out results/haul_mods_dodge.json
# Exact per-seed simulation of named routes (shared prefix tree), dodge on / off:
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --paths CC,CLC,LCC,CCCCC,CLLLC,LLLCC --variants base --seeds 40 --out results/haul_exact_dodge.json
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --paths CC,CLC,LCC,CCCCC,CLLLC,LLLCC --variants base --seeds 40 --no-dodge --out results/haul_exact_nododge.json
# Payout fit (offline: fights do not depend on the payout), then recompute haul values of a results file:
python3 harness/skyglass_wreck_sim/tools/haul_payout_fit.py results/haul_base_dodge.json --exact results/haul_exact_dodge.json
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --revalue "$PWD/harness/skyglass_wreck_sim/results/haul_mods_dodge.json" --out results/x.json
# Calibration / probes / determinism / spec:
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --fights --variants trophy --seeds 8      # each fight state from full HP
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --solo h-veteran,trophy-warden --seeds 6  # guard strength alone
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --probe-hazards --variants trophy,overgrown --seeds 6
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --repro trophy@CLLCL@5
TNR_SCRIPT=haul_main.ts harness/skyglass_wreck_sim/run.sh --spec-out harness/skyglass_wreck_sim/haul_spec.json
python3 harness/skyglass_wreck_sim/tools/haul_tables.py results/haul_base_dodge.json results/haul_mods_dodge.json --exact results/haul_exact_dodge.json
```

Variants: `base` (6 pages), `mods` (24 steeped pages), `all`, or a list such as `trophy,overgrown+rot`. `--set=path.to.knob=json`
overrides one param for a quick probe. Every fight is seeded by (page, seed, state) through the virtual clock
(`seedEntropy` -> `seedClock`); `--repro` reruns a path twice and compares actions, positions (pets included) and HP.
The state-merged evaluation gives each path the pooled HP of its state (about +-15 points per path); the exact runs
are the reference for the named routes.
