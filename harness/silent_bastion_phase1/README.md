# Silent Bastion Phase 1 — offline native progression proof

Offline, engine-native evidence for the Phase 1 progression graph
`state/silent_bastion_phase1_graph.json` (design handoff
`docs/handoffs/SILENT_BASTION_PHASE1_OFFLINE_PROOF_2026-10-14.md`). Results report:
`docs/reviews/SILENT_BASTION_PHASE1_NATIVE_RESULTS.md`.

**Graph revision:** r2 per RUL-2026-10-14-001 (one fourth fight per lane; the protocol dialog after
it routes to the Medical `givePools: 100` or Combat commander battle). `tools/restructure_protocol_choice.py`
produces r2 from the r1 design graph; `--check` confirms the committed graph is r2.

**Not a manifest.** The fixture is compiled from the symbolic graph for local tests only: fixture AI
users, a sentinel completion item, and placeholder starting effects. Nothing here is a build input.

## Run

```bash
harness/silent_bastion_phase1/run.sh            # upstream preflight + gates S, R, E
harness/silent_bastion_phase1/run.sh edges      # only p1_edges (also: static, runtime)
```

Requirements: git, bun 1.4.x, python3, `unshare` (util-linux), and a reachable Docker daemon.
Environment (optional): `TNR_ENGINE_SRC`, `TNR_ENGINE_WORK` (default `.work/`, git-ignored),
`TNR_OUT` (default `results/`), `TNR_KEEP_DB=1`.

## What `run.sh` does

1. `git archive c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd app` into a disposable export (no engine
   file is modified), then `bun install --frozen-lockfile --ignore-scripts`.
2. Copies `engine/` into the export as `app/tests/tnr_silent_bastion_phase1/` so upstream `@/…`
   aliases and `tests/setup/*` (factories, `describeWithDatabase`, `callerFor`) resolve.
3. Starts a throwaway MySQL from the upstream CI's own image (`test_build.yml`: `mysql:26.7.0`,
   pinned by digest) with `--network none`. It is reachable only through a unix socket in
   `.work/mysqld/`; the tests connect with `TEST_MYSQL_URL=…?socketPath=…`.
4. Runs the engine's own Pyramid/quest-run suites at the pin as a preflight
   (`results/upstream_preflight.log`).
5. Runs gates S, R and E with `bun test` inside `unshare -rn` (no network interfaces), with the
   upstream fork-PR placeholder environment and no credentials.
6. `tools/check_evidence.py` re-checks each evidence file (exists, has checks, none failed) and prints
   reproduced findings. Writes `results/provenance.json`.

`run.sh` exits nonzero if the preflight, `bun test`, or the evidence check fails.

## Gates

| File | Gate | What runs |
| --- | --- | --- |
| `engine/p1_static.test.ts` | **S** | `QuestValidator`, `verifyQuestContentForSave`, `verifyQuestObjectiveFlow`, `findPredecessor`, `buildObjectiveEdges` on the compiled fixture; 3,125-path enumeration; fail/win/reset edges; allowlist checks |
| `engine/p1_runtime.test.ts` | **R** | 15 complete attempts through the real routers: 4 all-success, 8 initial-loss matrices (a loss at every one of the 40 initial-lane battles), 2 retry-lane Arakane defeats, 1 five-consecutive-retry run |
| `engine/p1_edges.test.ts` | **E** | abandonment, premature/out-of-order input, missing Beacon (findings F1/F2), recovery freeze, hidden pause/version change, the real `quests.update` save, performance, retry-loop income (finding F3) |

Driver (`engine/lib/driver.ts`): `startQuest` → `checkRewards(choice)` (starts the battle through
quest consequences → `initiateBattle`) → settlement with the upstream pattern
(`calcBattleResult` + `combat/database.updateUser`, as `tests/server/api/quests.persistentBattle`)
→ `fetchUpdatedUser` (runs `reset_quest`/`fail_quest` consequences). The driver chooses dialog
options and outcomes only; it never writes quest trackers.

## Fixture limits (read before using any result)

- **Settlement is the upstream test pattern, not a played fight.** Outcomes and end pools are set on
  the battle snapshot before `calcBattleResult`; no combat actions or AI run. Combat balance is out
  of scope.
- **Starting effects are placeholders** (`engine/lib/graph.ts` `PLACEHOLDER_EFFECTS`). Division V's
  advertised Clear Prevent cannot be authored; its route carries a labelled stand-in.
- Fixture AIs have default stats and the empty `Default` AI profile.
- The quest is visible (`hidden:false`) in the local DB so a normal user can play it; E7 separately
  saves it hidden through the real editor procedure.
- Battle ryo is randomised by the engine; raw amounts are only in `*.timings.json`.
- Evidence JSON is deterministic (sorted keys; passing checks record names only). Timings live in
  `*.timings.json` and vary per run.
