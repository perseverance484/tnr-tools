# Skyglass treasure hunts, solo: report 2 (2026-10-28, RUL-2026-10-28-013)

This report supersedes report 1 below. Report 1's results files were overwritten by this run.

## What changed

**Inputs merged:**
- The fixed shared library: fable/skyglass-wreck-sim `5f6c3edb`. Lines is now a true fan, Seal Lines a diagonal cross,
  and Scatter A/B complementary halves. Blasts have cooldown 2. Violet blasts lock with non-shared types.
- The Wreck agent's `sim.ts` working-tree change, applied as is:
  - a virtual clock: `seedClock` from `seedEntropy`, `tickClock` once per action;
  - companion-pet support in `assembleFloor` (`pets` -> `processUsersForBattle` `petPreload`).

**Tide Line:** the fixed library still has no character-target push row, so Tide Line stays damage only.

### 1. Archive alarm guard

- **Record:** the Crown Archivist, Crownhold D3.REG1 (Skyglass Archive Keeper), live id `LZiunyinw9ScK3mh9HiR2` from
  `state/crownhold/ids.json`.
- **Source:** the row is the push/272 create payload, with the live readback stats (812,519.2 in every combat stat)
  from `tnr_results_1792984876132.json`.
- **Kit and rules:** its live Crownhold kit and rules, unchanged.
- **Alarm fights:** now Crown Archivist + Seal Charge under ALARM. The generator needs the Archivist in its `AI` map and
  in the alarm fight's `fight` list.
- **Cache Sentinel:** unchanged.
- **Tuned:** pools 2 (10,100 HP), 2 rows of +100% damage.
- **Caution:** the same live record is a Crownhold D3 regular. Upgrading it in place changes Crownhold too, unless the
  hunt gets its own copy (director call).

### 2. Sealwright and the Stonebound

- **The Sealwright** keeps Ward of Command, at pools 2.5 (12,625 HP) with 2 rows.
- **Called to the Archive** now summons Crown Stonebound:
  - Crownhold D3.REG4, live id `jqxu13kNHhfNY-NF68Ftb`;
  - its live record and rules, used as stored;
  - summon HP 15,000, more than the Sealwright's 12,625; 60% power; 3 rounds; one at a time.
- **Library bug found and patched for the hunts:**
  - Ward of Command's `decreasedamagetaken` row has `target: SELF`, inherited from its shape donor (Folding Screen
    Guard). So the ward always landed on the caster, whatever ally the rule picked.
  - This also means the dungeon Sealwright never warded the Captain.
  - The hunts use the same `lib-ward-of-command` record with that row's target set to `INHERIT` (validated).
  - Traced: the ward lands on the Stonebound whenever one is up, and on the Sealwright in the gaps.
  - The library owner needs to adopt the fix. It is listed in `hunts_spec.json` under `sharedKitFixes`.
- **Stonebound side effect:** its live Erupting Ground hits the Sealwright too, because its damage row is not
  enemies-only. This is shared Crownhold data, left as is.

### 3. First Blade fix

- The end-turn rule is the First Blade's last rule in `hunts_spec.json`.
- It is marked `SHARED KIT FIX for dg-first-blade`, and listed under `sharedKitFixes` for the Wreck agent's kit.

### 4. Pets

One modelled mid-rank companion joins the player in every hunt fight (`hunts.ts petFor`). It is the same model as the
Wreck harness's `petFor`; no pet record is captured.

| Field | Value |
|---|---|
| Rank | 5, "Hunter": the middle of a JONIN owner's allowed range (1-7) |
| Level | 30, the rank's cap |
| Stats | half the CHUNIN caps, spread evenly |
| Species | COMMON ASSAULT, no passives, no pet jutsu |
| AI | the engine's default rules: close in, basic attack |
| Spawn | behind the owner |

- **How it enters battle:** the engine's own `addPetsToBattle` builds the actor. It is a summon-like ally with
  calcHP(30) HP, fresh in every fight; pet HP does not carry between fights.
- **Effect:** its hits are tiny (4-22 damage). Its effect is as a target: enemies whose rules aim at the
  `CLOSEST_OPPONENT` often hit the pet.
- **Measurement gap:** the engine does not credit `damageDealt` to pet actors, so pet damage reads 0 in the results.
- **Seal Charges** also detonate on the pet.

### 5. Retune for the merged library and the pet

| Record | Report 1 | Report 2 |
|---|---|---|
| Foundry Warden | pools 1.5, 2 rows | pools 2.5 (12,625 HP), 1 row |
| Sealwright | pools 2, 2 rows | pools 2.5, 2 rows (ruling) |
| Crown Archivist | - | pools 2, 2 rows |
| Called to the Archive | Sentinel echo, 3,000 HP | Stonebound, 15,000 HP, 60% |

Every other stat is unchanged from report 1. The Captain is still within the dungeon Captain: same kit, pools 2, 4 rows.

## Results (40 seeds per path, pet on; dodge on and off)

### Summary

| Path | Win (dodge on) | End HP median [p10] | Rounds total | Lost at fight | Win (dodge off) | End HP (off) |
|---|---:|---|---:|---|---:|---|
| foundry | 32/40 | 51.9% [7.7] | 16.5 | F3: 8 | 14/40 | 32.6% |
| archive_clean | 32/40 | 48.1% [19.8] | 21.5 | F2: 8 | 0/40 | - |
| archive_alarm1 | 29/40 | 23.4% [9.1] | 27 | F2: 2, F3: 9 | 0/40 | - |
| archive_alarm3 | 15/40 | 22.6% [5.8] | 37 | F2: 2, F4: 7, F5: 16 | 0/40 | - |
| watch_000 | 37/40 | 68.9% [55.5] | 19 | F3: 3 | 15/40 | 56.7% |
| watch_100 | 34/40 | 65.8% [31.9] | 28 | F1: 3, F3: 3 | 8/40 | 38.3% |
| watch_010 | 38/40 | 68.9% [55.5] | 19 | F3: 2 | 29/40 | 53.5% |
| watch_110 | 31/40 | 68.9% [49.1] | 28 | F1: 3, F3: 6 | 9/40 | 29.8% |
| watch_001 | 37/40 | 45.4% [32] | 19 | F3: 3 | 15/40 | 52.3% |
| watch_101 | 34/40 | 45.4% [25.5] | 28 | F1: 3, F3: 3 | 7/40 | 55.5% |
| watch_011 | 38/40 | 45.4% [32] | 19 | F3: 2 | 29/40 | 48.7% |
| watch_111 | 31/40 | 45.4% [26.6] | 28 | F1: 3, F3: 6 | 9/40 | 25.5% |
| cache_right | 40/40 | 99.8% [56.8] | 9 | none | 40/40 | 72.4% |
| cache_wrong | 40/40 | 99.2% [56.8] | 13.5 | none | 40/40 | 71.7% |

