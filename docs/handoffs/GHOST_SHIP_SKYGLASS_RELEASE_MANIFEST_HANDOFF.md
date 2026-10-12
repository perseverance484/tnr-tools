# Handoff — Ghost Ship / Skyglass release manifest (push/90) for independent re-review (r2)

**Implementer:** Fable (Claude Code). **Reviewer:** ChatGPT, at the exact SHA. **Decisions:** dauntless (RUL-2026-10-12-001…012).

## 0a. Changes since the re-reviewed head `be15d7f4dac60cbb864085142b135a75d6de9bc4` (GS-R5)

- **GS-R5:** disposed by the director's release-specific exception, RUL-2026-10-12-013. It adds `push/90_ghost_ship_skyglass_release.validate_exception.py` and the ledger `state/ghost_ship_skyglass_release_validate_exception.json`.
- **push/90 manifest, generator, Forge code and harnesses are unchanged**: same sha256 `6b720542…`, Forge hash `628d60e4`. Only the ledger, the check tool, the ruling and documentation were added, so a narrow recheck suffices.
- **Non-blocking handoff corrections applied:** the dry-run count is 29/29, the Forge provenance is 0.5.2 pending, and risk 7 is the current suite state.

## 0. Changes since the reviewed head `5eb75123a3ef18012735ae7fcebab2f928734661`

| Review item | Fix | Evidence |
| --- | --- | --- |
| 1. Obsolete item requirement columns | The item creates no longer send the 8 `required*Offence/Defence` columns migration 0056 removed. The generator refuses any donor column absent from the live post-0056 item row (push/87 Heal Crystal III), except those 8 and the `craftingRequirements` relation | The push/90 item creates carry none. Dry-run check "new items carry no 0056-removed requirement column" |
| 2. Noncanonical boss effects | Every asserted AI `effects` array is the fixed point of the server's `insertAiSchema.effects` parse. IDG has no `statTypes`/`generalTypes` at 585534d7; `increasestat` `"Highest"` becomes `"None"` (`validators/combat.ts:140`) | STATS: parse(entry) == entry for the Captain, Crowned and Sealwright |
| 3. Obsolete `preferredStat` create/read-back conflict | Sealwright's create sends no `preferredStat`. **Forge 0.5.2:** lint L05 no longer requires it (0056 dropped the column) | `forge/test/post0056.test.mjs`; dry-run check "no AI save sent preferredStat" |
| 4. Incorrect two-stage Sealwright scaling | One full create with all six combat fields at 1,391,300 and `statsMultiplier: 5`, plus the Captain's masteries. push/93 is retired. **Forge 0.5.2** accepts `offence`/`defence`/masteries on a create (`AI_POST_0056_KEYS`) | STATS: stored 1,391,300 ×6, fights at the caps, repeated save stable. A control reproduces the defect: incomplete create gives offence/defence 30 |
| Stat requirement (RUL-2026-10-12-012) | `statsMultiplier: 5` on the 9 included existing AIs and Sealwright. Hazards untouched (10 / 20) | STATS: every included AI is stored at or above the caps; unscaled and level-100 quest fights enter at exactly 1,300,000 / 400,000; the hazards' stats and multipliers are unchanged |

**Forge 0.5.2 is a pending release** (`@x-release-pending 0.5.2`). After the merge, `release_pin.yml` must promote it, and the operator's loader must be on 0.5.2, **before** push/90 runs. Forge 0.5.1 refuses push/90's Sealwright create.

## 1. Repository / refs

| Field | Value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Branch | `fable/ghost-ship-release-manifest-20261012` |
| Base (merge-base with `main`) | `afce6caa19393791b07ddd8d404f2fadb91cbb6e` |
| Head (review target) | **the commit that adds this revision of this file**: the branch head when it was pushed. The handoff message quotes the exact SHA. Previous review target: `5eb75123…` |
| Main when frozen | `7e3a80101942565cad6964053f31cf83153f5d16` (adds only push/92; no conflict) |
| Art commit (`imagePack.ref`) | `d61c990d2935df9c4acc1d4c57f412cbd77c4303` |
| Integration target | `main`, **after** review. The director chose to wait for review before push/90 reaches Forge |

## 2. Scope

**Objective:** one reproducible, offline-validated Forge release for the Ghost Ship / Skyglass expansion. Running it is operator-only.

**Primary review surface:**

