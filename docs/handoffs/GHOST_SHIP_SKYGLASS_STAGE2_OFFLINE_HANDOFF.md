# Handoff — Ghost Ship / Skyglass Stage 2 offline tests (Fable → ChatGPT review)

Format: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Results: `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md`.

> **Revision status.** r3 passed ChatGPT's independent verification; **r4** (section at the end) applies its non-blocking follow-ups only. The sections from "Repository / refs" to "Explicitly not begun" are the **r1** handoff (`8c19a376…`), kept for traceability. Statements marked **[r1; superseded]** no longer hold. Where r1 and a later revision disagree, the later revision wins.

## Repository / refs

- Repository: `perseverance484/tnr-tools`.
- Implementation branch: `ccr-71fd390f-0j0g78`. This is the branch the Claude Code session was assigned, used in place of the suggested `fable/ghost-ship-skyglass-stage2-offline`. It has a single writer (Fable) and no other owner.
- Base SHA: `61373538035d41f7e773ec082b739740cdf0860e`, the complete design/test-input commit from the delivery bundle (`refs/heads/chatgpt/ghost-ship-stage2-review-20261011`, required ancestor `0dbd54c0…`). The bundle was verified (`git bundle verify` OK; file hashes match `handoff.json`).
- Head SHA **[r1; superseded — see r2/r3]**: the commit that adds this file. A file cannot name its own hash, so the exact frozen SHA is in the delivery message and on the pushed branch head. Review that SHA, not the branch name.
- Integration target: `main`. It was verified at `0eb57de20877d266dde666229ae4c68e8fbcf4c0` at start and again before commit. It is an ancestor of the base, so no reconciliation was needed.
- Note: the five bundle commits above `0dbd54c0` had not been published. Pushing this branch publishes them unchanged as ancestors. No `chatgpt/*` branch was written.

## Scope

**Objective:** run the accepted Stage 2 offline gates against actual pinned engine code and return reproducible evidence.

**Added files only [r1; superseded — r2 modified `docs/RULINGS.md` and `state/ghost_ship_skyglass_reward_decisions.md` and added `state/ghost_ship_skyglass_katana_record.json`; r3 modified the reward-decisions gate list]:**

- `harness/ghost_ship_stage2/` (runner, M0 script, engine tests, fixture libs, README, `.gitignore`, `results/`)
- `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md`
- `docs/design/GHOST_SHIP_CRYSTAL_ENGINE_CORRECTION_PROPOSAL.md`
- this file

No existing file was modified **[r1 only; superseded by r2 and r3]**.

**Not implemented:** no engine patch, no Crystal correction, no final AI rule array, no tuning, no manifest, no art, no quest edits, no publication.

## Verification (exact) [r1; superseded — r3 counts are in the r3 section]

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
6. B3 uses the real procedures, but with a read-only stub client. Acceptance means "the tested pre-write eligibility guards passed and the first write was reached", not a committed imbue. Persistence and concurrency guards were not run. (Corrected wording, r3/F6.)
7. Selector boundary IDG powers are injected through the upstream `makeEffect` helper; they are synthetic test inputs.
8. Single-opponent fights do not exercise RNG, so the 5 seeds are identical.
9. Sealwright's numeric profile uses the Captain as a carrier, and preferences/elements are an open contract gate.
10. The harness bug found and fixed during development (no `leftSideUserIds`, which made both sides friendly to `friendlyFire: ENEMIES` effects) is covered by the hazard damage assertions.

## Live-game statement

Live-game requests 0. Writes 0. Asset-CDN requests 0. No credentials, cookies or session material. No game server, live DB or API. No browser or installed-client checks. The upstream engine working tree is unchanged, and no engine file was edited even in the scratch export.

## Explicitly not begun

Final rule freeze; Crowned support activation; tuning; the Crystal engine correction; the Sword baseline (operator capture needed) **[r1; superseded — settled by RUL-2026-10-11-004 in r2]**; manifest assembly; art; publication.