### Per fight

| Path | Fight | Won / reached | Rounds median [p10-p90] | HP start -> end (median, p10 end) | Gross HP lost | Player idle turns | Won / reached (off) | HP end (off) |
|---|---|---:|---|---|---:|---:|---:|---|
| foundry | intake: Deck Warden + Core Canister | 40/40 | 6 [1-6] | 100 -> 88.9 (81) | 11.1% | 3.3% | 40/40 | 88.9 |
| foundry | pour hall: Arsenal Keeper + Seal Charge x2 | 40/40 | 6 [3-7] | 88.9 -> 81.2 (55.1) | 11.4% | 2.3% | 40/40 | 81.2 |
| foundry | crucible: Foundry Warden + Core Canister **(boss)** | 32/40 | 7 [6-9] | 81.2 -> 51.9 (7.7) | 40.2% | 13% | 14/40 | 32.6 |
| archive_clean | descent: Core Horror | 40/40 | 7 [7-7] | 100 -> 109 (109) | -9% | 0% | 23/40 | 33.6 |
| archive_clean | archive: Sealwright **(boss)** | 32/40 | 14.5 [10-16] | 109 -> 48.1 (19.8) | 60.9% | 0.4% | 0/23 | - |
| archive_alarm1 | descent: Core Horror | 40/40 | 7 [7-7] | 100 -> 109 (109) | -9% | 0% | 23/40 | 33.6 |
| archive_alarm1 | alarm 1: Crown Archivist + Seal Charge (alarm debuff) | 38/40 | 8 [5-8] | 109 -> 64.5 (57.5) | 43.5% | 1.9% | 11/23 | 32.2 |
| archive_alarm1 | archive: Sealwright **(boss)** | 29/38 | 15 [10-15] | 64.6 -> 23.4 (9.1) | 55.5% | 2.2% | 0/11 | - |
| archive_alarm3 | descent: Core Horror | 40/40 | 7 [7-7] | 100 -> 109 (109) | -9% | 0% | 23/40 | 33.6 |
| archive_alarm3 | alarm 1: Crown Archivist + Seal Charge (alarm debuff) | 38/40 | 8 [5-8] | 109 -> 64.5 (57.5) | 43.5% | 1.9% | 11/23 | 32.2 |
| archive_alarm3 | alarm 2: Crown Archivist + Seal Charge (alarm debuff) | 38/38 | 7.5 [5-8] | 64.6 -> 54.9 (20.9) | 30.7% | 1.2% | 8/11 | 33.1 |
| archive_alarm3 | alarm 3: Crown Archivist + Seal Charge (alarm debuff) | 31/38 | 6 [1-8] | 54.9 -> 36.8 (14.3) | 8.5% | 0.5% | 6/8 | 31 |
| archive_alarm3 | archive: Sealwright **(boss)** | 15/31 | 10 [10-15] | 36.8 -> 22.6 (5.8) | 27.7% | 0.9% | 0/6 | - |
| watch_000 | chart room: Wayfinder | 40/40 | 4 [4-5] | 100 -> 99.6 (67.2) | 0.4% | 0% | 40/40 | 93.4 |
| watch_000 | deck: First Blade | 40/40 | 6 [6-7] | 99.6 -> 105.2 (83.1) | -5.4% | 0% | 40/40 | 76.2 |
| watch_000 | helm: The Captain **(boss)** | 37/40 | 9 [6-10] | 105.2 -> 68.9 (55.5) | 31.1% | 11.3% | 15/40 | 56.7 |
| watch_100 | chart room: Wayfinder (term: elementalseal) | 37/40 | 12 [12-17] | 100 -> 81.2 (36) | 18.8% | 20.1% | 31/40 | 49.9 |
| watch_100 | deck: First Blade | 37/37 | 6 [6-7] | 81.2 -> 91.6 (48) | -13.3% | 0% | 27/31 | 34.4 |
| watch_100 | helm: The Captain **(boss)** | 34/37 | 9 [6-10] | 91.6 -> 65.8 (31.9) | 31.1% | 11.5% | 8/27 | 38.3 |
| watch_010 | chart room: Wayfinder | 40/40 | 4 [4-5] | 100 -> 99.6 (67.2) | 0.4% | 0% | 40/40 | 93.4 |
| watch_010 | deck: First Blade (term: disarm) | 40/40 | 6 [6-7] | 99.6 -> 105.2 (83.1) | -5.4% | 0% | 40/40 | 76.2 |
| watch_010 | helm: The Captain **(boss)** | 38/40 | 9 [6-10] | 105.2 -> 68.9 (55.5) | 31.1% | 12.9% | 29/40 | 53.5 |
| watch_110 | chart room: Wayfinder (term: elementalseal) | 37/40 | 12 [12-17] | 100 -> 81.2 (36) | 18.8% | 20.1% | 31/40 | 49.9 |
| watch_110 | deck: First Blade (term: disarm) | 37/37 | 6 [6-7] | 81.2 -> 91.6 (48) | -13.3% | 0% | 27/31 | 34.4 |
| watch_110 | helm: The Captain **(boss)** | 31/37 | 9 [6-10] | 91.6 -> 68.9 (49.1) | 31.1% | 9.1% | 9/27 | 29.8 |
| watch_001 | chart room: Wayfinder | 40/40 | 4 [4-5] | 100 -> 99.6 (67.2) | 0.4% | 0% | 40/40 | 93.4 |
| watch_001 | deck: First Blade | 40/40 | 6 [6-7] | 99.6 -> 105.2 (83.1) | -5.4% | 0% | 40/40 | 76.2 |
| watch_001 | helm: The Captain (term: healprevent) **(boss)** | 37/40 | 9 [6-10] | 105.2 -> 45.4 (32) | 54.6% | 11.3% | 15/40 | 52.3 |
| watch_101 | chart room: Wayfinder (term: elementalseal) | 37/40 | 12 [12-17] | 100 -> 81.2 (36) | 18.8% | 20.1% | 31/40 | 49.9 |
| watch_101 | deck: First Blade | 37/37 | 6 [6-7] | 81.2 -> 91.6 (48) | -13.3% | 0% | 27/31 | 34.4 |
| watch_101 | helm: The Captain (term: healprevent) **(boss)** | 34/37 | 9 [6-10] | 91.6 -> 45.4 (25.5) | 54.6% | 11.5% | 7/27 | 55.5 |
| watch_011 | chart room: Wayfinder | 40/40 | 4 [4-5] | 100 -> 99.6 (67.2) | 0.4% | 0% | 40/40 | 93.4 |
| watch_011 | deck: First Blade (term: disarm) | 40/40 | 6 [6-7] | 99.6 -> 105.2 (83.1) | -5.4% | 0% | 40/40 | 76.2 |
| watch_011 | helm: The Captain (term: healprevent) **(boss)** | 38/40 | 9 [6-10] | 105.2 -> 45.4 (32) | 54.6% | 12.9% | 29/40 | 48.7 |
| watch_111 | chart room: Wayfinder (term: elementalseal) | 37/40 | 12 [12-17] | 100 -> 81.2 (36) | 18.8% | 20.1% | 31/40 | 49.9 |
| watch_111 | deck: First Blade (term: disarm) | 37/37 | 6 [6-7] | 81.2 -> 91.6 (48) | -13.3% | 0% | 27/31 | 34.4 |
| watch_111 | helm: The Captain (term: healprevent) **(boss)** | 31/37 | 9 [6-10] | 91.6 -> 45.4 (26.6) | 49.3% | 9.1% | 9/27 | 25.5 |
| cache_right | dig: Skyglass Sentinel **(boss)** | 40/40 | 9 [9-10] | 100 -> 99.8 (56.8) | 0.2% | 0% | 40/40 | 72.4 |
| cache_wrong | wrong cove: Deck Warden + Seal Charge | 40/40 | 4 [1-6] | 100 -> 101 (89.7) | -1% | 3.6% | 40/40 | 101 |
| cache_wrong | dig: Skyglass Sentinel **(boss)** | 40/40 | 9 [9-10] | 101 -> 99.2 (56.8) | 2.7% | 0.3% | 40/40 | 71.7 |

