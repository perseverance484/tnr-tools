# Ghost Ship / Skyglass — final 2/2 items and Crowned Captain support: offline results

**Status:** r2 (director decisions 2026-10-12 applied); INDEPENDENT REVIEW PENDING. r1 was frozen at `4369f404dbfd83563d11508c2bcc2e0e17f9a786`. r2 changes only the Crystal record (RUL-2026-10-12-005: 12-Filament recipe restored, `canBeCrafted:true`, 20 undecided fields mirrored from the live Heal Crystal III row captured by push/87) and the CONTRACT/GUARDS tests for it. Katana, ACTIVE and CROWNED are unchanged in behaviour. Every gate (M0, CONTRACT, GUARDS, ACTIVE, CROWNED) passes on its stated scope. This report gives measurements. It does not accept balance, presentation, Crystal carrier values, publication or a manifest.

**Date:** 2026-10-12. **Implementer:** Fable (Claude Code). **Reviewer:** ChatGPT, at the frozen SHA. **Decisions:** dauntless.
**Governing briefs** (design commit `8a78115367feda143e9591f524b739a7d56330af`, which carries RUL-2026-10-12-001…007 on top of `fd7f0217…`): `state/prompt_ghost_ship_skyglass_final_item_revalidation.md` (RUL-2026-10-11-006) and `state/ghost_ship_skyglass_crowned_support_behavior.md` (RUL-2026-10-11-007/008).
**Harness:** `harness/ghost_ship_final/`. **Records:** `state/ghost_ship_skyglass_final_item_records.json`.

## 1. Gate summary

| Gate | Result | Scope | Evidence |
| --- | --- | --- | --- |
| **M0** | PASS, 482/0 | Unchanged r4 repository verifier; approved packets still resolve | `results/m0.json` |
| **CONTRACT** | PASS, 19/0 | Both complete final records through the pinned `ItemValidator`; exact r4 and 3/3 deltas; capture/packet hashes; instant-Consume negative control | `results/contract.json` |
| **GUARDS** | PASS, 24/0 | Real `imbueItem` / `craftItem` pre-write paths with a write-trapping stub: final LEGENDARY Crystal eligibility, Katana exclusion, hidden states, 12-Filament recipe (Forgemaster reaches the write; 11 Filaments, Master rank, hidden and wrong occupation rejected), native rank matrices | `results/guards.json` |
| **ACTIVE** | PASS, 81/0 | Real assembly and actions at 2/2: activation, granting/later hits, final eligible and first ineligible hit, independent shield expiry, overlap observation, Clear, Buff Prevent/immunity, costs/cooldown/range; upstream processor probes at 2/2 | `results/active.json` |
| **CROWNED** | PASS, 36/0 | Rule schema; heal boundary and fall-through; Copy trigger vs copied effects; selector, summons, path distance, precedence over S31; Reflect; captured/dormant/support fight comparison | `results/crowned.json` |

`bun test`: **45 pass, 0 fail, 218 expect() calls, 3 files.** The evidence checker passes all five gates, and the negative self-test enforces 5/5 probes. All 1,780 pinned engine files were verified unchanged before and after the run. Two full runs produced byte-identical `m0/contract/guards/active/crowned.json`.

## 2. Final item records (RUL006)

**Katana** = Night's Testament baseline + RUL004/005/006 overrides. Compared with the r4 record, the only changes are Consume power 40→15, `rounds` 0→2 and `shieldRounds` 3→2. Compared with the 3/3 carrier, only `rounds` and `shieldRounds` change (3→2). All 65 non-override fields equal the capture. The full validator accepts it.

**Crystal** = live Heal Crystal III mirror (`iJM0kb1i6iNXjADJlZGV_`, push/87 capture `harvests/inbox/tnr_results_1791766317760.json`) + ruling overrides:
- **Decided fields:** CRYSTAL, WEAPON-only, exactly one Consume10 (2/2), LEGENDARY, `canBeTraded:true`, **`canBeCrafted:true` with `craftingRequirements: [{ids:["@item:skyglass_filament"], number:12}]`** (RUL-2026-10-12-005).
- **Set from the rulings:** `inShop:false` (acquisition is the 3% Reliquary drop or the recipe) and `hidden:true` (creation doctrine).
- **Mirrored (RUL-2026-10-12-005):** the 20 fields no ruling sets equal the Heal Crystal III row, for example actionCostPerc 60, chakra/stamina 0, cooldown 5, cost 1, craftingExperience 800, target CHARACTER, requiredLevel 1, xpToLevel 1000. The packet lists them under `crystal.mirroredFields`; CONTRACT asserts each one. r1's 14 Flaming Sword shape-donor values are superseded.
- **Absent fields:** the auction price bounds and purchase limits are absent and take validator defaults.
- **Presentation:** pending; validation uses labelled placeholders.