| Path | Role |
| --- | --- |
| `push/90_ghost_ship_skyglass_release.gen.py` → `push/90_ghost_ship_skyglass_release.json` | Deterministic generator and its 50-entry final manifest (`--final --image-ref d61c990d…`); Forge hash `628d60e4` |
| `forge/src/runner/{validate,lints}.mjs`, `forge/test/post0056.test.mjs`, `forge/package.json`, `forge_bundle.js`, `forge_loader_user.js` | Forge 0.5.2: post-0056 AI create columns, L05 without preferredStat (pending release) |
| `harness/ghost_ship_final/engine/release_stats.test.ts` | Gate STATS (r3): pinned-server save path and battle scaling/clamping |
| `push/90_ghost_ship_skyglass_release.check.mjs`, `.rules.ts` | Forge pre-send check against live rows; engine `AiRule` parse |
| `harness/ghost_ship_release_dryrun/` | Headless ForgeCore dry run over FakeGame (29/29) |
| `harness/ghost_ship_legacy_baseline/` | Post-0056 legacy jutsu re-baseline and the consumer audit (with self-tests) |
| `art/ghost_ship_skyglass/` | 34 director-approved WebPs plus `_provenance/` |
| `state/ghost_ship_skyglass_release_{presentation,art}.json`, `state/ghost_ship_legacy_jutsu_{baseline_push86,edit_scope,consumer_audit}.json`, `state/ghost_ship_skyglass_release_manifest_report.json` | Inputs and generated ledgers |
| `push/91_ai_live_count_recheck.json`, `push/92_ai_unknown_id_reads.json` | Read-only captures. Both are already on `main`; push/91 ran and push/92 is no longer needed |
| `docs/RULINGS.md` (RUL-2026-10-12-001…011), `docs/reviews/GHOST_SHIP_SKYGLASS_RELEASE_MANIFEST_DRAFT.md` | Decisions and the full results report |

**Also on the branch, previously reviewed or frozen:**
- Stage 2 r4 `harness/ghost_ship_stage2/` (`3f825562…`).
- 3/3 Consume `harness/ghost_ship_consume/` (`fcd79e5a…`).
- Final items + Crowned `harness/ghost_ship_final/`. r1 `4369f404…` was reviewed. **r2** (`5e11d44c…`: Heal Crystal III mirror plus the 12-Filament recipe, RUL-2026-10-12-005) has not had its own review and is in scope here.

**What push/90 does (by phase):**
1. 5 scene creates.
2. 4 item creates (Filament, Crystal with its 12-Filament recipe, Katana, Reliquary with its loot table).
3. 9 scene renames with new art; Serum, Fragment and Crown edits with text and art.
4. 6 law-60 unequips.
5. 9 legacy jutsu text edits.
6. 11 AI final edits (rename, kit, RUL-003 remap with RUL-009 gates, Crowned support, loot, canonical boss IDG, new avatar, and `statsMultiplier: 5` on the 9 included AIs) plus the Sealwright full create (six combat fields at 1,391,300, multiplier 5).
7. Empty (the follow-up is retired; Sealwright is one full create).
8. 2 quest edits: 83 nodes each, hidden:true, new icon.

Before and after: full captures.

**Not implemented / not done:**
- No run and no publication.
- Counter Stance and Battle Trance are left unedited (RUL-010).
- No replacement icon was supplied for Death's Door or Death's Grasp.
- Forge's `targetId` ref defect is not fixed (no longer exercised: push/90 has no ref-targeted edit). A full re-pin of Forge's field sets to 585534d7 was deliberately not done, because it would newly refuse staged pre-0056 manifests from other workstreams (push/47, 56, 61, 62).
- Spent manifests 65–92 are not archived on `main`.

## 3. Verification (exact commands, all from the repository root at the head SHA)

