# Handoff — Silent Bastion Phase 1 native offline proof (Fable → ChatGPT review)

Format: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Results: `docs/reviews/SILENT_BASTION_PHASE1_NATIVE_RESULTS.md`. Request: `docs/handoffs/SILENT_BASTION_PHASE1_OFFLINE_PROOF_2026-10-14.md` §4.

## Repository / refs

- Repository: `perseverance484/tnr-tools`.
- Implementation branch: `claude/silent-bastion-phase1-validation-9628h6`. This is the branch the Claude Code session was assigned, used in place of a `fable/*` name. Single writer: Fable.
- Base SHA: `450c47bf88b38758477b5783569ea6ab7a0c146a`, the frozen head of `chatgpt/silent-bastion-design-20261013`, which carries the graph under test. That branch was not written to.
- Implementation commit: `04df556c7814ee1007176fb0b73395e8e82fbb59` (harness, evidence, results report).
- Head SHA: the commit that adds this file. A file cannot name its own hash, so the exact frozen SHA is in the delivery message and is the pushed branch head. Review that SHA.
- Integration target: `main`, verified at `1da18301e8e4660cedf3daa3e80893a2ac918f2b` before commit. `main` is **not** an ancestor: the design branch's merge-base is `057acddb…`. `git merge-tree` reports a clean merge. Integration belongs to the design workstream's merge.

## Scope

**Objective:** verify the Phase 1 progression graph against the pinned game source with offline, engine-native tests, and record results and blockers.

**Added files only:**
- `harness/silent_bastion_phase1/`: `run.sh`, `README.md`, `.gitignore`, `engine/{p1_static,p1_runtime,p1_edges}.test.ts`, `engine/lib/{graph,driver,scenario,report}.ts`, `tools/check_evidence.py`, `results/`;
- `docs/reviews/SILENT_BASTION_PHASE1_NATIVE_RESULTS.md`;
- this file.

No existing file was modified. The graph, design docs and generated projections (`state/active-context.md`, `state/status.json`) are untouched. No workstream roadmap was initialised: that waits for the integration boundary named in the request.

**Not implemented:** no engine patch, no graph change, no production manifest, no AI/stats/rewards, no effect values, no art, no publication.

## Verification (exact)

- `harness/silent_bastion_phase1/run.sh` → `run.sh: preflight=0 bun=0 evidence=0 -> exit 0`.
  - Upstream preflight at the pin (8 suites: `quest.battleRetry`, `questRun`, `quests.persistentBattle`, `quests.isolation`, `quests.runState`, `combat.questEntry`, `quests.pyramidConsequences`, `quests.battleConsequences`): 73 pass, 0 fail.
  - Gates: `Ran 44 tests across 3 files`, 44 pass, 0 fail.
  - Evidence: `s_static` 32 checks, `r_runtime` 7,648, `e_edges` 560; 0 failed. Findings F1, F2, F3 reproduced.
- A second independent run (`TNR_OUT=/tmp/…/run2 run.sh`) also exited 0. `s_static.json`, `r_runtime.json` and `e_edges.json` are byte-identical (`cmp`). The `*.timings.json` files are volatile by design.
- `results/provenance.json`: the harness file hashes match the committed files; the design graph sha256 is `bbb85dda…aee9`.
- Doctrine/law/pack/generated-contract gates: not applicable. No `skills/`, doctrine, projected or generated file changed.

## Source / provenance

- Engine `studie-tech/TheNinjaRPG@c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd` via `git archive`, with `bun install --frozen-lockfile --ignore-scripts`. bun 1.4.2, node v22.22.0. The lockfile hash is in provenance.
- DB: the upstream CI's own image `mysql:26.7.0@sha256:893418c8…9c3f`, run as `--network none`, unix socket only, throwaway.
- Isolation: `unshare -rn` with the upstream `test_build.yml` fork-PR placeholder environment.
- Network used *outside* the test namespace, for setup only: clone of the public engine repository, the npm registry for `bun install`, and the Docker Hub image pull. Nothing contacted the game.
- No captures used; no generated artifact rebuilt or adopted.

## Risk / debt — attack these hardest