## 3. Items at runtime (2/2)

- **Activation:** equipping grants nothing. The first weapon use converts its own hit (Katana 15%, Crystal 10%). Later actions convert, both in the same round and the next.
- **Lifetimes:** the buff has `rounds` 2, 2, 1 at offsets 0, 1, 2 and is gone at +3. The granting shield follows the same pattern.
  - The final eligible hit (+2) converts.
  - The first ineligible hit (+3) deals damage but earns no shield.
  - A shield earned at +2 outlives the buff: 2 at +3, 1 at +4, gone at +5.
  - The Crystal shows the same pattern.
- **Overlap (director-deferred; observed only):**
  - Same-action SELF dedupe is unchanged: the weapon's own Consume15 wins, and two Crystals on one weapon still give 10%.
  - **New at 2/2:** the shared Consume GCD (3 rounds) outlasts the 2-round buff. A second Crystal weapon is unavailable at +1 and +2, becomes usable at +3, and by then the first buff has expired. It converts 10%, not 20%.
  - The 3/3 package's 10+10→20% overlap therefore does not arise through separate weapon casts at the approved timing. No correction or restriction was made.
- **Unchanged behaviour:**
  - Pre-shield conversion basis, and Pierce destroying a target shield.
  - ALL-method aggregation control.
  - Clear removes item Consume.
  - Existing Buff Prevent does not suppress Consume.
  - Katana immunity blocks new Buff Prevent at offsets 0/1/2 and lets it land at +3.
  - Katana AP 40, costs 40/40/0, range 4, cooldown 6, shared GCD 3.
- **Processor probes** (upstream fixtures, now at 2/2): damage attribution, delayed/reflect/self/recoil handling, the ratio cap and the per-shield ceiling are unchanged.

## 4. Eligibility, crafting and trade

- **Imbue:**
  - The final LEGENDARY Crystal, in its published state, on an eligible imbuable WEAPON at Forgemaster passes every tested pre-write guard and reaches the first (trapped) write.
  - Native rank gate: only Forgemaster can imbue a LEGENDARY Crystal.
  - As created (`hidden:true`), the Crystal is invisible to `imbueItem` ("Crystal not found").
  - The non-imbuable Katana rejects it. Non-WEAPON, duplicate, slot-limit, equipped, occupation, auction-reserved and required-skill guards are unchanged.
- **Craft (r2, recipe restored):**
  - The final Crystal (published state) with 12 Filaments held at Forgemaster passes every pre-write craft guard and reaches the trapped first write (a DB transaction).
  - 11 Filaments: "You need 12 Skyglass Filament (harness carrier) (you have 11)". Master rank: "You need to be at least Forgemaster rank to craft LEGENDARY items". As created (`hidden:true`): "This item is hidden and cannot be crafted". GATHERING/HUNTING/no occupation are rejected.
  - The native rank × rarity control matrix is unchanged.
- **Trade:** `canBeTraded:true` is stored and survives validation, with no auction price bounds. This is **record/schema evidence only**. The source auction guard (`routers/auction.ts`, "Item is not tradable") was not executed, and no committed trade is claimed.
- **Boundary:** GUARDS stops at the first write. Persistence, CAS/concurrency, a completed craft or imbue, and an executed trade are not exercised.

## 5. Crowned Captain support

Candidate (concrete implementation for testing): S35 `health_below:40` → B07 (`target_has_effect` IDG ≥ 71, CLOSEST_OPPONENT, `distance_lower_than:5`, same target) → Rebounding Form (no condition) → the prior remapped chain, with `includeDefaultRules` unchanged. All three rules parse with the pinned `AiRule` schema. The three techniques are the preserved captured records (Reflect keeps its fractional 0.05 pool costs). All eleven members are kept, and the regular Captain is untouched.

**Heal (strict boundary, approved):**
- At engine ratio exactly 40.000, the Captain does not heal; at 40.1% it does not either.
- At 39.9% and at 20% it casts S35 and heals 2,727 HP = 15% of base max HP (18,180; the effective max equals the base max).
- Fall-through:
  - On cooldown → Reflect.
  - At 30 AP → move.
  - Under Heal Prevent, S35 is still selected but heals 0 ("cannot be healed"). The action is wasted.
