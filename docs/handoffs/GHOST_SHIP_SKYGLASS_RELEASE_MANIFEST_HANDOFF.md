# Handoff — Ghost Ship / Skyglass release manifest (push/90 + push/93) for independent review

**Implementer:** Fable (Claude Code). **Reviewer:** ChatGPT, at the exact SHA. **Decisions:** dauntless (RUL-2026-10-12-001…011).

## 1. Repository / refs

| Field | Value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Branch | `fable/ghost-ship-release-manifest-20261012` |
| Base (merge-base with `main`) | `afce6caa19393791b07ddd8d404f2fadb91cbb6e` |
| Head (review target) | **the commit that adds this file**: the branch head when this handoff was pushed. The handoff message quotes the exact SHA |
| Main when frozen | `7e3a80101942565cad6964053f31cf83153f5d16` (adds only push/92; no conflict) |
| Art commit (`imagePack.ref`) | `d61c990d2935df9c4acc1d4c57f412cbd77c4303` |
| Integration target | `main`, **after** review. The director chose to wait for review before push/90 reaches Forge |

## 2. Scope

**Objective:** one reproducible, offline-validated Forge release for the Ghost Ship / Skyglass expansion. Running it is operator-only.

**Primary review surface:**

| Path | Role |
| --- | --- |
| `push/90_ghost_ship_skyglass_release.gen.py` → `push/90_ghost_ship_skyglass_release.json` | Deterministic generator and its 50-entry final manifest (`--final --image-ref d61c990d…`) |
| `push/93_ghost_ship_sealwright_stats.gen.py` | Generates the post-run Sealwright stat edit from push/90's results bundle, with a literal id |
| `push/90_ghost_ship_skyglass_release.check.mjs`, `.rules.ts` | Forge pre-send check against live rows; engine `AiRule` parse |
| `harness/ghost_ship_release_dryrun/` | Headless ForgeCore dry run over FakeGame (27/27) |
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
6. 11 AI final edits (rename, kit, RUL-003 remap with RUL-009 gates, Crowned support, loot, boss IDG, new avatar) plus the Sealwright create.
7. Empty: Sealwright's post-0056 stats moved to push/93.
8. 2 quest edits: 83 nodes each, hidden:true, new icon.

Before and after: full captures.

**Not implemented / not done:**
- No run and no publication.
- Counter Stance and Battle Trance are left unedited (RUL-010).
- No replacement icon was supplied for Death's Door or Death's Grasp.
- Forge itself is unchanged: the `targetId` ref defect is worked around, not fixed.
- Spent manifests 65–92 are not archived on `main`.

## 3. Verification (exact commands, all from the repository root at the head SHA)

