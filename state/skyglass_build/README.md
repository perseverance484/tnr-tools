# Skyglass build inputs (harness specs, adopted for the remaining event manifests)

Generator inputs for `push/skyglass_library.gen.py` (push/342) and the later Skyglass generators. Offline harness
outputs, zero live requests. Do not hand-edit; regenerate from the harness.

| File | Source | Notes |
|---|---|---|
| `library_spec.json`, `build_spec.json`, `hunts_spec.json`, `crowned_captain_spec.json`, `crownhold_spec.json` | `fable/skyglass-final-sim` d5957e79, `harness/skyglass_wreck_sim/` (byte-identical) | `hunts_spec.json` predates the final pass: read final hunt stats and the Called to the Archive summon from `hunts.params.json` |
| `hunts.params.json` | same commit, `overrides/hunts.params.json` | final pass (`_final_pass`): echoPower 40, Watch Captain 2.5/1 + 10% givenDown. RUL-2026-10-30-060 item 1 (Captain pools 2.5 -> 3) is NOT in it yet |
| `charts_spec.json` | regenerated 2026-10-31 on `fable/skyglass-haul-fit` 6ad2a102 (engine pin c86f43f4): `TNR_SCRIPT=charts_main.ts harness/skyglass_wreck_sim/run.sh --params <charts.params.rul060.json> --spec-out <out>` with `specout_full.patch` applied | final-pass params plus RUL-2026-10-30-060 item 2 |
| `charts.params.rul060.json` | `overrides/charts.params.json` (d5957e79) with the Sealed Reliquary's Sealwright copy at 2 damage rows (RUL-2026-10-30-060 item 2) | |
| `haul_spec.json` | regenerated the same way: `TNR_SCRIPT=haul_main.ts run.sh --spec-out <out>` (default params = the 6ad2a102 fit) | identical to the committed 6ad2a102 `haul_spec.json` apart from the two added fields; the 24 steeped variants (Haul steeping dropped, RUL-2026-10-29-056) are trimmed from `graphs`/`counts` |
| `specout_full.patch` | 6 added lines in `engine/charts_main.ts` and `engine/haul_main.ts` | adds `fullRow` (the AI row the harness fought, as insertAiSchema input) and `fullProfile` (rules with their conditions and actions) to each spec-out AI record, so the copies can be created exactly as simulated. Not committed to the harness branch (scratch worktree only) |
