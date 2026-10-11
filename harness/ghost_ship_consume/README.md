# Ghost Ship / Skyglass — active Consume offline revalidation

Implements `state/prompt_ghost_ship_skyglass_consume_revalidation.md` at design
commit `46df27172556807ab5bf723b0aa8c1251445ba2e` (RUL-2026-10-11-005).
Katana15 / Crystal10 are approved. **Consume rounds3 / shieldRounds3 are test
carriers only.** No final item record, manifest, timing or economy freeze.

The historical `harness/ghost_ship_stage2/`, its builder, old Katana record and
results are unchanged. This successor copies the required fixture/assembly
helpers deliberately; it does not overwrite the r4 package.

## Run

Requirements: git, Python3, Bun1.4.x, Linux `libseccomp.so.2`, a local engine clone,
and the existing user-approved dependency install. The runner performs no install.

```bash
export TNR_ENGINE_SRC=/path/to/TheNinjaRPG
export TNR_DEPENDENCIES_APP=/path/to/approved-old-export/app
export TNR_ENGINE_WORK=/path/to/new-consume-work
# Default: private network namespace plus seccomp socket denial.
harness/ghost_ship_consume/run.sh
# Restricted container: explicit syscall-denial alternative, no namespace claim.
TNR_NETWORK_ISOLATION=seccomp harness/ghost_ship_consume/run.sh
```

`TNR_OUT` optionally selects an output directory. Before importing engine code,
the runner checks the exact pin, every pinned app file, both dependency manifests,
the resolved dependency directory, the generated carrier, and socket denial.
It clears previous known results first; an early failed preflight cannot leave a
prior clean result. It refuses an output path inside the historical harness.

The engine is exported with `git archive` at
`585534d7eb21d6f0dd678d5c3eb92662f611d39b`. Only a new test-suite directory is added;
no pinned engine file is edited. All 1,780 pinned app files are checked before and
after execution. Dependency manifests match the historical cddd7d91 export.
The main suite uses an explicit directory path so adjacent development suites are
not selected by Bun's substring filter.

`tools/test_env.sh` supplies only an environment allowlist and upstream CI
placeholders. Bun receives `--no-env-file --no-install`; no real credentials or
DB settings enter the child. Both isolation modes deny socket creation, connection,
listening, sending and io_uring setup. Extra inherited descriptors are closed.
A failed isolation setup prevents execution. `seccomp` does not claim a private
network namespace; the recorded run used it because `unshare -rn` is unavailable.

## Evidence and derivation

| File | Scope |
| --- | --- |
| `tools/build_item_carriers.py` | Reproducible new candidate record packet; run normally to rebuild, `--check` to verify |
| `state/ghost_ship_skyglass_active_consume_carriers.json` | Full Katana/Crystal test carriers with field provenance, capture hashes and exact old-to-new Katana diff |
| `engine/contract_guards.test.ts` | CONTRACT: complete item validation; GUARDS: real occupation eligibility paths with write-trapping DB and stubbed profile refresh |
| `engine/active_consume.test.ts` | Actual assembly/actions, later hits, expiry, overlap, Clear/Buff Prevent, accepted weapon costs/CD/range |
| `engine/lib/consume_probes.ts` | Upstream processor fixtures for damage attribution, delayed effects, reflection/self/recoil, ratio and shield ceilings |
| `results/m0.json` | Reuses the unchanged r4 repository-only verifier; approved packets still resolve |
| `results/{contract,guards,active}.json` | Deterministic scoped evidence, not a balance acceptance |
| `results/provenance.json` | Source/runtime/lockfile/carrier/harness hashes and all gate exit statuses |

Failure enforcement preserves r4's `Evidence.flush`, last-test `requireClean`,
post-run `check_evidence.py`, and five infrastructure-aware negative probes.
Missing tools, unavailable isolation or malformed negative results are failures,
not successful enforcement. The runner exits nonzero if any layer fails.

## Limits

- Fixed complete placements override secure random spawn; source-default damage
  settings, old captured player carriers, no trained elemental/PvP benefits.
- Assembly reproduces capped/cloned preprocessing, pool adjustments and mastery
  refresh; a throwing no-DB client is safe only for the asserted summon-free kit.
- Processor controls bypass item assembly and sometimes exceed legal content
  power to exercise ceilings. They are labelled separately from item tests.
- Crystal non-effect fields, rarity variants and recipe material ID are test
  carriers. No distribution/access policy or live ID is invented.
- GUARDS stops at the first write; no DB persistence, CAS/concurrency, full profile
  refresh, auction transaction or successful craft/imbue is claimed.
- A1/A2 fights are not rerun here. Old measurements do not become new-pin parity.
- No live requests/writes, CDN fetches, browser, installed-client or deployment check.

Detailed findings: `docs/reviews/GHOST_SHIP_ACTIVE_CONSUME_OFFLINE_RESULTS.md`.
Source drift: `docs/reviews/GHOST_SHIP_ACTIVE_CONSUME_SOURCE_DRIFT.md`.
