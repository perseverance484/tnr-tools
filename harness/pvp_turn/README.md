# PvP turn simulator on the TNR engine (offline)

Gives the dauntless PvP planner (`state/player/dauntless/tools/turn.py`) **exact one-turn outcomes** from the
game's own combat code instead of a hand-built approximation. Director-authorised 2026-11-11 ("Build the
offline harness for the planner"). No live requests: the engine runs in-process under Bun with socket
syscalls denied (`harness/ghost_ship_final/tools/offline_exec.py`, seccomp mode by default).

## Replay mode (default in turn.py since 2026-11-11)
`engine/replay_sim.ts` rebuilds the fight by replaying **every logged action of both sides** through the engine with
the real records from the offline catalog (`kit/catalog.json`, see Data). No record is fetched during a fight
(director, 2026-11-11: "No mid battle lookups or estimations"): an action id missing from the catalog prints
`CATALOG GAP` and is filled between fights.
The engine therefore holds every effect itself: seals (bloodline *effects*, not jutsu), time compression/dilation
(applies from the round after it is cast), barriers, ground effects, prevents, stuns, potency changes, heal-over-time,
cooldowns and shared locks. HP and positions are restored from the live battle after the replay.
- `list` mode → my AP and every available action with its engine cost; `turn.py` drops bundles the engine rejects.
- `eval` mode → each candidate bundle, then his reply bundles, most damaging first, up to 40: `typical` (median) and
  `best` (worst case for me). His kit is REAL when `kit/opponents/<userId>.json` was saved before the fight
  (`state/player/dauntless/tools/opponent_kit.py` from `jutsu.getPublicUserJutsus`: equipped jutsu and their real
  levels; no stand-in at all). Without it `turn.py` prints `his kit: ESTIMATED` and the calibrated stand-in fills his
  unseen moves. Items are not public (`item.getPublicUserItems`: "You can only view your own items"); items he uses
  resolve from the catalog by their logged id.
- `turn.py` scores the python top 6 plus the best Cleanse / Smoke / Clear bundles this way (~7 s per turn).
Director rationale (2026-11-11): "Dont just model the damage formula, model *everything*" — after a fight where the
text parser dropped seal, compression, a barrier, a potency debuff and heal-over-time.
Known gaps: some enemy self-heal records fail targeting (Cellular Regeneration), replay RNG (stun/seal rolls) can
differ from the live log, summons are stripped.

## What it runs (turn_sim.ts, tag-injection mode, kept for calibration/validation)
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
- `kit/catalog.json` (gitignored, rebuilt by `tools/build_catalog.py`, no live calls): every full jutsu/item record
  captured under `harvests/`, newest copy per id, with `kit/records.json` and `kit/live_overrides.json` laid on top.
  2026-11-11: 2,492 records (1,719 jutsu, 773 items); all 15 of Targaryen's equipped jutsu were present.
  `engine_bridge._records()` reads it (built on first use if missing).
- `kit/opponents/<userId>.json`: an opponent's equipped jutsu kit and levels saved before the fight.
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

## Replay fidelity (`tools/replay_fidelity.py`, 2026-11-11)
Replays a logged fight and compares the engine's HP loss per action with the logged "takes N damage" lines
(`trace: "effects"` in the request also dumps every live effect with power, level and powerPerLevel).
Targaryen (RUFKZ2jmaO, real kit): R1-R3 hits within 0-12% (Night's 631/631, Raimei Gen 594/587, Aetherion 788/821),
then R4 Ember 557/768 (-27%) and R5 Lotus 800/1811, Kunai 356/805 (-56%). The per-hit validator above stays at 1.9%
because it injects effect powers read from the log text; the replay recomputes them from records, so a stale record
compounds round over round. Lead: the harvested Chōha record grants -30% damage taken that the live R4 log does not
show (live: +30% given, +10 Water tag power). Next: anchor replayed effect powers to the logged text and flag record
drift. Demons Strike R1 replays for 0 (603 logged; he moved from (4,4) during that turn, positions are pinned).
Element access fixed in the same pass: three-element kits (bloodline + two innate) get two innate slots plus an
unlocked trained basic element (engine `elementalMastery.ts`), which made Raimei Gen and Thunder's Judgement castable.

## Limits (declared)
- Opponent kit: real equipped jutsu when saved before the fight (see Replay mode); otherwise the calibrated stand-in
  (`engine_bridge.enemy_kit`), flagged ESTIMATED. Opponent items, gear and bloodline passives are not public.
- Gear/armor modifiers are folded into the +33% passive; no per-item gear model.
- Summons are not assembled (they need DB templates); `turn.py` keeps its own summon handling.
- One turn deep: the planner's 1-round lookahead, reserves and guards stay in Python on top of the engine ply.

## Use
`turn.py` calls `engine_bridge.evaluate` on its 12 best bundles every turn (about 2–4 s) and prints
`engine: exact (...)`, or falls back to its own simulator if the engine is unavailable (`--no-engine` to skip).
Manual: `harness/pvp_turn/run.sh REQUEST.json` (schema in `engine/turn_sim.ts`).