## Revision r2 (2026-10-11): accepted Katana baseline [superseded as review target by r3]

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
- **Results [r2; combat figures superseded by r3]:** `run.sh` → 68 pass, 0 fail, 141 expect() calls. Evidence assertions: A1 160, A2 25, B1 4, B2 7, B3 10, C1 4, C2 16, C3 12, all with 0 failed. M0 482/482. Two runs produced byte-identical evidence. A1, A2, B1 and B2 evidence is unchanged from r1.
- **C3:** PASS for mechanics and economy. Presentation (description, battle description, image, effect animation/SFX) remains pending.
- **New observation:** `fetchUserItems` excludes hidden items, so a still-hidden Katana is invisible to `imbueItem`.
- Live-game requests 0, writes 0. No engine, art or manifest change.

## Revision r3 (2026-10-11): correction pass for ChatGPT's r2 review (F1–F6)

- **Reviewed target:** r2 `2c64c9e5a99bccc47d95ef852add1fe0daba5916`. Review verdict: REQUEST CHANGES. The review branch `chatgpt/review-ghost-ship-stage2-r2-20261011` (commit `7b7d7242…`) was local-only and was not fetched; the findings were applied as relayed by the user.
- **Base for r3:** r2 `2c64c9e5…`. `main` was verified at `50f980f08dfcc798723c26243b9399cc0a97911a` (no newer commit). The r3 head is the commit that adds this section; its exact SHA is in the delivery message.
- **Scope:** harness correctness, metrics and gate enforcement only. No accepted membership, ruling, reward value, rule array or tuning changed. No engine file was edited, including in the scratch export.

**Correction ledger**

| Finding | Fix | Where | Proof |
| --- | --- | --- | --- |
| **F1 — HIGH** battle-start caps missing | `assembleBattle` now reproduces `initiateBattle`'s preprocessing. It deep-clones each user, applies `capUserStats(user, user.rank)` (QUEST is not ranked; the captured quest `opponentAIs` carry no `scaleStats`, so no scaling or distribution applies), then calls `processUsersForBattle`, `applyPoolAdjustmentsToBase` for pool effects, `refreshMasteries` and the aggressor flag. Captured records are untouched | `engine/lib/sim.ts` | A1 asserts for all 11 AIs that battle offence/defence/generals/masteries = min(stored 0056 value, JONIN cap). A2 asserts the same for the Captain and the Sealwright carrier. All AIs are JONIN; every generals value is capped to 400,000; Core Canister's offence/defence 1,329,367 → 1,300,000. A1 and A2 were regenerated |
| **F2 — HIGH** failed evidence did not fail execution | `Evidence.flush` sets `process.exitCode = 1` on any failed check. `requireClean(...)` is the last test of every gate file and fails `bun test` on a failed or empty gate. `run.sh` re-checks every required evidence file with `tools/check_evidence.py` and exits nonzero if bun, the evidence check or the self-test fails | `engine/lib/report.ts`, all four test files, `run.sh`, `tools/check_evidence.py` | `selftest/run_negative.sh` runs on every `run.sh`. Four probes all exit 1 as required: synthetic `failed:1` evidence; a missing gate file; `bun test` on a file with a deliberately failed `Evidence.check` (fails in `requireClean`: `+ "deliberate failure"`); and the evidence that run wrote |
| **F3 — MEDIUM** A2 metric definitions | Damage is attributed from whole-step HP deltas, so delayed ticks count. The deltas reconcile exactly to final − initial HP (asserted), and player kits have no health cost or self-damage (asserted). Stun presence is reported apart from the engine AP reduction (`calcApReduction`) and full lockout (reduction ≥ 100). Clears are counted as removing or empty from a state diff of positive removable effects. There is one round-start sample per distinct round; the terminal state is kept separately | `engine/lib/sim.ts`, `engine/a2_sealwright.test.ts` | The Captain's delayed 505-HP ticks now count (e.g. JONIN-cap buffer/striker 4040 → 5050 = 4040 direct + 1010 delayed). Full lockout is 0 in all 120 fights. Empty Clears are reported (3–6 per fight vs strikers). Sample distinctness is asserted |
| **F4 — MEDIUM** cadence denominator | `FightResult.measuredRounds` is the completed interval (maxRounds when the cap is hit); cadence divides by it. The out-of-interval round-21 sample is no longer taken | `engine/lib/sim.ts`, `engine/a1_kits.test.ts` | A1 asserts a full 20-round interval with the dummy alive for every kit-only/candidate run |
| **F5 — MEDIUM** observations without assertions | Exact assertions: Consume shield present in rounds r..r+3 (3,3,2,1) and gone at r+4; immunity window [true,true,true,false]; blocked attempts leave no Buff Prevent; a power-100 Buff Prevent lands after the window; full per-round Katana cooldown and shared-GCD lock/release patterns; all 24 imbue/craft rank × rarity cells against a source-derived table; the exact slot-limit rejection; Pierce-vs-shield HP equality. A2 recorded-only checks were replaced too (B32 no-pool fall-through, exact Clear GCD [false,false,true,true], newly cast IDG removal, B16 AP timeline [0,20,20,0]) | `engine/c_katana.test.ts`, `engine/b_crystal.test.ts`, `engine/a2_sealwright.test.ts` | No `check(..., true)` remains. B3 14 and C2 18 assertions, all passing. B3/C2 recorded data are unchanged from r2 |
| **F6 — LOW** wording and stale prose | "every guard passed" → "tested pre-write eligibility guards passed; persistence/concurrency guards not run". The r2 claim that `state/` and `RULINGS.md` were unchanged is corrected. Superseded r1 statements are labelled. The stale "Build acceptance gates still open" list in `state/ghost_ship_skyglass_reward_decisions.md` now marks the Sword baseline (RUL-2026-10-11-004) and the Katana offline tests (C1–C3) closed and adds Katana presentation as open; no approved value changed | this file, results report, harness README, reward decisions | — |