- At low HP without high IDG, the round goes S35 (100 AP) → Reflect (60 AP) → move (20 AP). Heal plus Reflect displaces any 60-AP attack that round.

**Copy (IDG ≥ 71, approved):**
- IDG 30, 70 and 70.5 do not trigger Copy; the next rule is Reflect. IDG 71 and 90 trigger it.
- Copy is broad: IDG 90, DDT 40 and increasestat 20 were all cloned onto the Captain for 3 rounds, and the opponent keeps all three.
- Summed IDG 40 + 35 triggers, but copies one IDG (the stronger 40), not 75.
- Raw IDG triggers an **empty Copy** when the source is expired (`rounds:0`), bloodline-protected or item-sourced: nothing is copied ("finds no copyable effects").
- Buff Prevent on the Captain lets B07 be cast but copies nothing. A full 4-type copy budget copies nothing new.
- **Selector:**
  - A closest low-IDG summon blocks Copy even when a farther player has IDG 90.
  - A buffed closest summon triggers Copy and is the copy source.
  - Copy fires at path distance 4 and 5 and not at 6.
  - Against an adjacent IDG-90 player, the support candidate copies before Clear, while the prior dormant chain uses S31.

**Reflect (regular rotation, approved):**
- It is cast at full HP both far (hex 6) and near (hex 2); there is no inherited gate.
- The round after casting it, a player hit of 763.9 returns 267 (35%, floored) to the player. The Captain's own HP loss is **unchanged** at 763.9, so Reflect is not damage reduction.
- Buff Prevent applied before the cast stops the return.
- Lifetime: `rounds` 2, 2, 1, then gone at +3. Cooldown 4: Reflect is unavailable through +3 and available at +4.

**Fight comparison** (mean of 3 seeds; Captain at (8,4), player at (2,4); 40-round cap; boss always won 3/3):

| Player fixture | Variant | Rounds | Player dmg to boss | Boss HP left | Heals / HP | Copies / effects | Reflects / dmg returned | Offensive AP per round |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| JONIN cap, buffer | captured / dormant | 3 / 3 | 557 / 557 | 96.9% / 96.9% | 0 | 0 | 0 | 100 / 100 |
| | support | 4 | 2,765 | 84.8% | 0 | 1 / 3 | 1 / 954 | 75 |
| JONIN cap, striker | captured / dormant | 4 / 4 | 1,517 / 1,517 | 91.7% / 91.7% | 0 | 0 | 0 | 85 / 85 |
| | support | 4 | 1,888 | 89.6% | 0 | 0 | 1 / 358 | 85 |
| JONIN half, moderate | captured / dormant | 3 / 3 | 374 / 374 | 97.9% / 97.9% | 0 | 0 | 0 | 100 / 100 |
| | support | 3 | 374 | 97.9% | 0 | 0 | 1 / 130 | 86.7 |
| Durable, buffer | captured / dormant | 5 / 6 | 1,211 / 1,375 | 93.3% / 92.4% | 0 | 0 | 0 | 92 / 92 |
| | support | 6 | 2,962 | 83.7% | 0 | 1 / 3 | 2 / 988 | 70 |
| Durable, striker | captured / dormant | 11 / 12 | 4,965 / 5,620 | 72.7% / 69.1% | 0 | 0 | 0 | 72.7 / 75 |
| | support | 12 | 4,736 | 73.9% | 0 | 0 | 3 / 901 | 70 |
| Durable, moderate | captured / dormant | 5 / 6 | 1,080 / 1,080 | 94.1% / 94.1% | 0 | 0 | 0 | 92 / 92 |
| | support | 12 | 2,572 | 85.9% | 0 | 0 | 3 / 392 | 70 |
| **Forced 45% start**, durable buffer | dormant | 6 | 1,375 | 37.4% | 0 | 0 | 0 | 92 |
| | support | 12 | 4,182 | 52.0% | 2 / 5,454 | 2 / 5 | 3 / 1,216 | 63.3 |
| **Forced 45% start**, durable striker | dormant | 12 | 5,620 | 14.1% | 0 | 0 | 0 | 75 |
| | support | 11 | 5,675 | 43.8% | 2 / 5,454 | 0 | 3 / 1,118 | 69.1 |

**Material difficulty changes, reported before any tuning (none applied):**
1. **Lower offensive tempo.**
   - Support actions cost 10–27 AP per round. Offensive AP per round falls in five of six fixtures (for example 92 → 70 and 100 → 75); the JONIN-cap striker is unchanged at 85.
   - Several fights take longer: durable moderate goes from 6 to 12 rounds, and JONIN-cap buffer from 3 to 4.
   - Players therefore deal more total damage before dying: up to about 5× against the JONIN-cap buffer (557 → 2,765).
