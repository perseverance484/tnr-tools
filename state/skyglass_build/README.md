# Skyglass build inputs (harness specs), rule-cap pass

Generator inputs for `push/skyglass_library.gen.py` (push/342) and the later Skyglass generators. Offline harness
outputs, zero live requests. Do not hand-edit; regenerate from the harness.

**This directory on `fable/skyglass-rule-cap` supersedes `state/skyglass_build/` on `main`** for every AI rule list
(RUL-2026-10-31-066 item 1 and the director's law-40 gate decision of 2026-10-31):

- every AI profile has at most 20 rules (`AI_PROFILE_MAX_RULES`, theninjarpg@3314d122 `app/drizzle/constants.ts:1933`,
  enforced by `ai.updateAiProfile`, `app/src/server/api/routers/ai.ts:87`);
- every `distance_lower_than` on a rule that casts a shared-pool jutsu is that jutsu's range + 1 (law 40), the value
  Forge's `kitProblems` (`forge/src/runner/pool.mjs`) requires;
- the harness now fails any spec or battle with an AI over the cap (`engine/rulecap.ts`) and writes law-40 gates into
  every spec it emits (`engine/gates.ts`). Checked independently: 122 rule lists, 0 over the cap, 0 gate errors.

The trims and their effects are in `harness/skyglass_wreck_sim/REPORT.md`, section "Rule cap and law-40 gates".
RUL-2026-10-31-067: only the Faded names are applied; the base / Veteran / Rot-Touched folding is not (measured
infeasible as specified; REPORT.md §6). Proposed retunes (`overrides/*rulecap_proposed.json`) are **not** in these files.

| File | Source (`harness/skyglass_wreck_sim/`, this branch) | Notes |
|---|---|---|
| `build_spec.json` | `TNR_SCRIPT=build_kits.ts run.sh --params overrides/kits_endgame.params.json`, then `--version lvl50 --params overrides/kits_lvl50.params.json` | Core Horror and The Captain 20 rules (were 32 / 28); the level-50 copies are named "Faded <Name>" (RUL-2026-10-31-067 item 6) |
| `hunts_spec.json` | `TNR_SCRIPT=hunts_build.ts run.sh --params overrides/hunts.params.rul060.json --spec-out hunts_spec.json` | regenerated (the copy on main predated the final pass); The Captain at pools 3 (RUL-2026-10-30-060 item 1); Core Horror, The Captain, Wayfinder, Foundry Warden 20 rules |
| `hunts.params.json` | `overrides/hunts.params.rul060.json` | final-pass hunt stats + RUL-060 item 1 |
| `charts_spec.json` | `TNR_SCRIPT=charts_main.ts run.sh --params overrides/charts.params.rul060.json --spec-out charts_spec.json` | carries `fullRow` / `fullProfile` (the former `specout_full.patch`, now committed in `engine/charts_main.ts` and `engine/haul_main.ts`) |
| `charts.params.rul060.json` | `overrides/charts.params.rul060.json` | unchanged from main |
| `haul_spec.json` | `TNR_SCRIPT=haul_main.ts run.sh --spec-out haul_spec.json` (default params = the 6ad2a102 fit, merged here) | the 24 steeped variants trimmed from `graphs` / `counts`, as on main. **Guards are fixed level-100 records** (director 2026-10-31): every battle objective has `opponent_scaled_to_user: false`, each record `level: 100` with its `atLevel100` values |
| `crowned_captain_spec.json` | `TNR_SCRIPT=crowned_captain.ts run.sh --write-spec crowned_captain_spec.json --seeds 0` | 20 rules (were 40), cut by his measured rule use |
| `crownhold_spec.json` | `TNR_SCRIPT=crownhold.ts run.sh --write-spec crownhold_spec.json` | Crown Armsmaster 20 (were 30), The Second 20 (were 28) |
| `library_spec.json` | unchanged | |

Engine pin for all runs: `c86f43f4` (the harness pin; `ai_v2.ts` rule evaluation and the rule cap are unchanged at
`3314d122`).
