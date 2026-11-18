# The Flooded Stores build (Isonade + the looting crew)

Build-and-test output for the Stolen Stores weekend (design approved Nov 18, doc rev 33). Offline only: zero live
requests, nothing uploaded, created or unhidden. Every stage below needs the director's go before it runs.

## Files

- `harness/isonade.ts`, `harness/stores.ts`, `harness/stores_main.ts`: new runners for the Skyglass Wreck harness. They
  drop into `harness/skyglass_wreck_sim/engine/` on `fable/mother-of-echoes-act3` @ 11041772 (not on main) and import
  its modules unchanged. Engine: game pin 3314d122.
- `isonade_spec.json`, `isonade_results.json`: Isonade and the Grasping Arm records and the 30-seed fight results.
- `isonade_params_v2.json`, `isonade_spec_v2.json`, `isonade_results_v2*.json`: the Nov 18 fix (push/645). Isonade's
  warnings never overlap or lapse (innate stunprevent, slam and Black Water lands 70 AP, Black Water omens 50 AP, the
  bitten run ends on Slam III, third Black Water below 33%) and it is harder (slam 560, Black Water 640, brine 12%,
  bitten brine 3 rounds, pools x8.4). Run with `--params <abs>/isonade_params_v2.json`; with no params the harness
  reproduces v1. `_timecompression` adds `--tc 1`, `_goodplayer` uses the "good" pool policy.
- `stores_spec.json`, `stores_results.json`: the crew records (fs-* only; chart-* rows are the harness's own) and the
  30-seed results for The Flooded Stores fights 1-3 and the two beach fights.
- `flooded_stores_build.gen.py` -> `manifests/1_strips_and_jutsu.json` .. `4_ais.json`. Do not hand-edit.
- Animation strips: `art/isonade_anims/` (README there lists the weak spots).

## Commands (W=/root/isowork; worktree at the fable commit above, game checkout at the pin)

```
cd $W/wt && TNR_ENGINE_SRC=$W/game/tnr TNR_ENGINE_PIN=3314d122c93e036618483d18229a793ad7ad21fd TNR_ENGINE_WORK=$W/engwork \
  TNR_SCRIPT=isonade.ts harness/skyglass_wreck_sim/run.sh --seeds 30 --read 1,0.85 --write-spec <abs>/isonade_spec.json --out <abs>/isonade_results.json
... TNR_SCRIPT=stores_main.ts harness/skyglass_wreck_sim/run.sh --variants L100,L100noarmor,L50kit,L50 --runs flooded,beachDeckhand,beachMate --seeds 30 --out <abs>/stores_results.json
... TNR_SCRIPT=stores_main.ts harness/skyglass_wreck_sim/run.sh --spec-out <abs>/stores_spec.json
python3 flooded_stores_build.gen.py [--bundle=<results bundle> ...]
```

## Staged push (law 17)

AI `jutsus` arrays and a summon's `aiId` must be literal ids, so the build is four runs, each regenerated with
`--bundle=` from the earlier runs' results bundles: 1 strips + 26 jutsu; 2 the two summoned bodies; 3 the two summon
jutsu; 4 Isonade and the five crew. Stage 1 validates clean apart from the stale checks below; stages 2 and 4 show
their open refs until regenerated.

## validate.py checks that are stale at pin 3314d122 (evidence; laws not changed here)

- Law 4 (formula damage needs generalTypes): the damage formula uses the caster's `highestGenerals`; `generalTypes` is
  display-only (`libs/combat/tags.ts getAffected`). 134 live damage effects already ship `statTypes ["None"]` with no
  generalTypes. Forge treats it as warning L06.
- Law 6 for damage power: `PowerAttributes.power` has no max (`validators/combat.ts`); power 140 shipped in push/342.
- Law 14 `preferredStat`: the column was dropped (migration 0056; Forge `lints.mjs` no longer requires it); absent at the pin.

## Rule changes made for the validator (results identical, 30 seeds)

- Crew: the duplicate attack and end turn after the unconditional move were dead; the move is now the last rule.
- Isonade (now 20 rules, the cap) and the Grasping Arm end with an explicit end turn (law 41).