| Command | Result |
| --- | --- |
| `python3 push/90_ghost_ship_skyglass_release.gen.py --final --image-ref d61c990d2935df9c4acc1d4c57f412cbd77c4303 --check` | `OK: manifest and report are generator-exact` (50 entries; pending text 0, art 0; art coverage 34/34) |
| `node forge/tools/check_manifest.mjs push/90_ghost_ship_skyglass_release.json` | **0 pre-send problems, exit 0**, Forge manifest hash `e6c24afd`. The 8 warnings are captured gates on self-target stances |
| `node push/90_ghost_ship_skyglass_release.check.mjs` | 0 runtime-equivalent problems (edits validated against the captured live rows) |
| `(cd <engine export @585534d7>/app && bun --no-install run …/push/90_ghost_ship_skyglass_release.rules.ts "$PWD" …/push/90_ghost_ship_skyglass_release.json)` | 72 rules in 9 profiles, 0 failed; no change on round trip; every last rule is unconditional |
| `(cd forge && npm ci --ignore-scripts) && node harness/ghost_ship_release_dryrun/dryrun.mjs --out <dir>` | **27/27**; push/90 DONE, 50/50 VERIFIED, postflight 0 diff and 0 unresolved; push/93 generated from that run's bundle and VERIFIED. Two runs give byte-identical reports (`harness/ghost_ship_release_dryrun/results/dryrun_report.json`) |
| `(cd forge && npm test)` | 522/523. The one failure is pre-existing on `main`: push/79 sets `offence`/`defence` (no live row offline) |
| `python3 skills/producing-tnr-art/scripts/artpreflight.py <34 webps> --spec skills/producing-tnr-art/data/25x_DATA_art_spec.json` | 0 errors, 2 warnings (Serum 768px and quest icon 1202px oversize, non-blocking), 34 files. The 34 files match the director's SHA256SUMS, and `imagePack` sha256/bytes equal it |
| `python3 harness/ghost_ship_legacy_baseline/build_baseline.py --check` · `selftest.py` | OK · 6/6 |
| `python3 harness/ghost_ship_legacy_baseline/consumer_audit_selftest.py` | 8/8 |
| `python3 harness/ghost_ship_legacy_baseline/consumer_audit.py <push/81–84 results> --live-count harvests/inbox/tnr_results_1791772372237.json --accept-residual RUL-2026-10-12-011` | `ACCEPTED_RESIDUAL`: 535/535 read, live 506/522, 0 outside holders of edited jutsu |
| `TNR_REPO=$PWD python3 harness/ghost_ship_stage2/m0_verify.py --out x.json` | 482/0, byte-identical to all three committed frozen `m0.json` (the conversion packet is unchanged) |
| `harness/ghost_ship_final/run.sh` (r2, at `5e11d44c`) | M0 482/0, CONTRACT 19/0, GUARDS 24/0, ACTIVE 81/0, CROWNED 36/0; bun 45/0/218; two runs byte-identical |
| `python3 skills/building-tnr-content/scripts/validate.py push/90_… --strict` | **Not clean, by known classes** (draft doc §3): stale 45c/45d at `bdec2883` rejects live chest reward fields, effect `direction`/`description` and `farm*` nulls; build-order (law 60 sequence; `asset`→`gameAsset` ranks last); menu-shared-target on `d_parley` (live) and `d_recon_test` (approved lockout). L01 cleared |

## 4. Source / provenance

- **Engine:** `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`. This is upstream source; the deployed version is unverified (RUL-007).
- **Forge** under test: 0.5.0 behaviour (package 0.5.1), pinned field set `345d18ac`.
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

1. **Forge `targetId` refs are not resolved** (`forge/src/runner/runner.mjs:520`). The dry run found it, and it is worked around by push/93. Review that push/93 refuses every bundle except a DONE/success push/90 at hash `e6c24afd`. Between push/90 and push/93, Sealwright exists with placeholder offence and defence; the quests are hidden.
2. **The dry run is FakeGame, not the server.** It proves Forge's side only. Server-side `scaleEditedAi` (re-run on every AI edit) and `updateUserContent` are argued from source (draft doc §2) and are not executed. Synthetic seed rows: the Crown item, the 9 scene-asset shells and the post-0056 placeholder columns.
3. **Behaviour not measured offline:**
   - RUL-004 boss IDG 375/375/450;
   - RUL-009 gate normalisation, which collapses multi-band rules;
   - Sealwright, which RUL-002 accepted without new-pin testing.

   RUL-007 says calibration happens with a live tester while the quests are hidden.
4. **Residual consumers.** 16 live AIs were never read (RUL-011). Holders of Counter Stance and Battle Trance are unaffected (RUL-010).
5. **Placeholders and assumptions:**
   - Filament stackSize 5 and Reliquary `isEventItem:true` are mirrored, not ruled.
   - Scene folder `GhostShip`.
   - Quests are hidden by this run (they currently read hidden:false).
6. **validate.py classes not cleared** (§3). They need a separate contract regeneration with `schema_extract.py` and its adoption gate.
7. **The pre-existing Forge test failure** on push/79 shares the "no live row offline" class.

## 6. Live-game statement

- Agent live requests: 0. Agent game writes: 0.
- No credentials or session material used.
- All captures were operator-run and read-only.
- No browser, live-session, CDN or installed-client check was performed.
- Nothing was published.
- `main` received only the read-only capture manifests push/91 and push/92.

## 7. Operator sequence after review approval

1. Integrate into `main`.
2. Run push/90 in Forge and commit its results.
3. Run `python3 push/93_ghost_ship_sealwright_stats.gen.py --results harvests/inbox/<push/90 results>.json`, commit the output, then run push/93.
4. Tester calibration while the quests are hidden (RUL-007).
5. Publication is a separate director decision.