2. **Higher survivability when hurt.**
   - From a forced 45% start, the Captain heals twice (5,454 HP).
   - It ends at 52.0% instead of 37.4% against the durable buffer, and at 43.8% instead of 14.1% against the durable striker.
   - In the unforced fights no fixture took the Captain below 40%, so no heal was cast there.
3. **Copy fires only against the IDG buffers.** It fires once per buffer fight (3 effects) and twice in the forced buffer fight; it never fires against strikers or moderates.
4. **Reflect fires in every matchup**, returning 130–1,216 damage per fight.
5. **No change in outcome.** The Captain won all 66 fights (54 comparison fights and 12 forced-start fights). These fixtures don't show Crowned support changing who wins; they show slower, more attritional fights.

Captured and dormant rules never used the three support techniques (control). Five seeds would repeat the same deterministic encounter; these three seeds likewise are not independent win-rate samples.

## 6. Source / runtime / provenance

- Engine `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`, upstream (deployment unverified), exported with `git archive`. All 1,780 pinned app files were checked against their git blobs before and after.
- `bun.lock` sha256 `da6602f2550bea9f1baf8508fa82b03d320bfcee269257f36cf25b47f1906c08`, unchanged from the historical engine. The existing user-approved frozen install was reused; no install was run.
- Bun 1.4.2, Node v22.22.0, Python 3.13.16.
- Isolation mode **unshare**: a private network namespace (`unshare -rn`, available in this container) plus seccomp denial of socket/connect/bind/listen/accept/send/io_uring. Socket-denial preflight passed. The child environment is an `env -i` allowlist with CI placeholders only, and Bun runs with `--no-env-file --no-install`. No database is used; the stub traps writes.
- `results/provenance.json` records the harness file hashes, the final-records hash, the Crowned behaviour hash and all exit statuses.

## 7. Exact commands

```text
export TNR_ENGINE_SRC=<clone with 585534d7> TNR_DEPENDENCIES_APP=<approved frozen install> TNR_ENGINE_WORK=<fresh dir>
python3 harness/ghost_ship_final/tools/build_final_items.py           → wrote state/ghost_ship_skyglass_final_item_records.json
TNR_OUT=<scratch>/fr1 harness/ghost_ship_final/run.sh               → exit 0
  engine export: 1780 pinned files unchanged; offline socket-denial preflight: PASS
  build_final_items.py --check: current; ghost_ship_consume build_item_carriers.py --check: current
  M0 PASS: 482 checks, 0 failed
  bun test: 45 pass, 0 fail, 218 expect() calls, Ran 45 tests across 3 files
  evidence M0/CONTRACT/GUARDS/ACTIVE/CROWNED: clean (482/0, 19/0, 24/0, 81/0, 36/0)
  negative probes: 5/5 enforced; run.sh: bun=0 evidence=0 negativeSelftest=0 source=0 -> exit 0
harness/ghost_ship_final/run.sh   (second run → results/)          → exit 0
  cmp: m0/contract/guards/active/crowned.json byte-identical to the first run
Historical reproduction first: harness/ghost_ship_consume/run.sh → 34 pass/0 fail/195 expects, evidence byte-identical to fcd79e5
```

## 8. Remaining decisions and gaps (director)

- **Crowned support:** accept or adjust the rule order (Heal → Copy → Reflect → offense), the CLOSEST_OPPONENT selector and the measured tempo/survivability change. The approved triggers (strict < 40, IDG ≥ 71) are closed.
Settled 2026-10-12 (RUL-2026-10-12-001…008): Crowned support accepted as tested; Sealwright accepted as final (not tested here); nine-AI remap approved; minion IDG kept with boss IDG 375/375/450; recipe restored and Crystal mirrored (this r2); overlap closed as native; Filament MATERIAL/RARE/tradable; source-default damage settings accepted with live tester calibration.

Still open:
- **Presentation and art** for Katana, Crystal, Reliquary, Filament and Serum: supplied by the director (art zip last).
- **Fresh operator quest capture** (push/89) before any quest edit; the legacy packet hash re-baseline.

## 9. Not done

Live-game requests 0, writes 0, CDN requests 0, credentials none. No engine edit (including in scratch), tuning, art, manifest, publication, unhiding or quest edit. Frozen r4 and 3/3 harnesses, records and results are unchanged. The r1 SHA `4369f404…` is untouched. The global September Forge state was not touched. Nothing is on `main`.
