# PvP turn simulator on the TNR engine (offline)

Gives the dauntless PvP planner (`state/player/dauntless/tools/turn.py`) **exact one-turn outcomes** from the
game's own combat code instead of a hand-built approximation. Director-authorised 2026-11-11 ("Build the
offline harness for the planner"). No live requests: the engine runs in-process under Bun with socket
syscalls denied (`harness/ghost_ship_final/tools/offline_exec.py`, seccomp mode by default).

## What it runs
`engine/turn_sim.ts` assembles a COMBAT battle through the engine's `processUsersForBattle`
(via `engine/lib/`, a copy of `harness/ghost_ship_final/engine/lib` ported to the upstream module layout:
`alignBattle`/`calcApReduction` from `combat/turn.ts`, `refreshMasteries` from `combat/mastery.ts`), injects the
live tags rebuilt from the battle log as engine effects, sets HP/positions/cooldowns, then fires each
candidate bundle through `availableUserActions` → `performBattleAction` (legality, AP, range, cooldowns, shared
locks, damage pipeline, absorb/reflect/parry/lifesteal, Clear/Cleanse, shields, pierce) followed by each
enemy reply option.

## Engine version
Upstream `studie-tech/theninjarpg` `main` at **df864509f** (2026-11-10). The older pin 107d7a868 lacks the
live `parry` tag, so it cannot simulate Parry. Re-export when upstream moves:
```sh
git -C $GAME fetch origin && mkdir -p $WORK/engine && git -C $GAME archive origin/main app | tar -x -C $WORK/engine
(cd $WORK/engine/app && bun install --frozen-lockfile --ignore-scripts)   # user-approved dependency install
echo $WORK/engine/app > harness/pvp_turn/.engine_app                       # local pointer (gitignored)
```

## Data
- `kit/records.json`: newest captured full record of every PvP kit action (`tools/extract_kit.py` from
  `harvests/inbox`), with `kit/live_overrides.json` merged over the 9 records whose live `updatedAt` was newer
  (connector reads 2026-11-11).
- `kit/dauntless_profile.json`: live stats and jutsu levels (Rebirth 10, Thunder's 8, Eclipse 8, Parry 3,
  Shrapnel 2, the rest 25).

## Calibration (see results/)
Both sides at engine jonin caps plus a **+33% damage-given passive** each (gear/keystone/elemental boost the
harness user lacks). Fitted on 10 moves vs logged medians: mean abs error 3.0% over the 8 moves with n ≥ 3;
pierce exact (Night's 631/631, Stormblade 707/707).
Out of sample (`tools/validate_engine.py`, every logged turn of mine replayed with that turn's live tags):
33 comparable turns, **median abs error 1.8%**, 22 within 10%. Misses: AoE turns where a summon soaked damage
(Korin R6), and replays the validator could not place (15 illegal: repeated steps onto one tile, consumables
aimed at the wrong tile, cooldowns from older fight states). `results/validation.json` has every row.

## Limits (declared)
- Opponent kit is a calibrated stand-in (`engine_bridge.enemy_kit`) sized to the logged enemy hit/turn/burst,
  plus his real Night's Testament, Elite Smoke Bomb and Clear while available. His real records are unknown
  until he uses them.
- Gear/armor modifiers are folded into the +33% passive; no per-item gear model.
- Summons are not assembled (they need DB templates); `turn.py` keeps its own summon handling.
- One turn deep: the planner's 1-round lookahead, reserves and guards stay in Python on top of the engine ply.

## Use
`turn.py` calls `engine_bridge.evaluate` on its 12 best bundles every turn (about 2–4 s) and prints
`engine: exact (...)`, or falls back to its own simulator if the engine is unavailable (`--no-engine` to skip).
Manual: `harness/pvp_turn/run.sh REQUEST.json` (schema in `engine/turn_sim.ts`).
