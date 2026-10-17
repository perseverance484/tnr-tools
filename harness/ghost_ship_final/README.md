# Ghost Ship / Skyglass — final 2/2 items + Crowned Captain support (offline)

Implements, at design commit `8a78115367feda143e9591f524b739a7d56330af` (r2):

- `state/prompt_ghost_ship_skyglass_final_item_revalidation.md` (RUL-2026-10-11-006): final
  Katana15 / Crystal10 records with Consume `rounds:2` / `shieldRounds:2`, and a LEGENDARY,
  tradable Crystal; r2 applies RUL-2026-10-12-005 (12-Filament recipe restored, `canBeCrafted:true`,
  non-ruling fields mirrored from the live Heal Crystal III row captured by push/87);
- `state/ghost_ship_skyglass_crowned_support_behavior.md` (RUL-2026-10-11-007/008): Crowned
  Captain heal strictly below 40%, Copy at summed IDG ≥ 71, and regular Reflect.

This is a versioned successor. `harness/ghost_ship_stage2/` (r4) and `harness/ghost_ship_consume/`
(3/3 carriers, `fcd79e5a…`) and their records/results are unchanged and still reproduce; `run.sh`
re-checks the 3/3 carrier builder and refuses to write into either historical harness.

## r3 (2026-10-12): STATS gate

`engine/release_stats.test.ts` (gate **STATS**) replays every AI save push/90 performs through the pinned server path:
- Forge `mergeAi`, then `insertAiSchema.parse`, `setEmptyStringsToNulls`, `{...stored, ...data}` and `scaleEditedAi`;
- then a repeated identical save;
- then the battle paths at `combat.ts:2469-2487`: an unscaled fight, and a quest fight scaled to a level-100 opponent, both through `capUserStats`.

It covers the 9 included existing AIs, Sealwright's single full create from the `profile.create` placeholder, and the two hazards. It also proves every asserted AI `effects` array is a fixed point of the server's `insertAiSchema.effects` parse (RUL-2026-10-12-012 and review corrections 2 and 4). A control reproduces the superseded two-stage Sealwright path: an incomplete-stat create stores offence and defence at 30.

## Run

Requirements: git, Python 3, Bun 1.4.x, Linux `libseccomp.so.2`, a local engine clone, and the
existing user-approved dependency install (the runner performs no install).

```bash
export TNR_ENGINE_SRC=/path/to/TheNinjaRPG          # must contain 585534d7
export TNR_DEPENDENCIES_APP=/path/to/approved/app   # frozen install; manifests must match byte for byte
export TNR_ENGINE_WORK=/path/to/fresh-work-dir
harness/ghost_ship_final/run.sh                      # default: unshare -rn + seccomp socket denial
TNR_NETWORK_ISOLATION=seccomp harness/ghost_ship_final/run.sh   # restricted container; no namespace claim
```

The runner exports `585534d7eb21d6f0dd678d5c3eb92662f611d39b` with `git archive`, verifies every
pinned app file before and after the tests, checks the dependency manifests, proves socket
denial before importing engine code, rebuilds nothing but checks both record builders
(`--check`), runs M0 (the unchanged r4 verifier), the engine suites, `tools/check_evidence.py`
for M0/CONTRACT/GUARDS/ACTIVE/CROWNED/STATS, and the five-probe negative self-test. Any failing layer
makes it exit nonzero.

## Files

| Path | Role |
| --- | --- |
| `tools/build_final_items.py` | Derives `state/ghost_ship_skyglass_final_item_records.json`; `--check` verifies it. Asserts the exact deltas from the r4 Katana and the 3/3 carriers |
| `engine/contract_guards.test.ts` | CONTRACT: complete-record validation of both items. GUARDS: real `imbueItem`/`craftItem` pre-write paths with a write-trapping read-only DB stub, including the 12-Filament recipe craft path |
| `engine/active_consume.test.ts` | ACTIVE: real assembly/actions at 2/2 — activation, granting/later hits, final eligible and first ineligible hit, independent shield expiry, overlap observation, Clear, Buff Prevent/immunity, costs/cooldown/range; plus the upstream processor probes |
| `engine/crowned_support.test.ts` | CROWNED: rule schema, heal boundary and fall-through, Copy trigger vs copied effects, selector/summons/path distance, Reflect, and the captured/dormant/support fight comparison |
| `selftest/`, `tools/check_evidence.py` | Fail-closed evidence enforcement (unchanged design from the 3/3 package) |
| `results/` | Committed deterministic evidence and provenance |

## Limits

- Crystal fields no ruling sets mirror Heal Crystal III (`crystal.mirroredFields`); presentation
  fields are pending director text (labelled placeholders).
- GUARDS stops at the first write: no persistence, CAS/concurrency, committed craft/imbue or
  executed trade is claimed. `canBeTraded` is record/schema evidence only.
- Crowned selector inputs (HP fractions, IDG/prevent/copy-budget effects, summons) are injected
  with the upstream `makeEffect` helper; they are synthetic test inputs.
- Fights: fixed placements, source-default damage settings, the historical player carriers,
  single opponent (seeds repeat deterministic encounters; they are not independent win-rate
  samples). No numeric acceptance tolerance is applied.
- Engine pin is upstream source, not a verified deployed version. No live requests/writes, CDN,
  browser or installed-client checks.

Results: `docs/reviews/GHOST_SHIP_FINAL_ITEMS_CROWNED_OFFLINE_RESULTS.md`.
