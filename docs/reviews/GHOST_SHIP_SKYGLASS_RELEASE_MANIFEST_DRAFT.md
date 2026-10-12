# Ghost Ship / Skyglass — combined release manifest (push/90): final build

**Status:** FINAL BUILD COMPLETE (`--final --image-ref d61c990d2935df9c4acc1d4c57f412cbd77c4303`); INDEPENDENT REVIEW PENDING. Every input is supplied: director text (`224ab918`), 34 approved WebPs (intake `d61c990d`; 10 bound), fresh quest base (push/89), RUL-2026-10-12-001…011. Not run; no live request, write or publication.

**Date:** 2026-10-12. **Implementer:** Fable. **Decisions:** RUL-2026-10-12-001…008.

## 1. Files

| Path | Role |
| --- | --- |
| `push/90_ghost_ship_skyglass_release.gen.py` | Deterministic generator (`--draft` / `--final`, `--check`, `--gate-policy`) |
| `push/90_ghost_ship_skyglass_release.json` | Generated manifest (draft) |
| `state/ghost_ship_skyglass_release_manifest_report.json` | Generated ledger: per-AI kit/rule/loot/innate changes, gate audit, item chassis provenance, quest graph stats, input SHA-256s, pending slots |
| `push/90_ghost_ship_skyglass_release.check.mjs` | Forge gate with live rows: Forge's own parse/plan/Validator, each edit validated against its committed capture, AI merge replay |
| `push/90_ghost_ship_skyglass_release.rules.ts` | Parses every AI rule with the pinned engine `updateAiProfileSchema` |
| `state/ghost_ship_skyglass_release_presentation.json` | Director text (10 strings, approved at `224ab918`; effectPresentation null) |
| `state/ghost_ship_skyglass_release_art.json` | Art slots (10 required, pending the zip) |

## 2. What the manifest does (50 entries, executed by `phase`)