| Command | Result |
| --- | --- |
| `python3 push/90_ghost_ship_skyglass_release.gen.py --final --image-ref d61c990d2935df9c4acc1d4c57f412cbd77c4303 --check` | `OK: manifest and report are generator-exact` (50 entries; pending text 0, art 0; art coverage 34/34) |
| `node forge/tools/check_manifest.mjs push/90_ghost_ship_skyglass_release.json` (Forge 0.5.2 source) | **0 pre-send problems, exit 0**, Forge manifest hash `628d60e4`. The 8 warnings are captured gates on self-target stances |
| `node push/90_ghost_ship_skyglass_release.check.mjs` | 0 runtime-equivalent problems (edits validated against the captured live rows) |
| `(cd <engine export @585534d7>/app && bun --no-install run …/push/90_ghost_ship_skyglass_release.rules.ts "$PWD" …/push/90_ghost_ship_skyglass_release.json)` | 72 rules in 9 profiles, 0 failed; no change on round trip; every last rule is unconditional |
| `(cd forge && npm ci --ignore-scripts) && node harness/ghost_ship_release_dryrun/dryrun.mjs --out <dir>` | **29/29**; push/90 DONE, 50/50 VERIFIED; Sealwright created at 1,391,300 ×6 with multiplier 5; 9 included AIs written at 5; hazards 10/20; no `preferredStat`; no obsolete item column. Two runs give byte-identical reports |
| `(cd forge && npm test)` | **526/526** (3 new post-0056 tests; the push/79 compatibility failure that was pre-existing on `main` now passes) · `node build.mjs` bundle reproducible · `check_release_pin`, `check_bundle_budget`, `check_imports`, `check_boundaries` clean |
| `python3 skills/producing-tnr-art/scripts/artpreflight.py <34 webps> --spec skills/producing-tnr-art/data/25x_DATA_art_spec.json` | 0 errors, 2 warnings (Serum 768px and quest icon 1202px oversize, non-blocking), 34 files. The 34 files match the director's SHA256SUMS, and `imagePack` sha256/bytes equal it |
| `python3 harness/ghost_ship_legacy_baseline/build_baseline.py --check` · `selftest.py` | OK · 6/6 |
| `python3 harness/ghost_ship_legacy_baseline/consumer_audit_selftest.py` | 8/8 |
| `python3 harness/ghost_ship_legacy_baseline/consumer_audit.py <push/81–84 results> --live-count harvests/inbox/tnr_results_1791772372237.json --accept-residual RUL-2026-10-12-011` | `ACCEPTED_RESIDUAL`: 535/535 read, live 506/522, 0 outside holders of edited jutsu |
| `TNR_REPO=$PWD python3 harness/ghost_ship_stage2/m0_verify.py --out x.json` | 482/0, byte-identical to all three committed frozen `m0.json` (the conversion packet is unchanged) |
| `harness/ghost_ship_final/run.sh` (r3) | M0 482/0, CONTRACT 19/0, GUARDS 24/0, ACTIVE 81/0, CROWNED 36/0, **STATS 68/0**; bun 51 pass/0 fail/220 expects; two runs byte-identical; network-denied |
| `cd skills/building-tnr-content/data && python3 ../scripts/validate.py ../../../push/90_ghost_ship_skyglass_release.json` (with or without `--strict`) | Exit 1, **56 errors / 25 warnings**, all in the 9 approved classes of RUL-2026-10-12-013 |
| `python3 push/90_ghost_ship_skyglass_release.validate_exception.py` | **EXCEPTION HOLDS**: manifest sha256 `6b720542…`, validator and contract hashes, and the exact 81-line diagnostic multiset equal `state/ghost_ship_skyglass_release_validate_exception.json`. Negative probes (manifest byte change, a new unknown effect field, a ledger missing one diagnostic) each exit 1 |

## 4. Source / provenance

- **Engine:** `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`. This is upstream source; the deployed version is unverified (RUL-007).
- **Forge** under test: package and bundle **0.5.2** (pending release; the loader keeps released 0.5.1 with `@x-release-pending 0.5.2`). Pinned field set `345d18ac` plus the additive post-0056 AI create keys and L05 without `preferredStat`.
- **Captures:**

  | Capture | Contents |
  | --- | --- |
  | push/86 `tnr_results_1791727613862.json` | AIs, profiles and embedded jutsu |
  | push/87 `…1791766317760.json` | Heal Crystal III |
  | push/89 `…1791768613624.json` | Quests (hidden:false, expired window) |
  | push/81–84 `…1791771716198/1811766/1915726/1966137` | Census |
  | push/91 `…1791772372237.json` | Count 522 |
  | October 1 `…1790826836406.json` | Item and donor rows |
  | `…1789402842027.json` | Chest donor |

- **Generated artifacts were rebuilt by their producers, not hand-edited.** That covers push/90 and its report, the legacy baseline, the consumer audit, the final item records and the dry-run report.

## 5. Risk / debt (attack these)

1. **Forge 0.5.2 is required to run push/90.** It is a pending release. Run push/90 only after `release_pin.yml` promotes it, and the operator's Forge reports v0.5.2.
2. **The dry run is FakeGame, not the server.** Server-side `scaleEditedAi` and the battle scaling are now *executed* from pinned source by STATS. `updateUserContent` (the kit sync) is still argued from source, not executed. Synthetic seed rows: the Crown item, the 9 scene-asset shells and the post-0056 placeholder columns.
3. **Behaviour not measured offline:**
   - RUL-012 multiplier 5: the stats are proven, the fight difficulty is not;
   - RUL-004 boss IDG 375/375/450;
   - RUL-009 gate normalisation, which collapses multi-band rules;
   - Sealwright, which RUL-002 accepted without new-pin testing.

   RUL-007 says calibration happens with a live tester while the quests are hidden.