**What changed in the conclusions (results report §3–§4 replace r2):**

- Cadence damage (capped, ÷20) moves by −30.5% to +1.6% per AI and variant. The Captain is hit hardest (1550 → 1078, −30.5%), then the Crowned Captain (about −21%). Minions out-damage the Captain 3.9–11.6× (candidate rules).
- The reviewer's counterexamples reproduce exactly. Durable striker: the Captain wins 5/0 in 22 rounds, and Sealwright now **loses 0/5 in 31** (r2: won in 23). JONIN-cap striker: Captain 5 → 10 rounds, Sealwright 9 → 13. Durable buffer vs Sealwright: 27 → 39 rounds.
- Sealwright spikes 6–24% vs the Captain's 8–30% of max HP per action, and fights run 1.3–3.5× longer. Stun never fully locks the player out for either boss. Sealwright's Clears are empty against damage-only players.
- Unchanged: every selector outcome (thresholds, distance gate, GCD, targeting, blocked path, IDG states), hazard timing, Crowned dormancy (proposal: 3.5 → 4.0 rounds, boss HP 94.3% → 87.2%), and all B/C conclusions.

**Exact execution and provenance (r3).** Engine `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` via `git archive` into the git-ignored `.work/`. `bun.lock` sha256 `da6602f2550bea9f1baf8508fa82b03d320bfcee269257f36cf25b47f1906c08`. `bun install --frozen-lockfile --ignore-scripts` (user-approved for this pass). bun 1.4.2, node v22.22.0, python 3.13.16. Tests ran under `unshare -rn` with the upstream placeholder environment and no database. Before any change, r2 was reproduced here byte-identically (68 pass / 141 expect(); all nine evidence files equal to the committed ones).

```text
TNR_OUT=<scratch>/r3a harness/ghost_ship_stage2/run.sh   → exit 0
  M0 PASS: 482 checks, 0 failed
  bun test: 73 pass, 0 fail, 174 expect() calls, Ran 73 tests across 4 files
  evidence m0/a1/a2/b1/b2/b3/c1/c2/c3: clean
  assertions: a1 207, a2 39, b1 4, b2 7, b3 14, c1 4, c2 18, c3 12 — all 0 failed
  negative self-test: 4/4 probes exit 1 (as required)
harness/ghost_ship_stage2/run.sh   (second run → results/)  → exit 0; all nine evidence files byte-identical to the first run
python3 harness/ghost_ship_stage2/tools/build_katana_record.py --check → current
```

`results/provenance.json` records the harness file hashes (now including `selftest/` and `tools/`) and the bun, evidence-check and self-test exit statuses. Doctrine, law, pack and generated-contract gates do not apply: no `skills/`, doctrine or generated file changed.

**Remaining director decisions (not technical fixes; unchanged by r3 except that parity must now be judged on r3 numbers):** Sealwright rule order, closing rule, 40-AP filler and parity acceptance; Crowned support activation; the candidate rule remap for the other nine AIs; minion duplicate innate IDG; Crystal engine-correction authorization, Consume-on-Consume behaviour and rarity/trading/crafting; Katana description, battle text, image and effect animation/SFX; re-baselining the legacy jutsu packet's protected hashes against push/86; optional deployed-version or `gameSetting` capture.