| Phase | Entries |
| --- | --- |
| 1 | 5 asset creates: Exterior Keel Walk, Reconstruction Chamber, Quarantined Archive, Command Observation Gallery (SCENE_BACKGROUND), Sealwright Scene Portrait (SCENE_CHARACTER), all hidden |
| 2 | 4 item creates, all hidden: Skyglass Filament; Skyglass Crystal (12 × `@item:skyglass_filament`); Skyglass Katana; Skyglass Reliquary (Filament 1 @100, Rare Jewels 3 @100, Filament 1 @25, Serum @30, Ornate Chest @15, `@item:skyglass_crystal` @3) |
| 3 | 9 scene-asset renames; item edits: Skyglass Serum (director text), Fragment of the Skyglass Crown, The Skyglass Crown |
| 4 | 6 AI edits removing the nine edited legacy jutsu from every Ghost Ship AI that holds one (law 18/60 unequip) |
| 5 | 9 legacy jutsu edits: name / description / battleDescription (+ the live `injectableInBattle`, law 20). Counter Stance and Battle Trance are not edited (RUL-2026-10-12-010) |
| 6 | 11 AI edits (rename, accepted kit, RUL-003 remapped rules, Crowned support prefix, loot, boss innate IDG) and the Sealwright create (regular Captain's profile, accepted 10-rule priority, `includeDefaultRules:false`, IDG 375, no loot) |
| 7 | (removed) Sealwright's post-0056 stats now come from **push/93**, generated from push/90's results with the literal created id. Forge does not resolve `@ai:` in `targetId`, a defect found by the dry run |
| 8 | 2 quest edits: retheme text, Fragment removed from `w_Co`, 12 rewires, 26 new nodes (83 per quest, six endings), `@ai:sealwright` battle, `w_secret` → `@item:skyglass_reliquary` ×1 @100, `hidden:true` |

Before/after captures: full reads of both quests, the 11 AIs and their profiles, the 11 jutsu, the 3 edited items and the 9 renamed assets.

**Loot and innate:** Captain h-V9/Msk 1 → 0; Crowned Fragment 10 → 20, h-V9/Msk 0, Katana 3 (new). Captain keeps increasestat 30 and gains IDG 375/99r; Crowned's 60/99r IDG becomes 450; Sealwright IDG 375. Minion innates are untouched.

**Sealwright profile:** Forge 0.5.0 pins its AI key set to engine `345d18ac`, which predates migration 0056. It refuses `offence`/`defence`/masteries on a create. They are therefore sent in a follow-up edit, which validates against the live row. Source arithmetic (`scaleUserStats`, level 100, experience 3,339,000) reproduces the Captain's 834,780 in every combat stat and mastery. Forge's lint L05 requires `preferredStat` on a create: the Captain's last value (Bukijutsu, October 1) is sent and the live server strips the obsolete column.

## 3. Gates (draft, `--gate-policy law40`, RUL-2026-10-12-009)

| Gate | Result |
| --- | --- |
| Generator self-checks | PASS. RUL-003 remap equals the reviewed harness ledger (`harness/ghost_ship_stage2/results/a1.json`, 11/11 AIs). Legacy jutsu before-text equals push/86 for all 11. Diadem absent. Crowned innate was the single 60/99r IDG. Quest graphs: 83 nodes, one root, all reachable, no forward cycles, battles dialog-gated, endings `w_A w_B1 w_B2 w_C w_Co w_secret` |
| `--check` | PASS: manifest and report are generator-exact |
| Engine rule schema (`rules.ts`) | PASS: 72 rules across 9 profiles; no change on a key-order-insensitive round trip; every last rule is unconditional |
| Forge `tools/check_manifest.mjs` | REFUSED only on 10 × L17: unbound art (expected until the zip). The 14 law-40 refusals are gone |
| Forge check with live rows, `--art-probe` (dummy sizes in memory only) | **0 problems**; 8 warnings (captured gates on self-target stances, kept under RUL-003) |
| `validate.py --strict` | Not clean. Every finding is classified below; none is a defect in the manifest's intended writes |

`validate.py --strict` findings:
- **Stale generated contracts.** 45c/45d come from engine `bdec2883`. They reject the `noncombatconsumereward` reward fields of every live chest, effect `direction`/`description`, and null `farm*` item keys. Forge's own field sets (`345d18ac`, per `forge/src/runner/validate.mjs`) and the pinned engine `ItemValidator` (harness CONTRACT gate) accept them. Fixing this means regenerating the contracts with `schema_extract.py`, a separate task with its own adoption gate.
- **Build order.** Two causes:
  - The law 60 sequence requires the AI unequip before the jutsu edits.
  - validate.py renames `asset` to `gameAsset` before its order lookup, so assets rank after every entity. Assets are placed last in the array for that reason. Forge orders by `phase` and refs either way.
- **L01 on the Sealwright follow-up:** a `@ai:` ref as `targetId`. Forge resolves it by planOrder.
- **Menu shares a target:**
  - `d_parley` is the live riddle, where two wrong answers lead to the duel; the retheme preserves its edges.
  - `d_recon_test`'s two wrong seals lead to the approved lockout (RUL-2026-10-10-003).
- **Unbound art:** 10 slots.

## 4. Distance gates: settled by RUL-2026-10-12-009 (Option A)

RUL-003 keeps every captured rule condition. The captured gates were tuned for the old legacy jutsu ranges. After the remap, 14 `distance_lower_than` gates on pool jutsu sit **below** range+1:

- Oathkeeper Quick Strike: 2 vs 4.
- Arsenal Keeper:
  - Numbing Shot: 3 vs 6.
  - Twin Shot: 5 vs 6.
- Sentinel: Twin Shot at 2, 3 and 5 vs 6.
- Core Horror: Twin Shot at 2 and 5 vs 6.
- First Blade:
  - Rapid Fire: 2 vs 6.
  - Ion Lance: 3 vs 6.
  - Numbing Shot: 4 vs 6.
- Crowned Captain S31: 3 vs 4.
- Deck Warden Rapid Fire: 4 vs 6.
- Wayfinder Lunging Strike: 4 vs 5.

Law 40's text calls a gate at or below range safe; it only forfeits the outer band. Forge enforces exact equality and refuses the manifest.

- **Option A (CHOSEN), `--gate-policy law40`, now the default and required by `--final`:** set all 14 to range+1. Forge then accepts. Behaviour changes: these attacks fire from farther. Where one jutsu had several gated rules (for example Sentinel's Twin Shot at 2/3/5), the bands collapse, so the first rule always wins.
- **Option B (declined), keep captured gates:** change Forge's law 40 check to accept gate ≤ range+1. That is Lane A Forge code, needing a release build and independent review before the operator can run push/90.

## 5. Other placeholders (reversible; not ruled)

- **Filament** mirrors the Fragment chassis. `stackSize 5` is below the 12-Filament recipe; crafting sums every stack, so it works, but needs at least three stacks. Also `isEventItem false`, `slot NONE`.
- **Reliquary** mirrors the Endless Night Chest. `isEventItem true`; `stackSize 999`; `actionCostPerc 60`.
- **Scene assets** use folder `GhostShip` and `licenseDetails "TNR"`.

## 6. Still required before `--final`

1. ~~Fresh push/89 quest capture~~: done (`harvests/inbox/tnr_results_1791768613624.json`, Forge 0.5.0, 2026-10-12T01:30Z, DONE/success, 2/2 full reads). Both quests are identical to the October 1 capture: every top-level field and all 57 objectives match. Both read **`hidden:false`** with an expired window (2026-09-18 to 2026-09-21), contradicting the earlier hidden report. The generator now uses this capture as its default base and records the observed state; the quest edits assert `hidden:true`, so running push/90 hides both quests.
2. ~~Director text and art~~: done. Text at `224ab918`. Art: 34 director-approved WebPs committed at `d61c990d` (`art/ghost_ship_skyglass/`); all 34 match the handoff SHA256SUMS; canonical `artpreflight.py` gives 0 errors and 2 non-blocking oversize warnings. **All 34 are bound** (director, 2026-10-12: leave no old Ghost Ship art behind):
   - 10 required slots;
   - 11 renamed-AI avatars;
   - Crown, Fragment and Serum icons;
   - the quest icon on both quests;
   - 6 existing scene backgrounds and 3 existing portraits.

   `--final` now refuses if any WebP in `art/ghost_ship_skyglass/` is unbound. The imagePack (34 files, 6,833,826 bytes) equals the director's ledger. Still old, with no replacement art supplied: the custom icons of the Death's Door and Death's Grasp jutsu. Not Ghost Ship assets, so left as-is: the shared dialog-node and collect-item badges used by about 50 quests, and the default `avatarLight`.
3. ~~The §4 decision~~: settled (RUL-2026-10-12-009).
4. ~~Legacy jutsu hash re-baseline~~: done. `state/ghost_ship_legacy_jutsu_baseline_push86.json`; the generator refuses unless every jutsu-edit source row matches it.
5. ~~Consumer audit~~: resolved. RUL-2026-10-12-010 leaves Counter Stance and Battle Trance unedited (22 outside holders). For the nine edited jutsu, the census (535/535) found 0 outside holders. 16 live AIs remain unread (push/91 counted 522 vs 506 read); the director accepted that residual (RUL-2026-10-12-011). Verdict `ACCEPTED_RESIDUAL`. push/92 is no longer required.
6. Independent review of the frozen SHA; integration into `main` only afterwards.

## 7. Commands

```text
python3 push/90_ghost_ship_skyglass_release.gen.py --draft            # writes manifest + report
python3 push/90_ghost_ship_skyglass_release.gen.py --draft --check    # OK: generator-exact
node push/90_ghost_ship_skyglass_release.check.mjs --art-probe        # 0 problems (law40 default)
node forge/tools/check_manifest.mjs push/90_ghost_ship_skyglass_release.json   # REFUSED: 10 x L17 unbound art only, exit 1
(cd <engine export at 585534d7>/app && bun --no-install run <repo>/push/90_ghost_ship_skyglass_release.rules.ts "$PWD" <repo>/push/90_ghost_ship_skyglass_release.json)  # 72 rules, 0 failed
python3 skills/building-tnr-content/scripts/validate.py push/90_ghost_ship_skyglass_release.json --strict --ctors … --entities … --checks … --pool … --lints …   # findings per §3
```

## 8. Final gates (head after this commit)

| Gate | Result |
| --- | --- |
| `gen.py --final --image-ref d61c990d… --check` | OK, generator-exact; 50 entries; pending text 0, art 0 |
| imagePack vs director ledger | 10/10 sha256 + bytes equal; `imgSizes` equal to bytes |
| Forge runtime-equivalent check (`check.mjs`, no probe) | **0 problems**; 8 warnings (captured gates on self-target stances) |
| Forge `tools/check_manifest.mjs` | **0 problems**, exit 0, Forge manifest hash `e6c24afd` (50 entries; the Sealwright follow-up moved to push/93) |
| Engine rule parse | 72 rules, 0 failed |
| Consumer audit | `ACCEPTED_RESIDUAL` (RUL-2026-10-12-011); self-test 8/8 |
| Legacy baseline | `--check` OK; self-test 6/6; frozen M0 byte-identical ×3 |

Headless ForgeCore dry run: done, 27/27 (§9).

## 9. Headless Forge dry run (`harness/ghost_ship_release_dryrun/`)

The shipped ForgeCore ran against FakeGame, seeded from the committed captures, using the real art
bytes at `d61c990d`. Result: **27/27**.
- push/90: DONE, 50/50 items VERIFIED, postflight 0 diff and 0 unresolved.
- Image pack: 34/34 verified and 34 uploads recorded, with bytes equal to the pack.
- No `@ref` is left unresolved anywhere.
- Law-60 order holds: 6 unequips land before the first jutsu edit.
- Quests: 83 nodes each, hidden, new icon; the Sealwright battle and the Reliquary reward resolve to the created ids.
- push/93, generated from the run's own bundle, sets Sealwright's stats equal to the Captain's.

It found one real defect and it is fixed: the same-job `@ai:sealwright` `targetId` would have failed live. After the fix, Forge's own `tools/check_manifest.mjs` passes push/90 with **0 problems** (Forge manifest hash `e6c24afd`).

**Operator sequence:** run push/90, commit its results, then run `python3 push/93_ghost_ship_sealwright_stats.gen.py --results <push/90 results>`, then run push/93.

## 10. r2 after independent review of `5eb75123` (RUL-2026-10-12-012)

The four review corrections and the stat requirement are applied; see the handoff §0. In summary:
- **Item creates:** no item create sends the 0056-removed requirement columns.
- **Boss effects:** they are the server-parse fixed point (IDG has no `statTypes`; `increasestat` `"Highest"` becomes `"None"`).
- **Sealwright:** one full create without `preferredStat`, at 1,391,300 ×6 with `statsMultiplier: 5`. push/93 is retired; Forge 0.5.2 is required, and is a pending release.
- **Multipliers:** the 9 included existing AIs move to `statsMultiplier: 5`. Seal Charge and Core Canister are unchanged.

Gate STATS (`harness/ghost_ship_final` r3) executes the pinned save path and battle scaling. Every included AI enters unscaled fights, and quest fights scaled to a level-100 opponent, at exactly 1,300,000 / 400,000. Repeated saves are fixed points.

Gates: Forge `check_manifest` 0 problems (hash `628d60e4`), runtime check 0, rules 72/0, dry run 29/29, harness r3 clean ×2, Forge suite 526/526.

§§2, 8 and 9 above describe the earlier `5eb75123` state where they mention push/93 or the 51/50-entry follow-up. This section supersedes them.
