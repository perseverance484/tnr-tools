# Silent Bastion condensed 99-node candidate — offline native recovery/reset proof

Offline, engine-native evidence for the director-selected four-division graph
`state/silent_bastion_condensed99_candidate.json` (brief
`docs/handoffs/SILENT_BASTION_CONDENSED99_NATIVE_PROOF_BRIEF.md`). Results report:
`docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md`.

**Not a manifest.** The fixture is compiled from the symbolic graph for local tests only (fixture AI users,
a sentinel completion item, placeholder starting effects). Nothing here is a build input.

## Run

```bash
harness/silent_bastion_condensed99/run.sh                              # preflight + S, D, R, E on all variants
harness/silent_bastion_condensed99/run.sh runtime                      # one gate (static|defect|runtime|edges)
TNR_VARIANTS="candidate" harness/silent_bastion_condensed99/run.sh     # one variant
python3 harness/silent_bastion_condensed99/tools/derive_alternatives.py --check
```

Requirements and isolation are those of `harness/silent_bastion_phase1/` (git, bun 1.4.x, python3, `unshare`,
a Docker daemon): `git archive` export of `studie-tech/TheNinjaRPG@13d40c4c1509ecf44262aba1b5120266011ea786`,
`bun install --frozen-lockfile --ignore-scripts`, socket-only MySQL (`--network none`) from the upstream CI
image, tests inside `unshare -rn`, placeholder environment, no credentials. No engine file is modified.

## Variants

| Variant | Graph | Objectives | Status |
| --- | --- | --- | --- |
| `candidate` | `state/silent_bastion_condensed99_candidate.json` | 99 | design under test |
| `alt99_f4gate` | `graphs/alt99_f4gate.json` | 99 | remediation option (not selected) |
| `alt99_alertgate` | `graphs/alt99_alertgate.json` | 99 | remediation option (not selected) |
| `alt95_bossgates` | `graphs/alt95_bossgates.json` | 95 | remediation option (not selected) |

The `alt*` graphs are generated from the candidate by `tools/derive_alternatives.py` (`--check` runs in
`run.sh`). Each inserts a `dN.recovered` dialog between the recovery WIN and its reset, and folds one
existing single-option dialog gate per division to stay within budget.

## Gates

| File | Gate | What runs |
| --- | --- | --- |
| `engine/c99_static.test.ts` | **S** | `QuestValidator`, `verifyQuestObjectiveFlow`, `verifyQuestContentForSave`, `findPredecessor`, `buildObjectiveEdges`; counts, dialog gating, recovery templates and reset targets, 625-path enumeration, negative controls, reset-on-win-edge lint |
| `engine/c99_defect.test.ts` | **D** | per division: later loss → 50% recovery fight → recovery **loss**; where the WIN-edge reset fires and what the next fight is (finding C1) |
| `engine/c99_runtime.test.ts` | **R** | 18 complete attempts through the real routers: success on every route, losses at every normal-lane battle, consecutive recovery losses, commander losses on all four routes, Arakane defeats, mixed repeated failures |
| `engine/c99_edges.test.ts` | **E** | no-Beacon start (F1/F2), Beacon timing, abandonment, out-of-order input around recovery fights, hidden pause / version change at checkpoints, real `quests.update`, performance, retry income (F3), text exposure (F4/F5) |

`engine/lib/run99.ts` reads the path from the graph (so folded gates are followed automatically) and checks
every battle start (objective, opponent, pools, quest effects, Beacon), every win (end pools carried,
next objective, nothing auto-fires), every loss (1 HP, no Retry Battle, same-division checkpoint) and that
earlier divisions' completed objectives survive every later reset. The fixture compiler, driver and evidence
writer are the Phase 1 ones (`harness/silent_bastion_phase1/engine/lib/`), selected with `TNR_GRAPH`.

On the candidate, gate R never loses a `recovery_later` fight; that transition is the defect C1 and is
reproduced by gate D. Every other plan is identical across variants.

## Fixture limits

Same as Phase 1: settlement is the upstream test pattern (outcomes and end pools imposed, no combat
simulated), starting effects are placeholders, fixture AIs use the empty `Default` profile, the quest is
visible in the local DB (E6 saves it hidden through the real editor), battle ryo is randomised (raw amounts
only in `*.timings.json`). Evidence JSON is deterministic; timings vary per run.