1. **Settlement realism.** Battles are settled with the upstream `persistentBattle` test pattern: pools and HP are imposed on the snapshot, then `calcBattleResult` + `updateUser` run. No combat action runs. Any post-battle path that only the live `performAction` loop exercises is not covered.
2. **F1 severity and reach.** F1 is proven through the missing-Beacon trigger only. Other `initiateBattle` failure windows (races, a mid-transaction entry change) are argued from the source, not exercised.
3. **Compiler fidelity** (`engine/lib/graph.ts`). S checks that compiled edges equal the symbolic edges for all 208 nodes, but the compiler's choice of single-option dialog text, objective order (taken from JSON order) and placeholder tags is mine.
4. The fixture quest is `hidden:false` for play. The hidden-staging path is tested only by save (E7) and by pause/resume (E6).
5. Fixture AIs and the `Default` empty AI profile. Opponent identity is checked, not behaviour.
6. `checkRewards` reports `success:true` when the first battle is refused (F2). The scenario runner also asserts that the battle actually started, so this cannot mask a failure.

## Decisions open (user-owned)

- F1: whether to pursue an engine change, accept the risk, or apply the partial content mitigation (reorder f4 before commander). Results §3 lists the options.
- F2: whether a Beacon check at `startQuest` is wanted (engine).
- F3: retry-loop battle income — accept, scale (`scaleGains` on retry-lane battles), or cap.
- Unchanged and still open: the Arakane Combat Protocol (`clearprevent` unsupported), all protocol/alert values, and `sceneCharacters` for a visible save.

## Live-game statement

Live-game requests 0. Writes 0. No credentials, cookies or session material. No game server or live DB. No browser, Logbook/mobile or installed-client checks were performed.

## Explicitly not begun

Production manifest; Phase 2+ (puzzles/protocol values, regular opponents, commander data, rewards/economy, art); any engine patch for F1/F2; content-workstream roadmap initialisation; integration into `main`.

## Revision r2 (2026-10-14): director restructure, RUL-2026-10-14-001

- Previous frozen review target: `edc53025b9bb9a10bc5886f1fb60a9126d457067` (r1). The r2 head is the commit that adds this section; its exact SHA is in the delivery message. Sections above describe r1 except where this section differs.
- **Trigger:** dauntless ruled that the protocol is decided by the dialog that leads into the commander fight, not attached to the fourth enemy. Medical is now a full heal (`givePools: 100`).
- **Changes:**
  - `state/silent_bastion_phase1_graph.json` is now r2, produced by the new `harness/silent_bastion_phase1/tools/restructure_protocol_choice.py` (`--check` → current). Changes:
    - one fourth fight per lane (`d/b{i}.{lane}.f4`);
    - a protocol dialog `d{i}.{lane}.protocol` that routes directly to `b{i}.{lane}.boss.medical` (100) or `b{i}.{lane}.boss.combat`;
    - the per-protocol commander gate dialogs are removed;
    - the fourth fight is listed before the commanders;
    - 178 nodes (91 dialogs, 80 battles); formatting is unchanged (2-space JSON).
  - `docs/RULINGS.md`: RUL-2026-10-14-001 appended.
  - Medical text updated to the ruling in `state/silent_bastion_design.md`, `state/silent_bastion_release_plan.md` (prose and schematic) and `state/silent_bastion_commander_roster.md`. The roster's Combat-target wording was **not** changed: it remains the open contradiction in release plan §4.3.
  - Harness gates updated for the r2 shape. The Medical check now asserts 100% on every Medical start. E4b now asserts that the fourth fight precedes the commander.
  - Results report and README updated to r2.
- **Results:** `run.sh` → `preflight=0 bun=0 evidence=0 -> exit 0`.
  - Upstream preflight: 73 pass.
  - Gates: 43 tests pass.
  - Evidence: `s_static` 33, `r_runtime` 7,105, `e_edges` 561; 0 failed.
  - R covered 15 attempts, 557 battles, 78 losses and 72 retry entries. 3,125 success paths remain, at 20–25 battles each.
  - An independent second run produced byte-identical evidence. Provenance hashes match. The graph sha256 is `922b128e…ff5e`.
- **Findings after r2:**
  - **F1** is narrowed but **still open**. The commander-before-fourth-fight order is gone; the dialog-gate bypass in the missing-Beacon window remains.
  - **F2** and **F3** are unchanged.
- **Branch note:** the design documents on this branch now diverge from `chatgpt/silent-bastion-design-20261013` on the Medical value and structure. Reconcile at integration in favour of RUL-2026-10-14-001.