### Set pieces and behaviour

| Fight (first path seen) | Enemy | Appearances | Mark fired % | Marks / blasts per fight | Blast hit % (on / off) | Windows per fight | Signature % | Idle turns after r2 | Dealt per fight (on / off) |
|---|---|---:|---:|---|---|---:|---:|---:|---|
| intake: Deck Warden + Core Canister | Deck Warden | 40 | 0 | 0 / 0 | - / - | 0 | 42.5 | 0% | 816 / 816 |
| intake: Deck Warden + Core Canister | Core Canister | 40 | 0 | 0 / 0 | - / - | 0 | 90 | 44.4% | 1406 / 1406 |
| pour hall: Arsenal Keeper + Seal Charge x2 | Arsenal Keeper | 40 | 0 | 0 / 0 | - / - | 0 | 0 | 0% | 891 / 891 |
| pour hall: Arsenal Keeper + Seal Charge x2 | Seal Charge | 40 | 0 | 0 / 0 | - / - | 0 | 85 | 0% | 1489 / 1489 |
| crucible: Foundry Warden + Core Canister | Foundry Warden | 40 | 97.5 | 2.7 / 2.1 | 34.9 / 98.9 | 1 | 97.5 | 4.5% | 2864 / 5173 |
| crucible: Foundry Warden + Core Canister | Core Canister | 40 | 0 | 0 / 0 | - / - | 0 | 100 | - | 1326 / 1326 |
| descent: Core Horror | Core Horror | 40 | 100 | 2.1 / 2 | 5 / 95.9 | 0 | 100 | 0% | 1414 / 7522 |
| archive: Sealwright | Sealwright | 40 | 100 | 4.1 / 3.5 | 13.7 / 81.8 | 0.9 | 100 | 4.8% | 2778 / 3676 |
| archive: Sealwright | (clone or summon) | 40 | 0 | 0 / 0 | - / - | 0 | 0 | 0% | 0 / 0 |
| alarm 1: Crown Archivist + Seal Charge (alarm debuff) | Crown Archivist | 40 | 0 | 0 / 0 | - / - | 0 | 0 | 0% | 2357 / 2584 |
| alarm 1: Crown Archivist + Seal Charge (alarm debuff) | Seal Charge | 40 | 0 | 0 / 0 | - / - | 0 | 75 | 0% | 847 / 813 |
| alarm 2: Crown Archivist + Seal Charge (alarm debuff) | Crown Archivist | 38 | 0 | 0 / 0 | - / - | 0 | 0 | 0% | 2344 / 1974 |
| alarm 2: Crown Archivist + Seal Charge (alarm debuff) | Seal Charge | 38 | 0 | 0 / 0 | - / - | 0 | 60.5 | 0% | 615 / 531 |
| alarm 3: Crown Archivist + Seal Charge (alarm debuff) | Crown Archivist | 38 | 0 | 0 / 0 | - / - | 0 | 0 | 0% | 2114 / 2019 |
| alarm 3: Crown Archivist + Seal Charge (alarm debuff) | Seal Charge | 38 | 0 | 0 / 0 | - / - | 0 | 63.2 | - | 676 / 584 |
| chart room: Wayfinder | Wayfinder | 40 | 100 | 1.3 / 1.2 | 28.3 / 47.8 | 0 | 100 | 0% | 982 / 1305 |
| chart room: Wayfinder | (clone or summon) | 8 | 100 | 1.4 / 1 | 0 / 25 | 0 | 0 | 0% | 0 / 0 |
| deck: First Blade | First Blade | 40 | 100 | 2 / 1 | 0 / 100 | 0.7 | 100 | 38% | 844 / 2934 |
| helm: The Captain | The Captain | 40 | 100 | 3.5 / 1.6 | 4.6 / 45.8 | 0 | 100 | 0% | 3231 / 10287 |
| dig: Skyglass Sentinel | Skyglass Sentinel | 40 | 100 | 3.8 / 2.4 | 2.1 / 40.8 | 1 | 100 | 1.6% | 1570 / 3305 |
| wrong cove: Deck Warden + Seal Charge | Deck Warden | 40 | 0 | 0 / 0 | - / - | 0 | 35 | 0% | 680 / 680 |
| wrong cove: Deck Warden + Seal Charge | Seal Charge | 40 | 0 | 0 / 0 | - / - | 0 | 75 | 0% | 847 / 847 |

Dodge totals (all paths, dodge on): {"threatened": 2686, "dodged": 2455, "failedRooted": 149, "failedNoPath": 72, "failedOther": 6, "stepsTaken": 4332}


## Reading against the targets

- **Archive alarm paths:**
  - 1 alarm: **29/40** (target 25-30).
  - 3 alarms: **15/40** (target 15-20).
  - With dodge off, every Archive path is 0/40.
- **Archive boss is the costliest fight:**

  | Path | Sealwright | Alarm fights | Core Horror |
  |---|---|---|---|
  | Clean | 61% gross, 32/40 | - | -9% |
  | 1 alarm | 55% | 44% | -9% |

- **Foundry:** 32/40. The boss costs 40% gross (the earlier fights 11% each). 14/40 with dodge off.
- **Watch:** 31-38/40 across the eight term combinations.
  - The Captain is the costliest fight: 31% gross, 49% under healprevent. Every no-term loss is at the Captain.
  - **elementalseal** turns the Wayfinder into a 12-round fight and costs 3 runs there.
  - **disarm** does nothing to this build, which carries no weapon.
  - **healprevent** lowers end HP (69% -> 45%).
  - With dodge off: 7-29/40.