4. **Residual consumers.** 16 live AIs were never read (RUL-011). Holders of Counter Stance and Battle Trance are unaffected (RUL-010).
5. **Placeholders and assumptions:**
   - Filament stackSize 5 and Reliquary `isEventItem:true` are mirrored, not ruled.
   - Scene folder `GhostShip`.
   - Quests are hidden by this run (they currently read hidden:false).
6. **validate.py is not clean. It is under a release-specific exception (RUL-2026-10-12-013, GS-R5).** `push/90_ghost_ship_skyglass_release.validate_exception.py` must report `EXCEPTION HOLDS`. The contract regeneration (`schema_extract.py` plus its adoption gate) is a separate Lane A follow-up.
7. **Forge suite:** 526/526 at this target. The push/79 compatibility case that failed on `main` now passes under 0.5.2.

## 6. Live-game statement

- Agent live requests: 0. Agent game writes: 0.
- No credentials or session material used.
- All captures were operator-run and read-only.
- No browser, live-session, CDN or installed-client check was performed.
- Nothing was published.
- `main` received only the read-only capture manifests push/91 and push/92.

## 7. Operator sequence after review approval

1. Integrate into `main`.
2. Let `release_pin.yml` promote Forge 0.5.2, and confirm the operator's Forge shows v0.5.2. Confirm `python3 push/90_ghost_ship_skyglass_release.validate_exception.py` reports EXCEPTION HOLDS on the merged tree.
3. Run push/90 in Forge and commit its results.
4. Tester calibration while the quests are hidden (RUL-007).
5. Publication is a separate director decision.

## 8. Release outcome and session closeout (2026-10-12)

The release is applied live. All Ghost Ship / Skyglass content is in place, and both quests remain **hidden**. The director merged each step to `main` without the independent recheck.

| Step | Main commit | Results | Outcome |
| --- | --- | --- | --- |
| Merge push/90 + Forge 0.5.2 | `b62704c` (pin `ae77aa1`) | — | Forge loader promoted to 0.5.2 |
| Run push/90 | `760585b` | `tnr_results_1791779642866.json` | 48 match, 1 drift, 1 error (below) |
| push/93 "Guardian" repair | `52471a5` | `tnr_results_1791780626532.json` | quests ok; AI rename refused (`Guardian` taken) |
| push/94 "Skyglass Sentinel" repair | `11a7c1e` | `tnr_results_1791780861916.json` | DONE/success, 3/3 match |

- **The push/90 error.** The rename of AI `3V_gdHYaclMB1gTyOPAbV` to "Sentinel" was refused because another live AI owns that username. `updateAi` syncs the kit before the userData update, so the kit landed and nothing else did.
  - push/93 also failed: "Guardian" is taken too.
  - push/94 applied the full push/90 edit under the name **Skyglass Sentinel**. All 6 asserted keys match (username, jutsus, rules, includeDefaultRules, statsMultiplier 5, avatar), and the stored combat stats are 1,391,300.
  - The quests carry push/90's original "the Sentinel" text again. Rulings: RUL-2026-10-12-014 and RUL-2026-10-12-015.
- **The push/90 drift.** Skyglass Crystal `Cmo3JU-D9Nl_-xUxrvEJN` `craftingRequirements` reads back `undefined` because `item.get` does not return the relation.
  - The server stores the recipe after the guarded update (`item.ts:646-662` at 585534d7).
  - The director confirmed in the in-game editor that the recipe is 12 × Skyglass Filament `CTZ1mwhHrICLtiCaZATY6`. Resolved.
- Sealwright was created as `RBW5KsIXmTGR710D2y2Y7`.
- The design state names the AI "Sentinel" in `state/ghost_ship_retheme_patch.json` aiRenames, but the live username is "Skyglass Sentinel". The rename is owned by RUL-2026-10-12-015 and push/94. push/90 and its design state stay as spent release history.

**Open items (none blocking; not started):**
1. Offline audit of the other push/90 after-captures, beyond Forge's VERIFIED verdicts: the 8 other AIs at multiplier 5, the hazards at 10/20, and the items.
2. Forge `VERSION` label: `forge/src/main.mjs` still says `forge 0.5.1` while the package and bundle are 0.5.2 (Lane A).
3. Lane A refresh of `validate.py` and 45c/45d/45g to 585534d7. That retires the per-manifest exceptions (RUL-013/014/015).
4. A Forge capture path for `item.getItemWithCraftingRequirements`, so recipe edits can be verified.
5. Archive the spent manifests push/65–94. push/92 was never run.
6. Hidden tester calibration (RUL-007). Publication is a separate director decision and is **not authorized**.

**Live-game statement:** agent live requests 0, agent game writes 0, no credentials. Every write was an operator-run Forge job. The global `state/active-context.md` / `state/status.json` (September Forge work) were not touched, and `session_close.py` was not run, per the workstream brief.
