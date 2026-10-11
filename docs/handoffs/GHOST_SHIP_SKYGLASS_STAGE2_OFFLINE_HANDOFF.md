# Handoff — Ghost Ship / Skyglass Stage 2 offline tests (Fable → ChatGPT review)

Format: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Results: `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md`.

## Repository / refs

- Repository: `perseverance484/tnr-tools`.
- Implementation branch: `ccr-71fd390f-0j0g78`. This is the branch the Claude Code session was assigned, used in place of the suggested `fable/ghost-ship-skyglass-stage2-offline`. It has a single writer (Fable) and no other owner.
- Base SHA: `61373538035d41f7e773ec082b739740cdf0860e`, the complete design/test-input commit from the delivery bundle (`refs/heads/chatgpt/ghost-ship-stage2-review-20261011`, required ancestor `0dbd54c0…`). The bundle was verified (`git bundle verify` OK; file hashes match `handoff.json`).
- Head SHA: the commit that adds this file. A file cannot name its own hash, so the exact frozen SHA is in the delivery message and on the pushed branch head. Review that SHA, not the branch name.
- Integration target: `main`. It was verified at `0eb57de20877d266dde666229ae4c68e8fbcf4c0` at start and again before commit. It is an ancestor of the base, so no reconciliation was needed.
- Note: the five bundle commits above `0dbd54c0` had not been published. Pushing this branch publishes them unchanged as ancestors. No `chatgpt/*` branch was written.

## Scope

**Objective:** run the accepted Stage 2 offline gates against actual pinned engine code and return reproducible evidence.

**Added files only:**

- `harness/ghost_ship_stage2/` (runner, M0 script, engine tests, fixture libs, README, `.gitignore`, `results/`)
- `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md`
- `docs/design/GHOST_SHIP_CRYSTAL_ENGINE_CORRECTION_PROPOSAL.md`
- this file

No existing file was modified.

**Not implemented:** no engine patch, no Crystal correction, no final AI rule array, no tuning, no manifest, no art, no quest edits, no publication.

## Verification (exact)

- `python3 harness/ghost_ship_stage2/m0_verify.py` → `M0 PASS: 482 checks, 0 failed`.
- `harness/ghost_ship_stage2/run.sh` → `68 pass, 0 fail, 136 expect() calls, Ran 68 tests across 4 files`, exit 0. Evidence assertions: A1 160, A2 25, B1 4, B2 7, B3 9, C1 4, C2 15, C3 1, all with 0 failed.
- A second independent run produced byte-identical `results/{m0,a1,a2,b1,b2,b3,c1,c2,c3}.json`.
- Upstream preflight at the pin, same isolation: `consume.test.ts`, `ai_v2_rules.test.ts`, `shared_cooldown.test.ts` → 63 pass.
- Doctrine, law, pack and generated-contract gates: not applicable, because no `skills/`, doctrine or generated file changed.

## Source / provenance

- Engine `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` via `git archive`; `bun.lock` sha256 `da6602f2550bea9f1baf8508fa82b03d320bfcee269257f36cf25b47f1906c08`; bun 1.4.2; node v22.22.0. Dependencies: `bun install --frozen-lockfile --ignore-scripts` (user-approved). Tests ran under `unshare -rn` with upstream CI placeholder environment values and no database.
- Drift A (`4774560e`) → B → C (`1853b6ab`) is assessed in results §2. The B→C QUEST team-targeting change does not alter these fixtures; re-run at the deployed pin when known.
- Fixtures: committed captures by JSON pointer (hashes in `results/m0.json`), plus labelled carriers (results §2).
- Captured AI rows are converted with upstream migration 0056's AI branch.
- No generated artifact was regenerated or adopted.

## Risk / debt — attack these hardest

1. The 0056 conversion of pre-migration AI rows (`fixtures.ts migrate0056Ai`). Every boss number depends on it.
2. Source-default `dmgConfig` instead of live settings.
3. The battle loop replicates `combat.performAction`'s inner loop. An idle auto-combat turn is passed by expiring the round clock, as the live timer would.
4. `processUsersForBattle` is called with a throwing no-DB client. It is safe only because no fixture carries a summon; that is asserted.
5. Start tiles are fixed rather than randomly spawned.
6. B3 uses the real procedures, but with a read-only stub client. Acceptance means "every guard passed and the first write was reached", not a committed imbue.
7. Selector boundary IDG powers are injected through the upstream `makeEffect` helper; they are synthetic test inputs.
8. Single-opponent fights do not exercise RNG, so the 5 seeds are identical.
9. Sealwright's numeric profile uses the Captain as a carrier, and preferences/elements are an open contract gate.
10. The harness bug found and fixed during development (no `leftSideUserIds`, which made both sides friendly to `friendlyFire: ENEMIES` effects) is covered by the hazard damage assertions.

## Live-game statement

Live-game requests 0. Writes 0. Asset-CDN requests 0. No credentials, cookies or session material. No game server, live DB or API. No browser or installed-client checks. The upstream engine working tree is unchanged, and no engine file was edited even in the scratch export.

## Explicitly not begun

Final rule freeze; Crowned support activation; tuning; the Crystal engine correction; the Sword baseline (operator capture needed); manifest assembly; art; publication.

## Revision r2 (2026-10-11): accepted Katana baseline

- Previous frozen review target: `8c19a376b97c4d5099d43e6c7ea9e6eabf057d59`. The r2 head is the commit that adds this section; its exact SHA is in the delivery message.
- Intervening commits on this branch: `push/85` and `push/86` capture manifests, already run and archived on `main`.
- **Trigger:** RUL-2026-10-11-004. dauntless chose Night's Testament as the baseline, a Crystal-element Pierce, drop-only (not craftable) and tradable.
- **Changes:**
  - `state/ghost_ship_skyglass_katana_record.json`, derived by `harness/ghost_ship_stage2/tools/build_katana_record.py` (`--check` → current);
  - the capture bundle `harvests/inbox/tnr_results_1791727479372.json`, byte-identical to `main`;
  - `docs/RULINGS.md`, with RUL-2026-10-11-004 appended;
  - the Katana section of `state/ghost_ship_skyglass_reward_decisions.md`;
  - harness: the Katana now uses the accepted record; C1 validates the full record; C2 asserts cooldown 6; C3 is rewritten as final-record validation; B3 adds the hidden-state case;
  - results, report and README updated.
- **Results:** `run.sh` → 68 pass, 0 fail, 141 expect() calls. Evidence assertions: A1 160, A2 25, B1 4, B2 7, B3 10, C1 4, C2 16, C3 12, all with 0 failed. M0 482/482. Two runs produced byte-identical evidence. A1, A2, B1 and B2 evidence is unchanged from r1.
- **C3:** PASS for mechanics and economy. Presentation (description, battle description, image, effect animation/SFX) remains pending.
- **New observation:** `fetchUserItems` excludes hidden items, so a still-hidden Katana is invisible to `imbueItem`.
- Live-game requests 0, writes 0. No engine, art or manifest change.