- **Cache: 40/40 on both coves, and the Sentinel now costs almost nothing** (0-3% gross, end HP 99%).
  - Cause: the Sentinel's rules target the closest opponent, and the pet spawned beside the player takes many of its
    hits.
  - The ruling keeps the Cache Sentinel unchanged, so it was not retuned. Making the Cache a real fight again needs
    the Sentinel retuned with pets in mind (director call).
- **Time readouts:** the console's "(Ns)" elapsed times are negative. The virtual clock replaces `Date`, which the
  runner also uses for timing. Battle results are unaffected.

---

# Report 1 (superseded): offline simulation and build spec (2026-10-28)

The four hunts (Drowned Foundry, Quarantined Archive, Captain's Watch, Buried Cache) played end to end by one endgame
player, through the game's own combat engine (pin `c86f43f4`), offline. Zero live requests, no credentials.

## Files

All files are new. Shared files were read, not modified.

| File | What it is |
|---|---|
| `engine/hunts.ts` | Hunt enemies (kits, rules, solo stats), quest debuffs, fight sequences |
| `engine/hunts_main.ts` | Runner: whole hunts with carried pools, per-fight traces, parameter sweeps |
| `engine/hunts_build.ts` | Writes `hunts_spec.json` |
| `overrides/hunts.params.json` | The tuned solo stats |
| `tools/hunts_tables.py` | Builds the tables below |
| `results/hunts_final.json` | Final results, dodge on |
| `results/hunts_final_nododge.json` | Final results, dodge off |
| `results/hunts_reference.json` | Reference runs |

## Commands

Full run (add `--no-dodge` for the dodge-off runs):

```bash
TNR_SCRIPT=hunts_main.ts harness/skyglass_wreck_sim/run.sh --params harness/skyglass_wreck_sim/overrides/hunts.params.json \
    --paths all --seeds 40 --out harness/skyglass_wreck_sim/results/hunts_final.json
```

Trace one fight of a path (path@fight@seed):

```bash
TNR_SCRIPT=hunts_main.ts harness/skyglass_wreck_sim/run.sh --params ... --trace "watch_111@2@5"
```

Trace one ad hoc fight at full pools:

```bash
TNR_SCRIPT=hunts_main.ts harness/skyglass_wreck_sim/run.sh --params ... --trace "fight:Sealwright@0@2"
```

Build the spec:

```bash
TNR_SCRIPT=hunts_build.ts harness/skyglass_wreck_sim/run.sh --params harness/skyglass_wreck_sim/overrides/hunts.params.json \
    --spec-out harness/skyglass_wreck_sim/hunts_spec.json
```

Build the tables:

```bash
python3 harness/skyglass_wreck_sim/tools/hunts_tables.py harness/skyglass_wreck_sim/results/hunts_final.json \
    harness/skyglass_wreck_sim/results/hunts_final_nododge.json
```

`--sweep <file.json>` runs a list of parameter cases. `run.sh` only resolves the path flags it knows, so pass the sweep
file as an absolute path.

## How a hunt is modelled

- **Each fight** is a plain QUEST battle, built the way a `start_battle` objective builds it:
  - one player against the fight's AIs;
  - `opponent_scaled_to_user` false, `keepOriginalPools` false, no `givePools`;
  - live damage settings.
- **Pools carry over** between fights:
  - `database.ts` writes the battle's `curHealth`/`curChakra`/`curStamina` back unclamped.
  - An isolated run keeps the account in status `BATTLE`. So the next `processUsersForBattle` adds no regeneration
    (`restored = 0`); it only clamps current pools to the maximum.
  - The Kitsune set's +1,200 max HP (static, 20 rounds) is applied again at every battle start through the delta model.
    **So each fight starts with up to +1,200 HP (+24% of 5,050) over what the last fight ended on.**
  - HP figures below are % of the base 5,050, so they can read above 100. "Gross HP lost" is start − end, including
    that +24%.
- **Debuffs:** ALARM and TERM from `push/skyglass_hunts.gen.py`, unchanged. They go on the player through the engine's
  own `addQuestStartingEffects`.
- **Losses:** a lost, drawn or stalled fight (60 rounds) fails the hunt (RUL-2026-10-25-010).
- **Player:** the harness `average` player:
  - level 100 Jonin, full Kitsune set;
  - nine level-25 PvE jutsu; Fire and Wind elements; no weapon;
  - auto-combat rotation plus the harness dodge rule: step off `tg_heavy`, `tg_control` and `tg_linger` hexes, and onto
    `tg_safe` stars, in at most 3 one-hex moves.
- **Runs:** 40 seeds per path, dodge on and dodge off.

## Paths

| Hunt | Path | Fights in order (boss in bold) |
|---|---|---|
| Drowned Foundry | foundry | Deck Warden + Core Canister; Arsenal Keeper + Seal Charge x2; **Foundry Warden + Core Canister** |
| Quarantined Archive | archive_clean | Core Horror; **Sealwright** |
| | archive_alarm1, archive_alarm3 | Core Horror; then 1 or 3 fights of Skyglass Sentinel + Seal Charge under ALARM; **Sealwright** |
| Captain's Watch | watch_XYZ, all 8 term combinations | Wayfinder (X: elementalseal); First Blade (Y: disarm); **The Captain** (Z: healprevent) |
| Buried Cache | cache_right | **Skyglass Sentinel** |
| | cache_wrong | Deck Warden + Seal Charge; **Skyglass Sentinel** |

## Kits

### Crew enemies: same enemies as the dungeon

These crew enemies use their shared endgame kit and rule list unchanged, as `engine/kits.ts` builds it at this branch's
base (`buildEndgame` with `kits_endgame.params.json`):
- Deck Warden
- Seal Charge
- Skyglass Sentinel
- First Blade
- Wayfinder
- Core Horror
- The Captain

Two adjustments:
- **Library ids.** The six crew additions (Chain Hook, Oath of Stillness, Chart Mark, Skyglass Aegis, Mending Seal,
  Ward of Command) are remapped from their `dg-*` ids to the identical library records (`lib-*`).
- **Stats only.** Only AI stats differ from the dungeon copies: `poolsMultiplier`, the number of +100% damage rows,
  and `statsMultiplier` for the two hazards.

No endgame kit exists for two hunt enemies:
- **Arsenal Keeper:** keeps its live kit and live rules.
- **Core Canister:** takes the encounters doc's Canister rules:
  - Core Rupture when a player is within 2;
  - Core Rupture from round 7, the live fuse;
  - otherwise it stands still.

### Hunt bosses

The hunt bosses follow section 4. They are built on the shared set-piece library (`engine/library.ts`,
`library_spec.json`, fable/skyglass-wreck-sim 4bd5356a, fast-forwarded into this branch). They follow the coordinator's
usage rules:
- each blast rule sits on top, on `has_effect <its marker> >= 1`;
- after a mark come `has_effect <marker>` -> a plain attack -> end turn, ahead of the other marks;
- marks cost 40 AP and blasts 100 AP;
- set-piece rules sit above the boss's shared rule list, and no shared rule is removed.

| Boss | Move | Library records or source | Notes |
|---|---|---|---|
| Foundry Warden | Pour Line | Omen: Lines + Eruption: Lines | |
| | Overpour | (Pour Line) | Under 50%, the Pour Line mark jumps ahead of Quench |
| | Quench + Cooling Shell | Omen: Last Light + Quench | The window rides on Quench |
| | Mould Cage | Chain Hook (library crew addition) | He moves to stand by his Core Canister |
| | Plain moves | His live push/262 kit | |
| Sealwright | Script Lines | Omen: Seal Lines + Binding: Seal Lines | |
| | Archive Lock | Omen: Last Light, Binding + Command Absolute | |
| | Called to the Archive | `hunt-called-to-the-archive` (**NEW**) | One echo: 3,000 HP, 60% power, 3 rounds |
| | He Lowers His Seals | Lowered Guard | Under 30%, once |
| | Ward of Command, Mending Seal, Fetters, and the rest | His shared rules | |
| Skyglass Sentinel | Tide Line A/B | Omen: Rows A/B + Eruption: Rows A/B | B only under 50% |
| | Low Tide | Lowered Guard | Once |
| | Shell Wall | Adamantine Fortress (LIVE `i4lGrYY5HNN2Q2GPToKUS`) | |
| | Counter Stance | His shared rules | |
| Wayfinder | Old coastline A/B | Omen: Scatter A/B + Eruption: Scatter A/B | 2-round pools; B under 50%; Chart Mark stays his first move |
| First Blade | Ring | Omen: Ring + Eruption: Ring | |
| | "That was new." | Lowered Guard | Under 25%, once |
| | Hold while veiled | Added end-turn rule | See "Doesn't work as designed" |
| The Captain | Section 1 kit, as is | The shared dungeon kit | No Sealwright, so no Ward |

### New-jutsu count

- **New beyond the library: 1.** `hunt-called-to-the-archive` (summon). Section 5a budgets it under "Summons (Recall,
  Called to the Archive)", but `library.ts` does not build it yet.
