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
- `kit/live_jutsu_2026-11-11.jsonl`: live connector reads (2026-11-11) of the 35 PvP-relevant jutsu (my kit, every
  opponent action in my fight logs, saved opponent kits) whose live `updatedAt` was newer than the catalog copy; 300
  non-AI jutsu changed live since the 2026-10-23 bulk capture, 42 of them PvP-relevant, 7 already current. Engine
  fields only; `build_catalog.py` lays them on top. The remaining ~260 changed jutsu are still the Oct 23 copies: a
  full refresh needs the shell to reach the public catalog (www.theninjarpg.com is not on this session's network
  allowlist) or an operator-run Forge capture.
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

## Catalog refresh, gear and bloodlines (2026-11-11)
- `tools/fetch_catalog.py`: unauthenticated read-only public GETs on https://www.theninja-rpg.com (jutsu, items,
  bloodlines; visible records only, every page) into one `harvests/inbox` capture, then `build_catalog.py`. Hidden
  records are never asked for and `build_catalog.py` leaves out any it finds in a capture (RUL-2026-11-11-149). 2026-11-11:
  2,043 jutsu, 932 items, 101 bloodlines. Run between fights.
- Gear: the replay equips real worn gear (mine from `item.getUserItems`; opponents: the Kaeruun endgame set with
  Fortify III and a Subaku Mask) and bloodline rows; the engine folds gear into its pre-battle stage. Gear given
  points add to a base 60 (x(1+(60+g)/100)); gear DR points add to the 50% system DR (x(1-(50+dr)/100)), so 15 DR
  points cut incoming formula damage to 0.7x. Opponent gear varies, so `state/player/dauntless/tools/fit_gear.py`
  measures his totals from the logged hits (my hits -> his DR, his hits -> his given; pierce excluded) and stores
  `gearMods` in `kit/opponents/<id>.json`. Measured: Lzl3j0y given +72 / DR 0, Targaryen given +87 / DR 9.
- Fidelity after the fit: Targaryen every hit within 0-1% except his R1 Demons Strike (moved mid-turn, positions
  pinned) and his R5 Kunai (-32%); Lzl3j0y every hit within 0-9%. Opponent stats are at the caps (Night's
  Testament, a stat-driven pierce, logs a constant 631 against everyone).

## Replay fidelity (`tools/replay_fidelity.py`, 2026-11-11)
Replays a logged fight and compares the engine's HP loss per action with the logged "takes N damage" lines
(`trace: "effects"` in the request also dumps every live effect with power, level and powerPerLevel).
Targaryen (RUFKZ2jmaO, real kit): R1-R3 hits within 0-12% (Night's 631/631, Raimei Gen 594/587, Aetherion 788/821),
then R4 Ember 557/768 (-27%) and R5 Lotus 800/1811, Kunai 356/805 (-56%). The per-hit validator above stays at 1.9%
because it injects effect powers read from the log text; the replay recomputes them from records, so a stale record
compounds round over round. Lead: the harvested Chōha record grants -30% damage taken that the live R4 log does not
show (live: +30% given, +10 Water tag power). Confirmed live (Chōha updated 2026-11-08, no DR); after the live
refresh Lotus replays 1143/1811 (was 800), Kunai 508/805, Ember 557/768 unchanged. My kit's records are current, and
the engine's Clear strips every positive effect (as live did), so the remaining R4-R5 gap (x1.38-1.58) is outside the
records: likely live passives the harness lacks (bloodline effects, gear, keystone, trained-element +15%). Next:
anchor replayed effect powers to the logged text. Demons Strike R1 replays for 0 (603 logged; he moved from (4,4) during that turn, positions are pinned).
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
