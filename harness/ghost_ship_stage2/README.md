# Ghost Ship / Skyglass Stage 2 — offline harness

Offline, in-process evidence for gates **M0, A1, A2, B1, B2, B3, C1, C2, C3** of
`state/prompt_ghost_ship_skyglass_stage2_feasibility.md` and
`state/prompt_ghost_ship_skyglass_stage2_start.md`. The results report is
`docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md`.

## Run

```bash
harness/ghost_ship_stage2/run.sh            # M0 + all engine gates → results/
harness/ghost_ship_stage2/run.sh a2         # M0 + only test files matching "a2"
python3 harness/ghost_ship_stage2/m0_verify.py --out /tmp/m0.json   # M0 alone (stdlib)
```

Environment (all optional): `TNR_ENGINE_SRC` (an existing clone of
`studie-tech/TheNinjaRPG`), `TNR_ENGINE_WORK` (work dir, default `.work/`,
git-ignored), `TNR_OUT` (default `results/`). Requirements: git, bun 1.4.x,
python3, and `unshare` (util-linux) for the network namespace.

## What `run.sh` does

1. `git archive cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93 app` into a disposable
   export. The upstream checkout's working tree is never touched, and no engine
   file is modified.
2. `bun install --frozen-lockfile --ignore-scripts` against the pinned `bun.lock`
   (lifecycle scripts disabled).
3. Copies `engine/` into the export as `app/tests/tnr_ghost_ship_stage2/` so the
   upstream `@/…` aliases and test helpers resolve.
4. Runs M0 (`m0_verify.py`), which reads repository files only.
5. Runs `bun test tests/tnr_ghost_ship_stage2` inside `unshare -rn` (no network
   interfaces). It uses the upstream `test_build.yml` fork-PR placeholder
   environment values (no credentials) and no database (`TEST_MYSQL_URL` unset).
6. Writes `results/<gate>.json`, `results/bun_test.log` and
   `results/provenance.json` (engine pin, lockfile hash, runtime versions,
   harness file hashes, exit status).

Evidence JSON is deterministic. Every fight seeds `Math.random` (mulberry32).
Battle objects with wall-clock fields are omitted, and keys are sorted. Two
independent full runs produced byte-identical `m0/a1/a2/b1/b2/b3/c1/c2/c3.json`.

## Layout

| Path | Role |
| --- | --- |
| `m0_verify.py` | M0: source hashes, 65 memberships, retained protected-field hashes, AI/profile pointers, innate arrays, missing-vs-null drift |
| `engine/lib/fixtures.ts` | Committed-record loader (JSON pointers from the accepted packets), 0056 AI stat conversion, kit/rule variants, Sealwright carrier, player fixtures and policies |
| `engine/lib/sim.ts` | Battle assembly through the engine's `processUsersForBattle` (no DB client) and the `performAction` loop (`alignBattle` → `performAIaction` → `alignBattle`) |
| `engine/lib/items.ts`, `engine/lib/itembattle.ts` | Katana/Crystal records on the captured Flaming Sword carrier; player weapon actions via `availableUserActions` → `performBattleAction` |
| `engine/a1_kits.test.ts` | A1 |
| `engine/a2_sealwright.test.ts` | A2 |
| `engine/b_crystal.test.ts` | B1–B3 (B3 calls the real `occupation.imbueItem`/`craftItem` procedures with a read-only stub client; any write attempt is trapped) |
| `engine/c_katana.test.ts` | C1–C3 |
| `results/` | Committed evidence from the frozen run |

## Fixture limits (read before using any number)

- **Captured AI rows predate upstream migration 0056** (unified combat stats,
  commit `46f62cd9`, 2026-10-08). The harness applies that migration's AI
  branch verbatim: `offence` = max of the four offences, `defence` = max of the
  four defences, masteries = max(offence, defence) per art. A fresh
  post-migration operator capture must confirm the live values.
- **Damage settings:** `battle.extraState.dmgConfig` is unset, so the engine
  source defaults apply. Live `gameSetting` overrides were not read. Absolute
  damage can differ from live. Comparisons under identical settings are the
  evidence.
- **Players are test carriers**, not a population model: JONIN caps from
  `getUserCaps`, `calcHP/SP/CP(100)` pools (a ×2.5 "durable" band), or the
  upstream `battleScenario` defaults. They use non-elemental shared-pool jutsu
  and declared auto-combat policies.
- **Placement:** start tiles are fixed (player (2,4), boss (8,4) unless stated)
  rather than the engine's random spawn, so that both bosses face identical
  inputs.
- **Katana** is the accepted record `state/ghost_ship_skyglass_katana_record.json`
  (RUL-2026-10-11-004, Night's Testament baseline; rebuild/check with
  `tools/build_katana_record.py [--check]`). Presentation fields are labelled
  placeholders. **Crystal and imbuable-recipient** non-effect fields still come
  from the captured EPIC Flaming Sword row as a carrier.
- **0056 conversion** of the Oct 1 AI rows was confirmed exact against the live
  push/86 recapture (2026-10-11).
- **Crystal record is hypothetical:** it cannot pass the validator (B1). B2
  shows post-composition runtime only.
- **Single-opponent fights do not exercise RNG** in these kits, so the five
  seeds are identical per fixture. Multi-opponent RANDOM_* paths are covered
  only in the selector tests.
