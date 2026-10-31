# Skyglass build inputs (harness specs), rule-cap pass + RUL-2026-10-31-077 records

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
**RUL-2026-10-31-077 (adopted here):** the three retunes are in the params these files were built from (endgame Wreck
Captain pools 9, `overrides/kits_endgame.params.json`; Watch solo Captain pools 2.65, `overrides/hunts.params.rul077.json`;
Steeping Horror 5 damage rows + 35% damage given down, `overrides/charts.params.rul077.json`), and `records_spec.json` is
the enemy record table: every AI record the event fights, keyed (`base:`, `live:`, `veteran:`, `haul:`, `common:`,
`rot:`, `faded:`, `oneoff:`, `copy:`; srcId `sg344_<key with ':' -> '-'>`), one record per measured tuning, with the spec
entry that holds its row and rules and every fight that uses it (REPORT.md "RUL-2026-10-31-077" subsection). The level-50
copies are named "Faded <Name>" with a leading "The" dropped ("Faded Captain").

| File | Source (`harness/skyglass_wreck_sim/`, this branch) | Notes |
|---|---|---|
| `build_spec.json` | `TNR_SCRIPT=build_kits.ts run.sh --params overrides/kits_endgame.params.json`, then `--version lvl50 --params overrides/kits_lvl50.params.json` | Core Horror and The Captain 20 rules; endgame Captain pools 9 (RUL-077); the level-50 copies are the Faded tier ("Faded Captain") |
| `hunts_spec.json` | `TNR_SCRIPT=hunts_build.ts run.sh --params overrides/hunts.params.rul077.json --spec-out hunts_spec.json` | The Captain at pools 2.65 (RUL-2026-10-31-077); every AI carries `fullRow` / `fullProfile` (the hunts fight their own Veteran copies) |
| `hunts.params.json` | `overrides/hunts.params.rul077.json` | final-pass hunt stats + RUL-060 item 1, with the Captain at 2.65 (RUL-077) |
| `charts_spec.json` | `TNR_SCRIPT=charts_main.ts run.sh --params overrides/charts.params.rul077.json --spec-out charts_spec.json` | carries `fullRow` / `fullProfile` for `newAIs` and, new, `liveRecords` (the live records a run fights: the Fall's and the Burning Heading's crew, the Captain as ally); Steeping Horror 5 rows + 35% down (RUL-077) |
| `charts.params.rul060.json` | `overrides/charts.params.rul060.json` | unchanged from main |
| `records_spec.json` | `python3 harness/skyglass_wreck_sim/tools/records.py` (reads the four specs above and the captured AI usernames in `harvests/`) | RUL-2026-10-31-077 record table: 65 records (9 base = live, 4 live non-crew, 52 new copies); checks the cap and law-40 gates on every record, unique usernames, and that shared records are identical |
| `haul_spec.json` | `TNR_SCRIPT=haul_main.ts run.sh --spec-out haul_spec.json` (default params = the 6ad2a102 fit, merged here) | the 24 steeped variants trimmed from `graphs` / `counts`, as on main. **Guards are fixed level-100 records** (director 2026-10-31): every battle objective has `opponent_scaled_to_user: false`, each record `level: 100` with its `atLevel100` values |
| `crowned_captain_spec.json` | `TNR_SCRIPT=crowned_captain.ts run.sh --write-spec crowned_captain_spec.json --seeds 0` | 20 rules (were 40), cut by his measured rule use |
| `crownhold_spec.json` | `TNR_SCRIPT=crownhold.ts run.sh --write-spec crownhold_spec.json` | Crown Armsmaster 20 (were 30), The Second 20 (were 28) |
| `library_spec.json` | unchanged | |

Engine pin for all runs: `c86f43f4` (the harness pin; `ai_v2.ts` rule evaluation and the rule cap are unchanged at
`3314d122`).