- **Library records the hunts use: 24.** They are listed in `hunts_spec.json` under `jutsuCount`.
- **Everything else** the hunts use is either:
  - a live jutsu used as it is, or
  - the shared `dg-*` endgame kits (the Captain's Broadside and Ship's Bell sets; the Core Horror's set).
- **Battle-log lines and animation placeholder ids** come from the library records; the summon uses `cc_recall`. Each
  record's ids are listed in `hunts_spec.json`.

## Tuned solo stats (`overrides/hunts.params.json`; live records upgraded in place)

All storable. Each row was replayed through `scaleEditedAi` and passes `insertAiSchema`. Pools multipliers are chosen
so HP is a whole number: 3.25 and 1.25 fail the schema's integer `curHealth`.

| Record | Level | statsMultiplier | Pools | HP | +100% damage rows |
|---|---:|---:|---:|---:|---:|
| Deck Warden | 100 | 5 | 1 | 5,050 | 0 |
| Arsenal Keeper | 100 | 5 | 1 | 5,050 | 0 |
| Seal Charge | 70 | **1** (was 10) | as live | 3,550 | 0 |
| Core Canister | 56 | **5** (was 20) | as live | 2,850 | 0 |
| Core Horror | 100 | 5 | 2 | 10,100 | 2 |
| Skyglass Sentinel | 100 | 5 | 3.26 | 16,463 | 2 |
| Wayfinder | 100 | 5 | 1.26 | 6,363 | 1 |
| First Blade | 100 | 5 | 1.5 | 7,575 | 2 |
| Sealwright | 100 | 5 | 2 | 10,100 | 2 |
| Foundry Warden | 100 | 5 | 1.5 | 7,575 | 2 |
| The Captain | 100 | 5 | 2 | 10,100 | 4 |

Context for these numbers:
- **Damage rows.** The live crew carry 4-5 stacked damage rows, about x12, and the solo player dies on the first crew
  fight with them. Rows are now 0 to 2 for crew and 4 for the Captain.
- **The Captain** stays within the dungeon Captain: the same kit, pools 2 against the dungeon's 2.5, and 4 rows against
  the dungeon's 4. Upgrading his record replaces his live effects (one +375% row and +30% stats) with the 4 rows.
- **The two hazards** are tuned through `statsMultiplier`. Their Core Rupture (pierce 180 plus a 2-round stun) was the
  biggest single solo threat.

## Results (40 seeds per path)

### Summary

| Path | Win (dodge on) | End HP median [p10] | Rounds total | Lost at fight | Win (dodge off) | End HP (off) |
|---|---:|---|---:|---|---:|---|
| foundry | 34/40 | 31.7% [17.8] | 18 | F3: 6 | 0/40 | - |
| archive_clean | 39/40 | 87% [49.3] | 20 | F1: 1 | 5/40 | 44.6% |
| archive_alarm1 | 27/40 | 75.6% [10.3] | 27 | F1: 1, F2: 6, F3: 6 | 3/40 | 43.9% |
| archive_alarm3 | 8/40 | 31.1% [16.5] | 44 | F1: 1, F2: 6, F3: 13, F4: 10, F5: 2 | 0/40 | - |
| watch_000 | 32/40 | 54.3% [41.5] | 20 | F3: 8 | 9/40 | 36.4% |
| watch_100 | 33/40 | 45.7% [30.2] | 28 | F3: 7 | 1/40 | 30.1% |
| watch_010 | 35/40 | 67.7% [41.5] | 20 | F3: 5 | 4/40 | 36.4% |
| watch_110 | 32/40 | 44.2% [34.3] | 29 | F3: 8 | 0/40 | - |
| watch_001 | 32/40 | 30.8% [18] | 20 | F3: 8 | 9/40 | 12.9% |
| watch_101 | 33/40 | 22.2% [6.7] | 28 | F3: 7 | 1/40 | 6.6% |
| watch_011 | 35/40 | 44.2% [18] | 20 | F3: 5 | 4/40 | 12.9% |
| watch_111 | 32/40 | 20.6% [10.8] | 29 | F3: 8 | 0/40 | - |
| cache_right | 40/40 | 56.8% [56.8] | 9 | none | 39/40 | 23.9% |
| cache_wrong | 40/40 | 56.8% [45] | 14 | none | 35/40 | 20.1% |

### Per fight

| Path | Fight | Won / reached | Rounds median [p10-p90] | HP start -> end (median, p10 end) | Gross HP lost | Player idle turns | Won / reached (off) | HP end (off) |
|---|---|---:|---|---|---:|---:|---:|---|
| foundry | intake: Deck Warden + Core Canister | 40/40 | 6 [3-6] | 100 -> 83.4 (81.7) | 16.6% | 2.4% | 40/40 | 83.4 |
| foundry | pour hall: Arsenal Keeper + Seal Charge x2 | 40/40 | 7 [4-7] | 83.4 -> 63 (47.8) | 26.7% | 1.3% | 40/40 | 63 |
| foundry | crucible: Foundry Warden + Core Canister **(boss)** | 34/40 | 6 [6-6] | 63 -> 31.7 (17.8) | 30.5% | 6% | 0/40 | - |
| archive_clean | descent: Core Horror | 39/40 | 7 [7-7] | 100 -> 109 (78.2) | -9% | 0% | 21/40 | 33.6 |
| archive_clean | archive: Sealwright **(boss)** | 39/39 | 13 [8-19] | 109 -> 87 (49.3) | 13% | 0.7% | 5/21 | 44.6 |
| archive_alarm1 | descent: Core Horror | 39/40 | 7 [7-7] | 100 -> 109 (78.2) | -9% | 0% | 21/40 | 33.6 |
| archive_alarm1 | alarm 1: Skyglass Sentinel + Seal Charge (alarm debuff) | 33/39 | 11 [7-12] | 109 -> 57.1 (11.5) | 47.9% | 7% | 6/21 | 32.1 |
| archive_alarm1 | archive: Sealwright **(boss)** | 27/33 | 11 [8-19] | 57.1 -> 75.6 (10.3) | 11.8% | 1.8% | 3/6 | 43.9 |
| archive_alarm3 | descent: Core Horror | 39/40 | 7 [7-7] | 100 -> 109 (78.2) | -9% | 0% | 21/40 | 33.6 |
| archive_alarm3 | alarm 1: Skyglass Sentinel + Seal Charge (alarm debuff) | 33/39 | 11 [7-12] | 109 -> 57.1 (11.5) | 47.9% | 7% | 6/21 | 32.1 |
| archive_alarm3 | alarm 2: Skyglass Sentinel + Seal Charge (alarm debuff) | 20/33 | 8 [7-12] | 57.1 -> 32.8 (11.5) | 32.5% | 5.9% | 1/6 | 43.1 |
| archive_alarm3 | alarm 3: Skyglass Sentinel + Seal Charge (alarm debuff) | 10/20 | 9.5 [8-11] | 32.8 -> 23.8 (5) | 23.4% | 6.9% | 1/1 | 22.2 |
| archive_alarm3 | archive: Sealwright **(boss)** | 8/10 | 9.5 [8-13] | 23.8 -> 31.1 (16.5) | 0.9% | 0% | 0/1 | - |
| watch_000 | chart room: Wayfinder | 40/40 | 4 [4-4] | 100 -> 93.4 (67.2) | 6.6% | 1.8% | 40/40 | 93.4 |
| watch_000 | deck: First Blade | 40/40 | 7 [6-7] | 93.4 -> 85.4 (64.8) | -5.4% | 0% | 40/40 | 67.5 |
| watch_000 | helm: The Captain **(boss)** | 32/40 | 10 [9-10] | 85.4 -> 54.3 (41.5) | 31.1% | 14.4% | 9/40 | 36.4 |
| watch_100 | chart room: Wayfinder (term: elementalseal) | 40/40 | 12 [11-17] | 100 -> 78.8 (60) | 21.2% | 9.4% | 26/40 | 60.4 |
| watch_100 | deck: First Blade | 40/40 | 7 [6-7] | 78.8 -> 75.6 (56.8) | -5.4% | 0% | 26/26 | 34.5 |
| watch_100 | helm: The Captain **(boss)** | 33/40 | 10 [9-10] | 75.6 -> 45.7 (30.2) | 31.1% | 13.8% | 1/26 | 30.1 |
| watch_010 | chart room: Wayfinder | 40/40 | 4 [4-4] | 100 -> 93.4 (67.2) | 6.6% | 1.8% | 40/40 | 93.4 |
| watch_010 | deck: First Blade (term: disarm) | 40/40 | 7 [6-7] | 93.4 -> 85.4 (64.8) | -5.4% | 0% | 40/40 | 67.5 |
| watch_010 | helm: The Captain **(boss)** | 35/40 | 10 [9-10] | 85.4 -> 67.7 (41.5) | 31.1% | 13.4% | 4/40 | 36.4 |
| watch_110 | chart room: Wayfinder (term: elementalseal) | 40/40 | 12 [11-17] | 100 -> 78.8 (60) | 21.2% | 9.4% | 26/40 | 60.4 |
| watch_110 | deck: First Blade (term: disarm) | 40/40 | 7 [6-7] | 78.8 -> 75.3 (61.3) | -5.4% | 0% | 26/26 | 34.5 |
| watch_110 | helm: The Captain **(boss)** | 32/40 | 9.5 [9-10] | 75.3 -> 44.2 (34.3) | 31.1% | 14% | 0/26 | - |
| watch_001 | chart room: Wayfinder | 40/40 | 4 [4-4] | 100 -> 93.4 (67.2) | 6.6% | 1.8% | 40/40 | 93.4 |
| watch_001 | deck: First Blade | 40/40 | 7 [6-7] | 93.4 -> 85.4 (64.8) | -5.4% | 0% | 40/40 | 67.5 |
| watch_001 | helm: The Captain (term: healprevent) **(boss)** | 32/40 | 10 [9-10] | 85.4 -> 30.8 (18) | 54.6% | 14.4% | 9/40 | 12.9 |
| watch_101 | chart room: Wayfinder (term: elementalseal) | 40/40 | 12 [11-17] | 100 -> 78.8 (60) | 21.2% | 9.4% | 26/40 | 60.4 |
| watch_101 | deck: First Blade | 40/40 | 7 [6-7] | 78.8 -> 75.6 (56.8) | -5.4% | 0% | 26/26 | 34.5 |
| watch_101 | helm: The Captain (term: healprevent) **(boss)** | 33/40 | 10 [9-10] | 75.6 -> 22.2 (6.7) | 54.6% | 13.8% | 1/26 | 6.6 |
| watch_011 | chart room: Wayfinder | 40/40 | 4 [4-4] | 100 -> 93.4 (67.2) | 6.6% | 1.8% | 40/40 | 93.4 |
| watch_011 | deck: First Blade (term: disarm) | 40/40 | 7 [6-7] | 93.4 -> 85.4 (64.8) | -5.4% | 0% | 40/40 | 67.5 |
| watch_011 | helm: The Captain (term: healprevent) **(boss)** | 35/40 | 10 [9-10] | 85.4 -> 44.2 (18) | 54.6% | 13.4% | 4/40 | 12.9 |
| watch_111 | chart room: Wayfinder (term: elementalseal) | 40/40 | 12 [11-17] | 100 -> 78.8 (60) | 21.2% | 9.4% | 26/40 | 60.4 |
| watch_111 | deck: First Blade (term: disarm) | 40/40 | 7 [6-7] | 78.8 -> 75.3 (61.3) | -5.4% | 0% | 26/26 | 34.5 |
| watch_111 | helm: The Captain (term: healprevent) **(boss)** | 32/40 | 9.5 [9-10] | 75.3 -> 20.6 (10.8) | 54.6% | 14% | 0/26 | - |
| cache_right | dig: Skyglass Sentinel **(boss)** | 40/40 | 9 [9-10] | 100 -> 56.8 (56.8) | 43.2% | 0.8% | 39/40 | 23.9 |
| cache_wrong | wrong cove: Deck Warden + Seal Charge | 40/40 | 5 [3-6] | 100 -> 100.4 (88.2) | -0.4% | 3.2% | 40/40 | 100.4 |
| cache_wrong | dig: Skyglass Sentinel **(boss)** | 40/40 | 9 [9-9] | 100.4 -> 56.8 (45) | 43.2% | 0% | 35/40 | 20.1 |

### Set pieces and behaviour

| Fight (first path seen) | Enemy | Appearances | Mark fired % | Marks / blasts per fight | Blast hit % (on / off) | Windows per fight | Signature % | Idle turns after r2 | Dealt per fight (on / off) |
|---|---|---:|---:|---|---|---:|---:|---:|---|
| intake: Deck Warden + Core Canister | Deck Warden | 40 | 0 | 0 / 0 | - / - | 0 | 45 | 0% | 1090 / 1090 |
| intake: Deck Warden + Core Canister | Core Canister | 40 | 0 | 0 / 0 | - / - | 0 | 97.5 | 10% | 1567 / 1567 |
| pour hall: Arsenal Keeper + Seal Charge x2 | Arsenal Keeper | 40 | 0 | 0 / 0 | - / - | 0 | 0 | 0% | 1290 / 1290 |
| pour hall: Arsenal Keeper + Seal Charge x2 | Seal Charge | 40 | 0 | 0 / 0 | - / - | 0 | 82.5 | 0% | 1694 / 1694 |
| crucible: Foundry Warden + Core Canister | Foundry Warden | 40 | 100 | 2 / 1.6 | 11.1 / 79.6 | 1.2 | 100 | 0% | 3052 / 7069 |
| crucible: Foundry Warden + Core Canister | Core Canister | 40 | 0 | 0 / 0 | - / - | 0 | 100 | - | 1607 / 1607 |
| descent: Core Horror | Core Horror | 40 | 100 | 2.1 / 2 | 15 / 96 | 0 | 100 | 0% | 1792 / 7742 |
| archive: Sealwright | Sealwright | 39 | 100 | 4.4 / 1.5 | 6.8 / 91.5 | 1 | 100 | 12.6% | 1795 / 3511 |
| archive: Sealwright | (clone or summon) | 39 | 100 | 2.8 / 0.6 | 4.5 / 57.1 | 2.8 | 0 | 0% | 0 / 0 |
| alarm 1: Skyglass Sentinel + Seal Charge (alarm debuff) | Skyglass Sentinel | 39 | 100 | 3.3 / 2.2 | 2.3 / 29 | 1 | 100 | 7.5% | 3092 / 3131 |
| alarm 1: Skyglass Sentinel + Seal Charge (alarm debuff) | Seal Charge | 39 | 0 | 0 / 0 | - / - | 0 | 59 | - | 689 / 723 |
| alarm 2: Skyglass Sentinel + Seal Charge (alarm debuff) | Skyglass Sentinel | 33 | 93.9 | 2.8 / 1.8 | 1.6 / 25 | 0.9 | 93.9 | 5.7% | 2997 / 2925 |
| alarm 2: Skyglass Sentinel + Seal Charge (alarm debuff) | Seal Charge | 33 | 0 | 0 / 0 | - / - | 0 | 57.6 | - | 672 / 584 |
| alarm 3: Skyglass Sentinel + Seal Charge (alarm debuff) | Skyglass Sentinel | 20 | 100 | 2.4 / 1.7 | 3 / 100 | 1 | 100 | 6.1% | 2563 / 3230 |
| alarm 3: Skyglass Sentinel + Seal Charge (alarm debuff) | Seal Charge | 20 | 0 | 0 / 0 | - / - | 0 | 75 | - | 876 / 0 |
| chart room: Wayfinder | Wayfinder | 40 | 100 | 1.2 / 1.1 | 34.9 / 37.5 | 0 | 100 | 0% | 1379 / 1379 |
| deck: First Blade | First Blade | 40 | 100 | 2 / 0.7 | 0 / 100 | 0.5 | 70 | 38.3% | 1592 / 3608 |
| helm: The Captain | The Captain | 40 | 95 | 3.6 / 2.4 | 6.3 / 39 | 0 | 95 | 0% | 5072 / 9028 |
| chart room: Wayfinder (term: elementalseal) | (clone or summon) | 20 | 100 | 1 / 1 | 0 / 25 | 0 | 0 | 17.5% | 0 / 0 |
| dig: Skyglass Sentinel | Skyglass Sentinel | 40 | 100 | 3 / 2.2 | 0 / 40 | 1 | 100 | 2.9% | 2687 / 4440 |
| wrong cove: Deck Warden + Seal Charge | Deck Warden | 40 | 0 | 0 / 0 | - / - | 0 | 42.5 | 0% | 960 / 960 |
| wrong cove: Deck Warden + Seal Charge | Seal Charge | 40 | 0 | 0 / 0 | - / - | 0 | 50 | - | 584 / 584 |

Dodge totals (all paths, dodge on): {"threatened": 2598, "dodged": 2425, "failedRooted": 135, "failedNoPath": 38, "failedOther": 0, "stepsTaken": 4170}


### Reference runs (`results/hunts_reference.json`, 40 seeds, dodge on; not the build)

| Case | Path | Win | End HP median [p10] | Notes |
|---|---|---:|---|---|
| Build (for comparison) | archive_alarm1 | 27/40 | 75.6% [10.3] | Sentinel + Seal Charge under ALARM |
| Build | archive_alarm3 | 8/40 | 31.1% [16.5] | |
| Alarm fights: Sentinel only (no Seal Charge) | archive_alarm1 | 35/40 | 53.6% [20.8] | each alarm fight F2 37/39 |
| Alarm fights: Sentinel only | archive_alarm3 | 0/40 | - | attrition: F3 33/37, F4 2/33 (three 16k-HP Sentinels in a row) |
| Sealwright without the shared Ward of Command rule | archive_clean | 39/40 | 93.8% [52.7] | 8 rounds (build: 13) |
| Sealwright without Ward | archive_alarm1 | 31/40 | 50.9% [14.9] | |

Dropping the Seal Charge helps one alarm fight but not three: the alarm3 path is attrition from the boss-tuned shared
Sentinel. Ward of Command on himself lengthens the Sealwright fight (13 vs 8 rounds) but barely changes the win rate.

## Reading against the goals

- **Won most of the time by a player who reads the marks** (dodge on):

  | Path | Wins |
  |---|---|
  | Foundry | 34/40 (85%) |
  | Archive, clean | 39/40 |
  | Watch, every term combination | 32-35/40 (80-88%) |
  | Cache, both coves | 40/40 |

- **Marks are the fight** (dodge off):
  - Foundry 0/40; Archive clean 5/40; Watch 0-9/40.
  - The Foundry Warden's Quench hits 80% of the time with dodge off and 11% with it on.
  - The Core Horror's blasts hit 96% (off) against 15% (on).
- **The boss fight is the hardest fight** on every path except the Archive (below). Gross HP lost:

  | Hunt | Earlier fights | Boss |
  |---|---|---|
  | Foundry | 17%, 27% | 31% |
  | Watch | Wayfinder 7%, First Blade −5% (with no terms) | Captain 31%, 55% under healprevent |
  | Cache | wrong-cove fight 0% | Sentinel 43% |

  - Every Watch loss is at the Captain.
  - Every Foundry loss is at the Warden.
- **Terms in the Watch** make the hunt riskier mainly by draining HP; the win rate barely moves:
  - Median end HP: 54% with no terms, 21% with all three.
  - p10 end HP drops to 7-11% with healprevent.
  - Wins stay at 80-88%.
  - What each term does:
    - **elementalseal** turns the Wayfinder fight from 4 rounds into 12.
    - **healprevent** blocks the Kitsune absorb heal: the Captain fight costs 55% instead of 31%.
    - **disarm** does nothing to this build, which carries no weapon.
- **Archive alarm paths** are the exception to "most of the time". This is set by the shared Sentinel record (next
  section).

## Doesn't work as designed

1. **The alarm paths are hard: alarm1 27/40, alarm3 8/40.**
   - The cause is the shared Sentinel record. The live Sentinel is both the Cache boss and the Archive alarm guard, so
     it has one set of stats. Tuned as a boss fight that costs about 43% gross, each alarm fight with a Seal Charge
     costs about 48%.
   - The deaths are mostly from one combination: a Core Rupture stun (2 rounds) followed by an Eruption: Rows on the
     stunned player.
   - Three alarm fights in a row win 20%.
   - Dropping the Seal Charge (reference above) lifts alarm1 to 35/40 but alarm3 falls to 0/40: three 16k-HP
     Sentinels in a row are attrition, so the composition does not fix it.
   - The real lever is a separate, lighter alarm-guard record (a hunt-only AI id in the generator), or a
     lighter Sentinel and a weaker Cache boss. Both are director calls; the build keeps the generator's composition.
2. **The Sealwright's shared Ward of Command lands on himself when he fights solo.**
   - `HIGHEST_MAX_HEALTH_ALLY` includes the caster, and allies here are only him and his echo. So Ward of Command (80%
     damage reduction, 2 rounds, cooldown 2) self-casts, and so does Mending Seal.
   - Before the library's mark-then-end-turn rules, he was unkillable: 37-round wipes.
   - With them, Ward lands only in turns with no set piece, and the fight is winnable: 13 rounds, gross loss 13%.
   - Section 4b lists no Ward. Without it (reference above) the fight is 8 rounds instead of 13, with almost the same
     win rate. Whether the shared rule should stay is a director call.
   - The clean Archive's boss costs only 13% gross: the Sealwright is the hardest fight there, but not a hard fight.
     Pools 2.5 made it 14/20 in a sweep, so 2-2.5 is the band for the director to pick.
3. **First Blade: Glassveil Step kills him** (shared kit; affects the dungeon copy too).
   - While stealthed he can cast nothing, and no rule matches. The engine's give-up path then sets his HP to 0
     (`ai_v2.ts`, "exhausted and has to give up").
   - In the hunts I appended a rule, "end turn: hold while veiled". No shared rule was removed.
   - He now lives about 7 rounds and spends the veiled turns idle: 38% idle after round 2.
4. **Library gaps.**
   - **Tide Line push:** the shared rows blast has no push, so Tide Line deals damage only. Pushing needs a CHARACTER
     rows blast with a push row (a new record, or a push on the shared one).
   - **Archive Lock:** there is no shared violet field blast, so it uses Command Absolute as it is. Its battle line
     ("Kneel.") is the Crowned Captain's. Its own line needs a separate record (+1).
   - **Low Tide** cannot follow the surf: the 100 AP blast leaves no AP. It is cast in the Tide Line mark's turn, so
     the window covers the player's dodge turn.
   - **Lowered Guard has cooldown 99,** so Low Tide happens once per fight, not after every Tide Line.
   - **Overpour** ("two channels at once") has no second pattern in the library. It is expressed as Pour Line jumping
     ahead of Quench under 50%.
   - **Binding: Seal Lines** carries `seal` and `elementalseal` rows without `friendlyFire`. In a probe build they
     sealed the Sealwright's own echo when it stood on the lines. The library's owner should set ENEMIES on them.
5. **Not expressible.**
   - **Wayfinder "repositions to empty ground":** there is no "away from the player" ground target, and Body Flicker at
     `EMPTY_GROUND_CLOSEST_TO_SELF` only hops 1 hex. Left out.
   - **Foundry Warden "never leaves the crucible":** he walks to his Core Canister (`LOWEST_MAX_HEALTH_ALLY`), then
     holds.
6. **Clones and summons cast the boss's marks.**
   - The Wayfinder's Afterimage Decoy acts on his rules, so it lays Omen: Scatter too.
   - The Sealwright's echo runs the Sentinel's rules, so it lays Tide Line marks and uses its Lowered Guard.
   - This is shown as "(clone or summon)" in the table.
7. **Engine facts that affect the hunts.**
   - The Kitsune +1,200 HP returns at every fight start, worth about 24% per fight.
   - The Core Horror (shared kit, Archive descent) gains the player HP with dodge on (−9% gross). With dodge off it
     loses 19 of 40 runs: Undertow into Collapse, then the Maw.
8. **Player model.** No weapon, no bloodline, no cleanse use. A real player who cleanses Mould Cage, Keelbind or
   Fetters does better.

## Not done / not checked

- No live requests, no browser, no push.
- The `dg-*` shared kits (Captain, Core Horror) will move to the library as the Wreck agent migrates them. The hunt
  records reference whatever ids that produces, and the tuned stats should be re-checked after the merge.
- Images are placeholders (the library's donors).
- Real ids are minted by the builder. The `lib-*`, `hunt-*` and `dg-*` rule references must be remapped.