**Known limits still in force:** fixed start tiles and no random initial barriers; source-default `dmgConfig`; the turn loop replicates `performAction`'s inner loop; synthetic boundary IDG; single-opponent fights do not exercise RNG; Sealwright's numeric profile uses the Captain as carrier; B3 does not exercise persistence/concurrency guards.

**Not performed:** live-game requests 0, writes 0, asset-CDN requests 0. No credentials. No browser or client checks. No engine, art, manifest, publication or quest change. Nothing landed on `main`.

## Revision r4 (2026-10-11): non-blocking follow-ups from the r3 verification

- **Trigger:** ChatGPT verified r3 `79f435e8b0284ea275bcb89b819ac5f50f673507` as **PASS** for the scoped correction pass and closed F1–F6. Its review commit `0d44d01a…` (`chatgpt/review-ghost-ship-stage2-r3-20261011`) was local-only and not fetched; the follow-ups were applied as relayed. The PASS does not approve balance, Crystal production support, presentation, manifest assembly or publication.
- **Base:** r3 `79f435e8…`. `main` was verified at `50f980f08dfcc798723c26243b9399cc0a97911a`. The r4 head is the commit that adds this section.
- **Scope:** prose and the self-test wrapper only. No mechanics, test assertion, fixture or evidence value changed.

| Follow-up | Change |
| --- | --- |
| **R3-N1** empty-Clear wording | Results §4: against the damage-only fixture all Clears are S31 (B32 never cast). "The Clear component removes nothing against this damage-only fixture; S31 still deals damage." Routine S31 and conditional B32 are preserved |
| **R3-N2** negative-test wrapper | `selftest/run_negative.sh` checks preconditions (python3, bun, `unshare -rn`) and requires each failure to be the intended one. The checker probes must name the failure (`1 failed: bad`, `missing`). The bun probe's log must show 1 pass / 1 fail with the `requireClean` test failing on `"deliberate failure"`. The NEG artifact must exist with 2 checks and exactly that one named failure before it is fed to the checker. A new flush-only probe (`negative_flush_only.test.ts`: no `requireClean`, no `TNR_OUT`, log 1 pass / 0 fail) must still exit nonzero. Anything else is reported as INFRASTRUCTURE (exit 2) and fails `run.sh`; it is never counted as enforcement |
| **R3-N3** stale documentation | README layout row names the accepted Night's Testament-derived Katana record, with Flaming Sword as the Crystal/recipient carrier only. README and results §2 record that push/86 confirmed the 0056 conversion. Reward decisions: the "offline combat playback still remain[s] to be performed" sentence now says C1–C3 ran and passed verification |

**Wrapper proof.** Run outside `run.sh` (no placeholder environment), the bun probes crash at engine env validation. The r4 wrapper reports `INFRASTRUCTURE … did not run as intended` and exits 2; the r3 wrapper would have counted that crash as enforcement. Under `run.sh`, all five probes report `enforced`.

```text
TNR_OUT=<scratch>/r4a harness/ghost_ship_stage2/run.sh   → exit 0
  M0 PASS: 482 checks, 0 failed
  bun test: 73 pass, 0 fail, 174 expect() calls
  evidence m0/a1/a2/b1/b2/b3/c1/c2/c3: clean
  negative probes 5/5 enforced; run.sh: bun=0 evidence=0 negativeSelftest=0 -> exit 0
harness/ghost_ship_stage2/run.sh   (second run → results/)  → exit 0
  all nine evidence files byte-identical to the first run AND to r3
python3 harness/ghost_ship_stage2/tools/build_katana_record.py --check → current
```

Among the committed results only `results/provenance.json` (new self-test file hashes) and `results/bun_test.log` (run timings) changed. The engine pin, lockfile, runtime and isolation are as in r3. Live-game requests 0, writes 0, CDN 0, credentials none. No engine, ruling, reward value or rule change. Nothing landed on `main`.

**Ready for the director:** the remaining decisions are unchanged from r3. Judge them on the r3 measurements, and note that the five seeds repeat deterministic encounters; they are not independent win-rate samples.

